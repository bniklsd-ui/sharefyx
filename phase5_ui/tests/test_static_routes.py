"""`GET /ui/`, `GET /ui/static/{path}` (Plan §5 Step 6). Läuft gegen die echten, im Repo
geschifften `webui/static/*`-Dateien (kein `tmp`-Fixture-Verzeichnis) — das ist bewusst: ein
Test, der gegen eine Attrappe grünt, während die echte `app.html` ein Inline-`<script>` enthält,
wäre wertlos. `ui_settings`s `static_dir` (Default `webui/static/`) bleibt deshalb unverändert.
"""
from __future__ import annotations

import re

import httpx
import pytest
from starlette.applications import Starlette

from webui.config import DEFAULT_STATIC_DIR
from webui.routes_auth import ui_auth_routes
from webui.static_routes import _resolve_static_path, static_routes

BASE_URL = "https://space.example.ts.net"
SPACE = "niklas"
PASSWORD = "correct horse battery staple"

_CSRF_RE = re.compile(r'name="csrf" value="([^"]+)"')


def _client(app) -> httpx.AsyncClient:
    return httpx.AsyncClient(transport=httpx.ASGITransport(app=app), base_url=BASE_URL)


@pytest.fixture
def static_app(ui_settings, store, confirmed_users, sessions) -> Starlette:
    routes = ui_auth_routes(ui_settings, store, confirmed_users, sessions) + static_routes(
        ui_settings, sessions
    )
    return Starlette(routes=routes)


async def _login(client: httpx.AsyncClient, totp_code) -> None:
    response = await client.post(
        "/ui/login", data={"space": SPACE, "password": PASSWORD, "totp": totp_code()},
    )
    assert response.status_code == 200


def _font_filename() -> str:
    # Generischer Glob seit Phase 8 C1: das Webfont-Subset heißt je nach Schrift "InterVariable-subset.*.woff2"
    # (P5) oder "IBMPlex{Sans,Mono}-subset.*.woff2" (P8). Was hier gelesen wird, ist dem Test egal —
    # er prüft nur, dass die Static-Routes (Content-Type, Cache-Header) für das Muster stimmen, nicht
    # welcher konkrete Schnitt gebaut wurde. Wer einen Schriftnamen einführt, der nicht auf "-subset"
    # endet, bricht diesen Test, weil er dann auch das Routing/Caching bricht.
    matches = list(DEFAULT_STATIC_DIR.glob("fonts/*-subset.*.woff2"))
    assert matches, "kein gebautes Font-Subset unter webui/static/fonts/ gefunden"
    return matches[0].name


@pytest.mark.asyncio
async def test_index_route_requires_session(static_app, totp_code):
    async with _client(static_app) as client:
        anonymous = await client.get("/ui/", follow_redirects=False)
        assert anonymous.status_code == 303
        assert anonymous.headers["location"] == "/ui/login"

        await _login(client, totp_code)
        authenticated = await client.get("/ui/", follow_redirects=False)
        assert authenticated.status_code == 200
        assert "text/html" in authenticated.headers["content-type"]
        assert "<html" in authenticated.text


@pytest.mark.asyncio
async def test_app_loads_as_a_single_es_module(static_app, totp_code):
    """Step 7: der frühere Zwei-Skript-Aufbau (`js/updates.js` als globales Skript VOR `app.js`,
    Ladereihenfolge-Pflicht wegen `window.SharefyxUpdates`) ist mit dem Split in ES-Module
    entfallen — `updates.js` ist jetzt selbst ein Modul, das `app.js` ganz normal per `import`
    lädt, kein globaler Name, keine Reihenfolge-Regel mehr nötig. Genau EIN `<script
    type="module">`-Tag, das den neuen Einstiegspunkt referenziert; kein altes Skript-Tag auf
    den entfernten Top-Level-Pfad `/ui/static/app.js` (jetzt `/ui/static/js/app.js`)."""
    async with _client(static_app) as client:
        await _login(client, totp_code)
        response = await client.get("/ui/")
    html = response.text
    script_tags = re.findall(r"<script\b[^>]*>", html)
    assert script_tags == ['<script type="module" src="/ui/static/js/app.js">']


_JS_MODULES = (
    "app", "api", "state", "tree", "list", "editor", "markdown", "dialogs", "toasts", "updates",
    "spaces",
)


@pytest.mark.asyncio
async def test_static_files_are_served_with_correct_content_type(static_app):
    font_name = _font_filename()
    cases = {
        "app.html": "text/html",
        "app.css": "text/css",
        f"fonts/{font_name}": "font/woff2",
    }
    cases.update({f"js/{name}.js": "text/javascript" for name in _JS_MODULES})
    async with _client(static_app) as client:
        for path, expected in cases.items():
            response = await client.get(f"/ui/static/{path}")
            assert response.status_code == 200, path
            assert expected in response.headers["content-type"], path


@pytest.mark.asyncio
async def test_static_hashed_assets_get_immutable_cache_header(static_app):
    font_name = _font_filename()
    async with _client(static_app) as client:
        hashed = await client.get(f"/ui/static/fonts/{font_name}")
        assert "immutable" in hashed.headers["cache-control"]

        unhashed = await client.get("/ui/static/js/app.js")
        assert unhashed.headers["cache-control"] == "no-store"


def test_resolve_static_path_rejects_traversal():
    # Direkt gegen `_resolve_static_path()`, nicht über HTTP: `httpx`/ASGI-Server normalisieren
    # `../`-Segmente in der URL oft schon vor dem Routing weg — das würde eine echte Lücke im
    # eigenen Guard verdecken, statt sie zu belegen (das eigentliche Risiko ist ein Client, der
    # NICHT normalisiert).
    assert _resolve_static_path(DEFAULT_STATIC_DIR, "app.css") is not None
    assert _resolve_static_path(DEFAULT_STATIC_DIR, "../config.py") is None
    assert _resolve_static_path(DEFAULT_STATIC_DIR, "fonts/../../config.py") is None
    assert _resolve_static_path(DEFAULT_STATIC_DIR, "/etc/passwd") is None
    assert _resolve_static_path(DEFAULT_STATIC_DIR, "does-not-exist.css") is None


def test_app_html_contains_no_inline_script():
    html = (DEFAULT_STATIC_DIR / "app.html").read_text("utf-8")
    for match in re.finditer(r"<script\b[^>]*>", html):
        assert "src=" in match.group(0), f"Inline-<script> gefunden: {match.group(0)!r}"


def test_app_html_contains_no_inline_style_attribute():
    html = (DEFAULT_STATIC_DIR / "app.html").read_text("utf-8")
    assert "style=" not in html


