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
from pathlib import Path

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


def _element_by_class(html: str, klasse: str) -> str:
    """Der Tag mit dieser Klasse, samt Inhalt, oder Fehler — Gegenstück zu `_element_by_id`.

    Gebraucht für P9-AU (der Wrapper `.settings-menu__list`): der Test will **beide** Hälften
    desselben Tags lesen — dass die drei Punkte darin stehen *und* dass kein Knopf einen eigenen
    unteren Außenabstand trägt — und das ergibt erst der Elementinhalt, nicht der Tag allein.
    """
    match = re.search(
        rf'<(?P<tag>[a-zA-Z0-9]+)\b[^>]*\bclass="{re.escape(klasse)}"[^>]*>'
        rf'(?P<body>.*?)</(?P=tag)>',
        html,
        flags=re.DOTALL,
    )
    assert match is not None, f'Element mit class="{klasse}" nicht gefunden'
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
#
# **[2026-10-06, P9-BB: die Ausnahme von oben ist damit fällig — und die Liste wächst um vier
# Eigenschaften, damit das nicht durch eine Lücke geht.]**
#
#   * `padding-block` ist **erlaubt, aber nur mit dem einen gelockten Wert**
#     (`ERLAUBTES_PADDING_BLOCK_PRO_SELECTOR`). Der Menüpunkt ist seit P9-BB **flacher**
#     (4 px statt 6 px oben/unten; gemessene Höhe 35,69 px → 31,69 px), und das ist die erste
#     bewusste Abweichung von P9-AFs „Höhe aus `.tree__folder`". Das Gegenstück dazu ist der
#     Wächter: er erlaubt nicht die Eigenschaft, sondern den **Wert**.
#   * **`margin` stand nur als Kurzform auf der Liste** — `margin-bottom: …` fiel am Wächter
#     vorbei, denn die Verbotsliste wird **namensgenau** geprüft (`margin\s*:` matcht `margin-bottom`
#     nicht). Das war am 2026-10-06 an einer eingebauten Zeile aufgefallen: der Test behauptete
#     „diese Form wird rot" und die Form war grün. Die drei Langformen stehen jetzt **auch** dort.
#   * **`padding-block` stand vorher auf keiner Liste.** Eine Eigenschaft, die kein Wächter kennt,
#     meldet kein Wächter — die Lücke ist hier ausdrücklich geschlossen: die Langformen
#     `padding-block-start`/`-end` stehen jetzt auf der Verbotsliste und ebenso die logischen
#     Längsformen `padding-inline*`, die sonst der Umweg um `padding-left` wären.
VERBOTENE_OPTIK = ("height", "padding", "padding-top", "padding-bottom", "padding-right",
                    "padding-block-start", "padding-block-end",
                    "padding-inline", "padding-inline-start", "padding-inline-end",
                    "border-radius", "font", "margin", "margin-top", "margin-right",
                    "margin-bottom",
                    "line-height", "border")
# **[2026-10-05, P9-AV]** Zwei Eigenschaften sind aus dieser Liste **heraus** und in je einer
# Form wieder eingeschleust worden — nicht pauschal erlaubt:
#
#   * `box-shadow` — erlaubt ist **nur** der 1-px-Innenschatten der Standardfläche (derselbe
#     wie in `.btn`). Ein **äußerer** Schatten bleibt verboten: der wäre die Plastik, die der
#     Nikinger am 2026-10-05 mit „they are buttons and not fields to type something in" abgelehnt
#     hat — und die Feld-Fläche hatte ihn vorher ausdrücklich nicht.
#   * `color` — erlaubt ist **nur auf der Auswahlregel** und **nur** der Wert, den `.btn-primary`
#     selbst trägt. Ohne das wäre die Akzentfläche mit `--text-muted` beschriftet, also mit der
#     gedämpften Rail-Farbe auf blauem Grund.
#
# Die Formulierung „keine eigene Optik" wäre nach dieser Änderung eine Unwahrheit; die alte
# Verbotsliste steht deshalb nicht mehr als geltende Fassung im Docstring, sondern wird hier
# abgelöst.
ERLAUBTE_INNENSCHATTEN = ("inset", "rgba(255,255,255,", "var(--btn-lift)")
# Erlaubt sind ausschliesslich Flaeche, Ausrichtung, die linke Polsterkante (s. o.) und die
# **Haarlinie** des Standardknopfes. `border-color` ist bewusst erlaubt und `border` (die
# Kurzform) bewusst nicht: die Kurzform traegt Breite und Stil und koennte damit genau die
# Geometrie veraendern, die P9-AF an die Baumzeile bindet. Die Flaeche **ohne** Haarlinie
# waere zudem nicht die des Standardknopfes, sondern eine neue.
ERLAUBTE_OPTIK = ("background", "background-color", "background-image", "border-color",
                  "text-align", "padding-left")
TEXT_ALIGN_WERTE = ("left", "center", "right", "start", "end")
# Der einzige erlaubte Wert fuer `padding-left` — der der Sammelregel, mit der die Kette
# anfaengt. Alles andere waere eine eigene Polsterkante und damit Geometrie unter neuem Namen.
ERLAUBTES_PADDING_LEFT = "var(--space)"
# **[2026-10-05, P9-AX]** Der erlaubte linke Polsterwert ist **je Selektor verschieden**, und das
# ist der Punkt: der Menuepunkt traegt `var(--space)` (Nikinger-Entscheidung vom 2026-10-05,
# beidseitiges Polster, damit die mittige Beschriftung echt mittig liegt), die **Space-Zeile**
# `0` — ihre Beschriftung soll auf der Inhaltskante des Panels stehen, also buendig mit dem
# Panel-Titel, und nicht 32 px daneben (das geerbte Einzugs-Polster der Baumzeile). Ein
# einziger全局 erlaubter Wert koennte nicht beides sein.
# **[2026-10-06, P9-BF]** Die Space-Zeile traegt jetzt `var(--space)` statt `0`, **und** einen
# negativen `margin-left` in genau derselben Hoehe (siehe `_optik_verstoss`). Zusammen wandert das
# **Kaestchen** 8 px nach links, die **Beschriftung bleibt buntig mit dem Titel** (P9-AX) — vorher
# standen innen 1 px links gegen 9 px rechts, und genau die linke Kante war sein Punkt.
ERLAUBTES_PADDING_LEFT_PRO_SELECTOR = {
    ".settings-menu__item": "var(--space)",
    ".settings-space-row": "var(--space)",
}
# **Und derselbe Wert als Aussenabstand, negativ** — ein Whitelist-Eintrag pro Selektor, wie beim
# Polster. `None` heißt: die Eigenschaft hat hier nichts verloren (die Menuepunkte duerfen keinen
# negativen Aussenabstand tragen; das waere eine zweite Wahrheit ueber dieselbe Kante).
ERLAUBTES_MARGIN_LEFT_PRO_SELECTOR = {
    ".settings-menu__item": None,
    ".settings-space-row": "calc(var(--space) * -1)",
}
# **[2026-10-06, P9-BB]** Das vertikale Polster ist je Selektor **geschlossen** geregelt: der
# Menüpunkt darf genau **einen** Wert setzen, die Space-Zeile **keinen**. `None` heißt „diese
# Eigenschaft hat hier nichts verloren" — und das ist eine Aussage, kein Versehen: die Space-Zeile
# ist eine Baumzeile mit Linkspolster 0, ihre Höhe kommt aus derselben Sammelregel wie beim
# Menüpunkt **vor** P9-BB. Ein `padding-block` an der Zeile wäre eine dritte Höhenquelle, und
# genau die hat P9-AF abgeschafft.
ERLAUBTES_PADDING_BLOCK_PRO_SELECTOR = {
    ".settings-menu__item": "calc(var(--space) * 0.5)",
    ".settings-space-row": None,
}


def _koerper_mit(bodies: list[str], eigenschaft: str) -> str | None:
    """Der **erste** Regel-Body, der die Eigenschaft überhaupt nennt.

    **Der Grund ist derselbe wie bei `_farbe_von_btn_primary`:** `.btn` steht in der
    Übergangs-Sammelregel, und `_bare_rule_bodies(".btn")[0]` ist deshalb der `transition`-Body
    — ohne `background`, ohne `border`, ohne `box-shadow`. Ein Wächter, der `[0]` nimmt, prüft
    die falsche Regel und ist an korrektem Code rot; die erste Fassung dieses Tests war genau so
    gebaut und hat 14 Wächtergrün gegen eine leere Aussage eingetauscht.
    """
    for body in bodies:
        if _eigenschaft(body, eigenschaft):
            return body
    return None


