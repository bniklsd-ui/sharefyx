import re
from pathlib import Path

import pytest

from storage.errors import ValidationError
from storage.files import (
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
