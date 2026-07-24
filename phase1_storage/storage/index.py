"""SQLite-Index: reine Ableitung aus den Dateien (Entscheidung A). Jederzeit löschbar und
komplett aus `DATA_ROOT` rekonstruierbar über `rebuild_index()`. Ein korrupter Index ist nie
fatal — `connect()` erkennt das und baut ein leeres Schema neu auf; die Befüllung übernimmt
danach `rebuild_index()`.
"""
from __future__ import annotations

import hashlib
import json
import logging
import sqlite3
import time
from pathlib import Path

from .frontmatter import parse as parse_frontmatter
from .models import IndexStats

logger = logging.getLogger(__name__)

SAFE_FILESYSTEMS = {"ext4", "xfs", "btrfs"}

_SCHEMA = """
CREATE TABLE IF NOT EXISTS items (
    id TEXT PRIMARY KEY,
    space TEXT NOT NULL,
    type TEXT NOT NULL,
    title TEXT NOT NULL,
    status TEXT NOT NULL,
    due TEXT,
    tags_json TEXT NOT NULL,
    links_json TEXT NOT NULL,
    created TEXT NOT NULL,
    updated TEXT NOT NULL,
    version INTEGER NOT NULL,
    path TEXT NOT NULL,
    mtime REAL NOT NULL,
    size INTEGER NOT NULL,
    sha256 TEXT NOT NULL
);
"""


def connect(db_path: Path) -> sqlite3.Connection:
    """Öffnet (oder legt an) den Index. Ein korrupter DB-File wird verworfen und leer neu
    angelegt, nie eskaliert — die Wiederbefüllung ist Aufgabe von `rebuild_index()`.
    """
    try:
        conn = _open_and_init(db_path)
        conn.execute("SELECT COUNT(*) FROM items")
    except sqlite3.DatabaseError:
        logger.critical("Index %s ist korrupt — wird verworfen und leer neu angelegt", db_path)
        _discard(db_path)
        conn = _open_and_init(db_path)
    conn.row_factory = sqlite3.Row
    return conn


def _open_and_init(db_path: Path) -> sqlite3.Connection:
    # check_same_thread=False: Store serialisiert jeden Zugriff selbst über sein eigenes Lock
    # (Plan §3.1, "ein Prozess reicht"). Ohne das hier würde sqlite3 jeden Cross-Thread-Zugriff
    # ablehnen, auch wenn er durch das Store-Lock längst serialisiert ist.
    conn = sqlite3.connect(db_path, check_same_thread=False)
    try:
        conn.execute("PRAGMA journal_mode=WAL")
        conn.execute(_SCHEMA)
        conn.commit()
    except sqlite3.DatabaseError:
        conn.close()
        raise
    return conn


def _discard(db_path: Path) -> None:
    db_path.unlink(missing_ok=True)
    for suffix in ("-wal", "-shm"):
        Path(str(db_path) + suffix).unlink(missing_ok=True)


def upsert_item(conn: sqlite3.Connection, row: dict) -> None:
    _upsert_no_commit(conn, row)
    conn.commit()


def _upsert_no_commit(conn: sqlite3.Connection, row: dict) -> None:
    conn.execute(
        """
        INSERT INTO items (id, space, type, title, status, due, tags_json, links_json,
                            created, updated, version, path, mtime, size, sha256)
        VALUES (:id, :space, :type, :title, :status, :due, :tags_json, :links_json,
                :created, :updated, :version, :path, :mtime, :size, :sha256)
        ON CONFLICT(id) DO UPDATE SET
            space=excluded.space, type=excluded.type, title=excluded.title,
            status=excluded.status, due=excluded.due, tags_json=excluded.tags_json,
            links_json=excluded.links_json, created=excluded.created,
            updated=excluded.updated, version=excluded.version, path=excluded.path,
            mtime=excluded.mtime, size=excluded.size, sha256=excluded.sha256
        """,
        row,
    )


def delete_item(conn: sqlite3.Connection, item_id: str) -> None:
    conn.execute("DELETE FROM items WHERE id = ?", (item_id,))
    conn.commit()


