"""Die statische Nutzlast muss **jede Datei genau einmal** zählen (P10.5 Block 11, Schritt 11.7).

**Warum ein Wächter und keine Zeile in der Doku.** `phase5_ui/scripts/ui_budget.py` zählt die
Nutzlast des Erstaufrufs (`js/*.js`, `app.css`, die Fonts) und — seit Block 11.2 — den
**nachgeladenen Editor** unter `vendor/`. Beides ist eine **Liste von Dateien**, und eine Liste
von Dateien vergisst zuverlässig: eine neue Datei unter `static/` (das Wortzeichen `logo.svg`
stand bis 2026-10-24 **außerhalb** jeder Zählung und damit **außerhalb** des gemessenen
Erstaufrufs) fällt durch, ohne dass jemand etwas bemerkt. Die Messung meldete weiterhin
„grün" — sie maß simply eine Nutzlast, die es so nicht gibt.

**Die Zählung ist eine Zusage.** Der Plan (Schritt 11.7) verlangt genau das: eine Funktion
`static_payload_files(static_dir) -> (Erstaufruf, nachgeladen)` und einen Wächter, der prüft,
dass **jede** Datei unter `static/` **genau einmal** in einer der beiden Listen steht.

**Zwei Dateien sind bewusst nicht dabei** — und der Wächter nennt sie, statt sie zu schweigen:

* `app.html` — kommt als Shell über `/ui/` in die Zeile „Erstaufruf bis interaktiv" (dort wird
  sie gzip gezählt, nicht als statische Datei).
* die **Lizenztexte** (`fonts/OFL.txt`) — die lädt der Browser **nicht**; sie liegen dem Repo
  bei. Eine Zählung würde den Erstaufruf **größer** rechnen, als er ist.

**Die Zahlen, die daraus folgen (P10.5-H).** Der Erstaufruf liegt bei **206,4 KB** (Korridor
250 KB), der nachgeladene Editor bei **69,7 KB** (Korridor 80 KB).
"""
from __future__ import annotations

import importlib.util
import sys
from pathlib import Path

import pytest

REPO_ROOT = Path(__file__).resolve().parents[2]
SCRIPT = REPO_ROOT / "phase5_ui" / "scripts" / "ui_budget.py"
STATIC_DIR = REPO_ROOT / "phase5_ui" / "webui" / "static"

#: Die Korridore aus dem Plan (P10.5-H) — in Bytes.
ERSTAUFRUF_MAX = 250 * 1024
EDITOR_MAX = 80 * 1024


def _load():
    """Das Skript als Modul laden. Es importiert die Server-Pakete (`webui`, `storage`, …) —
    die liegen im Dev-venv installiert; ohne sie könnte der Wächter die Dateiauswahl nicht
    prüfen, und eine **zweite** Auswahl im Test wäre die Fehlerklasse, die er verhindert.

    **Der `sys.path` wird danach wiederhergestellt (2026-10-25, P10.5 Block 13).** Das
    Einfügen der Phase-Verzeichnisse macht die **repo-lokalen** `*.egg-info` für
    `importlib.metadata` sichtbar — und damit sieht der Wächter
    `phase9_hardening/tests/test_step_h_deps.py` (der die installierten Distributionen gegen
    `constraints.txt` prüft) jede Paket-Distribution **zweimal**: einmal als editable
    Installation (mit `direct_url.json`) und einmal als nacktes `egg-info` im Repo (ohne) —
    das zweite zählt als „installiert, aber nicht gepinnt" und der Test wird **rot**, obwohl
    nichts driftet. Die Reihenfolge in `pytest.ini` (`testpaths`) hat die Phase-10.5-Tests
    **hinten** — deshalb fiel es bisher niemandem auf; in jeder anderen Reihenfolge fiel es
    auf. Der Test stellt den Zustand jetzt wieder her, statt ihn zu hinterlassen."""
    vorher = list(sys.path)
    for pfad in ("phase2_mcp", "phase4_auth", "phase5_ui", "phase1_storage"):
        eintrag = str(REPO_ROOT / pfad)
        if eintrag not in sys.path:
            sys.path.insert(0, eintrag)
    try:
        spec = importlib.util.spec_from_file_location("ui_budget_unter_test", SCRIPT)
        module = importlib.util.module_from_spec(spec)
        # **Das Modul muss in `sys.modules` stehen**, bevor es ausgeführt wird: die
        # `@dataclass`-Dekoratoren lösen ihre Annotationen über `sys.modules[cls.__module__]`
        # auf — ohne den Eintrag bekommen sie `None` und die Deklaration bricht mitten in
        # der Auswertung ab.
        sys.modules[spec.name] = module
        spec.loader.exec_module(module)
    finally:
        sys.path[:] = vorher
    return module


