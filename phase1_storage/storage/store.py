"""`Store` — die öffentliche API des Pakets (Plan §2). Bindet `files.py`, `frontmatter.py`,
`index.py` und `models.py` zusammen. Kein Netz, kein MCP — Phase 1 ist vollständig offline
testbar (siehe Phase-Mission in `phase1_storage/CLAUDE.md`).
"""
from __future__ import annotations

import fcntl
import json
import sqlite3
import threading
from collections.abc import Sequence
from contextlib import contextmanager
from dataclasses import replace
from datetime import date, datetime, timezone
from pathlib import Path
from typing import Any, Callable

from . import files, history, index
from .acl import ACL_FILENAME, AclDecision, AclReader
from .errors import ConflictError, ItemNotFound, ValidationError
from .frontmatter import parse as parse_frontmatter
from .frontmatter import serialize as serialize_frontmatter
from .models import (
    DEFAULT_VISIBILITY,
    VISIBILITY_VALUES,
    AssetInfo,
    IndexStats,
    Item,
    ItemSummary,
    SearchResult,
    SpaceInfo,
    STATUS_VALUES,
    valid_statuses,
)
from .patch import PatchResult, TextEdit, apply_edits

_KNOWN_FIELDS = {
    "id", "space", "type", "title", "status", "due", "tags", "links",
    "created", "updated", "version", "visibility", "share_read", "share_write",
}
_DEFAULT_STATUS = {"task": "open", "note": "active"}
# Vom Store selbst verwaltet — dürfen nie über **fields/**changes hereinkommen, sonst
# überschreibt `Item.extra` beim Schreiben (`fields.update(item.extra)`) die berechneten Werte.
_SYSTEM_MANAGED_FIELDS = {"id", "space", "created", "updated", "version"}


def _default_now() -> datetime:
    return datetime.now(timezone.utc)


def _coerce_due(value: Any) -> date | None:
    if value is None:
        return None
    if isinstance(value, date):
        return value
    if isinstance(value, str):
        return date.fromisoformat(value)
    raise ValidationError(f"'due' muss date, ISO-String oder None sein, nicht {type(value)!r}")


def _parse_dt(value: str) -> datetime:
    return datetime.fromisoformat(value.replace("Z", "+00:00"))


def _format_dt(value: datetime) -> str:
    return value.astimezone(timezone.utc).strftime("%Y-%m-%dT%H:%M:%SZ")


def _item_from_text(text: str, *, version_override: int | None = None, folder_override: str = "") -> Item:
    fields, body = parse_frontmatter(text)
    extra = {k: v for k, v in fields.items() if k not in _KNOWN_FIELDS}
    return Item(
        id=fields["id"],
        space=fields["space"],
        type=fields["type"],
        title=fields["title"],
        status=fields["status"],
        body=body,
        due=date.fromisoformat(fields["due"]) if fields.get("due") else None,
        tags=list(fields.get("tags", []) or []),
        links=list(fields.get("links", []) or []),
        created=_parse_dt(fields["created"]),
        updated=_parse_dt(fields["updated"]),
        version=version_override if version_override is not None else fields["version"],
        folder=folder_override,
        visibility=fields.get("visibility", DEFAULT_VISIBILITY),
        share_read=list(fields.get("share_read", []) or []),
        share_write=list(fields.get("share_write", []) or []),
        extra=extra,
    )


def _item_to_text(item: Item) -> str:
    fields: dict[str, Any] = {
        "id": item.id,
        "space": item.space,
        "type": item.type,
        "title": item.title,
        "status": item.status,
    }
    if item.due is not None:
        fields["due"] = item.due.isoformat()
    fields["tags"] = list(item.tags)
    fields["links"] = list(item.links)
    fields["created"] = _format_dt(item.created)
    fields["updated"] = _format_dt(item.updated)
    fields["version"] = item.version
    # P6 Step 4: nur schreiben, wenn vom Default abweichend (Plan §2.1: "leer = nicht
    # vorhanden") -- sonst bekäme jedes bestehende Item beim nächsten Write ein stilles
    # `visibility: private`, obwohl das explizit Aufgabe von `migrate_visibility.py` (Step 6)
    # ist, nicht ein Nebeneffekt dieses Schritts. `folder` erscheint hier nie -- abgeleitet,
    # nie Frontmatter.
    if item.visibility != DEFAULT_VISIBILITY:
        fields["visibility"] = item.visibility
    if item.share_read:
        fields["share_read"] = list(item.share_read)
    if item.share_write:
        fields["share_write"] = list(item.share_write)
    fields.update(item.extra)
    return serialize_frontmatter(fields, item.body)


