#!/usr/bin/env python3
"""P10.5 Block 11, Schritt 11.5 — die To-do-Kästchen (ED-2) an der Wegwerf-Instanz.

**Wegwerf (Plan §2.3):** Port **18812** (eigener Port), eigene Wurzel
`/tmp/opencode/sharefyx-wegwerf-p105-b11-todo`, tmp-`DATA_ROOT`, tmp-`auth.sqlite3`,
File-Keyring, Umgebung ohne `SHAREFYX_*`/`SFX_*`, Stopp **nur** über die PID-Datei
(Hard Rule 9).

**Was gemessen wird (Abnahme P10.5-53, ED-2):**

| # | Zelle | Erwartung |
|---|---|---|
| 1 | **Kästchen sichtbar** | im Live-Editor steht je To-do-Zeile **ein** Kästchen (angehakt = `[x]`) |
| 2 | **Klick schaltet den Puffer** | `[ ]` und `[x]` wechseln sich ab — im **Text**, nicht im DOM |
| 3 | **Klick bei sauberem Editor schreibt** | die Version springt, der Server trägt `[x]` (Hard Rule 3: mit `version`) |
| 4 | **Klick bei geändertem Editor** | nur der Puffer — die Version bleibt |
| 5 | **Lesesicht** | das Kästchen ist da und **deaktiviert** (kein Schreibweg außerhalb des Editors) |
| 6 | **Rohmodus** (ED-5) | **jedes** Zeichen sichtbar — also auch das `[ ]`, und **kein** Kästchen |

**Der Gegenlauf ist der Kern der Probe.** Dass ein Klick bei sauberem Editor *speichert*,
ist eine **Entscheidung des Codes** — und ein Fehler darin wäre still: der Klick täte
"nur was", und niemand merkte es. Die zweite Messung liefert deshalb `editor.js` **ohne**
die Zeile `if (sauber) saveItem();` aus (same-origin, also CSP-konform) und erwartet, dass
**genau die Zelle 3** rot wird. **Die anderen Zellen bleiben grün** — sonst wäre der
Gegenlauf kein Gegenlauf, sondern ein Totalausfall.

**Die Belegpflicht (aus Block 11.4 übernommen):** die gepatchte Datei trägt eine
**Kennung** (`window.__p105_todo_variante`), und der Browser **liest sie zurück**. Ohne diesen
Beleg wäre jede Zahl aus dem Gegenlauf wertlos — die erste Fassung der Probe vom 2026-10-24
maß drei gleiche Werte und meldete „gleich".

**Der Zustand ist derselbe Server für beide Messungen:** der erste Lauf speichert (Version
1 → 2), der zweite sieht deshalb die Version 2. Die Zellen prüfen deshalb **relativ**
(„die Version hat sich geändert" / „die Version ist geblieben"), nicht absolut.

Aufruf: `.venv/bin/python phase10_5_finishing/probes/p105_b11_todo_probe.py`
Ergebnis: `phase10_5_finishing/probes/p105_b11_todo.json`
Gegenlauf: `phase10_5_finishing/probes/p105_b11_todo_gegenlauf.json`
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
WEGWERF_ROOT = Path("/tmp/opencode/sharefyx-wegwerf-p105-b11-todo")
DATA_ROOT = WEGWERF_ROOT / "data"
AUTH_DB = WEGWERF_ROOT / "auth.sqlite3"
DEK_FILE = WEGWERF_ROOT / "auth-dek"
SERVE_PID = WEGWERF_ROOT / "serve.pid"
SERVE_LOG = WEGWERF_ROOT / "serve.log"
PORT = 18812
BASE = f"https://127.0.0.1:{PORT}"
TLS_KEY = WEGWERF_ROOT / "key.pem"
TLS_CERT = WEGWERF_ROOT / "cert.pem"
SPACE = "alpha"
RESULT = Path(__file__).with_name("p105_b11_todo.json")
RESULT_GEGENLAUF = Path(__file__).with_name("p105_b11_todo_gegenlauf.json")

#: Der **Text** des Items. Drei To-do-Zeilen: zwei offen, eine erledigt — und ein Satz, der
#: **kein** To-do ist (an ihm darf kein Kästchen erscheinen).
BODY = (
    "# To-do-Item\n"
    "\n"
    "- [ ] offen\n"
    "- [ ] zweiter\n"
    "- [x] erledigt\n"
    "\n"
    "Ein Satz ohne Kaestchen.\n"
)

#: Die **Zeile**, an der der Klick gemessen wird: die erste offene Aufgabe.
TODO_ZEILE = "- [ ] offen"


def log(text: str) -> None:
    print(text, file=sys.stderr, flush=True)


SERVE_TLS_LAUNCHER = '''"""Dieselbe App wie phase2_mcp/scripts/serve.py, plus TLS."""
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


#: Die **Browser-Seite** der Probe. Sie laeuft im e2e-venv (Playwright), nicht im Dev-venv.
#:
#: **Zwei Laeufe:** der erste mit dem Original, der zweite mit der gepatchten `editor.js`
#: (der Gegenlauf). Der Server bleibt derselbe — die Zellen pruefen **relativ**.
BROWSER_SKILL = '''import json, sys, time, hmac, hashlib, struct, base64, re
from pathlib import Path

base, space, password, secret, workdir, variante = sys.argv[1:7]
work = Path(workdir)


def totp_now(secret_b32):
    key = base64.b32decode(secret_b32 + "=" * (-len(secret_b32) % 8))
    counter = int(time.time() // 30)
    digest = hmac.new(key, struct.pack(">q", counter), hashlib.sha1).digest()
    offset = digest[-1] & 0x0F
    code = (struct.unpack(">I", digest[offset:offset + 4])[0] & 0x7FFFFFFF) % 1000000
    return f"{code:06d}"


def warte_auf_neues_fenster():
    """**Der TOTP-Replay-Schutz des Auth-Servers.** `authserver/store.py :: consume_code()`
    merkt sich den zuletzt benutzten 30-Sekunden-Zaehler je Space (`totp_replay`) — der
    **selbe** Code darf **nicht** zweimal benutzt werden. Die zweite Anmeldung der Probe
    (der Gegenlauf) laeuft aber wenige Sekunden nach der ersten: ohne diese Warte laeuft
    sie im **selben** Fenster und endet mit **401** (gemessen am 2026-10-25: alle drei
    Versuche abgelehnt, alle im selben Fenster).

    Das ist ein Fehler des **Messgeraets**, nicht des Produkts: der Replay-Schutz ist
    richtig und gewollt (Plan §2.4 der Auth-Phase).
    """
    jetzt = int(time.time() // 30)
    warte = (jetzt + 1) * 30 + 1 - time.time()
    if warte > 0:
        time.sleep(warte)


from playwright.sync_api import sync_playwright


def js_route(route):
    """Liefert `editor.js` **ohne** die Zeile `if (sauber) saveItem();` -- same-origin,
    also CSP-konform (`script-src 'self'`). Der Wegwerf-Server liefert die Originaldatei."""
    try:
        antwort = route.fetch()
        text = antwort.text()
    except Exception:
        route.continue_()
        return
    text, n = re.subn(r"if \\(sauber\\) saveItem\\(\\);",
                      "if (sauber) { /* Gegenlauf: kein Speichern */ }", text, count=1)
    if n != 1:
        route.fulfill(status=500, body="Anker fehlt: " + str(n))
        return
    # Die **Kennung**: ohne sie waere der Gegenlauf blind (Block 11.4, Lehre).
    text = text.replace('"use strict";',
                        '"use strict";\\nwindow.__p105_todo_variante = "gegenlauf";', 1)
    route.fulfill(response=antwort, body=text)


out = {}
with sync_playwright() as p:
    browser = p.chromium.launch()
    context = browser.new_context(ignore_https_errors=True, viewport={"width": 1400, "height": 900})
    page = context.new_page()
    fehler = []
    page.on("pageerror", lambda exc: fehler.append(str(exc)))

    if variante == "gegenlauf":
        page.route("**/ui/static/js/editor.js", js_route)

    # -- Anmeldung ---------------------------------------------------------------
    # **Der TOTP-Code hat ein Fenster von 30 Sekunden**, und der Auth-Server merkt sich
    # den benutzten Zaehler (Replay-Schutz). Deshalb **vor** jeder Anmeldung auf ein
    # **neues** Fenster warten — sonst laeuft der zweite Lauf (Gegenlauf) im selben
    # Fenster und endet mit **401** (gemessen am 2026-10-25: drei Versuche, alle
    # abgelehnt). Der Fehler lag im Messgeraet, nicht im Produkt.
    angemeldet = False
    for _versuch in range(3):
        warte_auf_neues_fenster()
        page.goto(base + "/ui/login", wait_until="domcontentloaded")
        page.fill('input[name="space"]', space)
        page.fill('input[name="password"]', password)
        page.fill('input[name="totp"]', totp_now(secret))
        page.click('form[action="/ui/login"] button[type="submit"]')
        try:
            page.wait_for_selector("#shell", timeout=8000)
            angemeldet = True
            break
        except Exception:
            continue
    if not angemeldet:
        raise SystemExit("Anmeldung drei Mal fehlgeschlagen (TOTP-Fenster?).")

    # **Die Kennung** der ausgelieferten Datei: im Normalfall gibt es keine (die Datei
    # ist unveraendert), im Gegenlauf traegt sie eine. Beides wird **gelesen**, nicht
    # angenommen.
    #
    # **Erst **nach** dem Oeffnen des Items gelesen (also nach dem Laden des Editors):
    # `editor.js` wird erst mit der App-Seite geladen — die Anmeldeseite laedt es nicht.
    # Ein Lesen direkt nach der Anmeldung ergab deshalb immer „original", auch im
    # Gegenlauf (gemessen am 2026-10-25) — der Beleg war schlicht an der falschen Stelle.
    out["variante_ausgeliefert"] = "original"

    # **Nur die Entwuerfe loeschen — nicht das ganze sessionStorage.** Der CSRF-Token
    # liegt dort ebenfalls (`api.js :: csrfToken()` liest `sessionStorage["sfx:csrf"]`),
    # und ein leeres sessionStorage bedeutet: **jeder** Schreibvorgang endet mit **403**
    # (gemessen am 2026-10-25: der PATCH des Klicks wurde mit 403 abgelehnt — der Fehler
    # lag im Messgeraet, nicht im Produkt).
    try:
        page.evaluate("""() => {
          Object.keys(sessionStorage).forEach(function (k) {
            if (k.indexOf('sfx:draft:') === 0) sessionStorage.removeItem(k);
          });
        }""")
    except Exception:
        pass

    # -- Das Item oeffnen ---------------------------------------------------------
    page.wait_for_timeout(1200)
    page.wait_for_selector(".overview__space-open", timeout=20000)
    page.locator(".overview__space-open").first.click()
    page.wait_for_timeout(1200)
    page.locator(".list__row", has_text="To-do-Item").first.click()
    page.wait_for_timeout(1800)
    editor_da = False
    try:
        page.wait_for_selector(".CodeMirror", timeout=30000)
        editor_da = True
    except Exception:
        pass
    out["live_editor_da"] = editor_da
    # **Der Beleg wird jetzt gelesen** — der Editor ist geladen, also ist `editor.js`
    # ausgeliefert worden (und im Gegenlauf die gepatchte Fassung).
    out["variante_ausgeliefert"] = page.evaluate(
        "() => window.__p105_todo_variante || 'original'"
    )

    def wert():
        return page.evaluate("""() => {
          const w = document.querySelector('.CodeMirror');
          return w && w.CodeMirror ? w.CodeMirror.getValue() : null;
        }""")

    def version():
        return page.evaluate("""async () => {
          const chip = document.querySelector('#meta-item-id .id-chip');
          if (!chip) return null;
          const id = chip.textContent.trim();
          const antwort = await fetch('/api/v1/items/' + id, {credentials: 'same-origin'});
          if (!antwort.ok) return null;
          const item = await antwort.json();
          return {version: item.version, body: item.body};
        }""")

    # -- Zelle 1: die Kaestchen ----------------------------------------------------
    out["kaestchen"] = page.evaluate("""() => {
      const k = document.querySelectorAll('.CodeMirror .sfx-todo');
      return {
        anzahl: k.length,
        angehakt: Array.from(k).filter(function (x) { return x.checked; }).length,
        typen: Array.from(k).map(function (x) { return x.type; }),
      };
    }""")

    # -- Zelle 2 und 3: der Klick (Text und Write) ---------------------------------
    vor_klick = wert()
    version_vor = version()
    if out["kaestchen"].get("anzahl"):
        # Das **erste** Kaestchen: es ist das einer offenen Aufgabe (die Reihenfolge der
        # Kaestchen folgt der Reihenfolge der Zeilen).
        page.locator(".CodeMirror .sfx-todo").first.click()
        page.wait_for_timeout(1200)
    nach_klick = wert()
    version_nach = version()
    out["wert_vor"] = vor_klick
    out["wert_nach"] = nach_klick
    out["version_vor"] = version_vor
    out["version_nach"] = version_nach

    # -- Zelle 4: der Klick bei **geaendertem** Editor -----------------------------
    # Der Editor wird **geaendert** (ein Zeichen getippt) — dann gehoert der Klick zur
    # naechsten Speicherung: nur der Puffer.
    page.evaluate("""() => {
      const w = document.querySelector('.CodeMirror');
      w.CodeMirror.focus();
      w.CodeMirror.replaceRange('X', {line: 0, ch: 0});
    }""")
    page.wait_for_timeout(400)
    version_vor_dirty = version()
    wert_vor_dirty = wert()
    if out["kaestchen"].get("anzahl"):
        page.locator(".CodeMirror .sfx-todo").nth(1).click()
        page.wait_for_timeout(1200)
    out["wert_vor_dirty"] = wert_vor_dirty
    out["wert_nach_dirty"] = wert()
    out["version_vor_dirty"] = version_vor_dirty
    out["version_nach_dirty"] = version()

    # -- Zelle 5: die Lesesicht ----------------------------------------------------
    # `markdownToHtml()` wird **im Browser** aufgerufen -- dieselbe Funktion, die die
    # Lesesicht benutzt (`roPreviewEl.innerHTML = markdownToHtml(...)`), samt Sanitizer.
    #
    # **Der Zeilenumbruch wird ueber `String.fromCharCode(10)` gebildet**, nicht ueber
    # `\\n`: diese Datei wird als Python-Quelltext geschrieben und noch einmal als
    # Python-Quelltext ausgewertet -- ein `\\n` waere an der dritten Schicht ein
    # **echter** Umbruch und zerriss das JavaScript-Stringliteral (gemessen am 2026-10-25:
    # `SyntaxError: Invalid or unexpected token`).
    out["lesesicht"] = page.evaluate("""async () => {
      const m = await import('/ui/static/js/markdown.js');
      const NL = String.fromCharCode(10);
      const html = m.markdownToHtml('- [ ] offen' + NL + '- [x] erledigt' + NL, {});
      const huelle = document.createElement('div');
      huelle.innerHTML = html;
      const k = huelle.querySelectorAll('input');
      return {
        html: html,
        anzahl: k.length,
        alle_deaktiviert: Array.from(k).every(function (x) { return x.disabled; }),
        angehakt: Array.from(k).filter(function (x) { return x.checked; }).length,
      };
    }""")

    # -- Zelle 6: der Rohmodus -----------------------------------------------------
    page.click("#toggle-preview")
    page.wait_for_timeout(600)
    out["rohmodus"] = page.evaluate("""() => {
      const zeilen = Array.from(document.querySelectorAll('.CodeMirror-line'));
      return {
        kaestchen: document.querySelectorAll('.CodeMirror .sfx-todo').length,
        text: zeilen.map(function (z) { return z.textContent; }).join(String.fromCharCode(10)),
        roh: document.querySelector('.CodeMirror').classList.contains('is-raw'),
      };
    }""")
    out["seitenfehler"] = fehler

print(json.dumps(out, ensure_ascii=False))
'''


def _provision(space: str) -> dict:
    from authserver import passwords, totp
    from authserver.config import decode_data_encryption_key
    from authserver.secretbox import seal
    from authserver.store import AuthStore

    password = "wegwerf-todo-" + secrets.token_urlsafe(8)
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


def _setup() -> dict:
    shutil.rmtree(WEGWERF_ROOT, ignore_errors=True)
    WEGWERF_ROOT.mkdir(parents=True, exist_ok=True)
    DATA_ROOT.mkdir(parents=True, exist_ok=True)
    raw = secrets.token_bytes(32)
    DEK_FILE.write_text(base64.urlsafe_b64encode(raw).rstrip(b"=").decode("ascii") + "\n")
    os.chmod(DEK_FILE, 0o600)
    alpha = _provision(SPACE)
    # Der Seed: **ein** Item mit drei To-do-Zeilen (zwei offen, eine erledigt) und einem
    # Satz ohne Kaestchen. `task/open` — der Listenfilter zeigt standardmaessig nur
    # offene Aufgaben.
    code = (
        "import sys; sys.path.insert(0, 'phase1_storage')\n"
        "from storage.store import Store\n"
        f"s = Store({str(DATA_ROOT)!r}, git=True)\n"
        f"s.create({SPACE!r}, type='task', title='To-do-Item', body={BODY!r})\n"
    )
    subprocess.run(
        [".venv/bin/python", "-c", code], check=True, cwd=str(REPO_ROOT),
        env={**os.environ, "PYTHONPATH": str(REPO_ROOT / "phase1_storage")},
    )
    return alpha


def _serve() -> subprocess.Popen:
    env = os.environ.copy()
    for name in list(env):
        if name.startswith("SHAREFYX_") or name.startswith("SFX_"):
            env.pop(name)
    env["SPACE_DATA_ROOT"] = str(DATA_ROOT)
    env["SPACE_AUTH_DB"] = str(AUTH_DB)
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


def _browserlauf(alpha: dict, variante: str) -> dict:
    """Ein Lauf im Browser — entweder mit dem Original oder mit der gepatchten Datei."""
    skript = WEGWERF_ROOT / f"browser_{variante}.py"
    skript.write_text(BROWSER_SKILL, encoding="utf-8")
    e2e = Path.home() / ".claude-code-tools/e2e-venv/bin/python"
    out_file = (WEGWERF_ROOT / f"browser_{variante}.out").open("wb")
    err_file = (WEGWERF_ROOT / f"browser_{variante}.err").open("wb")
    proc = subprocess.Popen(
        [str(e2e), str(skript), BASE, alpha["space"], alpha["password"], alpha["secret"],
         str(WEGWERF_ROOT), variante],
        cwd=str(REPO_ROOT), stdout=out_file, stderr=err_file,
    )
    try:
        proc.wait(timeout=300)
    except subprocess.TimeoutExpired:
        proc.kill()
        proc.wait(timeout=10)
    text = (WEGWERF_ROOT / f"browser_{variante}.out").read_text(
        encoding="utf-8", errors="replace").strip()
    if not text:
        log("Browser-Fehler:\n" + (WEGWERF_ROOT / f"browser_{variante}.err").read_text(
            encoding="utf-8", errors="replace")[-3000:])
        raise SystemExit(f"Der Browser hat nichts gemeldet ({variante}).")
    return json.loads(text.splitlines()[-1])


def _umgeschaltet(vor: str | None, nach: str | None) -> bool:
    """Hat der Klick **genau eine** Zeile geaendert — und zwar `[ ]` gegen `[x]`?

    **Zeile fuer Zeile**, nicht als Text-Ersetzung ueber den ganzen Text: der Text traegt
    mehrere To-do-Zeilen, und ein globales Ersetzen wuerde **alle** `[ ]` tauschen. Der
    erste Wurf der Probe meldete deshalb „nicht umgeschaltet", obwohl der Klick genau
    richtig gearbeitet hatte (gemessen am 2026-10-25).
    """
    if vor is None or nach is None or vor == nach:
        return False
    vor_zeilen = vor.split("\n")
    nach_zeilen = nach.split("\n")
    if len(vor_zeilen) != len(nach_zeilen):
        return False
    geaendert = [
        (a, b) for a, b in zip(vor_zeilen, nach_zeilen) if a != b
    ]
    if len(geaendert) != 1:
        return False
    alt, neu = geaendert[0]
    return (alt.replace("[ ]", "[x]") == neu) or (alt.replace("[x]", "[ ]") == neu)


#: Eine To-do-Zeile: optionale Einrueckung, ein Listenzeichen, dann `[ ]`/`[x]`.
TODO_ZEILE_RE = re.compile(r"^[ \t]*[-*+][ \t]+\[([ xX])\]")


def _erwartete_kaestchen(text: str | None) -> tuple[int, int]:
    """(Anzahl To-do-Zeilen, Anzahl erledigter) — **aus dem Text**, nicht aus einer
    festen Zahl.

    **Warum relativ:** der zweite Lauf (Gegenlauf) sieht den Text, den der erste Lauf
    **gespeichert** hat — dort ist die erste Aufgabe inzwischen erledigt. Eine feste Zahl
    („ein Kaestchen ist angehakt") wuerde den zweiten Lauf grundlos rot melden (gemessen
    am 2026-10-25).
    """
    zeilen = [z for z in (text or "").split("\n") if TODO_ZEILE_RE.match(z)]
    erledigt = sum(1 for z in zeilen if TODO_ZEILE_RE.match(z).group(1).lower() == "x")
    return len(zeilen), erledigt


def _zellen(messung: dict) -> dict:
    """Die Zellen aus einer Messung — **ohne** die Gegenlauf-Mechanik."""
    kaestchen = messung.get("kaestchen") or {}
    lesesicht = messung.get("lesesicht") or {}
    rohmodus = messung.get("rohmodus") or {}
    version_vor = messung.get("version_vor") or {}
    version_nach = messung.get("version_nach") or {}
    version_vor_dirty = messung.get("version_vor_dirty") or {}
    version_nach_dirty = messung.get("version_nach_dirty") or {}
    erwartet_anzahl, erwartet_angehakt = _erwartete_kaestchen(messung.get("wert_vor"))
    return {
        "live_editor_geladen": messung.get("live_editor_da") is True,
        "todo_kaestchen_sichtbar": (
            erwartet_anzahl > 0
            and kaestchen.get("anzahl") == erwartet_anzahl
            and kaestchen.get("angehakt") == erwartet_angehakt
            and set(kaestchen.get("typen") or []) == {"checkbox"}
        ),
        "klick_schaltet_den_puffer": _umgeschaltet(
            messung.get("wert_vor"), messung.get("wert_nach")
        ),
        "klick_schreibt_mit_version": (
            version_vor.get("version") is not None
            and version_nach.get("version") is not None
            and version_nach.get("version") != version_vor.get("version")
            and "[x]" in (version_nach.get("body") or "")
        ),
        "klick_bei_geaendertem_editor_nur_puffer": (
            version_vor_dirty.get("version") is not None
            and version_nach_dirty.get("version") == version_vor_dirty.get("version")
            and messung.get("wert_nach_dirty") != messung.get("wert_vor_dirty")
        ),
        "lesesicht_zeigt_deaktiviertes_kaestchen": (
            lesesicht.get("anzahl") == 2
            and lesesicht.get("alle_deaktiviert") is True
            and lesesicht.get("angehakt") == 1
        ),
        "rohmodus_zeigt_jedes_zeichen": (
            rohmodus.get("roh") is True
            and rohmodus.get("kaestchen") == 0
            and "[" in (rohmodus.get("text") or "")
        ),
        "keine_seitenfehler": not messung.get("seitenfehler"),
    }


def main(argv: list[str] | None = None) -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.parse_args(argv)

    alpha = _setup()
    server = _serve()
    try:
        normal = _browserlauf(alpha, "normal")
        gegenlauf = _browserlauf(alpha, "gegenlauf")

        zellen_normal = _zellen(normal)
        zellen_gegenlauf = _zellen(gegenlauf)

        # **Der Beleg der Auslieferung.** Im Normalfall ist die Datei unveraendert; im
        # Gegenlauf traegt sie die Kennung. Ohne diesen Beleg waere der Gegenlauf blind.
        varianten_belege = {
            "normal": {
                "ausgeliefert": normal.get("variante_ausgeliefert"),
                "ist_die_variante": normal.get("variante_ausgeliefert") == "original",
            },
            "gegenlauf": {
                "ausgeliefert": gegenlauf.get("variante_ausgeliefert"),
                "ist_die_variante": gegenlauf.get("variante_ausgeliefert") == "gegenlauf",
            },
        }
        befund = dict(zellen_normal)
        befund["varianten_belege"] = varianten_belege
        befund["alle_varianten_ausgeliefert"] = all(
            b["ist_die_variante"] for b in varianten_belege.values()
        )
        # **Der Gegenlauf:** genau **eine** Zelle wird rot — die Schreib-Zelle. Bleibt
        # eine andere rot, waere der Gegenlauf kein Gegenlauf.
        rote_gegenlauf = [k for k, v in zellen_gegenlauf.items() if not v]
        befund["gegenlauf_rote_zellen"] = rote_gegenlauf
        befund["gegenlauf_bricht_genau_die_schreibzelle"] = rote_gegenlauf == [
            "klick_schreibt_mit_version"
        ]

        ok = all(v for v in befund.values() if isinstance(v, bool))
        ergebnis = {
            "probe": "p105_b11_todo",
            "instanz": {"basis": BASE, "pid": server.pid, "wegwerf": True},
            "befund": befund,
            "messung": {"normal": normal, "gegenlauf": gegenlauf},
            "alle_kriterien_erfuellt": ok,
        }
        RESULT.write_text(
            json.dumps(ergebnis, indent=2, ensure_ascii=False) + "\n", encoding="utf-8"
        )
        RESULT_GEGENLAUF.write_text(
            json.dumps({"messung": gegenlauf, "zellen": zellen_gegenlauf},
                       indent=2, ensure_ascii=False) + "\n",
            encoding="utf-8",
        )
        print(json.dumps(ergebnis, indent=2, ensure_ascii=False))
        return 0 if ok else 1
    finally:
        if server.poll() is None:
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
        SERVE_PID.unlink(missing_ok=True)


if __name__ == "__main__":
    raise SystemExit(main())
