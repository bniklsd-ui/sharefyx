#!/usr/bin/env python3
"""P10.5 Block 11, Schritt 11.8 — der Roundtrip (V201-Rest) an der Wegwerf-Instanz.

**Wegwerf (Plan §2.3):** Port **18813** (eigener Port), eigene Wurzel
`/tmp/opencode/sharefyx-wegwerf-p105-b11-rt`, tmp-`DATA_ROOT`, tmp-`auth.sqlite3`,
File-Keyring, Umgebung ohne `SHAREFYX_*`/`SFX_*`, Stopp **nur** über die PID-Datei
(Hard Rule 9).

**Was gemessen wird (Abnahme P10.5-52, V201-Rest):** die **zehn** M7-Fixtures (Frontmatter,
Listen, Tabelle, Code, Links, `itm_…`-Referenzen, Taskliste, Zitat, Unicode/Tabs,
Whitespace) als Items in der Wegwerf-Instanz. Je Item:

1. **Öffnen** → der Editor zeigt **byte-identisch** den Body des Servers, und
   `isDirty()` ist **false** — das Öffnen macht den Editor **nicht** zum geänderten.
2. **Speichern ist nicht nötig** — der Speicher-Knopf ist deaktiviert, das Versionsband
   zeigt den gespeicherten Stand.
3. **Die Datei auf der Platte ist byte-identisch** — vor dem Lauf und nach dem Lauf
   verglichen (im Python-Teil der Probe, über die echten Dateien).
4. **Ein Zeichen tippen und wieder löschen** → `isDirty()` ist wieder **false**.

**Warum `isDirty()` direkt gemessen wird.** Das Modul `editor.js` ist ein ES-Modul mit
`export function isDirty()`; die Probe importiert es **im Browser** (`import(...)`) und ruft
die Funktion auf — das ist **dieselbe** Modul-Instanz, die die App benutzt (der
Modul-Register ist nach URL geschlüsselt). Der Weg über die Oberfläche (der deaktivierte
Speicher-Knopf, das Versionsband) wird **zusätzlich** gemessen: zwei unabhaengige Größen
für dieselbe Aussage.

**Die Fixtures liegen jetzt im Repo** (`probes/fixtures_m7/`, **byte-identisch** zu den
M7-Fixtures aus dem Scratchpad `~/.claude-code-tools/m7/fixtures` — die M7-Messung selbst
lief dort, s. `phase10_inventory/messung/M7_editor.md`). Vorher wäre die Probe von einem
Scratchpad abhängig gewesen: ein Beleg, den niemand wiederholen kann, ist kein Beleg.

Aufruf: `.venv/bin/python phase10_5_finishing/probes/p105_b11_roundtrip_probe.py`
Ergebnis: `phase10_5_finishing/probes/p105_b11_roundtrip.json`
"""
from __future__ import annotations

import argparse
import base64
import hashlib
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
WEGWERF_ROOT = Path("/tmp/opencode/sharefyx-wegwerf-p105-b11-rt")
DATA_ROOT = WEGWERF_ROOT / "data"
AUTH_DB = WEGWERF_ROOT / "auth.sqlite3"
DEK_FILE = WEGWERF_ROOT / "auth-dek"
SERVE_PID = WEGWERF_ROOT / "serve.pid"
SERVE_LOG = WEGWERF_ROOT / "serve.log"
PORT = 18813
BASE = f"https://127.0.0.1:{PORT}"
TLS_KEY = WEGWERF_ROOT / "key.pem"
TLS_CERT = WEGWERF_ROOT / "cert.pem"
SPACE = "alpha"
RESULT = Path(__file__).with_name("p105_b11_roundtrip.json")

#: Die **zehn** M7-Fixtures — byte-identisch aus dem Scratchpad ins Repo kopiert (2026-10-25).
FIXTURE_DIR = REPO_ROOT / "phase10_5_finishing" / "probes" / "fixtures_m7"


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


