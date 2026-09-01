"""Phase 8 Block B Step B2 (P8-M, achte P1-Contract-Oeffnung).

Store-Tests fuer `item_links`-Integration: jeder Schreibpfad (create/update/patch/append/
move/archive) ruft intern `_write_item_file` -> `_replace_links_for_item`. Hier wird der
Kreis ueber `Store.links_all()` und ueber die Endpersistenz (Rebuild) geschlossen.
"""
from __future__ import annotations

import pytest

from storage.store import Store


@pytest.fixture
def clock():
    import datetime
    now = datetime.datetime(2026, 9, 1, 12, 0, 0, tzinfo=datetime.timezone.utc)

    def _now():
        return now
    return _now


@pytest.fixture
def store(tmp_path, clock):
    return Store(tmp_path, now_fn=clock)


def test_create_writes_frontmatter_and_body_links(store):
    """Phase 8 B2: nach `create(...)` mit `links=[...]` und einer Body-Referenz sind beide
    Kanten in `links_all()` sichtbar."""
    item = store.create(
        "nikinger", type="note", title="Quelle",
        links=["itm_deadbee0"],
        body="Siehe itm_cafe0000.",
    )
    links = sorted(store.links_all())
    assert links == [
        ("itm_11111111" if False else item.id, "itm_cafe0000", "body"),
        (item.id, "itm_deadbee0", "frontmatter"),
    ]


def test_create_ignores_non_itm_strings_in_links(store):
    """Phase 8 B2: `links:` darf beliebige Strings fuehren -- nur valide IDs werden Kanten."""
    item = store.create(
        "nikinger", type="note", title="Quelle",
        links=["itm_deadbee0", "https://example.com", "kein itm"],
        body="",
    )
    links = sorted(store.links_all())
    assert links == [(item.id, "itm_deadbee0", "frontmatter")]


def test_update_replaces_full_link_set(store):
    """Phase 8 B2: ein `update(links=[...])` ersetzt die Frontmatter-Kanten vollstaendig,
    Body-Kanten bleiben unangetastet (sie werden mechanisch aus dem Body extrahiert, nicht
    aus dem PATCH)."""
    item = store.create(
        "nikinger", type="note", title="Quelle",
        links=["itm_deadbee0"],
        body="Referenz itm_cafe0000.",
    )
    updated = store.update(
        item.id, version=item.version,
        links=["itm_11111111"],
        body="Body mit itm_cafe0000.",
    )
    links = sorted(store.links_all())
    # Frontmatter neu (deadbee0 weg, 11111111 da), Body bleibt (cafe0000 weiter im Body).
    assert links == [
        (item.id, "itm_11111111", "frontmatter"),
        (item.id, "itm_cafe0000", "body"),
    ]


def test_append_body_link_picks_up_new_references(store):
    """Phase 8 B2: `append(text=...)` ergaenzt den Body -- neue Body-Referenzen tauchen in
    `links_all()` auf."""
    item = store.create(
        "nikinger", type="note", title="Quelle",
        body="Anfang.",
        links=[],
    )
    store.append(item.id, version=item.version, text="Neu: itm_cafe0000.")
    links = list(store.links_all())
    assert (item.id, "itm_cafe0000", "body") in links


def test_patch_body_text_recomputes_links(store):
    """Phase 8 B2: `patch(old_text=, new_text=)` ersetzt eine Textstelle im Body -- wenn die
    alte Stelle eine Referenz war und die neue nicht, muss die Kante verschwinden, und
    umgekehrt."""
    item = store.create(
        "nikinger", type="note", title="Quelle",
        body="Siehe itm_cafe0000.",
        links=[],
    )
    assert (item.id, "itm_cafe0000", "body") in list(store.links_all())

    # itm_cafe0000 -> itm_deadbee0 ersetzen.
    store.patch(item.id, version=item.version, edits=[
        {"old_text": "itm_cafe0000", "new_text": "itm_deadbee0"},
    ])

    links = list(store.links_all())
    assert (item.id, "itm_cafe0000", "body") not in links
    assert (item.id, "itm_deadbee0", "body") in links


def test_archive_keeps_edges_for_archived_item(store):
    """Phase 8 B2: archive() ruft ebenfalls `_write_item_file` -> Kanten bleiben erhalten,
    ein archiviertes Item kann weiterhin als Quelle in der Graph-Ansicht erscheinen."""
    item = store.create(
        "nikinger", type="note", title="Quelle",
        links=["itm_deadbee0"],
        body="",
    )
    archived = store.archive(item.id, version=item.version)
    assert archived.status == "archived"
    links = list(store.links_all())
    assert (item.id, "itm_deadbee0", "frontmatter") in links


def test_move_preserves_link_set_unchanged(store):
    """Phase 8 B2: move() ruft ebenfalls `_write_item_file` -> Kantenmenge bleibt identisch
    (es ist kein Inhalt geaendert worden)."""
    (store._data_root / "fabian").mkdir()
    item = store.create(
        "nikinger", type="note", title="Quelle",
        links=["itm_deadbee0"],
        body="Siehe itm_cafe0000.",
    )
    store.move(item.id, version=item.version, space="fabian")
    links = sorted(store.links_all())
    assert links == [
        (item.id, "itm_cafe0000", "body"),
        (item.id, "itm_deadbee0", "frontmatter"),
    ]


def test_rebuild_round_trip_preserves_all_edges(store):
    """Phase 8 B2: nach `rebuild_index()` sind ALLE Kanten aus den Dateien wiederhergestellt
    -- Beweis fuer Hard Rule 2 (Index = Ableitung, vollstaendig rekonstruierbar)."""
    item = store.create(
        "nikinger", type="note", title="Quelle",
        links=["itm_deadbee0"],
        body="Siehe itm_cafe0000 und nochmal itm_cafe0000.",
    )
    expected = sorted(store.links_all())

    store.rebuild_index()

    assert sorted(store.links_all()) == expected


def test_drift_repair_updates_body_links(store, tmp_path):
    """Phase 8 B2: ein externer Body-Edit (Mensch im Editor) aendert die Body-Referenzen --
    `get()` ruft `_reconcile_and_get_row`, das die `item_links`-Tabelle anpasst."""
    item = store.create(
        "nikinger", type="note", title="Quelle",
        body="Erst itm_cafe0000.",
        links=[],
    )
    assert (item.id, "itm_cafe0000", "body") in list(store.links_all())

    # Mensch editiert die Datei direkt: Body-Referenz entfernt, dafuer eine neue.
    md_path = tmp_path / "nikinger" / f"{item.id}__quelle.md"
    text = md_path.read_text(encoding="utf-8")
    # Ersetze die alte Referenz durch eine neue, halbiere die mtime/size-Spuren (pyfakefs hier
    # zu umstaendlich; stattdessen direkt nach dem Edit `get()` aufrufen -- das veranlasst
    # `reconcile_and_get_row`).
    new_body = text.replace("itm_cafe0000", "itm_deadbee0")
    md_path.write_text(new_body, encoding="utf-8")
    # mtime explizit nach vorn setzen, sonst sieht reconcile den Edit nicht
    import os
    os.utime(md_path, (md_path.stat().st_atime, md_path.stat().st_mtime + 5))

    store.get(item.id)

    links = list(store.links_all())
    assert (item.id, "itm_cafe0000", "body") not in links
    assert (item.id, "itm_deadbee0", "body") in links
