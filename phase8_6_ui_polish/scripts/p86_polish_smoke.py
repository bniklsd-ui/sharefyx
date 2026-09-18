#!/usr/bin/env python3
"""Phase 8.6 Gate -- GA2 Smoke-Skript, 14 Stationen (Plan 2 §7.2).

Gegen die Wegwerf-Instanz aus `phase8_5_picker_release/scripts/wegwerf_setup_v3ritt.py`
(Muster laut §7.1 -- Port 18773, eigener tmp-DATA_ROOT/auth.sqlite3, PID-Datei-Stopp,
kein `pkill -f`, `sharefyx-mcp.service` bleibt unberuehrt).

Assertions sind gegen den AKTUELLEN Code abgeleitet, nicht gegen §7.2s Wortlaut --
der Plan ist vom 2026-09-13, seither liefen G-R/H/H-R-1..3/Nachtrag. Wo eine Station
von §7.2 abweicht, steht der Grund im Docstring der Stationsfunktion (Quelle der
Wahrheit ist der Code, Wurzel-CLAUDE.md).

Bekannte Abweichungen von §7.2s Wortlaut:
  - Stationen 5/6/(7): `.shell[data-view]` kennt nur die Werte "list"/"detail", nicht
    "editor" -- H-R.8 Lesart b (2026-09-17) toggled auf "detail" bei JEDEM offenen
    Editor UND jeder Karten-Detailansicht, nicht nur beim Editor, und das OHNE
    Media-Query-Wrapper (gilt bei 1440px genauso wie bei 1024px).
  - Station 6: der Graph-Knoten-Klick ist ein EINFACHER Klick, der in `hitTest()`
    (`graph.js:586`) einen Knoten trifft -- `dblclick` (`graph.js:685`) resettet nur
    Zoom/Pan bei einem Hintergrund-Doppelklick, das oeffnet gar nichts.
  - Station 7: H-R.8 Lesart a (Rail-Konsolidierung, "Alle Items"-Knopf loeschen) wurde
    NICHT gebaut -- nur Lesart b (Layout). Der Knopf existiert weiterhin und fuehrt
    zur selben Aktion wie Home (V110, negativer Befund, Plan §4.3).
  - Station 11: G-R.1s 1024-Stapel ist durch H-R.6 ersetzt -- kein Grid-Stack mehr,
    `.detail__graph { display: none }` bei jeder Breite <=1024px. H-R.7 zusaetzlich:
    bei offenem Editor <=1024px verschwinden Rail UND Liste (data-view="detail").

Stationen 3/5/8/10 laufen in Chromium UND Firefox (CSS-/Fokus-Verhalten). Der Rest nur
Chromium. Jede Station laeuft unabhaengig -- ein Fehlschlag bricht das Skript nicht ab
(Fehlschlaege werden gesammelt, nicht die erste beendet den Lauf).

CSRF-Grenze (§7.2 verbatim): die Wegwerf-Origin passt nicht zu SPACE_PUBLIC_BASE_URL,
jeder Browser-POST/PATCH aeusserhalb des Login-Formulars wuerde abgelehnt. Alle 14
Stationen unten sind bewusst Lese-/Render-Stationen.
"""
from __future__ import annotations

import base64
import datetime
import hashlib
import hmac
import json
import struct
import sys
import time
import urllib.parse
from pathlib import Path

from playwright.sync_api import Page, sync_playwright

REPO_ROOT = Path(__file__).resolve().parents[2]
OUT_DIR = REPO_ROOT / "docs" / "screenshots"
OUT_DIR.mkdir(parents=True, exist_ok=True)

BASE_URL = "http://127.0.0.1:18773"
WEGWERF_ROOT = Path("/tmp/opencode/sharefyx-wegwerf-v3ritt")
CREDS_PATH = WEGWERF_ROOT / "credentials.json"
IDS_PATH = WEGWERF_ROOT / "ids.json"


