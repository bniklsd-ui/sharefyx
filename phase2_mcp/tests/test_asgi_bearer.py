"""`BearerAuthASGI` (Plan §3.1, P4 Step 6a) — isoliert, kein echter Port, kein echter HTTP-Server
für die reinen ASGI-Tests; ein echter `httpx.ASGITransport`-Stack für die Integrationstests unten.

`test_guard_rejects_principal_from_other_request` gehört hier statt in `test_context.py`, weil
er die Kernbehauptung dieses Steps beweist: `context.py::assert_principal_matches_request()`
brauchte für den neuen Bearer-Weg KEINE Änderung, obwohl Plan §3.2 eine ankündigt (siehe
`asgi.py`-Moduldocstring) — beide ASGI-Schichten setzen denselben `scope['state']['token_hash']`
mit derselben `sha256`-Funktion.

**Schnitt, 2026-07-30 (Runbook-Schritt 8):** `TokenPathASGI`/`AuthModeASGI` sind entfernt, beide
Pfad-Token live widerrufen. Entfernt aus dieser Datei: `_FakePathResolver`,
`test_auth_mode_token_preserves_p2_behaviour`, `test_auth_mode_both_serves_bearer_and_path`,
`test_default_auth_mode_is_oauth` (testete nur noch, dass ein P2-Pfad-Token unter Bearer-Auth
401 bekommt — nach der Entfernung trivial wahr, kein eigenständiger Fund mehr) und
`test_six_tools_behave_identically_under_bearer_and_path_token` (Plan §5 Step 6, dritte
Done-when-Klausel — bewies, dass die sechs Tools unter Bearer und Pfad-Token identisch
antworten; mit dem Wegfall des Pfad-Tokens gibt es keine zweite Seite mehr, mit der zu
vergleichen wäre). Bewusst dokumentiert, nicht kommentarlos verschwunden — Details:
`phase4_auth/CLAUDE.md`, Session-Block Schnitt.
"""
from __future__ import annotations

import json
from datetime import datetime, timedelta, timezone

import httpx
import pytest
from fastmcp import Client
from fastmcp.client.transports import StreamableHttpTransport

from authserver.config import AuthSettings
from authserver.resolver import OAuthTokenResolver, ResolveError, ResolvedPrincipal
from authserver.store import AuthStore
from mcpserver import context
from mcpserver.app import OAuthConfig, create_app
from mcpserver.asgi import BearerAuthASGI
from mcpserver.auth import AuthError
from mcpserver.config import Settings
from storage.store import Store

CHALLENGE = (
    'Bearer error="invalid_token", error_description="Authentication required", '
    'resource_metadata="https://space.example.ts.net/.well-known/oauth-protected-resource/mcp", '
    'scope="space"'
)


class _FakeOAuthResolver:
    def __init__(self, mapping: dict[str, ResolvedPrincipal]) -> None:
        self._mapping = mapping

    def resolve(self, credential: str) -> ResolvedPrincipal:
        result = self._mapping.get(credential)
        if result is None:
            raise ResolveError("unbekannt")
        return result


def _http_scope(path: str, *, authorization: str | None = None) -> dict:
    headers = []
    if authorization is not None:
        headers.append((b"authorization", authorization.encode("utf-8")))
    return {
        "type": "http",
        "method": "POST",
        "path": path,
        "raw_path": path.encode("utf-8"),
        "root_path": "",
        "headers": headers,
        "query_string": b"",
    }


async def _run(app, scope) -> list[dict]:
    sent: list[dict] = []

    async def receive():
        return {"type": "http.request", "body": b"", "more_body": False}

    async def send(message):
        sent.append(message)

    await app(scope, receive, send)
    return sent


def _headers(sent: list[dict]) -> dict[bytes, bytes]:
    return dict(sent[0]["headers"])


@pytest.fixture
def clock():
    state = {"now": datetime(2026, 7, 28, 12, 0, 0, tzinfo=timezone.utc)}

    def now_fn():
        return state["now"]

    def advance(seconds=1):
        state["now"] += timedelta(seconds=seconds)

    now_fn.advance = advance
    return now_fn


@pytest.fixture
def store(tmp_path, clock):
    return AuthStore(tmp_path / "auth.sqlite3", now_fn=clock)


@pytest.fixture
def resolver(store):
    return OAuthTokenResolver(store)


def _issue_token(store, *, space="niklas", access_ttl_s=3600):
    family_id = store.create_family(
        space=space, client_id="c1", scope="space", resource="https://x/mcp"
    )
    access_token, _refresh = store.issue_token_pair(
        family_id, access_ttl_s=access_ttl_s, refresh_ttl_s=2592000
    )
    return access_token, family_id


