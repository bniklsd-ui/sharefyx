"""`/api/v1/{me,spaces,items,...}` (Plan §3.1–§3.3, §5 Step 5) — gegen `api_app` (Login mintet
die Sitzung, die die Items-API braucht, wie `test_account.py` es für `/api/v1/account/*` schon
tut).

Zwei Tests laufen bewusst gegen einen `unittest.mock.MagicMock(spec=Store)`, nicht `item_store`:
`test_acl_of_is_called_before_permission_check` und
`test_patch_foreign_item_is_403_and_never_reaches_store`. Ein echter `Store` würde beide
Tests vacuous bestehen lassen — `SharePolicy.can_write_item` gibt für ein fremdes, ungeteiltes
Item `False` zurück, aber ohne den Spy sähe man nicht, dass `store.update()`/`get()` bei einer
Rechteverweigerung wirklich nie aufgerufen werden, nur dass die Antwort 403 ist. **P6 Step 5:**
beide Tests spionieren jetzt `store.acl_of()` statt `store.space_of()` — die Rechtereihenfolge
selbst (Store-Aufruf vor Rechteprüfung, Rechteprüfung vor jedem weiteren Store-Aufruf) ist
unverändert, nur die aufgelöste Größe (`AclDecision` statt ein roher Space-String)."""
from __future__ import annotations

import dataclasses
import re
from datetime import datetime, timezone
from unittest.mock import MagicMock

import httpx
import pytest
from starlette.applications import Starlette
from storage.acl import AclDecision
from storage.models import Item
from storage.store import Store

from webui.api import api_routes
from webui.routes_auth import ui_auth_routes

BASE_URL = "https://space.example.ts.net"
SPACE = "niklas"
FOREIGN_SPACE = "fabian"
PASSWORD = "correct horse battery staple"
NOW = datetime(2026, 8, 5, 12, 0, 0, tzinfo=timezone.utc)

_CSRF_RE = re.compile(r'name="csrf" value="([^"]+)"')


def _client(app) -> httpx.AsyncClient:
    return httpx.AsyncClient(transport=httpx.ASGITransport(app=app), base_url=BASE_URL)


async def _login(client: httpx.AsyncClient, totp_code) -> str:
    response = await client.post(
        "/ui/login", data={"space": SPACE, "password": PASSWORD, "totp": totp_code()},
    )
    assert response.status_code == 200
    return _CSRF_RE.search(response.text).group(1)


def _headers(csrf: str) -> dict[str, str]:
    return {"Origin": BASE_URL, "X-CSRF-Token": csrf}


# -- Items: Suche --------------------------------------------------------------------------


@pytest.mark.asyncio
async def test_items_search_maps_all_store_parameters(
    ui_settings, store, confirmed_users, sessions, permissions, totp_code
):
    """Filterparameter (`query`/`space`/`type`/`status`/`tag`/`due_before`) wandern unverändert
    an `Store.search()` — `limit`/`offset` NICHT direkt (siehe Moduldocstring `api.py`: Store
    kennt keine „sichtbaren Spaces", diese Datei paginiert nach dem Sichtbarkeitsfilter selbst,
    holt also bewusst mehr als der Client verlangt)."""
    mock_store = MagicMock(spec=Store)
    mock_store.search.return_value = MagicMock(items=[], total=0, limit=50, offset=0)
    mock_store.list_spaces.return_value = []
    app = Starlette(
        routes=ui_auth_routes(ui_settings, store, confirmed_users, sessions)
        + api_routes(ui_settings, mock_store, sessions, permissions, store)
    )
    async with _client(app) as client:
        await _login(client, totp_code)
        response = await client.get(
            "/api/v1/items",
            params={
                "query": "budget", "space": "niklas", "type": "task", "status": "open",
                "tag": "wichtig", "due_before": "2026-09-01",
            },
        )
    assert response.status_code == 200
    _, kwargs = mock_store.search.call_args
    assert kwargs["space"] == "niklas"
    assert kwargs["type"] == "task"
    assert kwargs["status"] == "open"
    assert kwargs["tag"] == "wichtig"
    assert kwargs["due_before"].isoformat() == "2026-09-01"
    assert mock_store.search.call_args[0][0] == "budget"


@pytest.mark.asyncio
async def test_items_search_limit_is_capped_at_200(full_app_items, totp_code):
    async with _client(full_app_items) as client:
        await _login(client, totp_code)
        response = await client.get("/api/v1/items", params={"limit": "9999"})
    assert response.status_code == 200
    assert response.json()["limit"] == 200


