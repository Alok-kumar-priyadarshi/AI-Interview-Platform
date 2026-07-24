"""User management endpoints — see ``docs/05-api-design/users.md``.

Implements the endpoints supported by the Version 1 schema. The
``/users/me/preferences`` endpoints from the spec are intentionally deferred:
the ``users`` table has no preferences columns in Version 1 (the users entity
doc lists them under *Future Enhancements*), so adding them requires a
schema/migration change tracked separately.
"""

from __future__ import annotations

from typing import Annotated

from fastapi import APIRouter, Depends, status

from app.core.error_codes import ErrorCode
from app.dependencies.auth import CurrentUser, get_user_service
from app.exceptions.base import AppException
from app.schemas.common import SuccessResponse
from app.schemas.user import (
    AccountDeleteRequest,
    UserResponse,
    UserStatistics,
    UserUpdateRequest,
)
from app.services.user_service import UserService

router = APIRouter(prefix="/users", tags=["Users"])

UserServiceDep = Annotated[UserService, Depends(get_user_service)]


@router.get("/me", summary="Get current user profile")
async def get_me(user: CurrentUser) -> SuccessResponse[UserResponse]:
    return SuccessResponse(message="OK", data=UserResponse.model_validate(user))


@router.patch("/me", summary="Update current user profile")
async def update_me(
    user: CurrentUser,
    payload: UserUpdateRequest,
    user_service: UserServiceDep,
) -> SuccessResponse[UserResponse]:
    updated = await user_service.update_profile(user, full_name=payload.full_name)
    return SuccessResponse(
        message="Profile updated successfully.", data=UserResponse.model_validate(updated)
    )


@router.get("/me/statistics", summary="Get current user statistics")
async def get_my_statistics(
    user: CurrentUser,
    user_service: UserServiceDep,
) -> SuccessResponse[UserStatistics]:
    stats = await user_service.get_statistics(user.id)
    return SuccessResponse(message="OK", data=stats)


@router.delete("/me", summary="Delete current user account")
async def delete_me(
    user: CurrentUser,
    payload: AccountDeleteRequest,
    user_service: UserServiceDep,
) -> SuccessResponse[None]:
    if not payload.confirm:
        raise AppException(
            "Account deletion must be confirmed.",
            error_code=ErrorCode.VALIDATION_ERROR,
            status_code=status.HTTP_400_BAD_REQUEST,
        )
    await user_service.delete_account(user)
    return SuccessResponse(message="Account deleted successfully.", data=None)
