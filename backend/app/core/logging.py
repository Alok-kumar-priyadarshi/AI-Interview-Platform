"""Structured logging configuration.

Provides JSON logging in deployed environments (machine-parseable, correlated
by ``request_id``) and human-readable console logging for local development.

Every log record is automatically enriched with the current ``request_id`` and
``user_id`` (when available) via :class:`ContextFilter`, so business code can
simply call ``logger.info(...)`` without manually passing correlation data.

Sensitive values (tokens, secrets, passwords) must never be passed to the
logger — see ``docs/02-tech-stack/coding-standards.md`` (Logging).
"""

from __future__ import annotations

import logging
import sys

from pythonjsonlogger import jsonlogger

from app.core.config import get_settings
from app.core.context import get_request_id, get_user_id


class ContextFilter(logging.Filter):
    """Inject request-scoped correlation identifiers into every record."""

    def filter(self, record: logging.LogRecord) -> bool:
        record.request_id = get_request_id()
        record.user_id = get_user_id()
        return True


_CONSOLE_FORMAT = "%(asctime)s | %(levelname)-8s | %(name)s | req=%(request_id)s | %(message)s"


def _build_handler(log_format: str) -> logging.Handler:
    handler = logging.StreamHandler(sys.stdout)
    handler.addFilter(ContextFilter())

    if log_format == "json":
        formatter: logging.Formatter = jsonlogger.JsonFormatter(
            "%(asctime)s %(levelname)s %(name)s %(message)s %(request_id)s %(user_id)s",
            rename_fields={"asctime": "timestamp", "levelname": "level"},
        )
    else:
        formatter = logging.Formatter(_CONSOLE_FORMAT)

    handler.setFormatter(formatter)
    return handler


def configure_logging() -> None:
    """Configure the root logger. Idempotent; safe to call at startup."""
    settings = get_settings()
    root = logging.getLogger()

    # Remove any handlers installed by a previous configuration (e.g. reload).
    for existing in list(root.handlers):
        root.removeHandler(existing)

    root.addHandler(_build_handler(settings.LOG_FORMAT))
    root.setLevel(settings.LOG_LEVEL.upper())

    # Tame noisy third-party loggers; let access logging flow through uvicorn.
    logging.getLogger("uvicorn.access").handlers.clear()
    logging.getLogger("uvicorn.error").propagate = True
    logging.getLogger("sqlalchemy.engine").setLevel(
        logging.INFO if settings.DATABASE_ECHO else logging.WARNING
    )


def get_logger(name: str) -> logging.Logger:
    """Return a module-scoped logger."""
    return logging.getLogger(name)
