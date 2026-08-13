"""`GET /ui/`, `GET /ui/static/{path}` (Plan §5 Step 6). Läuft gegen die echten, im Repo
geschifften `webui/static/*`-Dateien (kein `tmp`-Fixture-Verzeichnis) — das ist bewusst: ein
Test, der gegen eine Attrappe grünt, während die echte `app.html` ein Inline-`<script>` enthält,
wäre wertlos. `ui_settings`s `static_dir` (Default `webui/static/`) bleibt deshalb unverändert.
"""
from __future__ import annotations

import re

import httpx
import pytest
from starlette.applications import Starlette

from webui.config import DEFAULT_STATIC_DIR
from webui.routes_auth import ui_auth_routes
from webui.static_routes import _resolve_static_path, static_routes

BASE_URL = "https://space.example.ts.net"
SPACE = "niklas"
PASSWORD = "correct horse battery staple"

_CSRF_RE = re.compile(r'name="csrf" value="([^"]+)"')


def _client(app) -> httpx.AsyncClient:
    return httpx.AsyncClient(transport=httpx.ASGITransport(app=app), base_url=BASE_URL)


@pytest.fixture
def static_app(ui_settings, store, confirmed_users, sessions) -> Starlette:
    routes = ui_auth_routes(ui_settings, store, confirmed_users, sessions) + static_routes(
        ui_settings, sessions
    )
    return Starlette(routes=routes)


async def _login(client: httpx.AsyncClient, totp_code) -> None:
    response = await client.post(
        "/ui/login", data={"space": SPACE, "password": PASSWORD, "totp": totp_code()},
    )
    assert response.status_code == 200


def _font_filename() -> str:
    matches = list(DEFAULT_STATIC_DIR.glob("fonts/InterVariable-subset.*.woff2"))
    assert matches, "kein gebautes Font-Subset unter webui/static/fonts/ gefunden"
    return matches[0].name


@pytest.mark.asyncio
async def test_index_route_requires_session(static_app, totp_code):
    async with _client(static_app) as client:
        anonymous = await client.get("/ui/", follow_redirects=False)
        assert anonymous.status_code == 303
        assert anonymous.headers["location"] == "/ui/login"

        await _login(client, totp_code)
        authenticated = await client.get("/ui/", follow_redirects=False)
        assert authenticated.status_code == 200
        assert "text/html" in authenticated.headers["content-type"]
        assert "<html" in authenticated.text


@pytest.mark.asyncio
async def test_app_loads_as_a_single_es_module(static_app, totp_code):
    """Step 7: der frühere Zwei-Skript-Aufbau (`js/updates.js` als globales Skript VOR `app.js`,
    Ladereihenfolge-Pflicht wegen `window.SharefyxUpdates`) ist mit dem Split in ES-Module
    entfallen — `updates.js` ist jetzt selbst ein Modul, das `app.js` ganz normal per `import`
    lädt, kein globaler Name, keine Reihenfolge-Regel mehr nötig. Genau EIN `<script
    type="module">`-Tag, das den neuen Einstiegspunkt referenziert; kein altes Skript-Tag auf
    den entfernten Top-Level-Pfad `/ui/static/app.js` (jetzt `/ui/static/js/app.js`)."""
    async with _client(static_app) as client:
        await _login(client, totp_code)
        response = await client.get("/ui/")
    html = response.text
    script_tags = re.findall(r"<script\b[^>]*>", html)
    assert script_tags == ['<script type="module" src="/ui/static/js/app.js">']


_JS_MODULES = (
    "app", "api", "state", "tree", "list", "editor", "markdown", "dialogs", "toasts", "updates",
)


@pytest.mark.asyncio
async def test_static_files_are_served_with_correct_content_type(static_app):
    font_name = _font_filename()
    cases = {
        "app.html": "text/html",
        "app.css": "text/css",
        f"fonts/{font_name}": "font/woff2",
    }
    cases.update({f"js/{name}.js": "text/javascript" for name in _JS_MODULES})
    async with _client(static_app) as client:
        for path, expected in cases.items():
            response = await client.get(f"/ui/static/{path}")
            assert response.status_code == 200, path
            assert expected in response.headers["content-type"], path


