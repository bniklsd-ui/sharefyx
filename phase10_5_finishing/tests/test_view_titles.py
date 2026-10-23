"""Wächter für den Tab-Titel (P10.5 Block 7, Schritt 7.3 — UI-3, V120).

**Was dieser Wächter prüft:** dass die **Verdrahtung** existiert — der Zustand in
`state.js`, die Aufrufe in `editor.js`, `tree.js`, `app.js` und `settings.js`.

**Was er ausdrücklich nicht prüft:** das Verhalten im Browser. Dafür ist die Probe
`probes/p105_b7_titel_probe.py` da (sie fährt eine Wegwerf-Instanz hoch, meldet sich an,
klickt durch die Ansichten und liest `document.title` — sechs Schritte, mit rotem
Gegenlauf). Ein Wächter, der den Titelverlauf behauptet, aber nur Quelltext liest, wäre
die Fehlerklasse, die der Phase-9-Befund „ein Wächter, der etwas anderes prüft als er
behauptet" beschreibt — deshalb sagt dieser Wächter, was er ist.

**Warum er überhaupt in der Suite steht:** die Deploy-Gate fährt die Suite, nicht die
Proben. Ohne diesen Wächter käme ein Fehler, der den Tab-Titel betrifft, erst beim
Sichtprüfen heraus — und zwar erst im Release."""
from __future__ import annotations

import re
from pathlib import Path

JS = Path(__file__).resolve().parents[2] / "phase5_ui/webui/static/js"


def _js(name: str) -> str:
    return (JS / name).read_text(encoding="utf-8")


def _funktionskoerper(text: str, funktion: str) -> str:
    """Der Rumpf einer Funktion — ohne den Rest der Datei.

    **Warum der Rumpf und nicht die ganze Datei:** ein Aufruf, der irgendwo im Kommentar
    steht, würde einen Test über die ganze Datei grün machen. Der Rumpf begrenzt die
    Aussage auf „in dieser Funktion"."""
    start = text.index("function " + funktion)
    # geschweifte Klammern zaehlen (der Rumpf enthaelt Objekte mit Klammern)
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


def test_state_owns_the_title():
    """Der Titel ist **Zustand** — eine Funktion, ein Ort (nicht ein Aufruf pro Stelle)."""
    state = _js("state.js")
    assert "export function setViewTitle(part)" in state
    assert "export function setPanelTitle(open)" in state
    assert "export function listViewTitle()" in state
    # Das Format: "Titel · sharefyx" (Plan §Block 7, Schritt 7.3) — mit Leerzeichen um den
    # Punkt, damit der Tab-Titel lesbar bleibt und nicht "Titel·sharefyx" heisst.
    assert '" · sharefyx"' in state
    assert re.search(r'document\.title = part \? part \+ " · sharefyx" : "sharefyx";', state), (
        "der Titel wird nicht im geplanten Format gesetzt"
    )


def test_the_item_title_is_set_when_an_item_opens():
    """Ein geöffnetes Item nennt seinen Titel im Tab (V120)."""
    editor = _js("editor.js")
    rumpf = _funktionskoerper(editor, "loadEditorFromItem")
    assert "setViewTitle(item.title)" in rumpf, (
        "loadEditorFromItem() setzt den Tab-Titel nicht — ohne das bleibt der Titel des "
        "vorigen Space stehen, während ein Item offen ist"
    )


def test_the_list_view_title_is_set_wherever_the_view_changes():
    """Die Listenansicht setzt ihren Titel an **allen** Stellen, an denen sie wechselt."""
    editor = _js("editor.js")
    assert "setViewTitle(listViewTitle())" in _funktionskoerper(editor, "showOverviewPane")
    tree = _js("tree.js")
    assert "setViewTitle(listViewTitle())" in _funktionskoerper(tree, "navigateAll")
    app = _js("app.js")
    # Der Zurueck-Knopf traegt keinen eigenen Funktionsnamen (sein Handler ist anonym) —
    # deshalb wird sein Block direkt aus dem Quelltext geschnitten.
    block = app[app.index('getElementById("back-button")'):]
    block = block[:block.index("});")]
    assert "setViewTitle(listViewTitle())" in block, (
        "der Zurueck-Knopf setzt den Listen-Titel nicht — nach dem Zurueck stuende der "
        "Item-Titel weiter im Tab"
    )


def test_the_settings_panel_lies_over_the_view():
    """Das Einstellungs-Panel ist ein **Overlay**: es überschreibt den Titel der Ansicht
    und gibt ihn beim Schließen zurück."""
    settings = _js("settings.js")
    rumpf = _funktionskoerper(settings, "show")
    assert "setPanelTitle(visible)" in rumpf
    state = _js("state.js")
    assert "panelOpen ? \"Einstellungen\" : viewTitle" in state, (
        "das Panel muss den Ansichts-Titel nur ueberdecken, nicht ersetzen — sonst stuende "
        "nach dem Schliessen 'Einstellungen' im Tab"
    )
