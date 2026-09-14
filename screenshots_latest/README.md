---
status: live
purpose: Verzeichnis der **aktuellen** Phase — Schnellzugriff für Nikinger, kein Grabbing in `docs/screenshots/<phase>_*`
read-when: Nikinger will die jüngsten Sichtprüfungs-Screenshots sehen, ohne durch die History zu scrollen
detail: L3 (Pointer-Verzeichnis, keine eigene Inhaltsquelle)
up: ../phase8_6_ui_polish/CLAUDE.md   # aktive Phase
down:
  - ../docs/screenshots/                # kanonische Ablage; diese Verzeichnis ist nur Symlink-Komfort
updated: 2026-09-14 (Phase 8.6 Block H — Block-G-Symlinks wurden ersetzt; Konvention gilt weiterhin, P8.6-AK)
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

## Aktueller Inhalt (Phase 8.6 Block H, Stand 2026-09-14)

| Dateiname | Original | Checkkriterium |
|---|---|---|
| `01_rail.png` | `../docs/screenshots/p86_block_h_01_1440_rail.png` | **Bei 1440 px: Rail zeigt unten in `.rail__account` zwei gestapelte Knöpfe — oben „Einstellungen" (Zahnrad, blau), unten „Abmelden" (Logout-Icon, `--caution` rot) als äußerster Knopf im Rail.** Beweis: Befund 7b weg (Umkehr von C1/N3-Lesart b, N.9), P8.6-AE erfüllt. |
| `02_rail_1200.png` | `../docs/screenshots/p86_block_h_02_1200_rail.png` | **Bei 1200 px: gleiches Layout wie 1440 — Rail 240 px voll sichtbar mit Labels, `.rail__account` mit beiden Knöpfen unten, kein Kollaps.** Beweis: Block H wirkt auch im schmalen Viewport (kein neuer Sonderfall, die Spalten-Anordnung ist der Normalfall in allen Breakpoints nach G-R). |
| `03_konto_dialog.png` | `../docs/screenshots/p86_block_h_03_1440_konto_dialog.png` | **Konto-Dialog offen bei 1440 px: „Update-Log ansehen" und „Spaces verwalten" tragen eine linke Akzentkante (`2px solid var(--line-strong)`) und ein Chevron-Icon rechts (`#i-chevron-right`, `margin-left: auto`) — sichtbar bedienbar, aber keine `.btn`-Plastik (B3-Kategorie „Navigation" bleibt erhalten).** Beweis: Befund 2 weg, V133 erfüllt (`elementFromPoint` erreichbar — die Knöpfe sind da, sie hatten nur keinen Afford). |

Drei weitere Screenshots (`01_1440_uebersicht`, `02_1440_editor_offen`, `03_1200_uebersicht`, `04_1200_editor_offen`, `05_1024_uebersicht`, `06_1024_editor_offen`) liegen in `docs/screenshots/p86_block_g_r_*.png` für die Sichtprüfung am Gerät — der Block-G-R-Layout-Umbau bleibt unverändert gültig (Block H hat das Layout nicht angefasst, nur den Rail-Inhalt und den Konto-Dialog).

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
