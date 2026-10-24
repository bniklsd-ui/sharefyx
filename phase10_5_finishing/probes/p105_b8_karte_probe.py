#!/usr/bin/env python3
"""P10.5 Block 8, Schritt 8.8 — die Gehirnkarte C2 im **echten Browser**.

Wegwerf-Instanz mit **200 Knoten** (Port 18772, tmp-`DATA_ROOT`, PID-Datei, Hard Rule 9 — nicht
gegen den laufenden Dienst). Gemessen wird nicht in der Quelle, sondern im gerenderten Bild:
was der Plan verlangt (Lappen, Furchen, Zellen, Aktivierung), ist eine Eigenschaft des
**Pixels**, nicht des Codes.

| Messung | Plan | was im Browser gemessen wird |
|---|---|---|
| `lappen` | 8.1 | die Pixel der Lappenflaeche (5% Space-Farbe ueber `--surface`) — **0**, wenn die Lappen nicht gezeichnet werden |
| `layout` | 8.5 (KA-2) | ein gezogener Knoten steht **nach dem Neuladen** noch an seiner Stelle (Pixel im Zielquadrat) |
| `filter` | 8.6 (KA-3) | die Suche dimmt die Nicht-Treffer (Pixel hell → gedimmt) und zaehlt sie; der Typfilter blendet Knoten **und** Bahnen aus |
| `reducedmotion` | 8.7 | **0** `requestAnimationFrame`-Aufrufe aus `graph.js` (das Bild ist trotzdem gemalt) |

**Gegenlauf `--gegenlauf lappen|layout|filter`:** die Regel in `graph.js` wird gepatcht (die Datei
wird danach **wiederhergestellt**) — die Messung muss dann **rot** werden. Ohne diesen Lauf
beweist die gruene Probe nichts.

Aufruf:  `~/.claude-code-tools/e2e-venv/bin/python phase10_5_finishing/probes/p105_b8_karte_probe.py
         [--gegenlauf NAME]`
Ergebnis: `phase10_5_finishing/probes/p105_b8_karte_probe.json`
Bilder:   `docs/screenshots/p105_b8_*.png`
"""
from __future__ import annotations

import argparse
import asyncio
import json
import subprocess
import sys
import urllib.request
from pathlib import Path

from playwright.async_api import async_playwright

REPO_ROOT = Path(__file__).resolve().parents[2]
WEGWERF_ROOT = Path("/tmp/opencode/sharefyx-wegwerf-200knoten")
AUTH_DB = WEGWERF_ROOT / "auth.sqlite3"
CREDS_FILE = WEGWERF_ROOT / "credentials.json"
SETUP = REPO_ROOT / "phase8_ui_graph" / "scripts" / "wegwerf_setup_200knoten.py"
GRAPH_JS = REPO_ROOT / "phase5_ui" / "webui" / "static" / "js" / "graph.js"
SHOT_DIR = REPO_ROOT / "docs" / "screenshots"
RESULT = Path(__file__).resolve().with_name("p105_b8_karte_probe.json")
PORT = 18772
BASE = f"http://127.0.0.1:{PORT}"

# -- Die Farben, nach denen gemessen wird (aus `app.css` + `graph.js`) -------------------------
SURFACE = (20, 24, 29)                 # `--surface` (#14181D) -- die Flaeche unter dem Canvas
SPACE_COLORS = [(74, 147, 240),        # own    (#4A93F0)
                (46, 184, 166),        # shared (#2EB8A6)
                (139, 147, 161)]       # foreign(#8B93A1)

# -- Die Gegenläufe: je einer ein eingebauter Fehler ------------------------------------------
# **Die Anker sind eindeutig** (Regel + Nachbarzeile): sonst patcht der Gegenlauf den
# Kommentar über der Regel statt der Regel.
GEGENLAEUFE = {
    "lappen": [
        ("  drawLobes(shown);", "  /* drawLobes(shown); */"),
    ],
    "layout": [
        ("      n.pinned = true;", "      n.pinned = false;"),
    ],
    "filter": [
        ("    if (filterType && n.type !== filterType) continue;",
         "    if (false && filterType && n.type !== filterType) continue;"),
        ("    if (filterStatus && n.status !== filterStatus) continue;",
         "    if (false && filterStatus && n.status !== filterStatus) continue;"),
    ],
}

