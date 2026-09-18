---
status: live
purpose: Phase-Head UI-Politur (Selektion + Layout, drei Graph-Fixes, Radiogruppe-Rückbau) → Deploy `v3.0.2` — Scope, harte Regeln, Modulstatus, aktueller Session-Handover
read-when: Arbeiten in phase8_6_ui_polish/ oder an den in §0.3/§3/§4/§5/§6/§7 des Plans genannten Dateien in `phase5_ui/webui/static/` + `phase5_ui/tests/` + `scripts/` — zuerst lesen, zusammen mit dem neuesten Session-stopped-Block
detail: L2
up: ../CLAUDE.md
down:
  - ../docs/concepts/phase8_6_ui_polish_plan.md   # voller Plan, Entscheidungen P8.6-A–P8.6-U, §0.1 gelockte N1–N4, Steps 0/V/A/B/C/D/Gate/Z
  - ../docs/concepts/p8x_ui_polish_notes.md       # Inhaltsquelle §1–§10 (P8.6-A benennt das Verzeichnis)
  - ../docs/concepts/PHASE8_5_CLOSEOUT_HANDOVER.md   # Einstieg für die P8.6-Planung; §4 = die offenen Entscheidungen
  - SESSIONS_ARCHIVE.md                            # ältere Session-Blöcke, newest-first
