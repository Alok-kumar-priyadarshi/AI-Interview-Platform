"""SQLAlchemy declarative base and shared column mixins.

Encodes the database conventions from ``docs/04-database/schema-overview.md``:

* **UUID primary keys** on every table (``id``).
* **Audit timestamps** (``created_at`` / ``updated_at``) on every business table.
* A deterministic **constraint naming convention** (``pk_``, ``fk_``, ``uq_``,
  ``ck_``, ``ix_``) so Alembic autogenerate produces stable, predictable names.

Types are chosen for cross-dialect portability: :class:`sqlalchemy.Uuid` maps to
native ``UUID`` on PostgreSQL and ``CHAR(32)`` on SQLite, allowing the same
models to back both production Postgres and the in-memory SQLite test database.
"""

from __future__ import annotations

import uuid
from datetime import UTC, datetime

from sqlalchemy import DateTime, MetaData, Uuid, func
from sqlalchemy.orm import DeclarativeBase, Mapped, mapped_column

# Deterministic constraint naming — see schema-overview.md (Naming Conventions):
# pk_ / fk_ / uq_ / chk_ / idx_.
NAMING_CONVENTION = {
    "ix": "idx_%(table_name)s_%(column_0_N_name)s",
    "uq": "uq_%(table_name)s_%(column_0_N_name)s",
    "ck": "chk_%(table_name)s_%(constraint_name)s",
    "fk": "fk_%(table_name)s_%(column_0_name)s_%(referred_table_name)s",
    "pk": "pk_%(table_name)s",
}


class Base(DeclarativeBase):
    """Declarative base shared by every ORM model."""

    metadata = MetaData(naming_convention=NAMING_CONVENTION)


class UUIDPrimaryKeyMixin:
    """Adds a UUID ``id`` primary key generated application-side."""

    id: Mapped[uuid.UUID] = mapped_column(
        Uuid,
        primary_key=True,
        default=uuid.uuid4,
    )


class TimestampMixin:
    """Adds ``created_at`` / ``updated_at`` audit columns.

    ``created_at`` is set once on insert; ``updated_at`` is refreshed on every
    update. Both use database-side defaults so timestamps remain correct even
    for rows created outside the ORM.
    """

    created_at: Mapped[datetime] = mapped_column(
        DateTime(timezone=True),
        nullable=False,
        server_default=func.now(),
    )
    # Python-side ``onupdate`` (not SQL ``func.now()``) so the new value is set
    # on the instance during flush and does not require a post-flush reload —
    # which would attempt async DB IO during synchronous response serialisation.
    updated_at: Mapped[datetime] = mapped_column(
        DateTime(timezone=True),
        nullable=False,
        server_default=func.now(),
        onupdate=lambda: datetime.now(UTC),
    )
