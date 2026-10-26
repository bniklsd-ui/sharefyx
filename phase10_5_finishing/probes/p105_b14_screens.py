#!/usr/bin/env python3
"""P10.5 Block 13 — die **Sichtungsbilder** fuer den Nikinger.

Drei Auftraege, fuenf Bilder (Wegwerf-Instanz, eigener Port, tmp-`DATA_ROOT`, eigener
Datenwurzel-Baum je Lauf, Stopp nur ueber die PID-Datei — Hard Rule 9):

| Bild | was |
|---|---|
| `p105_b14_01_knopfleiste.png` | die neue Leiste (Word-Reihenfolge, Gruppen, Trenner) |
| `p105_b14_02_groessen.png` | der Live-Editor: `klein` / normal / `gross` |
| `p105_b14_03_map_ganz.png` | die **ganze** Gehirnkarte (P10.5-37) |
| `p105_b14_04_map_fokus.png` | die Karte im Fokus (Ringe, Lappen, Zellen) |
| `p105_b14_05_map_seite.png` | die ganze Seite mit der Karte (Kontext) |

**Die ganze Karte:** die frueheren Bilder (P10.5 Block 8) zeigten den **Ausschnitt**, den
das Panel am Bildschirmrand zeigt — der Nikinger hat genau das verlangt (Auftrag 4:
„die ganze Gehirnkarte, nicht nur der Ausschnitt im Uebersichtspanel"). Die Karte ist
**frei zoom- und verschiebbar** (`graph.js`: Rad = Zoom 50 %..250 %, Doppelklick = Ansicht
zurueck). Das Bild zoomt deshalb auf die **kleinste** Stufe (50 %) und nutzt ein
**grosses Fenster** (1920x1200) — so passt die Welt der Knoten in das Bild.

Der Browser-Teil laeuft im **e2e-venv** (dort liegt Playwright) — als eigenes Skript, das
seine Werte ueber die Kommandozeile bekommt (kein `.format()` auf dem Quelltext).

Aufruf:  `.venv/bin/python phase10_5_finishing/probes/p105_b14_screens.py`
"""
from __future__ import annotations

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
WEGWERF_ROOT = Path("/tmp/opencode/sharefyx-wegwerf-b14")
DATA_ROOT = WEGWERF_ROOT / ("data-%d" % os.getpid())
AUTH_DB = WEGWERF_ROOT / "auth.sqlite3"
DEK_FILE = WEGWERF_ROOT / "auth-dek"
SERVE_PID = WEGWERF_ROOT / "serve.pid"
SERVE_LOG = WEGWERF_ROOT / "serve.log"
SHOT_DIR = REPO_ROOT / "docs" / "screenshots"
SPACE = "alpha"
PORT = 0
BASE = ""

# Der Inhalt, an dem die **Groessen** sichtbar werden: drei Zeilen, jede mit einer
# anderen Stufe. Die Reihenfolge der Klassen ist im Text **frei** (Farbe und Groesse
# duerfen in beiden Richtungen stehen) — das prueft `test_knopfleiste_word.py`.
BODY = """# Formate

[Normale Schrift]{.normal}

[Kleine Schrift]{.klein}

[Groessere Schrift]{.gross}

[Rot und klein]{.rot .klein}
"""


def _freier_port() -> int:
    """Ein freier TCP-Port auf dem Loopback (Bind auf 0, dann schliessen)."""
    import socket
    with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
        s.bind(("127.0.0.1", 0))
        return int(s.getsockname()[1])


def _setup() -> dict:
    WEGWERF_ROOT.mkdir(parents=True, exist_ok=True)
    DATA_ROOT.mkdir(parents=True, exist_ok=True)
    if not DEK_FILE.exists():
        raw = secrets.token_bytes(32)
        DEK_FILE.write_bytes(base64.urlsafe_b64encode(raw).rstrip(b"=") + b"\n")
        os.chmod(DEK_FILE, 0o600)
    from authserver import passwords, totp
    from authserver.config import decode_data_encryption_key
    from authserver.secretbox import seal
    from authserver.store import AuthStore

    password = "wegwerf-b14-" + secrets.token_urlsafe(8)
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
    store.set_totp_counter(SPACE, 0)
    return {"space": SPACE, "password": password, "secret": secret_b32}


