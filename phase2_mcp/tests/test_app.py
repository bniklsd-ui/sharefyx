"""End-to-End-Tests gegen eine echte `create_app()`-Instanz — kein echter Port, kein Netz
(`httpx.ASGITransport`), kein Keyring (Fake-Resolver). Plan §4 Step 5.

`test_principal_isolation_under_concurrency` ist die wichtigste Zusicherung der Phase (Mission,
Plan §5 Punkt 4): zwei gleichzeitige Tool-Aufrufe mit zwei verschiedenen Tokens müssen zwei
verschiedene Spaces sehen. Fällt dieser Test, ist es ein Cross-Space-Leak, kein Testproblem.
"""
from __future__ import annotations

import asyncio
import json
from collections.abc import Callable

import httpx
import pytest
from fastmcp import Client
from fastmcp.client.transports import StreamableHttpTransport
from starlette.applications import Starlette

from mcpserver import __version__
from mcpserver.app import create_app
from mcpserver.auth import AuthError, Principal
from mcpserver.config import Settings
from storage.store import Store

# Bewusst keine Nikinger-typischen Spacenamen (Plan §2.2 Erweiterungspfad: "Space-Namen kommen
# in keinem Produktivcode und in keinem Test vor") — Fixture-Namen wie im Plan gefordert.
TOKEN_ALPHA = "tok-alpha"
TOKEN_BETA = "tok-beta"


class _FakeResolver:
    """Wie in `test_asgi.py` — kein echter Keyring, direkter Dict-Lookup über den Klartext-
    Credential-String (Step 5 testet TokenPathASGI, nicht KeyringTokenResolver erneut)."""

    def __init__(self, mapping: dict[str, Principal]) -> None:
        self._mapping = mapping

    def resolve(self, credential: str) -> Principal:
        principal = self._mapping.get(credential)
        if principal is None:
            raise AuthError("unbekannt")
        return principal


@pytest.fixture
def store(tmp_path) -> Store:
    s = Store(tmp_path, git=False)
    s.create("alpha", type="task", title="Alpha-Item")
    s.create("beta", type="task", title="Beta-Item")
    s.create("beta", type="note", title="Zweites Beta-Item")
    return s


@pytest.fixture
def resolver() -> _FakeResolver:
    return _FakeResolver(
        {
            TOKEN_ALPHA: Principal(space="alpha", token_hash="hash-alpha"),
            TOKEN_BETA: Principal(space="beta", token_hash="hash-beta"),
        }
    )


@pytest.fixture
def app(tmp_path, store, resolver) -> Starlette:
    settings = Settings(data_root=tmp_path)
    return create_app(settings=settings, resolver=resolver, store=store)


def _http_client_factory(app: Starlette) -> Callable[..., httpx.AsyncClient]:
    transport = httpx.ASGITransport(app=app)

    def factory(**kwargs) -> httpx.AsyncClient:
        return httpx.AsyncClient(transport=transport, base_url="http://testserver", **kwargs)

    return factory


def _mcp_client(app: Starlette, token: str) -> Client:
    transport = StreamableHttpTransport(
        url=f"http://testserver/mcp/{token}",
        httpx_client_factory=_http_client_factory(app),
    )
    return Client(transport)


@pytest.mark.asyncio
async def test_health_ok(app):
    async with httpx.AsyncClient(
        transport=httpx.ASGITransport(app=app), base_url="http://testserver"
    ) as client:
        response = await client.get("/health")

    assert response.status_code == 200
    body = response.json()
    # Exakte Schlüsselmenge statt nur Teilstring-Checks — fängt eine spätere Erweiterung um ein
    # zusätzliches Feld ab, nicht nur zufällig gewählte Weltnamen (Finding aus dem Advisor-Review).
    assert set(body.keys()) == {"status", "service", "version"}
    assert body == {"status": "ok", "service": "sharefyx-mcp", "version": __version__}


@pytest.mark.asyncio
async def test_health_leaks_no_space_names(app):
    async with httpx.AsyncClient(
        transport=httpx.ASGITransport(app=app), base_url="http://testserver"
    ) as client:
        response = await client.get("/health")

    body_text = response.text
    for leak in ("alpha", "beta", "item_count", "/mcp", "path"):
        assert leak not in body_text


@pytest.mark.asyncio
async def test_mcp_requires_token(app):
    async with httpx.AsyncClient(
        transport=httpx.ASGITransport(app=app), base_url="http://testserver"
    ) as client:
        missing = await client.post("/mcp/", json={})
        unknown = await client.post("/mcp/not-a-real-token", json={})

    assert missing.status_code == 401
    assert missing.text == ""
    assert unknown.status_code == 401
    assert unknown.text == ""


