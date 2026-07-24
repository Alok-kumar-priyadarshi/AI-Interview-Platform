"""User service — business logic for user identity and provisioning."""

from __future__ import annotations

import uuid
from datetime import UTC, datetime

from sqlalchemy import delete, func, select
from sqlalchemy.ext.asyncio import AsyncSession

from app.core.logging import get_logger
from app.exceptions.base import UserNotFoundError
from app.models.enums import InterviewStatus, UserRole
from app.models.interview import Interview
from app.models.report import Report
from app.models.resume import Resume
from app.models.user import User
from app.repositories.user_repository import UserRepository
from app.schemas.auth import GoogleIdentity
from app.schemas.user import UserStatistics

logger = get_logger(__name__)


class UserService:
    def __init__(self, session: AsyncSession) -> None:
        self.session = session
        self.users = UserRepository(session)

    async def get_by_id(self, user_id: uuid.UUID) -> User:
        user = await self.users.get(user_id)
        if user is None:
            raise UserNotFoundError()
        return user

    async def get_or_create_from_google(self, identity: GoogleIdentity) -> tuple[User, bool]:
        """Provision a user from a verified Google identity.

        Returns ``(user, created)``. Existing users have their mutable profile
        fields and ``last_login_at`` refreshed; new users are created with the
        default candidate role.
        """
        now = datetime.now(UTC)
        user = await self.users.get_by_google_id(identity.google_id)
        created = False

        if user is None:
            user = User(
                google_id=identity.google_id,
                email=identity.email.lower(),
                full_name=identity.full_name.strip(),
                profile_picture_url=identity.picture,
                role=UserRole.CANDIDATE,
                last_login_at=now,
            )
            self.users.add(user)
            created = True
            logger.info("user_provisioned", extra={"email": user.email})
        else:
            # Refresh profile data that may have changed on Google's side.
            user.full_name = identity.full_name.strip() or user.full_name
            user.profile_picture_url = identity.picture
            user.last_login_at = now

        await self.users.flush()
        return user, created

    async def update_profile(self, user: User, *, full_name: str) -> User:
        """Update the user's editable profile fields."""
        user.full_name = full_name
        await self.users.flush()
        logger.info("user_profile_updated", extra={"user_id": str(user.id)})
        return user

    async def get_statistics(self, user_id: uuid.UUID) -> UserStatistics:
        """Aggregate interview/report/resume statistics for the user."""
        totals = (
            await self.session.execute(
                select(
                    func.count(Interview.id),
                    func.count(Interview.id).filter(
                        Interview.status == InterviewStatus.COMPLETED
                    ),
                    func.avg(Interview.overall_score),
                    func.max(Interview.overall_score),
                ).where(Interview.user_id == user_id)
            )
        ).one()
        total_interviews, completed, avg_score, max_score = totals

        reports_generated = (
            await self.session.execute(
                select(func.count(Report.id))
                .join(Interview, Report.interview_id == Interview.id)
                .where(Interview.user_id == user_id)
            )
        ).scalar_one()
        resume_count = (
            await self.session.execute(
                select(func.count(Resume.id)).where(Resume.user_id == user_id)
            )
        ).scalar_one()

        return UserStatistics(
            total_interviews=int(total_interviews or 0),
            completed_interviews=int(completed or 0),
            average_score=round(float(avg_score), 2) if avg_score is not None else None,
            highest_score=float(max_score) if max_score is not None else None,
            reports_generated=int(reports_generated or 0),
            resume_count=int(resume_count or 0),
        )

    async def delete_account(self, user: User) -> None:
        """Hard-delete the user's account and all owned data.

        Children are removed in FK-safe order (interviews before resumes,
        because ``interviews.resume_id`` uses ``ON DELETE RESTRICT``).
        """
        await self.session.execute(delete(Interview).where(Interview.user_id == user.id))
        await self.session.execute(delete(Resume).where(Resume.user_id == user.id))
        await self.users.delete(user)
        await self.users.flush()
        logger.info("user_account_deleted", extra={"user_id": str(user.id)})
