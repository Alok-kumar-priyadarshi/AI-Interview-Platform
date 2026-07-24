"""API tests for the authentication and user-management endpoints."""

from __future__ import annotations

from urllib.parse import parse_qs, urlparse

import pytest
from httpx import AsyncClient

from tests.auth_helper import login_tokens as _login

API = "/api/v1"


@pytest.mark.asyncio
async def test_me_requires_authentication(client: AsyncClient) -> None:
    resp = await client.get(f"{API}/auth/me")
    assert resp.status_code == 401
    body = resp.json()
    assert body["success"] is False
    assert body["error"]["code"] == "UNAUTHORIZED"


@pytest.mark.asyncio
async def test_full_login_flow_and_me(client: AsyncClient) -> None:
    tokens = await _login(client, "jane")
    assert int(tokens["expires_in"]) > 0
    assert tokens["refresh_token"]

    resp = await client.get(
        f"{API}/auth/me", headers={"Authorization": f"Bearer {tokens['access_token']}"}
    )
    assert resp.status_code == 200
    data = resp.json()["data"]
    assert data["email"] == "jane@example.com"
    assert data["role"] == "candidate"


@pytest.mark.asyncio
async def test_state_mismatch_rejected(client: AsyncClient) -> None:
    await client.get(f"{API}/auth/google/login", follow_redirects=False)
    resp = await client.get(
        f"{API}/auth/google/callback",
        params={"code": "jane", "state": "not-the-real-state"},
        follow_redirects=False,
    )
    # Failures redirect back to the SPA with an error fragment.
    assert resp.status_code == 302
    fragment = parse_qs(urlparse(resp.headers["location"]).fragment)
    assert fragment["error"] == ["OAUTH_FAILED"]


@pytest.mark.asyncio
async def test_refresh_returns_new_access_token(client: AsyncClient) -> None:
    tokens = await _login(client, "bob")
    resp = await client.post(
        f"{API}/auth/refresh", json={"refresh_token": tokens["refresh_token"]}
    )
    assert resp.status_code == 200
    assert resp.json()["data"]["access_token"]


@pytest.mark.asyncio
async def test_login_is_idempotent_for_same_user(client: AsyncClient) -> None:
    """Logging in twice with the same identity must not create a second user."""
    t1 = await _login(client, "carol")
    r1 = await client.get(
        f"{API}/users/me", headers={"Authorization": f"Bearer {t1['access_token']}"}
    )
    user_id_1 = r1.json()["data"]["id"]

    # Second login with the same identity handle must resolve to the same user.
    t2 = await _login(client, "carol")
    r2 = await client.get(
        f"{API}/users/me", headers={"Authorization": f"Bearer {t2['access_token']}"}
    )
    assert r2.json()["data"]["id"] == user_id_1


@pytest.mark.asyncio
async def test_update_profile(client: AsyncClient) -> None:
    tokens = await _login(client, "dave")
    headers = {"Authorization": f"Bearer {tokens['access_token']}"}
    resp = await client.patch(
        f"{API}/users/me", json={"full_name": "Dave Updated"}, headers=headers
    )
    assert resp.status_code == 200
    assert resp.json()["data"]["full_name"] == "Dave Updated"


@pytest.mark.asyncio
async def test_update_profile_validation(client: AsyncClient) -> None:
    tokens = await _login(client, "erin")
    headers = {"Authorization": f"Bearer {tokens['access_token']}"}
    resp = await client.patch(f"{API}/users/me", json={"full_name": "x"}, headers=headers)
    assert resp.status_code == 422
    assert resp.json()["error"]["code"] == "VALIDATION_ERROR"


@pytest.mark.asyncio
async def test_statistics_empty(client: AsyncClient) -> None:
    tokens = await _login(client, "frank")
    headers = {"Authorization": f"Bearer {tokens['access_token']}"}
    resp = await client.get(f"{API}/users/me/statistics", headers=headers)
    assert resp.status_code == 200
    data = resp.json()["data"]
    assert data["total_interviews"] == 0
    assert data["average_score"] is None


@pytest.mark.asyncio
async def test_delete_account_requires_confirmation(client: AsyncClient) -> None:
    tokens = await _login(client, "grace")
    headers = {"Authorization": f"Bearer {tokens['access_token']}"}
    bad = await client.request(
        "DELETE", f"{API}/users/me", json={"confirm": False}, headers=headers
    )
    assert bad.status_code == 400

    ok = await client.request(
        "DELETE", f"{API}/users/me", json={"confirm": True}, headers=headers
    )
    assert ok.status_code == 200
    # Token now resolves to a deleted user → 401.
    after = await client.get(f"{API}/auth/me", headers=headers)
    assert after.status_code == 401
