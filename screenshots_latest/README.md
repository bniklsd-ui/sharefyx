---
status: live
purpose: Verzeichnis der **aktuellen** Phase — Schnellzugriff für Nikinger, kein Grabbing in `docs/screenshots/<phase>_*`
read-when: Nikinger will die jüngsten Sichtprüfungs-Screenshots sehen, ohne durch die History zu scrollen
detail: L3 (Pointer-Verzeichnis, keine eigene Inhaltsquelle)
up: ../phase9_hardening/CLAUDE.md   # aktive Phase
down:
  - ../docs/screenshots/                # kanonische Ablage; diese Verzeichnis ist nur Symlink-Komfort
updated: 2026-10-05 (**Rotation auf die Nachtrags-Belege** — der dritte Symlink zeigt jetzt `p9_settings_08_rueckmeldung_1440.png` statt des Duplikats `04_drei_panels`; die **Tabelle ist mitgedreht** (die vier alten Zeilen standen noch auf B17, obwohl die Symlinks längst auf den settings-Block zeigten) · **die Kette ist repariert**: zwei Fäden trugen ein `updated: `-Präfix nach dem Trenner, damit war `rotate_index_updates.sh` für sie blind; `KNOWN_OFFENDERS` ist um diesen Eintrag gekürzt · **die Gegenlauf-Bilder des Blocks sind gelöscht**, rot eingecheckt sind nur die drei JSON-Gegenläufe) | 2026-10-05 (**Rotation auf die settings-Belege** — vier Symlinks neu, die vier B17-Links (`01_archivieren_*` … `04_editor_gesamt.png`) raus. Das ist die **offene Sichtfrage** des Blocks: die Messung ist 39/39, die Bilder sind angesehen, die Sichtprüfung des Nikingers steht aus. Bewusst **nicht** verlinkt: `p9_settings_06/07` (Passwortwechsel und Space-Anlegen sind Handgriffe ohne Aussagebild) und `03_updatelog_1440` (derselbe Inhalt wie im Fenster davor, nur an anderer Stelle) — ein Leseverzeichnis mit 7 Bildern wäre wieder ein Scrollen durch History) | 2026-10-02 (**Rotation auf die B17-Belege** — vier Symlinks neu, die sechs `p9_trace_*`-Links raus; die sind abgenommen und liegen versioniert in `docs/screenshots/`. Der Block ersetzt den Vorsichtsknopf auf die Standardfläche, und **diese Bilder sind die offene Sichtfrage**: die Messung ist 14/14, die Sichtung steht aus) | 2026-10-02 (**Abnahme durch den Nikinger mit Restbefund**: die sechs Bilder sind freigegeben; als Notiz hält er fest, dass noch nicht alle Knöpfe an das Schema angepasst sind — abgelegt als **B17** im Backlog von `phase9_hardening/CLAUDE.md` mit der gemessenen Klassenliste, *kein* Code-Touch) | 2026-10-02 (**die fünf Bilder und die Probe sind neu — der alte Beleg war der Gegenlauf.** Beim erneuten Lesen fiel auf: `p9_trace_probe.json` stand auf `alle_ok: false` (S5 rot) und Bild 05 zeigte `beta` statt `alpha`, weil der Hand-Gegenlauf des trace-Blocks Skript und Ausgabepfade geteilt hat. Eigener Lauf gegen die Zwei-Principalen-Wegwerf-Instanz → **8/8**, Bilder neu (Bild 02 ist zeichengleich), Wächter `test_committed_probe_evidence.py` verhindert die Wiederholung) | 2026-10-02 (Rotation auf die `p9_trace_*`-Belege: sechs Symlinks neu, die vier `p9_doing_*`-Links raus — der doing-Block ist mit dem Deploy `v3.1.0` erledigt und abgenommen) | 2026-10-02 (Rotation auf die `p9_doing_*`-Belege: vier Symlinks neu, die drei `p9_btn2_*`-Links raus — der Knopfoptik-Fall ist erledigt und abgenommen) | 2026-10-01 (Rotation auf die `.toolbar-btn`-Belege (`p9_btn2_*`): drei Symlinks neu, die drei `p9_step_e_*`-Links raus — Step E ist als Beleg in `docs/screenshots/` erledigt und die aktuell offene Sichtfrage ist die Knopfoptik vor dem Deploy. **Vier unversionierte Tailscale-Kopien** mit Leerzeichen im Namen wandern nach `docs/screenshots/p9_step_a_01..04_*` (Infra-Beleg zu A3, ausdrücklich keine Sichtprüfung), die fünfte Datei `Machines - Tailscale.html` ist gelöscht: leere SPA-Hülle, `tailscale-api-prefetch` = `{}`, kein Bildwert) | 2026-09-28 (Phase **9** — Rotation auf die ersten P9-Bilder: die sieben P8.6-Gate-Symlinks sind weg, drei `p9_step_e_*`-Links rein (P8.6-AK sagt genau das: "sie bleiben stehen, bis P9 eigene Screenshots produziert" — Step E hat als erster P9-Step welche produziert) | 2026-09-19 (Phase 8.6 abgeschlossen — Rotation auf die **Gate-Belege**: sieben Symlinks auf `p86_smoke_*` ersetzen die fünf H-R-3-Links. Das sind die Bilder, auf denen die Freigabe von `v3.0.2` beruht. Bleiben stehen, bis P9 eigene Screenshots produziert.)
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

## Aktueller Inhalt (Phase **9**, Block settings-Nachtrag, Stand 2026-10-05)

Vier Bilder aus `phase9_hardening/scripts/p9_settings_chain_probe.py` gegen die eigene
TLS-Wegwerf-Instanz (`p9_step_g_wegwerf.py`, Port 18775, Chromium 1440×900). Sie zeigen die
**sieben Punkte, die der Nikinger am 2026-10-05 aus der Bildsichtung notiert hat** (Mini-Plan §10,
Locks P9-AM–P9-AS, Abnahme P9-96–P9-102). **Die Bilder vom Vortag sind durch diese ersetzt** — sie
zeigten den alten Stand und sind im Repo versioniert überschrieben worden.

**Zwei der sieben Punkte sind kein Umbau, sondern eine Entscheidung, die im Bild sichtbar wird:**
der unausgewählte Menüpunkt trägt jetzt **dieselbe Fläche wie ein Eingabefeld** (`rgb(12,16,21)`
mit der Haarlinie `rgba(255,255,255,.16)`), und seine Beschriftung steht **mittig**. Die zweite
Hälfte davon ist die **Polster-Entscheidung** vom 2026-10-05: der Menüpunkt erbte als
`.tree__folder` die 32-px-Einrückung der Baumzeile und lag damit 12 px neben seiner Mitte; er
trägt jetzt beidseitig `--space` (8 px). **Das ist die einzige Stelle, an dem die Geometrie des
Menüpunkts von der Baumzeile abweicht** — Höhe, Polster oben/unten, Schrift und Rundung sind
 unverändert gemeinsam, und genau das misst Station S1 (im Beleg genannt, damit die Abweichung
sichtbar bleibt).

| Dateiname | Original | Checkkriterium |
|---|---|---|
| `01_einstellungen_menue.png` | `../docs/screenshots/p9_settings_01_menue_1440.png` | **Der eine Blick, um den es geht:** das Menü „Einstellungen" allein. Drei Punkte müssen sitzen: der **Titel steht mittig**, darunter mit deutlichem Abstand (24 px statt 8 px) die drei Knöpfe, und deren **Beschriftungen stehen mittig in der Fläche** — nicht links. Die Knöpfe sollen als **eingelassene Felder** wirken (dunkel wie ein Eingabefeld, mit feiner Kante), nicht als Plastik. |
| `02_einstellungen_kette.png` | `../docs/screenshots/p9_settings_02_passwort_1440.png` | **Der Zustandsunterschied, den man sehen muss:** links das Menü mit dem **aktiven** Punkt „Passwort ändern" (blauer Verlauf, unverändert wie eine Baumzeile in der Rail), rechts daneben das Passwort-Fenster. Die beiden **un**ausgewählten Punkte tragen die neue eingelassene Fläche — der Unterschied zwischen aktiv und inaktiv muss klar sein. **Das Passwort-Fenster selbst ist unverändert** (P9-AT, wörtlich „great"). |
| `03_einstellungen_drei_fenster.png` | `../docs/screenshots/p9_settings_08_rueckmeldung_1440.png` | **Die Kette in voller Breite** (Menü · Spaces · Space-Detail) und der **sechste Punkt**: alle Knöpfe in den Einstellungs-Fenstern stehen **rechts** — im Spaces-Panel rechtsbündig, im Detail-Panel „Space entfernen"/„Schließen" rechtsbündig. **Das war der gemeldete Überlauf** von „Space entfernen" mit den „(schreiben)"-Zeilen. **Wichtig, ehrlich gesagt:** im Harness gibt es **keine** Mitglieder, die Zeile ist **synthetisch** (Station S15) — der gemeldete Überlauf war hier **nicht vorhanden** (121 px Luft) und wird durch diesen Block **nicht als behoben behauptet**. Bitte in den eigenen Spaces ansehen. |
| `04_einstellungen_schmal_1024.png` | `../docs/screenshots/p9_settings_05_schmal_1024.png` | **Der vierte Punkt bei 1024 px:** im Schmal-Modus steht nur das rechteste Fenster, und der „Zurück"-Knopf oben links trägt jetzt das **echte Chevron-Icon** statt des Textpfeils `←`, der als Glyphe sichtbar nach unten hing. Er ist **mittig im Knopf** (dx/dy = 0 px gemessen) und **ohne Text** — der Name steckt in `aria-label` + `title`, ein Icon ohne Namen wäre für einen Screenreader beschriftungslos. |

**Was in diesem Block nicht gebaut wurde und warum.** Die Einrückung an der Quelle
(`.tree__folder`) auf die Rail einzuschränken wäre die sauberere Lösung gewesen, hätte aber
**zusätzlich** die Space-Zeilen im Panel verschoben — eine zweite, nicht beauftragte Änderung.
Und die Space-Liste kann **leer** bleiben, wenn man sie vor dem Laden der Übersicht öffnet: das ist
ein **Produktbefund aus diesem Lauf**, in die P10-Liste gewandert und in keinem Bild zu sehen
(siehe `phase9_hardening/ABNAHME_MATRIX.md`, Abschnitt „Drei Befunde aus diesem Block").

**Nicht hier, mit Begründung.** Die sechs `p9_trace_*`-Belege sind am 2026-10-02 abgenommen, die
vier `p9_doing_*` mit dem Deploy `v3.1.0`, die `p9_btn2_*`/`p9_btn3_*` mit der Standardoptik der
Knöpfe. Die **Gegenlauf-Bilder** dieses Blocks (`p9_settings_g4*/g5*/g6*`) sind **gelöscht, nicht
eingecheckt** — rot gehört dokumentiert, und dafür liegen die drei JSON-Gegenläufe im Repo.

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
