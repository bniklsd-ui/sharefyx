"""Servergerenderte HTML-Seiten für die Wege, auf denen es noch keine Sitzung gibt:
Login, Einladung, Enrollment, Fehler. Bewusst OHNE JavaScript-**Abhängigkeit** — diese Seiten
müssen auch dann vollständig funktionieren (Formular abschickbar), wenn app.js nicht lädt.

**[2026-08-06, Nikinger-Feedback „Sichtbarkeitsmöglichkeit beim Passwort eintippen"]:** `_PAGE`
lädt jetzt `app.js` (`defer`, dieselbe Datei, die `render_logged_in_page()` schon lud) für einen
Anzeigen/Verbergen-Umschalter auf Passwortfeldern (`.pw-field`/`.pw-toggle`, `app.js ::
initPasswordToggles()`) — reine Fortschreitung (progressive enhancement), kein `onclick`-Attribut
(CSP `script-src 'self'` ohne `unsafe-inline` bliebe sonst wirkungslos). Lädt app.js nicht, bleibt
das Feld einfach maskiert und das native `<form>` funktioniert unverändert — die Kerngarantie
dieses Docstrings bleibt damit gewahrt, nur die JS-FREIHEIT nicht mehr.

NICHT zu verwechseln mit authserver/templates.py: das ist die OAuth-Consent-Oberfläche und
bleibt getrennt (P5-G — eine UI-Sitzung kürzt den Consent nicht ab).

Step 3 baute Login und Fehler (Plan §5 Step 3 zeigt nur auf §2.7/§3.4). Step 4 ergänzt
Einladung/Enrollment/Recovery-Codes (§2.8) — bewusst weiterhin ohne JavaScript, deshalb submitten
diese Formulare NICHT gegen `/api/v1/account/*` (JSON-only, §3.1), sondern gegen eigene
`/ui/invite/{token}`- bzw. `/ui/enroll/confirm`-Routen in `routes_auth.py`, die dieselbe
`UserDirectory`-Logik aufrufen wie die spätere, JS-gestützte App-Shell (Step 6) — zwei dünne
Einstiege auf denselben Kernfunktionen, keine doppelte Geschäftslogik.

**[2026-08-05, Step 7b]** Diese Seiten trugen bis hierher überhaupt kein Klassen-Markup: sie
luden zwar `app.css`, aber dort gab es für nacktes `<form>`/`<label>`/`<button>` keine einzige
Regel — die Login-Seite sah deshalb aus wie ein unformatiertes Browser-Formular, während die
App-Shell daneben gestaltet war (Meldung des Nikingers). Sie teilen sich jetzt die Karte
`.auth`/`.auth-card` aus `app.css`. Dabei behoben: `render_enrollment_page()` setzte den weißen
Hintergrund hinter dem QR-Code per `style="…"`-Attribut — `security.py` sendet `style-src 'self'`
**ohne** `unsafe-inline`, das blockiert auch Style-Attribute, die Regel griff also nie. Ersetzt
durch `class="qr-frame"`. Ein Test hält fest, dass hier kein `style=` zurückkehrt.
"""
from __future__ import annotations

from html import escape

import segno

_PAGE = """<!doctype html>
<html lang="de"><head><meta charset="utf-8"><title>{title}</title>
<link rel="stylesheet" href="/ui/static/app.css"></head>
<body><div class="auth"><div class="auth-card{extra_class}">
<div class="auth__brand">sharefyx</div>
{body}
</div></div>
<script src="/ui/static/app.js" defer></script>
</body></html>"""


def _page(*, title: str, body: str, wide: bool = False) -> str:
    return _PAGE.format(title=title, body=body, extra_class=" auth-card--wide" if wide else "")


def _error_block(error: str | None) -> str:
    return f'<p class="form-error">{escape(error)}</p>' if error else ""


