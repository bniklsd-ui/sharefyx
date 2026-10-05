"""P9 Block settings — Einstellungen als Fensterkette (Plan
`docs/concepts/phase9_hardening_block_settings_plan.md`, Locks P9-AE–P9-AL, Abnahme
P9-83–P9-91/P9-93).

**Warum statisch und nicht im Browser.** Die Kette ist ein Zustandsproblem (welches Panel ist
offen, was schließt ein ESC), und die *Regeln* dafür sind Verträge zwischen `settings.js`,
dem Markup und dem Stylesheet. Diese Datei hält die Verträge fest; `app.js`s ESC-Kette ist
ein dritter Beteiligter, weil ein Dialog, den ESC nicht kennt, per Definition außerhalb der
Bedienung liegt — das ist keine Behauptung, die man aus dem Bild herausfindet.

**Zwei Dinge, die hier ausdrücklich NICHT geprüft werden** und die der Browser-Lauf
(`phase9_hardening/scripts/p9_settings_chain_probe.py`, S1–S9) prüft:
1. die *gemessene* Optik der Menüknöpfe (Höhe/Polster/Rundung ±1 px gegen eine echte
   `.tree__folder`-Zeile im Browser) — im Test steht hier nur, dass **kein eigener Wert**
   notiert ist, der von der Baumzeile abweichen könnte;
2. das Verhalten (Panelwechsel, ESC-Reihenfolge, Schmal-Modus) — dafür ist ein Browserlauf
   der ehrliche Weg, weil Zustand im DOM ohne Layout nicht entscheidbar ist.

Ein Test, der die Optik *behauptet* statt sie zu messen, wäre die achte Wiederholung der
Lehre aus den letzten Phasen: eine Prüfung, die das Richtige an der falschen Stelle prüft,
ist derselbe Fehler eine Ebene tieber. `test_settings_menu_items_reuse_the_tree_row_look()`
prüft deshalb die **Ursache** (kein kopierter Wert) und nicht die Wirkung.
"""
from __future__ import annotations

import re
from html import unescape

from webui.config import DEFAULT_STATIC_DIR

# Reihenfolge und Beschriftung aus P9-AE, wörtlich.
MENU_ITEMS = (
    ("settings-open-password", "Passwort ändern"),
    ("account-manage-spaces", "Spaces verwalten"),
    ("account-show-updates", "Update-Log"),
)
# P9-AJ: aktuelles Passwort -> neues -> wiederholen -> TOTP zuletzt.
PASSWORD_FIELDS = ("account-current", "account-new", "account-repeat", "account-totp")
# Panels der Kette in Stufenfolge (P9-AG). `menu` ist Stufe 1 und steht immer zuerst.
CHAIN_PANELS = ("settings-menu", "settings-password", "settings-spaces", "settings-space-detail",
                "settings-updates")


def _html() -> str:
    return (DEFAULT_STATIC_DIR / "app.html").read_text("utf-8")


def _css() -> str:
    return (DEFAULT_STATIC_DIR / "app.css").read_text("utf-8")


def _css_code() -> str:
    """`app.css` **ohne** Kommentare — Grundlage jeder Regel-Suche.

    Ein Kommentar in dieser Datei darf Kommas und geschweifte Klammern enthalten („90% /
    max-width: 440px", `--select-fill-quiet`); ein naiv gelesener Selektor zerlegt sich
    daran. Genau das ist beim Bauen dieses Tests passiert: die erste Fassung fand **null**
    Regeln fuer `.settings-menu__item`, weil sie den Kommentar ueber der Sammelregel als
    Selektor gelesen hat — und ein Wächter, der nichts findet, meldet „keine eigene Optik"
    als „kein Befund". Deshalb wird hier vorher ausgestrippt, statt den Kommentar im
    Selektor zu heilen."""
    return re.sub(r"/\*.*?\*/", "", _css(), flags=re.DOTALL)


def _js(name: str) -> str:
    """`name` mit oder ohne Endung — die Aufrufe mischen beide Formen, ein Anhängen wäre
    stumm falsch, wenn der Modulname schon die Endung trägt."""
    if not name.endswith(".js"):
        name += ".js"
    return (DEFAULT_STATIC_DIR / "js" / name).read_text("utf-8")


def _element_by_id(html: str, element_id: str) -> str:
    """Der Tag mit dieser ID, samt Inhalt, oder Fehler. Naiv per Regex, aber mit Absicht:
    `app.html` ist statisches Markup ohne Build (P5-T), es gibt keinen HTML-Parser im Projekt,
    und ein Test, der einen eigenen mitbringt, prüft am Ende den Parser.

    Die Entities werden aufgelöst (`&auml;` → `ä`): das Markup schreibt Umlaute konsequent
    als Entity (so wie es vor diesem Block schon tat), und ein Wächter, der die geschriebene
    Form vergleicht, würde beim ersten Umlaut-Umstieg rot werden — nicht weil sich etwas
    geändert hätte, sondern weil die Schreibweise wechselte."""
    match = re.search(
        rf'<(?P<tag>[a-zA-Z0-9]+)\b[^>]*\bid="{re.escape(element_id)}"[^>]*>'
        rf'(?P<body>.*?)</(?P=tag)>',
        html,
        flags=re.DOTALL,
    )
    assert match is not None, f'Element mit id="{element_id}" nicht gefunden'
    return unescape(match.group(0))


# `:not([…])` erst wegrechnen, bevor nach einem **Zustands**-Attribut gesucht wird: P9-AN
# schreibt die Flaeche gerade fuer die *nicht* ausgewaehlten Punkte, und genau dieses
# `:not([aria-current="true"])` darf den Wächter nicht dazu bringen, die eigene Regel wie
# eine Zustandsregel zu uebersehen.
_NOT_MIT_ATTRIBUT = re.compile(r":not\([^()]*\[[^()]*\][^()]*\)")


def _alle_regeln() -> list[tuple[str, list[str], str]]:
    """`(erster Selektor, Selektorliste, Body)` je Regel — die eine Lesemaschine des Moduls.

    Zwei Fehler, die diese Funktion ersetzt hat, waren beide *Zeilen*-Annahmen: eine Regel, die
    über mehrere Zeilen geschrieben ist (`#settings-menu h2 { … }` mit Umbruch), wurde von
    einem Muster nicht gefunden, das Selektor und `{` auf **einer** Zeile verlangt — und ein
    Wächter, der eine vorhandene Regel nicht findet, meldet „nicht gebaut". Das war am
    2026-10-05 zweimal dieselbe Fehlerklasse (einmal `re.escape()` auf einem bereits
    regexartigen String, einmal `class="btn settings-back"` mit fester Klassenreihenfolge).
    Body und Selektorliste werden deshalb am `{}`-Paar getrennt, nicht an Zeilenenden."""
    regeln = []
    for match in re.finditer(r"(?m)^([^{}]+?)\{([^{}]*)\}", _css_code()):
        selectors = [part.strip() for part in match.group(1).split(",")]
        regeln.append((selectors[0], selectors, match.group(2)))
    return regeln


