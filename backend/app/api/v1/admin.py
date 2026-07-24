"""Admin endpoints — see docs/05-api-design/admin.md. All require the admin role."""

from __future__ import annotations

import uuid
from typing import Annotated

from fastapi import APIRouter, Depends, Query
from pydantic import BaseModel

from app.dependencies.analytics import get_admin_service
from app.dependencies.auth import AdminUser
from app.dependencies.evaluation import get_evaluation_service
from app.schemas.common import Page, SuccessResponse
from app.services.admin_service import AdminService
from app.services.evaluation_service import EvaluationService

router = APIRouter(prefix="/admin", tags=["Admin"])

ServiceDep = Annotated[AdminService, Depends(get_admin_service)]


class UserStatusUpdate(BaseModel):
    status: str


@router.get("/dashboard", summary="Platform overview")
async def admin_dashboard(admin: AdminUser, service: ServiceDep) -> SuccessResponse[dict]:
    return SuccessResponse(message="OK", data=await service.platform_dashboard())


@router.get("/users", summary="List users")
async def list_users(
    admin: AdminUser,
    service: ServiceDep,
    page: Annotated[int, Query(ge=1)] = 1,
    page_size: Annotated[int, Query(ge=1, le=100)] = 20,
    search: str | None = None,
    role: str | None = None,
    status: str | None = None,
) -> SuccessResponse[Page[dict]]:
    users, total = await service.list_users(
        page=page, page_size=page_size, search=search, role=role, status=status
    )
    items = [
        {
            "id": str(u.id),
            "name": u.full_name,
            "email": u.email,
            "role": u.role,
            "status": "active" if u.is_active else "inactive",
        }
        for u in users
    ]
    return SuccessResponse(
        message="OK", data=Page.create(items, page=page, page_size=page_size, total=total)
    )


@router.get("/users/{user_id}", summary="User details")
async def user_details(
    admin: AdminUser, service: ServiceDep, user_id: uuid.UUID
) -> SuccessResponse[dict]:
    return SuccessResponse(message="OK", data=await service.get_user_details(user_id))


@router.patch("/users/{user_id}/status", summary="Update user status")
async def update_user_status(
    admin: AdminUser, service: ServiceDep, user_id: uuid.UUID, payload: UserStatusUpdate
) -> SuccessResponse[None]:
    await service.update_user_status(user_id, payload.status)
    return SuccessResponse(message="User status updated.", data=None)


@router.get("/interviews", summary="Monitor interviews")
async def monitor_interviews(
    admin: AdminUser,
    service: ServiceDep,
    page: Annotated[int, Query(ge=1)] = 1,
    page_size: Annotated[int, Query(ge=1, le=100)] = 20,
) -> SuccessResponse[Page[dict]]:
    interviews, total = await service.list_interviews(page=page, page_size=page_size)
    items = [
        {
            "id": str(i.id),
            "user_id": str(i.user_id),
            "status": i.status,
            "difficulty": i.difficulty,
            "mode": i.interview_type,
            "target_role": i.target_role,
            "overall_score": float(i.overall_score) if i.overall_score is not None else None,
            "created_at": i.created_at.isoformat(),
        }
        for i in interviews
    ]
    return SuccessResponse(
        message="OK", data=Page.create(items, page=page, page_size=page_size, total=total)
    )


@router.get("/evaluations", summary="Monitor evaluations")
async def monitor_evaluations(admin: AdminUser, service: ServiceDep) -> SuccessResponse[dict]:
    return SuccessResponse(message="OK", data=await service.evaluation_stats())


@router.post("/evaluations/{evaluation_id}/retry", summary="Retry evaluation")
async def retry_evaluation(
    admin: AdminUser,
    evaluation_id: uuid.UUID,
    evaluation_service: Annotated[EvaluationService, Depends(get_evaluation_service)],
) -> SuccessResponse[None]:
    evaluation = await evaluation_service.evaluations.get(evaluation_id)
    if evaluation is not None:
        interview_id = await evaluation_service.evaluations.interview_id_for(evaluation)
        if interview_id is not None:
            interview = await evaluation_service.interviews.get(interview_id)
            if interview is not None:
                await evaluation_service.run_for_interview(interview)
    return SuccessResponse(message="Evaluation queued.", data=None)


@router.get("/reports", summary="Monitor reports")
async def monitor_reports(
    admin: AdminUser,
    service: ServiceDep,
    page: Annotated[int, Query(ge=1)] = 1,
    page_size: Annotated[int, Query(ge=1, le=100)] = 20,
) -> SuccessResponse[Page[dict]]:
    reports, total = await service.list_reports(page=page, page_size=page_size)
    items = [
        {
            "id": str(r.id),
            "interview_id": str(r.interview_id),
            "overall_score": float(r.overall_score),
            "hiring_recommendation": r.hiring_recommendation,
            "generated_at": r.generated_at.isoformat(),
        }
        for r in reports
    ]
    return SuccessResponse(
        message="OK", data=Page.create(items, page=page, page_size=page_size, total=total)
    )


@router.get("/audit-logs", summary="Audit logs")
async def audit_logs(
    admin: AdminUser,
    service: ServiceDep,
    page: Annotated[int, Query(ge=1)] = 1,
    page_size: Annotated[int, Query(ge=1, le=100)] = 20,
) -> SuccessResponse[Page[dict]]:
    logs, total = await service.list_audit_logs(page=page, page_size=page_size)
    items = [
        {
            "id": str(log.id),
            "event_type": log.event_type,
            "action": log.action,
            "severity": log.severity,
            "user_id": str(log.user_id) if log.user_id else None,
            "occurred_at": log.occurred_at.isoformat(),
        }
        for log in logs
    ]
    return SuccessResponse(
        message="OK", data=Page.create(items, page=page, page_size=page_size, total=total)
    )
