import json
import logging
import os
import shutil
import subprocess
import threading
from dataclasses import asdict
from datetime import date, datetime, timedelta, timezone

import pytest

from storage.errors import ConflictError, ItemNotFound, ValidationError
from sharefyx_image_bytes import png_bytes
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


@pytest.fixture
def store_git(tmp_path, clock):
    return Store(tmp_path, now_fn=clock, git=True)


def test_data_root_property_returns_the_configured_root(tmp_path, clock):
    store = Store(tmp_path, now_fn=clock, git=False)
    assert store.data_root == tmp_path


def _git_log(tmp_path) -> list[str]:
    """Commit-Messages newest-first, wie `git log` sie liefert."""
    result = subprocess.run(
        ["git", "-C", str(tmp_path), "log", "--format=%s"],
        capture_output=True, text=True, check=True,
    )
    return result.stdout.strip().splitlines()


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


def test_search_sort_order_locks_status_then_due_then_updated_desc(store, clock):
    """Plan §4 Step 6 macht die Sortierung verbindlich (war seit Step 4 ein Platzhalter,
    ungetestet). Reihenfolge: (1) offener Status (`open`/`active`) vor allem anderen,
    (2) innerhalb dessen `due` aufsteigend, kein `due` sortiert zuletzt, (3) bei gleichem
    `due` der zuletzt aktualisierte zuerst.
    """
    early = store.create("nikinger", type="task", title="Early", due="2026-08-01")
    late = store.create("nikinger", type="task", title="Late", due="2026-09-01")
    no_due = store.create("nikinger", type="task", title="NoDue")
    done = store.create("nikinger", type="task", title="Done", due="2026-07-25")
    store.update(done.id, version=done.version, status="done")

    # gleiches due wie 'early', aber zuletzt aktualisiert -> muss vor 'early' stehen
    clock.advance(10)
    same_due_newer = store.create("nikinger", type="task", title="SameDueNewer", due="2026-08-01")

    result = store.search(space="nikinger", limit=50)
    titles = [i.title for i in result.items]

    assert titles == ["SameDueNewer", "Early", "Late", "NoDue", "Done"]


def test_search_filters_by_space_type_status_tag(store):
    store.create("nikinger", type="task", title="A", tags=["work"])
    store.create("nikinger", type="note", title="B", tags=["personal"])
    store.create("kollege", type="task", title="C", tags=["work"])

    result = store.search(space="nikinger", type="task", tag="work")
    assert [i.title for i in result.items] == ["A"]


def test_search_default_does_not_match_body_only_text(store):
    store.create("nikinger", type="note", title="Titel", body="EinBodyMarkerXYZ")

    result = store.search("EinBodyMarkerXYZ")

    assert result.total == 0


def test_search_in_body_true_matches_body_only_text(store):
    item = store.create("nikinger", type="note", title="Titel", body="EinBodyMarkerXYZ")

    result = store.search("EinBodyMarkerXYZ", in_body=True)

    assert [i.id for i in result.items] == [item.id]


def test_search_in_body_true_does_not_change_sort_or_total_for_title_matches(store, clock):
    # P6.5-U-Nebenbedingung: in_body=True darf ein bestehendes Titel-Match-Verhalten nicht
    # verändern -- derselbe Sortier-/Total-Pfad läuft in beiden Fällen.
    a = store.create("nikinger", type="task", title="Treffer A")
    clock.advance(1)
    b = store.create("nikinger", type="task", title="Treffer B")

    without = store.search("Treffer")
    with_body = store.search("Treffer", in_body=True)

    assert without.total == with_body.total == 2
    assert [i.id for i in without.items] == [i.id for i in with_body.items] == [b.id, a.id]


def test_search_listing_of_30_items_stays_within_calibrated_json_bound(store, clock):
    """Plan §4 Step 6 Done-when: 'Listing über 30 Items serialisiert zu <3 KB JSON'. Der
    3-KB-Schätzwert war `[VERIFY]` und ist gegen echte Beispieldaten empirisch widerlegt --
    schon der reine JSON-Rahmen von `ItemSummary` (12 Felder, leere Werte) kostet ~230 B/Item
    (~7 KB/30 Items), ein realistisches Item mit 2 Tags + kurzem Snippet ~345 B (~10.3 KB/30),
    das Maximum (3 Tags + voll ausgeschöpfter 160-Zeichen-Snippet) ~470 B (~14 KB/30) -- alle
    drei Stufen gemessen 2026-07-24 (Details im Session-stopped-Block der Phase-Head-Doku).
    3 KB ist bei diesem Feldsatz strukturell nicht erreichbar. Kalibrierter, hier verbindlich
    getesteter Wert: **12–16 KB** (Marge unter und über dem gemessenen Maximum).

    Nur die Ceiling-Stufe wird hier tatsächlich geprüft (feste Titel/Tags/Body, deterministische
    Uhr, nicht abhängig von dem, was `create()` gerade produziert -- sonst würde die Schwelle der
    Fixture hinterherlaufen statt etwas zu prüfen). Floor und Realistisch sind Out-of-Band-Messungen
    vom 2026-07-24, festgehalten im Session-stopped-Block, hier nicht mitgetestet -- diese
    einzelne Grenze schützt nicht alle drei Stufen. Die Untergrenze ist bewusst Teil der Assertion:
    ein Regression, der die Listing-Größe schrumpfen lässt (z.B. `snippet` verschwindet aus
    `ItemSummary` oder `_snippet`s Cap sinkt drastisch), soll auffallen -- das wäre eine
    `ItemSummary`-Feldsatz-Änderung und damit Nikinger-Sache, kein stiller Nebeneffekt.

    **[P9 Step F, 2026-09-30 — Neukalibrierung, Pflicht nach der eigenen Regel oben, mit
    Messung statt Schätzung]:** `ItemSummary` trägt seit Step F ein Feld mehr (`assignee`, F3),
    und dieser Docstring sagt ausdrücklich, dass eine Feldsatz-Änderung **kein stiller
    Nebeneffekt** sein darf -- deshalb die Zahlen hier und nicht bloß ein erhöhter Wert.
    Dieselbe Fixture, gemessen: **16.390 B** mit `assignee` gegen **16.300 B** ohne, also exakt
    **+16 B/Item** (`"assignee": "",` im Rahmen) und **559 B/Item** statt 543. Die alte
    Obergrenze 16 KB ist damit zu Recht rot geworden -- sie hat die echte Zunahme bemerkt.
    Neues Band **13–18 KB**: die Obergrenze behält ihre ~1,6 KB Marge über dem Messwert (vorher
    ~2 KB über 14 KB), die Untergrenze ihre ~3,4 KB darunter (vorher ~4 KB unter 15,9 KB). Die
    Untergrenze ist die eigentliche Wache: sie schlägt an, falls das Feld je wieder verschwindet.
    (Die 3-Tag-/Maximal-Stufe aus dem Docstring oben steigt entsprechend von ~470 auf ~486 B/Item.)
    """
    long_body = (
        "Ein realistischer Body-Text mit ein paar Saetzen, damit der Snippet auch wirklich "
        "etwas zu schneiden hat und nicht nur ein Wort lang ist. "
    ) * 2
    for i in range(30):
        store.create(
            "nikinger", type="task",
            title=f"Testaufgabe Nummer {i} mit etwas laengerem Titel",
            body=long_body, tags=["infra", "mcp", "phase1"], due="2026-08-02",
        )

    result = store.search(limit=50)
    payload = asdict(result)
    for item in payload["items"]:
        item["created"] = item["created"].strftime("%Y-%m-%dT%H:%M:%SZ")
        item["updated"] = item["updated"].strftime("%Y-%m-%dT%H:%M:%SZ")
    text = json.dumps(payload, default=str, ensure_ascii=False)

    size = len(text.encode("utf-8"))
    assert len(result.items) == 30
    assert 13 * 1024 < size < 18 * 1024


def test_rebuild_index_repopulates_from_files(store, tmp_path):
    store.create("nikinger", type="task", title="A")
    store.create("nikinger", type="task", title="B")

    stats = store.rebuild_index()
    assert stats.items_indexed == 2


def test_drift_bumped_version_survives_rebuild_index(store, tmp_path):
    """Regression: die durch Drift-Erkennung (Entscheidung D) erhöhte Version muss ins
    Frontmatter zurückgeschrieben werden. Täte sie das nicht, würde `rebuild_index()`
    (Entscheidung A, läuft laut Plan G bei jedem Start) sie lautlos wieder auf den alten
    Dateistand zurücksetzen — und das Konfliktschutz-Fenster erneut öffnen. Advisor-Fund,
    2026-07-24, siehe Session-stopped-Block.
    """
    item = store.create("nikinger", type="note", title="Einkaufsliste", body="Milch\n")
    path = tmp_path / "nikinger" / f"{item.id}__einkaufsliste.md"

    path.write_text(path.read_text().replace("Milch", "Milch, Butter"))
    later = path.stat().st_mtime + 5
    os.utime(path, (later, later))

    bumped = store.get(item.id)
    assert bumped.version == item.version + 1
    assert "version: 2" in path.read_text()

    store.rebuild_index()

    after_rebuild = store.get(item.id)
    assert after_rebuild.version == bumped.version


# -- Step 5: Git-Commit je Write -----------------------------------------------------------
#
# Die vier Pflicht-Tests oben bleiben bewusst auf `git=False` -- das ist Konfliktlogik, kein
# Git-Test. Diese Tests decken stattdessen Plan §4 Step 5 "Done when" ab: 3 Writes -> 3 Commits
# mit den erwarteten Messages, und ein kaputtes Git-Repo blockiert Writes nicht.


def test_git_enabled_commits_one_per_write_with_expected_messages(store_git, tmp_path):
    item = store_git.create("nikinger", type="task", title="Kühlschrank prüfen")
    updated = store_git.update(item.id, version=item.version, title="Kühlschrank geputzt")
    store_git.archive(updated.id, version=updated.version)

    log = _git_log(tmp_path)  # newest-first

    assert len(log) == 3
    assert log[2].startswith(f"create {item.id} [nikinger]")
    assert log[1].startswith(f"update {item.id} [nikinger]")
    assert log[0].startswith(f"archive {item.id} [nikinger]")


def test_git_enabled_append_commits_with_append_message(store_git, tmp_path):
    item = store_git.create("nikinger", type="note", title="Notiz", body="Zeile 1\n")
    store_git.append(item.id, version=item.version, text="Zeile 2")

    log = _git_log(tmp_path)

    assert log[0].startswith(f"append {item.id} [nikinger]")


def test_git_enabled_drift_rewrite_commits_with_drift_message(store_git, tmp_path):
    item = store_git.create("nikinger", type="note", title="Einkaufsliste", body="Milch\n")
    path = tmp_path / "nikinger" / f"{item.id}__einkaufsliste.md"
    path.write_text(path.read_text().replace("Milch", "Milch, Butter"))
    later = path.stat().st_mtime + 5
    os.utime(path, (later, later))

    store_git.get(item.id)  # triggert Drift-Erkennung (Entscheidung D) -> Version-Rewrite

    log = _git_log(tmp_path)

    assert log[0].startswith(f"drift {item.id} [nikinger]")


