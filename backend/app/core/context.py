"""Request-scoped context.

Holds the correlation (request) ID and authenticated user ID for the current
request in :class:`contextvars.ContextVar` slots. This lets the logging layer
attach correlation data to every log record without threading identifiers
through every function signature.
"""

from __future__ import annotations

from contextvars import ContextVar

request_id_ctx: ContextVar[str | None] = ContextVar("request_id", default=None)
user_id_ctx: ContextVar[str | None] = ContextVar("user_id", default=None)


def get_request_id() -> str | None:
    return request_id_ctx.get()


def get_user_id() -> str | None:
    return user_id_ctx.get()
