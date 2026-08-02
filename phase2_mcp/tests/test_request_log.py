"""Tests für `mcpserver/request_log.py` (Plan §3, P3 Step 2).

`test_tool_event_never_contains_item_title` ist der wichtigste Test dieses Moduls (Plan §4
Step 2): er prüft eine Zusage — das Log ist Betriebsdaten, nie Inhalt —, keine Implementierung.

**Schnitt, 2026-07-30 (Runbook-Schritt 8):** die drei Tests, die über den `app`-Fixture einen
echten Tool-Aufruf fahren, benutzen seither einen echten Bearer-Token aus einer temporären
`AuthStore` statt eines Pfad-Token-Fakes (`TokenPathASGI` ist entfernt) — siehe `test_app.py` für
dasselbe Muster.
"""
from __future__ import annotations

import json
import logging
from datetime import datetime, timezone

import httpx
import pytest
from fastmcp import Client
from fastmcp.client.transports import StreamableHttpTransport
from starlette.applications import Starlette

from authserver.config import AuthSettings
from authserver.store import AuthStore
from authserver.userdir import UserDirectory

from mcpserver.app import OAuthConfig, create_app
from mcpserver.config import Settings
from mcpserver.request_log import (
    LOGGER_NAME,
    AccessLogASGI,
    JsonLineFormatter,
    OAuthLogASGI,
    ToolCallLogMiddleware,
    log_event,
)
from storage.store import Store


class _CapturingHandler(logging.Handler):
    """Sammelt die rohen `LogRecord`-Objekte des `sharefyx.request`-Loggers — `record.msg` ist
    das Feld-Dict aus `log_event()`, unformatiert."""

    def __init__(self) -> None:
        super().__init__()
        self.records: list[logging.LogRecord] = []

    def emit(self, record: logging.LogRecord) -> None:
        self.records.append(record)


@pytest.fixture
def request_log_handler():
    handler = _CapturingHandler()
    logger = logging.getLogger(LOGGER_NAME)
    logger.addHandler(handler)
    logger.setLevel(logging.INFO)
    previous_propagate = logger.propagate
    logger.propagate = False
    try:
        yield handler
    finally:
        logger.removeHandler(handler)
        logger.propagate = previous_propagate


@pytest.fixture
def store(tmp_path) -> Store:
    s = Store(tmp_path, git=False)
    s.create("alpha", type="task", title="Alpha-Item")
    return s


@pytest.fixture
def auth_settings(tmp_path) -> AuthSettings:
    return AuthSettings(
        base_url="https://space.example.ts.net", db_path=tmp_path / "auth.sqlite3"
    )


@pytest.fixture
def auth_store(auth_settings) -> AuthStore:
    return AuthStore(auth_settings.db_path, now_fn=lambda: datetime.now(timezone.utc))


@pytest.fixture
def oauth(auth_settings, auth_store) -> OAuthConfig:
    return OAuthConfig(
        settings=auth_settings, store=auth_store, users=UserDirectory(auth_store, dek=None)
    )


@pytest.fixture
def token_alpha(auth_store, auth_settings) -> str:
    family_id = auth_store.create_family(
        space="alpha", client_id="c1", scope="space", resource=auth_settings.resource
    )
    access_token, _refresh = auth_store.issue_token_pair(
        family_id, access_ttl_s=3600, refresh_ttl_s=2592000
    )
    return access_token


@pytest.fixture
def app(tmp_path, store, oauth) -> Starlette:
    settings = Settings(data_root=tmp_path)
    return create_app(settings=settings, store=store, oauth=oauth)


def _mcp_client(app: Starlette, token: str) -> Client:
    transport = StreamableHttpTransport(
        url="http://testserver/mcp/",
        headers={"Authorization": f"Bearer {token}"},
        httpx_client_factory=lambda **kwargs: httpx.AsyncClient(
            transport=httpx.ASGITransport(app=app), base_url="http://testserver", **kwargs
        ),
    )
    return Client(transport)


def _records_as_text(handler: _CapturingHandler) -> str:
    """Serialisiert alle gesammelten Records wie der echte Formatter — für Substring-Checks
    über den kompletten Logpuffer (Plan-Vorgabe für den Titel-Grep-Test)."""
    return "\n".join(JsonLineFormatter().format(r) for r in handler.records)


def test_json_line_is_valid_json(request_log_handler):
    log_event(ev="tool", tool="search_items", space="niklas", ms=5, ok=True)

    assert len(request_log_handler.records) == 1
    line = JsonLineFormatter().format(request_log_handler.records[0])
    payload = json.loads(line)
    assert payload["ev"] == "tool"
    assert payload["tool"] == "search_items"
    assert payload["space"] == "niklas"
    assert payload["ms"] == 5
    assert payload["ok"] is True


