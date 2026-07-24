"""Audit log repository — append-only writes for :class:`~app.models.audit_log.AuditLog`."""

from __future__ import annotations

from app.models.audit_log import AuditLog
from app.repositories.base import BaseRepository


class AuditRepository(BaseRepository[AuditLog]):
    model = AuditLog

    # Audit records are append-only (docs/04-database/entities/audit_logs.md):
    # no update or delete methods are exposed here by design.
