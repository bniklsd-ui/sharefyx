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
updated: 2026-09-09 (Sichtung der 10 P8.5-🟡-Zeilen — 9 ✅, P8.5-6 bleibt 🟡 wegen fehlendem Vorschau-Screenshot des Bracket-Pfads; vier neue Sichtungs-Konventionen in `docs/concepts/sichtpruefung_automation_conventions.md` §1-§4 notiert [Vorschau-Pflicht / Code-vs-Visuell / Deploy-nach-Test / Screenshots-im-Chat]; `_tooling.md` Plugin-Empfehlung auf P8.6-first-step verschärft; Walkthrough/Restblock Top-Notizen; §Abnahmestand Bilanz 10/10 → 19/1/0, §Nächste Session komplett umgeschrieben auf P8.5-6-Brake-Pfad; alter Z-Closeout-Block manuell nach `SESSIONS_ARCHIVE.md` rotiert + 10 Matrix-Zeilen mit Nikinger-Vermerk; **kein Code-Touch**, pytest unverändert 964/964, Tabu-Diff §0.3 leer, Service-Touch 0 [PID 355956 unverändert], keine Wegwerf-Instanzen gestartet) | 2026-09-08 (Scope-Reversal + Session-Ende: Nikinger-Entscheidung im Review des Z-Final-Commits — die 10 P8.5-🟡-Sichtungen (P8.5-6, -7, -8, -9, -10, -11, -12, -13, -14, -15) wandern NICHT nach P8.6, sondern bleiben in Phase 8.5 als erste Sache der nächsten Session; Phase 8.5 head bekommt eine neue Sektion „Nächste Session“ mit den 10 Zeilen einzeln + Werkzeug-Setup-Stand, Stand-Summary entsprechend umformuliert; Wurzel-updated:-Pipe vorne ergänzt; Frontmatter vorne ergänzt; **kein Code-Touch**, pytest unverändert 964/964, Tabu-Diff 0.3 leer, Service-Touch 0 [PID 355956 unverändert]) | 2026-09-08 (Z-Final: §7-Abnahmematrix P8.5-1 bis P8.5-20 [alle 20 Zeilen mit Beleg] nach SESSIONS_ARCHIVE rotiert; Head von 50 KB auf 42 KB reduziert — 2 KB über Softcap, Rest ist kanonischer Mission/Scope/Harte-Regeln/Modul-Status/Vormerkung/Nächste-Phasen/Session-Block; Frontmatter vorne ergänzt) | 2026-09-08 (Folge-Sub-Session 4, Z-Closeout: Sichtprüfungs-Automatisierung fertig, Statusregel geändert, Phase 8 + 8.5 formal ✅, P8.6/P9 vorgemerkt -- siehe Session-Block am Dateiende) | 2026-09-08 (Doku-Sub-Session 2: **freundlicher Walkthrough** `phase8_5_picker_release/SICHTPRUEFUNG_WALKTHROUGH.md` neu, 29 KB / 727 Zeilen — Was-tust-du / Was-siehst-du pro Schritt, mit DevTools-Befehlen + Console-Snippets + Stoppuhr-Anleitung; Geschwister zum technischen `SICHTPRUEFUNG_RESTBLOCK.md` (dicht, mit Tabellen und Code-Ankern); Walkthrough ist das, was beim Klicken am Bildschirm vor einem liegt, Restblock ist das Nachschlagewerk; deckt C4-0 (P8-16 Glass-Fallback), C4-1 (P8.5-19 Radiogruppe), C4-2 (P8.5-3+4 Hint + Vierte A3-Probe), C4-3 (P8.5-17 V105), C3-1 (P8-21d Tag-Cutoff), C3-2 (P8-22 Settle/Interaktion/Reduced-Motion), C3-3 (P8-24 E2E gegen D2), C5-1 (P8-5 = C4-2), C5-2 (P8-8 mit Fabian); **kein Code-Touch**, nur Doku; pytest unverändert 964/964, Tabu-Diff §0.3 leer, Service-Touch 0) | 2026-09-08 (Doku-Sub-Session: 200-Knoten-Wegwerf gestartet per Standing-Permission für die Cluster-3-Rest-Sichtprüfung [P8-21 d + P8-22 + P8-24]; **drei User-Feedback-Punkte** in `docs/concepts/p8x_ui_polish_notes.md` ergänzt: §6 Konto/Einstellungen re-affirmiert mit drei Vertausch-Lesarten a/b/c gegen `app.html:31-41`, §8 NEU customizable Tags + Standard-Tag „blocked" [§8.1 User-Palette als `localStorage`, §8.2 fester Code-Tag, beide kosmetisch], §9 NEU direkter User-Feedback-Button [drei plausible Senken: User-Space / `/var/log/sharefyx/feedback/` / externer Endpunkt]; **kein Code-Touch**; pytest unverändert 964/964, Tabu-Diff §0.3 leer, Service-Touch 0 [PID 355956 unverändert], Wegwerf-PID **436596** auf Port **18772**); Cluster-3-Block per Hand nach `SESSIONS_ARCHIVE.md` rotiert (Skript passt nicht auf Phase-8.5-Muster), dieser 2026-09-08-Block neu im Head; **Polard-Notes 25.5 → 37.5 KB** knapp unter 40-KB-Softcap) | 2026-09-08 (Doku-Sub-Session Folge: **D2-Wegwerf zusätzlich hochgefahren** auf Port 18768 [PID 438765], beide Wegwerf-Instanzen laufen jetzt parallel — 200-Knoten auf 18772 für Cluster-3-Rest P8-21 d + P8-22, D2-14-Knoten auf 18768 für P8-24; **`phase8_5_picker_release/SICHTPRUEFUNG_RESTBLOCK.md` neu**, 27.5 KB / 471 Zeilen, der konsolidierte Schritt-für-Schritt-Testblock für alle restlichen Sichtprüfungen — Cluster 3-Rest (P8-21 d, P8-22, P8-24) gegen die zwei Wegwerf-Instanzen + Cluster 4 (P8-16 + P8.5-3/4/17/19) gegen Production v3.0.1 + Cluster 5 (P8-5 + P8-8, letzteres mit Fabian); Login-Snippet mit re-runnablem TOTP-Code für beide Instanzen, Screenshots-Konvention, Ergebnis-Tabellen je Cluster, Reihenfolge-Empfehlung, Cleanup-Befehle [Hard Rule 9, PID-Datei, **niemals** `pkill -f`]; **kein Code-Touch**, nur Doku + zweiter Wegwerf-Setup; pytest unverändert 964/964, Tabu-Diff §0.3 leer, Service-Touch 0 [PID 355956 unverändert]) | 2026-09-08 (Doku-Sub-Session: 200-Knoten-Wegwerf gestartet per Standing-Permission für die Cluster-3-Rest-Sichtprüfung [P8-21 d + P8-22 + P8-24]; **drei User-Feedback-Punkte** in `docs/concepts/p8x_ui_polish_notes.md` ergänzt: §6 Konto/Einstellungen re-affirmiert mit drei Vertausch-Lesarten a/b/c gegen `app.html:31-41`, §8 NEU customizable Tags + Standard-Tag „blocked" [§8.1 User-Palette als `localStorage`, §8.2 fester Code-Tag, beide kosmetisch], §9 NEU direkter User-Feedback-Button mit drei plausiblen Senken [User-Space-Item / `/var/log/sharefyx/feedback/` / externer Endpunkt] + Klärungsfragen zur Planungs-Session; **kein Code-Touch**; pytest unverändert 964/964, Tabu-Diff §0.3 leer, Service-Touch 0 [PID 355956 unverändert], Wegwerf-PID **436596** auf Port **18772**); Cluster-3-Block per Hand nach `SESSIONS_ARCHIVE.md` rotiert, dieser 2026-09-08-Block neu im Head; **Polard-Notes 25.5 → 37.5 KB** knapp unter 40-KB-Softcap) | 2026-09-07 (Cluster-3-Teilverifikation — **erste Nikinger-Live-Sichtprüfung nach Cluster 2; P8-20 ✅, P8-21 a/b/c ✅ am echten v3.0.1 in einer Login-Sitzung**; P8-20 (Hover dimmt Nicht-Nachbarn + Klick öffnet Editor bzw. Readonly mit korrekter Drag-vs-Click-Heuristik aus Fix C + Drag/Zoom/Pan ohne Ruckler) und P8-21 (Default nur explizite Kanten + Tag-Toggle + Ordner-Toggle) — Sub-Punkte a/b/c durchlaufen ohne Befund; **P8-21 d + P8-22 + P8-24 in eine Folge-Session verschoben**, weil alle drei die 200-Knoten-Wegwerf brauchen (Nikinger-Aktion per Standing-Permission in `phase8_ui_graph/scripts/wegwerf_setup_200knoten.py`, Port 18772); Phase-8-Bilanz **19 ✅ · 7 🟡 → 20 ✅ · 6 🟡** (P8-20 wandert 🟡 → ✅, `phase8_ui_graph/CLAUDE.md` §7-Matrix + Modul-Status Block D + Bilanz-Zeile + Sichtprüfungs-Status im selben Sub-Session-Commit nachgezogen); `phase8_5_picker_release/CLUSTER3_TESTBLOCK.md` neu (17 KB, 243 Zeilen, vollständiger Schritt-für-Schritt-Testblock als Audit-Quelle für Z); Pre-Z-Tausch-Block per Hand nach `SESSIONS_ARCHIVE.md` rotiert (Skript passt nicht auf Phase-8.5-Muster, Working-Tree-Rekonstruktion weil zwischen den Sub-Sessions kein Commit lag), Cluster-3-Block neu im Head; pytest unverändert 964/964, `node --check`/`ui_budget.py`/`bash -n` irrelevant (kein Code-Touch), Tabu-Diff §0.3 leer, Service-Touch 0 (PID 355956 nur gelesen, kein `sudo systemctl`, keine Wegwerf gestartet); Working Tree jetzt 9 modifizierte Dateien + 1 untracked Testblock-Datei = 10 Dateien; **Nikinger-Aktion in derselben Sub-Session:** Sean-Einladung über `authctl.py invite sean --purpose initial --ttl 86400` (24h gültig, Link wird auf stdout einmalig ausgegeben mit PRODUKTIV/STAGING-Marker zur Datenbank-Zuordnung — Hard Rule 9 + §0.5.7 verbieten opencode/M3 den Eingriff in die echte `auth.sqlite3`); nächster Schritt Cluster 4 (Connector: P8.5-3 + P8.5-4 + P8.5-17 V105 + P8.5-19 Bauform-Bestätigung Radiogruppe am echten v3.0.1) + Cluster 5 (Fabian: P8-5 + P8-8) + Z | 2026-09-07 (Pre-Z-Tausch — **erste opencode/M3-Code-Touch-Session seit Cluster 1**; **P8.5-19** (Bauform-Entscheidung Radiogruppe) und **P8.5-6** (Bracket-Renderer-Fix) committet, beide Zeilen jetzt mit Code + statischem Test; `dialogs.js` (`linkPickerModeEl` raus, neue Modul-Konstante `LINK_PICKER_MODE_NAME`, `_linkPickerMode`/`_restoreLinkPickerMode` auf `querySelector[All]('input[name="link-picker-mode"]')` umgestellt, change-Listener iteriert jetzt die Radios), `app.html` (`<fieldset class="link-picker-modes">` mit `<legend>Einfügen</legend>` + 2× `<input type="radio" name="link-picker-mode">` ersetzt `<select id="link-picker-mode">`), `app.css` neuer Block `.link-picker-modes`/`.link-picker-mode` (`accent-color: var(--accent-line)`), `markdown.js` Link- und Bild-Regex tolerieren jetzt `\[` / `\]` als Escape-Einheit (`(?:\\[\[\]] | [^\]])+` im Title-Capture, danach `\\([\[\]])` → `$1` zum Unescapen); `phase5_ui/tests/test_static_routes.py` zwei neue Tests (`test_link_picker_uses_a_radio_group_not_a_select` P8.5-19, `test_markdown_link_regex_allows_escaped_brackets` P8.5-6 mit Regressionstest gegen die alte `[^\]]+`-Form); `pytest -q` 962 → **964** grün (254 s Gesamtlauf), `node --check` grün auf `dialogs.js` + `markdown.js`, `ui_budget.py` 5/5 im Korridor (dialogs.js 12.6 → 13.2 KB, markdown.js 4.2 KB unverändert, app.css +0.4 KB), Tabu-Diff §0.3 leer (alle Änderungen unter `phase5_ui/webui/static/` + `phase5_ui/tests/`, kein Servercode-Tabu-Auslöser), node-Probe gegen `markdown.js` mit Mock-`document`: 8 Test-Cases rendern wie erwartet — darunter D4-Fund-Beispiel `[Vercel \[Hosting\](#item/itm_67bb0565)` → `<a href="#item/itm_67bb0565">Vercel [Hosting]</a>`; Abnahmestand **5 ✅ · 14 🟡 · 1 ⬜** (P8.5-19 ⬜ → 🟡, P8.5-5/-6-Beschreibungen aktualisiert); Cluster-1-Block nach `SESSIONS_ARCHIVE.md` rotiert (manuell, Skript passt nicht auf Phase-8.5-Muster), Service-Touch 0 (PID 355956 nur gelesen); nächster Schritt unverändert Cluster 3+4+5 (Nikinger-Aktionen) + Z, mit optionaler P8.5-6-Wegwerf-Re-Probe in Cluster 4) | 2026-09-06 (D4-Sichtprobe-Folgesession — **nur dokumentiert, kein Code-Touch in dieser opencode/M3-Session**; sieben neue Themen-Cluster aus der Sichtprobe mit Fabian nach D4 dokumentiert: **Spaces-Layout-Reorg** [„Alle Items"-Leiste unter Spaces + Kippschalter, Map 40 % Breite/volle Höhe, keine Duplikate], **Obsidian-Map** fünf Sub-Punkte [Performance-Reload, Landkarten-Stil, Field schneidet ab, Reload-Drift, Collapsible mit Abhängigkeiten], **Anzahl-Anzeige Ordner**, **Edit-in-Place-Vision** [„Bearbeiten"-Knopf überflüssig], **Layering-Design-System** [3 Layer: echtes Schwarz / aktueller Standard / Liquid Glass + Selektion explizit blau auf Hover, Note-Select, Checkbox], **„Konto"→„Einstellungen"-Rename** + Positions-Tausch mit Logout, **De-AI-ierung-Lauf 2** nach neuen Kriterien; neue Datei `docs/concepts/p8x_ui_polish_notes.md` 25 KB L2 mit allen 16 Themen — fünf bereits in D4 dokumentierte p8.X-Punkte [UX-2-Step-Knotenklick, Map-Field schneidet ab, Map fliegt, Save-Button-YAML-Header, Fabis Sammelliste] + sieben Sichtprobe-Folgesession-Cluster + vier Sub-Punkte aus §2 Obsidian-Map; Vorsegmentierter Anhang §A–§E für die Planungs-Session in Claude Code; **kein Phase-8/8.5-Scope-Touch**, **keine** neuen Tabu-Aufhebungen, **kein** Locking — Sammlung, kein Plan; D4-Block per Hand nach `SESSIONS_ARCHIVE.md` rotiert (Skript passt nicht auf Phase-8.5-Muster, bewährtes Vorgehen); Modul-Status P8.5 unverändert (3 ✅ · 14 🟡 · 3 ⬜); pytest nicht gelaufen, Tabu-Diff §0.3 leer, Service-Touch 0; nächster Schritt unverändert D5 + V105 + optional vor Z Radiogruppe + Bracket, dann Z) | 2026-09-06 (D4 Sichtprüfung am echten Gerät durch den Nikinger — **nur dokumentiert, kein Code-Touch in dieser opencode/M3-Session**; Block 1–7 + Vorbereitung komplett durchgelaufen, Login beide Accounts ✅, Tastaturnavigation in Firefox+Chrome+Safari auf zwei Accounts ✅, Block 2/4/5-Kern ohne Befund, drei echte Funde dokumentiert: **P8.5-19-Entscheidung Radiogruppe** [User-Präferenz „deutlich angenehmer", Tausch 5 Zeilen in `dialogs.js:584`+`app.html:277` ausstehend, Lucide-Icons `link-2`+`pilcrow`/`text-cursor-input` als Vorschlag offen], **P8.5-6 Bracket-Renderer-Bug** [Source-Escape `\[`/`\]` korrekt, aber `markdown.js`-Parser bricht Link in Vorschau — eckige Klammern zerlegen die URL-Zuordnung, runde Klammern funktionieren; §0.3 erlaubt `webui/static/js/`, Hard-Rule-9-Eskalation greift nicht, Fix-Pfad vor Z], **UX-2-Step-Knotenklick** [neues Feature „erster Klick Readonly-Vorschau, zweiter Klick vollständig" für p8.X parkiert, Fabi sammelt gerade], Save-Button-YAML-Header-Issue wahrscheinlich p8.X [parken bis Verifikation ob außerhalb Header-Kontext], zwei Map-Beobachtungen explizit bestätigt; **Phase 8 ✅ + p8.X als Folge-Phase** als Nikinger-Entscheidung für Z vorgemerkt; Modul-Status-Zeile 6 Block D um D4 ✅ erweitert (mit Findings-Anhang); P8.5-6-Zeile um Bracket-Bug-Caveat; P8.5-17-Zeile Update-Banner-live jetzt ✅; Summary-Zeile 3 ✅ · 14 🟡 · 3 ⬜ unverändert [P8.5-6 bleibt 🟡 Fix ausstehend, P8.5-17 bleibt 🟡 V105 offen]; D3-Block (154 Zeilen) per Hand nach `SESSIONS_ARCHIVE.md` rotiert (Skript passt nicht auf Phase-8.5-Muster); keine Code-Tests, kein Service-Touch; nächster Schritt D5 Vierte A3-Probe + V105 Connector-Check — beides Nikinger; optional vor Z Radiogruppe-Tausch + Bracket-Fix durch opencode/M3) | 2026-09-05 (D3-Prep — `phase8_5_picker_release/scripts/health_gate.sh` neu, 134 Zeilen bash, acht Gates (/health 200 + Retry-Loop, /ui/login 200, /api/v1/me 401, /mcp/ 401, .rail__version aus /ui/static/app.html, /opt/sharefyx/current, --require-todays-update-log, --expected-sha); **Lauf 2026-09-05 15:19:53Z 8/8 grün** gegen den frischen Deploy; **Discovery: D2 lief bereits** zwischen D1 (Commit heute früh) und dieser Session (PID **355956** statt 195922, Release `20260905T140325.378914Z`, ExecMainStartTimestamp `2026-09-05 16:10:18 CEST`), D3 ist Verifikation statt Vorbereitung; D1-Block (111 Zeilen) per Hand nach `SESSIONS_ARCHIVE.md` rotiert (Skript passt nicht auf Phase-8.5-Muster); Modul-Status-Zeile 6 Block D um D2 ✅ + D3 🟡 erweitert; Abnahmestand P8.5-17 Health-Gate-Teil jetzt 🟡 (C/L-Mix, Update-Banner-live + V105 weiter Nikinger); Summary-Zeile 3 ✅ · 14 🟡 · 3 ⬜ korrigiert; pytest nicht gelaufen (kein Python-Touch), `bash -n` OK, shellcheck nicht verfügbar (übersprungen, keine Konvention im Repo), Tabu-Diff §0.3 leer, Service-Touch 0 nur gelesen; nächster Schritt D4 Sichtprüfung am echten Gerät — Nikinger-Aktion) | 2026-09-05 (D1 committet — Badge `v3.0`→`v3.0.1` in `phase5_ui/webui/static/app.html:20` (P8.5-N7, statisches HTML nicht im Tabu §0.3); neuer `## 2026-09-05`-Block in `docs/UPDATE_LOG.md` mit drei Zeilen Picker-Modi/Tastatur/Generalisierter-Hint (Datums-Drift gegenüber Block-C-Spec dokumentiert: Block-C schlug `## 2026-09-04` vor, `date +%F`/`date -u +%F` ist heute 2026-09-05, `deploy.sh` Z. 117–131 verlangt strikt `today_utc`/`today_local`, sonst Gate-Abbruch); Block-C-Block per Hand nach `SESSIONS_ARCHIVE.md` rotiert (newest-first vor B1), Skript `scripts/rotate_session_block.sh` passt nicht auf Phase-8.5-Muster mit einem `## Session stopped` + mehreren `### date`-Subblöcken → Exit 2 „Bereits konform"; Modul-Status-Zeile D `⬜`→`🟡` (D1 fertig, D2–D5 als Nikinger-Aktionen vermerkt); pytest nicht gelaufen (kein Python-Touch), Tabu-Diff §0.3 leer (`app.html` und `docs/UPDATE_LOG.md` nicht tabu), `node --check`/`ui_budget.py` irrelevant; Service-Touch 0 PID 195922 ActiveEnterTimestamp 2026-09-02 11:51:57 CEST nur gelesen; nächster Schritt D2 = `sudo systemctl ... deploy.sh main`) | 2026-09-04 (Block C committet — `scripts/rotate_session_block.sh` aus `scripts/` nach `phase8_5_picker_release/scripts/` portiert (YAGNI aus A1/A2 geschlossen, ein Aufruf `Bereits konform` als Exit-2-Quittung), `wegwerf_setup_v3ritt.py` neu (Port 18773 V98, Standing-Permission-Muster aus Phase 8 reproduziert, 30 Items über 3 Spaces — 12 alpha + 10 beta + 8 gamma, 1 archiviertes, 1 mit item-level `share_read=["gamma"]` P6-§35-39-Fall, 1 mit Bild-Asset `ast_351d4217` per `put_asset()`, 11 explizite Kanten inkl. V102-Zwillings-Kante Buecherliste ↔ Empfehlungen Nikinger), `v3_ritt_playwright_smoke.py` neu (~720 Zeilen, `pyotp`+`async_playwright`, **26/26 Stationen grün: Chromium 13/13 + Firefox 13/13**, V101 für beide Browser bestätigt; 16 Screenshots `docs/screenshots/v3ritt_{chromium,firefox}_NN_*.png`; drei echte Befunde vorgelegt: 1. Smoke-Bug `src_id`→`src` [gefixt im Smoke, kein Server-Bug], 2. CSRF-Origin-Mismatch zwischen `http://127.0.0.1:18773` und `SPACE_PUBLIC_BASE_URL=https://wegwerf-v3ritt.invalid` wegen `_validate_base_url`-Pflicht [Befund für Step Z / Plan §4.C3], 3. Station 12 nur strukturell [bleibt, throwaway-verifiziert in P8]); Modul-Status C `⬜`→`🟡`, Abnahmestand 3 ✅ · 4 🟡 · 13 ⬜ → **3 ✅ · 13 🟡 · 4 ⬜** (P8.5-5/-6/-7/-8/-10/-11/-13/-15/-16 `⬜`→`🟡` mit Belegnotiz je Zeile); B1-Block nach `SESSIONS_ARCHIVE.md` rotiert (manuell — `rotate_session_block.sh` jetzt vorhanden, aber YAGNI-Stand aus A1/A2 gilt für die zweite Rotation nicht mehr, sobald Block D abgeschlossen ist); pytest 962/962 unverändert (kein Python-Touch im Block-C-Setup), Tabu-Diff §0.3 leer (kein `mcpserver/`/`storage/`/`authserver/`/`security.py`/`api.py`/`serializers.py`/`permissions.py`-Touch), Service-Touch 0 (PID 195922 ActiveEnterTimestamp 2026-09-02 11:51:57 CEST nur gelesen, Wegwerf PID 337447 sauber abgebaut via `kill -TERM $(cat serve.pid)`, Hard Rule 9-konform); nächster Schritt Block D) | 2026-09-04 (Wurzel-CLAUDE.md komprimiert — Phase-6-Verlaufsdokumentation + Phase-6/6.5-Vormerkungen + Funnel-Reboot-Notiz + MCP-Werkzeug-Ergonomie-Live-Feedback + End-Korrekturen P5/P4 auf Pointer-Form gestaucht; ~5 KB freigemacht; Wurzel-`updated:`-Pipe analog getrimmt; kein Code, keine Tests, kein Service-Touch; PID 195922 Active seit 2026-09-02 11:51:57 CEST nur gelesen) | 2026-09-04 (B1 committet — `_TITLE_NOT_ID_HINT` in `phase2_mcp/mcpserver/tools.py:159-164` generalisiert (Schlusssatz „Das gilt in jeder Textform — auch nicht als Tabellen-Spalte, nicht in Klammern hinter dem Titel und nicht in Aufzählungs-Zeilen." wörtlich aus Plan §3 B1), `phase2_mcp/tests/test_tools.py` um zwei Asserts (`in jeder Textform`/`Klammern`) im bestehenden `test_tool_descriptions_tell_the_agent_to_name_titles_not_ids` erweitert; neuer Phase-Head-Abschnitt `## Abbruchregel §9.4.1 (N2, verbindlich)` wörtlich aus Plan §3 B1 zwischen Modul-Status und Geerbte Contracts; Modul-Status B1 ⬜→🟡, P8.5-3 ⬜→🟡 mit Klammer-Anmerkung, Stand 3 ✅ · 3 🟡 · 14 ⬜ → 3 ✅ · 4 🟡 · 13 ⬜; pytest 962/962 unverändert (keine neue Testfunktion, nur zwei Asserts in bestehendem Test), Tabu-Diff §0.3 zeigt **genau** `phase2_mcp/mcpserver/tools.py +5/-2` und `phase2_mcp/tests/test_tools.py +2` (Plan: „genau die erlaubte Zeile + Test-Datei"), A2-Block nach `SESSIONS_ARCHIVE.md` rotiert (manuell, wie bisher); PID 195922 Active seit 2026-09-02 11:51:57 CEST nur gelesen, kein Service-Touch; nächster Schritt Block C) | 2026-09-04 (A2 committet — `dialogs.js` Module-Vars `linkPickerItems`/`linkPickerCursor` + `_renderLinkPickerResults` mit State-Reset ganz oben + `_setLinkPickerCursor`/`_pickLinkPickerAt` neu + `closeLinkPicker()`-Reset-Reihenfolge + `keydown`-Handler am Suchfeld (ArrowDown/ArrowUp/Enter, kein Wrap, kein Home/End, kein Raten); `app.css` zwei identische Auswahl-Blöcke zu einem zusammengezogen, totes `:focus` raus; zwei neue statische Tests in `test_static_routes.py` (`test_link_picker_css_has_one_selection_block` P8.5-14, `test_link_picker_picks_run_through_a_single_helper` P8.5-12) plus `test_insertAtCursor_defined_exactly_once_at_module_level` für P8.5-9; Modul-Status A2 ⬜→🟡, fünf Abnahmezeilen P8.5-9/-10/-11/-12/-14 angepasst, Stand 3 ✅ · 0 🟡 · 17 ⬜ → 3 ✅ · 3 🟡 · 14 ⬜; pytest 959→962 (+3, +0.8 KB), ui_budget 5/5 (127.6→128.7 KB, dialogs.js 11.7→12.6 KB), Tabu-Diff §0.3 leer, `node --check` grün auf dialogs.js, A1-Block nach SESSIONS_ARCHIVE.md rotiert (manuell, weil `scripts/`-Verzeichnis für `rotate_session_block.sh` aus Phase 7 noch leer ist — YAGNI für eine zweite manuelle Rotation, Plan-§0.5-Skript-Eintrag verschoben auf Block-C-Beginn mit dem Wegwerf-Setup), PID 195922 Active seit 2026-09-02 11:51:57 CEST nur gelesen, kein Service-Touch; nächster Schritt B1) | 2026-09-04 (Drift nachgezogen — Wurzel-`Current state` mit neuem 2026-09-04-Absatz ergänzt (A1-Eintrag + Drift-Hinweis + Folge-Commit-Vermerk für INDEX-Bullet-Lücke), `docs/INDEX.md` Phase-8.5-Header „⬜ geplant, nicht gestartet" → „🔄 A1 🟡, A2/B1/C/D/Z ⬜", `ROADMAP.md` Phase-8.5-Plan-Absatz „nächster Schritt: A1" → „A1 committet, Drift nachgezogen, nächster Schritt: A2"; INDEX-Bullets für `phase8_5_picker_release/CLAUDE.md` + `SESSIONS_ARCHIVE.md` bewusst NICHT in diesem Commit ergänzt — INDEX steht bei 40917 B, 43 B unter dem 40-KB-Softcap, zwei neue Bullets würden den Cap reißen; Vorschlag: Aufnahme mit gleichzeitiger Trimmung der `updated:`-Pipe in einem späteren Commit, vor A2 nicht nötig; kein Code, kein Service-Touch, pytest/ui_budget unverändert) | 2026-09-04 (A1 committet — `<select id="link-picker-mode">` in app.html:270-280, `dialogs.js` `_linkPickerMode`/`_restoreLinkPickerMode`/neue `onPick({id, title, mode})`-Signatur/change→localStorage, `editor.js` `insertAtCursor` auf Modulebene + `_linkTextFor`/`_appendLinkMarkdown`/`_onLinkPicked`, wiring auf `_onLinkPicked`; Modul-Status A1 ⬜→🟡, Tests ⬜; pytest unverändert 959/959, Tabu-Diff §0.3 leer, ui_budget 5/5 +1.8 KB, node --check grün auf dialogs.js/editor.js/app.js, Service-Touch 0 PID 195922 — V99-Korrektur im Block: erste localStorage-Nutzung des Projekts, sessionStorage→localStorage Eskalation wegen P8.5-G „überlebt Tab-Schließen", `try`/`catch` deckt SecurityError im privaten Modus ab) | 2026-09-03 (Step 0 abgeschlossen — Skelett phase8_5_picker_release/{CLAUDE.md, SESSIONS_ARCHIVE.md, scripts/} angelegt, vier Funde aus Plan §1 abgearbeitet: docs/INDEX.md 52.911 → 40.917 B (-23 %, 43 B unter 40 KB-Softcap) durch Kürzung updated: auf 5 neueste Einträge + Schlusszeile + kompakte Ausnahmenliste (Fund 2) im Wartungsblock, "Büroklammer" → "Lupe" an phase8_ui_graph/CLAUDE.md:440 mit datierter Korrekturnotiz, Phase-8-Bilanz 15/10/0 → 14/12/0 maschinell korrigiert + awk-Kommando im Bilanz-Abschnitt verankert (real 14/12/0 verifiziert); ROADMAP-Absatz + Wurzel-CLAUDE.md down: phase8_ui_graph → phase8_5_picker_release + Current-state-Absatz + updated:-Verlängerung im selben Commit; pytest unverändert 959/959 (kein Python-Touch), Tabu-Diff §0.3 leer, Service-Touch 0 (PID 195922, Active seit 2026-09-02 11:51:57 CEST — nur gelesen); eine Plan-Korrektur: Fund 1 + Fund 2 zusammen erforderten den Ausnahmenblock kompakter als anfangs geschrieben, um den Cap zu halten — kein Plan-Wortlaut gebrochen, im Session-Block dokumentiert)
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

**Statusregel geaendert 2026-09-08 (Nikinger-Entscheidung, Sichtpruefungs-Automatisierungs-
Sub-Session):** ✅ = live-verifiziert durch den Nikinger — **das schliesst ab sofort eine vom
Nikinger selbst gepruefte Wegwerf-Instanz-Automatisierung mit ein**, nicht mehr nur einen
eigenhaendigen Klick-Durchlauf am echten Geraet. (W) = Wegwerf-Instanz + vom Nikinger gepruefte
Evidenz reicht ab sofort fuer ✅, (L) = weiterhin nur gegen die echte Produktion beweisbar
(Identitaets-Kriterien), (C) = Code/Test reicht. Volle Herleitung:
`docs/concepts/sichtpruefung_automation_conventions.md`. P8.5-19 hat zusaetzlich den
„Superseded am selben Tag"-Marker (Radiogruppe → `<select>`-Rueckbau vorgemerkt fuer P8.6).

**Vollstaendige §7-Abnahmematrix P8.5-1 bis P8.5-20 (alle 20 Zeilen mit Status, Art, Beleg,
Commit-SHA, Screenshot-Verweis und Nikinger-Pruefvermerk wo zutreffend):**
`SESSIONS_ARCHIVE.md` §Abnahmematrix-Archiv (Phase 8.5, Z-Final-Rotation). Bilanz-Summary
und Stand-Zaehlung bleiben direkt unten im Head.


**Stand (2026-09-09):** 19 ✅ · 1 🟡 · 0 ⬜ von 20. **Sichtung 2026-09-09:** die 10 🟡-Zeilen
aus dem 2026-09-08-Stand durchgesehen — **9 davon (P8.5-7, -8, -9, -10, -11, -12, -13, -14, -15)
auf ✅**, weil: entweder grüne statische Tests (P8.5-9/-12/-14, (C)-Art) oder
Smoke-Skript-Asserted-Behavior + Screenshot des Daten-Zustands (P8.5-7/-10/-11/-13/-15,
(W)-Art) oder Smoke-Asserted-Behavior allein (P8.5-8, (W)-Art). Nikinger-Vertrauens-Regel
„Code/auto = M3-Sache, visuell = Nikinger-Sache" (neu in
`docs/concepts/sichtpruefung_automation_conventions.md` §2): die (C)-Zeilen + Smoke-(W)-Zeilen
sind durch den ausführenden Agenten verifiziert, kein zusätzlicher Sichtungs-Schritt nötig,
sofern der Beleg dokumentiert ist. **P8.5-6 bleibt 🟡** — der Bracket-Fix vom 2026-09-07 ist
post-Block-C und hat keinen Live-Smoke-Screenshot des Bracket-Pfads; die Block-C-Screenshots
zeigen nur die Edit-Ansicht ohne Vorschau-Panel (Nikinger-Auge reicht nicht für den
Render-Test, neue Konvention `docs/concepts/sichtpruefung_automation_conventions.md` §1:
Vorschau-Pflicht bei klickbaren Links). **Was P8.5-6 zum ✅ braucht:** Mini-Smoke gegen den
v3ritt-Wegwerf mit `[…]`-Titel-Item, **Vorschau-Panel sichtbar im Screenshot**, sodass der
gerenderte Link als klickbarer Hyperlink sichtbar wird (statt nur in der Markdown-Quelle).
**19 ✅:** P8.5-1/-2/-20 (Step 0, Doku), P8.5-3/-4 (2026-09-08, Connector-Live), P8.5-5
(Bauform), P8.5-7/-8/-9/-10/-11/-12/-13/-14/-15 (2026-09-09, Sichtung der Block-C-Evidenz
+ Code/Static-Tests grün), P8.5-16 (2026-09-07 Glass-Fallback), P8.5-17 (2026-09-08 V105
+ Update-Banner), P8.5-18 (2026-09-07 Sichtprüfung 1+2), P8.5-19 (2026-09-08 Radiogruppe,
superseded für P8.6). **1 🟡:** P8.5-6 (siehe oben). **0 ⬜.**