# -- Items: einzelnes lesen ------------------------------------------------------------------


@pytest.mark.asyncio
async def test_get_item_from_own_space_is_writable(full_app_items, item_store, totp_code):
    item = item_store.create(SPACE, type="note", title="Eigene Notiz")
    async with _client(full_app_items) as client:
        await _login(client, totp_code)
        response = await client.get(f"/api/v1/items/{item.id}")
    assert response.status_code == 200
    assert response.json()["readonly"] is False


@pytest.mark.asyncio
async def test_get_item_from_foreign_space_without_share_is_forbidden(
    full_app_items, item_store, totp_code
):
    """P6 Step 5: ohne jede Freigabe ist ein fremdes Item nicht mehr lesbar — anders als unter
    `OwnSpaceWritable`, wo jeder Space universell lesbar war (`readonly=True`, aber `200`)."""
    item = item_store.create(FOREIGN_SPACE, type="note", title="Fremde Notiz, ungeteilt")
    async with _client(full_app_items) as client:
        await _login(client, totp_code)
        response = await client.get(f"/api/v1/items/{item.id}")
    assert response.status_code == 403


@pytest.mark.asyncio
async def test_get_shared_item_from_foreign_space_is_readonly_true(
    full_app_items, item_store, totp_code
):
    item = item_store.create(FOREIGN_SPACE, type="note", title="Fremde Notiz, freigegeben")
    item_store.update(item.id, version=item.version, share_read=[SPACE])
    async with _client(full_app_items) as client:
        await _login(client, totp_code)
        response = await client.get(f"/api/v1/items/{item.id}")
    assert response.status_code == 200
    body = response.json()
    assert body["readonly"] is True
    assert body["shared"] is True


# -- Items: anlegen ---------------------------------------------------------------------------


@pytest.mark.asyncio
async def test_create_item_has_no_space_parameter(full_app_items, totp_code):
    """Ein mitgeschicktes `space`-Feld wird stillschweigend ignoriert — Rule 4 architektonisch
    (P5-A): der Ziel-Space ist immer die Sitzung, es gibt keinen Codepfad, der `body["space"]`
    je liest."""
    async with _client(full_app_items) as client:
        csrf = await _login(client, totp_code)
        response = await client.post(
            "/api/v1/items",
            json={"type": "note", "title": "Test", "space": FOREIGN_SPACE},
            headers=_headers(csrf),
        )
    assert response.status_code == 201
    assert response.json()["space"] == SPACE


@pytest.mark.asyncio
async def test_create_item_uses_session_space(full_app_items, totp_code, item_store):
    async with _client(full_app_items) as client:
        csrf = await _login(client, totp_code)
        response = await client.post(
            "/api/v1/items", json={"type": "note", "title": "Test"}, headers=_headers(csrf),
        )
    assert response.status_code == 201
    item_id = response.json()["id"]
    assert item_store.get(item_id).space == SPACE


@pytest.mark.asyncio
async def test_create_item_accepts_folder(full_app_items, totp_code, item_store):
    """K4 (`ITEM_MOVE_PLAN.md`): `_items_post`s Whitelist ließ `folder` bisher stillschweigend
    fallen, obwohl `create_item(folder=)` über MCP seit Step 6 funktioniert hat — Menschen konnten
    über die UI/API nicht in einen Ordner anlegen. `store.create()` validiert/slugifiziert
    `folder` selbst, kein zusätzlicher Check hier."""
    async with _client(full_app_items) as client:
        csrf = await _login(client, totp_code)
        response = await client.post(
            "/api/v1/items",
            json={"type": "note", "title": "Im Ordner", "folder": "Projekte"},
            headers=_headers(csrf),
        )
    assert response.status_code == 201
    assert response.json()["folder"] == "projekte"
    item_id = response.json()["id"]
    assert item_store.get(item_id).folder == "projekte"


# -- Items: PATCH, Rechte und Reihenfolge -----------------------------------------------------


