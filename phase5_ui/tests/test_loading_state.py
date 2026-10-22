"""**P10.5, Block 4 (2026-10-22)** — die Verdrahtung des Ladezustands und des schlanken
Clients, nicht das Verhalten.

Diese Datei prüft **Verdrahtung**, und sie sagt das ausdrücklich: ein Wächter, der behauptet,
das Verhalten zu prüfen, und es nicht tut, ist schlimmer als keiner (dieselbe Lehre wie in
`test_spaces_panel_refresh.py`). Das **Verhalten** — 150 ms ohne Gerüst, 400 ms mit Gerüst,
kein Text im Platzhalter — belegt der Browser-Probe
`phase10_5_finishing/probes/p105_b4_loading_probe.py` (Plan Block 4, Schritt 4.6).

Drei Zusagen, die hier festgehalten werden:

1. **PF-4:** der Client holt **nur** `/overview` — der zweite Vollabruf auf `/spaces` und der
   Merge im Client sind weg. Beide Routen liefern denselben Stand; der Server führt sie jetzt
   zusammen (`api.py :: _overview()` trägt `folders`/`members`).
2. **PF-4 (Poll):** `focus` und `visibilitychange` bekommen eine Mindestpause von 10 s. Der
   20-s-Intervall bleibt. Ohne die Pause feuerte jeder Tab-Wechsel sofort einen Abruf, und
   auf der langsamen Strecke wartete der Space-Wechsel dann hinter dem eigenen Poll (Z2).
3. **P10.5-S:** ein Platzhalter trägt **nie** eine `version`. Das ist hier nicht nur
   Konvention, sondern by construction: `loading.js` setzt eine CSS-Klasse und schreibt
   **keinen Text** in die Oberfläche — der Gerüstbau liegt vollständig in `app.css`.
"""
from __future__ import annotations

import re

from webui.config import UiSettings

_STATIC_DIR = UiSettings(base_url="https://space.example.ts.net").static_dir
_JS_DIR = _STATIC_DIR / "js"

_LINE_COMMENT = re.compile(r"//[^\n]*")
_BLOCK_COMMENT = re.compile(r"/\*.*?\*/", re.DOTALL)


def _read(name: str) -> str:
    return (_JS_DIR / name).read_text(encoding="utf-8")


def _code_only(source: str) -> str:
    """Der Quelltext **ohne** Kommentare. Die Kommentare dürfen das Wort „version" nennen —
    die Zusage gilt dem **Code**, der könnte sie brechen."""
    return _BLOCK_COMMENT.sub("", _LINE_COMMENT.sub("", source))


def test_the_client_fetches_the_overview_and_no_longer_the_spaces():
    """PF-4: ein Request statt zwei. Der alte Merge stand in `list.js :: loadOverview()`.

    Geprüft wird der **Code** ohne Kommentare — der Kommentar im Modul darf den alten Aufruf
    nennen (er erklärt, warum er weg ist), der Code darf ihn nicht mehr enthalten."""
    source = _code_only(_read("list.js"))
    assert 'api("/overview")' in source
    assert 'api("/spaces")' not in source, (
        "der zweite Vollabruf auf `/spaces` muss weg — `folders`/`members` stehen jetzt in "
        "der `/overview`-Antwort"
    )
    # Und der Merge ist wirklich weg, nicht nur der Aufruf: kein `byName`, kein `extra`.
    assert "byName" not in source
    assert "extra.folders" not in source


def test_the_overview_answer_carries_folders_and_members_on_the_server():
    """Die andere Hälfte von PF-4: was der Client nicht mehr holt, muss der Server liefern.
    Geprüft wird am echten Quelltext von `api.py` — der Test `test_overview.py` prüft die
    **Antwort**, dieser hier die **Stelle**, an der sie entsteht."""
    source = (_STATIC_DIR.parent / "api.py").read_text(encoding="utf-8")
    assert '"folders": list(space.folders)' in source
    assert '"members": list(space.members)' in source


def test_the_poll_has_a_ten_second_minimum_pause_for_focus_and_visibilitychange():
    """PF-4 (Poll): `focus` und `visibilitychange` werden gedrosselt, der 20-s-Intervall
    nicht. Ohne die Pause schlug der Nikinger-Fall aus P10 (M1) zu: jeder Tab-Wechsel feuerte
    sofort einen Abruf, und der Space-Wechsel wartete dann hinten an."""
    source = _read("app.js")
    assert "COUNTER_MIN_PAUSE_MS = 10000" in source
    assert "COUNTER_POLL_MS = 20000" in source, "der Intervall bleibt bei 20 s (Plan §4.3)"
    focus = source.index('addEventListener("focus"')
    visibility = source.index('addEventListener("visibilitychange"')
    assert "throttle: true" in source[focus:focus + 120], (
        "der Fokus-Auslöser muss die Mindestpause kennen"
    )
    assert "throttle: true" in source[visibility:visibility + 200], (
        "der Sichtbarkeits-Auslöser muss die Mindestpause kennen"
    )


