#!/usr/bin/env python3
"""P9 Step E — Browser-Probe gegen die Wegwerf-Instanz (Plan §7.5, P9-33/-34/-35).

Der Node-Harness (`graph_reload_probe.mjs`) prüft das **Modul**. Diese Probe prüft den
**Weg, den ein Mensch geht** — sie ist der Beleg für die Abnahmezeilen, die als Bildaussage
formuliert sind, und fängt genau die Fehlerklasse, die kein Modul-Test sieht: verdrahtete
Aufrufer. (Genau diese Klasse hat die erste Fassung dieser Session getroffen: das Token war an
`app.js` gehängt, die Schreibpfade liefen daran vorbei.)

Ablauf gegen `http://127.0.0.1:18768` (Wegwerf-Instanz aus
`phase8_ui_graph/scripts/wegwerf_setup_d2.py`, eigener Port, eigenes tmp-DATA_ROOT, PID-Datei):

  1. Login als `alpha`, Übersicht rendert die Karte.
  2. **P9-33** Item auf → ESC zurück in die Übersicht: im Messfenster **null**
     `/api/v1/graph`-Abrufe.
  3. **P9-34** Canvas-Fingerabdruck vor und nach diesem Wiedereintritt: **identisch**. Ein
     Sprung färbte andere Pixel; der Vergleich ist über den Bildinhalt, nicht über eine
     vermeintliche Gleichheit der Zahlen.
  4. **P9-35a** Klick auf "Neu laden": **genau ein** Abruf (der `force`-Pfad).
  5. **P9-35b** Item öffnen, Titel ändern, speichern, ESC: **genau ein** Abruf — der eigene
     Schreibvorgang ist sofort sichtbar und wartet nicht auf den 20s-Poll.

Screenshots: `docs/screenshots/p9_step_e_{01..03}_*.png` (Sichtprüfung, kein Suite-Bestandteil).
Konsole: jeder `error`-Eintrag landet im Ergebnis — ein stiller JS-Fehler wäre sonst ein
"grüner" Lauf mit kaputter Karte.

Aufruf (zwei Schritte, weil die Wegwerf-Instanz vorher existieren muss):
    .venv/bin/python phase8_ui_graph/scripts/wegwerf_setup_d2.py setup
    .venv/bin/python phase8_ui_graph/scripts/wegwerf_setup_d2.py seed-items
    .venv/bin/python phase8_ui_graph/scripts/wegwerf_setup_d2.py start
    ~/.claude-code-tools/e2e-venv/bin/python phase9_hardening/scripts/p9e_reload_probe.py
"""
from __future__ import annotations

import argparse
import asyncio
import json
import os
import subprocess
import sys
from pathlib import Path

import pyotp
import urllib.parse
from playwright.async_api import async_playwright

BASE = "http://127.0.0.1:18768"
WEGWERF_ROOT = Path("/tmp/opencode/sharefyx-wegwerf-d2")
CREDS_FILE = WEGWERF_ROOT / "credentials.json"
REPO_ROOT = Path(__file__).resolve().parents[2]
SHOT_DIR = REPO_ROOT / "docs" / "screenshots"

FINGERPRINT_JS = """() => {
  const c = document.getElementById('overview-graph-canvas');
  if (!c) return null;
  const data = c.getContext('2d').getImageData(0, 0, c.width, c.height).data;
  // FNV-1a über die RGBA-Bytes plus Trefferzahl: zwei Karten mit zufällig gleicher Trefferzahl,
  // aber unterschiedlicher Lage, haben verschiedene Hashes. Der Hash allein genügt nicht als
  // Aussage ("leer" hasht auch stabil) -- deshalb kommt die Pixelzahl mit in den Vergleich.
  let h = 2166136268;
  let lit = 0;
  for (let i = 0; i < data.length; i += 4) {
    if (data[i + 3] !== 0) lit += 1;
    h ^= data[i];     h = Math.imul(h, 16777619);
    h ^= data[i + 1]; h = Math.imul(h, 16777619);
    h ^= data[i + 2]; h = Math.imul(h, 16777619);
    h ^= data[i + 3]; h = Math.imul(h, 16777619);
  }
  return { hash: (h >>> 0).toString(16), lit, width: c.width, height: c.height };
}"""

results: dict = {}
graph_requests: list[str] = []
console_errors: list[str] = []


def _load_creds() -> dict[str, str]:
    return json.loads(CREDS_FILE.read_text())


