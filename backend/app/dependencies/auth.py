"""Authentication & authorization dependencies.

Provides the DI wiring for the auth stack and the ``get_current_user`` guard
used by every protected endpoint. Resolving the user here (not in each handler)
keeps route functions thin and enforces the documented validation pipeline:
extract → verify signature → verify expiry → load user → authorize.
"""

from __future__ import annotations

import uuid
from typing import Annotated

from fastapi import Depends
from fastapi.security import HTTPAuthorizationCredentials, HTTPBearer
from sqlalchemy.ext.asyncio import AsyncSession

from app.auth.oauth import GoogleOAuthClient, OAuthProvider
from app.core.config import Settings, get_settings
from app.core.context import user_id_ctx
from app.core.security import decode_token
from app.database.session import get_db
from app.exceptions.base import AdminRequiredError, AuthenticationError
from app.models.enums import UserRole
from app.models.user import User
from app.repositories.user_repository import UserRepository
from app.services.auth_service import AuthService
from app.services.user_service import UserService

# auto_error=False so we can emit the standard error envelope instead of
# FastAPI's default {"detail": ...} on a missing/invalid Authorization header.
_bearer = HTTPBearer(auto_error=False, description="JWT access token")

DbSession = Annotated[AsyncSession, Depends(get_db)]
SettingsDep = Annotated[Settings, Depends(get_settings)]


def get_oauth_provider(settings: SettingsDep) -> OAuthProvider:
    return GoogleOAuthClient(settings)


def get_user_service(db: DbSession) -> UserService:
    return UserService(db)


def get_auth_service(
    db: DbSession,
    provider: Annotated[OAuthProvider, Depends(get_oauth_provider)],
) -> AuthService:
    return AuthService(db, provider)


async def get_current_user(
    db: DbSession,
    credentials: Annotated[HTTPAuthorizationCredentials | None, Depends(_bearer)],
) -> User:
    """Resolve and return the authenticated, active user or raise 401."""
    if credentials is None or not credentials.credentials:
        raise AuthenticationError()

    payload = decode_token(credentials.credentials, expected_type="access")
    # A valid token whose subject no longer exists (or is inactive) is an
    # authentication failure (401), not a resource-not-found (404).
    user = await UserRepository(db).get(uuid.UUID(payload["sub"]))
    if user is None or not user.is_active:
        raise AuthenticationError()

    # Bind the user to the logging context for correlated request logs.
    user_id_ctx.set(str(user.id))
    return user


CurrentUser = Annotated[User, Depends(get_current_user)]


async def require_admin(user: CurrentUser) -> User:
    """Authorization guard for admin-only endpoints."""
    if user.role != UserRole.ADMIN:
        raise AdminRequiredError()
    return user


AdminUser = Annotated[User, Depends(require_admin)]
