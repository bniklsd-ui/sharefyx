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
        + api_routes(ui_settings, mock_store, sessions, permissions, store, confirmed_users)
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


# -- Items: globaler Modus (GLOBAL_SEARCH_PLAN.md, P6-AO/AS) ----------------------------------


@pytest.mark.asyncio
async def test_items_without_space_param_returns_items_from_all_readable_spaces(
    full_app_items, item_store, totp_code,
):
    """P6-AO: `GET /api/v1/items` ohne `space`-Parameter ist bereits die globale, item-weise
    ACL-gefilterte Suche -- ein Item mit ausschliesslich item-level `share_read` (kein
    space-level Grant) muss darin erscheinen, obwohl der Space selbst unter `/spaces` nicht
    auftaucht (siehe `test_spaces_omits_foreign_space_without_a_share` direkt oberhalb)."""
    item = item_store.create(FOREIGN_SPACE, type="note", title="Nur item-level geteilt")
    item_store.update(item.id, version=item.version, share_read=[SPACE])
    async with _client(full_app_items) as client:
        await _login(client, totp_code)
        response = await client.get("/api/v1/items")
    assert response.status_code == 200
    ids = {row["id"] for row in response.json()["items"]}
    assert item.id in ids


@pytest.mark.asyncio
async def test_items_without_space_param_still_hides_unreadable_items(
    full_app_items, item_store, totp_code,
):
    """Fail-closed-Gegenprobe zum Test oberhalb: ein Item ganz ohne Freigabe bleibt im globalen
    Modus unsichtbar, genau wie beim bewussten Space-Wechsel."""
    item = item_store.create(FOREIGN_SPACE, type="note", title="Fremd, ungeteilt")
    async with _client(full_app_items) as client:
        await _login(client, totp_code)
        response = await client.get("/api/v1/items")
    ids = {row["id"] for row in response.json()["items"]}
    assert item.id not in ids


@pytest.mark.asyncio
async def test_global_items_omit_snippet_for_foreign_rows_but_keep_own(
    full_app_items, item_store, totp_code,
):
    """P6-AS, dem Geiste von Rule 4 nach: eine fremde Zeile im globalen Modus traegt keinen
    `snippet`-Schluessel, die eigene Zeile in derselben Antwort schon."""
    own = item_store.create(SPACE, type="note", title="Eigen")
    foreign = item_store.create(FOREIGN_SPACE, type="note", title="Fremd, geteilt")
    item_store.update(foreign.id, version=foreign.version, share_read=[SPACE])
    async with _client(full_app_items) as client:
        await _login(client, totp_code)
        response = await client.get("/api/v1/items")
    rows = {row["id"]: row for row in response.json()["items"]}
    assert "snippet" in rows[own.id]
    assert "snippet" not in rows[foreign.id]


@pytest.mark.asyncio
async def test_items_with_space_param_keeps_snippet_for_foreign_space(
    full_app_items, item_store, totp_code, tmp_path,
):
    """Der bewusste Space-Wechsel (`space`-Parameter gesetzt) bleibt unveraendert -- P6-AS
    schraenkt nur den neuen globalen Modus ein, nicht das bestehende Verhalten."""
    foreign = item_store.create(FOREIGN_SPACE, type="note", title="Fremder Space, sichtbar")
    (tmp_path / "data" / FOREIGN_SPACE / ".share.yml").write_text(
        f"read: [{SPACE}]\n", encoding="utf-8"
    )
    async with _client(full_app_items) as client:
        await _login(client, totp_code)
        response = await client.get(f"/api/v1/items?space={FOREIGN_SPACE}")
    rows = {row["id"]: row for row in response.json()["items"]}
    assert "snippet" in rows[foreign.id]


@pytest.mark.asyncio
async def test_get_single_item_shared_item_level_only_is_readable(
    full_app_items, item_store, totp_code,
):
    """Ein Treffer aus dem globalen Modus muss auch oeffenbar sein (heutiges Verhalten von
    `_items_get_one`, hier gegen kuenftige Regression gepinnt -- kein neuer Code in diesem
    Schnitt, siehe GLOBAL_SEARCH_PLAN.md Sec0.1)."""
    item = item_store.create(FOREIGN_SPACE, type="note", title="Item-level frei")
    item_store.update(item.id, version=item.version, share_read=[SPACE])
    async with _client(full_app_items) as client:
        await _login(client, totp_code)
        response = await client.get(f"/api/v1/items/{item.id}")
    assert response.status_code == 200


