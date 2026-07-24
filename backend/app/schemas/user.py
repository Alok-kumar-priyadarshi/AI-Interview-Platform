"""User schemas."""

from __future__ import annotations

import uuid
from datetime import datetime

from pydantic import BaseModel, ConfigDict, EmailStr, Field, field_validator


class UserResponse(BaseModel):
    """Public representation of a user (safe to return to the owner)."""

    model_config = ConfigDict(from_attributes=True)

    id: uuid.UUID
    email: EmailStr
    full_name: str
    profile_picture_url: str | None = None
    role: str
    is_active: bool
    last_login_at: datetime | None = None
    created_at: datetime


class UserUpdateRequest(BaseModel):
    """Editable profile fields. Email is immutable (managed by Google OAuth)."""

    full_name: str = Field(..., min_length=2, max_length=100)

    @field_validator("full_name")
    @classmethod
    def _strip(cls, value: str) -> str:
        stripped = value.strip()
        if len(stripped) < 2:
            raise ValueError("full_name must be at least 2 characters.")
        return stripped


class UserStatistics(BaseModel):
    total_interviews: int
    completed_interviews: int
    average_score: float | None
    highest_score: float | None
    reports_generated: int
    resume_count: int


class AccountDeleteRequest(BaseModel):
    confirm: bool = Field(..., description="Must be true to confirm account deletion.")