def test_git_enabled_broken_repo_does_not_block_write_and_logs_critical(
    store_git, tmp_path, caplog
):
    """Echt kaputtes Repo, kein Mock: `.git` wird durch eine gewöhnliche Datei ersetzt, jeder
    folgende `git`-Aufruf in diesem Verzeichnis schlägt fehl. Der Write muss trotzdem
    durchlaufen (Entscheidung E: Git-Fehler sind best-effort, nie fatal).
    """
    shutil.rmtree(tmp_path / ".git")
    (tmp_path / ".git").write_text("kaputt, kein Repo\n")

    with caplog.at_level(logging.CRITICAL, logger="storage.history"):
        item = store_git.create("nikinger", type="task", title="Trotzdem geschrieben")

    path = tmp_path / "nikinger" / f"{item.id}__trotzdem-geschrieben.md"
    assert path.exists()
    critical_records = [r for r in caplog.records if r.levelno == logging.CRITICAL]
    assert len(critical_records) >= 1


# -- P2 Step 2: P1-Contract-Erweiterungen (space_of, repair_drift, Statusvalidierung) ------

def test_space_of_returns_space(store):
    item = store.create("nikinger", type="task", title="X")
    assert store.space_of(item.id) == "nikinger"


def test_space_of_unknown_raises_item_not_found(store):
    with pytest.raises(ItemNotFound):
        store.space_of("itm_deadbeef")


def test_get_repair_drift_false_leaves_file_untouched(store, tmp_path):
    item = store.create("nikinger", type="note", title="Fremd gelesen", body="Original\n")
    path = tmp_path / "nikinger" / f"{item.id}__fremd-gelesen.md"

    original_text = path.read_text()
    path.write_text(original_text.replace("Original", "Verändert von außen"))
    later = path.stat().st_mtime + 5
    os.utime(path, (later, later))
    mtime_before = path.stat().st_mtime
    bytes_before = path.read_bytes()

    fetched = store.get(item.id, repair_drift=False)

    assert "Verändert von außen" in fetched.body
    assert fetched.version == item.version  # nicht gebumpt — Datei blieb unangetastet
    assert path.stat().st_mtime == mtime_before
    assert path.read_bytes() == bytes_before


def test_get_repair_drift_false_creates_no_commit(store_git, tmp_path):
    item = store_git.create("nikinger", type="note", title="Ohne Commit", body="Original\n")
    path = tmp_path / "nikinger" / f"{item.id}__ohne-commit.md"
    log_before = _git_log(tmp_path)

    original_text = path.read_text()
    path.write_text(original_text.replace("Original", "Verändert von außen"))
    later = path.stat().st_mtime + 5
    os.utime(path, (later, later))

    store_git.get(item.id, repair_drift=False)

    assert _git_log(tmp_path) == log_before


def test_get_repair_drift_true_still_bumps(store, tmp_path):
    item = store.create("nikinger", type="note", title="Muss bumpen", body="Original\n")
    path = tmp_path / "nikinger" / f"{item.id}__muss-bumpen.md"

    original_text = path.read_text()
    path.write_text(original_text.replace("Original", "Verändert von außen"))
    later = path.stat().st_mtime + 5
    os.utime(path, (later, later))

    fetched = store.get(item.id, repair_drift=True)

    assert fetched.version == item.version + 1


def test_create_rejects_unknown_status(store):
    with pytest.raises(ValidationError):
        store.create("nikinger", type="task", title="X", status="bogus")


def test_update_rejects_unknown_status(store):
    item = store.create("nikinger", type="task", title="X")
    with pytest.raises(ValidationError):
        store.update(item.id, version=item.version, status="bogus")


def test_update_accepts_valid_status_per_type(store):
    task = store.create("nikinger", type="task", title="T")
    updated_task = store.update(task.id, version=task.version, status="done")
    assert updated_task.status == "done"

    note = store.create("nikinger", type="note", title="N")
    updated_note = store.update(note.id, version=note.version, status="archived")
    assert updated_note.status == "archived"


# -- P6 Step 1: patch() (P6-E/F/G) ----------------------------------------------------------
#
# Plan §4 Step 1 nennt eine eigene Datei `phase6_shares/tests/test_store_patch.py` dafür --
# `phase1_storage/tests/conftest.py` ist aber leer (P1-Präzedenzfall, siehe dessen leeren
# Inhalt): `clock`/`store`/`store_git`/`_git_log` leben alle lokal in dieser Datei, eine
# fixture-lose Schwesterdatei könnte sie nicht sehen. Plan §5s Testliste sagt ohnehin
# "test_store.py -- erweitert", nicht "neue Datei" -- dieser Widerspruch wird zugunsten der
# Zusammenfassungstabelle aufgelöst, dieselbe Kategorie Drift wie in P6 Step 0 (siehe
# `phase6_shares/CLAUDE.md`s Session-Block). Die reinen `apply_edits()`-Funktionstests (ohne
# Store) stehen tatsächlich in `phase6_shares/tests/test_patch.py` -- die haben keine
# Fixture-Abhängigkeit und passen dort.


def test_patch_bumps_version_once_for_many_edits(store):
    item = store.create("nikinger", type="note", title="Multi-Patch", body="Alpha\nBeta\nGamma\n")

    result = store.patch(
        item.id, version=item.version,
        edits=[
            {"old_text": "Alpha", "new_text": "Erste"},
            {"old_text": "Beta", "new_text": "Zweite"},
            {"old_text": "Gamma", "new_text": "Dritte"},
        ],
    )

    assert result.item.version == item.version + 1
    assert result.replacements == 3
    assert result.lines == (1, 2, 3)
    assert result.item.body == "Erste\nZweite\nDritte\n"
    assert result.bytes_before == len("Alpha\nBeta\nGamma\n".encode("utf-8"))
    assert result.bytes_after == len("Erste\nZweite\nDritte\n".encode("utf-8"))


def test_patch_creates_exactly_one_git_commit(store_git, tmp_path):
    item = store_git.create("nikinger", type="note", title="Patch-Commit", body="X\n")
    commits_before = len(_git_log(tmp_path))

    store_git.patch(item.id, version=item.version, edits=[{"old_text": "X", "new_text": "Y"}])

    log = _git_log(tmp_path)
    assert len(log) - commits_before == 1
    assert log[0].startswith(f"patch {item.id} [nikinger]")


def test_patch_on_version_mismatch_raises_conflict_and_leaves_file_untouched(store, tmp_path):
    item = store.create("nikinger", type="note", title="Konflikt", body="Original\n")
    path = tmp_path / "nikinger" / f"{item.id}__konflikt.md"
    original_bytes = path.read_bytes()

    with pytest.raises(ConflictError):
        store.patch(item.id, version=999, edits=[{"old_text": "Original", "new_text": "Neu"}])

    assert path.read_bytes() == original_bytes


def test_patch_on_archived_item_is_rejected(store):
    item = store.create("nikinger", type="task", title="Erledigt", body="X\n")
    archived = store.archive(item.id, version=item.version)

    with pytest.raises(ValidationError):
        store.patch(
            archived.id, version=archived.version, edits=[{"old_text": "X", "new_text": "Y"}]
        )


def test_patch_preserves_unknown_frontmatter_fields(store, tmp_path):
    item = store.create(
        "nikinger", type="note", title="Mit Zusatzfeld", body="Original\n", eigenes_feld="bleibt"
    )

    result = store.patch(
        item.id, version=item.version, edits=[{"old_text": "Original", "new_text": "Geändert"}]
    )

    assert result.item.extra == {"eigenes_feld": "bleibt"}
    path = tmp_path / "nikinger" / f"{item.id}__mit-zusatzfeld.md"
    assert "eigenes_feld: bleibt" in path.read_text()


# -- P6 Step 4: folder/visibility/share_*, acl_of(), list_spaces() ------------------------


def test_create_with_folder_places_file_under_it(store, tmp_path):
    item = store.create("nikinger", type="note", title="Im Ordner", folder="projekte/alpha")
    assert item.folder == "projekte/alpha"
    path = tmp_path / "nikinger" / "projekte" / "alpha" / f"{item.id}__im-ordner.md"
    assert path.exists()
    assert store.get(item.id).folder == "projekte/alpha"


def test_create_with_status_archived_lands_directly_in_archive_and_drops_folder(store, tmp_path):
    # Siebte Contract-Öffnung (P7 Step C4): ein direkt als `archived` angelegtes Item (z. B.
    # über `POST /api/v1/items` mit `status="archived"`, `_items_post` erlaubt beide Felder)
    # landet sofort unter `_archive/`, ein mitgeschicktes `folder` wird verworfen -- dieselbe
    # Zurücksetzung, die `archive()` seit je her vornimmt, hier nur vorgezogen auf `create()`.
    item = store.create(
        "nikinger", type="note", title="Direkt Erledigt", status="archived", folder="projekte",
    )
    assert item.folder == ""
    assert item.status == "archived"
    path = tmp_path / "nikinger" / "_archive" / f"{item.id}__direkt-erledigt.md"
    assert path.exists()
    assert not (tmp_path / "nikinger" / "projekte").exists()
    assert store.get(item.id).folder == ""


def test_create_rejects_folder_deeper_than_max(store):
    with pytest.raises(ValidationError):
        store.create("nikinger", type="note", title="Zu tief", folder="a/b/c")


def test_ensure_folder_creates_empty_directory(store, tmp_path):
    result = store.ensure_folder("nikinger", "Projekte/Backend")
    assert result == "projekte/backend"  # slugifiziert wie jeder andere Ordnerpfad (P6-Q)
    assert (tmp_path / "nikinger" / "projekte" / "backend").is_dir()
    # Ein leeres Verzeichnis erzeugt kein Item -- list_spaces() sieht es trotzdem, ohne einen
    # eigenen Index-Eintrag (derselbe rglob-Walk wie bei einem durch ein Item entstandenen Ordner).
    nikinger = next(s for s in store.list_spaces() if s.name == "nikinger")
    assert "projekte" in nikinger.folders
    assert "projekte/backend" in nikinger.folders


def test_ensure_folder_is_idempotent(store):
    store.ensure_folder("nikinger", "projekte")
    store.ensure_folder("nikinger", "projekte")  # zweiter Aufruf ist kein Fehler


def test_ensure_folder_rejects_too_deep_via_validate_folder(store):
    with pytest.raises(ValidationError):
        store.ensure_folder("nikinger", "a/b/c")


def test_ensure_folder_rejects_empty_string(store):
    with pytest.raises(ValidationError):
        store.ensure_folder("nikinger", "")


