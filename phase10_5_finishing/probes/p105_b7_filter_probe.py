#!/usr/bin/env python3
"""P10.5 Block 7, Schritte 7.6 (UI-6) und 7.7 (KA-5) — Zuständigen-Filter und `doing`-Hervorhebung.

Wegwerf-Instanz (Port **18792**, tmp-`DATA_ROOT`, PID-Datei, Hard Rule 9). Drei Aufgaben im Space
`alpha`: eine `doing` und `alpha` zugewiesen, eine `open` und `alpha` zugewiesen, eine `open`
ohne Zuständigen. Geprüft im Browser: (1) die Auswahl „Zugewiesen" ist sichtbar, (2) „alpha"
lässt weniger Zeilen stehen als „alle", „alle" stellt die Ausgangszahl wieder her, (3) der Chip
„In Arbeit" trägt `overview__space-count--doing` und die Akzentfarbe, die anderen nicht.

Gegenlauf `--gegenlauf`: die Zeile `params.set("assignee", …)` in `list.js` entfällt ⇒ rot.

Aufruf:  `.venv/bin/python phase10_5_finishing/probes/p105_b7_filter_probe.py [--gegenlauf]`
Ergebnis: `phase10_5_finishing/probes/p105_b7_filter_probe.json`
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
WEGWERF_ROOT = Path("/tmp/opencode/sharefyx-wegwerf-b76")
DATA_ROOT = WEGWERF_ROOT / "data"
AUTH_DB = WEGWERF_ROOT / "auth.sqlite3"
DEK_FILE = WEGWERF_ROOT / "auth-dek"
SERVE_PID = WEGWERF_ROOT / "serve.pid"
SERVE_LOG = WEGWERF_ROOT / "serve.log"
PORT = 18792
BASE = f"http://127.0.0.1:{PORT}"
SPACE = "alpha"
RESULT = Path(__file__).resolve().with_name("p105_b7_filter_probe.json")

BROWSER_SKILL = '''import json, sys, time, hmac, hashlib, struct, base64

base, space, password, secret = sys.argv[1:5]

def totp_now(secret_b32):
    key = base64.b32decode(secret_b32 + "=" * (-len(secret_b32) % 8))
    counter = int(time.time() // 30)
    digest = hmac.new(key, struct.pack(">q", counter), hashlib.sha1).digest()
    offset = digest[-1] & 0x0F
    code = (struct.unpack(">I", digest[offset:offset + 4])[0] & 0x7FFFFFFF) % 1000000
    return f"{code:06d}"

from playwright.sync_api import sync_playwright
out = {}
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
    page.wait_for_timeout(900)
    # KA-5: Chips der Uebersicht
    chips = page.evaluate("""() => Array.from(document.querySelectorAll('.overview__space-count')).map(c => ({
        bucket: c.dataset.bucket, doing: c.classList.contains('overview__space-count--doing'),
        color: getComputedStyle(c).color}))""")
    out["chips"] = chips
    out["accent"] = page.evaluate("""() => { const d = document.createElement('i'); d.style.color = 'var(--accent)';
        document.body.appendChild(d); const c = getComputedStyle(d).color; d.remove(); return c; }""")
    page.wait_for_selector(".overview__space-open", timeout=15000)
    page.locator(".overview__space-open").first.click()
    page.wait_for_timeout(900)
    out["zeilen_alle"] = page.locator(".list__row").count()
    # Der Eimer-Filter der Liste kann Zeilen ausblenden; wir zaehlen nur, wie sich die Zahl aendert.
    out["auswahl_da"] = page.locator("#list-assignee").count() == 1 and page.locator("#list-assignee").is_visible()
    out["optionen"] = page.evaluate("() => Array.from(document.querySelectorAll('#list-assignee option')).map(o => o.value)")
    page.select_option("#list-assignee", "alpha")
    page.wait_for_timeout(900)
    out["zeilen_alpha"] = page.locator(".list__row").count()
    page.select_option("#list-assignee", "")
    page.wait_for_timeout(900)
    out["zeilen_wieder_alle"] = page.locator(".list__row").count()
    # KA-5 Karte: Ringpixel in der Akzentfarbe zaehlen (Fuellung der eigenen Knoten ist #4A93F0, Abstand 12 in R).
    page.keyboard.press("Escape")
    page.wait_for_timeout(300)
    page.locator("#home-button").click() if page.locator("#home-button").count() else None
    page.wait_for_timeout(1200)
    out["ring_pixel"] = page.evaluate("""() => {
        const c = document.getElementById('overview-graph-canvas'); if (!c) return -1;
        const d = c.getContext('2d').getImageData(0, 0, c.width, c.height).data; let n = 0;
        for (let i = 0; i < d.length; i += 4)
          if (d[i+3] > 250 && Math.abs(d[i]-62) <= 2 && Math.abs(d[i+1]-141) <= 2 && Math.abs(d[i+2]-243) <= 2) n++;
        return n; }""")
    out["seitenfehler"] = fehler
    browser.close()
print(json.dumps(out, ensure_ascii=False))
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

    password = "wegwerf-b76-" + secrets.token_urlsafe(8)
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
    shutil.rmtree(DATA_ROOT, ignore_errors=True)
    DATA_ROOT.mkdir(parents=True, exist_ok=True)
    code = (
        "import sys; sys.path.insert(0, 'phase1_storage')\n"
        "from storage.store import Store\n"
        f"s = Store({str(DATA_ROOT)!r}, git=False)\n"
        f"for titel, status, wer in [('A doing', 'doing', {SPACE!r}), ('B offen', 'open', {SPACE!r}), ('C offen', 'open', '')]:\n"
        f"    i = s.create({SPACE!r}, type='task', title=titel)\n"
        "    s.update(i.id, version=i.version, status=status, assignee=wer)\n"
    )
    subprocess.run([".venv/bin/python", "-c", code], check=True, cwd=str(REPO_ROOT),
                   env={**os.environ, "PYTHONPATH": str(REPO_ROOT / "phase1_storage")})


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
        [str(e2e), str(skript), BASE, user["space"], user["password"], user["secret"]],
        cwd=str(REPO_ROOT), capture_output=True, text=True,
    )
    if proc.returncode != 0:
        return {"fehler": proc.stderr[-1500:], "schritte": []}
    return json.loads(proc.stdout.strip().splitlines()[-1])


def main(argv: list[str] | None = None) -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--gegenlauf", nargs="?", const="filter", choices=["filter", "ring"],
                        help="filter: die assignee-Zeile in list.js entfernen · ring: den doing-Ring in "
                             "graph.js abschalten — die Probe muss jeweils rot werden")
    args = parser.parse_args(argv)

    if args.gegenlauf == "ring":
        datei = REPO_ROOT / "phase5_ui/webui/static/js/graph.js"
        alt, neu = '    if (n.status === "doing") {', '    if (false && n.status === "doing") {'
    else:
        datei = REPO_ROOT / "phase5_ui/webui/static/js/list.js"
        alt, neu = '  if (state.assignee && !isGlobalScope()) params.set("assignee", state.assignee);\n', ""
    backup = None
    if args.gegenlauf:
        backup = datei.read_text(encoding="utf-8")
        assert alt in backup
        datei.write_text(backup.replace(alt, neu), encoding="utf-8")

    user = _setup()
    _seed_item()
    pid = _serve()
    try:
        b = _browser(user)
        chips = {c["bucket"]: c for c in b.get("chips", [])}
        befund = {
            "auswahl_sichtbar": b.get("auswahl_da") is True,
            "filter_verengt": 0 < b.get("zeilen_alpha", 0) < b.get("zeilen_alle", 0),
            "alle_stellt_her": b.get("zeilen_wieder_alle") == b.get("zeilen_alle") and b.get("zeilen_alle", 0) > 0,
            "chip_doing_hervorgehoben": bool(chips.get("doing", {}).get("doing")) and chips["doing"]["color"] == b.get("accent"),
            "karten_ring_gezeichnet": b.get("ring_pixel", 0) >= 20,
            "andere_chips_gedaempft": all(not c["doing"] and c["color"] != b.get("accent") for k, c in chips.items() if k != "doing") and len(chips) > 1,
        }
        ok = all(befund.values()) and not b.get("seitenfehler") and "fehler" not in b
        ergebnis = {"probe": "p105_b7_filter", "instanz": {"basis": BASE, "pid": pid, "wegwerf": True},
                    "befund": befund, "messung": b, "alle_kriterien_erfuellt": ok}
        if args.gegenlauf:
            ergebnis["gegenlauf"] = True
            ergebnis["gegenlauf_erwartet_rot"] = not ok
        RESULT.write_text(json.dumps(ergebnis, indent=2, ensure_ascii=False) + "\n", encoding="utf-8")
        print(json.dumps(ergebnis, indent=2, ensure_ascii=False))
        return (0 if not ok else 1) if args.gegenlauf else (0 if ok else 1)
    finally:
        _stop()
        if backup is not None:
            datei.write_text(backup, encoding="utf-8")


if __name__ == "__main__":
    raise SystemExit(main())
