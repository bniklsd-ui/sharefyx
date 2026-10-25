---
status: archive
purpose: L3-Archiv des Modul-Status und der Vormerkungen des Phase-8.6-Heads — verbatim, in Dokumentreihenfolge
read-when: beim Audit, wenn die Begründung, Messung oder Vormerkung eines Phase-8.6-Steps nachgelesen werden muss
detail: L3
up: ./CLAUDE.md
down:
updated: 2026-10-25 (angelegt in P10.5 Block 12 / DO-1 — `scripts/move_sections.py`, verbatim)
---

## Modul-Status

| # | Modul | Step | Status | Tests |
|---|---|---|---|---|
| 1 | Step 0 — Haushalt + Skelett: Phasenverzeichnis angelegt, sechs kaputte `up:`/`down:`-Links in `p8x_ui_polish_notes.md` gefixt, vier fehlende L1-Cards ergänzt (PROJECT_SESSION_LOG, SICHTPRUEFUNG_RESTBLOCK, SICHTPRUEFUNG_WALKTHROUGH, CLUSTER3_TESTBLOCK), drei `down:`-Listen im Inline-Format korrigiert (phase6_5_tools_images_plan, GLOBAL_SEARCH_PLAN, IMAGES_PLAN), `docs/INDEX.md` auf ≤ 38 KB komprimiert, zwei fehlende INDEX-Zeilen ergänzt (CLUSTER3_TESTBLOCK, THIRD_PARTY_LICENSES), zwei Drift-Korrekturen (`phase8_ui_graph` Softcap-Notiz + `phase5_ui` Behauptung widerrufen), Phasen-Head angelegt | 0 | ✅ | 0 (Skelett, wie P1/P6/6.5/7/8 Step 0) |
| 2 | Step V — **umgesetzt** (Nikinger-Aktion am 2026-09-10): Ollama 0.34.0 via offiziellem Install-Script (`curl -fsSL https://ollama.com/install.sh | sh`; **`apt install ollama` existiert auf Ubuntu 24.04 nicht — Vormerkungen korrigiert**), `qwen3-vl:8b` (Q4_K_M, 6,1 GB, Apache-2.0, neueste Qwen3-VL-Familie, gute UI/Code-Passung, CPU-only OK auf i5-14600KF). MCP-Wrapper `phase8_6_ui_polish/scripts/vision_ollama.py` (~89 Z., `requests.post(/api/generate)` mit base64-Image, `--model/--endpoint` konfigurierbar, Default 600 s Timeout für Cold-Start) **V119-Smoke ✅** (46 s, antwortet korrekt auf Deutsch: „Der Radio-Button ‚als Text-Link im Text' ist markiert"). Backend-Grundlage für V-plugin (siehe nächste Zeile). | V | ✅ (Ollama + V119) | +1 Skript (`vision_ollama.py`), keine pytest-Tests (CLI-Wrapper, manuell gegen `c4_p8519_01_radiogruppe_im_dialog.png` geraucht) |
| 2b | Step V-plugin — **umgesetzt** in dieser Session: `DavidEasden/opencode-vision` v1.3.0 via `npm install github:DavidEasden/opencode-vision` in `~/.config/opencode/` (Plugin-Build via lokalem `tsc`-Lauf im `/tmp/opencode-vision-src`-Klon vor dem Install, weil das `dist/`-Verzeichnis im Repo nicht eingecheckt ist und `prepublishOnly` nur beim `npm publish` greift). **AGPL-3.0-Lizenz-Check** (Nikinger-Wunsch 2026-09-10): Plugin läuft nur lokal in OpenCode-User-Config (`~/.config/opencode/`), keine Sharefyx-Komponente importiert das Plugin oder linked es, keine Verteilung — Lizenzpflichten greifen nicht. Plugin-Config `~/.config/opencode/opencode-vision.json` (`models: ["*"]` für User-level-Wildcard, `imageAnalysisTool: "local_vision_local_vision"` für OpenCode-Tool-Naming-Konvention `<server>_<tool>`). Plugin-Eintrag `"plugin": ["opencode-vision"]` in `~/.config/opencode/opencode.jsonc`. **MCP-Server `local_vision`** (raw JSON-RPC stdio, ~167 Z. Python, `requests.post(127.0.0.1:11434/api/generate)`, qwen3-vl:8b-Default, 600 s Cold-Start-Timeout, stderr-only-Logs per Hard Rule 7) — Datei `phase8_6_ui_polish/scripts/mcp_local_vision_server.py` + Eintrag in `opencode.jsonc`. **`opencode mcp list` 3/3 connected** (Playwright, Websearch, local_vision). **V121-Smoke ✅**: end-to-end durch den MCP-Server gegen `c4_p8519_01_radiogruppe_im_dialog.png` mit Prompt „Was siehst du? Antworte in einem Satz auf Deutsch." — qwen3-vl:8b antwortet korrekt: „Ich sehe eine dunkle Benutzeroberfläche der Anwendung ShareFyx mit dem aktiven Raum ‚alpha', einer Liste von Knoten ... und einem Pop-up-Fenster zum Verknüpfen von Elementen mit Optionen wie ‚als Text-Link im Text' oder ‚als Kante (Feld _Links)'." **[2026-09-11 Korrektur, Step V-vision-befund]** Plugin-Pfad **zurückgebaut** — Messung zeigt, dass er M3s nativen Bildpfad zerstört statt ihn zu öffnen; Details in Zeile 2c. | V-plugin | ⚠️ **zurückgebaut, vollzogen 2026-09-11** (Symlink entfernt, Gegenprobe 0 Tool-Calls) | +1 Skript (`mcp_local_vision_server.py`), 1 Smoke (init + tools/list + tools/call; manuell, nicht Suite-tauglich); ~~Konvention §4 der Schwester-Datei `sichtpruefung_automation_conventions.md` ist jetzt aktiv~~ — **§4 ist in OpenCode gar nicht erfüllbar**, siehe Zeile 2c |
| 2c | Step V-vision-befund — **Messung statt Recherche** (Nikinger-Sonderauftrag 2026-09-11, „die OpenCode-Vision-Route funktioniert nicht wirklich"): `minimax/MiniMax-M3` steht in OpenCodes models.dev-Cache als **`attachment: true`** + `modalities.input: [text,image,video]` (die ganze M2.x-Familie daneben: `false` / `[text]`), Provider über `@ai-sdk/anthropic` gegen `api.minimax.io/anthropic/v1`. **A/B mit `opencode run`** gegen `docs/screenshots/p8_6_block_a_picker_v3ritt.png`, Frage nur aus Pixeln beantwortbar (Zähler „Notizen 6" + orangefarbenes Badge „nur lesen" neben `gamma`): **Lauf A `--pure` (Plugin aus) → 0 Tool-Calls, korrekt** (nativ); **Lauf B (Plugin an) → 9 Tool-Calls**, FilePart vom Plugin gelöscht, `local_vision` 2× `error`, M3 baut sich per `bash`/`curl`/`base64` selbst einen Ollama-Call (5 Fehlversuche); **Lauf C `--pure` + eingebautes `read`-Tool → 1 Tool-Call, `Image read successfully`**, korrekt — ohne `-f`, ohne Plugin, ohne Ollama. **Befund: das Plugin ist nicht die Lösung, es ist der Defekt** — `removeProcessedImageParts()` amputiert bei `models: ["*"]` auch das Modell, das die Krücke nicht braucht; erklärt auch die Paste-Beschwerde (derselbe Hook). `local_vision`-MCP-Server selbst ✅ korrekt (direkt über stdio geprüft) — Ursache ist OpenCodes Tool-Timeout gegen den 46–180 s CPU-Cold-Start von `qwen3-vl:8b`. **Zweitbefund:** Web-UI-Bundle 1.18.30 kennt nur `prompt-*`/`user-message-attachment-image`-Slots, **keinen Assistant-/Tool-Result-Bild-Slot** — Bilder fließen einbahnig Mensch→Modell, Konvention §4 ist in OpenCode **dauerhaft unerfüllbar** und bleibt Claude-Code-only. | V-vision-befund | ✅ (Befund belegt; Rückbau = Nikinger-Entscheidung) | kein Produkt-Code-Touch; Doku: `sichtpruefung_automation_tooling.md` §Messbefund/§Empfehlung/§Historisch, `sichtpruefung_automation_conventions.md` §4-Korrektur |
| 3 | Block A — Fundament: A1 Radiogruppe → `<select, (P8.6-H/I), A2 Layer-/Selektions-Tokens (`--bg-void`/`--select-fill`/`--select-fill-quiet`/`--select-line`/`--select-line-quiet`/`--caution`, P8.6-C/D/E/F), A3 `--border-soft`-Renderfehler-Fix (`app.css:1270/1276` → `var(--line)`, Plan §3.3), A4 Konvention v3 um fünfte Kategorie „Vorsicht" in `phase8_ui_graph/CLAUDE.md` §Selection/Choice-Konvention v3 (P8.6-G) | A | ✅ | 964 → **966** (+2 statische Tests in Block A; `test_link_picker_uses_a_select_not_a_radio_group` ersetzt den P8.5-Test per P8.6-I, `test_no_raw_accent_rgba_outside_root` und `test_every_css_var_reference_is_defined` neu; **Abweichung von Plan §3.5/§8.2:** die anderen 4 Tests (`test_rail_order_…`, `test_account_button_…`, `test_caution_class_only_…`, `test_overview_graph_has_no_max_width`) gehoeren zu Block B/C und werden dort geschrieben, nicht hier — sonst waeren sie in Block A rot und pytest nicht grün, §0.5 Punkt 2 bricht) |
| 4 | Block B — Selektion vereinheitlichen: B1 Hover = leise Standardauswahl überall (`var(--select-fill-quiet)` + `outline` + `border-radius: var(--radius-sm)`, eine konsolidierte Regel statt der drei Flickenteppich-Fassungen), B2 Audit (V113-Befund: `.tree__space` hat im Code kein `aria-current` — anders als Plan §4.2 annimmt; `:not()`-Ausschluss trotzdem korrekt für künftige Reparatur vorbereitet), B3 Einstellungsmenü (`.account-nav`-Klasse statt `.btn`-Plastik für `#account-show-updates`/`#account-manage-spaces`, Navigation statt Aktion), B4 Sweep „alles Klickbare" mit Vorsicht-Kennzeichnung (`class="action--caution"`-Trägerklasse auf `#logout-button` und `#archive-button`, **genau zwei Mitglieder** — Test `test_caution_class_only_on_logout_and_archive` hält das fest), B5 Radien (genau eine Änderung: `.link-picker-results` `6px` → `var(--radius-sm)`, Block A hatte das nicht erwischt) | B | ✅ | 966 → **967** (+1 statischer Test in Block B; **Plan §3.5/§8.2-Abweichung eingehalten** — die drei für Block B vorgesehenen Tests `test_caution_class_only_on_logout_and_archive`/`test_every_css_var_reference_is_defined` (zusammen mit Block A) + `test_link_picker_uses_a_select_not_a_radio_group` (Block A, ersetzt P8.5-Test per P8.6-I) sind grün; `ui_budget.py` 5/5 im Korridor mit app.css 19.8 KB; **drei weitere** Tests aus der Plan-§8.2-Liste (`test_rail_order_…`, `test_account_button_…`, `test_overview_graph_has_no_max_width`) bleiben Block C vorbehalten — sonst waeren sie in B rot, §0.5 Punkt 2 bricht) |
| 5 | Block C — Struktur: C1 „Konto" → „Einstellungen", Lesart b (Einstellungen nach oben, Abmelden ans Rail-Ende, P8.6-J/N3), C2 „Alle Items" unter die Spaces (`tree.js :: renderRail()`, P8.6-J), C3 Map als rechte Spalte / volle Höhe (`.overview` als Grid, P8.6-K/L), C4 Spaces in der Übersicht klickbar (`.overview__space-row` + `<button class="overview__space-open">`, P8.6-P), C5 Ordner-Zähler clientseitig aus `state.items` (P8.6-O) | C | ✅ **geliefert** · ⚠️ **nicht auslieferbar** | 967 → **970** (+3 statische Tests); `ui_budget` 5/5, Tabu-Diff leer. **[2026-09-13, Partial Closeout]** Diese Zeile stand bis heute auf ⬜, obwohl der Block-C-Commit `90c72e2` ihren Nachzug behauptet hat — Hard-Rule-8-Miss, korrigiert. Die Nikinger-Sichtung vom 2026-09-12 hat den Block **nicht abgenommen**: neun UX-Befunde, Details im Session-Block |
| 6 | Block D — Graph-Fixes: D1 V102-Dedup (`dedupeEdges()` ungeordnetes Paar, P8.6-N), D2 deterministischer Layout-Seed (`seedJitter()` FNV-1a-Hash, P8.6-M), D3 `.overview__graph`-Höhe (V112-Gegenprobe — abhaengig von C3, daher mit Block C), **D4 `runSimulation()` `rafId` endlich gelesen + `cancelAnimationFrame`** — die **einzige Scope-Erweiterung** des Plans (P8.6-§6.4: §2.1-Gebiet, aber direkte Ursache von §2.4-Verschlimmerung + 3 Zeilen Fix + schon halb da; **streichen, wenn der Nikinger es in der Sichtprüfung anders sieht**) | D | ✅ (D1, D2, D4) · 🟡 (D3, haengt an Block C) | 966 → 966 (kein Test in Block D, dedup + seed + cancel sind graph.js-intern und durch das Vorhandensein des Codes hinreichend belegt — node-Probe gegen `dedupeEdges()`/`seedJitter()` separat verifiziert, Plan §0.5 ui_budget bleibt grün) |
| 7 | Gate — **GA1+GA2 ✅ 2026-09-18**: Wegwerf-Instanz (Port 18773, PID-Datei, Hard Rule 9) + `p86_polish_smoke.py` neu (14 Stationen aus Plan 2 §7.2, Chromium + Firefox für Station 3/5/8/10) — **18/18 grün** nach drei Korrektur-Runden gegen den aktuellen Code (§7.2s Wortlaut war stellenweise stale, Details im Session-Block). **GA3 ✅ 2026-09-18** — Nikinger-Sichtprüfung der 18 Screenshots; `back-button`-Fund als unkritisch entschieden (`#close-button` + ESC decken „zurück" bereits vollständig ab, der tote Pfeil bleibt liegen, kein Fix nötig). **GA4-D-a ✅ 2026-09-18**: Badge `app.html:20` `v3.0.1` → `v3.0.2`, `docs/UPDATE_LOG.md` neuer `## 2026-09-18`-Block (6 Zeilen). **GA4-D-b ✅ 2026-09-18** — `deploy.sh` durch den Nikinger, Release `/opt/sharefyx/releases/20260918T183907.597248Z`, SHA `1ad2665`, **995 pytest grün im Release** (deploy.sh führt sie selbst aus), automatischer Health-Check des Skripts 3/3 grün. Erster Lauf scheiterte am `git clone` (`Invalid path '.../.git': Permission denied`) — Ursache **kein** Rechte-/Mount-/Platzproblem (alles read-only geprüft, sogar per manuellem Reproduktionsversuch), sondern ein `umask 0177` in der Nikinger-Shell: strippt bei neu angelegten Verzeichnissen auch das Execute-Bit (`0777 & ~0177 = 0600`), macht sie für den eigenen Eigentümer untraversierbar. Fix: `deploy.sh` setzt jetzt `umask 022` selbst statt die der aufrufenden Shell zu erben (Zeile 39-49) + Regressionstest `test_deploy_succeeds_under_a_restrictive_ambient_umask` (setzt `umask 0177` im Testprozess vor `subprocess.run`, reproduziert den exakten Produktionsfehler ohne den Fix, grün mit ihm). **GA4-D-c ✅ 2026-09-18** — echter `health_gate.sh`-Lauf, kein Bericht ohne Beleg (Plan 2 §7.4, genau die Stelle, an der Plan 1 nur behauptet hatte): `--expected-version=v3.0.2 --require-todays-update-log --expected-sha=1ad2665` → **9/9 grün**, `{"result":"ok","actual_version":"v3.0.2","release_sha":"1ad266504c7b709a479666264232490434705102",...}`. | Gate | ✅ **GA1–GA4 alle ✅, Gate abgeschlossen** | 18 Screenshots `docs/screenshots/p86_smoke_*.png`, Report `phase8_6_ui_polish/scripts/p86_polish_smoke_report.json`. **Ein Befund unterwegs gefunden, geklärt:** `#back-button`/`.detail__back` ist toter Code (`app.css:1367` fest `display: none`, keine Override-Regel) — Nikinger-Entscheidung 2026-09-18: unkritisch, `#close-button`+ESC reichen als UI+Tastatur-Weg, kein Aufräum-Zwang. **v3.0.2 ist damit live.** Nächster und letzter Schritt: **Step Z** |
| 8 | Step Z — Closeout: Abnahmematrix §8.1 beider Plaene vollstaendig ausgewertet (**45 ✅ · 5 ⚠️ · 0 ⬜ · 4 ersetzt** von 54 Zeilen), `[VERIFY]`-Register bilanziert (**37 zu · 2 offen: V118, V136 · 2 nachtraeglich: V140/V141**), **Plan 2 §9 als kanonischer Closeout gefuellt** (P8.6-W), Zeiger-Zeile in Plan 1 §9 (die einzige erlaubte Aenderung am 📕-Snapshot), `PHASE8_6_CLOSEOUT_HANDOVER.md` von Partial- auf **Abschluss**-Handover P8.6 → P9 umgeschrieben, `phase8_6_ui_polish_uebersicht.svg` von **PARTIAL CLOSEOUT** auf die Abnahmezahl, Phase-Head/`ROADMAP.md`/`docs/INDEX.md`/Wurzel-`CLAUDE.md` auf ✅, Rotation per Skript | Z | ✅ | `pytest` **995 passed in 117,6 s**, `ui_budget` 5/5 (144,7 KB), Bereichs-Tabu-Diff `440e462^..HEAD` leer bis auf die angekuendigte P8.6-AJ-Ausnahme (2 Dateien, `store.py` 2/2 Zeilen). **Drei Funde in Step Z selbst:** `docs/INDEX.md` war auf **45.870 B** gewachsen (Kriterium ≤ 38 KB, dritter Verstoss der Phase) — im selben Commit gestrafft; **P8.6-18/-19 sind zusaetzlich zu -21/-22 ersetzt** (die Rail-Umkehr N.9 hat sie still umgedreht, Plan 2 §8.1 nannte nur die ersten beiden); **V136 wurde nie beantwortet** — das Nikinger-Feedback vom 2026-09-19 liefert dafuer jetzt einen realen Anlass |
| 9 | **Plan 2 — Step 0'** (Planungssession 2026-09-13): Doku-Hygiene repo-weit verifiziert (0 kaputte Links, 0 fehlende Cards, 0 fehlende INDEX-Zeilen), `docs/INDEX.md` von 38.815 auf **38.471 B** gebracht (sieben geschlossene Phasen-Zeilen gestrafft, −1.549 B; Plan-2-Zeile +1.205 B), Baselines neu gemessen, Anker-Drift gegen Plan 1 belegt | 0' | ✅ | `pytest` **969 passed + 1 Flake** (§1.3), `ui_budget` 5/5 (137,5 KB), `/api/v1/overview` 372,9 ms |
| 10 | **Block E — messen, nicht bauen** (Befund 9): `p86_viewport_probe.py` (CDP, `getBoundingClientRect` + `getComputedStyle` + `elementFromPoint` auf jeden Knopf-Mittelpunkt) bei 1024/1200/1440 px, **zweimal** — gegen die Wegwerf auf aktuellem `main` **und gegen eine zweite Wegwerf auf v3.0.1-Stand** (Methodik-Wechsel 2026-09-14: keine echten Produktions-Creds, Wegwerf-vor-Produktion reicht, ist exakt der Code der läuft). Trennt **9a** (live auf `v3.0.1`) von **9b** (durch Block C eingeführt). **E2a + E2b erledigt 2026-09-14:** Befund **9 banner-abhängig, nicht unconditional** — bei 1200 px **mit** Update-Banner zwei Recent-Items vom `.overview__col-right`-Container überdeckt; **ohne** Banner kein sichtbar unerreichbarer Knopf. **V125 geschlossen: 9a = 9b, gleiche Ursache, falsche Plan-Annahme** — bei 1200 px mit Banner sind die Maße auf main (Block C) und auf v3.0.1 **byte-identisch** (col-left 692×284, col-right 692×284). Block C hat nur die Recent-Items-Reihenfolge geändert, nicht das Layout. Die wahre Ursache ist die 140-px-Banner-Höhe und war schon auf v3.0.1 vorhanden. **V126** (1024 px unerreichbar?) **erledigt**: **0** sichtbare Buttons blockiert, alle 53 hidden-button-Treffer haben `rect=(0,0,0,0)` (data-view="list" blendet die Detail-Buttons aus — separater Mechanismus, kein Layout-Bug). | E | ✅ | +1 Skript (`p86_viewport_probe.py`, 421 Z. / 16 KB), +12 Screenshots `p86_probe_{main,main-clean,v3.0.1,v3.0.1-clean}_{1024,1200,1440}.png`, +4 Probe-JSON `phase8_6_ui_polish/probes/e2{a_main,a_main_clean,b_v3.0.1,b_v3.0.1_clean}.json` (~65 KB je), kein Produktcode, Tabu-Diff §0.3 leer |
| 11 | **Block F — Layering** (Befunde 1+8): `--panel-meta`/`--panel-meta-head`/`--panel-meta-line` verlieren ihren `--warn`-Bezug (gemessen: `rgba(229,169,60,.22)` **ist** `--warn` bei 22 %), Kopfdaten = Layer 2 / Editor = Layer 3 / Append-Zeile = Layer 2, vier rohe Flächen-Hex außerhalb `:root` auf Token (`#0E1116`/`#131A23`/`#1A2029`; `#fff` im QR bleibt) | F | ✅ | 970 → **972** (+2 statische Tests `test_no_raw_surface_hex_outside_root` P8.6-AD + `test_meta_panel_is_not_tinted_with_the_warning_colour` P8.6-AB, beide als byte-genaue Wächter); `ui_budget` 5/5 (130,1 KB, +0,1 KB app.css), Tabu-Diff §0.3 leer |
| 12 | **Block G — Layout-Umbau** (Befund 5, löst 3/4/6/7a mit): `.shell` → **`240px 480px 1fr`** (bewusst ausgelöstes und entschiedenes **P8.6-O2**), Übersicht zieht in den `.list`-Slot, Karte bekommt `.detail` allein, Editor ersetzt sie, **ESC bringt sie zurück**; `state.overview` als einziges neues Feld; `.overview`-Grid + 1280-px-Query **entfallen** (damit auch 9b); P8.6-P wiederhergestellt (ganze Space-Zeile klickbar) | G | ✅ | 970 → **976** (+6 statische Tests: `test_shell_grid_is_240_480_1fr` P8.6-X, `test_overview_lives_in_the_list_slot` P8.6-Y, `test_detail_graph_has_a_definite_height_chain` V112-Wächter nach Umzug §4.2.1, `test_overview_grid_and_its_media_query_are_gone` 9b-Regressionswächter, plus Anpassung von `test_overview_graph_has_no_max_width_or_min_height` an Compound-Selector `.detail__graph .overview__graph`); `ui_budget` 5/5 (141 KB, +10,9 KB durch `.detail__graph`-Kette + Kommentare — Plan §4.9-Erwartung „app.css kleiner" nicht erfüllt, dokumentiert im Session-Block; die +13 KB roh entsprechen ~3 KB gzip); Tabu-Diff §0.3 leer |
| 12b | **Block G-R — Layout-Revision nach Nikinger-Sichtung** (vier Befunde in einem Schritt, eingeschoben zwischen G und H auf Nikinger-Vorgabe 2026-09-14): **G-R.1 Breakpoints** — `@media (max-width: 1280px)` ersetzt durch zwei getrennte Queries: `≤1200px` Rail bleibt 240 / Liste 380 / Detail 1fr (Nikinger-Vorgabe: „Navigationszeile kracht zusammen" bei 1280-er Kollaps), `≤1024px` Stapel-Logik (Liste oben + Karte unten, Nav 240 bleibt sichtbar — Nikinger-Vorgabe: „Übersicht zusammenschieben und nav bar weiterhin vollständig zeigen", nicht Karte wegblenden); data-view-Switching-Logik aus Block G ersatzlos raus. **G-R.2 Map-Leerraum + Layer-Tone** — `.detail { background: var(--bg) }` neu (vorher Body-Erbe `--bg-void = #000`, drei sichtbare Töne für „Spalten-Hintergrund" --bg/--bg-void/--surface statt einem); `.detail__graph { padding: 16px 32px }` statt 32px rundum. **G-R.3 Editor-Header sticky + YAML bündig** — `.editor__head { position: sticky; background: var(--surface-raised); padding-top: 4px }` (Pendant zu `.list__head`, YAML-Kopfzeile rückt um 8 px nach oben); `.panel__head { padding: 11px 24px }` (Item-Row-Höhe ~41 px ≈ Panel-Header-Höhe ~41 px). **G-R.4 Wächter** — `test_shell_grid_is_240_480_1fr` umgestellt (drei Anker statt zwei, neue 1200/1024-Werte), vier neue Tests: `test_1200_breakpoint_keeps_rail_at_240`, `test_1024_breakpoint_stacks_list_over_detail`, `test_detail_uses_the_column_background_not_void`, `test_editor_head_is_sticky_with_the_list_head_background` + `test_panel_head_height_matches_a_list_row`. Mini-Plan `docs/concepts/phase8_6_ui_polish_block_g_r_plan.md` neu. | G-R | ✅ | 976 → **981** (Baseline 970 + 4 G + 2 F + 5 G-R); `ui_budget` 5/5 (**143 KB**, +1,6 KB roh, app.css 73.593 → 77.301 B); Tabu-Diff §0.3 trivial leer; sechs Selbst-Screenshots `p86_block_g_r_{01..06}_*.png` (111/134/110/131/93/128 KB) — Layer-Tone vereinheitlicht, Editor-sticky-Header sichtbar, Rail-240-Bleibt-Verhalten bei 1200 px, Stack-Logik bei 1024 px (Liste oben + Karte darunter, beide sichtbar). **Echter Fund beim Bau:** f-string-Regex-Match in `test_overview_grid_and_its_media_query_are_gone` hatte eine `]`-Klammer zu wenig (das Test-Modul kompilierte nicht) — behoben im selben Commit. |
| 13 | **Block H — Rail + Konto-Dialog** (Befunde 7b, 2): `.rail__account` trägt wieder Einstellungen **und** Abmelden (Abmelden bleibt äußerster Knopf) — **Umkehr von C1/N3-Lesart b**, Test wird umgekehrt und umbenannt; `.account-nav` bekommt eine Navigations-Anmutung (die Knöpfe fehlten nie, sie sahen nur nach Fließtext aus) | H | ✅ | 1 Test umbenannt + 1 angepasst (nested `<svg>`-Regex in `test_app_html_has_a_live_manage_spaces_entry`), 0 neu; `pytest` 981 unverändert, `ui_budget` 5/5 (143,1 KB, app.css 24,0 → 24,2 KB gzip), Tabu-Diff §0.3 leer |
| 14 | **Block H-R — Sichtungs-Revision nach Block H (fünf Sub-Blöcke)** (P8.6-AK-Plan `phase8_6_ui_polish_block_h_r_plan.md`): **H-R.1 OLED-BLACK für die drei Slots** (N.13 = Layer-Architektur-Revision, kein Polish) — `body`/`.shell`/`.rail`/`.list`/`.detail` auf `var(--bg-void) = #000`, `.rail`-`linear-gradient` ersatzlos weg; Layer-3-Elemente (`.overview__graph`, `.update-banner`, `.editor__head`, `.list__head`) behalten ihre `--surface`/`--surface-raised`-Tokens, Karte schwebt sichtbar (14 Stufen Helligkeits-Distanz statt 6); `--rail-top`-Token bleibt im `:root` als Geist stehen (kein Refactor-Scope). **H-R.2 `.account-nav` Akzent-Farbe** (N.14 = Spezialfall Konto-Dialog, "ausnahmsweise" laut Nikinger) — `background: var(--accent-quiet)` + ringsum `border: 1px solid var(--accent-edge)` + `border-left: 3px solid var(--accent)` + Chevron `color: var(--accent)`; Hover `color-mix(in srgb, var(--accent-quiet), var(--accent) 50%)` + `outline: var(--accent-line)`; `.rail__action` (Einstellungen + Abmelden) bleibt unverändert (N.14-Spezialfall nur `.account-nav`). **H-R.3 Editor-YAML-Bündigkeit** — `.editor__head padding-bottom` 12 → 40 px (`calc(var(--space) * 1.5)` → `* 5`), Editor-Head-Unterkante wandert von y=198,80 auf y=226,80 (1440 px) — Diff zur .list__head-Unterkante (y=225,94) **0,86 px ≤ 2 px Toleranz** (pre-fix: 27,14 px). **H-R.4 1024-er Map-Overlap** — V143-Probe misst **0 Rechteck-Schnittmenge** zwischen .list/.detail__graph/.rail bei 1024×768 (Übersicht + Editor); bestehende Stapel-Logik (`grid-template-rows: 1fr 1fr` + `.rail { grid-row: 1 / span 2 }` + `.detail { grid-column: 2 }`) ist korrekt — **kein CSS-Fix nötig, nur Wächter**. **H-R.5 1024-er Editor-Modus** — V144-Probe misst 16/16 Knöpfe `reachable: true`, keiner offscreen bei 1024×768; **kein CSS-Fix nötig, nur Markup-Wächter**. | H-R | ✅ | 981 → 988 (Teil 1: 1 Test umbenannt + 6 neue Wächter) → **991** (Teil 2: 3 neue Wächter für H-R.3/.4/.5); `ui_budget` 5/5 (**143,7 KB**, app.css 24,2 → 24,8 KB gzip, +0,6 KB für Block-Kommentare + Padding-Touch + Wächter-Komment); Tabu-Diff §0.3 leer; 5 Selbst-Screenshots `p86_block_h_r_{01..05}_*.png` (100/99/132/76/91 KB) — bei 1440 ist die YAML-Kopfzeile bündig zur .list__head-Unterkante, bei 1024 sind Liste oben + Karte unten sauber gestapelt, Editor-Knöpfe alle im unteren Slot sichtbar; CDP-Proben `probes/v142_v143_v144_{pre,post}_fix.json` (~9 KB je) |
| 14b | **Block H-R-3 — Claude-Code-Session, drei UX-Befunde aus der H-R-Teil-2-Sichtung** (`docs/concepts/phase8_6_ui_polish_block_h_r_3_escalation.md`): **H-R.6** (Befund 2, Umkehr von G-R.1, Nikinger-bestätigt 2026-09-17 „bei 'ohne Map' Entscheidung bleiben") — bei ≤1024 px eine Zeile statt zwei, `.detail__graph { display: none }` unabhängig vom JS-`hidden`-Attribut. **H-R.7** (Befund 3, Editor-Fullview bei ≤1024 px) — `.shell[data-view="detail"] { grid-template-columns: 1fr }` + `.rail { display: none }` innerhalb der 1024-Media-Query. **H-R.8** (Befund 1, Lesart b — Lesart a verworfen: ihre Prämisse „beide Rail-Knöpfe redundant" [V110] ist seit Block G/Plan 2 §4.3 überholt, `#home-button`/`.tree__scope` sind seither getrennte Aktionen) — `.shell[data-view="detail"] { grid-template-columns: 240px 1fr }` + `.list { display: none }` **ohne** Media-Query-Wrapper, gilt bei 1440/1200/1024 gleichermaßen. **Kein JS-/HTML-Touch nötig** — `shellEl.dataset.view` togglet bereits seit Block G zwischen „list"/„detail" (`editor.js` Zeilen 58/82/427), nur bislang ohne CSS-Konsument; ESC/× liefen schon vor diesem Block durch `closeEditor() → clearDetail() → showOverviewPane()`. | H-R-3 | ✅ | 992 (991 + 1 netto: zwei alte G-R.1-Tests `test_1024_breakpoint_stacks_list_over_detail` + `test_1024_no_overlap_in_css` waren nach dem Wegfall der Stapel-Logik reine Duplikate — ersterer umbenannt/umgeschrieben zu `test_1024_breakpoint_has_single_row_no_map`, zweiter gelöscht statt ein drittes Mal dieselben toten Grid-Properties zu prüfen; `test_shell_grid_is_240_480_1fr`s Anker 3 auf `grid-template-rows: 1fr` [statt `1fr 1fr`] nachgezogen; +2 neu `test_1024_editor_fullview_hides_rail_and_list` + `test_editor_open_hides_list_at_all_viewports`. **Abweichung von der Escalation-Report-Schätzung** (991 unverändert): die Schätzung kannte nur einen G-R.1-Test, tatsächlich gab es zwei). `ui_budget` 5/5 (144,2 KB gzip, +0,5 KB); Tabu-Diff §0.3 leer (nur `app.css` + `test_static_routes.py`); vier Selbst-Screenshots + Live-CDP-Probe `p86_block_h_r_3_self_check.py` gegen Wegwerf v3ritt (Port 18773, PID-Datei gestoppt) bestätigen alle drei Locks pixelgenau (`probes/h_r_3_probe.json`) |
| 15 | **Block J — `pytest`-Flake behoben** (P8.6-AJ, datierte Tabu-Ausnahme): `crypto.new_public_id()` (Rejection-Sampling gegen führendes `-`) neu unter `new_secret()`; `store.py:294` (`create_client`) + `store.py:393` (`create_family`) auf `new_public_id(16)` umgestellt, die zehn übrigen `new_secret`-Stellen unangetastet; `authctl.py`s `p_revoke.add_argument("--family-id", …)` bekommt einen `help`-Text für den Altbestand (`--family-id=-abc`-Gleichheitsform) | J | ✅ | 992 → **994** (+2 netto: `test_new_public_id_never_starts_with_a_dash` [5.000 Ziehungen] neu, `test_revoke_accepts_a_family_id_starting_with_a_dash` neu, `test_revoke_kills_the_family` auf `--family-id=` umgestellt statt zwei Argumenten — Verteidigung in der Tiefe); Tabu-Probe §6.4 exakt erfüllt (`git diff --stat -- phase4_auth/authserver` → genau zwei Dateien, `store.py` genau 2 geänderte Zeilen); eigener Commit, getrennt von jedem UI-Commit |


## Vormerkungen (nicht Teil eines aktuellen Steps)

- **Echte Domain statt `<node>.<tailnet>.ts.net` — Kandidat P9+ (2026-09-18, aus einem
  Live-Incident, nicht aus UI-Feedback).** Anlass: eine Tailscale-Account-Migration hat den
  Node auf ein neues Tailnet gehängt und damit den Funnel-Hostnamen komplett gewechselt
  (`tail89fc2a.ts.net` → `tail4a8b49.ts.net`) — zweite öffentliche-Adress-Änderung in der
  Betriebsdauer dieses Projekts (erste: der Proxmox-Umzug, dort blieb der Hostname zufällig
  gleich). Volle Herleitung, Diagnose und Fix: `phase3_edge/CLAUDE.md` Session-Block
  2026-09-18. **Warum das ein P9-Kandidat und kein P8.6-Punkt ist:** es berührt keine der neun
  UX-Befunde dieser Phase, sondern Betrieb/Exposure (P3-Eigentum) — passt eher neben oder vor
  den P9-Obsidian-Umbau als in die laufende UI-Politur. **Vorschlag, nicht entschieden:** ein
  CNAME auf den Funnel-Hostnamen (kleinster Schritt, DNS-Eintrag genügt, Funnel bleibt
  TLS-Terminierung) oder später ein eigener Reverse-Proxy mit Let's-Encrypt-Zertifikat
  (größerer Schritt, löst die Kopplung an Tailscale vollständig). Beides braucht eine bereits
  vorhandene oder neu zu beschaffende Domain — **Nikinger-Entscheidung, kein Auftrag an mich,
  eine zu registrieren.**

- **`p8.6 plan 2 (N.6)` — Layout-Reorg + Layering-Konsistenz + schmaler-Viewport + B-Backlog.** Nikinger-Sichtung der Block-C-Screenshots am 2026-09-12 hat sieben UX-Befunde ergeben (siehe Session-Block 2026-09-12 unten: B-Backlog mit Grauton-Inkonsistenz + fehlenden Konto-Dialog-Buttons; C-Befunde Refresh-Karte-Überlappung, kleine Karte, **großer Layout-Reorg-Vorschlag** Spaces + Zuletzt benutzt links + Map rechts + Editor im rechten Slot, Hover-Effekt-Verrutschen, „Alle Items"-Modus ohne Spaces-Übersicht, Rail-Reihenfolge Einstellungen+Abmelden anschließen, Editor-Layering, schmaler-Viewport-Buttons). Eigene Folge-Phase oder Sub-Phase von P8.6 (analog zur P8.6-Planungssession am 2026-09-08 / P8.5-Planungssession am 2026-09-09). Ziel: zweiter Vorabritt + Deploy, der alle sieben Befunde abdeckt. **Vormerkung wird zur aktiven Phase, sobald die nächste Claude-Code-Planungssession startet** — diese Session macht nur die Doku, kein Push + Deploy. **[2026-09-13, Partial Closeout]** Der Teil-Stand liegt jetzt geschrieben vor: `docs/concepts/PHASE8_6_CLOSEOUT_HANDOVER.md` (§4 ordnet die neun Befunde den Locks zu, die sie öffnen) + `docs/concepts/phase8_6_ui_polish_uebersicht.svg`. Plan 2 startet dort, nicht bei null.

- **`docs/INDEX.md` reißt bald den 40-KB-Softcap → eigene Rotationsregel, Kandidat P9**
  (Nikinger-Vorgabe 2026-09-11). Stand nach diesem Commit: **40.812 B, 148 B Reserve**
  zum `find -size +40k`-Limit (40.960 B) — nach dem Hinzufügen der
  `screenshots_latest/`-INDEX-Zeile + der §5-Konventions-Notiz wurden sieben ältere
  `updated:`-Pipe-Einträge gestrafft (Step 0, Migration-Vorbereitung, Step V deferred,
  Step V-vision-befund + Rückbau, Phase 8.6 eroeffnet, P8.5-Z-Closeout — die detaillierte
  Chronik liegt in den Phase-Heads + `SESSIONS_ARCHIVE.md`s, der INDEX ist Landkarte).
  Es ist derselbe Mechanismus, den die Phase-Heads bereits gelöst haben: der Body ist nicht
  das Problem, die **`updated:`-Frontmatter-Kette** ist es (jetzt ~1,5 KB über sieben
  Einträge). *Lösungsrichtung, noch nicht entschieden:* ein `docs/INDEX_UPDATES_ARCHIVE.md`
  (L3) plus eine Rotation analog `scripts/rotate_session_block.sh` — die Regel „ein
  aktueller Eintrag im Kopf, ältere verbatim ins Archiv" existiert schon, sie ist nur nie
  auf den INDEX angewandt worden. **Nicht in P8.6 lösen** (Doku-Struktur-Umbau, keine
  UI-Politur); bis dahin gilt die Handarbeit: pro Session einen alten Pipe-Eintrag straffen.
  **[2026-09-13, Partial Closeout]** Stand jetzt **38.822 B** — die Handarbeit wurde in
  dieser Session ausgeführt (sechs Zeilen geschlossener Phasen gestrafft, zwei neue Zeilen
  für Handover + Grafik aufgenommen). Damit ist **P8.6-4 erstmals erfüllt** (≤ 38 KB, nicht
  bloß unter 40.960 B) — die Zeile war seit Block A verletzt. **Nebenbefund:** der
  Frontmatter-Closer `---` klebte am Ende der `updated:`-Zeile statt auf einer eigenen Zeile
  zu stehen; das Frontmatter war damit formal kaputt. Behoben.
  **Kein Kandidat:** `DOC_LAYERS_CONVENTION.md` anfassen — die ist die byte-identische
  Trading-Bot-Kopie.

- **`screenshots_latest/` + Dateinamen+Checkkriterium-Konvention (Nikinger-Vorgabe 2026-09-11,
  etabliert).** Verzeichnis `screenshots_latest/` am Repo-Root mit Symlinks auf die
  Originale in `docs/screenshots/<phase>_*` — Schnellzugriff für den Nikinger, kein
  zweiter Speicherort. Bei Phasenwechsel: alte Symlinks weg, neue anlegen, README mit
  Tabelle + Checkkriterien ersetzen, `updated:`-Frontmatter ergänzen — alles im selben
  Commit wie die Phasen-Closeout-Doku-Updates. **Chat-Verhalten:** wenn M3/Claude-Code
  einen Screenshot für eine Sichtprüfung aufnimmt, sagt es **immer** im Chat zwei Dinge:
  (a) **Dateiname** (vorzugsweise aus `screenshots_latest/`, nicht der Original-Pfad),
  (b) **kurzes Checkkriterium** (ein bis zwei Sätze, was auf dem Bild zu sehen ist). Ausnahmen:
  reine Build-Belege („Smoke gegen Wegwerf X bestanden, Konsolen-Output als Bild")
  oder programmatische Verifikationen (Regex auf HTML). Volle Beschreibung:
  `docs/concepts/sichtpruefung_automation_conventions.md` §5.

- **P8.6-§6.4 (`cancelAnimationFrame` in `runSimulation()`) — streichbar:** der Fix ist
  drei Zeilen + direkt Ursache von §2.4-Verschlimmerung + schon halb da (`var rafId = null`
  wird zugewiesen, aber nie gelesen). Wenn der Nikinger in der Sichtprüfung anders entscheidet,
  ist es die einzige Scope-Erweiterung dieser Phase und wird in Block D gestrichen.
- **„Ordner umbenennen" → P9 oder danach** (Plan §0.4.1, bewusst draußen mit Analyse):
  die billige Frontend-Fassung verliert eine `.share.yml`-Freigabe still als Nebenwirkung
  einer Umbenennung (Hard Rule 4 — Rechte als Nebenwirkung); ein vollständiger Weg bräuchte
  `Store.rename_folder()` und wäre die neunte P1-Contract-Öffnung, die P8.6-S gerade zusperrt.
  Analyse ist der Ersatz für die Wiederholung der Untersuchung — wer das Feature plant, startet
  hier, nicht bei null.
- **Radiogruppe → `<select>`** (P8.6-H, Umkehr der P8.5-19-Entscheidung von 2026-09-06, die
  Nikinger selbst am 2026-09-08 umgekehrt hat): die Beschriftung **innerhalb** der Box
  (kein externes `<label>`), Kategorie *Choice* der Selection/Choice-Konvention v3 wieder
  hergestellt. `localStorage["sfx:linkpicker:mode"]` und sein Wert bleiben unverändert.

- **Vision-Backend: lokales Modell statt API** (Nikinger-Entscheidung 2026-09-10,
  umgesetzt 2026-09-10 in zwei Etappen): Proxmox-Migration durch (i5-14600KF,
  sharefyx-mcp PID 991 nach Auto-Restart); **Etappe 1 (Step V, 2026-09-10)** —
  Ollama 0.34.0 via offizielles Script + `qwen3-vl:8b` gepullt + MCP-Wrapper
  `phase8_6_ui_polish/scripts/vision_ollama.py` (~89 Z., CLI gegen
  `/api/generate`, V119-Smoke ✅ in 46 s).
  **Etappe 2 (Step V-plugin, 2026-09-10, diese Session)** — Plugin **doch
  installiert**, auf Wunsch des Nikingers („benutzen, reicht eine Erwähnung").
  AGPL-3.0-Check: Plugin läuft nur lokal in OpenCode-User-Config
  (`~/.config/opencode/node_modules/opencode-vision/dist/`), wird von keiner
  Sharefyx-Komponente importiert oder gelinked, keine Verteilung — Lizenzliche
  Pflichten greifen nicht (kein „convey" im AGPL-Sinn, kein Netzwerk-Service
  mit dem Plugin als Bestandteil). Lizenzhinweis bleibt als Audit-Spur in der
  Phase-Doku; **kein** README-Eintrag nötig (kein modifiziertes Derivat, keine
  Weitergabe). **Installationspfad:** Repo nach `/tmp/opencode/opencode-vision-src`
  geklont, `npm install` + `npm run build` (TypeScript-Compile), dann
  `npm install /tmp/opencode/opencode-vision-src` aus `~/.config/opencode/`
  heraus — der `dist/`-Ordner ist im Repo nicht eingecheckt (`files: ["dist"]`)
  und `prepublishOnly` läuft nur bei `npm publish`, nicht bei `npm install
  github:...`. **Plugin-Config** `~/.config/opencode/opencode-vision.json`
  mit `models: ["*"]` (Wildcard für alle Modelle, Nikinger-Vorgabe) +
  `imageAnalysisTool: "local_vision_local_vision"` (OpenCode-Konvention
  `<server>_<tool>` aus den Docs; das `mcp_`-Präfix aus dem Plugin-README ist
  Claude-Desktop-Konvention, nicht OpenCode). **MCP-Backend** `local_vision`
  (raw JSON-RPC stdio + `requests.post(127.0.0.1:11434/api/generate)`,
  qwen3-vl:8b-Default, 600 s Cold-Start-Timeout) — Datei
  `phase8_6_ui_polish/scripts/mcp_local_vision_server.py` + Eintrag in
  `opencode.jsonc`. **`opencode mcp list` zeigt 3/3 connected** (Playwright,
  Websearch, local_vision). **V121-Smoke ✅** end-to-end durch den MCP-Server
  gegen `c4_p8519_01_radiogruppe_im_dialog.png` — qwen3-vl:8b antwortet
  korrekt auf Deutsch. Konvention §4 der Schwester-Datei
  `sichtpruefung_automation_conventions.md` ist damit **aktiv** für die
  nächste Session.
  **Backend (korrigiert 2026-09-10 nach Ollama-Library-Suche):**
  `qwen3-vl:8b` (Q4_K_M, 6,1 GB, Apache-2.0, neueste Qwen3-VL-Familie, gute
  UI/Code-Screenshot-Passung) auf Ollama 0.34.0; MCP-Wrapper ruft `POST
  /api/generate` mit base64-Image. **V119-Smoke ✅** in 46 s
  (qwen3-vl:8b Cold-Start + Vision-Encoder + 60 Token Decoding auf
  i5-14600KF CPU-only). **Proxmox-Settings (Vorlage, abgearbeitet):**
  - **Host 1 (i5-14600KF, 6 P-Cores + 8 E-Cores, 20 Threads) — AKTIV:** 12 vCPUs
    = 6 P-Cores (CPU-Typ `host`, gepinnt auf Cores 0–5) + 4 E-Cores; 16 GB
    RAM (Ballooning aus); 50 GB Thin-LVM auf SSD (`local-lvm`); statische
    IPv4 im Cluster; Ollama lauscht auf `127.0.0.1:11434` (kein
    öffentliches Binding — MCP-Bridge spricht intern). P-Cores tragen
    100 % der Vision-Inference-Last; E-Cores übernehmen MCP-Server-Handler
    und Ollama-Stream-Pool.
  - **Host 2 (Ryzen 7 5800X, 8 Cores, 16 Threads, Zen 3):** 10 vCPUs = 8 Cores
    + 2 Threads; CPU-Typ `host`; 16 GB RAM; 50 GB; Netzwerk identisch.
  - **Modell-Recherche (Stand 2026-09-10, gegen Ollama-Library
    https://ollama.com/search?q=vision):**
    `qwen3-vl:8b` ✅ — neueste Qwen3-VL-Familie, 6M Pulls, Apache-2.0, beste
    UI/Code-Passung (Erstwahl, in der VM live verifiziert).
    `qwen2.5vl:7b` — Vorgänger-Familie, 4,8M Pulls (Fallback).
    `llava:13b` — klassisch, 14,8M Pulls (gut getestet, aber UI/Code
    schwächer als Qwen3-VL).
    `minicpm-v:8b`, `llama3.2-vision:11b` — Alternativen.
    `internvl2.5:8b` ❌ — **existiert nicht** auf der Ollama-Library
    (ursprüngliche Empfehlung, Recherche-Fehler).

- **Proxmox-Migration — Aktionsliste (Nikinger, 2026-09-10, „kurz und knackig
  Aktion → Command-Liste")** für die Migration von Mini-PC
  `savefyx-VMware-Virtual-Platform` (sharefyx-mcp.service PID 355956,
  `ActiveEnterTimestamp=2026-09-05 16:10:18 CEST`, **aktuell noch hier**) auf
  i5-14600KF (primär) bzw. Ryzen 7 5800X (sekundär). **opencode/M3 schreibt nur
  Doku + das MCP-Wrapper-Skript (Schritt 5);** alle `sudo systemctl`-/Proxmox-
  Befehle sind Nikinger-Aktionen (Hard Rule 9 + §0.5.7).

  **Schritt 1 — sharefyx-mcp + Funnel pause (Nikinger, Vordergrund-Shell):**
  ```
  sudo systemctl stop sharefyx-mcp
  sudo systemctl stop tailscaled
  ```
  Verifikation: `systemctl status sharefyx-mcp` → `inactive (dead)`,
  `pgrep -af sharefyx-mcp` liefert nichts. PID 355956 erst beim **Re-Start**
  verschwinden — vor dem Pause **nicht** festhalten, da D2-Deploy erfahrungsgemäß
  den Dienst erwartungsgemäß neu startet.

  **Schritt 2 — VM migrieren (Proxmox, je nach Storage):**

  *Live-Migration* (passende Shared Storage, beide Nodes sehen den Storage):
  ```
  qm migrate <VMID> <target-node> --online --with-local-disks
  ```

  *Cold-Migration* (Default, lokales `local-lvm` — Disk muss mit):
  ```
  qm shutdown <VMID> --timeout 60
  ```
  → in Proxmox-UI: VM auf Ziel-Node verschieben + CPU-Typ auf `host` setzen
  → wieder starten:
  ```
  qm start <VMID>
  ```

  *Re-Build* (nur wenn Mini-PC-Settings nicht passen — z. B. BIOS-Typ):
  ```
  qm stop <VMID>
  qm export <VMID> /tmp/sharefyx-export.vma.zst --format vma_zstd
  # auf Ziel-Node: neue VM anlegen, dann
  qm importdisk <new-vmid> /tmp/sharefyx-export.vma.zst <target-storage> --format vma_zstd
  ```

  **Schritt 3 — VM-Resources setzen (i5-14600KF primär):**
  ```
  qm set <VMID> --cores 12 --sockets 1 --cpu host --numa 0
  qm set <VMID> --memory 16384 --balloon 0
  qm set <VMID> --scsihw virtio-scsi-single --scsi0 local-lvm:50,iothread=1,discard=on
  ```

  **CPU-Pinning** (nur i5-14600KF; Ryzen 7 5800X braucht **kein** Pinning —
  Architektur kennt keine P/E-Unterscheidung, alle Cores gleichwertig):
  ```
  # Bestehende affinity-Zeile entfernen (idempotent), dann neue setzen:
  sed -i '/^affinity:/d' /etc/pve/qemu-server/<VMID>.conf
  echo 'affinity: 0-5,12-15' >> /etc/pve/qemu-server/<VMID>.conf
  # Verifikation:
  grep '^affinity:' /etc/pve/qemu-server/<VMID>.conf
  ```
  P-Core-Pinning 0–5 (= 6 P-Cores) + E-Core-Pinning 12–15 (= 4 E-Cores aus
  der hinteren Hälfte). Wirksam erst nach `qm stop <VMID>` + `qm start <VMID>`.

  Bei Ryzen 7 5800X nur `--cores 10 --sockets 1` setzen, kein Pinning.

  **Schritt 4 — Ollama installieren + Vision-Modell pullen (in der migrierten VM):**
  ```
  # Ubuntu 24.04 (noble) hat KEIN 'ollama'-Paket — offizielles Install-Script:
  curl -fsSL https://ollama.com/install.sh | sh
  # Erwartung: Binary nach /usr/local/bin/ollama, systemd-Unit 'ollama.service'
  # (Restart=on-failure, After=network-online.target), lauscht auf 127.0.0.1:11434.

  sudo systemctl enable --now ollama
  ollama --version   # 0.34.0+ verifiziert 2026-09-10
  ollama pull qwen3-vl:8b
  ollama list        # muss qwen3-vl:8b zeigen (Q4_K_M, ~6,1 GB)
  ```
  Ollama bindet per Default auf `127.0.0.1:11434` — **kein** öffentliches Binding
  (MCP-Bridge spricht intern; wäre ein Hard-Rule-1-Berührungspunkt). **iGPU
  (Intel UHD 770) wird nicht genutzt** — Ollama läuft CPU-only. Für V119-Smoke
  (gelegentliche 1-2 Bilder pro Session) ausreichend; nicht für Realtime.
  **Modellname-Korrektur 2026-09-10:** die ursprüngliche Empfehlung
  `internvl2.5:8b` war ein Recherche-Fehler — existiert nicht auf der
  Ollama-Library (Stand 2026-09-10, Suchtag „vision"). `qwen3-vl:8b` ist die
  Erstwahl; Alternativen: `qwen2.5vl:7b`, `llava:13b`, `minicpm-v:8b`,
  `llama3.2-vision:11b`. Alle über `--model <name>` im Wrapper umschaltbar.

  **Schritt 5 — MCP-Wrapper-Skript (opencode/M3, ✅ 2026-09-10):**
  Datei `phase8_6_ui_polish/scripts/vision_ollama.py`, 89 Zeilen Python (Spec
  Aktionsliste sagte „~50 Z."; die zusätzlichen Zeilen sind argparse-Help,
  Fehlerausgabe nach stderr, Exit-Codes 0/2/3/4). Spec:
  `requests.post("http://127.0.0.1:11434/api/generate", json={"model":
  "qwen3-vl:8b", "prompt": "...", "images": ["<base64>"], "stream": False})`.
  CLI: `--image <pfad>` + `--prompt <text>` + `[--model <name>]` + `[--endpoint
  <url>]`, Stdout = Model-Antwort. Liegt im Phase-Verzeichnis, weil das die
  einzige Stelle ist, an der Skripte leben dürfen, die zur Phase gehören.
  **Voraussetzung für Venv-Aufruf:** `requests` muss im Projekt-venv
  installiert sein (`.venv/bin/pip install requests`, eine Zeile, hier
  durchgeführt). **[2026-10-02 Korrektur, P9]:** „installiert" hieß nur
  *von Hand ins Dev-venv*, kein `pyproject.toml` deklariert `requests`. Das
  frische Release-venv von `deploy.sh` hat es nicht, und die P9-C6-Tests auf
  `mcp_local_vision_server.py` brachen dort den `v3.1.0`-Deploy ab. Der
  MCP-Server ist seitdem stdlib-only (`urllib`), **dieses CLI-Skript braucht
  `requests` weiterhin** — aus einem Release-venv läuft es nicht.
  **Timeout 600 s** — Cold-Start (Modell-Load 30–60 s +
  Vision-Encoder 5–10 s + Text-Decoding 30–60 s = 80–130 s auf i5-14600KF ohne
  GPU); Steady-State reichen 120 s.

  **Schritt 6 — V119-Abnahme (Smoke gegen echten Screenshot, ✅ 2026-09-10):**
  ```
  .venv/bin/python phase8_6_ui_polish/scripts/vision_ollama.py \
      --image docs/screenshots/c4_p8519_01_radiogruppe_im_dialog.png \
      --prompt "Sind in diesem Dialog zwei Radio-Buttons sichtbar? Welcher ist markiert?"
  ```
  Erwartung: „ja, beide sichtbar; der erste (‚body') ist markiert". **Tatsächlich
  geliefert (2026-09-10, qwen3-vl:8b, 46 s Cold-Start-inkl.):**
  „In dem gezeigten Dialog ‚Item verknüpfen' sind zwei Radio-Buttons sichtbar:
  ‚als Text-Link im Text', ‚als Kante (Feld _Links)'. Der Radio-Button ‚als Text-
  Link im Text' ist markiert." — Antwort auf Deutsch, beide Buttons erkannt,
  richtige Auswahl identifiziert. **V119 damit ✅.**

  **Schritt 7 — Health-Gate (Regression-Schutz, keine manuellen `start`-Calls):**
  ```
  bash phase8_5_picker_release/scripts/health_gate.sh --expected-sha=<HEAD>
  ```
  Erwartung: `health_gate.sh` 8/8 grün. Bei Rot: `journalctl -u sharefyx-mcp
  -n 200` + Diagnose-Block aus `phase3_edge/CLAUDE.md`. V119 erfolgreich → Phase-
  Head Modul-Status V119 🟡 → ✅, neuer `## YYYY-MM-DD`-Block in
  `docs/UPDATE_LOG.md`, V120 (Trigger-Events für Tab-Meta-Notiz) geöffnet.
  **Begründung der Verkürzung (2026-09-10, Restart-Logik entdeckt):** die
  `sudo systemctl start`-Aufrufe sind redundant — siehe „Restart-Logik"-
  Vormerkung unten. Der einzige manuelle Eingriff ist das **`stop`** in Schritt 1
  (zum Lock-Release vor der VM-Migration); nach der Migration sorgt die
  Auto-Restart-Mechanik (systemd `WantedBy=multi-user.target` + `Restart=on-failure`)
  allein für „services sind wieder up".

- **Restart-Logik (Nikinger-Fund 2026-09-10, Verifikation in dieser Session
  gelesen, kein Service-Touch)** — was nach der Proxmox-Migration tatsächlich
  gegriffen hat und damit die `sudo systemctl start`-Aufrufe in Schritt 7
  ersetzt:
  - **`sharefyx-mcp.service`** (`/etc/systemd/system/sharefyx-mcp.service:19-20`)
    trägt `Restart=on-failure` + `RestartSec=5` — Crash-Recovery im 5-Sekunden-
    Takt. Plus `After=network-online.target tailscaled.service` und
    `Wants=network-online.target` (Z. 6-7) — Boot-Reihenfolge ist damit
    deterministisch.
  - **`tailscaled.service`** (`/usr/lib/systemd/system/tailscaled.service:18`,
    vom Paket) trägt ebenfalls `Restart=on-failure`. Wird **nicht** durch eine
    eigene Unit ergänzt — die Vendor-Unit reicht.
  - **Beide Units sind `WantedBy=multi-user.target`** (implizit über
    `[Install]`-Sektion). Nach VM-Boot oder VM-Migration-Recovery starten sie
    ohne `systemctl start`-Aufruf.
  - **Konsequenz für die Aktionsliste:** Schritt 7 ist nur noch Health-Gate.
    Die `stop`-Aufrufe in Schritt 1 bleiben — sie sind **kein Restart-Pfad**,
    sondern Lock-Release für die Migration (Live-Migration blockiert sonst,
    Cold-Migration braucht sauberen State). Der **einzige** Schritt, der einen
    systemd-Aufruf enthält, ist also Schritt 1.
  - **V103-Notiz für den Deploy (P8.6-R):** die ungeklärte P8.5-V-Frage „ist
    der `sudo`-Prompt im Vordergrund sichtbar?" beantwortet sich durch diese
    Mechanik von selbst — beim Deploy nach P8.6 gibt es keinen einzigen
    `sudo`-Call mehr (D-a Agent, D-b Nikinger deployt **ohne** `sudo` falls
    Hard-Rule-9-konform ermöglicht — das ist eine Folge-Diskussion mit dem
    Nikinger, **nicht** P8.6-Entscheidung).

- **Tailscaled-Watchdog (Nikinger-Vorgabe 2026-09-15, Vorfall heute)** — die
  heutige Beobachtung zeigt eine Lücke in der bestehenden Restart-Logik:
  `tailscaled` ist gegen Crashes gesichert (`Restart=on-failure` in der
  Vendor-Unit), **nicht** aber gegen den heute aufgetretenen Fall
  „Control-Plane `controlplane.tailscale.com` lange nicht erreichbar +
  DERP reconnect halbfertig + `tailscale status` zeigt `offline`":
  - **Vorfall 2026-09-15:** VM-Suspend 17:51–21:50 CEST (~4 h) →
    `sharefyx-mcp.service` behält PID 991 (Kernel-freeze, kein Restart
    nötig), `tailscaled` wacht mit `time jump detected, slept 3h59m22s,
    probably wake from sleep` auf, kommt aber nicht mehr auf
    `controlplane.tailscale.com` (5+ min `PollNetMap: context canceled`
    im 60-s-Rhythmus, `tailscale netcheck` meldet DERP ok aber Control-
    Plane timeout). Folge: lokales `sharefyx-mcp` antwortet weiter 200 auf
    `/health`, **aber** `tailscale status` zeigt das Node als `offline`,
    externe Clients routen nicht, Tunnel ist effektiv tot.
    **Heilung:** manueller `sudo systemctl restart tailscaled` durch den
    Nikinger um ~21:55 CEST (5+ min Tunnel-Down user-seitig,
    Hard-Rule-9-konform nicht durch opencode/M3 auslösbar).
  - **Vorschlag (eigene Mini-Phase, nicht P8.6):** eine Watchdog-Unit für
    `tailscaled`, die nicht nur auf Crashes reagiert sondern auch auf
    „Control-Plane lange nicht erreichbar". Drei systemd-native Ansätze,
    alle ohne Code-Touch auf der Sharefyx-Seite:
    1. **`OnFailure=`-Hook** auf eine zweite Unit `[email protected]`
       — sehr einfach, deckt aber nur den Crash-Pfad, nicht den
       „service läuft, Control-Plane klemmt"-Pfad.
    2. **`tailscaled-watchdog.service`** mit `Type=oneshot`,
       `Restart=always`, der per `tailscale netcheck` oder
       `curl --max-time 5 https://controlplane.tailscale.com/machine/map`
       zyklisch prüft; bei Fehlschlag `systemctl restart tailscaled`.
       Hard-Rule-9-konform mit `User=savefyx` + `NoNewPrivileges=true` +
       `ProtectSystem=strict` absicherbar — kein offener Port, kein
       ungehärteter Service.
    3. **Tailscale-eigenes Feature** (Recherche nötig) für automatischen
       Restart nach längerer Control-Plane-Unterbrechung — vermutlich
       keines ohne kommerzielles Add-on.
  - **Scope-Notiz:** alle drei Ansätze berühren `/etc/systemd/system/`
    und sind **nicht** P8.6-Tabu (das gilt nur für `phase5_ui/...py` +
    `phase1_storage/storage` + `phase4_auth/authserver`). Eigene
    Mini-Phase, vermutlich zwischen P8.6 Gate und P9, oder als Schritt
    im nächsten Proxmox-Migrations-Ablauf (Vormerkung
    „Proxmox-Migration — Aktionsliste"). Hard Rule 9 +
    Session-Prompt-Regel „Tunnel bring-up = Nikinger-Aktion" bleiben
    unberührt: der Watchdog **müsste** vom System (systemd) ausgehen,
    nicht von opencode/M3 — der Auslöser ist eine zyklische Prüfung,
    kein manueller Eingriff. Wahl zwischen den drei Ansätzen ist eine
    **eigene Folge-Phase-Entscheidung**, nicht P8.6.

- **Zukunfts-Notes außerhalb des aktuellen Phasen-Scopes (Nikinger, 2026-09-10,
  „would be cool")** — explizit **nicht** P8.6, **nicht** P9, erst notiert:
  - **Tab-Meta-Texte dynamisch** — `<title>sharefyx - {item_title}</title>` beim
    Bearbeiten-Dialog oder Detail-Ansicht statt des aktuellen statischen
    `sharefyx`-Titels. UI-only, vermutlich `app.js :: openDetail()`/
    `closeDetail()` mit `document.title`-Update. Niedrigschwellig; könnte
    Anhängsel an P8.6-Block B werden (P8.6-H/I/J), oder eigene Mini-Phase.
    **[VERIFY] V120** — welche Events den Title-Update triggern sollen
    (Editor-Open, Detail-Open, Spaces-Wechsel, Suche).
  - **Custom 404-Seite** — statt FastAPI-Default-JSON
    (`{"detail": "Not Found"}`) eine HTML-Seite im App-Stil (Logo + „Diese Seite
    gibt es nicht" + Link zur Startseite). Statisches HTML in
    `phase5_ui/webui/static/404.html` + Custom-ExceptionHandler in
    `webui/api.py`. **Vorsicht:** `webui/api.py` ist im P8.6-Tabu (§0.3) — die
    Note gehört in eine Folge-Phase, in der die Tabu-Liste neu bewertet wird.
    Nicht-P8.6, vermutlich P9+ oder eigene Mini-Phase. Niedrigschwellig
    technisch, aber tabu-berührt.

- **Sichtprüfungs-Realität vs. Chat-Beschreibung — Diskrepanz am 2026-09-14 dokumentiert
  (Nachtrag im Block-G-R-Session-Block).** Nikinger: „die Realität ist recht weit weg
  von dem was du hier beschreibst". Konkret: meine Checkkriterien-Texte im Chat zu den
  sechs G-R-Screenshots waren **zu optimistisch** — der schwarze Ring rund um die Karte
  ist tatsächlich weg (Block G-R.2 hat geliefert), aber „drei Töne sind jetzt einer" und
  „YAML-Kopfzeile bündig zur Item-Zeile" waren **geglättete M3-Eigenbeschreibungen**, nicht
  Pixel-Realität. Mindestens drei unterscheidbare Töne bleiben sichtbar (Nikinger:
  „Farbe hinter der Map und der Space/item Übersicht ist unterschiedlich"); die YAML-
  Kopfzeile ist heute bündig zur Item-Reihe, aber **nicht** zur Suchzeile (Nikinger will
  beide Header auf Suchzeilen-Höhe). Drei weitere Sichtungs-Punkte (1024-er Map-Overlap,
  1024-er Editor-Modus, genereller Bedarf nach echter Pixel-Verifikation) sind im Block-G-R-
  Session-Block festgehalten. **Zwei Optionen, beide nur als Vormerkung, keine Entscheidung
  jetzt:** (A) Rückkehr zum manuellen MCP-Vision-Adapter mit lokalem Ollama (qwen3-vl:8b,
  Cold-Start 46–130 s — Batch-Aufruf für mehrere Bilder in einem Prompt reduziert das auf
  einmal Cold-Start; das Plugin drum herum war zurückgebaut worden, weil es M3s nativen
  Bildpfad zerstörte — der Adapter selbst bleibt korrekt und liefert echte, kalibrierte
  Bildbeschreibungen statt geglätteter M3-Eigenbeschreibungen). (B) API-Minimax-m3 als
  getrennte Phase für Sichtprüfung (zwei Modell-Instanzen, ein Prompt-Stereo; substantielle
  Architektur-Änderung, gehört in eine eigene Folge-Phase P9 oder eine neue Phase, nicht
  in P8.6). **Beide Optionen sind explizit kein P8.6-Auftrag** — sie sind Backlog für die
  nächste Phase-Planungssession.
