"""Das Baustellenregister und sein L3-Archiv: **derselbe Stand, an zwei Orten**.

**Warum es ein Archiv gibt (2026-10-24, Block 11.4).** Das Register stand auf **41.347 B** —
über dem Softcap (40.960 B), damit `doc_health` rot und das Deploy-Gate zu. Der Grund ist
**strukturell**: jede abgehakte Zeile wächst durch ihren Nachweis, und der Nachweis bleibt für
immer stehen. Ohne Schnitt wäre das Register nach jedem Block wieder über der Grenze.

**Der Schnitt (Phase-9-Präzedenz).** Die **geschlossenen** Zeilen (Ziel-Spalte mit ✅, ohne
⬜/🟡) tragen im Register einen **Zeiger** auf `REGISTER_ARCHIVE.md`; das Archiv trägt die
**vollen** Zeilen **verbatim**. Die **offenen** Zeilen (KA-1, ED-1, AL-1, UI-2, BT-11, …) stehen
mit ihrem vollständigen Befund **im Register** — das Register ist die Arbeitsliste, und was noch
arbeitet, gehört dorthin.

**Was dieser Wächter bindet.** Er prüft, dass Register und Archiv **denselben** Stand tragen:
jede geschlossene Zeile des Registers steht **byte-gleich** im Archiv, und die Spalten, die der
Zeiger-zeile im Register erhalten bleiben (ID, Posten, Herkunft, Gr., Risiko, Entsch., Ziel), sind
in beiden **gleich**. Ein Register, das die geschlossenen Zeilen kürzt, ohne das Archiv zu
führen, verliert die Belege — das wäre der Fehler, den dieser Wächter verhindert.

**Und die Luft (P10.5-2).** Die Abnahmezeile P10.5-2 verlangt für **beide** Dateien — Register
und INDEX — **mindestens 3.000 B unter der Grenze**. Diese Reserve ist kein Komfort, sondern
Voraussetzung: die nächsten Blöcke (11.5–11.8, 12, Z) legen Zeilen an.
"""
from __future__ import annotations

import re
from pathlib import Path

REPO_ROOT = Path(__file__).resolve().parents[2]
REGISTER = REPO_ROOT / "phase10_inventory" / "BAUSTELLENREGISTER.md"
REGISTER_ARCHIV = REPO_ROOT / "phase10_inventory" / "REGISTER_ARCHIVE.md"
INDEX = REPO_ROOT / "docs" / "INDEX.md"

SOFTCAP_BYTES = 40 * 1024
RESERVE_BYTES = 3000

#: Der Zeiger, den eine geschlossene Zeile im Register trägt.
ZEIGER = "→ 📦 `REGISTER_ARCHIVE.md`"

#: Die Spalten, die im Register erhalten bleiben: ID, Posten, Herkunft, Gr., Risiko, Entsch., Ziel.
ERHALTENE_SPALTEN = (1, 2, 3, 5, 6, 7, 8)


def _zeilen(text: str) -> dict[str, list[str]]:
    """Alle Registerzeilen je ID — aus den Tabellen des Registers."""
    zeilen: dict[str, list[str]] = {}
    for line in text.split("\n"):
        if not line.startswith("|"):
            continue
        spalten = line.split("|")
        if len(spalten) < 10:
            continue
        kennung = spalten[1].strip()
        if not kennung or kennung.startswith("-") or kennung == "ID":
            continue
        zeilen.setdefault(kennung, []).append(line)
    return zeilen


def _geschlossen(line: str) -> bool:
    """**Geschlossen** = die Ziel-Spalte nennt ein ✅ und **kein** ⬜ und **kein** 🟡."""
    ziel = line.split("|")[-2].strip()
    return "✅" in ziel and "⬜" not in ziel and "🟡" not in ziel


