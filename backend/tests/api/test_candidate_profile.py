"""API tests for the candidate profile (preferences) endpoints."""

from __future__ import annotations

import pytest
from httpx import AsyncClient

from tests.auth_helper import login_headers

API = "/api/v1"

_login = login_headers  # OAuth flow → Authorization header

VALID_PROFILE = {
    "target_role": "Backend Developer",
    "experience_years": 2,
    "degree": "B.Tech",
    "university": "AKTU",
    "graduation_year": 2027,
    "skills": ["Python", "FastAPI", "python"],  # duplicate (case-insensitive)
    "preferred_domains": ["Backend", "AI"],
    "expected_salary_min": 600000,
    "expected_salary_max": 1200000,
    "preferred_interview_language": "en",
    "preferred_interviewer_voice": "female",
    "preferred_interview_type": "technical",
}




@pytest.mark.asyncio
async def test_get_before_create_returns_404(client: AsyncClient) -> None:
    headers = await _login(client)
    resp = await client.get(f"{API}/candidate-profile", headers=headers)
    assert resp.status_code == 404
    assert resp.json()["error"]["code"] == "PROFILE_NOT_FOUND"


@pytest.mark.asyncio
async def test_create_and_get_profile(client: AsyncClient) -> None:
    headers = await _login(client)
    created = await client.post(f"{API}/candidate-profile", json=VALID_PROFILE, headers=headers)
    assert created.status_code == 201, created.text
    data = created.json()["data"]
    # Case-insensitive de-duplication of skills.
    assert data["skills"] == ["Python", "FastAPI"]
    assert data["target_role"] == "Backend Developer"

    fetched = await client.get(f"{API}/candidate-profile", headers=headers)
    assert fetched.status_code == 200
    assert fetched.json()["data"]["expected_salary_max"] == 1200000


@pytest.mark.asyncio
async def test_create_twice_conflicts(client: AsyncClient) -> None:
    headers = await _login(client)
    await client.post(f"{API}/candidate-profile", json=VALID_PROFILE, headers=headers)
    dup = await client.post(f"{API}/candidate-profile", json=VALID_PROFILE, headers=headers)
    assert dup.status_code == 409
    assert dup.json()["error"]["code"] == "PROFILE_EXISTS"


@pytest.mark.asyncio
async def test_salary_range_validation_on_create(client: AsyncClient) -> None:
    headers = await _login(client)
    bad = {**VALID_PROFILE, "expected_salary_min": 900000, "expected_salary_max": 500000}
    resp = await client.post(f"{API}/candidate-profile", json=bad, headers=headers)
    assert resp.status_code == 422
    assert resp.json()["error"]["code"] == "VALIDATION_ERROR"


@pytest.mark.asyncio
async def test_target_role_too_short(client: AsyncClient) -> None:
    headers = await _login(client)
    resp = await client.post(
        f"{API}/candidate-profile", json={**VALID_PROFILE, "target_role": "x"}, headers=headers
    )
    assert resp.status_code == 422


@pytest.mark.asyncio
async def test_update_profile(client: AsyncClient) -> None:
    headers = await _login(client)
    await client.post(f"{API}/candidate-profile", json=VALID_PROFILE, headers=headers)
    resp = await client.patch(
        f"{API}/candidate-profile",
        json={"experience_years": 3, "skills": ["Go", "Docker"]},
        headers=headers,
    )
    assert resp.status_code == 200
    data = resp.json()["data"]
    assert data["experience_years"] == 3
    assert data["skills"] == ["Go", "Docker"]


@pytest.mark.asyncio
async def test_update_salary_range_merged_validation(client: AsyncClient) -> None:
    headers = await _login(client)
    await client.post(f"{API}/candidate-profile", json=VALID_PROFILE, headers=headers)
    # Existing min is 600000; lowering max below it must fail.
    resp = await client.patch(
        f"{API}/candidate-profile", json={"expected_salary_max": 300000}, headers=headers
    )
    assert resp.status_code == 422


@pytest.mark.asyncio
async def test_delete_profile(client: AsyncClient) -> None:
    headers = await _login(client)
    await client.post(f"{API}/candidate-profile", json=VALID_PROFILE, headers=headers)
    deleted = await client.delete(f"{API}/candidate-profile", headers=headers)
    assert deleted.status_code == 200
    gone = await client.get(f"{API}/candidate-profile", headers=headers)
    assert gone.status_code == 404