# -- Items: ID-Suche (P7-A1, P7-D/E) ------------------------------------------------------------


@pytest.mark.asyncio
async def test_items_get_finds_an_item_by_its_id(full_app_items, item_store, totp_code):
    item = item_store.create(SPACE, type="note", title="Findbar per ID")
    async with _client(full_app_items) as client:
        await _login(client, totp_code)
        response = await client.get("/api/v1/items", params={"query": item.id})
    assert response.status_code == 200
    ids = {row["id"] for row in response.json()["items"]}
    assert ids == {item.id}


@pytest.mark.asyncio
async def test_id_lookup_ignores_space_and_folder_filter(full_app_items, item_store, totp_code):
    item = item_store.create(SPACE, type="note", title="In einem Ordner")
    async with _client(full_app_items) as client:
        await _login(client, totp_code)
        response = await client.get(
            "/api/v1/items",
            params={"query": item.id, "space": FOREIGN_SPACE, "folder": "irgendwo"},
        )
    ids = {row["id"] for row in response.json()["items"]}
    assert item.id in ids


@pytest.mark.asyncio
async def test_id_lookup_respects_read_permission(full_app_items, item_store, totp_code):
    item = item_store.create(FOREIGN_SPACE, type="note", title="Fremd, ungeteilt")
    async with _client(full_app_items) as client:
        await _login(client, totp_code)
        response = await client.get("/api/v1/items", params={"query": item.id})
    assert response.status_code == 200
    assert response.json()["items"] == []
    assert response.json()["total"] == 0


