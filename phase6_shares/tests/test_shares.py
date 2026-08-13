"""Tests für `webui.shares :: widens()` (Step 7 Commit 5a, Plan §1.2.5/P6-N) — die
Wahrheitstabelle aus der Ausführungsplan-Testliste (`serialized-seeking-aurora.md`, Commit 5):
Verkleinerung, Erweiterung, `visibility`-Wechsel in beide Richtungen (strukturell nie ein Widen,
siehe `shares.py`s Moduldocstring), reine Inhaltsänderung, und ein Ordner-Verschieben in einen
`.share.yml`-breiter geteilten Ordner."""
from __future__ import annotations

from storage.acl import AclReader

from webui.shares import ShareState, widens

SPACE = "niklas"


def _state(**overrides) -> ShareState:
    defaults = dict(
        visibility="private", share_read=frozenset(), share_write=frozenset(),
        space=SPACE, folder="",
    )
    defaults.update(overrides)
    return ShareState(**defaults)


def test_adding_a_share_read_name_widens(tmp_path):
    acl = AclReader(tmp_path)
    before = _state()
    after = _state(share_read=frozenset({"fabian"}))
    assert widens(before, after, acl=acl) is True


def test_adding_a_share_write_name_widens(tmp_path):
    acl = AclReader(tmp_path)
    before = _state()
    after = _state(share_write=frozenset({"fabian"}))
    assert widens(before, after, acl=acl) is True


def test_removing_a_share_read_name_does_not_widen(tmp_path):
    acl = AclReader(tmp_path)
    before = _state(share_read=frozenset({"fabian"}))
    after = _state()
    assert widens(before, after, acl=acl) is False


def test_removing_a_share_write_name_does_not_widen(tmp_path):
    acl = AclReader(tmp_path)
    before = _state(share_write=frozenset({"fabian"}))
    after = _state()
    assert widens(before, after, acl=acl) is False


def test_private_to_human_is_not_a_widen(tmp_path):
    # `decision_for()` benutzt `visibility` nie für die read/write-Vereinigung (P6 Step 5s
    # eigener Fund, hier wiederverwendet) — ein reiner Sichtbarkeitswechsel ohne Freigabe
    # ändert also nie die effektive Menge.
    acl = AclReader(tmp_path)
    before = _state(visibility="private")
    after = _state(visibility="human")
    assert widens(before, after, acl=acl) is False


def test_human_to_private_is_not_a_widen(tmp_path):
    acl = AclReader(tmp_path)
    before = _state(visibility="human")
    after = _state(visibility="private")
    assert widens(before, after, acl=acl) is False


def test_pure_content_edit_is_not_a_widen(tmp_path):
    acl = AclReader(tmp_path)
    state = _state(share_read=frozenset({"fabian"}))
    assert widens(state, state, acl=acl) is False


def test_folder_move_into_a_wider_shared_folder_widens(tmp_path):
    # Kein Item-Feld ändert sich (share_read/share_write/visibility identisch) — die Erweiterung
    # kommt ausschließlich aus der `.share.yml` des Zielordners, `decision_for()` muss das über
    # den `acl`-Parameter selbst auflösen, nicht `widens()` selbst.
    (tmp_path / SPACE / "geteilt").mkdir(parents=True)
    (tmp_path / SPACE / "geteilt" / ".share.yml").write_text("read: [fabian]\n", encoding="utf-8")
    acl = AclReader(tmp_path)
    before = _state(folder="")
    after = _state(folder="geteilt")
    assert widens(before, after, acl=acl) is True
