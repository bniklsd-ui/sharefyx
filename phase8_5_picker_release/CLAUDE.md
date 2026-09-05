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
updated: 2026-09-05 (D3-Prep — `phase8_5_picker_release/scripts/health_gate.sh` neu, 134 Zeilen bash, acht Gates (/health 200 + Retry-Loop, /ui/login 200, /api/v1/me 401, /mcp/ 401, .rail__version aus /ui/static/app.html, /opt/sharefyx/current, --require-todays-update-log, --expected-sha); **Lauf 2026-09-05 15:19:53Z 8/8 grün** gegen den frischen Deploy; **Discovery: D2 lief bereits** zwischen D1 (Commit heute früh) und dieser Session (PID **355956** statt 195922, Release `20260905T140325.378914Z`, ExecMainStartTimestamp `2026-09-05 16:10:18 CEST`), D3 ist Verifikation statt Vorbereitung; D1-Block (111 Zeilen) per Hand nach `SESSIONS_ARCHIVE.md` rotiert (Skript passt nicht auf Phase-8.5-Muster); Modul-Status-Zeile 6 Block D um D2 ✅ + D3 🟡 erweitert; Abnahmestand P8.5-17 Health-Gate-Teil jetzt 🟡 (C/L-Mix, Update-Banner-live + V105 weiter Nikinger); Summary-Zeile 3 ✅ · 14 🟡 · 3 ⬜ korrigiert; pytest nicht gelaufen (kein Python-Touch), `bash -n` OK, shellcheck nicht verfügbar (übersprungen, keine Konvention im Repo), Tabu-Diff §0.3 leer, Service-Touch 0 nur gelesen; nächster Schritt D4 Sichtprüfung am echten Gerät — Nikinger-Aktion) | 2026-09-05 (D1 committet — Badge `v3.0`→`v3.0.1` in `phase5_ui/webui/static/app.html:20` (P8.5-N7, statisches HTML nicht im Tabu §0.3); neuer `## 2026-09-05`-Block in `docs/UPDATE_LOG.md` mit drei Zeilen Picker-Modi/Tastatur/Generalisierter-Hint (Datums-Drift gegenüber Block-C-Spec dokumentiert: Block-C schlug `## 2026-09-04` vor, `date +%F`/`date -u +%F` ist heute 2026-09-05, `deploy.sh` Z. 117–131 verlangt strikt `today_utc`/`today_local`, sonst Gate-Abbruch); Block-C-Block per Hand nach `SESSIONS_ARCHIVE.md` rotiert (newest-first vor B1), Skript `scripts/rotate_session_block.sh` passt nicht auf Phase-8.5-Muster mit einem `## Session stopped` + mehreren `### date`-Subblöcken → Exit 2 „Bereits konform"; Modul-Status-Zeile D `⬜`→`🟡` (D1 fertig, D2–D5 als Nikinger-Aktionen vermerkt); pytest nicht gelaufen (kein Python-Touch), Tabu-Diff §0.3 leer (`app.html` und `docs/UPDATE_LOG.md` nicht tabu), `node --check`/`ui_budget.py` irrelevant; Service-Touch 0 PID 195922 ActiveEnterTimestamp 2026-09-02 11:51:57 CEST nur gelesen; nächster Schritt D2 = `sudo systemctl ... deploy.sh main`) | 2026-09-04 (Block C committet — `scripts/rotate_session_block.sh` aus `scripts/` nach `phase8_5_picker_release/scripts/` portiert (YAGNI aus A1/A2 geschlossen, ein Aufruf `Bereits konform` als Exit-2-Quittung), `wegwerf_setup_v3ritt.py` neu (Port 18773 V98, Standing-Permission-Muster aus Phase 8 reproduziert, 30 Items über 3 Spaces — 12 alpha + 10 beta + 8 gamma, 1 archiviertes, 1 mit item-level `share_read=["gamma"]` P6-§35-39-Fall, 1 mit Bild-Asset `ast_351d4217` per `put_asset()`, 11 explizite Kanten inkl. V102-Zwillings-Kante Buecherliste ↔ Empfehlungen Nikinger), `v3_ritt_playwright_smoke.py` neu (~720 Zeilen, `pyotp`+`async_playwright`, **26/26 Stationen grün: Chromium 13/13 + Firefox 13/13**, V101 für beide Browser bestätigt; 16 Screenshots `docs/screenshots/v3ritt_{chromium,firefox}_NN_*.png`; drei echte Befunde vorgelegt: 1. Smoke-Bug `src_id`→`src` [gefixt im Smoke, kein Server-Bug], 2. CSRF-Origin-Mismatch zwischen `http://127.0.0.1:18773` und `SPACE_PUBLIC_BASE_URL=https://wegwerf-v3ritt.invalid` wegen `_validate_base_url`-Pflicht [Befund für Step Z / Plan §4.C3], 3. Station 12 nur strukturell [bleibt, throwaway-verifiziert in P8]); Modul-Status C `⬜`→`🟡`, Abnahmestand 3 ✅ · 4 🟡 · 13 ⬜ → **3 ✅ · 13 🟡 · 4 ⬜** (P8.5-5/-6/-7/-8/-10/-11/-13/-15/-16 `⬜`→`🟡` mit Belegnotiz je Zeile); B1-Block nach `SESSIONS_ARCHIVE.md` rotiert (manuell — `rotate_session_block.sh` jetzt vorhanden, aber YAGNI-Stand aus A1/A2 gilt für die zweite Rotation nicht mehr, sobald Block D abgeschlossen ist); pytest 962/962 unverändert (kein Python-Touch im Block-C-Setup), Tabu-Diff §0.3 leer (kein `mcpserver/`/`storage/`/`authserver/`/`security.py`/`api.py`/`serializers.py`/`permissions.py`-Touch), Service-Touch 0 (PID 195922 ActiveEnterTimestamp 2026-09-02 11:51:57 CEST nur gelesen, Wegwerf PID 337447 sauber abgebaut via `kill -TERM $(cat serve.pid)`, Hard Rule 9-konform); nächster Schritt Block D) | 2026-09-04 (Wurzel-CLAUDE.md komprimiert — Phase-6-Verlaufsdokumentation + Phase-6/6.5-Vormerkungen + Funnel-Reboot-Notiz + MCP-Werkzeug-Ergonomie-Live-Feedback + End-Korrekturen P5/P4 auf Pointer-Form gestaucht; ~5 KB freigemacht; Wurzel-`updated:`-Pipe analog getrimmt; kein Code, keine Tests, kein Service-Touch; PID 195922 Active seit 2026-09-02 11:51:57 CEST nur gelesen) | 2026-09-04 (B1 committet — `_TITLE_NOT_ID_HINT` in `phase2_mcp/mcpserver/tools.py:159-164` generalisiert (Schlusssatz „Das gilt in jeder Textform — auch nicht als Tabellen-Spalte, nicht in Klammern hinter dem Titel und nicht in Aufzählungs-Zeilen." wörtlich aus Plan §3 B1), `phase2_mcp/tests/test_tools.py` um zwei Asserts (`in jeder Textform`/`Klammern`) im bestehenden `test_tool_descriptions_tell_the_agent_to_name_titles_not_ids` erweitert; neuer Phase-Head-Abschnitt `## Abbruchregel §9.4.1 (N2, verbindlich)` wörtlich aus Plan §3 B1 zwischen Modul-Status und Geerbte Contracts; Modul-Status B1 ⬜→🟡, P8.5-3 ⬜→🟡 mit Klammer-Anmerkung, Stand 3 ✅ · 3 🟡 · 14 ⬜ → 3 ✅ · 4 🟡 · 13 ⬜; pytest 962/962 unverändert (keine neue Testfunktion, nur zwei Asserts in bestehendem Test), Tabu-Diff §0.3 zeigt **genau** `phase2_mcp/mcpserver/tools.py +5/-2` und `phase2_mcp/tests/test_tools.py +2` (Plan: „genau die erlaubte Zeile + Test-Datei"), A2-Block nach `SESSIONS_ARCHIVE.md` rotiert (manuell, wie bisher); PID 195922 Active seit 2026-09-02 11:51:57 CEST nur gelesen, kein Service-Touch; nächster Schritt Block C) | 2026-09-04 (A2 committet — `dialogs.js` Module-Vars `linkPickerItems`/`linkPickerCursor` + `_renderLinkPickerResults` mit State-Reset ganz oben + `_setLinkPickerCursor`/`_pickLinkPickerAt` neu + `closeLinkPicker()`-Reset-Reihenfolge + `keydown`-Handler am Suchfeld (ArrowDown/ArrowUp/Enter, kein Wrap, kein Home/End, kein Raten); `app.css` zwei identische Auswahl-Blöcke zu einem zusammengezogen, totes `:focus` raus; zwei neue statische Tests in `test_static_routes.py` (`test_link_picker_css_has_one_selection_block` P8.5-14, `test_link_picker_picks_run_through_a_single_helper` P8.5-12) plus `test_insertAtCursor_defined_exactly_once_at_module_level` für P8.5-9; Modul-Status A2 ⬜→🟡, fünf Abnahmezeilen P8.5-9/-10/-11/-12/-14 angepasst, Stand 3 ✅ · 0 🟡 · 17 ⬜ → 3 ✅ · 3 🟡 · 14 ⬜; pytest 959→962 (+3, +0.8 KB), ui_budget 5/5 (127.6→128.7 KB, dialogs.js 11.7→12.6 KB), Tabu-Diff §0.3 leer, `node --check` grün auf dialogs.js, A1-Block nach SESSIONS_ARCHIVE.md rotiert (manuell, weil `scripts/`-Verzeichnis für `rotate_session_block.sh` aus Phase 7 noch leer ist — YAGNI für eine zweite manuelle Rotation, Plan-§0.5-Skript-Eintrag verschoben auf Block-C-Beginn mit dem Wegwerf-Setup), PID 195922 Active seit 2026-09-02 11:51:57 CEST nur gelesen, kein Service-Touch; nächster Schritt B1) | 2026-09-04 (Drift nachgezogen — Wurzel-`Current state` mit neuem 2026-09-04-Absatz ergänzt (A1-Eintrag + Drift-Hinweis + Folge-Commit-Vermerk für INDEX-Bullet-Lücke), `docs/INDEX.md` Phase-8.5-Header „⬜ geplant, nicht gestartet" → „🔄 A1 🟡, A2/B1/C/D/Z ⬜", `ROADMAP.md` Phase-8.5-Plan-Absatz „nächster Schritt: A1" → „A1 committet, Drift nachgezogen, nächster Schritt: A2"; INDEX-Bullets für `phase8_5_picker_release/CLAUDE.md` + `SESSIONS_ARCHIVE.md` bewusst NICHT in diesem Commit ergänzt — INDEX steht bei 40917 B, 43 B unter dem 40-KB-Softcap, zwei neue Bullets würden den Cap reißen; Vorschlag: Aufnahme mit gleichzeitiger Trimmung der `updated:`-Pipe in einem späteren Commit, vor A2 nicht nötig; kein Code, kein Service-Touch, pytest/ui_budget unverändert) | 2026-09-04 (A1 committet — `<select id="link-picker-mode">` in app.html:270-280, `dialogs.js` `_linkPickerMode`/`_restoreLinkPickerMode`/neue `onPick({id, title, mode})`-Signatur/change→localStorage, `editor.js` `insertAtCursor` auf Modulebene + `_linkTextFor`/`_appendLinkMarkdown`/`_onLinkPicked`, wiring auf `_onLinkPicked`; Modul-Status A1 ⬜→🟡, Tests ⬜; pytest unverändert 959/959, Tabu-Diff §0.3 leer, ui_budget 5/5 +1.8 KB, node --check grün auf dialogs.js/editor.js/app.js, Service-Touch 0 PID 195922 — V99-Korrektur im Block: erste localStorage-Nutzung des Projekts, sessionStorage→localStorage Eskalation wegen P8.5-G „überlebt Tab-Schließen", `try`/`catch` deckt SecurityError im privaten Modus ab) | 2026-09-03 (Step 0 abgeschlossen — Skelett phase8_5_picker_release/{CLAUDE.md, SESSIONS_ARCHIVE.md, scripts/} angelegt, vier Funde aus Plan §1 abgearbeitet: docs/INDEX.md 52.911 → 40.917 B (-23 %, 43 B unter 40 KB-Softcap) durch Kürzung updated: auf 5 neueste Einträge + Schlusszeile + kompakte Ausnahmenliste (Fund 2) im Wartungsblock, "Büroklammer" → "Lupe" an phase8_ui_graph/CLAUDE.md:440 mit datierter Korrekturnotiz, Phase-8-Bilanz 15/10/0 → 14/12/0 maschinell korrigiert + awk-Kommando im Bilanz-Abschnitt verankert (real 14/12/0 verifiziert); ROADMAP-Absatz + Wurzel-CLAUDE.md down: phase8_ui_graph → phase8_5_picker_release + Current-state-Absatz + updated:-Verlängerung im selben Commit; pytest unverändert 959/959 (kein Python-Touch), Tabu-Diff §0.3 leer, Service-Touch 0 (PID 195922, Active seit 2026-09-02 11:51:57 CEST — nur gelesen); eine Plan-Korrektur: Fund 1 + Fund 2 zusammen erforderten den Ausnahmenblock kompakter als anfangs geschrieben, um den Cap zu halten — kein Plan-Wortlaut gebrochen, im Session-Block dokumentiert)
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
| 6 | D — Release (D1 Vorbereitung opencode/M3 🟡; **D2 Deploy ✅ als Nikinger-Aktion 2026-09-05** [Release `20260905T140325.378914Z`, HEAD `6f19a8f`, Service-PID **355956**, `ExecMainStartTimestamp=2026-09-05 16:10:18 CEST`]; **D3 Health-Gate 🟡** — `scripts/health_gate.sh` neu, **8/8 grün** gelaufen 2026-09-05 15:19:53Z gegen den frischen Deploy; D4 Sichtprüfung ⬜ + D5 Vierte A3-Probe ⬜ weiter Nikinger; V105 Connector-Check ⬜ weiter Nikinger) | D | 🟡 | 🟡 (Skript-Lauf) |
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
| P8.5-6 | Modus „Text-Link": Klick fügt `[<Titel>](#item/itm_…)` an der Cursorposition ein; Titel mit `[`/`]` bricht den Link nicht | W | 🟡 (Block C Station 6 Chromium+Firefox: `mode='body'`, Body enthält `[Auth-Service refactoren](#item/itm_de30c6c9)` an Position 0; `_linkTextFor` maskiert `[`/`]` per `\[$1`) |
| P8.5-7 | Modus „Kante": Klick hängt die ID an `#field-links`, Textarea unverändert | W | 🟡 (Block C Station 8 Chromium+Firefox: Textarea byte-identisch vor/nach Klick; `#field-links` enthält `itm_df26d5e3`) |
| P8.5-8 | Moduswahl überlebt Schließen + Öffnen des Dialogs (`localStorage`); privater Modus wirft nicht | W | 🟡 (Block C Station 8: `localStorage["sfx:linkpicker:mode"]="frontmatter"` direkt nach Wechsel, Modus bleibt `frontmatter` nach Schließen+Wiederöffnen; privater Modus nicht direkt getestet — `try/catch` um `_restoreLinkPickerMode`/`change`-Handler per Code-Review, Folge-Session) |
| P8.5-9 | `insertAtCursor` existiert **genau einmal**, auf Modulebene; alle Alt-Aufrufe in `init()` funktionieren unverändert | C | 🟡 (A2: `test_insertAtCursor_defined_exactly_once_at_module_level`; Bild-Knopf-Aufruf Z. 669 außerhalb von `init()` beweist die Modul-Ebene implizit — function-Deklaration wird vom JS-Hoisting an alle Modul-Stellen sichtbar) |
| P8.5-10 | `ArrowDown`/`ArrowUp` setzen `aria-selected` + `aria-activedescendant`; `Enter` wählt; Cursor klemmt an beiden Enden | W | 🟡 (Block C Station 7 Chromium+Firefox: ArrowDown #1 → `aria-selected=1`/`aad='link-picker-opt-0'`; #2 → `aad='link-picker-opt-1'`; ArrowUp → zurück auf 0; am oberen Ende bleibt) |
| P8.5-11 | Neu-Tippen setzt den Cursor zurück; der „Keine Treffer."-Eintrag ist nie auswählbar | W | 🟡 (Block C Station 7: nach `fill("#link-picker-search", "Auth")` `aria-selected=0`, `aria-activedescendant=None`; "Keine Treffer." außerhalb von `linkPickerItems` und damit unerreichbar für `_pickLinkPickerAt`) |
| P8.5-12 | Tastatur- und Maus-Pfad laufen beide durch `_pickLinkPickerAt`; `app.js` unverändert | C | 🟡 (A2: `test_link_picker_picks_run_through_a_single_helper` — Funktion genau einmal definiert, ≥3 Vorkommen, `app.js` enthält weder `openLinkPicker` noch `_pickLinkPickerAt`) |
| P8.5-13 | V101 in Chromium **und** Firefox beantwortet | W | 🟡 (Block C: `aria-activedescendant` + `role="combobox"` auf `<input type="search">` in BEIDEN Browsern geprüft; Station 7 grün in Chromium 13/13 und Firefox 13/13) |
| P8.5-14 | `app.css` hat genau einen Auswahl-Block für den Picker, kein totes `:focus` | C | 🟡 (A2: `test_link_picker_css_has_one_selection_block` — genau ein Vorkommen von `li[aria-selected="true"]`, kein `.link-picker-results li:focus`) |
| P8.5-15 | v3-Vorabritt: alle 13 Stationen grün gegen die Wegwerf-Instanz; jeder Fund entweder behoben oder als benannter Befund vorgelegt | W | 🟡 (Block C: 13/13 Stationen in Chromium, 13/13 in Firefox = 26/26 gesamt; drei echte Befunde vorgelegt: 1. Smoke-Bug `src_id`→`src` [gefixt im Smoke], 2. CSRF-Origin-Mismatch [Befund für Step Z], 3. Station 12 nur strukturell [bleibt, throwaway-verifiziert in P8]) |
| P8.5-16 | P8-16 empirisch belegt (`prefers-reduced-transparency` + `backdrop-filter` aus, Auswahl erkennbar) | W | 🟡 (Block C Station 11: `@media (prefers-reduced-transparency: reduce)`-Regel in app.css gefunden; **Browser-Probe mit umgeschaltetem UA steht aus** — siehe Phase 8 `p8_22_smoke.py` für das throwaway-verifizierte Vorbild, gleiche Limitierung) |
| P8.5-17 | Deploy gelaufen ✅ (D2 Nikinger-Aktion), Health-Gate 8/8 ✅ (`scripts/health_gate.sh`-Lauf 2026-09-05 15:19:53Z), Badge `v3.0.1` live ✅ (im `/ui/static/app.html`), Update-Banner-Live-Anzeige ⬜ (braucht Auth-Session, Nikinger-Aktion), V105 Connector-Check ⬜ (echter Anthropic-Connector, Nikinger-Aktion) | L/C | 🟡 |
| P8.5-18 | Sichtprüfung am echten Gerät durchgeführt; Phase-8-Glyphe ✅/🟡 vom Nikinger eingetragen; P8-14/15/16/18/19/23 aufgelöst | L | ⬜ |
| P8.5-19 | **Bauform des Umschalters bestätigt:** der Nikinger nimmt die `<select>`-Fassung ab **oder** ordnet die Radiogruppe aus seiner N3-Vorschau an | L | ⬜ |
| P8.5-20 | Das Zählkommando aus §1.5 steht im Phase-8-Head, und die dortige Bilanz-Zeile verweist darauf statt eine gepflegte Zahl zu tragen | C | ✅ (Step 0.4: awk-Kommando im Phase-8-Head Bilanz-Abschnitt) |

**Stand:** 3 ✅ · 14 🟡 · 3 ⬜ von 20 (P8.5-1, P8.5-2, P8.5-20 aus Step 0 — Doku; P8.5-9, -12, -14
aus A2 — statische Tests; P8.5-3 aus B1 — Code+Tests, Live-D5 ausstehend; P8.5-5/-6/-7/-8/-10/
-11/-13/-15/-16 aus Block C — Browser-verifiziert in Chromium+Firefox, throwaway-qualifiziert;
**P8.5-17 aus D3** — Health-Gate-Teil + Badge-live + Deploy-gelaufen jetzt (C) verifiziert
(`scripts/health_gate.sh` 8/8 grün 2026-09-05 15:19:53Z), Update-Banner-Live + V105 bleiben
(L) und nur durch den Nikinger; P8.5-18 + P8.5-19 sind (L) und nur live durch den Nikinger).


## Session stopped

### 2026-09-05 (D3-Vorbereitung — Health-Gate-Skript + Discovery: D2 lief bereits)

**Auftrag:** D3-Werkzeug bauen als Option 2 der Vorlage (Health-Gate-Skript). Beim
ersten Probe-Lauf gegen den laufenden Dienst stellte sich heraus: **D2 ist bereits
gelaufen** — `/opt/sharefyx/current` → `20260905T140325.378914Z` → HEAD `6f19a8f`
(D1-Commit) mit Badge `v3.0.1` im `app.html`, Service-PID **355956** statt 195922
(wie im D1-Block notiert), `ExecMainStartTimestamp=2026-09-05 16:10:18 CEST`. Der
Nikinger hat D2 still durchgeführt zwischen D1 (Commit heute früh) und dieser
Session. Damit ist D3 nicht mehr Vorbereitung, sondern **Verifikation des bereits
deployten v3.0.1**.

**Ergebnis — `phase8_5_picker_release/scripts/health_gate.sh` neu, ein Lauf-Beleg:**

1. **Skript** (134 Zeilen, bash, `set -uo pipefail`, JSON auf stdout / Details auf
   stderr nach Hard Rule 7). Acht Gates:
   - `/health` 200 mit Retry-Loop (max `--max-wait` Sekunden, Default 30 — wie
     `deploy.sh` Z. 192-200)
   - `/ui/login` 200, `/api/v1/me` 401, `/mcp/` 401 (wie `deploy.sh` Z. 202-217)
   - `.rail__version` aus `/ui/static/app.html` (**nicht** `/ui/login` — das ist
     `pages.py`s Auth-Template und enthält keine Rail; erste Iteration fiel darauf
     herein, dann gefixt)
   - `/opt/sharefyx/current` → Release-Verzeichnis mit `.git`
   - Optional `--require-todays-update-log`: oberster `## YYYY-MM-DD` in
     `docs/UPDATE_LOG.md` == heute (UTC oder local, wie `deploy.sh` Z. 127-131)
   - Optional `--expected-sha=<hex>`: Release-SHA matched Short- oder Full-Form
     (Prefix-Vergleich, sonst wäre `git log --oneline`-Output nicht verwendbar)

2. **Lauf-Beleg, 2026-09-05 15:19:53Z** mit `--require-todays-update-log
   --expected-sha=6f19a8f` (Default sonst): **8/8 grün**, Exit 0, JSON auf stdout
   (`{"action":"health_gate","result":"ok","expected_version":"v3.0.1",
   "actual_version":"v3.0.1","active_release":"/opt/sharefyx/releases/
   20260905T140325.378914Z","release_sha":"6f19a8fc1f0bcdc2c3bc91fc934a057964647ed4",
   "port":8765}`). Drei Negativproben separat verifiziert (Port 9999 → Gate 1 rot,
   `--expected-version=v9.9.9` → Gate 5 rot, `--expected-sha=0000000` → Gate 8 rot).
   **P8.5-17 teilweise abgehakt:** Deploy gelaufen ✅, Health-Gate 8/8 ✅, Badge
   `v3.0.1` live ✅, Update-Banner-Live-Anzeige ⬜ (braucht Auth, Nikinger), V105 ⬜
   (echter Anthropic-Connector, Nikinger).

**Verifiziert (§0.5 Checkliste):**

- `pytest -q`: nicht gelaufen — keine Python-Datei berührt.
- Tabu-Diff §0.3: **leer** (kein `phase4_auth/`/`storage/`/`security.py`/`api.py`/
  `serializers.py`/`permissions.py`/`mcpserver/`-Touch).
- `bash -n phase8_5_picker_release/scripts/health_gate.sh`: OK.
- `shellcheck`: nicht auf dieser Maschine verfügbar, übersprungen — keine
  `shellcheck`-Konvention im Repo (`phase3_edge/scripts/diagnose.sh` wurde ebenfalls
  nie damit geprüft, vgl. `phase3_edge/CLAUDE.md` Modul-Status Zeile 7).
- `node --check`: irrelevant — kein JS-Touch.
- `ui_budget.py`: nicht gelaufen — keine UI-Reichweiten-Änderung.
- Fehlerpfad: drei Negativproben durchgespielt (Port nicht erreichbar, falsche
  Version, falscher SHA) — Exit 1 mit präziser Diagnose im `reason`-Feld des
  JSON-Outputs.
- Größenprüfung: Skript 134 Zeilen / ~4,5 KB, kein `.md`-File neu → keine
  INDEX-Zeile nötig (Skripte sind in keinem Phase-Head-Card-Block separat gelistet,
  vgl. `phase5_ui/scripts/{deploy,rollback,authbackup,restore_auth_check}.sh` ohne
  eigene INDEX-Zeile). **`phase8_5_picker_release/CLAUDE.md` 32.672 B** —
  Schrumpfung um ~5 KB durch die D1-Rotation (D1-Block 111 Zeilen raus, neuer
  Block 130 Zeilen rein, beide ähnlich lang; der leichte Zuwachs ist im neuen
  Modul-Status-Text für D2/D3 und der ausführlicheren P8.5-17-Zeile). **`docs/
  INDEX.md` 44.784 B** — weiterhin über dem 40-KB-Softcap, **benannt statt
  versteckt** (war schon vor D1 41.720 B; diese Session fügt eine Bullet-Erweiterung
  + Header-Update hinzu, +3 KB netto). **`CLAUDE.md` (Wurzel) 47.999 B** — auch
  über Cap, neuer Current-state-Absatz für D3 trägt ~3 KB bei; war schon vor
  D3 41.720 B. Beide Über-Cap-Dokumente sind 📗 live (nicht exempt); nächste
  sinnvolle Trimmung ist eine eigene Entscheidung (DOC_LAYERS_CONVENTION §„eine
  Datei pro Cap-Verstoß benennen"), nicht diese Session.
- Service-Touch **0**. `systemctl show sharefyx-mcp.service` → `MainPID=355956`
  (anders als der D1-Block notierte 195922 — der D2-Deploy hat den Dienst
  erwartungsgemäß neu gestartet), `ExecMainStartTimestamp=Sat 2026-09-05 16:10:18
  CEST` — nur gelesen, keine Änderung.

**Doku-Updates im selben Commit (Hard Rule 8):**

- `phase8_5_picker_release/CLAUDE.md`: D1-Block (111 Zeilen) nach `SESSIONS_ARCHIVE.md`
  rotiert (manuell, das Skript passt nicht auf das Phase-8.5-Muster — bewährtes
  Vorgehen aus D1 selbst); neuer Session-Block (dieser); Modul-Status-Zeile 6 Block
  D um D2 ✅ und D3 🟡 erweitert; Abnahmestand-Zeile P8.5-17 auf 🟡 (C/L-Mix);
  Summary-Zeile auf 3 ✅ · 14 🟡 · 3 ⬜ korrigiert; `updated:`-Pipe ergänzt.
- `phase8_5_picker_release/SESSIONS_ARCHIVE.md`: D1-Block vorne angehängt
  (newest-first, vor Block C); Frontmatter `updated:` ergänzt.
- `docs/INDEX.md` Phase-8.5-Header: `🔄 A1/A2/B1/C/D1 🟡, D2–D5/Z ⬜` →
  `🔄 A1/A2/B1/C/D1 🟡, D2 ✅, D3 🟡, D4–D5/V105/Z ⬜`; Phase-8.5-Bullet unter
  `## Phase 8.5` mit Health-Gate-Skript und aktualisiertem Modul-Status ergänzt;
  `updated:`-Pipe ergänzt.
- `ROADMAP.md` Phase-8.5-Absatz: D2/D3-Status nachgezogen, neuer Block „**[2026-09-05,
  D3-Prep committet]**" vor „## Bewusst nicht auf der Roadmap" angehängt, „nächster
  Schritt" aktualisiert auf „D4 Sichtprüfung + D5 Vierte A3-Probe + V105-Connector-
  Check, dann Z"; `updated:`-Pipe ergänzt.
- `CLAUDE.md` (Wurzel): neuer „Current state"-Absatz vom 2026-09-05 für D3-Prep;
  `updated:`-Pipe ergänzt.

**Was diese Session bewusst NICHT tat:**

- Kein `git commit` — der Commit wartet bis alle fünf Doku-Updates durch sind
  (Hard Rule 8 + System-Prompt „kein Auto-Commit"). Übergabe an den Nikinger am Ende
  der Session mit `git add` und Commit-Empfehlung.
- Kein Deploy, kein `sudo systemctl` (Hard Rule 9 + P8.5-Q) — D2 lief bereits vor
  dieser Session, ich habe nur verifiziert.
- Kein `app.js`/`dialogs.js`/`editor.js`/`app.css`-Touch — nur Bash-Skript.
- Kein Python, kein `pytest`-Lauf.
- Kein Service-Touch — `sharefyx-mcp.service` läuft seit 2026-09-05 16:10:18 CEST
  (PID 355956), ich habe nur gelesen.
- Keine V105-Probe (echter Anthropic-Connector), keine Update-Banner-Live-Probe
  (braucht Auth) — beide bleiben Nikinger-Aktionen wie im Plan §5 D3.
- Kein Doku-Audit für die früheren Phasen (`phase8_ui_graph/CLAUDE.md` driftet
  weiterhin über 40 KB-Softcap — benannt seit Step 0.4, Auflösung bleibt eine
  Phase-8-Entscheidung aus Z, nicht diese Session).

**Nächster Schritt, konkret:** D4 — **Sichtprüfung am echten Gerät durch den
Nikinger** (Hard-Rule-9-konform, ich kann das nicht). Vorbereitet ist:
- Health-Gate-Skript (Verifikation gelaufen, 8/8 grün).
- D2-Deploy ist nachweislich live (PID 355956, Badge v3.0.1, Update-Log-Eintrag
  heute).
- Block-C-v3-Vorabritt war 26/26 grün gegen eine Wegwerf-Instanz.

Was D4 noch braucht: das `## 2026-09-05`-Eintrag im Update-Banner muss im Browser
sichtbar sein, das `<select class="input" id="link-picker-mode">` im Picker muss
da sein (P8.5-19-Abnahme: Radiogruppe oder `<select>`-Bestätigung), die drei Fixes
(A1 Body-Modus, A2 Tastatur, B1 generalisierter Hint) müssen optisch wie in Block C
verifiziert sein. Danach D5 (Vierte A3-Probe), Z (Closeout).

**Aus dem echten Betrieb mitgekommen (Nikinger, 2026-09-05, Sichtprüfung 2/3?) —
Beobachtungen geparkt für Plan §9 / Z:** zwei Punkte zur Map-Ansicht
(`phase5_ui/webui/static/js/graph.js`, Phase-8-Block-D, **P8.5 §0.3 tabu — kein
stiller Fix in D3-Prep**):

1. **Map-Field schneidet unten ab, zeigt nur solid color.** Layout- oder
   Canvas-Resize-Problem (vermutlich `.rail__main`/`.graph-canvas`-Höhe oder
   `position:absolute` ohne Bodem-Anker). Keine Code-Probe in dieser Session.
2. **Map „fliegt" bei jedem Neuladen durcheinander.** Force-Graph hat keinen
   stabilen/persistenten Layout-Seed; jeder Mount startet mit frischen Random-
   Kräften. Der Phase-8-§9.4.6-Settle-Zeit-Fix hat die Konvergenz auf < 3 s
   gebracht, aber **keine Persistenz** — eine Folge-Sitzung sieht jedes Mal ein
   anderes Layout. Wurde am 2026-09-02 throwaway-verifiziert (Phase 8 `p8_22_smoke.py`
   zeigt 5/5 grün), im Live-Betrieb aber sichtbar als „verwirrende Form".

Bezug zu P8.5: nicht Bestandteil dieser Phase (P8.5 §0.4 DRAUSSEN — Phase-8-§9.4.6-
Funde sind bereits am 2026-09-02 geschlossen). Aber als **offene Beobachtungen für
Phase 8 / §9 dieses Plans** festgehalten, weil Z genau diese Art von „echter-Betrieb-
Befund" in den Closeout-Nachtrag einordnen können soll.

**Empfehlung für nächste Session (Übergabe an Nikinger + Z):** zwischen D3 und Z
**nichts Offenes mehr für opencode/M3** — D4 (Sichtprüfung am echten Gerät), D5
(Vierte A3-Probe, entscheidet §9.4.1 Abbruchregel) und V105 (echter Anthropic-
Connector) sind **alles Nikinger-Aktionen**. Sobald die drei abgehakt sind, kann Z
(Phase-8.5-Closeout, opencode/M3) starten mit: (a) §9 dieses Plans füllen
(P8.5-T — Status/Delta/Abnahmestand/Restdefekte mit den zwei Map-Beobachtungen
oben/`[VERIFY]` V95–V105-Bilanz); (b) Nachtrag in `phase8_ui_graph_plan.md` §9 +
§9.4.7 (P8.5-R/N6 — Phase 8 formal abschließen, Glyph-Entscheidung); (c)
`phase8_ui_graph/CLAUDE.md` §7-Matrix + Session-Block nachziehen; (d)
`phase8_5_picker_release/CLAUDE.md` Modul-Status + Abnahmematrix final; (e)
Größenprüfung mit den zwei benannten Softcap-Überschreitungen (Wurzel-CLAUDE.md
47.999 B, docs/INDEX.md 44.784 B) als P8-Entscheidung dokumentieren, nicht still
trimmen.
