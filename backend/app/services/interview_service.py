"""Interview service.

Owns the interview session lifecycle (create → ready → in_progress → completed
/cancelled), AI question generation, sequential question delivery, and text
answer submission.

Design notes / documented mappings (see current-state.md flagged conflicts):
* API ``mode`` (voice/text) is persisted as ``interviews.interview_type``.
* API ``interview_type`` (technical/behavioral/mixed) steers question generation
  but has no dedicated column; it is passed to the AI as configuration.
* ``target_role`` / ``experience_level`` / salary are sourced from the user's
  candidate preferences when available.
* Question generation runs synchronously (Version 1 excludes background workers).
* Voice answers/transcription are a later increment; v1 handles text answers.
"""

from __future__ import annotations

import json
import uuid
from datetime import UTC, datetime

from sqlalchemy.ext.asyncio import AsyncSession

from app.ai.service import AIService
from app.core.config import get_settings
from app.core.logging import get_logger
from app.exceptions.base import (
    AnswerAlreadyExistsError,
    AnswerNotFoundError,
    FileTooLargeError,
    InterviewNotFoundError,
    InvalidInterviewStateError,
    QuestionNotFoundError,
    ResumeNotFoundError,
    StorageUnavailableError,
    UnsupportedFileError,
)
from app.models.enums import (
    AnswerType,
    AuditEventType,
    ExperienceLevel,
    InterviewStatus,
    SubmissionStatus,
)
from app.models.interview import Interview
from app.models.interview_answer import InterviewAnswer
from app.models.interview_question import InterviewQuestion
from app.repositories.interview_repository import (
    InterviewAnswerRepository,
    InterviewQuestionRepository,
    InterviewRepository,
)
from app.repositories.preferences_repository import CandidatePreferencesRepository
from app.repositories.resume_repository import CandidateProfileRepository, ResumeRepository
from app.schemas.interview import InterviewCreate
from app.services.audit_service import AuditService
from app.services.storage import StorageProvider

logger = get_logger(__name__)

_CANCELLABLE = {InterviewStatus.CREATED, InterviewStatus.READY, InterviewStatus.IN_PROGRESS}

# Voice answers (docs/05-api-design/answers.md): WAV/MP3/WEBM/M4A, up to 25 MB.
MAX_AUDIO_BYTES = 25 * 1024 * 1024
_AUDIO_EXT = {
    "audio/wav": ".wav",
    "audio/x-wav": ".wav",
    "audio/mpeg": ".mp3",
    "audio/mp3": ".mp3",
    "audio/webm": ".webm",
    "audio/mp4": ".m4a",
    "audio/x-m4a": ".m4a",
    "audio/m4a": ".m4a",
}
_AUDIO_SUFFIXES = (".wav", ".mp3", ".webm", ".m4a")


def _ensure_aware(value: datetime) -> datetime:
    """Treat a naive datetime as UTC.

    PostgreSQL returns timezone-aware datetimes for ``TIMESTAMPTZ`` columns, but
    SQLite (used in tests) returns naive ones. Normalising here keeps arithmetic
    against ``datetime.now(UTC)`` correct on both backends.
    """
    return value if value.tzinfo is not None else value.replace(tzinfo=UTC)


def _map_experience_level(years: int | None) -> ExperienceLevel:
    if years is None:
        return ExperienceLevel.MID
    if years <= 0:
        return ExperienceLevel.FRESHER
    if years < 2:
        return ExperienceLevel.JUNIOR
    if years < 5:
        return ExperienceLevel.MID
    return ExperienceLevel.SENIOR


