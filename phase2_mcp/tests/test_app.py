"""End-to-End-Tests gegen eine echte `create_app()`-Instanz — kein echter Port, kein Netz
(`httpx.ASGITransport`), keine echte, dauerhafte `AuthStore` (temporäre Datei je Test). Plan §4
Step 5.

`test_principal_isolation_under_concurrency` ist die wichtigste Zusicherung der Phase (Mission,
Plan §5 Punkt 4): zwei gleichzeitige Tool-Aufrufe mit zwei verschiedenen Tokens müssen zwei
verschiedene Spaces sehen. Fällt dieser Test, ist es ein Cross-Space-Leak, kein Testproblem.

**Schnitt, 2026-07-30 (Runbook-Schritt 8):** `TokenPathASGI`/`AuthModeASGI` sind entfernt,
`create_app()` verlangt jetzt immer ein `OAuthConfig`. Die beiden Fixture-Token (vormals feste
Strings `tok-alpha`/`tok-beta` im Pfad) entstehen seither als echte, opake OAuth-Access-Token
gegen eine temporäre `AuthStore` (`token_alpha`/`token_beta`-Fixtures) und reisen als
`Authorization: Bearer <token>`-Header, nicht mehr im Pfad.
"""
from __future__ import annotations

import asyncio
import json
from collections.abc import Callable
from contextlib import asynccontextmanager
from datetime import datetime, timezone

import httpx
import pytest
from fastmcp import Client
from fastmcp.client.transports import StreamableHttpTransport
from starlette.applications import Starlette
from starlette.responses import Response

from authserver.config import AuthSettings
from authserver.store import AuthStore
from authserver.userdir import UserDirectory

from mcpserver import __version__
from mcpserver.app import OAuthConfig, create_app
from mcpserver.config import Settings
from storage.store import Store

# Bewusst keine Nikinger-typischen Spacenamen (Plan §2.2 Erweiterungspfad: "Space-Namen kommen
# in keinem Produktivcode und in keinem Test vor") — Fixture-Namen wie im Plan gefordert.


@pytest.fixture
def store(tmp_path) -> Store:
    s = Store(tmp_path, git=False)
    s.create("alpha", type="task", title="Alpha-Item")
    s.create("beta", type="task", title="Beta-Item")
    s.create("beta", type="note", title="Zweites Beta-Item")
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


def _issue_bearer_token(auth_store: AuthStore, auth_settings: AuthSettings, *, space: str) -> str:
    family_id = auth_store.create_family(
        space=space, client_id="c1", scope="space", resource=auth_settings.resource
    )
    access_token, _refresh = auth_store.issue_token_pair(
        family_id, access_ttl_s=3600, refresh_ttl_s=2592000
    )
    return access_token


@pytest.fixture
def token_alpha(auth_store, auth_settings) -> str:
    return _issue_bearer_token(auth_store, auth_settings, space="alpha")


@pytest.fixture
def token_beta(auth_store, auth_settings) -> str:
    return _issue_bearer_token(auth_store, auth_settings, space="beta")


@pytest.fixture
def app(tmp_path, store, oauth) -> Starlette:
    settings = Settings(data_root=tmp_path)
    return create_app(settings=settings, store=store, oauth=oauth)


class _CapturingFastMCP:
    """Ersetzt `build_mcp()`'s Rückgabewert nur, um zu sehen, welcher `allowed_hosts`-Wert bei
    `http_app()` ankommt — P3-C testet die Präzedenz explizit vs. Settings, nicht FastMCP selbst."""

    def __init__(self) -> None:
        self.received_allowed_hosts: list[str] | None = "not-called"

    def add_middleware(self, middleware) -> None:
        pass

    def http_app(self, *, path, stateless_http, allowed_hosts):
        self.received_allowed_hosts = allowed_hosts

        @asynccontextmanager
        async def _lifespan(app):
            yield

        class _FakeMcpApp:
            lifespan = _lifespan

        return _FakeMcpApp()


def test_create_app_prefers_explicit_allowed_hosts_over_settings(monkeypatch, tmp_path, store, oauth):
    fake_mcp = _CapturingFastMCP()
    monkeypatch.setattr("mcpserver.app.build_mcp", lambda *a, **kw: fake_mcp)
    settings = Settings(data_root=tmp_path, allowed_hosts=("from-settings.example",))

    create_app(
        settings=settings,
        store=store,
        oauth=oauth,
        allowed_hosts=["explicit.example"],
    )

    assert fake_mcp.received_allowed_hosts == ["explicit.example"]


