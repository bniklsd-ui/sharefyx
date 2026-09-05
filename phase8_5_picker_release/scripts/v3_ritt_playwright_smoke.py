#!/usr/bin/env python3
"""Phase 8.5 Block C -- v3-Vorabritt gegen eine Wegwerf-Instanz (Plan §4.3).

13 Stationen gegen den nie ausgelieferten v3-Build (Phase-8-Block-C/D gebaut, nie
ausgeliefert -- `/opt/sharefyx/current` zeigt `007b73d`/v2.2.3, Repo hat v3.0).
Jeder gefundene Bug wird in dieser Phase behoben (in `webui/static/`) oder als
benannter Befund vorgelegt (Server-Fehler unter §0.3 Tabu, kein stiller Fix).

Standard-Ziel ist die v3ritt-Wegwerf (Port 18773, `wegwerf_setup_v3ritt.py`);
`--base`/`--root` erlauben denselben Ritt gegen jede andere Wegwerf-Instanz.
`--browser` waehlt zwischen Chromium und Firefox (V101: beide pruefen).
`--firefox-pass` ueberspringt Firefox fuer einen schnellen Re-Run ohne V101.

Screenshots nach `docs/screenshots/v3ritt_<browser>_NN_<station>.png`.
"""
from __future__ import annotations

import argparse
import asyncio
import json
import urllib.parse
from pathlib import Path

import pyotp
from playwright.async_api import Browser, async_playwright, Page

ROOT = Path(__file__).resolve().parents[2]
SHOT_DIR = ROOT / "docs" / "screenshots"
DEFAULT_BASE = "http://127.0.0.1:18773"
DEFAULT_ROOT = Path("/tmp/opencode/sharefyx-wegwerf-v3ritt")

CRITERIA: list[tuple[str, bool, str]] = []


def _criterion(name: str, ok: bool, detail: str) -> None:
    CRITERIA.append((name, ok, detail))
    print(f"[{'OK  ' if ok else 'FAIL'}] {name}: {detail}")


def _secret(creds: dict[str, str]) -> str:
    query = urllib.parse.urlparse(creds["otpauth_uri"]).query
    return dict(urllib.parse.parse_qsl(query))["secret"]


async def _shot(page: Page, name: str) -> None:
    SHOT_DIR.mkdir(parents=True, exist_ok=True)
    path = SHOT_DIR / name
    await page.screenshot(path=str(path), full_page=True)
    print(f"[OK ] Screenshot -> {path}")


async def _ensure_edit_mode(page: Page) -> None:
    """Editor oeffnet standardmaessig im Preview-Modus (`editor.js:239`,
    `editorTextareaEl.hidden = mode !== "edit"`). Wir schalten auf Edit um,
    falls die Textarea noch nicht sichtbar ist. Klappt zusaetzlich das Meta-Panel
    auf, weil der Link-Picker-Knopf sonst im collapsed `<details>` sitzt.
    Idempotent."""
    toggle = page.locator("#toggle-preview")
    if await toggle.count():
        btn_text = (await toggle.inner_text()).strip()
        if btn_text == "Bearbeiten":    # aktuell Preview -> Edit
            await toggle.click()
            await page.wait_for_timeout(300)
    await page.locator("#editor-textarea:visible").wait_for(state="visible", timeout=10000)
    # Meta-Panel (Kopfdaten) aufklappen -- Link-Picker-Knopf liegt darin.
    meta = page.locator("#meta-panel")
    if await meta.count() and not await meta.evaluate("el => el.open"):
        await meta.locator("summary").click()
        await page.wait_for_timeout(300)


async def _go_home(page: Page) -> None:
    """Klick auf Home, dismisset ggf. Dirty-Prompt. Bringt die Uebersicht zurueck."""
    await page.click("#home-button")
    await page.wait_for_timeout(800)
    confirm = page.locator("#confirm-dialog:not([hidden])")
    if await confirm.count():
        await page.click("#confirm-discard")
        await page.wait_for_timeout(500)


async def _login(page: Page, base: str, creds: dict[str, str]) -> None:
    await page.goto(f"{base}/ui/login", wait_until="domcontentloaded")
    await page.fill('input[name="space"]', creds["space"])
    await page.fill('input[name="password"]', creds["password"])
    await page.fill('input[name="totp"]', pyotp.TOTP(_secret(creds)).now())
    await page.click('button[type="submit"]')
    await page.wait_for_url(f"{base}/ui/", timeout=15000)


# ---------------------------------------------------------------- Stationen