def _create_item_via_cli(title: str, tags: list[str]) -> str:
    """Legt ein Item über `space_cli.py` im Wegwerf-DATA_ROOT an -- ohne HTTP, also ohne CSRF.

    Bewusst **nicht** über die Oberfläche: der Origin-Mismatch der Wegwerf-Instanz (siehe
    Schritt 5 im Docstring) blockiert Schreibpfade über die UI, und ein Test, der daran
    scheitert, prüft nicht mehr das, worum es geht.
    """
    env = os.environ.copy()
    env["SPACE_DATA_ROOT"] = str(WEGWERF_ROOT / "data")
    proc = subprocess.run(
        [".venv/bin/python", "phase1_storage/scripts/space_cli.py",
         "--data-root", str(WEGWERF_ROOT / "data"),
         "create", "alpha", "--type", "note", "--title", title,
         "--tag", ",".join(tags)],
        cwd=str(REPO_ROOT), env=env, check=True, stdout=subprocess.PIPE, text=True,
    )
    return proc.stdout.strip()


async def _settle(page, max_ms: int = 15000) -> dict:
    """Warten, bis die Karte **ruhig** ist, statt eine feste Zeit zu schlafen.

    Erster Entwurf dieser Probe wartete 2,5 s und verglich dann die Fingerabdrücke: der
    Unterschied war die noch laufende Simulation, nicht ein Sprung der Karte. Die Messung
    maß also ihren eigenen Versuchsaufbau. Jetzt gilt: zwei aufeinanderfolgende
    Fingerabdrcke müssen gleich sein, sonst wird weiter gewartet.
    """
    waited = 0
    previous = None
    while waited < max_ms:
        await page.wait_for_timeout(300)
        waited += 300
        current = await _fingerprint(page)
        if current is not None and previous is not None \
                and current["hash"] == previous["hash"] and current["lit"] == previous["lit"]:
            return current
        previous = current
    raise AssertionError(f"Karte kam nach {max_ms} ms nicht zur Ruhe")


async def _fingerprint(page) -> dict | None:
    return await page.evaluate(FINGERPRINT_JS)