def render_error_page(message: str) -> str:
    """`message` kommt ausschließlich aus einer festen, internen Textmenge (nie aus
    Nutzereingabe) — trotzdem `escape()`, dieselbe Disziplin wie `authserver/templates.py`."""
    body = f"""<h1>Das hat nicht geklappt</h1>
<p class="form-error">{escape(message)}</p>
<div class="auth__actions"><a class="btn-primary" href="/ui/login">Zur Anmeldung</a></div>"""
    return _page(title="Fehler", body=body)


def render_logged_in_page(*, csrf_token: str) -> str:
    """Bootstrap-Seite zur echten App-Shell (Step 6). Trägt den CSRF-Token als verstecktes
    Formularfeld — derselbe Grund wie `request_id` in `authserver/templates.py ::
    render_login_form()`: der Token wird von `SessionManager.issue()`/`.rotate()` nur EIN
    einziges Mal als Klartext zurückgegeben (`ui_sessions` speichert nur `csrf_hash`), er muss
    also in genau dieser Antwort an den Browser weitergereicht werden. `app.js`s Bootstrap-Teil
    (`webui/static/app.js`) liest genau dieses Feld aus, legt den Wert in `sessionStorage` ab und
    leitet dann nach `/ui/` weiter (Plan-Abweichung 2, `phase5_ui/CLAUDE.md` Session-Block
    2026-08-05) — das Logout-Formular bleibt zusätzlich ohne JavaScript funktionsfähig, falls
    `app.js` aus irgendeinem Grund nicht lädt.
    **[2026-08-06]** `<script>` steht jetzt in `_PAGE` (alle Seiten laden app.js — Passwort-
    Sichtbarkeit, Nikinger-Feedback), hier also nicht mehr doppelt eingebunden. **Damit tragen
    jetzt AUCH `render_enrollment_page()` und `render_recovery_codes_page()` ein
    `name="csrf"`-Feld auf einer Seite, die app.js lädt** — `id="bootstrap-csrf"` markiert
    deshalb EXPLIZIT nur dieses Feld hier als das Bootstrap-Signal; `app.js` sucht seit diesem
    Fund gezielt danach, nicht mehr nach jedem `input[name="csrf"]`. Ohne diese Unterscheidung
    hätte der Bootstrap-Redirect (`location.replace("/ui/")`) mitten von der TOTP-Seed-Seite oder
    den zehn Recovery-Codes weg navigiert — beide werden nur EIN einziges Mal gezeigt, ein
    Advisor-Fund vor dem Commit, nicht live beobachtet."""
    body = f"""<h1>Angemeldet</h1>
<p>Einen Moment — die Oberfläche wird geladen.</p>
<form method="post" action="/ui/logout">
  <input type="hidden" id="bootstrap-csrf" name="csrf" value="{escape(csrf_token)}">
  <div class="auth__actions"><button class="btn" type="submit">Abmelden</button></div>
</form>"""
    return _page(title="Angemeldet", body=body)


def _group4(secret: str) -> str:
    """Base32-Seed in Vierergruppen, laut Plan §2.8 IMMER zusätzlich zum QR-Code gezeigt — ein
    QR-Code, den man bei Kamerafehler nicht abtippen kann, ist eine Sackgasse."""
    return " ".join(secret[i:i + 4] for i in range(0, len(secret), 4))


def render_invite_page(*, token: str, error: str | None = None) -> str:
    """Erster Schritt des Einladungs-Flows (§2.8) — kein CSRF-Token nötig, aus demselben Grund
    wie `render_login_page()`: vor dem Einlösen existiert noch keine Sitzung."""
    body = f"""<h1>Passwort setzen</h1>
<p>Du löst gerade eine Einladung ein. Der Link funktioniert genau einmal.</p>
{_error_block(error)}
<form method="post" action="/ui/invite/{escape(token)}">
  <label class="auth__field">Neues Passwort
    <span class="pw-field">
      <input class="input" type="password" name="password" id="invite-password" autocomplete="new-password">
      <button type="button" class="btn pw-toggle" data-target="invite-password" aria-pressed="false">Anzeigen</button>
    </span>
  </label>
  <div class="auth__actions"><button class="btn-primary" type="submit">Weiter</button></div>
</form>"""
    return _page(title="Einladung", body=body)


