"""Async database engine and session management.

Creates the process-wide async engine and session factory, and exposes the
``get_db`` FastAPI dependency that yields one session per request. Sessions are
never shared across requests (see
``docs/03-architecture/backend-architecture.md`` — Database Session Management).

The engine is created lazily so that importing this module never requires a
live database (important for tooling and unit tests that stub the session).
"""

from __future__ import annotations

from collections.abc import AsyncGenerator

from sqlalchemy.ext.asyncio import (
    AsyncEngine,
    AsyncSession,
    async_sessionmaker,
    create_async_engine,
)

from app.core.config import get_settings
from app.core.logging import get_logger

logger = get_logger(__name__)

_engine: AsyncEngine | None = None
_session_factory: async_sessionmaker[AsyncSession] | None = None


def get_engine() -> AsyncEngine:
    """Return the lazily-initialised async engine."""
    global _engine
    if _engine is None:
        settings = get_settings()
        _engine = create_async_engine(
            settings.async_database_url,
            echo=settings.DATABASE_ECHO,
            pool_size=settings.DATABASE_POOL_SIZE,
            max_overflow=settings.DATABASE_MAX_OVERFLOW,
            pool_timeout=settings.DATABASE_POOL_TIMEOUT,
            pool_pre_ping=True,  # transparently recycle stale connections
            future=True,
        )
        logger.info("database_engine_initialised", extra={"pool_size": settings.DATABASE_POOL_SIZE})
    return _engine


def get_session_factory() -> async_sessionmaker[AsyncSession]:
    """Return the lazily-initialised session factory."""
    global _session_factory
    if _session_factory is None:
        _session_factory = async_sessionmaker(
            bind=get_engine(),
            class_=AsyncSession,
            expire_on_commit=False,
            autoflush=False,
        )
    return _session_factory


async def get_db() -> AsyncGenerator[AsyncSession]:
    """FastAPI dependency that yields a request-scoped session.

    The session is committed on success and rolled back on any exception, then
    always closed. Service-layer code may also manage explicit transactions;
    this dependency guarantees a clean session lifecycle per request.
    """
    session_factory = get_session_factory()
    async with session_factory() as session:
        try:
            yield session
            await session.commit()
        except Exception:
            await session.rollback()
            raise
        finally:
            await session.close()


async def dispose_engine() -> None:
    """Dispose the engine's connection pool (called on application shutdown)."""
    global _engine
    if _engine is not None:
        await _engine.dispose()
        _engine = None
        logger.info("database_engine_disposed")
