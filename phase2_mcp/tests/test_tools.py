"""Unit-Tests für die sechs Tools (Plan §4 Step 6). `tools.register()` gibt die rohen,
undekorierten Tool-Funktionen zurück (`@mcp.tool(...)` reicht die Originalfunktion unverändert
durch), die hier direkt aufgerufen werden — die reale HTTP/FastMCP-Kette (`BearerAuthASGI`,
Guard, Nebenläufigkeit) ist bereits in
`test_app.py::test_principal_isolation_under_concurrency` (Step 5) end-to-end bewiesen. Hier
geht es um die Tool-eigene Semantik (Wrapping, Rechte, Fehlerabbildung, Token-Budget) — deshalb
wird der Guard (`assert_principal_matches_request`, braucht einen echten HTTP-Request-Kontext)
für diese Schicht bewusst gemockt statt für zwanzig Tests erneut eine echte FastMCP-App
hochzuziehen.
"""
from __future__ import annotations

import asyncio
import base64
import json
import os
from contextlib import contextmanager

import pytest
from fastmcp import Client, FastMCP
from fastmcp.exceptions import ToolError

from mcpserver import context, tools
from mcpserver.auth import AuthError, Principal
from mcpserver.permissions import Permissions, SharePolicy
from mcpserver.tools import UNTRUSTED_CLOSE, UNTRUSTED_OPEN, wrap_untrusted
from sharefyx_image_bytes import png_bytes
from storage.store import Store

# Bewusst keine Nikinger-typischen Spacenamen (Plan §2.2 Erweiterungspfad).
SPACE_A = "alpha"
SPACE_B = "beta"
# P10.5, Block 2 (2026-10-22): die Home-Space-Regeln brauchen Namen für „Home-Space eines
# anderen" und für einen zweiten Team-Space.
SPACE_C = "gamma"
SPACE_D = "delta"

# **Das Home-Space-Modell dieses Testkorpus** (P10.5, Block 2): `alpha` und `gamma` sind
# Home-Spaces (zwei Nutzer), `beta` und `delta` sind Team-Spaces (sie gehören niemandem). Live
# beantwortet das die Auth-DB (`mcpserver/app.py :: create_app()`:
# `get_user(space) is not None`), dieser Testkorpus hat keine — das Modell steht deshalb
# ausdrücklich hier, statt es zu erfinden.
HOME_SPACES = frozenset({SPACE_A, SPACE_C})


def _write_share_yml(directory, content: str) -> None:
    directory.mkdir(parents=True, exist_ok=True)
    (directory / ".share.yml").write_text(content, encoding="utf-8")


@pytest.fixture(autouse=True)
def _bypass_guard(monkeypatch):
    monkeypatch.setattr(context, "assert_principal_matches_request", lambda: None)


@contextmanager
def _as(space: str):
    token = context.set_principal(Principal(space=space, token_hash=f"hash-{space}"))
    try:
        yield
    finally:
        context.reset_principal(token)


@pytest.fixture
def store(tmp_path) -> Store:
    return Store(tmp_path, git=False)


@pytest.fixture
def permissions(store) -> Permissions:
    """**P10.5, Block 2 (2026-10-22):** die Policy kennt jetzt Home-Spaces und Team-Spaces —
    dafür braucht sie ein Prädikat. Ohne Prädikat kennt sie **keinen** Home-Space (fail-closed,
    `permissions.py`), deshalb steht das Modell hier ausdrücklich: `alpha`/`gamma` sind
    Home-Spaces, `beta`/`delta` sind Team-Spaces."""
    return SharePolicy(store.acl_reader, is_home_space=lambda space: space in HOME_SPACES)


@pytest.fixture
def tools_map(store, permissions):
    mcp = FastMCP("test-tools")
    return tools.register(mcp, store=store, permissions=permissions)


class _OwnSpaceOnlyVisible:
    """Test-Double für `test_list_spaces_filters_by_can_read` — beweist, dass `list_spaces` den
    `can_read`-Seam wirklich benutzt, nicht nur `OwnSpaceWritable`s Immer-True-Implementierung."""

    def can_read(self, actor: str, target: str) -> bool:
        return actor == target

    def can_write(self, actor: str, target: str) -> bool:
        return actor == target

    def visible_spaces(self, actor, all_spaces):
        return [s for s in all_spaces if self.can_read(actor, s)]


# -- tool descriptions (Phase 6.5 Step A1) ---------------------------------------------


def _description_of(mcp: FastMCP, name: str) -> str:
    # [VERIFY] V63, gegen fastmcp==3.4.4 geklärt: die Beschreibung hängt am `FunctionTool`,
    # das nur über das (async) `get_tool()` erreichbar ist, nicht über `inspect.signature()`
    # wie der Rest dieser Suite die Funktionen selbst prüft.
    tool = asyncio.run(mcp.get_tool(name))
    return tool.description


@pytest.fixture
def described_mcp(store, permissions):
    mcp = FastMCP("test-tools-descriptions")
    tools.register(mcp, store=store, permissions=permissions)
    return mcp


def test_list_spaces_description_does_not_claim_own_space_only(described_mcp):
    desc = _description_of(described_mcp, "list_spaces")
    assert "nur für den" not in desc
    assert "geteilte Spaces" in desc


def test_write_tool_descriptions_document_status_values(described_mcp):
    from storage.models import STATUS_VALUES

    for name in ("create_item", "update_item"):
        desc = _description_of(described_mcp, name)
        for item_type, values in STATUS_VALUES.items():
            for value in values:
                assert value in desc, f"{name} nennt {value!r} für {item_type!r} nicht"


def test_all_write_tools_carry_the_division_of_labour(described_mcp):
    for name in ("create_item", "update_item", "append_to_item", "patch_item"):
        assert tools.WRITE_TOOL_DIVISION in _description_of(described_mcp, name)


def test_search_description_states_title_and_tag_scope(described_mcp):
    desc = _description_of(described_mcp, "search_items")
    assert "Titel und" in desc
    assert "NICHT im Body" in desc


def test_write_tool_descriptions_point_to_list_spaces(described_mcp):
    for name in ("create_item", "update_item"):
        assert "list_spaces" in _description_of(described_mcp, name)


def test_get_item_description_points_to_get_item_meta(described_mcp):
    assert "get_item_meta" in _description_of(described_mcp, "get_item")


def test_tool_descriptions_tell_the_agent_to_name_titles_not_ids(described_mcp):
    for name in ("search_items", "get_item", "get_item_meta", "create_item"):
        assert tools._TITLE_NOT_ID_HINT in _description_of(described_mcp, name)
    assert "Einkaufsliste Winter" in tools._TITLE_NOT_ID_HINT
    assert "itm_a1b2c3d4" in tools._TITLE_NOT_ID_HINT
    assert "Tabellen-Spalte" in tools._TITLE_NOT_ID_HINT
    assert "in jeder Textform" in tools._TITLE_NOT_ID_HINT
    assert "Klammern" in tools._TITLE_NOT_ID_HINT


# -- list_spaces --------------------------------------------------------------------


def test_list_spaces_marks_own_space_writable(tools_map, store, tmp_path):
    # P6 Step 5: ohne Freigabe wäre SPACE_B für SPACE_A unsichtbar (test_foreign_space_is_
    # invisible_without_share) — ein `read:`-Grant hält es sichtbar, aber nicht schreibbar,
    # genau der Kontrast, den dieser Test prüfen will.
    _write_share_yml(tmp_path / SPACE_B, f"read: [{SPACE_A}]\n")
    store.create(SPACE_A, type="task", title="A")
    store.create(SPACE_B, type="task", title="B")

    with _as(SPACE_A):
        payload = json.loads(tools_map["list_spaces"]())

    by_name = {entry["name"]: entry for entry in payload}
    assert by_name[SPACE_A]["writable"] is True
    assert by_name[SPACE_B]["writable"] is False


def test_list_spaces_includes_empty_own_space(tools_map, store):
    """Fund B1 aus der Live-Adapter-Abnahme (docs/concepts/P2_ADAPTER_ABNAHME_2026-07-26.md):
    eine frische Sitzung, deren eigener Space noch kein Item hat, muss den eigenen Space
    trotzdem sehen (mit item_count=0) — sonst kennt sie nur fremde, nicht schreibbare Spaces
    und hat keine Orientierung, bevor sie blind `create_item` ruft."""
    store.create(SPACE_B, type="task", title="B")
    # SPACE_A (der eigene Space des Principals) hat bewusst noch KEIN Item.

    with _as(SPACE_A):
        payload = json.loads(tools_map["list_spaces"]())

    by_name = {entry["name"]: entry for entry in payload}
    assert by_name[SPACE_A] == {
        "name": SPACE_A, "item_count": 0, "writable": True, "members": [], "folders": [],
    }
    # SPACE_B ist ohne Freigabe unsichtbar (P6 Step 5) — anders als vor P6, wo jeder Space
    # universell sichtbar war.
    assert SPACE_B not in by_name