def _ist_eigene_regel(erster: str, selector: str) -> bool:
    """Traegt die Regel der Klasse etwas **eigenes** — und ist dabei **nicht** zustandsbedingt?

    Zwei Bedingungen, und die zweite ist am 2026-10-05 dazugekommen (P9-AN):

    1. Die Klasse steht am **Ende** des ersten Selektors, optional mit einem Vorfahren davor
       (`.settings-panel--menu .settings-menu__item`, so steht P9-APs Textmitte im
       Stylesheet). Die gemeinsame Regel
       `.rail__home, …, .tree__folder, …, .settings-menu__item, …` traegt genau die Werte der
       **Baumzeile**, die der Knopf uebernehmen soll — sie ist Wiederverwendung, nicht der
       Verstoß. Genau an diesem Unterschied haengt der Test.
    2. **Kein Attribut im Selektor** (nach Wegrechnen der `:not(…)`-Klammern). Eine Regel wie
       `.settings-menu__item[aria-current="true"]` ist der **Auswahlzustand** und traegt
       zu Recht Farbe, Kante und Schatten — sie wird von
       `test_the_selection_state_uses_aria_current_and_the_existing_fill()` geprueft, nicht
       von diesem Wächter. Ohne diese Bedingung waere die Regel mit P9-AN in Konflikt
       geraten, **obwohl** sie die Zustandsregel von P9-AO ist.

    Pseudo-Klassen sind erlaubt (`.settings-menu__item:hover`), weil sie nichts an der
    Geometrie aendern — verboten ist nur der **Zustand**."""
    if not re.search(rf"(?:^|\s){re.escape(selector)}(?=[:\s]|$)", erster):
        return False
    return "[" not in _NOT_MIT_ATTRIBUT.sub("", erster)


def _rule_bodies(css: str, selector: str, own_only: bool = False) -> list[str]:
    """Die Bodies aller CSS-Regeln, deren Selektorliste `selector` enthaelt.

    `own_only=True` liefert nur die Regeln, die `_ist_eigene_regel()` bejaht — also die, die
    der Klasse etwas eigenes geben. Ein Wächter, der die Sammelregel mitzaehlt, wuerde jede
    korrekte Wiederverwendung als Verfehlung melden."""
    bodies: list[str] = []
    for erster, selectors, body in _alle_regeln():
        if own_only:
            if _ist_eigene_regel(erster, selector):
                bodies.append(body)
            continue
        if selector in selectors:
            bodies.append(body)
    return bodies


def _tokens() -> set[str]:
    """Die Custom Properties, die `app.css` in `:root` **tatsaechlich** definiert.

    Nicht die Liste der erlaubten Namen aus einer Doku, sondern die aus dem File: ein Token,
    den es nicht gibt, faellt im Browser still auf den nicht gesetzten Wert zurueck, und die
    Flaeche der Menuepunkte waere dann wieder die des Fensterhintergrunds — mit dem
    `background`-Wert im Stylesheet und ohne sichtbare Wirkung. Genau diese Klasse Fehler ist
    der Grund, warum hier gegen die Definition und nicht gegen eine Absicht geprueft wird."""
    block = re.search(r":root\s*\{(.*?)\n\}", _css_code(), flags=re.DOTALL)
    assert block is not None, "app.css hat keinen :root-Block"
    return set(re.findall(r"(--[\w-]+)\s*:", block.group(1)))


# P9-AN, 2026-10-05: verboten ist die **Geometrie** und die **Textfarbe**, nicht die Flaeche.
# Die erste Fassung dieses Wächters stand `background` auf der Verbotsliste und wäre an
# **korrektem** Code rot geworden — P9-AN verlangt genau diese Flaeche. Erweitert wurde der
# Wächter im **selben Commit** wie der Bau, sonst hätte er eine Woche zu eng gemeldet und wäre
# dann weggeräumt statt korrigiert worden.
#
# **Das Polster ist in drei Hälften geteilt, und das ist die einzige Ausnahme:** `padding-left`
# darf der Menüpunkt setzen (Nikinger-Entscheidung 2026-10-05, mit der Messung aus Plan §10 —
# als `.tree__folder` erbte er die 32-px-Einrückung der Baumzeile und lag damit 12 px neben der
# Mitte), und **nur** mit dem Wert der Sammelregel. `padding` als Kurzform sowie
# `padding-top`/`padding-bottom`/`padding-right` bleiben verboten: sie tragen die **Höhe**,
# und die Höhe ist das, was P9-AF an die Baumzeile bindet.
VERBOTENE_OPTIK = ("height", "padding", "padding-top", "padding-bottom", "padding-right",
                    "border-radius", "font", "color", "box-shadow",
                    "border", "margin", "line-height")
# Erlaubt sind ausschliesslich Flaeche, Ausrichtung, die linke Polsterkante (s. o.) und die
# **Haarlinie** des Eingabefeldes. `border-color` ist bewusst erlaubt und `border` (die
# Kurzform) bewusst nicht: die Kurzform traegt Breite und Stil und koennte damit genau die
# Geometrie veraendern, die P9-AF an die Baumzeile bindet. Die Flaeche **ohne** Haarlinie
# waere zudem nicht die des Eingabefeldes, sondern eine neue — P9-97 vergleicht Hintergrund
# **und** Kante.
ERLAUBTE_OPTIK = ("background", "background-color", "background-image", "border-color",
                  "text-align", "padding-left")
TEXT_ALIGN_WERTE = ("left", "center", "right", "start", "end")
# Der einzige erlaubte Wert fuer `padding-left` — der der Sammelregel, mit der die Kette
# anfaengt. Alles andere waere eine eigene Polsterkante und damit Geometrie unter neuem Namen.
ERLAUBTES_PADDING_LEFT = "var(--space)"


def _optik_verstoss(body: str, tokens: set[str]) -> list[str]:
    """Alle Verstoesse eines Regel-Bodys: verbotene Eigenschaften, und erlaubte Eigenschaften
    mit einem Wert, der **kein** vorhandenes Token ist.

    Der zweite Teil ist der Grund, warum „erlaubt" nicht genug waere: `background: #0C1015`
    waere formal erlaubt und waere genau die dritte Variante, die P9-AF abschaffen wollte — nur
    eben eine fuer die Farbe statt fuer die Optik."""
    verstoesse: list[str] = []
    for prop in VERBOTENE_OPTIK:
        if re.search(rf"(^|[;{{\s]){prop}\s*:", body):
            verstoesse.append(f"verboten: {prop}")
    for match in re.finditer(rf"(^|[;{{\s])({"|".join(ERLAUBTE_OPTIK)})\s*:\s*([^;]*)", body):
        prop, wert = match.group(2), match.group(3).strip()
        if prop == "text-align":
            if wert not in TEXT_ALIGN_WERTE:
                verstoesse.append(f"text-align: {wert!r}")
            continue
        if prop == "padding-left":
            if wert != ERLAUBTES_PADDING_LEFT:
                verstoesse.append(
                    f"padding-left: {wert!r} (erlaubt ist nur {ERLAUBTES_PADDING_LEFT}, der "
                    f"Wert der Sammelregel)")
            continue
        for token in re.findall(r"var\((--[\w-]+)\)", wert):
            if token not in tokens:
                verstoesse.append(f"{prop}: undefiniertes Token {token}")
        if "var(" not in wert:
            verstoesse.append(f"{prop}: {wert!r} ist kein Token")
    return verstoesse


