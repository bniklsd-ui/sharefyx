import os
import threading
from datetime import date, datetime, timedelta, timezone

import pytest

from storage.errors import ConflictError, ItemNotFound, ValidationError
from storage.store import Store


@pytest.fixture
def clock():
    state = {"now": datetime(2026, 7, 24, 18, 0, 0, tzinfo=timezone.utc)}

    def now_fn():
        return state["now"]

    def advance(seconds=1):
        state["now"] += timedelta(seconds=seconds)

    now_fn.advance = advance
    return now_fn


@pytest.fixture
def store(tmp_path, clock):
    return Store(tmp_path, now_fn=clock, git=False)


# -- Die vier Pflicht-Tests aus Plan §4 Step 4 --------------------------------------------


def test_1_sequential_update_with_stale_version_raises_conflict(store):
    item = store.create("nikinger", type="task", title="Kühlschrank prüfen")
    store.update(item.id, version=item.version, title="Kühlschrank geputzt")

    with pytest.raises(ConflictError) as exc_info:
        store.update(item.id, version=item.version, title="Nochmal geändert")

    err = exc_info.value
    assert err.item_id == item.id
    assert err.expected_version == item.version
    assert err.current.title == "Kühlschrank geputzt"
    assert err.current.version == item.version + 1


def test_2_external_edit_is_detected_bumps_version_then_conflicts(store, tmp_path):
    item = store.create("nikinger", type="note", title="Einkaufsliste", body="Milch\n")
    path = tmp_path / "nikinger" / f"{item.id}__einkaufsliste.md"
    assert path.exists()

    original_text = path.read_text()
    path.write_text(original_text.replace("Milch", "Milch, Butter"))
    # mtime muss sich sichtbar unterscheiden, unabhängig von der Dateisystem-Auflösung.
    later = path.stat().st_mtime + 5
    os.utime(path, (later, later))

    fetched = store.get(item.id)
    assert "Milch, Butter" in fetched.body
    assert fetched.version == item.version + 1

    with pytest.raises(ConflictError):
        store.update(item.id, version=item.version, title="Sollte scheitern")


def test_3_concurrent_update_from_two_threads_exactly_one_wins(store):
    item = store.create("nikinger", type="task", title="Wettlauf")
    results: list[tuple[str, object]] = []
    barrier = threading.Barrier(2)

    def attempt(title):
        barrier.wait()
        try:
            results.append(("ok", store.update(item.id, version=item.version, title=title)))
        except ConflictError as exc:
            results.append(("conflict", exc))

    threads = [threading.Thread(target=attempt, args=(f"Titel {i}",)) for i in range(2)]
    for t in threads:
        t.start()
    for t in threads:
        t.join()

    outcomes = [kind for kind, _ in results]
    assert outcomes.count("ok") == 1
    assert outcomes.count("conflict") == 1

    final = store.get(item.id)
    assert final.version == item.version + 1


def test_4_update_on_archived_item_raises_instead_of_reactivating(store):
    item = store.create("nikinger", type="task", title="Erledigt")
    archived = store.archive(item.id, version=item.version)
    assert archived.status == "archived"

    with pytest.raises(ValidationError):
        store.update(archived.id, version=archived.version, status="open")

    still_archived = store.get(archived.id)
    assert still_archived.status == "archived"


# -- Grundlegende API-Abdeckung ------------------------------------------------------------


def test_create_defaults_status_by_type(store):
    task = store.create("nikinger", type="task", title="Task")
    note = store.create("nikinger", type="note", title="Note")
    assert task.status == "open"
    assert note.status == "active"


def test_create_rejects_system_managed_fields(store):
    with pytest.raises(ValidationError):
        store.create("nikinger", type="task", title="X", version=99)


def test_update_rejects_system_managed_fields(store):
    item = store.create("nikinger", type="task", title="X")
    with pytest.raises(ValidationError):
        store.update(item.id, version=item.version, created="2000-01-01T00:00:00Z")


def test_get_raises_item_not_found(store):
    with pytest.raises(ItemNotFound):
        store.get("itm_deadbeef")


def test_due_accepts_iso_string_and_date_object(store):
    a = store.create("nikinger", type="task", title="A", due="2026-08-02")
    b = store.create("nikinger", type="task", title="B", due=date(2026, 8, 3))
    assert a.due == date(2026, 8, 2)
    assert b.due == date(2026, 8, 3)


def test_update_preserves_extra_fields_across_writes(store, tmp_path):
    item = store.create("nikinger", type="note", title="Mit Zusatzfeld", eigenes_feld="bleibt")
    assert item.extra == {"eigenes_feld": "bleibt"}

    updated = store.update(item.id, version=item.version, title="Umbenannt")
    assert updated.extra == {"eigenes_feld": "bleibt"}

    path = tmp_path / "nikinger" / f"{item.id}__umbenannt.md"
    assert "eigenes_feld: bleibt" in path.read_text()


def test_update_renames_file_on_title_change(store, tmp_path):
    item = store.create("nikinger", type="note", title="Alter Titel")
    old_path = tmp_path / "nikinger" / f"{item.id}__alter-titel.md"
    assert old_path.exists()

    store.update(item.id, version=item.version, title="Neuer Titel")

    new_path = tmp_path / "nikinger" / f"{item.id}__neuer-titel.md"
    assert new_path.exists()
    assert not old_path.exists()


def test_append_adds_text_and_bumps_version(store):
    item = store.create("nikinger", type="note", title="Log", body="Zeile 1")
    updated = store.append(item.id, version=item.version, text="Zeile 2")
    assert updated.body == "Zeile 1\nZeile 2"
    assert updated.version == item.version + 1


def test_archive_moves_file_and_sets_status(store, tmp_path):
    item = store.create("nikinger", type="task", title="Fertig")
    old_path = tmp_path / "nikinger" / f"{item.id}__fertig.md"

    archived = store.archive(item.id, version=item.version)

    assert archived.status == "archived"
    assert not old_path.exists()
    archive_path = tmp_path / "nikinger" / "_archive" / f"{item.id}__fertig.md"
    assert archive_path.exists()


def test_list_spaces_counts_items(store):
    store.create("nikinger", type="task", title="A")
    store.create("nikinger", type="task", title="B")
    store.create("kollege", type="note", title="C")

    spaces = {s.name: s.item_count for s in store.list_spaces()}
    assert spaces == {"nikinger": 2, "kollege": 1}


def test_search_returns_summaries_not_full_bodies(store):
    store.create("nikinger", type="task", title="Findbar", tags=["infra"], body="X" * 500)
    store.create("nikinger", type="task", title="Anderes")

    result = store.search("Findbar")

    assert result.total == 1
    assert result.items[0].title == "Findbar"
    assert len(result.items[0].snippet) < 500
    assert not hasattr(result.items[0], "body")


def test_search_filters_by_space_type_status_tag(store):
    store.create("nikinger", type="task", title="A", tags=["work"])
    store.create("nikinger", type="note", title="B", tags=["personal"])
    store.create("kollege", type="task", title="C", tags=["work"])

    result = store.search(space="nikinger", type="task", tag="work")
    assert [i.title for i in result.items] == ["A"]


def test_rebuild_index_repopulates_from_files(store, tmp_path):
    store.create("nikinger", type="task", title="A")
    store.create("nikinger", type="task", title="B")

    stats = store.rebuild_index()
    assert stats.items_indexed == 2
