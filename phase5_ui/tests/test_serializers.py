"""`webui/serializers.py` direkt getestet (Plan §3.2, §5 Step 5) — reine Funktionen, kein Store,
kein HTTP.

**P6 Step 5:** `readonly` ist jetzt überall ein Pflichtparameter (der Aufrufer, `api.py`, löst
ihn über eine `AclDecision` auf — `serializers.py` selbst macht keine Store-Aufrufe, siehe
Moduldocstring dort); `own_space` bleibt zusätzlich für `shared`/`own`. `search_to_json()` ist
auf eine dünne Hülle um bereits fertige Item-Dicts geschrumpft, kein `SearchResult` mehr."""
from __future__ import annotations

from datetime import date, datetime, timezone

from storage.models import Item, ItemSummary, SpaceInfo

from webui.serializers import item_to_json, search_to_json, space_to_json, summary_to_json

NOW = datetime(2026, 8, 5, 12, 0, 0, tzinfo=timezone.utc)


def _item(**overrides) -> Item:
    fields = dict(
        id="itm_deadbeef", space="niklas", type="note", title="Test", status="active",
        body="Text", due=None, tags=["a"], links=[], created=NOW, updated=NOW, version=1,
        extra={},
    )
    fields.update(overrides)
    return Item(**fields)


def test_item_to_json_defaults_format_to_markdown():
    payload = item_to_json(_item(), readonly=False, own_space="niklas")
    assert payload["format"] == "markdown"
    assert payload["readonly"] is False


def test_item_to_json_reads_format_from_extra():
    payload = item_to_json(_item(extra={"format": "plain"}), readonly=True, own_space="niklas")
    assert payload["format"] == "plain"
    assert payload["extra"] == {"format": "plain"}
    assert payload["readonly"] is True


def test_item_to_json_body_is_plain_text_never_rendered():
    payload = item_to_json(_item(body="<b>roh</b>"), readonly=False, own_space="niklas")
    assert payload["body"] == "<b>roh</b>"


def test_item_to_json_due_is_iso_date_or_none():
    assert item_to_json(_item(due=None), readonly=False, own_space="niklas")["due"] is None
    assert (
        item_to_json(_item(due=date(2026, 9, 1)), readonly=False, own_space="niklas")["due"]
        == "2026-09-01"
    )


def test_item_to_json_includes_share_fields_and_shared_flag():
    own = item_to_json(_item(space="niklas"), readonly=False, own_space="niklas")
    assert own["folder"] == ""
    assert own["visibility"] == "private"
    assert own["share_read"] == []
    assert own["share_write"] == []
    assert own["shared"] is False

    foreign = item_to_json(
        _item(space="fabian", folder="a", visibility="human", share_read=["niklas"]),
        readonly=True, own_space="niklas",
    )
    assert foreign["folder"] == "a"
    assert foreign["visibility"] == "human"
    assert foreign["share_read"] == ["niklas"]
    assert foreign["shared"] is True


def test_summary_to_json_has_no_snippet_pop_but_has_readonly():
    s = ItemSummary(
        id="itm_deadbeef", space="niklas", type="note", title="Test", status="active",
        due=None, tags=[], links=[], created=NOW, updated=NOW, version=1, snippet="...",
    )
    payload = summary_to_json(s, own_space="niklas", readonly=False)
    assert payload["readonly"] is False
    assert payload["snippet"] == "..."
    assert payload["shared"] is False


def test_summary_to_json_keeps_snippet_by_default():
    s = ItemSummary(
        id="itm_deadbeef", space="niklas", type="note", title="Test", status="active",
        due=None, tags=[], links=[], created=NOW, updated=NOW, version=1, snippet="...",
    )
    payload = summary_to_json(s, own_space="niklas", readonly=False)
    assert payload["snippet"] == "..."


def test_summary_to_json_omits_snippet_key_when_disabled():
    s = ItemSummary(
        id="itm_deadbeef", space="fabian", type="note", title="Test", status="active",
        due=None, tags=[], links=[], created=NOW, updated=NOW, version=1, snippet="...",
    )
    payload = summary_to_json(s, own_space="niklas", readonly=True, include_snippet=False)
    assert "snippet" not in payload


def test_search_to_json_wraps_pre_serialized_items():
    own = summary_to_json(
        ItemSummary(
            id="itm_1", space="niklas", type="note", title="Eigen", status="active", due=None,
            tags=[], links=[], created=NOW, updated=NOW, version=1, snippet="...",
        ),
        own_space="niklas", readonly=False,
    )
    foreign = summary_to_json(
        ItemSummary(
            id="itm_2", space="fabian", type="note", title="Fremd", status="active", due=None,
            tags=[], links=[], created=NOW, updated=NOW, version=1, snippet="...",
        ),
        own_space="niklas", readonly=True,
    )
    payload = search_to_json([own, foreign], total=2, limit=50, offset=0)
    by_id = {i["id"]: i for i in payload["items"]}
    assert by_id["itm_1"]["readonly"] is False
    assert by_id["itm_1"]["shared"] is False
    assert by_id["itm_2"]["readonly"] is True
    assert by_id["itm_2"]["shared"] is True
    assert payload["total"] == 2


def test_space_to_json_marks_own_space():
    assert space_to_json(
        SpaceInfo(name="niklas", item_count=3), own_space="niklas", writable=True
    )["own"] is True
    assert space_to_json(
        SpaceInfo(name="fabian", item_count=1), own_space="niklas", writable=False
    )["own"] is False


def test_space_to_json_reports_writable_independently_of_own():
    # A shared (non-own) space can be writable via a .share.yml grant -- "own" and "writable"
    # are different questions (found live, 2026-08-13: the UI badged every non-own space
    # read-only regardless of an actual write grant).
    payload = space_to_json(
        SpaceInfo(name="shared", item_count=0), own_space="niklas", writable=True
    )
    assert payload["own"] is False
    assert payload["writable"] is True


def test_space_to_json_includes_members_and_folders():
    payload = space_to_json(
        SpaceInfo(name="fabian", item_count=1, members=("niklas",), folders=("projekte",)),
        own_space="niklas",
        writable=False,
    )
    assert payload["members"] == ["niklas"]
    assert payload["folders"] == ["projekte"]
