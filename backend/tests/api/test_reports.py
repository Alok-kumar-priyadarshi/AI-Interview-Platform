"""API tests for the evaluation + reports domain (post-completion pipeline)."""

from __future__ import annotations

import pytest
from httpx import AsyncClient
from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

from app.models.evaluation import Evaluation
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


@pytest.mark.asyncio
async def test_completion_generates_report_and_evaluations(client: AsyncClient) -> None:
    headers = await _login(client)
    interview_id = await _run_full_interview(client, headers, count=5)

    ref = await client.get(f"{API}/interviews/{interview_id}/report", headers=headers)
    assert ref.status_code == 200, ref.text
    report_id = ref.json()["data"]["report_id"]

    detail = await client.get(f"{API}/reports/{report_id}", headers=headers)
    assert detail.status_code == 200
    data = detail.json()["data"]
    assert data["overall_score"] == 85.0
    assert data["grade"] == "A"
    assert data["hiring_recommendation"] == "hire"
    assert data["summary"]
    assert "technical_knowledge" in data["categories"]
    assert len(data["recommendations"]) >= 1


@pytest.mark.asyncio
async def test_interview_evaluation_aggregate(client: AsyncClient) -> None:
    headers = await _login(client)
    interview_id = await _run_full_interview(client, headers, count=5)
    resp = await client.get(f"{API}/interviews/{interview_id}/evaluation", headers=headers)
    assert resp.status_code == 200
    data = resp.json()["data"]
    assert data["overall_score"] == 85.0
    assert data["categories"]["technical_knowledge"] == 88.0


@pytest.mark.asyncio
async def test_report_listing_and_status(client: AsyncClient) -> None:
    headers = await _login(client)
    await _run_full_interview(client, headers, count=5)
    listing = await client.get(f"{API}/reports", headers=headers)
    body = listing.json()["data"]
    assert body["total"] == 1
    report_id = body["items"][0]["report_id"]

    status = await client.get(f"{API}/reports/{report_id}/status", headers=headers)
    assert status.json()["data"] == {"status": "ready", "progress": 100}


@pytest.mark.asyncio
async def test_pdf_download_returns_pdf(client: AsyncClient) -> None:
    headers = await _login(client)
    interview_id = await _run_full_interview(client, headers, count=5)
    report_id = (
        await client.get(f"{API}/interviews/{interview_id}/report", headers=headers)
    ).json()["data"]["report_id"]
    resp = await client.get(f"{API}/reports/{report_id}/download", headers=headers)
    assert resp.status_code == 200
    assert resp.headers["content-type"] == "application/pdf"
    assert resp.content[:4] == b"%PDF"
    assert 'attachment; filename="' in resp.headers.get("content-disposition", "")


@pytest.mark.asyncio
async def test_per_answer_evaluation_lookup(client: AsyncClient, db_session: AsyncSession) -> None:
    headers = await _login(client)
    await _run_full_interview(client, headers, count=5)

    evaluations = (await db_session.execute(select(Evaluation))).scalars().all()
    assert len(evaluations) == 5
    evaluation_id = evaluations[0].id

    resp = await client.get(f"{API}/evaluations/{evaluation_id}", headers=headers)
    assert resp.status_code == 200
    data = resp.json()["data"]
    assert data["overall_score"] == 85.0
    assert data["grade"] == "A"

    status = await client.get(f"{API}/evaluations/{evaluation_id}/status", headers=headers)
    assert status.json()["data"] == {"status": "completed", "progress": 100}


@pytest.mark.asyncio
async def test_report_ownership_isolation(client: AsyncClient) -> None:
    owner = await _login(client, "owner")
    interview_id = await _run_full_interview(client, owner, count=5)
    report_id = (
        await client.get(f"{API}/interviews/{interview_id}/report", headers=owner)
    ).json()["data"]["report_id"]

    intruder = await _login(client, "intruder")
    resp = await client.get(f"{API}/reports/{report_id}", headers=intruder)
    assert resp.status_code == 404
    assert resp.json()["error"]["code"] == "REPORT_NOT_FOUND"
