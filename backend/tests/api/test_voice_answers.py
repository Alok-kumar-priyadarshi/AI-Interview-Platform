"""API tests for voice answers + transcription (fake Whisper + in-memory storage)."""

from __future__ import annotations

import pytest
from httpx import AsyncClient

from tests.auth_helper import login_headers

API = "/api/v1"

_login = login_headers  # OAuth flow → Authorization header
RESUME_TEXT = b"Jane Candidate\nBackend Developer\nSkills: Python\n"




async def _start_voice_interview(client: AsyncClient, headers: dict) -> str:
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
            "mode": "voice",
            "language": "en",
            "question_count": 5,
        },
        headers=headers,
    )
    interview_id = created.json()["data"]["interview_id"]
    await client.post(f"{API}/interviews/{interview_id}/start", headers=headers)
    return interview_id


@pytest.mark.asyncio
async def test_voice_answer_transcribed_and_stored(client: AsyncClient) -> None:
    headers = await _login(client)
    interview_id = await _start_voice_interview(client, headers)
    q = (
        await client.get(f"{API}/interviews/{interview_id}/questions/current", headers=headers)
    ).json()["data"]

    resp = await client.post(
        f"{API}/interviews/{interview_id}/answers/voice",
        data={"question_id": q["question_id"], "language": "en"},
        files={"audio": ("answer.webm", b"\x00\x01fake-audio", "audio/webm")},
        headers=headers,
    )
    assert resp.status_code == 201, resp.text
    answer_id = resp.json()["data"]["answer_id"]
    assert resp.json()["data"]["transcription_status"] == "completed"

    transcript = await client.get(
        f"{API}/interviews/{interview_id}/answers/{answer_id}/transcript", headers=headers
    )
    assert transcript.status_code == 200
    assert transcript.json()["data"]["transcript"] == "This is the transcribed spoken answer."
    assert transcript.json()["data"]["language"] == "en"


@pytest.mark.asyncio
async def test_unsupported_audio_rejected(client: AsyncClient) -> None:
    headers = await _login(client)
    interview_id = await _start_voice_interview(client, headers)
    q = (
        await client.get(f"{API}/interviews/{interview_id}/questions/current", headers=headers)
    ).json()["data"]
    resp = await client.post(
        f"{API}/interviews/{interview_id}/answers/voice",
        data={"question_id": q["question_id"]},
        files={"audio": ("answer.txt", b"not audio", "text/plain")},
        headers=headers,
    )
    assert resp.status_code == 415
    assert resp.json()["error"]["code"] == "UNSUPPORTED_FILE"
