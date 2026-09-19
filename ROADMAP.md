---
status: live
purpose: Phasenplan des Space-Servers — was in welcher Reihenfolge gebaut wird und warum, plus Status je Phase
read-when: Phasenwechsel, Scope-Frage („gehört X in diese Phase?"), Planung einer neuen Session
detail: L2
up: CLAUDE.md
down:
  - docs/concepts/phase1_storage_plan.md   # ausführungsreifer P1-Plan
  - docs/concepts/phase2_mcp_plan.md       # ausführungsreifer P2-Plan
  - docs/concepts/phase3_edge_plan.md      # ausführungsreifer P3-Plan
  - docs/concepts/phase4_auth_plan.md      # ausführungsreifer P4-Plan
  - docs/concepts/phase5_ui_plan.md        # ausführungsreifer P5-Plan
  - docs/concepts/phase6_shares_plan.md    # ausführungsreifer P6-Plan
  - docs/concepts/phase6_5_tools_images_plan.md   # ausführungsreifer P6.5-Plan
  - docs/concepts/phase7_spaces_admin_plan.md     # ausführungsreifer P7-Plan
  - docs/concepts/phase8_ui_graph_plan.md         # ausführungsreifer P8-Plan
updated: 2026-09-19 (**Nachtrag: drei Nikinger-Entscheidungen zu P9** — Domain als frueher P9-Schritt, Tailscaled-Watchdog freigegeben, und **neu**: eigener CUDA-Dienst auf der ungenutzten RTX 3060 als Ersatz der CPU-only-Vision-Strecke [Empfehlung LXC auf dem 3060-Host, Form entscheidet die Planungssession; `PHASE8_6_CLOSEOUT_HANDOVER.md` §4.8]. P9-Zeile entsprechend erweitert) | 2026-09-19 (**P8.6 abgeschlossen ✅ — Step Z durchgeführt, `v3.0.2` live seit 2026-09-18** [SHA `1ad2665`, `health_gate` 9/9]. Bilanz **45 ✅ · 5 ⚠️ · 0 ⬜ · 4 ersetzt** von 54 Zeilen, `pytest` **995**, `ui_budget` 5/5. Kanonischer Closeout in `phase8_6_ui_polish_plan2.md` §9 [P8.6-W], Einstieg für P9 in `PHASE8_6_CLOSEOUT_HANDOVER.md`. P9-Zeile um das Nikinger-Feedback vom 2026-09-19 ergänzt — zwei Bugs, ein Rechte-Thema, fünf Feature-Wünsche. Zwei `[VERIFY]` gehen offen über: V118, V136) | 2026-09-14 (**P8.6 Block H-R Teil 2 erledigt — drei CDP-Probe-Sub-Blöcke aus dem G-R-Nachtrag in einem Schritt ✅** — atomarer Block, ein Commit. **H-R.3** Editor-YAML-Bündigkeit: `.editor__head padding-bottom` 12 → 40 px (`calc(var(--space) * 1.5)` → `* 5`), Editor-Head-Unterkante wandert von y=198,80 auf y=226,80 (1440 px) — Diff zur .list__head-Unterkante (y=225,94) **0,86 px ≤ 2 px Toleranz** (V142-CDP-Probe pre 27,14 / post 0,86 px bei 1440 + 1200 px). **H-R.4** 1024-er Map-Overlap: V143-Probe misst **0 Rechteck-Schnittmenge** zwischen .list/.detail__graph/.rail bei 1024×768 in beiden Modi (Übersicht + Editor) — bestehende Stapel-Logik (`grid-template-rows: 1fr 1fr` + `.rail { grid-row: 1 / span 2 }` + `.detail { grid-column: 2 }`) ist korrekt, **kein CSS-Fix nötig**. **H-R.5** 1024-er Editor-Modus: V144-Probe misst 16/16 Knöpfe `reachable: true` (Archivieren/Speichern/×, 10 Format-Hilfen, Vorschau-Toggle, Bild-Insert, Anhängen + Input), keiner offscreen bei 1024×768 — **kein CSS-Fix nötig**. Drei neue statische Wächter (`test_editor_head_padding_bottom_aligns_with_list_head` mit Klammern-Balance-Parser für `calc(var(--space) * N)`, `test_1024_no_overlap_in_css`, `test_1024_editor_buttons_present`). Self-Check-Skript `phase8_6_ui_polish/scripts/p86_block_h_r_part2_self_check.py` neu (~290 Z., Playwright + CDP-Probe + 5 Screenshots + Login mit TOTP-Window-Retry). `pytest` 988 → **991** in 260 s, `ui_budget` 5/5 mit **143,7 KB** (app.css 24,7 → 24,8 KB gzip, +0,1 KB für den ausführlichen H-R.3-Kommentar + die Multiplikator-≥-4-Begründung im Wächter), Tabu-Diff §0.3 leer, kein Service-Touch (PID 991 nur gelesen), keine Wegwerf-Instanz nach dem Lauf mehr aktiv. 5 Selbst-Screenshots `p86_block_h_r_{01..05}_*.png` (100/99/132/76/91 KB): 1440 + 1200 Übersicht, 1440 Editor (YAML-Bündigkeit sichtbar), 1024 Übersicht (Liste oben + Karte unten sauber gestapelt), 1024 Editor (alle Knöpfe sichtbar). CDP-Proben `phase8_6_ui_polish/probes/v142_v143_v144_{pre,post}_fix.json` (~9 KB je). **Reihenfolge neu:** F → G → G-R ✅ → H ✅ → H-R-1+2 ✅ → J → Gate → Z. **Nächster Schritt: Block J** (P8.6-AJ, datierte Tabu-Ausnahme `phase4_auth/authserver/{crypto.py,store.py}` — `crypto.new_public_id()` mit Rejection-Sampling gegen führendes `-` + zwei Aufrufe in `store.py:294/393` + `authctl.py:199` help-Text; engere Tabu-Probe: `git diff --stat -- phase4_auth/authserver` muss genau zwei Dateien zeigen, `store.py` genau 2 Zeilen — jede Abweichung ist Abbruchgrund)) | updated: 2026-09-14 (**P8.6 Block H-R Teil 1 erledigt — H-R.1 OLED-BLACK für die drei Slots + H-R.2 account-nav-Akzent-Farbe in einem Schritt** — H-R.1 (N.13 Layer-Architektur-Revision): `body`/`.shell`/`.rail`/`.list`/`.detail` auf `var(--bg-void) = #000`, `.rail`-`linear-gradient` ersatzlos weg; Layer-3-Elemente (`.overview__graph`, `.update-banner`, `.editor__head`, `.list__head`) behalten `--surface`/`--surface-raised`-Tokens, Karte schwebt sichtbar (14 Stufen Helligkeits-Distanz statt 6); `--rail-top` bleibt im `:root` als Geist stehen. H-R.2 (N.14 Spezialfall Konto-Dialog, „ausnahmsweise" laut Nikinger): `.account-nav` jetzt `background: var(--accent-quiet)` + `border: 1px solid var(--accent-edge)` + `border-left: 3px solid var(--accent)` + Chevron `color: var(--accent)`; Hover `color-mix(in srgb, var(--accent-quiet), var(--accent) 50%)` + `outline: var(--accent-line)`; `.rail__action` (Einstellungen + Abmelden) bleibt neutral. 1 Test umbenannt + 6 neue Wächter (`test_three_slots_use_oled_black`, `test_rail_has_no_gradient_anymore`, `test_layer3_elements_keep_surface_tone` mit Plan-Korrektur `.detail__graph` → `.overview__graph`, `test_account_nav_uses_accent_fill`, `test_account_nav_hover_kept`, `test_rail_account_unchanged_from_block_h`, `test_rail_action_unchanged`). `pytest` 981 → **988** in 120 s, `ui_budget` 5/5 mit **143,6 KB**, Tabu-Diff §0.3 leer, kein Service-Touch (PID 991 nur gelesen). Drei Selbst-Screenshots `p86_block_h_r_{01..03}_*.png` (~135/135/150 KB). **Nächster Schritt: Block H-R-Teil-2** (CDP-Probe-Welle: H-R.3 Editor-YAML-Bündigkeit + H-R.4 1024-er Map-Overlap + H-R.5 1024-er Editor-Modus)) | updated: 2026-09-14 (**P8.6 Block G-R erledigt — Layout-Revision nach Sichtung, vier Befunde in einem Schritt behoben** — atomarer Block, eigener Commit (Nikinger-Vorgabe „Nein, bitte als G-R anhängen", kein Force-Push auf `081c432`). G-R.1 Breakpoints: 1280→1200 (Rail bleibt 240, „Navigationszeile kracht zusammen" gelöst) + neuer 1024-er-Stapel (Nav bleibt 240, Liste oben + Karte darunter, „Übersicht zusammenschieben" gelöst). G-R.2 Map-Leerraum + Layer-Tone-Drift: `.detail { background: var(--bg) }` neu (vorher Body-Erbe `--bg-void`, drei Töne statt einem). G-R.3 Editor-Header sticky + YAML bündig: `.editor__head` position:sticky + padding-top reduziert + `.panel__head { padding: 11px ... }` (Item-Row-Höhe ≈ Panel-Header-Höhe). G-R.4 Wächter: `test_shell_grid_is_240_480_1fr` umgestellt + vier neue Tests (`test_1200_breakpoint_keeps_rail_at_240`, `test_1024_breakpoint_stacks_list_over_detail`, `test_detail_uses_the_column_background_not_void`, `test_editor_head_is_sticky_with_the_list_head_background`, `test_panel_head_height_matches_a_list_row`). Mini-Plan `docs/concepts/phase8_6_ui_polish_block_g_r_plan.md` neu. `pytest` 976 → **981** (Baseline 970 + 4 G + 2 F + 5 G-R), `ui_budget` 5/5 mit **143 KB**, Tabu-Diff §0.3 trivial leer, kein Service-Touch (PID 991 nur gelesen). Sechs Selbst-Screenshots `p86_block_g_r_{01..06}_*.png`. **Reihenfolge neu:** F → G → G-R ✅ → H → J → Gate, G-R zwischen G und H auf Nikinger-Vorgabe 2026-09-14. Nächster Schritt: **Block H**) | updated: 2026-09-14 (**P8.6 Block G erledigt — Layout-Umbau, fünf Befunde in einem Schritt behoben** — `.shell` `240px 380px 1fr` → `240px 480px 1fr` per **P8.6-O2-Auslösung** (N.7 entschieden); DOM-Umzug `#list-overview` in `.list`-Slot + `#detail-graph` in `.detail`-Slot; `state.overview`-Flag neu; `.overview`-Grid + 1280-px-Query ersatzlos weg = **Befund 9b-Ursache** weg; `.detail__graph`-Höhenkette = V112-Wächter; `.overview__space-open` als Zeilen-Button mit Chips als `<span role="button">` = **Befund 6** behoben (P8.6-P wiederhergestellt). Befunde 3/4/5/7a mitbehoben (3 = Refresh aus .detail-Slot weg, 4 = Karte von 302 auf 720 px, 5 = Layout-Reorg, 7a = `renderOverview()`-Sperre im „Alle Items"-Modus). **Editor ersetzt die Karte, ESC bringt sie zurück** (N.8). `pytest` **976** (970 + 4 neue + 2 F), `ui_budget` 5/5 mit **141 KB** statt 130 KB (Plan §4.9-Erwartung „app.css kleiner" **nicht erfüllt**, dokumentierte Abweichung), Tabu-Diff §0.3 leer, Service-Touch 0 — PID 991 nur gelesen. **6 Selbst-Screenshots** `docs/screenshots/p86_block_g_{01..06}_*.png` (1440-Übersicht, 1440-Space-geöffnet, 1440-Editor-offen, 1440-Editor-nach-ESC, 1200-Übersicht, 1024-Übersicht). Plan 2 §4 ist maßgeblich; P8.6-Zeile oben aktualisiert. **Nächster Schritt: Block H** (Rail-Umkehr 7b + `.account-nav`-Anmutung). Reihenfolge-Empfehlung P8.6-AH: F → G ✅ → H → J → Gate) | 2026-09-14 (**P8.6 Block F erledigt — Layering + zwei Wächter scharf** — `phase8_6_ui_polish/scripts/p86_viewport_probe.py` neu (421 Z. / 16 KB, Playwright-Chromium, CDP-Probe nach Plan §2.2: `getBoundingClientRect` + `getComputedStyle` + `elementFromPoint`); E2a gegen Wegwerf Port 18773 (Hard Rule 9-konform über PID-Datei gestoppt). **Befund 9b banner-abhängig, nicht unconditional** — bei 1200 px mit Update-Banner zwei Recent-Items vom `.overview__col-right`-Container überdeckt, ohne Banner **0** sichtbare Buttons blockiert; die Plan-Annahme „`overflow: hidden` + `flex: 1` schlägt `height: auto`" stimmt nur halb — der eigentliche Auslöser ist die 140-px-Banner-Höhe. **V125** (gleiche Ursache 9a vs 9b?) **partiell** (9b-Natur geklärt, 9a wartet auf E2b), **V126** (1024 px unerreichbar?) **erledigt: 0**. **E2b wartet** auf `SPACE_PUBLIC_BASE_URL` + Produktions-`alpha`-Creds vom Nikinger. Status 🔄, Modul-Status Z10 🟡; `pytest` 969 + 1 Flake unverändert; Tabu-Diff §0.3 leer, Service-Touch 0 — sharefyx-mcp PID 991 nur gelesen) | 2026-09-13 (**P8.6 Plan 2 geschrieben** — `docs/concepts/phase8_6_ui_polish_plan2.md`; Bloecke E/F/G/H/J, Locks P8.6-W–P8.6-AL, Abnahme 33–54, `[VERIFY]` V123–V139. Sechs Nikinger-Entscheidungen N.7–N.12, darunter die entschiedene Ausloesung von **P8.6-O2** [`.shell` → `240px 480px 1fr`] und die **Umkehr von C1/N3-Lesart b**. Neuer Produktionsfehler gefunden: `pytest`-Baseline ist **969 + 1 Flake**. Status bleibt 🔄) | 2026-09-13 (**P8.6 Partial Closeout** — die Phase ist **nicht abgeschlossen und nicht ausgeliefert**: Gate ⬜ angehalten, Step Z ⬜, Badge `v3.0.1`, zwei ungepushte Commits. Die Nikinger-Sichtung vom 2026-09-12 ergab neun UX-Befunde statt der Freigabe; drei davon oeffnen gelockte Entscheidungen, einer ist auf der Produktion reproduziert. **Ein zweiter P8.6-Plan ist erforderlich.** Neu: `PHASE8_6_CLOSEOUT_HANDOVER.md` + `phase8_6_ui_polish_uebersicht.svg`; P8.6-Zeile umgeschrieben, Status bleibt 🔄) | 2026-09-12 (**P8.6 Block C ✅** — Struktur-Umbau: Einstellungen oben, Alle Items unten, Karte rechts voller Hoehe, klickbare Spaces, Ordner-Zaehler; `pytest` 970 V107, `ui_budget` 137,5 KB; **sechs Selbst-Screenshots** `p86_block_c_*.png` zeigen alle fünf Sub-Ziele + B4-Regression; sharefyx-mcp PID 991 unverändert; **Push + Deploy wartet auf Nikinger-Sichtung** der Screenshots — Drei-Bedingungen-Regel des Nikingers zu zwei Dritteln erfuellt; V115/V116/V117 belegt; drei Befunde waehrend Baus dokumentiert [activateView-Doppel-Definition, V117-Reset, V115-RAF]; Stand: Step 0/V/V-vision-befund/A/B/C/D [D1/D2/D4] ✅, V-plugin ⚠️ zurückgebaut, Gate §7 + Step Z als naechstes) | 2026-09-11 (P8.6 Block B ✅ + §5-Konvention; `pytest` 967, `ui_budget` 133,1 KB; vier Screenshots `p86_block_b_*.png`) | 2026-09-09 (Phase-8.5-Z-Closeout — Phase 8.5 mit Step Z **vollständig abgeschlossen**; Übersichtsgrafik + `PHASE8_5_CLOSEOUT_HANDOVER.md` neu (Umkehr der Locks P8.5-S/P8.5-R durch den Nikinger, im Plan §0.2 datiert), Plan §9 gefüllt; im Phase-8.5-Abschnitt die stale „v3.0 ist nicht ausgeliefert"-Korrektur durchgestrichen (der Deploy lief am 2026-09-05) und P8.5-S aus DRAUSSEN gestrichen; im Phase-8.X-Abschnitt die stale Notiz-Zahlen „16 Themen / 25 KB" auf **zehn Abschnitte / 40.9 KB** korrigiert, Schritt 1 als erledigt markiert, **Mobile-Hälfte der Außenkante aufgehoben** (Realtime bleibt draußen), Nummern-Frage „p8.7 vs. P9" als offen notiert)
---
# ROADMAP — Space-Server

**Build-Reihenfolge ist verbindlich.** Unter Zeit- oder Token-Druck fällt immer die *späteste*
Phase weg, nie eine frühere Regel. Insbesondere: die UI fällt weg, die Auth-Härtung nicht.

Statusglyphen: ⬜ nicht gestartet · 🔄 aktiv · 🟡 code-complete, nicht live-bewiesen · ✅ live-verifiziert

| Phase | Verzeichnis / Paket | Inhalt | Status |
|---|---|---|---|
| **P1** | `phase1_storage/` · `storage` | Datei-Store + Index + Versionierung. Kein Netz. | ✅ |
| **P2** | `phase2_mcp/` · `mcpserver` | MCP-Server, Token-Auth, 6 Tools. Lokal erreichbar. | ✅ |
| **P3** | `phase3_edge/` | Tunnel, systemd, Health, Logging, Ops-Skripte. Öffentlich erreichbar. | ✅ |
| **P4** | `phase4_auth/` · `authserver` | OAuth 2.1 + DCR; ersetzt den Pfad-Token. | ✅ |
| **P5** | `phase5_ui/` · `webui` | REST-API + Web-UI für Menschen. | ✅ |
| **P6** | `phase6_shares/` (kein eigenes Paket) | Freigaben, Ordner, `patch_item`, Update-Log, Bilder. | 🟡 |
| **P6.5** | `phase6_5_tools_images/` (kein eigenes Paket) | Werkzeug-Ergonomie, Abschluss Bilder. | 🟡 |
| **P7** | `phase7_spaces_admin/` (kein eigenes Paket) | Space-Verwaltung, Mehrfachauswahl, Konsolidierung. | ✅ |
| **P8** | `phase8_ui_graph/` (kein eigenes Paket) | UI-Neuanstrich v3, Verknüpfungs-Graph, P7-Erbposten. | ✅ |
| **P8.5** | `phase8_5_picker_release/` (kein eigenes Paket) | Link-Picker-Politur, v3-Vorabritt + Deploy; schließt Phase 8 ab. | ✅ |
| **P8.6** | `phase8_6_ui_polish/` | UI-Politur v3.0.2: Layout-Reorg, Layering, Rail-Umkehr, drei Graph-Fixes. **Abgeschlossen 2026-09-19, live seit 2026-09-18** (Release `20260918T183907.597248Z`, SHA `1ad2665`, `health_gate.sh --expected-version=v3.0.2 --expected-sha=1ad2665` **9/9 grün**, Ausgabe im Commit). **Zwei Pläne und drei Sichtungs-Revisionen**, weil die Nikinger-Sichtprüfung vom 2026-09-12 neun UX-Befunde statt der Freigabe zurückgab: Plan 1 (Step 0 · Step V · A · B · C · D) → **Bruch** → Plan 2 (E messen · F Layering · G Layout-Umbau · **G-R** · H Rail-Umkehr · **H-R** · **H-R-3** · J) → Gate GA1–GA4 → Step Z. **Bilanz 45 ✅ · 5 ⚠️ · 0 ⬜ · 4 ersetzt** von 54 Abnahmezeilen; `pytest` **995**, `ui_budget` 5/5 (144,7 KB von 250 KB), 38 Commits, 930/256 Zeilen Produktcode. **Keine neunte P1-Contract-Öffnung** — der Bereichs-Tabu-Diff `440e462^..HEAD` ist leer bis auf **eine** vorher angekündigte, datierte Ausnahme (**P8.6-AJ**, Block J: `phase4_auth/authserver`, 2 Dateien, `store.py` 2/2 Zeilen). Service-Touch durch einen Agenten **0**. **Drei Entscheidungen, die die Phase geprägt haben:** **P8.6-O2** wurde bewusst ausgelöst, vorgelegt und entschieden (`.shell` → `240px 480px 1fr`, P8.6-X) · **N.9** kehrte C1/N3-Lesart b um (Abmelden bleibt äußerster Knopf) · **N.12** ordnete die datierte Tabu-Ausnahme an, statt den `pytest`-Flake zu dulden — er war ein echter Produktionsfehler (`secrets.token_urlsafe(16)` liefert in **1,569 %** ein führendes `-`, das `argparse` als Optionsflag liest). **Zwei `[VERIFY]` gehen offen an P9:** **V118** (Zwillingskanten-Linienzahl, aus dem Screenshot nicht beantwortbar) und **V136** (Chips vs. `bindFolderDropTarget()`, nie beantwortet). Kanonischer Closeout: `docs/concepts/phase8_6_ui_polish_plan2.md` §9 (Lock P8.6-W; Plan 1 §9 trägt nur eine Zeiger-Zeile) · Einstieg für P9: `docs/concepts/PHASE8_6_CLOSEOUT_HANDOVER.md` · Grafik: `docs/concepts/phase8_6_ui_polish_uebersicht.svg`. | ✅ |
| **P9** | (nicht angelegt, Arbeitsname) | Obsidian-Map-/Graph-Umbau (`p8x_ui_polish_notes.md` §2) + verbundene AI-Sessions (§10.8). **Vorgemerkt 2026-09-10: „Ordner umbenennen"** — in P8.6 geprüft und bewusst vertagt, volle Analyse in `phase8_6_ui_polish_plan.md` §0.4.1 (die billige Frontend-Fassung lässt die `.share.yml` eines geteilten Ordners still zurück; der saubere Weg ist die **neunte P1-Contract-Öffnung**). Deploy-Ziel `v3.1.0`, laut Nikinger voraussichtlich letzter großer UI-Umbau. **[2026-09-19, aus dem P8.6-Closeout]** Neues Nikinger-Feedback liegt vollständig in `PHASE8_6_CLOSEOUT_HANDOVER.md` §4.1 — bewusst in drei Klassen statt als Feature-Liste: **zwei Bugs mit erstem Messbefund** (kein Drop-Ziel zurück auf die Space-Wurzel, `tree.js:205` ist die einzige Aufrufstelle · ESC prüft kein `document.fullscreenElement`, `app.js:204`), **ein Rechte-Thema** (Verschieben in fremde Spaces ist Hard Rule 4 / `.share.yml`, Einstieg `phase6_shares_plan.md` §0.7(a), nicht `app.css`) und **fünf Feature-Wünsche** (Logo + einheitliche Design-Vorlage, To-do-Checkboxen im Text, „aktuelle Aufgabe“ markieren/hervorheben, Aufgabe assignen, Löschen mit zweifacher Rückfrage + Namenseingabe — human-only, kein Bulk). Dazu offen: **echte Domain** statt `<node>.<tailnet>.ts.net` (Nikinger-Entscheidung), **Tailscaled-Watchdog** (eigene Mini-Phase), **`docs/INDEX.md`-Rotation** (dritter Budget-Verstoß in P8.6 — die Handarbeit trägt nicht mehr). **[2026-09-19, Nikinger-Entscheidungen zu P9 — drei Punkte sind entschieden, die Form nicht]:** **(1)** Die **echte Domain** wird als **einer der ersten Schritte in P9** eingebaut (raus aus „P9+"); der Weg — CNAME auf den Funnel-Hostnamen vs. eigener Reverse-Proxy — bleibt Planungsarbeit und haengt an der beschafften Domain. **(2)** Der **Tailscaled-Watchdog wird gebaut**; von den drei Ansaetzen deckt nachweislich nur der zyklisch pruefende (`tailscaled-watchdog.service`) den gemessenen Vorfall vom 2026-09-15 — ein `OnFailure=`-Hook feuert dort gar nicht, weil der Dienst durchlief. Ausloeser bleibt systemd, nie ein Agent (Hard Rule 9). **(3) Neu, nicht aus P8.6 stammend:** die ungenutzte **RTX 3060 (12 GB)** im Proxmox-Verbund bekommt einen **eigenen internen CUDA-Dienst**, der die CPU-only-Vision-Strecke abloest. Empfehlung (Details + Begruendung: `PHASE8_6_CLOSEOUT_HANDOVER.md` §4.8): **eigener LXC-Container auf dem 3060-Host mit Ollama, erreichbar als interner HTTP-Dienst auf der Proxmox-Bridge** — **nicht** in die sharefyx-VM, damit das Bauprinzip „der Server ist dumm" eine physische Grenze bleibt und kein Versprechen wird; die Client-Seite ist bereits konfigurierbar (`LOCAL_VISION_ENDPOINT`, `vision_ollama.py --endpoint`), der Umzug ist **eine Umgebungsvariable**, kein Code. Hard Rule 6 unberuehrt: interne Bindung, kein Funnel. Praeziser Ersatzgegenstand: **nicht** das Plugin (das ist seit 2026-09-11 zurueckgebaut), sondern das CPU-only-Ollama-Backend auf der sharefyx-VM. | ⬜ |

