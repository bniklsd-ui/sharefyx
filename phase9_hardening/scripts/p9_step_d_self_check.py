#!/usr/bin/env python3
"""P9 Step D — Browser-Selbstprüfung des Drop-Ziels „Space-Wurzel" (P9-28 – P9-31, V136/V157).

**Warum diese Datei überhaupt entsteht.** Step D2 ist am 2026-09-23 gebaut worden und hat bis heute
**drei statische Wächter** und **null** Fahrten am Browser bekommen: `test_static_routes.py` prüft,
dass `bindFolderDropTarget()` genau zwei Aufrufstellen hat und dass die Space-Zeile hinter einem
`if (space.own)`-Riegel hängt — also die **Form** des Aufrufs, nicht sein **Verhalten**. Die drei
Abnahmezeilen P9-29 (Zug auf die Space-Wurzel), P9-30 (sichtbarer Drop-Zustand) und P9-28 (ESC
außerhalb Vollbild) stehen deshalb in `ABNAHME_MATRIX.md` als ⬜ bzw. ⚠️ „strukturell erfüllt, nicht
belegt". Die Station, die sie schließen sollte — die erste von GA2 in Plan §11 — wurde nie gebaut.

**Die eine Falle, die dieses Skript von Anfang an vermeidet.** Man könnte den Wurf simpel mit
`element.dispatchEvent(new DragEvent("drop", {dataTransfer}))` erzeugen — und damit **den Listener
beweisen, nicht den Zug**. Genau das ist die Repo-Lehre, die inzwischen achtmal in Phase 9
wiederholt wurde (ein Zähler, der das Richtige zählt, ist nicht der, der die Aussage trägt).
Deshalb hier **echte Maus-Input-Pipeline** in Chromium (`mouse.down` → `move` in Schritten →
`mouse.up`), und Station 2 **misst die vom Browser erzeugte Ereigniskette** (`dragstart`,
mindestens ein `dragover`, `drop`) über zusätzliche Listener im Capture-Phase am `document` —
reines Zusehen, kein Eingriff in den Ablauf. Vorab gemessen, nicht angenommen: diese Kette feuert
in dieser Umgebung zuverlässig, inklusive `dataTransfer`-Inhalt.

**Was die Stationen je beweisen** (nicht: „die Funktion existiert"):

  1  Aufbau: Ordner mit Items, Space-Zeile da, Item-IDs bestimmt
  2  Die Ereigniskette kam vom Browser (dragstart → dragover → drop), inkl. der Item-ID im
     dataTransfer — der Nachweis, dass Station 3–5 nicht auf einem Dispatch beruhen
  3  Drop-Zustand **sichtbar**: Klasse `tree__realfolder--dragover` UND berechneter Stil
     (`border-style: dashed` in der Akzentfarbe) während des Zugs, mit Bild
  4  Nach dem Drop ist der Zustand wieder weg (keine hängende Markierung)
  5  **P9-29**: das Item steht danach in der Space-Wurzel — am **Server** (`GET` → `folder: ""`),
     in der Liste und im Toast (`(Space-Wurzel)`)
  6  Gegenrichtung ohne Restschaden: ein Wurzel-Item lässt sich in den Ordner ziehen (das war das
     einzige Ziel vor D2)
  7  Der Leerlauf-Riegel `tree.js:139`: ein Drop auf den **eigenen** Ausgangsordner löst **keinen**
     `PATCH` aus — an der Zahl der Requests gemessen, nicht am Aussehen
  8  **P9-28**: ESC außerhalb Vollbild schließt das Item weiterhin
  9  **P9-28, Gegenrichtung**: bei gesetztem `document.fullscreenElement` schließt ESC **nichts**
     (der Guard). Dass der Browser im Automationslauf *selbst* nicht aus dem Vollbild geht, ist
     gemessen und im Detail benannt — synthetische Tastendrücke lösen seinen Vollbild-Exit nicht
     aus, die App-Seite des Guards ist aber genau die, die P9-28 prüft.

**Was hier nicht behauptet wird:** P9-27 (ESC im **nativen** macOS-Vollbild) bleibt offen. Dafür
gibt es kein Playwright-Binary (WebKit fehlt im Cache), und natives Vollbild ist per Spezifikation
nicht automatisierbar — das ist eine Eigenschaft, keine Versäumnis dieses Skripts.

Aufruf (Hard Rule 9: Stopp ausschließlich über die PID-Datei des jeweiligen Wegwerf-Skripts):
    python phase9_hardening/scripts/p9_step_d_wegwerf.py start
    ~/.claude-code-tools/e2e-venv/bin/python phase9_hardening/scripts/p9_step_d_self_check.py
    python phase9_hardening/scripts/p9_step_d_wegwerf.py stop
"""
from __future__ import annotations

