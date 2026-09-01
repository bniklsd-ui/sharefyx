"""Phase 8 Block B Step B2 (P8-M, achte P1-Contract-Oeffnung).

Tests fuer `storage.index.replace_item_links` / `all_links` und die `item_links`-Tabelle
(Schema-Block, Rebuild-Verhalten, Delete-Cascade).
"""
from __future__ import annotations

import pytest

from storage import index
from storage.frontmatter import serialize


def _write_item(data_root, space, item_id, slug, *, title, links=None, body="Body.\n"):
    space_dir = data_root / space
    space_dir.mkdir(parents=True, exist_ok=True)
    fields = {
        "id": item_id,
        "space": space,
        "type": "note",
        "title": title,
        "status": "active",
        "tags": [],
        "links": links or [],
        "created": "2026-09-01T12:00:00Z",
        "updated": "2026-09-01T12:00:00Z",
        "version": 1,
    }
    path = space_dir / f"{item_id}__{slug}.md"
    path.write_text(serialize(fields, body))
    return path


# --- replace_item_links: Grundverhalten ---------------------------------------------------

def _all_links_as_tuples(conn):
    """Helper: `all_links` liefert `sqlite3.Row` (wie `all_rows`), die Tests hier wollen
    Tupel -- konsistent mit `Store.links_all()`s `list[tuple[str, str, str]]`-Vertrag."""
    return [(r["src_id"], r["dst_id"], r["kind"]) for r in index.all_links(conn)]


def test_replace_item_links_empty_list_removes_all_edges(tmp_path):
    """Phase 8 B2 (P8-M): `replace_item_links(conn, src_id, [])` entfernt saemtliche Kanten
    dieses Items -- dieselbe Semantik wie ein expliziter DELETE."""
    conn, _ = index.connect(tmp_path / ".index.sqlite3")
    index.replace_item_links(conn, "itm_a1b2c3d4", [
        ("itm_11111111", "frontmatter"),
        ("itm_22222222", "body"),
    ])
    assert len(index.all_links(conn)) == 2

    index.replace_item_links(conn, "itm_a1b2c3d4", [])
    assert index.all_links(conn) == []


def test_replace_item_links_is_destructive_not_additive(tmp_path):
    """Phase 8 B2 (P8-M): zweimal `replace_item_links` mit verschiedenen Zeilen -- die zweite
    ersetzt die erste vollstaendig, nichts bleibt stehen (anders als `upsert_item`'s
    ON CONFLICT-Verhalten)."""
    conn, _ = index.connect(tmp_path / ".index.sqlite3")
    index.replace_item_links(conn, "itm_src", [("itm_a", "body"), ("itm_b", "body")])
    index.replace_item_links(conn, "itm_src", [("itm_c", "frontmatter")])
    rows = _all_links_as_tuples(conn)
    assert rows == [("itm_src", "itm_c", "frontmatter")]


def test_replace_item_links_keeps_other_items_edges_intact(tmp_path):
    """Phase 8 B2 (P8-M): ein Aufruf auf src X fasst nicht die Kanten von src Y an."""
    conn, _ = index.connect(tmp_path / ".index.sqlite3")
    index.replace_item_links(conn, "itm_a", [("itm_target", "body")])
    index.replace_item_links(conn, "itm_b", [("itm_target", "frontmatter")])
    rows = sorted(_all_links_as_tuples(conn))
    assert rows == [
        ("itm_a", "itm_target", "body"),
        ("itm_b", "itm_target", "frontmatter"),
    ]


def test_replace_item_links_allows_same_dst_for_frontmatter_and_body(tmp_path):
    """Phase 8 B2 (P8-M): eine ID darf als Frontmatter- UND Body-Kante vom selben src existieren
    -- PK ist (src_id, dst_id, kind), nicht (src_id, dst_id)."""
    conn, _ = index.connect(tmp_path / ".index.sqlite3")
    index.replace_item_links(conn, "itm_src", [
        ("itm_target", "frontmatter"),
        ("itm_target", "body"),
    ])
    rows = sorted(_all_links_as_tuples(conn))
    assert rows == [
        ("itm_src", "itm_target", "body"),
        ("itm_src", "itm_target", "frontmatter"),
    ]


# --- row_from_file: body_refs werden mitgeliefert ---------------------------------------

def test_row_from_file_returns_body_refs_for_existing_links(tmp_path):
    """Phase 8 B2 (P8-M): `row_from_file` zieht body-Referenzen mit, damit `rebuild_index`
    ohne zweiten Datei-Read auskommt."""
    body = "Vor itm_a1b2c3d4 und itm_e5f6a7b8 nach."
    path = _write_item(tmp_path, "nikinger", "itm_77777777", "src",
                       title="Quelle", body=body)
    row = index.row_from_file(tmp_path, path)
    assert row["body_refs"] == ["itm_a1b2c3d4", "itm_e5f6a7b8"]


def test_row_from_file_body_refs_dedupes_repeated(tmp_path):
    path = _write_item(tmp_path, "nikinger", "itm_77777777", "src",
                       title="Quelle", body="itm_a1b2c3d4 itm_a1b2c3d4 itm_a1b2c3d4")
    row = index.row_from_file(tmp_path, path)
    assert row["body_refs"] == ["itm_a1b2c3d4"]