# -- BearerAuthASGI ---------------------------------------------------------------------


@pytest.mark.asyncio
async def test_missing_authorization_header_returns_401_with_challenge():
    async def inner(scope, receive, send):
        raise AssertionError("darf ohne Authorization-Header nie aufgerufen werden")

    app = BearerAuthASGI(inner, resolver=_FakeOAuthResolver({}), challenge=CHALLENGE)
    sent = await _run(app, _http_scope("/"))

    assert sent[0]["status"] == 401
    assert _headers(sent)[b"www-authenticate"] == CHALLENGE.encode("utf-8")
    assert sent[-1]["body"] == b""


@pytest.mark.asyncio
async def test_challenge_contains_resource_metadata_and_scope():
    async def inner(scope, receive, send):
        raise AssertionError("darf nie aufgerufen werden")

    app = BearerAuthASGI(inner, resolver=_FakeOAuthResolver({}), challenge=CHALLENGE)
    sent = await _run(app, _http_scope("/"))

    header = _headers(sent)[b"www-authenticate"].decode("utf-8")
    assert (
        'resource_metadata="https://space.example.ts.net/.well-known/oauth-protected-resource/mcp"'
        in header
    )
    assert 'scope="space"' in header


@pytest.mark.asyncio
async def test_non_bearer_scheme_is_rejected():
    async def inner(scope, receive, send):
        raise AssertionError("darf bei falschem Schema nie aufgerufen werden")

    app = BearerAuthASGI(inner, resolver=_FakeOAuthResolver({}), challenge=CHALLENGE)
    sent = await _run(app, _http_scope("/", authorization="Basic dXNlcjpwYXNz"))

    assert sent[0]["status"] == 401


@pytest.mark.asyncio
async def test_unknown_bearer_returns_401_without_detail():
    async def inner(scope, receive, send):
        raise AssertionError("darf bei unbekanntem Token nie aufgerufen werden")

    app = BearerAuthASGI(inner, resolver=_FakeOAuthResolver({}), challenge=CHALLENGE)
    sent = await _run(app, _http_scope("/", authorization="Bearer not-a-real-token"))

    assert sent[0]["status"] == 401
    assert sent[-1]["body"] == b""


@pytest.mark.asyncio
async def test_expired_token_returns_401(store, resolver, clock):
    token, _family_id = _issue_token(store, access_ttl_s=1)
    clock.advance(2)

    async def inner(scope, receive, send):
        raise AssertionError("darf bei abgelaufenem Token nie aufgerufen werden")

    app = BearerAuthASGI(inner, resolver=resolver, challenge=CHALLENGE)
    sent = await _run(app, _http_scope("/", authorization=f"Bearer {token}"))

    assert sent[0]["status"] == 401


@pytest.mark.asyncio
async def test_revoked_family_token_returns_401(store, resolver):
    token, family_id = _issue_token(store)
    store.revoke_family(family_id, "code_replay")

    async def inner(scope, receive, send):
        raise AssertionError("darf bei widerrufener Familie nie aufgerufen werden")

    app = BearerAuthASGI(inner, resolver=resolver, challenge=CHALLENGE)
    sent = await _run(app, _http_scope("/", authorization=f"Bearer {token}"))

    assert sent[0]["status"] == 401


@pytest.mark.asyncio
async def test_valid_bearer_sets_principal_space(store, resolver):
    token, _family_id = _issue_token(store, space="niklas")
    seen: dict = {}

    async def inner(scope, receive, send):
        seen["principal"] = context.current_principal()
        seen["state_hash"] = scope["state"]["token_hash"]
        await send({"type": "http.response.start", "status": 200, "headers": []})
        await send({"type": "http.response.body", "body": b""})

    app = BearerAuthASGI(inner, resolver=resolver, challenge=CHALLENGE)
    await _run(app, _http_scope("/", authorization=f"Bearer {token}"))

    assert seen["principal"].space == "niklas"
    assert seen["state_hash"] == seen["principal"].token_hash
    with pytest.raises(AuthError):
        context.current_principal()


