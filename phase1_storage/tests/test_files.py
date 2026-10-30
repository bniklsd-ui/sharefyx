import re
import zlib
from pathlib import Path

import pytest

from storage.errors import ValidationError
from storage.files import (
    ASSET_ID_RE,
    MAX_FOLDER_DEPTH,
    RESERVED_DIR_NAMES,
    asset_dir,
    asset_path,
    atomic_write,
    folder_from_path,
    generate_id,
    item_filename,
    item_path,
    move_asset_dir,
    new_asset_id,
    slugify,
    sniff_image_mime,
    strip_image_metadata,
    validate_folder,
)

ID_RE = re.compile(r"\Aitm_[0-9a-f]{8}\Z")


def test_generate_id_format_and_uniqueness():
    ids = [generate_id() for _ in range(200)]
    assert all(ID_RE.match(i) for i in ids)
    assert len(set(ids)) == 200


def test_slugify_transliterates_german_umlauts():
    assert slugify("Kühlschrank prüfen äöüß") == "kuehlschrank-pruefen-aeoeuess"


def test_slugify_collapses_and_strips_separators():
    assert slugify("  Hallo -- Welt!!  ") == "hallo-welt"


def test_slugify_falls_back_when_nothing_alnum_survives():
    assert slugify("!!!") == "item"


def test_item_filename_and_path(tmp_path):
    path = item_path(tmp_path, "nikinger", "itm_a1b2c3d4", "kuehlschrank")
    assert path == tmp_path / "nikinger" / "itm_a1b2c3d4__kuehlschrank.md"
    assert item_filename("itm_a1b2c3d4", "kuehlschrank") == "itm_a1b2c3d4__kuehlschrank.md"


def test_atomic_write_creates_and_overwrites(tmp_path):
    target = tmp_path / "item.md"
    atomic_write(target, "erste version\n")
    assert target.read_text() == "erste version\n"

    atomic_write(target, "zweite version\n")
    assert target.read_text() == "zweite version\n"

    leftover_tmp = list(tmp_path.glob(".*.tmp"))
    assert leftover_tmp == []


def test_atomic_write_200_items(tmp_path):
    space = tmp_path / "nikinger"
    space.mkdir()
    written = []
    for _ in range(200):
        item_id = generate_id()
        path = item_path(tmp_path, "nikinger", item_id, "titel")
        atomic_write(path, f"content for {item_id}\n")
        written.append((path, item_id))

    files = list(space.glob("*.md"))
    assert len(files) == 200
    for path, item_id in written:
        assert path.read_text() == f"content for {item_id}\n"


def test_atomic_write_crash_before_replace_leaves_no_partial_target(tmp_path, monkeypatch):
    target = tmp_path / "item.md"

    def boom(*args, **kwargs):
        raise OSError("simulated kill -9 between tmp write and replace")

    monkeypatch.setattr("storage.files.os.replace", boom)

    with pytest.raises(OSError):
        atomic_write(target, "sollte nie ankommen\n")

    assert not target.exists()
    assert list(tmp_path.glob(".*.tmp")) == []


def test_atomic_write_crash_preserves_existing_target(tmp_path, monkeypatch):
    target = tmp_path / "item.md"
    atomic_write(target, "alter inhalt\n")

    def boom(*args, **kwargs):
        raise OSError("simulated kill -9 between tmp write and replace")

    monkeypatch.setattr("storage.files.os.replace", boom)

    with pytest.raises(OSError):
        atomic_write(target, "sollte nicht ankommen\n")

    assert target.read_text() == "alter inhalt\n"


def test_item_path_places_file_under_folder(tmp_path):
    path = item_path(tmp_path, "nikinger", "itm_a1b2c3d4", "kuehlschrank", folder="projekte/alpha")
    assert path == tmp_path / "nikinger" / "projekte" / "alpha" / "itm_a1b2c3d4__kuehlschrank.md"


