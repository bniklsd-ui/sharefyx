"""`GET /api/v1/overview` (Step 7b, autonom geschlossene Plan-Lücke — siehe `webui/api.py`s
Moduldocstring). Speist die Übersichtsseite und die Zähler-Plaketten im Navigationsbaum.

Die Zähler sind hier bewusst prüfbar: der Plan lässt JavaScript ungetestet, deshalb liegt die
Zählung serverseitig und nicht in `app.js`. Die zentrale Aussage der Datei ist, dass ein Zähler
exakt so viele Items meint, wie die Liste beim Klick auf denselben Ordner zeigt — jede andere
Zahl wäre schlimmer als gar keine.
"""
from __future__ import annotations

import re
from datetime import datetime, timedelta, timezone

import httpx
import pytest
from mcpserver.permissions import OwnSpaceWritable
from starlette.applications import Starlette
from storage.store import Store

from webui.account import account_routes
from webui.api import _BUCKETS, api_routes
from webui.routes_auth import ui_auth_routes

BASE_URL = "https://space.example.ts.net"
SPACE = "niklas"
FOREIGN_SPACE = "fabian"
PASSWORD = "correct horse battery staple"

_CSRF_RE = re.compile(r'name="csrf" value="([^"]+)"')


def _client(app) -> httpx.AsyncClient:
    return httpx.AsyncClient(transport=httpx.ASGITransport(app=app), base_url=BASE_URL)


async def _login(client: httpx.AsyncClient, totp_code) -> None:
    response = await client.post(
        "/ui/login", data={"space": SPACE, "password": PASSWORD, "totp": totp_code()},
    )
    assert response.status_code == 200


@pytest.fixture
def ticking_store(tmp_path) -> Store:
    """Eigener `Store` mit einer schrittweise laufenden Uhr — `item_store` aus `conftest.py`
    benutzt die Systemuhr, und die löst innerhalb eines Tests nicht fein genug auf, um eine
    Sortierung nach `updated` überhaupt beobachtbar zu machen."""
    state = {"now": datetime(2026, 8, 5, 9, 0, 0, tzinfo=timezone.utc)}

    def now_fn():
        state["now"] += timedelta(minutes=1)
        return state["now"]

    data_root = tmp_path / "data"
    data_root.mkdir()
    return Store(data_root, git=False, now_fn=now_fn)


@pytest.fixture
def overview_app(ui_settings, store, confirmed_users, sessions, ticking_store) -> Starlette:
    routes = (
        ui_auth_routes(ui_settings, store, confirmed_users, sessions)
        + account_routes(ui_settings, store, confirmed_users, sessions)
        + api_routes(ui_settings, ticking_store, sessions, OwnSpaceWritable())
    )
    return Starlette(routes=routes)


@pytest.fixture
def seeded(ticking_store) -> Store:
    """Ein Item je Ordner plus ein zweites im Archiv, dazu ein fremder Space."""
    ticking_store.create(SPACE, type="task", title="offene Aufgabe")
    ticking_store.create(SPACE, type="task", title="erledigte Aufgabe", status="done")
    ticking_store.create(SPACE, type="note", title="aktive Notiz")
    archived = ticking_store.create(SPACE, type="note", title="alte Notiz")
    ticking_store.archive(archived.id, version=archived.version)
    archived_task = ticking_store.create(SPACE, type="task", title="alte Aufgabe")
    ticking_store.archive(archived_task.id, version=archived_task.version)
    ticking_store.create(FOREIGN_SPACE, type="note", title="Fabians Notiz", body="fremder Text")
    return ticking_store


def _space(payload, name):
    return next(entry for entry in payload if entry["name"] == name)