def _bare_rule_bodies(selector: str) -> list[str]:
    """Die Bodies der Regeln, deren **erster** Selektor exakt `selector` ist.

    Nicht dasselbe wie `_rule_bodies(..., own_only=True)`: dort zählt auch
    `.settings-menu__item:not([aria-current="true"])` und
    `.settings-panel--menu .settings-menu__item`, hier nur die nackte Selektorliste. Gebraucht
    für „diese Regel **und keine andere**" — z. B. dass die Basis-`.input`-Regel ihre Fläche
    wirklich dort trägt und nicht in `select.input`."""
    return [body for erster, _, body in _alle_regeln() if erster == selector]


def _eigenschaft(body: str, prop: str) -> str | None:
    """Der erste Wert dieser Eigenschaft im Body, oder `None`. Bewusst **ohne** Fallback auf
    die Sammelregeln: der Aufrufer will wissen, was **diese** Regel sagt."""
    m = re.search(rf"(?:^|[;{{\s]){prop}\s*:\s*([^;{{]+)", body)
    return m.group(1).strip() if m else None


def test_the_settings_menu_carries_exactly_three_buttons_in_the_locked_order():
    """P9-83 / P9-84: Titel „Einstellungen", **kein** Hinweistext, genau drei Knöpfe in der
    Reihenfolge aus P9-AE — und keiner mehr.

    „Genau drei" ist der Teil, der zählt. Ein vierter Knopf (oder ein Hinweistext) wäre eine
    stille Erweiterung, die niemand beauftragt hat; die Prüfung ist deshalb auf *Anzahl und
    Reihenfolge*, nicht auf das Vorhandensein der drei."""
    html = _html()
    menu = _element_by_id(html, "settings-menu")
    buttons = re.findall(r'<button[^>]*\bid="([^"]+)"', menu)
    assert buttons == [i for i, _ in MENU_ITEMS], buttons
    for element_id, label in MENU_ITEMS:
        assert re.search(re.escape(label), _element_by_id(html, element_id)), element_id
    # Kein Hinweistext: `.overlay__hint` im Menü wäre genau der Fließtext, den P9-AE abschafft.
    assert "overlay__hint" not in menu, menu
    # Und keine weiteren Knöpfe in irgendeiner Form (auch nicht ohne id).
    assert len(re.findall(r"<button", menu)) == 3, menu


def test_the_password_panel_puts_totp_last():
    """P9-AJ: aktuelles Passwort → neu → wiederholen → **TOTP zuletzt**. Grund im Lock: „so ist
    der Code beim Absenden noch frisch" — nach dem Tippen des neuen Passworts ist die
    Authenticator-App am weitesten von vorn.

    Geprüft wird die **Reihenfolge im Markup**, nicht die im DOM-Query: `querySelectorAll`
    liefert Dokumentreihenfolge, aber eine Assertion über `index()`-Vergleiche würde auch
    grün werden, wenn jemand die Felder per JS umhinge — und genau das wäre die Umgehung."""
    html = _html()
    panel = _element_by_id(html, "settings-password")
    # Nur die **Eingabefelder** — `account-error`/`-submit`/`-cancel` tragen denselben
    # Namensraum und würden die Reihenfolge verfälschen.
    found = tuple(
        m.group(1) for m in re.finditer(r'<input\b[^>]*\bid="(account-[a-z]+)"', panel)
    )
    assert found == PASSWORD_FIELDS, f"Passwortfelder in falscher Reihenfolge: {found}"
    # Der Hinweis zu Connectoren und Sitzungen ist mitgewandert (P9-AJ) — er stand vorher
    # im Konto-Dialog und soll jetzt **hier** stehen, nicht irgendwo verschwunden sein.
    assert "Danach musst du jeden Connector neu autorisieren" in panel, panel


def test_the_three_old_overlays_are_gone_and_the_chain_is_one():
    """P9-AG: eine Fensterkette, keine drei Overlays. Geprüft in **beiden** Richtungen: die
    alten IDs existieren nicht mehr (sonst gäbe es zwei Wege, dieselbe Sache zu öffnen), und
    alle fünf Panels hängen an **einem** `.settings-chain` in **einem** `.overlay`.

    Drei positionierte Overlays wären kein Nebeneinander, sondern drei Hintergründe
    übereinander, die sich dreifach abdunkeln (Plan §2, verworfene Alternative) — deshalb
    ist die *Ein*-Kette hier die eigentliche Aussage, nicht die Panelzahl."""
    html = _html()
    for gone in ("account-dialog", "space-admin-dialog", "update-log-dialog"):
        assert not re.search(rf'\bid="{gone}"', html), f"#{gone} existiert noch"

    # Der Ketten-Ausschnitt laeuft bis zum **naechsten** `.overlay`-Element, nicht bis zu
    # einem `</div></div>`: die Panels enthalten selbst verschachtelte `</div>`, ein
    # greediges Muster fresse deshalb die halbe Datei (erster Entwurf, gemessen) und der
    # Test pruefte dann die Aussenseite des Overlays mit.
    start = html.index('<div class="overlay" id="settings-overlay" hidden>')
    nxt = html.find('<div class="overlay"', start + 1)
    body = html[start: nxt if nxt != -1 else len(html)]
    assert '<div class="settings-chain">' in body, body[:200]
    for panel in CHAIN_PANELS:
        assert f'id="{panel}"' in body, panel
    # Kein zweiter Overlay-Rahmen **innerhalb** der Kette -- der eigene zaehlt nicht, also
    # erst abschneiden. `class="overlay"` als Textvergleich waere sonst ein Fehlalarm: jedes
    # Panel traegt `class="overlay__panel …"`, und der Praefix passt. Die Anfuehrungszeichen
    # hinter dem Wort sind die Grenze.
    inner = body[body.index('<div class="settings-chain">'):]
    assert not re.search(r'class="overlay"(?![-\w])', inner), inner


