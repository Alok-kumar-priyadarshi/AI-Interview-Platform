"""Application entrypoint and factory.

Builds and configures the FastAPI application: logging, middleware stack, CORS,
centralised exception handling, versioned routers, and lifespan management for
the database connection pool.

Run locally with::

    uvicorn app.main:app --reload
"""

from __future__ import annotations

from collections.abc import AsyncIterator
from contextlib import asynccontextmanager

from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

from app.api.v1.router import api_router
from app.core.config import get_settings
from app.core.logging import configure_logging, get_logger
from app.database.session import dispose_engine
from app.exceptions.handlers import register_exception_handlers
from app.middleware.request_context import RequestContextMiddleware

logger = get_logger(__name__)


@asynccontextmanager
async def lifespan(_: FastAPI) -> AsyncIterator[None]:
    """Manage startup and shutdown side effects."""
    settings = get_settings()
    configure_logging()
    logger.info(
        "application_startup",
        extra={"app": settings.APP_NAME, "version": settings.APP_VERSION, "env": settings.APP_ENV},
    )
    try:
        yield
    finally:
        await dispose_engine()
        logger.info("application_shutdown")


def create_app() -> FastAPI:
    """Application factory. Returns a fully-configured FastAPI instance."""
    settings = get_settings()
    configure_logging()

    app = FastAPI(
        title=settings.APP_NAME,
        version=settings.APP_VERSION,
        description="REST API for the AI Career Interview Platform.",
        docs_url="/docs",
        redoc_url="/redoc",
        openapi_url="/openapi.json",
        lifespan=lifespan,
    )

    # --- Middleware (executed bottom-up; register in reverse order of run) ---
    app.add_middleware(
        CORSMiddleware,
        allow_origins=settings.CORS_ALLOWED_ORIGINS,
        allow_credentials=True,
        allow_methods=["*"],
        allow_headers=["*"],
        expose_headers=["X-Request-ID"],
    )
    app.add_middleware(
        RequestContextMiddleware,
        log_requests=settings.ENABLE_REQUEST_LOGGING,
    )

    # --- Exception handling --------------------------------------------------
    register_exception_handlers(app)

    # --- Routers -------------------------------------------------------------
    app.include_router(api_router, prefix=settings.API_V1_PREFIX)

    return app


app = create_app()