def test_create_defaults_visibility_and_share_fields_and_omits_them_from_file(store, tmp_path):
    # Nikinger-Entscheidung 2026-08-12 (siehe phase6_shares/CLAUDE.md Session-Block, "Punkt 3"):
    # "fehlend == private" erfuellt Abnahmezeile 8 -- kein Sticky-Write. Eine explizit gesetzte
    # `visibility: private` verschwindet beim naechsten `update()` wieder aus der Datei (Default
    # wird nie geschrieben), das ist gewolltes Verhalten, keine Luecke: Abnahmezeile 8 wird ueber
    # `get_item`/die API gelesen (loest zu "private" auf), nicht ueber ein rohes Datei-`grep`.
    item = store.create("nikinger", type="note", title="Standard")
    assert item.visibility == "private"
    assert item.share_read == []
    assert item.share_write == []
    path = tmp_path / "nikinger" / f"{item.id}__standard.md"
    text = path.read_text()
    assert "visibility" not in text
    assert "share_read" not in text
    assert "share_write" not in text


def test_create_with_explicit_visibility_and_shares_is_written(store, tmp_path):
    item = store.create(
        "nikinger", type="note", title="Geteilt",
        visibility="human", share_read=["fabian"], share_write=["fabian"],
    )
    assert item.visibility == "human"
    assert item.share_read == ["fabian"]
    assert item.share_write == ["fabian"]
    path = tmp_path / "nikinger" / f"{item.id}__geteilt.md"
    text = path.read_text()
    assert "visibility: human" in text
    assert "share_read" in text and "fabian" in text


def test_create_rejects_unknown_visibility(store):
    with pytest.raises(ValidationError):
        store.create("nikinger", type="note", title="X", visibility="oeffentlich")


def test_update_moves_item_between_folders(store, tmp_path):
    item = store.create("nikinger", type="note", title="Wandert", folder="alt")
    old_path = tmp_path / "nikinger" / "alt" / f"{item.id}__wandert.md"
    assert old_path.exists()

    moved = store.update(item.id, version=item.version, folder="neu/unterordner")

    assert moved.folder == "neu/unterordner"
    assert not old_path.exists()
    new_path = tmp_path / "nikinger" / "neu" / "unterordner" / f"{item.id}__wandert.md"
    assert new_path.exists()


def test_update_out_of_folder_back_to_root(store, tmp_path):
    item = store.create("nikinger", type="note", title="Zurueck", folder="irgendwo")
    moved = store.update(item.id, version=item.version, folder="")
    assert moved.folder == ""
    assert (tmp_path / "nikinger" / f"{item.id}__zurueck.md").exists()


def test_update_sets_visibility_and_shares(store):
    item = store.create("nikinger", type="note", title="Wird geteilt")
    updated = store.update(
        item.id, version=item.version,
        visibility="human", share_read=["fabian"], share_write=[],
    )
    assert updated.visibility == "human"
    assert updated.share_read == ["fabian"]
    assert updated.share_write == []


def test_update_rejects_unknown_visibility(store):
    item = store.create("nikinger", type="note", title="X")
    with pytest.raises(ValidationError):
        store.update(item.id, version=item.version, visibility="oeffentlich")


def test_archive_forces_folder_empty(store, tmp_path):
    item = store.create("nikinger", type="task", title="Im Ordner archiviert", folder="projekte")
    archived = store.archive(item.id, version=item.version)
    assert archived.folder == ""
    archive_path = tmp_path / "nikinger" / "_archive" / f"{item.id}__im-ordner-archiviert.md"
    assert archive_path.exists()


def test_acl_of_returns_defaults_for_plain_item(store):
    item = store.create("nikinger", type="note", title="Ohne Freigabe")
    acl = store.acl_of(item.id)
    assert acl.space == "nikinger"
    assert acl.folder == ""
    assert acl.visibility == "private"
    assert acl.read == frozenset()
    assert acl.write == frozenset()


def test_acl_of_unions_item_shares_with_share_yml(store, tmp_path):
    (tmp_path / "nikinger").mkdir(parents=True, exist_ok=True)
    (tmp_path / "nikinger" / ".share.yml").write_text("read: [fabian]\n", encoding="utf-8")
    item = store.create("nikinger", type="note", title="Zusatzfreigabe", share_write=["dritter"])

    acl = store.acl_of(item.id)

    assert acl.read == frozenset({"fabian", "dritter"})  # write impliziert read
    assert acl.write == frozenset({"dritter"})


def test_acl_of_does_not_read_the_item_file(store, tmp_path, monkeypatch):
    item = store.create("nikinger", type="note", title="Ungelesen")
    path = tmp_path / "nikinger" / f"{item.id}__ungelesen.md"

    def boom(*args, **kwargs):
        raise AssertionError("acl_of() darf die Item-Datei nicht lesen")

    monkeypatch.setattr(type(path), "read_text", boom)
    monkeypatch.setattr(type(path), "read_bytes", boom)

    store.acl_of(item.id)  # darf nicht raisen


def test_acl_of_raises_item_not_found(store):
    with pytest.raises(ItemNotFound):
        store.acl_of("itm_deadbeef")


def test_list_spaces_reports_members_and_folders(store, tmp_path):
    store.create("nikinger", type="note", title="Eins", folder="projekte/alpha")
    store.create("nikinger", type="note", title="Zwei")
    (tmp_path / "nikinger" / ".share.yml").write_text("write: [fabian]\n", encoding="utf-8")

    spaces = store.list_spaces()

    nikinger = next(s for s in spaces if s.name == "nikinger")
    assert nikinger.item_count == 2
    assert nikinger.members == ("fabian",)
    assert nikinger.folders == ("projekte", "projekte/alpha")


def test_list_spaces_includes_empty_space_directory_without_items(store, tmp_path):
    (tmp_path / "fabian").mkdir()
    spaces = store.list_spaces()
    fabian = next(s for s in spaces if s.name == "fabian")
    assert fabian.item_count == 0
    assert fabian.folders == ()


def test_list_spaces_excludes_archive_and_assets_from_folders(store, tmp_path):
    item = store.create("nikinger", type="task", title="Wird archiviert")
    store.archive(item.id, version=item.version)
    (tmp_path / "nikinger" / "_assets").mkdir(exist_ok=True)

    nikinger = next(s for s in store.list_spaces() if s.name == "nikinger")
    assert nikinger.folders == ()


def test_search_filters_by_folder(store):
    store.create("nikinger", type="note", title="Drin", folder="projekte")
    store.create("nikinger", type="note", title="Draussen")

    result = store.search(folder="projekte")

    assert result.total == 1
    assert result.items[0].title == "Drin"


def test_search_filters_by_spaces_list(store):
    store.create("nikinger", type="note", title="Eigenes")
    store.create("fabian", type="note", title="Fremdes")

    result = store.search(spaces=["nikinger"])

    assert result.total == 1
    assert result.items[0].space == "nikinger"


def test_search_summary_carries_folder_and_visibility(store):
    store.create("nikinger", type="note", title="Mit Ordner", folder="projekte", visibility="human")
    result = store.search()
    assert result.items[0].folder == "projekte"
    assert result.items[0].visibility == "human"


# -- Step 7b: move() -- P6-AD-AJ, phase6_shares/ITEM_MOVE_PLAN.md §4 --------------------------


def test_move_between_spaces_rewrites_frontmatter_space(store, tmp_path):
    (tmp_path / "fabian").mkdir()
    item = store.create("nikinger", type="note", title="Umzug")

    moved = store.move(item.id, version=item.version, space="fabian")

    assert moved.space == "fabian"
    new_path = tmp_path / "fabian" / f"{item.id}__umzug.md"
    assert new_path.exists()
    assert not (tmp_path / "nikinger" / f"{item.id}__umzug.md").exists()
    # Fund B2 der P2-Adapter-Abnahme: Frontmatter muss mit dem Pfad mitziehen, nie divergieren.
    assert "space: fabian" in new_path.read_text(encoding="utf-8")
    fetched = store.get(item.id)
    assert fetched.space == "fabian"


def test_move_between_spaces_produces_exactly_one_commit(store_git, tmp_path):
    (tmp_path / "fabian").mkdir()
    item = store_git.create("nikinger", type="note", title="Umzug")

    store_git.move(item.id, version=item.version, space="fabian")

    messages = _git_log(tmp_path)
    move_commits = [m for m in messages if m.startswith("move ")]
    assert len(move_commits) == 1
    assert move_commits[0] == f"move {item.id} [fabian]"


def test_move_bumps_version_and_conflicts_on_stale_version(store, tmp_path):
    (tmp_path / "fabian").mkdir()
    item = store.create("nikinger", type="note", title="Umzug")

    moved = store.move(item.id, version=item.version, space="fabian")
    assert moved.version == item.version + 1

    with pytest.raises(ConflictError):
        store.move(item.id, version=item.version, space="nikinger")


def test_move_to_nonexistent_space_raises_instead_of_creating_it(store, tmp_path):
    item = store.create("nikinger", type="note", title="Umzug")

    with pytest.raises(ValidationError):
        store.move(item.id, version=item.version, space="nirgendwo")

    assert not (tmp_path / "nirgendwo").exists()


def test_move_removes_emptied_source_folder_but_keeps_one_with_share_yml(store, tmp_path):
    (tmp_path / "fabian").mkdir()
    without_share = store.create("nikinger", type="note", title="Leer wird", folder="alt")
    with_share = store.create("nikinger", type="note", title="Bleibt", folder="geteilt")
    (tmp_path / "nikinger" / "geteilt" / ".share.yml").write_text(
        "write: [fabian]\n", encoding="utf-8"
    )

    store.move(without_share.id, version=without_share.version, space="fabian")
    store.move(with_share.id, version=with_share.version, space="fabian")

    assert not (tmp_path / "nikinger" / "alt").exists()
    assert (tmp_path / "nikinger" / "geteilt").is_dir()
    assert (tmp_path / "nikinger" / "geteilt" / ".share.yml").exists()


def test_move_of_archived_item_rejects_a_real_folder_change(store):
    # Siebte Contract-Öffnung (P7 Step C4): ein reiner Space-Wechsel ist seit dieser Öffnung
    # erlaubt (siehe die beiden Tests unten) -- ein echter Ordner-Wechsel bleibt verboten, weil
    # ein archiviertes Item nie eine Ordnerposition trägt (`archive()` erzwingt `folder=""`).
    item = store.create("nikinger", type="note", title="Erledigt")
    archived = store.archive(item.id, version=item.version)

    with pytest.raises(ValidationError):
        store.move(archived.id, version=archived.version, folder="irgendwo")


