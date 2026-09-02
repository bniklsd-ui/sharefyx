#!/usr/bin/env python3
"""Phase 8 P8-24 -- kombinierter End-to-End-Ritt gegen eine Wegwerf-Instanz.

Abnahmezeile P8-24 (Plan §7): "Playwright-Durchlauf gegen Wegwerf: Uebersicht -> Scope ->
Graph -> Knotenklick -> Item". Die bestehenden Smokes decken jeweils einen Abschnitt ab
(`d1_playwright_smoke.py` Chip-Klick, `d2_playwright_smoke.py` Graph + Zoom,
`c4c5_playwright_smoke.py` Design) -- **dieser Lauf ist die zusammenhaengende Strecke** in
einer einzigen Sitzung, ohne Zwischen-Reload.

Standard-Ziel ist die D2-Wegwerf (Port 18768, `wegwerf_setup_d2.py`); `--base`/`--root`
erlauben denselben Ritt gegen jede andere Wegwerf-Instanz (z. B. die 200-Knoten-Instanz aus
`wegwerf_setup_200knoten.py`, Port 18772).

Stationen:
  1. Login -> `/ui/` (Cookie-Session, kein Bearer -- P5-F).
  2. **Uebersicht**: tabellose Space-Zeilen mit Counter-Chips, Legende sichtbar (D1).
  3. **Globaler Scope**: Home/Uebersicht-Knopf schaltet die Listen-Spalte auf "Alle Items"
     (P8-19, V82 -- idempotent, ein zweiter Klick aendert nichts).
  4. **Graph**: `/api/v1/graph` liefert Knoten + Kanten, Canvas ist bebildert, Empty-Hint weg.
  5. **Hover**: ein Knoten unter dem Zeiger dimmt die Nicht-Nachbarn (P8-20, gemessen an der
     Zahl voll deckender Knotenpixel -- gedimmte Knoten zeichnen mit `globalAlpha = 0.15`
     und tragen deshalb nicht mehr exakt die drei C3-Farben).
  6. **Knotenklick -> Item**: echter Mausklick auf einen Knotenmittelpunkt; danach muss die
     Detailspalte das Ziel-Item zeigen (Editor oder Nur-lesen-Ansicht).

Knotenmittelpunkte werden aus den Canvas-Pixeln zurueckgewonnen (die drei Knotenfarben aus
`js/graph.js :: COLORS` sind eindeutig gegen die Kantenfarbe `#7E8A98`) -- `graph.js`
exportiert seinen Zustand nicht, und dieser Smoke fasst den Produktionscode nicht an.

Kriterien werden gesammelt und am Ende bilanziert; ein gerissenes Kriterium bricht den Ritt
nicht ab (eine fehlende Station soll nicht die uebrigen Belege verschlucken).
"""
from __future__ import annotations

import argparse
import asyncio
import json
import urllib.parse
from pathlib import Path

import pyotp
from playwright.async_api import async_playwright

SHOT_DIR = Path(__file__).resolve().parents[2] / "docs" / "screenshots"
DEFAULT_BASE = "http://127.0.0.1:18768"
DEFAULT_ROOT = Path("/tmp/opencode/sharefyx-wegwerf-d2")

CRITERIA: list[tuple[str, bool, str]] = []


def _criterion(name: str, ok: bool, detail: str) -> None:
    CRITERIA.append((name, ok, detail))
    print(f"[{'OK  ' if ok else 'FAIL'}] {name}: {detail}")


# Knotenmittelpunkte + Zahl der voll deckenden Knotenpixel (fuer den Hover-Dim-Nachweis).
NODE_PROBE = """
() => {
  const c = document.getElementById('overview-graph-canvas');
  if (!c) return null;
  const rect = c.getBoundingClientRect();
  const sx = rect.width / c.width, sy = rect.height / c.height;
  const d = c.getContext('2d').getImageData(0, 0, c.width, c.height).data;
  const want = [[74,147,240],[46,184,166],[139,147,161]];   // COLORS.spaceOwn/Shared/Foreign
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
  return {
    opaque_pixels: hit.length,
    left: rect.left, top: rect.top,
    nodes: clusters.filter(cl => cl.n >= 3)
      .map(cl => ({ x: (cl.x / cl.n) * sx, y: (cl.y / cl.n) * sy, px: cl.n })),
  };
}
"""


def _secret(creds: dict[str, str]) -> str:
    query = urllib.parse.urlparse(creds["otpauth_uri"]).query
    return dict(urllib.parse.parse_qsl(query))["secret"]


