#!/usr/bin/env python3
"""Phase 8 P8-21 d -- exakter Tag-Kanten-Zaehler gegen die laufende 200-Knoten-Wegwerf.

Der bestehende `p8_22_smoke.py :: step4_tag_cutoff` beweist nur "Canvas-Hash aendert sich
UND Interaktion bleibt smooth" -- das unterscheidet einen korrekten >15-Riegel nicht von
einem kaputten (ein kaputter Riegel wuerde das Bild auch aendern, moeglicherweise sogar bei
einem einzelnen Frame noch fluessig bleiben). Dieses Skript zaehlt die tatsaechlich
gezeichneten Tag-Kanten exakt, indem es `CanvasRenderingContext2D.prototype.setLineDash`
und `.stroke()` per `addInitScript` instrumentiert -- BEVOR irgendein App-Code laedt, ohne
eine Zeile Quellcode zu aendern. `graph.js :: drawEdges()` ruft `ctx.setLineDash([4,4])`
unmittelbar vor `ctx.stroke()` fuer jede Tag-Kante (Zeile 399-409) -- das Patch zaehlt genau
diese Sequenz in einem einzelnen `draw()`-Aufruf.

Erwartung (aus `wegwerf_setup_200knoten.py`s Saat-Logik, TAG_CLIQUE_LIMIT=15 in graph.js):
  - `spitze` liegt auf genau 5 Knoten -> C(5,2) = 10 Kanten, MUSS durchkommen.
  - `last-200` liegt auf allen 200 Knoten -> C(200,2) = 19900, MUSS 0 sein (Riegel).
  - `gruppe-00`..`gruppe-11` liegen auf ~16-17 Knoten (>15) -> MUSS 0 sein (Riegel).
  => exakt 10 Tag-Kanten gezeichnet, nicht mehr, nicht weniger.

Standing-Permission-Rahmen: liest nur die bereits laufende Wegwerf-Instanz (Port 18772,
PID separat verwaltet), kein Service-Touch, kein `pkill -f`, kein Setup/Teardown hier --
die Instanz bleibt fuer Folgeproben stehen.
"""
from __future__ import annotations

import asyncio
import json
import sys
import urllib.parse
from pathlib import Path

import pyotp
from playwright.async_api import async_playwright

REPO_ROOT = Path(__file__).resolve().parents[2]
SCREENSHOT_DIR = REPO_ROOT / "docs" / "screenshots"
CREDS_PATH = Path("/tmp/opencode/sharefyx-wegwerf-200knoten/credentials.json")
PORT = 18772
BASE_URL = f"http://127.0.0.1:{PORT}"

EXPECTED_SPITZE_EDGES = 10  # C(5,2)

INIT_SCRIPT = """
window.__tagEdgeProbe = { tag: 0, folder: 0, plain: 0, calls: 0 };
(function () {
  const proto = CanvasRenderingContext2D.prototype;
  const origSetLineDash = proto.setLineDash;
  const origStroke = proto.stroke;
  let lastDash = [];
  proto.setLineDash = function (segments) {
    lastDash = segments || [];
    return origSetLineDash.apply(this, arguments);
  };
  proto.stroke = function () {
    // drawEdges() ruft moveTo/lineTo/stroke ausschliesslich fuer Kanten (Knoten
    // benutzen arc()+fill(), keine stroke()-Aufrufe) -- jeder stroke()-Call in
    // dieser App IST eine gezeichnete Kante.
    const dashKey = lastDash.join(",");
    if (dashKey === "4,4") window.__tagEdgeProbe.tag++;
    else if (dashKey === "1.5,3") window.__tagEdgeProbe.folder++;
    else window.__tagEdgeProbe.plain++;
    window.__tagEdgeProbe.calls++;
    return origStroke.apply(this, arguments);
  };
})();
"""


def _read_creds() -> dict:
    creds = json.loads(CREDS_PATH.read_text())
    secret_b32 = urllib.parse.unquote(creds["otpauth_uri"].split("secret=")[1].split("&")[0])
    creds["_secret_b32"] = secret_b32
    return creds


async def _login(page, space: str, password: str, secret_b32: str) -> None:
    await page.goto(f"{BASE_URL}/ui/login")
    await page.fill('input[name="space"]', space)
    await page.fill('input[name="password"]', password)
    await page.fill('input[name="totp"]', pyotp.TOTP(secret_b32).now())
    async with page.expect_navigation(timeout=10_000):
        await page.click('button[type="submit"]')
    await page.wait_for_url(lambda url: "/ui/login" not in url, timeout=10_000)


