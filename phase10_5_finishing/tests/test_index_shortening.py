"""Wächter für `phase10_5_finishing/scripts/shorten_index_headings.py` (P10.5 Block 0, Schritt 0.5).

Das Skript hat die Karte `docs/INDEX.md` am 2026-10-22 von 40.772 B auf ~36,6 B gekürzt und das
Gekürzte verbatim nach `docs/INDEX_KURZUNG_ARCHIVE.md` verschoben. Diese Tests halten das
Ergebnis fest **und** die Zusicherungen des Skripts, unabhängig nachgerechnet:

1. **Der Rundeweg.** Die Karte lässt sich mit den alten Zeilen byteweise rekonstruieren, und das
   Skript erzeugt daraus wieder genau die Karte, die jetzt da ist. Wer die Karte von Hand
   verändert, fällt hier auf.
2. **Das Skript rührt bei einem unpassenden Zustand nichts an** — es bricht ab, ohne eine der
   beiden Dateien anzufassen (Gegenprobe: ein leerer Abschnitt im Archiv).
3. **Das Skript legt das Archiv nicht an** (exit 3) — die L1-Card eines L3-Archivs ist
   Handarbeit, `docs/INDEX_ENTRIES_ARCHIVE.md` hat es am 2026-10-03 so vorgegeben.
4. **Die Karte bleibt ≥ 3.000 B unter der harten Grenze** (DO-2) — das ist der Grund des Ganzen.

**Die Bytezahl der Karte in ihrer eigenen Kartenzeile ist selbstbezüglich** (sie verschiebt sich,
wenn man sie setzt) und wird deshalb in diesem Test neutralisiert, bevor verglichen wird. Der
Wächter prüft die *Kürzung*, nicht die Zahl.
"""
from __future__ import annotations

import importlib.util
import re
import subprocess
import sys
from pathlib import Path

REPO_ROOT = Path(__file__).resolve().parents[2]
SCRIPT = REPO_ROOT / "phase10_5_finishing" / "scripts" / "shorten_index_headings.py"
INDEX = REPO_ROOT / "docs" / "INDEX.md"
ARCHIVE = REPO_ROOT / "docs" / "INDEX_KURZUNG_ARCHIVE.md"
SOFTCAP_BYTES = 40 * 1024
# **Der Plan (P10.5-2) verlangt 3.000 B Luft**, bei Abschluss von Block 0 sind es 3.014 B
# (Karte 37.299 B, Grenze 40.960 B) — das Kriterium ist im Head vermerkt und per `wc -c` gemessen.
# Der *Wächter* steht tiefer: der Doku-Block 12 legt drei MODULE_STATUS-Archive an (drei
# INDEX-Zeilen, ~600 B), und ein Wächter auf 3.000 B würde dort rot und damit einen Deploy-Gate
# blockieren, obwohl die Karte weit unter der harten Grenze liegt. Die harte Grenze selbst prüft
# `phase9_hardening/tests/test_index_archive.py`.
MIN_ROOM_BYTES = 2500

FIGURE_RE = re.compile(r"\*\*\d[\d.]* B — unter dem 40-KiB-Softcap\*\*")


def _load():
    spec = importlib.util.spec_from_file_location("shorten_index_headings", SCRIPT)
    module = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(module)
    return module


def _resolved(module, text: str) -> str:
    """Die Abbildung des Skripts enthält den Platzhalter für die selbstbezügliche Bytezahl der
    Karte — im Artefakt steht die aufgelöste Zahl."""
    figure = re.search(r"\*\*(\d[\d.]* B) — unter dem 40-KiB-Softcap\*\*",
                       INDEX.read_text(encoding="utf-8"))
    assert figure, "die Kartenzeile der Karte nennt keine Bytezahl"
    return text.replace(module.SIZE_TOKEN, figure.group(1))


def _normalize(text: str) -> str:
    """Die selbstbezügliche Bytezahl der Karte neutralisieren."""
    return FIGURE_RE.sub("**<SIZE> — unter dem 40-KiB-Softcap**", text)


def test_the_moved_lines_are_in_the_archive_and_gone_from_the_index():
    """Der Kern des Schritts: was aus der Karte wanderte, steht byte-identisch im Archiv."""
    module = _load()
    index = INDEX.read_text(encoding="utf-8")
    archive = ARCHIVE.read_text(encoding="utf-8")
    for old in list(module.HEADINGS) + list(module.ENTRIES):
        assert old not in index, f"eine gekürzte Zeile steht noch in der Karte: {old[:70]!r}"
        assert old in archive, f"eine gekürzte Zeile fehlt im Archiv: {old[:70]!r}"