def render_enrollment_page(*, secret: str, otpauth_uri: str, csrf_token: str, error: str | None = None) -> str:
    """Zweiter Schritt (§2.8): TOTP-Seed EIN einziges Mal als QR (Inline-SVG, `segno`, V29) und
    als Text gezeigt — beide gleichzeitig, keiner ist der „eigentliche" Weg. `csrf_token` kommt
    aus `SessionManager.issue()`/`.rotate()` (bereits ausgestellte Sitzung, Status
    „TOTP unbestätigt", §2.8) und wird hier zum ersten Mal an den Browser weitergereicht."""
    qr_svg = segno.make(otpauth_uri).svg_inline(scale=4, dark="#000", light="#fff")
    body = f"""<h1>Authenticator einrichten</h1>
<p>QR-Code scannen oder den Seed manuell eintragen. Beides wird nur dieses eine Mal gezeigt.</p>
{_error_block(error)}
<div class="qr-frame">{qr_svg}</div>
<code class="auth__seed">{escape(_group4(secret))}</code>
<form method="post" action="/ui/enroll/confirm">
  <input type="hidden" name="csrf" value="{escape(csrf_token)}">
  <label class="auth__field">Code aus der Authenticator-App
    <input class="input" type="text" name="code" autocomplete="one-time-code" inputmode="numeric">
  </label>
  <div class="auth__actions"><button class="btn-primary" type="submit">Bestätigen</button></div>
</form>"""
    return _page(title="Einrichtung", body=body, wide=True)


def render_recovery_codes_page(*, codes: list[str], csrf_token: str) -> str:
    """Dritter, letzter Schritt (§2.8): zehn Recovery-Codes EIN einziges Mal gezeigt
    (`UserDirectory.issue_recovery_codes()` gibt sie nur hier zurück, danach steht nur noch der
    Hash in `recovery_codes`). Trägt zusätzlich das Logout-Formular aus
    `render_logged_in_page()` — dieselbe Sitzung, derselbe `csrf_token`, kein zweiter."""
    codes_html = "".join(f"<li><code>{escape(c)}</code></li>" for c in codes)
    body = f"""<h1>Recovery-Codes</h1>
<p>Diese zehn Codes werden nur DIESES EINE MAL angezeigt. Jeder ersetzt einmalig den
TOTP-Code beim Anmelden, falls der Authenticator nicht verfügbar ist. Jetzt sichern.</p>
<ul class="auth__codes">{codes_html}</ul>
<form method="post" action="/ui/logout">
  <input type="hidden" name="csrf" value="{escape(csrf_token)}">
  <div class="auth__actions"><button class="btn-primary" type="submit">Gesichert — abmelden</button></div>
</form>"""
    return _page(title="Recovery-Codes", body=body, wide=True)


def render_login_page(*, error: str | None = None) -> str:
    """Kein CSRF-Token im Formular — vor einem erfolgreichen Login existiert keine Sitzung und
    damit kein `csrf_hash`, gegen den ein Double-Submit-Wert geprüft werden könnte (siehe
    `security.require_csrf()`-Docstring)."""
    body = f"""<h1>Anmelden</h1>
{_error_block(error)}
<form method="post" action="/ui/login">
  <label class="auth__field">Space
    <input class="input" type="text" name="space" autocomplete="username">
  </label>
  <label class="auth__field">Passwort
    <span class="pw-field">
      <input class="input" type="password" name="password" id="login-password" autocomplete="current-password">
      <button type="button" class="btn pw-toggle" data-target="login-password" aria-pressed="false">Anzeigen</button>
    </span>
  </label>
  <label class="auth__field">Code
    <input class="input" type="text" name="totp" autocomplete="one-time-code"
      placeholder="TOTP- oder Recovery-Code">
  </label>
  <div class="auth__actions"><button class="btn-primary" type="submit">Anmelden</button></div>
</form>"""
    return _page(title="Anmelden", body=body)
