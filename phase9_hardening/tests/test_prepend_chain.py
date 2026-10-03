"""Gate/Z (2026-10-03) — das Ketten-Voranstellen war der letzte Handgriff, und er ist gescheitert.

`scripts/rotate_index_updates.sh` rotiert eine `updated:`-Kette, aber **anfügen** musste bisher von Hand
geschehen: `phase9_hardening/CLAUDE.md` bekommt seinen neuesten Faden durch Kopieren der alten Zeile
nach vorn. **Fünfmal an einem Tag** ist dabei derselbe Fehler passiert — das `updated: `-Präfix der
Vorlage wanderte mit in den neuen Faden, oder ` | ` wurde zu ` · `. Beide Formen sind für das
Rotations-Skript unsichtbar (Anker `' | '` + ISO-Datum), und beide wurden erst *nach* dem Commit von
`test_rotate_index_updates.py` und `test_updated_chain.py` gefangen.

Deshalb `scripts/prepend_updated_chain.sh`. Die Regel, die es mechanisiert:

1. der Faden beginnt mit `JJJJ-MM-Tт (`, **ohne** `updated: `-Präfix (das Präfix gehört an die Zeile),
2. er enthält weder ` | updated: ` noch ` · ` vor einem Datum — beides erzeugt eigene, unsichtbare
   Fäden **innerhalb** des Fadens,
3. und das Ergebnis wird am echten Text gegen den Werkzeugvertrag geprüft, den
   `test_updated_chain.py` repo-weit durchsetzt.

**Gegenproben statt Augenschein:** `test_the_script_refuses_the_forms_that_hid_five_threads` füttert
ihm beide Fehlerformen ein und verlangt, dass es **abbricht** statt zu reparieren — ein Werkzeug, das
den Fehler mitnimmt, ist genau die Fehlerklasse, die es verhindern soll. Und
`test_the_script_would_have_refused_my_fifth_entry` baut den Faden nach, der in der Session vom
2026-10-03 wirklich im Head stand.
"""
import re
import subprocess
from pathlib import Path

REPO_ROOT = Path(__file__).resolve().parents[2]
SCRIPT = REPO_ROOT / "scripts" / "prepend_updated_chain.sh"

FRONTMATTER = "---\nstatus: live\npurpose: Test\nread-when: Test\ndetail: L2\nup: x\n"
# EIN Faden, und genau so einer: die Kette im Head traegt ` · ` auch **innerhalb** eines Fadens
# (sie beschreibt damit Dinge). Nur ein ` · ` **vor einem Datum** ist der Defekt.
THREAD = "2026-10-03 (**der neue Faden** — mit einem `·` und einem | im Text)"


def _head(chain_body: str) -> str:
    return FRONTMATTER + f"updated: {chain_body}\n---\n\n# Test\n\nText.\n"


def _run(target: Path, thread: str) -> subprocess.CompletedProcess:
    thread_file = target.with_suffix(".thread")
    thread_file.write_text(thread, encoding="utf-8")
    return subprocess.run(
        ["bash", str(SCRIPT), str(target), str(thread_file)],
        capture_output=True, text=True,
    )


def test_it_prepends_the_thread_and_leaves_the_rest_byte_identical(tmp_path):
    target = tmp_path / "CLAUDE.md"
    before = _head("2026-10-02 (alter Faden) | 2026-10-01 (noch einer)")
    target.write_text(before, encoding="utf-8")
    res = _run(target, THREAD)
    assert res.returncode == 0, res.stderr
    after = target.read_text(encoding="utf-8")
    # Die `updated:`-Zeile ist die 7. Zeile (Index 6) — mein erster Entwurf las Index 5 und
    # meldete genau damit einen Fehler, den das Skript nicht gemacht hatte.
    # Der neue Faden steht **vorn**, der alte Körper folgt unveraendert — genau das ist die
    # Zusage des Skripts, und deshalb steht hier die GANZE Zeile statt eines Präfixes.
    assert after.splitlines()[6] == f"updated: {THREAD} | 2026-10-02 (alter Faden) | 2026-10-01 (noch einer)"
    assert after.split("---\n", 2)[2] == before.split("---\n", 2)[2]  # Body unangetastet
    assert after.count("updated: ") == 1


