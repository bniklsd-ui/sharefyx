#!/usr/bin/env python3
"""6.6 (Teil 2) — der Consent im **echten Browser** (Chromium, Playwright).

Der Browser ist hier das Messgerät für **V197**: Chromium prüft `form-action` auch gegen das
Redirect-Ziel einer Formularantwort (P4 Live-Fund 8c, 2026-07-30) — ohne `http://127.0.0.1:*`
im CSP blockiert der Browser den Rücksprung auf den lokalen Listener des Clients **lautlos**
(kein Fehler auf der Seite, nur eine Konsolenmeldung). Der Server antwortet in dem Fall korrekt
mit 302 + gültigem Code — der Bruch passiert ausschließlich im Browser.

**Eigenes venv:** dieses Skript braucht Playwright und läuft mit
`~/.claude-code-tools/e2e-venv/bin/python` (nicht im Projekt-venv, Hard Rule im Prompt).

Aufruf:
    python p105_b6_consent_browser.py <authorize_url> <space> <password> <totp_secret_b32> <out_json>
"""
from __future__ import annotations

import base64
import hashlib
import hmac
import json
import struct
import sys
import time


def totp_now(secret_b32: str) -> str:
    """TOTP (RFC 6238, SHA1, 30 s) — der authserver-Pfad, unabhaengig von `authserver` (dieses
    Skript laeuft im Playwright-venv, nicht im Projekt-venv)."""
    key = base64.b32decode(secret_b32 + "=" * (-len(secret_b32) % 8))
    counter = int(time.time() // 30)
    digest = hmac.new(key, struct.pack(">q", counter), hashlib.sha1).digest()
    offset = digest[-1] & 0x0F
    code = (struct.unpack(">I", digest[offset:offset + 4])[0] & 0x7FFFFFFF) % 1000000
    return f"{code:06d}"


def main() -> int:
    if len(sys.argv) != 6:
        print(__doc__, file=sys.stderr)
        return 2
    authorize_url, space, password, secret_b32, out_path = sys.argv[1:6]

    from playwright.sync_api import sync_playwright

    result: dict = {"authorize_url": authorize_url}
    with sync_playwright() as p:
        browser = p.chromium.launch()
        # Das Wegwerf-Zertifikat ist selbstsigniert (CN/SAN 127.0.0.1) — der Browser muss
        # ihm trotzdem folgen duerfen, sonst messe ich den TLS-Fehler statt der CSP.
        page = browser.new_page(ignore_https_errors=True)
        console: list[str] = []
        page.on("console", lambda msg: console.append(f"{msg.type}: {msg.text}"))
        page.on("pageerror", lambda exc: console.append(f"pageerror: {exc}"))

        response = page.goto(authorize_url, wait_until="domcontentloaded")
        result["authorize_status"] = response.status if response else None
        result["has_login_form"] = page.locator('input[name="password"]').count() > 0

        if result["has_login_form"]:
            page.fill('input[name="space"]', space)
            page.fill('input[name="password"]', password)
            page.fill('input[name="totp"]', totp_now(secret_b32))
            page.click('button[value="allow"]')
            page.wait_for_load_state("domcontentloaded")
            page.wait_for_timeout(500)

        result["final_url"] = page.url
        try:
            result["page_text"] = page.inner_text("body")[:400]
        except Exception as exc:  # pragma: no cover - Messgeraet
            result["page_text"] = f"<nicht lesbar: {exc}>"
        result["console"] = console
        result["csp_violations"] = [
            line for line in console
            if "Content Security Policy" in line or "form-action" in line
        ]
        result["callback_reached"] = (
            "/mcp/oauth/callback" in page.url or "127.0.0.1:19876" in page.url
        )
        browser.close()

    with open(out_path, "w", encoding="utf-8") as fh:
        json.dump(result, fh, ensure_ascii=False, indent=2)
    print(json.dumps(result, ensure_ascii=False))
    return 0


if __name__ == "__main__":
    sys.exit(main())