def test_move_of_archived_item_between_spaces_relocates_to_target_archive(store, tmp_path):
    # Siebte Contract-Öffnung (P7 Step C4, N8/P7-20-Fund): vorher unterschiedslos verboten, was
    # einen Space mit Historie (`_archive/`-Inhalt) strukturell unentfernbar machte. Ein reiner
    # Space-Wechsel ist jetzt erlaubt -- `_write_item_file()` legt das Item dabei ins
    # Ziel-`_archive/`, nicht an die Space-Wurzel (`files.item_path()` kennt `_archive/` nicht).
    (tmp_path / "fabian").mkdir()
    item = store.create("nikinger", type="note", title="Erledigt")
    archived = store.archive(item.id, version=item.version)

    moved = store.move(archived.id, version=archived.version, space="fabian")

    assert moved.space == "fabian"
    assert moved.status == "archived"
    assert moved.folder == ""
    target_path = tmp_path / "fabian" / "_archive" / f"{item.id}__erledigt.md"
    assert target_path.exists()
    assert not (tmp_path / "nikinger" / "_archive" / f"{item.id}__erledigt.md").exists()
    fetched = store.get(item.id)
    assert fetched.space == "fabian"
    assert fetched.status == "archived"


def test_move_of_archived_item_produces_exactly_one_commit(store_git, tmp_path):
    (tmp_path / "fabian").mkdir()
    item = store_git.create("nikinger", type="note", title="Erledigt")
    archived = store_git.archive(item.id, version=item.version)

    store_git.move(archived.id, version=archived.version, space="fabian")

    messages = _git_log(tmp_path)
    move_commits = [m for m in messages if m.startswith("move ")]
    assert len(move_commits) == 1


# -- Bild-Assets (Phase 6.5 Step B1, fünfte Contract-Öffnung) ---------------------------

_PNG = png_bytes()


def test_put_asset_writes_atomically_and_commits_exactly_once(store_git, tmp_path):
    item = store_git.create("nikinger", type="note", title="Mit Bild")

    asset = store_git.put_asset(item.id, data=_PNG, filename="schnappschuss.png")

    assert asset.mime == "image/png"
    assert asset.bytes == len(_PNG)
    path = tmp_path / "nikinger" / "_assets" / item.id / f"{asset.id}.png"
    assert path.read_bytes() == _PNG
    messages = _git_log(tmp_path)
    asset_commits = [m for m in messages if m.startswith("asset ")]
    assert len(asset_commits) == 1


def test_put_asset_stores_the_stripped_bytes(store, tmp_path):
    """LG-8 / P1-Öffnung 15: auf der Platte liegt das **bereinigte** Bild, und
    `AssetInfo.bytes` zählt die bereinigte Länge — nicht die des Uploads.

    Der Weg über `put_asset()` ist der **eine** Weg: Web-Upload und `put_item_asset` laufen
    beide hier durch, es gibt keinen zweiten Pfad, der die Bereinigung vergessen könnte."""
    item = store.create("nikinger", type="note", title="Mit Metadaten")
    upload = png_bytes(text=b"geheim")

    asset = store.put_asset(item.id, data=upload)

    path = tmp_path / "nikinger" / "_assets" / item.id / f"{asset.id}.png"
    data = path.read_bytes()
    assert b"geheim" not in data
    assert asset.bytes == len(data)
    assert len(data) < len(upload)


def test_put_asset_rejects_unrecognized_bytes(store):
    item = store.create("nikinger", type="note", title="Ohne Bild")

    with pytest.raises(ValidationError):
        store.put_asset(item.id, data=b"nicht ein bild")


def test_list_assets_is_empty_for_an_item_without_images(store):
    item = store.create("nikinger", type="note", title="Textlich")

    assert store.list_assets(item.id) == []


def test_put_asset_created_matches_list_assets_created(store):
    # Advisor-Fund: put_asset() darf nicht self._now_fn() für `created` nehmen, wenn
    # list_assets() die Datei-mtime liest -- sonst zeigt dasselbe Asset zwei Werte.
    item = store.create("nikinger", type="note", title="Mit Bild")

    put = store.put_asset(item.id, data=_PNG)
    [listed] = store.list_assets(item.id)

    assert put.created == listed.created


def test_get_asset_returns_bytes_and_mime(store):
    item = store.create("nikinger", type="note", title="Mit Bild")
    asset = store.put_asset(item.id, data=_PNG)

    data, mime = store.get_asset(item.id, asset.id)

    assert data == _PNG
    assert mime == "image/png"


# -- Ultra-Review B1/B15 (2026-10-30): die asset_id wird nie roh zum Pfad -----------------------

_BAD_ASSET_IDS = [
    "../../../bob/itm_00000000__geheim",   # Traversal aus dem Asset-Verzeichnis heraus
    "../../../bob/.share",                 # fremde `.share.yml`
    "*",                                   # Wildcard: lieferte das erste Asset (B15)
    "ast_*",
    "ast_0123456?",
    "ast_01234567\n",                      # `$` liess einen Zeilenumbruch durch, `\Z` nicht
    "",
]


@pytest.mark.parametrize("bad", _BAD_ASSET_IDS)
def test_get_asset_rejects_a_malformed_asset_id_as_not_found(store, tmp_path, bad):
    item = store.create("nikinger", type="note", title="Mit Bild")
    store.put_asset(item.id, data=_PNG)
    # Köder ausserhalb des Asset-Verzeichnisses, den die ungeprüfte ID getroffen hätte
    (tmp_path / "bob").mkdir()
    (tmp_path / "bob" / ".share.yml").write_text("write: [mallory]\n", encoding="utf-8")

    with pytest.raises(ItemNotFound):
        store.get_asset(item.id, bad)


@pytest.mark.parametrize("bad", _BAD_ASSET_IDS)
def test_delete_asset_rejects_a_malformed_asset_id_and_moves_nothing(store, tmp_path, bad):
    item = store.create("nikinger", type="note", title="Mit Bild")
    asset = store.put_asset(item.id, data=_PNG)
    (tmp_path / "bob").mkdir()
    bait = tmp_path / "bob" / ".share.yml"
    bait.write_text("write: [mallory]\n", encoding="utf-8")

    with pytest.raises(ItemNotFound):
        store.delete_asset(item.id, bad)

    assert bait.read_text(encoding="utf-8") == "write: [mallory]\n"  # nicht verschoben
    assert [a.id for a in store.list_assets(item.id)] == [asset.id]   # eigenes Asset unberührt


def test_delete_asset_moves_to_trash_not_gone(store, tmp_path):
    item = store.create("nikinger", type="note", title="Mit Bild")
    asset = store.put_asset(item.id, data=_PNG)

    store.delete_asset(item.id, asset.id)

    assert store.list_assets(item.id) == []  # _trash/ wird beim Listing übersprungen
    trashed = tmp_path / "nikinger" / "_assets" / item.id / "_trash" / f"{asset.id}.png"
    assert trashed.read_bytes() == _PNG  # Entscheidung H: verschoben, nicht gelöscht


def test_move_carries_the_asset_directory_and_still_produces_one_commit(store_git, tmp_path):
    (tmp_path / "fabian").mkdir()
    item = store_git.create("nikinger", type="note", title="Umzug mit Bild")
    asset = store_git.put_asset(item.id, data=_PNG)

    store_git.move(item.id, version=item.version, space="fabian")

    old_dir = tmp_path / "nikinger" / "_assets" / item.id
    new_dir = tmp_path / "fabian" / "_assets" / item.id
    assert not old_dir.exists()
    assert (new_dir / f"{asset.id}.png").read_bytes() == _PNG
    messages = _git_log(tmp_path)
    move_commits = [m for m in messages if m.startswith("move ")]
    assert len(move_commits) == 1  # der Asset-Move erzeugt KEINEN eigenen Commit


def test_move_without_assets_is_unchanged(store, tmp_path):
    (tmp_path / "fabian").mkdir()
    item = store.create("nikinger", type="note", title="Ohne Bild")

    moved = store.move(item.id, version=item.version, space="fabian")

    assert moved.space == "fabian"


# -- P9 Block trace: `updated_by` (P9-AA–AD) ------------------------------------------------
#
# Reihenfolge wie in `docs/concepts/phase9_hardening_block_trace_plan.md` §4 T1–T5. Die
# Behauptung, die alle fuenf Tests zusammen tragen: **der Server weiss, wer geschrieben hat,
# und der Client kann das nicht behaupten.** Test 1 ist der positive Fall, Test 2 der
# Wechsel, Test 3 die Leere, Test 4 der Altbestand, Test 5 die Sperre.


def test_updated_by_is_written_to_the_file_and_read_back_by_get_and_search(store, tmp_path):
    """T1: `create(actor=...)` setzt `updated_by`, und **beide** Lesepfade liefern ihn.

    `get()` **und** `search()` sind geprueft, weil genau die Divergenz sonst unentdeckt
    bliebe, die P9 Step F als F10 aufgedeckt hat: `_summary()` vergisst ein Feld, `get()`
    liefert es, und die Datei sieht richtig aus. Ein Test auf `get()` allein waere die Haelfte."""
    item = store.create("nikinger", type="task", title="Kühlschrank prüfen", actor="niklas")

    pfad = tmp_path / "nikinger" / f"{item.id}__kuehlschrank-pruefen.md"
    assert "updated_by: niklas" in pfad.read_text(encoding="utf-8")
    assert store.get(item.id).updated_by == "niklas"
    assert store.search(space="nikinger").items[0].updated_by == "niklas"


def test_update_with_a_new_actor_overwrites_and_produces_exactly_one_commit(store_git, tmp_path):
    """T2: der Wert wechselt mit dem Schreiber, die Version mit, und es bleibt bei **einem**
    Commit. Der Commit-Teil ist kein Beiwerk: eine zweite Schreiboperation (etwa ein
    nachtraegliches Setzen von `updated_by`) wuerde die Versionsnummer ohne sichtbare
    Aenderung einmal mehr hochzaehlen."""
    item = store_git.create("nikinger", type="task", title="Umzug", actor="niklas")

    updated = store_git.update(item.id, version=item.version, title="Umzug Nord", actor="fabian")

    assert updated.updated_by == "fabian"
    assert updated.version == item.version + 1
    assert len([m for m in _git_log(tmp_path) if m.startswith("update ")]) == 1
    assert store_git.get(item.id).updated_by == "fabian"


def test_update_without_an_actor_leaves_updated_by_untouched(store):
    """T3 (P9-AB): leerer Akteur heisst **unbekannt**, nicht leer. Ein Operator-Skript, das
    eine Datei anfasst, darf den letzten *bekannten* Editor nicht aus dem Item loeschen —
    der alternative Weg waere ein erfundener Name, und eine erfundene Zuschreibung ist schlimmer
    als keine."""
    item = store.create("nikinger", type="task", title="Kabel suchen", actor="niklas")

    updated = store.update(item.id, version=item.version, title="Kabel finden")

    assert updated.updated_by == "niklas"


