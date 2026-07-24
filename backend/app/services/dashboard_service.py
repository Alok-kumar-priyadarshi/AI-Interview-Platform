"""Dashboard service — read-only analytics aggregated from interviews/reports."""

from __future__ import annotations

import uuid
from datetime import date, timedelta

from sqlalchemy import func, select
from sqlalchemy.ext.asyncio import AsyncSession

from app.models.enums import InterviewStatus
from app.models.interview import Interview
from app.models.report import Report


class DashboardService:
    def __init__(self, session: AsyncSession) -> None:
        self.session = session

    async def summary(self, user_id: uuid.UUID) -> dict:
        row = (
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
        total, completed, avg_score, max_score = row
        return {
            "total_interviews": int(total or 0),
            "completed_interviews": int(completed or 0),
            "average_score": round(float(avg_score), 2) if avg_score is not None else None,
            "highest_score": float(max_score) if max_score is not None else None,
            "current_streak": await self._current_streak(user_id),
        }

    async def statistics(self, user_id: uuid.UUID) -> dict:
        row = (
            await self.session.execute(
                select(
                    func.count(Interview.id),
                    func.count(Interview.id).filter(
                        Interview.status == InterviewStatus.COMPLETED
                    ),
                    func.count(Interview.id).filter(
                        Interview.status == InterviewStatus.CANCELLED
                    ),
                    func.count(Interview.id).filter(Interview.status == InterviewStatus.FAILED),
                    func.avg(Interview.overall_score),
                    func.max(Interview.overall_score),
                    func.min(Interview.overall_score),
                ).where(Interview.user_id == user_id)
            )
        ).one()
        total, completed, cancelled, failed, avg_score, best, lowest = row
        return {
            "total_interviews": int(total or 0),
            "completed": int(completed or 0),
            "cancelled": int(cancelled or 0),
            "failed": int(failed or 0),
            "average_score": round(float(avg_score), 2) if avg_score is not None else None,
            "best_score": float(best) if best is not None else None,
            "lowest_score": float(lowest) if lowest is not None else None,
        }

    async def trends(self, user_id: uuid.UUID, *, limit: int = 30) -> list[dict]:
        result = await self.session.execute(
            select(Interview.completed_at, Interview.overall_score)
            .where(
                Interview.user_id == user_id,
                Interview.status == InterviewStatus.COMPLETED,
                Interview.overall_score.is_not(None),
            )
            .order_by(Interview.completed_at.asc())
            .limit(limit)
        )
        return [
            {"date": completed_at.date().isoformat(), "score": float(score)}
            for completed_at, score in result.all()
            if completed_at is not None
        ]

    async def recent(self, user_id: uuid.UUID, *, limit: int = 5) -> list[dict]:
        result = await self.session.execute(
            select(Interview)
            .where(
                Interview.user_id == user_id,
                Interview.status == InterviewStatus.COMPLETED,
            )
            .order_by(Interview.completed_at.desc())
            .limit(limit)
        )
        return [
            {
                "interview_id": str(i.id),
                "type": i.target_role,
                "mode": i.interview_type,
                "score": float(i.overall_score) if i.overall_score is not None else None,
                "completed_at": i.completed_at.isoformat() if i.completed_at else None,
            }
            for i in result.scalars().all()
        ]

    async def recommendations(self, user_id: uuid.UUID) -> list[dict]:
        row = (
            await self.session.execute(
                select(Report)
                .join(Interview, Report.interview_id == Interview.id)
                .where(Interview.user_id == user_id)
                .order_by(Report.generated_at.desc())
                .limit(1)
            )
        ).scalar_one_or_none()
        if row is None:
            return []
        recommendations: list[dict] = []
        for index, item in enumerate(row.improvement_roadmap or []):
            if isinstance(item, dict):
                recommendations.append(
                    {
                        "priority": "high" if index == 0 else "medium",
                        "title": item.get("topic", "Improvement"),
                        "description": item.get("recommendation", ""),
                    }
                )
        return recommendations

    async def achievements(self, user_id: uuid.UUID) -> list[dict]:
        summary = await self.summary(user_id)
        achievements: list[dict] = []
        if summary["completed_interviews"] >= 1:
            achievements.append({"id": "first_interview", "title": "First Interview Completed"})
        if summary["highest_score"] is not None and summary["highest_score"] >= 90:
            achievements.append({"id": "score_90", "title": "Scored Above 90"})
        if summary["completed_interviews"] >= 10:
            achievements.append({"id": "ten_interviews", "title": "Ten Interviews Completed"})
        return achievements

    async def overview(self, user_id: uuid.UUID) -> dict:
        return {
            "summary": await self.summary(user_id),
            "recent_interviews": await self.recent(user_id),
            "recommendations": await self.recommendations(user_id),
            "achievements": await self.achievements(user_id),
        }

    async def _current_streak(self, user_id: uuid.UUID) -> int:
        result = await self.session.execute(
            select(Interview.completed_at)
            .where(
                Interview.user_id == user_id,
                Interview.status == InterviewStatus.COMPLETED,
                Interview.completed_at.is_not(None),
            )
            .order_by(Interview.completed_at.desc())
        )
        days = {row[0].date() for row in result.all() if row[0] is not None}
        if not days:
            return 0
        streak = 0
        cursor = date.today()
        # Allow the streak to start today or yesterday.
        if cursor not in days and (cursor - timedelta(days=1)) in days:
            cursor -= timedelta(days=1)
        while cursor in days:
            streak += 1
            cursor -= timedelta(days=1)
        return streak
