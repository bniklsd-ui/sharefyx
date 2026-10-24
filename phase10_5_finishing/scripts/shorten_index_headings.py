#!/usr/bin/env python3
"""shorten_index_headings.py — die INDEX-Karte von Chronik auf Stand zurückholen (P10.5 Block 0, Schritt 0.5).

**Wozu.** `docs/INDEX.md` stand am 2026-10-21 bei 40.772 B gegen die harte Grenze 40.960 B
(`phase9_hardening/tests/test_index_archive.py`). Jede Phase kostet eine Zeile, und eine Phase
allein kann die Karte über die Grenze heben. Der Plan (P10.5 §0.5) verlangt deshalb
**≥ 3.000 B Luft** und nennt als Hebel die **Abschnittsköpfe** der abgeschlossenen Phasen.

**Der Plan hat die Überschriften nicht summiert — gemessen (Befund vom 2026-10-22).** Die acht
`## Phase …`-Zeilen tragen zusammen **2.478 B**, und mit einer neuen Zeile von ≤ 120 B ist die
**Ersparnis höchstens ~1,7 B**. Aus den Köpfen allein ist die Plan-Zahl von 3.000 B **nicht
erreichbar**, auch nicht mit dem kürzestmöglichen Kopf. (Der Plan nennt „P8.6 allein ~600 B" —
das stimmt: 617 B. Nur die Summe fehlte.) Der Zielwert bleibt, der Hebel wird erweitert:

**Was dieses Skript tut — zwei Arten, beide verbatim:**
1. **Abschnittsköpfe** (`## Phase …`) wandern nach `docs/INDEX_KURZUNG_ARCHIVE.md` (📦, neu).
2. **Kartenzeilen**, deren Rest Chronik ist (Herleitung, Messreihen, Befundgeschichten),
   wandern in dieselbe Datei, in den Abschnitt „Kartenzeilen vor der Kürzung".

Beide Zugriffe sind **Zeilentausch**: eine alte Zeile (byteweise identisch) wird durch eine neue
ersetzt, die nur den **Stand** trägt. Nichts wird abgetippt, nichts wird weggelassen.

**Vier Gegenproben vor dem Schreiben** (sonst bricht das Skript ab, ohne eine der Dateien
anzufassen):
  (a) jede alte Zeile kommt im INDEX genau einmal vor
  (b) Reassemblierung: INDEX-neu, mit den alten Zeilen zurückersetzt, ist byte-identisch zum Original
  (c) jede alte Zeile steht nach dem Schreiben byte-identisch im Archiv
  (d) die Ersparnis im INDEX ist ≥ 3.000 B

**Der Karteneintrag nennt die eigene Größe** — eine selbstbezügliche Zahl, die kein Mensch
richtig setzen kann, solange die Karte sich dabei selbst verschiebt. Das Skript bestimmt sie
iterativ (einsetzen, messen, wiederholen) und bricht ab, wenn die Zahl nicht zur Ruhe kommt.

**Einmalwerkzeug.** Nach dem Lauf bricht ein zweiter Aufruf ab, weil die alten Zeilen nicht mehr in der
Karte stehen — das ist die gewollte Reaktion (kein Zustand, kein „halber Lauf"), keine Störung.

Aufruf:  phase10_5_finishing/scripts/shorten_index_headings.py [--check] [repo_root]
Exit:   0 = gekürzt (bei --check: alles in Ordnung, nichts geschrieben) · 1 = Abbruch, nichts
         geschrieben · 2 = nichts zu tun · 3 = Archiv fehlt (es wird nicht angelegt)
"""
from __future__ import annotations

import os
import re
import sys
from pathlib import Path

SIZE_TOKEN = "{{INDEX_SIZE}}"
MIN_SAVINGS = 3000
ARCHIVE_REL = "docs/INDEX_KURZUNG_ARCHIVE.md"
INDEX_REL = "docs/INDEX.md"
HEADINGS_SECTION = "## Abschnittsköpfe vor der Kürzung (2026-10-22), verbatim"
ENTRIES_SECTION = "## Kartenzeilen vor der Kürzung (2026-10-22), verbatim"

