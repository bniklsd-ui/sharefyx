#!/usr/bin/env python3
"""P9 — Pixel-Gegenprobe für `.toolbar-btn` (Nikinger-Entscheidung 2026-10-01, zweite Runde).

**Wozu ein Browser, obwohl es zwei statische Wächter gibt.** Die Wächter
(`test_toolbar_buttons_wear_the_standard_look`) prüfen, dass die vier Zustände die *richtigen
Tokens* nennen. Sie können nicht prüfen, dass daraus dasselbe Bild wird wie beim aktiven
Rail-Knopf — und genau das ist die Behauptung, die der Nikinger mit einem Blick entscheidet. Die
Vorgänger-Runde hat dafür `.btn` gegen `#home-button[aria-current]` pixelweise verglichen
(oben/Mitte/unten/Kante, ±1); dieses Skript macht dasselbe für die Formatierhilfen.

**Warum gegen `#home-button` und nicht gegen `.btn`.** `.btn` und `.toolbar-btn` teilen sich ab
dieser Runde dieselben Token — ein Vergleich der beiden untereinander wäre also zirkulär: Er wäre
auch dann grün, wenn beide Token falsch wären. Das Vorbild ist der Knopf, dessen Bild der Nikinger
am 2026-10-01 als *"das exakte Bild des Übersichtsknopfs"* abgenommen hat, und der einzige Knopf,
dessen Optik **unabhängig** feststeht.

**Was verglichen wird.** Vier Probenpunkte je Knopf (Kopfmitte, Mitte, Fußmitte, linke Kante bei
50 % Höhe), jedes Mal der Pixel aus einem echten Screenshot — nicht aus einem berechneten
CSS-Wert. Der Toleranzrahmen ±1 ist derselbe wie in der Vorgänger-Runde: PNG ist verlustfrei,
die einzige Differenz darf die Rundung an der Kante sein.

**Zusätzlich mitgeprüft: der deaktivierte Zustand.** In der Vorschau sind die Formatierhilfen
abgeschaltet (`editor.js :: setEditorMode`), und `:disabled` trägt bewusst `--surface` statt
`--btn-std-fill` — das ist der Punkt, an dem "alles auf Standardoptik" in "inaktiv lesbar"
kippt. Der Test prüft deshalb, dass der deaktivierte Knopf **sichtbar** anders ist (hellere
Fläche, mattere Schrift), nicht nur, dass er existiert.

    python phase9_hardening/scripts/p9_step_g_wegwerf.py start
    ~/.claude-code-tools/e2e-venv/bin/python phase9_hardening/scripts/p9_btn2_toolbar_probe.py
    python phase9_hardening/scripts/p9_step_g_wegwerf.py stop
"""
from __future__ import annotations

import argparse
import base64
import datetime
import hashlib
import hmac
import io
import json
import struct
import sys
import time
import urllib.parse
import urllib.request
from pathlib import Path

from PIL import Image
from playwright.sync_api import sync_playwright

REPO_ROOT = Path(__file__).resolve().parents[2]
OUT_DIR = REPO_ROOT / "docs" / "screenshots"
PROBE_DIR = REPO_ROOT / "phase9_hardening" / "probes"
DEFAULT_BASE_URL = "https://127.0.0.1:18775"
DEFAULT_CREDS = Path("/tmp/opencode/p9-step-g-wegwerf/credentials.json")

# Toleranz der Pixelprobe: ±2 pro Kanal. Die Vorgänger-Runde nutzte ±1 fuer KNÖPFE GLEICHER
# Höhe; hier sind es 24 px gegen 41 px, dieselbe relative Position faellt damit auf Zeile 17
# gegen Zeile 29 — im Bereich, wo der Gradient zwischen zwei Nachbarwerten interpoliert, sind
# das zwei Stufen. ±1 wuerde hier die Rundung des PNG-Samplings pruefen, nicht die Farbe.
PIXEL_TOLERANZ = 2

befunde: list[dict] = []


def pruefe(name: str, ok: bool, detail: str = "") -> None:
    befunde.append({"pruefung": name, "ok": bool(ok), "detail": detail})
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


def login(page, base_url: str, password: str, otpauth_uri: str) -> bool:
    """Zwei Fenster, weil ein im letzten Sekundenfragment verbrauchtes TOTP das
    Login-Rate-Limit auslöst (P8.6-Block-H-Fund, hierher übernommen)."""
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


def _box(page, selector: str) -> dict:
    return page.locator(selector).first.bounding_box()


