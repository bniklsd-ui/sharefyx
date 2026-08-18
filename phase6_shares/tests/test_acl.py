"""Tests für `storage.acl.AclReader` (Plan §1.2.3, §5 Testliste: Vererbung, fail-closed,
Cache-Invalidierung)."""
from __future__ import annotations

import logging

from storage.acl import ACL_FILENAME, AclReader, Grant
from storage.store import Store


def _write_share_yml(directory, content: str) -> None:
    directory.mkdir(parents=True, exist_ok=True)
    (directory / ACL_FILENAME).write_text(content, encoding="utf-8")


def test_no_share_yml_anywhere_grants_nothing(tmp_path):
    (tmp_path / "nikinger").mkdir()
    reader = AclReader(tmp_path)
    grant = reader.grants_for_dir(tmp_path / "nikinger")
    assert grant == Grant()


def test_space_root_share_yml_grants_directly(tmp_path):
    _write_share_yml(tmp_path / "nikinger", "read: [fabian]\nwrite: []\n")
    reader = AclReader(tmp_path)
    grant = reader.grants_for_dir(tmp_path / "nikinger")
    assert grant.read == frozenset({"fabian"})
    assert grant.write == frozenset()


def test_write_implies_read_without_being_listed_twice(tmp_path):
    _write_share_yml(tmp_path / "nikinger", "write: [fabian]\n")
    reader = AclReader(tmp_path)
    grant = reader.grants_for_dir(tmp_path / "nikinger")
    assert grant.read == frozenset({"fabian"})
    assert grant.write == frozenset({"fabian"})


def test_nested_folder_grant_is_union_with_space_root(tmp_path):
    _write_share_yml(tmp_path / "nikinger", "read: [fabian]\n")
    _write_share_yml(tmp_path / "nikinger" / "projekte" / "alpha", "write: [dritter]\n")
    reader = AclReader(tmp_path)

    grant = reader.grants_for_dir(tmp_path / "nikinger" / "projekte" / "alpha")

    assert grant.read == frozenset({"fabian", "dritter"})
    assert grant.write == frozenset({"dritter"})

    # Der Zwischenordner selbst (kein eigenes .share.yml) sieht nur den Space-Root-Grant.
    intermediate = reader.grants_for_dir(tmp_path / "nikinger" / "projekte")
    assert intermediate.read == frozenset({"fabian"})
    assert intermediate.write == frozenset()


def test_unparseable_yaml_grants_nothing_and_logs_critical(tmp_path, caplog):
    _write_share_yml(tmp_path / "nikinger", "read: [unclosed\n")
    reader = AclReader(tmp_path)

    with caplog.at_level(logging.CRITICAL):
        grant = reader.grants_for_dir(tmp_path / "nikinger")

    assert grant == Grant()
    assert any(r.levelno == logging.CRITICAL for r in caplog.records)


def test_non_mapping_yaml_grants_nothing_and_logs_critical(tmp_path, caplog):
    _write_share_yml(tmp_path / "nikinger", "- fabian\n- dritter\n")
    reader = AclReader(tmp_path)

    with caplog.at_level(logging.CRITICAL):
        grant = reader.grants_for_dir(tmp_path / "nikinger")

    assert grant == Grant()
    assert any(r.levelno == logging.CRITICAL for r in caplog.records)


def test_empty_share_yml_grants_nothing_without_error(tmp_path):
    _write_share_yml(tmp_path / "nikinger", "")
    reader = AclReader(tmp_path)
    assert reader.grants_for_dir(tmp_path / "nikinger") == Grant()


def test_unknown_keys_are_ignored(tmp_path):
    _write_share_yml(tmp_path / "nikinger", "read: [fabian]\nnote: \"Projekt Alpha\"\n")
    reader = AclReader(tmp_path)
    grant = reader.grants_for_dir(tmp_path / "nikinger")
    assert grant.read == frozenset({"fabian"})


def test_cache_is_keyed_by_stat_not_reread_on_every_call(tmp_path, monkeypatch):
    _write_share_yml(tmp_path / "nikinger", "read: [fabian]\n")
    reader = AclReader(tmp_path)
    first = reader.grants_for_dir(tmp_path / "nikinger")
    assert first.read == frozenset({"fabian"})

    # Inhalt ändern, aber stat() unverändert vorspiegeln -- der Cache muss den alten Wert
    # liefern, bis invalidate() oder ein echter stat()-Unterschied ihn ungültig macht.
    share_path = tmp_path / "nikinger" / ACL_FILENAME
    real_stat = share_path.stat()
    share_path.write_text("read: [dritter]\n", encoding="utf-8")
    monkeypatch.setattr(type(share_path), "stat", lambda self: real_stat)

    stale = reader.grants_for_dir(tmp_path / "nikinger")
    assert stale.read == frozenset({"fabian"})

    reader.invalidate()
    monkeypatch.undo()
    fresh = reader.grants_for_dir(tmp_path / "nikinger")
    assert fresh.read == frozenset({"dritter"})


def test_members_of_space_reads_only_space_root_write(tmp_path):
    _write_share_yml(tmp_path / "nikinger", "write: [fabian]\n")
    _write_share_yml(tmp_path / "nikinger" / "projekte", "write: [dritter]\n")
    reader = AclReader(tmp_path)
    assert reader.members_of_space("nikinger") == frozenset({"fabian"})


def test_acl_decision_follows_the_item_into_the_target_space(tmp_path):
    """§4.5: `Store.acl_of()` liest nie einen an das Item selbst gebundenen alten Wert — ein
    `move()` über Space-Grenzen muss die Rechte des NEUEN Pfads liefern, nicht die des alten.
    `AclReader` kennt ohnehin keine Items (nur Verzeichnisse), dieser Test beweist die
    Vereinigung über den echten `Store.move()`-Aufweg, nicht nur `AclReader` isoliert."""
    _write_share_yml(tmp_path / "nikinger", "write: [dritter]\n")
    _write_share_yml(tmp_path / "fabian", "read: [vierter]\n")
    store = Store(tmp_path, git=False)
    item = store.create("nikinger", type="note", title="Umzug")

    before = store.acl_of(item.id)
    assert before.space == "nikinger"
    assert before.write == frozenset({"dritter"})

    store.move(item.id, version=item.version, space="fabian")

    after = store.acl_of(item.id)
    assert after.space == "fabian"
    assert after.read == frozenset({"vierter"})
    assert after.write == frozenset()
    assert "dritter" not in after.read | after.write
