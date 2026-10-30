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
ASSET_ID_RE = re.compile(r"^ast_[0-9a-f]{8}\Z")


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


# -- P10.5, Block 3 (LG-8, P1-Öffnung 15): EXIF-Bereinigung ---------------------------------
#
# **Reine Byte-Chirurgie, keine neue Abhängigkeit.** Der Kern bleibt abhängigkeitsfrei (kein
# Pillow, kein piexif): der Server soll keine Bilder „verstehen", er soll sie von Metadaten
# befreien. Alles hier ist formatweise Marker-/Chunk-Arbeit, nach JPEG-Spezifikation gelesen.
#
# **Was fliegt raus:** Exif (GPS, Kameratyp, Zeitstempel), XMP, IPTC/Photoshop-Kommentare,
# PNG-Textfelder (`tEXt`/`iTXt`/`zTXt`), PNG-Zeitstempel (`tIME`) und WebP-`EXIF`/`XMP `.
# **Was bleibt:** alles, was das Bild selbst ist — und bei JPEG das ICC-Profil (`APP2`, sonst
# werden Farben falsch), JFIF (`APP0`) und Adobe (`APP14`, nötig für CMYK).
#
# **Fail-closed:** eine Struktur, die der Parser nicht vollständig versteht, ergibt
# `ValidationError` — nie wird ein halbbereinigtes Bild gespeichert (Geist von Hard Rule 5).

_EXIF_APP1_PREFIX = b"Exif\x00\x00"
_XMP_APP1_PREFIX = b"http://ns.adobe.com/xap/1.0/\x00"
_EXIF_ORIENTATION_TAG = 0x0112
_PNG_SIGNATURE = b"\x89PNG\r\n\x1a\n"
_PNG_DROP_CHUNKS = frozenset({b"eXIf", b"tEXt", b"iTXt", b"zTXt", b"tIME"})
# WebP-`VP8X`-Flagbits (Herstellerspezifikation): ICC 0x20, Alpha 0x10, EXIF 0x08, XMP 0x04,
# Animation 0x02. Wird ein Chunk entfernt, muss sein Bit mit verschwinden, sonst behauptet die
# Datei, sie hätte noch Metadaten, die sie nicht mehr hat.
_WEBP_FLAG_EXIF = 0x08
_WEBP_FLAG_XMP = 0x04

_STRIP_FAILED = "Bild konnte nicht bereinigt werden"


def strip_image_metadata(data: bytes, mime: str) -> bytes:
    """Entfernt die Metadaten aus einem Bild — **ohne** es anzufassen (LG-8, P1-Öffnung 15).

    `mime` ist der per Magic Bytes erkannte Typ (`sniff_image_mime()`), **nicht** eine Angabe
    des Clients: die Erkennung entscheidet, was passiert, und die Funktion prüft selbst nach,
    dass die Bytes zum behaupteten Format passen (fail-closed).

    * **JPEG:** `APP1` (Exif **und** XMP), `APP13` (IPTC/Photoshop) und `COM` fallen weg;
      `APP0` (JFIF), `APP2` (ICC) und `APP14` (Adobe) bleiben. Trägt das Original eine
      `Orientation` ≠ 1 (Tag `0x0112` in IFD0), wird ein **minimales** `APP1` mit genau diesem
      Tag neu geschrieben — sonst stünden Handyfotos nach dem Hochladen quer. Ab `SOS` wird
      alles byte-genau kopiert.
    * **PNG:** die Chunks `eXIf`, `tEXt`, `iTXt`, `zTXt` und `tIME` fallen weg, alle anderen
      bleiben in Reihenfolge (ihre CRC bleibt gültig, denn ihre Bytes ändern sich nicht).
    * **WebP (RIFF):** die Chunks `EXIF` und `XMP ` fallen weg, die zugehörigen Flag-Bits in
      `VP8X` werden gelöscht, die RIFF-Größe wird neu gesetzt.
    * **GIF:** unverändert — GIF kennt kein Exif (nur einen Kommentar-Block, der hier nicht
      geparst wird).

    **Ein Bild ohne Metadaten bleibt byte-identisch** (derselbe Byte-Strom, keine Neu-Kodierung).
    """
    if mime == "image/gif":
        _require_magic(data, (b"GIF87a", b"GIF89a"), mime)
        return data
    if mime == "image/jpeg":
        return _strip_jpeg(data)
    if mime == "image/png":
        return _strip_png(data)
    if mime == "image/webp":
        return _strip_webp(data)
    raise ValidationError(f"{_STRIP_FAILED}: unbekanntes Format {mime!r}")


def _require_magic(data: bytes, prefixes: tuple[bytes, ...], mime: str) -> None:
    if not any(data.startswith(prefix) for prefix in prefixes):
        raise ValidationError(f"{_STRIP_FAILED}: die Bytes passen nicht zu {mime}")