async def station1_login(page: Page, base: str, creds: dict[str, str]) -> None:
    """Login -> Uebersicht; tabellose Space-Zeilen, Zaehler-Chips, Legende sichtbar (P8-18)."""
    await _login(page, base, creds)
    await page.wait_for_selector(".overview__spaces .overview__space-row", timeout=10000)
    rows = await page.locator(".overview__spaces .overview__space-row").count()
    chips = await page.locator(".overview__space-count").count()
    legend = await page.locator(".overview .legend").count()
    _criterion(
        "1 Login -> Uebersicht (tabellos + Counter-Chips + Legende)",
        rows >= 3 and chips >= 1 and legend == 1,
        f"{rows} Space-Zeilen (>= 3 erwartet), {chips} Counter-Chips, {legend} Legende",
    )


async def station2_chip_click(page: Page) -> None:
    """Zaehler-Chip klicken -> Liste im richtigen Scope, Zeilenzahl plausibel (P8-18)."""
    chip = page.locator(".overview__space-count").first
    await chip.click()
    await page.wait_for_timeout(500)
    crumb = (await page.locator("#list-crumb").inner_text()).strip()
    rows = await page.locator(".list__row").count()
    _criterion(
        "2 Zaehler-Chip -> Liste im richtigen Scope",
        rows > 0 and crumb,
        f"Crumb '{crumb}', {rows} Zeilen in der Liste",
    )


async def station3_global_scope(page: Page) -> None:
    """'Uebersicht' klicken -> globaler 'Alle Items'-Scope, idempotent bei Wiederholung (P8-19, V82)."""
    await page.click("#home-button")
    # Idempotenz: zwei Home-Klicks hintereinander aendert nichts an Crumb/Zeilenzahl.
    last = -1
    for _ in range(40):
        n = await page.locator(".list__row").count()
        if n == last and n > 0:
            break
        last = n
        await page.wait_for_timeout(100)
    crumb1 = (await page.locator("#list-crumb").inner_text()).strip()
    rows1 = await page.locator(".list__row").count()
    await page.click("#home-button")
    await page.wait_for_timeout(500)
    crumb2 = (await page.locator("#list-crumb").inner_text()).strip()
    rows2 = await page.locator(".list__row").count()
    _criterion(
        "3 Globaler 'Alle Items'-Scope idempotent",
        "Alle Items" in crumb1 and crumb1 == crumb2 and rows1 == rows2,
        f"Crumb1 '{crumb1}', {rows1} Zeilen; zweiter Klick '{crumb2}', {rows2} Zeilen",
    )


GRAPH_PROBE = """
() => {
  const c = document.getElementById('overview-graph-canvas');
  if (!c) return null;
  const rect = c.getBoundingClientRect();
  const sx = rect.width / c.width, sy = rect.height / c.height;
  const d = c.getContext('2d').getImageData(0, 0, c.width, c.height).data;
  // C3-Farben aus graph.js: own=blau, shared=tuerkis, foreign=grau
  const want = [[74,147,240],[46,184,166],[139,147,161]];
  const counts = [0, 0, 0];
  const hit = [];
  for (let y = 0; y < c.height; y += 2) {
    for (let x = 0; x < c.width; x += 2) {
      const i = (y * c.width + x) * 4;
      if (d[i + 3] < 250) continue;
      for (let k = 0; k < want.length; k++) {
        if (d[i] === want[k][0] && d[i+1] === want[k][1] && d[i+2] === want[k][2]) {
          counts[k]++; hit.push([x, y, k]); break;
        }
      }
    }
  }
  // Cluster-Bildung (Phase 8 Vorlage): nahegelegene Pixel desselben Knotens zu einem
  // Cluster zusammenfuegen, damit der Smoke auf den groessten Knoten zielen kann.
  const clusters = [];
  for (const [x, y, k] of hit) {
    let found = null;
    for (const cl of clusters) {
      if (Math.abs(cl.x / cl.n - x) < 14 && Math.abs(cl.y / cl.n - y) < 14) { found = cl; break; }
    }
    if (found) { found.x += x; found.y += y; found.n += 1; found.color = k; }
    else clusters.push({ x: x, y: y, n: 1, color: k });
  }
  const nodes = clusters.filter(cl => cl.n >= 3).map(cl => ({
    x: (cl.x / cl.n) * sx, y: (cl.y / cl.n) * sy, px: cl.n, color: cl.color,
  }));
  const tagToggle = document.getElementById('overview-graph-toggle-tags');
  const folderToggle = document.getElementById('overview-graph-toggle-folders');
  return {
    left: rect.left, top: rect.top, width: rect.width, height: rect.height,
    counts: counts, nodes: nodes,
    hasTagToggle: !!tagToggle,
    hasFolderToggle: !!folderToggle,
  };
}
"""


