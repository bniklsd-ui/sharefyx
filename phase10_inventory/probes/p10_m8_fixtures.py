#!/usr/bin/env python3
"""M8-Fixture-Bau (P10-Plan §4, Register BT-11, D-14): fünf gemeine Screenshots mit
bekannter Antwort, dazu ein echtes UI-Bild aus `docs/screenshots/`.

Die Fragen sind bewusst so gebaut, dass die Antwort **aus den Pixeln alone** entscheidbar
und **vor dem Lauf schon bekannt** ist — dieselbe Regel wie `sichtpruefung_
automation_conventions.md` §Vision: ein Modell, das eine bekannte Antwort verneint, fällt.
Kategorien aus dem Plan: Beinahe-Duplikate · Farbnuancen · leere Flächen · überlappende
Panels · falsche Markierung.

Fixtures leben unter `phase10_inventory/probes/fixtures/` — das sind Messwerkzeuge, keine
Sichtprüfungs-Bilder, und gehören deshalb NICHT nach `docs/screenshots/` (dorthin kommen nur
Belege echten UI-Verhaltens).
"""
from __future__ import annotations

import json
from pathlib import Path

from PIL import Image, ImageDraw, ImageFont

DIR = Path(__file__).resolve().parent / "fixtures"
DIR.mkdir(exist_ok=True)
REPO_ROOT = Path(__file__).resolve().parents[2]

try:
    FONT = ImageFont.truetype(
        str(REPO_ROOT / "phase5_ui/webui/static/fonts/InterVariable.woff2"), 20
    )
    FONT_BIG = ImageFont.truetype(
        str(REPO_ROOT / "phase5_ui/webui/static/fonts/InterVariable.woff2"), 30
    )
except Exception:
    FONT = ImageFont.load_default()
    FONT_BIG = FONT

QUESTIONS: dict[str, dict] = {}


def _panel(img: ImageDraw, x0, y0, x1, y1, title) -> None:
    img.rounded_rectangle([x0, y0, x1, y1], radius=10, fill=(28, 33, 40), outline=(90, 100, 112))
    img.text((x0 + 16, y0 + 12), title, fill=(220, 226, 235), font=FONT_BIG)


def near_duplicate() -> None:
    """Kategorie Beinahe-Duplikate: zwei Panels, die sich in GENAU einem Text unterscheiden
    („Aktie-7" vs „Aktie-1"). Frage zählt die Differenz — wer „identisch" antwortet, fällt."""
    for variant, label in (("a", "AKTIE-7"), ("b", "AKTIE-1")):
        img = Image.new("RGB", (900, 420), (11, 13, 16))
        d = ImageDraw.Draw(img)
        _panel(d, 40, 40, 860, 380, "Depot-Abgleich")
        d.text((60, 120), f"Referenz: {label}", fill=(120, 200, 255), font=FONT)
        d.text((60, 180), "Menge: 42", fill=(200, 205, 212), font=FONT)
        d.text((60, 240), "Status: offen", fill=(200, 205, 212), font=FONT)
        img.save(DIR / f"m8_near_duplicate_{variant}.png")
    QUESTIONS["near_duplicate"] = {
        "images": ["m8_near_duplicate_a.png", "m8_near_duplicate_b.png"],
        "q": "Diese beiden Bilder sehen fast gleich aus. Nenne die EINE Zeile, in der sie sich unterscheiden (Wortlaut beider Werte).",
        "known": "Referenz-Zeile: AKTIE-7 (Bild 1) vs. AKTIE-1 (Bild 2); Menge/Status identisch.",
        "judge_contains": [["AKTIE-7", "AKTIE-1", "7", "1"]],
    }


def color_nuance() -> None:
    """Kategorie Farbnuancen: zwei Statuspunkte, einer ist ROT getönt, der andere GRÜN —
    beide dunkel und klein. Wer behauptet, beide seien gleichfarbig, fällt."""
    img = Image.new("RGB", (900, 300), (11, 13, 16))
    d = ImageDraw.Draw(img)
    _panel(d, 40, 40, 860, 260, "Dienste")
    d.ellipse([80, 150, 116, 186], fill=(140, 30, 30), outline=(200, 60, 60))
    d.text((130, 152), "alpha-dienst", fill=(200, 205, 212), font=FONT)
    d.ellipse([420, 150, 456, 186], fill=(25, 105, 60), outline=(60, 180, 110))
    d.text((470, 152), "beta-dienst", fill=(200, 205, 212), font=FONT)
    img.save(DIR / "m8_color_nuance.png")
    QUESTIONS["color_nuance"] = {
        "images": ["m8_color_nuance.png"],
        "q": "Welcher der beiden Dienste (alpha-dienst / beta-dienst) trägt den ROTEN Punkt?",
        "known": "alpha-dienst trägt den roten Punkt, beta-dienst den grünen.",
        "judge_contains": [["alpha"]],
    }


def empty_area() -> None:
    """Kategorie leere Flächen: ein Dialog mit EINEM Panel und einem großen leeren Bereich.
    Fallen-Klassiker (P9-Sichtung: das Modell erfand drei Panels in einem leeren Bild)."""
    img = Image.new("RGB", (1000, 500), (11, 13, 16))
    d = ImageDraw.Draw(img)
    _panel(d, 250, 120, 750, 380, "Archivieren")
    d.text((280, 220), "Soll das Element wirklich archiviert werden?", fill=(200, 205, 212), font=FONT)
    d.rounded_rectangle([560, 310, 710, 355], radius=8, fill=(62, 141, 243))
    d.text((590, 322), "Archivieren", fill=(255, 255, 255), font=FONT)
    # Rest: leer. Absichtlich.
    img.save(DIR / "m8_empty_area.png")
    QUESTIONS["empty_area"] = {
        "images": ["m8_empty_area.png"],
        "q": "Wie viele Panels/Fenster stehen im Bild, und was ist der Titel des Panels?",
        "known": "Genau EIN Panel mit dem Titel „Archivieren“; der Rest ist leer.",
        "judge_contains": [["ein", "1", "eine"], ["Archivieren"]],
    }


