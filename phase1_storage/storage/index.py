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

from .files import folder_from_path
from .frontmatter import parse as parse_frontmatter
from .linkscan import ITEM_REF_RE, extract_item_refs
from .models import IndexStats

logger = logging.getLogger(__name__)

SAFE_FILESYSTEMS = {"ext4", "xfs", "btrfs"}

# P6 Step 4 (Plan §1.4, V46): der Index kannte bis hierher keinen Versionsbegriff. Ein Sprung
# hier heißt "Schema verworfen und leer neu angelegt" (Hard Rule 2 — der Index ist Ableitung,
# billiger als jede Migration), nie ein `ALTER TABLE`.
#
# Phase 8 Block B (P8-M, achte P1-Contract-Oeffnung): Version 3 fuegt `item_links` hinzu --
# Kantenmenge zwischen Items, getrennt nach `kind` (`frontmatter`/`body`). Rebuild heilt
# alte Indices ueber `CREATE IF NOT EXISTS` + `rebuild_index()` (Hard Rule 2, keine Migration).
INDEX_SCHEMA_VERSION = 3

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
    sha256 TEXT NOT NULL,
    folder TEXT NOT NULL DEFAULT '',
    visibility TEXT NOT NULL DEFAULT 'private',
    share_read_json TEXT NOT NULL DEFAULT '[]',
    share_write_json TEXT NOT NULL DEFAULT '[]'
);

-- Phase 8 Block B Step B2 (P8-M): Item-zu-Item-Kanten. `src_id` ist immer ein existierendes
-- Item, `dst_id` MUSS nicht existieren (eine Notiz darf eine ID nennen, die (noch) nicht
-- existiert -- der API-Endpoint filtert das beim Lesen). `kind` unterscheidet Herkunft:
-- `frontmatter` = Eintrag im `links:`-Feld (menschengewollt), `body` = `itm_...`-Erwähnung im
-- Markdown-Body (mechanisch extrahiert, Plan §3 P8-M). PK ueber alle drei Spalten verhindert
-- Doppelkanten derselben Art; ein und dieselbe ID darf als Frontmatter- UND Body-Kante
-- existieren (zwei Zeilen, getrennte Kinds).
CREATE TABLE IF NOT EXISTS item_links (
    src_id TEXT NOT NULL,
    dst_id TEXT NOT NULL,
    kind TEXT NOT NULL,
    PRIMARY KEY (src_id, dst_id, kind)
);
CREATE INDEX IF NOT EXISTS idx_item_links_dst ON item_links(dst_id);
"""


def connect(db_path: Path) -> tuple[sqlite3.Connection, bool]:
    """Öffnet (oder legt an) den Index. Liefert `(conn, rebuilt)` — `rebuilt=True` heißt: das
    Schema wurde in diesem Aufruf leer neu angelegt (Datei fehlte, war korrupt, oder
    `PRAGMA user_version` stimmte nicht mit `INDEX_SCHEMA_VERSION` überein), der Index-Inhalt
    ist also leer.

    Das ist ein Rückkanal, den es vor P6 Step 4 nicht gab: `Store.__init__` ruft bei
    `rebuilt=True` selbst `rebuild_index()` — ohne das bliebe der Produktivindex nach dem
    nächsten echten Deploy leer, weil `phase2_mcp/scripts/serve.py` `rebuild_index()` sonst nie
    aufruft (einziger heutiger Aufrufer ist der manuelle `space_cli.py`-Befehl).
    """
    conn: sqlite3.Connection | None = None
    current_version: int | None = None
    try:
        conn = _open_and_init(db_path)
        conn.execute("SELECT COUNT(*) FROM items")
        current_version = conn.execute("PRAGMA user_version").fetchone()[0]
    except sqlite3.DatabaseError:
        conn = None

    if conn is not None and current_version == INDEX_SCHEMA_VERSION:
        conn.row_factory = sqlite3.Row
        return conn, False

    if conn is not None:
        conn.close()
        logger.critical(
            "Index %s hat Schema-Version %r (erwartet %r) — wird verworfen und leer neu "
            "angelegt", db_path, current_version, INDEX_SCHEMA_VERSION,
        )
    else:
        logger.critical("Index %s ist korrupt — wird verworfen und leer neu angelegt", db_path)

    _discard(db_path)
    conn = _open_and_init(db_path)
    conn.execute(f"PRAGMA user_version = {INDEX_SCHEMA_VERSION}")
    conn.commit()
    conn.row_factory = sqlite3.Row
    return conn, True


def _open_and_init(db_path: Path) -> sqlite3.Connection:
    # check_same_thread=False: Store serialisiert jeden Zugriff selbst über sein eigenes Lock
    # (Plan §3.1, "ein Prozess reicht"). Ohne das hier würde sqlite3 jeden Cross-Thread-Zugriff
    # ablehnen, auch wenn er durch das Store-Lock längst serialisiert ist.
    conn = sqlite3.connect(db_path, check_same_thread=False)
    try:
        conn.execute("PRAGMA journal_mode=WAL")
        # `executescript` fuer mehrstellige SQL: Phase 8 Block B Step B2 ergaenzt die Tabelle
        # `item_links` + Index, der String enthaelt damit mehrere durch `;` getrennte
        # Anweisungen -- `conn.execute` kann nur eine. `executescript` fuehrt sie alle in einer
        # impliziten Transaktion aus.
        conn.executescript(_SCHEMA)
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
                            created, updated, version, path, mtime, size, sha256,
                            folder, visibility, share_read_json, share_write_json)
        VALUES (:id, :space, :type, :title, :status, :due, :tags_json, :links_json,
                :created, :updated, :version, :path, :mtime, :size, :sha256,
                :folder, :visibility, :share_read_json, :share_write_json)
        ON CONFLICT(id) DO UPDATE SET
            space=excluded.space, type=excluded.type, title=excluded.title,
            status=excluded.status, due=excluded.due, tags_json=excluded.tags_json,
            links_json=excluded.links_json, created=excluded.created,
            updated=excluded.updated, version=excluded.version, path=excluded.path,
            mtime=excluded.mtime, size=excluded.size, sha256=excluded.sha256,
            folder=excluded.folder, visibility=excluded.visibility,
            share_read_json=excluded.share_read_json, share_write_json=excluded.share_write_json
        """,
        row,
    )


