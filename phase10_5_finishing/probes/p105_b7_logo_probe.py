#!/usr/bin/env python3
"""P10.5 Block 7, Schritt 7.2 (UI-2) — die Wortmarke an der **Wegwerf-Instanz**.

**Wozu diese Probe ist (2026-10-23).** Die Wortmarke hat drei Eigenschaften, die kein
Unit-Test sees:

1. **Der MIME-Typ.** Die Static-Route kannte kein `.svg` und lieferte
   `application/octet-stream` — und der Browser **rendert ein SVG mit falschem MIME-Typ
   nicht**. Der Fehler fiel nur auf, weil die Seite wirklich angeschaut wurde.
2. **Die CSP.** `img-src 'self' data:` muss das Zeichen durchlassen.
3. **Die tatsächliche Darstellung.** Das Zeichen muss 16 × 16 Pixel groß sein, an der
   richtigen Stelle sitzen und nicht abgeschnitten sein.

**Die Instanz ist eine Wegwerf-Instanz:** eigener Port **18790**, tmp-`DATA_ROOT`,
tmp-`auth.sqlite3`, eigener Keyring, eigenes DEK — **nicht** gegen `DATA_ROOT`, die echte
`auth.sqlite3` oder den laufenden Dienst. Start und Stopp laufen über die PID-Datei
(Hard Rule 9: kein `pkill -f`, kein `systemctl`).

**Gegenlauf (2026-10-23).** Der Lauf mit dem MIME-Typ `application/octet-stream` (also
**ohne** den Eintrag `.svg` in `static_routes.py`) muss **rot** werden: genau dann, wenn
der Browser das Zeichen nicht rendert. Der Gegenlauf ist der Grund, warum die Probe mehr
ist als ein Screenshot.

Aufruf:  `.venv/bin/python phase10_5_finishing/probes/p105_b7_logo_probe.py [--gegenlauf]`
Ergebnis: `phase10_5_finishing/probes/p105_b7_logo_probe.json`
"""
from __future__ import annotations

import argparse
import base64
import json
import os
import secrets
import signal
import subprocess
import sys
import time
import urllib.request
from pathlib import Path

REPO_ROOT = Path(__file__).resolve().parents[2]
WEGWERF_ROOT = Path("/tmp/opencode/sharefyx-wegwerf-b72")
DATA_ROOT = WEGWERF_ROOT / "data"
AUTH_DB = WEGWERF_ROOT / "auth.sqlite3"
DEK_FILE = WEGWERF_ROOT / "auth-dek"
SERVE_PID = WEGWERF_ROOT / "serve.pid"
SERVE_LOG = WEGWERF_ROOT / "serve.log"
SHOT = WEGWERF_ROOT / "login.png"
PORT = 18790
BASE = f"http://127.0.0.1:{PORT}"
RESULT = Path(__file__).resolve().with_name("p105_b7_logo_probe.json")


def _setup() -> None:
    WEGWERF_ROOT.mkdir(parents=True, exist_ok=True)
    DATA_ROOT.mkdir(parents=True, exist_ok=True)
    if not DEK_FILE.exists():
        raw = secrets.token_bytes(32)
        DEK_FILE.write_text(base64.urlsafe_b64encode(raw).rstrip(b"=").decode("ascii") + "\n")
        os.chmod(DEK_FILE, 0o600)


def _serve() -> int:
    env = os.environ.copy()
    env["SPACE_DATA_ROOT"] = str(DATA_ROOT)
    env["SPACE_AUTH_DB"] = str(AUTH_DB)
    env["SPACE_PUBLIC_BASE_URL"] = "https://wegwerf-b72.invalid"
    env["SPACE_PORT"] = str(PORT)
    env["CREDENTIALS_DIRECTORY"] = str(WEGWERF_ROOT)
    env["PYTHONPATH"] = str(REPO_ROOT)
    log = SERVE_LOG.open("ab")
    proc = subprocess.Popen(
        [".venv/bin/python", "phase2_mcp/scripts/serve.py", "--allowed-host", "127.0.0.1"],
        env=env, cwd=str(REPO_ROOT), stdout=log, stderr=subprocess.STDOUT, start_new_session=True,
    )
    SERVE_PID.write_text(str(proc.pid))
    for _ in range(60):
        try:
            urllib.request.urlopen(f"{BASE}/health", timeout=1).read()
            return proc.pid
        except Exception:
            time.sleep(0.25)
    raise SystemExit("Wegwerf-Server wurde nicht gesund.")


def _stop() -> None:
    if not SERVE_PID.exists():
        return
    pid = int(SERVE_PID.read_text().strip())
    try:
        os.kill(pid, signal.SIGTERM)
    except ProcessLookupError:
        pass
    for _ in range(40):
        if not Path(f"/proc/{pid}").exists():
            break
        time.sleep(0.25)
    SERVE_PID.unlink(missing_ok=True)


def _fetch(path: str) -> tuple[int, "email.message.Message", bytes]:
    """**Die Header-Map bleibt ein `Message`:** uvicorn schickt die Header klein
    (`content-type`), und ein `dict(...)` würde die Schreibweise zerstören — der erste Lauf
    sah deshalb einen leeren Content-Type, obwohl der Server richtig antwortete. `Message.get()`
    ist gross-/kleinschreibungs-unabhängig."""
    req = urllib.request.Request(f"{BASE}{path}")
    try:
        with urllib.request.urlopen(req, timeout=5) as resp:
            return resp.status, resp.headers, resp.read()
    except urllib.error.HTTPError as exc:
        return exc.code, exc.headers, exc.read()


