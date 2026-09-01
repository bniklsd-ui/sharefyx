"""Phase 8 Block B Step B1 (Plan §3 P8-M, achte P1-Contract-Oeffnung).

Tests fuer `storage.linkscan.extract_item_refs`. Rein, kein I/O, kein tmp_path noetig.
"""
from __future__ import annotations

from storage.linkscan import ITEM_REF_RE, extract_item_refs


# --- ITEM_REF_RE: Alphabet-Garantie -------------------------------------------------------

def test_item_ref_re_matches_canonical_id():
    assert ITEM_REF_RE.fullmatch("itm_a1b2c3d4")
    assert ITEM_REF_RE.fullmatch("itm_00000000")
    assert ITEM_REF_RE.fullmatch("itm_deadbeef")


def test_item_ref_re_is_case_sensitive_lower():
    """Item-IDs sind per Definition lower-hex (files.py ITEM_ID_RE: `[0-9a-f]`).
    Ein `itm_DEADBEEF` ist nach Konvention KEINE gueltige ID, der Body-Regex matcht es NICHT."""
    assert not ITEM_REF_RE.search("itm_DEADBEEF")
    assert not ITEM_REF_RE.fullmatch("itm_DEADBEEF")


def test_item_ref_re_rejects_too_short_or_too_long():
    assert not ITEM_REF_RE.fullmatch("itm_a1b2c3d")        # 7 hex
    assert not ITEM_REF_RE.fullmatch("itm_a1b2c3d4e")      # 9 hex
    assert not ITEM_REF_RE.fullmatch("itm_")               # leer
    assert not ITEM_REF_RE.fullmatch("itm_zzzzzzzz")       # non-hex


def test_item_ref_re_respects_word_boundaries():
    """Praefix ohne Wortgrenze (z.B. `fooitm_...`) matcht NICHT -- sonst wuerde jedes Vorkommen
    der acht Hex-Zeichen im Korpus mitmischen, das ist die Begruendung fuer `\b`.

    Bindestriche und Punkte ZAEHLEN als Wortgrenze (sie sind non-word in regex-\\b), deshalb
    matcht `pre-itm_a1b2c3d4-post` sehr wohl -- dokumentiert, kein Test, weil der Fall in
    natuerlichem Markdown praktisch nicht vorkommt (Backlinks stehen in eigenen Saetzen)."""
    assert not ITEM_REF_RE.search("fooitm_a1b2c3d4")
    assert ITEM_REF_RE.search("pre itm_a1b2c3d4 post")
    assert ITEM_REF_RE.search("(itm_a1b2c3d4)")  # Klammern sind Wortgrenze


# --- extract_item_refs: Verhalten ---------------------------------------------------------

def test_extract_empty_body():
    assert extract_item_refs("") == []


def test_extract_no_references():
    assert extract_item_refs("Ein Body ohne jede Referenz, einfach Prosa.") == []


def test_extract_single_naked_id():
    assert extract_item_refs("Siehe itm_a1b2c3d4 fuer Details.") == ["itm_a1b2c3d4"]


def test_extract_single_href_form():
    """`#item/itm_...`-Hrefs enthalten das Token -- ein Regex deckt beide Body-Formen ab."""
    assert extract_item_refs("Link: [Titel](#item/itm_a1b2c3d4)") == ["itm_a1b2c3d4"]


def test_extract_multiple_distinct_ids_in_order():
    body = "Erst itm_11111111, dann itm_22222222, dann itm_33333333."
    assert extract_item_refs(body) == ["itm_11111111", "itm_22222222", "itm_33333333"]


def test_extract_dedupes_repeated_id_keeps_first_occurrence():
    """Dieselbe ID zweimal -> genau ein Listeneintrag, in Reihenfolge des ERSTEN Auftretens."""
    body = "itm_a1b2c3d4 oben, und nochmal itm_a1b2c3d4 unten."
    assert extract_item_refs(body) == ["itm_a1b2c3d4"]


def test_extract_dedupes_across_href_and_naked_form():
    """Eine ID, einmal als Href und einmal nackt -> trotzdem nur ein Eintrag."""
    body = "Siehe [T](https://...#item/itm_a1b2c3d4) und itm_a1b2c3d4 selbst."
    assert extract_item_refs(body) == ["itm_a1b2c3d4"]


def test_extract_mixed_order_keeps_first_seen():
    body = "itm_aaaaaaaa und itm_bbbbbbbb und nochmal itm_aaaaaaaa und itm_cccccccc."
    assert extract_item_refs(body) == ["itm_aaaaaaaa", "itm_bbbbbbbb", "itm_cccccccc"]


def test_extract_inside_code_block_still_matches():
    """Keine Markdown-Semantik: eine ID in einem Code-Block ist eine gemeinte Referenz."""
    body = "```\nitm_a1b2c3d4\n```"
    assert extract_item_refs(body) == ["itm_a1b2c3d4"]


def test_extract_does_not_match_invalid_forms():
    """Zu kurze / zu lange IDs und Grossbuchstaben werden ignoriert, nicht zur Not repariert."""
    body = "itm_a itm_a1b2c3 itm_a1b2c3d4e itm_DEADBEEF itm_zzzzzzzz und itm_a1b2c3d4."
    assert extract_item_refs(body) == ["itm_a1b2c3d4"]


def test_extract_handles_adjacent_ids_without_separator():
    """Aneinandergereihte IDs ohne Whitespace -- ZIFFERN-BUCHSTABEN- bzw. ZIFFERN-BUCHSTABEN-
    Uebergaenge ziehen KEINE Wortgrenze (`\b` greift nur an non-word/word-Uebergaengen).
    Eine `4itm_e` Sequenz matcht daher weder die erste noch die zweite ID als ganze.

    Realer Fall tritt nie auf (zwei gueltige IDs ohne Trenner wuerden 16+ Hex-Zeichen am
    Stueck ergeben, kein Mensch schreibt das), aber das Verhalten ist dokumentiert und
    sinnvoll: ein Body, der zwei Referenzen will, hat dazwischen einen Separator."""
    assert extract_item_refs("itm_a1b2c3d4itm_e5f6a7b8") == []
    assert extract_item_refs("itm_a1b2c3d4 itm_e5f6a7b8") == ["itm_a1b2c3d4", "itm_e5f6a7b8"]
