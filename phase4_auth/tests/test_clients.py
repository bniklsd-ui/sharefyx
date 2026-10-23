from datetime import datetime, timezone
from pathlib import Path

import httpx
import pytest
from starlette.applications import Starlette

from authserver.clients import MAX_REGISTRATIONS_PER_WINDOW, redirect_uri_allowed
from authserver.config import AuthSettings
from authserver.routes import oauth_routes
from authserver.store import AuthStore

CLAUDE_REDIRECT_URI = "https://claude.ai/api/mcp/auth_callback"
# [2026-10-22, P10.5 Block 6] Die Form, die opencode wirklich schickt (V209, opencode 1.19.4):
# `http://127.0.0.1:19876/mcp/oauth/callback` — 127.0.0.1, expliziter Port, kein Query.
LOOPBACK_REDIRECT_URI = "http://127.0.0.1:19876/mcp/oauth/callback"


@pytest.fixture
def settings(tmp_path):
    return AuthSettings(base_url="https://space.example.ts.net", db_path=tmp_path / "unused.sqlite3")


@pytest.fixture
def store(tmp_path):
    return AuthStore(
        tmp_path / "auth.sqlite3", now_fn=lambda: datetime(2026, 7, 28, 12, 0, 0, tzinfo=timezone.utc)
    )


@pytest.fixture
def app(settings, store):
    return Starlette(routes=oauth_routes(settings, store, {}))


@pytest.fixture
def client_factory(app):
    def factory() -> httpx.AsyncClient:
        return httpx.AsyncClient(transport=httpx.ASGITransport(app=app), base_url="http://testserver")

    return factory


@pytest.mark.asyncio
async def test_register_accepts_claude_redirect_uri(client_factory):
    async with client_factory() as client:
        resp = await client.post(
            "/oauth/register",
            json={"client_name": "Claude", "redirect_uris": [CLAUDE_REDIRECT_URI]},
        )
    assert resp.status_code == 201
    assert resp.json()["redirect_uris"] == [CLAUDE_REDIRECT_URI]


@pytest.mark.asyncio
async def test_register_rejects_foreign_origin(client_factory):
    async with client_factory() as client:
        resp = await client.post(
            "/oauth/register", json={"redirect_uris": ["https://evil.example/callback"]}
        )
    assert resp.status_code == 400
    assert resp.json()["error"] == "invalid_redirect_uri"


@pytest.mark.asyncio
async def test_register_accepts_native_with_loopback_redirect(client_factory):
    """[2026-10-22, P10.5 Block 6, Lock P10.5-O] `application_type: "native"` wird angenommen —
    die Pauschalablehnung von P4 (Nikinger-Entscheidung 2026-07-28) ist datiert abgelöst. Der
    alte Test `test_register_rejects_native_application_type` (Zeile 63) wurde **bewusst durch
    diesen ersetzt**, nicht gelöscht: die Ablehnung gilt jetzt nur noch für unbekannte Werte
    (`test_register_rejects_unknown_application_type`)."""
    async with client_factory() as client:
        resp = await client.post(
            "/oauth/register",
            json={"application_type": "native", "redirect_uris": [LOOPBACK_REDIRECT_URI]},
        )
    assert resp.status_code == 201
    body = resp.json()
    assert body["redirect_uris"] == [LOOPBACK_REDIRECT_URI]
    assert body["application_type"] == "native"


@pytest.mark.asyncio
@pytest.mark.parametrize("payload", [
    pytest.param({"redirect_uris": [LOOPBACK_REDIRECT_URI]}, id="fehlend"),
    pytest.param({"application_type": None, "redirect_uris": [LOOPBACK_REDIRECT_URI]}, id="null"),
])
async def test_register_accepts_missing_application_type_with_loopback(client_factory, payload):
    """Die Form, die opencode wirklich schickt (V209, opencode 1.19.4): der DCR-Request traegt
    `application_type` **nicht** (`body.get("application_type")` liefert dann `None`) — erstaunlich
    genug: `null` und "fehlt" sind im JSON nicht unterscheidbar, wenn man es so liest."""
    async with client_factory() as client:
        resp = await client.post("/oauth/register", json=payload)
    assert resp.status_code == 201
    assert resp.json()["redirect_uris"] == [LOOPBACK_REDIRECT_URI]


