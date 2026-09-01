#!/usr/bin/env python3
"""Generiert den Lucide-Icon-Sprite-Block in `app.html`.

Liest die vendored SVGs unter `phase5_ui/vendor/lucide/icons/*.svg`, baut fuer jedes einen
`<symbol id="i-NAME" viewBox="0 0 24 24">…</symbol>`-Block und schreibt das Ergebnis zwischen
die Marker `<!-- ICONS:BEGIN -->` / `<!-- ICONS:END -->` in `phase5_ui/webui/static/app.html`.

Idempotent: ein zweiter Lauf erzeugt byte-identische Ausgabe. Wird von Hand aufgerufen, ist
kein Build-Step zur Laufzeit (P5-T "kein Build-Step" bleibt gewahrt; ein neuer Icon-Name
kommt nicht ohne menschliches Dafuer).

Vendoring-Format (Lucide-Original, 24x24 viewBox, fill="none" stroke="currentColor"):
    <svg xmlns=… viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2"
         stroke-linecap="round" stroke-linejoin="round">
      <path d="…"/>
      <line …/>
      <circle …/>
    </svg>

Sprite-Block:
    <svg id="icon-sprite" hidden xmlns="http://www.w3.org/2000/svg" aria-hidden="true">
      <symbol id="i-house" viewBox="0 0 24 24" fill="none" stroke="currentColor"
              stroke-width="2" stroke-linecap="round" stroke-linejoin="round">
        <path d="…"/>
      </symbol>
      …
    </svg>

Verwendung im Markup:
    <svg class="icon" aria-hidden="true"><use href="#i-house"></use></svg>

CSS-Stroke + Stroke-Width sitzen auf dem `<symbol>`, weil `<use>` keine der Attribute aus
dem SVG-Wurzelelement des Originals erbt -- nur die Attribute, die das Symbol selbst traegt.
Stroke/Fill-Wechsel via CSS-Klasse `.icon { stroke: currentColor; … }` funktionieren, weil das
Symbol fill/stroke auf "none"/"currentColor" gesetzt hat und CSS diese ueberschreiben kann
(SVG-Präsentationsattribute sind CSS-zugaenglich).
"""
from __future__ import annotations

import argparse
import re
import sys
from pathlib import Path

SCRIPT_DIR = Path(__file__).resolve().parent
REPO_ROOT = SCRIPT_DIR.parent.parent
VENDOR_DIR = REPO_ROOT / "phase5_ui" / "vendor" / "lucide" / "icons"
APP_HTML = REPO_ROOT / "phase5_ui" / "webui" / "static" / "app.html"

BEGIN_MARKER = "<!-- ICONS:BEGIN -->"
END_MARKER = "<!-- ICONS:END -->"
SPRITE_OPEN = '<svg id="icon-sprite" hidden xmlns="http://www.w3.org/2000/svg" aria-hidden="true">'
SPRITE_CLOSE = "</svg>"

# Stroke-Attribute, die wir auf das <symbol> heben. Lucide-SVGs haben sie auf dem Wurzel-<svg>;
# <use> erbt nur Attribute des Symbols, nicht des Original-Wurzel-<svg>.
ROOT_STROKE_ATTRS = (
    'fill="none"',
    'stroke="currentColor"',
    'stroke-width="2"',
    'stroke-linecap="round"',
    'stroke-linejoin="round"',
)

INNER_RE = re.compile(r"<svg[^>]*>(.*)</svg>", re.DOTALL)


def symbol_for(name: str, inner: str) -> str:
    """Baut einen <symbol>-Block aus einem Lucide-SVG-Inhalt."""
    # Inneres aufraeumen: fuehrende/folgende Whitespace + Leerzeilen normalisieren
    body = inner.strip()
    body = re.sub(r"\n\s+", "\n      ", body)
    attrs = " ".join(ROOT_STROKE_ATTRS)
    return (
        f'  <symbol id="i-{name}" viewBox="0 0 24 24" {attrs}>\n'
        f"      {body}\n"
        f"  </symbol>"
    )


def load_icons(vendor_dir: Path) -> list[tuple[str, str]]:
    """Laedt alle vendored Icons in alphabetischer Reihenfolge (deterministisches Sprite)."""
    if not vendor_dir.is_dir():
        raise SystemExit(f"Vendor-Verzeichnis fehlt: {vendor_dir}")
    icons: list[tuple[str, str]] = []
    for svg in sorted(vendor_dir.glob("*.svg")):
        name = svg.stem
        content = svg.read_text(encoding="utf-8")
        m = INNER_RE.search(content)
        if not m:
            raise SystemExit(f"Kann {svg} nicht parsen -- kein <svg>…</svg> gefunden.")
        icons.append((name, m.group(1)))
    if not icons:
        raise SystemExit(f"Keine Icons in {vendor_dir} gefunden.")
    return icons


def build_sprite(icons: list[tuple[str, str]]) -> str:
    """Baut den vollstaendigen Sprite-Block (inkl. Marker + umschliessendem <svg>)."""
    parts = [BEGIN_MARKER, SPRITE_OPEN]
    parts.extend(symbol_for(name, inner) for name, inner in icons)
    parts.append(SPRITE_CLOSE)
    parts.append(END_MARKER)
    return "\n".join(parts)


def replace_sprite(html: str, new_sprite: str) -> str:
    """Ersetzt den Block zwischen den Markern. Wirft, wenn Marker fehlen."""
    pattern = re.compile(
        re.escape(BEGIN_MARKER) + r".*?" + re.escape(END_MARKER),
        re.DOTALL,
    )
    if not pattern.search(html):
        raise SystemExit(
            f"Marker {BEGIN_MARKER!r} / {END_MARKER!r} fehlen in {APP_HTML}."
        )
    return pattern.sub(lambda _m: new_sprite, html)


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument(
        "--check",
        action="store_true",
        help="Prueft nur, ob der aktuelle Sprite-Block mit der Vendored-Quelle uebereinstimmt; "
             "Exit 0 = aktuell, Exit 1 = Drift (App wuerde beim naechsten Lauf geupdated).",
    )
    args = parser.parse_args()

    icons = load_icons(VENDOR_DIR)
    sprite = build_sprite(icons)
    html = APP_HTML.read_text(encoding="utf-8")

    if args.check:
        pattern = re.compile(
            re.escape(BEGIN_MARKER) + r"(.*?)" + re.escape(END_MARKER),
            re.DOTALL,
        )
        m = pattern.search(html)
        if not m:
            print(f"FAIL: Marker fehlen in {APP_HTML}", file=sys.stderr)
            return 1
        current = (m.group(0) or "").strip()
        wanted = sprite.strip()
        if current == wanted:
            print(f"OK: Sprite aktuell ({len(icons)} icons, {len(current)} bytes).")
            return 0
        print(
            f"DRIFT: Sprite in {APP_HTML} weicht von vendored Quelle ab.",
            file=sys.stderr,
        )
        return 1

    new_html = replace_sprite(html, sprite)
    if new_html == html:
        print(f"OK: Sprite bereits aktuell ({len(icons)} icons).")
        return 0

    APP_HTML.write_text(new_html, encoding="utf-8")
    print(f"Geschrieben: {len(icons)} icons in {APP_HTML}.")
    return 0


if __name__ == "__main__":
    sys.exit(main())