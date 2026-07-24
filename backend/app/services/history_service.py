"""History service.

Version 1 has no dedicated history table — history is a read projection over
**completed** interviews joined with their reports (docs/05-api-design/history.md:
"Archive == Completed Interviews"). The ``history_id`` is the interview id.
"""

from __future__ import annotations

import uuid

from sqlalchemy import func, select
from sqlalchemy.ext.asyncio import AsyncSession

from app.exceptions.base import HistoryNotFoundError
from app.models.enums import InterviewStatus
from app.models.interview import Interview
from app.models.report import Report
from app.repositories.interview_repository import InterviewRepository


class HistoryService:
    def __init__(self, session: AsyncSession) -> None:
        self.session = session
        self.interviews = InterviewRepository(session)

    def _base_query(self, user_id: uuid.UUID, *, keyword: str | None = None):
        query = (
            select(Interview, Report)
            .outerjoin(Report, Report.interview_id == Interview.id)
            .where(
                Interview.user_id == user_id,
                Interview.status == InterviewStatus.COMPLETED,
            )
        )
        if keyword:
            like = f"%{keyword.lower()}%"
            query = query.where(func.lower(Interview.target_role).like(like))
        return query

    async def list(
        self, user, *, page: int, page_size: int, keyword: str | None = None
    ) -> tuple[list[tuple[Interview, Report | None]], int]:
        base = self._base_query(user.id, keyword=keyword)
        total = (
            await self.session.execute(select(func.count()).select_from(base.subquery()))
        ).scalar_one()
        result = await self.session.execute(
            base.order_by(Interview.completed_at.desc())
            .limit(page_size)
            .offset((page - 1) * page_size)
        )
        return list(result.all()), int(total)

    async def get(self, user, history_id: uuid.UUID) -> tuple[Interview, Report | None]:
        result = await self.session.execute(
            self._base_query(user.id).where(Interview.id == history_id)
        )
        row = result.first()
        if row is None:
            raise HistoryNotFoundError()
        return row  # (Interview, Report | None)

    async def delete(self, user, history_id: uuid.UUID) -> None:
        interview, _ = await self.get(user, history_id)
        await self.interviews.delete(interview)
        await self.interviews.flush()
