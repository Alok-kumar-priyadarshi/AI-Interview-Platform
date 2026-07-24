"""Candidate preferences repository."""

from __future__ import annotations

import uuid

from sqlalchemy import select

from app.models.candidate_preferences import CandidatePreferences
from app.repositories.base import BaseRepository


class CandidatePreferencesRepository(BaseRepository[CandidatePreferences]):
    model = CandidatePreferences

    async def get_by_user_id(self, user_id: uuid.UUID) -> CandidatePreferences | None:
        result = await self.session.execute(
            select(CandidatePreferences).where(CandidatePreferences.user_id == user_id)
        )
        return result.scalar_one_or_none()