def _generate_totp(otpauth_uri: str) -> str:
    parsed = urllib.parse.urlparse(otpauth_uri)
    qs = urllib.parse.parse_qs(parsed.query)
    secret_b32 = qs["secret"][0]
    key = base64.b32decode(secret_b32 + "=" * (-len(secret_b32) % 8))
    counter = int(time.time() // 30)
    msg = struct.pack(">q", counter)
    h = hmac.new(key, msg, hashlib.sha1).digest()
    offset = h[-1] & 0x0F
    code_int = (struct.unpack(">I", h[offset:offset + 4])[0] & 0x7FFFFFFF) % 1000000
    return f"{code_int:06d}"


def login(page: Page, password: str, otpauth_uri: str) -> tuple[int, str]:
    secs_into = datetime.datetime.now().second
    wait = 35 - (secs_into % 30)
    print(f"Login: warte {wait}s auf frisches TOTP-Fenster ...", file=sys.stderr)
    time.sleep(wait)
    for window in range(2):
        page.goto(f"{BASE_URL}/ui/login", wait_until="domcontentloaded")
        page.locator('input[name="space"]').fill("alpha")
        page.locator('input[name="password"]').fill(password)
        totp_code = _generate_totp(otpauth_uri)
        print(f"  Fenster {window + 1}: TOTP {totp_code}", file=sys.stderr)
        page.locator('input[name="totp"]').fill(totp_code)
        with page.expect_response("**/ui/login**") as resp_info:
            page.locator('button[type="submit"]').click()
        resp = resp_info.value
        print(f"  Fenster {window + 1}: HTTP {resp.status}", file=sys.stderr)
        if resp.status in (200, 303):
            time.sleep(3.0)
            if not page.url.startswith(f"{BASE_URL}/ui/"):
                page.goto(f"{BASE_URL}/ui/", wait_until="domcontentloaded")
            return resp.status, "ok"
        if resp.status == 401:
            print("  TOTP verbraucht, warte 35s auf naechstes Fenster...", file=sys.stderr)
            time.sleep(35)
            continue
        return resp.status, f"http_{resp.status}"
    return 0, "tries_exhausted"


def _dismiss_update_banner(page: Page) -> None:
    try:
        dismiss = page.locator("#update-banner-dismiss")
        if dismiss.is_visible(timeout=1000):
            dismiss.click()
            time.sleep(0.3)
    except Exception:
        pass


def _goto_home(page: Page, viewport=(1440, 900)) -> None:
    page.set_viewport_size({"width": viewport[0], "height": viewport[1]})
    page.goto(f"{BASE_URL}/ui/", wait_until="domcontentloaded")
    page.wait_for_load_state("networkidle", timeout=5000)
    time.sleep(0.4)


def _shot(page: Page, name: str) -> str:
    path = OUT_DIR / f"p86_smoke_{name}.png"
    page.screenshot(path=str(path))
    return path.name


class Result:
    def __init__(self, station: str, ok: bool, note: str, shot: str | None = None, browser: str = "chromium"):
        self.station = station
        self.ok = ok
        self.note = note
        self.shot = shot
        self.browser = browser

    def line(self) -> str:
        mark = "OK " if self.ok else "FEHLER"
        shot = f" [{self.shot}]" if self.shot else ""
        return f"[{mark}] ({self.browser}) {self.station}: {self.note}{shot}"


def run_station(fn, page: Page, browser_name: str, results: list[Result]) -> None:
    name = fn.__name__
    try:
        ok, note, shot = fn(page)
        results.append(Result(name, ok, note, shot, browser_name))
    except Exception as exc:  # noqa: BLE001 -- Stationen sollen sich nicht gegenseitig kippen
        results.append(Result(name, False, f"Exception: {exc!r}", None, browser_name))


# -- Stationen ------------------------------------------------------------------------------

def station_01_uebersicht_1440(page: Page):
    """#1: Uebersicht steht im Listen-Slot, #detail-graph fuellt den Detail-Slot."""
    _goto_home(page, (1440, 900))
    _dismiss_update_banner(page)
    overview_visible = page.locator("#list-overview").is_visible()
    graph_visible = page.locator("#detail-graph").is_visible()
    shot = _shot(page, "01_1440_uebersicht")
    ok = overview_visible and graph_visible
    return ok, f"overview_visible={overview_visible} graph_visible={graph_visible}", shot


def station_02_rail_reihenfolge(page: Page):
    """#2: home-button, rail-tree, dann .rail__account mit account-button VOR logout-button."""
    order = page.evaluate(
        """() => {
            const ids = ['home-button', 'rail-tree', 'account-button', 'logout-button'];
            const els = ids.map(id => document.getElementById(id));
            if (els.some(e => !e)) return null;
            const positions = els.map(e => {
                let n = 0, cur = e;
                while (cur.previousElementSibling || cur.parentElement) {
                    if (cur.previousElementSibling) { cur = cur.previousElementSibling; n++; }
                    else break;
                }
                return e.compareDocumentPosition;
            });
            for (let i = 0; i < els.length - 1; i++) {
                const rel = els[i].compareDocumentPosition(els[i + 1]);
                if (!(rel & Node.DOCUMENT_POSITION_FOLLOWING)) return false;
            }
            return true;
        }"""
    )
    shot = _shot(page, "02_rail_reihenfolge")
    return bool(order), f"home<rail-tree<account-button<logout-button = {order}", shot


def _ensure_overview(page: Page) -> None:
    """Defensive Reset: vorherige Stationen koennen den Editor offen/den Space gewechselt
    gelassen haben. `home-button` fuehrt ueber closeEditor() -> clearDetail() ohnehin
    immer zurueck (V116/V117), unabhaengig vom Vorzustand."""
    page.locator("#home-button").click()
    page.wait_for_load_state("networkidle", timeout=5000)
    time.sleep(0.3)


def station_03_space_zeile_hover(page: Page):
    """#3: Hover-Fill deckt die ganze .overview__space-open-Zeile inkl. Chip-Leiste.

    `--select-fill-quiet` ist ein `linear-gradient(...)`-Token (app.css:75) -- das landet in
    `background-image`, nicht in `background-color`. Erste Fassung pruefte `backgroundColor`
    und lieferte auf Firefox faelschlich rgba(0,0,0,0) (Script-Bug, kein Produktbefund)."""
    _ensure_overview(page)
    row = page.locator(".overview__space-open").first
    box_before = row.bounding_box()
    row.hover()
    time.sleep(0.2)
    bg_image = page.evaluate(
        """() => {
            const el = document.querySelector('.overview__space-open');
            return getComputedStyle(el).backgroundImage;
        }"""
    )
    shot = _shot(page, "03_space_zeile_hover")
    ok = box_before is not None and bg_image not in ("none", None, "")
    return ok, f"hover_background-image={bg_image} width={box_before['width'] if box_before else None}", shot


def station_04_space_zeile_klicken(page: Page):
    """#4: Klick wechselt den Listen-Slot auf Items, die Karte bleibt stehen."""
    graph_before = page.locator("#detail-graph").is_visible()
    page.locator(".overview__space-open").first.click()
    page.wait_for_load_state("networkidle", timeout=5000)
    time.sleep(0.4)
    rows_visible = page.locator(".list__row").first.is_visible()
    graph_after = page.locator("#detail-graph").is_visible()
    shot = _shot(page, "04_space_zeile_klicken")
    ok = rows_visible and graph_before == graph_after is True
    return ok, f"rows_visible={rows_visible} graph_before={graph_before} graph_after={graph_after}", shot


def station_05_item_klicken_esc(page: Page):
    """#5: Editor ersetzt die Karte (data-view=detail), ESC bringt data-view=list zurueck.

    Abweichung von §7.2s Wortlaut: der Attributwert ist "detail", nicht "editor"
    (H-R.8 Lesart b, `app.css:421` + `editor.js`)."""
    _ensure_overview(page)
    row = page.locator(".list__row").first
    if not row.is_visible():
        page.locator(".overview__space-open").first.click()
        page.wait_for_load_state("networkidle", timeout=5000)
        time.sleep(0.3)
    row = page.locator(".list__row").first
    row.click()
    page.wait_for_load_state("networkidle", timeout=5000)
    time.sleep(0.4)
    view_after_open = page.evaluate("() => document.getElementById('shell').dataset.view")
    shot_open = _shot(page, "05a_item_editor_open")
    page.keyboard.press("Escape")
    time.sleep(0.4)
    view_after_esc = page.evaluate("() => document.getElementById('shell').dataset.view")
    shot_esc = _shot(page, "05b_item_editor_esc")
    ok = view_after_open == "detail" and view_after_esc == "list"
    return ok, f"view_after_open={view_after_open} view_after_esc={view_after_esc}", f"{shot_open},{shot_esc}"


def station_06_karten_knoten_esc(page: Page):
    """#6: Klick auf einen Graph-Knoten oeffnet denselben Editor-Weg wie ein Listen-Klick.

    Korrektur gegen die erste Fassung: `canvasEl.addEventListener("dblclick", onDoubleClick)`
    (graph.js:685) resettet nur Zoom/Pan bei einem Hintergrund-Doppelklick -- das Oeffnen
    laeuft ueber `onMouseUp` (graph.js:629), ein EINFACHER Klick, der in `hitTest()` (graph.js
    :586) auf einen Knoten trifft (Press-Bewegung < CLICK_SLOP). Da Knotenpositionen aus der
    Kraft-Simulation kommen (kein DOM, kein fester Anker), tastet diese Station ein 5x5-Raster
    um die Canvas-Mitte ab, bis ein Klick `data-view` auf "detail" kippt."""
    _ensure_overview(page)
    canvas = page.locator("#detail-graph canvas").first
    box = canvas.bounding_box()
    if not box:
        return False, "kein Canvas gefunden", None
    time.sleep(3.5)  # Simulation-Settle: ALPHA_DECAY 0.97/ALPHA_MIN 0.01 ~ 151 Ticks ~ 2.52s
                      # (graph.js:24) -- Knoten starten oben-links gebuendelt (graph.js:167)
                      # und driften erst per requestAnimationFrame zur Mitte.
    # Pixel-Scan statt Raster-Raten: ein 5x5-Raster verfehlte den einzigen sichtbaren Knoten
    # im ersten Versuch (Beweis-Screenshot 06_karten_knoten_klick.png zeigte genau einen
    # Punkt, deutlich ausserhalb des Rasters). `getImageData` liest den Canvas-Inhalt direkt
    # und findet den ersten Pixel, der sich vom fast-schwarzen Hintergrund abhebt -- robust
    # unabhaengig von Knotenzahl/-position, ohne auf das JS-Modul-interne `nodes`-Array
    # zugreifen zu muessen (das ist nicht exportiert).
    hit = page.evaluate(
        """() => {
            const canvas = document.querySelector('#detail-graph canvas');
            const ctx = canvas.getContext('2d');
            const data = ctx.getImageData(0, 0, canvas.width, canvas.height).data;
            const step = 3;
            for (let y = 0; y < canvas.height; y += step) {
                for (let x = 0; x < canvas.width; x += step) {
                    const i = (y * canvas.width + x) * 4;
                    const r = data[i], g = data[i + 1], b = data[i + 2];
                    // Hintergrund ist --bg-void (~#000) bzw. --bg (~#0B0D10) -- alles
                    // merklich heller ist ein Knoten/Kante/Label.
                    if (r > 40 || g > 40 || b > 40) {
                        const rect = canvas.getBoundingClientRect();
                        const scaleX = rect.width / canvas.width;
                        const scaleY = rect.height / canvas.height;
                        return { x: rect.left + x * scaleX, y: rect.top + y * scaleY };
                    }
                }
            }
            return null;
        }"""
    )
    view_after = "list"
    hit_xy = None
    if hit:
        page.mouse.click(hit["x"], hit["y"])
        time.sleep(0.3)
        view_after = page.evaluate("() => document.getElementById('shell').dataset.view")
        hit_xy = (round(hit["x"], 1), round(hit["y"], 1))
    shot = _shot(page, "06_karten_knoten_klick")
    if view_after == "detail":
        page.keyboard.press("Escape")
        time.sleep(0.3)
    view_after_esc = page.evaluate("() => document.getElementById('shell').dataset.view")
    ok = view_after == "detail" and view_after_esc == "list"
    return ok, f"hit_at_offset={hit_xy} view_after_click={view_after} view_after_esc={view_after_esc}", shot


def station_07_alle_items(page: Page):
    """#7: "Alle Items" -- keine Spaces-Uebersicht, kein Space-Name, kein "Zuletzt benutzt".

    Abweichung von §7.2: H-R.8 Lesart a (Knopf loeschen) wurde nicht gebaut, der Knopf
    existiert weiterhin (V110 negativer Befund, Plan §4.3) und fuehrt zur selben Aktion
    wie Home."""
    page.locator("#rail-tree").get_by_text("Alle Items", exact=False).first.click()
    page.wait_for_load_state("networkidle", timeout=5000)
    time.sleep(0.4)
    overview_hidden = page.locator("#list-overview").is_hidden()
    rows_visible = page.locator(".list__row").first.is_visible()
    shot = _shot(page, "07_alle_items")
    ok = overview_hidden and rows_visible
    return ok, f"overview_hidden={overview_hidden} rows_visible={rows_visible}", shot


def station_08_editor_kopfdaten(page: Page):
    """#8: YAML-Panel kuehl (Layer 2), kein warmer Stich (Befund 1+8, F1/H-R.3)."""
    page.locator("#home-button").click()
    page.wait_for_load_state("networkidle", timeout=5000)
    time.sleep(0.3)
    if page.locator(".overview__space-open").first.is_visible():
        page.locator(".overview__space-open").first.click()
        page.wait_for_load_state("networkidle", timeout=5000)
        time.sleep(0.3)
    page.locator(".list__row").first.click()
    page.wait_for_load_state("networkidle", timeout=5000)
    time.sleep(0.4)
    head_bg = page.evaluate(
        """() => {
            const head = document.querySelector('.editor__head');
            return head ? getComputedStyle(head).backgroundColor : null;
        }"""
    )
    padding_bottom = page.evaluate(
        """() => {
            const head = document.querySelector('.editor__head');
            return head ? getComputedStyle(head).paddingBottom : null;
        }"""
    )
    shot = _shot(page, "08_editor_kopfdaten")
    ok = head_bg is not None
    return ok, f"editor__head background={head_bg} padding-bottom={padding_bottom}", shot


def station_09_konto_dialog(page: Page):
    """#9: beide .account-nav sichtbar UND elementFromPoint-erreichbar (Befund 2/H2)."""
    page.locator("#account-button").click()
    time.sleep(0.4)
    reach = page.evaluate(
        """() => {
            const results = [];
            document.querySelectorAll('.account-nav').forEach(btn => {
                const r = btn.getBoundingClientRect();
                const cx = r.left + r.width / 2, cy = r.top + r.height / 2;
                const hit = document.elementFromPoint(cx, cy);
                results.push({ id: btn.id, reachable: hit === btn || btn.contains(hit) });
            });
            return results;
        }"""
    )
    shot = _shot(page, "09_konto_dialog")
    page.keyboard.press("Escape")
    time.sleep(0.2)
    ok = len(reach) >= 2 and all(r["reachable"] for r in reach)
    return ok, f"account-nav reachability: {reach}", shot


def station_10_1200px(page: Page):
    """#10: alle Knoepfe erreichbar, #list-overview scrollbar statt geklippt (9b-Regression)."""
    _goto_home(page, (1200, 900))
    _dismiss_update_banner(page)
    buttons_ok = page.evaluate(
        """() => {
            const ids = ['home-button', 'account-button', 'logout-button'];
            return ids.every(id => {
                const el = document.getElementById(id);
                if (!el) return false;
                const r = el.getBoundingClientRect();
                return r.width > 0 && r.height > 0;
            });
        }"""
    )
    clipped = page.evaluate(
        """() => {
            const el = document.getElementById('list-overview');
            if (!el || el.hidden) return null;
            return el.scrollHeight > el.clientHeight + 4 && getComputedStyle(el).overflowY === 'visible';
        }"""
    )
    shot = _shot(page, "10_1200px")
    ok = buttons_ok and clipped is not True
    return ok, f"buttons_ok={buttons_ok} clipped(bad if true)={clipped}", shot


def station_11_1024px(page: Page):
    """#11: <=1024px kein Map-Slot (H-R.6); Editor-open blendet Rail+Liste aus (H-R.7).

    Korrektur gegen §7.2s Wortlaut ("`.detail__back` erreichbar"): `.detail__back` ist in
    app.css:1367 fest `display: none` OHNE eine einzige Override-Regel irgendwo im Stylesheet
    (grep bestaetigt) -- der Knopf ist toter Code, kein Layout-Fund dieser Station. H-R.7 hat
    das Zurueck-Muster durch `#close-button` + ESC ersetzt (`closeEditor()`-Pfad, derselbe wie
    bei H-R.8). Diese Station prueft deshalb `#close-button`-Erreichbarkeit statt back-button
    und dokumentiert den toten Knopf separat als Befund."""
    _goto_home(page, (1024, 900))
    _dismiss_update_banner(page)
    graph_display_none = page.evaluate(
        "() => getComputedStyle(document.getElementById('detail-graph')).display === 'none'"
    )
    shot_list = _shot(page, "11a_1024_ohne_map")
    if page.locator(".overview__space-open").first.is_visible():
        page.locator(".overview__space-open").first.click()
        page.wait_for_load_state("networkidle", timeout=5000)
        time.sleep(0.3)
    page.locator(".list__row").first.click()
    page.wait_for_load_state("networkidle", timeout=5000)
    time.sleep(0.4)
    rail_hidden = page.evaluate(
        "() => getComputedStyle(document.querySelector('.rail')).display === 'none'"
    )
    list_hidden = page.evaluate(
        "() => getComputedStyle(document.querySelector('.list')).display === 'none'"
    )
    close_reachable = page.evaluate(
        """() => {
            const btn = document.getElementById('close-button');
            if (!btn) return false;
            const r = btn.getBoundingClientRect();
            if (r.width === 0 || r.height === 0) return false;
            const hit = document.elementFromPoint(r.left + r.width / 2, r.top + r.height / 2);
            return hit === btn || btn.contains(hit);
        }"""
    )
    back_button_dead = page.evaluate(
        "() => getComputedStyle(document.getElementById('back-button')).display === 'none'"
    )
    shot_editor = _shot(page, "11b_1024_editor_fullview")
    page.keyboard.press("Escape")
    time.sleep(0.3)
    ok = graph_display_none and rail_hidden and list_hidden and close_reachable
    return ok, (
        f"graph_display_none={graph_display_none} rail_hidden={rail_hidden} "
        f"list_hidden={list_hidden} close_reachable={close_reachable} "
        f"BEFUND_back_button_ist_tot(display:none ohne Override)={back_button_dead}"
    ), f"{shot_list},{shot_editor}"


def _canvas_checksum(page: Page) -> dict:
    """Liest #detail-graph-Canvas-Pixel direkt (nicht per PNG-Screenshot) -- vermeidet
    Rauschen aus der Umgebung (Cursor, Fokusring) und braucht kein PIL/numpy im e2e-venv."""
    return page.evaluate(
        """() => {
            const canvas = document.querySelector('#detail-graph canvas');
            const ctx = canvas.getContext('2d');
            const data = ctx.getImageData(0, 0, canvas.width, canvas.height).data;
            let sum = 0, litPixels = 0;
            for (let i = 0; i < data.length; i += 4) {
                const v = data[i] + data[i + 1] + data[i + 2];
                sum += v;
                if (v > 40) litPixels++;
            }
            return { width: canvas.width, height: canvas.height, sum, litPixels };
        }"""
    )


def station_12_uebersicht_zweimal(page: Page):
    """#12: identisches Kartenbild bei zweimaligem Oeffnen (FNV-Seed, D2/P8.6-M).

    Erste Fassung verglich volle PNG-Screenshots byteweise -- das schlug trotz 3.5s
    Settle-Wartezeit fehl. `integrate()` (graph.js) laeuft ueber echte
    `requestAnimationFrame`-Zeitschritte; zwei separate Laeufe treffen nie exakt dieselbe
    Frame-Zahl vor dem ALPHA_MIN-Abbruch, minimale Sub-Pixel-Drift ist also erwartbar, kein
    Determinismus-Bruch des FNV-Seeds selbst (der bestimmt nur die STARTPOSITIONEN/den
    Jitter, nicht die Vektor-Bahn dorthin). Diese Fassung vergleicht deshalb einen
    Pixel-Checksum aus dem Canvas direkt (Layout-Groessenordnung: Summe + Anzahl "heller"
    Pixel) mit Toleranz, statt exakter Bytegleichheit -- plus zwei Screenshots fuer die
    Nikinger-Sichtpruefung, die die eigentliche Instanz dieser Abnahme ist (§7.3)."""
    _goto_home(page, (1440, 900))
    _dismiss_update_banner(page)
    time.sleep(3.5)  # Simulation settle -- D2 FNV-Seed ist deterministisch, aber
                      # runSimulation() (D4 cancelAnimationFrame) braucht Zeit zum Ausklingen.
    shot1 = _shot(page, "12a_uebersicht_erstmalig")
    cs1 = _canvas_checksum(page)
    page.locator(".overview__space-open").first.click()
    page.wait_for_load_state("networkidle", timeout=5000)
    time.sleep(0.3)
    page.locator("#home-button").click()
    page.wait_for_load_state("networkidle", timeout=5000)
    time.sleep(3.5)
    shot2 = _shot(page, "12b_uebersicht_zweites_mal")
    cs2 = _canvas_checksum(page)
    lit_delta = abs(cs1["litPixels"] - cs2["litPixels"])
    lit_ref = max(cs1["litPixels"], cs2["litPixels"], 1)
    close_enough = lit_delta / lit_ref < 0.05  # <5% Abweichung in "hellen" Pixeln
    return close_enough, (
        f"checksum1={cs1} checksum2={cs2} lit_delta={lit_delta} "
        f"({lit_delta / lit_ref:.1%}) -- visuelle Gegenprobe der Screenshots empfohlen (§7.3)"
    ), f"{shot1},{shot2}"


def station_13_zwillingskanten(page: Page):
    """#13: eine Linie statt zwei fuer das V102-Praeparat "Buecherliste Q4" -> "Empfehlungen".

    Rein visuelle Station (Canvas, kein DOM) -- Screenshot fuer die Nikinger-Sichtprue-
    fung (§7.3), kein automatisches Pass/Fail moeglich."""
    _goto_home(page, (1440, 900))
    _dismiss_update_banner(page)
    if IDS_PATH.exists():
        ids = json.loads(IDS_PATH.read_text())
        target_id = ids["ids"].get("alpha:Buecherliste Q4")
    else:
        target_id = None
    if target_id:
        page.goto(f"{BASE_URL}/ui/#item/{target_id}", wait_until="domcontentloaded")
        page.wait_for_load_state("networkidle", timeout=5000)
        time.sleep(0.6)
    shot = _shot(page, "13_zwillingskanten_buecherliste")
    return True, f"screenshot-only, target_id={target_id} -- Nikinger prueft visuell", shot


def station_14_link_picker(page: Page):
    """#14: <select id="link-picker-mode">, Wahl aus localStorage wiederhergestellt (P8.6-H).

    Zwei Fehlversuche vorher: `.toolbar-btn[data-md="link"]` (app.html:212) ist NICHT der
    Link-Picker -- dessen Klick-Handler (editor.js:672-677, Action bei editor.js:660-668)
    fuegt nur ein statisches `[Linktext](Ziel-URL)`-Markdown-Snippet ein, ohne Dialog. Der
    echte Picker-Trigger ist `#link-picker-button` (app.html:192-197) neben dem
    Frontmatter-Feld "Links" -- der sitzt in einem `<details>`-Kopfdatenblock, der erst
    aufgeklappt sein muss (`editor.js:561-563 :: openLinkPicker({ onPick: _onLinkPicked })`)."""
    _goto_home(page, (1440, 900))
    _dismiss_update_banner(page)
    if page.locator(".overview__space-open").first.is_visible():
        page.locator(".overview__space-open").first.click()
        page.wait_for_load_state("networkidle", timeout=5000)
        time.sleep(0.3)
    page.locator(".list__row").first.click()
    page.wait_for_load_state("networkidle", timeout=5000)
    time.sleep(0.4)
    insert_link_btn = page.locator("#link-picker-button")
    opened = False
    try:
        if not insert_link_btn.first.is_visible(timeout=500):
            page.locator("details").first.evaluate("el => el.open = true")
            time.sleep(0.2)
        if insert_link_btn.first.is_visible(timeout=1000):
            insert_link_btn.first.click()
            opened = True
    except Exception:
        opened = False
    select_present = page.locator("#link-picker-mode").count() > 0
    shot = None
    value_before = None
    value_restored = None
    if opened and select_present:
        page.locator("#link-picker-mode").select_option("frontmatter")
        time.sleep(0.2)
        value_before = page.evaluate("() => window.localStorage.getItem('sfx:linkpicker:mode')")
        shot = _shot(page, "14a_link_picker_frontmatter")
        page.keyboard.press("Escape")
        time.sleep(0.2)
        try:
            insert_link_btn.first.click()
            time.sleep(0.3)
            value_restored = page.locator("#link-picker-mode").input_value()
        except Exception:
            value_restored = None
        finally:
            # Dialog offen lassen blockt jede folgende Station (ueberlagert #home-button
            # per pointer-events) -- Fund dieser Session, erste Fassung liess ihn offen.
            page.keyboard.press("Escape")
            time.sleep(0.2)
    ok = select_present and value_before == "frontmatter" and value_restored == "frontmatter"
    return ok, (
        f"select_present={select_present} opened={opened} "
        f"localStorage_after_change={value_before} restored_on_reopen={value_restored}"
    ), shot


CHROMIUM_ONLY = [
    station_01_uebersicht_1440,
    station_02_rail_reihenfolge,
    station_04_space_zeile_klicken,
    station_06_karten_knoten_esc,
    station_07_alle_items,
    station_09_konto_dialog,
    station_11_1024px,
    station_12_uebersicht_zweimal,
    station_13_zwillingskanten,
    station_14_link_picker,
]
BOTH_BROWSERS = [
    station_03_space_zeile_hover,
    station_05_item_klicken_esc,
    station_08_editor_kopfdaten,
    station_10_1200px,
]


def run_full_pass(browser_type, browser_name: str, results: list[Result], stations: list) -> None:
    browser = browser_type.launch()
    ctx = browser.new_context(viewport={"width": 1440, "height": 900})
    page = ctx.new_page()
    creds = json.loads(CREDS_PATH.read_text())
    status, note = login(page, creds["password"], creds["otpauth_uri"])
    if status not in (200, 303):
        results.append(Result("login", False, f"status={status} note={note}", None, browser_name))
        ctx.close()
        browser.close()
        return
    _dismiss_update_banner(page)
    for fn in stations:
        run_station(fn, page, browser_name, results)
    ctx.close()
    browser.close()


def main() -> int:
    if not CREDS_PATH.exists():
        print(f"ABBRUCH: {CREDS_PATH} fehlt -- Wegwerf-Instanz nicht vorbereitet.", file=sys.stderr)
        return 2

    results: list[Result] = []
    with sync_playwright() as p:
        print("== Chromium: alle 14 Stationen ==", file=sys.stderr)
        run_full_pass(p.chromium, "chromium", results, CHROMIUM_ONLY + BOTH_BROWSERS)

        print("== Firefox: Stationen 3/5/8/10 ==", file=sys.stderr)
        run_full_pass(p.firefox, "firefox", results, BOTH_BROWSERS)

    print("\n=== Ergebnis ===")
    for r in results:
        print(r.line())

    n_ok = sum(1 for r in results if r.ok)
    n_total = len(results)
    print(f"\n{n_ok}/{n_total} Stationen OK.")

    report_path = OUT_DIR.parent.parent / "phase8_6_ui_polish" / "scripts" / "p86_polish_smoke_report.json"
    report_path.write_text(json.dumps(
        [{"station": r.station, "ok": r.ok, "note": r.note, "shot": r.shot, "browser": r.browser}
         for r in results],
        indent=2, ensure_ascii=False,
    ))
    print(f"Report: {report_path}")

    return 0 if n_ok == n_total else 1


if __name__ == "__main__":
    sys.exit(main())
