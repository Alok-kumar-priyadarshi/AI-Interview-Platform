"""Interview model — see ``docs/04-database/entities/interviews.md``.

The parent entity for a complete assessment session: questions, answers,
evaluations, and the final report all hang off an interview.
"""

from __future__ import annotations

import uuid
from datetime import datetime
from decimal import Decimal
from typing import TYPE_CHECKING

from sqlalchemy import (
    CheckConstraint,
    DateTime,
    ForeignKey,
    Index,
    Integer,
    Numeric,
    String,
    Uuid,
)
from sqlalchemy.orm import Mapped, mapped_column, relationship

from app.database.base import Base, TimestampMixin, UUIDPrimaryKeyMixin
from app.models._constraints import enum_check, range_check
from app.models.enums import Difficulty, ExperienceLevel, InterviewStatus, InterviewType

if TYPE_CHECKING:
    from app.models.interview_question import InterviewQuestion
    from app.models.report import Report
    from app.models.resume import Resume
    from app.models.user import User


class Interview(UUIDPrimaryKeyMixin, TimestampMixin, Base):
    __tablename__ = "interviews"
    __table_args__ = (
        enum_check("interview_type", InterviewType, name="interview_type"),
        enum_check("difficulty", Difficulty, name="difficulty"),
        enum_check("status", InterviewStatus, name="status"),
        enum_check("experience_level", ExperienceLevel, name="experience_level"),
        range_check("overall_score", "overall_score"),
        CheckConstraint("answered_questions <= total_questions", name="answer_count"),
        CheckConstraint("total_questions >= 0 AND answered_questions >= 0", name="question_counts"),
        CheckConstraint("expected_salary IS NULL OR expected_salary >= 0", name="expected_salary"),
        Index("idx_interviews_user", "user_id"),
        Index("idx_interviews_resume", "resume_id"),
        Index("idx_interviews_status", "status"),
        Index("idx_interviews_created_at", "created_at"),
        Index("idx_interviews_role", "target_role"),
        Index("idx_interviews_company", "target_company"),
        Index("idx_interviews_user_created", "user_id", "created_at"),
    )

    user_id: Mapped[uuid.UUID] = mapped_column(
        Uuid, ForeignKey("users.id", ondelete="CASCADE"), nullable=False
    )
    resume_id: Mapped[uuid.UUID] = mapped_column(
        Uuid, ForeignKey("resumes.id", ondelete="RESTRICT"), nullable=False
    )
    title: Mapped[str] = mapped_column(String(255), nullable=False)
    interview_type: Mapped[str] = mapped_column(
        String(20), nullable=False, default=InterviewType.TEXT
    )
    interviewer_voice: Mapped[str | None] = mapped_column(String(50), nullable=True)
    target_role: Mapped[str] = mapped_column(String(150), nullable=False)
    target_company: Mapped[str | None] = mapped_column(String(150), nullable=True)
    expected_salary: Mapped[int | None] = mapped_column(Integer, nullable=True)
    experience_level: Mapped[str] = mapped_column(
        String(30), nullable=False, default=ExperienceLevel.FRESHER
    )
    difficulty: Mapped[str] = mapped_column(String(20), nullable=False, default=Difficulty.MEDIUM)
    ai_model: Mapped[str] = mapped_column(String(50), nullable=False)
    total_questions: Mapped[int] = mapped_column(Integer, nullable=False, default=0)
    answered_questions: Mapped[int] = mapped_column(Integer, nullable=False, default=0)
    overall_score: Mapped[Decimal | None] = mapped_column(Numeric(5, 2), nullable=True)
    status: Mapped[str] = mapped_column(String(30), nullable=False, default=InterviewStatus.CREATED)
    started_at: Mapped[datetime | None] = mapped_column(DateTime(timezone=True), nullable=True)
    completed_at: Mapped[datetime | None] = mapped_column(DateTime(timezone=True), nullable=True)
    duration_seconds: Mapped[int | None] = mapped_column(Integer, nullable=True)

    # --- Relationships ------------------------------------------------------
    user: Mapped[User] = relationship(back_populates="interviews")
    resume: Mapped[Resume] = relationship(back_populates="interviews")
    questions: Mapped[list[InterviewQuestion]] = relationship(
        back_populates="interview",
        cascade="all, delete-orphan",
        order_by="InterviewQuestion.question_number",
    )
    report: Mapped[Report | None] = relationship(
        back_populates="interview", cascade="all, delete-orphan", uselist=False
    )

    def __repr__(self) -> str:  # pragma: no cover - debug helper
        return f"<Interview id={self.id} status={self.status!r} role={self.target_role!r}>"
