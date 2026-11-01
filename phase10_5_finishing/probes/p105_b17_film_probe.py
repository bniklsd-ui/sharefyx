#!/usr/bin/env python3
"""P10.5 17.3 — Browser-Probe: der Launch-Film in der App (Plan
`docs/concepts/phase10_5_block17_film_app_plan.md` §5).

**Wegwerf:** die Film-Instanz `neu` (`film/wegwerf.py`, Port 8811, tmp-`DATA_ROOT`, Stopp nur über
die PID-Datei). Statik liest sie je Anfrage aus dem Arbeitsbaum; Python-Änderungen (CSP, Route)
brauchen einen Neustart der Wegwerf-Instanz.

**Browser: Google Chrome** (`/usr/bin/google-chrome`), nicht Playwrights Chromium — der
Open-Source-Build spielt kein H.264 (Plan F7). Mit `--autoplay-policy=document-user-activation-required`:
unter der strengen Regel beweist erst der Klick, dass Ton erlaubt ist.

**Zellen:** P1 Startbild + Klick spielt mit Ton · P2 ohne Klick keine `*.mp4`-Anfrage ·
P3 keine CSP-Verletzung · P4 die Browser-Anfrage bekommt 206 · P5 Wiedersehen aus dem Update-Log ·
P6 `Escape` schließt, `src` leer · P7 privates Fenster (`localStorage` wirft) ⇒ kein Startbild ·
P8 Bildschirmfoto mitten im Film.

Aufruf: `~/.claude-code-tools/film-venv/bin/python p105_b17_film_probe.py [--out x.json] [--vorab-gesehen]`.
`--vorab-gesehen` ist der Gegenlauf zu P1 (Schlüssel vorab gesetzt ⇒ kein Startbild).
"""
from __future__ import annotations

import json
import sys
import time
from pathlib import Path

FILM = Path(__file__).resolve().parents[1] / "film"
sys.path.insert(0, str(FILM))
from capture import totp_now  # noqa: E402

BASE = "https://127.0.0.1:8811"
ZUGANG = Path("/tmp/opencode/sharefyx-film-neu/zugang.json")
CHROME = "/usr/bin/google-chrome"
SHOT = Path("/tmp/opencode/sharefyx-film-neu/p105_b17_mitten_im_film.png")
SHOT_START = Path("/tmp/opencode/sharefyx-film-neu/p105_b17_startbild.png")

# Vor jedem Dokument: CSP-Verletzungen mitschreiben; optional `localStorage` werfen lassen (P7)
# oder den Schlüssel vorab setzen (Gegenlauf P1).
CSP_HOOK = """window.__csp = [];
document.addEventListener('securitypolicyviolation', e => window.__csp.push(e.violatedDirective + ' ' + e.blockedURI));"""
PRIVAT_HOOK = """Object.defineProperty(window, 'localStorage', { get() { throw new DOMException('privat', 'SecurityError'); } });"""
GESEHEN_HOOK = """try { localStorage.setItem('sfx:film:gesehen', '4.0.0'); } catch (e) {}"""


def _login(p) -> None:
    """Zwei Anmeldungen je Lauf (Hauptlauf, P7): der Server lehnt einen schon benutzten
    TOTP-Code ab (Replay-Schutz). Scheitert die Anmeldung, wartet die Probe das nächste
    30-s-Fenster ab und versucht es einmal neu."""
    z = json.loads(ZUGANG.read_text())
    for versuch in range(2):
        p.goto(BASE + "/ui/login", wait_until="domcontentloaded")
        p.fill('input[name="space"]', z["space"])
        p.fill('input[name="password"]', z["password"])
        p.fill('input[name="totp"]', totp_now(z["secret"]))
        p.click('form[action="/ui/login"] button[type="submit"]')
        try:
            p.wait_for_selector("#shell", timeout=10000)
            break
        except Exception:
            if versuch:
                raise
            p.wait_for_timeout((30 - time.time() % 30 + 1) * 1000)
    p.wait_for_timeout(1500)


def _kontext(browser, *hooks: str):
    ctx = browser.new_context(ignore_https_errors=True, viewport={"width": 1280, "height": 720})
    for hook in (CSP_HOOK, *hooks):
        ctx.add_init_script(hook)
    p = ctx.new_page()
    mp4: list[dict] = []
    p.on("response", lambda r: mp4.append({"status": r.status, "range": r.headers.get("content-range")})
         if r.url.endswith(".mp4") else None)
    fehler: list[str] = []
    p.on("pageerror", lambda e: fehler.append(str(e)))
    return ctx, p, mp4, fehler


