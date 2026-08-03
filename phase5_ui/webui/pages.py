"""Servergerenderte HTML-Seiten für die Wege, auf denen es noch keine Sitzung gibt:
Login, Einladung, Enrollment, Fehler. Bewusst OHNE JavaScript — diese Seiten müssen auch
dann funktionieren, wenn app.js nicht lädt.

NICHT zu verwechseln mit authserver/templates.py: das ist die OAuth-Consent-Oberfläche und
bleibt getrennt (P5-G — eine UI-Sitzung kürzt den Consent nicht ab).

Step 3 baute Login und Fehler (Plan §5 Step 3 zeigt nur auf §2.7/§3.4). Step 4 ergänzt
Einladung/Enrollment/Recovery-Codes (§2.8) — bewusst weiterhin ohne JavaScript, deshalb submitten
diese Formulare NICHT gegen `/api/v1/account/*` (JSON-only, §3.1), sondern gegen eigene
`/ui/invite/{token}`- bzw. `/ui/enroll/confirm`-Routen in `routes_auth.py`, die dieselbe
`UserDirectory`-Logik aufrufen wie die spätere, JS-gestützte App-Shell (Step 6) — zwei dünne
Einstiege auf denselben Kernfunktionen, keine doppelte Geschäftslogik.
"""
from __future__ import annotations

from html import escape

import segno

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


def _group4(secret: str) -> str:
    """Base32-Seed in Vierergruppen, laut Plan §2.8 IMMER zusätzlich zum QR-Code gezeigt — ein
    QR-Code, den man bei Kamerafehler nicht abtippen kann, ist eine Sackgasse."""
    return " ".join(secret[i:i + 4] for i in range(0, len(secret), 4))


def render_invite_page(*, token: str, error: str | None = None) -> str:
    """Erster Schritt des Einladungs-Flows (§2.8) — kein CSRF-Token nötig, aus demselben Grund
    wie `render_login_page()`: vor dem Einlösen existiert noch keine Sitzung."""
    error_html = f'<p class="error">{escape(error)}</p>' if error else ""
    body = f"""{error_html}<h1>Passwort setzen</h1>
<form method="post" action="/ui/invite/{escape(token)}">
  <label>Neues Passwort <input type="password" name="password" autocomplete="new-password"></label>
  <button type="submit">Weiter</button>
</form>"""
    return _PAGE.format(title="Einladung", body=body)


def render_enrollment_page(*, secret: str, otpauth_uri: str, csrf_token: str, error: str | None = None) -> str:
    """Zweiter Schritt (§2.8): TOTP-Seed EIN einziges Mal als QR (Inline-SVG, `segno`, V29) und
    als Text gezeigt — beide gleichzeitig, keiner ist der „eigentliche" Weg. `csrf_token` kommt
    aus `SessionManager.issue()`/`.rotate()` (bereits ausgestellte Sitzung, Status
    „TOTP unbestätigt", §2.8) und wird hier zum ersten Mal an den Browser weitergereicht."""
    qr_svg = segno.make(otpauth_uri).svg_inline(scale=4, dark="#000", light="#fff")
    error_html = f'<p class="error">{escape(error)}</p>' if error else ""
    body = f"""{error_html}<h1>Authenticator einrichten</h1>
<p>QR-Code scannen oder den Seed manuell eintragen:</p>
<div style="background:#fff;padding:8px;display:inline-block">{qr_svg}</div>
<p><code>{escape(_group4(secret))}</code></p>
<form method="post" action="/ui/enroll/confirm">
  <input type="hidden" name="csrf" value="{escape(csrf_token)}">
  <label>Code aus der Authenticator-App <input type="text" name="code" autocomplete="one-time-code"></label>
  <button type="submit">Bestätigen</button>
</form>"""
    return _PAGE.format(title="Einrichtung", body=body)


def render_recovery_codes_page(*, codes: list[str], csrf_token: str) -> str:
    """Dritter, letzter Schritt (§2.8): zehn Recovery-Codes EIN einziges Mal gezeigt
    (`UserDirectory.issue_recovery_codes()` gibt sie nur hier zurück, danach steht nur noch der
    Hash in `recovery_codes`). Trägt zusätzlich das Logout-Formular aus
    `render_logged_in_page()` — dieselbe Sitzung, derselbe `csrf_token`, kein zweiter."""
    codes_html = "".join(f"<li><code>{escape(c)}</code></li>" for c in codes)
    body = f"""<h1>Recovery-Codes</h1>
<p>Diese zehn Codes werden nur DIESES EINE MAL angezeigt. Jeder ersetzt einmalig den
TOTP-Code beim Anmelden, falls der Authenticator nicht verfügbar ist.</p>
<ul>{codes_html}</ul>
<form method="post" action="/ui/logout">
  <input type="hidden" name="csrf" value="{escape(csrf_token)}">
  <button type="submit">Fertig — abmelden</button>
</form>"""
    return _PAGE.format(title="Recovery-Codes", body=body)


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
