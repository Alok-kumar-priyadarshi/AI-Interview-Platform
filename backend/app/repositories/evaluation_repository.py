"""Evaluation and report repositories."""

from __future__ import annotations

import uuid

from sqlalchemy import func, select

from app.models.evaluation import Evaluation
from app.models.interview import Interview
from app.models.interview_answer import InterviewAnswer
from app.models.interview_question import InterviewQuestion
from app.models.report import Report
from app.repositories.base import BaseRepository


class EvaluationRepository(BaseRepository[Evaluation]):
    model = Evaluation

    async def get_by_answer(self, answer_id: uuid.UUID) -> Evaluation | None:
        result = await self.session.execute(
            select(Evaluation).where(Evaluation.answer_id == answer_id)
        )
        return result.scalar_one_or_none()

    async def list_by_interview(self, interview_id: uuid.UUID) -> list[Evaluation]:
        result = await self.session.execute(
            select(Evaluation)
            .join(InterviewAnswer, Evaluation.answer_id == InterviewAnswer.id)
            .join(InterviewQuestion, InterviewAnswer.question_id == InterviewQuestion.id)
            .where(InterviewQuestion.interview_id == interview_id)
            .order_by(InterviewQuestion.question_number)
        )
        return list(result.scalars().all())

    async def interview_id_for(self, evaluation: Evaluation) -> uuid.UUID | None:
        """Resolve the owning interview id for an evaluation (via answer→question)."""
        result = await self.session.execute(
            select(InterviewQuestion.interview_id)
            .join(InterviewAnswer, InterviewAnswer.question_id == InterviewQuestion.id)
            .where(InterviewAnswer.id == evaluation.answer_id)
        )
        return result.scalar_one_or_none()


class ReportRepository(BaseRepository[Report]):
    model = Report

    async def get_by_interview(self, interview_id: uuid.UUID) -> Report | None:
        result = await self.session.execute(
            select(Report).where(Report.interview_id == interview_id)
        )
        return result.scalar_one_or_none()

    async def list_by_user(
        self, user_id: uuid.UUID, *, page: int, page_size: int
    ) -> tuple[list[Report], int]:
        base = (
            select(Report)
            .join(Interview, Report.interview_id == Interview.id)
            .where(Interview.user_id == user_id)
        )
        total = (
            await self.session.execute(select(func.count()).select_from(base.subquery()))
        ).scalar_one()
        result = await self.session.execute(
            base.order_by(Report.generated_at.desc())
            .limit(page_size)
            .offset((page - 1) * page_size)
        )
        return list(result.scalars().all()), int(total)
