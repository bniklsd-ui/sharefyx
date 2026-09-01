"""Phase 8 Block B Step B3 (Plan §3 P8-M).

Tests fuer `GET /api/v1/graph` -- Knoten + Kanten fuer die Verknuepfungs-Graph-Ansicht.
Folgt demselben Muster wie `test_api.py`: In-Process-Starlette, Login ueber `totp_code()`,
ACL-Hilfskonstrukte ueber `item_store.update(... share_read=...)`.
"""
from __future__ import annotations

import pytest

BASE_URL = "https://space.example.ts.net"
SPACE = "niklas"
FOREIGN_SPACE = "fabian"
PASSWORD = "correct horse battery staple"


def _client(app):
    import httpx
    return httpx.AsyncClient(transport=httpx.ASGITransport(app=app), base_url=BASE_URL)


async def _login(client, totp_code) -> None:
    response = await client.post(
        "/ui/login", data={"space": SPACE, "password": PASSWORD, "totp": totp_code()},
    )
    assert response.status_code == 200


# --- Happy Path --------------------------------------------------------------------------

@pytest.mark.asyncio
async def test_graph_returns_visible_nodes_and_edges(full_app_items, item_store, totp_code):
    """Phase 8 B3: Frontmatter- UND Body-Kante tauchen beide auf, wenn beide Enden sichtbar
    sind -- der Knoten trägt die acht Felder exakt aus Plan §3 B3."""
    target = item_store.create(SPACE, type="note", title="Zielnotiz")
    source = item_store.create(
        SPACE, type="note", title="Quelle",
        links=[target.id],                       # Frontmatter-Kante
        body=f"Siehe {target.id} hier.",          # Body-Kante (dieselbe ID)
    )

    async with _client(full_app_items) as client:
        await _login(client, totp_code)
        response = await client.get("/api/v1/graph")

    assert response.status_code == 200
    data = response.json()

    by_id = {n["id"]: n for n in data["nodes"]}
    assert source.id in by_id
    assert target.id in by_id
    assert by_id[source.id]["title"] == "Quelle"
    assert by_id[source.id]["own"] is True
    assert by_id[source.id]["shared"] is False
    # Exakt die acht Felder aus Plan §3 B3 -- nicht mehr.
    assert set(by_id[source.id].keys()) == {
        "id", "title", "space", "own", "shared", "type", "status", "folder", "tags",
    }

    edges = sorted(data["edges"], key=lambda e: (e["src"], e["kind"], e["dst"]))
    assert edges == [
        {"src": source.id, "dst": target.id, "kind": "body"},
        {"src": source.id, "dst": target.id, "kind": "frontmatter"},
    ]


# --- ACL: unsichtbare Items -------------------------------------------------------------

@pytest.mark.asyncio
async def test_graph_hides_foreign_unshared_items_and_their_edges(
    full_app_items, item_store, totp_code,
):
    """Phase 8 B3 (Plan §3 B3, ACL-Leck-Riegel): ein `visibility: private` Item im fremden
    Space erscheint weder als Knoten noch als Kantenende -- auch nicht fuer eine Kante,
    die VON ihm weg zeigt (ein Outgoing-Edge wuerde sonst den Knoten verraten)."""
    foreign = item_store.create(FOREIGN_SPACE, type="note", title="Fremd & privat")
    own = item_store.create(
        SPACE, type="note", title="Eigene",
        links=[foreign.id],  # zeigt auf das fremde private Item
    )

    async with _client(full_app_items) as client:
        await _login(client, totp_code)
        response = await client.get("/api/v1/graph")

    data = response.json()
    node_ids = {n["id"] for n in data["nodes"]}
    # Nur die eigene Notiz sichtbar; das fremde private Item ist unsichtbar.
    assert own.id in node_ids
    assert foreign.id not in node_ids
    # Die Kante own -> foreign wird unterdrueckt, weil foreign nicht in der sichtbaren
    # Knotenmenge ist -- sonst waere foreign indirekt verraten (Edge verraten Knoten).
    assert all(e["dst"] != foreign.id for e in data["edges"])


@pytest.mark.asyncio
async def test_graph_includes_foreign_shared_item_as_node(full_app_items, item_store, totp_code):
    """Phase 8 B3: ein `share_read` fuer den eigenen Space macht das fremde Item sichtbar
    UND seine Kanten werden aufgefuellt -- beide Richtungen der ACL-Korrektheit."""
    foreign = item_store.create(FOREIGN_SPACE, type="note", title="Fremd & geteilt")
    # Item-level share_read macht das fremde Item fuer den eigenen Space lesbar.
    item_store.update(foreign.id, version=foreign.version, share_read=[SPACE])

    own = item_store.create(
        SPACE, type="note", title="Eigene",
        links=[foreign.id],
    )

    async with _client(full_app_items) as client:
        await _login(client, totp_code)
        response = await client.get("/api/v1/graph")

    data = response.json()
    node_ids = {n["id"] for n in data["nodes"]}
    assert own.id in node_ids
    assert foreign.id in node_ids
    assert any(e["src"] == own.id and e["dst"] == foreign.id for e in data["edges"])


