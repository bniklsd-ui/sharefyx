#!/usr/bin/env python3
"""P10.5 Block 7, Schritt 7.3 (UI-3) — der **Tab-Titel** je Ansicht (V120, D-5 deutsch).

**Wozu diese Probe ist.** Der Tab-Titel ist das einzige UI-Element, das **außerhalb** des
Fensters liegt — und deshalb das einzige, das man beim Wechseln eines Tabs sieht. Der Plan
(§Block 7, Schritt 7.3) nennt fünf Titel: „Übersicht", Space-Liste (Space-Name), Item
(Titel), „Karte", „Einstellungen". **Gemessen sind es vier Zustände, nicht fünf:** die Karte
ist kein eigener Zustand, sondern der Kontext-Bereich neben der Liste (sie ist im
Listen-Zustand immer sichtbar, und `loadGraph()` läuft bei jedem Spacewechsel, jedem
Home-Klick und jedem Refresh — ein dort gesetzter Titel würde den Item-Titel überschreiben
und beim Laden flackern). Das ist eine **datierte Korrektur zum Plan**; die Karte bekommt
deshalb keinen eigenen Titel.

**Der Gegenlauf (der Grund, warum das eine Probe und kein Screenshot ist).** Der Aufruf
`setViewTitle(item.title)` in `editor.js :: loadEditorFromItem()` entfernt ⇒ der Tab-Titel
bleibt beim Space-Namen stehen ⇒ die Probe muss **rot** werden.

**Wegwerf-Instanz:** eigener Port **18791**, tmp-`DATA_ROOT`, tmp-`auth.sqlite3`, eigener
Keyring, eigenes DEK, **ein** Space mit **einem** Item. Start und Stopp über die PID-Datei
(Hard Rule 9: kein `pkill -f`, kein `systemctl`).

Aufruf:  `.venv/bin/python phase10_5_finishing/probes/p105_b7_titel_probe.py [--gegenlauf]`
Ergebnis: `phase10_5_finishing/probes/p105_b7_titel_probe.json`
"""
from __future__ import annotations

import argparse
import base64
import json
import os
import secrets
import shutil
import signal
import subprocess
import sys
import time
import urllib.request
from datetime import datetime, timezone
from pathlib import Path

REPO_ROOT = Path(__file__).resolve().parents[2]
WEGWERF_ROOT = Path("/tmp/opencode/sharefyx-wegwerf-b73")
DATA_ROOT = WEGWERF_ROOT / "data"
AUTH_DB = WEGWERF_ROOT / "auth.sqlite3"
DEK_FILE = WEGWERF_ROOT / "auth-dek"
SERVE_PID = WEGWERF_ROOT / "serve.pid"
SERVE_LOG = WEGWERF_ROOT / "serve.log"
PORT = 18791
BASE = f"http://127.0.0.1:{PORT}"
SPACE = "alpha"
ITEM_TITEL = "Erster Eintrag fuer den Tab-Titel"
RESULT = Path(__file__).resolve().with_name("p105_b7_titel_probe.json")

