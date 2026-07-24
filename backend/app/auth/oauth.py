"""OAuth provider abstraction and Google implementation.

The auth service depends on the :class:`OAuthProvider` protocol, not on Google
directly, so additional providers can be added later without touching business
logic (see authentication-architecture.md — "Provider independent").
"""

from __future__ import annotations

import asyncio
from typing import Any, Protocol
from urllib.parse import urlencode

import httpx

from app.core.config import Settings
from app.core.logging import get_logger
from app.exceptions.base import OAuthError
from app.schemas.auth import GoogleIdentity

logger = get_logger(__name__)

GOOGLE_AUTH_URI = "https://accounts.google.com/o/oauth2/v2/auth"
GOOGLE_TOKEN_URI = "https://oauth2.googleapis.com/token"
GOOGLE_SCOPES = "openid email profile"


class OAuthProvider(Protocol):
    """A pluggable OAuth 2.0 identity provider."""

    def build_authorization_url(self, *, state: str) -> str: ...

    async def exchange_code(self, *, code: str) -> GoogleIdentity: ...


class GoogleOAuthClient:
    """Google OAuth 2.0 client (authorization-code flow)."""

    def __init__(self, settings: Settings) -> None:
        self._client_id = settings.GOOGLE_CLIENT_ID
        self._client_secret = settings.GOOGLE_CLIENT_SECRET
        self._redirect_uri = settings.GOOGLE_REDIRECT_URI
        self._timeout = 10.0

    def build_authorization_url(self, *, state: str) -> str:
        params = {
            "client_id": self._client_id,
            "redirect_uri": self._redirect_uri,
            "response_type": "code",
            "scope": GOOGLE_SCOPES,
            "state": state,
            "access_type": "offline",
            "include_granted_scopes": "true",
            "prompt": "select_account",
        }
        return f"{GOOGLE_AUTH_URI}?{urlencode(params)}"

    async def exchange_code(self, *, code: str) -> GoogleIdentity:
        """Exchange an authorization code for a verified Google identity."""
        token_payload = await self._request_tokens(code)
        id_token_str = token_payload.get("id_token")
        if not id_token_str:
            raise OAuthError("Google token response did not include an ID token.")

        claims = await asyncio.to_thread(self._verify_id_token, id_token_str)
        return GoogleIdentity(
            google_id=claims["sub"],
            email=claims["email"],
            full_name=claims.get("name") or claims["email"].split("@")[0],
            picture=claims.get("picture"),
            email_verified=bool(claims.get("email_verified", False)),
        )

    async def _request_tokens(self, code: str) -> dict[str, Any]:
        data = {
            "code": code,
            "client_id": self._client_id,
            "client_secret": self._client_secret,
            "redirect_uri": self._redirect_uri,
            "grant_type": "authorization_code",
        }
        try:
            async with httpx.AsyncClient(timeout=self._timeout) as client:
                response = await client.post(GOOGLE_TOKEN_URI, data=data)
        except httpx.HTTPError as exc:
            logger.warning("google_token_exchange_failed", extra={"error": str(exc)})
            raise OAuthError("Failed to reach Google for token exchange.") from exc

        if response.status_code != httpx.codes.OK:
            logger.warning("google_token_exchange_rejected", extra={"status": response.status_code})
            raise OAuthError("Google rejected the authorization code.")
        return response.json()

    def _verify_id_token(self, id_token_str: str) -> dict[str, Any]:
        """Verify the ID token's signature, audience, and expiry (blocking)."""
        # Imported lazily so the module loads without network/credentials at import time.
        from google.auth.transport import requests as google_requests
        from google.oauth2 import id_token as google_id_token

        try:
            claims: dict[str, Any] = google_id_token.verify_oauth2_token(
                id_token_str, google_requests.Request(), self._client_id
            )
        except ValueError as exc:
            raise OAuthError("Google ID token verification failed.") from exc

        if not claims.get("email"):
            raise OAuthError("Google ID token did not contain an email address.")
        return claims
