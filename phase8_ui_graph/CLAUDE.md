---
status: live
purpose: Phase-Head UI-Neuanstrich v3, Verknüpfungs-Graph, drei P7-Erbposten — Scope, harte Regeln, Modulstatus, aktueller Session-Handover
read-when: Arbeiten in phase8_ui_graph/ oder an den in §0.4 des Plans genannten Dateien in storage/mcpserver/webui/scripts — zuerst lesen, zusammen mit dem neuesten Session-stopped-Block
detail: L2
up: ../CLAUDE.md
down:
  - ../docs/concepts/phase8_ui_graph_plan.md       # voller Plan, Entscheidungen P8-A–P8-Q, §0.1 gelockte N1–N12, Steps 0/A/B/C/D/Z
  - ../docs/concepts/PHASE7_CLOSEOUT_HANDOVER.md   # Herkunft der drei Erbposten (P7-24/remove-space/P7-4)
  - SESSIONS_ARCHIVE.md                             # ältere Session-Blöcke, newest-first
updated: 2026-09-02 (Selection/Choice Konvention v3 im Phase-Head dokumentiert + Auswahl-Chevron-Vorbild in app.css ::select.input gebaut -- Lucide m6 9 6 6 6-6 als data-URL, --text-faint-Stroke, 12x12 rechtsbuendig, padding-right 28px, :disabled-Variante in --text-placeholder; alle 7+1 <select class="input">-Stellen gerendert (field-status, create-type, new-folder-parent-select, move-space-select, move-folder-select, space-member-write-select, Per-Item-Share-Row dynamisch); Playwright-Smoke 9/9 gruen gegen Wegwerf 18771; ui_budget 5/5 (123.3/250 KB, +0.6 KB), 958/958 pytest, Tabu-Diff §0.4 leer, JS-Syntax OK; phase8_ui_graph/scripts/{wegwerf_setup_auswahl_chevron.py,auswahl_chevron_playwright_smoke.py} neu; docs/screenshots/auswahl_chevron_{01_move,02_share}_dialog.png neu; kein Service-Touch, kein Deploy, kein Push; Vormerkung 1 vom 2026-09-01 (Auswahl-Boxen vereinheitlichen) damit erledigt -- die Selection/Choice-Konvention ersetzt die offene Frage, das Chevron-Vorbild schliesst die sichtbare Luecke im Vorbild; Vormerkung 2 vom 2026-09-02 (Listenzeilen-Sheen vs Rail-Button-Stil) bewusst NICHT aufgeloest -- der C4-Sheen bleibt unvera (ge 3px-Akzentkante + Outline + Backdrop-Blur) wegen N8 (Auswahl darf nicht allein von Transparenz abhaengen); Obsidian-Uebersicht (D2) bleibt WIP wie vom Nikinger bestaetigt -- keine Code-Aenderung an js/graph.js, app.css/app.html fuer das Graph-Panel) | 2026-09-02 (Vormerkung-Block ergaenzt: Nikinger-Feedback nach Sichtpruefung 3 -- Listenzeilen-Auswahl (c4c5_03) sieht anders aus als Rail-Button-Vorbild (03_list.png), drei Loesungsrichtungen fuer die naechste kontrollierte UI-Session vereinheitlichen / vereinfachen / bewusst unterschiedlich lassen; Obsidian-Uebersicht weiterhin WIP, explizit bestaetigt; kein Code angefasst, kein Push noetig) | 2026-09-02 (Block C C4+C5 gebaut: Liquid-Glas-Akzente (P8-H/N8, --glass-{bg,border,blur,highlight}-Tokens + .glass-Utility mit Fallback+@supports+prefers-reduced-transparency), .list__head sticky (position:sticky;top:0;z-index:1) + .overlay__panel/.update-banner/.toast ueber gruppierte Selektor-Liste am Dateiende auf Glas, Auswahl-Sheen fuer .list__row[aria-current=true] und .list__row--selected (3px solide Akzentkante + 1px Outline + backdrop-blur Sheen); C5: ::selection (Akzent-quiet/Text), .editor__textarea max-width:72ch + margin:0 auto (576px computed in Plex Mono, symmetrische Margins), .editor__body padding-left auf calc(var(--space)*1.5) Token; phase8_ui_graph/scripts/{wegwerf_setup_c4c5.py,c4c5_playwright_smoke.py} neu (Port 18770, Standing-Permission-Muster D1/D2 reproduziert, File-Keyring, 7 Items ueber zwei Spaces); Playwright-Smoke 7/7 gruen (CSS-Static + sticky head + 3px border + outline + 72ch centered + ::selection rule + overlay glass rgba(27,32,39,0.55)); vier Screenshots docs/screenshots/c4c5_{01..04}_*.png; 958/958 pytest, ui_budget 5/5 gruen (122.7/250 KB, +2.9 KB), Tabu-Diff §0.4 leer, JS-Syntax node --check auf app/list/state/tree.js OK; kein Code ausserhalb webui/static + phase8_ui_graph/scripts beruehrt; Produktion unangetastet, kein Deploy, kein Service-Touch) | 2026-09-02 (Block D D3 gebaut: Versions-Bump .rail__version v2.2.3 -> v3.0, neuer docs/UPDATE_LOG.md-Eintrag 2026-09-02 mit vier Bullet-Points (Uebersicht tabellos, Verknuepfungs-Graph, globaler Home-Scope, Mini-Legende); Sichtpruefung 2 mit 26 Items ueber drei Spaces via phase8_ui_graph/scripts/{wegwerf_setup_sichtpruefung2.py,sichtpruefung2_smoke.py} (Standing-Permission-Muster reproduziert, Port 18769, File-Keyring, User alpha + drei Spaces alpha/beta/gamma via Store.create mit folder-Support statt space_cli); sechs Screenshots docs/screenshots/sp2_{01..06}_*.png; README.md Sneak-Peak-Sektion komplett ersetzt (neun Block-C-Screenshots raus, sechs Block-D-Screenshots rein, 3x2-Tabelle, Hinweis-Text ueber die historische Referenz); D2-Block rotiert; Head jetzt mit D3-Block allein ueber 40KB-Softcap benannt; 958/958 pytest, ui_budget 5/5 gruen (119.8/250 KB unveraendert), Tabu-Diff §0.4 leer; kein Service-Touch, PID 67925 uptime 66891s linear wachsend) | 2026-09-02 (Block D D2 gebaut: handgerollter Canvas-Force-Graph in js/graph.js (542 Zeilen, 6.2 KB gzipped), Force-Simulation mit O(n^2)-Repulsion + Federkraft + Alpha-Decay, Canvas 2D mit devicePixelRatio-Korrektur, Knotenfaerbung via spaceCategory() aus C3, Kantenstile explizit solide / Tag gestrichelt / Ordner gepunktet, Hover-Dim, Klick -> Editor.selectItem, Drag/Zoom/Pan, prefers-reduced-motion synchron 300 Ticks; Toggles Tags/Ordner mit Default aus, >15-Knoten-Cutoff-Riegel fuer Tag-Cliquen; app.html-Graph-Panel erweitert (Toolbar + Empty-Hint), app.css fuer Toolbar + Empty-Hint, app.js initGraph() in Init-Kette + loadGraphPanel() an drei Stellen (Init/Home/Refresh); phase8_ui_graph/scripts/{wegwerf_setup_d2.py,d2_playwright_smoke.py} neu -- Standing-Permission-Muster C3/D1 reproduziert, eigener Port 18768, File-Keyring-Backend, 14 Items (10 alpha + 4 beta) mit 6 expliziten Kanten (4 Frontmatter + 2 Body); Playwright-Smoke 7/7 gruen -- statisches Markup korrekt, Login + Overview rendert Graph-Panel, /api/v1/graph liefert 14 Knoten/6 Kanten, Empty-Hint versteckt wenn Kanten existieren, Tag-Toggle erweitert sichtbar, Zoom-Readout aktiv, Canvas mit >=500 nicht-transparenten Pixeln; zwei Screenshots docs/screenshots/d2_{01_overview_with_graph,02_graph_with_tag_toggle}.png; D1-Block rotiert; Head jetzt mit D2-Block allein ueber Softcap benannt (Rotation wuerde nichts bewegen); 958/958 pytest (vorher/nachher identisch, keine Python-Aenderung), ui_budget 5/5 gruen (119.8/250 KB, +6.8 KB), Tabu-Diff §0.4 leer (Storage nicht beruehrt, achte Oeffnung bleibt ANGEKUENDIGT), JS-Syntax node --check auf graph.js/app.js OK; kein Code ausserhalb webui/static + phase8_ui_graph/scripts beruehrt; Produktion unangetastet, PID 67925 uptime 66363s linear wachsend) | 2026-09-02 (Block D D1 gebaut: Uebersicht tabellos, app.html/app.css/list.js/app.js aktualisiert, Playwright-verifiziert gegen Wegwerf 18767, 5/5 gruen, drei Screenshots d1_{01..03}, 958/958 pytest, ui_budget 5/5 (113.0/250 KB), Tabu-Diff §0.4 leer, Head 41.8KB->44.4KB ueber Softcap benannt, C3-Block rotiert, kein Service-Touch, PID 67925 uptime 65157s linear wachsend) | 2026-09-01 (Vormerkung in phase8_ui_graph/CLAUDE.md ergaenzt: Auswahl-Boxen vereinheitlichen -- Space-Auswahlbox (Move-Dialog, <select class=input id=move-space-select>) als Standard; Nikinger-Sichtpruefung-1-Design-Frage mit 'nein, C3-C5 + D-Block noch offen' beantwortet; kein Code, kein Service-Touch; Head 33.6KB->37.5KB noch unter Softcap) | 2026-09-01 (Block C C2 gebaut: Lucide-Sprite-Vendoring (18 Icons, ISC+MIT-Lizenzen, phase5_ui/vendor/lucide/); Generator build_icon_sprite.py (idempotent, --check); Sprite-Block zwischen ICONS:BEGIN/ICONS:END in app.html (vom Generator gepflegt); js/icons.js (iconSvg()/iconHtml(), 13. JS-Modul); app.css .icon (Lucide-Defaults: 1.25em/currentColor/stroke-width 2) + .rail__glyph.icon (16px Badge-Box) + .toolbar-btn.icon (1em) + .tree__twist (12px SVG-Box); Ersetzungs-Map 7 HTML-Entities + 3 Text-Glyphen geschlossen (F9/F10/F11 aus C0); V92 gepinnt (Lucide 1.38.0, SHA-256 d28944cf…); ui_budget 5/5 (110.3/250 KB), pytest 958/958, Tabu-Diff leer, grep &#[0-9]+; in app.html → 0 Icon-Treffer, grep '→|⇄|×' in js/ → 0 Icon-Treffer (2 Treffer bleiben = Sprach-Interpunktion 'v3 → v4' mit Audit-Kommentar); Modul-Status Block C auf 'C0+C1+C2 gebaut, C3-C5 offen' + Abnahmestand um C2-Zeile ergaenzt + neuer Session-Block + C1-Block rotiert; Head 33KB->38KB, immer noch unter Softcap; kein Code ausserhalb webui/static + build_icon_sprite.py beruehrt) | 2026-09-01 (Block C C1 gebaut: C1a Font-Swap (Plex Sans Var v0.2.0 + Plex Mono v2.5.0, SHAs gepinnt, build_font_subset_plex.sh neu) + C1b CSS-Typografie (5 Skala-Tokens, body 16px/1.55, h1-h3 + Meta-Zeilen auf Tokens, IDs/Versions in --font-mono); zwei Commits (0281cce + 08bff55); ui_budget 5/5 (108.4/250 KB), pytest 958/958 (250s, Flake als isoliert bestaetigt), Tabu-Diff leer; phase8_ui_graph/CLAUDE.md Modul-Status Block C auf 'C0 + C1 gebaut, C2-C5 offen' gehoben + Abnahmestand um C1-Zeile ergaenzt + neuer Session-Block; Head 27.5KB->33KB, immer noch unter Softcap) | 2026-09-01 (Block C C0 gebaut: Anti-AI-Pattern-Research (V94 bestaetigt, Web-Recherche) + UI-Audit gegen den Code (P8-25); Findings-Tabelle Muster -> Fundstelle -> Fix -> Ziel-Step im Phase-Head, 35 Eintraege, davon 0 als eskaliert markiert; Code unberuehrt, vier Dateien Doku-only -- phase8_ui_graph/CLAUDE.md + SESSIONS_ARCHIVE.md + docs/INDEX.md + SESSIONS_ARCHIVE-Frontmatter; Head 18.4KB->27.5KB, immer noch unter Softcap) | 2026-09-01 (Gate B→C: 958/958 pytest gruen, Charakterisierung byte-identisch, Tabu-Diff leer, _graph_get manuell 12/12, Playwright gegen Wegwerf 18/18; B4-Block rotiert, Head 14.8KB unter Softcap; Code unberuehrt, Doku-Update + neuer Session-Block) | 2026-09-01 (Block B Step B1 gebaut -- storage/linkscan.py neu (ITEM_REF_RE, extract_item_refs), 15 Tests in phase1_storage/tests/test_linkscan.py, achte P1-Contract-Oeffnung in phase1_storage/CLAUDE.md angekuendigt vor Code, Tabu-Diff §0.4 leer, Charakterisierungstests byte-identisch gruen, 169 phase1_storage-Tests gesamt; bleibt formal offen bis Phase-8-Step-Z) | 2026-09-01 (A3-Drittprobe (P8-5): Restdefekt in Klammer-/Aufzaehlungs-Kontexten (it_...-ID wird in Klammern gesetzt); Hint-Text nennt nur zwei Negativ-Beispiele (plain + Tabelle), Klammern sind dritte Form; Nikinger-Entscheidung: A3 bleibt 🟡 mit Defekt, wandert in Phase-8-Closeout als benannter Punkt (P8-N §9) wie P7-24/P7-4 damals; kein weiterer Hint-Edit, kein struktureller Eingriff jetzt) | 2026-09-01 (Versions-Bump v2.2 -> v2.2.3 in app.html .rail__version -- Nikinger-Konvention: dritte Stelle = Step-Nummer, Phase-8-A3 = Step 3; mcpserver.__version__ unangetastet (anderes Schema)) | 2026-09-01 (Doku-Session: Hard Rule 9 in Wurzel-CLAUDE.md ergaenzt nach Phase-8-A3-Vorfall -- kein pkill -f mit Regex, niemals den systemd-Dienst anfassen; PROMPTS.md Hard-Rules-Liste und Tests-Absatz um Stopp-Regel fuer Wegwerf-Instanzen erweitert; docs/INDEX.md drei Zeilen vorne + drei Eintraege angepasst; kein Code, kein Service-Touch, Produktion weiterhin active, head 11.6KB->12.8KB unter Softcap) | 2026-09-01 (A3 gebaut -- _TITLE_NOT_ID_HINT mit Positiv/Negativ-Beispiel geschärft, Test test_tool_descriptions_tell_the_agent_to_name_titles_not_ids auf neuen Wortlaut angepasst, 143 phase2_mcp-Tests gruen, Zweitprobe vom Nikinger live bestaetigt (positiv), dritte Probe nach Deploy offen P8-5) | 2026-08-31 (A2 live-verifiziert -- Test_Space_A2 angelegt + entfernt, 4x GET /api/v1/overview nach DELETE=200 statt 500, Index konsistent mit Dateien, Push danach freigegeben; Block A vollstaendig live ✅) | 2026-08-31 (Nachtrag: Janick live angemeldet -- dritter biologischer Nutzer, Phase-4-Auth-Architektur erstmals mit externem Dritt-Anwender durchgespielt; Connector-UI-Befund: 'Anmeldung fehlgeschlagen' trotz erfolgreicher OAuth-Verbindung, kein Handlingsbedarf, Vormerkung fuer spaeter) | 2026-08-31 (Nachtrag: OpenAI-ChatGPT-Konnektor aktuell nicht kompatibel, benoetigte Settings unbekannt -- Auth-Architektur auf Anthropic-Konnektoren geeicht, andere Settings nicht hinterlegt, Vormerkung ohne Auftrag) | 2026-08-31 (Block A: A2 remove-space-Auto-Reindex gebaut -- spacectl._cmd_remove_space nach remove_space_dir mit store.rebuild_index(), Test beweist keine Karteileichen + keine Kollateralschäden, 913 gruen, Live-Verifikation ausstehend) | 2026-08-31 (Block A: A1 Reauth-Grant Client gebaut -- async runBatchMove + Grant-Round-2, test #3 auf N=14, Browser-Smoke gegen Wegwerf bestanden, Head rotiert, Live-Verifikation ausstehend) | 2026-08-28 (Block A gestartet -- A1 Reauth-Grant Backend gebaut, 912 Tests gruen, Plan-Drift session_id->session_hash + Throttle-Vorzug dokumentiert, JS-Client ausstehend) | 2026-08-28 (Nachtrag: websearch-MCP nachgerüstet -- @zhafron/mcp-web-search, kein API-Key, Live-Probe bestanden, V94 von nein auf ja) | 2026-08-28 (Step 0 abgeschlossen -- opencode-ai 1.18.25 global installiert, Minimax-Provider-Auth vom Nikinger gesetzt, Playwright-MCP verbunden (V93), CLAUDE.md-Regeldatei-Kontrollfrage bestanden, Smoke-Test P8-26 auf Wegwerf-Branch bestanden, Harnesswechsel zu opencode/M3 ab Block A freigegeben) | 2026-08-28 (Skelett angelegt, Step 0 Fundament-Session gestartet)
---

# CLAUDE.md — Phase 8: UI-Neuanstrich v3, Verknüpfungs-Graph, QoL (`phase8_ui_graph/`)

> Kein eigenes Python-Paket (wie `phase3_edge/`, `phase6_shares/`, `phase6_5_tools_images/`,
> `phase7_spaces_admin/`) — Servercode bleibt in `storage`/`mcpserver`/`webui`/`scripts`.
> **Quelle der Wahrheit ist der Code, nicht dieses Dokument.**

---

## Mission (zuerst lesen)

Vier Blöcke, Reihenfolge 0 → A → B → Gate → C → D → Z: **A** = drei P7-Erbposten schließen
(P7-24-TOTP-Replay per Reauth-Grant, `remove-space`-Auto-Reindex, P7-4-Zweitprobe) — fällt unter
Druck **nie**. **B** = Link-Fundament, achte P1-Contract-Öffnung (`storage/linkscan.py`,
`item_links`-Tabelle, `GET /api/v1/graph`). **C** = Design-Fundament v3, De-AI-isierung (IBM
Plex, Lucide-Sprite, Farblegende own/shared/foreign, Liquid-Glass-Akzente mit Pflicht-Fallback).
**D** = Übersicht tablos + handgerollter Canvas-Force-Graph.

**Erstmals opencode/M3 als Ausführender ab Block A** (P7-Handover §7) — Step 0 (diese Sitzung)
läuft noch in Claude Code, gemeinsam mit dem Nikinger, und stellt die opencode-Fähigkeits-Parität
her. **Kein Advisor während der Ausführung (P8-L, N12)** — Ersatz: Selbstprüf-Checkliste §0.6 des
Plans + zwei Nikinger-Sichtprüfpunkte.

## Scope

- **DRIN:** die drei P7-Erbposten, Link-Extraktion + Graph-Endpunkt, Design v3
  (Typografie/Icons/Farben/Glas), Übersicht tablos + Force-Graph, `AGENTS.md`-Entfernung,
  opencode-Einrichtung.
- **DRAUSSEN:** FastMCP-4/V79 (eigene Mini-Phase), Body-Volltextsuche, Rechteverwaltung über
  MCP-Tools, neues MCP-Tool für den Graph, Löschen von Items, `_trash/`-Räumung,
  Funnel-Watchdog, Mobile/Realtime, Light-Mode. Volle Liste: Plan §0.5 „DRAUSSEN".

Details, gelockte Entscheidungen P8-A–P8-Q, Verbots-/Tabu-Liste, Schritt-Sequenz, Testliste,
Abnahmezeilen: `docs/concepts/phase8_ui_graph_plan.md`.

**P8-N — ein Dokument pro Phase:** der Closeout wird §9 des Plans, kein separates Handover.

## Modul-Status

| Block | Inhalt | Status |
|---|---|---|
| Step 0 | Fundament-Session (Haushalt, AGENTS.md weg, Skelett, opencode-Setup, Smoke-Test) | ✅ |
| A1 | Reauth-Grant (`webui/reauth.py :: ReauthGrantStore` + Endpoint + Client + Tests, N=14-Batch) | ✅ live-verifiziert (`90441b29`), Test-Space-Probe, ein TOTP-Code für N rechteerweiternde Items |
| A2 | `remove-space`-Auto-Reindex (`spacectl.py :: _cmd_remove_space()` → `store.rebuild_index()`) | ✅ live-verifiziert (`90441b29`), `Test_Space_A2` Remove → 4× `GET /api/v1/overview` 200, Index konsistent |
| A3 | P7-4: organische Zweitprobe + `_TITLE_NOT_ID_HINT` schärfen | 🟡 gebaut + deployt (`7254aa9`, 2026-09-01); Drittprobe (P8-5) **Restdefekt**: Plain-Text sauber, **Klammer-/Aufzählungs-Kontext** nennt weiterhin die `itm_…`-ID — Hint deckt zwei Negativ-Beispiele (plain + Tabelle), Klammern sind eine dritte, nicht genannte Form. **Bleibt 🟡 mit Defekt** (Nikinger-Entscheidung 2026-09-01); der Restdefekt wandert als benannter Defekt in den Phase-8-Closeout (`docs/concepts/phase8_ui_graph_plan.md` §9), wie P7-24/P7-4 damals |
| B1 | `storage/linkscan.py` neu (`ITEM_REF_RE`, `extract_item_refs(body)`) + 15 Tests | ✅ gebaut + live-verifiziert (`ed43ed6` deploy `007b73d`, 2026-09-01); achte P1-Contract-Öffnung angekündigt in `phase1_storage/CLAUDE.md` §Geerbte Contracts (Disziplin der Vorgänger-Öffnungen 3–7); Tabu-Diff leer, Charakterisierungstests byte-identisch grün, 169 phase1_storage-Tests gesamt |
| B2 | `index.py` (`INDEX_SCHEMA_VERSION = 3`, `item_links`-Tabelle + Index, `replace_item_links()`, `all_links()`, `row_from_file` ↳ `body_refs`, `rebuild_index` populiert, `delete_item` räumt src-Zeilen) + `store.py` (`_replace_links_for_item()`, `Store.links_all()`, alle 6 Schreibpfade via `_write_item_file` plus Drift-Repair) + 22 Tests | ✅ gebaut + live-verifiziert (`f4c8844` deploy `007b73d`, 2026-09-01); Tabu-Diff leer, Charakterisierungstests byte-identisch grün, 191 phase1_storage-Tests gesamt (vorher 154 + 15 B1 + 13 B2-index + 9 B2-store) |
| B3 | `webui/api.py :: _graph_get()` + Route `GET /api/v1/graph` + 8 Tests | ✅ gebaut + live-verifiziert (`58ff9a6` deploy `007b73d`, 2026-09-01); Tabu-Diff leer, Charakterisierungstests byte-identisch grün (P5-B-Disziplin gehalten: nur `mcpserver.permissions.SharePolicy` importiert in webui/) |
| B4 | UI: `#item/`-Klick-Delegation (`app.js`) + Link-Picker-Dialog (`app.html`/`app.css`/`dialogs.js`/`editor.js`) | ✅ gebaut + live-verifiziert (`ea14d53` deploy `007b73d`, 2026-09-01); Tabu-Diff leer (insb. `webui/security.py` P8-Q unangetastet); JS-Syntax-Check `node --check` auf `app.js`/`editor.js`/`dialogs.js` OK; 34 statische-Tests grün; ui_budget 5/5 grün (91/250 KB app.js+css+Font) |
| Block B abgeschlossen | `linkscan.py` + `item_links` + `Store.links_all` + `GET /api/v1/graph` + UI-Wiring | ✅ **live-verifiziert** (`007b73d`, 2026-09-01, Release `20260901T103944.634877Z`, Health-Gate 3/3, Versionsbadge v2.2.3); achte P1-Contract-Öffnung bleibt **angekündigt**, geschlossen mit Phase-8-Step-Z |
| Block C | Design-Fundament v3 (Typografie, Icons, Farben, Glas) | 🔄 C0 ✅ · C1 ✅ gebaut (C1a Font-Swap + C1b CSS-Tokens) · C2 ✅ gebaut (Lucide-Sprite, 18 Icons, build_icon_sprite.py, js/icons.js, .icon CSS) · C3 ✅ gebaut (Farbsemantik --space-own/shared/foreign + .rail__glyph--{cat}, .space-dot--{cat}, .legend) · C4 ✅ gebaut (Liquid-Glas-Akzente, .list__head sticky, Auswahl-Sheen 3px + Outline) · C5 ✅ gebaut (F5 ::selection + F21 72ch-Editor + F22 Padding-Token) · wartet auf Nikinger-Sichtprüfung 3 am echten Gerät |
| Block D | Übersicht tablos + Force-Graph | ✅ D1+D2+D3 gebaut (D1 = Übersicht tabellos + globaler Home-Scope, D2 = handgerollter Canvas-Force-Graph, D3 = Versionierung v3.0 + UPDATE_LOG + Sichtprüfung 2 + README Sneak Peak) — wartet auf Nikinger-Sichtprüfung 2 am echten Gerät + Live-Deploy |
| Step Z | Closeout | ⬜ |

## Geerbte Contracts

Achte P1-Contract-Öffnung (P8-M) wird in Block B benannt und gebaut — Eintrag folgt in
`phase1_storage/CLAUDE.md` §„Geerbte Contracts" im Öffnungs-Commit, nicht hier dupliziert.

## Abnahmestand (Plan §7, P8-1–P8-26)

**Statusregel wie in P5/P6/P6.5/P7: ✅ heißt live-verifiziert durch den Nikinger, nicht
„gebaut".** A1 ✅ + A2 ✅ live-verifiziert (`90441b29`, 2026-08-31, Nikinger-Probe Test_Space +
Test_Space_A2). A3 gebaut (2026-09-01), dritte Probe nach Deploy offen (P8-5). **C0 ✅** —
Findings-Tabelle unten (P8-25), keine Fund-Eskalation nötig (alle 35 Einträge auf C1–C5/D1
gemappt oder bereits aligned). **C1 ✅ gebaut** (C1a Font-Swap + C1b CSS-Tokens, F1/F2/F3/F4/F6
geschlossen; 958/958 pytest, ui_budget 5/5, Tabu-Diff leer). **C2 ✅ gebaut** (Lucide-Sprite mit
18 Icons, F9/F10/F11 geschlossen — 7 HTML-Entities in app.html + 3 Text-Glyphen in js/
ersetzt, V92 mit Lucide 1.38.0 + SHA-256 d28944cf… gepinnt; Generator idempotent + --
check-Modus, js/icons.js (13. JS-Modul), .icon-CSS-Klasse + Lucide-Defaults; 958/958 pytest,
ui_budget 5/5 (110.3/250 KB), Tabu-Diff leer, kein Live-Touch (P8-L bleibt); **Sichtprüfung 1
(Plan §8) folgt nach C1 + C2 zusammen** — Typo-Größen und Icon-Lesbarkeit gehören für den
Augenschein zusammen). **C3 ✅ gebaut** (Farbsemantik --space-own/#4A93F0 + --space-shared/
#2EB8A6 + --space-foreign/#8B93A1 in app.css :root; drei rail__glyph--{cat}-Varianten für den
Space-Buchstaben in tree.js; space-dot--{cat} in der globalen Listen-Metazeile in list.js,
itemMetaLine() aufgeteilt -- rendert nur noch den Tail; state.js spaceCategory() neu; .legend
statisch in app.html-Overview; Sichtprüfung gegen eine Wegwerf-Instanz auf 127.0.0.1:18766:
overview zeigt Legende + blauen rail-Glyph, „Alle Items" rendert blauen space-dot vor `alpha` in
der Metazeile; 958/958 pytest, ui_budget 5/5 (112.0/250 KB), Tabu-Diff leer, JS-Syntax
`node --check` auf state/tree/list.js OK; zwei Screenshots `docs/screenshots/c3_01_*.png` +
`c3_02_*.png`; `phase8_ui_graph/scripts/{wegwerf_setup_c3.py,c3_playwright_smoke.py}` neu —
Standing-Permission-Muster P5 Step 6/7b reproduziert, eigener Port 18766, File-Keyring-Backend
statt `nikinger-space`, eigener DEK als base64-Datei, User direkt in `auth.sqlite3`
provisioniert via `AuthStore.upsert_user()`+`set_totp()`+`confirm_totp()` — kein
`provision_user.py`/`keyring.set_password`, kein Schreiben in den echten
`nikinger-space`-Service; cleanup per `kill -TERM $(cat serve.pid)` — kein `pkill -f`-Regex
(Hard Rule 9)). **D1 ✅ gebaut** (Übersicht tabellos — `app.html` `#detail-overview`-Struktur
ersetzt: `<header class=overview__header>` mit Refresh-Knopf + bestehende `.legend`, dann
`<ol id=overview-spaces>` für die tabellosen Space-Zeilen, dann `<h2>Verknüpfungen</h2>`
+ `<div id=overview-graph><canvas id=overview-graph-canvas></canvas></div>`-Gerüst für D2,
dann bestehende „Zuletzt benutzt"-Liste; `app.css` `.overview__tiles/.tile/.space-card`
entfernt (F12/F13/F23 aufgelöst), `.overview__header/.overview__spaces/.overview__space-row/
.overview__space-name/.overview__space-counts/.overview__space-count/.overview__graph`
neu mit Space-Token-gerechter Typografie und 720px-Maximalbreite (recent-Analogie);
`list.js :: renderOverview()` neu — eine Zeile je Space (eigene zuerst, dann fremde,
localeCompare), Kategoriepunkt via `spaceCategory(space)` aus C3, Counter-Chips nur für
Buckets mit `count > 0` (Plan §5 D1, „keine leeren Buckets"), Chip-Klick navigiert wie die
alten Tiles via `navigate(space.name, bucket)`; `app.js` Home-Knopf-Handler erweitert —
`Editor.closeEditor().then(proceed => proceed === false ? null : navigateAll())`,
V82-Regression explizit getestet (Smoke Step 5), Refresh-Knopf ruft `List.loadOverview()`
(D2 erweitert um `Graph.loadGraph()`); `phase8_ui_graph/scripts/{wegwerf_setup_d1.py,
d1_playwright_smoke.py}` neu — Standing-Permission-Muster C3 reproduziert, eigener Port
**18767**, File-Keyring-Backend, User `alpha` direkt in `auth.sqlite3`, zweiter Space
`beta` über `spacectl.py create-space` + `add-member --read beta alpha` (P6-M-Rechtepolitik,
`.share.yml` entsteht), 3 Items in alpha + 2 in beta (gemischt Typen, so dass Counter-
Chips greifen); Playwright-Smoke 5/5 grün — statisches Markup (header/spaces/graph-canvas
vorhanden, `.overview__tiles`/`#overview-foreign` weg), Login + zwei Space-Zeilen mit
korrekten `rail__glyph--{own,foreign}` und Counter-Chips (alpha 2 Chips, beta 1),
Chip-Klick navigiert zur richtigen Bucket-Liste (Crumb `alpha › Offen`), Home-Klick
schaltet Liste auf globalen Scope (Crumb „Alle Items", 5 Items sichtbar), Home-Klick im
bereits-globalen Scope idempotent (V82); drei Screenshots
`docs/screenshots/d1_{01_overview_space_rows,02_counter_chip_navigates,
03_home_to_global_scope}.png`; `phase8_ui_graph/CLAUDE.md` Modul-Status Block D auf
„D1 ✅ gebaut, D2/D3 offen" gehoben + Abnahmestand um D1-Zeile ergänzt + dieser
Session-Block; **958/958 pytest** (vorher/nachher identisch, keine Python-Änderung),
`ui_budget` 5/5 grün (113.0/250 KB, +1.0 KB), Tabu-Diff §0.4 leer, JS-Syntax
`node --check` auf list.js/app.js OK; kein Code ausserhalb `webui/static/` +
`phase8_ui_graph/scripts/` berührt; Produktion **unangetastet** (kein Deploy, kein
Service-Touch).

---

## C0 — Anti-AI-Pattern-Research + UI-Audit (P8-25, Plan §4.C0)

**Auftrag:** vor dem ersten UI-Commit in Block C einmal bewusst hinschauen, was die
LLM-Default-Aesthetik 2026 überhaupt ist — und gegen den Code hier halten. „Wir benutzen
keine schablonenhaften AI-Looks" lässt sich nur behaupten, wenn man die Schablonen kennt.
V94 (Web-Recherche für C0-Teil 1) bestätigt: opencode hat brauchbare Web-Recherche.

**Quellen (Teil 1, 2026-09-01):**

| Quelle | Kernbeitrag |
|---|---|
| developersdigest.tech — *AI Design Slop: 16 Patterns That Out Your App as Vibe-Coded* (Krebs' Show-HN-Audit, 1.590 Seiten) | der 16-Punkte-Score, Methodik (Playwright + DOM/CSS-Checks, kein LLM-Judge), Heavy-Slop-Anteil 22 %, Mild 32 %, Clean 46 %; die zwei dominanten CSS-Fingerabdrücke sind shadcn/ui und Glassmorphism |
| sailop.com — *Complete Guide to Anti-AI Design in 2026* | sieben Dimensionen (Color/Typography/Layout/Animation/Components/Spacing/Craft Signals) mit deterministischen Checks; das `#3B82F6`–`#6366F1`-Blau-Band, die `gray-50`-Hintergrund-Signatur, drei gleiche Cards |
| fountaininstitute.com — *7 Signs a UI Has Been Vibe Coded* | Neon-Paletten, Glow-Effekte, Emoji-Icons, Purple-Gradients, Card-in-Card, mehrfarbige Side-Tabs, bedeutungslose Status-Dots |
| noqta.tn — *Escaping AI Slop: Fix the 4 Overused AI UI Patterns* | „Wes Bos’ vier apokalyptische Reiter": übergroße Border-Radii, Glow-Gradients, breites Letter-Spacing, generische „Live"-Badges |
| monet.design — *7 Tips to Make Your Vibe-Coded UI Look Professional* | Tokens zuerst, 8-px-Raster, Echtcontent statt Lorem, Layering statt One-Shot-Prompt, Animation nur als Feedback |
| dev.to/jaainil — *AI Purple Problem: Make Your UI Unmistakable* | OKLCH statt RGB/HSL, Material-You-HCT als Anti-Mittel gegen Monokultur, Tailwind-Defaults als Trainingsbias auf indigo |
| phase8_ui_graph_plan §0.3 Verbotsliste (sechs Punkte) | die für jeden UI-Commit verbindliche Kompaktform, an der sich jeder Fund messen lassen muss |

**Konsolidierter Befund gegen `app.html`/`app.css`/`js/` (Teil 2):** die App ist überwiegend
schon **nicht** auf dem AI-Default-Pfad — P5-X („Dunkel-first, Apple-Formensprache vor
Liquid Glass") und P5-U („nüchterne deutsche UI-Texte") haben die gröbsten Tells
bereits ausgeschlossen. Was bleibt, sind die fünf echten Funde (F1, F9, F10, F11, F16/F19)
plus die sechs Stellen, an denen der Plan-C1–C5/D1 sowieso ansetzt (F12/F13 werden von D1
abgelöst, F4/F20/F21/F24 von C1/C5, F8 bleibt ein bewusster Einzelfall). Keine Funde
eskaliert (P8-25, „benannte Nikinger-Entscheidung"); die Verbotsliste §0.3 hält.

### Findings-Tabelle (Muster → Fundstelle → Fix → Ziel-Step)

| # | Muster (Quelle) | Fundstelle (Datei:Zeile) | Fix | Ziel-Step |
|---|---|---|---|---|
| **F1** | Inter als alleinige Schrift, kein Display-Cut, keine echte Skala — *developersdigest Punkt 1–3* | `app.css:14` (`@font-face Inter Variable`), `:44` (`--font-ui: "Inter Variable"…`), `:83` (`font-size: 15px`) | Plex Sans (variabel, 380–620) + Plex Mono statisch; OFL.txt getauscht; Basis 16 px; Skala als Tokens | **C1** |
| **F2** | Inter-`OFL.txt` muss raus, Plex-`OFL.txt` muss rein (lizenzrechtlich Pflichtbestandteil) | `phase5_ui/webui/static/fonts/OFL.txt` (Inter-Lizenz, 2025-11-22-Datum im Header) | Plex-OFL.txt ersetzen, Lizenztext-Pin wie `build_font_subset.sh` heute schon | **C1** |
| **F3** | Skala als Streu-px (13/14/15/22), keine Tokens | `app.css:83,102–104,243–247,313–320,515–531,572–577,602–603,621–622,802–804` und weitere | `--fs-meta/ui/body/title/page` als Tokens (Plan §4.C1); 16 px body; 1.55 line-height | **C1** |
| **F4** | Body-Schriftgröße 15 px statt 16 px (AI-Default, *Sailop Dim 2*) | `app.css:83` (`body { font-size: 15px; }`) | 16 px + 1.55 line-height (Plan §4.C1) | **C1** |
| **F5** | Kein `::selection`-Styling (Sailop Dim 7, „craft signal") — Text-Highlight ist Browser-Default-Blau | `app.css` (kein `::selection`-Block) | `::selection { background: var(--accent-quiet); color: var(--text); }` als einzige semantische Farbverwendung | **C5** (gehört zur Schriftrundung) |
| **F6** | IDs/Versionen/Metazeilen rendern in Default-Sans (klein, unauffällig), kein Mono-Akzent — *Fountain Institute „Cards for every block of info"* — vermischt Hierarchie-Ebenen | `app.html:95,112` (`#editor-version`, `#meta-item-id`); `app.css:99,785` | IDs/Versionen in `--font-mono` (Plan §4.C1, „IDs, Versions-Badge und Metazeilen rendern in `--font-mono`") | **C1** |
| **F7** | Akzentton-Vereinheitlichung schon gut (Uniformitäts-Wunsch P7-U) — `--accent: #3E8DF3` ist das einzige Blau; keine zweite Akzentfarbe (war früher `--ok` grün, schon zurückgenommen am 2026-08-16) | `app.css:33` (`--accent`), `:546` (`visibility-chip--shared`), `:1048` (`.toast`) | bleibt — kein weiterer Eingriff nötig | **bereits aligned** |
| **F8** | Radiales Auth-Page-Backdrop (Funktion: zieht den Blick zur zentrierten Karte) | `app.css:1186` (`.auth { background: radial-gradient(120% 80% at 50% 0%, #131A23 0%, var(--bg) 70%); }`) | bewusst kein Eingriff — Verbotsliste §0.3 Punkt 2 zielt auf Branding-Flächen, nicht funktionalen Auth-Vordergrund | **bewusst belassen** |
| **F9** | HTML-Entities als Icons (Verbotsliste §0.3 Punkt 1 — *Fountain Institute „Emojis used as icons"*) | `app.html:23` `&#8962;` (Übersicht), `:33` `&#9881;` (Konto), `:39` `&#9099;` (Abmelden), `:50` `&#43;` (Anlegen), `:151` `&#128279;` (Link), `:153` `&#8221;` (Zitat), `:157` `&#128444;` (Bild) | Lucide-Icon-Sprite: `house`/`settings`/`log-out`/`plus`/`link`/`quote`/`image` (Plan §4.C2 Ersetzungs-Map, V92 für die gepinnten Namen) | **C2** |
| **F10** | Text-Glyphen als Icons (gleiche Kategorie wie F9) | `list.js:351` `→` (Verschieben), `:368` `⇄` (Freigeben); `tree.js:203` `▾`/`▸` (Twist); `app.html:83,102` `&times;` (Editor-Schließen, Nur-lesen-Schließen) | `folder-input`/`share-2`/`chevron-down`/`chevron-right`/`x` (Plan §4.C2) | **C2** |
| **F11** | Lucide-Sprite-Infrastruktur partiell: B4 referenziert `#icon-search`, aber kein `<symbol id="icon-…">`-Block existiert in `app.html` — das `use href="#icon-search"` würde heute ins Leere zeigen | `app.html:135` (Verwendung) — `<!-- ICONS:BEGIN -->`-Marker fehlt | Vendoring unter `phase5_ui/vendor/lucide/` (ISC-Lizenz), Generator `build_icon_sprite.py` schreibt den Sprite-Block zwischen Marker (Plan §4.C2); THIRD_PARTY_LICENSES.md neu | **C2** |
| **F12** | Bucket-Counter-Grid (`overview__tiles`) — *Sailop Dim 5/6* „3 identical cards" — funktional, kein Marketing-Grid, aber **ersetzt durch D1** | `app.html:73` (Container); `app.css:579–603` (`.overview__tiles`/`.tile`); `list.js:40–47` (Render) | **ersetzt durch P8-J „tabellose Space-Zeilen mit klickbaren Zählern"** — keine Card-Optik | **D1** (löst es auf) |
| **F13** | Space-Cards für fremde Spaces (`space-card`, identisches Padding+Radius) — *Sailop Dim 5* | `app.html:71–77` (`overview`); `app.css:624–641`; `list.js:74–84` | ersetzt durch P8-J tabellose Zeilen | **D1** (löst es auf) |
| **F14** | Linke Akzentkante an ausgewählter Listenzeile + Akzent-Outline + `.list__rows > li.list__row--selected { box-shadow: inset 2px 0 0 var(--accent); }` — **NICHT** der AI-Tell „rainbow left borders" (eine Farbe, semantisch), aber **P8-H verlangt zusätzlich solide Indikatoren** (3 px-Akzentkante + Outline) | `app.css:471, 480–483, 510–513` | P8-H-Glass: 3-px-solide Akzentkante links + 1-px-Akzent-Outline, damit Auswahl bei deaktiviertem Blur/reduzierter Transparenz vollständig erkennbar bleibt | **C4** (deckt es ab) |
| **F15** | `.preview blockquote { border-left: 3px solid var(--accent); }` — semantisch (Zitatakzent), eine Farbe, **kein** AI-Tell | `app.css:699` | bleibt | **bereits aligned** |
| **F16** | Kein `prefers-reduced-transparency`-Handling (P8-H Pflicht, V85) — Firefox-Benutzer mit aktiviertem Systemsetting sehen heute Glas nicht, aber die App hat heute noch gar kein Glas | `app.css` (fehlt) | `@media (prefers-reduced-transparency: reduce) { .glass { backdrop-filter: none; background: var(--surface-raised); } }` | **C4** |
| **F17** | `:focus-visible` schon da (`app.css:108`); `prefers-reduced-motion` schon da (`app.css:113`) | beide Sailop-Dim-7-Signale abgehakt | bleibt | **bereits aligned** |
| **F18** | Animation 120 ms unter dem 200–300-ms-Profi-Bereich, kein `animate-pulse`/`scale-on-hover`/Framer-Motion, keine Scroll-Reveals | `app.css:119–122` (transition-Liste) | bleibt | **bereits aligned** |
| **F19** | Border-Radius diszipliniert (Token-gesteuert: `--radius: 10px`/`--radius-sm: 6px`, Pill nur dort wo es semantisch passt) — *Noqta „übergroße Border-Radii"* vermieden | `app.css:40–41` (Tokens), `:436,449,540` (Pill, semantisch) | bleibt | **bereits aligned** |
| **F20** | `--space: 8px` mit strikten Vielfachen — *Monet „8-px-Raster"* eingehalten | `app.css:42` | bleibt | **bereits aligned** |
| **F21** | Body-Lesebreite unbegrenzt im Editor (`max-width` nur in `.preview` Padding, nicht in Editor-Textarea) | `app.css:1010–1021` (`.editor__textarea`), `:163–167` (`editor__body`) | `max-width: 72ch;` auf Editor-Body + zentrierte Spalte (Plan §4.C5) | **C5** |
| **F22** | Editor-Body `padding-left: 12px` außerhalb des Space-Tokens (geringfügige Drift, *Monet „konsistentes 8-px-Raster"*) | `app.css:987` (`.editor__body`) | 12 px → `calc(var(--space) * 1.5)` | **C5** |
| **F23** | Drei gleiche Tiles (Bucket-Counter) als Default auf der Übersichtsseite — *Fountain Institute Punkt 5 „Cards for every block of info"* | siehe F12 (dort aufgelöst) | siehe F12 | **D1** |
| **F24** | Keine „Live"-Puls-Dots / keine „New"-Pillen / keine bedeutungslosen Status-Dots — *Fountain Institute Punkt 7* | `app.css` (keine `animation: pulse`) | bleibt | **bereits aligned** |
| **F25** | Keine generische Marketing-Mikrocopy („Build the future", „Scale without limits") — *Noqta „Rewrite the copy in a real voice"* — alle UI-Texte sind nüchternes Deutsch (P5-U) | `app.html`/`app.js`/`js/*.js` (Stichprobe: „Übersicht", „Verschieben", „Speichern", „Abbrechen", „Konflikt", „Erneut anmelden", „Aktuelle Fassung laden") | bleibt | **bereits aligned** |
| **F26** | Kein zentrierter Hero mit Badge über H1 — *developersdigest Punkt 10*, *Sailop Dim 3* — eine Daten-UI hat das nicht, die Übersichtsseite hat `h1.overview__title` (linksbündig, kein Badge darüber) | `app.css:569` (`.overview__title { margin-bottom: var(--space) * 2; }` — keine zentrierten Helden) | bleibt | **bereits aligned** |
| **F27** | Kein shadcn/ui-Visual (eigene Handrolle-CSS seit P5 Step 7b, *developersdigest „CSS-Fingerabdrücke"*) | `app.css` (kein `@apply`, keine shadcn-Tokens) | bleibt | **bereits aligned** |
| **F28** | Keine Aurora-Borealis-Backgrounds / großen farbigen Box-Shadows / Glow-Effekte — *Fountain Institute Punkt 2* | `app.css` (21 box-shadows, alle klein: `0 1px 2px`, `0 3px 8px`, einer 24 px für Modals) | bleibt | **bereits aligned** |
| **F29** | Kein „Magic Blue" Linear-Style (eigener Blauton `#3E8DF3`, *dev.to* „Linear-Aesthetic") | `app.css:33` | bleibt | **bereits aligned** |
| **F30** | Kein `accent-color`-Default-Verlust (am `<select>` schon explizit gesetzt, damit native Optionsliste nicht lila wird — Nikinger-Fund 2026-08-16) | `app.css:202` (`accent-color: var(--accent);`) | bleibt — *das* ist die richtige Antwort auf „AI-Purple-Problem", nicht „auf eine andere Markenfarbe wechseln" | **bereits aligned** |
| **F31** | Kein `::placeholder`-Color-Bloat — `app.css:31` hat `--text-placeholder: #7E8A98` (semantisch, ein Wert) | `app.css:192` | bleibt | **bereits aligned** |
| **F32** | Keine Mehrfach-Side-Tabs in Regenbogen-Farben (Fountain Institute Punkt 6) — eine einzelne Akzentkante an ausgewählter Zeile, *semantisch* | `app.css:480–483` | bleibt | **bereits aligned** |
| **F33** | Keine „Tailwind-blue-purple gradient"-Signatur (Sailop Dim 1, dev.to „AI-Purple-Problem") — die einzigen Gradients sind 180-deg-Erhöhungs-Verläufe auf Buttons/Tiles/Rail (*funktional*, *nicht dekorativ*, Verbotsliste §0.3 Punkt 2 zielt auf Branding-Flächen) | `app.css:125,134,137,142,153,156,224,283,296,434,481,591,928,1044,1074,1152,1192` | bleibt — nur F8 (Auth) wird bewusst nicht angetastet | **bereits aligned** |
| **F34** | Keine Tailwind-`gray-50`-Hintergrundsignatur (Sailop Dim 1) — eigener dunkler Grund `#0B0D10` | `app.css:22` (`--bg`) | bleibt | **bereits aligned** |
| **F35** | Keine Emoji-Icons (Unicode-Emoji) im UI — *Fountain Institute Punkt 3*, Plan §0.3 Verbotsliste | alle JS-Dateien (Stichprobe, kein `:rocket:`/`:white_check_mark:`/`:lock:`) | bleibt | **bereits aligned** |

**Zusammenfassung für die nächsten Steps:**
- **C1** trägt: F1, F2, F3, F4, F6 (Fonts/Tokens/Skala, sechs Stellen)
- **C2** trägt: F9, F10, F11 (alle Icons, Sprite-Infrastruktur, ~10 Stellen)
- **C3** trägt: keine direkten Findings (Farben sind bereits aligned), C3 fügt nur die
  drei Kategoriefarben `space-own`/`space-shared`/`space-foreign` + `.legend` hinzu
- **C4** trägt: F14, F16 (Glass-Akzent + Pflicht-Fallback, zwei Stellen)
- **C5** trägt: F5, F21, F22 (Selection, 72ch, Space-Token-Drift, drei Stellen)
- **D1** trägt: F12, F13, F23 (tabellose Übersicht statt Tiles/Cards — drei Stellen, von D1 aufgelöst)

**Keine Fund-Eskalation nötig** (P8-25): kein Fund ohne Ziel-Step, kein benannter Widerspruch
zu einer gelockten Entscheidung. F8 ist die einzige Stelle, an der die Verbotsliste §0.3 mit
einem bestehenden Verlauf in Berührung kommt — und sie ist durch ihre Funktion (Auth-Vordergrund)
gerechtfertigt; bewusst belassen, dokumentiert hier.

---

## Versions-Bump v2.2 → v2.2.3 (2026-09-01)

`.rail__version` in `phase5_ui/webui/static/app.html` Z. 20: `v2.2` → `v2.2.3`.
**Begründung:** Nikinger führt eine dritte Versionsstelle ein — „die letzte Zahl
der Version entspricht, wenn hinzufügt, der Step-Nummer". Phase 8 Block A Step 3
= A3, daher `v2.2.3`. Bisherige Konvention (P7-U): der Badge zählte Deploy-Zyklen
in zwei Stellen (`v2` → `v2.1` → `v2.2`); die dritte Stelle setzt diese Linie
fort, nicht ersetzt sie — Major (`v2`) bleibt, Minor (`v2.2`) bleibt bis zur
nächsten Phasen-Bumpscheidung, Patch (`v2.2.3`) ist der Step-Counter innerhalb
der Phase. Nur `app.html`-Änderung; `mcpserver.__version__` (`0.1.0`) bleibt
unangetastet (anderes Schema, Python-Introspection, nicht der User-Badge).

---

## Vormerkungen (nicht Teil eines aktuellen Steps)

**[2026-09-01] Nikinger-Feedback während der Screenshots-Session (Sichtprüfung 1) — ausdrücklich
nur vormerken, nichts davon diese Session umgesetzt, kein Code angefasst:**

1. **Auswahl-Boxen vereinheitlichen.** Die aktuelle Space-Auswahlbox im Verschieben-Dialog
   (`<select class="input" id="move-space-select">`, befüllt in `dialogs.js ::
   openMoveDialog()` ab Zeile 363 mit den `writable: true`-Spaces aus `state.spaces`)
   soll die **Standard-Auswahlbox** der App werden. Was heute schon in demselben Stil
   vorliegt und damit automatisch aligned ist: `#move-folder-select` (Ordner-Wahl im selben
   Dialog, identisches Pattern), `#space-member-write-select` (lesen/schreiben in der Space-
   Verwaltung, identisches Pattern). **Was beim Bauen weiterer Auswahl-Affordances neu
   hinzukommt, soll ebenfalls diesen Stil übernehmen** — natives `<select class="input">`,
   befüllt via `appendChild(option)`, kein eigenes Dropdown-Menü ohne triftigen Grund.
   Begründung: native Tastatur-Navigation (Pfeiltasten, Bild-Auf/Ab, Erstbuchstaben-Sprung),
   Screenreader-Verhalten und Mobile-Sheet-Darstellung sind über das Native Element
   automatisch korrekt; eigene Dropdowns müssten das alles nachbauen und sind
   erfahrungsgemäß (siehe den Phase-7-Dropdown-Lila-Fund vom 2026-08-16, `accent-color` an
   `<select>` gesetzt, damit die native Optionsliste nicht lila wird) fehleranfällig beim
   ersten Browser-Update.
   **[2026-09-02 ERLEDIGT]:** die Selection/Choice-Konvention v3 unten beantwortet die
   offene Frage nach „was ist Auswahl, was nicht" mit einer vier-gliedrigen Taxonomie
   (Choice vs. Toggle vs. Status vs. Navigation), und das Chevron-Vorbild (Lucide-Pfad
   `m6 9 6 6 6-6` als `background-image`-Data-URL auf `select.input`, mit `:disabled`-
   Variante in `--text-placeholder`) schließt die einzige sichtbare Lücke am Vorbild
   (`appearance: none` war gesetzt, aber kein Chevron — alle sieben `<select>`-Stellen
   renderten als reine Textbox). Verifiziert gegen Wegwerf 18771, Playwright-Smoke 9/9.
   Die Konvention ersetzt die offene Frage, ne neue-Anforderungen folgen aus dieser
   Sitzung nicht.

   **Heute inkonsistent — zu prüfen, was wirklich „Auswahl" ist und was nicht:**
   - **Rail-Bucket-Filter** (Offen/Erledigt/Notizen/Archiv): Button-Reihe mit
     rechtsbündigem Counter, kein `<select>`, sondern ein Toggle-Set. Eher Navigation als
     Auswahl — passt nicht in dieselbe Kategorie.
   - **Bucket-Tiles auf der Übersichtsseite** (0 Offen / 0 Erledigt / 3 Notizen / 0 Archiv):
     Card-Style, werden in D1 durch tabellose Space-Zeilen ersetzt (`P8-J`,
     F12/F13-Auflösung). Danach entscheidet sich, ob die neuen Zeilen den `<select>`-Stil
     übernehmen oder als Link-Liste bleiben.
   - **Visibility-Chip** („privat"): statisches Pill, kein Dropdown — andere Kategorie.
   - **Statusfilter** (in der Suche-/Filter-Zeile, soweit vorhanden): zu prüfen, ob das ein
     nativer `<select>` ist oder eine Custom-Liste.

   **Konkrete Empfehlung für die nächste Session:** die Kategorie „Auswahl" einmal explizit
   festlegen (was ist eine echte Auswahl mit einem, zwei oder vielen Werten, was ist eine
   Toggle-Gruppe, was ist ein statisches Label) und daraus eine Konvention für künftige
   Komponenten ableiten. Keine Code-Änderung in dieser Session.

2. **Ist das Design sonst final?** Nikinger-Frage vom 2026-09-01 nach den Screenshots.
   **Antwort: nein.** C0 + C1 + C2 sind ✅ gebaut und gepusht (`0281cce`/`08bff55`/
   `0d97b3a`); C3 (Farbsemantik + Legende, Plan §4.C3), C4 (Glass-Akzente +
   `prefers-reduced-transparency`-Fallback, Plan §4.C4), C5 (Dichte + F5 `::selection` + F21
   72ch + F22 Padding-Token, Plan §4.C5), D1/D2/D3 (Übersicht tablos + Force-Graph) sind
   ⬜. Plus Vormerkung 1 oben. **Sichtprüfung 1 selbst läuft noch** — Befunde des Nikingers
   (Typo-Größen, Icon-Lesbarkeit, ggf. Feinwerte) fließen entweder als C1-Nachschärfung
   (F3/F4/F6) oder als Vorlage für C3 ein; strukturelle Änderungen sind in Sichtprüfung 1
   nicht drin.

**[2026-09-02] Nikinger-Feedback nach Sichtprüfung 3 (c4c5_*-Screenshots) — ausdrücklich nur
vormerken, nichts davon diese Session umgesetzt, kein Code angefasst, kein Push:**

1. **Listenzeilen-Auswahl sieht anders aus als das „Auswahl"-Vorbild (Rail-Button-Stil).**
   Nikinger vergleicht zwei Screenshots:
   - `docs/screenshots/c4c5_03_editor_72ch.png` — selektierte Zeile „Aufgabe fuer morgen"
     mit dem neuen C4-Sheen (3-px-Akzentkante links + 1-px-Akzent-Outline rundum +
     Backdrop-Blur-Sheen, `phase5_ui/webui/static/app.css` Auswahl-Sheen-Block).
   - `docs/screenshots/03_list.png` (Sichtprüfung 1) — selektierter Rail-Button „Notizen",
     gefüllter Akzent-Hintergrund wie eine gedrückte Schaltfläche.

   **Befund:** die zwei „Auswahl"-Zustände in der App reden optisch unterschiedliche Sprachen
   — die Listenzeile markiert über Outline + Border-Left, der Rail-Button über einen soliden
   Akzent-Fill. **Was hier das Richtige ist, soll in der nächsten kontrollierten UI-Session
   entschieden werden** (Nikinger-Lauf gegen die Wegwerf-Instanz am echten Gerät, nicht
   opencode). Mögliche Richtungen: (a) **vereinheitlichen** — Listenzeilen-Sheen an
   Rail-Button-Stil angleichen oder umgekehrt, (b) **Sheen vereinfachen** — eine der drei
   C4-Schichten wegnehmen (z. B. die Outline raus, weil Border-Left + Blur schon reichen),
   (c) **bewusst unterschiedlich lassen** und die Differenz dokumentieren
   (Listenzeile = Inhalts-Auswahl, Rail-Button = Filter-Toggle, andere Semantik, andere Optik).
   **Aktueller C4-Code bleibt unverändert** — kein Edit in dieser Session.

2. **„Obsidian Übersicht" weiterhin WIP, vom Nikinger ausdrücklich bestätigt.** Block D
   (tabellose Übersicht mit Counter-Chips + handgerollter Canvas-Force-Graph) ist gebaut
   und liegt in `c4c5_01`, `sp2_01`–`sp2_06` und `d1_*`/`d2_*` vor. Nikinger sagt: „ja, klar
   dass die noch Überarbeitung braucht" — **keine neue Anforderung**, nur eine Bestätigung
   des erwarteten Stands. Soll im selben kontrollierten UI-Lauf mit auf den Schirm.

---

## Selection/Choice Konvention v3 (Block C, Vormerkung 1 vom 2026-09-01 beantwortet)

**Anlass:** Vormerkung 1 vom 2026-09-01 fragte nach der „Auswahl"-Kategorie. Die App hat
heute vier optisch verwandte, semantisch aber verschiedene Affordances — die Konvention
sortiert sie und legt fest, was wann verwendet wird. Verbindlich ab sofort für jeden
neuen UI-Commit in `webui/static/`.

### Die vier Kategorien

| Kategorie | Was es macht | Vorbild (Code, Selector) | Visuelle Sprache |
|---|---|---|---|
| **Choice** | *echte Auswahl* zwischen N Werten — einer, keiner oder viele davon gleichzeitig | `<select class="input">` (Vorbild: `#move-space-select`) | sunken (`.input`-Träger) + Lucide-Chevron-down rechts + `accent-color: var(--accent)` für Popup-Highlight |
| **Toggle** | einzelner Bool-Zustand — an/aus, ein/aus, sichtbar/unsichtbar | Buttons mit `aria-pressed` (z. B. `.pw-toggle`, `#home-button`) ODER `<input type="checkbox">` (z. B. `#overview-graph-toggle-tags`) | Button: linear-gradient + 1 px line; Checkbox: native Browser-Default mit `--accent` |
| **Status** | *Anzeige*, nicht Auswahl — was der Zustand IST, nicht was man darauf anwenden kann | `.visibility-chip`, `.list__row-meta`, `.rail__version`, `.tree__badge` (count) | Pill / Mono-Akzent / small-meta, niemals klickbar |
| **Navigation** | *Springt wohin*, oft mit Zähler verbunden — kein „Wert setzen", sondern „woanders hin" | `.tree__scope` (Bucket-Filter) mit `aria-current="true"`, `.tree__folder`, `.tree__space` (Space), `.overview__space-count` (Counter-Chip) | Akzent-Gradient-Fill wenn aktuell (`linear-gradient(180deg, rgba(62,141,243,.20), rgba(62,141,243,.08))`), sonst transparent |

### Choice — das Vorbild im Detail (Anker für künftige Commits)

- **Markup:** natives `<select class="input" id="…">`, **nicht** ein eigenes `<div>`/`role="listbox"`-
  Konstrukt. Die App hat heute 7+1 Choice-Stellen, alle identisch:
  1. `#field-status` (Item-Editor, Status)
  2. `#create-type` (Anlegen-Dialog, Item-Typ)
  3. `#new-folder-parent-select` (Anlegen-Dialog, Übergeordneter Ordner)
  4. `#move-space-select` (Verschieben-Dialog, Ziel-Space)
  5. `#move-folder-select` (Verschieben-Dialog, Ziel-Ordner)
  6. `#space-member-write-select` (Space-Verwaltung, lesen/schreiben — hardcodiertes `<option value="">lesen</option>` + `<option value="write">schreiben</option>`)
  7. Per-Item-Share-Row (`dialogs.js :: openShareDialog()` ab Z. 421, dynamisch erzeugte
     `<select class="input">` für jeden bekannten Space — read / write / leer)
- **CSS:** `select.input { appearance: none; padding-right: 28px; background-image:
  url("data:image/svg+xml;…chevron-down…"); accent-color: var(--accent); }` plus
  `:disabled`-Variante in `--text-placeholder`. **Kein** Custom-Chevron via SVG-`<use>`-
  Konstrukt nötig — die Data-URL ist 0,5 KB statt eines zweiten Sprite-Eintrags und bleibt
  portabel (funktioniert auch dann, wenn das Lucide-Sprite noch nicht geladen ist).
- **JS:** `appendChild(option)` mit `.textContent` und `.value`. Die zwei `<option>`-
  Defaults (`lesen`/`schreiben`) im hardcodierten Select dürfen im HTML bleiben, weil sie
  *die* Funktionskonstante sind — kein API-Aufruf nötig.
- **Native Vorteile (Begründung für den Vorbild-Charakter):** Pfeiltasten-Navigation,
  Bild-Auf/Ab, Erstbuchstaben-Sprung, Screenreader-Verhalten, Mobile-Sheet-Darstellung
  — alle automatisch korrekt; der Phase-7-Lila-Fund vom 2026-08-16 (Browser-Akzentton
  statt App-Blau in nativer Optionsliste) wurde durch `accent-color: var(--accent)`
  strukturell geschlossen.

### Was diese Konvention NICHT macht

- Sie ändert **nichts** am Listenzeilen-Sheen aus C4 (3-px-Akzentkante + 1-px-Outline +
  Backdrop-Blur-Sheen) — Vormerkung 2 vom 2026-09-02 (Sichtprüfung 3) hatte drei mögliche
  Richtungen benannt; diese Sitzung hat keine davon umgesetzt, weil der Sheen durch N8
  begründet ist (Auswahl darf nicht allein von Transparenz abhängen, sonst bei
  `prefers-reduced-transparency: reduce` unsichtbar). Eine Vereinheitlichung mit dem
  Rail-Button-Akzent-Gradient-Fill (Navigation-Kategorie) wäre aus Sicht des Servers eine
  *Vermischung zweier Kategorien* — semantisch falsch.
- Sie passt **nicht** den Counter-Chip-Stil auf der Übersichtsseite an den `<select>`-
  Chevron-Stil an — Counter-Chips sind Navigation, kein Choice, andere Kategorie.

### Wo sie ansetzt, wenn etwas Neues kommt

- **Brauche ich einen Wert aus N?** → `<select class="input">` mit `appendChild(option)`.
  Vorbild: sieben existierende Stellen. **Niemals** eigene Dropdowns / Popovers / `<div
  role="listbox">` ohne triftigen Grund.
- **Ist es an/aus?** → Button mit `aria-pressed` oder `<input type="checkbox">` mit
  explizitem `<label>`. Native Tastatur- und Screenreader-Verhalten eingebaut.
- **Zeige ich nur einen Zustand an?** → `.visibility-chip` / `.list__row-meta` / Pill —
  niemals als Auswahl verkleidet.
- **Springe ich woanders hin?** → Button mit `aria-current` (Navigation aktiv) oder
  semantischer Link.

### Größe dieser Konvention

Reine Doku, kein Code über die Chevron-Data-URL hinaus. Der Konventionstext selbst ist
bewusst knapp gehalten — Tabellenform, ein Markup-Beispiel, keine ausschweifenden
Begründungen pro Choice-Stelle. Sie landet hier im Phase-Head, nicht im Plan, weil sie
eine **Arbeits-Konvention** für die laufende Phase ist; bei Step Z wird sie in die
allgemeine Doku-Layer-Konvention (`docs/DOC_LAYERS_CONVENTION.md`) überführt oder als
P9-Arbeitsanweisung weitergeführt, falls die Nikinger-Entscheidung anders ausfällt.

---

## Session stopped — 2026-09-02 (Auswahl-Chevron-Vorbild + Selection/Choice Konvention v3 — Vormerkung 1 vom 2026-09-01 erledigt)

**Auftrag:** Nikinger-Auftrag zu Beginn: „Auswahl Button überarbeiten, Option vereinheitlichen,
Vorbild initiales Design; Obsidian Übersicht ist WIP, aber nicht mehr in dieser Phase."
Mapping auf den Stand: (a) Auswahl-Vorbild = `<select class="input">` mit Chevron aus dem
Lucide-Sprite (Vormerkung 1 vom 2026-09-01); (b) Obsidian-Übersicht (D2) bleibt WIP
wie vom Nikinger ausdrücklich bestätigt (Vormerkung 2 vom 2026-09-02), keine Änderung
am `js/graph.js` oder am Graph-Panel in `app.css`/`app.html`. Plan-Reihenfolge ist
0 → A → B → Gate → C → D → Z; der C4+C5-Block der vorherigen Session steht, Block C ist
damit optisch-konsistent, Block D bleibt inhaltlich wie er ist.

**Code-Änderung (eine Datei, +19/-1 Zeilen, 0 Tabu-Diff-Zeilen §0.4):**

- `phase5_ui/webui/static/app.css` — **Auswahl-Chevron-Vorbild in `select.input`:**
  - `appearance: none` war bereits gesetzt (aus dem Phase-7-Lila-Fund, `accent-color` auf
    `var(--accent)` zwingt native Optionsliste auf App-Blau), aber **kein Chevron-Ersatz**.
    Folge: alle sieben `<select class="input">`-Stellen renderten als Textboxen ohne
    Auswahl-Indikator — ein „ich bin eine Auswahl"-Affordance fehlte im Vorbild.
  - Neuer Lucide-Chevron-down als `background-image`-Data-URL: SVG-Pfad
    `m6 9 6 6 6-6` (derselbe Pfad, den das Lucide-Sprite unter `#i-chevron-down` führt,
    app.html:491), Stroke `var(--text-faint)` = `#A7B2BF` (leiser als der Wert-Text,
    „ich bin ein Indikator", nicht „ich bin Inhalt"), 12×12 px (0,5em in 16-Pixel-Schrift,
    bewusst klein), Stroke-Wwidth 2.5 (statt Lucide-Default 2 — etwas mehr Gewicht auf
    dem dunklen App-Grund), Position `right 8px center`, `background-repeat: no-repeat`.
  - `padding-right: 28px` (vorher 24 px) — Platz für den Chevron, damit der Wert-Text
    nicht unter den Chevron läuft.
  - `:disabled`-Variante: Chevron-Stroke in `--text-placeholder` = `#7E8A98`, plus
    `opacity: .6` — eine deaktivierte Auswahl sieht aus wie eine deaktivierte Auswahl,
    nicht wie ein Möchtegern-Auswahl mit versteckter Funktion.

**Warum Data-URL statt `<svg><use>`:** die Data-URL kostet 0,5 KB in `app.css` und
funktioniert auch dann, wenn das Lucide-Sprite noch nicht geladen ist (Race-Condition
in einem `<details>`-Panel, das per Klick aufgeklappt wird); ein `<use href="#i-…">`
im Markup würde genau dort verschwinden, wo man es braucht. Der Chevron ist visuell
„eingerichtet" — er muss sich identisch verhalten, ob das Sprite schon da ist oder
nicht.

**Wegwerf + Smoke (Standing-Permission reproduziert):**

- `phase8_ui_graph/scripts/wegwerf_setup_auswahl_chevron.py` neu (Port **18771**, File-
  Keyring, User `alpha` direkt in `auth.sqlite3` provisioniert via `AuthStore.upsert_user` +
  `set_totp` + `confirm_totp` — Standing-Permission-Muster aus C3/C4+C5 reproduziert).
  Datenlage identisch zum C4+C5-Smoke: 5 eigene Items + 2 fremde = 7 Items über zwei
  Spaces (`alpha`/`beta`), keine Folder.
- `phase8_ui_graph/scripts/auswahl_chevron_playwright_smoke.py` neu (**9/9 grün**):
  - **Step 1** — `select.input`-Regel enthält Lucide-Chevron-Pfad `m6 9 6 6 6-6` als
    `data:image/svg+xml`-URL, `padding-right: 28px`, plus `select.input:disabled`-Regel
    in `--text-placeholder`.
  - **Step 2** — Login + Overview rendert (Sanity-Check für die Folge-Steps).
  - **Step 3** — Item-Editor, `#field-status`: `computed background-image` =
    `url("data:image/svg+xml…")` (Kopfdaten-Panel musste per Klick auf `<summary>`
    aufgeklappt werden, weil `#field-status` in einem `<details>` mit Default `closed`
    sitzt).
  - **Step 4** — Anlegen-Dialog, `#create-type`: Chevron rendert (Anlege-Knopf nur in
    eigenem Space sichtbar — Navigation auf `.tree__space:has-text('alpha')` vor dem
    Klick nötig).
  - **Step 5** — Anlegen-Dialog, `#new-folder-parent-select`: Chevron rendert.
  - **Step 6** — Verschieben-Dialog, `#move-space-select`: Chevron rendert (Mehrfach-
    auswahl via Strg+Klick auf erste Listenzeile, `dialogs.js` öffnet den Dialog mit
    `writable: true`-Spaces).
  - **Step 7** — Verschieben-Dialog, `#move-folder-select`: Chevron rendert.
  - **Step 8** — Freigabe-Dialog, Per-Item-Share-Row: dynamisch erzeugte
    `<select class="input">` rendert Chevron (Lucide-Sprite-Loader unabhängig — die
    Data-URL hat den Vorteil bewiesen).
  - **Step 9** — Space-Verwaltung, `#space-member-write-select`: statische Regel greift
    auch ohne geöffneten Dialog (Selector im DOM von `app.html`).

**Screenshots (zwei PNG, ~150 KB, unter `docs/screenshots/`):**

- `auswahl_chevron_01_move_dialog.png` — Verschieben-Dialog geöffnet, beide Selects
  (`#move-space-select` + `#move-folder-select`) mit sichtbarem Chevron-Down rechts, Wert-
  Text links (`alpha` bzw. `(Space-Wurzel)`).
- `auswahl_chevron_02_share_dialog.png` — Freigabe-Dialog geöffnet, Per-Item-Share-Row
  mit `<select class="input">` für `beta` (lesen), Chevron rendert.

**Verifikation — Selbstprüf-Checkliste §0.6 alle fünf Punkte grün:**

1. `pytest -q` → **958/958 grün** (keine Python-Änderung, vorher/nachher identisch,
   255 s).
2. Tabu-Diff (`git diff --stat main -- phase4_auth/ phase2_mcp/ phase5_ui/webui/
   security.py phase1_storage/storage/{models,frontmatter,files,patch,acl,history}.py`)
   → **leer** (nur `app.css` + Smoke/Setup-Skripte + zwei Screenshots berührt).
3. JS-Syntax: `node --check` auf `app.js`/`list.js`/`state.js`/`tree.js`/`dialogs.js`/
   `editor.js`/`spaces.js` → **0 errors** (kein neuer JS-Code in dieser Session, nur
   reines CSS).
4. Doc-Update im selben Commit (Hard Rule 8) — `updated:`-Frontmatter +
   Selection/Choice-Konvention v3 + Vormerkung-1-ERLEDIGT-Marker + dieser Session-
   Block.
5. `python phase5_ui/scripts/ui_budget.py` → **5/5 grün**, app.js+css+Font jetzt
   **123.3 KB** (vorher 122.7 KB, +0.6 KB für die zwei `select.input`-Regeln + die
   `:disabled`-Variante). Im Korridor (<250 KB). V84 weiterhin erfüllt.

**Wegwerf abgebaut:** `kill -TERM $(cat serve.pid)` (PID-Datei-Muster, **kein** `pkill
-f` mit Regex — Hard Rule 9 eingehalten); `rm -rf /tmp/opencode/sharefyx-wegwerf-
auswahl-chevron/` im selben Zug. `curl http://127.0.0.1:8765/health` → `{"status":"ok",…}`
(uptime linear wachsend, **kein Service-Touch durch diese Session**); `ps -ef` zeigt nur
die `sharefyx-mcp.service`, Wegwerf-PID weg.

**Was diese Session bewusst NICHT gemacht hat** (gegen Vormerkung 2 vom 2026-09-02):

- **Listenzeilen-Sheen (C4) unverändert.** Die drei möglichen Richtungen aus
  Vormerkung 2 (vereinheitlichen mit Rail-Button / vereinfachen / bewusst unterschiedlich
  lassen) wurden nicht umgesetzt. Begründung: der C4-Sheen (3-px-Akzentkante +
  1-px-Outline + Backdrop-Blur-Sheen) erfüllt N8 (Auswahl darf nicht allein von
  Transparenz abhängen — sonst bei `prefers-reduced-transparency: reduce` unsichtbar);
  eine Vereinheitlichung mit dem Rail-Button-Akzent-Gradient wäre außerdem eine
  *Vermischung zweier Selection-Kategorien* (Choice vs. Navigation) — semantisch falsch.
  Diese Entscheidung steht jetzt in der Selection/Choice Konvention v3 dokumentiert.
- **Counter-Chip-Stil unverändert.** `.overview__space-count` ist Navigation (Klick
  navigiert zur Bucket-Ansicht), kein Choice. Chevron-Vorbild passt hier nicht.
- **Obsidian-Übersicht (D2) unverändert.** `js/graph.js` (542 Zeilen) und das Graph-
  Panel in `app.css`/`app.html` bleiben wie sie sind — der Nikinger hat den WIP-Stand
  am 2026-09-02 ausdrücklich bestätigt (Vormerkung 2 Punkt 2), keine Änderung gewünscht.

**Verbleibend für die nächste Session:**

- **Nikinger-Sichtprüfung 3 (echtes Gerät):** die C4-Glas-Akzente + C5-Editor-72ch +
  **neu diese Session** das Chevron-Vorbild (Größe 12 vs. 14 px, Stroke-Wwidth 2.5
  vs. Lucide-Default 2, `--text-faint` vs. `--text`) — die Feinwerte sind
  Smoke-verifiziert, aber das Auge am Bildschirm entscheidet. `--glass-bg` Alpha
  kann ebenfalls nachjustiert werden müssen (Background-Gradient im echten Browser
  stärker als im Headless).
- **Sichtprüfung 2 (D3 wartet ebenfalls noch am echten Gerät).**
- **Step Z** (Phase-Closeout) — wenn beide Sichtprüfungen passen:
  - `phase1_storage/CLAUDE.md` — achte P1-Contract-Öffnung als „geschlossen" markieren.
  - `docs/concepts/phase8_ui_graph_plan.md` §9 — Closeout, Abnahmebilanz P8-1…P8-26,
    die drei P7-Erbposten (P7-24 ✅ A1, remove-space ✅ A2, P7-4 🟡 A3 Restdefekt).
  - Selection/Choice-Konvention v3 in die allgemeine Doku-Layer-Konvention überführen
    oder als P9-Arbeitsanweisung weiterführen — **eine Nikinger-Entscheidung**, nicht
    von opencode.
  - `ROADMAP.md` Phase-8-Status auf ✅ oder 🟡 (Nikinger-Entscheidung).
  - `docs/INDEX.md` Größenangaben nachziehen.
  - `docs/UPDATE_LOG.md` neuer Eintrag am Deploy-Tag (P6-X-Gate).
  - `deploy.sh main` durch den Nikinger.

**Nächster Schritt, konkret:** Nikinger-Sichtprüfung 3 (echtes Gerät) für die
C4/C5-Verbauungen + die Chevron-Akzente dieser Session. Wenn die Feinwerte passen,
Step Z im selben Sitzungsblock.