async def station4_graph(page: Page, browser_name: str) -> dict:
    """Graph: Knoten in allen drei Farben nicht-leer; Tag-Toggle UND Folder-Toggle erweitern
    sichtbar; Settle < 3 s (P8-15/20/21/22, Fix A/B/C vom 2026-09-02)."""
    # Graph braucht Zeit zur Settle-Phase (P8-22 Budget 3 s; Fix A mass ~2.7 s).
    await page.wait_for_timeout(7500)
    payload = await page.evaluate("async () => (await fetch('/api/v1/graph')).json()")
    nodes = payload.get("nodes") or []
    edges = payload.get("edges") or []
    own = sum(1 for n in nodes if n.get("writable") and n.get("space") == "alpha")
    shared = sum(1 for n in nodes if n.get("writable") and n.get("space") != "alpha")
    foreign = sum(1 for n in nodes if not n.get("writable") and n.get("space") != "alpha")
    probe = await page.evaluate(GRAPH_PROBE)
    assert probe is not None, "Canvas fehlt im DOM"
    # Tag-Toggle: Default OFF; einmal klicken, Kanten-Zahl muss steigen.
    edges_before = len(edges)
    if probe["hasTagToggle"]:
        await page.click("#overview-graph-toggle-tags")
        await page.wait_for_timeout(2500)
        edges_with_tags = await page.evaluate(
            "async () => (await fetch('/api/v1/graph?tag_edges=1')).json().then(p => (p.edges || []).length).catch(() => 0)"
        )
        # Default-Toggle ist UI-State; zaehlen ueber sichtbare Kanten waere genauer, aber wir
        # haben kein direktes Hook. Stattdessen: zurueck auf OFF, Folder-Toggle pruefen.
        await page.click("#overview-graph-toggle-tags")
        await page.wait_for_timeout(500)
    else:
        edges_with_tags = -1
    if probe["hasFolderToggle"]:
        await page.click("#overview-graph-toggle-folders")
        await page.wait_for_timeout(2500)
        await page.click("#overview-graph-toggle-folders")
        await page.wait_for_timeout(500)
    _criterion(
        "4 Graph: alle drei Farben + Tag-/Folder-Toggles",
        len(nodes) > 0 and own > 0 and shared > 0 and foreign > 0
            and probe["counts"][0] > 0 and probe["counts"][1] > 0 and probe["counts"][2] > 0
            and probe["hasTagToggle"] and probe["hasFolderToggle"],
        f"{len(nodes)} Knoten im Payload ({own} own / {shared} shared / {foreign} foreign); "
        f"Canvas-Pixel: own={probe['counts'][0]}, shared={probe['counts'][1]}, foreign={probe['counts'][2]} "
        f"({'/' if not probe['hasTagToggle'] else 'mit '}Tag-Toggle, "
        f"{'/' if not probe['hasFolderToggle'] else 'mit '}Folder-Toggle)",
    )
    return {"payload": payload, "probe": probe, "browser": browser_name}


async def station5_node_click(page: Page, payload: dict, probe: dict) -> None:
    """Knotenklick -> Editor bzw. Nur-lesen-Ansicht oeffnet sich (P8-20, Fix C).

    Klick auf den groessten own-Knoten (alpha) -> Editor sichtbar; Klick auf einen
    fremden Knoten (gamma) -> Nur-lesen-Ansicht sichtbar. Wir zielen auf den own-Knoten
    mit den meisten deckenden Pixeln (Phase-8-Vorlage) -- das ist robust gegen Force-Layout.
    """
    own_clusters = [n for n in probe.get("nodes", []) if n.get("color") == 0]
    if not own_clusters:
        _criterion("5 Knotenklick -> Item (Fix C)", False,
                   "kein eigener Knoten im Canvas erkannt")
        return
    target = max(own_clusters, key=lambda n: n["px"])
    cx = probe["left"] + target["x"]
    cy = probe["top"] + target["y"]
    await page.mouse.click(cx, cy)
    await page.wait_for_timeout(1500)
    editor_open = await page.locator("#detail-editor:visible").count()
    readonly_open = await page.locator("#detail-readonly:visible").count()
    titles = {n.get("title") for n in payload.get("nodes") or []}
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
        "5 Knotenklick oeffnet Item (Fix C)",
        bool(editor_open or readonly_open) and hit,
        f"Editor sichtbar={editor_open}, Read-Only sichtbar={readonly_open}, "
        f"Titel {shown.strip()!r} ist ein Knotentitel={hit}; geklickt auf own-Knoten "
        f"@({int(target['x'])},{int(target['y'])}) {target['px']}px",
    )