def test_list_spaces_filters_by_can_read(store):
    store.create(SPACE_A, type="task", title="A")
    store.create(SPACE_B, type="task", title="B")
    restricted = tools.register(FastMCP("restricted"), store=store, permissions=_OwnSpaceOnlyVisible())

    with _as(SPACE_A):
        payload = json.loads(restricted["list_spaces"]())

    assert {entry["name"] for entry in payload} == {SPACE_A}


# -- search_items -------------------------------------------------------------------


def test_search_defaults_exclude_archived(tools_map, store):
    open_item = store.create(SPACE_A, type="task", title="Offen")
    archived = store.create(SPACE_A, type="task", title="Archiviert")
    store.archive(archived.id, version=archived.version)

    with _as(SPACE_A):
        payload = json.loads(tools_map["search_items"]())

    ids = {entry["id"] for entry in payload["items"]}
    assert open_item.id in ids
    assert archived.id not in ids


def test_search_explicit_status_wins_over_default(tools_map, store):
    archived = store.create(SPACE_A, type="task", title="Archiviert")
    store.archive(archived.id, version=archived.version)

    with _as(SPACE_A):
        payload = json.loads(tools_map["search_items"](status="archived"))

    assert archived.id in {entry["id"] for entry in payload["items"]}


def test_search_limit_defaults_to_20(tools_map, store):
    for i in range(25):
        store.create(SPACE_A, type="task", title=f"Item {i}")

    with _as(SPACE_A):
        payload = json.loads(tools_map["search_items"]())

    assert payload["limit"] == tools.DEFAULT_LIMIT
    assert len(payload["items"]) == tools.DEFAULT_LIMIT
    assert payload["truncated"] is True


def test_search_limit_is_clamped_to_max(tools_map, store):
    for i in range(tools.MAX_LIMIT + 20):
        store.create(SPACE_A, type="task", title=f"Item {i}")

    with _as(SPACE_A):
        payload = json.loads(tools_map["search_items"](limit=10_000))

    # Nicht nur das echoete Feld — der Clamp muss die tatsächlich zurückgegebene Seite treffen,
    # sonst würde ein ungeklemmtes `limit` denselben Wert zurückmelden und der Test bestünde
    # trotzdem (Finding aus dem Advisor-Review).
    assert payload["limit"] == tools.MAX_LIMIT
    assert len(payload["items"]) == tools.MAX_LIMIT


def test_search_in_body_default_does_not_find_body_only_match(tools_map, store):
    store.create(SPACE_A, type="note", title="Titel ohne Treffer", body="EinBodyMarkerXYZ")

    with _as(SPACE_A):
        payload = json.loads(tools_map["search_items"](query="EinBodyMarkerXYZ"))

    assert payload["total"] == 0


def test_search_in_body_true_finds_body_only_match(tools_map, store):
    item = store.create(SPACE_A, type="note", title="Titel ohne Treffer", body="EinBodyMarkerXYZ")

    with _as(SPACE_A):
        payload = json.loads(tools_map["search_items"](query="EinBodyMarkerXYZ", in_body=True))

    assert item.id in {entry["id"] for entry in payload["items"]}


def test_foreign_space_is_invisible_without_share(tools_map, store):
    """P6 Step 5 (Plan §4 Step 5, Pflichttest): `search_items` filtert jetzt item-weise über
    `can_read_item`/`acl_of()`, nicht mehr space-weise über `visible_spaces` — ein Item in
    einem Space ohne jede `.share.yml`/Item-Freigabe ist unsichtbar, `total` zählt es nicht
    mit. Anders als unter `OwnSpaceWritable` (P2), wo jeder Space universell lesbar war."""
    store.create(SPACE_A, type="task", title="Eigenes Item A1")
    store.create(SPACE_A, type="task", title="Eigenes Item A2")
    store.create(SPACE_B, type="task", title="Fremdes Item B1, ungeteilt")

    with _as(SPACE_A):
        payload = json.loads(tools_map["search_items"]())

    assert {entry["space"] for entry in payload["items"]} == {SPACE_A}
    assert payload["total"] == 2  # nicht 3 — die Vorfilterung muss vor der Zählung passieren


def test_search_snippet_of_foreign_space_is_wrapped(tools_map, store, tmp_path):
    _write_share_yml(tmp_path / SPACE_B, f"read: [{SPACE_A}]\n")
    beta_item = store.create(SPACE_B, type="note", title="Fremd", body="Beta-Inhalt")

    with _as(SPACE_A):
        payload = json.loads(tools_map["search_items"](space=SPACE_B))

    entry = next(i for i in payload["items"] if i["id"] == beta_item.id)
    assert entry["snippet"].startswith(UNTRUSTED_OPEN.format(space=SPACE_B))
    assert entry["snippet"].endswith(UNTRUSTED_CLOSE)


def test_share_read_makes_exactly_one_item_visible_not_the_folder(tools_map, store):
    """Plan §4 Step 5, Pflichttest. Item-Freigabe (`share_read`) ist gezielt — anders als eine
    `.share.yml`, die den ganzen Ordner öffnet, macht sie NUR das eine Item sichtbar."""
    shared = store.create(SPACE_B, type="note", title="Freigegeben", folder="projekte")
    store.update(shared.id, version=shared.version, share_read=[SPACE_A])
    sibling = store.create(SPACE_B, type="note", title="Nicht freigegeben", folder="projekte")

    with _as(SPACE_A):
        payload = json.loads(tools_map["search_items"](space=SPACE_B))

    ids = {entry["id"] for entry in payload["items"]}
    assert shared.id in ids
    assert sibling.id not in ids


def test_folder_share_is_inherited_by_children(tools_map, store, tmp_path):
    """Plan §4 Step 5, Pflichttest. Eine `.share.yml` in einem Ordner gilt für Items in
    Unterordnern darunter (Vereinigung entlang des Pfads, Plan §1.2.3 Regel 1)."""
    _write_share_yml(tmp_path / SPACE_B / "projekte", f"read: [{SPACE_A}]\n")
    nested = store.create(SPACE_B, type="note", title="Tief verschachtelt", folder="projekte/alpha")

    with _as(SPACE_A):
        payload = json.loads(tools_map["search_items"](space=SPACE_B))

    assert nested.id in {entry["id"] for entry in payload["items"]}


def test_share_write_allows_update_and_append_but_not_in_other_folders(tools_map, store, tmp_path):
    """Plan §4 Step 5, Pflichttest. `.share.yml`-Freigaben sind ordnerscharf — write in einem
    Ordner erlaubt keinen Schreibzugriff auf ein Item in einem anderen, ungeteilten Ordner
    desselben Space."""
    _write_share_yml(tmp_path / SPACE_B / "geteilt", f"write: [{SPACE_A}]\n")
    shared_item = store.create(SPACE_B, type="note", title="Geteilt", folder="geteilt")
    other_item = store.create(SPACE_B, type="note", title="Ungeteilt", folder="privat")

    with _as(SPACE_A):
        update_receipt = json.loads(
            tools_map["update_item"](shared_item.id, version=shared_item.version, title="Geändert")
        )
        assert update_receipt["title"] == "Geändert"
        append_receipt = json.loads(
            tools_map["append_to_item"](shared_item.id, version=update_receipt["version"], text="Mehr")
        )
        assert append_receipt["op"] == "append"

        with pytest.raises(ToolError, match="write_denied"):
            tools_map["update_item"](other_item.id, version=other_item.version, title="Hack")


def test_human_only_item_is_invisible_to_agent_surface_including_total(tools_map, store):
    """Plan §4 Step 5, Pflichttest (P6-P). `visibility: human` sperrt selbst dem Eigentümer-
    Space die Agentenfläche — auch `get_item`, auch `total` in `search_items`. Das ist der
    ganze Zweck des Felds: ein Mensch kann ein eigenes Item vor Claude verbergen."""
    hidden = store.create(SPACE_A, type="note", title="Tagebuch", visibility="human")
    store.create(SPACE_A, type="note", title="Normal")

    with _as(SPACE_A):
        payload = json.loads(tools_map["search_items"]())
        assert hidden.id not in {entry["id"] for entry in payload["items"]}
        assert payload["total"] == 1

        with pytest.raises(ToolError, match="write_denied"):
            tools_map["get_item"](hidden.id)


def test_human_only_item_cannot_be_written_on_agent_surface(tools_map, store):
    """Fix, 2026-08-12 (Advisor-Fund nach dem ersten Step-5-Commit): `can_write_item` prüfte
    ursprünglich keine `visibility` — ein Item, das `get_item`/`search_items` bereits verbargen,
    war über `append_to_item`/`update_item` trotzdem beschreibbar, weil der Aufrufer sein
    eigener Space war. Ein Versionskonflikt hätte dabei sogar Version/Zeitstempel des
    angeblich "vollständig nicht existenten" Items preisgegeben."""
    hidden = store.create(SPACE_A, type="note", title="Tagebuch", body="Geheim", visibility="human")

    with _as(SPACE_A):
        with pytest.raises(ToolError, match="write_denied"):
            tools_map["update_item"](hidden.id, version=hidden.version, title="Verändert")
        with pytest.raises(ToolError, match="write_denied"):
            tools_map["append_to_item"](hidden.id, version=hidden.version, text="Mehr")
        # Insbesondere kein Versionskonflikt-Leck über eine falsche Version.
        with pytest.raises(ToolError, match="write_denied"):
            tools_map["update_item"](hidden.id, version=999, title="Verändert")

    unchanged = store.get(hidden.id)
    assert unchanged.title == "Tagebuch"
    assert unchanged.body == "Geheim"
    assert unchanged.version == hidden.version


