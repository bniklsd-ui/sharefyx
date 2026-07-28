"""Wegwerf-UI. Wird in Phase 5 durch die echte Web-Oberfläche ERSETZT, nicht erweitert.

Kein Framework, kein JavaScript, kein CSS-Build, keine Cookies. Wer hier eine
Template-Engine einführt, hat die Phase verwechselt.
"""
from __future__ import annotations

from html import escape

_PAGE = """<!doctype html>
<html lang="de"><head><meta charset="utf-8"><title>{title}</title></head>
<body>{body}</body></html>"""


def render_error_page(message: str) -> str:
    """`message` kommt ausschließlich aus einer festen, internen Textmenge (nie aus
    Nutzereingabe) — trotzdem `escape()`, CSP allein (`style-src 'unsafe-inline'` ist an)
    ist kein Ersatz dafür."""
    return _PAGE.format(title="Fehler", body=f"<p>{escape(message)}</p>")


def render_login_form(request_id: str) -> str:
    """`request_id` ist ein `secrets.token_urlsafe`-Wert (URL-safe-Alphabet, keine HTML-Sonder-
    zeichen) — `escape()` trotzdem, aus demselben Grund wie oben."""
    body = f"""<form method="post" action="/oauth/authorize">
  <input type="hidden" name="request_id" value="{escape(request_id)}">
  <label>Space <input type="text" name="space" autocomplete="username"></label>
  <label>Passwort <input type="password" name="password" autocomplete="current-password"></label>
  <label>TOTP-Code <input type="text" name="totp" autocomplete="one-time-code"></label>
  <button type="submit" name="action" value="allow">Anmelden</button>
  <button type="submit" name="action" value="deny">Ablehnen</button>
</form>"""
    return _PAGE.format(title="Anmelden", body=body)