def test_legacy_item_without_the_field_never_gets_an_empty_one(store, tmp_path):
    """T4: der **Altbestand** bekommt durch einen schreibenden Zugriff keine leere Zeile.
    Das ist dieselbe Eigenschaft wie F6/P9-42 bei `assignee`, und dieselbe Bedingung in
    `_item_to_text()`. Ohne sie stuende nach dem ersten Speichern `updated_by: ""` in jeder
    bestehenden Datei — und die UI zeigte eine leere Zeile an prominenter Stelle."""
    item = store.create("nikinger", type="task", title="Altbestand", actor="")
    # Pfad ueber den Index, nicht ueber den Slug: der Titelwechsel unten **benennt die Datei
    # um** (`rename_for_new_slug`), ein hart kodierter Dateiname waere hier still falsch —
    # und ein still falscher Fixture-Pfad sieht aus wie ein Befund am Produktivcode.
    def _datei():
        (treffer,) = list((tmp_path / "nikinger").glob(f"{item.id}__*.md"))
        return treffer

    assert "updated_by" not in _datei().read_text(encoding="utf-8")

    store.update(item.id, version=item.version, title="Altbestand (neu)")

    text = _datei().read_text(encoding="utf-8")
    assert "updated_by" not in text
    assert store.get(item.id).updated_by == ""


def test_updated_by_cannot_be_set_by_the_caller(store):
    """T5 (P9-AA): **kein** Schreibpfad nimmt das Feld an — weder beim Anlegen noch beim
    Aendern. `updated_by` steht in `_SYSTEM_MANAGED_FIELDS`; die Ablehnung ist eine
    `ValidationError`, also derselbe Fehler, den heute `created`/`updated` bekommen. Wer sich
    als jemand anderes ausgeben will, bekommt damit nicht etwa eine stille Fehlannahme, sondern
    eine laute."""
    with pytest.raises(ValidationError):
        store.create("nikinger", type="task", title="Erfunden", updated_by="fabian")

    item = store.create("nikinger", type="task", title="Echt", actor="niklas")
    with pytest.raises(ValidationError):
        store.update(item.id, version=item.version, updated_by="fabian")
    assert store.get(item.id).updated_by == "niklas"


# -- P10.5 Block 9: RE-7 `created_by` (P1-Öffnung 12) -------------------------------------
#
# Die Behauptung, die diese Tests tragen: **der Server weiss, wer ein Item angelegt hat, und
# der Wert bleibt das.** Anders als `updated_by` (P9 Block trace) ist `created_by` **einmalig**:
# es gibt genau einen Schreibvorgang, der es setzt — das Anlegen. Kein spaeterer Schreibpfad
# aendert es, kein Backfill erfindet es (Lock P10.5-W), und ueber keinen Kanal ist es setzbar.
#
# Die Muster sind dieselben wie bei `updated_by` (P9-AA–AD) — dieselbe Klasse Feld, dieselbe
# Herkunft (`actor`), dieselbe Sperre (`_SYSTEM_MANAGED_FIELDS`). Der Unterschied ist die
# Richtung: `updated_by` wandert mit dem letzten Schreiber, `created_by` steht fest.


def test_created_by_set_on_create_and_never_changed(store, tmp_path):
    """Der positive Fall: `create(actor=…)` setzt das Feld, es landet in der Datei, und **kein**
    spaeterer Schreibpfad aendert es — nicht `update`, nicht `append`, nicht `patch`, nicht
    `move`, nicht `archive`.

    Die Kette `update` → `append` → `patch` → `move` → `archive` ist keine Redundanz: jeder dieser
    Wege baut ein **neues** `Item` (ueber `dataclasses.replace`), und `replace()` nimmt den
    Feldwert mit — ein Weg, der ihn versehentlich zuruecksetzt, wuerde hier auffallen."""
    item = store.create("nikinger", type="task", title="Kühlschrank prüfen", actor="niklas")

    (pfad,) = list((tmp_path / "nikinger").glob(f"{item.id}__*.md"))
    assert "created_by: niklas" in pfad.read_text(encoding="utf-8")
    assert store.get(item.id).created_by == "niklas"
    assert store.search(space="nikinger").items[0].created_by == "niklas"

    updated = store.update(item.id, version=item.version, title="Kühlschrank (Dringend)")
    assert updated.created_by == "niklas"

    appended = store.append(item.id, version=updated.version, text="notiert")
    assert appended.created_by == "niklas"

    patched = store.patch(
        item.id, version=appended.version,
        edits=[{"old_text": "notiert", "new_text": "notiert!"}],
    )
    assert patched.item.created_by == "niklas"

    (tmp_path / "fabian").mkdir()
    moved = store.move(item.id, version=patched.item.version, space="fabian")
    assert moved.created_by == "niklas"

    archived = store.archive(item.id, version=moved.version)
    assert archived.created_by == "niklas"
    assert store.get(item.id).created_by == "niklas"


def test_created_by_absent_without_actor(store, tmp_path):
    """Ohne Akteur steht das Feld **gar nicht** in der Datei (P10.5-W: kein erfundenes
    Leerfeld). Ein leeres `created_by: ""` waere eine Aussage ("jemand ohne Namen"), die der
    Server nicht belegen kann — dieselbe Regel wie bei `assignee` (F6) und `updated_by` (P9-AB)."""
    item = store.create("nikinger", type="task", title="Ohne Namen", actor="")

    (pfad,) = list((tmp_path / "nikinger").glob(f"{item.id}__*.md"))
    text = pfad.read_text(encoding="utf-8")
    assert "created_by" not in text
    assert store.get(item.id).created_by == ""


def test_old_file_without_created_by_reads_as_empty(store, tmp_path):
    """Der **Altbestand**: ein Item, das vor diesem Feld existierte, liest sich als leer — und
    bekommt durch einen schreibenden Zugriff **keine** leere Zeile angehaengt.

    Der zweite Teil ist der eigentliche Test: ohne die Bedingung `if item.created_by:` in
    `_item_to_text()` bekaeme **jedes** bestehende Item beim naechsten beliebigen Write ein
    stilles `created_by: ""` — ein Frontmatter-Diff, den niemand bestellt hat, in jedem einzelnen
    Altbestand-Item (dieselbe Lehre wie P9-42 bei `assignee`)."""
    item = store.create("nikinger", type="task", title="Altbestand", actor="")

    def _datei():
        (treffer,) = list((tmp_path / "nikinger").glob(f"{item.id}__*.md"))
        return treffer

    assert "created_by" not in _datei().read_text(encoding="utf-8")

    store.update(item.id, version=item.version, title="Altbestand (neu)")

    text = _datei().read_text(encoding="utf-8")
    assert "created_by" not in text
    assert store.get(item.id).created_by == ""


def test_created_by_cannot_be_set_by_the_caller(store):
    """**Kein** Schreibpfad nimmt das Feld an — weder beim Anlegen noch beim Aendern.
    `created_by` steht in `_SYSTEM_MANAGED_FIELDS`; die Ablehnung ist eine `ValidationError`,
    also derselbe Fehler, den heute `created`/`updated` bekommen. Wer sich als jemand anderes
    ausgeben will, bekommt damit nicht eine stille Fehlannahme, sondern eine laute."""
    with pytest.raises(ValidationError):
        store.create("nikinger", type="task", title="Erfunden", created_by="fabian")

    item = store.create("nikinger", type="task", title="Echt", actor="niklas")
    with pytest.raises(ValidationError):
        store.update(item.id, version=item.version, created_by="fabian")
    assert store.get(item.id).created_by == "niklas"


def test_created_by_survives_a_git_commit_as_the_author_of_the_creating_commit(store_git, tmp_path):
    """Das Feld und der Git-Autor muessen **dasselbe** sein: ein Item, dessen Datei
    `created_by: niklas` traegt, wurde in einem Commit von `niklas` angelegt. Der Test haelt die
    beiden Spuren zusammen — sie stammen aus derselben Quelle (`actor`), und eine der beiden
    verliesse den Akteur waere ein halbfertiger Zugang.

    Das ist bewusst **kein** Git-Autor-Test: der Autor-Zweig ist P9-AC (und P9-AB: eine
    Fremdaenderung bekommt **keinen** Autor). Hier geht es nur darum, dass der Actor nicht auf
    dem Weg in die Datei verloren geht."""
    item = store_git.create("nikinger", type="task", title="Mit Autor", actor="niklas")

    assert store_git.get(item.id).created_by == "niklas"
    commits = _git_log(tmp_path)
    assert len([m for m in commits if m.startswith("create ")]) == 1


# -- P10.5 Block 9: RE-4 `Store.rename_folder()` (P1-Öffnung 13) -----------------------------
#
# Die Behauptung, die diese Tests tragen: **ein Ordner-Umbenennen ist ein reines
# Verzeichnis-Rename.** Der Ordner steht nicht im Frontmatter (P6 Step 4), also wird keine
# Item-Datei umgeschrieben, keine `version` erhoeht und kein Byte des Inhalts angefasst.
# Was sich aendert, ist der Pfad — und damit die Ableitung `folder`.


def test_rename_folder_moves_nested_and_share_file_keeps_versions(store_git, tmp_path):
    """Der Kern: die Dateien wandern, die **Versionen bleiben**, die `.share.yml` wandert mit.

    Die `.share.yml` ist der eigentliche Fund (P8.6 §0.4.1): die „billige Frontend-Fassung"
    liess die Freigabe eines geteilten Ordners zurueck, und der Ordner war danach eine
    Sackgasse — sichtbar, aber nicht mehr teilbar. Wer sie verliert, verliert eine
    Rechteeinstellung, die ein Mensch absichtlich gemacht hat."""
    item = store_git.create("alpha", type="task", title="Rechnung", folder="alt/unter")
    version_vorher = item.version
    inhalt_vorher = (tmp_path / "alpha" / "alt" / "unter" / f"{item.id}__rechnung.md").read_bytes()

    # Die Ordnerfreigabe: ein zweiter Mensch darf in diesem Ordner schreiben.
    (tmp_path / "alpha" / "alt" / ".share.yml").write_text(
        "read: [beta]\nwrite: [beta]\n", encoding="utf-8"
    )

    betroffen = store_git.rename_folder("alpha", "alt", "neu", actor="alpha")

    assert betroffen == 1
    # Die Datei ist am neuen Ort — **byte-identisch** (kein Umschreiben, kein Frontmatter-Diff).
    neue_datei = tmp_path / "alpha" / "neu" / "unter" / f"{item.id}__rechnung.md"
    assert neue_datei.is_file()
    assert neue_datei.read_bytes() == inhalt_vorher
    assert not (tmp_path / "alpha" / "alt").exists()
    # Die Version ist **unveraendert** — RE-4 hebt keine Version an.
    gelesen = store_git.get(item.id)
    assert gelesen.version == version_vorher
    assert gelesen.folder == "neu/unter"
    # Und die Freigabe ist mitgewandert — und wird am neuen Pfad **frisch** gelesen
    # (`AclReader`s Cache-Schluessel enthaelt den Pfad).
    assert (tmp_path / "alpha" / "neu" / ".share.yml").is_file()
    assert "beta" in store_git.acl_of(item.id).write


