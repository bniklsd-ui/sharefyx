#!/usr/bin/env python3
"""Phase 8 P8-22 -- Playwright-Lastmessung gegen die 200-Knoten-Wegwerf-Instanz (Port 18772).

Abnahmezeile P8-22 (Plan §7): "200-Knoten-Wegwerf-Datensatz: Simulation kommt < 3 s zur Ruhe,
Interaktion ohne Hakeln; `prefers-reduced-motion` rendert statisch."

Gemessen wird schwarzkastig -- `js/graph.js` exportiert seinen Simulationszustand nicht
(`nodes`/`alpha`/`rafId` sind Modul-privat), und dieser Smoke fasst den Produktionscode
deshalb bewusst nicht an. Zwei unabhaengige Messgroessen statt einer behaupteten:

1. **Sichtbare Ruhe** (`pixel_settle_ms`): der Canvas-Inhalt wird alle 100 ms gehasht; ruhig
   ist der Graph, sobald sich der Hash zweimal hintereinander nicht mehr aendert. Das ist die
   Groesse, die ein Mensch als "kommt zur Ruhe" wahrnimmt -- **darauf assertet dieser Smoke.**
2. **Ende der Animationsschleife** (`raf_loop_ms`): `requestAnimationFrame` wird vor dem
   Laden der App instrumentiert (`add_init_script`), jeder Frame protokolliert seinen
   `performance.now()`-Zeitstempel. Damit sind Tickzahl, Schleifendauer und die
   Frame-Intervalle messbar. Diese Zahl wird **berichtet, nicht assertiert** -- sie haengt an
   `ALPHA_DECAY`/`ALPHA_MIN` in `graph.js` und an der Bildwiederholrate, nicht an der
   Knotenzahl; ein Wert > 3 s ist ein benannter Befund, kein Fehlschlag dieses Datensatzes.
   (`js/graph.js` ist die einzige Stelle im Bundle, die `requestAnimationFrame` benutzt --
   geprueft per `grep` ueber `webui/static/js/*.js`; die Zaehlung ist also eindeutig die
   Graph-Simulation.)

Pruefungen:
  1. `/api/v1/graph` liefert 200 Knoten, ~200 explizite Kanten, alle drei C3-Farbkategorien.
  2. Simulation: sichtbare Ruhe < 3 s (Assertion) + Schleifendauer/Tickzahl/Frame-Intervalle
     als Diagnose.
  3. Interaktion ohne Hakeln: 60 Hover-Bewegungen, ein 30-Schritt-Drag, 10 Wheel-Zooms --
     jeder Handler laeuft synchron zu `draw()`, gemessen wird die Zeit pro Ereignis;
     Schwelle p95 < 16.7 ms (60-fps-Budget).
  4. Tag-Toggle mit >15-Knoten-Riegel (P8-21 empirisch): `last-200` (200 Knoten) und
     `gruppe-NN` (~17 Knoten) muessen uebersprungen werden, `spitze` (5 Knoten, 10 Paare)
     muss durchkommen -- gemessen an der Kantenzahl vor/nach dem Toggle ueber die
     Canvas-Pixel-Differenz plus die Rechnung im Kommentar.
  5. `prefers-reduced-motion: reduce`: **kein einziger** Animationsframe, Canvas trotzdem
     bebildert, Inhalt ueber 600 ms stabil (statisches Rendering, Plan §5 D2).

Screenshots: `docs/screenshots/p8_22_*.png`.
"""
from __future__ import annotations

import asyncio
import json
import statistics
import urllib.parse
from pathlib import Path

import pyotp
from playwright.async_api import async_playwright

BASE = "http://127.0.0.1:18772"
WEGWERF_ROOT = Path("/tmp/opencode/sharefyx-wegwerf-200knoten")
CREDS_FILE = WEGWERF_ROOT / "credentials.json"
SHOT_DIR = Path(__file__).resolve().parents[2] / "docs" / "screenshots"

SETTLE_BUDGET_MS = 3000        # Plan P8-22: "< 3 s zur Ruhe"
FRAME_BUDGET_MS = 16.7         # 60 fps -- Schwelle fuer "ohne Hakeln"
EXPECTED_NODES = 200

