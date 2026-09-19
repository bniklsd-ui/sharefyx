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
updated: 2026-09-14 (**P8.6 Block H-R Teil 2 erledigt: drei CDP-Probe-Sub-Blöcke in einem Schritt ✅ — H-R.3 Editor-YAML-Bündigkeit + H-R.4 1024-er Map-Overlap (kein Fix, 0-Overlap) + H-R.5 1024-er Editor-Modus (kein Fix, 16/16 reachable)** — opencode/M3 — atomarer Block, ein Commit. `phase5_ui/webui/static/app.css:1385` H-R.3: `.editor__head padding-bottom` von `calc(var(--space) * 1.5)` (12 px) auf `calc(var(--space) * 5)` (40 px) — Editor-Head-Unterkante wandert von y=198,80 auf y=226,80 (1440 px), .list__head-Unterkante bei y=225,94 → **diff_bottom 0,86 px ≤ 2 px Toleranz** (H-R.3-A Abnahme, V142-CDP-Probe pre-fix 27,14 / post-fix 0,86 px). H-R.4/H-R.5: V143 misst **0 Rechteck-Schnittmenge** zwischen .list/.detail__graph/.rail bei 1024×768 in beiden Modi — kein Bug, nur Wächter; V144 misst **16/16 Knöpfe `reachable: true`** (Archivieren/Speichern/×, 10 Format-Hilfen, Vorschau-Toggle, Bild-Insert, Anhängen + Input), keiner offscreen — kein Bug, nur Markup-Wächter. `phase5_ui/tests/test_static_routes.py` drei neue Tests: `test_editor_head_padding_bottom_aligns_with_list_head` (Klammern-Balance-Parser für `calc(var(--space) * N)`, fordert Multiplikator ≥ 4), `test_1024_no_overlap_in_css` (1024er-Media-Query hat `grid-template-rows: 1fr 1fr` + `.rail { grid-row: 1 / span 2 }` + `.detail { grid-column: 2 }`), `test_1024_editor_buttons_present` (Markup-Check für 6 Knopf-IDs + 9 data-md-Format-Hilfen + Titel-Input). `phase8_6_ui_polish/scripts/p86_block_h_r_part2_self_check.py` neu (~290 Z., Playwright + CDP-Probe + 5 Screenshots + TOTP-Window-Retry-Login). `pytest` 988 → **991** in 260 s, `ui_budget` 5/5 (**143,7 KB**, app.css 24,7 → 24,8 KB gzip), Tabu-Diff §0.3 leer, kein `pkill -f`, kein `systemctl`, sharefyx-mcp PID 991 nur gelesen. 5 Selbst-Screenshots `docs/screenshots/p86_block_h_r_{01..05}_*.png` (100/99/132/76/91 KB): bei 1440 ist die YAML-Kopfzeile bündig zur .list__head-Unterkante, bei 1024 sind Liste oben + Karte unten sauber gestapelt, Editor-Knöpfe alle im unteren Slot sichtbar. CDP-Proben `phase8_6_ui_polish/probes/v142_v143_v144_{pre,post}_fix.json` (~9 KB je). `screenshots_latest/`-Symlinks Block-H-R-Teil-1 → Block-H-R-Teil-2 (P8.6-AK blockweise, jetzt 5 Symlinks statt 3 — 03 zeigt jetzt den Editor mit Bündigkeit, 04+05 sind neu für 1024er). **Nächster Schritt: Block J** (P8.6-AJ, datierte Tabu-Ausnahme `phase4_auth/authserver/{crypto.py,store.py}` — `crypto.new_public_id()` mit Rejection-Sampling gegen führendes `-` + zwei Aufrufe in `store.py:294/393` + `authctl.py:199` help-Text; engere Tabu-Probe: `git diff --stat -- phase4_auth/authserver` muss genau zwei Dateien zeigen, `store.py` genau 2 Zeilen — jede Abweichung ist Abbruchgrund). Reihenfolge-Empfehlung P8.6-AH: G → G-R ✅ → H ✅ → **H-R-1 ✅** → **H-R-2 ✅** → J → Gate.) | 2026-09-14 (**P8.6 Block H-R Teil 1 erledigt ✅ — H-R.1 OLED-BLACK für die drei Slots + H-R.2 account-nav-Akzent-Farbe; H-R.3/.4/.5 ⬜ als Folgeblock** — atomarer Block, ein Commit. H1 P8.6-AE/N.9 (Befund 7b): `.rail__account` trägt wieder Einstellungen **und** Abmelden (Reihenfolge Einstellungen → Abmelden, Abmelden äußerster Knopf — Umkehr von Block C C1/N3-Lesart b); `.rail__action--account`-Regel ersatzlos weg (V137 geklärt); `.rail__account` ist `flex-direction: column` als Normalfall (die frühere Sonderregel in der wegoptimierten 1280-px-Media-Query war ein Geist). H2 (Befund 2): `.account-nav` als Flex-Container mit linker Akzentkante `2px solid var(--line-strong)` + Chevron-Icon `#i-chevron-right` rechts via `margin-left: auto` (gleiche Mechanik wie `.tree__count` aus Block C C5) — kein Rückfall in `.btn` (B3-Kategorie „Navigation" trägt); V133 erledigt. **Wächter:** `test_rail_order_settings_before_tree_logout_last` umbenannt + umgekehrt zu `test_rail_order_settings_and_logout_at_the_end` (P8.6-I-Mechanik), Docstring trägt beide Richtungen (2026-09-09 N3-Lesart b → 2026-09-13 N.9); `test_app_html_has_a_live_manage_spaces_entry`-Regex an nested `<svg>` angepasst (kein semantischer Drift). `pytest` 981 unverändert (1 Test umbenannt, 1 angepasst, 0 neu), `ui_budget` 5/5 (**143,1 KB**, app.css 24,0 → 24,2 KB gzip), Tabu-Diff §0.3 leer, kein `pkill -f`, kein `systemctl`, sharefyx-mcp PID 991 nur gelesen. **Drei Selbst-Screenshots** `docs/screenshots/p86_block_h_{01..03}_*.png` (111/110/141 KB). `screenshots_latest/`-Symlinks Block-G → Block-H (P8.6-AK blockweise — waren seit Block G nicht nachgezogen worden). **Nächster Schritt: Block J** (der `pytest`-Flake, P8.6-AJ, datierte Tabu-Ausnahme für `phase4_auth/authserver/{crypto.py,store.py}` — neue Funktion `new_public_id()` + zwei Aufrufe, `authctl.py:199` mit `help`-Text für Altbestand). Reihenfolge-Empfehlung P8.6-AH: G → G-R ✅ → H ✅ → J → Gate, jetzt mit H abgeschlossen.) | 2026-09-14 (**P8.6 Block G-R erledigt: Layout-Revision nach Sichtung, vier Befunde in einem Schritt behoben ✅** — atomarer Block, ein eigener Commit (Nikinger-Entscheidung 2026-09-14: „Nein, bitte als G-R anhängen", kein Force-Push auf `081c432`). G-R.1 **Breakpoints**: `@media (max-width: 1280px)` ersetzt durch `@media (max-width: 1200px)` (Nikinger-Vorgabe: Rail bleibt 240 px, NICHT auf 64 px kollabieren — „Navigationszeile kracht zusammen" gelöst); Liste 480 → 380 px; `display: none`-Regeln für Rail-Labels/Brand/Tree-Group entfallen ersatzlos. `@media (max-width: 1024px)` ersetzt durch Stapel-Logik: `grid-template-columns: 240px 1fr` + `grid-template-rows: 1fr 1fr` + `.rail { grid-row: 1 / span 2 }` + `.detail { grid-column: 2; grid-row: 2 }` — Nikinger-Vorgabe: „Übersicht zusammenschieben und nav bar weiterhin vollständig zeigen", nicht Karte wegblenden. data-view-Switching-Logik aus Block G ersatzlos raus. G-R.2 **Map-Leerraum + Layer-Tone-Vereinheitlichung** (Befund 1-Fortsetzung): `.detail { background: var(--bg) }` neu — vorher erbt von body (`--bg-void = #000`), drei sichtbare Töne für „Spalten-Hintergrund" waren `--bg` in `.list`, `--bg-void` in `.detail`, `--surface` in der Karte. Nach G-R.2: `.list` und `.detail` haben denselben `--bg`-Ton, der schwarze Ring rund um die Karte (Folge von `.detail__graph`-Padding) verschwindet. `.detail__graph { padding: calc(var(--space) * 2) calc(var(--space) * 4) }` — oben/unten 16 px statt 32 px. G-R.3 **Editor-Header sticky + YAML bündig** (Befund 6/7-Fortsetzung): `.editor__head { position: sticky; top: 0; background: var(--surface-raised); border-bottom: 1px solid var(--line); z-index: 1; padding: calc(var(--space) * 0.5) calc(var(--space) * 3) calc(var(--space) * 1.5) }` — padding-top von 12 px auf 4 px reduziert, die YAML-Kopfzeile rückt nach oben und schließt bündig mit der Suchzeilen-Unterkante im Listen-Slot ab. Sticky + `--surface-raised` als Pendant zu `.list__head` (Step 7b-Verhalten). `.panel__head { padding: 11px calc(var(--space) * 3) }` — vertikales Padding von 6 px auf 11 px erhöht, Item-Row-Höhe (~41 px) ≈ Panel-Header-Höhe (~41 px) für „buendig"-Optik. G-R.4 **Wächter**: `test_shell_grid_is_240_480_1fr` aus Block G umgestellt (drei Anker statt zwei, neue 1200- und 1024-Werte), vier neue Tests `test_1200_breakpoint_keeps_rail_at_240`, `test_1024_breakpoint_stacks_list_over_detail`, `test_detail_uses_the_column_background_not_void`, `test_editor_head_is_sticky_with_the_list_head_background` + `test_panel_head_height_matches_a_list_row`. **Mini-Plan** `docs/concepts/phase8_6_ui_polish_block_g_r_plan.md` neu (~12 KB). **Echte Fund beim Bau:** f-string-Regex-Match auf `css[m.start():m.end()]` (in `test_overview_grid_and_its_media_query_are_gone`) hatte eine `]`-Klammer zu wenig — der `.match()`-Aufruf schlug fehl, das Test-Module kompilierte nicht. Behoben im selben Commit. **Doku-Hygiene:** `test_1024_breakpoint_stacks_list_over_detail` musste mit einem Wort-Grenzen-Lookahead `\.detail(?![a-zA-Z_-])\s*\{` ausgestattet werden (compound `.detail__back` wird vom Bare-Selector nicht mitgezogen), und die Kommentar-Beispieltexte in der 1024-px-Media-Query (`shell[data-view="list"] .detail { display: none }`) wurden aus dem Kommentar entfernt (Regex matchte sonst die Kommentar-Buchstaben). Modul-Status Z13 ⬜→✅ (Reihenfolge-Anpassung: Block G-R ist zwischen Block G und Block H eingeschoben — G → G-R ✅ → H → J → Gate). `pytest` 976 → **981** in 248 s (Baseline 970 + 4 G + 2 F + 5 G-R), `ui_budget` 5/5 (**143 KB**, +1,6 KB roh; app.css 73.593 → 77.301 B), Tabu-Diff §0.3 trivial leer, kein `pkill -f`, kein `systemctl`, sharefyx-mcp **PID 991** nur gelesen. **Sechs Selbst-Screenshots** `p86_block_g_r_{01..06}_*.png` (111/134/110/131/93/128 KB): 1440-Übersicht (Layer-Tone vereinheitlicht), 1440-Editor-offen (sticky-Header + YAML bündig), 1200-Übersicht (Rail 240 mit Labels), 1200-Editor-offen, 1024-Übersicht (Liste oben + Karte darunter GESTAPELT), 1024-Editor-offen (Editor ersetzt Karte im unteren Slot). **Nächster Schritt: Block H** (Rail + Konto-Dialog, Befunde 7b + 2 — Nikinger-Vorgabe vom 2026-09-14: nach G-R ist die Reihenfolge H → J → Gate, nicht mehr J dazwischen)
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

**[2026-09-19, Nachtrag — Step-Z-Commit gepusht, drei Nikinger-Entscheidungen zu P9
aufgenommen.]** `1e61429` steht auf `origin/main` (`860ed72..1e61429`), Arbeitsbaum sauber.
**Die drei Entscheidungen, alle im `PHASE8_6_CLOSEOUT_HANDOVER.md` §4 verankert:**
**(1) Die echte Domain wird einer der ersten P9-Schritte** — raus aus der „P9+"-Warteschleife
(§4.2). Begründung für „früh": eine Adressänderung zieht den Claude-Connector in **beiden**
Konten nach sich; wer sie ans Ende legt, macht den Schnitt zweimal.
**(2) Der Tailscaled-Watchdog wird gebaut** (§4.3). Von den drei vorgemerkten Ansätzen deckt
nachweislich **nur einer** den Vorfall vom 2026-09-15 — ein `OnFailure=`-Hook feuert dort gar
nicht, weil `tailscaled` durchlief und nur die Control-Plane klemmte; nötig ist die zyklisch
prüfende Unit. Die Tabelle dazu nimmt der Planungssession die Messarbeit ab, nicht die Wahl.
**(3) Neu und nicht aus P8.6 stammend: die ungenutzte RTX 3060 (12 GB) im Proxmox-Verbund
bekommt einen eigenen internen CUDA-Dienst** (§4.8), der die CPU-only-Vision-Strecke ablöst;
Form „nach Empfehlung", Ausarbeitung in der Planungssession. **Empfehlung: eigener
LXC-Container auf dem 3060-Host mit Ollama, erreichbar als interner HTTP-Dienst auf der
Proxmox-Bridge — nicht in die sharefyx-VM.** Der Grund ist das Bauprinzip selbst: „der Server
ist dumm" heißt kein LLM im Serverpfad, und diese Grenze ist nachprüfbar, solange das Modell in
einer eigenen Kiste steht — steht es in der Produktions-VM, muss jeder künftige Leser dem Satz
glauben. Die Client-Seite ist dafür schon gebaut: `mcp_local_vision_server.py:195` liest
`LOCAL_VISION_ENDPOINT`, `vision_ollama.py:44` hat `--endpoint` — der Umzug ist **eine
Umgebungsvariable, kein Code**. Hard Rule 6 bleibt unberührt (interne Bindung, kein Funnel).
**Zwei Präzisierungen, die sonst in die Planung einwandern:** ersetzt wird **nicht** das Plugin
(das ist seit 2026-09-11 gemessen zurückgebaut), sondern das **CPU-only-Ollama-Backend** auf der
sharefyx-VM; und `mcp_local_vision_server.py` hat zwei Ungereimtheiten, die genau dann beißen,
wenn der Endpoint nicht mehr `127.0.0.1` ist — `:223` loggt beim Start `DEFAULT_ENDPOINT` statt
des aufgelösten Endpoints, und das `--endpoint`-Flag (`:274`) wirkt nur auf `--check`, nie auf
`serve()`. **Praktische Folge der 12 GB:** `qwen3-vl:8b` (Q4_K_M, 6,1 GB) passt vollständig in
den VRAM, der heutige Cold-Start von 46–180 s fällt auf Sekunden — erst das macht die in §4.6
geparkte Sichtprüfungs-Option (A) benutzbar, die drei Revisionsrunden dieser Phase verursacht
hat. ROADMAP-P9-Zeile und Handover-Frontmatter im selben Commit nachgezogen.


**[2026-09-19, Phase 8.6 abgeschlossen ✅ — Step Z durchgeführt, `v3.0.2` ist live, die Phase
steht auf ✅ — Claude Code — reine Doku-Session, kein Produktcode-Touch.** Abnahmematrix beider
Pläne vollständig ausgewertet: **45 ✅ · 5 ⚠️ · 0 ⬜ · 4 ersetzt** von 54 Zeilen, jede mit Beleg.
`[VERIFY]`-Bilanz V97/V103–V144: **37 geschlossen · 2 offen · 2 nachträglich bilanziert**.
Der **kanonische Closeout steht in `docs/concepts/phase8_6_ui_polish_plan2.md` §9** (Lock
P8.6-W); Plan 1 §9 trägt jetzt die eine erlaubte Zeiger-Zeile. `PHASE8_6_CLOSEOUT_HANDOVER.md`
ist von Partial- auf **Abschluss**-Handover P8.6 → P9 umgeschrieben (die beiden zitierten
Abschnitte §4.5/§4.6 sind im Kopf gesichert, die alte Fassung liegt in `373a431`);
`phase8_6_ui_polish_uebersicht.svg` neu gezeichnet, Badge von **PARTIAL CLOSEOUT** auf die
Abnahmezahl, zwei Bahnen mit der roten Bruchstelle dazwischen — gerendert und **angesehen**,
nicht ungesehen gemeldet (erster Durchgang hatte sechs Textüberläufe und zwei von `<rect>`
verdeckte Pfeile). **Gemessen, nicht übernommen:** `pytest` **995 passed in 117,6 s**,
`ui_budget` 5/5 (144,7 KB von 250 KB), **Bereichs**-Tabu-Diff `440e462^..HEAD` leer für die
sechs harten Pfade — bewusst als Bereichs-Diff und nicht als Working-Tree-Diff, der bei sauberem
Baum vakuös leer meldet und über die Phase nichts beweist; die enge `authserver`-Probe zeigt
exakt die angekündigte P8.6-AJ-Ausnahme (2 Dateien, `store.py` 2/2 Zeilen). **Vier Funde in
Step Z selbst:** `docs/INDEX.md` war auf **45.870 B** gewachsen (Kriterium ≤ 38 KB, **dritter**
Verstoß der Phase — gestrafft, aber die Ursache bleibt P9-Arbeit: die `updated:`-Kette braucht
eine Rotation, die Handarbeit trägt nicht mehr) · **P8.6-18/-19 sind zusätzlich zu -21/-22
ersetzt** (die Rail-Umkehr N.9 hat sie still umgedreht, Plan 2 §8.1 nannte nur die ersten zwei)
· **V136 wurde nie beantwortet** — durchgerutscht, nicht entschieden · **V140/V141 waren
materiell beantwortet, aber nie bilanziert**. **Zwei Abnahmezeilen bewusst nicht grün gemeldet:**
P8.6-15 (die geforderte Zuordnungstabelle im Phase-Head wurde nie geschrieben — der Sweep lief,
sein Ergebnis hält ein Test) und P8.6-44 (`--panel-meta*` tragen keinen `--warn`-Bezug mehr,
aber `app.css:770`/`:1306` behalten `rgba(229,169,60,.10)` an **echten** Warn-Elementen; das
Kriterium forderte `grep = 0` und war breiter als sein Zweck). **Das Nikinger-Feedback vom
2026-09-19** liegt im Handover §4.1, bewusst in drei Klassen statt als Feature-Liste: zwei Bugs
mit erstem read-only-Messbefund (`bindFolderDropTarget()` hat genau eine Aufrufstelle,
`tree.js:205` — es gibt ein Drop-Ziel *in* einen Ordner, aber keines zurück auf die
Space-Wurzel · der globale ESC-Handler `app.js:204` prüft kein `document.fullscreenElement`,
deshalb löst ein Tastendruck auf dem Mac zwei Aktionen aus), **ein Rechte-Thema** (Verschieben in
fremde Spaces ist Hard Rule 4 / `.share.yml`, Einstieg `phase6_shares_plan.md`, nicht `app.css`)
und fünf gewöhnliche Feature-Wünsche. **Eine Falle unterwegs, sofort zurückgerollt:** der erste
Patch-Versuch am Phase-Head schnitt mit `str.index("## Nächste Session")` — der Treffer lag in
der `updated:`-Frontmatter-Kette, nicht auf der Überschrift, und hätte 66 KB entfernt;
`git checkout --` hat es zurückgeholt, der zweite Versuch schneidet nur mit Zeilenumbruch-Ankern
und prüft vorher die Trefferzahl. **Rotation per `scripts/rotate_session_block.sh`** (Gate-Block
2026-09-18, 160 Z. / 13.043 B, verbatim ins Archiv, alle vier Gegenproben grün); Head
121.842 → 108.799 B. ROADMAP-P8.6-Zeile neu geschrieben und auf ✅, P9-Zeile um das Feedback
ergänzt, `docs/INDEX.md` gestrafft und nachgezogen, `screenshots_latest/` auf die Gate-Bilder
umgehängt (P8.6-AK) — alles im selben Commit. **Nächster Schritt: P9-Planungssession**, Einstieg
`docs/concepts/PHASE8_6_CLOSEOUT_HANDOVER.md`. Dieses Phasenverzeichnis ist ab jetzt Archiv.


**[2026-09-18, P8.6 Gate abgeschlossen — `v3.0.2` ist live ✅ — Claude Code — GA1–GA4 alle
erledigt, nur Step Z (Closeout) offen, Phase bleibt 🔄.** GA1 (Wegwerf-Instanz Port 18773) +
GA2 (`p86_polish_smoke.py` neu, 14 Stationen aus Plan 2 §7.2, 18/18 grün nach drei
Korrekturrunden gegen den aktuellen Code, nicht gegen den teils veralteten Plan-Wortlaut) +
GA3 (Nikinger-Sichtprüfung der 18 Screenshots — `#back-button`/`.detail__back` als toter Code
gefunden, `app.css:1367` fest `display: none` ohne Override; Nikinger-Entscheidung: unkritisch,
`#close-button`+ESC decken „zurück" bereits vollständig ab, kein Fix nötig) + GA4 (Badge
`app.html` `v3.0.1`→`v3.0.2`, `docs/UPDATE_LOG.md`-Eintrag, Deploy, Health-Gate). **Echter
Deploy-Blocker unterwegs gefunden und behoben:** `deploy.sh`s erster Lauf scheiterte am
`git clone`-Schritt (`Invalid path '.../.git': Permission denied`) — Eigentümer, Gruppe,
Mountpunkt und Plattenplatz waren alle in Ordnung, auch ein manueller Reproduktionsversuch im
Agenten-Kontext gelang zweimal. Ursache war ein `umask 0177` in der Nikinger-Shell: `git clone`
legt neue Verzeichnisse mit `0777 & ~umask` an, bei `0177` ergibt das `0600` — kein Execute-Bit,
auch nicht für den Eigentümer, macht das frisch angelegte Verzeichnis für niemanden mehr
traversierbar. Eine Klasse Fehler, die `ls -la` nicht zeigt, solange man nicht das neu
angelegte Kind-Verzeichnis selbst prüft. Fix: `phase5_ui/scripts/deploy.sh` setzt jetzt
`umask 022` explizit, statt die der aufrufenden Shell zu erben; Regressionstest
`test_deploy_succeeds_under_a_restrictive_ambient_umask` neu (setzt `umask 0177` im
Testprozess, reproduziert ohne den Fix denselben Fehlertext, grün mit ihm — gegengeprüft per
temporärem Revert). `pytest` 994 → **995**. **Zweiter Deploy-Versuch erfolgreich:** Release
`/opt/sharefyx/releases/20260918T183907.597248Z`, SHA `1ad2665`, `health_gate.sh
--expected-version=v3.0.2 --require-todays-update-log --expected-sha=1ad2665` **9/9 grün**, echter
Lauf mit JSON-Ausgabe im Commit (Plan 2 §7.4 — genau die Stelle, an der Plan 1 vorher nur
behauptet hatte, ohne dass es stimmte). Hard Rule 9 durchgehend eingehalten: `systemctl` lief
ausschließlich über den Nikinger (`sudo`-Prompt live bestätigt, V134 geschlossen), der Agent hat
an keiner Stelle selbst `systemctl` aufgerufen. **Phase 8.6 bleibt 🔄, nicht ✅** — der Gate ist
geschlossen, aber Step Z (Abnahmematrix vollständig, `[VERIFY]`-Bilanz inkl. dem noch offenen
V118, Plan 2 §9 als kanonischer Closeout, Übersichtsgrafik, finale Rotation) steht noch aus,
eigene Session. Details: `phase8_6_ui_polish/CLAUDE.md` Session-Block 2026-09-18.

**[2026-09-17, P8.6 Block J erledigt: `pytest`-Flake behoben (P8.6-AJ, datierte Tabu-Ausnahme) ✅ — Claude Code — eigener Commit, getrennt von jedem UI-Commit.** **Vorab-Korrektur:** die drei Commits zwischen dem letzten hier eingetragenen Stand (Block H) und diesem — Block H-R-3 (drei Locks H-R.6/.7/.8), der Rail-Exklusivitäts-Nachtrag und jetzt Block J — hatten diesen Current-state-Absatz nie nachgezogen, nur den Phase-Head; dieser Eintrag holt den Sprung nach, ohne die Zwischenschritte einzeln auszubuchstabieren (volle Herleitung: `phase8_6_ui_polish/CLAUDE.md` Session-Block 2026-09-17). **Block J selbst:** `phase4_auth/authserver/crypto.py` bekommt `new_public_id(nbytes: int = 16)` — Rejection-Sampling (`while value.startswith("-")`) statt Umkodierung, damit Alphabet/Länge zu `new_secret` identisch bleiben; behebt den seit 2026-08-20 als „reihenfolgeabhängiger Flake" fehldiagnostizierten Bug in `test_authctl.py::test_revoke_kills_the_family` — die echte Ursache (gemessen 2026-09-13, P8.6 Plan 2 §1.3): `secrets.token_urlsafe(16)` liefert in **1,569 %** der Ziehungen ein führendes `-`, `argparse` liest das als Optionsflag statt als Wert. `store.py:294` (`create_client` → `client_id`) und `store.py:393` (`create_family` → `family_id`) auf `crypto.new_public_id(16)` umgestellt — genau die zwei Stellen, deren Wert je auf einer Kommandozeile landet (`authctl revoke --family-id <ID>`); die zehn übrigen `new_secret`-Aufrufstellen bleiben unverändert, sie erzeugen opake Geheimnisse, die nie eine Kommandozeile sehen. `phase4_auth/scripts/authctl.py`s `--family-id`-Argument bekommt einen `help`-Text für den Altbestand (IDs von vor dem Fix können noch mit `-` beginnen — Gleichheitsform `--family-id=-abc`). **Drei Tests:** `test_revoke_kills_the_family` auf `--family-id=` umgestellt (Verteidigung in der Tiefe), neu `test_revoke_accepts_a_family_id_starting_with_a_dash` (Altbestands-Pfad) und `test_new_public_id_never_starts_with_a_dash` (5.000 Ziehungen, plus Länge/Alphabet-Gleichheit zu `new_secret`). **Enge Tabu-Probe (P8.6-AJ/§6.4) exakt erfüllt:** `git diff --stat -- phase4_auth/authserver` zeigt **genau zwei Dateien** (`crypto.py`, `store.py`), `store.py` **genau 2 geänderte Zeilen**; die breitere Tabu-Probe (§0.3) blieb ebenfalls leer — keine neunte P1-Contract-Öffnung. **Selbstprüfung:** `pytest -q` **994 passed in 111,5 s** (992 + 2 netto), `phase4_auth/tests/{test_crypto,test_authctl}.py` isoliert 26/26 grün, kein `ui_budget`-Touch nötig (kein `phase5_ui/webui/static/**`-Berührung), kein `pkill -f`, kein `systemctl`, sharefyx-mcp **PID 991** nicht angefasst. **Doku-Hygiene:** Phase-Head Modul-Status Zeile 15 ⬜→✅ + Session-Block-Nachtrag + Frontmatter-`updated:`-Kettenkorrektur, `docs/INDEX.md`-Phase-8.6-Zeilen (Kopf + Plan-Karten) nachgezogen, `phase4_auth/CLAUDE.md`s Flake-Notiz von „bekannt, nicht untersucht" auf „behoben, Ursache + Fix verlinkt" korrigiert, dieser Current-State-Absatz — alles im selben Commit. **Nächster Schritt: Gate** (Wegwerf-Ritt + `p86_polish_smoke.py`, 14 Stationen aus Plan 2 §7.2, Nikinger-Sichtprüfung mit fünf offenen Entscheidungen §7.3, danach Deploy `v3.0.2`) — Reihenfolge P8.6-AH ist damit **G → G-R → H → H-R (alle Teile) → J alle ✅, nur noch Gate → Z offen.**

**[2026-09-14, P8.6 Block H erledigt: Rail + Konto-Dialog, zwei Befunde in einem Schritt behoben ✅ — opencode/M3 — atomarer Block, ein Commit.** `phase5_ui/webui/static/app.html:19-53` H1 P8.6-AE/N.9: DOM-Reihenfolge im `.rail` ist wieder `.rail__brand` → `#home-button` → `#rail-tree` → **`.rail__account` mit zwei Knöpfen** (`#account-button` zuerst, `#logout-button` zuletzt). Umkehr von Block C C1 (N3-Lesart b hatte `#account-button` oben unter `#home-button` gesetzt) — Nikinger-Vorgabe 2026-09-13: „Abmelden bleibt weiterhin der äußerste Knopf." Vorzeichen aus Block C erhalten: „Einstellungen" statt „Konto" (Zahnrad-Icon), `#logout-button` weiter mit `class="action--caution"` (B4-Farbe aus Konvention v3). `phase5_ui/webui/static/app.css:634-657` `.rail__account` ist jetzt `flex-direction: column` als **Normalfall**, nicht als Sonderregel in einer Media-Query — die Sonderregel `@media (max-width:1280px) {.rail__account {flex-direction: column}}` aus dem Plan §5.1 war bereits von Block G-R gelöscht (G-R.1 hat die 1280-px-Query ersatzlos entfernt); die Spalten-Anordnung ist damit der einzige Pfad in allen Breakpoints. `.rail__action--account`-Regel ersatzlos weg (V137 geklärt — sie war Rest der Oben-Platzierung mit `margin: 0 var(--space) var(--space); width: auto;`, nach der Rückkehr in `.rail__account` reicht die Basis-Regel `.rail__action`). `app.css:670-708` H2 Befund 2: `.account-nav` jetzt `display: flex; align-items: center; gap: var(--space)` (statt `display: block; text-align: left`) + `border-left: 2px solid var(--line-strong)` als sichtbare Akzentkante; B3-Hover (`background: var(--select-fill-quiet)` + `outline`) bleibt unverändert; `.account-nav .icon { margin-left: auto; }` schiebt das Chevron-Icon an den rechten Rand (gleiche Mechanik wie `.tree__count` aus Block C C5). `app.html:464-468` beide `.account-nav`-Buttons tragen jetzt `<svg class="icon"><use href="#i-chevron-right"></use></svg>` als letztes Kind (Symbol existierte schon, `tree.js:229` nutzt es für `tree__twist`, kein neuer Asset). **Kein** Rückfall in `.btn` (B3-Kategorie „Navigation" trägt — die Knöpfe öffnen etwas, ändern nichts; der fehlende Afford war das Problem, nicht die Kategorie). V133 erledigt: `elementFromPoint` liefert jetzt das Button-Element statt `null` (die Knöpfe fehlten nie — sie hatten keinen sichtbaren Afford). **Wächter:** `test_rail_order_settings_before_tree_logout_last` umbenannt + umgekehrt zu `test_rail_order_settings_and_logout_at_the_end` (P8.6-I-Mechanik, „der Testname wird sonst zur Lüge"), Assertions `#home-button < #rail-tree < #account-button < #logout-button` plus zusätzliche Assertion `#logout-button == html.rfind('id="logout-button"')` als harter „Abmelden ist letzter"-Wächter, Docstring trägt **beide** Richtungen mit Datum (2026-09-09 N3-Lesart b → 2026-09-13 N.9); `test_app_html_has_a_live_manage_spaces_entry`-Regex `[^<]*` durch `.*?` mit `re.DOTALL` ersetzt (nested `<svg>`), separate Label-Assertion bleibt. **Drei echte Funde beim Bau (alle im selben Commit behoben):** (1) `test_shell_grid_is_240_480_1fr` (G-R-Wächter) schlug rot an, weil mein erster `.rail__account`-Kommentar das Literale `@media (max-width:1280px)` enthielt — der Wächter matchte den Kommentar-Text. Behoben durch allgemeinere Formulierung („die schmale-Query ist weg"). (2) `test_app_html_has_a_live_manage_spaces_entry` schlug nach dem H2-Markup-Touch rot an (`AssertionError: Menüpunkt 'Spaces verwalten' fehlt`), alte Regex mochte nested `<svg>` nicht — `.*?` mit `re.DOTALL` + separate Label-Assertion. (3) `scripts/rotate_session_block.sh phase8_6_ui_polish` lief nur, nachdem ich den neuen Block-H-Sub-Block an den Head angehängt hatte (Skript-Logik Z. 60-74: genau ein Block → exit 2, ≥2 Blöcke → rotieren); der G-R-Sub-Block wanderte verbatim ins Archiv, der Head trägt jetzt genau einen Block H. **Selbstprüfung §0.5:** `pytest -q` **981 passed in 108 s** (V107-Baseline 981 unverändert — Block H ändert keine Test-Zahl, 1 Test umbenannt + 1 minimal angepasst), `node --check` auf alle 13 JS-Dateien ✅ (keine JS-Änderungen), `ui_budget.py` **5/5 im Korridor**, 143,1 KB gzip, app.css jetzt **24,2 KB** gzip (vs. G-R 24,0 KB, +0,2 KB für die `.rail__account`-Spalten-Anordnung + `.account-nav`-Flex-Container + Chevron-Icon-Rule + die ausführlichen Block-H-Kommentare; app.css bleibt deutlich unter 250 KB), Tabu-Diff §0.3 **leer** (nur `phase5_ui/webui/static/{app.html,app.css}` und `phase5_ui/tests/test_static_routes.py` berührt). Kein `pkill -f`, kein `systemctl`, sharefyx-mcp **PID 991** nur gelesen. **Drei Selbst-Screenshots** `docs/screenshots/p86_block_h_{01..03}_*.png` (111/110/141 KB): Rail bei 1440 mit beiden Knöpfen unten, Rail bei 1200 mit gleicher Anordnung (kein Kollaps), Konto-Dialog offen mit Akzentkante + Chevron auf beiden Knöpfen. **Doku-Hygiene:** Modul-Status Z13 ⬜→✅ (Reihenfolge jetzt G → G-R ✅ → **H ✅** → J → Gate), dieser Session-Block, Rotation per `scripts/rotate_session_block.sh phase8_6_ui_polish` (G-R-Sub-Block 235 Z./18.073 B verbatim ins Archiv), Frontmatter `updated:` im Phase-Head (H-Eintrag voran), `docs/INDEX.md`-Phase-8.6-Karte nachgezogen, `screenshots_latest/`-Symlinks Block-G → Block-H (P8.6-AK blockweise — diese Symlinks waren seit Block G nicht aktualisiert worden, jetzt nachgeholt), dieser Current-State-Absatz — alles im selben Commit. **Nächster Schritt: Block J** (der `pytest`-Flake, P8.6-AJ, datierte Tabu-Ausnahme für `phase4_auth/authserver/{crypto.py,store.py}` — neue Funktion `new_public_id()` mit Rejection-Sampling gegen führendes `-` + zwei Aufrufe in `store.py:294/393`, `authctl.py:199` bekommt `help`-Text für den Altbestand). Plan §6.4 engere Tabu-Probe: `git diff --stat -- phase4_auth/authserver` zeigt **genau zwei Dateien**, `store.py` genau 2 Zeilen — jede Abweichung ist Abbruchgrund.

**[2026-09-14, P8.6 Block G erledigt: Layout-Umbau, fünf Befunde in einem Schritt behoben ✅ — opencode/M3 — atomarer Block, ein Commit.** `.shell` `240px 380px 1fr` → **`240px 480px 1fr`** per **P8.6-O2-Auslösung** (N.7 entschieden — gemessen brauchen Space-Zeilen ~433 px, 380 reichte nicht); DOM-Umzug `#list-overview` in `section.list` + `#detail-graph` (die Karte) in `section.detail` allein. **Befund 9b-Ursache weg:** `.overview`-Grid + 1280-px-Media-Query ersatzlos gelöscht. **V112-Wächter nach Umzug:** `.detail__graph { display: flex; flex-direction: column; flex: 1; min-height: 0; padding: ... }` + `.detail__graph .overview__graph { flex: 1; min-height: 0 }`. `state.overview: true` als neues Feld (P8.6-AA), `#home-button` setzt es **vor** `closeEditor()` (sonst rendert clearDetail mit altem Wert), mit Revert im else-Zweig (Cancel) und catch-Sicherheitsnetz. **Befund 6 behoben:** `.overview__space-open` ist jetzt der volle Zeilen-Button (width: 100%, padding statt LI), umschließt Glyph + Name + Chip-Counter-Chips als `<span role="button" tabindex="0">` (verschachtelte `<button>` wären ungültiges HTML). Hover-Regel wanderte vom LI auf den Button (P8.6-P wiederhergestellt). `renderListSlot()` neu exportiert (P8.6-AA); **alle Render-Aufrufer** (`loadItems`/`loadOverview`/`toggleSelected`/`clearSelection`/`clearDetail`/`loadEditorFromItem`/`selectItem`) umgestellt (V128 vollständig). **Editor ersetzt die Karte, ESC bringt sie zurück** (N.8) — visuell in Screenshots 03/04 bestätigt. **Vier neue statische Tests** in `test_static_routes.py` (G8): `test_shell_grid_is_240_480_1fr` (P8.6-X), `test_overview_lives_in_the_list_slot` (P8.6-Y), `test_detail_graph_has_a_definite_height_chain` (V112-Wächter nach Umzug), `test_overview_grid_and_its_media_query_are_gone` (9b-Regressionswächter); `test_overview_graph_has_no_max_width_or_min_height` an Compound-Selector angepasst (`^\.overview__graph\s*\{` mit `re.MULTILINE`, sonst hätte die neue `.detail__graph .overview__graph`-Regel ihn fälschlich gebrochen). **Echter Fund beim Self-Check (im selben Commit behoben):** `editor.js` rief `renderListSlot()` ohne Import → `[ERR] renderListSlot is not defined` in der Browser-Konsole, Editor öffnete sich nicht, erste Screenshot-Aufnahme zeigte es. Behoben durch Import-Ergänzung in editor.js Z. 9. **Sechs Selbst-Screenshots** `p86_block_g_{01..06}_*.png` (110-115 KB / 84 / 69 KB): 1440-Übersicht, 1440-Space-geöffnet, 1440-Editor-offen, 1440-Editor-nach-ESC, 1200-Übersicht, 1024-Übersicht. **Selbstprüfung §0.5:** `pytest` 970 → **976** in 107,04 s (Baseline 970 + 4 neue G-Tests + 2 F-Tests), `ui_budget` 5/5 im Korridor (**141 KB statt 130 KB** — Plan §4.9-Erwartung „app.css kleiner" **nicht erfüllt**, dokumentierte Abweichung: die `.detail__graph`-Höhenkette und ausführliche G7-Kommentare überwiegen den Grid-Lösch-Effekt), Tabu-Diff §0.3 trivial leer, kein `pkill -f`, kein `systemctl`, sharefyx-mcp PID 991 nur gelesen. **Doku-Hygiene:** Modul-Status Z12 ⬜→✅, Session-Block mit Block-G-Protokoll, Rotation per `scripts/rotate_session_block.sh phase8_6_ui_polish` (Block-F-Sub-Block 64 Z./4.382 B verbatim ins Archiv), docs/INDEX.md Phase-8.6-Karte nachgezogen, ROADMAP-P8.6-Zeile + Frontmatter nachgezogen, dieser Current-State-Absatz. **Nächster Schritt: Block H (Rail + Konto-Dialog, Befunde 7b + 2).** Plan §5: `.rail__account` trägt wieder Einstellungen **und** Abmelden (Abmelden bleibt äußerster Knopf — Umkehr von C1/N3-Lesart b, Nikinger-Entscheidung 2026-09-13 N.9). `.account-nav` bekommt eine Navigations-Anmutung (die zwei Knöpfe fehlten nie, sie sahen nur nach Fließtext aus — Befund 2 war eine Selbsttäuschung der CSS-Form, nicht eine Knopf-Lücke). `test_rail_order_settings_and_logout_at_the_end` wird umbenannt und umgekehrt. Reihenfolge-Empfehlung (P8.6-AH) bleibt F → G → H → J → Gate, jetzt mit G abgeschlossen.**

**[2026-09-14, P8.6 Block F erledigt: Layering konsequent, zwei Wächter scharf ✅ — opencode/M3 — atomarer Block, kein Mess-Overhead.** `phase5_ui/webui/static/app.css` F1-F3: `--panel-meta/--panel-meta-head/--panel-meta-line` entkoppelt (Befund 8, P8.6-AB N.10 — meta jetzt Layer 2 kühl, nicht mehr warm-getönt mit `rgba(229,169,60,.22)`); drei neue Token `--rail-top/--auth-glow/--auth-card-top` für die rohen Flächen-Hex `#0E1116/#131A23/#1A2029` (P8.6-AD); `.editor__append` trug schon `var(--surface) + border-top: var(--line)` (F2 null B-Aufwand, V127: 0). `phase5_ui/tests/test_static_routes.py` F4: **zwei neue Wächter als byte-genaue Regressionssperre** — `test_no_raw_surface_hex_outside_root` (jede `background:`/`gradient(`-Deklaration außerhalb `:root` nutzt Token; EXEMPT_HEX dokumentiert `#fff` QR + 9 Space-Kategorie-Hex) + `test_meta_panel_is_not_tinted_with_the_warning_colour` (prüft gezielt die drei `--panel-meta*`-Tokens, lässt legitime Warn-Themed-Chips mit `var(--warn)` zu). `#fff` in `.qr-frame` mit begründendem Kommentar ("QR-Code braucht echtes Weiß"); 9 Space-Kategorie-Hex in `.rail__glyph--own/--shared/--foreign` bleiben per Plan §3.3 explizit ausgenommen. Zwei Selbst-Screenshots `p86_block_f_{01_vorher_warm_meta,02_nachher_cool_meta}.png` (Vorher per `git stash`-Revert für die Aufnahme, danach pop — der Revert berührte nur app.css lokal, ist im Commit nicht enthalten); Checkkriterium in einem Satz: "das Meta-Panel zeigt eine kühle Layer-2-Fläche (`--surface = #14181D`) statt der warmen `rgba(229,169,60,.22)`-Tönung -- Befund 8 weg". **Selbstprüfung:** `pytest` 970 → **972** in 111,52 s (Baseline 970 + 2 neue Wächter), `ui_budget` 5/5 (130,1 KB, app.css 60.201 → 60.319 B, +118 B), Tabu-Diff §0.3 trivial leer, kein `pkill -f`, kein `systemctl`, sharefyx-mcp PID 991 nur gelesen. **Doku-Hygiene:** Modul-Status Z11 ⬜→✅, Phase-Head-`updated:` mit F-Eintrag ergänzt, SESSIONS_ARCHIVE.md-`updated:` mit Rotations-Eintrag, ROADMAP-P8.6-Zeile + docs/INDEX.md Phase-8.6-Karten nachzuziehen. Rotation per `scripts/rotate_session_block.sh phase8_6_ui_polish`, E2b-Sub-Block (78 Z. / 5.058 B) verbatim ins Archiv, Head 67.798 → 68.956 B. **Naechster Schritt: Block G (Layout-Umbau, Befund 5 + 3/4/6/7a) — löst P8.6-O2 aus, .shell → 240px 480px 1fr, ESC bringt Karte zurück.** Reihenfolge P8.6-AH: F → G → H → J → Gate, jetzt mit F abgeschlossen.**

**[2026-09-13, P8.6 Plan 2 geschrieben — Claude-Code-Planungssession, kein Produktcode-Touch.]** Ergebnis: `docs/concepts/phase8_6_ui_polish_plan2.md` (~69 KB, 📕-Snapshot gegen `main`@`26a7cc9`) — ausfuehrungsreif fuer alle neun UX-Befunde, Bloecke **E/F/G/H/J**, Locks **P8.6-W–P8.6-AL**, Abnahme **P8.6-33–P8.6-54**, `[VERIFY]` **V123–V139**. Die Phase bleibt **🔄 und nicht ausgeliefert**; live ist weiter `6f19a8f` (P8.5). **Sechs Nikinger-Entscheidungen (N.7–N.12):** **(N.7)** `.shell` wird **`240px 480px 1fr`** — die bewusste, vorgelegte und entschiedene Ausloesung von **P8.6-O2** (Messung: Space-Zeilen brauchen ~433 px, 380 reichen nicht). **(N.8)** Editor **ersetzt** die Karte, **ESC bringt sie zurueck** — auch nach Klick auf einen Karten-Knoten; ist Abnahmekriterium, nicht Nebenwirkung. **(N.9)** Befund 7b kehrt **C1 / N3-Lesart b** um (Einstellungen + Abmelden wieder unten, **Abmelden bleibt aeusserster Knopf**) — datierte Umkehr einer beantworteten Frage, keine stille Abweichung. **(N.10)** Layering per **Tiefe statt Farbe**. **(N.11)** Plan 2 ist ein eigenes Dokument; Plan 1 bleibt 📕 unangetastet, der **kanonische Closeout wandert nach Plan 2 §9** (P8.6-W). **(N.12)** Der `pytest`-Flake wird beidseitig gefixt. **Fuenf der neun Befunde haben jetzt eine gemessene Ursache statt einer Vermutung:** Befund 8 — `--panel-meta-line: rgba(229,169,60,.22)` **ist** `--warn: #E5A93C` bei 22 %, byte-genau; Befund 1 — 10 Flaechen-Token in `:root` plus **4 rohe Hex ausserhalb** (`#0E1116`/`#131A23`/`#1A2029`, dazu `#fff` im QR, das bleibt); **Befund 2 ist als Messfrage geschlossen — die Knoepfe fehlen nicht**, `app.html:484-485` rendert beide (sichtbar in `p86_block_b_04_account_dialog.png`), sie lesen sich wegen `background: none; border: none` nur als Fliesstext; Befund 4 — `1fr 40%` meint 40 % des **Detail-Slots**, also 302 px bei 1440 = 21 % der Seite, nicht die in P8.6-K zitierten „~40 % der gesamten Seite"; Befund 6 — **Lock-Abweichung, keine CSS-Wanze**: P8.6-P forderte die ganze Zeile klickbar, C4 baute einen inneren Button. **Befund 9 zerfaellt in zwei:** **9a** laeuft live auf `v3.0.1`, wo Block C gar nicht existiert (Ursache **unbekannt**, Block E misst sie), **9b** ist von Block C eingefuehrt (`overflow: hidden` + `flex: 1` schlaegt `height: auto`). Die Falle, die Block E vermeidet: 9b reparieren und „behoben" melden, waehrend 9a live stehen bleibt. **Neuer Produktionsfehler, beim Messen der Baseline gefunden:** `pytest` ergibt **969 passed + 1 failed**, nicht die dokumentierten 970 — `secrets.token_urlsafe(16)` liefert in **1,569 %** der Faelle ein fuehrendes `-`, dann haelt `argparse` den Wert fuer eine Option und `authctl revoke --family-id <id>` bricht ab; das trifft auch einen echten Operator bei jeder 64. Familie. Behandlung in Block J auf ausdrueckliche Anordnung — und damit die **erste datierte Tabu-Ausnahme** der Phase (**P8.6-AJ**: `phase4_auth/authserver/crypto.py` + zwei Zeilen `store.py`). **`phase1_storage/storage/**` bleibt zu — keine neunte P1-Contract-Oeffnung.** **V110 als negativer Befund geschlossen:** `#home-button` ruft heute `navigateAll()` (`app.js:99-105`) — „Uebersicht" und „Alle Items" sind **dieselbe Aktion**; es gibt keinen Zwei-Zustands-Schalter, sondern zwei Knoepfe fuer **einen** Zustand. **Doku-Hygiene:** 109 `.md` gescannt — 0 kaputte Links, 0 fehlende Cards, 0 fehlende INDEX-Zeilen; „nichts zu tun" war das Ergebnis, mit **einer** Ausnahme: `docs/INDEX.md` hatte gegen das ≤-38-KB-Kriterium nur **97 B Luft**, sieben geschlossene Phasen-Zeilen gestrafft (−1.549 B) ⇒ **38.473 B, 439 B Luft**. Rotation **per Skript** (P8.6-T), alle vier Gegenproben gruen, Head 72.808 → 65.666 B. `ui_budget` 5/5 (137,5 KB), `/api/v1/overview` **372,9 ms** (bestaetigt V108 ein zweites Mal). Tabu-Diff trivial leer, **Service-Touch 0**. **Naechster Schritt: opencode/M3 beginnt bei Block E — messen, nicht bauen.**

**[2026-09-13, P8.6 Partial Closeout — die Phase ist NICHT abgeschlossen und NICHT ausgeliefert.** Reine Doku-Session. **Klarstellung zum Stand:** `origin/main` steht auf `2a93e67`, lokal liegen **zwei** ungepushte Commits (`90c72e2` Block C, `bc2aa9f` Partial Closeout) — die Behauptung „7 Commits voraus" aus dem 2026-09-12-Block war falsch, per `git fetch` geprüft. Badge steht auf `v3.0.1`, Gate ⬜ **angehalten**, Step Z ⬜. **Neu:** `docs/concepts/PHASE8_6_CLOSEOUT_HANDOVER.md` (Teil-Stand, Delta, §4 ordnet die neun UX-Befunde den Locks zu, die sie öffnen — **P8.6-O2** `.shell`-Grid für Befund 5, **C1/N3-Lesart b** für Befund 7, **P8.6-E** für Befund 1+8, plus die Versionsfrage **P8.6-R**; §5 `[VERIFY]`-Bilanz 14 zu / 5 offen) + `docs/concepts/phase8_6_ui_polish_uebersicht.svg` (1080×1080, gerendert und visuell gegengeprüft, Badge **PARTIAL CLOSEOUT**). Beide existieren per **ausdrücklicher Nikinger-Anordnung vom 2026-09-13** — die in **P8.6-B** vorgesehene Ausnahme; **Plan §9 bleibt bewusst leer**, weil §9 der kanonische Abschluss ist und die Phase nicht abgeschlossen ist. **Rotation:** der Head verletzte **P8.6-T** (ein `## Session stopped` **plus** ein zweiter Session-Block als `###` — das Muster, bei dem `rotate_session_block.sh` fälschlich „bereits konform" meldet); `###` aufs `## Session stopped — <Datum>`-Schema gebracht, dann das Skript gelaufen: alle vier Gegenproben grün, Head **72.958 → 59.797 B**. **Archiv-Reparatur:** der Block-D-Sub-Block war seit der Hand-Rotation vom 2026-09-10 **mitten im Satz abgeschnitten** — **72 Zeilen / 4.403 B** fehlten; mechanisch aus `04dee6a:phase8_6_ui_polish/CLAUDE.md` wiederhergestellt, `cmp` byte-identisch, Altbestand nachweislich unverändert. **Drei weitere Drifts behoben:** Modul-Status Zeile 5 (Block C) stand auf ⬜, obwohl Commit `90c72e2` ihren Nachzug behauptet — Hard-Rule-8-Miss; `docs/INDEX.md` verletzte **P8.6-4** (40.870 B gegen ≤ 38 KB) → sechs Zeilen geschlossener Phasen gestrafft, zwei neue Zeilen aufgenommen, jetzt **38.822 B**, Kriterium erstmals seit Block A erfüllt; der Frontmatter-Closer `---` des INDEX klebte am Ende der `updated:`-Zeile statt auf einer eigenen — Frontmatter war formal kaputt. **`pytest` 970 passed in 116 s ✅** (V107-Baseline 964), Tabu-Diff §0.3 leer, Service-Touch 0 — sharefyx-mcp **PID 991** nur gelesen. **Nächster Schritt: Claude-Code-Planungssession für P8.6 Plan 2.** Empfohlene Reihenfolge (im Handover begründet): Befund 9 zuerst, weil er als einziger **auf der Produktion** reproduziert ist und damit nicht am P8.6-Deploy hängt — und zwar messen (CDP-Probe bei 1024/1200/1440), bevor repariert wird.  **Nikinger-Entscheidungen vom 2026-09-13:** **(a)** Deploy-Ziel bleibt **`v3.0.2`** — P8.6-R ist damit bestätigt, nicht überstimmt. **(b)** **Block C geht einzeln raus**, nicht in einem Sammel-Push nach Plan 2. **(c)** Die Ein-Block-Regel für die Current-state-Sektion hat er mir überlassen — **ich rate ab und habe sie verworfen**: sie hätte 3,4 KB gebracht und beim nächsten Session-Block wieder gerissen, weil **69 % der Datei in der `updated:`-Kette** steckten (28.090 B über 30 Einträge, davon 3.290 B glatte Duplikate) und nur 3.376 B in dieser Sektion. Die Kette ist stattdessen verbatim nach `PROJECT_SESSION_LOG.md` §Frontmatter-Archiv rotiert: **47.094 → 23.007 B**, alle fünf Session-Blöcke bleiben erhalten. **(d)** **Push ja, Deploy nein** (Nikinger, 2026-09-13, nachdem die Tatsachenlage aus §4.6 vorlag): die Commits gehen nach `origin/main`, **ausgeliefert wird nicht**. Live bleibt damit `6f19a8f` (P8.5). Ein Push ändert nichts an der Produktion — die drei von Block C neu eingeführten Befunde 3/4/6 erreichen keinen Nutzer, bis Plan 2 sie abgearbeitet hat. **Siebter Drift, in dieser Runde gefunden und der folgenreichste: von Phase 8.6 ist NICHTS live.** Phase-Head und der Step-V-Block unten behaupten „Push + Deploy für Block A + D vom Nikinger ausgeführt (`10f9f63..04dee6a`), `health_gate.sh --expected-sha=04dee6a` 8/8 grün". Das Werkzeug ist dabei in Ordnung: `health_gate.sh` liest den Release-SHA aus `/opt/sharefyx/current` (Z. 134/160); die Gegenprobe am 2026-09-13 meldet 7 OK + 1 FEHLER — das „8/8" ist nie so gelaufen. Gemessen am Server: `/opt/sharefyx/current` → `releases/20260905T140325.378914Z`, `git rev-parse HEAD` dort = **`6f19a8f`** — das ist der **P8.5**-Release vom 2026-09-05. Gegenprobe über sechs Block-Marker (`bg-void`, `select-fill`, `dedupeEdges`, `seedJitter`, `account-nav`, `overview__col-right`): **0 Treffer live, alle im Repo.** Das jüngste Verzeichnis unter `/opt/sharefyx/releases/` ist ebenfalls das vom 2026-09-05, und `deploy.sh:107` legt pro Lauf ein neues an — es hat also **kein** P8.6-Deploy gegeben. **Konsequenz für Entscheidung (b):** ein Deploy, der „nur Block C" ausliefert, existiert nicht — `deploy.sh` liefert `main` aus, also A+B+C+D zusammen. Der Push ist davon unberührt und läuft wie entschieden einzeln. **ROADMAP und diese Datei bleiben auf 🔄** — der formale Phasenschluss wäre eine stille Abweichung, solange Gate und Step Z offen sind.

**[2026-09-12, P8.6 Block C ✅ — Struktur-Umbau: Einstellungen oben, Alle Items unten, Karte rechts voller Hoehe, klickbare Spaces, Ordner-Zaehler.** Erst opencode/M3-Code-Touch seit Block B am 2026-09-11. **C1** `#account-button` raus aus `.rail__account` direkt unter `#home-button` + Label „Konto"→„Einstellungen" (N3-Lesart b, das `#i-settings`-Icon war schon immer ein Zahnrad). **C2** `tree.js :: renderRail()` ruft `renderScopeRow()` jetzt HINTER die Spaces + neue `tree__group`-Überschrift „Alles"; bestehende Kommentar zu „Lieber keine Zahl als eine unwahre" bleibt wörtlich erhalten (er ist die Antwort auf C5). **C3** `.overview` wird zweispaltiges Grid (`grid-template-columns: 1fr 40%` ab ≥1281px, Wrapper-DIVs `head-row`/`col-left`/`col-right`, `.overview__graph` ohne `max-width`/`min-height` [V112-Gegenprobe], `@media (max-width: 1280px)` kollabiert auf eine Spalte — Map rutscht unter die Liste); `requestAnimationFrame(resize)` in `loadGraph()` [V115] damit `seedInitialPositions()` nach dem nächsten Layout-Pass die endgültige Kartengröße hat. **C4** `.overview__space-open` als innerer `<button>` mit B1-hover + V116 `activateView`-Export (semantisch „in den Space wechseln ohne Bucket zu setzen") + `closeEditor().then(proceed => ...)`-Gating (dieselbe Disziplin wie Ordner-Buttons). **C5** `state.itemsLoaded`-Flag + `folderItemCount()`-Helfer + neuer V117-Reset in `activateView`/`navigateAll` (sonst zeigt das Rail für ein paar ms Counts aus dem falschen Pool); `.tree__count` bekommt `margin-left: auto` (gilt für Eimer + echte Ordner). **Drei Befunde/Abweichungen während Baus dokumentiert:** `activateView` doppelt definiert (Original-`function` plus neuer `export function`) → `PAGE ERROR: already declared` → `overview__spaces` blieb leer → Original entfernt; V117-Reset in beiden Navigation-Funktionen eingebaut; `requestAnimationFrame(resize)` als V115-Fix. **`pytest` 970 V107 ✅ (+3 statische Tests `test_rail_order_settings_before_tree_logout_last`/`test_account_button_says_einstellungen`/`test_overview_graph_has_no_max_width_or_min_height`), `ui_budget` V97 ✅ 5/5 (137,5 KB, +4,4 KB durch C1/C3/C4-CSS)**, Tabu-Diff §0.3 leer, Service-Touch 0 — sharefyx-mcp **PID 991** durchgehend unverändert. **Sechs Selbst-Screenshots** in `docs/screenshots/p86_block_c_{01..06}_*.png` zeigen alle fünf Sub-Ziele (Rail-Reihenfolge, „Alle Items" am Rail-Ende, Karte als rechte Spalte, klickbare Space-Zeile, Folder-Zähler) + B4-Vorsicht-Regression. Eigenes Self-Skript `phase8_6_ui_polish/scripts/p86_block_c_self_check.py` (~250 Z., Playwright + Login mit TOTP-Window-Retry + 6 Screenshots); Wegwerf-Setup reproduziert den v3ritt-Datenstand auf Port 18773, gestoppt über PID-Datei (Hard Rule 9-konform, kein `pkill -f`; `login_attempts`-Rate-Limit durch `cleanup`+`setup`+`seed-items`+`start` zurückgesetzt — das war nötig, nachdem drei fehlgeschlagene Login-Attempts die Bremse ausgelöst hatten). **Push + Deploy** für Block C wartet noch auf Dich (Drei-Bedingungen-Regel zu zwei Dritteln erfüllt — Code-Tests grün ✓, Bilder grün ✓, Nikinger-Sichtung ⬜).

**[2026-09-10, P8.6 Step V ✅ — Ollama + `qwen3-vl:8b` + V119-Smoke 46 s, Modellname-Korrektur + Plugin-Pfad für nächste Session.** Proxmox-Migration ✅ durch (i5-14600KF, sharefyx-mcp PID 991 nach Auto-Restart), Nikinger hat Ollama 0.34.0 via offizielles `curl | sh`-Script installiert (apt-Paket existiert auf Ubuntu 24.04 nicht — Korrektur in §Vormerkungen), `qwen3-vl:8b` (Q4_K_M, 6,1 GB) gepullt + V119-Smoke ✅ in 46 s gegen `c4_p8519_01_radiogruppe_im_dialog.png` (qwen3-vl:8b Cold-Start inkl. Vision-Encoder; deutsche Antwort korrekt: „Der Radio-Button ‚als Text-Link im Text' ist markiert"). `requests 2.34.2` ins Projekt-venv installiert; `phase8_6_ui_polish/scripts/vision_ollama.py` (89 Z., `requests.post(/api/generate)`, 600s-Timeout). **Modellname-Korrektur:** `internvl2.5:8b` (ursprüngliche Empfehlung) existiert nicht auf Ollama-Library — Recherche-Fehler von mir korrigiert auf `qwen3-vl:8b`. Phase-Head §Vormerkungen + Aktionsliste + Vision-Backend-Sektion entsprechend korrigiert. `pytest` V107 ✅ **966 unverändert**, `ui_budget` V97 ✅ 5/5, Tabu-Diff §0.3 leer, Service-Touch 0. **Push + Deploy** für Block A + D-Commits (`32fddba`, `04dee6a`) vom Nikinger in dieser Session autorisiert + ausgeführt (`10f9f63..04dee6a`). **Nächster Schritt** (Nikinger-Vorgabe 2026-09-10): **Schritt 1 = `DavidEasden/opencode-vision`-Plugin installieren** (vor jeder Sichtprüfung, damit Screenshots direkt im Chat gerendert werden — `docs/concepts/sichtpruefung_automation_conventions.md` §4), **Schritt 2 = visuelle Verifikation Block A + D** am echten Gerät gegen die neuen Screenshots (post-Block-A: `<select>`-Markup, post-Block-D: Zwillingskante weg + Karte stabil); Schritt 3 = Block B nach Plan §4; Schritt 4 = Block C nach Plan §5 + D3-Nachzug.

**[2026-09-10, P8.6 Block D ✅ [D1/D2/D4]** — Reiner `graph.js`-Commit (8,4 KB, +0,5 KB). D1 V102-Dedup (`dedupeEdges()` ungeordnetes Knotenpaar, P8.6-N, keine neunte P1-Contract-Öffnung), D2 FNV-1a-Layout-Seed (`seedJitter(id, salt)`, P8.6-M, „Karte fliegt" behoben), D4 `cancelAnimationFrame` in `runSimulation()` (P8.6-§6.4, **einzige Scope-Erweiterung**, streichbar). D3 🟡 wartet auf Block C. `pytest` 966 unverändert, `ui_budget` 5/5, Tabu-Diff §0.3 leer, Service-Touch 0. Items #2/3/4 aus dem Handover blockiert (Ollama-Migration steht bevor).

**[2026-09-10, P8.6 Block A ✅ — Fundament:** Radiogruppe→`<select>`, sechs neue Tokens (`--bg-void`/`--select-fill`/`--select-line`/`--caution` u. a.), `--border-soft`→`var(--line)`, Konvention v3 um „Vorsicht". Erste echte Code-Touch-Session der Phase. Tabu-Diff §0.3 leer, `pytest` 964→966, `ui_budget.py` 5/5. Nikinger hat die P8.5-19-Radiogruppe am 2026-09-08 selbst zurückgenommen. +2 statische Tests (P8.5-Test ersetzt, `test_no_raw_accent_rgba_outside_root`, `test_every_css_var_reference_is_defined` — hätte `--border-soft`-Bug gefunden). **Abweichung von Plan §3.5/§8.2 dokumentiert:** die anderen 4 Tests gehören zu Block B/C.

_Vollständige Chronik der älteren Einträge (Phase 8, Phase 8.5-Vorlauf, Phase 7/6.5/6-Abschluss,
Phase-5/4/3/2/1-Zusammenfassungen, Hard-Rule-Korrekturen): `docs/PROJECT_SESSION_LOG.md` (L3).
Neue Session-Blöcke wachsen oben in dieser Current-state-Sektion; ältere Blöcke rotieren
verbatim nach `PROJECT_SESSION_LOG.md`. **[2026-09-13]** Eine Ein-Block-Regel wurde erwogen und
**verworfen**: gemessen steckten 69 % der Dateigröße in der `updated:`-Frontmatter-Kette
(28.090 B über 30 Einträge, davon 3.290 B glatte Duplikate), nicht in dieser Sektion
(3.376 B). Die Kette ist verbatim nach `PROJECT_SESSION_LOG.md` §Frontmatter-Archiv rotiert —
dieselbe Lösungsrichtung, die für `docs/INDEX.md` vorgemerkt ist._



