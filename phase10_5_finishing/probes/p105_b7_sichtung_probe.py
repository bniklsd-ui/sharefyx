#!/usr/bin/env python3
"""P10.5 Block 7, Schritt 7.4 (UI-4) — die vier Posten der Sichtung vom 2026-10-24.

Wegwerf-Instanz (Port **18793**, tmp-`DATA_ROOT`, PID-Datei, Hard Rule 9 — **nicht** gegen den
laufenden Dienst). Gemessen wird im **echten Browser**, nicht in der Quelle: die Zahlen, die
der Nikinger gesehen hat (5,6 px Wortmarken-Abstand, ~140 px Banner-Höhe, „v316"), sind
Darstellungswerte — sie stehen in keiner Quelldatei.

| Posten | gemessen |
|---|---|
| 1 Wortmarken-Abstand | der Abstand zwischen dem Zeichen und dem Wortrest (px) |
| 2 „Zugewiesen"-Auswahl | die Kanten der Auswahl gegen die Kanten der Suchzeile darüber |
| 3 Update-Banner | die Höhe der Leiste und die Zahl ihrer Zeilen |
| 4 Versionsanzeige | die Größe des Punktes in der gerechneten Schrift und sein Abstand zum Nachbarn |

**Gegenlauf `--gegenlauf`:** die alte Fassung wiederherstellen — die Probe muss dann **rot**
werden. Ohne diesen Lauf beweist die grüne Probe nichts: ein Messgerät, das die falsche
Sache misst, ist grün und falsch zugleich (die Fehlerklasse, die dieser Ordner zweimal
gesehen hat).

Aufruf:  `.venv/bin/python phase10_5_finishing/probes/p105_b7_sichtung_probe.py
         [--gegenlauf mark|auswahl|banner|version|alle]`
Ergebnis: `phase10_5_finishing/probes/p105_b7_sichtung_probe.json`
Bilder:   `<Wegwerf-Root>/b74_*.png` (Wegwerf-Ordner, **nicht** im Repo)
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
WEGWERF_ROOT = Path("/tmp/opencode/sharefyx-wegwerf-b74")
DATA_ROOT = WEGWERF_ROOT / "data"
AUTH_DB = WEGWERF_ROOT / "auth.sqlite3"
DEK_FILE = WEGWERF_ROOT / "auth-dek"
SERVE_PID = WEGWERF_ROOT / "serve.pid"
SERVE_LOG = WEGWERF_ROOT / "serve.log"
PORT = 18793
BASE = f"http://127.0.0.1:{PORT}"
SPACE = "alpha"
RESULT = Path(__file__).resolve().with_name("p105_b7_sichtung_probe.json")
CSS_FILE = REPO_ROOT / "phase5_ui/webui/static/app.css"
JS_FILE = REPO_ROOT / "phase5_ui/webui/static/js/updates.js"

# -- Die Grenzwerte der Messung. Jeder ist an der Anforderung festgemacht, nicht am
#    aktuellen Wert nachgerechnet ("grün, weil es so ist" ist kein Beleg).
MAX_MARK_GAP_PX = 4.0        # der Abstand war 5,9 px (`.45em` bei 12,5 px) — der Nikinger
                              # nannte ihn zu groß; 4 px ist die Obergrenze, 0 ist verboten
                              # (sonst klebt das Zeichen am Wortrest)
MAX_BANNER_H_PX = 60.0       # eine einzeilige Leiste: die Knoepfe bestimmen die Hoehe
                              # (49 px gemessen) -- der alte Banner waechs mit dem Log-Eintrag
                              # (76 px bei drei Zeilen, ~140 px bei fuenf)
MIN_DOT_PEAK = 190.0         # der hellste Pixel des Punktes (0-255): bei 9 px waren es 155
                              # (61 %) -- der Punkt verblasste in den Grund, das ist der
                              # Befund „v316". Bei 11 px sind es 203 (80 %).
MIN_DOT_AREA = 2             # Pixel: ein Punkt ist kein einzelner Pixel
MIN_DOT_GAP_PX = 1.0         # und er muss vom Nachbarzeichen getrennt bleiben (eine Lücke)

# -- Die alten Werte (Gegenlauf). Jeder Eintrag: (Datei, alter Text, neuer Text).
#    **Die Anker sind eindeutig** (Regel + Nachbarzeile, nicht nur ein Wert): der erste
#    Entwurf take `margin-right: .2em;` — das stand auch im Kommentar ueber der Regel, und
#    der Gegenlauf hat den Kommentar gepatcht statt die Regel. Die Probe war danach gruen
#    und der Defekt nicht wiederhergestellt: ein Gegenlauf, der nichts wiederherstellt,
#    beweist nichts. Genau das ist der Fehler, den die erste Fassung dieses Laufs hatte.
GEGENLAEUFE = {
    "mark": [(CSS_FILE,
              "  vertical-align: -.22em;\n  margin-right: .2em;",
              "  vertical-align: -.22em;\n  margin-right: .45em;")],
    "auswahl": [(CSS_FILE,
                 ".list__assignee {\n  width: calc(100% - var(--space) * 4);\n"
                 "  margin: var(--space) calc(var(--space) * 2) 0;\n}",
                 ".list__assignee {\n  width: 100%;\n  margin-top: var(--space);\n}")],
    "banner": [
        (CSS_FILE, "  padding: 5px calc(var(--space) * 2);\n  font-size: var(--fs-meta);",
         "  padding: var(--space) calc(var(--space) * 3);\n  font-size: var(--fs-meta);"),
        (CSS_FILE, ":root { --banner-h: 40px; }", ":root { --banner-h: 80px; }"),
        (JS_FILE, 'markdownToHtml(zeilen.length ? zeilen[0] : "")',
         "markdownToHtml(markdownList(latest.lines))"),
    ],
    "version": [(CSS_FILE,
                 ".rail__version {\n  margin-left: .45em;\n  font-size: 11px;\n  font-weight: 400;\n"
                 "  letter-spacing: .03em;",
                 ".rail__version {\n  margin-left: .5em;\n  font-size: 9px;\n  font-weight: 400;\n"
                 "  letter-spacing: 0;")],
}

BROWSER_SKILL = '''import json, sys, time, hmac, hashlib, struct, base64

base, space, password, secret, shot_dir = sys.argv[1:6]

def totp_now(secret_b32):
    key = base64.b32decode(secret_b32 + "=" * (-len(secret_b32) % 8))
    counter = int(time.time() // 30)
    digest = hmac.new(key, struct.pack(">q", counter), hashlib.sha1).digest()
    offset = digest[-1] & 0x0F
    code = (struct.unpack(">I", digest[offset:offset + 4])[0] & 0x7FFFFFFF) % 1000000
    return f"{code:06d}"

# -- Die Hilfsfunktionen im Browser -------------------------------------------------------
MESS = """
() => {
  const OUT = {};
  // 1) Wortmarke: der Abstand zwischen dem Zeichen und dem Wortrest.
  const img = document.querySelector('.rail__brand .brand__mark');
  const brand = document.querySelector('.rail__brand');
  if (img && brand) {
    const walker = document.createTreeWalker(brand, NodeFilter.SHOW_TEXT);
    let node = null, treffer = null;
    while ((node = walker.nextNode())) { if (node.textContent.indexOf('harefyx') >= 0) { treffer = node; break; } }
    if (treffer) {
      const range = document.createRange();
      range.setStart(treffer, 0); range.setEnd(treffer, 1);
      const ir = img.getBoundingClientRect(), tr = range.getBoundingClientRect();
      OUT.marke = { abstand: tr.left - ir.right, img_breite: ir.width,
                    margin: getComputedStyle(img).marginRight,
                    text: treffer.textContent.trim() };
    }
  }
  // 4) Versionsanzeige: die Groesse des Punktes in der gerechneten Schrift.
  const v = document.querySelector('.rail__version');
  if (v) {
    const cs = getComputedStyle(v);
    const canvas = document.createElement('canvas');
    canvas.width = 120; canvas.height = 60;
    const ctx = canvas.getContext('2d');
    ctx.font = cs.fontWeight + ' ' + cs.fontSize + ' ' + cs.fontFamily;
    const gesetzt = ctx.font;   // haengt der Browser die Schrift an? sonst misst der Default
    ctx.textBaseline = 'alphabetic';
    ctx.fillStyle = '#fff';

    function tint(text, x, y) {
      ctx.clearRect(0, 0, canvas.width, canvas.height);
      ctx.fillText(text, x, y);
      const d = ctx.getImageData(0, 0, canvas.width, canvas.height).data;
      let minX = 1e9, maxX = -1, minY = 1e9, maxY = -1, summe = 0, spitze = 0;
      for (let yy = 0; yy < canvas.height; yy++) {
        for (let xx = 0; xx < canvas.width; xx++) {
          const a = d[(yy * canvas.width + xx) * 4 + 3];
          if (a > 30) {
            if (xx < minX) minX = xx; if (xx > maxX) maxX = xx;
            if (yy < minY) minY = yy; if (yy > maxY) maxY = yy;
            summe += a; if (a > spitze) spitze = a;
          }
        }
      }
      return { minX: minX, maxX: maxX, minY: minY, maxY: maxY, summe: summe, spitze: spitze };
    }
    function gruppen(text, x, y) {
      const r = tint(text, x, y);
      const d = ctx.getImageData(0, 0, canvas.width, canvas.height).data;
      const spalten = [];
      for (let xx = 0; xx < canvas.width; xx++) {
        let n = 0;
        for (let yy = 0; yy < canvas.height; yy++) if (d[(yy * canvas.width + xx) * 4 + 3] > 30) n++;
        spalten.push(n);
      }
      const g = []; let start = -1;
      for (let xx = 0; xx < spalten.length; xx++) {
        if (spalten[xx] > 0 && start < 0) start = xx;
        if (spalten[xx] === 0 && start >= 0) { g.push([start, xx - 1]); start = -1; }
      }
      if (start >= 0) g.push([start, spalten.length - 1]);
      return g;
    }
    const punkt = tint('.', 20, 40);
    const g31 = gruppen('3.', 20, 40);
    const g16 = gruppen('.1', 20, 40);
    // Die Tinte des Punktes bei mehreren Schriftgroessen -- die Groesse ist die
    // Entscheidung, nicht der Geschmack: 9 px (alt) gegen die Kandidaten.
    const stufen = {};
    for (const groesse of ['9px', '10px', '11px', '12px', '13px', '14px']) {
      ctx.font = '400 ' + groesse + ' ' + cs.fontFamily;
      const r = tint('.', 20, 40);
      stufen[groesse] = { breite: r.maxX >= r.minX ? r.maxX - r.minX + 1 : 0,
                          hoehe: r.maxY >= r.minY ? r.maxY - r.minY + 1 : 0,
                          tinte: r.summe, spitze: r.spitze };
    }
    ctx.font = cs.fontWeight + ' ' + cs.fontSize + ' ' + cs.fontFamily;
    OUT.version = {
      text: v.textContent, font_size: cs.fontSize, laufweite: cs.letterSpacing,
      schrift: gesetzt, dpr: window.devicePixelRatio,
      punkt_breite: punkt.maxX >= punkt.minX ? punkt.maxX - punkt.minX + 1 : 0,
      punkt_hoehe: punkt.maxY >= punkt.minY ? punkt.maxY - punkt.minY + 1 : 0,
      punkt_spitze: punkt.spitze, punkt_tinte: punkt.summe,
      punkt_stufen: stufen,
      gruppen_3_punkt: g31, gruppen_punkt_1: g16,
    };
  }
  // 3) das Update-Banner
  const b = document.getElementById('update-banner');
  if (b) {
    const body = document.getElementById('update-banner-body');
    const p = body ? body.querySelector('p') : null;
    OUT.banner = {
      sichtbar: !b.hidden,
      hoehe: b.offsetHeight,
      text: p ? p.textContent : '',
      zeilen: p ? p.getClientRects().length : 0,
      hat_log_knopf: !!document.getElementById('update-banner-log'),
      schiebt_layout: document.body.classList.contains('has-update-banner'),
    };
  }
  return OUT;
}
"""

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
    # Das Banner erscheint beim ersten Laden (frischer Nutzer => noch nie gesehen).
    try:
        page.wait_for_selector("#update-banner:not([hidden])", timeout=10000)
    except Exception:
        pass
    page.wait_for_timeout(700)
    out.update(page.evaluate(MESS))
    page.screenshot(path=shot_dir + "/b74_banner.png")
    # 2) die Auswahl braucht den Space-Modus (im globalen Modus ist sie ausgeblendet).
    page.wait_for_selector(".overview__space-open", timeout=15000)
    page.locator(".overview__space-open").first.click()
    page.wait_for_timeout(1200)
    out["zustand"] = page.evaluate("""() => ({
        kopf_versteckt: document.getElementById('list-head').hidden,
        uebersicht_versteckt: document.getElementById('list-overview').hidden,
        zeilen: document.querySelectorAll('.list__row').length,
        titel: document.title,
    })""")
    out["auswahl"] = page.evaluate("""() => {
        const sel = document.getElementById('list-assignee');
        const suche = document.getElementById('search-input');
        const knopf = document.getElementById('new-item-button');
        const liste = document.getElementById('list');
        if (!sel || !suche || !knopf || !liste) return null;
        const sr = sel.getBoundingClientRect(), ur = suche.getBoundingClientRect();
        const kr = knopf.getBoundingClientRect(), lr = liste.getBoundingClientRect();
        return { sichtbar: !sel.hidden, links: sr.left, rechts: sr.right, breite: sr.width,
                 suche_links: ur.left, suche_rechts: ur.right,
                 knopf_rechts: kr.right, liste_links: lr.left, liste_rechts: lr.right,
                 abstand_links: sr.left - ur.left, abstand_rechts: kr.right - sr.right,
                 abstand_liste: lr.right - sr.right,
                 margin: getComputedStyle(sel).margin };
    }""")
    page.screenshot(path=shot_dir + "/b74_liste.png")
    # Der Knopf "Alle Aenderungen" muss den Update-Log oeffnen -- seit der Banner nur noch
    # die Schlagzeile zeigt, ist das der einzige Weg zum ganzen Eintrag. Ohne diese Pruefung
    # waere "kompakter" ein Informationsverlust, den niemand bemerkt.
    # **Der Klick kommt zuletzt:** das Overlay der Einstellungen bleibt danach offen und
    # faengt jeden weiteren Klick ab (gemessen: der Klick auf die Space-Zeile wurde vom
    # Overlay abgefangen, der Lauf lief in einen Timeout).
    if out.get("banner", {}).get("hat_log_knopf"):
        page.click("#update-banner-log")
        page.wait_for_timeout(900)
        out["log"] = page.evaluate("""() => {
            const liste = document.getElementById('update-log-list');
            if (!liste) return { sichtbar: false, eintraege: 0 };
            return { sichtbar: liste.offsetParent !== null,
                     eintraege: liste.querySelectorAll('h3').length,
                     text: (liste.textContent || '').trim().slice(0, 100) };
        }""")
        page.screenshot(path=shot_dir + "/b74_log.png")
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

    password = "wegwerf-b74-" + secrets.token_urlsafe(8)
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
    # **Der TOTP-Zähler auf 0 zuruecksetzen** (Replay-Schutz, `routes_auth.py`:
    # `totp.verify(..., last_counter=store.get_totp_counter(space))`): ohne das schlaegt der
    # Login fehl, wenn zwei Laeufe desselben Wegwerf-Kontos im selben 30-Sekunden-Fenster
    # liegen -- der zweite Lauf nimmt denselben Code, der Server haelt ihn fuer eine
    # Wiedergabe. Gemessen: der Login antwortete 401, ohne dass etwas falsch war.
    store.set_totp_counter(SPACE, 0)
    return {"space": SPACE, "password": password, "secret": secret_b32}


def _seed_item() -> None:
    shutil.rmtree(DATA_ROOT, ignore_errors=True)
    DATA_ROOT.mkdir(parents=True, exist_ok=True)
    code = (
        "import sys; sys.path.insert(0, 'phase1_storage')\n"
        "from storage.store import Store\n"
        f"s = Store({str(DATA_ROOT)!r}, git=False)\n"
        f"for titel, status, wer in [('A doing', 'doing', {SPACE!r}), ('B offen', 'open', {SPACE!r})]:\n"
        "    i = s.create({0!r}, type='task', title=titel)\n"
        "    s.update(i.id, version=i.version, status=status, assignee=wer)\n".format(SPACE)
    )
    subprocess.run([".venv/bin/python", "-c", code], check=True, cwd=str(REPO_ROOT),
                   env={**os.environ, "PYTHONPATH": str(REPO_ROOT / "phase1_storage")})


def _serve() -> int:
    env = os.environ.copy()
    env["SPACE_DATA_ROOT"] = str(DATA_ROOT)
    env["SPACE_AUTH_DB"] = str(AUTH_DB)
    env["SPACE_PUBLIC_BASE_URL"] = "https://wegwerf-b74.invalid"
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
        [str(e2e), str(skript), BASE, user["space"], user["password"], user["secret"], str(WEGWERF_ROOT)],
        cwd=str(REPO_ROOT), capture_output=True, text=True,
    )
    if proc.returncode != 0:
        return {"fehler": proc.stderr[-1500:], "schritte": []}
    return json.loads(proc.stdout.strip().splitlines()[-1])


def _abstand_punkt_zu_nachbar(gruppen: list[list[int]]) -> float:
    """Die Lücke (in Pixeln) zwischen zwei Tinte-Gruppen — leer, wenn es keine zwei sind."""
    if len(gruppen) < 2:
        return -1.0
    return float(gruppen[1][0] - gruppen[0][1] - 1)


def main(argv: list[str] | None = None) -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--gegenlauf", nargs="?", const="alle",
                        choices=["mark", "auswahl", "banner", "version", "alle"],
                        help="die alte Fassung wiederherstellen — die Probe muss dann rot werden")
    args = parser.parse_args(argv)

    patches: list[tuple[Path, str, str]] = []
    if args.gegenlauf:
        keys = list(GEGENLAEUFE) if args.gegenlauf == "alle" else [args.gegenlauf]
        for key in keys:
            patches.extend(GEGENLAEUFE[key])

    # **Der Originalstand je Datei** — nicht die Zwischensaetze. Die erste Fassung legte
    # jede Zwischenfassung in einer Liste ab und stellte sie der Reihe nach wieder her:
    # am Ende stand die *vorletzte* Fassung in der Datei, der Gegenlauf blieb also halb
    # stehen und der naechste Lauf mass den halben Defekt. Jetzt: eine Datei, ein Original.
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

    # **Kein alter Befund darf als neuer durchgehen:** das Ergebnis wird vor dem Lauf
    # geloescht. Ein abgebrochener Lauf hinterlaesst damit kein JSON, das wie ein
    # frisches Ergebnis aussieht.
    RESULT.unlink(missing_ok=True)

    user = _setup()
    _seed_item()
    pid = _serve()
    try:
        b = _browser(user)
        marke = b.get("marke") or {}
        version = b.get("version") or {}
        banner = b.get("banner") or {}
        auswahl = b.get("auswahl") or {}
        punkt_abstand = min(
            _abstand_punkt_zu_nachbar(version.get("gruppen_3_punkt", [])),
            _abstand_punkt_zu_nachbar(version.get("gruppen_punkt_1", [])),
        )
        befund = {
            "marke_abstand_klein": 0 < marke.get("abstand", 99) <= MAX_MARK_GAP_PX,
            "auswahl_traegt_die_kanten": (
                auswahl.get("sichtbar") is True
                and abs(auswahl.get("abstand_links", 99)) <= 1.0
                and abs(auswahl.get("abstand_rechts", 99)) <= 1.5
            ),
            "banner_einzeilig": (
                banner.get("sichtbar") is True
                and banner.get("hoehe", 999) <= MAX_BANNER_H_PX
                and banner.get("zeilen") == 1
                and banner.get("hat_log_knopf") is True
            ),
            "log_erreichbar": (
                bool(b.get("log", {}).get("sichtbar"))
                and b.get("log", {}).get("eintraege", 0) >= 1
            ),
            "version_punkt_erkennbar": (
                version.get("punkt_spitze", 0) >= MIN_DOT_PEAK
                and version.get("punkt_breite", 0) * version.get("punkt_hoehe", 0) >= MIN_DOT_AREA
                and punkt_abstand >= MIN_DOT_GAP_PX
            ),
        }
        ok = all(befund.values()) and not b.get("seitenfehler") and "fehler" not in b
        ergebnis = {
            "probe": "p105_b7_sichtung",
            "instanz": {"basis": BASE, "pid": pid, "wegwerf": True},
            "grenzwerte": {
                "marke_max_px": MAX_MARK_GAP_PX, "banner_max_px": MAX_BANNER_H_PX,
                "punkt_spitze_min": MIN_DOT_PEAK, "punkt_flaeche_min": MIN_DOT_AREA,
                "punkt_abstand_min_px": MIN_DOT_GAP_PX,
            },
            "befund": befund,
            "messung": {
                "marke": marke, "auswahl": auswahl, "banner": banner, "version": version,
                "zustand": b.get("zustand"), "log": b.get("log"),
                "punkt_abstand": punkt_abstand,
            },
            "seitenfehler": b.get("seitenfehler", []),
            "browser_fehler": b.get("fehler"),
            "alle_kriterien_erfuellt": ok,
        }
        if args.gegenlauf:
            ergebnis["gegenlauf"] = args.gegenlauf
            ergebnis["gegenlauf_erwartet_rot"] = not ok
        RESULT.write_text(json.dumps(ergebnis, indent=2, ensure_ascii=False) + "\n", encoding="utf-8")
        print(json.dumps(ergebnis, indent=2, ensure_ascii=False))
        return (0 if not ok else 1) if args.gegenlauf else (0 if ok else 1)
    finally:
        _stop()
        for datei, inhalt in original.items():
            datei.write_text(inhalt, encoding="utf-8")


if __name__ == "__main__":
    raise SystemExit(main())
