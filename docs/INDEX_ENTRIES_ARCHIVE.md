---
status: archive
purpose: L3-Archiv der datierten Nachträge aus den Einträgen von `docs/INDEX.md` — verbatim, ein Abschnitt je Karte in der Reihenfolge der Karte
read-when: beim Audit, wenn die Herkunft einer INDEX-Änderung rekonstruiert werden muss, oder wenn eine Zahl aus einer Kartenzeile stammt, die hier steht
detail: L3
up: ./INDEX.md
down:
updated: 2026-10-03 (**erster Lauf** — 43 von 93 Einträgen, 37.391 B; der zweite Lauf meldet `Nichts zu tun` (exit 2), was `test_a_second_run_is_a_noop_exit_2` festhält) | 2026-10-03 (**angelegt** — Gate/Z, Nikinger-Entscheidung 2026-10-03 „Nachträge ins L3-Archiv, Kriterium neu baselinen". `docs/INDEX.md` wuchs am 2026-10-03 auf 71.491 B, davon **37.391 B datierte Nachträge in 43 von 93 Einträgen** — mehr als die Hälfte, und die seit Wochen als ungeklärt geführte Ursache der Überschreitung (P9-3/V145). Die `updated:`-Kette des INDEX ist **nicht** die Restmasse: sie hat 1.155 B und war am 2026-10-03 rotiert. Verschoben per `scripts/archive_index_entries.sh` mit fünf Gegenproben, darunter (b) die Reassemblierung des Originals byteweise und (d) „kein datierter Nachtrag bleibt im INDEX" — die unterscheidet Verschieben von Weglassen)
---

# Nachtrags-Archiv der INDEX-Karte

Jeder Abschnitt ist der **datierte Nachtrag einer Kartenzeile**, verbatim und ungekürzt. Im INDEX
selbst bleibt der Kopf jedes Eintrags: Glyph, Größe, Ein-Satz-Stand. Das ist die Trennung der
Doc-Layers-Konvention, auf L0 angewandt — die Karte ist der Stand, dieses Archiv ist die Chronik.

**Reihenfolge:** wie in der Karte, nicht newest-first. Ein Leser, der eine Kartenzeile liest und
ihren Nachtrag sucht, findet ihn über den Dateinamen; eine Chronik-Reihenfolge würde ihn zwingen,
43 Abschnitte zu durchsuchen.

**Was hier nicht steht und auch nicht hierher gehoert:** die `updated:`-Kette des INDEX
(`docs/INDEX_UPDATES_ARCHIVE.md`), die Session-Blöcke der Phase 9
(`phase9_hardening/SESSIONS_ARCHIVE.md`) und die Current-state-Chronik (`docs/PROJECT_SESSION_LOG.md`).
Vier Archive, vier verschiedene Sortierungen, weil sie vier verschiedene Fragen beantworten.

## `docs/INDEX.md`

**[2026-10-03] die Zusammensetzung ist gemessen, und sie widerspricht der bisherigen Annahme dreifach:** die `updated:`-Kette hat **1.155 B** und ist rotiert — eine weitere Rotation spart ~1 KB, nicht 30 KB · von 55.119 B Eintragsbytes in 93 Zeilen liegen **30.145 B** ab dem ersten datierten Nachtrag · **selbst 300 B je Zeile ergäben 39.971 B**, das Kriterium 38.912 B (P8.6 Plan 2 §1.2) ist **per Kürzen unerreichbar**, weil es für eine Datei mit weniger Zeilen gesetzt wurde. **Drei Wege raus, alle Nikinger-Entscheidung: Nachträge ins L3-Archiv · Kriterium neu baselinen · Benennung als Endzustand.** Beides prüft `phase9_hardening/tests/test_acceptance_numbers.py`, das einem meldet, wenn die Begründung überholt ist. [2026-10-03: **die gerundete Angabe ein zweites Mal mitgezogen** — der 17. Block (Kettenrotation, neue `phase9_hardening/UPDATES_ARCHIVE.md`-Zeile, korrigierte Phase-9-Head-Zeile) hat die Datei über das eigene ±2-KB-Fenster getrieben; jede Bytezahl dieser Datei ist ohnehin sofort wieder veraltet, das ist der Grund für die Rundung) (V145; **2026-10-02 (B17): +2,9 KB Pflichtpflege** — Phase-9-Head-/Archiv-Groessen, die `phase8_ui_graph`-Groesse mit der datierten Oversize-Benennung und zwei INDEX-Praefix-/Konventionszeilen; **jede eigene Groessenangabe dieser Datei ist der Grund, warum die Zahl sofort wieder veraltet**, deshalb gerundet; P9-L-Rotation der `updated:`-Kette) | **[2026-10-02]** **~57 KB, und damit heute größer als vorher (56.561 B auf HEAD)**, weil zwei Pflicht-Zeilen für die neuen Archive +58.396 gekostet haben und die `updated:`-Rotation nur 58.393 netto gespart hat. Die Kette rotiert ihrerseits wieder (Skript `scripts/rotate_index_updates.sh`, P9-L; **erster echter Lauf fand einen Defekt, jetzt Gegenprobe (e)**) — sie ist damit wieder klein, aber sie ist der kleinste Brocken dieser Datei: der Zuwachs war Pflichtpflege. Die Bytezahl bewusst gerundet, weil jede eigene Zeile die Zahl sofort wieder veraltet — `doc_health` akzeptiert `~NNKB` mit ±2 KB, siehe `scripts/doc_health.py :: _named_size_is_current`; **2026-10-01:** der Zuwachs (+1,8 KB) ist Pflichtpflege (Session-Block Phase 9, Phase-9-Head-Zeile, `screenshots/`-Präfixliste), nicht Weglassen)

## `CLAUDE.md`

**[2026-10-02] +6.536 B gegenueber 107.576 B, und die sind Pflichtpflege eines gebauten UI-Blocks** (B17: gemessene Korrektur zweier Zahlen, Lock-Konflikt, Gegenproben, drei eigene Fehler) · **diese Zeile führte drei widersprechende Groessen nebeneinander (99.051 / 58.091 / 53.040) — auf eine gebracht statt weitergeschrieben** · **[2026-10-02]** +106.139 gegenueber den 106.139 von gestern: der Gate/Z-Doku-Block (zwei Sektions-Rotationen + Skript-Defekt) ist Pflichtpflege eines laufenden Schritts, genau wie der trace-Block von ~4,9 KB gestern · **diese Zeile fuehrte drei widersprechende Groessen nebeneinander (99.051 / 58.091 / 53.040) — auf eine gebracht statt weitergeschrieben**; zuletzt dazu der **doing-Block-Block** (ein gebauter Step ist Pflichtpflege eines laufenden Schritts), davor der Block-doing-Planungsblock, davor der P9-Deploy-Absage-Block im Current state · **[2026-10-01, P9 Step A]** 106.139, ueber dem 40-KB-Softcap — benannt statt versteckt (P8-P); der A4-Vorbereitungs-Block waechst den Current state um ~2,6 KB — wie schon der Step-H-Eintrag, der einzige wachsende Abschnitt der Datei · **[2026-09-30, P9 Step B (zweiter Teil)]** 80.157 B, ueber dem 40-KB-Softcap (der Session-Eintrag zu Step H waechst den Body um ~4 KB — der einzige Current-state-Absatz, der noch waechst; die `updated:`-Kette ist seit 2026-09-13 rotiert) · **[2026-09-20, P9 Step 0]** 64.401 B, ueber dem 40-KB-Softcap — benannt statt versteckt (P8-P); die Frontmatter-`updated:`-Kette wurde 2026-09-13 nach `docs/PROJECT_SESSION_LOG.md` rotiert, seither ist nur der Body weitergewachsen (drei P9-Planungscommits)

