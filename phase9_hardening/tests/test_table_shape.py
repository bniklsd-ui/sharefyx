"""Gate/Z (2026-10-04) — eine Markdown-Tabellenzeile mit einem rohen `|` ist **unsichtbarer Text**.

**Der Fund.** Beim Messen der Softcap-Uberschreitung dieses Heads (die offene Frage „wie viele
Session-Blöcke bleiben im Head?") fiel auf, dass die §-Modulstatus-Tabelle 14 Datenzeilen hat und
**zwei davon kaputt sind**: in Zeile 28 (Step B) und Zeile 38 (Gate/Z) steht ein rohes ` | ` **im
Text der Statusspalte**. GFM trennt Zellen an `|`, also hat jede dieser Zeilen **vier** Zellen
statt drei — und der Renderer legt den Teil hinter dem Rohstrich in eine **Phantom-Spalte**, die
die Tabelle nicht hat. Der Leser sieht die Zelle bis zum Rohstrich und danach nichts mehr.

**Gemessen, nicht geschätzt: 4.097 B dieses Heads waren in der gerenderten Ansicht unsichtbar**
(2.990 B in Zeile 28, 1.107 B in Zeile 38) — darunter der ganze V153-Block des Step B und der
Schluss des Gate/Z-Eintrags. Der Text war da, lesbar, nur nicht *sichtbar*. Das ist dieselbe
Fehlerklasse wie der ` · `-Trenner in der `updated:`-Kette (`test_updated_chain.py`): die Datei ist
in jeder Textsuche vollständig, im Fließtext fehlt etwas, und kein Wächter meldet es, weil kein
Wächter die Form prüft.

**Warum es niemand gemerkt hat:** eine Tabelle mit *mehr* Zellen als ihr Kopf sieht in einer
Textausgabe nicht kaputt aus — sie sieht nach einer weiteren Spalte aus. Erst die Zeichenzählung
macht es zum Befund. Das ist die dritte Ausprägung derselben Sorte in dieser Phase (nach dem
Ketten-Präfix und dem fehlenden Feld) und dieselbe Lehre: **eine maschinell gepflegte Struktur
braucht einen Wächter, nicht Aufmerksamkeit.**

**Der Wächter** prüft repo-weit, dass jede Tabellenzeile so viele Zellen hat wie ihre Kopfzeile.
Zwei Details, ohne die er entweder falsch-grün oder falsch-rot würde:

* `\\|` ist die **korrekte** Form und wird nicht gezählt — das Repo benutzt sie an 17 Stellen
  (`initial\\|reset`, `Image \\| str`), sie ist also Konvention und kein Zufall.
* Zeilen in einem ```-Fence sind Prosa über Masken (`awk '/^\\| P8-/'` in einem 📕-Plan) und
  werden übersprungen, sonst hätte der erste Durchlauf eine Fundstelle mehr, die keine ist.

**Was hier nicht gebaut wird:** die 15 Fundstellen in fremden Dateien (abgeschlossene Phasen,
`ROADMAP.md`, zwei 📕-Snapshots, der P9-Plan, das Step-A-Runbook). Sie stehen in
`KNOWN_OFFENDERS` **mit Datei und Zeilennummer**, damit die Liste nicht wachsen kann, ohne dass es
auffällt — Muster wie `KNOWN_OFFENDERS` in `test_updated_chain.py` und `EXEMPT_HEX` in
`test_static_routes.py`. Wer eine repariert, streicht den Eintrag; der zweite Test sorgt dafür,
dass das nicht stillschweigend passiert.

**Gegenprobe statt Augenschein:** `test_the_checker_itself_catches_what_it_claims` füttert dem
Prüfer die drei Formen ein — eine saubere Tabelle, eine zu breite Zeile, ein `\\|` — und verlangt
für jede das richtige Urteil.
"""
import re
from pathlib import Path

REPO_ROOT = Path(__file__).resolve().parents[2]
SKIP_DIRS = {".git", ".venv", ".pytest_cache", "node_modules", ".agents", ".claude", ".playwright-mcp"}

# Zellenzahl ohne die **escaped** Pipes. Der negative Blickblick ist das ganze Argument: ohne ihn
# wäre jede korrekt escapete Zelle (17 Stellen im Repo) ein Verstoß.
CELL_SPLIT_RE = re.compile(r"(?<!\\)\|")
# Eine Trennzeile `|---|---|---|` zählt nicht als Datenzeile.
SEPARATOR_RE = re.compile(r"^\|[\s:|-]+\|$")