def test_app_html_has_a_live_manage_spaces_entry():
    """P7 Step C3 — der Menüpunkt ist jetzt scharf: kein `disabled` mehr, kein Verweis auf
    „Phase 7" (die Fläche ist diese Phase). Sichtbarkeit zur Laufzeit folgt `state.meta.
    space_admin` (`app.js`), nicht diesem statischen Markup (P5-T, kein Templating)."""
    html = (DEFAULT_STATIC_DIR / "app.html").read_text("utf-8")
    match = re.search(r'<button[^>]*id="account-manage-spaces"[^>]*>([^<]*)</button>', html)
    assert match is not None, "Menüpunkt 'Spaces verwalten' fehlt"
    assert "disabled" not in match.group(0)
    assert "Phase 7" not in html


def test_app_js_makes_no_external_requests():
    for name in _JS_MODULES:
        js = (DEFAULT_STATIC_DIR / "js" / f"{name}.js").read_text("utf-8")
        for needle in ("http://", "https://", "//cdn"):
            assert needle not in js, f"externe Referenz {needle!r} in js/{name}.js gefunden"


def test_write_controls_live_inside_detachable_containers():
    """Akzeptanzkriterium 12 verlangt bei einem fremden Space Schreib-Bedienelemente **nicht im
    DOM** — nicht bloß `hidden`. Bis Step 7b standen Editor, „+"-Knopf und Anlegen-Dialog
    permanent in `app.html` und waren nur ausgeblendet, also mit DevTools auffindbar; Step 7b
    hängt sie in `app.js :: detachable()` bei Bedarf aus dem Dokument aus.

    Dieser Test kann das Laufzeitverhalten nicht prüfen (JavaScript bleibt laut Plan
    unit-ungetestet, dafür lief die jsdom-Simulation). Er hält die Voraussetzung fest, auf der
    das Aushängen beruht: jedes Schreib-Bedienelement sitzt in genau einem der drei Container,
    die `state.js` aushängt (Step 7: aus `app.js` dorthin verschoben, `editorPart`/
    `createTriggers`/`createDialogPart` müssen von mehreren Modulen dieselbe Instanz teilen).
    Ein neuer Speichern-Knopf, den jemand außerhalb davon platziert, fällt hier auf statt erst
    live."""
    html = (DEFAULT_STATIC_DIR / "app.html").read_text("utf-8")
    js = (DEFAULT_STATIC_DIR / "js" / "state.js").read_text("utf-8")

    for container in ("detailEditorEl", "newItemButtonEl", "createButtonEl", "createDialogEl"):
        assert f"detachable({container})" in js, f"{container} wird nicht mehr ausgehängt"

    # Die Knöpfe, die schreiben, stehen im Editor-Teilbaum — geprüft über ihre Position im
    # Quelltext zwischen der öffnenden `#detail-editor`-Zeile und dem Anlegen-Dialog.
    editor_start = html.index('<div id="detail-editor"')
    editor_end = html.index('<div class="toast"')
    editor_markup = html[editor_start:editor_end]
    for control in ('id="save-button"', 'id="archive-button"', 'id="append-button"',
                    'id="editor-textarea"'):
        assert control in editor_markup, f"{control} liegt außerhalb von #detail-editor"


def test_link_picker_css_has_one_selection_block():
    """P8.5-14: app.css hat genau einen Auswahl-Block für den Link-Picker, kein totes `:focus`.

    Vor A2 gab es zwei identische Regelblöcke -- einen für `li:hover`/`li:focus` und einen
    für `li[aria-selected="true"]` -- beide mit denselben vier Deklarationen. Die `:focus`-
    Hälfte war toter Code (kein `tabindex` auf den `li`, kann nie feuern). A2 hat sie auf
    genau einen Block zusammengezogen: `li:hover` + `li[aria-selected="true"]`. Wer einen
    dritten Auswahl-Standard daneben stellt, fällt hier auf statt erst im Browser.
    """
    css = (DEFAULT_STATIC_DIR / "app.css").read_text("utf-8")
    assert css.count('li[aria-selected="true"]') == 1, (
        "app.css muss genau einen Auswahl-Block für den Link-Picker tragen "
        "(Phase 8.5 A2-Entdopplung)."
    )
    assert ".link-picker-results li:focus" not in css, (
        "Totes `.link-picker-results li:focus` darf nicht mehr vorkommen "
        "(kein tabindex auf den li, kann nie feuern)."
    )


def test_link_picker_picks_run_through_a_single_helper():
    """P8.5-12: Tastatur- und Maus-Pfad laufen beide durch `_pickLinkPickerAt`.

    Statt zweier separater Code-Pfade -- einer für den Klick-Listener in
    `_renderLinkPickerResults`, einer für den Enter-Handler im keydown des Suchfelds --
    rufen beide genau dieselbe Funktion. `app.js` bleibt außen vor (P8.5-L, dort darf
    kein Link-Picker-Handler sein, der den Helper umgeht).
    """
    dialogs = (DEFAULT_STATIC_DIR / "js" / "dialogs.js").read_text("utf-8")
    app_js = (DEFAULT_STATIC_DIR / "js" / "app.js").read_text("utf-8")
    # Genau eine Definition des Helpers in dialogs.js (Definition + 2 Aufrufe = 3 Vorkommen).
    assert dialogs.count("function _pickLinkPickerAt(") == 1, (
        "_pickLinkPickerAt muss genau einmal in dialogs.js definiert sein."
    )
    assert dialogs.count("_pickLinkPickerAt(") >= 3, (
        "Mindestens drei Vorkommen erwartet (1 Definition + Maus-Klick + Enter-Taste)."
    )
    # app.js bleibt tabu -- keine Picker-Handler, die am Helper vorbeilaufen würden.
    assert "openLinkPicker" not in app_js, (
        "app.js darf den Link-Picker nicht öffnen (P8.5-L)."
    )
    assert "_pickLinkPickerAt" not in app_js, (
        "app.js darf den Pick-Helper nicht umgehen -- Picker-Logik gehört nach dialogs.js."
    )


def test_insertAtCursor_defined_exactly_once_at_module_level():
    """P8.5-9: `insertAtCursor` existiert genau einmal, auf Modulebene; alle Alt-Aufrufe
    in `init()` funktionieren unverändert.

    Die Phase-8.5-A1-Anforderung (P8.5-I: `insertAtCursor` aus `init()` auf Modulebene
    gehoben, damit der Link-Picker-Pfad darauf zugreifen kann) war bislang nur per
    `grep -n` belegt. Jetzt mit pytest festgehalten: die function-Deklaration darf
    genau einmal vorkommen -- bei mehreren wäre unklar, welcher die Quelle der Wahrheit
    ist; bei null würde der Bild-Knopf-Aufruf (jetzt Z. 669) eine Referenz auf eine
    undefinierte Funktion tragen.

    Implizit über die Modul-Ebene: der Bild-Knopf-Listener liegt außerhalb von `init()`
    und kann den Helper nur sehen, wenn er auf Modul-Ebene deklariert ist -- eine
    function-Deklaration innerhalb von `init()` wäre über Function-Scoping außerhalb
    nicht sichtbar. Der Test prüft "genau einmal definiert" als Stellvertreter für die
    strukturelle Eigenschaft.
    """
    editor = (DEFAULT_STATIC_DIR / "js" / "editor.js").read_text("utf-8")
    assert editor.count("function insertAtCursor(") == 1, (
        "insertAtCursor muss genau einmal in editor.js definiert sein "
        "(Phase 8.5 A1, P8.5-I: auf Modulebene gehoben)."
    )