def test_human_only_item_is_visible_on_the_human_surface(store):
    """Kontrastprobe zu oben: `visibility: human` sperrt nur `Surface.AGENT`, nicht die
    `SharePolicy` selbst — dieselbe `AclDecision` bleibt für `Surface.HUMAN` lesbar
    (`webui/api.py` benutzt genau diesen Pfad, siehe `phase5_ui/tests/test_api.py`)."""
    from mcpserver.permissions import Surface

    hidden = store.create(SPACE_A, type="note", title="Tagebuch", visibility="human")
    policy = SharePolicy(store.acl_reader)
    acl = store.acl_of(hidden.id)
    assert policy.can_read_item(SPACE_A, acl, surface=Surface.HUMAN) is True
    assert policy.can_read_item(SPACE_A, acl, surface=Surface.AGENT) is False


def test_unknown_space_in_share_yml_grants_nothing(tools_map, store, tmp_path):
    """Plan §4 Step 5, Pflichttest — Wiring-Beweis auf Adapter-Ebene (die Mechanik selbst ist
    in `phase6_shares/tests/test_acl.py` erschöpfend getestet)."""
    _write_share_yml(tmp_path / SPACE_B, "read: [nichtexistent]\n")
    item = store.create(SPACE_B, type="note", title="Fremd")

    with _as(SPACE_A), pytest.raises(ToolError, match="write_denied"):
        tools_map["get_item"](item.id)


def test_broken_share_yml_grants_nothing_and_logs_critical(tools_map, store, tmp_path):
    """Plan §4 Step 5, Pflichttest — Wiring-Beweis auf Adapter-Ebene."""
    _write_share_yml(tmp_path / SPACE_B, "read: [unclosed\n")
    item = store.create(SPACE_B, type="note", title="Fremd")

    with _as(SPACE_A), pytest.raises(ToolError, match="write_denied"):
        tools_map["get_item"](item.id)


def test_search_result_size_budget(tools_map, store):
    # Realistische Body-Länge statt leerem Body (Finding aus dem Advisor-Review): `_snippet()`
    # trimmt bei 160 Zeichen, ein leerer Body macht jedes Snippet "" und misst damit den
    # günstigsten, nicht den realistischen Fall. Ein Teil der Items liegt zusätzlich im fremden
    # Space, damit auch der `<untrusted_content>`-Wrap-Overhead ins Budget einfließt.
    long_body = (
        "Dies ist ein realistischer Notizinhalt mit genug Text, um das volle 160-Zeichen-"
        "Snippet-Limit auszureizen, statt eines leeren oder trivialen Bodys. " * 3
    )
    for i in range(20):
        store.create(SPACE_A, type="task", title=f"Titel Nummer {i}", tags=["infra"], body=long_body)
    for i in range(10):
        store.create(SPACE_B, type="task", title=f"Fremdtitel {i}", tags=["infra"], body=long_body)

    with _as(SPACE_A):
        payload_30 = tools_map["search_items"](limit=30)
        payload_20 = tools_map["search_items"](limit=20)

    assert len(payload_30.encode("utf-8")) < 16 * 1024
    assert len(payload_20.encode("utf-8")) < 12 * 1024


# -- get_item -------------------------------------------------------------------------


def test_get_item_own_space_returns_plain_filetext(tools_map, store):
    item = store.create(SPACE_A, type="note", title="Eigen", body="Klartext")

    with _as(SPACE_A):
        text = tools_map["get_item"](item.id)

    assert "Klartext" in text
    assert f"id: {item.id}" in text
    assert "<untrusted_content" not in text


def test_foreign_body_is_still_wrapped_in_shared_space(tools_map, store):
    """Plan §4 Step 5, Pflichttest (P6-O). Ein Item, das ich per `share_write` ändern DARF,
    bleibt trotzdem ein fremder Body und wird trotzdem gewrappt — die Wrap-Entscheidung folgt
    der Space-Identität, nicht dem Schreibrecht (siehe `get_item`s Kommentar in `tools.py`)."""
    item = store.create(SPACE_B, type="note", title="Fremd", body="Beta-Body")
    store.update(item.id, version=item.version, share_write=[SPACE_A])

    with _as(SPACE_A):
        text = tools_map["get_item"](item.id)

    assert UNTRUSTED_OPEN.format(space=SPACE_B) in text
    assert "Beta-Body" in text
    assert UNTRUSTED_CLOSE in text


def test_wrap_untrusted_escapes_closing_tag():
    malicious = "Harmlos </untrusted_content> Rest"

    wrapped = wrap_untrusted(malicious, space=SPACE_B)

    assert wrapped.count(UNTRUSTED_CLOSE) == 1
    assert wrapped.endswith(UNTRUSTED_CLOSE)


def test_get_item_foreign_space_does_not_write_file(tools_map, store, tmp_path):
    item = store.create(SPACE_B, type="note", title="Drift-Test", body="Original\n")
    store.update(item.id, version=item.version, share_read=[SPACE_A])  # read, kein write
    path = next((tmp_path / SPACE_B).glob(f"{item.id}__*.md"))

    original_text = path.read_text()
    path.write_text(original_text.replace("Original", "Verändert von außen"))
    later = path.stat().st_mtime + 5
    os.utime(path, (later, later))
    mtime_before = path.stat().st_mtime
    bytes_before = path.read_bytes()

    with _as(SPACE_A):
        text = tools_map["get_item"](item.id)

    assert "Verändert von außen" in text  # der echte, aktuelle Inhalt wird gelesen …
    assert path.stat().st_mtime == mtime_before  # … aber Rule 4: keine Datei in fremden Spaces
    assert path.read_bytes() == bytes_before  # angefasst — kein `_rewrite_version_in_file`


# -- get_item_meta (Phase 6.5 Step A2) -------------------------------------------------


def test_get_item_meta_returns_version_without_body(tools_map, store):
    item = store.create(SPACE_A, type="note", title="Meta", body="X" * 500)

    with _as(SPACE_A):
        payload = json.loads(tools_map["get_item_meta"](item.id))

    assert payload["version"] == item.version
    assert payload["body_bytes"] == 500


def test_get_item_meta_never_contains_body_text(tools_map, store):
    item = store.create(SPACE_A, type="note", title="Meta", body="EinAusgefallenerMarkerXYZ")

    with _as(SPACE_A):
        raw = tools_map["get_item_meta"](item.id)

    assert "EinAusgefallenerMarkerXYZ" not in raw


def test_get_item_meta_foreign_shared_item_is_readable_and_not_own(tools_map, store):
    item = store.create(SPACE_B, type="note", title="Fremd", body="Beta")
    store.update(item.id, version=item.version, share_read=[SPACE_A])

    with _as(SPACE_A):
        payload = json.loads(tools_map["get_item_meta"](item.id))

    assert payload["own"] is False
    assert payload["space"] == SPACE_B


def test_get_item_meta_foreign_item_without_grant_is_denied(tools_map, store):
    item = store.create(SPACE_B, type="note", title="Fremd")

    with _as(SPACE_A), pytest.raises(ToolError, match="write_denied"):
        tools_map["get_item_meta"](item.id)


# -- create_item ----------------------------------------------------------------------


def test_create_item_uses_principal_space(tools_map, store):
    with _as(SPACE_A):
        receipt = json.loads(tools_map["create_item"](type="task", title="Neu"))

    assert receipt["space"] == SPACE_A
    counts = {s.name: s.item_count for s in store.list_spaces()}
    assert counts[SPACE_A] == 1


def test_create_item_into_foreign_space_is_denied(tools_map):
    """Plan §4 Step 5, Pflichttest. Ersetzt das alte `test_create_item_has_no_space_parameter`
    (P2-G) — `create_item` hat seit P6 Step 5 einen `space`-Parameter (P6-U), aber ein anderer
    Space als der eigene ist nur zulässig, wenn dessen `.share.yml` `write:` gewährt."""
    with _as(SPACE_A), pytest.raises(ToolError, match="write_denied"):
        tools_map["create_item"](type="task", title="Eindringling", space=SPACE_B)


def test_create_item_into_shared_space_is_allowed_for_member(tools_map, store, tmp_path):
    """Plan §4 Step 5, Pflichttest — Gegenprobe zu oben: mit `write:`-Mitgliedschaft gelingt
    dasselbe `create_item(space=...)`."""
    _write_share_yml(tmp_path / SPACE_B, f"write: [{SPACE_A}]\n")

    with _as(SPACE_A):
        receipt = json.loads(
            tools_map["create_item"](type="task", title="Eingeladen", space=SPACE_B)
        )

    assert receipt["space"] == SPACE_B
    counts = {s.name: s.item_count for s in store.list_spaces()}
    assert counts[SPACE_B] == 1


