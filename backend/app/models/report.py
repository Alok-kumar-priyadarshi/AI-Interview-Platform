"""Report model — see ``docs/04-database/entities/reports.md``.

One aggregated report per interview, derived from all answer evaluations.
"""

from __future__ import annotations

import uuid
from datetime import datetime
from decimal import Decimal
from typing import TYPE_CHECKING, Any

from sqlalchemy import (
    Boolean,
    CheckConstraint,
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
from app.database.types import JSONB
from app.models._constraints import enum_check, range_check
from app.models.enums import HiringRecommendation

if TYPE_CHECKING:
    from app.models.interview import Interview


class Report(UUIDPrimaryKeyMixin, TimestampMixin, Base):
    __tablename__ = "reports"
    __table_args__ = (
        enum_check("hiring_recommendation", HiringRecommendation, name="hiring_recommendation"),
        range_check("overall_score", "overall_score"),
        range_check("technical_score", "technical_score"),
        range_check("communication_score", "communication_score"),
        range_check("problem_solving_score", "problem_solving_score"),
        CheckConstraint("report_version >= 1", name="report_version"),
        Index("idx_reports_interview", "interview_id"),
        Index("idx_reports_score", "overall_score"),
        Index("idx_reports_generated_at", "generated_at"),
        Index("idx_reports_recommendation", "hiring_recommendation"),
    )

    interview_id: Mapped[uuid.UUID] = mapped_column(
        Uuid,
        ForeignKey("interviews.id", ondelete="CASCADE"),
        unique=True,
        nullable=False,
    )
    overall_score: Mapped[Decimal] = mapped_column(Numeric(5, 2), nullable=False)
    technical_score: Mapped[Decimal | None] = mapped_column(Numeric(5, 2), nullable=True)
    communication_score: Mapped[Decimal | None] = mapped_column(Numeric(5, 2), nullable=True)
    problem_solving_score: Mapped[Decimal | None] = mapped_column(Numeric(5, 2), nullable=True)
    executive_summary: Mapped[str] = mapped_column(Text, nullable=False)
    strengths: Mapped[Any] = mapped_column(JSONB, nullable=False, default=list)
    weaknesses: Mapped[Any] = mapped_column(JSONB, nullable=False, default=list)
    improvement_roadmap: Mapped[Any] = mapped_column(JSONB, nullable=False, default=list)
    hiring_recommendation: Mapped[str] = mapped_column(String(30), nullable=False)
    report_version: Mapped[int] = mapped_column(Integer, nullable=False, default=1)
    report_model: Mapped[str] = mapped_column(String(50), nullable=False)
    pdf_generated: Mapped[bool] = mapped_column(Boolean, nullable=False, default=False)
    pdf_storage_path: Mapped[str | None] = mapped_column(Text, nullable=True)
    generated_at: Mapped[datetime] = mapped_column(
        DateTime(timezone=True), nullable=False, server_default=func.now()
    )

    # --- Relationships ------------------------------------------------------
    interview: Mapped[Interview] = relationship(back_populates="report")

    def __repr__(self) -> str:  # pragma: no cover - debug helper
        return f"<Report id={self.id} interview_id={self.interview_id} score={self.overall_score}>"
