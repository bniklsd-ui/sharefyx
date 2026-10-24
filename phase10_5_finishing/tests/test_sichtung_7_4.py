"""P10.5 Block 7.4 (UI-4) — die vier Posten der Sichtung vom 2026-10-24.

**Was hier geprüft wird.** Der Nikinger hat am 2026-10-24 acht Screenshots der Hauptansichten
gesichtet und **vier** Posten notiert (Wortmarken-Abstand · „Zugewiesen"-Auswahl · Update-Banner
kompakter · Versionsanzeige). Die Liste steht wortgleich in
`phase10_5_finishing/STARTUPTRAG_ARCHIVE.md`, Schritt 7.4; der Ausführer setzt sie in
`app.css`/`app.html`/`js/updates.js` um.

**Warum Wächter *und* Messung.** Die Browser-Probe (`probes/p105_b7_sichtung_probe.py`) belegt
das Aussehen **jetzt** — an einer Wegwerf-Instanz, mit Zahlen. Der Wächter hier belegt, dass
die **Werte** auch nach dem nächsten Block noch gelten; ein späterer Block, der `.45em` oder
`font-size: 9px` zurückschreibt, wird rot, ohne dass jemand noch einmal sichtet.

**Die Gegenprobe steckt in derselben Datei** (Muster aus `test_head_rules.py`): derselbe
Prüfer muss an einem Text mit dem **alten** Wert rot werden. Ein Wächter, der nur am echten
Stand grün ist, prüft nichts — die Fehlerklasse, die dieser Ordner schon zweimal gesehen hat.

**Was hier ausdrücklich NICHT geprüft wird:** das Aussehen. „Der Punkt ist erkennbar" und
„die Leiste ist kompakt" sind Blicke, keine Messwerte; die Messung dafür steht in der Probe
(Pixel des Punktes, Höhe der Leiste, Kanten der Auswahl), das Augen-Urteil bleibt beim
Nikinger (Sichtung 7.4 / Nachsichtung nach Block 11).
"""
from __future__ import annotations

import re
from pathlib import Path

REPO_ROOT = Path(__file__).resolve().parents[2]
STATIC = REPO_ROOT / "phase5_ui/webui/static"
CSS = STATIC / "app.css"
HTML = STATIC / "app.html"
UPDATES_JS = STATIC / "js/updates.js"

# Der Abstand, den die Wortmarke zwischen Zeichen und Wortrest haben DARF -- gemessen
# 2026-10-24: `.45em` waren 5,6 px in der Rail (12,5 px). Der Nikinger nannte den Abstand
# "zu groß"; `.2em` sind 2,5 px. Die Obergrenze ist 0,25 em, damit ein späterer Block
# nicht wieder auf "gemütlich" zurückschaltet.
MAX_MARK_GAP_EM = 0.25

# Die Versionsanzeige: 9 px las sich als "v316" (der Punkt war kein Zeichen mehr).
# 11 px + Laufweite: der Punkt ist wieder ein Punkt. Unter 10,5 px ist er es nicht.
MIN_VERSION_PX = 10.5


# -- Mini-CSS-Zeilenleser ---------------------------------------------------------------

def _regeln(css: str) -> list[tuple[list[str], str]]:
    """Die Regeln der obersten Ebene als (Selektorliste, Rumpf).

    **Eigener Zaehler statt Regex:** ein Regex ueber `([^{}]+)\\{([^{}]*)\\}` gleicht den
    Selektor gegen den Rest der Datei mit (Kommentare, vorherige Bloecke) und findet die
    @media-Bloecke nicht als Bloecke -- beides faengt hier einen Selektor nicht. Der Zaehler
    ueberspringt jeden @media-Block als Ganzes (die vier Posten stehen im Grundblatt) und
    liest die Kommentare vorher weg."""
    ohne_kommentare = re.sub(r"/\*.*?\*/", "", css, flags=re.DOTALL)
    regeln: list[tuple[list[str], str]] = []
    index = 0
    laenge = len(ohne_kommentare)
    while index < laenge:
        oeffnung = ohne_kommentare.find("{", index)
        if oeffnung < 0:
            break
        selektor = ohne_kommentare[index:oeffnung].strip()
        tiefe = 1
        zeiger = oeffnung + 1
        while zeiger < laenge and tiefe:
            if ohne_kommentare[zeiger] == "{":
                tiefe += 1
            elif ohne_kommentare[zeiger] == "}":
                tiefe -= 1
            zeiger += 1
        if not selektor.startswith("@"):
            regeln.append(([s.strip() for s in selektor.split(",")], ohne_kommentare[oeffnung + 1:zeiger - 1]))
        index = zeiger
    return regeln