# -- update_item / append_to_item ------------------------------------------------------


def test_update_item_foreign_space_denied(tools_map, store):
    item = store.create(SPACE_B, type="task", title="Fremd")

    with _as(SPACE_A), pytest.raises(ToolError, match="write_denied"):
        tools_map["update_item"](item.id, version=item.version, title="Hack")


def test_append_to_item_foreign_space_denied(tools_map, store):
    item = store.create(SPACE_B, type="note", title="Fremd")

    with _as(SPACE_A), pytest.raises(ToolError, match="write_denied"):
        tools_map["append_to_item"](item.id, version=item.version, text="Hack")


# -- append_to_items (P10.5 Block 5, LG-4, Lock P10.5-J) --------------------------------


def _entries(*items_and_texts):
    return [
        tools.AppendEntry(item_id=i.id, version=i.version, text=t) for i, t in items_and_texts
    ]


def test_append_to_items_appends_each_with_its_own_version(tools_map, store):
    a = store.create(SPACE_A, type="note", title="A", body="eins")
    b = store.create(SPACE_A, type="note", title="B", body="zwei")

    with _as(SPACE_A):
        out = json.loads(tools_map["append_to_items"](_entries((a, "+a"), (b, "+bb"))))

    assert out["ok"] == 2 and out["failed"] == 0
    assert [r["item_id"] for r in out["results"]] == [a.id, b.id]
    assert [r["appended_bytes"] for r in out["results"]] == [2, 3]
    # je Eintrag eigene Versionserhöhung und eigener Store-Write
    assert [r["version"] for r in out["results"]] == [a.version + 1, b.version + 1]
    assert "+a" in store.get(a.id).body and "+bb" in store.get(b.id).body


def test_append_to_items_reports_conflict_and_continues(tools_map, store):
    a = store.create(SPACE_A, type="note", title="A", body="eins")
    b = store.create(SPACE_A, type="note", title="B", body="zwei")
    store.update(a.id, version=a.version, title="Extern geändert")  # a.version ist jetzt veraltet

    with _as(SPACE_A):
        out = json.loads(tools_map["append_to_items"](_entries((a, "+a"), (b, "+b"))))

    assert (out["ok"], out["failed"]) == (1, 1)
    assert out["results"][0]["ok"] is False and out["results"][0]["error"] == "conflict"
    assert out["results"][1]["ok"] is True
    assert "+a" not in store.get(a.id).body  # Hard Rule 3: der veraltete Eintrag schrieb nichts
    assert "+b" in store.get(b.id).body


def test_append_to_items_denies_foreign_entry_and_continues(tools_map, store):
    mine = store.create(SPACE_A, type="note", title="Mein", body="x")
    foreign = store.create(SPACE_B, type="note", title="Fremd", body="y")

    with _as(SPACE_A):
        out = json.loads(
            tools_map["append_to_items"](_entries((foreign, "Hack"), (mine, "ok")))
        )

    assert (out["ok"], out["failed"]) == (1, 1)
    assert out["results"][0]["error"] == "write_denied"
    assert "Hack" not in store.get(foreign.id).body
    assert "ok" in store.get(mine.id).body


@pytest.mark.parametrize("count", [0, 21])
def test_append_to_items_rejects_empty_and_more_than_20(tools_map, store, count):
    item = store.create(SPACE_A, type="note", title="A", body="x")
    entries = [tools.AppendEntry(item_id=item.id, version=item.version, text="t")] * count

    with _as(SPACE_A), pytest.raises(ToolError, match="validation_failed"):
        tools_map["append_to_items"](entries)
    assert store.get(item.id).version == item.version  # nichts geschrieben


def test_append_to_items_rejects_unknown_entry_fields(store, permissions):
    """`extra="forbid"` — ein `return_body` je Eintrag würde sonst still ignoriert."""
    item = store.create(SPACE_A, type="note", title="A", body="x")
    mcp = FastMCP("test-append-many")
    tools.register(mcp, store=store, permissions=permissions)

    async def _call():
        async with Client(mcp) as client:
            return await client.call_tool(
                "append_to_items",
                {"entries": [{"item_id": item.id, "version": item.version, "text": "t",
                              "return_body": True}]},
                raise_on_error=False,
            )

    with _as(SPACE_A):
        result = asyncio.run(_call())

    assert result.is_error
    assert "return_body" in result.content[0].text  # der Fehler nennt das fremde Feld, kein Fremdfehler
    assert store.get(item.id).version == item.version


def test_update_item_conflict_message_contains_current_version(tools_map, store):
    item = store.create(SPACE_A, type="task", title="X")
    store.update(item.id, version=item.version, title="Extern geändert")

    with _as(SPACE_A), pytest.raises(ToolError) as excinfo:
        tools_map["update_item"](item.id, version=item.version, title="Veraltet")

    message = str(excinfo.value)
    assert "conflict" in message
    assert str(item.version) in message
    assert str(item.version + 1) in message


def test_update_item_status_archived_routes_to_archive(tools_map, store, tmp_path):
    item = store.create(SPACE_A, type="task", title="Archivieren")

    with _as(SPACE_A):
        tools_map["update_item"](item.id, version=item.version, status="archived")

    archive_dir = tmp_path / SPACE_A / "_archive"
    assert any(p.name.startswith(item.id) for p in archive_dir.glob("*.md"))


def test_update_item_status_archived_rejects_other_fields(tools_map, store):
    item = store.create(SPACE_A, type="task", title="X")

    with _as(SPACE_A), pytest.raises(ToolError, match="invalid"):
        tools_map["update_item"](
            item.id, version=item.version, status="archived", title="Auch das noch"
        )


def test_update_item_invalid_status_rejected(tools_map, store):
    item = store.create(SPACE_A, type="task", title="X")

    with _as(SPACE_A), pytest.raises(ToolError, match="invalid"):
        tools_map["update_item"](item.id, version=item.version, status="bogus")


# -- Guard-Fehlerabbildung (Step-4-Advisor-Fund) -----------------------------------------


def test_patch_item_foreign_space_denied(tools_map, store):
    item = store.create(SPACE_B, type="note", title="Fremd", body="Text")

    with _as(SPACE_A), pytest.raises(ToolError, match="write_denied"):
        tools_map["patch_item"](
            item.id, version=item.version, edits=[{"old_text": "Text", "new_text": "Hack"}]
        )


def test_patch_item_zero_match_error_maps_to_patch_failed_tool_error(tools_map, store):
    item = store.create(SPACE_A, type="note", title="Patch-Fehler", body="Vorhanden")

    with _as(SPACE_A), pytest.raises(ToolError) as excinfo:
        tools_map["patch_item"](
            item.id, version=item.version,
            edits=[{"old_text": "Nicht da", "new_text": "X"}],
        )

    message = str(excinfo.value)
    assert "patch_failed" in message
    assert "edits[0]" in message
    assert "0 Treffer" in message
    # Werkzeug-Ergonomie-Fund (2026-08-14): der alte Text ("lies das Item neu") suggerierte ein
    # Textmatching-Problem, obwohl die häufigste reale Ursache ein Frontmatter-Feld ist, das
    # patch_item kategorisch nie erreicht -- die Meldung muss das jetzt sagen, statt zu einem
    # Re-Read zu raten, der nie hilft.
    assert "Body-Text" in message
    assert "update_item" in message


def test_patch_item_multi_match_error_names_the_lines(tools_map, store):
    item = store.create(SPACE_A, type="note", title="Mehrdeutig", body="X\nX\nX\n")

    with _as(SPACE_A), pytest.raises(ToolError) as excinfo:
        tools_map["patch_item"](
            item.id, version=item.version, edits=[{"old_text": "X", "new_text": "Y"}]
        )

    message = str(excinfo.value)
    assert "patch_failed" in message
    assert "3 Treffer" in message
    assert "Zeilen 1, 2" in message


# -- P6 Step 1: Quittungen statt Volltext (P6-H) -----------------------------------------


def test_write_tools_return_receipt_by_default(tools_map, store):
    with _as(SPACE_A):
        created = json.loads(tools_map["create_item"](type="task", title="Quittung"))
        assert created["op"] == "create"
        assert created["id"].startswith("itm_")
        assert created["space"] == SPACE_A
        item_id = created["id"]

        appended = json.loads(
            tools_map["append_to_item"](item_id, version=1, text="Zusatz")
        )
        assert appended["op"] == "append"
        assert appended["version"] == 2

        patched = json.loads(
            tools_map["patch_item"](
                item_id, version=2, edits=[{"old_text": "Zusatz", "new_text": "Geändert"}]
            )
        )
        assert patched["op"] == "patch"
        assert patched["version"] == 3
        assert patched["replacements"] == 1

        updated = json.loads(tools_map["update_item"](item_id, version=3, title="Neuer Titel"))
        assert updated["op"] == "update"
        assert updated["version"] == 4