def test_item_path_default_folder_is_unchanged():
    assert item_path(Path("/root"), "s", "itm_x", "slug") == Path("/root/s/itm_x__slug.md")


# -- P6 Step 4: validate_folder / folder_from_path -----------------------------------------


def test_validate_folder_empty_stays_empty():
    assert validate_folder("") == ""


def test_validate_folder_slugifies_each_segment():
    assert validate_folder("Projekte/Älpha") == "projekte/aelpha"


def test_validate_folder_rejects_depth_beyond_max():
    assert MAX_FOLDER_DEPTH == 2
    with pytest.raises(ValidationError):
        validate_folder("a/b/c")


def test_validate_folder_rejects_reserved_names():
    for reserved in RESERVED_DIR_NAMES:
        with pytest.raises(ValidationError):
            validate_folder(reserved)


def test_validate_folder_rejects_deep_traversal_via_depth_check(tmp_path):
    # ".." zaehlt als eigenes Segment -- bei genuegend Ebenen greift der Tiefen-Check, bevor
    # slugify() ueberhaupt laeuft (Advisor-Fund: kein dedizierter Traversal-Check noetig, aber
    # das Verhalten muss gepinnt sein, nicht nur "zufaellig sicher").
    with pytest.raises(ValidationError):
        validate_folder("../../etc")


def test_validate_folder_shallow_traversal_is_rewritten_not_rejected():
    # Innerhalb der erlaubten Tiefe wird ".." NICHT durchgereicht (kein Escape moeglich, path
    # bleibt immer unter data_root/space) -- slugify("..") faellt auf den "item"-Fallback
    # zurueck (kein alnum-Zeichen ueberlebt), das Ergebnis ist eine stille Umbenennung, kein
    # Fehler. Bewusst gepinnt, nicht als Bug behandelt: der Aufrufer bekommt einen harmlosen,
    # aber ueberraschenden Ordnernamen statt eines klaren Fehlers.
    assert validate_folder("../x") == "item/x"


def test_folder_from_path_roundtrips_with_item_path(tmp_path):
    path = item_path(tmp_path, "nikinger", "itm_a1b2c3d4", "titel", folder="projekte/alpha")
    assert folder_from_path(tmp_path, "nikinger", path) == "projekte/alpha"


def test_folder_from_path_top_level_is_empty(tmp_path):
    path = item_path(tmp_path, "nikinger", "itm_a1b2c3d4", "titel")
    assert folder_from_path(tmp_path, "nikinger", path) == ""


def test_folder_from_path_archive_is_never_a_folder(tmp_path):
    path = tmp_path / "nikinger" / "_archive" / "itm_a1b2c3d4__titel.md"
    assert folder_from_path(tmp_path, "nikinger", path) == ""


def test_slug_collision_does_not_overwrite(tmp_path):
    space = tmp_path / "nikinger"
    space.mkdir()
    id_a, id_b = generate_id(), generate_id()
    slug = slugify("Einkaufsliste")

    path_a = item_path(tmp_path, "nikinger", id_a, slug)
    path_b = item_path(tmp_path, "nikinger", id_b, slug)
    assert path_a != path_b

    atomic_write(path_a, "Liste A\n")
    atomic_write(path_b, "Liste B\n")

    assert path_a.read_text() == "Liste A\n"
    assert path_b.read_text() == "Liste B\n"
    assert len(list(space.glob("*.md"))) == 2


# -- Bild-Assets (Phase 6.5 Step B1) ----------------------------------------------------


@pytest.mark.parametrize(
    "data, expected_mime",
    [
        (b"\x89PNG\r\n\x1a\n" + b"rest", "image/png"),
        (b"\xff\xd8\xff" + b"rest", "image/jpeg"),
        (b"GIF87a" + b"rest", "image/gif"),
        (b"GIF89a" + b"rest", "image/gif"),
        (b"RIFF\x00\x00\x00\x00WEBPrest", "image/webp"),
    ],
)
def test_sniff_image_mime_recognizes_each_format(data, expected_mime):
    result = sniff_image_mime(data)
    assert result is not None
    assert result[0] == expected_mime


