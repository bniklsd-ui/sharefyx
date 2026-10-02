#!/usr/bin/env python3
"""P9 — Pixel-Gegenprobe für `#archive-button` (B17, Nikinger-Entscheidung 2026-10-02).

**Die Behauptung, die diese Probe messen soll.** `.btn.action--caution` trägt nach dieser
Runde **exakt** die Standardfläche — dieselben `--btn-std-*`-Tokens wie `.btn`, ohne eigene
Kopie. Die Entscheidung ist wortgleich die Zeile der Selection/Choice-Konvention v3
(`phase8_ui_graph/CLAUDE.md`, Kategorie „Vorsicht"): *Standard-Knopfplastik, aber
`color: var(--caution)` auf Label und Glyph; **keine** gefüllte rote Fläche.*

**Warum das überhaupt ein Befund war.** Vorher trug der Knopf die alte graue Familie
`--btn-face-top/bottom` (`#2A313A`/`#1C222A`) — und die ist **heller** als die Standardfläche
`#0C1C31`/`#050B13`. Gemessen heißt das: „Vorsicht" war der auffälligste Knopf der
Editor-Fußzeile, nicht der Standard. Ein Konsistenz-Befund, den man nicht am Markup sieht.

**Wozu ein Browser, obwohl die Wächter existieren.** `test_caution_button_wears_the_standard_face`
prüft, dass **keine** eigene Fläche mehr deklariert wird — es kann nicht prüfen, dass daraus
dasselbe Bild wird wie bei einem echten `.btn`. Das Muster ist das der beiden Vorgänger
(`p9_btn2_toolbar_probe.py`): dieselbe Fläche als String-Vergleich der *gerechneten* Werte
(das ist die eigentliche Behauptung) **plus** vier Probenpunkte aus einem echten Screenshot
(das ist das, was ein Auge entscheidet).

**Gegen wen verglichen wird — und warum nicht gegen `.btn-primary`.** `#archive-button` und
`#append-button` tragen ab dieser Runde **dieselben** Tokens, ein Vergleich der beiden untereinander
wäre also zirkulär: er wäre auch dann grün, wenn beide falsch wären. Das ist hier in Ordnung,
weil die zu prüfende Aussage genau „erbt dieselbe Fläche wie `.btn`" ist und `.btn` durch
`test_account_nav_and_standard_button_wear_the_rail_selection_look` (den Token-Namen) **und** den
btn2-Lauf (das Bild) unabhängig feststeht. Gegen `#save-button` (`.btn-primary`, Akzentfläche)
wäre der Vergleich sinnlos — es soll ja genau *nicht* so aussehen.

**Zwei Vorbedingungen werden behauptet, nicht angenommen** (die Lehre aus dem btn2-Lauf, dort hat
ein Selektor statt eines Werts geprüft und ein deaktivierter Knopf das Bild geliefert):
`#archive-button` trägt beide Klassen und ist **nicht** `:disabled` — er wird im Code nie
deaktiviert (`editor.js`: nur `if (!state.editingSnapshot) return;`), aber „nie" ist eine
Behauptung über den Code und keine Beobachtung des Laufs.

**Der Kontrast wird mitgemessen, aber nicht als Schwellwert verkauft.** `color: var(--caution)`
(`#E5484D`) auf `#0C1C31` ergibt **4,29:1** — besser als die 3,36:1 auf der alten grauen Plastik,
aber unter dem WCAG-AA-Wert 4,5:1 für normalgroßen Text (14 px/500 zählt nicht als „large text").
Deshalb ist die Prüfung „**nicht schlechter als vorher**" (eine echte Eigenschaft, die diese
Runde zusichert) und der Absolutwert steht im Detail. Ob die Beschriftung heller wird, ist eine
eigene Design-Entscheidung und **nicht** Teil dieses Blocks.

    python phase9_hardening/scripts/p9_step_g_wegwerf.py start
    ~/.claude-code-tools/e2e-venv/bin/python phase9_hardening/scripts/p9_btn3_caution_probe.py
    python phase9_hardening/scripts/p9_step_g_wegwerf.py stop

**Gegenlauf.** `--tag gegenprobe` schreibt nach `<name>_gegenprobe.json`; genau das ist der
Fehler, den `test_committed_probe_evidence.py` am 2026-10-02 teuer gemacht hat (Skript und
Ausgabepfade waren im Hand-Gegenlauf dieselben, die Probe-Datei im Repo war der Gegenlauf selbst).
"""
from __future__ import annotations

