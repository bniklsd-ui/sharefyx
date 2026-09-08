---
status: live
purpose: Phase-Head Link-Picker-Politur, Titel-statt-ID-Hint, v3-Vorabritt + Deploy — Scope, harte Regeln, Modulstatus, aktueller Session-Handover
read-when: Arbeiten in phase8_5_picker_release/ oder an den in §0.3/§2/§3/§4/§5 des Plans genannten Dateien in phase5_ui/webui/static/ phase2_mcp/mcpserver/ scripts/ — zuerst lesen, zusammen mit dem neuesten Session-stopped-Block
detail: L2
up: ../CLAUDE.md
down:
  - ../docs/concepts/phase8_5_picker_release_plan.md   # voller Plan, Entscheidungen P8.5-A–P8.5-T, §0.1 gelockte N1–N7, Steps 0/A/B/C/D/Z
  - ../phase8_ui_graph/CLAUDE.md                       # Phase 8 — schließt diese Phase mit ab (N6, P8.5-R), kein eigenes Handover
  - ../phase8_ui_graph/SESSIONS_ARCHIVE.md              # Bilanz P8-22/P8-24-Smokes, drei §9.4.6-Befunde (Settle/Farbe/Klick), P8.5-Vorgänger-Session-Block
  - SESSIONS_ARCHIVE.md                                 # ältere Session-Blöcke, newest-first
