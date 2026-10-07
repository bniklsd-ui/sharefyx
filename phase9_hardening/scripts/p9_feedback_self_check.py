#!/usr/bin/env python3
"""P9 Block feedback — Browser-Selbstpruefung mit **zwei Principals** (Mini-Plan B1, P9-BG/BI).

**Kopie der Login-/Navigations-Helfer aus `p9_trace_self_check.py`, kein Import** (gleiche
Begruendung dort). Der Bug R2: Anlegen im fremden, schreibbaren Space landete im Home-Space.

Stationen:
  1  A legt im Team-Space eine Notiz an -> API: `space == team`, Git-Autor alpha, die UI steht
     danach **im Team-Space** (`state.activeSpace`), das Item steht in dessen Liste
  2  Gegenlauf: dasselbe Item steht **nicht** im Home-Space von A
  3  Home-Space: Anlegen dort bleibt im Home-Space (unveraendertes Verhalten, P9-122)

Aufruf (Stopp nur ueber die PID-Datei, Hard Rule 9):
    python phase9_hardening/scripts/p9_feedback_wegwerf.py start
    ~/.claude-code-tools/e2e-venv/bin/python phase9_hardening/scripts/p9_feedback_self_check.py
    python phase9_hardening/scripts/p9_feedback_wegwerf.py stop
"""
from __future__ import annotations

import argparse
import base64
import datetime
import hashlib
import hmac
import json
import struct
import subprocess
import sys
import time
import urllib.error
import urllib.parse
import urllib.request
from pathlib import Path

from playwright.sync_api import Page, sync_playwright

REPO_ROOT = Path(__file__).resolve().parents[2]
OUT_DIR = REPO_ROOT / "docs" / "screenshots"
PROBE_DIR = REPO_ROOT / "phase9_hardening" / "probes"
DEFAULT_BASE_URL = "https://127.0.0.1:18778"   # eigene TLS-Instanz, siehe Wegwerf-Docstring
DEFAULT_CREDS = Path("/tmp/opencode/p9-feedback-wegwerf/credentials.json")
DEFAULT_DATA_ROOT = Path("/tmp/opencode/p9-feedback-wegwerf/data")

befunde: list[dict] = []
TEAM_TITEL = "B1 Team-Notiz"
HOME_TITEL = "B1 Home-Notiz"
TEAM_SPACE = "team"




def pruefe(name: str, ok: bool, detail: str = "") -> None:
    befunde.append({"pruefung": name, "ok": bool(ok), "detail": detail})
    print(f"  [{'OK ' if ok else 'FEHLER'}] {name}" + (f" — {detail}" if detail else ""),
          file=sys.stderr)


# --- TOTP/Login (entliehen aus p9_doing_self_check.py) --------------------------------------

#: Fachliche Namen, nicht aus dem Skript erfunden: die Itemsamen stehen im Wegwerf-Seed.
ANGEBOT = "Angebot schreiben"
KABEL = "Kabel suchen"
LEGACY = "Legacy-Notiz"


