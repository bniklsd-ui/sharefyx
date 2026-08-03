"""Übergreifende Trennung der beiden Auth-Wege (P5-F, Akzeptanzkriterium §6.19): `/mcp`
akzeptiert niemals Cookies (nur `Authorization: Bearer`), `/api`/`/ui` akzeptieren niemals
Bearer-Token (nur Cookie-Session). Dazu P5-G: `/oauth/authorize` liest niemals Cookies.
"""
from __future__ import annotations

from datetime import datetime, timezone

import httpx
import pytest
from authserver.config import AuthSettings
from authserver.routes import oauth_routes
from authserver.store import AuthStore
from authserver.userdir import UserDirectory
from mcpserver.app import OAuthConfig, create_app
from mcpserver.config import Settings
from starlette.applications import Starlette
from starlette.requests import Request
from starlette.responses import Response
from storage.store import Store

from webui.config import COOKIE_NAME, UiSettings
from webui.sessions import SessionManager

BASE_URL = "https://space.example.ts.net"
SPACE = "niklas"


def _issue_ui_session_cookie(auth_store: AuthStore) -> str:
    ui_settings = UiSettings(base_url=BASE_URL)
    sessions = SessionManager(auth_store, settings=ui_settings)
    response = Response()
    sessions.issue(response, space=SPACE)
    return response.headers["set-cookie"].split(";")[0].split("=", 1)[1]


@pytest.mark.asyncio
async def test_mcp_endpoint_ignores_session_cookie(tmp_path):
    """Reale, gültige UI-Sitzung — kein Fantasiewert. `/mcp` muss trotzdem 401 bleiben: es
    kennt nur `Authorization: Bearer`, keine Cookies (P5-F, Richtung 1)."""
    auth_settings = AuthSettings(base_url=BASE_URL, db_path=tmp_path / "auth.sqlite3")
    auth_store = AuthStore(auth_settings.db_path, now_fn=lambda: datetime.now(timezone.utc))
    users = UserDirectory(auth_store, dek=None)
    oauth = OAuthConfig(settings=auth_settings, store=auth_store, users=users)
    data_root = tmp_path / "data"
    data_root.mkdir()
    store = Store(data_root, git=False)
    store.create(SPACE, type="task", title="Item")
    settings = Settings(data_root=data_root)
    app = create_app(settings=settings, store=store, oauth=oauth)

    session_id = _issue_ui_session_cookie(auth_store)

    async with httpx.AsyncClient(
        transport=httpx.ASGITransport(app=app), base_url="http://testserver"
    ) as client:
        result = await client.post(
            "/mcp/", json={}, headers={"Cookie": f"{COOKIE_NAME}={session_id}"}
        )

    assert result.status_code == 401
    assert "WWW-Authenticate" in result.headers


@pytest.mark.asyncio
async def test_oauth_authorize_never_reads_cookies(tmp_path):
    """`start_authorize()`/`_authorize_get()` liest `request.cookies` an keiner Stelle (Plan
    P5-G) — belegt über einen Vergleich: identische Anfrage mit und ohne ein gültiges
    UI-Sitzungscookie muss dasselbe Formular liefern, keinen abgekürzten Consent."""
    auth_settings = AuthSettings(base_url=BASE_URL, db_path=tmp_path / "auth.sqlite3")
    auth_store = AuthStore(auth_settings.db_path, now_fn=lambda: datetime.now(timezone.utc))
    users = UserDirectory(auth_store, dek=None)
    client_row = auth_store.create_client(
        client_name="Claude", application_type=None,
        redirect_uris=["https://claude.ai/api/mcp/auth_callback"],
    )
    app = Starlette(routes=oauth_routes(auth_settings, auth_store, users))

    session_id = _issue_ui_session_cookie(auth_store)

    query = {
        "client_id": client_row.client_id,
        "redirect_uri": "https://claude.ai/api/mcp/auth_callback",
        "response_type": "code",
        "state": "xyz",
        "code_challenge": "a" * 43,
        "code_challenge_method": "S256",
    }

    async with httpx.AsyncClient(
        transport=httpx.ASGITransport(app=app), base_url=BASE_URL
    ) as client:
        without_cookie = await client.get("/oauth/authorize", params=query)
        with_cookie = await client.get(
            "/oauth/authorize", params=query, headers={"Cookie": f"{COOKIE_NAME}={session_id}"}
        )

    assert without_cookie.status_code == with_cookie.status_code == 200
    # Beide sind das Login-Formular (kein abgekürzter Consent wegen der mitgesendeten
    # UI-Sitzung, P5-G); `request_id` ist je Aufruf neu, daher kein reiner Text-/Längenvergleich.
    assert "Anmelden" in without_cookie.text
    assert "Anmelden" in with_cookie.text
    assert 'name="request_id"' in without_cookie.text
    assert 'name="request_id"' in with_cookie.text


def test_api_endpoint_ignores_bearer_token(sessions):
    """Platzhalter (Plan §5 Step 3: „nach Step 5 zu schärfen") — `/api/v1/*` existiert erst ab
    Step 5, ein Mount hier vorzugreifen wäre erfundener Scope. Was jetzt schon geprüft werden
    kann: `SessionManager`, der einzige Auth-Mechanismus, den die UI-Seite bislang hat, liest an
    keiner Stelle einen `Authorization`-Header — ein Request, der ausschließlich ein
    Bearer-Token trägt (kein Cookie), liefert `load()` grundsätzlich `None`."""
    request = Request(
        {
            "type": "http",
            "method": "GET",
            "headers": [(b"authorization", b"Bearer irgendein-mcp-token")],
        }
    )
    assert sessions.load(request) is None
