---
status: live
purpose: Regeln, Konventionen, Arbeitsweise und aktueller Stand des Space-Servers — wird jede Session automatisch geladen
read-when: immer, vor jeder Aktion in diesem Repository
detail: L2
up: docs/INDEX.md
down:
  - ROADMAP.md                          # Phasenplan + Status je Phase
  - docs/INDEX.md                       # L0-Karte aller .md
  - phase8_6_ui_polish/CLAUDE.md        # aktive Phase (Phase 8.6, UI-Politur, Ziel v3.0.2)
  - phase8_5_picker_release/CLAUDE.md   # abgeschlossene Phase (Phase 8.5 ✅, schließt Phase 8 mit ab)
updated: 2026-10-04 (**die Wurzel-Rotation ist auf K=1 umgekehrt und die drei Doku-Strukturen sind rotiert — der letzte offene Hebel gegen die Softcap-Überschreitungen war eine Tabelle, kein Block** — opencode/M3, zwei Commits, kein Produktcode-Touch, kein Deploy) · **Umkehr von P9-A = Lock-Aufhebung, Nikinger-Entscheidung 2026-10-04, datiert im Plan (`docs/concepts/phase9_hardening_plan.md` §0) nachgetragen** · **Die Wurzel trug 24 Session-Blöcke in §Current state (91.123 B von 114.771 B) und steht jetzt bei einem** — die älteren **verbatim** nach `docs/PROJECT_SESSION_LOG.md` (L3, wohin die Wurzel seit 2026-09-08 selbst zeigt), per **neuem Skript `scripts/rotate_root_current_state.sh`** (sechs Gegenproben; **die erste Fassung behielt bei K=1 den ältesten Block**, weil sie die Reihenfolge des Phase-Head-Skripts übernommen hat, obwohl die Wurzel newest-**first** ist — die Byte-Gegenprobe hat es gemeldet, nicht die Menge) · **Byte-Buchhaltung auf das Byte: 221.957 B vorher == 221.957 B nachher** · **und die Antwort, die zwei Sessions offen war: es sind nicht die Blöcke.** Phase-9-Head 56.860 B (15.900 B über dem Softcap) → nach Block- und Kettenrotation 49.033 B → **immer noch 14 KB drüber**, weil die §-Modulstatus-Tabelle **30.564 B in 14 Zeilen** trug, davon **15.041 B in drei** · ausführliche Statusspalten jetzt **verbatim** in `phase9_hardening/MODULE_STATUS_ARCHIVE.md`, im Head ein Kurzstand je Step ⇒ **der Phase-9-Head liegt zum ersten Mal unter dem Softcap** · **drei Doku-Befunde, alle live schlechter als sie aussahen:** 2 von 13 Statuszellen waren **unsichtbarer Text** (rohes `\|` ⇒ vier statt drei Zellen ⇒ Phantom-Spalte, 4.097 B, darunter der komplette V153-Block) · `test_acceptance_numbers.py` **verwarf den Marker der zweiten `[VERIFY]`-Lesart** (V162 Lesart B konnte unbemerkt ⬜ → ⚠️) · **drei verklebte Fäden** in `SESSIONS_ARCHIVE.md` und **einer** in `ABNAHME_MATRIX.md`, vom Rotations-Werkzeug gefunden, vom Wächter nicht — **die erste Fassung des neuen Wächters meldete grün, als sie genau den Defekt reproduzierte, den sie verhindern sollte** (sie las die Daten an der falschen Stelle) · **V162 *(Lesart B)* ⬜ → ⚠️** mit Doku-Zitat; für `--tcp` schweigen die Docs in **keine** Richtung, ein Gegenlauf braucht einen zweiten Tailnet-Knoten mit Shell ⇒ **die `socat`-Wahl ist nicht widerlegt, sondern gedeckt** · **K=1 ist die Konvention, und selbst K=1 passt nicht** — nicht die *Anzahl* der Blöcke ist das Problem, sondern die Breite einer Tabelle · `pytest` 1209 → **1217**, `ui_budget` 5/5, `doc_health` 0, kein `systemctl`, kein `pkill -f` | 2026-10-02 (**P9 B17 gebaut** — Vorsichtsknopf auf die exakte Standardfläche: die Backlog-Liste war falsch (1 Knopf mit Befund, nicht 15; `.btn.action--caution` matcht nur `#archive-button`, `.btn-primary` ist deine dokumentierte Ausnahme), der eigentliche Befund war eine **Helligkeit** (`#2A313A` heller als `#0C1C31`), mein Vorschlag einer rot getönten `--caution-std-*`-Fläche brach zwei Lock-Zeilen der Konvention v3 und fiel nach Rückfrage — exakt die Standardfläche, wortgleich v3; 3 Wächter (1 umgedreht), Gegenprobe 4 → 8 rot, Pixel-Probe 14/14 mit Gegenlauf 6 rot, `pytest` 1167 → 1169; **Kontrast 4,38:1 bleibt unter AA, benannt nicht entschieden**) | 2026-10-02 (**Gate/Z-Doku-Hälfte**, dreizehnter Block, opencode/M3, ein Commit, kein Deploy, kein Code-Touch: `phase1_storage` §Geerbte Contracts und `phase5_ui` §Abnahmestand **verbatim** in zwei neue L3-Archive rotiert — **beide benannten Softcap-Überschreitungen weg** (47.570 → 20.212 B, 43.801 → 33.126 B); **P9-L: INDEX-`updated:`-Kette rotiert, und der erste echte Lauf fand einen Skript-Defekt** — `rotate_index_updates.sh` rotierte 1 von 3 Fäden wegen eines `updated: `-Präfixes im Faden, gegen das der Split-Anker blind ist, und meldete dabei „verlustfrei"; jetzt **Gegenprobe (e)** + 2 Tests, Gegenprobe am Wächter grün; **14 neue Tests** (2 Skript + 8 Rotations-Wächter in `test_doc_rotations.py` + 4 in `test_committed_probe_evidence.py` + 1 Test für die reparierte (e)-Prüfung; **Gegenprobe: 5 eingebaute Verstöße → 5 rot**, bzw. 2 → 3), `pytest` 1152 → **1167**, `doc_health` 0 · **dabei gefunden: der eingecheckte Browser-Beleg des trace-Blocks war der Gegenlauf selbst** — Probe rot (`alle_ok: false`, S5 `alpha`→`beta`), Bild 05 zeigte `beta`, weil Hand-Gegenlauf und Erfolgslauf dieselben Ausgabepfade haben. Code war korrekt (`editor.js:781`), Beleg nicht. Eigener Lauf → 8/8, Probe und fünf Bilder neu) | 2026-10-02 (**Block trace gebaut**, zwölfter Block, opencode/M3: `assignee` sichtbar + vom Client gefüllt, `updated_by` + Git-Autor, **zehnte P1-Contract-Öffnung ohne Schema-Sprung**; 17 neue Tests, `pytest` 1128 → **1152**, Gegenlauf G1–G5, Browser 8/8 gegen eine Zwei-Principalen-Instanz mit echter Git-Historie; **ein Bestandstest mitgezogen, einer datiert zugeschnitten statt entfernt**, ein Fund drei Phasen entfernt; Release-Commit + Deploy `v3.1.1` beim Nikinger) | 2026-10-02 (**Release-Commit `v3.1.0` steht** — Badge `app.html:20` + neuer `## 2026-10-02`-Block in `docs/UPDATE_LOG.md` mit 6 Zeilen, jede Aussage eine physische Zeile und am echten `parse_update_log()` gegengeprüft; `pytest` 1128, `ui_budget` 5/5. **Der Deploy selbst ist Nikinger-Arbeit** (sudo, Hard Rule 9), die Health-Checks sind reine `curl`-GETs ohne Rechte und laufen durch M3) | 2026-10-02 (**P9 Block doing gebaut** — `_BUCKETS["doing"]` + Rail-Label „In Arbeit", Step-F-Wächter umgedreht, `pytest` 1128, Browser 11/11 mit Gegenlauf 7 rot, keine zehnte Contract-Öffnung; Deploy `v3.1.0` jetzt Nikinger-Schritt) | 2026-10-01 (**P9: Deploy `v3.1.0` verschoben, und der Grund ist gemessen** — Befund 11: `doing` steht nach dem Deploy als echte Option im Status-Feld der Kopfdaten (`editor.js :: populateStatusSelect` listet `state.meta.status_values` roh), und genau diese Eigenschaft ist der offene Befund P9-P: `bucketFor()`/`_overview()` kennen den Wert nicht ⇒ die Aufgabe erscheint in **keinem** der vier Ordner-Zähler. Nikinger-Entscheidung: erst der Mini-Plan von Opus, dann bauen + deployen — deshalb **kein** Release-Vorbereitungs-Commit (ein heute datierter `UPDATE_LOG`-Block würde das `deploy.sh`-Gate bei späterem Deploy abbrechen lassen, und der Changelog-Text ist ohne die `doing`-Entscheidung nicht schreibbar) · **`.toolbar-btn` in Standardoptik gebaut** (war der letzte echte Knopf auf der alten Plastik; `:disabled` bleibt `--surface`, `.rail__glyph` bleibt als Badge bewusst alt), Pixel-Probe `p9_btn2_toolbar_probe.py` **13/13**, Gegenprobe 1 Verstoß → 5 rot, `pytest` 1120 → **1122** · **fünfte Wiederholung derselben Repo-Lehre in der eigenen Probe:** ein Wächter, der etwas anderes prüft als er behauptet — `count() == 1` für `[aria-current]` ist wertlos (matcht das Attribut, nicht den Wert: der Knopf trug `"false"`), ein Pixelvergleich bei `fx=fy=0.5` trifft die Beschriftung, und eine Verlaufsmessung stand im Deaktiviert-Block · vier Tailscale-Bilder nach `docs/screenshots/p9_step_a_*` versioniert, die leere SPA-Hülle gelöscht, `screenshots_latest/` rotiert) | 2026-09-14 (**P8.6 Block H-R Teil 2 erledigt: drei CDP-Probe-Sub-Blöcke in einem Schritt ✅ — H-R.3 Editor-YAML-Bündigkeit + H-R.4 1024-er Map-Overlap (kein Fix, 0-Overlap) + H-R.5 1024-er Editor-Modus (kein Fix, 16/16 reachable)** — opencode/M3 — atomarer Block, ein Commit. `phase5_ui/webui/static/app.css:1385` H-R.3: `.editor__head padding-bottom` von `calc(var(--space) * 1.5)` (12 px) auf `calc(var(--space) * 5)` (40 px) — Editor-Head-Unterkante wandert von y=198,80 auf y=226,80 (1440 px), .list__head-Unterkante bei y=225,94 → **diff_bottom 0,86 px ≤ 2 px Toleranz** (H-R.3-A Abnahme, V142-CDP-Probe pre-fix 27,14 / post-fix 0,86 px). H-R.4/H-R.5: V143 misst **0 Rechteck-Schnittmenge** zwischen .list/.detail__graph/.rail bei 1024×768 in beiden Modi — kein Bug, nur Wächter; V144 misst **16/16 Knöpfe `reachable: true`** (Archivieren/Speichern/×, 10 Format-Hilfen, Vorschau-Toggle, Bild-Insert, Anhängen + Input), keiner offscreen — kein Bug, nur Markup-Wächter. `phase5_ui/tests/test_static_routes.py` drei neue Tests: `test_editor_head_padding_bottom_aligns_with_list_head` (Klammern-Balance-Parser für `calc(var(--space) * N)`, fordert Multiplikator ≥ 4), `test_1024_no_overlap_in_css` (1024er-Media-Query hat `grid-template-rows: 1fr 1fr` + `.rail { grid-row: 1 / span 2 }` + `.detail { grid-column: 2 }`), `test_1024_editor_buttons_present` (Markup-Check für 6 Knopf-IDs + 9 data-md-Format-Hilfen + Titel-Input). `phase8_6_ui_polish/scripts/p86_block_h_r_part2_self_check.py` neu (~290 Z., Playwright + CDP-Probe + 5 Screenshots + TOTP-Window-Retry-Login). `pytest` 988 → **991** in 260 s, `ui_budget` 5/5 (**143,7 KB**, app.css 24,7 → 24,8 KB gzip), Tabu-Diff §0.3 leer, kein `pkill -f`, kein `systemctl`, sharefyx-mcp PID 991 nur gelesen. 5 Selbst-Screenshots `docs/screenshots/p86_block_h_r_{01..05}_*.png` (100/99/132/76/91 KB): bei 1440 ist die YAML-Kopfzeile bündig zur .list__head-Unterkante, bei 1024 sind Liste oben + Karte unten sauber gestapelt, Editor-Knöpfe alle im unteren Slot sichtbar. CDP-Proben `phase8_6_ui_polish/probes/v142_v143_v144_{pre,post}_fix.json` (~9 KB je). `screenshots_latest/`-Symlinks Block-H-R-Teil-1 → Block-H-R-Teil-2 (P8.6-AK blockweise, jetzt 5 Symlinks statt 3 — 03 zeigt jetzt den Editor mit Bündigkeit, 04+05 sind neu für 1024er). **Nächster Schritt: Block J** (P8.6-AJ, datierte Tabu-Ausnahme `phase4_auth/authserver/{crypto.py,store.py}` — `crypto.new_public_id()` mit Rejection-Sampling gegen führendes `-` + zwei Aufrufe in `store.py:294/393` + `authctl.py:199` help-Text; engere Tabu-Probe: `git diff --stat -- phase4_auth/authserver` muss genau zwei Dateien zeigen, `store.py` genau 2 Zeilen — jede Abweichung ist Abbruchgrund). Reihenfolge-Empfehlung P8.6-AH: G → G-R ✅ → H ✅ → **H-R-1 ✅** → **H-R-2 ✅** → J → Gate.) | 2026-09-14 (**P8.6 Block H-R Teil 1 erledigt ✅ — H-R.1 OLED-BLACK für die drei Slots + H-R.2 account-nav-Akzent-Farbe; H-R.3/.4/.5 ⬜ als Folgeblock** — atomarer Block, ein Commit. H1 P8.6-AE/N.9 (Befund 7b): `.rail__account` trägt wieder Einstellungen **und** Abmelden (Reihenfolge Einstellungen → Abmelden, Abmelden äußerster Knopf — Umkehr von Block C C1/N3-Lesart b); `.rail__action--account`-Regel ersatzlos weg (V137 geklärt); `.rail__account` ist `flex-direction: column` als Normalfall (die frühere Sonderregel in der wegoptimierten 1280-px-Media-Query war ein Geist). H2 (Befund 2): `.account-nav` als Flex-Container mit linker Akzentkante `2px solid var(--line-strong)` + Chevron-Icon `#i-chevron-right` rechts via `margin-left: auto` (gleiche Mechanik wie `.tree__count` aus Block C C5) — kein Rückfall in `.btn` (B3-Kategorie „Navigation" trägt); V133 erledigt. **Wächter:** `test_rail_order_settings_before_tree_logout_last` umbenannt + umgekehrt zu `test_rail_order_settings_and_logout_at_the_end` (P8.6-I-Mechanik), Docstring trägt beide Richtungen (2026-09-09 N3-Lesart b → 2026-09-13 N.9); `test_app_html_has_a_live_manage_spaces_entry`-Regex an nested `<svg>` angepasst (kein semantischer Drift). `pytest` 981 unverändert (1 Test umbenannt, 1 angepasst, 0 neu), `ui_budget` 5/5 (**143,1 KB**, app.css 24,0 → 24,2 KB gzip), Tabu-Diff §0.3 leer, kein `pkill -f`, kein `systemctl`, sharefyx-mcp PID 991 nur gelesen. **Drei Selbst-Screenshots** `docs/screenshots/p86_block_h_{01..03}_*.png` (111/110/141 KB). `screenshots_latest/`-Symlinks Block-G → Block-H (P8.6-AK blockweise — waren seit Block G nicht nachgezogen worden). **Nächster Schritt: Block J** (der `pytest`-Flake, P8.6-AJ, datierte Tabu-Ausnahme für `phase4_auth/authserver/{crypto.py,store.py}` — neue Funktion `new_public_id()` + zwei Aufrufe, `authctl.py:199` mit `help`-Text für Altbestand). Reihenfolge-Empfehlung P8.6-AH: G → G-R ✅ → H ✅ → J → Gate, jetzt mit H abgeschlossen.) | 2026-09-14 (**P8.6 Block G-R erledigt: Layout-Revision nach Sichtung, vier Befunde in einem Schritt behoben ✅** — atomarer Block, ein eigener Commit (Nikinger-Entscheidung 2026-09-14: „Nein, bitte als G-R anhängen", kein Force-Push auf `081c432`). G-R.1 **Breakpoints**: `@media (max-width: 1280px)` ersetzt durch `@media (max-width: 1200px)` (Nikinger-Vorgabe: Rail bleibt 240 px, NICHT auf 64 px kollabieren — „Navigationszeile kracht zusammen" gelöst); Liste 480 → 380 px; `display: none`-Regeln für Rail-Labels/Brand/Tree-Group entfallen ersatzlos. `@media (max-width: 1024px)` ersetzt durch Stapel-Logik: `grid-template-columns: 240px 1fr` + `grid-template-rows: 1fr 1fr` + `.rail { grid-row: 1 / span 2 }` + `.detail { grid-column: 2; grid-row: 2 }` — Nikinger-Vorgabe: „Übersicht zusammenschieben und nav bar weiterhin vollständig zeigen", nicht Karte wegblenden. data-view-Switching-Logik aus Block G ersatzlos raus. G-R.2 **Map-Leerraum + Layer-Tone-Vereinheitlichung** (Befund 1-Fortsetzung): `.detail { background: var(--bg) }` neu — vorher erbt von body (`--bg-void = #000`), drei sichtbare Töne für „Spalten-Hintergrund" waren `--bg` in `.list`, `--bg-void` in `.detail`, `--surface` in der Karte. Nach G-R.2: `.list` und `.detail` haben denselben `--bg`-Ton, der schwarze Ring rund um die Karte (Folge von `.detail__graph`-Padding) verschwindet. `.detail__graph { padding: calc(var(--space) * 2) calc(var(--space) * 4) }` — oben/unten 16 px statt 32 px. G-R.3 **Editor-Header sticky + YAML bündig** (Befund 6/7-Fortsetzung): `.editor__head { position: sticky; top: 0; background: var(--surface-raised); border-bottom: 1px solid var(--line); z-index: 1; padding: calc(var(--space) * 0.5) calc(var(--space) * 3) calc(var(--space) * 1.5) }` — padding-top von 12 px auf 4 px reduziert, die YAML-Kopfzeile rückt nach oben und schließt bündig mit der Suchzeilen-Unterkante im Listen-Slot ab. Sticky + `--surface-raised` als Pendant zu `.list__head` (Step 7b-Verhalten). `.panel__head { padding: 11px calc(var(--space) * 3) }` — vertikales Padding von 6 px auf 11 px erhöht, Item-Row-Höhe (~41 px) ≈ Panel-Header-Höhe (~41 px) für „buendig"-Optik. G-R.4 **Wächter**: `test_shell_grid_is_240_480_1fr` aus Block G umgestellt (drei Anker statt zwei, neue 1200- und 1024-Werte), vier neue Tests `test_1200_breakpoint_keeps_rail_at_240`, `test_1024_breakpoint_stacks_list_over_detail`, `test_detail_uses_the_column_background_not_void`, `test_editor_head_is_sticky_with_the_list_head_background` + `test_panel_head_height_matches_a_list_row`. **Mini-Plan** `docs/concepts/phase8_6_ui_polish_block_g_r_plan.md` neu (~12 KB). **Echte Fund beim Bau:** f-string-Regex-Match auf `css[m.start():m.end()]` (in `test_overview_grid_and_its_media_query_are_gone`) hatte eine `]`-Klammer zu wenig — der `.match()`-Aufruf schlug fehl, das Test-Module kompilierte nicht. Behoben im selben Commit. **Doku-Hygiene:** `test_1024_breakpoint_stacks_list_over_detail` musste mit einem Wort-Grenzen-Lookahead `\.detail(?![a-zA-Z_-])\s*\{` ausgestattet werden (compound `.detail__back` wird vom Bare-Selector nicht mitgezogen), und die Kommentar-Beispieltexte in der 1024-px-Media-Query (`shell[data-view="list"] .detail { display: none }`) wurden aus dem Kommentar entfernt (Regex matchte sonst die Kommentar-Buchstaben). Modul-Status Z13 ⬜→✅ (Reihenfolge-Anpassung: Block G-R ist zwischen Block G und Block H eingeschoben — G → G-R ✅ → H → J → Gate). `pytest` 976 → **981** in 248 s (Baseline 970 + 4 G + 2 F + 5 G-R), `ui_budget` 5/5 (**143 KB**, +1,6 KB roh; app.css 73.593 → 77.301 B), Tabu-Diff §0.3 trivial leer, kein `pkill -f`, kein `systemctl`, sharefyx-mcp **PID 991** nur gelesen. **Sechs Selbst-Screenshots** `p86_block_g_r_{01..06}_*.png` (111/134/110/131/93/128 KB): 1440-Übersicht (Layer-Tone vereinheitlicht), 1440-Editor-offen (sticky-Header + YAML bündig), 1200-Übersicht (Rail 240 mit Labels), 1200-Editor-offen, 1024-Übersicht (Liste oben + Karte darunter GESTAPELT), 1024-Editor-offen (Editor ersetzt Karte im unteren Slot). **Nächster Schritt: Block H** (Rail + Konto-Dialog, Befunde 7b + 2 — Nikinger-Vorgabe vom 2026-09-14: nach G-R ist die Reihenfolge H → J → Gate, nicht mehr J dazwischen)
---
# CLAUDE.md — Project Instructions

> Read this file before doing anything in this repository.
> It is the single source of truth for project rules, conventions, and current state.

---

## What this project is

Ein **geteilter Kontext-Space-Server** für zwei Personen (Nikinger + Kollege) und deren
Claude-Instanzen. Notizen und Aufgaben liegen als Markdown-Dateien mit YAML-Frontmatter auf
einer Heim-VM; Claude greift über einen **Remote-MCP-Server** (Custom Connector, Streamable
HTTP) lesend und schreibend darauf zu, Menschen über eine Web-UI oder direkt im Editor.

Der Server läuft hinter **CGNAT** (RUT X50, Mobilfunk) — die Verbindung kommt von Anthropics
Backend, nicht vom Client. Erreichbarkeit daher **ausschließlich über einen ausgehenden
Tunnel**, niemals über Port-Forwarding.

Build order: `ROADMAP.md` · Doku-Karte: `docs/INDEX.md`

---

## Core principle (read carefully)

**Bauprinzip: Der Server ist dumm.**

Die gesamte Intelligenz sitzt beim Client (Claude). Der Server ist ein Aktenschrank mit
Schloss — mehr nicht.

**Der Server macht:**
- Dateien lesen/schreiben (atomar), Frontmatter parsen/serialisieren
- Index pflegen, Suchen beantworten, Paginierung
- Auth (Token → Space), Autorisierung (eigener Space schreibbar, fremde read-only)
- Versionierung, Konflikterkennung, Git-Commits
- Fehlerbehandlung, Logging, Health

**Der Server macht NIEMALS:**
- LLM-Calls, Embeddings, semantische Suche, Zusammenfassungen, Auto-Tagging
- irgendeine Form von „Verstehen" des Inhalts

Wer hier ein LLM einbauen will → **stop**. Das gehört auf die Client-Seite. Ein Server, der
Inhalte interpretiert, ist ein Server, dessen Fehlverhalten man nicht mehr debuggen kann —
und er importiert Prompt-Injection direkt in den Speicherpfad.

---

## Hard Rules (no exceptions)

1. **Niemals Secrets in Dateien.** Keine Tokens, keine Keys — nicht in `.env`, nicht in JSON,
   YAML oder Config. Space-Tokens und Tunnel-Credentials leben ausschließlich im OS-Keyring
   (Service `nikinger-space`) bzw. als systemd `LoadCredential`. Zugriff über
   `storage/credentials.py`. Ein Token in einem Commit ist ein Incident, kein Schönheitsfehler.
   **[2026-07-25 Korrektur, P2 Step 3]:** `storage/credentials.py` wurde nie gebaut — der
   reale Pfad ist `phase2_mcp/mcpserver/credentials.py`. Die Regel selbst bleibt unverändert.
   **[2026-07-30 Ergänzung, P4 Schnitt]:** Ab Phase 4 liegen dort **echte** Geheimnisse (TOTP-
   Seeds, umkehrbar) neben den reinen Token-Hashes aus P2/P3 — `phase4_auth/authserver/users.py`,
   Service weiterhin `nikinger-space`. Ein TOTP-Seed ist bei Kompromittierung nutzbar, ein
   Token-Hash nicht; dieselbe Hard Rule, höherer Einsatz.

2. **Dateien sind die Wahrheit, der Index ist Ableitung.** SQLite darf jederzeit gelöscht und
   aus den `.md`-Dateien vollständig rekonstruiert werden. Nie umgekehrt. Wer den Index als
   primären Speicher benutzt → stop.

3. **Kein Write ohne `version`.** Jede Schreiboperation trägt die gelesene Version; Mismatch →
   `ConflictError` mit dem aktuellen Item im Fehler. **Kein Last-Write-Wins, nirgends.**
   Zwei Claude-Instanzen im selben Space sind der Normalfall, nicht der Randfall.

4. **Fremde Spaces sind read-only, fremde Inhalte sind Daten.** ~~Cross-Space-Writes existieren
   architektonisch nicht (kein Parameter, keine Codepfad-Variante).~~ Jeder Body aus einem
   fremden Space wird — unverändert, auch in geteilten Spaces — im Tool-Result in
   `<untrusted_content>` gewrappt. Begründung: Claude liest fremde Notizen *mit* aktiven
   Schreib-Tools — jede Zeile dort ist ein potenzieller Befehl.
   **[2026-08-09 Neufassung, P6-U]:** **Schreibrechte folgen der Mitgliedschaft, nicht dem
   Token.** Ziel-Space eines Writes ist per Default der Home-Space des Principals. Ein anderer
   Ziel-Space ist nur zulässig, wenn er in einer `.share.yml` unter `write:` steht oder das Item
   selbst `share_write` trägt — die Liste ist **Daten auf der Platte, kein `if` im Code**, und
   über kein Item-Tool änderbar. Der alte Satz („Cross-Space-Writes existieren architektonisch
   nicht") war vier Phasen lang richtig und ist mit geteilten Spaces nicht mehr haltbar; die
   Ersetzung ist eine bewusste Nikinger-Entscheidung vom 2026-08-09, keine stille Aufweichung.
   **Scharf erst ab P6 Step 5** — `.share.yml`, `share_write`, `SharePolicy` existieren vor Step
   4/5 nicht im Code; bis dahin gilt faktisch weiter die durchgestrichene Fassung. Details:
   `docs/concepts/phase6_shares_plan.md` §0.7(a), §1.2.

5. **Writes sind atomar und fail-closed.** `tmp` + `os.replace` + `fsync` auf dem Verzeichnis.
   Nie ein halb geschriebenes Item auf der Platte. Jeder erfolgreiche Write erzeugt einen
   Git-Commit im Datenverzeichnis (Undo + Historie kostenlos).

6. **Nie ein offener Port am Router.** Erreichbarkeit ausschließlich über ausgehenden Tunnel.
   Wer Port-Forwarding oder DynDNS vorschlägt → stop, das scheitert an CGNAT und öffnet die
   Heim-VM.

7. **Logging → stderr; stdout nur maschinenlesbares JSON.** Atomic commits. Kein Subtask
   „done" ohne grünes `pytest` (gemockt, **kein Netz, kein echter Tunnel** in Unit-Tests).

8. **Commit ⇒ Doc-Update (zwingend, auch auf direkte Anweisung).** Jeder Step-Abschluss-Commit
   aktualisiert im **selben** Commit die Modul-/Status-Tabelle der Phase **und** den
   `## Session stopped`-Block. Neue `.md` ⇒ Zeile in `docs/INDEX.md` im selben Commit.

9. **Niemals per Regex-Substring Prozesse killen, niemals den systemd-Dienst anfassen.**
   `pkill -f <muster>` matcht mit Extended Regex — ein einzelner `.` matcht `/`, ein Modulname
   im eigenen und im Production-Args reicht, um die falsche PID zu treffen. Konkret
   (2026-09-01, Phase 8 Step A3 Nachbereitung): `pkill -f "phase2_mcp.scripts.serve"` killte
   sowohl die Wegwerf-Instanz als auch die Produktion (`sharefyx-mcp.service`, PID 38101,
   SIGTERM, Journal bestätigt). Stopp-Reihenfolge: **eigene** Wegwerf-Instanzen sind erlaubt
   zu stoppen, aber ausschließlich über PID-Datei, `pgrep -f` mit Anker (`$`) oder über den
   eindeutigen Port — nie über Regex im Cmdline. Den **einen** systemd-verwalteten
   `sharefyx-mcp.service` startet/stoppt/restartet **ausschließlich der Nikinger**
   (`sudo systemctl ...` läuft nicht aus dem `savefyx`-User, und auch wenn es liefe:
   Handlungsgrenze). Vor jedem `kill`/`pkill`/`systemctl` zuerst fragen: *ist das die echte
   Instanz, oder meine Wegwerf-Instanz, oder gar nicht meine?* Im Zweifel: fragen, nicht
   schießen.

---

## Working style

- **Quelle der Wahrheit ist der Code, nicht dieses Dokument.** Bei Widerspruch gewinnt das
  getestete Artefakt; das Dokument wird sofort mit datierter Korrekturnotiz gefixt.
- **`[VERIFY]`-Marker:** Alles, was gegen den echten Repo-Stand oder eine externe API geprüft
  werden muss, ist so markiert. Bei Ausführung verifizieren, **nie** als gesichert übernehmen.
- **Gelockte Entscheidungen bleiben gelockt.** Widersprechende Evidenz wird ein expliziter
  Befund für den Menschen, nie eine stille Abweichung.
- **Act vs. ask:** reversible, in-scope Schritte selbst ausführen; bei destruktiven Aktionen,
  Scope-Änderungen und Out-of-Scope-Edits stoppen und fragen.
- **Handover für einen kalten Leser schreiben.** Ergebnis zuerst, kein Session-Slang, nächster
  Schritt konkret genug zum Sofortstart.
- **Schritte, die am Fabi-Konto hängen, sind nie ein Phasen-Blocker.** Wenn eine Abnahmezeile nur
  durch eine Handlung des zweiten Claude-Kontos erfüllbar wäre, ist sie **zurückgestellt** und
  wandert in die nächste Phase — sie steht dann als ⬜ mit Grund und Zuständigkeit in der Matrix und
  **nicht** als offener Rest in der Übergabe. *Datierte Nikinger-Entscheidung 2026-10-04:* P9-13 und
  V150 („`list_spaces` aus **beidem** Claude-Konten über die neue Adresse") waren über zwei Sessions
  ⚠️ „1 von 2 Konten" und damit faktisch ein Blocker; sie sind heute auf ⬜ mit Wanderungsvermerk
  nach P10 gesetzt. **Begründung, die man merken muss:** ein Schritt, den nur ein Mensch mit einem
  Konto tun kann, ist keine Arbeit, die eine Phase aufhält — er ist ein Termin. Ein echter Blocker
  wäre ein **Code**-Fehler oder ein **Mess**-Befund.
- **Vor „das braucht einen echten Menschen/Connector" nachsehen, nicht neu erfinden:**
  `docs/concepts/sichtpruefung_automation_conventions.md` sammelt Techniken, mit denen sich
  Sichtprüfungen, die auf den ersten Blick blockiert wirken, doch skripten lassen (Canvas-
  Instrumentierung, OAuth-Dance ohne Browser, Zwei-Principal-Wegwerf-Muster). Erst dort
  nachsehen, dann ggf. recherchieren.

## Doku-Hygiene (Doc-Layers)

Vollspec: `docs/DOC_LAYERS_CONVENTION.md` (v1, 2026-07-06) — **byte-identische Kopie aus dem
Trading-Bot-Repo**, dort bewusst projekt-agnostisch geschrieben. Sie wird hier **nicht**
projektspezifisch angepasst: zwei Kopien derselben Regel, die sich unterschiedlich entwickeln,
sind schlimmer als eine, die an einer Stelle etwas allgemein formuliert ist. Wer sie ändern
will, ändert sie im Trading-Bot-Repo und kopiert erneut.

Kurzform: **L0** = `docs/INDEX.md` · **L1** = ≤15-Zeilen-Header-Card oben in jedem *lebenden*
Dokument · **L2** = schlanke Bodies, Softcap **≤40 KB** · **L3** = Archive und datierte
Snapshots. Rotationsregel ab Tag 1 scharf: ein Phase-Head trägt **genau einen** aktuellen
`## Session stopped`-Block; der vorherige wandert **verbatim** nach `SESSIONS_ARCHIVE.md`.
Durchführung über `scripts/rotate_session_block.sh <phase_verzeichnis>`, nie von Hand.

> Diese Regel gilt hier ab dem ersten Commit, nicht als späterer Rettungseinsatz. Im
> Trading-Bot-Repo wuchs `phase8_scheduler/CLAUDE.md` auf 211 KB, bevor sie eingeführt wurde.

---

## Current state

*Neue Session-Blöcke wachsen **oben** in dieser Sektion; die älteren rotieren **verbatim** nach
`docs/PROJECT_SESSION_LOG.md` — per `scripts/rotate_root_current_state.sh` (K=1, sechs Gegenproben,
u. a. byteweise Reassemblierung und Nachlesen jedes Blocks), **nie von Hand**. Die vollständige
Chronik der Phasen 1–8, der Hard-Rule-Korrekturen und der älteren Blöcke: `docs/PROJECT_SESSION_LOG.md` (L3).*

**[2026-10-05, die alte Adresse darf unbefristet schreiben — gebaut, nicht deployt — ein Commit, Produktcode
im Übergangsfenster, kein Service-Touch.]** Der Arbeitslaptop des Nikingers erreicht
`sharefyx.eurofyx.com` hinter dem Firmen-VPN (genua genuconnect) nicht: `NS_ERROR_NET_RESET`, 0 B übertragen.
Der Server ist gesund: DNS, TLS und `303` sind von der Heim-VM gemessen, und das MacBook kommt durch.
Vermutet, nicht belegt, ist ein Filter gegen neu registrierte Domains. **Nikinger-Entscheidung
2026-10-05:** beide Adressen schreiben parallel, bis die neue vom Arbeitslaptop aus belegt funktioniert.
Dafür gibt es `LEGACY_UNTIL=open` (fail-closed, nur das exakte Wort; CSRF-Pfad byte-identisch). Der
Dialog auf der alten Adresse nennt dann keinen Termin. **Damit ist der Satz „am 2026-10-18 schließt
das Übergangsfenster von selbst" aus dem Block vom 2026-10-04 überholt.** **Live seit 2026-10-05:**
`v3.1.2` (SHA `f4ef319`), Gate `ok`, und der laufende Prozess trägt `LEGACY_UNTIL=open`. Die Deploy-Schritte, die Notlösung ohne Release und die
PowerShell-Diagnose für den Laptop stehen im Session-Block vom 2026-10-05 in `phase9_hardening/CLAUDE.md`.
Der übrige Stand der Phase 9 ist unverändert: Abnahmezahlen in `phase9_hardening/ABNAHME_MATRIX.md`,
P9-15 ist die offene Aufgabe.