def _snippet(body: str, *, length: int = 160) -> str:
    text = " ".join(body.split())
    if len(text) <= length:
        return text
    cut = text.rfind(" ", 0, length)
    if cut <= 0:
        cut = length
    return text[:cut] + "…"


def _check_type_and_status(item_type: str, status: str) -> None:
    """Wirft `ValidationError` bei unbekanntem `type` oder einem `status`, der laut
    `models.STATUS_VALUES` für diesen `type` nicht erlaubt ist (Entscheidung D2). Einmal hier
    statt in jedem Adapter (CLI, MCP) neu — die CLI hielt das bisher nur über `argparse choices`
    ab, was ein zweiter Eingang (MCP) umgangen hätte.
    """
    allowed = valid_statuses(item_type)
    if not allowed:
        raise ValidationError(f"Unbekannter type {item_type!r} — erlaubt: {sorted(STATUS_VALUES)}")
    if status not in allowed:
        raise ValidationError(
            f"Status {status!r} nicht erlaubt für type {item_type!r} — erlaubt: {sorted(allowed)}"
        )


def _summary(item: Item) -> ItemSummary:
    return ItemSummary(
        id=item.id, space=item.space, type=item.type, title=item.title, status=item.status,
        due=item.due, tags=list(item.tags), links=list(item.links),
        created=item.created, updated=item.updated, version=item.version,
        snippet=_snippet(item.body),
        folder=item.folder, visibility=item.visibility,
        share_read=list(item.share_read), share_write=list(item.share_write),
    )


