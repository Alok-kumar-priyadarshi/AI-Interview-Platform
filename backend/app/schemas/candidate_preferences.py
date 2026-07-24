"""Candidate preferences schemas — see docs/05-api-design/candidate-profile.md."""

from __future__ import annotations

import uuid
from datetime import datetime

from pydantic import BaseModel, ConfigDict, Field, field_validator, model_validator

from app.models.enums import InterviewVoice, PreferredInterviewType, PreferredLanguage

MAX_SKILLS = 100
MAX_SKILL_LENGTH = 50


def _validate_skills(values: list[str]) -> list[str]:
    """Deduplicate case-insensitively and enforce count/length limits."""
    if len(values) > MAX_SKILLS:
        raise ValueError(f"At most {MAX_SKILLS} skills are allowed.")
    seen: dict[str, str] = {}
    for skill in values:
        cleaned = skill.strip()
        if not cleaned:
            continue
        if len(cleaned) > MAX_SKILL_LENGTH:
            raise ValueError(f"Each skill must be at most {MAX_SKILL_LENGTH} characters.")
        seen.setdefault(cleaned.lower(), cleaned)
    return list(seen.values())


class _PreferencesBase(BaseModel):
    experience_years: int | None = Field(default=None, ge=0, le=50)
    current_company: str | None = Field(default=None, max_length=255)
    education: str | None = Field(default=None, max_length=255)
    degree: str | None = Field(default=None, max_length=255)
    university: str | None = Field(default=None, max_length=255)
    graduation_year: int | None = Field(default=None, ge=1900, le=2100)
    skills: list[str] = Field(default_factory=list)
    preferred_domains: list[str] = Field(default_factory=list)
    expected_salary_min: int | None = Field(default=None, ge=0)
    expected_salary_max: int | None = Field(default=None, ge=0)
    preferred_interview_language: PreferredLanguage = PreferredLanguage.EN
    preferred_interviewer_voice: InterviewVoice | None = None
    preferred_interview_type: PreferredInterviewType = PreferredInterviewType.TECHNICAL

    @field_validator("skills")
    @classmethod
    def _skills(cls, value: list[str]) -> list[str]:
        return _validate_skills(value)

    @model_validator(mode="after")
    def _salary_range(self) -> _PreferencesBase:
        if (
            self.expected_salary_min is not None
            and self.expected_salary_max is not None
            and self.expected_salary_max < self.expected_salary_min
        ):
            raise ValueError("expected_salary_max must be >= expected_salary_min.")
        return self


class CandidatePreferencesCreate(_PreferencesBase):
    target_role: str = Field(..., min_length=2, max_length=100)


class CandidatePreferencesUpdate(BaseModel):
    """All fields optional; only provided fields are updated."""

    model_config = ConfigDict(extra="forbid")

    target_role: str | None = Field(default=None, min_length=2, max_length=100)
    experience_years: int | None = Field(default=None, ge=0, le=50)
    current_company: str | None = Field(default=None, max_length=255)
    education: str | None = Field(default=None, max_length=255)
    degree: str | None = Field(default=None, max_length=255)
    university: str | None = Field(default=None, max_length=255)
    graduation_year: int | None = Field(default=None, ge=1900, le=2100)
    skills: list[str] | None = None
    preferred_domains: list[str] | None = None
    expected_salary_min: int | None = Field(default=None, ge=0)
    expected_salary_max: int | None = Field(default=None, ge=0)
    preferred_interview_language: PreferredLanguage | None = None
    preferred_interviewer_voice: InterviewVoice | None = None
    preferred_interview_type: PreferredInterviewType | None = None

    @field_validator("skills")
    @classmethod
    def _skills(cls, value: list[str] | None) -> list[str] | None:
        return _validate_skills(value) if value is not None else None


class CandidatePreferencesResponse(BaseModel):
    model_config = ConfigDict(from_attributes=True)

    id: uuid.UUID
    target_role: str
    experience_years: int | None
    current_company: str | None
    education: str | None
    degree: str | None
    university: str | None
    graduation_year: int | None
    skills: list[str]
    preferred_domains: list[str]
    expected_salary_min: int | None
    expected_salary_max: int | None
    preferred_interview_language: str
    preferred_interviewer_voice: str | None
    preferred_interview_type: str
    created_at: datetime
    updated_at: datetime