def _strip_jpeg(data: bytes) -> bytes:
    """Marker-Folge bis `SOS` durchgehen, Metadaten-Segmente fallen lassen, ab `SOS` verbatim
    kopieren. Siehe `strip_image_metadata()` für die Regel im Klartext."""
    if not data.startswith(b"\xff\xd8"):
        raise ValidationError(f"{_STRIP_FAILED}: kein JPEG (SOI fehlt)")
    out = bytearray(b"\xff\xd8")
    pos = 2
    size = len(data)
    while pos < size:
        if data[pos] != 0xFF:
            raise ValidationError(f"{_STRIP_FAILED}: JPEG ohne Marker bei Byte {pos}")
        marker_start = pos
        while pos < size and data[pos] == 0xFF:
            pos += 1
        if pos >= size:
            raise ValidationError(f"{_STRIP_FAILED}: JPEG am Ende abgeschnitten")
        marker = data[pos]
        pos += 1
        if marker in (0xDA, 0xD9):  # SOS / EOI: ab hier ist der Bildinhalt
            out += data[marker_start:]
            return bytes(out)
        if marker == 0x01 or 0xD0 <= marker <= 0xD7:  # TEM / RSTn: ohne Nutzlast
            out += data[marker_start:pos]
            continue
        if pos + 2 > size:
            raise ValidationError(f"{_STRIP_FAILED}: JPEG-Segment abgeschnitten")
        length = int.from_bytes(data[pos:pos + 2], "big")
        if length < 2 or pos + length > size:
            raise ValidationError(f"{_STRIP_FAILED}: JPEG-Segmentlänge passt nicht")
        segment_end = pos + length
        payload = data[pos + 2:segment_end]
        pos = segment_end
        if marker == 0xE1:  # APP1 — Exif oder XMP
            if payload.startswith(_XMP_APP1_PREFIX):
                continue  # XMP fliegt raus
            if payload.startswith(_EXIF_APP1_PREFIX):
                orientation = _exif_orientation(payload)
                if orientation is not None and orientation != 1:
                    out += _minimal_exif_app1(orientation)
                continue  # das Original-APP1 fliegt in jedem Fall raus
            continue  # unbekanntes APP1: Metadaten, fliegt raus
        if marker in (0xED, 0xFE):  # APP13 (IPTC/Photoshop), COM (Kommentar)
            continue
        out += data[marker_start:segment_end]
    raise ValidationError(f"{_STRIP_FAILED}: JPEG ohne SOS (abgeschnitten)")


def _exif_orientation(payload: bytes) -> int | None:
    """Liest die `Orientation` (Tag `0x0112`) aus dem IFD0 eines Exif-Blocks.

    `payload` ist der **Inhalt** eines `APP1`-Segments, beginnend mit `Exif\\0\\0`. Gibt `None`
    zurück, wenn der Block keine Orientation trägt. **Alles andere** (unbekannte
    Byte-Reihenfolge, kaputter TIFF-Header, Orientation außerhalb 1–8) ist ein `ValidationError`:
    wer die Orientierung nicht sicher lesen kann, darf das Bild nicht halbbereinigt speichern.
    """
    tiff = payload[len(_EXIF_APP1_PREFIX):]
    if len(tiff) < 8:
        raise ValidationError(f"{_STRIP_FAILED}: Exif-Block zu kurz")
    if tiff[:2] == b"II":
        endian = "little"
    elif tiff[:2] == b"MM":
        endian = "big"
    else:
        raise ValidationError(f"{_STRIP_FAILED}: unbekannte Byte-Reihenfolge im Exif-Block")
    if int.from_bytes(tiff[2:4], endian) != 42:
        raise ValidationError(f"{_STRIP_FAILED}: ungültiger TIFF-Header im Exif-Block")
    ifd0 = int.from_bytes(tiff[4:8], endian)
    if ifd0 + 2 > len(tiff):
        raise ValidationError(f"{_STRIP_FAILED}: IFD0 liegt außerhalb des Exif-Blocks")
    entries = int.from_bytes(tiff[ifd0:ifd0 + 2], endian)
    for index in range(entries):
        entry = ifd0 + 2 + index * 12
        if entry + 12 > len(tiff):
            raise ValidationError(f"{_STRIP_FAILED}: IFD0-Eintrag liegt außerhalb des Exif-Blocks")
        if int.from_bytes(tiff[entry:entry + 2], endian) != _EXIF_ORIENTATION_TAG:
            continue
        value_type = int.from_bytes(tiff[entry + 2:entry + 4], endian)
        if value_type == 3:  # SHORT
            value = int.from_bytes(tiff[entry + 8:entry + 10], endian)
        elif value_type == 4:  # LONG
            value = int.from_bytes(tiff[entry + 8:entry + 12], endian)
        else:
            raise ValidationError(f"{_STRIP_FAILED}: unbekannter Typ der Orientation")
        if not 1 <= value <= 8:
            raise ValidationError(f"{_STRIP_FAILED}: Orientation {value} liegt außerhalb 1–8")
        return value
    return None


