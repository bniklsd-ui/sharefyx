"""Wächter für den Live-Editor (P10.5 Block 11, Schritt 11.3 — ED-1, ED-5).

**Was dieser Wächter prüft:** dass der Editor **einen** Text hat und **einen** Editor:

1. **Kein direkter Zugriff auf `editorTextareaEl.value`** außerhalb der vier Helfer
   (`getBody`, `setBody`, `_textUndAuswahl`, `_ersetze`). Das ist die ganze Fehlerklasse:
   im Live-Modus trägt CodeMirror den Text, die Textarea den **alten** — wer direkt liest,
   liest etwas Falsches (der „geänderte Editor" aus P10.5-S wäre still falsch).
2. **Kein Moduswechsel**: `setEditorMode` ist weg, `setRawMode(on)` ist da, und der Schalter
   heißt „Rohtext".
3. **Die Vorgabe beim Öffnen ist der Live-Modus** (`opts.mode === "raw"` ist die einzige
   Ausnahme).
4. **Der Editor wird aus der Textarea erzeugt** (`CodeMirror.fromTextArea`) — mit dem
   Markdown-Modus und `lineWrapping`.

**Was er ausdrücklich nicht prüft:** das Verhalten im Browser (der Editor lädt, man tippt,
der Cursor sitzt). Dafür sind die Proben des Blocks da (Playwright, Wegwerf-Instanz).
"""
from __future__ import annotations

import re
from pathlib import Path

REPO_ROOT = Path(__file__).resolve().parents[2]
JS = REPO_ROOT / "phase5_ui/webui/static/js"
EDITOR = JS / "editor.js"
APP_HTML = REPO_ROOT / "phase5_ui/webui/static/app.html"

#: Die Helfer, in denen ein direkter Zugriff erlaubt ist.
#:
#: `_editorBereit` steht mit drin, weil es genau **einmal** zulaesst: beim Uebernehmen des
#: Textes von der Textarea in den Live-Editor. Das passiert **vor** `cm` gesetzt wird — danach
#: waere `getBody()` bereits der Editor, und der Text der Textarea waere der falsche.
ERLAUBT = ("getBody", "setBody", "_textUndAuswahl", "_ersetze", "_editorBereit")


def _editor() -> str:
    return EDITOR.read_text(encoding="utf-8")


def _funktionskoerper(text: str, funktion: str) -> str:
    """Der Rumpf einer Funktion — ohne den Rest der Datei."""
    start = text.index("function " + funktion)
    tiefe, i = 0, text.index("{", start)
    beginn = i
    while True:
        if text[i] == "{":
            tiefe += 1
        elif text[i] == "}":
            tiefe -= 1
            if tiefe == 0:
                return text[beginn:i + 1]
        i += 1


def test_no_direct_textarea_value_access_outside_the_helpers():
    """**Die eine Regel des Umbaus.** Wer direkt `editorTextareaEl.value` liest oder
    schreibt, liest im Live-Modus den alten Text."""
    text = _editor()
    zeilen = text.split("\n")
    erlaubte_zeilen = set()
    for funktion in ERLAUBT:
        rumpf = _funktionskoerper(text, funktion)
        for zeile in rumpf.split("\n"):
            erlaubte_zeilen.add(zeile)
    verdaechtig = []
    for nummer, zeile in enumerate(zeilen, start=1):
        if "editorTextareaEl.value" not in zeile:
            continue
        if zeile.strip().startswith("//"):
            # Ein **Kommentar** erwaehnt den Ausdruck — er greift nicht darauf zu.
            continue
        if zeile in erlaubte_zeilen:
            continue
        verdaechtig.append(f"Zeile {nummer}: {zeile.strip()}")
    assert not verdaechtig, (
        "direkte Zugriffe auf `editorTextareaEl.value` ausserhalb der Helfer "
        f"{ERLAUBT}: " + "; ".join(verdaechtig)
    )


def test_the_body_goes_through_get_and_set():
    """`currentFormValues()` liest ueber `getBody()`, das Oeffnen schreibt ueber `setBody()`."""
    text = _editor()
    assert "body: getBody()," in text
    assert "setBody(item.body);" in text
    assert "setBody(draft.body);" in text


def test_there_is_no_mode_switch_any_more():
    """ED-1: **kein Moduswechsel.** `setEditorMode` ist weg, `setRawMode(on)` ist da."""
    text = _editor()
    assert "function setEditorMode" not in text
    assert "setEditorMode(" not in text, "es wird noch der alte Moduswechsel gerufen"
    assert "function setRawMode(on)" in text


def test_the_switch_is_called_rohtext_and_toggles_the_raw_mode():
    """Der Schalter heisst „Rohtext" (nicht „Vorschau") und schaltet den Rohmodus."""
    html = APP_HTML.read_text(encoding="utf-8")
    assert 'id="toggle-preview"' in html
    assert ">Rohtext</button>" in html
    text = _editor()
    assert "setRawMode(state.mode !== \"raw\");" in text


def test_the_live_mode_is_the_default_when_opening():
    """Die Vorgabe beim Oeffnen ist der Live-Modus; nur ein ausdrueckliches „raw" schaltet
    auf den Rohtext."""
    text = _editor()
    assert 'setRawMode(opts.mode === "raw");' in text


def test_the_editor_is_created_from_the_textarea_with_the_markdown_mode():
    """`fromTextArea` mit dem Markdown-Modus und `lineWrapping` — und der Notausgang bleibt
    die Textarea (der Editor ersetzt sie, statt einen zweiten Text zu fuehren)."""
    text = _editor()
    assert "CodeMirror.fromTextArea(editorTextareaEl" in text
    assert 'mode: { name: "markdown", highlightFormatting: true }' in text
    assert "lineWrapping: true" in text


def test_the_live_editor_reports_its_changes_like_the_textarea():
    """Eine Aenderung, ein Ort: `_editorGeaendert()` (Version + Entwurf) — der Live-Editor
    feuert „change", die Textarea „input"."""
    text = _editor()
    assert 'cm.on("change", _editorGeaendert);' in text
    rumpf = _funktionskoerper(text, "_editorGeaendert")
    assert "updateVersionBand()" in rumpf
    assert "saveDraft()" in rumpf
    assert 'input.addEventListener("input", _editorGeaendert);' in text


def test_inserting_at_the_cursor_uses_replace_selection_in_the_live_editor():
    """Der Plan (Schritt 11.3) nennt `cm.replaceSelection` ausdruecklich."""
    text = _editor()
    rumpf = _funktionskoerper(text, "insertAtCursor")
    assert "cm.replaceSelection(text);" in rumpf


def test_the_formatting_helpers_work_in_both_editors():
    """Die Formatierhilfen gehen ueber `_textUndAuswahl()`/`_ersetze()` — **ein** Code fuer
    Live-Editor und Notausgang."""
    text = _editor()
    rumpf = _funktionskoerper(text, "wrapSelection")
    assert "_textUndAuswahl()" in rumpf
    assert "_ersetze(" in rumpf
    rumpf2 = _funktionskoerper(text, "insertLinePrefix")
    assert "_textUndAuswahl()" in rumpf2
    assert "_ersetze(" in rumpf2
