"""API tests for history, dashboard, and admin endpoints."""

from __future__ import annotations

import uuid

import pytest
from httpx import AsyncClient
from sqlalchemy import update
from sqlalchemy.ext.asyncio import AsyncSession

from app.models.enums import UserRole
from app.models.user import User
from tests.auth_helper import login_headers

API = "/api/v1"

_login = login_headers  # OAuth flow → Authorization header
RESUME_TEXT = b"Jane Candidate\nBackend Developer\nSkills: Python, FastAPI\n"




async def _run_full_interview(client: AsyncClient, headers: dict, count: int = 5) -> str:
    up = await client.post(
        f"{API}/resumes", files={"file": ("r.txt", RESUME_TEXT, "text/plain")}, headers=headers
    )
    resume_id = up.json()["data"]["resume_id"]
    created = await client.post(
        f"{API}/interviews",
        json={
            "resume_id": resume_id,
            "interview_type": "technical",
            "difficulty": "medium",
            "mode": "text",
            "language": "en",
            "question_count": count,
        },
        headers=headers,
    )
    interview_id = created.json()["data"]["interview_id"]
    await client.post(f"{API}/interviews/{interview_id}/start", headers=headers)
    for _ in range(count):
        q = (
            await client.get(f"{API}/interviews/{interview_id}/questions/current", headers=headers)
        ).json()["data"]
        await client.post(
            f"{API}/interviews/{interview_id}/answers",
            json={"question_id": q["question_id"], "answer": "A thorough answer."},
            headers=headers,
        )
    await client.post(f"{API}/interviews/{interview_id}/complete", headers=headers)
    return interview_id


# --------------------------------------------------------------------------- #
# History                                                                     #
# --------------------------------------------------------------------------- #
@pytest.mark.asyncio
async def test_history_lists_completed_interviews(client: AsyncClient) -> None:
    headers = await _login(client)
    interview_id = await _run_full_interview(client, headers)
    listing = await client.get(f"{API}/history", headers=headers)
    body = listing.json()["data"]
    assert body["total"] == 1
    item = body["items"][0]
    assert item["interview_id"] == interview_id
    assert item["grade"] == "A"

    detail = await client.get(f"{API}/history/{interview_id}", headers=headers)
    assert detail.status_code == 200
    assert detail.json()["data"]["report_id"] is not None


@pytest.mark.asyncio
async def test_history_search_by_keyword(client: AsyncClient) -> None:
    headers = await _login(client)
    await _run_full_interview(client, headers)
    hit = await client.get(f"{API}/history/search?keyword=software", headers=headers)
    assert hit.json()["data"]["total"] == 1
    miss = await client.get(f"{API}/history/search?keyword=zzznope", headers=headers)
    assert miss.json()["data"]["total"] == 0


# --------------------------------------------------------------------------- #
# Dashboard                                                                   #
# --------------------------------------------------------------------------- #
@pytest.mark.asyncio
async def test_dashboard_overview_and_stats(client: AsyncClient) -> None:
    headers = await _login(client)
    await _run_full_interview(client, headers)

    overview = await client.get(f"{API}/dashboard", headers=headers)
    summary = overview.json()["data"]["summary"]
    assert summary["completed_interviews"] == 1
    assert summary["highest_score"] == 85.0
    assert summary["current_streak"] >= 1

    stats = await client.get(f"{API}/dashboard/statistics", headers=headers)
    assert stats.json()["data"]["completed"] == 1

    trends = await client.get(f"{API}/dashboard/trends", headers=headers)
    assert len(trends.json()["data"]) == 1

    achievements = await client.get(f"{API}/dashboard/achievements", headers=headers)
    ids = {a["id"] for a in achievements.json()["data"]}
    assert "first_interview" in ids


# --------------------------------------------------------------------------- #
# Admin                                                                       #
# --------------------------------------------------------------------------- #
@pytest.mark.asyncio
async def test_admin_requires_admin_role(client: AsyncClient) -> None:
    headers = await _login(client, "regular")
    resp = await client.get(f"{API}/admin/dashboard", headers=headers)
    assert resp.status_code == 403
    assert resp.json()["error"]["code"] == "ADMIN_REQUIRED"


async def _promote_to_admin(db_session: AsyncSession, email: str) -> None:
    await db_session.execute(update(User).where(User.email == email).values(role=UserRole.ADMIN))
    await db_session.commit()


@pytest.mark.asyncio
async def test_admin_dashboard_and_users(client: AsyncClient, db_session: AsyncSession) -> None:
    # A separate user to act on (so the admin never suspends themselves).
    await _login(client, "victim")
    headers = await _login(client, "boss")
    await _promote_to_admin(db_session, "boss@example.com")

    dash = await client.get(f"{API}/admin/dashboard", headers=headers)
    assert dash.status_code == 200
    assert dash.json()["data"]["total_users"] >= 2

    users = await client.get(f"{API}/admin/users?search=victim", headers=headers)
    items = users.json()["data"]["items"]
    victim_id = next(u["id"] for u in items if u["email"] == "victim@example.com")

    patch = await client.patch(
        f"{API}/admin/users/{victim_id}/status",
        json={"status": "suspended"},
        headers=headers,
    )
    assert patch.status_code == 200

    audit = await client.get(f"{API}/admin/audit-logs", headers=headers)
    assert audit.status_code == 200


@pytest.mark.asyncio
async def test_admin_user_not_found(client: AsyncClient, db_session: AsyncSession) -> None:
    headers = await _login(client, "boss2")
    await _promote_to_admin(db_session, "boss2@example.com")
    resp = await client.get(f"{API}/admin/users/{uuid.uuid4()}", headers=headers)
    assert resp.status_code == 404
    assert resp.json()["error"]["code"] == "USER_NOT_FOUND"
