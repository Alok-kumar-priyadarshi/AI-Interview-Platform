"""Portable column types.

The models must run against PostgreSQL in production and SQLite (via aiosqlite)
in the test suite. These type aliases resolve to the rich PostgreSQL types where
available and fall back to portable equivalents elsewhere:

* :data:`JSONB` → ``JSONB`` on PostgreSQL, generic ``JSON`` (stored as TEXT) on SQLite.
* :data:`INET` → ``INET`` on PostgreSQL, ``VARCHAR(45)`` (fits IPv6) on SQLite.

Reusing a single ``with_variant`` instance across columns is supported by
SQLAlchemy — type engines are shared, not mutated.
"""

from __future__ import annotations

from sqlalchemy import JSON, String
from sqlalchemy.dialects import postgresql

# JSONB on PostgreSQL; generic JSON elsewhere.
JSONB = JSON().with_variant(postgresql.JSONB(), "postgresql")

# INET on PostgreSQL; VARCHAR(45) elsewhere (max length of an IPv6 string).
INET = String(45).with_variant(postgresql.INET(), "postgresql")