# Die datierten Nachträge sind aus den Kartenzeilen verboten — der Wächter
# `phase9_hardening/tests/test_index_archive.py :: test_no_entry_line_carries_a_dated_addendum_any_more`
# prüft das am Artefakt. Ein Kartenkopf, der sie wieder hereinholt, ist also ein Fehler.
ADDENDA_RE = re.compile(r"(?:\*\*)?\[(?:20\d\d-\d\d-\d\d)")

# ---------------------------------------------------------------- die Abbildung
# Links: die alte Zeile, byteweise so, wie sie heute in `docs/INDEX.md` steht.
# Rechts: die neue Zeile — nur noch Stand, in derselben Form wie die Kartenzeilen
# (Glyph · Größe · Ein-Satz-Stand · Zeiger).

HEADINGS: dict[str, str] = {
    "## Phase 10 — ✅ abgeschlossen 2026-10-20 (Bestandsaufnahme, kein Produktcode). P10 und P10.5 sind eine Mission: Plan P10.5 freigegeben, Tor P10-8 offen (2026-10-21). Phasenziele: Anbieter-Unabhängigkeit, Karten-Umbau (Gehirnkarte)":
        "## Phase 10 — ✅ abgeschlossen 2026-10-20 (Bestandsaufnahme, kein Produktcode; Plan P10.5)",
    "## Phase 8.6 — ✅ abgeschlossen 2026-09-19, Step Z inklusive; live als `v3.0.2` seit 2026-09-18 (SHA `1ad2665`, `health_gate` 9/9). UI-Politur mit **zwei Plaenen und drei Sichtungs-Revisionen**: Plan 1 (Step 0/V/A/B/C/D) wurde am 2026-09-12 nicht abgenommen — neun UX-Befunde statt Freigabe —, Plan 2 (E/F/G/**G-R**/H/**H-R**/**H-R-3**/J) hat sie abgearbeitet. Bilanz **45 ✅ · 5 ⚠️ · 0 ⬜ · 4 ersetzt** von 54 Zeilen; `pytest` **995**, `ui_budget` 5/5 (144,7 KB); **keine neunte P1-Contract-Oeffnung**, eine angekuendigte Tabu-Ausnahme (P8.6-AJ). Zwei `[VERIFY]` gehen offen an P9: **V118**, **V136**":
        "## Phase 8.6 — ✅ abgeschlossen 2026-09-19 (UI-Politur, live `v3.0.2`; zwei Pläne)",
    "## Phase 8.5 — ✅ abgeschlossen 2026-09-09, Step Z inklusive (Link-Picker-Politur, Titel-statt-ID-Hint, v3-Vorabritt + Deploy; schließt Phase 8 formal mit ab; Bilanz **20 ✅ · 0 🟡 · 0 ⬜**; Statusregel geändert — vom Nikinger geprüfte Wegwerf-Automatisierung zählt als live-verifiziert; Closeout kanonisch in Plan §9, Einstieg für P8.6 über `PHASE8_5_CLOSEOUT_HANDOVER.md`; Folgephasen P8.6 → v3.0.2 + P9 → v3.1.0 vorgemerkt)":
        "## Phase 8.5 — ✅ abgeschlossen 2026-09-09 (Link-Picker-Politur, live `v3.0.2`)",
    "## Phase 9 — ✅ abgeschlossen 2026-10-08; live als `v3.1.4` seit 2026-10-08 (SHA `d04c0ec`, `health_gate` 9/9). Härtungsphase: acht Steps (0 Doku-Fundament · A eigene Domain über VPS · B Watchdog · C Vision auf der RTX 3060 · D zwei Bugs · E Karten-Reload · F Schema `doing`/`assignee` · G Löschen nach `._trash/` · H `fastmcp`-Pin) plus sieben Blöcke (doing · trace · Buttons · settings · drei Bildsichtungen · feedback). 134 Abnahmezeilen, Bilanz in `ABNAHME_MATRIX.md`; zwei angekündigte P1-Öffnungen; Einstieg für P10: `PHASE9_CLOSEOUT_HANDOVER.md`":
        "## Phase 9 — ✅ abgeschlossen 2026-10-08 (Härtung: acht Steps + sieben Blöcke, live `v3.1.4`)",
    "## Phase 8 — ✅ abgeschlossen 2026-09-08 (UI-Neuanstrich v3, Verknüpfungs-Graph, drei P7-Erbposten; Bilanz 26 ✅ · 0 🟡 · 0 ⬜ — maschinell gezählt; Closeout vollzogen im selben Commit wie Phase 8.5, kein separates Handover-Dokument, Konvention seit P7)":
        "## Phase 8 — ✅ abgeschlossen 2026-09-08 (UI-Neuanstrich v3, Verknüpfungs-Graph)",
    "## Phase 7 — ✅ abgeschlossen, live-verifiziert (`e88a624`, 22 von 24 Abnahmezeilen, 2 benannte Defekte an P8 vererbt)":
        "## Phase 7 — ✅ abgeschlossen (Space-Verwaltung, Mehrfachauswahl; live `e88a624`)",
    "## Phase 6 — 🟡 code-complete, nicht vollständig live-bewiesen (Restarbeiten: Fabian-Sitzung, §9 Mehrfachauswahl, Doku-Audit)":
        "## Phase 6 — 🟡 code-complete, nicht live-bewiesen (Freigaben, Ordner, Werkzeuge)",
    "## Phase 6.5 — 🟡 code-complete, 13/14 live bestanden (P6.5-14 strukturell offen)":
        "## Phase 6.5 — 🟡 code-complete, 13/14 live bestanden (Werkzeug-Ergonomie)",
}