@pytest.mark.asyncio
async def test_tool_event_has_tool_space_and_duration(app, token_alpha, request_log_handler):
    async with app.router.lifespan_context(app):
        async with _mcp_client(app, token_alpha) as client:
            await client.call_tool("list_spaces", {})

    tool_events = [r.msg for r in request_log_handler.records if r.msg.get("ev") == "tool"]
    assert len(tool_events) == 1
    event = tool_events[0]
    assert event["tool"] == "list_spaces"
    assert event["space"] == "alpha"
    assert isinstance(event["ms"], int)
    assert event["ok"] is True
    assert "err" not in event


@pytest.mark.asyncio
async def test_tool_event_error_carries_class_not_message(app, token_alpha, request_log_handler):
    async with app.router.lifespan_context(app):
        async with _mcp_client(app, token_alpha) as client:
            created = json.loads((await client.call_tool("list_spaces", {})).data)
            assert created  # sanity: alpha existiert

            created_text = (
                await client.call_tool("create_item", {"type": "task", "title": "Für Konflikt"})
            ).data
            item_id = created_text.splitlines()[1].split("id: ")[1].strip()

            conflict = await client.call_tool(
                "update_item",
                {"item_id": item_id, "version": 999, "title": "Veraltete Version"},
                raise_on_error=False,
            )
            assert conflict.is_error is True

    tool_events = [r.msg for r in request_log_handler.records if r.msg.get("ev") == "tool"]
    conflict_events = [e for e in tool_events if e.get("tool") == "update_item"]
    assert len(conflict_events) == 1
    assert conflict_events[0]["ok"] is False
    assert conflict_events[0]["err"] == "conflict"

    # Die rohe Fehlermeldung (`map_storage_error()`-Text mit ID/Zeitstempel) darf nirgends im
    # Logpuffer stehen — nur die Klasse.
    full_text = _records_as_text(request_log_handler)
    assert "wurde geändert" not in full_text
    assert item_id not in full_text


@pytest.mark.asyncio
async def test_tool_event_never_contains_item_title(app, token_alpha, request_log_handler):
    marker = "ZZZ-MARKER-TITLE"

    async with app.router.lifespan_context(app):
        async with _mcp_client(app, token_alpha) as client:
            created_text = (
                await client.call_tool("create_item", {"type": "task", "title": marker})
            ).data
            item_id = created_text.splitlines()[1].split("id: ")[1].strip()

            await client.call_tool("list_spaces", {})
            await client.call_tool("search_items", {"query": marker})
            await client.call_tool("get_item", {"item_id": item_id})
            await client.call_tool(
                "append_to_item", {"item_id": item_id, "version": 1, "text": "Angehängt."}
            )
            await client.call_tool(
                "update_item", {"item_id": item_id, "version": 2, "status": "archived"}
            )

    tool_events = [r.msg for r in request_log_handler.records if r.msg.get("ev") == "tool"]
    # Beweist, dass das Log tatsächlich lief (sechs Aufrufe: create, list, search, get, append,
    # update) — sonst würde dieser Test identisch grün bleiben, wenn die Middleware gar nichts
    # loggt (Advisor-Fund: eine reine Abwesenheits-Assertion ist eine Tautologie ohne das hier).
    assert len(tool_events) == 6
    assert all(event.get("tool") for event in tool_events)

    full_text = _records_as_text(request_log_handler)
    assert marker not in full_text


@pytest.mark.asyncio
async def test_http_event_redacts_token_segment(request_log_handler):
    async def fake_app(scope, receive, send):
        await send({"type": "http.response.start", "status": 200, "headers": []})
        await send({"type": "http.response.body", "body": b""})

    wrapped = AccessLogASGI(fake_app)
    async with httpx.AsyncClient(
        transport=httpx.ASGITransport(app=wrapped), base_url="http://testserver"
    ) as client:
        await client.get("/mcp/supersecrettoken123")

    http_events = [r.msg for r in request_log_handler.records if r.msg.get("ev") == "http"]
    assert len(http_events) == 1
    assert http_events[0]["path"] == "/mcp/<redacted>"
    full_text = _records_as_text(request_log_handler)
    assert "supersecrettoken123" not in full_text


@pytest.mark.asyncio
async def test_http_event_logs_401_status(request_log_handler):
    async def unauthorized_app(scope, receive, send):
        await send({"type": "http.response.start", "status": 401, "headers": []})
        await send({"type": "http.response.body", "body": b""})

    wrapped = AccessLogASGI(unauthorized_app)
    async with httpx.AsyncClient(
        transport=httpx.ASGITransport(app=wrapped), base_url="http://testserver"
    ) as client:
        await client.post("/mcp/not-a-real-token", json={})

    http_events = [r.msg for r in request_log_handler.records if r.msg.get("ev") == "http"]
    assert len(http_events) == 1
    assert http_events[0]["status"] == 401
    assert http_events[0]["method"] == "POST"