**[2026-09-08 Korrektur, Z-Closeout]:** P8 + P8.5 auf ✅ (Statusregel geändert — vom Nikinger
geprüfte Wegwerf-Automatisierung zählt jetzt als live-verifiziert, siehe `phase8_ui_graph/
CLAUDE.md` §Abnahmestand). Die bisherige **P8.X-Platzhalterzeile ist aufgeteilt** in **P8.6**
(kleine Politur, Patch-Bump `v3.0.2`) und **P9** (Graph-Umbau, Minor-Bump `v3.1.0`) — beide
Arbeitsnamen, noch nicht geplant/gelockt. `docs/concepts/p8x_ui_polish_notes.md` bleibt die
Sammel-Quelle für beide, bis eine Planungs-Session die Aufteilung offiziell zieht.

**[2026-09-06 Korrektur, Phase 8.5 D4-Sichtprobe-Folgesession]:** P8.5 fehlte als eigene
Tabellenzeile — beim Anlegen der P8.X-Zeile mitgefunden und nachgetragen, **keine**
inhaltliche Änderung. (P8.X selbst ist mit dem 2026-09-08-Eintrag oben in P8.6/P9
aufgeteilt worden.)

**[2026-08-23 Korrektur, P7 Step 0]:** P6.5 fehlte als eigene Tabellenzeile — beim Ergänzen der
P7-Zeile mitgefunden und nachgetragen, keine inhaltliche Änderung.