def _seed() -> None:
    """Die Items: das **Formate-Item** (fuer den Editor) und ein kleines Netz (fuer die
    Karte) — Knoten mit Ordner, Tags und Verweisen untereinander."""
    shutil.rmtree(DATA_ROOT, ignore_errors=True)
    DATA_ROOT.mkdir(parents=True, exist_ok=True)
    code = (
        "import sys; sys.path.insert(0, 'phase1_storage')\n"
        "from storage.store import Store\n"
        f"s = Store({str(DATA_ROOT)!r}, git=False)\n"
        f"s.create({SPACE!r}, type='task', title='Formate', body={BODY!r}, tags=['format'])\n"
        "netz = []\n"
        "titel = ['Projekt A', 'Projekt B', 'Aufgabe eins', 'Aufgabe zwei', 'Notiz drei',\n"
        "         'Notiz vier', 'Idee fuenf', 'Idee sechs', 'Frage sieben', 'Antwort acht',\n"
        "         'Tabelle neun', 'Bild zehn']\n"
        "for n, t in enumerate(titel, 1):\n"
        f"    netz.append(s.create({SPACE!r}, type='task', title=t, folder='ordner-%d' % (n % 3 + 1),\n"
        "                          tags=['netz', 'gruppe-%d' % (n % 2 + 1)]).id)\n"
        "for k, ziel in enumerate(netz):\n"
        "    s.update(ziel, version=1, links=[netz[(k + 1) % len(netz)], netz[(k + 3) % len(netz)]])\n"
    )
    subprocess.run([".venv/bin/python", "-c", code], check=True, cwd=str(REPO_ROOT),
                   env={**os.environ, "PYTHONPATH": str(REPO_ROOT / "phase1_storage")})


def _serve() -> int:
    env = os.environ.copy()
    env["SPACE_DATA_ROOT"] = str(DATA_ROOT)
    env["SPACE_AUTH_DB"] = str(AUTH_DB)
    env["SPACE_PUBLIC_BASE_URL"] = "https://wegwerf-b14.invalid"
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
        for _ in range(40):
            time.sleep(0.25)
            try:
                os.kill(pid, 0)
            except ProcessLookupError:
                return
        print(f"WARNUNG: Wegwerf-Server {pid} beendete sich nicht — SIGKILL.", file=sys.stderr)
        os.kill(pid, signal.SIGKILL)
    except ProcessLookupError:
        pass


