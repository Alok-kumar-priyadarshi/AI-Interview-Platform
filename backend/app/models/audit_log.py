"""Audit log model — see ``docs/04-database/entities/audit_logs.md``.

Append-only record of security, authentication, and business events. Has
``occurred_at`` / ``created_at`` but no ``updated_at`` (records are immutable),
so it does not use :class:`TimestampMixin`.
"""

from __future__ import annotations

import uuid
from datetime import datetime
from typing import TYPE_CHECKING, Any

from sqlalchemy import DateTime, ForeignKey, Index, String, Text, Uuid, func
from sqlalchemy.orm import Mapped, mapped_column, relationship

from app.database.base import Base, UUIDPrimaryKeyMixin
from app.database.types import INET, JSONB
from app.models._constraints import enum_check
from app.models.enums import AuditEventType, AuditSeverity

if TYPE_CHECKING:
    from app.models.user import User


class AuditLog(UUIDPrimaryKeyMixin, Base):
    __tablename__ = "audit_logs"
    __table_args__ = (
        enum_check("event_type", AuditEventType, name="event_type"),
        enum_check("severity", AuditSeverity, name="severity"),
        Index("idx_audit_user", "user_id"),
        Index("idx_audit_event_type", "event_type"),
        Index("idx_audit_resource", "resource_type", "resource_id"),
        Index("idx_audit_occurred_at", "occurred_at"),
        Index("idx_audit_request", "request_id"),
        Index("idx_audit_severity", "severity"),
        Index("idx_audit_user_occurred", "user_id", "occurred_at"),
        Index("idx_audit_event_occurred", "event_type", "occurred_at"),
    )

    # System-generated events may have a NULL user; keep logs if a user is removed.
    user_id: Mapped[uuid.UUID | None] = mapped_column(
        Uuid, ForeignKey("users.id", ondelete="SET NULL"), nullable=True
    )
    event_type: Mapped[str] = mapped_column(String(50), nullable=False)
    severity: Mapped[str] = mapped_column(String(20), nullable=False, default=AuditSeverity.INFO)
    resource_type: Mapped[str | None] = mapped_column(String(50), nullable=True)
    resource_id: Mapped[uuid.UUID | None] = mapped_column(Uuid, nullable=True)
    action: Mapped[str] = mapped_column(String(100), nullable=False)
    description: Mapped[str | None] = mapped_column(Text, nullable=True)
    request_id: Mapped[uuid.UUID | None] = mapped_column(Uuid, nullable=True)
    ip_address: Mapped[str | None] = mapped_column(INET, nullable=True)
    user_agent: Mapped[str | None] = mapped_column(Text, nullable=True)
    # "metadata" is reserved by SQLAlchemy's declarative Base; map to a safe attr.
    event_metadata: Mapped[Any] = mapped_column("metadata", JSONB, nullable=False, default=dict)
    occurred_at: Mapped[datetime] = mapped_column(
        DateTime(timezone=True), nullable=False, server_default=func.now()
    )
    created_at: Mapped[datetime] = mapped_column(
        DateTime(timezone=True), nullable=False, server_default=func.now()
    )

    # --- Relationships ------------------------------------------------------
    user: Mapped[User | None] = relationship(back_populates="audit_logs")

    def __repr__(self) -> str:  # pragma: no cover - debug helper
        return f"<AuditLog id={self.id} event={self.event_type!r} action={self.action!r}>"
