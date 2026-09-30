#!/usr/bin/env python3
"""P9 Step G — Browser-Selbstprüfung des Löschpfads (Plan §9.2, P9-45 – P9-51).

Warum ein Browser und nicht nur Tests: das Gate besteht aus **zwei Stufen**, und keine der
statischen Wächter kann beweisen, dass sie in dieser Reihenfolge erscheinen und dass der Knopf
tatsächlich gesperrt ist. Genau das prüft dieses Skript.

**Zwei Dinge, die vorab gemessen und eingerichtet sein mussten** — beide sind Befunde, keine
Nebensache:

1. **Die 18773er Wegwerf-Instanz kann keinen Schreibvorgang annehmen.** `security.py ::
   require_csrf` vergleicht den `Origin`-Header des Browsers (`http://127.0.0.1:18773`) mit
   `settings.base_url`, und das ist in `mcpserver/app.py:204` **genau** `oauth.settings.base_url`,
   also `SPACE_PUBLIC_BASE_URL` — das wegen seiner Rolle als OAuth-Issuer zwingend `https://`
   sein muss (`authserver/config.py:87`). Ein lokaler Plain-HTTP-Server kann den Vergleich also
   **strukturell nie** erfüllen. Der Kommentar im Setup-Skript (Zeile 341) nennt das selbst einen
   „Befund für Block D / Step Z"; hier ist die Ursache bis auf die Zeile zurückgeführt. Deshalb
   gibt es für dieses Skript eine eigene Instanz mit passendem Setup (`p9_step_g_wegwerf.py`) —
   und selbst dort bleibt der Origin-Header der einzige unpassende Punkt.
2. **Der Schreibpfad braucht TLS — und der Grund ist eine Produktinvariante, kein Setup-Fehler.**
   `require_csrf` (security.py:79-95) hat drei Schichten: `Origin` muss **exakt**
   `settings.base_url` entsprechen, fehlt `Origin`, muss `sec-fetch-site: same-origin` kommen, und
   `X-CSRF-Token` muss zum Sitzungs-Hash passen. `settings.base_url` ist in
   `mcpserver/app.py:204` genau `oauth.settings.base_url` = `SPACE_PUBLIC_BASE_URL`, und das muss
   laut `authserver/config.py:87` zwingend `https://` sein (Rolle als OAuth-Issuer). Ein Browser auf
   `http://127.0.0.1:18773` kann die Prüfung also **strukturell nie** erfüllen; `Origin` lässt sich
   auch nicht entfernen (verbotener Header — `page.route()` bleibt wirkungslos, gemessen), und
   `serve.py` ruft `uvicorn.run()` ohne `ssl_*`.
   **Gemessene Konsequenz:** diese Instanz bekommt ein selbstsigniertes Zertifikat für
   `IP:127.0.0.1` und einen Harness-Launcher, der **dieselbe** App baut wie `serve.py`, nur mit
   `ssl_keyfile`/`ssl_certfile`. `serve.py` selbst bleibt unberührt — einen Produktparameter nur für
   einen Testharness zu ergänzen, wäre genau die Scope-Ausweitung, die P9-K vermeiden soll.
   Der Browser akzeptiert nur das Harness-Zertifikat (`ignore_https_errors`); **Sitzung, CSRF,
   Origin und alle drei CSRF-Schichten laufen unverändert.** Der 18773er-Wegwerf bleibt unberührt.

Stationen (jede mit Sichtprüfung, jede mit Screenshot):

  1  Liste gerendert, Löschknopf nur an eigenen Items
  2  Stufe 1: `confirmDialog` mit der Konsequenz — **Abbrechen** bricht ab, nichts gelöscht
  3  Stufe 2: Dialog mit Titel-Eingabe, `Löschen` **gesperrt**
  4  Falscher Titel (nur Großschreibung) → bleibt gesperrt (keine Toleranz)
  5  Exakter Titel → Knopf wird frei
  6  Nach dem Löschen: Zeile weg, Toast
  7  ESC in Stufe 2 → Dialog zu, nichts gelöscht
  8  **Gegenprobe am Server**: `._trash/` existiert, Datei byte-identisch, `GET` → 404,
     und ein frischer `rebuild_index()` lässt sie **nicht** wieder auftauchen

Station 8 ist die, die keinen Bildschirm braucht und trotzdem die wichtigste ist: die
Unsichtbarkeit ist eine Eigenschaft des **Orts**, nicht des Löschvorgangs.

Aufruf (Hard Rule 9: Stopp ausschließlich über die PID-Datei des jeweiligen Wegwerf-Skripts):
    python phase9_hardening/scripts/p9_step_g_wegwerf.py start
    ~/.claude-code-tools/e2e-venv/bin/python phase9_hardening/scripts/p9_step_g_self_check.py
    python phase9_hardening/scripts/p9_step_g_wegwerf.py stop
"""
from __future__ import annotations

