"""Evaluation model — see ``docs/04-database/entities/evaluations.md``.

One AI-generated assessment per submitted answer.
"""

from __future__ import annotations

import uuid
from decimal import Decimal
from typing import TYPE_CHECKING, Any

from sqlalchemy import CheckConstraint, ForeignKey, Index, Integer, Numeric, String, Text, Uuid
from sqlalchemy.orm import Mapped, mapped_column, relationship

from app.database.base import Base, TimestampMixin, UUIDPrimaryKeyMixin
from app.database.types import JSONB
from app.models._constraints import range_check

if TYPE_CHECKING:
    from app.models.interview_answer import InterviewAnswer


class Evaluation(UUIDPrimaryKeyMixin, TimestampMixin, Base):
    __tablename__ = "evaluations"
    __table_args__ = (
        range_check("overall_score", "overall_score"),
        range_check("technical_score", "technical_score"),
        range_check("communication_score", "communication_score"),
        range_check("problem_solving_score", "problem_solving_score"),
        range_check("confidence_score", "confidence_score"),
        CheckConstraint(
            "evaluation_duration_ms IS NULL OR evaluation_duration_ms >= 0", name="duration"
        ),
        Index("idx_evaluations_answer", "answer_id"),
        Index("idx_evaluations_created_at", "created_at"),
        Index("idx_evaluations_model", "evaluation_model"),
    )

    answer_id: Mapped[uuid.UUID] = mapped_column(
        Uuid,
        ForeignKey("interview_answers.id", ondelete="CASCADE"),
        unique=True,
        nullable=False,
    )
    overall_score: Mapped[Decimal] = mapped_column(Numeric(5, 2), nullable=False)
    technical_score: Mapped[Decimal | None] = mapped_column(Numeric(5, 2), nullable=True)
    communication_score: Mapped[Decimal | None] = mapped_column(Numeric(5, 2), nullable=True)
    problem_solving_score: Mapped[Decimal | None] = mapped_column(Numeric(5, 2), nullable=True)
    confidence_score: Mapped[Decimal | None] = mapped_column(Numeric(5, 2), nullable=True)
    strengths: Mapped[Any] = mapped_column(JSONB, nullable=False, default=list)
    weaknesses: Mapped[Any] = mapped_column(JSONB, nullable=False, default=list)
    improvement_suggestions: Mapped[Any] = mapped_column(JSONB, nullable=False, default=list)
    detailed_feedback: Mapped[str | None] = mapped_column(Text, nullable=True)
    evaluation_model: Mapped[str] = mapped_column(String(50), nullable=False)
    evaluation_prompt_version: Mapped[str | None] = mapped_column(String(30), nullable=True)
    evaluation_duration_ms: Mapped[int | None] = mapped_column(Integer, nullable=True)

    # --- Relationships ------------------------------------------------------
    answer: Mapped[InterviewAnswer] = relationship(back_populates="evaluation")

    def __repr__(self) -> str:  # pragma: no cover - debug helper
        return f"<Evaluation id={self.id} answer_id={self.answer_id} score={self.overall_score}>"
