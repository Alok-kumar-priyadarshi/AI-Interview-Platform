"""Authentication schemas."""

from __future__ import annotations

from pydantic import BaseModel, Field


class TokenPair(BaseModel):
    """Issued on successful login."""

    access_token: str
    refresh_token: str
    token_type: str = "bearer"
    expires_in: int = Field(..., description="Access-token lifetime in seconds.")


class AccessTokenResponse(BaseModel):
    """Issued when refreshing an access token."""

    access_token: str
    token_type: str = "bearer"
    expires_in: int


class RefreshRequest(BaseModel):
    """Refresh-token payload. Optional because the token may arrive via cookie."""

    refresh_token: str | None = None


class GoogleAuthorizationURL(BaseModel):
    authorization_url: str


class GoogleIdentity(BaseModel):
    """Verified identity returned by Google's OAuth token exchange."""

    google_id: str
    email: str
    full_name: str
    picture: str | None = None
    email_verified: bool = False