def delete_item(conn: sqlite3.Connection, item_id: str) -> None:
    """Entfernt ein Item aus dem Index. Räumt auch die `item_links`-Zeilen mit dieser `src_id`
    auf (Phase 8 Block B Step B2, P8-M) -- ein verwaistes `dst_id` (das Item zeigte auf ein
    inzwischen geloeschtes anderes Item) bleibt stehen, die API filtert das beim Lesen."""
    conn.execute("DELETE FROM items WHERE id = ?", (item_id,))
    conn.execute("DELETE FROM item_links WHERE src_id = ?", (item_id,))
    conn.commit()


def get_item_row(conn: sqlite3.Connection, item_id: str) -> sqlite3.Row | None:
    return conn.execute("SELECT * FROM items WHERE id = ?", (item_id,)).fetchone()


def all_rows(conn: sqlite3.Connection) -> list[sqlite3.Row]:
    return conn.execute("SELECT * FROM items ORDER BY id").fetchall()


def replace_item_links(
    conn: sqlite3.Connection, src_id: str, rows: list[tuple[str, str]]
) -> None:
    """Phase 8 Block B Step B2 (P8-M): ersetzt die Kantenmenge eines Items vollständig.

    `rows` ist `[(dst_id, kind), ...]`. Semantik: ALLE bisherigen Zeilen mit dieser `src_id`
    verschwinden, die übergebenen werden genau so eingefügt. `kind` ∈ {"frontmatter", "body"}.
    Eine leere Liste löscht alle Kanten dieses Items.

    Implementierung in EINEM `BEGIN`-Block, damit `rebuild_index()` und Store-Schreibpfade
    nicht zwischen DELETE und INSERT von einem Leser in einem halb-leeren Zustand gesehen
    werden. sqlite3's autocommit + `commit()` am Ende ist hier ausreichend (single-threaded
    durch `Store._lock`).
    """
    conn.execute("DELETE FROM item_links WHERE src_id = ?", (src_id,))
    if rows:
        conn.executemany(
            "INSERT INTO item_links (src_id, dst_id, kind) VALUES (?, ?, ?)",
            [(src_id, dst_id, kind) for (dst_id, kind) in rows],
        )
    conn.commit()


