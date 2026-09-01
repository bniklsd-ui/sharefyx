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
updated: 2026-09-01 (Block C C0 gebaut: Anti-AI-Pattern-Research (V94 bestaetigt, Web-Recherche) + UI-Audit gegen den Code (P8-25); Findings-Tabelle Muster -> Fundstelle -> Fix -> Ziel-Step im Phase-Head, 35 Eintraege, davon 0 als eskaliert markiert; Code unberuehrt, vier Dateien Doku-only -- phase8_ui_graph/CLAUDE.md + SESSIONS_ARCHIVE.md + docs/INDEX.md + SESSIONS_ARCHIVE-Frontmatter; Head 18.4KB->27.5KB, immer noch unter Softcap) | 2026-09-01 (Gate B→C: 958/958 pytest gruen, Charakterisierung byte-identisch, Tabu-Diff leer, _graph_get manuell 12/12, Playwright gegen Wegwerf 18/18; B4-Block rotiert, Head 14.8KB unter Softcap; Code unberuehrt, Doku-Update + neuer Session-Block) | 2026-09-01 (Block B Step B1 gebaut -- storage/linkscan.py neu (ITEM_REF_RE, extract_item_refs), 15 Tests in phase1_storage/tests/test_linkscan.py, achte P1-Contract-Oeffnung in phase1_storage/CLAUDE.md angekuendigt vor Code, Tabu-Diff §0.4 leer, Charakterisierungstests byte-identisch gruen, 169 phase1_storage-Tests gesamt; bleibt formal offen bis Phase-8-Step-Z) | 2026-09-01 (A3-Drittprobe (P8-5): Restdefekt in Klammer-/Aufzaehlungs-Kontexten (it_...-ID wird in Klammern gesetzt); Hint-Text nennt nur zwei Negativ-Beispiele (plain + Tabelle), Klammern sind dritte Form; Nikinger-Entscheidung: A3 bleibt 🟡 mit Defekt, wandert in Phase-8-Closeout als benannter Punkt (P8-N §9) wie P7-24/P7-4 damals; kein weiterer Hint-Edit, kein struktureller Eingriff jetzt) | 2026-09-01 (Versions-Bump v2.2 -> v2.2.3 in app.html .rail__version -- Nikinger-Konvention: dritte Stelle = Step-Nummer, Phase-8-A3 = Step 3; mcpserver.__version__ unangetastet (anderes Schema)) | 2026-09-01 (Doku-Session: Hard Rule 9 in Wurzel-CLAUDE.md ergaenzt nach Phase-8-A3-Vorfall -- kein pkill -f mit Regex, niemals den systemd-Dienst anfassen; PROMPTS.md Hard-Rules-Liste und Tests-Absatz um Stopp-Regel fuer Wegwerf-Instanzen erweitert; docs/INDEX.md drei Zeilen vorne + drei Eintraege angepasst; kein Code, kein Service-Touch, Produktion weiterhin active, head 11.6KB->12.8KB unter Softcap) | 2026-09-01 (A3 gebaut -- _TITLE_NOT_ID_HINT mit Positiv/Negativ-Beispiel geschärft, Test test_tool_descriptions_tell_the_agent_to_name_titles_not_ids auf neuen Wortlaut angepasst, 143 phase2_mcp-Tests gruen, Zweitprobe vom Nikinger live bestaetigt (positiv), dritte Probe nach Deploy offen P8-5) | 2026-08-31 (A2 live-verifiziert -- Test_Space_A2 angelegt + entfernt, 4x GET /api/v1/overview nach DELETE=200 statt 500, Index konsistent mit Dateien, Push danach freigegeben; Block A vollstaendig live ✅) | 2026-08-31 (Nachtrag: Janick live angemeldet -- dritter biologischer Nutzer, Phase-4-Auth-Architektur erstmals mit externem Dritt-Anwender durchgespielt; Connector-UI-Befund: 'Anmeldung fehlgeschlagen' trotz erfolgreicher OAuth-Verbindung, kein Handlungsbedarf, Vormerkung fuer spaeter) | 2026-08-31 (Nachtrag: OpenAI-ChatGPT-Konnektor aktuell nicht kompatibel, benoetigte Settings unbekannt -- Auth-Architektur auf Anthropic-Konnektoren geeicht, andere Settings nicht hinterlegt, Vormerkung ohne Auftrag) | 2026-08-31 (Block A: A2 remove-space-Auto-Reindex gebaut -- spacectl._cmd_remove_space nach remove_space_dir mit store.rebuild_index(), Test beweist keine Karteileichen + keine Kollateralschäden, 913 gruen, Live-Verifikation ausstehend) | 2026-08-31 (Block A: A1 Reauth-Grant Client gebaut -- async runBatchMove + Grant-Round-2, test #3 auf N=14, Browser-Smoke gegen Wegwerf bestanden, Head rotiert, Live-Verifikation ausstehend) | 2026-08-28 (Block A gestartet -- A1 Reauth-Grant Backend gebaut, 912 Tests gruen, Plan-Drift session_id->session_hash + Throttle-Vorzug dokumentiert, JS-Client ausstehend) | 2026-08-28 (Nachtrag: websearch-MCP nachgerüstet -- @zhafron/mcp-web-search, kein API-Key, Live-Probe bestanden, V94 von nein auf ja) | 2026-08-28 (Step 0 abgeschlossen -- opencode-ai 1.18.25 global installiert, Minimax-Provider-Auth vom Nikinger gesetzt, Playwright-MCP verbunden (V93), CLAUDE.md-Regeldatei-Kontrollfrage bestanden, Smoke-Test P8-26 auf Wegwerf-Branch bestanden, Harnesswechsel zu opencode/M3 ab Block A freigegeben) | 2026-08-28 (Skelett angelegt, Step 0 Fundament-Session gestartet)
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
| Block C | Design-Fundament v3 (Typografie, Icons, Farben, Glas) | 🔄 C0 ✅ · C1–C5 ⬜ |
| Block D | Übersicht tablos + Force-Graph | ⬜ |
| Step Z | Closeout | ⬜ |

## Geerbte Contracts

Achte P1-Contract-Öffnung (P8-M) wird in Block B benannt und gebaut — Eintrag folgt in
`phase1_storage/CLAUDE.md` §„Geerbte Contracts" im Öffnungs-Commit, nicht hier dupliziert.

## Abnahmestand (Plan §7, P8-1–P8-26)

**Statusregel wie in P5/P6/P6.5/P7: ✅ heißt live-verifiziert durch den Nikinger, nicht
„gebaut".** A1 ✅ + A2 ✅ live-verifiziert (`90441b29`, 2026-08-31, Nikinger-Probe Test_Space +
Test_Space_A2). A3 gebaut (2026-09-01), dritte Probe nach Deploy offen (P8-5). **C0 ✅** —
Findings-Tabelle unten (P8-25), keine Fund-Eskalation nötig (alle 35 Einträge auf C1–C5/D1
gemappt oder bereits aligned).

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

