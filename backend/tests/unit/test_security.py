"""Unit tests for JWT security primitives."""

from __future__ import annotations

import uuid

import pytest
from jose import jwt

from app.core.config import get_settings
from app.core.security import (
    access_token_ttl_seconds,
    create_access_token,
    create_refresh_token,
    decode_token,
)
from app.exceptions.base import InvalidTokenError, TokenExpiredError


def test_access_token_roundtrip() -> None:
    uid = str(uuid.uuid4())
    token = create_access_token(user_id=uid, email="a@b.com", role="candidate")
    payload = decode_token(token, expected_type="access")
    assert payload["sub"] == uid
    assert payload["email"] == "a@b.com"
    assert payload["role"] == "candidate"
    assert payload["type"] == "access"


def test_refresh_token_roundtrip_has_unique_jti() -> None:
    uid = str(uuid.uuid4())
    t1 = create_refresh_token(user_id=uid)
    t2 = create_refresh_token(user_id=uid)
    p1 = decode_token(t1, expected_type="refresh")
    p2 = decode_token(t2, expected_type="refresh")
    assert p1["jti"] != p2["jti"]


def test_type_mismatch_rejected() -> None:
    token = create_access_token(user_id="x", email="a@b.com", role="candidate")
    with pytest.raises(InvalidTokenError):
        decode_token(token, expected_type="refresh")


def test_bad_signature_rejected() -> None:
    forged = jwt.encode({"sub": "x", "type": "access"}, "wrong-secret", algorithm="HS256")
    with pytest.raises(InvalidTokenError):
        decode_token(forged, expected_type="access")


def test_expired_token_rejected() -> None:
    settings = get_settings()
    # Manually craft an already-expired access token.
    expired = jwt.encode(
        {"sub": "x", "type": "access", "exp": 0},
        settings.JWT_SECRET_KEY,
        algorithm=settings.JWT_ALGORITHM,
    )
    with pytest.raises(TokenExpiredError):
        decode_token(expired, expected_type="access")


def test_ttl_matches_settings() -> None:
    assert access_token_ttl_seconds() == get_settings().JWT_ACCESS_TOKEN_EXPIRE_MINUTES * 60