@pytest.mark.asyncio
async def test_register_rejects_web_with_loopback(client_factory):
    """Ein "web"-Client laeuft im Browser auf einem fremden Rechner — ein Loopback-Ruecksprung
    kaeme dort nie an (P10.5-O). Abgelehnt wird er als **Redirect-Problem**
    (`invalid_redirect_uri`), nicht als Metadatenproblem: die Metadaten sind gueltig."""
    async with client_factory() as client:
        resp = await client.post(
            "/oauth/register",
            json={"application_type": "web", "redirect_uris": [LOOPBACK_REDIRECT_URI]},
        )
    assert resp.status_code == 400
    assert resp.json()["error"] == "invalid_redirect_uri"


@pytest.mark.asyncio
async def test_register_rejects_unknown_application_type(client_factory):
    async with client_factory() as client:
        resp = await client.post(
            "/oauth/register",
            json={"application_type": "desktop", "redirect_uris": [CLAUDE_REDIRECT_URI]},
        )
    assert resp.status_code == 400
    assert resp.json()["error"] == "invalid_client_metadata"


@pytest.mark.asyncio
@pytest.mark.parametrize("uri", [
    "http://127.0.0.1/callback",
    "http://127.0.0.1:0/callback",
    "http://127.0.0.1:70000/callback",
    "http://127.0.0.1:not-a-port/callback",
])
async def test_loopback_requires_explicit_port(client_factory, uri):
    """P10.5-O: der Port ist **explizit** (RFC 8252 §7.3 erlaubt auch den Wegfall — bewusst
    nicht gebaut). Port 0 und ein Port ausserhalb 1..65535 sind keine Ports."""
    async with client_factory() as client:
        resp = await client.post("/oauth/register", json={"redirect_uris": [uri]})
    assert resp.status_code == 400
    assert resp.json()["error"] == "invalid_redirect_uri"


@pytest.mark.asyncio
@pytest.mark.parametrize("uri", [
    "http://localhost:19876/callback",
    "http://[::1]:19876/callback",
])
async def test_loopback_rejects_localhost_and_ipv6(client_factory, uri):
    """Weder `localhost` noch `[::1]`: der gemessene opencode-DCR nutzt `127.0.0.1` (V209), und
    eine CSP-Host-Quelle kann kein IPv6-Literal ausdruecken (V210)."""
    async with client_factory() as client:
        resp = await client.post("/oauth/register", json={"redirect_uris": [uri]})
    assert resp.status_code == 400
    assert resp.json()["error"] == "invalid_redirect_uri"


@pytest.mark.asyncio
@pytest.mark.parametrize("uri", [
    "http://user@127.0.0.1:19876/callback",
    "http://user:pw@127.0.0.1:19876/callback",
    "http://127.0.0.1:19876/callback?code=1",
    "http://127.0.0.1:19876/callback#fragment",
])
async def test_loopback_rejects_query_fragment_userinfo(client_factory, uri):
    async with client_factory() as client:
        resp = await client.post("/oauth/register", json={"redirect_uris": [uri]})
    assert resp.status_code == 400
    assert resp.json()["error"] == "invalid_redirect_uri"


@pytest.mark.asyncio
async def test_loopback_rejects_malformed_uri_without_a_server_error(client_factory):
    """Kaputte URI (`[::1` ohne schliessende Klammer) — `urlsplit()` wirft `ValueError`. Das muss
    eine **Ablehnung** sein (400), kein 500er: `register_client()` faengt nur `DCRError`."""
    async with client_factory() as client:
        resp = await client.post("/oauth/register", json={"redirect_uris": ["http://[::1:19876/cb"]})
    assert resp.status_code == 400
    assert resp.json()["error"] == "invalid_redirect_uri"