@pytest.mark.asyncio
async def test_mcp_bare_mount_redirects_without_leaking(app):
    """`POST /mcp` (ohne Trailing-Slash, kein Token-Segment überhaupt) trifft Starlettes eigenes
    `redirect_slashes` **vor** `TokenPathASGI` — das ist eine dritte, von 401 unterscheidbare
    Antwortform (307), aber sie sagt nichts über Tokengültigkeit aus (es gibt in diesem Request
    gar kein Token-Segment) und trägt keine Space- oder Pfaddaten. Festgehalten, damit dieses
    Verhalten nicht erst bei der Live-Probe überrascht (Advisor-Review, Step 5)."""
    async with httpx.AsyncClient(
        transport=httpx.ASGITransport(app=app),
        base_url="http://testserver",
        follow_redirects=False,
    ) as client:
        response = await client.post("/mcp", json={})

    assert response.status_code == 307
    assert response.text == ""
    assert response.headers["location"] == "http://testserver/mcp/"


@pytest.mark.asyncio
async def test_tools_list_returns_six_tools(app):
    async with app.router.lifespan_context(app):
        async with _mcp_client(app, TOKEN_ALPHA) as client:
            tools = await client.list_tools()

    names = {tool.name for tool in tools}
    assert names == {
        "list_spaces",
        "search_items",
        "get_item",
        "create_item",
        "update_item",
        "append_to_item",
    }


@pytest.mark.asyncio
async def test_tools_list_annotations_present(app):
    async with app.router.lifespan_context(app):
        async with _mcp_client(app, TOKEN_ALPHA) as client:
            tools = await client.list_tools()

    for tool in tools:
        assert tool.title, f"{tool.name} hat keinen Titel"
        assert tool.description, f"{tool.name} hat keine Beschreibung"
        assert tool.annotations is not None, f"{tool.name} hat keine Annotations"
        assert tool.annotations.readOnlyHint is not None
        assert tool.annotations.destructiveHint is not None
        assert tool.annotations.idempotentHint is not None
        assert tool.annotations.openWorldHint is not None


@pytest.mark.asyncio
async def test_principal_isolation_under_concurrency(app):
    """Der wichtigste Test der Phase (Plan §4 Step 5, §5 Punkt 4, Mission). Zehn verschachtelte
    Aufrufe über zwei Tokens via `asyncio.gather` — echte Nebenläufigkeit auf demselben Event-
    Loop, nicht zwei sequenzielle Aufrufe. Jeder Aufruf muss `writable` exakt für den eigenen
    Space sehen; ein Leck zeigt sich als `writable=True` für den fremden Space oder umgekehrt.
    """

    async def call(token: str) -> str:
        async with _mcp_client(app, token) as client:
            result = await client.call_tool("list_spaces", {})
            return result.data

    async with app.router.lifespan_context(app):
        calls = [
            call(TOKEN_ALPHA) if i % 2 == 0 else call(TOKEN_BETA) for i in range(10)
        ]
        results = await asyncio.gather(*calls)

    for i, raw in enumerate(results):
        payload = json.loads(raw)
        by_name = {entry["name"]: entry for entry in payload}
        own_space = "alpha" if i % 2 == 0 else "beta"
        foreign_space = "beta" if i % 2 == 0 else "alpha"
        assert by_name[own_space]["writable"] is True
        assert by_name[foreign_space]["writable"] is False


@pytest.mark.asyncio
async def test_all_six_tools_are_callable_over_http(app):
    """Step 6 Done-when: alle sechs Tools über den ASGI-Testclient aufrufbar — nicht nur als
    Python-Funktion (`test_tools.py`, Guard gemockt), sondern durch den echten Stack aus Step 5
    (`TokenPathASGI`, Guard, laufende FastMCP-App). Ein Rundlauf pro Tool reicht hier; die
    granulare Semantik (Wrapping, Klemmung, Fehlertexte) ist bereits in `test_tools.py`
    bewiesen.
    """
    async with app.router.lifespan_context(app):
        async with _mcp_client(app, TOKEN_ALPHA) as alpha, _mcp_client(app, TOKEN_BETA) as beta:
            spaces = json.loads((await alpha.call_tool("list_spaces", {})).data)
            assert {s["name"] for s in spaces} == {"alpha", "beta"}

            created_text = (
                await alpha.call_tool(
                    "create_item", {"type": "task", "title": "Über HTTP angelegt"}
                )
            ).data
            assert "space: alpha" in created_text
            new_id = created_text.splitlines()[1].split("id: ")[1].strip()

            search_payload = json.loads(
                (await alpha.call_tool("search_items", {"query": "HTTP"})).data
            )
            assert any(item["id"] == new_id for item in search_payload["items"])

            own_text = (await alpha.call_tool("get_item", {"item_id": new_id})).data
            assert "<untrusted_content" not in own_text

            foreign_text = (await beta.call_tool("get_item", {"item_id": new_id})).data
            assert "<untrusted_content" in foreign_text

            appended_text = (
                await alpha.call_tool(
                    "append_to_item", {"item_id": new_id, "version": 1, "text": "Angehängt."}
                )
            ).data
            assert "Angehängt." in appended_text

            conflict = await alpha.call_tool(
                "update_item",
                {"item_id": new_id, "version": 1, "title": "Veraltete Version"},
                raise_on_error=False,
            )
            assert conflict.is_error is True
            assert "conflict" in conflict.content[0].text

            archived_text = (
                await alpha.call_tool(
                    "update_item", {"item_id": new_id, "version": 2, "status": "archived"}
                )
            ).data
            assert "status: archived" in archived_text
