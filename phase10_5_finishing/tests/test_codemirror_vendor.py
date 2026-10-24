"""Der vendorte Editor muss **exakt** die Datei sein, die in `THIRD_PARTY_LICENSES.md` steht.

**Warum ein Wächter und nicht ein Kommentar.** `static/vendor/codemirror/` liegt im Repo und
wird **nachgeladen** — ohne Build-Schritt, ohne Prüfsumme beim Ausliefern. Ein still
ausgetauschtes `codemirror.min.js` (etwa durch eine falsche Version aus dem Netz) wäre im
Oberflächentest **unsichtbar**: die Oberfläche lädt, der Editor arbeitet, der Roundtrip
schlägt vielleicht nicht einmal fehl — nur das Verhalten ändert sich leise. Deshalb stehen
die SHA-256-Summen **im Lizenzdokument** (das ohnehin mitgeliefert wird) und werden hier
gegen die Dateien im Baum geprüft.

**Gegenprobe (b):** der Prüfer muss auch dann rot werden, wenn eine **fremde** Datei
gleicher Größe untergeschoben wird. Der Test ersetzt deshalb den Inhalt einer Vendordatei
(durch einen gleichlangen Fremdinhalt) und verlangt, dass **dieselbe** Prüfung rot wird.
"""
from __future__ import annotations

import hashlib
import re
from pathlib import Path

REPO_ROOT = Path(__file__).resolve().parents[2]
VENDOR_DIR = REPO_ROOT / "phase5_ui/webui/static/vendor/codemirror"
LIZENZ = REPO_ROOT / "phase5_ui/THIRD_PARTY_LICENSES.md"

#: Die Dateien, die der Editor nachlädt (Plan §Block 11, Schritt 11.1).
ERWARTETE_DATEIEN = (
    "codemirror.min.js",
    "codemirror.min.css",
    "markdown.min.js",
    "xml.min.js",
    "meta.min.js",
)


def _tabelle() -> dict[str, str]:
    """Die SHA-256-Summen aus dem Lizenzdokument — die Quelle der Wahrheit."""
    text = LIZENZ.read_text(encoding="utf-8")
    treffer = dict(
        re.findall(r"^\| `([\w.\-]+)` \| `([0-9a-f]{64})` \|", text, flags=re.MULTILINE)
    )
    return treffer


def _pruefe(verzeichnis: Path, summen: dict[str, str]) -> list[str]:
    """Die Prüfung selbst — sie bekommt Verzeichnis und Summen übergeben, damit die
    Gegenprobe sie mit einem manipulierten Baum aufrufen kann."""
    befunde = []
    for name, erwartet in summen.items():
        pfad = verzeichnis / name
        if not pfad.exists():
            befunde.append(f"{name}: fehlt")
            continue
        ist = hashlib.sha256(pfad.read_bytes()).hexdigest()
        if ist != erwartet:
            befunde.append(f"{name}: SHA-256 {ist} != {erwartet}")
    return befunde


def test_every_vendor_file_exists():
    for name in ERWARTETE_DATEIEN:
        pfad = VENDOR_DIR / name
        assert pfad.exists(), f"die vendorte Datei fehlt: {name}"
        assert pfad.stat().st_size > 0, f"die vendorte Datei ist leer: {name}"


def test_the_license_document_names_every_vendor_file():
    summen = _tabelle()
    for name in ERWARTETE_DATEIEN:
        assert name in summen, f"{name} steht nicht mit SHA-256 im Lizenzdokument"


def test_the_vendor_files_match_their_recorded_checksums():
    """Die eigentliche Prüfung: die Dateien im Baum sind die dokumentierten."""
    summen = _tabelle()
    assert summen, "das Lizenzdokument nennt keine SHA-256-Summe — der Wächter prüft ins Leere"
    befunde = _pruefe(VENDOR_DIR, summen)
    assert not befunde, "die vendorten Dateien weichen vom Lizenzdokument ab: " + "; ".join(befunde)


def test_a_swapped_vendor_file_would_be_rejected(tmp_path):
    """Die Gegenprobe: derselbe Prüfer, ein manipulierter Baum — er muss rot werden."""
    summen = _tabelle()
    name = "codemirror.min.js"
    ziel = tmp_path / name
    original = (VENDOR_DIR / name).read_bytes()
    # **Gleichlangiger** Fremdinhalt: eine Größenprüfung würde ihn nicht erwischen.
    ziel.write_bytes(b"x" * len(original))
    befunde = _pruefe(tmp_path, summen)
    assert befunde, "ein untergeschobener CodeMirror wurde nicht erkannt"
    assert any(name in b for b in befunde)