def test_sniff_image_mime_webp_needs_correct_offset_8_marker():
    # RIFF-Header, aber kein "WEBP" bei Offset 8 -- ein anderes RIFF-Format (z.B. WAV) darf
    # nicht fälschlich als Bild durchgehen.
    assert sniff_image_mime(b"RIFF\x00\x00\x00\x00WAVErest") is None


def test_sniff_image_mime_unknown_bytes_returns_none():
    assert sniff_image_mime(b"not an image") is None


def test_sniff_image_mime_rejects_svg():
    svg = b"<svg xmlns='http://www.w3.org/2000/svg'></svg>"
    assert sniff_image_mime(svg) is None


def test_asset_path_rejects_invalid_ids(tmp_path):
    with pytest.raises(ValidationError):
        asset_dir(tmp_path, "nikinger", "not-an-item-id")
    with pytest.raises(ValidationError):
        asset_path(tmp_path, "nikinger", generate_id(), "not-an-asset-id", "png")


def test_move_asset_dir_is_a_no_op_without_a_source_directory(tmp_path):
    src = asset_dir(tmp_path, "nikinger", generate_id())
    dst = asset_dir(tmp_path, "beta", generate_id())

    move_asset_dir(src, dst)  # darf nicht werfen

    assert not dst.exists()


def test_move_asset_dir_moves_existing_directory(tmp_path):
    item_id = generate_id()
    src = asset_dir(tmp_path, "nikinger", item_id)
    src.mkdir(parents=True)
    (src / "ast_00000000.png").write_bytes(b"x")
    dst = asset_dir(tmp_path, "beta", item_id)

    move_asset_dir(src, dst)

    assert not src.exists()
    assert (dst / "ast_00000000.png").read_bytes() == b"x"


def test_new_asset_id_format_and_uniqueness():
    ids = [new_asset_id() for _ in range(200)]
    assert all(re.match(r"\Aast_[0-9a-f]{8}\Z", i) for i in ids)
    assert len(set(ids)) == 200


# -- EXIF-Bereinigung (P10.5, Block 3, LG-8 / P1-Öffnung 15) ------------------------------
#
# **Die Fixtures werden hier gebaut** (Bytes, keine Binärdateien im Repo) — Plan Block 3,
# Schritt 3.4. Sie sind so gebaut, dass sie den Weg durch den Stripper **wirklich** prüfen:
# eine echte Chunk-/Marker-Folge, keine bloßen Magic Bytes.


def _jpeg_segment(marker: int, payload: bytes) -> bytes:
    """Ein JPEG-Segment: `FF <marker>` + 2-Byte-Länge (inklusive sich selbst) + Nutzlast."""
    return bytes([0xFF, marker]) + (len(payload) + 2).to_bytes(2, "big") + payload


def _exif_payload(orientation: int | None = None, *, gps: bytes | None = None) -> bytes:
    """Ein Exif-APP1-Inhalt (`Exif\\0\\0` + TIFF-Block, Little-Endian) mit optionaler
    `Orientation` und einem optionalen GPS-IFD.

    Der GPS-Marker ist ein **erkennbarer String** — nach dem Strippen muss er weg sein, und
    genau daran prüft der Test, dass nicht nur die Orientation übrig bleibt.
    """
    entries: list[tuple[int, int, int, bytes]] = []
    if orientation is not None:
        entries.append((0x0112, 3, 1, orientation.to_bytes(2, "little") + b"\x00\x00"))
    tail = b""
    if gps is not None:
        gps_ifd = 8 + 2 + 12 * (len(entries) + 1) + 4
        gps_data = gps_ifd + 2 + 12 + 4
        entries.append((0x8825, 4, 1, gps_ifd.to_bytes(4, "little")))
        tail = (
            (1).to_bytes(2, "little")
            + (0x0001).to_bytes(2, "little")
            + (2).to_bytes(2, "little")
            + len(gps).to_bytes(4, "little")
            + gps_data.to_bytes(4, "little")
            + (0).to_bytes(4, "little")
            + gps
        )
    out = bytearray(b"II\x2a\x00")
    out += (8).to_bytes(4, "little")
    out += len(entries).to_bytes(2, "little")
    for tag, value_type, count, value in entries:
        out += tag.to_bytes(2, "little") + value_type.to_bytes(2, "little")
        out += count.to_bytes(4, "little") + value
    out += (0).to_bytes(4, "little")
    out += tail
    return b"Exif\x00\x00" + bytes(out)