> **Wichtige neue Konventionen aus dieser Sichtung (Nikinger-Feedback 2026-09-09):**
> 1. Vorschau-Pflicht bei klickbaren Links (Screenshots müssen den gerenderten Link zeigen,
>    nicht nur die Markdown-Quelle) — `docs/concepts/sichtpruefung_automation_conventions.md` §1.
> 2. Code/automatisierte Tests = M3/Claude-Code-Sache; visuell = Nikinger-Sache — §2.
> 3. Deploy erst nach Testauswertung, nicht danach — §3 (gilt ab P8.6; Phase-8.5-Vorlauf
>    fuhr bereits genau dieses Muster).
> 4. Screenshots im Chat präsentieren, sobald OpenCode-Vision-Plugin installiert ist
>    (P8.6 first step) — §4.

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

## Nächste Session

**Was als nächstes in Phase 8.5 läuft (NICHT P8.6 — Nikinger-Entscheidung 2026-09-08):**
P8.5-6 ist der einzige verbliebene 🟡. Sichtung 2026-09-09 hat die anderen 9 🟡-Zeilen auf ✅
gehoben; P8.5-6 braucht einen Mini-Smoke gegen den v3ritt-Wegwerf mit
**Vorschau-Panel-sichtbar-Screenshot** eines Items mit `[…]` im Titel (Bracket-Pfad), damit
der gerenderte Link als klickbarer Hyperlink sichtbar wird (neue Konvention
`docs/concepts/sichtpruefung_automation_conventions.md` §1).

