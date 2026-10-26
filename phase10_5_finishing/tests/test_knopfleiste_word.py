"""Wächter für die **Knopfleiste nach Word** (P10.5 Block 13, 2026-10-25).

Der Auftrag des Nikingers: „Die ganze Knopfleiste überarbeiten, an Word orientiert:
ähnliche Knöpfe, vor allem die **Reihenfolge 1:1 wie in Word**." Dazu die zwei
Nachbarposten desselben Auftrags: die **Schriftgröße** im Live-Editor (P10.5 Block 13.1)
und die **einheitliche Knopf-Farbe** (Block 13.3).

Diese Wächter lesen die **Quelle** (Markup und CSS). Sie sagen nichts darüber, wie es im
Browser aussieht — dafür ist die **Probe** da
(`phase10_5_finishing/probes/p105_b13_knopfleiste_probe.py`, 8 von 8 Zellen grün an der
Wegwerf-Instanz). Die Teilung ist die übliche: der Wächter hält die **Absicht** fest, die
Probe belegt die **Wirkung**.

**Warum die Reihenfolge überhaupt maschinell prüfbar sein muss:** eine Reihenfolge, die nur
im Kopf des Ausführenden steht, wird beim nächsten Umbau stillschweigend verschoben. Die
Soll-Liste steht deshalb **wortgleich** im Markup-Kommentar in `app.html` — ein zweiter
Ort, an dem sie auseinanderlaufen kann. Dieser Wächter prüft die Liste in `app.html`
gegen die Soll-Liste **hier**; die Probe misst zusätzlich, ob der Browser dasselbe zeigt
(DOM statt Quelle).
"""
from __future__ import annotations

import re
from html.parser import HTMLParser
from pathlib import Path

REPO_ROOT = Path(__file__).resolve().parents[2]
STATIC = REPO_ROOT / "phase5_ui/webui/static"
APP_HTML = STATIC / "app.html"
APP_CSS = STATIC / "app.css"
EDITOR_JS = STATIC / "js/editor.js"
SPRITE_SKIPT = STATIC / "js"
VENDOR_ICONS = REPO_ROOT / "phase5_ui/vendor/lucide/icons"

#: Die **Word-Reihenfolge** (Start-Ribbon). Eine allgemeine Anordnung ist nicht
#: urheberrechtlich geschützt — der Nikinger-Auftrag vom 2026-10-25.
#: Schriftart → Absatz → Formatvorlagen → Einfügen (der Rohtext-Schalter ist seit 2026-10-26 entfernt).
WORD_REIHENFOLGE = [
    "bold", "italic", "code", "format-farbe", "format-groesse",
    "ul", "ol", "format-ausrichtung",
    "h", "quote",
    "image", "hr", "link",
]

#: Die vier Word-Gruppen der Leiste + der Modus-Schalter (keine Word-Gruppe: ein
#: Ansichts-Schalter, wie Words Ansichtsumschalter in der Statuszeile).
WORD_GRUPPEN = ["schriftart", "absatz", "vorlagen", "einfuegen"]

#: Die fünf Icons, die mit der Werkzeugleiste nach Word dazukamen (Block 13.2). Sie
#: ersetzen die HTML-Entity-Zeichen `</>`, `•` und `—` — die Verbotsliste der Phase 8
#: (§0.3 Punkt 1) verbietet Entity-Zeichen als Icons ausdrücklich.
NEUE_ICONS = ["code", "heading", "list", "list-ordered", "minus"]