def _alle_dateien(static_dir: Path) -> set[Path]:
    return {p for p in static_dir.rglob("*") if p.is_file()}


def _ungedeckte_dateien(static_dir: Path, erstaufruf: list, nachgeladen: list) -> set[Path]:
    """Die Dateien unter `static/`, die **keine** der beiden Listen nennt.

    Die Ausnahmen (`app.html`, Lizenztexte) sind hier **einmal** festgeschrieben — der Test
    und seine Gegenprobe benutzen **dieselbe** Prüfung. Eine zweite Auswahl im Test wäre die
    Fehlerklasse, die dieser Wächter verhindert.
    """
    ausgenommen = {static_dir / "app.html"} | {
        p for p in _alle_dateien(static_dir) if p.suffix.lower() == ".txt"
    }
    erwartet = _alle_dateien(static_dir) - ausgenommen
    return erwartet - set(erstaufruf) - set(nachgeladen)


def _assert_vollstaendig(static_dir: Path, erstaufruf: list, nachgeladen: list) -> None:
    """**Die Prüfung selbst** — der echte Wächter *und* die Gegenprobe benutzen **diese**
    eine Funktion.

    **Warum das so gebaut ist:** eine Gegenprobe, die eine *zweite* Kopie der Prüfung
    benutzt, beweist nur, dass die Kopie das Beispiel erkennt — nicht, dass der Wächter es
    erkennt. Der Fehler, den dieser Wächter verhindert, ist genau der Fall „die Datei steht in
    keiner Liste, und niemand merkt es": das Wortzeichen `logo.svg` stand bis 2026-10-24 in
    **keiner** Liste, und `ui_budget.py` meldete weiterhin „grün". Eine zweite Auswahl im Test
    wäre dieselbe Fehlerklasse in neuer Form.
    """
    alle = erstaufruf + nachgeladen
    assert len(alle) == len(set(alle)), (
        "eine Datei steht in beiden Listen — sie wird doppelt gezählt: "
        f"{[str(p) for p in alle if alle.count(p) > 1]}"
    )

    ungedeckt = _ungedeckte_dateien(static_dir, erstaufruf, nachgeladen)
    assert not ungedeckt, (
        "die Auswahl der statischen Nutzlast kennt diese Datei(en) nicht — sie werden "
        "**nicht** gezählt, obwohl der Browser sie laedt: "
        f"{sorted(str(p.relative_to(static_dir)) for p in ungedeckt)}"
    )

    ausgenommen = {static_dir / "app.html"} | {
        p for p in _alle_dateien(static_dir) if p.suffix.lower() == ".txt"
    }
    zu_viel = set(alle) - (_alle_dateien(static_dir) - ausgenommen)
    assert not zu_viel, (
        "die Auswahl zaehlt Dateien, die es unter `static/` nicht gibt: "
        f"{sorted(str(p) for p in zu_viel)}"
    )