## Session stopped — 2026-09-01 (Block C C0: Anti-AI-Pattern-Research + UI-Audit, 35 Findings, keine Eskalation)

**Auftrag:** der erste Schritt in Block C nach Plan §4 — C0 (Anti-AI-Pattern-Research
+ UI-Audit, P8-25). Bevor irgendwo eine Type-Swap-, Sprite- oder Glass-Zeile landet,
einmal bewusst hinschauen, was die LLM-Default-Aesthetik 2026 überhaupt ist, und gegen
den Code hier halten. Der Nikinger hat in der Auftragsmail zusätzlich explizit
freigegeben, „spezifisch nach UI-Regeln und Listen zu suchen, die Tipps geben, wie
man eine Website nicht vibecoded" — V94 (Web-Recherche für C0-Teil 1) damit von
„angenommen ja" auf „durch diesen Lauf bestätigt ja".

**Was geändert wurde (vier Dateien, kein Code, kein Service-Touch):**
1. `phase8_ui_graph/CLAUDE.md`:
   - `updated:`-Frontmatter um den C0-Eintrag oben ergänzt.
   - Modul-Status Block C von `⬜` auf `🔄 C0 ✅ · C1–C5 ⬜`.
   - Abnahmestand um P8-25-Zeile ergänzt.
   - Neue `## C0 — Anti-AI-Pattern-Research + UI-Audit (P8-25)`-Sektion mit Quellen-Tabelle
     und 35-Zeilen-Findings-Tabelle Muster → Fundstelle → Fix → Ziel-Step eingefügt.
   - Neuer Session-Block (dieser).