class InterviewService:
    def __init__(
        self, session: AsyncSession, ai_service: AIService, storage: StorageProvider | None = None
    ) -> None:
        self.session = session
        self.ai = ai_service
        self.storage = storage
        self.interviews = InterviewRepository(session)
        self.questions = InterviewQuestionRepository(session)
        self.answers = InterviewAnswerRepository(session)
        self.resumes = ResumeRepository(session)
        self.profiles = CandidateProfileRepository(session)
        self.preferences = CandidatePreferencesRepository(session)
        self.audit = AuditService(session)

    # ------------------------------------------------------------------ #
    # Creation + generation                                              #
    # ------------------------------------------------------------------ #
    async def create(self, user, payload: InterviewCreate) -> Interview:
        resume = await self.resumes.get(payload.resume_id)
        if resume is None or resume.user_id != user.id:
            raise ResumeNotFoundError()

        prefs = await self.preferences.get_by_user_id(user.id)
        target_role = prefs.target_role if prefs else "Software Engineer"
        experience_level = _map_experience_level(prefs.experience_years if prefs else None)
        expected_salary = prefs.expected_salary_max if prefs else None
        ai_model = get_settings().GROQ_MODEL

        interview = Interview(
            user_id=user.id,
            resume_id=resume.id,
            title=f"{target_role} Mock Interview",
            interview_type=payload.mode,
            interviewer_voice=payload.interviewer_voice,
            target_role=target_role,
            expected_salary=expected_salary,
            experience_level=experience_level,
            difficulty=payload.difficulty,
            ai_model=ai_model,
            status=InterviewStatus.CREATED,
        )
        self.interviews.add(interview)
        await self.interviews.flush()

        await self._generate_questions(interview, payload, resume_id=resume.id)

        await self.audit.log(
            event_type=AuditEventType.INTERVIEW,
            action="CREATE_INTERVIEW",
            user_id=user.id,
            resource_type="interview",
            resource_id=interview.id,
            metadata={"status": interview.status},
        )
        return interview

    async def _generate_questions(
        self, interview: Interview, payload: InterviewCreate, *, resume_id: uuid.UUID
    ) -> None:
        try:
            profile_summary = await self._build_profile_summary(interview, resume_id)
            config = json.dumps(
                {
                    "target_role": interview.target_role,
                    "experience_level": interview.experience_level,
                    "difficulty": interview.difficulty,
                    "category": payload.interview_type,
                    "language": payload.language,
                    "question_count": payload.question_count,
                }
            )
            question_set, meta = await self.ai.generate_questions(
                profile_summary=profile_summary, config=config, count=payload.question_count
            )
            for index, generated in enumerate(question_set.questions, start=1):
                self.questions.add(
                    InterviewQuestion(
                        interview_id=interview.id,
                        question_number=index,
                        category=generated.category,
                        difficulty=generated.difficulty,
                        question_text=generated.question_text,
                        expected_answer_points=generated.expected_answer_points,
                        evaluation_rubric=generated.evaluation_rubric,
                        estimated_time_seconds=generated.estimated_time_seconds,
                        ai_model=meta.model,
                        generation_prompt_version=meta.prompt_version,
                    )
                )
            interview.total_questions = len(question_set.questions)
            interview.ai_model = meta.model
            interview.status = InterviewStatus.READY
            logger.info("interview_questions_generated", extra={"interview_id": str(interview.id)})
        except Exception:
            interview.status = InterviewStatus.FAILED
            logger.exception(
                "interview_generation_failed", extra={"interview_id": str(interview.id)}
            )
        finally:
            await self.interviews.flush()

    async def _build_profile_summary(self, interview: Interview, resume_id: uuid.UUID) -> str:
        profile = await self.profiles.get_by_resume_id(resume_id)
        parts: list[str] = [f"Target role: {interview.target_role}"]
        if profile is not None:
            if profile.professional_summary:
                parts.append(f"Summary: {profile.professional_summary}")
            if profile.skills:
                names = [s.get("name") for s in profile.skills if isinstance(s, dict)]
                parts.append("Skills: " + ", ".join(n for n in names if n))
        return "\n".join(parts)

    # ------------------------------------------------------------------ #
    # Retrieval                                                          #
    # ------------------------------------------------------------------ #
    async def get_owned(self, user, interview_id: uuid.UUID) -> Interview:
        interview = await self.interviews.get(interview_id)
        if interview is None or interview.user_id != user.id:
            raise InterviewNotFoundError()
        return interview

    async def list_for_user(self, user, **kwargs) -> tuple[list[Interview], int]:
        return await self.interviews.list_paginated(user.id, **kwargs)

    def build_status(self, interview: Interview) -> dict:
        answered = interview.answered_questions
        remaining = max(interview.total_questions - answered, 0)
        in_progress = interview.status == InterviewStatus.IN_PROGRESS
        current = answered + 1 if in_progress and remaining else None
        elapsed = None
        if interview.started_at is not None:
            end = (
                _ensure_aware(interview.completed_at)
                if interview.completed_at
                else datetime.now(UTC)
            )
            elapsed = int((end - _ensure_aware(interview.started_at)).total_seconds())
        return {
            "status": interview.status,
            "current_question": current,
            "completed_questions": answered,
            "remaining_questions": remaining,
            "elapsed_seconds": elapsed,
        }

    # ------------------------------------------------------------------ #
    # State transitions                                                  #
    # ------------------------------------------------------------------ #
    def _require_status(self, interview: Interview, *allowed: str) -> None:
        if interview.status not in allowed:
            raise InvalidInterviewStateError()

    async def start(self, user, interview_id: uuid.UUID) -> Interview:
        interview = await self.get_owned(user, interview_id)
        self._require_status(interview, InterviewStatus.READY)
        interview.status = InterviewStatus.IN_PROGRESS
        interview.started_at = datetime.now(UTC)
        await self.interviews.flush()
        return interview

    async def acknowledge_pause(self, user, interview_id: uuid.UUID) -> Interview:
        # Version 1 keeps no server-side paused state (no such column); the
        # client owns the timer. We validate state and acknowledge.
        interview = await self.get_owned(user, interview_id)
        self._require_status(interview, InterviewStatus.IN_PROGRESS)
        return interview

    async def complete(self, user, interview_id: uuid.UUID) -> Interview:
        interview = await self.get_owned(user, interview_id)
        self._require_status(interview, InterviewStatus.IN_PROGRESS)
        interview.status = InterviewStatus.COMPLETED
        interview.completed_at = datetime.now(UTC)
        if interview.started_at is not None:
            interview.duration_seconds = int(
                (interview.completed_at - _ensure_aware(interview.started_at)).total_seconds()
            )
        await self.interviews.flush()
        await self.audit.log(
            event_type=AuditEventType.INTERVIEW,
            action="COMPLETE_INTERVIEW",
            user_id=user.id,
            resource_type="interview",
            resource_id=interview.id,
        )

        # Trigger evaluation + report generation synchronously (Version 1 has no
        # worker). Best-effort: a failure here leaves the interview completed but
        # without a report, which can be regenerated by an admin.
        if get_settings().ENABLE_AI_FEEDBACK:
            from app.services.evaluation_service import EvaluationService

            try:
                await EvaluationService(
                    self.session, self.ai, self.storage
                ).run_for_interview(interview)
            except Exception:
                logger.exception(
                    "post_completion_evaluation_failed",
                    extra={"interview_id": str(interview.id)},
                )
        return interview

    async def cancel(self, user, interview_id: uuid.UUID) -> Interview:
        interview = await self.get_owned(user, interview_id)
        self._require_status(interview, *_CANCELLABLE)
        interview.status = InterviewStatus.CANCELLED
        await self.interviews.flush()
        return interview

    async def delete(self, user, interview_id: uuid.UUID) -> None:
        interview = await self.get_owned(user, interview_id)
        await self.interviews.delete(interview)
        await self.interviews.flush()

    # ------------------------------------------------------------------ #
    # Questions                                                          #
    # ------------------------------------------------------------------ #
    async def current_question(self, user, interview_id: uuid.UUID) -> InterviewQuestion:
        interview = await self.get_owned(user, interview_id)
        self._require_status(interview, InterviewStatus.IN_PROGRESS)
        number = interview.answered_questions + 1
        question = await self.questions.get_by_number(interview_id, number)
        if question is None:
            raise QuestionNotFoundError("No further questions.")
        return question

    async def get_question(
        self, user, interview_id: uuid.UUID, question_id: uuid.UUID
    ) -> InterviewQuestion:
        interview = await self.get_owned(user, interview_id)
        question = await self.questions.get(question_id)
        if question is None or question.interview_id != interview_id:
            raise QuestionNotFoundError()
        # During an active interview only the current question is accessible.
        if (
            interview.status == InterviewStatus.IN_PROGRESS
            and question.question_number != interview.answered_questions + 1
        ):
            raise InvalidInterviewStateError("Only the current question is available.")
        return question

    async def list_questions(self, user, interview_id: uuid.UUID) -> list[InterviewQuestion]:
        interview = await self.get_owned(user, interview_id)
        if interview.status != InterviewStatus.COMPLETED:
            raise InvalidInterviewStateError("Questions are available after completion.")
        return await self.questions.list_by_interview(interview_id)

    async def next_question(
        self, user, interview_id: uuid.UUID, question_id: uuid.UUID
    ) -> InterviewQuestion:
        interview = await self.get_owned(user, interview_id)
        self._require_status(interview, InterviewStatus.IN_PROGRESS)
        question = await self.questions.get(question_id)
        if question is None or question.interview_id != interview_id:
            raise QuestionNotFoundError()
        if await self.answers.get_by_question(question_id) is None:
            raise InvalidInterviewStateError("Submit the current answer before advancing.")
        following = await self.questions.get_by_number(interview_id, question.question_number + 1)
        if following is None:
            raise QuestionNotFoundError("No further questions.")
        return following

    # ------------------------------------------------------------------ #
    # Answers                                                            #
    # ------------------------------------------------------------------ #
    async def submit_text_answer(
        self, user, interview_id: uuid.UUID, *, question_id: uuid.UUID, answer: str
    ) -> InterviewAnswer:
        interview = await self.get_owned(user, interview_id)
        self._require_status(interview, InterviewStatus.IN_PROGRESS)

        question = await self.questions.get(question_id)
        if question is None or question.interview_id != interview_id:
            raise QuestionNotFoundError()
        # Re-answering an already-answered question is a distinct, explicit error;
        # check it before the sequential-order rule.
        if await self.answers.get_by_question(question_id) is not None:
            raise AnswerAlreadyExistsError()
        # Enforce sequential answering.
        if question.question_number != interview.answered_questions + 1:
            raise InvalidInterviewStateError("Answer questions in order.")

        record = InterviewAnswer(
            question_id=question_id,
            answer_type=AnswerType.TEXT,
            answer_text=answer,
            submission_status=SubmissionStatus.SUBMITTED,
        )
        self.answers.add(record)
        interview.answered_questions += 1
        await self.answers.flush()
        await self.audit.log(
            event_type=AuditEventType.INTERVIEW,
            action="SUBMIT_ANSWER",
            user_id=user.id,
            resource_type="answer",
            resource_id=record.id,
        )
        return record

    async def submit_voice_answer(
        self,
        user,
        interview_id: uuid.UUID,
        *,
        question_id: uuid.UUID,
        filename: str,
        content_type: str | None,
        data: bytes,
        language: str = "en",
    ) -> InterviewAnswer:
        """Store an audio answer, transcribe it (Groq Whisper), and persist it.

        Version 1 transcribes synchronously (no worker); the response reflects
        the terminal state.
        """
        if self.storage is None:
            raise StorageUnavailableError("Audio storage is not configured.")

        interview = await self.get_owned(user, interview_id)
        self._require_status(interview, InterviewStatus.IN_PROGRESS)

        question = await self.questions.get(question_id)
        if question is None or question.interview_id != interview_id:
            raise QuestionNotFoundError()
        if await self.answers.get_by_question(question_id) is not None:
            raise AnswerAlreadyExistsError()
        if question.question_number != interview.answered_questions + 1:
            raise InvalidInterviewStateError("Answer questions in order.")

        ext = self._validate_audio(filename=filename, content_type=content_type, size=len(data))
        key = f"audio/{interview_id}/{uuid.uuid4()}{ext}"
        storage_path = await self.storage.save(
            key=key, data=data, content_type=content_type or "application/octet-stream"
        )

        transcription = await self.ai.transcribe_audio(
            audio=data, filename=filename, language=language
        )

        record = InterviewAnswer(
            question_id=question_id,
            answer_type=AnswerType.VOICE,
            audio_storage_path=storage_path,
            transcription_text=transcription.text,
            transcription_confidence=transcription.confidence,
            language=transcription.language or language,
            submission_status=SubmissionStatus.SUBMITTED,
        )
        self.answers.add(record)
        interview.answered_questions += 1
        await self.answers.flush()
        await self.audit.log(
            event_type=AuditEventType.INTERVIEW,
            action="SUBMIT_VOICE_ANSWER",
            user_id=user.id,
            resource_type="answer",
            resource_id=record.id,
        )
        return record

    @staticmethod
    def _validate_audio(*, filename: str, content_type: str | None, size: int) -> str:
        if size == 0:
            raise UnsupportedFileError("The audio file is empty.")
        if size > MAX_AUDIO_BYTES:
            raise FileTooLargeError("Maximum audio size is 25 MB.")
        if content_type in _AUDIO_EXT:
            return _AUDIO_EXT[content_type]
        lower = filename.lower()
        for suffix in _AUDIO_SUFFIXES:
            if lower.endswith(suffix):
                return suffix
        raise UnsupportedFileError("Supported audio formats: WAV, MP3, WEBM, M4A.")

    async def get_transcript(
        self, user, interview_id: uuid.UUID, answer_id: uuid.UUID
    ) -> dict:
        answer = await self.get_answer(user, interview_id, answer_id)
        if answer.answer_type != AnswerType.VOICE or not answer.transcription_text:
            raise AnswerNotFoundError("No transcript is available for this answer.")
        return {
            "transcript": answer.transcription_text,
            "confidence": (
                float(answer.transcription_confidence)
                if answer.transcription_confidence is not None
                else None
            ),
            "language": answer.language,
        }

    async def get_answer(
        self, user, interview_id: uuid.UUID, answer_id: uuid.UUID
    ) -> InterviewAnswer:
        await self.get_owned(user, interview_id)
        answer = await self.answers.get(answer_id)
        if answer is None:
            raise AnswerNotFoundError()
        question = await self.questions.get(answer.question_id)
        if question is None or question.interview_id != interview_id:
            raise AnswerNotFoundError()
        return answer

    async def list_answers(self, user, interview_id: uuid.UUID) -> list[InterviewAnswer]:
        interview = await self.get_owned(user, interview_id)
        if interview.status != InterviewStatus.COMPLETED:
            raise InvalidInterviewStateError("Answers are available after completion.")
        return await self.answers.list_by_interview(interview_id)
