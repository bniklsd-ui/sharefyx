---
status: live
purpose: Phase-11-Head — Modulstatus der Schritte B0.1–B1.16 und der Blöcke 2, 3, Z; Abnahmestand P11-1–34; offene Punkte beim Nikinger und bei Eurofleet; die Startaufträge im Wortlaut; genau ein Session-Block. Der Plan steht in zwei Dateien unter docs/concepts/.
read-when: Arbeiten in phase11_editor/ — zuerst lesen, zusammen mit dem Session-Block unten
detail: L2
up: ../ROADMAP.md
down:
  - ../docs/concepts/phase11_editor_plan.md          # 📕 Rahmen: Locks P11-A–W, Arbeitsregeln, Abnahme, [VERIFY], Bedarf an Eurofleet, Fehlbilder
  - ../docs/concepts/phase11_editor_plan_block1.md   # 📕 Block 0 + Block 1: Schritte, Anker, Tests, Startaufträge
  - anker.json                                       # die Anker des Plans, maschinenlesbar (P11-W)
  - ../docs/concepts/PHASE10_5_CLOSEOUT_HANDOVER.md  # 📕 Einstieg, Vormerkungen
  - ../docs/concepts/phase10_5_editor_4_1_plan.md    # 📗 Befunde F1–F14, Verträge §4
updated: 2026-11-14 (Entscheidungen des Nikingers nachgetragen; Feedback 5 am Bild bestätigt, drei alte Branches gelöscht, drei freigegeben) | 2026-11-14 (Abschluss-Durchgang vor dem ersten Commit: 111 Anker, B0.3-Befehle korrigiert, neue Fallen in B1.3/B1.6/B1.9/B1.12–B1.16) | 2026-11-13 (angelegt — Planungssitzung P11: Plan in zwei Dateien, 89 Anker geprüft, nichts am Produkt gebaut)
---
# Phase 11 — Editor in Writer-Optik

> **Auftrag:** der Editor sieht aus wie ein Word- oder Writer-Dokument, die Datei bleibt Markdown. Tabellen bearbeitet man
> wie in Excel. Danach folgt die Oberfläche festen Regeln. Block 1 wird als **`v4.1.0`** ausgeliefert; Zwischenstände gehen
> nur auf die Probe-Instanz. **Stand: geplant, nichts gebaut.**

## Modulstatus

| Schritt | Inhalt | Wer | Status |
|---|---|---|---|
| B0.1 | Haushalt: INDEX teilen, Doku-Code-Durchgang | Claude Code | ⬜ |
| B0.2 | Baseline der Aufzeichnung | Claude Code | ⬜ |
| B0.3 | Probe-Instanz (zweiter Dienst auf dieser VM) | Claude Code + Nikinger | ⬜ |
| B1.0 | Probe-Fundament, kein Produktcode | Claude Code | ⬜ |
| B1.1 | Oberfläche: Ladeansicht, Rail, Listenkopf 🖼 | Claude Code | ⬜ |
| B1.2 | Typografie und Flächen 🖼 | Claude Code | ⬜ |
| B1.3 | Renderer-Fassade und Sicherheit (marked 18.1.3) | Ausführer | ⬜ |
| B1.4 | Erweiterungen und Konformität | Ausführer | ⬜ |
| B1.5 | Editor-Modus = Wahrheit | Ausführer | ⬜ |
| B1.6 | Einklappen I: Inline | Claude Code | ⬜ |
| B1.7 | Einklappen II: Blockmarker, Listen, Kästchen 🖼 | Claude Code | ⬜ |
| B1.8 | Listen und Tasten | Ausführer | ⬜ |
| B1.9 | Raster I: Zelle wählen und bearbeiten 🖼 | Claude Code | ⬜ |
| B1.10 | Raster II: Struktur | Ausführer | ⬜ |
| B1.11 | Raster III: Bereich und Zwischenablage | Ausführer | ⬜ |
| B1.12 | Suchen und Ersetzen | Ausführer | ⬜ |
| B1.13 | Komfort und Glyphen (streichbar) | Ausführer | ⬜ |
| B1.14 | Darstellungs-Gate | Claude Code | ⬜ |
| B1.15 | Sichtung auf der Probe-Instanz, echte Daten 🖼 📊 | Claude Code + Nikinger | ⬜ |
| B1.16 | Release `v4.1.0` | Claude Code + Nikinger | ⬜ |
| Block 2 | Oberfläche nach Regeln; Feedback-Knopf | offen | ⬜ (Anker plant eine eigene Sitzung nach `v4.1.0`) |
| Block 3 | Review-Rest (B14, B16, B17, B21, `ev=tool`), B12 messen | Ausführer | ⬜ |
| Z | Closeout P11 | Claude Code + Nikinger | ⬜ |