@pytest.mark.asyncio
async def test_patch_foreign_item_is_403_and_never_reaches_store(
    ui_settings, store, confirmed_users, sessions, permissions, totp_code
):
    mock_store = MagicMock(spec=Store)
    mock_store.acl_of.return_value = AclDecision(
        space=FOREIGN_SPACE, folder="", visibility="private", read=frozenset(), write=frozenset(),
    )
    app = Starlette(
        routes=ui_auth_routes(ui_settings, store, confirmed_users, sessions)
        + api_routes(ui_settings, mock_store, sessions, permissions, store)
    )
    async with _client(app) as client:
        csrf = await _login(client, totp_code)
        response = await client.patch(
            "/api/v1/items/itm_deadbeef", json={"version": 1, "title": "x"}, headers=_headers(csrf),
        )
    assert response.status_code == 403
    mock_store.acl_of.assert_called_once_with("itm_deadbeef")
    mock_store.update.assert_not_called()
    mock_store.get.assert_not_called()


@pytest.mark.asyncio
async def test_acl_of_is_called_before_permission_check(
    ui_settings, store, confirmed_users, sessions, permissions, totp_code
):
    """Reihenfolge ist nicht verhandelbar (Plan §3.3): `acl_of()` (index-only) MUSS laufen,
    BEVOR `can_write_item()` entscheidet — sonst gäbe es keine Grundlage für die Rechteprüfung.
    Ein Aufrufreihenfolge-Test braucht einen Spy, ein echter `Store` kann diese Reihenfolge
    nicht unterscheidbar machen. **P6 Step 5:** ersetzt den vormaligen `space_of()`-Spion —
    dieselbe Reihenfolgenfrage, jetzt mit der item-level ACL statt dem rohen Space-String."""
    fake_item = Item(
        id="itm_deadbeef", space=SPACE, type="note", title="x", status="active", body="",
        due=None, tags=[], links=[], created=NOW, updated=NOW, version=2, extra={},
    )
    mock_store = MagicMock(spec=Store)
    call_order: list[str] = []
    own_acl = AclDecision(
        space=SPACE, folder="", visibility="private", read=frozenset(), write=frozenset(),
    )
    mock_store.acl_of.side_effect = lambda item_id: (call_order.append("acl_of"), own_acl)[1]
    mock_store.update.side_effect = lambda *a, **kw: (call_order.append("update"), fake_item)[1]
    app = Starlette(
        routes=ui_auth_routes(ui_settings, store, confirmed_users, sessions)
        + api_routes(ui_settings, mock_store, sessions, permissions, store)
    )
    async with _client(app) as client:
        csrf = await _login(client, totp_code)
        await client.patch(
            "/api/v1/items/itm_deadbeef", json={"version": 1, "title": "x"}, headers=_headers(csrf),
        )
    assert call_order == ["acl_of", "update"]


@pytest.mark.asyncio
async def test_version_mismatch_returns_409_with_current_item(full_app_items, item_store, totp_code):
    item = item_store.create(SPACE, type="note", title="Original")
    item_store.update(item.id, version=item.version, title="Geändert")  # v1 -> v2, extern

    async with _client(full_app_items) as client:
        csrf = await _login(client, totp_code)
        response = await client.patch(
            f"/api/v1/items/{item.id}", json={"version": item.version, "title": "Konflikt"},
            headers=_headers(csrf),
        )
    assert response.status_code == 409
    body = response.json()
    assert body["error"] == "conflict"
    assert body["detail"]["current"]["version"] == 2
    assert body["detail"]["current"]["title"] == "Geändert"


@pytest.mark.asyncio
async def test_conflict_response_current_item_matches_item_to_json_exactly(
    full_app_items, item_store, totp_code,
):
    """Step 7: geht über `test_version_mismatch_returns_409_with_current_item` hinaus — der
    Konfliktdialog (§4.5) rendert die „aktuelle Fassung" direkt aus `detail.current`, braucht
    also mehr als Version/Titel: `format`/`extra`/`readonly` müssen exakt wie bei einem normalen
    `item_to_json()`-Aufruf vorhanden sein, sonst müsste `app.js` für den Konfliktfall einen
    zweiten Roundtrip fahren."""
    item = item_store.create(SPACE, type="note", title="Original", body="Text", tags=["a"])
    external = item_store.update(item.id, version=item.version, title="Extern geändert")

    async with _client(full_app_items) as client:
        csrf = await _login(client, totp_code)
        response = await client.patch(
            f"/api/v1/items/{item.id}", json={"version": item.version, "title": "Konflikt"},
            headers=_headers(csrf),
        )
    assert response.status_code == 409
    current = response.json()["detail"]["current"]
    for key in ("id", "space", "type", "status", "body", "due", "tags", "links", "created",
                "updated", "version", "format", "extra", "readonly"):
        assert key in current, key
    assert current["version"] == external.version
    assert current["format"] == "markdown"
    assert current["readonly"] is False