async def _probe() -> dict:
    SCREENSHOT_DIR.mkdir(parents=True, exist_ok=True)
    creds = _read_creds()
    result: dict = {}

    async with async_playwright() as p:
        browser = await p.chromium.launch(headless=True)
        ctx = await browser.new_context(viewport={"width": 1440, "height": 900})
        await ctx.add_init_script(INIT_SCRIPT)
        page = await ctx.new_page()

        await _login(page, creds["space"], creds["password"], creds["_secret_b32"])
        await page.goto(f"{BASE_URL}/ui/")
        await page.wait_for_selector("canvas", timeout=15_000)
        await page.wait_for_timeout(3500)  # Simulation zur Ruhe kommen lassen (Fix A: ~2.7s)

        # Die Animationsschleife ruft draw() jeden Frame neu auf, auch nach dem Settle
        # (60fps-Redraw fuer Hover/Interaktion) -- ein Zeitfenster erfasst also immer
        # mehrere Frames, nie exakt einen (erste zwei Versuche: 310 und 30 Tag-Kanten
        # gezaehlt, nicht 10 -- kein fester Frame-Grenzwert traf zuverlaessig einen
        # einzelnen Redraw). Ausweg: explizite Kanten (Frontmatter+Body, von der
        # Tag-Kante strukturell unabhaengig) werden JEDEN Frame exakt einmal gezeichnet
        # -- ihre Anzahl aus `/api/v1/graph` ist der Frame-Teiler. tag_count / frames
        # ist damit unabhaengig von der Fenstergroesse und der Zufallszahl der erfassten
        # Frames.
        explicit_edge_count = await page.evaluate(
            "() => fetch('/api/v1/graph').then(r => r.json()).then(g => g.edges.length)"
        )
        result["explicit_edge_count_from_api"] = explicit_edge_count

        def _per_frame(sample: dict) -> dict:
            frames = sample["plain"] / explicit_edge_count if explicit_edge_count else 0
            return {
                "frames_captured": frames,
                "tag_per_frame": sample["tag"] / frames if frames else sample["tag"],
                "raw": sample,
            }

        # Baseline: Tags aus.
        await page.evaluate("window.__tagEdgeProbe = {tag:0, folder:0, plain:0, calls:0}")
        await page.wait_for_timeout(300)
        baseline = await page.evaluate("window.__tagEdgeProbe")
        result["baseline_tags_off"] = _per_frame(baseline)

        # Tags an -- Riegel muss greifen. Reset ERST NACH dem Toggle-Klick + einer
        # kurzen Anlaufzeit fuer rebuildImplicitEdges() -- sonst zaehlt das Fenster
        # ein paar Uebergangs-Frames mit (Klick-Event bis Rebuild fertig ist), die
        # noch mit 0 Tag-Kanten zeichnen und den Mittelwert nach unten ziehen (erster
        # Versuch: 8.93/Frame statt 10 -- 25 von 28 Frames bei 10, 3 Uebergangs-Frames
        # bei 0, 250/28 ergibt den Bruch).
        await page.check("#overview-graph-toggle-tags")
        await page.wait_for_timeout(200)
        await page.evaluate("window.__tagEdgeProbe = {tag:0, folder:0, plain:0, calls:0}")
        await page.wait_for_timeout(300)
        with_tags = await page.evaluate("window.__tagEdgeProbe")
        result["with_tags_on"] = _per_frame(with_tags)

        await page.screenshot(
            path=str(SCREENSHOT_DIR / "c3rest_p821d_01_200knoten_tag_clique_limit.png"),
            full_page=False,
        )

        # Zurueck auf aus, gegenpruefen dass die Tag-Kanten wieder verschwinden.
        await page.uncheck("#overview-graph-toggle-tags")
        await page.wait_for_timeout(300)
        await page.evaluate("window.__tagEdgeProbe = {tag:0, folder:0, plain:0, calls:0}")
        await page.wait_for_timeout(300)
        after_toggle_off = await page.evaluate("window.__tagEdgeProbe")
        result["after_toggle_off"] = _per_frame(after_toggle_off)

        await ctx.close()
        await browser.close()

    return result


def _verdict(result: dict) -> tuple[bool, list[str]]:
    lines = []
    ok = True

    baseline_tag = result["baseline_tags_off"]["tag_per_frame"]
    if baseline_tag != 0:
        ok = False
        lines.append(f"[FAIL] Tags aus, aber {baseline_tag} Tag-Kanten/Frame (erwartet 0)")
    else:
        lines.append("[OK]   Tags aus -> 0 Tag-Kanten/Frame")

    with_tag = result["with_tags_on"]["tag_per_frame"]
    frames = result["with_tags_on"]["frames_captured"]
    if with_tag != EXPECTED_SPITZE_EDGES:
        ok = False
        lines.append(
            f"[FAIL] Tags an -> {with_tag} Tag-Kanten/Frame ({frames} Frames erfasst), "
            f"erwartet genau {EXPECTED_SPITZE_EDGES} (C(5,2) aus 'spitze'). Riegel liess "
            f"entweder last-200 oder eine gruppe-NN durch, oder 'spitze' fehlt/ist falsch gross."
        )
    else:
        lines.append(
            f"[OK]   Tags an -> genau {with_tag} Tag-Kanten/Frame ({frames} Frames erfasst, "
            f"deterministisch ueber den expliziten Kanten-Teiler) -- exakt 'spitze' C(5,2)=10, "
            f"last-200 [200 Knoten] und alle 12 gruppe-NN [~16-17 Knoten] korrekt vom "
            f">15-Riegel ausgeschlossen"
        )

    after_off = result["after_toggle_off"]["tag_per_frame"]
    if after_off != 0:
        ok = False
        lines.append(f"[FAIL] Toggle wieder aus, aber {after_off} Tag-Kanten/Frame noch da")
    else:
        lines.append("[OK]   Toggle wieder aus -> 0 Tag-Kanten/Frame (symmetrisch)")

    return ok, lines


async def _async_main() -> int:
    result = await _probe()
    print(json.dumps(result, indent=2))
    ok, lines = _verdict(result)
    print()
    for line in lines:
        print(line)
    print()
    print(f"P8-21d-Bilanz: {'BESTANDEN' if ok else 'FEHLGESCHLAGEN'}")
    return 0 if ok else 1


def main() -> int:
    return asyncio.run(_async_main())


if __name__ == "__main__":
    raise SystemExit(main())