🖼 = Bildurteil nur durch Claude Code oder den Nikinger · 📊 = hängt an der Form echter Daten.

## Deploy-Tabelle

| # | Version | SHA | `health_gate` | Ausgabe |
|---|---|---|---|---|
| — | `v4.0.2` | `d2ca573` | 8/9 am Folgetag (Datumsartefakt) | live seit 2026-11-06; ein Lauf ohne `--require-todays-update-log` steht aus |
| G | `v4.1.0` | — | — | nach B1.15; Ablauf Plan §2.4, die Probe-Instanz zuerst |

## Abnahmestand

**34 Zeilen** (P11-1–34), Kriterien wortgleich im Plan §4. Zählregel: ✅ erfüllt mit Beleg · ⚠️ erfüllt in anderer Form ·
⬜ offen. **Summe: 0 ✅ · 0 ⚠️ · 34 ⬜ (von 34).**

| # | Kurz | Stand | # | Kurz | Stand |
|---|---|---|---|---|---|
| 1 | INDEX dauerhaft entlastet | ⬜ | 18 | Tabelle nie breiter als der Container | ⬜ |
| 2 | Baseline im Head | ⬜ | 19 | Suchen und Ersetzen | ⬜ |
| 3 | Probe-Instanz läuft | ⬜ | 20 | Ladeansicht ohne alte Notiz | ⬜ |
| 4 | Eine Wahrheit, GFM ≥ 95 % | ⬜ | 21 | Rail-Fußzeile fest | ⬜ |
| 5 | Sicherheit zweischichtig | ⬜ | 22 | Zwei Flächentöne; Listenkopf | ⬜ |
| 6 | Editor-Modus ohne Widersprüche | ⬜ | 23 | Byte-Vertrag V1–V8 | ⬜ |
| 7 | Schrift wie die Lesesicht | ⬜ | 24 | Budget, drei Korridore | ⬜ |
| 8 | Keine Zeichen außerhalb des Cursor-Elements | ⬜ | 25 | Darstellungs-Gate | ⬜ |
| 9 | Editor-Text = Lesesicht-Text | ⬜ | 26 | **Sichtung mit echten Notizen** | ⬜ |
| 10 | Klick 100 %, Doppelklick, Ziehen | ⬜ | 27 | Live `v4.1.0` | ⬜ |
| 11 | Grenzen, 20 × Undo/Redo | ⬜ | 28 | Komfort und Glyphen (streichbar) | ⬜ |
| 12 | Tastenkosten ≤ 8 ms | ⬜ | 29 | Regelwerk und Regel-Probe | ⬜ |
| 13 | Kästchen, Punkt, Ebenen | ⬜ | 30 | Feedback-Ablage ohne Leseweg | ⬜ |
| 14 | Listen und Tasten | ⬜ | 31 | Review-Rest | ⬜ |
| 15 | Raster: Zelle | ⬜ | 32 | B12 gemessen | ⬜ |
| 16 | Raster: Struktur | ⬜ | 33 | Trailer und Ausführer-Daten | ⬜ |
| 17 | Raster: Bereich, Zwischenablage | ⬜ | 34 | Closeout | ⬜ |

## Offen beim Nikinger