def test_settings_menu_items_reuse_the_tree_row_look():
    """P9-AF: die Menüknöpfe tragen die Optik der Ordnerzeile im Navigationsbaum —
    **wiederverwendet**, nicht kopiert.

    Der Wächter prüft die *Ursache*: (a) die Knöpfe tragen `.tree__folder` im Markup, und
    (b) für `.settings-menu__item` ist **keine eigene Geometrie** notiert. Damit kann die
    Menüzeile nicht von der Baumzeile abweichen, ohne dass ein Test rot wird — was ein
    Wächter auf *gemessene* Optik in diesem Kontext nicht könnte (im Test gibt es kein
    Layout; die Messung macht die Browser-Probe, S1).

    Punkt (b) ist genau die Lehre vom 2026-10-01: `.account-nav` trug eine eigene Kopie der
    Knopfoptik, dadurch entstand eine dritte Variante, und der erste Korrekturversuch (auf
    `.btn` umstellen) löste das Problem nur durch eine weitere Kopie. Wiederverwendung ist
    die einzige Form, die sich nicht auflösen lässt.

    **Beide Lesarten, mit Datum — der Wächter wurde am 2026-10-05 (P9-AN) enger gezogen, und
    zwar im selben Commit wie der Bau.** Vorher stand `background` auf der Verbotsliste: der
    Wächter wäre an **korrektem** Code rot geworden, denn P9-AN verlangt für die unausgewählten
    Menüpunkte die Fläche des Eingabefeldes. Neu verboten sind nur noch **Geometrie,
    Textfarbe, Kanten-Kurzform und Schatten**; erlaubt sind Fläche, Haarlinie und
    `text-align` — und eine Fläche **nur** aus einem Token, das `app.css` in `:root` auch
    wirklich definiert. Die Formulierung „keine eigene Optik" wäre nach dieser Änderung eine
    Unwahrheit, deshalb steht der alte Satz nicht mehr im Docstring, sondern wird hier
    ausdrücklich abgelöst."""
    html = _html()
    css = _css()
    for element_id, _ in MENU_ITEMS:
        block = _element_by_id(html, element_id)
        assert "tree__folder" in block, f"{element_id} traegt nicht .tree__folder: {block}"
        assert "settings-menu__item" in block, element_id
    tokens = _tokens()
    flaeschen_woerter = 0
    for selector in (".settings-menu__item", ".settings-space-row"):
        rules = _rule_bodies(css, selector, own_only=True)
        assert rules, f"{selector} hat keine eigene Regel im Stylesheet"
        for body in rules:
            verstoesse = _optik_verstoss(body, tokens)
            assert not verstoesse, (selector, verstoesse, body)
            flaeschen_woerter += len(re.findall(r"(^|[;{\s])background\s*:", body))
    # **Und die Flaeche, die P9-AN verlangt, ist auch da.** Ein Wächter, der nur verbietet,
    # waere nach einem Revert des Baus immer noch gruen — er wuerde dann die *Abwesenheit*
    # des Verstoßes melden und die Abwesenheit der Loesung verschweigen. Fuer die
    # Space-Zeilen ist das nicht verlangt (P9-AN nennt nur die Menuepunkte), also genau eine.
    assert flaeschen_woerter >= 1, (
        "keine eigene Regel setzt eine Hintergrundflaeche — P9-AN (unausgewaehlter "
        "Menuepunkt traegt die Flaeche des Eingabefeldes) waere nicht gebaut"
    )


def test_the_menu_item_watchdog_bites_on_built_in_violations():
    """**Der Wächter wird an eingebauten Verstößen geprüft, nicht an vertrauensvollem Code.**

    Vier Zeilen, die keine Phase-9-Datei enthält, deren jede aber rot werden muss. Grund: P9-AN
    hat diesen Wächter von einem *Verbot* auf eine *Erlaubnis mit Bedingung* umgestellt
    (`background` ist erlaubt, `background: #0C1015` nicht). Ein Verbot kann man lesen und
    glauben; eine Erlaubnis mit Bedingung prüft man nur, indem man die Bedingung verletzt —
    sonst steht am Ende ein Wächter, der alles erlaubt, was niemand verboten hat.

    Der vierte Fall ist der eigentliche Fund dieser Zeile: `:not([aria-current="true"])` ist
    **keine Zustandsregel** (sonst wäre P9-AN mit P9-AO in Konflikt), wohl aber eine **eigene**
    (sonst umginge sie diesen Wächter). Genau das prüft `_ist_eigene_regel()`."""
    tokens = _tokens()
    verstoesse = {
        "eigene Hoehe": "height: 36px;",
        "eigenes Polster oben": "padding-top: 10px;",
        "eigenes Polster rechts": "padding-right: 20px;",
        "Polster-Kurzform": "padding: 10px;",
        "linkes Polster mit eigenem Wert": "padding-left: 24px;",
        "eigene Rundung": "border-radius: 10px;",
        "eigene Textfarbe": "color: var(--text);",
        "Kanten-Kurzform": "border: 1px solid var(--line-strong);",
        "eigener Schatten": "box-shadow: 0 1px 0 rgba(0,0,0,.5);",
        "Farbe statt Token": "background: #0C1015;",
        "erfundenes Token": "background: var(--sunken-tiefer);",
        "falscher Text-align": "text-align: middle;",
    }
    for name, body in verstoesse.items():
        assert _optik_verstoss(body, tokens), f"der Wächter meldet {name!r} ({body}) nicht"
    # Und die dreiköpfige Erlaubnis meldet **nichts**:
    erlaubt = ("background: var(--sunken);", "border-color: var(--line-strong);",
               "text-align: center;", f"padding-left: {ERLAUBTES_PADDING_LEFT};")
    for body in erlaubt:
        assert not _optik_verstoss(body, tokens), f"{body!r} wird zu Unrecht gemeldet"
    # `:not([aria-current="true"])` ist eine **eigene** Regel und **keine** Zustandsregel.
    assert _ist_eigene_regel('.settings-menu__item:not([aria-current="true"])',
                             ".settings-menu__item")
    assert not _ist_eigene_regel('.settings-menu__item[aria-current="true"]',
                                 ".settings-menu__item")
    # Die Sammelregel mit `.tree__folder` bleibt Wiederverwendung, kein eigener Verstoß.
    assert not _ist_eigene_regel(".rail__home", ".settings-menu__item")
    assert not _ist_eigene_regel(".settings-menu__item__klein", ".settings-menu__item")


def test_the_selection_state_uses_aria_current_and_the_existing_fill():
    """P9-AG: der Knopf des offenen Unterfensters trägt den Auswahlzustand **der Konvention** —
    `aria-current="true"` und `--select-fill`, dieselben zwei Werte wie eine aktive
    `.tree__folder`-Zeile. Kein neuer Füll-Farbwert, kein zweiter Zustand.

    Beide Hälften werden geprüft, weil jede für sich allein nichts bedeutet: `aria-current`
    ohne CSS-Regel ist ein Attribut, eine CSS-Regel ohne Attribut ist toter Ballast. Die
    Probe S1 vergleicht dann die *gemessenen* Werte der beiden Zustände."""
    css = _css()
    assert re.search(r"\.settings-menu__item\[aria-current=\"true\"\]", css), (
        "keine Auswahlregel für die Menüpunkte"
    )
    for selector in ('.settings-menu__item[aria-current="true"]', '.tree__folder[aria-current="true"]'):
        bodies = _rule_bodies(css, selector)
        assert bodies, f"keine Regel fuer {selector}"
        assert all("var(--select-fill)" in body for body in bodies), (
            f"{selector} nutzt nicht --select-fill: {bodies}"
        )
    # Und dieselbe **eine** Auswahlregel wie die Baumzeile — nicht eine daneben. Zwei
    # Regeln mit demselben Wert wären der Beginn der dritten Variante.
    assert _rule_bodies(css, '.settings-menu__item[aria-current="true"]') == _rule_bodies(
        css, '.tree__folder[aria-current="true"]'
    ), "die Auswahlregel der Menüpunkte weicht von der der Baumzeile ab"


