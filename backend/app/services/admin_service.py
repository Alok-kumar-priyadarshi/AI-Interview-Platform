"""Admin service — platform-wide monitoring and user management (admin-only).

Version 1 has a single ``is_active`` flag rather than a status enum, so the
documented Active/Suspended/Disabled statuses map onto it (Active → active,
Suspended/Disabled → inactive).
"""

from __future__ import annotations

import uuid

from sqlalchemy import func, or_, select
from sqlalchemy.ext.asyncio import AsyncSession

from app.exceptions.base import UserNotFoundError, ValidationError
from app.models.audit_log import AuditLog
from app.models.enums import InterviewStatus
from app.models.evaluation import Evaluation
from app.models.interview import Interview
from app.models.report import Report
from app.models.resume import Resume
from app.models.user import User

_STATUS_TO_ACTIVE = {"active": True, "suspended": False, "disabled": False}


class AdminService:
    def __init__(self, session: AsyncSession) -> None:
        self.session = session

    async def platform_dashboard(self) -> dict:
        total_users = (await self.session.execute(select(func.count(User.id)))).scalar_one()
        active_users = (
            await self.session.execute(
                select(func.count(User.id)).where(User.is_active.is_(True))
            )
        ).scalar_one()
        total_interviews = (
            await self.session.execute(select(func.count(Interview.id)))
        ).scalar_one()
        completed = (
            await self.session.execute(
                select(func.count(Interview.id)).where(
                    Interview.status == InterviewStatus.COMPLETED
                )
            )
        ).scalar_one()
        reports = (await self.session.execute(select(func.count(Report.id)))).scalar_one()
        return {
            "total_users": int(total_users),
            "active_users": int(active_users),
            "total_interviews": int(total_interviews),
            "completed_interviews": int(completed),
            "reports_generated": int(reports),
            "system_status": "healthy",
        }

    async def list_users(
        self,
        *,
        page: int,
        page_size: int,
        search: str | None = None,
        role: str | None = None,
        status: str | None = None,
    ) -> tuple[list[User], int]:
        query = select(User)
        if search:
            like = f"%{search.lower()}%"
            query = query.where(
                or_(func.lower(User.email).like(like), func.lower(User.full_name).like(like))
            )
        if role:
            query = query.where(User.role == role)
        if status:
            active = _STATUS_TO_ACTIVE.get(status.lower())
            if active is not None:
                query = query.where(User.is_active.is_(active))
        total = (
            await self.session.execute(select(func.count()).select_from(query.subquery()))
        ).scalar_one()
        result = await self.session.execute(
            query.order_by(User.created_at.desc()).limit(page_size).offset((page - 1) * page_size)
        )
        return list(result.scalars().all()), int(total)

    async def get_user_details(self, user_id: uuid.UUID) -> dict:
        user = await self.session.get(User, user_id)
        if user is None:
            raise UserNotFoundError()
        resume_count = (
            await self.session.execute(
                select(func.count(Resume.id)).where(Resume.user_id == user_id)
            )
        ).scalar_one()
        interview_count = (
            await self.session.execute(
                select(func.count(Interview.id)).where(Interview.user_id == user_id)
            )
        ).scalar_one()
        evaluation_count = (
            await self.session.execute(
                select(func.count(Evaluation.id))
                .join(Interview, Interview.id == Report.interview_id, isouter=True)
                .where(Interview.user_id == user_id)
            )
        ).scalar_one()
        return {
            "id": str(user.id),
            "name": user.full_name,
            "email": user.email,
            "role": user.role,
            "status": "active" if user.is_active else "inactive",
            "resume_count": int(resume_count),
            "interview_count": int(interview_count),
            "evaluation_count": int(evaluation_count),
            "last_login_at": user.last_login_at.isoformat() if user.last_login_at else None,
        }

    async def update_user_status(self, user_id: uuid.UUID, status: str) -> User:
        active = _STATUS_TO_ACTIVE.get(status.lower())
        if active is None:
            raise ValidationError("Status must be one of: active, suspended, disabled.")
        user = await self.session.get(User, user_id)
        if user is None:
            raise UserNotFoundError()
        user.is_active = active
        await self.session.flush()
        return user

    async def list_interviews(self, *, page: int, page_size: int) -> tuple[list[Interview], int]:
        total = (await self.session.execute(select(func.count(Interview.id)))).scalar_one()
        result = await self.session.execute(
            select(Interview)
            .order_by(Interview.created_at.desc())
            .limit(page_size)
            .offset((page - 1) * page_size)
        )
        return list(result.scalars().all()), int(total)

    async def list_reports(self, *, page: int, page_size: int) -> tuple[list[Report], int]:
        total = (await self.session.execute(select(func.count(Report.id)))).scalar_one()
        result = await self.session.execute(
            select(Report)
            .order_by(Report.generated_at.desc())
            .limit(page_size)
            .offset((page - 1) * page_size)
        )
        return list(result.scalars().all()), int(total)

    async def evaluation_stats(self) -> dict:
        total = (await self.session.execute(select(func.count(Evaluation.id)))).scalar_one()
        return {"completed": int(total), "processing": 0, "failed": 0}

    async def list_audit_logs(self, *, page: int, page_size: int) -> tuple[list[AuditLog], int]:
        total = (await self.session.execute(select(func.count(AuditLog.id)))).scalar_one()
        result = await self.session.execute(
            select(AuditLog)
            .order_by(AuditLog.occurred_at.desc())
            .limit(page_size)
            .offset((page - 1) * page_size)
        )
        return list(result.scalars().all()), int(total)