**Korrektur (2026-07-25, P2-Planungssession):** OAuth rückt von „ganz am Ende" auf „direkt nach
P3" — der Pfad-Token soll kurz leben, und die UI ist die Phase, die laut Build-Reihenfolge unter
Druck wegfallen darf, OAuth nicht. Begründung: `docs/concepts/phase2_mcp_plan.md` §0.3.

---

## Phase 1 — Storage-Kern
Status **✅** (2026-07-25): 8 Module + 68 Tests, `space_cli.py` als Beweis. Nikinger-Lauf gegen echten `DATA_ROOT` (`/home/savefyx/savefyx-data`) selbst ausgeführt. Details: `phase1_storage/CLAUDE.md` · Plan: `docs/concepts/phase1_storage_plan.md` · Handover: `docs/concepts/PHASE1_CLOSEOUT_HANDOVER.md`.

## Phase 2 — MCP-Server
Status **✅** (2026-07-26): 8 Module + 133 Tests (76 P1 + 57 P2), `mcp_smoke.py` als Beweis, **Adapter-Abnahme 21/21 gegen den echten Custom Connector** durch den Nikinger (`docs/concepts/P2_ADAPTER_ABNAHME_2026-07-26.md`). Details: `phase2_mcp/CLAUDE.md` · Plan: `docs/concepts/phase2_mcp_plan.md` · Handover: `docs/concepts/PHASE2_CLOSEOUT_HANDOVER.md`.