def test_the_narrow_mode_hides_the_menu_and_shows_a_back_button():
    """P9-AI: unterhalb der Summe der Panelbreiten bleibt **nur das rechteste** Panel sichtbar,
    mit „Zurück" links oben. Kein Quetschen, kein horizontales Scrollen — dieselbe Regel wie
    im P8.6-Editor (≤ 1024 px: Liste **oder** Editor, nie beides).

    Geprüft wird die *Form* der Regel, nicht ihre Breite (die misst die Browser-Probe, S8):
    (a) der Menü-Ausschluss liegt in einer Media-Query mit der 1024er-Obergrenze,
    (b) `:has()` wählt über die `hidden`-Attribute statt über eine JS-Entscheidung — sonst
    hätte die Kette einen zweiten Zustand, der auseinanderlaufen kann, und
    (c) „Zurück" ist im breiten Modus wirklich unsichtbar, nicht nur deaktiviert."""
    css = _css()
    narrow = re.search(r"@media \(max-width: 1024px\)\s*\{(?P<body>.*?)\n\}", css, flags=re.DOTALL)
    assert narrow is not None, "keine 1024er Media-Query für die Fensterkette"
    body = narrow.group("body")
    assert ":has(" in body and "#settings-menu" in body, body
    assert ".settings-back" in body and "display: inline-flex" in body, body
    # Breit: der Knopf existiert, ist aber nicht im Layout (`display: none`, nicht `hidden` —
    # ein `hidden` im Markup würde die `!important`-Regel weiter unten brauchen).
    assert re.search(r"(?m)^\.settings-back\s*\{\s*display:\s*none;", css), css
    html = _html()
    for panel in ("settings-password", "settings-spaces", "settings-space-detail", "settings-updates"):
        block = _element_by_id(html, panel)
        # **Die Klasse darf zwischen `btn` und `settings-back` weitere Knoepfe tragen.** Seit
        # P9-AQ ist es `btn btn--icon settings-back`, und ein Muster mit fester
        # Klassenreihenfolge meldete den Knopf als fehlend, obwohl er da ist — dieselbe
        # Fehlerklasse wie `re.escape()` auf einen bereits regexartigen String (2026-10-05):
        # ein Wächter, der am Muster scheitert, sieht wie ein Befund aus.
        back = re.search(
            r'<button[^>]*class="[^"]*\bsettings-back\b[^"]*"[^>]*>.*?</button>',
            block, flags=re.DOTALL)
        assert back is not None, f"kein Zurück-Knopf in #{panel}"
        # **Nur der öffnende Tag**, und `aria-hidden` ist kein `hidden`. Seit P9-AQ steckt im
        # Knopf ein `<svg aria-hidden="true">` — der erste Wächter, der auf `hidden` im
        # *ganzen* Element prüfte, meldete daraufhin vier Panels ohne Zurück-Knopf, während der
        # Knopf sichtbar neben dem Test stand. `(?<![\w-])` trennt die beiden Schreibweisen.
        opening = back.group(0).split(">", 1)[0]
        assert not re.search(r"(?<![\w-])hidden\b", opening), (
            f"#{panel}: der Zurück-Knopf darf nicht `hidden` tragen — er wird per CSS gesteuert"
        )


def test_every_stage_has_a_wired_back_button():
    """**Fund der Browser-Probe S8 (2026-10-05), als Wächter aufgestellt.** `settings.js`
    verdrahtete den „Zurück"-Knopf nur für die Stufen 2 — Stufe 3 (Space-Detail) war
    ausgenommen, mit der Begründung, die rechteste Stufe werde ohnehin von rechts geschlossen.

    Genau das ist der Fall, für den der Knopf erfunden ist: im Schmal-Modus ist Stufe 3 das
    **einzige** sichtbare Panel, also ist ihr „Zurück" der einzige Weg zur Stufe 2. Im breiten
    Modus fällt der Fehler nicht auf, weil ESC und „Schließen" denselben Weg nehmen — der
    Knopf war schlicht tot, und die Probe meldete ihn als *toten* Knopf, nicht als fehlenden.

    Der Wächter prüft die Verdrahtung, nicht die Existenz: `panelEls[name].querySelector(
    ".settings-back")` muss für **jede** Stufe außer dem Menü laufen. `space-detail` ist
    ausdrücklich genannt, damit die nächste Ausnahme wieder auffällt."""
    settings = _js("settings.js")
    # Die **zweite** `STAGES.forEach` -- die erste holt nur die Panel-Elemente. An der
    # richtigen zu unterscheiden ist hier nicht Formsache: `settings.js` hat drei solche
    # Schleifen (Elemente holen, Zurück verdrahten, Menüpunkte verdrahten), und ein Wächter,
    # der die erste erwischt, prüft eine Liste von `getElementById`-Aufrufen und meldet
    # Erfolg. Gesucht wird deshalb die, in der `.settings-back` vorkommt.
    schleifen = re.findall(r"STAGES\.forEach\(function \(name\) \{(.*?)\n  \}\);", settings,
                           flags=re.DOTALL)
    with_back = [b for b in schleifen if ".settings-back" in b]
    assert with_back, "keine STAGES-Schleife verdrahtet einen .settings-back-Knopf"
    body = with_back[0]
    assert 'if (name === "menu") return;' in body, (
        "die Ausnahme muss ausschließlich das Menü betreffen — 'space-detail' stand hier "
        "kurzzeitig und hat den Knopf tot gelassen"
    )
    assert '"space-detail"' not in body, body
    assert ".settings-back" in body and "closeFrom(name)" in body, body