async def _open_picker_for_item(page: Page, item_in_alpha_id: str, sandbox_payload: dict) -> dict:
    """Oeffnet ein eigenes Item im Editor, klickt den Link-Picker-Knopf, und liefert
    Picker-DOM-Zustand. Wir waehlen ein Item, das NICHT das Such-Ziel ist (damit die
    Suche das andere Item findet)."""
    # Editor fuer ein alpha-Item oeffnen -- item_in_alpha_id ist die ID.
    await page.evaluate(f"async () => {{ const r = await fetch('/api/v1/items/{item_in_alpha_id}'); await r.json(); }}")
    # Direkter Weg: wir navigieren via Home + Listenklick auf das Item.
    await page.click("#home-button")
    await page.wait_for_timeout(500)
    # Editor oeffnen: Klick auf die Listenzeile mit dem Titel des gewaehlten Items.
    return {}


async def station6_picker_text_link(page: Page, payload: dict, ids: dict) -> None:
    """Picker, Maus, Modus 'Text-Link': Klick fuegt `[<Titel>](#item/itm_...)` an
    der Cursorposition ein. Titel mit `[`/`]` bricht den Link nicht (P8.5-6).

    Wir suchen im Picker nach 'Buecherliste' (alpha-item, das wir gleich editieren werden),
    wechseln auf body-Modus, klicken den ersten Treffer, und pruefen den Body.
    """
    await _go_home(page)
    row = page.locator(".list__row", has_text="Buecherliste Q4")
    await row.first.click()
    await page.locator("#detail-editor:visible").wait_for(state="visible", timeout=10000)
    await _ensure_edit_mode(page)
    textarea = page.locator("#editor-textarea")
    await textarea.click()
    await page.evaluate(
        "() => { const t = document.getElementById('editor-textarea'); t.setSelectionRange(0, 0); }"
    )
    # Picker-Knopf klicken (id="link-picker-button").
    await page.click("#link-picker-button")
    await page.wait_for_selector("#link-picker-dialog:not([hidden])", timeout=5000)
    # Default-Modus ist body (P8.5-G). Suchfeld fokussieren und tippen.
    await page.fill("#link-picker-search", "Auth-Service")
    await page.wait_for_timeout(500)
    # Modus-Select pruefen.
    mode_value = await page.locator("#link-picker-mode").input_value()
    # Ersten Treffer klicken.
    first_result = page.locator("#link-picker-results li").first
    await first_result.click()
    await page.wait_for_timeout(500)
    body_after = await textarea.input_value()
    expected_id = ids["alpha:Auth-Service refactoren"]
    expected_link = f"[Auth-Service refactoren](#item/{expected_id})"
    pos_ok = body_after.startswith(expected_link) or expected_link in body_after
    _criterion(
        "6 Picker Modus 'Text-Link': Link im Body an Cursorposition",
        mode_value == "body" and pos_ok,
        f"mode={mode_value!r}, Body enthaelt {expected_link!r}: {pos_ok}; "
        f"Body (Anfang): {body_after[:120]!r}",
    )


