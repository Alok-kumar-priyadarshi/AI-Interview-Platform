"""Interview lifecycle endpoints — see docs/05-api-design/interviews.md."""

from __future__ import annotations

import uuid
from typing import Annotated

from fastapi import APIRouter, Depends, Query, status

from app.dependencies.auth import CurrentUser
from app.dependencies.interview import get_interview_service
from app.schemas.common import Page, SuccessResponse
from app.schemas.interview import (
    InterviewCreate,
    InterviewCreateResult,
    InterviewDetail,
    InterviewStatusResponse,
    InterviewSummary,
)
from app.services.interview_service import InterviewService

router = APIRouter(prefix="/interviews", tags=["Interviews"])

ServiceDep = Annotated[InterviewService, Depends(get_interview_service)]


@router.post("", status_code=status.HTTP_201_CREATED, summary="Create an interview")
async def create_interview(
    user: CurrentUser, service: ServiceDep, payload: InterviewCreate
) -> SuccessResponse[InterviewCreateResult]:
    interview = await service.create(user, payload)
    return SuccessResponse(
        message="Interview creation started.",
        data=InterviewCreateResult(interview_id=interview.id, status=interview.status),
    )


@router.get("", summary="List interviews")
async def list_interviews(
    user: CurrentUser,
    service: ServiceDep,
    page: Annotated[int, Query(ge=1)] = 1,
    page_size: Annotated[int, Query(ge=1, le=100)] = 20,
    status_filter: Annotated[str | None, Query(alias="status")] = None,
    difficulty: str | None = None,
    mode: str | None = None,
    sort: str = "-created_at",
) -> SuccessResponse[Page[InterviewSummary]]:
    items, total = await service.list_for_user(
        user,
        page=page,
        page_size=page_size,
        status=status_filter,
        difficulty=difficulty,
        mode=mode,
        sort=sort,
    )
    page_data = Page.create(
        [InterviewSummary.from_model(i) for i in items],
        page=page,
        page_size=page_size,
        total=total,
    )
    return SuccessResponse(message="OK", data=page_data)


@router.get("/{interview_id}", summary="Get interview details")
async def get_interview(
    user: CurrentUser, service: ServiceDep, interview_id: uuid.UUID
) -> SuccessResponse[InterviewDetail]:
    interview = await service.get_owned(user, interview_id)
    return SuccessResponse(message="OK", data=InterviewDetail.from_model(interview))


@router.get("/{interview_id}/status", summary="Get interview status")
async def get_interview_status(
    user: CurrentUser, service: ServiceDep, interview_id: uuid.UUID
) -> SuccessResponse[InterviewStatusResponse]:
    interview = await service.get_owned(user, interview_id)
    return SuccessResponse(
        message="OK", data=InterviewStatusResponse(**service.build_status(interview))
    )


@router.post("/{interview_id}/start", summary="Start interview")
async def start_interview(
    user: CurrentUser, service: ServiceDep, interview_id: uuid.UUID
) -> SuccessResponse[None]:
    await service.start(user, interview_id)
    return SuccessResponse(message="Interview started.", data=None)


@router.post("/{interview_id}/pause", summary="Pause interview")
async def pause_interview(
    user: CurrentUser, service: ServiceDep, interview_id: uuid.UUID
) -> SuccessResponse[None]:
    await service.acknowledge_pause(user, interview_id)
    return SuccessResponse(message="Interview paused.", data=None)


@router.post("/{interview_id}/resume", summary="Resume interview")
async def resume_interview(
    user: CurrentUser, service: ServiceDep, interview_id: uuid.UUID
) -> SuccessResponse[None]:
    await service.acknowledge_pause(user, interview_id)
    return SuccessResponse(message="Interview resumed.", data=None)


@router.post("/{interview_id}/complete", summary="Complete interview")
async def complete_interview(
    user: CurrentUser, service: ServiceDep, interview_id: uuid.UUID
) -> SuccessResponse[None]:
    await service.complete(user, interview_id)
    return SuccessResponse(message="Interview completed.", data=None)


@router.post("/{interview_id}/cancel", summary="Cancel interview")
async def cancel_interview(
    user: CurrentUser, service: ServiceDep, interview_id: uuid.UUID
) -> SuccessResponse[None]:
    await service.cancel(user, interview_id)
    return SuccessResponse(message="Interview cancelled.", data=None)


@router.delete("/{interview_id}", summary="Delete interview")
async def delete_interview(
    user: CurrentUser, service: ServiceDep, interview_id: uuid.UUID
) -> SuccessResponse[None]:
    await service.delete(user, interview_id)
    return SuccessResponse(message="Interview deleted.", data=None)
