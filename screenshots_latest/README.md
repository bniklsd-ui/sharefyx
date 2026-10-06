---
status: live
purpose: Verzeichnis der **aktuellen** Phase — Schnellzugriff für Nikinger, kein Grabbing in `docs/screenshots/<phase>_*`
read-when: Nikinger will die jüngsten Sichtprüfungs-Screenshots sehen, ohne durch die History zu scrollen
detail: L3 (Pointer-Verzeichnis, keine eigene Inhaltsquelle)
up: ../phase9_hardening/CLAUDE.md   # aktive Phase
down:
  - ../docs/screenshots/                # kanonische Ablage; diese Verzeichnis ist nur Symlink-Komfort
updated: 2026-10-06 (**alle acht** Bilder der zweiten Bildsichtung verlinkt, Nikinger-Anordnung: *„give me all 8 in the screenshots latest folder"* — die vier bisherigen Symlinks sind **ersetzt**, nicht ergänzt, und die vier neuen tragen Namen, die ihren Inhalt sagen; **die Tabelle ist neu geschrieben** mit einer Zeile und einem Checkkriterium je Bild. Aus dem README-Vortag (vier Bilder, bewusst auf vier reduziert) wird damit ein vollständiges Leseverzeichnis des Blocks · **der Punkt, den die Bilder nicht tragen können**, steht ausdrücklich darin: die Mitgliederliste `#space-member-list` hat **keine Mitglieder** im Harness (Home-Space), ihr `list-style/padding/margin` ist **aus dem Browser-Standard abgeleitet** und nicht gemessen) | 2026-10-05 (**Rotation auf die Nachtrags-Belege** — der dritte Symlink zeigt jetzt `p9_settings_08_rueckmeldung_1440.png` statt des Duplikats `04_drei_panels`; die **Tabelle ist mitgedreht** (die vier alten Zeilen standen noch auf B17, obwohl die Symlinks längst auf den settings-Block zeigten) · **die Kette ist repariert**: zwei Fäden trugen ein `updated: `-Präfix nach dem Trenner, damit war `rotate_index_updates.sh` für sie blind; `KNOWN_OFFENDERS` ist um diesen Eintrag gekürzt · **die Gegenlauf-Bilder des Blocks sind gelöscht**, rot eingecheckt sind nur die drei JSON-Gegenläufe) | 2026-10-05 (**Rotation auf die settings-Belege** — vier Symlinks neu, die vier B17-Links (`01_archivieren_*` … `04_editor_gesamt.png`) raus. Das ist die **offene Sichtfrage** des Blocks: die Messung ist 39/39, die Bilder sind angesehen, die Sichtprüfung des Nikingers steht aus. Bewusst **nicht** verlinkt: `p9_settings_06/07` (Passwortwechsel und Space-Anlegen sind Handgriffe ohne Aussagebild) und `03_updatelog_1440` (derselbe Inhalt wie im Fenster davor, nur an anderer Stelle) — ein Leseverzeichnis mit 7 Bildern wäre wieder ein Scrollen durch History) | 2026-10-02 (**Rotation auf die B17-Belege** — vier Symlinks neu, die sechs `p9_trace_*`-Links raus; die sind abgenommen und liegen versioniert in `docs/screenshots/`. Der Block ersetzt den Vorsichtsknopf auf die Standardfläche, und **diese Bilder sind die offene Sichtfrage**: die Messung ist 14/14, die Sichtung steht aus) | 2026-10-02 (**Abnahme durch den Nikinger mit Restbefund**: die sechs Bilder sind freigegeben; als Notiz hält er fest, dass noch nicht alle Knöpfe an das Schema angepasst sind — abgelegt als **B17** im Backlog von `phase9_hardening/CLAUDE.md` mit der gemessenen Klassenliste, *kein* Code-Touch) | 2026-10-02 (**die fünf Bilder und die Probe sind neu — der alte Beleg war der Gegenlauf.** Beim erneuten Lesen fiel auf: `p9_trace_probe.json` stand auf `alle_ok: false` (S5 rot) und Bild 05 zeigte `beta` statt `alpha`, weil der Hand-Gegenlauf des trace-Blocks Skript und Ausgabepfade geteilt hat. Eigener Lauf gegen die Zwei-Principalen-Wegwerf-Instanz → **8/8**, Bilder neu (Bild 02 ist zeichengleich), Wächter `test_committed_probe_evidence.py` verhindert die Wiederholung) | 2026-10-02 (Rotation auf die `p9_trace_*`-Belege: sechs Symlinks neu, die vier `p9_doing_*`-Links raus — der doing-Block ist mit dem Deploy `v3.1.0` erledigt und abgenommen) | 2026-10-02 (Rotation auf die `p9_doing_*`-Belege: vier Symlinks neu, die drei `p9_btn2_*`-Links raus — der Knopfoptik-Fall ist erledigt und abgenommen) | 2026-10-01 (Rotation auf die `.toolbar-btn`-Belege (`p9_btn2_*`): drei Symlinks neu, die drei `p9_step_e_*`-Links raus — Step E ist als Beleg in `docs/screenshots/` erledigt und die aktuell offene Sichtfrage ist die Knopfoptik vor dem Deploy. **Vier unversionierte Tailscale-Kopien** mit Leerzeichen im Namen wandern nach `docs/screenshots/p9_step_a_01..04_*` (Infra-Beleg zu A3, ausdrücklich keine Sichtprüfung), die fünfte Datei `Machines - Tailscale.html` ist gelöscht: leere SPA-Hülle, `tailscale-api-prefetch` = `{}`, kein Bildwert) | 2026-09-28 (Phase **9** — Rotation auf die ersten P9-Bilder: die sieben P8.6-Gate-Symlinks sind weg, drei `p9_step_e_*`-Links rein (P8.6-AK sagt genau das: "sie bleiben stehen, bis P9 eigene Screenshots produziert" — Step E hat als erster P9-Step welche produziert) | 2026-09-19 (Phase 8.6 abgeschlossen — Rotation auf die **Gate-Belege**: sieben Symlinks auf `p86_smoke_*` ersetzen die fünf H-R-3-Links. Das sind die Bilder, auf denen die Freigabe von `v3.0.2` beruht. Bleiben stehen, bis P9 eigene Screenshots produziert.)
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

## Aktueller Inhalt (Phase **9**, zweite Bildsichtung, Stand 2026-10-06)

**Alle acht** Bilder aus `phase9_hardening/scripts/p9_settings_polish_probe.py` (29/29 Stationen
grün, **sechs Gegenläufe G7–G12 6 von 6 wirksam**) gegen die eigene TLS-Wegwerf-Instanz
(`p9_step_g_wegwerf.py`, Port 18775, Chromium; 1440×900, Bild 05 mit 1024×768). **Nikinger-
Anordnung vom 2026-10-05:** *„give me all 8 in the screenshots latest folder"* — vorher standen hier
vier Bilder mit der Begründung, ein Leseverzeichnis mit sieben sei wieder Scrollen durch History.

**Was der Block gemacht hat** (Mini-Plan §11, Locks P9-AU–P9-AZ, Abnahme P9-103–P9-111): die
Menüpunkte tragen jetzt die **Standardknopf-Fläche** statt der des Eingabefeldes und haben **8 px
Abstand** untereinander (vorher 0 px — „glued to each each other"), der ausgewählte Punkt die
**Akzentfläche**; „Ändern" ist rot wie „Archivieren" (Vorsicht: teuer rückgängig zu machen) und
heiße **„Schließen"**; die Beschriftung der Space-Zeilen steht bündig mit dem Panel-Titel; das
Namensfeld im Detail-Panel steht beidseitig bündig mit der Zeile darunter.

| Dateiname | Original | Checkkriterium |
|---|---|---|
| `01_einstellungen_menue.png` | `../docs/screenshots/p9_settings_01_menue_1440.png` | **Der eine Blick, um den es geht.** Drei Punkte mit **sichtbarem Abstand** untereinander (vorher klebten sie aneinander), jede Fläche **wie „Schließen"/„Space anlegen"** — also Standard-Knopf, nicht wie ein Eingabefeld (kein Vertiefungs-Look). Der Titel steht weiter **mittig**, die Beschriftungen **mittig in der Fläche** (Textmitte 720 px == Knopfmitte 720 px) |
| `02_einstellungen_passwort.png` | `../docs/screenshots/p9_settings_02_passwort_1440.png` | **Zwei Dinge an einem Bild:** der Punkt **„Passwort ändern"** trägt jetzt die **Akzentfläche** (blau, wie ein Hauptknopf) — der ausgewählte Zustand. Und im Fenster: **„Ändern" ist rot** (Vorsicht wie „Archivieren", **keine** gefüllte rote Fläche) und der zweite Knopf heißt **„Schließen"** statt „Abbrechen". Das Passwort-Fenster selbst ist unverändert (P9-AT, wörtlich „great") |
| `03_einstellungen_updatelog.png` | `../docs/screenshots/p9_settings_03_updatelog_1440.png` | **Dritte Stufe, unverändert gebaut** — nur der Punkt **„Update-Log"** trägt jetzt die Akzentfläche. Das Fenster selbst: **unverändert**, wörtlich „great, as well as the update log" |
| `04_einstellungen_drei_fenster.png` | `../docs/screenshots/p9_settings_04_drei_panels_1440.png` | **Die Kette in voller Breite** und die Bündigkeit: die **Space-Zeilen stehen jetzt bündig mit dem Titel „Spaces verwalten"** (vorher 33 px daneben). Unten: „Name des neuen Space" und **„Space anlegen" auf einer Zeile**, das Feld bündig links mit dem Panelinhalt, der Knopf bündig rechts — und **der Knopf behält seine Größe** (142 px; vorher stand er allein auf der Zeile mit 80 px Versatz) |
| `05_einstellungen_schmal_1024.png` | `../docs/screenshots/p9_settings_05_schmal_1024.png` | **Derselbe Fix bei 1024 px**, wo nur das rechteste Panel steht: das Namensfeld steht jetzt **beidseitig bündig** mit der Zeile darunter (gemessen 0,0 px auf **beiden** Kanten; vorher 12 px zu schmal). Der „Zurück"-Knopf oben links trägt das Chevron-Icon, mittig, ohne Text |
| `06_einstellungen_passwort_gewechselt.png` | `../docs/screenshots/p9_settings_06_passwort_gewechselt.png` | **Nach dem echten Passwortwechsel** (HTTP 200, Toast, Sitzung besteht weiter). Kein Sichtprüfungs-Beleg — ein Handgriff ohne Aussagebild; aufgenommen, weil alle acht gewünscht waren |
| `07_einstellungen_space_angelegt.png` | `../docs/screenshots/p9_settings_07_space_angelegt.png` | **Nach dem Anlegen eines echten Space** (Zeile 16 → 17). Die **neue** Zeile steht bündig mit dem Titel wie die alten — der Fix gilt auch für frische Einträge, nicht nur für die vorhandenen |
| `08_einstellungen_rueckmeldung.png` | `../docs/screenshots/p9_settings_08_rueckmeldung_1440.png` | **Nach ESC** — die Kette ist geschlossen. Blatt als Beweis, dass die Tastenschließung von rechts nach links weiter gilt und der Schlüssel-Knopf rechts ausgerichtet bleibt |

**Was in diesem Block nicht gebaut wurde und warum.** Die Beschriftung der **Mitgliederliste**
(`#space-member-list`) bekommt `list-style: none; padding: 0; margin: 0` **aus dem
Browser-Standard abgeleitet** — der Browser lieferte dort Aufzählungspunkte **und** 40 px Einzug
(also dieselbe Fehlerart, nur größer). **Im Wegwerf-Harness ist das nicht messbar**, weil der
einzige eigene Space ein Home-Space ist und keine Mitglieder hat; ein synthetisches Mitglied wäre
ein Beleg für einen Zustand, den es live nicht gibt. **Bitte in den eigenen Spaces ansehen** — das
ist der einzige Punkt, den die Bilder nicht tragen können.

**Die Gegenlauf-Bilder** (`p9_settings_g7*` … `g12*`) sind **gelöscht, nicht eingecheckt** — rot
gehört dokumentiert, und dafür liegen die sechs JSON-Gegenläufe im Repo
(`phase9_hardening/probes/p9_settings_polish_probe_g*_gegenprobe.json`).

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