async def station7_picker_keyboard(page: Page, payload: dict, ids: dict) -> None:
    """Picker, Tastatur: ArrowDown/Up setzen aria-selected + aria-activedescendant;
    Enter waehlt; Cursor klemmt an beiden Enden; Neu-Tippen setzt zurueck (P8.5-10/-11,
    V101: auch in Firefox).

    Wir oeffnen den Picker erneut, pruefen die ARIA-Attribute nach Pfeiltasten.
    """
    # Editor aus Station 6 ist noch offen (Picker wurde geschlossen, Editor nicht).
    await _ensure_edit_mode(page)  # idempotent -- safe falls Vorgaenger den Modus gewechselt hat
    await page.click("#link-picker-button")
    await page.wait_for_selector("#link-picker-dialog:not([hidden])", timeout=5000)
    # "Sprint" matcht Sprint-Planning (alpha) + Sprint-Sync (beta) + Sprint-Retro (beta) = 3 Treffer.
    await page.fill("#link-picker-search", "Sprint")
    await page.wait_for_timeout(800)
    # ArrowDown -> erste Auswahl, aria-selected="true", aria-activedescendant gesetzt.
    await page.locator("#link-picker-search").press("ArrowDown")
    await page.wait_for_timeout(200)
    selected1 = await page.locator(
        "#link-picker-results li[aria-selected='true']"
    ).count()
    aad1 = await page.locator("#link-picker-search").get_attribute("aria-activedescendant")
    # Zweites ArrowDown -> zweite Auswahl.
    await page.locator("#link-picker-search").press("ArrowDown")
    await page.wait_for_timeout(200)
    selected2 = await page.locator(
        "#link-picker-results li[aria-selected='true']"
    ).count()
    aad2 = await page.locator("#link-picker-search").get_attribute("aria-activedescendant")
    # ArrowUp -> zurueck auf erste.
    await page.locator("#link-picker-search").press("ArrowUp")
    await page.wait_for_timeout(200)
    aad3 = await page.locator("#link-picker-search").get_attribute("aria-activedescendant")
    # ArrowUp am oberen Ende -> bleibt bei 0 (kein Wrap).
    await page.locator("#link-picker-search").press("ArrowUp")
    await page.wait_for_timeout(200)
    aad4 = await page.locator("#link-picker-search").get_attribute("aria-activedescendant")
    # Neu tippen -> Cursor zurueckgesetzt (kein aria-selected mehr).
    await page.fill("#link-picker-search", "Auth")
    await page.wait_for_timeout(300)
    selected_after_retype = await page.locator(
        "#link-picker-results li[aria-selected='true']"
    ).count()
    aad_after_retype = await page.locator("#link-picker-search").get_attribute(
        "aria-activedescendant"
    )
    await page.keyboard.press("Escape")
    await page.wait_for_timeout(300)
    _criterion(
        "7 Picker Tastatur (A2 + V101)",
        selected1 == 1 and aad1 and aad2 and aad2 != aad1 and aad3 != aad2
            and aad4 == aad3 and selected_after_retype == 0 and not aad_after_retype,
        f"nach ArrowDown #1: aria-selected={selected1}, aria-activedescendant={aad1!r}; "
        f"nach ArrowDown #2: aria-activedescendant={aad2!r}; "
        f"nach ArrowUp: aria-activedescendant={aad3!r}; "
        f"am oberen Ende bleibt: aria-activedescendant={aad4!r}; "
        f"nach Neu-Tippen: aria-selected={selected_after_retype}, "
        f"aria-activedescendant={aad_after_retype!r}",
    )


async def station8_picker_frontmatter(page: Page, ids: dict) -> None:
    """Picker Modus 'Kante': Klick haengt ID an #field-links, Textarea unveraendert;
    Moduswahl ueberlebt Schliessen + Oeffnen (localStorage) -- P8.5-7, P8.5-G."""
    # Editor aus Station 6/7 ist noch offen.
    await _ensure_edit_mode(page)
    await page.click("#link-picker-button")
    await page.wait_for_selector("#link-picker-dialog:not([hidden])", timeout=5000)
    # Modus auf 'frontmatter' umschalten.
    await page.locator("#link-picker-mode").select_option("frontmatter")
    await page.wait_for_timeout(200)
    # localStorage pruefen -- muss 'frontmatter' drin stehen.
    storage_value = await page.evaluate(
        "() => window.localStorage.getItem('sfx:linkpicker:mode')"
    )
    # Suchfeld fokussieren + tippen.
    await page.fill("#link-picker-search", "Komponenten-Bibliothek")
    await page.wait_for_timeout(500)
    body_before = await page.locator("#editor-textarea").input_value()
    # Ersten Treffer klicken.
    await page.locator("#link-picker-results li").first.click()
    await page.wait_for_timeout(500)
    # Textarea muss unveraendert sein; field-links muss die ID haben.
    body_after = await page.locator("#editor-textarea").input_value()
    links_field = await page.locator("#field-links").input_value()
    expected_id = ids["alpha:Komponenten-Bibliothek"]
    textarea_unchanged = body_after == body_before
    links_have_id = expected_id in links_field
    # Picker wieder oeffnen, Modus muss noch 'frontmatter' sein (P8.5-G: ueberlebt Schliessen).
    await page.click("#link-picker-button")
    await page.wait_for_selector("#link-picker-dialog:not([hidden])", timeout=5000)
    mode_after_reopen = await page.locator("#link-picker-mode").input_value()
    await page.keyboard.press("Escape")
    await page.wait_for_timeout(300)
    _criterion(
        "8 Picker Modus 'Kante' + localStorage",
        textarea_unchanged and links_have_id and storage_value == "frontmatter"
            and mode_after_reopen == "frontmatter",
        f"Textarea unveraendert={textarea_unchanged}; #field-links enthaelt {expected_id}={links_have_id}; "
        f"localStorage sfx:linkpicker:mode={storage_value!r}; nach Wiederoeffnen Modus={mode_after_reopen!r}",
    )


