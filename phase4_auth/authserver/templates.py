"""OAuth-Consent-UI. Kein Framework, kein CSS-Build, keine Cookies — bleibt architektonisch
getrennt von `webui/pages.py` (P5-G: eine UI-Sitzung kürzt den Consent nicht ab, `/oauth/
authorize` liest nie Cookies). Wer hier eine Template-Engine einführt, hat die Phase verwechselt.

**[2026-08-06 Korrektur, Nikinger-Feedback „alte UI beim Connector-Neuanmelden"]:** dieses Modul
trug seit P4 den Docstring „Wird in Phase 5 durch die echte Web-Oberfläche ERSETZT, nicht
erweitert" — P5-G verbietet aber genau das (ein eigener, getrennter Consent-Flow ist Absicht,
keine Übergangslösung). Das Modul blieb dadurch das rohe Phase-4-Formular, während `webui/
pages.py` seit Step 7b gestaltet ist (`.auth`/`.auth-card`, `app.css`) — sichtbar als „alte UI"
bei jeder Connector-(Re-)Autorisierung. Behoben durch **CSS-Wiederverwendung, nicht Code-Import**:
ein `<link>` auf `/ui/static/app.css` (dieselbe `webui`-Route, öffentlich, keine Sitzung nötig —
`static_routes.py :: _static()` prüft keine Auth) macht dieselben `.auth`-Klassen hier nutzbar,
ohne dass `authserver` ein einziges Python-Symbol aus `webui`/`mcpserver` importiert (P4-A bleibt
unverändert: kein Import, nur eine URL-Zeichenkette). Bewusst **kein** `<script>`: dieser Flow ist
sicherheitskritischer als `webui`s Seiten (P5-G), ein zusätzlicher JS-Pfad hier wäre eine größere
Angriffsfläche für einen kleinen kosmetischen Gewinn — anders als bei `webui/pages.py`, wo der
Login/Einladungs-Flow ohnehin schon `app.js` lädt (`render_logged_in_page()`).

Voraussetzung: `_security_headers()` erlaubte bisher `style-src 'unsafe-inline'` **ohne**
`'self'` — ein `<link rel="stylesheet" href="/ui/static/app.css">` wäre damit von der CSP
stillschweigend geblockt worden, dieselbe Fehlerklasse wie das `style="…"`-Attribut hinter dem
QR-Code (`pages.py`-Docstring, Step 7b). `style-src` ist deshalb auf `'self'` umgestellt
(`'unsafe-inline'` entfällt ersatzlos — diese Seite setzt kein einziges `style="…"`-Attribut),
`font-src 'self'` ergänzt (Inter-Variable-Subset aus `/ui/static/fonts/`).
"""
from __future__ import annotations

from html import escape

_PAGE = """<!doctype html>
<html lang="de"><head><meta charset="utf-8"><title>{title}</title>
<link rel="stylesheet" href="/ui/static/app.css"></head>
<body><div class="auth"><div class="auth-card">
<div class="auth__brand">sharefyx</div>
{body}
</div></div></body></html>"""


def render_error_page(message: str) -> str:
    """`message` kommt ausschließlich aus einer festen, internen Textmenge (nie aus
    Nutzereingabe) — trotzdem `escape()`, CSP allein ist kein Ersatz dafür."""
    body = f'<h1>Fehler</h1><p class="form-error">{escape(message)}</p>'
    return _PAGE.format(title="Fehler", body=body)


def render_login_form(request_id: str) -> str:
    """`request_id` ist ein `secrets.token_urlsafe`-Wert (URL-safe-Alphabet, keine HTML-Sonder-
    zeichen) — `escape()` trotzdem, aus demselben Grund wie oben."""
    body = f"""<h1>Connector autorisieren</h1>
<p>Ein Connector fragt nach Zugriff auf deinen Space. Unabhängig von einer laufenden
Browser-Sitzung — Passwort und Code werden bei jeder Autorisierung erneut geprüft (P5-G).</p>
<form method="post" action="/oauth/authorize">
  <input type="hidden" name="request_id" value="{escape(request_id)}">
  <label class="auth__field">Space
    <input class="input" type="text" name="space" autocomplete="username">
  </label>
  <label class="auth__field">Passwort
    <input class="input" type="password" name="password" autocomplete="current-password">
  </label>
  <label class="auth__field">TOTP-Code
    <input class="input" type="text" name="totp" autocomplete="one-time-code">
  </label>
  <div class="auth__actions auth__actions--row">
    <button class="btn-primary" type="submit" name="action" value="allow">Anmelden</button>
    <button class="btn" type="submit" name="action" value="deny">Ablehnen</button>
  </div>
</form>"""
    return _PAGE.format(title="Anmelden", body=body)