BROWSER_SKILL = '''import json, sys, time, hmac, hashlib, struct, base64

base, space, password, secret, item_titel = sys.argv[1:6]

def totp_now(secret_b32):
    key = base64.b32decode(secret_b32 + "=" * (-len(secret_b32) % 8))
    counter = int(time.time() // 30)
    digest = hmac.new(key, struct.pack(">q", counter), hashlib.sha1).digest()
    offset = digest[-1] & 0x0F
    code = (struct.unpack(">I", digest[offset:offset + 4])[0] & 0x7FFFFFFF) % 1000000
    return f"{code:06d}"

schritte = []

def titel(page, name):
    t = page.title()
    schritte.append({"schritt": name, "titel": t})
    return t

from playwright.sync_api import sync_playwright
with sync_playwright() as p:
    browser = p.chromium.launch()
    page = browser.new_page(viewport={"width": 1400, "height": 900})
    fehler = []
    page.on("pageerror", lambda exc: fehler.append(str(exc)))
    page.goto(base + "/ui/login", wait_until="domcontentloaded")
    page.fill('input[name="space"]', space)
    page.fill('input[name="password"]', password)
    page.fill('input[name="totp"]', totp_now(secret))
    page.click('form[action="/ui/login"] button[type="submit"]')
    page.wait_for_load_state("networkidle")
    page.wait_for_timeout(700)
    titel(page, "nach_dem_login")

    # In einen Space springen (die Spaces-Uebersicht)
    if page.locator(".overview__space-open").count() > 0:
        page.locator(".overview__space-open").first.click()
        page.wait_for_timeout(700)
    titel(page, "im_space")

    # Ein Item oeffnen
    diagnose = {
        "zeilen": page.locator(".list__row").count(),
        "view": page.evaluate("() => (document.getElementById('shell') || {}).dataset ? document.getElementById('shell').dataset.view : null"),
        "leertext": page.inner_text("#list")[:200] if page.locator("#list").count() else "",
    }
    if page.locator(".list__row").count() > 0:
        page.locator(".list__row").first.click()
        page.wait_for_timeout(900)
    titel(page, "im_item")
    diagnose["view_nach_klick"] = page.evaluate("() => (document.getElementById('shell') || {}).dataset ? document.getElementById('shell').dataset.view : null")

    # Die Einstellungen oeffnen und wieder schliessen
    page.click("#account-button")
    page.wait_for_timeout(500)
    titel(page, "im_einstellungen_panel")
    page.keyboard.press("Escape")
    page.wait_for_timeout(500)
    titel(page, "panel_geschlossen")

    # Zurueck in die Listenansicht.
    #
    # **ESC, nicht der Zurueck-Knopf:** der Knopf `#back-button` ist im Stylesheet
    # `display: none` — bei 1400 px ist er unsichtbar (gemessen: `is_visible()` false), und
    # der Weg aus der Item-Ansicht ist ESC (`app.js`: `else if (state.selectedId !== null)
    # Editor.closeEditor()`). Der Knopf bleibt im Markup, ist aber toter Code — eine
    # Beobachtung fuer die Sichtung (Block 7.4), kein Auftrag hier.
    diagnose["zurueck_knopf"] = {
        "anzahl": page.locator("#back-button").count(),
        "sichtbar": page.locator("#back-button").is_visible() if page.locator("#back-button").count() else None,
        "view_davor": page.evaluate("() => document.getElementById('shell').dataset.view"),
    }
    page.keyboard.press("Escape")
    page.wait_for_timeout(600)
    diagnose["view_danach"] = page.evaluate("() => document.getElementById('shell').dataset.view")
    titel(page, "nach_zurueck")

    browser.close()

print(json.dumps({"schritte": schritte, "seitenfehler": fehler, "diagnose": diagnose,
                  "item_titel": item_titel}, ensure_ascii=False))
'''


def _setup() -> dict:
    WEGWERF_ROOT.mkdir(parents=True, exist_ok=True)
    DATA_ROOT.mkdir(parents=True, exist_ok=True)
    if not DEK_FILE.exists():
        raw = secrets.token_bytes(32)
        DEK_FILE.write_text(base64.urlsafe_b64encode(raw).rstrip(b"=").decode("ascii") + "\n")
        os.chmod(DEK_FILE, 0o600)
    return _provision_user()


def _provision_user() -> dict:
    from authserver import passwords, totp
    from authserver.config import decode_data_encryption_key
    from authserver.secretbox import seal
    from authserver.store import AuthStore

    password = "wegwerf-b73-" + secrets.token_urlsafe(8)
    secret_b32 = totp.generate_secret()
    dek = decode_data_encryption_key(DEK_FILE.read_text().strip(), origin=str(DEK_FILE))
    store = AuthStore(str(AUTH_DB), now_fn=lambda: datetime.now(timezone.utc))
    store.upsert_user(
        space=SPACE,
        password_hash=passwords.hash_password(password),
        totp_secret_enc=seal(secret_b32.encode("ascii"), key=dek, aad=SPACE.encode("utf-8")),
        totp_alg="SHA1",
        totp_confirmed_at=datetime.now(timezone.utc),
        status="active",
    )
    return {"space": SPACE, "password": password, "secret": secret_b32}