def _declarations(css: str, selector: str) -> dict[str, str]:
    """Die Deklarationen der Regel mit genau diesem Selektor (als einer der
    Komma-Selektoren), **zusammengefasst** ueber alle Regeln mit diesem Selektor -- so
    arbeiten die spaeteren Regeln in CSS. Leere Menge, wenn es die Regel nicht gibt."""
    gesammelt: dict[str, str] = {}
    for selektoren, body in _regeln(css):
        if selector in selektoren:
            for key, value in re.findall(r"([-\w]+)\s*:\s*([^;]+);", body):
                gesammelt[key.strip()] = value.strip()
    return gesammelt


def _px(css: str, wert: str) -> float:
    """Wert in Pixeln. Rechnet `var(--space) * 2` und `12.5px` nach — der Wächter rechnet
    die Tokens nach, statt sie zu hartkodieren: `--space` kann sich ändern, ohne dass die
    Zahl im Test falsch wird."""
    wert = wert.strip()
    if wert.endswith("px"):
        return float(wert[:-2])
    if wert.endswith("em"):
        return float(wert[:-2]) * 16.0
    if wert.endswith("rem"):
        return float(wert[:-3]) * 16.0
    treffer = re.fullmatch(r"calc\(var\(--space\)\s*\*\s*([\d.]+)\)", wert)
    if treffer:
        return _px(css, _declarations(css, ":root").get("--space", "8px")) * float(treffer.group(1))
    raise AssertionError(f"Wert {wert!r} laesst sich nicht in Pixel umrechnen")


def _teile(wert: str) -> list[str]:
    """Die Whitespace-getrennten Teile eines CSS-Werts — **ohne** die Leerzeichen in
    `calc(...)` zu zaehlen. Ein blosses `wert.split()` zerlegt `calc(var(--space) * 2)`
    in vier Teile; das ist der Fehler, den der erste Wächter-Entwurf hatte."""
    teile: list[str] = []
    tiefe = 0
    aktuell = ""
    for zeichen in wert:
        if zeichen == "(":
            tiefe += 1
        elif zeichen == ")":
            tiefe -= 1
        if zeichen.isspace() and tiefe == 0:
            if aktuell:
                teile.append(aktuell)
                aktuell = ""
            continue
        aktuell += zeichen
    if aktuell:
        teile.append(aktuell)
    return teile


# -- Posten 1: der Abstand zwischen Wortmarke und Wortrest -------------------------------

def _pruefe_marken_abstand(css: str) -> None:
    deklarationen = _declarations(css, ".brand__mark")
    assert deklarationen, "app.css muss eine Regel fuer `.brand__mark` tragen"
    rohwert = deklarationen.get("margin-right", "")
    assert rohwert, (
        "`.brand__mark` braucht einen `margin-right` -- ohne ihn klebt das Zeichen der "
        "Wortmarke am Wortrest (Posten 1 der Sichtung vom 2026-10-24)."
    )
    wert = float(rohwert[:-2]) if rohwert.endswith("em") else _px(css, rohwert)
    assert 0 < wert <= MAX_MARK_GAP_EM, (
        f"der Abstand zwischen Zeichen und Wortrest ist {wert} em -- er war .45em und der "
        f"Nikinger nannte ihn zu gross (Sichtung 2026-10-24, Posten 1). Hoechstens "
        f"{MAX_MARK_GAP_EM} em, und keiner Null (sonst klebt es)."
    )


def test_posten_1_wortmarken_abstand_ist_klein():
    _pruefe_marken_abstand(CSS.read_text("utf-8"))


def test_posten_1_gegenprobe_der_alte_abstand_waere_rot():
    """Gegenprobe: der alte Wert `.45em` muss an **derselben** Pruefung rot werden."""
    css = CSS.read_text("utf-8")
    with_altem_wert = css.replace("margin-right: .2em;", "margin-right: .45em;", 1)
    assert with_altem_wert != css, "der Wert `.2em` steht nicht mehr in app.css"
    try:
        _pruefe_marken_abstand(with_altem_wert)
    except AssertionError:
        return
    raise AssertionError("der alte Abstand `.45em` ist grün geblieben -- der Wächter prüft nichts")


# -- Posten 2: die „Zugewiesen"-Auswahl traegt die Kanten der Zeile -------------------------