# -- Die Messungen im Browser -------------------------------------------------------------------

# Zaehlt die Pixel nach ihrer Herkunft: der **Kern** eines Knotens (die Space-Farbe in voller
# Deckung), ein **gedimmter** Knoten (die Space-Farbe mit 45% Deckung ueber der Flaeche) und
# die **Lappenflaeche** (5% Deckung -- der Wert der Vorlage C2).
MESS = """
() => {
  const c = document.getElementById('overview-graph-canvas');
  if (!c) return null;
  const d = c.getContext('2d').getImageData(0, 0, c.width, c.height).data;
  const SPACE = [[74,147,240],[46,184,166],[139,147,161]];
  const near = (a, b, tol) => Math.abs(a[0]-b[0]) <= tol && Math.abs(a[1]-b[1]) <= tol
                                 && Math.abs(a[2]-b[2]) <= tol;
  // **Die Deckung steht im Alphakanal.** Der Canvas ist transparent; die Mischung mit der
  // Flaeche (`--surface`) entsteht erst beim Anzeigen. Die drei Sorten:
  //   Deckung 1,00 -> der Kern eines Knotens (und sein Membranring)
  //   Deckung 0,45 -> ein **gedimmter** Knoten (Suche: Nicht-Treffer)
  //   Deckung 0,05 -> die **Lappenflaeche** (die Vorlage C2 malt sie mit 5%)
  const px = (i) => [d[i], d[i + 1], d[i + 2]];
  const xy = (i) => [(i / 4) % c.width, Math.floor((i / 4) / c.width)];
  // Die Antialiasing-Halos der Knoten haben ebenfalls eine Deckung zwischen 0 und 1 --
  // sie sind **keine** Lappen. Der Halo reicht aber nur 1-2 px ueber die gefuellte Flaeche
  // hinaus, also genuegt ein Ausschluss von **3 px** um die Kerne. Mit 13 px (dem ersten
  // Versuch) fiel die Lappenflaeche selbst mit weg: bei 200 Knoten liegt fast der ganze
  // Canvas innerhalb von 13 px eines Kerns.
  //
  // **Die Deckung der Lappenflaeche ist genau 13/255** (0,05 * 255 = 12,75 -> 13): die
  // Vorlage C2 malt sie mit 5%. Diese eine Deckung zu messen, statt eines Fensters,
  // trennt sie von den Bahnen, deren Antialiasing alle Deckungen von 0 bis 1 annimmt.
  const CELL = 16;
  const grid = new Map();
  for (let i = 0; i < d.length; i += 4) {
    if (d[i + 3] < 100) continue;
    const p = px(i);
    let ist = false;
    for (const sp of SPACE) { if (near(p, sp, 6)) { ist = true; break; } }
    if (!ist) continue;
    const [x, y] = xy(i);
    const k = Math.floor(x / CELL) + ',' + Math.floor(y / CELL);
    if (!grid.has(k)) grid.set(k, []);
    grid.get(k).push([x, y]);
  }
  const nahKern = (x, y) => {
    const cx = Math.floor(x / CELL), cy = Math.floor(y / CELL);
    for (let dy = -1; dy <= 1; dy++) {
      for (let dx = -1; dx <= 1; dx++) {
        const arr = grid.get((cx + dx) + ',' + (cy + dy));
        if (!arr) continue;
        for (const [ox, oy] of arr) {
          if (Math.abs(ox - x) < 3 && Math.abs(oy - y) < 3) return true;
        }
      }
    }
    return false;
  };
  let kern = 0, gedimmt = 0, lappen = 0;
  for (let i = 0; i < d.length; i += 4) {
    const a = d[i + 3];
    if (a < 4) continue;
    const p = px(i);
    if (a >= 250) {
      for (const sp of SPACE) { if (near(p, sp, 6)) { kern += 1; break; } }
      continue;
    }
    if (a >= 100 && a <= 135) {
      // **Ohne** den Halo-Ausschluss: die gedimmten *Kerne* liegen selbst in der Naehe der
      // Kerni (das Gitter enthaelt sie, weil sie dieselbe Deckungsklasse haben) -- mit dem
      // Ausschluss waere die Zahl null, obwohl die Suche gedimmt hat. Der Halo der
      // gedimmten Knoten zaehlt mit; die Messung vergleicht ohnehin die Zahlen unter
      //einander (mit/ohne Suche), nicht gegen eineAbsolute Groesse.
      for (const sp of SPACE) { if (near(p, sp, 6)) { gedimmt += 1; break; } }
      continue;
    }
    if (a >= 12 && a <= 14) {
      // Die Toleranz ist hier **enger** als bei den Kernen: die Bahnen (#7E8A98) liegen nur
      // 13 Kanalaele von der fremden Space-Farbe (#8B93A1) entfernt, und ihre
      // Antialiasing-Pixel haben ebenfalls eine Deckung zwischen 0 und 1 -- mit der weiten
      // Toleranz zaehlte die **Kante** mit statt der Lappe (gemessen: 706 Pixel, als die
      // Lappen ausgeschaltet waren). Bei der Lappenflaeche (Deckung 0,05) ist der
      // Rundungsfehler der praemultiplizierten Canvas dagegen hoechstens +-10.
      let ist = false;
      for (const sp of SPACE) { if (near(p, sp, 11)) { ist = true; break; } }
      if (!ist) continue;
      const [x, y] = xy(i);
      if (nahKern(x, y)) continue;
      lappen += 1;
    }
  }
  return { kern: kern, gedimmt: gedimmt, lappen: lappen, w: c.width, h: c.height };
}
"""