def test_link_picker_uses_a_select_not_a_radio_group():
    """P8.6-A1 (P8.6-H/I): Modus-Umschalter ist wieder ein **`<select class="input">`**,
    nicht die Radiogruppe aus P8.5-19.

    Historie (Docstring trägt beide Richtungen, P8.6-I):
      - 2026-09-06: Radiogruppe angeordnet (P8.5-19, Nikinger-Fund D4) --
        die Sichtpruefung war "deutlich angenehmer", ein Umschalter aendert
        *was ein Klick tut*, und das soll der Nutzer vor dem Klick sehen.
      - 2026-09-08: Nikinger nimmt das **selbst** zurueck (Handover §4.2) --
        die Selection/Choice-Konvention v3 verlangt Choice = nativ <select>;
        eine offene Ausnahme waere eine Regel mit eingebautem Gegenbeispiel.
    Bauform heute:
      <div class="input input--labeled">
        <label class="input-label-inline" for="link-picker-mode">Einfügen</label>
        <select class="input" id="link-picker-mode">
          <option value="body" selected>als Text-Link im Text</option>
          <option value="frontmatter">als Kante (Feld „Links")</option>
        </select>
      </div>
    `localStorage["sfx:linkpicker:mode"]` und sein Wert bleiben unveraendert -- Nutzer
    behalten ihre Wahl beim Bauform-Wechsel.

    Wer spaeter wieder eine Radiogruppe einbaut (oder das alte `LINK_PICKER_MODE_NAME`-
    Selektor-Konstrukt zurueckbringt), faellt hier auf statt erst in der naechsten
    Sichtpruefung.
    """
    html = (DEFAULT_STATIC_DIR / "app.html").read_text("utf-8")
    dialogs = (DEFAULT_STATIC_DIR / "js" / "dialogs.js").read_text("utf-8")

    # Markup: <select class="input" id="link-picker-mode"> mit genau zwei <option> in der
    # richtigen Reihenfolge. `body` ist default (selected), `frontmatter` danach.
    select_pattern = re.compile(
        r'<select\s+class="input"\s+id="link-picker-mode">\s*'
        r'<option\s+value="body"\s+selected>[^<]+</option>\s*'
        r'<option\s+value="frontmatter">[^<]+</option>\s*'
        r'</select>',
        re.DOTALL,
    )
    assert select_pattern.search(html), (
        "Picker-Modus-Markup fehlt: erwartet <select class=\"input\" id=\"link-picker-mode\"> "
        "mit zwei <option> ('body' selected, 'frontmatter') in dieser Reihenfolge (P8.6-H)."
    )

    # Fieldset+Legend-Konstrukt (Radiogruppe) ist weg.
    assert 'class="link-picker-modes"' not in html, (
        "Die alte Radiogruppe (class=\"link-picker-modes\") darf nicht mehr vorkommen "
        "(P8.6-A1, Radiogruppe-><select>-Rueckbau)."
    )

    # Radio-Eingaben unter dem Namen 'link-picker-mode' sind weg.
    assert 'name="link-picker-mode"' not in html, (
        "Die Radios unter name=\"link-picker-mode\" duerfen nicht mehr vorkommen "
        "(P8.6-A1, Radiogruppe-><select>-Rueckbau)."
    )

    # JS: die alte LINK_PICKER_MODE_NAME-Konstante und der Name-Selektor sind weg,
    # der ID-Selektor ist wieder da (getElementById).
    assert "LINK_PICKER_MODE_NAME" not in dialogs, (
        "dialogs.js darf die alte Konstante LINK_PICKER_MODE_NAME nicht mehr enthalten "
        "(P8.6-A1, Name-Selektor -> ID-Selektor)."
    )
    assert "input[name=\"link-picker-mode\"]" not in dialogs, (
        "dialogs.js darf nicht mehr nach 'input[name=\"link-picker-mode\"]' suchen -- "
        "die Radios sind weg, der <select> hat eine ID."
    )
    assert 'getElementById("link-picker-mode")' in dialogs, (
        "dialogs.js muss den <select> per getElementById('link-picker-mode') finden -- "
        "ID-Selektor ist zurueck."
    )


def test_markdown_link_regex_allows_escaped_brackets():
    r"""P8.5-6 (D4-Nikinger-Fund 2026-09-06, Pre-Z-Tausch 2026-09-07): Link- und Bild-Regex
    in `markdown.js` tolerieren `\[` / `\]` als Escape im Title/Alt.

    Vor dem Fix matchte `\[([^\]]+)\]` gierig bis zum ersten `]`, und ein vom Picker
    eingefuegter Titel wie `Notiz \[Entwurf\]` (Picker-Maskierung in `editor.js ::
    _linkTextFor`) zerlegte die URL-Zuordnung -- eckige Klammern ja, runde nein.
    Der Fix fuehrt `\\[\[\]]` als Alternative ein (zwei Zeichen als Einheit), und der
    gefangene Text wird danach per `\\([\[\]])` -> `$1` unescaped, damit der gerenderte
    Link-Text die Klammern literal zeigt.

    Statisch verifiziert (statt jsdom-Probe): die Regex-Quellen tragen den neuen Baustein.
    Wer den Fix rueckgaengig macht oder auf die alte `[^\]]+`-Form zurueckfaellt, faellt
    hier auf.
    """
    md = (DEFAULT_STATIC_DIR / "js" / "markdown.js").read_text("utf-8")

    # Beide Regex -- Link und Bild -- muessen die Escap-Einheit tragen.
    # Pattern: ein Backslash, gefolgt von [ oder ]. In JS-Quelltext als "\\[\[\]]" notiert.
    assert r"\\[\[\]]" in md, (
        r"Link-/Bild-Regex in markdown.js muss `\\[\[\]]` als Escape-Einheit tragen "
        r"(zwei Zeichen als Einheit: Backslash + [ oder ]). Vor P8.5-6 fehlte das, "
        r"eckige Klammern im Link-Text zerlegten die URL-Zuordnung."
    )
    # Unescape-Schritt: nach dem Match werden \\X -> X rueckuebersetzt, damit der
    # gerenderte Link-Text die Klammern literal zeigt (statt mit Backslash).
    assert r"\\([\[\]])" in md, (
        r"markdown.js muss `\\([\[\]])` -> `$1` nach dem Regex-Match anwenden, "
        r"damit der gerenderte Link-Text `Notiz [Entwurf]` statt `Notiz \[Entwurf\]` zeigt."
    )
    # Negative Regression: die alte, zu strenge Form darf nicht (mehr) allein stehen.
    # Sie steht im Code nirgends mehr als regex.source, weil der Fix sie ersetzt hat.
    assert re.search(r"replace\(/\[\^\]\][^\]]*\\\]\(\[\^\)\\\s\]\+\)\/g", md) is None, (
        r"Alte Regex `\[([^\]]+)\]\(([^)\s]+)\)` darf nicht mehr im markdown.js stehen "
        r"-- sie ist die Ursache des Bracket-Bugs und wurde durch die Escape-tolerante Form ersetzt."
    )


