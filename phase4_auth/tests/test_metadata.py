from datetime import datetime, timezone

import httpx
import pytest
from starlette.applications import Starlette

from authserver.config import AuthSettings
from authserver.metadata import authorization_server_metadata, protected_resource_metadata
from authserver.routes import oauth_routes
from authserver.store import AuthStore


@pytest.fixture
def settings(tmp_path):
    return AuthSettings(base_url="https://space.example.ts.net", db_path=tmp_path / "unused.sqlite3")


def test_prm_resource_equals_connector_url(settings):
    prm = protected_resource_metadata(settings)
    assert prm["resource"] == "https://space.example.ts.net/mcp"


def test_prm_lists_exactly_one_authorization_server(settings):
    prm = protected_resource_metadata(settings)
    assert prm["authorization_servers"] == ["https://space.example.ts.net"]


def test_as_metadata_advertises_s256_only(settings):
    meta = authorization_server_metadata(settings)
    assert meta["code_challenge_methods_supported"] == ["S256"]


def test_as_metadata_lists_offline_access(settings):
    meta = authorization_server_metadata(settings)
    assert "offline_access" in meta["scopes_supported"]


def test_as_metadata_has_no_cimd_flag(settings):
    meta = authorization_server_metadata(settings)
    assert "client_id_metadata_document_supported" not in meta


def test_as_metadata_sets_iss_parameter_flag(settings):
    meta = authorization_server_metadata(settings)
    assert meta["authorization_response_iss_parameter_supported"] is True


@pytest.fixture
def store(tmp_path):
    return AuthStore(
        tmp_path / "auth.sqlite3", now_fn=lambda: datetime(2026, 7, 28, 12, 0, 0, tzinfo=timezone.utc)
    )


@pytest.fixture
def app(settings, store):
    return Starlette(routes=oauth_routes(settings, store, {}))


@pytest.mark.asyncio
async def test_wellknown_paths_serve_identical_documents(app):
    """Beide Pfade sind in `routes.py` aktuell an dasselbe Handler-Funktionsobjekt gebunden,
    der Vergleich ist also nahezu tautologisch, solange das so bleibt. Der Test ist trotzdem
    kein Nichts: er ist der Regressions-Fang für den Tag, an dem jemand die beiden Routen auf
    zwei getrennte Handler aufteilt (z. B. um pfadabhängig zu reagieren) und dabei
    Byte-Gleichheit (Plan-Done-when: "byte-identische Dokumente") verliert. Bewusst
    `.content` (Rohbytes), nicht `.json()` — zwei geparste Dicts können gleich sein, obwohl die
    Serialisierung selbst abweicht (Key-Reihenfolge, Whitespace)."""
    async with httpx.AsyncClient(transport=httpx.ASGITransport(app=app), base_url="http://testserver") as client:
        r1 = await client.get("/.well-known/oauth-protected-resource")
        r2 = await client.get("/.well-known/oauth-protected-resource/mcp")
    assert r1.status_code == r2.status_code == 200
    assert r1.content == r2.content