ENTRIES: dict[str, str] = {
    # **P10.5 Block 7.4 (2026-10-24):** zwei weitere Kartenzeilen gekuerzt, weil die Karte
    # wieder zu dicht an der Grenze stand (DO-2 verlangt 2.500 B Luft, es waren 2.162 B).
    # Der Rest der Zeilen (das Warum, die Datums-Korrekturen, die Chronik der Bild-Praefixe)
    # wandert **verbatim** nach `docs/INDEX_KURZUNG_ARCHIVE.md` -- gleiche Form wie die
    # Kuerzung vom 2026-10-22.
    '- [docs/concepts/sichtpruefung_automation_conventions.md](./concepts/sichtpruefung_automation_conventions.md) — 📗 **21.765 B** (die Kartenzeile nannte bis 2026-10-05 `~8KB` für eine seit dem 2026-09-11 ~18 KB große Datei — zwei Appends ohne Nachzug, und `doc_health` liest keine KB-Angaben, also meldete es niemand) · **Nachtrag: `docs/INDEX_ENTRIES_ARCHIVE.md`**':
        '- [docs/concepts/sichtpruefung_automation_conventions.md](./concepts/sichtpruefung_automation_conventions.md) — 📗 **21.765 B** · Konventionen der Sichtprüfungs-Automatisierung · **Nachtrag: `docs/INDEX_ENTRIES_ARCHIVE.md`**',
    '- [docs/screenshots/](./screenshots/README.md) — 📗 ~1.1MB · kanonische Ablage aller Sichtpruefungs-Bilder, pro Phase praefixiert (`sp2_*`, `c4c5_*`, `p86_block_*`, `p86_probe_*`, **`p86_smoke_*` = die 17 Gate-Belege von `v3.0.2`**, **die P9-Praefixe: `p9_step_e_*` (Karten-Reload, 2026-09-28) · **`p9_step_d_*`** (Step-D-Probe: der gestrichelte Drop-Zustand an der Space-Zeile, 2026-10-03 — Build-Beleg, **nicht** die offene Sichtfrage) · `p9_step_g_*` (Loeschen) · `p9_btn_*`/`p9_btn2_*` (Standardoptik der Knoepfe, 2026-10-01) · **`p9_btn3_*` (B17:\nVorsichtsknopf auf die Standardflaeche, 2026-10-02 — die vier aktuellen Bilder, in\n`screenshots_latest/` verlinkt)** · `p9_doing_*` (der fuenfte Eimer „In Arbeit", 2026-10-02 — **die aktuellen vier Bilder, in `screenshots_latest/` verlinkt**) · `p9_trace_0*` (**die fünf Bilder und die Probe sind am 2026-10-02 neu aufgenommen**: der alte Beleg war der Gegenlauf des trace-Blocks selbst — Probe rot, Bild 05 zeigte `beta`; Wächter `test_committed_probe_evidence.py` verhindert das) · `p9_step_a_01..04_*` (Tailscale-Infra-Beleg aus A3 — **keine Sichtpruefung**, deshalb nicht in `screenshots_latest/`) · `p9a_legacy_*` (Uebergangsfenster)**). Die `c4c5_*`-Bilder besetzen die „Sneak Peak"-Tabelle im `README.md`. Schnellzugriff auf die jeweils aktuellen: `screenshots_latest/`. L1-Header-Card in `docs/screenshots/README.md`. Keine Geheimnisse in den Bildern, nur UI-Rendering':
        '- [docs/screenshots/](./screenshots/README.md) — 📗 ~1.1MB · kanonische Ablage aller Sichtpruefungs-Bilder, pro Phase praefixiert (`sp2_*`, `c4c5_*`, `p86_block_*`, `p86_probe_*`, `p86_smoke_*` = die 17 Gate-Belege von `v3.0.2`, `p9_step_*`, `p9_btn*`, `p9_doing_*`, `p9_trace_0*`, `p9a_legacy_*`) · die `c4c5_*`-Bilder besetzen die „Sneak Peak"-Tabelle im `README.md` · Schnellzugriff auf die jeweils aktuellen: `screenshots_latest/` · L1-Header-Card in `docs/screenshots/README.md` · keine Geheimnisse in den Bildern, nur UI-Rendering',
    "- [docs/INDEX.md](./INDEX.md) — 🔗 **diese Karte** (L0) · **38.288 B — unter dem 40-KiB-Softcap** (V145 ✅ seit 2026-10-03; **Nikinger-Entscheidung 2026-10-03: die datierten Nachträge wandern nach `docs/INDEX_ENTRIES_ARCHIVE.md`, das Kriterium von 38.912 B (P8.6 Plan 2 §1.2) auf den 40-KiB-Softcap neu baseliniert** — die 38.912 B waren für eine Datei mit weniger Zeilen gesetzt und waren **per Kürzen unerreichbar**: gemessen waren 71.573 B, davon **37.391 B Nachträge in 43 von 93 Einträgen**, und selbst 300 B je Zeile hätten 39.971 B ergeben. Verschoben per `scripts/archive_index_entries.sh` mit fünf Gegenproben, darunter die byteweise Reassemblierung des Originals; **4 Gegenproben des Skripts rot** (Schnitt mitten im Satz · `**` am falschen Ort · im INDEX vergessener Nachtrag · der Zeiger als Markdown-Link, den `doc_health` für die INDEX-Zeile des Archivs hielt) · **Wächter**: `phase9_hardening/tests/test_index_archive.py` — harter Größen-Gate, kein Nachtrag im INDEX, Archiv vollständig) · **Nachtrag: `docs/INDEX_ENTRIES_ARCHIVE.md`**":
        "- [docs/INDEX.md](./INDEX.md) — 🔗 **diese Karte** (L0) · **" + SIZE_TOKEN + " — unter dem 40-KiB-Softcap** (V145 ✅) · die Karten-Chronik steht in `docs/INDEX_ENTRIES_ARCHIVE.md` · **Nachtrag: `docs/INDEX_ENTRIES_ARCHIVE.md`**",
    "- [phase9_hardening/step_b/RUNBOOK_STEP_B.md](../phase9_hardening/step_b/RUNBOOK_STEP_B.md) — 📗 ~26KB · **der geführte Step-B-Ablauf B0–B3** (tailscaled-watchdog installieren und live beweisen) mit **drei gemessenen Befunden, die den Plan §4 korrigiert haben**: **der `sudoers`-Weg ist unbaubar** (die Unit setzt `NoNewPrivileges=true`, sudo lebt vom setuid-Bit — `setpriv --no-new-privs -- sudo -n -l` → *\"no new privileges\" flag is set*) · **die Box kennt nur die grobe polkit-Aktion** (`systemd 255.4`: `manage-units` für Start/Stop/Restart, man `org.freedesktop.systemd1(5)` §Security), ein `<defaults>`-Eintrag kann **nicht** nach Unit filtern · **die Units sind auf der VM noch nicht installiert** (`/etc/systemd/system/tailscaled-watchdog.*` fehlt, `list-timers` = 0). **V153 damit entschieden** (polkit) — ob systemd 255 das `unit`-Attribut mitschickt, war unprivilegiert nicht auslesbar (`pkcheck` → *not registered*) — **B0 hat es gemessen: `AUTORISIERT`**, Journal-Beleg bei `User=root` ⇒ die enge Regel trägt. Nebenbefund: eine Verweigerung kostet hier 25 s (kein polkit-Agent, headless). · **Nachtrag: `docs/INDEX_ENTRIES_ARCHIVE.md`**":
        "- [phase9_hardening/step_b/RUNBOOK_STEP_B.md](../phase9_hardening/step_b/RUNBOOK_STEP_B.md) — 📗 ~26KB · **der geführte Step-B-Ablauf B0–B3** (tailscaled-watchdog installieren und live beweisen) mit **drei gemessenen Befunden** (der `sudoers`-Weg ist unbaubar, die Box kennt nur die grobe polkit-Aktion, die Units fehlen auf der VM) — **V153 damit entschieden (polkit)**, B0 hat `AUTORISIERT` gemessen · **Nachtrag: `docs/INDEX_ENTRIES_ARCHIVE.md`**",
    "- [phase8_ui_graph/CLAUDE.md](../phase8_ui_graph/CLAUDE.md) — 📗 ~47KB — **6.901 B ÜBER dem 40-KiB-Softcap, benannt statt versteckt** (P8-P; **war schon auf HEAD\nüber der Grenze** (45.365 B), die alte Angabe `~43KB` lag nur noch im Toleranzfenster des Wächters;\ndie zwei B17-Korrekturen kosten +2.496 B, der Rest ist gewachsene Phase-8-Chronik — **die Lösung ist\ndie Rotation, kein Kürzen**) · Phase-8-Head, alle Bloecke ✅, Phase formal ✅, Abnahmestand **26 ✅ · 0 🟡 · 0 ⬜**. Traegt die **Selection/Choice-Konvention v3**, seit P8.6 Block A mit fuenfter Kategorie Vorsicht\n(`.action--caution`) — deshalb bei jedem UI-Commit zu lesen · **Nachtrag: `docs/INDEX_ENTRIES_ARCHIVE.md`**":
        "- [phase8_ui_graph/CLAUDE.md](../phase8_ui_graph/CLAUDE.md) — 📗 ~47KB — **6.901 B ÜBER dem 40-KiB-Softcap, benannt statt versteckt** (P8-P; die Lösung ist die Rotation, kein Kürzen) · Phase-8-Head, alle Bloecke ✅, Abnahmestand **26 ✅ · 0 🟡 · 0 ⬜**, trägt die **Selection/Choice-Konvention v3** (fünfte Kategorie Vorsicht) · **Nachtrag: `docs/INDEX_ENTRIES_ARCHIVE.md`**",
    "- [docs/INDEX_ENTRIES_ARCHIVE.md](./INDEX_ENTRIES_ARCHIVE.md) — 📦 **45.703 B** · L3-Archiv der **datierten Nachträge aus den Einträgen dieser Karte**, verbatim, ein Abschnitt je Karte in der Reihenfolge der Karte (nicht newest-first — wer einen Nachtrag sucht, sucht ihn über den Dateinamen, nicht über ein Datum). Angelegt am 2026-10-03, weil die Karte bei **71.573 B** stand und **37.391 B** davon Nachträge in 43 von 93 Einträgen waren — mehr als die Hälfte, und die seit Wochen als ungeklärt geführte Ursache der Überschreitung (P9-3/V145). **Die `updated:`-Kette der Karte ist nicht die Restmasse: 1.155 B, am 2026-10-03 rotiert** — wer die Datei rotieren wollte, hätte die falsche Stelle angefasst. Verschoben per `scripts/archive_index_entries.sh` (fünf Gegenproben, darunter die byteweise Reassemblierung des Originals und „kein datierter Nachtrag bleibt im INDEX\", die Verschieben von Weglassen unterscheidet); **vier Skript-Gegenproben waren rot, bevor es lief** — die Liste in `phase9_hardening/tests/test_index_archive.py`. **Regel für die nächste Session:** eine Kartenzeile bekommt wieder einen datierten Nachtrag, *wenn* er kurz ist — `test_no_entry_line_carries_a_dated_addendum_any_more` verbietet sie vollständig, und das ist Absicht: die Karte ist Stand, das Archiv ist Chronik":
        "- [docs/INDEX_ENTRIES_ARCHIVE.md](./INDEX_ENTRIES_ARCHIVE.md) — 📦 **46.456 B** · L3-Archiv der **datierten Nachträge aus den Einträgen dieser Karte**, verbatim, ein Abschnitt je Karte in der Reihenfolge der Karte (nicht newest-first — wer einen Nachtrag sucht, sucht ihn über den Dateinamen, nicht über ein Datum). Angelegt am 2026-10-03, weil die Karte bei **71.573 B** stand und **37.391 B** davon Nachträge in 43 von 93 Einträgen waren — mehr als die Hälfte, und die seit Wochen als ungeklärt geführte Ursache der Überschreitung (P9-3/V145). **Regel für die nächste Session:** eine Kartenzeile bekommt wieder einen datierten Nachtrag, *wenn* er kurz ist — `test_no_entry_line_carries_a_dated_addendum_any_more` verbietet sie vollständig, und das ist Absicht: die Karte ist Stand, das Archiv ist Chronik",
}