- **Bedarf an Eurofleet weiterreichen** (Plan §5; zuerst Kontextgrenze und Kontingent vor B1.3, `tailscale serve` mit B0.3): `tailscale serve` für die Probe-Instanz · Kontextgrenze ≤ 200.000 für die MiniMax-Modelle · Kontingent-Auskunft · optional Wächter, Deploy-Bündel, WebKit-Bibliotheken.
- **B0.3: sieben Befehle, zwei davon mit `sudo`** (Unit-Filter, Deploy auf die Probe-Instanz) — B0.3 schreibt sie hierher, Reihenfolge im Plan. Kosten: keine. Die Produktion bleibt unberührt (Unit-Filter, PID-Vergleich vorher/nachher).
- **Drei Branches löschen** (freigegeben 2026-11-14, vom Auto-Modus für Claude Code blockiert): `git branch -D hotfix-b1 deploy-version-marker-only` · `git push origin --delete nikinger_claude/elegant-volta-gnyarh`.
- **Aus dem Closeout offen:** `health_gate` für `v4.0.2` ohne `--require-todays-update-log` · die Termine BT-5, AL-1 Zeile 15, AL-2/AL-6, AL-4, V203 (Handover §8 Nr. 10).
- **Später zu entscheiden:** Version für Block 2/3 · marked 18.2.0 nur bei Sicherheitsfix (V220) · die vier Storage-Befunde B11, B13, B19, B22.

## Offen bei Eurofleet

Die acht Bedarfe mit Termin stehen im Plan §5. Dazu aus dem Closeout §6 Nr. 15, nur zur Kenntnis: Ollama braucht ein
abgeleitetes Modell mit `num_ctx 16384` · `opencode run` liest stdin (`</dev/null`) · `/tmp/opencode` regelmäßig räumen.

## Startaufträge

**Rahmen (vor jeden Schritt-Auftrag setzen, `<Schritt>` ersetzen):**

> Du arbeitest im Repo `savefxy` an **Phase 11, Schritt `<Schritt>`**. Lies in dieser Reihenfolge: den Session-Block in
> `phase11_editor/CLAUDE.md`; `docs/concepts/phase11_editor_plan.md` §0, §2 und §7 ganz; in
> `docs/concepts/phase11_editor_plan_block1.md` **nur** den Abschnitt `## <Schritt>`. Begrenze jede Shell-Ausgabe mit
> `| cut -c1-240`. Rufe zuerst `.venv/bin/python phase11_editor/scripts/plan_anker.py <Schritt>` auf. Baue **genau diesen
> Schritt** in **einer** Sitzung (Kontext höchstens 200.000 Tokens; bei 150.000 ohne Abschluss: Schnitt und Übergabe).
> Tests nur mit bereinigter Umgebung (§2.1 Nr. 3). Nur Wegwerf-Instanzen, Stopp über die PID-Datei; kein `sudo`, kein
> `systemctl`, kein Push, kein Deploy. Ein Commit am Ende nach §2.1 Nr. 5, mit deinem Modell-Trailer. Bei einem Auslöser aus
> §2.3: Stopp und Meldung im Session-Block. Der Schritt-Auftrag folgt.

**Schritt-Aufträge** (wortgleich im Plan, je am Ende des Schritts):

