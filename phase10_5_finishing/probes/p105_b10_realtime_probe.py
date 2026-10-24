#!/usr/bin/env python3
"""P10.5 Block 10, Schritt 10.5 — LG-1 (Volltext) und LG-2 (Realtime) an der Wegwerf-Instanz.

**Wegwerf (Plan §2.3):** Port **18810** (eigener Port, damit keine andere Probe hängt),
eigene Wurzel `/tmp/opencode/sharefyx-wegwerf-p105-b10`, tmp-`DATA_ROOT`, tmp-`auth.sqlite3`,
File-Keyring, Umgebung ohne `SHAREFYX_*`/`SFX_*`, Stopp **nur** über die PID-Datei
(Hard Rule 9: nie `pkill -f`, nie der systemd-Dienst).

**Zwei Principale:** `alpha` (der Browser) und `beta` (der Gegenlauf). Beide sind
Home-Spaces **ohne** Freigabe — `alpha` sieht `beta` nicht. Genau darum ist der Gegenlauf
messbar: ein Write in `beta` darf bei `alpha` **kein** Ereignis auslösen.

**Was gemessen wird (Abnahme P10.5-45, 46, 47, 48):**

| # | Zelle | Erwartung |
|---|---|---|
| 1 | Volltext **ohne** Schalter | ein Marker im **Text** wird **nicht** gefunden |
| 2 | Volltext **mit** Schalter | derselbe Marker wird gefunden |
| 3 | Ereignis nach einem Write | der Browser bekommt ein `changed`-Ereignis |
| 4 | **Latenz** | die neue Zeile ist **≤ 2 s** nach dem Write sichtbar |
| 5 | **P10.5-S**: geänderter Editor | der getippte Text steht **noch** drin, das Band erscheint |
| 6 | **Gegenlauf**: unsichtbarer Space | ein Write in `beta` löst **kein** Ereignis aus |
| 7 | **Shutdown** mit offenem Stream | der Prozess ist **≤ 10 s** nach SIGTERM weg |

**Wie gemessen wird.** Der Browser zählt die `changed`-Ereignisse selbst: ein Init-Script
umhüllt `EventSource`, **bevor** die App lädt, und schreibt Zeitstempel (Wanduhr, `Date.now()`)
in ein Fenster. Der Python-Prozess misst denselben Clock — die Latenz ist die Differenz
zwischen „Write abgeschickt" und „Zeile sichtbar". Der Server wird **nicht** angefasst: der
Write läuft über die Web-API mit einer echten Sitzung (CSRF-Token inklusive).

**Die Reihenfolge ist Teil der Messung.** Der fremde Write auf das offene Item kommt
**nach** dem Tippen (sonst wäre der Editor gar nicht geändert) und **vor** der Latenz-Messung
gemessen wird der Write, der eine **neue Zeile** erzeugt. Der Ablauf (Browser/Python
abwechselnd, über Dateien als Flag):

```
Browser  → session.json  (Sitzung + CSRF für den Python-Prozess)
Browser  → ready1.flag  (Volltext gemessen, Liste sichtbar, Zähler läuft)
Python   → write1.done  (neue Aufgabe in alpha)
Browser  → phase1.json  (Latenz + Ereignis gezählt)
Browser  → ready2.flag  (Item offen, Text getippt — der Editor ist jetzt geändert)
Python   → write2.done  (fremder Write auf genau dieses Item)
Browser  → phase2.json  (Band sichtbar? Text erhalten?)
Python   → write3.done  (Write in beta — für alpha unsichtbar)
Browser  → phase3.json  (Ereigniszähler unverändert?)
Python   → SIGTERM      (Shutdown-Messung mit offenem Stream)
Python   → shutdown.done
```

**Datierte Abweichung vom Plan (2026-10-24).** Der Plan (§Block 10, Schritt 10.5) nennt einen
„MCP-Write". Die Probe schreibt über die **Web-API** desselben Servers: nach dem Adapter ist
der Serverpfad derselbe (`Store.create()` → Commit → HEAD → Ereignis), und der MCP-Weg
bräuchte den OAuth-Dance (DCR + Consent), der nichts am Realtime-Pfad prüft. Der **Gegenlauf**
(unsichtbarer Space) braucht ohnehin einen zweiten Principalen — und der wird hier über die
Web-API bedient.

**TLS.** `require_csrf()` vergleicht den Origin-Header gegen `SPACE_PUBLIC_BASE_URL`, und
`_validate_base_url()` erzwingt https — ohne TLS wäre **kein** Schreibvorgang möglich
(derselbe Weg wie in `phase10_inventory/probes/p10_wegwerf.py`).

Aufruf: `.venv/bin/python phase10_5_finishing/probes/p105_b10_realtime_probe.py [--gegenlauf]`
Ergebnis: `phase10_5_finishing/probes/p105_b10_realtime.json`
"""
from __future__ import annotations

