"""Authentication service.

Orchestrates the Google OAuth login flow and JWT issuance/refresh. Depends on the
:class:`~app.auth.oauth.OAuthProvider` protocol rather than a concrete provider.
"""

from __future__ import annotations

import uuid

from sqlalchemy.ext.asyncio import AsyncSession

from app.auth.oauth import OAuthProvider
from app.core.logging import get_logger
from app.core.security import (
    access_token_ttl_seconds,
    create_access_token,
    create_refresh_token,
    create_state_token,
    decode_token,
    verify_state_token,
)
from app.exceptions.base import AuthenticationError, OAuthError
from app.models.enums import AuditEventType, AuditSeverity
from app.models.user import User
from app.schemas.auth import AccessTokenResponse, TokenPair
from app.services.audit_service import AuditService
from app.services.user_service import UserService

logger = get_logger(__name__)


class AuthService:
    def __init__(self, session: AsyncSession, oauth_provider: OAuthProvider) -> None:
        self.session = session
        self.oauth = oauth_provider
        self.users = UserService(session)
        self.audit = AuditService(session)

    # ------------------------------------------------------------------ #
    # OAuth login                                                        #
    # ------------------------------------------------------------------ #
    def start_login(self) -> str:
        """Return the Google authorization URL, embedding a signed state token.

        The state is a short-lived signed JWT (not a cookie), so CSRF protection
        survives the cross-site OAuth redirect chain reliably.
        """
        state = create_state_token()
        return self.oauth.build_authorization_url(state=state)

    async def complete_login(
        self,
        *,
        code: str,
        state: str,
        ip_address: str | None = None,
        user_agent: str | None = None,
    ) -> TokenPair:
        """Complete the OAuth callback: validate state, exchange code, issue tokens."""
        if not verify_state_token(state):
            await self.audit.log(
                event_type=AuditEventType.AUTHENTICATION,
                action="LOGIN_FAILED",
                severity=AuditSeverity.WARNING,
                description="Invalid or expired OAuth state.",
                ip_address=ip_address,
                user_agent=user_agent,
            )
            raise OAuthError("Invalid or expired OAuth state.")

        identity = await self.oauth.exchange_code(code=code)
        user, created = await self.users.get_or_create_from_google(identity)

        await self.audit.log(
            event_type=AuditEventType.AUTHENTICATION,
            action="LOGIN_SUCCESS",
            user_id=user.id,
            description="New account created." if created else "Returning user login.",
            ip_address=ip_address,
            user_agent=user_agent,
        )
        return self._issue_token_pair(user)

    # ------------------------------------------------------------------ #
    # Token refresh                                                      #
    # ------------------------------------------------------------------ #
    async def refresh(self, refresh_token: str) -> AccessTokenResponse:
        """Issue a new access token from a valid refresh token."""
        payload = decode_token(refresh_token, expected_type="refresh")
        user = await self.users.get_by_id(uuid.UUID(payload["sub"]))
        if not user.is_active:
            raise AuthenticationError("Account is inactive.")

        access_token = create_access_token(
            user_id=str(user.id), email=user.email, role=user.role
        )
        return AccessTokenResponse(
            access_token=access_token, expires_in=access_token_ttl_seconds()
        )

    async def logout(self, user: User, *, ip_address: str | None = None) -> None:
        await self.audit.log(
            event_type=AuditEventType.AUTHENTICATION,
            action="LOGOUT",
            user_id=user.id,
            ip_address=ip_address,
        )

    # ------------------------------------------------------------------ #
    # Helpers                                                            #
    # ------------------------------------------------------------------ #
    def _issue_token_pair(self, user: User) -> TokenPair:
        return TokenPair(
            access_token=create_access_token(
                user_id=str(user.id), email=user.email, role=user.role
            ),
            refresh_token=create_refresh_token(user_id=str(user.id)),
            expires_in=access_token_ttl_seconds(),
        )