def test_the_two_titles_share_one_gap_and_only_the_menu_title_is_centered():
    """P9-AM + P9-AR (2026-10-05, Nikinger): der Menütitel wird zentriert, und der Abstand
    zwischen Titel und erster Zeile ist **ein** Wert an **zwei** Stellen.

    Drei Behauptungen, drei Wächter statt einer:

    1. `text-align: center` steht **nur** am Menütitel. Der Space-Titel im Detail bleibt links,
       und die Titel der Unterfenster erst recht (P9-AT).
    2. Der Abstand ist **ein** Wert: `--settings-title-gap` wird **genau einmal** definiert
       (`.settings-chain`) und **genau zweimal** verwendet. Ein Wert, der zweimal notiert wird,
       ist der Beginn der dritten Variante — dieselbe Regel wie P9-AF, nur für einen Abstand.
    3. Er ist **kein** neuer Wert, sondern ein Vielfaches von `--space` (dessen
       `--space: 8px; /* alles ist ein Vielfaches davon */`). Eine freie Pixelzahl hier würde
       der erste Wert im Stylesheet sein, der sich nicht aus dem Raster ableiten lässt.

    Die **Wirkung** — dass beide Panels denselben Abstand messen und der Titel mittig steht —
    ist S11/S13 der Browser-Probe. Dieser Wächter prüft die Ursache, weil er sonst nur
    behauptete."""
    css = _css_code()
    # (1) …
    zentriert = [(erster, body) for erster, _, body in _alle_regeln()
                 if _eigenschaft(body, "text-align") == "center"]
    kette = [(s, b) for s, b in zentriert if "settings" in s]
    assert len(kette) == 1, (
        f"erwartet genau eine per text-align zentrierte Regel der Kette (der Menütitel), "
        f"gefunden {[s for s, _ in kette]}"
    )
    assert kette[0][0] == "#settings-menu h2", kette[0][0]
    for unberuehrt in ("#settings-password h2", "#settings-updates h2", "#settings-spaces h2",
                       "#settings-space-detail h2"):
        assert not any(unberuehrt in s for s, _ in kette), (
            f"{unberuehrt} darf nicht zentriert werden — P9-AM nennt den Menütitel, P9-AT "
            f"das Passwort- und das Update-Log-Panel ausdrücklich als unberührt"
        )
    # (2) …
    # **Aus den Regeln, nicht mit einem Zeilenmuster:** die Definition steht im *Body* der
    # `.settings-chain`-Regel, und ein Muster über die Zeilen fand zuerst den Body (dessen erste
    # Zeile auch am Zeilenanfang steht) — dieselbe Verwechslung wie beim Selektor, eine Ebene
    # tiefer: die richtige Stelle ist gefunden, aber der falsche Name gelesen.
    definitionen = [(erster, wert) for erster, _, body in _alle_regeln()
                    for wert in [re.search(r"(^|;|\s)--settings-title-gap\s*:\s*([^;]+)", body)]
                    if wert]
    assert len(definitionen) == 1, definitionen
    assert definitionen[0][0] == ".settings-chain", definitionen
    wert = definitionen[0][1].group(2).strip()
    assert re.fullmatch(r"calc\(var\(--space\) \* \d+(\.\d+)?\)", wert), (
        f"der Titelabstand muss ein Vielfaches von --space sein, gefunden {wert!r}"
    )
    # Und **genau zweimal verwendet**, an genau diesen beiden Regeln. Ein dritter Verwendungsort
    # wäre eine stille Erweiterung, eine zweite Definition eine Kopie; beides zählt hier über
    # die Body-Suche, nicht über eine Zahl im Kommentar.
    verwendung = sorted({erster for erster, _, body in _alle_regeln()
                         if "--settings-title-gap" in body
                         and "--settings-title-gap:" not in body})
    assert verwendung == ["#settings-menu h2", "#settings-space-detail h2"], verwendung
    # Und beide Regeln benutzen ihn wirklich als `margin-bottom` — sonst stünde der Wert
    # irgendwo im Selektor-Teil einer Regel und täte nichts.
    for selektor in ("#settings-menu h2", "#settings-space-detail h2"):
        regeln = [b for b in _bare_rule_bodies(selektor)]
        assert regeln, f"keine eigene Regel für {selektor}"
        assert any(_eigenschaft(b, "margin-bottom") == "var(--settings-title-gap)" for b in regeln), (
            f"{selektor} benutzt den gemeinsamen Titelabstand nicht als margin-bottom: {regeln}"
        )


def test_the_unselected_menu_item_takes_the_input_surface_verbatim():
    """P9-AN + P9-AO (2026-10-05, Nikinger): die unausgewählten Menüpunkte bekommen **die
    Fläche des Eingabefeldes**, die ausgewählten behalten den Auswahlzustand.

    **Der Token-Name wird nicht abgetippt, sondern verglichen.** Der Wächter liest den
    Hintergrund der `.input`-Regel aus dem Stylesheet und verlangt, dass die Menüregel
    *denselben* Wert nennt. Ein abgetippter Name (`var(--sunken)`) wäre eine zweite Kopie
    der Aussage: änderte die `.input`-Regel ihren Wert, bliebe der Wächter grün und die
    Menüpunkte hätten eine Fläche, die es im Panel nicht mehr gibt.

    Ebenso die Kante — und zwar aus demselben Grund, mit dem die Kurzform `border` verboten
    bleibt: `--line-strong` kommt aus der `.input`-Regel, `border` (die Kurzform) würde
    Breite und Stil mittragen und damit die an die Baumzeile gebundene Geometrie verändern.
    Das ist die einzige **Abweichung** vom Plantext (§10 führte `border-color` nicht als
    erlaubt auf, P9-97 vergleicht aber ausdrücklich „Hintergrund **und** Kante") und sie ist
    dort mit Grund notiert.

    Die **Geometrie** prüft `test_settings_menu_items_reuse_the_tree_row_look()`, die
    **Wirkung** misst die Browser-Probe (S10, S12)."""
    css = _css_code()
    input_bodies = _bare_rule_bodies(".input")
    assert input_bodies, "keine Basis-Regel für .input"
    eingabeflaeche = _eigenschaft(input_bodies[0], "background")
    eingabekante = _eigenschaft(input_bodies[0], "border")
    assert eingabeflaeche and eingabekante, (eingabeflaeche, eingabekante)
    # Die Kante der `.input` ist die **Kurzform** — der Wert, den die Menüregel als
    # `border-color` übernimmt, ist deren Farbanteil.
    farbanteil = eingabekante.split()[-1]
    assert farbanteil.startswith("var("), eingabekante

    eigene = _rule_bodies(css, '.settings-menu__item:not([aria-current="true"])', own_only=True)
    assert len(eigene) == 1, (
        f"genau eine eigene Regel für die unausgewählten Menüpunkte erwartet, gefunden {len(eigene)}"
    )
    body = eigene[0]
    assert _eigenschaft(body, "background") == eingabeflaeche, (
        f"die Fläche der Menüpunkte ({_eigenschaft(body, 'background')!r}) ist nicht die des "
        f"Eingabefeldes ({eingabeflaeche!r})"
    )
    assert _eigenschaft(body, "border-color") == farbanteil, (
        f"die Haarlinie der Menüpunkte ({_eigenschaft(body, 'border-color')!r}) ist nicht die des "
        f"Eingabefeldes ({farbanteil!r})"
    )
    # Und **kein** Schatten: die Vertiefung ist die Fläche, der Schatten wäre die Plastik
    # des Feldes, und P9-97 vergleicht Hintergrund und Kante.
    assert _eigenschaft(body, "box-shadow") is None, body
    # P9-AO: der Auswahlzustand ist **unberührt** — dieselbe eine Regel wie die Baumzeile, und
    # ohne `:not(…)`: die Auswahlregel ist nicht „die Menüregel minus ausgewählt", sondern die
    # Baumzeilenregel. (Die `:not`-Ausschluss-Form taucht im Stylesheet an anderer Stelle auf —
    # in P9-ANs *un*ausgewählten Menüpunkten — und würde hier sonst fälschlich als Umstellung
    # der Auswahlregel gemeldet.)
    auswahl = [(erster, body) for erster, selectors, body in _alle_regeln()
               if '.settings-menu__item[aria-current="true"]' in selectors]
    assert len(auswahl) == 1, auswahl
    assert ":not" not in auswahl[0][0], auswahl[0][0]
    assert auswahl[0][1] == _rule_bodies(css, '.tree__folder[aria-current="true"]')[0], (
        "die Auswahlregel der Menüpunkte weicht von der der Baumzeile ab"
    )