@pytest.mark.asyncio
async def test_id_lookup_with_unknown_id_returns_empty_list(full_app_items, totp_code):
    async with _client(full_app_items) as client:
        await _login(client, totp_code)
        response = await client.get("/api/v1/items", params={"query": "itm_deadbeef"})
    assert response.status_code == 200
    assert response.json()["total"] == 0


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
        + api_routes(ui_settings, mock_store, sessions, permissions, store, confirmed_users)
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
    # Step 7 Commit 5a: `_items_patch` ruft jetzt zusätzlich `store.acl_reader.decision_for()`
    # für das Re-Auth-Gate — ein unkonfigurierter `MagicMock(spec=Store)` liefert dafür einen
    # generischen `MagicMock` zurück, dessen `>`-Vergleich mit TypeError scheitert (nachgeprüft,
    # nicht angenommen). Body ändert hier weder `folder`/`visibility`/`share_read`/`share_write`,
    # `before`==`after` ist also der korrekte, unveränderte Zustand — beide `decision_for()`-
    # Aufrufe bekommen deshalb denselben `own_acl` zurück, `widens()` bleibt `False`.
    mock_store.acl_reader.decision_for.return_value = own_acl
    mock_store.update.side_effect = lambda *a, **kw: (call_order.append("update"), fake_item)[1]
    app = Starlette(
        routes=ui_auth_routes(ui_settings, store, confirmed_users, sessions)
        + api_routes(ui_settings, mock_store, sessions, permissions, store, confirmed_users)
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
async def test_items_patch_rejects_an_unknown_field(full_app_items, item_store, totp_code, tmp_path):
    """O6: der exakte Fall aus `ITEM_MOVE_PLAN.md` Sec112 -- ein Tippfehler-Feld (`spce` statt
    `space`) wird an der API-Flaeche abgewiesen, die Datei bleibt unveraendert."""
    item = item_store.create(SPACE, type="note", title="Original")
    path = tmp_path / "data" / SPACE
    path = next(path.glob(f"{item.id}*.md"))
    before = path.read_text(encoding="utf-8")
    async with _client(full_app_items) as client:
        csrf = await _login(client, totp_code)
        response = await client.patch(
            f"/api/v1/items/{item.id}", json={"version": item.version, "spce": FOREIGN_SPACE},
            headers=_headers(csrf),
        )
    assert response.status_code == 422
    assert response.json()["error"] == "validation_failed"
    assert path.read_text(encoding="utf-8") == before


@pytest.mark.asyncio
async def test_items_patch_accepts_every_field_the_ui_sends(full_app_items, item_store, totp_code):
    """V74: pinnt die Whitelist gegen die real von editor.js/list.js/dialogs.js gesendeten
    Schluessel -- eine Obermenge ist Pflicht, sonst bricht das Speichern (siehe api.py ::
    _PATCH_FIELDS-Kommentar)."""
    from webui.api import _PATCH_FIELDS

    sent_by_ui = {
        "version", "title", "body", "status", "due", "tags", "links", "format",
        "folder", "space", "share_read", "share_write", "password", "totp",
    }
    assert sent_by_ui <= _PATCH_FIELDS


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


# -- Re-Auth-Gate bei rechte-erweiternden Freigabeänderungen (Step 7 Commit 5a, P6-N) ----------


@pytest.mark.asyncio
async def test_widening_share_write_without_credentials_returns_reauth_required(
    full_app_items, item_store, totp_code,
):
    item = item_store.create(SPACE, type="note", title="Original")
    async with _client(full_app_items) as client:
        csrf = await _login(client, totp_code)
        response = await client.patch(
            f"/api/v1/items/{item.id}",
            json={"version": item.version, "share_write": ["fabian"]},
            headers=_headers(csrf),
        )
    assert response.status_code == 403
    assert response.json()["error"] == "reauth_required"
    # Kein stiller Teil-Schreibvorgang -- die Version im Index ist unverändert.
    assert item_store.get(item.id).version == item.version


@pytest.mark.asyncio
async def test_widening_share_write_with_wrong_password_returns_reauth_required(
    full_app_items, item_store, totp_code,
):
    item = item_store.create(SPACE, type="note", title="Original")
    async with _client(full_app_items) as client:
        csrf = await _login(client, totp_code)
        response = await client.patch(
            f"/api/v1/items/{item.id}",
            json={
                "version": item.version, "share_write": ["fabian"],
                "password": "ganz falsches passwort", "totp": totp_code(),
            },
            headers=_headers(csrf),
        )
    assert response.status_code == 403
    assert response.json()["error"] == "reauth_required"
    assert item_store.get(item.id).version == item.version


@pytest.mark.asyncio
async def test_widening_share_write_with_correct_credentials_succeeds(
    full_app_items, item_store, totp_code, clock,
):
    item = item_store.create(SPACE, type="note", title="Original")
    async with _client(full_app_items) as client:
        csrf = await _login(client, totp_code)
        clock.advance(31)  # neues TOTP-Zeitfenster, sonst Replay-Ablehnung bei der Re-Auth
        response = await client.patch(
            f"/api/v1/items/{item.id}",
            json={
                "version": item.version, "share_write": ["fabian"],
                "password": PASSWORD, "totp": totp_code(),
            },
            headers=_headers(csrf),
        )
    assert response.status_code == 200
    body = response.json()
    assert body["share_write"] == ["fabian"]
    # `password`/`totp` dienten nur dem Gate -- landen nicht als Frontmatter-Feld auf der Platte
    # (Advisor-Fund vor diesem Commit: `store.update()`s `extra`-Zweig hat keine Whitelist).
    assert "password" not in body["extra"]
    assert "totp" not in body["extra"]
    on_disk = item_store.get(item.id)
    assert "password" not in on_disk.extra
    assert "totp" not in on_disk.extra


# -- Step 7b: PATCH mit space= (Cross-Space-Move, ITEM_MOVE_PLAN.md Sec4.3) -------------------


@pytest.mark.asyncio
async def test_patch_with_space_requires_reauth_when_target_widens_access(
    full_app_items, item_store, totp_code, tmp_path,
):
    (tmp_path / "data" / FOREIGN_SPACE).mkdir(parents=True)
    (tmp_path / "data" / FOREIGN_SPACE / ".share.yml").write_text(
        f"write: [{SPACE}]\n", encoding="utf-8"
    )
    item = item_store.create(SPACE, type="note", title="Umzug")
    async with _client(full_app_items) as client:
        csrf = await _login(client, totp_code)
        response = await client.patch(
            f"/api/v1/items/{item.id}",
            json={"version": item.version, "space": FOREIGN_SPACE},
            headers=_headers(csrf),
        )
    assert response.status_code == 403
    assert response.json()["error"] == "reauth_required"
    assert item_store.get(item.id).space == SPACE  # kein stiller Teil-Move


@pytest.mark.asyncio
async def test_patch_with_space_does_not_require_reauth_when_target_narrows(
    full_app_items, item_store, totp_code, tmp_path,
):
    # fabian gewaehrt niklas space-level Schreibrecht (fuer P6-AE noetig) -- das Item selbst
    # traegt kein eigenes share_write, effektives write/read kommt also nur aus diesem Grant.
    (tmp_path / "data" / SPACE).mkdir(parents=True)  # Ziel muss als Space existieren
    item = item_store.create(FOREIGN_SPACE, type="note", title="Zurueck")
    (tmp_path / "data" / FOREIGN_SPACE / ".share.yml").write_text(
        f"write: [{SPACE}]\n", encoding="utf-8"
    )
    async with _client(full_app_items) as client:
        csrf = await _login(client, totp_code)
        # Ziel ist niklas' EIGENER Space -- keine .share.yml dort, das Item verliert also den
        # fabian-Grant, effektives write/read schrumpft von {niklas} auf {} -- keine Erweiterung.
        response = await client.patch(
            f"/api/v1/items/{item.id}",
            json={"version": item.version, "space": SPACE},
            headers=_headers(csrf),
        )
    assert response.status_code == 200
    assert response.json()["space"] == SPACE


@pytest.mark.asyncio
async def test_patch_with_space_without_folder_defaults_to_space_root(
    full_app_items, item_store, totp_code, tmp_path, clock,
):
    """ITEM_MOVE_PLAN.md Sec4.1 Punkt 3: ein Space-Wechsel ohne folder= landet an der
    Ziel-Space-Wurzel, NICHT im gleichnamigen Ordner im Zielspace."""
    (tmp_path / "data" / FOREIGN_SPACE).mkdir(parents=True)
    (tmp_path / "data" / FOREIGN_SPACE / ".share.yml").write_text(
        f"write: [{SPACE}]\n", encoding="utf-8"
    )
    item = item_store.create(SPACE, type="note", title="Umzug", folder="projekte")
    async with _client(full_app_items) as client:
        csrf = await _login(client, totp_code)
        clock.advance(31)  # neues TOTP-Zeitfenster, sonst Replay-Ablehnung bei der Re-Auth
        response = await client.patch(
            f"/api/v1/items/{item.id}",
            json={
                "version": item.version, "space": FOREIGN_SPACE,
                "password": PASSWORD, "totp": totp_code(),
            },
            headers=_headers(csrf),
        )
    assert response.status_code == 200
    assert response.json()["folder"] == ""
    assert item_store.get(item.id).folder == ""


@pytest.mark.asyncio
async def test_patch_item_level_share_write_holder_cannot_move_item_between_spaces(
    full_app_items, item_store, totp_code,
):
    """P6-AE, der Kern (Parity mit `mcpserver/tools.py`s gleichnamigem Test): item-level
    `share_write` erlaubt inhaltliche Aenderungen, aber nie einen Space-Wechsel -- auch nicht in
    den eigenen Space des Actors, der voll beschreibbar waere."""
    item = item_store.create(FOREIGN_SPACE, type="note", title="Fremd", share_write=[SPACE])
    async with _client(full_app_items) as client:
        csrf = await _login(client, totp_code)
        response = await client.patch(
            f"/api/v1/items/{item.id}",
            json={"version": item.version, "space": SPACE},
            headers=_headers(csrf),
        )
    assert response.status_code == 403
    assert response.json()["error"] == "forbidden"
    assert item_store.get(item.id).space == FOREIGN_SPACE


@pytest.mark.asyncio
async def test_patch_with_space_and_folder_together_uses_space_level_check_not_owner_guard(
    full_app_items, item_store, totp_code, tmp_path, clock,
):
    """Advisor-Fund vor dem Bauen (ITEM_MOVE_PLAN.md Sec4.2/4.3, 2026-08-17): derselbe
    Eigentuemer-Riegel-Fund wie in `mcpserver/tools.py`, hier fuer `_items_patch`. Ein Actor mit
    space-level Schreibrecht auf BEIDEN Seiten, aber ohne Eigentuemerschaft an der Quelle, muss
    trotzdem mit gesetztem `folder` verschieben duerfen."""
    third_space = "gamma"
    (tmp_path / "data" / FOREIGN_SPACE).mkdir(parents=True)
    (tmp_path / "data" / FOREIGN_SPACE / ".share.yml").write_text(
        f"write: [{SPACE}]\n", encoding="utf-8"
    )
    item = item_store.create(third_space, type="note", title="Umzug mit Ordner")
    (tmp_path / "data" / third_space / ".share.yml").write_text(
        f"write: [{SPACE}]\n", encoding="utf-8"
    )
    async with _client(full_app_items) as client:
        csrf = await _login(client, totp_code)
        clock.advance(31)  # neues TOTP-Zeitfenster, sonst Replay-Ablehnung bei der Re-Auth
        response = await client.patch(
            f"/api/v1/items/{item.id}",
            json={
                "version": item.version, "space": FOREIGN_SPACE, "folder": "projekte",
                "password": PASSWORD, "totp": totp_code(),
            },
            headers=_headers(csrf),
        )
    assert response.status_code == 200
    assert response.json()["space"] == FOREIGN_SPACE
    assert response.json()["folder"] == "projekte"


@pytest.mark.asyncio
async def test_narrowing_share_write_does_not_require_reauth(full_app_items, item_store, totp_code):
    item = item_store.create(SPACE, type="note", title="Original", share_write=["fabian"])
    async with _client(full_app_items) as client:
        csrf = await _login(client, totp_code)
        response = await client.patch(
            f"/api/v1/items/{item.id}", json={"version": item.version, "share_write": []},
            headers=_headers(csrf),
        )
    assert response.status_code == 200
    assert response.json()["share_write"] == []


@pytest.mark.asyncio
async def test_pure_content_patch_does_not_require_reauth(full_app_items, item_store, totp_code):
    item = item_store.create(SPACE, type="note", title="Original")
    async with _client(full_app_items) as client:
        csrf = await _login(client, totp_code)
        response = await client.patch(
            f"/api/v1/items/{item.id}", json={"version": item.version, "title": "Geändert"},
            headers=_headers(csrf),
        )
    assert response.status_code == 200
    assert response.json()["title"] == "Geändert"


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
        + api_routes(settings, item_store, sessions, permissions, store, confirmed_users)
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
        + api_routes(settings, item_store, sessions, permissions, store, confirmed_users)
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


# -- Assets (Phase 6.5 Step B2) --------------------------------------------------------------

_PNG = b"\x89PNG\r\n\x1a\n" + b"restliche-bytes-egal"


@pytest.mark.asyncio
async def test_asset_upload_download_roundtrip(full_app_items, item_store, totp_code):
    item = item_store.create(SPACE, type="note", title="Mit Bild")
    async with _client(full_app_items) as client:
        csrf = await _login(client, totp_code)
        upload = await client.post(
            f"/api/v1/items/{item.id}/assets", content=_PNG, headers=_headers(csrf),
        )
        assert upload.status_code == 201
        asset_id = upload.json()["id"]

        download = await client.get(f"/api/v1/items/{item.id}/assets/{asset_id}")
    assert download.status_code == 200
    assert download.content == _PNG
    assert download.headers["content-type"] == "image/png"
    assert download.headers["x-content-type-options"] == "nosniff"


@pytest.mark.asyncio
async def test_asset_upload_too_large_is_413(full_app_items, item_store, totp_code):
    item = item_store.create(SPACE, type="note", title="Mit Bild")
    too_big = _PNG + b"\x00" * (5 * 1024 * 1024)
    async with _client(full_app_items) as client:
        csrf = await _login(client, totp_code)
        response = await client.post(
            f"/api/v1/items/{item.id}/assets", content=too_big, headers=_headers(csrf),
        )
    assert response.status_code == 413


@pytest.mark.asyncio
async def test_asset_upload_wrong_type_is_422(full_app_items, item_store, totp_code):
    item = item_store.create(SPACE, type="note", title="Mit Bild")
    svg = b"<svg xmlns='http://www.w3.org/2000/svg'></svg>"
    async with _client(full_app_items) as client:
        csrf = await _login(client, totp_code)
        response = await client.post(
            f"/api/v1/items/{item.id}/assets", content=svg, headers=_headers(csrf),
        )
    assert response.status_code == 422


@pytest.mark.asyncio
async def test_asset_delete_moves_to_trash(full_app_items, item_store, totp_code):
    item = item_store.create(SPACE, type="note", title="Mit Bild")
    async with _client(full_app_items) as client:
        csrf = await _login(client, totp_code)
        upload = await client.post(
            f"/api/v1/items/{item.id}/assets", content=_PNG, headers=_headers(csrf),
        )
        asset_id = upload.json()["id"]
        delete = await client.delete(
            f"/api/v1/items/{item.id}/assets/{asset_id}", headers=_headers(csrf),
        )
        listing = await client.get(f"/api/v1/items/{item.id}/assets")
    assert delete.status_code == 200
    assert listing.json() == []


@pytest.mark.asyncio
async def test_asset_of_nonexistent_item_is_404(full_app_items, totp_code):
    async with _client(full_app_items) as client:
        await _login(client, totp_code)
        response = await client.get("/api/v1/items/itm_00000000/assets/ast_00000000")
    assert response.status_code == 404


@pytest.mark.asyncio
async def test_asset_of_foreign_ungranted_item_is_403_not_404(
    full_app_items, item_store, totp_code,
):
    """Existiert wie `_items_get_one` (Z. 418-426): fehlende ID -> 404, fremdes Item ohne
    Freigabe -> 403 -- zwei unterscheidbare Codes, kein „gibt es nicht"-Versteck. Der Plantext
    (Step B2-Tabelle) behauptet denselben Code für beide Fälle; das trifft auf den kopierten
    `_items_get_one`-Pfad selbst nicht zu (siehe `test_get_item_from_foreign_space_without_
    share_is_forbidden` oben) -- diese Route übernimmt das bestehende Verhalten unverändert,
    keine neue Abweichung."""
    item = item_store.create(FOREIGN_SPACE, type="note", title="Fremd, ungeteilt")
    asset_id = item_store.put_asset(item.id, data=_PNG).id
    async with _client(full_app_items) as client:
        await _login(client, totp_code)
        response = await client.get(f"/api/v1/items/{item.id}/assets/{asset_id}")
    assert response.status_code == 403


@pytest.mark.asyncio
async def test_assets_appear_in_item_to_json(full_app_items, item_store, totp_code):
    item = item_store.create(SPACE, type="note", title="Mit Bild")
    async with _client(full_app_items) as client:
        csrf = await _login(client, totp_code)
        await client.post(
            f"/api/v1/items/{item.id}/assets", content=_PNG, headers=_headers(csrf),
        )
        response = await client.get(f"/api/v1/items/{item.id}")
    assets = response.json()["assets"]
    assert len(assets) == 1
    assert assets[0]["mime"] == "image/png"


@pytest.mark.asyncio
async def test_assets_survive_a_patch_response(full_app_items, item_store, totp_code):
    """P7-A3-Nebenfund: `_items_patch`/`_items_append`/`_items_archive` gaben `item_to_json()`
    bisher ohne `assets=` zurueck -- jede Antwort truegete `assets: []`, auch wenn das Item
    laengst ein Bild hatte. `editor.js :: afterWrite()` laedt den Editor direkt aus genau dieser
    Antwort neu -- ohne diesen Fix waere die Asset-Leiste nach jedem Speichern leer gewesen."""
    item = item_store.create(SPACE, type="note", title="Mit Bild")
    async with _client(full_app_items) as client:
        csrf = await _login(client, totp_code)
        await client.post(f"/api/v1/items/{item.id}/assets", content=_PNG, headers=_headers(csrf))
        current = (await client.get(f"/api/v1/items/{item.id}")).json()
        patch = await client.patch(
            f"/api/v1/items/{item.id}",
            json={"version": current["version"], "title": "Umbenannt"},
            headers=_headers(csrf),
        )
        append = await client.post(
            f"/api/v1/items/{item.id}/append",
            json={"version": patch.json()["version"], "text": "mehr Text"},
            headers=_headers(csrf),
        )
    assert len(patch.json()["assets"]) == 1
    assert len(append.json()["assets"]) == 1


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
