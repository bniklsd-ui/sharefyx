---
status: live
purpose: Verzeichnis der **aktuellen** Phase — Schnellzugriff für Nikinger, kein Grabbing in `docs/screenshots/<phase>_*`
read-when: Nikinger will die jüngsten Sichtprüfungs-Screenshots sehen, ohne durch die History zu scrollen
detail: L3 (Pointer-Verzeichnis, keine eigene Inhaltsquelle)
up: ../phase9_hardening/CLAUDE.md   # aktive Phase
down:
  - ../docs/screenshots/                # kanonische Ablage; diese Verzeichnis ist nur Symlink-Komfort
updated: 2026-10-06 (**Sichtprüfung, dritte Runde: 8 Bilder, sieben ✅ und ein Punkt** — 01 *„passt"* · 02 *„sieht für mich passend aus"* · 03 *„sieht gut aus"* · 05 *„yo, passt"* · 06 *„identisch zu 1, passt"* · 07 *„passt so"* · **04 zurückgenommen** (*„ah, nehme 04 zurück, man muss scrollen. Passt so"*) · 08 mit **einem** Punkt, daraus Lock **P9-BF**: *„den Auswahl buttons der einzelnen Spaces bitte ein paar Px nach links erweitern, sodass innerliegender Text und Button Grenze den Standard Abstand einhalten"*). **Alle acht Bilder neu aufgenommen**; **Bild 08 ist die einzige verlangte Neuerstellung** — die Kästchen ragen jetzt 8 px nach links, innen **9 px wie rechts** statt 1 gegen 9, und die Beschriftung bleibt bündig mit dem Titel | 2026-10-06 (**26 zusätzliche Symlinks ergänzt und am selben Tag zurückgenommen**) — der Nikinger meinte mit *„alle relevanten Screenshots noch nach latest ziehen"* nur die Bilder **des neuesten Laufs** (die acht aus `p9_settings_kastchen_probe.py`), nicht die älteren Phase-9-Blöcke. Zurückgenommen per `git revert`, damit die Zurücknahme selbst nachlesbar bleibt und niemand sie in der nächsten Session wiederholt | 2026-10-06 (**alle acht Bilder neu aufgenommen**, aus dem Block „Kästchen enger" — Probe **48/48**, **sechs Gegenläufe G13–G18 6 von 6** wirksam) · **Bild 08 zeigt wieder Menü + „Spaces verwalten"**, also genau die Ansicht, aus der deine Worte kamen (der erste Lauf zeigte nur das Menü, weil die Liste beim ESC mit geschlossen wurde) · **Bild 07** zeigt die neu angelegte Zeile **aufgerollt** (`scrollIntoView`) *und* die Anlegezeile — und der Titel ist dort **nicht** im Bild, was das Kriterium jetzt sagt · **Bild 04** nennt die Position der Hinzufügen-Optionen (y 205..246) · **Bild 01** zeigt die Menüpunkte **flacher** (31,69 px statt 35,69 px), ihre **Breite bleibt** bei 131 px | 2026-10-06 (**Sichtprüfung des Nikingers notiert** — **02 · 03 · 05 · 06 freigegeben**, **01 · 04 · 07 · 08 mit neuen Punkten**, die als **P9-BA–P9-BD** (Abnahme **P9-112–P9-115**) in §12 des settings-Plans **mit allen Messwerten** stehen und **nicht gebaut** sind: alle drei Menüpunkte messen **131 × 35,69 px** bei Beschriftungen von 106/113/77 px (19 px Leerraum), die Space-Zeilen **184–239 px**; in **Bild 04 sind die Hinzufügen-Optionen nachgewiesen im eingecheckten PNG** (y 207..231) und stehen nur oben, weil der Mitgliederbereich leer ist; **Bild 07 zeigt die neue Zeile gar nicht**, weil das Panel scrollt) | 2026-10-06 (**alle acht** Bilder der zweiten Bildsichtung verlinkt, Nikinger-Anordnung: *„give me all 8 in the screenshots latest folder"* — die vier bisherigen Symlinks sind **ersetzt**, nicht ergänzt, und die vier neuen tragen Namen, die ihren Inhalt sagen; **die Tabelle ist neu geschrieben** mit einer Zeile und einem Checkkriterium je Bild. Aus dem README-Vortag (vier Bilder, bewusst auf vier reduziert) wird damit ein vollständiges Leseverzeichnis des Blocks · **der Punkt, den die Bilder nicht tragen können**, steht ausdrücklich darin: die Mitgliederliste `#space-member-list` hat **keine Mitglieder** im Harness (Home-Space), ihr `list-style/padding/margin` ist **aus dem Browser-Standard abgeleitet** und nicht gemessen) | 2026-10-05 (**Rotation auf die Nachtrags-Belege** — der dritte Symlink zeigt jetzt `p9_settings_08_rueckmeldung_1440.png` statt des Duplikats `04_drei_panels`; die **Tabelle ist mitgedreht** (die vier alten Zeilen standen noch auf B17, obwohl die Symlinks längst auf den settings-Block zeigten) · **die Kette ist repariert**: zwei Fäden trugen ein `updated: `-Präfix nach dem Trenner, damit war `rotate_index_updates.sh` für sie blind; `KNOWN_OFFENDERS` ist um diesen Eintrag gekürzt · **die Gegenlauf-Bilder des Blocks sind gelöscht**, rot eingecheckt sind nur die drei JSON-Gegenläufe) | 2026-10-05 (**Rotation auf die settings-Belege** — vier Symlinks neu, die vier B17-Links (`01_archivieren_*` … `04_editor_gesamt.png`) raus. Das ist die **offene Sichtfrage** des Blocks: die Messung ist 39/39, die Bilder sind angesehen, die Sichtprüfung des Nikingers steht aus. Bewusst **nicht** verlinkt: `p9_settings_06/07` (Passwortwechsel und Space-Anlegen sind Handgriffe ohne Aussagebild) und `03_updatelog_1440` (derselbe Inhalt wie im Fenster davor, nur an anderer Stelle) — ein Leseverzeichnis mit 7 Bildern wäre wieder ein Scrollen durch History) | 2026-10-02 (**Rotation auf die B17-Belege** — vier Symlinks neu, die sechs `p9_trace_*`-Links raus; die sind abgenommen und liegen versioniert in `docs/screenshots/`. Der Block ersetzt den Vorsichtsknopf auf die Standardfläche, und **diese Bilder sind die offene Sichtfrage**: die Messung ist 14/14, die Sichtung steht aus) | 2026-10-02 (**Abnahme durch den Nikinger mit Restbefund**: die sechs Bilder sind freigegeben; als Notiz hält er fest, dass noch nicht alle Knöpfe an das Schema angepasst sind — abgelegt als **B17** im Backlog von `phase9_hardening/CLAUDE.md` mit der gemessenen Klassenliste, *kein* Code-Touch) | 2026-10-02 (**die fünf Bilder und die Probe sind neu — der alte Beleg war der Gegenlauf.** Beim erneuten Lesen fiel auf: `p9_trace_probe.json` stand auf `alle_ok: false` (S5 rot) und Bild 05 zeigte `beta` statt `alpha`, weil der Hand-Gegenlauf des trace-Blocks Skript und Ausgabepfade geteilt hat. Eigener Lauf gegen die Zwei-Principalen-Wegwerf-Instanz → **8/8**, Bilder neu (Bild 02 ist zeichengleich), Wächter `test_committed_probe_evidence.py` verhindert die Wiederholung) | 2026-10-02 (Rotation auf die `p9_trace_*`-Belege: sechs Symlinks neu, die vier `p9_doing_*`-Links raus — der doing-Block ist mit dem Deploy `v3.1.0` erledigt und abgenommen) | 2026-10-02 (Rotation auf die `p9_doing_*`-Belege: vier Symlinks neu, die drei `p9_btn2_*`-Links raus — der Knopfoptik-Fall ist erledigt und abgenommen) | 2026-10-01 (Rotation auf die `.toolbar-btn`-Belege (`p9_btn2_*`): drei Symlinks neu, die drei `p9_step_e_*`-Links raus — Step E ist als Beleg in `docs/screenshots/` erledigt und die aktuell offene Sichtfrage ist die Knopfoptik vor dem Deploy. **Vier unversionierte Tailscale-Kopien** mit Leerzeichen im Namen wandern nach `docs/screenshots/p9_step_a_01..04_*` (Infra-Beleg zu A3, ausdrücklich keine Sichtprüfung), die fünfte Datei `Machines - Tailscale.html` ist gelöscht: leere SPA-Hülle, `tailscale-api-prefetch` = `{}`, kein Bildwert) | 2026-09-28 (Phase **9** — Rotation auf die ersten P9-Bilder: die sieben P8.6-Gate-Symlinks sind weg, drei `p9_step_e_*`-Links rein (P8.6-AK sagt genau das: "sie bleiben stehen, bis P9 eigene Screenshots produziert" — Step E hat als erster P9-Step welche produziert) | 2026-09-19 (Phase 8.6 abgeschlossen — Rotation auf die **Gate-Belege**: sieben Symlinks auf `p86_smoke_*` ersetzen die fünf H-R-3-Links. Das sind die Bilder, auf denen die Freigabe von `v3.0.2` beruht. Bleiben stehen, bis P9 eigene Screenshots produziert.)
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

## Aktueller Inhalt (Phase **9**, dritte Bildsichtung, Stand 2026-10-06)

**Alle acht** Bilder aus `phase9_hardening/scripts/p9_settings_kastchen_probe.py` (**48/48**
Stationen grün, **sechs Gegenläufe G13–G18 6 von 6 wirksam**) gegen die eigene TLS-Wegwerf-Instanz
(`p9_step_g_wegwerf.py`, Port 18775, Chromium; 1440×900, Bild 05 mit 1024×768).

**Was der Block gemacht hat** (Plan §12.1, Locks P9-BB/BC/BD/**BE**, Abnahme P9-116–P9-119): die drei
**Menüpunkte sind flacher** (4 px Polster oben/unten, gemessene Höhe **31,69 px** statt 35,69 px —
die Breite bleibt **131 px**, das ist P9-BA, vom Nikinger ausdrücklich auf „nur bei Spaces
verwalten" eingeschränkt); die **Space-Zeilen umklammern ihr eigenes Label** (Kästchen 92–147 px
statt 330 px für alle, rechts **9 px** statt 192–245 px Leerraum, die Beschriftung bleibt 1 px
bündig mit dem Titel); das **Spaces-Fenster ist schmaler** (338 px statt 380 px, **nur dieses** —
Menü, Passwort, Detail und Update-Log behalten ihre Breite).

| Dateiname | Original | Checkkriterium |
|---|---|---|
| `01_einstellungen_menue.png` | `../docs/screenshots/p9_settings_01_menue_1440.png` | **Die Höhe, um die es geht.** Die drei Punkte sind **flacher**: **31,69 px** statt 35,69 px (das Polster oben/unten ist von 6 px auf 4 px gegangen). Die **Breite bleibt bei allen dreien gleich (131 px)** und die Beschriftung bleibt **mittig** (Textmitte == Knopfmitte). Wenn du „bigger" als **Leerraum** gemeint hast, dann ist das hier **nicht** behoben — das war P9-BA und der Auftrag lautete „nur bei Spaces verwalten" |
| `02_einstellungen_passwort.png` | `../docs/screenshots/p9_settings_02_passwort_1440.png` | Unverändert gegenüber dem 2026-10-05 (du hattest es freigegeben): „Passwort ändern" trägt die **Akzentfläche**, **„Ändern" ist rot** (Vorsicht, keine gefüllte rote Fläche), der zweite Knopf heißt **„Schließen"**. Das Passwort-Fenster selbst unangetastet |
| `03_einstellungen_updatelog.png` | `../docs/screenshots/p9_settings_03_updatelog_1440.png` | Unverändert (freigegeben): nur der Punkt **„Update-Log"** trägt jetzt die Akzentfläche, das Fenster selbst ist unangetastet |
| `04_einstellungen_drei_fenster.png` | `../docs/screenshots/p9_settings_04_drei_panels_1440.png` | **Die Kette in voller Breite — und die Stelle, um die es bei Bild 04 geht: die Hinzufügen-Optionen stehen im rechten Panel („alpha") auf y 205..246**, das Namensfeld darüber auf y 157..197, direkt unter dem Hinweistext (16 px). Sie stehen **oben**, weil der Mitgliederbereich leer ist (Home-Space). Mitte: die Space-Zeilen umklammern jetzt ihr Label und stehen bündig mit „Spaces verwalten". Links: die Menüpunkte sind flacher |
| `05_einstellungen_schmal_1024.png` | `../docs/screenshots/p9_settings_05_schmal_1024.png` | Unverändert (freigegeben) — der Schmal-Modus mit dem Zurück-Knopf. **Zusätzlich geprüft:** die feste Breite des Spaces-Fensters ist hier **zurückgenommen**, das Panel flext (gemessen 422 px statt 338 px) |
| `06_einstellungen_passwort_gewechselt.png` | `../docs/screenshots/p9_settings_06_passwort_gewechselt.png` | Unverändert (freigegeben) — nach dem echten Passwortwechsel (HTTP 200, Toast). Kein Sichtprüfungs-Beleg |
| `07_einstellungen_space_angelegt.png` | `../docs/screenshots/p9_settings_07_space_angelegt.png` | **Die neu angelegte Zeile — diesmal aufgerollt.** Sie steht als **letzte** in der Liste (`zz-…`, deshalb landet sie sortiert am Ende) und ist **im Sichtbereich**: gemessen lag sie vorher bei y 1704 **unterhalb** des Panel-Folds (836 px), nach dem `scrollIntoView` des Laufs liegt sie bei y 765 vollständig im Bild. **Direkt darunter** die Anlegezeile: Feld und „Space anlegen" auf **einer** Zeile, das Feld **138 px** (vorher 180 px) — **der Platzhalter „Name des neuer…" ist deshalb abgeschnitten**, das ist der Preis der Verschmalung. Der **Titel ist hier nicht im Bild** (die Liste ist unten aufgerollt) — die Bündigkeit mit dem Titel zeigen Bild 04 und Bild 08 |
| `08_einstellungen_rueckmeldung.png` | `../docs/screenshots/p9_settings_08_rueckmeldung_1440.png` | **Dein Punkt vom 2026-10-06, umgesetzt (P9-BF):** jedes Kästchen ragt jetzt **8 px nach links** aus der Inhaltskante, damit der Text **innen** wieder den Standardabstand hält — vorher standen innen **1 px links** gegen **9 px rechts**. **Die Beschriftung selbst ist nicht gewandert**: sie steht weiter 1 px bündig mit „Spaces verwalten". **Das Vergleichsbild für deinen Punkt aus Bild 08.** Menü + „Spaces verwalten" nach ESC (das Detail war offen und wurde geschlossen, die Liste bleibt): die **Zeilen umklammern ihr Label** — die rechten Kanten sind jetzt **verschieden** und stehen direkt hinter dem Text (9 px Leerraum statt 192–245 px), die Beschriftung steht bündig mit dem Titel; das **Fenster ist schmaler** (338 px). Links die drei flacheren Menüpunkte |

### Stand der Sichtprüfung, dritte Runde (Nikinger, 2026-10-06, nach dem Block „Kästchen enger")

| Bild | Urteil |
|---|---|
| `01_einstellungen_menue.png` | ✅ *„passt"* |
| `02_einstellungen_passwort.png` | ✅ *„sieht für mich passend aus"* |
| `03_einstellungen_updatelog.png` | ✅ *„sieht gut aus"* |
| `04_einstellungen_drei_fenster.png` | ✅ *„ja"* — der erste Einwand (wo sind Namensfeld, Hinzufügen und Schließen) ist **zurückgenommen**: *„ah, nehme 04 zurück, man muss scrollen. Passt so"* |
| `05_einstellungen_schmal_1024.png` | ✅ *„yo, passt"* |
| `06_einstellungen_passwort_gewechselt.png` | ✅ *„identisch zu 1, passt"* |
| `07_einstellungen_space_angelegt.png` | ✅ *„passt so"* |
| `08_einstellungen_rueckmeldung.png` | ✅ *„perfekt, passt"* — **ein Punkt → P9-BF gebaut**, dieses Bild war die einzige verlangte Neuerstellung: *„den Auswahl buttons der einzelnen Spaces bitte ein paar Px nach links erweitern, sodass innerliegender Text und Button Grenze den Standard Abstand einhalten"* |

### Stand der Sichtprüfung, zweite Runde (2026-10-06 — vier Punkte, vier neue)

| Bild | Urteil |
|---|---|
| `01_einstellungen_menue.png` | **behoben (b)** — *„the update-log button is still bigger, I think you need to decrease its height"*; Antwort auf die Rückfrage: **(b) zusätzlich flacher**, Polster 6 → 4 px, Höhe **31,69 px**. Die Deutung „bigger = Leerraum" (P9-BA) hast du mit *„nur bei Spaces verwalten"* auf das Spaces-Panel eingeschränkt — die Menüpunkte behalten ihre Breite |
| `02_einstellungen_passwort.png` | ✅ *„looks fine now"* (unverändert) |
| `03_einstellungen_updatelog.png` | ✅ *„great"* (unverändert) |
| `04_einstellungen_drei_fenster.png` | **Kriterium korrigiert, kein Defekt** — *„where did the space hinzufügen options go?"*: die Optionen **sind** im Bild, **y 205..246** im rechten Panel, 16 px unter dem Hinweistext (Home-Space, Mitgliederbereich leer). Das alte Kriterium sagte dir nicht, wo du suchen sollst; das neue nennt die Position |
| `05_einstellungen_schmal_1024.png` | ✅ *„looks fine now"* (unverändert) |
| `06_einstellungen_passwort_gewechselt.png` | ✅ *„yes"* (unverändert) |
| `07_einstellungen_space_angelegt.png` | **behoben** — *„I honestly don't see that"*: die Zeile war da, aber **unterhalb des Sichtbereichs** (das Panel scrollt). Der Lauf rollt sie jetzt mit `scrollIntoView` auf, und die Station prüft das **Rechteck im Panel**; zusätzlich ist die **Anlegezeile mit im Bild**, die vorher aus keinem Bild mehr sichtbar war |
| `08_einstellungen_rueckmeldung.png` | **behoben** — *„move the button borders a little bit further to the left, leave the text where it is now. Cut the not used space from the right"* + *„nur bei Spaces verwalten, dort die Buttons der einzelnen Spaces nach Links, und das Fenster rechts verkleinern, aber nur dieses"*: Zeilen umklammern ihr Label (9 px statt 192–245 px Leerraum), Fenster 338 statt 380 px, Text unverändert bündig |

Diese acht Punkte stehen als **P9-BB/BC/BD/BE** (Abnahme **P9-116–P9-119**) in
`docs/concepts/phase9_hardening_block_settings_plan.md` §12.1 — **gebaut am 2026-10-06**.

**Was in diesem Block nicht gebaut wurde und warum.** Die Beschriftung der **Mitgliederliste**
(`#space-member-list`) steht weiter auf `list-style: none; padding: 0; margin: 0`, **aus dem
Browser-Standard abgeleitet** und **nicht gemessen** — im Wegwerf-Harness hat der einzige eigene
Space keine Mitglieder. **Bitte in deinen eigenen Spaces ansehen**, das ist der einzige Punkt, den
die acht Bilder nicht tragen können.

**Die Gegenlauf-Bilder** (`p9_settings_g13*` … `g18*`) sind **gelöscht, nicht eingecheckt** — rot
gehört dokumentiert, und dafür liegen die JSON-Gegenläufe im Repo
(`phase9_hardening/probes/p9_settings_kastchen_probe_g*.json`).

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
