"""Resume schemas."""

from __future__ import annotations

import uuid
from datetime import datetime
from typing import Any

from pydantic import BaseModel, ConfigDict


class ResumeSummary(BaseModel):
    """Compact resume representation for list responses."""

    model_config = ConfigDict(from_attributes=True)

    id: uuid.UUID
    file_name: str
    status: str
    uploaded_at: datetime
    is_default: bool

    @classmethod
    def from_model(cls, resume: Any) -> ResumeSummary:
        return cls(
            id=resume.id,
            file_name=resume.original_filename,
            status=resume.processing_status,
            uploaded_at=resume.created_at,
            is_default=resume.is_default,
        )


class ResumeDetail(BaseModel):
    id: uuid.UUID
    file_name: str
    file_size: int
    mime_type: str
    status: str
    uploaded_at: datetime
    is_default: bool

    @classmethod
    def from_model(cls, resume: Any) -> ResumeDetail:
        return cls(
            id=resume.id,
            file_name=resume.original_filename,
            file_size=resume.file_size_bytes,
            mime_type=resume.mime_type,
            status=resume.processing_status,
            uploaded_at=resume.created_at,
            is_default=resume.is_default,
        )


class ResumeUploadResult(BaseModel):
    resume_id: uuid.UUID
    status: str


class ResumeStatus(BaseModel):
    status: str
    progress: int


class ResumeMetadata(BaseModel):
    """Structured, AI-extracted candidate information for a resume."""

    professional_summary: str | None = None
    total_experience_years: float | None = None
    highest_education: str | None = None
    current_job_title: str | None = None
    current_company: str | None = None
    skills: list[dict] = []
    education: list[dict] = []
    experience: list[dict] = []
    projects: list[dict] = []
    certifications: list[dict] = []
    languages: list[str] = []
    ai_confidence_score: float | None = None

    @classmethod
    def from_model(cls, profile: Any) -> ResumeMetadata:
        return cls(
            professional_summary=profile.professional_summary,
            total_experience_years=(
                float(profile.total_experience_years)
                if profile.total_experience_years is not None
                else None
            ),
            highest_education=profile.highest_education,
            current_job_title=profile.current_job_title,
            current_company=profile.current_company,
            skills=profile.skills or [],
            education=profile.education or [],
            experience=profile.experience or [],
            projects=profile.projects or [],
            certifications=profile.certifications or [],
            languages=profile.languages or [],
            ai_confidence_score=(
                float(profile.ai_confidence_score)
                if profile.ai_confidence_score is not None
                else None
            ),
        )