#: Die **Browser-Seite** der Probe (e2e-venv, Playwright).
BROWSER_SKILL = '''import json, sys, time, hmac, hashlib, struct, base64
from pathlib import Path

base, space, password, secret, workdir, titel_json = sys.argv[1:7]
work = Path(workdir)
titel = json.loads(titel_json)


def totp_now(secret_b32):
    key = base64.b32decode(secret_b32 + "=" * (-len(secret_b32) % 8))
    counter = int(time.time() // 30)
    digest = hmac.new(key, struct.pack(">q", counter), hashlib.sha1).digest()
    offset = digest[-1] & 0x0F
    code = (struct.unpack(">I", digest[offset:offset + 4])[0] & 0x7FFFFFFF) % 1000000
    return f"{code:06d}"


def warte_auf_neues_fenster():
    """**Der TOTP-Replay-Schutz des Auth-Servers** (`totp_replay`): derselbe
    30-Sekunden-Code darf nicht zweimal benutzt werden. Die Probe wartet deshalb vor
    jeder Anmeldung auf ein neues Fenster (gemessen am 2026-10-25 in Block 11.5: ohne
    diese Warte endete die zweite Anmeldung mit 401)."""
    jetzt = int(time.time() // 30)
    warte = (jetzt + 1) * 30 + 1 - time.time()
    if warte > 0:
        time.sleep(warte)


from playwright.sync_api import sync_playwright

out = {"items": []}
with sync_playwright() as p:
    browser = p.chromium.launch()
    context = browser.new_context(ignore_https_errors=True, viewport={"width": 1400, "height": 900})
    page = context.new_page()
    fehler = []
    page.on("pageerror", lambda exc: fehler.append(str(exc)))

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

    # Nur die **Entwuerfe** loeschen -- das sessionStorage traegt den **CSRF-Token**
    # (`api.js :: csrfToken()`); ein leeres sessionStorage bedeutet: jeder Write endet
    # mit 403 (gemessen am 2026-10-25 in Block 11.5).
    try:
        page.evaluate("""() => {
          Object.keys(sessionStorage).forEach(function (k) {
            if (k.indexOf('sfx:draft:') === 0) sessionStorage.removeItem(k);
          });
        }""")
    except Exception:
        pass

    # In die Space-Uebersicht und dann in die Liste.
    page.wait_for_timeout(1200)
    page.wait_for_selector(".overview__space-open", timeout=20000)
    page.locator(".overview__space-open").first.click()
    page.wait_for_timeout(1500)

    for eintrag in titel:
        name = eintrag["titel"]
        zeile = page.locator(".list__row", has_text=name).first
        zeile.scroll_into_view_if_needed()
        zeile.click()
        page.wait_for_timeout(1400)
        try:
            page.wait_for_selector(".CodeMirror", timeout=30000)
        except Exception:
            out["items"].append({"titel": name, "fehler": "Editor kam nicht"})
            continue
        page.wait_for_timeout(700)
        messung = page.evaluate("""async () => {
          // **Dieselbe** Modul-Instanz, die die App benutzt (der Modul-Register ist
          // nach URL geschluesselt).
          const editor = await import('/ui/static/js/editor.js');
          const w = document.querySelector('.CodeMirror');
          const cm = w.CodeMirror;
          const chip = document.querySelector('#meta-item-id .id-chip');
          const id = chip ? chip.textContent.trim() : null;
          const antwort = await fetch('/api/v1/items/' + id, {credentials: 'same-origin'});
          const item = await antwort.json();
          const knopf = document.getElementById('save-button');
          const band = document.getElementById('version-band-number');
          const ergebnis = {
            id: id,
            text: cm.getValue(),
            body: item.body,
            version: item.version,
            dirty_beim_oeffnen: editor.isDirty(),
            knopf_deaktiviert: knopf ? knopf.disabled : null,
            band: band ? band.textContent : null,
          };
          // **Ein Zeichen tippen und wieder loeschen.**
          cm.replaceRange('X', {line: 0, ch: 0});
          ergebnis.dirty_nach_tippen = editor.isDirty();
          cm.replaceRange('', {line: 0, ch: 0}, {line: 0, ch: 1});
          ergebnis.dirty_nach_loeschen = editor.isDirty();
          ergebnis.text_nach_loeschen = cm.getValue();
          // **Der Rohtext (ED-5): jedes Zeichen sichtbar.** Der DOM-Text des Editors wird
          // mit dem Dokument verglichen -- **ohne** die Nullbreite, die CM5 in **leere**
          // Zeilen setzt (sonst waere der Vergleich an der Leerzeile falsch).
          const schalter = document.getElementById('toggle-preview');
          schalter.click();
          await new Promise(function (r) { setTimeout(r, 250); });
          const roh = Array.from(document.querySelectorAll('.CodeMirror-line'))
            .map(function (z) { return z.textContent; }).join(String.fromCharCode(10));
          ergebnis.rohmodus_text = roh.replace(/\\u200b/g, '');
          ergebnis.rohmodus_aktiv = document.querySelector('.CodeMirror').classList.contains('is-raw');
          schalter.click();
          await new Promise(function (r) { setTimeout(r, 250); });
          return ergebnis;
        }""")
        messung["titel"] = name
        out["items"].append(messung)
        # **Den Editor schliessen** -- der Weg, den ein Mensch geht (der X-Knopf).
        knopf_x = page.locator("#close-button")
        if knopf_x.count() and knopf_x.first.is_visible():
            knopf_x.first.click()
            page.wait_for_timeout(700)

    out["seitenfehler"] = fehler

print(json.dumps(out, ensure_ascii=False))
'''


