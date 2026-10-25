"""Wächter für den Kontrast der Vorsicht-Beschriftung (P10.5 Block 7, Schritt 7.5 — UI-5, D-7).

Liest die Token-Werte aus `app.css` und rechnet WCAG-Kontrast von `--caution` gegen die
Standardknopf-Fläche (Ruhe und Hover). Der Test rechnet nur — das Aussehen im Browser
bleibt Sache der Sichtung (7.4).

**[2026-10-25, P10.5 Block 13.3 — die Fläche ist jetzt *halbtransparent*.]** Vorher standen
in `--btn-std-fill` **deckende** Hex-Stops (`#0C1C31` …), die man direkt als Fläche rechnen
konnte. Jetzt sind es zwei Deckkraft-Stufen eines Blaus (`rgba(62,141,243,.20)` …) — die
Fläche hängt damit vom **Untergrund** ab, und der Untergrund muss **mitgerechnet** werden:
sonst prüft der Wächter eine Farbe, die es im Browser nicht gibt.

**Die Lehre aus dieser Fassung (der Fehler, den die erste Fassung gemacht hätte):** die alte
Fassung suchte in den Tokens nach `#rrggbb` — bei rgba-Stops findet sie **keine** und
prüft **nichts**, ohne zu fehlschlagen. Ein Wächter, der nichts findet, ist grün und
blind. Deshalb wird hier **ausdrücklich geprüft**, dass die Fläche überhaupt eine
auflösbare Deckkraft ist, und der Untergrund wird mitgerechnet.

Die Untergründe: alle Flächen, auf denen ein Standardknopf tatsächlich sitzen kann. Der
**schlimmste** Fall (der hellste Untergrund) entscheidet — `--surface-raised` (der
Editor-Kopf, #1B2027) ist es; das ist der Ort, an dem die Vorsicht-Aktion „Archivieren"
tatsächlich steht.
"""
from __future__ import annotations

import re
from pathlib import Path

CSS = Path(__file__).resolve().parents[2] / "phase5_ui/webui/static/app.css"

# Die Untergründe, auf denen ein Standardknopf sitzen kann (Token -> Wert). Der schlimmste
# Fall (der hellste) entscheidet — deshalb sind es alle, nicht einer.
UNTERGRUENDE = {
    "surface": "#14181D",          # Karten, Listenflaechen
    "surface-raised": "#1B2027",   # Editor-Kopf (dort steht „Archivieren")
    "panel-body-head": "#161C24",  # Kopf des Text-Panels (dort steht die Werkzeugleiste)
    "rail-top": "#0E1116",         # die Rail
}


def _token(name: str) -> str:
    m = re.search(r"^\s*--" + re.escape(name) + r":\s*([^;]+);", CSS.read_text(encoding="utf-8"), re.M)
    assert m, f"Token --{name} fehlt in app.css"
    return m.group(1).strip()


def _luminanz(hex_: str) -> float:
    h = hex_.lstrip("#")
    kanaele = [int(h[i:i + 2], 16) / 255 for i in (0, 2, 4)]
    r, g, b = [c / 12.92 if c <= 0.03928 else ((c + 0.055) / 1.055) ** 2.4 for c in kanaele]
    return 0.2126 * r + 0.7152 * g + 0.0722 * b


def kontrast(a: str, b: str) -> float:
    hell, dunkel = sorted((_luminanz(a), _luminanz(b)), reverse=True)
    return (hell + 0.05) / (dunkel + 0.05)


def _rgb(hex_: str) -> tuple[float, float, float]:
    h = hex_.lstrip("#")
    return tuple(float(int(h[i:i + 2], 16)) for i in (0, 2, 4))  # type: ignore[return-value]


def _mischung(farbe: tuple[float, float, float], deckkraft: float,
              untergrund: tuple[float, float, float]) -> tuple[float, float, float]:
    """Die Farbe, die der Browser zeigt: die Deckkraft ueber dem Untergrund."""
    return tuple(f * deckkraft + u * (1 - deckkraft) for f, u in zip(farbe, untergrund))


def _stops(token_wert: str) -> list[tuple[tuple[float, float, float], float]]:
    """Die Farbstopps eines Tokens: `rgba(r,g,b,a)` oder `#rrggbb` (deckend)."""
    out = []
    for m in re.finditer(r"rgba?\(\s*([\d.]+)\s*,\s*([\d.]+)\s*,\s*([\d.]+)\s*(?:,\s*([\d.]+)\s*)?\)",
                         token_wert):
        r, g, b = (float(m.group(i)) for i in (1, 2, 3))
        a = float(m.group(4)) if m.group(4) is not None else 1.0
        out.append(((r, g, b), a))
    for m in re.finditer(r"#[0-9A-Fa-f]{6}", token_wert):
        out.append((_rgb(m.group(0)), 1.0))
    return out


def _hex(farbe: tuple[float, float, float]) -> str:
    return "#" + "".join(f"{max(0, min(255, round(c))):02X}" for c in farbe)


def test_caution_text_meets_wcag_aa() -> None:
    caution = _token("caution")
    assert re.fullmatch(r"#[0-9A-Fa-f]{6}", caution), f"--caution muss ein Hex-Wert sein, ist {caution!r}"
    for flaeche in ("btn-std-fill", "btn-std-fill-hover"):
        stops = _stops(_token(flaeche))
        assert stops, (f"--{flaeche} enthaelt keine auflösbare Farbe — der Test würde sonst "
                       "nichts prüfen und trotzdem grün sein")
        for farbe, deckkraft in stops:
            for name, untergrund_hex in UNTERGRUENDE.items():
                gemischt = _mischung(farbe, deckkraft, _rgb(untergrund_hex))
                wert = kontrast(caution, _hex(gemischt))
                assert wert >= 4.5, (
                    f"--caution auf {_hex(gemischt)} (--{flaeche} {farbe} a={deckkraft} "
                    f"ueber --{name} {untergrund_hex}): {wert:.2f}:1"
                )


def test_the_button_fill_is_translucent() -> None:
    """**Die Fläche ist halbtransparent** (Block 13.3) — mit mindestens einer echten
    Deckkraft unter 1. Sonst waere der Kontrast-Wächter oben blind (er rechnet gegen
    `--surface-raised`, und eine deckende Flaeche braucht diese Rechnung nicht)."""
    stops = _stops(_token("btn-std-fill"))
    assert stops, "--btn-std-fill traegt keine Farbe"
    assert any(a < 1.0 for _, a in stops), (
        "--btn-std-fill muss mindestens eine halbtransparente Deckkraft tragen "
        "(Block 13.3: das blau-leicht-transparente Design)"
    )


def test_old_token_would_fail() -> None:
    """Gegenlauf im Code: der alte Wert (#E5484D) liegt auf der alten deckenden Ruhefläche
    bei 4,38:1. Auf der **neuen** (halbtransparenten, helleren) Fläche faellt er noch
    deutlicher durch."""
    assert kontrast("#E5484D", "#0C1C31") < 4.5
    neu = _mischung((62, 141, 243), 0.20, _rgb("#1B2027"))
    assert kontrast("#E5484D", _hex(neu)) < 4.5
