---
status: snapshot
purpose: Plan Phase 11 (Editor in Writer-Optik, Oberfläche, Review-Rest) gegen main@1128fdb — Rahmen für die ganze Phase. Zuschnitt, Locks P11-A–W, Arbeitsregeln, Blockübersicht, Abnahme P11-1–34, [VERIFY] ab V220, Bedarf an Eurofleet, Fehlbilder. Die Schritte von Block 0 und Block 1 stehen ausführungsreif in der Schwesterdatei.
read-when: vor jedem P11-Schritt — §0, §2, §7 ganz; dann nur den eigenen Schritt in phase11_editor_plan_block1.md
detail: L2
up: ../../ROADMAP.md
down:
  - ./phase11_editor_plan_block1.md            # 📕 Block 0 + Block 1: Schritte, Anker, Tests, Startaufträge
  - ../../phase11_editor/CLAUDE.md             # 🔄 Head: Modulstatus, Abnahmestand, Startaufträge, Session-Block
  - ./PHASE10_5_CLOSEOUT_HANDOVER.md           # 📕 Einstieg, Vormerkungen §6
  - ./phase10_5_editor_4_1_plan.md             # 📗 Editor-Plan: Befunde F1–F14, Verträge §4, Schritte S3a–S11
  - ./phase10_5_editor_4_1_plan_anhang.md      # 📗 Messmethoden A1–A15
  - ./eurofleet_stand_2026-11-08.md            # 📗 Ausführer, Kontingent
updated: 2026-11-14 (Abschluss-Durchgang vor dem ersten Commit: B0.3-Befehle, Undo- und Esc-Fallen, Vendor ohne Netz, neue Fehlbilder; §6 V227/V228/V234 geprüft) | 2026-11-13 (angelegt — Planungssitzung P11; Baseline, zwei Prototypen und ein Machbarkeitstest gemessen; nichts am Produkt gebaut)
---
# Phase 11 — Editor in Writer-Optik (Plan, Rahmen)

> **Leitziel (Nikinger, 2026-11-07):** der Editor sieht aus wie ein Word- oder Writer-Dokument. Die Datei bleibt Markdown.
> **Auftrag der Phase (Nikinger, 2026-11-12/13):** vollständiger Umbau des Editors; Tabellen bearbeiten „wie in Excel";
> danach die Oberfläche nach festen Regeln; fünf Feedback-Punkte (§1.2). Ausgeliefert wird Block 1 als **`v4.1.0`**.

## Leseanleitung (für jeden Ausführer — zuerst lesen)

1. Lies hier **§0, §2 und §7 ganz**. Lies danach in `phase11_editor_plan_block1.md` **nur deinen Schritt**:
   `grep -n '^## B' docs/concepts/phase11_editor_plan_block1.md`, dann `sed -n '<von>,<bis>p' … | cut -c1-240`.
2. **Langzeilen-Falle:** die Doku dieses Repos hat Absätze als Einzelzeilen. Jede Shell-Ausgabe mit `| cut -c1-240` begrenzen.
3. **Der String ist der Anker, die Zeilennummer die Abkürzung.** Vor jedem Edit:
   `.venv/bin/python phase11_editor/scripts/plan_anker.py <Schritt>` — das Skript nennt die **heutige** Zeile jedes Ankers
   und meldet, wenn einer nicht genau einmal vorkommt.
4. **Eine Sitzung je Schritt**, Kontext höchstens 200.000 Tokens. Übergabe nur über den Session-Block im Head.
5. Was in §6 **nicht** steht, ist am Code geprüft (Datum 2026-11-12/13, `main@1128fdb`). Was dort steht, prüfst du, bevor du baust.

---

## §0 Gelockte Entscheidungen

