from datetime import datetime, timezone
from pathlib import Path

import httpx
import pytest
from starlette.applications import Starlette

from authserver.clients import MAX_REGISTRATIONS_PER_WINDOW
from authserver.config import AuthSettings
from authserver.routes import oauth_routes
from authserver.store import AuthStore

CLAUDE_REDIRECT_URI = "https://claude.ai/api/mcp/auth_callback"


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
    return Starlette(routes=oauth_routes(settings, store))


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
async def test_register_rejects_native_application_type(client_factory):
    async with client_factory() as client:
        resp = await client.post(
            "/oauth/register",
            json={"application_type": "native", "redirect_uris": [CLAUDE_REDIRECT_URI]},
        )
    assert resp.status_code == 400
    assert resp.json()["error"] == "invalid_client_metadata"


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