BROWSER_SKILL = '''import json, sys
from playwright.sync_api import sync_playwright

base, shot = sys.argv[1], sys.argv[2]
with sync_playwright() as p:
    browser = p.chromium.launch()
    page = browser.new_page(viewport={"width": 900, "height": 760})
    antworten = []
    page.on("response", lambda r: antworten.append(
        {"url": r.url, "status": r.status, "content_type": r.headers.get("content-type", "")}))
    page.goto(base + "/ui/login", wait_until="networkidle")
    marke = page.evaluate("""() => {
        const img = document.querySelector(".brand__mark");
        if (!img) return {vorhanden: false};
        const r = img.getBoundingClientRect();
        return {vorhanden: true, vollstaendig: img.complete, natural_width: img.naturalWidth,
                natural_height: img.naturalHeight, breite: Math.round(r.width),
                hoehe: Math.round(r.height), alt: img.getAttribute("alt"),
                src: img.getAttribute("src")};
    }""")
    favicon = page.evaluate("""() => {
        const l = document.querySelector('link[rel="icon"]');
        return l ? l.getAttribute("href") : null;
    }""")
    page.screenshot(path=shot)
    browser.close()
print(json.dumps({"marke": marke, "favicon": favicon,
                  "antworten": [a for a in antworten if "logo" in a["url"]]}))
'''


def _browser() -> dict:
    """Der Browser ist das Messgerät: `naturalWidth` ist 0, wenn der Browser das Zeichen
    **nicht** gerendert hat (falscher MIME-Typ, blockierte CSP, 404)."""
    skript = WEGWERF_ROOT / "browser_check.py"
    skript.write_text(BROWSER_SKILL, encoding="utf-8")
    e2e = Path.home() / ".claude-code-tools/e2e-venv/bin/python"
    proc = subprocess.run([str(e2e), str(skript), BASE, str(SHOT)],
                          cwd=str(REPO_ROOT), capture_output=True, text=True)
    if proc.returncode != 0:
        return {"fehler": proc.stderr[-800:], "marke": {"vorhanden": False}}
    return json.loads(proc.stdout.strip().splitlines()[-1])


def main(argv: list[str] | None = None) -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--gegenlauf", action="store_true",
                        help="den MIME-Typ 'application/octet-stream' erzwingen (ohne den "
                             "Eintrag '.svg' in static_routes.py) — die Probe muss dann rot werden")
    args = parser.parse_args(argv)

    static_routes = REPO_ROOT / "phase5_ui/webui/static_routes.py"
    backup = None
    if args.gegenlauf:
        # **Der Gegenlauf:** der MIME-Eintrag `.svg` fliegt raus -- der Server antwortet dann
        # mit `application/octet-stream`, und der Browser darf das Zeichen **nicht** rendern.
        # Genau das war der Befund vom 2026-10-23: die Datei war da, das Markup war da, und
        # die Seite zeigte trotzdem kein Zeichen.
        backup = static_routes.read_text(encoding="utf-8")
        static_routes.write_text(
            backup.replace('    ".svg": "image/svg+xml",\n', ""), encoding="utf-8")

    _setup()
    pid = _serve()
    try:
        status, headers, body = _fetch("/ui/static/logo.svg")
        content_type = headers.get("content-type", "")
        csp = headers.get("content-security-policy", "")
        login_status, _, login_html = _fetch("/ui/login")
        browser = _browser()
        marke = browser.get("marke", {})
        favicon_im_html = 'rel="icon"' in login_html.decode("utf-8", "replace")
        bild_im_html = 'class="brand__mark"' in login_html.decode("utf-8", "replace")

        ergebnis = {
            "probe": "p105_b7_logo",
            "instanz": {"basis": BASE, "data_root": str(DATA_ROOT), "pid": pid, "wegwerf": True},
            "logo_datei": {
                "status": status,
                "content_type": content_type,
                "bytes": len(body),
                "ist_svg": b"<svg" in body,
            },
            "csp": csp,
            "login_seite": {
                "status": login_status,
                "hat_favicon_link": favicon_im_html,
                "hat_marke": bild_im_html,
            },
            "marke_im_browser": marke,
            "favicon_link": browser.get("favicon"),
            "logo_antworten": browser.get("antworten"),
            "screenshot": str(SHOT),
        }
        # Die Kriterien: MIME-Typ, CSP, Markup, Bildinhalt.
        ok = (
            status == 200
            and content_type.startswith("image/svg+xml")
            and "img-src 'self'" in csp
            and favicon_im_html
            and bild_im_html
            and marke.get("vorhanden") is True
            and marke.get("vollstaendig") is True
            and int(marke.get("natural_width", 0)) > 0
            and 12 <= int(marke.get("hoehe", 0)) <= 22
        )
        ergebnis["alle_kriterien_erfuellt"] = bool(ok)
        if args.gegenlauf:
            ergebnis["gegenlauf"] = True
            ergebnis["hinweis"] = (
                "Gegenlauf: der MIME-Eintrag '.svg' war entfernt (also "
                "'application/octet-stream') -- die Probe muss jetzt ROT sein, weil der "
                "Browser das Zeichen nicht rendert. Ist sie grün, prüft die Probe nicht das, "
                "was sie behauptet."
            )
            ergebnis["gegenlauf_erwartet_rot"] = not ok
        RESULT.write_text(json.dumps(ergebnis, indent=2, ensure_ascii=False) + "\n", encoding="utf-8")
        print(json.dumps(ergebnis, indent=2, ensure_ascii=False))
        if args.gegenlauf:
            # Im Gegenlauf ist das gewuenschte Ergebnis "nicht erfüllt" -- sonst waere die
            # Probe auch dann gruen, wenn sie nichts prueft.
            return 0 if not ok else 1
        return 0 if ok else 1
    finally:
        _stop()
        if backup is not None:
            static_routes.write_text(backup, encoding="utf-8")


if __name__ == "__main__":
    raise SystemExit(main())
