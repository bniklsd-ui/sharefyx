---
status: live
purpose: Verzeichnis der **aktuellen** Phase — Schnellzugriff für Nikinger, kein Grabbing in `docs/screenshots/<phase>_*`
read-when: Nikinger will die jüngsten Sichtprüfungs-Screenshots sehen, ohne durch die History zu scrollen
detail: L3 (Pointer-Verzeichnis, keine eigene Inhaltsquelle)
up: ../phase9_hardening/CLAUDE.md   # aktive Phase
down:
  - ../docs/screenshots/                # kanonische Ablage; diese Verzeichnis ist nur Symlink-Komfort
updated: 2026-09-28 (Phase **9** — Rotation auf die ersten P9-Bilder: die sieben P8.6-Gate-Symlinks sind weg, drei `p9_step_e_*`-Links rein (P8.6-AK sagt genau das: "sie bleiben stehen, bis P9 eigene Screenshots produziert" — Step E hat als erster P9-Step welche produziert) | 2026-09-19 (Phase 8.6 abgeschlossen — Rotation auf die **Gate-Belege**: sieben Symlinks auf `p86_smoke_*` ersetzen die fünf H-R-3-Links. Das sind die Bilder, auf denen die Freigabe von `v3.0.2` beruht. Bleiben stehen, bis P9 eigene Screenshots produziert.)
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

## Aktueller Inhalt (Phase **9**, Step E, Stand 2026-09-28)

Drei Bilder aus `p9e_reload_probe.py` gegen die Wegwerf-Instanz (Port 18768, 14 Items, Chromium
1440x900). Sie sind die **Belegbilder** der Abnahmezeilen P9-33/-34/-35 — die Zahlen (0 Abrufe,
1 statt 10 Bilder) stehen im Phase-9-Head, die Bilder zeigen den Zustand, in dem sie gemessen
wurden. **Zur Sichtprüfung durch den Nikinger geeignet, aber nicht deren Ersatz:** die
programmatische Messung ist der Beleg, ein Bild kann den Abruf-Zähler nicht zeigen.

| Dateiname | Original | Checkkriterium |
|---|---|---|
| `01_uebersicht_vor_wiedereintritt.png` | `../docs/screenshots/p9_step_e_01_uebersicht_vor_wiedereintritt.png` | **Ausgangslage vor dem Wiedereintritt:** Karte rechts im eigenen Slot, Rail links, Spaces + Zuletzt benutzt in der Mitte. Das ist der Zustand, mit dem Bild 02 verglichen wird — die Canvas-Fingerabdrücke beider Bilder sind **byte-gleich im Canvas-Teil** (`25481930`, 2.160 gezeichnete Pixel, 654x530 — aus dem finalen Lauf 2026-09-28). |
| `02_uebersicht_nach_wiedereintritt.png` | `../docs/screenshots/p9_step_e_02_uebersicht_nach_wiedereintritt.png` | **Nach Item-auf + ESC + Klick auf "Übersicht": exakt dasselbe Kartenbild.** Karte springt nicht, es gab **null** `/api/v1/graph`-Abrufe. Auf dem alten Stand wären es 1 Abruf und ~2,5 s sichtbare Bewegung gewesen. |
| `03_uebersicht_nach_fremder_aenderung.png` | `../docs/screenshots/p9_step_e_03_uebersicht_nach_fremder_aenderung.png` | **Nach einer Änderung von außen (CLI, nicht über die UI):** "P9 E von aussen" steht in "Zuletzt benutzt", die Karte hat einen Knoten mehr (14 → 15, programmatisch gezählt). Damit ist P9-35 belegt: eine echte Änderung wird beim nächsten Eintritt aufgenommen. |

**Warum die Wegwerf-Instanz und nicht das echte Gerät:** die Probe braucht einen
 reproduzierbaren Vorher/Nachher-Zustand und einen Abruf-Zähler, beides am echten Datenbestand
nicht. Für die *gefühlte* Karte (Lesebarkeit bei 200 Knoten, Bewegung bei Zoom/Pan) bleibt die
Sichtprüfung am echten Gerät nötig — dafür ist ohnehin Step Z (Gate) zuständig.

Ältere Bilder der Phase 8.6 (`p86_smoke_*`, `p86_block_*`, `p86_probe_*`) bleiben in
`docs/screenshots/` für die Historie erreichbar, sind aber nicht mehr prominent.


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