def die(msg: str, code: int = 1) -> None:
    print(f"ABBRUCH: {msg}", file=sys.stderr)
    sys.exit(code)


def format_size(size: int) -> str:
    """Bytes in der Schreibweise dieses Repos: Punkt als Tausendertrenner, `B` angehängt."""
    return f"{size:,}".replace(",", ".") + " B"


def splice(text: str, pairs: list[tuple[str, str]]) -> str:
    """Ersetzt (alt → neu) an den exakten Positionen. Jedes `alt` muss genau einmal
    vorkommen; das ist Gegenprobe (a) und zugleich die Voraussetzung dafür, dass der
    Zeilentausch verlustfrei ist."""
    edits = []
    for old, new in pairs:
        count = text.count(old)
        if count != 1:
            die(f"die alte Zeile kommt {count}-mal vor (erwartet: genau einmal) — {old[:70]!r}")
        edits.append((text.index(old), len(old), new))
    edits.sort()
    out, cursor = [], 0
    for pos, length, new in edits:
        if pos < cursor:
            die("zwei Ersetzungen überschneiden sich — der Schnitt ist nicht verlustfrei")
        out.append(text[cursor:pos])
        out.append(new)
        cursor = pos + length
    out.append(text[cursor:])
    return "".join(out)


def build_new_index(original: str) -> tuple[str, str, list[tuple[str, str]]]:
    """Baut den gekürzten INDEX und bestimmt die selbstbezügliche Größenangabe iterativ."""
    pairs = list(HEADINGS.items()) + list(ENTRIES.items())
    candidate = "0" * 8
    for _ in range(8):
        trial_pairs = [(old, new.replace(SIZE_TOKEN, candidate)) for old, new in pairs]
        text = splice(original, trial_pairs)
        new_size = len(text.encode("utf-8"))
        wanted = format_size(new_size)
        if wanted == candidate:
            resolved = [(old, new.replace(SIZE_TOKEN, candidate)) for old, new in pairs]
            return text, candidate, resolved
        candidate = wanted
    die("die selbstbezügliche Größenangabe kommt nicht zur Ruhe (8 Iterationen) — "
        "die Kartenzeile muss eine andere Bytezahl nennen")


