"""Dashboard endpoints — see docs/05-api-design/dashboard.md (read-only analytics)."""

from __future__ import annotations

from typing import Annotated

from fastapi import APIRouter, Depends, Query

from app.dependencies.analytics import get_dashboard_service
from app.dependencies.auth import CurrentUser
from app.schemas.common import SuccessResponse
from app.services.dashboard_service import DashboardService

router = APIRouter(prefix="/dashboard", tags=["Dashboard"])

ServiceDep = Annotated[DashboardService, Depends(get_dashboard_service)]


@router.get("", summary="Dashboard overview")
async def dashboard(user: CurrentUser, service: ServiceDep) -> SuccessResponse[dict]:
    return SuccessResponse(message="OK", data=await service.overview(user.id))


@router.get("/statistics", summary="Interview statistics")
async def statistics(user: CurrentUser, service: ServiceDep) -> SuccessResponse[dict]:
    return SuccessResponse(message="OK", data=await service.statistics(user.id))


@router.get("/trends", summary="Score trends")
async def trends(
    user: CurrentUser,
    service: ServiceDep,
    limit: Annotated[int, Query(ge=1, le=365)] = 30,
) -> SuccessResponse[list[dict]]:
    return SuccessResponse(message="OK", data=await service.trends(user.id, limit=limit))


@router.get("/recent", summary="Recent interviews")
async def recent(user: CurrentUser, service: ServiceDep) -> SuccessResponse[list[dict]]:
    return SuccessResponse(message="OK", data=await service.recent(user.id))


@router.get("/recommendations", summary="AI recommendations")
async def recommendations(user: CurrentUser, service: ServiceDep) -> SuccessResponse[list[dict]]:
    return SuccessResponse(message="OK", data=await service.recommendations(user.id))


@router.get("/achievements", summary="Achievements")
async def achievements(user: CurrentUser, service: ServiceDep) -> SuccessResponse[list[dict]]:
    return SuccessResponse(message="OK", data=await service.achievements(user.id))
