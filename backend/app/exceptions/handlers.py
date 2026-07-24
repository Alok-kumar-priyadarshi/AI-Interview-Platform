"""Centralised exception handlers.

Registers handlers that convert every raised exception into the standard error
envelope (``docs/05-api-design/errors.md``). Three tiers are covered:

1. :class:`~app.exceptions.base.AppException` — expected domain errors.
2. FastAPI ``RequestValidationError`` — request schema validation (HTTP 422).
3. Any uncaught :class:`Exception` — logged with a stack trace and returned as
   an opaque ``INTERNAL_SERVER_ERROR`` (implementation details never leak).
"""

from __future__ import annotations

from fastapi import FastAPI, Request, status
from fastapi.exceptions import RequestValidationError
from fastapi.responses import JSONResponse
from starlette.exceptions import HTTPException as StarletteHTTPException

from app.core.context import get_request_id
from app.core.error_codes import ErrorCode
from app.core.logging import get_logger
from app.exceptions.base import AppException
from app.schemas.common import ErrorBody, ErrorDetail, ErrorResponse

logger = get_logger(__name__)


def _render(status_code: int, code: str, message: str, details=None) -> JSONResponse:
    payload = ErrorResponse(
        error=ErrorBody(code=code, message=message, details=details),
        request_id=get_request_id(),
    )
    return JSONResponse(status_code=status_code, content=payload.model_dump(exclude_none=True))


async def _handle_app_exception(_: Request, exc: AppException) -> JSONResponse:
    details = None
    if exc.details:
        details = [ErrorDetail(**d) for d in exc.details]
    # 5xx domain errors are worth a warning; 4xx are expected client errors.
    log = logger.error if exc.status_code >= 500 else logger.info
    log("app_exception", extra={"error_code": exc.error_code, "status": exc.status_code})
    return _render(exc.status_code, exc.error_code, exc.message, details)


async def _handle_validation_error(_: Request, exc: RequestValidationError) -> JSONResponse:
    details = [
        ErrorDetail(
            field=".".join(str(loc) for loc in err["loc"] if loc != "body"),
            message=err["msg"],
        )
        for err in exc.errors()
    ]
    return _render(
        status.HTTP_422_UNPROCESSABLE_ENTITY,
        ErrorCode.VALIDATION_ERROR,
        "One or more validation errors occurred.",
        details,
    )


async def _handle_http_exception(_: Request, exc: StarletteHTTPException) -> JSONResponse:
    # Map bare Starlette/FastAPI HTTPExceptions (e.g. 404 on unknown routes)
    # onto the standard envelope so clients only ever see one error shape.
    code = {
        status.HTTP_401_UNAUTHORIZED: ErrorCode.UNAUTHORIZED,
        status.HTTP_403_FORBIDDEN: ErrorCode.FORBIDDEN,
        status.HTTP_404_NOT_FOUND: ErrorCode.INTERNAL_SERVER_ERROR,
        status.HTTP_429_TOO_MANY_REQUESTS: ErrorCode.RATE_LIMIT_EXCEEDED,
    }.get(exc.status_code, ErrorCode.INTERNAL_SERVER_ERROR)
    message = exc.detail if isinstance(exc.detail, str) else "Request failed."
    return _render(exc.status_code, code, message)


async def _handle_unexpected(_: Request, exc: Exception) -> JSONResponse:
    logger.exception("unhandled_exception", extra={"exc_type": type(exc).__name__})
    return _render(
        status.HTTP_500_INTERNAL_SERVER_ERROR,
        ErrorCode.INTERNAL_SERVER_ERROR,
        "An unexpected error occurred.",
    )


def register_exception_handlers(app: FastAPI) -> None:
    """Attach all exception handlers to the application."""
    app.add_exception_handler(AppException, _handle_app_exception)  # type: ignore[arg-type]
    app.add_exception_handler(RequestValidationError, _handle_validation_error)  # type: ignore[arg-type]
    app.add_exception_handler(StarletteHTTPException, _handle_http_exception)  # type: ignore[arg-type]
    app.add_exception_handler(Exception, _handle_unexpected)
