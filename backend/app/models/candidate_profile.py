"""Candidate profile model — see ``docs/04-database/entities/candidate_profiles.md``.

The structured, AI-extracted representation of a resume; the primary knowledge
source for interview question generation.
"""

from __future__ import annotations

import uuid
from decimal import Decimal
from typing import TYPE_CHECKING, Any

from sqlalchemy import CheckConstraint, ForeignKey, Index, Integer, Numeric, String, Text, Uuid
from sqlalchemy.orm import Mapped, mapped_column, relationship

from app.database.base import Base, TimestampMixin, UUIDPrimaryKeyMixin
from app.database.types import JSONB
from app.models._constraints import enum_check, range_check
from app.models.enums import ExtractionStatus

if TYPE_CHECKING:
    from app.models.resume import Resume


class CandidateProfile(UUIDPrimaryKeyMixin, TimestampMixin, Base):
    __tablename__ = "candidate_profiles"
    __table_args__ = (
        enum_check("extraction_status", ExtractionStatus, name="extraction_status"),
        CheckConstraint("profile_version >= 1", name="profile_version"),
        range_check("ai_confidence_score", "confidence_score"),
        Index("idx_candidate_profiles_resume", "resume_id"),
        Index("idx_candidate_profiles_version", "profile_version"),
        Index("idx_candidate_profiles_status", "extraction_status"),
        # GIN on PostgreSQL for JSONB search; a plain index elsewhere (SQLite).
        Index("idx_candidate_profiles_skills", "skills", postgresql_using="gin"),
        Index("idx_candidate_profiles_projects", "projects", postgresql_using="gin"),
    )

    resume_id: Mapped[uuid.UUID] = mapped_column(
        Uuid, ForeignKey("resumes.id", ondelete="CASCADE"), unique=True, nullable=False
    )
    profile_version: Mapped[int] = mapped_column(Integer, nullable=False, default=1)
    professional_summary: Mapped[str | None] = mapped_column(Text, nullable=True)
    total_experience_years: Mapped[Decimal | None] = mapped_column(Numeric(4, 1), nullable=True)
    highest_education: Mapped[str | None] = mapped_column(String(255), nullable=True)
    current_job_title: Mapped[str | None] = mapped_column(String(255), nullable=True)
    current_company: Mapped[str | None] = mapped_column(String(255), nullable=True)

    skills: Mapped[Any] = mapped_column(JSONB, nullable=False, default=list)
    education: Mapped[Any] = mapped_column(JSONB, nullable=False, default=list)
    experience: Mapped[Any] = mapped_column(JSONB, nullable=False, default=list)
    projects: Mapped[Any] = mapped_column(JSONB, nullable=False, default=list)
    certifications: Mapped[Any] = mapped_column(JSONB, nullable=False, default=list)
    languages: Mapped[Any] = mapped_column(JSONB, nullable=False, default=list)

    ai_confidence_score: Mapped[Decimal | None] = mapped_column(Numeric(5, 2), nullable=True)
    ai_model_version: Mapped[str | None] = mapped_column(String(50), nullable=True)
    extraction_status: Mapped[str] = mapped_column(
        String(30), nullable=False, default=ExtractionStatus.COMPLETED
    )

    # --- Relationships ------------------------------------------------------
    resume: Mapped[Resume] = relationship(back_populates="candidate_profile")

    def __repr__(self) -> str:  # pragma: no cover - debug helper
        return f"<CandidateProfile id={self.id} resume_id={self.resume_id} v{self.profile_version}>"