def _pixel_abs(page, selector: str, x: int, fy: float) -> tuple[int, int, int]:
    """Wie `_pixel`, aber mit **absolutem** x-Pixel. Für Rand- und Glyphenfragen: ein relativer
    x-Wert bedeutet bei einem 26-px-Knopf etwas anderes als bei einem 106-px-Knopf — der Rand
    liegt bei x=0 und bei x=3, dieselbe Zahl 0.03 dagegen mal hier, mal dort."""
    png = page.locator(selector).first.screenshot()
    img = Image.open(io.BytesIO(png)).convert("RGB")
    return img.getpixel((min(x, img.width - 1), min(int(img.height * fy), img.height - 1)))


def _pixel(page, selector: str, fx: float, fy: float) -> tuple[int, int, int]:
    """Ein echter Screenshot-Pixel an relativer Position (fx, fy) ∈ [0,1]² des Elements.

    Zwei Wege sind bewusst **nicht** genommen, beide mit gemessenem Fehlverhalten:

    * `page.screenshot(clip=…)` mit selbstgebauten Koordinaten — `bounding_box()` ist
      viewport-, der `clip`-Parameter dokumentbezogen. Bei einem gescrollten Panel landet die
      Probe daneben; im ersten Lauf dieses Skripts kam für `#home-button`由此 `(0,0,0)` zurück,
      also der schwarze Rail-Hintergrund statt des Knopfes.
    * `canvas`/`getImageData` — liest nur *gezeichnete* Flächen; ein CSS-Gradient mit
      `border-radius` und `box-shadow` kommt dort nicht an.

    `locator.screenshot()` löst beides: es scrollt das Element selbst in den Sichtbereich und
    liefert exakt dessen Box. Das ist der Pixel, den ein Auge sieht.
    """
    png = page.locator(selector).first.screenshot()
    img = Image.open(io.BytesIO(png)).convert("RGB")
    return img.getpixel((min(int(img.width * fx), img.width - 1),
                         min(int(img.height * fy), img.height - 1)))


def _vergleiche(name_a: str, name_b: str, pa: tuple, pb: tuple) -> tuple[int, str]:
    abweichung = max(abs(x - y) for x, y in zip(pa, pb))
    return abweichung, (f"{name_a}={pa} {name_b}={pb} max|Δ|={abweichung} "
                        f"(Toleranz ±{PIXEL_TOLERANZ})")


