---
status: live
purpose: Verzeichnis der **aktuellen** Phase — Schnellzugriff für Nikinger, kein Grabbing in `docs/screenshots/<phase>_*`
read-when: Nikinger will die jüngsten Sichtprüfungs-Screenshots sehen, ohne durch die History zu scrollen
detail: L3 (Pointer-Verzeichnis, keine eigene Inhaltsquelle)
up: ../phase8_6_ui_polish/CLAUDE.md   # aktive Phase
down:
  - ../docs/screenshots/                # kanonische Ablage; diese Verzeichnis ist nur Symlink-Komfort
updated: 2026-09-14 (Phase 8.6 Block H-R Teil 1 — Block-H-Symlinks wurden ersetzt; Konvention gilt weiterhin, P8.6-AK. Block-H-R-Teil-1 hat nur die zwei Sichtungs-Befunde OLED-BLACK + account-nav-Akzent gebaut; H-R.3/.4/.5 (CDP-Probe-Welle) und Block J folgen noch.)
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

## Aktueller Inhalt (Phase 8.6 Block H-R Teil 1, Stand 2026-09-14)

| Dateiname | Original | Checkkriterium |
|---|---|---|
| `01_uebersicht.png` | `../docs/screenshots/p86_block_h_r_01_1440_uebersicht.png` | **Bei 1440 px: Rail + Liste + Detail uniform schwarz (`--bg-void = #000`); die Karte (`.overview__graph` mit `--surface`) schwebt sichtbar als erkennbar helleres Rechteck auf dem schwarzen Detail-Slot.** Beweis: H-R.1 erfüllt (N.13 Layer-Architektur-Revision), G-R-Nachtrag-Backlog "Layer-Tone-Drift" mit-gelöst. |
| `02_uebersicht_1200.png` | `../docs/screenshots/p86_block_h_r_02_1200_uebersicht.png` | **Bei 1200 px: gleiches Layout wie 1440 — Rail 240 px mit Labels, alle drei Slots schwarz, Karte schwebt, kein Kollaps.** Beweis: OLED-BLACK wirkt in allen Breakpoints (kein neuer Sonderfall). |
| `03_konto_dialog.png` | `../docs/screenshots/p86_block_h_r_03_1440_konto_dialog.png` | **Konto-Dialog offen bei 1440 px: „Update-Log ansehen" und „Spaces verwalten" tragen jetzt einen deutlich blauen Akzent-Fill (`var(--accent-quiet)`) + ringsum Border (`var(--accent-edge)`) + 3-px-Akzentkante links (`var(--accent)`) + Akzent-Chevron rechts — sofort als wichtig erkennbar.** Beweis: H-R.2 erfüllt (N.14 "ausnahmsweise" für Konto-Dialog, "sieht man kaum"-Befund weg). Einstellungen + Abmelden unten sind neutral (N.14-Spezialfall greift nur für `.account-nav`). |

Hinweis: dies sind die H-R-Teil-1-Screenshots (zwei Sichtungs-Befunde gebaut). H-R.3/.4/.5 (Editor-YAML-Bündigkeit, 1024-er Map-Overlap, 1024-er Editor-Modus) sind als Folgeblock offen — deren Screenshots kommen mit der CDP-Probe-Welle. Block G-R-Screenshots (`p86_block_g_r_{01..06}_*.png`) und Block-H-Screenshots (`p86_block_h_{01..03}_*.png`) bleiben in `docs/screenshots/` für die Historie unverändert.

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
