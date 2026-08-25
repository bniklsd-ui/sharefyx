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

from webui.api import _BUCKETS

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
async def test_meta_publishes_the_bucket_definitions_verbatim(full_app_items, totp_code):
    """Step 7b: die Ordner des Navigationsbaums werden hier herausgegeben, damit `app.js` sie
    nicht ein zweites Mal definiert (vorher standen sie ausschließlich in `filterParams()`).
    Zusätzlich festgehalten, dass jeder Ordner nur aus Filtern besteht, die `/api/v1/items`
    tatsächlich versteht — ein Bucket mit einem Fantasieparameter wäre in der UI eine leere
    Liste ohne Fehlermeldung."""
    async with _client(full_app_items) as client:
        await _login(client, totp_code)
        buckets = (await client.get("/api/v1/meta")).json()["buckets"]

    assert buckets == _BUCKETS
    assert all(set(f) <= {"type", "status"} for f in buckets.values())
    # `archived` steht zuletzt: `app.js :: bucketFor()` nimmt den ersten Treffer, und eine
    # archivierte Aufgabe passt sonst nie ins Archiv (siehe `_BUCKETS`-Kommentar).
    assert list(buckets)[-1] == "archived"


@pytest.mark.asyncio
async def test_meta_reports_the_space_admin_kill_switch(full_app_items, ui_settings, totp_code):
    """P7 Step C2 — `space_admin` im Meta-Payload spiegelt `UiSettings.space_admin_enabled`
    (P7-R), damit C3s UI den Menüpunkt danach ein-/ausblenden kann. `full_app_items` baut
    `ui_settings` mit dem Feld-Default `False` (Step 7 Commit 6) — dieser Test pinnt genau das."""
    async with _client(full_app_items) as client:
        await _login(client, totp_code)
        body = (await client.get("/api/v1/meta")).json()

    assert body["space_admin"] == ui_settings.space_admin_enabled


@pytest.mark.asyncio
async def test_meta_requires_session(full_app_items):
    async with _client(full_app_items) as client:
        response = await client.get("/api/v1/meta")
    assert response.status_code == 401
    assert response.json()["error"] == "unauthenticated"
