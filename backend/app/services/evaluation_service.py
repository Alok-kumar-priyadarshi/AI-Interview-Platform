"""Evaluation & report service.

Runs the post-completion pipeline: evaluate each answer with the AI, persist one
:class:`Evaluation` per answer, aggregate into a single :class:`Report`, and set
the interview's overall score. Version 1 runs this synchronously (no workers).

Retrieval/ownership helpers back the evaluation and report APIs.
"""

from __future__ import annotations

import json
import uuid

from sqlalchemy.ext.asyncio import AsyncSession

from app.ai.service import AIService
from app.core.error_codes import ErrorCode
from app.core.logging import get_logger
from app.exceptions.base import (
    AppException,
    EvaluationNotFoundError,
    InterviewNotFoundError,
    ReportNotFoundError,
)
from app.models.enums import AuditEventType, SubmissionStatus
from app.models.evaluation import Evaluation
from app.models.interview import Interview
from app.models.report import Report
from app.repositories.evaluation_repository import EvaluationRepository, ReportRepository
from app.repositories.interview_repository import (
    InterviewAnswerRepository,
    InterviewQuestionRepository,
    InterviewRepository,
)
from app.services.audit_service import AuditService
from app.services.storage import StorageProvider
from app.utils.pdf import build_report_pdf

logger = get_logger(__name__)


def _avg(values: list[float]) -> float | None:
    present = [v for v in values if v is not None]
    return round(sum(present) / len(present), 2) if present else None


