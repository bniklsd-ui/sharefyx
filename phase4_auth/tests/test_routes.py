"""HTTP-Verdrahtung von `/oauth/authorize` und `/oauth/token` (Plan §5 Step 5) über echte
Requests (`httpx.ASGITransport`, gleiches Muster wie `test_clients.py`/`test_metadata.py`).
Die eigentliche Zustandslogik ist bereits in `test_flows.py` gegen `flows.py` direkt geprüft —
hier geht es um das, was nur über HTTP sichtbar ist: Statuscodes, Redirect-Ziel, Header, Cookies.
"""
import re
from datetime import datetime, timezone
from urllib.parse import parse_qs, urlsplit

import httpx
import pytest
from starlette.applications import Starlette

from authserver import passwords, totp
from authserver.config import AuthSettings
from authserver.crypto import pkce_challenge
from authserver.routes import oauth_routes
from authserver.secretbox import KEY_LEN, seal
from authserver.store import AuthStore
from authserver.userdir import UserDirectory

REDIRECT_URI = "https://claude.ai/api/mcp/auth_callback"
SPACE = "niklas"
PASSWORD = "correct horse battery staple"
TOTP_SECRET = totp.generate_secret()
VERIFIER = "b" * 64
CODE_CHALLENGE = pkce_challenge(VERIFIER)
FIXED_NOW = datetime(2026, 7, 28, 12, 0, 0, tzinfo=timezone.utc)


@pytest.fixture
def settings(tmp_path):
    return AuthSettings(base_url="https://space.example.ts.net", db_path=tmp_path / "unused.sqlite3")


@pytest.fixture
def store(tmp_path):
    return AuthStore(tmp_path / "auth.sqlite3", now_fn=lambda: FIXED_NOW)


@pytest.fixture
def dek() -> bytes:
    return bytes([0x5A]) * KEY_LEN


@pytest.fixture
def users(store, dek):
    """P5 Step 2: `UserDirectory` statt eines rohen `Mapping` — nur die Fixture-Konstruktion
    ändert sich, Testdaten und Assertions in diesem Modul bleiben unverändert."""
    store.upsert_user(
        SPACE,
        password_hash=passwords.hash_password(PASSWORD),
        totp_secret_enc=seal(TOTP_SECRET.encode("ascii"), key=dek, aad=SPACE.encode("utf-8")),
        totp_alg="SHA1",
        totp_confirmed_at=None,
        status="active",
    )
    return UserDirectory(store, dek=dek)


@pytest.fixture
def client_record(store):
    return store.create_client(
        client_name="Claude", application_type=None, redirect_uris=[REDIRECT_URI]
    )


@pytest.fixture
def app(settings, store, users):
    return Starlette(routes=oauth_routes(settings, store, users))


@pytest.fixture
def client_factory(app):
    def factory() -> httpx.AsyncClient:
        return httpx.AsyncClient(transport=httpx.ASGITransport(app=app), base_url="http://testserver")

    return factory