def test_no_raw_accent_rgba_outside_root():
    """P8.6-A2 (P8.6-C): maschineller Wächter ueber die fünf rohen `rgba(62,141,243,...)`,
    die vor Block A in `app.css` dupliziert waren.

    Vor Block A stand der Akzent-Verlauf vier Mal woertlich identisch im Stylesheet
    (`app.css:403/685/719/1291`) plus eine `.35`-Variante an `app.css:785` -- jeder
    kuenftige Hue-Shift haette vier Stellen treffen muessen. Block A fuehrt die zwei
    Token `--select-fill` (voller Verlauf) und `--select-line` (volle Akzent-Linie) ein,
    und ersetzt alle fuenf Vorkommen durch Verweise.

    Wer nach Block A wieder einen rohen `rgba(62,141,243,...)`-Wert irgendwo ausserhalb
    des `:root`-Blocks einfuegt (Background, Border, Outline, was auch immer), faellt
    hier auf. Ein Kommentar in `:root`, der das Pattern erklaert, ist erlaubt --
    die Assertion matcht nur die Funktion `rgba(...)`, nicht den Literal-String.
    """
    css = (DEFAULT_STATIC_DIR / "app.css").read_text("utf-8")

    # :root-Block abschneiden -- dort darf das Pattern stehen (Token-Definitionen +
    # Kommentar).
    stripped = re.sub(r":root\s*\{[^}]*\}", "", css, flags=re.DOTALL)

    # Akzent-rgba darf ausserhalb von :root nicht mehr vorkommen.
    matches = re.findall(r"rgba\(\s*62\s*,\s*141\s*,\s*243", stripped)
    assert not matches, (
        f"Roher rgba(62,141,243,...) ausserhalb von :root gefunden: "
        f"{len(matches)} Vorkommen. P8.6-C verlangt die Token --select-fill / "
        f"--select-fill-quiet / --select-line / --select-line-quiet. "
        f"Erste Treffer-Zeile mit `grep -n 'rgba(62,141,243' app.css` finden."
    )


def test_every_css_var_reference_is_defined():
    """P8.6-A3 (P8.6-C/F): jedes `var(--x)` in `app.css` muss **irgendwo** in der Datei
    definiert sein.

    Der Wunsch klingt trivial, ist aber die einzige strukturelle Antwort auf den
    `--border-soft`-Renderfehler (Plan §1.8, Step-0-Fund): ein Token, der im Quelltext
    steht, aber nirgendwo ein `--border-soft:` hat, zeichnet still einen leeren Wert
    und niemand merkt es bis zur naechsten Sichtpruefung.

    **Wichtig -- warum die Assertion NICHT auf `:root` einengt:** `@supports`-Bloecke
    und andere Scopes (z. B. der Phase-8-Glass-Fallback unter `@supports (backdrop-filter)`)
    definieren zulaessigerweise Tokens ausserhalb von `:root`. Eine zu strenge Variante
    wuerde diese zurechtgestellten Stellen als Fehler markieren. **Auch** `--caution:
    var(--danger)` ist eine `var()`-Referenz *innerhalb* von `:root` -- die Assertion
    matcht Referenzen, nicht Werte, also ist die Alias-Definition selbst kein Problem.
    Tokens werden oft inline in einer Property-Zeile definiert (z. B. `:root { --banner-h: 80px; }`
    statt einer eigenen Zeile) -- auch diese Variante muss matchen.

    Kommentare werden vor dem Vergleich entfernt, damit historische Notizen wie
    `color: var(--accent-text) -- letzteres Token war nirgends definiert` (P8.5-Step-7b-
    Erklaerung in einem Kommentar) nicht als "Referenz ohne Definition" gezaehlt werden.

    Wer einen Token benutzt, der nicht (irgendwo) definiert ist, faellt hier auf --
    auch der naechste Bug dieser Klasse.
    """
    css = (DEFAULT_STATIC_DIR / "app.css").read_text("utf-8")

    # CSS-Kommentare entfernen -- sie koennen historische Token-Namen erwaehnen, die
    # es heute nicht mehr gibt (P8.5-Step-7b erklaert z. B. `--accent-text`).
    css_no_comments = re.sub(r"/\*.*?\*/", "", css, flags=re.DOTALL)

    # Alle `var(--xxx)`-Referenzen einsammeln. Pattern: `var(--name` (Klammer oder Komma folgt).
    refs = set(re.findall(r"var\(\s*(--[a-zA-Z0-9_-]+)\s*[,)]", css_no_comments))

    # Alle `--xxx:`-Definitionen einsammeln. KEIN Zeilen-Anchor, weil Tokens auch inline
    # in einer Property-Zeile stehen koennen (`:root { --banner-h: 80px; }`).
    defs = set(re.findall(r"(--[a-zA-Z0-9_-]+)\s*:", css_no_comments))

    undefined = refs - defs
    assert not undefined, (
        f"Undefinierte CSS-Variablen in app.css: {sorted(undefined)}. "
        f"Jedes `var(--x)` braucht ein `--x:` (irgendwo in der Datei, nicht nur in :root). "
        f"Dieser Test haette den --border-soft-Bug gefunden -- und findet den naechsten."
    )


