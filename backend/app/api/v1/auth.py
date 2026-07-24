"""Authentication endpoints — see ``docs/05-api-design/authentication.md``.

Implements the Google OAuth 2.0 authorization-code flow plus JWT refresh,
logout, and current-user retrieval.
"""

from __future__ import annotations

from typing import Annotated
from urllib.parse import urlencode

from fastapi import APIRouter, Cookie, Depends, Query, Request, Response, status
from fastapi.responses import RedirectResponse

from app.core.config import Settings, get_settings
from app.core.logging import get_logger
from app.dependencies.auth import CurrentUser, get_auth_service
from app.exceptions.base import AppException, AuthenticationError
from app.schemas.auth import AccessTokenResponse, RefreshRequest
from app.schemas.common import SuccessResponse
from app.schemas.user import UserResponse
from app.services.auth_service import AuthService

logger = get_logger(__name__)

router = APIRouter(prefix="/auth", tags=["Authentication"])

_REFRESH_COOKIE = "refresh_token"
AuthServiceDep = Annotated[AuthService, Depends(get_auth_service)]


def _set_cookie(
    response: Response, name: str, value: str, *, settings: Settings, max_age: int
) -> None:
    response.set_cookie(
        key=name,
        value=value,
        max_age=max_age,
        httponly=True,
        secure=settings.COOKIE_SECURE,
        samesite=settings.COOKIE_SAMESITE,
    )


@router.get("/google/login", summary="Start Google OAuth login")
async def google_login(auth_service: AuthServiceDep) -> RedirectResponse:
    """Redirect the browser to Google's consent screen (302)."""
    authorization_url = auth_service.start_login()
    return RedirectResponse(url=authorization_url, status_code=status.HTTP_302_FOUND)


@router.get("/google/callback", summary="Google OAuth callback")
async def google_callback(
    request: Request,
    auth_service: AuthServiceDep,
    settings: Annotated[Settings, Depends(get_settings)],
    code: Annotated[str, Query(...)],
    state: Annotated[str, Query(...)],
) -> RedirectResponse:
    """Complete the OAuth flow and redirect back to the SPA.

    CSRF is protected by a signed ``state`` token (no cookie), so the sign-in
    path has no cross-site cookie/XHR dependency. On success the tokens are
    handed to the SPA via the URL fragment (``#…``) — never sent to servers or
    written to logs; on failure the SPA receives an ``#error=…`` code.
    """
    callback_url = f"{settings.FRONTEND_URL.rstrip('/')}/auth/callback"
    try:
        tokens = await auth_service.complete_login(
            code=code,
            state=state,
            ip_address=request.client.host if request.client else None,
            user_agent=request.headers.get("user-agent"),
        )
    except AppException as exc:
        logger.info("oauth_callback_failed", extra={"error_code": str(exc.error_code)})
        return RedirectResponse(
            url=f"{callback_url}#{urlencode({'error': exc.error_code})}",
            status_code=status.HTTP_302_FOUND,
        )

    fragment = urlencode(
        {
            "access_token": tokens.access_token,
            "refresh_token": tokens.refresh_token,
            "expires_in": tokens.expires_in,
        }
    )
    redirect = RedirectResponse(
        url=f"{callback_url}#{fragment}", status_code=status.HTTP_302_FOUND
    )
    _set_cookie(
        redirect,
        _REFRESH_COOKIE,
        tokens.refresh_token,
        settings=settings,
        max_age=settings.JWT_REFRESH_TOKEN_EXPIRE_DAYS * 86_400,
    )
    return redirect


@router.post("/refresh", summary="Refresh access token")
async def refresh_token(
    auth_service: AuthServiceDep,
    payload: RefreshRequest | None = None,
    refresh_cookie: Annotated[str | None, Cookie(alias=_REFRESH_COOKIE)] = None,
) -> SuccessResponse[AccessTokenResponse]:
    """Issue a new access token from the refresh token (body or cookie)."""
    token = (payload.refresh_token if payload else None) or refresh_cookie
    if not token:
        raise AuthenticationError("Refresh token is required.")
    result = await auth_service.refresh(token)
    return SuccessResponse(message="Token refreshed.", data=result)


@router.post("/logout", summary="Log out")
async def logout(
    request: Request,
    response: Response,
    user: CurrentUser,
    auth_service: AuthServiceDep,
) -> SuccessResponse[None]:
    """Clear the refresh cookie and record the logout event."""
    await auth_service.logout(user, ip_address=request.client.host if request.client else None)
    response.delete_cookie(_REFRESH_COOKIE)
    return SuccessResponse(message="Logged out successfully.", data=None)


@router.get("/me", summary="Current authenticated user")
async def me(user: CurrentUser) -> SuccessResponse[UserResponse]:
    return SuccessResponse(message="OK", data=UserResponse.model_validate(user))