def _png_chunk(chunk_type: bytes, payload: bytes) -> bytes:
    """Ein PNG-Chunk: Länge + Typ + Daten + CRC."""
    body = chunk_type + payload
    return (
        len(payload).to_bytes(4, "big")
        + body
        + (zlib.crc32(body) & 0xFFFFFFFF).to_bytes(4, "big")
    )


_PNG_IHDR = (1).to_bytes(4, "big") + (1).to_bytes(4, "big") + bytes([8, 2, 0, 0, 0])


def _webp_chunk(chunk_type: bytes, payload: bytes) -> bytes:
    """Ein WebP-Chunk: Typ + Größe + Daten (+ ein Füllbyte bei ungerader Größe)."""
    pad = b"\x00" if len(payload) % 2 else b""
    return chunk_type + len(payload).to_bytes(4, "little") + payload + pad


def test_strip_jpeg_removes_gps_exif_and_keeps_icc():
    """Der Kern von LG-8: GPS- und Gerätedaten fliegen raus — das **Farbprofil** bleibt.
    Ohne ICC-Profil (`APP2`) würden die Farben des Bildes falsch: das wäre Datenverlust,
    nicht Metadaten-Verlust. Ebenso bleibt JFIF (`APP0`) und Adobe (`APP14`, CMYK)."""
    jpeg = (
        b"\xff\xd8"
        + _jpeg_segment(0xE1, _exif_payload(6, gps=b"GPSLATITUDE"))
        + _jpeg_segment(0xE1, b"http://ns.adobe.com/xap/1.0/\x00XMP-DATEN")
        + _jpeg_segment(0xE2, b"ICC_PROFILE\x00PROFILDATEN")
        + _jpeg_segment(0xE0, b"JFIF\x00")
        + _jpeg_segment(0xED, b"Photoshop 3.0\x00")
        + _jpeg_segment(0xFE, b"ein Kommentar")
        + b"\xff\xda" + (8).to_bytes(2, "big") + b"\x00\x01\x00\x00" + b"\x7f" * 16 + b"\xff\xd9"
    )

    out = strip_image_metadata(jpeg, "image/jpeg")

    assert b"GPSLATITUDE" not in out
    assert b"XMP-DATEN" not in out
    assert b"ein Kommentar" not in out
    assert b"Photoshop 3.0" not in out
    assert b"ICC_PROFILE" in out
    assert b"JFIF" in out
    # Ab SOS wird alles byte-genau kopiert — der Bildinhalt ist unangetastet.
    assert out.endswith(b"\x7f" * 16 + b"\xff\xd9")
    assert out.startswith(b"\xff\xd8")


