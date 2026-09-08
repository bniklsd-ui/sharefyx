---
status: live
purpose: Regeln, Konventionen, Arbeitsweise und aktueller Stand des Space-Servers — wird jede Session automatisch geladen
read-when: immer, vor jeder Aktion in diesem Repository
detail: L2
up: docs/INDEX.md
down:
  - ROADMAP.md                          # Phasenplan + Status je Phase
  - docs/INDEX.md                       # L0-Karte aller .md
  - phase8_5_picker_release/CLAUDE.md   # aktive Phase (Phase 8.5, schließt Phase 8 mit ab)
updated: 2026-09-07 (Cluster-3-Teilverifikation — **P8-20 ✅ + P8-21 a/b/c ✅ am echten v3.0.1** durch den Nikinger in einer Login-Sitzung; P8-20 (Hover dimmt Nicht-Nachbarn + Klick öffnet Editor/Readonly via Fix C vom 2026-09-02 + Drag/Zoom/Pan) und P8-21 (Default nur explizite Kanten + Tag-Toggle + Ordner-Toggle) ohne Befund; P8-21 d + P8-22 + P8-24 in eine Folge-Session verschoben, weil alle drei die 200-Knoten-Wegwerf brauchen (Nikinger-Aktion); Phase-8-Bilanz **19 ✅ · 7 🟡 → 20 ✅ · 6 🟡** (P8-20 🟡 → ✅, P8-21 a/b/c bestätigt bei Beschreibung); `phase8_ui_graph/CLAUDE.md` §7 + Bilanz + Modul-Status Block D nachgezogen; `phase8_5_picker_release/CLUSTER3_TESTBLOCK.md` neu (17 KB, vollständiger Schritt-für-Schritt-Testblock für die Cluster-3-Prüfungen, Audit-Quelle für Z); pytest unverändert 964/964, Tabu-Diff §0.3 leer, Service-Touch 0 (PID 355956 nur gelesen, kein `sudo systemctl`); **Nikinger-Aktion in derselben Sub-Session:** Sean-Einladung — `authctl.py invite sean --purpose initial --ttl 86400` schreibt in die echte `auth.sqlite3` des `sharefyx-mcp.service` (Hard Rule 9 + §0.5.7 verbieten opencode/M3 den Eingriff), Link wird auf stdout einmalig ausgegeben; nächster Schritt Cluster 4 + 5 + Z, nach allen Clustern dann Phase-8-✅-Nachtrag + p8.X-Ankündigung im Z-Closeout) | 2026-09-07 (Phase 8.5 Pre-Z-Tausch — **erste opencode/M3-Code-Touch-Session seit Cluster 1**; P8.5-19 (Bauform Radiogruppe statt `<select>`) + P8.5-6 (Bracket-Renderer-Fix in `markdown.js`) committet, beide Zeilen jetzt mit Code + statischem Test; `dialogs.js` (`linkPickerModeEl` raus, neue Modul-Konstante `LINK_PICKER_MODE_NAME`, Selektor-Wechsel von `getElementById` auf `querySelector[All]('input[name="link-picker-mode"]')`, change-Listener iteriert die zwei Radios), `app.html` (`<fieldset class="link-picker-modes">` mit `<legend>Einfügen</legend>` + 2× `<input type="radio" name="link-picker-mode" value="…">` ersetzt `<select id="link-picker-mode">`), `app.css` neuer Block `.link-picker-modes`/`.link-picker-mode` mit `accent-color: var(--accent-line)`, `markdown.js` Link- und Bild-Regex tolerieren jetzt `\[` / `\]` als Escape-Einheit via `\\[\[\]]` (zwei Zeichen), danach `\\([\[\]])` → `$1` zum Unescapen des Title/Alt; `phase5_ui/tests/test_static_routes.py` +2 (`test_link_picker_uses_a_radio_group_not_a_select` P8.5-19, `test_markdown_link_regex_allows_escaped_brackets` P8.5-6 mit Regressionstest gegen die alte `[^\]]+`-Form); pytest 962 → **964** grün (254 s Gesamtlauf), `node --check` grün auf `dialogs.js` + `markdown.js`, `ui_budget.py` 5/5 im Korridor (dialogs.js 12.6 → 13.2 KB, markdown.js 4.2 KB, app.css +0.4 KB), Tabu-Diff §0.3 leer (alle Änderungen unter `phase5_ui/webui/static/` + `phase5_ui/tests/`, kein Servercode-Tabu-Auslöser), node-Probe gegen `markdown.js` mit Mock-`document`: 8 Test-Cases rendern wie erwartet — darunter D4-Fund-Beispiel `[Vercel \[Hosting\](#item/itm_67bb0565)` → `<a href="#item/itm_67bb0565">Vercel [Hosting]</a>`; Phase-8.5-Summary **5 ✅ · 13 🟡 · 2 ⬜ → 5 ✅ · 14 🟡 · 1 ⬜** (P8.5-19 ⬜ → 🟡, P8.5-5/-6-Beschreibungen aktualisiert); Phase-8-Bilanz unverändert 19/7/0; Phase-8.5-Head rotiert (Cluster-1-Block per Hand nach `SESSIONS_ARCHIVE.md`, dieser Pre-Z-Tausch-Block neu im Head, **~49 KB deutlich über 40-KB-Softcap** — Auflösung bleibt Z-Arbeit oder Trimm-Pass vor Z, gleiche Linie wie D3/D4 dokumentiert); Working Tree jetzt 7 uncommittete Dateien [5 Code/Tests + 2 Doku-Updates]; nächster Schritt unverändert Cluster 3+4+5 (Nikinger-Aktionen) + Z, mit optionaler P8.5-6-Wegwerf-Re-Probe in Cluster 4) | 2026-09-07 (Phase 8.5 + Phase 8 Cluster-2 — **erste echte Live-Verifikations-Welle seit D3**; Nikinger gegen v3.0.1 bestätigt: P8-14, P8-15, P8-18, P8-19, P8-23 (Screenshot `phase8_5_picker_release/screenshots/Bildschirmfoto 2026-09-07 um 17.08.37.png` zeigt tabellose Space-Zeilen + Zähler-Chips + VERKNÜPFUNGEN-Graph in eigen blau/geteilt türkis/fremd grau + ZULETZT-BENUTZT-Sektion + Badge `SHAREFYX v3.0.1`); P8.5-18 jetzt ✅ als Umbrella; Phase-8-Bilanz 14/12/0 → **19/7/0**, Phase-8.5-Bilanz 4/13/3 → **5/13/2** (P8.5-18 von ⬜ auf ✅); Phase-8-Glyph-Entscheidung noch offen (Vorschlag vorerst 🟡 bis Cluster 3/5); P8-20/21/22/24 + P8-5/8 bleiben 🟡 für Cluster 3/5; keine Code-Änderung in dieser Sub-Session — alle Updates sind Doku; Phase 8.5 Head rotiert (40.5 KB unter Cap); Working Tree jetzt 14 uncommittete Dateien [7 von D4+Sichtprobe-Folgesession + 7 von Cluster 1+2] | 2026-09-07 (Phase 8.5 Cluster-1 der Sichtprüfungen — **erste echte Code-Touch-Session seit D1**; `phase8_ui_graph/scripts/p8_16_glass_fallback_probe.py` + `wegwerf_setup_p8_16.py` neu (Port 18775, Standing-Permission-Muster reproduziert), vier Screenshots `docs/screenshots/p8_16_{01..04}_*.png`; CDP-Switch `prefers-reduced-transparency: reduce` über `Emulation.setEmulatedMedia` — beide Glass-Träger `.list__head`+`.overlay__panel` wechseln sauber `blur(14px) saturate(1.5)`+`rgba(27,32,39,0.55)` → `backdrop-filter: none`+`rgb(27,32,39)`, Selektion im Solid-Modus voll erkennbar mit Akzent-Fill+Outline; **P8.5-16 jetzt ✅**, doppelt mit Phase 8 P8-16 die selbe Evidenz; Phase-8-P8-16 bleibt 🟡 bis Nikinger-Sichtprüfung; Phase-8.5-Summary 3 ✅ · 14 🟡 · 3 ⬜ → **4 ✅ · 13 🟡 · 3 ⬜**; Phase-8.5-Head rotiert (40.579 B, 381 B unter 40-KB-Softcap); Working Tree jetzt 13 uncommittete Dateien [7 von D4+Sichtprobe-Folgesession + 6 von Cluster 1]; `pytest`/`node --check`/`ui_budget.py` nicht gelaufen (irrelevant), Tabu-Diff §0.3 leer (Phase-8.5-Tabu greift nicht für `phase8_ui_graph/scripts/`), Service-Touch 0 nur gelesen (PID 355956 unverändert seit 2026-09-05 16:10:18 CEST); nächster Schritt Cluster 2-5 je nach Nikinger) | 2026-09-06 (Phase 8.5 D4-Sichtprobe-Folgesession — **nur dokumentiert, kein Code-Touch in dieser opencode/M3-Session**; sieben neue Themen-Cluster aus der Sichtprobe mit Fabian nach D4 dokumentiert: **Spaces-Layout-Reorg** [„Alle Items"-Leiste unter Spaces + Kippschalter, Map 40 % Breite/volle Höhe, keine Duplikate], **Obsidian-Map** fünf Sub-Punkte [Performance-Reload, Landkarten-Stil, Field schneidet ab, Reload-Drift, Collapsible mit Abhängigkeiten], **Anzahl-Anzeige Ordner**, **Edit-in-Place-Vision** [„Bearbeiten"-Knopf überflüssig], **Layering-Design-System** [3 Layer: echtes Schwarz / aktueller Standard / Liquid Glass + Selektion explizit blau auf Hover, Note-Select, Checkbox], **„Konto"→„Einstellungen"-Rename** + Positions-Tausch mit Logout, **De-AI-ierung-Lauf 2** nach neuen Kriterien; neue Datei `docs/concepts/p8x_ui_polish_notes.md` 25 KB L2 mit allen 16 Themen — fünf bereits in D4 dokumentierte p8.X-Punkte [UX-2-Step-Knotenklick, Map-Field schneidet ab, Map fliegt, Save-Button-YAML-Header, Fabis Sammelliste] + sieben Sichtprobe-Folgesession-Cluster + vier Sub-Punkte aus §2 Obsidian-Map; Anhang §A–§E für die Planungs-Session in Claude Code; **kein Phase-8/8.5-Scope-Touch**, **keine** neuen Tabu-Aufhebungen, **kein** Locking — Sammlung, kein Plan; D4-Block per Hand nach `SESSIONS_ARCHIVE.md` rotiert (Skript passt nicht auf Phase-8.5-Muster, bewährtes Vorgehen); Modul-Status P8.5 unverändert (3 ✅ · 14 🟡 · 3 ⬜); pytest nicht gelaufen, Tabu-Diff §0.3 leer, Service-Touch 0; nächster Schritt unverändert D5 + V105 + optional vor Z Radiogruppe + Bracket, dann Z) | 2026-09-06 (Phase 8.5 D4 Sichtprüfung am echten Gerät durch den Nikinger — **nur dokumentiert, kein Code-Touch in dieser opencode/M3-Session**; Block 1–7 + Vorbereitung komplett durchgelaufen, Login beide Accounts ✅, Tastaturnavigation in Firefox+Chrome+Safari auf zwei Accounts ✅, Block 2/4/5-Kern ohne Befund, drei echte Funde dokumentiert: **P8.5-19-Entscheidung Radiogruppe** [User-Präferenz „deut... (line truncated to 2000 chars) | 2026-09-05 (Phase 8.5 D2 vom Nikinger zwischen D1 und D3 + D3-Prep, 🟡, ⬜ D4/D5/V105/Z als Nächstes. D2 ist **zwischen D1 (Commit heute früh) und D3 (diese Session) still durch den Nikinger gelaufen** — Entdeckung kam erst beim ersten Probe-Lauf des Health-Gate-Skripts: `/opt/sharefyx/current` → `20260905T140325.378914Z` → HEAD `6f19a8f` (D1), Service-PID **355956** (statt der im D1-Block notierten 195922 — D2-Deploy hat den Dienst erwartungsgemäß neu gestartet), `ExecMainStartTimestamp=2026-09-05 16:10:18 CEST`. Damit ist D3 nicht mehr Vorbereitung, sondern **Verifikation des bereits deployten v3.0.1**. Neu gebaut: `phase8_5_picker_release/scripts/health_gate.sh` (134 Zeilen bash, `set -uo pipefail`, JSON auf stdout / Details auf stderr nach Hard Rule 7), acht Gates — `/health` 200 mit Retry-Loop, `/ui/login` 200, `/api/v1/me` 401, `/mcp/` 401, `.rail__version` aus `/ui/static/app.html` (**nicht** `/ui/login` — `pages.py`s Auth-Template ohne Rail, erste Iteration fiel darauf herein, gefixt), `/opt/sharefyx/current` → Release mit `.git`, optional `--require-todays-update-log` (UTC/local wie `deploy.sh` Z. 127-131), optional `--expected-sha=<hex>` (Short- oder Full-Form per Prefix-Vergleich). **Lauf-Beleg 2026-09-05 15:19:53Z** mit `--require-todays-update-log --expected-sha=6f19a8f`: **8/8 grün**, Exit 0, JSON auf stdout (`result:"ok"`, `actual_version:"v3.0.1"`, `release_sha:"6f19a8f..."`, `active_release:"/opt/sharefyx/releases/20260905T140325.378914Z"`, `port:8765`). Drei Negativproben separat verifiziert (Port 9999 → Gate 1 rot, `--expected-version=v9.9.9` → Gate 5 rot, `--expected-sha=0000000` → Gate 8 rot). **P8.5-17 teilweise abgehakt:** Deploy gelaufen ✅, Health-Gate 8/8 ✅, Badge `v3.0.1` live ✅, Update-Banner-Live-Anzeige ⬜ (braucht Auth, Nikinger), V105 ⬜ (echter Anthropic-Connector, Nikinger). Modul-Status-Zeile 6 Block D um D2 ✅ + D3 🟡 erweitert; Abnahmestand-Zeile P8.5-17 Health-Gate-Teil 🟡; Summary **3 ✅ · 14 🟡 · 3 ⬜ von 20**; D1-Block (111 Zeilen) per Hand nach `SESSIONS_ARCHIVE.md` rotiert (Skript passt nicht auf das Phase-8.5-Muster — bewährtes Vorgehen aus D1 selbst). `pytest` nicht gelaufen (kein Python-Touch), `bash -n` OK, shellcheck nicht verfügbar (übersprungen, keine Konvention im Repo), Tabu-Diff §0.3 leer, Service-Touch 0 (PID 355956 nur gelesen). **Nächster Schritt:** D4 — Sichtprüfung am echten Gerät durch den Nikinger (`## 2026-09-05`-Eintrag im Update-Banner sichtbar, `<select class="input" id="link-picker-mode">` im Picker vorhanden — P8.5-19-Abnahme: Radiogruppe oder `<select>`-Bestätigung), D5 Vierte A3-Probe (entscheidet §9.4.1 Abbruchregel aus N2), V105-Connector-Check, Z Closeout. 2026-09-07 (Phase 8.5 Pre-Z-Tausch — **erste opencode/M3-Code-Touch-Session seit Cluster 1**; P8.5-19 (Bauform Radiogruppe statt `<select>`) + P8.5-6 (Bracket-Renderer-Fix in `markdown.js`) committet, beide Zeilen jetzt mit Code + statischem Test; `dialogs.js` (`linkPickerModeEl` raus, neue Modul-Konstante `LINK_PICKER_MODE_NAME`, Selektor-Wechsel von `getElementById` auf `querySelector[All]('input[name="link-picker-mode"]')`, change-Listener iteriert die zwei Radios), `app.html` (`<fieldset class="link-picker-modes">` mit `<legend>Einfügen</legend>` + 2× `<input type="radio" name="link-picker-mode" value="…">` ersetzt `<select id="link-picker-mode">`), `app.css` neuer Block `.link-picker-modes`/`.link-picker-mode` mit `accent-color: var(--accent-line)`, `markdown.js` Link- und Bild-Regex tolerieren jetzt `\[` / `\]` als Escape-Einheit via `\\[\[\]]` (zwei Zeichen), danach `\\([\[\]])` → `$1` zum Unescapen des Title/Alt; `phase5_ui/tests/test_static_routes.py` +2 (`test_link_picker_uses_a_radio_group_not_a_select` P8.5-19, `test_markdown_link_regex_allows_escaped_brackets` P8.5-6 mit Regressionstest gegen die alte `[^\]]+`-Form); pytest 962 → **964** grün (254 s Gesamtlauf), `node --check` grün auf `dialogs.js` + `markdown.js`, `ui_budget.py` 5/5 im Korridor (dialogs.js 12.6 → 13.2 KB, markdown.js 4.2 KB, app.css +0.4 KB), Tabu-Diff §0.3 leer (alle Änderungen unter `phase5_ui/webui/static/` + `phase5_ui/tests/`, kein Servercode-Tabu-Auslöser), node-Probe gegen `markdown.js` mit Mock-`document`: 8 Test-Cases rendern wie erwartet — darunter D4-Fund-Beispiel `[Vercel \[Hosting\](#item/itm_67bb0565)` → `<a href="#item/itm_67bb0565">Vercel [Hosting]</a>` (vor dem Fix kaputt); Phase-8.5-Summary **5 ✅ · 13 🟡 · 2 ⬜ → 5 ✅ · 14 🟡 · 1 ⬜** (P8.5-19 ⬜ → 🟡, P8.5-5/-6-Beschreibungen aktualisiert); Phase-8-Bilanz unverändert 19/7/0; Phase-8.5-Head rotiert (Cluster-1-Block per Hand nach `SESSIONS_ARCHIVE.md`, dieser Pre-Z-Tausch-Block neu im Head, **~49 KB deutlich über 40-KB-Softcap** — Auflösung bleibt Z-Arbeit oder Trimm-Pass vor Z, gleiche Linie wie D3/D4 dokumentiert); Working Tree jetzt 7 uncommittete Dateien [5 Code/Tests + 2 Doku-Updates]; nächster Schritt unverändert Cluster 3+4+5 (Nikinger-Aktionen) + Z, mit optionaler P8.5-6-Wegwerf-Re-Probe in Cluster 4) | 2026-09-07 (Phase 8.5 + Phase 8 Cluster-2 — **erste echte Live-Verifikations-Welle seit D3**; Nikinger gegen v3.0.1 bestätigt: P8-14, P8-15, P8-18, P8-19, P8-23 (Screenshot `phase8_5_picker_release/screenshots/Bildschirmfoto 2026-09-07 um 17.08.37.png` zeigt tabellose Space-Zeilen + Zähler-Chips + VERKNÜPFUNGEN-Graph in eigen blau/geteilt türkis/fremd grau + ZULETZT-BENUTZT-Sektion + Badge `SHAREFYX v3.0.1`); P8.5-18 jetzt ✅ als Umbrella; Phase-8-Bilanz 14/12/0 → **19/7/0**, Phase-8.5-Bilanz 4/13/3 → **5/13/2** (P8.5-18 von ⬜ auf ✅); Phase-8-Glyph-Entscheidung noch offen (Vorschlag vorerst 🟡 bis Cluster 3/5); P8-20/21/22/24 + P8-5/8 bleiben 🟡 für Cluster 3/5; keine Code-Änderung in dieser Sub-Session — alle Updates sind Doku; Phase 8.5 Head rotiert (40.5 KB unter Cap); Working Tree jetzt 14 uncommittete Dateien [7 von D4+Sichtprobe-Folgesession + 7 von Cluster 1+2] | 2026-09-07 (Phase 8.5 Cluster-1 der Sichtprüfungen — **erste echte Code-Touch-Session seit D1**; `phase8_ui_graph/scripts/p8_16_glass_fallback_probe.py` + `wegwerf_setup_p8_16.py` neu (Port 18775, Standing-Permission-Muster reproduziert), vier Screenshots `docs/screenshots/p8_16_{01..04}_*.png`; CDP-Switch `prefers-reduced-transparency: reduce` über `Emulation.setEmulatedMedia` — beide Glass-Träger `.list__head`+`.overlay__panel` wechseln sauber `blur(14px) saturate(1.5)`+`rgba(27,32,39,0.55)` → `backdrop-filter: none`+`rgb(27,32,39)`, Selektion im Solid-Modus voll erkennbar mit Akzent-Fill+Outline; **P8.5-16 jetzt ✅**, doppelt mit Phase 8 P8-16 die selbe Evidenz; Phase-8-P8-16 bleibt 🟡 bis Nikinger-Live-Sichtprüfung; Phase-8.5-Summary 3 ✅ · 14 🟡 · 3 ⬜ → **4 ✅ · 13 🟡 · 3 ⬜**; Phase-8.5-Head rotiert (40.579 B, 381 B unter 40-KB-Softcap); Working Tree jetzt 13 uncommittete Dateien [7 von D4+Sichtprobe-Folgesession + 6 von Cluster 1]; `pytest`/`node --check`/`ui_budget.py` nicht gelaufen (irrelevant), Tabu-Diff §0.3 leer (Phase-8.5-Tabu greift nicht für `phase8_ui_graph/scripts/`), Service-Touch 0 nur gelesen (PID 355956 unverändert seit 2026-09-05 16:10:18 CEST); nächster Schritt Cluster 2-5 je nach Nikinger) | 2026-09-06 (Phase 8.5 D4-Sichtprobe-Folgesession — **nur dokumentiert, kein Code-Touch in dieser opencode/M3-Session**; sieben neue Themen-Cluster aus der Sichtprobe mit Fabian dokumentiert: Spaces-Layout-Reorg, Obsidian-Map [5 Sub-Punkte], Anzahl-Anzeige Ordner, Edit-in-Place-Vision, Layering-Design-System [3 Layer + Selektion blau], „Konto"→„Einstellungen"-Rename, De-AI-ierung-Lauf 2; neue Datei `docs/concepts/p8x_ui_polish_notes.md` 25 KB L2 mit allen 16 Themen — fünf D4-Punkte + sieben Sichtprobe-Folgesession-Cluster + vier Sub-Punkte aus §2 Obsidian-Map; Anhang §A–§E für die Planungs-Session; **kein Plan, kein Locking, keine Tabu-Aufhebung** — Sammlung; neue ROOT-Current-State-Zeile für die Folgesession ergänzt; `phase8_5_picker_release/CLAUDE.md` aktiver Block auf D4-Sichtprobe-Folgesession umgestellt, D4-Block per Hand nach `SESSIONS_ARCHIVE.md` rotiert (Skript passt nicht auf Phase-8.5-Muster); keine Code-Tests, kein Service-Touch; nächster Schritt D5 Vierte A3-Probe + V105 Connector-Check — beides Nikinger; optional vor Z Radiogruppe-Tausch + Bracket-Fix durch opencode/M3) | 2026-09-06 (Phase 8.5 D4 Sichtprüfung durch den Nikinger — **nur dokumentiert, kein Code-Touch in dieser opencode/M3-Session**; Block 1–7 + Vorbereitung komplett durchgelaufen, drei echte Findings: **P8.5-19 Radiogruppe statt `<select>`** [Tausch 5 Z. ausstehend], **P8.5-6 Bracket-Renderer-Bug in `markdown.js`** [Fix ausstehend], **UX-2-Step-Knotenklick als neues Feature für p8.X** [parkiert]; Phase 8 ✅ + p8.X als Nikinger-Entscheidung für Z vorgemerkt; Modul-Status Zeile 6 Block D um D4 ✅ erweitert; Summary 3 ✅ · 14 🟡 · 3 ⬜; D3-Block per Hand nach SESSIONS_ARCHIVE.md rotiert; keine Code-Tests, kein Service-Touch; nächster Schritt D5 Vierte A3-Probe + V105 Connector-Check — beides Nikinger; optional vor Z Radiogruppe-Tausch + Bracket-Fix durch opencode/M3) | 2026-09-05 (Phase 8.5 D3-Prep — `scripts/health_gate.sh` neu, 134 Zeilen bash, acht Gates; **Lauf 2026-09-05 15:19:53Z 8/8 grün** gegen den frischen Deploy; **D2 lief zwischen D1 und D3 still durch den Nikinger** (PID 355956 statt 195922, Release `20260905T140325.378914Z`, ExecMainStartTimestamp `2026-09-05 16:10:18 CEST`) — D3 ist Verifikation statt Vorbereitung; D1-Block per Hand nach `SESSIONS_ARCHIVE.md` rotiert; Modul-Status Zeile 6 um D2 ✅ + D3 🟡 erweitert; Abnahmestand P8.5-17 Health-Gate-Teil 🟡, Summary-Zeile 3 ✅ · 14 🟡 · 3 ⬜; pytest nicht gelaufen (kein Python-Touch), bash -n OK, shellcheck nicht verfügbar (übersprungen, keine Konvention im Repo), Tabu-Diff §0.3 leer, Service-Touch 0; nächster Schritt D4 Sichtprüfung am echten Gerät — Nikinger-Aktion) | 2026-09-05 (Phase 8.5 D1 committet — Badge `v3.0`→`v3.0.1` in `phase5_ui/webui/static/app.html:20` (P8.5-N7, statisches HTML nicht im Tabu §0.3); neuer `## 2026-09-05`-Block in `docs/UPDATE_LOG.md` mit drei Zeilen Picker-Modi/Tastatur/Generalisierter-Hint — **Datums-Drift dokumentiert**: Block-C-Absatz schlug `## 2026-09-04` vor, `date +%F`/`date -u +%F` ist heute 2026-09-05, `deploy.sh` Z. 117–131 verlangt strikt `today_utc`/`today_local`, sonst Gate-Abbruch; Block-C-Block per Hand nach `SESSIONS_ARCHIVE.md` rotiert (Skript passt nicht auf Phase-8.5-Muster mit einem `## Session stopped` + mehreren `### date`-Subblöcken → Exit 2 „Bereits konform"); Modul-Status D `⬜`→`🟡` mit D2–D5 als Nikinger-Aktionen vermerkt; `pytest` nicht gelaufen (kein Python-Touch), Tabu-Diff §0.3 leer, Service-Touch 0 (PID 195922 / ActiveEnterTimestamp 2026-09-02 11:51:57 CEST nur gelesen); nächster Schritt D2 = `sudo systemctl ... deploy.sh main`) | 2026-09-04 (Wurzel-CLAUDE.md komprimiert -- Phase-6-Verlaufsdokumentation + Phase-6/6.5-Vormerkungen + Funnel-Reboot + MCP-Werkzeug-Ergonomie + End-Korrekturen P5/P4 auf Pointer-Form gestaucht; ~5 KB freigemacht, aktueller Stand ~39.7 KB unter Cap; Phase-8.5-Work-Abschnitt aktualisiert auf A1+A2, A1-Block rotiert nach Archiv) | 2026-09-04 (Phase 8.5 B1 committet -- `_TITLE_NOT_ID_HINT` in `phase2_mcp/mcpserver/tools.py:159-164` generalisiert, „Das gilt in jeder Textform -- auch nicht als Tabellen-Spalte, nicht in Klammern hinter dem Titel und nicht in Aufzählungs-Zeilen" wörtlich aus Plan §3 B1; `test_tools.py` zwei Asserts (`in jeder Textform`/`Klammern`); neuer Phase-Head-Abschnitt `## Abbruchregel §9.4.1 (N2, verbindlich)`; Modul-Status B1 + P8.5-3, A2-Block nach `SESSIONS_ARCHIVE.md` rotiert; pytest 962/962 unverändert, Tabu-Diff zeigt **genau** `tools.py +5/-2` und `test_tools.py +2`, kein Service-Touch) | 2026-09-04 (Phase 8.5 A2 committet `7ce0be0` -- Tastaturnavigation `aria-activedescendant` + `_pickLinkPickerAt` + CSS-Block-Entdopplung am Picker; +3 statische Tests in `test_static_routes.py`; A1-Block nach `SESSIONS_ARCHIVE.md` rotiert) | 2026-09-04 (Phase 8.5 Drift nachgezogen `4424310` + A1 committet `499d9be` -- Picker-Modus-Umschalter + `localStorage` `sfx:linkpicker:mode`; V99 `session` zu `local` als Eskalation wegen P8.5-G; erste `localStorage`-Nutzung des Projekts) | 2026-09-03 (Phase 8.5 Step 0 -- Skelett phase8_5_picker_release/{CLAUDE.md, SESSIONS_ARCHIVE.md, scripts/} angelegt; vier Paragraph-1-Funde: INDEX 52.911 zu 40.917 B unter Cap, Bueroklammer-zu-Lupe-Drift in phase8_ui_graph/CLAUDE.md:440, Phase-8-Bilanz korrigiert; ROADMAP-Abschnitt neu; Wurzel-`down:` umgestellt) | 2026-09-01 (Phase 8 Sichtpruefung 1 + Gate B zu C bestanden; **Hard Rule 9 ergaenzt** -- kein `pkill -f` mit Regex, niemals den systemd-Dienst anfassen, Lehre aus dem Prod-Vorfall 2026-09-01 Phase 8 Step A3 Nachbereitung) | aeltere Eintraegge: die jeweilige phase*/SESSIONS_ARCHIVE.md
---
# CLAUDE.md — Project Instructions

> Read this file before doing anything in this repository.
> It is the single source of truth for project rules, conventions, and current state.

---

## What this project is

Ein **geteilter Kontext-Space-Server** für zwei Personen (Nikinger + Kollege) und deren
Claude-Instanzen. Notizen und Aufgaben liegen als Markdown-Dateien mit YAML-Frontmatter auf
einer Heim-VM; Claude greift über einen **Remote-MCP-Server** (Custom Connector, Streamable
HTTP) lesend und schreibend darauf zu, Menschen über eine Web-UI oder direkt im Editor.

Der Server läuft hinter **CGNAT** (RUT X50, Mobilfunk) — die Verbindung kommt von Anthropics
Backend, nicht vom Client. Erreichbarkeit daher **ausschließlich über einen ausgehenden
Tunnel**, niemals über Port-Forwarding.

Build order: `ROADMAP.md` · Doku-Karte: `docs/INDEX.md`

---

## Core principle (read carefully)

**Bauprinzip: Der Server ist dumm.**

Die gesamte Intelligenz sitzt beim Client (Claude). Der Server ist ein Aktenschrank mit
Schloss — mehr nicht.

**Der Server macht:**
- Dateien lesen/schreiben (atomar), Frontmatter parsen/serialisieren
- Index pflegen, Suchen beantworten, Paginierung
- Auth (Token → Space), Autorisierung (eigener Space schreibbar, fremde read-only)
- Versionierung, Konflikterkennung, Git-Commits
- Fehlerbehandlung, Logging, Health

**Der Server macht NIEMALS:**
- LLM-Calls, Embeddings, semantische Suche, Zusammenfassungen, Auto-Tagging
- irgendeine Form von „Verstehen" des Inhalts

Wer hier ein LLM einbauen will → **stop**. Das gehört auf die Client-Seite. Ein Server, der
Inhalte interpretiert, ist ein Server, dessen Fehlverhalten man nicht mehr debuggen kann —
und er importiert Prompt-Injection direkt in den Speicherpfad.

---

## Hard Rules (no exceptions)

1. **Niemals Secrets in Dateien.** Keine Tokens, keine Keys — nicht in `.env`, nicht in JSON,
   YAML oder Config. Space-Tokens und Tunnel-Credentials leben ausschließlich im OS-Keyring
   (Service `nikinger-space`) bzw. als systemd `LoadCredential`. Zugriff über
   `storage/credentials.py`. Ein Token in einem Commit ist ein Incident, kein Schönheitsfehler.
   **[2026-07-25 Korrektur, P2 Step 3]:** `storage/credentials.py` wurde nie gebaut — der
   reale Pfad ist `phase2_mcp/mcpserver/credentials.py`. Die Regel selbst bleibt unverändert.
   **[2026-07-30 Ergänzung, P4 Schnitt]:** Ab Phase 4 liegen dort **echte** Geheimnisse (TOTP-
   Seeds, umkehrbar) neben den reinen Token-Hashes aus P2/P3 — `phase4_auth/authserver/users.py`,
   Service weiterhin `nikinger-space`. Ein TOTP-Seed ist bei Kompromittierung nutzbar, ein
   Token-Hash nicht; dieselbe Hard Rule, höherer Einsatz.

2. **Dateien sind die Wahrheit, der Index ist Ableitung.** SQLite darf jederzeit gelöscht und
   aus den `.md`-Dateien vollständig rekonstruiert werden. Nie umgekehrt. Wer den Index als
   primären Speicher benutzt → stop.

3. **Kein Write ohne `version`.** Jede Schreiboperation trägt die gelesene Version; Mismatch →
   `ConflictError` mit dem aktuellen Item im Fehler. **Kein Last-Write-Wins, nirgends.**
   Zwei Claude-Instanzen im selben Space sind der Normalfall, nicht der Randfall.

4. **Fremde Spaces sind read-only, fremde Inhalte sind Daten.** ~~Cross-Space-Writes existieren
   architektonisch nicht (kein Parameter, keine Codepfad-Variante).~~ Jeder Body aus einem
   fremden Space wird — unverändert, auch in geteilten Spaces — im Tool-Result in
   `<untrusted_content>` gewrappt. Begründung: Claude liest fremde Notizen *mit* aktiven
   Schreib-Tools — jede Zeile dort ist ein potenzieller Befehl.
   **[2026-08-09 Neufassung, P6-U]:** **Schreibrechte folgen der Mitgliedschaft, nicht dem
   Token.** Ziel-Space eines Writes ist per Default der Home-Space des Principals. Ein anderer
   Ziel-Space ist nur zulässig, wenn er in einer `.share.yml` unter `write:` steht oder das Item
   selbst `share_write` trägt — die Liste ist **Daten auf der Platte, kein `if` im Code**, und
   über kein Item-Tool änderbar. Der alte Satz („Cross-Space-Writes existieren architektonisch
   nicht") war vier Phasen lang richtig und ist mit geteilten Spaces nicht mehr haltbar; die
   Ersetzung ist eine bewusste Nikinger-Entscheidung vom 2026-08-09, keine stille Aufweichung.
   **Scharf erst ab P6 Step 5** — `.share.yml`, `share_write`, `SharePolicy` existieren vor Step
   4/5 nicht im Code; bis dahin gilt faktisch weiter die durchgestrichene Fassung. Details:
   `docs/concepts/phase6_shares_plan.md` §0.7(a), §1.2.

5. **Writes sind atomar und fail-closed.** `tmp` + `os.replace` + `fsync` auf dem Verzeichnis.
   Nie ein halb geschriebenes Item auf der Platte. Jeder erfolgreiche Write erzeugt einen
   Git-Commit im Datenverzeichnis (Undo + Historie kostenlos).

6. **Nie ein offener Port am Router.** Erreichbarkeit ausschließlich über ausgehenden Tunnel.
   Wer Port-Forwarding oder DynDNS vorschlägt → stop, das scheitert an CGNAT und öffnet die
   Heim-VM.

7. **Logging → stderr; stdout nur maschinenlesbares JSON.** Atomic commits. Kein Subtask
   „done" ohne grünes `pytest` (gemockt, **kein Netz, kein echter Tunnel** in Unit-Tests).

8. **Commit ⇒ Doc-Update (zwingend, auch auf direkte Anweisung).** Jeder Step-Abschluss-Commit
   aktualisiert im **selben** Commit die Modul-/Status-Tabelle der Phase **und** den
   `## Session stopped`-Block. Neue `.md` ⇒ Zeile in `docs/INDEX.md` im selben Commit.

9. **Niemals per Regex-Substring Prozesse killen, niemals den systemd-Dienst anfassen.**
   `pkill -f <muster>` matcht mit Extended Regex — ein einzelner `.` matcht `/`, ein Modulname
   im eigenen und im Production-Args reicht, um die falsche PID zu treffen. Konkret
   (2026-09-01, Phase 8 Step A3 Nachbereitung): `pkill -f "phase2_mcp.scripts.serve"` killte
   sowohl die Wegwerf-Instanz als auch die Produktion (`sharefyx-mcp.service`, PID 38101,
   SIGTERM, Journal bestätigt). Stopp-Reihenfolge: **eigene** Wegwerf-Instanzen sind erlaubt
   zu stoppen, aber ausschließlich über PID-Datei, `pgrep -f` mit Anker (`$`) oder über den
   eindeutigen Port — nie über Regex im Cmdline. Den **einen** systemd-verwalteten
   `sharefyx-mcp.service` startet/stoppt/restartet **ausschließlich der Nikinger**
   (`sudo systemctl ...` läuft nicht aus dem `savefyx`-User, und auch wenn es liefe:
   Handlungsgrenze). Vor jedem `kill`/`pkill`/`systemctl` zuerst fragen: *ist das die echte
   Instanz, oder meine Wegwerf-Instanz, oder gar nicht meine?* Im Zweifel: fragen, nicht
   schießen.

---

## Working style

- **Quelle der Wahrheit ist der Code, nicht dieses Dokument.** Bei Widerspruch gewinnt das
  getestete Artefakt; das Dokument wird sofort mit datierter Korrekturnotiz gefixt.
- **`[VERIFY]`-Marker:** Alles, was gegen den echten Repo-Stand oder eine externe API geprüft
  werden muss, ist so markiert. Bei Ausführung verifizieren, **nie** als gesichert übernehmen.
- **Gelockte Entscheidungen bleiben gelockt.** Widersprechende Evidenz wird ein expliziter
  Befund für den Menschen, nie eine stille Abweichung.
- **Act vs. ask:** reversible, in-scope Schritte selbst ausführen; bei destruktiven Aktionen,
  Scope-Änderungen und Out-of-Scope-Edits stoppen und fragen.
- **Handover für einen kalten Leser schreiben.** Ergebnis zuerst, kein Session-Slang, nächster
  Schritt konkret genug zum Sofortstart.

## Doku-Hygiene (Doc-Layers)

Vollspec: `docs/DOC_LAYERS_CONVENTION.md` (v1, 2026-07-06) — **byte-identische Kopie aus dem
Trading-Bot-Repo**, dort bewusst projekt-agnostisch geschrieben. Sie wird hier **nicht**
projektspezifisch angepasst: zwei Kopien derselben Regel, die sich unterschiedlich entwickeln,
sind schlimmer als eine, die an einer Stelle etwas allgemein formuliert ist. Wer sie ändern
will, ändert sie im Trading-Bot-Repo und kopiert erneut.

Kurzform: **L0** = `docs/INDEX.md` · **L1** = ≤15-Zeilen-Header-Card oben in jedem *lebenden*
Dokument · **L2** = schlanke Bodies, Softcap **≤40 KB** · **L3** = Archive und datierte
Snapshots. Rotationsregel ab Tag 1 scharf: ein Phase-Head trägt **genau einen** aktuellen
`## Session stopped`-Block; der vorherige wandert **verbatim** nach `SESSIONS_ARCHIVE.md`.
Durchführung über `scripts/rotate_session_block.sh <phase_verzeichnis>`, nie von Hand.

> Diese Regel gilt hier ab dem ersten Commit, nicht als späterer Rettungseinsatz. Im
> Trading-Bot-Repo wuchs `phase8_scheduler/CLAUDE.md` auf 211 KB, bevor sie eingeführt wurde.

---

## Current state

**[2026-09-03] Phase 8.5 geplant — ⬜ nicht gestartet.** Link-Picker-Politur, Titel-statt-ID-Hint,
v3-Vorabritt und Deploy (`phase8_5_picker_release/`, kein eigenes Python-Paket). Plan:
`docs/concepts/phase8_5_picker_release_plan.md` (N1–N7 gelockt, P8.5-A–P8.5-T, Abnahme
P8.5-1–P8.5-20, `[VERIFY]` V95–V105). Schließt die drei Restdefekte aus
`phase8_ui_graph_plan.md` §9.4.1–§9.4.3 und **beendet Phase 8 formal mit** (N6, Präzedenz
P7 Step A8 für Phase 6.5) — deshalb 8.5 und nicht 9. **Wichtige Korrektur zum Live-Stand:**
v3.0 ist **nicht** ausgeliefert — `/opt/sharefyx/current` zeigt auf `007b73d` (Block B),
Badge `v2.2.3`; Block C (Design v3) und Block D (Graph, tabellose Übersicht) liegen nur im
Repo. Deshalb ist ein **voller 13-Stationen-Vorabritt gegen eine Wegwerf-Instanz vor dem
Deploy** Teil dieser Phase (N5), nicht nur die drei Fixes. Kernbefund der Planung, im Code
verifiziert: ein Body-Link `[Titel](#item/itm_…)` ist bereits eine Graph-Kante
(`storage/linkscan.py`) — der Picker bekommt deshalb einen **Modus-Umschalter** statt eines
Kombi-Klicks. **Ausführung wieder opencode/M3 ohne Advisor** (N4), mit neuer
Eskalationsregel: Kaskaden-Ursachen gehen an Claude Code (Lehre vom 2026-09-02).

**[2026-09-03] Phase 8.5 — 🔄 Step 0 abgeschlossen, ⬜ A1 noch nicht angefangen.** Skelett
angelegt (`phase8_5_picker_release/{CLAUDE.md, SESSIONS_ARCHIVE.md, scripts/}` mit L1-Cards,
Modul-Status-Tabelle für Step 0/A/B/C/D/Z, Abnahmematrix nach §7-Muster, leerer
`## Session stopped`-Block), die vier vom Plan §1 benannten Funde abgearbeitet:
`docs/INDEX.md` 52.911 B → 40.917 B (Kürzung `updated:` auf die 5 neuesten Einträge +
Schlusszeile „ältere Einträge: phase*/SESSIONS_ARCHIVE.md", jetzt 43 B unter dem eigenen
40 KB-Softcap, Ausnahmenliste kompakt gehalten wegen der Mehrbelastung), vier card-lose
`.md` als korrekte Ausnahmen dokumentiert (Harness, Test-Fixtures, maschinell geparst,
Vendor/Lizenz), Doku/Code-Drift „Büroklammer" → „Lupe" in
`phase8_ui_graph/CLAUDE.md:440` mit datierter Korrekturnotiz, Phase-8-Abnahmebilanz
**15/10/0 → 14/12/0** maschinell korrigiert und awk-Kommando im Phase-8-Head Bilanz-Abschnitt
verankert (zählmaschinell nachprüfbar, statt weiterer Drift). ROADMAP-Abschnitt „Phase 8.5",
Wurzel-CLAUDE.md-`down:` auf `phase8_5_picker_release/CLAUDE.md` umgestellt, drei INDEX-Zeilen
unter „Phase 8.5 — 🔄 …" — alles im selben Commit (Hard Rule 8). **`pytest` unverändert
959/959 grün** (kein Python-Touch in dieser Session), Tabu-Diff §0.3 leer, kein Service-Touch
(PID 195922, ActiveEnterTimestamp 2026-09-02 11:51:57 CEST — nur gelesen). Nächster Schritt:
Block A / A1 (Picker-Modus-Umschalter).

**[2026-09-04] Phase 8.5 — 🔄 A1 committet, Drift nachgezogen, ⬜ A2 als Nächstes.** A1
(Picker-Modus-Umschalter + Body-Markdown-Link-Helper + `localStorage` unter
`sfx:linkpicker:mode`) gebaut und committet (`499d9be`, vollständiger Session-Block in
`phase8_5_picker_release/CLAUDE.md`); Modul-Status A1 `⬜` → `🟡` (Tests ⬜, Browser-Nachweis
folgt in Block C Station 6/8). **Drift-Korrektur in diesem Commit:** Wurzel-Current-state
+ `docs/INDEX.md` Phase-8.5-Eintrag + `ROADMAP.md` Phase-8.5-Absatz waren seit dem A1-Commit
versehentlich nicht nachgezogen — Phase-eigene Hard-Rule-8-Erweiterung (INDEX-Zeile +
ROADMAP + Wurzel-Current-state im selben Commit) verlangt das eigentlich; INDEX-Bullet-
Lücke (`phase8_5_picker_release/CLAUDE.md` + `SESSIONS_ARCHIVE.md` fehlen komplett unter
„Phase 8.5 — 🔄 …") geht auf die Planungs-Commit-Widmung im Step-0-Block zurück („drei
INDEX-Zeilen … bereits durch den Nikinger angelegt" — die dritte Zeile fehlte real).
Auflösung in einem Folge-Commit mit INDEX-Trimmung. **`pytest` 959/959 unverändert**,
Tabu-Diff §0.3 leer (kein Code-Touch in beiden Commits), ui_budget 5/5 (127.6 KB nach A1
+1.8 KB), `node --check` grün auf dialogs.js/editor.js/app.js, Service-Touch 0 (PID 195922,
ActiveEnterTimestamp 2026-09-02 11:51:57 CEST — nur gelesen). Nächster Schritt: A2
(Tastaturnavigation + CSS-Block-Entdopplung am Picker, `app.js` tabu).

**[2026-09-04] Phase 8.5 — 🔄 A2 committet, 🟡, ⬜ B1 als Nächstes.** A2 (`aria-activedescendant`-
Tastaturnavigation + gemeinsamer Pick-Pfad `_pickLinkPickerAt` + CSS-Block-Entdopplung am
Picker) gebaut und committet (vollständiger Session-Block im Phase-Head, A1-Block nach
`SESSIONS_ARCHIVE.md` rotiert); `dialogs.js` neue Modul-Variablen `linkPickerItems`/
`linkPickerCursor`, neuer `_renderLinkPickerResults`-Aufbau mit State-Reset ganz oben,
neue Helper `_setLinkPickerCursor`/`_pickLinkPickerAt`, neuer keydown-Handler am
Suchfeld (ArrowDown/ArrowUp/Enter, kein Wrap, kein Home/End, kein Raten; Escape bleibt
beim globalen Handler); `app.css` zwei identische Auswahl-Blöcke zusammengezogen, totes
`:focus` raus; drei neue statische Tests in `test_static_routes.py`
(`test_link_picker_css_has_one_selection_block` P8.5-14, `test_link_picker_picks_run_
through_a_single_helper` P8.5-12, `test_insertAtCursor_defined_exactly_once_at_module_level`
P8.5-9 nachgezogen — A1 hatte diese drei statisch zu belegen zurückgestellt); Modul-Status
A2 `⬜` → `🟡`, Abnahmestand **3 ✅ · 3 🟡 · 14 ⬜ von 20**. **`pytest` 962/962** (959 + 3 neu,
keine Regressionen), Tabu-Diff §0.3 leer (kein `storage/`/`mcpserver/`/`security.py`/`api.py`/
`serializers.py`/`permissions.py`-Touch), ui_budget 5/5 (128.7 KB, +1.1 KB durch `dialogs.js`
11.7 → 12.6 KB), `node --check` grün auf `dialogs.js`, Service-Touch 0 (PID 195922,
ActiveEnterTimestamp 2026-09-02 11:51:57 CEST — nur gelesen). Nächster Schritt: B1
(`_TITLE_NOT_ID_HINT` generalisierend schärfen in `mcpserver/tools.py:159-164`, einzige
erlaubte Tabu-Ausnahme).

**[2026-09-05] Phase 8.5 — 🔄 D1 committet, 🟡, ⬜ D2–D5 als Nächstes.** Release-
Vorbereitung opencode/M3 (Hard Rule 8 im selben Commit): Badge `v3.0` → `v3.0.1` in
`phase5_ui/webui/static/app.html:20` (P8.5-N7, statisches HTML ist nicht im Tabu §0.3);
neuer `## 2026-09-05`-Block in `docs/UPDATE_LOG.md` mit drei menschenlesbaren Zeilen
(Picker-Modi, Tastatur, Generalisierter Hint). **Datums-Drift ausdrücklich dokumentiert:**
Block-C-Absatz von gestern hatte noch `## 2026-09-04` vorgeschlagen — heute ist
`date +%F`/`date -u +%F` = 2026-09-05, und `deploy.sh` Z. 117–131 verlangt strikt
`today_utc`/`today_local` als oberstes Datum, sonst Gate-Abbruch. Block-C-Block per Hand
nach `SESSIONS_ARCHIVE.md` rotiert (newest-first, vor B1); Skript
`scripts/rotate_session_block.sh` passt nicht auf das Phase-8.5-Muster mit einem
`## Session stopped`-Header + mehreren `### date`-Subblöcken (Skript zählt nur den
`## Session stopped`-Marker und sieht immer genau einen → Exit 2 „Bereits konform").
Modul-Status D `⬜` → `🟡` mit D2–D5 als Nikinger-Aktionen vermerkt. **`pytest` nicht
gelaufen** (kein Python-Touch), Tabu-Diff §0.3 leer (`app.html` und `docs/UPDATE_LOG.md`
nicht tabu), Service-Touch **0** (PID 195922 / ActiveEnterTimestamp 2026-09-02 11:51:57
CEST nur gelesen). **Nächster Schritt:** D2 — Deploy als **Nikinger-Aktion** (`sudo
systemctl ... deploy.sh main` in interaktiver Vordergrund-Shell, V103 prüft den
`sudo`-Prompt; Hard Rule 9 — niemals `sudo systemctl` durch opencode/M3), danach D3
Health-Gate 3/3 + V105, D4 Sichtprüfung am echten Gerät + P8.5-19-Abnahme, D5 Vierte
A3-Probe (entscheidet §9.4.1 Abbruchregel aus N2), Z Closeout.

**[2026-09-06] Phase 8.5 — 🔄 D4-Sichtprobe-Folgesession durch den Nikinger (Notiz-Session, kein Code-Touch in dieser opencode/M3-Session), ⬜ D5/V105 als Nächstes, dann Z.** Im
Anschluss an D4 hat der Nikinger mit Fabian **sieben neue Themen-Cluster** aus
der Sichtprobe gesammelt, die über den D4-Sichtprüfungs-Scope hinausgehen und in
**p8.X** gehören: §1 Spaces-Layout-Reorg [„Alle Items"-Leiste unter Spaces +
Kippschalter, Map 40 % Breite/volle Höhe, keine Duplikate]; §2 Obsidian-Map fünf
Sub-Punkte [Performance-Reload, Landkarten-Stil, Field schneidet ab, Reload-Drift,
Collapsible mit Abhängigkeiten]; §3 Anzahl-Anzeige Ordner; §4 Edit-in-Place-Vision
[„Bearbeiten"-Knopf überflüssig, Word-ähnlich im Read-View editieren — harter
Konflikt mit Hard Rule 3 „kein Last-Write-Wins" und P7-24-Reauth-Grant-Mid-Edit];
§5 Layering-Design-System [3 Layer: echtes Schwarz / aktueller Standard /
Liquid Glass + Selektion explizit blau auf Hover, Note-Select, Checkbox,
größter Brocken]; §6 „Konto"→„Einstellungen"-Rename + Positions-Tausch mit
Logout; §7 De-AI-ierung-Lauf 2 [nach **neuen** Kriterien, dann positive
Erstellungs-Regeln]. **Neue Datei `docs/concepts/p8x_ui_polish_notes.md`** (L2,
25 KB, 2026-09-06) sammelt alle 16 Themen — fünf bereits in D4 dokumentierte
p8.X-Punkte + die sieben neuen Cluster + vier Sub-Punkte aus §2; Anhang §A–§E
(D4-Duplikat-Verweise, klare Außenkanten, sechs offene Fragen für die
Planungs-Session, Namens-Konvention, chronologische Tabelle). **Bewusst kein
Plan, kein Locking, keine Tabu-Aufhebung** — Sammlung, Strukturierung, kein
Phase-8.5-Scope-Touch. Doku-Updates im selben Zyklus: `phase8_5_picker_release/
CLAUDE.md` aktiver Block auf Folgesession umgestellt, D4-Block nach
`SESSIONS_ARCHIVE.md` rotiert; `docs/INDEX.md` neue Sektion „## Phase 8.X" +
Phase-8.5-Header-Hinweis; `ROADMAP.md` neue Sektion + Tabellen-Zeilen P8.5 + P8.X
(korrigiert); `phase8_ui_graph_plan.md §9.4.7` Anker auf neue Notizen-Datei
(folgt); pytest nicht gelaufen (kein Python-Touch), Tabu-Diff §0.3 leer,
Service-Touch 0 (letzter Stand 2026-09-05 16:10:18 CEST / PID 355956,
Hard Rule 9 + §0.5.7 — diese Session ist reine Doku, kein `sudo systemctl`).
**Nächster Schritt:** D5 (Vierte A3-Probe, Nikinger, entscheidet §9.4.1
Abbruchregel) + V105 (Connector-Check, Nikinger); optional vor Z durch
opencode/M3: Radiogruppe-Tausch + Bracket-Fix, damit Z die Endabnahme-Zeilen
P8.5-6 + P8.5-19 auf ✅ heben kann; dann Z (Phase-8.5-Closeout) mit
Phase-8-✅-Nachtrag + p8.X-Ankündigung, jetzt mit Verweis auf
`docs/concepts/p8x_ui_polish_notes.md` als Wahrheits-Quelle.

**Größenstand am Session-Ende (Ist-Werte, Notiz für die nächste Session /
für Z):** `CLAUDE.md` (Wurzel) **55.014 B** (+7.015 B durch diese Session,
deutlich über dem 40-KB-Softcap, signifikantes Wachstum — Wurzel-CLAUDE.md
näher am 56-KB als am 40-KB-Cap, Auflösung bleibt eine Phase-8-Z-Entscheidung
aus Z wie schon D3 dokumentiert hat); `ROADMAP.md` 43.819 B (neu über dem
Softcap, erstmals so notiert, **+1.406 B** durch neue Phase-8.X-Sektion + zwei
Tabellenzeilen); `docs/INDEX.md` 49.556 B (war schon über Cap, **+4.772 B**
durch neue Phase-8.X-Sektion + L0-Zeile); `docs/concepts/p8x_ui_polish_notes.md`
neu, 25.489 B; `phase8_5_picker_release/CLAUDE.md` 39.679 B (**knapp unter
Cap**, +1.641 B); `phase8_5_picker_release/SESSIONS_ARCHIVE.md` 75.330 B (L3,
exempt). **Kein** stilles Trimming — Pattern wie schon D3/D4: dokumentieren,
nicht kürzen; Auflösung ist Z-Arbeit.

**[2026-09-06] Phase 8.5 — 🔄 D4 Sichtprüfung am echten Gerät durch den Nikinger, alles nur dokumentiert, ⬜ D5/V105 als Nächstes, dann Z.** Block 1–7 + Vorbereitung komplett durchgelaufen, beide Accounts in Firefox+Chrome+Safari; Update-Banner `## 2026-09-05` mit drei Zeilen sichtbar ✅, beide Picker-Modi funktional ✅ (eigenes `localStorage["sfx:linkpicker:mode"]` bestätigt), Tastaturnavigation geht über die Mindestanforderung Chromium+Firefox hinaus, Insert-at-cursor-Hub Bild-Knopf ✅, Settle-Zeit 2 s unter 3 s-Ziel, alle drei Graph-Farben, Knotenklick öffnet das Item, Conflict-Dialog gegen Speicherbutton-Spam bewährt (Hard Rule 3 „kein Last-Write-Wins" hält). **Drei echte Findings — Scope-Entscheidungen alle in dieser Session getroffen, Fixe in Folge-Sessions:** (1) **P8.5-19 Radiogruppe statt `<select>`** — Nikinger-Präferenz „deutlich angenehmer", P8.5-F-Planer-Substitution raus, Tausch 5 Z. in `dialogs.js:584`+`app.html:277` ausstehend, Lucide-Icons `link-2`+`pilcrow`/`text-cursor-input` als Vorschlag offen; (2) **P8.5-6 Bracket-Renderer-Bug** — Source-Escape `\[`/`\]` korrekt im Body, aber `markdown.js`-Link-Parser bricht in Vorschau (eckige Klammern ja, runde nein), §0.3 erlaubt `webui/static/js/`, Hard-Rule-9-Eskalation greift nicht (Ursache liegt genau im Fix-Pfad), Fix-Pfad vor Z; (3) **UX-2-Step-Knotenklick** — neues Feature „erster Klick Readonly-Vorschau, zweiter Klick vollständig" für p8.X parkiert, Fabi sammelt gerade. Drei Parken-bestätigt (vom D3-Handover übernommen): Map-Field schneidet unten ab, Map fliegt bei jedem Reload, Save-Button-YAML-Header-Issue (wahrscheinlich p8.X, Verifikation ob außerhalb Header-Kontext steht aus). **Phase 8 ✅ + p8.X als Folge-Phase** als Nikinger-Entscheidung für Z vorgemerkt. Modul-Status Zeile 6 Block D jetzt D1 ✅ + D2 ✅ + D3 ✅ + D4 ✅, D5 ⬜ + V105 ⬜ weiter Nikinger; P8.5-6 mit Bracket-Caveat, P8.5-17 Update-Banner-Teil ✅; Summary 3 ✅ · 14 🟡 · 3 ⬜. D3-Block per Hand nach `phase8_5_picker_release/SESSIONS_ARCHIVE.md` rotiert (Skript passt nicht auf Phase-8.5-Muster). **Nächster Schritt:** D5 (Vierte A3-Probe, Nikinger, entscheidet §9.4.1 Abbruchregel) + V105 (Connector-Check, Nikinger); optional vor Z durch opencode/M3: Radiogruppe-Tausch + Bracket-Fix, damit Z die Endabnahme-Zeilen auf ✅ heben kann; dann Z (Phase-8.5-Closeout) mit `phase8_ui_graph_plan.md §9` + Phase-8-✅-Nachtrag.

**[2026-09-05] Phase 8.5 — 🔄 D2 vom Nikinger zwischen D1 und D3 + D3-Prep, 🟡, ⬜ D4/D5/V105/Z als Nächstes.** D2 ist **zwischen D1 (Commit heute früh) und D3 (diese Session) still durch den Nikinger gelaufen** — Entdeckung kam erst beim ersten Probe-Lauf des Health-Gate-Skripts: `/opt/sharefyx/current` → `20260905T140325.378914Z` → HEAD `6f19a8f` (D1), Service-PID **355956** (statt der im D1-Block notierten 195922 — D2-Deploy hat den Dienst erwartungsgemäß neu gestartet), `ExecMainStartTimestamp=2026-09-05 16:10:18 CEST`. Damit ist D3 nicht mehr Vorbereitung, sondern **Verifikation des bereits deployten v3.0.1**. Neu gebaut: `phase8_5_picker_release/scripts/health_gate.sh` (134 Zeilen bash, `set -uo pipefail`, JSON auf stdout / Details auf stderr nach Hard Rule 7), acht Gates — `/health` 200 mit Retry-Loop, `/ui/login` 200, `/api/v1/me` 401, `/mcp/` 401, `.rail__version` aus `/ui/static/app.html` (**nicht** `/ui/login` — `pages.py`s Auth-Template ohne Rail, erste Iteration fiel darauf herein, gefixt), `/opt/sharefyx/current` → Release mit `.git`, optional `--require-todays-update-log` (UTC/local wie `deploy.sh` Z. 127-131), optional `--expected-sha=<hex>` (Short- oder Full-Form per Prefix-Vergleich). **Lauf-Beleg 2026-09-05 15:19:53Z** mit `--require-todays-update-log --expected-sha=6f19a8f`: **8/8 grün**, Exit 0, JSON auf stdout (`result:"ok"`, `actual_version:"v3.0.1"`, `release_sha:"6f19a8f..."`, `active_release:"/opt/sharefyx/releases/20260905T140325.378914Z"`, `port:8765`). Drei Negativproben separat verifiziert (Port 9999 → Gate 1 rot, `--expected-version=v9.9.9` → Gate 5 rot, `--expected-sha=0000000` → Gate 8 rot). **P8.5-17 teilweise abgehakt:** Deploy gelaufen ✅, Health-Gate 8/8 ✅, Badge `v3.0.1` live ✅, Update-Banner-Live-Anzeige ⬜ (braucht Auth, Nikinger), V105 ⬜ (echter Anthropic-Connector, Nikinger). Modul-Status-Zeile 6 Block D um D2 ✅ + D3 🟡 erweitert; Abnahmestand-Zeile P8.5-17 Health-Gate-Teil 🟡; Summary **3 ✅ · 14 🟡 · 3 ⬜ von 20**; D1-Block (111 Zeilen) per Hand nach `SESSIONS_ARCHIVE.md` rotiert (Skript passt nicht auf das Phase-8.5-Muster — bewährtes Vorgehen aus D1 selbst). `pytest` nicht gelaufen (kein Python-Touch), `bash -n` OK, shellcheck nicht verfügbar (übersprungen, keine Konvention im Repo), Tabu-Diff §0.3 leer, Service-Touch 0 (PID 355956 nur gelesen). **Nächster Schritt:** D4 — Sichtprüfung am echten Gerät durch den Nikinger (`## 2026-09-05`-Eintrag im Update-Banner sichtbar, `<select class="input" id="link-picker-mode">` im Picker vorhanden — P8.5-19-Abnahme: Radiogruppe oder `<select>`-Bestätigung), D5 Vierte A3-Probe (entscheidet §9.4.1 Abbruchregel aus N2), V105-Connector-Check, Z Closeout.

**[2026-09-04] Phase 8.5 — 🔄 Block C committet, 🟡, ⬜ Block D + Z als Nächstes.** Voller
v3-Vorabritt (Plan §4) gegen eine Wegwerf-Instanz auf Port 18773 gefahren:
`phase8_5_picker_release/scripts/wegwerf_setup_v3ritt.py` (Wegwerf-Setup mit Standing-
Permission-Muster aus Phase 8: eigener Port, tmp-`DATA_ROOT`/tmp-`auth.sqlite3`/File-
Keyring; 30 Items über drei Spaces — 12 alpha + 10 beta + 8 gamma; ein archiviertes
Item, ein Item mit item-level `share_read=["gamma"]` (Deploy-Blocker-Fall aus P6 §35–
39), ein Item mit Bild-Asset (`ast_351d4217` per `put_asset()`); 11 explizite Kanten,
darunter die für V102 präparierte Zwillings-Kante body+frontmatter zwischen
`alpha:Buecherliste Q4` und `alpha:Empfehlungen Nikinger`); 16 Screenshots
`docs/screenshots/v3ritt_{chromium,firefox}_NN_*.png`. **`v3_ritt_playwright_smoke.py`:
13/13 Stationen grün in Chromium UND Firefox — 26/26 gesamt** (V101 beantwortet für beide
Browser). Drei **echte Befunde**, keine Code-Fixes im Tabu-Bereich nötig:
- **Smoke-Bug** (gefixt in dieser Session): Edge-Keys waren `src`/`dst` (konsistent mit
  `graph.js:325/394`), nicht `src_id`/`dst_id` wie im Smoke angenommen; ist beim
  V102-Vergleich aufgefallen, Smoke korrigiert, **kein Server-Bug**.
- **CSRF-Origin-Mismatch** zwischen Wegwerf-UI (`http://127.0.0.1:18773`) und
  konfiguriertem `SPACE_PUBLIC_BASE_URL` (`https://wegwerf-v3ritt.invalid`); `_validate_base_url`
  erzwingt https. Konsequenz: jeder `fetch()` mit POST/PATCH aus dem Browser-Kontext
  wird abgewiesen, das macht Station 13 (P8-1-Reauth-Grant-Mechanismus) im Wegwerf
  unscharf — der Live-Nikinger-Domain-Test in Block D fängt das auf. **Befund für
  Step Z / Plan-§4.C3.**
- **Pickstation 12 nur strukturell** (`@media (prefers-reduced-motion)` als Regel im
  CSS gefunden, aber keine echte Browser-Probe mit umgeschaltetem UA). War schon in
  Phase 8 `p8_22_smoke.py` throwaway-verifiziert (Fix A, 2,7 s statt 5,95 s); bleibt
  so.
- Modus-Selektor `<select>` vs. N3-Vorschau-`<input type="radio">`: **nicht als Befund
  behandelt** — die N3-Entscheidung war „Umschalter im Dialog" (P8.5-E), die Bauform
  `<select>` ist eine Planer-Substitution (P8.5-F), die der Nikinger in Block D4 am
  echten Gerät abnimmt (Abnahmezeile P8.5-19). Modul-Status C `⬜` → `🟡`, Abnahme-
  stand **3 ✅ · 13 🟡 · 4 ⬜ von 20** (P8.5-5, -6, -7, -8, -10, -11, -13, -15, -16 alle
  `⬜` → `🟡`; P8.5-3 bleibt `🟡` mit Klammer-Anmerkung für Live-D5). **`pytest` 962/962**
  unverändert (kein Python-Touch im Block-C-Setup, kein `phase5_ui/webui/`-Touch im
  Smoke), Tabu-Diff §0.3 leer, Wegwerf sauber abgebaut (`kill -TERM $(cat serve.pid)`,
  Hard Rule 9-konform), Produktion nachweislich unangetastet (PID 195922 / ActiveEnter
  2026-09-02 11:51:57 CEST vor/nach identisch). Nächster Schritt: **Block D** —
  Release-Vorbereitung (`.rail__version` `v3.0` → `v3.0.1`, neuer `## 2026-09-04`-Block
  in `docs/UPDATE_LOG.md`, drei Zeilen menschenlesbar zum Phase-8.5-Deploy), D2 Deploy
  als **Nikinger-Aktion** (Hard Rule 9 + P8.5-Q, niemals `sudo systemctl restart
  sharefyx-mcp` durch opencode/M3), D3 Health-Gate, D4 Sichtprüfung am echten Gerät,
  D5 Vierte A3-Probe (an der die Abbruchregel §9.4.1 fällt oder hält).

**[2026-09-04] Phase 8.5 — 🔄 B1 committet, 🟡, ⬜ Block C als Nächstes.** B1 (Hint generalisierend

**[2026-09-01] Phase 8 — 🔄 Block A + B ✅ live-verifiziert, Gate B→C bestanden.** UI-Neuanstrich v3,
Verknüpfungs-Graph (`GET /api/v1/graph` + `item_links`-Tabelle + `linkscan.py` + UI-Wiring), drei
P7-Erbposten (P7-24 Reauth-Grant ✅, `remove-space`-Auto-Reindex ✅, P7-4 Zweitprobe 🟡 mit
benanntem Restdefekt Klammer/Aufzählung). Plan: `docs/concepts/phase8_ui_graph_plan.md` (N1–N12
gelockt, P8-A–P8-Q, Abnahme P8-1–P8-24, `[VERIFY]` V81–V92). Kernentscheidungen: P7-24-Fix als
**Reauth-Grant** (vierte Option, in der Planung gefunden — kein Aufweichen des Anti-Replay),
**achte P1-Contract-Öffnung benannt** (Link-Extraktion beim Indexieren für den Graphen), Design
v3 (IBM Plex, Lucide-Sprite, Farblegende own/shared/foreign, Glass-Akzente mit Fallback).
**Ausführung erstmals opencode/M3, ohne Advisor-Stufe (N12)** — Ersatz: Plan §0.6 +
zwei Nikinger-Sichtprüfpunkte. Closeout wird §9 des Plans (ein Dokument pro Phase, P8-N).
**Gate B→C (2026-09-01)** alle vier Bedingungen grün: 958/958 pytest, Charakterisierung
byte-identisch, Tabu-Diff leer, `_graph_get` manuell gegen 3 Spaces + 12 ACL-Fälle 12/12,
Playwright-Smoke gegen Wegwerf-Instanz 18/18 (Picker + `#item/`-Navigation).
**Nächster Schritt:** Block C (Design-Fundament v3, Plan §4) — C0 Anti-AI-Research →
C1 Plex → C2 Lucide → C3 Farbsemantik → C4 Glass → C5 Dichte.

**[2026-08-28] Phase 8 geplant — ⬜ nicht gestartet.** UI-Neuanstrich v3, Verknüpfungs-Graph,
drei P7-Erbposten. Plan: `docs/concepts/phase8_ui_graph_plan.md` (N1–N12 gelockt, P8-A–P8-Q,
Abnahme P8-1–P8-24, `[VERIFY]` V81–V92). Kernentscheidungen: P7-24-Fix als **Reauth-Grant**
(vierte Option, in der Planung gefunden — kein Aufweichen des Anti-Replay), **achte
P1-Contract-Öffnung benannt** (Link-Extraktion beim Indexieren für den Graphen), Design v3
(IBM Plex, Lucide-Sprite, Farblegende own/shared/foreign, Glass-Akzente mit Fallback).
**Ausführung erstmals opencode/M3, ohne Advisor-Stufe (N12)** — Ersatz: Plan §0.6 +
zwei Nikinger-Sichtprüfpunkte. Closeout wird §9 des Plans (ein Dokument pro Phase, P8-N).

**[2026-08-28] Phase 7 abgeschlossen — ✅ live-verifiziert.** Space-Verwaltung in der
Weboberfläche, Mehrfachauswahl, Konsolidierung (`phase7_spaces_admin/`, kein eigenes Python-Paket)
sind gebaut, live deployt (`main`@`e88a624`, 2026-08-27) und abgenommen. **Abnahmestand: 22 von 24
Zeilen ✅, 2 ❌, 0 ungeprüft** — die Matrix ist vollständig durchgelaufen; das unterscheidet diese
Phase von P6/P6.5, wo Zeilen ungeprüft blieben. **Der Sprung auf ✅ ist eine Nikinger-Entscheidung
vom 2026-08-28** unter der Bedingung, dass die beiden ❌ als benannte Defekte an Phase 8 vererbt
werden: **P7-24** (`list.js :: moveSelectedItems()` reicht denselben TOTP-Code an jedes
sequenzielle PATCH einer Batch-Runde — der Server lehnt den Replay korrekt ab, ein Batch mit N
rechteerweiternden Items braucht real N Codes statt einem; echter Mechanismus-Defekt, Fix
bewusst in P8) und **P7-4** (Claude nennt Menschen gegenüber IDs statt Titeln, trotz der Anweisung
in vier Tool-Beschreibungen — kein Code-Fehler). **Dritter Erbposten aus dem Live-Betrieb:
`spacectl.py remove-space` reindiziert den SQLite-Index nicht** — der Incident vom 2026-08-27
(`GET /api/v1/overview` → 500 für jeden eingeloggten Nutzer) kam genau daher; der Zustand ist
per `space_cli.py reindex` behoben, die Ursache nicht. Sechste und siebte P1-Contract-Öffnung mit
dieser Phase geschlossen, keine achte angekündigt. **Einstiegsdokument für die Phase-8-Planung:
`docs/concepts/PHASE7_CLOSEOUT_HANDOVER.md`** (dort §4 die offenen Entscheidungen, §7 die
geänderte Arbeitsweise: Claude Code plant, opencode/M3 führt aus). Übersichtsgrafik:
`docs/concepts/phase7_spaces_admin_uebersicht.svg`. **Die folgenden Absätze bleiben als
Verlaufsdokumentation stehen.**

**[2026-08-23] Phase 7 aktiv — Space-Verwaltung, Mehrfachauswahl, Konsolidierung**
(`phase7_spaces_admin/`, kein eigenes Python-Paket) — **🔄, Block A weit fortgeschritten.** Step 0
(Haushalt + Doku-Audit) ✅, danach A1/A2 (Item-ID sichtbar+auffindbar)/A3 (Bild-Entfernen-Knopf,
schließt P6.5-12)/A4 (Feld-Whitelist, schließt O6) gebaut, A5 (Sichtbarkeits-Migration) live
`--apply` gefahren, A7/A7b (dritter Principal `testnutzer-p7` + `testcred.py`) live angelegt,
**A8 (formaler Abschluss Phase 6.5) durchgeführt** — siehe unten. Verbleibend in Block A: A6
(Purge-Gate, kalendarisch frühestens 2026-08-28). Plan: `docs/concepts/
phase7_spaces_admin_plan.md` (Entscheidungen P7-A–P7-W, alle zehn Nikinger-Fragen N1–N10 gelockt
in §0.1). Phase-Head: `phase7_spaces_admin/CLAUDE.md`.

**[2026-08-27 Korrektur]** Der Absatz oben blieb seit dem Phasenstart stehen und ist überholt.
**Phase 7 ist inhaltlich vollständig** — Block A (inkl. A8, Phase 6.5 formal abgeschlossen),
Gate A→C, Block C (C1–C5, Space-Verwaltung in der Weboberfläche) und Block B (Mehrfachauswahl,
`ITEM_MOVE_PLAN.md` §9) sind alle gebaut. **Live deployt, 2026-08-27, Nikinger-Lauf:**
`/opt/sharefyx/current` → `e88a6244d8eebb5d08d1d93c4a2725f84a2f5971`, Health-Gate 3/3 grün
(`/ui/login`→200, `/api/v1/me`→401, `/mcp/`→401 — alle drei die erwarteten Antworten, kein
Fehlschlag). **[2026-08-28 Korrektur]** Abnahmezeilen 31–34 (`ITEM_MOVE_PLAN.md` §9.5) sind seither
vom Nikinger selbst live gegen die echte Instanz bestätigt — 32/33/34 ohne Vorbehalt, 31 mit dem
bereits bekannten P7-24-TOTP-Vorbehalt (kein neuer Fund, Fix in der nächsten Phase). **A6
(Purge-Gate/P7-9) ebenfalls gefahren** — `token_families` 35→31, `clients` unverändert 54 wie
erwartet (90-Tage-Fenster erst 2026-10-27). **Kein offener Test/Gate mehr.** Verbleibend: Step Z
Rest (Phase-7-Closeout-Dokumente, Übersichtsgrafik, Rotationsprüfung). **Noch nicht ✅** — „✅
heißt live-verifiziert, nicht gebaut", der formale Sprung folgt erst mit dem Closeout. Details:
`phase7_spaces_admin/CLAUDE.md`, aktueller Session-Block.

**[2026-08-23, P7 Step A8] Phase 6.5 formal abgeschlossen als 🟡 — code-complete und live
deployt, aber NICHT vollständig live-verifiziert.** Bewusst **nicht** ✅: **12 von 14
Abnahmezeilen** live, davon zwei (P6.5-8/13) über eine im P7-Plan §A8.1 gebilligte Substitution
— `testnutzer-p7` statt Fabian, derselbe serverseitige Rechte-Code-Pfad. Verbleibend offen:
P6.5-12 (Entfernen-Knopf jetzt von P7 Step A3 gebaut, kein Browser-Klick-Nachweis) und P6.5-14
(Nikingers eigene Bewertung, kein Selbstzertifizierungs-Kriterium — bleibt strukturell offen).
Handover: `docs/concepts/PHASE6_5_CLOSEOUT_HANDOVER.md`. Übersichtsgrafik:
`docs/concepts/phase6_5_tools_images_uebersicht.svg`. **Der untenstehende Absatz vom
Phasenstart (2026-08-20) bleibt als Verlaufsdokumentation stehen, ist inzwischen überholt.**

**[2026-08-20] Zweite aktive Phase gestartet: Phase 6.5 — Werkzeug-Ergonomie und Bilder**
(`phase6_5_tools_images/`, kein eigenes Python-Paket) — **🔄 Step 0.** Sitzt bewusst zwischen der
noch laufenden Phase 6 und der reservierten Phase 7 (Space-Admin-UI, `app.html` unverändert).
Deckt die fünf noch offenen MCP-Werkzeug-Ergonomie-Punkte (siehe „Noch nicht entschieden" unten —
**jetzt geplant, nicht mehr offen**) und den Abschluss von Block C Bilder ab (löst
`phase6_shares/IMAGES_PLAN.md` als maßgebliche Quelle ab). Plan: `docs/concepts/
phase6_5_tools_images_plan.md` (Entscheidungen P6.5-A–P6.5-V, alle sechs Nikinger-Fragen N1–N6
gelockt in §0.0). Phase-Head: `phase6_5_tools_images/CLAUDE.md`.

**[2026-08-23] Phase 6 abgeschlossen als 🟡 — code-complete und live deployt, aber NICHT
vollständig live-verifiziert.** Bewusst **nicht** ✅: nur **12 von 39 Abnahmezeilen** sind
live-verifiziert, vier (31–34, §9 Mehrfachauswahl) wurden nie gebaut, Block C ist nach Phase 6.5
ausgewandert, sieben Zeilen hängen an einer Sitzung mit Fabians eigenem Login. Es gibt bewusst
**kein** `P6_ABNAHME_<datum>.md` — der Zeilenstatus steht in
`docs/concepts/PHASE6_CLOSEOUT_HANDOVER.md` §3. **Der Sprung auf ✅ ist eine offene
Nikinger-Entscheidung.** Zwei Aufgaben sind vom Nikinger ausdrücklich für die nächste Phase
benannt: (1) **Doku-Audit** der Modul-Status-Zeilen 8–16 in `phase6_shares/CLAUDE.md`, die noch
„gebaut, noch nicht deployt" tragen — vermutlich stale, wie sich am 2026-08-23 schon für die
globale Suche zeigte, aber **zu prüfen, nicht zu raten**; (2) **kein Entfernen-Knopf für Bilder**
in `phase5_ui/webui/static/js/editor.js`, obwohl N5 gelockt ist und der `DELETE`-Endpunkt
existiert (blockiert P6.5-12). Übersichtsgrafik: `docs/concepts/phase6_shares_uebersicht.svg`.
**Phase 6.5 ist davon unberührt und läuft weiter.** Der folgende Absatz bleibt als
Verlaufsdokumentation stehen.

**Phase 6 — Freigaben, Ordner, Werkzeug-Ergonomie** (`phase6_shares/`, kein
eigenes Python-Paket) — **offen/Kompakt:** Phase 6 abgeschlossen als `phase6_shares/CLAUDE.md`.
Verlaufsdokumentation zweier Blöcke (Block A Werkzeuge/Betrieb/Update-Banner, Block B
Dateisystem mit SharePolicy-Cutover; Block C Bilder nach 6.5 ausgewandert) ist dort —
Steps 0–3 (patch_item, ua-Feld, Update-Log-Banner) gebaut, Steps 4–6 (Storage-Fundament +
Rechtepolitik + Verwaltung) 2026-08-13 live deployed (`main`@`d068d1c`), IT-Sekus-UI-Fund
(writable-Badge + acht `ownSpaceActive()` zu `activeSpaceWritable()`) geschlossen,
Closeout-Handover `docs/concepts/PHASE6_CLOSEOUT_HANDOVER.md` mit 12-von-39-Live-Bilanz.
**Hard Rule 8:** Phase-6-/6.5-/7-Block-Detailnarrative werden hier nicht mehr dupliziert —
maßgebliche Quelle: die jeweilige `phase*/CLAUDE.md`.

**Deploy-Blocker (2026-08-18) + Funnel-Recovery (2026-08-19) — kompakt:**
Der 2026-08-18 entdeckte UI-Fund („kein über-alle-lesbaren-Items-Suchmodus", item-level-only
`share_*` über Web-UI unauffindbar, nur Connector-Zugriff) wurde 2026-08-19 geplant
(`phase6_shares/GLOBAL_SEARCH_PLAN.md`, P6-AO–AT; Q1: Titel/Tags-only, kein Body-Fulltext) —
Kernbefund im Code verifiziert: `GET /api/v1/items` *ohne* `space`-Parameter ist bereits die
globale, item-weise ACL-gefilterte Suche, es fehlte nur die UI-Fläche (kein neuer
Endpunkt). Steps G1–G2 gebaut (Playwright 10/10 gegen Wegwerf, Advisor-Fund
`editor.js :: clearDetail()` Scope-Reset mitgefixt), `d348e2e` 2026-08-23 zu `f96125e`
korrigiert (Closeout-Sweep) und live deployt. Der 2026-08-19-Funnel-Reboot-Fund (`tailscaled`-
Restart nach VM-Reboot, MagicDNS hatte den öffentlichen Pfad verdeckt) hat
`diagnose.sh`-Prüfung 5 korrigiert; Watchdog/Selbstheilung bewusst offen. Volle
Herleitung beider Punkte: `phase6_shares/CLAUDE.md` Session-Block 2026-08-23 bzw.
`phase3_edge/CLAUDE.md` Abschnitt 2026-08-19.

**[2026-08-19] Block C (Bilder) ist geplant:** `phase6_shares/IMAGES_PLAN.md` (Entscheidungen
**P6-AU–P6-BB**, Abnahmezeilen 40–47) — **fünf offene Nikinger-Entscheidungen B1–B5** (Binärblobs
in der Git-Historie des `DATA_ROOT` vs. Hard Rule 5, Größenriegel, Bildbytes fremder Items vor
einem sehenden Modell als Injektionskanal, den `<untrusted_content>` strukturell nicht erreicht,
MCP-Upload, Löschen eines Bildes vs. Entscheidung H/„kein Delete im Kern-API"). Vor dem Bau
einzuholen, nicht von Claude zu entscheiden.

**Phase 5 — Web-UI, REST-API und Auth-Selbstverwaltung** (`phase5_ui/`, Paket `webui`) — **✅
abgeschlossen, 2026-08-09 — 20/20 Abnahmezeilen live bestanden, 0 teilweise, 0 offen.** Zwei
Blöcke (A = Sicherheit + Auth-Selbstverwaltung, B = REST-API + UI) mit hartem Gate dazwischen,
beide durchlaufen. Menschen setzen ihr Passwort jetzt selbst im Browser, ohne SSH und ohne
Neustart (schließt Betriebsnotiz O1 auch live). Cutover auf `/opt/sharefyx/current` seit
2026-08-05, `deploy.sh`-Zyklus läuft. `git diff` auf `storage/`,
`mcpserver/{tools,permissions,server}.py` blieb über die gesamte Phase leer (Kriterium 18) —
derselbe Seam-Beweis wie in Phase 4, eine API-Fläche höher.

Vollständige Matrix, Modul-Status je Step und die gesamte Live-Debugging-Historie (u. a. der
Origin/CSRF-Fund am Block-A-Gate, die Step-7b-Revision von Plan §4.1/§4.3, Sicherheitsbefund S9)
stehen in `phase5_ui/CLAUDE.md` — read + newest Session-stopped-Block first, das ist die
maßgebliche Quelle für diese Phase, nicht diese Zeile hier. Ältere Session-Blöcke:
`phase5_ui/SESSIONS_ARCHIVE.md`.

Plan: `docs/concepts/phase5_ui_plan.md` (Entscheidungen P5-A–P5-AE, Steps 0–9). Herkunft/offene
Entscheidungen: `docs/concepts/PHASE4_CLOSEOUT_HANDOVER.md`. Abnahmeprotokoll:
`docs/concepts/P5_ABNAHME_2026-08-09.md`. Formaler Abschluss-Handover an P6:
`docs/concepts/PHASE5_CLOSEOUT_HANDOVER.md`.

**[2026-08-09 erledigt]** Vor-Phase-6-Vormerkungen F1 (Subspaces/Shared Spaces), F2 (kein Löschen, nur Archivieren), Client-Surface-Logging (ua-Feld), `patch_item` (gezielter Patch statt Volltext-Rewrite) sind alle in Phase 6 gelandet (`phase6_shares_plan.md`: F1 zu P6-J/K/Q/T, F2 zu §0.5 weiterhin draußen, Logging zu P6-A5/Step 2, `patch_item` zu P6-E/F/G/Step 1, gebaut als siebtes MCP-Tool 2026-08-09). F1b (Space, in dem alle unabhängig volle Rechte haben) bleibt wegen Hard Rule 4 bewusst draußen. Volltext: `phase6_shares/CLAUDE.md` Vormerkungen-Abschnitt.

**Phase 4 — OAuth 2.1 + DCR** (`phase4_auth/`, Paket `authserver`) — **✅ abgeschlossen,
2026-07-30 — 16/16 Abnahmezeilen live bestanden, Schnitt vollzogen.** Der Pfad-Token ist
verschwunden; ein eigener, im selben Prozess laufender Authorization Server (Discovery, Dynamic
Client Registration, PKCE, Argon2id + TOTP, opake rotierende Token) authentifiziert seither jeden
Connector. Kritischer Fund in Step 0: ein nie widerrufener Keyring-Token für einen seit P2
umbenannten dritten Space (`nikinger`) — live und schreibfähig, aber ohne zugehöriges
Verzeichnis; noch vor dem Schnitt widerrufen und live gegen `diagnose.sh`/
`export_space_map.py` bestätigt (Details: `docs/concepts/PHASE3_CLOSEOUT_HANDOVER.md` §5).

Sicherheitsbefunde **S1–S10 / O1–O2** (S1–S8 und S10 geschlossen; O1 strukturell durch P5
geschlossen; **O2 offen** — `clients`/`token_families` werden nie abgeräumt) stehen mit vollem
Verlauf und Fundstellen in `phase4_auth/CLAUDE.md`, ebenso der Modul-Status aller acht Steps und
das ausgeführte Inbetriebnahme-Runbook.

Plan: `docs/concepts/phase4_auth_plan.md` (Entscheidungen P4-A–P4-R, Steps 0–7 — geschrieben ohne
frischen Repo-Zugriff, siehe Plan-Kopf). Herkunft/offene Entscheidungen:
`docs/concepts/PHASE3_CLOSEOUT_HANDOVER.md`. Abnahmeprotokoll:
`docs/concepts/P4_ABNAHME_2026-07-29.md`. Sicherheits-Review vor der Abnahme:
`docs/concepts/P4_SECURITY_REVIEW_2026-07-29.md`. Formaler Abschluss-Handover an P5:
`docs/concepts/PHASE4_CLOSEOUT_HANDOVER.md`.

**Phase 3 — Exposure & Betrieb** (`phase3_edge/`, kein eigenes Python-Paket — Servercode bleibt
in `mcpserver`): ✅ **live-verifiziert, 13/13** — Ursprungsstand 10/13
(`docs/concepts/P3_ABNAHME_2026-07-27.md`). Zeile 6 (Reboot) löste sich am 2026-07-29 durch
einen unbeabsichtigten Reboot der VM (Windows-Host-Neustart des Nikingers), Zeile 12
(Backup-Timer-Lauf) durch einen realen Timer-Lauf in P4 Step 0. **[2026-08-02, P5 Step 0:]**
Zeile 13 (Restore-Nachweis) ist die letzte gefallen — Claude Code fuhr `restore_check.sh`
zunächst selbst als Kandidatenbeleg, der Nikinger führte denselben Lauf danach selbst aus
(identischer HEAD, `ok:true`) — echte Abnahme. **Phase 3 damit vollständig ✅.** Formaler
Abschluss-Handover an P4: `docs/concepts/PHASE3_CLOSEOUT_HANDOVER.md`. Plan: `docs/concepts/
phase3_edge_plan.md` (Entscheidungen P3-A–P3-N gelockt, Steps 0–7). Phase-Head:
`phase3_edge/CLAUDE.md`.

**Phase 2 — MCP-Server** (`phase2_mcp/`, Paket `mcpserver`): ✅ **abgeschlossen,
live-verifiziert seit 2026-07-26** — Quick-Tunnel-Probe + vollständige Adapter-Abnahme über den
echten Custom Connector durch den Nikinger, 21/21 Prüfungen, siehe
`docs/concepts/P2_ADAPTER_ABNAHME_2026-07-26.md`. Claude liest und schreibt über einen lokalen
`fastmcp`-Server auf den P1-Storage-Kern — Token→Space-Auflösung, sechs Tools,
`<untrusted_content>`-Wrapping fremder Bodies. Formaler Abschluss-Handover an P3:
`docs/concepts/PHASE2_CLOSEOUT_HANDOVER.md`. Plan: `docs/concepts/phase2_mcp_plan.md`
(Entscheidungen P2-A–P2-N, Steps 0–7). Phase-Head: `phase2_mcp/CLAUDE.md`.

**Phase 1 — Storage-Kern** (`phase1_storage/`, Paket `storage`): ✅ **abgeschlossen,
live-verifiziert.** Alle acht Module (Steps 0–7), 68 Tests grün (70 bei Phasenabschluss, minus
zwei bei Entfernung toten Codes in P2 Step 0 — siehe `phase1_storage/CLAUDE.md`) —
Frontmatter/Modelle, atomarer Datei-Store, SQLite-Index, Versionierung + Konfliktbehandlung,
Git-Commit je Write, Query-Layer, `space_cli.py` als Beweis. Der Nikinger hat den Lauf gegen den
echten `DATA_ROOT` (`/home/savefyx/savefyx-data`) selbst ausgeführt (2026-07-25, Hard Rule: kein
Test gegen den echten DATA_ROOT durch Claude Code). Details + Transkript:
`phase1_storage/CLAUDE.md`, Session-Block. Plan: `docs/concepts/phase1_storage_plan.md`
(Entscheidungen A–H gelockt, Steps 0–7). Die dort definierten Frontmatter-Felder und
`Store`-Signaturen sind ab jetzt Contract für P2 (drei einmalige, freigegebene Erweiterungen in
P2 Step 2 — siehe P2-Plan §0.4 Punkt L).

**Gelockte Rahmenentscheidungen (Nikinger, 2026-07-24, Browser-Planung):**

| # | Thema | Lock |
|---|---|---|
| R1 | Plan/Ausführung | Planung im Browser-Chat, Ausführung in Claude Code — wie im Trading-Bot-Projekt. |
| R2 | Plan-Tier | Beide Nutzer auf **Claude Pro**. Custom Connectors sind auf Pro verfügbar; jeder fügt seinen Connector selbst hinzu (kein Owner-Gate wie bei Team/Enterprise). `[VERIFY]` bei Ausführung gegen die aktuelle Doku. |
| R3 | Erreichbarkeit | **CGNAT** (RUT X50, Mobilfunk). Start mit **Cloudflare Tunnel** (schnellster Weg zum ersten Erlebnis), Migration auf **VPS + WireGuard** als P3-Option. Der MCP-Server ändert sich dabei nicht. **[2026-07-28 Ergänzung, P4 Step 0]:** Gebaut wurde stattdessen **Tailscale Funnel** (P3-A) — weder Cloudflare Tunnel noch VPS+WireGuard. Die Beschlusslage oben bleibt historisch korrekt stehen; Details zum tatsächlichen Weg: `docs/concepts/phase3_edge_plan.md` §0.4. |
| R4 | Vertraulichkeit | Bewusst akzeptiert: bei Cloudflare Tunnel terminiert Cloudflare TLS und sieht Klartext. **Kein E2E.** Der Server muss lesen können, damit Claude lesen kann — das schließt das Krypto-Modell des `Notizheft_example.html` aus. **[2026-07-27 Ergänzung, P3 Step 0]:** Ab P3 läuft der Weg über Tailscale Funnel; dort terminiert die Node selbst TLS, siehe `docs/concepts/phase3_edge_plan.md` §0.4. Der Relay-Betreiber sieht Notizinhalte damit nicht mehr im Klartext — „kein E2E" bleibt trotzdem richtig, denn Tailscale bleibt vertrauenswürdige Infrastruktur (Koordinationsserver, DNS, Relays). |
| R5 | Auth v0 | Token im Pfad (`/mcp/<token>`), Token = Identität = Space. Ehrlich benannter Kompromiss (Bearer-Passwort in einer URL, landet in Logs). **OAuth 2.1 + DCR ist Phase 4**, nicht optional-für-immer. **[2026-07-30 abgelöst, P4 Schnitt:]** Der Pfad-Token existiert nicht mehr — `TokenPathASGI` ist aus dem Code entfernt, beide Pfad-Token live widerrufen, `SPACE_AUTH_MODE` lässt nur noch `oauth` zu. Der Connector authentifiziert sich seither über OAuth 2.1 + DCR (Passwort + TOTP), siehe P4. |
| R6 | Zweck | **Lernprojekt**, später evtl. Arbeitswerkzeug. Bei Zielkonflikt gewinnt Lerneffekt über Bequemlichkeit — außer bei Safety/Secrets, dort gewinnt immer die sichere Variante. |

**Noch nicht entschieden (bewusst offen, für spätere Planungssessions):**
- ~~MCP-Werkzeug-Ergonomie, fünf offene Punkte~~ **[2026-08-20 geplant und gelockt]** — jetzt
  Block A von Phase 6.5 (`docs/concepts/phase6_5_tools_images_plan.md` §3, Entscheidungen
  P6.5-A–P6.5-H u. a.). Kein offener Planungsbedarf mehr — nur noch **nicht gebaut**. Der
  Absatz unten bleibt als Herkunftsnachweis stehen.
- ~~Item-Verschieben zwischen Ordnern und Spaces~~ **[2026-08-17 geplant und gelockt]** —
  `phase6_shares/ITEM_MOVE_PLAN.md` §4 (Step 7b, Space-Move, Entscheidungen P6-AD–AJ) + §9
  (Mehrfachauswahl, P6-AK–AN) sind ausführungsreif und per Nikinger-Freigabe gelockt. Kein
  offener Planungsbedarf mehr — nur noch **nicht gebaut**. Details:
  `phase6_shares/CLAUDE.md`s aktuellem Session-Block.
- **MCP-Werkzeug-Ergonomie, Live-Feedback (2026-08-14, sechs Punkte):** Bulk-Append, `list_spaces` auffindbarer, `patch_item`-vs-`update_item`-Aufgabenteilung, `get_item_meta`-Trennung vom vollen Body, Status-Enum-Doku in der Tool-Beschreibung, Suchtreffer-Robustheit. Der eine Bug (irreführende `patch_item`-Fehlermeldung „0 Treffer — lies das Item neu“ auf Frontmatter-Feldern; `patch_item` erreicht Frontmatter grundsätzlich nicht) ist am 2026-08-14 behoben (Text nennt jetzt die Ursache + `update_item` als Alternative, keine Frontmatter-Erkennungslogik). Übrige fünf Punkte: Phase 6.5 Block A, gelockt in `phase6_5_tools_images_plan.md` Abschnitt 3. Volltext: `phase6_shares/CLAUDE.md` Vormerkungen.

**[2026-08-02 Korrektur]** Web-UI-Planungs-Entscheidung **P5-V** (Neubau mit Ernte aus `notiz_heft_example.html`): Layout + `sanitizeHtml`/`markdownToHtml` übernommen; Vault-Encryption (R4-inkompatibel), `localStorage` und `connect-src 'none'` verworfen. **[2026-07-28 Korrektur]** Kollege-Frage (eigener Prozess vs. eigener Space) ist seit P3-G entschieden und live bewiesen: **ein Prozess, ein Space je Person** — zwei Spaces real (`niklas`, `fabian`) über denselben `sharefyx-mcp.service`.
