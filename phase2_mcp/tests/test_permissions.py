"""`SharePolicy` (P6 Step 5, ersetzt `OwnSpaceWritable`) — reine Rechteentscheidung, kein
Store-Aufruf außer über den injizierten `AclReader`. Adapter-Wiring (welche Tools welche
Methode wann aufrufen) liegt in `test_tools.py`/`phase5_ui/tests/test_api.py`; hier geht es um
`SharePolicy` selbst gegen einen echten `AclReader` auf einem `tmp_path`."""
from __future__ import annotations

from storage.acl import AclDecision, AclReader
from mcpserver.permissions import SharePolicy, Surface

SPACE_A = "alpha"
SPACE_B = "beta"


def _write_share_yml(directory, content: str) -> None:
    directory.mkdir(parents=True, exist_ok=True)
    (directory / ".share.yml").write_text(content, encoding="utf-8")


def test_own_space_always_readable_and_writable(tmp_path):
    policy = SharePolicy(AclReader(tmp_path))
    assert policy.can_read(SPACE_A, SPACE_A) is True
    assert policy.can_write(SPACE_A, SPACE_A) is True


def test_foreign_space_without_share_is_neither_readable_nor_writable(tmp_path):
    policy = SharePolicy(AclReader(tmp_path))
    assert policy.can_read(SPACE_A, SPACE_B) is False
    assert policy.can_write(SPACE_A, SPACE_B) is False


def test_space_root_share_yml_grants_read_and_write(tmp_path):
    _write_share_yml(tmp_path / SPACE_B, f"read: [{SPACE_A}]\nwrite: [{SPACE_A}]\n")
    policy = SharePolicy(AclReader(tmp_path))
    assert policy.can_read(SPACE_A, SPACE_B) is True
    assert policy.can_write(SPACE_A, SPACE_B) is True


def test_visible_spaces_filters_by_can_read(tmp_path):
    _write_share_yml(tmp_path / SPACE_B, f"read: [{SPACE_A}]\n")
    policy = SharePolicy(AclReader(tmp_path))
    assert policy.visible_spaces(SPACE_A, [SPACE_A, SPACE_B, "gamma"]) == [SPACE_A, SPACE_B]


def test_can_read_item_true_for_owner(tmp_path):
    policy = SharePolicy(AclReader(tmp_path))
    acl = AclDecision(space=SPACE_A, folder="", visibility="private", read=frozenset(), write=frozenset())
    assert policy.can_read_item(SPACE_A, acl, surface=Surface.AGENT) is True


def test_can_read_item_false_for_foreign_actor_without_share(tmp_path):
    policy = SharePolicy(AclReader(tmp_path))
    acl = AclDecision(space=SPACE_A, folder="", visibility="private", read=frozenset(), write=frozenset())
    assert policy.can_read_item(SPACE_B, acl, surface=Surface.AGENT) is False


def test_can_read_item_true_for_actor_in_read_set(tmp_path):
    policy = SharePolicy(AclReader(tmp_path))
    acl = AclDecision(
        space=SPACE_A, folder="", visibility="private", read=frozenset({SPACE_B}), write=frozenset(),
    )
    assert policy.can_read_item(SPACE_B, acl, surface=Surface.AGENT) is True


def test_can_read_item_human_only_blocks_agent_surface_even_for_owner(tmp_path):
    policy = SharePolicy(AclReader(tmp_path))
    acl = AclDecision(space=SPACE_A, folder="", visibility="human", read=frozenset(), write=frozenset())
    assert policy.can_read_item(SPACE_A, acl, surface=Surface.AGENT) is False
    assert policy.can_read_item(SPACE_A, acl, surface=Surface.HUMAN) is True


def test_can_read_item_as_human_is_equivalent_to_explicit_human_surface(tmp_path):
    policy = SharePolicy(AclReader(tmp_path))
    acl = AclDecision(
        space=SPACE_A, folder="", visibility="human", read=frozenset({SPACE_B}), write=frozenset(),
    )
    assert policy.can_read_item_as_human(SPACE_B, acl) == policy.can_read_item(
        SPACE_B, acl, surface=Surface.HUMAN
    )


def test_can_write_item_true_for_owner_and_write_set_false_otherwise(tmp_path):
    policy = SharePolicy(AclReader(tmp_path))
    acl = AclDecision(
        space=SPACE_A, folder="", visibility="private", read=frozenset({SPACE_B}), write=frozenset(),
    )
    assert policy.can_write_item(SPACE_A, acl, surface=Surface.AGENT) is True
    assert policy.can_write_item(SPACE_B, acl, surface=Surface.AGENT) is False  # nur read, kein write

    acl_write = AclDecision(
        space=SPACE_A, folder="", visibility="private",
        read=frozenset({SPACE_B}), write=frozenset({SPACE_B}),
    )
    assert policy.can_write_item(SPACE_B, acl_write, surface=Surface.AGENT) is True


def test_can_write_item_human_only_blocks_agent_surface_even_for_owner(tmp_path):
    """Fix, 2026-08-12 (Advisor-Fund nach dem ersten Step-5-Commit): ohne diese Sperre wäre ein
    `visibility: human`-Item für die Agentenfläche zwar unlesbar, aber weiterhin voll
    beschreibbar über den eigenen Space-Token — genau die Lücke, die P6-P schließen sollte."""
    policy = SharePolicy(AclReader(tmp_path))
    acl = AclDecision(space=SPACE_A, folder="", visibility="human", read=frozenset(), write=frozenset())
    assert policy.can_write_item(SPACE_A, acl, surface=Surface.AGENT) is False
    assert policy.can_write_item(SPACE_A, acl, surface=Surface.HUMAN) is True


def test_can_write_item_as_human_is_equivalent_to_explicit_human_surface(tmp_path):
    policy = SharePolicy(AclReader(tmp_path))
    acl = AclDecision(
        space=SPACE_A, folder="", visibility="human", read=frozenset(), write=frozenset({SPACE_B}),
    )
    assert policy.can_write_item_as_human(SPACE_B, acl) == policy.can_write_item(
        SPACE_B, acl, surface=Surface.HUMAN
    )