def test_strip_jpeg_keeps_orientation_only():
    """Ein Handyfoto mit Orientation 6 (90° gedreht) behält die Orientation — als
    **minimales** `APP1` mit genau einem Tag. Der ganze Exif-Block (GPS, Kamera, Zeit) ist
    weg; ohne Orientation stünde das Bild nach dem Hochladen quer."""
    jpeg = (
        b"\xff\xd8"
        + _jpeg_segment(0xE1, _exif_payload(6, gps=b"GPSLATITUDE"))
        + b"\xff\xda" + (8).to_bytes(2, "big") + b"\x00\x01\x00\x00" + b"\x00" * 8 + b"\xff\xd9"
    )

    out = strip_image_metadata(jpeg, "image/jpeg")

    assert out.count(b"\xff\xe1") == 1
    app1 = out[out.find(b"\xff\xe1"):]
    assert b"GPSLATITUDE" not in app1
    # Der Orientation-Tag 0x0112, Typ SHORT, Wert 6 (little endian im Wertfeld).
    assert b"\x12\x01\x03\x00\x01\x00\x00\x00\x06\x00" in app1
    # Sonst nichts: kein GPS-IFD-Pointer (0x8825), keine Kamera, keine Zeit.
    assert b"\x88\x25" not in app1
    # Das Minimal-APP1 ist 36 Byte lang (2 Marker + 2 Länge + 6 "Exif\0\0" + 26 TIFF).
    assert len(app1.split(b"\xff\xda")[0]) == 36


def test_strip_jpeg_drops_the_exif_when_the_orientation_is_one():
    """**Gegenlauf** zu `test_strip_jpeg_keeps_orientation_only`: Orientation 1 ist „normal
    stehend" — da gibt es nichts zu retten, das `APP1` fliegt vollständig weg."""
    jpeg = (
        b"\xff\xd8"
        + _jpeg_segment(0xE1, _exif_payload(1, gps=b"GPSLATITUDE"))
        + b"\xff\xda" + (8).to_bytes(2, "big") + b"\x00\x01\x00\x00" + b"\x00" * 8 + b"\xff\xd9"
    )

    out = strip_image_metadata(jpeg, "image/jpeg")

    assert b"\xff\xe1" not in out
    assert b"GPSLATITUDE" not in out


def test_strip_png_removes_text_chunks():
    """PNG: `tEXt`, `iTXt`, `zTXt`, `eXIf` und `tIME` fliegen weg, alle anderen Chunks
    bleiben **in Reihenfolge** — ihre CRC bleibt gültig, weil kein Byte eines behaltenen
    Chunks verändert wird."""
    png = (
        b"\x89PNG\r\n\x1a\n"
        + _png_chunk(b"IHDR", _PNG_IHDR)
        + _png_chunk(b"tEXt", b"Comment\x00geheim")
        + _png_chunk(b"eXIf", b"Exif-Daten")
        + _png_chunk(b"tIME", b"\x07\xe6\x01\x01\x00\x00\x00")
        + _png_chunk(b"IDAT", b"\x00\x01")
        + _png_chunk(b"IEND", b"")
    )

    out = strip_image_metadata(png, "image/png")

    assert b"geheim" not in out
    assert b"Exif-Daten" not in out
    assert b"tEXt" not in out and b"eXIf" not in out and b"tIME" not in out
    assert out.startswith(b"\x89PNG\r\n\x1a\n")
    assert b"IHDR" in out and b"IDAT" in out
    assert out.endswith(_png_chunk(b"IEND", b""))


def test_strip_webp_removes_exif_and_clears_flags():
    """WebP: die Chunks `EXIF` und `XMP ` fliegen weg, **und** die zugehörigen Flag-Bits in
    `VP8X` werden gelöscht — sonst behauptet die Datei, sie hätte noch Metadaten, die sie
    nicht mehr hat. Die RIFF-Größe wird neu gesetzt."""
    body = (
        _webp_chunk(b"VP8X", bytes([0x0C, 0, 0, 0, 0, 0, 0, 0, 0, 0]))  # EXIF-Bit | XMP-Bit
        + _webp_chunk(b"EXIF", b"Exif-Daten")
        + _webp_chunk(b"XMP ", b"XMP-Daten")
        + _webp_chunk(b"VP8 ", b"\x00" * 10)
    )
    webp = b"RIFF" + (4 + len(body)).to_bytes(4, "little") + b"WEBP" + body

    out = strip_image_metadata(webp, "image/webp")

    assert b"Exif-Daten" not in out
    assert b"XMP-Daten" not in out
    flags = out[20]  # RIFF(4) + Größe(4) + WEBP(4) + Chunk-Typ(4) + Chunk-Größe(4)
    assert flags & 0x08 == 0  # EXIF-Bit
    assert flags & 0x04 == 0  # XMP-Bit
    assert int.from_bytes(out[4:8], "little") == len(out) - 8