- **B0.1:** Teile die Doku-Karte in `docs/INDEX.md` und `docs/INDEX_ABGESCHLOSSEN.md`, lehre `doc_health.py` beide Dateien, baue den Wächter mit Gegenproben, zieh E6 als Kommentar nach und leg `phase11_editor/SESSIONS_ARCHIVE.md` an, bevor du den Planungsblock rotierst. Fertig, wenn `docs/INDEX.md` ≤ 32.960 B ist, `doc_health` 0 meldet und die volle Suite grün ist.
- **B0.2:** Miss die Baseline nach B0.1 (Suite, `doc_health`, `ui_budget`, Darstellungs-Probe beide Browser) und trag Zahlen und SHA in den Head ein. Jede Abweichung vom Rahmen §8 ist ein Befund.
- **B0.3:** Baue das Kopierskript mit seinen drei Abbrüchen, die zwei Staging-Platzhalter und den Unit-Filter in `install_units.sh` samt Tests. Schreib die sieben Befehle für den Nikinger in der Reihenfolge des Plans vollständig in den Head. Führe selbst nichts aus, was `sudo` braucht.
- **B1.0:** Baue Korpus, Spec und Writer-Probe nach den verbindlichen Messmethoden; kein Produktcode. Fertig, wenn die Probe in Chromium und Firefox läuft, die Basislinie mit der Spec übereinstimmt (0 Abweichungen) und der Selbsttest genau eine Zelle kippt.
- **B1.1:** Baue die drei Oberflächen-Punkte: neutrale Ladeansicht beim Notizwechsel, feste Rail-Fußzeile mit „Alle Items", Listenkopf im Ton seiner Fläche. Fertig, wenn `ladeansicht`, `rail_fest`, `listenkopf` in beiden Browsern grün sind, jeder der drei Gegenläufe genau seine Zelle kippt und drei Vorher/Nachher-Bilder im Session-Block genannt sind.
- **B1.2:** Stell den Editor auf das typografische System der Lesesicht (Plex Sans 16 px, Überschriften 22/18/16, Code Mono), gib Editor und Lesesicht eine gemeinsame Lesebreite, reduziere die Editor-Flächen auf zwei Töne und räum die toten Teile ab. Fertig, wenn `schrift`, `flaechen`, `tabelle_breite` grün sind, `klick30` 100 % bleibt und die Bilder im Session-Block stehen.
- **B1.3:** Vendore marked 18.1.3 (SHA-256 im Plan), bau `js/markdown.js` zur Fassade um (`ensureRenderer`, `markdownToHtml`, `blockRanges`), ersetze das Vor-Escapen durch den HTML-Token-Override (SI1) und erweitere den Sanitizer (SI2), teile das Budget in drei Korridore. Fertig, wenn die Darstellungs-Probe im Stand S3a `html_als_text` und `keine_aktiven` grün zeigt, beide Gegenläufe genau ihre Zelle kippen und `ui_budget` alle Zeilen OK meldet.
- **B1.4:** Bau die marked-Erweiterungen (Format inline und Block, Fußnoten ohne IDs) und die Overrides, stell das Tabellen-Widget auf `blockRanges` der Fassade um, extrahiere die GFM-Beispiele einmal als Fixture und ergänze den einen Satz in `_FORMAT_HINT`. Fertig, wenn im Stand S3b `konformitaet` ≥ 95 % ist, alle `l_*`-Zellen grün sind und die drei Gegenläufe genau ihre Zellen kippen.
- **B1.5:** Stell den CM5-Modus auf GFM (durchgestrichen, Aufgaben, kein xml), gib dem Editor ein eigenes Theme mit Kontrast ≥ 4,5 : 1, lass den Overlay Codespans auslassen, versteck `:::` nur bei gültigem Block und zieh die Kästchen-Regel auf GFM. Fertig, wenn im Stand S4 alle `konflikt_*`, `kontrast` und `e_durchgestrichen` grün sind und die drei Gegenläufe genau ihre Zellen kippen.
- **B1.6:** Bau `js/editor/marken.js`: Inline-Paare und Format-Formen werden per `markText` eingeklappt und nur aufgedeckt, solange der Cursor das Element berührt; Maus erst 450 ms nach dem Loslassen; Buchführung nur über `cm.findMarks`. Fertig, wenn `klick30`, `doppelklick`, `dreifachklick`, `ziehen`, `grenzen`, `undo20` in beiden Browsern grün sind, `tastenkosten` ≤ 8 ms ist und die drei Gegenläufe genau ihre Zellen kippen.
- **B1.7:** Erweitere `marken.js` zum einen Zeilenbauer: Überschrift- und Zitatzeichen, Listenpunkt als Widget mit Ebenen-Einzug, Kästchen aus `editor.js` übernommen, Code- und Trennlinien als Zeilenklassen. Fertig, wenn `marker_eingeklappt`, `kante`, `gleichtext`, `listenpunkt`, `ebenen`, `kaestchen` grün sind, `tastenkosten` ≤ 8 ms bleibt, die vier Gegenläufe genau ihre Zellen kippen und die Bilder im Session-Block stehen.
- **B1.8:** Bau `js/editor/tasten.js` mit den Listen- und Tastenregeln des Plans und ergänze die Knöpfe Durchgestrichen und Aufgabe. Fertig, wenn alle `liste_*`- und `taste_*`-Zellen in beiden Browsern grün sind und jeder Gegenlauf genau seine Zelle kippt.
- **B1.9:** Bau `js/editor/raster.js`: Zellcursor, Pfeile, Tippen ersetzt, F2/Enter/Doppelklick bearbeiten den Quelltext der Zelle in einem Eingabefeld, Enter und Tab schreiben per `replaceRange` genau diese Zelle, Esc verwirft, Rückfall auf den Rohtext bei abweichender Zellzahl. Fertig, wenn alle `raster_*`-Zellen und `bytes_zelle` in beiden Browsern grün sind, die sechs Gegenläufe genau ihre Zellen kippen und drei Bilder im Session-Block stehen.
- **B1.10:** Erweitere das Raster um die Strukturbefehle des Plans, je als ein Undo-Schritt, mit einer kleinen Leiste über der gewählten Tabelle. Fertig, wenn jede `raster_op_*`-Zelle den erwarteten Body-Diff zeigt und jeder Gegenlauf genau seine Zelle kippt.
- **B1.11:** Bau Bereichsauswahl, Kopieren als TSV und Einfügen von TSV und HTML-Tabellen (nur Text) ins Raster. Fertig, wenn die vier `raster_ablage_*`-Zellen grün sind und der Gegenlauf `html_als_markup` genau seine Zelle kippt.
- **B1.12:** Vendore `searchcursor` 5.65.16 und bau `js/editor/suche.js` mit eigenem Feld: Suchen, Ersetzen, Alle ersetzen als ein Undo-Schritt. Fertig, wenn die vier `suche_*`-Zellen grün sind und der Gegenlauf genau seine Zelle kippt.
- **B1.13:** Bau `js/editor/komfort.js` mit Gliederung, Zählung, Strg/Cmd+Klick auf Links (mit Rückfrage) und dem Zeilenvergleich im Konfliktdialog; den Glyphen-Teil (Download freigegeben 2026-11-14) baut Claude Code. Fertig, wenn `gliederung` und `link_folgen_fragt` grün sind, beide Gegenläufe genau ihre Zelle kippen und `ui_budget` alle Zeilen OK meldet.
- **B1.14:** Schließ das Darstellungs-Gate: jede Zelle beider Proben bekommt einen Gegenlauf, der genau sie kippt; bau den Katalog-Wächter und den optionalen statischen Check in `health_gate.sh`; trag den Deploy-Ablauf in den Head ein. Fertig, wenn beide Proben in beiden Browsern grün sind und jeder Gegenlauf `kippt_genau` meldet.
- **B1.15:** Begleite die Sichtung des Nikingers auf der Probe-Instanz: bereite die Befehle vor, nimm jeden Fund als nachgebaute Fixture mit Zelle auf und behebe ihn. Fertig, wenn der Nikinger P11-26 abnimmt.
- **B1.16:** Bereite das Release `v4.1.0` nach §2.4 vor (D0–D3) und lies nach dem Deploy des Nikingers die echte `health_gate`-Ausgabe in den Session-Block. Du deployst nicht selbst.