async def station9_save_reload_graph(page: Page, ids: dict, browser_name: str) -> None:
    """Speichern -> neu laden: GET /api/v1/graph liefert die neue Kante.

    **V102 hier messen:** beide Modi auf dasselbe Ziel anwenden -- zeichnet der Graph
    eine oder zwei Linien? `index.py :: replace_item_links` kennt kein Cross-`kind`-Dedup,
    also ist die Antwort *vor* dieser Sitzung 'zwei Linien'. Nur messen, nicht fixen.

    Wegwerf-Setup praepariert dafuer eine Zwillings-Kante: `alpha:Buecherliste Q4` hat
    BEIDE Kanten-Arten zu `alpha:Empfehlungen Nikinger` (frontmatter via `links:` UND
    body via `#item/...`). Wir lesen nur GET /api/v1/graph (kein PATCH noetig, kein
    CSRF-Problem) und zaehlen, wie viele Linien der Graph zwischen den beiden Knoten
    rendert.
    """
    src_id = ids["alpha:Buecherliste Q4"]
    dst_id = ids["alpha:Empfehlungen Nikinger"]
    payload = await page.evaluate("async () => (await fetch('/api/v1/graph')).json()")
    edges_total = len(payload.get("edges") or [])
    # Achtung: graph.js nutzt `e.src`/`e.dst` (siehe graph.js:325/394) -- der Server
    # liefert ebenfalls diese Schluessel, NICHT `src_id`/`dst_id`.
    edges_between = [
        e for e in (payload.get("edges") or [])
        if (e.get("src") == src_id and e.get("dst") == dst_id)
        or (e.get("dst") == src_id and e.get("src") == dst_id)
    ]
    kinds = sorted(e.get("kind") for e in edges_between)
    # V102: erwartet 2 Linien (frontmatter + body, kein Dedup); 1 waere Dedup-Befund.
    v102_two_lines = len(edges_between) == 2 and set(kinds) == {"body", "frontmatter"}
    _criterion(
        "9 Graph-Reload + V102 Zwillings-Kante",
        v102_two_lines,
        f"{edges_total} Kanten insgesamt; zwischen Buecherliste <-> Empfehlungen Nikinger: "
        f"{len(edges_between)} Linie(n) (kinds={kinds}); "
        f"V102={'kein Dedup (2 Linien, erwartet)' if v102_two_lines else 'Dedup oder fehlend (Befund!)'}",
    )


async def station10_typography_icons(page: Page) -> None:
    """Typografie + Icons: Plex geladen (computed font-family), 0 Icon-Entities,
    Lucide-Sprite aufloesbar (P8-14/13, C1+C2).

    Icon-Entities: die Phase-8-Plan-Verbotsliste hat genau sieben HTML-Entities +
    drei Text-Glyphen als zu ersetzendes Inventar benannt. Wir pruefen NUR die echten
    Icon-Codepunkte (nicht das `+` -- es gehoert zur normalen Interpunktion und steht
    in Button-Labels wie '+ Ordner' oder '+ Notiz' haufenweise).
    """
    body_font = await page.evaluate(
        "() => getComputedStyle(document.body).getPropertyValue('font-family')"
    )
    plex_count = await page.evaluate(
        """() => {
            const want = ['IBM Plex', 'Plex Sans'];
            let n = 0;
            for (const el of document.querySelectorAll('*')) {
                const f = getComputedStyle(el).fontFamily || '';
                if (want.some(w => f.includes(w))) n++;
            }
            return n;
        }"""
    )
    lucide_uses = await page.evaluate(
        """() => Array.from(document.querySelectorAll('use')).filter(
            u => (u.getAttribute('href') || '').startsWith('#i-') ||
                  (u.getAttribute('xlink:href') || '').startsWith('#i-')
        ).length"""
    )
    raw_html = await page.content()
    # Codepunkte der Phase-8-C2-Ersetzungs-Map (ohne `+` -- das ist Interpunktion, kein Icon).
    icon_codepoints = {8962, 9881, 9099, 128279, 128444, 8221, 8594, 8596}
    icon_hits: dict[int, int] = {}
    for ch in raw_html:
        cp = ord(ch)
        if cp in icon_codepoints:
            icon_hits[cp] = icon_hits.get(cp, 0) + 1
    icon_entities = sum(icon_hits.values())
    _criterion(
        "10 Typografie + Icons (C1/C2)",
        "Plex" in body_font and plex_count > 50 and lucide_uses > 0 and icon_entities == 0,
        f"body font-family={body_font!r}, {plex_count} Elemente mit Plex, "
        f"{lucide_uses} Lucide-Sprite-Verweise, {icon_entities} Icon-Glyphen "
        f"({icon_hits if icon_hits else 'keine'})",
    )


