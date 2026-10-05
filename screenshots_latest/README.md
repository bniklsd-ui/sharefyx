---
status: live
purpose: Verzeichnis der **aktuellen** Phase — Schnellzugriff für Nikinger, kein Grabbing in `docs/screenshots/<phase>_*`
read-when: Nikinger will die jüngsten Sichtprüfungs-Screenshots sehen, ohne durch die History zu scrollen
detail: L3 (Pointer-Verzeichnis, keine eigene Inhaltsquelle)
up: ../phase9_hardening/CLAUDE.md   # aktive Phase
down:
  - ../docs/screenshots/                # kanonische Ablage; diese Verzeichnis ist nur Symlink-Komfort
updated: 2026-10-05 (**Rotation auf die settings-Belege** — vier Symlinks neu, die vier B17-Links (`01_archivieren_*` … `04_editor_gesamt.png`) raus. Das ist die **offene Sichtfrage** des Blocks: die Messung ist 39/39, die Bilder sind angesehen, die Sichtprüfung des Nikingers steht aus. Bewusst **nicht** verlinkt: `p9_settings_06/07` (Passwortwechsel und Space-Anlegen sind Handgriffe ohne Aussagebild) und `03_updatelog_1440` (derselbe Inhalt wie im Fenster davor, nur an anderer Stelle) — ein Leseverzeichnis mit 7 Bildern wäre wieder ein Scrollen durch History) | updated: 2026-10-02 (**Rotation auf die B17-Belege** — vier Symlinks neu, die sechs `p9_trace_*`-Links raus; die sind abgenommen und liegen versioniert in `docs/screenshots/`. Der Block ersetzt den Vorsichtsknopf auf die Standardfläche, und **diese Bilder sind die offene Sichtfrage**: die Messung ist 14/14, die Sichtung steht aus) | updated: 2026-10-02 (**Abnahme durch den Nikinger mit Restbefund**: die sechs Bilder sind freigegeben; als Notiz hält er fest, dass noch nicht alle Knöpfe an das Schema angepasst sind — abgelegt als **B17** im Backlog von `phase9_hardening/CLAUDE.md` mit der gemessenen Klassenliste, *kein* Code-Touch) | 2026-10-02 (**die fünf Bilder und die Probe sind neu — der alte Beleg war der Gegenlauf.** Beim erneuten Lesen fiel auf: `p9_trace_probe.json` stand auf `alle_ok: false` (S5 rot) und Bild 05 zeigte `beta` statt `alpha`, weil der Hand-Gegenlauf des trace-Blocks Skript und Ausgabepfade geteilt hat. Eigener Lauf gegen die Zwei-Principalen-Wegwerf-Instanz → **8/8**, Bilder neu (Bild 02 ist zeichengleich), Wächter `test_committed_probe_evidence.py` verhindert die Wiederholung) | 2026-10-02 (Rotation auf die `p9_trace_*`-Belege: sechs Symlinks neu, die vier `p9_doing_*`-Links raus — der doing-Block ist mit dem Deploy `v3.1.0` erledigt und abgenommen) | 2026-10-02 (Rotation auf die `p9_doing_*`-Belege: vier Symlinks neu, die drei `p9_btn2_*`-Links raus — der Knopfoptik-Fall ist erledigt und abgenommen) | 2026-10-01 (Rotation auf die `.toolbar-btn`-Belege (`p9_btn2_*`): drei Symlinks neu, die drei `p9_step_e_*`-Links raus — Step E ist als Beleg in `docs/screenshots/` erledigt und die aktuell offene Sichtfrage ist die Knopfoptik vor dem Deploy. **Vier unversionierte Tailscale-Kopien** mit Leerzeichen im Namen wandern nach `docs/screenshots/p9_step_a_01..04_*` (Infra-Beleg zu A3, ausdrücklich keine Sichtprüfung), die fünfte Datei `Machines - Tailscale.html` ist gelöscht: leere SPA-Hülle, `tailscale-api-prefetch` = `{}`, kein Bildwert) | updated: 2026-09-28 (Phase **9** — Rotation auf die ersten P9-Bilder: die sieben P8.6-Gate-Symlinks sind weg, drei `p9_step_e_*`-Links rein (P8.6-AK sagt genau das: "sie bleiben stehen, bis P9 eigene Screenshots produziert" — Step E hat als erster P9-Step welche produziert) | 2026-09-19 (Phase 8.6 abgeschlossen — Rotation auf die **Gate-Belege**: sieben Symlinks auf `p86_smoke_*` ersetzen die fünf H-R-3-Links. Das sind die Bilder, auf denen die Freigabe von `v3.0.2` beruht. Bleiben stehen, bis P9 eigene Screenshots produziert.)
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

## Aktueller Inhalt (Phase **9**, Block B17, Stand 2026-10-02)

Vier Bilder aus `phase9_hardening/scripts/p9_btn3_caution_probe.py` gegen die eigene
TLS-Wegwerf-Instanz (`p9_step_g_wegwerf.py`, Port 18775, Chromium 1440x900). Sie zeigen **eine
einzige Änderung**: der Knopf „Archivieren" (`.btn.action--caution`, Kategorie „Vorsicht") trägt
jetzt **exakt** die Standardfläche, nur seine Beschriftung bleibt rot.