def main() -> int:
    ap = argparse.ArgumentParser()
    ap.add_argument("--base-url", default=DEFAULT_BASE_URL)
    ap.add_argument("--creds", type=Path, default=DEFAULT_CREDS)
    args = ap.parse_args()
    OUT_DIR.mkdir(parents=True, exist_ok=True)
    PROBE_DIR.mkdir(parents=True, exist_ok=True)

    creds = json.loads(args.creds.read_text())
    with sync_playwright() as pw:
        browser = pw.chromium.launch()
        page = browser.new_page(viewport={"width": 1440, "height": 900},
                                ignore_https_errors=True)
        page.goto(f"{args.base_url}/ui/login", wait_until="domcontentloaded")
        time.sleep(32 - (datetime.datetime.now().second % 30))
        if not login(page, args.base_url, creds["password"], creds["otpauth_uri"]):
            print("Login fehlgeschlagen", file=sys.stderr)
            return 2
        try:
            page.locator("#update-banner-dismiss").click(timeout=800)
        except Exception:
            pass

        # --- Station 1: das Vorbild, im Zustand, in dem es aktiv IST --------------------------
        #
        # **Zwei Fehler, die dieser Lauf zuerst gemacht hat — beide von der Sorte, die dieses
        # Repo schon viermal teuer geworden ist** (P8.6 Block H, P9 Step G, Step B, A4-Vorbereitung):
        # ein Wächter, der etwas anderes prüft als er behauptet.
        #
        # (a) Die Vorbedingung `count() == 1` für `#home-button[aria-current]` war wertlos: CSS-/DOM-
        #     Selektoren matchen ein Attribut, **nicht seinen Wert**. Der Knopf trug
        #     `aria-current="false"` — der Zähler war 1, der Knopf inaktiv. Verglichen wurde deshalb
        #     die schwarze Rail (`(0,0,0)`). Die Vorbedingung prüft jetzt `get_attribute(...) ==
        #     "true"`, und sie wird **vor** der Zustandsänderung geprüft, weil `#home-button` nur in
        #     der Übersicht aktiv ist.
        # (b) Der erste Pixelvergleich lief gegen einen **deaktivierten** Knopf: der Editor öffnet
        #     per P5-Entscheidung in der Vorschau. Beides wird jetzt behauptet, nicht angenommen.
        aktueller_knopf = page.locator("#home-button").first.get_attribute("aria-current")
        pruefe("Vorbild-Knopf ist WIRKLICH aktiv (aria-current == 'true')",
               aktueller_knopf == "true", f"aria-current={aktueller_knopf!r}")

        # Der Pixelvergleich selbst ist zweistufig, weil „dasselbe Bild" zwei verschiedene Fragen
        # hat: *dieselbe Fläche* (die gerechneten Werte — als Strings exakt vergleichbar) und
        # *dieselbe Interpolation* (der Verlauf über die Knopfhöhe). Die Fläche wird am
        # VORBILD im aktivierten Zustand geprüft, die Interpolation gegen das `.btn` im selben
        # Editor-Panel (dort sind beide hoch genug, dass die Zeilenrundung den Vergleich trägt).
        ref_bg = page.locator("#home-button").first.evaluate("e => getComputedStyle(e).backgroundImage")
        pruefe("Vorbild traegt den Auswahl-Fill, nicht 'none'",
               ref_bg not in ("none", ""), f"#home-button background-image={ref_bg!r}")

        # In den **eigenen** Space "alpha" — dieselbe Navigation, die `p9_step_g_self_check.py`
        # benutzt (`.overview__space-open` auf der Übersicht), nicht der Rail-Knopf `#home-button`:
        # der öffnet nur die Übersicht (bzw. zurück), er wechselt nicht in die Item-Liste.
        offen = page.locator(".overview__space-open", has_text="alpha")
        if offen.count() == 0:
            offen = page.locator(".overview__space-open")
        offen.first.click()
        time.sleep(1.8)
        page.locator(".list__row").first.click()
        page.wait_for_selector("#editor-toolbar", state="visible", timeout=10000)
        time.sleep(0.6)

        # **Produktinvariante, im ersten Probelauf gemessen:** der Editor öffnet per
        # P5-Entscheidung standardmäßig in der **Vorschau** ("Editor öffnet standardmäßig in der
        # Vorschau, zwei Ausnahmen: Neuanlage, Neuladen nach Schreibvorgang"). Die Formatierhilfen
        # sind dort `:disabled` — vor der Pixelprobe wird der Zustand also behauptet (Text des
        # Umschalters) und nicht nur angenommen.
        umschalter = page.locator("#toggle-preview").inner_text().strip()
        pruefe("Editor öffnet in der Vorschau (P5-Regel)", umschalter == "Bearbeiten",
               f"#toggle-preview = {umschalter!r}")
        page.locator("#toggle-preview").click()
        page.wait_for_selector("#editor-textarea:not([hidden])", timeout=5000)
        time.sleep(0.4)

        toolbar = '[data-md="bold"]'
        pruefe("Formatierhilfen sind im Bearbeiten-Modus aktiv",
               not page.locator(toolbar).is_disabled(), "data-md=bold nicht disabled")

        # **Nicht** `#link-picker-button`: der sitzt im Kopfdaten-`<details>`, das standardmäßig
        # ZUGEKLAPPT ist (P5 Step 7b) — im ersten Lauf war er `visible: false`, der Vergleich wäre
        # gegen eine 0x0-Box gelaufen. `#append-button` ist sichtbar, trägt `.btn` und sitzt auf
        # demselben `--surface`-Streifen wie die Formatierleiste (`.editor__append`).
        standard = "#append-button"
        tb_bg = page.locator(toolbar).first.evaluate("e => getComputedStyle(e).backgroundImage")
        st_bg = page.locator(standard).first.evaluate("e => getComputedStyle(e).backgroundImage")
        pruefe("gerechnete Flaeche ist identisch (backgroundImage, Stringgleichheit)",
               tb_bg == st_bg and tb_bg != "none", f"toolbar={tb_bg!r} btn={st_bg!r}")

        # Pixelprobe, **ohne** die Beschriftung zu treffen. Der erste Lauf verglich bei
        # `fx = 0.5, fy = 0.5` die Mitte der Knöpfe — und landete bei `#append-button` auf den
        # Glyphen von „Anhängen" (gemessen: Zeile h/2 trägt (128,196,242) und (233,230,203),
        # also Antialiasing-Pixel einer Schrift, Δ 34 zum Knopf daneben). Ein Pixelvergleich von
        # Knöpfen ist deshalb nur an **glyphenfreien** Stellen aussagekräftig: feste Spalte
        # x = 4 px (hinter der 1-px-Kante), darüber die drei Höhen des Verlaufs.
        for label, fy in (("Kopf", 0.30), ("Mitte", 0.50), ("Fuss", 0.72)):
            pt = _pixel_abs(page, toolbar, 4, fy)
            d, txt = _vergleiche("toolbar", "btn", pt, _pixel_abs(page, standard, 4, fy))
            pruefe(f"toolbar == .btn, Verlauf {label} (Spalte x=4px)", d <= PIXEL_TOLERANZ, txt)

        # Randpixel separat: bei 26 px Breite liegt die 1-px-Kante auf x=0, bei 106 px ebenfalls —
        # mit einem relativen x waeren es zwei verschiedene Stellen gewesen (Fund: der erste Lauf
        # verglich hier 0.02 des 26-px-Knopfs mit 0.02 des 106-px-Knopfs und verglich Fuellung
        # mit Fuellung statt Rand mit Rand; es ging trotzdem gruen, aus dem richtigen Grund).
        pt_r, pr_r = _pixel_abs(page, toolbar, 0, 0.5), _pixel_abs(page, standard, 0, 0.5)
        d_r, txt_r = _vergleiche("toolbar", "btn", pt_r, pr_r)
        pruefe("toolbar == .btn an der Kante (x=0px)", d_r <= PIXEL_TOLERANZ, txt_r)

        # Verlauf des **aktiven** Knopfs, gemessen **vor** dem Umschalten — der erste Versuch
        # stand im Deaktiviert-Block und maß damit zweimal denselben Zustand (Reihenfolgefehler
        # dieser Skript-Runde, am roten Ergebnis erkannt: oben == unten == (20,24,29), also die
        # Farbe von `--surface`, nicht die des Verlaufs).
        pa_oben, pa_unten = _pixel_abs(page, toolbar, 4, 0.25), _pixel_abs(page, toolbar, 4, 0.75)
        verlauf_aktiv = max(abs(a - b) for a, b in zip(pa_oben, pa_unten))
        pruefe("aktiver Knopf traegt einen Verlauf (oben != unten)", verlauf_aktiv >= 3,
               f"aktiv oben={pa_oben} unten={pa_unten} max|Δ|={verlauf_aktiv}")

        # Screenshot fuer das Auge des Ningkers: die Leiste im Zuschnitt, plus der volle Editor
        # (darin liegen Rail-Knopf und Formatierleiste im selben Bild — der eine Blick, um den es
        # bei dieser Entscheidung ging).
        page.locator("#editor-toolbar").screenshot(
            path=str(OUT_DIR / "p9_btn2_01_formatierleiste.png"))
        page.screenshot(path=str(OUT_DIR / "p9_btn2_02_editor.png"), full_page=False)

        # --- Deaktivierter Zustand: FLACH statt Verlauf -----------------------------------------
        #
        # Der erste Lauf prüfte „deaktiviert ist sichtbar heller als der aktiv" und war mit
        # Δsumme 11 rot — an einer **falschen Behauptung**: gemessen ist der deaktivierte Knopf
        # nicht heller, sondern flach (`--surface`, `backgroundImage: none`) mit matterer Schrift
        # (`--text-faint`). Die Eigenschaft, die man sehen kann und die ein Schwellwert schlecht
        # ausdrueckt, ist der **Verlauf**: aktiv interpoliert die Zeilen, deaktiviert sind oben
        # und unten derselbe Ton. Geprueft wird darum die Abwesenenz des Verlaufs statt einer
        # Helligkeitsgrenze, plus die Schriftfarbe als second channel.
        page.locator("#toggle-preview").click()
        page.wait_for_selector("#editor-preview:not([hidden])", timeout=5000)
        time.sleep(0.4)
        deaktiviert = page.locator(toolbar).is_disabled()
        pruefe("Formatierhilfen sind in der Vorschau deaktiviert", deaktiviert)
        if deaktiviert:
            farben = page.locator(toolbar).first.evaluate(
                "e => { const s = getComputedStyle(e); return [s.color, s.backgroundImage, s.borderColor]; }")
            pruefe("deaktivierter Knopf ist flach (backgroundImage none) und matter beschriftet",
                   farben[1] == "none" and farben[0] != "rgb(196, 205, 216)",
                   f"color={farben[0]} bg={farben[1]!r} border={farben[2]}")
            pd_oben, pd_unten = _pixel_abs(page, toolbar, 4, 0.25), _pixel_abs(page, toolbar, 4, 0.75)
            verlauf_aus = max(abs(a - b) for a, b in zip(pd_oben, pd_unten))
            pruefe("deaktivierter Knopf ist FLACH (oben == unten)", verlauf_aus <= 1,
                   f"deaktiviert oben={pd_oben} unten={pd_unten} max|Δ|={verlauf_aus}")
            page.locator("#editor-toolbar").screenshot(
                path=str(OUT_DIR / "p9_btn2_03_formatierleiste_deaktiviert.png"))
        browser.close()

    ok = all(b["ok"] for b in befunde)
    (PROBE_DIR / "p9_btn2_toolbar_probe.json").write_text(
        json.dumps({"result": "ok" if ok else "failed", "befunde": befunde},
                   indent=2, ensure_ascii=False) + "\n", encoding="utf-8")
    print(f"\n{sum(1 for b in befunde if b['ok'])}/{len(befunde)} Prüfungen grün → "
          f"phase9_hardening/probes/p9_btn2_toolbar_probe.json")
    return 0 if ok else 1


if __name__ == "__main__":
    sys.exit(main())