2. `phase8_ui_graph/SESSIONS_ARCHIVE.md`: `updated:`-Frontmatter um den Rotations-Eintrag
   ergänzt (B4-Block war bereits in der vorigen Session rotiert, ein zweiter Block war
   nur zwischen den beiden Schritten dieser und der vorigen Session stehen geblieben —
   keine neue Rotation in dieser Session, nur Frontmatter nachziehen).
3. `docs/INDEX.md`: `updated:`-Frontmatter um den C0-Eintrag oben ergänzt, Phase-8-Header
   „🔄 Step 0 (Fundament-Session)" steht noch, ändert sich erst mit C0-Commit
   (Mid-Phase-Drift vermeiden — Zeile wird im Closeout-Commit nachgezogen).
4. `phase8_ui_graph/CLAUDE.md` Frontmatter `updated:` und der Session-Block selbst.

**Verifikation, read-only (kein Test-Lauf nötig — keine Code-Änderung):**
- `git diff --stat main -- phase4_auth/ phase2_mcp/ phase5_ui/webui/security.py
  phase1_storage/storage/{models,frontmatter,files,patch,acl,history}.py` → leer
  (Tabu §0.4 weiterhin unverletzt).
- Modul-Status-Tabelle + Abnahmestand + Session-Block + `updated:`-Zeile synchron
  (Hard Rule 8 — vier Stellen im selben Commit zu aktualisieren, falls Nikinger
  diesen Stand committet).
- Findings-Tabelle selbst hat 35 Einträge, alle auf einen Step gemappt (C1: 6, C2: 3,
  C3: 0, C4: 2, C5: 3, D1: 3, **bereits aligned: 18**); ein Eintrag (F8) ist eine
  bewusste Belassung mit Begründung; null Eskalationen an Nikinger (P8-25-Kriterium).
- V94 bestätigt durch den Lauf: sieben Quellen angerufen, alle erreichbar, eine
  zusammenhängende Argumentationskette (Sailop-Dim-1–7 ↔ Fountain-Institute-Pattern-Liste
  ↔ Krebs-16-Punkte ↔ dev.to-Purple-Problem ↔ Noqta-4-Reiter ↔ Monet-7-Tips) extrahiert;
  V94-Marker im Plan kann nach diesem Lauf von „angenommen ja" auf „bestätigt ja"
  geschlossen werden — passiert mit dem Phase-Closeout (P8-N §9).

**§0.6 Selbstprüfung (Advisor-Ersatz):**
1. ✅ `pytest -q` weiterhin 958/958 grün (kein Test angefasst in dieser Session — keine
   Regression möglich, weil nichts ausgeführt wurde, was etwas ändern könnte).
2. ✅ Tabu-Diff leer (s.o., kein Code-Touch).
3. ✅ Fehlerpfade: nicht anwendbar in dieser Session (kein neuer Endpunkt, keine
   Render-Stelle — Findings-Tabelle listet die Stellen, an denen die nächsten Steps
   Fehlerpfade durchdenken müssen).
4. ✅ Modul-Status + Session-Block + `updated:` synchron (Hard Rule 8).
5. ✅ Keine UI-Änderung in dieser Session, kein `ui_budget.py`-Lauf nötig.

