"""`GET /api/v1/meta` (Step 7, autonom geschlossene Plan-Lücke — siehe `webui/api.py`s
Moduldocstring). Eigene Datei statt ein Abschnitt in `test_api.py`: ein einzelner Endpunkt mit
einer einzigen Aussage (Statusvokabular == `storage.models.STATUS_VALUES`), kein Grund, ihn in
die deutlich größere `test_api.py` zu mischen.
"""
from __future__ import annotations

import re

import httpx
import pytest
from storage.models import STATUS_VALUES

BASE_URL = "https://space.example.ts.net"
SPACE = "niklas"
PASSWORD = "correct horse battery staple"

_CSRF_RE = re.compile(r'name="csrf" value="([^"]+)"')


def _client(app) -> httpx.AsyncClient:
    return httpx.AsyncClient(transport=httpx.ASGITransport(app=app), base_url=BASE_URL)


async def _login(client: httpx.AsyncClient, totp_code) -> None:
    response = await client.post(
        "/ui/login", data={"space": SPACE, "password": PASSWORD, "totp": totp_code()},
    )
    assert response.status_code == 200


@pytest.mark.asyncio
async def test_meta_returns_status_values_matching_storage_models(full_app_items, totp_code):
    async with _client(full_app_items) as client:
        await _login(client, totp_code)
        response = await client.get("/api/v1/meta")

    assert response.status_code == 200
    expected = {kind: sorted(values) for kind, values in STATUS_VALUES.items()}
    assert response.json()["status_values"] == expected


@pytest.mark.asyncio
async def test_meta_requires_session(full_app_items):
    async with _client(full_app_items) as client:
        response = await client.get("/api/v1/meta")
    assert response.status_code == 401
    assert response.json()["error"] == "unauthenticated"
