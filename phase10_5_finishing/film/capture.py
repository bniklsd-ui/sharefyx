#!/usr/bin/env python3
"""P10.5 Block 16.1 — Aufnahmen der echten UI für den Launch-Film (Plan §2/§3.5).

Fährt die Wegwerf-Instanzen aus `wegwerf.py` (`neu` 8811, `alt` 8812) mit Playwright und legt
Standbilder und kurze Bildfolgen nach `~/sharefyx-film/stills/<instanz>/` — außerhalb des Repos.
Aufgenommen wird mit CDP `clip.scale = 2` (16.0: der einzige Weg, der scharf neu rastert), im
Fenster 1600 × 1000 (das Seitenverhältnis der Kacheln auf der Bühne) ⇒ 3200 × 2000 Pixel.

Aufruf mit `~/.claude-code-tools/film-venv/bin/python capture.py <neu|alt> [szene …]`.
Ausgabe JSON auf stdout (je Szene die geschriebenen Dateien).
"""
from __future__ import annotations

import base64
import hashlib
import hmac
import json
import struct
import sys
import time
from pathlib import Path

VW, VH, SCALE = 1600, 1000, 2
PORTS = {"neu": 8811, "alt": 8812}
OUT = Path.home() / "sharefyx-film" / "stills"


def totp_now(secret_b32: str, step: int = 0) -> str:
    key = base64.b32decode(secret_b32 + "=" * (-len(secret_b32) % 8))
    counter = int(time.time() // 30) + step
    digest = hmac.new(key, struct.pack(">q", counter), hashlib.sha1).digest()
    offset = digest[-1] & 0x0F
    return f"{(struct.unpack('>I', digest[offset:offset + 4])[0] & 0x7FFFFFFF) % 1000000:06d}"


class Kamera:
    """Eine angemeldete Seite + Aufnahme mit `clip.scale`."""

    def __init__(self, pw, instanz: str):
        self.instanz = instanz
        self.base = f"https://127.0.0.1:{PORTS[instanz]}"
        self.browser = pw.chromium.launch()
        self.ctx = self.browser.new_context(ignore_https_errors=True,
                                            viewport={"width": VW, "height": VH})
        self.page = self.ctx.new_page()
        self.fehler: list[str] = []
        self.page.on("pageerror", lambda e: self.fehler.append(str(e)))
        self.cdp = self.ctx.new_cdp_session(self.page)
        self.dir = OUT / instanz
        self.dir.mkdir(parents=True, exist_ok=True)
        self.dateien: dict[str, list[str]] = {}

    def login(self) -> None:
        z = json.loads(Path(f"/tmp/opencode/sharefyx-film-{self.instanz}/zugang.json").read_text())
        p = self.page
        p.goto(self.base + "/ui/login", wait_until="domcontentloaded")
        p.fill('input[name="space"]', z["space"])
        p.fill('input[name="password"]', z["password"])
        p.fill('input[name="totp"]', totp_now(z["secret"]))
        p.click('form[action="/ui/login"] button[type="submit"]')
        p.wait_for_selector("#shell", timeout=30000)
        p.wait_for_timeout(1500)
        # Den Update-Hinweis wegklicken (er gehört nicht in den Film; die alte UI hat keinen).
        if p.locator("#update-banner-dismiss").count() and p.locator("#update-banner-dismiss").is_visible():
            p.locator("#update-banner-dismiss").click()
            p.wait_for_timeout(500)

    def shot(self, szene: str, name: str, clip: dict | None = None) -> Path:
        c = clip or {"x": 0, "y": 0, "width": VW, "height": VH}
        png = base64.b64decode(self.cdp.send("Page.captureScreenshot", {
            "format": "png", "clip": {**c, "scale": SCALE}})["data"])
        ziel = self.dir / f"{szene}__{name}.png"
        ziel.write_bytes(png)
        self.dateien.setdefault(szene, []).append(ziel.name)
        return ziel

    def close(self) -> None:
        self.browser.close()


def szene_s1(k: Kamera) -> None:
    """S1: die Übersicht mit der Versionsangabe in der Leiste."""
    k.page.goto(k.base + "/ui/", wait_until="networkidle")
    k.page.wait_for_timeout(1500)
    k.shot("s1", "uebersicht")
    box = k.page.locator(".rail__version").bounding_box()
    k.dateien["s1_version"] = [k.page.locator(".rail__version").inner_text().strip()]
    if box:
        k.shot("s1", "version", {"x": max(box["x"] - 120, 0), "y": max(box["y"] - 40, 0),
                                 "width": 320, "height": 120})


TEXT_S2 = "## Ablauf\n**Wichtig:** Getränke bestellen\n- [ ] Tische leihen\n- [ ] Musik fragen\n- [ ] Einladung schreiben"


def _space_liste(k: Kamera, space: str = "studio") -> None:
    k.page.goto(k.base + "/ui/", wait_until="networkidle")
    k.page.wait_for_timeout(800)
    k.page.locator(".overview__space-open", has_text=space).first.click()
    k.page.wait_for_timeout(1200)


def _oeffne(k: Kamera, titel: str) -> None:
    _space_liste(k)
    k.page.locator("#rail-tree").get_by_text("Notizen", exact=True).first.click()
    k.page.wait_for_timeout(1000)
    k.page.fill("#search-input", titel)
    k.page.wait_for_timeout(1200)
    k.page.locator(".list__row", has_text=titel).first.click()
    k.page.wait_for_timeout(2000)


def szene_s2(k: Kamera) -> None:
    """S2–S4: der Editor. Neu: Tippen Zeichen für Zeichen (Bildfolge), Kästchen, Farbe/Größe.
    Alt: derselbe Text im alten Textfeld (ein Bild) — für den Lichtstreif 3 → 4."""
    _oeffne(k, "Sommerfest")
    p = k.page
    if k.instanz == "alt":
        ta = p.locator("#editor-textarea")
        if not ta.is_visible():  # v3.1.6 öffnet in der Vorschau; der Knopf schaltet um
            p.locator("#toggle-preview").click()
            p.wait_for_timeout(500)
        ta.click()
        p.keyboard.press("Control+End")
        ta.press_sequentially(TEXT_S2.replace("\n", "\n"), delay=0)
        p.wait_for_timeout(500)
        k.shot("s2", "fertig")
        return
    p.wait_for_selector(".CodeMirror", timeout=20000)
    p.evaluate("() => { const cm = document.querySelector('.CodeMirror').CodeMirror;"
               " cm.focus(); cm.setCursor(cm.lineCount(), 0); }")
    p.wait_for_timeout(300)
    k.shot("s2", "t000")
    for i, ch in enumerate(TEXT_S2, start=1):
        p.keyboard.press("Enter") if ch == "\n" else p.keyboard.insert_text(ch)
        p.wait_for_timeout(40)
        k.shot("s2", f"t{i:03d}")
    p.wait_for_timeout(400)
    k.shot("s2", "fertig")
    # S3: das erste Kästchen anklicken.
    box = p.locator(".CodeMirror input[type=checkbox]").first
    if box.count():
        box.click()
        p.wait_for_timeout(600)
        k.shot("s3", "kaestchen")
    # S4: „Getränke“ rot, „bestellen“ groß — je ein Wort, danach der Cursor weg (Zeile 0),
    # damit die Live-Darstellung das Markup verbirgt.
    def markiere(wort: str) -> None:
        p.evaluate("""w => { const cm = document.querySelector('.CodeMirror').CodeMirror;
            for (let l = 0; l < cm.lineCount(); l++) { const i = cm.getLine(l).indexOf(w);
              if (i >= 0) { cm.setSelection({line: l, ch: i}, {line: l, ch: i + w.length}); break; } }
            cm.focus(); }""", wort)
        p.wait_for_timeout(300)

    def ruhe() -> None:
        p.evaluate("() => { const cm = document.querySelector('.CodeMirror').CodeMirror; cm.setCursor(0, 0); }")
        p.wait_for_timeout(400)

    markiere("Getränke")
    k.shot("s4", "markiert")
    _waehle(p, "#format-farbe", "rot")
    ruhe()
    k.shot("s4", "rot")
    markiere("bestellen")
    _waehle(p, "#format-groesse", "gro")
    ruhe()
    k.shot("s4", "gross")
    for sel in ("#format-farbe", "#format-groesse"):
        k.dateien.setdefault("s4_optionen", []).append(
            f"{sel}: {p.locator(sel + ' option').all_inner_texts()}")


def _waehle(p, sel: str, teil: str) -> None:
    """Die erste Option, deren Text `teil` enthält."""
    werte = p.evaluate(f"() => [...document.querySelectorAll('{sel} option')].map(o => [o.value, o.textContent])")
    for wert, text in werte:
        if teil in text.lower() or teil in wert.lower():
            p.select_option(sel, wert)
            return


def _karte(k: Kamera) -> dict:
    return k.page.evaluate("""() => { const r = document.getElementById('overview-graph-canvas')
        .getBoundingClientRect(); return {x: r.left, y: r.top, width: r.width, height: r.height}; }""")


def szene_s5(k: Kamera) -> None:
    """S5/S6: die Karte — ganz (Zoom heraus), dann Suche, dann Status „In Arbeit“."""
    p = k.page
    p.set_viewport_size({"width": 1920, "height": 1200})
    p.goto(k.base + "/ui/", wait_until="networkidle")
    p.wait_for_timeout(2500)
    box = _karte(k)
    # v4 passt die Karte selbst ein (`fitView()`, solange niemand die Ansicht berührt hat) —
    # also **kein** Rad. v3.1.6 setzt die Ansicht per Doppelklick zurück.
    if k.instanz == "alt":
        p.mouse.dblclick(box["x"] + 6, box["y"] + box["height"] - 6)
    p.mouse.move(box["x"] + 4, box["y"] + box["height"] - 4)
    p.wait_for_timeout(2500)
    k.shot("s5", "ganz", box)
    if k.instanz == "neu":
        p.fill("#overview-graph-search", "Route")
        p.wait_for_timeout(1200)
        k.shot("s5", "suche", box)
        p.fill("#overview-graph-search", "")
        _waehle(p, "#overview-graph-filter-status", "arbeit")
        p.wait_for_timeout(1200)
        k.shot("s6", "in_arbeit", box)
    p.set_viewport_size({"width": VW, "height": VH})


def szene_s7(k: Kamera) -> None:
    """S7: Ordner umbenennen (Rechtsklick in der Leiste → Dialog → neue Leiste)."""
    p = k.page
    p.goto(k.base + "/ui/", wait_until="networkidle")
    p.wait_for_timeout(1200)
    p.locator("#rail-tree").get_by_text("projekte", exact=True).first.click(button="right")
    p.wait_for_timeout(500)
    p.locator("#folder-context-rename").click()
    p.wait_for_timeout(500)
    p.fill("#rename-folder-name-input", "sommer-2026")
    p.wait_for_timeout(300)
    k.shot("s7", "dialog")
    p.locator("#rename-folder-submit").click()
    p.wait_for_timeout(2000)
    k.shot("s7", "danach")


def szene_s8(k: Kamera) -> None:
    """S8: Filter „Zugewiesen“ in der Liste."""
    p = k.page
    _space_liste(k)
    p.locator("#rail-tree").get_by_text("In Arbeit", exact=True).first.click()
    p.wait_for_timeout(1000)
    k.shot("s8", "liste")
    _waehle(p, "#list-assignee", "studio") if "studio" in p.locator("#list-assignee").inner_text().lower() \
        else _waehle(p, "#list-assignee", "mir")
    p.wait_for_timeout(1200)
    k.shot("s8", "zugewiesen")


def szene_s10(k: Kamera) -> None:
    """S10: Ladezustand — die Übersicht künstlich verzögert (nur im Aufnahme-Browser)."""
    p = k.page
    p.route("**/api/v1/overview*", lambda route: (time.sleep(2.0), route.continue_()))
    p.goto(k.base + "/ui/", wait_until="domcontentloaded")
    p.wait_for_timeout(700)
    k.shot("s10", "laedt")
    p.wait_for_timeout(2500)
    k.shot("s10", "geladen")
    p.unroute("**/api/v1/overview*")


def szene_s11(k: Kamera) -> None:
    """S11: eine von Hand kaputte Notiz — die Suche liefert die übrigen."""
    data = Path(f"/tmp/opencode/sharefyx-film-{k.instanz}/data/studio")
    kaputt = sorted(data.rglob("itm_*gedanken*.md"))[0]
    text = kaputt.read_text(encoding="utf-8")
    kaputt.write_text(text.replace("title:", "title: [kaputt", 1), encoding="utf-8")
    p = k.page
    _space_liste(k)
    p.locator("#rail-tree").get_by_text("Alle Items", exact=True).first.click()
    p.wait_for_timeout(1000)
    p.fill("#search-input", "Gedanken")
    p.wait_for_timeout(1500)
    k.shot("s11", "suche")
    kaputt.write_text(text, encoding="utf-8")


def szene_s12(k: Kamera) -> None:
    """S12: die eigene Fehlerseite."""
    k.page.goto(k.base + "/ui/gibt-es-nicht", wait_until="networkidle")
    k.page.wait_for_timeout(800)
    k.shot("s12", "fehlerseite")


SZENEN = {"s1": szene_s1, "s2": szene_s2, "s5": szene_s5, "s7": szene_s7, "s8": szene_s8,
          "s10": szene_s10, "s11": szene_s11, "s12": szene_s12}
NUR_NEU = {"s7", "s8", "s10", "s11", "s12"}


def main() -> int:
    from playwright.sync_api import sync_playwright

    instanz = sys.argv[1]
    wahl = sys.argv[2:] or list(SZENEN)
    with sync_playwright() as pw:
        k = Kamera(pw, instanz)
        k.login()
        for s in wahl:
            if instanz == "alt" and s in NUR_NEU:
                continue
            try:
                SZENEN[s](k)
            except Exception as exc:  # eine Szene darf die anderen nicht mitnehmen
                k.dateien.setdefault("fehler", []).append(f"{s}: {exc.__class__.__name__}: {str(exc)[:300]}")
        k.close()
    print(json.dumps({"instanz": instanz, "dateien": k.dateien, "seitenfehler": k.fehler},
                     ensure_ascii=False))
    return 0


if __name__ == "__main__":
    sys.exit(main())