def test_create_app_uses_settings_allowed_hosts(monkeypatch, tmp_path, store, oauth):
    fake_mcp = _CapturingFastMCP()
    monkeypatch.setattr("mcpserver.app.build_mcp", lambda *a, **kw: fake_mcp)
    settings = Settings(data_root=tmp_path, allowed_hosts=("from-settings.example",))

    create_app(settings=settings, store=store, oauth=oauth, allowed_hosts=None)

    assert fake_mcp.received_allowed_hosts == ["from-settings.example"]


def _http_client_factory(app: Starlette) -> Callable[..., httpx.AsyncClient]:
    transport = httpx.ASGITransport(app=app)

    def factory(**kwargs) -> httpx.AsyncClient:
        return httpx.AsyncClient(transport=transport, base_url="http://testserver", **kwargs)

    return factory


def _mcp_client(app: Starlette, token: str) -> Client:
    transport = StreamableHttpTransport(
        url="http://testserver/mcp/",
        headers={"Authorization": f"Bearer {token}"},
        httpx_client_factory=_http_client_factory(app),
    )
    return Client(transport)


def test_create_app_mounts_ui_routes_without_import_cycle():
    """P5 Step 4 Nachtrag (siehe `mcpserver/app.py`s Moduldocstring): `mcpserver.app` importiert
    `webui.routes_auth`/`webui.account` — vorgezogen aus Step 5, damit Block As Live-Abnahme
    (Plan §6, Zeilen 1–9) überhaupt eine echte `/ui/login`/`/ui/invite/{token}` vorfindet. Das
    ist nur zyklenfrei, weil `mcpserver.permissions` (das einzige Symbol, das `webui` aus
    `mcpserver` ziehen darf, P5-B) selbst nichts aus `mcpserver.app` oder `webui` importiert.
    Grep statt Laufzeitprüfung. **[2026-08-05, P5 Step 5]:** `webui/api.py` existiert jetzt und
    importiert tatsächlich `mcpserver.permissions.OwnSpaceWritable` — genau der Fall, den dieser
    Test schon vorher als sicher belegt hatte (`mcpserver/permissions.py` importiert nichts aus
    `mcpserver.app`/`webui`, unverändert seit damals); die Vorhersage „existiert noch nicht" ist
    überholt, die Prämisse selbst weiterhin bewiesen."""
    import inspect

    import mcpserver.permissions as permissions_module

    source = inspect.getsource(permissions_module)
    assert "mcpserver.app" not in source
    assert "webui" not in source


@pytest.mark.asyncio
async def test_ui_login_reachable_through_create_app(app):
    """Live-Fund des Nikingers, 2026-08-03: `authctl.py invite` lieferte einen `/ui/invite/…`
    Link, aber der laufende Dienst kannte `/ui/*` gar nicht (`create_app()` mountete bis zu
    diesem Nachtrag nur `oauth_routes()`+`Mount("/mcp")`) — `404`. Dieser Test baut die reale
    `create_app()`-App (nicht `phase5_ui/tests`s eigenständige `Starlette(routes=ui_auth_routes(
    …))`-Testapp) und beweist, dass `/ui/login` darüber erreichbar ist — genau die Lücke, die
    live auffiel und in `phase5_ui/tests` nicht hätte auffallen können.

    Zusätzlich (Advisor-Fund vor dem Commit): `oauth_routes()` und `ui_auth_routes()` laufen jetzt
    in EINER Starlette-App — `security.py :: ui_security_headers()`s eigene, engere CSP
    (`form-action 'self'`) darf dabei nicht mit `authserver/routes.py`s OAuth-CSP
    (`form-action 'self' https://claude.ai https://claude.com`) verwechselt oder überschrieben
    werden. `phase5_ui/tests/test_security.py` bewies die Trennung bisher nur für die
    eigenständige Testapp — hier gegen den echten, zusammengesteckten Prozess."""
    async with httpx.AsyncClient(
        transport=httpx.ASGITransport(app=app), base_url="http://testserver"
    ) as client:
        response = await client.get("/ui/login")

    assert response.status_code == 200
    assert 'action="/ui/login"' in response.text
    csp = response.headers["content-security-policy"]
    assert "form-action 'self'" in csp
    assert "claude.ai" not in csp