def archive_text(original_archive: str, moved_headings: list[str], moved_entries: list[str]) -> str:
    """Hängt die verschobenen Zeilen an die zwei Abschnitte des Archivs."""
    text = original_archive
    for heading, section, blocks in (
        (HEADINGS_SECTION, HEADINGS_SECTION, moved_headings),
        (ENTRIES_SECTION, ENTRIES_SECTION, moved_entries),
    ):
        if section not in text:
            die(f"das Archiv hat den Abschnitt {section!r} nicht — es wird nicht angelegt")
        if not blocks:
            continue
        # Die verschobenen Überschriften stehen in einem Codeblock: eine `##`-Zeile im
        # Fließtext würde einen neuen Abschnitt erzeugen und den Abschnittszähler des
        # Wächters `test_index_archive.py` verschieben.
        body = "".join(f"```\n{line}\n```\n\n" for line in blocks) if section == HEADINGS_SECTION \
            else "".join(f"{line}\n\n" for line in blocks)
        marker = (f"> **Aus der Karte verschoben (2026-10-22, P10.5 Block 0 Schritt 0.5 — DO-2), "
                   f"verbatim:**\n\n")
        anchor = text.index(section) + len(section)
        # Direkt hinter der Überschrift (und ihrer Leerzeile) einfügen.
        rest = text[anchor:]
        if rest.startswith("\n\n"):
            anchor += 2
        text = text[:anchor] + "\n" + marker + body + text[anchor:].lstrip("\n")
    return text