## `README.md`

**[2026-09-02]** „Sneak Peak"-Sektion auf die vier `c4c5_*`-Screenshots aus Block C4+C5 umgestellt (Liquid-Glas-Akzente, Auswahl-Sheen, Editor-72ch, Anlege-Dialog-Glas); **[2026-09-01]** erstmals mit Screenshots bestückt (Sichtprüfung 1, neun Plex-Sans/Plex-Mono/Lucide-Icons-Bilder; seither zwei Mal ersetzt — `1b8c2b9` Block-D-Endstand mit sechs `sp2_*`, heute C4+C5-Endstand mit vier `c4c5_*`)

## `ROADMAP.md`

**[2026-09-30, nach P9 Step B]** **ROADMAP steht jetzt bei 48.498 B. 7.538 B über dem 40-KiB-Softcap — benannt statt versteckt** (P8-P): der Zuwachs ist die Step-H-Zeile der P9-Row, also Pflichtpflege · **[2026-09-30, nach P9 Step F+G]** **ROADMAP stand bei 45.351 B, 4.391 B über dem 40-KiB-Softcap — benannt statt versteckt** (P8-P): der Sprung von 42.080 B kam aus **Pflichtpflege** (zwei Step-Zeilen mit den Entscheidungen, die ein Leser sonst nicht nachvollziehen kann), nicht aus Weglassen. Straffung ist Step-Z-Arbeit. (Ursprünglicher Eintrag: 2026-09-20, P9 Step 0) — benannt statt versteckt (P8-P), Straffung ist Step-Z-Arbeit; P1–P5/P7/P8/P8.5 ✅, P6/P6.5 🟡, **P8.6 ✅**, **P9 🔄 in Arbeit** (Step 0 ✅, Step C 🟡, Step D 🟡, A/B/E/F/G/H ⬜)

## `docs/concepts/sichtpruefung_automation_conventions.md`

**[2026-09-08 neu]** wiederverwendbare Techniken, um eine scheinbar Mensch-/Connector-gebundene Sichtprüfung doch zu skripten: Canvas-Instrumentierung ohne App-Code-Änderung, Frame-Teiler-Trick gegen Dauerschleifen, OAuth-Dance ohne Browser gegen eine Wegwerf-Instanz, zwei-Principal-Wegwerf-Muster für Zweitnutzer-ACL-Tests, `mcp_smoke.py`-Fehlersignaturen; klärt auch, wann eine Sichtprüfung wirklich nicht substituierbar ist (Identität statt Verhalten)

## `docs/concepts/sichtpruefung_automation_tooling.md`

**[2026-09-28 ergänzt]** §Vormerkung zum **Modell** des Vision-Adapters: Messbefund aus P9 Step E (qualitative Fragen gut, **Zählen unbrauchbar** — dasselbe Bild, zwei Läufe, zwei Zahlen), Recherche: Zählen ist eine modellübergreifend dokumentierte VLM-Schwachstelle (arXiv 2605.30170, GroundCount 2603.10978, `qwen3-vl` namentlich in TrustNLP 2026) — **ein Modellwechsel ist nicht der Hebel**, sondern die Zuständigkeitsgrenze VLM-binär ↔ Messung-quantitativ; Kandidaten mit der Hardwaregrenze (6 GB RAM, nicht 12 GB VRAM) und ausdrücklich nicht gemessenen Größen · **[2026-09-11 Kernaussage umgekehrt, gemessen]** `minimax/MiniMax-M3` ist im models.dev-Katalog `attachment: true` + `modalities.input:[text,image,video]` — **M3 sieht Bilder in OpenCode nativ; das Vision-Plugin ist der Defekt, nicht die Lösung** (es löscht den FilePart). A/B/C/D-Messreihe mit `opencode run` (0 vs. 9 Tool-Calls; `read`-Tool 1 Call, plugin-unabhängig), Empfehlung = Rückbau statt Zusatz-Plugin, Plugin-Rangliste vom 2026-09-08 verbatim nach §Historisch (gilt weiter für M2.x). Zweitbefund: OpenCodes Web-UI hat **keinen Tool-Result-Bild-Slot** → Bilder fließen nur Mensch→Modell · **[2026-09-08 neu]** Werkzeug-Empfehlungen für automatisierte Sichtprüfungen (Playwright/CDP-Muster) in beiden CLIs

## `docs/PROMPTS.md`

**[2026-08-09]** Phasen-Abschluss läuft jetzt in Claude Code statt Browser+Google-Drive (Nikinger-Entscheidung, Effizienz); **[2026-08-18]** Prompt 1s Tests-Absatz nennt jetzt die Wegwerf-Instanz-Standing-Permission explizit (eigener Port/tmp-DATA_ROOT/eigenes venv, nie die echte laufende Instanz); **[2026-09-01]** Prompt 1s Hard-Rules-Liste um `pkill -f`-Verbot ergänzt (Verweis auf Hard Rule 9), Tests-Absatz um die operative Stopp-Regel für eigene Wegwerf-Instanzen erweitert (PID-Datei / `pgrep`-Anker / Port, nie Regex im Cmdline); lesen beim Start eines neuen Chats, nicht mitten in einer Session

## `docs/concepts/PHASE8_6_CLOSEOUT_HANDOVER.md`

**[2026-09-19]** **Abschluss**-Handover P8.6 → P9, Einstiegsdokument der P9-Planung. Status, Delta, **§4 die Entscheidungen — drei getroffen, der Rest offen**: §4.1 das Nikinger-Feedback vom 2026-09-19 in drei Klassen (zwei Bugs mit erstem Messbefund, ein Rechte-Thema, fuenf Feature-Wuensche), **§4.2 Domain = frueher P9-Schritt**, **§4.3 Tailscaled-Watchdog freigegeben** (mit der Tabelle, welcher Ansatz den gemessenen Vorfall ueberhaupt deckt), §4.4 INDEX-Rotation, §4.6 die offene Sichtpruefungs-Frage, **§4.8 GPU-Dienst auf der RTX 3060** (Empfehlung LXC auf dem 3060-Host, interner HTTP-Dienst — nicht in die sharefyx-VM; Umzug = eine Umgebungsvariable). Ersetzt den Partial-Closeout-Stand vom 2026-09-13, der in `373a431` erhalten bleibt

## `docs/concepts/phase8_6_ui_polish_uebersicht.svg`

**[2026-09-19 neu gezeichnet]** Uebersichtsgrafik 1080×1080, Badge **45 ✅ · 5 ⚠️ · 0 ⬜**. Zwei Bahnen (Plan 1 / Plan 2) mit der roten Bruchstelle der Sichtpruefung dazwischen; erklaert drei Dinge, die aus dem Code nicht ablesbar sind: warum es zwei Plaene brauchte, warum V102 ohne Server-Touch ging, warum die Gate-Ausgabe im Commit steht

## `phase8_5_picker_release/CLAUDE.md`