def test_caution_class_only_on_logout_and_archive():
    """P8.6 B4 (Plan §4.4 P8.6-G): Kategorie "Vorsicht" (Konvention v3, fünfte Kategorie in
    `phase8_ui_graph/CLAUDE.md` Selection/Choice-Konvention v3) wird über die Trägerklasse
    `action--caution` markiert. Genau zwei Elemente tragen sie:

      - `#logout-button`  -- einziges Rail-Mitglied (Session beenden)
      - `#archive-button` -- einziges Editor-Mitglied (Item ins Archiv verschieben)

    Beide Aktionen haben Rückweg-Kosten: Logout invalidiert UI-Session + aktive Connector-
    Token-Familien, Archivieren entfernt das Item aus der Standardansicht. "Verschieben",
    "Abwählen", "Erste Notiz anlegen", "Space verwalten" sind alle folgenlos oder trivial
    umkehrbar -- deshalb KEIN drittes Mitglied.

    Der Test zählt die Vorkommen im Markup UND prüft, dass die zwei Elemente die richtigen
    sind. Wer ein drittes Element mit der Klasse versieht (oder die alte ID-Selektor-Form
    `#logout-button { color: var(--caution) }` wieder einführt), fällt hier auf statt erst in
    der nächsten Sichtprüfung.
    """
    html = (DEFAULT_STATIC_DIR / "app.html").read_text("utf-8")

    # Genau zwei Vorkommen der Trägerklasse im Markup.
    assert html.count("action--caution") == 2, (
        "Trägerklasse `action--caution` muss genau zweimal in app.html vorkommen "
        "(P8.6 B4: Vorsicht-Kategorie mit genau zwei Mitgliedern). "
        f"Aktuelle Anzahl: {html.count('action--caution')}."
    )

    # Die zwei Elemente müssen die richtigen sein.
    logout_match = re.search(
        r'<button[^>]*id="logout-button"[^>]*>',
        html,
    )
    assert logout_match is not None, "#logout-button fehlt im Markup"
    assert "action--caution" in logout_match.group(0), (
        "#logout-button muss Trägerklasse `action--caution` tragen "
        "(P8.6 B4: einziges Rail-Mitglied der Vorsicht-Kategorie)."
    )

    archive_match = re.search(
        r'<button[^>]*id="archive-button"[^>]*>',
        html,
    )
    assert archive_match is not None, "#archive-button fehlt im Markup"
    assert "action--caution" in archive_match.group(0), (
        "#archive-button muss Trägerklasse `action--caution` tragen "
        "(P8.6 B4: einziges Editor-Mitglied der Vorsicht-Kategorie)."
    )

    # Die CSS-Regel existiert und referenziert --caution (statt z. B. var(--danger) direkt
    # zu wiederholen -- die Konvention verbietet zwei Farbnamen für dieselbe Bedeutung, P8.6-F).
    css = (DEFAULT_STATIC_DIR / "app.css").read_text("utf-8")
    assert ".action--caution" in css, (
        "app.css muss eine Regel für `.action--caution` tragen (P8.6 B4)."
    )
    assert "var(--caution)" in css, (
        "app.css muss `var(--caution)` verwenden (P8.6-F: ein Farbname pro Bedeutung, "
        "--danger und --caution teilen denselben Wert -- die Trägerklasse ist die "
        "semantische Differenzierung)."
    )


def test_rail_order_settings_before_tree_logout_last():
    """P8.6 Block C C1 (Plan §5.1): Reihenfolge im Rail ist jetzt
        1. .rail__brand
        2. #home-button           ("Übersicht")
        3. #account-button        ("Einstellungen")   <-- NEU: wandert hierhin
        4. #rail-tree             (Spaces + "Alle Items")
        5. #logout-button         ("Abmelden")        <-- letztes Kind in .rail__account

    Begründung (Plan §5.1): ein wörtlicher Tausch würde "Abmelden" an die prominenteste
    Stelle des Account-Blocks setzen -- Abmelden ist die seltenste und teuerste Aktion,
    Einstellungen (Zahnrad) ist häufig und folgenlos. N3-Lesart b ist bestätigt, nicht
    geraten.

    Wer die Reihenfolge umstellt (Einstellungen wieder nach unten, oder Abmelden nach oben),
    fällt hier auf statt erst in der nächsten Sichtprüfung. Test über die Reihenfolge der
    Tag-Positionen im HTML-String -- billig und robust gegen CSS-Layout-Änderungen.
    """
    html = (DEFAULT_STATIC_DIR / "app.html").read_text("utf-8")

    def _pos(tag_id: str) -> int:
        m = re.search(rf'id="{re.escape(tag_id)}"', html)
        assert m is not None, f"#{tag_id} fehlt im Markup"
        return m.start()

    pos_home = _pos("home-button")
    pos_account = _pos("account-button")
    pos_tree = _pos("rail-tree")
    pos_logout = _pos("logout-button")

    assert pos_home < pos_account, (
        f"#account-button (Einstellungen) muss NACH #home-button stehen, nicht davor. "
        f"Positionen: home={pos_home}, account={pos_account}."
    )
    assert pos_account < pos_tree, (
        f"#account-button (Einstellungen) muss VOR #rail-tree stehen -- das ist der Kern "
        f"von C1 (Plan §5.1, N3-Lesart b: Einstellungen oben, Abmelden ans Rail-Ende). "
        f"Positionen: account={pos_account}, tree={pos_tree}."
    )
    assert pos_tree < pos_logout, (
        f"#logout-button (Abmelden) muss ALS LETZTES im Rail stehen -- .rail__account ist "
        f"das Rail-Ende (margin-top: auto), und nach C1 ist Abmelden das einzige Kind dort. "
        f"Positionen: tree={pos_tree}, logout={pos_logout}."
    )


def test_account_button_says_einstellungen():
    """P8.6 Block C C1 (Plan §5.1): Label ist "Einstellungen", nicht "Konto" -- das Icon
    war schon immer ein Zahnrad (P5 Step 7b, app.css :: .icon), der Name hinkte hinterher.

    Wer den alten String zurückbringt (z. B. als vermeintliche Lokalisierung), fällt hier
    auf. Test über das <span class="rail__label">-Kind innerhalb des #account-button-Tags,
    nicht über freien Text im HTML -- sonst würde ein Kommentar wie "Konto-Dialog" im
    Quelltext fälschlich matchen.
    """
    html = (DEFAULT_STATIC_DIR / "app.html").read_text("utf-8")

    match = re.search(
        r'<button[^>]*id="account-button"[^>]*>(.*?)</button>',
        html,
        flags=re.DOTALL,
    )
    assert match is not None, "#account-button fehlt im Markup"
    button_html = match.group(0)

    assert "Einstellungen" in button_html, (
        "#account-button muss 'Einstellungen' als Label tragen (P8.6 C1, N3-Lesart b)."
    )
    assert ">Konto<" not in button_html, (
        "#account-button darf NICHT mehr 'Konto' als Label tragen (P8.6 C1: 'Konto' ist "
        "weggefallen, das Zahnrad war schon immer ein Settings-Icon)."
    )