def atomic_write(path: Path, text: str) -> None:
    tmp = path.with_name(path.name + ".tmp")
    tmp.write_text(text, encoding="utf-8")
    with open(tmp, "rb") as fh:
        os.fsync(fh.fileno())
    os.replace(tmp, path)


def main(argv: list[str]) -> int:
    check_only = "--check" in argv
    args = [a for a in argv if a != "--check"]
    repo_root = Path(args[0]) if args else Path(__file__).resolve().parents[2]

    index_path = repo_root / INDEX_REL
    archive_path = repo_root / ARCHIVE_REL
    if not index_path.is_file():
        die(f"INDEX nicht gefunden: {index_path}")
    if not archive_path.is_file():
        die(f"Archiv fehlt: {archive_path} — L3-Archiv mit L1-Card anlegen, es wird nicht "
            f"angelegt", 3)

    original = index_path.read_text(encoding="utf-8")
    archive_original = archive_path.read_text(encoding="utf-8")

    new_index, size_figure, resolved = build_new_index(original)

    # Gegenprobe (b): Reassemblierung — die neuen Zeilen zurück durch die alten ersetzt
    # ergeben das Original, byteweise.
    rebuilt = splice(new_index, [(new, old) for old, new in resolved])
    if rebuilt != original:
        die("Reassemblierung weicht vom Original ab — der Schnitt ist nicht verlustfrei, "
            "nichts geschrieben")
    print(f"OK  (b) Reassemblierung byte-identisch ({len(original.encode())} B)")

    # Kein Kartenkopf darf einen datierten Nachtrag hereinholen.
    for old, new in resolved:
        if ADDENDA_RE.search(new):
            die(f"die neue Zeile trägt einen datierten Nachtrag: {new[:70]!r}")

    savings = len(original.encode("utf-8")) - len(new_index.encode("utf-8"))
    if savings < MIN_SAVINGS:
        die(f"die Ersparnis ist {savings} B und damit unter {MIN_SAVINGS} B — "
            f"nichts geschrieben")
    print(f"OK  (d) Ersparnis {savings} B (>= {MIN_SAVINGS} B)")

    new_archive = archive_text(
        archive_original,
        [old for old, _ in HEADINGS.items()],
        [old for old, _ in ENTRIES.items()],
    )

    # Gegenprobe (c): jede alte Zeile steht byte-identisch im Archiv.
    for old in list(HEADINGS) + list(ENTRIES):
        if old not in new_archive:
            die(f"eine verschobene Zeile steht nicht byte-identisch im Archiv: {old[:70]!r}")
    print(f"OK  (c) {len(HEADINGS) + len(ENTRIES)} verschobene Zeilen byte-identisch im Archiv")

    print(f"OK  INDEX:  {len(original.encode())} B -> {len(new_index.encode())} B "
          f"(Kartenzeile der Karte selbst nennt {size_figure})")
    print(f"OK  Archiv: {len(archive_original.encode())} B -> {len(new_archive.encode())} B")

    if check_only:
        print("    --check: nichts geschrieben.")
        return 0

    atomic_write(archive_path, new_archive)
    if archive_path.read_text(encoding="utf-8") != new_archive:
        die("das Archiv ist nach dem Schreiben nicht gleich dem Geprüften — INDEX NICHT angefasst")
    atomic_write(index_path, new_index)
    if index_path.read_text(encoding="utf-8") != new_index:
        die("der INDEX ist nach dem Schreiben nicht gleich dem Geprüften")
    print("OK  geschrieben: Archiv zuerst, dann der INDEX.")
    return 0


if __name__ == "__main__":
    sys.exit(main(sys.argv[1:]))