def test_strip_leaves_clean_image_byte_identical():
    """Ein Bild **ohne** Metadaten bleibt byte-identisch — es wird nichts neu kodiert, nichts
    umgeschrieben, nichts „normalisiert“."""
    jpeg = (
        b"\xff\xd8"
        + _jpeg_segment(0xE0, b"JFIF\x00")
        + b"\xff\xda" + (8).to_bytes(2, "big") + b"\x00\x01\x00\x00" + b"\x11" * 8 + b"\xff\xd9"
    )
    png = b"\x89PNG\r\n\x1a\n" + _png_chunk(b"IHDR", _PNG_IHDR) + _png_chunk(b"IEND", b"")
    gif = b"GIF89a" + b"restliche-bytes-egal"

    assert strip_image_metadata(jpeg, "image/jpeg") == jpeg
    assert strip_image_metadata(png, "image/png") == png
    assert strip_image_metadata(gif, "image/gif") == gif


def test_strip_rejects_truncated_jpeg():
    """**Fail-closed:** ein abgeschnittenes JPEG wird **nicht** halbbereinigt gespeichert,
    sondern abgelehnt (Geist von Hard Rule 5: nie ein halber Zustand auf der Platte)."""
    voll = (
        b"\xff\xd8"
        + _jpeg_segment(0xE1, _exif_payload(6))
        + b"\xff\xda" + (8).to_bytes(2, "big") + b"\x00\x01\x00\x00" + b"\x00" * 8
    )

    with pytest.raises(ValidationError):
        strip_image_metadata(voll[:20], "image/jpeg")  # mitten im APP1 abgeschnitten
    with pytest.raises(ValidationError):
        strip_image_metadata(voll[:38], "image/jpeg")  # ohne SOS: kein Bildinhalt


def test_strip_rejects_a_broken_exif_block():
    """**Fail-closed:** ein Exif-Block, den der Parser nicht versteht, ergibt einen Fehler.
    Wer die Orientation nicht sicher lesen kann, darf das Bild nicht halbbereinigt speichern."""
    kaputt = b"Exif\x00\x00" + b"II" + b"\x00\x00"  # die Magic 42 fehlt
    jpeg = (
        b"\xff\xd8"
        + _jpeg_segment(0xE1, kaputt)
        + b"\xff\xda" + (8).to_bytes(2, "big") + b"\x00\x01\x00\x00" + b"\x00" * 8 + b"\xff\xd9"
    )

    with pytest.raises(ValidationError):
        strip_image_metadata(jpeg, "image/jpeg")


def test_strip_rejects_bytes_that_do_not_match_the_mime():
    """Der Typ kommt aus den Magic Bytes, nicht vom Client — und die Bytes müssen zum
    behaupteten Typ passen."""
    with pytest.raises(ValidationError):
        strip_image_metadata(b"\x89PNG\r\n\x1a\nrest", "image/jpeg")
    with pytest.raises(ValidationError):
        strip_image_metadata(b"egal", "image/tiff")


def test_asset_id_re_rejects_a_trailing_newline():
    """Ultra-Review B1 (2026-10-30): `$` lässt vor einem abschliessenden Zeilenumbruch ein
    Match zu — `\\Z` nicht. Die ID geht danach in einen Glob und einen Dateinamen."""
    assert ASSET_ID_RE.match("ast_0123abcd")
    assert not ASSET_ID_RE.match("ast_0123abcd\n")
