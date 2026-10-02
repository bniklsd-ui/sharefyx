---
status: live
purpose: Verzeichnis der **aktuellen** Phase — Schnellzugriff für Nikinger, kein Grabbing in `docs/screenshots/<phase>_*`
read-when: Nikinger will die jüngsten Sichtprüfungs-Screenshots sehen, ohne durch die History zu scrollen
detail: L3 (Pointer-Verzeichnis, keine eigene Inhaltsquelle)
up: ../phase9_hardening/CLAUDE.md   # aktive Phase
down:
  - ../docs/screenshots/                # kanonische Ablage; diese Verzeichnis ist nur Symlink-Komfort
updated: 2026-10-02 (**die fünf Bilder und die Probe sind neu — der alte Beleg war der Gegenlauf.** Beim erneuten Lesen fiel auf: `p9_trace_probe.json` stand auf `alle_ok: false` (S5 rot) und Bild 05 zeigte `beta` statt `alpha`, weil der Hand-Gegenlauf des trace-Blocks Skript und Ausgabepfade geteilt hat. Eigener Lauf gegen die Zwei-Principalen-Wegwerf-Instanz → **8/8**, Bilder neu (Bild 02 ist zeichengleich), Wächter `test_committed_probe_evidence.py` verhindert die Wiederholung) | 2026-10-02 (Rotation auf die `p9_trace_*`-Belege: sechs Symlinks neu, die vier `p9_doing_*`-Links raus — der doing-Block ist mit dem Deploy `v3.1.0` erledigt und abgenommen) | 2026-10-02 (Rotation auf die `p9_doing_*`-Belege: vier Symlinks neu, die drei `p9_btn2_*`-Links raus — der Knopfoptik-Fall ist erledigt und abgenommen) | 2026-10-01 (Rotation auf die `.toolbar-btn`-Belege (`p9_btn2_*`): drei Symlinks neu, die drei `p9_step_e_*`-Links raus — Step E ist als Beleg in `docs/screenshots/` erledigt und die aktuell offene Sichtfrage ist die Knopfoptik vor dem Deploy. **Vier unversionierte Tailscale-Kopien** mit Leerzeichen im Namen wandern nach `docs/screenshots/p9_step_a_01..04_*` (Infra-Beleg zu A3, ausdrücklich keine Sichtprüfung), die fünfte Datei `Machines - Tailscale.html` ist gelöscht: leere SPA-Hülle, `tailscale-api-prefetch` = `{}`, kein Bildwert) | updated: 2026-09-28 (Phase **9** — Rotation auf die ersten P9-Bilder: die sieben P8.6-Gate-Symlinks sind weg, drei `p9_step_e_*`-Links rein (P8.6-AK sagt genau das: "sie bleiben stehen, bis P9 eigene Screenshots produziert" — Step E hat als erster P9-Step welche produziert) | 2026-09-19 (Phase 8.6 abgeschlossen — Rotation auf die **Gate-Belege**: sieben Symlinks auf `p86_smoke_*` ersetzen die fünf H-R-3-Links. Das sind die Bilder, auf denen die Freigabe von `v3.0.2` beruht. Bleiben stehen, bis P9 eigene Screenshots produziert.)
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

## Aktueller Inhalt (Phase **9**, Block trace, Stand 2026-10-02)

Sechs Bilder aus `phase9_hardening/scripts/p9_trace_self_check.py` gegen die **eigene**
TLS-Wegwerf-Instanz (`p9_trace_wegwerf.py`, Port 18777, Chromium 1440x900). Sie zeigen den
Block, der die Frage „wer arbeitet dran, wer hat zuletzt geändert" beantwortet: `assignee`
wird sichtbar und vom **Client** gefüllt, `updated_by` steht als Lesezeile im Kopfdaten-Panel.

**Die Instanz hat zwei Konten (`alpha`, `beta`) und echte Git-Historie** — beides ist der
Beleg, nicht Beiwerk. Mit einem eingeloggten Menschen trügen `updated_by` und `assignee`
denselben Wert und jede Verwechslung bliebe unsichtbar; ohne Git gäbe es nichts, was S6
prüfen könnte.

**Der Beleg ist die Messung, nicht das Bild — und die Messung muss passen zum Code, der laeuft.** **[2026-10-02]** Genau hier ist es fast schiefgegangen: die eingecheckte Probe war der Gegenlauf selbst (rote Station, Bild 05 mit `beta`), der Code war korrekt. Ein Wächter (`phase9_hardening/tests/test_committed_probe_evidence.py`) verlangt jetzt von jeder committeten Probe: keine rote Station, und die Zusammenfassung darf den Stationen nicht widersprechen; ein Gegenlauf muss `*_gegenprobe.json` heißen. **Die beiden übrigen Proben im selben Verzeichnis waren grün — der Fehler fiel also nur auf, wenn man genau die eine Datei öffnet, um die es geht.**

**Der Beleg ist die Messung, nicht das Bild.** Das Skript prüft 8 Stationen aus dem echten DOM
(`probes/p9_trace_probe.json`, 8/8 grün). Die **Gegenprobe** ist der eigentliche Beleg: ohne
die Leer-Prüfung im P9-Z-Zweig meldet **S5** rot — und zwar genau die Aussage, die der Zweig
tragen soll: B zieht eine **A zugewiesene** Aufgabe auf „In Arbeit" und der Assignee springt
von `alpha` auf `beta`. Ein Zufuehlen, das kein Messwert bemerkt.

| Dateiname | Original | Checkkriterium |
|---|---|---|
| `01_bei_wird_gefuellt.png` | `../docs/screenshots/p9_trace_01_auftrag_vor_speichern.png` | **Die P9-Z-Regel, im Moment des Auslösens:** der Status steht auf `doing`, und das Feld **„Bei“** daneben trägt `alpha` — **noch bevor** gespeichert wurde (Versionsband sagt „ungespeichert"). Unter den Feldern die Lesezeile „Zuletzt geändert von alpha · Datum". |
| `02_liste_bei_alpha.png` | `../docs/screenshots/p9_trace_02_gespeichert_liste.png` | **Die Listenzeile:** die Metazeile führt „bei alpha“ direkt nach dem Status, vor der Fälligkeit. Wer den Ordner „In Arbeit“ öffnet, sieht ohne Klick, wer dran ist. |
| `03_ansicht_von_b.png` | `../docs/screenshots/p9_trace_03_ansicht_von_b.png` | **Ansicht von B** auf dieselbe Aufgabe: Metazeile „bei alpha“, Kopfdaten-Feld „Bei“ = `alpha`, Lesezeile „Zuletzt geändert von **alpha**“. B sieht A als letzten Schreiber — obwohl B selbst noch nichts angefasst hat. |
| `04_zuletzt_geaendert_von_b.png` | `../docs/screenshots/p9_trace_04_nach_b.png` | **Nach Bs eigenem Schreibvorgang:** die Lesezeile wechselt auf „Zuletzt geändert von **beta**“, das Feld „Bei“ bleibt **alpha**. Genau diese beiden Zeilen sind die Aussage des ganzen Blocks. |
| `05_p9z_fremd.png` | `../docs/screenshots/p9_trace_05_p9z_fremd.png` | **Der harte P9-Z-Fall:** B zieht eine Aufgabe, die **A** zugewiesen ist, auf „In Arbeit" — das Feld behält `alpha`. Ein Zufuehlen, das nur bei leerem Feld arbeitet. **Genau dieses Bild war das erste, was den Gegenlauf-Beleg verriet:** in der Version vom 2026-10-02, 10:34 stand hier `beta`, weil der Gegenlauf dieselben Pfade überschrieben hatte. Die Datei ist seither neu aufgenommen (8/8). |
| `06_legacy_ohne_feld.png` | `../docs/screenshots/p9_trace_06_legacy_ohne_feld.png` | **Der Altbestand:** dasselbe Item **ohne** `updated_by` (von Hand so erzeugt). Die Lesezeile ist **weg** — keine leere Zeile, kein „unbekannt“, kein Platzhalter; das Feld „Bei“ zeigt seinen Platzhalter. |

**Warum die Wegwerf-Instanz und nicht das echte Gerät:** der Beleg braucht einen
reproduzierbaren Vorher-Zustand (S1/S4/S5 **verbrauchen** ihn) **und** einen zweiten
Principal, und der Legacy-Item lässt sich nur auf einem frischen Seed ohne Feld anlegen. Am
echten Datenbestand wäre nichts davon zu halten. Für den Gesamteindruck bleibt die
Sichtprüfung am echten Gerät nötig — dafür ist der Augenschein am Deploy-Tag zuständig.

**Nicht hier, mit Begründung.** Die vier `p9_doing_*`-Belege (fünfter Eimer „In Arbeit") sind
mit dem Deploy `v3.1.0` abgenommen, die Tailscale-Bilder aus A3 sind Infra-Beleg ohne
Bildwert, und die `p9_btn2_*`-Belege sind mit der Standardoptik der Knöpfe erledigt. Alle
sechs liegen versioniert in `docs/screenshots/`.

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