def _farbe_von_btn_primary(css: str) -> str | None:
    """Die `color`-Deklaration der `.btn-primary`-Regel — **gelesen**, nicht abgetippt.

    Grund: `#fff` steht hier als erlaubter Wert, und ein abgetipptes `color` wäre die zweite Kopie
    der Aussage. Änderte `.btn-primary` seine Schriftfarbe, bliebe der Wächter grün und die
    Menüpunkte behielten eine andere. Dasselbe Muster wie beim Flächen-Vergleich — dort wird der
    Name verglichen, nicht der Wert.

    **Über alle eigenen Regeln des Selektors iterieren, nicht über die erste:** `.btn-primary`
    steht auch in der Übergangs-Sammelregel (`transition`), und die *erste* eigene Regel ist
    deshalb die mit `transition` — ohne `color`. Die erste Fassung dieses Helpers nahm `[0]` und
    gab `None` zurück; der Wächter, der es braucht, wäre dann an korrekter Welt rot.
    """
    for body in _rule_bodies(css, ".btn-primary", own_only=True):
        farbe = _eigenschaft(body, "color")
        if farbe:
            return farbe
    return None


def _ebenen(value: str) -> list[str]:
    """Die Schatten-Ebenen eines `box-shadow`-Werts — **mit Klammer-Tiefe**.

    Der erste Entwurf hat an jedem Komma getrennt und damit `rgba(255,255,255,.06)` in drei
    Stücke gerissen; der Wächter meldete daraufhin **korrekten** Code als Verstoß. Ein Mess- oder
    Wächterfehler, der aussieht wie ein Befund — die Fehlerklasse, die in diesem Block fünfmal
    vorkam.
    """
    ebene, tiefe, gefunden = "", 0, []
    for zeichen in value:
        if zeichen == "(":
            tiefe += 1
        elif zeichen == ")":
            tiefe -= 1
        if zeichen == "," and tiefe == 0:
            gefunden.append(ebene.strip())
            ebene = ""
        else:
            ebene += zeichen
    if ebene.strip():
        gefunden.append(ebene.strip())
    return gefunden


def _schatten_verstoss(body: str) -> list[str]:
    """Alle Schatten-Deklarationen, die **kein** Innenschatten der Standardfläche sind."""
    verstoesse: list[str] = []
    for match in re.finditer(r"(^|[;{\s])box-shadow\s*:\s*([^;]*)", body):
        wert = match.group(2).strip()
        for ebene in _ebenen(wert):
            if any(teil in ebene for teil in ERLAUBTE_INNENSCHATTEN):
                continue
            verstoesse.append(f"box-shadow: {ebene!r} (erlaubt ist nur der Innenschatten)")
    return verstoesse


def _optik_verstoss(body: str, tokens: set[str], erlaubte_color: str | None = None,
                    erlaubtes_padding_left: str = ERLAUBTES_PADDING_LEFT,
                    erlaubtes_padding_block: str | None = None,
                    erlaubtes_margin_left: str | None = None) -> list[str]:
    """Alle Verstoesse eines Regel-Bodys: verbotene Eigenschaften, erlaubte Eigenschaften
    mit einem Wert, der **kein** vorhandenes Token ist, und die beiden Polster-Ausnahmen mit
    ihrem je Selektor gelockten Wert.

    Der zweite Teil ist der Grund, warum „erlaubt" nicht genug waere: `background: #0C1015`
    waere formal erlaubt und waere genau die dritte Variante, die P9-AF abschaffen wollte — nur
    eben eine fuer die Farbe statt fuer die Optik.

    **`padding-block` wird hier und nicht in `ERLAUBTE_OPTIK` behandelt:** es ist die einzige
    erlaubte Eigenschaft, die **nur einen Token-Ausdruck** haben darf und sonst nichts — der
    Token-Check der Sammelliste wuerde jede andere Form (etwa `4px` ohne `--space`) durchlassen
    bzw. die richtige Form als „kein Token" melden. Deshalb steht es mit einem **eigenen**
    Vergleich da, genau wie `padding-left` (2026-10-06, P9-BB)."""
    verstoesse: list[str] = []
    for prop in VERBOTENE_OPTIK:
        if re.search(rf"(^|[;{{\s]){prop}\s*:", body):
            verstoesse.append(f"verboten: {prop}")
    verstoesse += _schatten_verstoss(body)
    # `color` ist nur auf der Auswahlregel erlaubt, und nur als der Wert aus `.btn-primary`.
    for match in re.finditer(r"(^|[;{\s])color\s*:\s*([^;]*)", body):
        wert = match.group(2).strip()
        if erlaubte_color is None or wert != erlaubte_color:
            verstoesse.append(f"color: {wert!r} (erlaubt ist nur der Wert aus .btn-primary)")
    # `padding-block`: **nur** mit dem gelockten Wert dieses Selektors (P9-BB). `None` oder ein
    # anderer Wert ist ein Verstoess — auch das Fehlen einer Ausnahme wird damit geprueft.
    for match in re.finditer(r"(^|[;{\s])padding-block\s*:\s*([^;]*)", body):
        wert = match.group(2).strip()
        if wert != erlaubtes_padding_block:
            verstoesse.append(
                f"padding-block: {wert!r} (erlaubt ist hier nur "
                f"{erlaubtes_padding_block!r})"
            )
    # **`margin-left` ist derselbe Fall wie `padding-block` (P9-BF)** und war vorher auf **keiner**
    # Liste: die Kurzform `margin` steht auf der Verbotsliste, `margin-left` ist davon nicht
    # erfasst -- es fiel also durch, ohne dass jemand es verboten hatte. Erlaubt ist **nur** der
    # gelockte negative Wert dieses Selektors, und an den Menuepunkten gar keiner.
    for match in re.finditer(r"(^|[;{\s])margin-left\s*:\s*([^;]*)", body):
        wert = match.group(2).strip()
        if wert != erlaubtes_margin_left:
            verstoesse.append(
                f"margin-left: {wert!r} (erlaubt ist hier nur "
                f"{erlaubtes_margin_left!r})"
            )
    for match in re.finditer(rf"(^|[;{{\s])({"|".join(ERLAUBTE_OPTIK)})\s*:\s*([^;]*)", body):
        prop, wert = match.group(2), match.group(3).strip()
        if prop == "text-align":
            if wert not in TEXT_ALIGN_WERTE:
                verstoesse.append(f"text-align: {wert!r}")
            continue
        if prop == "padding-left":
            if wert != erlaubtes_padding_left:
                verstoesse.append(
                    f"padding-left: {wert!r} (erlaubt ist nur {erlaubtes_padding_left})"
                )
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

    **Beide Lesarten, mit Datum — der Wächter wurde am 2026-10-05 zweimal umgebaut, und
    zwar jeweils im selben Commit wie der Bau.**

    *Erster Umbaut (P9-AN, gleicher Tag):* vorher stand `background` auf der Verbotsliste. Neu
    verboten sind nur noch **Geometrie, Textfarbe, Kanten-Kurzform und äußerer Schatten**;
    erlaubt sind Fläche, Haarlinie und `text-align` — und eine Fläche **nur** aus einem Token,
    das `app.css` in `:root` auch wirklich definiert.

    *Zweiter Umbaut (P9-AV, derselber Tag, **wieder auf Nikinger-Anordnung**):* P9-AV hat P9-AN
    umgedreht — die Fläche ist nicht mehr die des Eingabefeldes, sondern die des **Standardknopfes**,
    und die **Auswahl** trägt die Akzentfläche. Deshalb ist auch `color` in einer Form wieder
    erlaubt: nur auf der Auswahlregel, nur mit dem Wert aus `.btn-primary` (gelesen, nicht
    abgetippt), und ein **äußerer** Schatten bleibt verboten.

    *Dritter Umbaut (P9-BB, 2026-10-06, **wieder auf Nikinger-Anordnung**):* zu *„the update-log
    button is still bigger, I think you need to decrease its height"* hat er **(b)** gewählt —
    *zusätzlich flacher*, also ein eigenes vertikales Polster (`padding-block`, 4 px). Damit ist
    die Höhe des Menüpunkts zum ersten Mal **nicht mehr** die der Baumzeile (31,69 px gegen
    35,69 px, gemessen), und „P9-AF bindet die Höhe an `.tree__folder`" ist damit **an dieser
    einen Stelle überholt**. Der Wächter gibt der Eigenschaft nicht das Recht, sondern den
    **Wert**: `padding-block: calc(var(--space) * 0.5)` am Menüpunkt, sonst nirgends.

    **Was P9-AF weiterhin bindet** und dieser Wächter weiterhin prüft: die drei Punkte tragen
    `.tree__folder` im Markup, und **keine eigene** Rundung, Schrift, Höhe, kein `margin`, kein
    `border`, kein **äußerer** Schatten, keine eigene Textfarbe außer auf der Auswahlregel.
    Die Formulierung „keine eigene Geometrie" wäre seit P9-AN eine Unwahrheit, und seit P9-BB
    erst recht — sie steht deshalb nicht mehr im Docstring, sondern wird hier abgelöst."""
    html = _html()
    css = _css()
    for element_id, _ in MENU_ITEMS:
        block = _element_by_id(html, element_id)
        assert "tree__folder" in block, f"{element_id} traegt nicht .tree__folder: {block}"
        assert "settings-menu__item" in block, element_id
    tokens = _tokens()
    erlaubte_color = _farbe_von_btn_primary(_css())
    assert erlaubte_color, "die .btn-primary-Regel nennt keine color — der Wächter kann nichts erlauben"
    flaeschen_woerter = 0
    for selector in (".settings-menu__item", ".settings-space-row"):
        rules = _rule_bodies(css, selector, own_only=True)
        assert rules, f"{selector} hat keine eigene Regel im Stylesheet"
        for body in rules:
            # **Nur die Auswahlregel** darf eine eigene Schriftfarbe tragen (P9-AV): sie legt
            # die Akzentfläche und braucht darum eine helle Beschriftung. Jede andere eigene
            # Regel der Kette erbt die Farbrolle der Sammelregel.
            ist_auswahl = "aria-current" in selector and ":not(" not in selector
            verstoesse = _optik_verstoss(
                body, tokens,
                erlaubte_color if ist_auswahl else None,
                ERLAUBTES_PADDING_LEFT_PRO_SELECTOR[selector],
                ERLAUBTES_PADDING_BLOCK_PRO_SELECTOR[selector],
                ERLAUBTES_MARGIN_LEFT_PRO_SELECTOR[selector])
            assert not verstoesse, (selector, verstoesse, body)
            flaeschen_woerter += len(re.findall(r"(^|[;{\s])background\s*:", body))
    # **Und die Flaeche, die P9-AV verlangt, ist auch da.** Ein Wächter, der nur verbietet,
    # waere nach einem Revert des Baus immer noch gruen — er wuerde dann die *Abwesenheit*
    # des Verstosses melden und die Abwesenheit der Loesung verschweigen. Fuer die
    # Space-Zeilen ist das nicht verlangt (P9-AV nennt nur die Menuepunkte), also mindestens eine.
    assert flaeschen_woerter >= 1, (
        "keine eigene Regel setzt eine Hintergrundflaeche — P9-AV (unausgewaehlter "
        "Menuepunkt traegt die Flaeche des Standardknopfes) waere nicht gebaut"
    )


def test_the_menu_item_watchdog_bites_on_built_in_violations():
    """**Der Wächter wird an eingebauten Verstößen geprüft, nicht an vertrauensvollem Code.**

    Fünfzehn Zeilen, die keine Phase-9-Datei enthält, deren jede aber rot werden muss. Grund: P9-AN
    hat diesen Wächter von einem *Verbot* auf eine *Erlaubnis mit Bedingung* umgestellt
    (`background` ist erlaubt, `background: #0C1015` nicht), und P9-AV hat `box-shadow` und
    `color` in derselben Weise entschärft (Innenschatten erlaubt, äußerer nicht), und P9-BB hat
    mit `padding-block` eine ganze Eigenschaft dazugebracht. Ein Verbot kann
    man lesen und glauben; eine Erlaubnis mit Bedingung prüft man nur, indem man die Bedingung
    verletzt — sonst steht am Ende ein Wächter, der alles erlaubt, was niemand verboten hat.

    **[2026-10-05, P9-AV: zwei Fälle geändert, weil die alte Verbotsliste sie für erlaubt hielt]** —
    `eigener Schatten` ist jetzt ein **äußerer** (`box-shadow: 0 1px 0 rgba(0,0,0,.5)`), und
    `eigene Textfarbe` wird **zwei** Mal geprüft: einmal mit einer fremden Farbe (muss rot werden)
    und einmal mit der Farbe aus `.btn-primary` **in einer Nicht-Auswahlregel** (muss ebenfalls
    rot werden — sonst wäre die Ausnahme so breit wie der Wächter).

