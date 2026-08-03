"""`/api/v1/account/*` (Plan §2.8/§3.3, §5 Step 4) — gegen `full_app` (`ui_auth_routes()` +
`account_routes()` zusammen: Login mintet die Sitzung, die die Account-Routen brauchen)."""
from __future__ import annotations

import re

import httpx
import pytest
from starlette.applications import Starlette

from webui.account import account_routes
from webui.routes_auth import ui_auth_routes

BASE_URL = "https://space.example.ts.net"
SPACE = "niklas"
FOREIGN_SPACE = "fabian"
PASSWORD = "correct horse battery staple"
NEW_PASSWORD = "even longer correct horse battery"

_CSRF_RE = re.compile(r'name="csrf" value="([^"]+)"')


def _client(app) -> httpx.AsyncClient:
    return httpx.AsyncClient(transport=httpx.ASGITransport(app=app), base_url=BASE_URL)


async def _login(client: httpx.AsyncClient, totp_code) -> str:
    response = await client.post(
        "/ui/login", data={"space": SPACE, "password": PASSWORD, "totp": totp_code()},
    )
    assert response.status_code == 200
    return _CSRF_RE.search(response.text).group(1)


@pytest.mark.asyncio
async def test_account_is_locked_to_enrollment_until_totp_confirmed(
    ui_settings, store, users, sessions, totp_code
):
    """`users` (nicht `confirmed_users`) ist bewusst unbestätigt — genau der Zustand, den §2.8s
    Gate abfängt."""
    app = Starlette(
        routes=ui_auth_routes(ui_settings, store, users, sessions)
        + account_routes(ui_settings, store, users, sessions)
    )
    async with _client(app) as client:
        await _login(client, totp_code)
        response = await client.get("/api/v1/account/connectors")

    assert response.status_code == 403
    assert response.json()["error"] == "totp_required"


@pytest.mark.asyncio
async def test_password_change_requires_password_and_totp(full_app, totp_code, clock):
    async with _client(full_app) as client:
        csrf = await _login(client, totp_code)

        wrong = await client.post(
            "/api/v1/account/password",
            json={"password": "falsch", "totp": "000000", "new_password": NEW_PASSWORD},
            headers={"Origin": BASE_URL, "X-CSRF-Token": csrf},
        )
        assert wrong.status_code == 403
        assert wrong.json()["error"] == "forbidden"

        clock.advance(31)
        right = await client.post(
            "/api/v1/account/password",
            json={"password": PASSWORD, "totp": totp_code(), "new_password": NEW_PASSWORD},
            headers={"Origin": BASE_URL, "X-CSRF-Token": csrf},
        )
        assert right.status_code == 200


@pytest.mark.asyncio
async def test_password_change_revokes_all_token_families(full_app, store, totp_code, clock):
    f1 = store.create_family(space=SPACE, client_id="c1", scope="space", resource="https://x/mcp")
    f2 = store.create_family(space=SPACE, client_id="c2", scope="space", resource="https://x/mcp")

    async with _client(full_app) as client:
        csrf = await _login(client, totp_code)
        clock.advance(31)  # neues TOTP-Zeitfenster, sonst Replay-Ablehnung bei der Re-Auth
        response = await client.post(
            "/api/v1/account/password",
            json={"password": PASSWORD, "totp": totp_code(), "new_password": NEW_PASSWORD},
            headers={"Origin": BASE_URL, "X-CSRF-Token": csrf},
        )
    assert response.status_code == 200

    by_id = {f.family_id: f for f in store.list_families(space=SPACE)}
    assert by_id[f1].revoked_at is not None
    assert by_id[f2].revoked_at is not None


@pytest.mark.asyncio
async def test_password_change_returns_a_usable_csrf_token(full_app, totp_code, clock):
    """Advisor-Fund vor diesem Commit: `sessions.rotate()` gibt den CSRF-Token nur EIN
    einziges Mal zurück (`ui_sessions` speichert nur `csrf_hash`) — ein verworfener
    Rückgabewert hätte jede folgende CSRF-geprüfte Anfrage bis zum nächsten Login mit
    `403 csrf_failed` blockiert. Das reicht `test_password_change_requires_password_and_totp`
    nicht ab, weil der dortige zweite Aufruf noch den ALTEN Token benutzt (vor der Rotation)."""
    async with _client(full_app) as client:
        csrf = await _login(client, totp_code)
        clock.advance(31)
        changed = await client.post(
            "/api/v1/account/password",
            json={"password": PASSWORD, "totp": totp_code(), "new_password": NEW_PASSWORD},
            headers={"Origin": BASE_URL, "X-CSRF-Token": csrf},
        )
        assert changed.status_code == 200
        new_csrf = changed.json()["csrf_token"]
        assert new_csrf != csrf

        clock.advance(31)
        follow_up = await client.request(
            "DELETE", "/api/v1/account/sessions",
            json={"password": NEW_PASSWORD, "totp": totp_code()},
            headers={"Origin": BASE_URL, "X-CSRF-Token": new_csrf},
        )
    assert follow_up.status_code == 200


@pytest.mark.asyncio
async def test_password_change_revokes_other_sessions_but_not_current(full_app, totp_code, clock):
    async with _client(full_app) as client_a, _client(full_app) as client_b:
        csrf_a = await _login(client_a, totp_code)
        clock.advance(31)
        await _login(client_b, totp_code)

        clock.advance(31)
        response = await client_a.post(
            "/api/v1/account/password",
            json={"password": PASSWORD, "totp": totp_code(), "new_password": NEW_PASSWORD},
            headers={"Origin": BASE_URL, "X-CSRF-Token": csrf_a},
        )
        assert response.status_code == 200
        # Session A rotiert (P5-E), aber bleibt gültig — httpx übernimmt das neue Cookie aus
        # der Antwort automatisch in seinen eigenen Cookie-Jar.
        still_a = await client_a.get("/api/v1/account/connectors")
        assert still_a.status_code == 200

        dead_b = await client_b.get("/api/v1/account/connectors")
    assert dead_b.status_code == 401


@pytest.mark.asyncio
async def test_connector_list_shows_only_own_families(full_app, store, totp_code):
    own = store.create_family(space=SPACE, client_id="c1", scope="space", resource="https://x/mcp")
    store.create_family(space=FOREIGN_SPACE, client_id="c2", scope="space", resource="https://x/mcp")

    async with _client(full_app) as client:
        await _login(client, totp_code)
        response = await client.get("/api/v1/account/connectors")

    assert response.status_code == 200
    ids = [c["family_id"] for c in response.json()]
    assert ids == [own]


@pytest.mark.asyncio
async def test_connector_revoke_of_foreign_family_is_404_not_403(full_app, store, totp_code, clock):
    foreign = store.create_family(
        space=FOREIGN_SPACE, client_id="c2", scope="space", resource="https://x/mcp"
    )

    async with _client(full_app) as client:
        csrf = await _login(client, totp_code)
        clock.advance(31)  # neues TOTP-Zeitfenster, sonst Replay-Ablehnung bei der Re-Auth
        response = await client.request(
            "DELETE", f"/api/v1/account/connectors/{foreign}",
            json={"password": PASSWORD, "totp": totp_code()},
            headers={"Origin": BASE_URL, "X-CSRF-Token": csrf},
        )

    assert response.status_code == 404
    assert response.json()["error"] == "not_found"
    # Die fremde Familie ist unangetastet — ein 404 darf keine Nebenwirkung haben.
    (family,) = store.list_families(space=FOREIGN_SPACE)
    assert family.revoked_at is None