## Phase 3 — Exposure & Betrieb
Status **✅** (2026-07-27–2026-08-02): 13/13 live bestanden, **Tailscale Funnel** (ersetzt den ursprünglich geplanten Cloudflare-Tunnel, Korrektur 2026-07-28; **CGNAT-konform**, Hard Rule 6 eingehalten). Runbooks (`diagnose.sh` etc.) in `phase3_edge/CLAUDE.md`. Details: `phase3_edge/CLAUDE.md` · Plan: `docs/concepts/phase3_edge_plan.md` · Handover: `docs/concepts/PHASE3_CLOSEOUT_HANDOVER.md`.

## Phase 4 — OAuth 2.1
Status **✅** (2026-07-30): 16/16 live bestanden — Schnitt vollzogen, **Pfad-Token tot**, Argon2id + TOTP + DCR + PKCE, opake rotierende Token, zwei unabhängige Nutzer. Sicherheits-Review in `docs/concepts/P4_SECURITY_REVIEW_2026-07-29.md`. Details: `phase4_auth/CLAUDE.md` · Plan: `docs/concepts/phase4_auth_plan.md` · Handover: `docs/concepts/PHASE4_CLOSEOUT_HANDOVER.md`.

## Phase 5 — Web-UI
Status **✅** (2026-08-09): 20/20 live bestanden. Zwei Blöcke (A Sicherheit/Auth-Selbstverwaltung, B REST-API/UI) mit hartem Gate. **`git diff` auf `storage/`, `mcpserver/{tools,permissions,server}.py` blieb über die gesamte Phase leer** (Kriterium 18 — derselbe Seam-Beweis wie in P4, eine API-Fläche höher). Details: `phase5_ui/CLAUDE.md` · Handover: `docs/concepts/PHASE5_CLOSEOUT_HANDOVER.md`.