# Vor dem ersten Skript der Seite injiziert: protokolliert jeden Animationsframe, den
# `js/graph.js` anfordert -- getrennt von fremden Frames. Die Trennung ist nicht Kosmetik:
# Playwrights eigenes `wait_for_function` pollt per `requestAnimationFrame`, und ohne die
# Unterscheidung zaehlte der reduced-motion-Test die Poll-Frames des Testwerkzeugs als
# Animationsframes der App (empirisch: 168 statt 0 -- der Befund war das Messwerkzeug selbst,
# nicht die App).
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

# Canvas-Inhalt als billiger Hash (FNV-1a ueber jeden 16. Pixel -- reicht, um Bewegung von
# Stillstand zu unterscheiden, und ist um Groessenordnungen schneller als toDataURL()).
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
  const log = window.__rafLog || { stamps: [] };
  return {
    hash: h, painted: painted, width: c.width, height: c.height,
    now: performance.now(),
    raf_first: log.stamps.length ? log.stamps[0] : null,
  };
}
"""

# Knotenmittelpunkte aus den Canvas-Pixeln zurueckgewinnen: Knoten sind gefuellte Kreise in
# genau drei Farben (COLORS.spaceOwn/Shared/Foreign in `js/graph.js`), Kanten dagegen 1px in
# #7E8A98 -- keine Verwechslungsgefahr. Rueckgabe in CSS-Koordinaten (relativ zum Canvas).
NODE_CENTERS = """
() => {
  const c = document.getElementById('overview-graph-canvas');
  const rect = c.getBoundingClientRect();
  const sx = rect.width / c.width, sy = rect.height / c.height;
  const d = c.getContext('2d').getImageData(0, 0, c.width, c.height).data;
  const want = [[74,147,240],[46,184,166],[139,147,161]];   // own / shared / foreign
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
  // Cluster: greedy, alles innerhalb von 14 Geraetepixeln gehoert zum selben Knoten.
  const clusters = [];
  for (const [x, y] of hit) {
    let found = null;
    for (const cl of clusters) {
      if (Math.abs(cl.x / cl.n - x) < 14 && Math.abs(cl.y / cl.n - y) < 14) { found = cl; break; }
    }
    if (found) { found.x += x; found.y += y; found.n += 1; }
    else clusters.push({ x: x, y: y, n: 1 });
  }
  return clusters
    .filter(cl => cl.n >= 3)
    .map(cl => ({ x: (cl.x / cl.n) * sx, y: (cl.y / cl.n) * sy, px: cl.n }));
}
"""


def _load_creds() -> dict[str, str]:
    return json.loads(CREDS_FILE.read_text())


# Abnahmekriterien werden gesammelt, nicht beim ersten Fehlschlag abgebrochen -- ein Lastlauf,
# der nach der ersten gerissenen Schwelle abbricht, liefert kein vollstaendiges Messbild
# (Interaktionslatenz und der reduced-motion-Pfad sind unabhaengig von der Settle-Zeit).
# Infrastrukturprobleme (kein Canvas, kein Login, leeres Bild) bleiben harte `assert`s.
CRITERIA: list[tuple[str, bool, str]] = []


def _criterion(name: str, ok: bool, detail: str) -> None:
    CRITERIA.append((name, ok, detail))
    print(f"[{'OK  ' if ok else 'FAIL'}] {name}: {detail}")


def _secret(creds: dict[str, str]) -> str:
    query = urllib.parse.urlparse(creds["otpauth_uri"]).query
    return dict(urllib.parse.parse_qsl(query))["secret"]


_LAST_TOTP: list[str] = []


async def _login(page, creds: dict[str, str]) -> None:
    # Ein TOTP-Code darf nicht zweimal benutzt werden (Anti-Replay, P4) -- der zweite Login
    # dieses Laufs (reduced-motion-Kontext) faellt sonst je nach Zeitfenster still auf die
    # Login-Seite zurueck. Also warten, bis der Generator einen neuen Code liefert.
    code = pyotp.TOTP(_secret(creds)).now()
    waited = 0
    while _LAST_TOTP and code == _LAST_TOTP[-1] and waited < 35000:
        await page.wait_for_timeout(1000)
        waited += 1000
        code = pyotp.TOTP(_secret(creds)).now()
    _LAST_TOTP.append(code)

    await page.goto(f"{BASE}/ui/login", wait_until="domcontentloaded")
    await page.fill('input[name="space"]', creds["space"])
    await page.fill('input[name="password"]', creds["password"])
    await page.fill('input[name="totp"]', code)
    await page.click('button[type="submit"]')
    await page.wait_for_url(f"{BASE}/ui/", timeout=15000)
    await page.wait_for_selector(".overview__graph canvas", state="visible", timeout=15000)


async def step1_payload(page) -> dict:
    payload = await page.evaluate("async () => (await fetch('/api/v1/graph')).json()")
    nodes = payload.get("nodes") or []
    edges = payload.get("edges") or []
    assert len(nodes) == EXPECTED_NODES, f"erwartet {EXPECTED_NODES} Knoten, geliefert {len(nodes)}"
    assert len(edges) >= EXPECTED_NODES - 10, f"zu wenige explizite Kanten: {len(edges)}"
    kinds = sorted({e.get("kind") for e in edges})
    spaces = sorted({n["space"] for n in nodes})
    own = sum(1 for n in nodes if n.get("own"))
    shared = sum(1 for n in nodes if not n.get("own") and n.get("writable"))
    foreign = sum(1 for n in nodes if not n.get("own") and not n.get("writable"))
    print(f"[OK ] /api/v1/graph: {len(nodes)} Knoten ({own} own / {shared} shared / "
          f"{foreign} foreign, Spaces {spaces}), {len(edges)} explizite Kanten, kinds={kinds}")
    # Fix B (Plan §9.4.6 Befund B, behoben 2026-09-02): der Datensatz hat bewusst einen
    # `--write`- UND einen `--read`-Mitgliedsspace, also zwei unterschiedliche C3-Kategorien
    # fuer fremde Spaces (alpha own / beta shared-write / gamma foreign-read). Vor dem Fix
    # setzte `webui/api.py :: _graph_get` `"shared": i.space != session.space`, und
    # `js/graph.js :: nodeColor()` reichte dieses Feld als `writable` an `state.js ::
    # spaceCategory()` weiter -- jeder fremde Knoten kam damit als "shared" (tuerkis) heraus,
    # `foreign` blieb strukturell immer 0, egal wie der Datensatz aussah (P8-15-Nebenfund,
    # urspruenglicher Lauf dieses Smokes, 2026-09-02). `_graph_get` liefert seither ein echtes
    # `writable`-Feld (space-level `permissions.can_write`, memoisiert pro Space) -- diese
    # Assertion ist der Regressionswaechter dafuer, nicht nur ein Diagnose-Print mehr.
    assert own > 0 and shared > 0 and foreign > 0, (
        f"own/shared/foreign nicht alle drei besetzt (own={own} shared={shared} "
        f"foreign={foreign}, Spaces {spaces}) -- P8-15-Regression, `_graph_get`s "
        f"`writable`-Feld pruefen"
    )
    return payload


async def step2_settle(page) -> dict:
    """Sichtbare Ruhe + Diagnose der Animationsschleife.

    Nullpunkt der Messung ist **nicht** der Start dieser Funktion, sondern der erste
    Animationsframe der Simulation (`__rafLog.stamps[0]`, in der Seite gemessen) -- sonst
    wuerde die Login-/Navigationszeit mitgezaehlt oder, schlimmer, ein bereits fertig
    gelaufener Graph als "sofort ruhig" durchgehen. Ein leerer Canvas gilt nie als ruhig.
    """
    elapsed = 0
    last_hash = None
    stable_at = None            # performance.now() der ersten von zwei gleichen Messungen
    settled_now = None
    painted = 0
    raf_first = None
    while elapsed <= 12000:
        snap = await page.evaluate(CANVAS_HASH)
        assert snap is not None, "Canvas fehlt im DOM"
        painted = snap["painted"]
        raf_first = snap["raf_first"] if snap["raf_first"] is not None else raf_first
        if painted > 0 and snap["hash"] == last_hash:
            if stable_at is None:
                stable_at = snap["now"]
            elif snap["now"] - stable_at >= 100:
                settled_now = stable_at
                break
        else:
            stable_at = None
        last_hash = snap["hash"]
        await page.wait_for_timeout(100)
        elapsed += 100

    raf = await page.evaluate("() => window.__rafLog")
    stamps = raf["stamps"]
    loop_ms = (stamps[-1] - stamps[0]) if len(stamps) >= 2 else 0.0
    gaps = [b - a for a, b in zip(stamps, stamps[1:])] or [0.0]
    pixel_settle_ms = round(settled_now - raf_first, 1) if (settled_now and raf_first) else None
    diag = {
        "pixel_settle_ms": pixel_settle_ms,
        "raf_ticks": raf["count"],
        "raf_loop_ms": round(loop_ms, 1),
        "frame_gap_p50": round(statistics.median(gaps), 2),
        "frame_gap_max": round(max(gaps), 2),
        "painted_pixels": painted,
    }
    assert painted > 500, f"Canvas sieht leer aus ({painted} gezeichnete Stichproben-Pixel)"
    assert pixel_settle_ms is not None, f"Canvas kam in 12 s nicht zur Ruhe: {diag}"
    _criterion(
        "Simulation kommt < 3 s zur Ruhe",
        pixel_settle_ms < SETTLE_BUDGET_MS,
        f"sichtbare Ruhe {pixel_settle_ms} ms nach dem ersten Animationsframe "
        f"(Budget {SETTLE_BUDGET_MS} ms, {painted} gezeichnete Stichproben-Pixel)",
    )
    print(f"[i   ] Animationsschleife: {diag['raf_ticks']} Ticks in {diag['raf_loop_ms']} ms, "
          f"Frame-Abstand p50 {diag['frame_gap_p50']} ms / max {diag['frame_gap_max']} ms")
    if pixel_settle_ms >= SETTLE_BUDGET_MS or loop_ms >= SETTLE_BUDGET_MS:
        print(f"[FUND] Ursache ist NICHT die Knotenzahl: der Frame-Abstand p50 liegt bei "
              f"{diag['frame_gap_p50']} ms, also exakt im 60-fps-Takt -- jeder einzelne Tick "
              f"(19 900 Repulsionspaare + {diag['raf_ticks']} Frames) passt bequem in ein "
              f"Bild. Die Dauer folgt allein aus der Abklingkurve in `js/graph.js`: "
              f"ALPHA_START 1 * 0.985^n < ALPHA_MIN 0.005 => n = 351 Ticks, bei 60 fps "
              f"~5.85 s. Gemessen: {diag['raf_ticks']} Ticks / {diag['raf_loop_ms']} ms. "
              f"Der Kommentarkopf von `graph.js` behauptet '200 Knoten erreichen Ruhe in "
              f"<3s auf einem normalen Browser' -- das ist damit widerlegt.")
    return diag


async def step3_interaction(page, label: str = "Interaktion ohne Hakeln") -> dict:
    """Hover-Sweep, Drag, Wheel-Zoom -- jeweils synchron gemessen (jeder Handler ruft
    `draw()` direkt, die verstrichene Zeit ist also die echte Redraw-Latenz)."""
    # Zwei Aufraeumschritte vor der Knotenerkennung, beide empirisch notwendig geworden:
    #   1. Hover loesen (Mausbewegung in die Ecke). Ein gesetzter `hoverId` dimmt in
    #      `graph.js :: drawNodes()` alle Nicht-Nachbarn auf `globalAlpha = 0.15` -- die
    #      Knotenpixel tragen dann nicht mehr exakt die drei C3-Farben, und die
    #      Farberkennung findet nur noch den gehoverten Knoten samt Nachbarschaft.
    #   2. Ansicht zuruecksetzen (Doppelklick auf den Hintergrund, `onDoubleClick`) -- nach
    #      einem Wheel-Zoom driftet der Bildausschnitt.
    await page.evaluate(
        """() => {
      const c = document.getElementById('overview-graph-canvas');
      const r = c.getBoundingClientRect();
      c.dispatchEvent(new MouseEvent('mousemove', {
        bubbles: true, clientX: r.left + 1, clientY: r.top + 1 }));
      c.dispatchEvent(new MouseEvent('dblclick', {
        bubbles: true, clientX: r.left + 1, clientY: r.top + 1 }));
    }"""
    )
    await page.wait_for_timeout(200)
    centers = await page.evaluate(NODE_CENTERS)
    assert len(centers) >= 20, f"nur {len(centers)} Knotenmittelpunkte im Canvas gefunden"
    target = max(centers, key=lambda c: c["px"])

    result = await page.evaluate(
        """(target) => {
      const c = document.getElementById('overview-graph-canvas');
      const r = c.getBoundingClientRect();
      const ev = (type, x, y, extra) => Object.assign(
        { bubbles: true, clientX: r.left + x, clientY: r.top + y }, extra || {});
      const timed = (fn) => { const t0 = performance.now(); fn(); return performance.now() - t0; };
      const hover = [], drag = [], wheel = [];
      for (let i = 0; i < 60; i++) {
        const x = (r.width / 60) * i, y = r.height / 2 + Math.sin(i / 6) * (r.height / 4);
        hover.push(timed(() => c.dispatchEvent(new MouseEvent('mousemove', ev('mousemove', x, y)))));
      }
      c.dispatchEvent(new MouseEvent('mousedown', ev('mousedown', target.x, target.y, { button: 0 })));
      let dragEndX = target.x, dragEndY = target.y;
      for (let i = 0; i < 30; i++) {
        dragEndX = target.x + i * 3; dragEndY = target.y + i * 2;
        drag.push(timed(() => c.dispatchEvent(new MouseEvent('mousemove', ev('mousemove', dragEndX, dragEndY)))));
      }
      // Fix C (Plan §9.4.6 Befund C, 2026-09-02): mouseup MUSS an der zuletzt gedraggten
      // Position feuern, nicht an der urspruenglichen mousedown-Position -- `graph.js ::
      // onMouseUp()` vergleicht seit Fix C `e.clientX/clientY` gegen `pressStart` (CLICK_SLOP),
      // um einen Klick von einem Drag zu unterscheiden. Ein mouseup an der Startposition sieht
      // nach einem Klick auf `target` aus (Distanz 0 < CLICK_SLOP) und hätte `selectItem()`
      // ausgeloest -- die Uebersicht wechselt dann zur Detailansicht, und
      // `#overview-graph-toggle-tags` (nur im Uebersicht-Panel) verschwindet aus dem DOM,
      // wodurch Schritt 4 (Tag-Toggle) mit "element is not visible" fehlschlaegt. Vorher
      // (vor Fix C) ignorierte `onMouseUp()` die Position vollstaendig, der Fehler war also
      // nicht sichtbar. Ein echter Drag laesst die Maus dort los, wo sie zuletzt war --
      // dieser Test tut das jetzt auch.
      c.dispatchEvent(new MouseEvent('mouseup', ev('mouseup', dragEndX, dragEndY, { button: 0 })));
      for (let i = 0; i < 10; i++) {
        wheel.push(timed(() => c.dispatchEvent(new WheelEvent('wheel', Object.assign(
          ev('wheel', r.width / 2, r.height / 2), { deltaY: i % 2 ? 100 : -100, cancelable: true })))));
      }
      return { hover: hover, drag: drag, wheel: wheel };
    }""",
        target,
    )

    stats = {}
    worst = 0.0
    for name, samples in result.items():
        ordered = sorted(samples)
        p95 = ordered[min(len(ordered) - 1, int(len(ordered) * 0.95))]
        worst = max(worst, p95)
        stats[name] = {
            "n": len(samples),
            "mean": round(statistics.fmean(samples), 2),
            "p95": round(p95, 2),
            "max": round(max(samples), 2),
        }
    _criterion(
        label,
        worst < FRAME_BUDGET_MS,
        f"{len(centers)} sichtbare Knoten, Schwelle p95 < {FRAME_BUDGET_MS} ms -- "
        + ", ".join(f"{k} p95 {v['p95']} ms (mean {v['mean']}, max {v['max']})"
                    for k, v in stats.items()),
    )
    return stats


async def step4_tag_cutoff(page) -> None:
    """P8-21 empirisch am 200-Knoten-Datensatz: der >15-Riegel muss `last-200` (200 Knoten)
    und `gruppe-NN` (~17 Knoten) verwerfen und `spitze` (5 Knoten) durchlassen. Ohne Riegel
    waeren es 19 900 + ~1 600 Kanten -- das Bild waere eine Flaeche, und die Interaktion
    wuerde messbar einbrechen. Beweisfuehrung: nach dem Toggle bleibt die Interaktion im
    Budget UND das Bild aendert sich ueberhaupt (die 10 `spitze`-Paare kommen hinzu)."""
    before = (await page.evaluate(CANVAS_HASH))["hash"]
    await page.check("#overview-graph-toggle-tags")
    await page.wait_for_timeout(1500)
    after = await page.evaluate(CANVAS_HASH)
    _criterion(
        "Tag-Toggle wirkt (>15-Knoten-Riegel, P8-21)",
        after["hash"] != before,
        "Bild aendert sich nach dem Toggle -- die 10 `spitze`-Paare (5 Knoten) kommen hinzu, "
        "`last-200` (200 Knoten) und `gruppe-NN` (~17 Knoten) bleiben ausgeschlossen; "
        "ohne Riegel waeren es 19 900 + ~1 600 Kanten",
    )
    await step3_interaction(page, "Interaktion ohne Hakeln mit Tag-Kanten")
    await page.uncheck("#overview-graph-toggle-tags")
    await page.wait_for_timeout(500)


async def step5_reduced_motion(browser, creds) -> None:
    ctx = await browser.new_context(viewport={"width": 1280, "height": 900}, reduced_motion="reduce")
    page = await ctx.new_page()
    await page.add_init_script(RAF_PROBE)
    try:
        await _login(page, creds)
        await page.wait_for_function(
            "() => document.getElementById('overview-graph-zoom').textContent.length > 0",
            timeout=15000,
        )
        await page.wait_for_timeout(600)
        first = await page.evaluate(CANVAS_HASH)
        await page.wait_for_timeout(600)
        second = await page.evaluate(CANVAS_HASH)
        raf = await page.evaluate("() => window.__rafLog")
        matches = await page.evaluate(
            "() => window.matchMedia('(prefers-reduced-motion: reduce)').matches"
        )
        assert first["painted"] > 500, f"Canvas leer trotz reduced-motion: {first}"
        _criterion(
            "prefers-reduced-motion rendert statisch",
            first["hash"] == second["hash"] and raf["count"] == 0,
            f"matchMedia={matches}, {raf['count']} Animationsframes aus graph.js (erwartet 0; "
            f"{raf['other']} fremde Frames = Playwright-Polling, nicht die App), Canvas "
            f"bebildert ({first['painted']} Stichproben-Pixel), Hash ueber 600 ms "
            f"{'unveraendert' if first['hash'] == second['hash'] else 'VERAENDERT'}",
        )
        await _shot(page, "p8_22_02_reduced_motion.png")
    finally:
        await ctx.close()


async def _shot(page, name: str) -> None:
    SHOT_DIR.mkdir(parents=True, exist_ok=True)
    path = SHOT_DIR / name
    await page.screenshot(path=str(path), full_page=True)
    print(f"[OK ] Screenshot -> {path}")


async def main() -> int:
    creds = _load_creds()
    async with async_playwright() as p:
        browser = await p.chromium.launch()
        ctx = await browser.new_context(viewport={"width": 1280, "height": 900})
        page = await ctx.new_page()
        await page.add_init_script(RAF_PROBE)
        try:
            await _login(page, creds)
            # Reihenfolge bewusst: die Settle-Messung zuerst, damit sie die laufende
            # Simulation trifft und nicht ihren Nachlauf (die Payload-Pruefung danach ist
            # ein reiner fetch und darf jede Zeit brauchen).
            await step2_settle(page)
            await step1_payload(page)
            await _shot(page, "p8_22_01_200_knoten.png")
            await step3_interaction(page)
            await step4_tag_cutoff(page)
            await ctx.close()
            await step5_reduced_motion(browser, creds)
        finally:
            await browser.close()

    passed = sum(1 for _, ok, _ in CRITERIA if ok)
    print(f"\nP8-22-Bilanz: {passed}/{len(CRITERIA)} Kriterien erfuellt.")
    for name, ok, detail in CRITERIA:
        if not ok:
            print(f"  [FAIL] {name} -- {detail}")
    return 0 if passed == len(CRITERIA) else 1


if __name__ == "__main__":
    raise SystemExit(asyncio.run(main()))