def _pruefe_auswahl_kanten(css: str) -> None:
    deklarationen = _declarations(css, ".list__assignee")
    assert deklarationen, "app.css muss eine Regel fuer `.list__assignee` tragen"
    breite = deklarationen.get("width", "")
    assert breite != "100%", (
        "`.list__assignee` darf nicht `width: 100%` haben -- dann laeuft die Auswahl "
        "buendig an den Listenrand, waehrend die Suchzeile darueber 16 px Innenabstand "
        "haelt (Posten 2 der Sichtung vom 2026-10-24)."
    )
    rand = deklarationen.get("margin", "")
    assert rand, "`.list__assignee` braucht einen horizontalen Innenabstand (`margin`)"
    teile = _teile(rand)
    assert len(teile) == 3, (
        f"`.list__assignee` braucht `margin: <oben> <links/rechts> <unten>` -- notiert ist {rand!r}"
    )
    innen_abstand = _px(css, teile[1])
    assert innen_abstand == _px(css, "calc(var(--space) * 2)"), (
        f"der Innenabstand der Auswahl ist {innen_abstand} px -- die Suchzeile darueber "
        f"traegt {int(_px(css, 'calc(var(--space) * 2)'))} px. Zwei Zeilen, eine Kante."
    )
    # Die Gesamtbreite muss der Zeile entsprechen: Breite + zwei Innenabstaende = 100 %.
    gesamt = _px(css, breite) if not breite.startswith("calc(100%") else None
    if gesamt is None:
        m = re.fullmatch(r"calc\(100%\s*-\s*var\(--space\)\s*\*\s*([\d.]+)\)", breite)
        assert m, f"die Breite {breite!r} laesst sich nicht lesen"
        gesamt = 100.0 - _px(css, f"calc(var(--space) * {m.group(1)})")
    assert abs((gesamt + 2 * innen_abstand) - 100.0) < 0.01, (
        f"Breite ({gesamt} px) + zweimal Innenabstand ({innen_abstand} px) = "
        f"{gesamt + 2 * innen_abstand} px -- es muss 100 % der Zeile sein."
    )


def test_posten_2_auswahl_traegt_die_kanten_der_zeile():
    _pruefe_auswahl_kanten(CSS.read_text("utf-8"))


def test_posten_2_gegenprobe_die_buendige_auswahl_waere_rot():
    """Gegenprobe: `width: 100%` (die alte, buendige Auswahl) muss rot werden."""
    css = CSS.read_text("utf-8")
    alt = css.replace(
        ".list__assignee {\n  width: calc(100% - var(--space) * 4);\n"
        "  margin: var(--space) calc(var(--space) * 2) 0;\n}",
        ".list__assignee {\n  width: 100%;\n  margin-top: var(--space);\n}",
        1,
    )
    assert alt != css, "die alte Fassung der Auswahl steht nicht mehr in app.css"
    try:
        _pruefe_auswahl_kanten(alt)
    except AssertionError:
        return
    raise AssertionError("die buendige Auswahl ist gruen geblieben -- der Wächter prüft nichts")


# -- Posten 3: das Update-Banner ist eine einzeilige Leiste --------------------------------

def _pruefe_banner(css: str, html: str, js: str) -> None:
    banner = _declarations(css, ".update-banner")
    assert banner, "app.css muss eine Regel fuer `.update-banner` tragen"
    vertikal = banner.get("padding", "")
    assert vertikal, "`.update-banner` braucht ein `padding`"
    teile = _teile(vertikal)
    assert len(teile) == 2, f"das `padding` des Banners ist {vertikal!r}"
    hoehe = _px(css, teile[0])
    assert hoehe <= 8.0, (
        f"der Banner hat {hoehe} px Polster oben und unten -- er war 8 px und deckte mit "
        f"seinen Zeilen bis zu ~140 px (Sichtung 2026-10-24, Posten 3)."
    )
    # Der Einzeiler: die Zeile bricht nicht um und schneidet ab.
    absatz = _declarations(css, ".update-banner__body p")
    assert absatz.get("white-space") == "nowrap", (
        "die Zeile des Banners muss einzeilig bleiben (`white-space: nowrap`) -- sonst haengt "
        "die Hoehe des Banners an der Laenge des Log-Eintrags."
    )
    assert absatz.get("text-overflow") == "ellipsis", (
        "der abgeschnittene Rest der Zeile muss sichtbar bleiben (`text-overflow: ellipsis`)."
    )
    # Der Fallback fuer die Hoehe: er war 80 px, das wuerde die Leiste wieder aufblaehen.
    wurzel = _declarations(css, ":root")
    assert "--banner-h" in wurzel, "app.css muss `--banner-h` setzen"
    assert _px(css, wurzel["--banner-h"]) <= 48.0, (
        f"der Fallback `--banner-h` ist {wurzel['--banner-h']} -- er muss zur einzeiligen "
        f"Leiste passen, sonst schiebt er die Ansicht beim ersten Frame zu weit nach unten."
    )
    # Der Knopf, der den ganzen Eintrag zeigt.
    assert 'id="update-banner-log"' in html, (
        "app.html muss den Knopf `#update-banner-log` tragen -- ohne ihn waere der Rest des "
        "Log-Eintrags nicht erreichbar, seit der Banner nur noch die Schlagzeile zeigt."
    )
    # Und der Knopf muss auch etwas tun.
    assert "openPanel" in js, "js/updates.js muss den Update-Log aus dem Banner oeffnen koennen"
    show = js.split("function showBanner", 1)[1].split("function hideBanner", 1)[0]
    assert "markdownList" not in show, (
        "der Banner darf nicht mehr alle Zeilen des Eintrags als Liste rendern -- das war die "
        "Hoehe von ~140 px (Sichtung 2026-10-24, Posten 3)."
    )
    assert re.search(r"zeilen\[0\]", show), (
        "der Banner muss die ERSTE Zeile des Eintrags nehmen (`zeilen[0]`)."
    )