def test_overview_graph_has_no_max_width_or_min_height():
    """P8.6 Block C C3 (Plan §5.3): `.overview__graph` hat WEDER `max-width` (vorher 960px)
    NOCH `min-height` (vorher 55vh). Beide entfallen, weil der Container die Höhe aus
    der `.detail__graph`-Kette bezieht (siehe `test_detail_graph_has_a_definite_height_
    chain`).

    Dies ist der §2.3-Regressionswächter -- wer den alten 55vh-Trick zurückbringt, fällt
    hier auf. Test über CSS-String-Matching: die Regel darf in keiner **bloßen**
    `.overview__graph`-Deklaration diese Properties mehr enthalten.

    Phase 8.6 Plan 2 Block G G2: nach Block G trägt `.detail__graph .overview__graph`
    eine Flex-Basis-Definition (`flex: 1; min-height: 0`), die compound-Selector --
    absichtlich, der Wert ist hier kein Cap, sondern die Höhenweitergabe aus der Kette.
    Der Test matcht deshalb den **bloßen** Selektor `.overview__graph` am Zeilenanfang,
    nicht den compound. Anker `^` mit `re.MULTILINE`, weil `re.VERBOSE` / Lookbehinds
    fragile gegen CSS-Reformulierungen sind.
    """
    css = (DEFAULT_STATIC_DIR / "app.css").read_text("utf-8")

    # Phase 8.6 Plan 2 Block G: nur die bloße `.overview__graph { ... }`-Regel matchen,
    # NICHT `.detail__graph .overview__graph { ... }` (die trägt absichtlich `min-height: 0`
    # als Teil der Höhenkette, siehe §4.2.1). `^`-Anker mit `re.MULTILINE` ist robust gegen
    # Whitespace-Variationen und block-interne Zeilenumbrüche.
    matches = list(re.finditer(r"^\.overview__graph\s*\{([^}]*)\}", css, flags=re.MULTILINE))
    assert matches, (
        "app.css muss mindestens eine Regel für `.overview__graph` enthalten "
        "(sonst wäre der Test wirkungslos)."
    )

    for m in matches:
        body = m.group(1)
        assert "max-width" not in body, (
            f"`.overview__graph` darf kein `max-width` mehr tragen (P8.6 C3). "
            f"Block: {body.strip()}"
        )
        assert "min-height" not in body, (
            f"`.overview__graph` darf kein `min-height` mehr tragen (P8.6 C3, V112-Gegenprobe). "
            f"Block: {body.strip()}"
        )


def test_no_raw_surface_hex_outside_root():
    """P8.6-AD (Plan §8.2): Wächter über die drei rohen Flächen-Hex `#0E1116`, `#131A23`,
    `#1A2029`, die vor Block F als `.rail`-, Login- und `.auth-card`-Verlauf in `app.css`
    standen.

    Jede `background`-Deklaration außerhalb `:root` muss entweder `var(--…)` führen oder
    eine **dokumentierte Ausnahme** sein. Ausnahmen (vom Plan erlaubt):

      - `#fff` in `.qr-frame` (P8.6-AD wörtlich — QR-Code braucht echtes Weiß, keine
        Flächen-Semantik). Diese Stelle trägt einen begründenden Kommentar.
      - Die neun Hex-Werte der Space-Kategorien-Glyphen
        (`.rail__glyph--own/--shared/--foreign`, app.css Zeilen 499/504/509) — das sind
        Kategoriefarben, vom Plan §3.3 explizit ausgenommen („keine Grautöne, bleiben").

    Vor Block F waren es 17 rohe Hex-Treffer außerhalb `:root` (drei davon die hier
    zu schließenden Flächen-Hex); nach Block F sind es 11 Treffer, alle entweder
    dokumentierte Ausnahme (`#fff` QR) oder Space-Kategorie.

    Wer nach Block F wieder einen rohen Flächen-Hex irgendwo außerhalb des
    `:root`-Blocks einfügt, fängt diesen Test. Ein Kommentar in `:root`, der das
    Pattern erklärt, ist erlaubt -- die Assertion matcht nur Hex außerhalb `:root`,
    nicht den Token-Literal-String.
    """
    css = (DEFAULT_STATIC_DIR / "app.css").read_text("utf-8")

    # :root-Block abschneiden -- dort darf das Pattern stehen (Token-Definitionen +
    # Kommentar).
    stripped = re.sub(r":root\s*\{[^}]*\}", "", css, flags=re.DOTALL)

    # Ausnahmen: dokumentiert + explizit erlaubt.
    EXEMPT_HEX = {
        "#FFF",  # QR-Code-Hintergrund in .qr-frame (P8.6-AD)
        # Space-Kategorien-Glyphen (P8.6 §3.3 explizit ausgenommen):
        "#5DA8F7", "#3A7DCB", "#1F4F8F",   # own-Verlauf + Border
        "#48C9B6", "#259C8C", "#156959",   # shared-Verlauf + Border
        "#9CA3B0", "#6F7686", "#3F4452",   # foreign-Verlauf + Border
    }

    # Nur `background:`- und `linear-gradient(...)`/`radial-gradient(...)`-Zeilen sind
    # „Flächen"; `color:`/`border:`/Outline/Box-Shadow sind keine. Wir picken die
    # `background`-Eigenschaft und alle gradient-funktionen, wo auch immer sie stehen.
    found: list[tuple[int, str, str]] = []
    for ln, line in enumerate(stripped.splitlines(), 1):
        # Nur Linien, die nach `background:` greifen ODER eine gradient()-Funktion
        # enthalten (Verläufe können auch auf anderen Properties liegen, z. B.
        # `background-image`).
        if "background" not in line and "gradient(" not in line:
            continue
        for m in re.finditer(r"#[0-9A-Fa-f]{3,8}\b", line):
            hexv = m.group(0).upper()
            if hexv in EXEMPT_HEX:
                continue
            found.append((ln, hexv, line.strip()))

    assert not found, (
        f"Roher Flächen-Hex außerhalb von :root gefunden: {len(found)} Vorkommen. "
        f"P8.6-AD verlangt für alle nicht-dokumentierten Stellen einen Token. "
        f"Erste Treffer:\n" + "\n".join(f"  app.css:{ln}  {hexv}  {ctx}"
                                        for ln, hexv, ctx in found[:5])
    )


def test_meta_panel_is_not_tinted_with_the_warning_colour():
    """P8.6-AB (Plan §8.2, F1): Wächter über die Beobachtung, dass das Meta-Panel vor
    Block F mit `rgba(229,169,60,.22)` getönt war -- denselben Kanälen wie `--warn:
    #E5A93C` bei 22 % Deckkraft (Befund 8). Die Information „Kopfdaten" wurde mit
    der Bedeutung „Warnung" verwechselt.

    Der Test prüft **gezielt** die `--panel-meta*`-Tokens: keiner von ihnen darf
    die Warn-Kanäle (229,169,60) enthalten. Andere Stellen, die mit `var(--warn)`
    ein warn-getöntes Element bauen (z. B. die `.list__readonly`/
    `.detail__badge-readonly`-Chips mit `rgba(229,169,60,.10)`), bleiben erlaubt
    -- sie sind genau dann legitim, wenn sie `var(--warn)` referenzieren.

    Vor Block F: `--panel-meta-line: rgba(229,169,60,.22)` -- illegitime Verwendung.
    Nach Block F: `--panel-meta-line: var(--line)` -- Standard-Haarlinie, Layer-Höhe
    trägt die Unterscheidung statt Farbton.
    """
    css = (DEFAULT_STATIC_DIR / "app.css").read_text("utf-8")

    # Finde die drei Meta-Tokens und prüfe jeden einzeln.
    meta_tokens = ("--panel-meta", "--panel-meta-head", "--panel-meta-line")
    bad: list[str] = []
    for name in meta_tokens:
        m = re.search(rf"{re.escape(name)}\s*:\s*([^;]+);", css)
        assert m, f"{name} sollte in :root definiert sein"
        value = m.group(1).strip()
        if "229,169,60" in value or "229 ,169 ,60" in value:
            bad.append(f"{name}: {value}")

    assert not bad, (
        f"Meta-Panel-Token(s) verwenden die --warn-Kanäle (229,169,60) -- "
        f"Befund 8 ist zurück. P8.6-AB: Kopfdaten-Trennung läuft über Layer-Höhe, "
        f"nicht Farbton. Betroffen: {bad}"
    )


