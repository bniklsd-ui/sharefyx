#!/usr/bin/env python3
"""P10.5 — Sichtungs-Bilder an der Wegwerf-Instanz (statt Live-Sichtung).

**Wegwerf:** dieselbe Instanz-Mechanik wie `p105_b7_sichtung_probe.py` (Port 18793, tmp-`DATA_ROOT`,
tmp-`auth.sqlite3`, Stopp nur über die PID-Datei). Es wird nichts gemessen, es werden **Bilder**
gemacht: die Stellen, die der Nikinger beurteilt (UI-4: P10.5-32 · ED-1: P10.5-51), mit roten
Kästen und Nummern markiert. Bilder: `docs/screenshots/p105_sichtung_*.png`.

Aufruf: `.venv/bin/python phase10_5_finishing/probes/p105_sichtung_screens.py`
"""
from __future__ import annotations

import importlib.util
import json
import os
import subprocess
import sys
from pathlib import Path

REPO_ROOT = Path(__file__).resolve().parents[2]
SHOT_DIR = REPO_ROOT / "docs" / "screenshots"

_spec = importlib.util.spec_from_file_location("b7", Path(__file__).with_name("p105_b7_sichtung_probe.py"))
b7 = importlib.util.module_from_spec(_spec)
sys.path[:0] = [str(REPO_ROOT / "phase4_auth"), str(REPO_ROOT / "phase1_storage")]
_spec.loader.exec_module(b7)

FORMATE = ("# Formate\n\nEin Satz mit **fetter Marke** mitten drin.\n\nEin Satz mit *Kursiv* und `Code`.\n\n"
           "[rot]{.rot} [blau]{.blau} [grün]{.gruen} [gelb]{.gelb} [klein]{.klein} [groß]{.gross}\n\n"
           "::: {.zentriert}\nZentrierter Absatz\n:::\n\nLetzte Zeile ohne Zeichen.\n")
TODO = "- [ ] Eins\n- [x] Zwei\n- [ ] Drei\n"