def test_the_menu_label_is_centered_and_the_icon_button_is_named():
    """P9-AP + P9-AQ (2026-10-05, Nikinger): die Beschriftung der Menüknöpfe steht mittig, und
    „Zurück" trägt ein **echtes Icon** statt des Textpfeils.

    **Mittig auf einer Flex-Achse, nicht mit `text-align`.** Der Menüknopf ist `display: flex`
    (Sammelregel mit `.tree__folder`), und sein einziges Kind ist ein **anonymer Flex-Item** —
    ein Textknoten. `text-align: center` wirkt auf Blockcontainer; im Flex-Item zentriert es
    einen Text in sich selbst und **sichtbar nichts**. Die erste Fassung des Baus hatte genau
    das, und die erste Browser-Probe maß die Textmitte **8,5 px neben** der Knopfmitte (S11).
    Der Wächter prüft deshalb beides: dass `justify-content: center` dasteht, dass
    **`text-align` nicht** dasteht (eine Deklaration, die nichts tut, ist die zweite
    Wahrheit über denselben Zustand) und dass der Knopf überhaupt ein Flexcontainer ist —
    ohne die dritte Bedingung dürfte jemand die Sammelregel auf `display: block` umstellen und
    der Wächter bliebe grün.

    **Und das Polster, Nikinger-Entscheidung vom selben Tag.** Als `.tree__folder` erbte der
    Menüpunkt `padding-left: 32px` — die Einrückung der Baumzeile — und lag damit 12 px neben
    der Knopfmitte; exakt mittig ging nur mit symmetrischem Polster. Entscheidung: **beidseitig
    `--space`**. Geprüft wird deshalb, dass `padding-left` **genau** den Wert der Sammelregel
    trägt (jeder andere wäre Geometrie unter neuem Namen) und dass rechts kein eigenes Polster
    steht. Was das kostet — der Menüpunkt ist in *diesem* Wert nicht mehr die Baumzeile —, steht
    am Stylesheet und in der Browser-Messung S1, die den linken Wert jetzt gegen `--space`
    prüft statt gegen die Baumzeile.

    **Der Textpfeil `←` war eine Glyphe und hing sichtbar nach unten** — das ist der Grund für
    den Icon-Wechsel und nicht die Form der Beschriftung. Geprüft wird deshalb beides: dass
    `&larr;` **weg** ist (sonst stünde er als Text im Knopf neben dem Icon) und dass das Icon
    **da** ist.

    **Die Zugänglichkeit bleibt, obwohl der Text weg ist:** `title` **und** `aria-label` sind
    gesetzt. `aria-label` ist das, was ein Screenreader vorliest; `title` ist der native
    Tooltip. Fehlt eines, wäre der Knopf für einen Screenreader beschriftungslos — und das
    fällt in keinem Screenshot auf, also muss es hier stehen.

    Die Zentrierung **im Knopf** misst die Probe (S11: Textmitte gegen Knopfmitte, S12:
    Iconmitte); hier steht die Ursache."""
    css = _css_code()
    eigene = _rule_bodies(css, ".settings-menu__item", own_only=True)
    zentriert = [b for b in eigene if _eigenschaft(b, "justify-content") == "center"]
    assert len(zentriert) == 1, f"genau eine eigene Ausrichtungsregel erwartet: {eigene}"
    assert _eigenschaft(zentriert[0], "text-align") is None, (
        f"text-align in einer eigenen Menüpunkt-Regel: {zentriert[0]} — auf einem Flexcontainer "
        f"bewirkt es nichts, und eine Deklaration, die nichts bewirkt, ist die zweite "
        f"Wahrheit über denselben Zustand"
    )
    # Der Knopf **muss** ein Flexcontainer sein — sonst greift `justify-content` nicht und
    # die Zentrierung verschwände, ohne dass eine Assertion anschlägt.
    sammel = [b for s, sel, b in _alle_regeln() if ".settings-menu__item" in sel
              and len(sel) > 1]
    assert sammel and any(_eigenschaft(b, "display") == "flex" for b in sammel), (
        "die Sammelregel mit .tree__folder traegt kein `display: flex` mehr — P9-APs "
        "Ausrichtung hinge dann an einer leeren Deklaration"
    )

    html = _html()
    for panel in ("settings-password", "settings-spaces", "settings-space-detail", "settings-updates"):
        block = _element_by_id(html, panel)
        knopf = re.search(
            r'<button[^>]*class="[^"]*\bsettings-back\b[^"]*"[^>]*>.*?</button>',
            block, flags=re.DOTALL)
        assert knopf is not None, f"kein Zurück-Knopf in #{panel}"
        markup = knopf.group(0)
        assert '<use href="#i-chevron-left">' in markup, markup
        assert "larr" not in markup and "\u2190" not in markup, (
            f"#{panel}: der Textpfeil ist noch im Knopf — P9-AQ ersetzt ihn durch das Icon"
        )
        assert 'class="btn btn--icon settings-back"' in markup, markup
        # `_element_by_id()` löst die Entities auf — die Vergleichsform ist hier deshalb das
        # **Zeichen** `ü`, nicht `&uuml;`. (Die erste Fassung verglich gegen die Entity und
        # meldete vier Panels ohne Beschriftung, während die Attribute im Markup dastanden.)
        assert 'aria-label="Zurück"' in markup, f"#{panel}: aria-label fehlt"
        assert 'title="Zurück"' in markup, f"#{panel}: title fehlt"
    # Das Icon existiert wirklich — und als **eigenes** Symbol, nicht als Drehung.
    sprite = re.search(r"<!-- ICONS:BEGIN -->(.*?)<!-- ICONS:END -->", html, flags=re.DOTALL)
    assert sprite is not None
    symbol = re.search(
        r'<symbol id="i-chevron-left"[^>]*>\s*<path d="([^"]+)"', sprite.group(1))
    assert symbol is not None, "kein i-chevron-left im Sprite"
    assert symbol.group(1) == "m15 18-6-6 6-6", (
        f"der Pfad muss der Spiegel von i-chevron-right (m9 18 6-6-6-6) sein, "
        f"gefunden {symbol.group(1)!r}"
    )
    # Und es steht in der `KNOWN`-Liste: die Liste ist die Spur aller benutzten Symbole.
    assert '"chevron-left"' in _js("icons.js"), "chevron-left fehlt in der KNOWN-Liste"
    # Keine eigene Optik für den Zurück-Knopf: `.btn--icon` zentriert das Icon, eine Regel
    # hier wäre die zweite Wahrheit über dieselbe Sache.
    for body in _rule_bodies(css, ".settings-back", own_only=True):
        for prop in ("width", "height", "padding", "justify-content", "align-items"):
            assert _eigenschaft(body, prop) is None, (prop, body)


