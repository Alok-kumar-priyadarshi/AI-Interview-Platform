"""Interview history endpoints — see docs/05-api-design/history.md."""

from __future__ import annotations

import uuid
from typing import Annotated

from fastapi import APIRouter, Depends, Query

from app.dependencies.analytics import get_history_service
from app.dependencies.auth import CurrentUser
from app.schemas.common import Page, SuccessResponse
from app.schemas.history import HistoryDetail, HistoryItem
from app.services.history_service import HistoryService

router = APIRouter(prefix="/history", tags=["History"])

ServiceDep = Annotated[HistoryService, Depends(get_history_service)]


async def _paginated(
    service: HistoryService, user, *, page: int, page_size: int, keyword: str | None
) -> Page[HistoryItem]:
    rows, total = await service.list(user, page=page, page_size=page_size, keyword=keyword)
    return Page.create(
        [HistoryItem.from_row(interview, report) for interview, report in rows],
        page=page,
        page_size=page_size,
        total=total,
    )


@router.get("", summary="Interview history")
async def list_history(
    user: CurrentUser,
    service: ServiceDep,
    page: Annotated[int, Query(ge=1)] = 1,
    page_size: Annotated[int, Query(ge=1, le=100)] = 20,
) -> SuccessResponse[Page[HistoryItem]]:
    data = await _paginated(service, user, page=page, page_size=page_size, keyword=None)
    return SuccessResponse(message="OK", data=data)


@router.get("/search", summary="Search history")
async def search_history(
    user: CurrentUser,
    service: ServiceDep,
    keyword: str | None = None,
    page: Annotated[int, Query(ge=1)] = 1,
    page_size: Annotated[int, Query(ge=1, le=100)] = 20,
) -> SuccessResponse[Page[HistoryItem]]:
    return SuccessResponse(
        message="OK",
        data=await _paginated(service, user, page=page, page_size=page_size, keyword=keyword),
    )


@router.get("/archive", summary="Archived interviews (completed)")
async def archive(
    user: CurrentUser,
    service: ServiceDep,
    page: Annotated[int, Query(ge=1)] = 1,
    page_size: Annotated[int, Query(ge=1, le=100)] = 20,
) -> SuccessResponse[Page[HistoryItem]]:
    data = await _paginated(service, user, page=page, page_size=page_size, keyword=None)
    return SuccessResponse(message="OK", data=data)


@router.get("/{history_id}", summary="History details")
async def get_history(
    user: CurrentUser, service: ServiceDep, history_id: uuid.UUID
) -> SuccessResponse[HistoryDetail]:
    interview, report = await service.get(user, history_id)
    return SuccessResponse(message="OK", data=HistoryDetail.from_row(interview, report))


@router.delete("/{history_id}", summary="Delete history record")
async def delete_history(
    user: CurrentUser, service: ServiceDep, history_id: uuid.UUID
) -> SuccessResponse[None]:
    await service.delete(user, history_id)
    return SuccessResponse(message="History deleted successfully.", data=None)