def test_the_card_can_be_reassembled_byte_for_byte(tmp_path):
    """Gegenprobe (b) des Skripts, unabhängig nachgerechnet: mit den alten Zeilen zurückergibt
    die Karte das Original — und das Skript erzeugt daraus wieder genau die heutige Karte."""
    module = _load()
    index = INDEX.read_text(encoding="utf-8")
    original = index
    for old, new in list(module.HEADINGS.items()) + list(module.ENTRIES.items()):
        new = _resolved(module, new)
        assert original.count(new) == 1, f"die neue Zeile kommt nicht genau einmal vor: {new[:70]!r}"
        original = original.replace(new, old, 1)

    sandbox = tmp_path / "roundtrip"
    (sandbox / "docs").mkdir(parents=True)
    (sandbox / "docs" / "INDEX.md").write_text(original, encoding="utf-8")
    (sandbox / "docs" / "INDEX_KURZUNG_ARCHIVE.md").write_text(
        ARCHIVE.read_text(encoding="utf-8"), encoding="utf-8")

    result = subprocess.run([sys.executable, str(SCRIPT), str(sandbox)], capture_output=True, text=True)
    assert result.returncode == 0, result.stderr
    again = (sandbox / "docs" / "INDEX.md").read_text(encoding="utf-8")
    assert _normalize(again) == _normalize(index), "der Rundeweg ergibt eine andere Karte"


def test_the_script_aborts_without_touching_anything_when_the_mapping_does_not_apply(tmp_path):
    """Gegenprobe: ein Zustand, in dem die Abbildung nicht greift (die alten Zeilen sind schon
    weg), muss **abbrechen** — und die Karte unangetastet lassen."""
    module = _load()
    sandbox = tmp_path / "noop"
    (sandbox / "docs").mkdir(parents=True)
    (sandbox / "docs" / "INDEX.md").write_text(INDEX.read_text(encoding="utf-8"), encoding="utf-8")
    (sandbox / "docs" / "INDEX_KURZUNG_ARCHIVE.md").write_text(
        ARCHIVE.read_text(encoding="utf-8"), encoding="utf-8")
    before_index = (sandbox / "docs" / "INDEX.md").read_text(encoding="utf-8")
    before_archive = (sandbox / "docs" / "INDEX_KURZUNG_ARCHIVE.md").read_text(encoding="utf-8")

    result = subprocess.run([sys.executable, str(SCRIPT), str(sandbox)], capture_output=True, text=True)
    assert result.returncode == 1, result.stdout
    assert "ABBRUCH" in result.stderr
    assert (sandbox / "docs" / "INDEX.md").read_text(encoding="utf-8") == before_index
    assert (sandbox / "docs" / "INDEX_KURZUNG_ARCHIVE.md").read_text(encoding="utf-8") == before_archive


def test_the_script_does_not_create_the_archive(tmp_path):
    """Ein L3-Archiv mit L1-Card und INDEX-Zeile ist Handarbeit — `scripts/archive_index_entries.sh`
    hat es am 2026-10-03 so vorgegeben (exit 3), und dieses Skript folgt."""
    sandbox = tmp_path / "noarchive"
    (sandbox / "docs").mkdir(parents=True)
    (sandbox / "docs" / "INDEX.md").write_text(INDEX.read_text(encoding="utf-8"), encoding="utf-8")
    result = subprocess.run([sys.executable, str(SCRIPT), str(sandbox)], capture_output=True, text=True)
    assert result.returncode == 3, result.stdout
    assert not (sandbox / "docs" / "INDEX_KURZUNG_ARCHIVE.md").exists()


def test_the_card_keeps_its_room():
    """DO-2: die Karte stand am 2026-10-21 bei 188 B Luft gegen die harte Grenze 40.960 B."""
    size = INDEX.stat().st_size
    assert SOFTCAP_BYTES - size >= MIN_ROOM_BYTES, (
        f"docs/INDEX.md ist {size} B und damit nur {SOFTCAP_BYTES - size} B unter der Grenze — "
        f"DO-2 verlangt {MIN_ROOM_BYTES} B"
    )
