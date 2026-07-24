import logging

import pytest

from storage import index
from storage.frontmatter import serialize


def _write_item(data_root, space, item_id, slug, *, title, due=None, tags=None, links=None,
                 version=1, status="open", item_type="task", body="Body-Text.\n"):
    space_dir = data_root / space
    space_dir.mkdir(parents=True, exist_ok=True)
    fields = {
        "id": item_id,
        "space": space,
        "type": item_type,
        "title": title,
        "status": status,
        "tags": tags or [],
        "links": links or [],
        "created": "2026-07-24T18:20:00Z",
        "updated": "2026-07-24T18:20:00Z",
        "version": version,
    }
    if due is not None:
        fields["due"] = due
    path = space_dir / f"{item_id}__{slug}.md"
    path.write_text(serialize(fields, body))
    return path


def test_connect_creates_empty_schema(tmp_path):
    conn = index.connect(tmp_path / ".index.sqlite3")
    assert index.all_rows(conn) == []


def test_upsert_get_delete_roundtrip(tmp_path):
    conn = index.connect(tmp_path / ".index.sqlite3")
    row = {
        "id": "itm_a1b2c3d4", "space": "nikinger", "type": "task", "title": "Test",
        "status": "open", "due": None, "tags_json": "[]", "links_json": "[]",
        "created": "2026-07-24T18:20:00Z", "updated": "2026-07-24T18:20:00Z", "version": 1,
        "path": "nikinger/itm_a1b2c3d4__test.md", "mtime": 0.0, "size": 10, "sha256": "x",
    }
    index.upsert_item(conn, row)

    fetched = index.get_item_row(conn, "itm_a1b2c3d4")
    assert fetched["title"] == "Test"

    row["title"] = "Geändert"
    index.upsert_item(conn, row)
    assert index.get_item_row(conn, "itm_a1b2c3d4")["title"] == "Geändert"
    assert len(index.all_rows(conn)) == 1

    index.delete_item(conn, "itm_a1b2c3d4")
    assert index.get_item_row(conn, "itm_a1b2c3d4") is None


def test_row_from_file_extracts_expected_fields(tmp_path):
    _write_item(tmp_path, "nikinger", "itm_a1b2c3d4", "kuehlschrank",
                title="Kühlschrank prüfen", due="2026-08-02", tags=["infra"])
    path = tmp_path / "nikinger" / "itm_a1b2c3d4__kuehlschrank.md"

    row = index.row_from_file(tmp_path, path)

    assert row["id"] == "itm_a1b2c3d4"
    assert row["space"] == "nikinger"
    assert row["due"] == "2026-08-02"
    assert row["tags_json"] == '["infra"]'
    assert row["path"] == "nikinger/itm_a1b2c3d4__kuehlschrank.md"
    assert row["size"] == path.stat().st_size


def test_rebuild_index_matches_manual_upserts(tmp_path):
    _write_item(tmp_path, "nikinger", "itm_00000001", "erstes", title="Erstes")
    _write_item(tmp_path, "nikinger", "itm_00000002", "zweites", title="Zweites")
    _write_item(tmp_path, "kollege", "itm_00000003", "drittes", title="Drittes")
    # archivierte Items liegen unter _archive/ und müssen trotzdem indiziert werden
    (tmp_path / "nikinger" / "_archive").mkdir()
    _write_item(tmp_path, "nikinger", "itm_00000004", "viertes", title="Viertes", status="archived")

    conn = index.connect(tmp_path / ".index.sqlite3")
    stats = index.rebuild_index(tmp_path, conn)

    assert stats.items_indexed == 4
    ids = {row["id"] for row in index.all_rows(conn)}
    assert ids == {"itm_00000001", "itm_00000002", "itm_00000003", "itm_00000004"}


def test_rebuild_after_delete_is_identical_to_before(tmp_path):
    _write_item(tmp_path, "nikinger", "itm_00000001", "erstes", title="Erstes", tags=["a", "b"])
    _write_item(tmp_path, "nikinger", "itm_00000002", "zweites", title="Zweites", due="2026-08-02")

    db_path = tmp_path / ".index.sqlite3"
    conn = index.connect(db_path)
    index.rebuild_index(tmp_path, conn)
    before = [dict(r) for r in index.all_rows(conn)]
    conn.close()

    db_path.unlink()
    (tmp_path / ".index.sqlite3-wal").unlink(missing_ok=True)
    (tmp_path / ".index.sqlite3-shm").unlink(missing_ok=True)

    conn2 = index.connect(db_path)
    index.rebuild_index(tmp_path, conn2)
    after = [dict(r) for r in index.all_rows(conn2)]

    assert before == after


def test_corrupt_index_file_is_discarded_not_crashed(tmp_path):
    db_path = tmp_path / ".index.sqlite3"
    db_path.write_bytes(b"das ist keine sqlite datei, nur muell")

    conn = index.connect(db_path)  # darf nicht raisen

    assert index.all_rows(conn) == []

    _write_item(tmp_path, "nikinger", "itm_00000001", "erstes", title="Erstes")
    stats = index.rebuild_index(tmp_path, conn)
    assert stats.items_indexed == 1


def test_check_filesystem_safe_type_logs_nothing(tmp_path, caplog):
    with caplog.at_level(logging.CRITICAL, logger="storage.index"):
        result = index.check_filesystem(tmp_path, fstype="ext4")

    assert result == "ext4"
    assert caplog.records == []


def test_check_filesystem_unsafe_type_logs_exactly_one_critical(tmp_path, caplog):
    with caplog.at_level(logging.CRITICAL, logger="storage.index"):
        result = index.check_filesystem(tmp_path, fstype="nfs4")

    assert result == "nfs4"
    critical_records = [r for r in caplog.records if r.levelno == logging.CRITICAL]
    assert len(critical_records) == 1
    assert "nfs4" in critical_records[0].getMessage()


def test_detect_filesystem_type_against_real_tmp_path(tmp_path):
    # tmp_path liegt im echten Dateisystem der Testmaschine (ext4, siehe Step-0-Verifikation).
    # Kein Verstoss gegen "nie gegen DATA_ROOT testen" -- das ist pytest's eigenes tmp_path.
    assert index.detect_filesystem_type(tmp_path) == "ext4"
