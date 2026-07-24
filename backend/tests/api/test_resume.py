"""API tests for the resume endpoints (fake AI + in-memory storage)."""

from __future__ import annotations

import pytest
from httpx import AsyncClient

from tests.auth_helper import login_tokens

API = "/api/v1"
RESUME_TEXT = b"Jane Candidate\nBackend Developer\nSkills: Python, FastAPI, PostgreSQL\n"


async def _login(client: AsyncClient, handle: str = "jane") -> str:
    """Return the access token (this file's callers build headers themselves)."""
    tokens = await login_tokens(client, handle)
    return tokens["access_token"]


def _txt_file(name: str = "resume.txt") -> dict:
    return {"file": (name, RESUME_TEXT, "text/plain")}


@pytest.mark.asyncio
async def test_upload_processes_resume_and_creates_profile(client: AsyncClient) -> None:
    token = await _login(client)
    headers = {"Authorization": f"Bearer {token}"}

    up = await client.post(f"{API}/resumes", files=_txt_file(), headers=headers)
    assert up.status_code == 201, up.text
    data = up.json()["data"]
    assert data["status"] == "completed"
    resume_id = data["resume_id"]

    # First resume becomes the default.
    listing = await client.get(f"{API}/resumes", headers=headers)
    items = listing.json()["data"]
    assert len(items) == 1
    assert items[0]["is_default"] is True

    # Metadata reflects the (fake) AI extraction.
    meta = await client.get(f"{API}/resumes/{resume_id}/metadata", headers=headers)
    assert meta.status_code == 200
    assert meta.json()["data"]["skills"] == [{"name": "Python", "level": "Advanced"}]

    # Status endpoint reports completion.
    status = await client.get(f"{API}/resumes/{resume_id}/status", headers=headers)
    assert status.json()["data"] == {"status": "completed", "progress": 100}


@pytest.mark.asyncio
async def test_unsupported_file_type_rejected(client: AsyncClient) -> None:
    token = await _login(client)
    headers = {"Authorization": f"Bearer {token}"}
    resp = await client.post(
        f"{API}/resumes",
        files={"file": ("resume.exe", b"MZ...", "application/octet-stream")},
        headers=headers,
    )
    assert resp.status_code == 415
    assert resp.json()["error"]["code"] == "UNSUPPORTED_FILE"


@pytest.mark.asyncio
async def test_duplicate_upload_rejected(client: AsyncClient) -> None:
    token = await _login(client)
    headers = {"Authorization": f"Bearer {token}"}
    await client.post(f"{API}/resumes", files=_txt_file(), headers=headers)
    dup = await client.post(f"{API}/resumes", files=_txt_file(), headers=headers)
    assert dup.status_code == 409
    assert dup.json()["error"]["code"] == "CONFLICT"


@pytest.mark.asyncio
async def test_set_default_moves_flag(client: AsyncClient) -> None:
    token = await _login(client)
    headers = {"Authorization": f"Bearer {token}"}
    first = (await client.post(f"{API}/resumes", files=_txt_file("a.txt"), headers=headers)).json()
    second_bytes = RESUME_TEXT + b"second"
    second = (
        await client.post(
            f"{API}/resumes",
            files={"file": ("b.txt", second_bytes, "text/plain")},
            headers=headers,
        )
    ).json()

    await client.patch(f"{API}/resumes/{second['data']['resume_id']}/default", headers=headers)

    resumes = (await client.get(f"{API}/resumes", headers=headers)).json()["data"]
    listing = {r["id"]: r["is_default"] for r in resumes}
    assert listing[second["data"]["resume_id"]] is True
    assert listing[first["data"]["resume_id"]] is False


@pytest.mark.asyncio
async def test_ownership_isolation(client: AsyncClient) -> None:
    owner_token = await _login(client, "owner")
    owner_headers = {"Authorization": f"Bearer {owner_token}"}
    up = await client.post(f"{API}/resumes", files=_txt_file(), headers=owner_headers)
    resume_id = up.json()["data"]["resume_id"]

    intruder_token = await _login(client, "intruder")
    intruder_headers = {"Authorization": f"Bearer {intruder_token}"}
    resp = await client.get(f"{API}/resumes/{resume_id}", headers=intruder_headers)
    assert resp.status_code == 404
    assert resp.json()["error"]["code"] == "RESUME_NOT_FOUND"


@pytest.mark.asyncio
async def test_delete_resume(client: AsyncClient) -> None:
    token = await _login(client)
    headers = {"Authorization": f"Bearer {token}"}
    up = await client.post(f"{API}/resumes", files=_txt_file(), headers=headers)
    resume_id = up.json()["data"]["resume_id"]

    delete = await client.delete(f"{API}/resumes/{resume_id}", headers=headers)
    assert delete.status_code == 200
    gone = await client.get(f"{API}/resumes/{resume_id}", headers=headers)
    assert gone.status_code == 404
