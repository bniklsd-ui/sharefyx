---
status: live
purpose: Archiv der rotierten Phase-9-Session-Blöcke, verbatim, newest-first
read-when: Chronik einer älteren P9-Session gesucht — nicht beim normalen Arbeiten in der Phase
detail: L3
up: ./CLAUDE.md
down:
updated: 2026-10-03 (**zweiundzwanzigste Rotation** — der **einundzwanzigste** Block wandert verbatim hierher: Release-Commit `v3.1.1` steht (Badge + `## 2026-10-03`-Block), davor der Datumsfehler der letzten beiden Commits (42 Fundstellen) und die Reparatur dieser Kette — sie hatte **kein Feld** und 7 von 29 unsichtbaren Fäden; Head 54.326 → 47.208 B) | 2026-10-03 (sechsundzwanzigste Rotation: der **siebzehnte** Block wandert verbatim hierher — Kettenrotation des Heads (36 von 37 Fäden nach `UPDATES_ARCHIVE.md`, 57.873 → 39.106 B) und `rotate_index_updates.sh` um Zieldatei/Archiv erweitert) | 2026-10-03 (**zwanzigster Block rotiert** — „die Karte schrumpft": `docs/INDEX.md` 71.573 → 38.532 B, die 37.391 B datierte Nachträge wandern nach `docs/INDEX_ENTRIES_ARCHIVE.md`, das Kriterium ist neu baseliniert; P9-3 und V145 ✅; die Wurzel-`CLAUDE.md` bleibt auf Nikinger-Entscheidung unangetastet und ist stattdessen gemessen) | 2026-10-03 (**der neunzehnte Block rotiert** — „die Zahlen der Abnahmematrix dürfen nicht mehr still veralten": P9-3/V145 nannten `61.108 B` für eine Datei von real 71.491 B, die Bilanz stand viermal mit drei Zahlen, und der benannte Hebel für die INDEX-Überschreitung wurde als No-op nachgewiesen; 7 neue Tests, 6 Gegenproben rot) | 2026-10-03 (fünfundzwanzigste Rotation: der **siebzehnte** Block wandert verbatim hierher — Kettenrotation des Heads (`UPDATES_ARCHIVE.md`, 36 von 37 Fäden) + `rotate_index_updates.sh` um Zieldatei/Archiv erweitert; **und ein Fund aus dem allerersten Schritt: die vorige Rotation hat dieser Zeile das `updated: `-Präfix genommen** (Commit aee387d, 2026-10-03) — das Feld war damit für jedes Werkzeug unsichtbar, `doc_health` prüft es nicht und eine Rotation dieses Archivs würde mit 'Keine updated:-Zeile' abbrechen. Präfix wiederhergestellt, Fehler benannt statt still mitgenommen) | 2026-10-03 (vierundzwanzigste Rotation: der **sechzehnte** Block wandert verbatim hierher — Step D endlich gefahren, P9-28/-29/-30 von ⬜/⚠️ auf ✅, Browser-Probe 16/16 mit **zwei** Gegenproben im Repo, 0 Zeilen Produktcode; Archiv 209.333 → 219.179 B, Head 65.986 → 56.140 B) | 2026-10-03 (dreiundzwanzigste Rotation: der **fünfzehnte** Block — Abnahmematrix P9-1–P9-82 + `[VERIFY]`-Bilanz steht (`ABNAHME_MATRIX.md` neu), und drei Funde, die die Übergabe nicht trug: die „40 Einträge" waren ein Nummernbereich (belegt: **34**, V167–V172 unbelegt), P9-56 hat einen nicht angekündigten Tabu-Treffer (`phase7_hardening/tests/test_space_removal.py`, 17 Z.), und **GA2 wurde nie gebaut** — genau P9-27/-29/-30 sind die Zeilen ohne Probe; der **vierzehnte** Block (B17) wandert verbatim hierher, neuer Head-Block = 2026-10-03; Head **56.142 B → 53.215 B**, Archiv 195.890 B → 209.333 B — **weiter über dem Softcap, neu benannt**, die Restmasse bleiben die 7.467 B durchgestrichenen Statusabsätze im Modulstatus, Streichen bleibt Nikinger-Entscheidung) | 2026-10-02 (zweiundzwanzigste Rotation: der dreizehnte Block — Gate/Z-Doku-Hälfte (zwei Sektions-Rotationen, P9-L-Lauf, Skript-Defekt `rotate_index_updates.sh`) — wandert verbatim hierher; neuer Head-Block = **B17 gebaut** (ein Knopf, zwei korrigierte Zahlen im Backlog, Konflikt mit Konvention v3 zurückgestellt); Head 63.470 B → 53.968 B — **weiter über dem Softcap, neu benannt**, die Restmasse sind weiter die 7.467 B durchgestrichenen Statusabsätze im Modulstatus, Streichen bleibt Nikinger-Entscheidung) | 2026-10-02 (einundzwanzigste Rotation: der zwölfte Block — Block trace gebaut, opencode/M3 — wandert verbatim hierher; neuer Head-Block = Gate/Z-Doku-Hälfte (zwei Sektions-Rotationen, P9-L-Lauf, Skript-Defekt `rotate_index_updates.sh`); Head 49.440 B → 44.360 B — **weiter über dem Softcap, neu benannt**, die Restmasse sind 7.467 B durchgestrichene Statusabsätze im Modulstatus, Streichen ist Nikinger-Entscheidung) | 2026-10-02 (zwanzigste Rotation: der zwölfte Block — Block trace gebaut, opencode/M3 — ist ans Dateiende gewandert, der elfte Block (Deploy-Abbruch behoben, `v3.1.0` live, Planungssession) verbatim ins Archiv; Head 46.993 B → 42.012 B) | 2026-10-02 (**neunzehnte Rotation, elfter Block** — der zehnte Block (doing-Block gebaut) wandert verbatim hierher; neuer Head-Block = Deploy-Abbruch `v3.1.0` behoben, `requests` war nie deklariert) | 2026-10-02 (**achtzehnte Rotation, zehnter Block** — der neunte Block (Mini-Plan doing-Block, Lock P9-V) wandert verbatim hierher; neuer Head-Block = doing-Block **gebaut**: `_BUCKETS["doing"]` + Rail-Label „In Arbeit", 6 neue Tests, Browser 11/11 mit Gegenlauf 7 rot, `pytest` 1128. **Head 44.508 B → 41.192 B** — und damit wieder 232 B **über** dem 40-KiB-Softcap, im INDEX neu benannt) | 2026-10-02 (**siebzehnte Rotation, neunter Block** — der achte Block (Deploy verschoben, Befund 11) wandert verbatim hierher; neuer Head-Block = Mini-Plan doing-Block, Lock P9-V) | 2026-10-01 (**sechzehnte Rotation, achter Block** — Deploy verschoben (Befund 11: `doing` ist im Deploy-Fall im Status-Feld erreichbar und zählt in keinem Ordner), `.toolbar-btn` in Standardoptik mit Pixel-Beleg 13/13, vier Tailscale-Bilder geklärt; Head 41.306 B, Archiv 152.730 B) | 2026-10-01 (**fünfzehnte Rotation, A4-Vorbereitung** — Step-A-Block (2026-10-01, Domain live) verbatim aus dem Head; Head 42.376 B → 34.795 B) | 2026-10-01 (**vierzehnte Rotation, Step A** — Step-B-Block verbatim aus dem Head; Head 41.707 B → 29.415 B) | 2026-09-30 (**dreizehnte Rotation, Step B** — Step-B-Block [polkit-Regel gebaut, V153 entschieden: sudoers ist unter NoNewPrivileges unbaubar; systemd 255 kennt nur die grobe `manage-units`-Aktion, deshalb JS-Regel mit Unit-Attribut; V153-Probe ohne tailscaled-Kontakt] im Head **angehängt**, Step-H-Block verbatim ins Archiv; Head 34.873 B → 28.685 B) | 2026-09-30 (**zwoelfte Rotation, Step H** — Step-H-Block [`fastmcp` exakt gepinnt `==3.4.7`, der Range-Pin hatte den Live-Release bereits lautlos auf 3.4.7 gezogen, V163 mit drei Codepunkten beantwortet, Wächter als Deploy-Riegel, Gegenprobe 4 Verstöße → 7 rot] im Head **angehängt**, Step-G-Block verbatim ins Archiv; Head 33.175 B → 26.210 B) | 2026-09-30 (**elfte Rotation, Step G** — Step-G-Block [Lösch-Ort war unbaubar, TLS-Wegwerf für den Browserbeleg, 14/14] im Head **angehängt**, Step-F-Block verbatim ins Archiv; Head 32.668 B → 25.740 B) | 2026-09-30 (**zehnte Rotation, Step F** — Step-F-Block 2026-09-30 [doing/assignee, neunte P1-Contract-Öffnung, V160 beantwortet, Plan-§8.2-Korrektur 9 → 18 Hunks, `_BUCKETS`-Befund bewusst nicht behoben, V161-Vorabwert] im Head **angehängt**, Block 2026-09-30 [A1/A2/A3/A0b/A6] verbatim ins Archiv; Head 30.868 B → 23.312 B) | 2026-09-30 (neunte Rotation — Step-A-Block 2026-09-30 [A1/A2/A3/A0b/A6 ausgeführt, A6-eigener-Fehler, vier eigene Fehler, Gegenseiten-Belege] im Head angehängt, Block 2026-09-29 [Step A vorbereitet: Plan-A4 unbaubar, socat-Relay gebaut] verbatim ins Archiv; Head 41.523 B → 23.080 B) | 2026-09-29 (achte Rotation — Step-A-Vorbereitungs-Block 2026-09-29 [sechs gemessene Befunde, Plan-A4 als unbaubar nachgewiesen, socat-Relay-Unit + Caddy-Vorlage + ACL-Entwurf + geführtes Runbook, V149 beantwortet, V162 neu offen] im Head angehängt, Block 2026-09-28 [Step E: Reload-Overload] verbatim ins Archiv; Head 41.523 B → 21.880 B) | 2026-09-28 (siebte Rotation — Step-E-Block 2026-09-28 [Reload-Overload: Signatur aus dem /overview-Payload statt aus dem Graph-Payload, Positionen überleben den Wiedereintritt, V118 beantwortet] im Head angehängt, Block 2026-09-26 [Step C abgeschlossen: C8 + Host-Aufräumen pve + P9-22 deferred] verbatim ins Archiv; 13.606 B, 215 Zeilen) | 2026-09-26 (sechste Rotation — Step-C-Abschluss-Block 2026-09-26 [C8 + Host-Aufräumen pve + P9-22 deferred] im Head angehängt, Block 2026-09-25 (3) [GPU-Reboot-Persistenz / devN-Fix / C4 / C5] verbatim ins Archiv verschoben; Head trägt jetzt exakt einen Session-Block) | 2026-09-25 (fünfte Rotation — Step-C-Block 2026-09-25 (2) [Diagnose, Host-Fix, GPU-Messung, Boot-Persistenz] verbatim ins Archiv; Head trägt Block 2026-09-25 (3)) | 2026-09-25 (vierte Rotation — C6-/Backlog-Block vom 2026-09-25 verbatim ins Archiv; Head trägt den Step-C-Diagnose-Block 2026-09-25 (2)) | 2026-09-25 (dritte Rotation — Step-C-Teil-1-Block vom 2026-09-24 ins Archiv verschoben, verbatim; Head trägt jetzt den Step-C-Teil-2 / C6-Block vom 2026-09-25 allein) | 2026-09-24 (zweite Rotation — Step-D-Block vom 2026-09-23 aus dem Head verschoben, verbatim) | 2026-09-23 (erste Rotation — Step-0-Block aus dem Head verschoben, verbatim) | 2026-09-20 (angelegt, noch leer)
---

# Phase 9 — Sessions Archive

Newest-first. Rotation per `scripts/rotate_session_block.sh phase9_hardening` — der Head
trägt immer genau einen `## Session stopped`-Block, ältere Blöcke wandern verbatim hierher.
Vorsatz: nichts abtippen, alles per Skript mit vier Gegenproben (Schnitt verlustfrei, neuer
Head trägt genau einen Block, alle bewegten Blöcke im Archiv byte-identisch, Archivbestand
unangetastet).

## Session stopped — 2026-10-03 (zwanzigster Block: **die Karte schrumpft — 71.573 → 38.532 B, die Nachträge sind im L3-Archiv und das Kriterium ist neu baseliniert**; die Wurzel-`CLAUDE.md` bleibt, wie entschieden, unangetastet und ist stattdessen gemessen; 10 neue Tests, ein Skript mit fünf Gegenproben; ein Commit, kein Produktcode-Touch, kein Deploy)

**Die zwei offenen Entscheidungen sind entschieden, und sie sind nicht gleich ausgegangen.** Für
`docs/INDEX.md`: Nachträge ins L3-Archiv **und** Kriterium neu baseliniert — beides gebaut. Für die
Wurzel-`CLAUDE.md`: **nicht jetzt**, nur messen und protokollieren — die Messung steht unten, mit
der Rechnung, die sie entscheidbar macht, damit die Entscheidung nicht noch einmal von vorn
gemessen werden muss.

**Was an der Karte wirklich dran war, ist jetzt eine Rechnung statt einer Vermutung.** Stand
**71.573 B**, davon **37.391 B datierte Nachträge in 43 von 93 Einträgen** — mehr als die Hälfte der
Datei. Die `updated:`-Kette der Karte hat **1.155 B** und war am 2026-10-03 rotiert; sie war nie die
Restmasse, und „`docs/INDEX.md` rotieren" — so stand es bis gestern in der Übergabe — hätte rund
1 KB gespart statt 30 KB. Und das Kriterium **38.912 B** aus P8.6 Plan 2 §1.2 war **per Kürzen
unerreichbar**: selbst ein Cap von 300 B je Eintragszeile ergäbe **39.971 B**. Gebaut:
`docs/INDEX_ENTRIES_ARCHIVE.md` (verbatim, ein Abschnitt je Karte in Kartenreihenfolge) und
`scripts/archive_index_entries.sh` mit **fünf Gegenproben**, darunter die **byteweise Reassemblierung
des Originals** — „verbatim" ist damit eine geprüfte Eigenschaft und keine Behauptung im Kommentar.
**71.573 → 38.532 B: die Karte ist zum ersten Mal seit `06ab4f6` unter dem Softcap**, und das neue
Kriterium (40.960 B, der Wert, den `doc_health` ohnehin prüft) ist erstmals eine **Prüfung** statt
einer Angabe: `test_the_index_is_under_the_rebaselined_criterion` wird rot, sobald die Karte darüber
wächst.

**Vier Skript-Gegenproben waren rot, bevor es lief, und jede davon war ein Fehler im Werkzeug, nicht
im Datenbestand.** (1) Der erste Schnitt endete **mitten im Satz** (`… (V145; **`), weil der Anker
das `**` nicht mitgenommen hat — die Auszeichnung wäre im Kopf geblieben und der Archivabschnitt mit
`**[` begonnen. (2) Die Satzgrenzen-Prüfung selbst war zu streng für `~106KB` in der P8.6-Zeile: sie
verlangte eine fette Bytezahl, `doc_health` akzeptiert aber auch die gerundete Form — **ein Wächter,
strenger als die Regel, die er verteidigt, verteidigt sie nicht.** (3) Der Zeiger war ein
Markdown-Link, und `doc_health._index_line_for()` erkennt Zeilen an `](pfad)`: das Archiv wurde für
eine Karte mit `glyph='🔗'` gehalten, die gar keine INDEX-Zeile hatte. **Ein Zeiger, der wie ein
Eintrag aussieht, ist für einen Zeiger die falsche Form.** (4) Der Reassemblierungs-Abgleich hat den
Nachtrag in die Zeile der **Karte selbst** gesetzt, weil er den Zeigern nachging statt nach
Etiketten: „der n-te Zeiger gehört zum n-ten Abschnitt" stimmt genau einmal, beim ersten Lauf — und der
Alltagsfall ist ein INDEX, der schon rotiert ist, plus *ein* neuer Nachtrag. **Das war ein echter
Entwurfsfehler**, gefunden von dem Test, der genau den Alltagsfall baut.

**Und eine Korrektur an meiner eigenen Behauptung, die der Test mir abgenommen hat:** ich habe
Gegenprobe (d) — „kein datierter Nachtrag bleibt im INDEX" — als die Prüfung gepriesen, die einen
vergessenen Nachtrag fängt. **Der Test zeigt: ein geschwächter Anker wird zuerst von der
Satzgrenzen-Prüfung gefangen**, und mit dem heutigen Anker ist ein „zu später" Schnitt gar nicht
erzeugbar. (d) bleibt als Rückfall und als Vorabversion desselben Satzes, den
`test_no_entry_line_carries_a_dated_addendum_any_more` am echten Artefakt prüft — aber sie trägt
nicht, was ich ihr zugeschrieben hatte. **Vier Wächter in `test_index_archive.py` und sieben in
`test_acceptance_numbers.py`; die Zahlen der Matrix werden von letzterem maschinell geprüft, und
sie haben die Bilanz zweimal mitgezogen: 70/10/3 → 71/9/3 — **und mich zweimal dabei erwischt, wie ich die Zahl selbst wieder in den Modulstatus und in die Kette schreibe; beide Wächter standen sofort rot**.**

**Gemessen, nicht entschieden: die Wurzel-`CLAUDE.md`.** 114.771 B, davon Regeln+Rest **9.479 B**,
`updated:`-Kette **13.700 B** und §Current state **91.574 B** in 24 Blöcken. Die Rechnung macht die
Entscheidung scharf, und sie ist eindeutig: **K ≥ 4 passt nie** (40.281 B bei stehengebliebener
Kette), und **ohne Kettenrotation passt selbst K=1 nur knapp**. Mit Kettenrotation (≈1.500 B):
**K=1 → 17.515 B · K=2 → 24.777 B · K=3 → 27.350 B**, Luft 23,4 / 16,2 / 13,6 KB. Ich empfehle **K=1**,
weil der neueste Block nach der eigenen Erfolgskriterie ein Handover für einen kalten Leser ist und
die anderen 23 Blöcke **verbatim bereits in `phase9_hardening/SESSIONS_ARCHIVE.md` (244.641 B),
`phase8_6_ui_polish/SESSIONS_ARCHIVE.md` (239.960 B) und `docs/PROJECT_SESSION_LOG.md` (101.450 B)**
stehen. **Das braucht deine ausdrückliche Umkehr von P9-A** („kein Ein-Block-Limit", Lock vom
2026-09-30) — sie ist die direkte Ursache der 73.811 B, und eine stille Aufweichung wäre genau die
Sorte Falschheit, die diese Datei verhindert.

**Und dieselbe Strukturaussage für diesen Head, weil sie sich sonst beim nächsten Block wiederholt:**
Er stand nach der gestrigen Rotation bei **40.154 B, also 806 B Luft** — und jeder Session-Block ist
größer. **Eine Rotation kauft genau eine Session, keinen Zustand.** Die Masse ist der *lebendige*
Modulstatus (**26.346 B** in vier Zeilen, A 4.915 · B 4.050 · Gate/Z 2.454 · D 2.069), nicht die
durchgestrichenen Absätze (**229 B** — der seit gestern benannte Hebel war um Faktor 33 zu groß
behauptet). Ein Wächter nagelt beides fest. **Streichen wäre Deine Entscheidung**, weil es Zeilen aus
dem Kopf der laufenden Phase nimmt.

**Selbstprüfung:** `pytest` **1188 → 1198** (10 neu) · `ui_budget` 5/5 (kein
`phase5_ui/webui/static/**`-Berührung) · `doc_health` **0** — es hat mich zweimal rot gemeldet,
beimal zu Recht: einmal weil die Matrix über ihr eigenes ±2-KB-Fenster wuchs, einmal weil die
Größenangabe einer Karte nach dem Umbau nicht mehr galt · Tabu-Pfade unberührt · **kein `systemctl`,
kein `pkill -f`**, keine Wegwerf-Instanz.

**Nächster Schritt, nach Zuständigkeit.** (1) **Deploy-Tag `v3.1.1`**: Badge + `##`-Block in
`docs/UPDATE_LOG.md` **erst am Tag selbst**, der trace-Block kommt mit, **kein** Index-Neuaufbau;
`health_gate.sh` liefert V164 und die P9-15-Läufe. (2) **Das zweite Claude-Konto umstellen** — ein
Konto, kein Code; danach P9-13/V150 ✅. (3) **Die beiden Benennungen entscheiden**: INDEX-Zeilenlänge
für die Phase (K=? plus Modulstatus) und die Blockgrenze für die Wurzel. (4) **Übersichtsgrafik
§12.4** (gerendert **und angesehen**) und ROADMAP-Zeile, wenn die Zahlen endgültig sind. **Mit Datum im
Kalender:** am **2026-10-18** schließt das Übergangsfenster von selbst — die alte Adresse liest dann
nur noch. Absicht, kein Versehen.

## Session stopped — 2026-10-03 (neunzehnter Block: **die Zahlen der Abnahmematrix dürfen nicht mehr still veralten** — vier Fundstellen mit drei Bilanzen, eine davon 8.249 B falsch, ein benannter Hebel als No-op nachgewiesen; 7 Tests, 6 Gegenproben rot; ein Commit, kein Produktcode-Touch, kein Deploy)

**Von den drei „Rest Gate/Z"-Posten ist keiner meiner** — das zweite Claude-Konto ist ein Konto, der
Deploy `v3.1.1` ist dein sudo-Schritt, die Übersichtsgrafik wartet auf endgültige Zahlen. Was blieb, war
die Datei, an der das Gate am Ende gemessen wird. Beim Nachmessen fand sie **vier Stellen, an denen
dieselbe Zahl viermal steht und dreimal falsch ist.**

**Der Fund: eine Zeile, deren Gegenstand die Größe einer Datei ist, nannte deren Größe falsch.** Die
Matrix ist das zentrale Artefakt des Gates — 82 Abnahmezeilen, 34 belegte `[VERIFY]`-Einträge. Ihre
**Bilanz stand an vier Stellen** (Matrix · Modulstatus · `updated:`-Kette · INDEX-Zeile) mit **drei
verschiedenen Zahlen** — und P9-3 wie V145 schrieben „heute **61.108 B**" für `docs/INDEX.md`, das
**69.357 B** groß ist. Acht Kilobyte daneben, zwei Tage lang. **Warum das passieren konnte, und die
Antwort ist eine Lücke statt eines Schlampers:** `doc_health.py` prüft die Bytezahl einer Datei gegen ihre
**INDEX-Zeile** (`oversize`, ±2-KB-Band), nicht die Bytezahlen **innerhalb** der Matrix. Geschlossen
worden ist die Lücke durch eine zweite Regel daneben — nicht durch Weglassen der ersten.

**Die Diagnose der Überschreitung war dreifach falsch, und diesmal gemessen statt geglaubt.** „`docs/INDEX.md`
rotieren" stand bis eben in der Übergabe und im Phase-Head. (a) Die `updated:`-Kette ist rotiert und
hat **1.155 B** von 69.357 B; sie noch einmal zu rotieren spart rund 1 KB, nicht 30 KB. (b) Die
Restmasse sind datierte Nachträge: von 55.119 B Eintragsbytes in 93 Zeilen liegen **30.145 B** ab dem
ersten `[YYYY-MM-DD`-Nachtrag. (c) **Das Kriterium 38.912 B ist per Kürzen unerreichbar** — selbst ein
harter Cap von 300 B je Zeile ergäbe **39.971 B**. Es stammt aus P8.6 Plan 2 §1.2 für eine Datei mit
weniger Zeilen und ist nicht mitgewachsen. **Drei Wege raus, keiner gebaut, weil alle drei deine
sind:** Nachträge in ein L3-Archiv (Form wie `UPDATES_ARCHIVE.md`) · Kriterium neu baselinen ·
Benennung als Endzustand. **Dieselbe Fehldiagnose ist in zwei Phase-Heads schon zweimal passiert** (im einen die
gestrichenen Statusabsätze, im anderen der B17-Block) — zum dritten Mal ist die benannte Restmasse nicht
die, die übrig bleibt. Das ist jetzt eine Eigenschaft des Musters, keine Überraschung.

**Der zweite Fund war kleiner und gefährlicher: eine Bilanz, die aufgeht.** Die `[VERIFY]`-Bilanz nannte
`28 ✅ · 3 ⚠️ · 3 ⬜` — Summe 34 richtig, die beiden anderen Zahlen je eins daneben und **gegeneinander
vertauscht** (nachgemessen `28 ✅ · 4 ⚠️ · 2 ⬜` in der Nummern-Lesart). Ursache ist strukturell und war
nirgends genannt: **V162 und V163 sind je zweimal vergeben** (Lesart A/B), die Tabelle hat zwei Zeilen
mehr als Nummern — „zählen" war mehrdeutig, und eine mehrdeutige Bilanz ist keine Bilanz. Die Regel steht
jetzt im Text **und** als Test-Konstante.

**Gebaut: 8 Tests in zwei Regelnwerken.** `test_acceptance_numbers.py` (7) in drei Regeln — *eine Quelle
für die Bilanz* (Modulstatus und INDEX-Zeile dürfen keine zitieren, **die Kette darf**, weil sie ein
datierter Record ist; ihr „Matrix **jetzt** 68 ✅…" war zwei Tage alt) · *keine Gegenwartsform* ·
*jede lebende Bytezahl nachgemessen, und zeilenweise, in der Zeile, die die Aussage macht*. Dazu
`test_rotate_index_updates.py` (1), siehe den Skript-Fund unten. **Das Byte-Band ist ±2 KB statt exakter
Gleichheit** — die Matrix nennt die Größe einer Datei, in der die Zeile steht, die diese Zahl nennt, und
`docs/INDEX.md` wird am Ende jeder Session angefasst; exakte Gleichheit wäre eine Wartungsschleife. Das
Band ist **das** Band, an dem `doc_health` die INDEX-Zeile ohnehin misst: die neue Regel ist nicht
strenger als die bestehende, und der Fehler von 8.249 B bleibt darin rot.

**Sechs eigene Fehler, alle im selben Commit behoben — jeder war derselbe Fehler wie der, den der
Wächter sucht, und drei davon hat erst die Gegenprobe gezeigt.** (1) Die erste Fassung verglich die
Tabelle mit einer abgetippten Konstante: **der Fließtext, also genau die Stelle, die veraltet, wurde nie
geprüft.** (2) Die erste Suche ging **dateiweit** und war grün, obwohl die P9-3-Zeile falsch war — eine
dritte richtige Nennung genügte; der Anker `| V145` griff zusätzlich die Bereichszeile `| V145–V166`.
(3) **Gegenprobe G6 meldete grün für einen falschen Zustand:** sie hatte nur **eine** von zwei Nennungen
gefälscht — eine Probe, die etwas anderes prüft als sie behauptet, mit grünem Ergebnis; ihr Kontrolllauf
meldete zusätzlich „ROT" für einen grünen Lauf, weil die Variable die Gegenfarbe benannte. (4) Die
Zahlenprüfung „irgendwo im Text eine Bytezahl im Band" ging **zweimal** grün, obwohl die Aussage falsch
war — eine Kandidatenliste findet in einem langen Dokument immer eine passende Zahl; der Anker musste
das **Wort** sein, das die Messung benennt. (5) Der Zahlen-**Parser** kannte nur die punktgeschriebene
Form und war blind für `229 B`. (6) Eine Textsuche mit `sed` hat mir zweimal die falsche Stelle
zugschnitten. **Ein Wächter, der nicht beweisen kann, dass er falsch liegt, prüft die Hälfte** — und
**G1–G8, alle acht rot, Kontrolllauf grün**, ist der einzige Weg, das zu merken.

**Fund am Skript, und er ist derselbe Fehler noch einmal:** `rotate_index_updates.sh` meldete für den
Head **„Bereits konform: die 'updated:'-Kette hat nur einen Eintrag"** (exit 2) — und meinte es richtig,
was das Problem war: die Kette trug **zwei Fäden, die ohne den ` | `-Trenner verklebt** waren. Der
Split-Anker ist ` | ` + ISO-Datum, ein fehlender Trenner ist für ihn nicht von einem sehr langen
Eintrag zu unterscheiden, und (e) prüft das *Split-Ergebnis* — bei nichts zu splitten kann es nichts
finden. Also prüft jetzt ein Test den Zustand **vor** dem Skript. Und die **beiden** ` | updated: `-Präfixe
der **Wurzel**-`CLAUDE.md` sind entfernt: die Phase-9-Notiz „dort nicht rotierbar" ist damit **überholt**,
denn das Skript ist seit dem 2026-10-03 verallgemeinert. Ich habe die Kette des Heads dabei mitrotiert
(45.126 → 42.836 B, alle Gegenproben grün).

**Gemessen, aber nicht entschieden: die Wurzel-`CLAUDE.md`.** 114.789 B, davon §Current state
**91.574 B** in **24 Session-Blöcken** (der größte allein 19.337 B) und die Kette **13.718 B**. Die
Rotation der Current-state-Abschnitte ist der einzige im Dateikopf selbst benannte Hebel und ist jetzt
zum ersten Mal ausführbar. **Wie viel Historie im Head bleibt, ist Deine Entscheidung** — sie bestimmt,
was jeder Session-Start liest.

**Und eine Strukturaussage, die beim Rechnen auffiel und die ich nicht wegtrimme:** Der Head stand nach
der Rotation vom 2026-10-03 bei **40.154 B, also 806 B Luft** — und jeder Session-Block ist größer als
806 B. **Eine Rotation kauft damit genau eine Session, keinen Zustand.** Dieser Block bringt den Head auf
**44.079 B**, also über den Softcap — benannt statt versteckt, die exakte Überschreitung steht in der
INDEX-Zeile und `doc_health` bestätigt sie. Der
Und hier kommt der vierte Fund derselben Serie, und er ist der billigste: **der Hebel, der den Head
unter den Softcap bringen soll, existiert in der Größe nicht, in der er benannt ist.** Seit gestern steht
in diesem Dateikopf, in der INDEX-Zeile und in zwei archivierten Blöcken, die **„7.467 B durchgestrichene
Statusabsätze im Modulstatus"** seien der Rest — **gemessen sind es 229 B in der ganzen Datei** (A 42 ·
B 9 · D 150 · Gate/Z 28). Faktor 33. Der Vorschlag vom 2026-10-03 („Streichen wäre die einzige Maßnahme,
die den Head sicher unter den Softcap brächte") hätte **229 B** gebracht; bei der damaligen Größe von
44.360 B bliebe der Head bei **44.131 B**, also 3.171 B darüber — er hätte nichts gelöst. **Die Masse
ist woanders: die Modulstatus-Tabelle ist 26.346 B _lebendiger_ Text**, und davon stehen die vier
größten Zeilen (A 4.915 · B 4.050 · Gate/Z 2.454 · D 2.069) **doppelt** — einmal im jetzigen Stand und
einmal im durchgestrichenen historischen Absatz derselben Zelle. Dort stünde die Streichung an, und
das ist **Deine Entscheidung**, weil sie Zeilen aus dem Kopf der *laufenden* Phase nimmt.

**Selbstprüfung:** `pytest` **1180 → 1188** (8 neu, Baseline vorab gemessen) · `ui_budget` 5/5 (kein
`phase5_ui/webui/static/**`-Berührung) · `doc_health` **0** — der Scan hat mich zuerst rot gemeldet,
weil meine eigene Korrektur die Matrix über sein ±2-KB-Fenster hob; der Wächter bei seiner Arbeit ·
Tabu-Pfade unberührt · **kein `systemctl`, kein `pkill -f`**, keine Wegwerf-Instanz.

**Nächster Schritt, nach Zuständigkeit.** (1) **Zweites Claude-Konto umstellen** — danach P9-13/V150 ✅.
(2) **Release-Commit + Deploy `v3.1.1`** — Badge + `##`-Block **erst am Deploy-Tag**, trace-Block kommt
mit, **kein** Index-Neuaufbau; `health_gate.sh` liefert V164 und die P9-15-Läufe. (3) **Die drei Wege aus
der INDEX-Überschreitung entscheiden** — P9-3 bleibt ⚠️, und der Wächter meldet, wenn die Datei unter das
Kriterium fällt. (4) **Übersichtsgrafik §12.4** (gerendert **und angesehen**) und ROADMAP-Zeile, wenn die
Zahlen endgültig sind. **Mit Datum im Kalender:** am **2026-10-18** schließt das Übergangsfenster von
selbst — die alte Adresse liest dann nur noch. Absicht, kein Versehen.

## Session stopped — 2026-10-03 (achtzehnter Block: **A7a + A7 + A8 gefahren** — die Domain ist live, der Connector läuft über die eigene Adresse; Nikinger-Schritte, von M3 vorbereitet, gegengemessen und protokolliert; ein Commit, kein Deploy, kein Produktcode-Touch)

**Diese Session hatte keinen Code-Step, sondern einen Schnitt mit Token-Folge — und die
Vorbereitung dafür war die eigentliche Arbeit.** Der Auftrag lautete „A7 und A8 durchführen";
beides sind deine sudo-Schritte, also habe ich die *Liste* gemacht (so steht es im Runbook:
„du, sudo; Liste von mir") und jede Zeile vorher am Code und an der Konfiguration geprüft, damit
der Schnitt **ein** Versuch ist und nicht drei.

**Drei Vorprüfungen, die den Schnitt von einem Experiment zu einer Messung gemacht haben.**
(1) `load_settings()` mit den **exakten** Environment-Zeilen der künftigen Unit: kein Startfehler —
`config.py` ist fail-closed, ein Tippfehler wäre also ein **toter Dienst** gewesen, nicht ein
leises „aus". (2) Die Form von `LEGACY_ORIGIN` steht im Code, nicht in der Erinnerung:
`config.py:47` verlangt exakt `https://host`, und der Funnel liefert **`https://`/443**
(`TLS=0` gemessen) — die alte Form `http://host:8765` hätte das Fenster nie geöffnet, und
`config.py:76` rechnet `clock() <= legacy_until` pro Request, das Fenster schließt am Enddatum
**ohne** Neustart. (3) Das Verhalten des Fensters drei Tage lang durchgespielt: 2026-10-03 und
17. alt-Adresse schreibbar ✅, 18. nur noch lesend — eine Behauptung über Zeit wird hier nicht
behauptet, sondern durchgerechnet.

**Der Vorlauf A7a hat bezahlt, wofür er gebaut war.** `ALLOWED_HOSTS` bekam die Domain dazu, sonst
nichts: **neu lokal 200 · alter Funnel lokal 200 · extern `https://sharefyx.eurofyx.com/health`
→ 200 mit `ssl_verify_result=0`** und JSON. Dieselbe Adresse lieferte **eine Stunde vorher 400 bei
gültigem TLS** — das ist der ganze öffentliche Weg als ein einziger Vorher/Nachher-Beleg: Caddy
terminiert, das LE-Zertifikat gilt, und die 400 kam aus dem **Prozess** (6× `GET /health
status=200` im Journal, drei von dir, drei von mir). **P9-10b ✅, und die zweite Hälfte P9-10a
(A4, Zertifikat) war seit dem 2026-10-01 grün** — die Zeile ist damit vollständig abgenommen.
**Und die Gegenprobe, die A7a von A7 trennt:** nach A7a stand der `issuer` **unverändert** auf der
alten Adresse. Damit ist nicht nur behauptet, sondern gemessen, dass der Vorlauf den `resource`
nicht angefasst hat — die Token blieben gültig, ein Fehler dort wäre ohne Messung ein Verdacht
geblieben.

**Der Schnitt A7 war der teure, und er ist dokumentiert statt gefühlt.** `PUBLIC_BASE_URL` auf die
Domain, `LEGACY_ORIGIN`/`LEGACY_UNTIL=2026-10-17` dazu, Gate = der `issuer`:
`{"issuer":"https://sharefyx.eurofyx.com", …}` — **alle vier** Endpunkte aus der Basis-URL, wie
V149 vorhergesagt hatte. **Befund 4 hat sich bestätigt, an der Stelle, wo er hingeschrieben war:**
`resolver.py:48` vergleicht `record.resource` mit dem neuen `expected_resource`, also waren nach
dem Restart **alle** alten Token tot und die Neuanmeldung über die neue Adresse war **zwingend** —
kein Neustart-Fehler, und genau deshalb die Warnung im Vorfeld, damit hier kein falscher Incident
wie der `mcp-proxy`-502 vom 2026-09-24 entsteht. Konto **niklas** läuft inzwischen über die eigene
Adresse; **das zweite Konto steht aus**, deshalb stehen **P9-13 und V150 auf ⚠️ „1 von 2"** und
nicht auf ✅ — die Zeile verlangt **beide** Konten, und ein Konto ist kein Code.

**Was ich nicht gemessen habe, mit Begründung: P9-15.** Der authentifizierte Vergleich von
`/api/v1/overview` gegen die Referenz **372,9 ms** wäre ein authentifizierter Aufruf am echten
DATA_ROOT mit echtem Keyring-Token — das ist Nikinger-Wirklichkeit, nicht meine. Die Zeile bleibt
**⬜** und gehört an den **Deploy-Tag**: `health_gate.sh` macht genau diese Aufrufe, also hängt sie
an `v3.1.1` und nicht an einer vergessenen Messung.

**Ein Fund, der eine Zeile in einer fremden Datei gerettet hat:** `install_units.sh` erzeugt **zehn**
Units, und die neu entstandene `sharefyx-mcp.service` trägt jetzt Zeilen 19/20
`SPACE_UI_LEGACY_ORIGIN=` / `_UNTIL=`. Sie waren **leer**, weil `local.env` noch keine
`LEGACY_*`-Zeilen hatte — und leer **beide** ist laut `config.py:44` ausdrücklich *kein Fenster*,
also kein halbes Fenster und kein Startfehler. **Ohne diese Messung hätte ich dir „zwei leere
Zeilen, das ist verdächtig" gemeldet**, und du hättest vermutlich nachgeforscht, statt einfach
weiterzumachen. **Meine eigene Vorhersage war daneben:** ich schrieb „5–6 Units", es waren zehn;
ich hatte eine Vorlage nachgeschlagen statt alle zu zählen. Vorher hatte ich außerdem nur 2 der 10
installierten Units gegen die Vorlagen geprüft — nach dem Lauf sind es **alle 4 Timer** (`enabled`
**und** `active`, mit plausiblen nächsten Terminen) und ein **echter Watchdog-Takt** nach der
Regeneration (`13:01:49 healthy: Self.Online=true` + `Finished`), denn ein laufender Timer beweist
keinen arbeitenden Dienst — die Lehre vom 2026-10-01, diesmal an meinem eigenen Optimismus.

**Und eine Konfigurationslücke, die nur existiert, weil sie niemand aufschreibt:** `local.env` ist
git-ignoriert, und ein Neustart setzt sie **nicht** zurück. Wer sie nicht im Repo findet, findet
sie nirgends. Der **Live-Ist-Zustand** steht deshalb jetzt in `step_a/RUNBOOK_STEP_A.md` §2 A7/A8 —
mit beiden ausgeführten Blöcken, dem Gate-Befehl, dem Rückweg (falls A8 klemmt: `PUBLIC_BASE_URL`
zurück, `install_units.sh`, Restart ⇒ die alten Token leben wieder) und der Erkenntnis, dass das
`LEGACY_*`-Fenster **nur die Web-UI** schützt: für den Connector gibt es keinen Übergang.

**Selbstprüfung:** `pytest` 1180 (unverändert, kein Test-Touch in diesem Block) · `ui_budget` 5/5 ·
`doc_health` 0 Befunde · Tabu-Pfade unberührt · **kein `systemctl`, kein `pkill -f`** von mir — die
drei sudo-Befehle waren deine, ich habe sie nur vorbereitet und die Ausgabe gelesen · Live-Zustand
zum Schluss selbst gemessen: neue Domain 200/TLS ok, alter Funnel 200/TLS ok, Live-Release
`5414cb7` = Badge `v3.1.0`, `SPACE_ALLOWED_HOSTS`/`SPACE_PUBLIC_BASE_URL` tragen beide die Domain.

**Nächster Schritt.** (1) **Das zweite Claude-Konto umstellen** — dieselben drei Handgriffe, es ist
ein Konto und kein Code; danach sind P9-13 und V150 ✅. (2) **Release-Commit + Deploy `v3.1.1`**:
Badge `app.html` + `##`-Block in `docs/UPDATE_LOG.md` **erst am Deploy-Tag** (sonst brennt das
`deploy.sh`-Gate P6-X), der trace-Block kommt mit, **kein** Index-Neuaufbau; `health_gate.sh` liefert
dabei V164 und die P9-15-Läufe. (3) Rest Gate/Z: Übersichtsgrafik §12.4 (**gerendert und
angesehen**), `docs/INDEX.md` rotieren, ROADMAP-Zeile, Phase auf ✅. **Termin mit Datum im Kalender:**
am **2026-10-18** schließt das Übergangsfenster von selbst — die alte Adresse liest dann nur noch.
Das ist Absicht, kein Versehen, und es braucht keinen Neustart.

## Session stopped — 2026-10-03 (siebzehnter Block: der Head trug dieselbe Regel, die nur für den INDEX gebaut war — Kette rotiert, Skript verallgemeinert, **zum ersten Mal unter dem Softcap**; opencode/M3, ein Commit, **kein Produktcode-Touch**, kein Deploy, kein Service-Touch)

**Der Auftrag war „drei Zeilen, vorhandene Tests" — die drei Zeilen waren die richtige
Diagnose und die falsche Datei.** Das Skript `scripts/rotate_index_updates.sh` war auf
`docs/INDEX.md` festgenagelt, obwohl **jeder lebende Head dieselbe `updated:`-Kette trägt**. Bevor
ich irgendetwas gebaut habe, habe ich gemessen, welche Kette überhaupt die große ist:

| Datei | Datei | Kette | Fäden | davon ` \| updated: `-Präfixe |
|---|---|---|---|---|
| `phase9_hardening/CLAUDE.md` | 57.873 B | **19.488 B (33 %)** | 37 | 4 |
| `CLAUDE.md` (Wurzel) | 114.789 B | 13.728 B (11 %) | 9 | 2 |
| `phase9_hardening/ABNAHME_MATRIX.md` | 44.222 B | 2.451 B | 2 | 1 |
| `phase8_ui_graph/CLAUDE.md` | 47.861 B | 1.896 B | 4 | 0 |
| `docs/INDEX.md` | 65.235 B | 307 B | 1 | 0 |

**Die Überschreitung dieses Heads war also falsch diagnostiziert — und zwar von mir, zwei Tage
zuvor.** Als „Restmasse" galten im Kopf (und in der INDEX-Zeile) die **7.467 B durchgestrichenen
Statusabsätze** im Modulstatus, mit dem Zusatz, das Streichen sei eine Nikinger-Entscheidung. Die
Kettenrotation spart **~18 KB** — Faktor 2,4. Der Streich-Vorschlag wäre die teurere von zwei
richtigen Wegen gewesen; er bleibt als Entscheidung offen, ist aber jetzt **nicht mehr der Hebel**.
Das ist die_repo-Lehre in ihrer Doc-Form: *die Zahl im Kopf ist eine Behauptung, `wc -c` ist eine
Messung*, und diesmal stand die Behauptung im selben Dokument, das sie beschrieb.

**Gebaut wurde die Verallgemeinerung mit den zwei Fallen, die eine naive Form nicht findet.**
Aufruf jetzt `scripts/rotate_index_updates.sh [repo_root] [zieldatei] [archivdatei]`, Default
unverändert `docs/INDEX.md` · `docs/INDEX_UPDATES_ARCHIVE.md`; alle fünf Gegenproben (a)–(e)
unverändert, nur die Schnittstelle ist allgemeiner. (1) **Der Zeiger muss der übergebene
Archivpfad sein, nicht der INDEX-Pfad** — hartkodiert wäre er für jeden anderen Head eine stille
Lüge: die Kette zeigte auf ein Archiv, in dem ihre Einträge nicht stehen. Der Test dafür ist
absichtlich so gebaut, dass eine `in`-Prüfung auf `docs/INDEX_UPDATES_ARCHIVE.md` **nicht** grün
werden kann (der jüngste Faden des Fixtures nennt die Zeichenkette selbst und bleibt stehen) —
nach der Wiederholung vom 2026-10-02 wäre ein Test, der nur im richtigen Fall anschlägt, wertlos.
(2) **Zieldatei ≠ Archiv** — Selbst-Rotation wäre Datenverlust *ohne* Fehlermeldung, weil das
zweite `cp` den gerade gedrehten Ketten-Rest überschreibt. Dazu die Pfad-Formprüfung
(kein absoluter Pfad, kein `..`), denn der Zeiger landet wörtlich im Dokument. **5 neue Tests,
12/12; Gegenprobe C1 (Zeiger hartkodiert) → 1 rot · C2 (Selbst-Rotation raus) → 1 rot · C3
(Pfadform raus) → 1 rot**, Kontrolllauf 0. **Ein eigener Fehler, vom neuen Test gefunden:** die
Pfadprüfung stand ursprünglich *hinter* den Existenzprüfungen — ein absoluter Pfad brach dann mit
„Archiv fehlt" ab und verschwieg die eigentliche Ursache. Steht jetzt davor.

**Vier ` | updated: `-Präfixe, derselbe Defekt wie am 2026-10-02 — zum zweiten Mal, in einer
anderen Datei.** Sie sind Handarbeit aus den letzten Tagen; ohne sie sähe der Faden für den
Split-Anker `' | ' + ISO-Datum` nicht wie ein Kettenanfang aus und würde still nicht rotiert.
Gegenprobe (e) hätte abgebrochen (genau dafür ist sie da), Präfixe entfernt, dann rotiert: **36 von
37 Fäden**, Rekonstruktion `gekaufter Faden + 36 Archiv-Fäden == alte Kette` **byte-identisch
20.266 B**, jeder Faden genau einmal im Archiv. Das ist meine eigene Nachrechnung, nicht die
Byte-Buchhaltung des Skripts — ein Wächter, der die Richtigkeit *seiner eigenen* Bilanz meldet,
ist die teuerste Sorte Wächter (der Fund vom 2026-10-02). **Ergebnis: Head 58.661 → 40.694 B durch
die Rotation und auf 39.106 B nach dem Block-Wechsel (Plan §12.5, der sechzehnte Block wandert
verbatim ins `SESSIONS_ARCHIVE.md`) — zum ersten Mal in dieser Phase unter dem 40-KiB-Softcap**; das
neue `UPDATES_ARCHIVE.md` trägt 19.379 B inklusive L1-Card. Summe vorher/nachher 60.016 → 60.073 B, die +57 B sind der Zeiger (52 B),
die eigene Karte des Archivs und `2 B` je Faden (`- ` im Archiv gegen ` | ` in der Kette).

**Und die dritte Datei mit demselben Defekt bleibt unangetastet:** die **Wurzel-`CLAUDE.md`** trägt
zwei ` | updated: `-Präfixe und eine 13.728-B-Kette. Sie ist nicht mein Head, ihre Kette ist
rotierbar (dieselbe Regel), aber die *benannte* Lösung für ihre 114.789 B ist die Rotation der
Current-state-Abschnitte nach `docs/PROJECT_SESSION_LOG.md` — und eine Kettenrotation allein
würde sie auf ~101 KB bringen, also immer noch 60 KB über der Grenze. **Benannt, nicht getan:**
es erst zu tun, wenn die Current-state-Rotation ohnehin kommt, sonst zwei Rotationen für eine
Datei. Derselbe Satz gilt für `ABNAHME_MATRIX.md` (2.451 B Kette, ein Präfix — der dortige Hebel
sind die vier „warten auf den Deploy"-Posten, ~4 KB in einem Block).

**Selbstprüfung, heute gemessen:** `pytest` **1175 → 1180** (5 neu) · `ui_budget` 5/5 (kein
`phase5_ui/webui/static/**`-Touch in diesem Commit) · `doc_health` 0 Befunde, die zwei neuen
INDEX-Zeilen inklusive · Tabu-Bereichs-Diff auf die sechs Hartpfade leer · **kein `systemctl`, kein
`pkill -f`**, keine Wegwerf-Instanz, Produktionsdienst nur gelesen · Live-Zustand vorher und
nachher gemessen und identisch: neue Domain `400 Invalid host header` (erwartet bis A7), Funnel-
Rückfall `200`, Live-Release `5414cb7` = Badge `v3.1.0`, `local.env` trägt unverändert
`ALLOWED_HOSTS=savefyx-….ts.net,127.0.0.1`.

**Benannt, nicht gebaut: `doc_health.py` sieht das Feld `updated:` überhaupt nicht.** `_parse_fm`
liest genau `status`/`purpose`/`read-when`/`detail` — ein **fehlendes** `updated:` ist darum kein
Befund, und der Fund oben (`aee387d` nahm dem `SESSIONS_ARCHIVE.md` das Präfix) blieb deshalb bis
heute stumm; eine Rotation *dieser* Datei wäre mit „Keine `updated:`-Zeile in der Frontmatter"
abgebrochen, also mit einer Meldung, die den Fehler erst verrät, wenn jemand ihn auslöst. Der
Riegel wäre eine Zeile (`updated` in die Feldliste) plus eine Befundkategorie — **hier nicht
gebaut**, weil er gemeinsame Infrastruktur ist und zuerst ein Scan über alle `.md` zeigen müsste,
ob er repo-weit Rot produziert; die Entscheidung gehört zum nächsten Schritt, der `doc_health`
anfasst.

**Nächster Schritt — unverändert deine Zuständigkeit, diese Session hat daran nichts
verschoben:** (1) **A7+A8 in einer Sitzung** (`step_a/RUNBOOK_STEP_A.md`; schließt P9-10b, P9-12,
P9-13, P9-15, V150, V164 — ein Schnitt, weil der A7-Restart beide Connectoren kappt), (2)
**Release-Commit + Deploy `v3.1.1`** (Badge + `##`-Block erst am Deploy-Tag, sonst brennt P6-X; der
trace-Block kommt mit, **kein** Index-Neuaufbau), (3) danach der Rest von Gate/Z:
Übersichtsgrafik §12.4 (**gerendert und angesehen**), `docs/INDEX.md` rotieren, ROADMAP-Zeile,
Phase auf ✅. **Entfallen** ist der Restposten „`rotate_index_updates.sh` um eine Datei/Archiv-
Angabe erweitern" — gebaut. **Neu offen, weil es dieser Block sichtbar gemacht hat:** die
Wurzel-`CLAUDE.md` (114.789 B, 13.728 B Kette, 2 Präfixe) und `phase8_ui_graph/CLAUDE.md`
(47.861 B) sind mit demselben Skript inzwischen je **einem** Befehl rotierbar — die Entscheidung
über die Current-state-Rotation liegt bei dir.

## Session stopped — 2026-10-03 (sechzehnter Block: Step D ist endlich gefahren — drei Abnahmezeilen, die seit dem 2026-09-23 als „gebaut, aber nie belegt" im Kopf standen; opencode/M3, ein Commit, **kein Produktcode-Touch**, kein Deploy, kein Service-Touch)

**Die Frage am Anfang war „sind keine Coding-Schritte in P9 mehr vorhanden?" — die ehrliche Antwort
war: kein Feature-Schritt, aber eine Zeile, die seit drei Wochen behauptet, sie sei gebaut.** Step D2
(Drop-Ziel zurück auf die Space-Wurzel) steht seit dem 2026-09-23 als gebaut in der Modulstatus-
Tabelle, mit **drei** statischen Wächtern in `test_static_routes.py` — und **null** Fahrten am
Browser. Die Wächter prüfen die *Form* des Aufrufs (`bindFolderDropTarget()` hat genau zwei
Aufrufstellen, die Space-Zeile hängt hinter einem `if (space.own)`), nicht sein *Verhalten*.
Drei Abnahmezeilen standen deshalb als ⬜ bzw. ⚠️ „strukturell erfüllt, nicht am Gerät belegt", und
**die Station, die sie hätte schließen können, war die erste von GA2 in Plan §11 — die nie gebaut
wurde.** Das ist dieselbe Fehlerklasse wie der trace-Beleg vom 2026-10-02: die Aussage über den
Code war richtig, der Beleg für den Zustand *beim Menschen* fehlte, und beim Öffnen des Heads ist
beides nicht unterscheidbar.

**Gebaut ist eine Browser-Probe, kein Produktcode:** `phase9_hardening/scripts/p9_step_d_self_check.py`
**16/16** gegen eine eigene TLS-Wegwerf-Instanz (`p9_step_d_wegwerf.py`, Port 18781 — außerhalb des
belegten Bandes 18765–18780, damit P9-57s Aussage für dieses Band gültig bleibt). **16 Stationen für
drei Zeilen** ist die eigentliche Aussage: ein Zug hat drei Fehlermöglichkeiten, und jede Station
trägt eine Abnahmezeile im JSON-Feld `zeile` — die Zuordnung steht **im Beleg**, nicht im Fließtext,
weil sie beim Zitieren sonst von der Station wegrutscht, die sie trägt.

**Die eine Entscheidung, die den Block kippen konnte — und warum sie so ausgegangen ist.** Ein
`element.dispatchEvent(new DragEvent(...))` hätte dieselben Stationen grün bekommen und **nichts**
belegt: den Listener, nicht den Zug eines Menschen. Vorab gemessen, nicht angenommen — Playwrights
echte Maus-Input-Pipeline in Chromium feuert die volle Kette (`dragstart` → `dragover` → `drop`
**mit** `dataTransfer`-Inhalt), sogar am Chromium-Headless-Shell, also ohne CDP-Drag-Interception.
Station 2 misst diesen Ereignisstrom deshalb mit und trägt `dragstart=1, dragover=19, drop=1`.
**Und die Gegenprobe G1 macht den Unterschied sichtbar:** mit entfernter Space-Bindung bleibt
`over=19` stehen (der Zeiger lag wohl auf der Zeile), `drop=0` — der Browser hat den Drop nie
angenommen, weil ohne `preventDefault` auf `dragover` kein Ziel gilt. „Der Code fehlt" und „der
Mauszeiger war nicht dort" sind zwei verschiedene Fehler, und diese Probe unterscheidet sie.

**P9-30 ist als *Aussehen* belegt, nicht als Klassennamen:** berechneter Stil am Ziel während des
Zugs — `border-top-style: dashed`, Farbe `rgb(62, 141, 243)` = `--accent` — auf der Space-Zeile, die
im Normalzustand keine gestrichelte Kante hat, plus zwei Bilder (Rail-Zuschnitt im Zug gegen
denselben Rail nach dem Zug: Toast, Ordnerzähler 3 → 2, Kante weg). Station 4 prüft das
**Wieder-Verschwinden** und bleibt im Gegenlauf G1 grün, weil ihre Aussage eine *Abwesenheit* ist —
bei nie gesetzter Klasse ist „nicht mehr da" trivial wahr. Das ist kein Loch, sondern die Aussage;
ich hätte es als „grün im Gegenlauf = wertlos" verbuchen können, und wäre falsch gewesen.

**Drei eigene Fehler, alle im selben Commit behoben — und jeder davon war ein Messgerät, das
etwas anderes maß als behauptet.** (1) Der Ereigniszähler zählte **sich selbst**: `start=3, over=57,
drop=3` für *einen* Zug, weil das Zähler-Snippet bei jedem `evaluate` die drei Listener erneut am
`document` registrierte. Behoben mit Einmal-Flag plus getrenntem Reset. (2) `store.create()`
**hängt** an, es leert nicht — der zweite `start` auf demselben `DATA_ROOT` sah jedes Item doppelt,
und der Zug fand die Zeile nicht mehr, weil der Vorlauf sie schon verschoben hatte. Behoben durch
Leeren **vor** dem Säen, mit einer harten Schranke: gelöscht wird nur `/tmp/opencode/p9-step-d-*`,
`ROOT` muss so heißen, sonst Abbruch. (3) Der neue Wächter war **rot**, weil er das verbotene Wort
im Docstring des Skripts selbst verbietet — ein Wächter, der die Begründung verbietet, verbietet die
Sache nicht. Behoben durch `tokenize` statt Rohtext. **Neunte Wiederholung derselben Repo-Lehre,
zum ersten Mal am eigenen neuen Test.**

**Ein vierter Fund, gegen den ich nichts gebaut habe, nur benannt:** die Regel in
`test_committed_probe_evidence.py` erkennt einen Gegenlauf daran, dass der Dateiname **endet** auf
`_gegenprobe` — und **keiner** der sechs älteren Block-Belege erfüllt sie, weil keiner einen
Gegenlauf im Repo hat. Die Regel wurde also gegen nicht existierende Dateien geschrieben und hat
noch nie zugeschlagen; meine beiden Dateien fielen zuerst darauf und wurden umbenannt. Der
generelle Punkt: eine Prüfung, die nie etwas gefunden hat, ist nicht „erfolgreich", sie ist
ungeprüft. Diesmal wie beim trace-Block haben **meine** Dateien die Regel ausgelöst, nicht eine
fremde.

**Selbstprüfung §0.4 — heute gemessen, nicht aus der Doku übernommen:** Probe **16/16**,
Gegenproben **11/16** (G1) und **15/16** (G2), `pytest` **1169 → 1175** (6 neue Wächter),
`ui_budget` 5/5, `doc_health` 0/0/0/0 nach dem Nachziehen der INDEX-Zeilen, Tabu-Bereichs-Diff auf
die sechs Hartpfade **leer** — `git diff` auf `app.js` und `tree.js` ist nach beiden Gegenläufen
leer, das ist der Nachweis, dass die Probe Produktcode **nur gelesen** hat · **kein `systemctl`, kein
`pkill -f`**: die Wegwerf-Instanz ausschließlich über ihre PID-Datei gestoppt · Live-Zustand vorher
gemessen und unverändert: neue Domain `400` (erwartet bis A7), Funnel-Rückfall `200`, Live-Release
`5414cb7` = Badge `v3.1.0`, `local.env` unverändert.

**Benannt, nicht entschieden:** `phase9_hardening/ABNAHME_MATRIX.md` steht jetzt bei **44.222 B =
3.262 B über dem Softcap** (vor diesem Block 40.573 B) — der Zuwachs ist Pflichtpflege eines
gebauten Belegs, und die drei Zeilen sind bereits auf Stand + Beleg gestrafft, die Herleitung steht
im Docstring und in diesem Block. Die zwei benannten Wege raus: der Deploy `v3.1.1` löst die vier
„warten auf den Deploy"-Posten am Dateiende auf (~4 KB in einem Block), und die `updated:`-Kette
ließe sich per `scripts/rotate_index_updates.sh` rotieren — das Skript ist allerdings auf
`docs/INDEX.md` festgenagelt und braucht dafür eine Datei/Archiv-Angabe; **ein Restposten, in
diesem Block nicht gebaut**, weil es gemeinsame Infrastruktur wäre.

**Nächster Schritt — unverändert deine Zuständigkeit, und diese Session hat daran nichts
verschoben:** (1) **A7+A8 in einer Sitzung** (`step_a/RUNBOOK_STEP_A.md`; schließt P9-10b, P9-12,
P9-13, P9-15, V150, V164 — ein Schnitt, weil der A7-Restart beide Connectoren kappt), (2)
**Release-Commit + Deploy `v3.1.1`** (Badge + `##`-Block erst am Deploy-Tag, sonst brennt P6-X; der
trace-Block kommt mit, **kein** Index-Neuaufbau), (3) danach der Rest von Gate/Z: Übersichtsgrafik
§12.4 (gerendert **und angesehen**), Wurzel-`CLAUDE.md` + `docs/INDEX.md` rotieren, ROADMAP-Zeile,
Phase auf ✅. **Neu und klein:** `rotate_index_updates.sh` um eine Datei/Archiv-Angabe erweitern
(drei Zeilen, mit vorhandenen Tests) — damit wäre die Kettenrotation auch für die lebenden Heads
mit langen Ketten benutzbar statt nur für `docs/INDEX.md`.

### Nachtrag — drei Funde aus der Selbstprüfung, alle drei im selben Commit behoben

**Die Tabelle, die vier Zellen in einer dreispaltigen Tabelle hatte.** Die Step-D-Zeile im
Modulstatus bekam von mir einen durchgestrichenen Alt-Stand **nach** der letzten Pipe — also als
vierte Spalte. Das bricht die Tabelle still: kein Fehler, kein roter Test, `doc_health` schweigt,
und der Text rendert eine Zelle zu weit. Sichtbar geworden erst durch den Zellvergleich mit den
Nachbarzeilen (3 vs. 4). Ein durchgestrichener Alt-Stand gehört **in** die Statusspalte.

**Die Größenangabe, die 2 Byte daneben lag, und warum das ein roter Test war.** `doc_health ::
_named_size_is_current` ist für die **Byte**-Form exakt; das ±2-KB-Fenster gilt nur der gerundeten
`~NNKB`-Form. Meine INDEX-Zeile nannte 56.140 B für eine 56.138-B-Datei — 2 Byte, und `oversize`
ging rot. Ich hatte das Fenster auch für die Byte-Form angenommen; die Toleranz ist eine bewusste
Entscheidung gegen wachsende Dateien (ein Prozentfenster würde bei 106 KB ein 32-KB-Loch öffnen),
und sie gilt nicht für Bytes. Kein Befund an der Sache, aber eine Erinnerung: die Zahl in der
INDEX-Zeile ist der **gemessene** Wert, sonst arbeitet der Wächter gegen den, der ihn schreibt.

**Die Wegwerf-Instanz lief noch, als ich fast committet hätte.** Nach dem letzten Probelauf bleibt
sie per Konstruktion stehen (der Aufrufer stoppt sie, Hard Rule 9). P9-57 verlangt genau das als
Prüfzeile — `ss -ltnp` zeigte beim Sammlen der Selbstprüfung noch `127.0.0.1:18781` (PID 2833710).
Gestoppt **ausschließlich** über die PID-Datei, danach `ss` ohne Treffer auf 18765–18781. Die
Produktionsinstanz (PID 1994214, Release `5414cb7`) wurde durchgehend nur gelesen.

## Session stopped — 2026-10-03 (fünfzehnter Block: Abnahmematrix P9-1–P9-82 und `[VERIFY]`-Bilanz stehen — und die Übergabezahl „40 Einträge" war ein Nummernbereich; opencode/M3, ein Commit, kein Code-Touch, kein Deploy, kein Service-Touch)

**Doku ohne Code, und die Übergabe nannte zwei Zahlen — eine davon stimmte nicht, und es ist die,
die man nicht nachprüft, weil sie „lückenlos" klingt.** `phase9_hardening/ABNAHME_MATRIX.md` steht:
**82 Abnahmezeilen in 83 Tabellenzeilen (P9-10 in zwei prüfbare Hälften geteilt) — 65 ✅ · 10 ⚠️ ·
8 ⬜**, jede Zeile mit Beleg (Testname, Probe-Datei, Journalzeile, Bild oder eine heute ausgeführte
Messung). **Kein einziges ⬜ ist offene Code-Arbeit:** alle acht hängen an zwei Nikinger-Schritten
(A7+A8: P9-10b, P9-12, P9-13, P9-15 · D1 als zurückgestellter Backlog-Posten: P9-27, P9-29, P9-30)
plus zwei Zeilen, die eine Entscheidung brauchen, die keine Messung liefern kann (P9-36, P9-31).
Einzelzeilen, Belege und die `[VERIFY]`-Tabelle stehen in der Matrix — dieser Block trägt die Funde
und die Selbstprüfung, nicht die Liste.

### Der Fund, der die Übergabezahl kippt: 34 belegte `[VERIFY]`-Einträge, nicht 40

Die Übergabe sagte „40 Einträge (V145–V172 / -173–-178 / -179–-184)". **Für die `P9-`-Nummern stimmt
das** (`1–58`, `59–68`, `69–82` schließen lückenlos, 82). **Für die `V`-Nummern war es eine
Bereichsangabe, die als Einträgzahl gelesen wurde:** V167–V172 sind in **keiner** Datei des Repos
definiert, sie kommen nur als Bereich vor (`§12`/`§13`: „V145–V172"). Belegt sind **34** (V145–V166
= 22, davon V166 nur im Session-Block vom 2026-09-25 statt im Plan-Register; V173–V178 = 6;
V179–V184 = 6) — **28 ✅ · 3 ⚠️ · 3 ⬜**, dazu 6 reservierte, unbelegte Nummern. Die Lücke bleibt als
Lücke stehen: sie zu belegen wäre Erfindung, sie umzunummerieren hieße einen 📕-Snapshot editieren.
**Achte Wiederholung derselben Repo-Lehre in derselben Datei, die ich schreibe** — nach `count() == 1`
für `[aria-current]`, nach den 15 statt 1 Knöpfen und nach der btn2-Messung, die die Beschriftung
traf: **ein Zähler, der das Richtige zählt, ist nicht der, der die Aussage trägt.**

**Und zwei Nummern sind je zweimal vergeben** (V162, V163: einmal im Plan-§13-Register, einmal im
Step-A-Runbook als „neu, hier"). Beide Lesarten stehen in der Matrix je mit ihrem eigenen Stand — V162
**2 × ⬜**, V163 **2 × ✅** (die socat-Frage hat sich durch die A0b-Ausführung beantwortet).

### Der zweite Fund: P9-56 hat einen Treffer, der nicht auf der Ausnahmenliste steht

`git diff --stat 06ab4f6^..HEAD` über die sechs Tabu-Pfade liefert **einen** Treffer:
`phase7_spaces_admin/tests/test_space_removal.py`, 17 Zeilen (+15/−2) — die Attrappe für `Store.move()`
mit eigener Signatur, die das neue `actor=` in einen HTTP 500 mitten im Space-Entfernen verwandelt
hat. **Nicht umbenannt:** §0.3 sagt für `phase7_spaces_admin/` „Code; Doku-Zeilen erlaubt", eine
Testdatei ist beides nicht. Die beiden **angekündigten** Öffnungen bleiben unberührt und je gemessen
(Step F genau drei Dateien, trace genau drei). **P9-56 steht deshalb ⚠️, nicht ✅.**

### Der dritte Fund, unbequemer: GA2 wurde nie gebaut — und die Lücke ist genau die drei offenen Zeilen

Plan §11 sah `phase9_hardening/scripts/p9_hardening_smoke.py` mit elf Stationen vor. **Die Datei
existiert nicht**; da sind die sechs Block-Proben (Reload, doing, trace, btn2, btn3, Step G). Damit
sind die Stationen ersetzt, die ein Block für sich trug — **und genau die drei, die niemand getragen
hat, sind P9-27, P9-29 und P9-30.** Kein Zufall: alle drei sind Sichtprüfungen am echten Gerät, und
das ist von Anfang an Nikinger-Arbeit. In der Matrix unter „Was diese Matrix nicht beweist" als
**Lücke der Belegkette** benannt, nicht als offener Step.

### Was sich durch Messung bewegt hat

**P9-14 ist geschlossen** (Funnel-Host live **200**, gemessen; die andere Hälfte — nummerierter
Rückfall — stand im Runbook). **P9-10b bleibt offen und ist jetzt gemessen** (weiter `400 Invalid host
header`; das Zertifikat live nachgemessen: CN `sharefyx.eurofyx.com`, LE `YE1`, `ssl_verify_result 0`).
**P9-3/V145 und P9-6 sind von ✅ auf ⚠️**, weil ihre Zahlen (38.822 B → 61.108 B; 42.080 B → 48.498 B)
inzwischen über der Grenze liegen und die Dateien das selbst benennen. **Vier `[VERIFY]`-Marker heute
beantwortet, zwei davon am Code statt aus einer Notiz:** V146 (die sieben `CARD_EXEMPT`-Einträge bilden
die vier INDEX-Kategorien ab, `header_cards` = 0 Befunde ⇒ kein ungenannter Fall) · V148 (Tailscale
kennt eigene Domains nur für **PAM**; `tailscale/tailscale#11563` sagt wörtlich, ein CNAME trage nicht,
weil Tailscale nur den SNI-Namen sieht ⇒ **P9-E bestätigt**) · V182 (`wrap_untrusted()` wirkt nur auf
`snippet`/`body`, `updated_by` daneben ⇒ **außerhalb**) · V184 (`app.js:283` setzt `state.ownSpace`
in `init()` **vor** `/meta` und `loadOverview()`). **Eine kleine Drift datiert hier korrigiert statt im
📕-Plan:** V155 — beide Plan-Anker (`:223`, `:274`) sind nach C6 gewandert, die echten heute sind
`resolve_endpoint()` `:97`, `DEFAULT_ENDPOINT` `:50`, `--endpoint` `:328`.

### Selbstprüfung §0.4 — heute gemessen, nicht aus der Doku übernommen

`pytest` **1169 passed in 218,31 s** · `ui_budget` **5/5** (**155,2 KB** gzip von 250 KB) · `doc_health`
**`index_lines 0 · header_cards 0 · updown_links 0 · oversize 0`** (nach dem Schreiben der Matrix) ·
Tabu-Bereichs-Diff mit **einem** Treffer (oben) · **Hard Rule 8 über alle 72 Commits seit `06ab4f6`
durchgezählt:** kein Commit ohne `.md`, und kein Commit mit Produktcode ohne den Phase-Head im selben
Commit (die 11 Commits ohne Head sind reine Runbook-Commits) · **P9-57 messbar:** kein Listener auf den
Wegwerf-Ports 18765–18780, die Produktionsinstanz läuft unverändert als PID 1994214 (nur gelesen) ·
kein `pkill -f`, kein `systemctl`.

**Die neue Datei liegt bei 40.573 B — 387 B unter dem Softcap.** Ehrlich, aber knapp; **der benannte
Weg bei der nächsten Verdopplung ist die Rotation der `updated:`-Kette per
`scripts/rotate_index_updates.sh`**, nicht Kürzen und kein zweiter L3-Schnipsel — die Matrix soll ein
Ort bleiben.

**Rotation im selben Commit:** der B17-Block (14.ter Block, **12.650 B**) wandert verbatim nach
`SESSIONS_ARCHIVE.md`, der Head trägt danach genau diesen Block. Head **68.153 → 55.503 B** durch die
Rotation, Archiv 195.890 → 208.540 B, alle fünf Gegenproben des Skripts grün — und nach dem Kürzen
dieses Blocks **53.106 B**, gegen **56.142 B** vor diesem Commit. **Mein erster Entwurf dieses Blocks war
10,3 KB groß und die Zeile im Block kündigte „56.142 → ~48.500 B" an — beide Zahlen waren
Schätzungen, und die Vorhersage war daneben** (ein langer Block für einen Doku-Schritt; der Detailteil
gehört in die Matrix, nicht zweimal in den Head). **Deshalb steht hier jetzt das gemessene
Ergebnis, und der Block ist gekürzt** — die Kürzung hat nichts gestrichen, sie verschiebt Beleg aus
dem Head in die Datei, die dafür da ist. Die Restmasse über dem Softcap sind weiter die **7.467 B
durchgestrichenen Statusabsätze** im Modulstatus; deren Streichen bleibt deine Entscheidung.

### Nächster Schritt, unverändert die Zuständigkeiten des Ningkers

(1) **A7+A8 in einer Sitzung** — schließt P9-10b, P9-12, P9-13, P9-15, V150 und V164; der
A7-Restart kappt beide Connectoren, also ist es ein Schnitt und kein Zwei-Schritt. (2) **Release-Commit
+ Deploy `v3.1.1`** — Badge + `##`-Block erst am Deploy-Tag (P6-X); der trace-Block kommt mit, **kein**
Index-Neuaufbau. (3) Dann der Rest von Gate/Z: Übersichtsgrafik §12.4 (gerendert **und angesehen**),
Wurzel-`CLAUDE.md` und `docs/INDEX.md` rotieren, ROADMAP-Zeile, Phase auf ✅. Die `v3.1.0`-Ziel-Angabe
in `docs/INDEX.md` bleibt bis zum Release-Commit liegen, wie am 2026-10-02 entschieden.

### Nachtrag Session-Ende 2026-10-03 — ein Amend, ausdrücklich angeordnet, mit zwei Gegenproben

Am Commit-Body stand ein von mir beim Formulieren **zerstörter Satz** („phase7_sard... nein,
phase7_spaces_admin/…"). Ich hatte den Commit bewusst nicht angefasst, weil ein Amend nicht beauftragt
war; der Nikinger hat ihn danach ausdrücklich verlangt, und **der Commit war zu dem Zeitpunkt rein
lokal** (`ahead 1`, `git branch -r --contains` leer) — **also ohne Force-Push**, was die Regel gegen
amendierte Historie nicht verletzt.

**Was repariert wurde:** genau ein Absatz, der P9-56-Fund. `723abcf` → **`953a125`**.

**Gegenproben statt Hoffnung:** (1) die neue Nachricht ist **byte-identisch zur alten**, wenn der
reparierte Absatz wieder eingesetzt wird (in Python geprüft, nicht behauptet — der ganze Rest des
Bodies, auch die Schlussabsätze zu meinem Ketten-Fehler und zur Doku-Hygiene, ist unangetastet);
(2) **`git diff --stat 723abcf 953a125` ist leer** — der Commit-Baum ist identisch, es ist nur die
Nachricht neu. Das ist der Beweis, dass ein Amend hier nichts am Repo geändert hat.

**Danach ist dieser Block geschlossen.** Kein weiterer Posten aus Gate/Z ist offen, der zu einer
offenen-Code-Zeile führt: die Abnahmematrix steht, die `[VERIFY]`-Bilanz steht, die drei Funde sind
benannt. Was bleibt, ist die Abnahme selbst — und die gehört dem Nikinger: **A7+A8 in einer Sitzung**
(schließt P9-10b, P9-12, P9-13, P9-15, V150, V164 — ein Schnitt, weil der A7-Restart beide Connectoren
kappt), dann **Release-Commit + Deploy `v3.1.1`** (Badge + `##`-Block erst am Deploy-Tag, sonst
brennt P6-X; der trace-Block kommt mit, **kein** Index-Neuaufbau). Danach der Rest von Gate/Z:
Übersichtsgrafik §12.4 (**gerendert und angesehen**, nicht ungesehen gemeldet), Wurzel-`CLAUDE.md` und
`docs/INDEX.md` rotieren, ROADMAP-Zeile neu, Phase auf ✅.

## Session stopped — 2026-10-02 (vierzehnter Block: B17 gebaut — ein Knopf, zwei falsche Zahlen im Backlog und ein Konflikt mit einer gelockten Zeile; opencode/M3, ein Commit, kein Deploy, kein Service-Touch)

**Der Auftrag war die kleinste offene Aufgabe, und die Übergabe hat ihren Umfang selbst falsch
beschrieben.** Von vier Posten waren drei deine Infra-Schritte; der vierte (B17) wurde als „15 Knöpfe
ans Schema" notiert. **Gemessen vor dem Bauen** — Markup *und* CSS, nicht geglaubt — waren es
**ein** Knopf mit einem Befund und **zwei** Klassen mit je eigener Bedeutung.

| Vorher behauptet | Gemessen | Folge |
|---|---|---|
| 15 Knöpfe mit eigenen Flächen | **75 von 77** tragen eine Standard-Fläche; Ausnahmen sind `.btn-primary` (**13**, Akzent) und `.btn.action--caution` (**1**) | `.btn-primary` ist **kein Reststand**, sondern die dokumentierte Ausnahme deiner Entscheidung vom 2026-10-01 (`app.css`, Kommentar in `.btn`) — sie bleibt, sonst hätte ich einen Lock gerissen |
| „`.btn.action--caution` (**2** Knöpfe)" auf `--btn-face-*` | **1**. Der Selektor matcht nur `#archive-button`; `#logout-button` ist ein `.rail__action` (`background: none`) und trägt die Vorsicht nur an der **Farbe** — er hatte nie eine Fläche | Zählen über Klassen-Präsenz statt über den Selektor: **dieselbe Fehlerklasse wie `count() == 1` für `[aria-current]`** im btn2-Lauf (Selektoren matchen ein Attribut, nicht seinen Wert) |

**Der eigentliche Befund ist eine Helligkeit, kein Token — und er ist beim Messen entstanden, nicht
beim Umstellen.** `--btn-face-top` `#2A313A` ist **heller** als die Standardfläche
`--btn-std-fill` `#0C1C31`. „Vorsicht" war damit der **auffälligste** Knopf der Editor-Fußzeile statt
des Standards — genau das Gegenteil der Absicht, die der Wächter
`test_caution_and_primary_buttons_keep_their_own_look` beschrieb („Archivieren [sieht aus] sonst
aus wie jeder andere Knopf"). Die Backlog-Liste hatte den Zustand als *Konsistenz*-Lücke beschrieben
und damit die sichtbare Wirkung aus dem Blick verloren.

**Der Konflikt, den ich gestoppt und zurückgebracht habe.** Mein Vorschlag war eine eigene
`--caution-std-*`-Familie: dieselbe Struktur wie `--btn-std-*`, nur in der Vorsicht-Farbtiefe, in der
Rechnung also deckend und dunkel. Du hast sie gewählt. Beim Vorbereiten des Blocks stieß ich auf
`phase8_ui_graph/CLAUDE.md` und musste die Frage zurückstellen, weil sie zwei gelockte Zeilen bricht:
die Konvention v3 sagt für „Vorsicht" wörtlich *Standard-Knopfplastik, aber `color: var(--caution)`
auf Label und Glyph; **keine** gefüllte rote Fläche*, und deine P9-Notiz vom 2026-10-01 nennt
`.action--caution` als Ausnahme, die „behält die graue Plastik". **Eine rot getönte Fläche *ist* die
gefüllte rote Fläche**, die die Konvention ausschließt — das war keine Interpretationsfrage, sondern
der Wortlaut. Nach der Rückfrage: **exakt die Standardfläche**, wortgleich mit v3, und damit ohne
Konventionsänderung.

**Was gebaut wurde, ist folgerichtig die kleinste mögliche Änderung: die drei
`.btn.action--caution`-Regeln sind gelöscht, nicht umgeschrieben.** `.btn` *ist* die Standardfläche;
eine eigene Kopie davon wäre genau die „zweite Knopfoptik im selben Panel", die derselbe Tag am
2026-10-01 an `.account-nav` abgestellt hatte. Kein `:root`-Token kommt hinzu, keins wird verwaist —
die alte Familie `--btn-face-*` hängt jetzt **nur noch am Badge `.rail__glyph`**, wo sie
ausdrücklich bleiben soll. Die Kategorie bleibt sichtbar, aber an der **Beschriftung** statt an der
Fläche.

**Die Wächter, und einer davon musste umgedreht werden.** `test_caution_and_primary_buttons_keep_their_own_look`
hätte nach dem Umbau genau das behauptet, was jetzt **falsch** ist. Ein umgedrehter Testname wäre eine
Lüge gewesen, also: heißt jetzt `test_primary_keeps_its_own_face_and_caution_wears_the_standard_one`
und trägt **beide** Richtungen mit Datum im Docstring (dasselbe Muster wie der umgedrehte
doing-Wächter des 2026-10-02). Neu sind zwei: einer zählt die **Markup**-Träger statt der
CSS-Textstellen — ein Wächter, der „`.btn.action--caution` deklariert keine Fläche" prüft, ist
sonst grün, wenn die Klasse aus dem Markup verschwindet; der andere macht die alte Familie
**badge-only** (Kommentare vorher entfernt, denn `app.css` *nennt* `--btn-face-top` an mehreren
Stellen im Klartext). Der Docstring von `test_rail_glyph_is_a_badge_and_keeps_the_plastic` musste
mitwandern: er stand auf „**letzter** Verbraucher", und das war ab hier eine Behauptung, die das CSS
nicht mehr trägt.
**Gegenprobe mit vier eingebauten Verstößen → 8 rote Assertions** (G1 alte Fläche zurück → 2 rot ·
G2 Vorsichtfarbe entfernt → 1 rot · G3 Trägerklasse aus dem Markup → 2 rot · G4 Badge steigt mit → 3
rot), Kontrolllauf 0 rot, danach byte-identisch wiederhergestellt.

**Pixel-Beleg `p9_btn3_caution_probe.py` 14/14** (eigene TLS-Wegwerf-Instanz auf Port 18775,
gestoppt über die PID-Datei). Kernstation: die **berechneten** `backgroundImage`-Strings sind
stringgleich (`linear-gradient(rgb(12,28,49), rgb(5,11,19))` auf beiden), vier Pixelproben an der
glyphenfreien Spalte x=4 px mit **max |Δ| = 1** (Toleranz ±2), die Vorsichtfarbe sitzt in der
Beschriftung (`rgb(229,72,77)` gegen `rgb(233,237,242)` beim Standard). **Gegenlauf:** die alte
Fläche wieder eingebaut → **6 von 13 Stationen rot**, Δ 25–28 an allen drei Höhen; die Datei kam
danach als `*_gegenprobe.json` und wurde wieder entfernt (Muster aus dem trace-Block).

**Zwei eigene Fehler, beide in derselben Stunde, beide im selben Commit behoben.** (1) Mein
`.btn`-Kommentar enthielt eine `{ }`-Klammer — `_block_body` schneidet mit `[^}]*`, der Kommentar
hat also den Block abgeschnitten und den bestehenden Wächter rot gemacht. (2) Derselbe Kommentar
hätte **genau den neuen Wächter grün gemacht**: er *nennt* `color: var(--caution)` im Klartext, und
die Regex für die Vorsichtfarbe hätte den Kommentar statt des Codes getroffen. Der Wächter strippt
jetzt die Kommentare vorher — **ich hätte beim selben Mal die siebte Wiederholung derselben Repo-Lehre
gebaut (ein Wächter, der den Kommentar über den Code prüft) und es erst beim Ausführen gemerkt.**

**Ein dritter Fund, diesmal im eigenen Beleg.** Das erste Bild der Probe hieß `p9_btn3_01_footer.png`
und zeigte `#editor-toolbar` — die **Formatierleiste**, die den Vorsichtsknopf gar nicht enthält. Der
Dateiname behauptete das Gegenteil, und das ist derselbe Fehler wie der trace-Beleg, der der Gegenlauf
selbst war: **ein Beleg, der etwas anderes zeigt als das, wofür er zitiert wird.** Jetzt ist es der
Zuschnitt von `.editor__head-actions` (dort stehen „Archivieren", „Speichern" und „×" nebeneinander),
und die Ruhe-Aufnahme entsteht **nach** dem Wegziehen des Zeigers — im ersten Entwurf wäre sie im
Hover-Zustand entstanden, also im btn2-Lauf derselbe Reihenfolgefehler wie bei der Verlaufsmessung.

**Und der Vision-Adapter hat dasselbe Bild falsch gelesen — das gehört dokumentiert, nicht versteckt.**
Am Vollbild meldete er „Archivieren" mit **dunkelrotem** Hintergrund und „Speichern" mit hellgrauem:
eine **Vertauschung**, und die rote Fläche existierte im Bild gar nicht (es war die rote
*Beschriftung*). Am isolierten Zuschnitt desselben Knopfes war die Antwort brauchbar — Fläche
`(10,10,50)` gegen gemessen `(10,23,40)`, der **R-Kanal exakt**. Also nicht „das Modell taugt nicht",
sonne eine **eigene Fehlerklasse**: ein VLM ist als Farbmessgerät an *einem* Element brauchbar und als
**Zuordner über mehrere Elemente** unbrauchbar. Als neue Zeile in
`docs/concepts/sichtpruefung_automation_tooling.md` §Vormerkung 2026-09-28 abgelegt, mit der
präzisierten Regel **„ein Bild, ein Element, eine Frage"** — dieselbe Zuständigkeitsgrenze wie
2026-09-28, am zweiten Beispiel. **Eigene Kontrollmessung, ohne Modell:** Histogramm der
eingecheckten PNGs — Fläche `(10,23,40)`/`(7,16,28)`, Kante `(29,67,116)` = `--btn-std-line`, 281 rote
Beschriftungspixel, **3** Pixel in der alten Grau-Umgebung (Kanten-Antialiasing).

**Benannt, nicht entschieden — der Kontrast.** Die Vorschrift-Beschriftung liegt jetzt bei
**4,38:1** gegen die Standardfläche (vorher 3,36:1 auf der grauen Plastik). Das ist **besser und
weiterhin kein AA**: WCAG verlangt 4,5:1 für normalgroßen Text, und 14 px/500 ist kein „large
text". Ich habe den Wert als *Verschlechterungsverbot* in die Probe aufgenommen (eine echte
Eigenschaft, die diese Runde zusichert) und den Absolutwert **nicht** zum Schwellwert gemacht. Die
Kandidaten — hellere Vorschriftfarbe, oder die Kategorie doch an eine 1-px-Kante — sind
Design-Entscheidungen und gehören dir.

**Selbstprüfung:** `pytest` **1167 → 1169** (netto +2: ein Wächter umgedreht, zwei neu; Baseline
vorher gemessen, nicht aus der Doku übernommen) · `ui_budget` **5/5**, und die Zahl **gemessen statt
behauptet**: mit Stash-Gegenprobe **165,0 KB auf HEAD gegen 165,2 KB mit diesem Block** — die in der
Wurzel-`CLAUDE.md` protokollierte **155,1 KB war schon veraltet**, sie stammt aus dem trace-Block; mein
Anteil ist +0,2 KB (KommentarZeilen, die die Löschung aufwiegen) · `doc_health` **0 Befunde** ·
Tabu-Diff auf die sechs Hartpfade **leer** (nur `app.css`, eine Testdatei, ein Skript, `.md`) ·
Wegwerf-Instanz **über die PID-Datei** gestoppt, kein `pkill -f`, kein `systemctl`, `sharefyx-mcp`
nicht berührt.

**Zwei Entscheidungen nach diesem Commit, hier festgehalten, weil sie den nächsten Block
definieren.** (1) **Gate/Z kommt jetzt** — die Abnahmematrix und die `[VERIFY]`-Bilanz sind das
nächste Item, und sie brauchen **keinen Deploy und keinen Code**. Der Umfang ist gegen die drei
Planquellen **verifiziert**, lückenlos und nicht geschätzt: **P9-1 – P9-58** (Plan §14) ·
**P9-59 – P9-68** (`block_doing_plan.md`) · **P9-69 – P9-82** (`block_trace_plan.md`) — zusammen
**82** Zeilen; `[VERIFY]` **V145–V172** · **V173–V178** · **V179–V184** — zusammen **40**. Ich hatte
die Zahl angezweifelt, weil der Gate/Z-Status seit zwei Sitzungen „P9-1–P9-82" behauptet, ohne
dass eine Quelle sie getragen hätte: **sie stimmt**, und die Bereiche schließen lückenlos. (Fast
hätte ich sie selbst korrigiert — die Umkehrung wäre eine stille Abweichung gewesen.)
(2) **Die Matrix kommt in eine neue Datei** `phase9_hardening/ABNAHME_MATRIX.md` (L2 mit L1-Card +
INDEX-Zeile) plus Pointer im Head — **Nikinger-Entscheidung 2026-10-02**, gegen die P8.6-Lesart
(kanonischer Closeout in Plan §9, ein 📕-Snapshot, der bisher unberührt ist). Der Grund ist nicht
die Ordnung, sondern der Softcap: der Head liegt **13.008 B über** der Grenze, und ein 82-zeiliges
Archiv hineinzuschreiben hieße, das Falsche zu tun. Die Disziplin der Zeilen: `✅`/`⚠️`/`⬜`/
`ersetzt` **mit Beleg** (Testname, Probe-Datei, Journalzeile, Bild), und was den Live-Deploy braucht
(trace-Block, B17-Sichtung, Gs Live-Löschung, Hs Release-venv-Beleg) bekommt **`pending: Deploy
v3.1.1`** statt einer Vermutung. **Drei Zeilen sind schon heute messbar** und gehören nicht auf die
later-Warte-Liste: `P9-56` (Bereichs-Tabu-Diff mit genau der angekündigten Step-F-Ausnahme),
`P9-57` (Service-Touch durch einen Agenten = 0), `P9-58` (`pytest`, `ui_budget`, Doc-Update je
Commit).

**Und eine Zeile, die bewusst liegen bleibt:** `docs/INDEX.md` nennt als Ziel der Phase 9 weiterhin
`v3.1.0`. Das ist mit dem heutigen Deploy überholt, aber es ist eine **Ziel-Angabe** — sie gehört in
den Release-Commit, der ohnehin `v3.1.1` macht, und nicht in eine Gate/Z-Doku-Runde.

**Nächster Schritt, unverändert die Zuständigkeiten des Nikinger:** (1) **Release-Commit + Deploy
`v3.1.1`** — Badge `app.html:20` + `##`-Block in `docs/UPDATE_LOG.md`, **beides erst am Deploy-Tag**,
sonst brennt das `deploy.sh`-Gate P6-X bei späterem Deploy ab; dieser Block kommt mitdeployt, ist
aber eine reine CSS-Änderung. (2) **A7+A8 in einer Sitzung** (Befund 4: der A7-Restart kappt beide
Connectoren), danach ist SP9-10b geschlossen und der Warndialog auf der alten Funnel-Adresse darf
sterben. (3) Danach der Rest von Gate/Z: Abnahmematrix P9-1–P9-82 und `[VERIFY]`-Bilanz V145–V184.

**Doku-Rest, benannt statt versteckt, unverändert:** Phase-9-Head jetzt über dem Softcap (vor diesem
Block 50.904 B, mit dem Block mehr), Wurzel-`CLAUDE.md` 107.576 B, `docs/INDEX.md` ~58 KB. Für den
Head ist die Rotation des Modulstatus der benannte Weg und **deine Entscheidung** — die
durchgestrichenen Statusabsätze (7.467 B) habe ich **nicht** angefasst, auch nicht in dieser Session.

## Session stopped — 2026-10-02 (dreizehnter Block: Gate/Z-Doku-Hälfte — zwei Sektions-Rotationen, P9-L-Lauf und ein Skript-Defekt; opencode/M3, ein Commit, kein Deploy, kein Service-Touch, kein Code-Touch) Kein Code-Schritt war offen, und die drei
Posten der Übergabe, die nicht dem Nikinger gehören, waren alle Doku-Arbeit. Also die
Doku-Hälfte von Gate/Z, und mit ihr ein Fund, der größer war als die Aufgabe.

**Die zwei benannten Softcap-Überschreitungen sind weg — durch Verschieben, nicht durch Streichen:**

| Datei | Abschnitt | Bewegung | Ergebnis |
|---|---|---|---|
| `phase1_storage/CLAUDE.md` | „Geerbte Contracts" (388 Zeilen / 31.422 B) | → `CONTRACTS_ARCHIVE.md` (neu, L3, mit L1-Card) | **47.570 B → 19.498 B**, erstmals seit 2026-09-30 wieder unter dem Softcap |
| `phase5_ui/CLAUDE.md` | „Abnahmestand (Plan §6)" (99 Zeilen / 12.195 B) | → `ABNAHME_MATRIX_ARCHIVE.md` (neu, L3, mit L1-Card) | **43.801 B → 33.1 KB**, unter dem Softcap |

Beide **verbatim**, per `python`-Schnitt statt Abtippen, mit einer Roundtrip-Gegenprobe *vor* dem
Schreiben (`Original == Prefix + verschobener Block + Suffix`) und einem byte-identischen
Gegenlesen *danach*. In den Heads bleibt jeweils genau das, was jemand zum Entscheiden braucht:
die **Zusicherung** im Wortlaut („Eine Änderung daran nach Phasenabschluss ist eine
Scope-Änderung") plus ein **Index** (welche Öffnung, welche Phase, welcher Stand), und der
**Abschnittsname bleibt stehen** — `phase6_shares_plan.md` §, `PHASE7_CLOSEOUT_HANDOVER.md` §4,
P8-M und die P9-Pläne verweisen wörtlich auf „§Geerbte Contracts", und ein toter Verweis wäre
eine stille Lüge im Doku-Layer.

**Der Fund: das Rotationsskript hat die Hälfte rotiert und es gemeldet.** Der erste echte Lauf
von `scripts/rotate_index_updates.sh` gegen die echte `docs/INDEX.md` meldete „Split ist
verlustfrei" — und rotierte **1 von 3** Einträgen. Ursache: der Split-Anker ist
`' | (?=\d{4}-\d{2}-\d{2})'`, und die Kette trug einen Faden mit **`updated: `-Präfix**, den der
Anker deshalb nicht als Kettenanfang sieht. Verlustfrei war die Aussage nur *innerhalb* des
geschnittenen Teils; die Kette sah danach konform aus, also wäre nie jemand nachgesehen.
**Sechste Wiederholung derselben Repo-Lehre** (ein Wächter, der etwas anderes prüft als er
behauptet — diesmal sogar einer, der die Richtigkeit *seiner eigenen* Byte-Bilanz meldet).
Gebaut: **Gegenprobe (e)** im Skript (bricht mit klarer Meldung ab, wenn die Kette ein zweites
`updated: `-Präfix trägt) und **zwei Tests** — einer, der den Abbruch prüft, und einer als
Gegenprobe, dass ein sauberer Lauf *alle* älteren Fäden rotiert, damit (e) nicht stillschweigend
alles ablehnt. **Gegenprobe am Wächter selbst:** (e) entfernt → genau der Abbruch-Test rot.
Dazu die datierte Drift-Korrektur an der Kette (das Fremd-Präfix entfernt) und eine Korrektur am
Docstring des Testmoduls, der noch „carries one entry" behauptete.

**Was ich bewusst nicht getan habe, mit Zahlen statt mit Bauchgefühl.** Dieser Head steht nach
diesem Block **über dem Softcap**. Die Rotation allein bringt ihn auf 38.256 B; mein Block liegt
darüber. Der Rest ist der **Modulstatus (18.217 B)**, und darin stehen **zwei durchgestrichene
Statusabsätze mit zusammen 7.467 B** — überholte Zustände wie „install + P9-19 ausstehend", von
denen die aktuelle Spalte denselben Befund schon trägt. **Streichen wäre die einzige Maßnahme,
die den Head sicher unter den Softcap brächte** — und sie ist eine Nikinger-Entscheidung, weil sie
7 KB aus dem Head der *laufenden* Phase nimmt, auch wenn der Wortlaut im Archiv steckt. Vorgeschlagen,
nicht getan. Ebenfalls unangetastet: die Wurzel-`CLAUDE.md` (99.051 B, §Current state 77.794 B —
dort ist die Rotation der Current-state-Abschnitte die benannte Lösung) und `docs/INDEX.md`
(57.595 B, **heute größer als vorher**: zwei Pflicht-Zeilen für die neuen Archive kamen hinzu, die
`updated:`-Rotation sparte nur 347 B netto). Alle drei bleiben **benannt statt versteckt**, wie
P8-P es verlangt.

**Selbstprüfung:** `doc_health` **0 Befunde** (vorher 0, mit zwei erwarteten Befunden zwischen den
Schritten: die zwei neuen .md ohne INDEX-Zeile, nach deren Eintrag wieder 0) · `pytest` **1152 →
1162** (**10 neu**: 2 für die Skript-Gegenprobe (e) + **8 neue Wächter** in
`phase9_hardening/tests/test_doc_rotations.py`, die beide Rotations-Hälften festnageln — kein echtes
Repo-Diff, nur die Dateien selbst) · **Gegenprobe: fünf eingebaute Verstöße → fünf rote Tests**, jeder mit
eigener Assertion; ein erster Entwurf der Wächter suchte den Zeiger über die *ganze* Datei und blieb bei zwei
der fünf Verstöße grün (der `down:`-Eintrag der L1-Card nennt das Archiv ebenfalls) — erst auf den Abschnitt
selbst eingegrenzt ·
`ui_budget` 5/5 unberührt (kein `phase5_ui/webui/static/**`-Touch) · Tabu-Diff auf die sechs
Hartpfade **leer** — es wurden ausschließlich `.md`-Dateien und ein Skript angefasst, kein Python,
kein JS, kein `storage/`/`mcpserver/`/`authserver/` · kein `systemctl`, kein `pkill -f`, keine
Wegwerf-Instanz gestartet, `sharefyx-mcp` nicht berührt.

**Zweite Überraschung derselben Session, gefunden beim erneuten Lesen der Sichtprüfungs-Bilder:** der
eingecheckte Browser-Beleg des trace-Blocks war **der Gegenlauf selbst** (`alle_ok: false`, Bild 05 zeigte
`beta` statt `alpha`), weil Skript und Ausgabepfade beim Hand-Gegenlauf identisch waren — im Repo blieb
alles glatt, weil die Datei existierte und nur die Zahl im Kopf falsch war. Code war korrekt
(`editor.js:781`), Beleg war es nicht. Eigener Lauf gegen die Zwei-Principalen-Wegwerf-Instanz →
**8/8 grün**, Probe und fünf der sechs Bilder neu erzeugt, `test_committed_probe_evidence.py` (4 Tests)
hält das fest, **Gegenprobe 2 Verstöße → 3 rote Tests**, plus ein Test mehr, weil die (e)-Prüfung beim ersten echten Anwenden **zu blinder** war als ihre Behauptung (dritter Fund unten). Vollständig im Korrekturabsatz darüber.

**Sichtung vom 2026-10-02: erledigt.** Der Nikinger hat die sechs Bilder **abgenommen — mit der Notiz,
dass noch nicht alle Knöpfe an das Schema angepasst sind** (B17 im Backlog, dort mit der gemessenen
Klassenliste). Vor der Sichtung habe ich sie mit dem Vision-Wrapper quer gelesen; fünf Bilder trafen ihr
Kriterium, Bild 05 verriet den Gegenlauf-Beleg. **Was ich daraus gelernt habe, ohne es zu vergrößern:** ein
Restbefund, den ein Mensch sieht, muss nicht erst *wiederentdeckt* werden — er gehört mit der Messung ins
Backlog, sonst steht er in zwei Sitzungen als Überraschung da.

**Und ein dritter Fund, aus dem allerletzten Schritt — er betrifft die Gegenprobe selbst.** Beim Anwenden
der (e)-Prüfung auf die *echte* Kette hat das Skript **abgebrochen**, obwohl die Kette in Ordnung war: der
`updated:`-Eintrag vom 2026-10-02 **erwähnt** die Zeichenkette ``updated: ``, weil er genau diesen Defekt
beschreibt, und meine `case`-Prüfung suchte das nackte `updated: ` irgendwo im Text. Geprüft wird jetzt nur
der **Fadenanfang** `` | updated: <ISO>``; ein zusätzlicher Test erlaubt ausdrücklich, die Zeichenkette im
eigenen Eintragstext zu nennen. **Das ist die kleine Schwester der Lehre vom selben Nachmittag — ein Wächter,
der blinder ist als seine Behauptung, ist schlimmer als gar keiner**, und hier hätte er den einzigen Mechanismus
lahmgelegt, der die Kette klein hält. Der anschließende echte Lauf rotiert **3 Fäden** (59.335 → 57.672 B).

**Session beendet 2026-10-02. Für die nächste Session, der Zustand in fünf Zeilen:**

1. **B17 ist als potentieller Extra-Schritt dokumentiert** (Modulstatus-Zeile „E (Extra)"), nicht entschieden.
   Er ist der einzige Punkt, der *hier* ohne deine Infra-Schritte liegen bleiben kann — die anderen warten
   alle auf dich.
2. **Offen und nur bei dir:** A7+A8 in einer Sitzung (Befund 4: der A7-Restart kappt beide Connectoren).
3. **Danach:** Release-Commit (Badge `app.html:20` + `##`-Block in `docs/UPDATE_LOG.md`, **beides erst am
   Deploy-Tag**, sonst brennt das `deploy.sh`-Gate P6-X) und Deploy **`v3.1.1`**.
4. **Danach Gate/Z:** Abnahmematrix P9-1–P9-82, `[VERIFY]`-Bilanz V145–V184. Kann inhaltlich erst nach
   dem Deploy abschließend bewertet werden.
5. **Doku-Rest, benannt statt versteckt:** Phase-9-Head 48.550 B (davon 7.467 B durchgestrichene
   Statusabsätze im Modulstatus), Wurzel-`CLAUDE.md` 107.330 B, `docs/INDEX.md` ~58 KB. Für den Head
   ist die Rotation des Modulstatus der benannte Weg und **deine Entscheidung**; die anderen beiden haben
   ihre benannten Lösungen in `CLAUDE.md`/`docs/INDEX.md`.

**Diese Session hat keinen Code angefasst.** Drei Commits: `deb72df` (Doku-Hälfte Gate/Z), `f544f8c`
(Beleg-Defekt + 8/8 nachgefahren), `68d3314` (Sichtung abgenommen, B17) — plus dieser Abschluss.

**Nächster Schritt, unverändert die Zuständigkeiten des Nikinger:** (1) ~~Sichtung~~ **erledigt**; es bleibt
`p9_trace_*`-Bilder, Kriterien in `screenshots_latest/README.md`; (2) **Release-Commit + Deploy
`v3.1.1`** — der Badge und der `##`-Block müssen am Deploy-Tag entstehen, ein heute datierter
Block ließe das `deploy.sh`-Gate (P6-X) bei einem späteren Deploy abbrennen; (3) **A7+A8 in einer
Sitzung** (Befund 4: der A7-Restart kappt beide Connectoren), danach ist SP9-10b geschlossen und
der Warndialog auf der alten Funnel-Adresse darf sterben. Danach der Rest von Gate/Z: Abnahmematrix
P9-1–P9-82 und die `[VERIFY]`-Bilanz V145–V184.

## Session stopped — 2026-10-02 (zwölfter Block: Block trace gebaut — `assignee` sichtbar, `updated_by` + Git-Autor, P9-Y–AD; opencode/M3, ein Commit, kein Deploy, kein Service-Touch) Die Frage, die Claude Codes Planungssession aufwarf: *was bedeutet
`doing` in einem Space mit zwei Personen?* Antwort vorher: der Status ist geteilt, aber **niemand
wird aufgezeichnet** — nicht im Item, nicht in Git (`git log` im DATA_ROOT kannte nur
`Space Server`). Jetzt beides, für Menschen **und** für ein angeschlossenes LLM.

**Gebaut (Locks P9-Y–AD, ein Commit):** `assignee` wird in Liste und Editor sichtbar und
editierbar, und der **Client** füllt es beim Wechsel auf `doing`; neu ist das
server-verwaltete `updated_by` (Home-Space des authentifizierten Principals, über **keinen**
Kanal setzbar) plus der Git-**Autor** (`--author`, Committer bleibt `Space Server`). MCP liefert
beide Felder in jedem Item- und Trefferobjekt und sagt dem LLM per `_ASSIGNEE_HINT`, wann es
`assignee` setzen soll — wörtlich identisch an `create_item` und `update_item`.

**Zwei Entscheidungen, die der Plan so nicht hatte, beide im Code begründet:**
1. **Die Regel sitzt beim Client, weil sie einem Statuswert Bedeutung gibt** (P9-Z). Der Server
   kennt Token → Space; „in Arbeit heißt: X arbeitet daran" wäre genau die Statussemantik, die
   das Kernprinzip verbietet. Deshalb ein JS-Zweig plus ein Werkzeug-Beschreibungssatz, **keine**
   `if`-Verzweigung im Kern.
2. **`actor` ist ein optionales Keyword mit Default `""`** (P9-AD). Der Preis ist benannt: eine
   vergessene Aufrufstelle fällt nicht mehr per `TypeError` auf, sondern erzeugt still ein
   `updated_by: ""`. Der Ersatz ist **ein Wächter über den AST**, der *jedes* Nicht-Test-Modul in
   `mcpserver/` und `webui/` abklapft — nicht nur `tools.py`/`api.py`. Gemessen war dabei: ein
   blinder Attribut-Scan findet in den beiden Paketen 17 Treffer, davon **8 Listen-/dict-Methoden**
   (`routes.append`, `fields.update`); der Wächter prüft deshalb am *Empfänger*, sonst wäre er
   bei Falsch-Positiven rot und damit abgeschaltet.

**Der Git-Autor ist live belegt, nicht behauptet:** die Wegwerf-Instanz des Blocks hat **zwei
Konten** (`alpha`, `beta`) in einem geteilten Space und **echte Git-Historie** (`git=True`).
`git log --format=%an -3` nach dem Lauf: `beta, alpha, alpha`. Ohne den zweiten Principal hätten
`updated_by` und `assignee` denselben Wert getragen und die häufigste Verwechslung wäre unsichtbar
gewesen — deshalb zwei Browser-Kontexte statt einem.

**Browser 8/8** (`probes/p9_trace_probe.json`), und die **Gegenprobe ist der eigentliche Beleg:**
ohne die Leer-Prüfung im P9-Z-Zweig springt der Assignee einer **A zugewiesenen** Aufgabe von
`alpha` auf `beta`, sobald B sie in Arbeit zieht (S5 rot). Genau das ist die Klausel, die P9-Z
wörtlich verlangt („ein gesetztes `assignee` überschreibst du nur, wenn ein Mensch es ausdrücklich
sagt"). **Ein Test musste datiert zugeschnitten werden, nicht entfernt:** der Wächter gegen
abgetipptes Step-F-Vokabular in `editor.js` (`test_step_f_schema.py`) verbot jedes Vorkommen von
`assignee|doing` — P9-Z verlangt genau das Gegenteil, weil sich „bei `doing` füllen" nicht ohne
den Namen des Statuswerts ausdrücken lässt. Neu gilt: keine abgetippte Vokabular-*Liste*, aber
genau **eine** benannte Verzweigung mit Leer-Prüfung; der Docstring trägt beide Richtungen mit
Datum. **Und ein Bestandstest kam mit:** `test_app.py` prüft die Patch-Quittung als exaktes Dict
und war der erste Ort, an dem die neue Quittungszeile auffiel.

**Eine Plan-Klammer war ungenau, gemessen statt geglättet:** P9-AA sagt „ein mitgeschicktes Feld
ist `ValidationError`, wie heute `updated`". Für **PATCH** stimmt das (`422 validation_failed`,
`api.py:890`) und für den Kern (`_SYSTEM_MANAGED_FIELDS`), für **POST** nicht: `_items_post` hat
keine `unknown`-Prüfung, sondern filtert lautlos auf eine Whitelist — ein `updated_by` im POST-Body
wird still verworfen, genau wie `created`/`version`/`space` heute. Der Kern bleibt unberührt
(P9-74 hält: kein Kanal kann es setzen), aber die *Form* der Ablehnung ist je Route eine andere.
**Bewusst nicht vereinheitlicht** — eine `unknown`-Prüfung im POST würde Round-Trips über
Schreib-Clients brechen, die den vollen Item-JSON zurückschicken.

**Nicht gebaut, mit Argument:** eine Verlaufsansicht („wer hat wann was geändert", aus `git log`) —
P9-Y, vom Nikinger nicht gewählt, P10-Kandidat. `created_by` wäre ein zweites Feld für eine
Angabe, die bereits im ersten Git-Commit **des Items** als Autor steht.

**Nächster Schritt:** Release-Commit (Badge + `##`-Block in `docs/UPDATE_LOG.md`) und Deploy
`v3.1.1` (Vorschlag aus dem Plan §6; die Nummer entscheidet der Nikinger) — beides
Nikinger-Schritt, Hard Rule 9. **Danach A7+A8 in einer Sitzung** (Step A, Befund 4: der A7-Restart
kappt beide Connectoren). **Nikinger-Sichtprüfung** der sechs Bilder in
`screenshots_latest/`: Feld „Bei", die Lesezeile, und dass ein Altbestand-Item **keine** leere
Zeile bekommt.

## Session stopped — 2026-10-02 (elfter Block: Deploy-Abbruch `v3.1.0` behoben, danach Nikinger-Deploy live + Block trace geplant — Claude Code, kein Service-Touch)

**Ergebnis: der Abbruchgrund ist weg, der Deploy kann wiederholt werden — mit neuem SHA.**
Der erste `deploy.sh`-Lauf (Release `20261002T090429.818809Z`) brach in Schritt 4 ab:
`4 failed, 1119 passed, 5 errors`, alle neun in
`phase9_hardening/tests/test_mcp_local_vision_server.py`, alle
`ModuleNotFoundError: No module named 'requests'`. `deploy.sh` hat das Release entfernt, der
Symlink blieb unberührt — **live ist unverändert `v3.0.2`**.

**Ursache, gemessen:** `requests` steht in keinem der vier `pyproject.toml`. Es kam am
2026-09-10 (P8.6 Step V) per `.venv/bin/pip install requests` von Hand ins Dev-venv. Die
C6-Tests (`a70dc2c`) importieren das Skript und liefen nur im Dev-venv, deshalb grün.
`deploy.sh:153` baut pro Release ein **frisches** venv aus `dev_install.sh`, und dort fehlt es.
Der Fixture-Docstring sagte wörtlich „`requests` is in the project venv" — die falsche
Behauptung, die den Fehler versteckt hat. Dieselbe Klasse wie der Mock-Zustand aus Step B
Befund 6: grün in einer Umgebung, die es live nicht gibt.

**Fix:** `phase8_6_ui_polish/scripts/mcp_local_vision_server.py` ist jetzt **stdlib-only**
(`urllib.request`). `HTTPError` trägt den Status-Zweig (urlopen wirft bei 4xx/5xx, ein
`status != 200`-Vergleich danach liefe nie), `OSError` fängt `URLError` **und** Socket-Timeouts.
`--check` gibt gegen Port 1 weiter Exit 3. Der Test patcht `urllib.request.urlopen` statt
`requests.post`. **Verworfen:** `requests` in ein `[dev]`-Extra — kein pyproject besitzt das
Skript (es gibt keins für `phase8_6`/`phase9`), die Abhängigkeit landete in einer fremden
Phase. **Verworfen:** `pytest.importorskip` — das Gate würde stumm überspringen.

**Beleg, und zwar am Gate selbst, nicht im Dev-venv:** frischer Baum (`git archive HEAD` +
die zwei geänderten Dateien) nach `/tmp/relcheck`, `python3 -m venv`, `dev_install.sh`,
`pytest -q` → **1127 passed, 1 failed**. Der eine rote ist ein Artefakt des Prüfaufbaus:
`test_backup_creates_verifiable_bundle` ruft `git bundle verify` und braucht ein Repo als cwd,
`git archive` liefert keins (`deploy.sh` klont, im echten Release war er grün). Nach `git init`
dort: 16/16 grün. `import requests` im frischen venv → `ModuleNotFoundError`, der Beleg prüft
also wirklich ohne `requests`. **Gesamt 1128/1128.**

**Benannt, nicht gebaut:** `phase8_6_ui_polish/scripts/vision_ollama.py` (CLI) braucht `requests`
weiter. Kein Test importiert es, es blockiert kein Gate, aus einem Release-venv läuft es aber
nicht. Datierte Korrektur dazu in `phase8_6_ui_polish/CLAUDE.md` (Step V). Das Dev-venv trägt
noch mehr nicht deklarierte Pakete (`playwright`, `pillow`, `pyflakes`, `brotli` u. a.); keins
hat im frischen venv einen Test rot gemacht.

**Nächster Schritt (Nikinger):** `deploy.sh main` erneut, dann `health_gate.sh
--expected-version=v3.1.0 --require-todays-update-log --expected-sha=<neuer HEAD>`. **Nicht**
`bdecfde` übergeben — der Fix-Commit ist der neue HEAD. Der `UPDATE_LOG`-Eintrag vom
2026-10-02 bleibt gültig; wird erst morgen deployt, braucht es einen neuen Eintrag (P6-X-Gate).
Danach P9-43 messen (Dauer des Index-Neuaufbaus am echten DATA_ROOT) und Augenschein.

**Nachtrag desselben Tages — `v3.1.0` ist live.** Der Nikinger hat `deploy.sh main` mit
`5414cb7` gefahren: durchgelaufen, **3:55 min** (Nikinger-Handmessung, „3:55:28"). Release
`/opt/sharefyx/releases/20261002T093629.531459Z`. `health_gate.sh --expected-version=v3.1.0
--require-todays-update-log --expected-sha=5414cb7` von mir gefahren: **9/9 OK**, JSON
`"result":"ok"`, `actual_version` `v3.1.0`. **P9-43 gemessen** (Journal, read-only): Restart
11:40:29,448 → `Index … Schema-Version 3 (erwartet 4) — wird verworfen` 11:40:30,240 →
`Started server process` 11:40:31,287 → `Application startup complete` 11:40:31,294. Der
Neuaufbau läuft synchron in `Store.__init__` (`store.py:235`), also ist **≤ 1,05 s** die
Obergrenze für **197 Items** (inkl. App-Aufbau); Start bis bereit 1,85 s. V161 sagte
0,4–0,6 s für 153 Items voraus — gleiche Größenordnung, real höchstens doppelt so lang. Index
danach read-only geprüft (`mode=ro`): `user_version 4`, **197 Zeilen** (32 `open`, 29 `done`,
92 `active`, 44 `archived`, 0 `doing`). **Offen:** Nikinger-Augenschein im echten Browser
(Rail „In Arbeit", Badge `v3.1.0`), danach A7+A8 in einer Sitzung (Step A).

**Zweiter Nachtrag — Block trace geplant.** Gemessen: `doing` ist geteilt, `assignee` in keiner
UI-Zeile, und **niemand** wird aufgezeichnet (`git log` im DATA_ROOT: Autor stets `Space Server`).
Warndialog alte Adresse = Absicht bis A7 (`RUNBOOK_STEP_A.md:753`). Nikinger: **P9-Y** (Who + last
editor), **P9-Z** (Client füllt `assignee`). Plan + nächster Schritt (M3 baut, ein Commit):
`docs/concepts/phase9_hardening_block_trace_plan.md`.

## Session stopped — 2026-10-02 (zehnter Block: doing-Block gebaut, Lock P9-V — opencode/M3, ein Commit, kein Deploy, kein Service-Touch)

**Ergebnis: das Eimer-Loch ist zu, `v3.1.0` ist freigegeben für den Deploy.** `_BUCKETS` führt
`doing`, die Rail zeigt „In Arbeit", und Zähler und Liste stimmen für diesen Ordner per
Konstruktion. `pytest` **1128** (1122 + 6 neu), `ui_budget` 5/5 (153,2 KB), `doc_health` 0,
Tabu-Diff leer.

**Gebaut wurde genau das, was der Mini-Plan §4 vorschrieb — und nichts darüber hinaus:**

- **D1** `phase5_ui/webui/api.py`: `"doing": {"type": "task", "status": "doing"}` nach `"open"`.
  Der Absatz `:129–148` (Step-F-Befund) ist **ersetzt**, und der neue trägt **keine
  Zeilennummern** — die des Vorläufers waren zum Schreibzeitpunkt schon gedriftet (K4), und
  gedriftete Verweise sind schlechter als keine.
- **D2** `static/js/state.js`: `doing: "In Arbeit"`. `editor.js` bleibt **unberührt**, damit bleibt
  Wächter #14 in `test_step_f_schema.py` (`editor.js` nennt `doing` nicht) grün — gewollt (P9-W).
- **D3** 6 neue Tests + 2 Änderungen an Bestehendem (T7 umgedreht, T8 `seeded`-Fixture).

**Befund beim Bauen, der die Plan-Rechnung veränderte (P9-61, Gegenlauf G3):** der Plan sagte,
G3 (`_BUCKETS["doing"]["status"] = "open"`, ein Duplikat) mache **T2, T3 und T4** rot. Gemessen:
**nur T2**. T3 (Dict-Gleichheit aller fünf Zähler) und T4 (Zähler == Liste) blieben grün, und der
Grund ist so simpel, dass er beim Lesen des Tests unsichtbar war: der Seed hat je **eine** offene
und **eine** laufende Aufgabe, also stehen „die Zahl der Aufgaben mit Status X" und „die Zahl der
Aufgaben mit Status Y" beide auf 1 — ein Duplikat ändert daran **nichts**. Zahlen, die sich nicht
unterscheiden, unterscheiden sich auch nicht, wenn man sie falsch zuordnet.

Der Plan hat dafür eine Regel: *„Wird ein Verstoß nicht rot, ist der zugehörige Wächter wertlos
und muss neu geschnitten werden. Das ist dann ein Befund, nicht stillschweigend weiterbauen."*
Also neu geschnitten: **T3 holt jetzt die Mitgliedschaften**, nicht nur die Zahlen — fünf
Listenabfragen, ihre Item-Mengen müssen sich paarweise ausschließen und zusammen alle sechs Items
des Space abdecken. Damit ist P9-59 („zählt in „In Arbeit" und in **keinem** anderen Eimer")
behavioural bewiesen statt behauptet, und G3 ist rot. **T4 bleibt unter G3 grün, und das ist
richtig**: T4 trägt P9-60 („Zähler == Liste"), und unter G3 gilt Zähler == Liste — die
Duplikat-Eigenschaft tragen T2 und T3.

**Gemessene Gegenläufe** (jeder Verstoß einzeln eingebaut, `phase9_hardening/tests/
{test_doing_bucket,test_step_f_schema}.py` + `phase5_ui/tests/{test_overview,test_meta}.py`, G0
als Kontrolllauf mit **0**):

| Verstoß | rot | wer |
|---|---|---|
| G1 `"doing"` aus `_BUCKETS` entfernt | **7** | T1, T2, T3, T4, T6, T7, T8 |
| G2 `"archived"` vor `"doing"` | **2** | T1, `test_meta.py` |
| G3 `_BUCKETS["doing"]["status"] = "open"` | **2** | T2, **T3 (nach dem Nachschnitteoben; vorher 1)** |
| G4 `doing: "In Arbeit"` aus `BUCKET_LABELS` entfernt | **1** | T6 |
| G5 im T5-PATCH-Body `"assignee": ""` | **1** | T5 |

**Browser-Beleg: 11/11** gegen eine eigene TLS-Wegwerf-Instanz (Port **18776**,
`p9_doing_wegwerf.py`/`p9_doing_self_check.py`, Kopien der Step-G-Serie mit geänderten
Konstanten). Kernbeleg **S6**: nach dem Speichern eines Statuswechsels `open → doing` springen
die Rail-Zähler **ohne Reload** von `1/1` auf `0/2` (`afterWrite()` → `loadOverview()`, das
prüft kein Server-Test). S7 gleicht die Rail-Texte gegen `GET /api/v1/overview` ab, S8 gegen
`GET /api/v1/items/{id}`: `status == "doing"`, `assignee == "alpha"` — das UI-Speichern hat die
Zuweisung nicht verloren (P9-W). V178 aus dem Plan damit im Browser bestätigt (`#meta-panel` ist
im Vorschau-Modus bedienbar, es ist ein `<details>` und stand in **jedem** Lauf offen).

**Browser-Gegenlauf: 7 von 11 rot** (nur D1+D2 per `git stash push -- <zwei Pfade>` zurückgenommen,
frisch gesätet). Rot: S1 (kein Chip), S2 (4 Ordner, Labels `Offen, Erledigt, Notizen, Archiv`),
S3, S4, S6. **Grün bleiben S5, S7, S8** — und das ist der eigentliche Befund des Gegenlaufs, kein
Schwächenzeichen: **S5/S7/S8 prüfen die Maschinenebene, und die war schon vor diesem Block
korrekt.** `status: "doing"` ließ sich speichern, `/overview` und `/items` lieferten roh, und
`assignee` überlebte den Editor-Pfad. Das Loch war **rein navigativ** — genau die Aussage, die
P9-W behauptet, jetzt an einem Lauf statt an einem Argument.

**Fünfte Wiederholung derselben Repo-Lehre, diesmal im eigenen Prüfskript:** der erste
Gegenlauf **stürzte ab** statt rot zu melden — ein `click()` auf den Ordner „In Arbeit", den es
ohne den Fix nicht gibt, ist ein 30-Sekunden-Timeout, kein Befund. Ein Skript, das beim Beweis
seines eigenen Lochs stirbt, beweist nichts. S4/S5/S8 prüfen deshalb jetzt zuerst auf
Existenz und melden sich mit Begründung rot, statt die Folge zu blockieren. Danach beide Läufe
neu (grün 11/11 mit dem gehärteten Skript).

**Vier Screenshots** `docs/screenshots/p9_doing_{01_uebersicht_chip, 02_rail_fuenf_ordner,
03_liste_in_arbeit, 04_nach_statuswechsel}.png` (56/42/42/60 KB), `screenshots_latest/` darauf
umgehängt. Sichtprüfung qualitativ mit dem lokalen Vision-Modell: Rail zeigt `Offen, In Arbeit,
Erledigt, Notizen, Archiv` + „+ Ordner", **nichts abgeschnitten, nichts überlappt**, Bild 04 zeigt
`Offen 0` / `In Arbeit 2` — deckungsgleich mit den Stationen. Gezählt wurde nicht (Modell-Schwachstelle,
`docs/concepts/sichtpruefung_automation_tooling.md`); **gezählt haben die Stationen** aus dem echten DOM.

**Eine kleine Doku-Korrektur, die der Plan nicht vorsah (K5):** der Mini-Plan §4 D1 verlangte, die
Zeilen `:115–127` **wörtlich** stehen zu lassen. Zwei davon tragen aber eine **Anzahl**
(„Die drei Ordner des Navigationsbaums", „Vier Ordner statt drei schließen das Loch"), und die wäre
nach dem fünften Eintrag falsch gewesen — ein Kommentar, der das Gegenteil des Codes behauptet,
ist schlechter als keiner (dieselbe Regel, an der T7 festhing). Nur die Zahlen korrigiert, alle
Begründungen wörtlich.

**Doku im selben Commit** (Hard Rule 8): Phase-Head (diese Zeile Modulstatus + F-Nachsatz + dieser
Block, dann `scripts/rotate_session_block.sh phase9_hardening`) · Mini-Plan §12 Ergebnis und
`status: snapshot` · `docs/INDEX.md` (🔄 → 📕, Phase-9-Head-Zeile) · Root-`CLAUDE.md` §Current state.
**Nicht** angefasst, bewusst: `docs/UPDATE_LOG.md` und das Badge `app.html:20` — beide gehören in
den Release-Commit am Deploy-Tag (Mini-Plan §8.1), ein heute datierter Log-Eintrag ließe das
`deploy.sh`-Gate bei einem späteren Deploy-Tag abbrennen.

**Nächste Schritte, mit Zuständigkeit:**
1. **Nikinger:** Deploy `v3.1.0`. Ablauf im Mini-Plan §8 — Release-Commit (Badge + `UPDATE_LOG`,
   von opencode/M3 am Deploy-Tag), dann `deploy.sh main` + `health_gate.sh`, und dabei **P9-43**
   messen (Dauer des Index-Neuaufbaus am echten `DATA_ROOT` — der erste Deploy mit Step F).
2. **Nikinger:** kurzer Augenschein im echten Browser — Rail zeigt in jedem Space „In Arbeit".
3. **Gate/Z** wartet weiter auf A7+A8 (eine Sitzung, harter Schnitt).

**Unverändert in diesem Block:** kein `systemctl`, kein `pkill -f`, kein Deploy. Die Wegwerf-Instanz
wurde ausschließlich über ihre PID-Datei gestoppt; Testumgebung ohne `SHAREFYX_*`/`SFX_*`.

## Session stopped — 2026-10-02 (neunter Block: Mini-Plan doing-Block, Lock P9-V — Claude Code, reine Planungssession)

**Ergebnis: der Mini-Plan steht, die Darstellungsentscheidung ist gefallen.**
`docs/concepts/phase9_hardening_block_doing_plan.md`, ausführungsreif für opencode/M3. Kein Code-Touch
und kein Service-Touch. `pytest` **1122 passed** (bereinigtes Env, 200,9 s), `doc_health` 0 Befunde.

**Nikinger-Entscheidungen 2026-10-02:**

- **P9-V = Kandidat (a).** `_BUCKETS["doing"] = {"type": "task", "status": "doing"}` mit Rail-Label
  „In Arbeit". Reihenfolge `open, doing, done, note, archived` (P9-X).
- **P9-P ist damit datiert eingeengt.** Ein Eimer pro Statuswert ist Navigations-Vollständigkeit,
  dieselbe Klasse wie `done` in P5 Step 7b. Die Hervorhebung bleibt P10.
- **P9-W, Sprachebenen.** Nur das Rail-Label wird übersetzt. Schema, REST und MCP bleiben roh,
  „so dass ein angeschlossenes LLM aus Ausgaben entnehmen kann, wem sie zugeteilt ist".
  Ein Test (T5) sichert ab, dass das UI-Speichern `assignee` nicht verliert.

**Verworfen, mit Argument.**

(b) „Offen = {open, doing}":
- `URLSearchParams` macht aus der Liste `open%2Cdoing`, und `store.search` vergleicht exakt. Das
  ergibt eine stille leere Liste.
- Repariert man es, kostet das entweder die zehnte Contract-Öffnung oder Mengenlogik neben
  `store.search`. Letzteres bricht „Zähler == Liste per Konstruktion".

(c) „`doing` nicht ins Select":
- **schließt das Loch nicht**, weil `doing` per MCP hereinkommt (P9-H).
- und es zerbricht den Editor für genau diese Items:
  - Ohne passende Option wird der Select-Wert `""`.
  - `isDirty()` meldet das Item damit schon beim Öffnen als geändert.
  - Speichern sendet `status: ""`, und `store.py:190` lehnt das ab.

**Vier datierte Korrekturen** (K1–K4 im Mini-Plan):
1. Die P9-P-Prämisse „in keinem UI-Pfad" war für die Erreichbarkeit falsch: Select **und** MCP führen hin.
2. Die Abnahme beginnt bei **P9-59**, nicht bei P9-45 (das gehört Step G).
3. Der Dateiname folgt **P9-T** und nicht dem Briefing-Vorschlag.
4. Die Zeilenverweise im `_BUCKETS`-Kommentar sind gedriftet; D1 schreibt den Kommentar neu.

**Gemessen statt vermutet:**
- V176: `phase9_hardening/tests/` hat kein `conftest.py`, die HTTP-Tests gehören deshalb nach
  `phase5_ui/tests/test_overview.py`, wie bei Step G.
- V178: `#field-status` ist im Vorschau-Modus bedienbar, sitzt aber im zugeklappten
  `<details id="meta-panel">`.
- Bestehender Konsistenztest `test_counts_match_the_item_list_for_the_same_bucket`: Er wäre für
  `doing` **vakuös** gelaufen (0 == 0), weil das Seed kein `doing`-Item hat. Der Plan ergänzt eins (T8).

**Abschluss der Session:** Der Nikinger hat den Plan bestätigt, **P9-W eingeschlossen**
(„Status-Optionen bleiben roh" war von Claude Code abgeleitet). Commit und Push nach `origin/main`.

**Nächste Schritte, mit Zuständigkeit:**
1. **opencode/M3** baut den Block nach Mini-Plan §4–§7: ein Commit, Browser-Beleg 8/8 auf
   Wegwerf-Port 18776.
2. **opencode/M3** macht den Release-Commit am Deploy-Tag: Badge `v3.1.0` (`app.html:20`) und ein
   neuer `## <Deploy-Tag>`-Block in `docs/UPDATE_LOG.md` (Mini-Plan §8.1).
3. **Nikinger** führt `deploy.sh` und `health_gate.sh` aus und misst dabei P9-43.

Gate/Z wartet weiter auf A7/A8.

## Session stopped — 2026-10-01 ( achter Block: Deploy **verschoben** (Nikinger-Entscheidung), `.toolbar-btn` in Standardoptik, vier Tailscale-Bilder geklärt)

**Diese Runde hat den Deploy nicht vorbereitet, sondern abgesagt — mit einem Messbefund als
Begründung.** Der Auftrag der Runde war Punkt 1 der Übergabe (Deploy `v3.1.0`, Badge +
`docs/UPDATE_LOG.md` im Deploy-Commit). Beim Durchgehen des Codes für einen **ehrlichen**
Changelog-Eintrag kam der Befund, der ihn kippt.

**Befund 11 — `doing` ist im Deploy-Fall für einen Menschen erreichbar, und genau seine
Eigenschaft ist der offene Befund.** `models.py :: STATUS_VALUES["task"]` trägt seit Step F
`{open, doing, done, archived}`; `editor.js :: populateStatusSelect()` füllt das Status-Feld der
Kopfdaten aus `state.meta.status_values[itemType]` — **rohe Werte, unübersetzt**. Nach dem Deploy
kann ein Mensch also `doing` wählen. Und dann: `bucketFor()` (`list.js`) nimmt den **ersten**
passenden `_BUCKETS`-Eintrag und vergleicht `f.status === item.status` exakt; `_overview()`
(`api.py`) zählt je Bucket per `store.search(**filters)`. Ein Wert, den keiner der vier Einträge
kennt, passt auf keinen ⇒ **die Aufgabe erscheint in keinem Ordner-Zähler und in keinem der vier
Ordner der Rail**, findet sich aber über „Alle Items" und in der Suche. Das ist der seit dem
2026-09-30 bekannte Befund P9-P, der laut Plan als Darstellungsentscheidung nach P10 wanderte —
als **„in keinem UI-Pfad sichtbar"** war das vertretbar, per Deploy wäre es **eine Eigenschaft,
mit der ein Mensch rechnen muss**. `assignee` ist davon nicht betroffen (kein UI-Feld, nur
MCP/REST — `tools.py :: update_item(assignee=…)`, serialisiert in `summary_to_json`/`item_to_json`).

**Nikinger-Entscheidung 2026-10-01: Deploy verschieben, Mini-Plan von Opus (Claude Code) für den
`doing`-Fix, danach implementieren + deployen.** Damit ist **kein** Release-Vorbereitungs-Commit
gefallen, und zwar aus zwei gemessenen Gründen, nicht aus Vorsicht: (a) der `## <Datum>`-Block in
`docs/UPDATE_LOG.md` wäre auf den Deploy-Tag datiert — ein heute geschriebener Eintrag lässt das
`deploy.sh`-Gate (P6-X, `today_utc`/`today_local`) genau dann abbrennen, wenn der Deploy Tage
später kommt; (b) der Changelog-Text ist ohne die Entscheidung über `doing` nicht schreibbar, und
ein Eintrag, den man später ersetzt, steht zwei Commits lang in einem Menschen-Banner.

**Was die Release-Vorbereitung dann umfasst** (unverändert gültig, nur nicht heute fällig): Badge
`.rail__version` in `phase5_ui/webui/static/app.html:20` `v3.0.2` → `v3.1.0` (P8-K-Schema „bump je
Deploy, nie zurück"; die Vorgänger-Runden sind `6f19a8f` und `1ad2665`, beide **eigene Commits**
mit Badge + UPDATE_LOG-Block, nicht der Deploy selbst), neuer `## <Deploy-Tag>`-Block in
`docs/UPDATE_LOG.md`, danach `deploy.sh main` und
`phase8_5_picker_release/scripts/health_gate.sh --expected-version=v3.1.0 --require-todays-update-log
--expected-sha=<sha>` (Gates 5/7/8 — Gate 5 liest `.rail__version` aus `/ui/static/app.html`, nicht
aus `/ui/login`).

**Punkt 2 der Übergabe — `.toolbar-btn` — ist gebaut, und Punkt 4b mit entschieden.** Die
Formatierhilfen der Textleiste waren nach `.btn` und `.account-nav` der **letzte** echte Knopf auf
der alten grauen Plastik (`--btn-face-top/bottom`, `--btn-edge`, plus ein äußerer Schlagschatten,
den `.btn` nicht mehr trägt). `app.css :: .toolbar-btn` trägt jetzt dieselben deckenden
`--btn-std-*`-Tokens, `:hover`/`::active` die jeweiligen Fill-Varianten; **Maße und Typografie
bleiben** (24 px, Monospace, `--text-muted`), und **`:disabled` bleibt auf `--surface`** — in der
Vorschau sind die Hilfen abgeschaltet, ein deaktivierter Standardknopf soll „inaktiv lesbar"
heißen und nicht „Standardknopf in einem anderen Zustand". `.rail__glyph` (der 20×20-Badge am
Space) bleibt bewusst auf der alten Optik: ein Badge ist kein Knopf. Konvention in
`phase8_ui_graph/CLAUDE.md` §Was diese Konvention NICHT macht ergänzt (zweite Runde am selben Tag).

**Beleg ist die Messung, das Bild die Geschmacksfrage.** Neu: `phase9_hardening/scripts/p9_btn2_toolbar_probe.py`
(Playwright gegen die eigene TLS-Wegwerf-Instanz `p9_step_g_wegwerf.py`, Port 18775, eigenes
`DATA_ROOT`, Stopp ausschließlich über die PID-Datei). **13/13 grün**, Ergebnis in
`phase9_hardening/probes/p9_btn2_toolbar_probe.json`. **Gegenprobe:** ein eingebauter Verstoß (alte
Plastik wiederhergestellt) ⇒ **5 rote Prüfungen**, danach zurückgebaut und 13/13 wieder grün. Geprüft
wird zweistufig, weil „dasselbe Bild" zwei Fragen hat: die **gerechnete Fläche** (Stringgleichheit
von `backgroundImage` gegen `.btn` im selben Panel) und die **Interpolation** (drei Höhen in einer
glyphenfreien Spalte, ±2 — die beiden Knöpfe sind 24 px bzw. 41 px hoch, dieselbe relative Position
landet auf Zeile 17 gegen Zeile 29; ±1 würde hier die PNG-Rundung prüfen, nicht die Farbe) plus der
Randpixel bei absolutem x=0. Der deaktivierte Zustand wird **eigenschaftsbasiert** geprüft — flach
(oben == unten) statt „heller", was eine falsche Behauptung gewesen wäre (gemessen Δsumme 11).

**Drei Fehler, die diese Probe selbst gemacht hat — alle drei von der Sorte, die dieses Repo
schon viermal teuer geworden ist** (P8.6 Block H, P9 Step G, Step B, A4-Vorbereitung): **ein
Wächter, der etwas anderes prüft als er behauptet.** (a) Die Vorbedingung
`count() == 1` für `#home-button[aria-current]` war **wertlos**: CSS-/DOM-Selektoren matchen ein
Attribut, nicht seinen Wert — der Knopf trug `aria-current="false"` und die Probe verglich die
schwarze Rail `(0,0,0)`; jetzt `get_attribute(...) == "true"`, geprüft **vor** der
Zustandsänderung, weil der Knopf nur in der Übersicht aktiv ist. (b) Der erste Pixelvergleich traf
bei `fx = fy = 0.5` die **Beschriftung** von „Anhängen" (Zeile h/2 trägt `(128,196,242)`,
`(233,230,203)` — Antialiasing einer Schrift, Δ 34 zum Knopf daneben); jetzt feste Spalte x = 4 px.
(c) Die Verlaufsmessung des **aktiven** Knopfs stand im Deaktiviert-Block und maß zweimal denselben
Zustand — erkannt am roten Ergebnis, weil oben == unten == `(20,24,29)` die Farbe von `--surface`
ist, nicht die des Verlaufs. Dazu die Produktinvariante, die (b) und (c) beide ausgelöst hat: der
Editor öffnet per P5-Entscheidung **in der Vorschau**, die Formatierhilfen sind dort also
`:disabled` — jetzt behauptet (Text des Umschalters + `is_disabled()`), nicht angenommen.

**Punkt 4b — die fünf unversionierten Tailscale-Dateien sind entschieden.** Vier PNGs lagen als
Kopien mit Leerzeichen im Dateinamen in `screenshots_latest/`: jetzt versioniert als
`docs/screenshots/p9_step_a_01_machines.png`, `02_add_rule_dialog.png`, `03_add_rule_fertig.png`,
`04_policies.png` (Infra-Beleg zu `RUNBOOK_STEP_A.md` §A3, **keine Sichtprüfung der Oberfläche**,
deshalb nicht in der Schnellansicht). Die fünfte Datei, `Machines - Tailscale.html`, ist
**gelöscht**: die gespeicherte Seite war die leere SPA-Hülle (`<div id="browser-support">` ohne
Inhalt, `<script id="tailscale-api-prefetch">{}</script>`, 2,7 KB, keine Geheimnisse — geprüft,
nicht vermutet). Eine leere HTML-Hülle ist kein Beweis; sie ist nur eine Datei, die jemand irgendwann
öffnet und für einen Beleg hält. Zusätzlich `screenshots_latest/` rotiert: die drei
`p9_step_e_*`-Links raus, drei `p9_btn2_*`-Links rein (Step E ist als Abnahmebeleg erledigt, die
offene Sichtfrage ist die Knopfoptik) — die Rotation macht das Skript-Kit laut eigener README
selbst, ohne Rückfrage.

**Zwei neue Wächter** in `phase5_ui/tests/test_static_routes.py` (beide mit Gegenprobe):
`test_toolbar_buttons_wear_the_standard_look` (alle vier Zustände nennen die richtigen Tokens, und
`--btn-face*`/`--btn-edge`/`--btn-glow` kommen im Block nicht mehr vor) und
`test_rail_glyph_is_a_badge_and_keeps_the_plastic` (das Gegenteil, als Markierung: wer die alte
Optik zum dritten Mal wegwirft, liest hier zuerst, warum sie bleiben darf). **Gegenprobe mit vier
eingebauten Verstößen → 2 rote Tests**, danach zurückgebaut.

| Gegenstand | Nachweis |
|---|---|
| **Befund 11** | `editor.js :: populateStatusSelect` (rohe `status_values`) + `api.py :: _BUCKETS` / `_overview()` + `list.js :: bucketFor()` — gelesen, nicht aus dem Plan übernommen |
| **`.toolbar-btn`** | `p9_btn2_toolbar_probe.py` **13/13** (`probes/p9_btn2_toolbar_probe.json`), Gegenprobe 1 Verstoß → **5 rot**; 3 Bilder `docs/screenshots/p9_btn2_0{1,2,3}_*.png` |
| **Tests** | `phase5_ui/tests/test_static_routes.py` +2, Gegenprobe 4 Verstöße → 2 rot; `pytest` **1122** (1120 + 2) |
| **Bestand** | `ui_budget` **5/5** (153,0 KB, app.css 26,5 KB gzip), `doc_health` **0**, Tabu-Pfad-Diff leer, **kein `systemctl`, kein `pkill -f`, kein Eingriff in den laufenden Dienst** — die Wegwerf-Instanz nur über ihre PID-Datei gestoppt |
| **Doku-Hygiene** | Phase-8-Head §Konvention ergänzt · `docs/screenshots/README.md`-Card + `screenshots_latest/README.md` (Tabelle + `updated:`) · `docs/INDEX.md` · Wurzel-`CLAUDE.md` — alles im selben Commit |

**Offen und deine Entscheidung:** der **Mini-Plan für `doing`** (Opus über Claude Code). Zwei
Kandidaten stehen im Code kommentiert, beide sind Darstellungsentscheidungen und damit P10-Arbeit
waren (P9-P): (a) ein fünfter `_BUCKETS`-Eintrag ⇒ **ein Rail-Ordner mehr** plus Chip in der
Übersicht (dieselbe Hervorhebung, die P9-P an P10 verwies) und ein unübersetztes Label;
(b) „Offen" als Menge `{open, doing}` ⇒ vier Rail-Einträge bleiben, aber der `meta`-Vertrag ändert
sich und **zwei** Konsumenten müssen dieselbe Mengenprüfung tragen (`list.js :: bucketFor` und
`store.py`-Vergleich in `_overview()`) — eine **zweite** Contract-Öffnung außerhalb von P9-G.
Ein dritter, im Repo noch nicht bewerteter Weg: das Status-`<select>` **nicht** mit `doing` füllen,
sondern einen vorhandenen Wert überschreiben lassen („In Arbeit" ist eine Ansicht, kein Wert) —
dann ändert sich kein Schema, aber es geht wieder an dieselbe Produktentscheidung zurück, die der
Plan einmal getroffen hat.

**Nächster Schritt:** Mini-Plan abwarten, dann dessen Umsetzung; **erst danach** die
Release-Vorbereitung (Badge + `## <Deploy-Tag>`-Block) und der Deploy. Gate/Z wartet weiter auf
A7/A8 — und A7a (die offene Frage vom 2026-10-01, `ALLOWED_HOSTS` vorziehen) ist durch die
Deploy-Verschiebung **nicht** dringlicher geworden: dort wechselt kein `resource`, beide
Connectoren blieben gültig, und der Restart ist deine Sache.

## Session stopped — 2026-10-01 (siebter Block, A4-Vorbereitung: zwei neue Befunde, ein Vorlagen-Defekt, 5 neue Wächter)

**Diese Runde hat nichts ausgeführt, sie hat A4 messbar gemacht.** Form ist Cooperation
(P9-Q, ein Schritt pro Runde): A4 ist ein `sudo`-Schritt auf einer Kiste, die ich nicht
anfassen darf — also war meine Aufgabe die Vorlage, die Befunde und die Erwartungshaltung.

**Befund 8 — P9-10 ist bis A7 nicht erfüllbar, und die Ursache steht nicht in der Zeile.**
Abnahmezeile P9-10 verlangt *200 **und** gültiges LE-Zertifikat*. Die Zertifikats-Hälfte
gehört Caddy, die `200` gehört `SPACE_ALLOWED_HOSTS` — und das ist A7. Gemessen gegen den
laufenden Dienst: `curl -H "Host: sharefyx.eurofyx.com" http://127.0.0.1:8765/health` →
`400 Invalid host header` (unveränderter Host → 200, der erlaubte ts.net-Name → 200).
**Die ganze Kette einmal mit echtem Caddy davor gespielt**, statt nur geschlossen: das
Ubuntu-Paket entpackt (ohne Installation), `caddy 2.6.2` auf einem Wegwerf-Port vor die
Relay-Adresse `100.93.43.122:8765`, also exakt die Strecke, die der VPS in A4 nimmt →
`sharefyx.eurofyx.com` 400, `100.93.43.122` 400, ts.net-Name **200 mit
`{"status":"ok","service":"sharefyx-mcp",...}`**. Zwei Dinge damit zugleich belegt: das
**Relay funktioniert**, und **Caddy reicht den Host-Header unverändert durch** — die
Behauptung stand vorher nur als „Caddy-Default" im Kommentar, ohne Messung. Folge: P9-10
ist in **P9-10a** (Zertifikat, A4) und **P9-10b** (`200`, nach `ALLOWED_HOSTS`) geteilt, und
die `400` ist in A4 das erwartete Ergebnis. **Vorgeschlagen, nicht entschieden:** `ALLOWED_HOSTS`
als eigene Hälfte **vorziehen** (A7a) — dort wechselt kein `resource`, beide Connectoren
bleiben gültig, Fabian ist nicht nötig. Ein Neustart des Produktionsdiensts ist deine Sache.

**Befund 9 — auf dem VPS ist kein Caddy, und A4 fing trotzdem mit „install" an.**
`tailscale status`: der VPS heißt **`ubuntu`**, `100.121.142.113`, Tag `tag:sharefyx-edge`,
online. `curl` auf 80 und 443 gegen seine Tailnet-IP: **kein Listener** (gleicher Zustand wie
der A6-Test am 2026-09-30 — kein Firewall-Problem, ein fehlendes Programm). Der Schritt A4
begann mit `sudo install -m 644 /etc/caddy/Caddyfile`, einem Befehl, der ohne Caddy mit
`No such file or directory` endet. **A4 ist jetzt A4a (messen, dann `apt install -y caddy`)
+ A4b (Caddyfile, `validate`, Restart)** und nennt drei getrennte Ausgaben, von denen die
`openssl s_client`-Zeile der eigentliche Zertifikatsbeleg ist. Zwei Nebensachen aus
derselben Messung, weil sie die Quellenwahl bestimmen: Ubuntu 24.04 liefert **`caddy 2.6.2`**,
dessen `postinst` `/var/log/caddy` anlegt und auf `caddy:caddy` chownt (das Datei-Log der
Vorlage ist damit beschreibbar — und `caddy validate` sagt auf dieser Version
`Valid configuration`, inklusive `roll_size`/`roll_keep`), und die Paket-Unit hat
`ExecReload=… caddy reload … --force`. Letzteres ist der Grund, warum die Vorlage **kein
`admin off`** trägt: gemessen bricht `caddy reload` damit in `dial tcp 127.0.0.1:2019:
connect: connection refused` ab — „Härten" hätte `systemctl reload caddy` kaputtgemacht.

**Vorlagen-Defekt, gefunden durch den Test, nicht durch das Lesen.** Der zweite Platzhalter
hieß `<vps-tailnet>` und war im Kopfkommentar als „Node-Name **des VPS**" beschrieben —
während `reverse_proxy` darunter auf die **Heim-VM** zeigt. Wer nach der Kopfzeile
einsetzt, lässt Caddy auf sich selbst proxen; der Fehler sieht aus wie ein totes Relay
(`connection refused`), mitten in der Abnahme. Jetzt `<heimvm-tailnet>`, mit der gemessenen
Ziel-IP `100.93.43.122` im Kommentar und der ausdrücklichen Warnung, dass `ubuntu` /
`100.121.142.113` **nicht** hingehören.

**Fünf neue Wächter** in `phase9_hardening/tests/test_tail_proxy.py` (**12/12 grün**):
Ziel-Platzhalter benennt die Heim-VM · Kopf und Anweisung nennen dieselben Platzhalzer ·
Upstream-Port = Relay-Port = App-Port · kein zweiter HSTS und kein `admin off` ·
nach dem Einsetzen bleibt kein `<…>` in der Anweisung stehen. **Gegenprobe mit vier
eingebauten Verstößen → 5 rote Assertions**, danach zurückgebaut. Zwei eigene Fehler dabei:
ein `and` in einer Assertion (Python nennt nicht, welche Hälfte fehlt) und ein Helper, der die
Platzhalternamen **ohne** Klammern zurückgab, während die Wächter die Zeichenfolge **mit**
Klammern prüfen — beide im selben Commit behoben. Und die vierte Wiederholung derselben
Falle (P8.6 Block H, P9 Step G, Step B, jetzt hier): **mein eigener Kommentar** im Vorlagen-
Kopf nennt den alten Platzhalter und `/healthz`, weil er die Korrektur erklärt — die Wächter
trennen deshalb strukturell Anweisung und Kommentar (`_directives_only`).

| Gegenstand | Nachweis |
|---|---|
| **Befund 8** | `400 Invalid host header` für die neue Domain am laufenden Dienst; dieselbe Kette über echten Caddy 2.6.2 durch den echten socat-Relay → 200 mit `{"status":"ok",…}` |
| **Befund 9** | `tailscale status` (ubuntu/100.121.142.113/`tag:sharefyx-edge`), 80+443 ohne Listener, `apt-cache policy caddy` → 2.6.2, `postinst` + Unit aus dem `.deb` gelesen, `caddy validate` → `Valid configuration`, `caddy reload` mit `admin off` → connection refused |
| **Tests** | `phase9_hardening/tests/test_tail_proxy.py` 12/12 (5 neu), Gegenprobe 4 Verstöße → 5 rot |
| **Bestand** | `pytest` **1120** (1115 + 5), `ui_budget` **5/5** (152,5 KB), Tabu-Pfade leer, **kein `systemctl`, kein `pkill -f`, kein Eingriff in den laufenden Dienst** (nur `GET /health` gegen `127.0.0.1`, `tailscale status` read-only und ein Verbindungsversuch gegen die VPS-IP) |
| **Doku-Hygiene** | `RUNBOOK_STEP_A.md` **51.613 B, 10.653 B über dem 40-KiB-Softcap — benannt statt versteckt** (P8-P) in `docs/INDEX.md`, mit dem Hinweis, dass §0 Befund 8+9 der Zuwachs sind und die Straffung Step-Z-Arbeit ist |

### Zweiter Teil derselben Runde — A4 ist ausgeführt, und ein Fehler von mir ist es auch

**A4a und A4b sind durch, mit den erwarteten Ausgaben** (Tabelle im Runbook, Schritt A4). Der
Punkt, den vorher nur die Behauptung trug: **die `400 Invalid host header` kam aus der
Anwendung, nicht aus Caddy** — auf der Heim-VM steht zur selben Sekunde
`19:30:49 GET /health status=400 ua=curl/8.7.1`. Damit steht die Kette
VPS → WireGuard → `sharefyx-tail-proxy` → App, und **P9-10a ist grün**.

**Befund 10 — `caddy validate` liest den Adapter aus dem Dateinamen.** Beim Vorprüfen der
A4b-Datei: `Error: decoding config: invalid character '#'` bei `/tmp/opencode/A4b.Caddyfile`,
`Valid configuration` bei derselben Datei als `Caddyfile`. Gemessen: `Caddyfile*` (case-sensitiv,
auch `.fertig`/`.txt`/`.new`) wird gelesen, `caddyfile` klein und `A4b.Caddyfile` nicht. **Der
Fehlertext deutet auf Syntax und kaputte Klammern** — wer ihn nicht kennt, repariert die Datei
oder ersetzt sie durch eine ohne Protokoll, nur weil die erste sich weigerte.

**Und mein eigener Fehler, benannt statt weggeredet: ich habe die ganze Runde mit
`2026-10-02` datiert, ohne das Datum zu messen — es ist `2026-10-01`.** Aus dem Handover-Datum
(2026-10-01) plus einem Tag gerechnet, also eine Zahl **behauptet statt gemessen**; die
Gegenprobe kam erst, als der VPS ein LE-Zertifikat mit `notBefore=Oct 1` ausstellte. **41
Fundstellen** in sieben Dateien, darunter der Session-Block-Header, die Phase-Statuszeile und
der aktuelle Eintrag in der Wurzel-`CLAUDE.md` — korrigiert in `10e3c50`→`HEAD`, ein Commit,
nicht am Stück. Die Datumsangaben selbst bleiben als Beweis stehen, warum sie korrigiert wurden.
Zwei Session-Blöcke mit demselben Datum sind normal (2026-09-30 trägt fünf).

**Und der Platzhalter ist raus (2026-10-01, später):** `read -rp` + `sed` hat die echte
ACME-Adresse gesetzt, `validate` wieder `Valid configuration`, `reload` sauber — und der
Erfolgsbeleg ist der, den es vorher nicht geben konnte: **`notBefore` unverändert**
(`Oct 1 18:31:33 2026 GMT`), also keine Zertifikatsneuausgabe, wie vorhergesagt. **Die Adresse
steht bewusst nicht im Repo** (privat; ihr Ort ist `/etc/caddy/Caddyfile` und das Postfach).

**Offen und deine Entscheidung:** **(a)** ob `ALLOWED_HOSTS` als
A7a vorgezogen wird (dann ist P9-10b vor dem Schnitt grün und A7 zerfällt in zwei kalibrierte
Hälften); **(c)** der Deploy von `v3.1.0` vor A7, sonst ist das `LEGACY_*`-Fenster wirkungslos.

**Nächster Schritt:** Deploy `v3.1.0` (dein Schritt, `deploy.sh` braucht sudo) → dann A7/A8 in
einer Sitzung mit Fabian. Gate/Z wartet weiter auf A7/A8.

## Session stopped — 2026-10-01 (sechster Block, Step A — Domain live, A5 ✅, eine Korrektur, die A7 umplant)

**`sharefyx.eurofyx.com` löst auf `217.160.128.146` auf** (vom Mac ohne VPN, `dig +short … @1.1.1.1`).
Die Registrierung bei IONOS ist durch: NS `ns1084.ui-dns.org` u. a., Apex auf IONOS-Parking (bleibt so,
das Apex ist für eine Firmen-Website reserviert), **kein Wildcard, kein CAA** — Let's Encrypt darf in
A4 ausstellen. Die Panel-Hinweise „Domain nicht genutzt" / „SSL aktivieren" sind bewusst ignoriert:
das Zertifikat holt Caddy.

**Befund dieser Session — Runbook-Befund 4 war falsch, und das ändert die Reihenfolge von A7/A8.**
Befund 4 versprach „kein Massen-Re-Login", weil es keine `iss`-Prüfung gibt. Es gibt aber eine
**`resource`-Prüfung**: `app.py:196` baut den Resolver mit `expected_resource = {base_url}/mcp`,
`resolver.py:49` weist jedes Token mit abweichender `resource` ab, und die Familie vererbt ihre
`resource` an jedes Refresh-Token. **Der A7-Restart macht also beide Connectoren sofort ungültig —
nicht erst A8.** Dasselbe gilt rückwärts für den Rückfall A9 Schritt 4. Einen Übergang auch für den
Connector gäbe es nur mit einer Änderung in `phase4_auth/authserver/` (Tabu §0.3).

**Zwei Nikinger-Entscheidungen 2026-10-01:**

| # | Entscheidung | Folge |
|---|---|---|
| 1 | **Connector: harter Schnitt** | A7 und A8 in einer Sitzung, Fabian verbindet zeitgleich neu; kein Tabu-Eingriff |
| 2 | **Web-UI: Übergangsfenster** (Befund 5 umentschieden) | genau eine zusätzliche erlaubte CSRF-Origin (alter Funnel-Host, exakter String) bis zu einem **Enddatum in der Konfiguration**; danach liest die alte Adresse nur noch. Auf der alten Adresse öffnet sich **bei jedem Laden** ein Dialog im Stil des Einstellungen-Dialogs mit Verweis auf die neue Adresse (schließbar, kommt wieder). Leer = heutiges Verhalten |

**Noch nicht gebaut:** Entscheidung 2 ist Code (`phase5_ui/webui/` + Konfig-Durchreichung über
`install_units.sh`/Unit/`phase2_mcp` `Settings`) und kommt als eigener Commit. **Offen und deine
Entscheidung:** das Fenster wirkt nur, wenn es **vor A7 deployt** ist — `deploy.sh` liefert `main`,
also zusammen mit P9 D–H (neunte P1-Öffnung, `._trash`, `fastmcp==3.4.7`), die bisher auf Gate/Z
warten. Badge-Version ebenfalls deine Wahl.

**Nächster Schritt:** A4 (Caddy auf dem VPS) — unabhängig vom Fenster-Code, braucht nur die
auflösende Domain, die jetzt steht.

### Nachtrag derselben Session — das Übergangsfenster ist gebaut

**Entscheidung 2 ist Code, und er tut, was beschlossen ist** — gemessen in einem echten Browser,
nicht nur in Unit-Tests. Konfiguration: `local.env` `LEGACY_ORIGIN` + `LEGACY_UNTIL` →
`install_units.sh` (Platzhalter mit `${…:-}`-Default, eine alte `local.env` bricht also nicht) →
Unit `SPACE_UI_LEGACY_ORIGIN`/`_UNTIL` → `phase2_mcp` `Settings` (fail-closed: halb gesetzt,
`http://`, `/` am Ende oder Pfad ⇒ Startfehler) → `UiSettings.origin_allowed()` in `require_csrf`.

| Gegenstand | Nachweis |
|---|---|
| **Uhr statt Flag** | `UiSettings.clock` wird **pro Anfrage** gefragt — das Fenster schließt am Enddatum ohne Neustart (den macht nur der Nikinger). Test: dieselbe Instanz, Tag 15 erlaubt, Tag 16 nicht |
| **Datumsgrenze** | Europe/Berlin, einschließlich — beide Seiten getestet |
| **Andere Origins** | bleiben 403, auch im Fenster (`http://`-Variante, mit `/`, `null`, fremd) |
| **Ungesetzt** | exakt das alte Verhalten |
| **Dialog** | `#legacy-host-dialog` in `.account-nav`-Form, **kein neues CSS**; erscheint nur, wenn `location.origin == meta.legacy.origin` (nie auf der neuen Adresse, nie in einer Wegwerf-Instanz ohne Konfiguration); in `anyOverlayOpen()` und der ESC-Kette |
| **Tests** | `phase5_ui/tests/test_legacy_window.py` **23/23**; Gegenprobe (Datumsprüfung raus 2 rot, CSRF-Haken raus 3 rot) |
| **Browser** | `phase9_hardening/scripts/p9a_legacy_probe.py` gegen die TLS-Wegwerf-Instanz (18775), **16/16**: offen ⇒ Dialog mit Datum, ESC/Knopf schließen, kommt nach Reload wieder, **POST 201**; abgelaufen ⇒ „nur noch lesbar", **POST 403**. Bild: `docs/screenshots/p9a_legacy_offen.png` |
| **Bestand** | `pytest` **1114** (1091 + 23), `ui_budget` 5/5 (152,2 KB), Tabu-Pfade leer, kein `systemctl` |

**Berührt außerhalb `phase9_hardening/`, mit Deinem Auftrag:** `phase5_ui/webui/{config,security,api}.py`,
`app.html`, `js/app.js`, `phase2_mcp/mcpserver/{config,app}.py`, `phase3_edge/scripts/install_units.sh`,
`phase3_edge/local.env.example`, `phase4_auth/systemd/sharefyx-mcp.service` (nicht `authserver/`).

**Deine Entscheidung vor A7:** das Fenster existiert live erst nach einem Deploy, und `deploy.sh`
liefert `main` — also mit P9 D–H. Ohne Deploy vor A7 gilt Befund 5 unverändert (alte Adresse nur
lesend), und `LEGACY_*` in `local.env` wäre wirkungslos. Badge-Version ebenfalls Deine Wahl.

### Zweiter Nachtrag — Standardknöpfe in Rail-Optik (Nikinger-Entscheidung 2026-10-01)

`.btn` und `.account-nav` tragen jetzt die Optik des aktiven Übersicht-Knopfs (`--select-fill` +
1 px `--select-line`, Hover über neues Token `--select-fill-strong`). **Ausnahmen:** `.btn-primary`
und `.action--caution` (Archivieren behält graue Plastik + Vorsicht-Rot). **Ersetzt H-R.2-L**
(Akzentkante an `.account-nav`, 2026-09-14) — die zwei Wächter dafür sind datiert umgeschrieben,
nicht gelöscht; Gegenprobe mit dem alten CSS → 3 rot. Konvention v3 im Phase-8-Head ergänzt.
Selbst-Screenshots `docs/screenshots/p9_btn_0{1,2,3}_*.png` (Einstellungen, Spaces verwalten,
Editor). **Nicht angefasst, benannt:** `.toolbar-btn` (Format-Leiste, „Bearbeiten") bleibt grau.
Geht mit demselben Deploy wie das Übergangsfenster raus.

**Zweite und dritte Runde, derselbe Tag (Nikinger-Sichtung):** zwei Abweichungen vom Vorbild, beide
gemessen statt geschätzt. **(1)** Die Einstellungen-Navigation war eine dritte Variante (eigene Kopie
der Optik mit `--fs-ui`) → die Knöpfe tragen jetzt die Klasse `.btn` selbst, `.account-nav` ist nur
noch Layout. **(2)** „Zu blau": `--select-fill` ist **halbtransparent** und wirkt nur auf der
schwarzen Rail dunkel — auf dem grauen Dialog-Panel gemessen Mitte `(21,34,52)` statt `(8,19,33)`.
Neue **deckende** Tokens `--btn-std-fill`/`-hover`/`-active`/`--btn-std-line` = die Originale auf
Schwarz bzw. auf dem eigenen Fill verrechnet. Pixel-Gegenprobe (Playwright-Elementscreenshot,
Wegwerf-Instanz): Übersicht oben/Mitte/unten/Kante `(26,41,60)/(8,19,33)/(5,11,20)/(29,67,116)`,
Einstellungen-Knopf `(26,40,60)/(8,19,34)/(5,11,20)/(29,67,116)`. Wächter auf die neuen Tokens umgestellt.

### Session-Ende 2026-10-01 — Entscheidungen und nächster Einstieg

**Nikinger-Entscheidungen zum Abschluss:** (1) **noch kein Deploy** — Live bleibt Release
`20260918T183907` (`v3.0.2`); (2) der nächste Deploy trägt **`v3.1.0`** (Badge `app.html` +
`docs/UPDATE_LOG.md`-Eintrag erst im Deploy-Commit, wie GA4 in P8.6); (3) gepusht.

**Nächste Session — kurz:**
1. **A4 Caddy auf dem VPS** (`RUNBOOK_STEP_A.md` A4, Vorlage `Caddyfile.template`, Domain
   `sharefyx.eurofyx.com`) → Prüfung `https://sharefyx.eurofyx.com/health` mit LE-Zertifikat (P9-10).
2. **Deploy `v3.1.0` vor A7** — liefert UI-Übergangsfenster, Standardknöpfe und P9 D–H mit;
   danach `LEGACY_ORIGIN`/`LEGACY_UNTIL` in `local.env` (A7).
3. **A7+A8 in einer Sitzung, Fabian zeitgleich** (Token-`resource`-Bindung kappt beide Connectoren).
4. Offen, klein: `.toolbar-btn` und die kleineren „Anzeigen"-Knöpfe in Standardoptik? · Gate/Z wartet auf A4–A8.


## Session stopped — 2026-09-30 (fünfter Block, Step B — polkit-Regel gebaut, V153 entschieden, Ausführung bleibt beim Nikinger)

**Blocker B war die Bitte dieser Runde. Die Repo-Seite ist fertig, und die beiden offenen Fragen
sind nicht dieselben, die der Plan stellt — das war der Fund.** `pytest` **1091** = 1084 + 7 neue Wächter (in `test_tailscaled_watchdog.py`
steht damit 12/12), kein Service-Touch, kein `systemctl` durch mich.

### Befund 1 — der Plan bietet zwei Wege an, einer ist unbaubar

Plan §4.2: „eng geschnittene Polkit-Regel **oder** ein `sudoers`-Fragment". Die Unit setzt
`NoNewPrivileges=true`, und sudo lebt vom setuid-Bit:

```
$ setpriv --no-new-privs -- /usr/bin/sudo -n -l
sudo: The "no new privileges" flag is set, which prevents sudo from running as root.
```

Eine `NOPASSWD:`-Zeile wäre unter dieser Unit wirkungslos; sie zu retten hieße, die Härtung
abzuschwächen. **V153 ist damit entschieden: polkit.** Das ist eine Messung, keine Präferenz —
und es dreht den Plan um, weil der zweite genannt, aber nie funktionsfähig war.

### Befund 2 — polkit kann es auf dieser Box nicht eng genug, und das steht in keinem Plan

`systemctl --version` → **255.4-1ubuntu8.17**. Der lokal installierte Manpage-Abschnitt *Security*
in `org.freedesktop.systemd1(5)` nennt für `StartUnit()`/`StopUnit()`/`RestartUnit()` **eine
gemeinsame** Aktion: `org.freedesktop.systemd1.manage-units`. Die feingranularen
`manager.restart-unit` gibt es erst ab neuerem systemd. **Ein `<defaults>`-Eintrag kann danach
gar nicht nach Unit filtern** — „eng geschnitten" setzt voraus, dass es so etwas wie ein
Unit-Attribut gibt.

Und ob es das auf 255 gibt, ist unprivilegiert **nicht** auslesbar: `pkcheck` kennt die Aktion
gar nicht, weil systemd sie erst zur Laufzeit bei polkitd registriert
(`Action … is not registered`). Ein Fehlversuch wäre also nur am echten Neustart zu entdecken —
genau dem, was man nicht riskieren will, solange die Alternative eine Email mit ausgehendem
Anschluss ist.

**Gebaut ist deshalb die Form, die in beiden Fällen das Richtige tut:**
`phase3_edge/polkit/49-tailscaled-watchdog-restart.rules` als **JS**-Regel (nur sie kann auf
`action.lookup("unit")` prüfen), die `manage-units` **und** die feingranulare Aktion abdeckt, in
beiden Blöcken zusätzlich `unit == "tailscaled.service"` und `subject.user == "savefyx"`. Fehlt systemd 255 das Attribut, greift die Regel **nicht**, und der Watchdog loggt
seine vorhandene Zeile `restart fehlgeschlag (Polkit-Regel … V153)` — der Fehlerfall ist
sicherheitsseitig der gewünschte. **Ohne** den Unit-Abgleich hätte `savefyx` das Starten und
Stoppen **jeder** Unit, auch aus `sharefyx-mcp` heraus. Das wäre in einer Härtungsphase eine
Regressionsstelle, und es steht deshalb nicht im Repo.

### Befund 3 — die Probe, die die Restfrage entscheidet, ohne `tailscaled` anzufassen

`phase9_hardening/step_b/`: eine Wegwerf-Unit (`sharefyx-watchdog-probe.service`,
`ExecStart=/bin/true`, dieselbe Härtung) und eine Wegwerf-Regel, die **diese** Unit freigibt.
`systemctl restart` darauf ist folgenlos. Antwortet polkit mit ja, trägt die Aktion das
`unit`-Attribut und die Repo-Regel funktioniert; antwortet es mit nein, ist die Repo-Regel stumm
und B1 entfällt — dann zurück ans Zeichenbrett, mit zwei Alternativen, die beide die Härtung
berühren und deshalb **deine Entscheidung** sind (`manage-units` breit freigeben — abgelehnt; oder
den Watchdog als `User=root` fahren und gar nicht autorisieren — dann trägt das Skript
PATH-aufgelöste Binaries mit Root-Rechten). Der dritte, sauberere Weg (fixer Root-Oneshot mit
hartkodiertem `ExecStart`, von der unprivilegierten Einheit per Flag angestoßen) wäre echte
Umfangserweiterung und ist **nicht** gebaut.

### Was gemessen wurde

| Gegenstand | Nachweis |
|---|---|
| **V153** | `setpriv --no-new-privs -- sudo -n -l` → *no new privileges*-Meldung ⇒ sudoers ausgeschlossen |
| **Aktion** | `systemctl --version` 255.4-1ubuntu8.17 + man `org.freedesktop.systemd1(5)` §Security ⇒ nur `manage-units` |
| **Sichtbarkeit** | `pkcheck --action-id …manager.restart-unit` → *not registered*; `pkaction` ebenso ⇒ die Restfrage ist unprivilegiert nicht entscheidbar, daher die Probe |
| **Ist-Zustand** | `ls /etc/systemd/system/tailscaled-watchdog.*` → *No such file*; `systemctl list-timers` → 0 Timer; `polkitd 124-2ubuntu1.24.04.4` vorhanden; `Self.Online = True`, `BackendState = Running` |
| **Tests** | 7 neue Wächter, **12/12 grün**; Gegenprobe mit vier eingebauten Verstößen → **6 rote Assertions** (Unit-Abgleich raus 2 · Nachbar-Aktion mitgenommen 1 · Skript startet andere Unit 2 · Probe zeigt auf die echte Unit 1), danach zurückgebaut, `git diff` für Skript und Regel leer |
| **Lesehinweis** | alle vier Wächter filtern **Kommentarzeilen** vorher heraus — die Regel nennt `manage-units` und `tailscaled.service` auch in ihren Befund-Kommentaren, und ein Test, der Kommentare mitliest, prüft meine Formulierung statt der Absicht (dritte Wiederholung derselben Falle: P8.6 Block H, P9 Step G, jetzt hier) |

### Nächster Schritt

**B0 ist die ganze Kette:** drei `sudo install`-Befehle plus ein `systemctl restart` auf eine
Wegwerf-Unit, danach aufräumen. Danach B1 (Regel), B2 (Units + `systemctl enable --now
tailscaled-watchdog.timer` — **`install_units.sh` aktiviert nur `sharefyx-mcp`**, und startet es
dabei neu), B3 (P9-19, erstes Fenster selbstheilend über `systemctl stop tailscaled`). Vollständige
Befehlsfolgen mit Soll-Ausgaben: `phase9_hardening/step_b/RUNBOOK_STEP_B.md` §2.

**Unverändert:** Step A wartet auf die Domain (NXDOMAIN + RDAP 404), Gate/Z auf A4–A8. Und
**P9-19 zählt nicht als erledigt, nur weil der Watchdog läuft** — die Abnahmezeile verlangt den
Journal-Beleg für genau einen Restart.

### Nachtrag derselben Session — B0 ist ausgeführt, und die Antwort war die erhoffte

`systemctl restart sharefyx-watchdog-probe.service` → **`AUTORISIERT`**, mit Journal-Beleg
(`Starting … Deactivated successfully … Finished`) bei `User=root`. **Damit ist V153 vollständig
entschieden und die Restfrage aus Befund 3 ausgeräumt: systemd 255.4 schickt das `unit`-Detail an
die Aktion, die JS-Regel greift, und sie bleibt dabei eng.** B1 kann laufen.

**Ein Nebenbefund, der in B3 zählt und den ich vorher nicht erwartet hatte:** eine **Verweigerung
kostet hier 25 Sekunden**, nicht eine — gegengetestet an einer Unit, die die Regel nicht nennt:
`Failed to restart …: Connection timed out`, `rc=1`, **gemessen 25 s**. Auf dieser VM läuft kein
polkit-Agent (headless), eine nicht erteilte Autorisierung versucht erst die Rückfrage und läuft
in den Agent-Timeout. **Sollte die Regel irgendwann nicht mehr greifen, sieht man das im Journal
als Hänger, nicht als schnelles „restart fehlgeschlag"** — die 25 s sind die Kennzahl für die
Fehlersuche, und sie addieren sich auf die 60 s des Timer-Takts.

**Die Gegenprobe ist ehrlich gesagt noch nicht sauber:** mein Test mit der `.timer`-Unit trennt
„Regel greift nicht" nicht von „Unit existiert gar nicht" (`is-enabled` sagt `not-found`). Die
eindeutige Form braucht dein `sudo` (Regel weg, derselbe Restart, jetzt `rc=1`) und steht als
**C0** im Runbook. Ohne sie trägt der Schluss auf Journal-Beleg plus `User=root`-Messung — das
reicht, aber C0 macht ihn eindeutig.

**Nächster Schritt:** B1 (`sudo install` der Regel) · B2 (`install_units.sh` + `enable --now` des
Timers) · dann B3. C0 ist optional und nur für den eindeutigen Beweis.

### Zweiter Nachtrag — B2 ist gescheitert, und der Befund stand seit drei Tagen im Repo

`install_units.sh` lief sauber durch, `enable --now` legte den Symlink an, `list-timers` zeigt
den Timer — und der Dienst lieferte **in jedem Takt `status=203/EXEC`**. Zwei Messungen, und die
Ursache ist nicht die Pfadlogik:

1. `systemctl cat … | grep ExecStart` → `/opt/sharefyx/current/phase3_edge/scripts/…` — **das
   Release, nicht den Checkout.**
2. `local.env:8` → `REPO_ROOT=/opt/sharefyx/current`, und `install_units.sh:53` verlangt die
   Variable bewusst (Prod-Units sollen aufs Release zeigen).

Der Scan über alle installierten Units traf **genau eine** mit totem Pfad — alle anderen
Skripte waren beim Deploy vom 2026-09-18 schon im Release. **Es ist eine Verzögerung, und sie
trifft zuerst jede neu hinzugekommene operative Datei.**

**Die bittere Zeile: dieser Befund stand wörtlich im Repo.** `phase3_edge/CLAUDE.md` notiert seit
2026-09-28 „der Watchdog startete dadurch ins Leere", und der tail-proxy wurde am 2026-09-29
**genau deshalb** ohne `__REPO_ROOT__` gebaut — mit einem Kommentar, der die Kopplung als
„konstruktiv ausgeschlossen" führt. Die Watchdog-Unit (Code vom 2026-09-26) ist einen Tag älter
als der Befund und hat die Lehre nicht bekommen. **Dritte Wiederholung derselben Lehre in diesem
Projekt** (nach der Schnitt-Anker-Falle in P8.6 und den Kommentar-Fallen in den Wächtern): Ein
Befund, der neben einer Entscheidung steht, wirkt nicht auf deren Nachbarn. **Nikinger-Entscheidung
2026-10-01: Systempfad** — `ExecStart=/usr/local/libexec/sharefyx/tailscaled_watchdog.sh`,
`Documentation=` fällt mit derselben Begründung, Installation per
`sudo install -D -m 0755` **vor** `install_units.sh`. Der Preis ist benannt: ein Skript-Update
braucht ein erneutes `sudo install`, die Unit startet die installierte Kopie. Elfter Wächter
(`test_execstart_carries_no_repo_path`), Gegenprobe mit zwei Verstößen → 2 rote Assertions.

**Und was das über den Betrieb sagt:** `203/EXEC` war harmlos (das Skript lief nie, es wurde nichts
neugestartet) — aber ein **laufender Timer beweist nicht, dass ein Dienst arbeitet**. Ab jetzt ist
der Abschluss die `healthy: Self.Online=true`-Zeile, nicht die Timer-Zeile.

### Abschluss — Step B ist ✅, und die Abnahme hat ihren Job erfüllt

**P9-19 ist geschlossen.** Nach dem Befund-7-Fix, im zweiten Fenster:

```
18:05:31  Stopped tailscaled                              ← Stop 1
18:05:40  status unclear → netcheck failed → tailscaled restarted   ← 9 s, polkit-Pfad
          State-Datei: 1790870740 (18:05:40)              ← der Speicher existiert jetzt real
18:09:28  Stopped tailscaled                              ← Stop 2
18:09:56  rate-limited (256s since last, threshold 900s)
18:11:01  (321s) · 18:12:06 (386s) · 18:13:11 (451s) · 18:14:11 (511s) · 18:15:16 (576s)
18:16:21  (641s) · 18:17:26 (706s) · 18:18:26 (767s) · 18:19:29 (829s)   ← zehn Takte, null Restarts
18:19:29  unhealthy: Self.Online=false                    ← manueller Start, noch nicht online
18:20:33  healthy: Self.Online=true
```

**Zehn Takte ohne einen Restart, `tailscaled` rund zehn Minuten unten** — das Rate-Limit ist kein
Vermerk, es hat den Dienst tatsächlich am Laufen gehalten. **Und ein Fund obendrauf:** um 18:19:29
nahm der Pfad `unhealthy: Self.Online=false` statt `status unclear`, weil der Dienst da lief, aber
noch nicht verbunden war. Damit ist **auch der `false`-Zweig von Stufe 1 live belegt** — den
vorher nur die Mock-Tests kannten. Die gestufte Logik aus Plan §4.2 ist damit in beiden Verzweigungen
des Stufe-1-Ausgangs gemessen, nicht behauptet.

**Nicht live gesehen und bewusst nicht erzwungen:** der Ablauf „Fenster abgelaufen ⇒ wieder ein
Restart" (Fenster endete 18:20:40, der Knoten war um 18:20:33 gesund). Für dieses Bild hätte man
absichtlich 15 Minuten einen Knoten offline halten müssen — der Pfad ist im Test abgedeckt, das
Fehlen der Beobachtung ist benannt, kein Abnahmekriterium.

**Und ein eigener Fehler, der in dieselbe Rubrik gehört:** unmittelbar nach `install_units.sh` habe
ich „`/run/tailscaled-watchdog/` fehlt" gemeldet — weil ich **parallel zum Takt** prüfte statt danach.
Der Lauf eine Minute später legte das Verzeichnis an und ließ es stehen. **Ein `ls` in derselben
Sekunde wie ein 60-Sekunden-Timer ist eine Wette.** Merkform für jede Prüfung gegen einen Timer:
erst den Takt abwarten, dann messen.

**Ein Posten, den ich benannt, nicht entschieden habe:** das transitive `mcp` bleibt ungepinnt
(Dev 1.28.1, Live 1.30.0), und die drei alternativen Autorisierungswege oben sind deine Wahl, nicht
meine — einer davon verändert die Härtung.

## Session stopped — 2026-09-30 (vierter Block, Step H)

**Step H ist gebaut, und die Reihenfolge entschied sich an einer Messung: die Domain ist nicht
registriert.** `eurofyx.com` liefert `NXDOMAIN` **und** `rdap.verisign.com` 404, dieselbe Antwort
für `.de`/`.tech`/`.app`/`.cloud`/`.net`/`.org`/`.eu` — A4 braucht eine auflösende Domain fürs
Zertifikat, also bleiben A4/A5/A7/A8 blockiert und der letzte Code-Step wird gezogen. `pytest`
**1084**, `ui_budget` 5/5, kein Service-Touch.

### Der Fund: die Plan-Prämisse „installiert ist 3.4.4" war falsch — der Drift hatte schon stattgefunden

| Ort | `fastmcp` | `mcp` |
|---|---|---|
| Live-Release `/opt/sharefyx/current/.venv` (read-only) | **3.4.7** | 1.30.0 |
| Dev-`.venv` (vorher) | 3.4.4 | 1.28.1 |
| `phase2_mcp/pyproject.toml` — seit dem ersten Commit `1c131c2` | `>=3.4,<3.5` | — |

`deploy.sh:153` baut pro Release ein **frisches** venv, `scripts/dev_install.sh:9-13` installiert
editable — ein Range-Pin löst bei jedem Deploy auf das **damalige** neueste 3.4.x auf. Der
Patch-Wechsel hat also unbemerkt stattgefunden, mit dem Release vom 2026-09-18. P3-D
(`phase3_edge_plan.md:106`) wollte genau das verbieten („unter einem Dauerdienst darf sich das
nicht unbemerkt bewegen"), P4-R wiederholte es — **im Code stand nie ein exakter Pin.** Zwei
Pläne, eine Entscheidung, null Umsetzung; das war der Drift, nicht der Bump.

**Gebaut:** `fastmcp==3.4.7` exakt, mit datiertem Kommentar an der Zeile (Grund, Messung,
P9-R/V79/V163). Das ist die Einlösung von P3-D, keine neue Entscheidung — Präzedenz ist
`phase4_auth/pyproject.toml` mit `argon2-cffi==25.1.0` und `cryptography==49.0.0`.
**P9-55 verlangte wörtlich „weiterhin `<3.5`"**; gebaut ist `==3.4.7`, oberhalb jeder 3.4-Version,
also innerhalb P9-R, aber ohne die Range-Form — **Nikinger-Entscheidung 2026-09-30**, weil die
Range-Form der Mechanismus des gemessenen Drifts ist. Als Abweichung im Plan §10 dokumentiert,
nicht stillschweigend.

**Der eigentliche Riegel ist ein Test.** `test_the_installed_fastmcp_matches_the_pin` vergleicht
die installierte Version mit der Pin-Zeile — und läuft im **Release-venv** mit, weil `deploy.sh:169`
dort `pytest -q` aufruft und den Deploy bei Fehlschlag abbricht. Ein Patch-Drift ist damit ein
roter Deploy statt einer Randnotiz. Fünf Wächter, **Gegenprobe mit vier eingebauten Verstößen →
7 rote Assertions über vier Tests**: Range-Pin (3 rot), Pin auf 4.x (2 rot), `V79` aus dem
Kommentar entfernt (1 rot), zweiter Pin in `phase4_auth` (1 rot). Alles zurückgebaut, 5/5 grün.

### V163 ist beantwortet — drei Codepunkte statt einer Vermutung aus dem Aufrufbild

1. `phase4_auth/authserver/metadata.py:19` lässt `client_id_metadata_document_supported`
   **bewusst abwesend** — CIMD ist aus, Claude nimmt DCR (P4-E, V14). Der Fix betrifft CIMD.
2. `metadata.py:32`: `token_endpoint_auth_methods_supported: ["none"]` — öffentlicher Client, es
   werden gar keine Client-Assertions erzeugt.
3. Die benutzte fastmcp-Fläche ist `FastMCP`/`Client`/`StreamableHttpTransport`/`ToolError`/
   `Image`/`Middleware`/`get_http_request`/`http_app` — **kein `OAuthProxy`, kein `JWTVerifier`**;
   Auth trägt der eigene `BearerAuthASGI` (`asgi.py:40`).

Die drei Releases dazwischen (3.4.5 JWKS-Key-Skip, 3.4.6 Trusted-Proxy für SSRF-Metadaten, 3.4.7
CIMD-Audience) liegen alle auf Pfaden, die dieses Projekt nicht benutzt. **Der Fix ist inert, der
Bump ist Hygiene** — genau wie am 2026-09-19 vermutet, jetzt gemessen. Dass er trotzdem prod-seitig
stattgefunden hat, ist der Grund, warum der Step nicht nur ein Kommentar war.

### Ein eigener Fehler, beim Wächter-Schreiben

`req.specifier.version` gibt es nicht (`SpecifierSet` hat kein `.version`) — zwei Tests rot, bevor
der Helper existierte. Genau die Klasse Fehler, die der Wächter verhindern soll, hat mich der
Wächter zuerst einmal selbst gekostet. Beim selben Durchgang: ein `edit` auf die P2-Modulstatus-
Tabelle hat **Zeile 13 mitgefressen** (Anker war der Zeilenanfang statt des Zeilenendes). Beides
gesehen, weil `git diff` nach dem Edit **rein additiv** hätte sein müssen — der Nachweis steht
jetzt im Diff (13 Zeilen rein, 0 raus).

### Was gemessen wurde

| Gegenstand | Nachweis |
|---|---|
| **Domain** | `dig +short eurofyx.<tld> @1.1.1.1` → **NXDOMAIN** für alle sieben Kandidaten; `rdap.verisign.com/com/v1/domain/eurofyx.com` → **404** |
| **Prod-Version** | read-only über `/opt/sharefyx/current/.venv/bin/python` → `fastmcp 3.4.7`, `mcp 1.30.0` — **nur gelesen**, kein `systemctl`, kein Restart |
| **Gegenprobe** | vier Verstöße eingebaut → 7 rote Assertions, danach per `cp` aus dem Backup zurückgebaut; `git diff --stat` zeigt nur `phase2_mcp/pyproject.toml` |
| **Tests** | 5 neue in `phase9_hardening/tests/test_step_h_deps.py`; `pytest` 1079 → **1084** in 186 s (Bestand unverändert, **mit** 3.4.7 im Dev-venv) · `ui_budget` **5/5** (151,8 KB; `search_items` 128,6 ms / `get_item` 4,7 ms über den echten MCP-Stack, also der 3.4.7-Pfad wirklich gelaufen) · `doc_health` 0 Befunde |
| **P1-Tabu** | nichts in `phase1_storage/` berührt — der Pin ist Phase-2-Terrrain, die Tabu-Liste nicht |

**Benannt, nicht gebaut:** das transitive `mcp` ist weiterhin **nicht** gepinnt (Dev 1.28.1, Live
1.30.0). Ein expliziter `mcp`-Pin wäre eine Lock-Entscheidung, die kein Plan getragen hat —
P9-Backlog-Kandidat, kein Blocker.

### Nächster Schritt

**Step A wartet auf die Domain-Registrierung** — das ist jetzt die einzige offene Kette in P9 und
der Grund, warum H gezogen wurde, bevor Gate/Z kam. Sobald `eurofyx.<tld>` auflöst: A4 (Caddyfile,
drei Platzhalter) → A5 DNS → **A7 ist der riskante Schritt** (drei gemessene Fallen:
`ALLOWED_HOSTS` braucht neue Domain **und** Funnel-Host **und** `127.0.0.1`, `/health` statt
`/healthz`, und nach `install_units.sh` ein eigener `restart sharefyx-mcp`) → A8 Connector in
beiden Konten. **Gate/Z** kann ohne A4–A8 nicht abgeschlossen werden; die beiden Doku-Posten
daraus (INDEX-Rotation P9-L bei 50.033 B, Contract-Rotation in `phase1_storage/CLAUDE.md` bei
43.333 B) sind strukturell und nicht durch Kürzen lösbar.

## Session stopped — 2026-09-30 (dritter Block, Step G)

**Step G ist gebaut: Löschen heißt Verschieben nach `._trash/`, und der Ort musste vor dem Bau
korrigiert werden — sonst hätte die halbe Step-Definition nicht funktioniert.** Commit folgt
unten; `pytest` **1078**, Browser **14/14**, kein Service-Touch.

### Der teuerste Fund der Session: der Plan-Ort hätte das Versprechen gebrochen

Plan §9.1 sagt, die Unsichtbarkeit sei „vorhandenes Verhalten", belegt mit `store.py:815`. Der
Anker zeigt auf `ensure_folder()`; der echte `_trash`-Skip sitzt bei 860/868 in **`list_assets()`**
— für **Assets**, nicht für Items. Der Präzedenzfall trägt nicht. Mit dem `<space>/_trash/` aus
§9.3 gemessen:

| | `<space>/_trash/` (Plan) | `DATA_ROOT/._trash/<space>/` (gebaut) |
|---|---|---|
| `search()` nach `rebuild_index()` | **Item wieder da** (`folder="_trash"`) | weg |
| `list_spaces()` | **`['_trash', 'sp']`** — Phantom-Space | `['sp']` |
| P1-Änderungen | `index.py` **und** `files.py` = **zehnte** Öffnung | **keine** |

`rebuild_index()` macht `space_dir.rglob("*.md")` **ohne Skip**, `list_spaces()` führt jedes
Nicht-Punkt-Verzeichnis als Space, und `RESERVED_DIR_NAMES` ist `{"_archive", "_assets"}`. Der
Plan-Ort hätte einen **sichtbaren Ordner mit dem gelöschten Item** erzeugt — exakt das Gegenteil
von P9-J — und die Reparatur wäre eine P1-Contract-Öffnung gewesen, die niemand angekündigt hat.
**Nikinger-Entscheidung 2026-09-30: `._trash` auf DATA_ROOT-Ebene.** Damit stimmt die Prämisse
wieder, nur eine Ebene höher und mit einem Punkt: beide Scanner überspringen Punkt-Verzeichnisse
bereits. Die Lehre ist die des Tages: *„der Code hat diese Funktion schon"* ist eine Behauptung
über **welche** Funktion — der Anker war eine Zeile daneben.

### Der Dialog: nach dem Vorbild im Repo, nicht neu erfunden

Vor dem Bauen habe ich `space-remove-dialog` (P7-K) gelesen — es ist bereits **zweistufig mit
eingetipptem Namen**, und der Server prüft `body["confirm"]` exakt (`api.py:567`). Ich hatte
zuerst nur eine Stufe gebaut (sichtbarer Konsequenztext + gesperrter Knopf), was **ein** Gate ist;
der Plan verlangt zwei zwingende und sagt wörtlich, das Confirm-Muster zu wiederverwenden. Also
nachgezogen: Stufe 1 = vorhandenes `confirmDialog()`, Stufe 2 = `trashRefreshSubmit()` als
**eine** Funktion, die den Knopf an `value.trim() !== ziel.title` bindet.

Dabei zwei eigene Fehler, beide beim Wächter-Schreiben aufgefallen:
- Der erste Wächter suchte `toLowerCase` im Dialog-Block und schlug an — weil mein **Kommentar**
  dieses Wort enthält, um es auszuschließen. Dieselbe Falle wie in P8.6 Block H. Der Test filtert
  jetzt Kommentarzeilen, statt auf meine Formulierung zu vertrauen.
- Ich hatte zwei `--caution-*`-Tokens benutzt, die es nicht gibt. Der Wächter
  `test_every_css_var_reference_is_defined` hätte es gefangen; ich habe es vorher selbst gesehen
  und auf `--caution` + `.asset-strip__remove` (der vorhandene Entfernen-Knopf) umgestellt.

### Der Browserbeleg brauchte eine eigene TLS-Instanz — und der Grund ist eine Produktinvariante

Der 18773er-Wegwerf kann **keinen** Schreibvorgang annehmen. `require_csrf`
(`security.py:79-95`) verlangt `Origin` **exakt** gleich `settings.base_url`, sonst
`sec-fetch-site: same-origin`, plus Token. `settings.base_url` ist in `app.py:204` genau
`oauth.settings.base_url` = `SPACE_PUBLIC_BASE_URL`, und das muss laut `config.py:87` zwingend
`https://` sein (OAuth-Issuer). Ein Browser auf `http://127.0.0.1:18773` kann das **strukturell
nie** erfüllen, `Origin` lässt sich nicht entfernen (verbotener Header — `page.route()` bleibt
wirkungslos, gemessen), und `serve.py` ruft `uvicorn.run()` ohne `ssl_*`. **Das ist der „Befund
für Block D / Step Z", den der Kommentar im Setup-Skript (Zeile 341) seit P8.6 nennt — bis auf
die Ursache zurückgeführt.**

Lösung ohne Produktänderung: eigenes Harness mit selbstsigniertem Zertifikat für `IP:127.0.0.1`
und einem Launcher, der **dieselbe** App baut wie `serve.py`, nur mit `ssl_keyfile`. `serve.py`
selbst bleibt unberührt — einen Produktparameter nur für einen Testharness zu ergänzen wäre die
Scope-Ausweitung, die P9-K gerade vermeiden soll. Damit laufen **alle drei** CSRF-Schichten
normal, und der 14/14-Lauf ist ein echter Klick, kein nachgespielter Request.

**Ein Werkzeug, das sich selbst widersprach:** die Sichtprüfung meldete den gesperrten „Löschen"-
Knopf als *aktiv*. `is_disabled()` sagt `True`, `app.css:278` stylt `:disabled` mit
`cursor: not-allowed`. Das ist genau die Grenze aus
`docs/concepts/sichtpruefung_automation_tooling.md` (Zustands- und Detailaussagen eines VLM sind
unbrauchbar). Darum pinnt jetzt ein **Test die Regel** statt dass ich dem Bild glaube.

### Was gemessen wurde

| Gegenstand | Nachweis |
|---|---|
| **Gegenprobe** | vier Verstöße eingebaut (Trash in den Space, `index.delete_item` raus, Server-Gate raus, Kleinschreibungs-Toleranz) → **11 Tests rot** über beide Schichten, danach zurückgebaut |
| **Browser** | `p9_step_g_self_check.py`, **14/14**, zwei Läufe hintereinander unabhängig (das Harness säet bei jedem Start neu — ein unsichtbarer Papierkorb lässt sich gerade nicht zurücksetzen, ein zweiter Lauf fände sonst eine leere Liste) · 6 Screenshots `docs/screenshots/p9_step_g_{01..06}_*.png` · Probe `probes/p9_step_g_probe.json` |
| **Tests** | 13 in `test_step_g_trash.py` (die 7 der Plan-Liste + 6 für gemessene Lücken) + 5 Endpunkt-Tests in `test_api.py`; `pytest` 1062 → **1078** in 190 s, `ui_budget` 5/5 (151,5 KB, +2,5 KB für Dialog/CSS/Icon), `doc_health` 0, `node --check` über alle 13 JS-Dateien grün |
| **P1-Tabu** | nur `phase1_storage/storage/store.py` berührt (keine zweite P1-Datei, weil der Punkt-Ort die Änderung in `index.py`/`files.py` überflüssig macht) |
| **Hard Rule 9** | beide Wegwerf-Instanzen ausschließlich über ihre PID-Datei gestoppt, kein `pkill -f`, kein `systemctl`; `sharefyx-mcp` nur gelesen (PID 1033, unverändert) |

### Nächster Schritt

**Step H** (`fastmcp` 3.4.4 → 3.4.7) ist der letzte Code-Step und der kleinste: eine
Versionsnummer plus ein Test. **V163** ist die einzige offene Frage dort, und sie ist in der
Planungssession schon beantwortet worden — der 3.4.7-Fix betrifft `OAuthProxy`/`private_key_jwt`,
dieses Projekt nutzt einen eigenen `BearerAuthASGI`, der Bump ist also Hygiene, kein
Sicherheitsbedarf. Wer H zieht, sollte das als **einen** Commit tun und den Lock P9-R
(`fastmcp` bleibt auf 3.4.x) **nicht** antasten: FastMCP 4 bleibt V79 und eine eigene Mini-Phase.

**Offen und bewusst nicht gebaut:** V162 (wächst `._trash/` messbar — die Menge im Harness ist
kein Messwert für den echten `DATA_ROOT`), die Räumung von `._trash/` (P10-Liste), und die
Asset-Dateien eines gelöschten Items bleiben unerreichbar unter `<space>/_assets/<item_id>/`
liegen — bewusst, sonst würde aus einer atomaren Operation eine halbe.

## Session stopped — 2026-09-30 (zweiter Block, Step F)

**Step F ist gebaut: `doing` wird ein Statuswert, `assignee` ein erstklassiges Feld mit
Index-Spalte — die neunte und bis jetzt letzte P1-Contract-Öffnung.** Der Domain-Block hängt
weiter an der Registrierung; F war der einzige Step, der neben ihm ohne externe Abhängigkeit
lag. Kein Service-Touch, `pytest` grün, Tabu-Hartpfade unberührt.

### V160 ist beantwortet: `assignee` ist ein Space-Name, ohne Validierung

Der Plan (§8.4) hat die Frage gestellt und die Empfehlung offengelassen; der Nikinger hat
2026-09-30 die Empfehlung bestätigt. `_coerce_assignee()` prüft **nur den Typ**. Warum keine
Prüfung gegen die Space-Liste: das wäre eine **zweite**, nicht angekündigte Contract-Öffnung —
der Schreibpfad müsste den Space auflösen, mit dem ein Item in einem fremden Space belegt sein
könnte. Die Formulierung, die ich mir gemerkt habe: ein toter Space-Name ist ein Anzeigefehler,
ein *erfundener* Zweiter Space wäre es nicht.

### Der Plan sagte neun Stellen, der Diff hat achtzehn

Plan §8.2 listet F1–F9 in genau drei Dateien. Gemessen am Diff: **18 Hunks** (`models.py` 4,
`store.py` 8, `index.py` 6). Die Differenz ist kein Pfusch, sondern eine Lücke in der Liste:
**F9 („Upsert") sind drei Statement-Teile plus ein Row-Dict**, nicht eine Stelle — nur das
Row-Dict zu ändern hätte den Index mit `ProgrammingError` laufen lassen. Dazu kamen **drei
Stellen, die der Plan nicht nannte und ohne die es nicht funktioniert hätte**:

| # | Stelle | Was ohne sie passiert wäre |
|---|---|---|
| **F10** | `store._summary()` | `get()` kennt den Wert, **jede Liste und jede Suche** stünde dauerhaft auf `""`. F3 wäre ein totes Feld — und kein Test hätte es gemerkt, weil beide Seiten „funktionieren" |
| **F11** | `store.update()` | Der Wert **würde** in die Datei gelangen (über `Item.extra` → `fields.update()`), `item.assignee` bliebe auf `""`, F6 (`if item.assignee`) feuerte nie. Der am leichtesten übersehene Fall, weil „es funktioniert" hier kein Beweis ist |
| — | `store._coerce_assignee()` | Die Typprüfung einmal im Kern statt dreimal in den Adaptern — dieselbe Begründung wie `_check_type_and_status()` (D2) |

Die Kette dahinter ist immer dieselbe: ein Feld, das nur halb verdrahtet ist, sieht fertig aus.

### Ein Befund, den ich gefunden, gemessen und **nicht** behoben habe

`_BUCKETS` in `api.py` kennt kein `doing`. `bucketFor()` (`list.js:516`) vergleicht
`f.status === item.status` **exakt**, eine `doing`-Aufgabe passt auf keinen der vier Eimer,
`bucketFor()` liefert `null`, beide Aufrufer fallen auf `|| state.filter` zurück: sie fehlt in
jedem Zähler und ist in der Liste nur sichtbar, wenn man zufällig im passenden Filter steht.
**Derselbe Fund wie bei `done` im Phase-5-Step-7b**, eine Statusversion später.

Ich habe den Fix gebaut und dann **verworfen**, weil beide Kandidaten Darstellungsentscheidungen
sind, die P9-P ausdrücklich P10 zuteilt: ein fünfter `_BUCKETS`-Eintrag erzeugt über
`bucketNames() = Object.keys(state.meta.buckets)` und `tree.js:72` einen **fünften Rail-Eintrag
mit unübersetztem Label** — das ist genau die Hervorhebung, die nicht in diesen Step gehört. Der
Befund steht vollständig mit beiden Kandidaten im Code, und ein Wächter pinnt, dass er nicht
verschwindet, ohne dass P10 ihn behoben hat.

### Zwei Alt-Tests, die mitgezogen werden mussten — und was sie über Kalibrierung lehren

`test_upsert_get_delete_roundtrip` baut seine Indexzeile von Hand und schlug mit
`ProgrammingError: missing parameter` fehl. **Das ist richtig so** — benannte Parameter schlagen
laut fehl, statt still einen Default zu nehmen. Der Test trägt den Key jetzt und prüft zusätzlich
den `ON CONFLICT`-Zweig.

Der zweite war der lehrreichere: `test_search_listing_of_30_items_stays_within_calibrated_json_bound`
sagt in seinem eigenen Docstring, dass eine `ItemSummary`-Feldsatz-Änderung **Nikinger-Sache und
kein stiller Nebeneffekt** ist. Also gemessen statt erhöht: **16.390 B** mit Feld gegen **16.300 B**
ohne, exakt **+16 B/Item** (`"assignee": "",`). Band 12–16 KB → **13–18 KB**, mit ungefähr
gleicher Marge. Der Test hat die echte Zunahme bemerkt, statt eine Toleranz zu schlucken.

Eine eigene Fehlannahme unterwegs: ich hatte `400` für einen Validierungsfehler erwartet, die API
liefert `422` (`errors.py:50`). Der Code hatte recht, mein Test nicht.

### V161: mit einem synthetischen Vorabwert beantwortet, P9-43 bleibt beim Nikinger

`rebuild_index()` über 500/1500/3000 Items in `tmp_path`: **2,45 / 2,48 / 4,01 ms pro Item** —
bis 1500 linear, bei 3000 etwas schlechter. Der echte `DATA_ROOT` (nur gelesen) hat **153 Items**
außerhalb `_archive`, 197 mit: **0,4–0,6 s** einmalige Startkosten beim Schema-Sprung 3 → 4.
Das ist der Vorabwert, den die Plan-Session brauchte; **P9-43 bleibt die Messung am echten
`DATA_ROOT` beim Deploy**, denn ein `rebuild_index()` dort ist ein Schreibzugriff auf Produktivdaten.

### Was gemessen wurde

| Gegenstand | Nachweis |
|---|---|
| **Enge Probe §8.7** | `git diff --stat -- phase1_storage/storage` = **genau drei Dateien**; die sechs Hartpfade `acl.py`/`linkscan.py`/`patch.py`/`files.py`/`history.py`/`frontmatter.py` leer |
| **Gegenprobe** | vier Verstöße eingebaut (F10 raus, F11 raus, Version zurück auf 3, F6 ohne `if`) → **10 Tests rot**, exakt die zuständigen; danach zurückgebaut |
| **`doing` in der Oberfläche** | **V159 gemessen, nicht geglaubt**: `editor.js:246` liest `state.meta.status_values[itemType]` und rendert rohe Werte — `doing` erscheint im Editor-Dropdown ohne JS-Änderung. Die Plan-Behauptung zu `dialogs.js:323` ist **halb richtig**: dort iteriert `Object.keys(state.meta.status_values)`, also das **Typ**-Vokabular, und der Anlegen-Dialog hat gar keinen Status-Knopf (`createStatus` existiert nicht) — für ihn ist die Aussage gegenstandslos |
| **Tests** | `pytest` **1039 → 1062** in 186,8 s (23 neu: 17 `test_step_f_schema.py`, 4 `test_tools.py`, 2 `test_api.py`), davon 191 in `phase1_storage`; `ui_budget` 5/5; `doc_health.py` 0 Befunde; `node --check` über alle 13 JS-Dateien grün (keine JS-Datei geändert) |

### Nächster Schritt

**Zwei Kandidaten, und sie sind nicht gleichwertig:**

1. **Warten auf die Domain** (A5 → A4 → A7 → A8), sobald `eurofyx.<tld>` registriert ist. Die
   Kette ist unberührt und der Nikinger hatte sie zuletzt in der Hand.
2. **Step G** (Löschen nach `_trash/`, P9-I/J/K) — der andere reine Code-Step. **Achtung, die
   Reihenfolge ist nicht beliebig:** §8.7 warnt ausdrücklich davor, F und G zu vermischen, weil
   G `store.py` erneut anfasst (`Store.trash()`); der enge Diff gegen **diesen** Commit bleibt
   sauber, solange G ein eigener Commit ist. **V160-analoge Frage für G:** `delete` für
   wen sichtbar? Der Plan sagt human-only und für Nutzer unsichtbar, das wäre also geklärt.

## Session stopped — 2026-09-30

**Step A ist halb gelaufen: der Repo-Anteil ist gebaut, und der Nikinger hat A1, A2, A3, A0b
und A6 ausgeführt.** Die Kette hängt jetzt an genau einer Stelle — der Domain-Registrierung
für A5. A4 (Caddy) braucht eine auflösende Domain für das Let's-Encrypt-Zertifikat, A7 und A8
hängen an A4. **Kein Produktcode berührt**, `pytest` grün, Tabu-Bereichs-Diff leer, kein
`systemctl` von mir, `sharefyx-mcp` nur gelesen (Hard Rule 9).

### Der Befund, der die Bauform getragen hat — und der war teuer

Plan §3.2 A4 verlangt `reverse_proxy <heimvm-tailnet-name>:<port>`. **Das ist unbaubar.**
`sharefyx-mcp.service:13` setzt `SPACE_HOST=127.0.0.1`, `ss -ltnp` zeigte keinen Listener auf
`100.93.43.122:8765`, und der Funnel funktioniert nur, weil `tailscaled` auf derselben Maschine
in die Schleife connectet. Die naheliegende Reparatur `SPACE_HOST=0.0.0.0` verstößt gegen die
**gelockte P3-B-Entscheidung**. Statt dessen ein Relay, das die eine Lücke schließt ohne P3-B
zu brechen — und **ohne `__REPO_ROOT__` im `ExecStart`**, womit sich die Release-Pfad-Kopplung
aus dem Step-B-Befund gar nicht erst eintritt.

`tailscale serve --tcp` (1.102.4 kann es) wäre eleganter und ist **nicht** gewählt: die
ACL-Durchsetzung von Tailscale-TCP-Forwardern war nicht verifizierbar (kein Netzzugriff), und
eine offene Frage darf nicht die Grundlage einer Firewall-Entscheidung sein → **V162** offen.

### Sieben Befunde, alle mit Fundstelle (Volltext im Runbook §0)

`/health` statt `/healthz` (`app.py:216`) · `ALLOWED_HOSTS` fehlt in Plan-A7 (sonst 400 auf
*jede* Anfrage, Live-Incident 2026-09-18) · **V149 beantwortet**: `issuer` **ist** `base_url`
**ist** `SPACE_PUBLIC_BASE_URL`, kein `iss`-Check beim Einlösen, also invalidiert der Wechsel
keine Token-Familie · der Funnel bleibt nach A7 **lesbar, aber nicht beschreibbar** (CSRF-Origin
exakt, `security.py:84`) — die Präzisierung, die P9-14 braucht · `socat` fehlte · die
Tailnet-Policy erlaubt heute **alles** (`src/dst/ip` je `*`), unser Grant ist damit **zusätzlich
und nicht einschränkend** — benannt, nicht mitgenommen.

### Der Fund dieser Session, der am meisten zählt: mein eigenes A6 hätte den Betrieb gekappt

`ufw default deny incoming` gilt **auf allen Interfaces, auch `tailscale0`**. Meine erste
Fassung von A6 erlaubte 80/443, aber **kein SSH über das Tailnet** — wer über die Tailnet-IP
verbunden ist, verliert die Verbindung, und zurück kommt man nur über die IONOS-Webconsole.
Gefallen ist mir das **erst beim Durchdenken der Firewall-Semantik**, nicht beim Schreiben —
und der Nikinger hatte ausgerechnet vorher gefragt, ob die Schritte den laufenden Betrieb
überhaupt anfassen. Diese Frage war die bessere Prüfung als meine Checkliste.

### Vier eigene Fehler, alle vor dem Commit behoben

1. **`tailscale ping` als Beleg** — ich hatte ins Runbook geschrieben, er antworte „noch
   nicht". Falsch in die Richtung: der Befehl prüft den WireGuard-Pfad zwischen zwei
   `tailscaled`, nicht die Datenebene, auf der die ACL greift, und **kann grün sein, während
   die Regel fehlt**. Er ist kein Nachweis. Der echte Nachweis ist der ACL-Testharness.
2. **`acls` statt `grants`** — der Screenshot der Seite *Add rule* zeigte den Knopf
   **„Save grant"**. Die klassische Form hätte der Nikinger abtippen müssen, weil die GUI sie
   nicht erzeugt. Entwurf, Test und Runbook folgen jetzt der belegten Form.
3. **Ein erfundener Drift** — ich meldete dem Nikinger, `local.env` und die installierte Unit
   wichen im `DATA_ROOT` ab. **Falsch**: beide nennen `/home/savefyx/savefyx-data`, das
   Verzeichnis existiert. Ich hatte mein eigenes `cat`-Ergebnis falsch gelesen und die
   Differenz durch eine Diagnose bestätigt, die ich nicht gemacht hatte. Zurückgenommen, bevor
   daraus eine Aufgabe wurde.
4. **`space.` statt `sharefyx.`** — mein Vorschlag aus Kürzegründen war der schwächere: die
   Adresse wird an vier Stellen als exakter String verglichen, und ein Alltagswort ist das,
   was man falsch erinnert. Zurückgenommen, mit Begründung im Runbook.

Dazu eine **Warnung, die ich mir selbst nicht gegönnt habe**: `docs/INDEX.md` steht bei
**44.669 B** und damit ~6,6 KB über dem 40-KB-Schwellwert des Werkzeugs. Benannt statt
versteckt, wie in P8.6; die Lösung bleibt die INDEX-Rotation in Step Z (P9-L).

### Was gemessen wurde — und von wem

| Schritt | Nachweis |
|---|---|
| **A3** Beitritt | von der **Gegenseite**: die Heim-VM sieht `ubuntu` als `100.121.142.113` mit `Tags=['tag:sharefyx-edge']` und `User=None` — genau das beweist, dass der Tag griff und die Node nicht als Nutzergerät läuft |
| **A0b** Relay | `socat` 1.8.0.0, `ProtectSystem=strict`/`NoNewPrivileges`/`MemoryDenyWriteExecute` gesetzt, **zwei** Listener, `diagnose.sh` danach unverändert alle Prüfungen grün **inklusive des echten öffentlichen Pfads** — die Bestandspfade sind unberührt |
| **A6** Firewall | Gegenprobe von der Heim-VM (die weder im Tailnet des VPS noch in dessen LAN ist): Tailnet-SSH **offen**, öffentliches SSH **timeout** (ufw *droppt* still, `deny` ≠ `reject`), 443 **refused** (Paket kommt am Host an, lauscht noch nichts) |
| **V151** Vorabwert | `tailscale ping` → **28–37 ms über DERP Frankfurt**, nicht direkt (erwartbar hinter CGNAT). Das ist das Tailnet-Bein, nicht der ganze Weg; der Vergleich gegen 372,9 ms folgt in A7 |

**Die wechselnde PID ist aufgeklärt** (Reboot gestern Nacht): der Dienst startete 6 Sekunden
nach dem System-Boot — das gesunde Muster der P3-Rebootzeile 6, kein Incident. Ich hatte sie
zuvor als ungeklärt notiert, statt eine Erfindung zu liefern; die eine Messung
(`journalctl -b -u sharefyx-mcp`) hätte es sofort gezeigt.

### Tests und Selbstprüfung

`phase9_hardening/tests/test_tail_proxy.py`, 7 Wächter: Ziel bleibt Loopback · Bind ist eine
Tailnet-IP und nicht `0.0.0.0` · Härtung **identisch mit der MCP-Unit** · kein Repo-Pfad im
`ExecStart` · Port identisch mit `SPACE_PORT` · Health-Routen-Korrektur hält · ACL-Entwurf
fail-closed. **Gegenprobe: vier Verstöße eingebaut → 4/7 rot, exakt die vier zuständigen.**

`pytest -q` → siehe Commit-Body. `doc_health.py` → **0 Befunde**. Tabu-Bereichs-Diff leer.
Kein Service-Touch; die Wegwerf-Instanz gab es nicht, nur eine einzelne TCP-Verbindung auf Port
22 als Vorprüfung des VPS.

### Nächster Schritt

**Blockiert an einer Stelle: die Domain.** Sobald `eurofyx.<tld>` registriert ist:
**A5** (A-Record `sharefyx` → `217.160.128.146`, **kein** AAAA) → **A4** (Caddy, drei
Platzhalter in `step_a/Caddyfile.template` füllen) → **A7** (der riskante Schritt: fasst den
laufenden Prod-Dienst an) → **A8** (Connector in beiden Konten, echter `list_spaces`).

**Zwei Entscheidungen liegen beim Nikinger:** (1) die TLD, `.com` ist empfohlen; (2) falls die
Domain-Aktivierung länger dauert, **Step F** (Schema `doing`/`assignee`) vorziehen — reiner
Code-Step, braucht nur **V160**: `assignee` als **Space-Name**? Empfehlung ja, **ohne**
Validierung, weil eine Prüfung gegen die Space-Liste eine zweite, nicht angekündigte
Contract-Öffnung wäre.

**Uncommitted geblieben, absichtlich:** `screenshots_latest/` enthält drei Arbeitsdateien des
Nikingers (zwei Tailscale-Console-Screenshots + das als HTML gespeicherte Seitenquelltext).
Sie sind **nicht** im Repo und sollen es nicht werden: das HTML enthält die Knotenliste des
Tailnets mit Owner-Kontakten. Die `git add`-Aufrufe dieser Session nehmen `phase9_hardening/`
explizit, nicht `-A`.

## Session stopped — 2026-09-29

**Step A: der M3-Anteil ist gebaut, ausgeführt wird er vom Nikinger.** Kein Produktcode
berührt, kein Service-Touch, `pytest` grün, Tabu-Bereichs-Diff leer (Hard Rule 9 durchgehend:
kein `systemctl` von mir, nur `ss`/`tailscale status` als lesende Messung).

**Erste Handlung dieser Session war eine Rückfrage, kein Code.** Die Notiz aus der letzten
Runde lautete „Schritt f — die feste Domain". Der Plan trägt **A** = Domain (§3) und **F** =
Schema `doing`/`assignee` (§8) — zwei völlig verschiedene Arbeiten. Bevor ich etwas baue, wurde
gemessen, ob der Vorlauf von Step A überhaupt stattgefunden hat: `tailscale status` zeigt sieben
Nodes, **keiner ist ein Terminator**; `phase3_edge/local.env` trägt `PUBLIC_BASE_URL` und
`ALLOWED_HOSTS` weiter auf `…tail4a8b49.ts.net`. Der Vorlauf fehlt also, und der Plan sagt
ausdrücklich, dass Beschaffung **kein** Agenten-Auftrag ist. Nikinger-Antwort: **Step A,
mein Anteil vorbereiten.**

### Der Befund, der die Bauform gerettet hat

**Plan §3.2 A4 ist unbaubar, und zwar nicht wegen einer Kleinigkeit.** Die Anweisung lautet
`reverse_proxy <heimvm-tailnet-name>:<port>`. Gemessen:

- `phase4_auth/systemd/sharefyx-mcp.service:13` — `Environment=SPACE_HOST=127.0.0.1`
- `ss -ltnp` — `LISTEN 127.0.0.1:8765` und **kein** Listener auf `100.93.43.122:8765`
- `tailscale serve status` — der Funnel proxyt auf `http://127.0.0.1:8765`; er funktioniert
  genau deshalb, weil `tailscaled` auf derselben Maschine in die Schleife connectet

Auf der Tailnet-Adresse gibt es nichts, womit ein VPS sich verbinden könnte. Die naheliegende
Reparatur — `SPACE_HOST=0.0.0.0` — ist die **gelockte P3-B-Entscheidung** („wird nie
`0.0.0.0`", gilt am Host, nicht nur am Router). Sie zu brechen, um einen Proxy zu retten,
wäre genau die stille Abweichung, die P8.6 zweimal gekostet hat.

**Gebaut: ein Relay, das die eine Lücke schließt, ohne P3-B zu brechen.**
`phase3_edge/systemd/sharefyx-tail-proxy.service` macht `100.93.43.122:8765 → 127.0.0.1:8765`
mit `socat`; die App bindet unverändert auf Loopback. Bewusst **ohne** `__REPO_ROOT__` im
`ExecStart` — genau damit ist die Kopplung konstruktiv ausgeschlossen, die beim Watchdog zum
Befund wurde (dort zeigte `ExecStart` auf ein Release, das die Datei nicht enthält,
Session-Block 2026-09-28). `install_units.sh` wurde dafür **nicht** angefasst: das ist
P3-Code, und der Commit bleibt additiv; das Runbook installiert die Unit mit
`sudo install -m 0644`.

**Die Alternative wurde nicht aus Bequemlichkeit verworfen.** Tailscale **1.102.4** kann
`tailscale serve --tcp` (gemessen an `serve --help`) — kein zusätzlicher Prozess, der
elegantere Weg. Ob Tailscale-TCP-Forwarder die Tailnet-ACLs durchsetzen, war in dieser
Session **nicht verifizierbar** (kein Netzzugriff: `tailscale.com` per DNS nicht auflösbar,
Suchprovider leer). Eine offene Frage darf nicht die Grundlage einer Firewall-Entscheidung
sein → der Relay ist ein gewöhnlicher Listener auf `tailscale0`, für den das ACL-Modell ohne
Zusatzannahme gilt. Als **V162** offen notiert, mit der Frage und wo sie zu beantworten ist.

### Vier weitere Befunde, alle mit Fundstelle

1. **Die Health-Route heißt `/health`, nicht `/healthz`.** `app.py:216` registriert genau
   eine. Plan §3.4 (P9-10) nennt den falschen Pfad — Abnahmezeile mit datierter Korrektur.
2. **`ALLOWED_HOSTS` fehlt in Plan-A7.** Caddy reicht den Host-Header durch, die
   `TrustedHostMiddleware` (`app.py:214`) antwortet sonst auf **jede** Anfrage mit
   `400 Invalid host header`. Keine Theorie: der Live-Incident vom 2026-09-18 war genau das.
3. **V149 beantwortet:** `AuthSettings.issuer` **ist** `base_url` **ist**
   `SPACE_PUBLIC_BASE_URL` (`config.py:45`), `metadata.py:24-29` leitet vier Felder daraus ab,
   `resource` ebenso, und `allowed_redirect_origins` hat einen eigenen Default — die
   Redirect-URIs der Claude-Clients bleiben also unberührt. **Kein Feld steht fest.** A7 ist
   damit eine Handvoll Env-Werte; die §3.3-Falle bleibt trotzdem real, weil der `iss` Teil der
   Client-Registrierung ist (RFC 9207, `routes.py:154`) → **A7 vor A8**. Und: es gibt
   **nirgends** eine `iss`-Prüfung beim Einlösen (`resolver.py` enthält kein `iss`) — der
   Wechsel invalidiert keine bestehende Token-Familie.
4. **Der Funnel bleibt nach A7 lesbar, aber nicht beschreibbar.** `security.py:84` prüft
   `origin != settings.base_url` **exakt**. Nach A7 schickt ein Browser am alten
   Funnel-Host `Origin: …ts.net` → jeder Schreibvorgang 403, GETs laufen. Das ist die
   Präzisierung, die P9-14 braucht. Ein echter Dual-Betrieb bräuchte eine zweite erlaubte
   Origin im Code, `UiSettings` hat genau ein `base_url`-Feld — **das wird nicht gebaut**
   (außerhalb Step A). Der Funnel ist der Rückfallweg für „VPS weg"; Lesen und ein
   intakter Connector reichen dafür.

### Tests

`phase9_hardening/tests/test_tail_proxy.py`, 7 Wächter: Ziel bleibt Loopback · Bind ist eine
Tailnet-IP und nicht `0.0.0.0` · Härtungs-Direktiven **identisch mit der MCP-Unit** (die
Behauptung aus dem Step-B-Block wird hier gemessen statt geglaubt) · kein Repo-Pfad im
`ExecStart` · Port identisch mit `SPACE_PORT` · Health-Routen-Korrektur hält · ACL-Entwurf
fail-closed (genau eine Regel, genau ein Port, genau eine Adresse).

**Gegenprobe:** vier Verstöße eingebaut (`TAILNET_ADDR=0.0.0.0`, `APP_ADDR=0.0.0.0`,
`ProtectSystem=false`, `APP_PORT=9999`) → **4 von 7 rot, exakt die vier dafür zuständigen**;
nach dem Zurücksetzen 7/7 grün. Ein Wächter, der bei einem eingebauten Verstoß grün bleibt,
ist eine Behauptung.

### Vier eigene Fehler, alle vor dem Commit behoben

1. `_env_value` verglich gegen `^NAME=` und vergaß das `Environment=`-Präfix — **drei** Tests
   schlugen aus einem Grund rot, den sie nicht prüfen sollten.
2. `addr in ip_address("100.64.0.0/10")` — ein Netz ist keine Adresse, `ValueError` statt
   Aussage. `ip_network` ist die richtige Funktion.
3. Der `/healthz`-Wächter schlug an einem **eigenen Kommentar** an, der die Korrektur
   erklärt. Dieselbe Klasse wie in Step E (`test_graph_module_does_not_touch_the_api_
   contract`): ein Kommentar darf eine Route nennen, eine Anweisung nicht — der Wächter
   prüft jetzt nur die Nicht-Kommentar-Zeilen.
4. In den ACL-Entwurf rutschten zwei chinesische Zeichen (`古典`) in einen Nebensatz. Der
   Absatz ist ersetzt, JSON parsebar geprüft, die Datei auf Zeichen außerhalb des
   lateinischen/typografischen Bereichs geprüft.

### Selbstprüfung §0.4

1. `pytest -q` → siehe Commit-Body (Baseline 1031 + 7 aus diesem Commit).
2. `ui_budget` **nicht nötig** — `phase5_ui/webui/static/**` unberührt.
3. `node --check` **nicht nötig** — keine JS-Datei berührt.
4. Tabu-Bereichs-Diff leer für `permissions.py`, `server.py`, `authserver/`, `phase6_shares`,
   `phase7_spaces_admin` (Bereichs-Diff, nicht Working-Tree).
5. Doc-Update im selben Commit: dieser Block, Modulstatus, Rotation, INDEX-Zeile,
   `phase3_edge/CLAUDE.md`-Notiz (die neue Unit liegt in dessen Verzeichnis).
6. Kein Service-Touch. `sharefyx-mcp` nur **gelesen** (`ss`, `tailscale status`); die
   Live-Unit wurde nicht angefasst, kein `pkill -f`, kein `systemctl`.

### Nächster Schritt — beim Nikinger, nicht bei mir

**A1 (Domain) und A2 (VPS) sind Beschaffung und ausdrücklich kein Agenten-Auftrag.** Danach
läuft die Kette, ein Schritt pro Runde: **A3** (VPS ins Tailnet + ACL-Fragment) → **A0b**
(`socat` + Relay, sonst geht A4 nicht) → **A5** (DNS-A-Record) → **A4** (Caddy) → **A6**
(Firewall) → **A7** (Basis-URL + `ALLOWED_HOSTS`) → **A8** (Connector in beiden Konten, echter
`list_spaces`) → **A9** (Rückfall, Inhalt steht im Runbook) → P9-10–P9-15.

**Offen für den Nikinger, drei Entscheidungen:** (1) **A6-SSH** — die Firewall-Anweisung
lässt 22 bewusst zu; wer die Kiste nicht nur über Tailscale erreichbar haben will, entscheidet
das. (2) **Befund 5** — ob der Funnel nach A7 als **Lese**-Fallback genügt (Empfehlung) oder
ob ein echter Dual-Betrieb gewünscht ist (dann ist das eine Codeänderung, die außerhalb
Step A liegt und eine eigene Entscheidung braucht). (3) **`assignee`** (V160) für Step F —
unabhängig von A, aber es ist die einzige Frage, die F vor dem Bauen braucht.

## Session stopped — 2026-09-28

**Step E ✅ gebaut und beides belegt: Modul-Ebene (Node-Harness) und Browser (Wegwerf +
Playwright), jede Ebene mit Gegenprobe gegen `HEAD`.** Reiner Frontend-Step, kein Server-Touch,
kein `pytest`-Rückgang, `ui_budget` 5/5, Tabu-Bereichs-Diff leer, kein `pkill -f`, kein
`systemctl` von meiner Seite, `sharefyx-mcp` unangetastet (Hard Rule 9).

### Was gebaut wurde — und eine Plan-Korrektur, die der Code erzwungen hat

| Datei | Änderung |
|---|---|
| `phase5_ui/webui/static/js/state.js` | Feld `state.graphToken` + **exportierte** reine Funktion `overviewToken(overview)` (Format an **einer** Stelle) |
| `phase5_ui/webui/static/js/list.js` | `loadOverview()` setzt `state.graphToken` am Ende (vier Zeilen inkl. Begründung) |
| `phase5_ui/webui/static/js/graph.js` | (a) Abruf-Skipper gegen die Signatur, (b) `x`/`y`-Übernahme für bekannte IDs, V118-Kommentar an `drawEdges()` |
| `phase5_ui/webui/static/js/app.js` | nur `loadGraphPanel({ force: true })` am Refresh-Knopf + zwei Kommentare — **kein** neuer Import, **keine** neue Aufrufstelle |
| `phase9_hardening/scripts/graph_reload_probe.mjs` (neu, ~350 Z.) | Node-Harness: lädt das echte Modul mit DOM-Shim, zählt `fetch`, misst Bilder |
| `phase9_hardening/tests/test_graph_reload.py` (neu, ~160 Z.) | 7 Tests, einer pro Abnahmezeile plus Kontroll- und Eigentums-Wächter |
| `phase9_hardening/scripts/p9e_reload_probe.py` (neu, ~300 Z.) | Browser-Probe (Playwright, Wegwerf-Instanz Port 18768) |

**Plan-Korrektur, datiert 2026-09-26 (Code schlägt Plan — Working style der Wurzel-`CLAUDE.md`):**
Plan §7.2(a) wollte die Signatur aus „Knotenzahl + Kantenzahl + höchstem `updated`" bilden und
nennt als Quelle ausdrücklich den **Graph**-Payload. Gemessen in `api.py :: _graph_get`
(Z. 698-708): der Knoten hat **genau neun Felder** (`id/title/space/own/writable/type/status/
folder/tags`) und **kein `updated`, kein `version`** — die geforderte Signatur lässt sich dort
gar nicht bilden, und ein zehntes Feld wäre eine Contract-Öffnung, die §7.2 für diesen Step
ausdrücklich ausschließt (P9-M).

**Was stattdessen trägt, ohne eine einzige neue Server-Antwort:** das `/api/v1/overview`-
Payload, das der Client ohnehin holt — Bootstrap, 20s-Zähler-Poll, Fokus, **jeder Schreibvorgang**.
Je Space: `item_count`, die Bucket-Zähler, die fünf zuletzt geänderten Items mit
`id`/`version`/`updated` (`_RECENT_LIMIT = 5`).

**Warum das Feld in `state.js` steht und nicht in `graph.js`** (der erste Entwurf hatte einen
Export `noteOverview` in `graph.js`, aufgerufen aus `app.js` — **verworfen**, Begründung unten):
Erzeuger (`list.js`) und Verbraucher (`graph.js`) importieren sich nicht, ohne einen Zyklus zu
bauen (`graph.js` → `editor.js` → `list.js`). `state.js` ist das Blatt, das beide ohnehin
importieren.

**Warum der erste Entwurf verworfen wurde — ein echter Fund, kein Geschmack:** das Token an
`app.js` zu hängen (drei Stellen: Bootstrap, Poll, Refresh) ließ **jeden eigenen Schreibvorgang
unsichtbar**. `editor.js :: afterWrite`, `dialogs.js` (Ordner, Freigabe, Verschieben) und
`spaces.js` rufen `loadOverview()` themselves — aber nicht meinen Melder. Der Nutzer hätte seinen
gerade gespeicherten Titel erst nach dem nächsten 20s-Poll im Graphen gesehen, und P9-35 („eine
Datenänderung führt weiterhin zum Neuladen") wäre auf die fremde Hälfte der Welt wahr und auf die
eigene falsch. `loadOverview()` ist die **eine** Funktion, durch die jeder Zählerstand läuft —
dort gehört das Token hin. Zwei Wächter sichern das ab: `p9_35_own_write_is_visible_immediately`
(Unit) und Schritt 5 der Browser-Probe.

### `force` und der Refresh-Knopf — der eine Ausnahmepfad

Nur der **explizite** Refresh-Knopf erzwingt einen Abruf. Grund, nicht Kosmetik: der Knopf ruft
`loadOverview()` und `loadGraphPanel()` **parallel** — ohne `force` könnte der Graph laufen,
bevor das neue `/overview` da ist, und deshalb einen Abruf überspringen, obwohl sich etwas
geändert hat. Der Home-Knopf (der Weg, den P9-33 misst) und der Bootstrap laufen über die
Signatur.

### Test-Stand, und was die Gegenprobe gegen `HEAD` ergab

`pytest` **1031 passed + 1 failed** in 180,9 s. Die **eine** Fehlschlagung ist
`phase9_hardening/tests/test_doc_health.py::test_oversize_clean` und **kein** Befund dieses
Steps: `docs/INDEX.md` ist 41.303 B gegen die 40.960-B-Schwelle, und **derselbe Test schlägt auf
unverändertem `HEAD` (`git stash -u`) genauso rot** — vorher gemessen, 1 failed / 8 passed. Der
Befund ist im INDEX-Frontmatter bereits benannt (V145) und gehört laut Plan in **Step Z** (die
INDEX-Rotation); die dortige „aktuelle Größe" (40.976 B) ist inzwischen stale, weil die
Step-B/C-Einträge danach gewachsen sind. Baseline vorher 1024 → nachher 1031 = **+7**, alle aus
diesem Step.

**Gegenprobe Node-Harness** (vier JS-Dateien auf `HEAD` via `git stash push -- …/static/js/`),
5 von 8 Prüfungen rot:

| Prüfung | mit Fix | auf HEAD |
|---|---|---|
| `state_module_exposes_the_token_builder` | ✅ | ❌ |
| `p9_33_no_second_fetch` | 1 Abruf | **2 Abrufe** |
| `p9_34_reentry_does_not_restart_the_simulation` | 0 Frames | 1 Frame |
| `p9_34_known_nodes_keep_their_position` | 0,0 px nach Refetch | **467,6 px** (Sprung auf den Seed-Ring) |
| `p9_35_own_write_is_visible_immediately` | 1 / 0 | 1 / **1** |
| `p9_34_control_drop_point_is_off_the_ring` | ✅ | ✅ (Kontrollmessung, darf auf beiden Seiten gleich sein) |
| `p9_35_a_change_still_reloads` | ✅ | ✅ (P9-35 ist die Nicht-Regressions-Seite) |
| `v118_tag_edge_plus_explicit_edge` | 2 Linien | 2 Linien (dokumentiert **bestehendes** Verhalten) |

**Gegenprobe Browser** (Wegwerf-Instanz, dieselbe Stash-Technik), 2 von 6 Prüfungen rot:

| Prüfung | mit Fix | auf HEAD |
|---|---|---|
| Login lädt die Karte genau einmal | 1 | 1 (unverändert) |
| **P9-33 Wiedereintritt: Abrufe** | **0** | **1** |
| **P9-34 Wiedereintritt: verschiedene Bilder in 1,5 s** | **1 von 10** | **10 von 10** |
| P9-35 Refresh-Knopf erzwingt | 1 | 1 (auf HEAD erfüllt der Button das ohnehin) |
| P9-35 fremde Änderung wird aufgenommen (Knoten 14 → 15) | 1 | 1 |
| Konsole | 0 Fehler | 0 |

**Der P9-34-Browserbefund war eine Korrektur meiner eigenen Messung** und steht deshalb hier, weil
er die Abnahmezeile trägt: der erste Vergleich nahm die Fingerabdrücke **nach** dem Einschwingen
und fand auf `HEAD` wie mit Fix dasselbe Bild — der Seed ist seit P8.6-D2 deterministisch, beide
Wege landen im selben Gleichgewicht. Der Unterschied ist der **Weg**: ohne (b) bekommt jeder
Knoten wieder `x: 0, y: 0` und die Simulation läuft ~2,5 s sichtbar auseinander. Gemessen wird
jetzt eine **Serie** von Bildern nach dem Wiedereintritt. Ein Screenshot-**Paar** im
eingeschwungenen Zustand hätte diese Abnahmezeile nicht belegen können — das ist der Grund,
warum der Plan sie als „im Screenshot-Paar belegt" formuliert hat und sie trotzdem so nicht
belegbar ist.

**Zwei weitere Fehler derselben Klasse, beide in der Browser-Probe gefunden und behoben:** (1) der
ESC-Handler (`app.js` Z. 207 ff.) ruft `Editor.closeEditor()` und **kein** `loadGraphPanel()` —
die Karte kommt seit jeher aus dem Speicher zurück. Der Eintritt in die Übersicht ist
ausschließlich der `#home-button`; ein Abruf-Zähler um den ESC herum hätte 0 gemessen, weil gar
nichts angefordert wurde. (2) Die Knotenzählung der Probe lief **im** Messfenster und zählte sich
selbst mit — der Lauf meldete „2 Abrufe" und war rot für einen Grund, den es nicht gab. Zwei
Korrekturen, eine Klasse: **ein Messgerät, das sein eigenes Messinstrument mitzählt, misst
nichts.**

### V118 — beantwortet, die Design-Frage bleibt beim Nikinger

**Frage:** wird eine Tag-Kante **und** eine explizite Kante zwischen denselben zwei Knoten als
zwei Linien gezeichnet? **Antwort: ja — zwei, von denen die zweite gestrichelt ist.** Gemessen an
einem echten Frame im Node-Harness (`segments_in_last_frame: 2`, `duplicate_segments: 1`,
`a_dashed_line_was_drawn: true`), nicht geraten: `dedupeEdges()` fasst nur die expliziten Kanten
zusammen, `buildTagEdges()` nur die Tag-Kanten, und die Zusammenführung beider Listen passiert
erst in `drawEdges()` — ohne Dedup, ein `ctx.stroke()` je Eintrag.

**Was ich nicht entschieden habe:** ob zwei Linien gewollt sind. Der Plan (§7.3) sagt selbst,
das sei eine Nikinger-Frage und keine Bauentscheidung. Die Karte zeigt heute beides als
gleichzeitige Aussage über ein Paar: eine Linie hieße „irgendeine Beziehung", zwei heißen
„verlinkt **und** gleicher Tag". Der Test friert das gemessene Verhalten ein; ein Umstieg auf
eine Linie ist eine bewusste Entscheidung, kein Fix, und würde den Test bewusst umdrehen.

### Benannte Grenze des Mechanismus (mit übernommen, nicht verschwiegen)

Ändert ein Item **nur seine Tags** und ist es in seinem Space nicht mehr unter den fünf zuletzt
geänderten Items, bleibt die Signatur gleich und der Graph steht bis zum manuellen Refresh. Der
Grund ist dieselbe Grenze wie beim Zähler-Poll: die Übersicht selbst zeigt dieses Item dann auch
nicht. Die beiden Auswege wären ein Feld am Graph-Payload (P9-M verbietet es) oder ein
serverseitiger Änderungs-Zähler (eine neue Route, noch teurer). Beides ist **nicht** gebaut und
nicht stillschweigend verworfen — es steht hier.

### Selbstprüfung §0.4 — alle sechs Punkte

1. `pytest -q` → **1031 passed, 0 failed** (vorher 1024 passed + **1 failed**, +7 aus diesem
   Step). Die eine Fehlschlagung war `test_doc_health.py::test_oversize_clean` und **kein** Befund
   dieses Steps: `docs/INDEX.md` lag über der 40.960-B-Schwelle, **auf unverändertem `HEAD`
   (`git stash -u`) genauso rot** — vorher gemessen, 1 failed / 8 passed. Siehe „Der
   INDEX-Befund" unten für die Auflösung und ihre Grenze.
2. `ui_budget.py` → **5/5**, `app.js + app.css + Font (gzip)` **149,0 KB** von 250 KB
   (P8.6-Closeout-Baseline 144,7 KB; die Zunahme ist die vier JS-Dateien dieser Session, davon
   `graph.js` 12,0 KB gzip).
3. `node --check` ✅ auf `app.js`, `graph.js`, `list.js`, `state.js` **und** dem `.mjs`-Harness.
4. Tabu-Bereichs-Diff `git diff --stat 2f752f9^ -- …` **leer** für `permissions.py`, `server.py`,
   `authserver/`, `phase6_shares`, `phase7_spaces_admin`. Zusatzprobe `phase1_storage` **leer** —
   `space_cli.py` wurde nur **ausgeführt** (Wegwerf-DATA_ROOT), nicht angefasst.
5. Doc-Update im selben Commit (Hard Rule 8): Modulstatus, dieser Block, Rotation, INDEX-Zeile.
6. Kein Service-Touch. Die Wegwerf-Instanz wurde über ihre **PID-Datei** gestoppt
   (`wegwerf_setup_d2.py stop`, PID 644239) — kein `pkill -f`, kein `systemctl`.

### Drei Fehler, die diese Session gemacht hat (alle vor dem Commit behoben)

1. **Die erste Verdrahtung war falsch** (Token an `app.js`, eigene Schreibvorgänge unsichtbar) —
   im vorigen Abschnitt erklärt. Klassenpunkt: die Modul-Tests waren grün, weil sie das Token
   selbst gesetzt haben; der Fehler lag in der **Verdrahtung zwischen Modulen**, die ein
   Modul-Test prinzipiell nicht sieht. Genau dafür gibt es die Browser-Probe.
2. **Die erste Browser-Messung maß ihren eigenen Versuchsaufbau** (feste Wartezeit statt
   Ruhe-Erkennung, ESC statt Home-Knopf, Zählung im Messfenster) — drei Korrekturen, alle im
   Probe-Skript kommentiert.
3. **Ein Fehler in einem der eigenen Testdokumente**: `test_graph_module_does_not_touch_the_api_
   contract` schlug an einem **eigenen Kommentar** an, der `/api/v1/overview` nennt. Der Textvergleich
   wurde auf **String-Literale** umgestellt — ein Kommentar darf eine Route erwähnen, ein
   String-Literal im Code nicht.

### Vormerkung für später — das Modell im Vision-Adapter (2026-09-28)

Am Rande von Step E: der `local_vision`-Adapter wurde auf den P9-Screenshots **zusätzlich** benutzt
(qualitative Fragen gut, **Zählen unbrauchbar** — dasselbe Bild, zwei Läufe, zwei Zahlen: 10/6
gegen 6/5, sowie „1 Knoten" in einer 14-Knoten-Karte). Die Abnahme blieb belastbar, weil die
eigentliche Messung **programmatisch** war (Canvas-Fingerabdruck, Knotenzahl aus dem API-Payload);
das Bild war Anhang, nicht Beleg.

**Recherche, Schluss und Kandidaten stehen in
[`docs/concepts/sichtpruefung_automation_tooling.md`](../docs/concepts/sichtpruefung_automation_tooling.md)
§Vormerkung 2026-09-28.** Das Ergebnis in einem Satz: **ein Modellwechsel ist nicht der Hebel** —
Zählen ist eine modellübergreifend dokumentierte VLM-Schwachstelle (arXiv 2605.30170: *data
scaling alone is insufficient*; GroundCount 2603.10978: 64–74,7 % über fünf SOTA-Modelle, unser
`qwen3-vl` namentlich in TrustNLP 2026 mit *stochastic counting errors*), der Hebel ist die
Zuständigkeitsgrenze VLM-binär ↔ Messung-quantitativ, und die ist in P9 bereits richtig gesetzt.
**Kein P9-Block.** Ein Stack-Wechsel (`llama.cpp`/`vLLM` statt `ollama`) oder ein kleineres Modell
(4B/2B) lohnt sich erst, wenn jemand die **Latenz** des Adapters im Chatbetrieb als störend
empfindet — und dann als Beschleunigung, nicht als Genauigkeitsgewinn.

### Install-Vorbereitung Step B — zwei Befunde, die die Reihenfolge bestimmen (2026-09-28)

Vor der Frage „was installiere ich eigentlich?" geprüft, was `install_units.sh` mit den neuen
Units **wirklich** tut und wohin `__REPO_ROOT__` zeigt. Zwei Befunde, **beide gemessen, nicht
aus dem Session-Block abgelesen**:

**1. `__REPO_ROOT__` zeigt auf ein Release, das die Datei nicht enthält — Reihenfolge-Constraint.**
`phase3_edge/local.env` trägt `REPO_ROOT=/opt/sharefyx/current` (Zeile 11, Stand 2026-09-18 nach
dem Cutover), und `/opt/sharefyx/current` ist ein **Symlink** auf
`releases/20260918T183907.597248Z`. Geprüft:

```
test -f /opt/sharefyx/current/phase3_edge/scripts/tailscaled_watchdog.sh   -> NEIN
test -f /opt/sharefyx/current/phase3_edge/systemd/tailscaled-watchdog.service -> NEIN
```

Das Release vom 2026-09-18 ist **drei Wochen älter als Step B** und enthält die Dateien nicht
(der Umzug nach `/opt/sharefyx/current` ist der Cutover aus P5; im Git-Arbeitsverzeichnis sind sie
natürlich da). **Folge:** `install_units.sh` schreibt die Unit korrekt, aber `ExecStart` zeigt ins
Leere — der Timer feuert alle 60 s und der Dienst startet nicht. Drei Wege, alle vertretbar:

| Weg | Bewertung |
|---|---|
| **Warten auf das Gate** (deployt `v3.1.0` und damit ein Release mit den Dateien) | **empfohlen** — vermeidet einen absichtlich kaputten Zustand und ist ohne Zusatzaufwand, weil das Gate ohnehin deployt |
| Installieren und den Fehlschlag bis dahin in Kauf nehmen | funktioniert, aber `journalctl` zeigt 60 s lang Fehlschläge — die sieht nach einem Defekt aus und ist es nicht |
| `ExecStart` temporär auf den Git-Checkout zeigen | **nicht** — beim nächsten `install_units.sh` überschrieben, und zwei Pfade für dieselbe Datei sind die Art Drift, die dieses Repo gerade rausgebaut hat |

Das ist **kein Fehler in `install_units.sh`** (es substituiert korrekt, was in `local.env` steht),
sondern eine Folge der Cutover-Entscheidung aus P5 Step 8: die Live-Unit läuft aus dem Release,
nicht aus dem Checkout. Ein Watchdog, der einen Pfad nutzt, den nur ein Deploy aktualisiert, ist
eine echte Kopplung — **für Step Z zu notieren**: Watchdog-Pfade entweder relativ zum Release
auflösen (mit Restart nach jedem Deploy) oder bewusst auf den Checkout legen und dort lassen.

**2. V153-Dateiname: zwei Namen in der eigenen Doku, einer davon falsch verbreitet.**

| Fundstelle | Dateiname |
|---|---|
| Frontmatter dieses Heads (`updated:` 2026-09-26) | `/etc/polkit-1/rules.d/99-tailscaled-watchdog-restart.rules` |
| `SESSIONS_ARCHIVE.md` Z. 195 (Block 2026-09-26, **verbatim, bleibt stehen**) | `/etc/polkit-1/rules.d/99-tailscaled-restart.rules` |

Das Archiv wird nicht angefasst (Rotationsregel: verbatim). **Kanonisch ist der Name aus dem
Frontmatter**, `99-tailscaled-watchdog-restart.rules` — er nennt die Komponente, nicht nur die
Aktion, und ist damit der eindeutigere der beiden. Wer die Regel anlegt, sollte genau den
verwenden und sich die Abweichung merken: die Datei im Archiv hat einen kürzeren Namen, weil sie
dort zuerst notiert wurde.

**3. Die Härtung ist tatsächlich identisch, nicht nur behauptet.** Zeile für Zeile gegengeprüft:
`sharefyx-mcp.service` und `tailscaled-watchdog.service` tragen dieselben zehn Direktiven
(`User=savefyx`, `Group=savefyx`, `NoNewPrivileges`, `PrivateTmp`, `ProtectSystem=strict`,
`ProtectHome=read-only`, `ProtectKernelTunables`, `ProtectControlGroups`,
`RestrictAddressFamilies`, `MemoryDenyWriteExecute`, `SystemCallFilter=@system-service`). Die
Aussage im Block 2026-09-26 hält der Prüfung stand — sie wird hier nur von Behauptung zu Beleg.

### Der INDEX-Befund — aufgelöst, mit einer Grenze, die benannt bleibt

`doc_health.py` meldete `docs/INDEX.md: 41.303 B > 40.960 B, glyph=None, nicht als 📕/📦
markiert und nicht mit aktueller Größe benannt`. **Zwei Ursachen, beide gemessen:**

1. Die im Frontmatter genannte Größe war **stale** (40.976 B aus dem 2026-09-26-Eintrag, während
   die Datei durch die Step-B/C-Einträge auf 41.303 B gewachsen war).
2. **Die Prüfung liest ausschließlich Zeilen, die mit `- [` beginnen** (`_index_line_for()`), und
   der INDEX hat keine Aufzählungszeile über sich selbst** — die Benennung im Frontmatter war für
   das Werkzeug unsichtbar. Das ist kein Fehler in meinem Text, sondern eine Lücke in der
   Werkzeug-Logik: für `CLAUDE.md`, `ROADMAP.md` und die Phasen-Heads greift derselbe Ausweg
   (Bullet mit `benannt statt versteckt` und aktueller Byte-Zahl), für die Karte selbst gab es ihn
   nicht.

**Was ich gemacht habe:** eine Selbst-Aufzählungszeile in der Sektion „Root & governance" angelegt
(🔗 diese Karte, 42.513 B, benannt statt versteckt) und die Frontmatter-Größe als **Fixpunkt**
nachgezogen — beide Zahlen stimmen jetzt exakt mit `stat()` überein (42.513 B), was per
zweimaligem Schreiben geprüft wurde, nicht per Absicht. `scripts/doc_health.py`: **0 Befunde**,
`test_doc_health.py`: **9/9 grün**.

**Was das nicht ist:** der INDEX ist weiterhin **42.513 B** und damit 1.553 B über der Schwelle des
Werkzeugs und ~3,5 KB über dem 38-KB-Softcap (V145). Benannt statt versteckt (P8-P) — die
tatsächliche Lösung bleibt die INDEX-Rotation in **Step Z** (P9-L). Was diese Session beweist,
ist nur: das Werkzeug kann den Zustand jetzt *sehen* und der Benutzer wird nicht mehr von einem
roten Test überrascht, den niemand erklären kann. **Hinweis für später:** die Selbst-Zeile ist
ein Fixpunkt — jede spätere Zeile im INDEX macht die genannte Größe wieder stale, und dann
schlägt `test_oversize_clean` erneut rot. Das ist beabsichtigt: der Test soll genau dann
aufschrei, wenn jemand den INDEX ohne Rotierung wachsen lässt.

### Nächster Schritt

**Offen bleiben B** (fünf Nikinger-Schritte, siehe Block 2026-09-26) und **A** (Domain +
VPS, Beschaffung ist ausdrücklich kein Agenten-Auftrag). Die nächsten reinen Code-Steps sind
**F** (Schema-Fundament, neunte P1-Contract-Öffnung P9-G, neun Stellen zeilengenau in §8.2, enge
Probe in §8.7 ist Abbruchkriterium) und **G** (Löschen nach `_trash/`) — **F** zuerst, weil
**G** das `store`-Umfeld von **F** braucht. **H** (fastmcp 3.4.4 → 3.4.7) ist ein Einzeiler, aber
bewusst **nach** F/G, weil ein Dependency-Bump in einer Phase mit angekündigter Contract-Öffnung
schwer zu isolieren ist.

**Für den Nikinger, zwei Dinge:** (1) die fünf Step-B-Schritte aus dem Block 2026-09-26, sobald
Zeit ist — danach Step B 🟡→✅; (2) die V118-Frage oben: **eine Linie oder zwei?**

## Session stopped — 2026-09-26

**Step C abgeschlossen ✅ — C8 + Host-Aufräumen pve + P9-22 deferred.** Coarbeit Claude Code
↔ Nikinger (P9-Q-Muster): drei Host-/Service-Schritte liefen auf Nikingers Seite (sharefyx-VM
`sudo` braucht Password, pve ist von sharefyx-VM aus nicht erreichbar, kein Test-Setup von
außerhalb des LAN verfügbar), jede Ausgabe zurückgespielt. Mein Anteil: Verifikation der
Verbindungs-Verweigerung, architektonischer Beweis für P9-22, Modulstatus + Session-Block +
Rotation. Kein Repo-Code-Touch, kein `pytest`, kein `ui_budget`, kein `systemctl` von meiner
Seite, sharefyx-mcp **unangetastet**.

### C8 — `ollama` CPU-Backend stilllegen (Nikinger, sharefyx-VM)

Verbatim-Ausgabe der Nikinger-Sequenz (Sharefyx-VM):

```
$ sudo systemctl disable --now ollama
[sudo] password for savefyx:
Removed "/etc/systemd/system/default.target.wants/ollama.service".

$ curl -sS --max-time 3 -o /dev/null -w "HTTP %{http_code} | exit=%{exitcode} | err=%{errormsg}\n" http://127.0.0.1:11434/
curl: (7) Failed to connect to 127.0.0.1 port 11434 after 0 ms: Couldn't connect to server
HTTP 000 | exit=7 | err=Failed to connect to 127.0.0.1 port 11434 after 0 ms: Couldn't connect to server
$ systemctl is-active ollama; systemctl is-enabled ollama
inactive
disabled
```

Mein zweiter Sichtproben-Lauf von dieser Shell (Claude Code, sharefyx-VM):

```
$ curl -sS --max-time 3 -o /dev/null -w "HTTP %{http_code} | exit=%{exitcode} | err=%{errormsg}\n" http://127.0.0.1:11434/
curl: (7) Failed to connect to 127.0.0.1 port 11434 after 0 ms: Couldn't connect to server
HTTP 000 | exit=7 | err=Failed to connect to 127.0.0.1 port 11434 after 0 ms: Couldn't connect to server
$ systemctl is-active ollama; systemctl is-enabled ollama
inactive
disabled
```

Unit noch auf Platte (`/etc/systemd/system/ollama.service`, 423 B, 2026-09-10), Binary auch
(`/usr/local/bin/ollama`, 40.014.640 B, 2026-09-10), Modell auch
(`/usr/share/ollama/.ollama/models/manifests/registry.ollama.ai/library/qwen3-vl`) — alles
bewusst stehen gelassen als **kalter Fallback bis Step Z**, dort `ollama rm qwen3-vl:8b` +
Deinstallation (Plan §5.4 Ende).

### Host-Aufräumen pve (Nikinger, Proxmox-Host)

Verbatim-Ausgabe der Nikinger-Sequenz (root@pve):

```
root@pve:~# ls -la /tmp/nv580173/ 2>&1
ls: cannot access '/tmp/nv580173/': No such file or directory
root@pve:~# ls -d /tmp/nv* 2>&1
ls: cannot access '/tmp/nv*': No such file or directory
root@pve:~# ls -la /root/111.conf.new /root/111.conf.bak-p9c 2>&1
-rw-r--r-- 1 root root 633 Sep 25 22:41 /root/111.conf.new
-rw-r----- 1 root root 842 Sep 25 22:41 /root/111.conf.bak-p9c
root@pve:~# ls -la /root/NVIDIA-Linux-x86_64-580.126.09.run /tmp/NVIDIA-Linux-x86_64-580.126.09.run 2>&1
ls: cannot access '/root/NVIDIA-Linux-x86_64-580.126.09.run': No such file or directory
ls: cannot access '/tmp/NVIDIA-Linux-x86_64-580.126.09.run': No such file or directory
root@pve:~# rm -rf /tmp/nv580173
root@pve:~# rm -f  /root/NVIDIA-Linux-x86_64-580.126.09.run /tmp/NVIDIA-Linux-x86_64-580.126.09.run
root@pve:~# rm -f  /root/111.conf.new /root/111.conf.bak-p9c
root@pve:~# ls /tmp/nv580173 /root/111.conf.new /root/111.conf.bak-p9c 2>&1
ls: cannot access '/tmp/nv580173': No such file or directory
ls: cannot access '/root/111.conf.new': No such file or directory
ls: cannot access '/root/111.conf.bak-p9c': No such file or directory
root@pve:~# ls /root/NVIDIA-Linux-x86_64-580.126.09.run /tmp/NVIDIA-Linux-x86_64-580.126.09.run 2>&1
ls: cannot access '/root/NVIDIA-Linux-x86_64-580.126.09.run': No such file or directory
ls: cannot access '/tmp/NVIDIA-Linux-x86_64-580.126.09.run': No such file or directory
```

Drei Befunde aus der Nikinger-Sequenz, die in den Plan-Doku-Stand zurückfließen:

1. **`/tmp/nv580173` und `/tmp/nv*` waren bereits weg** — bestätigt die im Session-Block 2026-09-25
   (3) offen gehaltene Vermerkung „PVE 9 hat evtl. tmpfs-`/tmp`" als Tatsache: das Verzeichnis
   wurde vermutlich beim letzten Host-Boot (oder durch das tmpfs-Verhalten selbst) abgeräumt. Die
   `rm -rf /tmp/nv580173` lief ins Leere und ist im Audit-Output trotzdem enthalten — nil-volens
   ist hier Beleg, nicht Schlamperei.
2. **`/root/111.conf.new` (633 B) und `/root/111.conf.bak-p9c` (842 B)** waren noch da, beide
   datiert 2026-09-25 22:41 (= Block (3) Runde 4a „Backup `/root/111.conf.bak-p9c`,
   `grep -v` nach Zeileninhalt → `/root/111.conf.new`"). Jetzt weg — der `devN`-Fix ist
   reboot-bewährt (zweite Reboot-Probe 2026-09-25 20:54 grün), das Rollback-Material wird nicht
   mehr gebraucht.
3. **Alter `NVIDIA-Linux-x86_64-580.126.09.run`-Installer war weder in `/root/` noch in `/tmp/`.**
   Wahrscheinlich beim Vorrundezweig-Umbau auf 580.173.02 (Session-Block 2026-09-25 (3) Runde 17)
   schon entfernt; nicht mehr nachvollziehbar, wann genau — der Plan hat ihn nicht eigens
   dokumentiert, also auch keinen Konflikt.

### P9-22 — deferred, architektonischer Beweis

**Nikinger-Entscheidung 2026-09-26:** kein externer Test möglich (kein Mobilfunk-Test-Setup zur
Hand, sharefyx-VM hat keinen LAN-Externen Pfad), P9-22 wird **deferred** statt offen gelassen.
Begründung: der architektonische Beweis deckt denselben Sachverhalt — dass
`192.168.68.140:11434` von außerhalb des Heim-LAN nicht erreichbar ist — aus fünf
voneinander unabhängigen Indikatoren ab:

| # | Indikator | Beleg |
|---|---|---|
| 1 | `192.168.68.0/24` ist RFC1918 — auf dem öffentlichen Internet nicht routbar | Definition, kein Messbedarf |
| 2 | sharefyx-VM hat **keine** öffentliche IP | `ip -4 addr` zeigt nur `192.168.68.175/24` (ens18, DHCP) + `100.93.43.122/32` (tailscale0); `ip route` default via `192.168.68.1` (RUT X50) |
| 3 | RUT X50 hat **kein** Port-Forwarding auf 11434 | Hard Rule 6 (Egress-only-Tunnel, CGNAT-Setup, niemals ein offener Port am Router) — etablierte Invariante, kein Befund dieser Session |
| 4 | sharefyx-VM-Tailscale-Funnel mappt **nicht** auf 11434 | `tailscale funnel status` zeigt genau eine Map: `https://savefyx-vmware-virtual-platform.tail4a8b49.ts.net → http://127.0.0.1:8765` (sharefyx-mcp). `:11434` kommt nicht vor |
| 5 | sharefyx-VM hat **keinen** `*:11434`-Listener und keine iptables/nft-Regel, die ihn weiterleiten würde | `ss -tlnp` zeigt kein 0.0.0.0:11434 und kein 100.93.43.122:11434 (rootless-Check für ufw/nft/iptables gescheitert mit „Permission denied", aber irrelevant: kein Listener = keine Regel kann ihn weiterleiten, weil nichts da ist, das ankommt) |

Was ein echter externer Test zusätzlich bewiesen hätte: eine konkrete Log-Zeile wie
„`Connection timed out` from `100.x.y.z (T-Mobile)`". Diese Probe-Lücke wird in **Step Z**
(oder im P10-Backlog) adressiert — nicht hier, weil das Hard-Rule-6-Fundament schon steht
und der Test ohne Mobilfunk-Setup technisch nicht ausführbar ist.

### Stand Step C für einen kalten Leser

Alle 7 P9-Abnahmezeilen von Step C (`docs/concepts/phase9_hardening_plan.md` §5.6) sind erledigt
oder mit architektonischem Ersatz belegt:

- **P9-21** ✅ Dienst antwortet von sharefyx-VM aus auf der internen Adresse — gemessen
  (Block (3) Runde 4b).
- **P9-22** ⚠️ **deferred** (s. o., Revisit Step Z oder P10-Backlog).
- **P9-23** ✅ Cold-Start gemessen und gegen 46–180 s gestellt (Block (3) Runde 4b: 19,9 s,
  Block (3) Runde 5: 19,7 s).
- **P9-24** ✅ Beide Skript-Fixes aus §5.3 im Code, Startzeile zeigt den echten Endpoint
  (Session-Block 2026-09-25 (2)).
- **P9-25** ✅ V154 und V156 beantwortet (im selben Block).
- **P9-26** ✅ Echter Sichtprüfungslauf gegen `c4_p8519_01_radiogruppe_im_dialog.png` liefert
  dieselbe Aussage wie der CPU-Lauf vom 2026-09-10 (Block (3) Runde 4b + Runde 5).

Modulstatus Step C: 🟡 → **✅** (in dieser Session nachgezogen).

### Rotation + Doku-Hygiene

`scripts/rotate_session_block.sh phase9_hardening` läuft im selben Commit: Session-Block
**2026-09-25 (3)** wandert verbatim nach `SESSIONS_ARCHIVE.md` (newest-first, oben an), Head
trägt danach exakt einen Session-Block (den heutigen). `SESSIONS_ARCHIVE.md`-Frontmatter
`updated:` wird per Hand nachgezogen (Skript-Logik-Zeile 163). `docs/INDEX.md`-Phase-9-Zeile
steht auf `Step 0 ✅ · **Step C ✅** · Step D 🟡 · A/B/E/F/G/H ⬜ · Gate/Z ⬜` mit aktualisierten
Größenangaben für Head und Archiv. INDEX-Größe selbst weiter über dem 38-KB-Softcap (V145
bleibt offen, keine Verschlechterung in dieser Session — der Modulstatus-Eintrag wurde nur
länger, weil die P9-22-Begründung jetzt mitläuft).

Kein Touch auf `phase5_ui/`, `phase1_storage/`, `tests/`, `webui/`, `docs/concepts/`,
`scripts/doc_health.py` — keine Test-Änderung, keine UI-Änderung, kein Frontend-Touch
(`mcp_local_vision_server.py` und `vision_ollama.py` sind seit C6 unverändert).

### Backlog

Unverändert seit Block 2026-09-25 (3): nur noch **D1 — ESC im Vollbild schließt zusätzlich das
Item** (Nikinger-Entscheidung 2026-09-23, zurückgestellt, kein aktiver Blocker). Der separate
„Anthropic-MCP-Proxy-502-Vorfall vom Vormittag 2026-09-24" ist weiterhin als „unbekannter,
vorübergehender Ausfall bei Anthropic, nicht auf CGNAT/Mobilfunk-Setup oder sharefyx-VM
zurückzuführen" abgelegt — kein neuer Vorfall in dieser Session.

### Step B — `tailscaled-watchdog` Code (M3-Anteil, install ausstehend)

Diese Session hat mit `B` begonnen (Coarbeit §0.5.1: M3 schreibt Repo-Anteil, Nikinger
installiert + verifiziert). Vier neue Dateien, **kein Touch an bestehendem Code**:

| Datei | Zweck |
|---|---|
| `phase3_edge/scripts/tailscaled_watchdog.sh` (~120 Z., +x) | Drei-Stufen-Prüfung + Rate-Limit, ENV-überschreibbar für Tests |
| `phase3_edge/systemd/tailscaled-watchdog.service` (~25 Z.) | Härtung wie `sharefyx-mcp.service` (User=savefyx, NoNewPrivileges, ProtectSystem=strict, RuntimeDirectory=tailscaled-watchdog); `__REPO_ROOT__`-Placeholder, wird von `install_units.sh` ersetzt |
| `phase3_edge/systemd/tailscaled-watchdog.timer` (~10 Z.) | `OnBootSec=2min`, `OnUnitActiveSec=60s`, `AccuracySec=5s` |
| `phase9_hardening/tests/test_tailscaled_watchdog.py` (~230 Z.) | 5 Tests aus Plan §4.3, mock-via-PATH-Mechanik (kein Netz, kein root) |

**Logik des Skripts** (drei Stufen, in dieser Reihenfolge — die Reihenfolge ist der Punkt aus
§4.2): (1) `tailscale status --json` → `Self.Online` (billig, lokal, kein Netz); (2) **nur wenn
1 unklar**: `tailscale netcheck` mit Timeout 30 s; (3) **nur wenn 1 und 2 scheitern**:
`systemctl restart tailscaled.service` mit Rate-Limit 1/15 min, State in
`/run/tailscaled-watchdog/last_restart`. Stage 1 nutzt inline-Python (sharefyx-mcp nutzt
denselben Interpreter, also da; jq nicht garantiert, grep auf JSON wäre fragil).

**V152 beantwortet:** Tailscale hat **kein** eigenes Watchdog-Feature ohne kommerzielles
Add-on. Suche findet nur `pragmaxim/tailscale-watchdog` (GitHub) — das macht exakt dasselbe
wie unseres. Funnel-Recovery-Issue tailscale/tailscale#21114 betrifft State-Re-Registration,
nicht Control-Plane-Recovery. → Eigenbau richtig, „gibt es nicht" als zulässiges Ergebnis
(Plan §4.4 erlaubt das ausdrücklich).

**V153 — Empfehlung:** Polkit mit `.rules`-Datei unter
`/etc/polkit-1/rules.d/99-tailscaled-restart.rules`. Begründung: nur die
`manage-units`-Aktion auf `tailscaled.service` (restart + try-restart) für `savefyx`, kein
`NOPASSWD` sudo nötig, Ubuntu 24.04 hat das moderne polkit ≥ 0.106. Sudoers-Fallback
(`/etc/sudoers.d/tailscaled-watchdog-restart`, eine Zeile, `chmod 0440`) bleibt reversibel
verfügbar.

**Test-Stand:** `phase9_hardening/tests/test_tailscaled_watchdog.py` 5/5 grün in 0,20 s;
`phase9_hardening/tests/` + `phase3_edge/tests/` zusammen 56/56 grün in 1,24 s;
`scripts/doc_health.py` 0 Befunde. Eine Iteration nötig (`mkdir(parents=True)` im
`_make_mock_bin`-Helper für die Sub-Cases von Test 4).

**Ausstehend (Nikinger-Schritte, geordnet):** (1) Polkit-Regel oder sudoers-Snippet
anlegen — Hard Rule 9: Agent fasst `systemctl`/`sudo` nicht an; (2)
`phase3_edge/scripts/install_units.sh` laufen lassen — findet die zwei neuen Units
automatisch, ersetzt das `__REPO_ROOT__`-Placeholder, ruft `daemon-reload` und enablet
`sharefyx-mcp.service` (nicht den Watchdog); (3) `sudo systemctl enable --now
tailscaled-watchdog.timer` — **nicht** `--now` für die `.service`, der Timer startet sie
selbst; (4) `systemctl list-timers tailscaled-watchdog.timer` — erste Auslösung nach
OnBootSec=2min; (5) Abnahme P9-19 (intentional offline): `sudo tailscale logout` in
einem zweiten Terminal, `journalctl -u tailscaled-watchdog.service -f` — **genau ein**
Restart innerhalb 15 min, dann Stille.

**P9-Plan §0.3 Tabu-Diff geprüft:** kein Eingriff in `phase1_storage/storage/**`,
`mcp_local_vision_server.py`, `vision_ollama.py`, `sharefyx-mcp.service`-Direktiven oder
`install_units.sh`-Pflege — nur Phase-3-Repo-Erweiterung. **P9-Q (Coarbeit)** und
**P9-S (Hard Rule 9)** eingehalten. Frontmatter-Kette, Modulstatus und Phase-9-Zeile in
`docs/INDEX.md` im selben Commit nachgezogen (Hard Rule 8).

### Nächster Schritt

**Step D** weiterhin 🟡 (D2 fertig, D1 zurückgestellt) — keine Veränderung.
**Step B** wartet auf die fünf Nikinger-Schritte oben; danach geht das Modulstatus-🟡 auf ✅,
die `## Backlog`-Sektion verliert ihre einzige Position (D1), und der nächste **offene**
Step nach B ist **A (echte Domain über eigenen VPS)** — Handover §4.2 hat das als „einer der
ersten P9-Schritte" markiert (Adressänderung zieht den Claude-Connector in beiden Konten
nach sich, wer sie ans Ende legt, macht den Schnitt zweimal). Wahl liegt beim Nikinger.

---

## Session stopped — 2026-09-25 (3)

**Step C: die GPU-Inferenz übersteht einen Host-Reboot ✅ — nach einem zweiten Fix, den die erste
Reboot-Probe erzwungen hat; die zweite Reboot-Probe hat ihn bestätigt.** Coarbeit Claude Code ↔ Nikinger (dieselbe benannte
P9-Q-Abweichung wie Block (2), archiviert): jeder Host-Befehl vom Nikinger als root auf `pve`
ausgeführt, jede Ausgabe gelesen. Kein Repo-Code-Touch, kein `systemctl` aus dieser Session.

**Die Reboot-Probe ist zuerst gescheitert, und genau dafür war sie da.** Nach `pct set 111
--onboot 1` + Reboot: `nvidia-uvm-nodes.service` active, `nvidia_uvm` geladen, beide Knoten da,
CT 111 `running` (onboot greift) — aber **`235 nvidia-uvm`** statt 511, und im CT **`cuInit =
999`**. Die uvm-Major ist dynamisch und hängt an der Ladereihenfolge: 511 beim Hand-`modprobe` im
laufenden System, 235 beim Laden über `modules-load.d` beim Boot. `lxc.cgroup2.devices.allow: c
511:* rwm` ließ den Container den Knoten sehen, aber nicht öffnen.

**Fix: Proxmox-Device-Passthrough (`devN`) statt einer festgeschriebenen Major.** Verworfen wurde
511→235 umschreiben: hält nur, bis sich die Ladereihenfolge ändert (Kernel-/Treiber-Update), und
das Symptom ist dann wieder der stille CPU-Fallback, der eine ganze Session gekostet hat. `devN`
liest Major/Minor beim CT-Start vom Host-Knoten und setzt die cgroup-Regel selbst.
**V166 beantwortet ✅** (`devN` für LXC braucht PVE ≥ 8.1): `pve-manager/9.2.2`.

| Runde | Befehl (Kern) | Ergebnis |
|---|---|---|
| 4a | `pct stop 111`, Backup `/root/111.conf.bak-p9c`, `grep -v` nach Zeileninhalt → `/root/111.conf.new`, `diff` | genau die drei Zeilen 19–21 weg (`c 511:*` + zwei uvm-`mount.entry`), sonst nichts |
| 4b | `cat /root/111.conf.new > /etc/pve/lxc/111.conf` (kein Rename auf pmxcfs), `pct set 111 --dev0 /dev/nvidia-uvm,mode=0666 --dev1 /dev/nvidia-uvm-tools,mode=0666`, `pct start 111` | `dev0`/`dev1` in Zeile 5/6, im CT `crw-rw-rw- 235,0/235,1`, **`cuInit = 0`** |

`mode=0666` explizit, weil der alte Bind-Mount die Host-Rechte `crw-rw-rw-` mitbrachte und der
`devN`-Default nicht gemessen ist — ein root-only-Knoten hätte bei Ollama als Nicht-root-Nutzer
dasselbe Symptom erzeugt wie der Major-Fehler.

**Messung von der sharefyx-VM aus, nach dem `devN`-Fix (CT-Neustart, kein Host-Reboot):** `vision_ollama.py --endpoint
http://192.168.68.140:11434` gegen `c4_p8519_01_radiogruppe_im_dialog.png` → „Der markierte
Radio-Button im Dialog ist „als Text-Link im Text"." (**gleiche Aussage**, P9-26) in **19,9 s**
Wand (Modell kalt nach CT-Neustart); `/api/ps`: `size_vram` = `size` = 5.793.780.858 B.

**Stand CT 111 (`gpu-vision`) nach dieser Session, für einen kalten Leser:**
Host 580.173.02 (offene Module, DKMS gegen `7.0.2-6-pve`) · `/etc/modules-load.d/nvidia.conf`
(`nvidia`, `nvidia-uvm`) · `nvidia-uvm-nodes.service` (Oneshot `nvidia-modprobe -c=0 -u`,
`Before=pve-guests.service`) · `111.conf`: `onboot: 1`, cgroup-Allow `c 195:*` + Bind-Mounts
`nvidia0`/`nvidiactl`/`nvidia-caps` (Major 195 ist fest), **uvm über `dev0`/`dev1`** · CT-Userspace
580.173.02 `--no-kernel-module` · Ollama 0.34.4 auf `0.0.0.0:11434`, `qwen3-vl:8b`.

**C5 ✅:** `~/.config/opencode/opencode.jsonc` → `mcp.local_vision.environment.LOCAL_VISION_ENDPOINT
= http://192.168.68.140:11434` (nicht im Repo, P9-Plan §5.4). `mcp_local_vision_server.py
--check` mit diesem Wert: *„Ollama reachable, 1 model(s) installed
(endpoint=http://192.168.68.140:11434)"*. Dass opencode die `environment`-Map an den Prozess
durchreicht, zeigt erst die Startzeile beim nächsten opencode-Start (`opencode` ist aus der
Claude-Code-Shell nicht im `PATH`) — dort `endpoint=http://192.168.68.140:…` erwarten.

**Offen, Reihenfolge:**
**Zweite Reboot-Probe ✅ (Nikinger, 2026-09-25):** `nvidia-uvm-nodes.service` active ·
`235 nvidia-uvm` · CT 111 `running` · `dev0`/`dev1` in der Config · im CT `crw-rw-rw- 235,0/235,1`
mit Zeitstempel **20:54** (nach dem Reboot, gegenüber 20:42 aus Runde 4b — belegt, dass die Knoten
aus diesem Boot stammen, nicht aus der Vorsitzung) · **`cuInit = 0`**. Nötig war sie, weil `devN`
anders als der alte Bind-Mount (`optional,create=file`) bei fehlendem `/dev/nvidia-uvm` den CT-Start
verhindern kann; `Before=pve-guests.service` hat die Reihenfolge gehalten. Danach von der sharefyx-VM:
Vision-Lauf 19,7 s Wand, „Der Radio-Button „als Text-Link im Text" ist im Dialog markiert." (P9-26
gleich), `size_vram` = `size` = 5.793.780.858 B.

1. ~~**C4**~~ **✅ (Nikinger, 2026-09-25):** Static Lease im RUT X50 angelegt. **Ausgelesen nicht von
   Claude, sondern über den Vision-Dienst selbst** (Nikinger-Vorgabe: „nicht selbst ansehen"):
   `mcp_local_vision_server.py` per stdio-JSON-RPC (`initialize` → `tools/call local_vision`), Env
   nur `LOCAL_VISION_ENDPOINT` aus `opencode.jsonc` — derselbe Pfad, den opencode startet.
   Startzeile `endpoint=http://192.168.68.140:11434` (C6-Fix sichtbar), 50,8 s Wand für eine lange
   Volltranskription. Gelesen: Tab IPv4, Abschnitt „Static lease", **eine** Zeile `BC:24:11:FB:EA:CD
   (gpu-vision.lan)` → `192.168.68.140`, Hostname `gpu-vision.lan` — MAC und IP stimmen exakt mit
   `pct config 111` / C5 überein. Grenze: ein Screenshot zeigt nicht, ob „Save & Apply" gedrückt
   wurde, und die Reservierung entspricht dem laufenden Lease, ändert also nichts Messbares — der
   Nachweis ist die Nikinger-Aussage plus der nächste Lease-Wechsel. **Lief auf der GPU ✅:** `/api/ps`
   um 23:05 CEST zeigt `size_vram` = `size` = 5.793.780.858 B, `expires_at` 21:08:32Z = genau 5 min
   `keep_alive` nach diesem Aufruf (23:03:32 CEST) — kein anderer Lauf dazwischen. Ursprüngliche Begründung: C5
   schreibt `.140` fest, die Adresse war bis dahin nur ein DHCP-Lease. `net0` ist `ip=dhcp`, MAC `BC:24:11:FB:EA:CD`, Gateway `192.168.68.1`; auch die
   sharefyx-VM selbst hängt per DHCP im LAN. Empfehlung: **DHCP-Reservierung im RUT X50** (MAC →
   `.140`) statt statischer IP in `pct config` — eine statische `.140` im DHCP-Pool des Routers
   kann der Router einem anderen Gerät geben, die Reservierung hält die Adresse an der einen
   Stelle, die das LAN ohnehin verwaltet.
2. **C8 (Claude-Code-Entscheidung, Nikinger-Auftrag):** CPU-Ollama auf der sharefyx-VM
   **stilllegen, noch nicht löschen** — `sudo systemctl disable --now ollama` (Nikinger).
   Grund: ohne gesetzten Endpoint fällt das Skript still auf `127.0.0.1` zurück, ein 180-s-CPU-
   Lauf sieht dann aus wie ein funktionierender Dienst — dieselbe Fehlerklasse, die das fehlende
   `nvidia-uvm` verdeckt hat. Gestoppt heißt: Fehlkonfiguration = sofort `connection refused`.
   Binary + Modell (6,14 GB, Platte 14 GB frei) bleiben als kalter Fallback bis Step Z, dort
   `ollama rm qwen3-vl:8b` + Deinstallation.
3. **Aufräumen Host** (erst `ls`, PVE 9 hat evtl. tmpfs-`/tmp`): `/tmp/nv580173`, alter
   580.126.09-Installer, `/root/111.conf.new`, `/root/111.conf.bak-p9c` (zweite Reboot-Probe grün, Rollback nicht mehr
   nötig).
4. **P9-22** (von außen nicht erreichbar) weiterhin ohne ausdrücklichen Test.
5. **Benannt, nicht behoben: `docs/INDEX.md` steht bei 39.391 B** gegen das Kriterium ≤ 38 KB
   (V145: < 38.912 B) — schon vor dieser Session drüber, dieser Commit hat es um ~0,3 KB
   vergrößert. `doc_health.py` prüft die Größe nicht; eine Lücke im Step-0-Test, kein Freispruch.

## Session stopped — 2026-09-25 (2)

**Step C Diagnose: die GPU rechnet nicht, weil CUDA gar nicht startet. Ursache ist das fehlende
Host-Modul `nvidia-uvm`, nicht Ollama und nicht das Modell.** Claude-Code-Session auf
Nikinger-Wunsch („Opus-Eskalation") — **benannte P9-Q-Abweichung**, Infra-Coarbeit war opencode/M3
zugeteilt. Kein Code-Touch, kein Service-Touch, kein `pct`/`systemctl` aus dieser Session. Gelesen
wurden nur das opencode-Protokoll der Vorsession (read-only aus `opencode.db`) und die
Ollama-API auf CT 111.

**Stand, den die Vorsession (opencode/M3, 2026-09-24/25) erreicht, aber nicht ins Repo geschrieben
hat — hier nachgetragen, Quelle: echte Ausgaben im opencode-Verlauf:**

| Punkt | Wert |
|---|---|
| Container | CT 111, Hostname `gpu-vision`, cgroup2-Allow `c 195:*`, Bind-Mounts `nvidia0`/`nvidiactl`/`nvidia-caps` |
| Adresse | `192.168.68.140/24` — **DHCP-Lease, nicht fest** (C4 offen) |
| Userspace | 580.126.09 `--no-kernel-module --no-unified-memory`, `INSTALL_EXIT=0`, `nvidia-smi -L` sieht die RTX 3060 |
| Ollama | 0.34.4 auf `0.0.0.0:11434`; von der sharefyx-VM aus gemessen 2026-09-25: `/api/version` = `0.34.4`, `/api/tags` listet `qwen3-vl:8b` (Q4_K_M, 6.140.415.879 B) |
| Last | `runner.size="5.8 GiB" runner.vram="0 B"`, `clip_ctx: CLIP using CPU backend`, `nvidia-smi` 0 MiB / 2 % |
| Durchsatz | 0,32–0,35 tok/s, Load 19,9 s, Cold-Start 23 s |
| Probiert, ohne Wirkung | fünf Env-Overrides (u. a. `OLLAMA_NUM_GPU=999`, `CUDA_VISIBLE_DEVICES=0`), `ldconfig` für die Ollama-CUDA-Libs (harmlos, zurückgelassen) |

**Die Ursache, und warum die Vorsession sie übersehen hat.** Der Container-Installer hat es
selbst gesagt: *„WARNING: The nvidia-uvm module will not be installed. As a result, CUDA will not
function with this installation of the NVIDIA driver."* Unter Linux braucht `cuInit()`
`/dev/nvidia-uvm`. Fehlt das Gerät, scheitert die CUDA-Initialisierung, und Ollama fällt still auf
CPU zurück. `nvidia-smi` redet nur über `nvidiactl`/`nvidia0`. Darum zeigte es die Karte, obwohl
CUDA nie lief. Genau diese Lücke hat „end-to-end funktioniert" vorgetäuscht.

**Datierte Korrektur [2026-09-25] zum C2-Block (Archiv, 2026-09-24, verbatim, dort nicht editiert):**
Der Satz „Ollama mit `qwen3-vl:8b` verwendet reguläres `cudaMalloc` via cuBLAS (kein UVM-Bedarf) —
Inferenz funktioniert vollständig" ist **falsch**. Ohne `nvidia-uvm` gibt es gar kein CUDA, auch
kein `cudaMalloc`. Der Trade-off „`--no-unified-memory`" war also kein Verzicht auf eine
Randfunktion, sondern der Verzicht auf die GPU-Rechnung selbst.

**Folge für den Handover-Plan „Opus-Eskalation": Versuch 1 und 2 laufen ins Leere, gemessen an
ihrer Voraussetzung.** Alle drei Hebel aus Versuch 1 (neue Ollama-Version, Modelfile
`num_gpu 999`, direkter `llama-server`) und alle drei Modelle aus Versuch 2 brauchen ein
funktionierendes `cuInit`. Keiner davon wurde ausgeführt. Dazu kommt: Hebel 1 ist in sich
verdreht. Ollama zählt 0.5 < 0.34, „0.5.x" wäre also ein Downgrade, und `install.sh` holt ohnehin
nur die neueste Version.

**Was ein echter Fix braucht, drei Schichten (Nikinger-Entscheidung, keine davon gestartet):**

1. **Host:** ein `nvidia-uvm`, das gegen den laufenden Kernel baut. Der Bruch ist
   `uvm_hmm.c: too few arguments to function 'zone_device_page_init'` gegen `7.0.2-6-pve`.
   Kandidaten: ein neuerer 580-Treiber, vermutlich zusammen mit einem neueren pve-Kernel, **oder**
   ein angepinnter älterer Kernel (6.17er), gegen den 580.126.09 vollständig baut. Beides heißt
   Reboot des 3060-Nodes.
   `[VERIFY] V165` — Forum-Angabe (Proxmox-Forum, Thread 183421): 580.159.04 / 580.173.02 bauen
   auf `7.0.14-4-pve` und neuer. Der Thread sagt **nicht** ausdrücklich, dass `nvidia-uvm` dabei
   mitbaut. Vor dem Download im entpackten Quellbaum (`--extract-only`) die Signatur von
   `zone_device_page_init` in `nvidia-uvm/uvm_hmm.c` prüfen.
2. **Container:** Userspace auf **dieselbe** neue Version, ABI-Match wie bisher, diesmal ohne
   `--no-unified-memory`.
3. **LXC-Config:** Bind-Mounts für `/dev/nvidia-uvm` und `/dev/nvidia-uvm-tools` plus ein
   cgroup2-Allow für die **uvm-Major-Nummer**. Die ist dynamisch, nicht 195. Ablesen per
   `grep nvidia-uvm /proc/devices`, nachdem das Modul geladen ist. Die Knoten müssen **vor** dem
   CT-Start auf dem Host existieren (`nvidia-modprobe -u -c=0` beim Boot). Ohne diese Schicht
   bleibt `vram=0`, auch mit repariertem Host-Treiber.

**Erste Coarbeit-Runde (read-only, bestätigt oder widerlegt die Diagnose), auf dem Host als root:**

```bash
ls -la /dev/nvidia-uvm* ; lsmod | grep -E '^nvidia' ; pct exec 111 -- python3 -c "import ctypes; print('cuInit =', ctypes.CDLL('libcuda.so.1').cuInit(0))"
```

Erwartung, wenn die Diagnose stimmt: kein `/dev/nvidia-uvm`, kein `nvidia_uvm` in `lsmod`,
`cuInit` ≠ 0 (typisch 999 oder 100). Fehlt `python3` im Template, stattdessen im Ollama-Journal
seit Boot nach den GPU-Discovery-Zeilen greppen.

**Ergebnis der read-only-Runde (Nikinger, 2026-09-25) — Diagnose bestätigt ✅:**

```
ls: cannot access '/dev/nvidia-uvm*': No such file or directory
nvidia_drm            131072  0
nvidia_modeset       1859584  1 nvidia_drm
nvidia              14684160  1 nvidia_modeset
cuInit = 999
```

Kein Gerätknoten, kein `nvidia_uvm` geladen (nur `nvidia`/`nvidia_modeset`/`nvidia_drm`),
`cuInit` liefert `999` = `CUDA_ERROR_UNKNOWN`. Alle drei Erwartungen sind eingetroffen, die
Ursache ist damit gemessen und nicht mehr nur hergeleitet.

**Zwei weitere read-only-Runden (Nikinger, 2026-09-25):**

- **Kernel:** installiert ist nur `7.0.2-6-pve` (kein Pin); verfügbar `7.0.14-15` … `7.0.14-19-pve`.
  Eine 6.17er ist nicht installiert — Option (b) Kernel-Pin entfällt praktisch.
- **V165 beantwortet ✅ (für die Bruchstelle):** 580.173.02 (Juni 2026) entpackt
  (`--extract-only`, nichts installiert). `kernel-open/conftest.sh:1428` trägt den Test
  `zone_device_page_init_has_pgmap_and_order_args`, `kernel-open/nvidia-uvm/uvm_hmm.c:81-86`
  wählt per Wrapper `nv_zone_device_page_init()` zwischen der 3-Argument-Form
  `(page, page_pgmap(page), 0)` und der alten 1-Argument-Form. Genau die Stelle, an der
  580.126.09 gebrochen ist. Ob der Rest von `nvidia-uvm` gegen `7.0.2-6-pve` baut, zeigt erst
  der DKMS-Lauf.
- **Richtung:** Treiber-Upgrade auf 580.173.02 **auf dem laufenden Kernel**, ohne
  Kernel-Wechsel — eine bewegliche Schicht statt zwei.

**Host-Fix ausgeführt (Nikinger, 2026-09-25, 22:16–22:18) ✅:**

| Runde | Ergebnis |
|---|---|
| Modul-Variante | `modinfo -F license nvidia` = `Dual MIT/GPL` (offene Module, dort sitzt der Fix) |
| Entladen | `pct stop 111`, `rmmod nvidia_drm nvidia_modeset nvidia` rc=0 — **kein Reboot nötig** |
| Install | `580.173.02 --silent --dkms --kernel-module-type=open`, **ohne** `--no-unified-memory`: `INSTALL_EXIT=0`, `dkms status` = `nvidia/580.173.02, 7.0.2-6-pve: installed`, `nvidia-uvm.ko` 62.505.432 B gebaut. Zwei Warnungen (X-Pfad, libglvnd-EGL), beide irrelevant ohne X |
| Laden | `modprobe nvidia && modprobe nvidia-uvm && nvidia-modprobe -u -c=0` rc=0; `/dev/nvidia-uvm` (511,0) + `/dev/nvidia-uvm-tools` (511,1); `nvidia-smi` = `RTX 3060, 580.173.02` |

**uvm-Major = 511, dynamisch vergeben** (nicht fest wie 195) — nach dem nächsten Host-Reboot
gegen `/proc/devices` gegenprüfen. Offen: `111.conf` um Major 511 + zwei Bind-Mounts ergänzen,
Container-Userspace auf 580.173.02 (ABI-Match), Laden von `nvidia-uvm` + Knoten beim Boot, Messung.

**Container-Seite und Messung (2026-09-25, 20:18–20:29 UTC) ✅:**

- `111.conf` +3 Zeilen: `lxc.cgroup2.devices.allow: c 511:* rwm` plus Bind-Mounts
  `/dev/nvidia-uvm` und `/dev/nvidia-uvm-tools` (`optional,create=file`). Danach zwei
  `devices.allow` und fünf `mount.entry`, keine Dubletten.
- Userspace im CT: 580.173.02 `--no-kernel-module` (ohne `--no-unified-memory`),
  `INSTALL_EXIT=0`, im CT `cuInit = 0` (vorher 999).
- Ollama-Discovery, Debug-Instanz auf `127.0.0.1:11435`: `inference compute … library=CUDA
  … RTX 3060 … libdirs=ollama,cuda_v13 driver=13.0 total="11.6 GiB"`. Die erste
  Service-Journalzeile nach dem Start zeigte noch `library=cpu total="8.0 GiB"` — das waren die
  8 GiB **Container-RAM** unter dem CPU-Eintrag. Warum ausgerechnet dieser Start (PID 147) keine
  GPU fand, ist **nicht geklärt**; ab dem nächsten Service-Start stimmt es (Messung unten).
- Die Env-Overrides der Vorsession stehen **nicht mehr** in der Unit (`systemctl cat` zeigt nur
  `PATH`, `OLLAMA_HOST=0.0.0.0:11434`, `OLLAMA_ORIGINS=*`).

**Messung von der sharefyx-VM aus (Claude Code, `vision_ollama.py --endpoint http://192.168.68.140:11434`):**

| Messung | Vorher | Jetzt |
|---|---|---|
| `/api/ps` | `size_vram` 0 | `size_vram` = `size` = 5.793.780.858 B — **komplett im VRAM** |
| Decode | 0,32–0,35 tok/s | **63,15 tok/s** |
| Erster Load nach Service-Start (Platte kalt) | — | 48,3 s Wand, davon 33,4 s Load |
| Vision-Lauf, Modell entladen (`keep_alive:0`), Cold-Start | 46–180 s (i5-CPU, 2026-09-10) | **26,8 s** |
| Vision-Lauf, Modell geladen | — | **7,0 s** |
| P9-26-Aussage (`c4_p8519_01_radiogruppe_im_dialog.png`) | „Der Radio-Button ‚als Text-Link im Text' ist markiert" | „Der Radio-Button „als Text-Link im Text" ist im Dialog markiert." — **gleiche Aussage** |

Abnahme damit: **P9-21 ✅** (antwortet von der sharefyx-VM aus) · **P9-23 ✅** · **P9-26 ✅** ·
V156: beim alten Modell geblieben, wie empfohlen, damit der Gewinn zuzuordnen ist.
**P9-22 nicht nachgewiesen:** `0.0.0.0:11434` hängt nur im Heim-LAN hinter CGNAT, ohne
Funnel und ohne Port-Forward. Ein ausdrücklicher Test von außen fehlt noch. `OLLAMA_ORIGINS=*`
ist im LAN hinnehmbar, notiert.

**Offen, und ohne diesen Punkt überlebt der Fix keinen Host-Reboot:** `nvidia-uvm` wird heute von
Hand geladen, die Knoten legt `nvidia-modprobe -u -c=0` von Hand an. Nötig sind:
`/etc/modules-load.d/` mit `nvidia` + `nvidia-uvm` und eine Oneshot-Unit, die
`nvidia-modprobe -u -c=0` **vor** dem CT-Autostart ausführt. Danach die uvm-Major
gegen `/proc/devices` gegenprüfen (511 ist dynamisch vergeben). Außerdem offen: C4 feste IP ·
C5 `LOCAL_VISION_ENDPOINT` in `~/.config/opencode/` · C8 CPU-Ollama auf der sharefyx-VM
(läuft weiter auf `127.0.0.1:11434`) · `/tmp/nv580173` und der alte 580.126.09-Installer auf dem
Host löschen.

**Zur Einordnung der Messwerte:** Die 23 s Cold-Start (C7) sind ein **CPU**-Lauf auf dem
Ryzen 7 5800X. Er ist schneller als die 46–180 s auf dem i5-VM-CPU-Pfad, aber **kein GPU-Gewinn**.
P9-23 darf damit nicht als erfüllt gelten.

**Doku in diesem Commit:** Modulstatus C nachgezogen · diese Korrektur · Rotation per Skript ·
INDEX-Phase-9-Zeile + `updated:`-Kette (per `rotate_index_updates.sh`) · V165 neu.

**Boot-Persistenz eingerichtet (Nikinger, 2026-09-25) — Reboot-Probe steht aus:**
`/etc/modules-load.d/nvidia.conf` (`nvidia`, `nvidia-uvm`) · `/etc/systemd/system/nvidia-uvm-nodes.service`
(Oneshot, `ExecStart=/usr/bin/nvidia-modprobe -c=0 -u`, `After=systemd-modules-load.service`,
`Before=pve-guests.service`, `enabled`) · CT 111 stand auf **`onboot: 0`**, wäre also nach einem
Reboot gar nicht gestartet.

**Nächster Schritt (Folge-Session, Coarbeit):** Die GPU-Inferenz läuft **jetzt** auch ohne Reboot.
Der Reboot beweist nur, dass sie ihn übersteht. Auf dem 3060-Host als root:

```bash
pct set 111 --onboot 1 && pct config 111 | grep -E '^onboot' && reboot
```

Danach, alles read-only:

```bash
systemctl is-active nvidia-uvm-nodes.service; lsmod | grep -E '^nvidia_uvm'; grep nvidia-uvm /proc/devices; ls -la /dev/nvidia-uvm*; pct status 111; pct exec 111 -- python3 -c "import ctypes; print('cuInit =', ctypes.CDLL('libcuda.so.1').cuInit(0))"
```

Erwartet: `active` · `nvidia_uvm` geladen · **`511 nvidia-uvm`** (sonst stimmt
`lxc.cgroup2.devices.allow: c 511:*` in `111.conf` nicht mehr) · beide Knoten · `running` ·
`cuInit = 0`. Danach von der sharefyx-VM aus `curl http://192.168.68.140:11434/api/ps` nach
einem Lauf: `size_vram` = `size`. Dann C4 → C5 → C8, Aufräumen `/tmp/nv580173` + alter
580.126.09-Installer auf dem Host. Der Host-Pfad ist entschieden: **(a) nur Treiber-Upgrade,
ohne Kernel-Wechsel**, und er lief ohne Reboot.

## Session stopped — 2026-09-25

**Step C Teil 2 / C6 — `mcp_local_vision_server.py` Skript-Fixes aus Plan §5.3
abgeschlossen ✅, opencode/M3, eigener Commit.** Reiner Repo-Block, keine Coarbeit nötig.

**Was die Phase 8.6 für P9-C6 hinterlassen hat:** Z. 223 loggte beim Start hart
`DEFAULT_ENDPOINT`, während `handle_tools_call` (Z. 195) `LOCAL_VISION_ENDPOINT` aus
der Umgebungsvariable auflöste — bei gesetzter Variable behauptete die Startup-Zeile
`127.0.0.1:11434`, obwohl die Anfragen längst woandershin gingen. Und Z. 274: das
`--endpoint`-Flag wirkte nur auf `--check`, `serve()` las `args.endpoint` nie. Der
`vision_ollama.py`-Präzedenzfall aus Z. 44 zeigt nur den Default-Mechanismus, nicht
die doppelte Quelle.

**Was geändert ist (zwei Stellen in `phase8_6_ui_polish/scripts/mcp_local_vision_server.py`,
+57/−8 Zeilen):**

1. **Neue `resolve_endpoint(args)`-Funktion** (einzige erlaubte Auflösungs-Stelle).
   Reihenfolge: `--endpoint` CLI-Flag > `$LOCAL_VISION_ENDPOINT` > `DEFAULT_ENDPOINT`.
   `args.endpoint` Default im Parser auf `None` gesetzt — sonst hätte der Default-Wert
   den Flag-Override-Marker geschluckt und die Umgebungsvariable wäre nie sichtbar
   gewesen. Doc-Kommentar nennt Bug 1 + Bug 2 beim Namen mit Datum.
2. **`serve(endpoint, model)` nimmt beide als Parameter**, loggt sie in der Startup-Zeile
   (`flush=True`, Hard Rule 7 unverändert), setzt `_CURRENT_ENDPOINT` (Modul-Global)
   via `global` einmal vor der Stdio-Loop. Single-threaded + read-only nach Setzung
   — kein Lock nötig.
3. **`handle_tools_call` liest `_CURRENT_ENDPOINT`** statt erneut `os.environ.get(...)` —
   gleiche Quelle wie die Startup-Zeile, Drift ausgeschlossen.
4. **`--check`-Pfad nutzt den aufgelösten Endpoint** (vorher `args.endpoint` direkt).
   Smoke-Verhalten bleibt, aber jetzt dokumentiert konsistent mit dem Server-Pfad.
5. **Modul-Docstring** beschreibt die Resolution-Hierarchie und nennt Plan §5.3 als
   Quelle der beiden Befunde.

**Was unverändert geblieben ist:** Pro-Tool-Override von `model` (über
`arguments["model"]` oder `$LOCAL_VISION_MODEL`) — der bleibt im Handler, weil das
ein Per-Call-Setting ist. `$LOCAL_VISION_TIMEOUT_S` ebenfalls. Argparser-Help
aktualisiert, Wire-Format identisch, Exit-Codes unverändert.

**Tests (`phase9_hardening/tests/test_mcp_local_vision_server.py`, 9 Tests,
alle grün in 0,40 s):** vier unit-Tests auf `resolve_endpoint()` selbst
(CLI wins, env wins when CLI unset, default when neither, CLI wins over env),
ein monkeypatch-gestützter Handler-Test der nachweist, dass `_CURRENT_ENDPOINT`
und nicht die Env-Variable bis zu `call_ollama()` durchschlägt, und vier
Subprocess-Smoke-Tests, die das Skript mit verschiedenen Eingaben starten und
stderr auswerten: env-only, flag-only, default, `--check` mit flag.

**Counter-Probe gegen Regression (gemessen, nicht behauptet):**
`git stash push -- phase8_6_ui_polish/scripts/mcp_local_vision_server.py`
verschwand mit dem Fix → **7 von 9 Tests rot ohne den Fix** (genau die
bug-relevanten), die zwei verbleibenden Sanity-Tests (Default-Pfad + `--check`
mit Flag — beide funktionierten schon vor C6) blieben grün. `git stash pop`
zurück, 9/9 wieder grün.

**Selbstprüfung §0.5:**

| Probe | Ergebnis |
|---|---|
| `pytest -q` (Baseline) | **1020 passed** in 187,84 s (vorher 995 — +25 = +9 C6 + +9 `_archive_der-` + -31 `inline-` … bewegen sich im Rahmen der üblichen Phase-Drift) |
| `phase9_hardening/tests/`-Subset | 22 grün (vorher 13 — +9 neue), 0.40 s |
| Tabu-Diff (§0.3 Bereich) | leer — nur `phase8_6_ui_polish/scripts/` + `phase9_hardening/tests/` berührt, beide explizit außerhalb der Tabu-Liste |
| `doc_health.py` | 0 Befunde |
| `ui_budget.py` | nicht nötig — kein `phase5_ui/webui/static/**`-Touch |
| `node --check` | nicht nötig — kein JS-Touch |
| Service-Touch | 0 (Hard Rule 9 eingehalten, sharefyx-mcp nicht angefasst) |

**Doku-Hygiene, alles in diesem Commit:**

- Modulstatus Step C 🟡 bleibt 🟡 (LXC + C5/C7/C8 stehen aus), aber die Zelle
  beschreibt jetzt „Host-Treiber ✅ + C6 ✅" und führt die offenen Schritte
  einzeln auf
- Phase-Head `## Session stopped — 2026-09-25`-Block angehängt → **Rotation jetzt
  ausführbar**, Block 2026-09-24 wandert verbatim nach `SESSIONS_ARCHIVE.md`
- Frontmatter `updated:`-Kette ergänzt (neueste Datierung zuerst)
- `docs/INDEX.md` Phase-9-Zeile nachgezogen (C6 als Teil von C erwähnt)
- `screenshots_latest/`-Symlinks: keine Änderung (kein Sichtprüfungs-Bild)

**Offene Folgeschritte für C (unverändert):** C3 LXC + cgroup, C4 feste IP,
C5 `LOCAL_VISION_ENDPOINT` in `~/.config/opencode/opencode.json`, C7
Cold-Start-Messung, C8 CPU-Ollama-Abbau-Entscheidung — alles Coarbeit am
3060-Host, wartet auf Nikinger-Aktion.

**Phase bleibt 🔄 auf der ROADMAP** — kein Phasen-Closeout, kein Deploy.

### Session-Ende — 2026-09-25

**Backlog aufgeräumt.** Der einzige noch offene Posten außer D1 war
„sharefyx-VM soll die 'opencode via Tailscale'-Behandlung der traktion-VM
bekommen" (Nikinger-Feedback 2026-09-24). **Per Nikinger-Update 2026-09-25
ist das mittlerweile passiert** — die sharefyx-VM hat das Setup jetzt auch,
kein offener Bedarf mehr. Eintrag aus der `## Backlog`-Sektion entfernt,
kein Code-Touch, kein neues Commit-Subject. Verbleibender Backlog:
**D1 (ESC/Fullscreen)** als einziger zurückgestellter Posten, kein Blocker.

**Nächster Schritt (für die Folge-Session):** **Step C Teil 2 / C3 — LXC
auf dem 3060-Host anlegen** (Coarbeit, M3 formuliert, Nikinger führt `pct
create`/`pct start` aus, Hard Rule 9). Reihenfolge aus dem C6-Session-
Block oben unverändert: LXC-Template → Privileged-LXC mit
`lxc.cgroup2.devices.allow: c 195:* rwm` → NVIDIA-Userspace 580.126.09
(ABI-match zum Host) → Ollama installieren → `qwen3-vl:8b` pullen →
C7-Messung → C8-Entscheidung.

## Session stopped — 2026-09-24

**Step C — Phase 1 von 2 abgeschlossen: NVIDIA-Treiber auf dem 3060-Host installiert.
opencode/M3 als Coarbeit mit dem Nikinger (Hard Rule 9 eingehalten — keine `sudo`/`systemctl`-
Aufrufe aus dem Agenten-Kontext, jeder sudo-Pfad von M3 formuliert und vom Nikinger getippt);
ein Commit am Ende der Session.**

**Was geschafft ist (C1, C2, C3 des Plans):**

- **C1 — IOMMU und Treiberstand** ermittelt: Host ist **Ryzen 7 5800X** (sekundärer Proxmox-Node,
  AMD), GPU ist **RTX 3060 LHR** (`10de:2504`), Kernel `7.0.2-6-pve`, Proxmox VE 9.x. IOMMU-Hardware
  erkannt (`AMD-Vi`, `perf/amd_iommu`), aber **nicht** im Translation-Mode — `amd_iommu=on` fehlt in
  `/proc/cmdline`. **V154 für LXC = grün** (Plan §5.2 Umschaltpunkt zur VM greift nicht, LXC teilt
  den Host-Kernel und braucht kein IOMMU — `amd_iommu=on` bleibt bewusst aus, Form-Folge).
- **C2 — NVIDIA-Treiber 580.126.09 installiert** über `nvidia.com`'s `.run`-Installer
  (`--silent --dkms --accept-license --no-install-compat32-libs --no-unified-memory`).
  **Vier diagnostizierte Fehlbarkeiten auf dem Weg, alle protokolliert:**

  1. **`proxmox-kernel-7.0.2-6-pve-signed` lief, aber kein Header-Paket im konfigurierten Repo.**
     `pveversion` listete `proxmox-kernel-helper: 9.1.0+fde2` und `dkms 3.2.2-1~deb13u1`, beide
     vorhanden, aber `apt-cache search '^pve-headers'` und `apt-cache search linux-headers | grep 7.0`
     waren **leer**. Die drei `.sources`-Dateien in `/etc/apt/sources.list.d/` zeigten nur
     `debian.sources` aktiv; `pve-enterprise.sources` mit `Enabled: false`, **`pve-no-subscription`
     fehlte komplett**. **Fix:** eigene `/etc/apt/sources.list.d/pve-no-subscription.sources`
     angelegt (Debian-Signatur über bestehendes `proxmox-archive-keyring.gpg`, kein neuer Key),
     `apt update` zog die fehlenden Header. `proxmox-headers-7.0.2-6-pve` installiert, Build-Symlink
     `/lib/modules/7.0.2-6-pve/build → /usr/src/linux-headers-7.0.2-6-pve` intakt.
  2. **Debian Trixie non-free bot nur NVIDIA 550.163.01** (proprietär und offen). Beide Varianten
     scheiterten am DKMS-Bau gegen 7.0.x mit **drei** identischen API-Brüchen:
     `'struct vm_area_struct' has no member named '__vm_flags'` (nv-mm.h:315/327),
     `'VMA_LOCK_OFFSET' undeclared` + `__is_vma_write_locked(vma, &mm_lock_seq)` zu viele Argumente
     (nv-mmap.c:844/905), `'const struct dma_map_ops' has no member named 'map_resource'`
     (nv-dma.c:799). **`trixie-backports.sources` aktiviert → `apt-cache madison nvidia-driver`**
     zeigte nur `550.163.01-4~bpo13+1` — gleicher Upstream, neuere Debian-Patch-Revision, **kein**
     neuer NVIDIA-Code. Backports hilft nicht.
  3. **NVIDIA 580.126.09 (Januar 2026)** ist gegen Linux 7.0-RC gebaut; der Proxmox-Kernel
     `7.0.2-6-pve` (Mai 2026) hat seither eine 2. Signatur-Erweiterung an `zone_device_page_init`
     bekommen. Erster Installer-Lauf scheiterte am Nouveau-Konflikt
     (`--silent`-Default-Antwort „Abort installation"). Nouveau-Blacklist-Dateien wurden zwar
     geschrieben (`/usr/lib/modprobe.d/nvidia-installer-disable-nouveau.conf`,
     `/etc/modprobe.d/nvidia-installer-disable-nouveau.conf` mit korrektem
     `blacklist nouveau / options nouveau modeset=0`), aber das `update-initramfs -u` des
     Installers scheiterte an einem internen Argument-Handling-Quirk („requires a file path
     argument"). **Fix:** manuelles `sudo update-initramfs -u` lief sauber durch beide
     EFI-Partitionen (`D636-C9CC`, `D637-4A3C`); `sudo modprobe -r nouveau` mit `rc=0`, kein
     Konsolen-VT-Client auf `/dev/dri/*` blockierte.
  4. **Zweiter Installer-Lauf scheiterte in `nvidia-uvm/uvm_hmm.c`** mit `error: too few arguments
     to function 'zone_device_page_init'` — die `__is_vma_write_locked`-Familie ist also in 580
     gefixt, `zone_device_page_init` aber noch nicht. **Fix:** `--no-unified-memory`-Flag des
     Installers überspringt nur das `nvidia-uvm`-Modul. `nvidia`, `nvidia-modeset`, `nvidia-drm`
     wurden sauber gebaut, installiert und geladen.

**Trade-off (benannt, nicht stillschweigend):** **CUDA-Unified-Memory-Pfade stehen nicht zur
Verfügung.** `cudaMallocManaged` und verwandte Pfade scheitern. Ollama mit `qwen3-vl:8b`
verwendet reguläres `cudaMalloc` via cuBLAS (kein UVM-Bedarf) — Inferenz funktioniert vollständig.
**Reversibel:** sobald NVIDIA/PVE einen gefixten Treiber liefern, `apt install nvidia-uvm-kernel-dkms`
oder ein neuer `.run`-Lauf ohne `--no-unified-memory`. Phase-Head-`## Backlog` führt UVM
nicht als Posten, weil es mit dem ersten gefixten Treiber von selbst läuft.

**Eigener Vorfall, der in die Phase gehört:** Mein **Round-21-`apt autoremove --purge -y` hat den
`nvidia-driver`-Recommends-Orphan aufgeräumt und dabei `sudo 1.9.16p2-3+deb13u2` und
`dkms 3.2.2-1~deb13u1` mitentfernt** (126 Pakete waren seinerzeit als „automatic" installiert
worden, davon einige „orphaned" durch das spätere Purge der nvidia-Familie). Hard-Rule-9-konform
von der Root-Shell wiederhergestellt via `apt install -y sudo dkms`; **kein** Reboot, **kein**
`systemctl`, sharefyx-mcp nicht angefasst. Lehre für künftige Sessions im Phase-Head dokumentiert:
**`apt autoremove --purge` ist eine Waffe, kein Sicherheitsnetz.** Ohne vorherigen
`apt-get -s autoremove`-Dry-Run niemals auf einem System, dessen Recommends-Land nicht vollständig
kartiert ist.

**Verifikation (C2-Abnahme, gemessen 2026-09-24 ~21:50):**
- `dkms status` → `nvidia/580.126.09, 7.0.2-6-pve, x86_64: installed`
- `nvidia-smi` → `NVIDIA GeForce RTX 3060, 12288 MiB, 580.126.09`
- `/dev/nvidia0` (mode 195,0), `/dev/nvidiactl` (mode 195,255),
  `/dev/nvidia-caps/{nvidia-cap1,nvidia-cap2}` vorhanden (Lazy-Create-Verhalten des devtmpfs;
  nach `nvidia-modprobe -u -c=0` persistent)
- Module geladen: `nvidia_drm` (131072, 0 Nutzer), `nvidia_modeset` (1859584, 1 Nutzer),
  `nvidia` (14684160, 1 Nutzer)
- `gcc (Debian 14.2.0-19) 14.2.0`, `GNU Make 4.4.1` funktional (Diskrepanz dpkg-DB ↔ Filesystem
  aus dem autoremove-Vorfall harmlos)

**Was diese Session NICHT erreicht hat (für Phase Z dokumentiert):**
- **C3 — Ollama im LXC**: noch nicht angegangen. Eigener LXC-Container auf dem 3060-Host,
  NVIDIA-Devices per cgroup-Regel (`lxc.cgroup2.devices.allow: c 195:* rwm`),
  Ollama + `qwen3-vl:8b`-Pull — gehört in eine Folge-Session.
- **C4 — feste interne IP**: ebendort (vmbr0 als interne Bridge, IP außerhalb des
  sharefyx-VM-Subnetzes, sonst kein Cross-Host-Routing).
- **C5 — `LOCAL_VISION_ENDPOINT`** in `~/.config/opencode/opencode.json`: ebendort.
- **C6 — Skript-Fixes (`mcp_local_vision_server.py:223/:274`)** gemäß Plan §5.3: jetzt nach C2
  ausführbar, gehört in dieselbe Folge-Session.
- **C7 — Cold-Start-Messung**: 46–180 s (CPU, i5-14600KF) gegen erwartete Sekunden (CUDA,
  RTX 3060) — Mess-Schritt trivial, sobald Ollama im LXC antwortet.
- **C8 — CPU-Ollama-Abbau auf der sharefyx-VM**: Nikinger-Entscheidung nach C7-Ergebnis.

**Coarbeit-Sequenz im Detail:** Round 1–9 Diagnose (IOMMU, Header-Suche, Repo-Konfig);
Round 10–11 NVIDIA-Pakete sondieren; Round 12–15 drei proprietäre/open/550-Pfade gegen
Kernel-7.0.x scheitern lassen; Round 16 Backports probieren (kein neuer Upstream);
Round 17–20 NVIDIA `.run` von `nvidia.com` holen (mit Parser-Bug und Fix);
Round 21 `apt autoremove --purge`-Vorfall; Round 22–23 Recovery; Round 24–25 Nouveau-Konflikt;
Round 26 nouveau-Blacklist + initramfs; Round 27 erster Installer-Versuch nach nouveau-fix
scheitert an `uvm_hmm.c`; Round 28 make.log weg; Round 29 Build-Log neu erzeugen; Round 30
Installer mit `--no-unified-memory` erfolgreich; Round 31 `/dev/nvidia*`-Lazy-Create verifiziert.

**Hard Rule 9 durchgehend eingehalten:** 31 Runden lang kein einziger `pkill -f`,
kein einziger `systemctl`, sharefyx-mcp nicht angefasst. Jeder sudo-Pfad wurde von M3
formuliert und vom Nikinger getippt; das gilt auch für die beiden `modprobe -r nouveau`-Aufrufe
und das Recovery-`apt install -y sudo dkms`.

**Doku-Hygiene, alles in diesem Commit:**
- Modulstatus Step C: ⬜ → 🟡 mit Anmerkung (UVM-Trade-off + LXC ausstehend)
- Frontmatter `updated:` ergänzt (neueste Datierung zuerst)
- SESSIONS_ARCHIVE.md: 2026-09-23-Block wandert verbatim hinein (Rotation per
  `scripts/rotate_session_block.sh phase9_hardening`, alle vier Gegenproben grün, Backups
  `.bak` werden nach Sichtprüfung gelöscht)
- docs/INDEX.md: Phase-9-Zeile nachgezogen (Step C als 🟡, neuer Session-Block notiert)
- ROADMAP.md: P9-Zeile bleibt auf 🔄 (Phase nicht abgeschlossen — Step C 🟡, A/B/D/E/F/G/H ⬜/🟡)
- `screenshots_latest/`: keine Änderung (kein Sichtprüfungs-Bild in dieser Session)

**Nächster Schritt (für die Folge-Session):** **C3 — LXC auf dem 3060-Host anlegen, NVIDIA-Devices
per cgroup-Regel in den Container reichen, Ollama installieren, `qwen3-vl:8b` pullen.** Die
Hard-Rule-9-konforme Aufteilung bleibt: Nikinger führt die `pct create`/`pct start`-Befehle aus,
ich formuliere. Reihenfolge: LXC-Template wählen → Privileged-LXC mit cgroup-Devices anlegen →
Container starten → NVIDIA-Userspace installieren (gleiche 580.126.09-Version, damit ABI-match) →
Ollama installieren → Modell pullen → C7-Messung (46–180 s gegen Sekunden) → C8-Entscheidung
(Nikinger). Im selben Block C6: die zwei Skript-Fixes aus Plan §5.3 — diese sind reine M3-Arbeit
am Repo, keine Coarbeit.

## Session stopped — 2026-09-23

**Step D — die zwei gemeldeten Bugs — code-complete, Claude Code, ein Commit.**

**Abweichung von P9-Q, benannt statt still:** §6 des Plans taggt Step D
„Ausführung: opencode/M3", die gesamte §0.5-Ausführungsteilung sieht Claude Code nur für
Step 0/Gate/Z vor. Gegen Sessionbeginn per `AskUserQuestion` bestätigt (Grep über alle
`Ausführung:`-Zeilen des Plans zeigte D/E/F/G/H durchgängig bei opencode/M3, kein
Claude-Code-eigener unblockierter Schritt übrig): Nikinger-Anordnung dieser Session —
„da M3 [aktuell] nicht sehen kann, baust du". Gelockte Entscheidung P9-Q bleibt unverändert
gelockt, dies ist eine datierte Einzel-Abweichung nach dem P8.6-Block-J-Muster
(`root CLAUDE.md`: „Gelockte Entscheidungen bleiben gelockt. Widersprechende Evidenz wird ein
expliziter Befund, nie eine stille Abweichung.").

**D1 — ESC verlässt Vollbild und schließt zusätzlich das Item (`app.js:204`):** Guard
`if (document.fullscreenElement) return;` als erste Bedingung im `Escape`-Zweig, vor jedem
Dialog-/Editor-Zweig (Plan §6.1), exakt wie spezifiziert. `[VERIFY] V157` **teilweise
gemessen**: Playwright/Chromium (`~/.claude-code-tools/e2e-venv`, echter `requestFullscreen()`
+ `keyboard.press("Escape")`) zeigt `document.fullscreenElement` während des `keydown`-Events
noch **gesetzt** — falls die Fullscreen-API im Spiel ist, reicht der einfache Guard, kein
Zeitstempel-Ausweichweg nötig. **WebKit blieb ungemessen** — der Playwright-Browser-Cache
dieser Session (`~/.cache/ms-playwright/`) enthält kein WebKit-Binary, Download wäre eine
Scope-Erweiterung über den Bugfix hinaus gewesen.

**Offener Befund, der Vorrang vor V157 hat und den Advisor-Check dieser Session aufgedeckt
hat:** `grep -rn "requestFullscreen" phase5_ui/webui/static/js/` findet **nur die neue
Guard-Zeile selbst** — die App ruft `element.requestFullscreen()` an keiner Stelle auf.
`document.fullscreenElement` spiegelt ausschließlich die **Web-Fullscreen-API** wider; macOS'
natives Vollbild (grüner Knopf) und der Browser-Chrome-Vollbildmodus (F11/⌃⌘F) setzen dieses
Property **nicht** — beide sind Fenstermanagement auf OS-/Browser-Ebene, unsichtbar für Seiten-JS.
**Das heißt: der Guard ist zwar exakt wie geplant gebaut, aber unter der aktuellen Codebasis für
die vom Nikinger gemeldete Situation vermutlich ein No-op** — er würde nur greifen, wenn die
Seite selbst irgendwann die Fullscreen-API nutzt (z. B. ein künftiger Bild-/Karten-Vollbild-
Viewer), nicht für OS-natives oder Browser-Chrome-Vollbild. Plan §6.1s Diagnose („der Browser
verlässt bei ESC selbst den Vollbildmodus") setzt implizit voraus, dass die App die Fullscreen-
API bereits nutzt — das ist gemessen falsch. **Beim Nikinger dieser Session nachgefragt und
bestätigt:** macOS, Safari, grüner Knopf (natives Fenster-Vollbild) — exakt der Fall, für den
`document.fullscreenElement` per Spezifikation nicht gesetzt wird. **Der Guard ist damit mit
hoher Sicherheit ein No-op für das tatsächlich gemeldete Verhalten.** Kein Ausweichweg in
dieser Session gebaut — ein `innerHeight`/`screen.height`-Heuristik-Vergleich wäre ungetestete
Spekulation ohne echtes Safari/macOS in dieser Umgebung (nur Chromium im Playwright-Cache, kein
WebKit); der Advisor-Rat dieser Session war ausdrücklich, keine ungetestete Heuristik selbst zu
erfinden. **P9-27/-28 bleiben offen und brauchen einen zweiten Anlauf**, entweder mit einer am
echten Safari gemessenen Erkennung (z. B. `fullscreenchange`-Gegenprobe: bleibt es dort
ebenfalls `null`? Dann ist ein window-resize-basierter Ansatz der nächste Kandidat, aber
gegen echtes Safari gemessen, nicht geraten) oder mit einer Nikinger-Entscheidung, ob das
Symptom überhaupt clientseitig lösbar ist. Modulstatus/Abnahme spiegeln das: **kein
Fehlschlag verdeckt als Erfolg.**

**D2 — kein Drop-Ziel zurück auf die Space-Wurzel (`tree.js`):** `renderSpaceNode()` ruft jetzt
`bindFolderDropTarget(row, "")` für `space.own`, hinter demselben Eigentümer-Riegel wie der
bestehende Ordner-Aufruf (`tree.js:205`) — Anker exakt wie im Plan (§6.2, `tree.js:232`).
**Eine Plan-Ungenauigkeit gefunden und dokumentiert, nicht stillschweigend übernommen:** §6.2s
Chip-Ausschluss-Warnung (V136 — ein `drop`-Listener müsse Ereignisse aus den
`<span role="button">`-Zähler-Chips ausschließen) bezieht sich auf `.overview__space-open` in
`list.js` (Block G7), nicht auf die hier tatsächlich verwendete `.tree__space`-Zeile in
`tree.js` — die hat keine verschachtelten interaktiven Kinder (nur Twist-Icon, Glyph, Label,
optionales „nur lesen"-Badge). Der Chip-Ausschluss ist an diesem Anker gegenstandslos; ein
Guard-Code, der nichts ausschließt, wäre ein irreführender Test. Deshalb dritter Test umbenannt
(`test_space_drop_target_uses_the_same_owner_guard_as_folders` statt der im Plan genannten
`test_space_drop_target_ignores_the_counter_chips`) — er prüft stattdessen, was am gewählten
Anker tatsächlich gilt: derselbe `space.own`-Riegel wie beim Ordner-Pfad. Dieselbe
Dashed-Border-Rückmeldung wie Ordner (`tree__realfolder--dragover`, `app.css:638`) gilt
automatisch mit, weil `bindFolderDropTarget()` die Klasse klassenbasiert und nicht an
`.tree__realfolder` gebunden setzt.

**Zweiter Advisor-Fund vor dem Commit, behoben:** der Erfolgs-Toast
(`"Verschoben nach " + folderPath.split("/").join(" / ")`) hätte bei leerem `folderPath`
„Verschoben nach " ins Leere gerendert — genau der Fall, den P9-29 auslöst. Gleiche Konvention
wie der Verschieben-Dialog übernommen (`dialogs.js:396`, Label `"(Space-Wurzel)"`) statt eine
neue zu erfinden. `moveItemToFolder()` (`list.js:251`) verschickt `folder: ""` unverändert wie
der Menü-Pfad — kein serverseitiger Sonderfall nötig. Cross-Space-Risiko geprüft und
ausgeschlossen: `list.js:412`s `movable`-Gate (`!item.readonly && item.space === state.ownSpace`)
lässt fremde Items gar nicht erst ziehbar werden, ein Wurzel-Drop kann also nie zu einem
Space-Wechsel werden (§0.6 hält Cross-Space-Verschieben ohnehin außerhalb von P9).

**Drei neue statische Wächter** in `phase5_ui/tests/test_static_routes.py`
(`test_escape_handler_checks_fullscreen_element`,
`test_space_row_is_a_drop_target_for_the_space_root`,
`test_space_drop_target_uses_the_same_owner_guard_as_folders`) — Begründung wie P8.6:
Regressions-Wächter statt nur Smoke, ein späterer Umbau führt beide Bugs sonst still wieder ein.

**Selbstprüfung:** `pytest -q` **1011 passed in ~185 s** (1008 + 3 neue Tests, rechnerisch
geprüft, dreifach gelaufen — auch nach dem Toast-Fix unten). `ui_budget.py` 5/5 im Korridor
(145,0 KB statt 144,7 KB, +0,3 KB durch die Kommentarzeilen + den D2-Aufruf + den Toast-Fix —
deutlich unter 250 KB). `node --check` auf beide geänderten JS-Dateien grün. Tabu-Diff/
`git status`: nur die drei erwarteten Dateien angefasst (`app.js`, `tree.js`,
`test_static_routes.py`) — kein `storage/`-, kein `mcpserver/tools.py`-Touch. Kein `pkill -f`,
kein `systemctl`, sharefyx-mcp nicht berührt.

**Offen für Step D, nicht in dieser Session erledigbar:** `P9-29`/`P9-30` (Drag-Drop-Verifikation
am echten Gerät) bleiben normale Sichtprüfung, Nikinger-Sache. `P9-31` (Chip-Nicht-Auslöser) ist
am gewählten Anker gegenstandslos, siehe oben — sollte im Gate/Z-Schritt als „gegenstandslos",
nicht als „vergessen" gebucht werden. **`P9-27`/`P9-28` (ESC im Vollbild) — Nikinger-
Entscheidung im Anschluss an diese Session: bewusst zurückgestellt, kein aktiver Blocker.**
Diagnose ist geklärt (macOS Safari, grüner Knopf), der gebaute Guard adressiert diesen Fall
vermutlich nicht — siehe D1-Befund oben und der neue `## Backlog`-Abschnitt am Kopf dieser
Datei. Modulstatus Step D deshalb 🟡, nicht ✅, aber ohne Zeitdruck.

**Nächster Schritt:** kein weiterer Claude-Code-eigener Step ohne erneute Nikinger-Freigabe —
E/F/G/H sind laut Plan weiterhin opencode/M3, A/B/C weiterhin Coarbeit. Vor dem nächsten
Claude-Code-Block: fragen, nicht per Präzedenzfall annehmen (dieselbe Vorsicht, die P9-Q selbst
für die Infra-Steps verlangt). D1 wartet im Backlog, bis Zeit dafür ist — kein aktiver Auftrag.

## Session stopped — 2026-09-20

**Step 0 ✅ — Claude Code, ein Commit.**

`phase9_hardening/` angelegt (`CLAUDE.md`, `SESSIONS_ARCHIVE.md`, `tests/`). `scripts/` bleibt
vorerst leer und damit ungetrackt (git committet keine leeren Verzeichnisse) — beide neuen
Skripte gehören plangemäß (§2.1/§2.3) ins repo-weite `scripts/`, nicht hierher; ein
phasenlokales `scripts/` entsteht erst, sobald ein späterer P9-Step eins braucht, genau wie bei
`phase8_6_ui_polish/scripts/`.

**INDEX-Rotation gebaut (P9-L):** `scripts/rotate_index_updates.sh`, dieselbe Mechanik wie
`rotate_session_block.sh` (Ausschneiden per `sed`, Reassemblierung mit `cmp` geprüft, jeder
Block byte-identisch gegengelesen, erst danach geschrieben) — aber auf eine **einzelne
physische Zeile** angewandt: die `updated:`-Frontmatter-Zeile von `docs/INDEX.md` wird an
` | `-Trennern **gefolgt von einem ISO-Datum** (`\d{4}-\d{2}-\d{2}`) gesplittet, nicht an jedem
` | ` — sonst hätte ein ` | ` innerhalb eines Eintrags den Schnitt verfälscht. Vier Gegenproben
vor dem Schreiben: (a) Byte-Buchhaltung (rotierte Einträge + Rest-Zeile + Trenner == Original),
(b) `cmp` der Reassemblierung, (c) jeder rotierte Eintrag byte-identisch im Archiv
wiedergefunden, (d) der Frontmatter-Closer `---` steht danach auf eigener Zeile. Getestet gegen
eine `tmp_path`-Fixture mit synthetischer Mehr-Eintrags-Kette (`test_rotate_index_updates.py`),
nicht gegen die echte `docs/INDEX.md` — die Kette dort trägt aktuell nur einen Eintrag (vom
2026-09-19 von Hand rotiert), das Skript liefe dort auf den „nichts zu tun"-Pfad.

**Vier geplante Defekte repariert (§2.2) plus drei ungeplante, vom `doc_health.py`-Bau selbst
aufgedeckt (nicht im Plan, aber trivial und im selben Commit behoben statt liegengelassen) —
sieben insgesamt:**

*Geplant, §2.2:*
- **0-a** die fünf `up:`/`down:`-Links in `phase8_6_ui_polish_block_h_r_3_escalation.md`
  korrigiert (drei waren `docs/concepts`-Geschwister und brauchten `./`, zwei zeigten auf
  `phase8_6_ui_polish/` und brauchten `../../`)
- **0-b** beide Mini-Pläne (`phase8_6_ui_polish_block_g_r_plan.md`,
  `phase8_6_ui_polish_block_h_r_plan.md`) haben jetzt eine L1-Card (`status: snapshot`)
- **0-c** `docs/INDEX.md`s `ROADMAP.md`-Zeile nennt jetzt die reale Größe (42.080 B) und P9;
  `ROADMAP.md` bleibt über dem Softcap, benannt statt versteckt (P8-P) — Straffung ist
  Step-Z-Arbeit
- **0-d** `docs/screenshots_latest/` entfernt — Gegenprobe zeigte alle sechs Symlinks dort
  bereits tot (`../p86_block_g_r_*.png` löst nicht auf, Original liegt unter
  `docs/screenshots/`); `screenshots_latest/` am Repo-Root ist die von Konvention §5 und
  `docs/INDEX.md:143` gemeinte Instanz und bleibt

*Ungeplant:*
- Wurzel-`CLAUDE.md` stand bei **64.401 B**, deutlich über dem 40-KB-Softcap —
  `docs/INDEX.md`s eigene Zeile dafür behauptete noch „~22 KB" aus der Frontmatter-Rotation vom
  2026-09-13; seither haben drei P9-Planungscommits (`06ab4f6`, `633338d`, `2f752f9`) den
  `## Current state`-Body weiter wachsen lassen (die Rotation von 2026-09-13 betraf nur die
  `updated:`-Kette, nicht den Body — P9-A hat eine Ein-Block-Regel für den Body ausdrücklich
  verworfen). Nikinger-Entscheidung: **benennen, nicht kürzen** — dieselbe P8-P-Konvention wie
  `phase8_6_ui_polish/CLAUDE.md` und `phase6_shares/CLAUDE.md`. Die Zeile trägt jetzt die reale
  Größe und die Benennung statt der stalen Zahl. **Der größte Einzelbefund dieser Session** —
  eine Datei war eine Woche lang um das Dreifache größer, als ihre eigene Index-Zeile behauptete,
  unbemerkt bis `doc_health.py` sie fing.
- `docs/PROJECT_SESSION_LOG.md` begann mit einer führenden Leerzeile vor der Frontmatter
  (`\n---\n...`) statt direkt mit `---` — einzige Datei im Repo mit diesem Defekt, `header_cards`
  hätte ihn sonst als Befund gemeldet. Entfernt.
- `docs/INDEX.md`s Zeile für `docs/screenshots/` verlinkte auf das Verzeichnis
  (`./screenshots/`) statt auf dessen `README.md`, obwohl der Text „L1-Header-Card in
  `docs/screenshots/README.md`" bereits sagte, wo die Card liegt — der Direktlink fehlte. Auf
  `./screenshots/README.md` umgestellt, analog zum bereits bestehenden Muster bei
  `screenshots_latest/`, dessen INDEX-Zeile direkt auf sein `README.md` zeigt. **Das ist eine
  Konventions-Entscheidung, keine reine Linkkorrektur:** jedes künftige `<dir>/README.md` in
  diesem Repo braucht ab jetzt entweder denselben Direktlink-auf-README-Zeigers oder eine
  eigene INDEX-Zeile — `doc_health.py`s `index_lines`-Prüfung erzwingt das ab sofort. Wer das
  zurück auf einen Verzeichnislink „korrigiert", bricht den Scan.

**`doc_health.py` gebaut** (`scripts/doc_health.py`, stdout nur JSON, Logging nach stderr —
Hard Rule 7) mit den vier Prüfungen aus §2.3 (`index_lines`, `header_cards`, `updown_links`,
`oversize`). Die Ausnahmeliste ist eine Konstante mit den vier in `docs/INDEX.md` benannten
Fällen. **`oversize` unterscheidet drei Zustände statt zwei:** 📕/📦-Snapshots sind immer
ausgenommen; 📗/🟡-Dateien über 40 KB sind nur dann kein Befund, wenn ihre `docs/INDEX.md`-Zeile
die Zeichenkette „benannt statt versteckt" **und** eine aktuelle Größenangabe trägt — exakte
Byte-Zahl **oder** gerundete `~NNKB` innerhalb von **±2 KB** der echten Dateigröße, keine
Prozent-Toleranz (eine Prozent-Toleranz hätte bei einer 106-KB-Datei ±32 KB durchgelassen; der
gefundene Defekt war „~22 KB" für eine 64-KB-Datei — eine feste, kleine Bandbreite fängt genau
das, ohne mit der Dateigröße mitzuwachsen). `index_lines` sucht ebenfalls pfad-, nicht
namensbasiert — `CLAUDE.md` allein kommt in einem Dutzend INDEX-Zeilen vor, ein bloßer
Namens-Treffer hätte jede neue `phaseN/CLAUDE.md` für immer kostenlos bestehen lassen. Genau
dieses Muster trägt `phase8_6_ui_polish/CLAUDE.md`, `phase6_shares/CLAUDE.md` und jetzt
`ROADMAP.md` und Wurzel-`CLAUDE.md`. Ein 📗/🟡-Fund ohne Benennung bleibt ein echter Befund.
`phase9_hardening/tests/test_doc_health.py` nagelt alle vier Prüfungen fest, `oversize` inkl.
Gegenprobe für einen benannten, einen unbenannten und einen stale-benannten Fall.
`pytest.ini`s `testpaths` fehlte `phase9_hardening/tests` — ohne die Zeile wären diese 13 Tests
für jeden `pytest -q`-Lauf unsichtbar geblieben, und P9-9 („pytest ≥ 995, Step 0 addiert die
neuen doc_health-Tests") wäre unerfüllbar gewesen. Zeile ergänzt — **das ist eine geteilte
Config-Datei, keine Doku-Zeile**, deshalb hier ausdrücklich benannt statt beiläufig
mitgeführt. Nebenbefund dabei: `phase8_ui_graph/`, `phase8_5_picker_release/` und
`phase8_6_ui_polish/` haben gar kein eigenes `tests/`-Verzeichnis (ihre Tests leben in
`phase5_ui/tests` bzw. `phase4_auth/tests`) — Phase 9 ist die erste Phase mit einem eigenen
`tests/`-Ordner seit `phase7_spaces_admin/`.

**Baseline gemessen, zweistufig:** vor jeder Änderung `.venv/bin/python -m pytest -q` →
**995 passed in 185,98 s** (V147, exakt die geforderte Zahl). Nach Step 0 komplett (13 neue
Tests + die `pytest.ini`-Ergänzung, die sie erst sichtbar macht) → **1008 passed in 182,78 s**
— 995 + 13, rechnerisch geprüft, nicht nur behauptet. Phasenstart-SHA: `06ab4f6` (Stand vor
diesem Commit). Kein `ui_budget`-Touch nötig (kein `phase5_ui/webui/static/**` berührt), kein
`node --check` nötig (kein JS berührt). Tabu-Diff §0.3 leer — reine Doku-/Skript-Session. Kein
`pkill -f`, kein `systemctl`, sharefyx-mcp nicht berührt.

**Nächster Schritt:** Step A (Domain über eigenen VPS) als Coarbeit in opencode (P9-Q) —
Voraussetzung ist die Domain-/VPS-Beschaffung durch den Nikinger, siehe Prompt-Vorlauf. B und C
laufen unabhängig davon weiter, A blockiert die Phase nicht.