# -- Phase 8.6 Plan 2 Block G Wächter (P8.6-X, P8.6-Y, P8.6-AF, P8.6-AL) ----------------

def test_shell_grid_is_240_480_1fr():
    """P8.6 Plan 2 Block G G1 (P8.6-X): das seit Phase 5 unveraenderte .shell-Raster
    wird bewusst verschoben (P8.6-O2-Ausloesung, N.7) -- von 240px 380px 1fr auf
    240px 480px 1fr. Die 1280-px-Media-Query muss die Aenderung mitziehen
    (64px 480px 1fr statt 64px 380px 1fr). Begruendung 480 statt 380: gemessen
    brauchen die Space-Zeilen ~433 px (Glyph + Name + bis zu drei Zaehler-Chips),
    380 reichte nicht.

    Wer das Raster zurueckdreht, faengt diesen Test. Prueft zwei Anker: die
    Default-Regel (Zeile mit "1fr" als dritter Spalte) und die 1280-px-Media-Query
    (zweite ".shell { ... }"-Deklaration in einer @media-Regel). Beide muessen
    "480px" enthalten, keine darf "380px" enthalten.
    """
    css = (DEFAULT_STATIC_DIR / "app.css").read_text("utf-8")

    # Default-Block: ".shell { display: grid; grid-template-columns: 240px 480px 1fr; ... }"
    default_match = re.search(r"\.shell\s*\{[^}]*grid-template-columns\s*:\s*([^;]+);", css)
    assert default_match is not None, (
        ".shell muss eine grid-template-columns-Deklaration enthalten "
        "(sonst waere der Block G-Gitterumbau rueckgaengig gemacht worden)."
    )
    default_cols = default_match.group(1).strip()
    assert "480px" in default_cols, (
        f".shell-Default-Block muss '480px' enthalten (Block G G1, P8.6-X, N.7). "
        f"Gefunden: '{default_cols}'."
    )
    assert "380px" not in default_cols, (
        f".shell-Default-Block darf '380px' NICHT mehr enthalten -- das war der "
        f"Phase-5-Stand. Block G G1 hat das auf 480px erweitert. "
        f"Gefunden: '{default_cols}'."
    )
    assert "1fr" in default_cols, (
        f".shell-Default-Block muss die dritte Spalte als '1fr' definieren "
        f"(Detail-Slot wächst mit dem Viewport). Gefunden: '{default_cols}'."
    )

    # 1280-px-Media-Query: sucht die @media-Regel und prueft die darin enthaltene
    # .shell-Deklaration. Pattern: "@media (max-width: 1280px) { ... .shell { ... } ... }"
    media_match = re.search(
        r"@media\s*\(max-width:\s*1280px\)\s*\{(.*?)\n\}", css, flags=re.DOTALL
    )
    assert media_match is not None, (
        "@media (max-width: 1280px) muss in app.css existieren "
        "(sonst waere der Breakpoint-Block geloescht worden)."
    )
    media_body = media_match.group(1)
    shell_in_media = re.search(r"\.shell\s*\{[^}]*grid-template-columns\s*:\s*([^;]+);", media_body)
    assert shell_in_media is not None, (
        ".shell muss INNERHALB der 1280-px-Media-Query eine grid-template-columns-"
        "Deklaration tragen (sonst waere der schmale Viewport kaputt)."
    )
    media_cols = shell_in_media.group(1).strip()
    assert "480px" in media_cols, (
        f".shell in @media (max-width: 1280px) muss '480px' enthalten -- Block G G1 "
        f"zieht die 480px-Breite in den schmalen Viewport mit. Gefunden: '{media_cols}'."
    )
    assert "380px" not in media_cols, (
        f".shell in @media (max-width: 1280px) darf '380px' NICHT enthalten. "
        f"Gefunden: '{media_cols}'."
    )


def test_overview_lives_in_the_list_slot():
    """P8.6 Plan 2 Block G G2 (P8.6-Y): die Uebersicht (Spaces + Zuletzt benutzt)
    zieht in den Listen-Slot (#list-overview in section.list), die Karte hat den
    Detail-Slot fuer sich allein (#overview-graph in section.detail). Editor ersetzt
    die Karte, ESC bringt sie zurueck (N.8).

    Prueft die Position der beiden Elemente in app.html -- byte-genau ueber String-
    Matching, billig und robust gegen CSS-Layout-Aenderungen. Wer eines der Elemente
    an die alte Stelle zurueckverschiebt, faengt diesen Test.

    Anker der beiden Elemente: das eroeffnende Tag von section.list bzw. section.detail
    muss VOR dem eroeffnenden Tag des Ziels liegen.
    """
    html = (DEFAULT_STATIC_DIR / "app.html").read_text("utf-8")

    # Eroeffnende Tags finden.
    list_open = re.search(r'<section\s+class="list"\s+id="list"\s*>', html)
    detail_open = re.search(r'<section\s+class="detail"\s+id="detail"\s*>', html)
    assert list_open is not None, '<section class="list" id="list"> fehlt im Markup'
    assert detail_open is not None, '<section class="detail" id="detail"> fehlt im Markup'

    # list-overview muss innerhalb von section.list stehen, NACH deren eroeffnendem Tag
    # und VOR deren schliessendem </section>. Das eroeffnende Tag von detail-overview
    # (vorhanden oder nicht) ist irrelevant.
    list_overview_open = re.search(r'<div\s+class="overview"\s+id="list-overview"', html)
    assert list_overview_open is not None, (
        '<div class="overview" id="list-overview"> fehlt im Markup (Plan §4.2 G2).'
    )
    # section.list schliesst VOR section.detail; das ist die strukturelle Garantie.
    assert list_open.start() < list_overview_open.start(), (
        "#list-overview muss INNERHALB section.list stehen -- "
        "eroeffnendes section.list-Tag muss VOR #list-overview kommen. "
        f"Positionen: section.list={list_open.start()}, "
        f"#list-overview={list_overview_open.start()}."
    )

    # overview-graph muss innerhalb section.detail stehen (V129-Bestaetigung: das Element
    # selbst wandert mit, nur sein Elternteil wechselt von .overview__col-right nach
    # .detail__graph).
    overview_graph_open = re.search(r'<div\s+class="overview__graph"\s+id="overview-graph"', html)
    assert overview_graph_open is not None, (
        '<div class="overview__graph" id="overview-graph"> fehlt im Markup.'
    )
    assert detail_open.start() < overview_graph_open.start(), (
        "#overview-graph muss INNERHALB section.detail stehen, NICHT mehr in #detail-overview "
        "(Plan §4.2 G2: die Karte hat den Detail-Slot allein). "
        f"Positionen: section.detail={detail_open.start()}, "
        f"#overview-graph={overview_graph_open.start()}."
    )

    # Negative Pruefung: das alte #detail-overview darf nicht mehr im Markup sein --
    # wurde in #list-overview umbenannt und in den Listen-Slot verschoben (G5).
    assert 'id="detail-overview"' not in html, (
        "#detail-overview darf nicht mehr im Markup vorkommen -- Block G G2 hat es zu "
        "#list-overview umbenannt (war der Wrapper um Spaces + Graph, jetzt sind die "
        "getrennt)."
    )