def test_the_loading_module_offers_the_two_hundred_millisecond_default():
    """Der Plan nennt die Signatur wörtlich: `withLoading(el, promise, { delayMs = 200 } = {})`.
    Darunter 200 ms gibt es kein Flackern (Z4: „Ladezustand genau ab 200 ms")."""
    source = _read("loading.js")
    assert "export function withLoading(el, promise, { delayMs = 200 } = {})" in source, (
        "die Signatur ist Teil des Plans — eine andere wäre eine stille Abweichung"
    )
    assert 'classList.add("is-loading")' in source
    assert 'classList.remove("is-loading")' in source


def test_the_placeholder_cannot_carry_any_text_at_all():
    """P10.5-S: ein Platzhalter trägt nie eine `version`. Geprüft wird die **Eigenschaft**,
    nicht das Wort: der Code des Moduls schreibt **keinen Text** in die Oberfläche (kein
    `textContent`, kein `innerHTML`, kein `insertAdjacentHTML`) — er setzt eine CSS-Klasse.
    Damit kann hier keine Versionsnummer erscheinen, und keine in einen Write geraten.

    Die Kommentare dürfen das Wort nennen (sie tun es), deshalb wird der Code vorher von ihnen
    befreit."""
    code = _code_only(_read("loading.js"))
    for verboten in ("textContent", "innerHTML", "insertAdjacentHTML", "createTextNode"):
        assert verboten not in code, (
            f"`{verboten}` im Ladezustand — der Platzhalter darf keinen Text erzeugen"
        )
    assert "version" not in code.lower()


def test_the_loading_state_is_wired_at_the_four_places():
    """Übersicht, Liste, Item-Öffnen und Karte (Plan §4.4). Die vier Stellen sind namentlich
    genannt, damit eine verschobene Verdrahtung auffällt."""
    assert 'withLoading(listOverviewEl, api("/overview"))' in _read("list.js")
    assert 'withLoading(listRowsEl, api("/items?"' in _read("list.js")
    assert 'withLoading(detailEl, api("/items/"' in _read("editor.js")
    assert 'withLoading(graphEl, api("/graph"))' in _read("graph.js")


def test_overlapping_requests_do_not_cancel_each_others_loading_state():
    """Zwei Abrufe können **gleichzeitig** an einem Element hängen: der 20-s-Poll und ein
    Schreibvorgang, oder der Poll und der Aktualisieren-Knopf. Ohne Zähler nähme der
    **schnellere** Abruf die Klasse ab, während der langsamere noch läuft — der Ladezustand
    verschwände, obwohl noch etwas kommt. Der Fund kam aus der Browser-Probe (4.6): der erste
    Entwurf nahm die Klasse im `done()`-Zweig immer ab.

    Verdrahtungswaechter: der Zaehler muss je Element laufen und die Klasse erst beim
    **letzten** Abruf abnehmen."""
    source = _read("loading.js")
    assert "offeneLadezustaende" in source, "der Zaehler je Element fehlt"
    assert "WeakMap" in source, "der Zaehler muss je Element laufen, nicht global"
    code = _code_only(source)
    # Die Klasse darf **nur** im Zweig "kein Abruf mehr offen" abgenommen werden.
    assert code.count('classList.remove("is-loading")') == 1
    assert "if (offen <= 0)" in code, (
        "die Klasse muss an die Zahl der offenen Abrufe gebunden sein"
    )


def test_the_skeleton_is_static_under_reduced_motion():
    """Bei `prefers-reduced-motion: reduce` ist das Gerüst **statisch**, ohne Schimmer —
    dieselbe Rücksicht wie beim Graphen (Plan §5 D2, `MAX_TICKS_REDUCED`)."""
    css = (_STATIC_DIR / "app.css").read_text(encoding="utf-8")
    assert ".is-loading::after" in css
    reduced = css[css.index("@media (prefers-reduced-motion: reduce)", css.index(".is-loading::after")):]
    block = reduced[:reduced.index("}") + 1]
    assert "animation: none" in block, (
        "im Reduced-Motion-Zweig muss die Animation ausgeschaltet sein"
    )