## Session stopped — 2026-11-14 (Planung P11 fertig: Plan in zwei Dateien, 111 Anker geprüft, nichts am Produkt gebaut)

**Ergebnis.** P11 ist geplant: Rahmen `docs/concepts/phase11_editor_plan.md` (Locks P11-A–W, Abnahme P11-1–34, `[VERIFY]` V220–V235, Bedarf an Eurofleet, Fehlbilder) und Schritte `docs/concepts/phase11_editor_plan_block1.md` (B0.1–B0.3, B1.0–B1.16, je mit Ankern, Tests, Rot-Probe und Startauftrag). 111 Anker in `anker.json`, jeder genau einmal (`scripts/plan_anker.py`, Wächter `tests/test_plan_anker.py`).
**Entschieden (Nikinger 2026-11-13).** Zuschnitt angenommen · CodeMirror 5 bleibt, Zeichen werden eingeklappt · Tabellen „wie in Excel" · Abnahmezeilen für die Writer-Optik · Ausführer: beide · Probe-Instanz als zweiter Dienst auf dieser VM, vor dem ersten Editor-Deploy · Deploy-Logik bleibt im Repo · E6–E9, E11, E12 nach Empfehlung · Feedback-Ablage nur für den Nikinger, auf der VM · Feedback 1/3/5 erst mit `v4.1.0` · INDEX dauerhaft teilen.
**Gemessen.** `main@1128fdb` (2026-11-12): `pytest` 1938 grün, 1 rot (die damals unversionierte Notiz) · `doc_health` 1 · `ui_budget` 6/6 (238,1 / 74,0 KB) · Darstellungs-Probe 26 rot von 62, beide Browser. Prototyp Einklappen (2026-11-13): Klick 19/19, Bytes gleich, 5,0–6,1 ms je Taste, Mausregel nötig; Raster machbar in beiden Browsern. Die Prototypen liegen nicht im Repo. Arbeitsbaum mit dem Plan (2026-11-14): `pytest` 1965 grün, 0 rot · `doc_health` 0.
**Abschluss-Durchgang (2026-11-14, Claude Code; die Planungssitzung endete am Limit vor dem Commit).** Am Code und an den npm-Quellen nachgeprüft und eingearbeitet: B0.3-Befehle (Update-Log-Gate der Probe-Instanz, `health_gate --current-link`, Unit-Filter statt Neuschreiben aller Units, `authctl.py invite <space>`) · CM5 verschmilzt gleiche `+`-Ursprünge binnen 1250 ms zu einem Undo-Schritt (`changeGeneration(true)`) · Esc und Link-Klick im Raster · überlappende Klapp-Bereiche werfen · `tabellen.js:175` gegen das `\n` am Ende der marked-Ausgabe · marked und `searchcursor` ohne Netz aus dem npm-Cache · zwei zahnlose Undo-Gegenläufe (B1.10, B1.12) über einen Ursprung ohne `+` scharf gemacht · B1.13 ausgeplant (der Glyphen-Teil braucht Netz) · Haushalt-Befunde in B0.1 Nr. 8 · `rotate_session_block.sh` braucht `SESSIONS_ARCHIVE.md` → B0.1 Nr. 9 · 22 neue Anker.
**Entschieden (Nikinger 2026-11-14).** Push von `7d0b592` · Lesart „wie in Excel" (P11-G) bestätigt · V227: dieselbe DEK-Datei bleibt · Regelkandidat „Sichtung zuerst als Bild an der Wegwerf-Instanz" kommt beim Closeout P11 in die Wurzel · B1.13: die zwei Font-Downloads sind freigegeben · Feedback 5 = Variante A (Kopf schwarz wie Liste und Rail, ohne Glas), am Vergleichsbild der Wegwerf-Instanz · `p105-block5/7/9` gelöscht (lokal und `origin`); die Löschung von `hotfix-b1`, `deploy-version-marker-only` (steckt inhaltlich in `main` bzw. ist überholt) und `origin/nikinger_claude/elegant-volta-gnyarh` ist freigegeben, der Auto-Modus hat sie Claude Code verweigert — Befehle unter „Offen beim Nikinger".
**Advisor.** Planung: zwei Durchgänge als Review-Agent (Renderer zuerst, Zell-Bearbeitung im Quelltext, Zelle `gleichtext`). Abschluss-Durchgang ohne Advisor (Nikinger 2026-11-14).
**Mit diesem Commit.** Plan, Head, Anker-Werkzeug und Wächter, eurofleet-Notiz mit INDEX-Zeile, ROADMAP-Zeile P11, Wurzel-„Current state"; zwei alte Kartenzeilen verbatim ins Kürzungs-Archiv (die dauerhafte Lösung ist B0.1).
**Nächster Schritt.** **B0.1** (Claude Code), Startauftrag oben. Vorher beim Nikinger: den Bedarf an Eurofleet weiterreichen und die drei Branch-Befehle (Abschnitt „Offen beim Nikinger").