# Die Kernpixel in einem Quadrat um einen Punkt (Canvas-Geraetepixel) -- damit wird geprueft,
# ob an einer **bestimmten** Stelle ein Knoten steht (fuer KA-2: der gezogene Knoten).
REGION = """
([cx, cy, r]) => {
  const c = document.getElementById('overview-graph-canvas');
  const d = c.getContext('2d').getImageData(0, 0, c.width, c.height).data;
  const SPACE = [[74,147,240],[46,184,166],[139,147,161]];
  const near = (a, b) => Math.abs(a[0]-b[0]) <= 6 && Math.abs(a[1]-b[1]) <= 6
                           && Math.abs(a[2]-b[2]) <= 6;
  let n = 0;
  for (let y = Math.max(0, cy - r); y <= Math.min(c.height - 1, cy + r); y++) {
    for (let x = Math.max(0, cx - r); x <= Math.min(c.width - 1, cx + r); x++) {
      const i = (y * c.width + x) * 4;
      if (d[i + 3] < 250) continue;
      const px = [d[i], d[i + 1], d[i + 2]];
      for (const sp of SPACE) { if (near(px, sp)) { n += 1; break; } }
    }
  }
  return n;
}
"""

# Die Knotenmittelpunkte aus den Canvas-Pixeln (Muster aus `p8_22_smoke.py :: NODE_CENTERS`):
# die Knotenkerne tragen die drei Space-Farben in voller Deckung, die Kanten nicht.
NODE_CENTERS = """
() => {
  const c = document.getElementById('overview-graph-canvas');
  const rect = c.getBoundingClientRect();
  const sx = rect.width / c.width, sy = rect.height / c.height;
  const d = c.getContext('2d').getImageData(0, 0, c.width, c.height).data;
  const want = [[74,147,240],[46,184,166],[139,147,161]];
  const hit = [];
  for (let y = 0; y < c.height; y += 2) {
    for (let x = 0; x < c.width; x += 2) {
      const i = (y * c.width + x) * 4;
      if (d[i + 3] < 250) continue;
      for (const w of want) {
        if (d[i] === w[0] && d[i + 1] === w[1] && d[i + 2] === w[2]) { hit.push([x, y]); break; }
      }
    }
  }
  const clusters = [];
  for (const [x, y] of hit) {
    let found = null;
    for (const cl of clusters) {
      if (Math.abs(cl.x / cl.n - x) < 14 && Math.abs(cl.y / cl.n - y) < 14) { found = cl; break; }
    }
    if (found) { found.x += x; found.y += y; found.n += 1; }
    else clusters.push({ x: x, y: y, n: 1 });
  }
  return clusters.filter(cl => cl.n >= 3)
    .map(cl => ({ x: (cl.x / cl.n) * sx, y: (cl.y / cl.n) * sy, px: cl.n }));
}
"""

