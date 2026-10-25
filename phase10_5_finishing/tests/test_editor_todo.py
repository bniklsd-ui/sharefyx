"""Wächter für die To-do-Kästchen (P10.5 Block 11, Schritt 11.5 — ED-2).

**Was der Plan verlangt (Plan §Block 11, Schritt 11.5):** `- [ ]`/`- [x]` am Zeilenanfang
werden im Live-Modus per `cm.markText(…, {replacedWith: <checkbox>})` ersetzt; ein Klick
schaltet **den Text im Puffer**. War der Editor **vor** dem Klick unveraendert, folgt sofort
`saveItem()` (mit der Snapshot-`version`, Hard Rule 3; ein Konflikt oeffnet den bestehenden
Dialog). War er **geaendert**, gehoert der Klick zur naechsten Speicherung. In der Lesesicht
(`markdown.js`) werden die Kaestchen **angezeigt und deaktiviert** — kein Schreibweg
ausserhalb des Editors.

**Drei Fehlerklassen, die diese Datei bewacht:**

1. **Der Klick muss den Text umschalten, nicht das DOM.** Ein Kaestchen, dessen `checked`
   man im Browser setzt, waere ein **zweiter** Zustand: der Server bekommt nichts, und der
   Text waere nicht mehr die Quelle. Der Wächter verlangt `cm.replaceRange(...)` mit
   `[ ]`/`[x]` — der Schreibpfad des Puffers.
2. **Der Schreibweg haengt an `version`.** `saveItem()` nimmt die Version aus dem
   Schnappschuss (`state.editingSnapshot.version`) — Hard Rule 3. Und der Klick speichert
   **nur dann sofort, wenn der Editor vorher sauber war**; sonst gehoert er zur naechsten
   Speicherung. Beides haengt an **einer** Zeile: `if (sauber) saveItem();`.
3. **Die Lesesicht darf keinen Schreibweg haben.** Der Sanitizer **erzwingt** `disabled` und
   `type="checkbox"` — erlauben waere nicht genug (fail-closed).

**Der Beleg (nicht der Quelltext) entscheidet.** Die Probe `p105_b11_todo_probe.py` misst
an der Wegwerf-Instanz im echten Browser: der Klick schaltet den Puffer, der Klick bei
sauberem Editor **schreibt** (die Version springt), der Klick bei geaendertem Editor
**nicht**, die Lesesicht zeigt **deaktivierte** Kaestchen, und der Rohmodus zeigt jedes
Zeichen. Der **Gegenlauf** liefert `editor.js` **ohne** die Zeile `if (sauber) saveItem();`
aus und muss **genau die Schreib-Zelle** rot machen — bricht er keine, misst er nichts; bricht
er zu viele, ist er unpräzise.
"""
from __future__ import annotations

import json
import re
from pathlib import Path

REPO_ROOT = Path(__file__).resolve().parents[2]
PROBE_DIR = REPO_ROOT / "phase10_5_finishing" / "probes"
GRUEN = PROBE_DIR / "p105_b11_todo.json"
GEGENLAUF = PROBE_DIR / "p105_b11_todo_gegenlauf.json"
EDITOR_JS = REPO_ROOT / "phase5_ui" / "webui" / "static" / "js" / "editor.js"
MARKDOWN_JS = REPO_ROOT / "phase5_ui" / "webui" / "static" / "js" / "markdown.js"
HEAD = REPO_ROOT / "phase10_5_finishing" / "CLAUDE.md"

#: Die Zelle, die der Gegenlauf brechen muss: das **Speichern** beim Klick auf einen
#: sauberen Editor. Alles andere bleibt grün — sonst waere der Gegenlauf kein Gegenlauf.
GEGENLAUF_ZELLEN = ("klick_schreibt_mit_version",)


def _befund(datei: Path) -> dict:
    assert datei.exists(), f"der Beleg fehlt: {datei}"
    return json.loads(datei.read_text(encoding="utf-8"))