| Lock | Entscheidung | Begründung (damit niemand sie gutgemeint aufmacht) |
|---|---|---|
| **P11-A** | **Umfang** = Blöcke 0–3 und Z nach §1 und §3. Was dort „später" oder „entfällt" heißt, wird in P11 nicht gebaut. | Nikinger 2026-11-13 (Zuschnitt angenommen) |
| **P11-B** | **Der Editor bleibt CodeMirror 5.65.16.** Kein CodeMirror 6, kein WYSIWYG-Editor mit Markdown-Serialisierung (ProseMirror, TipTap, Milkdown). | CM6 braucht ein offline gebautes Bündel (P5-T: kein Build-Schritt) und +40 KB. Ein serialisierender Editor schreibt die Datei neu und bricht den Byte-Vertrag (P11-F). |
| **P11-C** | **Markdown-Zeichen werden eingeklappt**, per `cm.markText(…, {collapsed: true})`, nicht per CSS versteckt. | `visibility: hidden` behält den Platz (Einzug vor Überschriften, Lücken um Fettdruck — Bild 3 des Nikingers). Gemessen 2026-11-13: Klickgenauigkeit 19/19, Bytes gleich, beide Browser. |
| **P11-D** | **Aufdeck-Regel.** Ein Inline-Element (fett, kursiv, Code, durchgestrichen, Link, Format-Form `[Text]{.rot}`) zeigt seine Zeichen nur, solange der Cursor es **berührt**. `# ` und `> ` nur auf der Cursorzeile. Das Listenzeichen `- ` ist ein Punkt, außer der Cursor steht im Zeichen. **Nur Paare** werden eingeklappt; ein einzelnes `*` bleibt sichtbar. **Maus:** aufgedeckt wird erst **450 ms nach `mouseup`**. | Ohne Mausregel scheitern in Firefox der Doppelklick auf Fettdruck und der Dreifachklick auf Überschriften; Ziehen über Zeichen bricht in beiden Browsern ab (gemessen 2026-11-13). Ein einzelnes eingeklapptes `*` wäre ein unsichtbar gelöschtes Inhaltszeichen. |
| **P11-E** | **Eine Darstellungs-Wahrheit:** marked **18.1.3** (vendort, nachgeladen) hinter der Fassade `js/markdown.js`, für Lesesicht, Update-Log und Tabellen-Widget. Der eigene Sanitizer bleibt die letzte Schranke. | Editor-Plan E2: 535 von 544 GFM-Beispielen statt 164. Zwei Parser (CM5-Modus, marked) entscheiden sonst unbemerkt verschieden — deshalb die Zelle `gleichtext` (P11-9). |
| **P11-F** | **Byte-Vertrag V1–V7 gilt unverändert** (Editor-Plan §4.2). Neu **V8 (Raster):** ein Zell-Edit ändert nur den getrimmten Inhalt dieser Zelle; ein getipptes `\|` wird `\\|`, ein Zeilenumbruch `<br>`; nie auffüllen, nie neu ausrichten; ein Strukturbefehl ändert nur Zeilen dieser Tabelle. | Hard Rule 2 (Dateien sind die Wahrheit). `\\|` und `<br>` sind die einzigen Zeichen, die der Editor schreibt, ohne dass sie getippt wurden — ohne sie zerfiele die Tabelle. |
| **P11-G** | **Tabellen „wie in Excel" = Bedienmodell:** Zellcursor, Pfeiltasten, Tippen ersetzt, F2/Enter/Doppelklick bearbeitet, Enter und Tab schreiben und springen, Esc verwirft, Entf leert, Bereich wählen, Kopieren und Einfügen als TSV, Zeilen und Spalten einfügen und löschen. **Anzeige = gerenderte Zelle, Bearbeitung = Quelltext der Zelle** (wie Formel und Wert in Excel). Keine Formeln, keine verbundenen Zellen, keine Spaltenbreiten. | Nikinger 2026-11-13. Eine frei editierbare gerenderte Zelle wäre Rückserialisierung im Kleinen (P11-B). Formeln und verbundene Zellen kennt GFM nicht; ED-4 (eigener Item-Typ) bleibt „später". |
| **P11-H** | **Reihenfolge Block 1:** Probe-Fundament → Oberfläche → Typografie → Renderer → Editor-Modus → Einklappen → Tasten → Raster → Suche → Gate → Sichtung → Release. | Der Modus-Schritt ändert die Tokens, aus denen das Einklappen baut; Zellgrenzen stimmen erst mit dem neuen Renderer. Die ersten drei Schritte baut Claude Code — so beginnen die Ausführer-Schritte erst, wenn das MiniMax-Kontingent weniger knapp ist. |
| **P11-I** | **Ausführer:** Schritte mit **C** baut Claude Code; Schritte mit **E** baut opencode mit MiniMax M3.1 Flash, Rückfall MiniMax M3, danach Claude Code. **Ein Ausführerwechsel ist kein Planwechsel.** Jeder Commit trägt den Modell-Trailer; je Sitzung stehen Wanduhr, Kontingent (wenn sichtbar) und Eingriffe im Session-Block. | Nikinger 2026-11-13; eurofleet-Notiz §4 (Rohdaten für die Harness-Bewertung). |
| **P11-J** | **Bildurteile fällen nur Claude Code oder der Nikinger.** Ein Ausführer, der Bilder nur über `local_vision` sieht, schreibt kein Bildurteil in einen Bericht. Schritte mit Bildurteil tragen 🖼. | Block 14.6: das lokale Vision-Modell widersprach sich, der Ausführer übernahm es (eurofleet-Notiz §8). |
| **P11-K** | **Probe-Instanz:** die vorhandene Unit `sharefyx-staging.service` als zweiter Dienst auf dieser VM. Eigener Port, eigener Datenordner (Kopie), eigene `auth.sqlite3`, nur im Tailnet (`tailscale serve`, **nie** Funnel). Kopiert wird nur in eine Richtung: echt → Kopie. **Kein Blue/Green-Umschalten.** | Lehre aus Deploy D: die Wegwerf-Saat hat nicht die Form echter Daten. Ein eigener Gast wäre ein zweiter Deploy-Weg und ein zweiter Schlüsselbund. P5-AB (kein Blue/Green) bleibt: zwei Farben auf derselben `auth.sqlite3` verlangen expand/contract. |
| **P11-L** | **Die Deploy-Logik bleibt im Repo** (`deploy.sh`, `rollback.sh`, `health_gate.sh`, je mit Tests). Eurofleet darf den **Aufruf** bündeln, ausgelöst vom Nikinger; Eurofleet baut nichts um. | Hard Rule 9; die Skripte sind getesteter Produktcode. |
| **P11-M** | **Ein Deploy für Block 1: `v4.1.0`.** Zwischenstände gehen nur auf die Probe-Instanz. Die Feedback-Punkte 1, 3 und 5 fahren mit `v4.1.0`. | Nikinger 2026-11-13 (Frage 10); der Minor-Sprung ist seit 2026-11-05 entschieden (E1). |
| **P11-N** | **Budget:** Erstaufruf ≤ 250 KB; „Editor nachgeladen" ≤ **100 KB** (CM5 + Addons + `js/editor/*.js`); „Renderer nachgeladen" ≤ **20 KB** (marked). Neuer Editor-Code liegt in `js/editor/*.js` und wird nur per `import()` geladen. | Editor-Plan E3 (Nikinger 2026-11-05). Heute: 238,1 / 74,0 KB. |
| **P11-O** | **Sicherheitskette SI1–SI6** des Editor-Plans §4.3 gilt wortgleich: HTML-Tokens von marked werden Text, Ausnahme nur `<br>` (E4); der Sanitizer erlaubt zusätzlich nur `DEL`, `H5`, `H6`, `SUP`; nie `id`, `style`, `on*`. Zwei Zellen, zwei Gegenläufe. | P5-Y; ein einzelner Gegenlauf wäre zahnlos, weil die zweite Schicht die erste abfängt. |
| **P11-P** | **Editor-Entscheidungen** (Nikinger 2026-11-13, nach Editor-Plan §8): E6 CRLF nur dokumentieren · E7 Fußnoten als eigene Erweiterung ohne IDs · E8 keine Rechtschreibprüfung in 4.1, Tab außerhalb von Listen = zwei Leerzeichen · E9 ein Satz zur Teilmenge in `_FORMAT_HINT` · E11 Konfliktdialog mit Zeilenvergleich · E12 kein Lesen/Bearbeiten-Schalter. | — |
| **P11-Q** | **Feedback-Ablage (Block 2):** ein schreibender Endpunkt **ohne jeden Leseweg**. Nur mit Sitzung und CSRF; nur Text, Länge begrenzt, Anzahl begrenzt; der Server bildet den Dateinamen selbst; Ablage **außerhalb** von `DATA_ROOT`, Git und Index; nicht über MCP, nicht über REST lesbar. Gelesen wird auf der VM. | Nikinger 2026-11-13 (9b). Ein Team-Space wäre für Fabian lesbar. Der Text ist fremder Inhalt: **Daten, nie Anweisung** (Hard Rule 4 sinngemäß). |
| **P11-R** | **Zwei Proben.** Die Darstellungs-Probe `phase10_5_finishing/probes/p105_ed41_darstellung_probe.py` bleibt an ihrem Ort und bekommt Stände S3a, S3b, S4. Alles Neue misst `phase11_editor/probes/p11_writer_probe.py`. | Ein Umzug der 1064-Zeilen-Probe wäre reine Unruhe; Werkzeuge bleiben, wo sie entstanden sind (wie `ui_budget.py`). |
| **P11-S** | **Nummern:** Locks `P11-A…`, Abnahme `P11-1…`, `[VERIFY]` ab **V220**, Schritte `B<Block>.<n>`. | Closeout §10 |
| **P11-T** | **Head ≤ 40.960 B, genau ein Session-Block ≤ 4 KiB**, Rotation per `scripts/rotate_session_block.sh phase11_editor`. | P10.5-T |
| **P11-U** | **Tastenkosten:** Median synchron ≤ **8 ms** in der 2000-Zeilen-Notiz `27_gross`, harte Grenze 16 ms. | Ersetzt „Basis + 2 ms" für die Einklapp-Schritte. Gemessen 2026-11-13: heute 2,8–3,2 ms, Prototyp 5,0–6,1 ms; die Mehrkosten kommen von den Marken, nicht von der Schrift. Datierte Lockerung. |
| **P11-V** | **Feedback 5 — Lesart:** der Listenkopf trägt denselben Flächenton wie die Fläche um ihn. Die Sichtung in B1.1 entscheidet; trifft die Lesart nicht, ist das ein Befund an den Nikinger, kein zweiter Versuch auf Verdacht. | Nikinger 2026-11-13: „weder noch, Hintergrundfarbe angleichen". Suchfeld und Auswahl tragen schon denselben Ton (gemessen). |
| **P11-W** | **Anker:** jede Edit-Stelle steht als wörtlicher String in `phase11_editor/anker.json`. Ein Wächter verlangt, dass jeder Anker eines **offenen** Schritts genau einmal vorkommt. Ändert ein Schritt den Anker eines späteren, zieht **er** die Datei nach. | Schritte verschieben einander die Zeilen; ein doppelter Anker beißt still nicht (Falle 18.2b). |

