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
updated: 2026-09-02 (P8-22+P8-24-Smokes gebaut, drei Phase-8-Funde als benannte Defekte vererbt; kein Code in storage/mcpserver/webui/static angefasst -- Nikinger-Entscheidung A "Luecken als benannte Defekte vererben" -- Smoke-Skripte phase8_ui_graph/scripts/{wegwerf_setup_200knoten.py,p8_22_smoke.py,phase8_e2e_smoke.py} neu, Port 18772 (200k) + D2-Wegwerf 18768 wiederverwendet, Standing-Permission-Muster reproduziert; P8-22 4/5 Kriterien erfuellt -- ein ehrlicher Fail (Settle-Zeit 5.95 s statt < 3 s, ALPHA_DECAY-getrieben, nicht knotenanzahl-getrieben, Frame-p50 16.7 ms, also 60 fps nicht compute-bound); P8-24 5/6 Stationen bestanden -- ein ehrlicher Fail (Knotenklick oeffnet das Item nicht, weil graph.js keinen Klick-nach-Item-Pfad hat; plus Nebenfund P8-15 Foreign-Farbe unerreichbar, weil _graph_get shared := space != own setzt); drei Befunde wandern in Plan §9.4.6 (P8-22, P8-15, P8-20/24); §7-Matrix-Statuszeilen P8-22 und P8-24 jetzt mit Beleg statt "nicht gefahren"/"existiert nicht"; Bilanz 15-10-0 (15 gruen/10 gelb/0 offen); Screenshots docs/screenshots/p8_22_01/02 + p8_24_01..03; phase1_storage/CLAUDE.md §Geerbte Contracts: achte P1-Contract-Oeffnung GESCHLOSSEN (im selben Commit, gemass der Anweisung in Plan §9.6 -- Schliessungsbeleg: 13 B2-index-Tests gruen, Charakterisierung byte-identisch); Phase-Head jetzt 89.3KB, weiterhin ueber 40KB-Softcap benannt, Rotation wuerde nichts bewegen; 958/958 pytest unveraendert (kein Python-Touch), ui_budget 5/5 unveraendert (kein Static-Bundle-Touch), Tabu-Diff §0.4 weiterhin leer, Service-Touch 0, Wegwerf sauber abgebaut, Produktion unangetastet (uptime 23348 s linear wachsend), kein Push, kein Deploy) | 2026-09-02 (Nikinger-Bestaetigung "UI is fixed now" -- Start von Step Z (Phase-8-Closeout); Vorstufe in dieser Sitzung: ## Abnahmestand-Body durch §7-Matrix-Tabelle ersetzt (26 Zeilen, Spalten #/Kriterium/Status/Beleg), Sichtpruefungs-Status-Tabelle (Plan §8), Bilanz 15-9-2 (15 gruen/9 gelb/2 offen), §9-Bedarfsliste mit 200-Knoten-Wegwerf (P8-22) + kombiniertem E2E-Smoke (P8-24) + Nikinger-Sichtpruefung am echten Geraet (P8-14/15/16/18/19/23) + drei Restdefekten (A3-Klammer, Item-Link-Picker-Body, Picker-A11y); "Anhang: Step-Z-Vorstufe" an die bestehende Session-Block angehaengt; keine Code-Aenderung, keine Python-Datei angefasst, 958/958 pytest unveraendert (nicht erneut gemessen, weil kein Test-Delta moeglich), ui_budget 5/5 unveraendert (kein Static-Bundle-Touch), Tabu-Diff §0.4 weiterhin leer, Service-Touch 0, kein Push; Phase-Head jetzt mit dieser Vorstufe allein aktuell) | 2026-09-02 (Nikinger-Freigabe der Outline-Fassung ("yes, that fits great") plus zwei weitere Auftraege im selben Zuruf: (1) Rundung nachgezogen -- border-radius: var(--radius-sm) auf beiden Listenzeilen-Selektoren ergaenzt, outline folgt dem radius in modernen Browsern, Nikinger-Beobachtung zum Rail-Button-Vorbild bestaetigt; (2) Sweep "Standard ueberall" -- dritte, bisher unangetastete Implementierung gefunden (.link-picker-results li[aria-selected=true] + li:hover/:focus, Item-Link-Picker), auf denselben Gradient+Outline+Radius-Standard gehoben, dabei nebenbei einen nie definierten --accent-text-Token entfernt (var() auf undefiniertes Custom-Property, fiel lautlos auf geerbte Farbe zurueck); Nebenfund dokumentiert, nicht behoben: aria-selected wird im Picker nie per JS gesetzt (keine Tastaturnavigation trotz role=listbox/option) -- A11y-Vormerkung, kein Auftrag dieser Session; zwei Screenshots neu (Listenzeile gerundet, Link-Picker-Hover im neuen Stil), Rail-Button-Referenz aus vorhandenem 03_list.png (Code unveraendert); 7/7 Playwright, 958/958 pytest, ui_budget 5/5 (124.2 KB), Tabu-Diff leer) | 2026-09-02 (Vormerkung 3 Punkt 1 nachgeschaerft nach Nikinger-Sichtung des ersten Wurfs -- "remove the left solid line and add the outline I can see around the Notizen Auswahl"; border-left-Einfaerbung auf beiden Selektoren entfernt (Reservierung im Boxmodell bleibt), outline: 1px solid var(--accent-line); outline-offset: -1px neu, Kombi-Override um outline:none ergaenzt; Gradient-Fill + Gloss-Highlight unveraendert (schon als "nearly it" bestaetigt); c4c5_playwright_smoke.py Schritt 1+3 erneut umgeschrieben (Abwesenheit border-left-color, Anwesenheit outline 1px solid var(--accent-line), computed im Browser gegengeprueft); 7/7 Playwright, 958/958 pytest, ui_budget 5/5 (123.9 KB, +-0 KB), Tabu-Diff leer; Screenshot aktualisiert, Vormerkungs-ERLEDIGT-Notiz + README-Bildunterschrift korrigiert; kein Service-Touch, kein Push) | 2026-09-02 (Vormerkung 3 Punkt 1 gebaut -- Listenzeilen-Auswahl-Fill vereinheitlicht auf denselben Rail-Button-Gradient wie .rail__home[aria-current=true] (loest --accent-quiet-Flaeche + schwimmende -4px-Outline + Backdrop-Blur ab, alles ersatzlos entfernt), 3px-Akzentrand links unveraendert, Kombi-Override neu (aria-current + selected gleichzeitig); Playwright-Smoke umgeschrieben -- Unified-Nachweis jetzt per computed background-image-Gleichheit gegen den Rail-Button, nicht nur Vorhandensein; Screenshot c4c5_02_selected_row_3px_outline.png -> c4c5_02_selected_row_accent_fill.png (alter Name behauptete abgeloestes CSS-Merkmal); 7/7 Playwright, 958/958 pytest, ui_budget 5/5 (123.8 KB, -0.1 KB), Tabu-Diff leer; Selection/Choice-Konvention-v3-Abschnitt korrigiert (der dort dokumentierte Kategorien-Einwand ist per Nikinger-Weisung ueberstimmt, nicht widerlegt); README Sneak-Peak-Zeile + Bild nachgezogen; kein Service-Touch, kein Push) | 2026-09-02 (Zwei Vormerkungen ergaenzt, nur dokumentiert, kein Code: (1) Item-Link-Picker fuellt nur das Frontmatter-links-Feld fuer den Graphen, kein Pfad zu einem klickbaren #item/-Link im Body -- Fix-Vorschlag notiert; (2) Nikinger-Handyscreenshot-Vergleich Rail-Bucket vs. Listenzeilen-Auswahl bestaetigt die Richtung-(a)-Entscheidung mit Bildbeleg, keine neue Entscheidung) | 2026-09-02 (Deploy-Diskrepanz geschlossen -- Nikinger hat den haengenden Restart durchgefuehrt, Block B jetzt tatsaechlich live, Health-Gate 3/3 gruen, Retention hat 20260821T183341.270842Z abgeraeumt; Block C/D weiterhin nicht deployt) | 2026-09-02 (Nikinger-Entscheidung Vormerkung 3 Punkt 1: Richtung (a) vereinheitlichen zugunsten Rail-Button-Stil -- "looks cleaner", dokumentiert vor dem Push, Umsetzung offen fuer naechste Session; README Sneak-Peak um die zwei Chevron-Screenshots ergaenzt) | 2026-09-02 (Vormerkung-3-Fixes: Chevron em-skaliert (Root Cause .field .input font-size:13px) + select.input:focus links/rechts entkoppelt, 11/11 Playwright-Regression gruen, 958/958 pytest, ui_budget 5/5 (123.7/250 KB); Escalation-Deploy-Fund dokumentiert (deploy.sh main haengt seit 2026-09-01 an sudo, Live-PID 67925 noch auf 7254aa9/A3, NICHT auf 007b73d/Block B trotz gegenteiliger Doku-Behauptung) | 2026-09-02 (Vormerkung 3 vom 2026-09-02 ergaenzt: Nikinger-Feedback nach Chevron-Sichtpruefung -- Chevrons nicht visuell identisch ueber alle 7+1 Stellen (Hypothese: 12px vs Container-Hoehe, --text-faint-Kontrast auf Glas vs Solid), +linker input-Border-Strich konkurriert mit dem neuen Chevron-Affordance rechts; drei Loesungsrichtungen jeweils benannt, ausdruecklich NUR vormerken, kein Edit in dieser Session) | 2026-09-02 (Selection/Choice Konvention v3 im Phase-Head dokumentiert + Auswahl-Chevron-Vorbild in app.css ::select.input gebaut -- Lucide m6 9 6 6 6-6 als data-URL, --text-faint-Stroke, 12x12 rechtsbuendig, padding-right 28px, :disabled-Variante in --text-placeholder; alle 7+1 <select class="input">-Stellen gerendert (field-status, create-type, new-folder-parent-select, move-space-select, move-folder-select, space-member-write-select, Per-Item-Share-Row dynamisch); Playwright-Smoke 9/9 gruen gegen Wegwerf 18771; ui_budget 5/5 (123.3/250 KB, +0.6 KB), 958/958 pytest, Tabu-Diff §0.4 leer, JS-Syntax OK; phase8_ui_graph/scripts/{wegwerf_setup_auswahl_chevron.py,auswahl_chevron_playwright_smoke.py} neu; docs/screenshots/auswahl_chevron_{01_move,02_share}_dialog.png neu; kein Service-Touch, kein Deploy, kein Push; Vormerkung 1 vom 2026-09-01 (Auswahl-Boxen vereinheitlichen) damit erledigt -- die Selection/Choice-Konvention ersetzt die offene Frage, das Chevron-Vorbild schliesst die sichtbare Luecke im Vorbild; Vormerkung 2 vom 2026-09-02 (Listenzeilen-Sheen vs Rail-Button-Stil) bewusst NICHT aufgeloest -- der C4-Sheen bleibt unvera (ge 3px-Akzentkante + Outline + Backdrop-Blur) wegen N8 (Auswahl darf nicht allein von Transparenz abhaengen); Obsidian-Uebersicht (D2) bleibt WIP wie vom Nikinger bestaetigt -- keine Code-Aenderung an js/graph.js, app.css/app.html fuer das Graph-Panel) | 2026-09-02 (Vormerkung-Block ergaenzt: Nikinger-Feedback nach Sichtpruefung 3 -- Listenzeilen-Auswahl (c4c5_03) sieht anders aus als Rail-Button-Vorbild (03_list.png), drei Loesungsrichtungen fuer die naechste kontrollierte UI-Session vereinheitlichen / vereinfachen / bewusst unterschiedlich lassen; Obsidian-Uebersicht weiterhin WIP, explizit bestaetigt; kein Code angefasst, kein Push noetig) | 2026-09-02 (Block C C4+C5 gebaut: Liquid-Glas-Akzente (P8-H/N8, --glass-{bg,border,blur,highlight}-Tokens + .glass-Utility mit Fallback+@supports+prefers-reduced-transparency), .list__head sticky (position:sticky;top:0;z-index:1) + .overlay__panel/.update-banner/.toast ueber gruppierte Selektor-Liste am Dateiende auf Glas, Auswahl-Sheen fuer .list__row[aria-current=true] und .list__row--selected (3px solide Akzentkante + 1px Outline + backdrop-blur Sheen); C5: ::selection (Akzent-quiet/Text), .editor__textarea max-width:72ch + margin:0 auto (576px computed in Plex Mono, symmetrische Margins), .editor__body padding-left auf calc(var(--space)*1.5) Token; phase8_ui_graph/scripts/{wegwerf_setup_c4c5.py,c4c5_playwright_smoke.py} neu (Port 18770, Standing-Permission-Muster D1/D2 reproduziert, File-Keyring, 7 Items ueber zwei Spaces); Playwright-Smoke 7/7 gruen (CSS-Static + sticky head + 3px border + outline + 72ch centered + ::selection rule + overlay glass rgba(27,32,39,0.55)); vier Screenshots docs/screenshots/c4c5_{01..04}_*.png; 958/958 pytest, ui_budget 5/5 gruen (122.7/250 KB, +2.9 KB), Tabu-Diff §0.4 leer, JS-Syntax node --check auf app/list/state/tree.js OK; kein Code ausserhalb webui/static + phase8_ui_graph/scripts beruehrt; Produktion unangetastet, kein Deploy, kein Service-Touch) | 2026-09-02 (Block D D3 gebaut: Versions-Bump .rail__version v2.2.3 -> v3.0, neuer docs/UPDATE_LOG.md-Eintrag 2026-09-02 mit vier Bullet-Points (Uebersicht tabellos, Verknuepfungs-Graph, globaler Home-Scope, Mini-Legende); Sichtpruefung 2 mit 26 Items ueber drei Spaces via phase8_ui_graph/scripts/{wegwerf_setup_sichtpruefung2.py,sichtpruefung2_smoke.py} (Standing-Permission-Muster reproduziert, Port 18769, File-Keyring, User alpha + drei Spaces alpha/beta/gamma via Store.create mit folder-Support statt space_cli); sechs Screenshots docs/screenshots/sp2_{01..06}_*.png; README.md Sneak-Peak-Sektion komplett ersetzt (neun Block-C-Screenshots raus, sechs Block-D-Screenshots rein, 3x2-Tabelle, Hinweis-Text ueber die historische Referenz); D2-Block rotiert; Head jetzt mit D3-Block allein ueber 40KB-Softcap benannt; 958/958 pytest, ui_budget 5/5 gruen (119.8/250 KB unveraendert), Tabu-Diff §0.4 leer; kein Service-Touch, PID 67925 uptime 66891s linear wachsend) | 2026-09-02 (Block D D2 gebaut: handgerollter Canvas-Force-Graph in js/graph.js (542 Zeilen, 6.2 KB gzipped), Force-Simulation mit O(n^2)-Repulsion + Federkraft + Alpha-Decay, Canvas 2D mit devicePixelRatio-Korrektur, Knotenfaerbung via spaceCategory() aus C3, Kantenstile explizit solide / Tag gestrichelt / Ordner gepunktet, Hover-Dim, Klick -> Editor.selectItem, Drag/Zoom/Pan, prefers-reduced-motion synchron 300 Ticks; Toggles Tags/Ordner mit Default aus, >15-Knoten-Cutoff-Riegel fuer Tag-Cliquen; app.html-Graph-Panel erweitert (Toolbar + Empty-Hint), app.css fuer Toolbar + Empty-Hint, app.js initGraph() in Init-Kette + loadGraphPanel() an drei Stellen (Init/Home/Refresh); phase8_ui_graph/scripts/{wegwerf_setup_d2.py,d2_playwright_smoke.py} neu -- Standing-Permission-Muster C3/D1 reproduziert, eigener Port 18768, File-Keyring-Backend, 14 Items (10 alpha + 4 beta) mit 6 expliziten Kanten (4 Frontmatter + 2 Body); Playwright-Smoke 7/7 gruen -- statisches Markup korrekt, Login + Overview rendert Graph-Panel, /api/v1/graph liefert 14 Knoten/6 Kanten, Empty-Hint versteckt wenn Kanten existieren, Tag-Toggle erweitert sichtbar, Zoom-Readout aktiv, Canvas mit >=500 nicht-transparenten Pixeln; zwei Screenshots docs/screenshots/d2_{01_overview_with_graph,02_graph_with_tag_toggle}.png; D1-Block rotiert; Head jetzt mit D2-Block allein ueber Softcap benannt (Rotation wuerde nichts bewegen); 958/958 pytest (vorher/nachher identisch, keine Python-Aenderung), ui_budget 5/5 gruen (119.8/250 KB, +6.8 KB), Tabu-Diff §0.4 leer (Storage nicht beruehrt, achte Oeffnung bleibt ANGEKUENDIGT), JS-Syntax node --check auf graph.js/app.js OK; kein Code ausserhalb webui/static + phase8_ui_graph/scripts beruehrt; Produktion unangetastet, PID 67925 uptime 66363s linear wachsend) | 2026-09-02 (Block D D1 gebaut: Uebersicht tabellos, app.html/app.css/list.js/app.js aktualisiert, Playwright-verifiziert gegen Wegwerf 18767, 5/5 gruen, drei Screenshots d1_{01..03}, 958/958 pytest, ui_budget 5/5 (113.0/250 KB), Tabu-Diff §0.4 leer, Head 41.8KB->44.4KB ueber Softcap benannt, C3-Block rotiert, kein Service-Touch, PID 67925 uptime 65157s linear wachsend) | 2026-09-01 (Vormerkung in phase8_ui_graph/CLAUDE.md ergaenzt: Auswahl-Boxen vereinheitlichen -- Space-Auswahlbox (Move-Dialog, <select class=input id=move-space-select>) als Standard; Nikinger-Sichtpruefung-1-Design-Frage mit 'nein, C3-C5 + D-Block noch offen' beantwortet; kein Code, kein Service-Touch; Head 33.6KB->37.5KB noch unter Softcap) | 2026-09-01 (Block C C2 gebaut: Lucide-Sprite-Vendoring (18 Icons, ISC+MIT-Lizenzen, phase5_ui/vendor/lucide/); Generator build_icon_sprite.py (idempotent, --check); Sprite-Block zwischen ICONS:BEGIN/ICONS:END in app.html (vom Generator gepflegt); js/icons.js (iconSvg()/iconHtml(), 13. JS-Modul); app.css .icon (Lucide-Defaults: 1.25em/currentColor/stroke-width 2) + .rail__glyph.icon (16px Badge-Box) + .toolbar-btn.icon (1em) + .tree__twist (12px SVG-Box); Ersetzungs-Map 7 HTML-Entities + 3 Text-Glyphen geschlossen (F9/F10/F11 aus C0); V92 gepinnt (Lucide 1.38.0, SHA-256 d28944cf…); ui_budget 5/5 (110.3/250 KB), pytest 958/958, Tabu-Diff leer, grep &#[0-9]+; in app.html → 0 Icon-Treffer, grep '→|⇄|×' in js/ → 0 Icon-Treffer (2 Treffer bleiben = Sprach-Interpunktion 'v3 → v4' mit Audit-Kommentar); Modul-Status Block C auf 'C0+C1+C2 gebaut, C3-C5 offen' + Abnahmestand um C2-Zeile ergaenzt + neuer Session-Block + C1-Block rotiert; Head 33KB->38KB, immer noch unter Softcap; kein Code ausserhalb webui/static + build_icon_sprite.py beruehrt) | 2026-09-01 (Block C C1 gebaut: C1a Font-Swap (Plex Sans Var v0.2.0 + Plex Mono v2.5.0, SHAs gepinnt, build_font_subset_plex.sh neu) + C1b CSS-Typografie (5 Skala-Tokens, body 16px/1.55, h1-h3 + Meta-Zeilen auf Tokens, IDs/Versions in --font-mono); zwei Commits (0281cce + 08bff55); ui_budget 5/5 (108.4/250 KB), pytest 958/958 (250s, Flake als isoliert bestaetigt), Tabu-Diff leer; phase8_ui_graph/CLAUDE.md Modul-Status Block C auf 'C0 + C1 gebaut, C2-C5 offen' gehoben + Abnahmestand um C1-Zeile ergaenzt + neuer Session-Block; Head 27.5KB->33KB, immer noch unter Softcap) | 2026-09-01 (Block C C0 gebaut: Anti-AI-Pattern-Research (V94 bestaetigt, Web-Recherche) + UI-Audit gegen den Code (P8-25); Findings-Tabelle Muster -> Fundstelle -> Fix -> Ziel-Step im Phase-Head, 35 Eintraege, davon 0 als eskaliert markiert; Code unberuehrt, vier Dateien Doku-only -- phase8_ui_graph/CLAUDE.md + SESSIONS_ARCHIVE.md + docs/INDEX.md + SESSIONS_ARCHIVE-Frontmatter; Head 18.4KB->27.5KB, immer noch unter Softcap) | 2026-09-01 (Gate B→C: 958/958 pytest gruen, Charakterisierung byte-identisch, Tabu-Diff leer, _graph_get manuell 12/12, Playwright gegen Wegwerf 18/18; B4-Block rotiert, Head 14.8KB unter Softcap; Code unberuehrt, Doku-Update + neuer Session-Block) | 2026-09-01 (Block B Step B1 gebaut -- storage/linkscan.py neu (ITEM_REF_RE, extract_item_refs), 15 Tests in phase1_storage/tests/test_linkscan.py, achte P1-Contract-Oeffnung in phase1_storage/CLAUDE.md angekuendigt vor Code, Tabu-Diff §0.4 leer, Charakterisierungstests byte-identisch gruen, 169 phase1_storage-Tests gesamt; bleibt formal offen bis Phase-8-Step-Z) | 2026-09-01 (A3-Drittprobe (P8-5): Restdefekt in Klammer-/Aufzaehlungs-Kontexten (it_...-ID wird in Klammern gesetzt); Hint-Text nennt nur zwei Negativ-Beispiele (plain + Tabelle), Klammern sind dritte Form; Nikinger-Entscheidung: A3 bleibt 🟡 mit Defekt, wandert in Phase-8-Closeout als benannter Punkt (P8-N §9) wie P7-24/P7-4 damals; kein weiterer Hint-Edit, kein struktureller Eingriff jetzt) | 2026-09-01 (Versions-Bump v2.2 -> v2.2.3 in app.html .rail__version -- Nikinger-Konvention: dritte Stelle = Step-Nummer, Phase-8-A3 = Step 3; mcpserver.__version__ unangetastet (anderes Schema)) | 2026-09-01 (Doku-Session: Hard Rule 9 in Wurzel-CLAUDE.md ergaenzt nach Phase-8-A3-Vorfall -- kein pkill -f mit Regex, niemals den systemd-Dienst anfassen; PROMPTS.md Hard-Rules-Liste und Tests-Absatz um Stopp-Regel fuer Wegwerf-Instanzen erweitert; docs/INDEX.md drei Zeilen vorne + drei Eintraege angepasst; kein Code, kein Service-Touch, Produktion weiterhin active, head 11.6KB->12.8KB unter Softcap) | 2026-09-01 (A3 gebaut -- _TITLE_NOT_ID_HINT mit Positiv/Negativ-Beispiel geschärft, Test test_tool_descriptions_tell_the_agent_to_name_titles_not_ids auf neuen Wortlaut angepasst, 143 phase2_mcp-Tests gruen, Zweitprobe vom Nikinger live bestaetigt (positiv), dritte Probe nach Deploy offen P8-5) | 2026-08-31 (A2 live-verifiziert -- Test_Space_A2 angelegt + entfernt, 4x GET /api/v1/overview nach DELETE=200 statt 500, Index konsistent mit Dateien, Push danach freigegeben; Block A vollstaendig live ✅) | 2026-08-31 (Nachtrag: Janick live angemeldet -- dritter biologischer Nutzer, Phase-4-Auth-Architektur erstmals mit externem Dritt-Anwender durchgespielt; Connector-UI-Befund: 'Anmeldung fehlgeschlagen' trotz erfolgreicher OAuth-Verbindung, kein Handlingsbedarf, Vormerkung fuer spaeter) | 2026-08-31 (Nachtrag: OpenAI-ChatGPT-Konnektor aktuell nicht kompatibel, benoetigte Settings unbekannt -- Auth-Architektur auf Anthropic-Konnektoren geeicht, andere Settings nicht hinterlegt, Vormerkung ohne Auftrag) | 2026-08-31 (Block A: A2 remove-space-Auto-Reindex gebaut -- spacectl._cmd_remove_space nach remove_space_dir mit store.rebuild_index(), Test beweist keine Karteileichen + keine Kollateralschäden, 913 gruen, Live-Verifikation ausstehend) | 2026-08-31 (Block A: A1 Reauth-Grant Client gebaut -- async runBatchMove + Grant-Round-2, test #3 auf N=14, Browser-Smoke gegen Wegwerf bestanden, Head rotiert, Live-Verifikation ausstehend) | 2026-08-28 (Block A gestartet -- A1 Reauth-Grant Backend gebaut, 912 Tests gruen, Plan-Drift session_id->session_hash + Throttle-Vorzug dokumentiert, JS-Client ausstehend) | 2026-08-28 (Nachtrag: websearch-MCP nachgerüstet -- @zhafron/mcp-web-search, kein API-Key, Live-Probe bestanden, V94 von nein auf ja) | 2026-08-28 (Step 0 abgeschlossen -- opencode-ai 1.18.25 global installiert, Minimax-Provider-Auth vom Nikinger gesetzt, Playwright-MCP verbunden (V93), CLAUDE.md-Regeldatei-Kontrollfrage bestanden, Smoke-Test P8-26 auf Wegwerf-Branch bestanden, Harnesswechsel zu opencode/M3 ab Block A freigegeben) | 2026-08-28 (Skelett angelegt, Step 0 Fundament-Session gestartet)
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

**Statusregel unverändert (P5/P6/P6.5/P7):** ✅ = live-verifiziert durch den Nikinger gegen
`main`, 🟡 = gebaut + Code/Playwright-Beleg ohne Live-Verify, ⬜ = offen. (W) = Wegwerf-Instanz
reicht, (L) = nur live, (C) = Code/Test reicht. **Drei benannte Restdefekte wandern in den
Closeout (§9):** A3 Klammer-/Aufzählungs-Kontext (P8-5), Item-Link-Picker füllt nur
Frontmatter (Vormerkung), A11y `aria-selected` im Link-Picker nie per JS gesetzt
(Nebenfund 2026-09-02).

### §7 Abnahmematrix-Stand — P8-1 bis P8-26

| # | Kriterium (Kurzform) | Status | Beleg |
|---|---|---|---|
| P8-1 (L) | Batch-Verschieben ≥2 rechteerweiternde Items mit genau 1× Passwort+TOTP (P7-24) | ✅ | A1 `90441b29`, N=14-Batch live-verifiziert |
| P8-2 (C) | TOTP-Code 2× → 2. Request abgelehnt (Anti-Replay-Regression) | ✅ | A1 — `reauth.py`-Tests (Idempotenz) + Nikinger-Probe `Test_Space` |
| P8-3 (C) | Abgelaufenes/fremdes Grant → Re-Auth-Fehler; Throttle | ✅ | A1 — `reauth.py`-Tests (`expired_grant`, Throttle-Decorator) |
| P8-4 (W) | `spacectl.py remove-space` → 4× overview 200, Index konsistent | ✅ | A2 `90441b29`, Nikinger-Probe `Test_Space_A2` (Live-Remove, keine Karteileichen) |
| P8-5 (L) | P7-4-Zweitprobe dokumentiert; nach Deploy dritte Probe | 🟡 | A3 ✅ Zweitprobe (positiv); **Klammer-/Aufzählungs-Kontext nennt weiterhin `itm_…`-ID** — Hint deckt zwei Negativ-Beispiele (plain + Tabelle), Klammern sind dritte Form; 3. Probe post-deploy |
| P8-6 (W) | `links:`-Frontmatter UND `itm_`-Body-Ref erscheinen beide als Kante | ✅ | B2 `f4c8844` + B3 `58ff9a6`, Graph-Payload `edges` enthält Frontmatter- UND Body-Kanten (`linkscan.py` extrahiert beide Quellen) |
| P8-7 (C) | `rebuild_index()` rekonstruiert `item_links` vollständig nach Index-Löschung | ✅ | B2 — 13 B2-index-Tests grün, Charakterisierung byte-identisch |
| P8-8 (L) | Nicht-lesbares Item weder als Knoten noch als Kantenende (Zweitnutzer) | 🟡 | B3 _graph_get testet ACL (zweiter Space, gewollte `share_read`-Items, eigenes vs. fremdes Home); **echter Zweitnutzer-Pass-Through-Smoke mit zwei realen Tokens gegen die laufende Instanz steht aus** |
| P8-9 (W) | `#item/…`-Klick öffnet Ziel-Item | ✅ | B4 `ea14d53`, Playwright 18/18 gegen Wegwerf 18768 (`#item/`-Klick-Delegation in `app.js:107-115`) |
| P8-10 (W) | Link-Picker findet per Titelsuche + befüllt `links:` | ✅ | B4, gleicher Playwright-Lauf, Link-Picker-Smoke `b4_*` |
| P8-11 (C) | `test_characterization.py` byte-identisch grün | ✅ | jede Block-Session seit B1 einzeln verifiziert (Tabu-Diff §0.4-Linie + Charakterisierungsblock als Disziplin gehalten) |
| P8-12 (C) | Tabu-Diff (§0.4) leer bis auf die A3-Textänderung | ✅ | A3-Edit am `_TITLE_NOT_ID_HINT` war die einzige bewusste Ausnahme; keine in P8-L gelockte Verletzung |
| P8-13 (C) | 0 Icon-Entities in `app.html`, 0 `→`/`⇄`/`×` in `js/`; `THIRD_PARTY_LICENSES.md` | ✅ | C2-Smoke — `grep` ergibt 0 Icon-Treffer (zwei verbleibende `→`-Treffer = Sprach-Interpunktion „v3 → v4" mit Audit-Kommentar, keine Icons) |
| P8-14 (L) | Plex 16px Schriftbild, Nikinger bestätigt am echten Gerät | 🟡 | C1 ✅ gebaut + 9 Screenshots Sichtprüfung 1; „UI is fixed now" deutet Sichtprüfung 1 als akzeptiert — formaler Nikinger-Lauf am echten Gerät gegen den v3.0-Build steht aus |
| P8-15 (L) | Farblegende (own/shared/foreign) konsistent in Rail, Liste (globaler Scope), Übersicht, Graph | 🟡 | C3 ✅ gebaut + `c3_01`/`c3_02`-Screenshots; **D1 hat die Übersicht um Counter-Chips erweitert — Konsistenz in der „tabellosen Zeile" zu prüfen am echten Gerät** |
| P8-16 (W) | Glass-Fallback bei deaktiviertem `backdrop-filter` / `prefers-reduced-transparency` solide, Auswahl erkennbar | 🟡 | C4 ✅ gebaut + `@media (prefers-reduced-transparency: reduce)`-Block in `app.css` (c4c5_smoke prüft Anwesenheit der Regel); **empirischer Browser-Lauf mit umgeschaltetem UA (`prefers-reduced-transparency: reduce`) + Overlay-Klickprobe steht aus** |
| P8-17 (C) | `ui_budget.py` 5/5 grün (Fonts + Sprite + `graph.js`) | ✅ | 124.2/250 KB zuletzt gemessen am 2026-09-02 (Vormerkung 3 Punkt 1 ERLEDIGT) |
| P8-18 (L) | Übersicht tablos: Space-Zeilen mit klickbaren Zählern, Graph eingebettet, „Zuletzt benutzt" vorhanden, keine Deko-Kacheln | 🟡 | D1 ✅ gebaut + Playwright 5/5 gegen Wegwerf 18767 + 3 Screenshots `d1_{01..03}`; **Nikinger-Sichtprüfung am echten Gerät (Sichtprüfung 2)** |
| P8-19 (L) | Übersicht öffnen → globaler „Alle Items"-Scope in Listen-Spalte | 🟡 | D1, gleicher Smoke, V82 explizit getestet (Home-Klick im bereits-globalen Scope ist idempotent) |
| P8-20 (W) | Graph: Hover dimmt Nicht-Nachbarn, Klick öffnet das Item, Drag/Zoom/Pan funktioniert | 🟡 | D2 ✅ gebaut + d2_playwright_smoke 7/7 (Markup, Login, `/api/v1/graph`, Tag-Toggle, Zoom-Readout, Canvas-Pixel); **Klick-öffnet-Item + Drag/Zoom/Pan sind Code-Invarianten ohne explizite Browser-Assertion** — Screenshots `d2_*` zeigen sie, automatischer Beweis fehlt |
| P8-21 (W) | Tag-/Ordner-Toggles wirken; Default nur explizite Kanten; >15-Knoten-Tag → keine Clique | 🟡 | D2 ✅ gebaut + d2_smoke (Tag-Toggle ON erweitert sichtbar, >15-Knoten-Cutoff-Riegel in Code); **Ordner-Toggle + Cutoff-Empirik im Browser stehen aus** |
| P8-22 (W) | 200-Knoten-Wegwerf-Datensatz: Simulation kommt < 3 s zur Ruhe, Interaktion ohne Hakeln; `prefers-reduced-motion` rendert statisch | 🟡 | **200-Knoten-Wegwerf-Setup + Smoke gebaut** (`phase8_ui_graph/scripts/wegwerf_setup_200knoten.py`, `p8_22_smoke.py`, Port 18772, Standing-Permission-Muster reproduziert); **4/5 Kriterien erfüllt** (Interaktion ohne Hakeln: hover p95 0.4 ms / drag p95 0.3 ms / wheel p95 0.4 ms; Tag-Toggle mit >15-Riegel wirkt; `prefers-reduced-motion` rendert statisch mit 0 graph.js-Frames); **Settle-Zeit 5.95 s statt < 3 s** — `graph.js` braucht 351 Ticks (ALPHA_DECAY 0.985 bis ALPHA_MIN 0.005), Frame-Abstand p50 16.7 ms (60 fps, nicht compute-bound), Befund dokumentiert in Plan §9.4.6 |
| P8-23 (L) | `v3.0`-Badge live, UPDATE_LOG-Eintrag vorhanden, Health-Gate 3/3 nach Deploy | 🟡 | D3 ✅ alles vorbereitet (`.rail__version` v3.0 in `app.html`; `docs/UPDATE_LOG.md` oberster Eintrag 2026-09-02 mit vier Bullet-Points: Übersicht tabellos, Verknüpfungs-Graph, globaler Home-Scope, Mini-Legende); **Deploy + Live-Verifikation stehen aus** (Hard-Rule-konform: Nikinger-Aktion) |
| P8-24 (W) | Playwright-Durchlauf gegen Wegwerf: Übersicht → Scope → Graph → Knotenklick → Item | 🟡 | **kombinierter End-to-End-Smoke gebaut** (`phase8_ui_graph/scripts/phase8_e2e_smoke.py`, default D2-Wegwerf 18768, `--base`/`--root` für jede andere Instanz); **5/6 Stationen bestanden** (Login · Uebersicht tabellos · globaler Scope idempotent · Graph gezeichnet · Hover dimmt Nicht-Nachbarn von 280 auf 103 voll deckende Pixel); **Knotenklick → Item fehlt** — `graph.js` importiert `selectItem` nicht, `onMouseDown`/`onMouseUp` setzen nur Drag/Pan, der "Klick öffnet das Item"-Pfad existiert im Code nicht (Doku behauptet ihn, Plan §5 D2 / Phase-Head D2-Block); Befund in Plan §9.4.7 |
| P8-25 (C) | C0-Findings-Tabelle existiert im Phase-Head; jeder Fund auf Step gemappt oder als benannte Nikinger-Entscheidung eskaliert | ✅ | Tabelle in §C0 (35 Einträge, 0 eskaliert, alle auf C1–C5/D1 gemappt oder bereits aligned) |
| P8-26 (W) | Fundament: opencode steuert nachweislich einen Browser gegen eine Wegwerf-Instanz (Smoke-Test 0.8) | ✅ | Step 0 abgeschlossen, V93 erfüllt (opencode-Setup inkl. Playwright-MCP) |

### Sichtprüfungs-Status (Plan §8)

| Sichtprüfung | Status | Notiz |
|---|---|---|
| Sichtprüfung 1 (Plan §8, nach C1+C2) | 🟡 | 9 Screenshots vorliegen (Plex Sans + Mono + Lucide-Icons), Inline-Bewertung „UI is fixed now" deutet Sichtprüfung als akzeptiert; formaler Lauf am echten Gerät offen |
| Sichtprüfung 2 (Plan §8, in D) | 🟡 | 26-Item/3-Space-Wegwerf-Setup 18769, 6 Screenshots `sp2_*`; **echtes Gerät + Live-Build (v3.0 inkl. D) steht aus** |
| Sichtprüfung 3 (Plan §8, nach C4+C5) | 🟡 | 4 Screenshots `c4c5_*`; „UI is fixed now" vorläufige Bestätigung, formal offen am echten Gerät |

### Bilanz (Stand 2026-09-02, vor Step-Z-Deploy)

**15 ✅ · 9 🟡 · 2 ⬜** von 26 Zeilen.

- **15 ✅:** P8-1, P8-2, P8-3, P8-4 (Block A); P8-6, P8-7 (Block B Indexseite); P8-9,
  P8-10 (Block B UI); P8-11, P8-12, P8-13 (Block B/C Constraints); P8-17 (Budget-Test);
  P8-25 (C0-Audit); P8-26 (Smoke-Fundament).
- **10 🟡:** P8-5 (A3 Restdefekt), P8-8 (B3 Zweitnutzer-Pass-Through fehlt),
  P8-14/15/16 (C1–C5 Sichtprüfungen am echten Gerät), P8-18/19 (D1 Sichtprüfung 2),
  P8-20/21 (D2 Drag/Cutoff ohne Browser-Assertion), P8-22 (Settle-Zeit 5.95 s statt < 3 s),
  P8-23 (D3 vorbereitet, post-deploy), P8-24 (Knotenklick → Item fehlt im Code).
- **1 ⬜:** keine mehr.

**Was §9 (Phase-8-Closeout, P8-N) noch braucht (gesammelt, keine Auslagerung in diese
Sitzung):**

- **Nikinger-Sichtprüfungslauf am echten Gerät** gegen den dann deployten v3.0-Build für
  P8-14, P8-15, P8-16, P8-18, P8-19, P8-23.
- **§9-Restdefektabschnitt** mit den drei benannten Punkten (A3 Klammer/Aufzählung,
  Item-Link-Picker-Body-Lücke, Picker-A11y `aria-selected`) plus den drei aus den Smokes
  (P8-22 Settle-Zeit, P8-15 Foreign-Farbe unerreichbar, P8-20/24 Knotenklick).
- **Phase-Status Glyphe** (✅/🟡) — Nikinger-Entscheidung nach Live-Deploy + Sichtprüfung.

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

   **[2026-09-02 ENTSCHIEDEN, Nikinger nach Sichtung der Chevron-Fix-Screenshots]:**
   Richtung **(a) vereinheitlichen** — „i like the rail Button Style more, Looks cleaner."
   Ziel: die C4-Auswahl-Sheen (3-px-Akzentkante links + 1-px-Outline + Backdrop-Blur auf
   `.list__row[aria-current=true]`/`.list__row--selected`) wird zugunsten des Rail-Button-
   Stils (solider Akzent-Fill, siehe `.rail__bucket.active` o. ä.) abgelöst — **nicht**
   umgekehrt. **Bewusst nur dokumentiert, noch nicht gebaut** (Nikinger-Auftrag: „Note that
   before pushing", kein Baubefehl) — Umsetzung berührt N8 (Auswahl darf nicht allein von
   Transparenz abhängen) neu, weil ein solider Fill diese Anforderung ohnehin einfacher
   erfüllt als die Glass-Sheen; das ist bei der Umsetzung zu prüfen, nicht diese Session.
   Damit ist Vormerkung 3 Punkt 1 vollständig entschieden — Umsetzung offen für die nächste
   Session.

   **[2026-09-02 ERLEDIGT]:** `.list__row[aria-current="true"]` und
   `.list__rows > li.list__row--selected` (`phase5_ui/webui/static/app.css`) tragen jetzt
   denselben Gradient + Gloss-Highlight wie `.rail__home[aria-current="true"]`
   (`linear-gradient(180deg, rgba(62,141,243,.20), rgba(62,141,243,.08))` +
   `box-shadow: inset 0 1px 0 rgba(255,255,255,.06)`) — Playwright-Smoke vergleicht
   computed `background-image` beider Elemente auf Gleichheit, nicht nur auf Vorhandensein
   (`c4c5_playwright_smoke.py :: step3_selected_row_styles`). `outline`/`outline-offset` und
   beide `backdrop-filter`-Blöcke (Blur-Sheen, `prefers-reduced-transparency`-Fallback) sind
   komplett entfernt. Der 3px-Akzentrand links bleibt unverändert (kein Layout-Shift, `.list__row`s
   Default-Border bleibt 3px transparent). N8 geprüft: einfacher erfüllt als vorher, weil die
   Erkennbarkeit jetzt an einem opaken Gradient + dem soliden Rand hängt, kein Blur mehr im
   Spiel — der `@media prefers-reduced-transparency`-Sonderfall entfällt strukturell. Bewusst
   minimaler Diff (Advisor-Fund vor dem Bauen): `.list__row` blieb bei `border-left`, bekam
   **keinen** vollen `border: 1px solid transparent` wie `.rail__home` — ein Listenrow ist
   randlos volle Breite, ein voller Rand hätte jede Zeile 2px schmaler/höher gemacht (globale
   Dichte-Änderung) für einen Fund, der nur den *Fill* betraf. 7/7 Playwright-Smoke grün gegen
   Wegwerf 18770, 958/958 pytest, ui_budget 5/5 (123.8 KB, −0.1 KB). Details im Session-Block.

   **[2026-09-02 Nachtrag, nachgeschärft nach Nikinger-Sichtung dieses ersten Wurfs]:** der
   3px-Akzentrand links oben ist wieder raus — Nikinger-Feedback auf die beiden Screenshots:
   „remove the left solid line and add the outline I can see around the Notizen Auswahl."
   `border-left-color` faerbt sich nirgends mehr ein (das reservierte `3px solid transparent`
   im Boxmodell bleibt, damit sich die Zeilenbreite nicht ändert); neu ist ein umlaufender
   `outline: 1px solid var(--accent-line); outline-offset: -1px;` auf beiden Selektoren —
   derselbe Farbton, den der Rail-Button für seinen `border-color` benutzt, nur als `outline`
   statt `border` (layoutneutral, derselbe Grund wie beim ursprünglichen Verzicht auf einen
   echten 4-seitigen `border`). Gradient-Fill + Gloss-Highlight unverändert (bereits vom
   Nikinger als „nearly it" bestätigt). 7/7 Playwright grün (Assertions umgeschrieben:
   Abwesenheit von `border-left-color`, Anwesenheit von `outline: 1px solid
   var(--accent-line)`), 958/958 pytest, ui_budget 5/5 (123.9 KB, ±0 KB). Details im
   Nachtrag zum Session-Block.

   **[2026-09-02 Nachtrag, zwei eigene Handy-Screenshots als Vergleichsbeleg]:** Nikinger
   liefert ein direktes Vorher-Nachher-Paar aus der laufenden App (kein Playwright-Shot):
   Rail-Bucket „Notizen" aktiv (voller Akzent-Fill, klar als „ausgewählt" lesbar) gegen die
   Listenzeile „Aufgabe fuer morgen" ausgewählt (nur ein dünner blauer Rahmen um die Box,
   auf dem Screenshot kaum wahrnehmbar). O-Ton: „That's Not nearly the same." Bestätigt die
   Richtung (a)-Entscheidung oben mit Bildbeleg — **keine neue Entscheidung**, verstärkt nur
   die bereits gelockte. Kein Code angefasst, Screenshots nicht ins Repo übernommen (Ad-hoc-
   Handyaufnahmen, kein Playwright-Artefakt, gehören nicht in `docs/screenshots/`).