def _zellen(befund: dict) -> dict[str, bool]:
    """Nur die **booleschen** Zellen — Messwerte sind keine Zellen."""
    return {k: v for k, v in befund.items() if isinstance(v, bool)}


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


def test_the_green_report_has_all_cells_green():
    bericht = _befund(GRUEN)
    assert bericht.get("alle_kriterien_erfuellt") is True, (
        "der grüne Beleg meldet nicht 'alle Kriterien erfüllt' — die Datei ist kein Beleg"
    )
    rot = [k for k, v in _zellen(bericht["befund"]).items() if not v]
    assert not rot, f"rote Zellen im grünen Beleg: {rot}"


def test_both_variants_were_really_delivered():
    """**Die Belegpflicht.** Die Gegenlauf-Fassung traegt eine Kennung
    (`window.__p105_todo_variante`), die der Browser **zurueckliest**. Ohne diesen Beleg
    waere jede Zahl aus dem Gegenlauf wertlos — die erste Fassung der Probe las die
    Kennung an der falschen Stelle (vor dem Laden des Editors) und meldete deshalb immer
    „original"."""
    varianten = _befund(GRUEN)["befund"]["varianten_belege"]
    assert varianten["normal"]["ausgeliefert"] == "original", (
        "der Normalfall muss die unveränderte Datei ausliefern"
    )
    assert varianten["gegenlauf"]["ausgeliefert"] == "gegenlauf", (
        "der Gegenlauf hat die gepatchte Datei **nicht** ausgeliefert — die Messung waere "
        "fuer die Katz"
    )


def test_the_counter_run_breaks_exactly_the_write_cell():
    bericht = _befund(GEGENLAUF)
    rot = sorted(k for k, v in _zellen(bericht["zellen"]).items() if not v)
    assert rot == sorted(GEGENLAUF_ZELLEN), (
        f"der Gegenlauf muss genau die Zelle {sorted(GEGENLAUF_ZELLEN)} brechen, "
        f"gebrochen wurde: {rot}"
    )


def test_the_two_reports_are_different_files():
    """Der Gegenlauf darf den grünen Beleg nicht überschreiben."""
    assert GRUEN != GEGENLAUF
    assert GRUEN.read_text(encoding="utf-8") != GEGENLAUF.read_text(encoding="utf-8")


def test_the_checkbox_is_a_mark_with_a_replaced_node():
    """**Der Plan nennt `cm.markText(…, {replacedWith: <checkbox>})` genau so** — und `atomic`,
    damit der Cursor nicht **in** `[ ]` hineinwandert."""
    quelle = EDITOR_JS.read_text(encoding="utf-8")
    assert "cm.markText(" in quelle, "der Editor setzt keine Marke"
    rumpf = _funktionskoerper(quelle, "_todoMarkenAuffrischen")
    assert "replacedWith" in rumpf, "die Marke traegt kein Kaestchen"
    assert "atomic: true" in rumpf, "die Marke ist nicht atomar — der Cursor wanderte hinein"
    assert 'kasten.type = "checkbox";' in quelle, "das Kaestchen ist keine Checkbox"


def test_the_click_switches_the_text_not_the_dom():
    """**Der Text ist die Quelle.** Der Klick schreibt `[ ]`/`[x]` in den Puffer — ein
    Kaestchen, dessen `checked` man nur im Browser setzt, waere ein **zweiter** Zustand."""
    quelle = EDITOR_JS.read_text(encoding="utf-8")
    rumpf = _funktionskoerper(quelle, "_todoUmschalten")
    assert "cm.replaceRange(" in rumpf, "der Klick schreibt nicht in den Puffer"
    assert '"[x]"' in rumpf and '"[ ]"' in rumpf, (
        "der Klick kennt die beiden Texte nicht — er schaltet also nichts um"
    )
    # **Kein**Direktschreiben in den DOM-Zustand des Kaestchens.
    assert "kasten.checked =" not in rumpf, (
        "der Klick setzt den DOM-Zustand des Kaestchens — der Text waere nicht mehr die "
        "Quelle, und der Server wuesste nichts"
    )


