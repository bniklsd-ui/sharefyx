---
status: live
purpose: Verzeichnis der **aktuellen** Phase — Schnellzugriff für Nikinger, kein Grabbing in `docs/screenshots/<phase>_*`
read-when: Nikinger will die jüngsten Sichtprüfungs-Screenshots sehen, ohne durch die History zu scrollen
detail: L3 (Pointer-Verzeichnis, keine eigene Inhaltsquelle)
up: ../phase8_6_ui_polish/CLAUDE.md   # aktive Phase
down:
  - ../docs/screenshots/                # kanonische Ablage; diese Verzeichnis ist nur Symlink-Komfort
updated: 2026-09-17 (Phase 8.6 Block H-R-3 — vier Symlinks ersetzt: 01 1440-Editor-offen [Listen-Slot weg, H-R.8], 02 1200-Kontrolle [gleiches Verhalten wie 1440, H-R.7 leckt nicht], 03 1024-ohne-Karte [H-R.6, Umkehr von G-R.1], 04 1024-Editor-fullview [H-R.7, Rail+Liste weg]. H-R-Teil-2-Screenshots (Editor-YAML-Bündigkeit, 1024er-Stapel) bleiben über `docs/screenshots/p86_block_h_r_{01..05}_*.png` erreichbar, nicht mehr prominent — der 1024er-Stapel aus H-R-Teil-2 ist durch H-R.6 ersetzt.)
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

## Aktueller Inhalt (Phase 8.6 Block H-R-3, Stand 2026-09-17)

| Dateiname | Original | Checkkriterium |
|---|---|---|
| `01_1440_editor_offen.png` | `../docs/screenshots/p86_block_h_r_3_01_1440_editor_open.png` | **Bei 1440 px mit offenem Item: der Listen-Slot ist komplett weg — Rail (240 px) direkt gefolgt vom Editor, der den restlichen Platz füllt.** Beweis: Lock H-R.8 (Lesart b), Probe `dataset_view=detail, list_display=none, rail_display=flex`. |
| `02_1200_editor_offen.png` | `../docs/screenshots/p86_block_h_r_3_04_1200_editor_open.png` | **Bei 1200 px mit offenem Item: identisches Verhalten wie bei 1440 — Rail bleibt sichtbar, nur die Liste ist weg.** Beweis: H-R.7 (Editor-Fullview) greift NICHT bei 1200 px, nur bei ≤1024 px — Kontroll-Screenshot. |
| `03_1024_ohne_karte.png` | `../docs/screenshots/p86_block_h_r_3_02_1024_list_only.png` | **Bei 1024 px in der Übersicht: keine Karte/Graph mehr sichtbar — nur Rail + Liste in einer Zeile.** Beweis: Lock H-R.6 (Umkehr von G-R.1), Probe `detail_graph_display=none`. |
| `04_1024_editor_fullview.png` | `../docs/screenshots/p86_block_h_r_3_03_1024_editor_fullview.png` | **Bei 1024 px mit offenem Item: Rail UND Liste komplett weg, der Editor füllt den vollen Viewport (1024×768).** Beweis: Lock H-R.7, Probe `rail_display=none, list_display=none, grid-template-columns=1024px`. |

Hinweis: dies sind die H-R-3-Screenshots (drei Locks H-R.6/H-R.7/H-R.8, ein Commit). Die H-R-Teil-1+2-Screenshots (`p86_block_h_r_{01..05}_*.png`, Editor-YAML-Bündigkeit + der jetzt ersetzte 1024er-Stapel) bleiben über `docs/screenshots/` für die Historie erreichbar, sind aber nicht mehr prominent — der 1024er-Stapel aus Teil 2 existiert nach H-R.6 nicht mehr. Block G-R-Screenshots (`p86_block_g_r_{01..06}_*.png`) und Block-H-Screenshots (`p86_block_h_{01..03}_*.png`) bleiben in `docs/screenshots/` für die Historie unverändert.

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