@pytest.mark.asyncio
async def test_validation_error_returns_422(full_app_items, item_store, totp_code):
    item = item_store.create(SPACE, type="note", title="Original")
    async with _client(full_app_items) as client:
        csrf = await _login(client, totp_code)
        response = await client.patch(
            f"/api/v1/items/{item.id}", json={"version": item.version, "due": "kein-datum"},
            headers=_headers(csrf),
        )
    assert response.status_code == 422
    assert response.json()["error"] == "validation_failed"


@pytest.mark.asyncio
async def test_unknown_item_returns_404(full_app_items, totp_code):
    async with _client(full_app_items) as client:
        csrf = await _login(client, totp_code)
        response = await client.patch(
            "/api/v1/items/itm_ffffffff", json={"version": 1, "title": "x"}, headers=_headers(csrf),
        )
    assert response.status_code == 404
    assert response.json()["error"] == "not_found"


@pytest.mark.asyncio
async def test_archived_item_update_returns_422(full_app_items, item_store, totp_code):
    item = item_store.create(SPACE, type="note", title="Original")
    archived = item_store.archive(item.id, version=item.version)
    async with _client(full_app_items) as client:
        csrf = await _login(client, totp_code)
        response = await client.patch(
            f"/api/v1/items/{item.id}", json={"version": archived.version, "title": "x"},
            headers=_headers(csrf),
        )
    assert response.status_code == 422
    assert response.json()["error"] == "validation_failed"


# -- Format-Seam / Roundtrip (P5-Z) -----------------------------------------------------------


@pytest.mark.asyncio
async def test_extra_frontmatter_fields_survive_roundtrip(full_app_items, item_store, totp_code):
    item = item_store.create(SPACE, type="note", title="Original", **{"priority": "high"})
    async with _client(full_app_items) as client:
        csrf = await _login(client, totp_code)
        response = await client.patch(
            f"/api/v1/items/{item.id}", json={"version": item.version, "title": "Geändert"},
            headers=_headers(csrf),
        )
    assert response.status_code == 200
    assert response.json()["extra"]["priority"] == "high"


@pytest.mark.asyncio
async def test_format_field_defaults_to_markdown_and_roundtrips(full_app_items, totp_code):
    async with _client(full_app_items) as client:
        csrf = await _login(client, totp_code)
        default = await client.post(
            "/api/v1/items", json={"type": "note", "title": "A"}, headers=_headers(csrf),
        )
        assert default.json()["format"] == "markdown"

        explicit = await client.post(
            "/api/v1/items", json={"type": "note", "title": "B", "format": "plain"},
            headers=_headers(csrf),
        )
    assert explicit.json()["format"] == "plain"


# -- Sicherheit: kein HTML, Größenbegrenzung, Session-vs-Bearer, CSRF ------------------------


@pytest.mark.asyncio
async def test_no_html_appears_in_any_api_response(full_app_items, totp_code):
    raw_html = "<script>alert(1)</script> & <b>fett</b>"
    async with _client(full_app_items) as client:
        csrf = await _login(client, totp_code)
        response = await client.post(
            "/api/v1/items", json={"type": "note", "title": "T", "body": raw_html},
            headers=_headers(csrf),
        )
    assert response.status_code == 201
    assert response.headers["content-type"].startswith("application/json")
    assert response.json()["body"] == raw_html  # byte-identisch als Text, nicht gerendert (P5-Y)


@pytest.mark.asyncio
async def test_oversized_body_returns_413(full_app_items, totp_code):
    huge = "x" * (1024 * 1024 + 1)
    async with _client(full_app_items) as client:
        csrf = await _login(client, totp_code)
        response = await client.post(
            "/api/v1/items", json={"type": "note", "title": "T", "body": huge},
            headers=_headers(csrf),
        )
    assert response.status_code == 413
    assert response.json()["error"] == "payload_too_large"


