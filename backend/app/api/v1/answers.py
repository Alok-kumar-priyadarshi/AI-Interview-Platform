"""Interview answer endpoints — see docs/05-api-design/answers.md.

Version 1 supports text answers. Voice upload + Whisper transcription is a
later increment (requires audio storage + the transcription pipeline).
"""

from __future__ import annotations

import uuid
from typing import Annotated

from fastapi import APIRouter, Depends, File, Form, UploadFile, status

from app.dependencies.auth import CurrentUser
from app.dependencies.interview import get_interview_service
from app.schemas.common import SuccessResponse
from app.schemas.interview import AnswerDetail, AnswerResult, AnswerSubmit, TranscriptResponse
from app.services.interview_service import InterviewService

router = APIRouter(prefix="/interviews", tags=["Answers"])

ServiceDep = Annotated[InterviewService, Depends(get_interview_service)]


@router.post(
    "/{interview_id}/answers", status_code=status.HTTP_201_CREATED, summary="Submit text answer"
)
async def submit_answer(
    user: CurrentUser, service: ServiceDep, interview_id: uuid.UUID, payload: AnswerSubmit
) -> SuccessResponse[AnswerResult]:
    answer = await service.submit_text_answer(
        user, interview_id, question_id=payload.question_id, answer=payload.answer
    )
    return SuccessResponse(
        message="Answer submitted successfully.",
        data=AnswerResult(answer_id=answer.id, submitted_at=answer.submitted_at),
    )


@router.post(
    "/{interview_id}/answers/voice",
    status_code=status.HTTP_201_CREATED,
    summary="Upload voice answer",
)
async def submit_voice_answer(
    user: CurrentUser,
    service: ServiceDep,
    interview_id: uuid.UUID,
    question_id: Annotated[uuid.UUID, Form(...)],
    audio: Annotated[UploadFile, File(...)],
    language: Annotated[str, Form()] = "en",
) -> SuccessResponse[dict]:
    data = await audio.read()
    answer = await service.submit_voice_answer(
        user,
        interview_id,
        question_id=question_id,
        filename=audio.filename or "answer.webm",
        content_type=audio.content_type,
        data=data,
        language=language,
    )
    return SuccessResponse(
        message="Voice answer uploaded.",
        data={"answer_id": str(answer.id), "transcription_status": "completed"},
    )


@router.get("/{interview_id}/answers", summary="List answers (completed interviews)")
async def list_answers(
    user: CurrentUser, service: ServiceDep, interview_id: uuid.UUID
) -> SuccessResponse[list[AnswerDetail]]:
    answers = await service.list_answers(user, interview_id)
    return SuccessResponse(
        message="OK",
        data=[
            AnswerDetail(
                answer_id=a.id,
                question_id=a.question_id,
                type=a.answer_type,
                submitted_at=a.submitted_at,
                response_time_seconds=a.response_time_seconds,
            )
            for a in answers
        ],
    )


@router.get(
    "/{interview_id}/answers/{answer_id}/transcript", summary="Get voice answer transcript"
)
async def get_transcript(
    user: CurrentUser, service: ServiceDep, interview_id: uuid.UUID, answer_id: uuid.UUID
) -> SuccessResponse[TranscriptResponse]:
    transcript = await service.get_transcript(user, interview_id, answer_id)
    return SuccessResponse(message="OK", data=TranscriptResponse(**transcript))


@router.get("/{interview_id}/answers/{answer_id}", summary="Get answer details")
async def get_answer(
    user: CurrentUser, service: ServiceDep, interview_id: uuid.UUID, answer_id: uuid.UUID
) -> SuccessResponse[AnswerDetail]:
    a = await service.get_answer(user, interview_id, answer_id)
    return SuccessResponse(
        message="OK",
        data=AnswerDetail(
            answer_id=a.id,
            question_id=a.question_id,
            type=a.answer_type,
            submitted_at=a.submitted_at,
            response_time_seconds=a.response_time_seconds,
        ),
    )