def test_write_tools_return_full_filetext_when_return_body_true(tools_map, store):
    with _as(SPACE_A):
        created_text = tools_map["create_item"](
            type="task", title="Volltext", return_body=True
        )
        assert "id: itm_" in created_text and f"space: {SPACE_A}" in created_text
        item_id = created_text.splitlines()[1].split("id: ")[1].strip()

        appended_text = tools_map["append_to_item"](
            item_id, version=1, text="Zusatz", return_body=True
        )
        assert "Zusatz" in appended_text

        patched_text = tools_map["patch_item"](
            item_id, version=2,
            edits=[{"old_text": "Zusatz", "new_text": "Geändert"}],
            return_body=True,
        )
        assert "Geändert" in patched_text

        updated_text = tools_map["update_item"](
            item_id, version=3, title="Neuer Titel", return_body=True
        )
        assert "title: Neuer Titel" in updated_text


def test_receipt_never_contains_body_text(tools_map, store):
    marker = "GEHEIMER-BODY-MARKER"

    with _as(SPACE_A):
        created = tools_map["create_item"](type="note", title="Marker-Item", body=marker)
        assert marker not in created
        item_id = json.loads(created)["id"]

        appended = tools_map["append_to_item"](item_id, version=1, text="unabhaengiger Text")
        assert marker not in appended

        patched = tools_map["patch_item"](
            item_id, version=2, edits=[{"old_text": marker, "new_text": marker + "-patched"}]
        )
        assert marker not in patched

        updated = tools_map["update_item"](item_id, version=3, body=marker + "-updated")
        assert marker not in updated

        # Gegenprobe: mit return_body=True taucht der Marker tatsächlich auf -- sonst wäre der
        # Test oben vakuos (er würde auch bestehen, wenn die Tools kaputt wären).
        full_text = tools_map["get_item"](item_id)
        assert marker in full_text


def test_update_item_rejects_share_fields(tools_map, store):
    item = store.create(SPACE_A, type="note", title="X")

    with _as(SPACE_A):
        for field, value in (
            ("visibility", "human"),
            ("share_read", ["beta"]),
            ("share_write", ["beta"]),
        ):
            with pytest.raises(ToolError, match="invalid"):
                tools_map["update_item"](item.id, version=item.version, **{field: value})


def test_share_write_cannot_move_item_to_a_different_folder(tools_map, store, tmp_path):
    """Nikinger-Entscheidung 2026-08-12 (kein Plan-Text, Advisor-Fund vor dem Build): ein
    `share_write`-Halter darf ein fremdes Item inhaltlich ändern, aber nicht in einen anderen
    Ordner verschieben — sonst könnte er dessen Sichtbarkeit über eine breitere `.share.yml`
    dort erweitern, ohne dass die Agentenfläche je ein Re-Auth-Gate dafür hätte."""
    _write_share_yml(tmp_path / SPACE_B / "eng", f"write: [{SPACE_A}]\n")
    item = store.create(SPACE_B, type="note", title="Wird verschoben", folder="eng")

    with _as(SPACE_A):
        with pytest.raises(ToolError, match="invalid"):
            tools_map["update_item"](item.id, version=item.version, folder="weit")

        # Inhaltlich bleibt der Schreibzugriff intakt — nur `folder` ist gesperrt.
        receipt = json.loads(
            tools_map["update_item"](item.id, version=item.version, title="Geändert")
        )
        assert receipt["title"] == "Geändert"

    unchanged = store.get(item.id)
    assert unchanged.folder == "eng"


# -- update_item(space=...) -- Step 7b, P6-AD-AJ, ITEM_MOVE_PLAN.md Sec4.2 -------------------


def test_update_item_with_space_moves_between_shared_spaces(tools_map, store, tmp_path):
    _write_share_yml(tmp_path / SPACE_B, f"write: [{SPACE_A}]\n")
    item = store.create(SPACE_A, type="note", title="Umzug")

    with _as(SPACE_A):
        receipt = json.loads(
            tools_map["update_item"](item.id, version=item.version, space=SPACE_B)
        )
        assert receipt["version"] == item.version + 1

    moved = store.get(item.id)
    assert moved.space == SPACE_B
    assert (tmp_path / SPACE_B / f"{item.id}__umzug.md").exists()
    assert not (tmp_path / SPACE_A / f"{item.id}__umzug.md").exists()


def test_item_level_share_write_holder_cannot_move_item_to_another_space(
    tools_map, store, tmp_path
):
    """P6-AE, der Kern: item-level `share_write` erlaubt inhaltliche Änderungen, aber niemals
    einen Space-Wechsel — selbst wenn das Ziel für den Actor voll beschreibbar ist. Sonst
    könnte ein Delegat, der genau EIN fremdes Item bearbeiten darf, es in einen geteilten Space
    wegtragen (Exfiltration und Entzug in einem Zug, kein Re-Auth-Gate auf der Agentenfläche)."""
    item = store.create(SPACE_B, type="note", title="Fremdes Item", share_write=[SPACE_A])

    with _as(SPACE_A), pytest.raises(ToolError, match="write_denied"):
        # Ziel ist der EIGENE Space von alpha -- voll beschreibbar, rettet den Move trotzdem
        # nicht: der Riegel ist die Quellseite (SPACE_B), nicht das Ziel.
        tools_map["update_item"](item.id, version=item.version, space=SPACE_A)

    unchanged = store.get(item.id)
    assert unchanged.space == SPACE_B


def test_move_into_space_without_write_grant_is_denied(tools_map, store):
    item = store.create(SPACE_A, type="note", title="Umzug")

    with _as(SPACE_A), pytest.raises(ToolError, match="write_denied"):
        tools_map["update_item"](item.id, version=item.version, space=SPACE_B)


def test_move_out_of_space_without_write_grant_is_denied(tools_map, store, tmp_path):
    # Ziel (gamma) waere fuer alpha voll beschreibbar -- beweist, dass ausschliesslich die
    # fehlende Quellberechtigung (SPACE_B) den Move blockiert, nicht ein Zielproblem.
    _write_share_yml(tmp_path / SPACE_C, f"write: [{SPACE_A}]\n")
    item = store.create(SPACE_B, type="note", title="Fremdes Item", share_write=[SPACE_A])

    with _as(SPACE_A), pytest.raises(ToolError, match="write_denied"):
        tools_map["update_item"](item.id, version=item.version, space=SPACE_C)


def test_update_item_with_space_and_folder_together_uses_space_level_check_not_owner_guard(
    tools_map, store, tmp_path
):
    """Advisor-Fund vor dem Bauen (ITEM_MOVE_PLAN.md Sec4.2, 2026-08-17): der alte
    Eigentuemer-Riegel gegen Nicht-Eigentuemer-Ordnerwechsel haette einen legitimen
    Cross-Space-Move mit gleichzeitig gesetztem folder= faelschlich blockiert, weil kein
    Principal wie ein geteilter Space heisst. Ein Actor mit space-level Schreibrecht auf BEIDEN
    Seiten, aber ohne Eigentuemerschaft an der Quelle, muss trotzdem verschieben duerfen.

    **[Nachtrag P10.5, Block 2, 2026-10-22]:** Quelle und Ziel sind jetzt **Team-Spaces**
    (`beta` → `delta`), nicht der Home-Space `alpha`. Grund: P10.5-N (Nikinger 2026-10-21)
    verbietet, ein Item **aus** dem Home-Space eines anderen herauszutragen — das wäre dort ein
    Löschen (P9-K sperrt Löschen in fremden Home-Spaces). Der Testzweck bleibt derselbe: der
    Eigentuemer-Riegel darf einen legitimen Cross-Space-Move mit `folder=` nicht blockieren."""
    _write_share_yml(tmp_path / SPACE_B, f"write: [{SPACE_C}]\n")
    _write_share_yml(tmp_path / SPACE_D, f"write: [{SPACE_C}]\n")
    item = store.create(SPACE_B, type="note", title="Umzug mit Ordner")

    with _as(SPACE_C):
        receipt = json.loads(
            tools_map["update_item"](
                item.id, version=item.version, space=SPACE_D, folder="projekte"
            )
        )
        assert receipt["version"] == item.version + 1

    moved = store.get(item.id)
    assert moved.space == SPACE_D
    assert moved.folder == "projekte"


# -- P10.5, Block 2: RE-2 (Ordner wechseln im Team-Space), P10-I, P10.5-N --------------------


def test_update_item_folder_change_in_team_space_by_team_writer(tools_map, store, tmp_path):
    """**RE-2 (P10.5, Block 2, 2026-10-22):** ein space-level Schreiber in einem **Team-Space**
    darf den Ordner eines Items ändern. Vorher stand hier `acl.space != principal.space` — damit
    durfte auf der Agentenfläche nur der Eigentümer-Space den Ordner wechseln, während die
    Web-Oberfläche es seit E1a (P9-BG/BP) durfte: zwei Wege, zwei Regeln (D-17). Jetzt gilt
    `permissions.manages_space()` auf beiden Flächen."""
    _write_share_yml(tmp_path / SPACE_B, f"write: [{SPACE_A}]\n")
    item = store.create(SPACE_B, type="note", title="Ordnerwechsel", folder="eng")

    with _as(SPACE_A):
        receipt = json.loads(
            tools_map["update_item"](item.id, version=item.version, folder="weit")
        )
        assert receipt["version"] == item.version + 1

    assert store.get(item.id).folder == "weit"


