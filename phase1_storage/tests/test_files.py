import re

import pytest

from storage.files import (
    atomic_write,
    generate_id,
    item_filename,
    item_path,
    rename_for_new_slug,
    slugify,
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


def test_rename_for_new_slug(tmp_path):
    space = tmp_path / "nikinger"
    space.mkdir()
    item_id = generate_id()
    old_path = item_path(tmp_path, "nikinger", item_id, "alter-titel")
    atomic_write(old_path, "Inhalt bleibt gleich\n")

    new_path = rename_for_new_slug(old_path, item_id, "neuer-titel")

    assert new_path == item_path(tmp_path, "nikinger", item_id, "neuer-titel")
    assert not old_path.exists()
    assert new_path.read_text() == "Inhalt bleibt gleich\n"


def test_rename_for_new_slug_is_noop_when_slug_unchanged(tmp_path):
    space = tmp_path / "nikinger"
    space.mkdir()
    item_id = generate_id()
    path = item_path(tmp_path, "nikinger", item_id, "titel")
    atomic_write(path, "Inhalt\n")

    result = rename_for_new_slug(path, item_id, "titel")

    assert result == path
    assert path.read_text() == "Inhalt\n"
