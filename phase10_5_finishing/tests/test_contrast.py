"""Wächter für den Kontrast der Vorsicht-Beschriftung (P10.5 Block 7, Schritt 7.5 — UI-5, D-7).

Liest die Token-Werte aus `app.css` und rechnet WCAG-Kontrast von `--caution` gegen alle
Farbstops der Standardknopf-Fläche (Ruhe und Hover). Der Test rechnet nur — das Aussehen im
Browser bleibt Sache der Sichtung (7.4)."""
from __future__ import annotations

import re
from pathlib import Path

CSS = Path(__file__).resolve().parents[2] / "phase5_ui/webui/static/app.css"


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


def test_caution_text_meets_wcag_aa() -> None:
    caution = _token("caution")
    assert re.fullmatch(r"#[0-9A-Fa-f]{6}", caution), f"--caution muss ein Hex-Wert sein, ist {caution!r}"
    for flaeche in ("btn-std-fill", "btn-std-fill-hover"):
        for stop in re.findall(r"#[0-9A-Fa-f]{6}", _token(flaeche)):
            assert kontrast(caution, stop) >= 4.5, f"--caution auf {stop} ({flaeche}): {kontrast(caution, stop):.2f}:1"


def test_old_token_would_fail() -> None:
    """Gegenlauf im Code: der alte Wert (#E5484D) liegt auf der Ruhefläche bei 4,38:1."""
    assert kontrast("#E5484D", "#0C1C31") < 4.5