**[2026-09-09, Z-Closeout]** Phase-8.5-Head, Steps 0/A1/A2/B1/C/D/Z alle ✅, **Abnahmestand 20 ✅ · 0 🟡 von 20**, `v3.0.1` live-deployt (Release `20260905T140325.378914Z`) — **das ist bis heute der live laufende Release**. Code-Pfad: `phase5_ui/webui/static/{dialogs.js,editor.js,markdown.js}` + `phase2_mcp/mcpserver/tools.py:159-164` (`_TITLE_NOT_ID_HINT`)

## `phase8_5_picker_release/SESSIONS_ARCHIVE.md`

**[2026-09-09]** enthält seit dem Z-Closeout zusätzlich §Abnahmematrix-Archiv (20 Zeilen mit Beleg) und §updated-Pipe-Archiv (19 Frontmatter-Einträge des Heads, verbatim)

## `phase8_5_picker_release/SICHTPRUEFUNG_WALKTHROUGH.md`

**[2026-09-08, Doku-Sub-Session]** freundlicher Walkthrough für die Sichtprüfung am echten Gerät — Was-tust-du / Was-siehst-du pro Schritt, mit DevTools-Befehlen, Console-Snippets, Stoppuhr-Anleitung. Geschwister zum technischen `SICHTPRUEFUNG_RESTBLOCK.md` (denselben Inhalt dichter). Deckt C3-Rest (P8-21d/-22/-24) + C4 (P8-16 + P8.5-19/-3/-4/-17) + C5 (P8-5/-8 mit Fabian). Login-Snippet mit re-runnablem TOTP-Code (rollt alle 30 s) + Hard-Rule-9-konformer Cleanup-Befehl

## `phase8_5_picker_release/CLUSTER3_TESTBLOCK.md`

**[2026-09-07, Cluster-3-Teilverifikation]** Schritt-für-Schritt-Testblock nur für Phase-8-Cluster 3 (P8-20/-21/-22/-24) gegen eine 200-Knoten-Wegwerf-Instanz; älter, vom `SICHTPRUEFUNG_RESTBLOCK.md` abgelöst, bleibt als Audit-Quelle für Z erhalten

## `docs/concepts/phase8_5_picker_release_plan.md`

**[2026-09-09, Z-Closeout]** P8.5-Plan gegen `main@6272cad`, opencode/M3 ohne Advisor (N4). **Kernbefund:** ein Body-Link `[Titel](#item/itm_…)` ist bereits eine Graph-Kante (`storage/linkscan.py`). **§9 gefüllt = kanonischer Closeout**; §0.2 trägt datierte Korrekturnotizen an P8.5-S und P8.5-R (beide vom Nikinger umgekehrt). Gelockt N1–N7 + P8.5-A–P8.5-T, Abnahme 1–20, `[VERIFY]` V95–V105. 📕-Snapshot, vom Softcap ausgenommen

## `docs/concepts/PHASE8_5_CLOSEOUT_HANDOVER.md`

**[2026-09-09]** Abschluss-Handover P8.5→P8.6, Einstieg der ersten P8.6-Planung. Abnahmebilanz 20/20, **§4 die offenen Entscheidungen** (V102-Zwillingskante, Radiogruppe-Rückbau, CSRF-Origin-Mismatch im Wegwerf-Setup, Mobile-Außenkante aufgehoben), **§4.7 das geerbte Ledger — von P8.6 unangetastet**, `[VERIFY]` V95–V105, §7 die zwei umgekehrten Locks

## `docs/concepts/phase8_5_picker_release_uebersicht.svg`

**[2026-09-09 neu]** Übersichtsgrafik Phase 8.5 (1080×1080, Stil der Phase-7-Grafik: Status-Badge, Mission-Box, Flussdiagramm 0 → A1 → A2 → B1 → C → D → Z). Erklärt zwei Mechanismen, die aus dem Code nicht ablesbar sind: **ein Body-Link ist bereits eine Graph-Kante** (`linkscan.py` matcht das `itm_`-Token) und **die Zweiteilung des Deploys durch Hard Rule 9**. Umkehr des Locks P8.5-S, im Plan §0.2 datiert

## `phase9_hardening/CLAUDE.md`

