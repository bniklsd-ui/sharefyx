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
    assert 12 * 1024 < size < 16 * 1024


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


def test_create_rejects_folder_deeper_than_max(store):
    with pytest.raises(ValidationError):
        store.create("nikinger", type="note", title="Zu tief", folder="a/b/c")


def test_create_defaults_visibility_and_share_fields_and_omits_them_from_file(store, tmp_path):
    # Offener Punkt (nicht diese Phase's Aufgabe, siehe phase6_shares/CLAUDE.md Session-Block):
    # eine explizit gesetzte `visibility: private` verschwindet beim naechsten `update()` wieder
    # aus der Datei (Default wird nie geschrieben) -- kollidiert potenziell mit Abnahmezeile 8
    # ("jedes Item traegt visibility"), je nachdem wie der Nikinger die Zeile bei der Live-
    # Abnahme liest. Funktional harmlos (fehlend == "private" beim naechsten Lesen), aber vor
    # Step 6s Migrationsabnahme zu klaeren.
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
