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


def _rule_bodies(css: str, selector: str, own_only: bool = False) -> list[str]:
    """Die Bodies aller CSS-Regeln, deren Selektorliste `selector` enthaelt.

    **Der Fallstrick, der hier zwei Fassungen braucht:** die gemeinsame Regel
    `.rail__home, …, .tree__folder, …, .settings-menu__item, .settings-space-row { … }`
    enthaelt die Klasse ebenfalls — und traegt genau die Werte der **Baumzeile**, die der
    Knopf uebernehmen soll. Mit `own_only=True` kommen nur die Regeln heraus, in denen die
    Klasse **an erster Stelle** der Selektorliste steht; das sind die Regeln, die der Klasse
    etwas eigenes geben. Genau die duerfen keine Optik tragen (P9-AF), und genau an diesem
    Unterschied haengt der Test — ein Wächter, der die Sammelregel mitzaehlt, wuerde jede
    korrekte Wiederverwendung als Verfehlung melden.
    """
    css = _css_code()
    bodies: list[str] = []
    for match in re.finditer(r"(?m)^([^{}]+?)\{([^{}]*)\}", css):
        selectors = [part.strip() for part in match.group(1).split(",")]
        if own_only:
            if selectors and selectors[0] == selector:
                bodies.append(match.group(2))
            continue
        if selector in selectors:
            bodies.append(match.group(2))
    return bodies


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
    (b) für `.settings-menu__item` ist **kein** optischer Wert notiert. Damit kann die
    Menüzeile nicht von der Baumzeile abweichen, ohne dass ein Test rot wird — was ein
    Wächter auf *gemessene* Optik in diesem Kontext nicht könnte (im Test gibt es kein
    Layout; die Messung macht die Browser-Probe, S1).

    Punkt (b) ist genau die Lehre vom 2026-10-01: `.account-nav` trug eine eigene Kopie der
    Knopfoptik, dadurch entstand eine dritte Variante, und der erste Korrekturversuch (auf
    `.btn` umstellen) löste das Problem nur durch eine weitere Kopie. Wiederverwendung ist
    die einzige Form, die sich nicht auflösen lässt."""
    html = _html()
    css = _css()
    for element_id, _ in MENU_ITEMS:
        block = _element_by_id(html, element_id)
        assert "tree__folder" in block, f"{element_id} traegt nicht .tree__folder: {block}"
        assert "settings-menu__item" in block, element_id
    # Kein eigener optischer Wert fuer die Menuepunkte — weder Hoehe noch Polster noch
    # Rundung, Schrift, Hintergrund, Kante oder Farbe. Nur *eigene* Regeln zaehlen; die
    # Sammelregel mit `.tree__folder` ist die Wiederverwendung, nicht der Verstoß.
    for selector in (".settings-menu__item", ".settings-space-row"):
        rules = _rule_bodies(css, selector, own_only=True)
        assert rules, f"{selector} hat keine eigene Regel im Stylesheet"
        for body in rules:
            for prop in ("height", "padding", "border-radius", "font", "background", "border",
                         "color", "box-shadow"):
                assert not re.search(rf"(^|[;\s]){prop}\s*:", body), (selector, prop, body)


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
        back = re.search(r'<button[^>]*class="btn settings-back"[^>]*>[^<]*</button>', block)
        assert back is not None, f"kein Zurück-Knopf in #{panel}"
        assert "hidden" not in back.group(0), (
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
