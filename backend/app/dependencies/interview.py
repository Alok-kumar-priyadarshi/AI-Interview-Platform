"""Interview dependency wiring."""

from __future__ import annotations

from typing import Annotated

from fastapi import Depends
from sqlalchemy.ext.asyncio import AsyncSession

from app.ai.service import AIService
from app.database.session import get_db
from app.dependencies.ai import get_ai_service
from app.dependencies.resume import get_storage
from app.services.interview_service import InterviewService
from app.services.storage import StorageProvider


def get_interview_service(
    db: Annotated[AsyncSession, Depends(get_db)],
    ai_service: Annotated[AIService, Depends(get_ai_service)],
    storage: Annotated[StorageProvider, Depends(get_storage)],
) -> InterviewService:
    return InterviewService(db, ai_service, storage)
