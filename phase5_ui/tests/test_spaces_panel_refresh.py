"""**BG-1 (P10.5, Block 2, 2026-10-22)** — die Verdrahtung, nicht das Verhalten.

Der Befund: öffnete der Mensch „Spaces verwalten", **bevor** das (langsame) `/overview`
antwortete, blieb die Space-Liste leer — auch danach, denn `spaces.js` liest `state.spaces` und
füllt die Liste nur beim Öffnen des Panels nach (V202, M4 reproduziert: 0 Zeilen, nach
Panel-Zu/Auf 2).

Der **Beweis** des Verhaltens ist die Browser-Probe (M4,
`phase10_inventory/probes/p10_m4_bg1_probe.py`) — die darf nur Claude Code fahren (Plan Block 2,
Schritt 2.5, Wegwerf-Instanz). Dieser Wächter sichert nur die **Verdrahtung**, die die Probe
prüft: die Kopplung läuft über ein Ereignis (`list.js` → `window` → `spaces.js`), weil
`spaces.js` `loadOverview()` aus `list.js` importiert und ein Import **zurück** einen Zyklus
bauen würde (dieselbe Form wie bei `state.graphToken`).

Ein Wächter, der behauptet, das Verhalten zu prüfen, und es nicht tut, ist schlimmer als
keiner — deshalb steht hier ausdrücklich „Verdrahtung, nicht Verhalten".
"""
from __future__ import annotations

import re

from webui.config import UiSettings

_JS_DIR = UiSettings(base_url="https://space.example.ts.net").static_dir / "js"

_IMPORT_RE = re.compile(r'^\s*import\s[^\n]*?from\s+"(\./[^"]+)"', re.MULTILINE)

_EVENT_NAME = "sfx:overview-loaded"


def _read(name: str) -> str:
    return (_JS_DIR / name).read_text(encoding="utf-8")


def test_list_js_fires_the_overview_loaded_event_after_filling_state_spaces():
    source = _read("list.js")
    assert f'new CustomEvent("{_EVENT_NAME}")' in source
    assign = source.index("state.spaces = overview;")
    dispatch = source.index(f'new CustomEvent("{_EVENT_NAME}")')
    assert assign < dispatch, (
        "das Ereignis muss NACH dem Füllen von `state.spaces` kommen — sonst rendert der "
        "Empfänger den alten Stand"
    )


def test_spaces_js_listens_for_it_and_rerenders_only_when_the_panel_is_open():
    source = _read("spaces.js")
    listener = source.index(f'addEventListener("{_EVENT_NAME}"')
    block = source[listener:listener + 600]
    assert "renderSpaceList()" in block, "der Listener muss die Liste neu zeichnen"
    assert "hidden" in block, (
        "der Listener muss prüfen, ob das Panel offen ist — sonst zeichnet er ins Leere"
    )


def test_the_coupling_runs_through_the_event_not_through_an_import():
    """Der Ereignis-Weg ist Absicht: `spaces.js` importiert `loadOverview()` aus `list.js`, ein
    Import von `spaces.js` zurück in `list.js` wäre ein Zyklus."""
    assert "./list.js" in _IMPORT_RE.findall(_read("spaces.js"))
    assert "./spaces.js" not in _IMPORT_RE.findall(_read("list.js"))
