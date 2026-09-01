"""Phase 8 Block B Step B1 (Plan §3 P8-M, achte P1-Contract-Oeffnung).

Mechanische Erkennung von `itm_`-Referenzen in Item-Bodies. Rein, kein I/O, deterministisch.

Eine Referenz hat exakt das Alphabet von `ITEM_ID_RE` aus `files.py:40` (`^itm_[0-9a-f]{8}$`)
und wird im Body **als Wort** gesucht -- Wortgrenzen ueber `\b`, weil sonst ein
`fooitm_deadbeef`-Praefix fälschlich mitmischen würde. Reihenfolge und Eindeutigkeit sind
beobachtbar: dieselbe ID an N Stellen ergibt genau einen Listeneintrag in Auftrittsreihenfolge.

Designentscheidungen, die hier stillschweigend getroffen wurden und im Plan stehen:
- Keine Markdown-Semantik. Weder Code-Block- noch Inline-Code-Ausnahmen. Eine `itm_...`-ID in
  einem Code-Block ist eine gemeinte Referenz; False-Positives sind bei 8 Hex-Zeichen hinter
  festem Praefix praktisch ausgeschlossen.
- Keine `href="#item/itm_..."`-Sonderbehandlung -- das Praefix `#item/` enthält das `itm_`-
  Token ohnehin, der Regex matcht es. Wer ein `#item/itm_foo` schreibt, bekommt genau eine
  Kante; die UI kann das spaeter (#item/-Navigation, Block B4) auf den Title mappen.
"""
from __future__ import annotations

import re


# Alphabet exakt wie ITEM_ID_RE in files.py:40 -- bei Aenderung dort MUSS dieses Pattern
# nachgezogen werden, der harte Beweis ist phase1_storage/tests/test_files.py.
ITEM_REF_RE = re.compile(r"\bitm_[0-9a-f]{8}\b")


def extract_item_refs(body: str) -> list[str]:
    """Eindeutige `itm_`-Referenzen in `body` in Auftrittsreihenfolge.

    Rein mechanisch, kein Verstehen. `body` ist der reine Markdown-Body OHNE Frontmatter
    (Store uebergibt den bereits separierten Body aus `_item_from_text`/Frontmatter-Parser).
    Liefert jede ID genau einmal, in der Reihenfolge ihres ersten Auftretens.
    """
    seen: set[str] = set()
    out: list[str] = []
    for match in ITEM_REF_RE.finditer(body):
        ref = match.group(0)
        if ref not in seen:
            seen.add(ref)
            out.append(ref)
    return out