# datei -> [(Zeile, Zellenzahl-Kopf, Zellenzahl-Zeile), …] — **alle gemessen** am 2026-10-04 mit
# demselben Prüfer, den dieser Test benutzt. Zeilennummern stehen mit drin, weil eine Ausnahme ohne
# Ort ein Gerücht ist.
KNOWN_OFFENDERS: dict[str, list[tuple[int, int, int]]] = {
    "docs/concepts/phase4_auth_plan.md": [(112, 3, 2)],
    "docs/concepts/phase5_ui_plan.md": [(316, 2, 3)],
    "docs/concepts/phase8_6_ui_polish_plan.md": [(66, 3, 4)],  # 📕
    "phase6_shares/GLOBAL_SEARCH_PLAN.md": [(309, 3, 2), (310, 3, 2)],
    "docs/concepts/phase9_hardening_plan.md": [(1245, 3, 4), (1251, 3, 4), (1252, 3, 4), (1253, 3, 4), (1255, 3, 4)],
    "docs/concepts/phase9_hardening_block_doing_plan.md": [(172, 3, 5)],
    "docs/concepts/phase9_hardening_block_trace_plan.md": [(185, 3, 11)],  # 📕
    "phase2_mcp/CLAUDE.md": [(125, 5, 4)],
    "phase8_6_ui_polish/CLAUDE.md": [(131, 5, 6)],  # abgeschlossene Phase
    "phase9_hardening/step_a/RUNBOOK_STEP_A.md": [(917, 3, 4)],
}
# `phase9_hardening/CLAUDE.md` steht **nicht** in der Liste: die beiden Fundstellen dort sind am
# 2026-10-04 behoben (verlustfrei, ` · ` bzw. entfernt), und genau das ist der Punkt dieser Datei.


def cell_count(line: str) -> int:
    """Zellenzahl einer Tabellenzeile; escaped Pipes zählen nicht mit."""
    stripped = line.strip()
    if not stripped.startswith("|"):
        return 0
    return len(CELL_SPLIT_RE.split(stripped.strip("|")))


def table_defects(text: str) -> list[tuple[int, int, int]]:
    """Alle (Zeile, Kopf, Zeile) im Text, bei denen die Zellenanzahl nicht zum Kopf passt.

    Eine nicht-`|`-Zeile beendet die laufende Tabelle — so wird aus zwei direkt aufeinander
    folgenden Blöcken nicht eine gemeinsame Tabelle, und ein Codeblock mit Masken zählt nicht.
    """
    defects: list[tuple[int, int, int]] = []
    expected: int | None = None
    in_fence = False
    for lineno, line in enumerate(text.split("\n"), start=1):
        if line.lstrip().startswith("```"):
            in_fence = not in_fence
            expected = None
            continue
        if in_fence:
            continue
        if not line.lstrip().startswith("|"):
            expected = None
            continue
        if SEPARATOR_RE.match(line.strip()):
            continue
        found = cell_count(line)
        if expected is None:
            expected = found
            continue
        if found != expected:
            defects.append((lineno, expected, found))
    return defects


def offenders() -> list[str]:
    found: list[str] = []
    for path in sorted(REPO_ROOT.rglob("*.md")):
        rel_path = path.relative_to(REPO_ROOT)
        if SKIP_DIRS & set(rel_path.parts):
            continue
        rel = rel_path.as_posix()
        defects = table_defects(path.read_text(encoding="utf-8", errors="replace"))
        if not defects:
            continue
        if rel in KNOWN_OFFENDERS and defects == KNOWN_OFFENDERS[rel]:
            continue  # gemessen, benannt, unverändert — siehe Moduldocstring
        rendered = ", ".join(f"{ln}: Kopf {exp} vs. Zeile {got}" for ln, exp, got in defects)
        found.append(f"{rel}: {rendered}")
    return found


def hidden_bytes(line: str, expected: int) -> int:
    """Wie viele Bytes dieser Zeile landen in Zellen, die es in der Tabelle nicht gibt.

    `expected` ist die Zellenzahl der Kopfzeile — ohne sie wäre die Kennzahl nicht berechenbar,
    denn „hidden" heißt immer *hidden relativ zu einer Spaltenzahl*.
    """
    parts = CELL_SPLIT_RE.split(line.strip().strip("|"))
    return sum(len(p.encode("utf-8")) for p in parts[expected:])


def test_no_unnamed_file_hides_table_cells_in_a_phantom_column():
    assert offenders() == []


def test_the_known_offenders_still_look_exactly_as_measured():
    """Gegenprobe: die Ausnahmeliste darf nicht still veralten.

    Wer eine Fundstelle repariert, muss sie hier streichen — sonst meldet dieser Test den Veteranen
    als *unbekannten* Verstoß und der eigentliche Wächter bleibt grün. Umgekehrt verschwindet ein
    reparierter Eintrag nicht einfach: er taucht als frischer Verstoß auf. Muster wie in
    `test_updated_chain.py`.
    """
    measured: dict[str, list[tuple[int, int, int]]] = {}
    for path in sorted(REPO_ROOT.rglob("*.md")):
        rel_path = path.relative_to(REPO_ROOT)
        if SKIP_DIRS & set(rel_path.parts):
            continue
        rel = rel_path.as_posix()
        if rel not in KNOWN_OFFENDERS:
            continue
        defects = table_defects(path.read_text(encoding="utf-8", errors="replace"))
        if defects or KNOWN_OFFENDERS[rel]:
            measured[rel] = defects
    assert measured == KNOWN_OFFENDERS, (
        "Die Ausnahmeliste stimmt nicht mehr mit dem Repo überein — entweder ist eine Fundstelle "
        "repariert (dann hier streichen, die Korrektur aber in der Session festhalten) oder ein "
        "neuer Verstoß ist dazugekommen (dann in KNOWN_OFFENDERS mit Zeilennummer aufnehmen)"
    )