import argparse
import base64
import json
import os
import re
import secrets
import shutil
import signal
import subprocess
import sys
import time
from datetime import datetime, timezone
from pathlib import Path

REPO_ROOT = Path(__file__).resolve().parents[2]
WEGWERF_ROOT = Path("/tmp/opencode/sharefyx-wegwerf-p105-b10")
DATA_ROOT = WEGWERF_ROOT / "data"
AUTH_DB = WEGWERF_ROOT / "auth.sqlite3"
DEK_FILE = WEGWERF_ROOT / "auth-dek"
SERVE_PID = WEGWERF_ROOT / "serve.pid"
SERVE_LOG = WEGWERF_ROOT / "serve.log"
PORT = 18810
# **TLS statt http — kein Kosmetikposten:** `require_csrf()` vergleicht den Origin-Header
# gegen `SPACE_PUBLIC_BASE_URL`, und `_validate_base_url()` erzwingt https. Mit
# `https://127.0.0.1:18810` + selbstsigniertem Zertifikat stimmen alle drei Seiten
# überein — sonst wäre kein einziger Schreibvorgang möglich.
BASE = f"https://127.0.0.1:{PORT}"
TLS_KEY = WEGWERF_ROOT / "key.pem"
TLS_CERT = WEGWERF_ROOT / "cert.pem"
SPACE = "alpha"
FREMD = "beta"
RESULT = Path(__file__).with_name("p105_b10_realtime.json")
#: Der Gegenlauf schreibt in eine **eigene** Datei: sonst überschriebe er das grüne
#: Ergebnis (und die Akte im Repo trüge plötzlich einen roten Lauf).
RESULT_GEGENLAUF = Path(__file__).with_name("p105_b10_realtime_gegenlauf.json")

#: Der Marker steht im **Text** (nicht im Titel) — die Volltext-Suche findet ihn nur mit
#: dem Schalter.
MARKER_BODY = "EinBodyMarkerXYZ"
#: Der Titel der neu angelegten Aufgabe. Die **Zeile** in der Liste zeigt den Titel, nicht
#: den Text — deshalb wird die Latenz am Titel gemessen.
TITEL_LIVE = "Realtime-Aufgabe"
#: Das Item, das der Browser öffnet und bearbeitet.
TITEL_EDITOR = "Editor-Item"
#: Der getippte Text — er muss nach dem fremden Write **noch** dastehen (P10.5-S).
TIPP_TEXT = "Getippt von mir"

#: Die Frist der Abnahme P10.5-46: eine Änderung ist in **zwei Sekunden** sichtbar.
LATENZ_MAX_MS = 2000
#: Die Frist der Abnahme P10.5-48: der Shutdown mit offenem Stream dauert höchstens 10 s.
SHUTDOWN_MAX_S = 10


def log(text: str) -> None:
    print(text, file=sys.stderr, flush=True)


SERVE_TLS_LAUNCHER = '''"""Der **Produktiv**-Start (`phase2_mcp/scripts/serve.py`), plus TLS.

**Warum nicht eine Kopie des App-Aufbaus:** die Abnahme P10.5-48 misst den Shutdown mit
offenem Stream — und die Frist dafür steht im Produktivcode
(`serve.py :: timeout_graceful_shutdown=5`). Eine Kopie des Startskripts würde den Wert
mitkopieren oder weglassen; weglassen hieße: die Probe misst eine Attrappe und meldet
grün, obwohl der Produktivpfad unbegrenzt warten würde (genau der Fehlermodus, den
dieses Repo mehrfach als „ein Wächter, der etwas anderes prüft als er behauptet"
notiert hat). Deshalb ruft der Launcher **das Produktivskript** auf und ergänzt nur die
beiden TLS-Parameter — an `uvicorn.run`, das `serve.py` selbst aufruft.
"""
import os, sys
sys.path.insert(0, os.environ["REPO_ROOT"])
import uvicorn
from phase2_mcp.scripts import serve

_orig_run = uvicorn.run


def _run(*args, **kwargs):
    kwargs["ssl_keyfile"] = os.environ["TLS_KEY"]
    kwargs["ssl_certfile"] = os.environ["TLS_CERT"]
    return _orig_run(*args, **kwargs)


uvicorn.run = _run
serve.main(["--allowed-host", "127.0.0.1"])
'''