def _totp_code() -> str:
    counter = int(FIXED_NOW.timestamp() // 30)
    return totp.totp_at(TOTP_SECRET, counter, algo="SHA1")


def _authorize_query(client_id: str, *, redirect_uri=REDIRECT_URI, state="xyz") -> dict[str, str]:
    return {
        "client_id": client_id,
        "redirect_uri": redirect_uri,
        "response_type": "code",
        "state": state,
        "code_challenge": CODE_CHALLENGE,
        "code_challenge_method": "S256",
    }


def _extract_request_id(html: str) -> str:
    match = re.search(r'name="request_id" value="([^"]+)"', html)
    assert match, html
    return match.group(1)


async def _obtain_code(client: httpx.AsyncClient, client_record) -> str:
    """Ein vollständiger, einmaliger Durchlauf GET+POST /oauth/authorize. Pro Test höchstens
    einmal aufrufen — der TOTP-Zähler dieses Space würde bei einem zweiten Aufruf innerhalb
    derselben (fest eingefrorenen) Sekunde als Replay gelten."""
    get_resp = await client.get("/oauth/authorize", params=_authorize_query(client_record.client_id))
    request_id = _extract_request_id(get_resp.text)
    post_resp = await client.post(
        "/oauth/authorize",
        data={
            "request_id": request_id, "space": SPACE, "password": PASSWORD,
            "totp": _totp_code(), "action": "allow",
        },
        follow_redirects=False,
    )
    return parse_qs(urlsplit(post_resp.headers["location"]).query)["code"][0]


# -- /oauth/authorize ---------------------------------------------------------------------


@pytest.mark.asyncio
async def test_authorize_get_renders_login_form_for_valid_request(client_factory, client_record):
    async with client_factory() as client:
        resp = await client.get("/oauth/authorize", params=_authorize_query(client_record.client_id))
    assert resp.status_code == 200
    assert "location" not in resp.headers
    assert "request_id" in resp.text


@pytest.mark.asyncio
async def test_authorize_get_unknown_client_returns_error_page_not_redirect(client_factory):
    async with client_factory() as client:
        resp = await client.get(
            "/oauth/authorize", params=_authorize_query("ghost-client"), follow_redirects=False,
        )
    assert resp.status_code == 400
    assert "location" not in resp.headers


@pytest.mark.asyncio
async def test_authorize_post_happy_path_redirects_with_code(client_factory, client_record):
    async with client_factory() as client:
        code = await _obtain_code(client, client_record)
    assert code


@pytest.mark.asyncio
async def test_authorize_post_deny_redirects_with_access_denied(client_factory, client_record):
    async with client_factory() as client:
        get_resp = await client.get("/oauth/authorize", params=_authorize_query(client_record.client_id))
        request_id = _extract_request_id(get_resp.text)
        resp = await client.post(
            "/oauth/authorize",
            data={"request_id": request_id, "space": SPACE, "password": "", "totp": "", "action": "deny"},
            follow_redirects=False,
        )
    assert resp.status_code == 302
    query = parse_qs(urlsplit(resp.headers["location"]).query)
    assert query["error"] == ["access_denied"]
    assert query["state"] == ["xyz"]


# -- /oauth/token -------------------------------------------------------------------------


@pytest.mark.asyncio
async def test_token_endpoint_exchanges_code_for_tokens(client_factory, client_record):
    async with client_factory() as client:
        code = await _obtain_code(client, client_record)
        resp = await client.post(
            "/oauth/token",
            data={
                "grant_type": "authorization_code", "code": code, "redirect_uri": REDIRECT_URI,
                "client_id": client_record.client_id, "code_verifier": VERIFIER,
            },
        )
    assert resp.status_code == 200
    body = resp.json()
    assert body["token_type"] == "Bearer"
    assert body["access_token"]
    assert body["refresh_token"]
    assert body["scope"] == "space"


@pytest.mark.asyncio
async def test_token_response_has_no_store(client_factory, client_record):
    async with client_factory() as client:
        code = await _obtain_code(client, client_record)
        resp = await client.post(
            "/oauth/token",
            data={
                "grant_type": "authorization_code", "code": code, "redirect_uri": REDIRECT_URI,
                "client_id": client_record.client_id, "code_verifier": VERIFIER,
            },
        )
    assert resp.headers["cache-control"] == "no-store"
    assert resp.headers["pragma"] == "no-cache"


@pytest.mark.asyncio
async def test_token_endpoint_rejects_bad_grant_type(client_factory):
    async with client_factory() as client:
        resp = await client.post("/oauth/token", data={"grant_type": "carrier_pigeon"})
    assert resp.status_code == 400
    assert resp.json()["error"] == "unsupported_grant_type"


# -- Sicherheits-Header und Cookies (Plan §2.6, P4-O) --------------------------------------


@pytest.mark.asyncio
async def test_html_responses_carry_security_headers(client_factory, client_record):
    async with client_factory() as client:
        resp = await client.get("/oauth/authorize", params=_authorize_query(client_record.client_id))
    assert resp.headers["content-security-policy"].startswith("default-src 'none'")
    assert resp.headers["referrer-policy"] == "no-referrer"
    assert resp.headers["x-content-type-options"] == "nosniff"
    assert resp.headers["x-frame-options"] == "DENY"
    assert resp.headers["cache-control"] == "no-store"
    assert "strict-transport-security" in resp.headers


@pytest.mark.asyncio
async def test_csp_form_action_allows_the_oauth_redirect_target(client_factory, client_record):
    """Live-Fund 2026-07-30: Chromium prüft `form-action` auch gegen das Redirect-Ziel einer
    Formular-Antwort, nicht nur gegen das unmittelbare `action`-Attribut — `POST
    /oauth/authorize` antwortet bei Erfolg mit einem 302 nach `settings.allowed_redirect_origins`.
    Fehlt einer dieser Origins in `form-action`, blockiert der Browser den Redirect lautlos
    (kein Fehler auf der Seite, der Server selbst antwortet korrekt mit 302 + gültigem Code)."""
    async with client_factory() as client:
        resp = await client.get("/oauth/authorize", params=_authorize_query(client_record.client_id))
    csp = resp.headers["content-security-policy"]
    assert "form-action 'self' https://claude.ai https://claude.com" in csp


@pytest.mark.asyncio
async def test_redirect_with_existing_query_keeps_both_params(client_factory, store):
    """S5: ein registrierter Redirect mit eigenem Query-String darf durch die Code-Antwort nicht
    verstümmelt werden — `code`/`state` müssen dazukommen, nicht das erste `?` verdoppeln."""
    redirect_with_query = "https://claude.ai/api/mcp/auth_callback?tenant=acme"
    client_record = store.create_client(
        client_name="Claude", application_type=None, redirect_uris=[redirect_with_query]
    )
    async with client_factory() as client:
        get_resp = await client.get(
            "/oauth/authorize", params=_authorize_query(client_record.client_id, redirect_uri=redirect_with_query)
        )
        request_id = _extract_request_id(get_resp.text)
        post_resp = await client.post(
            "/oauth/authorize",
            data={
                "request_id": request_id, "space": SPACE, "password": PASSWORD,
                "totp": _totp_code(), "action": "allow",
            },
            follow_redirects=False,
        )
    location = post_resp.headers["location"]
    split = urlsplit(location)
    assert split.netloc == "claude.ai" and split.path == "/api/mcp/auth_callback"
    query = parse_qs(split.query)
    assert query["tenant"] == ["acme"]
    assert query["code"]
    assert query["state"] == ["xyz"]


@pytest.mark.asyncio
async def test_redirect_error_with_existing_query_keeps_both_params(client_factory, store):
    redirect_with_query = "https://claude.ai/api/mcp/auth_callback?tenant=acme"
    client_record = store.create_client(
        client_name="Claude", application_type=None, redirect_uris=[redirect_with_query]
    )
    async with client_factory() as client:
        get_resp = await client.get(
            "/oauth/authorize", params=_authorize_query(client_record.client_id, redirect_uri=redirect_with_query)
        )
        request_id = _extract_request_id(get_resp.text)
        resp = await client.post(
            "/oauth/authorize",
            data={"request_id": request_id, "space": SPACE, "password": "", "totp": "", "action": "deny"},
            follow_redirects=False,
        )
    query = parse_qs(urlsplit(resp.headers["location"]).query)
    assert query["tenant"] == ["acme"]
    assert query["error"] == ["access_denied"]


@pytest.mark.asyncio
async def test_no_cookie_is_ever_set(client_factory, client_record):
    """Belegt P4-O (kein Cookie, nirgends) über den vollständigen Fluss: GET-Formular,
    POST-Consent, POST-Token-Tausch."""
    async with client_factory() as client:
        get_resp = await client.get("/oauth/authorize", params=_authorize_query(client_record.client_id))
        assert "set-cookie" not in get_resp.headers
        request_id = _extract_request_id(get_resp.text)

        post_resp = await client.post(
            "/oauth/authorize",
            data={
                "request_id": request_id, "space": SPACE, "password": PASSWORD,
                "totp": _totp_code(), "action": "allow",
            },
            follow_redirects=False,
        )
        assert "set-cookie" not in post_resp.headers
        code = parse_qs(urlsplit(post_resp.headers["location"]).query)["code"][0]

        token_resp = await client.post(
            "/oauth/token",
            data={
                "grant_type": "authorization_code", "code": code, "redirect_uri": REDIRECT_URI,
                "client_id": client_record.client_id, "code_verifier": VERIFIER,
            },
        )
        assert "set-cookie" not in token_resp.headers
