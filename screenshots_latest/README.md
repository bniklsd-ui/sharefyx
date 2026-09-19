---
status: live
purpose: Verzeichnis der **aktuellen** Phase — Schnellzugriff für Nikinger, kein Grabbing in `docs/screenshots/<phase>_*`
read-when: Nikinger will die jüngsten Sichtprüfungs-Screenshots sehen, ohne durch die History zu scrollen
detail: L3 (Pointer-Verzeichnis, keine eigene Inhaltsquelle)
up: ../phase8_6_ui_polish/CLAUDE.md   # aktive Phase
down:
  - ../docs/screenshots/                # kanonische Ablage; diese Verzeichnis ist nur Symlink-Komfort
updated: 2026-09-19 (Phase 8.6 abgeschlossen — Rotation auf die **Gate-Belege**: sieben Symlinks auf `p86_smoke_*` ersetzen die fünf H-R-3-Links. Das sind die Bilder, auf denen die Freigabe von `v3.0.2` beruht. Bleiben stehen, bis P9 eigene Screenshots produziert.)
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

## Aktueller Inhalt (Phase 8.6 **abgeschlossen**, Gate-Belege, Stand 2026-09-19)

Dies sind die Bilder aus dem **Gate-Lauf** (`p86_polish_smoke.py`, 18/18 Stationen, zwei
Browser) — also genau die Belege, auf denen die Freigabe von `v3.0.2` am 2026-09-18 beruht.
Sie bleiben hier stehen, bis P9 eigene Screenshots produziert.

| Dateiname | Original | Checkkriterium |
|---|---|---|
| `01_1440_uebersicht.png` | `../docs/screenshots/p86_smoke_01_1440_uebersicht.png` | **Bei 1440 px: die Übersicht (Spaces + Zuletzt benutzt) steht im linken Listen-Slot, die Karte hat den rechten Slot allein.** Das ist das Ergebnis des Layout-Umbaus aus Block G (P8.6-Y). |
| `02_esc_holt_die_karte_zurueck.png` | `../docs/screenshots/p86_smoke_05b_item_editor_esc.png` | **Nach ESC ist die Karte wieder da, wo eben noch der Editor war.** Der Rückweg ist Abnahmekriterium (N.8), nicht Nebenwirkung; Probe `view_after_esc=list`. |
| `03_kartenknoten_oeffnet_editor.png` | `../docs/screenshots/p86_smoke_06_karten_knoten_klick.png` | **Ein Klick auf einen Karten-Knoten öffnet den Editor** — einfacher Klick, kein Doppelklick. Der Doppelklick setzt nur Zoom/Pan zurück. |
| `04_rail_reihenfolge.png` | `../docs/screenshots/p86_smoke_02_rail_reihenfolge.png` | **Einstellungen und Abmelden stehen wieder beide unten, Abmelden als äußerster Knopf.** Die bewusste Umkehr von C1/N3-Lesart b (N.9); Probe `home < rail-tree < account-button < logout-button`. |
| `05_konto_dialog.png` | `../docs/screenshots/p86_smoke_09_konto_dialog.png` | **Beide Knöpfe im Konto-Dialog sehen bedienbar aus** (Akzentkante + Chevron) und sind per `elementFromPoint` erreichbar. Sie haben nie gefehlt — sie lasen sich nur wie Fließtext. |
| `06_1024_ohne_karte.png` | `../docs/screenshots/p86_smoke_11a_1024_ohne_map.png` | **Bei 1024 px in der Übersicht: keine Karte, nur Rail + Liste in einer Zeile.** Lock H-R.6, die Umkehr des 1024er-Stapels aus G-R.1. |
| `07_1024_editor_fullview.png` | `../docs/screenshots/p86_smoke_11b_1024_editor_fullview.png` | **Bei 1024 px mit offenem Item: Rail und Liste weg, der Editor füllt den Viewport.** Lock H-R.7. |

Ältere Bilder dieser Phase (`p86_block_*`, `p86_probe_*`) bleiben in `docs/screenshots/` für die
Historie erreichbar, sind aber nicht mehr prominent.


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