def _video(p) -> dict:
    return p.evaluate("""() => { const v = document.getElementById('launch-film-video');
      return { t: v.currentTime, muted: v.muted, paused: v.paused, src: v.getAttribute('src'),
               err: v.error && v.error.code, offen: !document.getElementById('launch-film').hidden,
               start: !document.getElementById('launch-film-start').hidden,
               vollbild: !!document.fullscreenElement,
               gesehen: (() => { try { return localStorage.getItem('sfx:film:gesehen'); } catch (e) { return 'WIRFT'; } })(),
               csp: window.__csp }; }""")


def main() -> int:
    from playwright.sync_api import sync_playwright

    out = Path(sys.argv[sys.argv.index("--out") + 1]) if "--out" in sys.argv else \
        Path(__file__).with_name("p105_b17_film.json")
    vorab = "--vorab-gesehen" in sys.argv
    cells: dict[str, dict] = {}
    with sync_playwright() as pw:
        browser = pw.chromium.launch(executable_path=CHROME, args=[
            "--autoplay-policy=document-user-activation-required"])
        ctx, p, mp4, fehler = _kontext(browser, *([GESEHEN_HOOK] if vorab else []))
        _login(p)
        vor_klick = _video(p)
        anfragen_vor_klick = len(mp4)
        cells["P1_startbild"] = {"ok": vor_klick["offen"] and vor_klick["start"]
                                 and vor_klick["gesehen"] == "4.0.0", **vor_klick}
        if not vor_klick["offen"]:
            cells["abbruch"] = {"ok": False, "grund": "kein Startbild — Rest der Probe ohne Sinn"}
        else:
            p.screenshot(path=str(SHOT_START))
            p.click("#launch-film-play")
            p.wait_for_timeout(2500)
            spielt = _video(p)
            p.screenshot(path=str(SHOT))
            cells["P1_klick_spielt_mit_ton"] = {"ok": spielt["t"] > 0.5 and not spielt["muted"]
                                                and not spielt["paused"], **spielt}
            cells["P3_csp"] = {"ok": not spielt["csp"] and spielt["err"] is None,
                               "verletzungen": spielt["csp"]}
            cells["P4_range"] = {"ok": any(r["status"] == 206 and r["range"] for r in mp4),
                                 "antworten": mp4[:5]}
            cells["P8_bild"] = {"ok": SHOT.is_file(), "datei": str(SHOT)}
            p.keyboard.press("Escape")  # ein Druck: Film zu, Vollbild verlassen
            p.wait_for_timeout(800)
            zu = _video(p)
            cells["P6_escape_schliesst"] = {"ok": not zu["offen"] and zu["src"] is None
                                            and not zu["vollbild"], **zu}

            # P2: neu laden — kein Startbild, keine Anfrage an das Video.
            mp4.clear()
            p.reload(wait_until="networkidle")
            p.wait_for_timeout(1500)
            neu = _video(p)
            cells["P2_ohne_klick_kein_download"] = {
                "ok": not neu["offen"] and not mp4 and anfragen_vor_klick == 0,
                "anfragen_vor_erstem_klick": anfragen_vor_klick, "anfragen_nach_reload": len(mp4)}

            # P5: aus dem Update-Log wieder abspielen.
            p.evaluate("window.dispatchEvent(new CustomEvent('sfx:open-panel', {detail: {name: 'updates'}}))")
            p.wait_for_timeout(800)
            p.click("#update-log-film")
            p.wait_for_timeout(2500)
            wieder = _video(p)
            cells["P5_wiedersehen"] = {"ok": wieder["offen"] and wieder["t"] > 0.5
                                       and not wieder["muted"], **wieder}
        cells["seitenfehler"] = {"ok": not fehler, "fehler": fehler}
        ctx.close()

        # P7: privates Fenster.
        ctx, p, mp4, fehler = _kontext(browser, PRIVAT_HOOK)
        _login(p)
        privat = _video(p)
        cells["P7_privat_kein_startbild"] = {"ok": not privat["offen"] and not mp4
                                             and privat["gesehen"] == "WIRFT", **privat}
        ctx.close()
        browser.close()

    ok = all(c["ok"] for c in cells.values())
    out.write_text(json.dumps({"ok": ok, "vorab_gesehen": vorab, "cells": cells}, indent=2,
                              ensure_ascii=False) + "\n")
    print(json.dumps({"ok": ok, "rot": [k for k, c in cells.items() if not c["ok"]]}))
    return 0 if ok else 1


if __name__ == "__main__":
    sys.exit(main())