def test_rename_folder_produces_exactly_one_commit(store_git, tmp_path):
    """**Ein** Commit fuer das ganze Umbenennen — derselbe Autor wie bei jedem anderen
    Schreibvorgang. Zwei Commits wuerden die Historie der Dateien in zwei Haelften zerlegen,
    von denen die erste allein schon den neuen Pfad zeigt."""
    store_git.create("alpha", type="task", title="Rechnung", folder="alt")

    store_git.rename_folder("alpha", "alt", "neu", actor="alpha")

    commits = [m for m in _git_log(tmp_path) if m.startswith("rename-folder ")]
    assert len(commits) == 1, commits
    assert "alpha:alt→neu" in commits[0]


def test_rename_folder_index_equals_rebuild(store, tmp_path):
    """Der Index nach dem Umbenennen ist **identisch** mit einem frischen Rebuild (Hard Rule 2:
    der Index ist Ableitung, nie Wahrheit). Der Test vergleicht beide Zeilen fuer Zeile."""
    store.create("alpha", type="task", title="Eins", folder="alt")
    store.create("alpha", type="task", title="Zwei", folder="alt/unter")
    store.create("alpha", type="note", title="Drei", folder="anders")

    store.rename_folder("alpha", "alt", "neu")

    from storage import index as index_mod
    mit_rename = {
        (r["id"], r["space"], r["path"], r["folder"], r["version"], r["sha256"])
        for r in index_mod.all_rows(store._conn)
    }
    store.rebuild_index()
    nach_rebuild = {
        (r["id"], r["space"], r["path"], r["folder"], r["version"], r["sha256"])
        for r in index_mod.all_rows(store._conn)
    }
    assert mit_rename == nach_rebuild


def test_rename_folder_refuses_existing_target_and_descendant(store, tmp_path):
    """Zwei Ablehnungen, und **nichts** bewegt in beiden Fällen:
    - der Zielname existiert bereits,
    - der Zielname liegt **unter** dem alten Ordner (`neu/unter` unter `alt`).
    Das zweite ist der Fall, in dem `os.rename()` sonst mit einem nüchternen `EINVAL` abbräche —
    hier steht eine lesbare Meldung, und der Ordner bleibt unangetastet."""
    store.create("alpha", type="task", title="Eins", folder="alt")
    store.create("alpha", type="task", title="Zwei", folder="belegt")

    with pytest.raises(ValidationError):
        store.rename_folder("alpha", "alt", "belegt")
    with pytest.raises(ValidationError):
        store.rename_folder("alpha", "alt", "alt/unter")
    with pytest.raises(ValidationError):
        store.rename_folder("alpha", "gibtsnicht", "neu")

    assert (tmp_path / "alpha" / "alt").is_dir()
    assert not (tmp_path / "alpha" / "neu").exists()
    assert not (tmp_path / "alpha" / "alt" / "unter").exists()


def test_rename_folder_resumes_after_crash(store_git, tmp_path, monkeypatch):
    """**9.4: Absturzsicherheit.** Der Absturz kommt **nach** dem Verzeichnis-Rename (der
    kritische Moment: das Verzeichnis ist schon gewandert, der Index noch nicht nachgezogen).

    Erwartet: ein neuer `Store` **beendet** den Rename von allein — der Ordner steht unter dem
    neuen Namen, der Index stimmt, der Marker ist **weg**, und es gibt **einen** Commit.

    Der Weg dahin ist derselbe wie im Plan: `Store.__init__` findet den Marker, fuehrt den
    Rename idempotent zu Ende (das Verzeichnis wandert **nicht** noch einmal — `old` existiert
    nicht mehr) und loescht den Marker."""
    store_git.create("alpha", type="task", title="Rechnung", folder="alt")
    item = store_git.search(space="alpha").items[0]

    def _absturz(*_args, **_kwargs):
        raise RuntimeError("Absturz mitten im Rename")

    monkeypatch.setattr(Store, "_reindex_moved_folder", _absturz)
    with pytest.raises(RuntimeError):
        store_git.rename_folder("alpha", "alt", "neu", actor="alpha")

    # Der Marker liegt noch da — das ist der Beweis, dass die Wiederaufnahme ueberhaupt
    # etwas zu tun hat.
    marker = tmp_path / ".rename-pending.json"
    assert marker.is_file()
    # Das Verzeichnis ist schon gewandert (der Absturz kam danach).
    assert (tmp_path / "alpha" / "neu").is_dir()

    monkeypatch.undo()
    neuer_store = Store(tmp_path, git=True)

    # Endzustand: der Ordner steht unter dem neuen Namen, der Index stimmt, der Marker ist weg.
    assert not marker.exists()
    gelesen = neuer_store.get(item.id)
    assert gelesen.folder == "neu"
    assert (tmp_path / "alpha" / "neu" / f"{item.id}__rechnung.md").is_file()
    commits = [m for m in _git_log(tmp_path) if m.startswith("rename-folder ")]
    assert len(commits) == 1, commits


# -- RE-3: Space umbenennen (P10.5 Block 9, P1-Oeffnung 14) ---------------------------------
#
# Anders als beim Ordner (RE-4) steht der Space-Namen **im Frontmatter** — Verzeichnis und
# Frontmatter duerfen nie auseinanderlaufen. Deshalb: `space=new`, `version+1`, `updated=now`,
# `updated_by=actor` — die Semantik von `move()`.


def test_rename_space_rewrites_frontmatter_bumps_versions_one_commit(store_git, tmp_path):
    """Der Kern: Verzeichnis **und** Frontmatter sagen danach den neuen Namen, die Version
    springt **genau einmal**, und der ganze Vorgang ist **ein** Commit."""
    item = store_git.create("alt", type="task", title="Rechnung")
    version_vorher = item.version
    updated_vorher = item.updated

    betroffen = store_git.rename_space("alt", "neu", actor="alpha")

    assert betroffen == 1
    # Das Verzeichnis ist gewandert, das alte ist weg.
    assert (tmp_path / "neu").is_dir()
    assert not (tmp_path / "alt").exists()
    # Das Frontmatter sagt den neuen Space — **und** die Version ist +1 (die Semantik von
    # `move()`: ein Space-Wechsel ist ein Schreibvorgang, kein reines Verschieben).
    gelesen = store_git.get(item.id)
    assert gelesen.space == "neu"
    assert gelesen.version == version_vorher + 1
    # `updated` wird auf `now_fn()` gesetzt — die Uhr des Tests steht aber still, deshalb ist
    # der Wert **gleich**, nicht groesser. Entscheidend ist, dass er **geschrieben** wurde
    # (sonst haette die Datei den alten Zeitstempel behalten).
    assert gelesen.updated == updated_vorher
    assert gelesen.updated_by == "alpha"
    # Und **ein** Commit fuer den ganzen Vorgang.
    commits = [m for m in _git_log(tmp_path) if m.startswith("rename-space ")]
    assert len(commits) == 1, commits
    assert "alt→neu" in commits[0]


def test_rename_space_keeps_the_archived_items(store_git, tmp_path):
    """**Archivierte Items** liegen unter `_archive/` — sie wandern mit und sagen danach auch
    den neuen Space. Wer sie vergisst, haette Items mit `space: alt` im neuen Verzeichnis: der
    Index waere dann eine Luege."""
    item = store_git.create("alt", type="note", title="Archiviert")
    store_git.archive(item.id, version=item.version)

    betroffen = store_git.rename_space("alt", "neu", actor="alpha")

    assert betroffen == 1
    archiv = list((tmp_path / "neu" / "_archive").glob("*.md"))
    assert len(archiv) == 1
    assert "space: neu" in archiv[0].read_text(encoding="utf-8")


def test_rename_space_moves_trash_dir_untouched(store_git, tmp_path):
    """`._trash/<old>` wandert nach `._trash/<new>` — die Dateien darin bleiben **unveraendert**:
    sie sind Historie (ein geloeschtes Item bleibt im alten Space nachvollziehbar), und
    `._trash` wird von keinem Scan gelesen."""
    item = store_git.create("alt", type="note", title="Weg damit")
    store_git.trash(item.id, version=item.version)
    muell = list((tmp_path / "._trash" / "alt").glob("*.md"))
    assert len(muell) == 1
    inhalt_vorher = muell[0].read_bytes()

    store_git.rename_space("alt", "neu", actor="alpha")

    assert not (tmp_path / "._trash" / "alt").exists()
    nachher = list((tmp_path / "._trash" / "neu").glob("*.md"))
    assert len(nachher) == 1
    assert nachher[0].read_bytes() == inhalt_vorher


def test_rename_space_index_equals_rebuild(store, tmp_path):
    """Der Index nach dem Umbenennen ist **identisch** mit einem frischen Rebuild (Hard Rule 2)."""
    store.create("alt", type="task", title="Eins")
    store.create("alt", type="note", title="Zwei", folder="ordner")
    store.create("beta", type="note", title="Fremd")

    store.rename_space("alt", "neu")

    from storage import index as index_mod
    mit_rename = {
        (r["id"], r["space"], r["path"], r["folder"], r["version"], r["sha256"])
        for r in index_mod.all_rows(store._conn)
    }
    store.rebuild_index()
    nach_rebuild = {
        (r["id"], r["space"], r["path"], r["folder"], r["version"], r["sha256"])
        for r in index_mod.all_rows(store._conn)
    }
    assert mit_rename == nach_rebuild


def test_rename_space_refuses_existing_target_and_bad_names(store, tmp_path):
    """Der **Gegenlauf**: ein existierender Zielname, ein Name mit `/`, ein Punktname und ein
    reservierter Name werden abgelehnt — und **nichts** bewegt."""
    store.create("alt", type="task", title="Eins")
    store.create("belegt", type="task", title="Zwei")

    for ziel, grund in [
        ("belegt", "existiert bereits"),
        ("mit/slash", "kein gültiger Space-Name"),
        (".versteckt", "kein gültiger Space-Name"),
        ("_archive", "kein gültiger Space-Name"),
        ("alt", "Der neue Name ist der alte"),
    ]:
        with pytest.raises(ValidationError) as exc_info:
            store.rename_space("alt", ziel)
        assert grund.lower() in str(exc_info.value).lower(), (ziel, str(exc_info.value))
    # Nichts bewegt: der alte Space steht noch, mit seiner Datei.
    assert (tmp_path / "alt").is_dir()
    assert len(list((tmp_path / "alt").glob("*.md"))) == 1