# --- Browser-Skript ----------------------------------------------------------------------

BROWSER_SKILL = '''import json, sys, time, hmac, hashlib, struct, base64
from pathlib import Path

base, space, password, secret, workdir, marker_body, titel_live, titel_editor = sys.argv[1:9]
work = Path(workdir)

def totp_now(secret_b32):
    key = base64.b32decode(secret_b32 + "=" * (-len(secret_b32) % 8))
    counter = int(time.time() // 30)
    digest = hmac.new(key, struct.pack(">q", counter), hashlib.sha1).digest()
    offset = digest[-1] & 0x0F
    code = (struct.unpack(">I", digest[offset:offset + 4])[0] & 0x7FFFFFFF) % 1000000
    return f"{code:06d}"

def wait_file(name, seconds):
    """Wartet auf eine Datei (die der Python-Prozess schreibt)."""
    ende = time.time() + seconds
    while time.time() < ende:
        if (work / name).exists():
            return True
        time.sleep(0.02)
    return False

from playwright.sync_api import sync_playwright

out = {}
with sync_playwright() as p:
    browser = p.chromium.launch()
    # Das Wegwerf-Zertifikat ist selbstsigniert (CN/SAN 127.0.0.1).
    context = browser.new_context(ignore_https_errors=True, viewport={"width": 1400, "height": 900})
    page = context.new_page()
    fehler = []
    page.on("pageerror", lambda exc: fehler.append(str(exc)))
    # Der EventSource wird umhüllt, **bevor** die App lädt: so zählt der Browser jedes
    # "changed"-Ereignis selbst, mit Wanduhr-Zeitstempel (Date.now()).
    page.add_init_script("""
      (function () {
        const Orig = window.EventSource;
        function Patched(url, opts) {
          const es = new Orig(url, opts);
          window.__es = es;
          window.__changed = 0;
          window.__changedAt = [];
          es.addEventListener("changed", function () {
            window.__changed++;
            window.__changedAt.push(Date.now());
          });
          return es;
        }
        Patched.OPEN = Orig.OPEN;
        Patched.CONNECTING = Orig.CONNECTING;
        Patched.CLOSED = Orig.CLOSED;
        window.EventSource = Patched;
      })();
    """)
    page.goto(base + "/ui/login", wait_until="domcontentloaded")
    page.fill('input[name="space"]', space)
    page.fill('input[name="password"]', password)
    page.fill('input[name="totp"]', totp_now(secret))
    page.click('form[action="/ui/login"] button[type="submit"]')
    # **Kein "networkidle"**: der Ereignis-Stream hält die Verbindung offen -- die Seite
    # wird nie ruhig. Gewartet wird auf die App-Shell.
    page.wait_for_selector("#shell", timeout=30000)
    page.wait_for_timeout(1200)

    # **Die Sitzung geht an den Python-Prozess.** Grund: der Login verbraucht den
    # TOTP-Zähler (Replay-Schutz) -- ein zweiter Login als `alpha` (der Python-Prozess
    # braucht die Sitzung für die API-Writes) würde mit demselben Code abgewiesen.
    cookies = page.context.cookies()
    (work / "session.json").write_text(json.dumps({
        "cookie": "; ".join(f"{c['name']}={c['value']}" for c in cookies),
        "csrf": page.evaluate("() => sessionStorage.getItem('sfx:csrf')"),
    }))

    # -- LG-1: der Volltext-Schalter ----------------------------------------------------
    out["schalter_vorhanden"] = page.locator("#search-in-body").count() == 1
    page.wait_for_selector(".overview__space-open", timeout=20000)
    page.locator(".overview__space-open").first.click()
    page.wait_for_timeout(900)
    page.fill("#search-input", marker_body)
    page.wait_for_timeout(900)
    out["treffer_ohne_schalter"] = page.locator(".list__row").count()
    page.check("#search-in-body")
    page.wait_for_timeout(900)
    out["treffer_mit_schalter"] = page.locator(".list__row").count()
    page.uncheck("#search-in-body")
    page.fill("#search-input", "")
    page.wait_for_timeout(900)

    # -- LG-2, Phase 1: die Latenz ------------------------------------------------------
    # Der Zähler für die neue Zeile: er merkt sich, **wann** sie sichtbar wurde. Die
    # Zeile zeigt den **Titel** (nicht den Text) -- deshalb wird der Titel gesucht.
    page.evaluate("""() => {
      window.__neu = null;
      const treffer = %s;
      const timer = setInterval(function () {
        const rows = Array.from(document.querySelectorAll(".list__row"));
        const hit = rows.find(function (r) {
          return r.textContent.indexOf(treffer) !== -1;
        });
        if (hit) { window.__neu = Date.now(); clearInterval(timer); }
      }, 20);
    }""" % json.dumps(titel_live))
    (work / "ready1.flag").write_text("ready")
    wait_file("write1.done", 90)
    page.wait_for_timeout(600)
    out["stream_ready_state"] = page.evaluate("() => window.__es ? window.__es.readyState : -1")
    out["erscheint_at"] = page.evaluate("() => window.__neu")
    out["changed_nach_write1"] = page.evaluate("() => window.__changed")
    out["changed_at_nach_write1"] = page.evaluate("() => window.__changedAt")
    (work / "phase1.json").write_text(json.dumps(out))

    # -- P10.5-S: der Editor wird nie überschrieben ------------------------------------
    # **Erst jetzt** wird das Item geöffnet und verändert -- der fremde Write kommt
    # danach (sonst wäre der Editor gar nicht geändert).
    page.locator(".list__row", has_text=titel_editor).first.click()
    page.wait_for_timeout(1200)
    out["editor_offen"] = page.locator("#detail-editor").is_visible()
    # Der Editor öffnet in der **Vorschau** (Vorgabe seit P5) -- zum Tippen muss der
    # Umschalter gedrückt werden, sonst ist die Textarea unsichtbar.
    if page.locator("#toggle-preview").count():
        page.click("#toggle-preview")
        page.wait_for_timeout(500)
    out["textarea_sichtbar"] = page.locator("#editor-textarea").is_visible()
    out["version_vorher"] = page.locator("#version-band-number").inner_text()
    page.fill("#editor-textarea", "Getippt von mir")
    page.wait_for_timeout(600)
    out["version_ungespeichert"] = page.locator("#version-band-number").inner_text()
    out["dirty_vorher"] = page.evaluate("() => window.__changed")
    (work / "ready2.flag").write_text("ready")
    wait_file("write2.done", 90)
    page.wait_for_timeout(2500)
    out["band_sichtbar"] = page.locator("#editor-changed").is_visible()
    out["band_text"] = page.locator("#editor-changed-text").inner_text()
    out["text_erhalten"] = page.input_value("#editor-textarea")
    out["changed_nach_write2"] = page.evaluate("() => window.__changed")
    (work / "phase2.json").write_text(json.dumps(out))

    # -- Gegenlauf: der Write im unsichtbaren Space --------------------------------------
    wait_file("write3.done", 90)
    page.wait_for_timeout(3000)
    out["changed_nach_write3"] = page.evaluate("() => window.__changed")
    out["seitenfehler"] = fehler
    (work / "phase3.json").write_text(json.dumps(out))

    # Der Stream bleibt offen, bis der Server weg ist (die Shutdown-Messung braucht
    # einen offenen Stream).
    wait_file("shutdown.done", 90)
    browser.close()
print(json.dumps(out, ensure_ascii=False))
'''


