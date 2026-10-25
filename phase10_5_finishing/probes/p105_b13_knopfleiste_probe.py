#!/usr/bin/env python3
"""P10.5 Block 13 — die **Knopfleiste nach Word** und die **Editor-Groessen**.

Wegwerf-Instanz (**freier Port je Lauf**, tmp-`DATA_ROOT` mit **eigenem Baum je Lauf**,
tmp-`auth.sqlite3`, Stopp nur über die PID-Datei — Hard Rule 9, **nicht** gegen den
laufenden Dienst). Gemessen wird im **echten
Browser**: Schriftgroesse, Zeilenhoehe, Cursorposition, DOM-Reihenfolge, Knopfmasse und
Knopfflaeche sind Darstellungswerte — sie stehen in keiner Quelldatei.

| # | Zelle | was sie beweist |
|---|---|---|
| 1 | `groesse_wirkt` | `[gross]` ist groesser, `[klein]` kleiner als der normale Text (px) |
| 2 | `zeile_springt_nicht` | die Zeile mit `[gross]` ist **so hoch wie** eine normale Zeile |
| 3 | `cursor_auf_dem_zeichen` | der Cursor landet **exakt** auf dem geklickten Zeichen (V211) |
| 4 | `reihenfolge_word` | die DOM-Reihenfolge der Leiste ist die **Word-Reihenfolge** |
| 5 | `knoepfe_gleich` | alle Knöpfe sind gleich hoch und gleich breit |
| 6 | `gruppen_vier` | **vier** Format-Gruppen + der Modus-Schalter, mit Trennern dazwischen |
| 7 | `flaeche_transparent_blau` | die Standardflaeche ist das **blaue, halbtransparente** Design |
| 8 | `keine_entity_icons` | keine HTML-Entity-Zeichen als Icons mehr (Verbotsliste §0.3) |

**Gegenlauf `--gegenlauf`:** die alte Fassung wiederherstellen — die Probe muss dann **rot**
werden. Ohne diesen Lauf beweist die grüne Probe nichts.

Aufruf:  `.venv/bin/python phase10_5_finishing/probes/p105_b13_knopfleiste_probe.py
         [--gegenlauf groesse|zeile|reihenfolge|flaeche|alle]`
Ergebnis: `phase10_5_finishing/probes/p105_b13_knopfleiste_probe.json`
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
WEGWERF_ROOT = Path("/tmp/opencode/sharefyx-wegwerf-b13")
# **Der Datenwurzel-Baum ist je Lauf eigenes** (PID im Namen). Grund (Fund vom 2026-10-25):
# ein zurueckgebliebener Server aus dem **vorigen** Lauf hat seinen Index in die *neue*
# Instanz geschrieben — die alte Zeile (`itm_242ae8c5`) stand im Index, die Datei auf der
# Platte hatte eine andere ID (`itm_02172e08`), und die Uebersicht lief in einen **500**
# (`FileNotFoundError` im Store). Ein eigener Baum pro Lauf macht das unmoeglich: kein
# Prozess teilt sich einen Pfad mit einem anderen Lauf.
DATA_ROOT = WEGWERF_ROOT / ("data-%d" % os.getpid())
AUTH_DB = WEGWERF_ROOT / "auth.sqlite3"
DEK_FILE = WEGWERF_ROOT / "auth-dek"
SERVE_PID = WEGWERF_ROOT / "serve.pid"
SERVE_LOG = WEGWERF_ROOT / "serve.log"
# **Der Port ist je Lauf frei** (Fund vom 2026-10-25): ein zurueckgebliebener Wegwerf-Server
# aus dem vorigen Lauf hielt den festen Port — der neue Server startete nicht
# ("address already in use"), und der Browser sprach mit dem **alten** Prozess (anderer
# Datenwurzel-Baum → die Uebersicht lief in einen 500). Ein freier Port pro Lauf macht das
# unmoeglich. Die **Wahl des Ports ist nicht die Sache des Anwenders** — der Port ist Wegwerf.
PORT = 0
BASE = ""


def _freier_port() -> int:
    """Ein freier TCP-Port auf dem Loopback (Bind auf 0, dann schliessen)."""
    import socket
    with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
        s.bind(("127.0.0.1", 0))
        return int(s.getsockname()[1])
SPACE = "alpha"
RESULT = Path(__file__).resolve().with_name("p105_b13_knopfleiste_probe.json")

CSS_FILE = REPO_ROOT / "phase5_ui/webui/static/app.css"
JS_FILE = REPO_ROOT / "phase5_ui/webui/static/js/editor.js"
HTML_FILE = REPO_ROOT / "phase5_ui/webui/static/app.html"

# Die **erwartete Reihenfolge** — 1:1 nach dem Start-Ribbon von Word (s. den Kommentar in
# `app.html`). Die Liste steht hier **zweimal**: einmal als Soll und einmal als Ist-Messung
# im Browser. Ein Wächter, der nur die Quelle liest, wäre die Kopie davon — der Browser
# ist die Wahrheit (die Quelle kann eine Reihenfolge haben, die der Browser umsortiert).
WORD_REIHENFOLGE = [
    "bold", "italic", "code", "format-farbe", "format-groesse",
    "ul", "ol", "format-ausrichtung",
    "h", "quote",
    "image", "hr", "link",
    "toggle-preview",
]

# Die Gegenläufe: (Datei, alter Text, neuer Text). **Die Anker sind eindeutig** (eine
# Regel plus Nachbarzeile), nicht nur ein Wert — sonst trifft der Patch den Kommentar
# statt der Regel (das ist im Repo zweimal passiert).
GEGENLAEUFE = {
    # Der alte Overlay: nur die Farbe, die Groesse faerbt nichts.
    "groesse": [(JS_FILE,
                 "  function klasse(a, b) {\n"
                 "    var r = [];\n"
                 "    var farbe = null;\n"
                 "    var groesse = null;\n"
                 "    var namen = [a, b].filter(Boolean);\n"
                 "    for (var i = 0; i < namen.length; i++) {\n"
                 "      var n = namen[i];\n"
                 "      if (V.farben[n]) {\n"
                 "        if (farbe) return null;                 // **zwei** Farben: nicht erlaubt\n"
                 "        farbe = V.farben[n];\n"
                 "      } else if (V.groessen[n]) {\n"
                 "        if (groesse) return null;               // **zwei** Groessen: nicht erlaubt\n"
                 "        groesse = V.groessen[n];\n"
                 "      } else {\n"
                 "        return null;                            // unbekannte Klasse: **woertlich**\n"
                 "      }\n"
                 "    }\n"
                 "    if (!farbe && !groesse) return null;\n"
                 "    if (farbe) r.push(farbe);\n"
                 "    if (groesse) r.push(groesse);\n"
                 "    if (!farbe) r.push(\"md-plain\");\n"
                 "    return r.join(\" \");\n"
                 "  }",
                 "  function klasse(a, b) {\n"
                 "    var k = [a, b].filter(Boolean);\n"
                 "    for (var n = 0; n < k.length; n++) if (!V.farben[k[n]] && !V.groessen[k[n]]) return null;\n"
                 "    for (var f = 0; f < k.length; f++) if (V.farben[k[f]]) return V.farben[k[f]];\n"
                 "    return k.length ? \"md-plain\" : null;\n"
                 "  }")],
    # Die alte relative Zeilenhoehe: mit ihr springt die Zeile.
    "zeile": [(CSS_FILE, "  line-height: 21px;\n}", "  line-height: 1.6;\n}")],
    # Die alte Reihenfolge: Link vor H (und Zitat/Liste an anderer Stelle).
    "reihenfolge": [(HTML_FILE,
                     '              <button type="button" class="toolbar-btn" data-md="code" title="Code"',
                     '              <button type="button" class="toolbar-btn" data-md="link" title="Link" aria-label="Link"><svg class="icon" aria-hidden="true"><use href="#i-link"></use></svg></button>\n'
                     '              <button type="button" class="toolbar-btn" data-md="code" title="Code"')],
    # Die alte deckende Flaeche.
    "flaeche": [(CSS_FILE,
                 "  --btn-std-fill:        linear-gradient(180deg, rgba(62,141,243,.20), rgba(62,141,243,.08));",
                 "  --btn-std-fill:        linear-gradient(180deg, #0C1C31, #050B13);")],
}

BODY = (
    "# Formate\n\n"
    "Normaler Text auf einer eigenen Zeile.\n\n"
    "[klein]{.klein} klein\n"
    "[normal]{.normal} normal\n"
    "[gross]{.gross} gross\n"
    "[rot]{.rot} [rot gross]{.rot .gross} beides\n"
)

BROWSER_SKILL = r'''import json, sys, time, hmac, hashlib, struct

base, space, password, secret = sys.argv[1:5]

def totp_now(secret_b32):
    key = base64.b32decode(secret_b32 + "=" * (-len(secret_b32) % 8))
    counter = int(time.time() // 30)
    digest = hmac.new(key, struct.pack(">q", counter), hashlib.sha1).digest()
    # **Das LETZTE** Byte des Digests (RFC 4226, §5.3) — `digest[0]` ist der falsche
    # Offset und liefert einen Code, den der Server nie annimmt. (Der Fehler stand
    # zuerst in dieser Datei und hat den **Login der Probe** totgeprueft: 401, und die
    # Probe meldete acht rote Zellen — ein Messgeraet, das die falsche Sache misst.)
    offset = digest[-1] & 0x0F
    code = (struct.unpack(">I", digest[offset:offset + 4])[0] & 0x7FFFFFFF) % 1000000
    return f"{code:06d}"

import base64
from playwright.sync_api import sync_playwright

MESS = """
() => {
  const OUT = {};

  // -- 1/2) Die Groessen im Live-Editor: die *berechnete* Schriftgroesse der Textspans
  //        und die Hoehe der Zeile, in der sie stehen.
  const cm = document.querySelector('.CodeMirror');
  const ref = cm ? getComputedStyle(cm) : null;
  const spans = {
    klein: document.querySelector('.CodeMirror .cm-md-s-klein'),
    normal: document.querySelector('.CodeMirror .cm-md-s-normal'),
    gross: document.querySelector('.CodeMirror .cm-md-s-gross'),
  };
  OUT.schrift = {basis: ref ? ref.fontSize : null};
  for (const k of Object.keys(spans)) {
    const el = spans[k];
    OUT.schrift[k] = el ? getComputedStyle(el).fontSize : null;
    OUT.schrift[k + "_klasse"] = el ? el.className : null;
  }
  const hoehe = (span) => {
    if (!span) return null;
    const line = span.closest('.CodeMirror-line');
    return line ? line.getBoundingClientRect().height : null;
  };
  OUT.zeilenhoehe = {
    klein: hoehe(spans.klein),
    normal: hoehe(spans.normal),
    gross: hoehe(spans.gross),
  };

  // -- 3) Der Cursor: die *letzte* Textstelle der Zeile "gross" (das sichtbare Wort nach
  //        der Form) und ihr Index im Dokument (die DOM-Zeilen zaehlen die versteckten
  //        Formatierungszeichen mit — der Index ist also der Dokument-Index).
  const ziel = (() => {
    const el = spans.gross;
    if (!el) return null;
    const line = el.closest('.CodeMirror-line');
    if (!line) return null;
    const walker = document.createTreeWalker(line, NodeFilter.SHOW_TEXT);
    let node, letzter = null, offset = 0;
    while ((node = walker.nextNode())) {
      const t = node.textContent;
      if (node.parentElement && node.parentElement.classList.contains('cm-md-s-gross')
          && t.trim() === 'gross') {
        letzter = {node: node, offset: offset};
      }
      offset += t.length;
    }
    if (!letzter) return null;
    const range = document.createRange();
    range.selectNodeContents(letzter.node);
    const r = range.getBoundingClientRect();
    return {x: r.left, y: r.top + r.height / 2, ch: letzter.offset};
  })();
  OUT.ziel = ziel;

  // -- 4) Die Reihenfolge der Leiste (DOM, nicht Quelle).
  const bar = document.querySelector('#editor-toolbar');
  OUT.reihenfolge = bar
    ? Array.from(bar.querySelectorAll('button, select')).map(el => el.dataset.md || el.id)
    : null;

  // -- 5) Die Masse der Knöpfe.
  const knoepfe = bar ? Array.from(bar.querySelectorAll('.toolbar-btn')) : [];
  OUT.knoepfe = knoepfe.map(el => {
    const r = el.getBoundingClientRect();
    return {md: el.dataset.md || el.id, w: Math.round(r.width * 100) / 100,
            h: Math.round(r.height * 100) / 100};
  });
  OUT.icons = knoepfe.map(el => {
    const svg = el.querySelector('svg.icon');
    const r = (svg || el).getBoundingClientRect();
    return {md: el.dataset.md || el.id, icon: !!svg,
            w: Math.round(r.width * 100) / 100, h: Math.round(r.height * 100) / 100};
  });

  // -- 6) Die Gruppen und ihre Trenner.
  const gruppen = bar ? Array.from(bar.querySelectorAll('.toolbar-group')) : [];
  OUT.gruppen = gruppen.map(g => ({
    name: g.dataset.wordGroup || null,
    kinder: g.children.length,
    trenner: getComputedStyle(g).borderLeftWidth,
  }));

  // -- 7) Die Standardflaeche: der *Verlauf* ist das halbtransparente Blau.
  const btn = document.querySelector('#archive-button');
  const tb = document.querySelector('#editor-toolbar .toolbar-btn');
  const bg = (el) => el ? getComputedStyle(el).backgroundImage : null;
  OUT.flaeche = {archivieren: bg(btn), toolbar: bg(tb),
                 hover: btn ? getComputedStyle(btn).getPropertyValue('--btn-std-fill-hover') : null};

  // -- 8) Keine HTML-Entity-Zeichen als Icons mehr.
  OUT.entities = knoepfe.filter(el => {
    const t = (el.textContent || '').trim();
    return t === '•' || t === '—' || t === '</>' || t === 'H' || t === '1.';
  }).map(el => el.dataset.md || el.id);

  return OUT;
}
"""

out = {"schritte": []}
with sync_playwright() as p:
    br = p.chromium.launch()
    page = br.new_page(viewport={"width": 1400, "height": 900})
    fehler = []
    page.on("pageerror", lambda e: fehler.append(str(e)))
    page.goto(base + "/ui/login", wait_until="domcontentloaded")
    page.fill('input[name="space"]', space)
    page.fill('input[name="password"]', password)
    page.fill('input[name="totp"]', totp_now(secret))
    page.click('form[action="/ui/login"] button[type="submit"]')
    page.wait_for_selector("#shell", timeout=30000)
    page.wait_for_selector(".overview__space-open", timeout=20000)
    page.locator(".overview__space-open").first.click()
    page.wait_for_timeout(1000)
    page.locator(".list__row", has_text="Formate").first.click()
    page.wait_for_selector(".CodeMirror", timeout=30000)
    page.wait_for_timeout(1200)

    mess = page.evaluate(MESS)
    out["messung"] = mess

    # Der Cursor: klicken und die Cursorposition lesen.
    ziel = mess.get("ziel")
    cursor = None
    if ziel:
        page.mouse.click(ziel["x"] + 1, ziel["y"])
        page.wait_for_timeout(400)
        cursor = page.evaluate("""() => {
          const w = document.querySelector('.CodeMirror');
          if (!w || !w.CodeMirror) return null;
          const c = w.CodeMirror.getCursor();
          return {line: c.line, ch: c.ch};
        }""")
    out["cursor"] = cursor
    out["cursor_ziel_ch"] = ziel["ch"] if ziel else None
    out["seitenfehler"] = fehler
    br.close()
print(json.dumps(out, ensure_ascii=False))
'''


def _setup() -> dict:
    WEGWERF_ROOT.mkdir(parents=True, exist_ok=True)
    DATA_ROOT.mkdir(parents=True, exist_ok=True)
    if not DEK_FILE.exists():
        raw = secrets.token_bytes(32)
        DEK_FILE.write_text(base64.urlsafe_b64encode(raw).rstrip(b"=").decode("ascii") + "\n")
        os.chmod(DEK_FILE, 0o600)
    from authserver import passwords, totp
    from authserver.config import decode_data_encryption_key
    from authserver.secretbox import seal
    from authserver.store import AuthStore

    password = "wegwerf-b13-" + secrets.token_urlsafe(8)
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


def _seed_item() -> None:
    shutil.rmtree(DATA_ROOT, ignore_errors=True)
    DATA_ROOT.mkdir(parents=True, exist_ok=True)
    code = (
        "import sys; sys.path.insert(0, 'phase1_storage')\n"
        "from storage.store import Store\n"
        f"s = Store({str(DATA_ROOT)!r}, git=False)\n"
        f"s.create({SPACE!r}, type='task', title='Formate', body={BODY!r})\n"
    )
    subprocess.run([".venv/bin/python", "-c", code], check=True, cwd=str(REPO_ROOT),
                   env={**os.environ, "PYTHONPATH": str(REPO_ROOT / "phase1_storage")})


def _serve() -> int:
    env = os.environ.copy()
    env["SPACE_DATA_ROOT"] = str(DATA_ROOT)
    env["SPACE_AUTH_DB"] = str(AUTH_DB)
    env["SPACE_PUBLIC_BASE_URL"] = "https://wegwerf-b13.invalid"
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
    # **Der Stopp wird geprueft, nicht angenommen** (Hard Rule 9: kein `pkill -f`, kein
    # Regex — und kein "wird schon"). Ein zurueckgebliebener Server ist genau der Fund
    # vom 2026-10-25 (er hat den Index der naechsten Instanz ueberschrieben).
    if Path(f"/proc/{pid}").exists():
        print(f"WARNUNG: der Wegwerf-Server {pid} lebt noch — er wird per PID beendet.",
              file=sys.stderr)
        try:
            os.kill(pid, signal.SIGKILL)
        except ProcessLookupError:
            pass
        for _ in range(20):
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
        return {"fehler": proc.stderr[-2000:]}
    return json.loads(proc.stdout.strip().splitlines()[-1])


def _px(wert) -> float:
    """'13px' -> 13.0 (und None -> -1)."""
    if not wert:
        return -1.0
    return float(str(wert).replace("px", ""))


def main(argv: list[str] | None = None) -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--gegenlauf", nargs="?", const="alle",
                        choices=["groesse", "zeile", "reihenfolge", "flaeche", "alle"],
                        help="die alte Fassung wiederherstellen — die Probe muss dann rot werden")
    args = parser.parse_args(argv)

    patches: list[tuple[Path, str, str]] = []
    if args.gegenlauf:
        keys = list(GEGENLAEUFE) if args.gegenlauf == "alle" else [args.gegenlauf]
        for key in keys:
            patches.extend(GEGENLAEUFE[key])

    original: dict[Path, str] = {}
    for datei, alt, neu in patches:
        if datei not in original:
            original[datei] = datei.read_text(encoding="utf-8")
        inhalt = datei.read_text(encoding="utf-8")
        assert alt in inhalt, (
            f"der Gegenlauf passt nicht mehr auf {datei}: {alt!r} — die Anker stimmen nicht "
            f"mehr (oder der Defekt ist schon zurueckgedreht)"
        )
        datei.write_text(inhalt.replace(alt, neu, 1), encoding="utf-8")

    global PORT, BASE
    PORT = _freier_port()
    BASE = f"http://127.0.0.1:{PORT}"

    RESULT.unlink(missing_ok=True)
    try:
        user = _setup()
        _seed_item()
        pid = _serve()
        try:
            b = _browser(user)
        finally:
            _stop()

        mess = b.get("messung") or {}
        schrift = mess.get("schrift") or {}
        hoehen = mess.get("zeilenhoehe") or {}
        knoepfe = mess.get("knoepfe") or []
        icons = mess.get("icons") or []
        gruppen = mess.get("gruppen") or []
        flaeche = mess.get("flaeche") or {}

        basis = _px(schrift.get("basis"))
        klein = _px(schrift.get("klein"))
        gross = _px(schrift.get("gross"))
        normal_zeile = hoehen.get("normal") or 0
        gross_zeile = hoehen.get("gross") or 0
        klein_zeile = hoehen.get("klein") or 0

        befund = {
            "groesse_wirkt": (
                basis > 0 and klein > 0 and gross > 0
                and klein <= basis * 0.90
                and gross >= basis * 1.15
            ),
            "zeile_springt_nicht": (
                normal_zeile > 0 and gross_zeile > 0 and klein_zeile > 0
                and abs(gross_zeile - normal_zeile) <= 1.0
                and abs(klein_zeile - normal_zeile) <= 1.0
            ),
            "cursor_auf_dem_zeichen": (
                b.get("cursor") is not None
                and b.get("cursor_ziel_ch") is not None
                and b["cursor"]["ch"] == b["cursor_ziel_ch"]
            ),
            "reihenfolge_word": mess.get("reihenfolge") == WORD_REIHENFOLGE,
            "knoepfe_gleich": (
                len(knoepfe) > 0
                and all(abs(k["h"] - 24.0) <= 0.6 for k in knoepfe)
                and len({round(k["w"], 1) for k in icons if k["icon"]}) <= 1
            ),
            "gruppen_vier": (
                len(gruppen) == 5
                and all(g["trenner"] == "0px" for g in gruppen[:1])
                and all(g["trenner"] == "1px" for g in gruppen[1:])
            ),
            "flaeche_transparent_blau": (
                "rgba(62, 141, 243" in (flaeche.get("archivieren") or "")
                and "rgba(62, 141, 243" in (flaeche.get("toolbar") or "")
            ),
            "keine_entity_icons": not mess.get("entities"),
        }
        ok = all(befund.values()) and not b.get("seitenfehler") and "fehler" not in b
        ergebnis = {
            "probe": "p105_b13_knopfleiste",
            "instanz": {"basis": BASE, "pid": pid, "wegwerf": True},
            "gegenlauf": args.gegenlauf,
            "befund": befund,
            "alle_ok": ok,
            "messung": mess,
            "cursor": b.get("cursor"),
            "cursor_ziel_ch": b.get("cursor_ziel_ch"),
            "seitenfehler": b.get("seitenfehler"),
            "fehler": b.get("fehler"),
        }
        RESULT.write_text(json.dumps(ergebnis, ensure_ascii=False, indent=2), encoding="utf-8")
        print(json.dumps({"alle_ok": ok, "befund": befund}, ensure_ascii=False))
        return 0 if ok else 1
    finally:
        for datei, inhalt in original.items():
            datei.write_text(inhalt, encoding="utf-8")


if __name__ == "__main__":
    sys.exit(main())