class _Toolbar(HTMLParser):
    """Liest die Werkzeugleiste aus dem Markup: die Bedienelemente in DOM-Reihenfolge, die
    Gruppen in ihrer Reihenfolge und der Text jedes Knopfes (ohne die SVG-Iconen)."""

    def __init__(self) -> None:
        super().__init__()
        self._tiefe = 0
        self._drin = False
        self._knopf_tiefe = 0
        self.elemente: list[str] = []
        self.gruppen: list[str] = []
        self.knopf_texte: list[str] = []
        self._text = ""

    def handle_starttag(self, tag, attrs):  # noqa: D102 - HTMLParser
        d = dict(attrs)
        if not self._drin:
            if tag == "div" and d.get("id") == "editor-toolbar":
                self._drin = True
                self._tiefe = 1
            return
        self._tiefe += 1
        if tag == "button":
            self.elemente.append(d.get("data-md") or d.get("id") or "?")
            self._knopf_tiefe = self._tiefe
            self._text = ""
        elif tag == "select":
            self.elemente.append(d.get("id") or "?")
        elif tag == "div" and "toolbar-group" in (d.get("class") or ""):
            self.gruppen.append(d.get("data-word-group") or "modus")

    def handle_data(self, data):  # noqa: D102 - HTMLParser
        if self._knopf_tiefe:
            self._text += data

    def handle_endtag(self, tag):  # noqa: D102 - HTMLParser
        if self._drin:
            if tag == "button" and self._knopf_tiefe == self._tiefe:
                self.knopf_texte.append(self._text.strip())
                self._knopf_tiefe = 0
                self._text = ""
            self._tiefe -= 1
            if self._tiefe == 0:
                self._drin = False


def _toolbar() -> _Toolbar:
    p = _Toolbar()
    p.feed(APP_HTML.read_text(encoding="utf-8"))
    return p


def test_toolbar_order_is_the_word_order() -> None:
    """**Die Reihenfolge 1:1 wie in Word** (Nikinger-Auftrag 2026-10-25). Die Soll-Liste
    steht wortgleich im Markup-Kommentar in `app.html` — dieser Wächter vergleicht die
    **Quelle**, die Probe vergleicht den **Browser**."""
    t = _toolbar()
    assert t.elemente == WORD_REIHENFOLGE, (
        f"die Reihenfolge der Werkzeugleiste weicht von Word ab: {t.elemente!r} "
        f"statt {WORD_REIHENFOLGE!r}"
    )


def test_toolbar_carries_the_word_groups() -> None:
    """Die vier Word-Gruppen und der Modus-Schalter. Die Gruppen sind nicht nur Kosmetik:
    sie tragen die **Trenner** (`.toolbar-group + .toolbar-group`), und der Modus-Schalter
    steht **ganz rechts** (`margin-left: auto`) — wie Words Ansichtsumschalter."""
    t = _toolbar()
    assert t.gruppen == WORD_GRUPPEN, f"die Gruppen der Leiste: {t.gruppen!r}"


def test_no_entity_icons_left_in_the_toolbar() -> None:
    """**Keine Emoji und keine HTML-Entity-Zeichen als Icons** (Phase-8-Verbotsliste §0.3
    Punkt 1: „nur das Lucide-Sprite"). Vor Block 13.2 trug die Leiste `</>`, `•` und `—`."""
    html = APP_HTML.read_text(encoding="utf-8")
    block = html.split('id="editor-toolbar"', 1)[1].split("</div>\n", 1)[0]
    for zeichen in ("&bull;", "&mdash;", "&lt;/&gt;"):
        assert zeichen not in block, f"das Entity-Zeichen {zeichen!r} steht noch in der Leiste"
    # Jeder Knopf traegt **entweder** ein Sprite-Icon **oder** einen der zwei Buchstaben
    # (B und I — genau wie in Word; die sind keine Icons). Der Modus-Schalter traegt seine
    # **Beschriftung** ("Rohtext") — das ist kein Icon, sondern Text.
    t = _toolbar()
    for text in t.knopf_texte:
        if not text:
            continue
        assert text in ("B", "I", "Rohtext"), (
            f"unbekannte Knopfbeschriftung {text!r} in der Leiste — erlaubt sind die "
            f"zwei Buchstaben und die Beschriftung des Modus-Schalters"
        )


