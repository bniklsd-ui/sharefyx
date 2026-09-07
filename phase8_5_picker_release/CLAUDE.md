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
updated: 2026-09-06 (D4-Sichtprobe-Folgesession — **nur dokumentiert, kein Code-Touch in dieser opencode/M3-Session**; sieben neue Themen-Cluster aus der Sichtprobe mit Fabian nach D4 dokumentiert: **Spaces-Layout-Reorg** [„Alle Items"-Leiste unter Spaces + Kippschalter, Map 40 % Breite/volle Höhe, keine Duplikate], **Obsidian-Map** fünf Sub-Punkte [Performance-Reload, Landkarten-Stil, Field schneidet ab, Reload-Drift, Collapsible mit Abhängigkeiten], **Anzahl-Anzeige Ordner**, **Edit-in-Place-Vision** [„Bearbeiten"-Knopf überflüssig], **Layering-Design-System** [3 Layer: echtes Schwarz / aktueller Standard / Liquid Glass + Selektion explizit blau auf Hover, Note-Select, Checkbox], **„Konto"→„Einstellungen"-Rename** + Positions-Tausch mit Logout, **De-AI-ierung-Lauf 2** nach neuen Kriterien; neue Datei `docs/concepts/p8x_ui_polish_notes.md` 25 KB L2 mit allen 16 Themen — fünf bereits in D4 dokumentierte p8.X-Punkte [UX-2-Step-Knotenklick, Map-Field schneidet ab, Map fliegt, Save-Button-YAML-Header, Fabis Sammelliste] + sieben Sichtprobe-Folgesession-Cluster + vier Sub-Punkte aus §2 Obsidian-Map; Vorsegmentierter Anhang §A–§E für die Planungs-Session in Claude Code; **kein Phase-8/8.5-Scope-Touch**, **keine** neuen Tabu-Aufhebungen, **kein** Locking — Sammlung, kein Plan; D4-Block per Hand nach `SESSIONS_ARCHIVE.md` rotiert (Skript passt nicht auf Phase-8.5-Muster, bewährtes Vorgehen); Modul-Status P8.5 unverändert (3 ✅ · 14 🟡 · 3 ⬜); pytest nicht gelaufen, Tabu-Diff §0.3 leer, Service-Touch 0; nächster Schritt unverändert D5 + V105 + optional vor Z Radiogruppe + Bracket, dann Z) | 2026-09-06 (D4 Sichtprüfung am echten Gerät durch den Nikinger — **nur dokumentiert, kein Code-Touch in dieser opencode/M3-Session**; Block 1–7 + Vorbereitung komplett durchgelaufen, Login beide Accounts ✅, Tastaturnavigation in Firefox+Chrome+Safari auf zwei Accounts ✅, Block 2/4/5-Kern ohne Befund, drei echte Funde dokumentiert: **P8.5-19-Entscheidung Radiogruppe** [User-Präferenz „deutlich angenehmer", Tausch 5 Zeilen in `dialogs.js:584`+`app.html:277` ausstehend, Lucide-Icons `link-2`+`pilcrow`/`text-cursor-input` als Vorschlag offen], **P8.5-6 Bracket-Renderer-Bug** [Source-Escape `\[`/`\]` korrekt, aber `markdown.js`-Parser bricht Link in Vorschau — eckige Klammern zerlegen die URL-Zuordnung, runde Klammern funktionieren; §0.3 erlaubt `webui/static/js/`, Hard-Rule-9-Eskalation greift nicht, Fix-Pfad vor Z], **UX-2-Step-Knotenklick** [neues Feature „erster Klick Readonly-Vorschau, zweiter Klick vollständig" für p8.X parkiert, Fabi sammelt gerade], Save-Button-YAML-Header-Issue wahrscheinlich p8.X [parken bis Verifikation ob außerhalb Header-Kontext], zwei Map-Beobachtungen explizit bestätigt; **Phase 8 ✅ + p8.X als Folge-Phase** als Nikinger-Entscheidung für Z vorgemerkt; Modul-Status-Zeile 6 Block D um D4 ✅ erweitert (mit Findings-Anhang); P8.5-6-Zeile um Bracket-Bug-Caveat; P8.5-17-Zeile Update-Banner-live jetzt ✅; Summary-Zeile 3 ✅ · 14 🟡 · 3 ⬜ unverändert [P8.5-6 bleibt 🟡 Fix ausstehend, P8.5-17 bleibt 🟡 V105 offen]; D3-Block (154 Zeilen) per Hand nach `SESSIONS_ARCHIVE.md` rotiert (Skript passt nicht auf Phase-8.5-Muster); keine Code-Tests, kein Service-Touch; nächster Schritt D5 Vierte A3-Probe + V105 Connector-Check — beides Nikinger; optional vor Z Radiogruppe-Tausch + Bracket-Fix durch opencode/M3) | 2026-09-05 (D3-Prep — `phase8_5_picker_release/scripts/health_gate.sh` neu, 134 Zeilen bash, acht Gates (/health 200 + Retry-Loop, /ui/login 200, /api/v1/me 401, /mcp/ 401, .rail__version aus /ui/static/app.html, /opt/sharefyx/current, --require-todays-update-log, --expected-sha); **Lauf 2026-09-05 15:19:53Z 8/8 grün** gegen den frischen Deploy; **Discovery: D2 lief bereits** zwischen D1 (Commit heute früh) und dieser Session (PID **355956** statt 195922, Release `20260905T140325.378914Z`, ExecMainStartTimestamp `2026-09-05 16:10:18 CEST`), D3 ist Verifikation statt Vorbereitung; D1-Block (111 Zeilen) per Hand nach `SESSIONS_ARCHIVE.md` rotiert (Skript passt nicht auf Phase-8.5-Muster); Modul-Status-Zeile 6 Block D um D2 ✅ + D3 🟡 erweitert; Abnahmestand P8.5-17 Health-Gate-Teil jetzt 🟡 (C/L-Mix, Update-Banner-live + V105 weiter Nikinger); Summary-Zeile 3 ✅ · 14 🟡 · 3 ⬜ korrigiert; pytest nicht gelaufen (kein Python-Touch), `bash -n` OK, shellcheck nicht verfügbar (übersprungen, keine Konvention im Repo), Tabu-Diff §0.3 leer, Service-Touch 0 nur gelesen; nächster Schritt D4 Sichtprüfung am echten Gerät — Nikinger-Aktion) | 2026-09-05 (D1 committet — Badge `v3.0`→`v3.0.1` in `phase5_ui/webui/static/app.html:20` (P8.5-N7, statisches HTML nicht im Tabu §0.3); neuer `## 2026-09-05`-Block in `docs/UPDATE_LOG.md` mit drei Zeilen Picker-Modi/Tastatur/Generalisierter-Hint (Datums-Drift gegenüber Block-C-Spec dokumentiert: Block-C schlug `## 2026-09-04` vor, `date +%F`/`date -u +%F` ist heute 2026-09-05, `deploy.sh` Z. 117–131 verlangt strikt `today_utc`/`today_local`, sonst Gate-Abbruch); Block-C-Block per Hand nach `SESSIONS_ARCHIVE.md` rotiert (newest-first vor B1), Skript `scripts/rotate_session_block.sh` passt nicht auf Phase-8.5-Muster mit einem `## Session stopped` + mehreren `### date`-Subblöcken → Exit 2 „Bereits konform"; Modul-Status-Zeile D `⬜`→`🟡` (D1 fertig, D2–D5 als Nikinger-Aktionen vermerkt); pytest nicht gelaufen (kein Python-Touch), Tabu-Diff §0.3 leer (`app.html` und `docs/UPDATE_LOG.md` nicht tabu), `node --check`/`ui_budget.py` irrelevant; Service-Touch 0 PID 195922 ActiveEnterTimestamp 2026-09-02 11:51:57 CEST nur gelesen; nächster Schritt D2 = `sudo systemctl ... deploy.sh main`) | 2026-09-04 (Block C committet — `scripts/rotate_session_block.sh` aus `scripts/` nach `phase8_5_picker_release/scripts/` portiert (YAGNI aus A1/A2 geschlossen, ein Aufruf `Bereits konform` als Exit-2-Quittung), `wegwerf_setup_v3ritt.py` neu (Port 18773 V98, Standing-Permission-Muster aus Phase 8 reproduziert, 30 Items über 3 Spaces — 12 alpha + 10 beta + 8 gamma, 1 archiviertes, 1 mit item-level `share_read=["gamma"]` P6-§35-39-Fall, 1 mit Bild-Asset `ast_351d4217` per `put_asset()`, 11 explizite Kanten inkl. V102-Zwillings-Kante Buecherliste ↔ Empfehlungen Nikinger), `v3_ritt_playwright_smoke.py` neu (~720 Zeilen, `pyotp`+`async_playwright`, **26/26 Stationen grün: Chromium 13/13 + Firefox 13/13**, V101 für beide Browser bestätigt; 16 Screenshots `docs/screenshots/v3ritt_{chromium,firefox}_NN_*.png`; drei echte Befunde vorgelegt: 1. Smoke-Bug `src_id`→`src` [gefixt im Smoke, kein Server-Bug], 2. CSRF-Origin-Mismatch zwischen `http://127.0.0.1:18773` und `SPACE_PUBLIC_BASE_URL=https://wegwerf-v3ritt.invalid` wegen `_validate_base_url`-Pflicht [Befund für Step Z / Plan §4.C3], 3. Station 12 nur strukturell [bleibt, throwaway-verifiziert in P8]); Modul-Status C `⬜`→`🟡`, Abnahmestand 3 ✅ · 4 🟡 · 13 ⬜ → **3 ✅ · 13 🟡 · 4 ⬜** (P8.5-5/-6/-7/-8/-10/-11/-13/-15/-16 `⬜`→`🟡` mit Belegnotiz je Zeile); B1-Block nach `SESSIONS_ARCHIVE.md` rotiert (manuell — `rotate_session_block.sh` jetzt vorhanden, aber YAGNI-Stand aus A1/A2 gilt für die zweite Rotation nicht mehr, sobald Block D abgeschlossen ist); pytest 962/962 unverändert (kein Python-Touch im Block-C-Setup), Tabu-Diff §0.3 leer (kein `mcpserver/`/`storage/`/`authserver/`/`security.py`/`api.py`/`serializers.py`/`permissions.py`-Touch), Service-Touch 0 (PID 195922 ActiveEnterTimestamp 2026-09-02 11:51:57 CEST nur gelesen, Wegwerf PID 337447 sauber abgebaut via `kill -TERM $(cat serve.pid)`, Hard Rule 9-konform); nächster Schritt Block D) | 2026-09-04 (Wurzel-CLAUDE.md komprimiert — Phase-6-Verlaufsdokumentation + Phase-6/6.5-Vormerkungen + Funnel-Reboot-Notiz + MCP-Werkzeug-Ergonomie-Live-Feedback + End-Korrekturen P5/P4 auf Pointer-Form gestaucht; ~5 KB freigemacht; Wurzel-`updated:`-Pipe analog getrimmt; kein Code, keine Tests, kein Service-Touch; PID 195922 Active seit 2026-09-02 11:51:57 CEST nur gelesen) | 2026-09-04 (B1 committet — `_TITLE_NOT_ID_HINT` in `phase2_mcp/mcpserver/tools.py:159-164` generalisiert (Schlusssatz „Das gilt in jeder Textform — auch nicht als Tabellen-Spalte, nicht in Klammern hinter dem Titel und nicht in Aufzählungs-Zeilen." wörtlich aus Plan §3 B1), `phase2_mcp/tests/test_tools.py` um zwei Asserts (`in jeder Textform`/`Klammern`) im bestehenden `test_tool_descriptions_tell_the_agent_to_name_titles_not_ids` erweitert; neuer Phase-Head-Abschnitt `## Abbruchregel §9.4.1 (N2, verbindlich)` wörtlich aus Plan §3 B1 zwischen Modul-Status und Geerbte Contracts; Modul-Status B1 ⬜→🟡, P8.5-3 ⬜→🟡 mit Klammer-Anmerkung, Stand 3 ✅ · 3 🟡 · 14 ⬜ → 3 ✅ · 4 🟡 · 13 ⬜; pytest 962/962 unverändert (keine neue Testfunktion, nur zwei Asserts in bestehendem Test), Tabu-Diff §0.3 zeigt **genau** `phase2_mcp/mcpserver/tools.py +5/-2` und `phase2_mcp/tests/test_tools.py +2` (Plan: „genau die erlaubte Zeile + Test-Datei"), A2-Block nach `SESSIONS_ARCHIVE.md` rotiert (manuell, wie bisher); PID 195922 Active seit 2026-09-02 11:51:57 CEST nur gelesen, kein Service-Touch; nächster Schritt Block C) | 2026-09-04 (A2 committet — `dialogs.js` Module-Vars `linkPickerItems`/`linkPickerCursor` + `_renderLinkPickerResults` mit State-Reset ganz oben + `_setLinkPickerCursor`/`_pickLinkPickerAt` neu + `closeLinkPicker()`-Reset-Reihenfolge + `keydown`-Handler am Suchfeld (ArrowDown/ArrowUp/Enter, kein Wrap, kein Home/End, kein Raten); `app.css` zwei identische Auswahl-Blöcke zu einem zusammengezogen, totes `:focus` raus; zwei neue statische Tests in `test_static_routes.py` (`test_link_picker_css_has_one_selection_block` P8.5-14, `test_link_picker_picks_run_through_a_single_helper` P8.5-12) plus `test_insertAtCursor_defined_exactly_once_at_module_level` für P8.5-9; Modul-Status A2 ⬜→🟡, fünf Abnahmezeilen P8.5-9/-10/-11/-12/-14 angepasst, Stand 3 ✅ · 0 🟡 · 17 ⬜ → 3 ✅ · 3 🟡 · 14 ⬜; pytest 959→962 (+3, +0.8 KB), ui_budget 5/5 (127.6→128.7 KB, dialogs.js 11.7→12.6 KB), Tabu-Diff §0.3 leer, `node --check` grün auf dialogs.js, A1-Block nach SESSIONS_ARCHIVE.md rotiert (manuell, weil `scripts/`-Verzeichnis für `rotate_session_block.sh` aus Phase 7 noch leer ist — YAGNI für eine zweite manuelle Rotation, Plan-§0.5-Skript-Eintrag verschoben auf Block-C-Beginn mit dem Wegwerf-Setup), PID 195922 Active seit 2026-09-02 11:51:57 CEST nur gelesen, kein Service-Touch; nächster Schritt B1) | 2026-09-04 (Drift nachgezogen — Wurzel-`Current state` mit neuem 2026-09-04-Absatz ergänzt (A1-Eintrag + Drift-Hinweis + Folge-Commit-Vermerk für INDEX-Bullet-Lücke), `docs/INDEX.md` Phase-8.5-Header „⬜ geplant, nicht gestartet" → „🔄 A1 🟡, A2/B1/C/D/Z ⬜", `ROADMAP.md` Phase-8.5-Plan-Absatz „nächster Schritt: A1" → „A1 committet, Drift nachgezogen, nächster Schritt: A2"; INDEX-Bullets für `phase8_5_picker_release/CLAUDE.md` + `SESSIONS_ARCHIVE.md` bewusst NICHT in diesem Commit ergänzt — INDEX steht bei 40917 B, 43 B unter dem 40-KB-Softcap, zwei neue Bullets würden den Cap reißen; Vorschlag: Aufnahme mit gleichzeitiger Trimmung der `updated:`-Pipe in einem späteren Commit, vor A2 nicht nötig; kein Code, kein Service-Touch, pytest/ui_budget unverändert) | 2026-09-04 (A1 committet — `<select id="link-picker-mode">` in app.html:270-280, `dialogs.js` `_linkPickerMode`/`_restoreLinkPickerMode`/neue `onPick({id, title, mode})`-Signatur/change→localStorage, `editor.js` `insertAtCursor` auf Modulebene + `_linkTextFor`/`_appendLinkMarkdown`/`_onLinkPicked`, wiring auf `_onLinkPicked`; Modul-Status A1 ⬜→🟡, Tests ⬜; pytest unverändert 959/959, Tabu-Diff §0.3 leer, ui_budget 5/5 +1.8 KB, node --check grün auf dialogs.js/editor.js/app.js, Service-Touch 0 PID 195922 — V99-Korrektur im Block: erste localStorage-Nutzung des Projekts, sessionStorage→localStorage Eskalation wegen P8.5-G „überlebt Tab-Schließen", `try`/`catch` deckt SecurityError im privaten Modus ab) | 2026-09-03 (Step 0 abgeschlossen — Skelett phase8_5_picker_release/{CLAUDE.md, SESSIONS_ARCHIVE.md, scripts/} angelegt, vier Funde aus Plan §1 abgearbeitet: docs/INDEX.md 52.911 → 40.917 B (-23 %, 43 B unter 40 KB-Softcap) durch Kürzung updated: auf 5 neueste Einträge + Schlusszeile + kompakte Ausnahmenliste (Fund 2) im Wartungsblock, "Büroklammer" → "Lupe" an phase8_ui_graph/CLAUDE.md:440 mit datierter Korrekturnotiz, Phase-8-Bilanz 15/10/0 → 14/12/0 maschinell korrigiert + awk-Kommando im Bilanz-Abschnitt verankert (real 14/12/0 verifiziert); ROADMAP-Absatz + Wurzel-CLAUDE.md down: phase8_ui_graph → phase8_5_picker_release + Current-state-Absatz + updated:-Verlängerung im selben Commit; pytest unverändert 959/959 (kein Python-Touch), Tabu-Diff §0.3 leer, Service-Touch 0 (PID 195922, Active seit 2026-09-02 11:51:57 CEST — nur gelesen); eine Plan-Korrektur: Fund 1 + Fund 2 zusammen erforderten den Ausnahmenblock kompakter als anfangs geschrieben, um den Cap zu halten — kein Plan-Wortlaut gebrochen, im Session-Block dokumentiert)
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
| P8.5-3 | `_TITLE_NOT_ID_HINT` generalisiert; `test_tools.py` grün mit den zwei neuen Asserts; **Abbruchregel wörtlich im Phase-Head** | C | 🟡 (B1: Code committet — Generalisierung „Das gilt in jeder Textform" + Klammern/Aufzählungs-Zeilen wörtlich aus Plan §3 B1; zwei Asserts `in jeder Textform`/`Klammern` ergänzt; Abbruchregel-Abschnitt zwischen Modul-Status und Geerbte Contracts eingefügt; Live-Verifikation P8.5-4 kommt mit Block D5) |
| P8.5-4 | Vierte A3-Probe über den echten Connector: keine rohe `itm_…`-ID in Fließtext, Tabelle, Klammer, Aufzählung | L | ⬜ |
| P8.5-5 | Picker-Dialog trägt `<select class="input" id="link-picker-mode">` mit beiden Werten; Konvention v3 eingehalten | C | 🟡 (Block C: `dialogs.js:114` `<select class="input" id="link-picker-mode">` mit `value="body"`/`value="frontmatter"`; Konvention v3 eingehalten — `app.html:277-280`; statischer Test `test_link_picker_dialog_has_a_mode_select` aus P8.5-Block wäre Folge-Session) |
| P8.5-6 | Modus „Text-Link": Klick fügt `[<Titel>](#item/itm_…)` an der Cursorposition ein; Titel mit `[`/`]` bricht den Link nicht | W | 🟡 (Block C Station 6 Chromium+Firefox: `mode='body'`, Body enthält `[Auth-Service refactoren](#item/itm_de30c6c9)` an Position 0; `_linkTextFor` maskiert `[`/`]` per `\[$1`; **D4-Fund 2026-09-06: Source-Escape im Body korrekt (`\[Vercel\]` im Titel `itm_67bb0565`), aber `markdown.js`-Link-Parser bricht den Link in der Vorschau — eckige Klammern zerlegen die URL-Zuordnung, runde Klammern funktionieren; §0.3 erlaubt `webui/static/js/`, Fix-Pfad in Folge-Session vor Z, Zeile bleibt 🟡 bis Fix + Re-Verify**) |
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
| P8.5-17 | Deploy gelaufen ✅ (D2 Nikinger-Aktion), Health-Gate 8/8 ✅ (`scripts/health_gate.sh`-Lauf 2026-09-05 15:19:53Z), Badge `v3.0.1` live ✅ (im `/ui/static/app.html`), **Update-Banner-Live-Anzeige ✅ (D4-Sichtprüfung 2026-09-06: drei Zeilen Picker-Modi/Tastatur/Generalisierter-Hint sichtbar)**, V105 Connector-Check ⬜ (echter Anthropic-Connector, Nikinger-Aktion) | L/C | 🟡 |
| P8.5-18 | Sichtprüfung am echten Gerät durchgeführt; Phase-8-Glyphe ✅/🟡 vom Nikinger eingetragen; P8-14/15/16/18/19/23 aufgelöst | L | ✅ (2026-09-07, Nikinger live gegen v3.0.1: P8-14 ✅, P8-15 ✅, P8-18 ✅, P8-19 ✅, P8-23 ✅; P8-16 bleibt 🟡 bis eigene Live-Sichtprüfung der Phase-8-§7-P8-16-Zeile — Cluster-1-Wegwerf-Beleg ist drin, Werfer-Verifikation reicht für P8.5-16 aber nicht für die Phase-8-§7-Statusregel „✅ = live-verifiziert durch den Nikinger"; Phase-8-Glyph-Entscheidung ✅/🟡 ist noch offen — siehe §Abnahme-Sitzung-Block 2026-09-07) |
| P8.5-19 | **Bauform des Umschalters bestätigt:** der Nikinger nimmt die `<select>`-Fassung ab **oder** ordnet die Radiogruppe aus seiner N3-Vorschau an | L | ⬜ |
| P8.5-20 | Das Zählkommando aus §1.5 steht im Phase-8-Head, und die dortige Bilanz-Zeile verweist darauf statt eine gepflegte Zahl zu tragen | C | ✅ (Step 0.4: awk-Kommando im Phase-8-Head Bilanz-Abschnitt) |

**Stand:** 5 ✅ · 13 🟡 · 2 ⬜ von 20 (P8.5-1, P8.5-2, P8.5-20 aus Step 0 — Doku; P8.5-9, -12, -14
aus A2 — statische Tests; P8.5-3 aus B1 — Code+Tests, Live-D5 ausstehend; P8.5-5/-6/-7/-8/-10/
-11/-13/-15 aus Block C — Browser-verifiziert in Chromium+Firefox, throwaway-qualifiziert;
**P8.5-16 vom 2026-09-07 ✅** — `phase8_ui_graph/scripts/p8_16_glass_fallback_probe.py` gegen
Wegwerf 18775, CDP-Switch `prefers-reduced-transparency: reduce`, beide Glass-Träger
(`.list__head` + `.overlay__panel`) wechseln `backdrop-filter: blur(14px) saturate(1.5)` +
`rgba(27,32,39,0.55)` → `backdrop-filter: none` + `rgb(27,32,39)`, Selektion im Solid-Modus
voll erkennbar mit Akzent-Fill + Outline (kein Blur nötig), Restore identisch zur Baseline;
vier Screenshots `docs/screenshots/p8_16_{01..04}_*.png`;
**P8.5-17 aus D3** — Health-Gate-Teil + Badge-live + Deploy-gelaufen jetzt (C) verifiziert
(`scripts/health_gate.sh` 8/8 grün 2026-09-05 15:19:53Z), Update-Banner-Live + V105 bleiben
(L) und nur durch den Nikinger; **P8.5-18 vom 2026-09-07 ✅** — Nikinger-Sichtprüfung 1+2 am
echten Gerät gegen v3.0.1 bestätigt P8-14/15/18/19/23 (Phase-8-§7-Statusregel ✅=live-verifiziert
erfüllt), Phase-8-Glyph-Entscheidung ist noch offen (siehe §Phase-8-Head-Bilanz-Abschnitt);
P8.5-4 (Vierte A3-Probe) und P8.5-19 (Bauform-Entscheidung Radiogruppe vs. `<select>`) bleiben
(L) und nur durch den Nikinger.


## Session stopped

### 2026-09-07 (Cluster 1 der Sichtprüfungen am echten Gerät — P8-16 Glass-Fallback-Probe gegen Wegwerf, P8.5-16 jetzt ✅)

**Auftrag:** Cluster 1 der Sichtprüfungen aus der Liste vom 2026-09-06
durch opencode/M3 als Wegwerf-Probe. P8-16 war die einzige Sichtprüfung
ohne jeden empirischen Beleg (`@media (prefers-reduced-transparency: reduce)`-
Regel im Code, aber nie im Browser gegen UA-Switch geprüft) — also die
Probe, die sich am ehesten aus der offenen Liste ziehen ließ, ohne den
Nikinger an den echten Browser zu binden.

**Ergebnis — P8.5-16 jetzt ✅** (Phase 8 P8-16 bleibt 🟡, throwaway-Eidenz
ist drin, Nikinger-Live-Sichtprüfung gegen v3.0.1 am echten Gerät steht separat
aus, ist Teil der P8.5-18-Live-Verifikation).

**Was gebaut wurde** (Standing-Permission-Rahmen, Phase 8 §0.0 reproduziert):

- `phase8_ui_graph/scripts/wegwerf_setup_p8_16.py` — minimaler Wegwerf-Setup,
  Port 18775, ein User (Niklas als `alpha`), ein Item („Notiz fuer P8-16-Probe"),
  tmp-`DATA_ROOT` unter `/tmp/opencode/sharefyx-wegwerf-p8_16/`, tmp-`auth.sqlite3`,
  File-Keyring (`keyring.set_keyring(FileBackend(...))`), `auth-dek` 32 B Random,
  User direkt in `auth.sqlite3` provisioniert (kein `provision_user.py`),
  `cleanup` per `kill -TERM $(cat serve.pid)` (kein `pkill -f`, Hard Rule 9).
  Pattern 1:1 von `phase8_ui_graph/scripts/wegwerf_setup_c4c5.py` (P8-Block-C
  C4+C5), aber auf das P8-16-Minimum reduziert (keine zweite Space, kein
  Graph-Fixture, keine Mehrfachauswahl).
- `phase8_ui_graph/scripts/p8_16_glass_fallback_probe.py` — Playwright-Probe
  gegen die Wegwerf, single-step Chromium (headless), n=1 Item reicht für die
  Glass-Probe. Sechs Stationen: (1) Login (single-step Form: `space` +
  `password` + `totp` auf einer Seite, `pages.py:160-177` — die zwei Runden
  password→otp im ersten Wurf waren falsch geraten und wurden nach `pages.py`-
  Inspektion auf eine Runde korrigiert); (2) Baseline-Screenshot der Listen-
  Ansicht mit `.list__head` als Glass-Träger; (3) Account-Dialog öffnen
  (`#account-button` → `#account-dialog` ohne `hidden`), `.overlay__panel`-
  Screenshot; (4) CDP-`Emulation.setEmulatedMedia` für `prefers-reduced-
  transparency: reduce` (Playwright hat keine direkte Option für diese Media
  Feature, CDP ist der saubere Weg), Selektor `.overlay__panel` wird
  `wait_for_function` auf `backdrop-filter: none`; (5) Dialog schließen +
  Selektion auf Listenzeile (Klick auf erste `.list__rows button.list__row`,
  die Default-Bucket auf „Offen" filterte unsere eine Note raus, also
  `#home-button` für den globalen „Alle Items"-Scope, danach ist die Zeile
  da); (6) Restore via CDP-`setEmulatedMedia` mit `no-preference` für beide
  Features. Computed-Style-Reads via `page.evaluate` + `getComputedStyle`.

**Beleg (n=1 Probe, 7/7 grün):**

| Check | backdrop-filter | background |
|---|---|---|
| baseline.list__head | `blur(14px) saturate(1.5)` | `rgba(27,32,39,0.55)` |
| baseline.overlay__panel | `blur(14px) saturate(1.5)` | `rgba(27,32,39,0.55)` |
| reduced.overlay__panel | `none` | `rgb(27,32,39)` |
| reduced.list__head | `none` | `rgb(27,32,39)` |
| restored.list__head | `blur(14px) saturate(1.5)` | `matchMedia=false` ✓ |
| reduced.selection | Gradient `linear-gradient(rgba(62,141,243,.2), rgba(62,141,243,.08))` + Outline `1px solid rgba(62,141,243,.4)` — **Selektion voll erkennbar ohne Blur** (Akzent-Fill aus Vormerkung 3 Punkt 1, Outline aus dem 2026-09-02-Nachtrag, der 3-px-transparente Default-Rand reserviert das Boxmodell) | `rgba(0,0,0,0)` |
| items_api | 200, `items,total,limit,offset`-Shape mit der einen Note drin | — |

`@media (prefers-reduced-transparency: reduce)` greift sowohl für den Default-
Block (`.glass` Utility, `app.css:194-200`) als auch für die gruppierte Liste
am Dateiende (`.list__head, .overlay__panel, .update-banner, .toast`,
`app.css:1734-1743`). Die Selektion im Solid-Modus ist nicht allein von
Transparenz abhängig — N8 (Auswahl darf nicht nur über Blur erkennbar sein,
sonst bei deaktiviertem Blur unsichtbar) ist gewahrt.

**Vier Screenshots in `docs/screenshots/`:** `p8_16_01_baseline_list.png`
(Listen-Ansicht, Glass), `p8_16_02_baseline_dialog.png` (Account-Dialog offen,
Glass), `p8_16_03_reduced_transparency_list.png` (Listen-Ansicht mit
`prefers-reduced-transparency: reduce`, solide `.list__head`),
`p8_16_04_reduced_transparency_selection.png` (selektierte Listenzeile im
Solid-Modus, Akzent-Fill + Outline sichtbar). Alle 1440×900, ~80-120 KB pro
Stück.

**Verifiziert (§0.5 Checkliste — Phase 8.5-Konvention):**

- `pytest -q`: nicht gelaufen — keine `.venv`-Python-Datei in
  `phase8_ui_graph/scripts/` berührt (Setup ruft `space_cli.py` als
  Subprocess auf, Smoke ruft Playwright + pyotp, beide nutzen vorhandene
  Libs ohne neue Imports).
- Tabu-Diff §0.3 (`phase4_auth/`/`storage/`/`security.py`/`api.py`/
  `serializers.py`/`permissions.py`/`mcpserver/`): **leer** — die neuen
  Skripte liegen in `phase8_ui_graph/scripts/`, das vom Phase-8.5-Tabu gar
  nicht erfasst wird (das Tabu zielt auf Servercode in `authserver`/
  `mcpserver`/`storage`/`webui/security.py`/etc., nicht auf Wegwerf-Setups
  und Smoke-Skripte; Phase 8 hat ein eigenes Tabu §0.4, das hier auch
  nicht greift).
- `bash -n`/`node --check`/`ui_budget.py`: nicht relevant — keine JS-
  /CSS-/Servercode-Änderung in dieser Session.
- Service-Touch **0**. `systemctl show sharefyx-mcp.service` MainPID=**355956**
  ExecMainStartTimestamp=`Sat 2026-09-05 16:10:18 CEST` (Hard Rule 9 +
  §0.5.7, nur gelesen). Eigene Wegwerf-Instanz sauber per PID-Datei gestoppt,
  kein `pkill -f` mit Regex.
- Größenprüfung am Ende (Ist-Werte): `phase8_5_picker_release/CLAUDE.md` 41.7 KB
  (war 40.9 KB, +0.8 KB netto nach Rotation des Sichtprobe-Folgesession-Blocks
  raus und Cluster-1-P8-16-Block rein — **+0.8 KB ÜBERSCHREITET den 40-KB-Softcap
  erstmals in dieser Phase**, Auflösung ist Z-Arbeit oder ein Trimm-Pass vor Z);
  `SESSIONS_ARCHIVE.md` 79 KB (L3, exempt); `phase8_ui_graph/CLAUDE.md` 94 KB
  (war 93.6 KB, +0.4 KB durch die erweiterte P8-16-Belegs-Spalte, weiter exempt
  als geschlossene Phase mit dem Closeout-Block als einzigem aktiven Inhalt);
  zwei neue Skripte 9.3 KB + 6.7 KB; vier Screenshots ~380 KB gesamt.

**Doku-Updates im selben Commit (Hard Rule 8):**

- `phase8_ui_graph/CLAUDE.md` §7 P8-16-Zeile: Belegs-Spalte um die
  empirische Wegwerf-Eidenz erweitert (Glass-Wechsel + Selektions-Erkennbarkeit
  + vier Screenshots), Status bleibt 🟡 (live-Verifikation durch Nikinger offen).
- `phase8_5_picker_release/CLAUDE.md` §Abnahmestand P8.5-16: 🟡 → ✅, Stand-Zeile
  3 ✅ · 14 🟡 · 3 ⬜ → **4 ✅ · 13 🟡 · 3 ⬜**.
- `phase8_5_picker_release/CLAUDE.md` Session-Block: Sichtprobe-Folgesession
  rotiert nach `SESSIONS_ARCHIVE.md`, dieser Cluster-1-Block hier neu,
  Frontmatter-`updated:` vorne ergänzt.
- `phase8_5_picker_release/SESSIONS_ARCHIVE.md`: Sichtprobe-Folgesession-Block
  vorne angehängt (newest-first, verbatim aus dem Head kopiert, 155 Zeilen
  unverändert), Frontmatter-`updated:` vorne ergänzt.
- `docs/INDEX.md`: zwei neue Zeilen für die Skripte unter Phase 8 + ggf.
  eine Zeile für die Screenshots (zu prüfen, ob die Softcap-Reißer werden —
  siehe unten).

**Was diese Session bewusst NICHT tat:**

- Keine Cluster 2-5 (Sichtprüfung 2+3 / Connector / Fabian) — die folgen
  nach Cluster 1, abhängig vom Nikinger (Live-Browser / Connector).
- Keine Phase-8.5-Bilanz-Sprünge außer P8.5-16 (Phase 8 P8-16 bleibt 🟡 bis
  Nikinger-Live; Phase-8-Bilanz bleibt 14/12/0).
- Keine Aufhebung von Phase-8/8.5-Tabus.
- Kein `sudo systemctl`, keine `systemctl show`-Calls (nur eine
  `show`-Abfrage am Anfang zur Übergabe-Notierung, danach nur die eigenen
  Wegwerf-Instanzen via `cat serve.pid` + `kill`).
- Kein `git commit` — Working Tree enthält jetzt 13 uncommittete Dateien
  (7 von D4+Sichtprobe-Folgesession + 6 von Cluster 1). Nikinger entscheidet
  Commit-Schnitt (vermutlich getrennt: D4+Sichtprobe zusammen, dann Cluster 1+
  Status-Updates als Folge-Commit).

**Nächster Schritt, konkret:**

- **Cluster 2** (Sichtprüfung 2 + 3 am echten Gerät durch den Nikinger, ~25 Min):
  P8-14 (Plex 16px), P8-15 (Farblegende), P8-18 + P8-19 (Übersicht tabellos +
  „Alle Items"-Scope), P8-23 (post-deploy-Abnahme), P8.5-18 (umbrella) +
  P8-16 (Phase-8-Aspekt, throwaway-Eidenz schon da). Doppelung mit Phase-8
  P8-22/24 (200-Knoten-Settle + Ritt Übersicht→Scope→Graph→Klick→Item) und
  P8-20 (Graph-Knotenklick) und P8-21 (Tag-/Ordner-Toggles + Cutoff) ist
  Cluster 3.
- **Cluster 3** (Verhalten am echten Gerät, ~15 Min): P8-20, P8-21, P8-22,
  P8-24 — eine zusammenhängende Login-Sitzung am live v3.0.1.
- **Cluster 4** (Connector, ~10 Min): P8.5-3 (Live-D5 entscheidet §9.4.1),
  P8.5-4 (Vierte A3-Probe), P8.5-17 (V105), P8.5-19 (Bauform-Entscheidung
  Radiogruppe vs. `<select>`, 30 Sek).
- **Cluster 5** (Fabian-Sitzung): P8-5, P8-8 — wenn Fabian verfügbar oder
  `testnutzer-p7` zur Hand.
- **Optional vor Z** durch opencode/M3: P8.5-19-Tausch (5 Z. in `dialogs.js`+
  `app.html`) + P8.5-6 Bracket-Renderer-Fix (in `markdown.js`) — damit Z
  die Endabnahme-Zeilen auf ✅ heben kann.
- **Z** (Phase-8.5-Closeout): nach allen Clustern, mit Verweis auf
  `docs/concepts/p8x_ui_polish_notes.md` als Wahrheits-Quelle für p8.X.
- **`git commit`**: Nikinger entscheidet.

**Größe-Hinweis:** Phase-Head **41.7 KB**, erstmals über 40 KB-Softcap in
dieser Phase (war 40.9 KB am Ende Sichtprobe-Folgesession, +0.8 KB netto).
Auflösung bleibt Z (Phase-8.5-Closeout kann den Head auf ein normales
Maß bringen) oder ein Trimm-Pass vor Z — beides nicht diese Session.