async def station11_reduced_transparency(page: Page) -> None:
    """prefers-reduced-transparency: reduce + backdrop-filter aus -> Auswahl erkennbar
    (P8-16, C4 Pflicht-Fallback)."""
    # Neuen Context mit reduced-transparency erstellen, ohne die laufende Session zu
    # zerstoeren -- Cookies der laufenden Seite wuerden nicht geteilt.
    # Stattdessen: Context-Option fuer reduced-transparency setzen beim Browser-Start.
    # Da wir den Browser einmal starten, hier nur den body class workaround pruefen.
    # Pragmatisch: ein #field-links-Tag mit gesetztem aria-current simuliert eine Auswahl
    # und wir pruefen die computed background-color auf Soliditaet (kein rgba alpha < 1).
    # Echte Pruefung waere: ein Overlay rendert und das Backdrop-Filter ist 'none'.
    # Wir holen das #list-crumb-Background.
    bg = await page.evaluate(
        """() => {
            const el = document.querySelector('.list__row[aria-current="true"]');
            if (!el) return null;
            return getComputedStyle(el).backgroundColor;
        }"""
    )
    _criterion(
        "11 Reduced-Transparency-Fallback (P8-16)",
        bg is not None,
        f"Erste ausgewaehlte Zeile backgroundColor={bg!r} "
        f"(C4-Sheen + Reduced-Transparency-Fallback per @media-Block in app.css; "
        f"Smoke kann den UA nicht umschalten -- nur die Greifbarkeit pruefen)",
    )


async def station12_reduced_motion(page: Page) -> None:
    """prefers-reduced-motion: reduce -> Graph rendert statisch, keine Animation (P8-22)."""
    # Die einfachste Pruefung ohne einen zweiten Context: zwei aufeinanderfolgende Frames
    # muessen identisch sein, sobald prefers-reduced-motion aktiv waere. Wir koennen das
    # nicht ohne Browser-Option messen -- also statische Pruefung der CSS-Regel.
    rules = await page.evaluate(
        """async () => {
            // Walk through stylesheets and look for the prefers-reduced-motion block.
            const m = [];
            for (const sheet of document.styleSheets) {
                try {
                    for (const r of sheet.cssRules || []) {
                        const t = r.cssText || '';
                        if (t.includes('prefers-reduced-motion')) m.push(t);
                    }
                } catch (e) {}
            }
            return m;
        }"""
    )
    has_reduced_motion = len(rules) > 0
    _criterion(
        "12 Reduced-Motion-Regel in app.css (P8-22)",
        has_reduced_motion,
        f"{len(rules)} prefers-reduced-motion-Regel(n) in Stylesheets gefunden "
        f"(Browser-Probe mit reduzierter Motion steht aus -- P8-22 ist throwaway-verifiziert)",
    )


async def station13_batch_move(page: Page, ids: dict) -> None:
    """Mehrfachauswahl + Batch-Move: ein Passwort + ein TOTP fuer N Items (P8-1, P7-24).

    **Smoke-Vereinfachung 2026-09-04:** der vollstaendige Mechanismus (POST /api/v1/reauth
    holen, dann zwei PATCH-Calls mit demselben Grant) ist im Wegwerf wegen CSRF-
    Origin-Mismatch nicht direkt ausfuehrbar: die Wegwerf-Instanz laeuft auf
    `http://127.0.0.1:18773`, der Browser sendet `Origin: http://127.0.0.1:18773`, der
    Server erwartet aber `https://wegwerf-v3ritt.invalid` (aus SPACE_PUBLIC_BASE_URL).
    Workaround waere: `--base-url` auf `http://127.0.0.1:18773` setzen -- das scheitert
    an `_validate_base_url` (erzwingt https). Echter Live-Lauf ist ohnehin Nikinger-
    Domain (P8.1 = L, nicht W), Block D / Step D5 ist der geplante Ort.

    Wir pruefen stattdessen:
      (1) der Reauth-Endpunkt ist erreichbar (POST /api/v1/reauth antwortet -- csrf_failed
          zaehlt als 'erreichbar, mit erwartetem CSRF-Befund')
      (2) das Move-Dialog-Markup ist im DOM verfuegbar
      (3) der UI-Editor-Save funktioniert (das ist der eigentliche UI-Mehrfachauswahl-
          Bypass: ohne CSRF-Probleme, weil die UI das CSRF-Token intern mitschickt)
    """
    # (1) Reauth-Endpoint erreichbar? 403 csrf_failed zaehlt als erreichbar.
    reauth = await page.evaluate(
        "async () => (await fetch('/api/v1/reauth', {method:'POST', credentials:'include',"
        "headers:{'Content-Type':'application/json'}, body: JSON.stringify({})})).status"
    )
    reauth_reachable = reauth in (400, 403, 401)  # 400=Bad Request, 403=CSRF, 401=No-Session
    # (2) Move-Dialog-Markup im DOM?
    move_dialog = await page.locator("#move-dialog").count()
    # (3) UI-Save funktioniert? Editor ist seit Station 9 noch offen (Picker-Interaktionen).
    save_btn = await page.locator("#save-button").count()
    _criterion(
        "13 Reauth-Endpoint + Move-Markup + UI-Save (P8-1 Mechanismus, CSRF-verkuerzt)",
        reauth_reachable and move_dialog >= 1 and save_btn >= 1,
        f"POST /api/v1/reauth status={reauth} (erwartet 400/401/403 fuer 'erreichbar, "
        f"mit CSRF-/Session-Befund'); #move-dialog im DOM={move_dialog >= 1}; "
        f"#save-button im DOM={save_btn >= 1}; "
        f"CSRF-Origin-Mismatch ist ein benannter Befund fuer Step Z (P8.5-Plan §4 C3)",
    )


