r"""Wächter für die Format-Konvention Stufe 2 (P10.5 Block 11, Schritt 11.6 — ED-3).

**Was der Plan verlangt (Plan §Block 11, Schritt 11.6):**

- `markdown.js`: Inline-Regel `\[([^\]\n]+)\]\{((?:\.[a-z]+)(?: \.[a-z]+)?)\}` — **nur
  bekannte Klassen** (höchstens eine Farbe + eine Größe) → `<span class="md-c-rot
  md-s-gross">…</span>`, **sonst wörtlich**. Block: `::: {.zentriert}` … `:::` →
  `<div class="md-a-zentriert">` + rekursiv `markdownToHtml(inner)`; keine Verschachtelung;
  ein fehlendes Ende → wörtlich.
- Sanitizer: `span` und `div` mit `class` **nur aus einer festen Menge** (Muster
  `ALLOWED_CELL_CLASSES`).
- Editor: Werkzeugleiste mit Farbe, Größe und Ausrichtung; ein CM5-Overlay (`cm.addOverlay`)
  färbt `[…]{.rot}` schon beim Schreiben.
- MCP: ein Satz `_FORMAT_HINT` in `tools.py`, **wörtlich identisch** an allen fünf Werkzeugen,
  die einen Body schreiben.

**Vier Fehlerklassen, die diese Datei bewacht:**

1. **Eine unbekannte Klasse darf keine Klasse werden.** `.style` ist **wörtlich** — der
   Renderer darf keine Klasse erfinden, die es nicht gibt. Das ist eine **Entscheidung des
   Codes**; ein Fehler darin wäre still (die Ausgabe sähe „fast richtig" aus).
2. **Der Sanitizer muss die Klassen filtern.** Eine Klasse aus dem freien Text wäre ein
   freier CSS-Hook. Also: `span`/`div` sind erlaubt, ihre `class` nur aus der festen Menge.
3. **Im Code wird nichts formatiert.** `` `[x]{.rot}` `` ist ein Codespan — dort greift
   **keine** Formatierung (das ist zugleich die Korrektur eines Alt-Fehlers: `**fett**` in
   einem Codespan wurde früher **fett**).
4. **Die fünf MCP-Werkzeuge tragen denselben Satz.** Zwei Wortlautvarianten wären zwei
   Definitionen derselben Regel (dieselbe Begründung wie bei `_ASSIGNEE_HINT`).

**Der Beleg (nicht der Quelltext) entscheidet.** Die Probe `p105_b11_markdown_probe.py` misst
an der Wegwerf-Instanz im echten Browser (neun Zellen) und liest dasselbe Item über den
**MCP** (`get_item` → Rohtext). Der **Gegenlauf** liefert die `markdown.js` **ohne** die
wörtlich-Fallback aus und muss **genau die Zelle** „unbekannte Klasse wörtlich" rot machen.
"""
from __future__ import annotations

import json
import re
from pathlib import Path

REPO_ROOT = Path(__file__).resolve().parents[2]
PROBE_DIR = REPO_ROOT / "phase10_5_finishing" / "probes"
GRUEN = PROBE_DIR / "p105_b11_markdown.json"
GEGENLAUF = PROBE_DIR / "p105_b11_markdown_gegenlauf.json"
MARKDOWN_JS = REPO_ROOT / "phase5_ui" / "webui" / "static" / "js" / "markdown.js"
EDITOR_JS = REPO_ROOT / "phase5_ui" / "webui" / "static" / "js" / "editor.js"
APP_HTML = REPO_ROOT / "phase5_ui" / "webui" / "static" / "app.html"
APP_CSS = REPO_ROOT / "phase5_ui" / "webui" / "static" / "app.css"
TOOLS_PY = REPO_ROOT / "phase2_mcp" / "mcpserver" / "tools.py"

#: Die Zelle, die der Gegenlauf brechen muss: die **unbekannte Klasse** bleibt wörtlich.
GEGENLAUF_ZELLE = "unbekannte_klasse_woertlich"

