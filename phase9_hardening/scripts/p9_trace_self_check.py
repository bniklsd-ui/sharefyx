#!/usr/bin/env python3
"""P9 Block trace — Browser-Selbstprüfung mit **zwei Principals** (Mini-Plan §4 T8, S1–S7).

**Kopie der Login-/API-Teile von `p9_doing_self_check.py`, kein Import** — dieselbe
Begründung wie dort: die Step-G-/doing-Skripte haengen an Modulkonstanten, ein Import wuerde
sie verbiegen.

**Warum zwei Browser-Kontexte.** Der Block behauptet zwei Dinge ueber *zwei Personen*:
`updated_by` wechselt mit dem Schreiber, `assignee` nicht. Mit einem einzigen eingeloggten
Menschen tragen beide Felder denselben Wert und jede Verwechslung bleibt unentdeckt. Der
zweite Kontext ist deshalb kein Komfort, sondern die Abnahme.

**Warum ueberhaupt ein Browser.** Kein statischer Test kann pruefen, dass `#field-assignee`
beim Statuswechsel **vor dem Speichern** gefuellt ist (S1) — das ist der Moment, an dem ein
Mensch die Regel sieht. Und S6 (Git-Autor) braucht echte Commits, S7 braucht einen Item ohne
Feld, den ein Wegwerf-Seed nur von Hand herstellen kann.

Stationen (Mini-Plan §4 T8):

  1  A waehlt „In Arbeit" → `#field-assignee` zeigt **A**, noch **vor** dem Speichern
  2  A speichert → Listenzeile „… doing · bei A", Toast
  3  B oeffnet dasselbe Item → Metazeile „bei A", Meta-Panel „Zuletzt geaendert von A"
  4  B aendert den Titel → „Zuletzt geaendert von B", `assignee` **weiter** A
  5  B zieht eine Aufgabe mit `assignee: A` auf „In Arbeit" → bleibt A (P9-Z)
  6  `git log --format=%an` im Wegwerf-`DATA_ROOT` → neuester Autor B, A unter den ersten drei
  7  Legacy-Item ohne Feld → **keine** leere Zeile, kein „undefined"

**Jede Station meldet sich selbst rot, statt die Folge zu blockieren** (Befund B4 aus dem
doing-Block: dort ist der erste Browser-Gegenlauf beim Klick auf einen Ordner, den es ohne den
Fix nicht gibt, **abgestuerzt** statt rot zu melden — ein Skript, das beim Beweis des Lochs
stirbt, beweist nichts).

Aufruf (Hard Rule 9: Stopp ausschliesslich ueber die PID-Datei des Wegwerf-Skripts):
    python phase9_hardening/scripts/p9_trace_wegwerf.py start
    ~/.claude-code-tools/e2e-venv/bin/python phase9_hardening/scripts/p9_trace_self_check.py
    python phase9_hardening/scripts/p9_trace_wegwerf.py stop
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
DEFAULT_BASE_URL = "https://127.0.0.1:18777"   # eigene TLS-Instanz, siehe Wegwerf-Docstring
DEFAULT_CREDS = Path("/tmp/opencode/p9-trace-wegwerf/credentials.json")
DEFAULT_DATA_ROOT = Path("/tmp/opencode/p9-trace-wegwerf/data")

befunde: list[dict] = []


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
        alpha_ctx = browser.new_context(viewport={"width": 1440, "height": 900},
                                        ignore_https_errors=True)
        beta_ctx = browser.new_context(viewport={"width": 1440, "height": 900},
                                       ignore_https_errors=True)
        alpha = alpha_ctx.new_page()
        beta = beta_ctx.new_page()
        for page in (alpha, beta):
            page.goto(f"{args.base_url}/ui/login", wait_until="domcontentloaded")
        # TOTP-Fenster abwarten, statt ein verbrauchtes zu senden (Login-Rate-Limit).
        time.sleep(32 - (datetime.datetime.now().second % 30))
        if not login(alpha, args.base_url, "alpha", creds["alpha"]["password"],
                     creds["alpha"]["otpauth_uri"]):
            print("Login alpha fehlgeschlagen", file=sys.stderr)
            return 2
        if not login(beta, args.base_url, "beta", creds["beta"]["password"],
                     creds["beta"]["otpauth_uri"]):
            print("Login beta fehlgeschlagen", file=sys.stderr)
            return 2
        for page in (alpha, beta):
            try:
                page.locator("#update-banner-dismiss").click(timeout=800)
            except Exception:
                pass

        # --- S1: A waehlt „In Arbeit" -> #field-assignee zeigt A, VOR dem Speichern --------
        if not _in_den_shared_space(alpha, args.base_url):
            pruefe("S1 P9-Z: #field-assignee zeigt A vor dem Speichern", False,
                   "der geteilte Space ist nicht erreichbar — kein Schreibpfad pruefbar")
            angebot_id = None
        else:
            _ordner(alpha, "Offen").first.click()
            time.sleep(1.5)
            angebot_id = _item_oeffnen(alpha, ANGEBOT)
            if angebot_id is None or not _oeffne_meta_panel(alpha):
                pruefe("S1 P9-Z: #field-assignee zeigt A vor dem Speichern", False,
                       f"Item {ANGEBOT!r} nicht in der Liste bzw. Meta-Panel zu")
            else:
                vorher = alpha.locator("#field-assignee").input_value()
                # Der Wert kommt **roh** aus `state.meta.status_values` (P9-W) — der echte
                # Optionswert, nicht das Rail-Label.
                alpha.locator("#field-status").select_option("doing")
                time.sleep(0.5)
                nachher = alpha.locator("#field-assignee").input_value()
                pruefe("S1 P9-Z: #field-assignee zeigt A vor dem Speichern",
                       vorher.strip() == "" and nachher == "alpha",
                       f"vorher={vorher!r} nachher={nachher!r}")
                alpha.screenshot(path=str(OUT_DIR / "p9_trace_01_auftrag_vor_speichern.png"))

        # --- S2: A speichert -> Listenzeile „doing · bei A" --------------------------------
        if angebot_id is None:
            pruefe("S2 Speichern: Listenzeile zeigt 'doing · bei A'", False,
                   "uebersprungen: S1 lieferte keine Item-ID")
        else:
            alpha.locator("#save-button").click()
            time.sleep(2.5)
            toast = alpha.locator(".toast").first
            toast_text = toast.inner_text().strip() if alpha.locator(".toast").count() else ""
            meta_zeile = ""
            if _ordner(alpha, "In Arbeit").count():
                _ordner(alpha, "In Arbeit").first.click()
                time.sleep(1.5)
                zeilen = alpha.locator(".list__rows > li", has_text=ANGEBOT)
                if zeilen.count():
                    meta_zeile = zeilen.first.locator(".list__row-meta").inner_text()
            pruefe("S2 Speichern: Listenzeile zeigt 'doing · bei A'",
                   "Gespeichert" in toast_text and "doing" in meta_zeile
                   and "bei alpha" in meta_zeile,
                   f"Toast={toast_text!r} Meta={meta_zeile!r}")
            alpha.screenshot(path=str(OUT_DIR / "p9_trace_02_gespeichert_liste.png"))

        # --- S3: B sieht die Aufgabe in „In Arbeit" mit beiden Angaben ---------------------
        if angebot_id is None:
            pruefe("S3 B sieht 'bei A' und 'Zuletzt geaendert von A'", False,
                   "uebersprungen: keine Item-ID")
        else:
            if not _in_den_shared_space(beta, args.base_url):
                pruefe("S3 B sieht 'bei A' und 'Zuletzt geaendert von A'", False,
                       "der geteilte Space ist fuer B nicht erreichbar")
            else:
                _ordner(beta, "In Arbeit").first.click()
                time.sleep(1.5)
                beta_zeile_meta = ""
                zeile = beta.locator(".list__rows > li", has_text=ANGEBOT)
                if zeile.count():
                    beta_zeile_meta = zeile.first.locator(".list__row-meta").inner_text()
                beta_id = zeile.first.locator(".list__row").get_attribute("data-id") \
                    if zeile.count() else None
                if beta_id is None:
                    pruefe("S3 B sieht 'bei A' und 'Zuletzt geaendert von A'", False,
                           "die Aufgabe erscheint bei B nicht unter 'In Arbeit'")
                else:
                    zeile.first.click()
                    time.sleep(1.5)
                    _oeffne_meta_panel(beta)
                    von_a = beta.locator("#meta-updated-by").inner_text().strip()
                    feld = beta.locator("#field-assignee").input_value()
                    pruefe("S3 B sieht 'bei A' und 'Zuletzt geaendert von A'",
                           "bei alpha" in beta_zeile_meta and "alpha" in von_a
                           and feld == "alpha",
                           f"Liste={beta_zeile_meta!r} Panel={von_a!r} Feld={feld!r}")
                    beta.screenshot(path=str(OUT_DIR / "p9_trace_03_ansicht_von_b.png"))

                    # --- S4: B aendert den Titel -> B ist der letzte Schreiber ---------------
                    beta.locator("#field-title").fill(f"{ANGEBOT} (neu)")
                    beta.locator("#save-button").click()
                    time.sleep(2.5)
                    _oeffne_meta_panel(beta)
                    nach_titel = beta.locator("#meta-updated-by").inner_text().strip()
                    feld_nachher = beta.locator("#field-assignee").input_value()
                    pruefe("S4 B aendert den Titel: 'Zuletzt geaendert von B', assignee bleibt A",
                           "beta" in nach_titel and "alpha" not in nach_titel
                           and feld_nachher == "alpha",
                           f"Panel={nach_titel!r} Feld={feld_nachher!r}")
                    beta.screenshot(path=str(OUT_DIR / "p9_trace_04_nach_b.png"))

        # --- S5: P9-Z an einem FREMD zugewiesenen Item -------------------------------------
        if not _in_den_shared_space(beta, args.base_url):
            pruefe("S5 P9-Z: fremd zugewiesene Aufgabe bleibt bei A", False,
                   "der geteilte Space ist fuer B nicht erreichbar")
        else:
            _ordner(beta, "Offen").first.click()
            time.sleep(1.5)
            kabel_id = _item_oeffnen(beta, KABEL)
            if kabel_id is None or not _oeffne_meta_panel(beta):
                pruefe("S5 P9-Z: fremd zugewiesene Aufgabe bleibt bei A", False,
                       f"Item {KABEL!r} nicht in der Liste bzw. Meta-Panel zu")
            else:
                vorher = beta.locator("#field-assignee").input_value()
                beta.locator("#field-status").select_option("doing")
                time.sleep(0.5)
                nachher = beta.locator("#field-assignee").input_value()
                pruefe("S5 P9-Z: fremd zugewiesene Aufgabe bleibt bei A",
                       vorher == "alpha" and nachher == "alpha",
                       f"vorher={vorher!r} nachher={nachher!r}")
                beta.screenshot(path=str(OUT_DIR / "p9_trace_05_p9z_fremd.png"))

        # --- S6: der Git-Autor im Wegwerf-DATA_ROOT -----------------------------------------
        autoren: list[str] = []
        try:
            autoren = subprocess.run(
                ["git", "-C", str(args.data_root), "log", "--format=%an", "-3"],
                capture_output=True, text=True, check=True,
            ).stdout.strip().splitlines()
        except Exception as exc:  # pragma: no cover - nur bei kaputtem Wegwerf-Setup
            pruefe("S6 Git-Autor: neuester Commit ist B, A unter den ersten drei", False,
                   f"git log schlug fehl: {exc}")
        if autoren:
            pruefe("S6 Git-Autor: neuester Commit ist B, A unter den ersten drei",
                   autoren[0] == "beta" and "alpha" in autoren[1:],
                   f"neueste drei Autoren={autoren}")

        # --- S7: Legacy-Item ohne Feld ------------------------------------------------------
        if not _in_den_shared_space(alpha, args.base_url):
            pruefe("S7 Legacy-Item: keine leere Zeile, kein 'undefined'", False,
                   "der geteilte Space ist nicht erreichbar")
        else:
            _ordner(alpha, "Notizen").first.click()
            time.sleep(1.5)
            legacy_id = _item_oeffnen(alpha, LEGACY)
            if legacy_id is None:
                pruefe("S7 Legacy-Item: keine leere Zeile, kein 'undefined'", False,
                       f"Item {LEGACY!r} nicht in der Liste")
            else:
                _oeffne_meta_panel(alpha)
                zeile = alpha.locator("#meta-updated-by").inner_text().strip()
                panel = alpha.locator("#meta-panel").inner_text()
                listen_zeile = alpha.locator(".list__rows > li", has_text=LEGACY).first
                listen_meta = listen_zeile.locator(".list__row-meta").inner_text() \
                    if listen_zeile.count() else ""
                pruefe("S7 Legacy-Item: keine leere Zeile, kein 'undefined'",
                       zeile == "" and "undefined" not in panel and "bei " not in listen_meta,
                       f"Panel={zeile!r} Liste={listen_meta!r}")
                alpha.screenshot(path=str(OUT_DIR / "p9_trace_06_legacy_ohne_feld.png"))

        # --- S7b: die API fuehrt dasselbe (kein reines Anzeige-Feld) -------------------------
        status, raw = _api(args.base_url, "/api/v1/items?space=team", cookie=_cookie_header(beta))
        items = json.loads(raw).get("items", []) if status == 200 else []
        zuweisung = next((i for i in items if i["title"].startswith(ANGEBOT)), {})
        pruefe("S7b API: updated_by=B, assignee=alpha am selben Item",
               status == 200 and zuweisung.get("updated_by") == "beta"
               and zuweisung.get("assignee") == "alpha",
               f"HTTP {status} updated_by={zuweisung.get('updated_by')!r} "
               f"assignee={zuweisung.get('assignee')!r}")

        browser.close()

    report = {
        "base_url": args.base_url,
        "data_root": str(args.data_root),
        "befunde": befunde,
        "alle_ok": all(b["ok"] for b in befunde),
    }
    (PROBE_DIR / "p9_trace_probe.json").write_text(
        json.dumps(report, indent=2, ensure_ascii=False))
    print(f"\n{sum(b['ok'] for b in befunde)}/{len(befunde)} Pruefungen gruen", file=sys.stderr)
    return 0 if report["alle_ok"] else 1


if __name__ == "__main__":
    raise SystemExit(main())
