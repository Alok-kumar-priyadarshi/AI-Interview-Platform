"""Interview, question, and answer repositories."""

from __future__ import annotations

import uuid

from sqlalchemy import Select, func, select

from app.models.interview import Interview
from app.models.interview_answer import InterviewAnswer
from app.models.interview_question import InterviewQuestion
from app.repositories.base import BaseRepository

_SORTABLE = {"created_at": Interview.created_at, "overall_score": Interview.overall_score}


class InterviewRepository(BaseRepository[Interview]):
    model = Interview

    def _filtered(
        self,
        user_id: uuid.UUID,
        *,
        status: str | None,
        difficulty: str | None,
        mode: str | None,
    ) -> Select:
        query = select(Interview).where(Interview.user_id == user_id)
        if status:
            query = query.where(Interview.status == status)
        if difficulty:
            query = query.where(Interview.difficulty == difficulty)
        if mode:
            query = query.where(Interview.interview_type == mode)
        return query

    async def list_paginated(
        self,
        user_id: uuid.UUID,
        *,
        page: int,
        page_size: int,
        status: str | None = None,
        difficulty: str | None = None,
        mode: str | None = None,
        sort: str = "-created_at",
    ) -> tuple[list[Interview], int]:
        base = self._filtered(user_id, status=status, difficulty=difficulty, mode=mode)

        total = (
            await self.session.execute(
                select(func.count()).select_from(base.subquery())
            )
        ).scalar_one()

        descending = sort.startswith("-")
        column = _SORTABLE.get(sort.lstrip("-"), Interview.created_at)
        order = column.desc() if descending else column.asc()

        result = await self.session.execute(
            base.order_by(order).limit(page_size).offset((page - 1) * page_size)
        )
        return list(result.scalars().all()), int(total)


class InterviewQuestionRepository(BaseRepository[InterviewQuestion]):
    model = InterviewQuestion

    async def list_by_interview(self, interview_id: uuid.UUID) -> list[InterviewQuestion]:
        result = await self.session.execute(
            select(InterviewQuestion)
            .where(InterviewQuestion.interview_id == interview_id)
            .order_by(InterviewQuestion.question_number)
        )
        return list(result.scalars().all())

    async def get_by_number(
        self, interview_id: uuid.UUID, number: int
    ) -> InterviewQuestion | None:
        result = await self.session.execute(
            select(InterviewQuestion).where(
                InterviewQuestion.interview_id == interview_id,
                InterviewQuestion.question_number == number,
            )
        )
        return result.scalar_one_or_none()


class InterviewAnswerRepository(BaseRepository[InterviewAnswer]):
    model = InterviewAnswer

    async def get_by_question(self, question_id: uuid.UUID) -> InterviewAnswer | None:
        result = await self.session.execute(
            select(InterviewAnswer).where(InterviewAnswer.question_id == question_id)
        )
        return result.scalar_one_or_none()

    async def list_by_interview(self, interview_id: uuid.UUID) -> list[InterviewAnswer]:
        result = await self.session.execute(
            select(InterviewAnswer)
            .join(InterviewQuestion, InterviewAnswer.question_id == InterviewQuestion.id)
            .where(InterviewQuestion.interview_id == interview_id)
            .order_by(InterviewQuestion.question_number)
        )
        return list(result.scalars().all())