@pytest.mark.asyncio
async def test_api_requires_session_not_bearer(full_app_items):
    """Wird in `phase2_mcp/tests/test_isolation.py` gegen die ECHTE `create_app()` geschärft
    (P5-F Richtung 2, Akzeptanzkriterium §6.19) — hier zusätzlich gegen die reine `webui`-Teilapp,
    ohne den vollen MCP-Stack aufzubauen."""
    async with _client(full_app_items) as client:
        response = await client.get(
            "/api/v1/items", headers={"Authorization": "Bearer irgendein-mcp-token"},
        )
    assert response.status_code == 401
    assert response.json()["error"] == "unauthenticated"


@pytest.mark.asyncio
async def test_api_write_requires_csrf(full_app_items, totp_code):
    async with _client(full_app_items) as client:
        await _login(client, totp_code)
        response = await client.post(
            "/api/v1/items", json={"type": "note", "title": "T"},
            headers={"Origin": BASE_URL},  # kein X-CSRF-Token
        )
    assert response.status_code == 403
    assert response.json()["error"] == "csrf_failed"


# -- Archivieren: eigener Fund (store.archive() hat keinen Schutz gegen doppeltes Archivieren) -


@pytest.mark.asyncio
async def test_archive_of_already_archived_item_returns_422(full_app_items, item_store, totp_code):
    item = item_store.create(SPACE, type="note", title="Original")
    archived = item_store.archive(item.id, version=item.version)
    async with _client(full_app_items) as client:
        csrf = await _login(client, totp_code)
        response = await client.post(
            f"/api/v1/items/{item.id}/archive", json={"version": archived.version},
            headers=_headers(csrf),
        )
    assert response.status_code == 422
    assert response.json()["error"] == "validation_failed"


@pytest.mark.asyncio
async def test_append_to_archived_item_returns_422(full_app_items, item_store, totp_code):
    item = item_store.create(SPACE, type="note", title="Original")
    archived = item_store.archive(item.id, version=item.version)
    async with _client(full_app_items) as client:
        csrf = await _login(client, totp_code)
        response = await client.post(
            f"/api/v1/items/{item.id}/append", json={"version": archived.version, "text": "x"},
            headers=_headers(csrf),
        )
    assert response.status_code == 422


@pytest.mark.asyncio
async def test_append_endpoint_concatenates_patch_endpoint_replaces(
    full_app_items, item_store, totp_code,
):
    """Step 7: `app.js` bildet „Notiz anhängen" auf `POST .../append` ab, nicht auf ein
    read-modify-write über `PATCH` — dieser Test beweist den Verhaltensunterschied, den diese
    UI-Entscheidung voraussetzt: `append` hängt an, `PATCH` mit einem `body`-Feld ersetzt
    vollständig."""
    appended = item_store.create(SPACE, type="note", title="A", body="Zeile eins")
    replaced = item_store.create(SPACE, type="note", title="B", body="Zeile eins")

    async with _client(full_app_items) as client:
        csrf = await _login(client, totp_code)
        append_response = await client.post(
            f"/api/v1/items/{appended.id}/append",
            json={"version": appended.version, "text": "Zeile zwei"},
            headers=_headers(csrf),
        )
        patch_response = await client.patch(
            f"/api/v1/items/{replaced.id}",
            json={"version": replaced.version, "body": "Zeile zwei"},
            headers=_headers(csrf),
        )

    assert append_response.json()["body"] == "Zeile eins\nZeile zwei"
    assert patch_response.json()["body"] == "Zeile zwei"


# -- /api/v1/me, /api/v1/spaces ----------------------------------------------------------------


@pytest.mark.asyncio
async def test_me_returns_session_space(full_app_items, totp_code):
    async with _client(full_app_items) as client:
        await _login(client, totp_code)
        response = await client.get("/api/v1/me")
    assert response.status_code == 200
    assert response.json()["space"] == SPACE


@pytest.mark.asyncio
async def test_spaces_marks_own_space(full_app_items, item_store, tmp_path, totp_code):
    """P6 Step 5: ein fremder Space ist nur noch sichtbar, wenn eine `.share.yml` das gewährt
    (`test_foreign_space_is_invisible_without_share`) — vorher war jeder Space über
    `OwnSpaceWritable.can_read` immer sichtbar. Diese `.share.yml` ist deshalb Teil des
    Fixtures, nicht optional: ohne sie würde `FOREIGN_SPACE` in der Antwort schlicht fehlen."""
    item_store.create(FOREIGN_SPACE, type="note", title="Fremd")
    (tmp_path / "data" / FOREIGN_SPACE / ".share.yml").write_text(
        f"read: [{SPACE}]\n", encoding="utf-8"
    )
    async with _client(full_app_items) as client:
        await _login(client, totp_code)
        response = await client.get("/api/v1/spaces")
    by_name = {s["name"]: s for s in response.json()}
    assert by_name[SPACE]["own"] is True
    assert by_name[FOREIGN_SPACE]["own"] is False
    assert by_name[SPACE]["writable"] is True
    assert by_name[FOREIGN_SPACE]["writable"] is False  # only "read:" granted, not "write:"