def test_rename_resumes_after_crash(tmp_path, clock, monkeypatch):
    """**9.4 Absturzsicherheit:** der Prozess stirbt mitten im Umschreiben. Ein neuer `Store`
    fuehrt den Rename zu Ende: das Verzeichnis steht unter dem neuen Namen, **jedes** Frontmatter
    sagt den neuen Space, die Index stimmt, der Marker ist weg.

    Die Datei, die beim Absturz schon umgeschrieben war, bekommt **keinen** zweiten
    Versionssprung — das ist der Punkt der Idempotenz."""
    store = Store(tmp_path, now_fn=clock, git=False)
    store.create("alt", type="task", title="Eins")
    store.create("alt", type="task", title="Zwei")

    # Der Absturz: nach der **ersten** Datei fliegt die Pipeline weg.
    original = store._rewrite_space_frontmatter
    aufrufe = {"n": 0}

    def kaputt(old, new, actor):
        betroffen = original(old, new, actor)
        aufrufe["n"] += 1
        raise RuntimeError("Prozess stirbt")

    monkeypatch.setattr(store, "_rewrite_space_frontmatter", kaputt)
    with pytest.raises(RuntimeError):
        store.rename_space("alt", "neu", actor="alpha")
    monkeypatch.undo()

    # Der Marker liegt noch da — das ist der **Zweck** des Markers.
    assert (tmp_path / ".rename-pending.json").is_file()

    # Ein neuer Store nimmt die Arbeit wieder auf.
    neu = Store(tmp_path, now_fn=clock, git=False)
    assert not (tmp_path / ".rename-pending.json").exists()
    assert (tmp_path / "neu").is_dir()
    assert not (tmp_path / "alt").exists()
    for datei in (tmp_path / "neu").glob("*.md"):
        assert "space: neu" in datei.read_text(encoding="utf-8")
    # Der Index stimmt mit einem Rebuild ueberein.
    from storage import index as index_mod
    zeilen = {
        (r["id"], r["space"], r["version"])
        for r in index_mod.all_rows(neu._conn)
    }
    neu.rebuild_index()
    assert zeilen == {
        (r["id"], r["space"], r["version"])
        for r in index_mod.all_rows(neu._conn)
    }


# -- P10.5 Block 15.2: der Dienststart scheitert nie an Daten (Ultra-Review B2/B3/B20) -------
#
# Eine Datei darf **eine Datei** kosten — nie den Index und nie den Start. Die Wächter sind so
# geschnitten, dass keiner der drei Fixes einen anderen verdeckt (Advisor 15.2): der B20-Wächter
# prüft, dass die CRLF-Datei **indiziert** ist (nicht nur, dass der Start lebt — das schafft B3
# allein), und B2 hat drei getrennte Wächter (Eltern anlegen · Marker weg, wenn nichts wanderte ·
# Start trotz gescheiterter Wiederaufnahme).


def _fremde_dateien(tmp_path):
    """Vier Dateien, die ein Mensch (oder ein Werkzeug) in einen Space legen kann."""
    (tmp_path / "alpha" / "README.md").write_text("# Hallo\n\nKein Frontmatter.\n", encoding="utf-8")
    (tmp_path / "alpha" / "kaputt.md").write_text("---\ntitle: [offen\n---\nx\n", encoding="utf-8")
    (tmp_path / "alpha" / "ohne_id.md").write_text("---\ntitle: x\n---\n", encoding="utf-8")
    (tmp_path / "alpha" / "latin1.md").write_bytes("---\ntitle: \xe4\n---\n".encode("latin-1"))


def test_rebuild_skips_unreadable_files_and_indexes_the_rest(store, tmp_path, caplog):
    """B3: vorher brach der Neuaufbau an der ersten fremden `.md` ab — **nach** dem
    committeten `DELETE`, Index leer. Jetzt: die drei Items stehen, jede fremde Datei steht mit
    Pfad im `CRITICAL`-Log."""
    ids = [store.create("alpha", type="task", title=t).id for t in ("a", "b", "c")]
    _fremde_dateien(tmp_path)
    with caplog.at_level(logging.CRITICAL, logger="storage.index"):
        stats = store.rebuild_index()
    assert stats.items_indexed == 3
    assert {store.get(i).id for i in ids} == set(ids)
    meldungen = " ".join(r.getMessage() for r in caplog.records)
    for name in ("README.md", "kaputt.md", "ohne_id.md", "latin1.md"):
        assert name in meldungen


def test_rebuild_skips_a_value_sqlite_cannot_bind(store, tmp_path):
    """B3: `status: [a, b]` ist ein Wert, den SQLite nicht binden kann (`ProgrammingError`) — das
    kostet die Datei, nicht den Index. **[15.3]:** hier stand bis 15.3 `title: [a, b]`; den
    koerziert der Lesepfad jetzt (B5, `test_hand_edited_title_list_stays_visible_after_rebuild`),
    `status` bleibt der Zeuge fuer den `ProgrammingError`-Zweig."""
    gut = store.create("alpha", type="task", title="gut")
    schlecht = store.create("alpha", type="task", title="schlecht")
    pfad = next((tmp_path / "alpha").glob(f"{schlecht.id}__*.md"))
    pfad.write_text(pfad.read_text(encoding="utf-8").replace("status: open", "status:\n- a\n- b"), encoding="utf-8")
    assert store.rebuild_index().items_indexed == 1
    assert store.get(gut.id).title == "gut"


def test_store_starts_with_fresh_index_despite_foreign_files(tmp_path, clock):
    """B3, der Startpfad: ein frischer Index (Schema-Sprung im Deploy) heisst `rebuild_index()`
    in `Store.__init__` — vorher warf das, der Dienst startete nicht."""
    store = Store(tmp_path, now_fn=clock, git=False)
    item = store.create("alpha", type="task", title="bleibt")
    _fremde_dateien(tmp_path)
    (tmp_path / ".index.sqlite3").unlink()
    neu = Store(tmp_path, now_fn=clock, git=False)
    assert neu.get(item.id).title == "bleibt"


def test_rebuild_keeps_old_index_on_environment_error(store, monkeypatch):
    """B3, Transaktion: ein Fehler der **Umgebung** (hier: `OperationalError` mitten im
    Neuaufbau) bricht ab — und der **alte** Index steht vollstaendig, statt halb geleert
    committet zu sein (vorher committete der erste Kanten-Commit das `DELETE`)."""
    import sqlite3

    from storage import index as index_mod

    ids = {store.create("alpha", type="task", title=t).id for t in ("a", "b", "c")}
    echt = index_mod._index_one_file
    aufrufe = {"n": 0}

    def zweiter_wirft(*args):
        aufrufe["n"] += 1
        if aufrufe["n"] == 2:
            raise sqlite3.OperationalError("database is locked")
        return echt(*args)

    monkeypatch.setattr(index_mod, "_index_one_file", zweiter_wirft)
    with pytest.raises(sqlite3.OperationalError):
        store.rebuild_index()
    assert {r["id"] for r in index_mod.all_rows(store._conn)} == ids


def test_rebuild_tolerates_duplicate_frontmatter_links(store, tmp_path):
    """15.2-Fund (nicht im Review): `links: [itm_x, itm_x]` von Hand riss den Primaerschluessel
    von `item_links` — `IntegrityError`, derselbe Startblocker wie B3. Die Kante zaehlt einmal."""
    from storage import index as index_mod

    ziel = store.create("alpha", type="task", title="ziel")
    quelle = store.create("alpha", type="task", title="quelle")
    pfad = next((tmp_path / "alpha").glob(f"{quelle.id}__*.md"))
    pfad.write_text(
        pfad.read_text(encoding="utf-8").replace("links: []", f"links:\n- {ziel.id}\n- {ziel.id}"),
        encoding="utf-8",
    )
    assert store.rebuild_index().items_indexed == 2
    kanten = [r for r in index_mod.all_links(store._conn) if r["src_id"] == quelle.id]
    assert [(r["dst_id"], r["kind"]) for r in kanten] == [(ziel.id, "frontmatter")]


def _als_crlf(tmp_path, item_id):
    pfad = next((tmp_path / "alpha").glob(f"{item_id}__*.md"))
    pfad.write_bytes(pfad.read_bytes().replace(b"\n", b"\r\n"))
    return pfad


def test_crlf_item_is_indexed_and_readable(tmp_path, clock):
    """B20: die CRLF-Datei ist **im Index** und lesbar — nicht bloss „der Start lebt"
    (das schaffte B3 allein, indem es die Datei uebersprang)."""
    store = Store(tmp_path, now_fn=clock, git=False)
    item = store.create("alpha", type="task", title="Windows", body="Zeile\n")
    _als_crlf(tmp_path, item.id)
    (tmp_path / ".index.sqlite3").unlink()
    neu = Store(tmp_path, now_fn=clock, git=False)
    assert neu.get(item.id).title == "Windows"
    assert item.id in {s.id for s in neu.search(space="alpha").items}


def test_crlf_item_survives_update(store, tmp_path):
    """B20, Rueckweg: ein Update schreibt das Frontmatter mit `\\n` (`serialize()`), der Body
    behaelt sein `\\r\\n` — gemischte Zeilenenden, aber die Datei bleibt lesbar und indiziert."""
    item = store.create("alpha", type="task", title="Windows", body="Zeile\n")
    pfad = _als_crlf(tmp_path, item.id)
    store.rebuild_index()
    gelesen = store.get(item.id)
    neu = store.update(item.id, version=gelesen.version, status="done")
    assert neu.status == "done"
    assert store.rebuild_index().items_indexed == 1
    assert store.get(item.id).status == "done"
    assert pfad.read_bytes().startswith(b"---\nid: ")


def test_rename_folder_into_missing_parent(store_git, tmp_path):
    """B2, der Ausloeser: `projekte` → `archiv/projekte` bei fehlendem `archiv/` — ein legitimer
    Klick eines Space-Verwalters. Vorher `FileNotFoundError` und ein liegengebliebener Marker."""
    item = store_git.create("alpha", type="task", title="Plan", folder="projekte")
    assert store_git.rename_folder("alpha", "projekte", "archiv/projekte") == 1
    assert store_git.get(item.id).folder == "archiv/projekte"
    assert not (tmp_path / ".rename-pending.json").exists()


@pytest.mark.parametrize("art", ["folder", "space"])
def test_rename_failing_before_anything_moved_clears_marker(store, tmp_path, monkeypatch, art):
    """B2: scheitert der Rename, **bevor** etwas wandert, beschreibt der Marker nichts Halbes —
    er muss weg, sonst fuehrte der naechste Start einen Rename aus, den der Aufrufer als Fehler
    gesehen hat (und vorher: an dem er jedes Mal wieder scheiterte)."""
    store.create("alpha", type="task", title="Plan", folder="projekte")

    def kein_rename(*_a, **_k):
        raise PermissionError("EACCES")

    monkeypatch.setattr(Store, "_rename_directory", staticmethod(kein_rename))
    with pytest.raises(PermissionError):
        if art == "folder":
            store.rename_folder("alpha", "projekte", "neu")
        else:
            store.rename_space("alpha", "beta")
    assert not (tmp_path / ".rename-pending.json").exists()


def test_store_starts_when_rename_resume_fails(tmp_path, clock, monkeypatch, caplog):
    """B2, der Startpfad: die Wiederaufnahme scheitert (hier erzwungen) — der Store startet
    trotzdem, der Index stimmt mit der Platte, der Marker **bleibt** (die einzige Spur) und steht
    im `CRITICAL`-Log. Vorher: unter systemd eine Crash-Schleife."""
    store = Store(tmp_path, now_fn=clock, git=False)
    item = store.create("alpha", type="task", title="Plan", folder="alt")
    marker = tmp_path / ".rename-pending.json"
    marker.write_text(json.dumps({"kind": "folder", "space": "alpha", "old": "alt", "new": "neu"}))

    def kaputt(*_a, **_k):
        raise OSError("EIO")

    monkeypatch.setattr(Store, "_rename_directory", staticmethod(kaputt))
    with caplog.at_level(logging.CRITICAL, logger="storage.store"):
        neu = Store(tmp_path, now_fn=clock, git=False)
    assert marker.is_file()
    assert neu.get(item.id).folder == "alt"
    assert any("Wiederaufnahme gescheitert" in r.getMessage() for r in caplog.records)


