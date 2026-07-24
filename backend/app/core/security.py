"""JWT security primitives.

Pure, side-effect-free helpers for issuing and verifying the platform's JWTs.
Two token types are used (see ``docs/05-api-design/authentication.md``):

* **access**  — short-lived (15 min), carries ``sub`` / ``email`` / ``role``.
* **refresh** — long-lived (30 days), carries ``sub`` and a unique ``jti``.

Signing uses HS256 with ``JWT_SECRET_KEY``. These functions never touch the
database — user resolution happens in the dependency/service layer.
"""

from __future__ import annotations

import uuid
from datetime import UTC, datetime, timedelta
from typing import Any, Literal

from jose import JWTError, jwt

from app.core.config import get_settings
from app.exceptions.base import InvalidTokenError, TokenExpiredError

TokenType = Literal["access", "refresh"]


def _now() -> datetime:
    return datetime.now(UTC)


def create_access_token(*, user_id: str, email: str, role: str) -> str:
    """Return a signed short-lived access token."""
    settings = get_settings()
    issued = _now()
    expires = issued + timedelta(minutes=settings.JWT_ACCESS_TOKEN_EXPIRE_MINUTES)
    claims = {
        "sub": user_id,
        "email": email,
        "role": role,
        "type": "access",
        "iat": issued,
        "exp": expires,
    }
    return jwt.encode(claims, settings.JWT_SECRET_KEY, algorithm=settings.JWT_ALGORITHM)


def create_refresh_token(*, user_id: str) -> str:
    """Return a signed long-lived refresh token with a unique ``jti``."""
    settings = get_settings()
    issued = _now()
    expires = issued + timedelta(days=settings.JWT_REFRESH_TOKEN_EXPIRE_DAYS)
    claims = {
        "sub": user_id,
        "type": "refresh",
        "jti": uuid.uuid4().hex,
        "iat": issued,
        "exp": expires,
    }
    return jwt.encode(claims, settings.JWT_SECRET_KEY, algorithm=settings.JWT_ALGORITHM)


def access_token_ttl_seconds() -> int:
    """Access-token lifetime in seconds (the API's ``expires_in``)."""
    return get_settings().JWT_ACCESS_TOKEN_EXPIRE_MINUTES * 60


def create_state_token() -> str:
    """Return a short-lived, signed OAuth ``state`` token.

    The state is self-contained (signed with the server secret), so CSRF
    protection does not depend on a browser cookie surviving the OAuth redirect
    chain — which is fragile on ``http://localhost`` and across sites.
    """
    settings = get_settings()
    issued = _now()
    claims = {
        "type": "oauth_state",
        "nonce": uuid.uuid4().hex,
        "iat": issued,
        "exp": issued + timedelta(minutes=10),
    }
    return jwt.encode(claims, settings.JWT_SECRET_KEY, algorithm=settings.JWT_ALGORITHM)


def verify_state_token(token: str | None) -> bool:
    """Return ``True`` iff ``token`` is a valid, unexpired OAuth state token."""
    if not token:
        return False
    settings = get_settings()
    try:
        payload = jwt.decode(token, settings.JWT_SECRET_KEY, algorithms=[settings.JWT_ALGORITHM])
    except JWTError:
        return False
    return payload.get("type") == "oauth_state"


def decode_token(token: str, *, expected_type: TokenType) -> dict[str, Any]:
    """Decode and validate a token, enforcing signature, expiry, and type.

    Raises :class:`TokenExpiredError` if expired and :class:`InvalidTokenError`
    for any other validation failure (bad signature, wrong type, malformed).
    """
    settings = get_settings()
    try:
        payload: dict[str, Any] = jwt.decode(
            token, settings.JWT_SECRET_KEY, algorithms=[settings.JWT_ALGORITHM]
        )
    except jwt.ExpiredSignatureError as exc:  # type: ignore[attr-defined]
        raise TokenExpiredError() from exc
    except JWTError as exc:
        raise InvalidTokenError() from exc

    if payload.get("type") != expected_type:
        raise InvalidTokenError(f"Expected a {expected_type} token.")
    if not payload.get("sub"):
        raise InvalidTokenError("Token is missing the subject claim.")
    return payload