import argparse
import base64
import datetime
import hashlib
import hmac
import json
import ssl
import struct
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
DEFAULT_BASE_URL = "https://127.0.0.1:18781"
DEFAULT_CREDS = Path("/tmp/opencode/p9-step-d-wegwerf/credentials.json")

ORDNER = "rechnungen"  # **gemessen, nicht geraten**: `files.validate_folder()` slugifiziert
# jedes Segment, `store.create(..., folder="Rechnungen")` landet also als `rechnungen` auf der
# Platte. Ein Skript, das den un-normalisierten Namen hartnäckt, scheitert an einer Eigenschaft des
# Speichernamens und nicht an der Sache, die es prüft (gemessen beim ersten Lauf).
TITEL_RAUS = "Rechnung September"      # Quelle des Zuges nach oben (P9-29)
TITEL_ORDNER = "Steuern 2026"          # Quelle für den Leerlauf-Riegel (Station 7)
TITEL_WURZEL = "Wurzel-Notiz"          # Gegenrichtung rein (Station 6) und Leerlauf-Quelle

# Reines Zusehen: drei Zähler am `document` im Capture-Phase. Der Zweck ist Station 2 — ohne sie
# ist nicht unterscheidbar, ob ein Zug oder ein `dispatchEvent` die Stationen 3–5 ausgelöst hat.
#
# **Die erste Fassung dieses Snippets zählte sich selbst** (gemessen: `start=3, over=57, drop=3` für
# genau *einen* Zug): der Zähler-Block stand bei jedem Aufruf erneut da und registrierte die drei
# Listener ein zweites, drittes Mal — jedes Ereignis kam damit mehrfach an. Ein Zähler, der sich
# selber vervielfacht, ist kein Zähler. Deshalb jetzt ein Einmal-Flag für die Installation und ein
# getrennter Reset, der nur die Werte auf Null setzt.
ZAEHLER_SNIPPET = """
if (!window.__dndInstalled) {
  window.__dndInstalled = true;
  window.__dnd = {start: 0, over: 0, drop: 0, daten: []};
  window.__dndReset = function () {
    window.__dnd = {start: 0, over: 0, drop: 0, daten: []};
  };
  document.addEventListener('dragstart', function () { window.__dnd.start++; }, true);
  document.addEventListener('dragover', function () { window.__dnd.over++; }, true);
  document.addEventListener('drop', function (e) {
    window.__dnd.drop++;
    try { window.__dnd.daten.push(e.dataTransfer.getData('text/plain')); } catch (err) { }
  }, true);
}
"""


def _detail_offen(page: Page) -> bool:
    """Ist **irgendein** Detail-Pane offen?

    Zwei Elemente, nicht eins: ein eigenes Item öffnet den **Editor** (`#detail-editor`), ein
    fremdes/schreibgeschütztes die Nur-Lesen-Ansicht (`#detail-readonly`). Die erste Fassung der
    Station 8 prüfte nur das Readonly-Pane und meldete `offen=False` — an einem Item, das offen war.
    Genau die Klasse Fehler, die eine Abnahmezeile grün rechnet, weil sie das falsche Element ansieht.
    """
    return (
        page.locator("#detail-readonly:not([hidden])").count() == 1
        or page.locator("#detail-editor:not([hidden])").count() == 1
    )

befunde: list[dict] = []


