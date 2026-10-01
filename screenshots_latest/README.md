---
status: live
purpose: Verzeichnis der **aktuellen** Phase — Schnellzugriff für Nikinger, kein Grabbing in `docs/screenshots/<phase>_*`
read-when: Nikinger will die jüngsten Sichtprüfungs-Screenshots sehen, ohne durch die History zu scrollen
detail: L3 (Pointer-Verzeichnis, keine eigene Inhaltsquelle)
up: ../phase9_hardening/CLAUDE.md   # aktive Phase
down:
  - ../docs/screenshots/                # kanonische Ablage; diese Verzeichnis ist nur Symlink-Komfort
updated: 2026-10-01 (Rotation auf die `.toolbar-btn`-Belege (`p9_btn2_*`): drei Symlinks neu, die drei `p9_step_e_*`-Links raus — Step E ist als Beleg in `docs/screenshots/` erledigt und die aktuell offene Sichtfrage ist die Knopfoptik vor dem Deploy. **Vier unversionierte Tailscale-Kopien** mit Leerzeichen im Namen wandern nach `docs/screenshots/p9_step_a_01..04_*` (Infra-Beleg zu A3, ausdrücklich keine Sichtprüfung), die fünfte Datei `Machines - Tailscale.html` ist gelöscht: leere SPA-Hülle, `tailscale-api-prefetch` = `{}`, kein Bildwert) | updated: 2026-09-28 (Phase **9** — Rotation auf die ersten P9-Bilder: die sieben P8.6-Gate-Symlinks sind weg, drei `p9_step_e_*`-Links rein (P8.6-AK sagt genau das: "sie bleiben stehen, bis P9 eigene Screenshots produziert" — Step E hat als erster P9-Step welche produziert) | 2026-09-19 (Phase 8.6 abgeschlossen — Rotation auf die **Gate-Belege**: sieben Symlinks auf `p86_smoke_*` ersetzen die fünf H-R-3-Links. Das sind die Bilder, auf denen die Freigabe von `v3.0.2` beruht. Bleiben stehen, bis P9 eigene Screenshots produziert.)
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

## Aktueller Inhalt (Phase **9**, `.toolbar-btn` in Standardoptik, Stand 2026-10-01)

Drei Bilder aus `phase9_hardening/scripts/p9_btn2_toolbar_probe.py` gegen die **eigene**
TLS-Wegwerf-Instanz (`p9_step_g_wegwerf.py`, Port 18775, Chromium 1440x900). Sie zeigen den Stand,
der die offene Frage aus dem Session-Ende 2026-10-01 beantworten soll: tragen die zehn
Formatierhilfen + „Vorschau" jetzt **dieselbe Optik** wie der aktive Übersichtsknopf.

**Der Beleg ist die Messung, nicht das Bild.** Das Skript vergleicht echte Screenshot-Pixel
(`probes/p9_btn2_toolbar_probe.json`, 13/13 grün, Gegenprobe mit eingebautem Verstoß → 5 rot):
gerechnete Fläche stringgleich mit `.btn`, Verlauf in drei Höhen Δ ≤ 2, Randpixel Δ = 0. Das Bild
beantwortet die eine Frage, die eine Messung nicht kann: **gefällt es.**

| Dateiname | Original | Checkkriterium |
|---|---|---|
| `01_formatierleiste.png` | `../docs/screenshots/p9_btn2_01_formatierleiste.png` | **Die Leiste im Zuschnitt (379x25):** elf Knöpfe, dunkelblau mit heller Kante, in der Mitte der breitere „Vorschau". Auf dem alten Stand trugen sie die graue Plastik und stochen sichtbar gegen die Panel-Fläche. |
| `02_editor_standardoptik.png` | `../docs/screenshots/p9_btn2_02_editor.png` | **Das ganze Fenster — der eine Blick, um den es ging:** Rail-Knopf „Übersicht" oben links (dieselbe Optik), Formatierleiste rechts, „Anhängen" unten rechts als `.btn` im selben Panel. Drei Knopfoptiken auf einem Bild: entscheidend ist, dass alle drei **gleich** aussehen. |
| `03_formatierleiste_deaktiviert.png` | `../docs/screenshots/p9_btn2_03_formatierleiste_deaktiviert.png` | **Zustand in der Vorschau (385x25):** alle Formatierhilfen flach und matter statt im Verlauf — so soll „inaktiv lesbar" aussehen. Absicht und nicht Versehen: `:disabled` trägt `--surface`, nicht `--btn-std-fill`. |

**Warum die Wegwerf-Instanz und nicht das echte Gerät:** die Probe braucht einen
reproduzierbaren Zustand **und** einen Pixelvergleich in einem Lauf; am echten Datenbestand wäre
beides nicht gegen eine Vorher-Version zu halten. Für den Gesamteindruck der Oberfläche bleibt die
Sichtprüfung am echten Gerät nötig — dafür ist ohnehin Step Z (Gate) zuständig.

**Nicht hier, mit Begründung.** Die vier Tailscale-Adminbilder aus A3 (2026-09-30) lagen als
unversionierte Kopien mit Leerzeichen im Dateinamen in diesem Verzeichnis. Sie sind jetzt unter
`docs/screenshots/p9_step_a_01..04_*` versioniert (Infra-Beleg zu `RUNBOOK_STEP_A.md` §A3, **keine
Sichtprüfung der Oberfläche**) und gehören deshalb nicht in die Schnellansicht. Die fünfte Datei,
`Machines - Tailscale.html`, ist **gelöscht**: die gespeicherte Seite war nur die leere SPA-Hülle
(`<div id="root">` leer, `tailscale-api-prefetch` = `{}`, 2,7 KB) — ohne Bildwert, und eine
Admin-Seite im Repo ist kein Beweis, den ein Bild liefert.

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