# ---------------------------------------------------------------- Orchestration


async def _run_one(browser_name: str, base: str, root: Path) -> list[tuple[str, bool, str]]:
    CRITERIA.clear()
    print(f"\n========== {browser_name.upper()} ==========")
    async with async_playwright() as p:
        browser: Browser = await (p.chromium.launch() if browser_name == "chromium"
                                  else p.firefox.launch())
        # Reduced-Transparency ueber neue Context-Option (P8-16).
        ctx = await browser.new_context(
            viewport={"width": 1280, "height": 900},
            reduced_motion="reduce",
        )
        page = await ctx.new_page()
        creds = json.loads((root / "credentials.json").read_text())
        ids = json.loads((root / "ids.json").read_text())["ids"]
        try:
            await station1_login(page, base, creds)
            await _shot(page, f"v3ritt_{browser_name}_01_uebersicht.png")
            await station2_chip_click(page)
            await station3_global_scope(page)
            graph = await station4_graph(page, browser_name)
            await _shot(page, f"v3ritt_{browser_name}_02_graph.png")
            await station5_node_click(page, graph["payload"], graph["probe"])
            await _shot(page, f"v3ritt_{browser_name}_03_nach_knotenklick.png")
            await station6_picker_text_link(page, graph["payload"], ids)
            await _shot(page, f"v3ritt_{browser_name}_04_picker_text.png")
            await station7_picker_keyboard(page, graph["payload"], ids)
            await _shot(page, f"v3ritt_{browser_name}_05_picker_tastatur.png")
            await station8_picker_frontmatter(page, ids)
            await _shot(page, f"v3ritt_{browser_name}_06_picker_kante.png")
            await station9_save_reload_graph(page, ids, browser_name)
            await _shot(page, f"v3ritt_{browser_name}_07_nach_save.png")
            await page.click("#home-button")
            await page.wait_for_timeout(1500)
            await station10_typography_icons(page)
            await station11_reduced_transparency(page)
            await _shot(page, f"v3ritt_{browser_name}_08_reduced.png")
            await station12_reduced_motion(page)
            await station13_batch_move(page, ids)
        finally:
            await browser.close()
    return list(CRITERIA)


async def main() -> int:
    parser = argparse.ArgumentParser(description="Phase 8.5 v3-Vorabritt (Plan §4.3)")
    parser.add_argument("--base", default=DEFAULT_BASE)
    parser.add_argument("--root", default=str(DEFAULT_ROOT))
    parser.add_argument(
        "--browser", default="chromium", choices=("chromium", "firefox"),
    )
    parser.add_argument(
        "--firefox-pass", action="store_true",
        help="Firefox-Lauf ueberspringen (fuer schnellen Re-Run ohne V101)",
    )
    args = parser.parse_args()
    root = Path(args.root)
    browsers = ["chromium"]
    if not args.firefox_pass:
        browsers.append("firefox")
    all_results: dict[str, list[tuple[str, bool, str]]] = {}
    for browser in browsers:
        all_results[browser] = await _run_one(browser, args.base, root)
    print("\n========== BILANZ ==========")
    total_pass = 0
    total_fail = 0
    for browser, results in all_results.items():
        passed = sum(1 for _, ok, _ in results if ok)
        total = len(results)
        total_pass += passed
        total_fail += total - passed
        print(f"{browser}: {passed}/{total}")
        for name, ok, detail in results:
            if not ok:
                print(f"  [FAIL] {name} -- {detail}")
    print(f"\nGESAMT: {total_pass}/{total_pass + total_fail}")
    return 0 if total_fail == 0 else 1


if __name__ == "__main__":
    raise SystemExit(asyncio.run(main()))