def test_rename_refused_while_marker_pending(store, tmp_path):
    """15.2: solange ein Marker liegt, beginnt kein neuer Rename — er wuerde den Marker
    ueberschreiben und damit die einzige Spur des halben Renames loeschen."""
    store.create("alpha", type="task", title="Plan", folder="alt")
    marker = tmp_path / ".rename-pending.json"
    marker.write_text('{"kind": "folder", "space": "alpha", "old": "x", "new": "y"}')
    with pytest.raises(ValidationError):
        store.rename_folder("alpha", "alt", "neu")
    with pytest.raises(ValidationError):
        store.rename_space("alpha", "beta")
    assert json.loads(marker.read_text())["old"] == "x"
    assert (tmp_path / "alpha" / "alt").is_dir()


# -- P10.5 Block 15.3 (Ultra-Review B5/B8): Lesen ist nachsichtig, Schreiben ist streng -------


def _von_hand(tmp_path, item_id, alt, neu):
    pfad = next(tmp_path.rglob(f"{item_id}__*.md"))
    text = pfad.read_text(encoding="utf-8")
    assert alt in text
    pfad.write_text(text.replace(alt, neu, 1), encoding="utf-8")
    return pfad


def _commits(root):
    return subprocess.run(
        ["git", "-C", str(root), "rev-list", "--count", "HEAD"],
        capture_output=True, text=True, check=True,
    ).stdout.strip()


def test_hand_edited_int_tag_keeps_search_alive(store, tmp_path):
    """B5: `tags: [2026]` von Hand — vorher starb jede Textsuche aller Nutzer mit `TypeError`,
    weil die Suche die Tags als Strings verkettet."""
    item = store.create("alpha", type="task", title="Jahresplan")
    store.create("alpha", type="task", title="Anderes")
    _von_hand(tmp_path, item.id, "tags: []", "tags: [2026]")
    assert store.get(item.id).tags == ["2026"]
    assert [s.id for s in store.search("2026").items] == [item.id]
    assert store.search("anderes").total == 1
    assert [s.id for s in store.search(tag="2026").items] == [item.id]


def test_hand_edited_numeric_title_can_be_updated(store, tmp_path):
    """B5: `title: 2026` von Hand — vorher brach jedes Update (`slugify()` auf einem `int`)."""
    item = store.create("alpha", type="task", title="Hallo")
    _von_hand(tmp_path, item.id, "title: Hallo", "title: 2026")
    gelesen = store.get(item.id)
    assert gelesen.title == "2026"
    neu = store.update(item.id, version=gelesen.version, body="neu")
    assert neu.title == "2026"
    assert store.get(item.id).body == "neu"


@pytest.mark.parametrize("roh, titel", [
    ("title: [a, b]", "[a, b]"),
    ("title:", ""),
    ("title: true", "true"),
    ("title: 1.0", "1.0"),
    ("title: {a: 1}", "{a: 1}"),
])
def test_hand_edited_title_list_stays_visible_after_rebuild(store, tmp_path, roh, titel):
    """B5 (Hinweis aus 15.2): ein Titel, der kein String ist, kostete beim Neuaufbau die Datei
    (`[a, b]` → `ProgrammingError`, leer → `NOT NULL`). Jetzt bleibt das Item sichtbar, mit dem
    Titel, wie er im YAML stand — und es laesst sich weiter schreiben."""
    item = store.create("alpha", type="task", title="Hallo")
    _von_hand(tmp_path, item.id, "title: Hallo", roh)
    assert store.rebuild_index().items_indexed == 1
    assert [s.title for s in store.search().items] == [titel]
    gelesen = store.get(item.id)
    assert gelesen.title == titel
    assert store.update(item.id, version=gelesen.version, status="done").title == titel


@pytest.mark.parametrize("roh, tags", [
    ("tags: abc", ["abc"]),
    ("tags: [[x]]", ["[x]"]),
    ("tags: [{a: 1}, ~, b]", ["{a: 1}", "b"]),
    ("tags:", []),
])
def test_hand_edited_tags_are_normalized(store, tmp_path, roh, tags):
    """B5: `tags: abc` wurde zu drei Ein-Buchstaben-Tags (`list("abc")`), verschachtelte Werte
    brachen die Suche. Nach dem Neuaufbau sehen Index und `get()` dieselbe Liste."""
    item = store.create("alpha", type="task", title="Hallo")
    _von_hand(tmp_path, item.id, "tags: []", roh)
    assert store.rebuild_index().items_indexed == 1
    assert store.get(item.id).tags == tags
    assert store.search("hallo").total == 1


def test_hand_edited_int_link_does_not_break_get(store, tmp_path):
    """15.3, Fund neben B5: `links: [1]` von Hand brach `get()` und jedes Update
    (`ITEM_REF_RE.fullmatch` auf einem `int`)."""
    item = store.create("alpha", type="task", title="Hallo")
    _von_hand(tmp_path, item.id, "links: []", "links: [1]")
    gelesen = store.get(item.id)
    assert gelesen.links == ["1"]
    assert store.update(item.id, version=gelesen.version, status="done").links == ["1"]


@pytest.mark.parametrize("feld, wert", [
    ("tags", [1, 2]), ("tags", "abc"), ("links", [1]), ("title", 123), ("title", None),
    ("body", 5), ("type", ["task"]), ("status", ["open"]), ("folder", 123), ("share_read", "bob"),
])
def test_update_rejects_wrong_types_before_writing(store_git, tmp_path, feld, wert):
    """B5/B8, Schreiben ist streng: ein falscher Typ ist `ValidationError` — Datei, Version und
    Git-Historie bleiben, wie sie waren. Vorher schrieb `body: 5` Datei und Index und warf erst
    danach; `tags: "abc"` wurde zu drei Tags."""
    item = store_git.create("alpha", type="task", title="Hallo")
    pfad = next(tmp_path.rglob(f"{item.id}__*.md"))
    vorher, commits = pfad.read_bytes(), _commits(tmp_path)
    with pytest.raises(ValidationError):
        store_git.update(item.id, version=1, **{feld: wert})
    assert pfad.read_bytes() == vorher
    assert store_git.get(item.id).version == 1
    assert _commits(tmp_path) == commits


@pytest.mark.parametrize("felder", [
    {"tags": [1, 2]}, {"tags": "abc"}, {"links": "itm_00000000"}, {"title": 123}, {"body": 5},
])
def test_create_rejects_wrong_types(store, tmp_path, felder):
    with pytest.raises(ValidationError):
        store.create("alpha", **{"type": "task", "title": "Hallo", **felder})
    assert not list(tmp_path.rglob("itm_*.md"))


def test_link_failure_leaves_no_written_file(store_git, tmp_path, monkeypatch):
    """B8, die strukturelle Garantie hinter der Typpruefung: was beim Schreiben noch werfen kann,
    wirft **vor** dem Write. Hier wirft die Link-Extraktion (erzwungen) — Datei, Version und
    Historie bleiben unveraendert, statt einer Datei auf v+1 ohne Commit."""
    import storage.store as store_mod

    item = store_git.create("alpha", type="task", title="Hallo")
    pfad = next(tmp_path.rglob(f"{item.id}__*.md"))
    vorher, commits = pfad.read_bytes(), _commits(tmp_path)

    def kaputt(_body):
        raise RuntimeError("Link-Extraktion")

    monkeypatch.setattr(store_mod, "extract_item_refs", kaputt)
    with pytest.raises(RuntimeError):
        store_git.update(item.id, version=1, body="neu")
    monkeypatch.undo()
    assert pfad.read_bytes() == vorher
    assert store_git.get(item.id).version == 1
    assert _commits(tmp_path) == commits


# -- P10.5 Block 15.3b (E5 = A): ein `share_*`-Skalar von Hand ist eine Freigabe ------------


@pytest.mark.parametrize("feld", ["share_read", "share_write"])
def test_hand_edited_scalar_share_is_one_grant(store, tmp_path, caplog, feld):
    """E5 = A (Nikinger, 2026-10-30): `share_read: fabian` von Hand ist **eine** Freigabe an
    `fabian`. Vorher: sechs Freigaben an `f`, `a`, `b`, … — in `acl_of()` (aus dem Index) wie in
    `get()` —, und der erste gewoehnliche Write schrieb die Buchstabenliste auf die Platte.
    Jede Koerzion meldet ein `WARNING` mit Pfad: die Rechteerweiterung lief am Re-Auth-Gate
    vorbei, also muss sie im Log stehen."""
    item = store.create("alpha", type="task", title="Hallo")
    pfad = _von_hand(tmp_path, item.id, "links: []", f"links: []\n{feld}: fabian")
    with caplog.at_level(logging.WARNING, logger="storage.frontmatter"):
        assert store.rebuild_index().items_indexed == 1
    assert any(str(pfad) in r.getMessage() and feld in r.getMessage() for r in caplog.records)
    assert getattr(store.acl_of(item.id), feld) == frozenset({"fabian"})
    # Im Betrieb warnt `get()`/`search()` (der Start baut den Index nicht neu) — der Pfad muss
    # auch auf diesem Weg (`_row_to_item`) in der Meldung stehen.
    caplog.clear()
    with caplog.at_level(logging.WARNING, logger="storage.frontmatter"):
        gelesen = store.get(item.id)
    assert any(str(pfad) in r.getMessage() for r in caplog.records)
    assert getattr(gelesen, feld) == ["fabian"]
    store.update(item.id, version=gelesen.version, status="done")
    assert f"{feld}:\n- fabian\n" in pfad.read_text(encoding="utf-8")
    assert getattr(store.acl_of(item.id), feld) == frozenset({"fabian"})


@pytest.mark.parametrize("roh, erwartet", [
    ("share_read: [fabian]", ["fabian"]),
    ("share_read:", []),
    ("share_read: ~", []),
])
def test_share_list_or_empty_reads_without_warning(store, tmp_path, caplog, roh, erwartet):
    """15.3b: nur der Skalar warnt — die Listenform und ein leeres Feld sind kein Befund."""
    item = store.create("alpha", type="task", title="Hallo")
    _von_hand(tmp_path, item.id, "links: []", f"links: []\n{roh}")
    with caplog.at_level(logging.WARNING, logger="storage.frontmatter"):
        store.rebuild_index()
        assert store.get(item.id).share_read == erwartet
    assert not [r for r in caplog.records if r.name == "storage.frontmatter"]
    assert store.acl_of(item.id).share_read == frozenset(erwartet)