class EvaluationService:
    def __init__(
        self, session: AsyncSession, ai_service: AIService, storage: StorageProvider | None = None
    ) -> None:
        self.session = session
        self.ai = ai_service
        self.storage = storage
        self.evaluations = EvaluationRepository(session)
        self.reports = ReportRepository(session)
        self.questions = InterviewQuestionRepository(session)
        self.answers = InterviewAnswerRepository(session)
        self.interviews = InterviewRepository(session)
        self.audit = AuditService(session)

    # ------------------------------------------------------------------ #
    # Pipeline                                                           #
    # ------------------------------------------------------------------ #
    async def run_for_interview(self, interview: Interview) -> Report | None:
        """Evaluate answers and generate the aggregate report (idempotent)."""
        existing = await self.reports.get_by_interview(interview.id)
        if existing is not None:
            return existing

        questions = await self.questions.list_by_interview(interview.id)
        answers = {a.question_id: a for a in await self.answers.list_by_interview(interview.id)}

        evaluations: list[Evaluation] = []
        summaries: list[dict] = []
        for question in questions:
            answer = answers.get(question.id)
            if answer is None:
                continue
            evaluation = await self.evaluations.get_by_answer(answer.id)
            if evaluation is None:
                answer_text = answer.answer_text or answer.transcription_text or ""
                result, meta = await self.ai.evaluate_answer(
                    question=question.question_text,
                    rubric=question.evaluation_rubric or {},
                    answer=answer_text,
                )
                evaluation = Evaluation(
                    answer_id=answer.id,
                    overall_score=result.overall_score,
                    technical_score=result.technical_score,
                    communication_score=result.communication_score,
                    problem_solving_score=result.problem_solving_score,
                    confidence_score=result.confidence_score,
                    strengths=result.strengths,
                    weaknesses=result.weaknesses,
                    improvement_suggestions=result.improvement_suggestions,
                    detailed_feedback=result.detailed_feedback,
                    evaluation_model=meta.model,
                    evaluation_prompt_version=meta.prompt_version,
                    evaluation_duration_ms=meta.duration_ms,
                )
                self.evaluations.add(evaluation)
                answer.submission_status = SubmissionStatus.EVALUATED
            evaluations.append(evaluation)
            summaries.append(
                {
                    "question_number": question.question_number,
                    "question": question.question_text,
                    "overall_score": float(evaluation.overall_score),
                    "strengths": evaluation.strengths,
                    "weaknesses": evaluation.weaknesses,
                }
            )

        await self.evaluations.flush()

        if not evaluations:
            logger.info("evaluation_skipped_no_answers", extra={"interview_id": str(interview.id)})
            return None

        return await self._generate_report(interview, evaluations, summaries)

    async def _generate_report(
        self, interview: Interview, evaluations: list[Evaluation], summaries: list[dict]
    ) -> Report:
        computed = {
            "overall": _avg([float(e.overall_score) for e in evaluations]),
            "technical": _avg(
                [float(e.technical_score) for e in evaluations if e.technical_score is not None]
            ),
            "communication": _avg(
                [
                    float(e.communication_score)
                    for e in evaluations
                    if e.communication_score is not None
                ]
            ),
            "problem_solving": _avg(
                [
                    float(e.problem_solving_score)
                    for e in evaluations
                    if e.problem_solving_score is not None
                ]
            ),
        }
        interview_summary = json.dumps(
            {
                "target_role": interview.target_role,
                "difficulty": interview.difficulty,
                "experience_level": interview.experience_level,
                "question_count": len(summaries),
                "computed_scores": computed,
            }
        )
        content, meta = await self.ai.generate_report(
            interview_summary=interview_summary, evaluations=json.dumps(summaries)
        )

        report = Report(
            interview_id=interview.id,
            overall_score=content.overall_score,
            technical_score=content.technical_score or computed["technical"],
            communication_score=content.communication_score or computed["communication"],
            problem_solving_score=content.problem_solving_score or computed["problem_solving"],
            executive_summary=content.executive_summary,
            strengths=content.strengths,
            weaknesses=content.weaknesses,
            improvement_roadmap=content.improvement_roadmap,
            hiring_recommendation=content.hiring_recommendation,
            report_model=meta.model,
            pdf_generated=False,
        )
        self.reports.add(report)
        interview.overall_score = content.overall_score
        await self.reports.flush()

        await self._render_pdf(report, interview)

        await self.audit.log(
            event_type=AuditEventType.REPORT,
            action="GENERATE_REPORT",
            user_id=interview.user_id,
            resource_type="report",
            resource_id=report.id,
        )
        logger.info("report_generated", extra={"interview_id": str(interview.id)})
        return report

    async def _render_pdf(self, report: Report, interview: Interview) -> None:
        """Render and store the report PDF (best-effort; failure is non-fatal)."""
        if self.storage is None:
            return
        try:
            pdf_bytes = build_report_pdf(report, interview)
            key = f"reports/{interview.id}/{report.id}.pdf"
            path = await self.storage.save(key=key, data=pdf_bytes, content_type="application/pdf")
            report.pdf_storage_path = path
            report.pdf_generated = True
            await self.reports.flush()
        except Exception:  # pragma: no cover - PDF is a convenience, never blocks
            logger.exception("report_pdf_generation_failed", extra={"report_id": str(report.id)})

    async def get_report_pdf(self, user, report_id: uuid.UUID) -> tuple[bytes, str]:
        """Return (pdf_bytes, filename) for a report the user owns."""
        report = await self.get_report(user, report_id)
        if not report.pdf_generated or not report.pdf_storage_path or self.storage is None:
            raise AppException(
                "PDF report is not yet available.",
                error_code=ErrorCode.PDF_NOT_READY,
                status_code=409,
            )
        key = report.pdf_storage_path.split("://", 1)[-1]
        if report.pdf_storage_path.startswith("s3://"):
            key = key.split("/", 1)[-1]
        data = await self.storage.load(key=key)
        return data, f"interview_report_{report_id}.pdf"

    # ------------------------------------------------------------------ #
    # Retrieval (ownership-checked)                                       #
    # ------------------------------------------------------------------ #
    async def _owned_interview(self, user, interview_id: uuid.UUID) -> Interview:
        interview = await self.interviews.get(interview_id)
        if interview is None or interview.user_id != user.id:
            raise InterviewNotFoundError()
        return interview

    async def get_evaluation(self, user, evaluation_id: uuid.UUID) -> Evaluation:
        evaluation = await self.evaluations.get(evaluation_id)
        if evaluation is None:
            raise EvaluationNotFoundError()
        interview_id = await self.evaluations.interview_id_for(evaluation)
        interview = await self.interviews.get(interview_id) if interview_id else None
        # Don't leak existence of another user's evaluation.
        if interview is None or interview.user_id != user.id:
            raise EvaluationNotFoundError()
        return evaluation

    async def get_interview_evaluation(self, user, interview_id: uuid.UUID) -> Report:
        await self._owned_interview(user, interview_id)
        report = await self.reports.get_by_interview(interview_id)
        if report is None:
            raise EvaluationNotFoundError("Evaluation is not available yet.")
        return report

    async def get_report(self, user, report_id: uuid.UUID) -> Report:
        report = await self.reports.get(report_id)
        if report is None:
            raise ReportNotFoundError()
        interview = await self.interviews.get(report.interview_id)
        # Don't leak existence of another user's report.
        if interview is None or interview.user_id != user.id:
            raise ReportNotFoundError()
        return report

    async def get_interview_report(self, user, interview_id: uuid.UUID) -> Report:
        await self._owned_interview(user, interview_id)
        report = await self.reports.get_by_interview(interview_id)
        if report is None:
            raise ReportNotFoundError()
        return report

    async def list_reports(self, user, *, page: int, page_size: int) -> tuple[list[Report], int]:
        return await self.reports.list_by_user(user.id, page=page, page_size=page_size)