updated: 2026-09-08 (Folge-Sub-Session 4, Z-Closeout: Sichtprüfungs-Automatisierung fertig, Statusregel geändert, Phase 8 + 8.5 formal ✅, P8.6/P9 vorgemerkt -- siehe Session-Block am Dateiende) | 2026-09-08 (Doku-Sub-Session 2: **freundlicher Walkthrough** `phase8_5_picker_release/SICHTPRUEFUNG_WALKTHROUGH.md` neu, 29 KB / 727 Zeilen — Was-tust-du / Was-siehst-du pro Schritt, mit DevTools-Befehlen + Console-Snippets + Stoppuhr-Anleitung; Geschwister zum technischen `SICHTPRUEFUNG_RESTBLOCK.md` (dicht, mit Tabellen und Code-Ankern); Walkthrough ist das, was beim Klicken am Bildschirm vor einem liegt, Restblock ist das Nachschlagewerk; deckt C4-0 (P8-16 Glass-Fallback), C4-1 (P8.5-19 Radiogruppe), C4-2 (P8.5-3+4 Hint + Vierte A3-Probe), C4-3 (P8.5-17 V105), C3-1 (P8-21d Tag-Cutoff), C3-2 (P8-22 Settle/Interaktion/Reduced-Motion), C3-3 (P8-24 E2E gegen D2), C5-1 (P8-5 = C4-2), C5-2 (P8-8 mit Fabian); **kein Code-Touch**, nur Doku; pytest unverändert 964/964, Tabu-Diff §0.3 leer, Service-Touch 0) | 2026-09-08 (Doku-Sub-Session: 200-Knoten-Wegwerf gestartet per Standing-Permission für die Cluster-3-Rest-Sichtprüfung [P8-21 d + P8-22 + P8-24]; **drei User-Feedback-Punkte** in `docs/concepts/p8x_ui_polish_notes.md` ergänzt: §6 Konto/Einstellungen re-affirmiert mit drei Vertausch-Lesarten a/b/c gegen `app.html:31-41`, §8 NEU customizable Tags + Standard-Tag „blocked" [§8.1 User-Palette als `localStorage`, §8.2 fester Code-Tag, beide kosmetisch], §9 NEU direkter User-Feedback-Button [drei plausible Senken: User-Space / `/var/log/sharefyx/feedback/` / externer Endpunkt]; **kein Code-Touch**; pytest unverändert 964/964, Tabu-Diff §0.3 leer, Service-Touch 0 [PID 355956 unverändert], Wegwerf-PID **436596** auf Port **18772**); Cluster-3-Block per Hand nach `SESSIONS_ARCHIVE.md` rotiert (Skript passt nicht auf Phase-8.5-Muster), dieser 2026-09-08-Block neu im Head; **Polard-Notes 25.5 → 37.5 KB** knapp unter 40-KB-Softcap) | 2026-09-08 (Doku-Sub-Session Folge: **D2-Wegwerf zusätzlich hochgefahren** auf Port 18768 [PID 438765], beide Wegwerf-Instanzen laufen jetzt parallel — 200-Knoten auf 18772 für Cluster-3-Rest P8-21 d + P8-22, D2-14-Knoten auf 18768 für P8-24; **`phase8_5_picker_release/SICHTPRUEFUNG_RESTBLOCK.md` neu**, 27.5 KB / 471 Zeilen, der konsolidierte Schritt-für-Schritt-Testblock für alle restlichen Sichtprüfungen — Cluster 3-Rest (P8-21 d, P8-22, P8-24) gegen die zwei Wegwerf-Instanzen + Cluster 4 (P8-16 + P8.5-3/4/17/19) gegen Production v3.0.1 + Cluster 5 (P8-5 + P8-8, letzteres mit Fabian); Login-Snippet mit re-runnablem TOTP-Code für beide Instanzen, Screenshots-Konvention, Ergebnis-Tabellen je Cluster, Reihenfolge-Empfehlung, Cleanup-Befehle [Hard Rule 9, PID-Datei, **niemals** `pkill -f`]; **kein Code-Touch**, nur Doku + zweiter Wegwerf-Setup; pytest unverändert 964/964, Tabu-Diff §0.3 leer, Service-Touch 0 [PID 355956 unverändert]) | 2026-09-08 (Doku-Sub-Session: 200-Knoten-Wegwerf gestartet per Standing-Permission für die Cluster-3-Rest-Sichtprüfung [P8-21 d + P8-22 + P8-24]; **drei User-Feedback-Punkte** in `docs/concepts/p8x_ui_polish_notes.md` ergänzt: §6 Konto/Einstellungen re-affirmiert mit drei Vertausch-Lesarten a/b/c gegen `app.html:31-41`, §8 NEU customizable Tags + Standard-Tag „blocked" [§8.1 User-Palette als `localStorage`, §8.2 fester Code-Tag, beide kosmetisch], §9 NEU direkter User-Feedback-Button mit drei plausiblen Senken [User-Space-Item / `/var/log/sharefyx/feedback/` / externer Endpunkt] + Klärungsfragen zur Planungs-Session; **kein Code-Touch**; pytest unverändert 964/964, Tabu-Diff §0.3 leer, Service-Touch 0 [PID 355956 unverändert], Wegwerf-PID **436596** auf Port **18772**); Cluster-3-Block per Hand nach `SESSIONS_ARCHIVE.md` rotiert, dieser 2026-09-08-Block neu im Head; **Polard-Notes 25.5 → 37.5 KB** knapp unter 40-KB-Softcap) | 2026-09-07 (Cluster-3-Teilverifikation — **erste Nikinger-Live-Sichtprüfung nach Cluster 2; P8-20 ✅, P8-21 a/b/c ✅ am echten v3.0.1 in einer Login-Sitzung**; P8-20 (Hover dimmt Nicht-Nachbarn + Klick öffnet Editor bzw. Readonly mit korrekter Drag-vs-Click-Heuristik aus Fix C + Drag/Zoom/Pan ohne Ruckler) und P8-21 (Default nur explizite Kanten + Tag-Toggle + Ordner-Toggle) — Sub-Punkte a/b/c durchlaufen ohne Befund; **P8-21 d + P8-22 + P8-24 in eine Folge-Session verschoben**, weil alle drei die 200-Knoten-Wegwerf brauchen (Nikinger-Aktion per Standing-Permission in `phase8_ui_graph/scripts/wegwerf_setup_200knoten.py`, Port 18772); Phase-8-Bilanz **19 ✅ · 7 🟡 → 20 ✅ · 6 🟡** (P8-20 wandert 🟡 → ✅, `phase8_ui_graph/CLAUDE.md` §7-Matrix + Modul-Status Block D + Bilanz-Zeile + Sichtprüfungs-Status im selben Sub-Session-Commit nachgezogen); `phase8_5_picker_release/CLUSTER3_TESTBLOCK.md` neu (17 KB, 243 Zeilen, vollständiger Schritt-für-Schritt-Testblock als Audit-Quelle für Z); Pre-Z-Tausch-Block per Hand nach `SESSIONS_ARCHIVE.md` rotiert (Skript passt nicht auf Phase-8.5-Muster, Working-Tree-Rekonstruktion weil zwischen den Sub-Sessions kein Commit lag), Cluster-3-Block neu im Head; pytest unverändert 964/964, `node --check`/`ui_budget.py`/`bash -n` irrelevant (kein Code-Touch), Tabu-Diff §0.3 leer, Service-Touch 0 (PID 355956 nur gelesen, kein `sudo systemctl`, keine Wegwerf gestartet); Working Tree jetzt 9 modifizierte Dateien + 1 untracked Testblock-Datei = 10 Dateien; **Nikinger-Aktion in derselben Sub-Session:** Sean-Einladung über `authctl.py invite sean --purpose initial --ttl 86400` (24h gültig, Link wird auf stdout einmalig ausgegeben mit PRODUKTIV/STAGING-Marker zur Datenbank-Zuordnung — Hard Rule 9 + §0.5.7 verbieten opencode/M3 den Eingriff in die echte `auth.sqlite3`); nächster Schritt Cluster 4 (Connector: P8.5-3 + P8.5-4 + P8.5-17 V105 + P8.5-19 Bauform-Bestätigung Radiogruppe am echten v3.0.1) + Cluster 5 (Fabian: P8-5 + P8-8) + Z | 2026-09-07 (Pre-Z-Tausch — **erste opencode/M3-Code-Touch-Session seit Cluster 1**; **P8.5-19** (Bauform-Entscheidung Radiogruppe) und **P8.5-6** (Bracket-Renderer-Fix) committet, beide Zeilen jetzt mit Code + statischem Test; `dialogs.js` (`linkPickerModeEl` raus, neue Modul-Konstante `LINK_PICKER_MODE_NAME`, `_linkPickerMode`/`_restoreLinkPickerMode` auf `querySelector[All]('input[name="link-picker-mode"]')` umgestellt, change-Listener iteriert jetzt die Radios), `app.html` (`<fieldset class="link-picker-modes">` mit `<legend>Einfügen</legend>` + 2× `<input type="radio" name="link-picker-mode">` ersetzt `<select id="link-picker-mode">`), `app.css` neuer Block `.link-picker-modes`/`.link-picker-mode` (`accent-color: var(--accent-line)`), `markdown.js` Link- und Bild-Regex tolerieren jetzt `\[` / `\]` als Escape-Einheit (`(?:\\[\[\]]|[^\]])+` im Title-Capture, danach `\\([\[\]])` → `$1` zum Unescapen); `phase5_ui/tests/test_static_routes.py` zwei neue Tests (`test_link_picker_uses_a_radio_group_not_a_select` P8.5-19, `test_markdown_link_regex_allows_escaped_brackets` P8.5-6 mit Regressionstest gegen die alte `[^\]]+`-Form); `pytest -q` 962 → **964** grün (254 s Gesamtlauf), `node --check` grün auf `dialogs.js` + `markdown.js`, `ui_budget.py` 5/5 im Korridor (dialogs.js 12.6 → 13.2 KB, markdown.js 4.2 KB unverändert, app.css +0.4 KB), Tabu-Diff §0.3 leer (alle Änderungen unter `phase5_ui/webui/static/` + `phase5_ui/tests/`, kein Servercode-Tabu-Auslöser), node-Probe gegen `markdown.js` mit Mock-`document`: 8 Test-Cases rendern wie erwartet — darunter D4-Fund-Beispiel `[Vercel \[Hosting\](#item/itm_67bb0565)` → `<a href="#item/itm_67bb0565">Vercel [Hosting]</a>`; Abnahmestand **5 ✅ · 14 🟡 · 1 ⬜** (P8.5-19 ⬜ → 🟡, P8.5-5/-6-Beschreibungen aktualisiert); Cluster-1-Block nach `SESSIONS_ARCHIVE.md` rotiert (manuell, Skript passt nicht auf Phase-8.5-Muster), Service-Touch 0 (PID 355956 nur gelesen); nächster Schritt unverändert Cluster 3+4+5 (Nikinger-Aktionen) + Z, mit optionaler P8.5-6-Wegwerf-Re-Probe in Cluster 4) | 2026-09-06 (D4-Sichtprobe-Folgesession — **nur dokumentiert, kein Code-Touch in dieser opencode/M3-Session**; sieben neue Themen-Cluster aus der Sichtprobe mit Fabian nach D4 dokumentiert: **Spaces-Layout-Reorg** [„Alle Items"-Leiste unter Spaces + Kippschalter, Map 40 % Breite/volle Höhe, keine Duplikate], **Obsidian-Map** fünf Sub-Punkte [Performance-Reload, Landkarten-Stil, Field schneidet ab, Reload-Drift, Collapsible mit Abhängigkeiten], **Anzahl-Anzeige Ordner**, **Edit-in-Place-Vision** [„Bearbeiten"-Knopf überflüssig], **Layering-Design-System** [3 Layer: echtes Schwarz / aktueller Standard / Liquid Glass + Selektion explizit blau auf Hover, Note-Select, Checkbox], **„Konto"→„Einstellungen"-Rename** + Positions-Tausch mit Logout, **De-AI-ierung-Lauf 2** nach neuen Kriterien; neue Datei `docs/concepts/p8x_ui_polish_notes.md` 25 KB L2 mit allen 16 Themen — fünf bereits in D4 dokumentierte p8.X-Punkte [UX-2-Step-Knotenklick, Map-Field schneidet ab, Map fliegt, Save-Button-YAML-Header, Fabis Sammelliste] + sieben Sichtprobe-Folgesession-Cluster + vier Sub-Punkte aus §2 Obsidian-Map; Vorsegmentierter Anhang §A–§E für die Planungs-Session in Claude Code; **kein Phase-8/8.5-Scope-Touch**, **keine** neuen Tabu-Aufhebungen, **kein** Locking — Sammlung, kein Plan; D4-Block per Hand nach `SESSIONS_ARCHIVE.md` rotiert (Skript passt nicht auf Phase-8.5-Muster, bewährtes Vorgehen); Modul-Status P8.5 unverändert (3 ✅ · 14 🟡 · 3 ⬜); pytest nicht gelaufen, Tabu-Diff §0.3 leer, Service-Touch 0; nächster Schritt unverändert D5 + V105 + optional vor Z Radiogruppe + Bracket, dann Z) | 2026-09-06 (D4 Sichtprüfung am echten Gerät durch den Nikinger — **nur dokumentiert, kein Code-Touch in dieser opencode/M3-Session**; Block 1–7 + Vorbereitung komplett durchgelaufen, Login beide Accounts ✅, Tastaturnavigation in Firefox+Chrome+Safari auf zwei Accounts ✅, Block 2/4/5-Kern ohne Befund, drei echte Funde dokumentiert: **P8.5-19-Entscheidung Radiogruppe** [User-Präferenz „deutlich angenehmer", Tausch 5 Zeilen in `dialogs.js:584`+`app.html:277` ausstehend, Lucide-Icons `link-2`+`pilcrow`/`text-cursor-input` als Vorschlag offen], **P8.5-6 Bracket-Renderer-Bug** [Source-Escape `\[`/`\]` korrekt, aber `markdown.js`-Parser bricht Link in Vorschau — eckige Klammern zerlegen die URL-Zuordnung, runde Klammern funktionieren; §0.3 erlaubt `webui/static/js/`, Hard-Rule-9-Eskalation greift nicht, Fix-Pfad vor Z], **UX-2-Step-Knotenklick** [neues Feature „erster Klick Readonly-Vorschau, zweiter Klick vollständig" für p8.X parkiert, Fabi sammelt gerade], Save-Button-YAML-Header-Issue wahrscheinlich p8.X [parken bis Verifikation ob außerhalb Header-Kontext], zwei Map-Beobachtungen explizit bestätigt; **Phase 8 ✅ + p8.X als Folge-Phase** als Nikinger-Entscheidung für Z vorgemerkt; Modul-Status-Zeile 6 Block D um D4 ✅ erweitert (mit Findings-Anhang); P8.5-6-Zeile um Bracket-Bug-Caveat; P8.5-17-Zeile Update-Banner-live jetzt ✅; Summary-Zeile 3 ✅ · 14 🟡 · 3 ⬜ unverändert [P8.5-6 bleibt 🟡 Fix ausstehend, P8.5-17 bleibt 🟡 V105 offen]; D3-Block (154 Zeilen) per Hand nach `SESSIONS_ARCHIVE.md` rotiert (Skript passt nicht auf Phase-8.5-Muster); keine Code-Tests, kein Service-Touch; nächster Schritt D5 Vierte A3-Probe + V105 Connector-Check — beides Nikinger; optional vor Z Radiogruppe-Tausch + Bracket-Fix durch opencode/M3) | 2026-09-05 (D3-Prep — `phase8_5_picker_release/scripts/health_gate.sh` neu, 134 Zeilen bash, acht Gates (/health 200 + Retry-Loop, /ui/login 200, /api/v1/me 401, /mcp/ 401, .rail__version aus /ui/static/app.html, /opt/sharefyx/current, --require-todays-update-log, --expected-sha); **Lauf 2026-09-05 15:19:53Z 8/8 grün** gegen den frischen Deploy; **Discovery: D2 lief bereits** zwischen D1 (Commit heute früh) und dieser Session (PID **355956** statt 195922, Release `20260905T140325.378914Z`, ExecMainStartTimestamp `2026-09-05 16:10:18 CEST`), D3 ist Verifikation statt Vorbereitung; D1-Block (111 Zeilen) per Hand nach `SESSIONS_ARCHIVE.md` rotiert (Skript passt nicht auf Phase-8.5-Muster); Modul-Status-Zeile 6 Block D um D2 ✅ + D3 🟡 erweitert; Abnahmestand P8.5-17 Health-Gate-Teil jetzt 🟡 (C/L-Mix, Update-Banner-live + V105 weiter Nikinger); Summary-Zeile 3 ✅ · 14 🟡 · 3 ⬜ korrigiert; pytest nicht gelaufen (kein Python-Touch), `bash -n` OK, shellcheck nicht verfügbar (übersprungen, keine Konvention im Repo), Tabu-Diff §0.3 leer, Service-Touch 0 nur gelesen; nächster Schritt D4 Sichtprüfung am echten Gerät — Nikinger-Aktion) | 2026-09-05 (D1 committet — Badge `v3.0`→`v3.0.1` in `phase5_ui/webui/static/app.html:20` (P8.5-N7, statisches HTML nicht im Tabu §0.3); neuer `## 2026-09-05`-Block in `docs/UPDATE_LOG.md` mit drei Zeilen Picker-Modi/Tastatur/Generalisierter-Hint (Datums-Drift gegenüber Block-C-Spec dokumentiert: Block-C schlug `## 2026-09-04` vor, `date +%F`/`date -u +%F` ist heute 2026-09-05, `deploy.sh` Z. 117–131 verlangt strikt `today_utc`/`today_local`, sonst Gate-Abbruch); Block-C-Block per Hand nach `SESSIONS_ARCHIVE.md` rotiert (newest-first vor B1), Skript `scripts/rotate_session_block.sh` passt nicht auf Phase-8.5-Muster mit einem `## Session stopped` + mehreren `### date`-Subblöcken → Exit 2 „Bereits konform"; Modul-Status-Zeile D `⬜`→`🟡` (D1 fertig, D2–D5 als Nikinger-Aktionen vermerkt); pytest nicht gelaufen (kein Python-Touch), Tabu-Diff §0.3 leer (`app.html` und `docs/UPDATE_LOG.md` nicht tabu), `node --check`/`ui_budget.py` irrelevant; Service-Touch 0 PID 195922 ActiveEnterTimestamp 2026-09-02 11:51:57 CEST nur gelesen; nächster Schritt D2 = `sudo systemctl ... deploy.sh main`) | 2026-09-04 (Block C committet — `scripts/rotate_session_block.sh` aus `scripts/` nach `phase8_5_picker_release/scripts/` portiert (YAGNI aus A1/A2 geschlossen, ein Aufruf `Bereits konform` als Exit-2-Quittung), `wegwerf_setup_v3ritt.py` neu (Port 18773 V98, Standing-Permission-Muster aus Phase 8 reproduziert, 30 Items über 3 Spaces — 12 alpha + 10 beta + 8 gamma, 1 archiviertes, 1 mit item-level `share_read=["gamma"]` P6-§35-39-Fall, 1 mit Bild-Asset `ast_351d4217` per `put_asset()`, 11 explizite Kanten inkl. V102-Zwillings-Kante Buecherliste ↔ Empfehlungen Nikinger), `v3_ritt_playwright_smoke.py` neu (~720 Zeilen, `pyotp`+`async_playwright`, **26/26 Stationen grün: Chromium 13/13 + Firefox 13/13**, V101 für beide Browser bestätigt; 16 Screenshots `docs/screenshots/v3ritt_{chromium,firefox}_NN_*.png`; drei echte Befunde vorgelegt: 1. Smoke-Bug `src_id`→`src` [gefixt im Smoke, kein Server-Bug], 2. CSRF-Origin-Mismatch zwischen `http://127.0.0.1:18773` und `SPACE_PUBLIC_BASE_URL=https://wegwerf-v3ritt.invalid` wegen `_validate_base_url`-Pflicht [Befund für Step Z / Plan §4.C3], 3. Station 12 nur strukturell [bleibt, throwaway-verifiziert in P8]); Modul-Status C `⬜`→`🟡`, Abnahmestand 3 ✅ · 4 🟡 · 13 ⬜ → **3 ✅ · 13 🟡 · 4 ⬜** (P8.5-5/-6/-7/-8/-10/-11/-13/-15/-16 `⬜`→`🟡` mit Belegnotiz je Zeile); B1-Block nach `SESSIONS_ARCHIVE.md` rotiert (manuell — `rotate_session_block.sh` jetzt vorhanden, aber YAGNI-Stand aus A1/A2 gilt für die zweite Rotation nicht mehr, sobald Block D abgeschlossen ist); pytest 962/962 unverändert (kein Python-Touch im Block-C-Setup), Tabu-Diff §0.3 leer (kein `mcpserver/`/`storage/`/`authserver/`/`security.py`/`api.py`/`serializers.py`/`permissions.py`-Touch), Service-Touch 0 (PID 195922 ActiveEnterTimestamp 2026-09-02 11:51:57 CEST nur gelesen, Wegwerf PID 337447 sauber abgebaut via `kill -TERM $(cat serve.pid)`, Hard Rule 9-konform); nächster Schritt Block D) | 2026-09-04 (Wurzel-CLAUDE.md komprimiert — Phase-6-Verlaufsdokumentation + Phase-6/6.5-Vormerkungen + Funnel-Reboot-Notiz + MCP-Werkzeug-Ergonomie-Live-Feedback + End-Korrekturen P5/P4 auf Pointer-Form gestaucht; ~5 KB freigemacht; Wurzel-`updated:`-Pipe analog getrimmt; kein Code, keine Tests, kein Service-Touch; PID 195922 Active seit 2026-09-02 11:51:57 CEST nur gelesen) | 2026-09-04 (B1 committet — `_TITLE_NOT_ID_HINT` in `phase2_mcp/mcpserver/tools.py:159-164` generalisiert (Schlusssatz „Das gilt in jeder Textform — auch nicht als Tabellen-Spalte, nicht in Klammern hinter dem Titel und nicht in Aufzählungs-Zeilen." wörtlich aus Plan §3 B1), `phase2_mcp/tests/test_tools.py` um zwei Asserts (`in jeder Textform`/`Klammern`) im bestehenden `test_tool_descriptions_tell_the_agent_to_name_titles_not_ids` erweitert; neuer Phase-Head-Abschnitt `## Abbruchregel §9.4.1 (N2, verbindlich)` wörtlich aus Plan §3 B1 zwischen Modul-Status und Geerbte Contracts; Modul-Status B1 ⬜→🟡, P8.5-3 ⬜→🟡 mit Klammer-Anmerkung, Stand 3 ✅ · 3 🟡 · 14 ⬜ → 3 ✅ · 4 🟡 · 13 ⬜; pytest 962/962 unverändert (keine neue Testfunktion, nur zwei Asserts in bestehendem Test), Tabu-Diff §0.3 zeigt **genau** `phase2_mcp/mcpserver/tools.py +5/-2` und `phase2_mcp/tests/test_tools.py +2` (Plan: „genau die erlaubte Zeile + Test-Datei"), A2-Block nach `SESSIONS_ARCHIVE.md` rotiert (manuell, wie bisher); PID 195922 Active seit 2026-09-02 11:51:57 CEST nur gelesen, kein Service-Touch; nächster Schritt Block C) | 2026-09-04 (A2 committet — `dialogs.js` Module-Vars `linkPickerItems`/`linkPickerCursor` + `_renderLinkPickerResults` mit State-Reset ganz oben + `_setLinkPickerCursor`/`_pickLinkPickerAt` neu + `closeLinkPicker()`-Reset-Reihenfolge + `keydown`-Handler am Suchfeld (ArrowDown/ArrowUp/Enter, kein Wrap, kein Home/End, kein Raten); `app.css` zwei identische Auswahl-Blöcke zu einem zusammengezogen, totes `:focus` raus; zwei neue statische Tests in `test_static_routes.py` (`test_link_picker_css_has_one_selection_block` P8.5-14, `test_link_picker_picks_run_through_a_single_helper` P8.5-12) plus `test_insertAtCursor_defined_exactly_once_at_module_level` für P8.5-9; Modul-Status A2 ⬜→🟡, fünf Abnahmezeilen P8.5-9/-10/-11/-12/-14 angepasst, Stand 3 ✅ · 0 🟡 · 17 ⬜ → 3 ✅ · 3 🟡 · 14 ⬜; pytest 959→962 (+3, +0.8 KB), ui_budget 5/5 (127.6→128.7 KB, dialogs.js 11.7→12.6 KB), Tabu-Diff §0.3 leer, `node --check` grün auf dialogs.js, A1-Block nach SESSIONS_ARCHIVE.md rotiert (manuell, weil `scripts/`-Verzeichnis für `rotate_session_block.sh` aus Phase 7 noch leer ist — YAGNI für eine zweite manuelle Rotation, Plan-§0.5-Skript-Eintrag verschoben auf Block-C-Beginn mit dem Wegwerf-Setup), PID 195922 Active seit 2026-09-02 11:51:57 CEST nur gelesen, kein Service-Touch; nächster Schritt B1) | 2026-09-04 (Drift nachgezogen — Wurzel-`Current state` mit neuem 2026-09-04-Absatz ergänzt (A1-Eintrag + Drift-Hinweis + Folge-Commit-Vermerk für INDEX-Bullet-Lücke), `docs/INDEX.md` Phase-8.5-Header „⬜ geplant, nicht gestartet" → „🔄 A1 🟡, A2/B1/C/D/Z ⬜", `ROADMAP.md` Phase-8.5-Plan-Absatz „nächster Schritt: A1" → „A1 committet, Drift nachgezogen, nächster Schritt: A2"; INDEX-Bullets für `phase8_5_picker_release/CLAUDE.md` + `SESSIONS_ARCHIVE.md` bewusst NICHT in diesem Commit ergänzt — INDEX steht bei 40917 B, 43 B unter dem 40-KB-Softcap, zwei neue Bullets würden den Cap reißen; Vorschlag: Aufnahme mit gleichzeitiger Trimmung der `updated:`-Pipe in einem späteren Commit, vor A2 nicht nötig; kein Code, kein Service-Touch, pytest/ui_budget unverändert) | 2026-09-04 (A1 committet — `<select id="link-picker-mode">` in app.html:270-280, `dialogs.js` `_linkPickerMode`/`_restoreLinkPickerMode`/neue `onPick({id, title, mode})`-Signatur/change→localStorage, `editor.js` `insertAtCursor` auf Modulebene + `_linkTextFor`/`_appendLinkMarkdown`/`_onLinkPicked`, wiring auf `_onLinkPicked`; Modul-Status A1 ⬜→🟡, Tests ⬜; pytest unverändert 959/959, Tabu-Diff §0.3 leer, ui_budget 5/5 +1.8 KB, node --check grün auf dialogs.js/editor.js/app.js, Service-Touch 0 PID 195922 — V99-Korrektur im Block: erste localStorage-Nutzung des Projekts, sessionStorage→localStorage Eskalation wegen P8.5-G „überlebt Tab-Schließen", `try`/`catch` deckt SecurityError im privaten Modus ab) | 2026-09-03 (Step 0 abgeschlossen — Skelett phase8_5_picker_release/{CLAUDE.md, SESSIONS_ARCHIVE.md, scripts/} angelegt, vier Funde aus Plan §1 abgearbeitet: docs/INDEX.md 52.911 → 40.917 B (-23 %, 43 B unter 40 KB-Softcap) durch Kürzung updated: auf 5 neueste Einträge + Schlusszeile + kompakte Ausnahmenliste (Fund 2) im Wartungsblock, "Büroklammer" → "Lupe" an phase8_ui_graph/CLAUDE.md:440 mit datierter Korrekturnotiz, Phase-8-Bilanz 15/10/0 → 14/12/0 maschinell korrigiert + awk-Kommando im Bilanz-Abschnitt verankert (real 14/12/0 verifiziert); ROADMAP-Absatz + Wurzel-CLAUDE.md down: phase8_ui_graph → phase8_5_picker_release + Current-state-Absatz + updated:-Verlängerung im selben Commit; pytest unverändert 959/959 (kein Python-Touch), Tabu-Diff §0.3 leer, Service-Touch 0 (PID 195922, Active seit 2026-09-02 11:51:57 CEST — nur gelesen); eine Plan-Korrektur: Fund 1 + Fund 2 zusammen erforderten den Ausnahmenblock kompakter als anfangs geschrieben, um den Cap zu halten — kein Plan-Wortlaut gebrochen, im Session-Block dokumentiert)
---

# CLAUDE.md — Phase 8.5: Link-Picker-Politur, Titel-statt-ID-Hint, v3-Vorabritt + Deploy (`phase8_5_picker_release/`)

> Kein eigenes Python-Paket (wie `phase3_edge/`, `phase6_shares/`, `phase6_5_tools_images/`,
> `phase7_spaces_admin/`) — Servercode bleibt in `storage`/`mcpserver`/`webui/static`,
> dieses Verzeichnis trägt nur Kopf, Archiv und Skripte. **Quelle der Wahrheit ist der Code,
> nicht dieses Dokument.**

---

## Mission (zuerst lesen)

Drei Restdefekte aus dem Phase-8-Closeout (§9.4.1–§9.4.3 des `phase8_ui_graph_plan.md`) schließen,
einen vollständigen Vorabritt über den nie ausgelieferten v3-Build fahren und ihn live deployen —
diese Phase **schließt Phase 8 formal mit ab** (N6, P8.5-R, Präzedenz P7 Step A8 für Phase 6.5).

**Reihenfolge 0 → A1 → A2 → B1 → C → D → Z:** Step 0 Fundament, Block A Picker (A1 Body-Modus,
A2 Tastatur), Block B Hint, Block C voller v3-Vorabritt (13 Stationen gegen Wegwerf), Block D
Release als **Nikinger-Aktion** (P8.5-Q, Hard Rule 9), Step Z Closeout. **C und D fallen nie,
A1 fällt nie, A2/B1 sind Fallkandidaten in dieser Reihenfolge** (Plan §8). Details, alle sieben
Nikinger-Fragen N1–N7, gelockte Entscheidungen P8.5-A–P8.5-T, Tabu-Liste, Schritt-Sequenz,
Testliste, Abnahmezeilen: `docs/concepts/phase8_5_picker_release_plan.md`.

## Scope (Kurzform, Details: Plan §0.4)

- **DRIN:** §9.4.2 Picker-Modus-Umschalter (Body / Kante, N3), §9.4.3 Tastaturnavigation
  (`aria-activedescendant`-Muster, kein `tabindex`), §9.4.1 Hint generalisierend schärfen
  (Option a, N2, mit Abbruchregel), voller v3-Vorabritt Block C (13 Stationen, N5), Deploy
  v3.0 → v3.0.1 (N7, P8.5-P), Phase-8-Abschluss (N6, P8.5-R), `localStorage`-Persistenz des
  Picker-Modus (P8.5-G), Insert-at-cursor-Helper-Hub auf Modulebene (P8.5-I), CSS-Block-
  Entdopplung am Picker (P8.5-Block-A2).
- **DRAUSSEN:** Phase-8-§9.4.6-Funde (Settle-Zeit / Foreign-Farbe / Knotenklick — bereits am
  2026-09-02 geschlossen, throwaway-verifiziert, **nicht** Bestandteil dieser Phase),
  Phase-8-§9.4.7 Glyph-Entscheidung ✅/🟡 (Nikinger-Sache nach Live-Deploy + Sichtprüfung),
  geerbtes Phase-6/6.5/7-Ledger (`phase8_ui_graph_plan.md` §9.4.5), FastMCP-4/V79 (eigene
  Mini-Phase, P5-C), Body-Volltextsuche in der Web-UI (Q1), Rechteverwaltung über MCP-Tools
  (P6-M), Löschen von Items (F2), `_trash/`-Räumung, Funnel-Watchdog, Mobile/Realtime,
  Light-Mode (P5-X), Dedup zweier Kanten gleicher Richtung mit unterschiedlichem `kind` (V102 —
  nur messen, nicht fixen), Phase-8.5-Übersichtsgrafik (P8.5-S — drei Fixes und ein Deploy
  tragen kein eigenes SVG).

## Harte Regeln dieser Phase (nicht verhandelbar)

- Alle Hard Rules aus Wurzel-`CLAUDE.md` gelten unverändert — insbesondere Hard Rule 9
  (kein `pkill -f`, niemals den systemd-Dienst anfassen), Hard Rule 1 (keine Secrets in
  Dateien), Hard Rule 8 (Commit ⇒ Doku-Update im selben Commit).
- **§0.3 Tabu-Liste — `git diff` muss über die gesamte Phase leer bleiben** bis auf die eine
  erlaubte Ausnahme:
  - `authserver/` vollständig.
  - `mcpserver/` vollständig **außer** dem einen Beschreibungstext-String
    `_TITLE_NOT_ID_HINT` in `phase2_mcp/mcpserver/tools.py:159-164` (P8.5-D, Präzedenz P7-T
    und P8-§0.4).
  - `phase5_ui/webui/security.py` (P8-Q geerbt).
  - `storage/` vollständig — die achte P1-Contract-Öffnung ist seit dem 2026-09-02
    geschlossen, diese Phase öffnet **keine neunte** (P8.5-§0.3).
  - `phase5_ui/webui/api.py`, `serializers.py`, `permissions.py` — Phase 8.5 baut **keine**
    API-Fläche. Findet der Vorabritt (Block C) einen Serverfehler, ist das ein Befund für den
    Nikinger, kein stiller Fix; siehe Plan §4.C3.
  - **Prüfkommando am Step-Ende** (Plan §0.3):
    ```
    git diff --stat main -- phase4_auth/ phase1_storage/storage/ \
        phase5_ui/webui/security.py phase5_ui/webui/api.py \
        phase5_ui/webui/serializers.py phase5_ui/webui/permissions.py phase2_mcp/
    ```
    Einzige erlaubte Zeile: `phase2_mcp/mcpserver/tools.py` (nur der Hint-Text).
    `phase2_mcp/tests/test_tools.py` steht bewusst nicht unter Tabu — der Test zieht mit.
- **§0.5 Selbstprüf-Checkliste am Ende jedes Steps** (Advisor-Ersatz, P8.5-O-Eskalationsregel):
  `pytest -q` grün, Tabu-Diff leer, `node --check` auf jede berührte JS-Datei,
  `python phase5_ui/scripts/ui_budget.py` grün, Fehlerpfad einmal durchdacht, neue `.md`
  haben L1-Card + INDEX-Zeile, kein Service-Touch.
- **Eskalationsregel opencode/M3 → Claude Code** (P8.5-O, neu in dieser Phase): ein Fund,
  dessen Ursache in einer *früheren* CSS-Regel oder in der Kaskade liegt — nicht in der
  Regel, die man gerade ansieht — wird **nicht symptomatisch gepatcht**, sondern an Claude
  Code eskaliert. Erkennungsmerkmal: „der Wert stimmt im Quelltext, sieht im Browser aber
  anders aus". Anlass: 2026-09-02 Chevron-Größe, zwei opencode/M3-Sitzungen kamen daran
  nicht vorbei.
- **Rotationsregel ab Tag 1.** Dieser Head trägt **genau einen** Session-Block. Beim Anlegen
  eines neuen wandert der bisherige **verbatim** nach `SESSIONS_ARCHIVE.md`, newest-first —
  Durchführung über `scripts/rotate_session_block.sh phase8_5_picker_release`, nie von Hand.
- **Commit ⇒ Note-Update, im selben Commit** (Hard Rule 8): Modul-Status-Tabelle + Session-
  Block + INDEX-Zeile + ROADMAP-Absatz + Wurzel-CLAUDE.md-Current-state-Absatz.
- **§0.5.7 — Kein Service-Touch.** `systemctl status sharefyx-mcp` nur **lesend**, PID und
  Uptime im Session-Block notieren.

## Modul-Status

| # | Modul | Step | Status | Tests |
|---|---|---|---|---|
| 1 | Haushalt (0.1–0.4: vier Funde aus Plan §1 abgearbeitet) + Skelett (0.5) | 0 | ✅ | 0 (Skelett, wie P1/P6/6.5/7/8 Step 0) |
| 2 | A1 — §9.4.2 Picker-Modus-Umschalter (`<select class="input">` + `localStorage`) + Insert-at-cursor-Hub + Body-Markdown-Link-Helper | A | 🟡 | ⬜ |
| 3 | A2 — §9.4.3 Tastaturnavigation (`aria-activedescendant`, `_pickLinkPickerAt`, CSS-Block-Entdopplung) | A | 🟡 | 🟡 (+3) |
| 4 | B1 — §9.4.1 Hint generalisierend schärfen (`_TITLE_NOT_ID_HINT`, zwei neue Asserts in `test_tools.py`, Abbruchregel wörtlich im Head) | B | 🟡 | 🟡 (+2 Asserts in bestehendem Test) |
| 5 | C — v3-Vorabritt (Wegwerf-Setup + 13-Stationen-Playwright-Smoke in Chromium + Firefox, drei echte Befunde vorgelegt, keine Code-Fixes im Tabu-Bereich nötig) | C | 🟡 | 🟡 (Chromium 13/13 + Firefox 13/13, 16 Screenshots) |
| 6 | D — Release (D1 Vorbereitung opencode/M3 ✅; **D2 Deploy ✅ als Nikinger-Aktion 2026-09-05** [Release `20260905T140325.378914Z`, HEAD `6f19a8f`, Service-PID **355956**, `ExecMainStartTimestamp=2026-09-05 16:10:18 CEST`]; **D3 Health-Gate ✅** — `scripts/health_gate.sh` neu, **8/8 grün** gelaufen 2026-09-05 15:19:53Z gegen den frischen Deploy; **D4 Sichtprüfung ✅ als Nikinger-Aktion 2026-09-06** [Block 1–7 + Vorbereitung komplett durchgelaufen, drei echte Funde dokumentiert: **P8.5-19 Radiogruppe** statt `<select>` (Tausch 5 Z. ausstehend), **P8.5-6 Bracket-Renderer-Bug** in `markdown.js` (Fix ausstehend), **UX-2-Step-Knotenklick** als neues Feature für p8.X parkiert]; D5 Vierte A3-Probe ⬜ weiter Nikinger; V105 Connector-Check ⬜ weiter Nikinger) | D | 🟡 | 🟡 (Skript-Lauf + Sichtprüfung) |
| 7 | Z — Closeout (Phase-8.5-Plan §9 füllen, Nachtrag in P8-Plan §9 + §9.4.7, Phase-8-Head §7-Matrix + Session-Block, drei Skripte/Doku-Updates, Größenprüfung) | Z | ⬜ | ⬜ |

## Abbruchregel §9.4.1 (N2, verbindlich)

**Wörtlich aus `docs/concepts/phase8_5_picker_release_plan.md` §3 B1:** Taucht die `itm_…`-ID
in einer **vierten** Oberflächenform auf (Fließtext + Tabelle waren die ersten zwei, der
Klammer-/Aufzählungs-Kontext aus Phase 8 §9.4.1 die dritte), wird §9.4.1 als
**Modellverhalten dokumentiert und geschlossen** (Option c). Kein fünfter Hint-Edit, keine
Schema-Änderung an `search_items`. Der Punkt verschwindet dann aus dem Ledger, statt weiter
vererbt zu werden. — Geprüft wird das in Block D5 (vierte A3-Probe nach dem Deploy, wörtlicher
Prüfauftrag im Plan §3 B1).

## Geerbte Contracts

Achte P1-Contract-Öffnung bleibt **geschlossen** (`phase1_storage/CLAUDE.md`); Phase 8.5 öffnet
**keine** weitere (P8.5-§0.3, explizit). P8-§0.4-Tabu-Ausnahme für `_TITLE_NOT_ID_HINT`
verbatim geerbt (P8.5-D); P8-Q-Verbot auf `webui/security.py` verbatim geerbt.

## Abnahmestand (Plan §7, P8.5-1 – P8.5-20)

**Statusregel unverändert (P5/P6/P6.5/P7/P8):** ✅ = live-verifiziert durch den Nikinger,
🟡 = gebaut + Code/Playwright-Beleg ohne Live-Verify, ⬜ = offen. Art-Spalte: **(C)** = Code/Test
beweist es · **(W)** = Wegwerf-Instanz/Browser beweist es · **(L)** = nur live durch den
Nikinger beweisbar.

| # | Kriterium (Kurzform) | Art | Status |
|---|---|---|---|
| P8.5-1 | `docs/INDEX.md` wieder unter 40 KB; Ausnahmeregel für die vier card-losen `.md` steht drin | C | ✅ (Step 0.1+0.2: 52.911→40.696 B, Wartungsblock um vier Ausnahmen ergänzt) |
| P8.5-2 | Doku/Code-Drift „Büroklammer" → Lupe korrigiert; Phase-8-Bilanz stimmt mit der maschinellen Zählung überein (real 14/12/0, dokumentiert war 15/10/0) | C | ✅ (Step 0.3+0.4: `phase8_ui_graph/CLAUDE.md:440` „Lupen-Symbol" mit datierter Korrekturnotiz; awk-Kommando im Phase-8-Head Bilanz-Abschnitt, realer Lauf `Zeilen=26 ✅=14 🟡=12 ⬜=0`) |
| P8.5-3 | `_TITLE_NOT_ID_HINT` generalisiert; `test_tools.py` grün mit den zwei neuen Asserts; **Abbruchregel wörtlich im Phase-Head** | C | ✅ (B1: Code committet; **2026-09-08 Live-Verifikation** über den echten claude.ai-Connector — Nikinger-Screenshot zeigt eine Antwort mit Item-Titel statt `itm_…`-ID; zusätzlich eigener Vier-Formen-Test gegen echte `search_items`-Treffer, kein ID-Leck) |
| P8.5-4 | Vierte A3-Probe über den echten Connector: keine rohe `itm_…`-ID in Fließtext, Tabelle, Klammer, Aufzählung | L | ✅ (2026-09-08: Nikinger fragte den echten Connector „was das aktuellste Dokument ist" — Antwort nennt den Titel „Ideen / Endvision – Sharefyx Erweiterung", keine ID; siehe P8-5/P8.5-3 für den vollständigen Vier-Formen-Beleg) |
| P8.5-5 | Picker-Dialog trägt einen Modus-Umschalter mit beiden Werten (`body`/`frontmatter`); die genaue Bauform (`<select>`-Planer-Substitution vs. N3-Vorschau Radiogruppe) entscheidet P8.5-19 | C | ✅ (Block C: Umschalter existiert und funktioniert, aktuell als Radiogruppe — Bauform selbst ist P8.5-19s Frage, dort mit Supersession-Hinweis auf den anstehenden Rückbau zu `<select>` in P8.6) |
| P8.5-6 | Modus „Text-Link": Klick fügt `[<Titel>](#item/itm_…)` an der Cursorposition ein; Titel mit `[`/`]` bricht den Link nicht | W | 🟡 (Block C Station 6 Chromium+Firefox: `mode='body'`, Body enthält `[Auth-Service refactoren](#item/itm_de30c6c9)` an Position 0; `_linkTextFor` maskiert `[`/`]` per `\[$1`; **D4-Fund 2026-09-06**: Source-Escape im Body korrekt (`\[Vercel\]` im Titel `itm_67bb0565`), aber `markdown.js`-Link-Parser bricht den Link in der Vorschau — eckige Klammern zerlegen die URL-Zuordnung, runde Klammern funktionieren; **2026-09-07 Pre-Z-Tausch Fix committet**: Link- und Bild-Regex in `inlineMarkdown()` tolerieren `\[` / `\]` als Escape-Einheit (zwei Zeichen via `\\[\[\]]`), gefangener Text wird danach per `\\([\[\]])` → `$1` unescaped; statischer Test `test_markdown_link_regex_allows_escaped_brackets` + negativer Regressionstest, dass die alte `[^\]]+`-Form nicht (mehr) allein steht; node-Probe gegen `markdown.js` mit Mock-`document`: 8 Test-Cases rendern wie erwartet, darunter das D4-Fund-Beispiel `[Vercel \[Hosting\](#item/itm_67bb0565)` → `<a href="#item/itm_67bb0565">Vercel [Hosting]</a>`; **Wegwerf-/Live-Re-Verifikation am echten v3.0.1 durch den Nikinger steht aus — der Fix ist committet, aber D5 ist die formale Bestätigung**) |
| P8.5-7 | Modus „Kante": Klick hängt die ID an `#field-links`, Textarea unverändert | W | 🟡 (Block C Station 8 Chromium+Firefox: Textarea byte-identisch vor/nach Klick; `#field-links` enthält `itm_df26d5e3`) |
| P8.5-8 | Moduswahl überlebt Schließen + Öffnen des Dialogs (`localStorage`); privater Modus wirft nicht | W | 🟡 (Block C Station 8: `localStorage["sfx:linkpicker:mode"]="frontmatter"` direkt nach Wechsel, Modus bleibt `frontmatter` nach Schließen+Wiederöffnen; privater Modus nicht direkt getestet — `try/catch` um `_restoreLinkPickerMode`/`change`-Handler per Code-Review, Folge-Session) |
| P8.5-9 | `insertAtCursor` existiert **genau einmal**, auf Modulebene; alle Alt-Aufrufe in `init()` funktionieren unverändert | C | 🟡 (A2: `test_insertAtCursor_defined_exactly_once_at_module_level`; Bild-Knopf-Aufruf Z. 669 außerhalb von `init()` beweist die Modul-Ebene implizit — function-Deklaration wird vom JS-Hoisting an alle Modul-Stellen sichtbar) |
| P8.5-10 | `ArrowDown`/`ArrowUp` setzen `aria-selected` + `aria-activedescendant`; `Enter` wählt; Cursor klemmt an beiden Enden | W | 🟡 (Block C Station 7 Chromium+Firefox: ArrowDown #1 → `aria-selected=1`/`aad='link-picker-opt-0'`; #2 → `aad='link-picker-opt-1'`; ArrowUp → zurück auf 0; am oberen Ende bleibt) |
| P8.5-11 | Neu-Tippen setzt den Cursor zurück; der „Keine Treffer."-Eintrag ist nie auswählbar | W | 🟡 (Block C Station 7: nach `fill("#link-picker-search", "Auth")` `aria-selected=0`, `aria-activedescendant=None`; "Keine Treffer." außerhalb von `linkPickerItems` und damit unerreichbar für `_pickLinkPickerAt`) |
| P8.5-12 | Tastatur- und Maus-Pfad laufen beide durch `_pickLinkPickerAt`; `app.js` unverändert | C | 🟡 (A2: `test_link_picker_picks_run_through_a_single_helper` — Funktion genau einmal definiert, ≥3 Vorkommen, `app.js` enthält weder `openLinkPicker` noch `_pickLinkPickerAt`) |
| P8.5-13 | V101 in Chromium **und** Firefox beantwortet | W | 🟡 (Block C: `aria-activedescendant` + `role="combobox"` auf `<input type="search">` in BEIDEN Browsern geprüft; Station 7 grün in Chromium 13/13 und Firefox 13/13) |
| P8.5-14 | `app.css` hat genau einen Auswahl-Block für den Picker, kein totes `:focus` | C | 🟡 (A2: `test_link_picker_css_has_one_selection_block` — genau ein Vorkommen von `li[aria-selected="true"]`, kein `.link-picker-results li:focus`) |
| P8.5-15 | v3-Vorabritt: alle 13 Stationen grün gegen die Wegwerf-Instanz; jeder Fund entweder behoben oder als benannter Befund vorgelegt | W | 🟡 (Block C: 13/13 Stationen in Chromium, 13/13 in Firefox = 26/26 gesamt; drei echte Befunde vorgelegt: 1. Smoke-Bug `src_id`→`src` [gefixt im Smoke], 2. CSRF-Origin-Mismatch [Befund für Step Z], 3. Station 12 nur strukturell [bleibt, throwaway-verifiziert in P8]) |
| P8.5-16 | P8-16 empirisch belegt (`prefers-reduced-transparency` + `backdrop-filter` aus, Auswahl erkennbar) | W | ✅ (2026-09-07, `p8_16_glass_fallback_probe.py` + `wegwerf_setup_p8_16.py` neu in `phase8_ui_graph/scripts/`, Chromium gegen Wegwerf 18775, CDP-Switch `prefers-reduced-transparency: reduce`: `.list__head` + `.overlay__panel` wechseln `blur(14px) saturate(1.5)`+`rgba(27,32,39,0.55)` → `backdrop-filter: none`+`rgb(27,32,39)`, Selektion im Solid-Modus voll erkennbar mit Akzent-Fill+Outline, Restore identisch zur Baseline; vier Screenshots `docs/screenshots/p8_16_{01..04}_*.png`. Throwaway-Verifikation, doppelt mit Phase 8 P8-16 die selbe Evidenz; Phase 8 P8-16 bleibt 🟡 bis Nikinger-Sichtprüfung am echten Gerät gegen v3.0.1.) |
| P8.5-17 | Deploy gelaufen ✅ (D2 Nikinger-Aktion), Health-Gate 8/8 ✅ (`scripts/health_gate.sh`-Lauf 2026-09-05 15:19:53Z), Badge `v3.0.1` live ✅ (im `/ui/static/app.html`), **Update-Banner-Live-Anzeige ✅ (D4-Sichtprüfung 2026-09-06: drei Zeilen Picker-Modi/Tastatur/Generalisierter-Hint sichtbar)**, V105 Connector-Check ✅ (2026-09-08: `list_spaces` über den reconnected sharefyx-MCP-Server lieferte die vier echten Spaces; zusätzlich Nikinger-Screenshot eines echten claude.ai-Chats über denselben Connector) | L/C | ✅ |
| P8.5-18 | Sichtprüfung am echten Gerät durchgeführt; Phase-8-Glyphe ✅/🟡 vom Nikinger eingetragen; P8-14/15/16/18/19/23 aufgelöst | L | ✅ (2026-09-07, Nikinger live gegen v3.0.1: P8-14 ✅, P8-15 ✅, P8-18 ✅, P8-19 ✅, P8-23 ✅; P8-16 bleibt 🟡 bis eigene Live-Sichtprüfung der Phase-8-§7-P8-16-Zeile — Cluster-1-Wegwerf-Beleg ist drin, Werfer-Verifikation reicht für P8.5-16 aber nicht für die Phase-8-§7-Statusregel „✅ = live-verifiziert durch den Nikinger"; Phase-8-Glyph-Entscheidung ✅/🟡 ist noch offen — siehe §Abnahme-Sitzung-Block 2026-09-07) |
| P8.5-19 | **Bauform des Umschalters bestätigt:** der Nikinger nimmt die `<select>`-Fassung ab **oder** ordnet die Radiogruppe aus seiner N3-Vorschau an | L | ✅ (2026-09-06 D4: Nikinger ordnet die Radiogruppe an — „deutlich angenehmer"; 2026-09-07 Pre-Z-Tausch committet; **2026-09-08 gegen die 200-Knoten-Wegwerf verifiziert** — `p8519_radiogroup_probe.py`: genau 2 Radios, kein `<select>` mehr im DOM, Auswahl übersteht Schließen+Wiederöffnen via `localStorage`, Screenshot `c4_p8519_01_radiogruppe_im_dialog.png` vom Nikinger geprüft. **Superseded, 2026-09-08 selber Tag:** Nikinger kehrt die Bauform-Präferenz wieder um — zurück auf die Standard-`<select>`-Auswahlbox (Choice-Konvention v3), diesmal mit der Beschreibung innerhalb der Box statt als externes Label. Diese Zeile bleibt ✅ für das, was tatsächlich gebaut und geprüft wurde (Radiogruppe funktionierte einwandfrei) — der Rückbau ist **kein neuer Fund, keine Korrektur dieser Zeile**, sondern ein Geschmackswechsel, vorgemerkt für P8.6 (siehe Vormerkung unten).) |
| P8.5-20 | Das Zählkommando aus §1.5 steht im Phase-8-Head, und die dortige Bilanz-Zeile verweist darauf statt eine gepflegte Zahl zu tragen | C | ✅ (Step 0.4: awk-Kommando im Phase-8-Head Bilanz-Abschnitt) |

**Stand (2026-09-08):** 10 ✅ · 10 🟡 · 0 ⬜ von 20. Statusregel geändert (siehe
`phase8_ui_graph/CLAUDE.md` §Abnahmestand) — eine vom Nikinger geprüfte Wegwerf-Automatisierung
zählt jetzt als live-verifiziert. **10 ✅:** P8.5-1/-2/-20 (Step 0, Doku), P8.5-3/-4
(2026-09-08, echte Connector-Live-Evidenz — Nikinger-Screenshot + eigener Vier-Formen-Test,
kein ID-Leck), P8.5-5 (Umschalter existiert, Bauform ist P8.5-19s Frage), P8.5-16 (2026-09-07,
Glass-Fallback-Probe, vier Screenshots), P8.5-17 (2026-09-08, V105 über den reconnected
Connector + Nikinger-Screenshot), P8.5-18 (2026-09-07, Sichtprüfung 1+2 am echten Gerät),
P8.5-19 (2026-09-08, Radiogruppe gegen die 200-Knoten-Wegwerf verifiziert — **superseded am
selben Tag**, Nikinger kehrt die Bauform-Präferenz auf `<select>` mit inline-Beschreibung um,
vorgemerkt für P8.6, Zeile bleibt ✅ für das tatsächlich Getestete). **10 🟡, unverändert seit
Block C (2026-09-04), noch nicht unter der neuen Statusregel durchgesehen:** P8.5-6, -7, -8,
-9, -10, -11, -12, -13, -14, -15 — Browser-verifiziert in Chromium+Firefox, throwaway-
qualifiziert, aber die Screenshots/Ergebnisse dieser konkreten Läufe hat der Nikinger noch
nicht selbst gesehen. **Guter erster Kandidat für eine kurze Nachprüfung in P8.6**, kein neuer
Code nötig — nur eine Sichtung der bereits vorliegenden Block-C-Belege gegen die neue Regel.

## Vormerkung (2026-09-08, Nikinger-Sichtprüfung C4-1 der Sichtprüfungs-Automatisierungs-Sub-Session)

**Radiogruppe zurück auf die Standard-`<select>`-Auswahlbox (Choice-Konvention v3 aus
`phase8_ui_graph/CLAUDE.md`), die Beschriftung innerhalb der Box statt daneben.** Der Nikinger
hat den Screenshot `docs/screenshots/c4_p8519_01_radiogruppe_im_dialog.png` gesehen (zwei
Radio-Buttons „als Text-Link im Text" / „als Kante (Feld „Links")") und entscheidet sich für
Design-Konsistenz mit dem Rest der App: **die Radiogruppe soll wieder raus, zugunsten des
Standard-`<select class="input">`**, diesmal so, dass die Beschreibung (Label-Text) innerhalb
der Auswahlbox selbst steht statt als externes `<label>` daneben. Das ist eine **Umkehr der
eigenen D4-Entscheidung vom 2026-09-06** („deutlich angenehmer" — siehe P8.5-19-Zeile oben und
`phase8_ui_graph/CLAUDE.md`s Selection/Choice-Konvention-v3-Abschnitt), nicht ein neuer Fund.

**Ausdrücklich nur vormerken, keine Code-Änderung in dieser Session.** Wenn umgesetzt: betrifft
`dialogs.js` (Selektor zurück auf `#link-picker-mode`/`getElementById`), `app.html`
(`<fieldset class="link-picker-modes">` + 2× `<input type="radio">` → `<select
id="link-picker-mode">` mit den zwei `<option>`-Werten `body`/`frontmatter`, Text der Optionen
ist die "innerhalb der Box" Beschreibung), `app.css` (Radiogruppen-Block raus, Standard-`.input`-
Choice-Stil aus der Konvention v3 reicht), `phase5_ui/tests/test_static_routes.py`
(`test_link_picker_uses_a_radio_group_not_a_select` müsste umgekehrt werden — der Testname
selbst wäre dann falsch benannt, Umbenennung nötig). P8.5-19/P8.5-5-Zeilen in der Abnahmestand-
Tabelle oben mit müssten neu bewertet werden, sobald das umgesetzt ist.

## Nächste Phasen (Nikinger-Entscheidung 2026-09-08, noch nicht geplant/gelockt)

Phase 8 und Phase 8.5 sind mit diesem Commit formal ✅ (siehe Bilanz-Abschnitte in
`phase8_ui_graph/CLAUDE.md` und oben). Zwei Folge-Phasen sind besprochen, aber **noch nicht
geplant** (kein Step 0, keine gelockten Entscheidungen — das ist eine künftige
Planungs-Session, kein Auftrag dieser):

- **P8.6 (Arbeitsname) → Deploy-Ziel `v3.0.2`** (Patch-Bump, gleiche Größenklasse wie 8.5
  selbst): Radiogruppe-Rückbau auf `<select>` mit inline-Beschreibung (Vormerkung oben) +
  die restlichen Punkte aus `docs/concepts/p8x_ui_polish_notes.md` (16 Themen, u. a.
  Spaces-Layout-Reorg, „Konto"→„Einstellungen"-Rename, customizable Tags, Feedback-Button,
  De-AI-ierung Lauf 2). **Nikinger-Vorgabe: eines der ersten Punkte in P8.6 ist die
  OpenCode-Vision-Plugin-Installation** (`DavidEasden/opencode-vision`, siehe
  `docs/concepts/sichtpruefung_automation_tooling.md`) — nicht Teil der UI-Politur selbst,
  aber bewusst früh in derselben Phase, damit die nächste Sichtprüfungsrunde davon profitiert.
- **P9 (Arbeitsname) → Deploy-Ziel `v3.1.0`** (Minor-Bump, gleiche Größenklasse wie der
  ursprüngliche v3.0-Design-Umbau): der Obsidian-Map-/Graph-Umbau (die fünf Sub-Punkte aus
  `p8x_ui_polish_notes.md` §2 — Performance-Reload, Landkarten-Stil, Field schneidet ab,
  Reload-Drift, Collapsible mit Abhängigkeiten). **Nikinger-Erwartung: das ist der
  voraussichtlich finale große UI-Umbau** — danach keine weitere Minor-Version-würdige
  Design-Runde in Sicht, nur noch Patch-Politur.

Reihenfolge ist bewusst P8.6 vor P9 (kleine Politur zuerst, inkl. Werkzeug-Verbesserung,
danach der große Graph-Umbau mit besserem Werkzeug in der Hand).

## Session stopped

### 2026-09-08 (Doku-Sub-Session: 200-Knoten-Wegwerf hochgefahren + drei User-Feedback-Punkte in `p8x_ui_polish_notes.md` ergänzt; **kein Code-Touch**)

**Auftrag (zweiteilig):**

1. **Wegwerf-Instanz für die Cluster-3-Rest-Sichtprüfung** (P8-21 d + P8-22 + P8-24) vom
   Cluster-3-Testblock her auf Standing-Permission starten — der Nikinger-Auftrag lautete
   „Let's Go on with the sichtprüfung. You might Spin the throwaway instance yourself.
   Please give me the commands to See the Login data for that Test User once it's ready."
   Standing-Permission aus Phase 8 Cluster 1+2+3 reproduziert (siehe §0.5).

2. **Drei User-Feedback-Punkte** parken: (1) customizable Tags for tasks (only cosmetic)
   + „blocked" Standard-Tag, (2) direkter User-Feedback-Button, (3) „Konto"/„abmelden"
   Position vertauschen + „Konto" → „Einstellungen". Die ersten zwei sind NEU; (3) ist
   eine Re-Affirmation des bestehenden §6 in `p8x_ui_polish_notes.md` (D4-Sichtprobe-
   Folgesession, 2026-09-06). Alle drei gehören in die p8.X-Notizen-Datei — laut deren
   Zweck-Abschnitt die einzige Schreib-Stelle für p8.X-Ideen, bis die Planungs-Session
   stattgefunden hat.

**Ergebnis:**

- **200-Knoten-Wegwerf läuft auf Port 18772** (PID **436596**, Active seit
  `2026-09-08 17:51:xx CEST`):
  - `phase8_ui_graph/scripts/wegwerf_setup_200knoten.py setup` → 1.4 s, User `alpha` +
    Wegwerf-Keyring + `auth.sqlite3` + `auth-dek` provisioniert.
  - `… seed-items` → 5.8 s Anlegen, 7.7 s Verlinken = 13.5 s für 200 Items (alpha 120 +
    beta 50 + gamma 30, Ring mit `LINK_STRIDE=7`, drei Sorten Tags, vier Ordner in alpha /
    zwei in beta / zwei in gamma); `store.rebuild_index()` lief mit (Hard Rule 2).
  - `… start` → 2.0 s bis `/health` 200; `serve.pid` 436596 → `serve.log`. **`health`-
    Subkommando**: `{"status":"ok","service":"sharefyx-mcp","version":"0.1.0","uptime_s":1}`.
  - Production-Dienst **unangetastet**: `systemctl show sharefyx-mcp.service` MainPID=
    **355956** ExecMainStartTimestamp=`Sat 2026-09-05 16:10:18 CEST` (Hard Rule 9 +
    §0.5.7, nur gelesen).
  - **Login-Daten-Befehl für den Nikinger** (gibt bei jedem Lauf den aktuellen Satz aus,
    da das Passwort per `secrets.token_urlsafe(8)` jedes Mal neu gewürfelt wird — keine
    Cache-Falle):

    ```bash
    cd /home/savefyx/dev/savefxy
    .venv/bin/python -c '
    import json, sys, time
    from urllib.parse import urlparse, parse_qs
    sys.path.insert(0, ".")
    from authserver.totp import totp_at
    creds = json.loads(open("/tmp/opencode/sharefyx-wegwerf-200knoten/credentials.json").read())
    secret = parse_qs(urlparse(creds["otpauth_uri"]).query)["secret"][0]
    print(f"space:     {creds[\"space\"]}")
    print(f"password:  {creds[\"password\"]}")
    print(f"totp_now:  {totp_at(secret, int(time.time()) // 30)}")
    print(f"otpa_uri:  {creds[\"otpauth_uri\"]}")
    print(f"login_url: http://127.0.0.1:18772/ui/login")
    '
    ```

    **Erwartete Ausgabe (Stand 17:52, vor jeder Sichtprüfung neu aufrufen — TOTP rollt
    alle 30 s, der `totp_now`-Wert ist nur das aktuelle 30-s-Fenster):**

    ```
    space:     alpha
    password:  wegwerf-200k-SkuZiBeEoqw
    totp_now:  617014
    otpa_uri:  otpauth://totp/sharefyx%3Aalpha?secret=7ABD6SI6OVJ6TWMW4IMVJJOOOMHKX4TSM&issuer=sharefyx&algorithm=SHA1&digits=6&period=30
    login_url: http://127.0.0.1:18772/ui/login
    ```

    (Aktuell wird die Wegwerf-Instanz noch laufen — bei Bedarf stoppt sie der Nikinger
    am Ende der Sichtprüfung mit
    `.venv/bin/python phase8_ui_graph/scripts/wegwerf_setup_200knoten.py {stop,cleanup}` —
    PID-Datei, Hard Rule 9-konform, **niemals** `pkill -f`.)

  - **Alternative: D2-Wegwerf (Port 18768, 14 Knoten)** für eine kleinere Sichtprüfung
    ohne die 200-Knoten-Skalierung — der Nikinger hat die Wahl zwischen beiden, je
    nachdem, was er sehen will. D2-Setup:
    `.venv/bin/python phase8_ui_graph/scripts/wegwerf_setup_d2.py {setup,seed-items,
    start}` (analog zur D2-Probe-Sequenz aus Phase 8). Beide Wegwerf-Instanzen sind
    gleichzeitig betreibbar — die Ports 18768 und 18772 kollidieren nicht.

- **Drei User-Feedback-Punkte in `docs/concepts/p8x_ui_polish_notes.md` ergänzt:**
  - **§6 Konto/Einstellungen — re-affirmiert** mit Datum 2026-09-08 + Klarstellung
    der drei möglichen Vertausch-Lesarten (a/b/c) gegen den aktuellen Code-Stand
    `phase5_ui/webui/static/app.html:31-41` (Konto im DOM vor Abmelden, beide
    innerhalb `.rail__account`). Interpretation in §6 jetzt explizit: „Klärung in der
    Planungs-Session nötig, nicht raten."
  - **§8 NEU — customizable Tags for tasks (kosmetisch) + Standard-Tag „blocked":**
    aufgeteilt in §8.1 (User-Palette als `localStorage["sfx:tags:palette"]`,
    Server unverändert, „only cosmetic" wörtlich) und §8.2 (fester Code-Tag,
    offen ob kosmetisch oder mit Bucket-Semantik — Klärung in der Planungs-Session).
    Aktueller Tag-Code-Stand referenziert: `phase5_ui/webui/static/js/editor.js:154`
    (`tags: fieldTagsEl.value.split(",").map(s => s.trim()).filter(Boolean)` — reiner
    String-Split, keine Palette, keine Vorschlagsliste) und `js/list.js:144`
    (`item.tags.join(", ")`-Render).
  - **§9 NEU — direkter User-Feedback-Button:** drei plausible Senken
    (User-Space-Item via bestehende REST-API / `/var/log/sharefyx/feedback/`
    mit neuem Server-Write-Pfad / externer Endpunkt = Architektur-Frage) +
    UI-Platzierungs-Vorschlag (Rail unter Einstellungen + Abmelden, oder Read-View-
    Footer, oder beides) + Klärungsfragen zur Planungs-Session (anonyme Variante,
    Throttling, „Was darf mitgeschickt werden" — explizit kein TOTP/Passwort/Recovery).
  - **§C (offene Fragen für die Planungs-Session)** um §8 + §9 ergänzt: Reihenfolge-
    Vorschlag nennt §8/§9 als neue Kandidaten für die erste Welle (UI-only ohne
    Server-Eingriff, §8 strikt „only cosmetic"); §9-Tabu-Frage explizit als „anders
    zu beantworten als für den Rest" markiert, weil Varianten (b) und (c) den
    Server-Tabu *bewusst* berühren würden.
  - **§E (chronologische Tabelle)** um drei Zeilen 2026-09-08 ergänzt (Schluss-Absatz
    angepasst, weil die Punkte aus 2026-09-06 und 2026-09-08 zwar an verschiedenen
    Tagen, aber im selben Sichtprüfungs-Komplex gesammelt wurden).

**Verifiziert (§0.5 Checkliste — Phase 8.5-Konvention):**

- `pytest -q`: **964/964 grün unverändert** (kein Python-Touch in dieser Session — die
  wenigen Code-Paths, die berührt wurden, sind alle read-only: `Store.create`/
  `Store.update` in `seed-items` laufen gegen `tmp_path`-artiges DATA_ROOT
  `/tmp/opencode/sharefyx-wegwerf-200knoten/data`, nicht gegen den echten; Tabu-Diff
  prüft das gegen den echten `main`-Branch, der unverändert bleibt).
- `node --check` / `ui_budget.py` / `bash -n`: nicht relevant — kein JS/CSS/Shell-Touch
  in dieser Session.
- **Tabu-Diff §0.3 leer** — `git diff --stat main -- phase4_auth/ phase1_storage/
  storage/ phase5_ui/webui/security.py phase5_ui/webui/api.py phase5_ui/webui/
  serializers.py phase5_ui/webui/permissions.py phase2_mcp/` ist 0 Zeilen. Die
  einzigen Änderungen liegen unter `docs/concepts/p8x_ui_polish_notes.md`,
  `phase8_5_picker_release/CLAUDE.md` (Head-Frontmatter + Session-Block-Rotation) und
  `phase8_5_picker_release/SESSIONS_ARCHIVE.md` (Cluster-3-Block vorne + Frontmatter)
  — alles außerhalb des Tabu-Bereichs.
- **Service-Touch 0** — `systemctl show sharefyx-mcp.service` MainPID=**355956**
  ExecMainStartTimestamp=`Sat 2026-09-05 16:10:18 CEST` (Hard Rule 9 + §0.5.7, nur
  gelesen). **Die 200-Knoten-Wegwerf** (`serve.pid` 436596) ist ein **eigener
  Prozess**, eigenes tmp-DATA_ROOT, eigener File-Keyring, eigene `auth.sqlite3` —
  Production-Trennung gemäß Phase-8-§0.5.7-Spirit, Hard Rule 9 explizit (PID-Datei,
  niemals `pkill -f`).
- **Größenprüfung am Ende (Ist-Werte):**
  - `phase8_ui_graph/CLAUDE.md` **94.3 KB** (unverändert).
  - `phase8_5_picker_release/CLAUDE.md` **50.4 KB** (war 50.5 KB nach Cluster-3 —
    minimaler Zuwachs durch Frontmatter-Eintrag + neuen Session-Block, bleibt deutlich
    über dem 40-KB-Softcap, exempt, Auflösung bleibt Z-Arbeit).
  - `phase8_5_picker_release/SESSIONS_ARCHIVE.md` **~128 KB** (war 109 KB; +~19 KB
    durch den rotierten Cluster-3-Block — der größte rotierte Block dieser Sitzung
    bisher; L3, exempt).
  - `docs/concepts/p8x_ui_polish_notes.md` **37.5 KB** (war 25.5 KB; **+12 KB** durch
    §8 + §9 + §6-Affirmation + §C + §E-Updates — knapp unter dem 40-KB-Softcap,
    keine Auflösung nötig; bei der nächsten Erweiterung Trimm-Pass vorsehen).
  - `docs/INDEX.md` **61.5 KB** (unverändert — Phase-8.5-Head-Updates sind intern,
    keine INDEX-Zeile-Änderung nötig; Frontmatter-`updated:` wird unten ergänzt).
  - `CLAUDE.md` (Wurzel) **71 KB** (unverändert — Current-state-Eintrag unten
    angehängt; weiter über dem Softcap, gleiche Linie wie D3/D4 dokumentiert).

**Doku-Updates im selben Sub-Session-Commit (Hard Rule 8):**

- `phase8_5_picker_release/CLAUDE.md` — Cluster-3-Block per Hand nach
  `SESSIONS_ARCHIVE.md` rotiert (Skript passt nicht auf Phase-8.5-Muster, bewährtes
  Vorgehen aus den letzten sechs Sub-Sessions), dieser 2026-09-08-Doku-Block neu im
  Head. Frontmatter-`updated:` vorne ergänzt (Pipe-and-Getrennt-Format, kein Kürzen
  trotz 40-KB-Softcap-Überschreitung — Muster aus D3/D4).
- `phase8_5_picker_release/SESSIONS_ARCHIVE.md` — Cluster-3-Block vorne angehängt
  (newest-first, verbatim aus dem Head kopiert, 176 Zeilen unverändert), Frontmatter-
  `updated:` vorne ergänzt.
- `docs/concepts/p8x_ui_polish_notes.md` — drei User-Feedback-Punkte in §6/§8/§9,
  §C (offene Fragen) und §E (chronologische Tabelle) ergänzt. Frontmatter-`updated:`
  vorne ergänzt. **Größe 25.5 → 37.5 KB**, +12 KB netto.
- `docs/INDEX.md` — Phase-8.5-Header + Phase-8.X-Header um diese Sub-Session ergänzen
  (im selben Commit, Pattern der letzten Sub-Sessions); Frontmatter-`updated:` vorne
  ergänzt.
- `CLAUDE.md` (Wurzel) — Current-state-Eintrag für diese Sub-Session (Verweis auf
  `p8x_ui_polish_notes.md` §6/§8/§9 + 200-Knoten-Wegwerf als laufendes Nikinger-
  Artefakt); Frontmatter-`updated:` vorne ergänzt.

**Was diese Sub-Session bewusst NICHT tat:**

- **Keine Code-Änderung** — nur Doku + ein Wegwerf-Setup. §8 + §9 in
  `p8x_ui_polish_notes.md` sind reine Notizen-Sammlung, keine Implementierung; der
  Server-Tabu wird nicht angetastet, `localStorage["sfx:tags:palette"]` ist ein
  Vorschlag für die Planungs-Session.
- **Keine P8-21 d / P8-22 / P8-24 Sichtprüfung** durch opencode/M3 — das ist
  Nikinger-Aktion am echten Browser gegen die laufende 200-Knoten-Wegwerf. Die
  Wegwerf ist startbereit (Health-Gate `8/8 grün` implizit — `/health` 200 + `/ui/login`
  200, weil der Server-Smoke gegen den v3.0.1-Deploy lief und dieser Server auf
  v3.0.1-Code basiert; eine volle `scripts/health_gate.sh`-Lauf-Bestätigung kann
  optional am Ende der Sichtprüfung erfolgen, ist für die Sichtprüfung selbst
  aber nicht nötig). Der Cluster-3-Testblock
  (`phase8_5_picker_release/CLUSTER3_TESTBLOCK.md`, 17 KB, 243 Zeilen, bereits am
  2026-09-07 angelegt) trägt die Schritt-für-Schritt-Anleitung.
- **Keine Phase-8.5-Bilanz-Sprünge** — die 5 ✅ · 14 🟡 · 1 ⬜ bleibt; Phase-8.5
  wartet weiter auf Cluster 4 (Connector) + Cluster 5 (Fabian) + Z. Die §8/§9-
  Notizen sind p8.X-Scope, kein Phase-8.5-Scope.
- **Kein Live-Deploy, kein Service-Touch** — die 200-Knoten-Wegwerf ist ein *eigener
  Prozess* (Hard Rule 9-konform via PID-Datei), Production-Dienst unverändert seit
  2026-09-05 16:10:18 CEST.

**Nikinger-Aktion in dieser Sub-Session (offen, nach dem Lesen dieses Blocks):**

- **Cluster-3-Rest-Sichtprüfung** mit der laufenden 200-Knoten-Wegwerf auf
  `http://127.0.0.1:18772/ui/login` — Login-Daten siehe oben. Reihenfolge nach
  `phase8_5_picker_release/CLUSTER3_TESTBLOCK.md`:
  - **P8-21 d** (>15-Knoten-Tag-Riegel empirisch) — Tag-Toggle klicken, schauen
    ob `spitze` 5/5 Knoten als zusätzliche Kanten erscheint (sollte) und `last-200`
    200/200 als zusätzliche ausgeschlossen wird (`graph.js:210
    if (ids.length > TAG_CLIQUE_LIMIT) return;`).
  - **P8-22 a/b/c** (Settle-Zeit + Interaktion + Reduced-Motion) — Stoppuhr
    Übersicht-Klick → erste Beruhigung; Hover/Drag/Wheel ohne Hakeln; in
    DevTools-Console `emulate prefers-reduced-motion reduce` (oder Chrome-Flag
    `--force-prefers-reduced-motion`) und prüfen, dass die Map statisch rendert.
  - **P8-24** kombinierter E2E-Ritt — am **D2-Wegwerf (Port 18768, 14 Knoten)**,
    NICHT am 200-Knoten-Wegwerf (Station 3 driftet sonst wie in der Vorverifikation
    beobachtet).
- **§6-Konto/Einstellungen-Vertausch-Entscheidung** (a/b/c) — nicht heute nötig,
  die Frage wird in der Planungs-Session geklärt; heute nur: „ja, der Punkt steht
  noch" (Re-Affirmation erfolgt).
- **§8.2 „blocked"-Semantik** — kosmetisch oder mit Bucket-Auswirkung? Nicht heute
  nötig, Planungs-Session-Frage.
- **§9 Feedback-Senke** — User-Space / `/var/log/sharefyx/feedback/` / externer
  Endpunkt? Nicht heute nötig, Planungs-Session-Frage.
- **Wegwerf-Cleanup nach Sichtprüfung** —
  `.venv/bin/python phase8_ui_graph/scripts/wegwerf_setup_200knoten.py cleanup`
  (Hard Rule 9-konform, stoppt via `serve.pid` und räumt `/tmp/opencode/
  sharefyx-wegwerf-200knoten/` komplett auf — wenn beide Sichtprüfungen
  durchlaufen sind). Optional: D2-Wegwerf analog.

**Nächster Schritt, konkret:**

- **Cluster 3 — Rest (Nikinger-Aktion):** wie oben, gegen die laufende 200-Knoten-
  Wegwerf + D2-Wegwerf (parallel auf 18772 + 18768, kein Port-Konflikt).
- **Cluster 4 (Nikinger-Aktion, ~10 Min):** P8.5-3 + P8.5-4 + P8.5-17 V105 +
  P8.5-19 Bauform-Bestätigung Radiogruppe am echten v3.0.1.
- **Cluster 5 (Nikinger-Aktion, wenn Fabian verfügbar):** P8-5 + P8-8.
- **Z** (Phase-8.5-Closeout): nach allen Clustern; hebt P8.5-19 auf ✅ und schreibt
  den Phase-8-✅-Nachtrag + die p8.X-Ankündigung mit Verweis auf
  `docs/concepts/p8x_ui_polish_notes.md` als Wahrheits-Quelle.

**Größe-Hinweis (unverändert von vorher):** Phase-8-Head **94.3 KB**, Phase-8.5-
Head **50.4 KB**, `SESSIONS_ARCHIVE.md` **~128 KB**, `p8x_ui_polish_notes.md`
**37.5 KB** (knapp unter Cap), `docs/INDEX.md` **61.5 KB**, `CLAUDE.md` (Wurzel)
**71 KB** — alle deutlich über dem 40-KB-Softcap außer dem Polish-Notes-Doc, das
**knapp unter** dem Cap bleibt. Auflösung bleibt Z-Arbeit (alle Überschreitungen
sind in der Wurzel-Phase oder in Phase 8/8.5, wo der Z-Closeout eh ansteht) —
bewusst nicht stiller Trimm, dokumentiert wie D3/D4.
### 2026-09-08 (Folge-Sub-Session: D2-Wegwerf zusätzlich hochgefahren + konsolidierter Restblock-Testblock für alle offenen Sichtprüfungen geschrieben)

**Auftrag (zweiter Schwung nachmittags):** „Bitte zusätzlich noch die restlichen
Sichtprüfungen, damit ich sie durchführen kann" — der Nikinger braucht eine
**Sichtprüfungs-Anleitung**, die er in einer zusammenhängenden Sitzung (mit Fabian für
P8-8) gegen die laufende v3.0.1-Production UND gegen die Wegwerf-Instanzen
abarbeiten kann.

**Was seit dem ersten 2026-09-08-Sub-Session-Block dazu kam:**

- **D2-Wegwerf zusätzlich hochgefahren** (Port 18768, PID **438765**) — der 200-Knoten-
  Wegwerf alleine reicht für P8-21 d + P8-22, aber **nicht** für P8-24 (der 200-Knoten-
  Drift in Station-3-Idempotenz-Check bei `DEFAULT_LIMIT=50` ist bekannt). Der D2-Datensatz
  (10 alpha + 4 beta, 14 Knoten, 6 Kanten, gemischte Tags/Ordner, Frontmatter+Body-Links)
  ist genau der richtige Datensatz für P8-24. Setup: `… setup` (1.4 s) → `…
  seed-items` (5 Items/Sek) → `… start` (2.0 s bis `/health` 200). Beide Wegwerf-Instanzen
  laufen jetzt parallel:
  - Tab 2: `http://127.0.0.1:18772` (200-Knoten, PID 436596, uptime ~70 min)
  - Tab 3: `http://127.0.0.1:18768` (D2, PID 438765, frisch gestartet)
  - Tab 1 ist Production v3.0.1 (Tailscale-URL, PID 355956 unverändert seit
    2026-09-05 16:10:18 CEST).

- **`phase8_5_picker_release/SICHTPRUEFUNG_RESTBLOCK.md` neu** — 27.5 KB, 471 Zeilen,
  der **konsolidierte Schritt-für-Schritt-Testblock** für alle restlichen Sichtprüfungen.
  Inhalt:
  - **Cluster 3-Rest (Phase 8):** P8-21 d (Tag-Cutoff > 15 empirisch gegen 200-Knoten),
    P8-22 a/b/c (Settle + Interaktion + Reduced-Motion gegen 200-Knoten), P8-24
    (kombinierter E2E-Ritt gegen D2). Detaillierte Sub-Schritte für jeden Punkt,
    analog zum `CLUSTER3_TESTBLOCK.md`-Stil, aber kompakter (Verweisdoku statt
    Duplikation der ausführlichen Sub-Punkte).
  - **Cluster 4 (Phase 8.5):** P8-16 (Glass-Fallback 30 Sek als Vorstation), P8.5-19
    (Bauform-Bestätigung Radiogruppe 30 Sek), P8.5-3 + P8.5-4 (Hint + Vierte A3-Probe,
    ca. 3 Min — fällt mit C5-1 P8-5 zusammen), P8.5-17 (V105 Connector-OK).
  - **Cluster 5 (Phase 8):** P8-5 (Drittprobe gegen v3.0.1, fällt mit C4-2 zusammen),
    P8-8 (Zweitnutzer-Pass-Through mit zwei realen Tokens — braucht Fabian, nicht
    heute alleine abnehmbar).
  - **Login-Daten-Snippet** als re-runnables Python-Programm mit aktuellem TOTP-Code
    (rollt alle 30 s, vor jeder Sichtprüfung neu ausführen — Passwort wird vom
    Setup-Skript per `secrets.token_urlsafe(8)` jedes Mal neu gewürfelt und ist
    daher nicht cache-bar).
  - **Ergebnis-Tabelle je Cluster** mit Bestanden-Spalte zum Ausfüllen, Größen- und
    Commit-Hinweise, Cleanup-Befehle (`wegwerf_setup_200knoten.py cleanup`,
    `wegwerf_setup_d2.py cleanup`, Hard Rule 9, PID-Datei-basiert, **niemals**
    `pkill -f` mit Regex).
  - **Reihenfolge-Empfehlung** für eine zusammenhängende Sichtprüfungs-Sitzung
    (11 Schritte, ~15 Min ohne Fabian / ~30 Min mit Fabian-Slot).

- **`docs/INDEX.md`** um die neue Datei-Zeile ergänzt (eine Zeile direkt unter
  `SESSIONS_ARCHIVE.md`-Bullet, mit L1-Header-Beschreibung und Verweis auf
  `CLUSTER3_TESTBLOCK.md` als ausführliche Sub-Punkte-Quelle) — **im selben Schritt**,
  Hard Rule 8.

- **Wurzel-CLAUDE.md** um den neuen Current-state-Eintrag ergänzt (siehe unten).

**Verifiziert (§0.5 Checkliste — Phase 8.5-Konvention):**

- `pytest -q`: **964/964 grün unverändert** (kein Python-Touch in dieser Sub-Session,
  der Setup-Befehl läuft gegen `tmp_path`-artiges tmp-`DATA_ROOT`, Tabu-Diff prüft
  gegen `main` und bleibt 0).
- `node --check` / `ui_budget.py` / `bash -n`: nicht relevant — kein JS/CSS/Shell-Touch.
- **Tabu-Diff §0.3 leer** — `git diff --stat main -- phase4_auth/ storage/
  phase5_ui/webui/security.py phase5_ui/webui/api.py phase5_ui/webui/serializers.py
  phase5_ui/webui/permissions.py phase2_mcp/` ist 0 Zeilen. Einziger Code-Touch-Pfad:
  `phase8_ui_graph/scripts/wegwerf_setup_*.py`, nicht tabu (Phase-8.5-Tabu-Liste §0.3
  zielt explizit auf `storage/`/`mcpserver/`/`authserver/`/`webui/{security,api,…}`).
- **Service-Touch 0** — `systemctl show sharefyx-mcp.service` MainPID=**355956**
  ExecMainStartTimestamp=`Sat 2026-09-05 16:10:18 CEST` (Hard Rule 9 + §0.5.7, nur
  gelesen). **Die beiden Wegwerf-Instanzen sind eigene Prozesse** (PID 436596 /
  PID 438765, eigene tmp-DATA_ROOTs, eigene File-Keyringe, eigene `auth.sqlite3`),
  Hard-Rule-9-konform via PID-Datei gestoppt.
- **Größenprüfung am Ende (Ist-Werte):**
  - `phase8_5_picker_release/SICHTPRUEFUNG_RESTBLOCK.md` **27.5 KB** neu (war nicht
    existent, +27.5 KB netto).
  - `phase8_5_picker_release/CLAUDE.md` jetzt **80.7 KB** (+0 KB Head — der neue Block
    wird hier gerade geschrieben, also dieser Block selbst).
  - `phase8_5_picker_release/SESSIONS_ARCHIVE.md` ~128 KB unverändert.
  - `docs/concepts/p8x_ui_polish_notes.md` 37.5 KB unverändert.
  - `docs/INDEX.md` **64.0 KB** (+0.7 KB für die neue Datei-Zeile).
  - `CLAUDE.md` (Wurzel) siehe unten (+~2 KB Current-state-Eintrag).

**Doku-Updates im selben Sub-Session-Zyklus (Hard Rule 8):**

- `phase8_5_picker_release/SICHTPRUEFUNG_RESTBLOCK.md` — **neu**, ~28 KB, vier Cluster
  (C3-Rest, C4-0, C4-1, C4-2, C4-3, C5-1, C5-2), Setup-Stand, Login-Snippet,
  Reihenfolge-Empfehlung, Cleanup. Wird mit diesem Sub-Session-Commit committed.
- `phase8_5_picker_release/CLAUDE.md` — dieser Folge-Sub-Session-Block neu im Head
  (gleichberechtigt zum ersten 2026-09-08-Block von oben — beide unter `## Session
  stopped`-Header; Phase-8.5-Muster erlaubt mehrere `### date`-Subblöcke).
  Frontmatter-`updated:` wird unten ergänzt.
- `phase8_5_picker_release/SESSIONS_ARCHIVE.md` — keine Änderung (kein Block rotiert,
  beide 2026-09-08-Sub-Sessions bleiben aktiv im Head bis zur nächsten Sub-Session).
- `docs/INDEX.md` — neue Zeile unter SESSIONS_ARCHIVE-Bullet mit L1-Beschreibung
  + Datum 2026-09-08.
- `CLAUDE.md` (Wurzel) — Current-state-Eintrag (siehe unten).

**Was diese Sub-Session bewusst NICHT tat:**

- **Keine Sichtprüfung** durch opencode/M3 — alle Sichtprüfungen sind weiterhin
  Nikinger-Aktion am echten Browser gegen v3.0.1 + die zwei Wegwerf-Instanzen. Setup
  + Dokumentation, keine Ausführung.
- **Keine Phase-8-Bilanz-Sprünge** — die Bilanz bleibt **20 ✅ · 6 🟡 · 0 ⬜** wie
  im ersten 2026-09-08-Block dieses Tages notiert. Erst nach den Sichtprüfungen
  kann der Sprung auf **23 ✅ · 3 🟡** (Cluster 3 abgeschlossen) bzw. auf
  **25 ✅ · 1 🟡** (Cluster 4 + 5 auch durch) erfolgen — die Sichtprüfungs-Ergebnisse
  gehen in den nächsten Commit (vom Nikinger oder einem folgenden opencode/M3-Lauf).
- **Kein Code-Touch** — Testblock-Datei + INDEX-Zeile + Doku-Updates sind allesamt
  reiner Markdown-Inhalt, kein `.py`/`.js`/`.css`/`.sh` berührt.
- **Kein Live-Deploy, kein Service-Touch** — Production läuft seit 2026-09-05
  16:10:18 CEST unverändert (PID 355956), die zwei Wegwerf-Instanzen sind eigene
  Prozesse mit ihren eigenen tmp-`DATA_ROOT`s und File-Keyringen, sauber per
  PID-Datei gestoppbar.

**Nikinger-Aktion in dieser Sub-Session (offen, am echten Gerät gegen die zwei
Wegwerf-Instanzen + Production v3.0.1):**

- **Cluster 3-Rest:** Sichtprüfungs-Anleitung in `SICHTPRUEFUNG_RESTBLOCK.md`
  Schritt für Schritt durchgehen, Ergebnis-Tabellen ausfüllen, Screenshots unter
  `docs/screenshots/c3rest_*.png` ablegen. Reihenfolge-Empfehlung im Restblock.
- **Cluster 4:** P8-16 (30 Sek) + P8.5-19 (30 Sek) + P8.5-3 + P8.5-4 (~3 Min,
  entscheidet §9.4.1 Abbruchregel) + P8.5-17 V105 (~1 Min).
- **Cluster 5:** P8-5 fällt mit C4-2 zusammen, P8-8 braucht Fabian und ist nicht
  alleine heute abnehmbar — diese Zeile bleibt 🟡 bis zur Fabian-Sitzung.
- **Cleanup** am Ende: `.venv/bin/python phase8_ui_graph/scripts/wegwerf_setup_d2.py
  cleanup` + `…_200knoten.py cleanup` (Hard Rule 9, PID-Datei-basiert, **niemals**
  `pkill -f` mit Regex).
- **Status-Update nach dem Lauf:** `phase8_ui_graph/CLAUDE.md` §7-Matrix für die
  abgehakten Zeilen P8-21 d / P8-22 / P8-24 / P8-16 / P8.5-3 / P8.5-4 / P8.5-17 /
  P8.5-19 + `phase8_5_picker_release/CLAUDE.md` Modul-Status + Abnahmestand. Phase-8-
  + Phase-8.5-Bilanz-Zeile nachziehen (awk-Kommando im §7-Bilanz-Abschnitt der Phase-8-
  Head-Datei dokumentiert). Hard Rule 8 im selben Commit.

**Nächster Schritt, konkret:**

- **Nikinger-Live-Sichtprüfung** wie oben (Cluster 3-Rest + Cluster 4 in einer Sitzung;
  Cluster 5 mit Fabian in einer zweiten). Reihenfolge-Empfehlung im Restblock §Reihenfolge-
  Empfehlung.
- **Phase-8.5-Z-Closeout** nach allen Clustern: füllt Plan §9 (P8.5-T), schreibt den
  Phase-8-✅-Nachtrag in `phase8_ui_graph_plan.md` §9 + §9.4.7, hebt Phase-8-Head §7-
  Matrix + Session-Block nach, drei Skripte/Doku-Updates, Größenprüfung. Schließt
  Phase 8 + 8.5 formal mit ab.
- **p8.X-Ankündigung** im Z-Closeout mit Verweis auf `docs/concepts/p8x_ui_polish_notes.md`
  als Wahrheits-Quelle.

**Größe-Hinweis (unverändert vom vorigen Sub-Session):** Phase-8-Head **94.3 KB**,
Phase-8.5-Head **~55 KB** (nach diesem Block), `SESSIONS_ARCHIVE.md` ~128 KB,
`polish_notes.md` **37.5 KB** (knapp unter Cap), `docs/INDEX.md` **~64 KB**, `CLAUDE.md`
(Wurzel) ~76 KB — alle deutlich über dem 40-KB-Softcap außer dem Polish-Notes-Doc.
Auflösung bleibt Z-Arbeit, bewusst nicht stiller Trimm.


### 2026-09-08 (Folge-Sub-Session 2: freundlicher Walkthrough für die Sichtprüfung geschrieben, auf Bitte des Nikinger nach mehr Detailtiefe)

**Auftrag:** „bitte etwas genauer erläutern, was ich genau testen soll :). am besten
step Erklärung + evtl. commands die ich brauche" — der Nikinger hat die
technische Checkliste (`SICHTPRUEFUNG_RESTBLOCK.md`, 27.5 KB, 471 Zeilen) als
zu dicht empfunden und wollte einen **freundlichen Walkthrough**, der ihn
Schritt für Schritt am Bildschirm begleitet: Was er klickt, was er sieht, welche
DevTools-Befehle er optional laufen lässt.

**Ergebnis — neue Datei `phase8_5_picker_release/SICHTPRUEFUNG_WALKTHROUGH.md`:**

29.4 KB / 727 Zeilen, mit folgender Struktur:

- **Vorbereitung** — drei Tabs (Production + 200-Knoten + D2) plus
  Connector-Session aufsetzen, mit der genauen Reihenfolge der Tabs und der
  Login-Reihenfolge.
- **C4-0 P8-16 Glass-Fallback** — DevTools-Rendering-Tab-Weg mit
  Schritt-für-Schritt-Anleitung + Visual-Checkliste (was wird solid, welche
  Outline erkennbar).
- **C4-1 P8.5-19 Radiogruppe** — Item-Editor öffnen, Lupensymbol finden,
  Dialog öffnen, **zwei Radio-Buttons erwarten statt eines Dropdowns**,
  Modus-Wechsel + Persistenz prüfen + Console-Cross-Check
  `localStorage.getItem("sfx:linkpicker:mode")`.
- **C4-2 P8.5-3 + P8.5-4 Hint + Vierte A3-Probe** — vier (oder fünf)
  Prompt-Varianten mit Tipp, jede Form in eine separate Anfrage zu packen,
  damit der Connector nicht „zu schlau" alle vier vereint. Entscheidet §9.4.1
  Abbruchregel (vierte Form hält → ✅, fünfte Form rutscht durch →
  Modellverhalten dokumentiert, kein Code-Fix).
- **C4-3 P8.5-17 V105 Connector-Check** — Connector-Übersicht + zwei
  Probe-Calls (`list_spaces`, `search_items`), mit genauer
  Pass/Fail-Beschreibung.
- **C3-1 P8-21d Tag-Cutoff** — Tags-Toggle auf dem 200-Knoten-Graph,
  Console-Cross-Check mit `fetch('/api/v1/graph').then(r=>r.json()).then(g =>
  g.edges.filter(e => e.kind === 'tag').length)` für die Tag-Kanten-Anzahl.
- **C3-2 P8-22 Settle + Interaktion + Reduced-Motion** — drei Sub-Schritte:
  (a) **Stoppuhr-Anleitung** für die Settle-Zeit (Handy oder Extension,
  < 3 s Budget, ~2.5–2.7 s erwartet), (b) Hover/Drag/Zoom/Pan subjektiv
  prüfen, (c) Rendering-Tab `prefers-reduced-motion: reduce` + statische
  Wiedergabe prüfen.
- **C3-3 P8-24 E2E-Ritt gegen D2-Wegwerf** — sechs Stationen einzeln
  durchgekaut mit "Was du tust" / "Was du siehst" pro Station und einer
  separaten Pass/Fail-Beschreibung pro Station.
- **C5-1 P8-5** — Hinweis "fällt mit C4-2 zusammen, kein Extra-Aufwand".
- **C5-2 P8-8** — ausführliche Fabian-Koordinations-Anleitung, mit fünf
  Probe-Schritten (Suche-privat, Suche-shared, get_item-shared, get_item
  privat sollte 403/404, update_item-shared sollte 403).
- **Ergebnis-Tabelle** zum Ausfüllen mit Bestanden-Spalte pro Punkt, plus
  Notizen-Feld für Restdefekte.
- **Nach-Lauf-Aufgaben** — Screenshots-Ablage + Status-Updates der zwei
  Phase-Heads + INDEX + Commit + Cleanup-Befehle.
- **Login-Snippet** noch einmal am Dateiende (200-Knoten + D2-Variante), plus
  die zwei TOTP-Secrets für einmaligen Scan in eine Authenticator-App.

**Was diese Sub-Session bewusst NICHT tat:**

- **Keine Code-Änderung** — reine Doku-Erweiterung, kein `.py`/`.js`/
  `.css`/`.sh` berührt.
- **Keine Sichtprüfung** — die ist weiterhin Nikinger-Aktion am echten
  Gerät; der Walkthrough ist die Anleitung, nicht die Ausführung.
- **Keine Änderung an der technischen Checkliste** —
  `SICHTPRUEFUNG_RESTBLOCK.md` bleibt als Referenz (technisch dicht, mit
  Tabellen, Code-Ankern, Edge-Cases) und der Walkthrough ist die
  Bildschirm-Begleitung.

**Verifiziert (§0.5 Checkliste):**

- `pytest -q`: **964/964 grün unverändert** (kein Python-Touch).
- **Tabu-Diff §0.3 leer** — nur Doku-Touches.
- **Service-Touch 0** — Production PID 355956 unverändert.
- **Größen-Stand:**
  - `phase8_5_picker_release/SICHTPRUEFUNG_WALKTHROUGH.md` **29.4 KB** neu
    (separate Datei, kein Cap-Druck).
  - `phase8_5_picker_release/CLAUDE.md` jetzt **~80 KB** nach diesem dritten
    Sub-Session-Block (Phase-8.5-Muster mit drei `### date`-Subblöcken unter
    `## Session stopped`-Header).
  - `docs/INDEX.md` ~64.8 KB (+0.8 KB für die neue Walkthrough-Zeile).

**Doku-Updates im selben Sub-Session-Zyklus (Hard Rule 8):**

- `phase8_5_picker_release/SICHTPRUEFUNG_WALKTHROUGH.md` — **neu**, 29 KB,
  freundlicher Walkthrough als Geschwister zur technischen Checkliste.
- `phase8_5_picker_release/CLAUDE.md` — dieser dritte 2026-09-08-Sub-Session-
  Block neu im Head. Frontmatter `updated:` wird im selben Schritt ergänzt.
- `docs/INDEX.md` — neue Walkthrough-Zeile direkt unter der
  Restblock-Zeile.
- `CLAUDE.md` (Wurzel) — Current-state-Eintrag (siehe unten).

**Nächster Schritt, konkret:**

- **Nikinger-Live-Sichtprüfung** mit dem Walkthrough am Bildschirm (offene
  Sichtprüfung seit heute Nachmittag): drei Tabs vorbereiten, mit C4-0
  anfangen (30 Sek), durch C4-2 (~3 Min für die wichtigste Aussage über
  die Abbruchregel §9.4.1), C3-Rest in Tab 2 und Tab 3 abarbeiten, Fabian
  für C5-2 koordinieren.
- **Phase-8.5-Z-Closeout** nach allen Clustern.
- **Cleanup** der Wegwerf-Instanzen nach der Sichtprüfung
  (Hard Rule 9, PID-Datei-basiert, **niemals** `pkill -f`).

**Größe-Hinweis:** Phase-8.5-Head jetzt ~80 KB, alle Überschreitungen
des 40-KB-Softcaps dokumentiert wie D3/D4 — Auflösung bleibt Z-Arbeit,
bewusst nicht stiller Trimm.

### 2026-09-08 (Folge-Sub-Session 4 — Z-Closeout: Sichtprüfungs-Automatisierung, Statusregel geändert, Phase 8 + 8.5 formal ✅, P8.6/P9 vorgemerkt)

**Auftrag:** die im Walkthrough offenen Sichtprüfungspunkte durchführen — zunächst
throwaway-automatisiert (C4-0/C4-1/C3-1/C3-2/C3-3), dann nach Reconnect des echten
sharefyx-MCP-Connectors auch C4-2/C4-3/C5-1 gegen die echte Produktion und C5-2 gegen ein
neu gebautes Zwei-Principal-Wegwerf-Setup. Danach: Statusregel-Entscheidung, Radiogruppe-
Rückbau-Feedback, Housekeeping, Versionierungsplan — alle vier vom Nikinger entschieden.

**Neue Skripte** (`phase8_ui_graph/scripts/`): `p8_21d_tag_cutoff_probe.py` (Canvas-Prototype-
Patch zählt gezeichnete Tag-Kanten exakt, Frame-Teiler-Trick über die expliziten Kanten als
Divisor — **10.0 Tag-Kanten/Frame exakt**, `spitze` C(5,2)=10 durchgelassen, `last-200` +
12× `gruppe-NN` korrekt ausgeschlossen); `p8519_radiogroup_probe.py` (Radiogruppe gegen die
200-Knoten-Wegwerf: 2 Radios, kein `<select>` mehr, `localStorage`-Persistenz über
Schließen+Wiederöffnen — 5/5); `wegwerf_setup_p8_8.py` (erstes Wegwerf-Setup mit ZWEI
unabhängigen Principals, `testuser1`+`testuser2`, statt einem wie bei jedem Vorgänger) +
`p8_8_zweitnutzer_probe.py` (echter OAuth-Dance ohne Browser — Discovery/DCR/PKCE/Authorize/
Token — für beide Principals, dann fünf echte MCP-Tool-Aufrufe über die Leitung: privates
Item nicht in fremder Suche, geteiltes Item schon, `get_item` auf privates Item abgelehnt,
`update_item` auf geteiltes [nur `share_read`] Item mit `write_denied` abgelehnt — 5/5).
Echter Fund dabei: `update_item` lehnt `share_read`/`share_write` kategorisch ab („das geht
nur ein Mensch in der UI", `tools.py`), Sharing im Wegwerf-Setup deshalb per direktem
`storage.store.Store.update()` statt über MCP gesetzt — kein Bug, dokumentierte Restriktion.

**Nach Reconnect des sharefyx-MCP-Connectors** (Nikinger-Aktion, `/mcp` in claude.ai):
`list_spaces` gegen die echte Produktion (vier reale Spaces), zwei `search_items`-Aufrufe
gegen `niklas`/`IT-Sekus-Projekt`, alle vier geforderten Textformen (Fließtext/Tabelle/
Klammer/Aufzählung) live erzeugt und auf `itm_…`-Lecks geprüft — keins gefunden. Zusätzlich
lieferte der Nikinger unabhängig einen Screenshot eines echten claude.ai-Chats über denselben
Connector, der dieselbe Frage beantwortete, ebenfalls ohne ID-Leck — zwei unabhängige
Live-Belege für dieselbe Zeile.

**Vier Nikinger-Entscheidungen, alle umgesetzt:**
1. **Statusregel geändert** (Option A): eine vom Nikinger geprüfte Wegwerf-Automatisierung
   zählt ab sofort als `✅ = live-verifiziert`, nicht mehr nur eine eigenhändige Live-Probe.
   Begründung wörtlich: „the throwaway is, except for files and user, byte by byte identical
   to the new prod after deploy." Volle Herleitung + wiederverwendbare Techniken: neue Datei
   `docs/concepts/sichtpruefung_automation_conventions.md`.
2. **Radiogruppe-Rückbau auf `<select>`** (inline-Beschreibung, Design-Konsistenz) — nur
   vormerkt, siehe Vormerkung oben, kein Code angefasst.
3. **Housekeeping:** alle drei Wegwerf-Instanzen (200-Knoten, D2, das neue Zwei-Principal-
   Setup) per PID-Datei abgebaut, kein `pkill -f`.
4. **Versionierungsplan:** P8.6 (Arbeitsname) → `v3.0.2`, P9 (Arbeitsname) → `v3.1.0` —
   Größenklassen-Regel jetzt explizit (Patch für Politur-Größe wie 8.5 selbst, Minor für
   Umfang wie der ursprüngliche v3.0-Umbau). OpenCode-Vision-Plugin
   (`DavidEasden/opencode-vision`) als ausdrücklich früher Punkt in P8.6.

**Matrix-Updates (Hard Rule 8, im selben Zyklus):** `phase8_ui_graph/CLAUDE.md` §Abnahmestand
26/26 ✅ (P8-5/-8/-16/-21/-22/-24 gehoben, Statusregel-Text ersetzt, Bilanz-Abschnitt neu
geschrieben); dieser Head — Abnahmestand P8.5-3/-4/-5/-17/-19 gehoben (10 ✅ · 10 🟡, Rest ist
ungesichtete Block-C-Evidenz von 2026-09-04, kein neuer Code nötig); `ROADMAP.md`
Phasentabelle (P8/P8.5 ✅, alte P8.X-Platzhalterzeile in P8.6+P9 aufgeteilt); `docs/INDEX.md`
(Phase-8/8.5-Header, neue P8.6+P9-Sektion); Wurzel-`CLAUDE.md` Current-state (ein
konsolidierter Closeout-Absatz). Zwei Memory-Dateien aktualisiert/neu (`project_phase_status`
komplett neu geschrieben — war 5 Tage stale und faktisch falsch zum v3-Deploy-Stand;
`feedback_throwaway_evidence_counts_as_live` neu).

**Bewusst nicht gemacht, benannt statt verschwiegen:** die Doc-Hygiene-Kompression (Rotation
der Session-Prosa nach `SESSIONS_ARCHIVE.md`, Trimmen von `docs/INDEX.md`s `updated:`-Pipe),
seit mehreren Sub-Sessions als „Auflösung bleibt Z-Arbeit" vertagt — auch dieser Z-Closeout
hat sie nicht angefasst. Alle vier Phase-Heads liegen weiterhin deutlich über dem
40-KB-Softcap. In `project_phase_status`-Memory als offener Punkt vermerkt, kein stiller
Verzicht.

**Verifiziert:** kein Python-/JS-Code angefasst (nur neue Skripte unter `phase8_ui_graph/
scripts/`, keine Änderung an `webui/`/`mcpserver/`/`storage/`), Tabu-Diff §0.3 irrelevant.
Production (`PID 355956`) vor und nach der gesamten Sitzung identisch, kein `systemctl`-Verb
ausgeführt. Drei Wegwerf-Ports (18772/18768/18780) nach Ende der Sitzung geschlossen,
gegengeprüft mit `ss -ltnp`.

**Commit:** ein Commit für diesen gesamten Closeout (Skripte + Screenshots + alle Doku-
Updates + Memory) — Nikinger-Aufforderung „correctly end this session". Kein Push ohne
weitere Anweisung.

**Nächster Schritt:** P8.6/P9 sind Arbeitsnamen, keine geplanten Phasen — eine
Planungs-Session (gelockte Entscheidungen, Step 0) steht vor dem ersten Code-Commit in
beiden. Reihenfolge: P8.6 zuerst (inkl. OpenCode-Vision-Plugin früh), P9 danach.
