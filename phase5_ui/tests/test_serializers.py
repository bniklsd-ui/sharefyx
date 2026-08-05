"""`webui/serializers.py` direkt getestet (Plan §3.2, §5 Step 5) — reine Funktionen, kein Store,
kein HTTP."""
from __future__ import annotations

from datetime import date, datetime, timezone

from storage.models import Item, ItemSummary, SearchResult, SpaceInfo

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
    payload = item_to_json(_item(), readonly=False)
    assert payload["format"] == "markdown"
    assert payload["readonly"] is False


def test_item_to_json_reads_format_from_extra():
    payload = item_to_json(_item(extra={"format": "plain"}), readonly=True)
    assert payload["format"] == "plain"
    assert payload["extra"] == {"format": "plain"}
    assert payload["readonly"] is True


def test_item_to_json_body_is_plain_text_never_rendered():
    payload = item_to_json(_item(body="<b>roh</b>"), readonly=False)
    assert payload["body"] == "<b>roh</b>"


def test_item_to_json_due_is_iso_date_or_none():
    assert item_to_json(_item(due=None), readonly=False)["due"] is None
    assert item_to_json(_item(due=date(2026, 9, 1)), readonly=False)["due"] == "2026-09-01"


def test_summary_to_json_has_no_readonly_field():
    s = ItemSummary(
        id="itm_deadbeef", space="niklas", type="note", title="Test", status="active",
        due=None, tags=[], links=[], created=NOW, updated=NOW, version=1, snippet="...",
    )
    assert "readonly" not in summary_to_json(s)


def test_search_to_json_marks_foreign_items_readonly():
    own = ItemSummary(
        id="itm_1", space="niklas", type="note", title="Eigen", status="active", due=None,
        tags=[], links=[], created=NOW, updated=NOW, version=1, snippet="...",
    )
    foreign = ItemSummary(
        id="itm_2", space="fabian", type="note", title="Fremd", status="active", due=None,
        tags=[], links=[], created=NOW, updated=NOW, version=1, snippet="...",
    )
    result = SearchResult(items=[own, foreign], total=2, limit=50, offset=0)
    payload = search_to_json(result, own_space="niklas")
    by_id = {i["id"]: i for i in payload["items"]}
    assert by_id["itm_1"]["readonly"] is False
    assert by_id["itm_2"]["readonly"] is True
    assert payload["total"] == 2


def test_space_to_json_marks_own_space():
    assert space_to_json(SpaceInfo(name="niklas", item_count=3), own_space="niklas")["own"] is True
    assert space_to_json(SpaceInfo(name="fabian", item_count=1), own_space="niklas")["own"] is False