def test_the_new_icons_are_vendored_and_in_the_sprite() -> None:
    """Die fünf neuen Icons liegen **vendored** vor (mit Pin-Nachweis im
    `vendor/lucide/README.md`) und stehen im Sprite — der Generator ist der einzige
    Weg dorthin (`build_icon_sprite.py`), damit der Sprite nie von Hand driftet."""
    html = APP_HTML.read_text(encoding="utf-8")
    for name in NEUE_ICONS:
        assert (VENDOR_ICONS / f"{name}.svg").exists(), f"vendor/lucide/icons/{name}.svg fehlt"
        assert f'id="i-{name}"' in html, f"das Symbol i-{name} fehlt im Sprite"
    # Die Reihenfolge im Sprite ist alphabetisch (der Generator sortiert) — das ist die
    # Billigkeit des Sprites: kein Zufalls-Block, der beim Handpflegen zerfaellt.
    symbole = re.findall(r'<symbol id="i-([a-z0-9-]+)"', html)
    erwartet = [q.stem for q in sorted(VENDOR_ICONS.glob("*.svg"))]
    assert symbole == erwartet, (
        "der Sprite entspricht nicht der vendored Reihenfolge (der Generator sortiert "
        "die Dateinamen) — der Sprite waere von Hand gepflegt"
    )


def test_sprite_generator_is_idempotent() -> None:
    """**Der Generator muss den Sprite unveraendert neu erzeugen.** Ohne diesen Schritt
    waere der Sprite eine Handarbeit, die beim naechsten Icon-Update stillschweigend
    abweicht."""
    import subprocess
    import sys
    proc = subprocess.run(
        [sys.executable, str(REPO_ROOT / "phase5_ui/scripts/build_icon_sprite.py"), "--check"],
        cwd=str(REPO_ROOT), capture_output=True, text=True,
    )
    assert proc.returncode == 0, f"der Sprite driftet ab: {proc.stdout}{proc.stderr}"


def test_editor_overlay_returns_the_size_class() -> None:
    """**Die Groesse wirkt im Live-Editor** (Block 13.1): der Overlay-Token gibt die
    Groessen-Klasse mit. Vorher gab er nur die Farbe zurueck — die Groesse zeigte sich
    erst in der Vorschau."""
    js = EDITOR_JS.read_text(encoding="utf-8")
    assert "r.push(groesse);" in js, (
        "der Overlay-Overlay gibt die Groessen-Klasse nicht zurueck — `klein`/`gross` "
        "wuerden im Live-Editor wieder nur in der Vorschau wirken"
    )
    # Die Reihenfolge im Text ist frei (`{.gross .rot}`) — der Wächter verlangt deshalb,
    # dass **jeder** Name gegen beide Vokabulare geprueft wird.
    assert "V.farben[n]" in js and "V.groessen[n]" in js, (
        "die Klasse wird nicht gegen beide Vokabulare geprueft — die Reihenfolge der "
        "Klassen im Text ([Text]{.gross .rot}) wuerde falsch aufgeloest"
    )


def test_editor_line_height_is_a_fixed_length() -> None:
    """**Die Zeile springt nicht** (Block 13.1): der Editor traegt eine **feste**
    Zeilenhoehe in **px**. Eine relative Angabe (`1.6`) waechst mit der Schrift — genau
    der Sprung, den der Nikinger nicht mehr sehen wollte. Die Groessen-Klassen tragen
    `line-height: 0`: sie tragen keine eigene Zeilenbox, die Grundlinie bleibt die der
    Zeile, die Zeile bleibt 21 px."""
    css = re.sub(r"/\*.*?\*/", "", APP_CSS.read_text(encoding="utf-8"), flags=re.DOTALL)
    m = re.search(r"^\.CodeMirror\s*\{([^}]*)\}", css, flags=re.MULTILINE)
    assert m, ".CodeMirror fehlt im Stylesheet"
    assert re.search(r"line-height\s*:\s*\d+px\s*;", m.group(1)), (
        "die Zeilenhoehe des Editors muss eine feste Laenge in px sein — eine relative "
        f"Angabe waechst mit der Schrift: {m.group(1)!r}"
    )
    for klasse in ("klein", "normal", "gross"):
        regel = re.search(rf"^\.CodeMirror \.cm-md-s-{klasse}\s*\{{([^}}]*)\}}", css,
                          flags=re.MULTILINE)
        assert regel, f".CodeMirror .cm-md-s-{klasse} fehlt"
        assert "line-height: 0" in regel.group(1), (
            f".cm-md-s-{klasse} traegt keine eigene Zeilenbox (line-height: 0) — "
            f"sonst waechst die Zeile mit der Schrift: {regel.group(1)!r}"
        )


