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
updated: 2026-09-08 (Z-Final: Current-State-Sektion [428 Zeilen, ~48 KB historische Session-Blöcke aus P1-P8.5] nach `docs/PROJECT_SESSION_LOG.md` rotiert [neues L3-Archiv]; Kopf jetzt 166 Zeilen / ~34 KB — **unter dem 40-KB-Softcap**; Frontmatter vorne ergänzt; aktive Phase weiterhin phase8_5_picker_release/CLAUDE.md, die Phase-8/8.5-Heads sind in derselben Z-Final-Runde separat komprimiert worden) | 2026-09-08 (Phase 8.5 Z-Closeout — Sichtprüfungs-Automatisierung gegen Wegwerf + echte Produktion, Statusregel geändert (Nikinger-geprüfte Wegwerf-Automatisierung zählt als live-verifiziert), Bilanz 26 ✅ · 0 🟡 · 0 ⬜ für Phase 8 und 10 ✅ · 10 🟡 · 0 ⬜ für Phase 8.5; P8.6 (→v3.0.2) + P9 (→v3.1.0) als Folgephasen vorgemerkt; sechs Wegwerf-Instanzen sauber abgebaut, Produktion PID 355956 durchgehend unangetastet) | 2026-09-07 (Cluster-3-Teilverifikation — **P8-20 ✅ + P8-21 a/b/c ✅ am echten v3.0.1** durch den Nikinger in einer Login-Sitzung; P8-20 (Hover dimmt Nicht-Nachbarn + Klick öffnet Editor/Readonly via Fix C vom 2026-09-02 + Drag/Zoom/Pan) und P8-21 (Default nur explizite Kanten + Tag-Toggle + Ordner-Toggle) ohne Befund; P8-21 d + P8-22 + P8-24 in eine Folge-Session verschoben, weil alle drei die 200-Knoten-Wegwerf brauchen (Nikinger-Aktion); Phase-8-Bilanz **19 ✅ · 7 🟡 → 20 ✅ · 6 🟡** (P8-20 🟡 → ✅, P8-21 a/b/c bestätigt bei Beschreibung); `phase8_ui_graph/CLAUDE.md` §7 + Bilanz + Modul-Status Block D nachgezogen; `phase8_5_picker_release/CLUSTER3_TESTBLOCK.md` neu (17 KB, vollständiger Schritt-für-Schritt-Testblock für die Cluster-3-Prüfungen, Audit-Quelle für Z); pytest unverändert 964/964, Tabu-Diff §0.3 leer, Service-Touch 0 (PID 355956 nur gelesen, kein `sudo systemctl`); **Nikinger-Aktion in derselben Sub-Session:** Sean-Einladung — `authctl.py invite sean --purpose initial --ttl 86400` schreibt in die echte `auth.sqlite3` des `sharefyx-mcp.service` (Hard Rule 9 + §0.5.7 verbieten opencode/M3 den Eingriff), Link wird auf stdout einmalig ausgegeben; nächster Schritt Cluster 4 + 5 + Z, nach allen Clustern dann Phase-8-✅-Nachtrag + p8.X-Ankündigung im Z-Closeout) | 2026-09-07 (Phase 8.5 Pre-Z-Tausch — **erste opencode/M3-Code-Touch-Session seit Cluster 1**; P8.5-19 (Bauform Radiogruppe statt `<select>`) + P8.5-6 (Bracket-Renderer-Fix in `markdown.js`) committet, beide Zeilen jetzt mit Code + statischem Test; `dialogs.js` (`linkPickerModeEl` raus, neue Modul-Konstante `LINK_PICKER_MODE_NAME`, Selektor-Wechsel von `getElementById` auf `querySelector[All]('input[name="link-picker-mode"]')`, change-Listener iteriert die zwei Radios), `app.html` (`<fieldset class="link-picker-modes">` mit `<legend>Einfügen</legend>` + 2× `<input type="radio" name="link-picker-mode" value="…">` ersetzt `<select id="link-picker-mode">`), `app.css` neuer Block `.link-picker-modes`/`.link-picker-mode` mit `accent-color: var(--accent-line)`, `markdown.js` Link- und Bild-Regex tolerieren jetzt `\[` / `\]` als Escape-Einheit via `\\[\[\]]` (zwei Zeichen), danach `\\([\[\]])` → `$1` zum Unescapen des Title/Alt; `phase5_ui/tests/test_static_routes.py` +2 (`test_link_picker_uses_a_radio_group_not_a_select` P8.5-19, `test_markdown_link_regex_allows_escaped_brackets` P8.5-6 mit Regressionstest gegen die alte `[^\]]+`-Form); pytest 962 → **964** grün (254 s Gesamtlauf), `node --check` grün auf `dialogs.js` + `markdown.js`, `ui_budget.py` 5/5 im Korridor (dialogs.js 12.6 → 13.2 KB, markdown.js 4.2 KB, app.css +0.4 KB), Tabu-Diff §0.3 leer (alle Änderungen unter `phase5_ui/webui/static/` + `phase5_ui/tests/`, kein Servercode-Tabu-Auslöser), node-Probe gegen `markdown.js` mit Mock-`document`: 8 Test-Cases rendern wie erwartet — darunter D4-Fund-Beispiel `[Vercel \[Hosting\](#item/itm_67bb0565)` → `<a href="#item/itm_67bb0565">Vercel [Hosting]</a>`; Phase-8.5-Summary **5 ✅ · 13 🟡 · 2 ⬜ → 5 ✅ · 14 🟡 · 1 ⬜** (P8.5-19 ⬜ → 🟡, P8.5-5/-6-Beschreibungen aktualisiert); Phase-8-Bilanz unverändert 19/7/0; Phase-8.5-Head rotiert (Cluster-1-Block per Hand nach `SESSIONS_ARCHIVE.md`, dieser Pre-Z-Tausch-Block neu im Head, **~49 KB deutlich über 40-KB-Softcap** — Auflösung bleibt Z-Arbeit oder Trimm-Pass vor Z, gleiche Linie wie D3/D4 dokumentiert); Working Tree jetzt 7 uncommittete Dateien [5 Code/Tests + 2 Doku-Updates]; nächster Schritt unverändert Cluster 3+4+5 (Nikinger-Aktionen) + Z, mit optionaler P8.5-6-Wegwerf-Re-Probe in Cluster 4) | 2026-09-07 (Phase 8.5 + Phase 8 Cluster-2 — **erste echte Live-Verifikations-Welle seit D3**; Nikinger gegen v3.0.1 bestätigt: P8-14, P8-15, P8-18, P8-19, P8-23 (Screenshot `phase8_5_picker_release/screenshots/Bildschirmfoto 2026-09-07 um 17.08.37.png` zeigt tabellose Space-Zeilen + Zähler-Chips + VERKNÜPFUNGEN-Graph in eigen blau/geteilt türkis/fremd grau + ZULETZT-BENUTZT-Sektion + Badge `SHAREFYX v3.0.1`); P8.5-18 jetzt ✅ als Umbrella; Phase-8-Bilanz 14/12/0 → **19/7/0**, Phase-8.5-Bilanz 4/13/3 → **5/13/2** (P8.5-18 von ⬜ auf ✅); Phase-8-Glyph-Entscheidung noch offen (Vorschlag vorerst 🟡 bis Cluster 3/5); P8-20/21/22/24 + P8-5/8 bleiben 🟡 für Cluster 3/5; keine Code-Änderung in dieser Sub-Session — alle Updates sind Doku; Phase 8.5 Head rotiert (40.5 KB unter Cap); Working Tree jetzt 14 uncommittete Dateien [7 von D4+Sichtprobe-Folgesession + 7 von Cluster 1+2] | 2026-09-07 (Phase 8.5 Cluster-1 der Sichtprüfungen — **erste echte Code-Touch-Session seit D1**; `phase8_ui_graph/scripts/p8_16_glass_fallback_probe.py` + `wegwerf_setup_p8_16.py` neu (Port 18775, Standing-Permission-Muster reproduziert), vier Screenshots `docs/screenshots/p8_16_{01..04}_*.png`; CDP-Switch `prefers-reduced-transparency: reduce` über `Emulation.setEmulatedMedia` — beide Glass-Träger `.list__head`+`.overlay__panel` wechseln sauber `blur(14px) saturate(1.5)`+`rgba(27,32,39,0.55)` → `backdrop-filter: none`+`rgb(27,32,39)`, Selektion im Solid-Modus voll erkennbar mit Akzent-Fill+Outline; **P8.5-16 jetzt ✅**, doppelt mit Phase 8 P8-16 die selbe Evidenz; Phase-8-P8-16 bleibt 🟡 bis Nikinger-Sichtprüfung; Phase-8.5-Summary 3 ✅ · 14 🟡 · 3 ⬜ → **4 ✅ · 13 🟡 · 3 ⬜**; Phase-8.5-Head rotiert (40.579 B, 381 B unter 40-KB-Softcap); Working Tree jetzt 13 uncommittete Dateien [7 von D4+Sichtprobe-Folgesession + 6 von Cluster 1]; `pytest`/`node --check`/`ui_budget.py` nicht gelaufen (irrelevant), Tabu-Diff §0.3 leer (Phase-8.5-Tabu greift nicht für `phase8_ui_graph/scripts/`), Service-Touch 0 nur gelesen (PID 355956 unverändert seit 2026-09-05 16:10:18 CEST); nächster Schritt Cluster 2-5 je nach Nikinger) | 2026-09-06 (Phase 8.5 D4-Sichtprobe-Folgesession — **nur dokumentiert, kein Code-Touch in dieser opencode/M3-Session**; sieben neue Themen-Cluster aus der Sichtprobe mit Fabian nach D4 dokumentiert: **Spaces-Layout-Reorg** [„Alle Items"-Leiste unter Spaces + Kippschalter, Map 40 % Breite/volle Höhe, keine Duplikate], **Obsidian-Map** fünf Sub-Punkte [Performance-Reload, Landkarten-Stil, Field schneidet ab, Reload-Drift, Collapsible mit Abhängigkeiten], **Anzahl-Anzeige Ordner**, **Edit-in-Place-Vision** [„Bearbeiten"-Knopf überflüssig], **Layering-Design-System** [3 Layer: echtes Schwarz / aktueller Standard / Liquid Glass + Selektion explizit blau auf Hover, Note-Select, Checkbox], **„Konto"→„Einstellungen"-Rename** + Positions-Tausch mit Logout, **De-AI-ierung-Lauf 2** nach neuen Kriterien; neue Datei `docs/concepts/p8x_ui_polish_notes.md` 25 KB L2 mit allen 16 Themen — fünf bereits in D4 dokumentierte p8.X-Punkte [UX-2-Step-Knotenklick, Map-Field schneidet ab, Map fliegt, Save-Button-YAML-Header, Fabis Sammelliste] + sieben Sichtprobe-Folgesession-Cluster + vier Sub-Punkte aus §2 Obsidian-Map; Anhang §A–§E für die Planungs-Session in Claude Code; **kein Phase-8/8.5-Scope-Touch**, **keine** neuen Tabu-Aufhebungen, **kein** Locking — Sammlung, kein Plan; D4-Block per Hand nach `SESSIONS_ARCHIVE.md` rotiert (Skript passt nicht auf Phase-8.5-Muster, bewährtes Vorgehen); Modul-Status P8.5 unverändert (3 ✅ · 14 🟡 · 3 ⬜); pytest nicht gelaufen, Tabu-Diff §0.3 leer, Service-Touch 0; nächster Schritt unverändert D5 + V105 + optional vor Z Radiogruppe + Bracket, dann Z) | 2026-09-06 (Phase 8.5 D4 Sichtprüfung am echten Gerät durch den Nikinger — **nur dokumentiert, kein Code-Touch in dieser opencode/M3-Session**; Block 1–7 + Vorbereitung komplett durchgelaufen, Login beide Accounts ✅, Tastaturnavigation in Firefox+Chrome+Safari auf zwei Accounts ✅, Block 2/4/5-Kern ohne Befund, drei echte Funde dokumentiert: **P8.5-19-Entscheidung Radiogruppe** [User-Präferenz „deut... (line truncated to 2000 chars) | 2026-09-05 (Phase 8.5 D2 vom Nikinger zwischen D1 und D3 + D3-Prep, 🟡, ⬜ D4/D5/V105/Z als Nächstes. D2 ist **zwischen D1 (Commit heute früh) und D3 (diese Session) still durch den Nikinger gelaufen** — Entdeckung kam erst beim ersten Probe-Lauf des Health-Gate-Skripts: `/opt/sharefyx/current` → `20260905T140325.378914Z` → HEAD `6f19a8f` (D1), Service-PID **355956** (statt der im D1-Block notierten 195922 — D2-Deploy hat den Dienst erwartungsgemäß neu gestartet), `ExecMainStartTimestamp=2026-09-05 16:10:18 CEST`. Damit ist D3 nicht mehr Vorbereitung, sondern **Verifikation des bereits deployten v3.0.1**. Neu gebaut: `phase8_5_picker_release/scripts/health_gate.sh` (134 Zeilen bash, `set -uo pipefail`, JSON auf stdout / Details auf stderr nach Hard Rule 7), acht Gates — `/health` 200 mit Retry-Loop, `/ui/login` 200, `/api/v1/me` 401, `/mcp/` 401, `.rail__version` aus `/ui/static/app.html` (**nicht** `/ui/login` — `pages.py`s Auth-Template ohne Rail, erste Iteration fiel darauf herein, gefixt), `/opt/sharefyx/current` → Release mit `.git`, optional `--require-todays-update-log` (UTC/local wie `deploy.sh` Z. 127-131), optional `--expected-sha=<hex>` (Short- oder Full-Form per Prefix-Vergleich). **Lauf-Beleg 2026-09-05 15:19:53Z** mit `--require-todays-update-log --expected-sha=6f19a8f`: **8/8 grün**, Exit 0, JSON auf stdout (`result:"ok"`, `actual_version:"v3.0.1"`, `release_sha:"6f19a8f..."`, `active_release:"/opt/sharefyx/releases/20260905T140325.378914Z"`, `port:8765`). Drei Negativproben separat verifiziert (Port 9999 → Gate 1 rot, `--expected-version=v9.9.9` → Gate 5 rot, `--expected-sha=0000000` → Gate 8 rot). **P8.5-17 teilweise abgehakt:** Deploy gelaufen ✅, Health-Gate 8/8 ✅, Badge `v3.0.1` live ✅, Update-Banner-Live-Anzeige ⬜ (braucht Auth, Nikinger), V105 ⬜ (echter Anthropic-Connector, Nikinger). Modul-Status-Zeile 6 Block D um D2 ✅ + D3 🟡 erweitert; Abnahmestand-Zeile P8.5-17 Health-Gate-Teil 🟡; Summary **3 ✅ · 14 🟡 · 3 ⬜ von 20**; D1-Block (111 Zeilen) per Hand nach `SESSIONS_ARCHIVE.md` rotiert (Skript passt nicht auf das Phase-8.5-Muster — bewährtes Vorgehen aus D1 selbst). `pytest` nicht gelaufen (kein Python-Touch), `bash -n` OK, shellcheck nicht verfügbar (übersprungen, keine Konvention im Repo), Tabu-Diff §0.3 leer, Service-Touch 0 (PID 355956 nur gelesen). **Nächster Schritt:** D4 — Sichtprüfung am echten Gerät durch den Nikinger (`## 2026-09-05`-Eintrag im Update-Banner sichtbar, `<select class="input" id="link-picker-mode">` im Picker vorhanden — P8.5-19-Abnahme: Radiogruppe oder `<select>`-Bestätigung), D5 Vierte A3-Probe (entscheidet §9.4.1 Abbruchregel aus N2), V105-Connector-Check, Z Closeout. 2026-09-07 (Phase 8.5 Pre-Z-Tausch — **erste opencode/M3-Code-Touch-Session seit Cluster 1**; P8.5-19 (Bauform Radiogruppe statt `<select>`) + P8.5-6 (Bracket-Renderer-Fix in `markdown.js`) committet, beide Zeilen jetzt mit Code + statischem Test; `dialogs.js` (`linkPickerModeEl` raus, neue Modul-Konstante `LINK_PICKER_MODE_NAME`, Selektor-Wechsel von `getElementById` auf `querySelector[All]('input[name="link-picker-mode"]')`, change-Listener iteriert die zwei Radios), `app.html` (`<fieldset class="link-picker-modes">` mit `<legend>Einfügen</legend>` + 2× `<input type="radio" name="link-picker-mode" value="…">` ersetzt `<select id="link-picker-mode">`), `app.css` neuer Block `.link-picker-modes`/`.link-picker-mode` mit `accent-color: var(--accent-line)`, `markdown.js` Link- und Bild-Regex tolerieren jetzt `\[` / `\]` als Escape-Einheit via `\\[\[\]]` (zwei Zeichen), danach `\\([\[\]])` → `$1` zum Unescapen des Title/Alt; `phase5_ui/tests/test_static_routes.py` +2 (`test_link_picker_uses_a_radio_group_not_a_select` P8.5-19, `test_markdown_link_regex_allows_escaped_brackets` P8.5-6 mit Regressionstest gegen die alte `[^\]]+`-Form); pytest 962 → **964** grün (254 s Gesamtlauf), `node --check` grün auf `dialogs.js` + `markdown.js`, `ui_budget.py` 5/5 im Korridor (dialogs.js 12.6 → 13.2 KB, markdown.js 4.2 KB, app.css +0.4 KB), Tabu-Diff §0.3 leer (alle Änderungen unter `phase5_ui/webui/static/` + `phase5_ui/tests/`, kein Servercode-Tabu-Auslöser), node-Probe gegen `markdown.js` mit Mock-`document`: 8 Test-Cases rendern wie erwartet — darunter D4-Fund-Beispiel `[Vercel \[Hosting\](#item/itm_67bb0565)` → `<a href="#item/itm_67bb0565">Vercel [Hosting]</a>` (vor dem Fix kaputt); Phase-8.5-Summary **5 ✅ · 13 🟡 · 2 ⬜ → 5 ✅ · 14 🟡 · 1 ⬜** (P8.5-19 ⬜ → 🟡, P8.5-5/-6-Beschreibungen aktualisiert); Phase-8-Bilanz unverändert 19/7/0; Phase-8.5-Head rotiert (Cluster-1-Block per Hand nach `SESSIONS_ARCHIVE.md`, dieser Pre-Z-Tausch-Block neu im Head, **~49 KB deutlich über 40-KB-Softcap** — Auflösung bleibt Z-Arbeit oder Trimm-Pass vor Z, gleiche Linie wie D3/D4 dokumentiert); Working Tree jetzt 7 uncommittete Dateien [5 Code/Tests + 2 Doku-Updates]; nächster Schritt unverändert Cluster 3+4+5 (Nikinger-Aktionen) + Z, mit optionaler P8.5-6-Wegwerf-Re-Probe in Cluster 4) | 2026-09-07 (Phase 8.5 + Phase 8 Cluster-2 — **erste echte Live-Verifikations-Welle seit D3**; Nikinger gegen v3.0.1 bestätigt: P8-14, P8-15, P8-18, P8-19, P8-23 (Screenshot `phase8_5_picker_release/screenshots/Bildschirmfoto 2026-09-07 um 17.08.37.png` zeigt tabellose Space-Zeilen + Zähler-Chips + VERKNÜPFUNGEN-Graph in eigen blau/geteilt türkis/fremd grau + ZULETZT-BENUTZT-Sektion + Badge `SHAREFYX v3.0.1`); P8.5-18 jetzt ✅ als Umbrella; Phase-8-Bilanz 14/12/0 → **19/7/0**, Phase-8.5-Bilanz 4/13/3 → **5/13/2** (P8.5-18 von ⬜ auf ✅); Phase-8-Glyph-Entscheidung noch offen (Vorschlag vorerst 🟡 bis Cluster 3/5); P8-20/21/22/24 + P8-5/8 bleiben 🟡 für Cluster 3/5; keine Code-Änderung in dieser Sub-Session — alle Updates sind Doku; Phase 8.5 Head rotiert (40.5 KB unter Cap); Working Tree jetzt 14 uncommittete Dateien [7 von D4+Sichtprobe-Folgesession + 7 von Cluster 1+2] | 2026-09-07 (Phase 8.5 Cluster-1 der Sichtprüfungen — **erste echte Code-Touch-Session seit D1**; `phase8_ui_graph/scripts/p8_16_glass_fallback_probe.py` + `wegwerf_setup_p8_16.py` neu (Port 18775, Standing-Permission-Muster reproduziert), vier Screenshots `docs/screenshots/p8_16_{01..04}_*.png`; CDP-Switch `prefers-reduced-transparency: reduce` über `Emulation.setEmulatedMedia` — beide Glass-Träger `.list__head`+`.overlay__panel` wechseln sauber `blur(14px) saturate(1.5)`+`rgba(27,32,39,0.55)` → `backdrop-filter: none`+`rgb(27,32,39)`, Selektion im Solid-Modus voll erkennbar mit Akzent-Fill+Outline; **P8.5-16 jetzt ✅**, doppelt mit Phase 8 P8-16 die selbe Evidenz; Phase-8-P8-16 bleibt 🟡 bis Nikinger-Live-Sichtprüfung; Phase-8.5-Summary 3 ✅ · 14 🟡 · 3 ⬜ → **4 ✅ · 13 🟡 · 3 ⬜**; Phase-8.5-Head rotiert (40.579 B, 381 B unter 40-KB-Softcap); Working Tree jetzt 13 uncommittete Dateien [7 von D4+Sichtprobe-Folgesession + 6 von Cluster 1]; `pytest`/`node --check`/`ui_budget.py` nicht gelaufen (irrelevant), Tabu-Diff §0.3 leer (Phase-8.5-Tabu greift nicht für `phase8_ui_graph/scripts/`), Service-Touch 0 nur gelesen (PID 355956 unverändert seit 2026-09-05 16:10:18 CEST); nächster Schritt Cluster 2-5 je nach Nikinger) | 2026-09-06 (Phase 8.5 D4-Sichtprobe-Folgesession — **nur dokumentiert, kein Code-Touch in dieser opencode/M3-Session**; sieben neue Themen-Cluster aus der Sichtprobe mit Fabian dokumentiert: Spaces-Layout-Reorg, Obsidian-Map [5 Sub-Punkte], Anzahl-Anzeige Ordner, Edit-in-Place-Vision, Layering-Design-System [3 Layer + Selektion blau], „Konto"→„Einstellungen"-Rename, De-AI-ierung-Lauf 2; neue Datei `docs/concepts/p8x_ui_polish_notes.md` 25 KB L2 mit allen 16 Themen — fünf D4-Punkte + sieben Sichtprobe-Folgesession-Cluster + vier Sub-Punkte aus §2 Obsidian-Map; Anhang §A–§E für die Planungs-Session; **kein Plan, kein Locking, keine Tabu-Aufhebung** — Sammlung; neue ROOT-Current-State-Zeile für die Folgesession ergänzt; `phase8_5_picker_release/CLAUDE.md` aktiver Block auf D4-Sichtprobe-Folgesession umgestellt, D4-Block per Hand nach `SESSIONS_ARCHIVE.md` rotiert (Skript passt nicht auf Phase-8.5-Muster); keine Code-Tests, kein Service-Touch; nächster Schritt D5 Vierte A3-Probe + V105 Connector-Check — beides Nikinger; optional vor Z Radiogruppe-Tausch + Bracket-Fix durch opencode/M3) | 2026-09-06 (Phase 8.5 D4 Sichtprüfung durch den Nikinger — **nur dokumentiert, kein Code-Touch in dieser opencode/M3-Session**; Block 1–7 + Vorbereitung komplett durchgelaufen, drei echte Findings: **P8.5-19 Radiogruppe statt `<select>`** [Tausch 5 Z. ausstehend], **P8.5-6 Bracket-Renderer-Bug in `markdown.js`** [Fix ausstehend], **UX-2-Step-Knotenklick als neues Feature für p8.X** [parkiert]; Phase 8 ✅ + p8.X als Nikinger-Entscheidung für Z vorgemerkt; Modul-Status Zeile 6 Block D um D4 ✅ erweitert; Summary 3 ✅ · 14 🟡 · 3 ⬜; D3-Block per Hand nach SESSIONS_ARCHIVE.md rotiert; keine Code-Tests, kein Service-Touch; nächster Schritt D5 Vierte A3-Probe + V105 Connector-Check — beides Nikinger; optional vor Z Radiogruppe-Tausch + Bracket-Fix durch opencode/M3) | 2026-09-05 (Phase 8.5 D3-Prep — `scripts/health_gate.sh` neu, 134 Zeilen bash, acht Gates; **Lauf 2026-09-05 15:19:53Z 8/8 grün** gegen den frischen Deploy; **D2 lief zwischen D1 und D3 still durch den Nikinger** (PID 355956 statt 195922, Release `20260905T140325.378914Z`, ExecMainStartTimestamp `2026-09-05 16:10:18 CEST`) — D3 ist Verifikation statt Vorbereitung; D1-Block per Hand nach `SESSIONS_ARCHIVE.md` rotiert; Modul-Status Zeile 6 um D2 ✅ + D3 🟡 erweitert; Abnahmestand P8.5-17 Health-Gate-Teil 🟡, Summary-Zeile 3 ✅ · 14 🟡 · 3 ⬜; pytest nicht gelaufen (kein Python-Touch), bash -n OK, shellcheck nicht verfügbar (übersprungen, keine Konvention im Repo), Tabu-Diff §0.3 leer, Service-Touch 0; nächster Schritt D4 Sichtprüfung am echten Gerät — Nikinger-Aktion) | 2026-09-05 (Phase 8.5 D1 committet — Badge `v3.0`→`v3.0.1` in `phase5_ui/webui/static/app.html:20` (P8.5-N7, statisches HTML nicht im Tabu §0.3); neuer `## 2026-09-05`-Block in `docs/UPDATE_LOG.md` mit drei Zeilen Picker-Modi/Tastatur/Generalisierter-Hint — **Datums-Drift dokumentiert**: Block-C-Absatz schlug `## 2026-09-04` vor, `date +%F`/`date -u +%F` ist heute 2026-09-05, `deploy.sh` Z. 117–131 verlangt strikt `today_utc`/`today_local`, sonst Gate-Abbruch; Block-C-Block per Hand nach `SESSIONS_ARCHIVE.md` rotiert (Skript passt nicht auf Phase-8.5-Muster mit einem `## Session stopped` + mehreren `### date`-Subblöcken → Exit 2 „Bereits konform"); Modul-Status D `⬜`→`🟡` mit D2–D5 als Nikinger-Aktionen vermerkt; `pytest` nicht gelaufen (kein Python-Touch), Tabu-Diff §0.3 leer, Service-Touch 0 (PID 195922 / ActiveEnterTimestamp 2026-09-02 11:51:57 CEST nur gelesen); nächster Schritt D2 = `sudo systemctl ... deploy.sh main`) | 2026-09-04 (Wurzel-CLAUDE.md komprimiert -- Phase-6-Verlaufsdokumentation + Phase-6/6.5-Vormerkungen + Funnel-Reboot + MCP-Werkzeug-Ergonomie + End-Korrekturen P5/P4 auf Pointer-Form gestaucht; ~5 KB freigemacht, aktueller Stand ~39.7 KB unter Cap; Phase-8.5-Work-Abschnitt aktualisiert auf A1+A2, A1-Block rotiert nach Archiv) | 2026-09-04 (Phase 8.5 B1 committet -- `_TITLE_NOT_ID_HINT` in `phase2_mcp/mcpserver/tools.py:159-164` generalisiert, „Das gilt in jeder Textform -- auch nicht als Tabellen-Spalte, nicht in Klammern hinter dem Titel und nicht in Aufzählungs-Zeilen" wörtlich aus Plan §3 B1; `test_tools.py` zwei Asserts (`in jeder Textform`/`Klammern`); neuer Phase-Head-Abschnitt `## Abbruchregel §9.4.1 (N2, verbindlich)`; Modul-Status B1 + P8.5-3, A2-Block nach `SESSIONS_ARCHIVE.md` rotiert; pytest 962/962 unverändert, Tabu-Diff zeigt **genau** `tools.py +5/-2` und `test_tools.py +2`, kein Service-Touch) | 2026-09-04 (Phase 8.5 A2 committet `7ce0be0` -- Tastaturnavigation `aria-activedescendant` + `_pickLinkPickerAt` + CSS-Block-Entdopplung am Picker; +3 statische Tests in `test_static_routes.py`; A1-Block nach `SESSIONS_ARCHIVE.md` rotiert) | 2026-09-04 (Phase 8.5 Drift nachgezogen `4424310` + A1 committet `499d9be` -- Picker-Modus-Umschalter + `localStorage` `sfx:linkpicker:mode`; V99 `session` zu `local` als Eskalation wegen P8.5-G; erste `localStorage`-Nutzung des Projekts) | 2026-09-03 (Phase 8.5 Step 0 -- Skelett phase8_5_picker_release/{CLAUDE.md, SESSIONS_ARCHIVE.md, scripts/} angelegt; vier Paragraph-1-Funde: INDEX 52.911 zu 40.917 B unter Cap, Bueroklammer-zu-Lupe-Drift in phase8_ui_graph/CLAUDE.md:440, Phase-8-Bilanz korrigiert; ROADMAP-Abschnitt neu; Wurzel-`down:` umgestellt) | 2026-09-01 (Phase 8 Sichtpruefung 1 + Gate B zu C bestanden; **Hard Rule 9 ergaenzt** -- kein `pkill -f` mit Regex, niemals den systemd-Dienst anfassen, Lehre aus dem Prod-Vorfall 2026-09-01 Phase 8 Step A3 Nachbereitung) | aeltere Eintraegge: die jeweilige phase*/SESSIONS_ARCHIVE.md
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
- **Vor „das braucht einen echten Menschen/Connector" nachsehen, nicht neu erfinden:**
  `docs/concepts/sichtpruefung_automation_conventions.md` sammelt Techniken, mit denen sich
  Sichtprüfungen, die auf den ersten Blick blockiert wirken, doch skripten lassen (Canvas-
  Instrumentierung, OAuth-Dance ohne Browser, Zwei-Principal-Wegwerf-Muster). Erst dort
  nachsehen, dann ggf. recherchieren.

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

**[2026-09-08, Z-Closeout] Phase 8 ✅ + Phase 8.5 ✅ — formal abgeschlossen, Statusregel geändert, zwei Folgephasen (P8.6 → v3.0.2, P9 → v3.1.0) vorgemerkt.** Sichtprüfungs-Automatisierungs-Sub-Session: 9 von 9 Sichtprüfungs-Punkten aus dem D5/Cluster-4/Cluster-5-Restblock durchgelaufen — teils gegen Wegwerf-Instanzen (Canvas-Instrumentierung für den exakten Tag-Kanten-Zähler, CDP-Medien-Emulation für Glass-Fallback, ein neu gebautes Zwei-Principal-Wegwerf-Setup für den echten Zweitnutzer-ACL-Nachweis über OAuth+MCP), teils gegen die echte Produktion (der reconnectete sharefyx-MCP-Connector: `list_spaces` + ein echter claude.ai-Chat des Nikingers, der ein Item korrekt beim Titel statt bei der `itm_…`-ID nannte). **Statusregel-Änderung, Nikinger-Entscheidung:** eine vom Nikinger selbst geprüfte Wegwerf-Instanz-Automatisierung (byte-identischer Git-Checkout wie Produktion, Unterschied nur `DATA_ROOT`/`auth.sqlite3`/Identität) zählt jetzt als „live-verifiziert" — Details, Begründung, wiederverwendbare Techniken: `docs/concepts/sichtpruefung_automation_conventions.md` (neu, samt Schwester-Datei `sichtpruefung_automation_tooling.md` für Werkzeug-/Plugin-Empfehlungen). Phase-8-Bilanz **26 ✅ · 0 🟡 · 0 ⬜**, Phase-8.5-Bilanz **10 ✅ · 10 🟡 · 0 ⬜** (die verbleibenden 🟡 sind Block-C-Belege von 2026-09-04, die der Nikinger unter der neuen Regel noch nicht gesichtet hat — kein neuer Code nötig, nur eine Sichtung). Drei Wegwerf-Instanzen (200-Knoten, D2, das neue Zwei-Principal-Setup) sauber abgebaut, PID-Datei-basiert, kein `pkill -f`, Produktion durchgehend unangetastet (PID 355956). **Zwei Folgephasen besprochen, noch nicht geplant:** **P8.6** (Arbeitsname, → `v3.0.2`) bündelt die restlichen `p8x_ui_polish_notes.md`-Punkte + einen Radiogruppe-Rückbau auf `<select>` (Nikinger kehrt seine eigene D4-Entscheidung um, Design-Konsistenz) — **erster Punkt darin: das OpenCode-Vision-Plugin installieren** (`DavidEasden/opencode-vision`), damit künftige Sichtprüfungsrunden davon profitieren; **P9** (Arbeitsname, → `v3.1.0`) ist der Obsidian-Map-/Graph-Umbau, laut Nikinger voraussichtlich der letzte große UI-Umbau. Volle Herleitung, Matrix-Zeilen, Screenshots: `phase8_ui_graph/CLAUDE.md` §Abnahmestand, `phase8_5_picker_release/CLAUDE.md` Abnahmestand + „Nächste Phasen"-Abschnitt.

_Vollständige Chronik der älteren Einträge (Phase 8, Phase 8.5-Vorlauf, Phase 7/6.5/6-Abschluss,
Phase-5/4/3/2/1-Zusammenfassungen, Hard-Rule-Korrekturen): `docs/PROJECT_SESSION_LOG.md` (L3).
Neue Session-Blöcke wachsen oben in dieser Current-state-Sektion; ältere Blöcke rotieren
verbatim nach `PROJECT_SESSION_LOG.md` (neues Muster, gilt ab diesem Z-Final-Run)._