async def _ok_app(scope, receive, send):
    await send({"type": "http.response.start", "status": 200, "headers": []})
    await send({"type": "http.response.body", "body": b""})


@pytest.mark.asyncio
async def test_oauth_events_carry_stage_and_duration(request_log_handler):
    """Plan §4/§5 Step 6: `ev="oauth"`-Zeilen tragen `stage` und `ms`. `client_id` nur bei
    `authorize_get` (Query-Parameter, kein Body-Read) — die anderen drei Routen bleiben ohne."""
    wrapped = OAuthLogASGI(_ok_app)
    async with httpx.AsyncClient(
        transport=httpx.ASGITransport(app=wrapped), base_url="http://testserver"
    ) as client:
        await client.get("/oauth/authorize", params={"client_id": "cli_abc123"})
        await client.post("/oauth/authorize", data={})
        await client.post("/oauth/register", json={})
        await client.post("/oauth/token", data={})

    oauth_events = [r.msg for r in request_log_handler.records if r.msg.get("ev") == "oauth"]
    by_stage = {e["stage"]: e for e in oauth_events}
    assert set(by_stage) == {"authorize_get", "authorize_post", "register", "token"}
    for event in oauth_events:
        assert isinstance(event["ms"], int)
        assert event["ok"] is True

    assert by_stage["authorize_get"]["client_id"] == "cli_abc123"
    for stage in ("authorize_post", "register", "token"):
        assert "client_id" not in by_stage[stage]
        assert "err" not in by_stage[stage]
        assert "grant" not in by_stage[stage]
        assert "space" not in by_stage[stage]


@pytest.mark.asyncio
async def test_oauth_log_skips_discovery_and_mcp_paths(request_log_handler):
    """`OAuthLogASGI` loggt ausschließlich `/oauth/*` — Discovery/`/health`/`/mcp` bleiben
    `AccessLogASGI`s alleinige `ev="http"`-Zeile, keine doppelte Protokollierung derselben
    Anfrage (Plan §4, Advisor-Vorgabe P4 Step 6b)."""
    wrapped = OAuthLogASGI(_ok_app)
    async with httpx.AsyncClient(
        transport=httpx.ASGITransport(app=wrapped), base_url="http://testserver"
    ) as client:
        await client.get("/.well-known/oauth-protected-resource")
        await client.get("/health")
        await client.post("/mcp/sometoken", json={})

    oauth_events = [r.msg for r in request_log_handler.records if r.msg.get("ev") == "oauth"]
    assert oauth_events == []


@pytest.mark.asyncio
async def test_oauth_log_reflects_error_status(request_log_handler):
    """`ok` ist HTTP-Status-Ebene (siehe `OAuthLogASGI`-Docstring) — ein 400 (z. B.
    `invalid_grant`) muss als `ok=False` erscheinen, ohne dass die Klasse dafür den Body liest."""

    async def _error_app(scope, receive, send):
        await send({"type": "http.response.start", "status": 400, "headers": []})
        await send({"type": "http.response.body", "body": b""})

    wrapped = OAuthLogASGI(_error_app)
    async with httpx.AsyncClient(
        transport=httpx.ASGITransport(app=wrapped), base_url="http://testserver"
    ) as client:
        await client.post("/oauth/token", data={})

    oauth_events = [r.msg for r in request_log_handler.records if r.msg.get("ev") == "oauth"]
    assert len(oauth_events) == 1
    assert oauth_events[0]["ok"] is False


@pytest.mark.asyncio
async def test_logging_failure_does_not_break_tool_call():
    class _BrokenHandler(logging.Handler):
        def emit(self, record: logging.LogRecord) -> None:
            raise RuntimeError("Handler kaputt")

    logger = logging.getLogger(LOGGER_NAME)
    handler = _BrokenHandler()
    logger.addHandler(handler)
    previous_propagate = logger.propagate
    logger.propagate = False
    try:

        class _FakeMessage:
            name = "some_tool"

        class _FakeContext:
            message = _FakeMessage()

        async def call_next(_context):
            return "tool-result"

        middleware = ToolCallLogMiddleware()
        result = await middleware.on_call_tool(_FakeContext(), call_next)

        assert result == "tool-result"
    finally:
        logger.removeHandler(handler)
        logger.propagate = previous_propagate


def test_request_logger_does_not_propagate_to_root():
    from mcpserver.logging_setup import configure_logging

    configure_logging("INFO")

    assert logging.getLogger(LOGGER_NAME).propagate is False