#: Das Vokabular — **eine** Quelle: `markdown.js` (der Renderer), `app.html` (die
#: Werkzeugleiste) und die Werkzeugbeschreibung im MCP (der LLM) müssen dasselbe kennen.
FARBEN = ("rot", "blau", "gruen", "gelb")
GROESSEN = ("klein", "normal", "gross")
AUSRICHTUNGEN = ("links", "zentriert", "rechts")

#: Die fünf Werkzeuge, die einen Body schreiben (P10.5-56).
SCHREIB_WERKZEUGE = (
    "create_item", "update_item", "append_to_item", "append_to_items", "patch_item",
)


def _text(datei: Path) -> str:
    return datei.read_text(encoding="utf-8")


def _befund(datei: Path) -> dict:
    assert datei.exists(), f"der Beleg fehlt: {datei}"
    return json.loads(datei.read_text(encoding="utf-8"))


# -- Der Beleg --------------------------------------------------------------------------------


def test_the_green_report_has_all_cells_green():
    befund = _befund(GRUEN)
    assert befund.get("alle_gruen") is True, (
        "der grüne Beleg meldet nicht 'alle_gruen' — die Datei ist kein Beleg"
    )
    zellen = befund.get("zellen") or {}
    assert zellen, "der Beleg traegt keine Zellen"
    rot = [k for k, v in zellen.items() if not v.get("ok")]
    assert not rot, f"rote Zellen im grünen Beleg: {rot}"


def test_the_report_carries_the_nine_named_cells():
    zellen = _befund(GRUEN).get("zellen") or {}
    erwartet = {
        "farbe", "groesse", "farbe_und_groesse", "unbekannte_klasse_woertlich",
        "ausrichtung", "html_woertlich", "codespan_unformatiert", "werkzeugleiste",
        "mcp_get_item_rohtext",
    }
    assert erwartet <= set(zellen), f"fehlende Zellen: {sorted(erwartet - set(zellen))}"


def test_the_counter_run_breaks_exactly_the_literal_cell():
    befund = _befund(GRUEN).get("gegenlauf") or {}
    assert sorted(befund.get("gebrochen") or []) == [GEGENLAUF_ZELLE], (
        "der Gegenlauf muss genau die Zelle 'unbekannte Klasse wörtlich' brechen — "
        f"gebrochen: {befund.get('gebrochen')}"
    )
    assert befund.get("bricht_genau_die_erwartete") is True
    assert befund.get("die_anderen_bleiben_gruen") is True, (
        "der Gegenlauf hat nebenbei etwas anderes kaputtgemacht — dann misst er nicht"
    )


def test_both_variants_were_actually_delivered():
    """Ohne den Beleg „welche Datei lief" ist jede Zahl aus dem Gegenlauf wertlos."""
    belege = _befund(GRUEN).get("varianten_belege") or {}
    assert set(belege) == {"original", "gegenlauf"}
    assert belege["original"]["ausgeliefert"] == "original"
    assert belege["gegenlauf"]["ausgeliefert"] == "gegenlauf"


def test_the_mcp_returns_the_raw_text():
    zelle = (_befund(GRUEN).get("zellen") or {}).get("mcp_get_item_rohtext") or {}
    assert zelle.get("ok") is True
    assert zelle.get("gemessen", {}).get("fehlend") == [], (
        "der MCP hat den Text nicht woertlich zurueckgegeben"
    )


# -- Der Quelltext: die Regeln ----------------------------------------------------------------


def test_the_vocabulary_lives_in_one_place():
    """`markdown.js` ist die Quelle — die Werkzeugleiste und der MCP muessen dasselbe
    kennen, sonst bietet der Editor etwas an, das der Renderer nicht kennt."""
    text = _text(MARKDOWN_JS)
    for name in FARBEN + GROESSEN + AUSRICHTUNGEN:
        assert f'"{name}"' in text, f"das Vokabular kennt {name} nicht"
    for klasse in ("md-c-rot", "md-s-klein", "md-a-zentriert"):
        assert klasse in text, f"die Klasse {klasse} fehlt"
    assert "export var FORMAT_VOKABULAR" in text, (
        "das Vokabular muss exportiert werden — der Editor laedt dieselbe Liste"
    )