def test_update_item_move_into_foreign_home_space_denied(tools_map, store, tmp_path):
    """**P10-I (P10.5, Block 2, 2026-10-22):** kein Item wandert in den Home-Space eines
    anderen — auch nicht mit space-level `write:` dort. Schreibrecht (P6-AE) ist die eine
    Frage, die *Regel*, wohin ein Item wandern darf, eine andere."""
    _write_share_yml(tmp_path / SPACE_C, f"write: [{SPACE_A}]\n")
    item = store.create(SPACE_A, type="note", title="Umzug")

    with _as(SPACE_A), pytest.raises(ToolError, match="write_denied"):
        tools_map["update_item"](item.id, version=item.version, space=SPACE_C)

    unchanged = store.get(item.id)
    assert unchanged.space == SPACE_A


def test_update_item_move_out_of_foreign_home_space_denied(tools_map, store, tmp_path):
    """**P10.5-N (P10.5, Block 2, Nikinger 2026-10-21):** kein Item wandert **aus** dem
    Home-Space eines anderen heraus — das wäre dort ein Löschen (P9-K sperrt Löschen in fremden
    Home-Spaces). Die Quelle ist diesmal der fremde Home-Space, das Ziel ein Team-Space."""
    _write_share_yml(tmp_path / SPACE_C, f"write: [{SPACE_A}]\n")
    _write_share_yml(tmp_path / SPACE_B, f"write: [{SPACE_A}]\n")
    item = store.create(SPACE_C, type="note", title="Wandert raus")

    with _as(SPACE_A), pytest.raises(ToolError, match="write_denied"):
        tools_map["update_item"](item.id, version=item.version, space=SPACE_B)

    unchanged = store.get(item.id)
    assert unchanged.space == SPACE_C


def test_update_item_move_into_team_space_still_allowed(tools_map, store, tmp_path):
    """**Gegenlauf** zu `test_update_item_move_into_foreign_home_space_denied`: dasselbe
    Schreibrecht, aber das Ziel ist ein **Team-Space** — der Weg bleibt offen. Team-Spaces
    gehören niemandem, also greift weder P10-I noch P10.5-N."""
    _write_share_yml(tmp_path / SPACE_B, f"write: [{SPACE_A}]\n")
    item = store.create(SPACE_A, type="note", title="Umzug")

    with _as(SPACE_A):
        receipt = json.loads(
            tools_map["update_item"](item.id, version=item.version, space=SPACE_B)
        )
        assert receipt["version"] == item.version + 1

    assert store.get(item.id).space == SPACE_B


# -- P10.5, Block 2, Nachzug (2026-10-22): RE-1-Parität beim Anlegen mit Ordner ---------------


def test_create_item_with_folder_in_foreign_home_space_denied(tools_map, store, tmp_path):
    """**RE-1-Parität (Befund aus der Probe 2.5, Nikinger-Entscheidung 2026-10-22):** ein Item
    mit **Ordner** in einem fremden **Home-Space** legt diesen Ordner beim Anlegen an — damit
    war RE-1 (Ordner anlegen) dort eine Hintertür, obwohl der Actor space-level `write:` hat.
    Dieselbe Regel wie RE-2 (Ordner wechseln): in einen Ordner schreiben darf nur, wer den
    Space **verwaltet** — der eigene Space und Team-Spaces mit Schreibrecht."""
    _write_share_yml(tmp_path / SPACE_C, f"write: [{SPACE_A}]\n")

    with _as(SPACE_A), pytest.raises(ToolError, match="write_denied"):
        tools_map["create_item"](
            type="note", title="Ordner im fremden Home-Space", space=SPACE_C, folder="neu",
        )

    # Fail-closed: **nichts** angelegt — kein Ordner, kein Item.
    assert not (tmp_path / SPACE_C / "neu").exists()
    assert store.search(space=SPACE_C).items == []


def test_create_item_with_folder_in_team_space_allowed(tools_map, store, tmp_path):
    """**Gegenlauf** zu `test_create_item_with_folder_in_foreign_home_space_denied`: dieselbe
    `.share.yml` mit `write:`, aber das Ziel ist ein **Team-Space** — dort darf der Ordner
    angelegt werden (Team-Spaces gehören niemandem, P10-I greift nicht)."""
    _write_share_yml(tmp_path / SPACE_B, f"write: [{SPACE_A}]\n")

    with _as(SPACE_A):
        receipt = json.loads(
            tools_map["create_item"](
                type="note", title="Ordner im Team-Space", space=SPACE_B, folder="neu",
            )
        )

    assert receipt["space"] == SPACE_B
    assert store.get(receipt["id"]).folder == "neu"
    assert (tmp_path / SPACE_B / "neu").is_dir()


def test_create_item_without_folder_in_foreign_home_space_still_allowed(tools_map, store, tmp_path):
    """**Gegenlauf** zu `test_create_item_with_folder_in_foreign_home_space_denied`: **ohne**
    Ordner bleibt das Anlegen an der Space-Wurzel erlaubt (P6-U, Hard Rule 4 Neufassung: der
    Ziel-Space ist ein anderer nur, wenn `.share.yml` dort `write:` gewährt). Die Regel
    betrifft den **Ordner**, nicht das Item."""
    _write_share_yml(tmp_path / SPACE_C, f"write: [{SPACE_A}]\n")

    with _as(SPACE_A):
        receipt = json.loads(
            tools_map["create_item"](type="note", title="Ohne Ordner", space=SPACE_C)
        )

    assert receipt["space"] == SPACE_C
    assert store.get(receipt["id"]).folder == ""


def test_update_item_with_space_rejects_combined_content_changes(tools_map, store):
    item = store.create(SPACE_A, type="note", title="Umzug")

    with _as(SPACE_A), pytest.raises(ToolError, match="invalid"):
        tools_map["update_item"](
            item.id, version=item.version, space=SPACE_A, title="Gleichzeitig auch das"
        )


def test_guard_auth_error_is_mapped_to_tool_error(tools_map, store, monkeypatch):
    """Deckt genau die Lücke ab, die der Advisor in Step 4 vorausgesagt hat: ein `AuthError`
    aus dem Guard läuft INNERHALB eines Tool-Aufrufs (das 401-Fenster ist vorbei) und muss über
    `map_storage_error()` in einen `ToolError` laufen statt roh aus dem Tool zu fallen. Diese
    Lücke bestand tatsächlich kurzzeitig während der Implementierung — ohne `_authenticated_
    principal()` wäre `AuthError` unbehandelt durchgefallen."""

    def _raise_auth_error():
        raise AuthError("Request-Kontext passt nicht zum aufgelösten Principal")

    monkeypatch.setattr(context, "assert_principal_matches_request", _raise_auth_error)

    with _as(SPACE_A), pytest.raises(ToolError, match="auth_error"):
        tools_map["list_spaces"]()


# -- get_item_asset / put_item_asset (Phase 6.5 Step B4) -------------------------------------

_PNG = png_bytes()


def test_get_item_meta_lists_assets_without_bytes(tools_map, store):
    item = store.create(SPACE_A, type="note", title="Mit Bild")
    asset = store.put_asset(item.id, data=_PNG)

    with _as(SPACE_A):
        payload = json.loads(tools_map["get_item_meta"](item.id))

    assert payload["assets"] == [
        {"id": asset.id, "mime": "image/png", "bytes": len(_PNG), "filename": ""}
    ]


def test_get_item_asset_returns_image_content_for_own_item(tools_map, store):
    item = store.create(SPACE_A, type="note", title="Mit Bild")
    asset = store.put_asset(item.id, data=_PNG)

    with _as(SPACE_A):
        image = tools_map["get_item_asset"](item.id, asset.id)

    content = image.to_image_content()
    assert content.mime_type == "image/png"
    assert base64.b64decode(content.data) == _PNG


def test_get_item_asset_foreign_item_with_share_read_only_returns_metadata_not_bytes(
    tools_map, store,
):
    """Der B3-Kerntest (P6.5-M): Leserecht allein reicht nicht für Bildbytes -- ein fremdes
    Bild vor einem sehenden Modell ist ein Injektionskanal, den <untrusted_content> strukturell
    nicht erreicht. Schreibrecht ist der gewählte Vertrauensmarker, nicht Leserecht."""
    item = store.create(SPACE_B, type="note", title="Fremd, nur lesbar", share_read=[SPACE_A])
    asset = store.put_asset(item.id, data=_PNG)

    with _as(SPACE_A):
        result = tools_map["get_item_asset"](item.id, asset.id)

    assert isinstance(result, str)
    payload = json.loads(result)
    assert payload["bytes_available"] is False
    assert payload["mime"] == "image/png"
    assert "hint" in payload