def test_only_the_settings_chain_aligns_its_buttons_right():
    """P9-AS (2026-10-05, Nikinger): **alle** Knöpfe in den Einstellungs-Fenstern stehen rechts
    — und die anderen Overlays bleiben, wie sie waren.

    Der Lock nennt genau diesen Umfang („nicht in den anderen Overlays"), und genau der ist der
    Teil, den ein Wächter sonst übersieht: `justify-content: flex-end` in der **unscoped**
    `.overlay__actions`-Regel hätte denselben Anker und dieselbe Wirkung an fünf Stellen mehr,
    darunter im modalen Entfernen-Dialog, der P9-AK ausdrücklich als eigenes Fenster führt.

    Die Wirkung misst die Probe (S13/S14: Knopf-Mitte rechts vom Feld, und die Boxen von
    „Space entfernen" und der letzten „(schreiben)"-Zeile überlappen sich nicht). Hier steht,
    dass die Regel **scoped** ist und dass die Basis-Regel ihre Ausrichtung nicht mitbekommt."""
    css = _css_code()
    scoped = _bare_rule_bodies(".settings-chain .overlay__actions")
    assert len(scoped) == 1, f"genau eine eigene Regel erwartet, gefunden {len(scoped)}"
    assert _eigenschaft(scoped[0], "justify-content") == "flex-end", scoped
    # Die Basis-Regel darf **keine** Ausrichtung tragen — sonst gälte sie überall.
    for body in _bare_rule_bodies(".overlay__actions"):
        assert _eigenschaft(body, "justify-content") is None, (
            f"die unscoped .overlay__actions-Regel richtet jetzt ihre Knöpfe aus: {body}"
        )
    # Kein anderer Overlay wird von der Kette erwischt: **keine** `.overlay__actions`-Regel
    # außerhalb der Kette richtet ihre Knöpfe aus. (Der erste Entwurf prüfte *jede* Regel mit
    # `justify-content: flex-end` im ganzen Stylesheet und meldete `.overview__space-counts`
    # aus der Übersicht — dieselbe Fehlerklasse wie die Bilanz-Prüfung, die eine Zahl suchte,
    # die sie prüft, im falschen Dokument aber findet.)
    for erster, selectors, body in _alle_regeln():
        if _eigenschaft(body, "justify-content") != "flex-end":
            continue
        if any(".overlay__actions" in s for s in selectors):
            assert erster.startswith(".settings-chain"), (
                f"eine Ausrichtungs-Regel an .overlay__actions ausserhalb der Kette: {erster}"
            )
    # Der Entfernen-Dialog ist ein **eigenes** Fenster (P9-AK) und trägt die Kette nicht.
    assert "space-remove-dialog" not in css or not re.search(
        r"space-remove-dialog[^{}]*\{", css), "der Entfernen-Dialog hängt an der Kette"


def test_the_escape_chain_knows_the_settings_chain_as_one_dialog():
    """P9-AH: ESC schließt das **rechteste** Panel; die Kette ist für die Tastatur **ein**
    Dialog. `anyOverlayOpen()` und die ESC-Kette in `app.js` müssen sie deshalb als eine
    Einheit kennen — sonst gäbe es einen Dialog, den ESC nicht schließt.

    Geprüft wird zusätzlich die **Reihenfolge**: das modale Entfernen-Fenster
    (`#space-remove-dialog`) steht **über** der Kette (Plan §0.3) und muss deshalb **vor**
    `closeRightmost()` geprüft werden. Andernfalls schlöß ein ESC das Entfernen-Fenster *und*
    das Panel darunter in einem Tastendruck — ein Fehler, den kein Markup-Test sieht."""
    app = _js("app.js")
    assert 'document.getElementById("settings-overlay")' in app
    assert "settingsOverlayEl.hidden" in app
    # Genau eine Zeile, in der die Kette als Dialog gilt — keine drei Einzelzweige mehr.
    assert not re.search(r"accountDialogEl|spaceAdminDialogEl|updateLogDialogEl", app), (
        "die drei alten Dialog-IDs dürfen in app.js nicht mehr vorkommen"
    )
    escape_block = app.split('if (event.key === "Escape")')[1].split("if (event.key === \"/\")")[0]
    assert escape_block.count("settingsOverlayEl.hidden") == 1, escape_block
    assert "closeRightmost()" in escape_block, escape_block
    remove_at = escape_block.index("closeRemoveSpaceDialog()")
    chain_at = escape_block.index("closeRightmost()")
    assert remove_at < chain_at, (
        "das Entfernen-Fenster liegt über der Kette und muss im ESC-Zweig zuerst stehen"
    )


def test_only_one_module_opens_a_panel():
    """**Eigener Fund beim Bauen (2026-10-05), als Wächter aufgestellt.** Beim ersten Umbau
    hingen **zwei** `click`-Listener auf demselben Menüknopf: `app.js` öffnete
    `openSpaceAdminDialog()`, `settings.js` schaltete um. Beide liefen bei jedem Klick — der
    Knopf hätte sich nie geschlossen (öffnen, dann schließen) und der Reset hätte doppelt
    stattgefunden.

    Die Lehre ist nicht „kein Doppel-Listener", sondern: **es gibt genau einen Öffner**.
    Wer ein Panel öffnet, übergibt seinen Zustands-Reset als `prepare` an `settings.js`
    (`registerPanel`), statt selbst am DOM zu drehen oder selbst zuzuhören.

    Geprüft wird, dass `openPanel` nur in `settings.js` aufgerufen wird und dass die drei
    Eigentümer sich über `registerPanel` anmelden — beides statisch, weil ein zweiter Öffner
    genau die Art Fehler ist, die im Bild nicht auffällt (es sieht ja „richtig" aus)."""
    settings = _js("settings.js")
    callers = {}
    for name in ("app.js", "dialogs.js", "spaces.js", "updates.js", "editor.js", "list.js",
                 "tree.js", "graph.js", "state.js", "toasts.js"):
        source = _js(name)
        uses = len(re.findall(r"\bopenPanel\(", source))
        if uses:
            callers[name] = uses
    assert callers == {}, f"openPanel() wird außerhalb von settings.js benutzt: {callers}"
    assert "export function openPanel(" in settings

    for name, panel in (("dialogs.js", "password"), ("spaces.js", "spaces"),
                        ("updates.js", "updates")):
        source = _js(name)
        assert f'registerPanel("{panel}"' in source, (
            f"{name} meldet seinen Reset für '{panel}' nicht an"
        )