### §0.1 Was P11 ausdrücklich nicht tut

CodeMirror 6 · Rechtschreibprüfung · Formeln, verbundene Zellen, Spaltenbreiten · Editor-Farben Stufe 3 (freie Farben) ·
ein eigener Tabellen-Item-Typ (ED-4) · Handy-Oberfläche (UI-7) · verbundene AI-Sessions (LG-11) · CIMD (PA-4) ·
Eingriffe in `phase1_storage/storage/` (die Review-Befunde B11, B13, B19, B22 bleiben „später") · ein LLM im Server ·
Blue/Green-Umschalten · ein Leseweg für Feedback.

---

## §1 Zuschnitt

### §1.1 Vormerkungen aus dem Closeout §6

| # | Punkt | P11 | Begründung |
|---|---|---|---|
| 1 | Leitziel Writer-Optik | **in P11**, Block 1 | Kern der Phase; als messbare Zeilen plus Sichtung (P11-7–13, P11-26) |
| 2 | Editor 4.1 S3a–S11 | **in P11**, Block 1, neu geschnitten | S4 „Listenzeichen gedimmt" und der S5a-Gegenlauf sind durch P11-C überholt |
| 3 | Tabelle bleibt Tabelle | **in P11**, Block 1 (B1.9–B1.11) | als Raster nach P11-G |
| 4 | Feedback-Knopf | **in P11**, Block 2 | Ablage nach P11-Q |
| 5 | Zweite Instanz | **in P11**, Block 0 (B0.3) | vor dem ersten Editor-Deploy (P11-K) |
| 6 | Wiederkehrender Darstellungs-Check | **in P11**, Block 1 (B1.14) | die Probe existiert, die Verankerung fehlt |
| 7 | Editor-Farben Stufe 3 | später | erst nach der Writer-Optik |
| 8 | `ev=tool` ohne `client_id` | **in P11**, Block 3 | Logtext, kein Verhalten |
| 9 | Nur lesender Agenten-Zugang | später | Konto-Entscheidung des Nikingers, kein Code |
| 10 | Trading-VM-Anbindung | entfällt | seit 2026-11-08 verbunden (eurofleet-Notiz §5) |
| 11 | A1 `ausreisser` | entfällt | live nicht beobachtbar |
| 12 | Korpus-Lücke „Tabelle direkt unter Textzeile" | **in P11**, B1.0 | eine Fixture |
| 13 | Review-Rest B14, B16, B17, B21 | **in P11**, Block 3 | klein, außerhalb von `storage/` |
| 13 | Review-Rest B11, B13, B19, B22 | später | je eine angekündigte P1-Öffnung |
| 13 | Review-Rest B12 | **in P11**, Block 3, **nur messen** | bei 263 Items kein Schmerz |
| 14 | PA-4, ED-4, UI-7, LG-11 | später | je eine eigene Phase |
| 15 | Betrieb klein (Ollama-Kontext, `opencode run </dev/null`, Platte) | **in P11**, B0.1, nur Doku | Umsetzung bei Eurofleet (§5) |

### §1.2 Feedback des Nikingers (2026-11-12), an der Wegwerf-Instanz gemessen

| # | Punkt | Befund (gemessen 2026-11-12) | Schritt |
|---|---|---|---|
| F1 | Ladeansicht in Form der alten Notiz | `editor.js:939` legt `is-loading` über `#detail`; `app.css:3022 ff.` lässt den alten Inhalt sichtbar | B1.1 |
| F2 | zwei oder drei Farben im Editor | vier Flächentöne: `#1B2027`, `#14181D`, `#10151B`, `#0C1017` | B1.2 |
| F3 | „Alle Items", „Einstellungen", „Abmelden" fest | `.rail` scrollt als Ganzes (986 px Inhalt in 620 px) | B1.1 |
| F4 | vollständiger Umbau, danach Regeln | — | Block 1, Block 2 |
| F5 | Hintergrundfarbe angleichen | Lesart P11-V | B1.1 |

---

## §2 Arbeitsregeln für jeden Schritt

### §2.1 Ablauf einer Sitzung

1. `pwd` = Repo-Wurzel, `git status` sauber. Schrittbasis notieren: `git rev-parse --short HEAD`.
2. Lies den Session-Block im Head, dann deinen Schritt. Rufe `plan_anker.py <Schritt>` auf.
3. Baue den Schritt. Kein Schritt ist fertig ohne grünes `pytest`:
   `env $(env | grep -oE '^(SHAREFYX_|SFX_|SPACE_)[A-Z_]*' | sed 's/^/-u /') .venv/bin/python -m pytest -q -p no:cacheprovider`
   (bereinigte Umgebung — ein Testlauf mit geerbten Variablen hat den Produktionsdienst einmal 52-mal neu gestartet).
4. Am Schrittende: `scripts/doc_health.py` = 0 Treffer, `phase5_ui/scripts/ui_budget.py` alle Zeilen OK, die Proben des Schritts.
5. **Ein Commit je Schritt**, im selben Commit: Modulstatus und Abnahmestand im Head, neuer Session-Block (der alte rotiert per
   Skript), `anker.json` (Schritt auf `erledigt`), jede neue `.md` mit Header-Card und INDEX-Zeile.
   Betreff: `phase 11: B<n>.<m> -- <was>; pytest <zahl> gruen`. **Lies den Betreff einmal gegen.**
6. **Kein Push, kein Deploy, kein `systemctl`.** Push fragt der Nikinger frei; Deploy macht nur er (Hard Rule 9).

### §2.2 Wegwerf-Instanz und Proben

- Eigener Port, tmp-`DATA_ROOT`, tmp-`auth.sqlite3`, eigener DEK, TLS selbstsigniert, Umgebung ohne `SHAREFYX_*`/`SFX_*`/`SPACE_*`,
  Stopp **nur** über die PID-Datei. Die Mechanik steht fertig in `phase10_5_finishing/probes/p105_b14_layout_probe.py`
  (`_setup`, `_serve`, `_stop`, `_freier_port`, `_saubere_umgebung`); lade sie als Modul wie `p105_ed41_darstellung_probe.py:95–120`.
- Playwright aus `~/.claude-code-tools/e2e-venv` (Chromium 151, Firefox 153). Immer
  `add_init_script("localStorage.setItem('sfx:film:gesehen','4.0.0')")`, sonst frisst das Film-Startbild die Klicks.
- **Gegenläufe** patchen eine **Kopie** der statischen Dateien (Umgebungsvariable `ED41_STATIC_DIR`, Weiche in
  `p105_ed41_darstellung_probe.py:108–120`), nie den Arbeitsbaum. Jeder Patch-Anker kommt genau einmal vor.
- **Eine Prüfung, die nicht rot werden kann, zählt nicht.** Jeder Schritt nennt, wie man seine Zellen rot bekommt. Fällt ein
  Gegenlauf grün aus, ist er zahnlos: neu bauen, für die Szene von heute.
- Nie gegen den echten `DATA_ROOT`, die echte `auth.sqlite3`, den Keyring oder den laufenden Dienst.

### §2.3 Rückgabe-Auslöser (Stopp, Meldung im Session-Block)

1. Der Schritt braucht eine Datei außerhalb seiner erlaubten Pfade.
2. `git diff --stat <Schrittbasis>..HEAD -- phase1_storage/storage` ist nicht leer.
3. Ein Test außerhalb des Schritts wird rot und der Grund ist nicht offensichtlich der eigene Diff.
4. Ein `[VERIFY]` aus §6 fällt anders aus, als der Plan annimmt.
5. Der Plan widerspricht dem Code: der Code gewinnt; kleine Drift mit datierter Notiz fixen, große an den Nikinger.
6. Irgendetwas verlangt `sudo`, `systemctl`, den echten `DATA_ROOT`, den Keyring, das Netz oder Geld. *(2026-11-14: marked 18.1.3 und
   `searchcursor` 5.65.16 liegen im npm-Cache dieser VM — `npm pack … --offline` braucht kein Netz. Netz braucht nur der
   Glyphen-Teil von B1.13.)*
7. Drei erfolglose Anläufe am selben Fehler.
8. Der Kontext erreicht 150.000 Tokens und der Schritt ist nicht fertig: Schnitt, Übergabe, neue Sitzung.
9. Ein Bildurteil wäre nötig und du bist nicht Claude Code (P11-J).

### §2.4 Deploy-Ablauf (einmal für `v4.1.0`, später gleich)

| # | Schritt | Wer |
|---|---|---|
| D0 | Darstellungs-Probe und Writer-Probe an der Wegwerf-Instanz, beide Browser; Ergebnis-JSON im Release-Commit | Claude Code |
| D1 | Volle Suite grün, `doc_health` 0, `ui_budget` alle Zeilen OK | Claude Code |
| D2 | Badge `.rail__version` (`app.html:25`) · `docs/UPDATE_LOG.md`, oberste Überschrift = Deploy-Tag, deutsch, für Menschen | Claude Code |
| D3 | Commit, Push nach Freigabe | Claude Code |
| D4 | **Probe-Instanz zuerst:** die Befehle iii–v aus B0.3 — `deploy.sh main` mit den Variablen der Probe-Instanz und `SHAREFYX_ALLOW_STALE_UPDATELOG=1`, `health_gate.sh --port=8766 --current-link=/opt/sharefyx/staging` | **Nikinger** |
| D5 | Sichtung mit echten Notizen auf der Probe-Instanz (P11-26) | Nikinger + Claude Code |
| D6 | `deploy.sh main` produktiv; `health_gate.sh --expected-version=v4.1.0 --expected-sha=<sha>`, am Deploy-Tag mit `--require-todays-update-log`, sonst ohne (Gate-Datumsfalle) | **Nikinger** |
| D7 | Die echte Ausgabe von `health_gate.sh` in den Session-Block; bei Rot `rollback.sh` | Claude Code liest · **Nikinger** rollt |

---

## §3 Blockübersicht

| Block | Inhalt | Wer | Version | Detail |
|---|---|---|---|---|
| **0** | Haushalt (INDEX dauerhaft entlasten, Doku-Code-Durchgang), Baseline der Aufzeichnung, Probe-Instanz | Claude Code + Nikinger | — | Block-1-Datei, B0.1–B0.3 |
| **1** | Editor 4.1 „Writer-Optik": 17 Schritte B1.0–B1.16 | Claude Code + Ausführer | `v4.1.0` | Block-1-Datei |
| **2** | Oberfläche nach Regeln; Feedback-Knopf | offen | Entscheidung Nikinger | §3.1 |
| **3** | Review-Rest und Betrieb | Ausführer | mit Block 2 | §3.2 |
| **Z** | Closeout P11 (Handover, Grafik, Rotationen) | Claude Code + Nikinger | — | Prompt 3 |

### §3.1 Block 2 — Oberfläche nach Regeln, Feedback-Knopf (Ziel, Abnahme, Abhängigkeiten; noch keine Anker)

**Ziel.** Die ganze Oberfläche folgt einem geschriebenen, messbaren Regelwerk, und Rückmeldungen landen sicher auf der VM.
**Abhängigkeit:** Block 1 ist ausgeliefert (die Regeln messen den neuen Editor mit). **Vor dem Bau:** die Anker dieses
Blocks plant eine eigene kurze Planungssitzung gegen den Stand nach `v4.1.0`.

- **2.1 Regelwerk** `docs/concepts/ui_regeln.md` (neu), höchstens 15 Regeln, jede messbar: Textkontrast ≥ 4,5 : 1 · sichtbarer
  Fokus an jedem bedienbaren Element · Zielgröße ≥ 24 × 24 px · höchstens zwei Schriftfamilien · Abstände auf dem 8-px-Raster ·
  je Ebene ein Flächenton · jeder Zustand (Ruhe, Hover, Aktiv, Gesperrt, Fokus) unterscheidbar · alles per Tastatur erreichbar,
  Esc schließt die oberste Ebene · kein Ladezustand zeigt alten Inhalt · jede Fehlermeldung nennt, was zu tun ist.
- **2.2 Regel-Probe** `p11_regeln_probe.py`: misst jede Regel in fünf Ansichten (Übersicht, Liste, Editor, Lesesicht,
  Einstellungen), Basislinie rot, je Regel ein Gegenlauf.
- **2.3 Fixes** je Regel, bis die Probe grün ist; Bildurteil Claude Code, Sichtung Nikinger.
- **2.4 Feedback-Knopf** nach P11-Q: `POST /api/v1/feedback` in `phase5_ui/webui/api.py` (Sitzung + CSRF; Text ≤ 4.000 Zeichen;
  höchstens 10 je Stunde und Konto; Antwort 204 ohne Inhalt); Ablage als Datei mit Modus 0600 in einem Verzeichnis neben der
  `auth.sqlite3` (über `StateDirectory`), Dateiname `JJJJMMTT-HHMMSS-<zufall>.md`, Kopfzeilen Konto, Zeit, Version, Ansicht;
  kein `GET`, kein MCP-Werkzeug, nicht im Index, nicht im Daten-Git. Knopf in der Rail-Fußzeile, Dialog mit einem Textfeld.
  **Abnahme:** Schreibweg mit Gegenlauf (ohne CSRF 403, zu lang 422, elfte Meldung 429); **kein** Pfad liefert den Text zurück
  (Wächter über die Routenliste); Pfad-Traversal unmöglich, weil kein Nutzerwert in den Dateinamen fließt.

### §3.2 Block 3 — Review-Rest und Betrieb (Ziel, Abnahme, Abhängigkeiten; noch keine Anker)

**Abhängigkeit:** keine zu Block 1; kann parallel laufen, sobald ein Ausführer frei ist.

| Posten | Ziel | Abnahme |
|---|---|---|
| B14 | `search_items(offset<0)` klemmt auf 0 wie REST | Test: negativer Offset = Seite 1, `truncated` stimmt |
| B16 | der Editor bietet `archived` nicht mehr in der Status-Auswahl an | Probe-Zelle; Gegenlauf macht sie rot |
| B17 | eine Versionsquelle: `/health` meldet die Version der Oberfläche | `health_gate` liest `/health` statt der HTML-Zeichenkette |
| B21 | unauthentifizierte Authorize-Aufrufe erzeugen höchstens N offene Zeilen je Client | Test mit N+1 Aufrufen |
| `ev=tool` | die Tool-Logzeile trägt die `client_id` | Test auf die Logzeile |
| B12 | **nur Messung:** Such- und Listenzeit bei 263, 1.000 und 5.000 Items | Zahlen im Head; Umbau nur auf Entscheidung |

---

## §4 Abnahme

**Zählregel:** ✅ erfüllt mit Beleg am Ort · ⚠️ erfüllt in anderer Form, Abweichung benannt · ⬜ offen. Jede Zeile gilt erst mit
ihrem Gegenlauf. Gezählt wird im Head. Sichtbare Eigenschaften, die der Nikinger erwartet, sind Zeilen — das Leitziel steht
diesmal in der Tabelle (P11-7 bis P11-13 und P11-26).

| # | Kriterium | Beleg | Schritt |
|---|---|---|---|
| P11-1 | Die INDEX-Karte hat dauerhaft ≥ 8.000 B Luft; jede `.md` hat eine Zeile in einer der beiden Karten; `doc_health` 0 | Wächter + `doc_health` | B0.1 |
| P11-2 | Baseline der Aufzeichnung steht mit Zahlen und Commit im Head | Head | B0.2 |
| P11-3 | Die Probe-Instanz läuft mit einer Kopie der Daten, ist nur im Tailnet erreichbar und nicht über den Funnel | Nikinger, Ausgabe im Head | B0.3 |
| P11-4 | Eine Wahrheit: Lesesicht, Update-Log und Tabellen-Widget aus derselben Fassade; GFM-Teilmenge ≥ 95 % | Darstellungs-Probe S3b | B1.4 |
| P11-5 | Sicherheit zweischichtig: `html_als_text` und `keine_aktiven`, je eigener Gegenlauf | Probe + pytest | B1.3 |
| P11-6 | Editor-Modus: keine Widersprüche F4a–f; jede Tokenfarbe ≥ 4,5 : 1 | Darstellungs-Probe S4 | B1.5 |
| P11-7 | Schrift: Fließtext im Editor Plex Sans 16 px, Code Plex Mono 13 px, Überschriften 22/18/16 px, gleich der Lesesicht | Zelle `schrift` | B1.2 |
| P11-8 | Kein Markdown-Zeichen sichtbar außerhalb des Elements unter dem Cursor; die linke Kante einer Überschrift = linke Kante des Absatzes (± 1 px) | Zellen `marker_eingeklappt`, `kante` | B1.6, B1.7 |
| P11-9 | Sichtbarer Editor-Text = Text der Lesesicht, je Korpus-Datei (Ausnahmen namentlich) | Zelle `gleichtext` | B1.7 |
| P11-10 | Klickgenauigkeit 100 % bei ≥ 30 Zielen; Doppelklick, Dreifachklick, Ziehen — beide Browser | Zellen `klick30`, `doppelklick`, `dreifachklick`, `ziehen` | B1.6 |
| P11-11 | Tastatur an Elementgrenzen; nach 20 × Undo/Redo Bytes gleich und Marken = Wunschliste | Zellen `grenzen`, `undo20` | B1.6 |
| P11-12 | Tastenkosten nach P11-U | Zelle `tastenkosten` | B1.6, B1.7 |
| P11-13 | Aufgabe = Kästchen-Element; Liste = Punkt oder Nummer; jede Ebene sichtbar eingerückt (≥ 16 px je Ebene) | Zellen `kaestchen`, `listenpunkt`, `ebenen` | B1.7 |
| P11-14 | Listen und Tasten: Enter setzt fort, leerer Punkt beendet, Tab stuft, Rücktaste am Inhaltsanfang entfernt das Zeichen, Strg+B/I/K | Zellen `liste_*`, `taste_*` | B1.8 |
| P11-15 | Raster: Zelle wählen, Pfeile, Tippen, F2, Enter, Tab, Esc, Entf, Undo; nur die Zelle ändert Bytes | Zellen `raster_*`, `bytes_zelle` | B1.9 |
| P11-16 | Raster: Zeile und Spalte einfügen und löschen, Ausrichtung, Tabelle einfügen; Body-Diff = erwartete Zeilen | Zellen `raster_op_*` | B1.10 |
| P11-17 | Raster: Bereich wählen, Kopieren als TSV, Einfügen von TSV und HTML-Tabellen (nur Text) | Zellen `raster_ablage_*` | B1.11 |
| P11-18 | Eine Tabelle ist nie breiter als ihr Container; breite Tabellen scrollen im Widget | Zelle `tabelle_breite` | B1.2 |
| P11-19 | Suchen und Ersetzen im Editor: findet Zeile 1500 von 2000; „alle ersetzen" ist ein Undo-Schritt | Zellen `suche_*` | B1.12 |
| P11-20 | Beim Wechsel der Notiz ist nach 200 ms nichts von der alten Notiz sichtbar; unter 200 ms kein Flackern | Zelle `ladeansicht` | B1.1 |
| P11-21 | „Alle Items", „Einstellungen", „Abmelden" bleiben bei 620 px Höhe und überlaufendem Baum im Bild | Zelle `rail_fest` | B1.1 |
| P11-22 | Editor: genau zwei Flächentöne (Leisten, Schreibfläche); Listenkopf nach P11-V | Zellen `flaechen`, `listenkopf` + Bild | B1.1, B1.2 |
| P11-23 | Byte-Vertrag V1–V8 auf dem Korpus, beide Browser | beide Proben | B1.14 |
| P11-24 | Budget nach P11-N; jede Datei gezählt; kein statischer Import aus `js/editor/` | `ui_budget.py` + Wächter | B1.3 |
| P11-25 | Darstellungs-Gate: jede Zelle hat einen Gegenlauf, der genau sie rot macht; der Ablauf §2.4 steht im Head | Lauf + Wächter | B1.14 |
| P11-26 | **Sichtung mit echten Notizen** auf der Probe-Instanz: ≥ 5 Notizen, darunter die größte (1836 Zeilen), eine mit breiter Tabelle, eine Aufgabenliste | Nikinger | B1.15 |
| P11-27 | Live `v4.1.0`: Deploy, `health_gate` mit echter Ausgabe, Sichtung | Nikinger | B1.16 |
| P11-28 | Komfort (Gliederung, Zählung, Strg+Klick, Konflikt-Zeilenvergleich) und Glyphen `→ ✓ ≤` aus Plex — **streichbar** | Zellen `gliederung`, `link_folgen_fragt`, `glyphen` | B1.13 |
| P11-29 | Regelwerk steht; die Regel-Probe ist in fünf Ansichten grün, je Regel ein Gegenlauf | Probe | Block 2 |
| P11-30 | Feedback-Ablage nach P11-Q: Schreibweg mit drei Gegenläufen; kein Leseweg | pytest + Wächter | Block 2 |
| P11-31 | B14, B16, B17, B21 und `ev=tool` nach §3.2 | pytest, Probe | Block 3 |
| P11-32 | B12 gemessen (drei Größen), Zahlen im Head | Messung | Block 3 |
| P11-33 | Jeder Ausführer-Commit trägt den Modell-Trailer; je Sitzung Wanduhr, Kontingent, Eingriffe im Session-Block | `git log`, Archiv | laufend |
| P11-34 | Closeout: Handover, Grafik, Rotationen, formaler Schluss | Dokumente | Z |

---

## §5 Bedarf an Eurofleet

| # | Bedarf | Bis wann | Bemerkung |
|---|---|---|---|
| 1 | **Probe-Instanz erreichbar machen:** ein `tailscale serve`-Eintrag für ihren Port, nur im Tailnet, nie Funnel | vor B1.15, besser mit B0.3 | die Unit ist installiert und abgeschaltet; einschalten und Konto anlegen macht der Nikinger |
| 2 | **Ausführer-Anbindung:** Kontextgrenze ≤ 200.000 für die beiden MiniMax-Modelle in opencode auf dieser VM; Rückmeldung des wirksamen Werts | vor B1.3 | die opencode-Konfiguration ändert nur Eurofleet |
| 3 | **Kontingent-Auskunft:** reicht „M Plan Go" neben dem Messlauf des Trading-Bots für etwa eine Sharefyx-Sitzung am Tag? | vor B1.3 | sonst baut Claude Code die E-Schritte (P11-I) |
| 4 | **Platz:** die Datenkopie braucht 14 MB (gemessen 2026-11-13); je Release ≈ 310 MB mit eigenem venv, die Probe-Instanz behält bis zu fünf (≈ 1,6 GB, gemessen 2026-11-14); `/tmp/opencode` regelmäßig räumen | laufend | 25 GB frei am 2026-11-12 und 2026-11-14 |
| 5 | **Wächter (optional):** die Probe-Instanz in die Überwachung aufnehmen; Alarm, falls ihr Port je über den Funnel erreichbar wird | nach B0.3 | V203 (Funnel-Wächter) ist weiter offen |
| 6 | **Deploy-Bündel (optional, P11-L):** ein Aufruf, der `deploy.sh` und `health_gate.sh` in fester Reihenfolge startet, ausgelöst vom Nikinger | vor B1.16 | keine eigene Logik |
| 7 | **Harness-Bewertung:** P11 liefert Trailer und Kontingent je Sitzung; B1.3 eignet sich als „schon gelaufener Code-Block" | nach B1.3 | eurofleet-Notiz §8 |
| 8 | **WebKit-Systembibliotheken (optional):** damit Safari messbar wird (Liste im Editor-Plan §9, V-E1) | vor B1.14 | braucht `sudo` |

---

## §6 Bei Ausführung verifizieren (vollständig — was hier nicht steht, gilt als geprüft)

| V | Was | Wann | Annahme des Plans |
|---|---|---|---|
| V220 | marked: Sicherheitshinweise und Änderungen zwischen 18.1.3 und 18.2.0 (neueste Version am 2026-11-13) | B1.3 | es bleibt bei 18.1.3; ein Sicherheitsfix in 18.2.0 ist eine Entscheidung des Nikingers |
| V221 | CodeMirror 5: Änderungen 5.65.16 → 5.65.21 an `markText`/eingeklappten Bereichen | B1.6 | kein Sprung geplant |
| V222 | marked unter der App-CSP (`script-src 'self'`): lädt `import()` das ESM im echten Seitenkontext? | B1.3 | ja (gemessen nur ohne CSP, V-E4) |
| V223 | Eingabemethoden (IME) und Rechtschreib-Unterstreichung an eingeklappten Bereichen | B1.15 | kopflos nicht messbar; Sichtung |
| V224 | Safari/WebKit | B1.14 | nicht gemessen, solange Bedarf 8 offen ist |
| V225 | Rollbalken und Sprungziele in langen Notizen mit Proportionalschrift (CM5 schätzt Zeilenhöhen aus der Zeichenzahl) | B1.2, B1.7 | Sprung auf Zeile 1500 landet ± eine Zeile |
| V226 | `tailscale serve` für die Probe-Instanz neben dem Funnel der Produktion auf demselben Knoten (geerbt: V36) | B0.3 | geht mit eigenem Port |
| V227 | Die Staging-Unit lädt denselben verschlüsselten DEK wie die Produktion bei eigener `auth.sqlite3` — **Fakt** (dieselbe Datei `/etc/sharefyx/auth-dek.cred`, gelesen 2026-11-14); offen ist nur, ob das gewollt ist | B0.3 | unkritisch; der Nikinger entscheidet |
| V228 | ✅ 2026-11-14: die installierte Staging-Unit läuft aus `/opt/sharefyx/current`; `deploy.sh` kennt `SHAREFYX_CURRENT_LINK`, `SHAREFYX_SERVICE`, `SHAREFYX_PORT` — eigener Symlink, Befehle in B0.3 | — | — |
| V229 | Form echter Daten: die größte Notiz (1836 Zeilen), Fabians Tabellen, `<br>` in Zellen | B1.15 | Korpus deckt sie |
| V230 | Browser-Hit-Test in Firefox: `caretRangeFromPoint` fehlt oder weicht ab, dann `caretPositionFromPoint` | B1.0 | Probe braucht beide Wege |
| V231 | Feedback 5: trifft die Lesart P11-V? | B1.1 | Sichtung |
| V232 | Icons „durchgestrichen" und „Aufgabe" im Sprite (`build_icon_sprite.py`) | B1.8 | fehlen heute |
| V233 | Wirksame Kontextgrenze des Ausführers in opencode | vor jedem E-Schritt | ≤ 200.000 (Bedarf 2) |
| V234 | ✅ 2026-11-14: `searchcursor.js` unminifiziert aus dem npm-Cache, SHA-256 in B1.12; `continuelist` wird nicht vendort (B1.8 baut die Listenregeln selbst) | — | — |
| V235 | Kosten der Marken: lässt sich der synchrone Anteil unter 8 ms halten, wenn Kästchen, Punkte und Inline-Marken in einem Zeilenbauer liegen? | B1.7 | ja (Prototyp 5–6 ms ohne Zusammenlegung) |
| V-E1–V-E14 | die Liste des Editor-Plans §9 — außer V-E9 (✅ 2026-11-14: `fontTools` und `brotli` liegen in `~/.claude-code-tools/film-venv`) | wie dort | unverändert geerbt |

---

## §7 Fehlbilder: Symptom → erster Verdächtiger

| Symptom | Erster Verdächtiger |
|---|---|
| Klicks der Probe tun nichts | Film-Startbild: `sfx:film:gesehen` nicht gesetzt |
| Zweiter Login der Probe gibt 401 | TOTP-Schritt verbraucht: `totp_zuruecksetzen()` aus `p105_b14_layout_probe.py` |
| Probe meldet „Klick daneben" bei fast allen Zielen | das Messgerät: Koordinaten vor einem Scroll gemessen (so geschehen am 2026-11-12) — nach jedem Rücksetzen neu messen |
| Hit-Test liefert in Firefox `null` | `caretRangeFromPoint` (V230) |
| Eine CSS-Regel greift nicht | das vendorte `codemirror.min.css` (wird **vor** `app.css` eingefügt) oder `.cm-s-default`; Spezifität prüfen, nicht `!important` |
| `<style>` oder `style=` wirkt nicht, ohne Fehlermeldung | CSP `style-src 'self'`: nur Klassen oder CSSOM aus JS |
| Die ganze Seite rutscht, unten ein schwarzer Balken | DOM-`scrollIntoView` auf einem Widget statt `cm.scrollIntoView` |
| Doppelklick markiert in Firefox nichts | Mausregel fehlt oder greift nicht (P11-D) |
| Ein Zeichen fehlt im sichtbaren Text | unpaariger Marker eingeklappt (P11-D) oder Zellgrenze an `\\|` |
| Marken verdoppeln sich nach Undo | Buchführung über eine eigene Liste statt `cm.findMarks` |
| Endlosschleife, Browser hängt | Abgleich hängt an „update" oder baut ohne Signaturvergleich neu |
| Das Tabellen-Widget verschwindet nach einem Zell-Edit | der `change`-Zuhörer in `tabellen.js` räumt jede Änderung im Bereich; Ursprung `+sfxzelle` ausnehmen |
| `[Text]{.rot}` zeigt wieder Klammern | die Format-Zeichen kommen nur aus dem Overlay, nicht aus `getLineTokens` |
| `import()` liefert 404 nur im Gegenlauf | die Kopie der statischen Dateien ist älter als der Arbeitsbaum |
| `test_index_lines_clean` rot | eine neue `.md` ohne Zeile in der Karte |
| `test_table_shape` rot („Kopf 3 vs. Zeile 5") | ein `\|` in einem Code-Span einer Tabellenzeile teilt die Zelle trotzdem: als `\|` schreiben (so geschehen 2026-11-14) |
| Budget-Wächter rot ohne Größenänderung | neue Datei unter `static/` in keiner Liste von `static_payload_files()` |
| Anker-Wächter rot | ein früherer Schritt hat den String geändert: `anker.json` nachziehen, kein Fehler deines Schritts |
| `health_gate` 8/9 am Tag nach dem Deploy | `--require-todays-update-log` (Datumsfalle) |
| `deploy.sh` bricht am Update-Log ab | die oberste `##`-Überschrift trägt nicht den Deploy-Tag |
| `rotate_session_block.sh`: `ABBRUCH: Archiv fehlt` | `phase11_editor/SESSIONS_ARCHIVE.md` gibt es erst ab B0.1 Nr. 9 |
| Deploy auf die **Probe-Instanz** bricht am Update-Log ab | `SHAREFYX_ALLOW_STALE_UPDATELOG=1` fehlt (nur dort; B0.3 iv) |
| `health_gate` gegen Port 8766 grün, aber SHA der Produktion | `--current-link=/opt/sharefyx/staging` fehlt: das Skript prüft sonst `/opt/sharefyx/current` |
| `health_gate` Gate 5 rot: `.rail__version ist 'v4.…', erwartet 'v3.0.1'` | `--expected-version` fehlt; die Vorgabe in `health_gate.sh:29` ist veraltet (B17) |
| Probe-Instanz zeigt nach der Kopie alte Listen | kein Neustart nach der Kopie, oder `--delete-excluded` fehlt (alter Index) |
| Ab einer Zeile fehlen alle Marken; Konsole: `partially overlapping` | zwei eingeklappte Bereiche überlappen teilweise — CM5 wirft; Wunschbereiche vorher vereinigen (B1.6) |
| Ein Strg+Z macht zwei Zell-Edits rückgängig | gleicher `+`-Ursprung binnen 1250 ms verschmilzt: `cm.changeGeneration(true)` vor dem Schreiben (B1.9) |
| Esc in einer Zelle schließt die ganze Notiz | `stopPropagation()` fehlt; die Esc-Kette in `app.js:317 ff.` greift |
| Klick auf einen Link in einer Zelle öffnet eine andere Notiz ohne Rückfrage | `click`-Zuhörer an der Hülle fehlt; `app.js:135 ff.` ruft `selectItem()` direkt |
| Tabellen-Widget fehlt nach B1.3, ohne Fehlermeldung | `tabellen.js:175` `slice(-8)` gegen marked-Ausgabe mit `\n` am Ende: vorher `trim()` |

---

## §8 Ausgangslage (gemessen, `main@1128fdb`)

| Messung | Wert | Datum |
|---|---|---|
| `pytest` | 1938 grün · 1 rot von 1939 (461,9 s); rot nur `test_index_lines_clean` wegen der damals unversionierten eurofleet-Notiz | 2026-11-12 |
| `pytest` mit den P11-Dateien (Arbeitsbaum vor dem Plan-Commit) | 1965 grün, 0 rot (486,4 s) · `doc_health` 0 · 89 Anker je genau einmal (nach dem Abschluss-Durchgang: 111) | 2026-11-14 |
| `doc_health` | 1 Treffer (dieselbe Datei) | 2026-11-12 |
| `ui_budget` | 6/6: Erstaufruf 238,1 von 250 KB · Editor nachgeladen 74,0 von 80 KB · bis interaktiv 253,2 von 400 KB | 2026-11-12 |
| Darstellungs-Probe | Chromium 151 und Firefox 153 je 26 rot von 62 Zellen, 0 Abweichungen vom Stand S2 | 2026-11-12 |
| Klickgenauigkeit heute | 18/18 | 2026-11-13 |
| Tastenkosten heute, `27_gross` | 2,8–3,2 ms synchron | 2026-11-13 |
| Prototyp Einklappen | Klick 19/19 · Bytes gleich · 0 Seitenfehler · 5,0–6,1 ms · Mausregel nötig (Firefox) | 2026-11-13 |
| Machbarkeit Raster | beide Browser: wählen, Pfeile, tippen, Tab, F2, Esc, `\\|`, 2 × Undo = Bytes gleich, nicht geändert | 2026-11-13 |
| marked 18.1.3 | `lib/marked.esm.js` 49.668 B, 14.934 B gzip, SHA-256 `e76f3b37046a5d294159872002e5f6fcda8ed232e1be45ff76b3863f2919dae3`, MIT | 2026-11-13 |
| Probe-Instanz | `sharefyx-staging.service` installiert, `disabled`, `inactive`; Port 8766; läuft aus `/opt/sharefyx/current` | 2026-11-12 |
| VM | 4 Kerne · 5,8 GiB RAM, 2,1 GiB verfügbar · 25 GB frei · echte Daten 14 MB | 2026-11-12/13 |

Die Prototypen liegen nicht im Repo. Ihre Regeln stehen in P11-C, P11-D, P11-G und in den Schritten B1.6, B1.7, B1.9.