def test_the_checker_itself_catches_what_it_claims():
    """Gegenprobe am Prüfer, nicht am Datenbestand."""
    sauber = "| a | b |\n|---|---|\n| 1 | 2 |\n| 3 | 4 |\n"
    zu_breit = "| a | b |\n|---|---|\n| 1 | 2 | 3 |\n"
    zu_schmal = "| a | b |\n|---|---|\n| nur eins |\n"
    escaped = "| a | b |\n|---|---|\n| `x \\| y` | 2 |\n"
    zwei_tabellen = "| a | b |\n|---|---|\n| 1 | 2 |\n\nFließtext\n\n| a | b |\n|---|---|\n| 1 | 2 | 3 |\n"
    im_fence = "```\n| a | b | c |\n```\n"

    assert table_defects(sauber) == []
    assert table_defects(zu_breit) == [(3, 2, 3)]
    assert table_defects(zu_schmal) == [(3, 2, 1)]
    assert table_defects(escaped) == []
    assert table_defects(zwei_tabellen) == [(9, 2, 3)]
    assert table_defects(im_fence) == []


def test_the_p9_module_status_table_shows_every_row_it_writes():
    """Der Regressionstest auf den Fund selbst: alle Zeilen der Tabelle haben drei Zellen.

    Als **Anzahl der Zeilen** formuliert, nicht als Byte-Zahl — die Aussage, die er tragen soll,
    ist „kein Status verschwindet mehr in einer Phantom-Spalte", nicht „es sind genau 4.097 B".
    14 ist Kopf + 13 Datenzeilen (0, A–H, doing, trace, E (Extra), Gate/Z).
    """
    text = (REPO_ROOT / "phase9_hardening" / "CLAUDE.md").read_text(encoding="utf-8")
    head = text.split("\n## Modulstatus\n", 1)[1].split("\n## ", 1)[0]
    rows = [l for l in head.split("\n") if l.lstrip().startswith("|") and not SEPARATOR_RE.match(l.strip())]
    assert len(rows) == 14, f"erwartet Kopf + 13 Datenzeilen, gefunden {len(rows)}"
    assert all(cell_count(r) == 3 for r in rows), [
        f"Zeile mit {cell_count(r)} Zellen: {r[:70]}" for r in rows if cell_count(r) != 3
    ]


def test_the_two_repaired_rows_kept_their_text():
    """Gegenprobe zur Reparatur: die Bytes sind nicht weg, sie stehen woanders.

    ` · ` statt ` | ` in Step B, und in Gate/Z wanderte der Rohstrich aus dem Codespan heraus.
    Beides verliert kein Zeichen — dieser Test verhindert, dass eine künftige „Kürzung" die
    Behebung für eine Auslassung hält. **Geprüft wird nur die §-Modulstatus-Tabelle:** die
    kaputte Form kommt im Session-Block und in der `updated:`-Kette weiterhin *wörtlich* vor,
    weil beide den Defekt beschreiben — das ist gewollt und wäre als Treffer falsch gemeldet.
    """
    text = (REPO_ROOT / "phase9_hardening" / "CLAUDE.md").read_text(encoding="utf-8")
    table = text.split("\n## Modulstatus\n", 1)[1].split("\n## ", 1)[0]
    assert "Add-on) · ~~🟡 ~~ M3-Anteil" in table
    assert "Fäden mit `updated: `-Präfix + 3 mit ` · `-Trenner" in table
    assert "Fäden mit ` | updated: `-Präfix" not in table
    # Die beiden geretteten Passagen stehen noch drin — echte Bytes, nicht nur Trenner.
    assert "V153 entschieden und einer der beiden Plan-Wege nachweislich unbaubar" in table
    assert "für `rotate_index_updates.sh` unsichtbar**" in table


def test_hidden_bytes_is_measured_not_guessed():
    """Die Kennzahl, mit der der Fund benannt ist: sie muss an einem Beispiel stimmen."""
    assert hidden_bytes("| a | b |", 2) == 0                # nichts außerhalb der zwei Spalten
    assert hidden_bytes("| a | b | c |", 2) == len(" c ")  # eine Phantom-Zelle
    # Zwei Phantom-Zellen: 3 + 3 Bytes, die Trenner dazwischen zählen nicht mit.
    assert hidden_bytes("| a | b | c | d |", 2) == len(" c ") + len(" d ")