# --- Dangling references ----------------------------------------------------------------

@pytest.mark.asyncio
async def test_graph_silently_drops_edges_to_nonexistent_dst(full_app_items, item_store, totp_code):
    """Phase 8 B3: ein Body-Verweis auf eine ID, die nicht (mehr) existiert, erzeugt keine
    Kante -- der API-Endpoint filtert das. Kein 404, kein 500."""
    item_store.create(
        SPACE, type="note", title="Verwaister Verweis",
        body="Siehe itm_deadbeef.",
    )

    async with _client(full_app_items) as client:
        await _login(client, totp_code)
        response = await client.get("/api/v1/graph")

    assert response.status_code == 200
    data = response.json()
    assert data["edges"] == []


# --- Archiv-Default + Opt-In -------------------------------------------------------------

@pytest.mark.asyncio
async def test_graph_excludes_archived_items_by_default(full_app_items, item_store, totp_code):
    """Phase 8 B3: ein archiviertes Item erscheint ohne `?archived=1` NICHT als Knoten, und
    Kanten zu/von ihm verschwinden ebenfalls."""
    live = item_store.create(SPACE, type="note", title="Live")
    archive_target = item_store.create(SPACE, type="note", title="Wird archiviert")
    item_store.create(
        SPACE, type="note", title="Quelle",
        links=[archive_target.id],
    )
    item_store.archive(archive_target.id, version=archive_target.version)

    async with _client(full_app_items) as client:
        await _login(client, totp_code)
        response = await client.get("/api/v1/graph")

    data = response.json()
    node_ids = {n["id"] for n in data["nodes"]}
    assert live.id in node_ids
    assert archive_target.id not in node_ids
    # Kante Quelle -> archive_target ist ebenfalls draussen.
    assert all(e["dst"] != archive_target.id for e in data["edges"])


@pytest.mark.asyncio
async def test_graph_includes_archived_items_with_explicit_flag(
    full_app_items, item_store, totp_code,
):
    """Phase 8 B3: `?archived=1` schaltet den Default ab -- archivierte Items erscheinen
    wieder als Knoten UND als Kanten-Endpunkte."""
    live = item_store.create(SPACE, type="note", title="Live")
    archived = item_store.create(SPACE, type="note", title="Archiviert")
    item_store.create(
        SPACE, type="note", title="Quelle",
        links=[archived.id],
    )
    item_store.archive(archived.id, version=archived.version)

    async with _client(full_app_items) as client:
        await _login(client, totp_code)
        response = await client.get("/api/v1/graph?archived=1")

    data = response.json()
    node_ids = {n["id"] for n in data["nodes"]}
    assert live.id in node_ids
    assert archived.id in node_ids
    # Kante zurueck.
    assert any(e["src"] != archived.id and e["dst"] == archived.id for e in data["edges"])


# --- Self-Loop-Filter --------------------------------------------------------------------

@pytest.mark.asyncio
async def test_graph_drops_self_loop_edges(full_app_items, item_store, totp_code):
    """Phase 8 B3 (Plan §3 B3, `src != dst`): eine `links:[itm_self]`-Selbstkante ist nie
    sinnvoll und wird unterdrueckt."""
    self_ref = item_store.create(
        SPACE, type="note", title="Selbstbezueglich",
        body="Ich bin itm_self_referenz.",
        links=[],
    )
    # Body-Referenz auf eigene ID ist realistisch (Menschen verlinken sich selbst) -- keine
    # Frontmatter noetig.
    item_store.update(
        self_ref.id, version=self_ref.version, body=f"Siehe {self_ref.id} selbst.",
    )

    async with _client(full_app_items) as client:
        await _login(client, totp_code)
        response = await client.get("/api/v1/graph")

    data = response.json()
    assert data["edges"] == []


# --- Authentifizierung -------------------------------------------------------------------

@pytest.mark.asyncio
async def test_graph_requires_session(full_app_items):
    """Phase 8 B3: ohne gueltige Session -> 401, wie alle anderen geschuetzten Routen."""
    async with _client(full_app_items) as client:
        response = await client.get("/api/v1/graph")
    assert response.status_code == 401