def test_row_from_file_body_refs_empty_when_no_refs(tmp_path):
    path = _write_item(tmp_path, "nikinger", "itm_77777777", "src",
                       title="Quelle", body="Reine Prosa ohne jede Referenz.")
    row = index.row_from_file(tmp_path, path)
    assert row["body_refs"] == []


# --- rebuild_index: item_links-Tabelle wird mit aufgefuellt ----------------------------

def test_rebuild_index_populates_item_links_from_files(tmp_path):
    """Phase 8 B2 (P8-M): Voll-Rebuild fuegt `item_links`-Zeilen aus Frontmatter (`links:`) +
    Body (mechanisch) ein. Beleg fuer Hard Rule 2 -- der Index darf jederzeit geloescht und
    vollstaendig aus den Dateien rekonstruiert werden."""
    _write_item(tmp_path, "nikinger", "itm_11111111", "src",
                title="Quelle", links=["itm_22222222"], body="Siehe itm_33333333.")
    _write_item(tmp_path, "nikinger", "itm_22222222", "fm",
                title="FM-Target")
    _write_item(tmp_path, "nikinger", "itm_33333333", "bd",
                title="Body-Target")

    conn, _ = index.connect(tmp_path / ".index.sqlite3")
    stats = index.rebuild_index(tmp_path, conn)
    assert stats.items_indexed == 3

    rows = sorted(_all_links_as_tuples(conn))
    assert rows == [
        ("itm_11111111", "itm_22222222", "frontmatter"),
        ("itm_11111111", "itm_33333333", "body"),
    ]


def test_rebuild_index_ignores_non_itm_strings_in_links_field(tmp_path):
    """Phase 8 B2 (P8-M): `links:` darf beliebige Strings enthalten -- nur voll-ID-matches
    werden zur Kante. `https://example.com` ist erlaubt und keine Kante."""
    _write_item(tmp_path, "nikinger", "itm_11111111", "src",
                title="Quelle",
                links=["itm_22222222", "https://example.com", "kein itm"],
                body="")
    conn, _ = index.connect(tmp_path / ".index.sqlite3")
    index.rebuild_index(tmp_path, conn)
    rows = sorted(_all_links_as_tuples(conn))
    assert rows == [("itm_11111111", "itm_22222222", "frontmatter")]


def test_rebuild_index_full_wipe_clears_old_links(tmp_path):
    """Phase 8 B2 (P8-M): Rebuild ist destruktiv fuer ALLE `item_links` -- nicht nur die
    Kanten der geloeschten Items. Sonst wuerden stale Kanten aus dem Vor-Stand stehen
    bleiben."""
    _write_item(tmp_path, "nikinger", "itm_11111111", "src",
                title="Quelle", links=["itm_22222222"], body="")
    conn, _ = index.connect(tmp_path / ".index.sqlite3")
    index.rebuild_index(tmp_path, conn)
    assert len(index.all_links(conn)) == 1

    # Komplette Datei loeschen, neu rebuilden -- Kante muss weg sein.
    (tmp_path / "nikinger" / "itm_11111111__src.md").unlink()
    index.rebuild_index(tmp_path, conn)
    assert index.all_links(conn) == []


def test_rebuild_index_dangling_dst_does_not_crash(tmp_path):
    """Phase 8 B2 (P8-M): eine Datei darf eine ID nennen, die (noch) nicht existiert -- das
    ist kein Fehler, der API-Endpoint filtert das beim Lesen."""
    _write_item(tmp_path, "nikinger", "itm_11111111", "src",
                title="Quelle", body="Verweist auf itm_deadbee0.")
    conn, _ = index.connect(tmp_path / ".index.sqlite3")
    index.rebuild_index(tmp_path, conn)
    rows = _all_links_as_tuples(conn)
    assert len(rows) == 1
    assert rows[0] == ("itm_11111111", "itm_deadbee0", "body")


# --- delete_item: src-Zeilen raeumen -----------------------------------------------------

def test_delete_item_clears_outgoing_edges(tmp_path):
    """Phase 8 B2 (P8-M): `delete_item` entfernt auch die `item_links`-Zeilen mit dieser
    `src_id` -- dangling edges bleiben, weil die API beim Lesen filtert."""
    conn, _ = index.connect(tmp_path / ".index.sqlite3")
    index.replace_item_links(conn, "itm_victim", [
        ("itm_x", "body"),
        ("itm_y", "frontmatter"),
    ])
    index.replace_item_links(conn, "itm_other", [
        ("itm_z", "body"),
    ])
    # delete_item loescht blind -- die items-Zeile muss dafuer nicht existieren (kein FK).
    # Die src-Zeilen aus itm_victim werden trotzdem entfernt, itm_other bleibt unangetastet.
    index.delete_item(conn, "itm_victim")
    rows = sorted(_all_links_as_tuples(conn))
    assert rows == [("itm_other", "itm_z", "body")]


# --- all_links: Sortierung & Vollstaendigkeit --------------------------------------------

def test_all_links_returns_sorted_output(tmp_path):
    conn, _ = index.connect(tmp_path / ".index.sqlite3")
    index.replace_item_links(conn, "itm_z", [("itm_target", "body")])
    index.replace_item_links(conn, "itm_a", [("itm_target", "frontmatter")])
    rows = _all_links_as_tuples(conn)
    # (src_id, kind, dst_id) Sortierung.
    assert rows[0] == ("itm_a", "itm_target", "frontmatter")
    assert rows[1] == ("itm_z", "itm_target", "body")
