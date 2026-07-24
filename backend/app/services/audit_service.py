"""Audit service — records security and business events (append-only).

Auditing is best-effort: a failure to write an audit record must never break the
underlying business operation, so writes are wrapped defensively. Sensitive
values (tokens, secrets) must never be passed in.
"""

from __future__ import annotations

import uuid
from typing import Any

from sqlalchemy.ext.asyncio import AsyncSession

from app.core.logging import get_logger
from app.models.audit_log import AuditLog
from app.models.enums import AuditEventType, AuditSeverity
from app.repositories.audit_repository import AuditRepository

logger = get_logger(__name__)


class AuditService:
    def __init__(self, session: AsyncSession) -> None:
        self.session = session
        self.audits = AuditRepository(session)

    async def log(
        self,
        *,
        event_type: AuditEventType,
        action: str,
        severity: AuditSeverity = AuditSeverity.INFO,
        user_id: uuid.UUID | None = None,
        resource_type: str | None = None,
        resource_id: uuid.UUID | None = None,
        description: str | None = None,
        ip_address: str | None = None,
        user_agent: str | None = None,
        metadata: dict[str, Any] | None = None,
    ) -> None:
        try:
            entry = AuditLog(
                user_id=user_id,
                event_type=event_type,
                severity=severity,
                resource_type=resource_type,
                resource_id=resource_id,
                action=action,
                description=description,
                ip_address=ip_address,
                user_agent=user_agent,
                event_metadata=metadata or {},
            )
            self.audits.add(entry)
            await self.audits.flush()
        except Exception:  # pragma: no cover - defensive; audit must not break flow
            logger.exception("audit_write_failed", extra={"action": action})