def test_a_clean_editor_saves_immediately_and_a_dirty_one_does_not():
    """**Hard Rule 3.** Der Klick auf einen **sauberen** Editor ist ein Schreibvorgang — mit
    der Version aus dem Schnappschuss. Bei einem **geaenderten** Editor gehoert der Klick zur
    naechsten Speicherung: nur Puffer."""
    quelle = EDITOR_JS.read_text(encoding="utf-8")
    rumpf = _funktionskoerper(quelle, "_todoUmschalten")
    assert "var sauber = !isDirty();" in rumpf, (
        "der Klick prueft nicht, ob der Editor vorher unveraendert war"
    )
    assert "if (sauber) saveItem();" in rumpf, (
        "der Klick speichert nicht sofort — die Abnahme verlangt genau das"
    )
    # **Der Zustand muss VOR** dem Puffer-Schreiben gemessen sein: sonst waere der Editor
    # durch den eigenen Klick schon geaendert und `isDirty()` waere immer wahr.
    assert rumpf.index("var sauber = !isDirty();") < rumpf.index("cm.replaceRange("), (
        "`isDirty()` wird **nach** dem Schreiben gemessen — dann ist der Editor durch den "
        "eigenen Klick immer geaendert und der Klick speichert nie"
    )
    # Und `saveItem()` nimmt die Version aus dem Schnappschuss.
    save = _funktionskoerper(quelle, "saveItem")
    assert "version: state.editingSnapshot.version" in save, (
        "`saveItem()` schreibt ohne die Version aus dem Schnappschuss — Hard Rule 3"
    )


def test_the_raw_mode_shows_every_character_and_no_checkbox():
    """**ED-5.** Im Rohmodus steht **jedes** Zeichen — also auch das `[ ]`. Die Kaestchen
    werden abgeraeumt."""
    quelle = EDITOR_JS.read_text(encoding="utf-8")
    rumpf = _funktionskoerper(quelle, "_todoMarkenAuffrischen")
    assert 'state.mode !== "raw"' in rumpf, (
        "die Kaestchen werden auch im Rohmodus gesetzt — das `[ ]` waere unsichtbar (ED-5)"
    )
    assert "_todoMarkenAuffrischen();" in _funktionskoerper(quelle, "setRawMode"), (
        "der Rohmodus schaltet die Kaestchen nicht um"
    )


def test_the_read_view_shows_a_disabled_checkbox_without_a_write_path():
    """**Die Lesesicht.** Das Kaestchen ist da — und **deaktiviert**. Der Sanitizer
    **erzwingt** `disabled` und `type="checkbox"` (fail-closed: erlauben waere nicht
    genug)."""
    quelle = MARKDOWN_JS.read_text(encoding="utf-8")
    assert "_todoHtml(" in quelle, "die Lesesicht kennt das To-do-Kaestchen nicht"
    todo = _funktionskoerper(quelle, "_todoHtml")
    assert 'type="checkbox"' in todo, "das Kaestchen der Lesesicht ist keine Checkbox"
    assert "disabled" in todo, "das Kaestchen der Lesesicht ist nicht deaktiviert"
    # Der Sanitizer: **erzwingen**, nicht nur erlauben.
    assert '"INPUT"' in quelle, "der Sanitizer kennt das INPUT-Tag nicht"
    assert 'child.setAttribute("disabled", "disabled");' in quelle, (
        "der Sanitizer **erzwingt** `disabled` nicht — ein anhakbares Kaestchen waere ein "
        "Schreibweg ausserhalb des Editors"
    )
    assert 'child.setAttribute("type", "checkbox");' in quelle, (
        "der Sanitizer erzwingt den Typ nicht"
    )


def test_the_head_names_the_step():
    """Die Doku muss den Schritt nennen — sonst steht im Head eine Behauptung ohne Beleg."""
    head = HEAD.read_text(encoding="utf-8")
    assert "11.5" in head, "der Phase-Head nennt 11.5 nicht"
    assert "ED-2" in head, "der Phase-Head nennt ED-2 nicht"