# Der Ruhe-Zustand: der Canvas-Hash aendert sich zweimal hintereinander nicht mehr.
CANVAS_HASH = """
() => {
  const c = document.getElementById('overview-graph-canvas');
  if (!c) return null;
  const d = c.getContext('2d').getImageData(0, 0, c.width, c.height).data;
  let h = 0x811c9dc5, painted = 0;
  for (let i = 0; i < d.length; i += 64) {
    h ^= d[i] + d[i + 1] + d[i + 2] + d[i + 3];
    h = (h * 16777619) >>> 0;
    if (d[i + 3] !== 0) painted += 1;
  }
  return { hash: h, painted: painted, now: performance.now() };
}
"""

# Zaehlt die Animationsframes, die **aus graph.js** kommen (der Stack entscheidet -- Playwrights
# eigenes Polling zaehlt nicht mit; derselbe Filter wie in `p8_22_smoke.py`).
RAF_PROBE = """
(() => {
  const log = { count: 0, other: 0, stamps: [] };
  window.__rafLog = log;
  const orig = window.requestAnimationFrame.bind(window);
  window.requestAnimationFrame = function (cb) {
    const fromGraph = String(new Error().stack || '').includes('graph.js');
    return orig(function (t) {
      if (fromGraph) { log.count += 1; log.stamps.push(performance.now()); }
      else { log.other += 1; }
      return cb(t);
    });
  };
})();
"""


