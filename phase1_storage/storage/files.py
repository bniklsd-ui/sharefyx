"""Dateipfade, IDs und atomare Writes. Kennt keine Frontmatter/YAML — bekommt fertigen
Dateitext von der aufrufenden Schicht (`store.py`, ab Step 4) und schreibt ihn nur sicher weg.
"""
from __future__ import annotations

import os
import secrets
import tempfile
from pathlib import Path

from .errors import ValidationError

# P6 Step 4 (Plan §1.2.3/§1.3): `_archive`/`_assets` sind reservierte Space-Unterverzeichnisse,
# nie ein Ordner, den ein Item wählen kann. Bewusst hier statt in `acl.py` definiert (wie im
# Plan-Snippet vorgeschlagen) — Ordnerpfad-Validierung ist bereits `files.py`s Job
# (`item_path`/`slugify` leben schon hier); `acl.py` importiert die Konstante von hier.
RESERVED_DIR_NAMES = frozenset({"_archive", "_assets"})
MAX_FOLDER_DEPTH = 2

_UMLAUT_MAP = str.maketrans(
    {
        "ä": "ae",
        "ö": "oe",
        "ü": "ue",
        "Ä": "Ae",
        "Ö": "Oe",
        "Ü": "Ue",
        "ß": "ss",
    }
)


def generate_id() -> str:
    """`itm_` + 8 Hex-Zeichen (Entscheidung F). Unveränderlich über die Lebenszeit des Items."""
    return "itm_" + secrets.token_hex(4)


def slugify(title: str) -> str:
    """Dateiname-taugliche Kurzform des Titels. Deutsche Umlaute korrekt transliteriert."""
    text = title.translate(_UMLAUT_MAP).lower()
    chars = [c if c.isalnum() else "-" for c in text]
    slug = "".join(chars)
    while "--" in slug:
        slug = slug.replace("--", "-")
    slug = slug.strip("-")
    return slug or "item"


def item_filename(item_id: str, slug: str) -> str:
    """`<id>__<slug>.md` (Entscheidung F). Lookup läuft nie über diesen Namen, nur über die ID."""
    return f"{item_id}__{slug}.md"


def item_path(data_root: Path, space: str, item_id: str, slug: str, folder: str = "") -> Path:
    if folder:
        return data_root / space / folder / item_filename(item_id, slug)
    return data_root / space / item_filename(item_id, slug)


def validate_folder(folder: str) -> str:
    """Normalisiert/validiert einen Ordnerpfad (P6-Q): jedes Segment wird wie ein Titel
    slugifiziert, Tiefe <= `MAX_FOLDER_DEPTH`, kein Segment aus `RESERVED_DIR_NAMES`. Leerer
    String bleibt leer (kein Ordner) — das ist der Default und immer gültig.

    Der Reserviert-Check läuft VOR dem Slugifizieren, auf dem rohen (nur lowercased) Segment:
    `slugify("_archive")` strippt das führende `_` (kein `isalnum()`-Zeichen) und würde sonst
    unbemerkt zu `"archive"` — einem eigenen, nicht reservierten Namen — werden. Ein Aufrufer,
    der `_archive` als Ordner meint, bekommt so einen klaren Fehler statt einer stillen
    Umbenennung.
    """
    if not folder:
        return ""
    segments = [s for s in folder.split("/") if s]
    if len(segments) > MAX_FOLDER_DEPTH:
        raise ValidationError(
            f"Ordner {folder!r} ist zu tief verschachtelt (max. {MAX_FOLDER_DEPTH} Ebenen)"
        )
    for raw in segments:
        if raw.lower() in RESERVED_DIR_NAMES:
            raise ValidationError(f"Ordnername {raw!r} ist reserviert")
    normalized = [slugify(s) for s in segments]
    for raw, seg in zip(segments, normalized):
        if not seg:
            raise ValidationError(f"Ordnersegment {raw!r} ergibt keinen gültigen Namen")
    return "/".join(normalized)


def folder_from_path(data_root: Path, space: str, path: Path) -> str:
    """Kehrt `item_path`s Ordnerplatzierung um — `folder` ist immer abgeleitet, nie
    Frontmatter (Plan §1.3). Archivierte Items (`_archive/...`) gelten nie als "in einem
    Ordner" (P6-R, Archiv bleibt flach), auch wenn `_archive` selbst ein Verzeichnis ist.
    """
    parts = path.relative_to(data_root / space).parts[:-1]
    if parts and parts[0] in RESERVED_DIR_NAMES:
        return ""
    return "/".join(parts)


def atomic_write(path: Path, content: str, *, encoding: str = "utf-8") -> None:
    """tmp-Datei im selben Verzeichnis -> fsync -> `os.replace` -> Verzeichnis-fsync.

    `os.replace` ist auf demselben Dateisystem eine atomare Rename-Syscall — es kann keine
    halb geschriebene Zieldatei entstehen, auch nicht bei einem Absturz mittendrin. Der einzige
    Fall, der aufräumt, ist ein regulärer Python-Exception-Pfad (z. B. Platte voll); ein echtes
    `kill -9` hinterlässt bestenfalls eine verwaiste tmp-Datei, nie eine korrupte Zieldatei.
    """
    directory = path.parent
    fd, tmp_name = tempfile.mkstemp(dir=directory, prefix=f".{path.name}.", suffix=".tmp")
    try:
        with os.fdopen(fd, "w", encoding=encoding) as f:
            f.write(content)
            f.flush()
            os.fsync(f.fileno())
        os.replace(tmp_name, path)
    except BaseException:
        try:
            os.unlink(tmp_name)
        except FileNotFoundError:
            pass
        raise
    else:
        dir_fd = os.open(directory, os.O_RDONLY)
        try:
            os.fsync(dir_fd)
        finally:
            os.close(dir_fd)


def move_file(old_path: Path, new_path: Path) -> None:
    """Atomarer Move (auch über Verzeichnisse hinweg, z. B. nach `_archive/`), mit
    Verzeichnis-fsync auf Quelle und Ziel. No-op wenn `old_path == new_path`.
    """
    if old_path == new_path:
        return
    new_path.parent.mkdir(parents=True, exist_ok=True)
    os.replace(old_path, new_path)
    for directory in {old_path.parent, new_path.parent}:
        dir_fd = os.open(directory, os.O_RDONLY)
        try:
            os.fsync(dir_fd)
        finally:
            os.close(dir_fd)
