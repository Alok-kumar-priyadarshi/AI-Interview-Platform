"""Candidate preferences model.

Backs the ``/candidate-profile`` API (docs/05-api-design/candidate-profile.md):
a **user-owned, manually-maintained** set of interview preferences and career
targets. This is intentionally distinct from
:class:`~app.models.candidate_profile.CandidateProfile`, which is the
*resume-derived, AI-extracted* profile (one per resume).

Introduced in migration 0003 as a documented schema addition (the entity was
defined by the API contract but not the original DB schema).
"""

from __future__ import annotations

import uuid
from typing import TYPE_CHECKING, Any

from sqlalchemy import CheckConstraint, ForeignKey, Integer, String, Uuid
from sqlalchemy.orm import Mapped, mapped_column, relationship

from app.database.base import Base, TimestampMixin, UUIDPrimaryKeyMixin
from app.database.types import JSONB
from app.models._constraints import enum_check
from app.models.enums import InterviewVoice, PreferredInterviewType, PreferredLanguage

if TYPE_CHECKING:
    from app.models.user import User


class CandidatePreferences(UUIDPrimaryKeyMixin, TimestampMixin, Base):
    __tablename__ = "candidate_preferences"
    __table_args__ = (
        enum_check("preferred_interview_type", PreferredInterviewType, name="interview_type"),
        enum_check("preferred_interview_language", PreferredLanguage, name="language"),
        # A NULL voice satisfies a CHECK ... IN (...) (unknown → not violated).
        enum_check("preferred_interviewer_voice", InterviewVoice, name="voice"),
        CheckConstraint(
            "experience_years IS NULL OR (experience_years >= 0 AND experience_years <= 50)",
            name="experience_years",
        ),
        CheckConstraint(
            "graduation_year IS NULL OR (graduation_year >= 1900 AND graduation_year <= 2100)",
            name="graduation_year",
        ),
        CheckConstraint(
            "expected_salary_min IS NULL OR expected_salary_min >= 0", name="salary_min"
        ),
        CheckConstraint(
            "expected_salary_max IS NULL OR expected_salary_min IS NULL "
            "OR expected_salary_max >= expected_salary_min",
            name="salary_range",
        ),
    )

    user_id: Mapped[uuid.UUID] = mapped_column(
        Uuid, ForeignKey("users.id", ondelete="CASCADE"), unique=True, nullable=False
    )
    target_role: Mapped[str] = mapped_column(String(150), nullable=False)
    experience_years: Mapped[int | None] = mapped_column(Integer, nullable=True)
    current_company: Mapped[str | None] = mapped_column(String(255), nullable=True)
    education: Mapped[str | None] = mapped_column(String(255), nullable=True)
    degree: Mapped[str | None] = mapped_column(String(255), nullable=True)
    university: Mapped[str | None] = mapped_column(String(255), nullable=True)
    graduation_year: Mapped[int | None] = mapped_column(Integer, nullable=True)
    skills: Mapped[Any] = mapped_column(JSONB, nullable=False, default=list)
    preferred_domains: Mapped[Any] = mapped_column(JSONB, nullable=False, default=list)
    expected_salary_min: Mapped[int | None] = mapped_column(Integer, nullable=True)
    expected_salary_max: Mapped[int | None] = mapped_column(Integer, nullable=True)
    preferred_interview_language: Mapped[str] = mapped_column(
        String(10), nullable=False, default=PreferredLanguage.EN
    )
    preferred_interviewer_voice: Mapped[str | None] = mapped_column(String(20), nullable=True)
    preferred_interview_type: Mapped[str] = mapped_column(
        String(20), nullable=False, default=PreferredInterviewType.TECHNICAL
    )

    # --- Relationships ------------------------------------------------------
    user: Mapped[User] = relationship(back_populates="preferences")

    def __repr__(self) -> str:  # pragma: no cover - debug helper
        return f"<CandidatePreferences user_id={self.user_id} role={self.target_role!r}>"