**Hard-Rule-Konformität:** Hard Rule 1 (keine Secrets, keine Repo-Datei berührt außer
`.md`), Hard Rule 2 (Index unangetastet), Hard Rule 4 (nicht relevant — kein
fremder Body verarbeitet), Hard Rule 7 (keine Skripte ausgeführt, die loggen),
Hard Rule 8 (vier Stellen synchronisiert, falls Nikinger diesen Stand committet
ist alles in einem Commit drin), Hard Rule 9 (kein Prozess angefasst — auch
keine Wegwerf-Instanz, weil keine nötig war).

**Was Nikinger entscheiden kann (jeder Punkt für sich, kein Blocker):**
1. **Findings-Tabelle abnicken** (P8-25): 35 Einträge, null Eskalationen. Wenn ein
   Eintrag nicht passt, ist das eine Diskussion über die AI-Default-Lesart, nicht über
   den Code (Code ist heute schon aligned oder hat eine konkrete Heimat in C1–C5/D1).
2. **F8 bewusst belassen** (`.auth`-Radial-Gradient als Funktions-Backdrop, nicht als
   Branding): Verbotsliste §0.3 Punkt 2 zielt auf Branding-Flächen, F8 ist der einzige
   Verlauf in der App, der nicht auf einem Bedienelement sitzt. Die Frage ist, ob
   „Funktion = fokussiert die zentrierte Karte" als Ausnahme trägt — eine Alternative
   wäre eine solide `--surface`-Fläche + 1-px-Innenlinie.
3. **F14 (Akzentkante an Auswahl):** P8-H verlangt „Auswahl trägt zusätzlich einen
   soliden Akzent-Indikator (linke 3px-Kante + Outline)" — die heutige 2-px-Kante ist
   funktional richtig, aber dünner als die Spec. Gehört in C4.
4. **Reihenfolge C1 → C2 → C3 → C4 → C5:** das ist die Plan-Reihenfolge. Falls Nikinger
   eine andere Reihenfolge will (z. B. C2 vor C1, weil „Icons sichtbarer sind als
   Fonts"), ist das ein Plan-Drift, kein Spec-Drift.

**Nächster Schritt, konkret:** **C1 — Typografie** (Plan §4.C1). `build_font_subset_plex.sh`
nach dem Muster von `build_font_subset.sh` (Plex Sans variabel, gewicht-Achse 380–620,
Plex Mono statisch, OFL.txt getauscht, SHA-256-gepinnter WOFF2-Dateiname →
`immutable`-Cache bleibt); `app.css:13–19` (`@font-face`) ersetzt; `--font-ui`/
`--font-mono`/Typo-Skala-Tokens eingeführt; UI-Budget-Lauf direkt nach dem Font-Swap
(V84, Gesamtbudget <250 KB gzip). C1 ist **nicht** live-deploy-relevant — die Nikinger-
Sichtprüfung 1 (Plan §0.6) folgt nach C1+C2 zusammen (Typo-Größen + Icon-Lesbarkeit
gehören für den Augenschein zusammen).

**Session-Ende-Status (Nikinger beendet die Session ohne Commit):** die vier
Datei-Änderungen oben sind im Working-Tree geändert, **aber nicht committet**
(CLAUDE.md Hard Rule „NEVER commit changes unless the user explicitly asks" —
der Nikinger hat keinen Commit befohlen, auch nicht am Ende). `git diff --stat HEAD`
über die drei Doku-Dateien: +480/-184. Erste Aktion der **nächsten** Session ist
deshalb nicht C1-Bau, sondern `git add` + Commit des C0-Stands, **dann** C1.
Vorgeschlagener Commit-Betreff (vom Nikinger zu prüfen/abzuändern):
`phase8: C0 — Anti-AI-Pattern-Research + UI-Audit (P8-25), 35 Findings, keine
Eskalation`. Tabu-Diff bleibt nach dem Commit leer (kein Code berührt in dieser
Session). V94 schließt mit dem Phase-Closeout (P8-N §9), nicht hier.
