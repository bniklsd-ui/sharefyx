#!/usr/bin/env python3
"""P9 Block feedback — Browser-Selbstpruefung mit **zwei Principals** (Mini-Plan B1, P9-BG/BI).

**Kopie der Login-/Navigations-Helfer aus `p9_trace_self_check.py`, kein Import** (gleiche
Begruendung dort). Der Bug R2: Anlegen im fremden, schreibbaren Space landete im Home-Space.

Stationen:
  1  A legt im Team-Space eine Notiz an -> API: `space == team`, Git-Autor alpha, die UI steht
     danach **im Team-Space** (`state.activeSpace`), das Item steht in dessen Liste
  2  Gegenlauf: dasselbe Item steht **nicht** im Home-Space von A
  3  Home-Space: Anlegen dort bleibt im Home-Space (unveraendertes Verhalten, P9-122)
  4  (B2, P9-BH) der offene Anlegen-Dialog nennt sein Ziel: im Team-Space ``team``, im
     Home-Space ``alpha`` mit Home-Vermerk — gelesen **vor** dem Absenden, im echten Dialog
  5  (B2) Messung, kein Urteil: nach team -> Uebersicht (`#home-button`) — ist ein Anlegen-Knopf
     sichtbar, und wenn ja, welches Ziel nennt der Dialog? (`state.activeSpace` bleibt in der
     Uebersicht absichtlich stehen, `tree.js:66`.) Die Station meldet den Befund nur.
  6  (E1a, P9-BP/BQ) im Team-Space loescht alpha ein Item, das **beta** angelegt hat, ueber den
     echten Zwei-Schritt-Dialog; der Dialog nennt `beta`, der Papierkorb-Commit traegt `alpha`
  7  (E1a) alpha zieht ein beta-Item per **echter Maus** auf den Team-Ordner `ablage`
  8  (E1a) Freigeben bleibt beim eigenen Space: Team-Zeilen haben keinen Freigeben-Knopf
  9  (B3, P9-BN) Einstellungen + Update-Log offen -> „Schliessen" im Menue -> Overlay und alle
     Panels `hidden`
 10  (B4, P9-BM) Spaces verwalten -> `team` -> der gemessene Abstand zwischen zwei Mitgliederzeilen
     ist `--space`. `team` traegt aus dem Seed zwei Mitglieder (alpha, beta), die Liste ist also
     im Harness erstmals **gefuellt** — das ist die Grenze aus P9-107/P9-110, jetzt geschlossen

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


def _anlegen(page: Page, titel: str, bild: str | None = None) -> str | None:
    """Legt an und liefert die Zielzeile des offenen Dialogs (B2), gelesen **vor** dem Absenden.
    `None`, wenn es die Zeile nicht gibt — der alte Client hat keine."""
    page.locator("#create-button:visible, #new-item-button:visible").first.click()
    ziel = page.locator("#create-target")
    ziel_text = ziel.text_content() if ziel.count() else None
    if bild:
        page.locator("#create-dialog .overlay__panel").screenshot(path=str(OUT_DIR / bild))
    page.locator("#create-title-input").fill(titel)
    page.locator("#create-submit").click()
    time.sleep(2.5)
    return ziel_text


def _git_autor(data_root: Path) -> str:
    return subprocess.run(["git", "-C", str(data_root), "log", "--format=%an", "-1"],
                          capture_output=True, text=True, check=False).stdout.strip()


def _team_item(base_url: str, page: Page, titel: str) -> dict | None:
    status, raw = _api(base_url, "/api/v1/items?space=team", cookie=_cookie_header(page))
    treffer = [i for i in json.loads(raw).get("items", []) if i["title"] == titel] \
        if status == 200 else []
    return treffer[0] if treffer else None


def _e1a(page: Page, args) -> None:
    # S8 zuerst: es braucht nur die Liste, und ein Loeschen danach aendert sie.
    zeilen = page.locator(".list__rows > li").filter(has_text="E1a ")
    teilen = page.locator(".list__rows > li").filter(has_text="E1a ").locator(".list__row-share").count()
    loeschen = zeilen.locator(".list__row-trash").count()
    pruefe("S8 Team-Zeilen: Loeschen ja, Freigeben nein",
           zeilen.count() == 2 and loeschen == 2 and teilen == 0,
           f"Zeilen={zeilen.count()} Loeschknoepfe={loeschen} Freigabeknoepfe={teilen}")

    # S6: Loeschen eines beta-Items durch alpha
    vorher = _team_item(args.base_url, page, "E1a Loeschen")
    zeile = page.locator(".list__rows > li").filter(has_text="E1a Loeschen")
    hinweis = None
    if zeile.locator(".list__row-trash").count():
        zeile.locator(".list__row-trash").click()
        page.locator("#confirm-ok").click()
        hinweis = page.locator("#trash-consequence").text_content()
        page.locator("#trash-dialog .overlay__panel").screenshot(
            path=str(OUT_DIR / "p9_feedback_e1a_loeschen.png"))
        page.locator("#trash-confirm-input").fill("E1a Loeschen")
        page.locator("#trash-submit").click()
        time.sleep(2.0)
    nachher = _team_item(args.base_url, page, "E1a Loeschen")
    autor = _git_autor(args.data_root)
    pruefe("S6 alpha loescht im Team-Space ein Item von beta",
           vorher is not None and vorher.get("updated_by") == "beta" and nachher is None,
           f"vorher updated_by={vorher and vorher.get('updated_by')!r} danach vorhanden={nachher is not None}")
    pruefe("S6b der Loeschdialog nennt beta, der Papierkorb-Commit traegt alpha",
           bool(hinweis) and "Zuletzt geändert von beta" in hinweis and autor == "alpha",
           f"Hinweis={hinweis!r} Git-Autor={autor!r}")

    # S7: Drag & Drop eines beta-Items auf den Team-Ordner
    quelle = page.locator(".list__rows > li").filter(has_text="E1a Ziehen")
    ziel = page.locator('.tree__realfolder[data-space="team"][data-folder="ablage"]')
    if quelle.count() and ziel.count():
        quelle.first.drag_to(ziel.first)
        time.sleep(2.0)
    item = _team_item(args.base_url, page, "E1a Ziehen")
    pruefe("S7 alpha zieht ein beta-Item per Maus in den Team-Ordner",
           item is not None and item.get("folder") == "ablage",
           f"Quelle={quelle.count()} Ziel={ziel.count()} folder={item and item.get('folder')!r}")


def _b3(page: Page) -> None:
    knopf = page.locator("#settings-menu-close")
    if knopf.count() == 0:
        pruefe("S9 Schliessen im Einstellungsmenue schliesst die ganze Kette", False,
               "kein Schliessen-Knopf im Menue")
        return
    page.locator("#account-button").click()
    time.sleep(0.6)
    page.locator("#account-show-updates").click()
    time.sleep(0.8)
    offen = page.evaluate("""[...document.querySelectorAll('#settings-overlay .settings-panel')]
        .filter(p => !p.hidden).length""")
    page.locator("#settings-menu .overlay__panel, #settings-menu").first.screenshot(
        path=str(OUT_DIR / "p9_feedback_b3_menue.png"))
    knopf.click()
    time.sleep(0.6)
    zu = page.evaluate("""({overlay: document.getElementById('settings-overlay').hidden,
        offen: [...document.querySelectorAll('#settings-overlay .settings-panel')]
        .filter(p => !p.hidden).length})""")
    pruefe("S9 Schliessen im Einstellungsmenue schliesst die ganze Kette",
           offen >= 2 and zu["overlay"] is True,
           f"vorher offene Panels={offen} danach Overlay hidden={zu['overlay']} offene Panels={zu['offen']}")


def _b4(page: Page) -> None:
    page.locator("#account-button").click()
    time.sleep(0.6)
    page.locator("#account-manage-spaces").click()
    time.sleep(0.8)
    zeile = page.locator(".settings-space-row").filter(has_text="team")
    if zeile.count() == 0:
        pruefe("S10 Mitgliederzeilen haben den Standardabstand", False, "keine Space-Zeile `team`")
        return
    zeile.first.click()
    time.sleep(1.2)
    m = page.evaluate("""() => {
        const r2 = (v) => Math.round(v * 100) / 100;
        const liste = document.getElementById('space-member-list');
        const zeilen = [...liste.querySelectorAll(':scope > li')].map(li => li.getBoundingClientRect());
        const probe = document.createElement('div');
        probe.style.cssText = 'position:absolute;visibility:hidden;width:var(--space)';
        document.body.appendChild(probe);
        const space = probe.getBoundingClientRect().width;
        probe.remove();
        return {n: zeilen.length, space: r2(space),
                abstaende: zeilen.slice(1).map((b, i) => r2(b.top - zeilen[i].bottom))};
    }""")
    k = page.evaluate("""() => {
        const r2 = (v) => Math.round(v * 100) / 100;
        const hinzu = document.getElementById('space-member-add-submit').getBoundingClientRect();
        const zeilen = [...document.querySelectorAll('#space-member-list > li')]
          .filter(li => li.querySelector('button'));
        return {rechts_hinzu: r2(hinzu.right), zeilen: zeilen.map(li => {
          const t = li.querySelector('span').getBoundingClientRect();
          const b = li.querySelector('button').getBoundingClientRect();
          return {rechts: r2(b.right), abstand: r2(b.left - t.right)}; })};
    }""")
    pruefe("S10b Entfernen-Knoepfe sitzen rechtsbuendig auf der Kante von „Hinzufuegen“, Abstand zum Text >= --space",
           len(k["zeilen"]) >= 2 and all(abs(z["rechts"] - k["rechts_hinzu"]) <= 1 and z["abstand"] >= m["space"]
                                         for z in k["zeilen"]),
           f"Hinzufuegen rechts={k['rechts_hinzu']} Zeilen={k['zeilen']}")
    page.locator("#settings-space-detail").screenshot(path=str(OUT_DIR / "p9_feedback_b4_mitglieder.png"))
    pruefe("S10 Mitgliederzeilen haben den Standardabstand (--space)",
           m["n"] >= 2 and m["space"] > 0 and all(abs(a - m["space"]) <= 0.5 for a in m["abstaende"]),
           f"Zeilen={m['n']} --space={m['space']} px Abstaende={m['abstaende']}")
    page.locator("#settings-menu-close").click()
    time.sleep(0.6)


def main() -> int:
    global OUT_DIR
    ap = argparse.ArgumentParser()
    ap.add_argument("--base-url", default=DEFAULT_BASE_URL)
    ap.add_argument("--creds", type=Path, default=DEFAULT_CREDS)
    ap.add_argument("--data-root", type=Path, default=DEFAULT_DATA_ROOT)
    # Getrennter Bericht fuer Gegenlaeufe, damit kein Gegenlauf den Erfolgsbeleg ueberschreibt
    # (derselbe Fehler wie im trace-Block 2026-10-02). Die B1-Belege bleiben als Stand von B1 liegen.
    ap.add_argument("--report", type=Path, default=PROBE_DIR / "p9_feedback_b4_probe.json")
    ap.add_argument("--screenshots-dir", type=Path, default=OUT_DIR)
    args = ap.parse_args()
    OUT_DIR = args.screenshots_dir
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
            ziel = _anlegen(alpha, TEAM_TITEL, bild="p9_feedback_b2_ziel_team.png")
            pruefe("S4 der Anlegen-Dialog nennt den Team-Space als Ziel",
                   ziel == "Anlegen in: team", f"Zielzeile={ziel!r}")
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

        # --- S6–S8: E1a im Team-Space --------------------------------------------------------
        if _in_den_shared_space(alpha, args.base_url):
            _e1a(alpha, args)

        # --- S5: Uebersicht nach team — Messung, kein Urteil ---------------------------------
        if _in_den_shared_space(alpha, args.base_url):
            alpha.locator("#home-button").click()
            time.sleep(1.2)
            knoepfe = alpha.locator("#create-button:visible, #new-item-button:visible").count()
            ziel = None
            if knoepfe:
                alpha.locator("#create-button:visible, #new-item-button:visible").first.click()
                ziel = alpha.locator("#create-target").text_content() \
                    if alpha.locator("#create-target").count() else None
                alpha.locator("#create-cancel").click()
            befunde.append({"pruefung": "S5 Messung: Anlegen-Knopf in der Uebersicht nach team",
                            "ok": True, "messung": True,
                            "detail": f"sichtbare Knoepfe={knoepfe} Zielzeile={ziel!r}"})
            print(f"  [MESS] S5 Uebersicht nach team: Knoepfe={knoepfe} Zielzeile={ziel!r}",
                  file=sys.stderr)

        # --- S9: Schliessen im Einstellungsmenue (B3) ------------------------------------------
        _b3(alpha)

        # --- S10: Abstand der Mitgliederzeilen (B4) ------------------------------------------
        _b4(alpha)

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
            ziel = _anlegen(alpha, HOME_TITEL)
            pruefe("S4b der Anlegen-Dialog nennt im Home-Space den Home-Space als Ziel",
                   ziel == "Anlegen in: alpha (dein Home-Space)", f"Zielzeile={ziel!r}")
            status, raw = _api(args.base_url, "/api/v1/items?space=alpha", cookie=_cookie_header(alpha))
            home = [i for i in json.loads(raw).get("items", []) if i["title"] == HOME_TITEL] \
                if status == 200 else []
            pruefe("S3 Anlegen im Home-Space bleibt im Home-Space",
                   len(home) == 1 and home[0]["space"] == "alpha",
                   f"HTTP {status} Treffer={len(home)}")

        browser.close()

    report = {"base_url": args.base_url, "befunde": befunde,
              "alle_ok": all(b["ok"] for b in befunde)}
    args.report.write_text(
        json.dumps(report, indent=2, ensure_ascii=False))
    print(f"\n{sum(b['ok'] for b in befunde)}/{len(befunde)} Pruefungen gruen", file=sys.stderr)
    return 0 if report["alle_ok"] else 1


if __name__ == "__main__":
    raise SystemExit(main())