import argparse
import base64
import datetime
import hashlib
import hmac
import io
import json
import re
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

# Dieselbe Toleranz wie der btn2-Lauf: ±2 pro Kanal. PNG ist verlustfrei, die Differenz an der
# Kante darf die Rundung des Samplings sein. „Archivieren" (≈100 px) und „Anhängen" (≈106 px)
# haben dieselbe Hoehe, dieselbe Schrift — die Verlaufsauswertung ist also vergleichbar, nur die
# Breite unterscheidet sich, und deshalb wird wie dort an einer festen Spalte (x = 4 px, hinter
# der 1-px-Kante) gemessen, nie an einem relativen x.
PIXEL_TOLERANZ = 2

# Historische Werte der grauen Plastik, gemessen am Stand vor dieser Runde (app.css HEAD,
# `.btn.action--caution`): die Familie `--btn-face-top/bottom`. Sie stehen hier als Konstante,
# weil die alte Regel **gelöscht** ist — im CSS wäre der Vergleich unmöglich, und ein Beleg,
# der sich selbst mit vergleicht, misst nichts.
ALTE_FLAECHE_OBEN = (0x2A, 0x31, 0x3A)
ALTE_FLAECHE_UNTEN = (0x1C, 0x22, 0x2A)

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


def _pixel_abs(page, selector: str, x: int, fy: float) -> tuple[int, int, int]:
    """Wie im btn2-Lauf: **absolutes** x, weil der Rand bei x=0 liegt und ein relatives x bei
    100 px Breite etwas anderes bedeutet als bei 26 px. Glyphenfreie Spalte x = 4 px."""
    png = page.locator(selector).first.screenshot()
    img = Image.open(io.BytesIO(png)).convert("RGB")
    return img.getpixel((min(x, img.width - 1), min(int(img.height * fy), img.height - 1)))


def _vergleiche(name_a: str, name_b: str, pa: tuple, pb: tuple) -> tuple[int, str]:
    abweichung = max(abs(x - y) for x, y in zip(pa, pb))
    return abweichung, (f"{name_a}={pa} {name_b}={pb} max|Δ|={abweichung} "
                        f"(Toleranz ±{PIXEL_TOLERANZ})")


def _rgb_stops(background_image: str) -> list[tuple[int, int, int]]:
    """Die `rgb(...)`-Stopps eines berechneten `linear-gradient` in Reihenfolge.

    Chrome serialisiert `linear-gradient(180deg, #2A313A, #1C222A)` als
    `linear-gradient(rgb(42, 49, 58) 0%, rgb(28, 34, 42) 100%)` — die Prozentangaben sind im
    String, die Reihenfolge auch, und beides wird hier benutzt statt geraten.
    """
    return [tuple(int(x) for x in m) for m in re.findall(r"rgb\((\d+),\s*(\d+),\s*(\d+)\)",
                                                      background_image)]


def _luminanz(rgb: tuple[int, int, int]) -> float:
    kanal = []
    for wert in rgb:
        c = wert / 255
        kanal.append(c / 12.92 if c <= 0.03928 else ((c + 0.055) / 1.055) ** 2.4)
    return 0.2126 * kanal[0] + 0.7152 * kanal[1] + 0.0722 * kanal[2]


def _kontrast(text_rgb: tuple[int, int, int], bg_rgb: tuple[int, int, int]) -> float:
    a, b = _luminanz(text_rgb), _luminanz(bg_rgb)
    hell, dunkel = max(a, b), min(a, b)
    return (hell + 0.05) / (dunkel + 0.05)