## Phase 6 — Freigaben, Ordner, Werkzeug-Ergonomie
Status **🟡** (2026-08-23, bewusst nicht ✅): Code-complete und live deployt, aber nur 12/39 Abnahmezeilen live-verifiziert (drei benannte Tasks für nächste Phase in `PHASE6_CLOSEOUT_HANDOVER.md` §4). Drei Blöcke (A Werkzeuge/Betrieb/Update-Banner, B Dateisystem mit SharePolicy, C Bilder nach 6.5 ausgewandert). Details: `phase6_shares/CLAUDE.md` · Handover: `docs/concepts/PHASE6_CLOSEOUT_HANDOVER.md`.

## Phase 6.5 — Werkzeug-Ergonomie und Bilder
Status **🟡** code-complete (13/14 live, P6.5-14 strukturell offen — Nikinger-Bewertung): fünf offene MCP-Werkzeug-Ergonomie-Punkte geschlossen + Abschluss Block C Bilder (`put_asset`/`get_item_asset`/`<untrusted_content>`). Drei neue Punkte nach Phase 6.5 in `PHASE6_5_CLOSEOUT_HANDOVER.md` benannt. Details: `phase6_5_tools_images/CLAUDE.md` · Handover: `docs/concepts/PHASE6_5_CLOSEOUT_HANDOVER.md`.

## Phase 7 — Space-Verwaltung, Mehrfachauswahl, Konsolidierung
Status **✅** (2026-08-28): 22/24 Abnahmezeilen live, 2 ❌ als benannte Defekte an Phase 8 vererbt (P7-24 TOTP-Replay im Batch, P7-4 Claude-nennt-IDs-statt-Titeln) — die Matrix ist **vollständig durchgelaufen**, das unterscheidet P7 von P6/P6.5. Live: `e88a624`, Health-Gate 3/3 grün. Drei Erbposten aus dem Live-Betrieb (P7-24, P7-4, `remove-space`-Auto-Reindex) in Phase 8 gebaut. Details: `phase7_spaces_admin/CLAUDE.md` · Handover: `docs/concepts/PHASE7_CLOSEOUT_HANDOVER.md`.

## Phase 8 — UI-Neuanstrich, Verknüpfungs-Graph, QoL

**Mission, drei Stränge:** (A) die drei benannten P7-Erbposten sind behoben bzw. entschieden —
ein Batch-Verschieben braucht eine einzige Passwort+TOTP-Eingabe (Reauth-Grant statt
TOTP-Replay), `remove-space` hinterlässt nie wieder einen stalen Index, P7-4 bekommt seine
Zweitprobe. (B/D) ein Mensch sieht in einem Graphen, welche Items wie verknüpft sind
(`links:`-Feld + `itm_`-Body-Referenzen + zuschaltbare Tag-/Ordner-Kanten), und die Übersicht
zeigt tablos, was tatsächlich gebraucht wird. (C) die UI verliert ihren AI-Template-Look:
Lucide-Icons statt HTML-Entities, IBM Plex 16px statt Inter 15px, Farblegende
own/shared/foreign, Liquid-Glass-Akzente mit Pflicht-Fallback — Version v3.0.

- **DRIN:** Reauth-Grant (`POST /api/v1/reauth`), `remove-space`-Auto-Reindex, P7-4-Zweitprobe
  + Textschärfung, achte P1-Contract-Öffnung (`linkscan.py`, `item_links`, `GET /api/v1/graph`),
  `#item/`-Navigation, Link-Picker, Icon-Sprite, Plex-Fonts, Farbsemantik, Glass-Akzente,
  tablose Übersicht, handgerollter Canvas-Graph, v3.0.
- **DRAUSSEN:** FastMCP-4/V79, Body-Volltextsuche UI, Rechteverwaltung über MCP, neues
  MCP-Graph-Tool, Löschen von Items, `_trash/`-Räumung, Funnel-Watchdog, Light-Mode,
  Glyph-Entscheidungen P6/P6.5.
- **Erstmals: Claude Code plant, opencode/M3 führt aus — ohne Advisor-Stufe in der Ausführung**
  (Nikinger-Entscheidung N12; Ersatzmechanismen im Plan §0.6).

**Status 🔄 (2026-09-01, Block A + B ✅ live-verifiziert, Gate B→C bestanden):**
Plan `docs/concepts/phase8_ui_graph_plan.md` ausführungsreif, alle zwölf Nikinger-Fragen
N1–N12 in §0.1 gelockt, Entscheidungen P8-A–P8-Q, Abnahmezeilen P8-1–P8-24, `[VERIFY]`
  V81–V92. Closeout wird §9 des Plans (P8-N: ein Dokument pro Phase, kein separates
  Handover). **Block A (A1 Reauth-Grant, A2 `remove-space`-Auto-Reindex, A3
  P7-4-Zweitprobe 🟡 mit benanntem Restdefekt Klammer/Aufzählung) + Block B
  (`storage/linkscan.py`, `item_links`-Tabelle, `GET /api/v1/graph`, `#item/`-
  Navigation, Link-Picker-Dialog) sind seit `main@007b73d` live, Release
  `20260901T103944.634877Z`. Gate B→C (2026-09-01) grün: 958/958 pytest, Charakterisierung
  byte-identisch, Tabu-Diff leer, `_graph_get` manuell 12/12, Playwright gegen
  Wegwerf 18/18. Nächster Schritt: Block C — Design-Fundament v3 (Plan §4).**

---

## Phase 8.5 — Link-Picker-Politur und v3-Release

