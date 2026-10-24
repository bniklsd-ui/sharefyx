"""Wächter für den Realtime-Client (P10.5 Block 10, Schritt 10.3 — LG-2, P10.5-S).

**Was dieser Wächter prüft:** dass die **Verdrahtung** existiert — der `EventSource`, die drei
Folgen eines Ereignisses, die Unversehrtheit des geänderten Editors und der Poll-Rückfall.

**Was er ausdrücklich nicht prüft:** das Verhalten im Browser. Dafür ist die Probe
`probes/p105_b10_realtime_probe.py` da (sie fährt eine Wegwerf-Instanz hoch, schreibt über
MCP und misst, ob die Änderung im Browser ankommt). Ein Wächter, der die Reaktionszeit
behauptet, aber nur Quelltext liest, wäre die Fehlerklasse aus dem Phase-9-Befund „ein
Wächter, der etwas anderes prüft als er behauptet" — deshalb sagt dieser Wächter, was er ist.

**Die Regel, auf die alles zielt, ist P10.5-S:** ein **geänderter** Editor wird nie
überschrieben. Der Server meldet nur, dass sich etwas geändert hat; die Entscheidung trifft
der Mensch."""
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


def test_the_client_opens_the_event_stream():
    """Der Client öffnet den Strom an der API-Route — ohne Token, mit Cookie (same-origin)."""
    realtime = _js("realtime.js")
    assert 'new EventSource("/api/v1/events")' in realtime
    assert 'source.addEventListener("changed"' in realtime


def test_a_change_reloads_the_counters():
    """Ein Ereignis lädt die Übersicht — das setzt auch `state.graphToken`, an dem die Karte
    hängt (P9-33): die Karte braucht keinen eigenen Abruf."""
    realtime = _js("realtime.js")
    rumpf = _funktionskoerper(realtime, "onChanged")
    assert "List.loadOverview()" in rumpf


def test_the_list_is_reloaded_only_for_the_affected_space():
    """Die Item-Liste wird nur neu geladen, wenn der **aktive** Space betroffen ist (im
    globalen Modus „Alle Items" dagegen immer)."""
    realtime = _js("realtime.js")
    rumpf = _funktionskoerper(realtime, "onChanged")
    assert "List.loadItems()" in rumpf
    assert "isGlobalScope()" in rumpf
    assert "spaces.indexOf(state.activeSpace)" in rumpf


def test_a_changed_editor_is_never_overwritten():
    """**P10.5-S:** Ist der Editor geändert, wird er **nicht** überschrieben — es erscheint
    ein Hinweisband. Der Server meldet nur; der Mensch entscheidet."""
    realtime = _js("realtime.js")
    rumpf = _funktionskoerper(realtime, "refreshOpenItem")
    assert "Editor.isDirty()" in rumpf
    assert "Editor.showChangedBanner(item)" in rumpf
    # Der Weg "neu laden" darf **nur** taken werden, wenn der Editor sauber ist.
    reihenfolge = rumpf.index("Editor.isDirty()")
    assert reihenfolge < rumpf.index("Editor.showChangedBanner(item)")
    assert reihenfolge < rumpf.index("Editor.reloadFromServer(item)")


def test_a_reload_takes_content_and_version_together():
    """Beim Neuladen werden Inhalt **und** Version übernommen — sonst zeigte der Editor eine
    Version, die es nicht gibt (P10.5-S, Abnahme P10.5-47)."""
    editor = _js("editor.js")
    rumpf = _funktionskoerper(editor, "reloadFromServer")
    assert "loadEditorFromItem(item" in rumpf
    assert "clearDraft(item.id)" in rumpf


def test_the_dirty_state_is_readable_from_outside():
    """`isDirty()` muss **exportiert** sein — der Realtime-Client entscheidet danach, ob er
    den Editor anfassen darf."""
    editor = _js("editor.js")
    assert "export function isDirty()" in editor


def test_the_poll_is_only_the_fallback():
    """Solange der Ereignis-Stream offen ist, pollt der Client nicht (er würde dieselben
    Daten zweimal holen). Ohne Stream: der Poll mit **120 s** Abstand. Fokus und
    Sichtbarkeit lösen weiter aus."""
    app = _js("app.js")
    assert "COUNTER_POLL_FALLBACK_MS = 120000" in app
    block = app[app.index("window.setInterval(function () {"):]
    block = block[:block.index("}, COUNTER_POLL_MS);")]
    assert "realtimeOpen()" in block
    assert "COUNTER_POLL_FALLBACK_MS" in block


def test_the_banner_exists_in_the_markup():
    """Ein Hinweisband, das es im DOM nicht gibt, wäre kein Hinweisband."""
    html = (WEBUI / "static/app.html").read_text(encoding="utf-8")
    assert 'id="editor-changed"' in html
    assert 'id="editor-changed-text"' in html
    assert 'id="editor-changed-reload"' in html
    assert re.search(r'id="editor-changed"[^>]*hidden', html), (
        "das Hinweisband muss **versteckt** starten — es erscheint nur, wenn sich wirklich "
        "etwas geaendert hat"
    )