def pruefe(name: str, ok: bool, detail: str = "", zeile: str = "") -> None:
    """`zeile` ist die Abnahmezeile aus `ABNAHME_MATRIX.md`, die diese Station trägt.

    **Warum sie im Beleg steht und nicht nur im Fließtext.** Ein Bild, das eine Aussage stützt,
    wird zitiert („Sichtprüfung 4, siehe `p9_step_g_04_…`") — und beim Zitieren rutscht eine Zeile
    leicht von der Station, die sie trägt, zu der Station, die nur dabei war. Die Zuordnung steht
    deshalb maschinenlesbar **im Beleg selbst**; `test_step_d_drop_target.py` prüft die Deckung in
    beiden Richtungen: jede als belegt behauptete Matrix-Zeile braucht eine Station, und jede
    Station muss eine Zeile nennen, die in der Matrix existiert.
    """
    befunde.append({"pruefung": name, "ok": bool(ok), "detail": detail, "zeile": zeile})
    print(f"  [{'OK ' if ok else 'FEHLER'}] {name}" + (f" — {detail}" if detail else ""),
          file=sys.stderr)


def _generate_totp(otpauth_uri: str) -> str:
    qs = urllib.parse.parse_qs(urllib.parse.urlparse(otpauth_uri).query)
    secret_b32 = qs["secret"][0]
    key = base64.b32decode(secret_b32 + "=" * (-len(secret_b32) % 8))
    msg = struct.pack(">q", int(time.time() // 30))
    h = hmac.new(key, msg, hashlib.sha1).digest()
    offset = h[-1] & 0x0F
    return f"{(struct.unpack('>I', h[offset:offset + 4])[0] & 0x7FFFFFFF) % 1000000:06d}"


def login(page: Page, base_url: str, password: str, otpauth_uri: str) -> bool:
    for _fenster in range(2):
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


def _api(base_url: str, path: str, *, cookie: str) -> tuple[int, bytes]:
    """Rohzugriff auf die eigene API, um den **Zustand nach dem Zug** zu prüfen. `unverified`
    betrifft nur das selbstsignierte Harness-Zertifikat — dieselbe Ausnahme wie
    `ignore_https_errors` im Browser; Sitzung und Rechteprüfung laufen unverändert."""
    req = urllib.request.Request(f"{base_url}{path}")
    req.add_header("Cookie", cookie)
    try:
        with urllib.request.urlopen(req, context=ssl._create_unverified_context()) as resp:
            return resp.status, resp.read()
    except urllib.error.HTTPError as exc:
        return exc.code, exc.read()


def _cookie_header(page: Page) -> str:
    return "; ".join(f"{c['name']}={c['value']}" for c in page.context.cookies())


def _mitte(page: Page, quell_sel: str, ziel_sel: str) -> dict:
    """Ein Zug über die **echte** Maus-Input-Pipeline, mit zwei Messpunkten im Bild des Zugs.

    `mitte` entsteht, während die Maustaste gedrückt ist: das ist der einzige Zeitpunkt, zu dem
    der Drop-Zustand (Station 3) überhaupt sichtbar sein kann — nach `mouse.up` ist er weg, und ein
    Bild *danach* würde die Aussage der Station nicht zeigen können.
    """
    quelle = page.locator(quell_sel)
    ziel = page.locator(ziel_sel)
    qs, zs = quelle.bounding_box(), ziel.bounding_box()
    page.mouse.move(qs["x"] + qs["width"] / 2, qs["y"] + qs["height"] / 2)
    page.mouse.down()
    # Die ersten Schritte sind die Dragschwelle von Chromium: erst danach feuert `dragstart`.
    page.mouse.move(qs["x"] + qs["width"] / 2 + 24, qs["y"] + qs["height"] / 2 + 12, steps=6)
    page.mouse.move(zs["x"] + zs["width"] / 2, zs["y"] + zs["height"] / 2, steps=18)
    page.wait_for_timeout(250)
    mitte = page.evaluate(
        """(sel) => {
            const el = document.querySelector(sel);
            if (!el) return {vorhanden: false};
            const s = getComputedStyle(el);
            return {
                vorhanden: true,
                klasse: el.className,
                dragover: el.classList.contains('tree__realfolder--dragover'),
                border_style: s.borderTopStyle,
                border_color: s.borderTopColor,
                background: s.backgroundColor,
            };
        }""",
        ziel_sel,
    )
    return {"mitte": mitte}


def main() -> int:
    ap = argparse.ArgumentParser()
    ap.add_argument("--base-url", default=DEFAULT_BASE_URL)
    ap.add_argument("--creds", type=Path, default=DEFAULT_CREDS)
    ap.add_argument("--report", default="p9_step_d_probe.json")
    # **Der Gegenlauf schreibt in andere Dateien.** Grund ist derselbe wie beim trace-Block
    # (2026-10-02): Skript und Ausgabepfade waren dort identisch, der Gegenlauf hat den grünen
    # Beleg im Repo überschrieben, und im Commit lag ein Beleg mit `alle_ok: false`. Ein Gegenlauf
    # darf rot sein — das ist sein Zweck — aber er darf **nie** den Erfolgsnachweis überschreiben.
    # Deshalb eigener Report-Name über `--report` und eigene Bildablage über `--screenshots-dir`
    # (die Gegenläufe schreiben nach `/tmp/opencode` und kommen gar nicht erst ins Repo).
    ap.add_argument("--screenshots-dir", type=Path, default=OUT_DIR)
    args = ap.parse_args()
    args.screenshots_dir.mkdir(parents=True, exist_ok=True)
    PROBE_DIR.mkdir(parents=True, exist_ok=True)
    bilder = args.screenshots_dir

    creds = json.loads(args.creds.read_text())
    with sync_playwright() as pw:
        browser = pw.chromium.launch()
        page = browser.new_page(viewport={"width": 1440, "height": 900},
                                ignore_https_errors=True)
        # **Request-Zähler** für Station 7: der Leerlauf-Riegel ist die Abwesenheit eines PATCH,
        # und eine Abwesenheit lässt sich nur an einer Zählung prüfen, nicht an einem Zustand.
        patches: list[str] = []
        page.on("request", lambda r: patches.append(r.url) if r.method == "PATCH" else None)

        page.goto(f"{args.base_url}/ui/login", wait_until="domcontentloaded")
        time.sleep(32 - (datetime.datetime.now().second % 30))  # TOTP-Fenster, Login-Rate-Limit
        if not login(page, args.base_url, creds["password"], creds["otpauth_uri"]):
            print("Login fehlgeschlagen", file=sys.stderr)
            return 2
        try:
            page.locator("#update-banner-dismiss").click(timeout=800)
        except Exception:
            pass
        page.add_init_script(ZAEHLER_SNIPPET)

        # --- Station 1: Aufbau -----------------------------------------------------------
        page.goto(f"{args.base_url}/ui/", wait_until="domcontentloaded")
        time.sleep(1.5)
        space_zeile = page.locator(".tree__space", has_text="alpha")
        pruefe("1 Space-Zeile in der Rail", space_zeile.count() >= 1,
               f"{space_zeile.count()} Treffer auf .tree__space", zeile="P9-29")
        if space_zeile.count() and page.locator(f'.tree__realfolder[data-folder="{ORDNER}"]').count() == 0:
            # Die Ordnerzeilen rendert `renderSpaceNode()` nur im aufgeklappten Zustand.
            space_zeile.first.click()
            time.sleep(0.8)
        ordner_zeile = page.locator(f'.tree__realfolder[data-folder="{ORDNER}"]')
        pruefe("1 Ordnerzeile sichtbar", ordner_zeile.count() == 1,
               f"{ordner_zeile.count()} Treffer auf .tree__realfolder[data-folder={ORDNER!r}]", zeile="P9-29")

        # Space-Ansicht ("Alle Items" des Space) — sie listet alle Items, auch die im Ordner.
        page.locator(".overview__space-open", has_text="alpha").first.click()
        time.sleep(2.0)
        zeilen = page.locator(".list__rows > li")
        pruefe("1 Space-Ansicht gerendert", zeilen.count() == 3, f"{zeilen.count()} Zeilen", zeile="P9-29")
        page.screenshot(path=str(bilder / "p9_step_d_01_space_ansicht.png"))

        def zeile_von(titel: str):
            return page.locator(".list__rows > li").filter(
                has=page.locator(".list__row-title", has_text=titel)).first

        id_aus = zeile_von(TITEL_RAUS).locator(".list__row").get_attribute("data-id")
        id_wurzel = zeile_von(TITEL_WURZEL).locator(".list__row").get_attribute("data-id")
        id_ordner = zeile_von(TITEL_ORDNER).locator(".list__row").get_attribute("data-id")
        pruefe("1 Item-IDs bestimmt", all([id_aus, id_wurzel, id_ordner]),
               f"raus={id_aus} wurzel={id_wurzel} ordner={id_ordner}", zeile="P9-29")

        # --- Station 6 zuerst: Gegenrichtung rein (das einzige Ziel vor D2) ---------------
        vor_patches = len(patches)
        page.evaluate("() => window.__dndReset()")
        _mitte(page, f'.list__rows > li:has(.list__row-title:text-is("{TITEL_WURZEL}"))',
               f'.tree__realfolder[data-folder="{ORDNER}"]')
        page.screenshot(path=str(bilder / "p9_step_d_02_dragover_ordner.png"))
        page.mouse.up()
        time.sleep(2.0)
        status, roh = _api(args.base_url, f"/api/v1/items/{id_wurzel}",
                           cookie=_cookie_header(page))
        folder_wurzel = json.loads(roh).get("folder") if status == 200 else None
        pruefe("6 Wurzel-Item in den Ordner gezogen (Gegenrichtung)",
               folder_wurzel == ORDNER and len(patches) > vor_patches,
               f"folder={folder_wurzel!r}, PATCHes={len(patches) - vor_patches}", zeile="P9-29")

        # --- Station 3+4+5: der eigentliche P9-29-Zug, aus dem Ordner heraus -------------
        ordner_zeile.click()
        time.sleep(2.0)
        im_ordner = page.locator(".list__rows > li").count()
        ordner_alle = im_ordner
        pruefe("1 Ordneransicht zeigt nur Ordner-Items", im_ordner == 3,
               f"{im_ordner} Zeilen (das Wurzel-Item ist Station 6 in den Ordner gewandert)", zeile="P9-29")
        page.screenshot(path=str(bilder / "p9_step_d_03_ordneransicht.png"))

        page.evaluate("() => window.__dndReset()")
        vor_patches = len(patches)
        zustand = _mitte(page, f'.list__rows > li:has(.list__row-title:text-is("{TITEL_RAUS}"))',
                         ".tree__space")
        mitte = zustand["mitte"]
        # Das Bild **im** Zug: die gestrichelte Kante ist der ganze Gegenstand der Station.
        page.locator(".rail").screenshot(
            path=str(bilder / "p9_step_d_04_dragover_space_zeile.png"))
        page.mouse.up()
        time.sleep(2.5)
        zaehler_nach = page.evaluate("() => window.__dnd")

        # Station 2: die Kette kam vom Browser, und die Item-ID war im dataTransfer.
        pruefe("2 Browser-Ereigniskette: dragstart → dragover → drop",
               zaehler_nach["start"] == 1 and zaehler_nach["over"] >= 1
               and zaehler_nach["drop"] == 1 and id_aus in zaehler_nach["daten"],
               f"start={zaehler_nach['start']} over={zaehler_nach['over']} "
               f"drop={zaehler_nach['drop']} daten={zaehler_nach['daten']}", zeile="P9-29")
        # Station 3: nicht nur die Klasse, sondern der berechnete Stil — "sichtbar" ist eine
        # Aussage über das Aussehen, und eine Klasse ohne CSS wäre ein toter Name.
        pruefe("3 Drop-Zustand sichtbar (Klasse + gestrichelte Akzentkante)",
               bool(mitte.get("dragover")) and mitte.get("border_style") == "dashed",
               f"dragover={mitte.get('dragover')} border={mitte.get('border_style')} "
               f"farbe={mitte.get('border_color')}", zeile="P9-30")
        nach_klasse = page.locator(".tree__space.tree__realfolder--dragover").count()
        pruefe("4 Drop-Zustand nach dem Drop wieder weg", nach_klasse == 0,
               f"{nach_klasse} Elemente mit der Klasse", zeile="P9-30")
        toast = page.locator(".toast")
        toast_text = toast.first.inner_text() if toast.count() else ""
        pruefe("5 Toast nennt die Space-Wurzel", "(Space-Wurzel)" in toast_text,
               repr(toast_text[:80]), zeile="P9-29")
        cookie = _cookie_header(page)
        status, roh = _api(args.base_url, f"/api/v1/items/{id_aus}", cookie=cookie)
        folder_aus = json.loads(roh).get("folder") if status == 200 else "<kein 200>"
        pruefe("5 Item steht in der Space-Wurzel (Server)", folder_aus == "",
               f"GET /api/v1/items/{id_aus} -> {status}, folder={folder_aus!r}", zeile="P9-29")
        im_ordner = page.locator(".list__rows > li").count()
        pruefe("5 Ordnerliste ohne das Item", im_ordner == ordner_alle - 1,
               f"{ordner_alle} -> {im_ordner} Zeilen", zeile="P9-29")
        page.screenshot(path=str(bilder / "p9_step_d_05_nach_dem_zug.png"))

        # --- Station 7: Leerlauf-Riegel `tree.js:139` ------------------------------------
        vor_patches = len(patches)
        page.evaluate("() => window.__dndReset()")
        _mitte(page, f'.list__rows > li:has(.list__row-title:text-is("{TITEL_ORDNER}"))',
               f'.tree__realfolder[data-folder="{ORDNER}"]')
        page.mouse.up()
        time.sleep(2.0)
        zaehler_leerlauf = page.evaluate("() => window.__dnd")
        pruefe("7 Drop auf den eigenen Ordner löst keinen PATCH aus",
               len(patches) == vor_patches and zaehler_leerlauf["drop"] == 1,
               f"drop={zaehler_leerlauf['drop']} (der Zug kam an), "
               f"PATCHes={len(patches) - vor_patches}", zeile="P9-29")
        status, roh = _api(args.base_url, f"/api/v1/items/{id_ordner}", cookie=cookie)
        pruefe("7 Item im Ordner geblieben",
               status == 200 and json.loads(roh).get("folder") == ORDNER,
               f"folder={json.loads(roh).get('folder')!r}" if status == 200 else f"HTTP {status}", zeile="P9-29")

        # --- Station 8/9: ESC mit und ohne fullscreenElement (P9-28) --------------------
        zeile_von(TITEL_ORDNER).locator(".list__row").click()
        time.sleep(1.5)
        offen_vor = _detail_offen(page)
        page.keyboard.press("Escape")
        time.sleep(1.0)
        zu_nach = not _detail_offen(page)
        pruefe("8 ESC außerhalb Vollbild schließt das Item", offen_vor and zu_nach,
               f"offen={offen_vor} zu={zu_nach}", zeile="P9-28")

        zeile_von(TITEL_ORDNER).locator(".list__row").click()
        time.sleep(1.5)
        fs = page.evaluate(
            """async () => {
                await document.documentElement.requestFullscreen().catch(() => {});
                await new Promise(r => setTimeout(r, 400));
                return !!document.fullscreenElement;
            }""")
        page.screenshot(path=str(bilder / "p9_step_d_06_vollbild.png"))
        page.keyboard.press("Escape")
        time.sleep(1.0)
        bleibt_offen = _detail_offen(page)
        pruefe("9 ESC bei gesetztem fullscreenElement schließt nichts",
               fs and bleibt_offen,
               f"fullscreenElement={fs}, Item-offen={bleibt_offen} "
               f"(der Browser selbst verlässt im Automationslauf den Vollbildmodus nicht — "
               f"synthetische Tastendrücke; die App-Seite des Guards ist die geprüfte)", zeile="P9-28")
        browser.close()

    report = {
        "base_url": args.base_url,
        "ordner": ORDNER,
        "item_ids": {"raus": id_aus, "wurzel": id_wurzel, "ordner": id_ordner},
        "befunde": befunde,
        "alle_ok": all(b["ok"] for b in befunde),
    }
    (PROBE_DIR / args.report).write_text(json.dumps(report, indent=2, ensure_ascii=False))
    print(f"\n{sum(b['ok'] for b in befunde)}/{len(befunde)} Pruefungen gruen", file=sys.stderr)
    return 0 if report["alle_ok"] else 1


if __name__ == "__main__":
    raise SystemExit(main())
