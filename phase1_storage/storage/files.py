"""Dateipfade, IDs und atomare Writes. Kennt keine Frontmatter/YAML — bekommt fertigen
Dateitext von der aufrufenden Schicht (`store.py`, ab Step 4) und schreibt ihn nur sicher weg.
"""
from __future__ import annotations

import os
import re
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


ASSET_ID_PREFIX = "ast_"
ITEM_ID_RE = re.compile(r"^itm_[0-9a-f]{8}$")
ASSET_ID_RE = re.compile(r"^ast_[0-9a-f]{8}$")


def new_asset_id() -> str:
    """Zwilling zu `generate_id()` (P6.5-R) — gleiches Format, eigener Namensraum
    (`ast_` statt `itm_`), damit eine Asset-ID nie mit einer Item-ID verwechselbar ist."""
    return ASSET_ID_PREFIX + secrets.token_hex(4)


# (Magic-Präfix, MIME, Dateiendung) — Reihenfolge ist Prüfreihenfolge. WebP braucht zwei
# Prüfungen (RIFF-Header UND "WEBP" bei Offset 8), deshalb kein Eintrag hier — siehe
# `sniff_image_mime()`. SVG/HEIC/PDF bewusst nicht dabei (P6-AZ): SVG ist ausführbares
# Markup (XSS/XXE-Fläche), die anderen beiden haben keinen genannten Anwendungsfall.
ASSET_MIME_TYPES: tuple[tuple[bytes, str, str], ...] = (
    (b"\x89PNG\r\n\x1a\n", "image/png", "png"),
    (b"\xff\xd8\xff", "image/jpeg", "jpg"),
    (b"GIF87a", "image/gif", "gif"),
    (b"GIF89a", "image/gif", "gif"),
)


def sniff_image_mime(data: bytes) -> tuple[str, str] | None:
    """Erkennt PNG/JPEG/GIF/WebP an den Magic Bytes, nie an einer angegebenen Endung —
    ein Client-seitiger Dateiname ist keine vertrauenswürdige Typangabe. `None` bei jedem
    unbekannten Format (P6-AZ: SVG/HEIC/PDF absichtlich nicht erkannt)."""
    for prefix, mime, ext in ASSET_MIME_TYPES:
        if data.startswith(prefix):
            return mime, ext
    # WebP: RIFF-Container, "WEBP" erst bei Offset 8 -- ein reiner Präfix-Check auf "RIFF"
    # würde auch andere RIFF-Formate (z.B. WAV/AVI) fälschlich als Bild durchlassen.
    if data[:4] == b"RIFF" and data[8:12] == b"WEBP":
        return "image/webp", "webp"
    return None


def asset_dir(data_root: Path, space: str, item_id: str) -> Path:
    if not ITEM_ID_RE.match(item_id):
        raise ValidationError(f"Ungültige item_id: {item_id!r}")
    return data_root / space / "_assets" / item_id


def asset_path(data_root: Path, space: str, item_id: str, asset_id: str, ext: str) -> Path:
    if not ASSET_ID_RE.match(asset_id):
        raise ValidationError(f"Ungültige asset_id: {asset_id!r}")
    return asset_dir(data_root, space, item_id) / f"{asset_id}.{ext}"


def move_asset_dir(src_dir: Path, dst_dir: Path) -> None:
    """No-op, wenn `src_dir` nicht existiert (Normalfall: die meisten Items haben keine
    Bilder) — sonst atomarer Verzeichnis-Move mit `fsync` auf beiden Elternverzeichnissen,
    dasselbe Muster wie `move_file()`. Ein bereits nicht-leer existierendes `dst_dir`
    propagiert `OSError(ENOTEMPTY)` unverändert (P6.5-S) — kein stilles Zusammenführen zweier
    Asset-Verzeichnisse."""
    if src_dir == dst_dir or not src_dir.exists():
        return
    dst_dir.parent.mkdir(parents=True, exist_ok=True)
    os.replace(src_dir, dst_dir)
    for directory in {src_dir.parent, dst_dir.parent}:
        dir_fd = os.open(directory, os.O_RDONLY)
        try:
            os.fsync(dir_fd)
        finally:
            os.close(dir_fd)


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


def atomic_write_bytes(path: Path, content: bytes) -> None:
    """Binäres Gegenstück zu `atomic_write()` — eigene Funktion statt eines `bytes|str`-Zweigs
    dort, damit die Textvariante ihre `encoding`-Semantik unangetastet behält. Gleiche
    tmp+fsync+`os.replace`+Verzeichnis-fsync-Mechanik."""
    directory = path.parent
    fd, tmp_name = tempfile.mkstemp(dir=directory, prefix=f".{path.name}.", suffix=".tmp")
    try:
        with os.fdopen(fd, "wb") as f:
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