SKILL = r'''
import json, sys, time, hmac, hashlib, struct, base64, io
from pathlib import Path
from PIL import Image, ImageDraw
base, space, password, secret, outdir = sys.argv[1:6]
SC = 2

def totp_now(s):
    key = base64.b32decode(s + "=" * (-len(s) % 8))
    d = hmac.new(key, struct.pack(">q", int(time.time() // 30)), hashlib.sha1).digest()
    o = d[-1] & 0x0F
    return f"{(struct.unpack('>I', d[o:o+4])[0] & 0x7FFFFFFF) % 1000000:06d}"

from playwright.sync_api import sync_playwright

def shot(page, name, boxes, clip=None):
    """boxes: [(label, locator-or-rect)] -- rote Kästen mit Nummer, im Bild."""
    rects = []
    for lab, what in boxes:
        if isinstance(what, dict):
            r = what
        else:
            bb = what.first.bounding_box()
            if not bb: continue
            r = bb
        rects.append((lab, r))
    data = page.screenshot(clip=clip) if clip else page.screenshot()
    im = Image.open(io.BytesIO(data)).convert("RGB")
    dr = ImageDraw.Draw(im)
    ox, oy = (clip["x"], clip["y"]) if clip else (0, 0)
    for lab, r in rects:
        x0, y0 = (r["x"] - ox) * SC - 4, (r["y"] - oy) * SC - 4
        x1, y1 = x0 + r["width"] * SC + 8, y0 + r["height"] * SC + 8
        dr.rectangle([x0, y0, x1, y1], outline=(255, 40, 40), width=3)
        dr.rectangle([x0, y0 - 26, x0 + 30, y0], fill=(255, 40, 40))
        dr.text((x0 + 9, y0 - 21), lab, fill=(255, 255, 255))
    im.save(Path(outdir) / name)
    return name, [lab for lab, _ in rects]

out = []
with sync_playwright() as p:
    br = p.chromium.launch()
    page = br.new_page(viewport={"width": 1400, "height": 900}, device_scale_factor=SC)
    err = []
    page.on("pageerror", lambda e: err.append(str(e)))
    page.goto(base + "/ui/login", wait_until="domcontentloaded")
    page.fill('input[name="space"]', space); page.fill('input[name="password"]', password)
    page.fill('input[name="totp"]', totp_now(secret))
    page.click('form[action="/ui/login"] button[type="submit"]')
    page.wait_for_selector("#shell", timeout=30000)
    try: page.wait_for_selector("#update-banner:not([hidden])", timeout=10000)
    except Exception: pass
    page.wait_for_timeout(800)
    # UI-4 (1) Wortmarke + (4) Version, (2) Banner
    brand = page.locator(".rail__brand").bounding_box()
    out.append(shot(page, "p105_sichtung_01_wortmarke_version.png",
        [("1", page.locator(".brand__mark")), ("2", page.locator(".rail__version"))],
        clip={"x": max(brand["x"]-10,0), "y": max(brand["y"]-10,0), "width": brand["width"]+40, "height": brand["height"]+20}))
    out.append(shot(page, "p105_sichtung_02_update_banner.png", [("3", page.locator("#update-banner"))]))
    page.wait_for_selector(".overview__space-open", timeout=20000)
    page.locator(".overview__space-open").first.click()
    page.wait_for_timeout(1200)
    out.append(shot(page, "p105_sichtung_03_liste_zugewiesen.png",
        [("4", page.locator("#list-assignee")), ("5", page.locator("#search-input"))]))
    # ED-1: Formate
    page.locator(".list__row", has_text="Formate").first.click()
    page.wait_for_selector(".CodeMirror", timeout=30000); page.wait_for_timeout(1200)
    zeile = page.locator(".CodeMirror-line", has_text="fetter Marke").first
    bb = zeile.bounding_box()
    page.mouse.click(bb["x"] + 60, bb["y"] + bb["height"] / 2); page.wait_for_timeout(500)
    out.append(shot(page, "p105_sichtung_04_editor_cursor_zeile.png",
        [("6", page.locator(".CodeMirror-line", has_text="fetter Marke")),
         ("7", page.locator(".CodeMirror-line", has_text="Kursiv"))]))
    letzte = page.locator(".CodeMirror-line", has_text="Letzte Zeile").first.bounding_box()
    page.mouse.click(letzte["x"] + 40, letzte["y"] + 8); page.wait_for_timeout(500)
    out.append(shot(page, "p105_sichtung_05_editor_formate.png",
        [("8", page.locator("#format-farbe")), ("9", page.locator(".CodeMirror-line", has_text="klein")),
         ("10", page.locator(".CodeMirror-line", has_text="Zentrierter"))]))
    page.click("#toggle-preview"); page.wait_for_timeout(600)
    out.append(shot(page, "p105_sichtung_06_rohtext.png",
        [("11", page.locator("#toggle-preview")), ("12", page.locator(".CodeMirror-line", has_text="fetter Marke"))]))
    page.click("#toggle-preview")
    page.click("#close-button"); page.wait_for_selector(".list__row", state="visible", timeout=15000)
    page.locator(".list__row", has_text="To-do-Item").first.click()
    page.wait_for_selector(".CodeMirror .sfx-todo", timeout=30000); page.wait_for_timeout(800)
    out.append(shot(page, "p105_sichtung_07_todo_kaestchen.png",
        [("13", page.locator(".CodeMirror .sfx-todo").nth(0)), ("14", page.locator(".CodeMirror .sfx-todo").nth(1))]))
    br.close()
print(json.dumps({"bilder": out, "seitenfehler": err}, ensure_ascii=False))
'''


def main() -> int:
    SHOT_DIR.mkdir(exist_ok=True)
    b7._stop()
    user = b7._setup()
    b7._seed_item()
    code = (
        "import sys; sys.path.insert(0, 'phase1_storage')\n"
        "from storage.store import Store\n"
        f"s = Store({str(b7.DATA_ROOT)!r}, git=False)\n"
        f"s.create({b7.SPACE!r}, type='task', title='Formate', body={FORMATE!r})\n"
        f"s.create({b7.SPACE!r}, type='task', title='To-do-Item', body={TODO!r})\n"
    )
    subprocess.run([".venv/bin/python", "-c", code], check=True, cwd=str(REPO_ROOT),
                   env={**os.environ, "PYTHONPATH": str(REPO_ROOT / "phase1_storage")})
    pid = b7._serve()
    try:
        skript = b7.WEGWERF_ROOT / "screens.py"
        skript.write_text(SKILL, encoding="utf-8")
        e2e = Path.home() / ".claude-code-tools/e2e-venv/bin/python"
        proc = subprocess.run(
            [str(e2e), str(skript), b7.BASE, user["space"], user["password"], user["secret"], str(SHOT_DIR)],
            cwd=str(REPO_ROOT), capture_output=True, text=True)
        if proc.returncode != 0:
            print(proc.stderr[-2000:], file=sys.stderr)
            return 1
        print(proc.stdout.strip().splitlines()[-1])
        return 0
    finally:
        b7._stop()
        print(f"Wegwerf-Instanz (pid {pid}) gestoppt", file=sys.stderr)


if __name__ == "__main__":
    sys.exit(main())