**Die Behauptung, um die es geht, ist eine Gleichheit, keine Schönheit.** Vorher trug der Knopf
die alte graue Familie `--btn-face-*` (`#2A313A`) — und die ist **heller** als die Standardfläche
`#0C1C31`. „Vorsicht" war damit der auffälligste Knopf der Editor-Fußzeile statt des Standards.
**Gemessen:** die berechneten `backgroundImage`-Strings sind jetzt stringgleich
(`linear-gradient(rgb(12,28,49), rgb(5,11,19))` auf beiden), vier Pixelproben an der glyphenfreien
Spalte x=4 px mit **max |Δ| = 1**, die Vorsichtfarbe sitzt in der Beschriftung (`rgb(229,72,77)`
gegen `rgb(233,237,242)` beim Standard). **Gegenprobe:** alte Fläche wieder eingebaut → 6 von 13
Stationen rot, Δ 25–28 an allen drei Höhen.

| Dateiname | Original | Checkkriterium |
|---|---|---|
| `01_archivieren_und_speichern.png` | `../docs/screenshots/p9_btn3_01_kopfleiste.png` | **Der eine Blick, um den es geht:** „Archivieren" und „Speichern" nebeneinander. Der Knopf darf **nicht heller** wirken als der Standard — er ist jetzt dieselbe dunkelblaue Fläche, unterschieden nur an der **roten Beschriftung**. „Speichern" bleibt bewusst die helle Akzentfläche (Hauptaktion). |
| `02_archivieren_ruhe.png` | `../docs/screenshots/p9_btn3_02_ruhe.png` | **Derselbe Knopf isoliert, 115×41, Ruhezustand** (die Aufnahme entsteht nach dem Wegziehen des Zeigers — ein Hover-Bild hätte den Beleg verfälscht). Fläche dunkelblau mit einer hellblauen 1-px-Kante, Schrift rot. Zum Vergleich: das war vorher ein heller grauer Block. |
| `03_archivieren_hover.png` | `../docs/screenshots/p9_btn3_04_hover.png` | **Der Hover-Zustand:** die Fläche wird **einen Tick heller** (der Standard-Hover `--btn-std-fill-hover`), die Beschriftung bleibt unverändert rot. Der Knopf darf auf Hover nicht aus der Reihe fallen. |
| `04_editor_gesamt.png` | `../docs/screenshots/p9_btn3_03_editor.png` | **Der ganze Editor** zur Einordnung: Knopfleiste, Kopfdaten, Formatierleiste, Anhängen-Streifen — alle Standardknöpfe tragen jetzt dieselbe Fläche, und „Archivieren" ist die einzige Abweichung in der Farbe, nicht in der Form. |

**Zwei Dinge, die der Sichtprüfung nicht zu Entscheidung gehören, die aber benannt sind.** Der
**Kontrast** der roten Beschriftung liegt bei 4,38:1 (vorher 3,36:1) — besser, aber unter dem
WCAG-AA-Wert 4,5:1 für normalgroßen Text; ob die Schrift heller wird, ist eine Design-Entscheidung.
Und eine **eigene rote Fläche** (`--caution-std-*`) wurde bewusst **nicht** gebaut: die
Selection/Choice-Konvention v3 schließt eine „gefüllte rote Fläche" aus.

**Nicht hier, mit Begründung.** Die sechs `p9_trace_*`-Belege sind am 2026-10-02 abgenommen
(der Restbefund daraus ist genau dieser Block), die vier `p9_doing_*` mit dem Deploy `v3.1.0`, die
`p9_btn2_*` mit der Standardoptik der Knöpfe. Alle liegen versioniert in `docs/screenshots/`.

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
