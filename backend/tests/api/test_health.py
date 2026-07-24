"""API tests for the Health & monitoring endpoints."""

from __future__ import annotations

import pytest
from httpx import AsyncClient

API = "/api/v1"


@pytest.mark.asyncio
async def test_health_returns_healthy(client: AsyncClient) -> None:
    resp = await client.get(f"{API}/health")
    assert resp.status_code == 200
    body = resp.json()
    assert body["success"] is True
    assert body["data"]["status"] == "healthy"
    assert body["data"]["version"] == "1.0.0"
    assert "uptime_seconds" in body["data"]


@pytest.mark.asyncio
async def test_liveness_is_independent_of_dependencies(client: AsyncClient) -> None:
    resp = await client.get(f"{API}/health/live")
    assert resp.status_code == 200
    assert resp.json() == {"status": "alive"}


@pytest.mark.asyncio
async def test_readiness_ok_when_database_reachable(client: AsyncClient) -> None:
    resp = await client.get(f"{API}/health/ready")
    assert resp.status_code == 200
    assert resp.json() == {"status": "ready"}


@pytest.mark.asyncio
async def test_version_endpoint(client: AsyncClient) -> None:
    resp = await client.get(f"{API}/health/version")
    assert resp.status_code == 200
    data = resp.json()["data"]
    assert data["version"] == "1.0.0"
    assert data["environment"] == "ci"


@pytest.mark.asyncio
async def test_request_id_header_present(client: AsyncClient) -> None:
    resp = await client.get(f"{API}/health/live")
    assert resp.headers.get("X-Request-ID", "").startswith("req_")


@pytest.mark.asyncio
async def test_unknown_route_returns_standard_error_envelope(client: AsyncClient) -> None:
    resp = await client.get(f"{API}/does-not-exist")
    assert resp.status_code == 404
    body = resp.json()
    assert body["success"] is False
    assert "code" in body["error"]
    assert body["request_id"].startswith("req_")
