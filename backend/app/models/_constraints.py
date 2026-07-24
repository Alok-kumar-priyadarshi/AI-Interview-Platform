"""Helpers for building table constraints from domain enums.

Keeps ``CHECK`` constraint definitions DRY: the allowed values come from the
enums in :mod:`app.models.enums`, so a new enum member automatically widens the
constraint without editing raw SQL.
"""

from __future__ import annotations

from enum import StrEnum

from sqlalchemy import CheckConstraint

from app.models.enums import values


def enum_check(column: str, enum_cls: type[StrEnum], name: str) -> CheckConstraint:
    """Return a ``CHECK (<column> IN (...))`` constraint for an enum column."""
    allowed = ", ".join(f"'{value}'" for value in values(enum_cls))
    return CheckConstraint(f"{column} IN ({allowed})", name=name)


def range_check(column: str, name: str, *, low: float = 0, high: float = 100) -> CheckConstraint:
    """Return a ``CHECK (<column> BETWEEN low AND high)`` constraint (nullable-safe)."""
    expr = f"{column} IS NULL OR ({column} >= {low} AND {column} <= {high})"
    return CheckConstraint(expr, name=name)