def overlapping() -> None:
    """Kategorie überlappende Panels: zwei überlappende Karten — zählt, welches oben liegt
    ( deckt den Titel des anderen)."""
    img = Image.new("RGB", (900, 500), (11, 13, 16))
    d = ImageDraw.Draw(img)
    _panel(d, 60, 60, 560, 420, "Grundplan")
    _panel(d, 380, 180, 840, 460, "Gegenansicht")
    d.text((90, 200), "Inhalt: Planung", fill=(200, 205, 212), font=FONT)
    d.text((410, 300), "Inhalt: Revision", fill=(200, 205, 212), font=FONT)
    img.save(DIR / "m8_overlapping.png")
    QUESTIONS["overlapping"] = {
        "images": ["m8_overlapping.png"],
        "q": "Zwei Panels überlappen. Welcher Titel ist VOLL lesbar und welches Panel liegt oben?",
        "known": "„Gegenansicht“ liegt oben und ist voll lesbar; „Grundplan“ wird überdeckt.",
        "judge_contains": [["Gegenansicht"]],
    }


def wrong_marking() -> None:
    """Kategorie falsche Markierung: vier Zeilen, die DRITTE ist markiert (Akzentbalken) —
    wer oben-stehend als markiert angibt, fällt (P9-Sichtungsfehler-Kategorie)."""
    img = Image.new("RGB", (700, 420), (11, 13, 16))
    d = ImageDraw.Draw(img)
    _panel(d, 40, 40, 660, 380, "Aufgaben")
    rows = ["Erste Aufgabe", "Zweite Aufgabe", "Dritte Aufgabe", "Vierte Aufgabe"]
    for i, label in enumerate(rows):
        y = 120 + i * 60
        if i == 2:
            d.rounded_rectangle([60, y - 6, 640, y + 38], radius=8, fill=(38, 68, 110))
            d.rectangle([60, y - 6, 66, y + 38], fill=(62, 141, 243))
        d.text((84, y), label, fill=(230, 234, 240), font=FONT)
    img.save(DIR / "m8_wrong_marking.png")
    QUESTIONS["wrong_marking"] = {
        "images": ["m8_wrong_marking.png"],
        "q": "Welche der vier Aufgaben ist markiert (hervorgehobene Zeile)?",
        "known": "Die DRITTE Aufgabe (Dritte Aufgabe) ist markiert.",
        "judge_contains": [["dritte", "Dritte", "3."]],
    }


def real_screenshot() -> None:
    """Echtes UI-Bild mit bekannter Antwort — der V119-Beleg aus P8.6 (damals korrekt
    beantwortet): zwei Radio-Buttons, „als Text-Link im Text" ist markiert."""
    QUESTIONS["real_radiogruppe"] = {
        "images": [str(REPO_ROOT / "docs/screenshots/c4_p8519_01_radiogruppe_im_dialog.png")],
        "q": "Welcher Radio-Button in diesem Dialog ist markiert?",
        "known": "„als Text-Link im Text“ ist markiert (V119-Beleg aus P8.6).",
        "judge_contains": [["Text-Link", "text-link"]],
    }


def real_ein_panel() -> None:
    """Frage 7 — die echte Falle vom 2026-10-05 (Konventionen, Vision-Abschnitt): reine
    Layout-Frage ans Einstellungen-Menü. Das Bild zeigt genau EIN Panel; qwen3-vl:8b erfand
    damals „drei Panels: Übersicht, alpha, VERKNÜPFUNGEN". Bekannt, aus Messung/Code, nicht
    Augenmaß: sichtbare_panels == ['settings-menu'] (2026-10-05); Titel „Einstellungen“
    **zentriert** — P9-AM, `app.css` `#settings-menu h2 { text-align: center }` (nur dieses
    Panel; Unterfenster-Titel bleiben links, P9-AT). Korrektur 2026-10-19: die erste Fassung
    dieser Frage urteilte „linksbündig“ nach dem z. B.-Beispiel der Konventionen — der Code
    widerlegte es. Das Bild ist p9_settings_01_menue_1440.png (Bild 04 heißt explizit
    drei_panels)."""
    QUESTIONS["real_ein_panel"] = {
        "images": [str(REPO_ROOT / "docs/screenshots/p9_settings_01_menue_1440.png")],
        "q": "Ein Panel oder drei? Wie viele Panels/Fenster zeigt das Bild, welchen Titel trägt das Panel, und ist der Titel links oder mittig ausgerichtet?",
        "known": "Genau EIN Panel (Einstellungen-Menü), Titel „Einstellungen“, mittig (zentriert, P9-AM).",
        "judge_contains": [
            ["genau ein", "nur ein", "ein panel", "ein fenster", "ein einzel", "einzelnes", "one panel", "1 panel", "eins", "einzigen"],
            ["einstellungen"],
            ["mittig", "zentriert", "centered", "center"],
        ],
    }


def main() -> int:
    near_duplicate()
    color_nuance()
    empty_area()
    overlapping()
    wrong_marking()
    real_screenshot()
    real_ein_panel()
    (DIR / "questions.json").write_text(
        json.dumps(QUESTIONS, ensure_ascii=False, indent=2) + "\n"
    )
    print(f"{len(QUESTIONS)} Fixtures + Fragen nach {DIR}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