@pytest.mark.asyncio
async def test_ui_invite_reachable_through_create_app(app, auth_store):
    """Gegenstück zum Live-Fund: ein über `AuthStore.create_invite()` (dieselbe Methode, die
    `authctl.py invite` aufruft) erzeugter Link muss über die reale App eine `200`-Einladeseite
    liefern, kein `404`."""
    token = auth_store.create_invite(space="alpha", purpose="initial", ttl_s=3600)

    async with httpx.AsyncClient(
        transport=httpx.ASGITransport(app=app), base_url="http://testserver"
    ) as client:
        response = await client.get(f"/ui/invite/{token}")

    assert response.status_code == 200


@pytest.mark.asyncio
async def test_ui_index_route_reachable_through_create_app(app, auth_store, auth_settings):
    """Step 6: `GET /ui/` (die echte App-Shell) muss über die reale `create_app()`-App
    erreichbar sein — ohne Sitzung ein `303` nach `/ui/login` (dieselbe Sitzungsprüfung wie
    `webui/static_routes.py`s eigene Tests, hier gegen den zusammengesteckten Prozess statt eine
    eigenständige Testapp), mit einer gültigen Sitzung `200` mit `app.html`-Inhalt."""
    from webui.config import COOKIE_NAME, UiSettings
    from webui.sessions import SessionManager

    async with httpx.AsyncClient(
        transport=httpx.ASGITransport(app=app), base_url=auth_settings.base_url,
    ) as client:
        anonymous = await client.get("/ui/", follow_redirects=False)
        assert anonymous.status_code == 303
        assert anonymous.headers["location"] == "/ui/login"

        ui_settings = UiSettings(base_url=auth_settings.base_url)
        ui_sessions = SessionManager(auth_store, settings=ui_settings)
        cookie_response = Response()
        ui_sessions.issue(cookie_response, space="alpha")
        session_id = cookie_response.headers["set-cookie"].split(";")[0].split("=", 1)[1]

        authenticated = await client.get(
            "/ui/", headers={"Cookie": f"{COOKIE_NAME}={session_id}"},
        )
    assert authenticated.status_code == 200
    assert "<html" in authenticated.text


@pytest.mark.asyncio
async def test_api_items_reachable_through_create_app(app, auth_store, auth_settings):
    """Gegenstück zu `test_ui_login_reachable_through_create_app`, für Step 5: `webui/api.py`
    wird über dieselbe `oauth.store`/`oauth.users`-Instanz gemountet, kein zweiter DB-Handle —
    ein Item, über die `store`-Fixture dieser Datei angelegt (`space="alpha"`), muss über die
    echte `create_app()`-App per Session-Cookie lesbar sein."""
    from webui.config import COOKIE_NAME, UiSettings
    from webui.sessions import SessionManager

    ui_settings = UiSettings(base_url=auth_settings.base_url)
    ui_sessions = SessionManager(auth_store, settings=ui_settings)
    cookie_response = Response()
    ui_sessions.issue(cookie_response, space="alpha")
    session_id = cookie_response.headers["set-cookie"].split(";")[0].split("=", 1)[1]

    async with httpx.AsyncClient(
        transport=httpx.ASGITransport(app=app), base_url=auth_settings.base_url,
    ) as client:
        response = await client.get(
            "/api/v1/items", params={"space": "alpha"},
            headers={"Cookie": f"{COOKIE_NAME}={session_id}"},
        )

    assert response.status_code == 200
    payload = response.json()
    assert payload["total"] == 1  # "alpha" hat laut `store`-Fixture oben genau ein Item
    assert payload["items"][0]["title"] == "Alpha-Item"


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
    # `uptime_s` kam in P3 Step 4 dazu (P3-I) — dieser Test hat die Erweiterung wie vorgesehen
    # rot gemeldet, statt sie stillschweigend durchzulassen.
    assert set(body.keys()) == {"status", "service", "version", "uptime_s"}
    assert body["status"] == "ok"
    assert body["service"] == "sharefyx-mcp"
    assert body["version"] == __version__
    assert isinstance(body["uptime_s"], int)
    assert body["uptime_s"] >= 0


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
        unknown = await client.post(
            "/mcp/", json={}, headers={"Authorization": "Bearer not-a-real-token"}
        )

    assert missing.status_code == 401
    assert missing.text == ""
    assert "WWW-Authenticate" in missing.headers
    assert unknown.status_code == 401
    assert unknown.text == ""
    assert "WWW-Authenticate" in unknown.headers


