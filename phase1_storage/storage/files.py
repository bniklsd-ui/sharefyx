"""Dateipfade, IDs und atomare Writes. Kennt keine Frontmatter/YAML — bekommt fertigen
Dateitext von der aufrufenden Schicht (`store.py`, ab Step 4) und schreibt ihn nur sicher weg.
"""
from __future__ import annotations

import os
import secrets
import tempfile
from pathlib import Path

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


def item_path(data_root: Path, space: str, item_id: str, slug: str) -> Path:
    return data_root / space / item_filename(item_id, slug)


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


def rename_for_new_slug(old_path: Path, item_id: str, new_slug: str) -> Path:
    """Benennt die Datei bei Titeländerung um. Die ID im Namen bleibt, nur der Slug wechselt."""
    new_path = old_path.parent / item_filename(item_id, new_slug)
    move_file(old_path, new_path)
    return new_path