def test_button_fill_is_the_transparent_blue() -> None:
    """**Die Knopf-Flaeche ist das blaue, leicht-transparente Design** (Block 13.3,
    Nikinger-Auftrag). Vorher standen dort **deckende** Hex-Werte (`#0C1C31`); die waren
    eine datierte Entscheidung vom 2026-10-01 (P9), die der Nikinger am 2026-10-25
    umgekehrt hat.

    Der Wächter prueft beides: dass die Deckkraft **kleiner als 1** ist (sonst waere die
    Flaeche wieder deckend) und dass es **das eine Blau** ist (rgba 62,141,243 — der
    Akzent, dieselben drei RGB-Werte wie `--accent` und `--select-fill`)."""
    css = APP_CSS.read_text(encoding="utf-8")
    m = re.search(r"^\s*--btn-std-fill\s*:\s*([^;]+);", css, flags=re.MULTILINE)
    assert m, "--btn-std-fill fehlt"
    wert = m.group(1)
    assert "rgba(62,141,243" in wert, f"--btn-std-fill traegt nicht das Akzentblau: {wert!r}"
    deckkraefte = [float(x) for x in re.findall(r"rgba\(62,141,243,([\d.]+)\)", wert)]
    assert deckkraefte, "--btn-std-fill traegt keine rgba-Deckkraft"
    assert all(d < 1.0 for d in deckkraefte), (
        f"--btn-std-fill muss halbtransparent sein, gefunden: {deckkraefte}"
    )
    for token in ("btn-std-fill-hover", "btn-std-fill-active", "btn-std-line"):
        t = re.search(rf"^\s*--{token}\s*:\s*([^;]+);", css, flags=re.MULTILINE)
        assert t, f"--{token} fehlt"
        assert "62,141,243" in t.group(1), f"--{token} nutzt ein anderes Blau: {t.group(1)!r}"


def test_the_caution_colour_has_room_on_the_new_fill() -> None:
    """**Die Vorsicht-Farbe auf der neuen Flaeche** (Block 13.3): mit der
    halbtransparenten Flaeche liegt der Knopf heller als frueher — #F06A6E haette auf
    dem Editor-Kopf nur 4,10:1 (Hover 3,59:1) erreicht (unter AA). Der Wächter rechnet das nach, statt
    es zu behaupten (der Rechenweg steht in `test_contrast.py`)."""
    from phase10_5_finishing.tests.test_contrast import (
        UNTERGRUENDE, _hex, _mischung, _rgb, _stops, _token, kontrast,
    )

    caution = _token("caution")
    stops = _stops(_token("btn-std-fill"))
    assert stops, "--btn-std-fill traegt keine Farbe"
    schlimmster = 99.0
    for farbe, deckkraft in stops:
        for name, untergrund in UNTERGRUENDE.items():
            wert = kontrast(caution, _hex(_mischung(farbe, deckkraft, _rgb(untergrund))))
            schlimmster = min(schlimmster, wert)
    assert schlimmster >= 4.5, (
        f"--caution {caution} erreicht auf der Standardflaeche nur {schlimmster:.2f}:1 "
        f"(WCAG AA verlangt 4,5:1)"
    )