@pytest.mark.asyncio
async def test_spaces_reports_writable_for_a_shared_non_own_space(
    full_app_items, item_store, tmp_path, totp_code
):
    """Live-Fund 2026-08-13: `IT-Sekus-Projekt` war über MCP `writable:true`, aber die
    Web-UI zeigte "nur lesen" -- `_spaces()`/`space_to_json()` lieferten nie ein `writable`-
    Feld, nur `own`, und `app.js` badgte jeden nicht-eigenen Space hart als read-only. Ein
    Space mit einem `write:`-Grant (statt nur `read:`) muss `own: false, writable: true`
    liefern, nicht `own` und `writable` verwechseln."""
    item_store.create(FOREIGN_SPACE, type="note", title="Geteilt")
    (tmp_path / "data" / FOREIGN_SPACE / ".share.yml").write_text(
        f"write: [{SPACE}]\n", encoding="utf-8"
    )
    async with _client(full_app_items) as client:
        await _login(client, totp_code)
        response = await client.get("/api/v1/spaces")
    by_name = {s["name"]: s for s in response.json()}
    assert by_name[FOREIGN_SPACE]["own"] is False
    assert by_name[FOREIGN_SPACE]["writable"] is True


@pytest.mark.asyncio
async def test_spaces_omits_foreign_space_without_a_share(full_app_items, item_store, totp_code):
    """Neues Verhalten (P6 Step 5, P6-U): ein Space ohne `.share.yml` und ohne Mitgliedschaft
    ist für einen fremden Actor nicht mehr sichtbar — nicht nur nicht schreibbar."""
    item_store.create(FOREIGN_SPACE, type="note", title="Fremd, ungeteilt")
    async with _client(full_app_items) as client:
        await _login(client, totp_code)
        response = await client.get("/api/v1/spaces")
    assert FOREIGN_SPACE not in {s["name"] for s in response.json()}


# -- POST /api/v1/spaces/{space}/folders (Step 7 Commit 3, K4) ------------------------------


@pytest.mark.asyncio
async def test_create_folder_makes_an_empty_directory_visible_in_spaces(
    full_app_items, totp_code
):
    async with _client(full_app_items) as client:
        csrf = await _login(client, totp_code)
        create = await client.post(
            f"/api/v1/spaces/{SPACE}/folders", json={"folder": "Projekte"}, headers=_headers(csrf),
        )
        assert create.status_code == 201
        assert create.json() == {"folder": "projekte"}

        spaces = await client.get("/api/v1/spaces")
    own = next(s for s in spaces.json() if s["name"] == SPACE)
    assert "projekte" in own["folders"]


@pytest.mark.asyncio
async def test_create_folder_rejects_foreign_space_even_with_write_share(
    full_app_items, item_store, tmp_path, totp_code
):
    """Derselbe Eigentümer-Riegel wie `_items_patch`s `folder`-Feld (2026-08-12): ein
    `write:`-Grant erlaubt, einzelne Items zu ändern, aber keinen neuen, leeren Ordner in einem
    fremden Space anzulegen."""
    item_store.create(FOREIGN_SPACE, type="note", title="Fremd")
    (tmp_path / "data" / FOREIGN_SPACE / ".share.yml").write_text(
        f"write: [{SPACE}]\n", encoding="utf-8"
    )
    async with _client(full_app_items) as client:
        csrf = await _login(client, totp_code)
        response = await client.post(
            f"/api/v1/spaces/{FOREIGN_SPACE}/folders",
            json={"folder": "Projekte"}, headers=_headers(csrf),
        )
    assert response.status_code == 403


@pytest.mark.asyncio
async def test_create_folder_rejects_depth_over_max(full_app_items, totp_code):
    """Dünner Wrapper über `files.validate_folder()` — dessen eigene Traversal-/Tiefenlogik ist
    bereits in `phase1_storage/tests/test_files.py` getestet, hier nur die Fehlerweiterleitung."""
    async with _client(full_app_items) as client:
        csrf = await _login(client, totp_code)
        response = await client.post(
            f"/api/v1/spaces/{SPACE}/folders", json={"folder": "a/b/c"}, headers=_headers(csrf),
        )
    assert response.status_code == 422


