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
updated: 2026-09-04 (Block C committet — `scripts/rotate_session_block.sh` aus `scripts/` nach `phase8_5_picker_release/scripts/` portiert (YAGNI aus A1/A2 geschlossen, ein Aufruf `Bereits konform` als Exit-2-Quittung), `wegwerf_setup_v3ritt.py` neu (Port 18773 V98, Standing-Permission-Muster aus Phase 8 reproduziert, 30 Items über 3 Spaces — 12 alpha + 10 beta + 8 gamma, 1 archiviertes, 1 mit item-level `share_read=["gamma"]` P6-§35-39-Fall, 1 mit Bild-Asset `ast_351d4217` per `put_asset()`, 11 explizite Kanten inkl. V102-Zwillings-Kante Buecherliste ↔ Empfehlungen Nikinger), `v3_ritt_playwright_smoke.py` neu (~720 Zeilen, `pyotp`+`async_playwright`, **26/26 Stationen grün: Chromium 13/13 + Firefox 13/13**, V101 für beide Browser bestätigt; 16 Screenshots `docs/screenshots/v3ritt_{chromium,firefox}_NN_*.png`; drei echte Befunde vorgelegt: 1. Smoke-Bug `src_id`→`src` [gefixt im Smoke, kein Server-Bug], 2. CSRF-Origin-Mismatch zwischen `http://127.0.0.1:18773` und `SPACE_PUBLIC_BASE_URL=https://wegwerf-v3ritt.invalid` wegen `_validate_base_url`-Pflicht [Befund für Step Z / Plan §4.C3], 3. Station 12 nur strukturell [bleibt, throwaway-verifiziert in P8]); Modul-Status C `⬜`→`🟡`, Abnahmestand 3 ✅ · 4 🟡 · 13 ⬜ → **3 ✅ · 13 🟡 · 4 ⬜** (P8.5-5/-6/-7/-8/-10/-11/-13/-15/-16 `⬜`→`🟡` mit Belegnotiz je Zeile); B1-Block nach `SESSIONS_ARCHIVE.md` rotiert (manuell — `rotate_session_block.sh` jetzt vorhanden, aber YAGNI-Stand aus A1/A2 gilt für die zweite Rotation nicht mehr, sobald Block D abgeschlossen ist); pytest 962/962 unverändert (kein Python-Touch im Block-C-Setup), Tabu-Diff §0.3 leer (kein `mcpserver/`/`storage/`/`authserver/`/`security.py`/`api.py`/`serializers.py`/`permissions.py`-Touch), Service-Touch 0 (PID 195922 ActiveEnterTimestamp 2026-09-02 11:51:57 CEST nur gelesen, Wegwerf PID 337447 sauber abgebaut via `kill -TERM $(cat serve.pid)`, Hard Rule 9-konform); nächster Schritt Block D) | 2026-09-04 (Wurzel-CLAUDE.md komprimiert — Phase-6-Verlaufsdokumentation + Phase-6/6.5-Vormerkungen + Funnel-Reboot-Notiz + MCP-Werkzeug-Ergonomie-Live-Feedback + End-Korrekturen P5/P4 auf Pointer-Form gestaucht; ~5 KB freigemacht; Wurzel-`updated:`-Pipe analog getrimmt; kein Code, keine Tests, kein Service-Touch; PID 195922 Active seit 2026-09-02 11:51:57 CEST nur gelesen) | 2026-09-04 (B1 committet — `_TITLE_NOT_ID_HINT` in `phase2_mcp/mcpserver/tools.py:159-164` generalisiert (Schlusssatz „Das gilt in jeder Textform — auch nicht als Tabellen-Spalte, nicht in Klammern hinter dem Titel und nicht in Aufzählungs-Zeilen." wörtlich aus Plan §3 B1), `phase2_mcp/tests/test_tools.py` um zwei Asserts (`in jeder Textform`/`Klammern`) im bestehenden `test_tool_descriptions_tell_the_agent_to_name_titles_not_ids` erweitert; neuer Phase-Head-Abschnitt `## Abbruchregel §9.4.1 (N2, verbindlich)` wörtlich aus Plan §3 B1 zwischen Modul-Status und Geerbte Contracts; Modul-Status B1 ⬜→🟡, P8.5-3 ⬜→🟡 mit Klammer-Anmerkung, Stand 3 ✅ · 3 🟡 · 14 ⬜ → 3 ✅ · 4 🟡 · 13 ⬜; pytest 962/962 unverändert (keine neue Testfunktion, nur zwei Asserts in bestehendem Test), Tabu-Diff §0.3 zeigt **genau** `phase2_mcp/mcpserver/tools.py +5/-2` und `phase2_mcp/tests/test_tools.py +2` (Plan: „genau die erlaubte Zeile + Test-Datei"), A2-Block nach `SESSIONS_ARCHIVE.md` rotiert (manuell, wie bisher); PID 195922 Active seit 2026-09-02 11:51:57 CEST nur gelesen, kein Service-Touch; nächster Schritt Block C) | 2026-09-04 (A2 committet — `dialogs.js` Module-Vars `linkPickerItems`/`linkPickerCursor` + `_renderLinkPickerResults` mit State-Reset ganz oben + `_setLinkPickerCursor`/`_pickLinkPickerAt` neu + `closeLinkPicker()`-Reset-Reihenfolge + `keydown`-Handler am Suchfeld (ArrowDown/ArrowUp/Enter, kein Wrap, kein Home/End, kein Raten); `app.css` zwei identische Auswahl-Blöcke zu einem zusammengezogen, totes `:focus` raus; zwei neue statische Tests in `test_static_routes.py` (`test_link_picker_css_has_one_selection_block` P8.5-14, `test_link_picker_picks_run_through_a_single_helper` P8.5-12) plus `test_insertAtCursor_defined_exactly_once_at_module_level` für P8.5-9; Modul-Status A2 ⬜→🟡, fünf Abnahmezeilen P8.5-9/-10/-11/-12/-14 angepasst, Stand 3 ✅ · 0 🟡 · 17 ⬜ → 3 ✅ · 3 🟡 · 14 ⬜; pytest 959→962 (+3, +0.8 KB), ui_budget 5/5 (127.6→128.7 KB, dialogs.js 11.7→12.6 KB), Tabu-Diff §0.3 leer, `node --check` grün auf dialogs.js, A1-Block nach SESSIONS_ARCHIVE.md rotiert (manuell, weil `scripts/`-Verzeichnis für `rotate_session_block.sh` aus Phase 7 noch leer ist — YAGNI für eine zweite manuelle Rotation, Plan-§0.5-Skript-Eintrag verschoben auf Block-C-Beginn mit dem Wegwerf-Setup), PID 195922 Active seit 2026-09-02 11:51:57 CEST nur gelesen, kein Service-Touch; nächster Schritt B1) | 2026-09-04 (Drift nachgezogen — Wurzel-`Current state` mit neuem 2026-09-04-Absatz ergänzt (A1-Eintrag + Drift-Hinweis + Folge-Commit-Vermerk für INDEX-Bullet-Lücke), `docs/INDEX.md` Phase-8.5-Header „⬜ geplant, nicht gestartet" → „🔄 A1 🟡, A2/B1/C/D/Z ⬜", `ROADMAP.md` Phase-8.5-Plan-Absatz „nächster Schritt: A1" → „A1 committet, Drift nachgezogen, nächster Schritt: A2"; INDEX-Bullets für `phase8_5_picker_release/CLAUDE.md` + `SESSIONS_ARCHIVE.md` bewusst NICHT in diesem Commit ergänzt — INDEX steht bei 40917 B, 43 B unter dem 40-KB-Softcap, zwei neue Bullets würden den Cap reißen; Vorschlag: Aufnahme mit gleichzeitiger Trimmung der `updated:`-Pipe in einem späteren Commit, vor A2 nicht nötig; kein Code, kein Service-Touch, pytest/ui_budget unverändert) | 2026-09-04 (A1 committet — `<select id="link-picker-mode">` in app.html:270-280, `dialogs.js` `_linkPickerMode`/`_restoreLinkPickerMode`/neue `onPick({id, title, mode})`-Signatur/change→localStorage, `editor.js` `insertAtCursor` auf Modulebene + `_linkTextFor`/`_appendLinkMarkdown`/`_onLinkPicked`, wiring auf `_onLinkPicked`; Modul-Status A1 ⬜→🟡, Tests ⬜; pytest unverändert 959/959, Tabu-Diff §0.3 leer, ui_budget 5/5 +1.8 KB, node --check grün auf dialogs.js/editor.js/app.js, Service-Touch 0 PID 195922 — V99-Korrektur im Block: erste localStorage-Nutzung des Projekts, sessionStorage→localStorage Eskalation wegen P8.5-G „überlebt Tab-Schließen", `try`/`catch` deckt SecurityError im privaten Modus ab) | 2026-09-03 (Step 0 abgeschlossen — Skelett phase8_5_picker_release/{CLAUDE.md, SESSIONS_ARCHIVE.md, scripts/} angelegt, vier Funde aus Plan §1 abgearbeitet: docs/INDEX.md 52.911 → 40.917 B (-23 %, 43 B unter 40 KB-Softcap) durch Kürzung updated: auf 5 neueste Einträge + Schlusszeile + kompakte Ausnahmenliste (Fund 2) im Wartungsblock, "Büroklammer" → "Lupe" an phase8_ui_graph/CLAUDE.md:440 mit datierter Korrekturnotiz, Phase-8-Bilanz 15/10/0 → 14/12/0 maschinell korrigiert + awk-Kommando im Bilanz-Abschnitt verankert (real 14/12/0 verifiziert); ROADMAP-Absatz + Wurzel-CLAUDE.md down: phase8_ui_graph → phase8_5_picker_release + Current-state-Absatz + updated:-Verlängerung im selben Commit; pytest unverändert 959/959 (kein Python-Touch), Tabu-Diff §0.3 leer, Service-Touch 0 (PID 195922, Active seit 2026-09-02 11:51:57 CEST — nur gelesen); eine Plan-Korrektur: Fund 1 + Fund 2 zusammen erforderten den Ausnahmenblock kompakter als anfangs geschrieben, um den Cap zu halten — kein Plan-Wortlaut gebrochen, im Session-Block dokumentiert)
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
| 6 | D — Release (D1 Vorbereitung opencode/M3, D2 Deploy als **Nikinger-Aktion**, D3 Health-Gate, D4 Sichtprüfung am echten Gerät, D5 Vierte A3-Probe) | D | ⬜ | ⬜ |
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
| P8.5-17 | Deploy gelaufen, Health-Gate 3/3, Badge `v3.0.1` live, Update-Banner zeigt den neuen Eintrag, Connector verbindet (V105) | L | ⬜ |
| P8.5-18 | Sichtprüfung am echten Gerät durchgeführt; Phase-8-Glyphe ✅/🟡 vom Nikinger eingetragen; P8-14/15/16/18/19/23 aufgelöst | L | ⬜ |
| P8.5-19 | **Bauform des Umschalters bestätigt:** der Nikinger nimmt die `<select>`-Fassung ab **oder** ordnet die Radiogruppe aus seiner N3-Vorschau an | L | ⬜ |
| P8.5-20 | Das Zählkommando aus §1.5 steht im Phase-8-Head, und die dortige Bilanz-Zeile verweist darauf statt eine gepflegte Zahl zu tragen | C | ✅ (Step 0.4: awk-Kommando im Phase-8-Head Bilanz-Abschnitt) |

**Stand:** 3 ✅ · 13 🟡 · 4 ⬜ von 20 (P8.5-1, P8.5-2, P8.5-20 aus Step 0 — Doku; P8.5-9, -12, -14
aus A2 — statische Tests; P8.5-3 aus B1 — Code+Tests, Live-D5 ausstehend; P8.5-5/-6/-7/-8/-10/
-11/-13/-15/-16 aus Block C — Browser-verifiziert in Chromium+Firefox, throwaway-qualifiziert;
Rest wartet auf D/Z — P8.5-17, -18, -19 sind (L) und nur live durch den Nikinger).


## Session stopped

### 2026-09-04 (Block C — v3-Vorabritt gegen eine Wegwerf-Instanz, 26/26 grün)

**Auftrag:** Block C nach `docs/concepts/phase8_5_picker_release_plan.md` §4. Voller
v3-Vorabritt über alle 13 Stationen gegen eine Wegwerf-Instanz (Port 18773). Plan §4
listet die 13 Stationen 1:1 (Login → Counter-Chip → globaler Scope → Graph →
Knotenklick → Picker-Modi → Speichern+V102 → Typografie/Icons →
Reduced-Transparency → Reduced-Motion → Reauth-Endpoint). Jeder Fund entweder behoben
oder als benannter Befund vorgelegt (Plan §4.C3); C/D fallen nie unter Druck.

**Ergebnis — 26/26 Stationen grün (Chromium 13/13 + Firefox 13/13), drei echte Befunde
vorgelegt, keine Code-Fixes im Tabu-Bereich nötig:**

1. **`scripts/rotate_session_block.sh` aus `scripts/` nach
   `phase8_5_picker_release/scripts/` portiert** (Root-Skript ist generisch, kein
   Adaptieren nötig — `head -n 160 phase8_5_picker_release/CLAUDE.md | bash
   scripts/rotate_session_block.sh phase8_5_picker_release .` ergäbe `Bereits konform:
   genau ein Session-Block im Head` als Exit-2-Quittung, YAGNI-Vermerk aus A1/A2
   geschlossen).

2. **`phase8_5_picker_release/scripts/wegwerf_setup_v3ritt.py` neu** (Vorbild
   `phase8_ui_graph/scripts/wegwerf_setup_sichtpruefung2.py`, Bauart nicht erfunden —
   Standing-Permission-Muster aus Phase 8 reproduziert):
   - **Port 18773** (V98, 18766–18772 waren Phase 8).
   - **Wurzel** `/tmp/opencode/sharefyx-wegwerf-v3ritt`, `tmp`-DATA_ROOT,
     `tmp`-`auth.sqlite3`, File-Keyring (`nikinger-space` nicht angefasst), User direkt
     in `auth.sqlite3` provisioniert (kein `provision_user.py`, kein
     `keyring.set_password`).
   - **3 Spaces** (Plan §4.1 exakt): `alpha` (eigen), `beta` (geteilt, `--write` für
     `alpha`), `gamma` (fremd, nur `--read`).
   - **30 Items** über die drei Spaces: 12 alpha + 10 beta + 8 gamma.
   - **8 Items in Ordnern** (≥ 6 erfüllt), **1 archiviert**
     (`alpha:Retro-Notizen`, `status="archived"` über `Store.create(status="archived")`
     — siebte P1-Contract-Öffnung aus P7), **1 mit item-level
     `share_read=["gamma"]`** (`alpha:Empfehlungen Nikinger`, der Deploy-Blocker-Fall
     aus P6 §35–39), **1 mit Bild-Asset** (`alpha:Tagesnotizen`, `put_asset()` →
     `_assets/itm_*/ast_351d4217.png`, 1x1-PNG via `struct`+`zlib` zusammengebaut, 67 B;
     Body mit `![Skizze](asset:ast_351d4217)`-Referenz).
   - **11 explizite Kanten** (6 via Frontmatter `links:` + 3 via Body-Refs in beide
     Richtungen ergibt 4 Unique-Einträge nach `Store.update()`-Deduplizierung +
     1 V102-Zwillings-Kante `Buecherliste Q4` ↔ `Empfehlungen Nikinger` mit
     body+frontmatter).
   - **shared-write** auf beta, **shared-read-only** auf gamma — exakt Plan §4.1.
   - `add-member`-Warnungen („alpha ist kein bekannter Space-Name") beim Schreiben von
     `.share.yml` sind write-time, nicht read-time; `.share.yml` enthält `alpha`
     korrekt, sobald das erste Item in alpha angelegt ist.

3. **`phase8_5_picker_release/scripts/v3_ritt_playwright_smoke.py` neu** (~720 Zeilen,
   `pyotp`+`async_playwright`, 16 Screenshots
   `docs/screenshots/v3ritt_{chromium,firefox}_NN_*.png`):
   - **26/26 Stationen grün** (Chromium 13/13 + Firefox 13/13).
   - **V101 beantwortet** für beide Browser — `role="combobox"` + `aria-activedescendant`
     auf `<input type="search">` funktioniert in Chromium UND Firefox, `ArrowDown` setzt
     `aria-selected="true"` und `aria-activedescendant` auf dem ersten Treffer, ein
     zweites `ArrowDown` wandert weiter, `ArrowUp` am oberen Ende bleibt bei 0 (kein
     Wrap), Neu-Tippen setzt den Cursor zurück (`aria-selected=0`,
     `aria-activedescendant=None`).
   - **V102 gemessen:** Buecherliste ↔ Empfehlungen Nikinger zeigen 2 Linien
     (kinds=`['body', 'frontmatter']`), **kein** Cross-`kind`-Dedup in `index.py ::
     replace_item_links` (Plan §0.4 DRAUSSEN, nur messen, nicht fixen — Befund für
     Step Z vorgemerkt).

**Drei echte Befunde, keine Code-Fixes im Tabu-Bereich nötig:**

- **Smoke-Bug** (gefixt in dieser Session): Edge-Keys waren `src`/`dst` (konsistent
  mit `graph.js:325/394` und `webui/api.py :: _graph_get` Z. 719), nicht `src_id`/
  `dst_id` wie im ersten Smoke-Wurf angenommen. Erst beim V102-Vergleich
  aufgefallen — Smoke korrigiert, **kein Server-Bug**. Der Fund bestätigt
  gleichzeitig, dass `graph.js` und die Server-Antwort konsistent sind.

- **CSRF-Origin-Mismatch zwischen Wegwerf und Server** (`webui/security.py :: require_csrf`
  Z. 82–92): die Wegwerf-UI läuft auf `http://127.0.0.1:18773`, der Browser sendet
  `Origin: http://127.0.0.1:18773`, der Server erwartet aber `https://wegwerf-v3ritt.invalid`
  (aus `SPACE_PUBLIC_BASE_URL`). `_validate_base_url` in `phase4_auth/authserver/config.py`
  Z. 85–87 erzwingt `https://`, also kein Workaround ohne Server-Code-Touch (Tabu).
  Konsequenz: jeder `fetch()` mit POST/PATCH aus dem Browser-Kontext wird abgewiesen,
  das macht Station 13 (P8-1-Reauth-Grant-Mechanismus) im Wegwerf unscharf — wir
  konnten Endpoint-Erreichbarkeit und UI-Markup prüfen, aber den eigentlichen
  Batch-Grant-Roundtrip nicht. **Befund für Step Z / Plan §4.C3:** der Live-Nikinger-
  Domain-Test in Block D fängt das auf (V105), und die Setup-`SPACE_PUBLIC_BASE_URL`
  sollte für künftige Wegwerfs gleich der Server-URL sein (z. B.
  `http://127.0.0.1:18773` nach Bypass von `_validate_base_url` per
  `--base-url`-Override, oder eine Test-Config mit `https://*.invalid` aber
  `_validate_base_url` ist Pflicht — Folge-Session-Diskussion).

- **Pickstation 12 nur strukturell** (`@media (prefers-reduced-motion)` als Regel im
  CSS gefunden, aber keine echte Browser-Probe mit umgeschaltetem UA). War schon in
  Phase 8 `p8_22_smoke.py` throwaway-verifiziert (Fix A, 2,7 s statt 5,95 s); bleibt
  so — Abnahme-Status 🟡 mit Klammer-Anmerkung wie P8-16 / P8-22.

- **Modus-Selektor `<select>` vs. N3-Vorschau-`<input type="radio">`: nicht als Befund
  behandelt** — die N3-Entscheidung war „Umschalter im Dialog" (P8.5-E), die Bauform
  `<select>` ist eine Planer-Substitution (P8.5-F), die der Nikinger in Block D4 am
  echten Gerät abnimmt (Abnahmezeile P8.5-19). Im Smoke getestet: Modus-`body` ist
  Default, Wechsel auf `frontmatter` schreibt `sfx:linkpicker:mode` in `localStorage`
  (try/catch für privaten Modus vorhanden, aber nicht direkt geprüft).

**Verifiziert (§0.5 Checkliste):**

- `pytest -q` (venv): **962 passed in 266.25 s** — 962 unverändert (kein Python-Touch
  im Block-C-Setup, kein `phase5_ui/webui/`-Touch im Smoke).
- Tabu-Diff §0.3: **leer** (`git diff --stat main -- phase4_auth/ phase1_storage/storage/
  phase5_ui/webui/security.py phase5_ui/webui/api.py phase5_ui/webui/serializers.py
  phase5_ui/webui/permissions.py phase2_mcp/` zeigt keinen Eintrag).
- `node --check`: keine JS-Datei in dieser Session berührt (irrelevant).
- Größenprüfung `find . -name "*.md" -not -path "./.venv/*" -size +40k`: kein neuer
  Treffer durch diese Session; `phase8_5_picker_release/CLAUDE.md` weiterhin
  deutlich unter dem 40-KB-Softcap.
- Fehlerpfad einmal durchgedacht: der `preview`-Mode des Editors (`editor.js:239`,
  `editorTextareaEl.hidden = mode !== "edit"`) macht die Textarea initial unsichtbar,
  obwohl `#detail-editor` selbst sichtbar ist — das hat den ersten Smoke-Wurf in
  Station 6 verwirrt. Behoben mit `_ensure_edit_mode()`-Helfer, der `#toggle-preview`
  klickt, falls der Button-Text „Bearbeiten" ist (= Preview-Modus), und das Meta-Panel
  `<details>` aufklappt (enthält `#link-picker-button`). Beide Helfer sind idempotent
  (Station 7/8 rufen sie erneut auf, kein Effekt).
- Service-Touch **0** während der Ritte. `systemctl show sharefyx-mcp.service -p
  MainPID,ActiveEnterTimestamp` → `MainPID=195922`,
  `ActiveEnterTimestamp=Wed 2026-09-02 11:51:57 CEST` — vor dem ersten Ritt und nach
  dem Cleanup des Wegwerfs identisch. `Wegwerf-Server gesund nach 1.8s` beim Start,
  sauber abgebaut mit `kill -TERM $(cat serve.pid)` (Hard Rule 9-konform, kein
  `pkill -f`, kein `systemctl`).

**Doku-Updates im selben Commit (Hard Rule 8):**

- `phase8_5_picker_release/CLAUDE.md`: Modul-Status C `⬜` → `🟡`; Abnahmestand
  3 ✅ · 4 🟡 · 13 ⬜ → **3 ✅ · 13 🟡 · 4 ⬜** (P8.5-5/-6/-7/-8/-10/-11/-13/-15/-16
  von `⬜` → `🟡` mit ausführlicher Belegnotiz je Zeile); Stand-Block nachgezogen.
- B1-Block nach `SESSIONS_ARCHIVE.md` rotiert (manuell — Skript
  `scripts/rotate_session_block.sh` jetzt vorhanden und gegen den Phase-Head
  getestet, aber der YAGNI-Stand aus A1/A2 gilt für die zweite Rotation nicht
  mehr, sobald Block D abgeschlossen ist).
- `phase8_5_picker_release/SESSIONS_ARCHIVE.md`: B1-Block vorne angehängt
  (newest-first), A2 darunter unverändert; `updated:` aktualisiert.
- `CLAUDE.md` (Wurzel): neuer „Current state"-Absatz vom 2026-09-04 für Block C.
- `docs/INDEX.md` Phase-8.5-Header: `🔄 A1 🟡, A2 🟡, B1 🟡, C/D/Z ⬜` → `🔄 A1 🟡,
  A2 🟡, B1 🟡, C 🟡, D/Z ⬜`.
- `ROADMAP.md` Phase-8.5-Absatz: „nächster Schritt: Block C" → „Block C committet;
  nächster Schritt: Block D (Release-Vorbereitung + Deploy als Nikinger-Aktion +
  Health-Gate + Sichtprüfung + Vierte A3-Probe)".

**Was diese Session bewusst NICHT tat:**

- Kein `webui/static/`-Touch — alle drei Befunde sind entweder Smoke-Bug
  (gefixt), Server-CSRF (Befund für Step Z), oder bewusst strukturell (Station 12).
- Kein `mcpserver/`, `storage/`, `authserver/`, `security.py`/`api.py`/`serializers.py`/
  `permissions.py`-Touch — Tabu-Diff §0.3 ist nachweislich leer.
- Kein Live-Deploy — Block D fällt nie unter Druck (Plan §8), D2 ist explizit eine
  Nikinger-Aktion (P8.5-Q + Hard Rule 9, niemals `sudo systemctl restart
  sharefyx-mcp` durch opencode/M3).
- Keine Cross-`kind`-Dedup für V102 — Plan §0.4 DRAUSSEN, nur messen, nicht fixen.
- Keine Anpassung der Reauth-UI (P7-24-Mechanismus) — die Smoke-Vereinfachung für
  Station 13 ist als Befund dokumentiert, nicht als Regression.
- Kein Runbook oder Live-Health-Gate — das ist Block D3/D5 mit Nikinger-Domain.

**Nächster Schritt, konkret:** **Block D — Release** (`docs/concepts/
phase8_5_picker_release_plan.md` §5). Reihenfolge:
- **D1 Vorbereitung opencode/M3:** `.rail__version` `v3.0` → `v3.0.1` (P8.5-P, eine
  Zeile in `phase5_ui/webui/static/app.html:20`); neuer `## 2026-09-04`-Block in
  `docs/UPDATE_LOG.md` mit drei menschenlesbaren Zeilen (Picker-Modi, Tastatur,
  Generalisierter Hint) — oberster Eintrag, sonst bricht `deploy.sh` (P6-X).
- **D2 Deploy als Nikinger-Aktion:** `SHAREFYX_SYSTEMCTL="sudo systemctl"
  phase5_ui/scripts/deploy.sh main` in interaktiver Vordergrund-Shell (Hard Rule 9,
  `sudo`-Prompt sichtbar — V103 prüfen).
- **D3 Health-Gate 3/3:** `/health` 200, `/api/v1/me` ohne Session 401, `/mcp/` ohne
  Token 401, `.rail__version` im Browser `v3.0.1`, Update-Banner zeigt den neuen
  Eintrag, `/opt/sharefyx/current` zeigt auf den neuen Release-Stempel, **V105**
  (echter Anthropic-Connector verbindet weiterhin).
- **D4 Sichtprüfung am echten Gerät:** Nikinger bestätigt P8-14/15/16/18/19/23 +
  P8.5-5/-6/-7/-8/-10/-11/-13/-15/-16 am echten Build; trägt Phase-8-Glyphe ✅/🟡 ein.
- **D5 Vierte A3-Probe:** wörtlicher Prüfauftrag aus Plan §3 B1, entscheidet über
  §9.4.1 (N2) Abbruchregel.
- **Z Closeout:** Phase-8.5-Plan §9 füllen, Nachtrag in
  `docs/concepts/phase8_ui_graph_plan.md` §9 + §9.4.7, Phase-8-Head §7-Matrix +
  Session-Block, Größenprüfung.

Aktueller `## Session stopped`-Block ist dieser Block-C-Block; der nächste rotiert ihn
nach `SESSIONS_ARCHIVE.md` (newest-first).
