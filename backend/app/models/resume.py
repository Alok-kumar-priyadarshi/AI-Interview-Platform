"""Resume model — see ``docs/04-database/entities/resumes.md``.

Stores resume **metadata** only; the file itself lives in object storage and the
parsed content lives in :class:`~app.models.candidate_profile.CandidateProfile`.
"""

from __future__ import annotations

import uuid
from datetime import datetime
from typing import TYPE_CHECKING

from sqlalchemy import (
    BigInteger,
    Boolean,
    CheckConstraint,
    DateTime,
    ForeignKey,
    Index,
    String,
    Text,
    Uuid,
)
from sqlalchemy.orm import Mapped, mapped_column, relationship

from app.database.base import Base, TimestampMixin, UUIDPrimaryKeyMixin
from app.models._constraints import enum_check
from app.models.enums import ProcessingStatus, UploadStatus

if TYPE_CHECKING:
    from app.models.candidate_profile import CandidateProfile
    from app.models.interview import Interview
    from app.models.user import User


class Resume(UUIDPrimaryKeyMixin, TimestampMixin, Base):
    __tablename__ = "resumes"
    __table_args__ = (
        enum_check("upload_status", UploadStatus, name="upload_status"),
        enum_check("processing_status", ProcessingStatus, name="processing_status"),
        CheckConstraint("file_size_bytes > 0", name="file_size"),
        Index("idx_resumes_user_id", "user_id"),
        Index("idx_resumes_processing_status", "processing_status"),
        Index("idx_resumes_created_at", "created_at"),
        Index("idx_resumes_checksum", "checksum_sha256"),
    )

    user_id: Mapped[uuid.UUID] = mapped_column(
        Uuid, ForeignKey("users.id", ondelete="CASCADE"), nullable=False
    )
    original_filename: Mapped[str] = mapped_column(String(255), nullable=False)
    stored_filename: Mapped[str] = mapped_column(String(255), nullable=False)
    storage_path: Mapped[str] = mapped_column(Text, nullable=False)
    mime_type: Mapped[str] = mapped_column(String(100), nullable=False)
    file_size_bytes: Mapped[int] = mapped_column(BigInteger, nullable=False)
    checksum_sha256: Mapped[str] = mapped_column(String(64), unique=True, nullable=False)
    # Added in migration 0002 to support the resume "set default" endpoint
    # (docs/05-api-design/resume.md). Only one default per user, enforced in
    # the service layer.
    is_default: Mapped[bool] = mapped_column(Boolean, nullable=False, default=False)
    upload_status: Mapped[str] = mapped_column(
        String(30), nullable=False, default=UploadStatus.UPLOADED
    )
    processing_status: Mapped[str] = mapped_column(
        String(30), nullable=False, default=ProcessingStatus.PENDING
    )
    ai_model_version: Mapped[str | None] = mapped_column(String(50), nullable=True)
    processing_started_at: Mapped[datetime | None] = mapped_column(
        DateTime(timezone=True), nullable=True
    )
    processing_completed_at: Mapped[datetime | None] = mapped_column(
        DateTime(timezone=True), nullable=True
    )

    # --- Relationships ------------------------------------------------------
    user: Mapped[User] = relationship(back_populates="resumes")
    candidate_profile: Mapped[CandidateProfile | None] = relationship(
        back_populates="resume", cascade="all, delete-orphan", uselist=False
    )
    interviews: Mapped[list[Interview]] = relationship(back_populates="resume")

    def __repr__(self) -> str:  # pragma: no cover - debug helper
        return f"<Resume id={self.id} user_id={self.user_id} status={self.processing_status!r}>"