@pytest.mark.asyncio
async def test_static_hashed_assets_get_immutable_cache_header(static_app):
    font_name = _font_filename()
    async with _client(static_app) as client:
        hashed = await client.get(f"/ui/static/fonts/{font_name}")
        assert "immutable" in hashed.headers["cache-control"]

        unhashed = await client.get("/ui/static/js/app.js")
        assert unhashed.headers["cache-control"] == "no-store"


def test_resolve_static_path_rejects_traversal():
    # Direkt gegen `_resolve_static_path()`, nicht über HTTP: `httpx`/ASGI-Server normalisieren
    # `../`-Segmente in der URL oft schon vor dem Routing weg — das würde eine echte Lücke im
    # eigenen Guard verdecken, statt sie zu belegen (das eigentliche Risiko ist ein Client, der
    # NICHT normalisiert).
    assert _resolve_static_path(DEFAULT_STATIC_DIR, "app.css") is not None
    assert _resolve_static_path(DEFAULT_STATIC_DIR, "../config.py") is None
    assert _resolve_static_path(DEFAULT_STATIC_DIR, "fonts/../../config.py") is None
    assert _resolve_static_path(DEFAULT_STATIC_DIR, "/etc/passwd") is None
    assert _resolve_static_path(DEFAULT_STATIC_DIR, "does-not-exist.css") is None


def test_app_html_contains_no_inline_script():
    html = (DEFAULT_STATIC_DIR / "app.html").read_text("utf-8")
    for match in re.finditer(r"<script\b[^>]*>", html):
        assert "src=" in match.group(0), f"Inline-<script> gefunden: {match.group(0)!r}"


def test_app_html_contains_no_inline_style_attribute():
    html = (DEFAULT_STATIC_DIR / "app.html").read_text("utf-8")
    assert "style=" not in html


def test_app_js_makes_no_external_requests():
    for name in _JS_MODULES:
        js = (DEFAULT_STATIC_DIR / "js" / f"{name}.js").read_text("utf-8")
        for needle in ("http://", "https://", "//cdn"):
            assert needle not in js, f"externe Referenz {needle!r} in js/{name}.js gefunden"


def test_write_controls_live_inside_detachable_containers():
    """Akzeptanzkriterium 12 verlangt bei einem fremden Space Schreib-Bedienelemente **nicht im
    DOM** — nicht bloß `hidden`. Bis Step 7b standen Editor, „+"-Knopf und Anlegen-Dialog
    permanent in `app.html` und waren nur ausgeblendet, also mit DevTools auffindbar; Step 7b
    hängt sie in `app.js :: detachable()` bei Bedarf aus dem Dokument aus.

    Dieser Test kann das Laufzeitverhalten nicht prüfen (JavaScript bleibt laut Plan
    unit-ungetestet, dafür lief die jsdom-Simulation). Er hält die Voraussetzung fest, auf der
    das Aushängen beruht: jedes Schreib-Bedienelement sitzt in genau einem der drei Container,
    die `state.js` aushängt (Step 7: aus `app.js` dorthin verschoben, `editorPart`/
    `createTriggers`/`createDialogPart` müssen von mehreren Modulen dieselbe Instanz teilen).
    Ein neuer Speichern-Knopf, den jemand außerhalb davon platziert, fällt hier auf statt erst
    live."""
    html = (DEFAULT_STATIC_DIR / "app.html").read_text("utf-8")
    js = (DEFAULT_STATIC_DIR / "js" / "state.js").read_text("utf-8")

    for container in ("detailEditorEl", "newItemButtonEl", "createButtonEl", "createDialogEl"):
        assert f"detachable({container})" in js, f"{container} wird nicht mehr ausgehängt"

    # Die Knöpfe, die schreiben, stehen im Editor-Teilbaum — geprüft über ihre Position im
    # Quelltext zwischen der öffnenden `#detail-editor`-Zeile und dem Anlegen-Dialog.
    editor_start = html.index('<div id="detail-editor"')
    editor_end = html.index('<div class="toast"')
    editor_markup = html[editor_start:editor_end]
    for control in ('id="save-button"', 'id="archive-button"', 'id="append-button"',
                    'id="editor-textarea"'):
        assert control in editor_markup, f"{control} liegt außerhalb von #detail-editor"
