"""Request context & access-logging middleware.

Assigns a correlation ID to every request, binds it (and, once authenticated,
the user ID) to the logging context, measures processing time, and emits a
structured access log line. The correlation ID is echoed back in the
``X-Request-ID`` response header so clients and support can trace requests.
"""

from __future__ import annotations

import time
import uuid

from starlette.middleware.base import BaseHTTPMiddleware, RequestResponseEndpoint
from starlette.requests import Request
from starlette.responses import Response

from app.core.context import request_id_ctx, user_id_ctx
from app.core.logging import get_logger

logger = get_logger("app.access")

REQUEST_ID_HEADER = "X-Request-ID"


def _new_request_id() -> str:
    return f"req_{uuid.uuid4().hex[:16]}"


class RequestContextMiddleware(BaseHTTPMiddleware):
    def __init__(self, app, *, log_requests: bool = True) -> None:  # type: ignore[no-untyped-def]
        super().__init__(app)
        self._log_requests = log_requests

    async def dispatch(self, request: Request, call_next: RequestResponseEndpoint) -> Response:
        request_id = request.headers.get(REQUEST_ID_HEADER) or _new_request_id()
        request_token = request_id_ctx.set(request_id)
        user_token = user_id_ctx.set(None)
        request.state.request_id = request_id

        start = time.perf_counter()
        try:
            response = await call_next(request)
        except Exception:
            duration_ms = (time.perf_counter() - start) * 1000
            logger.exception(
                "request_failed",
                extra={
                    "method": request.method,
                    "path": request.url.path,
                    "duration_ms": round(duration_ms, 2),
                },
            )
            raise
        else:
            duration_ms = (time.perf_counter() - start) * 1000
            response.headers[REQUEST_ID_HEADER] = request_id
            if self._log_requests:
                logger.info(
                    "request_completed",
                    extra={
                        "method": request.method,
                        "path": request.url.path,
                        "status_code": response.status_code,
                        "duration_ms": round(duration_ms, 2),
                    },
                )
            return response
        finally:
            request_id_ctx.reset(request_token)
            user_id_ctx.reset(user_token)
