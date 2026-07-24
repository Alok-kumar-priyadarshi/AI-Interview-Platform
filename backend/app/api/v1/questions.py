"""Interview question delivery endpoints — see docs/05-api-design/questions.md."""

from __future__ import annotations

import uuid
from typing import Annotated

from fastapi import APIRouter, Depends

from app.dependencies.auth import CurrentUser
from app.dependencies.interview import get_interview_service
from app.schemas.common import SuccessResponse
from app.schemas.interview import CurrentQuestion, QuestionDetail, QuestionListItem
from app.services.interview_service import InterviewService

router = APIRouter(prefix="/interviews", tags=["Questions"])

ServiceDep = Annotated[InterviewService, Depends(get_interview_service)]


@router.get("/{interview_id}/questions/current", summary="Get the current question")
async def get_current_question(
    user: CurrentUser, service: ServiceDep, interview_id: uuid.UUID
) -> SuccessResponse[CurrentQuestion]:
    q = await service.current_question(user, interview_id)
    return SuccessResponse(
        message="OK",
        data=CurrentQuestion(
            question_id=q.id,
            sequence=q.question_number,
            category=q.category,
            difficulty=q.difficulty,
            question=q.question_text,
            estimated_time_seconds=q.estimated_time_seconds,
        ),
    )


@router.get("/{interview_id}/questions", summary="List questions (completed interviews)")
async def list_questions(
    user: CurrentUser, service: ServiceDep, interview_id: uuid.UUID
) -> SuccessResponse[list[QuestionListItem]]:
    questions = await service.list_questions(user, interview_id)
    return SuccessResponse(
        message="OK",
        data=[
            QuestionListItem(
                id=q.id,
                sequence=q.question_number,
                category=q.category,
                difficulty=q.difficulty,
                question=q.question_text,
            )
            for q in questions
        ],
    )


@router.get("/{interview_id}/questions/{question_id}", summary="Get question details")
async def get_question(
    user: CurrentUser, service: ServiceDep, interview_id: uuid.UUID, question_id: uuid.UUID
) -> SuccessResponse[QuestionDetail]:
    q = await service.get_question(user, interview_id, question_id)
    return SuccessResponse(
        message="OK",
        data=QuestionDetail(
            id=q.id,
            sequence=q.question_number,
            category=q.category,
            difficulty=q.difficulty,
            estimated_time_seconds=q.estimated_time_seconds,
        ),
    )


@router.post("/{interview_id}/questions/{question_id}/next", summary="Advance to next question")
async def next_question(
    user: CurrentUser, service: ServiceDep, interview_id: uuid.UUID, question_id: uuid.UUID
) -> SuccessResponse[dict]:
    q = await service.next_question(user, interview_id, question_id)
    return SuccessResponse(
        message="OK", data={"next_question_id": str(q.id), "sequence": q.question_number}
    )
