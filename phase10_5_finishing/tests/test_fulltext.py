"""Wächter für den Volltext-Schalter (P10.5 Block 10, Schritt 10.1 — LG-1).

**Was dieser Wächter prüft:** dass die **Verdrahtung** existiert — der Schalter im Markup,
der Zustand in `state.js`, das Anhängen des Parameters in `list.js` und der Parameter auf der
Serverseite (`api.py`).

**Was er ausdrücklich nicht prüft:** das Verhalten im Browser. Dafür ist die Probe
`probes/p105_b10_realtime_probe.py` da (sie fährt eine Wegwerf-Instanz hoch, sucht im Body
und prüft, dass der Schalter die Trefferlage ändert). Ein Wächter, der die Treffer behauptet,
aber nur Quelltext liest, wäre die Fehlerklasse aus dem Phase-9-Befund „ein Wächter, der etwas
anderes prüft als er behauptet" — deshalb sagt dieser Wächter, was er ist.

**Der Server-Teil ist doppelt abgesichert:** `phase5_ui/tests/test_api.py` prüft das
**Verhalten** am echten Store (ohne `in_body` kein Treffer, mit `in_body` ein Treffer, und ein
fremdes Item bleibt unsichtbar). Dieser Wächter hier prüft nur, dass die Schaltflächen
tatsächlich verbunden sind — ein Schalter, der nichts schickt, wäre im Browser „kaputt" und in
der Suite grün."""
from __future__ import annotations

import re
from pathlib import Path

WEBUI = Path(__file__).resolve().parents[2] / "phase5_ui/webui"
JS = WEBUI / "static/js"


def _js(name: str) -> str:
    return (JS / name).read_text(encoding="utf-8")


def _funktionskoerper(text: str, funktion: str) -> str:
    """Der Rumpf einer Funktion — ohne den Rest der Datei (siehe `test_view_titles.py`)."""
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


def test_the_switch_exists_in_the_markup():
    """Ein Schalter, den es im DOM nicht gibt, ist kein Schalter."""
    html = (WEBUI / "static/app.html").read_text(encoding="utf-8")
    assert 'id="search-in-body"' in html
    assert 'type="checkbox"' in html


def test_the_state_owns_the_flag():
    """Der Volltext ist **Zustand** — ein Feld, ein Ort (nicht ein zweiter Ort im Markup)."""
    state = _js("state.js")
    assert re.search(r"inBody:\s*false", state), (
        "der Volltext-Schalter gehoert in `state.js` — sonst wuerde jeder, der ihn liest, "
        "seinen eigenen Zustand fuehren"
    )


def test_the_list_sends_the_parameter():
    """`loadItems()` haengt `in_body=1` an — und **nur**, wenn der Schalter an ist."""
    liste = _js("list.js")
    rumpf = _funktionskoerper(liste, "loadItems")
    assert 'params.set("in_body", "1")' in rumpf
    assert "if (state.inBody)" in rumpf


def test_the_switch_reloads_the_list():
    """Ein Schalter, der die Liste nicht neu laedt, waere ein Schalter ohne Wirkung."""
    liste = _js("list.js")
    assert "fulltextEl.addEventListener(\"change\"" in liste
    assert "state.inBody = !!fulltextEl.checked" in liste


def test_the_parameter_is_also_sent_in_the_global_scope():
    """Der globale Modus („Alle Items") durchsucht **alle** sichtbaren Spaces — der Volltext
    gilt dort genauso. `in_body` darf deshalb nicht an `isGlobalScope()` haengen."""
    liste = _js("list.js")
    rumpf = _funktionskoerper(liste, "loadItems")
    zeile = [z for z in rumpf.splitlines() if 'in_body' in z]
    assert zeile, "der Parameter kommt in `loadItems()` nicht vor"
    assert not any("isGlobalScope" in z for z in zeile), (
        "der Volltext darf nicht an den globalen Modus gebunden sein — er gilt im Space-Modus "
        "wie im globalen Modus"
    )


def test_the_server_reads_the_parameter():
    """Der Server liest `in_body` **als Wahrheitswert** und reicht ihn an den Store durch."""
    api = (WEBUI / "api.py").read_text(encoding="utf-8")
    assert "_parse_bool(q.get(\"in_body\"))" in api
    assert "in_body=in_body" in api