async def station1_login(page, base: str, creds: dict[str, str]) -> None:
    await page.goto(f"{base}/ui/login", wait_until="domcontentloaded")
    await page.fill('input[name="space"]', creds["space"])
    await page.fill('input[name="password"]', creds["password"])
    await page.fill('input[name="totp"]', pyotp.TOTP(_secret(creds)).now())
    await page.click('button[type="submit"]')
    await page.wait_for_url(f"{base}/ui/", timeout=15000)
    await page.wait_for_selector(".overview__graph canvas", state="visible", timeout=15000)
    _criterion("1 Login -> /ui/", True, f"Cookie-Session gegen {base}, Uebersicht gerendert")


async def station2_overview(page) -> None:
    # Die tabellose Uebersicht wird nach Login asynchron befuellt; `wait_for_selector` auf
    # die erste Zeile ueberbrueckt den initialen Render-Pfad, dann erst auszaehlen.
    await page.wait_for_selector(".overview__spaces .overview__space-row", timeout=10000)
    rows = page.locator(".overview__spaces .overview__space-row")
    count = await rows.count()
    chips = await page.locator(".overview__space-count").count()
    legend = await page.locator(".overview .legend").count()
    tiles = await page.locator(".overview__tiles, .space-card").count()
    _criterion(
        "2 Uebersicht tabellos mit Counter-Chips",
        count >= 1 and chips >= 1 and legend == 1 and tiles == 0,
        f"{count} Space-Zeilen, {chips} Counter-Chips, {legend} Legende, "
        f"{tiles} alte Kachel-/Card-Elemente (erwartet 0)",
    )


async def station3_global_scope(page) -> None:
    await page.click("#home-button")
    # V82: der globale Listen-Scope wird asynchron geladen (zwei Home-Klicks noetig, wenn der
    # erste noch im eigenen-Space-Snapshot landet). Wir warten, bis die Zeilenzahl zweimal
    # hintereinander konstant ist -- dann ist der Ladevorgang abgeschlossen, und der zweite
    # Klick ist der echte Idempotenz-Test.
    async def row_count() -> int:
        return await page.locator(".list__row").count()

    last = -1
    for _ in range(40):          # 40 * 100 ms = 4 s
        n = await row_count()
        if n == last and n > 0:
            break
        last = n
        await page.wait_for_timeout(100)
    crumb = (await page.locator("#list-crumb").inner_text()).strip()
    rows_before = await row_count()
    await page.click("#home-button")
    await page.wait_for_timeout(500)
    crumb2 = (await page.locator("#list-crumb").inner_text()).strip()
    rows_after = await row_count()
    _criterion(
        "3 Globaler 'Alle Items'-Scope (P8-19/V82)",
        "Alle Items" in crumb and crumb2 == crumb and rows_after == rows_before,
        f"Crumb '{crumb}', {rows_before} Zeilen; zweiter Home-Klick idempotent "
        f"(Crumb '{crumb2}', {rows_after} Zeilen)",
    )


async def station4_graph(page) -> dict:
    payload = await page.evaluate("async () => (await fetch('/api/v1/graph')).json()")
    nodes = payload.get("nodes") or []
    edges = payload.get("edges") or []
    probe = await page.evaluate(NODE_PROBE)
    empty_hidden = await page.locator("#overview-graph-empty").evaluate("el => el.hidden")
    assert probe is not None, "Canvas fehlt im DOM"
    _criterion(
        "4 Graph gezeichnet",
        len(nodes) > 0 and len(edges) > 0 and len(probe["nodes"]) > 0 and empty_hidden,
        f"{len(nodes)} Knoten / {len(edges)} explizite Kanten im Payload, "
        f"{len(probe['nodes'])} Knoten im Bild erkannt, Empty-Hint versteckt={empty_hidden}",
    )
    return {"payload": payload, "probe": probe}


async def station5_hover_dim(page, probe: dict) -> dict:
    """Hover dimmt Nicht-Nachbarn (P8-20). Messbar, weil `drawNodes()` gedimmte Knoten mit
    `globalAlpha = 0.15` zeichnet -- deren Pixel tragen danach nicht mehr exakt die
    Knotenfarbe, die Zahl voll deckender Knotenpixel bricht also ein."""
    target = max(probe["nodes"], key=lambda n: n["px"])
    before = probe["opaque_pixels"]
    await page.mouse.move(probe["left"] + target["x"], probe["top"] + target["y"])
    await page.wait_for_timeout(300)
    hovered = await page.evaluate(NODE_PROBE)
    after = hovered["opaque_pixels"]
    _criterion(
        "5 Hover dimmt Nicht-Nachbarn (P8-20)",
        after < before * 0.75,
        f"voll deckende Knotenpixel {before} -> {after} "
        f"({100 * after / max(1, before):.0f} % -- Rest zeichnet mit globalAlpha 0.15)",
    )
    return {"target": target, "left": probe["left"], "top": probe["top"]}