def test_every_closed_row_in_the_register_points_to_an_archive_row():
    """Jede geschlossene Zeile des Registers trägt den **Zeiger** — und im Archiv steht zu
    derselben ID eine Zeile. Fehlt die, ist der Beleg weg: das Register nennt den Zeiger, und
    im Archiv steht nichts dazu."""
    assert REGISTER_ARCHIV.exists(), f"das Archiv fehlt: {REGISTER_ARCHIV}"
    register = REGISTER.read_text(encoding="utf-8")
    archiv = REGISTER_ARCHIV.read_text(encoding="utf-8")
    zeiger_zeilen = [z for zs in _zeilen(register).values() for z in zs if ZEIGER in z]
    assert zeiger_zeilen, "das Register trägt keine Zeiger-Zeile — der Wächter prüfte nichts"
    for zeile in zeiger_zeilen:
        kennung = zeile.split("|")[1].strip()
        voll = [z for z in _zeilen(archiv).get(kennung, []) if _geschlossen(z)]
        assert voll, (
            f"das Register zeigt für {kennung} auf das Archiv, aber das Archiv trägt keine "
            "geschlossene Zeile dazu — der Beleg ist weg"
        )
        assert ZEIGER not in voll[0], (
            f"die Archivzeile für {kennung} trägt selbst einen Zeiger — das Archiv trägt die "
            "vollen Zeilen"
        )


def test_the_archive_carries_no_unknown_ids():
    """Das Archiv darf keine Zeile führen, die das Register nicht (mehr) kennt — das wäre ein
    Beleg ohne Gegenstück."""
    register_ids = set(_zeilen(REGISTER.read_text(encoding="utf-8")))
    archiv_ids = set(_zeilen(REGISTER_ARCHIV.read_text(encoding="utf-8")))
    unbekannt = archiv_ids - register_ids
    assert not unbekannt, f"das Archiv trägt Zeilen, die das Register nicht kennt: {unbekannt}"


def test_the_pointer_rows_keep_their_columns():
    """Die Zeiger-Zeile im Register und die Vollzeile im Archiv müssen in den **erhaltenen**
    Spalten **gleich** sein — sonst ist der Zeiger eine Lüge mit Verzögerung."""
    register = REGISTER.read_text(encoding="utf-8")
    archiv = REGISTER_ARCHIV.read_text(encoding="utf-8")
    for kennung, zeilen in _zeilen(register).items():
        for zeile in zeilen:
            if ZEIGER not in zeile:
                continue
            voll = [z for z in _zeilen(archiv).get(kennung, []) if _geschlossen(z)]
            assert voll, f"im Register steht ein Zeiger für {kennung}, im Archiv nichts"
            kurz_sp = zeile.split("|")
            voll_sp = voll[0].split("|")
            for spalte in ERHALTENE_SPALTEN:
                assert kurz_sp[spalte] == voll_sp[spalte], (
                    f"Zeile {kennung}, Spalte {spalte}: Register {kurz_sp[spalte]!r} != "
                    f"Archiv {voll_sp[spalte]!r}"
                )


def test_the_register_keeps_the_open_rows_in_full():
    """Die **offenen** Zeilen stehen mit ihrem Befund im Register — das Archiv ist kein
    Friedhof für unerledigte Arbeit."""
    register = REGISTER.read_text(encoding="utf-8")
    for kennung in ("KA-1", "ED-1", "AL-1", "UI-2", "BT-11"):
        zeilen = [z for z in _zeilen(register).get(kennung, [])]
        assert zeilen, f"die Zeile {kennung} fehlt im Register"
        assert ZEIGER not in zeilen[0], (
            f"die Zeile {kennung} ist noch offen und darf **nicht** auf das Archiv zeigen"
        )


def test_the_register_and_the_index_keep_their_reserve():
    """**P10.5-2:** Register und INDEX je **mindestens 3.000 B** unter dem Softcap."""
    for datei, name in ((REGISTER, "das Register"), (INDEX, "die INDEX")):
        groesse = datei.stat().st_size
        luft = SOFTCAP_BYTES - groesse
        assert luft >= RESERVE_BYTES, (
            f"{name} ist {groesse} B — nur {luft} B Luft unter dem Softcap "
            f"({SOFTCAP_BYTES} B); P10.5-2 verlangt {RESERVE_BYTES} B"
        )


def test_the_index_names_the_register_and_the_archive():
    """Die Karte muss beide Dateien nennen — sonst findet sie niemand."""
    index = INDEX.read_text(encoding="utf-8")
    for pfad in ("phase10_inventory/BAUSTELLENREGISTER.md", "phase10_inventory/REGISTER_ARCHIVE.md"):
        assert pfad in index, f"docs/INDEX.md nennt {pfad} nicht"
        zeile = [z for z in index.split("\n") if z.startswith("- [") and pfad in z]
        assert zeile, f"docs/INDEX.md hat keine Kartenzeile für {pfad}"
        assert re.search(r"\*\*(\d[\d.]*) B\*\*", zeile[0]), (
            f"die Kartenzeile für {pfad} nennt keine Bytezahl"
        )
