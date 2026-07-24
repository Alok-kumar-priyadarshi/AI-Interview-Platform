"""Resume and candidate-profile repositories."""

from __future__ import annotations

import uuid

from sqlalchemy import func, select, update

from app.models.candidate_profile import CandidateProfile
from app.models.resume import Resume
from app.repositories.base import BaseRepository


class ResumeRepository(BaseRepository[Resume]):
    model = Resume

    async def list_by_user(self, user_id: uuid.UUID) -> list[Resume]:
        result = await self.session.execute(
            select(Resume).where(Resume.user_id == user_id).order_by(Resume.created_at.desc())
        )
        return list(result.scalars().all())

    async def count_by_user(self, user_id: uuid.UUID) -> int:
        result = await self.session.execute(
            select(func.count(Resume.id)).where(Resume.user_id == user_id)
        )
        return int(result.scalar_one())

    async def get_by_checksum(self, user_id: uuid.UUID, checksum: str) -> Resume | None:
        result = await self.session.execute(
            select(Resume).where(
                Resume.user_id == user_id, Resume.checksum_sha256 == checksum
            )
        )
        return result.scalar_one_or_none()

    async def clear_default(self, user_id: uuid.UUID) -> None:
        """Unset the default flag on all of a user's resumes."""
        await self.session.execute(
            update(Resume).where(Resume.user_id == user_id).values(is_default=False)
        )


class CandidateProfileRepository(BaseRepository[CandidateProfile]):
    model = CandidateProfile

    async def get_by_resume_id(self, resume_id: uuid.UUID) -> CandidateProfile | None:
        result = await self.session.execute(
            select(CandidateProfile).where(CandidateProfile.resume_id == resume_id)
        )
        return result.scalar_one_or_none()