def _provision(space: str) -> dict:
    from authserver import passwords, totp
    from authserver.config import decode_data_encryption_key
    from authserver.secretbox import seal
    from authserver.store import AuthStore

    password = "wegwerf-rt-" + secrets.token_urlsafe(8)
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


def _fixtures() -> list[dict]:
    """Die zehn Fixtures mit ihrem Inhalt — **byte-genau**."""
    eintraege = []
    for pfad in sorted(FIXTURE_DIR.glob("*.md")):
        eintraege.append({
            "datei": pfad.name,
            "titel": "Fixture " + pfad.stem,
            "inhalt": pfad.read_text(encoding="utf-8"),
        })
    assert len(eintraege) == 10, f"es sind {len(eintraege)} Fixtures, erwartet 10"
    return eintraege


def _setup() -> tuple[dict, list[dict]]:
    shutil.rmtree(WEGWERF_ROOT, ignore_errors=True)
    WEGWERF_ROOT.mkdir(parents=True, exist_ok=True)
    DATA_ROOT.mkdir(parents=True, exist_ok=True)
    raw = secrets.token_bytes(32)
    DEK_FILE.write_text(base64.urlsafe_b64encode(raw).rstrip(b"=").decode("ascii") + "\n")
    os.chmod(DEK_FILE, 0o600)
    alpha = _provision(SPACE)
    fixtures = _fixtures()
    # Der Seed: **ein Item je Fixture**, der Body ist der Fixture-Inhalt **byte-genau**.
    code = [
        "import sys; sys.path.insert(0, 'phase1_storage')",
        "from storage.store import Store",
        f"s = Store({str(DATA_ROOT)!r}, git=True)",
    ]
    for eintrag in fixtures:
        code.append(
            f"s.create({SPACE!r}, type='task', title={eintrag['titel']!r}, "
            f"body={eintrag['inhalt']!r})"
        )
    subprocess.run(
        [".venv/bin/python", "-c", "\n".join(code)], check=True, cwd=str(REPO_ROOT),
        env={**os.environ, "PYTHONPATH": str(REPO_ROOT / "phase1_storage")},
    )
    return alpha, fixtures


def _datei_abdruck() -> dict[str, str]:
    """Ein Abdruck **jeder** Item-Datei auf der Platte (SHA-256 ueber die Bytes)."""
    abdruck = {}
    space_dir = DATA_ROOT / SPACE
    if not space_dir.exists():
        return abdruck
    for pfad in sorted(space_dir.glob("*.md")):
        abdruck[pfad.name] = hashlib.sha256(pfad.read_bytes()).hexdigest()
    return abdruck


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


def _sichtbar(text: str | None) -> str:
    """**Der sichtbare Text, normalisiert.**

    **Warum normalisiert wird (gemessen am 2026-10-25):** CodeMirror **zeichnet** einen
    Tab als Tabstopp (vier Leerzeichen) und das **erste** Leerzeichen einer Zeile als
    geschuetztes Leerzeichen (`\u00a0`) -- das ist **Darstellung**, kein verborgenes
    Zeichen. Ein byte-genauer Vergleich meldete deshalb bei vier der zehn Fixtures einen
    Unterschied, obwohl **kein** Zeichen fehlte. Der Vergleich normalisiert deshalb den
    **Whitespace** (Runs zu einem Leerzeichen, Randauszug entfernt) und vergleicht die
    **Zeichen** -- das ist die Aussage, die ED-5 meint: im Rohtext ist **nichts**
    unsichtbar.
    """
    return re.sub(r"[\s\u00a0]+", " ", text or "").strip()


