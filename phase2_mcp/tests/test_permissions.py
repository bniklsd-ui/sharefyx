"""`SharePolicy` (P6 Step 5, ersetzt `OwnSpaceWritable`) — reine Rechteentscheidung, kein
Store-Aufruf außer über den injizierten `AclReader`. Adapter-Wiring (welche Tools welche
Methode wann aufrufen) liegt in `test_tools.py`/`phase5_ui/tests/test_api.py`; hier geht es um
`SharePolicy` selbst gegen einen echten `AclReader` auf einem `tmp_path`."""
from __future__ import annotations

from storage.acl import AclDecision, AclReader
from mcpserver.permissions import SharePolicy, Surface

SPACE_A = "alpha"
SPACE_B = "beta"
# P10.5, Block 2 (2026-10-22): die Home-Space-Regeln brauchen zwei weitere Namen — `gamma` steht
# für den Home-Space eines **anderen** Nutzers, `delta` für einen Team-Space.
SPACE_C = "gamma"
SPACE_D = "delta"


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


# -- Home-Spaces und Team-Spaces (P10.5, Block 2: RE-1, RE-2, P10-I, P10.5-N) -----------------


def _policy(tmp_path, home_spaces: set[str]) -> SharePolicy:
    """Policy mit Home-Space-Kenntnis. Live setzt `mcpserver/app.py :: create_app()` dasselbe
    Prädikat aus der Auth-DB (`get_user(space) is not None`); hier steht es ausdrücklich."""
    return SharePolicy(AclReader(tmp_path), is_home_space=lambda space: space in home_spaces)


def test_team_space_needs_a_home_space_predicate(tmp_path):
    """**Fail-closed (Plan Block 2):** ohne Prädikat kennt die Policy keinen Home-Space — und
    damit auch keinen Team-Space. Ein Space, von dem niemand behauptet, dass er niemandem
    gehört, ist kein *belegter* Team-Space, und Team-Rechte gibt es nur dort."""
    without_predicate = SharePolicy(AclReader(tmp_path))
    assert without_predicate.is_home_space(SPACE_A) is False
    assert without_predicate.is_team_space(SPACE_B) is False

    with_predicate = _policy(tmp_path, {SPACE_A})
    assert with_predicate.is_home_space(SPACE_A) is True
    assert with_predicate.is_team_space(SPACE_B) is True
    assert with_predicate.is_home_space(SPACE_B) is False


def test_manages_space_owner_and_team_writer(tmp_path):
    """Wer darf wie der Eigentümer handeln? Der Eigentümer immer, ein space-level Schreiber in
    einem **Team-Space** — und niemand sonst. Ein fremder Home-Space bleibt gesperrt (P10-I)."""
    _write_share_yml(tmp_path / SPACE_B, f"write: [{SPACE_A}]\n")
    policy = _policy(tmp_path, {SPACE_A, SPACE_C})

    assert policy.manages_space(SPACE_A, SPACE_A) is True      # der eigene Space
    assert policy.manages_space(SPACE_A, SPACE_B) is True       # Team-Space + space-level write
    assert policy.manages_space(SPACE_C, SPACE_B) is False      # Team-Space, aber kein Grant
    assert policy.manages_space(SPACE_A, SPACE_C) is False      # fremder Home-Space
    assert policy.manages_space(SPACE_A, SPACE_D) is False      # Team-Space, aber kein Grant


def test_foreign_home_space_is_never_a_move_target(tmp_path):
    """P10-I: kein Item wandert in den Home-Space eines anderen — auch nicht mit Schreibrecht
    dort. Der eigene Home-Space und Team-Spaces bleiben offen."""
    _write_share_yml(tmp_path / SPACE_C, f"write: [{SPACE_A}]\n")
    policy = _policy(tmp_path, {SPACE_A, SPACE_C})

    assert policy.may_move_between(SPACE_A, SPACE_A, SPACE_C) is False   # fremder Home-Space
    assert policy.may_move_between(SPACE_A, SPACE_A, SPACE_D) is True    # Team-Space
    assert policy.may_move_between(SPACE_A, SPACE_A, SPACE_A) is True    # eigener Space


def test_foreign_home_space_is_never_a_move_source(tmp_path):
    """P10.5-N (Nikinger 2026-10-21): kein Item wandert **aus** dem Home-Space eines anderen
    heraus — das wäre dort ein Löschen (P9-K sperrt Löschen in fremden Home-Spaces)."""
    _write_share_yml(tmp_path / SPACE_C, f"write: [{SPACE_A}]\n")
    policy = _policy(tmp_path, {SPACE_A, SPACE_C})

    assert policy.may_move_between(SPACE_A, SPACE_C, SPACE_D) is False   # fremder Home-Space
    assert policy.may_move_between(SPACE_A, SPACE_D, SPACE_D) is True    # Team-Space
    assert policy.may_move_between(SPACE_A, SPACE_A, SPACE_D) is True    # eigener Space