def test_an_unknown_class_stays_literal():
    """Der Kern der Konvention: `.style` ist **woertlich**. Ohne diesen `return null`
    wuerde der Renderer eine Klasse erfinden, die es nicht gibt."""
    text = _text(MARKDOWN_JS)
    assert re.search(r"return null;(\s*//\s*unbekannte Klasse:)", text), (
        "die wörtlich-Fallback fuer unbekannte Klassen fehlt"
    )


def test_the_sanitizer_filters_the_classes():
    """`span`/`div` duerfen durch — ihre `class` nur aus der festen Menge."""
    text = _text(MARKDOWN_JS)
    assert '"SPAN", "DIV"' in text, "span und div sind nicht erlaubt"
    assert re.search(r"SPAN:\s*new Set\(\[\"class\"\]\)", text)
    assert re.search(r"DIV:\s*new Set\(\[\"class\"\]\)", text)
    assert "ALLOWED_FORMAT_CLASSES" in text, (
        "die Klassen der Format-Konvention brauchen eine feste Menge — ein freier "
        "Klassenname waere ein freier CSS-Hook"
    )
    assert re.search(r"ALLOWED_FORMAT_CLASSES\.has\(k\)", text), (
        "die Klassen werden nicht gefiltert"
    )


def test_the_inline_rule_comes_before_the_links():
    """Der Plan sagt es ausdruecklich: die Inline-Regel steht **vor** den Links."""
    text = _text(MARKDOWN_JS)
    regel = text.find("FORMAT_INLINE_RE, function")
    links = text.find("href")
    assert regel != -1, "die Inline-Regel fehlt"
    assert links != -1
    assert regel < links, "die Inline-Regel muss vor den Links stehen"


def test_code_spans_are_protected():
    """Im Codespan wird **nichts** formatiert — dort greift keine Regel."""
    text = _text(MARKDOWN_JS)
    assert re.search(r"split\(/\(`\[\^`\]\+\`\)/g\)", text), (
        "die Codespans werden nicht ausgeschnitten — die Format-Regel liefe in sie hinein"
    )


def test_the_editor_has_the_overlay_and_the_three_fields():
    editor = _text(EDITOR_JS)
    assert "cm.addOverlay" in editor, "der CM5-Overlay fehlt"
    assert "_formatOverlayToken" in editor
    html = _text(APP_HTML)
    for feld in ("format-farbe", "format-groesse", "format-ausrichtung"):
        assert f'id="{feld}"' in html, f"das Feld {feld} fehlt in der Werkzeugleiste"
    for name in FARBEN + GROESSEN + AUSRICHTUNGEN:
        assert f'value="{name}"' in html, f"die Option {name} fehlt in der Werkzeugleiste"


def test_the_css_carries_the_nine_classes():
    css = _text(APP_CSS)
    for klasse in (
        "md-c-rot", "md-c-blau", "md-c-gruen", "md-c-gelb",
        "md-s-klein", "md-s-normal", "md-s-gross",
        "md-a-links", "md-a-zentriert", "md-a-rechts",
    ):
        assert f".{klasse} " in css or f".{klasse} {{" in css, f"die Klasse {klasse} fehlt"


def test_the_mcp_hint_exists_and_names_the_vocabulary():
    text = _text(TOOLS_PY)
    assert "_FORMAT_HINT = (" in text, "der _FORMAT_HINT fehlt"
    for name in FARBEN + GROESSEN + AUSRICHTUNGEN:
        assert f".{name}" in text, f"der _FORMAT_HINT nennt {name} nicht"