def test_get_item_asset_with_read_only_grant_and_unknown_asset_id_is_asset_not_found(
    tools_map, store,
):
    """Advisor-Fund vor dem Commit: der may_see_bytes=False-Zweig prüfte urspruenglich NIE, ob
    die asset_id ueberhaupt existiert -- jede erfundene ID waere hier "erfolgreich" gewesen
    (bytes_available: false), waehrend derselbe Aufruf mit Schreibrecht fuer dieselbe ID
    korrekt asset_not_found geworfen haette. Jetzt symmetrisch: Existenz zuerst, unabhaengig
    vom Rechtelevel."""
    item = store.create(SPACE_B, type="note", title="Fremd, nur lesbar", share_read=[SPACE_A])

    with _as(SPACE_A), pytest.raises(ToolError, match="asset_not_found"):
        tools_map["get_item_asset"](item.id, "ast_00000000")


def test_get_item_asset_foreign_item_with_share_write_returns_bytes(tools_map, store):
    item = store.create(SPACE_B, type="note", title="Fremd, beschreibbar", share_write=[SPACE_A])
    asset = store.put_asset(item.id, data=_PNG)

    with _as(SPACE_A):
        image = tools_map["get_item_asset"](item.id, asset.id)

    assert base64.b64decode(image.to_image_content().data) == _PNG


def test_get_item_asset_foreign_item_without_grant_denied(tools_map, store):
    item = store.create(SPACE_B, type="note", title="Fremd, ungeteilt")
    asset = store.put_asset(item.id, data=_PNG)

    with _as(SPACE_A), pytest.raises(ToolError, match="write_denied"):
        tools_map["get_item_asset"](item.id, asset.id)


def test_get_item_asset_unknown_asset_id_gives_asset_not_found_not_item_not_found(
    tools_map, store,
):
    """B1s Advisor-Fund, hier geschlossen: `ItemNotFound`s Standardtext ('prüfe die ID mit
    search_items') ist für eine Asset-ID irreführend -- `AssetNotFound` liefert stattdessen
    einen zur Asset-ID passenden Hinweis (`get_item_meta`)."""
    item = store.create(SPACE_A, type="note", title="Ohne Bild")

    with _as(SPACE_A), pytest.raises(ToolError, match="asset_not_found.*get_item_meta"):
        tools_map["get_item_asset"](item.id, "ast_00000000")


def test_put_item_asset_writes_and_returns_receipt_without_bytes(tools_map, store):
    item = store.create(SPACE_A, type="note", title="Ziel")
    data_b64 = base64.b64encode(_PNG).decode()

    with _as(SPACE_A):
        receipt = json.loads(
            tools_map["put_item_asset"](item.id, data_b64, filename="foto.png")
        )

    assert receipt["op"] == "asset"
    assert receipt["mime"] == "image/png"
    assert receipt["bytes"] == len(_PNG)
    assert receipt["item_version"] == item.version
    assert "asset:" + receipt["asset_id"] in receipt["hint"]
    assert data_b64 not in json.dumps(receipt)

    [stored] = store.list_assets(item.id)
    assert stored.id == receipt["asset_id"]


def test_put_item_asset_foreign_space_without_grant_denied(tools_map, store):
    item = store.create(SPACE_B, type="note", title="Fremd")
    data_b64 = base64.b64encode(_PNG).decode()

    with _as(SPACE_A), pytest.raises(ToolError, match="write_denied"):
        tools_map["put_item_asset"](item.id, data_b64)

    assert store.list_assets(item.id) == []


def test_no_tool_response_ever_carries_a_base64_image_payload(tools_map, store):
    """P6.5-N, die erzwingbare Hälfte: Bildbytes verlassen den Server über GENAU EIN Tool
    (`get_item_asset`) -- `get_item`, `get_item_meta`, `search_items` und jede Quittung
    (inkl. `put_item_asset`s eigener) enthalten NIE die Base64-Nutzlast, auch nicht für ein
    eigenes Item mit Bild. Assertion gegen einen eigenen, unverwechselbaren Bytes-Marker
    (Advisor-Vorgabe) statt gegen `_PNG` oben: eine kurze Fixture beweist per Zufall dasselbe
    wie ein Marker, ein Marker beweist es absichtlich -- und die zusätzliche Klartext-Prüfung
    (nicht nur Base64) fängt auch den Fehlerfall "jemand gibt rohe Bytes statt Base64 zurück",
    den die reine Base64-Suche nicht abdecken würde."""
    item = store.create(SPACE_A, type="note", title="Mit Bild", body="Text.")
    marker = b"MARKER-NIE-IN-EINER-ANTWORT"
    # Der Marker steckt **im Bildinhalt** (IDAT), nicht in einem Metadaten-Chunk: Metadaten
    # werden beim Hochladen entfernt (P10.5 Block 3, LG-8) — der Marker müsste also gar nicht
    # erst in der Datei stehen, und die Prüfung wäre wertlos.
    png = png_bytes(payload=marker)
    data_b64 = base64.b64encode(png).decode()

    with _as(SPACE_A):
        put_receipt = tools_map["put_item_asset"](item.id, data_b64)
        get_meta = tools_map["get_item_meta"](item.id)
        get_full = tools_map["get_item"](item.id)
        search = tools_map["search_items"](query="Mit Bild")

    marker_text = marker.decode("ascii")
    for response in (put_receipt, get_meta, get_full, search):
        assert data_b64 not in response
        assert marker_text not in response


# -- P9 Step F: `doing` und `assignee` über MCP (Plan §8.3) ----------------------------------


def test_create_item_accepts_the_doing_status_and_the_assignee(tools_map):
    """`doing` braucht keine Werkzeug-Änderung — `_status_hint()` generiert das Vokabular aus
    `STATUS_VALUES` (P6.5-C), und `assignee` ist ein gewöhnlicher Inhaltsparameter wie `due`."""
    with _as(SPACE_A):
        receipt = json.loads(
            tools_map["create_item"](
                type="task", title="Angebot schreiben", status="doing", assignee=SPACE_B,
            )
        )
    assert receipt["op"] == "create"
    assert store_assignee_via_search(tools_map, receipt["id"]) == SPACE_B


def test_return_body_shows_the_assignee_that_was_just_written(tools_map):
    """`item_to_filetext()` dupliziert bewusst die Feldreihenfolge von `storage.store._item_to_text`
    (Modul-Docstring). Ohne ihren `assignee`-Eintrag gäbe dieser Aufruf einen Dateitext zurück,
    der das Feld nicht enthält, während es auf der Platte steht — ein Werkzeug, das etwas
    anderes zurückgibt als es geschrieben hat."""
    with _as(SPACE_A):
        text = tools_map["create_item"](
            type="task", title="Filetext", assignee=SPACE_B, return_body=True,
        )
    assert "assignee: " + SPACE_B in text


def test_update_item_clears_the_assignee_with_an_empty_string(tools_map):
    """`assignee=""` ist "niemand zugewiesen" und **nicht** "unverändert": der Kern behandelt
    den leeren String als Default und schreibt das Feld dann nicht in die Datei. Deshalb `is not
    None` im Werkzeug statt eines truthiness-Tests — sonst könnte ein Agent eine Aufgabe nie
    wieder freigeben."""
    with _as(SPACE_A):
        created = json.loads(
            tools_map["create_item"](type="task", title="Zuweisen", assignee=SPACE_B)
        )
        tools_map["update_item"](created["id"], created["version"], assignee="")
    assert store_assignee_via_search(tools_map, created["id"]) == ""


def test_update_item_rejects_a_non_string_assignee(tools_map):
    with _as(SPACE_A):
        created = json.loads(tools_map["create_item"](type="task", title="Typfehler"))
        with pytest.raises(ToolError, match="assignee"):
            tools_map["update_item"](created["id"], created["version"], assignee=42)


def store_assignee_via_search(tools_map, item_id: str) -> str:
    """Liest `assignee` über den Agenten-Pfad zurück (`search_items`), nicht über den Store —
    ein Test, der denselben Speicher liest, den er eben geschrieben hat, beweist die
    Serialisierung nicht."""
    with _as(SPACE_A):
        found = json.loads(tools_map["search_items"](query="", limit=50))
    return next(row["assignee"] for row in found["items"] if row["id"] == item_id)


# -- P9 Block trace: `updated_by` + `_ASSIGNEE_HINT` (Plan §4 T8/T9) -------------------------
#
# Die Wächter, die nicht hier wohnen, stehen in `phase9_hardening/tests/test_trace_block.py`
# (AST ueber beide Adapterpakete) — hier steht alles, was die echten Tools und die echten
# Werkzeugbeschreibungen betrifft, denn `_as()`/`tools_map` leben hier.


