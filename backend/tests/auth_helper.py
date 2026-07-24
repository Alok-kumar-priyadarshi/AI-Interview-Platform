"""Shared OAuth login helper for API tests.

The backend OAuth callback redirects to the SPA with tokens in the URL fragment
(``#access_token=…&refresh_token=…``). These helpers drive the login flow and
extract the tokens from that redirect.
"""

from __future__ import annotations

from urllib.parse import parse_qs, urlparse

from httpx import AsyncClient

API = "/api/v1"


async def login_tokens(client: AsyncClient, handle: str = "jane") -> dict:
    """Run the full OAuth flow and return the token fragment as a dict."""
    login = await client.get(f"{API}/auth/google/login", follow_redirects=False)
    # The signed state token is embedded in the Google authorization URL.
    state = parse_qs(urlparse(login.headers["location"]).query)["state"][0]
    resp = await client.get(
        f"{API}/auth/google/callback",
        params={"code": handle, "state": state},
        follow_redirects=False,
    )
    fragment = parse_qs(urlparse(resp.headers["location"]).fragment)
    return {key: values[0] for key, values in fragment.items()}


async def login_headers(client: AsyncClient, handle: str = "jane") -> dict:
    """Return an ``Authorization`` header dict for an authenticated user."""
    tokens = await login_tokens(client, handle)
    return {"Authorization": f"Bearer {tokens['access_token']}"}