class Store:
    def __init__(
        self,
        data_root: Path,
        *,
        now_fn: Callable[[], datetime] = _default_now,
        git: bool = True,
    ) -> None:
        self._data_root = Path(data_root)
        self._now_fn = now_fn
        self._git_enabled = git
        self._lock = threading.RLock()
        self._db_path = self._data_root / ".index.sqlite3"
        self._conn, rebuilt = index.connect(self._db_path)
        self._acl = AclReader(self._data_root)
        if self._git_enabled:
            history.ensure_repo(self._data_root)
        if rebuilt:
            # Das Schema wurde gerade leer (neu) angelegt (V46-Fix, siehe index.connect()) --
            # ohne diesen Aufruf bliebe ein echter Dienst-Neustart nach einem Schema-Sprung
            # dauerhaft mit leerem Index laufen, weil `serve.py` `rebuild_index()` sonst nie
            # aufruft. Dateien sind die Wahrheit (Hard Rule 2), das hier ist billig.
            self.rebuild_index()

    # -- Sperren -----------------------------------------------------------------

    @contextmanager
    def _file_write_lock(self):
        """`flock` auf `<DATA_ROOT>/.write.lock` — schützt gegen andere Prozesse (nicht gegen
        den Menschen im Editor, siehe Plan §3.2). Nur um den eigentlichen Dateischreibvorgang.
        """
        lock_path = self._data_root / ".write.lock"
        lock_path.touch(exist_ok=True)
        with open(lock_path, "r+") as f:
            fcntl.flock(f, fcntl.LOCK_EX)
            try:
                yield
            finally:
                fcntl.flock(f, fcntl.LOCK_UN)

    def _commit(self, op: str, item_id: str, space: str) -> None:
        """Git-Commit nach einem erfolgreichen Write (Entscheidung E), Message `<op> <id>
        [<space>]`. Wird ausschließlich aus Aufrufern heraus benutzt, die bereits
        `self._file_write_lock()` halten — das serialisiert die Git-Aufrufe auch über
        Prozessgrenzen hinweg (siehe `history.commit`-Docstring). Nie fatal: `history.commit`
        loggt selbst `critical` und wirft nie.
        """
        if self._git_enabled:
            history.commit(self._data_root, f"{op} {item_id} [{space}]")

    # -- Interne Helfer ------------------------------------------------------------

    def _row_to_item(self, row: sqlite3.Row) -> Item:
        path = self._data_root / row["path"]
        # `folder` wird aus dem Pfad NEU abgeleitet, nicht aus `row["folder"]` übernommen: die
        # Index-Spalte ist reine Ableitung (Hard Rule 2), kein autoritativer Wert. Würde ein
        # veralteter/falscher Index-Wert hier direkt durchgereicht, würde ihn `update()` beim
        # nächsten Schreibvorgang über `_write_item_file`s Zielpfad-Berechnung ungefragt zur
        # Wahrheit machen und die Datei verschieben — "ein Index-Fehler fasst nie eine Datei an"
        # (`phase1_storage/CLAUDE.md`) gilt auch hier.
        return _item_from_text(
            path.read_text(encoding="utf-8"),
            version_override=row["version"],
            folder_override=files.folder_from_path(self._data_root, row["space"], path),
        )

    def _reconcile_and_get_row(self, item_id: str, *, repair_drift: bool = True) -> sqlite3.Row:
        """Liest die Indexzeile, erkennt externe Edits (Entscheidung D) und reindiziert bei
        Bedarf. Bei echter Inhaltsänderung wird die gebumpte Version **ins Frontmatter
        zurückgeschrieben** — sonst würde ein `rebuild_index()` (Entscheidung A, jederzeit
        erlaubt, läuft laut Plan G beim Start) die Version wieder auf den alten Dateistand
        zurücksetzen und das Konfliktschutz-Fenster lautlos wieder öffnen (Nikinger-Entscheidung
        2026-07-24, siehe Session-stopped-Block).

        `repair_drift=False` (P2 Step 2, Entscheidung D3): bei erkannter Inhaltsänderung wird
        **nicht** ins Frontmatter zurückgeschrieben und **kein** Git-Commit erzeugt — nur der
        Index wird nachgezogen (reine Ableitung, kein Cross-Space-Write). Für fremde Spaces:
        ein Lesezugriff dort fasst keine Datei an (Rule 4); `version` ist dort informativ, nicht
        autoritativ, weil es dort per Architektur keine Writes gibt.

        Muss unter `self._lock` **und** `self._file_write_lock()` aufgerufen werden — diese
        Methode kann schreiben (deshalb keine eigene Lock-Verwaltung: verschachteltes `flock`
        auf demselben Lockfile würde sich selbst blockieren, wenn `update`/`append`/`archive`
        den Write-Lock bereits halten und intern hierher reinlaufen).
        """
        row = index.get_item_row(self._conn, item_id)
        if row is None:
            raise ItemNotFound(item_id)
        path = self._data_root / row["path"]
        if not path.exists():
            raise ItemNotFound(item_id)
        stat = path.stat()
        if stat.st_mtime != row["mtime"] or stat.st_size != row["size"]:
            fresh = index.row_from_file(self._data_root, path)
            if fresh["sha256"] != row["sha256"]:
                if repair_drift:
                    new_version = row["version"] + 1
                    self._rewrite_version_in_file(path, new_version)
                    self._commit("drift", item_id, row["space"])
                    fresh = index.row_from_file(self._data_root, path)
                # sonst: `fresh["version"]` trägt bereits die Version aus der Datei selbst
                # (der Mensch hat sie nie angefasst) — nichts weiter zu tun.
            else:
                fresh["version"] = row["version"]
            index.upsert_item(self._conn, fresh)
            row = index.get_item_row(self._conn, item_id)
        return row

    def _rewrite_version_in_file(self, path: Path, new_version: int) -> None:
        """Schreibt nur das `version`-Feld neu — sonst nichts. Minimaler Fußabdruck: die Datei
        bleibt bis auf dieses eine Feld exakt so, wie der Mensch sie hinterlassen hat.
        """
        text = path.read_text(encoding="utf-8")
        fields, body = parse_frontmatter(text)
        fields["version"] = new_version
        files.atomic_write(path, serialize_frontmatter(fields, body))

    def _write_item_file(self, item: Item, *, old_path: Path | None, op: str) -> Path:
        """Schreibt `item` an den (ggf. neuen) Pfad, benennt bei Titeländerung um, aktualisiert
        den Index und committet (`op` benennt den Git-Commit, z.B. "create"/"update"/"append").
        Muss unter `self._lock` **und** `self._file_write_lock()` aufgerufen werden.
        """
        slug = files.slugify(item.title)
        target_path = files.item_path(self._data_root, item.space, item.id, slug, folder=item.folder)
        write_path = old_path if old_path is not None else target_path
        write_path.parent.mkdir(parents=True, exist_ok=True)
        files.atomic_write(write_path, _item_to_text(item))
        if old_path is not None and old_path != target_path:
            files.move_file(write_path, target_path)
        row = index.row_from_file(self._data_root, target_path)
        index.upsert_item(self._conn, row)
        self._commit(op, item.id, item.space)
        return target_path

    # -- Öffentliche API (Plan §2) ---------------------------------------------------

    def list_spaces(self) -> list[SpaceInfo]:
        """Vereinigung aus Verzeichnissen unter `data_root` und Indexzeilen (P6 Step 4, Plan
        §1.4) — ein frisch angelegter geteilter Space ohne Item wäre sonst unsichtbar (derselbe
        Fund wie B1 aus der P2-Adapter-Abnahme, eine Ebene höher). `members` kommt aus der
        Space-Wurzel-`.share.yml`, `folders` aus einem sortierten Verzeichnis-Walk ohne
        `RESERVED_DIR_NAMES`.
        """
        with self._lock:
            counts: dict[str, int] = {}
            for row in index.all_rows(self._conn):
                counts[row["space"]] = counts.get(row["space"], 0) + 1
            disk_spaces = {
                p.name for p in self._data_root.iterdir()
                if p.is_dir() and not p.name.startswith(".")
            }
            names = sorted(set(counts) | disk_spaces)
            result = []
            for name in names:
                space_dir = self._data_root / name
                members = tuple(sorted(self._acl.members_of_space(name)))
                folders: tuple[str, ...] = ()
                if space_dir.is_dir():
                    folders = tuple(sorted(
                        d.relative_to(space_dir).as_posix()
                        for d in space_dir.rglob("*")
                        if d.is_dir()
                        and not any(part in files.RESERVED_DIR_NAMES for part in d.relative_to(space_dir).parts)
                    ))
                result.append(SpaceInfo(
                    name=name, item_count=counts.get(name, 0), members=members, folders=folders,
                ))
            return result

    def ensure_folder(self, space: str, folder: str) -> str:
        """Legt einen leeren Ordner an (Step 7 Commit 3, K4) — reine Verzeichnisoperation, kein
        Content-Write: kein Git-Commit, kein eigener Index-Eintrag nötig, `list_spaces()`s
        `rglob`-Walk findet ein `mkdir`'tes Verzeichnis genauso wie eines, das durch ein Item
        entstanden ist. Idempotent (`exist_ok=True`) — ein bereits vorhandener Ordner ist kein
        Fehler, derselbe Nutzer könnte sonst durch einen Doppelklick eine Fehlermeldung sehen,
        obwohl am Ergebnis nichts falsch ist.
        """
        with self._lock:
            folder = files.validate_folder(folder)
            if not folder:
                raise ValidationError("Ordnername darf nicht leer sein")
            (self._data_root / space / folder).mkdir(parents=True, exist_ok=True)
            return folder

    @property
    def acl_reader(self) -> AclReader:
        """Der eine `AclReader`, den dieser `Store` selbst benutzt (P6 Step 5) — Aufrufer, die
        eine `AclDecision` außerhalb von `acl_of()` bauen müssen (z. B. `mcpserver.tools
        .search_items` für eine ganze Seite `ItemSummary`-Zeilen), teilen sich damit denselben
        `stat()`-invalidierten Cache statt einen zweiten, unabhängig veraltenden `AclReader`
        zu instanziieren."""
        return self._acl

    def acl_of(self, item_id: str) -> AclDecision:
        """Rechte eines Items, ausschließlich aus dem Index — liest die Item-DATEI NICHT
        (gleiche Eigenschaft wie `space_of()`, P2: sicher aufrufbar, BEVOR feststeht, ob der
        Zugriff überhaupt erlaubt ist).
        """
        with self._lock:
            row = index.get_item_row(self._conn, item_id)
        if row is None:
            raise ItemNotFound(item_id)
        space = row["space"]
        # Wie in `_row_to_item()`: aus dem Pfad abgeleitet, nicht aus `row["folder"]`
        # übernommen — reine Pfad-Arithmetik, kein Datei-Lesezugriff, verletzt also nicht den
        # "liest die Item-DATEI NICHT"-Vertrag oben.
        folder = files.folder_from_path(self._data_root, space, self._data_root / row["path"])
        return self._acl.decision_for(
            space=space, folder=folder, visibility=row["visibility"],
            share_read=json.loads(row["share_read_json"]),
            share_write=json.loads(row["share_write_json"]),
        )

    def space_of(self, item_id: str) -> str:
        """Space eines Items, ausschließlich über den Index. Schreibt nichts, liest keine Datei.
        Wird von der Autorisierungsschicht (P2) gebraucht, BEVOR entschieden ist, ob ein
        Zugriff überhaupt erlaubt ist — ein Rechtefehler darf den Store sonst nicht erreichen.
        """
        with self._lock:
            row = index.get_item_row(self._conn, item_id)
        if row is None:
            raise ItemNotFound(item_id)
        return row["space"]

    def search(
        self,
        query: str | None = None,
        *,
        space: str | None = None,
        spaces: list[str] | None = None,
        folder: str | None = None,
        type: str | None = None,
        status: str | None = None,
        tag: str | None = None,
        due_before: date | None = None,
        limit: int = 50,
        offset: int = 0,
        in_body: bool = False,
    ) -> SearchResult:
        with self._lock:
            rows = index.all_rows(self._conn)

        items = [self._row_to_item(r) for r in rows]

        def matches(item: Item) -> bool:
            if space is not None and item.space != space:
                return False
            if spaces is not None and item.space not in spaces:
                return False
            if folder is not None and item.folder != folder:
                return False
            if type is not None and item.type != type:
                return False
            if status is not None and item.status != status:
                return False
            if tag is not None and tag not in item.tags:
                return False
            if due_before is not None and (item.due is None or item.due >= due_before):
                return False
            if query:
                # P6.5-N4: Body nur bei explizitem in_body=True — item.body ist über
                # _row_to_item() ohnehin schon geladen, kein zusätzlicher Datei-Zugriff.
                haystack = f"{item.title} {' '.join(item.tags)}"
                if in_body:
                    haystack += " " + item.body
                if query.lower() not in haystack.lower():
                    return False
            return True

        filtered = [i for i in items if matches(i)]
        filtered.sort(
            key=lambda i: (
                i.status != "open" and i.status != "active",
                i.due or date.max,
                -(i.updated.timestamp()),
            )
        )
        total = len(filtered)
        page = filtered[offset : offset + limit]
        return SearchResult(
            items=[_summary(i) for i in page], total=total, limit=limit, offset=offset,
        )

    def get(self, item_id: str, *, repair_drift: bool = True) -> Item:
        with self._lock, self._file_write_lock():
            row = self._reconcile_and_get_row(item_id, repair_drift=repair_drift)
            return self._row_to_item(row)

    def create(
        self, space: str, *, type: str, title: str, body: str = "", folder: str = "", **fields
    ) -> Item:
        with self._lock, self._file_write_lock():
            reserved = _SYSTEM_MANAGED_FIELDS & fields.keys()
            if reserved:
                raise ValidationError(f"Felder {sorted(reserved)} sind vom Store verwaltet")
            folder = files.validate_folder(folder)
            now = self._now_fn()
            status = fields.pop("status", _DEFAULT_STATUS.get(type, "active"))
            _check_type_and_status(type, status)
            due = _coerce_due(fields.pop("due", None))
            tags = fields.pop("tags", [])
            links = fields.pop("links", [])
            visibility = fields.pop("visibility", DEFAULT_VISIBILITY)
            if visibility not in VISIBILITY_VALUES:
                raise ValidationError(
                    f"Unbekannte visibility {visibility!r} — erlaubt: {sorted(VISIBILITY_VALUES)}"
                )
            share_read = fields.pop("share_read", [])
            share_write = fields.pop("share_write", [])
            item = Item(
                id=files.generate_id(), space=space, type=type, title=title, status=status,
                body=body, due=due, tags=list(tags), links=list(links),
                created=now, updated=now, version=1, folder=folder,
                visibility=visibility, share_read=list(share_read), share_write=list(share_write),
                extra=fields,
            )
            self._write_item_file(item, old_path=None, op="create")
            return item

    def update(self, item_id: str, *, version: int, **changes) -> Item:
        with self._lock, self._file_write_lock():
            row = self._reconcile_and_get_row(item_id)
            current = self._row_to_item(row)
            if current.version != version:
                raise ConflictError(item_id, expected_version=version, current=current)
            if current.status == "archived":
                raise ValidationError(f"Item {item_id} ist archiviert — update verboten")

            old_path = self._data_root / row["path"]
            updated_extra = dict(current.extra)
            known_updatable = {"type", "title", "status", "body", "due", "tags", "links"}
            kwargs: dict[str, Any] = {}
            for key, value in changes.items():
                if key in _SYSTEM_MANAGED_FIELDS:
                    raise ValidationError(f"Feld '{key}' ist vom Store verwaltet, nicht änderbar")
                if key == "due":
                    kwargs["due"] = _coerce_due(value)
                elif key == "folder":
                    # `Store.update()` erlaubt das Setzen -- die Sperre für Agenten
                    # (visibility/share_read/share_write) sitzt eine Schicht höher in
                    # `mcpserver.tools.update_item` (P6-M), nicht hier (`folder` selbst ist
                    # nicht gesperrt, Agenten dürfen Items in Ordner verschieben).
                    kwargs["folder"] = files.validate_folder(value)
                elif key == "visibility":
                    if value not in VISIBILITY_VALUES:
                        raise ValidationError(
                            f"Unbekannte visibility {value!r} — erlaubt: {sorted(VISIBILITY_VALUES)}"
                        )
                    kwargs["visibility"] = value
                elif key in ("share_read", "share_write"):
                    kwargs[key] = list(value)
                elif key in known_updatable:
                    kwargs[key] = value
                else:
                    updated_extra[key] = value

            _check_type_and_status(
                kwargs.get("type", current.type), kwargs.get("status", current.status)
            )

            new_item = replace(
                current,
                **kwargs,
                extra=updated_extra,
                version=current.version + 1,
                updated=self._now_fn(),
            )
            self._write_item_file(new_item, old_path=old_path, op="update")
            return new_item

    def append(self, item_id: str, *, version: int, text: str) -> Item:
        with self._lock, self._file_write_lock():
            row = self._reconcile_and_get_row(item_id)
            current = self._row_to_item(row)
            if current.version != version:
                raise ConflictError(item_id, expected_version=version, current=current)
            if current.status == "archived":
                raise ValidationError(f"Item {item_id} ist archiviert — append verboten")

            old_path = self._data_root / row["path"]
            separator = "\n" if current.body and not current.body.endswith("\n") else ""
            new_item = replace(
                current,
                body=current.body + separator + text,
                version=current.version + 1,
                updated=self._now_fn(),
            )
            self._write_item_file(new_item, old_path=old_path, op="append")
            return new_item

    def patch(self, item_id: str, *, version: int, edits: Sequence[TextEdit]) -> PatchResult:
        """Ersetzt exakte Textstellen im Body, ohne ihn komplett neu zu schreiben (P6-E).
        Reihenfolge wie `update`/`append`, mit einem zusätzlichen Schritt: `apply_edits()`
        läuft auf einer Kopie des Bodys, **bevor** irgendetwas geschrieben wird — ein
        `PatchError` (Treffer ≠ 1) verlässt diese Methode, ohne dass Datei, Index oder Version
        angefasst wurden.
        """
        with self._lock, self._file_write_lock():
            row = self._reconcile_and_get_row(item_id)
            current = self._row_to_item(row)
            if current.version != version:
                raise ConflictError(item_id, expected_version=version, current=current)
            if current.status == "archived":
                raise ValidationError(f"Item {item_id} ist archiviert — patch verboten")

            old_path = self._data_root / row["path"]
            bytes_before = len(current.body.encode("utf-8"))
            new_body, lines = apply_edits(current.body, edits)
            bytes_after = len(new_body.encode("utf-8"))

            new_item = replace(
                current, body=new_body, version=current.version + 1, updated=self._now_fn(),
            )
            self._write_item_file(new_item, old_path=old_path, op="patch")
            return PatchResult(
                item=new_item, replacements=len(edits), lines=lines,
                bytes_before=bytes_before, bytes_after=bytes_after,
            )

    def archive(self, item_id: str, *, version: int) -> Item:
        with self._lock, self._file_write_lock():
            row = self._reconcile_and_get_row(item_id)
            current = self._row_to_item(row)
            if current.version != version:
                raise ConflictError(item_id, expected_version=version, current=current)

            old_path = self._data_root / row["path"]
            new_item = replace(
                current, status="archived", folder="",
                version=current.version + 1, updated=self._now_fn(),
            )
            slug = files.slugify(new_item.title)
            archive_path = (
                self._data_root / new_item.space / "_archive" / files.item_filename(new_item.id, slug)
            )
            files.atomic_write(old_path, _item_to_text(new_item))
            files.move_file(old_path, archive_path)
            row2 = index.row_from_file(self._data_root, archive_path)
            index.upsert_item(self._conn, row2)
            self._commit("archive", new_item.id, new_item.space)
            return new_item

    def move(
        self, item_id: str, *, version: int, space: str | None = None, folder: str | None = None
    ) -> Item:
        """Verschiebt ein Item in einen anderen Space und/oder Ordner (P6-AD,
        `phase6_shares/ITEM_MOVE_PLAN.md` §4.1). Eigene Methode statt eines `space=`-Feldes an
        `update()` — `space` bleibt in `_SYSTEM_MANAGED_FIELDS`, derselbe Schutz, der den
        Divergenz-Fund B2 der P2-Adapter-Abnahme (Verzeichnis sagt `niklas`, Frontmatter sagt
        `nikinger`) verhindert. Genau ein Git-Commit (`move <id> [<ziel-space>]` über
        `_write_item_file()`s bestehenden `_commit()`-Aufruf), genau ein Versionssprung.
        Autorisierung passiert NICHT hier (wie überall im Store) — Aufrufer prüfen Rechte VOR
        diesem Call (P6-AE: Schreibrecht auf Quelle UND Ziel).
        """
        with self._lock, self._file_write_lock():
            row = self._reconcile_and_get_row(item_id)
            current = self._row_to_item(row)
            if current.version != version:
                raise ConflictError(item_id, expected_version=version, current=current)
            if current.status == "archived":
                raise ValidationError(f"Item {item_id} ist archiviert — move verboten")

            old_path = self._data_root / row["path"]
            target_space = current.space
            if space is not None:
                # Explizite Prüfung statt `_write_item_file()`s `mkdir(parents=True)` beiläufig
                # entscheiden zu lassen — sonst macht ein Tippfehler im Zielnamen aus Versehen
                # einen neuen, rechtefreien Space (§4.1 Punkt 2).
                if not (self._data_root / space).is_dir():
                    raise ValidationError(
                        f"Ziel-Space {space!r} existiert nicht — move legt keinen neuen Space an"
                    )
                target_space = space

            if folder is not None:
                target_folder = files.validate_folder(folder)
            elif space is not None:
                # Space-Wechsel ohne folder=: Ziel ist die Space-Wurzel, NICHT der gleichnamige
                # Ordner im Zielspace — ein Ordnername bedeutet dort etwas anderes und trägt
                # potenziell eine andere `.share.yml` (§4.1 Punkt 3).
                target_folder = ""
            else:
                target_folder = current.folder

            new_item = replace(
                current, space=target_space, folder=target_folder,
                version=current.version + 1, updated=self._now_fn(),
            )
            # P6.5-T: das Asset-Verzeichnis zieht mit, BEVOR `_write_item_file()` committet —
            # ein Move erzeugt weiterhin genau einen Git-Commit (P6-Abnahmezeile 26s Mechanik).
            files.move_asset_dir(
                files.asset_dir(self._data_root, current.space, current.id),
                files.asset_dir(self._data_root, target_space, current.id),
            )
            self._write_item_file(new_item, old_path=old_path, op="move")
            self._cleanup_emptied_folders(old_path.parent, current.space)
            return new_item

    def _cleanup_emptied_folders(self, folder_dir: Path, space: str) -> None:
        """P6-AF: nach einem Move leer gewordene Quellordner aufräumen, aufwärts bis maximal zur
        Space-Wurzel. Abbruch bei einer `.share.yml` (eine bewusste Freigabe eines Menschen ist
        kein Rest — sie wegzuräumen würde eine Rechteeinstellung als Nebenwirkung eines Moves
        löschen) oder einem nicht-leeren Verzeichnis. Reine Aufräum-Nebenwirkung ohne eigenen
        Git-Commit, dieselbe Kategorie wie `ensure_folder()`.
        """
        space_root = self._data_root / space
        current = folder_dir
        while space_root in current.parents:
            if (current / ACL_FILENAME).exists():
                break
            try:
                if any(current.iterdir()):
                    break
                current.rmdir()
            except OSError:
                break
            current = current.parent

    def put_asset(
        self, item_id: str, *, data: bytes, filename: str | None = None
    ) -> AssetInfo:
        """Legt ein Bild unter `<space>/_assets/<item_id>/` ab (P6.5-T, fünfte Contract-
        Öffnung). Kein `version`-Parameter — Assets sind nicht Teil der Item-Versionierung,
        ein Upload konkurriert nie mit einem Text-Write um dieselbe `version`."""
        with self._lock, self._file_write_lock():
            row = self._reconcile_and_get_row(item_id, repair_drift=False)
            space = row["space"]
            sniffed = files.sniff_image_mime(data)
            if sniffed is None:
                raise ValidationError(
                    "Unbekanntes oder nicht unterstütztes Bildformat — erlaubt: "
                    "PNG/JPEG/GIF/WebP"
                )
            mime, ext = sniffed
            asset_id = files.new_asset_id()
            target_dir = files.asset_dir(self._data_root, space, item_id)
            target_dir.mkdir(parents=True, exist_ok=True)
            path = files.asset_path(self._data_root, space, item_id, asset_id, ext)
            files.atomic_write_bytes(path, data)
            self._commit("asset", item_id, space)
            # `created` kommt aus der Datei-mtime, nicht aus `self._now_fn()` — nichts
            # persistiert den Upload-Zeitpunkt separat, also muss put_asset() dieselbe Quelle
            # liefern, die list_assets() beim nächsten Listing sieht (Advisor-Fund, sonst
            # zeigen dieselbe Asset zwei verschiedene `created`-Werte).
            created = datetime.fromtimestamp(path.stat().st_mtime, tz=timezone.utc)
            return AssetInfo(
                id=asset_id, mime=mime, bytes=len(data),
                filename=filename or "", created=created,
            )

    def list_assets(self, item_id: str) -> list[AssetInfo]:
        """Kein Index-Eintrag für Assets (P6-AY) — direktes Verzeichnis-Listing.
        `_trash/` wird übersprungen (verschobene, „entfernte" Assets, N5)."""
        with self._lock, self._file_write_lock():
            row = self._reconcile_and_get_row(item_id, repair_drift=False)
            target_dir = files.asset_dir(self._data_root, row["space"], item_id)
            if not target_dir.is_dir():
                return []
            result = []
            for path in sorted(target_dir.iterdir()):
                if path.name == "_trash" or not path.is_file():
                    continue
                asset_id = path.stem
                if not files.ASSET_ID_RE.match(asset_id):
                    continue
                # Nur die für sniff_image_mime() nötigen ersten 12 Bytes lesen (WebPs
                # Offset-8-Prüfung ist der längste Fall) — ein Listing darf nicht jedes Bild
                # vollständig einlesen, das widerspräche get_item_metas eigenem Versprechen
                # "um Größenordnungen billiger" (Advisor-Fund).
                with path.open("rb") as f:
                    sniffed = files.sniff_image_mime(f.read(12))
                mime = sniffed[0] if sniffed is not None else ""
                stat = path.stat()
                result.append(AssetInfo(
                    id=asset_id, mime=mime, bytes=stat.st_size, filename="",
                    created=datetime.fromtimestamp(stat.st_mtime, tz=timezone.utc),
                ))
            return result

    def get_asset(self, item_id: str, asset_id: str) -> tuple[bytes, str]:
        """Bytes + MIME — die MIME kommt erneut aus den Magic Bytes, nicht aus der
        Dateiendung (dieselbe Nie-der-Endung-vertrauen-Regel wie beim Upload)."""
        with self._lock, self._file_write_lock():
            row = self._reconcile_and_get_row(item_id, repair_drift=False)
            target_dir = files.asset_dir(self._data_root, row["space"], item_id)
            matches = list(target_dir.glob(f"{asset_id}.*")) if target_dir.is_dir() else []
            if not matches:
                raise ItemNotFound(asset_id)
            data = matches[0].read_bytes()
            sniffed = files.sniff_image_mime(data)
            mime = sniffed[0] if sniffed is not None else "application/octet-stream"
            return data, mime

    def delete_asset(self, item_id: str, asset_id: str) -> None:
        """„Verschieben statt Entfernen" (N5, gelockt): das Bild landet in `_trash/`,
        Entscheidung H (kein Hard-Delete im Kern-API) bleibt formal unangetastet. Die
        Body-Referenz läuft danach ins Leere und rendert als Alt-Text — kein Rewrite des
        Bodys hier, das ist Aufgabe der aufrufenden Schicht, falls gewünscht."""
        with self._lock, self._file_write_lock():
            row = self._reconcile_and_get_row(item_id, repair_drift=False)
            space = row["space"]
            target_dir = files.asset_dir(self._data_root, space, item_id)
            matches = list(target_dir.glob(f"{asset_id}.*")) if target_dir.is_dir() else []
            if not matches:
                raise ItemNotFound(asset_id)
            trash_dir = target_dir / "_trash"
            trash_dir.mkdir(parents=True, exist_ok=True)
            files.move_file(matches[0], trash_dir / matches[0].name)
            self._commit("asset_trash", item_id, space)

    def rebuild_index(self) -> IndexStats:
        with self._lock:
            return index.rebuild_index(self._data_root, self._conn)
