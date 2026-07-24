"""Evaluation endpoints — see docs/05-api-design/evaluations.md."""

from __future__ import annotations

import uuid
from typing import Annotated

from fastapi import APIRouter, Depends

from app.dependencies.auth import AdminUser, CurrentUser
from app.dependencies.evaluation import get_evaluation_service
from app.schemas.common import SuccessResponse
from app.schemas.evaluation import EvaluationResponse, InterviewEvaluation, StatusProgress
from app.services.evaluation_service import EvaluationService

router = APIRouter(tags=["Evaluations"])

ServiceDep = Annotated[EvaluationService, Depends(get_evaluation_service)]


@router.get("/evaluations/{evaluation_id}", summary="Get evaluation")
async def get_evaluation(
    user: CurrentUser, service: ServiceDep, evaluation_id: uuid.UUID
) -> SuccessResponse[EvaluationResponse]:
    evaluation = await service.get_evaluation(user, evaluation_id)
    return SuccessResponse(message="OK", data=EvaluationResponse.from_model(evaluation))


@router.get("/evaluations/{evaluation_id}/status", summary="Get evaluation status")
async def get_evaluation_status(
    user: CurrentUser, service: ServiceDep, evaluation_id: uuid.UUID
) -> SuccessResponse[StatusProgress]:
    await service.get_evaluation(user, evaluation_id)
    return SuccessResponse(message="OK", data=StatusProgress(status="completed", progress=100))


@router.get("/interviews/{interview_id}/evaluation", summary="Get interview evaluation")
async def get_interview_evaluation(
    user: CurrentUser, service: ServiceDep, interview_id: uuid.UUID
) -> SuccessResponse[InterviewEvaluation]:
    report = await service.get_interview_evaluation(user, interview_id)
    return SuccessResponse(message="OK", data=InterviewEvaluation.from_report(report))


@router.post("/evaluations/{evaluation_id}/retry", summary="Retry evaluation (admin)")
async def retry_evaluation(
    admin: AdminUser, service: ServiceDep, evaluation_id: uuid.UUID
) -> SuccessResponse[None]:
    # Re-runs the pipeline for the owning interview (idempotent if a report exists).
    evaluation = await service.evaluations.get(evaluation_id)
    if evaluation is not None:
        interview_id = await service.evaluations.interview_id_for(evaluation)
        if interview_id is not None:
            interview = await service.interviews.get(interview_id)
            if interview is not None:
                await service.run_for_interview(interview)
    return SuccessResponse(message="Evaluation queued for retry.", data=None)
