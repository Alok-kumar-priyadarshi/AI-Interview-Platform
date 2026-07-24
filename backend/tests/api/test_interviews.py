"""API tests for the interview domain (create → answer → complete)."""

from __future__ import annotations

import pytest
from httpx import AsyncClient

from tests.auth_helper import login_headers

API = "/api/v1"

_login = login_headers  # OAuth flow → Authorization header
RESUME_TEXT = b"Jane Candidate\nBackend Developer\nSkills: Python, FastAPI\n"




async def _upload_resume(client: AsyncClient, headers: dict) -> str:
    up = await client.post(
        f"{API}/resumes", files={"file": ("r.txt", RESUME_TEXT, "text/plain")}, headers=headers
    )
    return up.json()["data"]["resume_id"]


async def _create_interview(client: AsyncClient, headers: dict, resume_id: str, count: int = 5):
    return await client.post(
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


@pytest.mark.asyncio
async def test_create_interview_generates_questions_and_is_ready(client: AsyncClient) -> None:
    headers = await _login(client)
    resume_id = await _upload_resume(client, headers)
    resp = await _create_interview(client, headers, resume_id, count=5)
    assert resp.status_code == 201, resp.text
    data = resp.json()["data"]
    assert data["status"] == "ready"

    detail = await client.get(f"{API}/interviews/{data['interview_id']}", headers=headers)
    assert detail.json()["data"]["total_questions"] == 5


@pytest.mark.asyncio
async def test_full_text_interview_flow(client: AsyncClient) -> None:
    headers = await _login(client)
    resume_id = await _upload_resume(client, headers)
    interview_id = (await _create_interview(client, headers, resume_id, count=5)).json()["data"][
        "interview_id"
    ]

    # Cannot get current question before starting.
    early = await client.get(f"{API}/interviews/{interview_id}/questions/current", headers=headers)
    assert early.status_code == 409

    await client.post(f"{API}/interviews/{interview_id}/start", headers=headers)

    # Answer all five questions in order.
    for expected_seq in (1, 2, 3, 4, 5):
        current = await client.get(
            f"{API}/interviews/{interview_id}/questions/current", headers=headers
        )
        assert current.status_code == 200
        q = current.json()["data"]
        assert q["sequence"] == expected_seq
        submit = await client.post(
            f"{API}/interviews/{interview_id}/answers",
            json={"question_id": q["question_id"], "answer": "A detailed answer."},
            headers=headers,
        )
        assert submit.status_code == 201, submit.text

    status = await client.get(f"{API}/interviews/{interview_id}/status", headers=headers)
    sdata = status.json()["data"]
    assert sdata["completed_questions"] == 5
    assert sdata["remaining_questions"] == 0

    complete = await client.post(f"{API}/interviews/{interview_id}/complete", headers=headers)
    assert complete.status_code == 200

    # Questions + answers become listable after completion.
    qs = await client.get(f"{API}/interviews/{interview_id}/questions", headers=headers)
    assert len(qs.json()["data"]) == 5
    ans = await client.get(f"{API}/interviews/{interview_id}/answers", headers=headers)
    assert len(ans.json()["data"]) == 5


@pytest.mark.asyncio
async def test_duplicate_answer_rejected(client: AsyncClient) -> None:
    headers = await _login(client)
    resume_id = await _upload_resume(client, headers)
    interview_id = (await _create_interview(client, headers, resume_id, count=5)).json()["data"][
        "interview_id"
    ]
    await client.post(f"{API}/interviews/{interview_id}/start", headers=headers)
    q = (
        await client.get(f"{API}/interviews/{interview_id}/questions/current", headers=headers)
    ).json()["data"]
    body = {"question_id": q["question_id"], "answer": "first"}
    await client.post(f"{API}/interviews/{interview_id}/answers", json=body, headers=headers)
    dup = await client.post(f"{API}/interviews/{interview_id}/answers", json=body, headers=headers)
    assert dup.status_code == 409
    assert dup.json()["error"]["code"] == "ANSWER_ALREADY_EXISTS"


@pytest.mark.asyncio
async def test_start_requires_ready_state(client: AsyncClient) -> None:
    headers = await _login(client)
    resume_id = await _upload_resume(client, headers)
    interview_id = (await _create_interview(client, headers, resume_id, count=5)).json()["data"][
        "interview_id"
    ]
    await client.post(f"{API}/interviews/{interview_id}/start", headers=headers)
    # Second start is invalid (already in_progress).
    again = await client.post(f"{API}/interviews/{interview_id}/start", headers=headers)
    assert again.status_code == 409
    assert again.json()["error"]["code"] == "INVALID_INTERVIEW_STATE"


@pytest.mark.asyncio
async def test_ownership_isolation(client: AsyncClient) -> None:
    owner = await _login(client, "owner")
    resume_id = await _upload_resume(client, owner)
    interview_id = (await _create_interview(client, owner, resume_id)).json()["data"][
        "interview_id"
    ]
    intruder = await _login(client, "intruder")
    resp = await client.get(f"{API}/interviews/{interview_id}", headers=intruder)
    assert resp.status_code == 404


@pytest.mark.asyncio
async def test_list_interviews_paginated(client: AsyncClient) -> None:
    headers = await _login(client)
    resume_id = await _upload_resume(client, headers)
    await _create_interview(client, headers, resume_id)
    listing = await client.get(f"{API}/interviews?page=1&page_size=10", headers=headers)
    body = listing.json()["data"]
    assert body["total"] == 1
    assert body["page"] == 1
    assert len(body["items"]) == 1