def _seed_item() -> None:
    # **Determinismus:** die Wegwerf-Instanz wird wiederverwendet, der Datenbestand nicht.
    # Ohne das Leeren sammelt sich bei jedem Lauf ein Item mehr (gemessen: nach vier Läufen
    # vier Items mit demselben Titel), und der **Index** bleibt auf den gelöschten Items
    # stehen — die Übersicht zeigte danach gar keine Space mehr (gemessen: der leere
    # Space-Block). Ein Messgerät, das von der Zahl der Läufe abhängt, ist keines.
    shutil.rmtree(DATA_ROOT, ignore_errors=True)
    DATA_ROOT.mkdir(parents=True, exist_ok=True)
    env = os.environ.copy()
    env["SPACE_DATA_ROOT"] = str(DATA_ROOT)
    subprocess.run(
        [".venv/bin/python", "phase1_storage/scripts/space_cli.py", "--data-root", str(DATA_ROOT),
         "create", SPACE, "--type", "task", "--title", ITEM_TITEL],
        check=True, env=env, cwd=str(REPO_ROOT), stdout=subprocess.DEVNULL,
    )


def _serve() -> int:
    env = os.environ.copy()
    env["SPACE_DATA_ROOT"] = str(DATA_ROOT)
    env["SPACE_AUTH_DB"] = str(AUTH_DB)
    env["SPACE_PUBLIC_BASE_URL"] = "https://wegwerf-b73.invalid"
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


def _browser(user: dict) -> dict:
    skript = WEGWERF_ROOT / "browser_check.py"
    skript.write_text(BROWSER_SKILL, encoding="utf-8")
    e2e = Path.home() / ".claude-code-tools/e2e-venv/bin/python"
    proc = subprocess.run(
        [str(e2e), str(skript), BASE, user["space"], user["password"], user["secret"], ITEM_TITEL],
        cwd=str(REPO_ROOT), capture_output=True, text=True,
    )
    if proc.returncode != 0:
        return {"fehler": proc.stderr[-1500:], "schritte": []}
    return json.loads(proc.stdout.strip().splitlines()[-1])


def main(argv: list[str] | None = None) -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--gegenlauf", action="store_true",
                        help="den Aufruf `setViewTitle(item.title)` entfernen — die Probe "
                             "muss dann rot werden (der Tab bliebe beim Space-Namen)")
    args = parser.parse_args(argv)

    editor_js = REPO_ROOT / "phase5_ui/webui/static/js/editor.js"
    backup = None
    if args.gegenlauf:
        backup = editor_js.read_text(encoding="utf-8")
        editor_js.write_text(
            backup.replace("  setViewTitle(item.title);\n", ""), encoding="utf-8")

    user = _setup()
    _seed_item()
    pid = _serve()
    try:
        browser = _browser(user)
        schritte = browser.get("schritte", [])
        titel = {s["schritt"]: s["titel"] for s in schritte}
        erwartet = {
            "nach_dem_login": "Übersicht · sharefyx",
            "im_space": f"{SPACE} · sharefyx",
            "im_item": f"{ITEM_TITEL} · sharefyx",
            "im_einstellungen_panel": "Einstellungen · sharefyx",
            "panel_geschlossen": f"{ITEM_TITEL} · sharefyx",
            "nach_zurueck": f"{SPACE} · sharefyx",
        }
        befund = {k: {"erwartet": v, "gemessen": titel.get(k), "ok": titel.get(k) == v}
                  for k, v in erwartet.items()}
        ok = bool(schritte) and all(b["ok"] for b in befund.values()) and not browser.get("seitenfehler")
        ergebnis = {
            "probe": "p105_b7_titel",
            "instanz": {"basis": BASE, "data_root": str(DATA_ROOT), "pid": pid, "wegwerf": True},
            "befunde": befund,
            "schritte": schritte,
            "seitenfehler": browser.get("seitenfehler", []),
            "browser_fehler": browser.get("fehler"),
            "diagnose": browser.get("diagnose"),
            "alle_kriterien_erfuellt": ok,
        }
        if args.gegenlauf:
            ergebnis["gegenlauf"] = True
            ergebnis["hinweis"] = (
                "Gegenlauf: der Aufruf `setViewTitle(item.title)` war entfernt — die Probe "
                "muss jetzt ROT sein. Ist sie grün, prüft sie nicht das, was sie behauptet."
            )
            ergebnis["gegenlauf_erwartet_rot"] = not ok
        RESULT.write_text(json.dumps(ergebnis, indent=2, ensure_ascii=False) + "\n", encoding="utf-8")
        print(json.dumps(ergebnis, indent=2, ensure_ascii=False))
        if args.gegenlauf:
            return 0 if not ok else 1
        return 0 if ok else 1
    finally:
        _stop()
        if backup is not None:
            editor_js.write_text(backup, encoding="utf-8")


if __name__ == "__main__":
    raise SystemExit(main())
