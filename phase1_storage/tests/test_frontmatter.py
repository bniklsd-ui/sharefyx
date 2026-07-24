import pytest

from storage.frontmatter import FrontmatterError, parse, serialize

FIXTURES = [
    pytest.param(
        "---\n"
        "id: itm_a1b2c3d4\n"
        "space: nikinger\n"
        "type: task\n"
        "title: Kühlschrank prüfen äöüß\n"
        "status: open\n"
        "due: 2026-08-02\n"
        "tags:\n"
        "- infra\n"
        "- mcp\n"
        "links:\n"
        "- itm_9f8e7d6c\n"
        "created: 2026-07-24T18:20:00Z\n"
        "updated: 2026-07-24T18:20:00Z\n"
        "version: 4\n"
        "custom_field: bleibt erhalten\n"
        "---\n"
        "Zeile eins.\n"
        "\n"
        "Zweite Zeile mit Umlauten: äöüß.\n",
        id="umlaute-mehrzeilig-unbekanntes-feld",
    ),
    pytest.param(
        "---\n"
        "id: itm_deadbeef\n"
        "space: nikinger\n"
        "type: note\n"
        "title: Leer\n"
        "status: active\n"
        "tags: []\n"
        "links: []\n"
        "created: 2026-07-24T18:20:00Z\n"
        "updated: 2026-07-24T18:20:00Z\n"
        "version: 1\n"
        "---\n",
        id="leerer-body",
    ),
]


@pytest.mark.parametrize("text", FIXTURES)
def test_roundtrip_is_byte_identical(text):
    fields, body = parse(text)
    assert serialize(fields, body) == text


def test_parse_preserves_field_order():
    text = "---\nzed: 1\nalpha: 2\nmid: 3\n---\nbody\n"
    fields, _ = parse(text)
    assert list(fields.keys()) == ["zed", "alpha", "mid"]


def test_parse_keeps_date_like_values_as_strings():
    text = "---\ndue: 2026-08-02\ncreated: 2026-07-24T18:20:00Z\n---\nbody\n"
    fields, _ = parse(text)
    assert fields["due"] == "2026-08-02"
    assert fields["created"] == "2026-07-24T18:20:00Z"


def test_parse_rejects_missing_frontmatter():
    with pytest.raises(FrontmatterError):
        parse("kein frontmatter hier\n")


def test_parse_rejects_unclosed_frontmatter():
    with pytest.raises(FrontmatterError):
        parse("---\nid: itm_deadbeef\nbody ohne schliessendes delimiter\n")