def _minimal_exif_app1(orientation: int) -> bytes:
    """Ein `APP1`-Segment, das **nur** die Orientation trägt (26 Byte TIFF + 6 Byte `Exif\\0\\0`).

    Bewusst klein: das Ziel ist, die Orientierung zu erhalten und **sonst nichts** aus dem
    alten Exif-Block zu retten — GPS, Kameratyp, Seriennummer und Zeitstempel bleiben draußen.
    Little-Endian (`II`), unabhängig von der Byte-Reihenfolge des Originals: gültig ist gültig,
    und die Leser akzeptieren beide.
    """
    tiff = bytearray()
    tiff += b"II\x2a\x00"                       # Little-Endian, Magic 42
    tiff += (8).to_bytes(4, "little")            # Offset von IFD0
    tiff += (1).to_bytes(2, "little")            # ein Eintrag
    tiff += _EXIF_ORIENTATION_TAG.to_bytes(2, "little")
    tiff += (3).to_bytes(2, "little")            # Typ SHORT
    tiff += (1).to_bytes(4, "little")            # Anzahl
    tiff += orientation.to_bytes(2, "little") + b"\x00\x00"  # Wert + Füllbytes
    tiff += (0).to_bytes(4, "little")            # kein Folger-IFD
    payload = _EXIF_APP1_PREFIX + bytes(tiff)
    return b"\xff\xe1" + (len(payload) + 2).to_bytes(2, "big") + payload


def _strip_png(data: bytes) -> bytes:
    """Chunk-Folge durchgehen, die Text-/Zeit-/Exif-Chunks fallen lassen, den Rest in
    Reihenfolge behalten. Weil kein Byte eines behaltenen Chunks verändert wird, bleiben
    dessen CRC gültig."""
    if not data.startswith(_PNG_SIGNATURE):
        raise ValidationError(f"{_STRIP_FAILED}: kein PNG")
    out = bytearray(_PNG_SIGNATURE)
    pos = len(_PNG_SIGNATURE)
    size = len(data)
    while pos < size:
        if pos + 8 > size:
            raise ValidationError(f"{_STRIP_FAILED}: PNG-Chunk abgeschnitten")
        length = int.from_bytes(data[pos:pos + 4], "big")
        chunk_type = data[pos + 4:pos + 8]
        chunk_end = pos + 12 + length  # Länge + Typ + Daten + CRC
        if chunk_end > size:
            raise ValidationError(f"{_STRIP_FAILED}: PNG-Chunk abgeschnitten")
        if chunk_type not in _PNG_DROP_CHUNKS:
            out += data[pos:chunk_end]
        if chunk_type == b"IEND":
            out += data[chunk_end:]  # was hinter IEND steht, bleibt unangetastet
            return bytes(out)
        pos = chunk_end
    raise ValidationError(f"{_STRIP_FAILED}: PNG ohne IEND")


def _strip_webp(data: bytes) -> bytes:
    """RIFF-Chunks durchgehen, `EXIF` und `XMP ` fallen lassen, die Flag-Bits in `VP8X`
    löschen und die RIFF-Größe neu setzen."""
    if len(data) < 12 or data[:4] != b"RIFF" or data[8:12] != b"WEBP":
        raise ValidationError(f"{_STRIP_FAILED}: kein WebP (RIFF/WEBP fehlt)")
    riff_size = int.from_bytes(data[4:8], "little")
    end = 8 + riff_size
    if end > len(data):
        raise ValidationError(f"{_STRIP_FAILED}: WebP abgeschnitten (RIFF-Größe zu groß)")
    chunks: list[tuple[bytes, bytes]] = []
    pos = 12
    while pos + 8 <= end:
        chunk_type = data[pos:pos + 4]
        chunk_size = int.from_bytes(data[pos + 4:pos + 8], "little")
        chunk_end = pos + 8 + chunk_size + (chunk_size & 1)  # ungerade Größen haben ein Füllbyte
        if chunk_end > end:
            raise ValidationError(f"{_STRIP_FAILED}: WebP-Chunk abgeschnitten")
        chunks.append((chunk_type, data[pos:chunk_end]))
        pos = chunk_end
    if pos != end:
        raise ValidationError(f"{_STRIP_FAILED}: WebP-Chunks gehen nicht auf")
    drop_exif = any(chunk_type == b"EXIF" for chunk_type, _ in chunks)
    drop_xmp = any(chunk_type == b"XMP " for chunk_type, _ in chunks)
    body = bytearray()
    for chunk_type, chunk in chunks:
        if chunk_type in (b"EXIF", b"XMP "):
            continue
        if chunk_type == b"VP8X" and len(chunk) >= 9:
            flags = chunk[8]
            if drop_exif:
                flags &= ~_WEBP_FLAG_EXIF
            if drop_xmp:
                flags &= ~_WEBP_FLAG_XMP
            chunk = chunk[:8] + bytes([flags]) + chunk[9:]
        body += chunk
    out = bytearray(b"RIFF")
    out += (4 + len(body)).to_bytes(4, "little")  # RIFF-Größe: „WEBP" + die Chunks
    out += b"WEBP"
    out += body
    out += data[end:]  # was hinter dem RIFF-Container steht, bleibt unangetastet
    return bytes(out)


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