def test_posten_3_banner_ist_eine_einzeilige_leiste():
    _pruefe_banner(CSS.read_text("utf-8"), HTML.read_text("utf-8"), UPDATES_JS.read_text("utf-8"))


def test_posten_3_gegenprobe_die_alle_zeilen_waeren_rot():
    """Gegenprobe: die alte Fassung (alle Zeilen als Liste, 8 px Polster, 80 px Fallback)
    muss an **derselben** Pruefung rot werden."""
    css = CSS.read_text("utf-8")
    html = HTML.read_text("utf-8")
    js = UPDATES_JS.read_text("utf-8")
    alt_css = css.replace(
        "  padding: 5px calc(var(--space) * 2);\n  font-size: var(--fs-meta);",
        "  padding: var(--space) calc(var(--space) * 3);\n  font-size: var(--fs-meta);", 1)
    alt_css = alt_css.replace(":root { --banner-h: 40px; }", ":root { --banner-h: 80px; }", 1)
    alt_js = js.replace("markdownToHtml(zeilen.length ? zeilen[0] : \"\")", "markdownToHtml(markdownList(latest.lines))", 1)
    assert alt_css != css and alt_js != js, "die alte Fassung des Banners steht nicht mehr im Quelltext"
    try:
        _pruefe_banner(alt_css, html, alt_js)
    except AssertionError:
        return
    raise AssertionError("die alte Banner-Fassung ist gruen geblieben -- der Wächter prüft nichts")


# -- Posten 4: die Versionsanzeige traegt Punkte ------------------------------------------

def _pruefe_version(css: str) -> None:
    deklarationen = _declarations(css, ".rail__version")
    assert deklarationen, "app.css muss eine Regel fuer `.rail__version` tragen"
    groesse = deklarationen.get("font-size", "")
    assert groesse, "`.rail__version` braucht eine `font-size`"
    px = _px(css, groesse)
    assert px >= MIN_VERSION_PX, (
        f"die Versionsanzeige ist {px} px -- bei 9 px las sie sich als \"v316\", der Punkt war "
        f"kein Zeichen mehr (Sichtung 2026-10-24, Posten 4). Mindestens {MIN_VERSION_PX} px."
    )
    laufweite = deklarationen.get("letter-spacing", "0")
    assert laufweite not in ("0", "0px", "normal"), (
        "die Versionsanzeige braucht Laufweite (`letter-spacing`) -- ohne sie klebt die "
        "Versionsnummer an der Wortmarke und die Punkte verschwinden zwischen den Ziffern."
    )


def test_posten_4_version_ist_lesbar():
    _pruefe_version(CSS.read_text("utf-8"))


def test_posten_4_gegenprobe_die_9px_version_waere_rot():
    """Gegenprobe: `font-size: 9px` (die alte, unlesbare Anzeige) muss rot werden."""
    css = CSS.read_text("utf-8")
    alt = css.replace(
        ".rail__version {\n  margin-left: .45em;\n  font-size: 11px;\n  font-weight: 400;\n"
        "  letter-spacing: .03em;",
        ".rail__version {\n  margin-left: .5em;\n  font-size: 9px;\n  font-weight: 400;\n"
        "  letter-spacing: 0;", 1)
    assert alt != css, "die alte Fassung der Versionsanzeige steht nicht mehr in app.css"
    try:
        _pruefe_version(alt)
    except AssertionError:
        return
    raise AssertionError("die 9-px-Version ist gruen geblieben -- der Wächter prüft nichts")
