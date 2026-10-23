"""Markup-Invarianten der servergerenderten Auth-Seiten (`webui/pages.py`, Step 7b).

Diese Seiten sind der einzige Teil der Oberfläche, der ohne JavaScript funktionieren muss, und
der einzige, der HTML im Python-Code zusammensetzt. Zwei Eigenschaften sollen deshalb nicht
stillschweigend zurückkehren können:

1. **Kein `style="…"`-Attribut.** `security.py` sendet `style-src 'self'` ohne `unsafe-inline` —
   ein Style-Attribut wird vom Browser verworfen. Bis Step 7b stand genau so eines hinter dem
   QR-Code (weißer Hintergrund) und war wirkungslos: ein Fix, der wie einer aussah, aber keiner
   war. Das ist die unangenehme Sorte Fehler, weil nichts davon im Server sichtbar wird.
2. **Kein Inline-`<script>`.** Dieselbe CSP verbietet es (`script-src 'self'`); `app.css`/`app.js`
   werden ausschließlich als Datei eingebunden. Die Entsprechung für die App-Shell steht in
   `test_static_routes.py`.
"""
from __future__ import annotations

import re

import pytest
from authserver import totp

from webui import pages

_STYLE_ATTR_RE = re.compile(r"\sstyle\s*=", re.IGNORECASE)
_SCRIPT_OPEN_RE = re.compile(r"<script\b[^>]*>", re.IGNORECASE)


def _all_pages() -> dict[str, str]:
    secret = totp.generate_secret()
    return {
        "login": pages.render_login_page(),
        "login_error": pages.render_login_page(error="Anmeldung fehlgeschlagen."),
        "error": pages.render_error_page("Irgendetwas ging schief."),
        "logged_in": pages.render_logged_in_page(csrf_token="token"),
        "invite": pages.render_invite_page(token="einladung"),
        "invite_error": pages.render_invite_page(token="einladung", error="Passwort zu kurz."),
        "enrollment": pages.render_enrollment_page(
            secret=secret,
            otpauth_uri=totp.provisioning_uri(secret, space="niklas", issuer="sharefyx"),
            csrf_token="token",
        ),
        "recovery": pages.render_recovery_codes_page(codes=["aaaa-bbbb"] * 10, csrf_token="token"),
    }


@pytest.mark.parametrize("name", sorted(_all_pages()))
def test_no_page_uses_an_inline_style_attribute(name):
    html = _all_pages()[name]
    assert not _STYLE_ATTR_RE.search(html), f"style-Attribut in {name} — von der CSP verworfen"


@pytest.mark.parametrize("name", sorted(_all_pages()))
def test_no_page_uses_an_inline_script(name):
    html = _all_pages()[name]
    for match in _SCRIPT_OPEN_RE.finditer(html):
        assert "src=" in match.group(0), f"Inline-<script> in {name}: {match.group(0)!r}"


@pytest.mark.parametrize("name", sorted(_all_pages()))
def test_every_page_wears_the_shared_auth_card(name):
    """Die Meldung des Nikingers war „Login-Seite immer noch identisch zu vorher": die Seiten
    luden `app.css`, benutzten daraus aber keine einzige Klasse. Ein Stylesheet-Link ohne
    Klassen-Markup sieht im Diff nach Gestaltung aus und ist keine."""
    html = _all_pages()[name]
    assert '<div class="auth">' in html
    assert "auth-card" in html
    assert '<link rel="stylesheet" href="/ui/static/app.css">' in html


# -- P10.5 Block 7, Schritt 7.2 (UI-2): die Wortmarke als EIN Austauschpunkt --------------


def _app_html() -> str:
    from webui.config import DEFAULT_STATIC_DIR

    return (DEFAULT_STATIC_DIR / "app.html").read_text(encoding="utf-8")


