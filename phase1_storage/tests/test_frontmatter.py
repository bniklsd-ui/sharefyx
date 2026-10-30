import pytest

from storage.frontmatter import FrontmatterError, inline_text, normalize_item_fields, parse, serialize

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


# -- P10.5 Block 15.2 (Ultra-Review B20): CRLF und kaputtes YAML ----------------------------


def test_parse_accepts_crlf_delimiters():
    """B20: eine unter Windows gespeicherte Datei ist Frontmatter wie jede andere. Der Body
    behaelt seine Zeilenenden byteweise — `parse()` normalisiert nichts."""
    fields, body = parse("---\r\nid: itm_a1b2c3d4\r\ntitle: Ä\r\n---\r\nZeile 1\r\nZeile 2\r\n")
    assert fields == {"id": "itm_a1b2c3d4", "title": "Ä"}
    assert body == "Zeile 1\r\nZeile 2\r\n"


def test_parse_wraps_yaml_error_as_frontmatter_error():
    """15.2: `yaml.YAMLError` ist kein `ValueError` — ohne Uebersetzung lief kaputtes YAML an
    jedem `except ValueError` im Kern vorbei."""
    with pytest.raises(FrontmatterError):
        parse("---\ntitle: [kaputt\n---\nx")


@pytest.mark.parametrize("wert, text", [
    (2026, "2026"), (1.0, "1.0"), (True, "true"), (["a", "b"], "[a, b]"), ({"a": 1}, "{a: 1}"),
    (None, ""), ("x", "x"), (["2026-08-02"], "[2026-08-02]"), (["Ä ö"], "[Ä ö]"),
])
def test_inline_text_reads_like_the_yaml(wert, text):
    """15.3 (B5): ein Nicht-String wird zu dem Text, der im YAML stand — nicht zu Pythons `str()`
    (`True`, `['a', 'b']`). Kein `...`-Dokumentende, keine Timestamp-Quotes."""
    assert inline_text(wert) == text


def test_normalize_item_fields_leaves_share_fields_and_input_alone():
    """15.3: `share_read: fabian` bleibt roh (eine Koerzion waere eine Rechteerweiterung ohne
    Re-Auth), und `parse()`s Ergebnis wird nicht veraendert — `_write_version_only` schreibt es
    zurueck, wie der Mensch es schrieb."""
    roh = {"title": 5, "tags": "a", "links": None, "share_read": "fabian"}
    assert normalize_item_fields(roh) == {
        "title": "5", "tags": ["a"], "links": [], "share_read": "fabian",
    }
    assert roh == {"title": 5, "tags": "a", "links": None, "share_read": "fabian"}