**[2026-10-04, dritte Fassung desselben Tages — Nikinger-Entscheidung: Schritte, die am Fabi-Konto hängen, sind nie ein Phasen-Blocker.** P9-13 und V150 (das zweite Claude-Konto) standen zwei Sessions auf ⚠️ „1 von 2 Konten" und waren damit **faktisch ein Blocker durch eine Person**; beide Zeilen sind auf **⬜ mit Wanderungsvermerk nach P10** gesetzt, und **P9-15** (drei Läufe `/api/v1/overview` mit echter UI-Session) ist **die Arbeit der nächsten Session**. **Die Marke wechselt von ⚠️ auf ⬜, weil das zwei verschiedene Dinge sind:** ⚠️ heißt in der Matrix *erfüllt mit benannter Abweichung*, und ein Konto ist keine Abweichung, sondern ein fehlender Schritt. Die Regel selbst steht **generell** in der Wurzel-`CLAUDE.md` §Working style und als Nikinger-Entscheidung im Plan §0.1a — nicht nur hier. **Bilanzen folgen der Maschine, nicht der Hand:** Abnahme **71 ✅ · 9 ⚠️ · 3 ⬜**, `[VERIFY]` **31 ✅ · 1 ⚠️ · 2 ⬜**; V157 ist der einzige verbleibende ⚠️, V150 und V162 *(Lesart A)* die beiden ⬜.

**[2026-10-04, die ausführlichen Statusspalten sind in ein L3-Archiv gewandert — damit liegt der Phase-9-Head zum ersten Mal unter dem 40-KiB-Softcap.** `phase9_hardening/CLAUDE.md` **56.860 → 31.357 B**; die **§-Modulstatus-Tabelle trug 30.564 B in 14 Zeilen**, davon **15.041 B in drei** (Gate/Z 6.075 · A 4.915 · B 4.050). Jede Statusspalte steht jetzt **verbatim** in `phase9_hardening/MODULE_STATUS_ARCHIVE.md` (L3, eine Sektion je Step), im Head bleibt je Step ein **Kurzstand** mit Marker, Zustand, Offenem und Zeiger. Verlustfrei belegt: Roundtrip-Gegenprobe (Sektion == alte Zelle, Byte für Byte) und ein Wächter, der in **beide** Richtungen prüft (jede Zeile hat eine Sektion, keine Sektion ist leer, die Masse liegt über 95 %).

**[2026-10-04] beide Rotationen gefahren, und das Ergebnis ist die Antwort auf die offene Schnittzahl-Frage — sie ist gegenstandslos:** Session-Block (17.780 B verbatim nach `SESSIONS_ARCHIVE.md`) und `updated:`-Kette (6 von 7 Fäden nach `UPDATES_ARCHIVE.md`) ⇒ der Head stand bei 66.223 B und liegt nach beiden Rotationen bei 49.033 B; **die Ketten- und die Blockschnittfrage sind damit beide erledigt, und der Rest ist allein die §-Modulstatus-Tabelle ** (30.564 B in 14 Zeilen (Kopf + 13 Datenzeilen), davon 15.041 B in drei). K=1 ist die Konvention, und selbst K=1 passt nicht, weil nicht die *Anzahl* der Blöcke das Problem ist, sondern die Breite einer Tabelle. **Kürzen in ein L3-Archiv ist damit der letzte Hebel und ist Nikinger-Entscheidung** (verbatim + Roundtrip, am 2026-10-02 an `phase1_storage/CONTRACTS_ARCHIVE.md` und `phase5_ui/ABNAHME_MATRIX_ARCHIVE.md` bewährt). **Zwei Doku-Befunde aus derselben Messung:** zwei von dreizehn Statuszellen der Tabelle waren **unsichtbarer Text** (rohes `\|` ⇒ vier statt drei Zellen ⇒ Phantom-Spalte, 4.097 B, darunter der komplette V153-Block des Step B), behoben verlustfrei und repo-weit bewacht (`test_table_shape.py`); und `test_acceptance_numbers.py` **verwarf den Marker der zweiten `[VERIFY]`-Lesart**, weshalb V162 Lesart B unbemerkt von ⬜ auf ⚠️ wechseln konnte. **[2026-10-04] `ABNAHME_MATRIX.md`:** V162 *(Lesart B)* ⬜ → ⚠️ mit Zitat (Tailscale-Doku: ACLs gelten für Serve ausdrücklich, für `--tcp` schweigen die Docs in beide Richtungen) — die socat-Wahl ist damit nicht widerlegt, sondern gedeckt.

**[2026-10-03] die Aussage „zum ersten Mal unter dem Softcap, mit 806 B Luft" ist mit diesem Block datiert überholt: eine Rotation kauft genau eine Session, keinen Zustand** — 806 B Luft tragen keinen Session-Block, und dieser ist 8,2 KB groß. **der Hebel dafür ist weg: die seit gestern benannten „7.467 B durchgestrichene Statusabsätze" sind gemessen 189 B in der ganzen Datei** (Faktor 39) — die Masse ist der *lebendige* Modulstatus, 13.488 B in vier Zeilen · **Nikinger-Entscheidung, nicht getan** (siebzehnter Block: Kettenrotation; der achtzehnte Block, A7+A8, kostete davon wieder 1.048 B, Netto über beide Blöcke **−7.452 B**) — **[2026-10-03, Kettenrotation: die bisherige Überschreitung war falsch diagnostiziert, und zwar von mir zwei Tage zuvor.** Stand 57.873 B, davon **19.488 B `updated:`-Kette = 33 % der Datei** (37 Fäden); benannt war als Restmasse stattdessen die Rotation der 7.467 B durchgestrichenen Statusabsätze — Faktor 2,4 daneben. Gebaut: `scripts/rotate_index_updates.sh` um Zieldatei/Archiv erweitert (Default `docs/INDEX.md` unverändert, alle fünf Gegenproben unverändert), 36 von 37 Fäden verbatim nach `UPDATES_ARCHIVE.md`, Rekonstruktion byte-identisch · **58.661 → 40.694 B durch die Rotation, 39.106 B nach dem Session-Block-Wechsel** · **die Aussage „57.873 B — 16.913 B ÜBER dem Softcap, benannt statt versteckt" ist mit diesem Block datiert überholt**; das Streichen der Statusabsätze bleibt eine Nikinger-Entscheidung, ist aber **nicht mehr der Hebel** · **[2026-10-03, sechzehnter Block: Step D ist gefahren]** die letzte Abnahmezeile mit fehlendem Beleg — P9-28/-29/-30 von ⬜/⚠️ auf ✅ durch eine Browser-Probe (**16/16**, echte Maus-Input-Pipeline statt `dispatchEvent`, **zwei Gegenproben rot im Repo**), **6 Wächter**, **0 Zeilen Produktcode**; Matrix jetzt **68 ✅ · 9 ⚠️ · 6 ⬜** · **[2026-10-03] nach der Rotation des B17-Blocks, danach der Amend-Nachtrag und jetzt die **vierundzwanzigste** Rotation (der sechzehnte Block: Step D)** — `doc_health`s `oversize` hat die veraltete Zahl im selben Durchlauf gemeldet, das ist der Wächter bei seiner Arbeit — **dieselbe Passage behauptete bis hierhin, die Restmasse seien die 7.467 B durchgestrichenen Statusabsätze im Modulstatus und die Lösung sei deren Rotation: beides ist mit dem 17. Block datiert überholt** (die Kettenrotation spart ~18 KB), das Streichen der Statusabsätze selbst bleibt unangetastet eine Nikinger-Entscheidung · **[2026-10-02] vierzehnter Block: B17 GEBAUT** (opencode/M3, ein Commit, kein Deploy) — der
Notiz aus der Sichtung folgend war genau **ein** Knopf gemeint: **`.btn.action--caution` (1**, nicht 2
— der Selektor matcht nur `#archive-button`; `#logout-button` ist ein `.rail__action` und hat keine
Fläche). Die **13** `.btn-primary` sind **kein Reststand**, sondern deine dokumentierte Ausnahme vom
2026-10-01. Gebaut: die drei `.btn.action--caution`-Regeln **gelöscht**, nicht umgeschrieben (`.btn`
*ist* die Standardfläche), `:root` unberührt, die alte Familie `--btn-face-*` hängt jetzt
**badge-only** an `.rail__glyph`. **Der Befund war eine Helligkeit:** `#2A313A` ist heller als
`#0C1C31` — „Vorsicht“ war der auffälligste Knopf der Fußzeile statt des Standards. **Konflikt
zurückgestellt:** mein Vorschlag einer rot getönten `--caution-std-*`-Fläche brach zwei Lock-Zeilen
(Konvention v3: „**keine** gefüllte rote Fläche“) und fiel nach Rückfrage — es ist jetzt **exakt** die
Standardfläche, wortgleich v3 · **3 Wächter** (1 umgedreht mit Datum in beide Richtungen, 2 neu),
**Gegenprobe 4 Verstöße → 8 rote Assertions** · **Pixel-Probe 14/14**, Gegenlauf 6 rot (Δ 25–28) ·
`pytest` 1167 → **1169**, `ui_budget` 5/5 (mit Stash-Gegenprobe gemessen: **+0,2 KB** — die
protokollierte 155,1 KB war schon veraltet) · **benannt, nicht entschieden:** Kontrast der Vorschrift
4,38:1 (vorher 3,36:1) — besser, aber kein AA · **[2026-10-02] dreizehnter Block:
Gate/Z-Doku-Hälfte** (opencode/M3, ein Commit, kein Deploy, kein Code-Touch) — `phase1_storage` §Geerbte Contracts und `phase5_ui` §Abnahmestand **verbatim** in zwei neue L3-Archive rotiert (die beiden benannten Softcap-Überschreitungen sind damit weg) · **P9-L: INDEX-`updated:`-Kette rotiert, und der erste echte Lauf fand einen Skript-Defekt** — `rotate_index_updates.sh` rotierte **1 von 3** Fäden, weil einer ein `updated: `-Präfix trug, das der Split-Anker nicht sieht; **Gegenprobe (e)** + 2 Tests (Gegenprobe am Wächter: (e) entfernt → genau der Abbruch-Test rot) + 8 Rotations-Wächter in `test_doc_rotations.py` (Gegenprobe 5 Verstöße → 5 rot; **die (e)-Prüfung selbst war dabei zu blind und wurde repariert** — sie suchte das nackte `updated: ` irgendwo im Text, die Kette *erwähnt* die Zeichenkette aber, weil sie den Defekt beschreibt; jetzt wird nur der Fadenanfang ` | updated: <ISO>` geprüft, mit Test) · einundzwanzigste Rotation des Heads (trace-Block wandert verbatim ins Archiv) · `pytest` 1152 → **1162**, `doc_health` 0 · **[2026-10-02] zwölfter Block: Block trace GEBAUT** (Locks P9-Y–AD, **zehnte P1-Contract-Öffnung**, kein Index-Schema-Sprung) — `updated_by` serververwaltet + Git-**Autor**, UI „bei X“ / Feld **„Bei“** / Lesezeile „Zuletzt geändert von X“, **24 neue Tests**, `pytest` 1128 → **1152**, **Browser 8/8** gegen eine Zwei-Principalen-Instanz mit echter Git-Historie

## `phase9_hardening/ABNAHME_MATRIX.md`

**[2026-10-03] +2,1 KB aus dem Zahlen-Wächter-Block, und der Wächter hat mich dabei zuerst rot gemeldet, weil meine eigene Korrektur die Matrix über sein eigenes ±2-KB-Fenster hob** — der Scan bei seiner Arbeit; **[2026-10-03] A7a+A7+A8 gefahren** — P9-10b ✅ und P9-12 ✅ (beide mit Vorher/Nachher-Messung), P9-13/V150 ⚠️ „1 von 2 Konten", P9-15 bleibt ⬜ und gehört an den Deploy-Tag; **+3.329 B** aus genau diesen sechs Pflichtzeilen, jede mit Their-Beleg im Repo; · **[2026-10-03] die Zeile wuchs von 44.222 auf 47.551 B, weil sechs Abnahmezeilen an einem Tag belegt wurden** **[2026-10-03] Step D belegt** — die drei Zeilen P9-28/-29/-30 wandern von ⬜/⚠️ auf ✅ (Bilanz in der Datei selbst, nicht hier — sie wandert mit jedem Step); die Datei stand am selben Tag noch bei 40.573 B, also **+3.649 B aus Pflichtpflege eines gebauten Belegs**, nicht aus Weglassen — die Zeilen sind bewusst auf Stand + Beleg gestrafft, die Herleitung steht im Phase-Head-Block und im Docstring des Probeskripts · **die zwei benannten Wege raus**: der Deploy `v3.1.1` löst die vier „warten auf den Deploy“-Posten am Dateiende auf (~4 KB, ein Block), und die `updated:`-Kette ließe sich per `scripts/rotate_index_updates.sh` rotieren — das Skript ist allerdings auf `docs/INDEX.md` festgenagelt und braucht dafür eine Datei/Archiv-Angabe, ein benannter Restposten, **nicht** in diesem Block gebaut) · **[2026-10-03, erste Fassung]** **40.573 B, 387 B unter dem 40-KiB-Softcap** · **[2026-10-03 neu, Gate/Z-Doku-Hälfte zwei]** die Abnahmematrix der Phase 9 und die `[VERIFY]`-Bilanz als **eine** Datei: **82 Abnahmezeilen in 83 Tabellenzeilen (P9-10 in zwei prüfbare Hälften geteilt), **jede Zeile mit Stand und Beleg** — die **Bilanz steht nur in der Datei selbst** (sie wandert mit jedem Step; `phase9_hardening/tests/test_acceptance_numbers.py` zählt sie nach) (Testname, Probe-Datei, Journalzeile, Bild oder eine ausgeführte Messung); **kein ⬜ ist offene Code-Arbeit** (alle acht hängen an A7+A8 und am zurückgestellten D1, plus zwei Zeilen mit ausstehender Entscheidung) · **`[VERIFY]`: 34 belegte Einträge, nicht 40** — die Übergabezahl war die Größe des **Nummernbereichs** V145–V184, **V167–V172 sind in keiner Quelle definiert**; dazu **zwei Nummerkollisionen** (V162/V163 je zweimal vergeben, beide Lesarten je mit Stand geführt) · **drei Funde, die die Übergabe nicht trug:** P9-56 hat einen nicht angekündigten Tabu-Treffer (`phase7_spaces_admin/tests/test_space_removal.py`, 17 Z.), **GA2 (`p9_hardening_smoke.py`) wurde nie gebaut** — und genau P9-27/-29/-30 sind die Zeilen ohne Probe, und V155s beide Plan-Anker sind nach C6 gewandert · **durch Messung bewegt:** P9-14 geschlossen (Funnel live 200), P9-10b heute gemessen (weiter 400, wartet auf A7), P9-3/V145 und P9-6 von ✅ auf ⚠️ (Zahlen heute über der Grenze), V146/V148/V155/V182/V184 beantwortet. **Bei der nächsten Verdopplung eines Belegs ist die Rotation der `updated:`-Kette per `scripts/rotate_index_updates.sh` der benannte Weg**, nicht Kürzen (40 KB sind knapp)

## `phase9_hardening/step_a/RUNBOOK_STEP_A.md`

**[2026-10-03] A7+A8 ausgeführt und der Ablauf auf den Ist-Zustand nachgezogen** — A7a ist damit entschieden, §2 A7/A8 tragen jetzt den **Live-Zustand von `local.env`** (git-ignoriert, sonst nirgends), den Gate-Befehl, den Rückweg und die Erkenntnis, dass `LEGACY_*` nur die Web-UI schützt; **+3.365 B** aus dieser Nachpflege, die Aufgabenliste selbst ist unverändert; · **die drei Befunde vom 2026-10-01 sind der Zuwachs** (8 = P9-10 ist bis A7 nicht erfüllbar, 9 = auf dem VPS ist kein Caddy, 10 = `caddy validate` liest den Adapter aus dem Dateinamen), plus die Neufassung von A4 als A4a/A4b und der A4-Ergebnisblock Straffung ist Step-Z-Arbeit, nicht vor A4 · **[2026-10-01, A4 erledigt]** A4b vollständig geschlossen: der ACME-Platzhalter `deine@adresse.de` per `read`+`sed` durch die echte Adresse ersetzt, `notBefore` **unverändert** (keine Neuausstellung — die `email` gehört zum ACME-Konto, nicht zum Zertifikat; die Adresse steht bewusst nicht im Repo) · Befund 10 (`caddy validate` liest den Adapter aus dem Dateinamen: `Caddyfile*` ja, `caddyfile`/`A4b.Caddyfile` nein → `invalid character '#'`) + **A4a/A4b durch**: 2.6.2 via apt, `Valid configuration`, `certificate obtained successfully` (LE `YE1`, CN `sharefyx.eurofyx.com`) ⇒ **P9-10a ✅**; die erwartete `400 Invalid host header` extern **und** als `status=400 ua=curl/8.7.1` im Journal der Heim-VM — der Beweis, dass VPS → Tailnet → Relay → App steht · **[2026-10-01] Befund 8 + Befund 9** · **[2026-10-01] A5 ✅, Befund 4 korrigiert (Token-`resource`-Bindung), Befund 5 umentschieden** · **der geführte Step-A-Ablauf A1–A9** (Coarbeit nach P9-Q, ein Schritt pro Runde) mit **neun gemessenen Befunden**, die den Plan und den Ablauf korrigiert haben: **Plan-A4 ist unbaubar** (auf der Tailnet-IP lauscht nichts — `SPACE_HOST=127.0.0.1`, `ss -ltnp` belegt; `0.0.0.0` wäre P3-B gebrochen) und wird durch ein socat-Relay ersetzt · `/health` statt `/healthz` (P9-10) · `ALLOWED_HOSTS` fehlt in Plan-A7 · **V149 beantwortet** (alle Metadatenfelder abgeleitet, kein `iss`-Check beim Einlösen) · der Funnel bleibt nach A7 **lesbar, aber nicht beschreibbar** (CSRF-Origin exakt) · **V162 neu offen** (ACL-Durchsetzung von `tailscale serve --tcp`, der Grund für die socat-Wahl). Dazu `Caddyfile.template` (A4), `tailscale-acl.draft.json` (A3), `phase3_edge/systemd/sharefyx-tail-proxy.service` (der Relay) und 7 Wächter. **Stand 2026-10-01: A1/A2/A3/A0b/A5/A6 ✅ — offen ist genau A4** (A4a misst und installiert, A4b legt die Konfiguration; der VPS heißt `ubuntu`/100.121.142.113 und hat noch kein Caddy, Befund 9) · **Der Session-Fund: mein eigenes A6 hätte den Betrieb gekappt** — `ufw default deny incoming` gilt auch auf `tailscale0`, die SSH-Regel fehlte

## `phase9_hardening/step_b/RUNBOOK_STEP_B.md`

**[2026-10-01]** B2 zuerst gescheitert (`203/EXEC`): `local.env` setzt `REPO_ROOT=/opt/sharefyx/current`, also zeigt die Unit aufs Release, das das Skript (26.09.) nicht enthält — **B2a** installiert es nach `/usr/local/libexec/sharefyx/`, Nikinger-Entscheidung, tail-proxy-Muster. Und: **ein laufender Timer beweist nicht, dass ein Dienst arbeitet**. **Gelöst im dritten Takt:** `healthy: Self.Online=true` + `Finished` im Journal. **B3 hat dann einen echten Bug gefunden:** `RuntimeDirectoryPreserve=no` ⇒ systemd löschte die Rate-Limit-State-Datei nach jedem Takt, das Limit war nie in Kraft (zwei Restarts 189 s auseinander). Fix `RuntimeDirectoryPreserve=yes` + 2 Wächter; **der Test dafür war grün, weil sein Mock einen Zustandsspeicher simuliert, den es live nicht gibt** — vierte Wiederholung derselben Repo-Lehre. **P9-19 danach geschlossen:** erster Restart 9 s nach dem Stopp, danach **zehn Takte `rate-limited` ohne Restart**; nebenbei der `false`-Zweig von Stufe 1 live belegt. **Step B ✅.** Dazu die beiden Fallstricke: `install_units.sh` aktiviert nur `sharefyx-mcp` (und startet es neu), der Watchdog-Timer braucht ein eigenes `systemctl enable --now`. B3 (P9-19) nennt drei Induktions-Varianten mit ihren Risiken und eine Empfehlung

## `phase9_hardening/SESSIONS_ARCHIVE.md`

**[2026-10-03] siebenundzwanzigste Rotation** (der **neunzehnte** Block: die Zahlen der Matrix, `test_acceptance_numbers.py`) · **[2026-10-03] sechsundzwanzigste Rotation** (der **siebzehnte** Block — Kettenrotation des Heads, Skript verallgemeinert) | **[2026-10-03] fünfundzwanzigste Rotation** (der **siebzehnte** Block — Kettenrotation des Heads + Skript verallgemeinert; **dabei gefunden: die vorige Rotation hat der `updated:`-Zeile dieses Archivs das Präfix genommen** (Commit `aee387d`) — das Feld war für jedes Werkzeug unsichtbar, `doc_health` prüft es nicht und eine Rotation dieses Archivs wäre mit „Keine `updated:`-Zeile" abgebrochen; Präfix wiederhergestellt) | **[2026-10-03] vierundzwanzigste Rotation** (der **sechzehnte** Block — Step D gefahren, P9-28/-29/-30 ✅, Probe 16/16 mit zwei Gegenproben; der fünfzehnte steht in `ABNAHME_MATRIX.md`) | **[2026-10-03] dreiundzwanzigste Rotation** (der **fünfzehnte** Block — Abnahmematrix P9-1–P9-82 + `[VERIFY]`-Bilanz steht in `ABNAHME_MATRIX.md`, drei Funde die die Übergabe nicht trug: „40 Einträge" waren ein Nummernbereich, P9-56 hat einen nicht angekündigten Tabu-Treffer, GA2 wurde nie gebaut — genau P9-27/-29/-30 fehlen; der **vierzehnte** Block (B17) wandert verbatim hierher) · **[2026-10-02] zweiundzwanzigste Rotation** (der dreizehnte Block — Gate/Z-Doku-Hälfte

## `phase9_hardening/UPDATES_ARCHIVE.md`

**[2026-10-03] +2,3 KB: die Kette des Phase-9-Heads ist zum ersten Mal seit dem 2026-10-03 wieder rotiert worden (zwei verklebte Fäden, 45.126 → 42.836 B)** · **[2026-10-03 neu]** L3-Archiv der `updated:`-Kette des Phase-9-Heads, verbatim, newest-first — **36 von 37 Fäden** bei der ersten Rotation (Kette 19.488 B → 1.426 B). Entstanden, weil dieselbe Regel bis dahin an `docs/INDEX.md` **festgenagelt** war, obwohl jeder lebende Head dieselbe Kette trägt: `rotate_index_updates.sh` nimmt jetzt Zieldatei + Archiv als Argumente (Default unverändert). **Vier der Fäden trugen ein ` | updated: `-Präfix** — derselbe Defekt wie am 2026-10-02 in der INDEX-Kette, für den es die Gegenprobe (e) gibt; ohne sie wäre der Lauf abgebrochen, nicht halb rotiert. Rekonstruktion `gekaufter Faden + 36 Archiv-Fäden == alte Kette` byte-identisch (20.266 B), jeder Faden genau einmal
— wandert verbatim hierher, neuer Head-Block = B17 gebaut; Head 63.470 B → 53.968 B) ·
**[2026-10-02] zwanzigste Rotation (der zwölfte Block angehängt, der elfte verbatim ins Archiv; Head 46.993 B → 42.012 B)** · **[2026-10-02] neunzehnte Rotationder P9-Plan**, ausfuehrungsreif, 📕-Snapshot gegen `main@2f752f9`. Locks **P9-A–P9-T**, Abnahme **P9-1–P9-58**, `[VERIFY]` **V145–V164** plus die drei geerbten (V118, V136, V120). **Zwei Befunde, die eine Handover-Annahme widerlegen:** Tailscale Funnel kann keine eigene Domain (der CNAME-Weg aus `PHASE8_6_CLOSEOUT_HANDOVER.md` §4.2 existiert nicht, P9-E), und `SharePolicy` ist bereits gebaut — das Cross-Space-Rechte-Thema braucht **kein** fertiges P6 (§0.6). §12 ist der kanonische Closeout, §15 die P10-Liste

## `docs/concepts/phase9_hardening_block_trace_plan.md`

**[2026-10-02] §9 gefüllt (opencode/M3) — 🔄 → 📕, ab jetzt nicht mehr editiert** — 8 ✅ · 1 ⚠️ · 0 ⬜ (P9-69–P9-82), Browser 8/8 mit Gegenlauf, `pytest` 1128 → **1152**. **Eine Plan-Klammer war ungenau** (P9-AA: POST verwirft `updated_by` lautlos statt `ValidationError` — PATCH und der Kern lehnen ab), **eine Stelle mehr gebaut als geplant** (`mcpserver/receipts.py` für P9-72 „Schreibantworten“). Locks P9-Y–P9-AD, Abnahme P9-69–P9-82, `[VERIFY]` V179–V184 · **[2026-10-02] geschrieben (Claude Code), ausführungsreif für opencode/M3**

## `docs/concepts/phase9_hardening_block_doing_plan.md`

**[2026-10-02] gebaut (opencode/M3), §12 Ergebnis: 8 ✅ · 0 ⚠️ · 1 ⬜** — 🔄 → 📕, ab jetzt nicht mehr editiert (📕-Snapshot, vom Softcap ausgenommen), Voraussetzung für den Deploy `v3.1.0`: fünfter `_BUCKETS`-Eintrag „In Arbeit" (Lock **P9-V**, Nikinger-Entscheidung Kandidat (a); (b) Menge und (c) Select-Verzicht mit Argument verworfen), Sprachebenen **P9-W** (nur Rail-Label übersetzt, REST/MCP roh — LLM liest `doing` + `assignee`), Reihenfolge **P9-X**. Abnahme **P9-59–P9-68**, `[VERIFY]` V173–V178, Testliste T1–T8 mit Gegenlauf, Browser-Beleg auf Wegwerf-Port 18776, Deploy-Nachschub §8 (Nikinger)

## `docs/concepts/p8x_ui_polish_notes.md`

**[2026-09-09, P8.6 Step 0]** die sechs `up:`/`down:`-Links dieser Datei waren alle unaufloesbar (`../` statt `../../`) — Fix in P8.6 Step 0, siehe Plan §1.2

## `phase8_ui_graph/CLAUDE.md`

**[2026-10-02, B17] zwei Stellen
datiert korrigiert:** die Kategorie-Zeile („keine gefüllte rote Fläche“) ist **wörtlich gültig** und
war zwischen dem 2026-10-01 und dem 2026-10-02 **nicht eingehalten** (`#archive-button` behielt die
alte graue Fläche, die heller ist als die Standardfläche); die P9-Notiz „behält die graue Plastik“ ist
damit ausdrücklich überholt. §7-Abnahmematrix, C0-Anti-AI-Audit, Z-Closeout-Block; Beweis-Tabellen im `SESSIONS_ARCHIVE.md`. Code-Pfad: `storage/linkscan.py` (achte P1-Contract-Oeffnung), `webui/api.py :: _graph_get`, `webui/static/js/{graph,list,dialogs,app,editor}.js`. **[2026-09-13, V111 geschlossen]** 43.190 B, ueber dem 40-KB-Softcap — benannt statt versteckt (P8-P); die Zeile nannte bis heute die veraltete Zahl 42.343 B plus eine Schaetzung

## `phase8_ui_graph/SESSIONS_ARCHIVE.md`

**[2026-09-02]** sechsundzwanzig Einträge nach achtzehnter Rotation (Vormerkung-3-Punkt-1-Block nach Fixes-A/B/C-Session ins Archiv, Phase-8-Head jetzt mit dem neuen Session-Block allein)

## `phase7_spaces_admin/CLAUDE.md`

**[2026-08-28, zweite Rotation]** wieder unter dem 40KB-Softcap. Step Z (Closeout) — Nikinger-Entscheidung ✅ statt 🟡 (Matrix vollständig durchgelaufen, anders als P6), `PHASE7_CLOSEOUT_HANDOVER.md` + Übersichtsgrafik neu, sechste und siebte P1-Contract-Öffnung geschlossen. Abnahmestand **22 ✅ · 2 ❌ · 0 ungeprüft**, 904 Tests grün; read + newest Session-stopped block first

## `docs/concepts/PHASE7_CLOSEOUT_HANDOVER.md`

**[2026-08-28]** Abschluss-Handover P7→P8, Einstieg der Phase-8-Planung. Abnahme 22/24, §4 offene Entscheidungen (P7-24 TOTP-Replay, `spacectl.py remove-space` reindiziert nicht — Live-Incident 2026-08-27), geerbtes Ledger, `[VERIFY]` V71–V80 (nur V79 offen), P1-Contract beide Öffnungen geschlossen, **§7 die geänderte Arbeitsweise** (Claude Code plant, opencode/M3 führt aus)

## `phase6_shares/ITEM_MOVE_PLAN.md`

**[2026-08-13 neu, 2026-08-17 erweitert und gelockt]** Zusatzplan zu P6 Step 7: Item-Verschieben zwischen Ordnern und Spaces (Step 7b, Entscheidungen P6-AD–AJ, gelockt per Nikinger-Freigabe, `[VERIFY]` V52–V55 geschlossen) + §9 Mehrfachauswahl (P6-AK–AN, kein neuer Endpunkt/MCP-Tool) + Textfarben-Lesbarkeitsfix (Step 7a, ✅ gebaut). Abnahme 25–34, Nebenbefunde O6/O7. Nahe am 40KB-Softcap — nächste Erweiterung braucht Größenprüfung vor dem Schreiben. Geteilte Spaces über UI anlegen bleibt ausdrücklich draußen (P6-V)

## `phase6_shares/GLOBAL_SEARCH_PLAN.md`

**[2026-08-19] gebaut + Playwright-verifiziert** (10/10 grün, V57/V58 geschlossen) — ein Advisor-Fund: `editor.js :: clearDetail()` setzte `state.scope` nicht zurück. Q1 (nur Titel/Tags, keine Body-Suche) vom Nikinger entschieden. **[2026-08-23] live deployt**, Zeilen 35/38/39 bestanden, 36/37 brauchen Fabian

## `phase6_shares/IMAGES_PLAN.md`

**[2026-08-19 neu, 2026-08-20 nachrangig]** Zusatzplan **Block C — Bilder** (im P6-Plan nur stichwortartig), **abgelöst durch `docs/concepts/phase6_5_tools_images_plan.md`** — alle B1–B5 dort gelockt, `[VERIFY]` V59–V62 dorthin übernommen (kein Duplikat). Bleibt als Herkunftsnachweis der Bauart-Vorgabe (`<space>/_assets/<item_id>/`, `RESERVED_DIR_NAMES`, `![Alt](asset:ast_…)`) stehen, wird nicht mehr weitergepflegt

## `docs/concepts/PHASE6_CLOSEOUT_HANDOVER.md`

**[2026-08-23]** Abschluss-Handover P6. **Kernsatz: code-complete + live deployt, aber nur 12 von 39 Abnahmezeilen live bestanden** — §3 ersetzt das fehlende `P6_ABNAHME_*.md`. Zwei Nikinger-Aufgaben (§4.1 Doku-Audit, §4.2 fehlender Entfernen-Knopf), offene Entscheidungen §5.1–§5.7, Befunde O4–O7, `[VERIFY]` V39–V58 + geerbtes V12

## `phase6_5_tools_images/CLAUDE.md`

**[2026-08-25]** Live-Instanz auf `main`@`53bad20`, P6.5-12 per echtem Browser-Klick gegen `testnutzer-p7` bestanden. **Abnahmestand 13/14, Block A 4/4, Block B 9/10.** Offen: P6.5-14 (Nikingers eigene Bewertung, strukturell offen). V64/`filename`-Persistenzfrage unverändert offen; read + newest Session-stopped block first

## `docs/concepts/PHASE6_5_CLOSEOUT_HANDOVER.md`

**[2026-08-23 neu, P7 Step A8.3]** Abschluss-Handover P6.5→Block C dieser Phase. Status/Delta seit dem P6-Handover, Abnahmestand-Tabelle P6.5-1–14 (12/14), zwei offene Entscheidungen (P6.5-14, `_trash/`-Räumung), `[VERIFY]`-Bilanz V59–V70

## `phase5_ui/CLAUDE.md`

**[2026-10-02, P9 Gate/Z-Doku-Pflege P9-L] §Abnahmestand rotiert:** 99 Zeilen / 12.195 B wanden **verbatim** (inkl. der Kurzfassung, der beiden späteren Nachträge (2026-08-13-Korrektur, 2026-10-02 trace-Block) und der Cutover-Notiz) nach `ABNAHME_MATRIX_ARCHIVE.md`; der Head behält Stand + Zeiger und „20/20 ✅, Phase 5 ✅“ wörtlich (43.801 B → 33.280 B, **2.841 B → 0 B**). Die Phase ist seit 2026-08-09 geschlossen, die Matrix seither nie nachgezogen — gewachsenes Deckmaterial, kein lebender Status · Phase-5-Head; Steps 0–8b ✅· Phase-5-Head; Steps 0–8b ✅ (Block A Sicherheit/Selbstverwaltung + Block B REST-API/UI, hartes Gate dazwischen) — **20/20 Abnahmezeilen live, Phase 5 ✅** (2026-08-09). Enthaelt die vollstaendige Abnahmematrix, Modul-Status je Step und die Live-Debugging-Historie (Origin/CSRF-Fund, Step-7b-Revision, S9). 40.957 B — **3 B unter** dem Softcap (die gegenteilige Behauptung stand hier bis 2026-09-10 falsch). Head + neuesten Session-Block zuerst lesen

## `phase5_ui/ABNAHME_MATRIX_ARCHIVE.md`

**[2026-10-02, P9 Gate/Z-Doku-Pflege P9-L neu]** L3-Archiv des Abschnitts „Abnahmestand (Plan §6)" aus `phase5_ui/CLAUDE.md` — die 20-Zeilen-Matrix mit Kriterium, Stand und Beleg, dazu die vier Nachträge und die Cutover-Notiz, verbatim (99 Zeilen / 12.195 B). Phase 5 ist seit 2026-08-09 abgeschlossen und die Matrix seither nie nachgezogen — gewachsenes Deckmaterial; der Head behält den Stand (20/20 ✅, Phase 5 ✅) und den Zeiger

## `phase3_edge/CLAUDE.md`

**[2026-09-18]** Tailscale-Account-Migration hat den Funnel zerstoert (Tailnet-Suffix `tail89fc2a.ts.net` → `tail4a8b49.ts.net`) — behoben, alle sechs `diagnose.sh`-Pruefungen wieder gruen; neue URL `https://savefyx-vmware-virtual-platform.tail4a8b49.ts.net`. **2026-09-30:** neues Verzeichnis `phase3_edge/polkit/` mit der einen Regel, ohne die der tailscaled-watchdog seinen Befehl nicht ausführen dürfte (V153: `sudoers` ist unter `NoNewPrivileges` unbaubar — `setpriv` belegt es; polkit kennt auf systemd 255 nur die grobe `manage-units`-Aktion, deshalb JS-Regel mit `unit`-Attribut-Abgleich). **Zwei Fallstricke dokumentiert:** `install_units.sh` restart't keinen bereits laufenden Dienst, und der Funnel ueberlebt einen Reboot nicht immer sauber (`sudo systemctl restart tailscaled` behebt es). **Watchdog: seit 2026-09-19 freigegeben**, Form in `PHASE8_6_CLOSEOUT_HANDOVER.md` §4.3; read + newest Session-stopped block first

## `phase1_storage/CLAUDE.md`

**[2026-10-02, P9 Gate/Z-Doku-Pflege P9-L] §Geerbte Contracts rotiert:** 388 Zeilen / 31.422 B wanden **verbatim** nach `CONTRACTS_ARCHIVE.md`, der Head trägt nur noch Öffnungs-Index + Abschluss-Zusicherung (47.570 B → 20.212 B, **6.610 B → 0 B**). Die Datei hatte die Lösung seit 2026-09-30 selbst benannt (Rotation, nicht Kürzen) · **[2026-10-02, P9 Block trace] zehnte, benannte Contract-Öffnung gebaut** — `Item`/`ItemSummary` bekommen `updated_by`, `actor: str = ""` an allen neun Store-Schreibmethoden, `history.commit(author=)`; **kein Index-Schema-Sprung**; enge Probe = **genau drei Dateien**; `pytest` 1128 → **1152** · **[2026-09-30, P9 Step F] neunte, benannte Contract-Öffnung gebaut** — `doing` als Task-Status (`note` unverändert), `assignee` mit Index-Spalte, `INDEX_SCHEMA_VERSION` 3 → 4, **keine Migration**; **V160 = Space-Name ohne Validierung (Lock P9-U)**; `pytest` 1039 → 1062 · **[2026-08-09, P6 Step 1]** dritte, benannte Contract-Öffnung — `store.py :: patch()` + `patch.py` (neu), 81 Tests · **[2026-08-25, P7 Step C4]** siebte — `move()` erlaubt Space-Wechsel für archivierte Items; 154 Tests · phase head; alle acht Module ✅, live-verifiziert gegen den echten DATA_ROOT (2026-07-25); Frontmatter-Schema + `Store`-Signaturen Contract für P2 · **Altlasten dieser Zeile entfernt statt weitergeschrieben:** bis 2026-09-30 stand sie auf „~31KB" bei real 37 KB, danach auf 43.333 B bei real 47.570 B

## `phase1_storage/CONTRACTS_ARCHIVE.md`

**[2026-10-02, P9 Gate/Z-Doku-Pflege P9-L neu]** L3-Archiv des Abschnitts „Geerbte Contracts" aus `phase1_storage/CLAUDE.md` — alle benannten P1-Contract-Öffnungen verbatim (388 Zeilen / 31.422 B), in der Reihenfolge des Originals. Entstanden durch **Rotation, nicht durch Kürzen**: die Datei stand bei 47.570 B (6.610 B über dem Softcap), und der Vermerk vom 2026-09-30 im Head hatte Ursache und Lösung selbst benannt (zehn Öffnungen an einem Ort). Der Head trägt jetzt nur noch den Öffnungs-Index + die Abschluss-Zusicherung; wörtliche Verweise aus `phase6_shares_plan.md`, `PHASE7_CLOSEOUT_HANDOVER.md` §4, P8-M und den P9-Plänen auf „§Geerbte Contracts" bleiben auflösbar, weil der Abschnittsname im Head erhalten blieb

## `docs/INDEX_UPDATES_ARCHIVE.md`

**[2026-09-23]** zweite Rotation per `scripts/rotate_index_updates.sh` (P9-L, gebaut in P9 Step 0), erste Skript-Rotation dieser Kette

## `screenshots_latest/`

**[2026-09-11, Nikinger-Vorgabe neu]** Schnellzugriff auf die Screenshots der aktuellen Phase; Symlinks auf `docs/screenshots/<phase>_*`, README.md mit der aktuellen Tabelle (Dateiname → Original + Checkkriterium); beim Phasenwechsel rotieren (alte Symlinks weg, neue anlegen, README ersetzen); siehe Konvention `docs/concepts/sichtpruefung_automation_conventions.md` §5

## `phase5_ui/THIRD_PARTY_LICENSES.md`

**[2026-09-10, P8.6 Step 0]** Lucide ISC/MIT + Plex OFL. als vendored Bibliotheken unter `phase5_ui/vendor/`; **keine L1-Card** (dokumentierte Ausnahme der Card-Pflicht — Lizenztext gehört zu den vier Ausnahmen in Plan §1.3), INDEX-Zeile aber fällig (sie betrifft die Card, nicht den Index)
