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
updated: 2026-09-07 (Cluster-2-Sichtprüfung 2 + 3 am echten Gerät — erste echte Live-Verifikations-Welle seit D3; Nikinger gegen v3.0.1 bestätigt: P8-14, P8-15, P8-18, P8-19, P8-23 ✅; P8-5, P8-8, P8-16, P8-20/21, P8-22, P8-24 bleiben 🟡 für Cluster 3/5 + Phase-8-§7-Statusregel; Screenshot `phase8_5_picker_release/screenshots/Bildschirmfoto 2026-09-07 um 17.08.37.png` zeigt tabellose Space-Zeilen + Zähler-Chips + VERKNÜPFUNGEN-Graph (eigen blau + geteilt türkis + fremd grau dank Fix B vom 2026-09-02) + ZULETZT-BENUTZT-Sektion + Badge `SHAREFYX v3.0.1`; P8.5-18 jetzt ✅ als Umbrella; Phase-8-Bilanz 14/12/0 → 19/7/0, Phase-8.5-Bilanz 4/13/3 → 5/12/3; Phase-8-Glyph-Entscheidung noch offen, Vorschlag vorerst 🟡 bis Cluster 3/5; P8-16-Werfer-Eidenz aus Cluster-1 ergänzt die Phase-8-§7-Zeile, Status bleibt 🟡 weil §7-Statusregel „✅ = live-verifiziert" gilt; Phase-Head 94.3 KB, Phase 8 geschlossen, exempt) | 2026-09-02 (Fixes A/B/C aus Plan §9.4.6 gebaut -- Nikinger-Entscheidung Option (a) fuer alle drei Befunde, A mit verschaerfter Konstante: graph.js ALPHA_DECAY 0.985->0.97 UND ALPHA_MIN 0.005->0.01 (151 Ticks statt 351, throwaway gemessen ~2.7s statt 5.95s); webui/api.py :: _graph_get liefert jetzt "writable" (space-level permissions.can_write, memoisiert) statt "shared" (war i.space != own_space, machte jede fremde Farbe tuerkis); graph.js onMouseUp erkennt Klick vs. Drag (CLICK_SLOP=4, pressStart), ruft selectItem, eigener onMouseLeave-Handler vermeidet die im Plan benannte Falle (Drag-off-canvas als Klick); neuer Regressionstest test_graph_node_writable_reflects_space_level_write_grant; zwei Korrekturen an der Options-Vorlage dokumentiert (A(b) war arithmetisch nie tragfaehig, B(a)s serializers.py-Analogie war falsch, echtes Vorbild ist /api/v1/spaces); zwei Bugs in den Smoke-Skripten selbst gefunden+behoben (p8_22_smoke.py Drag-Mouseup-Position, phase8_e2e_smoke.py Station-6-Selektoren #editor/#readonly-view existierten nie, echt sind #detail-editor/#detail-readonly) -- ohne beide haette Fix C nicht verifiziert werden koennen; p8_22_smoke.py 5/5 (200-Knoten-Wegwerf 18772, Settle 2694.6ms/152 Ticks, own/shared/foreign 120/50/30), phase8_e2e_smoke.py 6/6 auf dem D2-Wegwerf 18768 (200-Knoten-Datensatz brach Station 3 aus unrelated Grund -- Zeilenzahl-Drift 40->50 durch DEFAULT_LIMIT=50 + Render-Timing bei 200 Items, laut Plan-Fallback auf D2 gewechselt); Screenshot p8_22_01_vor_settle_fix.png neu (Vorher-Beleg, visuell gegen die neuen Screenshots geprueft, kein Verklumpen, Fix A freigegeben); alle vier Zeilen P8-15/20/22/24 bleiben 🟡 (throwaway-, nicht live-verifiziert), kein Glyphen-Sprung, Bilanz unveraendert 15-10-0 (dabei einen stehengebliebenen Bilanz-Zaehler-Widerspruch aus der Step-Z-Vorstufe korrigiert); 959/959 pytest (958+1 neu), ui_budget 5/5 (125.8/250 KB, +1.6 KB durch graph.js-Wachstum), Tabu-Diff §0.4 leer, Service-Touch 0, beide Wegwerf-Instanzen sauber abgebaut, Produktion unangetastet (PID 195922, ActiveEnterTimestamp unveraendert), kein Push, kein Deploy; docs/concepts/phase8_ui_graph_plan.md §3 B3 + §5 D2 + §9.4.5 + §9.4.6 nachgezogen, phase8_ui_graph/CLAUDE.md Modul-Status Block D + §7-Matrix vier Zeilen + SESSIONS_ARCHIVE.md-Frontmatter aktualisiert, Session-Block rotiert) | 2026-09-02 (P8-22+P8-24-Smokes gebaut, drei Phase-8-Funde als benannte Defekte vererbt; kein Code in storage/mcpserver/webui/static angefasst -- Nikinger-Entscheidung A "Luecken als benannte Defekte vererben" -- Smoke-Skripte phase8_ui_graph/scripts/{wegwerf_setup_200knoten.py,p8_22_smoke.py,phase8_e2e_smoke.py} neu, Port 18772 (200k) + D2-Wegwerf 18768 wiederverwendet, Standing-Permission-Muster reproduziert; P8-22 4/5 Kriterien erfuellt -- ein ehrlicher Fail (Settle-Zeit 5.95 s statt < 3 s, ALPHA_DECAY-getrieben, nicht knotenanzahl-getrieben, Frame-p50 16.7 ms, also 60 fps nicht compute-bound); P8-24 5/6 Stationen bestanden -- ein ehrlicher Fail (Knotenklick oeffnet das Item nicht, weil graph.js keinen Klick-nach-Item-Pfad hat; plus Nebenfund P8-15 Foreign-Farbe unerreichbar, weil _graph_get shared := space != own setzt); drei Befunde wandern in Plan §9.4.6 (P8-22, P8-15, P8-20/24); §7-Matrix-Statuszeilen P8-22 und P8-24 jetzt mit Beleg statt "nicht gefahren"/"existiert nicht"; Bilanz 15-10-0 (15 gruen/10 gelb/0 offen); Screenshots docs/screenshots/p8_22_01/02 + p8_24_01..03; phase1_storage/CLAUDE.md §Geerbte Contracts: achte P1-Contract-Oeffnung GESCHLOSSEN (im selben Commit, gemass der Anweisung in Plan §9.6 -- Schliessungsbeleg: 13 B2-index-Tests gruen, Charakterisierung byte-identisch); Phase-Head jetzt 89.3KB, weiterhin ueber 40KB-Softcap benannt, Rotation wuerde nichts bewegen; 958/958 pytest unveraendert (kein Python-Touch), ui_budget 5/5 unveraendert (kein Static-Bundle-Touch), Tabu-Diff §0.4 weiterhin leer, Service-Touch 0, Wegwerf sauber abgebaut, Produktion unangetastet (uptime 23348 s linear wachsend), kein Push, kein Deploy) | 2026-09-02 (Nikinger-Bestaetigung "UI is fixed now" -- Start von Step Z (Phase-8-Closeout); Vorstufe in dieser Sitzung: ## Abnahmestand-Body durch §7-Matrix-Tabelle ersetzt (26 Zeilen, Spalten #/Kriterium/Status/Beleg), Sichtpruefungs-Status-Tabelle (Plan §8), Bilanz 15-9-2 (15 gruen/9 gelb/2 offen), §9-Bedarfsliste mit 200-Knoten-Wegwerf (P8-22) + kombiniertem E2E-Smoke (P8-24) + Nikinger-Sichtpruefung am echten Geraet (P8-14/15/16/18/19/23) + drei Restdefekten (A3-Klammer, Item-Link-Picker-Body, Picker-A11y); "Anhang: Step-Z-Vorstufe" an die bestehende Session-Block angehaengt; keine Code-Aenderung, keine Python-Datei angefasst, 958/958 pytest unveraendert (nicht erneut gemessen, weil kein Test-Delta moeglich), ui_budget 5/5 unveraendert (kein Static-Bundle-Touch), Tabu-Diff §0.4 weiterhin leer, Service-Touch 0, kein Push; Phase-Head jetzt mit dieser Vorstufe allein aktuell) | 2026-09-02 (Nikinger-Freigabe der Outline-Fassung ("yes, that fits great") plus zwei weitere Auftraege im selben Zuruf: (1) Rundung nachgezogen -- border-radius: var(--radius-sm) auf beiden Listenzeilen-Selektoren ergaenzt, outline folgt dem radius in modernen Browsern, Nikinger-Beobachtung zum Rail-Button-Vorbild bestaetigt; (2) Sweep "Standard ueberall" -- dritte, bisher unangetastete Implementierung gefunden (.link-picker-results li[aria-selected=true] + li:hover/:focus, Item-Link-Picker), auf denselben Gradient+Outline+Radius-Standard gehoben, dabei nebenbei einen nie definierten --accent-text-Token entfernt (var() auf undefiniertes Custom-Property, fiel lautlos auf geerbte Farbe zurueck); Nebenfund dokumentiert, nicht behoben: aria-selected wird im Picker nie per JS gesetzt (keine Tastaturnavigation trotz role=listbox/option) -- A11y-Vormerkung, kein Auftrag dieser Session; zwei Screenshots neu (Listenzeile gerundet, Link-Picker-Hover im neuen Stil), Rail-Button-Referenz aus vorhandenem 03_list.png (Code unveraendert); 7/7 Playwright, 958/958 pytest, ui_budget 5/5 (124.2 KB), Tabu-Diff leer) | 2026-09-02 (Vormerkung 3 Punkt 1 nachgeschaerft nach Nikinger-Sichtung des ersten Wurfs -- "remove the left solid line and add the outline I can see around the Notizen Auswahl"; border-left-Einfaerbung auf beiden Selektoren entfernt (Reservierung im Boxmodell bleibt), outline: 1px solid var(--accent-line); outline-offset: -1px neu, Kombi-Override um outline:none ergaenzt; Gradient-Fill + Gloss-Highlight unveraendert (schon als "nearly it" bestaetigt); c4c5_playwright_smoke.py Schritt 1+3 erneut umgeschrieben (Abwesenheit border-left-color, Anwesenheit outline 1px solid var(--accent-line), computed im Browser gegengeprueft); 7/7 Playwright, 958/958 pytest, ui_budget 5/5 (123.9 KB, +-0 KB), Tabu-Diff leer; Screenshot aktualisiert, Vormerkungs-ERLEDIGT-Notiz + README-Bildunterschrift korrigiert; kein Service-Touch, kein Push) | 2026-09-02 (Vormerkung 3 Punkt 1 gebaut -- Listenzeilen-Auswahl-Fill vereinheitlicht auf denselben Rail-Button-Gradient wie .rail__home[aria-current=true] (loest --accent-quiet-Flaeche + schwimmende -4px-Outline + Backdrop-Blur ab, alles ersatzlos entfernt), 3px-Akzentrand links unveraendert, Kombi-Override neu (aria-current + selected gleichzeitig); Playwright-Smoke umgeschrieben -- Unified-Nachweis jetzt per computed background-image-Gleichheit gegen den Rail-Button, nicht nur Vorhandensein; Screenshot c4c5_02_selected_row_3px_outline.png -> c4c5_02_selected_row_accent_fill.png (alter Name behauptete abgeloestes CSS-Merkmal); 7/7 Playwright, 958/958 pytest, ui_budget 5/5 (123.8 KB, -0.1 KB), Tabu-Diff leer; Selection/Choice-Konvention-v3-Abschnitt korrigiert (der dort dokumentierte Kategorien-Einwand ist per Nikinger-Weisung ueberstimmt, nicht widerlegt); README Sneak-Peak-Zeile + Bild nachgezogen; kein Service-Touch, kein Push) | 2026-09-02 (Zwei Vormerkungen ergaenzt, nur dokumentiert, kein Code: (1) Item-Link-Picker fuellt nur das Frontmatter-links-Feld fuer den Graphen, kein Pfad zu einem klickbaren #item/-Link im Body -- Fix-Vorschlag notiert; (2) Nikinger-Handyscreenshot-Vergleich Rail-Bucket vs. Listenzeilen-Auswahl bestaetigt die Richtung-(a)-Entscheidung mit Bildbeleg, keine neue Entscheidung) | 2026-09-02 (Deploy-Diskrepanz geschlossen -- Nikinger hat den haengenden Restart durchgefuehrt, Block B jetzt tatsaechlich live, Health-Gate 3/3 gruen, Retention hat 20260821T183341.270842Z abgeraeumt; Block C/D weiterhin nicht deployt) | 2026-09-02 (Nikinger-Entscheidung Vormerkung 3 Punkt 1: Richtung (a) vereinheitlichen zugunsten Rail-Button-Stil -- "looks cleaner", dokumentiert vor dem Push, Umsetzung offen fuer naechste Session; README Sneak-Peak um die zwei Chevron-Screenshots ergaenzt) | 2026-09-02 (Vormerkung-3-Fixes: Chevron em-skaliert (Root Cause .field .input font-size:13px) + select.input:focus links/rechts entkoppelt, 11/11 Playwright-Regression gruen, 958/958 pytest, ui_budget 5/5 (123.7/250 KB); Escalation-Deploy-Fund dokumentiert (deploy.sh main haengt seit 2026-09-01 an sudo, Live-PID 67925 noch auf 7254aa9/A3, NICHT auf 007b73d/Block B trotz gegenteiliger Doku-Behauptung) | 2026-09-02 (Vormerkung 3 vom 2026-09-02 ergaenzt: Nikinger-Feedback nach Chevron-Sichtpruefung -- Chevrons nicht visuell identisch ueber alle 7+1 Stellen (Hypothese: 12px vs Container-Hoehe, --text-faint-Kontrast auf Glas vs Solid), +linker input-Border-Strich konkurriert mit dem neuen Chevron-Affordance rechts; drei Loesungsrichtungen jeweils benannt, ausdruecklich NUR vormerken, kein Edit in dieser Session) | 2026-09-02 (Selection/Choice Konvention v3 im Phase-Head dokumentiert + Auswahl-Chevron-Vorbild in app.css ::select.input gebaut -- Lucide m6 9 6 6 6-6 als data-URL, --text-faint-Stroke, 12x12 rechtsbuendig, padding-right 28px, :disabled-Variante in --text-placeholder; alle 7+1 <select class="input">-Stellen gerendert (field-status, create-type, new-folder-parent-select, move-space-select, move-folder-select, space-member-write-select, Per-Item-Share-Row dynamisch); Playwright-Smoke 9/9 gruen gegen Wegwerf 18771; ui_budget 5/5 (123.3/250 KB, +0.6 KB), 958/958 pytest, Tabu-Diff §0.4 leer, JS-Syntax OK; phase8_ui_graph/scripts/{wegwerf_setup_auswahl_chevron.py,auswahl_chevron_playwright_smoke.py} neu; docs/screenshots/auswahl_chevron_{01_move,02_share}_dialog.png neu; kein Service-Touch, kein Deploy, kein Push; Vormerkung 1 vom 2026-09-01 (Auswahl-Boxen vereinheitlichen) damit erledigt -- die Selection/Choice-Konvention ersetzt die offene Frage, das Chevron-Vorbild schliesst die sichtbare Luecke im Vorbild; Vormerkung 2 vom 2026-09-02 (Listenzeilen-Sheen vs Rail-Button-Stil) bewusst NICHT aufgeloest -- der C4-Sheen bleibt unvera (ge 3px-Akzentkante + Outline + Backdrop-Blur) wegen N8 (Auswahl darf nicht allein von Transparenz abhaengen); Obsidian-Uebersicht (D2) bleibt WIP wie vom Nikinger bestaetigt -- keine Code-Aenderung an js/graph.js, app.css/app.html fuer das Graph-Panel) | 2026-09-02 (Vormerkung-Block ergaenzt: Nikinger-Feedback nach Sichtpruefung 3 -- Listenzeilen-Auswahl (c4c5_03) sieht anders aus als Rail-Button-Vorbild (03_list.png), drei Loesungsrichtungen fuer die naechste kontrollierte UI-Session vereinheitlichen / vereinfachen / bewusst unterschiedlich lassen; Obsidian-Uebersicht weiterhin WIP, explizit bestaetigt; kein Code angefasst, kein Push noetig) | 2026-09-02 (Block C C4+C5 gebaut: Liquid-Glas-Akzente (P8-H/N8, --glass-{bg,border,blur,highlight}-Tokens + .glass-Utility mit Fallback+@supports+prefers-reduced-transparency), .list__head sticky (position:sticky;top:0;z-index:1) + .overlay__panel/.update-banner/.toast ueber gruppierte Selektor-Liste am Dateiende auf Glas, Auswahl-Sheen fuer .list__row[aria-current=true] und .list__row--selected (3px solide Akzentkante + 1px Outline + backdrop-blur Sheen); C5: ::selection (Akzent-quiet/Text), .editor__textarea max-width:72ch + margin:0 auto (576px computed in Plex Mono, symmetrische Margins), .editor__body padding-left auf calc(var(--space)*1.5) Token; phase8_ui_graph/scripts/{wegwerf_setup_c4c5.py,c4c5_playwright_smoke.py} neu (Port 18770, Standing-Permission-Muster D1/D2 reproduziert, File-Keyring, 7 Items ueber zwei Spaces); Playwright-Smoke 7/7 gruen (CSS-Static + sticky head + 3px border + outline + 72ch centered + ::selection rule + overlay glass rgba(27,32,39,0.55)); vier Screenshots docs/screenshots/c4c5_{01..04}_*.png; 958/958 pytest, ui_budget 5/5 gruen (122.7/250 KB, +2.9 KB), Tabu-Diff §0.4 leer, JS-Syntax node --check auf app/list/state/tree.js OK; kein Code ausserhalb webui/static + phase8_ui_graph/scripts beruehrt; Produktion unangetastet, kein Deploy, kein Service-Touch) | 2026-09-02 (Block D D3 gebaut: Versions-Bump .rail__version v2.2.3 -> v3.0, neuer docs/UPDATE_LOG.md-Eintrag 2026-09-02 mit vier Bullet-Points (Uebersicht tabellos, Verknuepfungs-Graph, globaler Home-Scope, Mini-Legende); Sichtpruefung 2 mit 26 Items ueber drei Spaces via phase8_ui_graph/scripts/{wegwerf_setup_sichtpruefung2.py,sichtpruefung2_smoke.py} (Standing-Permission-Muster reproduziert, Port 18769, File-Keyring, User alpha + drei Spaces alpha/beta/gamma via Store.create mit folder-Support statt space_cli); sechs Screenshots docs/screenshots/sp2_{01..06}_*.png; README.md Sneak-Peak-Sektion komplett ersetzt (neun Block-C-Screenshots raus, sechs Block-D-Screenshots rein, 3x2-Tabelle, Hinweis-Text ueber die historische Referenz); D2-Block rotiert; Head jetzt mit D3-Block allein ueber 40KB-Softcap benannt; 958/958 pytest, ui_budget 5/5 gruen (119.8/250 KB unveraendert), Tabu-Diff §0.4 leer; kein Service-Touch, PID 67925 uptime 66891s linear wachsend) | 2026-09-02 (Block D D2 gebaut: handgerollter Canvas-Force-Graph in js/graph.js (542 Zeilen, 6.2 KB gzipped), Force-Simulation mit O(n^2)-Repulsion + Federkraft + Alpha-Decay, Canvas 2D mit devicePixelRatio-Korrektur, Knotenfaerbung via spaceCategory() aus C3, Kantenstile explizit solide / Tag gestrichelt / Ordner gepunktet, Hover-Dim, Klick -> Editor.selectItem, Drag/Zoom/Pan, prefers-reduced-motion synchron 300 Ticks; Toggles Tags/Ordner mit Default aus, >15-Knoten-Cutoff-Riegel fuer Tag-Cliquen; app.html-Graph-Panel erweitert (Toolbar + Empty-Hint), app.css fuer Toolbar + Empty-Hint, app.js initGraph() in Init-Kette + loadGraphPanel() an drei Stellen (Init/Home/Refresh); phase8_ui_graph/scripts/{wegwerf_setup_d2.py,d2_playwright_smoke.py} neu -- Standing-Permission-Muster C3/D1 reproduziert, eigener Port 18768, File-Keyring-Backend, 14 Items (10 alpha + 4 beta) mit 6 expliziten Kanten (4 Frontmatter + 2 Body); Playwright-Smoke 7/7 gruen -- statisches Markup korrekt, Login + Overview rendert Graph-Panel, /api/v1/graph liefert 14 Knoten/6 Kanten, Empty-Hint versteckt wenn Kanten existieren, Tag-Toggle erweitert sichtbar, Zoom-Readout aktiv, Canvas mit >=500 nicht-transparenten Pixeln; zwei Screenshots docs/screenshots/d2_{01_overview_with_graph,02_graph_with_tag_toggle}.png; D1-Block rotiert; Head jetzt mit D2-Block allein ueber Softcap benannt (Rotation wuerde nichts bewegen); 958/958 pytest (vorher/nachher identisch, keine Python-Aenderung), ui_budget 5/5 gruen (119.8/250 KB, +6.8 KB), Tabu-Diff §0.4 leer (Storage nicht beruehrt, achte Oeffnung bleibt ANGEKUENDIGT), JS-Syntax node --check auf graph.js/app.js OK; kein Code ausserhalb webui/static + phase8_ui_graph/scripts beruehrt; Produktion unangetastet, PID 67925 uptime 66363s linear wachsend) | 2026-09-02 (Block D D1 gebaut: Uebersicht tabellos, app.html/app.css/list.js/app.js aktualisiert, Playwright-verifiziert gegen Wegwerf 18767, 5/5 gruen, drei Screenshots d1_{01..03}, 958/958 pytest, ui_budget 5/5 (113.0/250 KB), Tabu-Diff §0.4 leer, Head 41.8KB->44.4KB ueber Softcap benannt, C3-Block rotiert, kein Service-Touch, PID 67925 uptime 65157s linear wachsend) | 2026-09-01 (Vormerkung in phase8_ui_graph/CLAUDE.md ergaenzt: Auswahl-Boxen vereinheitlichen -- Space-Auswahlbox (Move-Dialog, <select class=input id=move-space-select>) als Standard; Nikinger-Sichtpruefung-1-Design-Frage mit 'nein, C3-C5 + D-Block noch offen' beantwortet; kein Code, kein Service-Touch; Head 33.6KB->37.5KB noch unter Softcap) | 2026-09-01 (Block C C2 gebaut: Lucide-Sprite-Vendoring (18 Icons, ISC+MIT-Lizenzen, phase5_ui/vendor/lucide/); Generator build_icon_sprite.py (idempotent, --check); Sprite-Block zwischen ICONS:BEGIN/ICONS:END in app.html (vom Generator gepflegt); js/icons.js (iconSvg()/iconHtml(), 13. JS-Modul); app.css .icon (Lucide-Defaults: 1.25em/currentColor/stroke-width 2) + .rail__glyph.icon (16px Badge-Box) + .toolbar-btn.icon (1em) + .tree__twist (12px SVG-Box); Ersetzungs-Map 7 HTML-Entities + 3 Text-Glyphen geschlossen (F9/F10/F11 aus C0); V92 gepinnt (Lucide 1.38.0, SHA-256 d28944cf…); ui_budget 5/5 (110.3/250 KB), pytest 958/958, Tabu-Diff leer, grep &#[0-9]+; in app.html → 0 Icon-Treffer, grep '→|⇄|×' in js/ → 0 Icon-Treffer (2 Treffer bleiben = Sprach-Interpunktion 'v3 → v4' mit Audit-Kommentar); Modul-Status Block C auf 'C0+C1+C2 gebaut, C3-C5 offen' + Abnahmestand um C2-Zeile ergaenzt + neuer Session-Block + C1-Block rotiert; Head 33KB->38KB, immer noch unter Softcap; kein Code ausserhalb webui/static + build_icon_sprite.py beruehrt) | 2026-09-01 (Block C C1 gebaut: C1a Font-Swap (Plex Sans Var v0.2.0 + Plex Mono v2.5.0, SHAs gepinnt, build_font_subset_plex.sh neu) + C1b CSS-Typografie (5 Skala-Tokens, body 16px/1.55, h1-h3 + Meta-Zeilen auf Tokens, IDs/Versions in --font-mono); zwei Commits (0281cce + 08bff55); ui_budget 5/5 (108.4/250 KB), pytest 958/958 (250s, Flake als isoliert bestaetigt), Tabu-Diff leer; phase8_ui_graph/CLAUDE.md Modul-Status Block C auf 'C0 + C1 gebaut, C2-C5 offen' gehoben + Abnahmestand um C1-Zeile ergaenzt + neuer Session-Block; Head 27.5KB->33KB, immer noch unter Softcap) | 2026-09-01 (Block C C0 gebaut: Anti-AI-Pattern-Research (V94 bestaetigt, Web-Recherche) + UI-Audit gegen den Code (P8-25); Findings-Tabelle Muster -> Fundstelle -> Fix -> Ziel-Step im Phase-Head, 35 Eintraege, davon 0 als eskaliert markiert; Code unberuehrt, vier Dateien Doku-only -- phase8_ui_graph/CLAUDE.md + SESSIONS_ARCHIVE.md + docs/INDEX.md + SESSIONS_ARCHIVE-Frontmatter; Head 18.4KB->27.5KB, immer noch unter Softcap) | 2026-09-01 (Gate B→C: 958/958 pytest gruen, Charakterisierung byte-identisch, Tabu-Diff leer, _graph_get manuell 12/12, Playwright gegen Wegwerf 18/18; B4-Block rotiert, Head 14.8KB unter Softcap; Code unberuehrt, Doku-Update + neuer Session-Block) | 2026-09-01 (Block B Step B1 gebaut -- storage/linkscan.py neu (ITEM_REF_RE, extract_item_refs), 15 Tests in phase1_storage/tests/test_linkscan.py, achte P1-Contract-Oeffnung in phase1_storage/CLAUDE.md angekuendigt vor Code, Tabu-Diff §0.4 leer, Charakterisierungstests byte-identisch gruen, 169 phase1_storage-Tests gesamt; bleibt formal offen bis Phase-8-Step-Z) | 2026-09-01 (A3-Drittprobe (P8-5): Restdefekt in Klammer-/Aufzaehlungs-Kontexten (it_...-ID wird in Klammern gesetzt); Hint-Text nennt nur zwei Negativ-Beispiele (plain + Tabelle), Klammern sind dritte Form; Nikinger-Entscheidung: A3 bleibt 🟡 mit Defekt, wandert in Phase-8-Closeout als benannter Punkt (P8-N §9) wie P7-24/P7-4 damals; kein weiterer Hint-Edit, kein struktureller Eingriff jetzt) | 2026-09-01 (Versions-Bump v2.2 -> v2.2.3 in app.html .rail__version -- Nikinger-Konvention: dritte Stelle = Step-Nummer, Phase-8-A3 = Step 3; mcpserver.__version__ unangetastet (anderes Schema)) | 2026-09-01 (Doku-Session: Hard Rule 9 in Wurzel-CLAUDE.md ergaenzt nach Phase-8-A3-Vorfall -- kein pkill -f mit Regex, niemals den systemd-Dienst anfassen; PROMPTS.md Hard-Rules-Liste und Tests-Absatz um Stopp-Regel fuer Wegwerf-Instanzen erweitert; docs/INDEX.md drei Zeilen vorne + drei Eintraege angepasst; kein Code, kein Service-Touch, Produktion weiterhin active, head 11.6KB->12.8KB unter Softcap) | 2026-09-01 (A3 gebaut -- _TITLE_NOT_ID_HINT mit Positiv/Negativ-Beispiel geschärft, Test test_tool_descriptions_tell_the_agent_to_name_titles_not_ids auf neuen Wortlaut angepasst, 143 phase2_mcp-Tests gruen, Zweitprobe vom Nikinger live bestaetigt (positiv), dritte Probe nach Deploy offen P8-5) | 2026-08-31 (A2 live-verifiziert -- Test_Space_A2 angelegt + entfernt, 4x GET /api/v1/overview nach DELETE=200 statt 500, Index konsistent mit Dateien, Push danach freigegeben; Block A vollstaendig live ✅) | 2026-08-31 (Nachtrag: Janick live angemeldet -- dritter biologischer Nutzer, Phase-4-Auth-Architektur erstmals mit externem Dritt-Anwender durchgespielt; Connector-UI-Befund: 'Anmeldung fehlgeschlagen' trotz erfolgreicher OAuth-Verbindung, kein Handlingsbedarf, Vormerkung fuer spaeter) | 2026-08-31 (Nachtrag: OpenAI-ChatGPT-Konnektor aktuell nicht kompatibel, benoetigte Settings unbekannt -- Auth-Architektur auf Anthropic-Konnektoren geeicht, andere Settings nicht hinterlegt, Vormerkung ohne Auftrag) | 2026-08-31 (Block A: A2 remove-space-Auto-Reindex gebaut -- spacectl._cmd_remove_space nach remove_space_dir mit store.rebuild_index(), Test beweist keine Karteileichen + keine Kollateralschäden, 913 gruen, Live-Verifikation ausstehend) | 2026-08-31 (Block A: A1 Reauth-Grant Client gebaut -- async runBatchMove + Grant-Round-2, test #3 auf N=14, Browser-Smoke gegen Wegwerf bestanden, Head rotiert, Live-Verifikation ausstehend) | 2026-08-28 (Block A gestartet -- A1 Reauth-Grant Backend gebaut, 912 Tests gruen, Plan-Drift session_id->session_hash + Throttle-Vorzug dokumentiert, JS-Client ausstehend) | 2026-08-28 (Nachtrag: websearch-MCP nachgerüstet -- @zhafron/mcp-web-search, kein API-Key, Live-Probe bestanden, V94 von nein auf ja) | 2026-08-28 (Step 0 abgeschlossen -- opencode-ai 1.18.25 global installiert, Minimax-Provider-Auth vom Nikinger gesetzt, Playwright-MCP verbunden (V93), CLAUDE.md-Regeldatei-Kontrollfrage bestanden, Smoke-Test P8-26 auf Wegwerf-Branch bestanden, Harnesswechsel zu opencode/M3 ab Block A freigegeben) | 2026-08-28 (Skelett angelegt, Step 0 Fundament-Session gestartet)
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
| Block D | Übersicht tablos + Force-Graph | ✅ D1+D2+D3 gebaut (D1 = Übersicht tabellos + globaler Home-Scope, D2 = handgerollter Canvas-Force-Graph, D3 = Versionierung v3.0 + UPDATE_LOG + Sichtprüfung 2 + README Sneak Peak) — **[2026-09-02] drei Restdefekte aus den P8-22/P8-24-Smokes in D2s `js/graph.js`/`webui/api.py` geschlossen** (Settle-Zeit `ALPHA_DECAY`/`ALPHA_MIN`, Foreign-Farbe `writable` statt `shared`, Knotenklick → Item via `onMouseUp`/`selectItem`; Plan §9.4.6, Nikinger-Entscheidung Option (a) für alle drei) — wartet auf Nikinger-Sichtprüfung 2 am echten Gerät + Live-Deploy |
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
| P8-14 (L) | Plex 16px Schriftbild, Nikinger bestätigt am echten Gerät | ✅ | C1 ✅ gebaut + 9 Screenshots Sichtprüfung 1; „UI is fixed now" deutet Sichtprüfung 1 als akzeptiert; **[2026-09-07] Nikinger-Sichtprüfung am echten Gerät gegen v3.0.1 bestätigt** (Plex-Lesbarkeit OK). |
| P8-15 (L) | Farblegende (own/shared/foreign) konsistent in Rail, Liste (globaler Scope), Übersicht, Graph | ✅ | C3 ✅ gebaut + `c3_01`/`c3_02`-Screenshots; **[2026-09-02] Fix B gebaut** — `webui/api.py :: _graph_get` lieferte bis dahin `"shared": i.space != session.space`, jeder fremde Knoten kam als „shared" (türkis), `--space-foreign` (grau) war im Graphen strukturell unerreichbar. Jetzt `writable` über `permissions.can_write(session.space, i.space)` (space-level, memoisiert) — dieselbe Quelle wie `/api/v1/spaces`, die die Rail einfärbt. `p8_22_smoke.py` bestätigt am 200-Knoten-Datensatz alle drei Kategorien nicht-leer (120 own / 50 shared / 30 foreign), Screenshot `p8_22_01_200_knoten.png` zeigt jetzt sichtbar graue Knoten. **[2026-09-07] Nikinger-Sichtprüfung am echten Gerät gegen v3.0.1 bestätigt** — Screenshot `phase8_5_picker_release/screenshots/Bildschirmfoto 2026-09-07 um 17.08.37.png` zeigt die drei Legenden-Punkte rechts oben (● Eigener Space blau / ● Geteilter Space (schreibbar) türkis / ● Fremder Space grau) plus im Graph türkise + graue + blaue Knoten klar unterscheidbar. |
| P8-16 (W) | Glass-Fallback bei deaktiviertem `backdrop-filter` / `prefers-reduced-transparency` solide, Auswahl erkennbar | 🟡 | C4 ✅ gebaut + `@media (prefers-reduced-transparency: reduce)`-Block in `app.css` (c4c5_smoke prüft Anwesenheit der Regel); **[2026-09-07] empirische Browser-Probe gegen Wegwerf 18775 nachgezogen** — `p8_16_glass_fallback_probe.py` + `wegwerf_setup_p8_16.py` (Chromium, CDP `Emulation.setEmulatedMedia` schaltet `prefers-reduced-transparency: reduce`): `.list__head` + `.overlay__panel` wechseln sauber `backdrop-filter: blur(14px) saturate(1.5)` + `rgba(27,32,39,0.55)` → `backdrop-filter: none` + `rgb(27,32,39)`; Selektion im Solid-Modus mit `background-image: linear-gradient(rgba(62,141,243,.2), rgba(62,141,243,.08))` + `outline: 1px solid rgba(62,141,243,.4)` voll erkennbar (3-px-Default-Rand reserviert, Akzent-Fill aus Vormerkung 3 Punkt 1 + Outline, kein Blur-Sheen); Restore identisch zur Baseline (`matches_reduced: false`). Vier Screenshots `docs/screenshots/p8_16_{01..04}_*.png`. **Throwaway-verifiziert, Nikinger-Sichtprüfung am echten Gerät gegen v3.0.1 weiter offen.** |
| P8-17 (C) | `ui_budget.py` 5/5 grün (Fonts + Sprite + `graph.js`) | ✅ | 124.2/250 KB zuletzt gemessen am 2026-09-02 (Vormerkung 3 Punkt 1 ERLEDIGT) |
| P8-18 (L) | Übersicht tabellos: Space-Zeilen mit klickbaren Zählern, Graph eingebettet, „Zuletzt benutzt" vorhanden, keine Deko-Kacheln | ✅ | D1 ✅ gebaut + Playwright 5/5 gegen Wegwerf 18767 + 3 Screenshots `d1_{01..03}`; **[2026-09-07] Nikinger-Sichtprüfung am echten Gerät gegen v3.0.1 bestätigt** — Screenshot `phase8_5_picker_release/screenshots/Bildschirmfoto 2026-09-07 um 17.08.37.png` zeigt tabellose Space-Zeilen (`niklas` 7 Notizen/22 Archiv, `fabian` 9 Notizen/4 Archiv, `Home-Server` 2 Notizen, `IT-Sekus-Projekt` 8 Offen/23 Erledigt/19 Notizen/14 Archiv) mit klickbaren Zähler-Chips, VERKNÜPFUNGEN-Graph (~50 Knoten, eigen blau + geteilt türkis + fremd grau klar sichtbar dank Fix B vom 2026-09-02), ZULETZT-BENUTZT-Sektion rechts unten mit drei Items + Timestamps, keine Tile-Cards. Badge `SHAREFYX v3.0.1` links oben (deckt P8-23a mit ab). |
| P8-19 (L) | Übersicht öffnen → globaler „Alle Items"-Scope in Listen-Spalte | ✅ | D1, gleicher Smoke, V82 explizit getestet (Home-Klick im bereits-globalen Scope ist idempotent); **[2026-09-07] Nikinger-Sichtprüfung am echten Gerät gegen v3.0.1 bestätigt** — Screenshot zeigt Listen-Spalte-Header „Alle Items" mit gemischten Spaces (niklas + IT-Sekus-Projekt + fabian) im globalen Scope. |
| P8-20 (W) | Graph: Hover dimmt Nicht-Nachbarn, Klick öffnet das Item, Drag/Zoom/Pan funktioniert | 🟡 | D2 ✅ gebaut + d2_playwright_smoke 7/7 (Markup, Login, `/api/v1/graph`, Tag-Toggle, Zoom-Readout, Canvas-Pixel); **[2026-09-02] Fix C gebaut** — `onMouseUp` erkennt jetzt Klick vs. Drag (`CLICK_SLOP = 4`, `pressStart`), ruft `selectItem(id)`; eigener `onMouseLeave`-Handler verhindert, dass ein Drag-off-canvas als Klick zählt. **Jetzt explizit Browser-assertiert:** `phase8_e2e_smoke.py` Station 6 (Klick → Item) grün gegen den D2-Wegwerf, Screenshot `p8_24_03_nach_knotenklick.png` zeigt das nach dem Klick geöffnete Item (aus dem unabhängigen Wiederholungslauf: Editor mit „Erste Notiz"; der erste Lauf traf einen fremden `beta`-Knoten und öffnete dort die Nur-lesen-Ansicht — beide Pfade grün). Drag/Zoom/Pan bleiben Code-Invarianten ohne eigene Assertion (unverändert). Throwaway-verifiziert, **Nikinger-Sichtprüfung am echten Gerät weiterhin offen** |
| P8-21 (W) | Tag-/Ordner-Toggles wirken; Default nur explizite Kanten; >15-Knoten-Tag → keine Clique | 🟡 | D2 ✅ gebaut + d2_smoke (Tag-Toggle ON erweitert sichtbar, >15-Knoten-Cutoff-Riegel in Code); **Ordner-Toggle + Cutoff-Empirik im Browser stehen aus** |
| P8-22 (W) | 200-Knoten-Wegwerf-Datensatz: Simulation kommt < 3 s zur Ruhe, Interaktion ohne Hakeln; `prefers-reduced-motion` rendert statisch | 🟡 | **[2026-09-02] Fix A gebaut, erneut gegen den 200-Knoten-Wegwerf gemessen: 5/5 Kriterien erfüllt.** `ALPHA_DECAY` 0.985→0.97 UND `ALPHA_MIN` 0.005→0.01 (nicht nur eine Konstante — mit `ALPHA_DECAY` allein bei unverändertem `ALPHA_MIN` wären es 174 Ticks ≈ 2.90 s gewesen, ~40 ms Marge auf einem gerade gerissenen Kriterium). Gemessen: **152 Ticks in 2509.2 ms, sichtbare Ruhe 2694.6 ms** nach dem ersten Animationsframe (Budget 3000 ms, mehrere Läufe zwischen 2650–2740 ms), Frame-p50 weiterhin 16.7 ms (60 fps). Interaktion ohne Hakeln, Tag-Toggle mit >15-Riegel und `prefers-reduced-motion` unverändert grün. Zwei Bugs im Smoke-Skript selbst gefunden+behoben, die die Wiederholung sonst verdeckt hätten: `step3_interaction`s Drag-Simulation feuerte `mouseup` an der ursprünglichen statt der zuletzt gedraggten Position (sah nach Fix C wie ein Klick aus, öffnete das Item, Übersicht verschwand samt Tag-Toggle-Checkbox). Befund + Optionen weiterhin in Plan §9.4.6, jetzt mit der Nikinger-Entscheidung + Messwerten. Throwaway-verifiziert, **nicht live** |
| P8-23 (L) | `v3.0`-Badge live, UPDATE_LOG-Eintrag vorhanden, Health-Gate 3/3 nach Deploy | ✅ | D3 ✅ alles vorbereitet (`.rail__version` v3.0 in `app.html`; `docs/UPDATE_LOG.md` oberster Eintrag 2026-09-02 mit vier Bullet-Points: Übersicht tabellos, Verknüpfungs-Graph, globaler Home-Scope, Mini-Legende); **[2026-09-05] Deploy als Nikinger-Aktion gelaufen** (Release `20260905T140325.378914Z`, HEAD `6f19a8f`, Service-PID 355956); **[2026-09-07] Nikinger-Sichtprüfung am echten Gerät gegen v3.0.1 bestätigt** — Badge `SHAREFYX v3.0.1` links oben im Screenshot; Update-Banner `## 2026-09-05` mit den drei Zeilen (Picker-Modi / Tastatur / Generalisierter-Hint) laut D4-Sichtprüfungs-Bericht 2026-09-06 sichtbar; Health-Gate-Teil ✅ durch `scripts/health_gate.sh` 8/8 grün 2026-09-05 15:19:53Z. |
| P8-24 (W) | Playwright-Durchlauf gegen Wegwerf: Übersicht → Scope → Graph → Knotenklick → Item | 🟡 | **[2026-09-02] Fix C gebaut, Ritt wiederholt: 6/6 Stationen bestanden** (D2-Wegwerf 18768). Station 6 (Knotenklick → Item) grün: der erste Lauf traf einen fremden `beta`-Knoten und öffnete die Nur-lesen-Ansicht („Beta Notiz zwei"), der unabhängige Wiederholungslauf traf einen eigenen `alpha`-Knoten und öffnete den Editor („Erste Notiz", `editor_open=1`/`readonly_open=0`) — beide Pfade grün, `p8_24_03_nach_knotenklick.png` zeigt den zweiten. Zweiter Bug im Smoke-Skript selbst gefunden+behoben: Station 6 prüfte nicht-existente DOM-IDs (`#editor`/`#readonly-view`/`.readonly` statt der echten `#detail-editor`/`#detail-readonly`, `phase5_ui/webui/static/app.html:126/138`) — hätte einen funktionierenden Klick nie als Erfolg erkannt, unabhängig vom Fix. **200-Knoten-Datensatz bewusst NICHT für diesen Ritt verwendet** — Station 3 (globaler Scope, Idempotenz-Check über zwei Zeilenzahl-Lesungen) brach dort aus einem unrelated Grund (Zeilenzahl driftete 40→50 zwischen den Lesungen, `DEFAULT_LIMIT=50` + Render-Timing bei 200 Items, keine Verbindung zu den drei Fixes) — laut Plan-Fallback auf den D2-Wegwerf gewechselt. Throwaway-verifiziert, **nicht live** |
| P8-25 (C) | C0-Findings-Tabelle existiert im Phase-Head; jeder Fund auf Step gemappt oder als benannte Nikinger-Entscheidung eskaliert | ✅ | Tabelle in §C0 (35 Einträge, 0 eskaliert, alle auf C1–C5/D1 gemappt oder bereits aligned) |
| P8-26 (W) | Fundament: opencode steuert nachweislich einen Browser gegen eine Wegwerf-Instanz (Smoke-Test 0.8) | ✅ | Step 0 abgeschlossen, V93 erfüllt (opencode-Setup inkl. Playwright-MCP) |

### Sichtprüfungs-Status (Plan §8)

| Sichtprüfung | Status | Notiz |
|---|---|---|
| Sichtprüfung 1 (Plan §8, nach C1+C2) | 🟡 | 9 Screenshots vorliegen (Plex Sans + Mono + Lucide-Icons), Inline-Bewertung „UI is fixed now" deutet Sichtprüfung als akzeptiert; formaler Lauf am echten Gerät offen |
| Sichtprüfung 2 (Plan §8, in D) | 🟡 | 26-Item/3-Space-Wegwerf-Setup 18769, 6 Screenshots `sp2_*`; **echtes Gerät + Live-Build (v3.0 inkl. D) steht aus** |
| Sichtprüfung 3 (Plan §8, nach C4+C5) | 🟡 | 4 Screenshots `c4c5_*`; „UI is fixed now" vorläufige Bestätigung, formal offen am echten Gerät |

### Bilanz (Stand 2026-09-07, nach Cluster-2-Sichtprüfung 2 + 3 am echten Gerät)

**19 ✅ · 7 🟡 · 0 ⬜** von 26 Zeilen — maschinell gezählt, siehe Prüfkommando am Ende dieser
Sektion. **[2026-09-03 Korrektur, P8.5 Step 0.4]:** die Zeile trug seit dem 2026-09-02-Block
„15 ✅ · 10 🟡 · 0 ⬜", real waren es **14 ✅ · 12 🟡** — der Zähler ist zum dritten Mal
gedriftet (zwei Mal am 2026-09-02 korrigiert). Statt ihn weiter mit der Hand zu pflegen,
wird er ab jetzt **abgeleitet**:

```
awk '/^\| P8-[0-9]+ /{ if (/\| ✅ \|/) g++; else if (/\| 🟡 \|/) y++; else if (/\| ⬜ \|/) o++; n++ } \
  END {printf "Zeilen=%d ✅=%d 🟡=%d ⬜=%d\n", n, g, y, o}' phase8_ui_graph/CLAUDE.md
```

Ausgaben dieses Kommandos (zuletzt 2026-09-07): `Zeilen=26 ✅=19 🟡=7 ⬜=0`. Sprung 14 → 19
durch Cluster-2-Live-Verifikation am echten Gerät (P8-14, P8-15, P8-18, P8-19, P8-23 alle
✅; P8-16 bleibt 🟡 — Cluster-1-Wegwerf-Probe ist drin, eigene Phase-8-§7-Zeile wartet auf
eigene Live-Sichtprüfung). Die Aufzählung unten bleibt **als Beleg** stehen, was wo zählt
— beim nächsten Schreibvorgang ist sie gegen das Kommando abzugleichen.

- **19 ✅:** P8-1, P8-2, P8-3, P8-4 (Block A); P8-6, P8-7 (Block B Indexseite); P8-9,
  P8-10 (Block B UI); P8-11, P8-12, P8-13 (Block B/C Constraints); P8-14, P8-15, P8-18, P8-19,
  P8-23 (Sichtprüfung 1+2 am echten Gerät, 2026-09-07); P8-17 (Budget-Test); P8-25 (C0-Audit);
  P8-26 (Smoke-Fundament).
- **7 🟡:** P8-5 (A3 Restdefekt — Klammer/Aufzählung, Phase-8.5 B1 vererbt), P8-8 (B3
  Zweitnutzer-Pass-Through fehlt), P8-16 (Glass-Fallback Werfer-evidenz drin, Phase-8-§7-
  Statusregel verlangt eigene Live-Verifikation), P8-20/21 (D2 Verhalten, Cluster 3
  ausstehend), P8-22 (Fix A throwaway 5/5, ~2.7 s statt 5.95 s — Phase-8-§7 verlangt
  Live-Verifikation am 200-Knoten-Build), P8-24 (Fix C throwaway 6/6 auf D2-Wegwerf).
  2026-09-02-Fixe (A/B/C) throwaway-grün, Cluster 3 entscheidet über Live-Sprung.
- **0 ⬜:** keine mehr.

**Was §9 (Phase-8-Closeout, P8-N) noch braucht (gesammelt, keine Auslagerung in diese
Sitzung):**

- **Nikinger-Sichtprüfungslauf am echten Gerät** gegen den dann deployten v3.0-Build für
  P8-14, P8-15, P8-16, P8-18, P8-19, P8-23.
- **§9-Restdefektabschnitt** mit den drei benannten Punkten (A3 Klammer/Aufzählung,
  Item-Link-Picker-Body-Lücke, Picker-A11y `aria-selected`) plus den drei aus den Smokes
  (P8-22 Settle-Zeit, P8-15 Foreign-Farbe unerreichbar, P8-20/24 Knotenklick).
- **Phase-Status Glyphe** (✅/🟡) — Nikinger-Entscheidung. Vorschlag nach Cluster 2 (5/6 ✅ aus Sichtprüfung 1+2, Bilanz 19/7/0): **🟡 vorerst**, weil Cluster 3 (P8-20/21/22/24 Verhalten) + Cluster 5 (P8-5/P8-8) noch offen sind; erst nach allen Clustern ist die Bilanz 22+ ✅ und der Sprung auf ✅ sauber begründet. Alternative: nach den nächsten 5-7 ✅-Zeilen (Ziel 23-25) direkt ✅.

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
2. **Link-Picker-Knopf** (Lupen-Symbol im Kopfdaten-Panel, `editor.js:88-100
   _appendLinkId`, Phase 8 Block B Step B4) — öffnet eine Item-Suche, hängt die gewählte
   `itm_…`-ID an das **Frontmatter-Feld `links:`** an (Komma-Konvention). Dient
   ausschließlich dem Verknüpfungs-Graphen (`linkscan.py` liest dieses Feld für
   Graph-Kanten) — wird **nirgends als Text oder Link gerendert**.
   **[2026-09-03 Korrektur, P8.5 Step 0.3]:** Stand vorher „Büroklammer-Symbol", `app.html:183`
   rendert aber `<use href="#i-search">` (`#i-search` aus dem Lucide-Sprite, eingeführt in
   Phase 8 Block C2). `docs/UPDATE_LOG.md` (2026-09-01) sagt bereits korrekt „Lupe".
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

## Session stopped — 2026-09-02 (Fixes A/B/C aus §9.4.6 gebaut: Settle-Zeit, Foreign-Farbe, Knotenklick)

**Auftrag:** Nikinger hat die drei in Plan §9.4.6 vorgelegten Befunde entschieden — Option
**(a)** für alle drei, bei Befund A mit einer Verschärfung (beide Konstanten statt nur
`ALPHA_DECAY`). Auftrag: die drei Fixes bauen, mit den bereits existierenden Smokes
(`p8_22_smoke.py`, `phase8_e2e_smoke.py`) verifizieren, Doku im selben Commit nachziehen. Zwei
Korrekturen an der Options-Vorlage selbst waren Teil des Auftrags: Option A(b) war
arithmetisch nie tragfähig (`ALPHA_MIN` 0.005→0.02 allein ergibt ~259 Ticks ≈ 4.31 s, weiterhin
über dem Budget), Option B(a)s Begründung "analog zu `serializers.py`s `shared`-Feld" war
falsch (dieselbe Näherung wie der Bug, kein Vorbild — das echte Vorbild ist `/api/v1/spaces`).

**Fix A — `phase5_ui/webui/static/js/graph.js`:** `ALPHA_MIN` 0.005→0.01, `ALPHA_DECAY`
0.985→0.97 (Zeilen ~71-72). Modul-Header-Kommentar (Zeilen 19-29) von der widerlegten
Behauptung "200 Knoten erreichen Ruhe in <3s" auf die gemessene Wahrheit + die neue Rechnung
umgeschrieben, mit Datum. `MAX_TICKS_REDUCED = 300` unverändert gelassen, aber kommentiert:
nicht mehr die bindende Grenze für `prefers-reduced-motion` (Schleife endet jetzt schon bei
~151 Ticks am `ALPHA_MIN`-Abbruch).

**Fix B — `phase5_ui/webui/api.py :: _graph_get`:** Knoten-Feld `"shared": i.space !=
session.space` ersetzt durch `"writable": _writable(i.space)`, wobei `_writable()` eine lokale
Closure ist, die `permissions.can_write(session.space, space)` **pro Space memoisiert**
(ein `dict` außerhalb der List Comprehension — bei 200 Knoten ~3 Aufrufe statt 200). Kein neuer
`mcpserver`-Import (P5-B-Disziplin: weiterhin nur `SharePolicy`, `permissions` war als Parameter
bereits im Scope der Factory). Docstring korrigiert (war "acht Felder", die Liste hatte immer
neun) + neuer Absatz, der erklärt, woher `writable` kommt und warum NICHT `serializers.py`
das Vorbild ist. `phase5_ui/webui/static/js/graph.js :: nodeColor()` auf `n.writable` statt
`n.shared` umgestellt, Kommentar korrigiert (behauptete vorher fälschlich, `spaceCategory()`
werde hier nicht benutzt — der Code rief sie längst auf).

**Fix C — `phase5_ui/webui/static/js/graph.js`:** `selectItem` aus `editor.js` importiert
(kein Zyklus — nur `app.js` importiert `graph.js`). Neue Konstante `CLICK_SLOP = 4`, neuer
Modul-Zustand `pressStart`. `onMouseDown` merkt sich `{x, y, node}` (node `null` bei
Hintergrund-Press). `onMouseUp` vergleicht die Pointer-Position gegen `pressStart`; bei einer
Bewegung < `CLICK_SLOP` UND einem getroffenen Knoten: `selectItem(pressStart.node.id)
.catch(reportUnexpectedError)`. **Die im Plan benannte Falle vermieden:** `mouseup` und
`mouseleave` teilten sich vorher denselben Handler — mit der neuen Klick-Erkennung hätte ein
Drag, das den Canvas verlässt, eine Selektion ausgelöst. Eigener `onMouseLeave`-Handler
registriert (nur Reset, nie `selectItem`), `mouseleave`-Listener umgehängt.

**Tests (`phase5_ui/tests/test_graph.py`):** `shared` → `writable` in der bestehenden
Happy-Path-Assertion + im Neun-Felder-Set (Kommentar von "acht" auf "neun" korrigiert). Neuer
Test `test_graph_node_writable_reflects_space_level_write_grant`: zwei fremde Spaces, einer nur
`read:`-geteilt (`writable: False` erwartet), einer `write:`-geteilt (`writable: True`
erwartet) — der eigentliche Regressionswächter für den Bug, ohne den er lautlos zurückkommen
könnte. 9/9 `test_graph.py` grün, Gesamtsuite 959/959 (958 + 1 neu).

**Verifikation — die Smokes sind der Beweis, keine Proxy-Metrik:**

1. `pytest -q` → **959/959 grün** (261 s). Kein Tabu-Diff-Treffer (`phase4_auth/`,
   `phase2_mcp/`, `webui/security.py`, `storage/{models,frontmatter,files,patch,acl,history}.py`
   — leer).
2. `ui_budget.py` → **5/5 grün**, `app.js + app.css + Font (gzip)` **125.8 KB** (vorher 124.2 KB,
   +1.6 KB durch `graph.js`-Wachstum — weiterhin weit unter dem 250 KB-Budget).
3. **200-Knoten-Wegwerf (Port 18772) + `p8_22_smoke.py` (e2e-venv): 5/5 Kriterien, im ersten
   Versuch 4/5** — Station "Tag-Toggle" schlug fehl (`#overview-graph-toggle-tags` "element is
   not visible"), weil `step3_interaction`s Drag-Simulation `mouseup` an der ursprünglichen
   `target`-Position statt der zuletzt gedraggten Position feuerte: mit Fix C sah das nach
   einem Klick auf den Knoten aus, `selectItem` navigierte weg von der Übersicht, die Toggle-
   Checkbox verschwand aus dem DOM. Root Cause gefunden (nicht geraten — `dx=dy=0` zwischen
   `mousedown`- und `mouseup`-Koordinaten im Skript nachgerechnet), `p8_22_smoke.py` korrigiert
   (`mouseup` feuert jetzt an `dragEndX/dragEndY`, mit Kommentar). Zusätzlich: der `[FUND]`-Print
   über `shared` vs. `writable` in `step1_payload` durch eine echte Assertion ersetzt
   (`own > 0 and shared > 0 and foreign > 0`), Text auf Vergangenheitsform + Fix-Datum
   umgeschrieben. Danach durchgehend grün: **sichtbare Ruhe 2694.6 ms** nach dem ersten
   Animationsframe (Budget 3000 ms; drei weitere Läufe zwischen 2650–2740 ms), **152 Ticks in
   2509.2 ms**, Frame-p50 16.7 ms (60 fps, unverändert nicht compute-bound); `/api/v1/graph`
   liefert **120 own / 50 shared / 30 foreign** (vorher wäre `foreign` strukturell 0 gewesen);
   Interaktion ohne Hakeln (hover/drag/wheel p95 < 1 ms, wheel-Ausreißer bis 6.5 ms, weit unter
   dem 16.7 ms-Budget); Tag-Toggle mit >15-Riegel wirkt; `prefers-reduced-motion` 0
   `graph.js`-Frames, Canvas über 600 ms unverändert. Zwei Screenshots überschrieben
   (`p8_22_01_200_knoten.png`, `p8_22_02_reduced_motion.png` — beide zeigen nach Fix B jetzt
   sichtbar graue Knoten). **Alter Stand vorher gesichert:** `p8_22_01_vor_settle_fix.png`
   (Vorher-Vergleich, ausschließlich blau/türkis, kein Grau) — visuell gegengeprüft (Read auf
   beide Bilder): die neue Layout-Verteilung ist der alten vergleichbar dicht/verteilt, kein
   sichtbares Verklumpen — Fix A freigegeben, kein Rückfall auf Option (c).
4. **Kombinierter E2E-Ritt (`phase8_e2e_smoke.py`):** erst gegen den 200-Knoten-Wegwerf
   versucht (wie in der Aufgabe vorgeschlagen) — Station 3 (globaler Scope, Idempotenz über
   zwei Zeilenzahl-Lesungen) brach mit 40→50 Zeilen zwischen den Lesungen, ein Effekt aus
   `DEFAULT_LIMIT=50` (`webui/api.py`) plus DOM-Render-Timing bei 200 Items, **ohne
   Zusammenhang mit den drei Fixes** — laut Aufgaben-Fallback auf den **D2-Wegwerf (Port
   18768)** gewechselt. Dort **6/6 Stationen grün**, inklusive der neuen Station 6
   (Knotenklick → Item: Klick auf einen `beta`-Knoten öffnete die Nur-lesen-Ansicht "Beta Notiz
   zwei", Screenshot `p8_24_03_nach_knotenklick.png` zeigt sie). **Zweiter Skript-Bug
   gefunden+behoben:** `station6_node_click` prüfte `#editor`/`#readonly-view`/`.readonly`/
   `#readonly-title` — keine dieser IDs/Klassen existiert in `app.html` (echt: `#detail-editor`/
   `#detail-readonly`/`#ro-title`, `phase5_ui/webui/static/app.html:126-140`). Ohne diesen Fix
   hätte Station 6 **auch bei funktionierendem Klick** weiter FAIL gezeigt — beim Nachprüfen
   aufgefallen, weil `#field-title` (korrekt) schon einen echten Knotentitel lieferte, während
   `editor_open`/`readonly_open` beide 0 blieben. `[FUND]`-Text im Skript auf den neuen,
   tatsächlichen Fehlerfall umgeschrieben (öffnet das Item nicht / falsche Selektoren), Docstring
   der Funktion trägt die Korrekturnotiz. Drei Screenshots überschrieben (`p8_24_01..03`, jetzt
   vom D2-Datensatz statt vom 200-Knoten-Datensatz — historisch identische Dateinamen, neuer
   Inhalt).
5. **Beide Wegwerf-Instanzen sauber abgebaut** (`wegwerf_setup_200knoten.py cleanup`,
   `wegwerf_setup_d2.py cleanup`, je PID-Datei, kein `pkill -f`). **Produktion unangetastet:**
   `systemctl show sharefyx-mcp.service -p MainPID,ActiveEnterTimestamp` → `MainPID=195922`,
   `ActiveEnterTimestamp=Wed 2026-09-02 11:51:57 CEST` — identisch vor und nach der gesamten
   Sitzung, kein `systemctl`-Verb ausgeführt.

6. **Unabhängige Nachverifikation durch Claude Code (Opus), 2026-09-02 abends.** Der
   ausführende Sonnet-Agent lief nach Punkt 5 in ein Session-Limit (HTTP 429), **bevor** er
   committen konnte; Claude Code hat den Stand übernommen, den Diff Datei für Datei gelesen und
   **beide Smokes selbst neu gefahren** statt die Zahlen des Agenten zu übernehmen — die
   Wegwerf-Instanzen waren zu dem Zeitpunkt bereits abgebaut, also frisch aufgesetzt:
   - 200-Knoten-Wegwerf (Port 18772, neu aufgesetzt): `p8_22_smoke.py` **5/5**, sichtbare Ruhe
     **2685.5 ms** (Agent maß 2694.6 ms — Differenz im Rauschen), **152 Ticks in 2511.4 ms**,
     Frame-Abstand p50 16.7 ms / max 19.4 ms, `/api/v1/graph` **120 own / 50 shared / 30
     foreign** über 200 Knoten und 206 explizite Kanten (Fix B: alle drei C3-Kategorien real
     besetzt, vorher wäre `foreign` strukturell 0 gewesen), hover/drag/wheel p95 ≤ 0.5 ms,
     `prefers-reduced-motion` 0 `graph.js`-Frames.
   - D2-Wegwerf (Port 18768, neu aufgesetzt): `phase8_e2e_smoke.py` **6/6**, Station 6
     `editor_open=1`, angezeigter Titel „Erste Notiz" = Knotentitel (dieser Lauf traf einen
     eigenen `alpha`-Knoten, der Lauf des Agenten einen fremden `beta`-Knoten mit
     Nur-lesen-Ansicht — beide Pfade grün; die drei `p8_24_*`-Screenshots stammen aus diesem
     zweiten Lauf und wurden entsprechend nachgezogen).
   - `pytest -q` **959/959 grün in 257.86 s** (eigener Lauf, Exit 0 — bestätigt die Zahl des
     Agenten: 958 vorher + 1 neuer Regressionstest), `ui_budget.py` 5/5 („Alle 5 Messgrößen im
     Zielkorridor"), Tabu-Diff §0.4 leer (eigener Lauf), nach dem Abbau kein Port 187xx mehr offen, Produktion weiterhin `MainPID=195922` /
     `ActiveEnterTimestamp=Wed 2026-09-02 11:51:57 CEST` (Journal: genau ein Stop/Start heute,
     11:51:57 — der Nikinger-Restart vom Vormittag, Stunden vor dieser Sitzung).

**Nicht Teil der drei Befunde, aber notwendig, um sie zu verifizieren — zwei Bugs in den
Smoke-Skripten selbst behoben** (siehe Punkte 3/4 oben): `p8_22_smoke.py`s Drag-Mouseup-Position
und `phase8_e2e_smoke.py`s Station-6-Selektoren. Beide waren vor Fix C unsichtbar (der alte
`onMouseUp` ignorierte Position/DOM-Zustand komplett), sind jetzt aber echte Voraussetzungen für
eine korrekte Messung — kein Scope-Kriechen, sondern der Preis dafür, dass Fix C tatsächlich
etwas am System ändert, das die Skripte vorher nie beobachten konnten.

**Doku-Updates im selben Commit (Hard Rule 8):**

- `docs/concepts/phase8_ui_graph_plan.md`: §9.4.5-Ledger-Zeile "Neu in P8 (2026-09-02, aus den
  200-Knoten-/E2E-Smokes)" auf "geschlossen in diesem Commit" gesetzt; §9.4.6 um die
  Nikinger-Entscheidung + beide Korrekturen (A(b) arithmetisch tot, B(a)-Begründung falsch)
  ergänzt, Optionen-Text selbst unverändert (Entscheidungsverlauf bleibt lesbar); §3 B3 +
  §5 D2 mit datierten Korrekturnotizen (Feldname, Alpha-Konstanten, Klick-Pfad jetzt gebaut).
- `phase8_ui_graph/CLAUDE.md`: Modul-Status Block-D-Zeile um die drei Fixes ergänzt; §7-Matrix
  P8-15/P8-20/P8-22/P8-24 mit neuen Belegen (Messwerte, Screenshots, Fix-Beschreibung) — **keine
  Zeile auf ✅ gehoben**, alle vier bleiben 🟡 (throwaway-, nicht live-verifiziert). Nebenbei
  einen stehengebliebenen Bilanz-Zähler-Widerspruch korrigiert ("9 🟡 · 2 ⬜" vs. der eigenen
  Aufzählung direkt darunter, die schon 10 🟡/0 ⬜ auflistete) — Drift aus der
  Step-Z-Vorstufen-Session, kein Effekt dieser Sitzung, hier mit Datum gefixt. Bilanz-Zahl
  selbst unverändert (15 ✅ · 10 🟡 · 0 ⬜) — kein Glyphen-Sprung, wie gefordert.
- `docs/INDEX.md`: Frontmatter-`updated:`-Zeile um diesen Eintrag ergänzt.
- Session-Block rotiert (`scripts/rotate_session_block.sh phase8_ui_graph`, nachdem dieser
  Block angehängt war — das Skript verlangt zwei `## Session stopped`-Marker, um etwas zu
  bewegen; mit nur einem meldet es "bereits konform" und tut nichts, wie diese Sitzung
  empirisch bestätigt hat. Der Auftragstext "erst rotieren, dann schreiben" war insofern nicht
  wörtlich ausführbar — mechanisch richtig ist: neuen Block anhängen, dann rotieren).

**Was diese Sitzung NICHT gemacht hat (bewusst, außerhalb des Auftrags):**

- Keine Live-Verifikation, kein Deploy, kein Push. Alle vier Zeilen bleiben 🟡.
- Kein Fix für die weiterhin offenen Restdefekte A3 Klammer/Aufzählung, Item-Link-Picker-Body,
  Picker-A11y (§9.4.1-§9.4.3) — nicht Teil dieser drei Befunde.
- `MAX_TICKS_REDUCED` unverändert (nur kommentiert, nicht geändert — war nicht Teil der
  Nikinger-Entscheidung).

**Commit:** ein Commit für Fixes A/B/C + Test + zwei Smoke-Skript-Korrekturen + alle
Doku-Updates (eine Entscheidungs-Charge, ein Verifikationslauf). Hash wird nach dem Commit vom
Nikinger im `git log` gesehen — diese Notiz zitiert bewusst kein Hash-Präfix (Henne-Ei: die
Notiz ist Teil desselben Commits, den sie beschreibt).

**Verbleibend für die nächste Session (unverändert von vorher):**

- **Nikinger-Sichtprüfung 2 + 3** am echten Gerät gegen den dann deployten v3.0-Build
  (P8-14, P8-15, P8-16, P8-18, P8-19, P8-23) — jetzt inklusive der drei frisch gebauten Fixes.
- **A3 Klammer/Aufzählung** + **Item-Link-Picker-Body-Lücke** + **Picker-A11y** bleiben
  wie dokumentiert (§9.4.1-§9.4.3), keine dieser drei angefasst.
- **Glyphe ✅/🟡** ist weiterhin Nikinger-Entscheidung nach Live-Deploy + Sichtprüfung.

**Keine Push.** Lokaler Commit, bleibt liegen bis zum nächsten deploy-Bündel oder bis der
Nikinger die Fixes + Doku-Update abgenickt hat.