@pytest.mark.asyncio
async def test_mcp_bare_mount_redirects_without_leaking(app):
    """`POST /mcp` (ohne Trailing-Slash) trifft Starlettes eigenes `redirect_slashes` **vor**
    `BearerAuthASGI` — das ist eine dritte, von 401 unterscheidbare Antwortform (307), trägt aber
    keine Space- oder Pfaddaten. Festgehalten, damit dieses Verhalten nicht erst bei der
    Live-Probe überrascht (Advisor-Review, Step 5)."""
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
async def test_tools_list_returns_seven_tools(app, token_alpha):
    async with app.router.lifespan_context(app):
        async with _mcp_client(app, token_alpha) as client:
            tools = await client.list_tools()

    names = {tool.name for tool in tools}
    assert names == {
        "list_spaces",
        "search_items",
        "get_item",
        "create_item",
        "update_item",
        "append_to_item",
        "patch_item",
    }


@pytest.mark.asyncio
async def test_tools_list_annotations_present(app, token_alpha):
    async with app.router.lifespan_context(app):
        async with _mcp_client(app, token_alpha) as client:
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
async def test_principal_isolation_under_concurrency(app, token_alpha, token_beta):
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
            call(token_alpha) if i % 2 == 0 else call(token_beta) for i in range(10)
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
async def test_all_seven_tools_are_callable_over_http(app, token_alpha, token_beta):
    """Step 6 Done-when (P2), um `patch_item` erweitert (P6 Step 1): alle sieben Tools über den
    ASGI-Testclient aufrufbar — nicht nur als Python-Funktion (`test_tools.py`, Guard gemockt),
    sondern durch den echten Stack aus Step 5 (`BearerAuthASGI`, Guard, laufende FastMCP-App).
    Ein Rundlauf pro Tool reicht hier; die granulare Semantik (Wrapping, Klemmung, Fehlertexte,
    Quittungsformat) ist bereits in `test_tools.py` bewiesen — `create_item`/`append_to_item`/
    `update_item(status=archived)` benutzen hier bewusst `return_body=True`, damit die
    Inhaltsprüfungen unten (space/id/„Angehängt."/„status: archived") weiterhin gegen echten
    Dateitext laufen statt gegen die seit P6 Step 1 standardmäßige Quittung.
    """
    async with app.router.lifespan_context(app):
        async with _mcp_client(app, token_alpha) as alpha, _mcp_client(app, token_beta) as beta:
            spaces = json.loads((await alpha.call_tool("list_spaces", {})).data)
            assert {s["name"] for s in spaces} == {"alpha", "beta"}

            created_text = (
                await alpha.call_tool(
                    "create_item",
                    {"type": "task", "title": "Über HTTP angelegt", "return_body": True},
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
                    "append_to_item",
                    {
                        "item_id": new_id, "version": 1, "text": "Angehängt.",
                        "return_body": True,
                    },
                )
            ).data
            assert "Angehängt." in appended_text

            patched_receipt = json.loads(
                (
                    await alpha.call_tool(
                        "patch_item",
                        {
                            "item_id": new_id, "version": 2,
                            "edits": [{"old_text": "Angehängt.", "new_text": "Angehängt. Gepatcht."}],
                        },
                    )
                ).data
            )
            assert patched_receipt == {
                "op": "patch", "id": new_id, "space": "alpha", "title": "Über HTTP angelegt",
                "version": 3, "updated": patched_receipt["updated"],
                "replacements": 1, "lines": [1],
                "bytes": {"before": len("Angehängt.".encode()), "after": len("Angehängt. Gepatcht.".encode())},
            }

            conflict = await alpha.call_tool(
                "update_item",
                {"item_id": new_id, "version": 1, "title": "Veraltete Version"},
                raise_on_error=False,
            )
            assert conflict.is_error is True
            assert "conflict" in conflict.content[0].text

            archived_text = (
                await alpha.call_tool(
                    "update_item",
                    {
                        "item_id": new_id, "version": 3, "status": "archived",
                        "return_body": True,
                    },
                )
            ).data
            assert "status: archived" in archived_text
