---
status: live
purpose: Verzeichnis der **aktuellen** Phase — Schnellzugriff für Nikinger, kein Grabbing in `docs/screenshots/<phase>_*`
read-when: Nikinger will die jüngsten Sichtprüfungs-Screenshots sehen, ohne durch die History zu scrollen
detail: L3 (Pointer-Verzeichnis, keine eigene Inhaltsquelle)
up: ../phase8_6_ui_polish/CLAUDE.md   # aktive Phase
down:
  - ../docs/screenshots/                # kanonische Ablage; diese Verzeichnis ist nur Symlink-Komfort
updated: 2026-09-14 (Phase 8.6 Block G — Block-B-Symlinks wurden ersetzt; Konvention gilt weiterhin, P8.6-AK)
---
# `screenshots_latest/` — Schnellzugriff auf die Screenshots der aktuellen Phase

**Was hier liegt:** die Screenshots, die **in der aktuell laufenden Phase** für die
Sichtprüfung relevant sind — als **Symlinks** auf die Originale in
`../docs/screenshots/<phase>_*`. Single source of truth bleibt `docs/screenshots/`;
dieses Verzeichnis ist ein Lese-Komfort, kein Archiv.

**Wann aktualisieren:** zu Beginn jeder neuen Phase (oder am Ende der vorigen) —
die alten Symlinks raus, die neuen rein. opencode/M3 macht das im selben Commit wie
die Doku-Aktualisierung der Phase, kein eigener PR.

**Naming:** durchnummeriert mit kurzem Screenshot-Inhalt im Filename, **nicht** mit
Phase-Tag (der ändert sich beim Phasenwechsel, der Inhalt bleibt). Begründung:
der Nikinger soll die Datei auch ohne Phase-Kontext sofort verstehen.

## Sichtprüfungs-Konvention (Nikinger 2026-09-11, neu)

Wenn opencode/M3 Screenshots aufnimmt, sagt es **immer** zwei Dinge in den Chat:

1. **Dateiname** (was hier in `screenshots_latest/` liegt, nicht der Original-Pfad)
2. **Checkkriterium** (kurz — was der Nikinger auf dem Bild sehen soll, ein bis zwei Sätze)

Das gilt unabhängig davon, ob M3 selbst das Bild mit dem `read`-Tool beurteilen kann —
auch wenn M3's eigene Bewertung positiv ist, ist die **Nikinger-Verifikation** der
Pflicht-Beleg (P8.6-O-Eskalationsregel: ein Build, der nur durch Selbstprüfung eines
bildfähigen Modells abgesichert ist, ist noch nicht live-verifiziert; die
`Sichtpruefung`-Schwester-Datei regelt das vollständig).

Ausnahmen, in denen M3 den Dateinamen + Checkkriterium **nicht** nennt:
- Wenn der Screenshot ein reiner Build-Beleg ist (z. B. „Smoke gegen Wegwerf X
  bestanden, hier der Konsolen-Output als Bild") und M3 den Befund bereits im
  Klartext dokumentiert hat.
- Wenn die Verifikation programmatisch ist (Regex auf gerenderten HTML-Output
  o. ä.) und der Screenshot nur Anhang ist.

## Aktueller Inhalt (Phase 8.6 Block G, Stand 2026-09-14)

| Dateiname | Original | Checkkriterium |
|---|---|---|
| `01_uebersicht.png` | `../docs/screenshots/p86_block_g_01_1440_uebersicht.png` | **`.shell` ist 240/480/1fr, Spaces + Zuletzt benutzt im Listen-Slot (Mitte), Verknüpfungs-Graph hat den Detail-Slot allein (~720 px breit).** Beweis: Befund 5 weg, Befund 4 weg (Karte ist 50 % statt 21 %), Befund 7a weg (`renderOverview()` wird im Listen-Slot gerendert). |
| `02_space_geoeffnet.png` | `../docs/screenshots/p86_block_g_02_1440_space_geoeffnet.png` | **Nach Klick auf eine Space-Zeile in der Übersicht: die ganze Zeile (inkl. der drei Chip-Counter-Chips „5 Offen / 6 Notizen / 1 Archiv") ist klickbar, der Hover-Fill reicht über die ganze Zeile.** Beweis: Befund 6 weg, P8.6-P wiederhergestellt (G7). |
| `03_editor_offen.png` | `../docs/screenshots/p86_block_g_03_1440_editor_offen.png` | **Nach Klick auf ein Item: der Editor ersetzt die Karte im Detail-Slot — Kopfdaten + Text-Panel + Anhängen-Zeile sichtbar, Karte weg.** Beweis: G2/G5, ESC-Kette funktioniert (N.8). |
| `04_editor_nach_esc.png` | `../docs/screenshots/p86_block_g_04_1440_editor_nach_esc.png` | **Nach ESC: Editor weg, Verknüpfungs-Graph ist zurück.** Beweis: N.8 — „ESC bringt die Karte zurück". |

`05_1200_uebersicht.png` und `06_1024_uebersicht.png` sind in `docs/screenshots/p86_block_g_*.png` vorhanden, hier nicht gesymlinkt (Platzhalter-Konvention — vier Hauptscreenshots im Schnellzugriff, alle sechs im Original-Verzeichnis für die Sichtprüfung am Gerät).

## Rotation

Beim Phasen-Wechsel (z. B. Phase 8.6 → Phase 8.7/P9):

1. Neue Screenshots unter `docs/screenshots/<new_phase>_*` aufnehmen.
2. Alle alten Symlinks hier löschen.
3. Neue Symlinks hier anlegen, mit dem Nummerierungs-Schema der neuen Phase
   (z. B. `01_...`, `02_...`).
4. Diese README.md aktualisieren mit der neuen Tabelle + Checkkriterien.
5. Im selben Commit den `updated:`-Eintrag oben ergänzen.

opencode/M3 macht das **selbst** ohne Rückfrage — es ist Teil der
Phase-Closeout-Pflichten, kein Nikinger-Auftrag.