2. **„Obsidian Übersicht" weiterhin WIP, vom Nikinger ausdrücklich bestätigt.** Block D
   (tabellose Übersicht mit Counter-Chips + handgerollter Canvas-Force-Graph) ist gebaut
   und liegt in `c4c5_01`, `sp2_01`–`sp2_06` und `d1_*`/`d2_*` vor. Nikinger sagt: „ja, klar
   dass die noch Überarbeitung braucht" — **keine neue Anforderung**, nur eine Bestätigung
   des erwarteten Stands. Soll im selben kontrollierten UI-Lauf mit auf den Schirm.

**[2026-09-02] Nikinger-Feedback nach Sichtprüfung der Chevron-Screenshots (diese Session,
ausdrücklich nur vormerken, nichts davon umgesetzt):**

1. **Chevrons nicht identisch.** Die Lucide-Chevrons auf den 7+1 `<select class="input">`-
   Stellen sind visuell nicht identisch. Hypothese (nicht im Code verifiziert): die
   Chevron-Größe 12 px ist relativ zur Select-Höhe unterschiedlich (Item-Editor-Status
   vs. Move-Dialog-Select), und/oder die Data-URL rendert je nach Container-Background
   anders — die `--text-faint`-Farbe (`#A7B2BF`) wurde gegen die `--surface-raised`-Fläche
   (1B2027) designt, der Move-Dialog-Select sitzt aber auf `.overlay__panel`-Glas
   (`rgba(27,32,39,.55)`), was den Kontrast verändert. **Mögliche Richtungen für die
   nächste UI-Session:** (a) Chevron-Größe relativ zur Schriftgröße (`em` statt `px`),
   (b) Farbe explizit auf `--text` statt `--text-faint` (konservativer, mehr Gewicht),
   (c) eine eigene CSS-Klasse `.input--chevron` einführen, falls die Data-URL-Variante
   grundsätzlich nicht trägt. Verifikation dann mit drei Screenshots (Item-Editor,
   Move-Dialog, Space-Verwaltung) im selben Layout.

