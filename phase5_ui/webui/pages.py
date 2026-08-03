"""Servergerenderte HTML-Seiten für die Wege, auf denen es noch keine Sitzung gibt:
Login, Einladung, Enrollment, Fehler. Bewusst OHNE JavaScript — diese Seiten müssen auch
dann funktionieren, wenn app.js nicht lädt.

NICHT zu verwechseln mit authserver/templates.py: das ist die OAuth-Consent-Oberfläche und
bleibt getrennt (P5-G — eine UI-Sitzung kürzt den Consent nicht ab).

Step 3 baut Login und Fehler (Plan §5 Step 3 zeigt nur auf §2.7/§3.4). Einladung/Enrollment
folgen in Step 4, zusammen mit `passwords_policy.py`, das die Einladungsannahme braucht (§2.8).
"""
from __future__ import annotations

from html import escape

_PAGE = """<!doctype html>
<html lang="de"><head><meta charset="utf-8"><title>{title}</title>
<link rel="stylesheet" href="/ui/static/app.css"></head>
<body>{body}</body></html>"""


def render_error_page(message: str) -> str:
    """`message` kommt ausschließlich aus einer festen, internen Textmenge (nie aus
    Nutzereingabe) — trotzdem `escape()`, dieselbe Disziplin wie `authserver/templates.py`."""
    return _PAGE.format(title="Fehler", body=f"<p>{escape(message)}</p>")


def render_logged_in_page(*, csrf_token: str) -> str:
    """Übergangsseite bis Step 6 die echte App-Shell baut. Trägt den CSRF-Token als verstecktes
    Formularfeld — derselbe Grund wie `request_id` in `authserver/templates.py ::
    render_login_form()`: der Token wird von `SessionManager.issue()`/`.rotate()` nur EIN
    einziges Mal als Klartext zurückgegeben (`ui_sessions` speichert nur `csrf_hash`), er muss
    also in genau dieser Antwort an den Browser weitergereicht werden, sonst kann keine
    nachfolgende, CSRF-geprüfte Anfrage (z. B. `/ui/logout`) je einen gültigen Wert vorlegen."""
    body = f"""<p>Angemeldet.</p>
<form method="post" action="/ui/logout">
  <input type="hidden" name="csrf" value="{escape(csrf_token)}">
  <button type="submit">Abmelden</button>
</form>"""
    return _PAGE.format(title="Angemeldet", body=body)


def render_login_page(*, error: str | None = None) -> str:
    """Kein CSRF-Token im Formular — vor einem erfolgreichen Login existiert keine Sitzung und
    damit kein `csrf_hash`, gegen den ein Double-Submit-Wert geprüft werden könnte (siehe
    `security.require_csrf()`-Docstring)."""
    error_html = f'<p class="error">{escape(error)}</p>' if error else ""
    body = f"""{error_html}<form method="post" action="/ui/login">
  <label>Space <input type="text" name="space" autocomplete="username"></label>
  <label>Passwort <input type="password" name="password" autocomplete="current-password"></label>
  <label>Code <input type="text" name="totp" autocomplete="one-time-code"
    placeholder="TOTP- oder Recovery-Code"></label>
  <button type="submit">Anmelden</button>
</form>"""
    return _PAGE.format(title="Anmelden", body=body)