Der vierte Fall ist der eigentliche Fund dieser Zeile: `:not([aria-current="true"])` ist
    **keine Zustandsregel** (sonst wäre P9-AN mit P9-AO in Konflikt), wohl aber eine **eigene**
    (sonst umginge sie diesen Wächter). Genau das prüft `_ist_eigene_regel()`.

    **[2026-10-06, P9-BB: vier Fälle dazu, und einer davon ist der wichtigste.]**
    `padding-block` stand bis eben auf **keiner** Liste — weder verboten noch erlaubt, also von
    beiden Seiten unbewacht, und genau dort hat der Bau seine erste eigene Höhe gesetzt. Drei neue
    Verbote (`padding-block` mit anderem Wert, die Langform `padding-block-start`, und die
    logische Längsform `padding-inline-start` als Umweg um `padding-left`) und **eine** neue
    Erlaubnis. Der wichtigste Fall ist der letzte Absatz: der gelockte Wert ist am Menüpunkt
    grün und an der Space-Zeile rot — eine Erlaubnis, die überall gilt, wäre keine Ausnahme."""
    tokens = _tokens()
    erlaubte_color = _farbe_von_btn_primary(_css())
    verstoesse = {
        "eigene Hoehe": "height: 36px;",
        "eigenes Polster oben": "padding-top: 10px;",
        "eigenes Polster rechts": "padding-right: 20px;",
        "Polster-Kurzform": "padding: 10px;",
        "linkes Polster mit eigenem Wert": "padding-left: 24px;",
        "eigene Rundung": "border-radius: 10px;",
        "eigene Textfarbe": "color: var(--text);",
        "Kanten-Kurzform": "border: 1px solid var(--line-strong);",
        "aeusserer Schatten": "box-shadow: 0 1px 0 rgba(0,0,0,.5);",
        "Farbe statt Token": "background: #0C1015;",
        "erfundenes Token": "background: var(--sunken-tiefer);",
        "falscher Text-align": "text-align: middle;",
        # P9-BB: die neue Eigenschaft in drei Formen, in denen sie **nicht** durchlässt.
        "polster-block mit anderem Wert": "padding-block: 10px;",
        "polster-block als Langform": "padding-block-start: 4px;",
        "polster-inline als Umweg um padding-left": "padding-inline-start: 40px;",
        # P9-BF: `margin-left` in drei Formen, in denen es **nicht** durchlässt. Ohne diese drei
        # Zeilen wäre die Erlaubnis ungetestet -- und `margin-left` stand bis eben auf keiner Liste.
        "aussenabstand links mit anderem Wert": "margin-left: 4px;",
        "aussenabstand links positiv": "margin-left: var(--space);",
        "aussenabstand als Langform unten": "margin-bottom: calc(var(--space) * -1);",
    }
    for name, body in verstoesse.items():
        assert _optik_verstoss(body, tokens), f"der Wächter meldet {name!r} ({body}) nicht"
    # Und die dreiköpfige Erlaubnis meldet **nichts**:
    erlaubt = (f"background: var(--btn-std-fill);", "border-color: var(--btn-std-line);",
               "text-align: center;", f"padding-left: {ERLAUBTES_PADDING_LEFT};",
               "box-shadow: inset 0 1px 0 rgba(255,255,255,.06);")
    for body in erlaubt:
        assert not _optik_verstoss(body, tokens), f"{body!r} wird zu Unrecht gemeldet"
    # **P9-BB: der gelockte vertikale Polster ist am Menüpunkt grün …**
    pb = ERLAUBTES_PADDING_BLOCK_PRO_SELECTOR[".settings-menu__item"]
    assert not _optik_verstoss(f"padding-block: {pb};", tokens, erlaubtes_padding_block=pb), (
        f"der gelockte Wert {pb!r} wird am Menuepunkt zu Unrecht gemeldet — P9-BB waere nicht baubar"
    )
    # … und an der **Space-Zeile** rot, denn dort hat die Eigenschaft nichts verloren.
    assert _optik_verstoss(f"padding-block: {pb};", tokens,
                           erlaubtes_padding_block=(
                               ERLAUBTES_PADDING_BLOCK_PRO_SELECTOR[".settings-space-row"])), (
        "dieselbe Deklaration ist an der Space-Zeile erlaubt — die Ausnahme waere so breit wie "
        "der Wächter"
    )
    # **Und P9-BF in derselben Form:** der negative Aussenabstand ist an der Space-Zeile gruen …
    ml = ERLAUBTES_MARGIN_LEFT_PRO_SELECTOR[".settings-space-row"]
    assert not _optik_verstoss(f"margin-left: {ml};", tokens, erlaubtes_margin_left=ml), (
        f"der gelockte Aussenabstand {ml!r} wird an der Space-Zeile zu Unrecht gemeldet — "
        "P9-BF waere nicht baubar"
    )
    # … und am Menuepunkt **rot**, denn dort gibt es keine zweite Kante zu verlegen.
    assert _optik_verstoss(f"margin-left: {ml};", tokens,
                           erlaubtes_margin_left=ERLAUBTES_MARGIN_LEFT_PRO_SELECTOR[
                               ".settings-menu__item"]), (
        "derselbe Aussenabstand ist am Menuepunkt erlaubt — die Ausnahme waere so breit wie der "
        "Wächter"
    )
    # Und die **Auswahlregel** darf die Farbe aus `.btn-primary` tragen — sonst wäre P9-AV nicht
    # baubar, und das wäre eine Regel, die den Bau verhindert statt ihn zu prüfen.
    assert not _optik_verstoss(f"color: {erlaubte_color};", tokens, erlaubte_color), (
        "die Auswahlregel meldet die Farbe aus .btn-primary zu Unrecht"
    )
    # …und **nur** dort. Dieselbe Farbe in einer eigenen Nicht-Auswahlregel muss rot werden.
    assert _optik_verstoss(f"color: {erlaubte_color};", tokens), (
        "eine Nicht-Auswahlregel darf keine eigene Schriftfarbe tragen — die Ausnahme wäre "
        "sonst so breit wie der Wächter"
    )
    # `:not([aria-current="true"])` ist eine **eigene** Regel und **keine** Zustandsregel.
    assert _ist_eigene_regel('.settings-menu__item:not([aria-current="true"])',
                             ".settings-menu__item")
    assert not _ist_eigene_regel('.settings-menu__item[aria-current="true"]',
                                 ".settings-menu__item")
    # Die Sammelregel mit `.tree__folder` bleibt Wiederverwendung, kein eigener Verstoß.
    assert not _ist_eigene_regel(".rail__home", ".settings-menu__item")
    assert not _ist_eigene_regel(".settings-menu__item__klein", ".settings-menu__item")


def test_the_selection_state_uses_aria_current_and_the_accent_surface():
    """P9-AG/P9-AO: der Knopf des offenen Unterfensters trägt `aria-current="true"` — **das
    Zustands-Attribut bleibt unverändert**.

    **[2026-10-05, P9-AV: die Fläche ist bewusst eine andere geworden, und dieser Wächter
    musste umgedreht werden — mit beiden Lesarten im Repo, weil die alte hier nicht falsch war,
    sondern widerrufen.]**

    *Die widerrufene Lesart (P9-AO):* der ausgewählte Menüpunkt trug `--select-fill`, denselben
    Wert wie eine aktive `.tree__folder`-Zeile in der Rail — „kein neuer Füll-Farbwert". Der
    Nikinger hat die Bilder angesehen und entschieden: ausgewählt bekommt die **Akzentfläche**
    eines Hauptknopfes (`--accent-face-*` + `--accent-edge`), damit der offene Zustand sich neben
    den Nachbarpanels wie ein Knopf zeigt und nicht wie eine Baumzeile.

    **Warum das keine dritte Variante ist (der Kern des alten Wächters):** die Fläche wird nicht
    abgetippt, sondern gegen die `.btn-primary`-Regel **verglichen** — dieselbe Technik wie beim
    Standardknopf. Zwei eigene Werte wären die dritte Variante; ein Wert, den die Hauptknopf-Regel
    selbst vorgibt, ist eine Nennung.

    Beide Hälften werden geprüft, weil jede für sich allein nichts bedeutet: `aria-current` ohne
    CSS-Regel ist ein Attribut, eine CSS-Regel ohne Attribut ist toter Ballast. Die Probe misst
    dann die *berechneten* Werte der beiden Zustände (S1)."""
    css = _css()
    assert re.search(r"\.settings-menu__item\[aria-current=\"true\"\]", css), (
        "keine Auswahlregel für die Menüpunkte"
    )
    eigene = _rule_bodies(css, '.settings-menu__item[aria-current="true"]')
    assert eigene, "keine eigene Auswahlregel für die Menüpunkte"
    assert all("var(--accent-face-top)" in body for body in eigene), (
        f"die Auswahl der Menüpunkte nutzt nicht die Akzentfamilie: {eigene}"
    )
    # Und **genau eine** eigene Regel mit der Fläche (die Hover-Regel daneben hat `:hover` im
    # Selektor). Zwei Flächenregeln wären der Beginn der dritten Variante.
    mit_flaeche = [b for b in eigene if re.search(r"(^|[;{\s])background\s*:", b)]
    assert len(mit_flaeche) == 1, f"genau eine Flächenregel erwartet, gefunden {len(mit_flaeche)}"
    # **Die Baumzeile behält `--select-fill`** — sie ist eine Zeile in einem Baum, kein Knopf.
    # Der Wächter prüft das mit, weil die Formulierung „derselbe Auswahlzustand wie die Baumzeile"
    # sonst als Überprüfung beider gelesen würde.
    for body in _rule_bodies(css, '.tree__folder[aria-current="true"]'):
        assert "var(--select-fill)" in body, (
            f"die Baumzeile verliert ihren Auswahl-Fill: {body}"
        )


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


def test_the_unselected_menu_item_takes_the_standard_button_surface():
    """**P9-AV (2026-10-05, Nikinger) — und das ist eine Umkehr, mit Datum.**

    *Die widerrufene Lesart:* P9-AN (gleicher Tag, gleicher Block) verlangte die **Fläche des
    Eingabefeldes** (`--sunken` + `--line-strong`), und dieser Wächter hieß entsprechend
    `…_takes_the_input_surface_verbatim`. Der Nikinger hat die Bilder angesehen und geschrieben:
    *„since they are buttons and not fields to type something in"*. Damit war P9-AN **an der
    falschen Stelle**: die Fläche des Eingabefeldes gehört laut Selection/Choice-Konvention v3 zur
    Kategorie **Choice**, und die Menüpunkte sind **Navigation** (P9-AF, `.tree__folder`).

    *Was jetzt gilt:* unausgewählt exakt die Fläche des **Standardknopfes** (`--btn-std-fill` +
    `--btn-std-line` + derselbe 1-px-Innenschatten), ausgewählt die **Akzentfläche** wie
    `.btn-primary` (`--accent-face-*` + `--accent-edge`).

    **Der Token-Name wird nicht abgetippt, sondern verglichen** — und jetzt gegen die `.btn`-Regel
    statt gegen die `.input`-Regel. Ein abgetipptes `var(--btn-std-fill)` wäre eine zweite Kopie
    der Aussage: änderte die `.btn`-Regel ihren Wert, bliebe der Wächter grün und die Menüpunkte
    hätten eine Fläche, die es im Panel nicht mehr gibt. Dasselbe Muster wie in der Fassung von
    P9-AN, nur mit der anderen Vorlage.

    **Der Schatten wird jetzt verlangt, nicht verboten** (`inset 0 1px 0 rgba(255,255,255,.06)`,
    ebenfalls aus der `.btn`-Regel gelesen): ohne ihn sähe der Menüpunkt flacher aus als
    „Schließen" im Nachbarpanel, und genau dieser Vergleich war der Auftrag. Ein **äußerer**
    Schatten bleibt verboten (`_schatten_verstoss`).

    Die **Geometrie** prüft `test_settings_menu_items_reuse_the_tree_row_look()`, die **Wirkung**
    misst die Browser-Probe."""
    css = _css_code()
    btn_bodies = _bare_rule_bodies(".btn")
    assert btn_bodies, "keine Basis-Regel für .btn"
    # Die **Übergangs-Sammelregel** steht in dieser Liste mit drin (sie nennt `.btn` als ersten
    # Selektor); die gesuchte Regel ist die, die `background` überhaupt nennt.
    btn = _koerper_mit(btn_bodies, "background")
    assert btn, f"keine .btn-Regel mit einer Fläche: {btn_bodies}"
    knopf_flaeche = _eigenschaft(btn, "background")
    knopf_kante = _eigenschaft(btn, "border")
    knopf_schatten = _eigenschaft(btn, "box-shadow")
    assert knopf_flaeche and knopf_kante and knopf_schatten, (
        knopf_flaeche, knopf_kante, knopf_schatten)
    # Die Kante der `.btn` ist die **Kurzform** — der Wert, den die Menüregel als `border-color`
    # übernimmt, ist deren Farbanteil. (`border` selbst bleibt verboten: die Kurzform trägt Breite
    # und Stil und könnte damit genau die Geometrie verändern, die P9-AF bindet.)
    farbanteil = knopf_kante.split()[-1]
    assert farbanteil.startswith("var("), knopf_kante

    # **Ueber den Selektor filtern, nicht ueber den Body.** Fuer den unausgewaehlten Zustand
    # gibt es eine Flaechenregel und eine Hoverregel, und **beide nennen ein `background`** --
    # die erste Fassung dieses Tests hat ueber `_eigenschaft(body, "background")` gefiltert und
    # damit den Hover mitgezaehlt (gemessen 2, erwartet 1, Aussage wertlos). Der Selektor ist
    # das, was Flaeche und Hover unterscheidet.
    eigene = [body for erster, selectors, body in _alle_regeln()
              if erster == '.settings-menu__item:not([aria-current="true"])']
    assert len(eigene) == 1, (
        f"genau eine eigene Flaechenregel fuer die unausgewaehlten Menuepunkte erwartet, "
        f"gefunden {len(eigene)}"
    )
    body = eigene[0]
    # Und der Hover existiert als **eigene** Regel mit der Hover-Flaeche des Standardknopfes --
    # sonst wuerde die Kette beim Ueberfahren in eine andere Optik kippen, die es sonst nirgends
    # gibt. Der Token wird verglichen, nicht die Farbe.
    hover = [b for erster, selectors, b in _alle_regeln()
             if erster == '.settings-menu__item:not([aria-current="true"]):hover']
    assert len(hover) == 1, f"genau eine eigene Hoverregel erwartet, gefunden {len(hover)}"
    btn_hover = [b for erster, selectors, b in _alle_regeln() if erster == ".btn:hover"]
    assert btn_hover, "die .btn-Regel traegt keine eigene :hover-Regel -- der Vergleich hat nichts"
    assert _eigenschaft(hover[0], "background") == _eigenschaft(btn_hover[0], "background"), (
        f"der Hover der Menuepunkte ({_eigenschaft(hover[0], 'background')!r}) weicht vom Hover "
        f"des Standardknopfes ({_eigenschaft(btn_hover[0], 'background')!r}) ab"
    )
    assert _eigenschaft(body, "background") == knopf_flaeche, (
        f"die Flaeche der Menuepunkte ({_eigenschaft(body, 'background')!r}) ist nicht die des "
        f"Standardknopfes ({knopf_flaeche!r})"
    )
    assert _eigenschaft(body, "border-color") == farbanteil, (
        f"die Haarlinie der Menuepunkte ({_eigenschaft(body, 'border-color')!r}) ist nicht die des "
        f"Standardknopfes ({farbanteil!r})"
    )
    assert _eigenschaft(body, "box-shadow") == knopf_schatten, (
        f"der Innenschatten der Menuepunkte ({_eigenschaft(body, 'box-shadow')!r}) weicht von dem "
        f"des Standardknopfes ({knopf_schatten!r}) ab -- ohne ihn waere die Flaeche eine andere"
    )

    # Und P9-AV's zweite Haelfte: die **Auswahl** traegt die Akzentfamilie, nicht den
    # Rail-Auswahl-Fill. Auch hier werden die Namen verglichen, nicht die Werte abgetippt.
    auswahl = [(erster, body) for erster, selectors, body in _alle_regeln()
               if '.settings-menu__item[aria-current="true"]' in selectors]
    assert len(auswahl) == 1, auswahl
    regel = auswahl[0][1]
    haupt = _koerper_mit(_bare_rule_bodies(".btn-primary"), "background")
    assert haupt, "keine .btn-primary-Regel mit einer Akzentflaeche"
    assert _eigenschaft(regel, "background") == _eigenschaft(haupt, "background"), (
        f"die Auswahlflaeche ({_eigenschaft(regel, 'background')!r}) ist nicht die Akzentflaeche "
        "von .btn-primary"
    )
    # Die Haarlinie des Hauptknopfes ist die **Kurzform** -- der Vergleichswerte ist ihr
    # Farbanteil, genau wie bei `.btn` oben.
    assert _eigenschaft(regel, "border-color") == _eigenschaft(haupt, "border").split()[-1], (
        "die Kante der Auswahl weicht vom Farbanteil der Kante des Hauptknopfes ab"
    )
    # Der **Zustand** bleibt `aria-current` (P9-AG/P9-AO unberührt) — nur die Fläche ist eine
    # andere als die der Baumzeile. Die Auswahlregel darf deshalb NICHT mehr mit der Baumzeile
    # übereinstimmen: die Formulierung „derselbe Auswahlzustand wie die Baumzeile" aus P9-AO ist
    # mit P9-AV **an der Fläche** widerrufen, am Zustand nicht.
    assert regel != _rule_bodies(css, '.tree__folder[aria-current="true"]')[0], (
        "die Auswahlregel der Menuepunkte ist wieder wortgleich die der Baumzeile -- das waere "
        "eine stille Rueckkehr zu P9-AO und widerspraeche P9-AV"
    )
    assert ":not" not in auswahl[0][0], auswahl[0][0]


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


def test_the_menu_points_have_the_gap_the_space_rows_have():
    """P9-AU (2026-10-05, Nikinger: *„the buttons shouldn't be glued to each other"*) — und
    gemessen war **0 px**.

    **Der Abstand wird nicht abgetippt, sondern verglichen**, und zwar gegen
    `#space-admin-list`: das ist die **zweite** Liste derselben Kette, und beide tragen seit
    P9-AK denselben Wunsch („Zeilen mit sichtbarem Abstand"). Zwei notierte Werte wären zwei
    Stellen, an denen derselbe Abstand auseinanderlaufen darf — dieselbe Begründung wie bei
    P9-AMs `--settings-title-gap`.

    **Und der Abstand hängt an einem Wrapper, nicht an jedem Knopf.** Die Alternative wäre
    `margin-bottom` an jedem der drei Punkte außer dem letzten: eine Sonderbehandlung für den
    letzten Knopf, also eine zweite Wahrheit über dieselbe Sache. Der Wächter prüft deshalb
    beides — den Wrapper im Markup **und** dass kein Knopf einen eigenen unteren Außenabstand
    trägt.
    """
    html = _html()
    css = _css()
    # Der Wrapper existiert und traegt die drei Punkte.
    assert 'class="settings-menu__list"' in html, "der Wrapper .settings-menu__list fehlt im Markup"
    liste = _element_by_class(html, "settings-menu__list")
    assert liste.count("settings-menu__item") == 3, liste
    assert "<h2>" not in liste, "der Titel gehoert nicht in den Wrapper (er traegt seinen eigenen Abstand)"
    # Er traegt den Abstand — und derselbe wie die Space-Liste darunter.
    wrapper = _koerper_mit(_rule_bodies(css, ".settings-menu__list", own_only=True), "gap")
    assert wrapper, "keine eigene Regel fuer .settings-menu__list"
    assert _eigenschaft(wrapper, "display") == "flex", wrapper
    assert _eigenschaft(wrapper, "flex-direction") == "column", wrapper
    space_liste = [b for erster, selectors, b in _alle_regeln()
                   if erster == "#space-admin-list"]
    assert space_liste, "die Regel fuer #space-admin-list fehlt — der Vergleich hat nichts"
    assert _eigenschaft(wrapper, "gap") == _eigenschaft(space_liste[0], "gap"), (
        f"der Abstand der Menuepunkte ({_eigenschaft(wrapper, 'gap')!r}) weicht vom Abstand der "
        f"Space-Zeilen ({_eigenschaft(space_liste[0], 'gap')!r}) ab"
    )
    # Kein Knopf traegt einen eigenen unteren Aussenabstand — das waere der zweite Ort.
    assert "margin-bottom" not in liste, liste
    # **[2026-10-06, P9-BF]** Die Pruefung ist **namensgenau** geworden. Vorher stand hier
    # `assert "margin" not in body` — und die Space-Zeile traegt seit P9-BF einen **negativen**
    # `margin-left`, mit dem das Kaestchen 8 px nach links wandert, ohne dass die Beschriftung
    # wandert. Ein Substring-Test haette den Lock verboten statt zu pruefen: er kannte nur
    # "irgendwo ein margin", nicht **welches** und nicht **mit welchem Wert**.
    for selektor in (".settings-menu__item", ".settings-space-row"):
        for body in _rule_bodies(css, selektor, own_only=True):
            for prop in ("margin", "margin-top", "margin-right", "margin-bottom"):
                assert not re.search(rf"(^|[;{{\s]){prop}\s*:", body), (selektor, prop, body)
            if "margin-left" in body:
                assert _eigenschaft(body, "margin-left") == (
                    ERLAUBTES_MARGIN_LEFT_PRO_SELECTOR[selektor]), (selektor, body)


def test_the_password_buttons_are_caution_and_close():
    """P9-AW (2026-10-05, Nikinger, wörtlich): *„copying the 'archivieren' Buttons style (so
    'Ändern' Becomes red) … a password change is [irreversible]"* und *„change 'abbrechen' to
    'schließen' since all other menus use 'schließen'"*.

    **Zwei Wörter, zwei Begründungen.** „Ändern" war `.btn-primary` — die *Hauptaktion* — und die
    Hauptaussage eines roten Knopfes in diesem Repo ist *nicht rückgängig zu machen*; der
    Passwortwechsel erzwingt für jeden Connector eine neue Autorisierung und meldet alle anderen
    Browser ab (der Panel-Hinweistext sagt genau das). Und „Abbrechen" beschrieb eine Absicht,
    die es hier nicht gibt: es gibt nur das Fenster, das man schließt — alle anderen Knöpfe der
    Kette heißen „Schließen".

    **Die Fläche wird nicht abgetippt, sondern verglichen** — gegen `.btn`, denn genau das ist
    die Kategorie „Vorsicht": Standard-Knopfplastik mit roter Beschriftung und **ohne** gefüllte
    rote Fläche (Selection/Choice-Konvention v3). Der Knopf trägt die Klasse selbst; wir prüfen
    das **Markup**, weil eine Prüfung des CSS-Texts grün bliebe, wenn die Klasse aus dem HTML
    verschwände.
    """
    html = _html()
    css = _css()
    knopf = _element_by_id(html, "account-submit")
    assert "action--caution" in knopf, knopf
    assert re.search(r'class="[^"]*\bbtn\b', knopf), knopf
    assert "btn-primary" not in knopf, (
        f"#account-submit traegt wieder die Hauptaktionsflaeche (widerrufene Lesart vor P9-AW): {knopf}"
    )
    # Keine eigene Regel fuer den Knopf: die Flaeche erbt er von `.btn`, die Farbe von
    # `.action--caution`. Eine eigene Regel waere eine dritte Variante.
    assert not re.search(r"#account-submit", css), (
        "app.css hat eine eigene Regel fuer #account-submit — die Vorsicht erbt ihre Flaeche"
    )
    assert "var(--caution)" in _rule_bodies(css, ".action--caution")[0]
    # Und das Wort.
    knopf_text = _element_by_id(html, "account-cancel")
    # `_element_by_id` loest die Entities auf (`&szlig;` -> `\u00df`), deshalb wird die
    # **aufgeloeste** Form geprueft — die geschriebene Form zu vergleichen hiesse, den Test beim
    # ersten Umlaut-Umstieg rot werden zu lassen, ohne dass sich etwas geaendert haette.
    assert "Schlie\u00dfen" in knopf_text, knopf_text
    # **HTML-Kommentare vor der Wortsuche entfernen.** Sonst ist der *Kommentar*, der die
    # Umbenennung erklaert, der Befund — genau die Umkehrung, die in diesem Block schon einmal
    # eine Zaehlung verschoben hat (die `action--caution`-Zaehlung in `test_static_routes.py`).
    ohne_kommentare = re.sub(r"<!--.*?-->", "", html, flags=re.DOTALL)
    assert "Abbrechen" not in _element_by_id(ohne_kommentare, "settings-password"), (
        "im Passwort-Panel steht noch 'Abbrechen'"
    )
    # Und die anderen Fenster der Kette tragen dasselbe Wort — sonst waere die
    # Vereinheitlichung an zwei von vier Stellen. **Ueber die Knopf-IDs, nicht ueber das
    # Panel:** `_element_by_id` schneidet beim ersten `</div>` ab (siehe dessen Docstring), und
    # die Panels enthalten verschachtelte `div`s — die erste Fassung dieses Tests hat genau
    # daran gescheitert und „traegt kein Schlie&szlig;en" gemeldet, drei Zeichen vor dem Wort.
    for knopf_id in ("space-admin-close", "space-detail-close", "update-log-close"):
        assert "Schlie\u00dfen" in _element_by_id(html, knopf_id), knopf_id


def test_the_two_input_rows_stop_being_staircases():
    """P9-AX + P9-AY + P9-AZ (2026-10-05) — **drei Versätze, zwei Regeln**.

    Der gemessene Befund, alle drei aus derselben Messung: die Beschriftung der Space-Zeilen stand
    **33 px** rechts vom Panel-Titel (32 px geerbtes Einzugs-Polster der Baumzeile + 1 px Rahmen),
    das Namensfeld im Detail-Panel war **12 px** schmaler als die Zeile darunter, und die Anlege-Zeile
    im Spaces-Panel war **80 px** versetzt.

    **P9-AY wird nicht als Zahl geprüft, sondern als Folge.** Der Test verlangt das Raster und
    die Spaltenüberspannung — nicht `width: 234px`. Eine getippte Breite wäre zwei Kopien
    (der Knopfbreiten), die bei jeder Beschriftungsänderung still auseinanderlaufen; das Raster
    misst die Knöpfe selbst.

    **P9-AZ ist der Fall, in dem dieselbe Technik nicht greift** — dort ist die Folgezeile *ein*
    Knopf (142 px), und das Feld daran zu binden hieße, ein Eingabefeld auf 142 px zu verengen.
    Der Test verlangt deshalb `flex: 1` **und** `nowrap`: ohne das zweite Umbricht das Feld wieder
    auf seine eigene Zeile, und die Wirkung wäre die vorherige.
    """
    css = _css()
    # P9-AY: Raster mit zwei `max-content`-Spalten, Feld ueberspannt, Zeile rechtsbuendig.
    raster = [body for erster, selectors, body in _alle_regeln()
              if "#space-member-name-input" in erster and ":has(" in erster]
    assert len(raster) == 1, f"genau eine Rasterregel fuer die Member-Aktionszeile erwartet: {len(raster)}"
    regel = raster[0]
    assert _eigenschaft(regel, "display") == "grid", regel
    assert _eigenschaft(regel, "grid-template-columns") == "repeat(2, max-content)", regel
    assert _eigenschaft(regel, "justify-content") == "end", regel
    # Das Feld ueberspannt beide Spalten **und** streckt sich: `grid-column` allein laesst es
    # defaultmaessig start-ausgerichtet, also auf seine Inhaltsbreite schrumpfen.
    feld_regeln = [b for erster, selectors, b in _alle_regeln()
                   if erster == "#space-member-name-input"]
    assert len(feld_regeln) == 1, f"genau eine eigene Regel fuer das Member-Namensfeld: {len(feld_regeln)}"
    assert _eigenschaft(feld_regeln[0], "grid-column") == "1 / -1", feld_regeln[0]
    assert _eigenschaft(feld_regeln[0], "justify-self") == "stretch", feld_regeln[0]
    # **Und keine Breite notiert** — das ist der Punkt der ganzen Regel.
    for eigenschaft in ("width", "flex-basis", "flex"):
        assert _eigenschaft(feld_regeln[0], eigenschaft) is None, (
            f"das Member-Namensfeld traegt eine eigene {eigenschaft} — die Breite soll aus den "
            "Knopfbreiten folgen, nicht aus einer Zahl im Stylesheet"
        )
    # P9-AZ: eine Zeile, Feld fuellt den Rest.
    anlegen = [body for erster, selectors, body in _alle_regeln()
               if "#space-create-name-input" in erster and ":has(" not in erster]
    assert len(anlegen) == 1, f"genau eine eigene Regel fuer das Anlege-Feld erwartet: {len(anlegen)}"
    assert _eigenschaft(anlegen[0], "flex") == "1", anlegen[0]
    assert _eigenschaft(anlegen[0], "min-width") == "0", anlegen[0]
    nowrap = [b for erster, selectors, b in _alle_regeln()
              if erster == "#settings-spaces .overlay__actions"]
    assert len(nowrap) == 1, f"die Zeile der Anlege-Aktionen braucht ihre eigene nowrap-Regel: {len(nowrap)}"
    assert _eigenschaft(nowrap[0], "flex-wrap") == "nowrap", nowrap[0]
    # P9-AX: die Space-Zeilen bündig mit dem Panel-Titel. **Kein Icon**, deshalb ist die
    # Einrueckung leerer Raum — das prueft der Test am Markup mit.
    html = _html()
    assert not re.search(r'class="[^"]*settings-space-row[^"]*"[^>]*>\s*<', html), (
        "die Space-Zeile hat jetzt ein erstes Kind-Element — die Annahme 'kein Icon' von P9-AX "
        "waere damit falsch und der Padding-Wert neu zu messen"
    )
    zeilen = [b for erster, selectors, b in _alle_regeln()
              if erster == ".settings-panel .settings-space-row"]
    assert len(zeilen) == 1, f"genau eine eigene Regel fuer die Space-Zilen im Panel: {len(zeilen)}"
    # **[2026-10-06, P9-BF — die Umkehr, mit beiden Lesarten im Repo.]** Bis eben stand hier
    # `padding-left == "0"`, und das war **P9-AX**: die Beschriftung gehört auf dieselbe Kante wie
    # der Panel-Titel. Der Nikinger hat am Bild 08 darum gebeten, das **Kaestchen** ein paar Pixel
    # nach links zu erweitern, damit der Text **innen** wieder den Standardabstand haelt — gemessen
    # waren vorher innen **1 px links** gegen **9 px rechts**. Beide Locks zugleich haelt nur
    # **Polster und negativer Aussenabstand in derselben Hoehe**: `0` allein liess die Beschriftung
    # am Kasten kleben, `var(--space)` allein schob sie 8 px nach rechts und brach P9-AX.
    assert _eigenschaft(zeilen[0], "padding-left") == ERLAUBTES_PADDING_LEFT_PRO_SELECTOR[
        ".settings-space-row"], zeilen[0]
    assert _eigenschaft(zeilen[0], "margin-left") == ERLAUBTES_MARGIN_LEFT_PRO_SELECTOR[
        ".settings-space-row"], (
        "ohne den negativen Aussenabstand wandert die Beschriftung mit dem Polster nach rechts "
        "und P9-AX ist gebrochen: " + str(zeilen[0])
    )
    # Und die Mitgliederliste: Browser-Standard waere Aufzaehlungspunkt und 40 px Einzug.
    mitglieder = [b for erster, selectors, b in _alle_regeln()
                  if erster == "#space-member-list"]
    assert len(mitglieder) == 1, f"genau eine Regel fuer #space-member-list erwartet: {len(mitglieder)}"
    assert _eigenschaft(mitglieder[0], "list-style") == "none", mitglieder[0]
    assert _eigenschaft(mitglieder[0], "padding") == "0", mitglieder[0]
    # `margin: 0` ist Teil desselben Satzes: der Titelabstand (24 px, P9-AM) muss der einzige
    # bestimmende Wert bleiben, sonst haengt P9-96/P9-101 an einem Browser-Standard.
    assert _eigenschaft(mitglieder[0], "margin") == "0", mitglieder[0]
    # P9-BM (B4, 2026-10-08): der Standardabstand zwischen den Zeilen sitzt am Wrapper. Ein
    # `margin` an den Zeilen waere die zweite Quelle desselben Abstands (P9-AU-Muster).
    assert _eigenschaft(mitglieder[0], "display") == "flex", mitglieder[0]
    assert _eigenschaft(mitglieder[0], "flex-direction") == "column", mitglieder[0]
    assert _eigenschaft(mitglieder[0], "gap") == "var(--space)", mitglieder[0]


# --- Block „Kästchen enger" (Plan §12.1, Locks P9-BB/BC/BD/BE, Abnahme P9-116 – P9-119) ---------

def test_the_menu_points_are_flatter_and_keep_their_width():
    """P9-BB (2026-10-06, Nikinger zu Bild 01: *„the update-log button is still bigger, I think
    you need to decrease its height"*, Antwort **(b)**: *zusätzlich flacher*).

    **Gemessen vorher:** alle drei Punkte **35,69 px** hoch (Polster 6 px oben/unten aus der
    Sammelregel, Zeilenkasten 21,69 px, 2 px Rahmen) — an einem Bild, in dem **nichts**
    ausgewählt war, und also **ohne** einen Zustand, der die Höhe erklärt. **Gemessen nachher:**
    **31,69 px**. Die Breite ist **nicht** Teil dieses Locks: das „kästchen enger" aus Bild 08 hat
    der Nikinger ausdrücklich **nur für „Spaces verwalten"** verlangt (P9-BA damit **widerrufen**,
    siehe `test_only_the_spaces_panel_is_narrower()`), also behalten die Menüpunkte ihre
    `width: 100%` und ihre mittige Beschriftung (P9-AP, P9-99).

    Der Wächter prüft **beide** Richtungen: die Höhe ist kleiner (P9-BB), **und** Breite,
    Zentrierung und linkes Polster sind unangetastet (P9-AV/P9-AP/P9-AX). „Der Menüpunkt ist
    schmaler geworden" wäre eine stille Verletzung von P9-AF, und „er ist flacher" eine stille
    Verletzung von P9-AP — beide Richtungen stehen deshalb hier."""
    css = _css()
    basis = _bare_rule_bodies(".settings-menu__item")
    assert len(basis) == 1, f"genau eine nackte Regel fuer .settings-menu__item erwartet: {len(basis)}"
    assert _eigenschaft(basis[0], "width") == "100%", (
        f"die Menuepunkte sind nicht mehr auf Panelbreite gestreckt — P9-BA wurde am 2026-10-06 "
        f"auf 'nur bei Spaces verwalten' eingeschraenkt, die Breite gehoert unveraendert: {basis[0]}"
    )
    menue = [b for erster, selectors, b in _alle_regeln()
             if erster == ".settings-panel--menu .settings-menu__item"]
    assert len(menue) == 1, f"genau eine Regel fuer den Menuepunkt im Menuepanel: {len(menue)}"
    regel = menue[0]
    assert _eigenschaft(regel, "padding-block") == ERLAUBTES_PADDING_BLOCK_PRO_SELECTOR[
        ".settings-menu__item"], regel
    # Und die beiden Nachbarn desselben Locks unveraendert:
    assert _eigenschaft(regel, "justify-content") == "center", regel
    assert _eigenschaft(regel, "padding-left") == "var(--space)", regel


def test_the_space_rows_hug_their_own_label():
    """P9-BC (2026-10-06, Nikinger zu Bild 08: *„move the button borders a little bit further to
    the left, leave the text where it is now. Cut the not used space from the right"*).

    **Gemessen vorher:** Kästchen **330 px**, Beschriftungen **84–137 px** ⇒ **192–245 px**
    Leerraum rechts, bei bereits bündigem Text (P9-AX ✅, 1 px). Gebaut wird genau der
    Leerraum, nicht der Text: die Zeile umklammert ihr **eigenes** Label.

    # **Der Wert steht an der Liste, nicht an der Zeile** — `align-items: flex-start` auf
    # `#space-admin-list`. Die Alternative (`width: fit-content` an jeder Zeile) wäre derselbe Wert
    # an N Orten; und die Zeile muss trotzdem `width: auto` tragen, denn die **Sammelregel** oben
    # (`.rail__home, …, .settings-space-row, …`) setzt `width: 100%` — das war der Fund des
    # ersten Gegenlaufs dieses Blocks: die eigene Regel war weg, die Streckung nicht. Genau diese
    # beiden Richtungen prüft der Wächter (Liste richtet links aus, Zeile hat **keine** 100 %).
    # `max-width: 100%` ist die einzige Bremse (ein langer Name, P9-U legt die Länge nicht fest,
    # darf das Panel nicht aufweiten) — und sie wird mitgeprüft, weil ein Wächter, der sie nicht
    # kennt, sie beim nächsten Umbau verliert."""
    css = _css()
    listen = [b for erster, selectors, b in _alle_regeln() if erster == "#space-admin-list"]
    assert len(listen) == 1, f"genau eine Regel fuer #space-admin-list erwartet: {len(listen)}"
    assert _eigenschaft(listen[0], "align-items") == "flex-start", (
        f"die Space-Zeilen stehen wieder auf der vollen Panelbreite — P9-BC waere nicht gebaut: "
        f"{listen[0]}"
    )
    zeilen = [b for erster, selectors, b in _alle_regeln()
              if erster == ".settings-space-row"]
    assert len(zeilen) == 1, f"genau eine eigene Regel fuer die Space-Zeile erwartet: {len(zeilen)}"
    assert _eigenschaft(zeilen[0], "width") == "auto", (
        f"die Space-Zeile traegt keine eigene Breite — die Sammelregel setzt `width: 100%`, und "
        f"genau das war der Fund vom 2026-10-06 (28 Kästchen auf 238 px = Panelbreite): {zeilen[0]}"
    )
    assert _eigenschaft(zeilen[0], "max-width") == "100%", zeilen[0]
    # Und der Abstand von P9-AK/P9-AU steht weiter an derselben Regel:
    assert _eigenschaft(listen[0], "gap") == "var(--space)", listen[0]


def test_only_the_spaces_panel_is_narrower():
    """P9-BE (2026-10-06, Nikinger zu Bild 08, wörtlich: *„nur bei Spaces verwalten, dort die
    Buttons der einzelnen Spaces nach Links, und das Fenster rechts verkleinern, aber nur
    dieses"*).

    „**Nur dieses**" ist der Auftrag, nicht die Ausnahme — deshalb prüft der Wächter **beide**
    Richtungen: die Klasse hängt genau **einem** Panel, und es ist genau das Spaces-Panel; die
    Basisbreite der anderen Panels bleibt die von `.settings-panel`.

    **Die Breite wird nicht abgetippt, sondern verglichen:** sie muss **kleiner** sein als das
    `max-width` der Basisregel (gemessen vorher 380 px — das Panel stand an seinem Deckel, Inhalt
    330 px). Verglichen wird gegen das **`max-width`**, nicht gegen das `min-width` (340 px): ein
    Vergleich gegen 340 wäre mit 338 px grün und damit **auf der falschen Seite** — genau dieser
    Fehler stand in der ersten Fassung dieses Tests und in der ersten Fassung der CSS-Regel, weil
    `min-width` bei `box-sizing: border-box` die Breite **des Rahmens** ist. Die Browser-Probe
    (S5/P9-118) misst den **Inhalt** und vergleicht ihn am geklonten Schatten.
    Eine Zahl im Test wäre die zweite Kopie — die Zahl steht in `app.css` neben ihrer Herleitung
    (Feld + Abstand + Knopf), und die Herleitung ändert sich mit den Beschriftungen.

    **Und der Schmal-Modus (≤1024 px) muss die feste Breite zurücknehmen**, sonst gewinnt die
    Klassenregel gegen `.settings-panel { flex: 1 }` und das Panel streckt sich nicht mehr. Das
    ist die zweite Hälfte desselben Locks und der Fall, den die erste Fassung der Regel
    gebrochen hätte."""
    html = _html()
    css = _css()
    traeger = [re.search(r'\bid="([^"]+)"', tag).group(1) for tag in re.findall(
        r'<div\b(?=[^>]*\bid="settings-[a-z-]+")(?=[^>]*\bsettings-panel--list\b)[^>]*>', html)]
    assert traeger == ["settings-spaces"], (
        f"die feste Panelbreite traegt nicht (nur) #settings-spaces: {traeger}"
    )
    basis = [b for erster, selectors, b in _alle_regeln() if erster == ".settings-panel"]
    # **Zwei** Regeln mit diesem Selektor gibt es: die Basis und die des Schmal-Modus (≤1024 px),
    # und `_alle_regeln()` unterscheidet sie nicht — es ist eine flache Liste. Unterscheiden
    # **hier** tut man sie an `flex`: das setzt nur die Media-Query-Regel („Panel flext im
    # Schmal-Modus"). Die Basis ist damit die ohne, und die ist die, gegen die verglichen wird.
    basis = [b for b in basis if not _eigenschaft(b, "flex")]
    assert len(basis) == 1, f"genau eine Basisregel fuer .settings-panel erwartet: {len(basis)}"
    eigen = [b for erster, selectors, b in _alle_regeln()
             if erster == ".settings-panel--list"]
    # Auch hier zwei: die feste Breite und ihre Ruecknahme im Schmal-Modus.
    assert len(eigen) == 2, (
        f"genau zwei Regeln fuer .settings-panel--list erwartet (Breite + Ruecknahme im "
        f"Schmal-Modus): {len(eigen)}"
    )
    fest, ruecknahme = eigen[0], eigen[1]
    schmal, breit = (_eigenschaft(fest, "min-width"), _eigenschaft(fest, "max-width"))
    assert schmal and schmal == breit, (
        f"die Breite steht an zwei Werten ({schmal!r} / {breit!r}) — sie ist eine Entscheidung "
        f"und gehoert an eine Stelle: {fest}"
    )
    basis_max = _eigenschaft(basis[0], "max-width")
    assert float(schmal.removesuffix("px")) < float(basis_max.removesuffix("px")), (
        f"das Spaces-Fenster erreicht mit {schmal} noch die alte Deckelbreite ({basis_max}) — "
        "P9-BE waere nicht gebaut"
    )
    # **Und im Schmal-Modus ist die feste Breite wieder weg.** Die Media-Query liegt am Ende der
    # Datei und gewinnt bei gleicher Spezifitaet — ohne diese Regel waere das Panel dort starr.
    medien = re.search(r"@media \(max-width: 1024px\) \{(.*?)\n\}", _css(), flags=re.DOTALL)
    assert medien, "die 1024-px-Media-Query fehlt — der Test prueft ins Leere"
    assert _eigenschaft(ruecknahme, "min-width") == "0", ruecknahme
    assert _eigenschaft(ruecknahme, "max-width") == "none", ruecknahme


def test_the_two_sight_check_criteria_name_the_position_and_the_panel():
    """P9-BD (2026-10-06, Abnahme **P9-119**): **das Checkkriterium ist Teil des Belegs.**

    Der Befund vom 2026-10-06 war kein Defekt, sondern ein Kriteriumfehler: Bild 04 zeigte die
    Hinzufügen-Optionen (am eingecheckten PNG nachgewiesen, y 207..231), und der Nikinger
    fragte *„where did the space hinzufügen options go?"*, weil das Kriterium ihm **nicht sagte,
    wo im Bild er nachsehen soll**. Ein Bild ohne Ort ist für eine Sichtprüfung wertlos — das ist
    keine Formulierungsfrage, sondern dieselbe Fehlerklasse wie ein Wächter, der etwas anderes
    prüft als er behauptet.

    Bild 07 ist derselbe Fall von der anderen Seite: *„I honestly don't see that"* — die Zeile war
    da, aber **unterhalb des Sichtbereichs**, weil das Panel scrollt. Der Wächter verlangt
    darum, dass das Kriterium **das Panel** benennt und das **Aufrollen** sagt; dafür steht genau
    ein Wort als Anker: `scrollIntoView`.

    **Warum der Anker ein Wort und nicht eine Absicht:** die erste Fassung dieses Wächters suchte
    nur nach `Liste` und `Scroll` — und wurde **an der alten, falschen Zeile grün**, weil dort
    zufällig „nicht die **Liste**" und „unterhalb des **Sichtbereichs**" stand. Ein Wächter, der
    an der Formulierung *des Befunds* grün wird, prüft nicht den Auftrag. Der Anker steht
    deshalb im **Kriterium** (was der Nikinger tun soll), nicht im Urteil (was er sagte).

    **Der Wächter pinnt sonst keine Wortwahl.** Wird das Kriterium umgeschrieben und `scrollIntoView`
    fehlt, sagt die Fehlermeldung genau, was hineingehört."""
    readme = (Path(__file__).resolve().parents[2] / "screenshots_latest" / "README.md").read_text(
        "utf-8")
    # **Es gibt zwei Tabellen** mit derselben Bild-Nummer: die **Checkkriterien** (was der
    # Nikinger tun soll) und den **Stand der Sichtprüfung** (was er gesagt hat). Geprüft wird die
    # **erste** — das ist die, die vor dem Blick auf das Bild gelesen wird. (Die erste Fassung
    # nahm die letzte und war damit an der Urteilszeile hängen geblieben.)
    reihen: dict[str, list[str]] = {}
    for m in re.finditer(r"(?m)^\| `(\d\d_[^`]+)`.*$", readme):
        reihen.setdefault(m.group(1), []).append(m.group(0))
    for nummer in ("04_", "07_"):
        assert [k for k in reihen if k.startswith(nummer)], (
            f"im README steht keine Tabellenzeile fuer {nummer}: {sorted(reihen)}"
        )
    kriterium_04 = reihen[next(k for k in reihen if k.startswith("04_"))][0]
    assert re.search(r"\by\s*[^0-9]{0,3}\d{3}", kriterium_04), (
        "das Kriterium zu Bild 04 nennt keine Pixelposition — der Nikinger hat genau danach "
        f"gesucht und es nicht gefunden: {kriterium_04}"
    )
    kriterium_07 = reihen[next(k for k in reihen if k.startswith("07_"))][0]
    assert "scrollIntoView" in kriterium_07, (
        "das Kriterium zu Bild 07 sagt nicht, dass die neue Zeile vor dem Screenshot mit "
        f"`scrollIntoView` aufgerollt wird — genau daran ist sie im Bild vom 2026-10-06 "
        f"unsichtbar geblieben: {kriterium_07}"
    )
    assert re.search(r"Liste|#space-admin-list", kriterium_07), (
        f"das Kriterium zu Bild 07 nennt das Panel nicht, in dem die Zeile steht (die "
        f"Space-Liste, nicht das Detail-Panel): {kriterium_07}"
    )


def test_the_space_rows_keep_the_standard_gap_inside_on_both_sides():
    """P9-BF (2026-10-06, Nikinger zu Bild 08: *„den Auswahl buttons der einzelnen Spaces bitte ein
    paar Px nach links erweitern, sodass innerliegender Text und Button Grenze den Standard Abstand
    einhalten"*).

    **Gemessen vorher:** innen **1 px** links (nur der Rahmen) gegen **9 px** rechts (8 px Polster
    + 1 px Rahmen) — die Beschriftung klebte an der linken Kästchenkante. **Gebaut:** Polster
    `var(--space)` **plus** ein negativer `margin-left` in derselben Höhe, damit das **Kästchen**
    wandert und die **Beschriftung** nicht.

    **Der Wächter prüft die Kopplung, nicht die beiden Werte einzeln.** Zwei Zahlen, die nicht
    miteinander verrechnet werden, sind zwei unabhängige Locks — und die Kombination ist der ganze
    Punkt: `padding-left: 0` allein klebt (sein Befund), `padding-left: var(--space)` allein schiebt
    die Beschriftung **8 px nach rechts** und bricht **P9-AX** (die Beschriftung gehört auf dieselbe
    Kante wie der Panel-Titel). Also: **beide Werte müssen aus derselben Quelle kommen**, und das
    ist an den beiden Werten des Selektor-Index geprüft — nicht an einer Zahl im Test.
    """
    css = _css()
    zeilen = [b for erster, selectors, b in _alle_regeln()
              if erster == ".settings-panel .settings-space-row"]
    assert len(zeilen) == 1, f"genau eine eigene Regel fuer die Space-Zilen im Panel: {len(zeilen)}"
    regel = zeilen[0]
    # **Die Kopplung: der Aussenabstand ist genau die Negation des Polsters**, als Ausdruck und
    # nicht als Zahl. Sonst wuerde ein spaeterer Umbau `margin-left: -4px` neben einem 8-px-Polster
    # durchgehen und die Beschriftung 4 px nach rechts schieben.
    polster = _eigenschaft(regel, "padding-left")
    aussen = _eigenschaft(regel, "margin-left")
    assert aussen == f"calc({polster} * -1)", (
        f"der Aussenabstand {aussen!r} ist nicht die Negation des Polsters {polster!r} — das "
        "Kaestchen wandert dann nicht um genau die Strecke, die das Polster oeffnet"
    )
    # Und die **beiden** Werte stehen an **einer** Stelle, nicht auf zwei Regeln verteilt.
    # (`any(... in s for s in selectors)`, nicht `in selectors` — die Selektorliste ist eine Liste
    # von Strings, und `in` auf einer Liste prüft Gleichheit, nicht Teilstring. Die erste Fassung
    # stand auf `in selectors` und zählte deshalb **null**.)
    assert len([b for erster, selectors, b in _alle_regeln()
                if any(".settings-space-row" in s for s in selectors) and "padding-left" in b]) == 1, (
        "die Space-Zile traegt ihr linkes Polster an mehreren Stellen — eine Kante, eine Quelle"
    )
    # **P9-AX gilt weiter**: die Beschriftung bleibt buntig mit dem Titel. Das ist der zweite Teil
    # des Locks und der Grund fuer den negativen Aussenabstand; die Wirkung misst die Browser-Probe
    # (S5/P9-120), weil sie im Test nicht existiert.
    assert polster == ERLAUBTES_PADDING_LEFT_PRO_SELECTOR[".settings-space-row"]