def test_https_rules_unchanged(tmp_path):
    """Der https-Zweig ist unveraendert: exakter Origin-Vergleich gegen die Allowlist, kein
    Port- und kein Pfadvergleich. `https://127.0.0.1:19876` ist **nicht** automatisch erlaubt —
    das entscheidet die Allowlist, wie vor P10.5 Block 6."""
    settings = AuthSettings(base_url="https://space.example.ts.net", db_path=tmp_path / "a.sqlite3")
    assert redirect_uri_allowed(CLAUDE_REDIRECT_URI, settings) is True
    assert redirect_uri_allowed("https://evil.example/callback", settings) is False
    assert redirect_uri_allowed("https://127.0.0.1:19876/callback", settings) is False

    with_loopback = AuthSettings(
        base_url="https://space.example.ts.net",
        db_path=tmp_path / "b.sqlite3",
        allowed_redirect_origins=("https://127.0.0.1:19876",),
    )
    assert redirect_uri_allowed("https://127.0.0.1:19876/callback", with_loopback) is True


@pytest.mark.asyncio
async def test_register_returns_no_client_secret(client_factory):
    async with client_factory() as client:
        resp = await client.post("/oauth/register", json={"redirect_uris": [CLAUDE_REDIRECT_URI]})
    body = resp.json()
    assert "client_secret" not in body
    assert body["token_endpoint_auth_method"] == "none"


@pytest.mark.asyncio
async def test_register_requires_json_content_type(client_factory):
    async with client_factory() as client:
        resp = await client.post(
            "/oauth/register",
            content=f"redirect_uris={CLAUDE_REDIRECT_URI}".encode(),
            headers={"content-type": "application/x-www-form-urlencoded"},
        )
    assert resp.status_code == 400
    assert resp.json()["error"] == "invalid_client_metadata"


@pytest.mark.asyncio
async def test_register_rejected_content_type_does_not_consume_rate_limit(client_factory):
    """Pinnt eine bewusste Reihenfolge-Entscheidung: der Content-Type-Check läuft VOR der
    Registrierungsbremse, verbraucht also kein Kontingent. Ohne diesen Test könnte eine spätere
    "Vereinfachung" (Bremse zuerst, ist billiger) das stillschweigend umdrehen."""
    async with client_factory() as client:
        for _ in range(MAX_REGISTRATIONS_PER_WINDOW):
            resp = await client.post(
                "/oauth/register",
                content=f"redirect_uris={CLAUDE_REDIRECT_URI}".encode(),
                headers={"content-type": "application/x-www-form-urlencoded"},
            )
            assert resp.status_code == 400
        # Kontingent wäre nach MAX_REGISTRATIONS_PER_WINDOW abgelehnten Versuchen aufgebraucht,
        # hätten sie mitgezählt — eine gültige Registrierung muss trotzdem noch durchgehen.
        resp = await client.post("/oauth/register", json={"redirect_uris": [CLAUDE_REDIRECT_URI]})
    assert resp.status_code == 201


@pytest.mark.asyncio
async def test_register_is_rate_limited(client_factory):
    async with client_factory() as client:
        for _ in range(MAX_REGISTRATIONS_PER_WINDOW):
            resp = await client.post(
                "/oauth/register", json={"redirect_uris": [CLAUDE_REDIRECT_URI]}
            )
            assert resp.status_code == 201
        resp = await client.post("/oauth/register", json={"redirect_uris": [CLAUDE_REDIRECT_URI]})
    assert resp.status_code == 429


def test_redirect_uri_allowed_is_the_only_matching_path():
    """Plan §2.6 [SEAM]: `redirect_uri_allowed()` muss die einzige Stelle bleiben, die eine
    Redirect-URI gegen `allowed_redirect_origins` vergleicht. Grep, nicht Verhalten — ein
    Verhaltenstest würde nur beweisen, dass die Funktion tut, was sie tut, nicht dass sie die
    einzige ist, die es tut.
    """
    authserver_dir = Path(__file__).resolve().parent.parent / "authserver"
    allowed_files = {"config.py", "clients.py"}
    offenders = [
        path.name
        for path in sorted(authserver_dir.glob("*.py"))
        if path.name not in allowed_files
        and "allowed_redirect_origins" in path.read_text(encoding="utf-8")
    ]
    assert offenders == [], (
        f"'allowed_redirect_origins' taucht außerhalb config.py/clients.py auf: {offenders} — "
        "Plan §2.6 [SEAM]: redirect_uri_allowed() muss die einzige Vergleichsstelle bleiben."
    )
