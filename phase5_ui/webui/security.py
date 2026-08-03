"""Sicherheits-Header + CSRF-Prüfung der UI (Plan §2.7, §3.4) — **getrennt** von
`authserver/routes.py :: _security_headers()`: die OAuth-Seiten brauchen `claude.ai` in
`form-action`, die UI nicht; eine gemeinsame Funktion würde eine der beiden Seiten schwächen.
"""
from __future__ import annotations

from authserver import crypto
from authserver.models import SessionRow
from starlette.requests import Request

from .config import UiSettings
from .errors import CsrfError


def ui_security_headers(settings: UiSettings) -> dict[str, str]:
    """Plan §3.4. `img-src 'self' data:` ist die einzige Lockerung (Inline-SVG-QR-Code, Step 4).
    `script-src 'self'` ohne `unsafe-inline`: jedes Stück JavaScript liegt in `app.js`, kein
    `onclick`-Attribut, kein `<script>`-Block."""
    headers = {
        "Content-Security-Policy": (
            "default-src 'none'; script-src 'self'; style-src 'self'; "
            "img-src 'self' data:; font-src 'self'; connect-src 'self'; form-action 'self'; "
            "frame-ancestors 'none'; base-uri 'none'"
        ),
        "Referrer-Policy": "no-referrer",
        "X-Content-Type-Options": "nosniff",
        "X-Frame-Options": "DENY",
        "Cross-Origin-Opener-Policy": "same-origin",
        "Cross-Origin-Resource-Policy": "same-origin",
        "Permissions-Policy": "camera=(), microphone=(), geolocation=(), interest-cohort=()",
        "Cache-Control": "no-store",
    }
    if settings.hsts:
        headers["Strict-Transport-Security"] = "max-age=63072000; includeSubDomains"
    return headers


def require_csrf(
    request: Request,
    session: SessionRow,
    *,
    settings: UiSettings,
    form_token: str | None = None,
) -> None:
    """Wirft `CsrfError` (→403), wenn eine der drei Prüfungen scheitert (Plan §2.7). Braucht
    eine bereits geladene `session: SessionRow` (`SessionManager.load()`) — schützt damit
    ausschließlich Routen, die schon eine gültige Sitzung voraussetzen (z. B. `/ui/logout`,
    ab Step 4/5 die Account-/API-Routen). `/ui/login` selbst hat vor dem Erfolg keine Sitzung
    und damit keinen `csrf_hash`, gegen den ein Double-Submit-Token geprüft werden könnte —
    dort schützt stattdessen `SameSite=Strict` plus die Fehlversuchsbremse.

    `form_token` ist der bereits aus dem Formular gelesene Wert (`form.get("csrf")`) — diese
    Funktion liest den Request-Body selbst nicht, um nicht implizit `async` zu werden und den
    Body kein zweites Mal konsumieren zu müssen; ein Aufrufer, der ohnehin `await
    request.form()` braucht, reicht das Feld einfach durch."""
    if request.method in ("GET", "HEAD"):
        return

    origin = request.headers.get("origin")
    if origin is not None:
        if origin != settings.base_url:
            raise CsrfError("Herkunft (Origin) stimmt nicht")
    elif request.headers.get("sec-fetch-site") != "same-origin":
        raise CsrfError("Herkunft nicht bestimmbar")

    submitted = request.headers.get("x-csrf-token") or form_token
    if submitted is None or not crypto.secrets_equal(crypto.hash_secret(submitted), session.csrf_hash):
        raise CsrfError("CSRF-Token fehlt oder stimmt nicht")