def test_every_thread_of_the_result_is_visible_to_the_rotation_anchor(tmp_path):
    """Das ist die eigentliche Zusage: nach dem Lauf ist kein Faden blind."""
    target = tmp_path / "CLAUDE.md"
    target.write_text(_head("2026-10-02 (a) | 2026-10-01 (b)"), encoding="utf-8")
    assert _run(target, THREAD).returncode == 0
    body = re.search(r"^updated: (.*)$", target.read_text(encoding="utf-8"), re.M).group(1)
    starts = [m.start() for m in re.finditer(r"\d{4}-\d{2}-\d{2} \(", body)]
    assert all(i == 0 or body[:i].endswith(" | ") for i in starts), "ein Faden ist blind"
    assert len(re.split(r" \| (?=\d{4}-\d{2}-\d{2})", body)) == 3


def test_the_script_refuses_the_forms_that_hid_five_threads(tmp_path):
    """Gegenproben: beide Fehlerformen müssen **abbruchen**, nicht stillschweigend repariert werden."""
    for name, thread, marker in [
        ("Praefix im Faden", "updated: 2026-10-03 (mitgeschlepptes Praefix)", "Praefix"),
        ("' · ' vor einem Datum im Faden", "2026-10-03 (a) · 2026-10-02 (b)", "blind"),
        ("Praefix vor einem Datum im Faden", "2026-10-03 (a) | updated: 2026-10-02 (b)", "unsichtbarer Faden"),
        ("kein Datum am Anfang", "**kein Datum** vorn", "beginnen"),
    ]:
        target = tmp_path / f"{abs(hash(name))}.md"
        target.write_text(_head("2026-10-02 (alter Faden)"), encoding="utf-8")
        res = _run(target, thread)
        assert res.returncode != 0, f"{name}: das Skript haette angenommen: {res.stdout}"
        assert marker in res.stderr, f"{name}: Abbruchmeldung ohne den Grund — {res.stderr.strip()}"
        assert target.read_text(encoding="utf-8") == _head("2026-10-02 (alter Faden)"), f"{name}: Datei trotz Abbruch angefasst"


def test_it_refuses_a_head_whose_field_is_invisible(tmp_path):
    """Die Regression vom 2026-10-03: die Kette stand als nackte Zeile unter `down:`."""
    target = tmp_path / "CLAUDE.md"
    target.write_text(
        FRONTMATTER + "2026-10-02 (Faden ohne Feld) | 2026-10-01 (b)\n---\n\n# Test\n",
        encoding="utf-8",
    )
    res = _run(target, THREAD)
    assert res.returncode != 0
    assert "unsichtbar" in res.stderr


def test_the_script_would_have_refused_my_fifth_entry(tmp_path):
    """Der Faden, der am 2026-10-03 wirklich im Phase-9-Head stand — nachgebaut, nicht beschrieben."""
    target = tmp_path / "CLAUDE.md"
    target.write_text(_head("2026-10-02 (alter Faden)"), encoding="utf-8")
    real = "updated: 2026-10-03 (**P9-15 gemessen** — Bilanzen) | updated: 2026-10-03 (**früherer Faden** — x)"
    res = _run(target, real)
    assert res.returncode != 0
    assert "Praefix" in res.stderr


def test_two_runs_keep_the_newest_thread_in_front(tmp_path):
    """Reihenfolge über mehrere Läufe: der zuletzt eingefügte Faden steht vorn (newest-first)."""
    target = tmp_path / "CLAUDE.md"
    target.write_text(_head("2026-10-01 (erster Faden)"), encoding="utf-8")
    assert _run(target, "2026-10-02 (zweiter)").returncode == 0
    assert _run(target, "2026-10-03 (dritter)").returncode == 0
    body = re.search(r"^updated: (.*)$", target.read_text(encoding="utf-8"), re.M).group(1)
    assert body.startswith("2026-10-03 (dritter) | 2026-10-02 (zweiter) | 2026-10-01 (erster Faden)")