def _generate_totp(otpauth_uri: str) -> str:
    qs = urllib.parse.parse_qs(urllib.parse.urlparse(otpauth_uri).query)
    secret_b32 = qs["secret"][0]
    key = base64.b32decode(secret_b32 + "=" * (-len(secret_b32) % 8))
    msg = struct.pack(">q", int(time.time() // 30))
    h = hmac.new(key, msg, hashlib.sha1).digest()
    offset = h[-1] & 0x0F
    return f"{(struct.unpack('>I', h[offset:offset + 4])[0] & 0x7FFFFFFF) % 1000000:06d}"


def login(page: Page, base_url: str, space: str, password: str, otpauth_uri: str) -> bool:
    for _fenster in range(2):
        page.goto(f"{base_url}/ui/login", wait_until="domcontentloaded")
        page.locator('input[name="space"]').fill(space)
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
    """Rohzugriff auf die eigene API — dieselbe Sitzung wie der Browser. `unverified` betrifft
    nur das selbstsignierte Harness-Zertifikat; am Server aendert das nichts. Nur fuer
    **GET**-Gegenproben benutzt, nie fuer einen Schreibvorgang."""
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


def _cookie_header(page: Page) -> str:
    return "; ".join(f"{c['name']}={c['value']}" for c in page.context.cookies())


def _in_den_shared_space(page: Page, base_url: str) -> bool:
    """Wechselt **idempotent** in den geteilten Space und wartet auf den Listen-Slot.

    **Zwei Dinge, die dieser Aufruf zuerst abstuerzen musste, beide gemessen, nicht vermutet:**
    1. `.overview__space-open` traegt **kein** `data-space`-Attribut (gemessen: `None`) und
       der Name steht in einem eigenen `.overview__space-name-label` — der Selektor aus dem
       doing-Skript (`[data-space="alpha"], .overview__space-open`) fiel also auf die
       Textsuche zurueck. Der Label-Selektor ist enger: `has_text="team"` matcht auch die
       eigene Space-Zeile, sobald ein Space-Name das andere als Teilstring enthaelt.
    2. Ein zweiter Aufruf **ohne** vorherigen Weg zur Uebersicht scheitert mit einem
       30-Sekunden-Click-Timeout, weil der Overview-Slot dann `hidden` ist — das Skript
       waere beim Beweis abgestuerzt statt rot zu melden (Befund B4 aus dem doing-Block).
       Deshalb: erst `#home-button` (Uebersicht), dann die Space-Zeile.
    """
    try:
        page.locator("#home-button").click(timeout=5000)
        time.sleep(1.2)
    except Exception:
        pass
    zeile = page.locator(".overview__space-open").filter(
        has=page.locator('.overview__space-name-label:text-is("team")')
    )
    if zeile.count() == 0:
        zeile = page.locator(".overview__space-open").filter(has_text="team")
    if zeile.count() == 0:
        return False
    try:
        zeile.first.click(timeout=5000)
    except Exception:
        return False
    time.sleep(2.0)
    # **Der Rail-Knoten eines fremden Spaces ist zunächst zugeklappt.** `renderSpaceNode()`
    # rendert die Eimer nur, wenn `space.own` oder `state.expanded[name] === true` ist — fuer
    # den eigenen Space ist das immer wahr, fuer `team` nie ohne Klick. Gemessen, nicht
    # angenommen: der erste Lauf fand nach dem Space-Wechsel **null** Eimer-Knoepfe.
    if page.locator('.tree__folder[data-space="team"][data-bucket]').count() == 0:
        knoten = page.locator(".tree__space").filter(
            has=page.locator('.rail__label:text-is("team")')
        )
        if knoten.count() == 0:
            return False
        try:
            knoten.first.click(timeout=5000)
        except Exception:
            return False
        time.sleep(1.2)
    return page.locator('.tree__folder[data-space="team"][data-bucket]').count() > 0


def _ordner(page: Page, label: str):
    return page.locator('.tree__folder[data-space="team"][data-bucket]').filter(
        has=page.locator(f'.rail__label:text-is("{label}")')
    )


def _oeffne_meta_panel(page: Page) -> bool:
    """`#meta-panel` ist ein `<details>` und klappt sich beim Editor-Oeffnen nicht auf.
    Explizit aufklappen — sonst liefe `select_option` ins Leere und der Fehler laege
    scheinbar am Status statt am Panel."""
    try:
        page.locator("#meta-panel:not([open]) summary").click(timeout=1500)
    except Exception:
        pass
    time.sleep(0.4)
    return page.locator("#meta-panel[open]").count() == 1


def _item_oeffnen(page: Page, titel: str) -> str | None:
    """Klickt eine Listenzeile an und liefert die Item-ID (oder `None`, wenn es sie nicht
    gibt). Weich aus demselben Grund wie `_in_den_shared_space`."""
    zeile = page.locator(".list__rows > li", has_text=titel).first
    if zeile.count() == 0:
        return None
    item_id = zeile.locator(".list__row").get_attribute("data-id")
    zeile.click()
    time.sleep(1.5)
    return item_id


def _anlegen(page: Page, titel: str) -> None:
    page.locator("#create-button:visible, #new-item-button:visible").first.click()
    page.locator("#create-title-input").fill(titel)
    page.locator("#create-submit").click()
    time.sleep(2.5)


def main() -> int:
    ap = argparse.ArgumentParser()
    ap.add_argument("--base-url", default=DEFAULT_BASE_URL)
    ap.add_argument("--creds", type=Path, default=DEFAULT_CREDS)
    ap.add_argument("--data-root", type=Path, default=DEFAULT_DATA_ROOT)
    args = ap.parse_args()
    OUT_DIR.mkdir(parents=True, exist_ok=True)
    PROBE_DIR.mkdir(parents=True, exist_ok=True)

    creds = json.loads(args.creds.read_text())
    with sync_playwright() as pw:
        browser = pw.chromium.launch()
        ctx = browser.new_context(viewport={"width": 1440, "height": 900},
                                  ignore_https_errors=True)
        alpha = ctx.new_page()
        alpha.goto(f"{args.base_url}/ui/login", wait_until="domcontentloaded")
        time.sleep(32 - (datetime.datetime.now().second % 30))
        if not login(alpha, args.base_url, "alpha", creds["alpha"]["password"],
                     creds["alpha"]["otpauth_uri"]):
            print("Login alpha fehlgeschlagen", file=sys.stderr)
            return 2
        try:
            alpha.locator("#update-banner-dismiss").click(timeout=800)
        except Exception:
            pass

        # --- S1: Anlegen im Team-Space ------------------------------------------------------
        if not _in_den_shared_space(alpha, args.base_url):
            pruefe("S1 Anlegen im Team-Space landet im Team-Space", False,
                   "der geteilte Space ist nicht erreichbar")
        else:
            _anlegen(alpha, TEAM_TITEL)
            aktiv = alpha.evaluate("document.querySelector('#list-title, .list__title')?.textContent || ''")
            status, raw = _api(args.base_url, "/api/v1/items?space=team", cookie=_cookie_header(alpha))
            team = [i for i in json.loads(raw).get("items", []) if i["title"] == TEAM_TITEL] \
                if status == 200 else []
            autoren = subprocess.run(
                ["git", "-C", str(args.data_root), "log", "--format=%an", "-1"],
                capture_output=True, text=True, check=False).stdout.strip()
            in_liste = alpha.locator(".list__rows > li", has_text=TEAM_TITEL).count()
            pruefe("S1 Anlegen im Team-Space landet im Team-Space",
                   len(team) == 1 and team[0]["space"] == "team" and autoren == "alpha",
                   f"HTTP {status} Treffer={len(team)} Git-Autor={autoren!r}")
            pruefe("S1b danach steht die UI im Team-Space (Item in der Liste)",
                   in_liste >= 1, f"Zeilen mit Titel={in_liste} Kopf={aktiv!r}")
            alpha.screenshot(path=str(OUT_DIR / "p9_feedback_b1_team.png"))

            # --- S2: Gegenlauf — nicht im Home-Space ---------------------------------------
            status, raw = _api(args.base_url, "/api/v1/items?space=alpha", cookie=_cookie_header(alpha))
            home = [i for i in json.loads(raw).get("items", []) if i["title"] == TEAM_TITEL] \
                if status == 200 else ["?"]
            pruefe("S2 Gegenlauf: das Team-Item steht nicht im Home-Space",
                   status == 200 and home == [], f"HTTP {status} Treffer im Home={len(home)}")

        # --- S3: Anlegen im Home-Space bleibt im Home-Space ----------------------------------
        alpha.locator("#home-button").click()
        time.sleep(1.2)
        eigen = alpha.locator(".overview__space-open").filter(
            has=alpha.locator('.overview__space-name-label:text-is("alpha")'))
        if eigen.count() == 0:
            pruefe("S3 Anlegen im Home-Space bleibt im Home-Space", False, "Home-Zeile fehlt")
        else:
            eigen.first.click()
            time.sleep(2.0)
            _anlegen(alpha, HOME_TITEL)
            status, raw = _api(args.base_url, "/api/v1/items?space=alpha", cookie=_cookie_header(alpha))
            home = [i for i in json.loads(raw).get("items", []) if i["title"] == HOME_TITEL] \
                if status == 200 else []
            pruefe("S3 Anlegen im Home-Space bleibt im Home-Space",
                   len(home) == 1 and home[0]["space"] == "alpha",
                   f"HTTP {status} Treffer={len(home)}")

        browser.close()

    report = {"base_url": args.base_url, "befunde": befunde,
              "alle_ok": all(b["ok"] for b in befunde)}
    (PROBE_DIR / "p9_feedback_b1_probe.json").write_text(
        json.dumps(report, indent=2, ensure_ascii=False))
    print(f"\n{sum(b['ok'] for b in befunde)}/{len(befunde)} Pruefungen gruen", file=sys.stderr)
    return 0 if report["alle_ok"] else 1


if __name__ == "__main__":
    raise SystemExit(main())