def _totp(otpauth_uri: str) -> str:
    """Der TOTP-Code aus der `otpauth_uri` des Wegwerf-Kontos (Muster aus der M6-Probe)."""
    import base64
    import hashlib
    import hmac
    import struct
    import time
    import urllib.parse
    qs = dict(urllib.parse.parse_qsl(urllib.parse.urlparse(otpauth_uri).query))
    key = base64.b32decode(qs["secret"] + "=" * (-len(qs["secret"]) % 8))
    counter = int(time.time() // 30)
    digest = hmac.new(key, struct.pack(">q", counter), hashlib.sha1).digest()
    off = digest[-1] & 0x0F
    return f"{(struct.unpack('>I', digest[off:off + 4])[0] & 0x7FFFFFFF) % 1000000:06d}"


def _totp_zaehler_zuruecksetzen(space: str) -> None:
    """Den TOTP-Zaehler des Wegwerf-Kontos auf 0 zuruecksetzen.

    `routes_auth.py` prueft `totp.verify(..., last_counter=store.get_totp_counter(space))` —
    jeder Login **verbraucht** einen Zaehlschritt. Der P8-22-Smoke hat den Zaehler dieser
    Wegwerf-Instanz schon verbraucht; ein zweiter Login im selben 30-Sekunden-Fenster
    schlaegt deshalb mit 401 fehl, obwohl nichts falsch ist. (Dasselbe Muster wie in
    `p105_b7_sichtung_probe.py :: _provision_user`.)
    """
    code = (
        "from datetime import datetime, timezone\n"
        "from authserver.store import AuthStore\n"
        f"store = AuthStore({str(AUTH_DB)!r}, now_fn=lambda: datetime.now(timezone.utc))\n"
        f"store.set_totp_counter({space!r}, 0)\n"
    )
    subprocess.run([str(REPO_ROOT / ".venv" / "bin" / "python"), "-c", code], check=True)


async def _login(page, creds: dict) -> None:
    _totp_zaehler_zuruecksetzen(creds["space"])
    await page.goto(f"{BASE}/ui/login", wait_until="domcontentloaded")
    await page.fill('input[name="space"]', creds["space"])
    await page.fill('input[name="password"]', creds["password"])
    await page.fill('input[name="totp"]', _totp(creds["otpauth_uri"]))
    await page.click('form[action="/ui/login"] button[type="submit"]')
    await page.wait_for_load_state("networkidle")
    await page.wait_for_selector(".overview__graph canvas", state="visible", timeout=15000)


async def _warte_bereit(page) -> None:
    """Nach dem Neuladen: die Session (Cookie) lebt weiter — nur auf die Karte warten."""
    await page.wait_for_selector(".overview__graph canvas", state="visible", timeout=15000)


async def _settle(page, budget_ms: int = 12000) -> None:
    """Warten, bis der Canvas zweimal hintereinander gleich ist (die Karte zur Ruhe)."""
    elapsed = 0
    last = None
    stable = None
    while elapsed <= budget_ms:
        snap = await page.evaluate(CANVAS_HASH)
        if snap is None:
            raise RuntimeError("Canvas fehlt im DOM")
        if snap["painted"] > 0 and snap["hash"] == last:
            if stable is None:
                stable = snap["now"]
            elif snap["now"] - stable >= 100:
                return
        else:
            stable = None
        last = snap["hash"]
        await page.wait_for_timeout(100)
        elapsed += 100
    raise RuntimeError("Canvas kam nicht zur Ruhe")


def _instance_gesund() -> bool:
    try:
        urllib.request.urlopen(f"{BASE}/health", timeout=2).read()
        return True
    except Exception:
        return False


def _instanz_starten() -> None:
    """Die 200-Knoten-Wegwerf-Instanz aufsetzen (das Skript aus Phase 8, unveraendert)."""
    if not CREDS_FILE.exists():
        subprocess.run([sys.executable, str(SETUP), "setup"], cwd=str(REPO_ROOT), check=True)
        subprocess.run([sys.executable, str(SETUP), "seed-items"], cwd=str(REPO_ROOT), check=True)
    subprocess.run([sys.executable, str(SETUP), "start"], cwd=str(REPO_ROOT), check=True)


def _patchen(patches: list[tuple[str, str]]) -> str:
    """Die Datei patchen und den **alten** Inhalt zurueckgeben (der Aufrufer stellt wieder her)."""
    original = GRAPH_JS.read_text(encoding="utf-8")
    source = original
    for old, new in patches:
        if old not in source:
            raise SystemExit(f"Gegenlauf-Anker nicht gefunden: {old!r}")
        source = source.replace(old, new)
    GRAPH_JS.write_text(source, encoding="utf-8")
    return original


async def main(argv: list[str] | None = None) -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--gegenlauf", choices=sorted(GEGENLAEUFE), default=None)
    args = parser.parse_args(argv)

    if not _instance_gesund():
        _instanz_starten()
    creds = json.loads(CREDS_FILE.read_text())

    original = None
    if args.gegenlauf:
        original = _patchen(GEGENLAEUFE[args.gegenlauf])

    ergebnis: dict = {"gegenlauf": args.gegenlauf, "messungen": {}}
    try:
        async with async_playwright() as p:
            browser = await p.chromium.launch()
            ctx = await browser.new_context(viewport={"width": 1280, "height": 900})
            page = await ctx.new_page()
            await page.add_init_script(RAF_PROBE)
            fehler: list[str] = []
            page.on("pageerror", lambda e: fehler.append(str(e)))
            await _login(page, creds)
            await _settle(page)

            # -- 1) Die Lappen (8.1) --------------------------------------------------------
            grund = await page.evaluate(MESS)
            ergebnis["messungen"]["lappen"] = {
                "lappen_pixel": grund["lappen"],
                "kern_pixel": grund["kern"],
                # Die **Flaeche** der Lappen haengt sehr von der spatialen Anordnung ab
                # (gemessen: 3142 bis 137492 Pixel bei derselben Topologie, je nachdem, in
                # welcher Reihenfolge die Knoten im Index stehen -- die Simulation ist
                # empfindlich). Geprueft wird deshalb: **es gibt Lappen**, nicht: wie viele.
                # Der Gegenlauf (die Lappen abgeschaltet) liefert 0.
                "ok": grund["lappen"] > 100,
            }

            # -- 2) Der Fokus (8.4): Screenshot mit den Ringen -------------------------------
            zentren = await page.evaluate(NODE_CENTERS)
            zentrum = zentren[len(zentren) // 2] if zentren else {"x": 100, "y": 100}
            box = await page.evaluate(
                """() => { const r = document.getElementById('overview-graph-canvas')
                                   .getBoundingClientRect();
                     return { left: r.left, top: r.top, width: r.width, height: r.height }; }"""
            )
            await page.mouse.move(box["left"] + zentrum["x"], box["top"] + zentrum["y"])
            await page.wait_for_timeout(300)
            await page.locator("#overview-graph-canvas").screenshot(
                path=str(SHOT_DIR / "p105_b8_02_fokus.png"))
            await page.screenshot(path=str(SHOT_DIR / "p105_b8_01_ruhe.png"))

            # -- 3) Die Suche (8.6, KA-3) --------------------------------------------------
            await page.mouse.move(box["left"] + 2, box["top"] + 2)
            await page.wait_for_timeout(200)
            await page.fill("#overview-graph-search", "Knoten 01")
            await page.wait_for_timeout(400)
            mit_suche = await page.evaluate(MESS)
            treffer_text = (await page.locator("#overview-graph-hits").inner_text()).strip()
            await page.locator("#overview-graph-canvas").screenshot(
                path=str(SHOT_DIR / "p105_b8_03_suche.png"))
            await page.fill("#overview-graph-search", "")
            await page.wait_for_timeout(400)
            ohne_suche = await page.evaluate(MESS)

            # -- 4) Der Typfilter (8.6, KA-3) ----------------------------------------------
            typen = await page.evaluate(
                """() => Array.from(document.getElementById('overview-graph-filter-type').options)
                                 .map(o => o.value).filter(v => v)"""
            )
            filtertyp = "task" if "task" in typen else (typen[0] if typen else None)
            if filtertyp:
                await page.select_option("#overview-graph-filter-type", filtertyp)
                await page.wait_for_timeout(400)
            mit_filter = await page.evaluate(MESS)
            await page.locator("#overview-graph-canvas").screenshot(
                path=str(SHOT_DIR / "p105_b8_04_filter.png"))
            if filtertyp:
                await page.select_option("#overview-graph-filter-type", "")
                await page.wait_for_timeout(300)

            ergebnis["messungen"]["filter"] = {
                "treffer_text": treffer_text,
                "kern_ohne_suche": ohne_suche["kern"],
                "kern_mit_suche": mit_suche["kern"],
                "gedimmt_mit_suche": mit_suche["gedimmt"],
                "filter_typ": filtertyp,
                "kern_mit_filter": mit_filter["kern"],
                "ok": ("Treffer" in treffer_text
                       and mit_suche["gedimmt"] > 0
                       and mit_filter["kern"] < ohne_suche["kern"]),
            }

            # -- 5) KA-2: das Layout ueberlebt das Neuladen (8.5) -------------------------
            # **Das Kriterium ist das Kartenbild, nicht ein einzelner Pixel.** Ein einzelner
            # Pixel taugt nicht: bei 200 Knoten liegt an fast jeder Stelle ein Knoten, und
            # ein Geraeusch in der Simulation verschiebt ihn. Gemessen wird deshalb:
            #   1) die **gemerkte Ablage** aendert sich durch den Zug (sonst wurde gar kein
            #      Knoten gezogen, sondern die Ansicht verschoben -- das aendert die Ablage
            #      *nicht*),
            #   2) das **Kartenbild nach dem Neuladen** ist dasselbe wie vor dem Neuladen.
            # Der Gegenlauf (der gemerkte Knoten wird nicht festgehalten) verschiebt ihn
            # zurueck -- das Bild unterscheidet sich.
            LAYOUT_LESE = """
() => {
  const k = Object.keys(localStorage).find(k => k.startsWith('sfx:graph:layout'));
  if (!k) return null;
  const v = JSON.parse(localStorage.getItem(k));
  return { key: k, v: v.v, n: Object.keys(v.pos || {}).length,
           pos: JSON.stringify(v.pos) };
}
"""
            vorher_lage = await page.evaluate(LAYOUT_LESE)
            layout_info = await page.evaluate(
                """
() => {
  const c = document.getElementById('overview-graph-canvas');
  const rect = c.getBoundingClientRect();
  const d = c.getContext('2d').getImageData(0, 0, c.width, c.height).data;
  const SPACE = [[74,147,240],[46,184,166],[139,147,161]];
  const near = (a, b) => Math.abs(a[0]-b[0]) <= 6 && Math.abs(a[1]-b[1]) <= 6
                           && Math.abs(a[2]-b[2]) <= 6;
  const cores = [];
  for (let y = 0; y < c.height; y++) {
    for (let x = 0; x < c.width; x++) {
      const i = (y * c.width + x) * 4;
      if (d[i + 3] < 250) continue;
      const px = [d[i], d[i + 1], d[i + 2]];
      for (const sp of SPACE) { if (near(px, sp)) { cores.push([x, y]); break; } }
    }
  }
  // Der Griffpunkt muss der **Mittelpunkt eines Knotens** sein -- nicht irgendein Kernpixel.
  // Der Kern eines Knotens besteht aus der gefuellten Scheibe (Deckung 1) **und** dem
  // Membranring (2 px, Deckung 1); zwischen zwei dicht beieinander liegenden Knoten liegt
  // deshalb ein Kernpixel, der zu *keinem* Mittelpunkt gehoert. Getroffen wird mit
  // `hitTest()`, das den Knoten im Radius 14 px sucht: bei 200 dicht gepackten Knoten
  // liegt ein solches Zwischenpixel **ausserhalb** dieses Radius (gemessen: 15 px) -- der
  // Griff ging ins Leere und die Ansicht wurde **verschoben** statt gezogen.
  // Der **dichteste** Kernpixel ist der Mittelpunkt (die Scheibe fuellt sich um die Mitte).
  const CELL = 4;
  const grid = new Map();
  for (const [x, y] of cores) {
    const k = Math.floor(x / CELL) + ',' + Math.floor(y / CELL);
    if (!grid.has(k)) grid.set(k, []);
    grid.get(k).push([x, y]);
  }
  let quelle = null, bestDist = -1;
  for (const [x, y] of cores) {
    let dicht = 0;
    const cx = Math.floor(x / CELL), cy = Math.floor(y / CELL);
    for (let dy = -1; dy <= 1; dy++) {
      for (let dx = -1; dx <= 1; dx++) {
        const arr = grid.get((cx + dx) + ',' + (cy + dy));
        if (!arr) continue;
        for (const [ox, oy] of arr) {
          if (Math.abs(ox - x) <= 2 && Math.abs(oy - y) <= 2) dicht += 1;
        }
      }
    }
    if (dicht > bestDist) { bestDist = dicht; quelle = [x, y]; }
  }
  let ziel = null;
  for (let y = 24; y < c.height - 24 && !ziel; y += 4) {
    for (let x = 24; x < c.width - 24; x += 4) {
      let frei = true;
      for (const [ox, oy] of cores) {
        if (Math.abs(ox - x) < 16 && Math.abs(oy - y) < 16) { frei = false; break; }
      }
      if (frei) { ziel = [x, y]; break; }
    }
  }
  const sx = rect.width / c.width, sy = rect.height / c.height;
  return {
    kerne: cores.length, abstand: bestDist,
    quelle_px: quelle, quelle_css: quelle ? [quelle[0] * sx, quelle[1] * sy] : null,
    ziel_px: ziel, ziel_css: ziel ? [ziel[0] * sx, ziel[1] * sy] : null,
  };
}
"""
            )
            layout = {"quelle_px": layout_info["quelle_px"], "ziel_px": layout_info["ziel_px"],
                      "kerne": layout_info["kerne"], "abstand": layout_info["abstand"]}
            if layout_info["quelle_px"] and layout_info["ziel_px"]:
                await page.evaluate(
                    """
([q, z]) => {
  const c = document.getElementById('overview-graph-canvas');
  const r = c.getBoundingClientRect();
  const ev = (type, x, y, extra) => Object.assign(
    { bubbles: true, clientX: r.left + x, clientY: r.top + y }, extra || {});
  c.dispatchEvent(new MouseEvent('mousemove', ev('mousemove', q[0], q[1])));
  c.dispatchEvent(new MouseEvent('mousedown', ev('mousedown', q[0], q[1], { button: 0 })));
  for (let i = 1; i <= 20; i++) {
    const x = q[0] + (z[0] - q[0]) * i / 20;
    const y = q[1] + (z[1] - q[1]) * i / 20;
    c.dispatchEvent(new MouseEvent('mousemove', ev('mousemove', x, y)));
  }
  c.dispatchEvent(new MouseEvent('mouseup', ev('mouseup', z[0], z[1], { button: 0 })));
}
""",
                    [layout_info["quelle_css"], layout_info["ziel_css"]],
                )
                await page.wait_for_timeout(1800)     # das Speichern ist gedrosselt (1 s)
                nachher_lage = await page.evaluate(LAYOUT_LESE)
                # Der Mauszeiger weg vom Canvas (sonst zeichnet die Karte den Fokus mit --
                # der ist nach dem Neuladen nicht da, und die Bilder waeren nicht vergleichbar).
                await page.mouse.move(box["left"] + 2, box["top"] + 2)
                await page.wait_for_timeout(200)
                # **Auf die Ruhe warten**, bevor der Vergleich gezogen wird: die Simulation
                # laeuft beim Zug noch, und die freien Knoten wandern weiter. Erst wenn das
                # Bild steht, sind die beiden Bilder vergleichbar.
                await _settle(page)
                bild_vorher = await page.evaluate(CANVAS_HASH)
                pixel_vorher = await page.evaluate(REGION, layout_info["ziel_px"] + [14])
                await page.reload(wait_until="domcontentloaded")
                await _warte_bereit(page)
                await _settle(page)
                bild_nachher = await page.evaluate(CANVAS_HASH)
                pixel_nachher = await page.evaluate(REGION, layout_info["ziel_px"] + [14])
                # **Das Kriterium ist die Position, nicht das ganze Bild.** Zwei Gruende,
                # beide gemessen: (1) die Ablage rundet auf ganze Pixel (`Math.round`), die
                # wiederhergestellte Position weicht also bis zu 0,71 px ab -- die Kernpixel
                # eines Knotens liegen dadurch anders auf dem Raster (26164 gegen 25924
                # Kernpixel, 1 %); (2) die **Lappen sind fragile Fragmente**: sie entstehen
                # aus einem 8-px-Raster ueber die *naechste* Nachbarschaft, und eine
                # Verschiebung um weniger als einen Pixel aendert die Zellenlage -- vor dem
                # Neuladen waren es drei Lappen, danach einer (gemessen: `data-lobes`).
                # Beides ist kein Fehler des Merkens, sondern eine Eigenschaft der
                # Darstellung. Gemessen wird deshalb: **der gezogene Knoten steht nach dem
                # Neuladen noch an seiner Stelle** (Kernpixel am Ziel) -- und die Ablage hat
                # sich durch den Zug ueberhaupt geaendert (sonst waere gar kein Knoten
                # gezogen worden, sondern die Ansicht verschoben).
                layout.update({
                    "ablage_geaendert": bool(vorher_lage and nachher_lage
                                            and vorher_lage["pos"] != nachher_lage["pos"]),
                    "eintraege": nachher_lage["n"] if nachher_lage else 0,
                    "pixel_vorher": pixel_vorher,
                    "pixel_nachher": pixel_nachher,
                    "bild_vorher": bild_vorher["hash"],
                    "bild_nachher": bild_nachher["hash"],
                    "bild_gleich": bild_vorher["hash"] == bild_nachher["hash"],
                    "ok": bool(vorher_lage and nachher_lage
                               and vorher_lage["pos"] != nachher_lage["pos"]
                               and pixel_vorher > 0 and pixel_nachher > 0),
                })
            else:
                layout.update({"ok": False, "grund": "kein isolierter Knoten oder keine leere Stelle"})
            ergebnis["messungen"]["layout"] = layout

            ergebnis["seitenfehler"] = fehler
            await ctx.close()

            # -- 6) Reduced motion (8.7): 0 Frames, aber ein gemaltes Bild -----------------
            ctx2 = await browser.new_context(viewport={"width": 1280, "height": 900},
                                             reduced_motion="reduce")
            page2 = await ctx2.new_page()
            await page2.add_init_script(RAF_PROBE)
            await _login(page2, creds)
            await page2.wait_for_timeout(1200)
            raf = await page2.evaluate("() => window.__rafLog")
            rm = await page2.evaluate(MESS)
            ergebnis["messungen"]["reducedmotion"] = {
                "raf_calls": raf["count"],
                "kern_pixel": rm["kern"],
                "ok": raf["count"] == 0 and rm["kern"] > 0,
            }
            await ctx2.close()
            await browser.close()
    finally:
        if original is not None:
            GRAPH_JS.write_text(original, encoding="utf-8")

    RESULT.write_text(json.dumps(ergebnis, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")
    rot = [k for k, v in ergebnis["messungen"].items() if not v.get("ok")]
    print(json.dumps(ergebnis, ensure_ascii=False, indent=2))
    if rot:
        print(f"ROT: {rot}", file=sys.stderr)
        return 1
    print("Alle Messungen gruen.")
    return 0


if __name__ == "__main__":
    raise SystemExit(asyncio.run(main()))