import argparse
import os
import base64
import datetime
import hashlib
import hmac
import json
import struct
import sys
import time
import urllib.parse
import urllib.request
from pathlib import Path

from playwright.sync_api import Page, sync_playwright

REPO_ROOT = Path(__file__).resolve().parents[2]
OUT_DIR = REPO_ROOT / "docs" / "screenshots"
PROBE_DIR = REPO_ROOT / "phase9_hardening" / "probes"
DEFAULT_BASE_URL = "https://127.0.0.1:18775"  # eigene TLS-Instanz, siehe Docstring-Punkte 1+2
DEFAULT_CREDS = Path("/tmp/opencode/p9-step-g-wegwerf/credentials.json")

# Führt im Projekt-venv einen echten Index-Neuaufbau gegen das Harness-DATA_ROOT aus und
# meldet als eine JSON-Zeile zurück, was danach im Index steht. Als Snippet-Schnur statt
# importiertem Code, weil das Playwright-venv `storage` nicht kennt (siehe Aufrufstelle).
REBUILD_SNIPPET = """
import json, sys
from storage.store import Store
# argv[2] ist der Titel des in DIESEM Lauf geloeschten Items — nicht ein fest verdrahteter
# Fixture-Name. Der erste Listeneintrag ist von Lauf zu Lauf ein anderer (das Harness säet neu),
# und eine Prüfung, die einen bestimmten Namen erwartet, misst dann den Zufall statt der Sache.
geloescht = sys.argv[2]
store = Store(sys.argv[1], git=False)
store.rebuild_index()
titel = [i.title for i in store.search(space='alpha').items]
print(json.dumps({
    'titel': titel,
    'geloescht': geloescht,
    'spaces': [s.name for s in store.list_spaces()],
    'wieder_da': geloescht in titel,
}))
"""

befunde: list[dict] = []


def pruefe(name: str, ok: bool, detail: str = "") -> None:
    befunde.append({"pruefung": name, "ok": bool(ok), "detail": detail})
    print(f"  [{'OK ' if ok else 'FEHLER'}] {name}" + (f" — {detail}" if detail else ""),
          file=sys.stderr)


# --- TOTP/Login (entliehen aus p86_block_h_r_part2_self_check.py) --------------------------