@pytest.mark.asyncio
async def test_create_folder_rejects_reserved_name(full_app_items, totp_code):
    async with _client(full_app_items) as client:
        csrf = await _login(client, totp_code)
        response = await client.post(
            f"/api/v1/spaces/{SPACE}/folders", json={"folder": "_archive"}, headers=_headers(csrf),
        )
    assert response.status_code == 422


# -- /api/v1/updates (P6 Step 3) ----------------------------------------------------------------


@pytest.mark.asyncio
async def test_updates_get_reports_latest_and_unset_seen_state(
    ui_settings, store, confirmed_users, sessions, permissions, item_store, totp_code, tmp_path
):
    log_path = tmp_path / "UPDATE_LOG.md"
    log_path.write_text("## 2026-08-09\n- Erster Eintrag.\n", encoding="utf-8")
    settings = dataclasses.replace(ui_settings, update_log_path=log_path)
    app = Starlette(
        routes=ui_auth_routes(settings, store, confirmed_users, sessions)
        + api_routes(settings, item_store, sessions, permissions, store)
    )
    async with _client(app) as client:
        await _login(client, totp_code)
        response = await client.get("/api/v1/updates")
    assert response.status_code == 200
    body = response.json()
    assert body["entries"] == [
        {"id": "2026-08-09#1", "date": "2026-08-09", "lines": ["Erster Eintrag."]}
    ]
    assert body["latest_id"] == "2026-08-09#1"
    assert body["seen_update_id"] is None


@pytest.mark.asyncio
async def test_updates_seen_sets_latest_id_and_is_separated_per_space(
    ui_settings, store, confirmed_users, sessions, permissions, item_store, totp_code, tmp_path
):
    log_path = tmp_path / "UPDATE_LOG.md"
    log_path.write_text("## 2026-08-09\n- Eintrag.\n", encoding="utf-8")
    settings = dataclasses.replace(ui_settings, update_log_path=log_path)
    app = Starlette(
        routes=ui_auth_routes(settings, store, confirmed_users, sessions)
        + api_routes(settings, item_store, sessions, permissions, store)
    )
    async with _client(app) as client:
        csrf = await _login(client, totp_code)
        seen_response = await client.post("/api/v1/updates/seen", headers=_headers(csrf))
        assert seen_response.status_code == 200
        after = await client.get("/api/v1/updates")
    assert after.json()["seen_update_id"] == "2026-08-09#1"
    # Serverseitig berechnet, nicht clientseitig geschickt (Moduldocstring `api.py`) — UND pro
    # Space getrennt: ein anderer Nutzer bleibt vom Klick des ersten unberührt.
    assert store.get_seen_update_id(FOREIGN_SPACE) is None


def test_webui_imports_exactly_one_mcpserver_symbol():
    """§1.2/P5-B: `webui` darf genau ein Symbol aus `mcpserver` importieren
    (`permissions.SharePolicy`, seit P6 Step 5 — vorher `OwnSpaceWritable`). Geprüft über den
    echten Quelltext, nicht über eine Behauptung — jede `from mcpserver...`/`import
    mcpserver`-Zeile in `webui/*.py` wird gezählt. `Surface` bleibt bewusst außen vor
    (`SharePolicy.can_read_item_as_human()` kapselt es innerhalb von `mcpserver/permissions.py`
    — ein zweiter Name aus demselben Modul wäre trotzdem ein zweites Symbol)."""
    import ast
    from pathlib import Path

    webui_dir = Path(__file__).resolve().parent.parent / "webui"
    imported_symbols: set[str] = set()
    for path in webui_dir.glob("*.py"):
        tree = ast.parse(path.read_text(encoding="utf-8"), filename=str(path))
        for node in ast.walk(tree):
            if isinstance(node, ast.ImportFrom) and node.module and node.module.startswith("mcpserver"):
                for alias in node.names:
                    imported_symbols.add(f"{node.module}.{alias.name}")
            if isinstance(node, ast.Import):
                for alias in node.names:
                    if alias.name.startswith("mcpserver"):
                        imported_symbols.add(alias.name)
    assert imported_symbols == {"mcpserver.permissions.SharePolicy"}