**Mission:** drei 🟡-Restdefekte aus Phase-8-Closeout §9.4.1–§9.4.3 schließen, einen vollständigen
v3-Vorabritt über den nie ausgelieferten v3-Build fahren und ihn live deployen — diese Phase
**schließt Phase 8 formal mit ab** (N6, Präzedenz P7 Step A8 für Phase 6.5). ~~**Wichtige Korrektur zum Live-Stand:** v3.0 ist **nicht** ausgeliefert …~~
**[2026-09-05 erledigt]:** der Vorabritt lief 26/26, der Deploy ging durch — live seit
`main@6f19a8f`, Release `20260905T140325.378914Z`, Badge `v3.0.1`, Service-PID 355956.
Der Grund für den vollen 13-Stationen-Ritt (N5) bleibt der richtige: Block C/D waren ein
UI-Umbau, den nie ein echter Nutzer gesehen hatte.

- **DRIN:** Picker-Modus-Umschalter „Text-Link / Kante" mit `localStorage`-Persistenz
  (P8.5-§2 A1); Tastaturnavigation über `aria-activedescendant`-Muster (P8.5-§2 A2); Hint
  `_TITLE_NOT_ID_HINT` generalisierend geschärft mit verbindlicher Abbruchregel (P8.5-§3 B1);
  v3-Vorabritt gegen Wegwerf-Instanz mit 13 Stationen (P8.5-§4 C); Deploy `v3.0` → `v3.0.1`
  als **Nikinger-Aktion** (P8.5-§5 D2, Hard Rule 9); Phase-8-Closeout-Nachtrag
  (`phase8_ui_graph_plan.md` §9).
- **DRAUSSEN:** Phase-8-§9.4.6-Funde (Settle-Zeit / Foreign-Farbe / Knotenklick — bereits am
  2026-09-02 geschlossen), Phase-8-§9.4.7 Glyph-Entscheidung ✅/🟡 (Nikinger-Sache nach
  Live-Deploy + Sichtprüfung), geerbtes Phase-6/6.5/7-Ledger (`phase8_ui_graph_plan.md` §9.4.5),
  FastMCP-4/V79 (eigene Mini-Phase, P5-C), `_trash/`-Räumung, Funnel-Watchdog, Mobile/Realtime,
  Light-Mode, ~~Phase-8.5-Übersichtsgrafik (P8.5-S)~~ **[2026-09-09 aufgehoben, Nikinger]:**
  die Grafik existiert — `docs/concepts/phase8_5_picker_release_uebersicht.svg`, Korrekturnotiz
  im Plan §0.2.

**Plan:** `docs/concepts/phase8_5_picker_release_plan.md` (744 Zeilen, geschrieben 2026-09-03
gegen `main@6272cad`). N1–N7 in §0.1 gelockt, Entscheidungen P8.5-A–P8.5-T, Steps 0/A/B/C/D/Z,
Abnahmezeilen P8.5-1–P8.5-20, `[VERIFY]` V95–V105. **Closeout ist §9 des Plans (gefüllt
2026-09-09, kanonisch); Einstieg für die P8.6-Planung ist
`docs/concepts/PHASE8_5_CLOSEOUT_HANDOVER.md` §4.** **Step 0
abgeschlossen** (Haushalt-Funde, Skelett, Größenkorrekturen); **A1 committet** (`499d9be`,
2026-09-04, Picker-Modus-Umschalter + Body-Markdown-Link-Helper + `localStorage`,
Modul-Status 🟡, Tests ⬜, vollständiger Session-Block im Phase-Head); **Drift nachgezogen**
in einem separaten Folge-Commit (Wurzel-Current-state, dieser Absatz, INDEX-Header);
**A2 committet** (Tastaturnavigation + gemeinsamer Pick-Pfad `_pickLinkPickerAt` +
CSS-Block-Entdopplung am Picker; drei neue statische Tests; Modul-Status 🟡; A1-Block
nach `SESSIONS_ARCHIVE.md` rotiert); **B1 committet** (`_TITLE_NOT_ID_HINT` generalisiert
in `mcpserver/tools.py:159-164` — Schlußsatz „Das gilt in jeder Textform" wörtlich aus
Plan §3 B1; zwei Asserts in `test_tools.py`; Abbruchregel-Abschnitt im Phase-Head;
Modul-Status 🟡; A2-Block nach `SESSIONS_ARCHIVE.md` rotiert); Abnahmestand
**3 ✅ · 4 🟡 · 13 ⬜ von 20**. **nächster Schritt:** **Block C** — v3-Vorabritt gegen
eine Wegwerf-Instanz (Plan §4, 13 Stationen Playwright-Smoke gegen den nie ausgelieferten
v3-Build; Wegwerf-Setup mit tmp `DATA_ROOT`/`auth.sqlite3`/eigenem Port, inkl. Portierung
von `scripts/rotate_session_block.sh` aus Phase 7 für `phase8_5_picker_release/`).

**[2026-09-04, Block C committet]** v3-Vorabritt gegen Wegwerf Port 18773 (V98) gefahren:
`phase8_5_picker_release/scripts/wegwerf_setup_v3ritt.py` (Standing-Permission-Muster aus
Phase 8 reproduziert — eigener Port, tmp `DATA_ROOT`/`auth.sqlite3`, File-Keyring; 30
Items über 3 Spaces alpha/beta/gamma inkl. 1 archiviertes, 1 mit item-level `share_read=
["gamma"]` (P6-§35-39-Deploy-Blocker-Fall), 1 mit Bild-Asset via `put_asset()`; 11
explizite Kanten inkl. V102-Zwillings-Kante Buecherliste ↔ Empfehlungen Nikinger);
`scripts/rotate_session_block.sh` aus `scripts/` nach `phase8_5_picker_release/scripts/`
portiert, YAGNI aus A1/A2 geschlossen; `phase8_5_picker_release/scripts/
v3_ritt_playwright_smoke.py` neu (~720 Zeilen, `pyotp`+`async_playwright`). **Ergebnis:
26/26 Stationen grün** (Chromium 13/13 + Firefox 13/13, V101 für beide Browser
bestätigt); drei echte Befunde vorgelegt, **keine Code-Fixes im Tabu-Bereich nötig**:
(1) Smoke-Bug Edge-Keys `src_id`/`dst_id` → `src`/`dst` (gefixt im Smoke, kein
Server-Bug — passt zu `graph.js:325/394` und `webui/api.py:719`), (2) CSRF-Origin-
Mismatch zwischen `http://127.0.0.1:18773` und `SPACE_PUBLIC_BASE_URL=
https://wegwerf-v3ritt.invalid` wegen `_validate_base_url`-Pflicht (Befund für Step Z /
Plan §4.C3, **nicht** in dieser Phase lösbar ohne Server-Code-Touch), (3) Station 12
nur strukturell (`prefers-reduced-motion`-Regel im CSS gefunden, keine echte
Browser-Probe mit umgeschaltetem UA — bleibt, throwaway-verifiziert in Phase 8
`p8_22_smoke.py`); Modus-Selektor `<select>` vs. N3-Vorschau-Radio nicht als Befund
behandelt (P8.5-F-Planer-Substitution, P8.5-19-Sichtprüfung). Abnahmestand jetzt
**3 ✅ · 13 🟡 · 4 ⬜ von 20** (P8.5-5/-6/-7/-8/-10/-11/-13/-15/-16 aus Block C
`⬜`→`🟡`). 16 Screenshots `docs/screenshots/v3ritt_{chromium,firefox}_NN_*.png` neu.
`pytest -q` 962/962 unverändert (kein Python-Touch im Block-C-Setup), Tabu-Diff §0.3
leer, Service-Touch 0 (PID 195922 / ActiveEnterTimestamp 2026-09-02 11:51:57 CEST
nur gelesen; Wegwerf PID 337447 sauber abgebaut via `kill -TERM $(cat serve.pid)`,
Hard Rule 9-konform). **nächster Schritt:** **Block D** — Release-Vorbereitung
(`v3.0` → `v3.0.1`, neuer `## 2026-09-04`-Block in `docs/UPDATE_LOG.md` mit drei
menschenlesbaren Zeilen), D2 Deploy als **Nikinger-Aktion** (Hard Rule 9 + P8.5-Q,
niemals `sudo systemctl restart sharefyx-mcp` durch opencode/M3), D3 Health-Gate,
D4 Sichtprüfung am echten Gerät, D5 Vierte A3-Probe (an der die Abbruchregel §9.4.1
(N2) fällt oder hält).

