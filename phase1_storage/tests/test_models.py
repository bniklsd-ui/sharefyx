from datetime import datetime, timezone

from storage.models import (
    DEFAULT_VISIBILITY,
    VISIBILITY_VALUES,
    IndexStats,
    Item,
    ItemSummary,
    SearchResult,
    SpaceInfo,
)


def _now():
    return datetime(2026, 7, 24, 18, 20, tzinfo=timezone.utc)


def test_item_defaults():
    item = Item(
        id="itm_a1b2c3d4",
        space="nikinger",
        type="task",
        title="Kühlschrank prüfen",
        status="open",
        created=_now(),
        updated=_now(),
        version=1,
    )
    assert item.body == ""
    assert item.due is None
    assert item.tags == []
    assert item.links == []
    assert item.extra == {}
    assert item.folder == ""
    assert item.visibility == DEFAULT_VISIBILITY
    assert item.share_read == []
    assert item.share_write == []


def test_visibility_values_and_default():
    assert VISIBILITY_VALUES == frozenset({"private", "human"})
    assert DEFAULT_VISIBILITY == "private"
    assert DEFAULT_VISIBILITY in VISIBILITY_VALUES


def test_search_result_holds_summaries_not_full_items():
    summary = ItemSummary(
        id="itm_a1b2c3d4",
        space="nikinger",
        type="task",
        title="Kühlschrank prüfen",
        status="open",
        created=_now(),
        updated=_now(),
        version=1,
        snippet="Erste 160 Zeichen des Bodies...",
    )
    result = SearchResult(items=[summary], total=1, limit=50, offset=0)
    assert result.items[0].snippet
    assert not hasattr(result.items[0], "body")


def test_space_info_and_index_stats_construct():
    info = SpaceInfo(name="nikinger", item_count=3)
    assert info.members == ()
    assert info.folders == ()
    SpaceInfo(name="fabian", item_count=1, members=("dritter",), folders=("projekte",))
    IndexStats(items_indexed=3, duration_seconds=0.02)