# Der Browser-Teil als **eigenes Skript** (Playwright liegt im e2e-venv, nicht im
# Projekt-venv). Die Werte kommen ueber die Kommandozeile — kein `.format()` auf einem
# Quelltext, in dem JavaScript steht.
BROWSER_SKILL = '''import base64, hashlib, hmac, struct, sys, time
from pathlib import Path

from playwright.sync_api import sync_playwright

BASE, SPACE, PASSWORD, SECRET = sys.argv[1:5]
SHOTS = Path(sys.argv[5])


def totp_now(secret_b32):
    key = base64.b32decode(secret_b32 + "=" * (-len(secret_b32) % 8))
    digest = hmac.new(key, struct.pack(">q", int(time.time() // 30)), hashlib.sha1).digest()
    offset = digest[-1] & 0x0F
    code = (struct.unpack(">I", digest[offset:offset + 4])[0] & 0x7FFFFFFF) % 1000000
    return f"{code:06d}"


fehler = []
with sync_playwright() as p:
    br = p.chromium.launch()
    page = br.new_page(viewport={"width": 1400, "height": 900})
    page.on("pageerror", lambda e: fehler.append(str(e)))
    page.goto(BASE + "/ui/login", wait_until="domcontentloaded")
    page.fill('input[name="space"]', SPACE)
    page.fill('input[name="password"]', PASSWORD)
    page.fill('input[name="totp"]', totp_now(SECRET))
    page.click('form[action="/ui/login"] button[type="submit"]')
    page.wait_for_selector("#shell", timeout=30000)
    page.wait_for_timeout(1500)

    # -- 1) Die Version im Rail-Kopf ------------------------------------------------
    print("Version:", page.locator(".rail__version").inner_text())
    page.locator(".rail__brand").screenshot(path=str(SHOTS / "p105_b14_01_version.png"))

    # -- 2) Die Leiste ohne Rohtext-Knopf --------------------------------------------
    page.wait_for_selector(".overview__space-open", timeout=20000)
    page.locator(".overview__space-open").first.click()
    page.wait_for_timeout(1500)
    page.locator(".list__row", has_text="Formate").first.click()
    page.wait_for_selector(".CodeMirror", timeout=30000)
    page.wait_for_timeout(1800)
    print("Rohtext-Knoepfe:", page.locator("#toggle-preview").count(),
          "| Text 'Rohtext' in der Leiste:", page.locator("#editor-toolbar", has_text="Rohtext").count())
    page.locator("#editor-toolbar").screenshot(path=str(SHOTS / "p105_b14_02_knopfleiste.png"))

    # -- 3) Einstellungen: Auswahl bleibt in Stufe 2 (Menue) UND Stufe 3 (Space-Zeile) --
    page.click("#account-button")
    page.wait_for_selector("#settings-menu", state="visible")
    page.click("#account-manage-spaces")
    page.wait_for_selector(".settings-space-row", timeout=15000)
    page.wait_for_timeout(500)
    zeilen = page.locator(".settings-space-row")
    print("Space-Zeilen:", zeilen.count())
    page.locator(".settings-chain").screenshot(path=str(SHOTS / "p105_b14_03_spaces_liste.png"))
    zeilen.first.click()
    page.wait_for_selector("#settings-space-detail", state="visible", timeout=15000)
    page.wait_for_timeout(600)
    print("aria-current Menue:", page.locator("#account-manage-spaces").get_attribute("aria-current"),
          "| Space-Zeile:", zeilen.first.get_attribute("aria-current"))
    page.locator(".settings-chain").screenshot(path=str(SHOTS / "p105_b14_04_spaces_detail.png"))
    # Detail schliessen: die Markierung der Zeile faellt, die des Menues bleibt
    page.click("#space-detail-close")
    page.wait_for_timeout(400)
    print("nach Zurueck -> Menue:", page.locator("#account-manage-spaces").get_attribute("aria-current"),
          "| Space-Zeile:", zeilen.first.get_attribute("aria-current"))

    print(f"Seitenfehler: {fehler}")
    br.close()
'''


def main() -> int:
    global PORT, BASE
    SHOT_DIR.mkdir(parents=True, exist_ok=True)
    PORT = _freier_port()
    BASE = f"http://127.0.0.1:{PORT}"
    creds = _setup()
    _seed()
    _serve()
    skript = WEGWERF_ROOT / "screens_b14.py"
    skript.write_text(BROWSER_SKILL, encoding="utf-8")
    e2e = Path.home() / ".claude-code-tools/e2e-venv/bin/python"
    try:
        proc = subprocess.run(
            [str(e2e), str(skript), BASE, creds["space"], creds["password"],
             creds["secret"], str(SHOT_DIR)],
            cwd=str(REPO_ROOT), capture_output=True, text=True, timeout=240,
        )
        print(proc.stdout.strip()[-2000:])
        if proc.returncode != 0:
            print(proc.stderr.strip()[-3000:], file=sys.stderr)
            return 1
    finally:
        _stop()
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
