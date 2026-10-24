"""Die committen Belege der Block-11.4-Probe: die Live-Darstellung des Editors.

**Was diese Probe misst (und warum sie drei Verbergungs-Arten fährt).** Der Plan verlangt für
`.cm-formatting` (die `**` eines starken Textes) eine Ausblendung — die Formatierungszeichen
sollen nur auf der **Cursorzeile** sichtbar sein. Dafür gibt es drei Kandidaten:
`visibility: hidden`, `display: none` und `font-size: 0`. Der Plan nennt `display: none` gegen
`font-size: 0` als Prüfpaar (`[VERIFY V211]`), und das Kriterium ist die **korrekte
Cursorposition nach dem Klick**.

**Das Ergebnis ist eine Entscheidung, keine Geschmackssache** — und die Entscheidung steht in
den Beleg: `visibility: hidden` hält den Cursor an der richtigen Stelle, `display: none` und
`font-size: 0` setzen ihn **genau so viele Zeichen zu früh**, wie verdeckte Formatierungszeichen
vor ihm stehen. Diese Datei bindet die Entscheidung an den Beleg: wer sie später umdreht,
muss die Belege umdrehen — und der Test sagt dann, warum.

**Zwei Fallen, die der Wächter ausdrücklich bewacht.**

* **Die Variante muss wirklich ausgeliefert worden sein.** Die erste Fassung der Probe
  schaltete die CSS per Inline-`<style>` um — die CSP der App (`style-src 'self'`, ohne
  `'unsafe-inline'`) **blockiert** das. Die Probe meldete drei gleiche Werte und damit „grün
  ohne etwas gemessen zu haben". Jetzt wird die Variante **same-origin** ausgeliefert
  (`page.route` auf `/ui/static/app.css`) und **im Browser zurückgelesen**
  (`--p105-variante`) — der Wächter prüft, dass jede Variante auch wirklich angekommen ist.
* **Der Gegenlauf muss genau die Zellen brechen, die er brechen soll.** Er dreht den Fix in
  `editor.js` ab (`setBody` setzt den Cursorzeilen-Marker nicht neu). Bricht er keine Zelle,
  misst er nichts; bricht er zu viele, ist er unpräzise.
"""
from __future__ import annotations

import json
from pathlib import Path

REPO_ROOT = Path(__file__).resolve().parents[2]
PROBE_DIR = REPO_ROOT / "phase10_5_finishing" / "probes"
GRUEN = PROBE_DIR / "p105_b11_live.json"
GEGENLAUF = PROBE_DIR / "p105_b11_live_gegenlauf.json"
EDITOR_JS = REPO_ROOT / "phase5_ui" / "webui" / "static" / "js" / "editor.js"
HEAD = REPO_ROOT / "phase10_5_finishing" / "CLAUDE.md"

#: Die drei Verbergungs-Arten, die die Probe fährt (in dieser Reihenfolge).
VARIANTEN = ("visibility", "display", "fontsize")

#: Die Zellen, die der Gegenlauf brechen muss. Sie alle drei haengen an **einer** Ursache:
#: `cm.setValue()` nimmt die Zeilenklassen mit, und die Kurzpruefung in `_cursorZeileSetzen()`
#: (`cmCursorZeile === zeile`) verhindert, dass der Marker neu gesetzt wird.
#: Die Zahl der verdeckten Formatierungszeichen vor der Zielstelle: die beiden `**` des
#: starken Textes. Genau um diese Zahl ruecken `display: none` und `font-size: 0` den
#: Cursor nach vorn (gemessen am 2026-10-24).
VERDECKTE_ZEICHEN = 2

GEGENLAUF_ZELLEN = (
    "cursorzeile_markiert",
    "cursorzeile_markiert_nach_zurueck",
    "formatierung_auf_der_cursorzeile_sichtbar",
)


def _befund(datei: Path) -> dict:
    assert datei.exists(), f"der Beleg fehlt: {datei}"
    return json.loads(datei.read_text(encoding="utf-8"))


def _zellen(befund: dict) -> dict[str, bool]:
    """Nur die **booleschen** Zellen — Messwerte (Indices, Pixel) sind keine Zellen."""
    return {k: v for k, v in befund.items() if isinstance(v, bool)}


def test_the_green_report_has_all_cells_green():
    bericht = _befund(GRUEN)
    assert bericht.get("alle_kriterien_erfuellt") is True, (
        "der grüne Beleg meldet nicht 'alle Kriterien erfüllt' — die Datei ist kein Beleg"
    )
    rot = [k for k, v in _zellen(bericht["befund"]).items() if not v]
    assert not rot, f"rote Zellen im grünen Beleg: {rot}"
    assert len(_zellen(bericht["befund"])) >= 15, (
        "der Beleg trägt weniger als 15 Zellen — die Zählung in der Doku stimmt nicht mehr"
    )


def test_every_variant_was_really_delivered():
    """**Die CSP-Falle.** Ohne diesen Wächter darf die Probe wieder drei gleiche Zahlen
    melden, ohne etwas gemessen zu haben: die erste Fassung schaltete die CSS per
    Inline-`<style>` um, und die CSP der App blockiert das."""
    varianten = _befund(GRUEN)["messung"]["varianten"]
    for name in VARIANTEN:
        assert name in varianten, f"die Variante {name!r} fehlt im Beleg"
        ausgeliefert = varianten[name].get("variante_ausgeliefert")
        assert ausgeliefert == name, (
            f"die Variante {name!r} wurde **nicht** ausgeliefert (gelesen: {ausgeliefert!r}) — "
            "der Browser hatte eine andere CSS, und die Messung waere fuer die Katz"
        )


