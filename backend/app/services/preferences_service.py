"""Candidate preferences service.

Enforces the business rules from docs/05-api-design/candidate-profile.md:
one profile per user, ownership, and salary-range consistency across partial
updates.
"""

from __future__ import annotations

from sqlalchemy.ext.asyncio import AsyncSession

from app.core.logging import get_logger
from app.exceptions.base import ProfileExistsError, ProfileNotFoundError, ValidationError
from app.models.candidate_preferences import CandidatePreferences
from app.models.user import User
from app.repositories.preferences_repository import CandidatePreferencesRepository
from app.schemas.candidate_preferences import (
    CandidatePreferencesCreate,
    CandidatePreferencesUpdate,
)

logger = get_logger(__name__)


class PreferencesService:
    def __init__(self, session: AsyncSession) -> None:
        self.session = session
        self.repo = CandidatePreferencesRepository(session)

    async def get(self, user: User) -> CandidatePreferences:
        prefs = await self.repo.get_by_user_id(user.id)
        if prefs is None:
            raise ProfileNotFoundError()
        return prefs

    async def create(self, user: User, payload: CandidatePreferencesCreate) -> CandidatePreferences:
        if await self.repo.get_by_user_id(user.id) is not None:
            raise ProfileExistsError()
        prefs = CandidatePreferences(user_id=user.id, **payload.model_dump())
        self.repo.add(prefs)
        await self.repo.flush()
        logger.info("candidate_preferences_created", extra={"user_id": str(user.id)})
        return prefs

    async def update(
        self, user: User, payload: CandidatePreferencesUpdate
    ) -> CandidatePreferences:
        prefs = await self.get(user)
        updates = payload.model_dump(exclude_unset=True)
        for field, value in updates.items():
            setattr(prefs, field, value)

        # Re-validate the salary range against the merged state.
        if (
            prefs.expected_salary_min is not None
            and prefs.expected_salary_max is not None
            and prefs.expected_salary_max < prefs.expected_salary_min
        ):
            raise ValidationError("expected_salary_max must be >= expected_salary_min.")

        await self.repo.flush()
        logger.info("candidate_preferences_updated", extra={"user_id": str(user.id)})
        return prefs

    async def delete(self, user: User) -> None:
        prefs = await self.get(user)
        await self.repo.delete(prefs)
        await self.repo.flush()
