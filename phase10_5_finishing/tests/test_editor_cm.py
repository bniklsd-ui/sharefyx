"""Wächter für den Nachlader des Editors (P10.5 Block 11, Schritt 11.2 — ED-1).

**Was dieser Wächter prüft:** dass die **Verdrahtung** existiert — die Reihenfolge (CSS,
dann der Kern, dann die Modus-Dateien), das **eine** gecachte Promise, der Fehlerpfad
`null` (Rohmodus als Notausgang, ED-5) und die Übereinstimmung der Dateiliste mit dem
Verzeichnis `static/vendor/codemirror/`.

**Was er ausdrücklich nicht prüft:** das Verhalten im Browser. Dafür ist die Probe des
Blocks da (Playwright, Wegwerf-Instanz). Ein Wächter, der die Reaktionszeit behauptet, aber
nur Quelltext liest, wäre die Fehlerklasse aus dem Phase-9-Befund „ein Wächter, der etwas
anderes prüft als er behauptet".

**Der dritte Test ist der wichtigste:** die Dateiliste des Laders muss **exakt** den
Dateien im Vendor-Verzeichnis entsprechen. Ein neues Vendor-File, das der Lader nicht
kennt, wäre sonst ein stiller Fehler — der Editor liefe ohne den Modus, ohne dass irgendwo
etwas rot wird. Die Gegenprobe dazu steht in `test_codemirror_vendor.py` (SHA-256).
"""
from __future__ import annotations

import re
from pathlib import Path

REPO_ROOT = Path(__file__).resolve().parents[2]
JS = REPO_ROOT / "phase5_ui/webui/static/js"
VENDOR = REPO_ROOT / "phase5_ui/webui/static/vendor/codemirror"
LADER = JS / "editor_cm.js"


def _text() -> str:
    return LADER.read_text(encoding="utf-8")


def _skriptliste() -> list[str]:
    """Die Dateinamen aus `VENDOR_SCRIPTS` (in der Reihenfolge des Quelltexts)."""
    block = re.search(r"const VENDOR_SCRIPTS = \[(.*?)\];", _text(), flags=re.DOTALL)
    assert block, "der Lader nennt keine Skriptliste"
    return re.findall(r'"([^"]+)"', block.group(1))


def test_the_loader_is_a_module_and_exports_the_entry_point():
    text = _text()
    assert "export function ensureCodeMirror()" in text
    assert "export function isLoaded()" in text


def test_the_loader_loads_the_css_before_the_scripts():
    """Erst das CSS, dann die Skripte: ohne CSS ist der Editor da, aber unsichtbar."""
    text = _text()
    assert "await ladeCss(" in text
    assert text.index("await ladeCss(") < text.index("await ladeScript(")


def test_the_loader_loads_the_core_before_the_modes():
    """`codemirror.min.js` zuerst, `markdown.min.js` zuletzt — der Modus braucht den Kern,
    und die Modus-Dateien brauchen einander (`meta`, `xml`)."""
    liste = _skriptliste()
    assert liste[0] == "codemirror.min.js", liste
    assert liste[-1] == "markdown.min.js", liste
    assert liste.index("meta.min.js") < liste.index("xml.min.js") < liste.index("markdown.min.js")


def test_the_script_list_matches_the_vendor_directory():
    """**Die Liste des Laders gegen das Verzeichnis.** Ein Vendor-File, das der Lader nicht
    kennt, wäre ein stiller Fehler (der Editor liefe ohne den Modus)."""
    im_baum = sorted(p.name for p in VENDOR.glob("*.js"))
    assert sorted(_skriptliste()) == im_baum, (
        f"der Lader lädt {_skriptliste()}, im Verzeichnis liegen {im_baum}"
    )


def test_the_promise_is_cached():
    """Der Editor wird höchstens einmal geladen — ein zweiter Aufruf wartet auf dasselbe
    Promise (sonst lädt jeder Aufrufer die Dateien erneut)."""
    text = _text()
    assert "if (!ladePromise) ladePromise = lade();" in text


def test_a_failure_resolves_with_null_instead_of_throwing():
    """Der Fehlerpfad: `null` — der Editor bleibt Textarea (Rohmodus, ED-5). Ein Wurf nach
    oben würde den Editor unbenutzbar machen, statt auf die Notausgang-Lösung zurückzufallen."""
    text = _text()
    assert "catch (err)" in text
    assert "return null;" in text
    assert "throw " not in text, "der Lader darf nicht werfen — der Rohmodus ist der Notausgang"