**Der P8.5-6-Mini-Smoke im Detail:**
- `phase8_ui_graph/scripts/wegwerf_setup_v3ritt.py setup,seed-items,start` — v3ritt-Wegwerf
  hochfahren, Item mit Titel `Vercel [Hosting]` anlegen
- `phase8_5_picker_release/scripts/v3_ritt_playwright_smoke.py`-Station 6 mit
  `--preview-open`-Flag (neu hinzuzufügen, ~10 Zeilen Skript) oder direkt in einem
  Inline-Smoke: Picker öffnen → `[…]`-Item einfügen → **Vorschau-Panel aufklappen** →
  Screenshot speichern
- Screenshot `docs/screenshots/c4_p856_01_bracket_vorschau.png` + Skript-Output

Bei Erfolg springt Bilanz 19 ✅ · 1 🟡 → **20 ✅ · 0 🟡 · 0 ⬜**, Phase 8.5 dann formal
vollständig abgeschlossen (nicht nur „19 ✅ unter Regel + 1 🟡 als Kandidat").

**Werkzeug:** `SICHTPRUEFUNG_WALKTHROUGH.md` (freundlich), `SICHTPRUEFUNG_RESTBLOCK.md`
(technisch), Login-Snippet mit re-runnablem TOTP-Code am Dateiende des Walkthrough.
Setup-Stand: Production v3.0.1 live (PID 355956 unverändert); die zwei Wegwerf-Instanzen
(200-Knoten auf Port 18772, D2-14-Knoten auf Port 18768) wurden am 2026-09-08 abgebaut —
bei Bedarf neu starten mit `phase8_ui_graph/scripts/wegwerf_setup_{200knoten,d2}.py
setup,seed-items,start` (Hard Rule 9-konform via PID-Datei, niemals `pkill -f`).

**Optional:** falls das OpenCode-Vision-Plugin (P8.6 first step, siehe Vormerkung oben) zu
Beginn dieser Session installiert wird, kann M3 die Screenshots direkt im Chat präsentieren
+ Was-zu-validieren-Zeile darunter — der Nikinger sichtet dann ohne Dateisystem-Umweg.

## Session stopped

### 2026-09-09 (Sichtung der 10 P8.5-🟡-Zeilen — 9 ✅, P8.5-6 bleibt 🟡; vier neue Sichtungs-Konventionen notiert; kein Code-Touch)

**Auftrag:** die seit Block C (2026-09-04) als 🟡 geführten 10 P8.5-Zeilen (P8.5-6, -7, -8,
-9, -10, -11, -12, -13, -14, -15) gegen die am 2026-09-08 geänderte Statusregel sichten
(Nikinger-geprüfte Wegwerf-Instanz zählt als live-verifiziert) und Bilanz aktualisieren.
Belege liegen seit Block C in `docs/screenshots/v3ritt_{chromium,firefox}_*.png` +
`phase8_5_picker_release/scripts/v3_ritt_playwright_smoke.py` + den vier statischen Tests
in `phase5_ui/tests/test_static_routes.py` vor. Scope-Reversal vom 2026-09-08 (nicht P8.6,
sondern Phase 8.5 hier abschließen) ist umgesetzt.

**Methodik:** opencode/M3 sichtet die Screenshots (vision über `Read`-Tool) + die Smoke-
Assertions + die statischen Tests grün, fasst pro Zeile Datei-zum-ersten-Check + Was-du-
siehst + M3-Sichtung-reicht-Tabelle zusammen (10 Zeilen-Einträge im Chat), Nikinger
bewertet jede Zeile mit „✅ / 🟡 / M3 reicht / ich muss selber ran".

**Nikinger-Bewertung pro Zeile (verbatim aus dem Chat):**
- **P8.5-6** — „sieht stark danach aus das Link noch nicht funktioniert, allerdings sieht
  das auch nach der bearbeiten Ansicht aus" → 🟡 bleibt, neue Konvention §1 (Vorschau-Pflicht)
  greift: Block-C-Screenshots zeigen nur Edit-Ansicht ohne Vorschau-Panel, Nikinger-Auge
  reicht nicht für den Render-Test; Bracket-Fix vom 2026-09-07 ist post-Block-C und hat
  keinen Live-Smoke-Screenshot des Bracket-Pfads
- **P8.5-7** — „ja, aber auch hier wäre ein Screenshot mit Vorschau aktiviert besser
  gewesen" → ✅ mit Notiz (Daten-Teil korrekt, Vorschau-Screenshot wäre besser gewesen)
- **P8.5-8 bis -14** — jeweils „code ist deine Sache" → ✅ (Code + Smoke-Asserted-Behavior)
- **P8.5-13** — „auch hier: nächstes mal auf Vorschau klicken zusätzlich" → ✅ mit Notiz
- **P8.5-15** — „sieht ebenfalls korrekt aus" → ✅

**Vier neue Konventionen notiert** (Nikinger-Feedback 2026-09-09, in den richtigen Stellen
verankert):
1. **Vorschau-Pflicht bei klickbaren Links** (Screenshots müssen den gerenderten Link
   zeigen, nicht nur die Markdown-Quelle) — neue Sektion in
   `docs/concepts/sichtpruefung_automation_conventions.md` §1, plus Top-Notiz in
   `SICHTPRUEFUNG_WALKTHROUGH.md` und `SICHTPRUEFUNG_RESTBLOCK.md` mit Verweis auf den
   ausführlichen Konventionstext.
2. **Wer validiert was** — (C) Code/Test durch M3/Claude Code ohne Nikinger-Schritt, (W)
   Wegwerf-Instanz-Automatisierung mit Nikinger-Sichtung, (L) live durch Nikinger,
   Visuelles immer Nikinger-Auge (bis OpenCode-Vision-Plugin in P8.6 installiert ist).
   `docs/concepts/sichtpruefung_automation_conventions.md` §2 als Tabelle.
3. **Deploy erst nach Testauswertung — nicht umgekehrt** (Tests fahren → Sichtung → Stand
   „sicher" → Deploy als Nikinger-Aktion) — `docs/concepts/sichtpruefung_automation_conventions.md`
   §3; gilt ab P8.6, Phase-8.5-Vorlauf fuhr bereits genau dieses Muster
   (D3-Health-Gate 8/8 grün vor D2-Deploy).
4. **Screenshots im Chat präsentieren, sobald OpenCode-Vision-Plugin installiert ist** —
   `docs/concepts/sichtpruefung_automation_conventions.md` §4 plus Update der
   Plugin-Empfehlung in `docs/concepts/sichtpruefung_automation_tooling.md`
   (P8.6 first step ist jetzt explizit „verbindlich", nicht mehr „nächster Schritt für
   eine spätere Session").

**Doc-Updates in diesem Commit (Hard Rule 8):**
- `phase8_5_picker_release/CLAUDE.md` — §Abnahmestand Bilanz 10 ✅ · 10 🟡 → **19 ✅ · 1 🟡
  · 0 ⬜** mit Erklärung pro Zeile, §Nächste Session komplett umgeschrieben auf
  „P8.5-6-Brake-Pfad mit Vorschau-Screenshot", §Session-Block-Update (dieser Block), Frontmatter-
  `updated:`-Pipe vorne ergänzt; alter Z-Closeout-Block rotiert nach `SESSIONS_ARCHIVE.md`
  (manuell, weil `scripts/rotate_session_block.sh` auf das Phase-8.5-Muster mit einem
  `## Session stopped` + mehreren `### date`-Subblöcken nicht passt — bewährtes Vorgehen aus
  den vorherigen Rotationen).
- `phase8_5_picker_release/SESSIONS_ARCHIVE.md` — Z-Closeout-Block vorne angehängt
  (newest-first, verbatim aus dem damaligen Head-Stand), §Abnahmematrix-Archiv-Header
  aktualisiert (Bilanz-Stand), zehn Zeilen P8.5-6/-7/-8/-9/-10/-11/-12/-13/-14/-15 mit neuen
  Status + Nikinger-Sichtungs-Vermerken; Frontmatter `updated:` ergänzt.
- `docs/concepts/sichtpruefung_automation_conventions.md` — neue Sektion
  „Konventionen für Sichtungs-Skripte und -Output (Nikinger-Feedback 2026-09-09)" mit den
  vier Regeln, zwischen Intro und „Der Kernsatz"-Block.
- `docs/concepts/sichtpruefung_automation_tooling.md` — „Nächster konkreter Schritt"-Block
  von „spätere Session" auf „P8.6 first step (Nikinger-Vorgabe 2026-09-08)" verschärft,
  Begründung warum früh (Sichtungs-Reibung ohne Plugin).
- `phase8_5_picker_release/SICHTPRUEFUNG_WALKTHROUGH.md` +
  `phase8_5_picker_release/SICHTPRUEFUNG_RESTBLOCK.md` — Top-Notiz „Wichtig (Sichtungs-
  Konvention 2026-09-09): Vorschau-Pflicht bei klickbaren Links" mit Verweis auf
  `docs/concepts/sichtpruefung_automation_conventions.md` §1.
- `docs/INDEX.md` — Phase-8.5-Header (Bilanz-Stand aktualisiert auf 19/1/0 + neuer Sub-Session-
  Eintrag), Frontmatter-`updated:` vorne ergänzt.
- `docs/ROADMAP.md` — Phase-8.5-Zeile Bilanz-Stand aktualisiert auf 19/1/0 + Sub-Session-
  Vermerk.
- `CLAUDE.md` (root) — Current-State-Absatz um neuen 2026-09-09-Eintrag ergänzt.

**Bilanz-Bewegung:** 10 ✅ · 10 🟡 → **19 ✅ · 1 🟡 · 0 ⬜** (9 von 10 Sichtungs-Zeilen auf
✅, P8.5-6 bleibt 🟡 wegen fehlendem Vorschau-Screenshot des Bracket-Pfads).

**Verifiziert:** kein Python-/JS-Code angefasst (alle Änderungen in `.md`-Dateien +
Frontmatter-Pipes), Tabu-Diff §0.3 leer (kein Servercode-Touch), Production-PID 355956
unverändert (nur gelesen via `systemctl status sharefyx-mcp`), keine Wegwerf-Instanzen
gestartet/gestoppt (Block-C-Screenshots + statische Tests reichen für die 9 ✅-Zeilen).
`pytest phase5_ui/tests/test_static_routes.py` 15/15 grün (für die vier (C)-Zeilen
P8.5-6-Brace-Fix, P8.5-9, P8.5-12, P8.5-14).

**Commit:** ein Commit für diese Sichtung (Doc-Updates in den oben genannten Dateien + alle
`updated:`-Pipes + Frontmatter, kein Code-Touch) — Hard Rule 8 im selben Commit.
Kein Push ohne weitere Anweisung.

**Nächster Schritt:** P8.5-6-Brake-Pfad (Mini-Smoke mit Vorschau-Screenshot) als
Nikinger-/opencode-Aktion in einer Folge-Session, dann Bilanz 20 ✅ · 0 🟡 · 0 ⬜ und Phase
8.5 vollständig abgeschlossen. **Oder:** Sprung direkt zu P8.6-Planung mit OpenCode-Vision-
Plugin-Installation als erstem Schritt — dann eröffnen sich dieselben Sichtungs-Erleichterungen
(Plugin ist da), und der P8.5-6-Brake-Pfad kann inline im ersten P8.6-Schritt mitlaufen.
