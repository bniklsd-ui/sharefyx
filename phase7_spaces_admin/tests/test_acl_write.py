"""Tests für die Schreibseite von `storage/acl.py` (P7 Step C1, sechste Contract-Öffnung) —
immer gegen ein Wegwerf-`tmp_path`, nie gegen den echten `DATA_ROOT`. `phase6_shares/
tests/test_spacectl.py` (20 Tests) bleibt unverändert grün als Regressionsbeweis derselben
Extraktion — diese Datei prüft `acl.py`s neue Funktionen direkt, ohne den CLI-Umweg.
"""
from __future__ import annotations

import subprocess
from pathlib import Path

import pytest
import yaml

from storage import acl


@pytest.fixture
def data_root(tmp_path) -> Path:
    root = tmp_path / "data"
    root.mkdir()
    return root


def _share_yml(space_dir: Path) -> dict:
    return yaml.safe_load((space_dir / ".share.yml").read_text(encoding="utf-8"))


def _commit_count(data_root: Path) -> int:
    result = subprocess.run(
        ["git", "-C", str(data_root), "log", "--oneline"],
        capture_output=True, text=True,
    )
    return len(result.stdout.splitlines())


# -- add_member -----------------------------------------------------------------------------


def test_add_member_adds_to_read(data_root):
    (data_root / "niklas").mkdir()
    added = acl.add_member(data_root, "niklas", "fabian", write=False)
    assert added is True
    assert _share_yml(data_root / "niklas") == {"read": ["fabian"]}


def test_add_member_is_idempotent(data_root):
    (data_root / "niklas").mkdir()
    acl.add_member(data_root, "niklas", "fabian", write=False)
    added_again = acl.add_member(data_root, "niklas", "fabian", write=False)
    assert added_again is False
    assert _share_yml(data_root / "niklas") == {"read": ["fabian"]}


def test_add_member_write_implies_read_without_duplicate_entry(data_root):
    (data_root / "niklas").mkdir()
    acl.add_member(data_root, "niklas", "fabian", write=True)
    data = _share_yml(data_root / "niklas")
    assert data == {"write": ["fabian"]}
    assert "read" not in data


def test_add_member_produces_exactly_one_commit(data_root):
    (data_root / "niklas").mkdir()
    before = _commit_count(data_root)
    acl.add_member(data_root, "niklas", "fabian", write=False)
    assert _commit_count(data_root) == before + 1


# -- remove_member ---------------------------------------------------------------------------


def test_remove_member_removes_from_both_lists(data_root):
    # `write:` impliziert `read:` nur beim Lesen (`AclReader`), nicht in der Datei selbst —
    # ein Name kann trotzdem in beiden Rohlisten stehen (z.B. historisch von Hand editiert).
    # Genau dieser Fall ist es, den `remove_member` aus beiden entfernen muss.
    space_dir = data_root / "niklas"
    space_dir.mkdir()
    (space_dir / acl.ACL_FILENAME).write_text(
        yaml.safe_dump({"read": ["fabian"], "write": ["fabian"]}), encoding="utf-8",
    )
    removed = acl.remove_member(data_root, "niklas", "fabian")
    assert removed == ["read", "write"]
    assert not (data_root / "niklas" / acl.ACL_FILENAME).exists()


def test_remove_member_no_op_when_not_present(data_root):
    (data_root / "niklas").mkdir()
    before = _commit_count(data_root)
    removed = acl.remove_member(data_root, "niklas", "fabian")
    assert removed == []
    assert _commit_count(data_root) == before


def test_remove_member_leaves_the_other_list_intact(data_root):
    (data_root / "niklas").mkdir()
    acl.add_member(data_root, "niklas", "fabian", write=False)
    acl.add_member(data_root, "niklas", "testnutzer-p7", write=False)
    acl.remove_member(data_root, "niklas", "fabian")
    assert _share_yml(data_root / "niklas") == {"read": ["testnutzer-p7"]}


def test_remove_member_produces_exactly_one_commit(data_root):
    (data_root / "niklas").mkdir()
    acl.add_member(data_root, "niklas", "fabian", write=False)
    before = _commit_count(data_root)
    acl.remove_member(data_root, "niklas", "fabian")
    assert _commit_count(data_root) == before + 1


# -- create_space -----------------------------------------------------------------------------


def test_create_space_creates_the_directory(data_root):
    path = acl.create_space(data_root, "dritter")
    assert path == data_root / "dritter"
    assert path.is_dir()


def test_create_space_rejects_existing(data_root):
    acl.create_space(data_root, "dritter")
    with pytest.raises(acl.AclWriteError):
        acl.create_space(data_root, "dritter")


@pytest.mark.parametrize("name", ["a/b", ".hidden", "_archive", "_assets"])
def test_create_space_rejects_invalid_names(data_root, name):
    with pytest.raises(acl.AclWriteError):
        acl.create_space(data_root, name)


# -- remove_space_dir / spaces_referencing -----------------------------------------------------


def test_remove_space_dir_removes_the_directory(data_root):
    acl.create_space(data_root, "dritter")
    acl.remove_space_dir(data_root, "dritter")
    assert not (data_root / "dritter").exists()


def test_remove_space_dir_rejects_unknown_space(data_root):
    with pytest.raises(acl.AclWriteError):
        acl.remove_space_dir(data_root, "nirgends")


def test_spaces_referencing_finds_references(data_root):
    (data_root / "niklas").mkdir()
    (data_root / "fabian").mkdir()
    acl.add_member(data_root, "niklas", "fabian", write=False)
    hits = acl.spaces_referencing(data_root, "fabian")
    assert hits == ["niklas/.share.yml"]


def test_spaces_referencing_excludes_given_path(data_root):
    (data_root / "niklas").mkdir()
    acl.add_member(data_root, "niklas", "fabian", write=False)
    hits = acl.spaces_referencing(
        data_root, "fabian", exclude=data_root / "niklas" / acl.ACL_FILENAME,
    )
    assert hits == []


# -- read_share_file: laut statt fail-closed, getrennt von AclReader --------------------------


def test_read_share_file_raises_on_malformed_yaml_while_aclreader_stays_fail_closed(data_root):
    space_dir = data_root / "niklas"
    space_dir.mkdir()
    (space_dir / acl.ACL_FILENAME).write_text("not: a: valid: mapping: [", encoding="utf-8")
    with pytest.raises(yaml.YAMLError):
        acl.read_share_file(data_root, "niklas")
    reader = acl.AclReader(data_root)
    assert reader.grants_for_space("niklas") == acl.Grant()
