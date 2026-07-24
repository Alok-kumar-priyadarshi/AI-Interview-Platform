"""Shared API schema primitives.

Defines the standard success/error envelopes and the pagination container used
across every endpoint, per ``docs/05-api-design/README.md`` and
``docs/05-api-design/errors.md``. Keeping these in one place guarantees a
consistent contract for the frontend.
"""

from __future__ import annotations

from typing import Generic, TypeVar

from pydantic import BaseModel, Field

T = TypeVar("T")


class SuccessResponse(BaseModel, Generic[T]):
    """Envelope for every successful response.

    Example::

        {"success": true, "message": "Interview created successfully.", "data": {...}}
    """

    success: bool = True
    message: str = "OK"
    data: T | None = None


class ErrorDetail(BaseModel):
    """A single field-level validation detail."""

    field: str
    message: str


class ErrorBody(BaseModel):
    code: str = Field(..., description="Machine-readable error identifier.")
    message: str = Field(..., description="Human-readable error summary.")
    details: list[ErrorDetail] | None = None


class ErrorResponse(BaseModel):
    """Envelope for every failed response."""

    success: bool = False
    error: ErrorBody
    request_id: str | None = None


class PaginationMeta(BaseModel):
    page: int = Field(..., ge=1)
    page_size: int = Field(..., ge=1)
    total: int = Field(..., ge=0)
    total_pages: int = Field(..., ge=0)


class Page(BaseModel, Generic[T]):
    """Paginated collection container.

    Mirrors the pagination shape documented in
    ``docs/05-api-design/pagination.md``.
    """

    items: list[T]
    page: int
    page_size: int
    total: int
    total_pages: int

    @classmethod
    def create(cls, items: list[T], *, page: int, page_size: int, total: int) -> Page[T]:
        total_pages = (total + page_size - 1) // page_size if page_size else 0
        return cls(
            items=items,
            page=page,
            page_size=page_size,
            total=total,
            total_pages=total_pages,
        )