def test_detail_graph_has_a_definite_height_chain():
    """P8.6 Plan 2 Block G G2 §4.2.1 (V112-Waechter): die Hoehenkette, die nach dem
    Umzug der Karte in den Detail-Slot noetig ist, weil das bisherige Grid die
    definite Hoehe geliefert hat. Wer eine der beiden Stufen vergisst, baut den
    V112-Bug wieder ein (Karte schneidet unten ab).

    Stufe 1 -- .detail__graph { display: flex; flex-direction: column; flex: 1;
                                 min-height: 0; padding: ... }
    Stufe 2 -- .detail__graph .overview__graph { flex: 1; min-height: 0 }

    Prueft die Anwesenheit aller vier Eigenschaften pro Stufe. Reihenfolge der
    Properties ist egal; das CSS-Parsing-Tool versteht sie in jeder Reihenfolge.
    """
    css = (DEFAULT_STATIC_DIR / "app.css").read_text("utf-8")

    # Stufe 1: .detail__graph { ... } als Bloeckselektor (nicht compound mit .overview__graph).
    detail_graph_match = re.search(
        r"^\.detail__graph\s*\{([^}]*)\}", css, flags=re.MULTILINE
    )
    assert detail_graph_match is not None, (
        "app.css muss eine Regel `.detail__graph { ... }` enthalten "
        "(sonst hat Block G G2 die Hoehenkette nicht aufgebaut)."
    )
    stufe1_body = detail_graph_match.group(1)
    assert "flex: 1" in stufe1_body, (
        f".detail__graph braucht `flex: 1` -- sonst fuellt es den Detail-Slot nicht. "
        f"Block: {stufe1_body.strip()}"
    )
    assert "min-height: 0" in stufe1_body, (
        f".detail__graph braucht `min-height: 0` -- ohne das waechst die Flex-Basis "
        f"aus dem Inhalt, und die Karte schneidet oben ab. "
        f"Block: {stufe1_body.strip()}"
    )
    assert "flex-direction: column" in stufe1_body, (
        f".detail__graph braucht `flex-direction: column` -- sonst stapeln sich die "
        f"Kinder horizontal statt vertikal. Block: {stufe1_body.strip()}"
    )

    # Stufe 2: .detail__graph .overview__graph { ... } als Compound-Selektor.
    chain_match = re.search(
        r"\.detail__graph\s+\.overview__graph\s*\{([^}]*)\}", css
    )
    assert chain_match is not None, (
        "app.css braucht eine Regel `.detail__graph .overview__graph { ... }` -- "
        "die zweite Stufe der Hoehenkette. Ohne sie hat .overview__graph keine "
        "definite Hoehe, und das Canvas faellt auf seine Attribut-Hoehe zurueck "
        "(V112-Bug)."
    )
    stufe2_body = chain_match.group(1)
    assert "flex: 1" in stufe2_body, (
        f".detail__graph .overview__graph braucht `flex: 1` -- die Weitergabe der "
        f"Resthoehe an die Karte. Block: {stufe2_body.strip()}"
    )
    assert "min-height: 0" in stufe2_body, (
        f".detail__graph .overview__graph braucht `min-height: 0` -- damit die "
        f"flex-Basis nicht der Inhalt ist. Block: {stufe2_body.strip()}"
    )


def test_overview_grid_and_its_media_query_are_gone():
    """P8.6 Plan 2 Block G G6 (9b-Regressionswaechter): Block G raeumt das
    .overview-Grid und seine 1280-px-Media-Query ersatzlos ab. Befund 9b ist genau,
    dass die Media-Query die Karte unter 1280 px verkleinerte, weil die Grid-Spalten
    zusammenbrachen -- das Grid existiert nicht mehr, also kann die Ursache auch
    nicht zurueckkehren.

    Verbote:
      - Keine CSS-Regel enthaelt `grid-template-columns: 1fr 40%` (das war das
        .overview-Grid in C3, jetzt weg).
      - Keine CSS-Regel verwendet `.overview__col-left` (Wrapper-DIV aus C3,
        ersatzlos geloescht in G6).
      - Keine CSS-Regel verwendet `.overview__col-right` (dasselbe fuer die rechte
        Spalte).
      - Keine CSS-Regel verwendet `.overview__head-row` (head-row-Spanning-DIV,
        ersatzlos geloescht in G6).

    Wer spaeter eines der vier Artefakte zurueckbringt, faengt diesen Test.
    """
    css = (DEFAULT_STATIC_DIR / "app.css").read_text("utf-8")

    # Hinweis: `.overview__space-row` (Space-Zeile im Uebersichts-Inhalt) und
    # `.overview__header`, `.overview__spaces`, `.overview__recent` (Inhalte der
    # Uebersicht) bleiben erhalten -- das hier prueft NUR die geloeschten Grid-Wrapper.

    forbidden_classes = (
        ".overview__col-left",
        ".overview__col-right",
        ".overview__head-row",
    )
    for cls in forbidden_classes:
        # Suche nach dem Selektor in CSS-Regeln: ".overview__col-left" gefolgt von
        # beliebigem Text bis zur Klammer.
        pattern = re.escape(cls) + r"[^{]*\{"
        m = re.search(pattern, css)
        assert m is None, (
            f"{cls} darf in app.css nicht mehr vorkommen (Block G G6 hat das "
            f"Wrapper-DIV ersatzlos geloescht). Treffer bei Position {m.start()}: "
            f"'{m.group(0)}'."
        )

    # 1fr 40% war die Grid-Definition des .overview-Containers in Block C.
    # In G2 ist die Uebersicht ein einspaltiger Fluss -- diese Definition darf
    # nirgends mehr stehen.
    grid_pattern = re.compile(r"grid-template-columns\s*:\s*1fr\s+40%\s*;")
    m = grid_pattern.search(css)
    assert m is None, (
        f"`grid-template-columns: 1fr 40%` darf in app.css nicht mehr vorkommen "
        f"(Block G G6 hat das .overview-Grid ersatzlos geloescht). "
        f"Treffer bei Position {m.start()}: '{css[m.start():m.end()]}'. "
        f"Hinweis: 1fr 1fr (z.B. fuer .auth__codes) und 64px 480px 1fr (.shell "
        f"im Breakpoint) sind erlaubt und bleiben hiervon unberuehrt -- der Regex "
        f"matcht nur das exakte `1fr 40%`-Verhaeltnis."
    )