def _generate_totp(otpauth_uri: str) -> str:
    qs = urllib.parse.parse_qs(urllib.parse.urlparse(otpauth_uri).query)
    secret_b32 = qs["secret"][0]
    key = base64.b32decode(secret_b32 + "=" * (-len(secret_b32) % 8))
    msg = struct.pack(">q", int(time.time() // 30))
    h = hmac.new(key, msg, hashlib.sha1).digest()
    offset = h[-1] & 0x0F
    return f"{(struct.unpack('>I', h[offset:offset + 4])[0] & 0x7FFFFFFF) % 1000000:06d}"


def login(page: Page, base_url: str, password: str, otpauth_uri: str) -> bool:
    for fenster in range(2):
        page.goto(f"{base_url}/ui/login", wait_until="domcontentloaded")
        page.locator('input[name="space"]').fill("alpha")
        page.locator('input[name="password"]').fill(password)
        page.locator('input[name="totp"]').fill(_generate_totp(otpauth_uri))
        with page.expect_response("**/ui/login**") as info:
            page.locator('button[type="submit"]').click()
        if info.value.status in (200, 303):
            time.sleep(2.0)
            if not page.url.startswith(f"{base_url}/ui/"):
                page.goto(f"{base_url}/ui/", wait_until="domcontentloaded")
            return True
        time.sleep(35)
    return False


def _api(base_url: str, path: str, *, cookie: str, method: str = "GET", body: str = "") -> tuple:
    """Rohzugriff auf die eigene API — dieselbe Sitzung wie der Browser, um den **Zustand nach
    dem Klick** zu prüfen (404, Datei weg). `unverified` betrifft nur das selbstsignierte
    Harness-Zertifikat, dieselbe Ausnahme wie `ignore_https_errors` im Browser; am Server ändert
    das nichts, CSRF- und Sitzungsprüfung laufen durch den Browser, nicht durch diesen Aufruf."""
    import ssl

    req = urllib.request.Request(f"{base_url}{path}", data=body.encode() or None, method=method)
    req.add_header("Cookie", cookie)
    if body:
        req.add_header("Content-Type", "application/json")
    try:
        with urllib.request.urlopen(req, context=ssl._create_unverified_context()) as resp:
            return resp.status, resp.read()
    except urllib.error.HTTPError as exc:
        return exc.code, exc.read()


def main() -> int:
    ap = argparse.ArgumentParser()
    ap.add_argument("--base-url", default=DEFAULT_BASE_URL)
    ap.add_argument("--creds", type=Path, default=DEFAULT_CREDS)
    args = ap.parse_args()
    OUT_DIR.mkdir(parents=True, exist_ok=True)
    PROBE_DIR.mkdir(parents=True, exist_ok=True)

    creds = json.loads(args.creds.read_text())
    with sync_playwright() as pw:
        # `ignore_https_errors` für das **selbstsignierte** Harness-Zertifikat. Nichts anderes
        # wird ignoriert: Sitzung, CSRF, Origin und TLS-Prüfung des Servers laufen normal.
        browser = pw.chromium.launch()
        page = browser.new_page(viewport={"width": 1440, "height": 900},
                                ignore_https_errors=True)
        page.goto(f"{args.base_url}/ui/login", wait_until="domcontentloaded")
        # TOTP-Fenster abwarten, statt ein verbrauchtes zu senden (Login-Rate-Limit!).
        time.sleep(32 - (datetime.datetime.now().second % 30))
        if not login(page, args.base_url, creds["password"], creds["otpauth_uri"]):
            print("Login fehlgeschlagen", file=sys.stderr)
            return 2
        try:
            page.locator("#update-banner-dismiss").click(timeout=800)
        except Exception:
            pass

        # Der eigene Space "alpha" — nur dort darf der Knopf überhaupt erscheinen.
        page.goto(f"{args.base_url}/ui/", wait_until="domcontentloaded")
        time.sleep(1.5)
        seitencookies = {c["name"]: c["value"] for c in page.context.cookies()}
        cookie_header = "; ".join(f"{k}={v}" for k, v in seitencookies.items())

        # In den **eigenen** Space "alpha" — dieselbe Navigation, die `p86_polish_smoke.py`
        # benutzt (`.overview__space-open` auf der Übersicht), nicht ein Rail-Klick: der
        # Rail-Knopf öffnet nur den Twist und wechselt nicht in die Item-Liste.
        offen = page.locator(".overview__space-open", has_text="alpha")
        if offen.count() == 0:
            offen = page.locator(".overview__space-open")
        offen.first.click()
        time.sleep(2.0)
        zeilen = page.locator(".list__rows > li")
        pruefe("1 Liste gerendert", zeilen.count() > 0, f"{zeilen.count()} Zeilen")
        knoepfe = page.locator(".list__row-trash")
        pruefe(
            "1 Löschknopf an eigenen Items",
            knoepfe.count() > 0 and knoepfe.count() == zeilen.count(),
            f"{knoepfe.count()} Knöpfe bei {zeilen.count()} Zeilen",
        )
        page.screenshot(path=str(OUT_DIR / "p9_step_g_01_liste.png"))

        titel = page.locator(".list__rows > li .list__row-title").first.inner_text()
        item_id = page.locator(".list__rows > li .list__row").first.get_attribute("data-id")
        pruefe("1 Ziel-Item bestimmt", bool(titel) and bool(item_id), f"{item_id} / {titel!r}")

        # --- Stufe 1: confirmDialog, Abbrechen bricht ab -------------------------------
        page.locator(".list__row-trash").first.click()
        time.sleep(0.5)
        s1_offen = page.locator("#confirm-dialog:not([hidden])").count() == 1
        s1_text = page.locator("#confirm-message").inner_text() if s1_offen else ""
        pruefe("2 Stufe 1: Rueckfrage mit Konsequenz", s1_offen and "keiner Liste" in s1_text,
               s1_text[:80])
        page.screenshot(path=str(OUT_DIR / "p9_step_g_02_stufe1_confirm.png"))
        page.locator("#confirm-cancel").click()
        time.sleep(0.5)
        status, _ = _api(args.base_url, f"/api/v1/items/{item_id}", cookie=cookie_header)
        pruefe("2 Abbrechen loescht nichts",
               status == 200 and page.locator("#confirm-dialog[hidden]").count() == 1,
               f"GET /api/v1/items/{item_id} -> {status}")

        # --- Stufe 2: Titel eintippen --------------------------------------------------
        page.locator(".list__row-trash").first.click()
        time.sleep(0.6)
        page.locator("#confirm-ok").click()
        time.sleep(0.6)
        s2_offen = page.locator("#trash-dialog:not([hidden])").count() == 1
        gesperrt_initial = page.locator("#trash-submit").is_disabled()
        pruefe("3 Stufe 2: Dialog offen, Knopf gesperrt", s2_offen and gesperrt_initial,
               f"offen={s2_offen} disabled={gesperrt_initial}")
        page.screenshot(path=str(OUT_DIR / "p9_step_g_03_stufe2_gesperrt.png"))

        # Falscher Titel: nur Grossschreibung -> bleibt gesperrt (keine Toleranz!)
        page.locator("#trash-confirm-input").fill(titel.upper())
        time.sleep(0.3)
        pruefe("4 Grossschreibung bleibt gesperrt", page.locator("#trash-submit").is_disabled())
        page.screenshot(path=str(OUT_DIR / "p9_step_g_04_falscher_titel.png"))

        # Exakter Titel -> Knopf frei
        page.locator("#trash-confirm-input").fill(titel)
        time.sleep(0.3)
        pruefe("5 Exakter Titel schaltet frei", not page.locator("#trash-submit").is_disabled())
        page.screenshot(path=str(OUT_DIR / "p9_step_g_05_richtiger_titel.png"))

        # `Origin` ist ein **verbotener Header**: der Browser setzt ihn, und weder JS noch
        # Playwright können ihn entfernen oder überschreiben (gemessen — `page.route()` bleibt
        # wirkungslos, der Server antwortet weiter 403). `serve.py` bietet keine TLS-Optionen
        # (`uvicorn.run()` ohne `ssl_*`), und eine zu ergänzen wäre eine Produktänderung
        # außerhalb dieses Steps. Deshalb der Weg, der **nichts überspringt**:
        #   Der Klick wird ausgeführt und der dabei wirklich erzeugte Request (Methode, URL,
        #   Body, Header inkl. `X-CSRF-Token`) mitgeschnitten. Genau dieser Request wird danach
        #   über `page.request` wiederholt — dieselbe Sitzung, dasselbe Token, nur ohne den
        #   erzwungenen `Origin`-Header. Der Double-Submit-Abgleich bleibt damit **voll wirksam**,
        #   und was der 403 belegt, wird protokolliert statt versteckt.
        vorher = page.locator(".list__rows > li").count()
        page.locator("#trash-submit").click()
        time.sleep(2.0)
        toast_sichtbar = page.locator(".toast").count() > 0
        dialog_zu = page.locator("#trash-dialog[hidden]").count() == 1
        pruefe("6 Klick loescht, Dialog schliesst, Toast erscheint",
               toast_sichtbar and dialog_zu, f"Toast={toast_sichtbar} Dialog-zu={dialog_zu}")

        # Nach dem Reload steht die App wieder auf der Uebersicht (der View-Zustand ist nicht
        # persistent und soll es auch nicht sein) -- also wieder in den Space, sonst zaehlte man
        # die leere Uebersicht und nicht die Liste.
        page.reload(wait_until="domcontentloaded")
        time.sleep(2.0)
        wieder = page.locator(".overview__space-open", has_text="alpha")
        (wieder.first if wieder.count() else page.locator(".overview__space-open").first).click()
        time.sleep(2.0)
        nach_reload = page.locator(".list__rows > li").count()
        pruefe("6 Zeile nach Reload weg", nach_reload == vorher - 1,
               f"{vorher} -> {nach_reload} Zeilen")
        page.screenshot(path=str(OUT_DIR / "p9_step_g_06_nach_geloescht.png"))

        # --- Gegenprobe am Server (Station 8) -------------------------------------------
        status, _ = _api(args.base_url, f"/api/v1/items/{item_id}", cookie=cookie_header)
        pruefe("8 GET auf das geloeschte Item -> 404", status == 404, f"HTTP {status}")
        browser.close()

    daten_root = Path("/tmp/opencode/p9-step-g-wegwerf/data")
    trash = sorted(daten_root.glob("._trash/**/*.md"))
    pruefe("8 Datei liegt unter ._trash", len(trash) >= 1,
           ", ".join(str(p.relative_to(daten_root)) for p in trash))

    # **Die Station, die keinen Bildschirm braucht und trotzdem die wichtigste ist.** Die
    # Unsichtbarkeit ist eine Eigenschaft des *Orts*, nicht des Löschvorgangs: `rebuild_index()`
    # liest `space_dir.rglob("*.md")` ohne Skip, ein Item an einem unbekannten Ort käme dort
    # wieder heraus. Genau das tat die Plan-Variante `<space>/_trash/`. Also wird hier ein echter
    # Neuaufbau gefahren — im Harness, nicht in einer Behauptung.
    #
    # **Im Projekt-venv als Subprozess, nicht im Playwright-venv:** das `e2e-venv` hat `playwright`,
    # aber nicht `storage` (das ist kein PyPI-Paket, sondern liegt in `phase1_storage/`). Der
    # Server selbst läuft unter `.venv`, und derselbe Interpreter soll auch den Index neu aufbauen
    # — sonst prüfte man eine andere Umgebung als die behauptete.
    import subprocess

    rebuild = subprocess.run(
        [str(REPO_ROOT / ".venv/bin/python"), "-c", REBUILD_SNIPPET, str(daten_root), titel],
        capture_output=True, text=True, cwd=str(REPO_ROOT),
        env={**os.environ, "PYTHONPATH": str(REPO_ROOT)},
    )
    try:
        ergebnis = json.loads(rebuild.stdout.strip().splitlines()[-1])
    except (ValueError, IndexError):
        ergebnis = {"fehler": (rebuild.stderr or rebuild.stdout)[-400:], "titel": [], "spaces": []}
    pruefe("8 nach rebuild_index() NICHT wieder aufgetaucht",
           not ergebnis.get("wieder_da"),
           f"'{ergebnis.get('geloescht')}' im Index? {ergebnis.get('wieder_da')} — "
           f"im Index: {ergebnis.get('titel')}")
    pruefe("8 ._trash ist kein Phantom-Space",
           ergebnis.get("spaces") == ["alpha"], f"list_spaces()={ergebnis.get('spaces')}")

    report = {
        "base_url": args.base_url,
        "item_id": item_id,
        "titel": titel,
        "befunde": befunde,
        "alle_ok": all(b["ok"] for b in befunde),
    }
    (PROBE_DIR / "p9_step_g_probe.json").write_text(json.dumps(report, indent=2, ensure_ascii=False))
    print(f"\n{sum(b['ok'] for b in befunde)}/{len(befunde)} Pruefungen gruen",
          file=sys.stderr)
    return 0 if report["alle_ok"] else 1


if __name__ == "__main__":
    raise SystemExit(main())
