"""Bild-Assets × ACL (Phase 6.5 Step B2, Plan §3 Step B2 Testliste). Testheimat ist dieses NEUE
Phasenverzeichnis, nicht `phase6_shares/tests/` — dieselbe Konvention wie `test_acl.py` dort:
`Store` + `SharePolicy` direkt, kein HTTP-Layer. Ein Bild trägt selbst keine eigene ACL (P6-AW,
`docs/concepts/phase6_5_tools_images_plan.md` §3 Step B2-Tabelle) — es erbt die Rechte des
Items, über dasselbe `store.acl_of(item_id)` + `can_read_item_as_human()`/
`can_write_item_as_human()`, das `webui/api.py`s Asset-Routen vor jedem Store-Aufruf benutzen.
Diese Tests beweisen genau diese Vererbung, nicht die HTTP-Fläche selbst (dafür:
`phase5_ui/tests/test_api.py`, Abschnitt „Assets").

Zwilling zu `phase6_shares/tests/test_acl.py ::
test_acl_decision_follows_the_item_into_the_target_space` — hier eine Ebene weiter: nicht nur
die `AclDecision`, sondern auch die tatsächlichen Bild-Bytes müssen dem Item über eine
Space-Grenze hinweg folgen.
"""
from __future__ import annotations

from mcpserver.permissions import SharePolicy
from storage.store import Store

_PNG = b"\x89PNG\r\n\x1a\n" + b"restliche-bytes-egal"


def _write_share_yml(directory, content: str) -> None:
    directory.mkdir(parents=True, exist_ok=True)
    (directory / ".share.yml").write_text(content, encoding="utf-8")


def test_foreign_item_with_share_read_makes_its_asset_downloadable(tmp_path):
    store = Store(tmp_path, git=False)
    permissions = SharePolicy(store.acl_reader)
    item = store.create("fabian", type="note", title="Fremd, aber geteilt")
    asset = store.put_asset(item.id, data=_PNG)
    store.update(item.id, version=item.version, share_read=["niklas"])

    acl = store.acl_of(item.id)
    assert permissions.can_read_item_as_human("niklas", acl)
    data, mime = store.get_asset(item.id, asset.id)
    assert data == _PNG
    assert mime == "image/png"


def test_foreign_item_without_a_grant_denies_read(tmp_path):
    store = Store(tmp_path, git=False)
    permissions = SharePolicy(store.acl_reader)
    item = store.create("fabian", type="note", title="Fremd, ungeteilt")
    store.put_asset(item.id, data=_PNG)

    acl = store.acl_of(item.id)
    assert not permissions.can_read_item_as_human("niklas", acl)


def test_share_read_alone_does_not_grant_write(tmp_path):
    store = Store(tmp_path, git=False)
    permissions = SharePolicy(store.acl_reader)
    item = store.create("fabian", type="note", title="Nur lesbar")
    store.update(item.id, version=item.version, share_read=["niklas"])

    acl = store.acl_of(item.id)
    assert permissions.can_read_item_as_human("niklas", acl)
    assert not permissions.can_write_item_as_human("niklas", acl)


def test_asset_follows_the_item_into_the_target_space_and_is_readable_there(tmp_path):
    """Zwilling zu `test_acl_decision_follows_the_item_into_the_target_space` — Asset-Bytes
    statt nur der `AclDecision`."""
    _write_share_yml(tmp_path / "beta", "read: [vierter]\n")
    store = Store(tmp_path, git=False)
    permissions = SharePolicy(store.acl_reader)
    item = store.create("nikinger", type="note", title="Umzug mit Bild")
    asset = store.put_asset(item.id, data=_PNG)

    store.move(item.id, version=item.version, space="beta")

    acl = store.acl_of(item.id)
    assert acl.space == "beta"
    assert permissions.can_read_item_as_human("vierter", acl)
    data, mime = store.get_asset(item.id, asset.id)
    assert data == _PNG
    assert mime == "image/png"
