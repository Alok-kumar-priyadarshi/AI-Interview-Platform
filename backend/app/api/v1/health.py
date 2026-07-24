"""Health & monitoring endpoints.

Implements the public probes from ``docs/05-api-design/health.md``:

* ``GET /health``         — overall health summary
* ``GET /health/live``    — liveness (never touches external dependencies)
* ``GET /health/ready``   — readiness (verifies critical dependencies)
* ``GET /health/version`` — deployed version metadata

The admin-only ``/health/dependencies`` and ``/health/metrics`` endpoints are
introduced alongside the admin authorization layer.
"""

from __future__ import annotations

import time
from datetime import UTC, datetime
from typing import Any

from fastapi import APIRouter, Depends, Response, status
from sqlalchemy import text
from sqlalchemy.ext.asyncio import AsyncSession

from app.core.config import Settings, get_settings
from app.core.logging import get_logger
from app.database.session import get_db
from app.schemas.common import SuccessResponse

logger = get_logger(__name__)

router = APIRouter(prefix="/health", tags=["Health"])

# Captured at import time; close enough to process start for uptime reporting.
_STARTED_AT = datetime.now(UTC)
_MONOTONIC_START = time.monotonic()


def _uptime_seconds() -> int:
    return int(time.monotonic() - _MONOTONIC_START)


@router.get("", summary="Overall application health")
async def health(settings: Settings = Depends(get_settings)) -> SuccessResponse[dict[str, Any]]:
    return SuccessResponse(
        message="Service is healthy.",
        data={
            "status": "healthy",
            "timestamp": datetime.now(UTC).isoformat(),
            "version": settings.APP_VERSION,
            "uptime_seconds": _uptime_seconds(),
        },
    )


@router.get("/live", summary="Liveness probe")
async def liveness() -> dict[str, str]:
    # Must never depend on external services (health.md — Business Rules).
    return {"status": "alive"}


@router.get("/ready", summary="Readiness probe")
async def readiness(
    response: Response,
    db: AsyncSession = Depends(get_db),
) -> dict[str, str]:
    """Return ``ready`` only when critical dependencies are reachable.

    Version 1 gates readiness on database connectivity; additional dependency
    checks (AI provider, storage) are layered in as those services come online.
    """
    try:
        await db.execute(text("SELECT 1"))
    except Exception:
        logger.exception("readiness_check_failed")
        response.status_code = status.HTTP_503_SERVICE_UNAVAILABLE
        return {"status": "not_ready"}
    return {"status": "ready"}


@router.get("/version", summary="Deployed application version")
async def version(settings: Settings = Depends(get_settings)) -> SuccessResponse[dict[str, Any]]:
    return SuccessResponse(
        message="OK",
        data={
            "application": settings.APP_NAME,
            "version": settings.APP_VERSION,
            "environment": settings.APP_ENV,
        },
    )