def test_every_static_file_is_counted_exactly_once():
    """Jede Datei unter `static/` steht in **genau einer** der beiden Listen."""
    module = _load()
    erstaufruf, nachgeladen = module.static_payload_files(STATIC_DIR)
    _assert_vollstaendig(STATIC_DIR, erstaufruf, nachgeladen)


def test_the_editor_is_counted_as_loaded_later():
    """Der Editor (CodeMirror) wird **nachgeladen**, nicht im Erstaufruf mitgezählt — sonst
    wäre die Erstaufruf-Zahl falsch (der Browser laedt ihn beim Oeffnen eines Items)."""
    module = _load()
    erstaufruf, nachgeladen = module.static_payload_files(STATIC_DIR)
    assert nachgeladen, "die nachgeladene Liste ist leer — der Editor wird nicht gezaehlt"
    for pfad in nachgeladen:
        assert pfad.is_relative_to(STATIC_DIR / "vendor"), (
            f"{pfad.name} liegt nicht unter `vendor/` — es wird nicht nachgeladen"
        )
    for pfad in erstaufruf:
        assert not pfad.is_relative_to(STATIC_DIR / "vendor"), (
            f"{pfad.name} liegt unter `vendor/` und wird doch im Erstaufruf gezaehlt"
        )


def test_the_two_corridors_hold():
    """**P10.5-50:** Erstaufruf ≤ 250 KB, Editor ≤ 80 KB — und beide Zahlen werden hier
    **gemessen**, nicht aus dem Skript-Durchlauf übernommen."""
    module = _load()
    erstaufruf, nachgeladen = module.static_payload_files(STATIC_DIR)

    erstaufruf_bytes = 0
    for pfad in erstaufruf:
        if pfad.suffix == ".woff2":
            erstaufruf_bytes += pfad.stat().st_size
        else:
            erstaufruf_bytes += module._gz(pfad.read_bytes())
    assert erstaufruf_bytes < ERSTAUFRUF_MAX, (
        f"der Erstaufruf ist {erstaufruf_bytes} B und damit über dem Korridor "
        f"({ERSTAUFRUF_MAX} B)"
    )

    editor_bytes = sum(module._gz(p.read_bytes()) for p in nachgeladen)
    assert editor_bytes < EDITOR_MAX, (
        f"der nachgeladene Editor ist {editor_bytes} B und damit über dem Korridor "
        f"({EDITOR_MAX} B)"
    )


def test_the_watcher_is_not_vacuous(tmp_path):
    """**Die Gegenprobe.** Eine Datei, die die Auswahl **nicht** kennt, muss den Wächter rot
    machen — sonst prüfte er nichts.

    Der Fehler, den der Wächter verhindert, ist genau dieser: das Wortzeichen `logo.svg`
    stand bis 2026-10-24 in **keiner** Liste, und die Messung meldete weiterhin „grün".

    **Die Gegenprobe benutzt dieselbe Prüfung wie der Wächter** (`_assert_vollstaendig`) —
    nicht eine zweite, ähnliche: sonst beweist sie nur sich selbst.
    """
    module = _load()
    falsch = tmp_path / "static"
    (falsch / "js").mkdir(parents=True)
    (falsch / "js" / "app.js").write_text("x", encoding="utf-8")
    (falsch / "app.css").write_text("x", encoding="utf-8")
    (falsch / "logo.svg").write_text("x", encoding="utf-8")
    (falsch / "app.html").write_text("<html>", encoding="utf-8")
    # **Die Datei, die niemand zaehlt** -- genau so war es mit `logo.svg`.
    (falsch / "manifest.json").write_text("{}", encoding="utf-8")

    erstaufruf, nachgeladen = module.static_payload_files(falsch)
    with pytest.raises(AssertionError) as fehler:
        _assert_vollstaendig(falsch, erstaufruf, nachgeladen)
    assert "manifest.json" in str(fehler.value), (
        f"die Gegenprobe greift an der falschen Stelle: {fehler.value}"
    )