@pytest.mark.asyncio
async def test_guard_rejects_principal_from_other_request(monkeypatch, store, resolver):
    token, _family_id = _issue_token(store, space="niklas")
    seen: dict = {}

    class _FakeState:
        token_hash = "hash-von-einem-anderen-request"

    class _FakeRequest:
        state = _FakeState()

    monkeypatch.setattr(
        "fastmcp.server.dependencies.get_http_request", lambda: _FakeRequest()
    )

    async def inner(scope, receive, send):
        try:
            context.assert_principal_matches_request()
            seen["raised"] = False
        except AuthError:
            seen["raised"] = True
        await send({"type": "http.response.start", "status": 200, "headers": []})
        await send({"type": "http.response.body", "body": b""})

    app = BearerAuthASGI(inner, resolver=resolver, challenge=CHALLENGE)
    await _run(app, _http_scope("/", authorization=f"Bearer {token}"))

    assert seen["raised"] is True


# -- Verdrahtung über create_app() ---------------------------------------------------------


@pytest.mark.asyncio
async def test_bearer_token_reaches_a_real_tool_call(tmp_path):
    """Schließt Advisor-Fund 1: die Behauptung "context.py brauchte keine Änderung" wird bisher
    nur gegen ein Fake bewiesen (`test_valid_bearer_sets_principal_space`) bzw. gegen einen
    handgebauten Fake-Request (`test_guard_rejects_principal_from_other_request`) — keiner der
    beiden Tests lässt `scope['state']` tatsächlich durch die echte FastMCP-App bis zu
    `tools.py :: context.assert_principal_matches_request()` laufen. Hier läuft ein Bearer-Token
    durch den vollen Stack (`create_app()` → `BearerAuthASGI` → FastMCP → `list_spaces`) — wenn
    der Guard falsch läge, würde `AuthError` hier auftreten, nicht in einem Fake."""
    auth_settings = AuthSettings(
        base_url="https://space.example.ts.net", db_path=tmp_path / "auth.sqlite3"
    )
    auth_store = AuthStore(auth_settings.db_path, now_fn=lambda: datetime.now(timezone.utc))
    family_id = auth_store.create_family(
        space="alpha", client_id="c1", scope="space", resource=auth_settings.resource
    )
    access_token, _refresh = auth_store.issue_token_pair(
        family_id, access_ttl_s=3600, refresh_ttl_s=2592000
    )

    data_root = tmp_path / "data"
    data_root.mkdir()
    settings = Settings(data_root=data_root)
    store = Store(data_root, git=False)
    store.create("alpha", type="task", title="Alpha-Item")

    app = create_app(
        settings=settings,
        store=store,
        oauth=OAuthConfig(settings=auth_settings, store=auth_store, users={}),
    )

    transport = StreamableHttpTransport(
        url="http://testserver/mcp/",
        headers={"Authorization": f"Bearer {access_token}"},
        httpx_client_factory=lambda **kwargs: httpx.AsyncClient(
            transport=httpx.ASGITransport(app=app), base_url="http://testserver", **kwargs
        ),
    )

    async with app.router.lifespan_context(app):
        async with Client(transport) as client:
            result = await client.call_tool("list_spaces", {})

    spaces = {entry["name"] for entry in json.loads(result.data)}
    assert "alpha" in spaces


@pytest.mark.asyncio
async def test_trusted_host_middleware_protects_root_app_when_configured(tmp_path):
    """Schließt Advisor-Fund 2: `TrustedHostMiddleware` wurde bisher von keinem Test tatsächlich
    instanziiert. Prüft beide Seiten (erlaubter vs. fremder Host) UND dass `/health` — worauf P3s
    Disconnected-Runbook angewiesen ist — unter der Middleware weiter antwortet."""
    auth_settings = AuthSettings(
        base_url="https://space.example.ts.net", db_path=tmp_path / "auth.sqlite3"
    )
    auth_store = AuthStore(auth_settings.db_path, now_fn=lambda: datetime.now(timezone.utc))

    data_root = tmp_path / "data"
    data_root.mkdir()
    settings = Settings(data_root=data_root, allowed_hosts=("space.example.ts.net",))
    store = Store(data_root, git=False)

    app = create_app(
        settings=settings,
        store=store,
        oauth=OAuthConfig(settings=auth_settings, store=auth_store, users={}),
    )

    async with httpx.AsyncClient(
        transport=httpx.ASGITransport(app=app), base_url="http://testserver"
    ) as client:
        allowed = await client.get("/health", headers={"Host": "space.example.ts.net"})
        rejected = await client.get("/health", headers={"Host": "evil.example"})
        wellknown = await client.get(
            "/.well-known/oauth-protected-resource", headers={"Host": "space.example.ts.net"}
        )

    assert allowed.status_code == 200
    assert rejected.status_code == 400
    assert wellknown.status_code == 200