@pytest.mark.asyncio
async def test_counts_match_the_item_list_for_the_same_bucket(overview_app, seeded, totp_code):
    """Der eigentliche Zweck der Datei: Zähler und Liste dürfen nie auseinanderlaufen. Geprüft
    wird nicht gegen erwartete Zahlen, sondern gegen `/api/v1/items` mit genau den Filtern, die
    `_BUCKETS` für denselben Ordner definiert."""
    async with _client(overview_app) as client:
        await _login(client, totp_code)
        overview = (await client.get("/api/v1/overview")).json()
        own = _space(overview, SPACE)
        for bucket, filters in _BUCKETS.items():
            listing = await client.get(
                "/api/v1/items", params={**filters, "space": SPACE, "limit": 200},
            )
            assert listing.status_code == 200
            assert own["counts"][bucket] == listing.json()["total"], bucket


@pytest.mark.asyncio
async def test_archived_task_lands_in_archive_and_done_task_is_not_lost(overview_app, seeded, totp_code):
    """Der Fund, der den vierten Ordner nötig machte: eine auf `done` gesetzte Aufgabe war in
    keinem der drei Mockup-Ordner mehr auffindbar. Zusätzlich: eine ARCHIVIERTE Aufgabe zählt
    zum Archiv, nicht zu „Offen" (deshalb ist `archived` typunabhängig)."""
    async with _client(overview_app) as client:
        await _login(client, totp_code)
        counts = _space((await client.get("/api/v1/overview")).json(), SPACE)["counts"]

    assert counts["open"] == 1
    assert counts["done"] == 1
    assert counts["note"] == 1
    assert counts["archived"] == 2


@pytest.mark.asyncio
async def test_recent_is_newest_first_and_carries_no_snippet(overview_app, seeded, totp_code):
    async with _client(overview_app) as client:
        await _login(client, totp_code)
        own = _space((await client.get("/api/v1/overview")).json(), SPACE)

    updated = [row["updated"] for row in own["recent"]]
    assert updated == sorted(updated, reverse=True)
    assert len(own["recent"]) <= 5
    # Rule 4 dem Geiste nach: die Übersicht zeigt keinen Fließtext, auch nicht aus dem eigenen
    # Space — sonst wäre die Fläche für fremde Spaces eine Sonderregel statt einer Eigenschaft.
    assert all("snippet" not in row for row in own["recent"])


@pytest.mark.asyncio
async def test_foreign_space_is_visible_but_marked_not_own(overview_app, seeded, totp_code):
    async with _client(overview_app) as client:
        await _login(client, totp_code)
        payload = (await client.get("/api/v1/overview")).json()

    foreign = _space(payload, FOREIGN_SPACE)
    assert foreign["own"] is False
    assert _space(payload, SPACE)["own"] is True
    assert all(row["readonly"] is True for row in foreign["recent"])


@pytest.mark.asyncio
async def test_own_space_appears_even_without_a_single_item(overview_app, totp_code):
    """Derselbe B1-Sonderfall wie in `/api/v1/spaces` (P2-Adapter-Abnahme): ein Space ohne Items
    taucht in `Store.list_spaces()` gar nicht auf — die Übersicht wäre sonst beim allerersten
    Login leer, ohne Zähler und ohne Anlegen-Einstieg."""
    async with _client(overview_app) as client:
        await _login(client, totp_code)
        payload = (await client.get("/api/v1/overview")).json()

    own = _space(payload, SPACE)
    assert own["own"] is True
    assert own["recent"] == []
    assert set(own["counts"]) == set(_BUCKETS)
    assert all(count == 0 for count in own["counts"].values())


@pytest.mark.asyncio
async def test_overview_requires_a_session(overview_app):
    async with _client(overview_app) as client:
        response = await client.get("/api/v1/overview")
    assert response.status_code == 401
    assert response.json()["error"] == "unauthenticated"


@pytest.mark.asyncio
async def test_overview_ignores_a_bearer_token(overview_app):
    """P5-F: `/api` akzeptiert niemals Bearer-Token, nur die Cookie-Sitzung (Akzeptanzkriterium
    19) — für den neuen Endpunkt genauso festgehalten wie für die aus Step 5."""
    async with _client(overview_app) as client:
        response = await client.get(
            "/api/v1/overview", headers={"Authorization": "Bearer irgendein-token"},
        )
    assert response.status_code == 401
