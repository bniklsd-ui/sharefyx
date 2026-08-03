"""`/ui/login`, `/ui/logout` gegen eine echte, in-process `Starlette`-App (Plan §5 Step 3,
Done-when: „Login/Logout gegen eine In-Process-App durchgespielt"). `base_url` ist `https://…`
(siehe `conftest.py`-Docstring) — sonst reist das `Secure`-Cookie in httpx nie zurück und jeder
Folgetest sähe fälschlich „keine Sitzung" statt den echten Fehlerfall.
"""
from __future__ import annotations

import re

import httpx
import pytest
from authserver.crypto import pkce_challenge
from authserver.ratelimit import MAX_FAILURES

# Dieselben Konstanten wie in conftest.py — Muster wie test_flows.py/test_routes.py (P4):
# Test-Konstanten werden je Datei dupliziert, nicht über einen Import geteilt.
BASE_URL = "https://space.example.ts.net"
SPACE = "niklas"
PASSWORD = "correct horse battery staple"

_CSRF_RE = re.compile(r'name="csrf" value="([^"]+)"')


def _client(app) -> httpx.AsyncClient:
    return httpx.AsyncClient(transport=httpx.ASGITransport(app=app), base_url=BASE_URL)


def _extract_csrf(html: str) -> str:
    match = _CSRF_RE.search(html)
    assert match is not None, f"kein CSRF-Feld in der Antwort: {html!r}"
    return match.group(1)


@pytest.mark.asyncio
async def test_login_wrong_password_and_unknown_space_are_indistinguishable(app, totp_code):
    async with _client(app) as client:
        wrong_password = await client.post(
            "/ui/login",
            data={"space": SPACE, "password": "falsches-passwort", "totp": totp_code()},
        )
        unknown_space = await client.post(
            "/ui/login",
            data={"space": "ghost-space", "password": "irrelevant", "totp": "000000"},
        )

    assert wrong_password.status_code == unknown_space.status_code == 401
    assert wrong_password.text == unknown_space.text


@pytest.mark.asyncio
async def test_correct_totp_with_wrong_password_does_not_burn_the_counter(app, store, totp_code):
    """Advisor-Fund (P5 Step 3, vor dem Commit): die erste Fassung rief `set_totp_counter()`
    innerhalb des TOTP-Zweigs auf, VOR dem Passwort-Gate — ein richtiger TOTP-Code mit falschem
    Passwort hätte das aktuelle Zeitfenster für den echten Nutzer verbrannt (dieselbe Lehre wie
    `flows.py :: submit_consent()`, jetzt hier wiederholt statt vermieden). Fix: Zähler erst
    nach VOLLSTÄNDIGEM Erfolg hochsetzen."""
    assert store.get_totp_counter(SPACE) is None
    async with _client(app) as client:
        response = await client.post(
            "/ui/login",
            data={"space": SPACE, "password": "falsches-passwort", "totp": totp_code()},
        )
    assert response.status_code == 401
    assert store.get_totp_counter(SPACE) is None


@pytest.mark.asyncio
async def test_login_rotates_session_id(app, clock, store, totp_code):
    async with _client(app) as client:
        first = await client.post(
            "/ui/login", data={"space": SPACE, "password": PASSWORD, "totp": totp_code()},
        )
        assert first.status_code == 200
        first_session_id = client.cookies.get("__Host-sfx_session")
        assert first_session_id is not None

        clock.advance(31)  # neues TOTP-Zeitfenster, sonst Replay-Ablehnung
        second = await client.post(
            "/ui/login", data={"space": SPACE, "password": PASSWORD, "totp": totp_code()},
        )
        assert second.status_code == 200
        second_session_id = client.cookies.get("__Host-sfx_session")

    assert second_session_id is not None
    assert second_session_id != first_session_id
    # die erste Sitzung ist serverseitig widerrufen (rotiert), nicht nur überschrieben
    rows = store.list_sessions(SPACE)
    assert len(rows) == 2
    assert sum(1 for r in rows if r.revoked_at is not None) == 1


@pytest.mark.asyncio
async def test_logout_revokes_server_side(app, store, totp_code):
    async with _client(app) as client:
        login = await client.post(
            "/ui/login", data={"space": SPACE, "password": PASSWORD, "totp": totp_code()},
        )
        csrf_token = _extract_csrf(login.text)

        logout = await client.post(
            "/ui/logout", data={"csrf": csrf_token}, headers={"Origin": BASE_URL},
        )
        assert logout.status_code == 303

    rows = store.list_sessions(SPACE)
    assert len(rows) == 1
    assert rows[0].revoked_at is not None
    assert rows[0].revoked_reason == "logout"


@pytest.mark.asyncio
async def test_expired_session_cookie_is_cleared_on_response(app, clock, totp_code):
    async with _client(app) as client:
        login = await client.post(
            "/ui/login", data={"space": SPACE, "password": PASSWORD, "totp": totp_code()},
        )
        csrf_token = _extract_csrf(login.text)

        clock.advance(12 * 3600 + 1)  # über dem Idle-Timeout (P5-E)
        logout = await client.post(
            "/ui/logout", data={"csrf": csrf_token}, headers={"Origin": BASE_URL},
        )

    assert logout.status_code == 303
    assert "set-cookie" in logout.headers
    assert "__Host-sfx_session=" in logout.headers["set-cookie"]
    assert "Max-Age=0" in logout.headers["set-cookie"] or 'Max-Age="0"' in logout.headers["set-cookie"]


@pytest.mark.asyncio
async def test_ui_pages_carry_security_headers(app):
    async with _client(app) as client:
        response = await client.get("/ui/login")

    assert response.status_code == 200
    assert response.headers["Content-Security-Policy"]
    assert response.headers["X-Frame-Options"] == "DENY"
    assert response.headers["Cache-Control"] == "no-store"


@pytest.mark.asyncio
async def test_login_uses_same_throttle_as_oauth_consent(
    app, store, users, ui_settings, clock, tmp_path, totp_code
):
    from authserver import flows
    from authserver.config import AuthSettings
    from authserver.ratelimit import LoginThrottle

    auth_settings = AuthSettings(
        base_url=ui_settings.base_url, db_path=tmp_path / "unused.sqlite3"
    )
    oauth_client = store.create_client(
        client_name="Claude", application_type=None,
        redirect_uris=["https://claude.ai/api/mcp/auth_callback"],
    )
    oauth_throttle = LoginThrottle(store, now_fn=clock)

    async with _client(app) as client:
        for _ in range(MAX_FAILURES):
            resp = await client.post(
                "/ui/login", data={"space": SPACE, "password": "falsch", "totp": "000000"},
            )
            assert resp.status_code == 401

    # dieselbe `login_attempts`-Zeile (P5 Plan §2.7): eine Sperre über die UI muss den
    # OAuth-Consent-Login für denselben Space genauso treffen.
    pending = flows.start_authorize(
        store=store, settings=auth_settings, client_id=oauth_client.client_id,
        redirect_uri="https://claude.ai/api/mcp/auth_callback", response_type="code",
        state="xyz", code_challenge=pkce_challenge("a" * 64), code_challenge_method="S256",
        scope=None, resource=None,
    )
    assert isinstance(pending, flows.RenderForm)
    result = flows.submit_consent(
        store=store, settings=auth_settings, users=users, throttle=oauth_throttle,
        now_fn=clock, request_id=pending.request_id, space=SPACE, password=PASSWORD,
        totp_code=totp_code(), action="allow",
    )
    assert isinstance(result, flows.ErrorPage)
    assert "gesperrt" in result.message
