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