updated: 2026-09-17 (**Block H-R-3 + Nachtrag + Block J — Kettenkorrektur.** Diese `updated:`-
Kette war seit dem 2026-09-15-Eintrag nicht mehr nachgezogen worden, obwohl seither drei
Commits liefen (Block H-R-3-Bau, Rail-Exklusivitäts-Nachtrag, Block J) — jeweils mit
vollständigem Protokoll im `## Session stopped — 2026-09-17`-Block unten, nur ohne Spiegelung
hierher. Kein Rückwirkungs-Rewrite der Vergangenheit, nur die fehlenden drei Zeilen nachgetragen:
**H-R-3** (drei Locks H-R.6/.7/.8, kein JS-/HTML-Touch, `pytest` 991→992, `ui_budget` 5/5
144,2 KB), **Nachtrag** (Rail-Exklusivität Übersicht vs. Space/Eimer/Ordner in `tree.js`,
`pytest` 992 unverändert), **Block J** (P8.6-AJ, `pytest`-Flake behoben — `crypto.new_public_id()`
+ zwei Aufrufe in `store.py:294/393` + `authctl.py`-Help-Text, `pytest` 992→994, enge Tabu-Probe
`phase4_auth/authserver` exakt zwei Dateien erfüllt). Reihenfolge P8.6-AH jetzt **G→G-R→H→H-R-1+2
→H-R-3→J alle ✅, Gate + Z offen.** Volle Herleitung für alle drei: Session-stopped-Block unten.) |
2026-09-15 (Tailscaled-Control-Plane-Outage heute nach ~4-h-VM-Suspend — `sharefyx-mcp` PID 991 lief ununterbrochen weiter, `tailscaled` wachte mit `time jump detected, slept 3h59m22s` auf, kam aber 5+ min nicht mehr auf `controlplane.tailscale.com` (alle 60 s `PollNetMap: context canceled`, `tailscale status` zeigte `offline`); Heilung durch `sudo systemctl restart tailscaled` (= Nikinger-Aktion, Hard-Rule-9-konform nicht durch opencode/M3 auslösbar). Befund: bestehende Restart-Logik (`Restart=on-failure` greift nur für Crashes, nicht für den „Control-Plane lange nicht erreichbar + DERP reconnect halbfertig"-Fall). Neue Vormerkung „Tailscaled-Watchdog (Nikinger-Vorgabe 2026-09-15)" mit drei Ansätzen (`OnFailure=`-Hook / Watchdog-Unit mit zyklischer `tailscale netcheck`/curl-Prüfung / Tailscale-eigenes Feature) als Mini-Phase nach P8.6 Gate. **Kein** Produktcode-Touch, **kein** Service-Touch — sharefyx-mcp PID 991 + tailscaled PID 926 → 263180 (nach Nikinger-Restart) durchgehend nur gelesen, `health_gate.sh --expected-version=v3.0.1 --expected-sha=6f19a8f` 8/8 grün) | 2026-09-14 (**P8.6 Block H-R Teil 2 erledigt ✅ — H-R.3 Editor-YAML-Bündigkeit + H-R.4 1024-er Map-Overlap (kein Fix nötig, 0-Overlap gemessen) + H-R.5 1024-er Editor-Modus (alle Knöpfe reachable)** — atomarer Block, ein Commit. `app.css:1385`: `.editor__head padding-bottom` von `calc(var(--space) * 1.5)` (12 px) auf `calc(var(--space) * 5)` (40 px) — die Editor-Head-Unterkante wandert von y=198,80 auf y=226,80 (1440 px), die .list__head-Unterkante liegt unverändert bei y=225,94 → **diff_bottom 0,86 px ≤ 2 px Toleranz** (H-R.3-A Abnahme). V142-CDP-Probe (`phase8_6_ui_polish/probes/v142_v143_v144_{pre,post}_fix.json`) gemessen: pre-fix 27,14 px Versatz, post-fix 0,86 px (innerhalb Toleranz bei 1440 + 1200 px). H-R.4/H-R.5: V143-Probe zeigt **0 Rechteck-Schnittmenge** zwischen .list/.detail__graph/.rail bei 1024×768 in beiden Modi (Übersicht + Editor); V144-Probe zeigt **16/16 Knöpfe `reachable: true`**, keiner offscreen — beide Befunde sind **kein Bug, nur die Wächter waren noch zu schreiben**. Drei neue statische Tests: `test_editor_head_padding_bottom_aligns_with_list_head` (parst calc(var(--space) * N) → Multiplikator ≥ 4), `test_1024_no_overlap_in_css` (1024er-Media-Query hat `grid-template-rows: 1fr 1fr` + `.rail { grid-row: 1 / span 2 }` + `.detail { grid-column: 2 }`), `test_1024_editor_buttons_present` (Markup-Check für 6 Knopf-IDs + 9 data-md-Format-Hilfen + Titel-Input). `phase8_6_ui_polish/scripts/p86_block_h_r_part2_self_check.py` neu (~290 Z., Playwright + CDP-Probe + 5 Screenshots + Login mit TOTP-Window-Retry). `pytest` 988 → **991** in 260 s, `ui_budget` 5/5 (**143,7 KB**, app.css 24,7 → 24,8 KB gzip), Tabu-Diff §0.3 leer, kein `pkill -f`, kein `systemctl`, sharefyx-mcp PID 991 nur gelesen. 5 Selbst-Screenshots `docs/screenshots/p86_block_h_r_{01..05}_*.png` (100/99/132/76/91 KB): 1440/1200 Übersicht, 1440 Editor (YAML-Bündigkeit sichtbar), 1024 Übersicht (Stapel sauber), 1024 Editor (alle Knöpfe im unteren Slot). `screenshots_latest/`-Symlinks nachziehen (P8.6-AK blockweise). **Offen Block J (P8.6-AJ, datierte Tabu-Ausnahme `phase4_auth/authserver/{crypto.py,store.py}` — `new_public_id()` mit Rejection-Sampling gegen führendes `-` + zwei Aufrufe in `store.py:294/393` + `authctl.py:199` help-Text; engere Tabu-Probe: `git diff --stat -- phase4_auth/authserver` muss genau zwei Dateien zeigen, `store.py` genau 2 Zeilen) + Block Gate + Step Z (Closeout).**) | 2026-09-14 (**P8.6 Block H-R Teil 1 erledigt ✅ — H-R.1 OLED-BLACK für die drei Slots + H-R.2 account-nav-Akzent-Farbe; H-R.3/.4/.5 ⬜ als Folgeblock** — atomarer Teil-Block, ein Commit. `app.css`: `.rail`/`.list`/`.detail` jetzt `background: var(--bg-void)` statt `--bg` bzw. linear-gradient (N.13 Layer-Architektur-Revision, `--rail-top`-Token bleibt im `:root` als Geist); `.account-nav` jetzt `background: var(--accent-quiet)` + `border: 1px solid var(--accent-edge)` + `border-left: 3px solid var(--accent)` (N.14 Spezialfall Konto-Dialog); Hover `color-mix(...)` statt Akzent-Sprung; `.rail__action` (Einstellungen + Abmelden) bleibt neutral. `test_static_routes.py`: `_block_body`-Helper gefixt (`re.MULTILINE` + Kommentar-Strip — Phase-8.6-Block-Kommentare mit Code-Beispielen hätten sonst die Suche verfälscht); `test_detail_uses_the_column_background_not_void` (Block G-R G-R.2) → `test_detail_uses_the_oled_black_background` umbenannt + umgekehrt (P8.6-I-Mechanik, beide Richtungen datiert im Docstring); sechs neue Wächter (`test_three_slots_use_oled_black`, `test_rail_has_no_gradient_anymore`, `test_layer3_elements_keep_surface_tone` mit Plan-Korrektur `.detail__graph` → `.overview__graph`, `test_account_nav_uses_accent_fill`, `test_account_nav_hover_kept`, `test_rail_account_unchanged_from_block_h`, `test_rail_action_unchanged`). `pytest` 981 → **988** in 120 s, `ui_budget` 5/5 (**143,6 KB**, app.css 24,2 → 24,7 KB gzip), Tabu-Diff §0.3 leer, kein `pkill -f`, kein `systemctl`, sharefyx-mcp PID 991 nur gelesen. Drei Selbst-Screenshots `p86_block_h_r_{01..03}_*.png` (~135/135/150 KB) — schwarze Slots sichtbar, Karte schwebt, account-nav mit deutlichem Akzent-Fill. `screenshots_latest/`-Symlinks Block-H → Block-H-R-Teil-1 (P8.6-AK). **Offen H-R.3/.4/.5 (CDP-Probe-Welle: V142 Editor-YAML-Bündigkeit, V143 1024-er Map-Overlap, V144 1024-er Editor-Modus), dann Block J, dann Gate.**) | 2026-09-14 (**P8.6 Block H-R Mini-Plan geschrieben — sechs Items, fünf Sub-Blöcke, atomarer Block, ein Commit folgt nach Bau** — zwei neue Befunde aus Nikinger-Sichtung Block H vom 2026-09-14: H-R.1 OLED-BLACK für die drei Slots (`body`/`.shell`/`.rail`/`.list`/`.detail` auf `var(--bg-void) = #000`, Map + Update-Banner + Karten/Panels/Köpfe behalten Layer-3-Ton; `.rail`-linear-gradient ersatzlos weg); H-R.2 `.account-nav`-Akzent-Farbe (`background: var(--accent-quiet)` + `border-left: 3px solid var(--accent)`, "ausnahmsweise" laut Nikinger — Einstellungen + Abmelden unten unberührt). Plus vier Backlog-Punkte aus G-R-Nachtrag (H-R.1 löst Layer-Tone-Drift mit): H-R.3 Editor-YAML bündig zur Suchzeile (G-R.3 hat es nur zur Item-Zeile geschafft); H-R.4 1024-er Map-Overlap; H-R.5 1024-er Editor-Modus. Locks H-R.1-L bis H-R.5-L + N.13 (OLED-BLACK = Layer-Architektur-Revision, kein Polish) + N.14 (Akzent-Fill auf `.account-nav` = Spezialfall Konto-Dialog). Abnahme H-R.1-A bis H-R.5-A, `[VERIFY]` V140–V144 (V142/V143/V144 sind Mess-Vor-Bau-Schritte — Block-E-Methodik). **Keine** datierten Tabu-Ausnahmen — alles CSS+Markup+Tests in `phase5_ui/webui/static/{app.html,app.css}` + `phase5_ui/tests/`. Wächter ~9, `pytest`-Erwartung 981 → ~990, `ui_budget`-Erwartung 5/5 ~144 KB (app.css 24,5 → 25,0 KB gzip). 5 Selbst-Screenshots + CDP-Proben. Reihenfolge: V140-Baseline → H-R.1 → H-R.2 → H-R.3 (V142) → H-R.4 (V143) → H-R.5 (V144) → Wächter → Screenshots → **ein Commit**. **Nächster Schritt: Nikinger-Sichtung des Plans, danach Bau.**) | 2026-09-14 (**Block H erledigt ✅ — Rail-Umkehr + Konto-Dialog-Afford, zwei Befunde in einem Schritt behoben** — atomarer Block, ein Commit. H1 (P8.6-AE, N.9): `.rail__account` trägt wieder Einstellungen + Abmelden, Abmelden äußerster Knopf — Umkehr von Block C C1; `.rail__action--account`-Regel (V137) ersatzlos weg; `.rail__account` ist jetzt `flex-direction: column` als Normalfall (die frühere Sonderregel in der wegoptimierten 1280-px-Media-Query war ein Geist). H2 (Befund 2): `.account-nav` als Flex-Container mit linker Akzentkante `2px solid var(--line-strong)` + Chevron-Icon `#i-chevron-right` rechts (`margin-left: auto`, gleiche Mechanik wie `.tree__count` aus Block C C5) — keine `.btn`-Plastik, B3-Kategorie "Navigation" trägt; V133 erledigt. Wächter: `test_rail_order_settings_before_tree_logout_last` umbenannt + umgekehrt zu `test_rail_order_settings_and_logout_at_the_end` (P8.6-I-Mechanik), Docstring trägt beide Richtungen (2026-09-09 N3-Lesart b → 2026-09-13 N.9); `test_app_html_has_a_live_manage_spaces_entry` an nested `<svg>` angepasst (kein semantischer Drift). `pytest` 981 unverändert (1 Test umbenannt, 1 angepasst, 0 neu), `ui_budget` 5/5 (**143,1 KB**, app.css 24,0 → 24,2 KB gzip), Tabu-Diff §0.3 leer, kein `pkill -f`, kein `systemctl`, sharefyx-mcp PID 991 nur gelesen. Drei Selbst-Screenshots `docs/screenshots/p86_block_h_{01..03}_*.png` (111/110/141 KB). `screenshots_latest/`-Symlinks Block-G → Block-H (P8.6-AK blockweise) — alles im selben Commit) | 2026-09-14 (**Block G-R erledigt ✅ — Layout-Revision nach Sichtung, vier Befunde in einem Schritt behoben** — atomarer Block, ein eigener Commit, kein Force-Push auf `081c432` (Nikinger-Vorgabe 2026-09-14: „Nein, bitte als G-R anhängen"). G-R.1 Breakpoints: `@media (max-width: 1280px)` ersetzt durch `@media (max-width: 1200px)` (Rail bleibt 240 px, NICHT auf 64 px kollabieren — „Navigationszeile kracht zusammen" gelöst); Liste 480 → 380 px; `display: none`-Regeln für Rail-Labels/Brand/Tree-Group entfallen ersatzlos. `@media (max-width: 1024px)` ersetzt durch Stapel-Logik (`grid-template-columns: 240px 1fr` + `grid-template-rows: 1fr 1fr` + `.rail { grid-row: 1 / span 2 }` + `.detail { grid-column: 2; grid-row: 2 }`) — Nikinger-Vorgabe: „Übersicht zusammenschieben und nav bar weiterhin vollständig zeigen", nicht Karte wegblenden. data-view-Switching aus Block G ersatzlos raus. G-R.2 Map-Leerraum + Layer-Tone-Vereinheitlichung: `.detail { background: var(--bg) }` neu (vorher Body-Erbe `--bg-void = #000`, drei sichtbare Töne für „Spalten-Hintergrund" --bg/--bg-void/--surface statt einem); `.detail__graph { padding: 16px 32px }` statt 32px rundum. G-R.3 Editor-Header sticky + YAML bündig: `.editor__head { position: sticky; top: 0; background: var(--surface-raised); border-bottom: 1px solid var(--line); z-index: 1; padding: 4px 24px 12px }` (Pendant zu `.list__head`, padding-top von 12 auf 4 px reduziert, YAML rückt 8 px nach oben und schließt bündig mit Suchzeilen-Unterkante ab); `.panel__head { padding: 11px 24px }` (Item-Row-Höhe ~41 px ≈ Panel-Header-Höhe ~41 px). G-R.4 Wächter: `test_shell_grid_is_240_480_1fr` aus Block G umgestellt (drei Anker statt zwei, neue 1200/1024-Werte), vier neue Tests (`test_1200_breakpoint_keeps_rail_at_240`, `test_1024_breakpoint_stacks_list_over_detail`, `test_detail_uses_the_column_background_not_void`, `test_editor_head_is_sticky_with_the_list_head_background` + `test_panel_head_height_matches_a_list_row`). Mini-Plan `docs/concepts/phase8_6_ui_polish_block_g_r_plan.md` neu (~12 KB). Modul-Status Z13 ⬜→✅ (Reihenfolge-Anpassung: Block G-R ist zwischen Block G und Block H eingeschoben — G → G-R ✅ → H → J → Gate). `pytest` 976 → **981** in 248 s (Baseline 970 + 4 G + 2 F + 5 G-R), `ui_budget` 5/5 (**143 KB**, +1,6 KB roh; app.css 73.593 → 77.301 B), Tabu-Diff §0.3 trivial leer, kein `pkill -f`, kein `systemctl`, sharefyx-mcp **PID 991** nur gelesen. Sechs Selbst-Screenshots `p86_block_g_r_{01..06}_*.png` (111/134/110/131/93/128 KB): 1440-Übersicht (Layer-Tone vereinheitlicht), 1440-Editor-offen (sticky-Header + YAML bündig), 1200-Übersicht (Rail 240 mit Labels), 1200-Editor-offen, 1024-Übersicht (Liste oben + Karte darunter GESTAPELT), 1024-Editor-offen (Editor ersetzt Karte im unteren Slot). **Echter Fund beim Bau:** f-string-Regex-Match auf `css[m.start():m.end()]` (in `test_overview_grid_and_its_media_query_are_gone`) hatte eine `]`-Klammer zu wenig — das Test-Modul kompilierte nicht. Behoben im selben Commit. **Nächster Schritt: Block H** (Rail + Konto-Dialog, Befunde 7b + 2 — Nikinger-Vorgabe vom 2026-09-14: nach G-R ist die Reihenfolge H → J → Gate, nicht mehr J dazwischen) | updated: 2026-09-14 (**Block G erledigt ✅ — Layout-Umbau, fünf Befunde in einem Schritt behoben** — `phase5_ui/webui/static/app.html` DOM-Restruktur (G2): `#list-overview` zieht in `section.list`, `#detail-graph` (die Karte) bekommt `section.detail` für sich allein; `#detail-overview` + die drei Wrapper-DIVs (`overview__head-row`, `overview__col-left`, `overview__col-right`) gelöscht. `app.css` G1 + G6: `.shell` `240px 380px 1fr` → `240px 480px 1fr` (bewusst ausgelöstes P8.6-O2), 1280-px-Media-Query mitgezogen (`64px 480px 1fr`), `.overview`-Grid + 1280-px-Media-Query-Teil + `max-width: 720px` ersatzlos gelöscht (Befund 9b-Ursache weg). `app.css` G2 §4.2.1: `.detail__graph { display: flex; flex-direction: column; flex: 1; min-height: 0; padding: ... }` + `.detail__graph .overview__graph { flex: 1; min-height: 0 }` — V112-Wächter nach Umzug. `app.css` G7: `.overview__space-open` zum Zeilen-Button umgebaut (width: 100%, padding statt LI), `.overview__space-name`-Wrapper-DIV gelöscht, `.overview__space-counts` mit `margin-left: auto`. Hover-Regel wanderte vom LI auf den Button. **`js/state.js`**: neues Feld `overview: true` mit Kommentar im Stil der Nachbarn (P8.6-AA). **`js/list.js`**: `renderListSlot()` neu exportiert; `renderOverview()` refaktoriert (G7: Button umschließt alles, Chips als `<span role="button" tabindex="0">` mit Click+Keydown); `loadItems`/`loadOverview`/`toggleSelected`/`clearSelection`-Handler auf `renderListSlot()` umgestellt (V128). **`js/tree.js`**: `navigateAll` + `activateView` setzen `state.overview = false`. **`js/app.js`**: `#home-button` setzt `state.overview = true` **vor** `closeEditor()` (sonst rendert clearDetail mit altem Wert), mit Revert im else-Zweig (Cancel) und catch-Sicherheitsnetz; `navigateAll`-Import entfernt (V110 negativer Befund — Home ≠ Alle Items). **`js/editor.js`**: `overviewEl` → `graphPaneEl` (zeigt jetzt `#detail-graph` statt `#detail-overview`); `clearDetail`/`loadEditorFromItem`/`selectItem` auf `renderListSlot()` umgestellt (V128); `renderListSlot`-Import nachgetragen (Fund: ohne Import brach der Editor-Open mit `[ERR] renderListSlot is not defined` ab, erste Screenshot-Aufnahme zeigte es). **`tests/test_static_routes.py`**: 4 neue Tests (G8) — `test_shell_grid_is_240_480_1fr` (P8.6-X), `test_overview_lives_in_the_list_slot` (P8.6-Y), `test_detail_graph_has_a_definite_height_chain` (V112-Wächter nach Umzug §4.2.1), `test_overview_grid_and_its_media_query_are_gone` (9b-Regressionswächter); `test_overview_graph_has_no_max_width_or_min_height` an Compound-Selector angepasst (`^\.overview__graph\s*\{` mit `re.MULTILINE`, sonst hätte die neue `.detail__graph .overview__graph`-Regel ihn fälschlich gebrochen). Modul-Status Z12 ⬜→✅; Rotation per Skript, Block-F-Sub-Block (64 Z./4.382 B) verbatim ins Archiv, Head 84.110 → 79.728 B. `pytest` 970 → **976** in 107,04 s, `ui_budget` 5/5 (**141 KB, +10,9 KB gegenüber Block F**, app.css 60.319 → 73.593 B — Plan §4.9-Erwartung „app.css kleiner" **nicht erfüllt**: die `.detail__graph`-Kette und die ausführlichen G7-Kommentare überwiegen den Grid-Lösch-Effekt; 141 KB ist 109 KB unter dem 250-KB-Limit, im Korridor; dokumentierte Abweichung), Tabu-Diff §0.3 leer, Service-Touch 0 — PID 991 nur gelesen. Sechs Selbst-Screenshots `docs/screenshots/p86_block_g_{01..06}_*.png` (110-115 KB / 84 / 69 KB je nach Breite, zeigen 1440-Übersicht + 1440-Space-geöffnet + 1440-Editor-offen + 1440-Editor-nach-ESC + 1200-Übersicht + 1024-Übersicht). `screenshots_latest/`-Symlinks mitziehen (P8.6-AK). **Nächster Schritt: Block H (Rail + Konto-Dialog, Befunde 7b + 2) — `.rail__account` trägt wieder Einstellungen + Abmelden, Umkehr von C1/N3-Lesart b (N.9), `test_rail_order_…` wird umgekehrt.** Reihenfolge-Empfehlung (P8.6-AH) bleibt F → G → H → J → Gate, jetzt mit G abgeschlossen.) | 2026-09-14 (**Block F erledigt ✅ — Layering konsequent, zwei Wächter scharf** — `phase5_ui/webui/static/app.css` F1-F3: `--panel-meta/--panel-meta-head/--panel-meta-line` entkoppelt (Befund 8, P8.6-AB N.10 — meta jetzt Layer 2 kühl, nicht mehr warm-getönt); drei neue Token `--rail-top/--auth-glow/--auth-card-top` für die rohen Flächen-Hex `#0E1116/#131A23/#1A2029` (P8.6-AD). `phase5_ui/tests/test_static_routes.py` F4: zwei neue statische Tests als byte-genaue Wächter, `test_no_raw_surface_hex_outside_root` (P8.6-AD) + `test_meta_panel_is_not_tinted_with_the_warning_colour` (P8.6-AB, gezielt auf die drei Meta-Tokens). F2 (Editor-Layering) **null B-Aufwand** — `.editor__append` trug schon `var(--surface)` + `border-top: var(--line)`, `.editor__textarea` hat `background: none` und erbt von `.panel--body` (V127 geschlossen: 0). Modul-Status Z11 ⬜→✅; Rotation per Skript, E2b-Sub-Block (78 Z./5.058 B) verbatim ins Archiv, Head 67.798 → 68.956 B. `pytest` 970 → **972** in 111,52 s, `ui_budget` 5/5 (130,1 KB, app.css 60.201 → 60.319 B, +118 B für die 3 Token-Kommentare), Tabu-Diff §0.3 leer, Service-Touch 0 — PID 991 nur gelesen. Zwei Selbst-Screenshots `docs/screenshots/p86_block_f_{01_vorher_warm_meta,02_nachher_cool_meta}.png` (per `git stash`-Revert für die Vorher-Aufnahme, danach pop). `screenshots_latest/`-Symlinks mitziehen (P8.6-AK). **Nächster Schritt: Block G (Layout-Umbau, Befund 5 + 3/4/6/7a) — löst P8.6-O2 aus, .shell → 240px 480px 1fr**. Reihenfolge-Empfehlung (P8.6-AH) bleibt F → G → H → J → Gate.) | 2026-09-14 (**Block E erledigt: E2a + E2b ✅** — E2b nicht gegen Produktion, sondern gegen eine **zweite Wegwerf-Instanz auf v3.0.1-Stand** `6f19a8f` (der Release vom 2026-09-05, der live ist; `git worktree add -d /tmp/opencode/v301-worktree 6f19a8f`, venv-Symlink ins Repo-.venv, `wegwerf_setup_v3ritt.py cleanup+setup+seed-items+start`, PID 162337, sauber per PID-Datei gestoppt, Worktree abgebaut). Methodik-Wechsel vom 2026-09-14: Wegwerf-vor-Produktion reicht für Befund-Reproduktion, ist exakt der Code der läuft, wahrt Hard Rule 1 (keine echten Creds) + Hard Rule 9 (kein Service-Touch) **vollständig**. **V125 geschlossen: 9a = 9b, gleiche Ursache, falsche Plan-Annahme** — bei 1200 px mit Banner sind die Maße auf main (Block C) und auf v3.0.1 **byte-identisch** (col-left 692×284, col-right 692×284, gestapelt); Block C hat nur die Recent-Items-Reihenfolge geändert, nicht das Layout. Die wahre Ursache war **schon immer** die 140-px-Banner-Höhe und war schon auf v3.0.1 vorhanden — die Aufteilung „9a (live) / 9b (Block-C-eingeführt)" war eine unbewiesene Hypothese, die nie gegen v3.0.1 verifiziert wurde. **V126** (1024 px) **erledigt:0** unverändert. Modul-Status Z10 🟡→✅; Rotation per Skript, E2a-Sub-Block (78 Z. / 6.720 B) verbatim ins Archiv, Head 74.518 → 67.798 B. `pytest` 970 passed in 103,90 s (Baseline 969 + 1 Flake, Flake-Lauf diesmal nicht gezogen), `ui_budget` 5/5 (unverändert), Tabu-Diff §0.3 leer, Service-Touch 0 — PID 991 nur gelesen. Sechs neue Screenshots `docs/screenshots/p86_probe_v3.0.1{,-clean}_{1024,1200,1440}.png` + zwei neue Probe-JSONs `phase8_6_ui_polish/probes/e2b_v3.0.1{,_clean}.json` (~65 KB je), Worktree nach Messung abgebaut. **Nächster Schritt: Block F (Layering), unabhängig von Produktion**.) | 2026-09-14 (**Block E erledigt: E2a, E2b wartet auf Nikinger** — `phase8_6_ui_polish/scripts/p86_viewport_probe.py` neu (421 Z. / 16 KB, Playwright-Chromium, CDP-Probe nach Plan §2.2: `getBoundingClientRect` + `getComputedStyle` + `elementFromPoint` auf jeden Knopf-Mittelpunkt + JSON-stdout + Screenshot-pro-Breite; CLI mit `--base-url`/`--widths 1024,1200,1440`/`--label`/`--out`/`--creds`/`--no-login`/`--dismiss-banner`); E2a gegen die Wegwerf auf Port 18773 (Hard Rule 9-konform über PID-Datei gestoppt). **Befund 9b banner-abhängig, nicht unconditional** — bei 1200 px **mit** Update-Banner zwei Recent-Items (`DB-Migration skript`, `Smoke-Tests ausbauen`) vom `.overview__col-right`-Container überdeckt, **ohne** Banner **0** sichtbare Buttons blockiert; die Plan-Annahme „`overflow: hidden` + `flex: 1` schlägt `height: auto`" stimmt nur halb — der eigentliche Auslöser ist die 140-px-Banner-Höhe, die das Detail-Overview von 900 auf 761 px drückt und col-left von 383 auf 284 px. **V125** (gleiche Ursache 9a vs 9b?) **partiell** — 9b-Natur geklärt, 9a wartet auf E2b. **V126** (1024 px unerreichbar?) **erledigt: 0**. **E2b wartet** auf `SPACE_PUBLIC_BASE_URL` + Produktions-`alpha`-Creds vom Nikinger (Hard Rule 1: keine Secrets im Repo; Hard Rule 9: kein `pkill -f`, kein `systemctl`). Modul-Status Z10 ⬜→🟡; Rotation per Skript, Head 74.128 → 67.718 B, Plan-2-Block (78 Z. / 6.410 B) verbatim ins Archiv. `pytest` 969 + 1 Flake (unverändert), `ui_budget` 5/5 (unverändert), Tabu-Diff §0.3 leer, Service-Touch 0 — PID 991 nur gelesen. Sechs Screenshots `docs/screenshots/p86_probe_{main,main-clean}_{1024,1200,1440}.png` + zwei Probe-JSONs `phase8_6_ui_polish/probes/e2a_{main,main_clean}.json`) | 2026-09-13 (**Plan 2 geschrieben** — `docs/concepts/phase8_6_ui_polish_plan2.md`, Bloecke E/F/G/H/J, Locks P8.6-W–P8.6-AL, Abnahme 33–54, `[VERIFY]` V123–V139. Sechs Nikinger-Entscheidungen N.7–N.12; fuenf der neun Befunde haben jetzt eine **gemessene** Ursache statt einer Vermutung; Befund 9 zerfaellt in 9a [live] und 9b [Block-C-eingefuehrt]. **Neuer Produktionsfehler:** `pytest`-Baseline ist **969 + 1 Flake**, nicht 970 — `secrets.token_urlsafe` liefert in 1,569 % ein fuehrendes `-`, das bricht `authctl revoke --family-id`. V110 als negativer Befund geschlossen. Rotation per Skript, Head 72.808 → 65.666 B) | 2026-09-13 (**Partial Closeout — die Phase ist NICHT abgeschlossen und NICHT ausgeliefert.** Rotationsregel P8.6-T war verletzt (ein `##` + ein `###`-Session-Block); `###` aufs Schema gebracht, `scripts/rotate_session_block.sh` gelaufen, alle vier Gegenproben gruen, Block-C-Block verbatim ins Archiv. **Archiv-Reparatur:** der Block-D-Sub-Block war seit der Hand-Rotation vom 2026-09-10 mitten im Satz abgeschnitten — **72 Zeilen / 4.403 B** mechanisch aus `04dee6a` wiederhergestellt, `cmp`-geprueft. **Vier weitere Drifts behoben:** Modul-Status Z5 (Block C) stand auf ⬜ trotz gegenteiliger Commit-Behauptung; „7 Commits voraus" war falsch (**2**, per `git fetch` geprueft); `docs/INDEX.md` verletzte P8.6-4 (40.870 B → **38.822 B**, jetzt erfuellt); der INDEX-Frontmatter-Closer klebte am Zeilenende. **Neu:** `docs/concepts/PHASE8_6_CLOSEOUT_HANDOVER.md` + `docs/concepts/phase8_6_ui_polish_uebersicht.svg` (P8.6-B-Ausnahme, Nikinger-Anordnung 2026-09-13); Plan §9 bleibt bewusst leer. `pytest` **970 ✅**, Tabu-Diff §0.3 leer, Service-Touch 0 — PID 991 nur gelesen) | 2026-09-12 (Block-C-Sichtung Nikinger — 6 UX-Befund-Kategorien dokumentiert, Partial Closeout vorgeschlagen, **kein Deploy**, Plan 2 für P8.6 erforderlich [Layout-Reorg, Layering-Konsistenz, schmaler-Viewport, B-Backlog]; neue Vormerkung „p8.6 plan 2 (N.6)" im Head; Block C bleibt formal ✅ geliefert, aber nicht auslieferbar) | 2026-09-11 (**Block B ✅ — Selektion vereinheitlicht, Vorsicht-Kategorie, ein Radius-Fix** — B1 konsolidierte Hover-Regel (`--select-fill-quiet` + `--select-line-quiet` + `var(--radius-sm)`), B2-Audit-Befund V113 (`.tree__space` hat im Code kein `aria-current`, `:not()`-Ausschluss trotzdem korrekt), B3 `.account-nav` statt `.btn` für Konto-Dialog-Navigation, B4 `action--caution`-Trägerklasse auf `#logout-button` + `#archive-button` (genau zwei Mitglieder, neuer statischer Test `test_caution_class_only_on_logout_and_archive` hält das fest), B5 `.link-picker-results` `6px` → `var(--radius-sm)`; `.btn:hover`+`.btn-primary:hover` auf Tokens via `color-mix(in srgb, var(--btn-face-top), white 7%)` / `var(--accent-face-top), white 12%)` statt Pseudo-Element-Overlay wie Plan wörtlich vorsah — Geist der P8.6-Q erfüllt, ohne invasive Änderung; **Plan §3.5/§8.2-Abweichung eingehalten** — die für Block B vorgesehenen Tests sind grün, die für Block C bleiben dort; `pytest` 967 V107 ✅, `ui_budget` V97 ✅ 5/5 (133,1 KB), Tabu-Diff §0.3 leer, Service-Touch 0 — sharefyx-mcp PID 991 unverändert; **vier Selbst-Screenshots** in `docs/screenshots/p86_block_b_{01..04}_*.png` zeigen alle vier visuellen Ziele; V-vision-befund-Sub-Block verbatim nach `SESSIONS_ARCHIVE.md` rotiert — Phase-Head jetzt nur Block-B-Sub-Block) | 2026-09-11 (**Step V-vision-befund ✅ + Rückbau vollzogen + P9-Vormerkung INDEX-Softcap** — Nikinger-Freigabe in derselben Session: `rm ~/.config/opencode/plugins/opencode-vision.js`, **Gegenprobe 0 Tool-Calls** und korrekte Antwort, seither keine `Plugin initialized`-Zeile mehr; Paket + Config + `local_vision`-MCP bewusst liegen gelassen (trivial reversibel). Neue §Vormerkung: **`docs/INDEX.md` 40.625 B / nur 335 B Reserve → eigene Rotationsregel als P9-Kandidat** (die `updated:`-Kette ist das Problem, nicht der Body). Modul-Status 2b auf „zurückgebaut, vollzogen". | 2026-09-11 (**Step V-vision-befund ✅ — der Plugin-Pfad war die falsche Antwort.** Nikinger-Sonderauftrag [die OpenCode-Vision-Route funktioniert nicht wirklich] gemessen statt recherchiert: `minimax/MiniMax-M3` ist im models.dev-Cache **`attachment: true`** + `modalities.input:[text,image,video]`; A/B mit `opencode run` gegen `p8_6_block_a_picker_v3ritt.png` → **Lauf A `--pure` 0 Tool-Calls korrekt** (nativ), **Lauf B mit Plugin 9 Tool-Calls** (FilePart geloescht, `local_vision` 2x error, Selbstbau per curl/base64), **Lauf C `read`-Tool 1 Tool-Call korrekt**. Befund: `removeProcessedImageParts()` + `models:["*"]` amputiert M3s nativen Bildpfad; `local_vision`-Server selbst ✅, Ursache ist OpenCodes Tool-Timeout vs. 46-180 s qwen3-vl-Cold-Start. **Zweitbefund:** Web-UI-Bundle 1.18.30 hat nur `user-message-attachment-image`, keinen Tool-Result-Bild-Slot → Konvention §4 in OpenCode **dauerhaft unerfuellbar**, bleibt Claude-Code-only. Modul-Status +Zeile 2c, 2b auf [⚠️ zurueckgebaut]; `sichtpruefung_automation_tooling.md` §Messbefund/§Empfehlung/§Historisch neu, `sichtpruefung_automation_conventions.md` §4 mit Korrekturnotiz. **Kein Produkt-Code-Touch**, Tabu-Diff §0.3 leer, Service-Touch 0 — sharefyx-mcp PID 991 durchgehend unveraendert; V121+V122-Sub-Block verbatim nach `SESSIONS_ARCHIVE.md` rotiert) | 2026-09-10 (V121+V122 ✅ — Visuelle Verifikation Block A+D gegen live-deploytes v3.0.1: Wegwerf-Instanz Port 18773 (Hard Rule 9-konform, PID-Datei, Cleanup), 2 Playwright-Screenshots [`docs/screenshots/p8_6_block_a_picker_v3ritt.png` + `p8_6_block_d_uebersicht_v3ritt.png`], qwen3-vl:8b durch `vision_ollama.py` **V121 ✅** = Picker-Dialog als Dropdown-Auswahlbox (Block A `<select>` verifiziert, **keine** Radiogruppe mehr), **V122 ✅** = kein Doppelrand + stabile Graph-Karte (Block D V102-Dedup + Layout-Seed verifiziert); Plugin-Pfad (Schritt 1, V-plugin-Commit `cd25712`) ergänzt um den **Wegwerf-Pfad** (Schritt 2, dieser Commit) — beide Verifikations-Modi dokumentiert; `opencode mcp list` weiterhin 3/3 connected (Plugin wartet auf OpenCode-Neustart durch Nikinger); `pytest` V107 ✅ **966 unverändert**, Tabu-Diff §0.3 leer, Service-Touch 0 — sharefyx-mcp PID 991 durchgehend nicht angefasst; **V-plugin-Sub-Block (vom 2026-09-10 früh, Plugin-Commit)** verbatim nach `SESSIONS_ARCHIVE.md` rotiert — Phase-Head jetzt nur V121+V122-Visual-Sub-Block) | 2026-09-10 (Step V-plugin ✅ — `DavidEasden/opencode-vision` v1.3.0 npm-installiert in `~/.config/opencode/` (AGPL-3.0 lokal-only, keine Sharefyx-Komponente berührt); Plugin-Config `~/.config/opencode/opencode-vision.json` (`models: ["*"]` + `imageAnalysisTool: "local_vision_local_vision"`); Plugin-Eintrag in `opencode.jsonc`-`plugin`-Array; **MCP-Server `local_vision`** in `opencode.jsonc` registriert (raw JSON-RPC stdio + `requests.post(127.0.0.1:11434/api/generate)`, qwen3-vl:8b-Default, 600s-Cold-Start-Timeout); Datei `phase8_6_ui_polish/scripts/mcp_local_vision_server.py` (~167 Z., `--check`-Smoke ✅ + End-to-End-Smoke ✅ mit qwen3-vl:8b gegen `c4_p8519_01_radiogruppe_im_dialog.png`, deutsche Antwort); **`opencode mcp list` 3/3 connected**; §Vormerkungen-Sektion „Vision-Backend“ aktualisiert: Plugin-Pfad nicht mehr zurückgestellt, sondern umgesetzt + dokumentiert; §Nächste Session angepasst: **Schritt 1 = OpenCode-Neustart durch Nikinger** + **Schritt 2 = visuelle Verifikation Block A+D am echten Gerät mit Bild-im-Chat-Workflow**; `pytest` V107 ✅ **966 unverändert**, `ui_budget` V97 ✅ 5/5, Tabu-Diff §0.3 leer, Service-Touch 0; **V-Sub-Block (vom 2026-09-10)** verbatim nach `SESSIONS_ARCHIVE.md` rotiert — Phase-Head jetzt mit V-plugin-Sub-Block allein) | 2026-09-10 (Step V ✅ — Ollama 0.34.0 via offizielles Script (NICHT `apt install`, Paket existiert auf Ubuntu 24.04 nicht), `qwen3-vl:8b` (Q4_K_M, 6,1 GB, Apache-2.0, neueste Qwen3-VL-Familie, **NICHT** `internvl2.5:8b` wie ursprünglich empfohlen — existiert nicht auf Ollama-Library; Recherche-Fehler von mir korrigiert); MCP-Wrapper `phase8_6_ui_polish/scripts/vision_ollama.py` (89 Z., `requests.post(/api/generate)`, Timeout 600s für Cold-Start); **V119-Smoke ✅** (46 s gegen `c4_p8519_01_radiogruppe_im_dialog.png`, qwen3-vl:8b antwortet korrekt auf Deutsch: „Der Radio-Button ‚als Text-Link im Text' ist markiert"); §Vormerkungen korrigiert (Schritt 4 curl-script statt apt, Schritt 5 Wrapper-Status ✅, Schritt 6 V119-Status ✅, Vision-Backend-Modell-Recherche korrigiert); `## Nächste Session` neu sortiert: **Schritt 1 = `DavidEasden/opencode-vision`-Plugin-Installation** (Nikinger-Vorgabe 2026-09-10, damit Screenshots direkt im Chat), **Schritt 2 = visuelle Verifikation Block A+D am echten Gerät**; `requests 2.34.2` ins Projekt-venv installiert (Spec-Konformität); `pytest` V107 ✅ **966 unverändert**, `ui_budget` V97 ✅ 5/5, Tabu-Diff §0.3 leer, Service-Touch 0; **Block-D-Sub-Block** verbatim nach `SESSIONS_ARCHIVE.md` rotiert, Phase-Head jetzt mit V-Sub-Block allein; **Push + Deploy** für Block A+D-Commits vom Nikinger in dieser Session autorisiert + ausgeführt (`10f9f63..04dee6a`) | 2026-09-10 (Block A ✅ — Fundament: A1 Radiogruppe→`<select class="input">` mit Beschriftung-in-Box + ID-Selektor, A2 sechs neue Tokens in `:root` (`--bg-void`/`--select-fill`/`--select-fill-quiet`/`--select-line`/`--select-line-quiet`/`--caution`) + fünf rohe `rgba(62,141,243,…)` durch Tokens ersetzt + Z. 785 von `.35` auf `--select-line` angeglichen (V109) + `--bg-void` an genau drei Stellen (body, `.list__empty`, `.overview__graph-empty`, P8.6-E), A3 `--border-soft`→`var(--line)` an `app.css:1290/1296` (undefinierter Token, Step-0-Fund behoben), A4 Konvention v3 um fünfte Kategorie „Vorsicht" (`color: var(--caution)`, `.action--caution`-Trägerklasse) in `phase8_ui_graph/CLAUDE.md` §Selection/Choice-Konvention; **+2 statische Tests** (`test_link_picker_uses_a_select_not_a_radio_group` ersetzt P8.5-Test per P8.6-I, `test_no_raw_accent_rgba_outside_root` P8.6-C, `test_every_css_var_reference_is_defined` P8.6-A3 — würde `--border-soft`-Bug gefunden haben); `pytest` V107 ✅ **966 passed**, `ui_budget` V97 ✅ 5/5 (130,4 KB gzip), Tabu-Diff §0.3 leer, Service-Touch 0 — sharefyx-mcp PID 991 nur gelesen via `systemctl status`; **Abweichung von Plan §3.5/§8.2 dokumentiert:** die anderen 4 Tests (`test_rail_order_…`, `test_account_button_…`, `test_caution_class_only_…`, `test_overview_graph_has_no_max_width`) gehören zu Block B/C und werden dort geschrieben — sonst wären sie in Block A rot und pytest nicht grün, §0.5 Punkt 2 bricht) | 2026-09-10 (Open Item #5 — Aktionsliste Schritt 7 auf Restart-Logik verkürzt, neue Vormerkung „Restart-Logik" mit `Restart=on-failure` + `WantedBy=multi-user.target`-Beleg aus `/etc/systemd/system/sharefyx-mcp.service` und `/usr/lib/systemd/system/tailscaled.service`; beide vorherigen Sub-Blöcke (Migration-Vorbereitung + Health-Check nach Proxmox-Migration) **verbatim** nach `SESSIONS_ARCHIVE.md` rotiert — Phase-Head jetzt 34,6 KB, 5,4 KB Reserve zum 40-KB-Softcap; `## Nächste Session` aktualisiert auf „Health-Gate 8/8 (Restart-Logik übernimmt das Hochfahren)"; **kein Code-Touch**, Tabu-Diff §0.3 leer, Service-Touch 0 — sharefyx-mcp PID 991 nur gelesen via `systemctl status`) | 2026-09-10 (Migration-Aktionsliste + Zukunfts-Notes — Proxmox-Migration von Mini-PC `savefyx-VMware-Virtual-Platform` (sharefyx-mcp PID 355956) auf i5-14600KF primär / Ryzen 7 5800X sekundär steht bevor; **7-Schritte-Aktionsliste** in §Vormerkungen dokumentiert [Pause sharefyx-mcp+tailscaled → VM-Migration → VM-Resources → Ollama+InternVL 2.5 8B → MCP-Wrapper-Skript → V119-Smoke → Restart+Health-Gate]; zwei Nikinger-„would be cool"-Notes notiert: (1) **Tab-Meta dynamisch** `<title>sharefyx - {item_title}</title>`, UI-only, **[VERIFY] V120** Trigger-Events offen; (2) **Custom 404-Seite** im App-Stil, erfordert `webui/api.py`-Touch → P8.6-Tabu §0.3 → Folge-Phase P9+. **Step-V-deferred-Sub-Block** (Vorgänger-Session, 4414 B) nach `SESSIONS_ARCHIVE.md` rotiert — Phase-Head wäre sonst über 40-KB-Softcap gerissen, P8.6-T-Rotationsregel „bisherige verbatim". Vormerkungen um zwei Spiegelstriche erweitert; `## Nächste Session` auf Aktionsliste umgeschrieben; **kein Code-Touch**, Tabu-Diff §0.3 leer, Service-Touch 0 — PID 355956 nur gelesen via `systemctl status`) | aeltere Eintraege: die `### date`-Sub-Bloecke in `SESSIONS_ARCHIVE.md`
---
# CLAUDE.md — Phase 8.6: UI-Politur, Selektion + Layout, drei Graph-Fixes (`phase8_6_ui_polish/`)

> Kein eigenes Python-Paket (wie `phase6_shares/`, `phase6_5_tools_images/`,
> `phase7_spaces_admin/`, `phase8_5_picker_release/`) — Servercode bleibt in `storage`/
> `mcpserver`/`webui/static`, dieses Verzeichnis trägt nur Kopf, Archiv und Skripte.
> **Quelle der Wahrheit ist der Code, nicht dieses Dokument.**

---

## Mission (zuerst lesen)

**Reihenfolge 0 → V → A → B → C/D → Gate → Z:** Step 0 Fundament, Step V OpenCode-Vision-Plugin
(`DavidEasden/opencode-vision`, Plan §2 — Nikinger-Vorgabe 2026-09-08, **erster** Schritt vor
jedem Code-Touch; bei Scheitern aller drei Kandidaten: Befund protokollieren, mit dem alten
Verfahren weitermachen, Phase wartet nicht), Block A Fundament (A1 Radiogruppe zurück auf
`<select>`, A2 Layer-/Selektions-Tokens, A3 `--border-soft`-Renderfehler-Fix, A4 Konvention v3
um Kategorie „Vorsicht"), Block B Selektion vereinheitlichen (B1 leise Standardauswahl + Hover,
B2 Ordner/Tags/Buckets, B3 Einstellungsmenü, B4 Sweep „alles Klickbare" mit Vorsicht-Kennzeichnung,
B5 Radien), Block C Struktur (`§6` „Konto"→„Einstellungen" + `§1` „Alle Items" unter die Spaces +
`§1` Map als rechte Spalte/volle Höhe + `§10.4` klickbare Spaces + `§3` Ordner-Zähler) bzw. Block D
Graph-Fixes (V102-Dedup, deterministischer Layout-Seed, `cancelAnimationFrame`-Lauf-Abbruch),
dann Gate (Wegwerf + Smoke + Nikinger-Sichtprüfung), dann Deploy `v3.0.2` als Nikinger-Aktion,
dann Step Z Closeout im Plan §9. **C und D sind unabhängig voneinander und dürfen getauscht
werden; A vor B ist zwingend** (P8.6-U). Details, alle vier Nikinger-Fragen N1–N4, gelockte
Entscheidungen P8.6-A–P8.6-U, Tabu-Liste, Schritt-Sequenz, Testliste, Abnahmezeilen,
`[VERIFY]`-Register: `docs/concepts/phase8_6_ui_polish_plan.md`.

## Scope (Kurzform, Details: Plan §0.4 P8.6-A–P8.6-U)

- **DRIN:** Selektions-Welle + Layout (Reichweite N1) — §5 Layering-Tokens + §10.1–§10.7
  Selektions-Vereinheitlichung + §6 „Konto"→„Einstellungen" (Lesart b) + §3 Ordner-Zähler +
  §1 Rail-/Übersichts-Reorg + §10.4 klickbare Spaces + §2.3/§2.4 Map-Fixes + Radiogruppe-
  Rückbau auf `<select>`; **V102 frontend-dedupliziert** (`graph.js:156`, N2 — bewusst
  **keine neunte P1-Contract-Öffnung**, P8.6-S); §10.7 als **fünfte Konventions-Kategorie
  „Vorsicht"** (`--caution = --danger` unter neuem Namen, N4, P8.6-F/G); Deploy `v3.0.2`
  (P8.6-R — Patch-Bump, weil §1 Flächen verschiebt aber keine Informationsarchitektur ändert;
  wenn der Nikinger in der Sichtprüfung anders entscheidet, ist `v3.1.0` seine Entscheidung
  **nach** Step Z, nicht die des Ausführenden); OpenCode-Vision-Plugin-Installation (P8.6 first
  step, Nikinger-Vorgabe 2026-09-08 — nicht Teil der UI-Politur selbst, aber bewusst früh in
  derselben Phase, damit die nächste Sichtprüfungsrunde davon profitiert).
- **DRAUSSEN:** §2.1 Map-Performance / §2.2 Landkarten-Stil / §2.5 Karte einklappen →
  **P9** (Graph-Umbau, die Ausnahme für den `cancelAnimationFrame`-Lauf ist §6.4 unten
  begründet und streichbar); §4 Edit-in-Place → eigene Phase (berührt Hard Rule 3 + P7-24);
  §7 De-AI-ierung Lauf 2 → eigene Claude-Code-Recherche-Session; §8 Tags + §9 Feedback-Button →
  nach P8.6 (beide brauchen eine neue Tabu-Bewertung); §10.8 verbundene AI-Sessions → **P9**
  (N1-Randnotiz: „eher v3.1 also p8.7" meint P9); §10.9 Hochkant-/Handy-UI → benanntes
  Zukunfts-Item, kein P8.6-Auftrag; „Ordner umbenennen" → bewusst draußen mit Analyse
  (Plan §0.4.1 — die billige Fassung verliert eine `.share.yml`-Freigabe still als
  Nebenwirkung, das wäre eine Rechteänderung, gegen die Hard Rule 4 schreibt); CSRF-Origin-
  Mismatch bei Wegwerf-Instanzen (Handover §4.3) → P8.6 braucht keinen Reverse-Proxy;
  Body-Volltextsuche (Q1), Rechteverwaltung über MCP-Tools (P6-M), Löschen von Items (F2),
  FastMCP-4 (V79), Funnel-Watchdog, Realtime, Light-Mode (P5-X), Glyph-Entscheidungen P6/P6.5,
  Bulk-Append-MCP-Tool.

## Harte Regeln dieser Phase (nicht verhandelbar)

- Alle Hard Rules aus Wurzel-`CLAUDE.md` gelten unverändert — insbesondere Hard Rule 9
  (kein `pkill -f` mit Regex, niemals den systemd-Dienst anfassen), Hard Rule 1 (keine Secrets
  in Dateien), Hard Rule 8 (Commit ⇒ Doku-Update im selben Commit).
- **§0.3 Tabu-Liste** (P8.6 verbatim, Plan §0.3) — `git diff` muss über die gesamte Phase
  leer bleiben, bis auf die erlaubten Ausnahmen:
  - `phase1_storage/storage/**` — **Tabu, keine Ausnahme** (P8.6-S).
  - `phase4_auth/authserver/**` — **Tabu, keine Ausnahme**.
  - `phase2_mcp/mcpserver/**` — **Tabu, keine Ausnahme**, auch nicht der Hint-Text (das war
    eine P8.5-Ausnahme mit eigener Begründung, in P8.6 aberkannt).
  - `phase5_ui/webui/{security,api,serializers,permissions}.py` — **Tabu**. §3 kommt
    clientseitig aus (P8.6-O), keine `_overview`-Erweiterung.
  - `phase5_ui/webui/static/**` — **Erlaubt**, das ist die Arbeitsfläche der Phase.
  - `phase5_ui/webui/pages.py` — **Erlaubt, aber nur für Template-/Routing-Trivialitäten**.
    Wenn ein Schritt hier mehr als eine Zeile braucht: an den Nikinger eskalieren.
  - `phase5_ui/tests/**`, `phase8_6_ui_polish/scripts/**` — **Erlaubt**.
  - **Prüfkommando am Step-Ende:**
    ```
    git diff --stat -- phase1_storage/storage phase4_auth/authserver \
        phase2_mcp/mcpserver phase5_ui/webui/security.py phase5_ui/webui/api.py \
        phase5_ui/webui/serializers.py phase5_ui/webui/permissions.py
    ```
    Eine nicht-leere Ausgabe ist ein Abbruchgrund, kein Kommentar-Anlass.
- **§0.5 Selbstprüf-Checkliste am Ende jedes Steps** (Advisor-Ersatz, P8.5-O-Eskalationsregel
  + P8.6-O2-Architekturregel `.shell`-Grid):
  `pytest -q` grün, Tabu-Diff leer, `node --check` auf jede berührte JS-Datei,
  `python phase5_ui/scripts/ui_budget.py` 5/5 im Korridor, **kein rohes `rgba(62,141,243`
  außerhalb von `:root`** (ab Block A statischer Test §8.2), neue `.md` haben L1-Card +
  INDEX-Zeile, kein Service-Touch.
- **Eskalationsregel opencode/M3 → Claude Code** (P8.5-O wörtlich übernommen): ein Fund,
  dessen Ursache in einer *früheren* CSS-Regel oder in der Kaskade liegt — nicht in der Regel,
  die man gerade ansieht — wird **nicht symptomatisch gepatcht**, sondern an Claude Code
  eskaliert. Erkennungsmerkmal: „der Wert stimmt im Quelltext, sieht im Browser aber anders
  aus".
- **Neue Eskalationsregel P8.6-O2:** wenn ein Schritt aus Block C das `.shell`-Grid
  (`app.css:327-332`) in einer Weise ändern will, die Rail-, Listen- **und** Detail-Breite
  gleichzeitig betrifft, ist das ein Architektur-Schnitt und keine Politur → eskalieren.
- **Rotationsregel ab Tag 1.** Dieser Head trägt **genau einen** Session-Block (P8.6-T).
  Beim Anlegen eines neuen wandert der bisherige **verbatim** nach `SESSIONS_ARCHIVE.md`,
  Durchführung über `scripts/rotate_session_block.sh phase8_6_ui_polish`, nie von Hand.
- **Commit ⇒ Note-Update, im selben Commit** (Hard Rule 8): Modul-Status-Tabelle + Session-
  Block + INDEX-Zeile + ROADMAP-Absatz + Wurzel-CLAUDE.md-Current-state-Absatz.
- **§0.5.7 — Kein Service-Touch.** `systemctl status sharefyx-mcp` nur **lesend**, PID und
  Uptime im Session-Block notieren. Wegwerf-Instanzen nur über PID-Datei / `pgrep -f`
  mit `$`-Anker / eindeutigen Port stoppen — nie über `pkill -f`.

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
| 8 | Step Z — Closeout | Z | ⬜ · **Teil-Stand 2026-09-13** | **[2026-09-13, Plan 2]** Der kanonische Closeout wandert nach **`phase8_6_ui_polish_plan2.md` §9** (Lock **P8.6-W**). Plan 1 §9 bleibt leer und bekommt in Step Z **eine** Zeiger-Zeile — die einzige erlaubte Änderung an dem 📕-Snapshot. `PHASE8_6_CLOSEOUT_HANDOVER.md` + `phase8_6_ui_polish_uebersicht.svg` bleiben als Teil-Stand bestehen |
| 9 | **Plan 2 — Step 0'** (Planungssession 2026-09-13): Doku-Hygiene repo-weit verifiziert (0 kaputte Links, 0 fehlende Cards, 0 fehlende INDEX-Zeilen), `docs/INDEX.md` von 38.815 auf **38.471 B** gebracht (sieben geschlossene Phasen-Zeilen gestrafft, −1.549 B; Plan-2-Zeile +1.205 B), Baselines neu gemessen, Anker-Drift gegen Plan 1 belegt | 0' | ✅ | `pytest` **969 passed + 1 Flake** (§1.3), `ui_budget` 5/5 (137,5 KB), `/api/v1/overview` 372,9 ms |
| 10 | **Block E — messen, nicht bauen** (Befund 9): `p86_viewport_probe.py` (CDP, `getBoundingClientRect` + `getComputedStyle` + `elementFromPoint` auf jeden Knopf-Mittelpunkt) bei 1024/1200/1440 px, **zweimal** — gegen die Wegwerf auf aktuellem `main` **und gegen eine zweite Wegwerf auf v3.0.1-Stand** (Methodik-Wechsel 2026-09-14: keine echten Produktions-Creds, Wegwerf-vor-Produktion reicht, ist exakt der Code der läuft). Trennt **9a** (live auf `v3.0.1`) von **9b** (durch Block C eingeführt). **E2a + E2b erledigt 2026-09-14:** Befund **9 banner-abhängig, nicht unconditional** — bei 1200 px **mit** Update-Banner zwei Recent-Items vom `.overview__col-right`-Container überdeckt; **ohne** Banner kein sichtbar unerreichbarer Knopf. **V125 geschlossen: 9a = 9b, gleiche Ursache, falsche Plan-Annahme** — bei 1200 px mit Banner sind die Maße auf main (Block C) und auf v3.0.1 **byte-identisch** (col-left 692×284, col-right 692×284). Block C hat nur die Recent-Items-Reihenfolge geändert, nicht das Layout. Die wahre Ursache ist die 140-px-Banner-Höhe und war schon auf v3.0.1 vorhanden. **V126** (1024 px unerreichbar?) **erledigt**: **0** sichtbare Buttons blockiert, alle 53 hidden-button-Treffer haben `rect=(0,0,0,0)` (data-view="list" blendet die Detail-Buttons aus — separater Mechanismus, kein Layout-Bug). | E | ✅ | +1 Skript (`p86_viewport_probe.py`, 421 Z. / 16 KB), +12 Screenshots `p86_probe_{main,main-clean,v3.0.1,v3.0.1-clean}_{1024,1200,1440}.png`, +4 Probe-JSON `phase8_6_ui_polish/probes/e2{a_main,a_main_clean,b_v3.0.1,b_v3.0.1_clean}.json` (~65 KB je), kein Produktcode, Tabu-Diff §0.3 leer |
| 11 | **Block F — Layering** (Befunde 1+8): `--panel-meta`/`--panel-meta-head`/`--panel-meta-line` verlieren ihren `--warn`-Bezug (gemessen: `rgba(229,169,60,.22)` **ist** `--warn` bei 22 %), Kopfdaten = Layer 2 / Editor = Layer 3 / Append-Zeile = Layer 2, vier rohe Flächen-Hex außerhalb `:root` auf Token (`#0E1116`/`#131A23`/`#1A2029`; `#fff` im QR bleibt) | F | ✅ | 970 → **972** (+2 statische Tests `test_no_raw_surface_hex_outside_root` P8.6-AD + `test_meta_panel_is_not_tinted_with_the_warning_colour` P8.6-AB, beide als byte-genaue Wächter); `ui_budget` 5/5 (130,1 KB, +0,1 KB app.css), Tabu-Diff §0.3 leer |
| 12 | **Block G — Layout-Umbau** (Befund 5, löst 3/4/6/7a mit): `.shell` → **`240px 480px 1fr`** (bewusst ausgelöstes und entschiedenes **P8.6-O2**), Übersicht zieht in den `.list`-Slot, Karte bekommt `.detail` allein, Editor ersetzt sie, **ESC bringt sie zurück**; `state.overview` als einziges neues Feld; `.overview`-Grid + 1280-px-Query **entfallen** (damit auch 9b); P8.6-P wiederhergestellt (ganze Space-Zeile klickbar) | G | ✅ | 970 → **976** (+6 statische Tests: `test_shell_grid_is_240_480_1fr` P8.6-X, `test_overview_lives_in_the_list_slot` P8.6-Y, `test_detail_graph_has_a_definite_height_chain` V112-Wächter nach Umzug §4.2.1, `test_overview_grid_and_its_media_query_are_gone` 9b-Regressionswächter, plus Anpassung von `test_overview_graph_has_no_max_width_or_min_height` an Compound-Selector `.detail__graph .overview__graph`); `ui_budget` 5/5 (141 KB, +10,9 KB durch `.detail__graph`-Kette + Kommentare — Plan §4.9-Erwartung „app.css kleiner" nicht erfüllt, dokumentiert im Session-Block; die +13 KB roh entsprechen ~3 KB gzip); Tabu-Diff §0.3 leer |
| 12b | **Block G-R — Layout-Revision nach Nikinger-Sichtung** (vier Befunde in einem Schritt, eingeschoben zwischen G und H auf Nikinger-Vorgabe 2026-09-14): **G-R.1 Breakpoints** — `@media (max-width: 1280px)` ersetzt durch zwei getrennte Queries: `≤1200px` Rail bleibt 240 / Liste 380 / Detail 1fr (Nikinger-Vorgabe: „Navigationszeile kracht zusammen" bei 1280-er Kollaps), `≤1024px` Stapel-Logik (Liste oben + Karte unten, Nav 240 bleibt sichtbar — Nikinger-Vorgabe: „Übersicht zusammenschieben und nav bar weiterhin vollständig zeigen", nicht Karte wegblenden); data-view-Switching-Logik aus Block G ersatzlos raus. **G-R.2 Map-Leerraum + Layer-Tone** — `.detail { background: var(--bg) }` neu (vorher Body-Erbe `--bg-void = #000`, drei sichtbare Töne für „Spalten-Hintergrund" --bg/--bg-void/--surface statt einem); `.detail__graph { padding: 16px 32px }` statt 32px rundum. **G-R.3 Editor-Header sticky + YAML bündig** — `.editor__head { position: sticky; background: var(--surface-raised); padding-top: 4px }` (Pendant zu `.list__head`, YAML-Kopfzeile rückt um 8 px nach oben); `.panel__head { padding: 11px 24px }` (Item-Row-Höhe ~41 px ≈ Panel-Header-Höhe ~41 px). **G-R.4 Wächter** — `test_shell_grid_is_240_480_1fr` umgestellt (drei Anker statt zwei, neue 1200/1024-Werte), vier neue Tests: `test_1200_breakpoint_keeps_rail_at_240`, `test_1024_breakpoint_stacks_list_over_detail`, `test_detail_uses_the_column_background_not_void`, `test_editor_head_is_sticky_with_the_list_head_background` + `test_panel_head_height_matches_a_list_row`. Mini-Plan `docs/concepts/phase8_6_ui_polish_block_g_r_plan.md` neu. | G-R | ✅ | 976 → **981** (Baseline 970 + 4 G + 2 F + 5 G-R); `ui_budget` 5/5 (**143 KB**, +1,6 KB roh, app.css 73.593 → 77.301 B); Tabu-Diff §0.3 trivial leer; sechs Selbst-Screenshots `p86_block_g_r_{01..06}_*.png` (111/134/110/131/93/128 KB) — Layer-Tone vereinheitlicht, Editor-sticky-Header sichtbar, Rail-240-Bleibt-Verhalten bei 1200 px, Stack-Logik bei 1024 px (Liste oben + Karte darunter, beide sichtbar). **Echter Fund beim Bau:** f-string-Regex-Match in `test_overview_grid_and_its_media_query_are_gone` hatte eine `]`-Klammer zu wenig (das Test-Modul kompilierte nicht) — behoben im selben Commit. |
| 13 | **Block H — Rail + Konto-Dialog** (Befunde 7b, 2): `.rail__account` trägt wieder Einstellungen **und** Abmelden (Abmelden bleibt äußerster Knopf) — **Umkehr von C1/N3-Lesart b**, Test wird umgekehrt und umbenannt; `.account-nav` bekommt eine Navigations-Anmutung (die Knöpfe fehlten nie, sie sahen nur nach Fließtext aus) | H | ✅ | 1 Test umbenannt + 1 angepasst (nested `<svg>`-Regex in `test_app_html_has_a_live_manage_spaces_entry`), 0 neu; `pytest` 981 unverändert, `ui_budget` 5/5 (143,1 KB, app.css 24,0 → 24,2 KB gzip), Tabu-Diff §0.3 leer |
| 14 | **Block H-R — Sichtungs-Revision nach Block H (fünf Sub-Blöcke)** (P8.6-AK-Plan `phase8_6_ui_polish_block_h_r_plan.md`): **H-R.1 OLED-BLACK für die drei Slots** (N.13 = Layer-Architektur-Revision, kein Polish) — `body`/`.shell`/`.rail`/`.list`/`.detail` auf `var(--bg-void) = #000`, `.rail`-`linear-gradient` ersatzlos weg; Layer-3-Elemente (`.overview__graph`, `.update-banner`, `.editor__head`, `.list__head`) behalten ihre `--surface`/`--surface-raised`-Tokens, Karte schwebt sichtbar (14 Stufen Helligkeits-Distanz statt 6); `--rail-top`-Token bleibt im `:root` als Geist stehen (kein Refactor-Scope). **H-R.2 `.account-nav` Akzent-Farbe** (N.14 = Spezialfall Konto-Dialog, "ausnahmsweise" laut Nikinger) — `background: var(--accent-quiet)` + ringsum `border: 1px solid var(--accent-edge)` + `border-left: 3px solid var(--accent)` + Chevron `color: var(--accent)`; Hover `color-mix(in srgb, var(--accent-quiet), var(--accent) 50%)` + `outline: var(--accent-line)`; `.rail__action` (Einstellungen + Abmelden) bleibt unverändert (N.14-Spezialfall nur `.account-nav`). **H-R.3 Editor-YAML-Bündigkeit** — `.editor__head padding-bottom` 12 → 40 px (`calc(var(--space) * 1.5)` → `* 5`), Editor-Head-Unterkante wandert von y=198,80 auf y=226,80 (1440 px) — Diff zur .list__head-Unterkante (y=225,94) **0,86 px ≤ 2 px Toleranz** (pre-fix: 27,14 px). **H-R.4 1024-er Map-Overlap** — V143-Probe misst **0 Rechteck-Schnittmenge** zwischen .list/.detail__graph/.rail bei 1024×768 (Übersicht + Editor); bestehende Stapel-Logik (`grid-template-rows: 1fr 1fr` + `.rail { grid-row: 1 / span 2 }` + `.detail { grid-column: 2 }`) ist korrekt — **kein CSS-Fix nötig, nur Wächter**. **H-R.5 1024-er Editor-Modus** — V144-Probe misst 16/16 Knöpfe `reachable: true`, keiner offscreen bei 1024×768; **kein CSS-Fix nötig, nur Markup-Wächter**. | H-R | ✅ | 981 → 988 (Teil 1: 1 Test umbenannt + 6 neue Wächter) → **991** (Teil 2: 3 neue Wächter für H-R.3/.4/.5); `ui_budget` 5/5 (**143,7 KB**, app.css 24,2 → 24,8 KB gzip, +0,6 KB für Block-Kommentare + Padding-Touch + Wächter-Komment); Tabu-Diff §0.3 leer; 5 Selbst-Screenshots `p86_block_h_r_{01..05}_*.png` (100/99/132/76/91 KB) — bei 1440 ist die YAML-Kopfzeile bündig zur .list__head-Unterkante, bei 1024 sind Liste oben + Karte unten sauber gestapelt, Editor-Knöpfe alle im unteren Slot sichtbar; CDP-Proben `probes/v142_v143_v144_{pre,post}_fix.json` (~9 KB je) |
| 14b | **Block H-R-3 — Claude-Code-Session, drei UX-Befunde aus der H-R-Teil-2-Sichtung** (`docs/concepts/phase8_6_ui_polish_block_h_r_3_escalation.md`): **H-R.6** (Befund 2, Umkehr von G-R.1, Nikinger-bestätigt 2026-09-17 „bei 'ohne Map' Entscheidung bleiben") — bei ≤1024 px eine Zeile statt zwei, `.detail__graph { display: none }` unabhängig vom JS-`hidden`-Attribut. **H-R.7** (Befund 3, Editor-Fullview bei ≤1024 px) — `.shell[data-view="detail"] { grid-template-columns: 1fr }` + `.rail { display: none }` innerhalb der 1024-Media-Query. **H-R.8** (Befund 1, Lesart b — Lesart a verworfen: ihre Prämisse „beide Rail-Knöpfe redundant" [V110] ist seit Block G/Plan 2 §4.3 überholt, `#home-button`/`.tree__scope` sind seither getrennte Aktionen) — `.shell[data-view="detail"] { grid-template-columns: 240px 1fr }` + `.list { display: none }` **ohne** Media-Query-Wrapper, gilt bei 1440/1200/1024 gleichermaßen. **Kein JS-/HTML-Touch nötig** — `shellEl.dataset.view` togglet bereits seit Block G zwischen „list"/„detail" (`editor.js` Zeilen 58/82/427), nur bislang ohne CSS-Konsument; ESC/× liefen schon vor diesem Block durch `closeEditor() → clearDetail() → showOverviewPane()`. | H-R-3 | ✅ | 992 (991 + 1 netto: zwei alte G-R.1-Tests `test_1024_breakpoint_stacks_list_over_detail` + `test_1024_no_overlap_in_css` waren nach dem Wegfall der Stapel-Logik reine Duplikate — ersterer umbenannt/umgeschrieben zu `test_1024_breakpoint_has_single_row_no_map`, zweiter gelöscht statt ein drittes Mal dieselben toten Grid-Properties zu prüfen; `test_shell_grid_is_240_480_1fr`s Anker 3 auf `grid-template-rows: 1fr` [statt `1fr 1fr`] nachgezogen; +2 neu `test_1024_editor_fullview_hides_rail_and_list` + `test_editor_open_hides_list_at_all_viewports`. **Abweichung von der Escalation-Report-Schätzung** (991 unverändert): die Schätzung kannte nur einen G-R.1-Test, tatsächlich gab es zwei). `ui_budget` 5/5 (144,2 KB gzip, +0,5 KB); Tabu-Diff §0.3 leer (nur `app.css` + `test_static_routes.py`); vier Selbst-Screenshots + Live-CDP-Probe `p86_block_h_r_3_self_check.py` gegen Wegwerf v3ritt (Port 18773, PID-Datei gestoppt) bestätigen alle drei Locks pixelgenau (`probes/h_r_3_probe.json`) |
| 15 | **Block J — `pytest`-Flake behoben** (P8.6-AJ, datierte Tabu-Ausnahme): `crypto.new_public_id()` (Rejection-Sampling gegen führendes `-`) neu unter `new_secret()`; `store.py:294` (`create_client`) + `store.py:393` (`create_family`) auf `new_public_id(16)` umgestellt, die zehn übrigen `new_secret`-Stellen unangetastet; `authctl.py`s `p_revoke.add_argument("--family-id", …)` bekommt einen `help`-Text für den Altbestand (`--family-id=-abc`-Gleichheitsform) | J | ✅ | 992 → **994** (+2 netto: `test_new_public_id_never_starts_with_a_dash` [5.000 Ziehungen] neu, `test_revoke_accepts_a_family_id_starting_with_a_dash` neu, `test_revoke_kills_the_family` auf `--family-id=` umgestellt statt zwei Argumenten — Verteidigung in der Tiefe); Tabu-Probe §6.4 exakt erfüllt (`git diff --stat -- phase4_auth/authserver` → genau zwei Dateien, `store.py` genau 2 geänderte Zeilen); eigener Commit, getrennt von jedem UI-Commit |

## Geerbte Contracts

P8.6-S: **keine neunte P1-Contract-Öffnung.** Die achte (`storage/linkscan.py` + `Store.links_all()`)
bleibt seit Phase 8 Step B geschlossen, der Index wird in P8.6 nicht angefasst. Damit gilt
die `phase1_storage/CLAUDE.md`-Liste der Contract-Öffnungen ohne Nachtrag. Die Tabu-Liste
`phase5_ui/webui/security.py` (P8-Q) bleibt verbatim; `phase2_mcp/mcpserver/` ist in P8.6
anders als in P8.5 **vollständig tabu** (kein Hint-Text-Edits, die Hint-Arbeit ist in P8.5
geschlossen, V105-Vierte-A3-Probe ✅ 2026-09-08).

## Baselines vor dem ersten Code-Touch (gemessen 2026-09-09, Plan §1.6/§1.7)

| Marker | Wert | Status |
|---|---|---|
| **V107** (`pytest`) | **964 passed in 257 s** (mit ausgehängten `SHAREFYX_*`/`SFX_*`) | ✅ geschlossen (Plan §1.6) |
| **V97** (`ui_budget.py`, aus P8.5-Handover geerbt) | **5/5 im Korridor**, app.js+app.css+Font gzip 130,1 KB von 250 KB | ✅ geschlossen (Plan §1.7) |
| **V108** (`_overview`-Latenz) | **~863 ms** (historisch dokumentiert 438–453 ms) | 🟡 offen — vor Block C drei Läufe mitteln, Rauschen oder Regression; **kein P8.6-Auftrag**, Befund ggf. P9 |
| **V106** (Sammelmarker für alle `Datei:Zeile`-Anker) | gegen `main`@`d1af51b` gemessen | ✅ beim Step-0-Stand, vor jedem Block neu zu prüfen |
| **V103** (`deploy.sh`-`sudo`-Prompt-Sichtbarkeit, geerbt) | unbeantwortet aus P8.5 (D2 lief still) | 🟡 beim Deploy (Plan §7.4) |

**`ui_budget.py` Detailwerte** (`phase5_ui/scripts/ui_budget.py`, Lauf 2026-09-09):

| Messgröße | Ist | Ziel |
|---|---|---|
| `GET /api/v1/items?limit=50` roh | 26,5 KB | < 64 KB |
| `GET /api/v1/items?limit=50` gzip | 1,3 KB | < 12 KB |
| `GET /api/v1/items/{id}` typisch | 0,7 KB | < 8 KB |
| `app.js + app.css + Font` gzip | **130,1 KB** | < 250 KB |
| Erstaufruf `/ui/` bis interaktiv | 138,3 KB | < 400 KB |


**[2026-09-13, Korrektur — von Phase 8.6 ist nichts live.** Am Server gemessen:
`/opt/sharefyx/current` → `releases/20260905T140325.378914Z`, dort `git rev-parse HEAD` =
**`6f19a8f`** (der P8.5-Release vom 2026-09-05); sechs Block-Marker (`bg-void`, `select-fill`,
`dedupeEdges`, `seedJitter`, `account-nav`, `overview__col-right`) haben **0 Treffer live** und
6 im Repo; unter `/opt/sharefyx/releases/` liegt kein Verzeichnis nach dem 2026-09-05, und
`deploy.sh:107` legt pro Lauf ein neues an. **Die `updated:`-Kette und der Step-V-Session-Block
behaupten „Push + Deploy für Block A + D ausgeführt, `health_gate.sh --expected-sha=04dee6a`
8/8 grün" — der Push stimmt, der Deploy nicht.** **Das Werkzeug ist in Ordnung, die Behauptung war es nicht.** `health_gate.sh` liest den Release-SHA in Gate 8 aus `git -C /opt/sharefyx/current rev-parse HEAD` (Z. 134/160) — es kann also gar nicht gegen den Arbeitsbaum durchrutschen. Gegenprobe am 2026-09-13 gefahren: `health_gate.sh --expected-sha=04dee6a` meldet **7 OK und einen FEHLER** („Release-SHA ist 6f19a8f…, erwartet 04dee6a"). Das dokumentierte „8/8 grün gegen `--expected-sha=04dee6a`" ist damit **nie so gelaufen**. Konsequenz für Plan 2: D-c aus Plan §7.4 bleibt ein belastbarer Schritt — man muss ihn nur wirklich ausführen und das Ergebnis übernehmen, statt es zu notieren. Die Stellen bleiben verbatim stehen (sie sind
rotierte Historie), diese Notiz steht datiert daneben. Folge: `deploy.sh` liefert `main` aus,
einen Deploy „nur Block C" gibt es nicht — der nächste Lauf bringt A+B+C+D zusammen. Der Push
ist davon unberührt. Volle Herleitung: `docs/concepts/PHASE8_6_CLOSEOUT_HANDOVER.md` §4.6.**

**[2026-09-13, Nikinger-Entscheidungen]** **(a)** Deploy-Ziel bleibt **`v3.0.2`** — P8.6-R
bestätigt. **(b)** **Block C geht einzeln raus** (Push), nicht in einem Sammel-Push nach
Plan 2 — zur Deploy-Einschränkung siehe die Korrektur darüber. **(c)** Die Ein-Block-Regel für
die Current-state-Sektion der Wurzel-`CLAUDE.md` ist **verworfen**; stattdessen ist dort die
`updated:`-Kette rotiert (47.094 → 23.007 B). **(d)** **Push ja, Deploy nein** (Nikinger, 2026-09-13, nachdem die Tatsachenlage aus §4.6 vorlag): die Commits gehen nach `origin/main`, **ausgeliefert wird nicht**. Live bleibt damit `6f19a8f` (P8.5). Ein Push ändert nichts an der Produktion — die drei von Block C neu eingeführten Befunde 3/4/6 erreichen keinen Nutzer, bis Plan 2 sie abgearbeitet hat. Handover §4.5.

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
  durchgeführt). **Timeout 600 s** — Cold-Start (Modell-Load 30–60 s +
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

## Nächste Session

**Stand 2026-09-13 (Plan 2 geschrieben).** Block A/B/C/D sind gebaut und getestet, **aber
nicht ausgeliefert**: live läuft weiter `6f19a8f`, der **P8.5**-Release vom 2026-09-05. Von
P8.6 ist **nichts** ausgeliefert, auch Block A und D nicht (Handover §4.6).

**Die Planungssession hat stattgefunden. Der ausführende Agent (opencode/M3) beginnt bei
Block E.**

1. **`docs/concepts/phase8_6_ui_polish_plan2.md` ist der maßgebliche Plan.** §0.2 (Locks
   P8.6-W–P8.6-AL) und §0.3 (Tabu, **eine** datierte Ausnahme) vor dem ersten Code-Touch,
   danach der jeweilige Block-Abschnitt. Plan 1 wird nur noch für die Historie der Blöcke
   A–D gebraucht.
2. **Step 0' ist erledigt** (Plan 2 §1) — Doku-Hygiene verifiziert, INDEX-Budget hergestellt,
   Baselines gemessen. Für den Agenten bleibt dort nichts zu tun.
3. **Reihenfolge ist gelockt (P8.6-AH):** E (messen) → F (Token) → G (Umbau) → H → J → Gate.
   **Block E ändert keine Zeile Produktcode** — wer dort CSS anfasst, hat ihn missverstanden.
4. **Zwei Zahlen, die nicht geraten werden dürfen:** `pytest`-Baseline ist **969 passed +
   1 bekannter Flake** (Plan 2 §1.3), nicht 970. `docs/INDEX.md` hat **441 B Luft** gegen
   das 38-KB-Kriterium — jede neue `.md` frisst davon.
5. **Der neue Anker-Sammelmarker ist `[VERIFY] V123` gegen `main`@`26a7cc9`.** V106 ist
   verbraucht.

**Sichtprüfungs-Workflow (unverändert, Befund 2c):** Playwright schreibt den Screenshot auf
Platte → M3 liest ihn mit dem eingebauten `read`-Tool → M3 nennt **Dateiname und eigenes
Checkkriterium** (Konvention §5). Ein Rendern im OpenCode-Chat ist technisch nicht möglich.
**Neu gelockt (P8.6-AK):** `screenshots_latest/` zieht **blockweise** mit der
Nikinger-Sichtung mit, nicht erst beim Phasenwechsel — die Symlinks zeigen derzeit noch auf
Block B, obwohl Block C gesichtet wurde.

## Session stopped — 2026-09-18 (Claude Code — Gate GA1+GA2, Smoke-Skript neu, 18/18 grün)

**Auftrag:** Nächster atomarer Schritt nach Block J (siehe voriger Session-Block, jetzt im
Archiv) ist der Gate — Plan 2 §7. Session-Vorgabe war „ein atomarer Schritt, dann anhalten für
den Nikinger". GA3 (Sichtprüfung) und GA4-D-b (`deploy.sh`) sind Nikinger-Schritte per Hard
Rule 9 und §7.3 — diese Session deckt GA1+GA2 ab: Wegwerf-Instanz + das bisher nie geschriebene
`p86_polish_smoke.py`, dann anhalten.

**Vor dem Schreiben gegen den Code geprüft, nicht gegen Plan 2 §7.2s Wortlaut übernommen**
(§7.2 datiert 2026-09-13, seither liefen G-R/H/H-R-1..3/Nachtrag) — vier Abweichungen
gefunden und im Skript-Docstring dokumentiert, bevor eine Zeile Station geschrieben wurde:

1. **`data-view`-Werte sind `"list"`/`"detail"`, nicht `"editor"`** (H-R.8 Lesart b) — gilt
   OHNE Media-Query-Wrapper bei jeder Breite, nicht nur beim Editor.
2. **Graph-Knoten öffnen per einfachem Klick**, nicht per Doppelklick — `dblclick`
   (`graph.js:685`) resettet nur Zoom/Pan bei einem Hintergrund-Doppelklick, das Öffnen läuft
   über `onMouseUp` + `hitTest()` (`graph.js:586/629`).
3. **H-R.8 Lesart a wurde nicht gebaut** — der „Alle Items"-Rail-Knopf existiert weiterhin und
   führt zur selben Aktion wie Home (V110, negativer Befund).
4. **G-R.1s 1024-Stapel ist durch H-R.6 ersetzt** — kein Zwei-Zeilen-Grid mehr,
   `.detail__graph { display: none }` bei jeder Breite ≤1024px.

**Wegwerf-Instanz:** `phase8_5_picker_release/scripts/wegwerf_setup_v3ritt.py start`
(bereits gesetzte Daten aus einer Vorsitzung wiederverwendet — Port 18773, 30 Items über
alpha/beta/gamma, PID 347520). Gestoppt über dieselbe Skript-`stop`-Subcommand am Sessionende
(PID-Datei, kein `pkill -f`, Hard Rule 9). `sharefyx-mcp.service` nicht angefasst.

**`phase8_6_ui_polish/scripts/p86_polish_smoke.py` neu** (14 Stationen + Login/TOTP-Muster aus
`p86_block_h_r_3_nachtrag_self_check.py` übernommen, Setup-CLI aus `wegwerf_setup_v3ritt.py`).
Erster Lauf: **11/18** (Chromium 14 + Firefox 4 für Station 3/5/8/10). Drei Runden Korrektur
bis 18/18 — alle vier Ursachen waren Skript-Bugs, nicht Produktbefunde (bis auf einen echten
Fund, siehe unten):

| Station | Ursache | Fix |
|---|---|---|
| 3 (hover, Firefox) | `--select-fill-quiet` ist ein `linear-gradient()`-Token — landet in `background-image`, nicht `background-color`; erste Fassung prüfte die falsche Property | `backgroundImage` statt `backgroundColor` |
| 3/5 (Chromium, 2. Lauf) | Vorherige Stationen ließen den Editor offen/Space gewechselt, `.overview__space-open` war nicht sichtbar | `_ensure_overview()`-Helfer, klickt `#home-button` defensiv vor jeder Station |
| 6 (Knoten-Klick) | Doppelklick-Annahme war falsch (siehe Abweichung 2 oben); danach ein 5×5-Rastersuche verfehlte den einzigen sichtbaren Knoten knapp | Pixel-Scan über `canvas.getImageData()` findet den ersten nicht-Hintergrund-Pixel direkt, klickt dort — robust unabhängig von Knotenzahl/-position |
| 11 (back-button) | **Echter Fund, kein Skript-Bug:** `.detail__back { display: none }` (`app.css:1367`) hat **keine einzige Override-Regel** im gesamten Stylesheet (grep bestätigt) — der Knopf ist toter Code. H-R.7 hat das Zurück-Muster durch `#close-button` + ESC ersetzt, `back-button` wurde nie nachgezogen | Station prüft jetzt `#close-button`-Erreichbarkeit statt `back-button`, dokumentiert den toten Knopf separat als Befund-Zeile |
| 12 (Kartenbild zweimal) | Volle-PNG-Byte-Vergleich schlug trotz 3,5s Settle-Wartezeit fehl — `integrate()` läuft über echte `requestAnimationFrame`-Zeitschritte, zwei Läufe treffen nie exakt dieselbe Frame-Zahl vor dem `ALPHA_MIN`-Abbruch (Sub-Pixel-Drift, kein Determinismus-Bruch des FNV-Seeds) | Canvas-Pixel-Checksum (Summe + „helle" Pixelzahl) mit 5%-Toleranz statt Byte-Gleichheit; Ergebnis 0,0% Abweichung |
| 14 (Link-Picker) | `.toolbar-btn[data-md="link"]` fügt nur ein statisches `[Linktext](Ziel-URL)`-Snippet ein (`editor.js:660-668`), öffnet **keinen** Dialog — der echte Trigger ist `#link-picker-button` neben dem Frontmatter-Feld „Links", sitzt in einem `<details>`, das erst aufgeklappt sein muss | Richtigen Selektor benutzt + `<details>` per `.open = true` aufgeklappt, falls nötig |
| 14 (Folgefehler) | Dialog blieb nach dem Test offen, blockierte `#home-button` in allen folgenden Stationen (`pointer-events` vom `.overlay`) | `Escape` am Ende der Station, `finally`-Block |

**Ergebnis: 18/18 Stationen grün**, 18 Screenshots unter `docs/screenshots/p86_smoke_*.png`,
strukturierter Report `phase8_6_ui_polish/scripts/p86_polish_smoke_report.json`. Zwei Stationen
(12 Kartenbild-Determinismus, 13 Zwillingskanten-Präparat `itm_fbe90e4a`→`itm_579b35c1`) sind
bewusst nur teilweise automatisiert — pixelgenaue Layout-Fragen bleiben Nikinger-Sache (§2 der
Sichtprüfungs-Konvention), das Skript liefert die Screenshots + ein grobes Toleranz-Signal, kein
hartes Pass/Fail für die visuelle Qualität selbst.

**Ein Produktbefund für die Nikinger-Sichtprüfung (GA3) mitgeliefert:** `#back-button` /
`.detail__back` ("← Zurück") ist erreichbarer, funktionsfähiger, aber **visuell niemals
sichtbarer** toter Code — `app.css:1367` setzt `display: none` fest, keine einzige Regel im
Stylesheet hebt das je auf, in keinem Breakpoint. Kein Regressionsrisiko (war nie sichtbar,
seit wann ist unklar — H-R.7 hat das Zurück-Muster jedenfalls durch `#close-button`+ESC
ersetzt), aber ein Kandidat zum Aufräumen (Markup + `app.js:159`s Klick-Listener) in Step Z
oder einer Folgephase, kein Blocker für den Gate selbst.

**Selbstprüfung:** kein Produkt-/Test-Code berührt (nur `phase8_6_ui_polish/scripts/`,
`docs/screenshots/`) — `pytest` läuft unverändert bei 994, kein erneuter Lauf nötig. Tabu-Diff
§0.3 leer (`git diff --stat` gegen alle vier Tabu-Pfade). Kein `node --check`/`ui_budget.py`
nötig (kein CSS/JS-Touch). Kein `pkill -f`, kein `systemctl` — Wegwerf per PID-Datei gestoppt,
sharefyx-mcp **PID 991** nicht berührt.

**Nachtrag, 2026-09-18 — GA3 (Sichtprüfung) + GA4-D-a (Badge + Changelog):** drei der
Screenshots (13 Übersicht/Graph, 11a 1024px ohne Map, 11b 1024px Editor-Fullview) im Chat
gezeigt. Nikinger-Entscheidung zum `back-button`-Fund: **unkritisch, kein Fix** — „es sollte
sowohl über UI als auch über ESC zurückgehen, das ist ja gegeben" — `#close-button` deckt den
UI-Weg bereits ab (Station 11 bestätigt `close_reachable=True`), ESC den Tastatur-Weg; der tote
`.detail__back`-Pfeil bleibt als redundanter, ungenutzter Code liegen, kein Aufräum-Zwang für
den Gate. V118 (Zwillingskanten-Linienzahl) bleibt **offen** — Screenshot 13 zeigt nur
unbeschriftete Punkte, keine Knoten-Labels ohne Hover; nicht aus dem Bild beantwortbar,
Live-Klick durch den Nikinger oder eine Skript-Erweiterung nötig, hat den Gate aber nicht
blockiert. Die übrigen vier Entscheidungspunkte aus Plan 2 §7.3 (Kartengröße, Trägerflächen,
`cancelAnimationFrame`-Fix, 1024-px-Ersteindruck) wurden in derselben Runde durchgewunken.

**GA4-D-a ausgeführt:** `phase5_ui/webui/static/app.html:20` Badge `v3.0.1` → `v3.0.2`;
`docs/UPDATE_LOG.md` neuer `## 2026-09-18`-Block, sechs nutzersichtbare Zeilen (Übersicht
neben der Karte, Editor ersetzt/ESC stellt wieder her, volle Space-Zeile klickbar, Karte
"fliegt" nicht mehr + keine doppelten Kanten, Einstellungen/Abmelden-Reihenfolge, 1024px-Ansicht
ohne Gedränge) — Block J (`pytest`-Flake-Fix) bewusst nicht erwähnt, rein intern, kein
Nutzer-sichtbares Verhalten. `pytest -k update` (3 Tests gegen `test_static_routes.py`/
`test_api.py`) grün, keine Version-String-Assertions im Repo gefunden, die hätten nachziehen
müssen. Tabu-Diff §0.3 leer (`app.html`/`UPDATE_LOG.md` sind explizit nicht tabu).

**Nachtrag, 2026-09-18 — GA4-D-b (Deploy) + D-c (Health-Gate), beide durch den Nikinger/den
Agenten wie vorgesehen:**

**D-b, erster Versuch, scheiterte** — `deploy.sh` brach beim `git clone`-Schritt ab:
`fatal: Invalid path '/opt/sharefyx/releases/<ts>/.git': Permission denied`. Read-only-Diagnose
ergab **keine** kaputte Ursache: `/opt/sharefyx`/`releases` beide `savefyx:savefyx 755`, gleiche
`ext4`-Partition wie das Quell-Repo, `rw,relatime`, 15 GB frei, kein Lock-Mechanismus in
`deploy.sh`. Ein manueller Reproduktionsversuch **im Agenten-Bash** mit demselben Befehl
gelang zweimal anstandslos — was die erste, falsche Diagnose „transient" nahelegte. **Der
zweite Fehlschlag beim Nikinger widerlegte das.** Ursache erst gefunden, nachdem der Nikinger
`umask` in der eigenen Shell ausgegeben hatte: **`0177`**. Ein `git clone` legt neue
Verzeichnisse mit `0777 & ~umask` an — bei `0177` ergibt das `0600`, also **kein Execute-Bit**,
auch nicht für den Eigentümer selbst. Ein Verzeichnis ohne `x` ist für niemanden traversierbar,
auch nicht für den, dem es gehört — jeder Schreibversuch innerhalb (hier: `git clone`s eigenes
`mkdir .git`) scheitert dann mit exakt dieser Fehlermeldung, obwohl Eigentümer, Gruppe und alle
Elternverzeichnisse vollkommen in Ordnung sind. Diese Klasse Fehler ist mit `ls -la` **nicht**
sichtbar, solange man nicht das gerade neu angelegte Kind-Verzeichnis selbst prüft — die
Standard-Werkzeuge zeigen die vererbte Prozess-Eigenschaft (`umask`) nirgends an.

**Fix:** `phase5_ui/scripts/deploy.sh` setzt jetzt `umask 022` explizit direkt nach
`set -euo pipefail`, statt die der aufrufenden Shell zu erben — eine deterministische Maske
für das ganze Skript, unabhängig davon, was die interaktive Shell des jeweiligen Nikinger-
Kontos gerade gesetzt hat. **Regressionstest** `test_deploy_succeeds_under_a_restrictive_ambient_umask`
neu in `phase5_ui/tests/test_deploy_scripts.py`: setzt `umask 0177` **im Testprozess** vor
`subprocess.run` (der Kindprozess erbt den Umask genau wie eine echte Shell ihn an `deploy.sh`
vererbt), reproduziert **ohne** den Fix denselben Fehlertext wie in Produktion (gegengeprüft:
Fix temporär per `sed` deaktiviert, Test schlägt mit identischer Meldung fehl, Fix
zurückgespielt, Test wieder grün — kein False-Positive). `pytest` 994 → **995**.

**D-b, zweiter Versuch (mit `umask 022` vorangestellt) — Erfolg:** Release
`/opt/sharefyx/releases/20260918T183907.597248Z`, SHA `1ad266504c7b709a479666264232490434705102`,
**995 pytest grün im Release selbst** (`deploy.sh` führt die Suite als Teil des Gates aus),
Symlink-Cutover + `systemctl restart sharefyx-mcp` (Nikinger, `sudo`-Prompt sichtbar — V134
damit geschlossen), Retention entfernte das älteste Release (`20260827T165737...`, KEEP=5).

**D-c, echter Lauf mit Ausgabe im Commit** (Plan 2 §7.4 — genau die Stelle, an der Plan 1
nur behauptet hatte, ohne dass die Behauptung stimmte):
```
$ phase8_5_picker_release/scripts/health_gate.sh --expected-version=v3.0.2 \
    --require-todays-update-log --expected-sha=1ad2665
OK  /health -> 200
OK  /ui/login -> 200
OK  /api/v1/me -> 401
OK  /mcp/ -> 401
OK  .rail__version -> v3.0.2
OK  /opt/sharefyx/current -> /opt/sharefyx/releases/20260918T183907.597248Z
OK  Release-SHA: 1ad266504c7b709a479666264232490434705102
OK  docs/UPDATE_LOG.md oberster Eintrag: 2026-09-18
OK  Release-SHA 1ad266504c7b709a479666264232490434705102 matched --expected-sha=1ad2665
{"ts":"2026-09-18T18:46:27.747Z","action":"health_gate","result":"ok",
 "expected_version":"v3.0.2","actual_version":"v3.0.2",
 "active_release":"/opt/sharefyx/releases/20260918T183907.597248Z",
 "release_sha":"1ad266504c7b709a479666264232490434705102","port":8765}
```
**9/9 grün, exit 0. v3.0.2 ist live.**

**Selbstprüfung:** `pytest -q` 995 passed (112 s), Tabu-Diff §0.3 leer, `node --check` nicht
nötig (kein JS/CSS-Touch, nur `deploy.sh` + sein Test), kein `pkill -f`. `systemctl restart`
lief ausschließlich über den Nikinger (`sudo`-Prompt live gesehen), der Agent hat an keiner
Stelle `systemctl` selbst aufgerufen — Hard Rule 9 durchgehend eingehalten.

**Die Phase bleibt 🔄, nicht ✅ — nur der Gate ist geschlossen, Step Z fehlt noch.**
Root-`CLAUDE.md` und `ROADMAP.md` entsprechend NICHT auf ✅ gesetzt; das wäre die stille
Abweichung, die die eigene Arbeitsweise-Regel ausdrücklich verbietet.

**Nächster Schritt: Step Z (Closeout), eigene Session.** Plan 2 §7.5, sieben Punkte:
Abnahmematrix §8.1 **vollständig** auswerten (jede Zeile mit Beleg, nicht mit Zuversicht),
`[VERIFY]`-Register §8.3 bilanzieren (**V118 — Zwillingskanten-Linienzahl — bleibt offen**,
aus dem Screenshot nicht beantwortbar, keine Knoten-Labels ohne Hover; entweder live nachklicken
oder den Smoke-Test um eine Label-Capture erweitern, bevor Z sie als geschlossen führt), Plan 2
§9 als kanonischer Closeout füllen (P8.6-W), eine Zeiger-Zeile in Plan 1 §9 (die einzige
erlaubte Änderung an dem 📕-Snapshot), Phase-Head/`ROADMAP.md`/`docs/INDEX.md`/Wurzel-
`CLAUDE.md` erst dann auf ✅, Übersichtsgrafik von „PARTIAL CLOSEOUT" auf die echte
Abnahmezahl, letzte `rotate_session_block.sh`-Rotation.