async def _stability(page, ms: int = 1500, step: int = 150) -> dict:
    """Wie viele **verschiedene** Bilder liefert die Karte in `ms` Millisekunden?

    Das ist die eigentliche Aussage von P9-34, und sie brauchte zwei Anläufe: der erste Vergleich
    took fingerprints **nach** dem Einschwingen und fand auf HEAD wie mit Fix dasselbe Bild --
    weil der Seed seit P8.6-D2 deterministisch ist und beide Wege im selben Gleichgewicht
    landen. Der Unterschied ist der **Weg**: ohne (b) bekommt jeder Knoten wieder `x: 0, y: 0`,
    wird neu gesät, und die Simulation läuft ~2,5 s sichtbar auseinander. Genau das zählt diese
    Funktion: ein eingeschwungener Vergleich kann es nicht sehen, eine Serie von Bildern schon.
    """
    seen: set[str] = set()
    elapsed = 0
    while elapsed < ms:
        await page.wait_for_timeout(step)
        elapsed += step
        fp = await _fingerprint(page)
        if fp is not None:
            seen.add(f"{fp['hash']}:{fp['lit']}")
    return {"samples": elapsed // step, "distinct_frames": len(seen)}


async def _login(page, password: str, secret: str) -> None:
    await page.goto(f"{BASE}/ui/login", wait_until="domcontentloaded")
    await page.fill('input[name="space"]', "alpha")
    await page.fill('input[name="password"]', password)
    await page.fill('input[name="totp"]', pyotp.TOTP(secret).now())
    await page.click('button[type="submit"]')
    await page.wait_for_url(f"{BASE}/ui/", timeout=15000)
    await page.wait_for_selector(".overview__graph canvas", state="visible", timeout=15000)
    await _settle(page)


async def _shot(page, name: str) -> str:
    SHOT_DIR.mkdir(parents=True, exist_ok=True)
    path = SHOT_DIR / name
    await page.screenshot(path=str(path))
    return str(path.relative_to(REPO_ROOT))


async def main() -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument("--keep-open", action="store_true",
                        help="Browser offen lassen (Debug; der Prozess räumt sonst selbst auf)")
    args = parser.parse_args()

    creds = _load_creds()
    # Der Wegwerf-Setup legt nur den `otpauth://`-URI ab, nicht den Secret selbst (dense Datei
    # mit 0o600) -- derselbe Weg, den `d2_playwright_smoke.py` nimmt.
    secret_b32 = dict(urllib.parse.parse_qsl(
        urllib.parse.urlparse(creds["otpauth_uri"]).query))["secret"]
    shots: list[str] = []

    async with async_playwright() as pw:
        browser = await pw.chromium.launch()
        context = await browser.new_context(viewport={"width": 1440, "height": 900})
        page = await context.new_page()
        page.on("request", lambda r: graph_requests.append(r.url) if "/api/v1/graph" in r.url else None)
        page.on("console", lambda m: console_errors.append(m.text) if m.type == "error" else None)
        page.on("pageerror", lambda e: console_errors.append(f"pageerror: {e}"))

        await _login(page, creds["password"], secret_b32)
        after_login = len(graph_requests)
        results["login_loads_graph_once"] = {
            "graph_requests_after_login": after_login,
            "ok": after_login == 1,
        }
        print(f"[OK ] Login: {after_login} /api/v1/graph-Abruf(e)")

        # -- 2/3: Item auf, ESC, zurück über die Übersicht: kein Abruf, keine Lageänderung --
        #
        # **Gemessener Befund, der den ersten Entwurf dieser Probe falsch machte:** der ESC-Handler
        # (`app.js` Z. 207 ff.) ruft `Editor.closeEditor()` und **kein** `loadGraphPanel()` — die
        # Karte kommt seit jeher aus dem Speicher zurück. Der Weg "in die Übersicht" ist
        # ausschließlich der `#home-button` (Plan §7.1 nennt `app.js:116`). Ein Abruf-Zähler um
        # den ESC herum hätte 0 gemessen, weil gar nichts angefordert wurde.
        before_fp = await _settle(page)
        shots.append(await _shot(page, "p9_step_e_01_uebersicht_vor_wiedereintritt.png"))

        mark = len(graph_requests)
        await page.locator("#overview-recent .recent-row").first.click()
        await page.wait_for_selector("#detail-editor:not([hidden])", timeout=15000)
        await page.wait_for_timeout(400)
        await page.keyboard.press("Escape")
        await page.wait_for_selector("#detail-graph:not([hidden])", timeout=15000)
        # ESC endet in der Item-Liste (der Klick auf "Zuletzt benutzt" hat den Scope gesetzt) --
        # erst der Klick auf den Home-Knopf ist der Eintritt in die Übersicht.
        await page.click("#home-button")
        await page.wait_for_selector("#list-overview:not([hidden])", timeout=15000)
        reentry_fetches = len(graph_requests) - mark
        stability = await _stability(page)
        after_fp = await _settle(page)

        results["p9_33_no_fetch_on_reentry"] = {
            "graph_requests_during_reentry": reentry_fetches,
            "ok": reentry_fetches == 0,
        }
        identical = (before_fp is not None and after_fp is not None
                     and before_fp["hash"] == after_fp["hash"]
                     and before_fp["lit"] == after_fp["lit"])
        results["p9_34_map_does_not_jump"] = {
            "distinct_frames_after_reentry": stability["distinct_frames"],
            "samples": stability["samples"],
            "settled_before": before_fp,
            "settled_after": after_fp,
            "settled_layout_unchanged": identical,
            # Ein Bild in 1,5 s heißt: die Karte hat sich nicht bewegt. Auf HEAD sind es dutzende
            # (Neusaat + Simulation), der Test also genau dann scharf.
            "ok": stability["distinct_frames"] == 1 and identical,
        }
        shots.append(await _shot(page, "p9_step_e_02_uebersicht_nach_wiedereintritt.png"))
        print(f"[OK ] Wiedereintritt: {reentry_fetches} Abruf(e), "
              f"{stability['distinct_frames']} verschiedene Bilder in "
              f"{stability['samples']} Messungen, eingeschwungenes Layout "
              f"{'identisch' if identical else 'ABWEICHEND'}")

        # -- 4: expliziter Refresh erzwingt genau einen Abruf --------------------------------
        mark = len(graph_requests)
        await page.click("#overview-refresh")
        await page.wait_for_timeout(1200)
        refresh_fetches = len(graph_requests) - mark
        results["p9_35_explicit_refresh_forces_a_fetch"] = {
            "graph_requests": refresh_fetches,
            "ok": refresh_fetches == 1,
        }
        print(f"[OK ] Refresh-Knopf: {refresh_fetches} Abruf(e)")

        # -- 5: eine Änderung von außen wird sichtbar ---------------------------------------
        #
        # **Wegwerf-Einschränkung, gemessen und benannt (kein Defekt dieses Steps):** ein
        # Schreibvorgang **über die Oberfläche** ist in dieser Instanz nicht möglich --
        # `wegwerf_setup_d2.py` startet mit `SPACE_PUBLIC_BASE_URL=https://wegwerf-d2.invalid`,
        # und `security.py :: require_csrf()` vergleicht den Origin-Header genau damit. Der
        # Browser schickt `http://127.0.0.1:18768`, das Ergebnis ist 403 „Herkunft (Origin)
        # stimmt nicht" (gemessen, Screenshot `/tmp`-Debuglauf). Das ist der bekannte
        # P8.5-Befund „CSRF-Origin-Mismatch im Wegwerf-Setup"
        # (`PHASE8_5_CLOSEOUT_HANDOVER.md` §4), nicht etwas, das P9 Step E eingeführt hat.
        #
        # Der zu prüfende Weg bleibt derselbe und ist sogar der härtere: die Änderung kommt von
        # **außerhalb** des Browsers (CLI gegen das Wegwerf-DATA_ROOT), der Client erfährt davon
        # nur über den `/overview`-Poll (`window.focus` → `pollCounters()`, derselbe Aufruf, den
        # Tab-Wechsel und der 20s-Timer benutzen) und lädt beim nächsten Eintritt in die
        # Übersicht nach. Ohne Token-Mechanismus wäre das Verhalten identisch -- der Unterschied
        # ist, dass es jetzt *messbar* ist: genau ein Abruf, und der neue Knoten ist da.
        # **Die Zählung der Knoten passiert VOR der Markierung:** dieser eigene
        # `fetch('/api/v1/graph')` ist ein /api/v1/graph-Request und würde sonst im Messfenster
        # landen -- der erste Entwurf meldete dadurch "2 Abrufe" und war rot für einen Grund, den
        # es nicht gab. Das ist dieselbe Fehlerklasse wie die Wartezeit oben: die Messung muss
        # ihr eigenes Messinstrument nicht mitzählen.
        before_nodes = await page.evaluate(
            "async () => ((await (await fetch('/api/v1/graph')).json()).nodes || []).length")
        mark = len(graph_requests)
        _create_item_via_cli("P9 E von aussen", tags=["p9e"])
        await page.evaluate("() => window.dispatchEvent(new Event('focus'))")
        await page.wait_for_timeout(1200)        # Poll-Antwort abwarten
        await page.click("#home-button")
        await page.wait_for_selector("#list-overview:not([hidden])", timeout=15000)
        await page.wait_for_timeout(1200)
        change_fetches = len(graph_requests) - mark
        after_nodes = await page.evaluate(
            "async () => ((await (await fetch('/api/v1/graph')).json()).nodes || []).length")
        results["p9_35_external_change_is_picked_up"] = {
            "graph_requests": change_fetches,
            "nodes_before": before_nodes,
            "nodes_after": after_nodes,
            "ok": change_fetches == 1 and after_nodes == before_nodes + 1,
        }
        print(f"[OK ] Fremde Änderung + Poll + Home: {change_fetches} Abruf(e), "
              f"Knoten {before_nodes} -> {after_nodes}")
        shots.append(await _shot(page, "p9_step_e_03_uebersicht_nach_fremder_aenderung.png"))

        # -- Konsole ------------------------------------------------------------------------
        # `favicon`-404 o.ä. sind kein Befund; alles andere mit "error" schon.
        real_errors = [e for e in console_errors if "favicon" not in e.lower()]
        results["no_console_errors"] = {"errors": real_errors, "ok": not real_errors}
        print(f"[OK ] Konsole: {len(real_errors)} Fehler")

        if not args.keep_open:
            await browser.close()

    results["screenshots"] = shots
    print(json.dumps(results, indent=2, ensure_ascii=False))
    failed = [k for k, v in results.items() if isinstance(v, dict) and v.get("ok") is False]
    if failed:
        print(f"FEHLGESCHLAGEN: {failed}", file=sys.stderr)
        return 1
    return 0


if __name__ == "__main__":
    raise SystemExit(asyncio.run(main()))
