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
updated: 2026-09-04 (B1-Handover-Footer ergänzt — `### Session-Handover — nächste Session startet hier` am Ende des B1-Blocks, macht den Block-C-Start für die nächste Session explizit; kein Code, kein Test, kein Service-Touch; Phase-Head `updated:`-Pipe vorne verlängert, sonst unverändert) | 2026-09-04 (Wurzel-CLAUDE.md komprimiert — Phase-6-Verlaufsdokumentation + Phase-6/6.5-Vormerkungen + Funnel-Reboot-Notiz + MCP-Werkzeug-Ergonomie-Live-Feedback + End-Korrekturen P5/P4 auf Pointer-Form gestaucht; ~5 KB freigemacht; Wurzel-`updated:`-Pipe analog getrimmt; kein Code, keine Tests, kein Service-Touch; PID 195922 Active seit 2026-09-02 11:51:57 CEST nur gelesen) | 2026-09-04 (B1 committet — `_TITLE_NOT_ID_HINT` in `phase2_mcp/mcpserver/tools.py:159-164` generalisiert (Schlusssatz „Das gilt in jeder Textform — auch nicht als Tabellen-Spalte, nicht in Klammern hinter dem Titel und nicht in Aufzählungs-Zeilen." wörtlich aus Plan §3 B1), `phase2_mcp/tests/test_tools.py` um zwei Asserts (`in jeder Textform`/`Klammern`) im bestehenden `test_tool_descriptions_tell_the_agent_to_name_titles_not_ids` erweitert; neuer Phase-Head-Abschnitt `## Abbruchregel §9.4.1 (N2, verbindlich)` wörtlich aus Plan §3 B1 zwischen Modul-Status und Geerbte Contracts; Modul-Status B1 ⬜→🟡, P8.5-3 ⬜→🟡 mit Klammer-Anmerkung, Stand 3 ✅ · 3 🟡 · 14 ⬜ → 3 ✅ · 4 🟡 · 13 ⬜; pytest 962/962 unverändert (keine neue Testfunktion, nur zwei Asserts in bestehendem Test), Tabu-Diff §0.3 zeigt **genau** `phase2_mcp/mcpserver/tools.py +5/-2` und `phase2_mcp/tests/test_tools.py +2` (Plan: „genau die erlaubte Zeile + Test-Datei"), A2-Block nach `SESSIONS_ARCHIVE.md` rotiert (manuell, wie bisher); PID 195922 Active seit 2026-09-02 11:51:57 CEST nur gelesen, kein Service-Touch; nächster Schritt Block C) | 2026-09-04 (A2 committet — `dialogs.js` Module-Vars `linkPickerItems`/`linkPickerCursor` + `_renderLinkPickerResults` mit State-Reset ganz oben + `_setLinkPickerCursor`/`_pickLinkPickerAt` neu + `closeLinkPicker()`-Reset-Reihenfolge + `keydown`-Handler am Suchfeld (ArrowDown/ArrowUp/Enter, kein Wrap, kein Home/End, kein Raten); `app.css` zwei identische Auswahl-Blöcke zu einem zusammengezogen, totes `:focus` raus; zwei neue statische Tests in `test_static_routes.py` (`test_link_picker_css_has_one_selection_block` P8.5-14, `test_link_picker_picks_run_through_a_single_helper` P8.5-12) plus `test_insertAtCursor_defined_exactly_once_at_module_level` für P8.5-9; Modul-Status A2 ⬜→🟡, fünf Abnahmezeilen P8.5-9/-10/-11/-12/-14 angepasst, Stand 3 ✅ · 0 🟡 · 17 ⬜ → 3 ✅ · 3 🟡 · 14 ⬜; pytest 959→962 (+3, +0.8 KB), ui_budget 5/5 (127.6→128.7 KB, dialogs.js 11.7→12.6 KB), Tabu-Diff §0.3 leer, `node --check` grün auf dialogs.js, A1-Block nach SESSIONS_ARCHIVE.md rotiert (manuell, weil `scripts/`-Verzeichnis für `rotate_session_block.sh` aus Phase 7 noch leer ist — YAGNI für eine zweite manuelle Rotation, Plan-§0.5-Skript-Eintrag verschoben auf Block-C-Beginn mit dem Wegwerf-Setup), PID 195922 Active seit 2026-09-02 11:51:57 CEST nur gelesen, kein Service-Touch; nächster Schritt B1) | 2026-09-04 (Drift nachgezogen — Wurzel-`Current state` mit neuem 2026-09-04-Absatz ergänzt (A1-Eintrag + Drift-Hinweis + Folge-Commit-Vermerk für INDEX-Bullet-Lücke), `docs/INDEX.md` Phase-8.5-Header „⬜ geplant, nicht gestartet" → „🔄 A1 🟡, A2/B1/C/D/Z ⬜", `ROADMAP.md` Phase-8.5-Plan-Absatz „nächster Schritt: A1" → „A1 committet, Drift nachgezogen, nächster Schritt: A2"; INDEX-Bullets für `phase8_5_picker_release/CLAUDE.md` + `SESSIONS_ARCHIVE.md` bewusst NICHT in diesem Commit ergänzt — INDEX steht bei 40917 B, 43 B unter dem 40-KB-Softcap, zwei neue Bullets würden den Cap reißen; Vorschlag: Aufnahme mit gleichzeitiger Trimmung der `updated:`-Pipe in einem späteren Commit, vor A2 nicht nötig; kein Code, kein Service-Touch, pytest/ui_budget unverändert) | 2026-09-04 (A1 committet — `<select id="link-picker-mode">` in app.html:270-280, `dialogs.js` `_linkPickerMode`/`_restoreLinkPickerMode`/neue `onPick({id, title, mode})`-Signatur/change→localStorage, `editor.js` `insertAtCursor` auf Modulebene + `_linkTextFor`/`_appendLinkMarkdown`/`_onLinkPicked`, wiring auf `_onLinkPicked`; Modul-Status A1 ⬜→🟡, Tests ⬜; pytest unverändert 959/959, Tabu-Diff §0.3 leer, ui_budget 5/5 +1.8 KB, node --check grün auf dialogs.js/editor.js/app.js, Service-Touch 0 PID 195922 — V99-Korrektur im Block: erste localStorage-Nutzung des Projekts, sessionStorage→localStorage Eskalation wegen P8.5-G „überlebt Tab-Schließen", `try`/`catch` deckt SecurityError im privaten Modus ab) | 2026-09-03 (Step 0 abgeschlossen — Skelett phase8_5_picker_release/{CLAUDE.md, SESSIONS_ARCHIVE.md, scripts/} angelegt, vier Funde aus Plan §1 abgearbeitet: docs/INDEX.md 52.911 → 40.917 B (-23 %, 43 B unter 40 KB-Softcap) durch Kürzung updated: auf 5 neueste Einträge + Schlusszeile + kompakte Ausnahmenliste (Fund 2) im Wartungsblock, "Büroklammer" → "Lupe" an phase8_ui_graph/CLAUDE.md:440 mit datierter Korrekturnotiz, Phase-8-Bilanz 15/10/0 → 14/12/0 maschinell korrigiert + awk-Kommando im Bilanz-Abschnitt verankert (real 14/12/0 verifiziert); ROADMAP-Absatz + Wurzel-CLAUDE.md down: phase8_ui_graph → phase8_5_picker_release + Current-state-Absatz + updated:-Verlängerung im selben Commit; pytest unverändert 959/959 (kein Python-Touch), Tabu-Diff §0.3 leer, Service-Touch 0 (PID 195922, Active seit 2026-09-02 11:51:57 CEST — nur gelesen); eine Plan-Korrektur: Fund 1 + Fund 2 zusammen erforderten den Ausnahmenblock kompakter als anfangs geschrieben, um den Cap zu halten — kein Plan-Wortlaut gebrochen, im Session-Block dokumentiert)
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
| 5 | C — v3-Vorabritt (Wegwerf-Setup + 13-Stationen-Playwright-Smoke, jeder Fund in dieser Phase behoben oder als benannter Befund vorgelegt) | C | ⬜ | ⬜ |
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
| P8.5-5 | Picker-Dialog trägt `<select class="input" id="link-picker-mode">` mit beiden Werten; Konvention v3 eingehalten | C | ⬜ (Code committet; statischer Test für Block-C-Vorbereitung oder Folge-Session) |
| P8.5-6 | Modus „Text-Link": Klick fügt `[<Titel>](#item/itm_…)` an der Cursorposition ein; Titel mit `[`/`]` bricht den Link nicht | W | ⬜ (Code committet; Browser-Nachweis Block C Station 6) |
| P8.5-7 | Modus „Kante": Klick hängt die ID an `#field-links`, Textarea unverändert | W | ⬜ (Code committet; Browser-Nachweis Block C Station 8) |
| P8.5-8 | Moduswahl überlebt Schließen + Öffnen des Dialogs (`localStorage`); privater Modus wirft nicht | W | ⬜ (Code committet; Browser-Nachweis Block C Station 8, inkl. privater Modus) |
| P8.5-9 | `insertAtCursor` existiert **genau einmal**, auf Modulebene; alle Alt-Aufrufe in `init()` funktionieren unverändert | C | 🟡 (A2: `test_insertAtCursor_defined_exactly_once_at_module_level`; Bild-Knopf-Aufruf Z. 669 außerhalb von `init()` beweist die Modul-Ebene implizit — function-Deklaration wird vom JS-Hoisting an alle Modul-Stellen sichtbar) |
| P8.5-10 | `ArrowDown`/`ArrowUp` setzen `aria-selected` + `aria-activedescendant`; `Enter` wählt; Cursor klemmt an beiden Enden | W | 🟡 (A2: Code committet; Browser-Nachweis Block C Station 7) |
| P8.5-11 | Neu-Tippen setzt den Cursor zurück; der „Keine Treffer."-Eintrag ist nie auswählbar | W | 🟡 (A2: Code committet — State-Reset ganz oben in `_renderLinkPickerResults` räumt `linkPickerItems`+`linkPickerCursor`+`aria-activedescendant`; "Keine Treffer." bleibt außerhalb von `linkPickerItems` und damit unerreichbar für `_pickLinkPickerAt`; Browser-Nachweis Block C Station 7) |
| P8.5-12 | Tastatur- und Maus-Pfad laufen beide durch `_pickLinkPickerAt`; `app.js` unverändert | C | 🟡 (A2: `test_link_picker_picks_run_through_a_single_helper` — Funktion genau einmal definiert, ≥3 Vorkommen, `app.js` enthält weder `openLinkPicker` noch `_pickLinkPickerAt`) |
| P8.5-13 | V101 in Chromium **und** Firefox beantwortet | W | ⬜ |
| P8.5-14 | `app.css` hat genau einen Auswahl-Block für den Picker, kein totes `:focus` | C | 🟡 (A2: `test_link_picker_css_has_one_selection_block` — genau ein Vorkommen von `li[aria-selected="true"]`, kein `.link-picker-results li:focus`) |
| P8.5-15 | v3-Vorabritt: alle 13 Stationen grün gegen die Wegwerf-Instanz; jeder Fund entweder behoben oder als benannter Befund vorgelegt | W | ⬜ |
| P8.5-16 | P8-16 empirisch belegt (`prefers-reduced-transparency` + `backdrop-filter` aus, Auswahl erkennbar) | W | ⬜ |
| P8.5-17 | Deploy gelaufen, Health-Gate 3/3, Badge `v3.0.1` live, Update-Banner zeigt den neuen Eintrag, Connector verbindet (V105) | L | ⬜ |
| P8.5-18 | Sichtprüfung am echten Gerät durchgeführt; Phase-8-Glyphe ✅/🟡 vom Nikinger eingetragen; P8-14/15/16/18/19/23 aufgelöst | L | ⬜ |
| P8.5-19 | **Bauform des Umschalters bestätigt:** der Nikinger nimmt die `<select>`-Fassung ab **oder** ordnet die Radiogruppe aus seiner N3-Vorschau an | L | ⬜ |
| P8.5-20 | Das Zählkommando aus §1.5 steht im Phase-8-Head, und die dortige Bilanz-Zeile verweist darauf statt eine gepflegte Zahl zu tragen | C | ✅ (Step 0.4: awk-Kommando im Phase-8-Head Bilanz-Abschnitt) |

**Stand:** 3 ✅ · 4 🟡 · 13 ⬜ von 20 (P8.5-1, P8.5-2, P8.5-20 aus Step 0 — nur Doku-Arbeit; P8.5-9,
P8.5-12, P8.5-14 aus A2 — statische Tests, Browser-Nachweis für P8.5-10/-11/-13 mit Block C;
P8.5-3 aus B1 — Code/Tests grün, Live-Verifikation mit Block D5; Rest wartet auf C/D).

## Session stopped

### 2026-09-04 (B1 — `_TITLE_NOT_ID_HINT` generalisierend geschärft, Code committet)

**Auftrag:** B1 nach `docs/concepts/phase8_5_picker_release_plan.md` §3 B1. Einzige
erlaubte Tabu-Ausnahme in `mcpserver/` (P8.5-D, Präzedenz P7-T und P8-§0.4). Hint
generalisierend schärfen (Option a, N2), zwei neue Asserts in `test_tools.py`,
Abbruchregel wörtlich im Phase-Head.

**Ergebnis — alle drei Eingriffsgruppen aus Plan §3 B1 committet, §0.5 Checkliste grün:**

1. **`phase2_mcp/mcpserver/tools.py` Z. 159–164.** `_TITLE_NOT_ID_HINT` generalisiert.
   Der alte Schwanz `; auch nicht als Tabellen-Spalte.` ist durch einen Vier-Zeilen-
   Schlusssatz ersetzt: *„Das gilt in jeder Textform — auch nicht als Tabellen-Spalte,
   nicht in Klammern hinter dem Titel und nicht in Aufzählungs-Zeilen."* — wörtlich aus
   Plan §3 B1. Die drei Negativ-Beispiele stehen jetzt als **Illustration der Regel**,
   nicht als abschließende Liste; der Satz „Das gilt in jeder Textform" ist die
   eigentliche Änderung, der Rest ist Konkretisierung. Wörtlich identisch an den vier
   Verwendungsstellen (`search_items`/`get_item`/`get_item_meta`/`create_item`) — die
   `update_item`/`append_to_item`/`patch_item`-Beschreibungen tragen den Hint bewusst
   nicht (reine Schreibwerkzeuge, Vorlage aus Phase 7; siehe auch „Fehlerpfad" unten).

2. **`phase2_mcp/tests/test_tools.py` Z. 137–143.** `test_tool_descriptions_tell_the_
   agent_to_name_titles_not_ids` um zwei Asserts erweitert:
   - `assert "in jeder Textform" in tools._TITLE_NOT_ID_HINT`
   - `assert "Klammern" in tools._TITLE_NOT_ID_HINT`
   Bestehende Asserts (`"Einkaufsliste Winter"`, `"itm_a1b2c3d4"`, `"Tabellen-Spalte"`,
   plus Hint-in-Beschreibung für `search_items`/`get_item`/`get_item_meta`/
   `create_item`) bleiben unverändert gültig — keine Anpassung am Testaufbau, nur zwei
   zusätzliche Zeilen.

3. **`phase8_5_picker_release/CLAUDE.md`.** Neuer Abschnitt `## Abbruchregel §9.4.1
   (N2, verbindlich)` zwischen Modul-Status und Geerbte Contracts, wörtlich aus Plan
   §3 B1: *„Taucht die `itm_…`-ID in einer **vierten** Oberflächenform auf (Fließtext +
   Tabelle waren die ersten zwei, der Klammer-/Aufzählungs-Kontext aus Phase 8 §9.4.1
   die dritte), wird §9.4.1 als **Modellverhalten dokumentiert und geschlossen**
   (Option c). Kein fünfter Hint-Edit, keine Schema-Änderung an `search_items`. Der
   Punkt verschwindet dann aus dem Ledger, statt weiter vererbt zu werden. — Geprüft
   wird das in Block D5 (vierte A3-Probe nach dem Deploy, wörtlicher Prüfauftrag im
   Plan §3 B1)."* — Pflichtbestandteil der Abnahmezeile P8.5-3.

**Begleitende Doku-Updates im selben Commit (Hard Rule 8):**

- `phase8_5_picker_release/CLAUDE.md`: Modul-Status B1 `⬜` → `🟡`; P8.5-3 `⬜` → `🟡`
  mit Klammer-Anmerkung für den Code-Beleg; Stand-Zeile 3 ✅ · 3 🟡 · 14 ⬜ →
  3 ✅ · 4 🟡 · 13 ⬜.
- A2-Block nach `SESSIONS_ARCHIVE.md` rotiert (manuell, wie in A1/A2 — Skript
  `scripts/rotate_session_block.sh` aus Phase 7 noch nicht für `phase8_5_picker_release/`
  portiert; YAGNI bis Block-C-Beginn).
- `phase8_5_picker_release/SESSIONS_ARCHIVE.md`: A2-Block vorne angehängt
  (newest-first), A1 darunter unverändert; `updated:` aktualisiert.
- `CLAUDE.md` (Wurzel): neuer „Current state"-Absatz vom 2026-09-04 für B1.
- `docs/INDEX.md` Phase-8.5-Header: `🔄 A1 🟡, A2 🟡, B1/C/D/Z ⬜` → `🔄 A1 🟡, A2
  🟡, B1 🟡, C/D/Z ⬜`.
- `ROADMAP.md` Phase-8.5-Absatz: „nächster Schritt: B1" → „B1 committet; nächster
  Schritt: Block C (Wegwerf-Setup + 13-Stationen-Playwright-Smoke)".

**Verifiziert (§0.5 Checkliste):**

- `pytest -q` (venv): **962 passed in 256.65 s** — 962 unverändert (keine neue
  Testfunktion, nur zwei Asserts im bestehenden
  `test_tool_descriptions_tell_the_agent_to_name_titles_not_ids`); keine Regressionen.
- Tabu-Diff aus §0.3 zeigt **genau** die erlaubten zwei Dateien:
  `git diff --stat main -- phase4_auth/ phase1_storage/storage/ phase5_ui/webui/security.py
  phase5_ui/webui/api.py phase5_ui/webui/serializers.py phase5_ui/webui/permissions.py
  phase2_mcp/` →
  ```
  phase2_mcp/mcpserver/tools.py  | 5 +++--
  phase2_mcp/tests/test_tools.py | 2 ++
  ```
  Plan §3 B1 „Tabu: … Der Diff auf `phase2_mcp/` darf **genau** diese eine Datei plus
  die Testdatei zeigen." — exakt erfüllt.
- `node --check`: keine JS-Datei berührt (irrelevant für diese Session).
- Größenprüfung `find . -name "*.md" -not -path "./.venv/*" -size +40k`: **kein**
  neuer Treffer durch diese Session; `phase8_5_picker_release/CLAUDE.md` jetzt ~27 KB
  (vorher ~27 KB), weiterhin deutlich unter dem Cap — kein Rotationsschritt nötig.
- Fehlerpfad einmal durchgedacht: bestehender Test prüft den Hint an den vier
  Verwendungsstellen, an denen er tatsächlich eingebettet ist. Die Generalisierung
  ist **additiv** (kein bestehender Fall wird gebrochen, nur neue Fälle werden
  abgedeckt) — wer vorher schon „Tabellen-Spalte" las, sieht jetzt zusätzlich
  „Klammern" und „Aufzählungs-Zeilen". Wenn der Generalisierungs-Satz später einmal
  entfernt werden müsste (Pflege, niemand weiß), würde der bestehende Assert
  `"Tabellen-Spalte" in tools._TITLE_NOT_ID_HINT` zuerst feuern — das ist das
  gewollte Sicherheitsnetz. Ein viertes `_TITLE_NOT_ID_HINT`-Vorkommen (etwa in einem
  fünften Tool) fällt durch den `assert tools._TITLE_NOT_ID_HINT in
  _description_of(described_mcp, name)`-Loop nicht auf — der Test ist absichtlich
  nicht „viermal vorkommend", sondern „in diesen vier Beschreibungen vorhanden".
- Service-Touch **0**. `systemctl status sharefyx-mcp` zeigt **PID 195922**, Active seit
  `Wed 2026-09-02 11:51:57 CEST` (3 days zum Sitzungsbeginn) — nichts angefasst, nur
  gelesen. **PID + ActiveEnterTimestamp im Session-Block notiert, wie §0.5.7 verlangt.**

**Was diese Session bewusst NICHT tat:**

- Browser-/Live-Verifikation für P8.5-4 (vierte A3-Probe) — kommt mit Block D5 nach
  dem Deploy.
- `test_mcp_smoke.py`-Anpassung an den neuen Hint-Text — der Smoke ist eine Live-
  Probe, die keinen Description-Text liest (nur Tool-Aufrufe gegen den Server); keine
  Anpassung nötig, keine Lücke im Smoke.
- Block C (Wegwerf-Setup + 13-Stationen-Playwright-Smoke) — nächster Schritt nach
  diesem Commit; Plan §4.
- `mcpserver/tools.py` sonst anfassen — die Tabu-Ausnahme gilt **ausschließlich** für
  den Hint-Text. `WRITE_TOOL_DIVISION`, `_LIST_SPACES_POINTER`, alle
  Beschreibungs-Strings anderer Tools bleiben unangetastet (gegengeprüft mit
  `git diff` auf der Datei).
- `mcp_smoke.py`-Beschreibungen — der Hint erscheint nur in Tool-Beschreibungen, der
  Smoke spricht die Tools über Funktionsaufrufe an.

**Nächster Schritt, konkret:** **Block C — v3-Vorabritt gegen eine Wegwerf-Instanz**
(`docs/concepts/phase8_5_picker_release_plan.md` §4). Erst Wegwerf-Setup
(`scripts/serve.py` mit tmp `DATA_ROOT`/tmp `auth.sqlite3`/eigenem Port, inkl. der seit
Step 0 angekündigten Portierung von `scripts/rotate_session_block.sh` aus Phase 7 für
`phase8_5_picker_release/`), dann 13 Stationen Playwright-Smoke; jeder Fund entweder
behoben oder als benannter Befund vorgelegt. Plan §4 listet die 13 Stationen.

---

### Session-Handover — nächste Session startet hier

Session endet mit **B1 committet** (`5fee41e`, 2026-09-04) — `pytest` 962/962 grün, Tabu-Diff
zeigt genau `phase2_mcp/mcpserver/tools.py +5/-2` und `phase2_mcp/tests/test_tools.py +2`,
kein Service-Touch (PID 195922 nur gelesen). **Weitermachen mit Block C** — v3-Vorabritt
gegen eine Wegwerf-Instanz (Plan §4). Reihenfolge: (1) Wegwerf-Setup (eigener Port,
`tmp_path` für `DATA_ROOT` + `auth.sqlite3`; **Skript `scripts/rotate_session_block.sh` aus
Phase 7 nach `phase8_5_picker_release/scripts/` portieren**, YAGNI-Vermerk aus A1/A2
schließen) → (2) 13 Stationen Playwright-Smoke aus Plan §4.3 (jede Station mit Klartext-
Ergebnis, jeder Fund entweder behoben oder als benannter Befund vorgelegt) → (3) Block D
(Release als **Nikinger-Aktion**, P8.5-Q + Hard Rule 9; niemals `systemctl restart
sharefyx-mcp` durch opencode/M3) → (4) D5 Vierte A3-Probe, an der die Abbruchregel §9.4.1
(N2) fällt oder hält → (5) Step Z (Closeout). Aktueller `## Session stopped`-Block ist
dieser B1-Block; der nächste rotiert B1 nach `SESSIONS_ARCHIVE.md` (newest-first).