def test_brand_uses_the_single_logo_file():
    """**D-6 / UI-2:** die Wortmarke zeigt an **beiden** Stellen auf **dieselbe** Datei.

    Die Datei `static/logo.svg` ist der **einzige** Austauschpunkt: ein neues Zeichen wird
    einmal getauscht, und beide Stellen (die Rail der App-Shell und die Anmeldeseite)
    ziehen nach. Zwei Dateien — eine für die Rail, eine für die Seite — wären die Fehlerklasse,
    die hier endet: die Rail zeigt ein Zeichen, die Anmeldeseite ein anderes.

    Geprüft wird **beides**:
    * die Rail (`app.html`) und die serverseitig gerenderte Seite (`pages.py`) nennen dieselbe
      URL, und
    * die URL zeigt auf eine Datei, die **da ist** (ein Pfad ins Leere ist grün in jedem
      Test, der nur den String prüft)."""
    from webui.config import DEFAULT_STATIC_DIR

    logo_url = "/ui/static/logo.svg"
    app_html = _app_html()
    assert f'<img class="brand__mark" src="{logo_url}" alt="S">' in app_html, (
        "die Rail muss das Zeichen als Bild mit dem Alternativtext 'S' einbinden "
        "(das 'S' ist der erste Buchstabe von 'sharefyx', der Wortrest steht als Text daneben)"
    )
    assert (DEFAULT_STATIC_DIR / "logo.svg").is_file(), f"{logo_url} zeigt ins Leere"

    for name, html in _all_pages().items():
        assert f'<img class="brand__mark" src="{logo_url}" alt="S">' in html, (
            f"die Seite {name} bindet das Zeichen nicht ein"
        )
        assert f'<link rel="icon" type="image/svg+xml" href="{logo_url}">' in html, (
            f"die Seite {name} trägt kein Favicon aus derselben Datei"
        )

    assert f'<link rel="icon" type="image/svg+xml" href="{logo_url}">' in app_html, (
        "die App-Shell trägt kein Favicon aus derselben Datei"
    )


def test_the_logo_file_is_valid_xml():
    """Das Zeichen muss **wohlgeformtes XML** sein.

    **Warum dieser Wächter existiert (2026-10-23, Block 7.2):** die erste Fassung der Datei
    trug im Kommentar zwei Bindestriche (`--`). XML verbietet `--` innerhalb eines Kommentars
    — der Browser zeigte die **Fehlerseite** statt des Zeichens, und kein Test der Suite
    sah es: die Datei war Text, und Text ist für die Suite Text. Der Fehler fiel erst auf,
    weil das Zeichen als PNG angeschaut wurde.

    `xml.etree.ElementTree` ist der Parser, den der Browser in der Nähe abbildet: ein
    Wohlfehltheitsfehler ist hier ein Fehler."""
    import xml.etree.ElementTree as ET

    from webui.config import DEFAULT_STATIC_DIR

    ET.parse(DEFAULT_STATIC_DIR / "logo.svg")


def test_the_logo_file_has_exactly_one_drawing():
    """Die Datei ist **eine** Datei: es darf kein zweites Logo im Static-Verzeichnis liegen.

    Hintergrund: die Entwurfsdateien unter `docs/concepts/` (vier Stände vom 2026-10-18) sind
    **Belege**, keine Auslieferung — die Oberfläche darf sie nicht referenzieren. Dieser
    Wächter prüft die *Oberfläche*: unter `static/` liegt genau ein Logo, und die beiden
    Markenstellen nennen es."""
    from webui.config import DEFAULT_STATIC_DIR

    logos = sorted(p.name for p in DEFAULT_STATIC_DIR.glob("*logo*"))
    assert logos == ["logo.svg"], f"unter static/ liegen {logos} — es darf genau ein Zeichen geben"

    for name, html in _all_pages().items():
        # keine der Entwurfsdateien darf in der Oberfläche auftauchen
        assert "entwuerfe" not in html, f"die Seite {name} verweist auf eine Entwurfsdatei"
