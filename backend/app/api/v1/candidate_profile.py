"""Candidate profile (preferences) endpoints — see
docs/05-api-design/candidate-profile.md.

Backed by the ``candidate_preferences`` table (user-owned preferences), distinct
from the resume-derived AI profile exposed at ``/resumes/{id}/metadata``.
"""

from __future__ import annotations

from typing import Annotated

from fastapi import APIRouter, Depends, status
from sqlalchemy.ext.asyncio import AsyncSession

from app.database.session import get_db
from app.dependencies.auth import CurrentUser
from app.schemas.candidate_preferences import (
    CandidatePreferencesCreate,
    CandidatePreferencesResponse,
    CandidatePreferencesUpdate,
)
from app.schemas.common import SuccessResponse
from app.services.preferences_service import PreferencesService

router = APIRouter(prefix="/candidate-profile", tags=["Candidate Profile"])


def get_preferences_service(
    db: Annotated[AsyncSession, Depends(get_db)],
) -> PreferencesService:
    return PreferencesService(db)


ServiceDep = Annotated[PreferencesService, Depends(get_preferences_service)]


@router.get("", summary="Get candidate profile")
async def get_profile(
    user: CurrentUser, service: ServiceDep
) -> SuccessResponse[CandidatePreferencesResponse]:
    prefs = await service.get(user)
    return SuccessResponse(message="OK", data=CandidatePreferencesResponse.model_validate(prefs))


@router.post("", status_code=status.HTTP_201_CREATED, summary="Create candidate profile")
async def create_profile(
    user: CurrentUser, service: ServiceDep, payload: CandidatePreferencesCreate
) -> SuccessResponse[CandidatePreferencesResponse]:
    prefs = await service.create(user, payload)
    return SuccessResponse(
        message="Candidate profile created successfully.",
        data=CandidatePreferencesResponse.model_validate(prefs),
    )


@router.patch("", summary="Update candidate profile")
async def update_profile(
    user: CurrentUser, service: ServiceDep, payload: CandidatePreferencesUpdate
) -> SuccessResponse[CandidatePreferencesResponse]:
    prefs = await service.update(user, payload)
    return SuccessResponse(
        message="Candidate profile updated successfully.",
        data=CandidatePreferencesResponse.model_validate(prefs),
    )


@router.delete("", summary="Delete candidate profile")
async def delete_profile(user: CurrentUser, service: ServiceDep) -> SuccessResponse[None]:
    await service.delete(user)
    return SuccessResponse(message="Candidate profile deleted.", data=None)