# --- Setup --------------------------------------------------------------------------------

def _provision(space: str) -> dict:
    """Legt einen Principalen in der tmp-`auth.sqlite3` an (Technik 4, zwei Principale)."""
    from authserver import passwords, totp
    from authserver.config import decode_data_encryption_key
    from authserver.secretbox import seal
    from authserver.store import AuthStore

    password = "wegwerf-b10-" + secrets.token_urlsafe(8)
    secret_b32 = totp.generate_secret()
    dek = decode_data_encryption_key(DEK_FILE.read_text().strip(), origin=str(DEK_FILE))
    store = AuthStore(str(AUTH_DB), now_fn=lambda: datetime.now(timezone.utc))
    store.upsert_user(
        space=space,
        password_hash=passwords.hash_password(password),
        totp_secret_enc=seal(secret_b32.encode("ascii"), key=dek, aad=space.encode("utf-8")),
        totp_alg="SHA1",
        totp_confirmed_at=datetime.now(timezone.utc),
        status="active",
    )
    return {"space": space, "password": password, "secret": secret_b32}


def _totp(secret_b32: str) -> str:
    from authserver import totp

    return totp.totp_at(secret_b32, int(time.time() // 30), algo="SHA1")


def _setup() -> tuple[dict, dict]:
    shutil.rmtree(WEGWERF_ROOT, ignore_errors=True)
    WEGWERF_ROOT.mkdir(parents=True, exist_ok=True)
    DATA_ROOT.mkdir(parents=True, exist_ok=True)
    raw = secrets.token_bytes(32)
    DEK_FILE.write_text(base64.urlsafe_b64encode(raw).rstrip(b"=").decode("ascii") + "\n")
    os.chmod(DEK_FILE, 0o600)
    alpha = _provision(SPACE)
    beta = _provision(FREMD)
    _seed()
    return alpha, beta


def _seed() -> None:
    """Seed **mit** Git — der Ereignis-Feed liest den HEAD, und der erste Write nach dem
    Serverstart muss gegen einen echten Commit diffen können."""
    code = (
        "import sys; sys.path.insert(0, 'phase1_storage')\n"
        "from storage.store import Store\n"
        f"s = Store({str(DATA_ROOT)!r}, git=True)\n"
        # Eine Aufgabe, deren **Text** den Marker trägt (der Titel trägt ihn nicht).
        f"s.create({SPACE!r}, type='task', title='Volltext-Aufgabe', "
        f"body='Der Marker {MARKER_BODY} steckt im Text.')\n"
        # Die Aufgabe, die der Browser später öffnet und bearbeitet.
        f"s.create({SPACE!r}, type='task', title='{TITEL_EDITOR}', body='Urspruenglich.')\n"
    )
    subprocess.run(
        [".venv/bin/python", "-c", code], check=True, cwd=str(REPO_ROOT),
        env={**os.environ, "PYTHONPATH": str(REPO_ROOT / "phase1_storage")},
    )


def _port_frei() -> bool:
    import socket

    with socket.socket() as sock:
        sock.settimeout(0.5)
        return sock.connect_ex(("127.0.0.1", PORT)) != 0


def _serve() -> subprocess.Popen:
    if not _port_frei():
        raise SystemExit(
            f"Port {PORT} ist belegt — vermutlich eine hängengebliebene eigene Wegwerf-"
            "Instanz. Sie wird **nicht** per Regex gesucht (Hard Rule 9): bitte über die "
            "PID-Datei unter /tmp/opencode/sharefyx-wegwerf-p105-b10/serve.pid beenden."
        )
    env = os.environ.copy()
    for name in list(env):
        if name.startswith("SHAREFYX_") or name.startswith("SFX_"):
            env.pop(name)
    env["SPACE_DATA_ROOT"] = str(DATA_ROOT)
    env["SPACE_AUTH_DB"] = str(AUTH_DB)
    # Der Wert, gegen den `require_csrf` den Browser-Origin vergleicht — exakt die URL,
    # die der Browser aufruft.
    env["SPACE_PUBLIC_BASE_URL"] = BASE
    env["SPACE_PORT"] = str(PORT)
    env["CREDENTIALS_DIRECTORY"] = str(WEGWERF_ROOT)
    env["PYTHONPATH"] = str(REPO_ROOT)
    env["REPO_ROOT"] = str(REPO_ROOT)
    env["TLS_KEY"] = str(TLS_KEY)
    env["TLS_CERT"] = str(TLS_CERT)
    if not (TLS_KEY.exists() and TLS_CERT.exists()):
        subprocess.run(
            ["openssl", "req", "-x509", "-newkey", "rsa:2048", "-keyout", str(TLS_KEY),
             "-out", str(TLS_CERT), "-days", "2", "-nodes", "-subj", "/CN=127.0.0.1",
             "-addext", "subjectAltName=IP:127.0.0.1"],
            check=True, capture_output=True,
        )
    launcher = WEGWERF_ROOT / "serve_tls.py"
    launcher.write_text(SERVE_TLS_LAUNCHER, encoding="utf-8")
    log_file = SERVE_LOG.open("ab")
    proc = subprocess.Popen(
        [".venv/bin/python", str(launcher)],
        env=env, cwd=str(REPO_ROOT), stdout=log_file, stderr=subprocess.STDOUT,
        start_new_session=True,
    )
    SERVE_PID.write_text(str(proc.pid))
    import ssl
    import urllib.request

    ctx = ssl._create_unverified_context()
    for _ in range(80):
        try:
            urllib.request.urlopen(f"{BASE}/health", timeout=1, context=ctx).read()
            return proc
        except Exception:
            time.sleep(0.25)
    raise SystemExit("Wegwerf-Server wurde nicht gesund.")


# --- HTTP -------------------------------------------------------------------------------

def _login(user: dict) -> tuple[str, str]:
    """Login → (Cookie, CSRF-Token). Die Sitzung ist eine echte `ui_sessions`-Zeile."""
    import httpx

    with httpx.Client(base_url=BASE, timeout=15, verify=False) as client:
        response = client.post(
            "/ui/login",
            data={
                "space": user["space"], "password": user["password"], "totp": _totp(user["secret"]),
            },
        )
        if response.status_code != 200:
            raise SystemExit(f"Login fehlgeschlagen: {response.status_code} {response.text[:400]}")
        treffer = re.search(r'name="csrf" value="([^"]+)"', response.text)
        if not treffer:
            raise SystemExit("kein CSRF-Token in der Login-Antwort")
        cookie = "; ".join(f"{k}={v}" for k, v in response.cookies.items())
        return cookie, treffer.group(1)


def _post_item(cookie: str, csrf: str, title: str, body: str, space: str | None = None) -> dict:
    import httpx

    payload = {"type": "task", "title": title, "body": body}
    if space:
        payload["space"] = space
    with httpx.Client(base_url=BASE, timeout=15, verify=False) as client:
        response = client.post(
            "/api/v1/items",
            json=payload,
            headers={"Cookie": cookie, "X-CSRF-Token": csrf, "Origin": BASE},
        )
    if response.status_code != 201:
        raise SystemExit(f"Anlegen fehlgeschlagen: {response.status_code} {response.text[:400]}")
    return response.json()


def _patch_item(cookie: str, csrf: str, item_id: str, version: int, title: str) -> dict:
    import httpx

    with httpx.Client(base_url=BASE, timeout=15, verify=False) as client:
        response = client.patch(
            f"/api/v1/items/{item_id}",
            json={"version": version, "title": title},
            headers={"Cookie": cookie, "X-CSRF-Token": csrf, "Origin": BASE},
        )
    if response.status_code != 200:
        raise SystemExit(f"Patch fehlgeschlagen: {response.status_code} {response.text[:400]}")
    return response.json()


def _wait_file(name: str, seconds: float = 60) -> bool:
    ende = time.time() + seconds
    while time.time() < ende:
        if (WEGWERF_ROOT / name).exists():
            return True
        time.sleep(0.02)
    return False


def _touch(name: str) -> None:
    (WEGWERF_ROOT / name).write_text("ok", encoding="utf-8")


def _stop_measure(proc: subprocess.Popen) -> float:
    """SIGTERM **nur** über die PID-Datei (Hard Rule 9) und misst, wie lange der Prozess zum
    Beenden braucht — bei **offenem Stream** (der Browser hält ihn).

    **Die Messung wartet auf das `Popen`-Objekt, nicht auf `/proc/<pid>`.** Ein beendeter
    Prozess bleibt als **Zombie** in `/proc` stehen, solange ihn niemand wegkholt — die erste
    Fassung dieser Messung prüfte nur `Path("/proc/<pid>").exists()` und meldete deshalb
    30,03 s (die eigene Obergrenze), obwohl der Server längst fertig war (der Log zeigte
    „Cancel 1 running task(s), timeout graceful shutdown exceeded" nach 5 s).
    """
    start = time.time()
    os.kill(proc.pid, signal.SIGTERM)
    try:
        proc.wait(timeout=60)
    except subprocess.TimeoutExpired:
        return time.time() - start
    return time.time() - start


def _proc_state(pid: int) -> str | None:
    """Der Zustand eines Prozesses aus `/proc/<pid>/stat` (z. B. `Z` = Zombie) — oder `None`,
    wenn der Prozess nicht (mehr) existiert."""
    try:
        text = Path(f"/proc/{pid}/stat").read_text(encoding="utf-8", errors="replace")
    except OSError:
        return None
    # Der Zustand steht im Klammerteil hinter dem Prozessnamen: `... (name) Z ...`
    try:
        return text.rsplit(")", 1)[1].split()[0]
    except IndexError:
        return None


def _browser_log() -> None:
    """Die Browser-Ausgabe zeigen (sie steht in Dateien, nicht in Pipes)."""
    for name in ("browser.err", "browser.out"):
        pfad = WEGWERF_ROOT / name
        if pfad.exists():
            text = pfad.read_text(encoding="utf-8", errors="replace").strip()
            if text:
                log(f"--- {name} ---\n{text[-3000:]}")


def _browser(alpha: dict) -> subprocess.Popen:
    skript = WEGWERF_ROOT / "browser_check.py"
    skript.write_text(BROWSER_SKILL, encoding="utf-8")
    e2e = Path.home() / ".claude-code-tools/e2e-venv/bin/python"
    # stdout/stderr gehen in **Dateien** (nicht in Pipes): so kann der Probe-Lauf die
    # Browser-Ausgabe ansehen, ohne auf das Prozessende zu warten (und ohne Pipe-Füllen).
    out_file = (WEGWERF_ROOT / "browser.out").open("wb")
    err_file = (WEGWERF_ROOT / "browser.err").open("wb")
    return subprocess.Popen(
        [str(e2e), str(skript), BASE, alpha["space"], alpha["password"], alpha["secret"],
         str(WEGWERF_ROOT), MARKER_BODY, TITEL_LIVE, TITEL_EDITOR],
        cwd=str(REPO_ROOT), stdout=out_file, stderr=err_file,
    )


def _item_id(title: str) -> str:
    """Die Item-ID anhand des Titels (aus dem Seed, nicht aus dem Browser)."""
    from storage.store import Store

    store = Store(str(DATA_ROOT), git=False)
    for row in store.search(title, space=SPACE, limit=50).items:
        if row.title == title:
            return row.id
    raise SystemExit(f"Seed-Item {title!r} nicht gefunden")


# --- Ablauf ------------------------------------------------------------------------------

def main(argv: list[str] | None = None) -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument(
        "--gegenlauf", action="store_true",
        help="bricht den Ereignis-Filter in api.py aus (der Filter darf unsichtbare Spaces "
             "durchlassen) — die Probe muss dann rot werden",
    )
    args = parser.parse_args(argv)

    api_datei = REPO_ROOT / "phase5_ui/webui/api.py"
    backup = None
    if args.gegenlauf:
        # Der Gegenlauf bricht **genau eine** Zeile: die Filterung "kein Ereignis, wenn sich
        # nur Unsichtbares geändert hat". Der Anker wird über den Zeilenanfang gesucht (die
        # Einrückung ist deep-indented und ändert sich mit dem Code), nicht über eine feste
        # Zahl Leerzeichen.
        backup = api_datei.read_text(encoding="utf-8")
        zeilen = backup.splitlines(keepends=True)
        treffer = [i for i, z in enumerate(zeilen) if z.strip() == "if not spaces:"]
        assert len(treffer) == 1, f"Gegenlauf-Anker: {len(treffer)} Treffer (genau 1 erwartet)"
        i = treffer[0]
        einrueckung = zeilen[i][: len(zeilen[i]) - len(zeilen[i].lstrip())]
        zeilen[i] = einrueckung + "if False:\n"
        api_datei.write_text("".join(zeilen), encoding="utf-8")

    alpha, beta = _setup()
    server = None
    proc = None
    try:
        server = _serve()
        pid = server.pid
        proc = _browser(alpha)
        if not _wait_file("session.json", 90):
            _browser_log()
            raise SystemExit("Der Browser wurde nicht bereit (keine Sitzung).")
        sitzung = json.loads((WEGWERF_ROOT / "session.json").read_text(encoding="utf-8"))
        alpha_cookie, alpha_csrf = sitzung["cookie"], sitzung["csrf"]
        beta_cookie, beta_csrf = _login(beta)
        if not _wait_file("ready1.flag", 120):
            _browser_log()
            raise SystemExit("Der Browser wurde nicht bereit.")

        # (1) Write in alpha — der Browser muss die Aenderung sehen (Latenz!).
        t0 = time.time() * 1000
        _post_item(alpha_cookie, alpha_csrf, TITEL_LIVE, f"Der Text der neuen Aufgabe.")
        _touch("write1.done")
        if not _wait_file("phase1.json", 60):
            _browser_log()
            raise SystemExit("Phase 1 des Browsers kam nicht zurueck.")

        # (2) Fremder Write auf das Item, das der Browser **offen und geaendert** hat
        #     (P10.5-S). Der Browser muss erst tippen (ready2.flag).
        if not _wait_file("ready2.flag", 60):
            _browser_log()
            raise SystemExit("Der Browser hat das Item nicht geoeffnet.")
        _patch_item(
            alpha_cookie, alpha_csrf, _item_id(TITEL_EDITOR), 1, TITEL_EDITOR + " (geaendert)"
        )
        _touch("write2.done")
        if not _wait_file("phase2.json", 60):
            _browser_log()
            raise SystemExit("Phase 2 des Browsers kam nicht zurueck.")

        # (3) Write in beta — fuer alpha unsichtbar, also **kein** Ereignis.
        _post_item(beta_cookie, beta_csrf, "Beta-Aufgabe", "Nur fuer beta sichtbar.")
        _touch("write3.done")
        if not _wait_file("phase3.json", 60):
            _browser_log()
            raise SystemExit("Phase 3 des Browsers kam nicht zurueck.")

        # (4) Shutdown mit offenem Stream (der Browser haelt ihn noch).
        dauer = _stop_measure(server)
        _touch("shutdown.done")
        try:
            proc.wait(timeout=60)
        except subprocess.TimeoutExpired:
            proc.kill()
            proc.wait(timeout=10)
        stdout = (WEGWERF_ROOT / "browser.out").read_text(encoding="utf-8", errors="replace")
        stderr = (WEGWERF_ROOT / "browser.err").read_text(encoding="utf-8", errors="replace")
        if proc.returncode != 0:
            log(f"Browser-Fehler: {stderr[-1500:]}")
        messung = json.loads(stdout.strip().splitlines()[-1]) if stdout.strip() else {}

        phase1 = json.loads((WEGWERF_ROOT / "phase1.json").read_text(encoding="utf-8"))
        phase2 = json.loads((WEGWERF_ROOT / "phase2.json").read_text(encoding="utf-8"))
        phase3 = json.loads((WEGWERF_ROOT / "phase3.json").read_text(encoding="utf-8"))
        latenz = None
        if messung.get("erscheint_at") and t0:
            latenz = messung["erscheint_at"] - t0
        befund = {
            "volltext_schalter_vorhanden": messung.get("schalter_vorhanden") is True,
            "volltext_ohne_schalter_kein_treffer": messung.get("treffer_ohne_schalter") == 0,
            "volltext_mit_schalter_treffer": messung.get("treffer_mit_schalter", 0) >= 1,
            "ereignis_angekommen": (messung.get("changed_nach_write1") or 0) >= 1,
            "latenz_ms": latenz,
            "latenz_ok": latenz is not None and latenz <= LATENZ_MAX_MS,
            "editor_text_erhalten": messung.get("text_erhalten") == TIPP_TEXT,
            "editor_band_sichtbar": messung.get("band_sichtbar") is True,
            "unsichtbarer_space_kein_ereignis": (
                messung.get("changed_nach_write3") == messung.get("changed_nach_write2")
            ),
            "shutdown_s": round(dauer, 2),
            "shutdown_ok": dauer <= SHUTDOWN_MAX_S,
            "keine_seitenfehler": not messung.get("seitenfehler"),
        }
        ok = all(v for k, v in befund.items() if isinstance(v, bool))
        ergebnis = {
            "probe": "p105_b10_realtime",
            "instanz": {"basis": BASE, "pid": pid, "wegwerf": True},
            "befund": befund,
            "messung": messung,
            "phase1": phase1,
            "phase2": phase2,
            "phase3": phase3,
            "alle_kriterien_erfuellt": ok,
        }
        if args.gegenlauf:
            ergebnis["gegenlauf"] = True
            ergebnis["gegenlauf_erwartet_rot"] = not ok
        ziel = RESULT_GEGENLAUF if args.gegenlauf else RESULT
        ziel.write_text(
            json.dumps(ergebnis, indent=2, ensure_ascii=False) + "\n", encoding="utf-8"
        )
        print(json.dumps(ergebnis, indent=2, ensure_ascii=False))
        return (0 if not ok else 1) if args.gegenlauf else (0 if ok else 1)
    finally:
        if proc is not None and proc.poll() is None:
            proc.kill()
        # Die eigene Wegwerf-Instanz beenden (Hard Rule 9: PID-Datei, kein Regex).
        # **SIGTERM zuerst, SIGKILL als Notnagel:** uvicorn wartet bei einem offenen
        # Ereignis-Stream unbegrenzt auf die Verbindung — ohne die harte Variante bleibt die
        # Instanz stehen und blockiert den Port für den nächsten Lauf (gemessen: eine
        # hängengebliebene Instanz aus einem Lauf mit kaputtem Launcher).
        if server is not None and server.poll() is None:
            try:
                os.kill(server.pid, signal.SIGTERM)
            except ProcessLookupError:
                pass
            try:
                server.wait(timeout=12)
            except subprocess.TimeoutExpired:
                try:
                    os.kill(server.pid, signal.SIGKILL)
                except ProcessLookupError:
                    pass
                try:
                    server.wait(timeout=10)
                except subprocess.TimeoutExpired:
                    log(f"WARN: Wegwerf-Server {server.pid} liess sich nicht beenden.")
        SERVE_PID.unlink(missing_ok=True)
        if backup is not None:
            api_datei.write_text(backup, encoding="utf-8")


if __name__ == "__main__":
    raise SystemExit(main())