async def station6_node_click(page, payload: dict, aim: dict) -> None:
    """Klick auf den Knoten muss das Item oeffnen (P8-20/P8-24, Plan §5 D2, Fix C ab
    2026-09-02 -- `graph.js :: onMouseUp()` erkennt jetzt einen Klick (< CLICK_SLOP Bewegung
    seit dem mousedown auf einem Knoten) und ruft `selectItem(id)`.

    **[2026-09-02 Korrektur]** die Locators hier zielten auf `#editor`/`#readonly-view`/
    `.readonly`/`#readonly-title` -- keine dieser IDs/Klassen existiert in `app.html`
    (echte IDs: `#detail-editor`/`#detail-readonly`/`#ro-title`, siehe
    `phase5_ui/webui/static/app.html:126-138`). Die Kriteriumspruefung war dadurch VOR Fix C
    strukturell blind (Editor/Nur-lesen wurden nie als sichtbar erkannt, egal ob der Klick
    funktionierte) -- der urspruengliche P8-24-Lauf (5/6, Station 6 FAIL) haette mit den alten
    Selektoren selbst nach einem funktionierenden Klick weiterhin FAIL gezeigt. Erst beim
    Nachpruefen von Fix C aufgefallen: `#field-title` (korrekt) hatte einen echten Knotentitel
    geliefert, aber `editor_open`/`readonly_open` blieben beide 0."""
    titles = {n["title"] for n in payload.get("nodes") or []}
    await page.mouse.click(aim["left"] + aim["target"]["x"], aim["top"] + aim["target"]["y"])
    await page.wait_for_timeout(1200)
    editor_open = await page.locator("#detail-editor:visible").count()
    readonly_open = await page.locator("#detail-readonly:visible").count()
    shown = ""
    for selector in ("#field-title", "#ro-title"):
        loc = page.locator(selector)
        if await loc.count():
            try:
                shown = (await loc.first.input_value()) or ""
            except Exception:
                shown = (await loc.first.inner_text()) or ""
            if shown:
                break
    hit = shown.strip() in titles
    _criterion(
        "6 Knotenklick oeffnet das Item",
        bool(editor_open or readonly_open) and hit,
        f"Editor sichtbar={editor_open}, Nur-lesen sichtbar={readonly_open}, "
        f"angezeigter Titel {shown.strip()!r} ist ein Knotentitel={hit}",
    )
    if not (editor_open or readonly_open):
        print("[FUND] Klick hat das Item NICHT geoeffnet -- `graph.js :: onMouseUp()`/"
              "`selectItem`-Pfad (Fix C) pruefen, oder `#detail-editor`/`#detail-readonly` "
              "sind aus einem anderen Grund nicht sichtbar geworden.")


async def _shot(page, name: str) -> None:
    SHOT_DIR.mkdir(parents=True, exist_ok=True)
    path = SHOT_DIR / name
    await page.screenshot(path=str(path), full_page=True)
    print(f"[OK ] Screenshot -> {path}")


async def main() -> int:
    parser = argparse.ArgumentParser(description="Phase 8 kombinierter E2E-Ritt (P8-24)")
    parser.add_argument("--base", default=DEFAULT_BASE, help=f"Default {DEFAULT_BASE}")
    parser.add_argument("--root", default=str(DEFAULT_ROOT), help=f"Default {DEFAULT_ROOT}")
    parser.add_argument("--shot-prefix", default="p8_24", help="Praefix der Screenshots")
    args = parser.parse_args()

    creds = json.loads((Path(args.root) / "credentials.json").read_text())

    async with async_playwright() as p:
        browser = await p.chromium.launch()
        ctx = await browser.new_context(viewport={"width": 1280, "height": 900})
        page = await ctx.new_page()
        try:
            await station1_login(page, args.base, creds)
            await station2_overview(page)
            await station3_global_scope(page)
            # Der Graph laeuft nach dem Home-Klick neu an (`app.js :: loadGraphPanel()`) --
            # erst zur Ruhe kommen lassen, sonst zielt der Klick auf eine alte Position.
            await page.wait_for_timeout(7000)
            graph = await station4_graph(page)
            await _shot(page, f"{args.shot_prefix}_01_uebersicht_graph.png")
            aim = await station5_hover_dim(page, graph["probe"])
            await _shot(page, f"{args.shot_prefix}_02_hover_dim.png")
            await station6_node_click(page, graph["payload"], aim)
            await _shot(page, f"{args.shot_prefix}_03_nach_knotenklick.png")
        finally:
            await browser.close()

    passed = sum(1 for _, ok, _ in CRITERIA if ok)
    print(f"\nP8-24-Bilanz: {passed}/{len(CRITERIA)} Stationen bestanden.")
    for name, ok, detail in CRITERIA:
        if not ok:
            print(f"  [FAIL] {name} -- {detail}")
    return 0 if passed == len(CRITERIA) else 1


if __name__ == "__main__":
    raise SystemExit(asyncio.run(main()))