def get_item_row(conn: sqlite3.Connection, item_id: str) -> sqlite3.Row | None:
    return conn.execute("SELECT * FROM items WHERE id = ?", (item_id,)).fetchone()


def all_rows(conn: sqlite3.Connection) -> list[sqlite3.Row]:
    return conn.execute("SELECT * FROM items ORDER BY id").fetchall()


def row_from_file(data_root: Path, path: Path) -> dict:
    """Liest eine Item-Datei und baut die dazugehörige Index-Zeile. Kein Schreibzugriff."""
    raw_bytes = path.read_bytes()
    fields, _body = parse_frontmatter(raw_bytes.decode("utf-8"))
    stat = path.stat()
    return {
        "id": fields["id"],
        "space": path.relative_to(data_root).parts[0],
        "type": fields["type"],
        "title": fields["title"],
        "status": fields["status"],
        "due": fields.get("due"),
        "tags_json": json.dumps(fields.get("tags", [])),
        "links_json": json.dumps(fields.get("links", [])),
        "created": fields["created"],
        "updated": fields["updated"],
        "version": fields["version"],
        "path": path.relative_to(data_root).as_posix(),
        "mtime": stat.st_mtime,
        "size": stat.st_size,
        "sha256": hashlib.sha256(raw_bytes).hexdigest(),
    }


def rebuild_index(data_root: Path, conn: sqlite3.Connection) -> IndexStats:
    """Verwirft den Indexinhalt und baut ihn komplett aus den Dateien unter `data_root` neu auf.
    Ein Index-Fehler darf nie eine Datei anfassen — diese Funktion liest ausschließlich.
    """
    start = time.monotonic()
    conn.execute("DELETE FROM items")
    count = 0
    for space_dir in sorted(p for p in data_root.iterdir() if p.is_dir() and not p.name.startswith(".")):
        for md_path in sorted(space_dir.rglob("*.md")):
            row = row_from_file(data_root, md_path)
            _upsert_no_commit(conn, row)
            count += 1
    conn.commit()
    return IndexStats(items_indexed=count, duration_seconds=time.monotonic() - start)


def detect_filesystem_type(path: Path) -> str:
    """Liest `/proc/mounts` und liefert den Dateisystemtyp des am tiefsten passenden Mountpoints.

    `os.statvfs` liefert den Typ nicht direkt (nur Blockgrößen etc.) — `/proc/mounts` ist unter
    Linux die einfachste zuverlässige Quelle (`[VERIFY]` aus dem Plan, hiermit aufgelöst).
    """
    resolved = str(path.resolve())
    best: tuple[str, str] | None = None
    with open("/proc/mounts", encoding="utf-8") as f:
        for line in f:
            parts = line.split()
            if len(parts) < 3:
                continue
            mount_point = parts[1].replace("\\040", " ")
            fstype = parts[2]
            if resolved == mount_point or resolved.startswith(mount_point.rstrip("/") + "/"):
                if best is None or len(mount_point) > len(best[0]):
                    best = (mount_point, fstype)
    if best is None:
        raise RuntimeError(f"kein Mountpoint für {path} in /proc/mounts gefunden")
    return best[1]


def check_filesystem(path: Path, *, fstype: str | None = None) -> str:
    """Prüft `path` gegen `SAFE_FILESYSTEMS` und loggt `critical` bei Abweichung — nie fatal.

    `fstype` kann für Tests direkt injiziert werden, um `/proc/mounts` zu umgehen.
    """
    resolved_fstype = fstype if fstype is not None else detect_filesystem_type(path)
    if resolved_fstype not in SAFE_FILESYSTEMS:
        logger.critical(
            "DATA_ROOT %s liegt auf Dateisystem %r (nicht in %s) — flock ist dort ggf. nicht "
            "verlässlich, siehe phase1_storage_plan.md §3.2",
            path,
            resolved_fstype,
            sorted(SAFE_FILESYSTEMS),
        )
    return resolved_fstype