**[2026-09-05, D1 committet]** Release-Vorbereitung opencode/M3: Badge `v3.0` →
`v3.0.1` in `phase5_ui/webui/static/app.html:20` (P8.5-N7); neuer `## 2026-09-05`-
Block in `docs/UPDATE_LOG.md` mit drei Zeilen (Picker-Modi / Tastatur / Generalisierter
Hint). **Datums-Drift zur Block-C-Spec ausdrücklich dokumentiert:** Block-C-Absatz oben
hatte noch `## 2026-09-04` vorgeschlagen (geschrieben am 2026-09-04, dem Tag von Block C);
heute ist `date +%F`/`date -u +%F` = 2026-09-05, und `deploy.sh` Z. 117–131 verlangt strikt
`today_utc` oder `today_local` als oberstes Datum, sonst Gate-Abbruch — Eintrag deshalb auf
2026-09-05 datiert. Block-C-Block per Hand nach `SESSIONS_ARCHIVE.md` rotiert
(newest-first, vor B1); Skript `scripts/rotate_session_block.sh` passt nicht auf das
Phase-8.5-Muster mit einem `## Session stopped`-Header + mehreren `### date`-Subblöcken
(Skript zählt `## Session stopped`-Header und sieht immer genau einen → Exit 2 „Bereits
konform"). Modul-Status D `⬜` → `🟡` mit D2–D5 als Nikinger-Aktionen vermerkt. `pytest`
nicht gelaufen (kein Python-Touch), Tabu-Diff §0.3 leer (`app.html` und `docs/UPDATE_LOG.md`
nicht tabu), Service-Touch 0 (PID 195922/ActiveEnterTimestamp 2026-09-02 11:51:57 CEST nur
gelesen). **nächster Schritt:** D2 — Deploy als Nikinger-Aktion
(`SHAREFYX_SYSTEMCTL="sudo systemctl" phase5_ui/scripts/deploy.sh main` in interaktiver
Vordergrund-Shell, V103 prüft den `sudo`-Prompt; Hard Rule 9 — niemals `sudo systemctl`
durch opencode/M3), D3 Health-Gate 3/3 + V105, D4 Sichtprüfung am echten Gerät +
P8.5-19-Abnahme des `<select>`-Modus-Selektors, D5 Vierte A3-Probe (entscheidet §9.4.1
Abbruchregel aus N2).

**[2026-09-05, D2 vom Nikinger zwischen D1 und D3 + D3-Prep committet]** D2 ist zwischen
D1 (Commit heute früh) und D3 (diese Session) **still durch den Nikinger gelaufen** —
Entdeckung kam erst beim ersten Probe-Lauf des Health-Gate-Skripts:
`/opt/sharefyx/current` → `20260905T140325.378914Z` → HEAD `6f19a8f` (D1), Service-PID
**355956** (statt der im D1-Block notierten 195922 — D2-Deploy hat den Dienst erwartungsgemäß
neu gestartet), `ExecMainStartTimestamp=2026-09-05 16:10:18 CEST`. Damit ist D3 nicht mehr
Vorbereitung, sondern **Verifikation des bereits deployten v3.0.1**. Neu gebaut:
`phase8_5_picker_release/scripts/health_gate.sh` (134 Zeilen bash, `set -uo pipefail`,
JSON auf stdout / Details auf stderr nach Hard Rule 7), acht Gates — `/health` 200 mit
Retry-Loop (max `--max-wait` Sekunden, Default 30, wie `deploy.sh` Z. 192-200), `/ui/login`
200, `/api/v1/me` 401, `/mcp/` 401 (wie `deploy.sh` Z. 202-217), `.rail__version` aus
`/ui/static/app.html` (**nicht** `/ui/login` — das ist `pages.py`s Auth-Template und enthält
keine Rail; erste Iteration fiel darauf herein, dann gefixt), `/opt/sharefyx/current` →
Release-Verzeichnis mit `.git`, optional `--require-todays-update-log` (oberster
`## YYYY-MM-DD` in `docs/UPDATE_LOG.md` == heute UTC/local, wie `deploy.sh` Z. 127-131),
optional `--expected-sha=<hex>` (Release-SHA matched Short- oder Full-Form per
Prefix-Vergleich). **Lauf-Beleg 2026-09-05 15:19:53Z** mit `--require-todays-update-log
--expected-sha=6f19a8f`: **8/8 grün**, Exit 0, JSON auf stdout
(`{"action":"health_gate","result":"ok","expected_version":"v3.0.1",
"actual_version":"v3.0.1","active_release":"/opt/sharefyx/releases/20260905T140325.378914Z",
"release_sha":"6f19a8fc1f0bcdc2c3bc91fc934a057964647ed4","port":8765}`). Drei Negativproben
separat verifiziert (Port 9999 → Gate 1 rot, `--expected-version=v9.9.9` → Gate 5 rot,
`--expected-sha=0000000` → Gate 8 rot). **P8.5-17 teilweise abgehakt:** Deploy gelaufen ✅,
Health-Gate 8/8 ✅, Badge `v3.0.1` live ✅, Update-Banner-Live-Anzeige ⬜ (braucht Auth,
Nikinger), V105 ⬜ (echter Anthropic-Connector, Nikinger). Modul-Status-Zeile 6 Block D um
D2 ✅ + D3 🟡 erweitert; Abnahmestand-Zeile P8.5-17 Health-Gate-Teil 🟡; Summary
**3 ✅ · 14 🟡 · 3 ⬜ von 20**; D1-Block (111 Zeilen) per Hand nach `SESSIONS_ARCHIVE.md`
rotiert (Skript passt nicht auf das Phase-8.5-Muster — bewährtes Vorgehen aus D1 selbst).
`pytest` nicht gelaufen (kein Python-Touch), `bash -n` OK, shellcheck nicht verfügbar
(übersprungen, keine Konvention im Repo), Tabu-Diff §0.3 leer, Service-Touch 0 (PID 355956
nur gelesen). **nächster Schritt:** **D4 ✅ erledigt 2026-09-06** (Sichtprüfung am echten Gerät durch den Nikinger,
Update-Banner sichtbar, beide Picker-Modi funktional, drei echte Findings dokumentiert: **P8.5-19
Radiogruppe** statt `<select>` — Tausch 5 Z. ausstehend; **P8.5-6 Bracket-Renderer-Bug** in
`markdown.js` — Fix ausstehend; **UX-2-Step-Knotenklick** als neues Feature für p8.X parkiert;
**Phase 8 ✅ + p8.X** als Nikinger-Entscheidung für Z vorgemerkt); **D5 Vierte A3-Probe**
(entscheidet §9.4.1 Abbruchregel aus N2 — Nikinger-Aktion); **V105-Connector-Check** (echter
Anthropic-Connector — Nikinger-Aktion); **optional vor Z** durch opencode/M3: Radiogruppe-Tausch
(P8.5-19) + Bracket-Renderer-Fix (P8.5-6); dann **Z (Closeout)** mit Phase-8-✅-Eintrag +
p8.X-Ankündigung in `phase8_ui_graph_plan.md §9.4.7`.

---

## Phase 8.X — UI-Polish-Folge-Phase (nur Notizen, kein Plan)

**Mission, ein Satz:** Nach dem v3.0.1-Deploy und dem Phase-8.5-Closeout sammelt diese
Folge-Phase die offenen UI-Polish-Wünsche aus der Sichtprobe-Folgesession 2026-09-06
(Nikinger + Fabian) plus die bereits in Phase 8.5 D4 parkierten p8.X-Punkte.

**Status:** ⬜ nicht gestartet, **kein** Plan-Doc, **kein** Locking. Nikinger-Entscheidung
in Phase 8.5 D4 vorgemerkt (`phase8_5_picker_release/CLAUDE.md` und
`phase8_ui_graph_plan.md §9.4.7`).

**Notiz-Sammlung:** `docs/concepts/p8x_ui_polish_notes.md` (L2, **40.9 KB**, 2026-09-06
angelegt, zuletzt 2026-09-09) — **zehn Abschnitte**: §1 Spaces-Layout-Reorg, §2 Obsidian-Map
(fünf Sub-Punkte), §3 Anzahl-Anzeige Ordner, §4 Edit-in-Place-Vision, §5 Layering-Design-System,
§6 „Konto"→„Einstellungen"-Rename, §7 De-AI-ierung-Lauf 2, §8 customizable Tags + Standard-Tag
„blocked", §9 direkter Feedback-Button, **§10 (2026-09-09) neun Nikinger-Punkte aus dem
Phase-8.5-Closeout-Auftrag** — Icon-/Trägerflächen-Radien, Hover als transparentere
Standardauswahl, Ordner-/Tags-Auswahl, klickbare Spaces, Einstellungsmenü, alles Klickbare mit
Farbausnahme für „Abmelden"/„Archivieren", verbundene AI-Sessions, Hochkant-/Handy-UI.
Anhang §A–§E. **Die Zahlen „16 Themen / 25 KB" hier standen bis 2026-09-09 stale.**

**Reihenfolge der nächsten Schritte (Stand 2026-09-09):**

1. ~~**Phase 8.5 Z**~~ **✅ erledigt 2026-09-09** — Phase 8 + 8.5 formal abgeschlossen,
   Closeout in Plan §9, Handover `docs/concepts/PHASE8_5_CLOSEOUT_HANDOVER.md`.
2. **Planungs-Session für P8.6** (Claude Code, weil §5 Layering + §10 design-system-weit
   sind) — beantwortet die §C-Fragen, schätzt Reichweite, spaltet ggf. in Sub-Phasen.
   **Erster Punkt der Phase: OpenCode-Vision-Plugin installieren** (Nikinger-Vorgabe).
   Einstiegsdokument ist das Handover §4, nicht die Phase-Heads.
3. ~~**Plan-Doc + Phase-Verzeichnis** — Name noch nicht gelockt~~ **✅ erledigt 2026-09-09**
   — gelockt als `phase8_6_ui_polish/` + `docs/concepts/phase8_6_ui_polish_plan.md` (P8.6-A).
   **Die Nummern-Frage ist entschieden:** der Nikinger hat bestätigt, dass sein „eher v3.1
   also p8.7" das meint, was die Dokumente **P9 → `v3.1.0`** nennen. **Es gibt kein P8.7.**
   Die verbundenen AI-Sessions (`p8x_ui_polish_notes.md` §10.8) sind damit P9-Inhalt.
   Umbenannt wurde nichts — der Wortlaut bleibt in §10.8 zitiert stehen.
4. **Ausführung P8.6** in opencode/M3 nach Plan §1–§8, Reihenfolge Step 0 ✅ → Step V
   **aufgeschoben** (Migration steht bevor, Plugin-Pfad zurückgestellt) → A → B
   → C/D → Gate → Deploy → Step Z. Der Closeout wird Plan **§9** (P8-N). **Aktuell
   (2026-09-10): Proxmox-Migration + Ollama-Setup + MCP-Wrapper-Skript als nächster
   Nikinger-Schritt** (Aktionsliste 7 Schritte im Phase-Head §Vormerkungen).

**Was NICHT in p8.X gehört** (klare Außenkanten, Notizen-Datei §B): Body-Volltextsuche
in der Web-UI (Q1 gelockt), Rechteverwaltung über MCP-Tools (P6-M), Löschen von Items
(F2), FastMCP-4/V79 (eigene Mini-Phase per P5-C), Funnel-Watchdog, ~~Mobile/~~Realtime,
Light-Mode (P5-X), Glyph-Entscheidungen P6/P6.5. **[2026-09-09, Nikinger]:** die
**Mobile-Hälfte ist aufgehoben** — die Hochkant-/Handy-Ansicht ist ab sofort ein benanntes
Zukunfts-Item (Notizen §10.9), kein P8.6-Auftrag, aber in einer freieren Phasenplanung zu
berücksichtigen. **Realtime bleibt draußen.**

---

## Bewusst nicht auf der Roadmap

- **Semantische Suche / Embeddings.** Verstößt gegen das Bauprinzip. Bei zwei Nutzern und
  einigen hundert Items schlägt Frontmatter-Filterung jede Vektorsuche in Präzision und Kosten.
- ~~**Feingranulare Rechte.** Zwei Personen, gegenseitiges Vertrauen. Cross-Space-Read ist
  standardmäßig an. Der Schutz gegen fremde Inhalte ist Rule 4, nicht ein ACL-Modell.~~
  **Ergänzung 2026-07-25:** P2 baut den Seam dafür (`Permissions.can_read`), damit es später kein
  Umbau wird — die Policy selbst bleibt bewusst `True` für alle, siehe „Zurückgestellt aus P2".
  **[2026-08-09 Korrektur, P6-Planungssession]:** Der Satz war bis heute richtig; mit Phase 6
  wird er widerlegt — Sichtbarkeitsstufen und Item-/Ordner-Freigaben (P6-J/K) sind jetzt Scope.
  Details: `docs/concepts/phase6_shares_plan.md` §0.5.
- **Mehrmandantenfähigkeit.** Wenn ein dritter Nutzer dazukommt, ist das eine Planungssession,
  kein `if`-Zweig. **[2026-08-09 Korrektur, P6-Planungssession]:** Der Satz ist **erfüllt, nicht
  widerlegt** — die Planungssession hat am 2026-08-09 stattgefunden und genau daraus ist Phase 6
  entstanden; ein dritter Nutzer wird darin real angelegt, geprüft und wieder entfernt (P6-W),
  über eine echte Planungssession, keinen stillen `if`-Zweig.
