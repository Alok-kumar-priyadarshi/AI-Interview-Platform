"""Resume dependency wiring."""

from __future__ import annotations

from typing import Annotated

from fastapi import Depends
from sqlalchemy.ext.asyncio import AsyncSession

from app.ai.service import AIService
from app.core.config import Settings, get_settings
from app.database.session import get_db
from app.dependencies.ai import get_ai_service
from app.services.resume_service import ResumeService
from app.services.storage import StorageProvider, build_storage


def get_storage(settings: Annotated[Settings, Depends(get_settings)]) -> StorageProvider:
    return build_storage(settings)


def get_resume_service(
    db: Annotated[AsyncSession, Depends(get_db)],
    storage: Annotated[StorageProvider, Depends(get_storage)],
    ai_service: Annotated[AIService, Depends(get_ai_service)],
) -> ResumeService:
    return ResumeService(db, storage, ai_service)
