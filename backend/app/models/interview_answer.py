"""Interview answer model — see ``docs/04-database/entities/interview_answers.md``.

One answer per question (Version 1). Voice answers store an audio reference and
a Whisper transcription; text answers store ``answer_text`` directly.
"""

from __future__ import annotations

import uuid
from datetime import datetime
from decimal import Decimal
from typing import TYPE_CHECKING

from sqlalchemy import (
    DateTime,
    ForeignKey,
    Index,
    Integer,
    Numeric,
    String,
    Text,
    Uuid,
    func,
)
from sqlalchemy.orm import Mapped, mapped_column, relationship

from app.database.base import Base, TimestampMixin, UUIDPrimaryKeyMixin
from app.models._constraints import enum_check, range_check
from app.models.enums import AnswerType, SubmissionStatus

if TYPE_CHECKING:
    from app.models.evaluation import Evaluation
    from app.models.interview_question import InterviewQuestion


class InterviewAnswer(UUIDPrimaryKeyMixin, TimestampMixin, Base):
    __tablename__ = "interview_answers"
    __table_args__ = (
        enum_check("answer_type", AnswerType, name="answer_type"),
        enum_check("submission_status", SubmissionStatus, name="submission_status"),
        range_check("transcription_confidence", "transcription_confidence"),
        range_check("response_time_seconds", "response_time", low=0, high=86_400),
        Index("idx_answers_question", "question_id"),
        Index("idx_answers_status", "submission_status"),
        Index("idx_answers_language", "language"),
        Index("idx_answers_submitted_at", "submitted_at"),
    )

    question_id: Mapped[uuid.UUID] = mapped_column(
        Uuid,
        ForeignKey("interview_questions.id", ondelete="CASCADE"),
        unique=True,
        nullable=False,
    )
    answer_type: Mapped[str] = mapped_column(String(20), nullable=False, default=AnswerType.TEXT)
    answer_text: Mapped[str | None] = mapped_column(Text, nullable=True)
    audio_storage_path: Mapped[str | None] = mapped_column(Text, nullable=True)
    transcription_text: Mapped[str | None] = mapped_column(Text, nullable=True)
    transcription_confidence: Mapped[Decimal | None] = mapped_column(Numeric(5, 2), nullable=True)
    language: Mapped[str] = mapped_column(String(20), nullable=False, default="en")
    response_time_seconds: Mapped[int | None] = mapped_column(Integer, nullable=True)
    submission_status: Mapped[str] = mapped_column(
        String(30), nullable=False, default=SubmissionStatus.SUBMITTED
    )
    submitted_at: Mapped[datetime] = mapped_column(
        DateTime(timezone=True), nullable=False, server_default=func.now()
    )

    # --- Relationships ------------------------------------------------------
    question: Mapped[InterviewQuestion] = relationship(back_populates="answer")
    evaluation: Mapped[Evaluation | None] = relationship(
        back_populates="answer", cascade="all, delete-orphan", uselist=False
    )

    def __repr__(self) -> str:  # pragma: no cover - debug helper
        return f"<InterviewAnswer id={self.id} question_id={self.question_id}>"