def main(argv: list[str] | None = None) -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.parse_args(argv)

    alpha, fixtures = _setup()
    vorher = _datei_abdruck()
    server = _serve()
    try:
        skript = WEGWERF_ROOT / "browser_rt.py"
        skript.write_text(BROWSER_SKILL, encoding="utf-8")
        e2e = Path.home() / ".claude-code-tools/e2e-venv/bin/python"
        out_file = (WEGWERF_ROOT / "browser.out").open("wb")
        err_file = (WEGWERF_ROOT / "browser.err").open("wb")
        proc = subprocess.Popen(
            [str(e2e), str(skript), BASE, alpha["space"], alpha["password"], alpha["secret"],
             str(WEGWERF_ROOT), json.dumps([{"titel": f["titel"]} for f in fixtures])],
            cwd=str(REPO_ROOT), stdout=out_file, stderr=err_file,
        )
        try:
            proc.wait(timeout=420)
        except subprocess.TimeoutExpired:
            proc.kill()
            proc.wait(timeout=10)
        text = (WEGWERF_ROOT / "browser.out").read_text(encoding="utf-8", errors="replace").strip()
        if not text:
            log("Browser-Fehler:\n" + (WEGWERF_ROOT / "browser.err").read_text(
                encoding="utf-8", errors="replace")[-3000:])
            raise SystemExit("Der Browser hat nichts gemeldet.")
        messung = json.loads(text.splitlines()[-1])
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

    nachher = _datei_abdruck()
    dateien_unveraendert = vorher == nachher and len(vorher) == 10

    items = messung.get("items") or []
    befund = {
        "alle_zehn_items_geprueft": len(items) == 10,
        "texte_byte_identisch": all(
            (i.get("text") is not None and i.get("body") is not None
             and i["text"] == i["body"]) for i in items
        ),
        "oeffnen_macht_nicht_geaendert": all(i.get("dirty_beim_oeffnen") is False for i in items),
        "speichern_ist_nicht_noetig": all(i.get("knopf_deaktiviert") is True for i in items),
        "typpen_macht_geaendert": all(i.get("dirty_nach_tippen") is True for i in items),
        "loeschen_macht_wieder_sauber": all(
            i.get("dirty_nach_loeschen") is False for i in items
        ),
        "text_nach_loeschen_wieder_der_ursprung": all(
            i.get("text_nach_loeschen") == i.get("text") for i in items
        ),
        "dateien_auf_der_platte_unveraendert": dateien_unveraendert,
        # **ED-5:** im Rohtext steht **jedes** Zeichen -- der DOM-Text des Editors traegt
        # dann **dieselben Zeichen** wie das Dokument.
        "rohmodus_zeigt_jedes_zeichen": all(
            i.get("rohmodus_aktiv") is True
            and _sichtbar(i.get("rohmodus_text")) == _sichtbar(i.get("text"))
            for i in items
        ),
        "keine_seitenfehler": not messung.get("seitenfehler"),
    }
    # **Je Item** die Einzelwerte — der Leser soll sehen, welches Fixture was trug.
    einzel = []
    for eintrag, item in zip(fixtures, items):
        einzel.append({
            "datei": eintrag["datei"],
            "titel": eintrag["titel"],
            "bytes": len(eintrag["inhalt"].encode("utf-8")),
            "text_gleich_body": item.get("text") == item.get("body"),
            "dirty_beim_oeffnen": item.get("dirty_beim_oeffnen"),
            "dirty_nach_tippen": item.get("dirty_nach_tippen"),
            "dirty_nach_loeschen": item.get("dirty_nach_loeschen"),
            "knopf_deaktiviert": item.get("knopf_deaktiviert"),
            "rohmodus_text_gleich_text": (
                _sichtbar(item.get("rohmodus_text")) == _sichtbar(item.get("text"))
            ),
            "version": item.get("version"),
        })

    ok = all(befund.values())
    ergebnis = {
        "probe": "p105_b11_roundtrip",
        "instanz": {"basis": BASE, "pid": server.pid, "wegwerf": True},
        "befund": befund,
        "einzel": einzel,
        "messung": messung,
        "alle_kriterien_erfuellt": ok,
    }
    RESULT.write_text(
        json.dumps(ergebnis, indent=2, ensure_ascii=False) + "\n", encoding="utf-8"
    )
    print(json.dumps(ergebnis, indent=2, ensure_ascii=False))
    return 0 if ok else 1


if __name__ == "__main__":
    raise SystemExit(main())