def all_links(conn: sqlite3.Connection) -> list[sqlite3.Row]:
    """Liest alle `item_links`-Zeilen. Sortierung: (src_id, kind, dst_id) -- deterministisch
    für Tests."""
    return conn.execute(
        "SELECT src_id, dst_id, kind FROM item_links ORDER BY src_id, kind, dst_id"
    ).fetchall()


def row_from_file(data_root: Path, path: Path) -> dict:
    """Liest eine Item-Datei und baut die dazugehörige Index-Zeile. Kein Schreibzugriff.

    Phase 8 Block B Step B2 (P8-M): gibt zusaetzlich `body_refs` (reine `itm_…`-Referenzen im
    Markdown-Body, Auftrittsreihenfolge, dedupliziert) im Dict zurueck. Konsumenten, die das
    Key nicht kennen (namentlich `upsert_item` via `_upsert_no_commit`), ignorieren es still --
    der INSERT-Statement nennt die Spalte nicht. `body_refs` wird ausschliesslich von
    `rebuild_index()` und `_reconcile_and_get_row()` gelesen, um `item_links` zu befuellen."""
    raw_bytes = path.read_bytes()
    text = raw_bytes.decode("utf-8")
    fields, body = parse_frontmatter(text)
    stat = path.stat()
    space = path.relative_to(data_root).parts[0]
    return {
        "id": fields["id"],
        "space": space,
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
        # `folder` ist immer abgeleitet (Plan §1.3), nie ein Frontmatter-Feld -- anders als
        # `visibility`/`share_*`, die aus der Datei kommen und beim Fehlen ihren Default nehmen
        # (gleiches Muster wie `due` oben).
        "folder": folder_from_path(data_root, space, path),
        "visibility": fields.get("visibility", "private"),
        "share_read_json": json.dumps(fields.get("share_read", []) or []),
        "share_write_json": json.dumps(fields.get("share_write", []) or []),
        # Body-Referenzen, NICHT in `items` gespeichert, nur fuer `item_links`-Befuellung.
        "body_refs": extract_item_refs(body),
    }


def rebuild_index(data_root: Path, conn: sqlite3.Connection) -> IndexStats:
    """Verwirft den Indexinhalt und baut ihn komplett aus den Dateien unter `data_root` neu auf.
    Ein Index-Fehler darf nie eine Datei anfassen — diese Funktion liest ausschließlich.

    Phase 8 Block B Step B2 (P8-M): befuellt zusaetzlich `item_links`. Pro Datei: erst
    `upsert_item` (die `items`-Zeile), dann `replace_item_links` mit den Frontmatter-Referenzen
    (alle `links:`-Eintraege, die `ITEM_REF_RE.fullmatch` passieren -- beliebige Strings im
    `links:`-Feld bleiben erlaubt und werden keine Kante) plus den Body-Referenzen aus
    `row_from_file()["body_refs"]`. `DELETE FROM items` oben wird durch `DELETE FROM
    item_links` ergaenzt -- sonst bleiben stale Kanten aus dem Vorab-Stand stehen."""
    start = time.monotonic()
    conn.execute("DELETE FROM items")
    conn.execute("DELETE FROM item_links")
    count = 0
    edge_count = 0
    for space_dir in sorted(p for p in data_root.iterdir() if p.is_dir() and not p.name.startswith(".")):
        for md_path in sorted(space_dir.rglob("*.md")):
            row = row_from_file(data_root, md_path)
            _upsert_no_commit(conn, row)
            frontmatter_refs = [
                ref for ref in json.loads(row["links_json"]) if ITEM_REF_RE.fullmatch(ref)
            ]
            rows = [(ref, "frontmatter") for ref in frontmatter_refs] + [
                (ref, "body") for ref in row["body_refs"]
            ]
            replace_item_links(conn, row["id"], rows)
            count += 1
            edge_count += len(rows)
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