def test_mcp_write_records_the_writing_principal_and_leaves_assignee_alone(tools_map, store, tmp_path):
    """T8: A legt eine Aufgabe in einem geteilten Space an und setzt `assignee` auf sich, B
    aendert spaeter nur den Titel. Danach gilt: **`updated_by` ist B, `assignee` weiter A.**

    Genau diese beiden Haelfaften sind die Aussage des Blocks. Ein Test, der nur `updated_by`
    prueft, wuerde durch eine Implementierung bestehen, die bei jedem Schreibvorgang auch
    `assignee` ueberschreibt — und das waere die Zerstoerung von Lock P9-Z, die niemand
    bemerkt, weil beide Felder plausible Werte tragen."""
    _write_share_yml(tmp_path / SPACE_B, f"write: [{SPACE_A}]\n")
    item = store.create(
        SPACE_B, type="task", title="Angebot schreiben", folder="", assignee=SPACE_A,
        actor=SPACE_A,
    )

    with _as(SPACE_B):
        receipt = json.loads(
            tools_map["update_item"](item.id, version=item.version, title="Angebot schreiben (neu)")
        )

    assert receipt["updated_by"] == SPACE_B
    assert receipt["version"] == item.version + 1
    aktualisiert = store.get(item.id)
    assert aktualisiert.updated_by == SPACE_B
    assert aktualisiert.assignee == SPACE_A, "der Assignee gehoert A, B hat ihn nicht angefasst"


def test_both_write_tools_carry_the_assignee_hint_verbatim(described_mcp):
    """T9: `_ASSIGNEE_HINT` steht **woertlich identisch** in `create_item` und `update_item`.

    Das ist der Lock P9-Z fuer den zweiten Client: der Server kann einem Agenten nicht
    beibringen, was „in Arbeit" bedeutet, also steht die Regel im Text, den der Agent liest.
    Zwei Wortlautvarianten wuerden zwei Regeln sein — und eine davon gewinnt, ohne dass es
    jemand gemerkt haette."""
    for name in ("create_item", "update_item"):
        assert tools._ASSIGNEE_HINT in _description_of(described_mcp, name), name
    # Und die Regel sagt beides: setzen **und** nicht ueberschreiben. Nur die erste Haelfte
    # zu pruefen haette eine Implementierung passieren lassen, die fremde Aufgaben klaut.
    assert "überschreibst" in tools._ASSIGNEE_HINT
    assert "updated_by setzt der Server" in tools._ASSIGNEE_HINT


def test_all_five_write_tools_carry_the_format_hint_verbatim(described_mcp):
    """P10.5 Block 11, Schritt 11.6 (ED-3): die **Format-Konvention** steht woertlich
    identisch in allen **fuenf** Werkzeugen, die einen Body schreiben.

    Dieselbe Begründung wie bei `_ASSIGNEE_HINT`: die Formate sind eine Konvention
    zwischen Client und Mensch, und der Agent liest den Text, in dem sie steht. Fuenf
    Werkzeuge mit fuenf Wortlautvarianten wären fuenf Regeln — und eine davon gewinnt,
    ohne dass es jemand gemerkt haette.

    Der Server **prueft** die Form nicht und **wandelt** sie nicht um: er speichert
    `[Text]{.rot}` als das, was es ist. Der Hinweis ist eine Anweisung an den Client,
    keine Zusage des Servers."""
    for name in ("create_item", "update_item", "append_to_item", "append_to_items",
                 "patch_item"):
        assert tools._FORMAT_HINT in _description_of(described_mcp, name), name
    # Das Vokabular muss **vollstaendig** benannt sein: ein Agent, der eine Klasse erfindet,
    # schreibt etwas, das woertlich bleibt.
    for name in ("rot", "blau", "gruen", "gelb", "klein", "normal", "gross",
                 "links", "zentriert", "rechts"):
        assert f".{name}" in tools._FORMAT_HINT, name


def test_no_mcp_tool_accepts_updated_by(tools_map):
    """P9-AA ueber MCP: `update_item` und `create_item` haben **keinen** `updated_by`-Parameter.
    Ueber FastMCP laeuft ein unbekanntes Argument als Tool-Fehler, nicht als stiller
    Verzicht — der Agent kann es also gar nicht erst losschicken, ohne es zu merken."""
    import inspect

    for name in ("create_item", "update_item"):
        parameter = inspect.signature(tools_map[name]).parameters
        assert "updated_by" not in parameter, f"{name} hat einen updated_by-Parameter"
    with _as(SPACE_A):
        with pytest.raises(Exception) as excinfo:
            tools_map["update_item"]("itm_00000000", version=1, title="x", updated_by="fabian")
    assert "updated_by" in str(excinfo.value) or "unexpected" in str(excinfo.value).lower()


def test_read_paths_and_the_receipt_carry_updated_by(tools_map, store):
    """P9-72: `search_items`, `get_item_meta` und die Schreibquittung tragen den Schreiber.
    Der Volltext-Pfad (`return_body=True`) ist durch T12 in P9 Step F bereits fuer `assignee`
    abgesichert und hier derselbe Weg — `item_to_filetext()` bekommt dieselbe Zeile."""
    item = store.create(SPACE_A, type="task", title="Rechnung", actor=SPACE_A)

    with _as(SPACE_A):
        treffer = json.loads(tools_map["search_items"]())
        meta = json.loads(tools_map["get_item_meta"](item.id))
        quittung = tools_map["update_item"](item.id, version=item.version, title="Rechnung II")
        volltext = tools_map["update_item"](
            item.id, version=item.version + 1, title="Rechnung III", return_body=True
        )

    assert treffer["items"][0]["updated_by"] == SPACE_A
    assert meta["updated_by"] == SPACE_A
    # Die **Standard**-Antwort eines Schreibvorgangs ist die Quittung (P6-H), nicht der
    # Dateitext — beide sind geprueft, weil ein Agent je nach Aufruf die eine oder die andere
    # sieht. `return_body=True` holt denselben Inhalt als YAML-Frontmatter.
    assert json.loads(quittung)["updated_by"] == SPACE_A
    assert "updated_by: alpha" in volltext


# -- P10.5 Block 9: RE-7 `created_by` (P1-Öffnung 12) -------------------------------------
#
# Der MCP-Pfad hat **drei** Leseflächen, und alle drei muessen dasselbe zeigen: die
# Trefferliste (`search_items`), die Metadaten-Ansicht (`get_item_meta`) und der
# Volltext (`item_to_filetext()`, `return_body=True`). Ein Feld, das auf einer Flaeche lesbar
# ist und auf der anderen fehlt, ist genau die Divergenz, die P9 Step F als F10 aufgedeckt hat
# (`assignee` in `_summary()`) und P9-72 fuer `updated_by`.


def test_get_item_meta_shows_created_by(tools_map, store):
    """`get_item_meta` nennt den Anleger — und der kommt aus dem **Token**, nicht aus dem
    Aufruf: das Werkzeug hat keinen `created_by`-Parameter (das Waechter
    `test_no_mcp_tool_accepts_updated_by` deckt das fuer `updated_by` ab, `created_by` ist
    derselbe Fall und wird hiermit genauso behandelt)."""
    item = store.create(SPACE_A, type="task", title="Rechnung", actor=SPACE_A)

    with _as(SPACE_A):
        meta = json.loads(tools_map["get_item_meta"](item.id))

    assert meta["created_by"] == SPACE_A


def test_the_read_paths_carry_created_by(tools_map, store):
    """Alle drei Leseflaechen nennen den Anleger: die Trefferliste, die Metadaten und der
    Volltext. Der Volltext ist der Weg, den `create_item(return_body=True)` zurueckgibt — er
    muss die Datei **zeichengleich** abbilden, sonst behauptet das Werkzeug etwas anderes, als
    es geschrieben hat (`item_to_filetext()` vs. `storage.store._item_to_text()`)."""
    item = store.create(SPACE_A, type="task", title="Rechnung", actor=SPACE_A)

    with _as(SPACE_A):
        treffer = json.loads(tools_map["search_items"]())
        meta = json.loads(tools_map["get_item_meta"](item.id))
        volltext = tools_map["update_item"](
            item.id, version=item.version, title="Rechnung II", return_body=True
        )

    assert treffer["items"][0]["created_by"] == SPACE_A
    assert meta["created_by"] == SPACE_A
    assert "created_by: alpha" in volltext


def test_no_mcp_tool_accepts_created_by(tools_map, store):
    """**Kein** Werkzeug nimmt `created_by` an — weder beim Anlegen noch beim Aendern. Der Wert
    ist serververwaltet (`store._SYSTEM_MANAGED_FIELDS`); ein Agent, der sich als jemand anderes
    ausgeben will, bekommt eine **laute** Ablehnung, keine stille Fehlannahme."""
    with pytest.raises(Exception) as excinfo:
        tools_map["create_item"](type="task", title="Erfunden", created_by="beta")
    assert "created_by" in str(excinfo.value) or "unexpected" in str(excinfo.value).lower()

    item = store.create(SPACE_A, type="task", title="Echt", actor=SPACE_A)
    with _as(SPACE_A):
        with pytest.raises(Exception) as excinfo:
            tools_map["update_item"](item.id, version=item.version, created_by="beta")
    assert "created_by" in str(excinfo.value) or "unexpected" in str(excinfo.value).lower()