def test_visibility_is_the_measured_winner():
    """**Die V211-Entscheidung, an den Beleg gebunden.** `visibility: hidden` haelt den Cursor
    an der richtigen Stelle; `display: none` und `font-size: 0` ruecken ihn um **genau** die
    Zahl der verdeckten Formatierungszeichen nach vorn."""
    varianten = _befund(GRUEN)["messung"]["varianten"]

    gut = varianten["visibility"]["stellen"]
    assert gut, "die Variante 'visibility' hat keine Messstellen"
    for stelle in gut:
        cursor = stelle["cursor"]
        assert cursor is not None, "der Cursor wurde nicht gemessen"
        assert cursor["ch"] == stelle["erwarteter_index"], (
            f"bei {stelle['zeichen']!r} steht der Cursor auf ch {cursor['ch']}, erwartet war "
            f"{stelle['erwarteter_index']}"
        )
        assert stelle["sprung"] == 0.0, (
            f"bei {stelle['zeichen']!r} springt die Zeile um {stelle['sprung']} px — "
            "die Zeile darf nicht springen, wenn der Cursor hineinwechselt"
        )

    for name in ("display", "fontsize"):
        stellen = varianten[name]["stellen"]
        assert stellen, f"die Variante {name!r} hat keine Messstellen"
        # Bei diesen beiden Arten bekommen die `**` auf der Cursorzeile **Platz**
        # (`display: inline` statt `display: none`), waehrend sie auf allen anderen Zeilen
        # keinen Platz haben. Die Zeile **springt** also, sobald der Cursor hineinwechselt --
        # und der Cursor landet danach um genau die Zahl der verdeckten Zeichen zu früh.
        abweichungen = []
        for stelle in stellen:
            cursor = stelle["cursor"]
            assert cursor is not None, f"bei {name!r} wurde der Cursor nicht gemessen"
            abweichung = stelle["erwarteter_index"] - cursor["ch"]
            if abweichung:
                abweichungen.append((stelle["zeichen"], abweichung))
        assert abweichungen, (
            f"bei {name!r} steht der Cursor ueberall richtig — die Behauptung 'diese Art "
            "verschiebt den Cursor' waere dann falsch, und der Wächter wuerde sie nur noch "
            "behaupten"
        )
        for zeichen, abweichung in abweichungen:
            assert abweichung == VERDECKTE_ZEICHEN, (
                f"bei {name!r} steht der Cursor bei {zeichen!r} um {abweichung} Zeichen daneben "
                f"— erwartet waere genau {VERDECKTE_ZEICHEN} (die beiden `**`)"
            )


def test_the_counter_run_breaks_exactly_the_cursor_line_cells():
    bericht = _befund(GEGENLAUF)
    assert bericht.get("alle_kriterien_erfuellt") is False, (
        "der Gegenlauf ist grün — er misst nichts"
    )
    rot = sorted(k for k, v in _zellen(bericht["befund"]).items() if not v)
    assert rot == sorted(GEGENLAUF_ZELLEN), (
        f"der Gegenlauf muss genau die Zellen {sorted(GEGENLAUF_ZELLEN)} brechen, "
        f"gebrochen wurde: {rot}"
    )


def test_the_two_reports_are_different_files():
    """Der Gegenlauf darf den grünen Beleg nicht überschreiben."""
    assert GRUEN != GEGENLAUF
    assert GRUEN.read_text(encoding="utf-8") != GEGENLAUF.read_text(encoding="utf-8")


def test_setbody_resets_the_cursor_line_marker_before_setvalue():
    """**Der Fix, an den Quelltext gebunden.** `cm.setValue()` ersetzt das ganze Dokument und
    nimmt die Zeilenklassen mit; CM5 feuert dabei **kein** `cursorActivity`. Ohne das
    Zuruecksetzen von `cmCursorZeile` greift die Kurzpruefung in `_cursorZeileSetzen()` und der
    Marker bleibt weg. Der Gegenlauf der Probe dreht genau diese drei Zeilen ab."""
    quelle = EDITOR_JS.read_text(encoding="utf-8")
    beginn = quelle.index("export function setBody(text)")
    abschnitt = quelle[beginn:quelle.index("\n}", beginn) + 2]
    zuruecksetzen = abschnitt.index("cmCursorZeile = null;")
    setzen = abschnitt.index("cm.setValue(text);")
    assert zuruecksetzen < setzen, (
        "in `setBody()` muss `cmCursorZeile = null;` **vor** dem `cm.setValue(text);` stehen — "
        "sonst haelt die Kurzpruefung die alte (falsche) Meinung"
    )
    assert "_cursorZeileSetzen();" in abschnitt, (
        "`setBody()` muss den Cursorzeilen-Marker danach neu setzen"
    )


def test_the_head_names_the_measurement():
    """Die Doku muss die Messung nennen — sonst steht im Head eine Behauptung ohne Beleg."""
    head = HEAD.read_text(encoding="utf-8")
    assert "11.4" in head, "der Phase-Head nennt 11.4 nicht"
    assert "V211" in head, "der Phase-Head nennt die V211-Messung nicht"
