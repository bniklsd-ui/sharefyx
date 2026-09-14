---
status: live
purpose: Verzeichnis der **aktuellen** Phase — Schnellzugriff für Nikinger, kein Grabbing in `docs/screenshots/<phase>_*`
read-when: Nikinger will die jüngsten Sichtprüfungs-Screenshots sehen, ohne durch die History zu scrollen
detail: L3 (Pointer-Verzeichnis, keine eigene Inhaltsquelle)
up: ../phase8_6_ui_polish/CLAUDE.md   # aktive Phase
down:
  - ../docs/screenshots/                # kanonische Ablage; diese Verzeichnis ist nur Symlink-Komfort
updated: 2026-09-14 (Phase 8.6 Block H-R Teil 2 — fünf Symlinks ersetzt (01/02 Übersichten, 03 Editor-offen bei 1440, 04 1024er Übersicht, 05 1024er Editor-offen); H-R-Teil-1-Konto-Dialog-Screenshot nicht mehr prominent — der ist über `docs/screenshots/p86_block_h_r_03_1440_konto_dialog.png` weiterhin erreichbar; H-R.3 Editor-YAML-Bündigkeit sichtbar in 03, H-R.4 1024er-Stapel in 04, H-R.5 1024er-Editor in 05.)
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

## Aktueller Inhalt (Phase 8.6 Block H-R Teil 1+2, Stand 2026-09-14)

| Dateiname | Original | Checkkriterium |
|---|---|---|
| `01_uebersicht.png` | `../docs/screenshots/p86_block_h_r_01_1440_uebersicht.png` | **Bei 1440 px: Rail + Liste + Detail uniform schwarz (`--bg-void = #000`); die Karte (`.overview__graph` mit `--surface`) schwebt sichtbar als erkennbar helleres Rechteck auf dem schwarzen Detail-Slot.** Beweis: H-R.1 erfüllt (N.13 Layer-Architektur-Revision), G-R-Nachtrag-Backlog "Layer-Tone-Drift" mit-gelöst. |
| `02_uebersicht_1200.png` | `../docs/screenshots/p86_block_h_r_02_1200_uebersicht.png` | **Bei 1200 px: gleiches Layout wie 1440 — Rail 240 px mit Labels, alle drei Slots schwarz, Karte schwebt, kein Kollaps.** Beweis: OLED-BLACK wirkt in allen Breakpoints (kein neuer Sonderfall). |
| `03_editor_offen.png` | `../docs/screenshots/p86_block_h_r_03_1440_editor_offen.png` | **Bei 1440 px: Editor offen — der Editor-Kopf (Titel „Konferenz 2026" + v1-gespeichert-Badge + Archivieren + Speichern + ×) endet auf gleicher Y-Position wie der Listen-Kopf (Alle Items + Suchfeld).** Die YAML-Kopfdaten-Zeile „Kopfdaten YAML-Frontmatter" beginnt auf gleicher Höhe wie das erste Item („Konferenz 2026") im Listen-Slot — der 27-px-Versatz vor H-R.3 ist weg. Beweis: V142-CDP-Probe pre-fix 27,14 px / post-fix 0,86 px (≤ 2 px Toleranz). |
| `04_1024_uebersicht.png` | `../docs/screenshots/p86_block_h_r_04_1024_uebersicht.png` | **Bei 1024 px: Liste oben (Spaces-Übersicht „alpha/beta/gamma" mit Counts) und Karte unten (Verknüpfungsgraph mit Tags/Ordner-Toggles) sauber gestapelt — Rail links 240 px vollständig sichtbar.** Beweis: V143-CDP-Probe misst 0 Rechteck-Schnittmenge zwischen .list/.detail__graph/.rail. |
| `05_1024_editor.png` | `../docs/screenshots/p86_block_h_r_05_1024_editor_offen.png` | **Bei 1024 px: Editor im unteren Slot — alle Knöpfe sichtbar: Archivieren, Speichern, × (im Editor-Kopf), Format-Toolbar (B I </> Link H Anführungszeichen Liste 1. — Bild Vorschau), Anhängen-Feld + Button (am Fuß).** Beweis: V144-CDP-Probe misst 16/16 Knöpfe `reachable: true`, keiner offscreen. |

Hinweis: dies sind die H-R-Teil-1+2-Screenshots (alle fünf Sub-Blöcke gebaut). Der H-R-Teil-1-Konto-Dialog-Screenshot (`p86_block_h_r_03_1440_konto_dialog.png`) bleibt über `docs/screenshots/` für die Historie erreichbar, ist aber nicht mehr in `screenshots_latest/` prominent — der Editor-Bündigkeits-Screenshot ist hier wichtiger. Block G-R-Screenshots (`p86_block_g_r_{01..06}_*.png`) und Block-H-Screenshots (`p86_block_h_{01..03}_*.png`) bleiben in `docs/screenshots/` für die Historie unverändert.

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
