"""Resume endpoints — see ``docs/05-api-design/resume.md``."""

from __future__ import annotations

import uuid
from typing import Annotated

from fastapi import APIRouter, Depends, File, UploadFile, status

from app.dependencies.auth import CurrentUser
from app.dependencies.resume import get_resume_service
from app.schemas.common import SuccessResponse
from app.schemas.resume import (
    ResumeDetail,
    ResumeMetadata,
    ResumeStatus,
    ResumeSummary,
    ResumeUploadResult,
)
from app.services.resume_service import ResumeService

router = APIRouter(prefix="/resumes", tags=["Resume"])

ResumeServiceDep = Annotated[ResumeService, Depends(get_resume_service)]


@router.get("", summary="List resumes")
async def list_resumes(
    user: CurrentUser, service: ResumeServiceDep
) -> SuccessResponse[list[ResumeSummary]]:
    resumes = await service.list_for_user(user.id)
    return SuccessResponse(message="OK", data=[ResumeSummary.from_model(r) for r in resumes])


@router.post("", status_code=status.HTTP_201_CREATED, summary="Upload a resume")
async def upload_resume(
    user: CurrentUser,
    service: ResumeServiceDep,
    file: Annotated[UploadFile, File(...)],
) -> SuccessResponse[ResumeUploadResult]:
    data = await file.read()
    resume = await service.upload(
        user,
        filename=file.filename or "resume",
        content_type=file.content_type,
        data=data,
    )
    return SuccessResponse(
        message="Resume uploaded successfully.",
        data=ResumeUploadResult(resume_id=resume.id, status=resume.processing_status),
    )


@router.get("/{resume_id}", summary="Get resume details")
async def get_resume(
    user: CurrentUser, service: ResumeServiceDep, resume_id: uuid.UUID
) -> SuccessResponse[ResumeDetail]:
    resume = await service.get_owned(user, resume_id)
    return SuccessResponse(message="OK", data=ResumeDetail.from_model(resume))


@router.get("/{resume_id}/status", summary="Get resume processing status")
async def get_resume_status(
    user: CurrentUser, service: ResumeServiceDep, resume_id: uuid.UUID
) -> SuccessResponse[ResumeStatus]:
    resume = await service.get_owned(user, resume_id)
    return SuccessResponse(
        message="OK",
        data=ResumeStatus(status=resume.processing_status, progress=service.progress_for(resume)),
    )


@router.get("/{resume_id}/metadata", summary="Get extracted resume metadata")
async def get_resume_metadata(
    user: CurrentUser, service: ResumeServiceDep, resume_id: uuid.UUID
) -> SuccessResponse[ResumeMetadata]:
    profile = await service.get_metadata(user, resume_id)
    return SuccessResponse(message="OK", data=ResumeMetadata.from_model(profile))


@router.patch("/{resume_id}/default", summary="Set default resume")
async def set_default_resume(
    user: CurrentUser, service: ResumeServiceDep, resume_id: uuid.UUID
) -> SuccessResponse[None]:
    await service.set_default(user, resume_id)
    return SuccessResponse(message="Default resume updated.", data=None)


@router.delete("/{resume_id}", summary="Delete resume")
async def delete_resume(
    user: CurrentUser, service: ResumeServiceDep, resume_id: uuid.UUID
) -> SuccessResponse[None]:
    await service.delete(user, resume_id)
    return SuccessResponse(message="Resume deleted successfully.", data=None)
