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
    space_admin` (`app.js`), nicht diesem statischen Markup (P5-T, kein Templating).

    Block H H2 (Plan §5.2): die Knöpfe tragen jetzt zusätzlich ein Chevron-Icon
    (`<svg class="icon">...</svg>`); die Regex muss daher nested-Tags innerhalb des
    Buttons erlauben, nicht nur reinen Text. Capture-Gruppe wird auf den sichtbaren
    Text-Label-Teil eingeschränkt (erstes nicht-leeres Text-Stück vor dem ersten `<`)."""
    html = (DEFAULT_STATIC_DIR / "app.html").read_text("utf-8")
    # non-greedy `.*?` damit das inner svg erlaubt ist, aber </button> greift
    match = re.search(
        r'<button[^>]*id="account-manage-spaces"[^>]*>(.*?)</button>',
        html,
        flags=re.DOTALL,
    )
    assert match is not None, "Menüpunkt 'Spaces verwalten' fehlt"
    button_html = match.group(0)
    assert "disabled" not in button_html
    # Label-Text ist im ersten Text-Knoten vor dem ersten <svg> -- regex sucht "Spaces verwalten"
    assert re.search(r"Spaces verwalten", button_html), (
        "#account-manage-spaces muss 'Spaces verwalten' als Label tragen (P7 C3)."
    )
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


def test_rail_order_settings_and_logout_at_the_end():
    """P8.6 Block H H1 (Plan §5.1, N.9 + P8.6-AE): Reihenfolge im Rail ist wieder
        1. .rail__brand
        2. #home-button           ("Übersicht")
        3. #rail-tree             (Spaces + "Alle Items")
        4. #account-button        ("Einstellungen")   <-- ZURÜCK in .rail__account
        5. #logout-button         ("Abmelden")        <-- letztes Element im Rail

    NAMEN + UMKEHR -- beide Richtungen sind gelockt und datiert (P8.6-I-Mechanik wörtlich
    übernommen):

    • 2026-09-09, Block C C1, N3-Lesart b: Reihenfolge war .rail__brand / #home-button /
      #account-button / #rail-tree / #logout-button (Einstellungen oben, Abmelden ans Rail-
      Ende). Begründung damals: "Abmelden ist die seltenste und teuerste Aktion -- ein
      wörtlicher Tausch würde sie an die prominenteste Stelle setzen." Der Test hieß
      `test_rail_order_settings_before_tree_logout_last` und prüfte
      pos_account < pos_tree, pos_tree < pos_logout, pos_home < pos_account.

    • 2026-09-13, Plan 2 §5.1, Nikinger-Entscheidung N.9: kehrt das um, "Abmelden bleibt
      weiterhin der äußerste Knopf" -- beide Knöpfe unten, Reihenfolge
      Einstellungen → Abmelden. Hintergrund: das Layout ist anders als bei C1 (kein
      einsamer Knopf oben zwischen Übersicht und Baum), die ursprüngliche Begründung
      verfängt nicht mehr.

    Wer die Reihenfolge ein drittes Mal umstellt (z. B. Einstellungen wieder oben, oder
    Abmelden vor Einstellungen), fällt hier auf statt erst in der nächsten Sichtprüfung.
    Test über die Reihenfolge der Tag-Positionen im HTML-String -- billig und robust gegen
    CSS-Layout-Änderungen.
    """
    html = (DEFAULT_STATIC_DIR / "app.html").read_text("utf-8")

    def _pos(tag_id: str) -> int:
        m = re.search(rf'id="{re.escape(tag_id)}"', html)
        assert m is not None, f"#{tag_id} fehlt im Markup"
        return m.start()

    pos_home = _pos("home-button")
    pos_tree = _pos("rail-tree")
    pos_account = _pos("account-button")
    pos_logout = _pos("logout-button")

    assert pos_home < pos_tree, (
        f"#rail-tree muss NACH #home-button stehen (unverändert seit Step 7b). "
        f"Positionen: home={pos_home}, tree={pos_tree}."
    )
    assert pos_tree < pos_account, (
        f"#account-button (Einstellungen) muss NACH #rail-tree stehen -- das ist der Kern "
        f"von Block H H1 (Plan §5.1, N.9 + P8.6-AE: Einstellungen zurück in .rail__account). "
        f"Positionen: tree={pos_tree}, account={pos_account}."
    )
    assert pos_account < pos_logout, (
        f"#logout-button (Abmelden) muss NACH #account-button stehen -- die Reihenfolge in "
        f".rail__account ist Einstellungen → Abmelden (N.9 wörtlich: 'Abmelden bleibt "
        f"weiterhin der äußerste Knopf'). "
        f"Positionen: account={pos_account}, logout={pos_logout}."
    )
    assert pos_logout == html.rfind('id="logout-button"'), (
        f"#logout-button muss das letzte Element im Rail sein -- .rail__account ist das "
        f"Rail-Ende (margin-top: auto), und Block H H1 verlangt 'Abmelden als äußerster "
        f"Knopf' (N.9). "
        f"Positionen: logout={pos_logout}, html_len={len(html)}."
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
    """P8.6 Plan 2 Block G G1 (P8.6-X) und Block G-R G-R.1: das seit Phase 5 unveraenderte
    .shell-Raster wird bewusst verschoben (P8.6-O2-Ausloesung, N.7) -- von 240px 380px 1fr
    auf 240px 480px 1fr. Phase 8.6 Block G-R hat den Breakpoint von 1280 px auf 1200 px
    verschoben (Nikinger-Vorgabe 2026-09-14: Rail bleibt 240 in beiden Breakpoints) und
    fuehrt eine zweite Stufe bei 1024 px ein, die Liste + Karte vertikal stapelt.

    Wer das Raster zurueckdreht, faengt diesen Test. Prueft drei Anker: die Default-Regel
    (240/480/1fr), die 1200-px-Media-Query (240/380/1fr) und die 1024-px-Media-Query
    (240/1fr mit Stapel-Logik via grid-row).
    """
    css = (DEFAULT_STATIC_DIR / "app.css").read_text("utf-8")

    # Anker 1 -- Default-Block: ".shell { display: grid; grid-template-columns: 240px 480px 1fr; ... }"
    default_match = re.search(r"\.shell\s*\{[^}]*grid-template-columns\s*:\s*([^;]+);", css)
    assert default_match is not None, (
        ".shell muss eine grid-template-columns-Deklaration enthalten "
        "(sonst waere der Block G-Gitterumbau rueckgaengig gemacht worden)."
    )
    default_cols = default_match.group(1).strip()
    assert "240px" in default_cols, (
        f".shell-Default-Block muss '240px' enthalten (Block G G1, P8.6-X, N.7). "
        f"Gefunden: '{default_cols}'."
    )
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

    # Anker 2 -- 1200-px-Media-Query: Rail bleibt 240, Liste schrumpft auf 380, Detail
    # bleibt 1fr (Block G-R G-R.1). Pattern: "@media (max-width: 1200px) { ... .shell { ... } ... }"
    media_1200 = re.search(
        r"@media\s*\(max-width:\s*1200px\)\s*\{(.*?)\n\}", css, flags=re.DOTALL
    )
    assert media_1200 is not None, (
        "@media (max-width: 1200px) muss in app.css existieren "
        "(Block G-R G-R.1 hat den Breakpoint von 1280 auf 1200 verschoben)."
    )
    media_1200_body = media_1200.group(1)
    shell_in_1200 = re.search(
        r"\.shell\s*\{[^}]*grid-template-columns\s*:\s*([^;]+);", media_1200_body
    )
    assert shell_in_1200 is not None, (
        ".shell muss INNERHALB der 1200-px-Media-Query eine grid-template-columns-"
        "Deklaration tragen."
    )
    media_1200_cols = shell_in_1200.group(1).strip()
    assert "240px" in media_1200_cols, (
        f".shell in @media (max-width: 1200px) muss '240px' als erste Spalte tragen -- "
        f"Block G-R G-R.1 haelt die Rail bewusst bei 240 px, NICHT auf 64 px kollabiert. "
        f"Gefunden: '{media_1200_cols}'."
    )
    assert "380px" in media_1200_cols, (
        f".shell in @media (max-width: 1200px) muss '380px' als zweite Spalte tragen -- "
        f"Block G-R G-R.1 schrumpft die Liste von 480 auf 380 px "
        f"(Item-Titel + Meta + Move/Share-Buttons passen). Gefunden: '{media_1200_cols}'."
    )
    assert "64px" not in media_1200_cols, (
        f".shell in @media (max-width: 1200px) darf NICHT '64px' als erste Spalte haben -- "
        f"Block G-R G-R.1 verbietet die Rail-Kollaps-Logik des 1280-er-Blocks. "
        f"Gefunden: '{media_1200_cols}'."
    )

    # Anker 3 -- 1024-px-Media-Query: Rail 240 + rechte Spalte 1fr, EINE Zeile (Block H-R-3
    # H-R.6 -- Umkehr von G-R.1s Stapel-Logik, siehe test_1024_breakpoint_has_single_row_no_map
    # fuer die volle Herleitung).
    media_1024 = re.search(
        r"@media\s*\(max-width:\s*1024px\)\s*\{(.*?)\n\}", css, flags=re.DOTALL
    )
    assert media_1024 is not None, (
        "@media (max-width: 1024px) muss in app.css existieren."
    )
    media_1024_body = media_1024.group(1)
    shell_in_1024 = re.search(
        r"\.shell\s*\{(.*?)\}", media_1024_body, flags=re.DOTALL
    )
    assert shell_in_1024 is not None, (
        ".shell muss INNERHALB der 1024-px-Media-Query eine Deklaration tragen."
    )
    media_1024_shell = shell_in_1024.group(1)
    # grid-template-columns muss "240px" und "1fr" enthalten (zwei Spalten)
    cols_1024_match = re.search(
        r"grid-template-columns\s*:\s*([^;]+);", media_1024_shell
    )
    assert cols_1024_match is not None, (
        ".shell in 1024-px-Media-Query braucht grid-template-columns."
    )
    cols_1024 = cols_1024_match.group(1).strip()
    assert "240px" in cols_1024, (
        f".shell in 1024-px-Media-Query muss '240px' enthalten (Rail bleibt 240). "
        f"Gefunden: '{cols_1024}'."
    )
    assert "1fr" in cols_1024, (
        f".shell in 1024-px-Media-Query muss '1fr' enthalten (rechte Spalte flexibel). "
        f"Gefunden: '{cols_1024}'."
    )
    # grid-template-rows muss "1fr" genau EINMAL haben -- eine Zeile (H-R.6, kein Stapel mehr).
    rows_1024_match = re.search(
        r"grid-template-rows\s*:\s*([^;]+);", media_1024_shell
    )
    assert rows_1024_match is not None, (
        ".shell in 1024-px-Media-Query braucht grid-template-rows (H-R.6)."
    )
    rows_1024 = rows_1024_match.group(1).strip()
    assert rows_1024.count("1fr") == 1, (
        f".shell in 1024-px-Media-Query braucht GENAU EINE '1fr'-Zeile (H-R.6: kein "
        f"Stapel mehr, Karte ist weg). Gefunden: '{rows_1024}'."
    )

    # Negative Regression: der alte 1280-er Breakpoint-Block ist weg. Block G-R G-R.1 hat
    # ihn auf 1200 verschoben; wer ihn als Geist zurueckbringt, hat den alten Rail-Kollaps
    # wieder drin.
    assert not re.search(r"@media\s*\(max-width:\s*1280px\)", css), (
        "@media (max-width: 1280px) darf nicht mehr in app.css vorkommen "
        "(Block G-R G-R.1 hat den Breakpoint von 1280 auf 1200 verschoben -- der alte "
        "Block kollabierte die Rail auf 64 px, was bei 1200 px Sichtung der Nikinger als "
        "'Navigationszeile kracht zusammen' beschrieb)."
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


# -- Phase 8.6 Plan 2 Block G-R Wächter (G-R.1, G-R.2, G-R.3, G-R.4) -----------------------

def test_1200_breakpoint_keeps_rail_at_240():
    """P8.6 Block G-R G-R.1 (Nikinger-Sichtung 2026-09-14): bei ≤1200 px bleibt die Rail
    bewusst 240 px breit. Der alte 1280-er Block kollabierte die Rail auf 64 px (Icons
    only, Texte weg) -- Nikinger-Beobachtung im 1200-px-Screenshot: 'Navigationszeile
    kracht zusammen'.

    Wer den Rail-Kollaps wieder einbaut (`.rail__label, .rail__brand, .tree__group,
    .tree__count, .tree__badge { display: none }`), fängt diesen Test. Geprüft wird: in
    der 1200-px-Media-Query darf KEINE `.rail__label { display: none }`-Regel stehen.
    """
    css = (DEFAULT_STATIC_DIR / "app.css").read_text("utf-8")

    media_1200 = re.search(
        r"@media\s*\(max-width:\s*1200px\)\s*\{(.*?)\n\}", css, flags=re.DOTALL
    )
    assert media_1200 is not None, (
        "@media (max-width: 1200px) muss in app.css existieren "
        "(sonst waere Block G-R G-R.1 rueckgaengig gemacht worden)."
    )
    media_1200_body = media_1200.group(1)

    # Rail-Texte duerfen NICHT ausgeblendet werden -- das war die Kollaps-Logik des 1280-er
    # Blocks, die bei 1200 px zur Meldung 'Navigationszeile kracht zusammen' gefuehrt hat.
    for forbidden in (
        r"\.rail__label[^{]*\{\s*display\s*:\s*none",
        r"\.rail__brand[^{]*\{\s*display\s*:\s*none",
        r"\.tree__group[^{]*\{\s*display\s*:\s*none",
        r"\.tree__count[^{]*\{\s*display\s*:\s*none",
        r"\.tree__badge[^{]*\{\s*display\s*:\s*none",
    ):
        m = re.search(forbidden, media_1200_body)
        assert m is None, (
            f"In @media (max-width: 1200px) darf Rail-Text nicht via 'display: none' "
            f"ausgeblendet werden (Block G-R G-R.1 -- Rail bleibt 240 px, Texte sichtbar). "
            f"Verbotenes Pattern getroffen bei Position {m.start() if m else 'n/a'}: "
            f"'{m.group(0) if m else ''}'."
        )

    # Zentrierung der Icons -- das war der alte Hinweis darauf, dass die Rail kollabiert.
    # Bei 240-px-Rail waere Icon-Zentrierung sichtbar falsch (Texte + Icons linksbuendig).
    m = re.search(r"\.rail__home[^{]*\{\s*justify-content\s*:\s*center", media_1200_body)
    assert m is None, (
        f"In @media (max-width: 1200px) darf '.rail__home { justify-content: center }' "
        f"nicht stehen (Rail bleibt 240 px, linksbuendig wie im Default). "
        f"Treffer: '{m.group(0) if m else ''}'."
    )


def test_1024_breakpoint_has_single_row_no_map():
    """P8.6 Block H-R-3, Lock H-R.6 (Befund 2, Nikinger-Sichtung 2026-09-15, Umkehr von
    G-R.1, bestaetigt 2026-09-17: 'bei 'ohne Map' Entscheidung bleiben und umsetzen').

    G-R.1 (2026-09-14) hatte bei <=1024 px Liste + Karte vertikal gestapelt (zwei Zeilen,
    Rail spannt beide via `grid-row: 1 / span 2`, `.detail` explizit in Zeile 2). Die naechste
    Sichtung (2026-09-15) kehrt das um: bei 1024 px soll es KEINE Karte mehr geben, Rail +
    Liste in einer Zeile. Ersetzt sowohl diesen Test (vormals
    `test_1024_breakpoint_stacks_list_over_detail`) als auch das eigenstaendige
    `test_1024_no_overlap_in_css` (H-R.4-L) -- beide prueften exakt dieselben jetzt toten
    G-R.1-Grid-Properties (`grid-template-rows: 1fr 1fr` / `.rail { grid-row: 1 / span 2 }` /
    `.detail { grid-column: 2 }`); nach dem Wegfall der Stapel-Logik waeren sie reine
    Duplikate geworden. `_konsequenz aus dem stapel-wegfall_`: ein Overlap zwischen Karte und
    Rail/Liste kann nicht mehr auftreten, wenn die Karte nie sichtbar ist -- H-R.4-Ls Sorge
    ist damit strukturell erledigt, kein eigener Test noetig.
    """
    css = (DEFAULT_STATIC_DIR / "app.css").read_text("utf-8")

    media_1024 = re.search(
        r"@media\s*\(max-width:\s*1024px\)\s*\{(.*?)\n\}", css, flags=re.DOTALL
    )
    assert media_1024 is not None, (
        "@media (max-width: 1024px) muss in app.css existieren."
    )
    media_1024_body = media_1024.group(1)
    media_1024_body_nc = re.sub(r"/\*.*?\*/", "", media_1024_body, flags=re.DOTALL)

    # 1. .shell traegt eine EINZIGE Zeile, nicht mehr zwei gleich hohe.
    shell_match = re.search(r"\.shell\s*\{([^}]*)\}", media_1024_body_nc)
    assert shell_match is not None, (
        ".shell braucht eine Regel in @media (max-width: 1024px)."
    )
    shell_body = shell_match.group(1)
    assert "grid-template-rows: 1fr;" in shell_body or re.search(
        r"grid-template-rows:\s*1fr\s*;", shell_body
    ), (
        f".shell in @media (max-width: 1024px) muss 'grid-template-rows: 1fr' tragen "
        f"(H-R.6: eine Zeile, kein Stapel mehr). Block: {shell_body.strip()}"
    )

    # 2. .rail spannt nicht mehr zwei Zeilen -- eine Zeile reicht, es gibt nur noch eine.
    rail_match = re.search(r"\.rail\s*\{([^}]*)\}", media_1024_body_nc)
    assert rail_match is not None, (
        ".rail braucht eine Regel in @media (max-width: 1024px)."
    )
    rail_body = rail_match.group(1)
    assert "grid-row: 1;" in rail_body or re.search(r"grid-row:\s*1\s*;", rail_body), (
        f".rail in @media (max-width: 1024px) muss 'grid-row: 1' tragen (H-R.6: keine "
        f"zweite Zeile mehr zum Spannen). Block: {rail_body.strip()}"
    )

    # 3. .detail__graph (die Karte) ist unabhaengig vom JS-`hidden`-Attribut ausgeblendet.
    graph_match = re.search(r"\.detail__graph\s*\{([^}]*)\}", media_1024_body_nc)
    assert graph_match is not None, (
        ".detail__graph braucht eine Regel in @media (max-width: 1024px) (H-R.6: keine "
        "Karte bei <=1024 px)."
    )
    assert "display: none" in graph_match.group(1), (
        f".detail__graph in @media (max-width: 1024px) muss 'display: none' tragen. "
        f"Block: {graph_match.group(1).strip()}"
    )

    # 4. Negativ: G-R.1s Stapel-Marker sind vollstaendig weg.
    for forbidden, label in (
        (r"grid-template-rows:\s*1fr\s+1fr", "grid-template-rows: 1fr 1fr (G-R.1-Stapel)"),
        (r"span\s*2", "grid-row: ... span 2 (G-R.1-Rail-Spannung)"),
        (r"\.detail(?![a-zA-Z_-])\s*\{[^}]*grid-column", ".detail { grid-column: ... } (G-R.1-Platzierung)"),
    ):
        m = re.search(forbidden, media_1024_body_nc)
        assert m is None, (
            f"G-R.1-Erbe '{label}' muss aus @media (max-width: 1024px) weg sein (H-R.6: "
            f"sauberer Schnitt, kein Override-Layer). Treffer: '{m.group(0) if m else ''}'."
        )


def test_1024_editor_fullview_hides_rail_and_list():
    """P8.6 Block H-R-3, Lock H-R.7 (Befund 3, Nikinger-Sichtung 2026-09-15): bei <=1024 px
    UND offenem Detail-/Editor-Slot (`dataset.view === "detail"`) fuellt der Editor den
    kompletten Viewport -- Rail und Liste sind komplett weg, nicht nur die Karte (die ist ab
    H-R.6 sowieso immer weg bei 1024 px).

    ESC/× brauchen keinen neuen JS-Handler: `closeEditor() -> clearDetail() ->
    showOverviewPane()` setzt `dataset.view` bereits seit Block G auf "list" zurueck
    (editor.js:58/82) -- das war nur bislang ohne CSS-Konsumenten. Kein `app.js`/`editor.js`-
    Touch in diesem Block.
    """
    css = (DEFAULT_STATIC_DIR / "app.css").read_text("utf-8")

    media_1024 = re.search(
        r"@media\s*\(max-width:\s*1024px\)\s*\{(.*?)\n\}", css, flags=re.DOTALL
    )
    assert media_1024 is not None
    body = re.sub(r"/\*.*?\*/", "", media_1024.group(1), flags=re.DOTALL)

    detail_view_match = re.search(
        r'\.shell\[data-view="detail"\]\s*\{([^}]*)\}', body
    )
    assert detail_view_match is not None, (
        '@media (max-width: 1024px) braucht eine .shell[data-view="detail"]-Regel '
        "(H-R.7: Editor-Fullview -- eine Spalte statt zwei)."
    )
    assert "grid-template-columns: 1fr" in detail_view_match.group(1), (
        f'.shell[data-view="detail"] in @media (max-width: 1024px) muss '
        f"'grid-template-columns: 1fr' tragen (H-R.7: volle Breite fuer .detail). "
        f"Block: {detail_view_match.group(1).strip()}"
    )

    rail_hidden_match = re.search(
        r'\.shell\[data-view="detail"\]\s+\.rail\s*\{([^}]*)\}', body
    )
    assert rail_hidden_match is not None, (
        '@media (max-width: 1024px) braucht .shell[data-view="detail"] .rail '
        "(H-R.7: Rail komplett weg im Editor-Fullview)."
    )
    assert "display: none" in rail_hidden_match.group(1), (
        f'.shell[data-view="detail"] .rail in @media (max-width: 1024px) muss '
        f"'display: none' tragen. Block: {rail_hidden_match.group(1).strip()}"
    )


def test_editor_open_hides_list_at_all_viewports():
    """P8.6 Block H-R-3, Lock H-R.8 (Befund 1, Lesart b -- Nikinger-Entscheidung
    2026-09-17, Lesart a verworfen: ihre Praemisse 'beide Rail-Knoepfe fuehren zur selben
    Aktion' [V110] ist seit Block G / Plan 2 §4.3 ueberholt, `#home-button` und
    `.tree__scope` sind seither getrennte, nicht-redundante Aktionen -- app.js:97-100,
    tree.js:252 `renderScopeRow()`).

    Der eigentliche Befund war der Listen-Slot NEBEN einem offenen Editor, nicht die
    Rail-Knoepfe. Fix: `.shell[data-view="detail"] .list { display: none }` OHNE
    Media-Query-Wrapper -- gilt bei 1440 px genauso wie bei 1024 px. Rail bleibt bei
    Desktop-Breiten sichtbar (nur bei <=1024 px blendet H-R.7 sie zusaetzlich aus).
    """
    css = (DEFAULT_STATIC_DIR / "app.css").read_text("utf-8")

    # Muss AUSSERHALB jeder @media-Regel stehen -- am Zeilenanfang, keine Einrueckung.
    m = re.search(
        r'^\.shell\[data-view="detail"\]\s*\{([^}]*)\}', css, flags=re.MULTILINE
    )
    assert m is not None, (
        'app.css braucht eine Top-Level-Regel .shell[data-view="detail"] { ... } '
        "ausserhalb jeder @media-Query (H-R.8 Lesart b: gilt bei allen Breiten)."
    )
    assert "grid-template-columns: 240px 1fr" in m.group(1), (
        f'.shell[data-view="detail"] muss "grid-template-columns: 240px 1fr" tragen -- '
        f"die Liste faellt weg, die Karte/Editor-Spalte nimmt den freien Platz. "
        f"Block: {m.group(1).strip()}"
    )

    list_hidden = re.search(
        r'^\.shell\[data-view="detail"\]\s+\.list\s*\{([^}]*)\}', css, flags=re.MULTILINE
    )
    assert list_hidden is not None, (
        'app.css braucht eine Top-Level-Regel .shell[data-view="detail"] .list '
        "{ display: none } ausserhalb jeder @media-Query."
    )
    assert "display: none" in list_hidden.group(1), (
        f'.shell[data-view="detail"] .list muss "display: none" tragen. '
        f"Block: {list_hidden.group(1).strip()}"
    )

    # Negativ: Lesart a (Rail-Knopf loeschen) wurde NICHT umgesetzt -- beide Knoepfe bleiben,
    # sie sind seit Block G unterschiedliche Aktionen, keine Redundanz mehr.
    html = (DEFAULT_STATIC_DIR / "app.html").read_text("utf-8")
    assert 'id="home-button"' in html, (
        "#home-button darf nicht verschwinden -- H-R.8 Lesart a wurde verworfen "
        "(V110-Praemisse ueberholt seit Block G)."
    )


def test_detail_uses_the_oled_black_background():
    """P8.6 Block H-R H-R.1 (Nikinger-Sichtung 2026-09-14): OLED-BLACK fuer die drei
    Slots. Block G-R G-R.2 hatte .detail auf --bg (#0B0D10) gezogen, um den schwarzen
    Ring rund um die Karte wegzubekommen. H-R.1 (N.13) geht einen Schritt weiter:
    alle drei Slots -- .rail, .list, .detail -- auf --bg-void (#000); die Karte
    (--surface) bleibt Layer 3 und schwebt sichtbar auf dem schwarzen Slot.

    NAMEN + UMKEHR -- beide Richtungen sind gelockt und datiert (P8.6-I-Mechanik):

    • 2026-09-14, Block G-R G-R.2: .detail background = var(--bg), drei sichtbare
      Toene (--bg / --bg-void / --surface) auf zwei reduziert. Begrundung: schwarzer
      Ring rund um die Karte. Der Test hiess
      `test_detail_uses_the_column_background_not_void` und pruefte
      `var(--bg) in detail_body`, `var(--bg-void) not in detail_body`.

    • 2026-09-14, Block H-R H-R.1, Nikinger-Entscheidung N.13: OLED-BLACK -- alle
      drei Slots auf --bg-void. Hintergrund: "echtes OLED-BLACK" maximiert den
      Kontrast zur Karte (--surface), die Karte "schwebt" sichtbar.

    Wer den Hintergrund herausnimmt oder auf --bg zurueckdreht, faengt diesen Test --
    N.13 ist eine Layer-Architektur-Revision, kein UI-Polish, und ein stiller
    Refactor zurueck auf --bg bricht sie ohne explizite Aufhebung.
    """
    css = (DEFAULT_STATIC_DIR / "app.css").read_text("utf-8")

    detail_body = _block_body(css, ".detail")

    assert "background" in detail_body, (
        f".detail braucht eine background-Deklaration (H-R.1-L). "
        f"Block: {detail_body.strip()}"
    )
    assert "var(--bg-void)" in detail_body, (
        f".detail muss 'var(--bg-void)' als Hintergrund tragen (H-R.1-L N.13 "
        f"OLED-BLACK). Gefunden: '{detail_body.strip()}'. Vor H-R.1 stand hier "
        f"'var(--bg)' (Block G-R G-R.2)."
    )
    assert "var(--bg)" not in detail_body, (
        f".detail darf 'var(--bg)' NICHT als Hintergrund tragen (H-R.1-L N.13: "
        f"das waere der fruehere G-R.2-Zustand und bricht OLED-BLACK). "
        f"Block: {detail_body.strip()}"
    )


def test_editor_head_is_sticky_with_the_list_head_background():
    """P8.6 Block G-R G-R.3 (Nikinger-Sichtung 2026-09-14): der Editor-Kopf verhaelt
    sich jetzt wie der List-Kopf -- sticky bei Scroll, gleicher Hintergrund (--surface-
    raised), gleiche Trennlinie (border-bottom 1px solid var(--line)).

    Wer die sticky-Position oder den Hintergrund entfernt, faengt diesen Test -- der
    Editor-Kopf scrollt dann mit dem Body-Inhalt, und der visuelle Unterschied zwischen
    den beiden Spalten-Koepfen kehrt zurueck.
    """
    css = (DEFAULT_STATIC_DIR / "app.css").read_text("utf-8")

    editor_head_match = re.search(r"\.editor__head\s*\{([^}]*)\}", css)
    assert editor_head_match is not None, (
        "app.css muss eine Regel `.editor__head { ... }` enthalten."
    )
    head_body = editor_head_match.group(1)

    assert "position: sticky" in head_body, (
        f".editor__head braucht 'position: sticky' (Block G-R G-R.3 -- Pendant zu "
        f".list__head). Block: {head_body.strip()}"
    )
    assert "top: 0" in head_body, (
        f".editor__head braucht 'top: 0' -- sticky am oberen Rand des Detail-Slots. "
        f"Block: {head_body.strip()}"
    )
    assert "var(--surface-raised)" in head_body, (
        f".editor__head muss 'var(--surface-raised)' als Hintergrund tragen -- "
        f"identisch zu .list__head, ein Layer im UI-Vokabular. "
        f"Block: {head_body.strip()}"
    )
    assert "border-bottom" in head_body, (
        f".editor__head braucht eine border-bottom-Trennlinie (1 px solid var(--line)) "
        f"-- identisch zu .list__head. Block: {head_body.strip()}"
    )
    assert "z-index: 1" in head_body, (
        f".editor__head braucht 'z-index: 1' -- hebt den sticky-Kopf ueber den Body-Inhalt, "
        f"ohne mit Editor-/Overlay-Stacks (hoehere z-indizes) zu kollidieren. "
        f"Block: {head_body.strip()}"
    )


def test_panel_head_height_matches_a_list_row():
    """P8.6 Block G-R G-R.3 (Nikinger-Vorgabe 2026-09-14): 'ziemlich genau so gross wie
    eine item Zeile'. Item-Row-Hoehe: padding 8 + Content ~25 + padding 8 = ~41 px.
    Panel-Header nach G-R.3: padding 11 + Content ~19 + padding 11 = ~41 px.

    Wer den Panel-Header wieder auf 6 px padding vertikal zurueckdreht, faengt diesen
    Test -- die 'buendig'-Vorgabe zwischen YAML-Kopfzeile und Item-Zeile waere weg.
    """
    css = (DEFAULT_STATIC_DIR / "app.css").read_text("utf-8")

    panel_head_match = re.search(r"\.panel__head\s*\{([^}]*)\}", css)
    assert panel_head_match is not None, (
        "app.css muss eine Regel `.panel__head { ... }` enthalten."
    )
    panel_body = panel_head_match.group(1)

    padding_match = re.search(r"padding\s*:\s*([^;]+);", panel_body)
    assert padding_match is not None, (
        f".panel__head braucht eine padding-Deklaration. Block: {panel_body.strip()}"
    )
    padding_value = padding_match.group(1).strip()

    # Erste Zahl im padding-Wert muss 11 px sein (vertikales padding oben).
    # Format-Erlaubnis: "11px", "11px 24px", "11px 24px 11px", "11px 24px 11px 24px".
    parts = padding_value.split()
    assert parts, (
        f".panel__head padding-Wert nicht parsbar: '{padding_value}'"
    )
    top_padding = parts[0]
    # Akzeptiere sowohl '11px' als auch '11' (manche Autoren lassen die Einheit weg bei 0).
    assert top_padding in ("11px", "11"), (
        f".panel__head padding-top muss 11 px sein (Block G-R G-R.3 -- Item-Row-Hoehe "
        f"~41 px = 11 + Content + 11). Gefunden: '{top_padding}' (Wert: '{padding_value}')."
    )


# --- Phase 8.6 Block H-R (Plan: docs/concepts/phase8_6_ui_polish_block_h_r_plan.md) ----
# Sechs neue Wächter für H-R.1 (OLED-BLACK für die drei Slots) und H-R.2 (account-nav-Akzent-Farbe).
# H-R.3/.4/.5 (Editor-YAML-Bündigkeit + 1024-er) sind CDP-Probe-Schritte — sie werden im
# Self-Check gemessen, nicht in statischen Tests (siehe Plan §5 / §11).


def _block_body(css: str, selector: str) -> str:
    """Liefert den Body des nächsten `{ ... }`-Blocks hinter dem Selector.

    Drei Fixes ggü. der ersten H-R.0-Fassung:
      1. `^`-Anker + `re.MULTILINE`: `body` matcht nur das Top-Level-`body`-Element
         (Z. 147), nicht `html, body { height: 100%; ... }` (Z. 142) oder
         `.rail, .list, .detail { ... }` (Z. 368, dort beginnt `.rail` am
         Zeilenanfang, aber das Komma zwischen den Selektoren verhindert das Match
         des `\s*{`-Patterns).
      2. Kommentare werden aus dem Body entfernt (`/* ... */`), weil Phase 8.6
         ausführliche Block-Kommentare trägt, die Code-Beispiele wie `var(--accent)`
         oder `linear-gradient` enthalten — eine Suche nach CSS-Properties im
         rohen Body würde diese Beispieltexte fälschlich matchen.
      3. `[^}]*` body ist ausreichend — kein Block hat verschachtelte Klammern in
         den H-R-relevanten Selektoren (Top-Level-Regeln haben alle flache Bodies).
    """
    m = re.search(rf"^{re.escape(selector)}\s*\{{([^}}]*)\}}", css, flags=re.MULTILINE)
    assert m is not None, (
        f"{selector} sollte in app.css einen Top-Level-Block haben "
        f"(am Zeilenanfang, gefolgt von `{{ ... }}`)."
    )
    body = m.group(1)
    # CSS-Kommentare strippen, sonst matcht eine Property-Suche Beispieltexte.
    body = re.sub(r"/\*.*?\*/", "", body, flags=re.DOTALL)
    return body


def test_three_slots_use_oled_black():
    """H-R.1-L (Plan §6): body, .rail, .list, .detail haben `background: var(--bg-void)`.
    .shell hat keinen eigenen Background — erbt von body. Vor H-R.1 waren .list/.detail
    auf `--bg` (#0B0D10), .rail hatte einen linear-Gradient. Nach H-R.1 sind alle drei
    Slots echtes Schwarz (N.13).

    Wer nach H-R.1 wieder einen der drei Slots auf `--bg` oder einen anderen Ton dreht,
    fängt diesen Test. Ein Refactor zurück auf `--bg` ohne explizite Aufhebung von N.13
    ist ein stiller Layer-Architektur-Bruch und wird hier geblockt.
    """
    css = (DEFAULT_STATIC_DIR / "app.css").read_text("utf-8")

    for sel in ("body", ".rail", ".list", ".detail"):
        body = _block_body(css, sel)
        m = re.search(r"background\s*:\s*([^;]+);", body)
        assert m is not None, (
            f"{sel} braucht eine background-Deklaration (H-R.1-L). Block: {body.strip()}"
        )
        value = m.group(1).strip()
        assert value == "var(--bg-void)", (
            f"{sel} background muss var(--bg-void) sein (H-R.1 OLED-BLACK). "
            f"Gefunden: '{value}'. Vor H-R.1 stand hier `--bg` oder ein linear-gradient."
        )

    # .shell hat per Definition keinen eigenen Background -- erbt von body.
    # Wer hier einen `background`-Eintrag hinzufügt, hat den Body-Erb-Mechanismus
    # gebrochen; der Test failt dann sichtbar mit der Begründung.
    shell_body = _block_body(css, ".shell")
    assert "background" not in shell_body, (
        f".shell darf KEINEN eigenen background haben (H-R.1-L: erbt von body, "
        f"body = --bg-void). Block: {shell_body.strip()}"
    )


def test_rail_has_no_gradient_anymore():
    """H-R.1-L (Plan §1, N.13): `.rail` hat keinen `linear-gradient(...)`-Hintergrund
    mehr. Vor H-R.1: `linear-gradient(180deg, var(--rail-top), var(--bg))` für den
    "Wortmarke oben etwas heller"-Look. Nach H-R.1: flaches `--bg-void`. Der Effekt
    der alten Sonderregel war auf schwarzem Grund sinnlos (kein erkennbarer
    Helligkeitsverlauf von #0E1116 zu #000).

    `--rail-top` bleibt im `:root` definiert (funktionslos), das prüft ein separater
    Test (`test_rail_top_token_still_in_root` -- bewusst NICHT hier, weil das ein
    Doku-Thema ist, kein UI-Verhalten).
    """
    css = (DEFAULT_STATIC_DIR / "app.css").read_text("utf-8")
    rail_body = _block_body(css, ".rail")
    assert "linear-gradient" not in rail_body, (
        f".rail darf keinen linear-gradient mehr enthalten (H-R.1-L OLED-BLACK). "
        f"Gefunden in Block: {rail_body.strip()}"
    )
    assert "radial-gradient" not in rail_body, (
        f".rail darf keinen radial-gradient enthalten (H-R.1-L). "
        f"Gefunden in Block: {rail_body.strip()}"
    )


def test_layer3_elements_keep_surface_tone():
    """H-R.1-L (Plan §6, H-R.1-A): Layer-3-Elemente behalten ihre bisherigen Background-
    Tokens (`--surface`, `--surface-raised`). H-R.1 ändert nur die Hintergrund-Slots,
    nicht die Karten/Panels/Banner/Köpfe, die darauf liegen.

    Geprüft werden die wichtigsten vier:
      - `.detail__graph` (die Karte im Detail-Slot, `--surface`)
      - `.update-banner` (transient am oberen Rand, `--surface-raised`)
      - `.editor__head` (sticky Editor-Kopf, `--surface-raised`)
      - `.list__head` (sticky Listen-Kopf, `--surface-raised`)

    Wer nach H-R.1 die Karte versehentlich auf `--bg-void` zieht (sie würde auf dem
    schwarzen Slot verschwinden), fängt diesen Test.
    """
    css = (DEFAULT_STATIC_DIR / "app.css").read_text("utf-8")

    # (selector, erwarteter Background-Token)
    # HINWEIS: die Karte im Detail-Slot ist NICHT `.detail__graph` (das ist nur
    # der Container mit Padding/Flex), sondern `.overview__graph` (Border +
    # Background + Toolbar). Plan-Fehler von H-R.0 -- hier korrigiert.
    cases = (
        (".overview__graph", "var(--surface)"),
        (".update-banner", "var(--surface-raised)"),
        (".editor__head", "var(--surface-raised)"),
        (".list__head", "var(--surface-raised)"),
    )
    for sel, expected in cases:
        body = _block_body(css, sel)
        m = re.search(r"background\s*:\s*([^;]+);", body)
        assert m is not None, (
            f"{sel} braucht eine background-Deklaration. Block: {body.strip()}"
        )
        value = m.group(1).strip()
        assert value == expected, (
            f"{sel} background muss '{expected}' bleiben (H-R.1-L Layer-3-Erhalt). "
            f"Gefunden: '{value}'. Layer-3-Elemente sollen auf dem schwarzen Slot "
            f"sichtbar 'schweben' -- wenn der Background auf --bg-void wechselt, "
            f"verschwindet das Element."
        )


def test_account_nav_uses_accent_fill():
    """H-R.2-L (Plan §2, N.14): `.account-nav` hat Akzent-Fill (genau: `var(--accent-quiet)`
    oder `var(--accent)`). Vor H-R.2 war es `background: none` + `border: none` + eine
    2-px-Akzentkante in `--line-strong` -- "sieht man kaum" (Nikinger-Sichtung
    2026-09-14). Nach H-R.2: Akzent-quiet-Fill + ringsum border in `--accent-edge` +
    `border-left: 3px solid var(--accent)`.

    N.14 ist ein Spezialfall (gilt nur für .account-nav). Andere Navigations-Elemente
    (`.rail__action`) bleiben unverändert -- siehe `test_rail_action_unchanged` weiter
    unten.
    """
    css = (DEFAULT_STATIC_DIR / "app.css").read_text("utf-8")
    body = _block_body(css, ".account-nav")
    bg_m = re.search(r"background\s*:\s*([^;]+);", body)
    assert bg_m is not None, (
        f".account-nav braucht eine background-Deklaration (H-R.2-L). "
        f"Block: {body.strip()}"
    )
    bg_value = bg_m.group(1).strip()
    assert bg_value in ("var(--accent-quiet)", "var(--accent)"), (
        f".account-nav background muss Akzent-Fill sein (H-R.2-L: var(--accent-quiet) "
        f"oder var(--accent)). Gefunden: '{bg_value}'. Vor H-R.2 stand hier 'none'."
    )

    # border-left muss Akzent-Farbe tragen (Afford).
    bl_m = re.search(r"border-left\s*:\s*([^;]+);", body)
    assert bl_m is not None, (
        f".account-nav braucht eine border-left-Deklaration (H-R.2-L). "
        f"Block: {body.strip()}"
    )
    bl_value = bl_m.group(1).strip()
    assert "var(--accent)" in bl_value, (
        f".account-nav border-left muss var(--accent) enthalten (H-R.2-L). "
        f"Gefunden: '{bl_value}'."
    )


def test_account_nav_hover_kept():
    """H-R.2-L: `.account-nav:hover` behält ein Hover-Verhalten. Vor H-R.2 war es
    `background: var(--select-fill-quiet) + outline: 1px solid var(--select-line-quiet)`.
    Nach H-R.2: Akzent-Fill wird verstärkt (`color-mix`) + Outline in `--accent-line`
    statt `--select-line-quiet`.

    Wer den Hover-Block ersatzlos löscht, fängt diesen Test -- der Knopf wäre dann
    statisch ohne Rückmeldung.
    """
    css = (DEFAULT_STATIC_DIR / "app.css").read_text("utf-8")

    # .account-nav + :hover zusammen als Block.
    m = re.search(
        r"\.account-nav\s*:\s*hover\s*\{([^}]*)\}",
        css,
    )
    assert m is not None, (
        ".account-nav:hover braucht einen eigenen Block (H-R.2-L Hover-Erhalt). "
        "Wer den :hover-Block ersatzlos löscht, bricht diesen Test."
    )
    hover_body = m.group(1)
    # Mindestens eines der folgenden muss vorhanden sein: background-Änderung,
    # outline-Änderung, color-mix. Ein leerer Hover-Block zählt nicht als Hover.
    has_background = "background" in hover_body
    has_outline = "outline" in hover_body
    assert has_background or has_outline, (
        f".account-nav:hover muss mindestens background- oder outline-Eintrag haben "
        f"(H-R.2-L). Block: {hover_body.strip()}"
    )


def test_rail_account_unchanged_from_block_h():
    """H-R.2-L: `.rail__account` bleibt unverändert seit Block H. Block H hat es auf
    `flex-direction: column` als Normalfall umgestellt; die alte Sonderregel in einer
    wegoptimierten Media-Query ist weg. Nach H-R.2 (H-R.1 hat `.rail`-Background
    geändert, nicht `.rail__account`) muss `.rail__account` weiterhin `flex-direction:
    column` haben und genau zwei Knöpfe umschließen.

    Diese Wächter ergänzen `test_rail_order_settings_and_logout_at_the_end` (Block H
    hat dort die Reihenfolge festgehalten -- Position der Knöpfe im Markup).
    """
    css = (DEFAULT_STATIC_DIR / "app.css").read_text("utf-8")
    body = _block_body(css, ".rail__account")
    assert "flex-direction: column" in body, (
        f".rail__account muss flex-direction: column behalten (Block H H1, "
        f"H-R.2-L unverändert). Block: {body.strip()}"
    )

    # Markup-Check: genau zwei Knöpfe im .rail__account (Einstellungen + Abmelden).
    html = (DEFAULT_STATIC_DIR / "app.html").read_text("utf-8")
    m = re.search(
        r'<div class="rail__account">\s*(.*?)\s*</div>\s*</nav>',
        html,
        re.DOTALL,
    )
    assert m is not None, (
        ".rail__account sollte im Markup direkt vor </nav> stehen (Block H H1)."
    )
    block = m.group(1)
    assert block.count("<button") == 2, (
        f".rail__account muss genau zwei <button>s umschließen "
        f"(Einstellungen + Abmelden, Block H H1). Gefunden: {block.count('<button')}"
    )
    assert "account-button" in block, (
        "#account-button muss in .rail__account stehen (Block H H1, N.9-Umkehr)."
    )
    assert "logout-button" in block, (
        "#logout-button muss in .rail__account stehen (Block H H1, N.9-Umkehr)."
    )


def test_rail_action_unchanged():
    """H-R.2-L (N.14): `.rail__action` (Einstellungen + Abmelden unten) bleibt
    unverändert. N.14 ist ein Spezialfall für `.account-nav` -- die Rail-Knöpfe
    sollen weiterhin transparent + Hover sein, NICHT den Akzent-Fill der
    Konto-Dialog-Knöpfe erben.

    Nikinger-Sichtung 2026-09-14: "Bei einstellungen und abmelden passt das eigentlich
    so, ich finde auch die kleine Trennung gut." -- das ist die Begründung für N.14.
    Wer hier den Akzent-Fill auf `.rail__action` ausdehnt, fängt diesen Test.
    """
    css = (DEFAULT_STATIC_DIR / "app.css").read_text("utf-8")
    body = _block_body(css, ".rail__action")
    bg_m = re.search(r"background\s*:\s*([^;]+);", body)
    bg_value = bg_m.group(1).strip() if bg_m else "(kein background-Eintrag)"
    # .rail__action darf KEINEN Akzent-Fill haben (N.14: Spezialfall nur .account-nav).
    assert "var(--accent)" not in bg_value or bg_value == "transparent", (
        f".rail__action background darf nicht Akzent-Fill sein (H-R.2-L N.14 "
        f"Spezialfall nur .account-nav). Gefunden: '{bg_value}'."
    )


# --- Phase 8.6 Block H-R Teil 2 (Plan: docs/concepts/phase8_6_ui_polish_block_h_r_plan.md)
# Drei Sub-Bloecke: H-R.3 (Editor-YAML-Buendigkeit), H-R.4 (1024-er Map-Overlap),
# H-R.5 (1024-er Editor-Modus). CDP-Proben V142/V143/V144 sind pre-fix/post-fix gemessen
# (probes/v142_v143_v144_{pre_fix,post_fix}.json); die drei Wächter hier halten die Fixes
# statisch fest, damit ein stiller Refactor zurueck auf G-R.3-Stand geblockt wird.


def test_editor_head_padding_bottom_aligns_with_list_head():
    """H-R.3-L (Plan §3, V142): `.editor__head { padding-bottom }` muss >= 32 px sein,
    damit die Editor-Head-Unterkante auf gleicher Y-Position liegt wie die
    .list__head-Unterkante (CDP-Probe pre-fix: 27,14 px Versatz, post-fix: 0,86 px,
    H-R.3-A Abnahmekriterium <= 2 px Toleranz).

    Vorher (G-R.3-Stand): padding-bottom = calc(var(--space) * 1.5) = 12 px.
    Block G-R.3 hatte das so gelassen, weil es nur die Item-Zeile-YAML-Bündigkeit
    reparieren sollte ("die YAML-Kopfzeile schliesst buendig mit der Item-Zeile ab"
    -- Nikinger-Vorgabe vom 2026-09-14 zur damaligen Zeit). Nikinger hat am selben
    Tag in der Sichtung erkannt, dass die YAML-Kopfzeile zur Suchzeilen-Unterkante
    bündig sein muss, nicht zur Item-Zeile (H-R.3 neu) -- und das ist nur erreichbar,
    wenn der Editor-Head inkl. Bottom-Padding die volle .list__head-Höhe einnimmt.

    padding-top bleibt klein (calc(var(--space) * 0.5) = 4 px) -- der Titel sitzt
    weiter oben, die YAML-Box beginnt 4 px unter dem oberen Rand. Nur padding-bottom
    muss gross genug sein, um die Unterkante auf Listen-Head-Höhe zu bringen.

    Wer das padding-bottom wieder auf 12 px oder kleiner zurueckdreht, faengt diesen
    Test. Der visuelle Effekt waere der G-R.3-Stand: YAML-Kopfzeile sitzt ~27 px
    ueber der Suchzeilen-Unterkante, der Editor wirkt im Detail-Slot hoeher als die
    Liste im Listen-Slot.

    Parser-Hinweis: `padding: calc(var(--space) * 0.5) calc(var(--space) * 3)
    calc(var(--space) * 5)` -- die Klammern im `calc(...)`-Ausdruck enthalten
    Leerzeichen. Ein naiver Split auf Whitespace zerlegt das in 5 Teile (nicht 3).
    Wir extrahieren die drei Werte deshalb per Regex-Pattern statt mit `.split()`.
    """
    css = (DEFAULT_STATIC_DIR / "app.css").read_text("utf-8")

    head_match = re.search(r"\.editor__head\s*\{([^}]*)\}", css)
    assert head_match is not None, (
        "app.css muss eine Regel `.editor__head { ... }` enthalten."
    )
    head_body = head_match.group(1)
    head_body = re.sub(r"/\*.*?\*/", "", head_body, flags=re.DOTALL)

    padding_match = re.search(r"padding\s*:\s*([^;]+);", head_body)
    assert padding_match is not None, (
        f".editor__head braucht eine padding-Deklaration. Block: {head_body.strip()}"
    )
    padding_value = padding_match.group(1).strip()

    # Drei top-Level calc(...) oder px-/Zahl-Werte extrahieren. Ein calc-Ausdruck
    # enthaelt selbst Klammern (var(--space) hat -- in den runden), deshalb
    # koennen wir nicht `[^)]*` verwenden -- wir parsen manuell.
    parts: list[str] = []
    i = 0
    while i < len(padding_value):
        # Skip whitespace.
        while i < len(padding_value) and padding_value[i].isspace():
            i += 1
        if i >= len(padding_value):
            break
        if padding_value[i:].startswith("calc("):
            # Klammern-Balance mitnehmen -- bei einer 'calc('(' startet die
            # Zaehlung bei 1, bei ')' dekrementiert, Ende bei 0.
            depth = 0
            j = i
            while j < len(padding_value):
                if padding_value[j] == "(":
                    depth += 1
                elif padding_value[j] == ")":
                    depth -= 1
                    if depth == 0:
                        j += 1
                        break
                j += 1
            parts.append(padding_value[i:j])
            i = j
        else:
            # Zahl + optional Einheit (px, rem, em).
            j = i
            while j < len(padding_value) and not padding_value[j].isspace():
                j += 1
            parts.append(padding_value[i:j])
            i = j
    assert len(parts) >= 3, (
        f".editor__head padding-Shorthand muss 3 Werte haben (top horizontal bottom), "
        f"gefunden: '{padding_value}' (extrahierte Teile: {parts})."
    )

    bottom_raw = parts[2].strip()

    def _to_px(value: str) -> float:
        """Wandelt einen CSS-Padding-Wert in Pixel um. Akzeptiert:
        - '40px'      -> 40
        - 'calc(var(--space) * 5)' -> 40  (--space = 8 px per :root-Token)
        - '5'         -> 5  (Fallback fuer Werte ohne Einheit)
        """
        if value.endswith("px"):
            return float(value[:-2])
        if value.startswith("calc(") and "var(--space)" in value:
            # Multiplikator aus 'calc(var(--space) * N)' extrahieren.
            m = re.search(r"\*\s*([\d.]+)", value)
            assert m is not None, (
                f"calc(...) mit var(--space) braucht einen Multiplikator: '{value}'"
            )
            return float(m.group(1)) * 8.0  # --space = 8 px per :root-Token
        # Plain number ohne Einheit
        return float(value)

    bottom_px = _to_px(bottom_raw)
    assert bottom_px >= 32, (
        f".editor__head padding-bottom muss >= 32 px sein (H-R.3-L: Bündigkeit zur "
        f".list__head-Unterkante, V142-CDP-Probe pre-fix 27,14 px / post-fix 0,86 px "
        f"Versatz). Gefunden: '{bottom_raw}' = {bottom_px} px. "
        f"Vor H-R.3 stand hier 'calc(var(--space) * 1.5)' = 12 px."
    )


def test_1024_editor_buttons_present():
    """H-R.5-L (Plan §5, V144): bei 1024 px sind alle Editor-Bedienelemente im DOM
    und nicht `hidden`. CDP-Probe V144 (pre_fix + post_fix, beide): alle 16 Knöpfe
    (Archivieren, Speichern, ×, 10 Format-Hilfen, Vorschau-Toggle, Anhängen +
    Anhängen-Input) als `reachable: true` gemessen.

    Konkreter Befund V144: alle Knöpfe haben positive Rect-Werte innerhalb des
    1024x768-Viewports, keiner ist offscreen. Wer einen der Knöpfe aus dem
    Markup nimmt oder `hidden` setzt (z. B. über `.editor__head-actions { display: none }`
    ohne Sub-Selektor oder ähnliches), faengt diesen Test.

    Wir prüfen hier nur die Markup-Ebene (kein CDP-Lauf im pytest): jede ID +
    jedes data-md-Attribut muss in app.html vorkommen. Das ist die strukturelle
    Garantie; das visuelle Layout wird per V144 / 1024-er-Screenshot gehalten.
    """
    html = (DEFAULT_STATIC_DIR / "app.html").read_text("utf-8")

    # Editor-Head-Knöpfe (im .editor__head-actions-Container)
    for btn_id in ("archive-button", "save-button", "close-button"):
        assert f'id="{btn_id}"' in html, (
            f"app.html muss id='{btn_id}' enthalten (H-R.5-L Editor-Knöpfe im "
            f"Detail-Slot, bei 1024 px im unteren Stapel-Slot)."
        )

    # Format-Toolbar im .panel__head der Text-Paneele
    for md in ("bold", "italic", "code", "link", "h", "quote", "ul", "ol", "hr"):
        assert f'data-md="{md}"' in html, (
            f"app.html muss Format-Toolbar-Knopf data-md='{md}' enthalten "
            f"(H-R.5-L Editor-Format-Hilfen)."
        )

    # Vorschau-Toggle + Bild-Insert + Append (zusätzliche Editor-Bedienelemente)
    for btn_id in ("toggle-preview", "insert-image-button", "append-button", "append-input"):
        assert f'id="{btn_id}"' in html, (
            f"app.html muss id='{btn_id}' enthalten (H-R.5-L zusätzliche "
            f"Editor-Bedienelemente)."
        )

    # Titel-Eingabefeld (für V142-Sticky-Header-Inhalt relevant)
    assert 'id="field-title"' in html, (
        "app.html muss id='field-title' enthalten (H-R.5-L Titel-Eingabefeld im "
        "Editor-Head)."
    )
