"""Interview question model — see ``docs/04-database/entities/interview_questions.md``.

Questions are immutable after generation; this table has a ``created_at`` but no
``updated_at`` (hence it does not use :class:`TimestampMixin`).
"""

from __future__ import annotations

import uuid
from datetime import datetime
from typing import TYPE_CHECKING, Any

from sqlalchemy import (
    CheckConstraint,
    DateTime,
    ForeignKey,
    Index,
    Integer,
    String,
    Text,
    UniqueConstraint,
    Uuid,
    func,
)
from sqlalchemy.orm import Mapped, mapped_column, relationship

from app.database.base import Base, UUIDPrimaryKeyMixin
from app.database.types import JSONB
from app.models._constraints import enum_check
from app.models.enums import Difficulty, QuestionCategory

if TYPE_CHECKING:
    from app.models.interview import Interview
    from app.models.interview_answer import InterviewAnswer


class InterviewQuestion(UUIDPrimaryKeyMixin, Base):
    __tablename__ = "interview_questions"
    __table_args__ = (
        UniqueConstraint("interview_id", "question_number", name="uq_questions_interview_order"),
        enum_check("category", QuestionCategory, name="category"),
        enum_check("difficulty", Difficulty, name="difficulty"),
        CheckConstraint("question_number > 0", name="question_number"),
        CheckConstraint(
            "estimated_time_seconds IS NULL OR estimated_time_seconds > 0", name="estimated_time"
        ),
        Index("idx_questions_interview", "interview_id"),
        Index("idx_questions_category", "category"),
        Index("idx_questions_difficulty", "difficulty"),
        Index("idx_questions_interview_order", "interview_id", "question_number"),
    )

    interview_id: Mapped[uuid.UUID] = mapped_column(
        Uuid, ForeignKey("interviews.id", ondelete="CASCADE"), nullable=False
    )
    question_number: Mapped[int] = mapped_column(Integer, nullable=False)
    category: Mapped[str] = mapped_column(String(40), nullable=False)
    difficulty: Mapped[str] = mapped_column(String(20), nullable=False, default=Difficulty.MEDIUM)
    question_text: Mapped[str] = mapped_column(Text, nullable=False)
    expected_answer_points: Mapped[Any] = mapped_column(JSONB, nullable=False, default=list)
    evaluation_rubric: Mapped[Any] = mapped_column(JSONB, nullable=False, default=dict)
    estimated_time_seconds: Mapped[int | None] = mapped_column(Integer, nullable=True)
    ai_model: Mapped[str] = mapped_column(String(50), nullable=False)
    generation_prompt_version: Mapped[str | None] = mapped_column(String(30), nullable=True)
    created_at: Mapped[datetime] = mapped_column(
        DateTime(timezone=True), nullable=False, server_default=func.now()
    )

    # --- Relationships ------------------------------------------------------
    interview: Mapped[Interview] = relationship(back_populates="questions")
    answer: Mapped[InterviewAnswer | None] = relationship(
        back_populates="question", cascade="all, delete-orphan", uselist=False
    )

    def __repr__(self) -> str:  # pragma: no cover - debug helper
        return f"<InterviewQuestion id={self.id} #{self.question_number} cat={self.category!r}>"