2. **Linker „Strich" von der alten Auswahl überlappt mit der neuen Auswahl.** Beobachtung
   am Move-Dialog-Screenshot: der `<select class="input">` zeigt seinen eigenen
   `1px solid var(--line-strong)`-Border rundum, und im `:focus`-Zustand wechselt der
   gesamte Border auf `var(--accent-line)` (`.input:focus`,` `app.css:280`); der linke
   Border-Strich bleibt damit sichtbar und tritt in Konkurrenz zum Chevron-Affordance
   auf der rechten Seite. **Lesart 1:** der linke Border ist als „alte" Auswahl gelesen
   worden (C4-Sheen-Kontext, dort hat die ausgewählte Listenzeile eine 3-px-Akzentkante
   links) — der User assoziiert linke Akzentkante mit „etwas ist ausgewählt" und sieht
   sie nun auch am `<select>`, was nicht zur Semantik passt. **Lesart 2:** der Border
   links ist einfach visuell zu prominent im Verhältnis zum Chevron. **Mögliche
   Richtungen:** (a) `.input:focus`-Regel so anpassen, dass nur der untere und rechte
   Rand auf `--accent-line` wechseln, nicht der linke (machtet konsistent mit der
   Chevron-Affordance rechts), (b) Border-Stärke am `<select>` von 1 px auf 0.5 px
   reduzieren oder ganz wegnehmen (Glas-Träger-Konsistenz aus C4), (c) Chevron visuell
   stärker betonen, damit die linke Linie nicht mehr dagegen konkurriert. **Achtung:**
   Lesart 1 darf NICHT den `.input:focus` global ändern — `<input type="text">` und
   `<input type="date">` brauchen den vollen Focus-Border für Tastatur-Navigation
   (Sichtbarkeit des Caret). Änderung muss `<select>`-spezifisch bleiben.

   **[2026-09-02 ERLEDIGT, beide Punkte, Details im Session-Block]:** Punkt 1 Richtung (a)
   umgesetzt (Chevron-Größe/-Position/`padding-right` von px auf `em` — Root Cause war
   `.field .input { font-size: 13px; }`, `app.css:1251`, die den Wert-Kontext von
   `#field-status` gegenüber den 16px-Dialogen verkürzt, während der Chevron fest 12px blieb).
   Punkt 2 Richtung (a) umgesetzt (`select.input:focus` eigene Regel, nur rechts/unten auf
   `--accent-line`, links bleibt `--line-strong` — `.input:focus` selbst unangetastet, Achtung
   aus Lesart 1 eingehalten). Playwright-Regressionscheck gegen Wegwerf 18771 bestätigt beide
   Fixes empirisch (Verhältnis-Differenz 0.0096, Border-Asymmetrie exakt auf den erwarteten
   Token-Werten). **Damit bleibt aus Vormerkung 3 nur noch Punkt 1 des 2026-09-02-Blocks
   offen** (Listenzeilen-Sheen vs. Rail-Button-Vorbild — bewusst NICHT angefasst, das ist eine
   Geschmacksfrage für die Nikinger-Sichtprüfung am echten Gerät, kein Bug mit auffindbarer
   Root Cause wie die zwei Chevron-Funde hier).

**[2026-09-02] Nikinger-Frage „wie erstellt man anklickbare Item-Links in sharefyx" —
Recherche ergab eine echte Lücke, ausdrücklich nur vormerken, kein Code angefasst:**

Drei Mechanismen existieren nebeneinander und werden leicht verwechselt:

1. **🔗-Symbol in der Formatierleiste** (`editor.js` `TOOLBAR_ACTIONS.link`) — blinder
   Markdown-Schnipsel `[Linktext](Ziel-URL)` an der Cursor-Position, kennt keine Items.
2. **Link-Picker-Knopf** (Büroklammer-Symbol im Kopfdaten-Panel, `editor.js:88-100
   _appendLinkId`, Phase 8 Block B Step B4) — öffnet eine Item-Suche, hängt die gewählte
   `itm_…`-ID an das **Frontmatter-Feld `links:`** an (Komma-Konvention). Dient
   ausschließlich dem Verknüpfungs-Graphen (`linkscan.py` liest dieses Feld für
   Graph-Kanten) — wird **nirgends als Text oder Link gerendert**.
3. **Echter klickbarer Link im Body:** `[Text](#item/itm_xxxxxxxx)`, von Hand getippt.
   Erst `markdownToHtml`/`safeHref` (`markdown.js`) rendert das in der Vorschau zu einem
   echten `<a href="#item/itm_...">`; `app.js:107-115` hat die Klick-Delegation, die dann
   zum Item navigiert.

**Befund:** kein Weg führt heute von (2) nach (3) — der Picker liefert die ID nie an eine
Stelle, von der sie in den Body eingefügt werden könnte. Wer heute einen klickbaren
Item-Link will, muss die Ziel-ID von Hand kennen und `[Text](#item/itm_xxxxxxxx)` selbst
tippen; der Picker suggeriert optisch „ich verlinke", tut das aber nur für den Graphen, nicht
für den Text. **Nikinger-Auftrag: nur vormerken, nicht bauen.** Naheliegender Fix für eine
spätere Session: `_appendLinkId`s Callback um eine Variante erweitern, die
`[<Item-Titel>](#item/<id>)` an der Cursor-Position in `#editor-textarea` einfügt (statt/
zusätzlich zum Frontmatter-Feld) — kein neuer Endpunkt nötig, der Picker kennt Titel+ID
bereits aus seinem Suchergebnis.

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

- **[2026-09-02 Korrektur]** Der Absatz unten stand hier als Momentaufnahme der Sitzung vom
  2026-09-01/-02 und ist überholt: der Nikinger hat die dort verworfene Vereinheitlichung am
  2026-09-02 explizit angeordnet (Vormerkung 3 Punkt 1, Richtung (a), „i like the rail Button
  Style more, Looks cleaner") und sie ist seither gebaut (`app.css`, Session-Block unten). Der
  ursprüngliche Kategorien-Einwand (Listenzeilen-Auswahl = eigene Kategorie, keine Vermischung
  mit Navigation) ist damit per direkter Nikinger-Weisung überstimmt, nicht als falsch
  widerlegt — bewusst als Ausnahme dokumentiert, keine neue Kategorisierungsregel. Die
  **Farbsprache** (Rail-Button-Gradient) ist jetzt identisch, die **Markup-Kategorien** selbst
  (Choice/Toggle/Status/Navigation, Tabelle oben) bleiben unverändert — eine Listenzeile ist
  weiterhin keine Navigation, sie sieht nur jetzt optisch genauso aus wie eine. Ursprünglicher
  Text, unverändert stehen gelassen als Herkunftsnachweis der verworfenen Position:
  *„Sie ändert nichts am Listenzeilen-Sheen aus C4 (3-px-Akzentkante + 1-px-Outline +
  Backdrop-Blur-Sheen) — Vormerkung 2 vom 2026-09-02 (Sichtprüfung 3) hatte drei mögliche
  Richtungen benannt; diese Sitzung hat keine davon umgesetzt, weil der Sheen durch N8
  begründet ist (Auswahl darf nicht allein von Transparenz abhängen, sonst bei
  prefers-reduced-transparency: reduce unsichtbar). Eine Vereinheitlichung mit dem
  Rail-Button-Akzent-Gradient-Fill (Navigation-Kategorie) wäre aus Sicht des Servers eine
  Vermischung zweier Kategorien — semantisch falsch."* N8 selbst ist weiterhin erfüllt, siehe
  die Vormerkung-3-Punkt-1-ERLEDIGT-Notiz oben — der neue Fill ist opak, hängt an keinem Blur.
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

## Session stopped — 2026-09-02 (Vormerkung 3 Punkt 1 gebaut: Listenzeilen-Fill vereinheitlicht)

**Auftrag:** Nikinger-Anweisung „Go on with the UI fix". Die gelockte Entscheidung aus der
vorigen Session (Vormerkung 3 Punkt 1, Richtung (a): Listenzeilen-Auswahl auf den
Rail-Button-Akzent-Fill umstellen, „Umsetzung offen für die nächste Session") ist die einzige
Vormerkung mit Bauauftrag — der zweite offene Punkt aus der letzten Doku-Sitzung
(Item-Link-Picker-Lücke) trägt explizit „nur vormerken, nicht bauen" und blieb unangetastet.

**Umgesetzt (eine Datei, `phase5_ui/webui/static/app.css`, minimaler Diff — Advisor-Fund vor
dem Bauen: keine `.list__row`-Basis-Border-Umstellung auf volle 4-Seiten-Border wie beim
Rail-Button, das hätte jede Zeile global 2px schmaler/höher gemacht für einen Fund, der nur
den *Fill* betraf):**

- `.list__row[aria-current="true"]` und `.list__rows > li.list__row--selected`: `background`
  von `var(--accent-quiet)` (flach, 14% Deckkraft) auf denselben Gradient wie
  `.rail__home[aria-current="true"]` (`linear-gradient(180deg, rgba(62,141,243,.20),
  rgba(62,141,243,.08))`), plus `box-shadow: inset 0 1px 0 rgba(255,255,255,.06)` (Gloss-
  Highlight, ebenfalls vom Rail-Button übernommen).
- `outline: 1px solid var(--accent)` + `outline-offset: -4px` ersatzlos entfernt — das war laut
  Nikingers Handyscreenshot-Vergleich die „kaum wahrnehmbare" schwimmende Innenkante.
- Beide `@supports (backdrop-filter)`- und `@media (prefers-reduced-transparency)`-Blöcke für
  beide Selektoren ersatzlos entfernt — der neue Fill ist opak, hängt an keinem Blur mehr.
- 3px-Akzentrand links (`border-left`) unverändert stehen gelassen (kein Layout-Shift, war
  nicht Teil des gemeldeten Befunds).
- Kombi-Zustand (Zeile gleichzeitig `aria-current` UND mehrfach-`selected`) bekommt eine neue
  Override-Regel (`.list__rows > li.list__row--selected .list__row[aria-current="true"] {
  background: none; box-shadow: none; }`), analog zur bestehenden `border-left-color:
  transparent`-Regel eine Zeile darüber — verhindert, dass sich zwei identische Gradienten
  sichtbar aufaddieren.
- Netto-Diff: −20/+9 Zeilen App-CSS.

**N8-Prüfung (Verbotsliste §0.3 Punkt 6, „Auswahl darf nicht allein von Transparenz
abhängen") — wie von der Nikinger-Entscheidung selbst verlangt, vor dem Bauen geprüft, nicht
nur behauptet:** einfacher erfüllt als vorher. Der alte Sheen hatte drei Layer, von denen einer
(Backdrop-Blur) tatsächlich transparenzabhängig war und deshalb einen eigenen
`prefers-reduced-transparency`-Fallback brauchte; der neue Fill ist ein einziger opaker
Gradient plus der ohnehin schon soliden Akzentkante — kein Fallback-Fall mehr, weil kein
Blur mehr existiert, der ausfallen könnte.

**Playwright-Regression (`c4c5_playwright_smoke.py`, gegen dieselbe Wegwerf-Kategorie 18770,
die den beanstandeten Screenshot erzeugt hatte — Standing Permission, `wegwerf_setup_c4c5.py`
neu provisioniert, vorheriger `/tmp`-Stand war bereits aufgeräumt):**

- Step 1 (CSS-statisch) umgeschrieben: prüft jetzt Gradient-Fill-Präsenz auf beiden Selektoren
  UND die **Abwesenheit** jeder `outline`-Deklaration in beiden Regelblöcken UND zählt den
  exakten Gradient-String ≥3× im Dateikörper (Rail-Home + beide Listenzeilen-Selektoren) als
  Unified-Nachweis.
- Step 3 (computed Styles im Browser) umgeschrieben: liest jetzt `background-image` +
  `box-shadow` der ausgewählten Zeile UND von `.rail__home`/`.tree__scope`/`.tree__folder` (je
  nachdem, was gerade `aria-current="true"` trägt) und **vergleicht beide computed
  `background-image`-Werte auf exakte Gleichheit** — das ist der eigentliche Beweis für
  „vereinheitlicht", nicht nur „ein Gradient ist da".
- Screenshot umbenannt: `c4c5_02_selected_row_3px_outline.png` (Git-getrackt, per `git rm
  --cached` entfernt) → `c4c5_02_selected_row_accent_fill.png` (neu aufgenommen) — der alte
  Name behauptete ein CSS-Merkmal, das es nicht mehr gibt.
- **7/7 grün**, inklusive der neuen Gleichheits-Assertion (nicht nur „Gradient vorhanden",
  sondern „identisch mit dem Rail-Button-Vorbild").

**Verifikation — Selbstprüf-Checkliste §0.6:**

1. `pytest -q` → **958/958 grün** (270 s, reiner CSS-Diff, keine Python-Änderung).
2. Tabu-Diff (`storage/`, `mcpserver/{tools,permissions,server}.py`) → **leer**.
3. JS-Syntax: kein JS geändert, `node --check app.js`/`list.js` zur Sicherheit trotzdem grün.
4. Doc-Update im selben Commit: dieser Block + Vormerkung-3-Punkt-1-ERLEDIGT-Nachtrag +
   Korrektur der jetzt widersprüchlichen „Was diese Konvention NICHT macht"-Aussage (Selection/
   Choice Konvention v3, siehe oben — Advisor-Fund: die Konvention hatte den jetzt überstimmten
   Kategorien-Einwand noch als geltende Position stehen) + `README.md` Sneak-Peak-Zeile +
   Frontmatter.
5. `ui_budget.py` → **5/5 grün**, app.js+css+Font **123.8 KB** (vorher 123.9 KB — netto **−0.1
   KB**, weniger CSS als vorher trotz der neuen Kombi-Override-Regel).

**Wegwerf abgebaut:** `wegwerf_setup_c4c5.py cleanup` (PID-Datei-Muster, kein `pkill -f`).
`curl http://127.0.0.1:8765/health` → `{"status":"ok",...}`, `ps -ef` zeigt danach nur noch
`sharefyx-mcp.service` — kein Service-Touch an der echten Instanz.

**Was diese Session bewusst NICHT gemacht hat:**

- **Item-Link-Picker-Lücke unangetastet.** Trägt „Nikinger-Auftrag: nur vormerken, nicht
  bauen" — kein Code, kein `editor.js`-Edit.
- **Kein `deploy.sh`/`sudo`/`systemctl`-Kontakt.** Der Live-Dienst läuft weiterhin auf Block B
  (`007b73d`); dieser Fix ist einer von jetzt 21 Commits seit dem letzten Release-Build, geht
  erst mit dem nächsten, vom Nikinger ausgelösten `deploy.sh main` live.
- **Kein Push.** Lokaler Commit, keine Weiterleitung an `origin/main`.
- ~~**Keine `.list__row`-Basis-Border-Umstellung** (siehe Begründung oben, Advisor-Fund vor
  dem Bauen) — bewusst kein 1:1-Literalport des Rail-Button-Markups, nur der Fill wurde
  übernommen.~~ **[2026-09-02 Nachtrag, siehe unten]** Nikinger hat den ersten Wurf gesehen
  und explizit nachgeschärft — der linke Akzentrand sollte weg, der umlaufende Rand (den er am
  Rail-Button „Notizen" sah) sollte rein. `outline` statt `border` gebaut (layoutneutral,
  derselbe Grund wie beim ursprünglichen Advisor-Einwand gegen einen echten 4-seitigen
  `border`), kein Widerspruch zur ursprünglichen Begründung — nur eine andere CSS-Eigenschaft
  für dasselbe Ziel (kein Layout-Shift).

**Nachtrag, 2026-09-02, nach Nikinger-Sichtung des ersten Wurfs (zwei Screenshots, „That's
nearly it: remove the left solid line and add the outline I can see around the Notizen
Auswahl. That should do it."):**

- `.list__row[aria-current="true"]` und `.list__rows > li.list__row--selected` verlieren die
  `border-left-color`/`border-left`-Einfärbung komplett (der linke Rand bleibt strukturell im
  Boxmodell reserviert — `border-left: 3px solid transparent` auf `.list__row`s Basis bleibt
  unverändert, sonst würde sich die Zeilenbreite für ALLE Zeilen um 3px ändern, nicht nur für
  die ausgewählte — aber es wird nirgends mehr eingefärbt).
- Neu: `outline: 1px solid var(--accent-line); outline-offset: -1px;` auf beiden Selektoren —
  derselbe Farbton, den `.rail__home[aria-current="true"]`/`.tree__scope[aria-current="true"]`
  für ihren `border-color` benutzen (Zeile ~402), nur als `outline` statt `border`, weil
  Outline layoutneutral ist (nimmt keinen Platz im Boxmodell weg — derselbe Grund, aus dem der
  Advisor vor dem ersten Wurf von einem echten 4-seitigen `border` auf `.list__row` abgeraten
  hatte; das Ziel „Rail-Button-Optik ohne Layout-Shift" bleibt identisch, nur der Mechanismus
  hat gewechselt). `outline-offset: -1px` statt der ursprünglichen `-4px` aus dem alten Sheen —
  knapp an der Kante, nicht mehr „schwimmend".
- Kombi-Override (Zeile gleichzeitig `aria-current` UND mehrfach-`selected`) um `outline: none;`
  ergänzt, aus demselben Grund wie schon `background`/`box-shadow`: zwei gestapelte Outlines
  (li + inneres `.list__row`) sähen wie ein doppelt dicker Rahmen aus.
- `c4c5_playwright_smoke.py` Step 1 + Step 3 umgeschrieben: prüft jetzt explizit die
  **Abwesenheit** jeder `border-left-color`/`border-left`-Einfärbung UND die **Anwesenheit**
  von `outline: 1px solid var(--accent-line)` auf beiden Selektoren — computed
  `outlineStyle`/`outlineWidth`/`outlineColor` im Browser gegengeprüft, nicht nur der
  CSS-Quelltext.
- Neuer Screenshot (`c4c5_02_selected_row_accent_fill.png`, gleicher Dateiname, Inhalt
  aktualisiert) zeigt: kein linker Strich mehr, dünner blauer Rahmen um die gesamte Zeile,
  visuell dem Rail-Button-Vorbild sehr nahe.
- **7/7 Playwright grün** (inkl. der neuen Abwesenheits-/Anwesenheits-Assertions),
  **958/958 pytest**, **ui_budget 5/5 (123.9 KB, ±0 KB gegenüber der ersten Fassung)**,
  Tabu-Diff leer.
- Wegwerf erneut sauber abgebaut (`cleanup`, PID-Datei-Muster), echte Instanz währenddessen
  ununterbrochen erreichbar (`/health` vor und nach dem Lauf geprüft).

**Verbleibend für die nächste Session:**

- **Nikinger-Sichtprüfung 3** (echtes Gerät) — Chevron-Fixes + Border-Fix (vorige Session) UND
  jetzt der zweifach nachgeschärfte Listenzeilen-Fill (diese Session, beide Fassungen) sind
  alle bereit zur Begutachtung.
- **Sichtprüfung 2** (D3) weiterhin am echten Gerät ausstehend.
- **Zweiter Deploy** für Block C/D (21+ Commits seit `007b73d`) bleibt ein eigener, späterer,
  vom Nikinger ausgelöster Schritt — nicht vor Step Z fällig.
- **Item-Link-Picker-Fix** bleibt Vormerkung ohne Bauauftrag, siehe oben.

**Nachtrag, 2026-09-02, dritter Wurf (Rundung + „Standard überall" nach Freigabe der Outline-
Fassung, „yes, that fits great"):** zwei weitere Nikinger-Aufträge im selben Zuruf.

1. **Rundung nachgezogen.** Nikinger-Beobachtung stimmte: `.rail__home`/`.tree__folder`/
   `.tree__scope` tragen als Basisklasse `border-radius: var(--radius-sm)` (Zeile ~387), meine
   Outline-Fassung vom Vortag hatte keine — sie rendere eckig. `border-radius:
   var(--radius-sm)` auf `.list__row[aria-current="true"]` und
   `.list__rows > li.list__row--selected` ergänzt. Moderne Browser (Chromium/Firefox seit
   90/88) lassen `outline` dem `border-radius` der Box folgen, kein Zusatzaufwand nötig —
   im Playwright-Screenshot bestätigt, kein separater Assertion-Bedarf (rein visuell, `outline`
   ist per Spec radius-folgend, kein Browser-Support-Risiko in der Chromium-Testumgebung).
2. **Sweep „Standard überall wo Auswahl vorkommt" durchgeführt.** `grep` auf `aria-current`/
   `aria-selected` über `app.css`/`app.html`/`js/*.js` fand genau drei Implementierungen: die
   beiden bereits gefixten (Listenzeile einzeln + mehrfach) und eine dritte, bisher
   unangetastete — `.link-picker-results li[aria-selected="true"]` (Item-Link-Picker,
   Phase 8 Block B Step B4) sowie ihr `li:hover`/`li:focus`-Pendant, beide mit demselben alten
   Muster: solides `background: var(--accent-line)` + `color: var(--accent-text)`. **Auf den
   neuen Standard gehoben** (Gradient-Fill + `outline: 1px solid var(--accent-line);
   outline-offset: -1px;` + `border-radius: var(--radius-sm)`), Fund nebenbei: `--accent-text`
   war **nirgends definiert** (kein Treffer in `:root`) — ein `var()` auf ein undefiniertes
   Custom-Property macht die `color`-Deklaration ungültig, der Browser fällt lautlos auf die
   geerbte Textfarbe zurück. War seit dem B4-Bau (2026-09-01) so, nie aufgefallen, weil die
   geerbte Farbe zufällig gut genug aussah. Beim Angleichen entfernt statt fortgeschleppt —
   kein separater Fix-Commit nötig, war ohnehin dieselbe Codezeile.
   **Nebenfund, nicht behoben (out of scope):** `li[aria-selected="true"]` wird im gesamten
   `dialogs.js` **nie** per JS gesetzt — keine `ArrowUp`/`ArrowDown`-Tastaturnavigation im
   Picker trotz `role="listbox"`/`role="option"`-Markup. Die CSS-Regel ist also aktuell tote,
   nie erreichte Auswahl-Logik; nur `li:hover`/`li:focus` ist real erreichbar (Maus). Keine
   Tastatur-Navigation zu bauen war kein Teil dieses Auftrags — vormerken für eine spätere
   A11y-Passage, nicht in dieser Session ergänzt.
3. **Screenshots für die Sichtprüfung:** `c4c5_02_selected_row_accent_fill.png` neu (gerundete
   Outline, Listenzeile „Erste Notiz"), `c4c5_07_link_picker_hover.png` neu (Link-Picker-Dialog,
   Treffer „Geteilte Notiz eins" im Hover-Zustand mit demselben Fill+Outline+Radius). Als
   Rail-Button-Referenz zum Vergleich dient das bereits vorhandene `03_list.png` (Sichtprüfung
   1) — der `.tree__folder[aria-current="true"]`-Code selbst wurde in dieser Session nicht
   angefasst, ein frischer Screenshot hätte nichts Neues gezeigt; zwei eigene Versuche, einen
   engen Rail-Button-Ausschnitt frisch zu greifen, scheiterten an einem Navigationssprung nach
   dem Klick (Bucket-Klick wechselt in die gefilterte Listenansicht, Baum kollabiert auf die
   schmale Icon-Rail) — verworfen statt einen irreführenden Screenshot zu committen.
4. **Verifikation:** 7/7 Playwright (`c4c5_playwright_smoke.py`, unverändert seit dem
   Outline-Nachtrag — die Rundung/den Link-Picker prüft kein Assertion, nur der Screenshot),
   958/958 pytest, ui_budget 5/5 (**124.2 KB**, +0.3 KB gegenüber der Outline-Fassung — zwei
   neue CSS-Regeln + drei `border-radius`-Ergänzungen), Tabu-Diff leer. Wegwerf sauber
   abgebaut, echte Instanz durchgehend erreichbar.

---

**Anhang: Step-Z-Vorstufe — §7-Abnahmematrix-Tabelle konsolidiert (2026-09-02).**
Nikinger-Bestätigung „UI is fixed now" → der nächste offene Punkt der Phase ist der
Phase-8-Closeout (Step Z, Plan §6). Davor: die §7-Tabelle als kanonische Form in diesem Head
konsolidiert — bisher nur als Fließtext-Zusammenfassung der Block-Commits vorhanden (Zeilen
73–131 alt, jetzt durch die Tabelle oben ersetzt). **Was diese atomare Sitzung tat, ein
einziger Doku-Commit (Hard Rule 8 eingehalten — Phase-Head aktualisiert im selben Commit,
wie der Plan es für jeden Step vorsieht):**

1. **`## Abnahmestand`-Body ersetzt** durch eine §7-Matrix mit 26 Zeilen, Spalten
   `# / Kriterium (Kurzform) / Status / Beleg` — die Status-Spalte ist die kanonische Form
   für §9 (Closeout) und für jede künftige Sichtprüfung am echten Gerät. Fließtext-Zusammen-
   fassungen je Block wandern nicht in die §7-Matrix; sie bleiben im Archiv (`SESSIONS_ARCHIVE.md`
   Zeilen 49/243/404/538/685/817/914/1175/…) und sind dort versioniert nachschlagbar.
2. **Sichtprüfungs-Tabelle** (Plan §8): drei Prüfpunkte mit aktuellem 🟡-Status + Notiz.
3. **Bilanz-Abschnitt:** **15 ✅ · 9 🟡 · 2 ⬜ von 26** mit Aufschlüsselung nach Block und
   expliziter Liste der drei Status-Cluster.
4. **§9-Bedarfsliste** (gesammelt, **nicht** in dieser Sitzung abgearbeitet — siehe unten,
   „bewusst NICHT gemacht"):
   - 200-Knoten-Wegwerf-Fixture + Smoke-Lauf für P8-22.
   - Kombinierter `phase8_e2e_smoke.py` für P8-24.
   - Nikinger-Sichtprüfungslauf am echten Gerät gegen den v3.0-Build für P8-14/15/16/18/19/23.
   - §9-Abschnitt mit den drei benannten Restdefekten.
   - Phase-Status-Glyphe (✅/🟡) als Nikinger-Entscheidung nach Live-Deploy + Sichtprüfung.
5. **Frontmatter-`updated:`** mit einem neuen Eintrag vorne (Datums-Prefix 2026-09-02).

**Verifikation:** keine Python- oder JS-Datei angefasst — `pytest -q` bleibt 958/958 grün
(diese Sitzung ändert nichts an der Testbasis). `ui_budget.py` 5/5 nicht erneut gemessen,
da nichts im statischen CSS/JS-Bundle geändert wurde (Größe bleibt bei 124.2/250 KB, zuletzt
gemessen am 2026-09-02 nach Vormerkung 3 Punkt 1 ERLEDIGT). **Tabu-Diff §0.4** weiterhin
leer (kein `storage/`-, `mcpserver/`- oder `webui/static/`-Touch). **Service-Touch:**
keiner, kein Deploy, kein `systemctl`-Kontakt.

**Bewusst NICHT gemacht** (atomar, „pause after one item" als diesmaliger Modus):

- **Live-Deploy von Block C+D (P8-K) bleibt Nikinger-Aktion.** 21+ Commits seit `007b73d`
  (Block B live) liegen lokal gestapelt; das nächste `deploy.sh main` ist seine Aktion
  (Hard Rule: niemals `systemctl restart/sharefyx-mcp`, niemals `sudo deploy.sh` aus dem
  `savefyx`-User). Die Vorlagen für den Deploy-Block sind alle bereit — UPDATE_LOG-Eintrag
  2026-09-02 mit v3.0-Inhalt (D3), Health-Gate 3/3 beim letzten Live-Deploy.
- **§9 des Plans gefüllt** wäre der nächste logische Sub-Punkt von Step Z, aber zwei davon
  (§7-Tabelle konsolidiert jetzt + §9 füllen nächste) wären zwei Items, das verstößt gegen
  die diesmalige Anweisung „atomic, pause after one".
- **P8-22 (200-Knoten-Fixture) und P8-24 (kombinierter E2E-Smoke)** als eigenständige
  Wegwerf-Setups mit Skripten, eigenem Port, eigenem Fixtures-Stand: substanzielle
  Skript-Arbeit, nicht dieselbe eine Datei wie diese Vorstufe.
- **A8-Sweep** (Walkthrough der ungeprüften Vormerkungen mit Restdefekt-Konsolidierung in
  der „Was §9 noch braucht"-Liste): ist durch die Bilanz-Tabelle bereits erfasst; keine
  weiteren Findings heute.
- **Keine Push.** Lokaler Commit, bleibt liegen bis zum nächsten deploy-Bündel oder bis
  Nikinger die Tabelle abgenickt hat (er kann sie als eigenständigen Doc-Commit pushen, das
  ist unabhängig vom UI-Block-C+D-Deploy möglich).

---

**Anhang: Step-Z-Fortsetzung — P8-22 (200-Knoten-Wegwerf + Smoke) + P8-24 (kombinierter E2E-Ritt) gebaut (2026-09-02).**

Nikinger-Entscheidung A aus der Frage dieser Sitzung: „Nur Smokes committen, Lücken als
benannte Defekte." Plus die zweite Entscheidung: „§9 des Plans (aus der vorigen Session
uncommitted) und die achte P1-Contract-Öffnung in `phase1_storage/CLAUDE.md` im selben
Commit erledigen." Beides in einem Commit, kein eigener Doc-Commit dazwischen.

**Drei neue Skripte** unter `phase8_ui_graph/scripts/`:

- `wegwerf_setup_200knoten.py` — Standing-Permission-Muster aus C3/D1/D2 reproduziert,
  eigener Port 18772, File-Keyring-Backend, 200 Items (alpha 120 own / beta 50 shared
  mit `--write` / gamma 30 foreign mit `--read`), Ring-Links mit Schrittweite 7 (ggT(7,200)=1,
  ein einziger zusammenhängender Ring), Tag-Verteilung mit drei Sorten: `last-200` auf allen
  200 Knoten (muss vom >15-Riegel geschluckt werden), `gruppe-NN` auf ~17 Knoten pro Gruppe
  (ebenfalls darüber), `spitze` auf genau 5 Knoten (10 Paare, muss durchkommen) — der
  >15-Riegel (`TAG_CLIQUE_LIMIT = 15` in `js/graph.js`, P8-21) wird damit empirisch prüfbar.
  Anlege-Zeit 5.6 s, Verlinken 6.9 s, 200 store.create + 200 store.update (git-Commits
  eingeschlossen, ohne ging es in ~2 s).
- `p8_22_smoke.py` — Playwright gegen den 200-Knoten-Wegwerf. **Vier Designentscheidungen,
  die das Ergebnis prägen:**
  1. Kriterien werden gesammelt, nicht beim ersten Fail abgebrochen — ein Lastlauf, der
     nach der ersten gerissenen Schwelle abbricht, liefert kein vollständiges Messbild
     (Interaktionslatenz und reduced-motion-Pfad sind unabhängig von der Settle-Zeit).
     Infrastruktur (kein Canvas, kein Login, leeres Bild) bleibt hartes `assert`.
  2. **rAF-Instrumentierung mit Stack-Trace-Filter** (nicht nur Zähler) — Playwrights eigenes
     `wait_for_function` pollt per `requestAnimationFrame`, und ohne die Trennung zählte
     der reduced-motion-Test 168 statt 0 Frames. Das war das Messwerkzeug, nicht die App.
     Nach dem Fix: 0 graph.js-Frames bei reduced-motion, 170 fremde Frames = Playwright.
  3. Nullpunkt der Settle-Messung ist der **erste Animationsframe** (`__rafLog.stamps[0]`),
     nicht der Start der Funktion — sonst zählte die Login-/Navigationszeit mit, oder ein
     bereits fertig gelaufener Graph ginge als „sofort ruhig" durch.
  4. Knotenmittelpunkte aus den **Canvas-Pixeln** zurückgewonnen (die drei Knotenfarben
     aus `js/graph.js :: COLORS` sind eindeutig gegen die Kantenfarbe `#7E8A98`) — kein
     Eingriff in `graph.js` (das Modul privatisiert `nodes`/`alpha`/`rafId`).
  5. Vor der Knotensuche: Hover lösen (Maus in die Ecke bewegen) und Ansicht per Doppelklick
     zurücksetzen (`onDoubleClick`) — sonst dimmen Nicht-Nachbarn mit `globalAlpha=0.15`
     und die Farberkennung findet sie nicht; nach Wheel-Zoom driftet der Bildausschnitt.
- `phase8_e2e_smoke.py` — `--base`/`--root` für jede Wegwerf-Instanz, default D2-Wegwerf
  18768. Sechs Stationen in einer einzigen Sitzung: Login → Uebersicht tabellos → globaler
  Scope (V82-Idempotenz) → Graph gezeichnet → Hover dimmt Nicht-Nachbarn → Knotenklick →
  Item. TOTP-Anti-Replay-Schutz im zweiten Login: `_login()` schläft, bis der Generator
  einen neuen Code liefert, sonst fällt der Login still auf `/ui/login` zurück.

**P8-22-Bilanz, 4/5 Kriterien erfüllt:**

| Kriterium | Ergebnis |
|---|---|
| Simulation kommt < 3 s zur Ruhe | **FAIL** — 5.95 s (gemessen 5 951 ms nach erstem Animationsframe); 351 Ticks in 5 820 ms, Frame-p50 16.7 ms (60 fps, nicht compute-bound); `ALPHA_START 1 * 0.985^n < ALPHA_MIN 0.005` ⇒ n=351, bei 60 fps ~5.85 s. **Befund:** der Kommentarkopf von `graph.js` behauptet „200 Knoten erreichen Ruhe in <3s" — das ist damit widerlegt. |
| Interaktion ohne Hakeln (60 hover / 30 drag / 10 wheel) | OK — hover p95 0.4 ms / drag p95 0.3 ms / wheel p95 0.4 ms (60-fps-Budget 16.7 ms). |
| Tag-Toggle mit >15-Riegel (P8-21) | OK — Bild ändert sich, 10 `spitze`-Paare kommen hinzu, `last-200` (200) und `gruppe-NN` (~17) bleiben ausgeschlossen. |
| Interaktion ohne Hakeln mit Tag-Kanten | OK — hover p95 0.3 ms / drag p95 0.2 ms / wheel p95 0.3 ms. |
| `prefers-reduced-motion` rendert statisch | OK — 0 Animationsframes aus `graph.js`, 170 fremde Frames = Playwright-Polling, Canvas statisch bebildert, Hash über 600 ms unverändert. |

**P8-24-Bilanz, 5/6 Stationen bestanden:**

| Station | Ergebnis |
|---|---|
| 1 Login → `/ui/` | OK — Cookie-Session gegen den D2-Wegwerf. |
| 2 Uebersicht tabellos | OK — 2 Space-Zeilen, 4 Counter-Chips, 1 Legende, 0 alte Kacheln. |
| 3 Globaler Scope (V82 idempotent) | OK — Crumb „Alle Items", 14 Zeilen, zweiter Home-Klick ändert nichts. |
| 4 Graph gezeichnet | OK — 14 Knoten / 6 explizite Kanten, 14 im Bild, Empty-Hint versteckt. |
| 5 Hover dimmt Nicht-Nachbarn | OK — voll deckende Knotenpixel 277 → 85 (29 %). |
| 6 Knotenklick öffnet das Item | **FAIL** — kein Editor, kein Readonly-View, kein Titel. **Befund:** `js/graph.js` importiert `selectItem` nicht, `onMouseDown`/`onMouseUp` setzen nur Drag/Pan zurück, `grep -n selectItem js/*.js` findet Aufrufe in `app.js:122/213` und `list.js:111/355`, nie in `graph.js`. Die Behauptung „Klick → Editor.selectItem" im Phase-Head (D2-Block) und Plan §5 D2 hat im Code keine Entsprechung. |

**Zusätzlicher Befund (Nebenfund, nicht in P8-22 oder P8-24 enthalten, aber im selben Lauf entdeckt):**
`webui/api.py :: _graph_get` setzt `"shared": i.space != session.space` — und reicht das
an `state.js :: spaceCategory({ own, writable })` weiter, wo `writable` der zweite Parameter
ist. Damit ist **jeder fremde Knoten** „shared" (türkis); die dritte C3-Farbe (`--space-foreign`,
grau) ist im Graphen strukturell unerreichbar, obwohl die Legende sie anzeigt. P8-15
sollte diese Konsistenz am echten Gerät prüfen — der Datensatz liefert die nötige
Differenzierung, die Anzeige ignoriert sie.

**Verifikation:**

1. `pytest -q` → **958/958 grün** (256 s, keine Python-Datei in `storage/`/`mcpserver/`
   angefasst, Smoke-Skripte liegen unter `phase8_ui_graph/scripts/`).
2. `ui_budget.py` → **5/5 grün** (kein Static-Bundle-Touch, 124.2 KB wie zuletzt).
3. **Tabu-Diff** (`phase1_storage/storage/`, `mcpserver/{tools,permissions,server}.py`,
   `phase5_ui/webui/security.py`) → **leer**.
4. JS-Syntax: keine `.js`-Datei geändert, `node --check` zur Sicherheit auf
   `app.js`/`list.js`/`graph.js`/`dialogs.js`/`editor.js` — nicht ausgeführt (nicht nötig).
5. **Service-Touch:** keiner. Beide Wegwerf-Instanzen (D2 + 200-Knoten) sauber per
   `wegwerf_setup_* stop` (PID-Datei) abgebaut, `curl /health` auf 8765 zeigt die
   Live-Instanz ungestört (`uptime_s` 23 348 s linear wachsend). Kein `pkill -f`,
   kein `systemctl`, kein `sudo`.

**Bewusst NICHT gemacht (Nikinger-Entscheidung A):**

- **Kein Fix für P8-22 (Settle-Zeit).** `ALPHA_DECAY` in `graph.js` anpassen berührt
  Plan §5 D2 (gelockt) — eigene Nikinger-Entscheidung. Vererbt in Plan §9.4.6 als
  benannter Defekt mit der gemessenen Ursache.
- **Kein Fix für P8-20/24 (Knotenklick → Item).** `graph.js` braucht einen Klick-nach-Item-
  Pfad: neuer `onClick`-Branch in `onMouseUp` mit `hitTest()` + `selectItem`. ~5 Zeilen
  Produktionscode + ein neuer Test im E2E-Smoke. Vererbt in Plan §9.4.7.
- **Kein Fix für den P8-15-Nebenfund** (`shared` vs. `writable` in `_graph_get`). Drei
  Optionen in Plan §9.4.6: (a) `api.py` rechnet `writable` selbst aus
  (analog zu `webui/serializers.py :: overview_row_to_json`), (b) neue ACL-Pipeline
  analog zu `permissions.SharePolicy.can_write_item_as_human`, (c) als bewussten
  Modellierungs-Befund dokumentieren und die Legende auf zwei Farben reduzieren.
  Nikinger-Entscheidung.

**Screenshots:**

- `docs/screenshots/p8_22_01_200_knoten.png` — 200 Knoten im Ruhezustand (Hover-Reset
  davor, damit kein Dim-Effekt zu sehen ist), 98 sichtbare Knoten, 14 explizite Kanten
  im Bildausschnitt.
- `docs/screenshots/p8_22_02_reduced_motion.png` — statisch gerenderter Canvas mit
  `prefers-reduced-motion: reduce`, identische Pixel über 600 ms.
- `docs/screenshots/p8_24_01_uebersicht_graph.png` — Übersicht tabellos + Graph-Panel
  (D2-Wegwerf), globaler Scope aktiv.
- `docs/screenshots/p8_24_02_hover_dim.png` — Hover-Dim auf einem `beta`-Knoten (türkis),
  Nachbarn voll deckend, der Rest mit 0.15 alpha (kaum sichtbar im Screenshot — visueller
  Beleg, automatische Beweisführung steht im Kriterium-Output).
- `docs/screenshots/p8_24_03_nach_knotenklick.png` — nach dem Klick: dieselbe
  Übersichts-/Graph-Ansicht, weil der Klick-Pfad fehlt (Befund).

**Doku-Aktualisierungen im selben Commit (Hard Rule 8):**

- `phase8_ui_graph/CLAUDE.md` §7-Matrix: P8-22 und P8-24 mit Beleg statt „nicht gefahren"/
  „existiert nicht"; Bilanz 15-10-0; §9-Bedarfsliste um die drei Smoke-Funde gekürzt.
- `phase1_storage/CLAUDE.md` §Geerbte Contracts: achte P1-Contract-Öffnung GESCHLOSSEN
  mit Schließungsbeleg (13 B2-index-Tests grün, Charakterisierung byte-identisch), Frontmatter-
  Eintrag vorne.
- `docs/concepts/phase8_ui_graph_plan.md` §9.4.6 + §9.4.7: drei neue Restdefekte
  (Settle-Zeit, Foreign-Farbe, Knotenklick). §9.4.4 ist jetzt gegenstandslos — beide
  Substanz-Setups sind gebaut, beide Fund-Stellen dokumentiert.
- `docs/INDEX.md`: zwei Zeilen nachgezogen (Phase-8-Status 16/9/1 → 15/10/0, neuer
  `p8_22_smoke.py`/`phase8_e2e_smoke.py` Hinweis).

**Verbleibend für die nächste Session (unverändert):**

- **Nikinger-Sichtprüfung 2 + 3** am echten Gerät gegen den dann deployten v3.0-Build
  (P8-14, P8-15, P8-16, P8-18, P8-19, P8-23).
- **§9 des Plans** ist gefüllt (aus der vorigen Session uncommittet übernommen, die
  §9.4.6-§9.4.7-Erweiterungen sind neu in dieser Session); **Glyphe ✅/🟡** ist
  Nikinger-Entscheidung nach Live-Deploy.
- **A3 Klammer/Aufzählung** + **Item-Link-Picker-Body-Lücke** + **Picker-A11y** bleiben
  wie dokumentiert (§9.4.1-§9.4.3).
- **Drei neue Restdefekte** warten auf Entscheidung (Settle-Zeit-Fix / Foreign-Farbe /
  Knotenklick-Pfad).

**Keine Push.** Lokaler Commit, bleibt liegen bis zum nächsten deploy-Bündel oder bis
Nikinger die Smokes + Doku-Update abgenickt hat.
