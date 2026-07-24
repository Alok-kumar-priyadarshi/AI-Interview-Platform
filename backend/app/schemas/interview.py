"""Interview, question, and answer schemas.

See docs/05-api-design/{interviews,questions,answers}.md.
"""

from __future__ import annotations

import uuid
from datetime import datetime
from typing import Any

from pydantic import BaseModel, Field

from app.models.enums import (
    Difficulty,
    InterviewType,
    InterviewVoice,
    PreferredInterviewType,
    PreferredLanguage,
)


class InterviewCreate(BaseModel):
    resume_id: uuid.UUID
    # Category of questions to generate (technical/behavioral/mixed).
    interview_type: PreferredInterviewType = PreferredInterviewType.TECHNICAL
    difficulty: Difficulty = Difficulty.MEDIUM
    # Interaction mode → persisted as interviews.interview_type (text/voice).
    mode: InterviewType = InterviewType.TEXT
    language: PreferredLanguage = PreferredLanguage.EN
    interviewer_voice: InterviewVoice | None = None
    question_count: int = Field(default=10, ge=5, le=50)
    time_limit_minutes: int | None = Field(default=None, ge=10, le=180)


class InterviewCreateResult(BaseModel):
    interview_id: uuid.UUID
    status: str


class InterviewSummary(BaseModel):
    id: uuid.UUID
    title: str
    status: str
    difficulty: str
    mode: str
    target_role: str
    total_questions: int
    answered_questions: int
    overall_score: float | None
    created_at: datetime

    @classmethod
    def from_model(cls, interview: Any) -> InterviewSummary:
        return cls(
            id=interview.id,
            title=interview.title,
            status=interview.status,
            difficulty=interview.difficulty,
            mode=interview.interview_type,
            target_role=interview.target_role,
            total_questions=interview.total_questions,
            answered_questions=interview.answered_questions,
            overall_score=float(interview.overall_score)
            if interview.overall_score is not None
            else None,
            created_at=interview.created_at,
        )


class InterviewDetail(InterviewSummary):
    target_company: str | None
    experience_level: str
    interviewer_voice: str | None
    started_at: datetime | None
    completed_at: datetime | None
    duration_seconds: int | None

    @classmethod
    def from_model(cls, interview: Any) -> InterviewDetail:
        return cls(
            **InterviewSummary.from_model(interview).model_dump(),
            target_company=interview.target_company,
            experience_level=interview.experience_level,
            interviewer_voice=interview.interviewer_voice,
            started_at=interview.started_at,
            completed_at=interview.completed_at,
            duration_seconds=interview.duration_seconds,
        )


class InterviewStatusResponse(BaseModel):
    status: str
    current_question: int | None
    completed_questions: int
    remaining_questions: int
    elapsed_seconds: int | None


# --------------------------------------------------------------------------- #
# Questions                                                                   #
# --------------------------------------------------------------------------- #


class CurrentQuestion(BaseModel):
    question_id: uuid.UUID
    sequence: int
    category: str
    difficulty: str
    question: str
    estimated_time_seconds: int | None


class QuestionDetail(BaseModel):
    id: uuid.UUID
    sequence: int
    category: str
    difficulty: str
    estimated_time_seconds: int | None


class QuestionListItem(BaseModel):
    id: uuid.UUID
    sequence: int
    category: str
    difficulty: str
    question: str


# --------------------------------------------------------------------------- #
# Answers                                                                     #
# --------------------------------------------------------------------------- #


class AnswerSubmit(BaseModel):
    question_id: uuid.UUID
    answer: str = Field(..., min_length=1, max_length=20_000)


class AnswerResult(BaseModel):
    answer_id: uuid.UUID
    submitted_at: datetime


class AnswerDetail(BaseModel):
    answer_id: uuid.UUID
    question_id: uuid.UUID
    type: str
    submitted_at: datetime
    response_time_seconds: int | None


class TranscriptResponse(BaseModel):
    transcript: str
    confidence: float | None
    language: str