def main() -> int:
    ap = argparse.ArgumentParser()
    ap.add_argument("--base-url", default=DEFAULT_BASE_URL)
    ap.add_argument("--creds", type=Path, default=DEFAULT_CREDS)
    ap.add_argument("--tag", default="", help="Suffix der Probe-Datei, z. B. 'gegenprobe'")
    args = ap.parse_args()
    # Mit Unterstrich, damit ein Gegenlauf am Dateinamen erkennbar bleibt — dieselbe Regel, an der
    # `test_committed_probe_evidence.py` eine rote Probe erkennt (`*_gegenprobe.json`).
    suffix = f"_{args.tag}" if args.tag else ""
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

        # --- Station 0: in den Editor ----------------------------------------------------------------
        offen = page.locator(".overview__space-open", has_text="alpha")
        if offen.count() == 0:
            offen = page.locator(".overview__space-open")
        offen.first.click()
        time.sleep(1.8)
        page.locator(".list__row").first.click()
        page.wait_for_selector("#editor-toolbar", state="visible", timeout=10000)
        time.sleep(0.6)

        ziel = "#archive-button"
        referenz = "#append-button"

        # --- Station 1/2: die Vorbedingungen -----------------------------------------------------------
        ziel_klassen = (page.locator(ziel).first.get_attribute("class") or "").split()
        pruefe("Vorbedingung: #archive-button traegt .btn UND .action--caution",
               "btn" in ziel_klassen and "action--caution" in ziel_klassen,
               f"class={ziel_klassen!r}")
        pruefe("Vorbedingung: #archive-button ist sichtbar und NICHT deaktiviert",
               page.locator(ziel).first.is_visible() and not page.locator(ziel).first.is_disabled(),
               "der Knopf wird im Code nie deaktiviert (editor.js) — behauptet, nicht angenommen")
        ref_klassen = (page.locator(referenz).first.get_attribute("class") or "").split()
        pruefe("Vorbedingung: #append-button ist ein .btn ohne action--caution (Vergleichsbasis)",
               "btn" in ref_klassen and "action--caution" not in ref_klassen,
               f"class={ref_klassen!r}")

        # --- Station 3/4: die Behauptung selbst, als Stringgleichheit --------------------------------
        ziel_bg = page.locator(ziel).first.evaluate("e => getComputedStyle(e).backgroundImage")
        ref_bg = page.locator(referenz).first.evaluate("e => getComputedStyle(e).backgroundImage")
        pruefe("gerechnete Flaeche ist identisch (backgroundImage, Stringgleichheit)",
               ziel_bg == ref_bg and ziel_bg != "none",
               f"archive={ziel_bg!r} btn={ref_bg!r}")
        kanten = page.evaluate(
            """([a, b]) => [a, b].map(s => {
                 const e = document.querySelector(s); const c = getComputedStyle(e);
                 return [c.borderTopColor, c.borderTopWidth, c.borderTopStyle,
                         c.boxShadow, c.paddingTop, c.fontSize, c.fontWeight].join('|');
               })""", [ziel, referenz])
        pruefe("Kante, Polster und Typografie sind identisch (nur die Beschriftungsfarbe nicht)",
               kanten[0] == kanten[1],
               f"archive={kanten[0]!r} btn={kanten[1]!r}")

        # --- Station 5: die alte graue Plastik ist weg ------------------------------------------------
        # Die alte Familie ist gelöscht, deshalb wird gegen ihre *gemessenen* Farbwerte geprüft
        # (RGB als Zahlen im berechneten Gradient-String), nicht gegen einen CSS-Text, den es
        # nicht mehr gibt. Sonst wäre die Prüfung eine V tautologie über den eigenen Umbau.
        traeger = [f"{k[0]}, {k[1]}, {k[2]}" for k in (ALTE_FLAECHE_OBEN, ALTE_FLAECHE_UNTEN)]
        pruefe("Vorsichtsknopf traegt NICHT mehr die alte graue Plastik (--btn-face-*)",
               not any(t in ziel_bg for t in traeger),
               f"kein Stopp {ALTE_FLAECHE_OBEN}/{ALTE_FLAECHE_UNTEN} in {ziel_bg!r}")

        # --- Station 6/7/8: Pixelprobe ----------------------------------------------------------------
        for label, fy in (("Kopf", 0.30), ("Mitte", 0.50), ("Fuss", 0.72)):
            pt = _pixel_abs(page, ziel, 4, fy)
            d, txt = _vergleiche("archive", "btn", pt, _pixel_abs(page, referenz, 4, fy))
            pruefe(f"archive == .btn, Verlauf {label} (Spalte x=4px)", d <= PIXEL_TOLERANZ, txt)

        pa_oben, pa_unten = _pixel_abs(page, ziel, 4, 0.25), _pixel_abs(page, ziel, 4, 0.75)
        verlauf = max(abs(a - b) for a, b in zip(pa_oben, pa_unten))
        pruefe("Vorsichtsknopf traegt einen Verlauf (oben != unten, nicht die deaktivierte Flaeche)",
               verlauf >= 3, f"oben={pa_oben} unten={pa_unten} max|Δ|={verlauf}")

        # --- Station 9: die Kategorie ist noch sichtbar ---------------------------------------------
        ziel_color = page.locator(ziel).first.evaluate("e => getComputedStyle(e).color")
        ref_color = page.locator(referenz).first.evaluate("e => getComputedStyle(e).color")
        pruefe("Beschriftung traegt die Vorsichtsfarbe, nicht die Standardfarbe",
               ziel_color == "rgb(229, 72, 77)" and ziel_color != ref_color,
               f"archive={ziel_color} btn={ref_color} (--caution == --danger == #E5484D)")

        # --- Station 10: Hover ----------------------------------------------------------------------
        page.locator(ziel).first.hover()
        time.sleep(0.35)
        hover_bg = page.locator(ziel).first.evaluate("e => getComputedStyle(e).backgroundImage")
        pruefe("Hover traegt einen eigenen Zustand (--btn-std-fill-hover), nicht denselben",
               hover_bg != ziel_bg and "132, 42, 73" not in hover_bg,
               f"hover={hover_bg!r} ruhe={ziel_bg!r}")
        page.locator(ziel).first.screenshot(path=str(OUT_DIR / f"p9_btn3_04_hover{suffix}.png"))
        # Zeiger weg, bevor der Ruhe-Zustand aufgenommen wird. **Reihenfolgefehler, absichtlich
        # hier abgesichert:** der erste Entwurf nahm die Ruhe-Aufnahme am Ende der Skripts, also
        # während der Zeiger noch auf dem Knopf lag — das Bild hätte den Hover gezeigt und wäre
        # als Beleg für die Ruhe zitiert worden (im btn2-Lauf stand aus genau diesem Grund die
        # Verlaufsmessung im Deaktiviert-Block).
        page.mouse.move(10, 10)
        time.sleep(0.35)
        ruhe_bg = page.locator(ziel).first.evaluate("e => getComputedStyle(e).backgroundImage")
        pruefe("nach dem Wegziehen des Zeigers ist der Ruhe-Zustand wieder da (Aufnahme stimmt)",
               ruhe_bg == ziel_bg, f"ruhe={ruhe_bg!r} erwartet={ziel_bg!r}")

        # --- Station 11: Kontrast, gemessen statt behauptet ------------------------------------------
        stops = _rgb_stops(ziel_bg)
        if len(stops) == 2:
            neu = _kontrast((229, 72, 77), stops[0])   # oberer Stopp = ungünstigster Fall
            alt = _kontrast((229, 72, 77), ALTE_FLAECHE_OBEN)
            pruefe("Beschriftungskontrast ist NICHT schlechter als auf der alten grauen Plastik",
                   neu >= alt,
                   f"neu {neu:.2f}:1 (Text #E5484D auf {stops[0]}) gegen alt {alt:.2f}:1 "
                   f"(auf #2A313A) — WCAG-AA (4.5:1) fuer 14px/500 bleibt offen, siehe Docstring")
        else:
            pruefe("Kontrast messbar (zwei rgb-Stopps im berechneten Gradienten)",
                   False, f"backgroundImage={ziel_bg!r}")

        # --- Screenshots fuer das Auge des Ningkers ------------------------------------------------
        # `.editor__head-actions` ist die Leiste, in der `Archivieren`, `Speichern` und das "×"
        # nebeneinander stehen — **der** eine Blick, um den es hier geht. Der erste Entwurf dieses
        # Skripts schnitt `#editor-toolbar` aus und nannte das Bild `..._footer.png`: das ist die
        # *Formatierleiste*, sie enthält den Vorsichtsknopf gar nicht, und der Dateiname behauptete
        # das Gegenteil. Ein Screenshot, der etwas anderes zeigt als sein Name, ist derselbe Fehler
        # wie ein Beleg, der etwas anderes belegt (trace-Block, 2026-10-02).
        page.locator(ziel).first.screenshot(path=str(OUT_DIR / f"p9_btn3_02_ruhe{suffix}.png"))
        page.locator(".editor__head-actions").screenshot(
            path=str(OUT_DIR / f"p9_btn3_01_kopfleiste{suffix}.png"))
        page.screenshot(path=str(OUT_DIR / f"p9_btn3_03_editor{suffix}.png"), full_page=False)
        browser.close()

    ok = all(b["ok"] for b in befunde)
    name = f"p9_btn3_caution_probe{suffix}.json"
    (PROBE_DIR / name).write_text(
        json.dumps({"result": "ok" if ok else "failed", "befunde": befunde},
                   indent=2, ensure_ascii=False) + "\n", encoding="utf-8")
    print(f"\n{sum(1 for b in befunde if b['ok'])}/{len(befunde)} Prüfungen grün → "
          f"phase9_hardening/probes/{name}")
    return 0 if ok else 1



if __name__ == "__main__":
    sys.exit(main())
