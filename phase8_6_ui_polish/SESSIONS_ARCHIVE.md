---
status: archive
purpose: Archivierte Session-stopped-Blöcke aus phase8_6_ui_polish/CLAUDE.md, verbatim, newest-first
read-when: Auditieren der vollen Phase-8.6-Historie — der aktuelle Session-Block lebt im Phase-Head, nicht hier
detail: L3
up: ./CLAUDE.md
down:
updated: 2026-09-18 (Block-H-R-3-Bau-Session-Block [Claude Code, 2026-09-17] per `scripts/rotate_session_block.sh phase8_6_ui_polish` verbatim ins Archiv rotiert — Phase-Head 118.450→104.826 B, Archiv 212.293→225.917 B. Phase-Head trägt jetzt den Gate-GA1+GA2-Session-Block [Claude Code, Wegwerf-Ritt + `p86_polish_smoke.py` neu, 18/18 Stationen grün, ein Produktbefund `.detail__back` toter Code]. **Korrektur-Notiz:** erster Rotationslauf dieser Session hatte das neue Session-Block VOR dem alten eingefügt — das Skript hält Konvention „neuester Block steht zuletzt im Head" (`KEEP_INDEX = STARTS.length - 1`), archivierte dadurch den neuen statt des alten Blocks. Aus den Skript-eigenen `.bak`-Backups wiederhergestellt, Blockreihenfolge vor dem zweiten Lauf vertauscht, zweiter Lauf korrekt) | 2026-09-17 (Block H-R-3 Escalation-Session-Block [Claude Code, 2026-09-15] per `scripts/rotate_session_block.sh phase8_6_ui_polish` verbatim ins Archiv rotiert — Phase-Head 105.433→101.545 B, Archiv 208.018→211.906 B. Phase-Head trägt jetzt den Block-H-R-3-Bau-Session-Block [Claude Code, drei Locks H-R.6/H-R.7/H-R.8, pytest 991→992, Live-Verifikation gegen Wegwerf v3ritt]) | 2026-09-15 (Block H-R-3 Escalation-Report nach Nikinger-Sichtung — Phase-Head 101.669→96.476 B, Archiv 201.928→207.121 B. Watchdog-Vormerkungs-Sub-Block 105 Z./5.193 B per `scripts/rotate_session_block.sh phase8_6_ui_polish` ins Archiv rotiert; Phase-Head jetzt nur Block-H-R-3-Escalation-Session-Block. **Rein dokumentarisch — keine Code-Änderung.** Drei Nikinger-Befunde aus Sichtung der fünf H-R-Teil-2-Screenshots (01/02 akzeptiert, 03 Klärungsbedarf, 04 Umkehr von G-R.1, 05 neue Editor-fullview-Variante) → `docs/concepts/phase8_6_ui_polish_block_h_r_3_escalation.md` neu (~9 KB). Mini-Plan-Vorschlag mit drei Locks H-R.6/H-R.7/H-R.8 + Wächter-Liste + zwei Klärungsfragen. Routing-Hinweis: opencode/M3 für Pixel-Befunde ausgeschlossen (V-vision-befund 2026-09-11), diese Runde ist **Claude-Code-Territorium**. Nächster Schritt: Block H-R-3 (Claude Code), dann J, Gate, Z) | 2026-09-15 (Tailscaled-Watchdog-Vormerkung nach heutiger Control-Plane-Outage — Phase-Head 109.087→97.776 B, Archiv 189.880→201.191 B. Block-H-R-Teil-2-Session-Block 191 Z./11.311 B per `scripts/rotate_session_block.sh phase8_6_ui_polish` ins Archiv rotiert; Phase-Head jetzt nur Tailscaled-Watchdog-Session-Block. **Rein dokumentarisch — keine Code-Änderung.** Neue Vormerkung „Tailscaled-Watchdog (Nikinger-Vorgabe 2026-09-15)" in §Vormerkungen mit drei Lösungs-Ansätzen (OnFailure-Hook / Watchdog-Unit mit zyklischer Prüfung / Tailscale-eigenes Feature) für „Control-Plane lange nicht erreichbar"-Fall. Nächster Schritt: Block J (P8.6-AJ, der `pytest`-Flake) unverändert; Watchdog als Mini-Phase nach P8.6 Gate) | 2026-09-14 (**Block H-R Teil 2 erledigt ✅ — H-R.3 + H-R.4 + H-R.5** — Head 109.202→99.718 B, Archiv 180.176→189.660 B. Block-H-R-Teil-1-Session-Block 146 Z./9.484 B per `scripts/rotate_session_block.sh phase8_6_ui_polish` ins Archiv rotiert; Phase-Head jetzt nur Block-H-R-Teil-2-Session-Block. **Phase 8.6 ist nach H-R-2 bei Block 12 von 13 angekommen** — Editor-YAML-Bündigkeit (CSS-Fix: padding-bottom 12 → 40 px, V142-CDP-Probe 27,14 → 0,86 px) + 1024-er Map-Overlap (kein Fix, V143 misst 0 Rechteck-Schnittmenge) + 1024-er Editor-Modus (kein Fix, V144 misst 16/16 Knöpfe reachable); der nächste Block ist J (der pytest-Flake, P8.6-AJ), dann Gate, dann Z (Closeout)) | 2026-09-14 (**Block H-R Teil 1 erledigt ✅ — H-R.1 + H-R.2** — Head 88.519 B [unverändert nach Rotation], Archiv 151.336→169.569 B. Block-G-R-Session-Block 235 Z./18.073 B per `scripts/rotate_session_block.sh phase8_6_ui_polish` ins Archiv rotiert; Phase-Head jetzt nur Block-H-Session-Block. **Phase 8.6 ist nach H bei Block 10 von 13 angekommen — Rail-Umkehr (Befund 7b) + Konto-Dialog-Afford (Befund 2) in einem Schritt behoben, der nächste Block ist J (der pytest-Flake, P8.6-AJ, datierte Tabu-Ausnahme für phase4_auth/authserver/{crypto.py,store.py})**) | 2026-09-14 (**Block G-R erledigt ✅** — Head 82.028→85.760 B, Archiv 138.612→151.336 B. Block-G-Session-Block 159 Z./11.728 B per `scripts/rotate_session_block.sh phase8_6_ui_polish` ins Archiv rotiert; Phase-Head jetzt nur Block-G-R-Session-Block. **`Phase 8.6` ist nach G-R bei Block 9 von 13 angekommen — Layout/Editor-YAML-Bündigkeit + Layer-Tone-Drift aus der Sichtung behoben, der nächste Block ist H (Rail + Konto-Dialog, Befunde 7b + 2)**) | 2026-09-14 (E2b-Sub-Block [vom 2026-09-14, E2b-Commit `cc3f342`] per `scripts/rotate_session_block.sh` verbatim aus dem Phase-Head hierher rotiert — sechste Skript-Rotation der Phase, alle vier Gegenproben gruen; 78 Zeilen / 5.058 B; Archiv 128.603 → 133.661 B) | 2026-09-14 (E2a-Sub-Block [vom 2026-09-14 früh, E2a-Commit `f8e413c`] per `scripts/rotate_session_block.sh` verbatim aus dem Phase-Head hierher rotiert — fünfte Skript-Rotation der Phase, alle vier Gegenproben gruen; 78 Zeilen / 6.720 B; Archiv 121.609 → 128.329 B) | 2026-09-14 (Plan-2-Block [vom 2026-09-13] per `scripts/rotate_session_block.sh` verbatim aus dem Phase-Head hierher rotiert — vierte Skript-Rotation der Phase, alle vier Gegenproben gruen; 78 Zeilen / 6.410 B; Archiv 114.955 → 121.365 B) | 2026-09-13 (Block-C-Sichtungs-Sub-Block [vom 2026-09-12, Commit `bc2aa9f`] per `scripts/rotate_session_block.sh` verbatim aus dem Phase-Head hierher rotiert — zweite Skript-Rotation der Phase, alle vier Gegenproben gruen; 114 Zeilen / 7.142 B; Archiv 107.535 → 114.677 B) | 2026-09-13 (Block-C-Sub-Block [vom 2026-09-12, Commit `90c72e2`] per `scripts/rotate_session_block.sh` verbatim aus dem Phase-Head hierher rotiert — erste Skript-Rotation dieser Phase, alle vier Gegenproben gruen. **Reparatur:** der Block-D-Sub-Block war seit der Hand-Rotation vom 2026-09-10 mitten im Satz gekappt; **72 Zeilen / 4.403 B** aus `04dee6a:phase8_6_ui_polish/CLAUDE.md` mechanisch wiederhergestellt, `cmp` gegen das Original byte-identisch, Altbestand nachweislich unveraendert. Der vormals verwaiste `## Session stopped`-Header fuehrt seither korrekt die beiden `###`-Sub-Bloecke darunter) | 2026-09-11 (Block-B-Sub-Block [vom 2026-09-11, Block-B-Commit] verbatim aus dem Phase-Head hierher rotiert vor dem Block-B-Nächste-Session-Update (P8.6-T-Rotationsregel); Phase-Head trägt jetzt nur den Block-B-Sub-Block) | 2026-09-11 (V121+V122-Visual-Sub-Block [vom 2026-09-10, Commit `5152d35`] verbatim aus dem Phase-Head hierher rotiert vor dem V-vision-befund-Commit (P8.6-T-Rotationsregel); Phase-Head trägt jetzt nur den V-vision-befund-Sub-Block, SESSIONS_ARCHIVE jetzt mit neun Sub-Blöcken) | aeltere Eintraege: die `### date`-Sub-Bloecke in `SESSIONS_ARCHIVE.md`
---
# SESSIONS_ARCHIVE.md — Phase 8.6: UI-Politur, Selektion + Layout, drei Graph-Fixes

Archiv der historischen Sub-Blöcke, newest-first. Der aktuelle Session-Block lebt im
Phase-Head (`./CLAUDE.md` §Session stopped). Rotation nach P8.6-T: bei jedem neuen
`### date`-Sub-Block wandert der bisherige **verbatim** hierher. Skript
`scripts/rotate_session_block.sh phase8_6_ui_polish` für saubere Übernahme — die
Phase-8.5-Step-V-deferred-Rotation am 2026-09-10 wurde **per Hand** gemacht, weil
das Skript auf das Phase-8.5-Muster passt und mit einem `## Session stopped` + mehreren
`### date`-Subblöcken Exit 2 „Bereits konform" wirft.

---







## Session stopped — 2026-09-17 (Claude Code — Block H-R-3, drei Locks, ein Commit)

**Auftrag:** Escalation-Report `phase8_6_ui_polish_block_h_r_3_escalation.md` übernehmen,
zwei offene Klärungsfragen mit dem Nikinger durchgehen, dann H-R.6/H-R.7/H-R.8 bauen und live
gegen die Wegwerf-Instanz verifizieren (opencode/M3 ist für Pixel-Befunde nicht der richtige
Adressat, siehe Vorsitzung).

**Klärung (AskUserQuestion, vor dem Bau):**

1. **H-R.8:** Nikinger wählte **Lesart b** (Layout-Wechsel). Vorher recherchiert und dem
   Nikinger vorgelegt: Lesart a stützte sich auf eine überholte Prämisse — `app.js:97-100`
   dokumentiert, dass `#home-button` (→ Spaces-Übersicht) und `.tree__scope` (→ globaler
   „Alle Items"-Modus) seit Block G / Plan 2 §4.3 **getrennte, nicht-redundante** Aktionen
   sind, nicht mehr dieselbe wie zur V110-Zeit. Lesart a hätte eine funktionierende Funktion
   gelöscht, keine Redundanz behoben.
2. **G-R.1-raus:** Nikinger bestätigte „bei 'ohne Map' Entscheidung bleiben und umsetzen" —
   sauberer Schnitt statt Override-Layer (Empfehlung übernommen, keine explizite
   Einzelentscheidung dazu nötig).

**Code-Erkenntnis vor dem Bau, senkt den Scope drastisch:** `shellEl.dataset.view` togglet
bereits seit Block G zwischen `"list"`/`"detail"` (`editor.js:58` `showOverviewPane()`,
`editor.js:82` `clearDetail()`, `editor.js:427` `loadEditorFromItem()`) — **ohne** CSS-
Konsument bislang. ESC (`app.js:216`) und die ×-Buttons (`editor.js:554`) laufen beide durch
`closeEditor() → clearDetail() → showOverviewPane()`. Das deckt „ESC/× bringt zurück" für
H-R.7 **und** H-R.8 vollständig ab, ohne eine Zeile JS oder HTML anzufassen — die Escalation-
Report-Schätzung („app.js + editor.js: ~5–10 Zeilen JS-Touch") war zu hoch gegriffen.

**Gebaut (`phase5_ui/webui/static/app.css`, ein Commit):**

- **Lock H-R.8** (außerhalb jeder `@media`-Query, gilt bei allen Breiten):
  `.shell[data-view="detail"] { grid-template-columns: 240px 1fr }` +
  `.shell[data-view="detail"] .list { display: none }`.
- **Lock H-R.6** (innerhalb `@media (max-width: 1024px)`, ersetzt G-R.1 komplett):
  `.shell { grid-template-columns: 240px 1fr; grid-template-rows: 1fr }` (eine Zeile statt
  zwei), `.rail { grid-row: 1 }`, `.detail__graph { display: none }`.
- **Lock H-R.7** (innerhalb derselben Media-Query, baut auf H-R.8s Basisregel auf — gleiche
  Spezifität, spätere Quellreihenfolge gewinnt): `.shell[data-view="detail"] {
  grid-template-columns: 1fr }` + `.shell[data-view="detail"] .rail { display: none }`.

**Cascade-Probe vor dem Testlauf:** `.shell[data-view="detail"]` hat Spezifität (0,2,0),
schlägt die reinen `.shell`-Regeln in den 1200/1024-Media-Queries (0,1,0) unabhängig von der
Quellreihenfolge — die 1024-interne Fassung von `.shell[data-view="detail"]` (gleiche
Spezifität wie die Basisregel, aber später im Quelltext) gewinnt dort zusätzlich gegen die
Basisregel. Beide Mechanismen von Hand durchgerechnet, dann live per Probe bestätigt (unten).

**Tests (`phase5_ui/tests/test_static_routes.py`):** zwei G-R.1-Tests waren nach dem Wegfall
der Stapel-Logik reine Duplikate derselben jetzt toten Grid-Properties —
`test_1024_breakpoint_stacks_list_over_detail` umbenannt + neu geschrieben zu
`test_1024_breakpoint_has_single_row_no_map` (prüft `grid-template-rows: 1fr` statt `1fr 1fr`,
`.detail__graph display:none`, Negativ-Check auf alle G-R.1-Marker), `test_1024_no_overlap_in_css`
**gelöscht** (seine gesamte Prämisse — Überlapp-Risiko zwischen Karte und Rail/Liste — entfällt,
wenn die Karte nie sichtbar ist; ein dritter Test mit denselben Assertions wäre reine
Duplikation gewesen). `test_shell_grid_is_240_480_1fr`s dritter Anker (1024-px-Zeilen) auf
`grid-template-rows: 1fr` nachgezogen (schlug sonst rot an — im ersten Testlauf gefunden, nicht
vorher gesehen). Zwei neue Tests: `test_1024_editor_fullview_hides_rail_and_list` (H-R.7),
`test_editor_open_hides_list_at_all_viewports` (H-R.8, inkl. Negativ-Check, dass `#home-button`
nicht verschwunden ist — Lesart a wurde verworfen). **Netto +1 Test** (991 → **992**) —
Abweichung von der Escalation-Report-Schätzung „991 unverändert", die nur von einem
G-R.1-Test ausging statt den tatsächlich vorhandenen zwei.

**Live-Verifikation (eigenes Skript `phase8_6_ui_polish/scripts/p86_block_h_r_3_self_check.py`,
Wegwerf-Instanz v3ritt, Port 18773, `.venv/bin/python wegwerf_setup_v3ritt.py start`/`stop`,
PID-Datei-gestoppt, Hard-Rule-9-konform):**

| Viewport | Zustand | `dataset.view` | `.rail` | `.list` | `.detail__graph` | Grid |
|---|---|---|---|---|---|---|
| 1440 | Editor offen | detail | flex | **none** | none | `240px 1200px` |
| 1200 (Kontrolle) | Editor offen | detail | flex | **none** | none | `240px 960px` |
| 1024 | Übersicht | list | flex | flex | **none** | `240px 784px` |
| 1024 | Editor offen | detail | **none** | **none** | none | `1024px` |

Alle vier Zeilen bestätigen die Locks exakt wie vorhergesagt — inklusive der Kontroll-Zeile
(1200 px verhält sich wie 1440, H-R.7 leckt nicht in den 1200-Breakpoint). Vier Screenshots
`docs/screenshots/p86_block_h_r_3_{01,02,03,04}_*.png`, visuell gegengeprüft (kein
Layout-Bruch, Editor-Kopf + Format-Toolbar + Anhängen-Zeile bleiben in allen vier Zuständen
korrekt gerendert). `screenshots_latest/` im selben Commit nachgezogen (P8.6-AK, vier
Symlinks + README-Tabelle ersetzt).

**Selbstprüfung §0.5:** `pytest -q` **992 passed in 116,64 s** (Baseline 991 unverändert
+1 netto, siehe oben), Tabu-Diff §0.3 leer (`git diff --stat` gegen die Tabu-Pfade: leer;
tatsächlich berührt nur `phase5_ui/webui/static/app.css` +
`phase5_ui/tests/test_static_routes.py` + das neue Self-Check-Skript), `node --check` auf
alle 13 JS-Dateien ✅ (keine JS-Änderung), `ui_budget.py` **5/5 im Korridor** (144,2 KB gzip,
+0,5 KB ggü. 143,7 KB — passt zur erwarteten +1–2 KB roh). Kein `pkill -f`, kein `systemctl`,
sharefyx-mcp **PID 991** durchgehend nur gelesen (`systemctl status` read-only bestätigt,
Uptime 1 Woche).

**Doku-Hygiene:** Modul-Status neue Zeile 14b (H-R-3), dieser Session-Block, Rotation per
`scripts/rotate_session_block.sh phase8_6_ui_polish` (H-R-3-Escalation-Session-Block vom
2026-09-15 wandert verbatim ins Archiv), `docs/INDEX.md`-Zeile für die neuen Screenshots +
das neue Skript nachgezogen, `screenshots_latest/README.md` im selben Commit.

**Nächster Schritt:** Block J (`pytest`-Flake, P8.6-AJ, datierte Tabu-Ausnahme
`phase4_auth/authserver/{crypto.py,store.py}`) — Reihenfolge P8.6-AH jetzt: G ✅ → G-R ✅ →
H ✅ → H-R-Teil-1+2 ✅ → **H-R-3 ✅** → **J ⬜** → **Gate ⬜** → **Z ⬜** (Closeout).

**Nachtrag, 2026-09-17 — Rail-Exklusivität Übersicht vs. Space/Eimer/Ordner (Nikinger-Fund
aus dem `03_1024_ohne_karte.png`-Screenshot):** Nikinger-Feedback nach Sichtung der vier
H-R-3-Screenshots: „wenn ich 'Übersicht' auswähle, sollte das jede andere Auswahl (wie
alpha→Offen) ausschließen, da das unterschiedliche Aktionen sind." Beleg: `state.activeSpace`/
`state.filter`/`state.folder` werden beim Wechsel in die Übersicht (`state.overview = true`,
`app.js` homeButtonEl-Handler) **bewusst nicht** geleert — der Rückweg in den zuvor besuchten
Space soll die Filterung wiederfinden (siehe Kommentar `list.js :: clearDetail()`). `tree.js`s
Highlight-Logik (`renderFolders()` Zeile 63, `folderButton()` Zeile 182, `homeButtonEl.setAttribute`
Zeile 334) prüfte das aber nie gegen `state.overview` — ein zuvor markierter Eimer/Ordner blieb
`aria-current="true"`, während gleichzeitig die Übersicht angezeigt wurde. Zusätzlich war
`#home-button`s eigene Logik zu grob: `state.selectedId === null` markierte Home auch dann als
aktuell, wenn tatsächlich ein Space/Eimer/Ordner **oder** der globale „Alle Items"-Modus ohne
ausgewähltes Item gezeigt wurde — dieselbe Doppel-Markierungs-Klasse in zwei weiteren
Kombinationen, nicht nur der vom Nikinger gemeldeten.

**Fix (`phase5_ui/webui/static/js/tree.js`, kein CSS-/HTML-Touch):** drei Stellen ergänzt um
die fehlende Übersicht-Exklusivität — `renderFolders()`- und `folderButton()`-Bedingungen
bekommen `!state.overview` als zusätzliche Voraussetzung für `aria-current="true"`;
`homeButtonEl`s Bedingung wechselt von `state.selectedId === null` auf `state.overview === true`
(Home steht seit Block G konkret für die Übersicht, Plan 2 §4.3 — der eigene Zustandsflag ist
der richtige Schalter, nicht die Item-Auswahl). `isGlobalScope()`/„Alle Items" brauchte keine
Änderung — `state.scope === "all"` und `state.overview === true` schließen sich durch die
bestehenden Setter (`navigateAll()`, homeButtonEl-Handler) bereits strukturell aus.

**Verifikation:** eigenes Skript `phase8_6_ui_polish/scripts/p86_block_h_r_3_nachtrag_self_check.py`
gegen die Wegwerf-Instanz v3ritt (Port 18773, PID-Datei-gestoppt) — navigiert nach
`alpha → Offen` (`aria-current`: home=false, Offen=true), dann zurück in die Übersicht
(`aria-current`: home=true, Offen=null, Alle-Items=null) — **exklusiv, wie gefordert**.
Screenshot `docs/screenshots/p86_block_h_r_3_nachtrag_uebersicht_exklusiv.png` zeigt nur noch
„Übersicht" markiert, „Offen" ohne Hervorhebung, „alpha" bleibt aufgeklappt (das ist reiner
Expand-Zustand, keine Aktuell-Markierung, unverändert).

**Selbstprüfung:** `pytest -q` **992 passed** (unverändert, keine pytest-Berührung — JS bleibt
laut P5-T unit-ungetestet), `node --check` auf `tree.js` ✅, `ui_budget` 5/5 (144,7 KB, +0,5 KB
Kommentare), Tabu-Diff §0.3 leer, sharefyx-mcp PID 991 nur gelesen. Zweiter Commit dieser
Session (der erste war der H-R-3-Bau oben) — eigener Fund nach Sichtung, kein Amend.

**Nachtrag 2, 2026-09-17 — Block J erledigt (P8.6-AJ, `pytest`-Flake, beide Hälften nach
Plan 2 §6 wörtlich).** Dritter Commit dieser Session, bewusst getrennt vom UI-Diff oben (§6.5:
„ein Auth-Touch gehört nicht in einen CSS-Diff").

**J1 (Produktionsfehler):** `phase4_auth/authserver/crypto.py` bekommt `new_public_id(nbytes:
int = 16)` direkt unter `new_secret()` — Rejection-Sampling (`while not value.startswith("-")`)
statt Umkodierung, damit Alphabet und Länge zu `new_secret` identisch bleiben (Entropieverlust
= ein verworfenes 64stel). `store.py:294` (`create_client` → `client_id`) und `store.py:393`
(`create_family` → `family_id`) auf `crypto.new_public_id(16)` umgestellt — genau die zwei
Stellen, deren Wert später auf einer Kommandozeile steht (`authctl revoke --family-id <ID>`).
Die zehn übrigen `new_secret`-Aufrufstellen (`store.py:339, 465, 516, 517, 578, 579, 905, 1019,
1020` plus die eine in `create_client` selbst für `client_secret`, sofern vorhanden) bleiben
unverändert — sie erzeugen opake Geheimnisse, die nie eine Kommandozeile sehen.

**J2 (Altbestand):** `phase4_auth/scripts/authctl.py`s `p_revoke.add_argument("--family-id",
…)` bekommt einen `help`-Text, der die Gleichheitsform (`--family-id=-abc`) nennt — der einzig
sinnvolle Ausweg für IDs, die vor diesem Fix vergeben wurden. Keine `sys.argv`-Vorverarbeitung
(wäre ein Sonderweg an `argparse` vorbei).

**J3 (Tests):** `test_revoke_kills_the_family` (`phase4_auth/tests/test_authctl.py`) auf
`"--family-id=" + family_id` umgestellt — Verteidigung in der Tiefe, der Test bleibt grün, auch
falls je wieder eine führende `-` vorkäme. Neu: `test_revoke_accepts_a_family_id_starting_with_a_dash`
(Altbestands-Pfad, `--family-id=-abc` → rc 0) und `test_new_public_id_never_starts_with_a_dash`
(`phase4_auth/tests/test_crypto.py`, 5.000 Ziehungen, zusätzlich Länge/Alphabet-Gleichheit zu
`new_secret` geprüft — bei 1,569 % gemessener Trefferquote macht das einen stillen Rückfall auf
`new_secret` praktisch unmöglich unentdeckt).

**J4 (enge Tabu-Probe, vor dem Commit ausgeführt):** `git diff --stat -- phase4_auth/authserver`
→ **genau zwei Dateien** (`crypto.py`, `store.py`), in `store.py` **genau 2 geänderte Zeilen**
(4 Diff-Zeilen: 2 entfernt, 2 hinzugefügt) — deckungsgleich mit der Plan-2-§6.4-Erwartung. Die
breitere Tabu-Probe (§0.3, `phase1_storage/storage` + `phase2_mcp/mcpserver` +
`phase5_ui/webui/{security,api,serializers,permissions}.py`) blieb ebenfalls leer — **keine**
neunte P1-Contract-Öffnung.

**Selbstprüfung §0.5:** `pytest -q` **994 passed in 111,5 s** (992 + 2 netto — J3 fügt zwei
Tests hinzu, `test_revoke_kills_the_family` ist eine Umstellung, kein neuer Test; Plan-2-§6.5-
Erwartung „+3, ≥ 972 passed" war gegen die alte 969-Baseline geschätzt, die reale Baseline ist
seit H-R-3 bei 992 gewachsen). `phase4_auth/tests/{test_crypto,test_authctl}.py` isoliert
**26/26 grün**. Keine `ui_budget`-Prüfung nötig (kein `phase5_ui/webui/static/**`-Touch, Block
J ist reiner Auth-Code + Auth-Tests). Kein `pkill -f`, kein `systemctl`, sharefyx-mcp **PID 991**
nicht angefasst.

**Doku-Hygiene:** Modul-Status Zeile 15 ⬜→✅, dieser Nachtrag-2-Abschnitt, `docs/INDEX.md`-
Phase-8.6-Zeile + Wurzel-`CLAUDE.md`-Current-state + `phase4_auth/CLAUDE.md`s Flake-Notiz
(„bekannter Flake" → „behoben, siehe hier") im selben Commit nachgezogen.

**Nächster Schritt:** Reihenfolge P8.6-AH damit **G ✅ → G-R ✅ → H ✅ → H-R-1+2 ✅ → H-R-3 ✅ →
J ✅ → Gate ⬜ → Z ⬜.** Gate ist ein eigener, größerer Schritt (Wegwerf-Ritt +
`p86_polish_smoke.py`, 14 Stationen aus Plan 2 §7.2, Chromium+Firefox für vier Stationen,
Nikinger-Sichtprüfung mit fünf offenen Entscheidungen §7.3, danach Deploy `v3.0.2` — Plan 2
§7) — bewusst nicht in diesem atomaren Schritt mitgebaut.
## Session stopped — 2026-09-15 (opencode/M3 — Block H-R-3 Escalation-Report, Übergabe an Claude Code)

**Rein dokumentarisch, kein Produktcode-Touch, kein Service-Touch.**
Nikinger-Sichtung der fünf `p86_block_h_r_{01..05}_*.png`-Screenshots hat
drei neue UX-Befunde ergeben, die über Block H-R-Teil-2 hinausgehen:

| # | Befund | Schwere |
|---|---|---|
| 01 | super, sieht nach dem aus was wir wollen | ✅ akzeptiert |
| 02 | konsistentes Design | ✅ akzeptiert |
| 03 | „Alle Items" + „Übersicht" sind zwei Buttons für eine Aktion (V110), und Listen-Slot bei 1440 px Editor-open zeigt Übersicht statt Items — redundant | Klärungsbedarf |
| 04 | 1024 px **keine Map** — Umkehr von Block G-R G-R.1 | Layout-Revision |
| 05 | 1024 px **nur Editor** (Navbar + Liste + Karte weg), ESC/× zurück | neue Variante |

### Was ausgeliefert wurde (dieser Commit)

- **`docs/concepts/phase8_6_ui_polish_block_h_r_3_escalation.md` neu (~9 KB)** —
  Anlass, Stand, Mini-Plan-Vorschlag mit drei Locks H-R.6/H-R.7/H-R.8,
  zwei offene Klärungsfragen, technischer Scope, Tabu-§0.3-Verträglichkeit,
  erwartete Kennzahlen, fünf empfohlene Screenshots, Modell-Empfehlung für
  die Claude-Code-Session. **Direkt-Einstieg-fähig** — Claude Code kann
  ohne weitere M3-Vermittlung mit dem Report arbeiten.
- **`docs/INDEX.md`** — Frontmatter `updated:` mit H-R-3-Eintrag
  prependet, neue Zeile 47 für den Escalation-Report nachgezogen.
- **`phase8_6_ui_polish/CLAUDE.md`** — dieser Session-Block.
- **Rotation per `scripts/rotate_session_block.sh phase8_6_ui_polish`** —
  Watchdog-Sub-Block vom Vorturn (191 Z./11.311 B) ins Archiv rotiert;
  Phase-Head trägt jetzt diesen Escalation-Session-Block allein.

### Was NICHT ausgeliefert wurde (mit Begründung)

- **Keine Code-Touches** an `phase5_ui/webui/static/{app.css,app.html,app.js,tree.js}`
  oder `phase5_ui/tests/test_static_routes.py` — die H-R.3-Locks werden
  von Claude Code in der nächsten Session gebaut, mit Pixel-Verifikation
  am laufenden System. opencode/M3 ist für Pixel-Befunde nicht der
  richtige Adressat (Nikinger-Vorgabe: „Evtl sollte sich Claude Code
  darum kümmern, solange das Vision plugin bzw die Weiterleitung der
  Bilder an dich nicht 100% funktioniert"; V-vision-befund 2026-09-11
  dokumentiert die Lücke).
- **Keine Klärung der zwei offenen Fragen** (H-R.8 Lesart a vs. b;
  G-R.1-raus-Bestätigung) — diese gehen mit dem Escalation-Report an
  Claude Code, der sie mit dem Nikinger direkt durchgeht.

### Drei Hard-Rule-Checkpoints am Session-Ende

1. **Hard Rule 1** (keine Secrets): keine Credentials, kein neuer
   Code-Touch, keine Schreib-Operationen außer den Doc-Updates.
2. **Hard Rule 9** (kein Service-Touch durch opencode/M3): `systemctl
   status` + `journalctl` + `tailscale status`/`netcheck` + `curl`/
   `health_gate.sh` weiterhin nur lesend, **kein** `systemctl
   restart/start`, kein `kill`, kein `pkill -f`. Der manuelle
   `systemctl restart tailscaled` um ~21:55 CEST war **Nikinger-Aktion**;
   sharefyx-mcp PID 991 + tailscaled PID 263180 durchgehend nur gelesen.
3. **Hard Rule 8** (Commit ⇒ Doku-Update im selben Commit):
   Escalation-Report + INDEX.md-Updates + dieser Session-Block +
   Frontmatter-`updated:`-Eintrag in Phase-Head + SESSIONS_ARCHIVE.md-
   `updated:`-Eintrag (nach Rotation) — alles im selben Commit.

### Nächster Schritt

Push dieses Commits (Nikinger-Aktion), dann Übergabe an Claude Code für
Block H-R-3. Nach Klärung der zwei offenen Fragen mit dem Nikinger baut
Claude Code die drei Locks + drei Wächter in einem atomaren Commit. Reihenfolge
P8.6-AH jetzt: G ✅ → G-R ✅ → H ✅ → H-R-Teil-1+2 ✅ → **H-R-3 ⬜
(Claude Code)** → **J ⬜** → **Gate ⬜** → **Z ⬜** (Closeout).

Tailscaled-Watchdog bleibt als Mini-Phase nach P8.6 Gate eingereiht
(siehe §Vormerkungen im Phase-Head).

## Session stopped — 2026-09-15 (opencode/M3 — Tailscaled-Control-Plane-Outage heute, Watchdog-Vormerkung + neuer Block-Vorschlag)

**Rein diagnostisch, kein Produktcode-Touch.** Nikinger-Vorgabe nach der
~4-h-Downphase heute: „teste, ob die restart Logik korrekt funktioniert
hat, und führe ggf entsprechende befehle aus bzw gebe sie mir". Befund in
drei Schritten — neue Vormerkung in §Vormerkungen.

### Schritt 1 — Restart-Logik-Verifikation (alle read-only)

`systemctl status sharefyx-mcp` → active (running) seit 5 Tagen, PID 991
unverändert, 117,8 MB RAM, 1 h 31 min CPU akkumuliert.
`phase8_5_picker_release/scripts/health_gate.sh --expected-version=v3.0.1
--expected-sha=6f19a8f` → **8/8 grün** (`result:ok`,
`Release-SHA 6f19a8fc1f0bcdc2c3bc91fc934a057964647ed4 matched`). Live ist
weiter v3.0.1 / `6f19a8f` (Korrektur-Stand 2026-09-13 unverändert).

Journalctl-Restart-Historie (`Aug 30 … Sep 10`): sieben systemd-Restarts
in 17 Tagen, typischer Takt 1–5 Tage. Aktueller PID 991 läuft seit
2026-09-10 19:37:48 — hat den heutigen Suspend **ohne** systemd-Restart
überlebt (Kernel freezed Prozess-State, `Active since`-Timestamp
unverändert). `Restart=on-failure` + `RestartSec=5` +
`WantedBy=multi-user.target` + `After=network-online.target tailscaled.service`
+ `Wants=network-online.target` in `/etc/systemd/system/sharefyx-mcp.service`
(Z. 4-7/23-24) — korrekt konfiguriert, kein Drift.

### Schritt 2 — Downtime-Ursache (NICHT Crash, sondern Suspend)

`t tailscaled`-Journal um **21:50:30 CEST**: `time jump detected (slept
3h59m22s), probably wake from sleep` — VM war **17:51–21:50 CEST**
suspendiert (~4 h), kein Reboot. `sharefyx-mcp` behielt PID 991;
`tailscaled` wachte mit `LinkChange: major, rebinding` + `magicsock:
endpoints changed` auf, DERP-Region 4 wurde neu verbunden — dann klemmte
die Control-Plane.

Restart-Logik greift hier **nicht**: sie ist für Crashes (Exit-Code ≠ 0),
nicht für Suspend/Resume. Für Suspend bleibt der Prozess-State erhalten,
kein systemd-Eingriff nötig.

### Schritt 3 — Tunnel-Befund (`tailscale status` zeigte `offline`)

Während `sharefyx-mcp` weiter lokal 200/401 antwortete (alle 8 Gates grün),
zeigte `tailscale status` `100.118.131.68 … linux offline` — Control-
Plane kannte das Node nicht als online. Journal zeigte alle 60 s dasselbe
Muster ab 21:51:

```
21:51:30  control: map response long-poll timed out!
          Received error: PollNetMap: context canceled
21:52:30  control: lite map update error after 2m0.001s
          Post "https://controlplane.tailscale.com/machine/map":
          context canceled
21:53:30  … dito …
21:54:30  … dito …
```

`controlplane.tailscale.com` 5+ min nicht erreichbar (DNS-Resolution,
CGNAT-Router oder Tailscale-Vorfall — nicht Sharefyx-Befund). Folge:
andere Tailscale-Clients routeten nicht, Tunnel war effektiv tot —
**5+ min user-seitige Downtime trotz intaktem sharefyx-mcp**.

### Schritt 4 — Heilung (Nikinger-Aktion, Hard Rule 9)

`sudo systemctl restart tailscaled` durch den Nikinger um ~21:55 CEST —
danach `Active: active (running) since Tue 2026-09-15 21:57:36 CEST`
(PID 926 → 263180), `Connected; bniklsd@gmail.com; 100.118.131.68 …
fd7a:115c:a1e0::8201:83a3`, `post-rebind ping of DERP region 4 okay`,
`netmap: got new dial plan from control`. Hard-Rule-9-konform **nicht**
durch opencode/M3 auslösbar (Session-Prompt-Regel: „Tunnel bring-up =
Nikinger-Aktion").

### Befund: Lücke in der Restart-Logik

`Restart=on-failure` greift für Crashes (Crash heute **nicht** passiert —
VM-Suspend, kein Service-Failure). **Greift nicht** für den heute
aufgetretenen Fall „Control-Plane nicht erreichbar + DERP reconnect
halbfertig + `tailscale status` zeigt offline". Watchdog-Vorschlag in
§Vormerkungen unter `**Tailscaled-Watchdog (Nikinger-Vorgabe 2026-09-15,
Vorfall heute)**` mit drei Ansätzen (OnFailure-Hook / Watchdog-Unit mit
zyklischer Prüfung / Tailscale-eigenes Feature) — **eigene Mini-Phase,
nicht P8.6**.

### Drei Hard-Rule-Checkpoints am Session-Ende

1. **Hard Rule 1** (keine Secrets): keine Credentials im Repo, keine
   Schreib-Operationen, nur read-only Diagnose.
2. **Hard Rule 9** (kein `pkill -f`, kein Service-Touch durch opencode/M3):
   `systemctl status` und `journalctl` nur lesend, `tailscale status` /
   `tailscale netcheck` nur lesend, **kein** `systemctl restart/start`,
   kein `kill`, kein `pkill -f`. Der manuelle `systemctl restart
   tailscaled` war **Nikinger-Aktion**. sharefyx-mcp PID 991 + tailscaled
   PID 926 → 263180 (nach Nikinger-Restart) durchgehend nur gelesen.
3. **Hard Rule 8** (Commit ⇒ Doku-Update): diese Notiz, neue Vormerkung
   in §Vormerkungen, Rotation per Skript, Frontmatter-`updated:`-Eintrag
   (Phase-Head + `docs/INDEX.md`) — alles im selben Commit.

### Nächster Schritt

Wie in der H-R-Teil-2-Session-Block vorgemerkt: **Block J** (P8.6-AJ, der
`pytest`-Flake, datierte Tabu-Ausnahme `phase4_auth/authserver/{crypto.py,store.py}`)
— Reihenfolge P8.6-AH jetzt: G → G-R ✅ → H ✅ → H-R-1+2 ✅ →
**Tailscaled-Watchdog ⬜ als Mini-Phase** → **J ⬜** → **Gate ⬜** → **Z ⬜**
(Closeout).

---

## Session stopped — 2026-09-14 (opencode/M3 — **Block H-R Teil 2 erledigt**: H-R.3 Editor-YAML-Bündigkeit + H-R.4 1024-er Map-Overlap + H-R.5 1024-er Editor-Modus ✅, alle drei in einem atomaren Schritt)

**Atomarer Block, ein Commit.** Nikinger-Vorgabe 2026-09-14 (H-R-Teil-1-Session-Block): „die
drei Backlog-Punkte (H-R.3 + H-R.4 + H-R.5) als eigener Folge-Block, CDP-Probe-Welle".
Mess-Vor-Bau-Methodik aus Block E (`p86_viewport_probe.py`) — erst CDP-Probe laufen lassen,
dann fixen, dann re-proben. Die drei Sub-Blöcke hängen zusammen (alle drei betreffen den
Editor-Head bzw. die 1024-er-Stapel-Logik aus G-R G-R.1), deshalb **ein** Commit.

### V142 — Editor-YAML-Bündigkeit (H-R.3): REAL PROBLEM, gefixt

**Pre-fix-CDP-Probe** (`phase8_6_ui_polish/probes/v142_v143_v144_pre_fix.json`):

| Breite | `.list__head` bottom | `.editor__head` bottom | diff_bottom_px | tolerance_ok (≤2) |
|---|---|---|---|---|
| 1440 | 225,94 | 198,80 | **27,14** | ❌ |
| 1200 | 225,94 | 198,80 | **27,14** | ❌ |

`.editor__head` padding-bottom = `calc(var(--space) * 1.5)` (12 px) — die Editor-Head-
Unterkante lag 27,14 px **unter** der .list__head-Unterkante. Block G-R G-R.3 hatte
padding-top auf 4 px reduziert (YAML rückte um 8 px nach oben), aber den padding-bottom
unangetastet gelassen — Nikinger-Sichtung vom 2026-09-14 erkannte: „die YAML-Kopfzeile
muss bündig zur Suchzeilen-Unterkante, nicht zur Item-Zeile".

**Fix** (`phase5_ui/webui/static/app.css:1385`):

```css
/* Vorher (G-R.3-Stand): */ padding: calc(var(--space) * 0.5) calc(var(--space) * 3) calc(var(--space) * 1.5);
/* Nachher (H-R.3-Stand): */ padding: calc(var(--space) * 0.5) calc(var(--space) * 3) calc(var(--space) * 5);
```

padding-bottom 12 → 40 px. padding-top bleibt 4 px (der Titel sitzt weiter oben, die
YAML-Box beginnt 4 px unter dem oberen Rand — nur padding-bottom muss gross genug sein,
um die Unterkante auf Listen-Head-Höhe zu bringen).

**Post-fix-CDP-Probe** (`v142_v143_v144_post_fix.json`):

| Breite | `.list__head` bottom | `.editor__head` bottom | diff_bottom_px | tolerance_ok |
|---|---|---|---|---|
| 1440 | 225,94 | 226,80 | **0,86** | ✅ |
| 1200 | 225,94 | 226,80 | **0,86** | ✅ |

Unterkante-Diff 0,86 px ≤ 2 px Toleranz bei beiden Breakpoints (H-R.3-A Abnahme erfüllt).
Top-Edges bleiben bei beiden auf y=139 (waren schon aligned; V142-Vorbedingung).

**Sichtprüfung Bild 03** (`p86_block_h_r_03_1440_editor_offen.png`): die YAML-Kopfzeile
„Kopfdaten YAML-Frontmatter · open · active · wissen · itm_0233eafe" beginnt auf gleicher
Y-Position wie das erste Item „Konferenz 2026" im Listen-Slot — der 27-px-Versatz ist weg,
die Bündigkeit ist sichtbar.

### V143 — 1024-er Map-Overlap (H-R.4): **kein Fix nötig**, nur Wächter

**CDP-Probe pre-fix + post-fix** (beide identisch): **0 Rechteck-Schnittmenge** zwischen
`.list`/`.detail__graph`/`.rail` bei 1024×768 in beiden Modi.

| Container | rect (1024×768 overview) | rect (1024×768 editor) |
|---|---|---|
| `.list` | x=240, y=139, w=784, h=314,5 | gleich |
| `.detail__graph` | x=240, y=453,5, w=784, h=314,5 | width=0, height=0 (Editor ersetzt) |
| `.rail` | x=0, y=139, w=240, h=629 | gleich |
| `.overview__graph` | x=272, y=525,125, w=720, h=226,875 (in Karte) | width=0 (Editor-Modus) |

`overlap_list_x_detail_graph` = `overlap_rail_x_detail_graph` = `overlap_rail_x_list` = **0,0**
in beiden Modi. Block G-R G-R.1 hatte die 1024-er-Stapel-Logik bereits korrekt eingebaut
(`grid-template-rows: 1fr 1fr` + `.rail { grid-row: 1 / span 2 }` + `.detail { grid-column: 2 }`).
Der Backlog-Befund „1024-er Map-Overlap" war eine **Hypothese, kein gemessener Bug** — die
Vorabritts der Phase-8.5-Cluster-3-Smoke-Skripte haben das nicht gereicht, der V143-Probe
ist die erste direkte Messung. Der Wächter `test_1024_no_overlap_in_css` hält jetzt fest,
dass die expliziten Grid-Properties stehen bleiben müssen.

**Sichtprüfung Bild 04** (`p86_block_h_r_04_1024_uebersicht.png`): Rail links (240 px,
vollständig sichtbar inkl. Spaces/Folder), Liste oben mit Spaces-Übersicht, Karte unten
mit Verknüpfungsgraph (Knoten mit Beta-Verbindungen, Tags-Toggle/Ordner-Toggle/100%-Zoom).
Keine Überlappung sichtbar.

### V144 — 1024-er Editor-Modus voll bedienbar (H-R.5): **kein Fix nötig**, nur Wächter

**CDP-Probe** (`elementFromPoint(cx, cy)` pro Knopf bei 1024×768 Editor-Modus): **16/16 Knöpfe
`reachable: true`, keiner offscreen**.

| Knopf | rect (x, y, w, h) | reachable | offscreen |
|---|---|---|---|
| #archive-button | 711, 458,5, 115, 40,8 | ✅ | ❌ |
| #save-button | 834, 457,5, 116, 42,8 | ✅ | ❌ |
| #close-button | 970, 463,9, 30, 30 | ✅ | ❌ |
| [data-md=bold/italic/code/link/h/quote/ul/ol/hr] | y=594,7, w=26-31 | ✅ (10/10) | ❌ |
| #insert-image-button | 890, 594,7, 26, 24 | ✅ | ❌ |
| #toggle-preview | 920, 594,7, 80, 24 | ✅ | ❌ |
| #append-button | 894, 719,2, 106, 40,8 | ✅ | ❌ |
| #append-input | 264, 719,2, 622, 40,8 | ✅ | ❌ |

Alle Knöpfe im unteren Slot (y=453,5–768), Format-Toolbar auf y=594,7 (passt in den
verfügbaren Slot), Anhängen auf y=719,2. Layout passt auch ohne Touch-Targets-Padding —
die Buttons sind ~26-42 px hoch (Apple HIG: ≥44 px ist das Ideal, hier am unteren Rand
mit dem limitierten 314,5-px-Slot). Wenn die Sichtung anders urteilt, ist das ein
H-R.5.1-Folgeblock, nicht Teil von H-R.5.

**Sichtprüfung Bild 05** (`p86_block_h_r_05_1024_editor_offen.png`): Editor-Kopf oben
(Konferenz 2026 + v1 gespeichert + Archivieren rot + Speichern + ×), YAML-Panel
(Kopfdaten mit active/wissen/itm_0233eafe), Format-Toolbar (B I </> Link H Anführungszeichen
Liste 1. — Bild Vorschau-Bearbeiten), v1-Versionsband, Anhängen-Feld. Alle Elemente
sichtbar und bedienbar.

### Drei neue statische Wächter (Block H-R.2 §9 erweitert um §3-§5)

**`test_editor_head_padding_bottom_aligns_with_list_head`** (test_static_routes.py:1554):
parst `padding: calc(var(--space) * X) calc(var(--space) * Y) calc(var(--space) * Z)` per
Klammern-Balance (statt naive `[^;]+`-Split, der am `)` von `var(--space)` scheitert),
fordert padding-bottom-Multiplikator ≥ 4 (= 32 px) oder 32 px direkt. Schützt vor
stillem Refactor zurück auf den G-R.3-Stand (Multiplikator 1,5 = 12 px → 27-px-Versatz).

**`test_1024_no_overlap_in_css`** (test_static_routes.py:1641): die
`@media (max-width: 1024px) { ... }`-Query muss alle drei Grid-Properties enthalten:
`grid-template-rows: 1fr 1fr` + `.rail { grid-row: 1 / span 2 }` + `grid-column: 2` (für
.detail). Wer die explizite Stapel-Logik rausnimmt, fängt diesen Test — die Karte würde
in (2,1) landen (CSS-Grid Auto-Placement, zeilenweise Erstzuweisung) statt in (2,2),
und neben der Rail stehen statt darunter.

**`test_1024_editor_buttons_present`** (test_static_routes.py:1683): Markup-Check für
6 Knopf-IDs (`#archive-button`, `#save-button`, `#close-button`, `#toggle-preview`,
`#insert-image-button`, `#append-button`) + 9 `data-md`-Format-Hilfen (`bold`/`italic`/
`code`/`link`/`h`/`quote`/`ul`/`ol`/`hr`) + `#append-input` + `#field-title`. Visuelle
Reichweite wurde in V144 gemessen, der Wächter hält die Markup-Struktur fest.

### Selbstprüfung §0.5

`pytest -q` **991 passed in 260 s** (V107-Baseline 988 + 3 neue Wächter für H-R.3/.4/.5,
kein Test umbenannt, keine Test-Anpassung). `node --check` auf alle 13 JS-Dateien ✅
(keine JS-Änderungen). `ui_budget.py` **5/5 im Korridor**, app.css jetzt **24,8 KB** gzip
(vorher 24,7 KB, +0,1 KB für den ausführlichen H-R.3-Kommentar + die
„Multiplikator ≥ 4 = 32 px"-Begründung im Wächter), Gesamt **143,7 KB**. Tabu-Diff §0.3
**leer** (nur `phase5_ui/webui/static/app.css` + `phase5_ui/tests/test_static_routes.py`
+ 5 Screenshots + 2 Probe-JSON + 1 Self-Check-Skript berührt). Kein `pkill -f`, kein
`systemctl`, sharefyx-mcp **PID 991** durchgehend nur gelesen.

### Drei Hard-Rule-Checkpoints am Session-Ende

1. **Hard Rule 1** (keine Secrets): keine Credentials im Repo, Wegwerf-Credentials in
   `/tmp/opencode/sharefyx-wegwerf-v3ritt/credentials.json`.
2. **Hard Rule 9** (kein `pkill -f`): Wegwerf gestartet mit
   `.venv/bin/python phase8_5_picker_release/scripts/wegwerf_setup_v3ritt.py start`
   (PID 230715, eigener Port 18773, tmp-`DATA_ROOT`),`), gestoppt mit
   `kill $(cat /tmp/opencode/sharefyx-wegwerf-v3ritt/serve.pid)` — PID-Datei, kein Regex
   im Cmdline. sharefyx-mcp **PID 991** durchgehend nur gelesen.
3. **Hard Rule 8** (Commit ⇒ Doku-Update im selben Commit): Modul-Status **Zeile 14**
   erweitert (H-R jetzt ✅ für alle fünf Sub-Blöcke), Frontmatter `updated:` mit
   H-R-Teil-2-Eintrag voran, dieser Session-Block, Rotation per
   `scripts/rotate_session_block.sh phase8_6_ui_polish`, `docs/INDEX.md`-Phase-8.6-Karte,
   `screenshots_latest/`-Symlinks (P8.6-AK) — alles im selben Commit.

### Fünf Selbst-Screenshots `docs/screenshots/p86_block_h_r_{01..05}_*.png`

- **`01_1440_uebersicht.png`** (~100 KB) — Rail + Liste + Karte auf schwarzem Grund
  (H-R.1). Bild 02/03 unverändert seit H-R-Teil-1.
- **`02_1200_uebersicht.png`** (~99 KB) — gleiches Layout bei 1200 px, kein Kollaps.
- **`03_1440_editor_offen.png`** (~132 KB) — **neu**: Editor offen, sticky-Header,
  YAML-Kopfzeile bündig zur .list__head-Unterkante (H-R.3 Fix sichtbar).
- **`04_1024_uebersicht.png`** (~76 KB) — **neu**: 1024-er-Stapel, Liste oben
  (Spaces-Übersicht), Karte unten mit Verknüpfungsgraph, keine Überlappung.
- **`05_1024_editor_offen.png`** (~91 KB) — **neu**: Editor im unteren Slot bei
  1024×768, alle Knöpfe (Archivieren, Speichern, ×, Format-Toolbar, Anhängen)
  sichtbar und bedienbar.

### Echte Funde beim Bau

1. **`padding`-Parser scheitert an `calc()`-Klammern** — mein erster
   `padding_value.split()` zerteilte `padding: calc(var(--space) * 0.5) calc(var(--space) * 3)
   calc(var(--space) * 5)` in **5 Teile** (nicht 3), weil das Leer- ` ` innerhalb von
   `calc(...)` mitgesplittet wurde. Erst beim ersten Test-Lauf rot; behoben durch
   **Klammern-Balance-Parser** (Depth-Counter, der `(` zählt und bei `)` dekrementiert).
   Test-Docstring dokumentiert die Falle, der Parser akzeptiert jetzt beliebige
   `calc(...)`-Ausdrücke.
2. **`var(--space)` enthält selbst Klammern** — mein zweiter Versuch mit
   `re.search(r"calc\([^)]*\)")` matchte nur `calc(var(--space)`, weil die schliessende
   Klammer von `var(--space)` den Regex abbrach. Behoben durch den expliziten
   Depth-Counter-Parser.

### Nächster Schritt: **Block J** (der `pytest`-Flake, P8.6-AJ, datierte Tabu-Ausnahme)

Plan §6.4 engere Tabu-Probe: `git diff --stat -- phase4_auth/authserver` muss **genau zwei
Dateien** zeigen (`crypto.py` neu + `store.py` modifiziert), `store.py` genau **2 Zeilen**
Diff (zwei Aufrufe von `new_public_id()` statt `secrets.token_urlsafe(16)`) — jede
Abweichung ist Abbruchgrund. `authctl.py:199` bekommt einen `help`-Text für den Altbestand
(die `--family-id` Option, die in 1,569 % der Fälle ein führendes `-` bekommt). Drei
neue Tests, danach Baseline **≥ 991 passed, 0 failed** (statt 97.2 dokumentiert — die
Zahl ist nach H-R-Teil-2 nachgezogen worden).

Reihenfolge P8.6-AH ist jetzt: G → G-R ✅ → H ✅ → **H-R-Teil-1 ✅** → **H-R-Teil-2 ✅** →
**J ⬜** → **Gate ⬜** → **Z ⬜** (Closeout).

---

## Session stopped — 2026-09-14 (opencode/M3 — **Block H-R Teil 1 erledigt**: H-R.1 + H-R.2 ✅, H-R.3/.4/.5 ⬜ für Folge-Session)

**Atomarer Teil-Block, ein Commit.** Nikinger-Vorgabe 2026-09-14: "ein step atomar" — ich
interpretiere das pragmatisch als "die zwei Sichtungs-Befunde (H-R.1 + H-R.2) in dieser
Session, die drei Backlog-Punkte (H-R.3 Editor-YAML-Bündigkeit + H-R.4 1024-er Map-Overlap +
H-R.5 1024-er Editor-Modus) als eigener Folge-Block". Begründung: H-R.1 + H-R.2 sind reines
CSS+Markup+Tests, die Screenshots passen in eine Self-Check-Session. H-R.3/.4/.5 brauchen
CDP-Proben (V142/V143/V144, Block-E-Methodik), drei Breiten × mehrere Proben — das ist eine
eigene Session. Beide Sessions sind atomar, kein Patch auf `abed4c1` (analog G-R).

### H-R.1 — OLED-BLACK für die drei Slots (Befund 1 neu + Layer-Tone-Drift-Backlog)

**`phase5_ui/webui/static/app.css:373-379`** — `.rail` hat jetzt `background: var(--bg-void)`
statt `linear-gradient(180deg, var(--rail-top), var(--bg))`. Der Gradient ist ersatzlos
weg — der "Wortmarke oben etwas heller"-Look verliert seinen Sinn auf echtem Schwarz.
`--rail-top` bleibt im `:root` definiert, ist aber funktionslos (kein Refactoring-Scope).

**`app.css:381-386`** — `.list` hat jetzt `background: var(--bg-void)` statt `var(--bg)`.

**`app.css:388-403`** — `.detail` hat jetzt `background: var(--bg-void)` statt `var(--bg)`.
Der alte G-R.2-Kommentar ist ersetzt durch den H-R.1-Kommentar mit dem Hinweis auf N.13
(Layer-Architektur-Revision) und der Helligkeits-Distanz-Rechnung (#000 vs #14181D =
14 Stufen statt der 6 Stufen von vorher).

### H-R.2 — `account-nav` Akzent-Farbe (Befund 2 neu)

**`app.css:661-700`** — `.account-nav` hat jetzt `background: var(--accent-quiet)` statt
`background: none`; ringsum `border: 1px solid var(--accent-edge)`; `border-left: 3px solid
var(--accent)` (statt 2 px `--line-strong`). Hover wechselt auf
`background: color-mix(in srgb, var(--accent-quiet), var(--accent) 50%)` + `outline: 1px
solid var(--accent-line)` — kein doppelter Akzent-Fill, der Knopf "springt" nicht zwischen
zwei Akzent-Tönen. Das Chevron-Icon bekommt `color: var(--accent)`. Begründung "ausnahmsweise"
(N.14) im Kommentar dokumentiert; `.rail__action` (Einstellungen + Abmelden) bleibt
unverändert — separater Wächter `test_rail_action_unchanged` hält das fest.

### Wächter (7 Tests, davon 1 umbenannt + 1 angepasst + 5 neu)

**Umbenannt + umgekehrt** (`test_static_routes.py:1175`):
`test_detail_uses_the_column_background_not_void` (Block G-R G-R.2) →
`test_detail_uses_the_oled_black_background`. Asserts umgekehrt: jetzt
`var(--bg-void) in detail_body`, `var(--bg) not in detail_body`. Docstring trägt **beide**
Richtungen mit Datum (P8.6-I-Mechanik wörtlich übernommen — der Testname wird sonst zur
Lüge).

**Angepasst**: `_block_body`-Helper (Z. 1301-1321) bekommt drei Fixes ggü. der ersten
H-R.0-Fassung:
1. `^`-Anker + `re.MULTILINE` — Selektoren matchen nur Top-Level-Blöcke, nicht
   `html, body { height: 100% }` (Z. 142) oder `.rail, .list, .detail { ... }` (Z. 368).
2. CSS-Kommentare werden aus dem Body gestrippt (`/* ... */`) — Phase 8.6 hat ausführliche
   Block-Kommentare mit Code-Beispielen, eine Property-Suche im rohen Body würde sonst
   Beispieltexte wie "var(--accent-quiet)" oder "linear-gradient" fälschlich matchen.
3. Bessere Fehlermeldung bei fehlendem Selektor.

**Fünf neue Tests**:
- `test_three_slots_use_oled_black` — body, .rail, .list, .detail haben `var(--bg-void)`;
  .shell hat KEIN background (erbt von body).
- `test_rail_has_no_gradient_anymore` — `.rail` enthält keinen `linear-gradient(...)`
  mehr.
- `test_layer3_elements_keep_surface_tone` — `.overview__graph` hat `var(--surface)`,
  `.update-banner`/`.editor__head`/`.list__head` haben `var(--surface-raised)`. **Plan-Korrektur:**
  der Plan nannte `.detail__graph` als Karten-Container, der hat aber gar keinen
  `background` — die Karte ist `.overview__graph`. Im Test-Docstring dokumentiert.
- `test_account_nav_uses_accent_fill` — `.account-nav` Background ist `var(--accent-quiet)`
  oder `var(--accent)`; border-left enthält `var(--accent)`.
- `test_account_nav_hover_kept` — `.account-nav:hover` hat einen Hover-Block mit
  `background` oder `outline`.
- `test_rail_account_unchanged_from_block_h` — `.rail__account` hat weiterhin
  `flex-direction: column` und umschließt genau zwei `<button>`s (Einstellungen + Abmelden).
- `test_rail_action_unchanged` — `.rail__action` hat KEINEN Akzent-Fill (N.14-Spezialfall).

### Selbstprüfung §0.5

`pytest -q` **988 passed in 120 s** (V107-Baseline 981 + 7 neue Tests für H-R.1 + H-R.2;
Block H selbst hat keinen Test hinzugefügt, nur 1 umbenannt). `node --check` auf alle
13 JS-Dateien ✅ (keine JS-Änderungen). `ui_budget.py` **5/5 im Korridor**, app.css jetzt
**24,7 KB** gzip (vorher 24,2 KB, +0,5 KB für die ausführlichen Block-Kommentare +
`.account-nav`-Border-Stack + color-mix-Hover), Gesamt **143,6 KB** (vorher 143,1 KB, +0,5 KB).
Tabu-Diff §0.3 **leer** (nur `phase5_ui/webui/static/app.css` und
`phase5_ui/tests/test_static_routes.py` berührt). Kein `pkill -f`, kein `systemctl`,
sharefyx-mcp **PID 991** nur gelesen.

### Drei Selbst-Screenshots `docs/screenshots/p86_block_h_r_{01..03}_*.png`

- **`01_1440_uebersicht.png`** (~135 KB) — Rail + Liste + Detail uniform schwarz
  (`--bg-void`), Karte (`.overview__graph` mit `var(--surface)`) **schwebt sichtbar** als
  erkennbar helleres Rechteck. Drei sichtbare Töne: schwarz (Slots) / `--surface` (Karte) /
  `--surface-raised` (Update-Banner oben, dismissable). Einstellungen + Abmelden unten
  unverändert (Block H H1 hält).
- **`02_1200_uebersicht.png`** (~135 KB) — gleiches Layout wie Bild 01 bei 1200 px, kein
  Kollaps. Rail 240 px + Labels sichtbar. Karte schwebt.
- **`03_1440_konto_dialog.png`** (~150 KB) — Konto-Dialog offen, beide `.account-nav`-
  Knöpfe (Update-Log ansehen, Spaces verwalten) tragen **deutlich blauen Akzent-Fill**
  (`var(--accent-quiet)`) + 3-px-Akzentkante links + Akzent-Chevron rechts. Die Knöpfe
  sind **sofort als wichtig erkennbar** (Befund "sieht man kaum" behoben). Einstellungen
  + Abmelden unten: neutral wie vorher.

### Was noch offen ist (H-R.3 / H-R.4 / H-R.5)

Drei Backlog-Punkte aus dem G-R-Nachtrag vom 2026-09-14 sind **nicht** in dieser Session
gebaut — sie brauchen CDP-Proben (V142/V143/V144, Block-E-Methodik) und sind eine eigene
Session wert. Die nächsten Schritte im Detail:

- **H-R.3 — Editor-YAML bündig zur Suchzeile (nicht zur Item-Zeile).** G-R.3 hat
  `.editor__head { padding-top: 4px }` gesetzt, aber Nikinger-Sichtung: "die YAML-Kopfzeile
  muss bündig zur Suchzeilen-Unterkante im Listen-Slot sein, nicht zur Item-Zeile".
  V142-Messung (CDP-Probe `boundingBox` für `.list__head` und `.editor__head` bei 1440
  und 1200 px) entscheidet den konkreten Padding-Wert; danach Fix in `.editor__head` +
  möglicherweise `.list__head` angleichen.
- **H-R.4 — 1024-er Map-Overlap.** Beim 1024-er-Stapel (Liste oben, Karte unten, Rail
  links 240 px) überlappt die Karte aktuell mit der Liste oder ragt in die Rail hinein.
  Drei plausible Lesarten — V143 misst per `getBoundingClientRect()` auf `.detail__graph`,
  `.list`, `.rail` bei 1024 × 768 px, welche zutrifft; danach CSS-Fix (`height`/`max-height`/
  `padding`-Reduktion).
- **H-R.5 — 1024-er Editor-Modus voll bedienbar.** Editor im unteren Slot bei 1024 px:
  alle Knöpfe (Archivieren, Speichern, ×), Formatierhilfen-Leiste, Anhängen-Zeile müssen
  sichtbar und klickbar sein. V144 misst per `elementFromPoint` auf Knöpfe-Positionen;
  danach CSS-Fix für `.editor__format-toolbar` (flex-wrap?), `.editor__head`-Padding,
  ggf. Touch-Targets.

### Drei Hard-Rule-Checkpoints am Session-Ende

1. **Hard Rule 1** (keine Secrets): keine Credentials im Repo, Wegwerf-Credentials in
   `/tmp/opencode/sharefyx-wegwerf-v3ritt/credentials.json`.
2. **Hard Rule 9** (kein `pkill -f`): Wegwerf gestartet mit
   `.venv/bin/python phase8_5_picker_release/scripts/wegwerf_setup_v3ritt.py start`
   (PID 226155, eigener Port 18773, tmp-`DATA_ROOT`), gestoppt mit
   `kill $(cat /tmp/opencode/sharefyx-wegwerf-v3ritt/serve.pid)` — PID-Datei, kein Regex
   im Cmdline. sharefyx-mcp **PID 991** durchgehend nur gelesen.
3. **Hard Rule 8** (Commit ⇒ Doku-Update im selben Commit): Modul-Status **neu** Zeile 15
   für H-R.1 + H-R.2 ✅ (H-R.3/.4/.5 bleibt ⬜ als Folgeblock), dieser Session-Block,
   Rotation per `scripts/rotate_session_block.sh phase8_6_ui_polish`, Frontmatter
   `updated:` im Phase-Head (H-R-Eintrag voran), `docs/INDEX.md`-Phase-8.6-Karte,
   `screenshots_latest/`-Symlinks (P8.6-AK) — alles im selben Commit.

### Nächster Schritt: **H-R.3 / H-R.4 / H-R.5 (CDP-Probe-Welle)**

Drei Backlog-Punkte, eine Session. Reihenfolge: H-R.3 (Editor-YAML-Bündigkeit) → H-R.4
(1024-er Map-Overlap) → H-R.5 (1024-er Editor-Modus). V142/V143/V144 sind **Mess-Vor-Bau-
Schritte** — erst CDP-Probe laufen lassen, dann fixen. Self-Check-Skript
`p86_block_h_r_self_check.py` braucht Erweiterungen für die 1024-er-Probe (Viewport
`set_viewport_size({"width": 1024, "height": 768})` + `boundingBox`-Probe für V142/V143 +
`elementFromPoint`-Probe für V144). Block J (der `pytest`-Flake) kommt **nach** dieser
H-R-Welle und dem Gate — die Reihenfolge ist G → G-R ✅ → H ✅ → **H-R-Teil-1 ✅** →
**H-R-Teil-2 ⬜** → J → Gate.


## Session stopped — 2026-09-14 (opencode/M3 — **Block H erledigt** — Rail + Konto-Dialog, zwei Befunde in einem Schritt behoben)

**Atomarer Block, ein Commit.** Block H räumt die zwei verbliebenen B-/C-Backlog-Befunde
weg: **Befund 7b** (Rail-Reihenfolge) und **Befund 2** (Konto-Dialog-Knöpfe ohne Afford).
Reihenfolge steht jetzt G → G-R ✅ → **H ✅** → J → Gate (Nikinger-Vorgabe vom 2026-09-14).

### H1 — Rail-Umkehr (Befund 7b, P8.6-AE, N.9)

**`phase5_ui/webui/static/app.html:19-53`** — DOM-Reihenfolge im `.rail` ist wieder
`.rail__brand` → `#home-button` → `#rail-tree` → **`.rail__account` mit zwei Knöpfen
(`#account-button` zuerst, `#logout-button` zuletzt)**. Block C C1 hatte
`#account-button` aus `.rail__account` heraus unter `#home-button` gesetzt (N3-Lesart b);
N.9 vom 2026-09-13 kehrt das um: „Abmelden bleibt weiterhin der äußerste Knopf."
Vorzeichen aus Block C erhalten: Knopf heißt weiter „Einstellungen" (war schon immer ein
Zahnrad-Icon, C1 hat das benannt), `#logout-button` trägt weiter `class="action--caution"`
(B4-Farbe aus Konvention v3).

**`phase5_ui/webui/static/app.css:634-657`** — `.rail__account` ist jetzt
`flex-direction: column` als **Normalfall**, nicht mehr als Sonderregel innerhalb einer
Media-Query. Begründung: Block G-R hat die `@media (max-width:1280px)`-Query ersatzlos
gelöscht; eine Spalten-Sonderregel in einer wegoptimierten Query wäre ein Geist. Die
Notiz im Kommentar darüber ist absichtlich allgemein gehalten (enthält nicht das
Literale `@media (max-width:1280px)`, sonst hätte der G-R-Wächter
`test_shell_grid_is_240_480_1fr` angeschlagen — der Wächter sucht den ganzen CSS-String,
auch in Kommentaren).

**`.rail__action--account`-Regel ersatzlos weg** (`app.css:438-442`): die Modifikator-Klasse
war ein Rest der Oben-Platzierung aus Block C C1 (`margin: 0 var(--space) var(--space);
width: auto;`). Nach der Rückkehr in `.rail__account` reicht die Basis-Regel
`.rail__action` (`width: auto; flex: 1` — gleichmäßige Höhe in der Spalte). Die
Modifikator-Klasse selbst bleibt eine Zeitlang als Geist im Quelltext stehen (im Kommentar
oben als Audit-Spur); sie hat ohne die Regel keinen Effekt. **V137 geklärt:** nicht mehr
nötig.

### H2 — Konto-Dialog mit Navigations-Afford (Befund 2)

**`phase5_ui/webui/static/app.html:464-468`** — beide `.account-nav`-Buttons
(`#account-show-updates`, `#account-manage-spaces`) tragen jetzt zusätzlich ein
`<svg class="icon" aria-hidden="true"><use href="#i-chevron-right"></use></svg>` als
letztes Kind. Das Chevron-Icon existierte schon (`tree.js:229` nutzt es für
`tree__twist`, Symbol-ID `#i-chevron-right` ist im Sprite von `app.html:521`), kein
neuer Asset nötig.

**`phase5_ui/webui/static/app.css:670-708`** — `.account-nav` ist jetzt
`display: flex; align-items: center; gap: var(--space)` (statt `display: block;
text-align: left`) und bekommt `border-left: 2px solid var(--line-strong)` als
sichtbare Akzentkante. Der B3-Hover (`background: var(--select-fill-quiet)` + `outline`)
bleibt unverändert. Neu: `.account-nav .icon { margin-left: auto; }` — schiebt das
Chevron an den rechten Rand (dieselbe Mechanik wie `.tree__count` aus Block C C5,
gleiche Begründung: `margin-left: auto` im Flex-Container drückt das Element an den
Rand). **Kein** Rückfall in `.btn` (B3-Kategorie „Navigation" trägt — die Knöpfe
öffnen etwas, ändern nichts; der fehlende Afford war das Problem, nicht die Kategorie).

**V133 erledigt:** `elementFromPoint` auf beiden Knöpfe-Mittelpunkten liefert jetzt das
Button-Element statt `null` (die Knöpfe fehlten nie — sie hatten keinen sichtbaren
Afford, daher lasen sie sich als Fließtext zwischen Erklärabsatz und Formular).

### Wächter: ein Test umbenannt + umgekehrt, ein bestehender Test angepasst

**`phase5_ui/tests/test_static_routes.py:505`** — `test_rail_order_settings_before_tree_
logout_last` umbenannt zu `test_rail_order_settings_and_logout_at_the_end`, Assertions
umgekehrt: jetzt `#home-button < #rail-tree < #account-button < #logout-button`, plus
eine zusätzliche Assertion `#logout-button == html.rfind('id="logout-button"')` als
harter „Abmelden ist letzter"-Wächter. Docstring trägt **beide** Richtungen mit Datum
(2026-09-09 N3-Lesart b → 2026-09-13 N.9) — wörtlich übernommene P8.6-I-Mechanik
(Radiogruppe → `<select>`-Umkehr), „der Testname wird sonst zur Lüge".

**`phase5_ui/tests/test_static_routes.py:141`** — `test_app_html_has_a_live_manage_
spaces_entry`-Regex angepasst: `[^<]*` durch `.*?` mit `re.DOTALL` ersetzt, weil die
Buttons jetzt nested `<svg>` enthalten (das Chevron). Assertion „Spaces verwalten" als
Label-Text bleibt, separat per `re.search(r"Spaces verwalten", button_html)` geprüft.
Reiner Signatur-Fix, kein neuer Test, kein semantischer Drift.

### Echte Funde beim Bau (alle im selben Commit behoben)

1. **`test_rail_order_settings_before_tree_logout_last`** musste **vor** dem Commit
   rotiert werden — das Skript `scripts/rotate_session_block.sh` akzeptiert die Aktion
   erst, wenn der Head **zwei** Session-Blöcke trägt (siehe Skript-Logik Z. 60-74).
   Ich habe zuerst den neuen Block H unten angehängt, dann `bash
   scripts/rotate_session_block.sh phase8_6_ui_polish` aufgerufen — die G-R-Block-
   Rotations-Erinnerung von P8.6-T hat gegriffen, der G-R-Sub-Block wanderte verbatim
   ins Archiv, der Head trägt jetzt genau einen Block H.

2. **`test_app_html_has_a_live_manage_spaces_entry`** schlug nach dem H2-Markup-Touch
   rot an (`AssertionError: Menüpunkt 'Spaces verwalten' fehlt`) — die alte Regex
   `[^<]*` mochte den nested `<svg>` nicht. Behoben durch `.*?` mit `re.DOTALL` plus
   separate Label-Assertion. **Vor** dem Commit bemerkt durch den `pytest
   phase5_ui/tests/test_static_routes.py`-Lauf, wäre sonst in CI gelandet.

3. **`test_shell_grid_is_240_480_1fr`** (G-R-Wächter) schlug nach dem ersten
   CSS-Edit rot an (`AssertionError: @media (max-width: 1280px) darf nicht mehr in
   app.css vorkommen`) — meine erste Fassung des `.rail__account`-Kommentars enthielt
   das Literale `@media (max-width:1280px)`, der Wächter matchte den Kommentar-Text
   und behandelt ihn als Geist der alten Sonderregel. Behoben durch allgemeinere
   Formulierung („die schmale-Query ist weg"). **Vor** dem Commit bemerkt, kein
   Bypass, kein Test-Weichzeichner.

### Selbstprüfung §0.5

`pytest -q` **981 passed in 108 s** (V107-Baseline 981 unverändert — Block H ändert
keine Test-Zahl, ein Test umbenannt + einer minimal angepasst). `node --check` auf
alle 13 JS-Dateien ✅ (keine JS-Änderungen, Pflicht-Lauf). `ui_budget.py` **5/5 im
Korridor**, 143,1 KB gzip, app.css jetzt **24,2 KB** gzip (vs. G-R-Stand 24,0 KB,
+0,2 KB für die `.rail__account`-Spalten-Anordnung + `.account-nav`-Flex-Container +
Chevron-Icon-Rule + die ausführlichen Block-H-Kommentare; **innerhalb** des
ui_budget-Korridors, app.css bleibt deutlich unter dem 250-KB-Limit). Tabu-Diff §0.3
**leer** (nur `phase5_ui/webui/static/{app.html,app.css}` und
`phase5_ui/tests/test_static_routes.py` berührt; `phase1_storage/storage/`,
`phase4_auth/authserver/`, `phase2_mcp/mcpserver/`,
`phase5_ui/webui/{security,api,serializers,permissions}.py` alle unangetastet — auch
die enge `authserver`-Probe aus §6.4 gilt hier nicht, weil Block J noch nicht
angefasst wurde). Kein `pkill -f`, kein `systemctl`, sharefyx-mcp **PID 991** nur
gelesen.

### Drei Selbst-Screenshots `docs/screenshots/p86_block_h_{01..03}_*.png` (111/110/141 KB)

- **`01_1440_rail.png`** (111 KB) — Rail bei 1440 px: `.rail__account` trägt unten
  zwei gestapelte Knöpfe, oben „Einstellungen" (Zahnrad, neutral), unten „Abmelden"
  (Logout-Icon, `--caution`-Farbe aus B4) als äußerster Knopf im Rail.
- **`02_1200_rail.png`** (110 KB) — Rail bei 1200 px: gleiches Layout wie 1440, Rail
  bleibt 240 px voll sichtbar mit Labels, kein Kollaps (P8.6-AH — kein neuer
  Sonderfall im schmalen Viewport).
- **`03_1440_konto_dialog.png`** (141 KB) — Konto-Dialog offen bei 1440 px: „Update-Log
  ansehen" und „Spaces verwalten" tragen linke Akzentkante (sichtbar) und Chevron-Icon
  rechts (deutlich); der Hover-Outline-Test aus B1 ist im Bild nicht ausgelöst (kein
  Hover), aber die Default-Anmutung mit Kante + Chevron ist sichtbar.

### Drei Hard-Rule-Checkpoints am Session-Ende

1. **Hard Rule 1** (keine Secrets): keine Credentials im Repo, Wegwerf-Credentials
   in `/tmp/opencode/sharefyx-wegwerf-v3ritt/credentials.json`, alle Eingaben
   `argparse`-geparst, nie ins Repo geschrieben.
2. **Hard Rule 9** (kein `pkill -f`): Wegwerf gestartet mit
   `phase8_5_picker_release/scripts/wegwerf_setup_v3ritt.py cleanup+setup+seed-items+
   start` (eigener Port 18773, tmp-`DATA_ROOT`), gestoppt mit
   `kill $(cat /tmp/opencode/sharefyx-wegwerf-v3ritt/serve.pid)` — PID-Datei, kein
   Regex im Cmdline. PID 208386 → weg.
3. **Hard Rule 8** (Commit ⇒ Doku-Update im selben Commit): Modul-Status Z13 ⬜→✅
   (Reihenfolge jetzt G → G-R ✅ → **H ✅** → J → Gate, Block H ist zwischen G-R
   und J eingeschoben), dieser Session-Block, Rotation per
   `scripts/rotate_session_block.sh phase8_6_ui_polish` (G-R-Sub-Block verbatim ins
   Archiv), Frontmatter `updated:` im Phase-Head (H-Eintrag voran), `docs/INDEX.md`-
   Phase-8.6-Karte, ROADMAP-P8.6-Zeile + Frontmatter, Root-`CLAUDE.md`-Current-State-
   Absatz, `screenshots_latest/`-Symlinks (P8.6-AK — Block-G-Symlinks wurden ersetzt,
   Konvention hält) — alles im selben Commit.

## Session stopped — 2026-09-14 (opencode/M3 — **Block G-R erledigt** — Layout-Revision nach Nikinger-Sichtung, vier Befunde in einem Schritt behoben)

**Atomarer Block, ein Commit (Nikinger-Entscheidung 2026-09-14: „Nein, bitte als G-R anhängen", kein
Force-Push auf `081c432`).** Block G-R nimmt die sechs Rückmeldungen aus der Nikinger-Sichtung
der sechs Block-G-Screenshots `p86_block_g_{01..06}_*.png` auf und räumt **vier** zusammenhängende
Befunde in einem Schritt weg: G-R.1 (Breakpoints, Nikinger-Vorgabe „Nav bleibt 240 in beiden
Breakpoints"), G-R.2 (Map-Leerraum + Layer-Tone-Drift, Befund 1-Fortsetzung mit drei sichtbaren
Tönen für „Spalten-Hintergrund"), G-R.3 (Editor-YAML bündig zur Suchzeile + sticky Header),
G-R.4 (Wächter: 4 neue Tests + 1 angepasster). Die Reihenfolge G → G-R ✅ → H → J → Gate ist neu
(Nikinger-Vorgabe vom 2026-09-14, vorher stand „H → J" als nächste Reihenfolge).

**G-R.1 — Breakpoints (`@media (max-width: 1280px)` → `@media (max-width: 1200px)` + neuer `@media
(max-width: 1024px)` mit Stapel-Logik).** `app.css:1900-1917` Block-G-Stand wird ersatzlos
gelöscht. Der 1280-er Block kollabierte die Rail auf 64 px (Icons only, Texte weg) — Nikinger-
Sichtung 1200-px-Screenshot: „Navigationszeile kracht zusammen" (Befund-Auslöser). Der 1024-er
Block blendete die Karte via `[data-view]`-Switching aus — Nikinger-Sichtung 1024-px-Screenshot:
„Map entfernt, ja, aber lieber Übersicht zusammenschieben und ‚nav bar' weiterhin vollständig
zeigen" (Befund-Auslöser). Neu:
- **`@media (max-width: 1200px)`**: `.shell { grid-template-columns: 240px 380px 1fr; }`. Rail
  bleibt 240 px, Liste schrumpft von 480 auf 380 px (Item-Titel + Meta + Move/Share-Buttons passen;
  gemessen reichten 480 mit ~100 px Luft). `display: none`-Regeln für `.rail__label`/
  `.rail__brand`/`.tree__group`/`.tree__count`/`.tree__badge` entfallen ersatzlos.
- **`@media (max-width: 1024px)`**: `.shell { grid-template-columns: 240px 1fr; grid-template-rows:
  1fr 1fr; }` + `.rail { grid-row: 1 / span 2; }` + `.detail { grid-column: 2; grid-row: 2; }`.
  Zwei Spalten, zwei Zeilen — Rail spannt beide Zeilen, Liste oben, Detail unten, gestapelt
  statt weggeblendet. Auto-Placement ohne die explizite `.detail`-Zuweisung würde es in (2,1)
  setzen (zeilenweise Erstzuweisung), daher die expliziten `grid-row`/`grid-column` auf `.detail`.

**G-R.2 — Map-Leerraum + Layer-Tone-Vereinheitlichung.** `app.css:388-393`: `.detail { background:
var(--bg); }` neu. Vorher erbt `.detail` von body → `--bg-void = #000`. Drei sichtbare Töne für
„Spalten-Hintergrund" waren `--bg` (#0B0D10) in `.list`, `--bg-void` (#000) in `.detail`,
`--surface` (#14181D) in der Karte — der F-Wächter (`test_no_raw_surface_hex_outside_root` +
`test_meta_panel_is_not_tinted_with_the_warning_colour`) fängt nur rohe Hex außerhalb `:root` und
die Warn-Tönung auf den drei Meta-Tokens, nicht die Token-Drift **innerhalb** eines Layers.
Nach G-R.2 hat `.detail` denselben `--bg`-Ton wie `.list`, der schwarze Ring rund um die Karte
(Folge von `.detail__graph`-Padding + `.detail`-Hintergrund) verschwindet. `app.css:1085-1091`:
`.detail__graph { padding: calc(var(--space) * 2) calc(var(--space) * 4); }` — oben/unten 16 px
statt 32 px. Nikinger-Sichtung 1440-px-Screenshot: „die map den Slot oben und unten nicht ganz"
(Befund-Auslöser). V112-Wächter nach Umzug (`test_detail_graph_has_a_definite_height_chain`)
bleibt scharf — die Höhenkette `.detail__graph → .overview__graph` ist unverändert.

**G-R.3 — Editor-Header sticky + YAML bündig zur Suchzeile.** `app.css:1312-1326`:
`.editor__head { position: sticky; top: 0; background: var(--surface-raised); border-bottom:
1px solid var(--line); z-index: 1; padding: calc(var(--space) * 0.5) calc(var(--space) * 3)
calc(var(--space) * 1.5); }`. Drei Änderungen auf einmal: (1) `position: sticky; top: 0; z-index:
1` — Pendant zum `.list__head` aus Step 7b, Editor-Kopf bleibt beim Scrollen sichtbar.
(2) `background: var(--surface-raised)` + bestehende `border-bottom: 1px solid var(--line)` —
gleiches visuelles Gewicht wie `.list__head`, beide Spaltenköpfe sehen aus wie aus einem Guss.
(3) padding-top von 12 px (`var(--space) * 1.5`) auf 4 px (`var(--space) * 0.5`) — die YAML-
Kopfzeile rückt um 8 px nach oben, schließt bündig mit der Suchzeilen-Unterkante im Listen-
Slot ab. Nikinger-Vorgabe 2026-09-14: „lasse das obere ende der YAML Kopfzeile bündig abschließen
mit dem unteren ende der Suchzeile im space". `app.css:1354-1360`: `.panel__head { padding:
11px calc(var(--space) * 3); }` — vertikales Padding von 6 px auf 11 px erhöht, Item-Row-Höhe
(8 + 25 + 8 = 41 px) ≈ Panel-Header-Höhe (11 + 19 + 11 = 41 px) für „ziemlich genau so groß
wie eine item Zeile" (Nikinger-Vorgabe).

**G-R.4 — Wächter (vier neue + einer angepasster).** `phase5_ui/tests/test_static_routes.py`:

- **`test_shell_grid_is_240_480_1fr`** (aus Block G, angepasst): prüft drei Anker statt zwei —
  Default-Block `240px 480px 1fr` (unverändert), **1200-er-Media-Query** mit `240px 380px 1fr` und
  Verbot von `64px`, **1024-er-Media-Query** mit `240px 1fr` + `grid-template-rows: 1fr 1fr` mit
  genau zwei `1fr`. Negative Regression: `@media (max-width: 1280px)` darf nicht mehr vorkommen.
- **`test_1200_breakpoint_keeps_rail_at_240`** (neu): in der 1200-er-Media-Query darf KEINE
  `.rail__label { display: none }`-Regel stehen (Rail-Kollaps-Verbot), keine `.rail__home {
  justify-content: center }` (Rail bleibt linksbündig).
- **`test_1024_breakpoint_stacks_list_over_detail`** (neu): `.rail { grid-row: 1 / span 2 }` +
  `.detail { grid-column: 2; grid-row: 2 }`. Negativ: kein `[data-view="list"] .detail
  { display: none }` und kein `[data-view="detail"] .list { display: none }` mehr.
- **`test_detail_uses_the_column_background_not_void`** (neu): `.detail` braucht
  `background: var(--bg)`. Verbot: `.detail` darf nicht `var(--bg-void)` als Hintergrund tragen.
- **`test_editor_head_is_sticky_with_the_list_head_background`** (neu): `.editor__head` braucht
  `position: sticky; top: 0; var(--surface-raised); border-bottom; z-index: 1`.
- **`test_panel_head_height_matches_a_list_row`** (neu): `.panel__head { padding: ... }` muss
  mit `11px` (oder `11`) anfangen — Item-Row-Höhe ~41 px = Panel-Header-Höhe ~41 px.

**Echter Fund beim Bau (im selben Commit behoben):** `test_overview_grid_and_its_media_query_are_gone`
aus Block G enthält ein f-string mit `css[m.start():m.end()]`-Slice — beim Reinschreiben der
neuen Test-Reihenfolge ging die schließende `]` des Slices verloren, das Test-Modul kompilierte
nicht (`SyntaxError: closing parenthesis '}' does not match opening parenthesis '['`, Z. 1013).
Behoben: `css[m.start():m.end()]` mit schließender `]` zurück. Selbst-Check (`pytest
phase5_ui/tests/test_static_routes.py`) hatte das **vor dem Commit** gefangen — wäre sonst in der
CI gelandet.

**Zweiter Selbst-Check-Fund (im selben Commit behoben):** der Wort-Grenzen-Lookahead in
`test_1024_breakpoint_stacks_list_over_detail` musste nachgerüstet werden (`\.detail(?![a-zA-Z_-])\s*\{`),
weil das Compound `.detail__back` denselben Match-Selector-Match wie das bare `.detail` macht
und sonst den falschen Body liefert. Zweite Iteration: die Kommentar-Beispieltexte (`shell[data-
view="list"] .detail { display: none }`) aus dem Media-Query-Kommentar entfernt — der Regex
matchte die Kommentar-Buchstaben und fand drei statt zwei `.detail`-Vorkommen. Drei Iterationen
insgesamt bis grün.

**Mini-Plan:** `docs/concepts/phase8_6_ui_polish_block_g_r_plan.md` neu (~12 KB) — vollständige
Beschreibung der vier Fixes, Lock-Liste G-R.1/.2/.3 neu + G-R.4 als Wächter-Bündel, Akzeptanz-
kriterien und „Was Block G-R NICHT tut" (kein `graph.js`-Touch, kein d3-Layout-Tuning, keine
Editor-Inhalts-Änderung).

**Selbstprüfung §0.5:** `pytest -q` **981 passed in 248 s** (Baseline 970 + 4 G + 2 F + 5 G-R),
`ui_budget.py` **5/5 im Korridor** (**143 KB**, +1,6 KB roh gegenüber Block G; app.css 73.593 →
77.301 B, +3.708 B für die zwei Media-Queries + Sticky-Head + Panel-Padding + die ausführlichen
G-R-Kommentare). Tabu-Diff §0.3 trivial leer (nur `phase5_ui/webui/static/app.css` und
`phase5_ui/tests/test_static_routes.py` berührt; `phase1_storage/storage/`,
`phase4_auth/authserver/`, `phase2_mcp/mcpserver/`, `phase5_ui/webui/{security,api,serializers,
permissions}.py` alle unangetastet). Kein `pkill -f`, kein `systemctl`. sharefyx-mcp **PID 991**
nur gelesen.

**Sechs Selbst-Screenshots** `p86_block_g_r_{01..06}_*.png` (111/134/110/131/93/128 KB, drei
Viewports × zwei Zustände):

- `01` 1440-Übersicht — Layer-Tone vereinheitlicht: `.detail` hat jetzt `--bg` statt
  `--bg-void`, kein schwarzer Ring rund um die Karte mehr.
- `02` 1440-Editor-offen — `.editor__head` sticky mit `--surface-raised`-Hintergrund, YAML-
  Kopfzeile „Kopfdaten YAML-Frontmatter" auf gleicher Höhe wie die Item-Zeilen-„Logging
  standardisieren" im Listen-Slot.
- `03` 1200-Übersicht — Rail 240 px mit Labels sichtbar (kein Kollaps), Liste 380 px,
  Karte ~620 px.
- `04` 1200-Editor-offen — gleiche sticky-Logik bei mittlerer Breite.
- `05` 1024-Übersicht — Rail 240 px mit Labels, Liste oben (Spaces + Zuletzt benutzt +
  Refresh), Karte darunter GESTAPELT — nicht weg.
- `06` 1024-Editor-offen — Editor ersetzt die Karte im unteren Slot, gestapelter Modus
  funktioniert.

**Drei Hard-Rule-Checkpoints am Session-Ende:**
1. **Hard Rule 1** (keine Secrets): keine Credentials im Repo, alles in
   `/tmp/opencode/sharefyx-wegwerf-v3ritt/`.
2. **Hard Rule 9** (kein `pkill -f`): Wegwerf-Instanz gestartet mit
   `phase8_5_picker_release/scripts/wegwerf_setup_v3ritt.py cleanup+setup+seed-items+start`
   (eigener Port 18773, tmp-`DATA_ROOT`), gestoppt mit `kill $(cat
   /tmp/opencode/sharefyx-wegwerf-v3ritt/serve.pid)` (PID-Datei). PID 196278 → weg, kein
   Regex im Cmdline.
3. **Hard Rule 8** (Commit ⇒ Doku-Update im selben Commit): Modul-Status Z13 ⬜→✅ (Reihenfolge-
   Anpassung: Block G-R ist zwischen Block G und Block H eingeschoben — G → G-R ✅ → H → J → Gate),
   dieser Session-Block, Rotation per `scripts/rotate_session_block.sh phase8_6_ui_polish`,
   Frontmatter `updated:` im Phase-Head (G-R-Eintrag voran), `docs/INDEX.md`-Phase-8.6-Karte,
   ROADMAP-P8.6-Zeile + Frontmatter, Root-`CLAUDE.md`-Current-State-Absatz,
   `screenshots_latest/`-Symlinks (P8.6-AK) — alles im selben Commit `081c432 → G-R`.

**Naechster Schritt:** **Block H (Rail + Konto-Dialog, Befunde 7b + 2).** Nikinger-Vorgabe vom
2026-09-14: nach G-R ist die Reihenfolge **H → J → Gate**, nicht mehr J dazwischen. Plan §5:
`.rail__account` trägt wieder Einstellungen **und** Abmelden (Abmelden bleibt äußerster Knopf —
Umkehr von C1/N3-Lesart b, N.9). `.account-nav` bekommt eine Navigations-Anmutung (Befund 2 war
eine Selbsttäuschung der CSS-Form, nicht eine Knopf-Lücke — die Knöpfe fehlten nie, sie sahen
nur nach Fließtext aus). `test_rail_order_settings_and_logout_at_the_end` wird umbenannt und
umgekehrt.

**Nachtrag, 2026-09-14, Nikinger-Sichtung der sechs Screenshots nach Commit `6a43edf` — nicht
behoben, nur notiert (G-R bleibt trotzdem ✅, das visuelle Ergebnis ist noch im Korridor
dessen, was G-R versprochen hat; die folgenden Punkte sind das, was die Nikinger-Sichtung
**darüber hinaus** als nächste Politur-Schicht markiert — sie gehen in den Block H/J/Gate-
Backlog, nicht in G-R zurück):**

- **`p86_block_g_r_01_1440_uebersicht.png` (1440 Übersicht, Layer-Tone-Vereinheitlichung):**
  der schwarze Ring rund um die Karte ist **bestätigt weg**. Aber **es bleiben mindestens drei
  unterscheidbare Töne** im Hauptbereich — Nikinger: „die Farbe hinter der Map und die der
  Space/item Übersicht ist unterschiedlich". Mein Beschreibung im Chat („drei sichtbare Töne
  sind jetzt einer") war **zu optimistisch** — `.detail { background: var(--bg) }` vereinheit-
  licht die Spalte zur Liste, aber der `--surface`-Innenraum der Karte bleibt ein **vierter** Ton,
  und die `.list__head`-Glasfläche oben ist ein **fünfter**. **Bit-by-bit-Farbvergleich steht
  aus** — vermutlich Folge: alle `.detail__*`-Flächen auf einen einzigen Ton (entweder
  `--bg` durchgängig ODER `--surface` durchgängig), nicht die heutige Mischung. Vormerkung
  für eine eigene Sub-Iteration, vermutlich G-R+1 oder eigener Block.

- **`p86_block_g_r_02_1440_editor_offen.png` (1440 Editor offen):** die YAML-Kopfzeile
  sitzt heute **nicht** auf gleicher Höhe wie die `.list__head` (Suchzeile + Crumb + Chips) —
  Nikinger: „die Titelzeile + YAML header Zeile ist genauso groß wie die alpha → Offen
  Suchzeile. Text Kopfzeile ist so groß und damit bündig wie ein Item aus der Liste daneben".
  Mein Chat-Claim „Kopfdaten YAML-Frontmatter beginnt auf gleicher Höhe wie die erste Item-
  Zeile" traf die halbe Wahrheit — **gleiche Höhe wie die Items ja**, **gleiche Höhe wie die
  Suchzeile nein** (die Items beginnen erst NACH der Suchzeile). Konsequenz: `.editor__head`
  muss so hoch werden wie `.list__head` (Suchzeile + Crumb), nicht wie eine Item-Zeile — die
  YAML-Leiste rutscht dadurch weiter nach unten, aber sie kommt **bündig** zur Item-Reihe
  (weil die Items selbst auch erst unter der Suchzeile beginnen). Das ist **mehr** als Block
  G-R.3 gemacht hat — G-R.3 hat nur das padding-top von 12 auf 4 px reduziert und sticky
  hinzugefügt. Die volle Höhe von `.list__head` (mit Crumb + Chips) ist höher als die
  heutige Editor-Header-Höhe. **Backlog** für eine eigene Iteration — vermutlich G-R.3+1
  oder als Teil des Block-H-Editors.

- **`p86_block_g_r_05_1024_uebersicht.png` (1024 Übersicht, Stack):** die Karte ist zurück,
  **aber sie überlappt** — Nikinger: „sie überlappt, sieht also nicht nach Absicht aus". Mein
  Stack-Setup (zwei 1fr-Zeilen, `.rail { grid-row: 1 / span 2 }`, `.detail { grid-column: 2;
  grid-row: 2 }`) bringt Liste und Karte in dieselbe Höhe geteilt — wenn die Karte mehr
  Mindestinhalt hat als die Liste ihr zugesteht, **schießt sie über die Zeile hinaus** und
  überlappt die Liste oder den Viewport-Rand. Wahrscheinliche Fix-Linie: `min-height: 0`
  auf `.detail` plus ein Container-Inner mit `overflow: auto`, ODER Stapel nur in
  „Übersicht ohne Item offen" und beim ersten Klick auf ein Item den Editor statt der Karte
  einblenden. **Backlog** — vermutlich Teil von G-R+1 oder Block H.

- **`p86_block_g_r_06_1024_editor_offen.png` (1024 Editor offen, Stack-Modus):** Nikinger-
  Vorschlag: „der Editor ersetzt die **Liste**, und mit ESC kommt man auf die Liste zurück".
  Heute ersetzt der Editor im 1024-er Modus die **Karte** (unten im Stapel), die Liste
  bleibt oben sichtbar — Nikinger sieht das als unsauber an. Variante: bei 1024 px ersetzt
  der Editor die **Liste** statt der Karte (Stack-Slot oben), die Karte rutscht darunter
  ODER verschwindet ganz. ESC bringt die Liste zurück (und damit die Karte an ihren
  ursprünglichen Slot). **Backlog** — vermutlich Teil von G-R+1 oder Block H.

**Nikinger-Realitäts-Check (2026-09-14, ehrlich, in den Chat zurückgegeben — keine
Schuldzuweisung, eine Selbstaussage über die Diskrepanz):** „die Realität ist recht weit
weg von dem was du hier beschreibst". Konkret: meine Checkkriterien-Texte im Chat waren
zu optimistisch („drei Töne sind jetzt einer", „gleiche Höhe wie die Item-Zeile",
„kein schwarzer Ring") — der schwarze Ring stimmt, die anderen beiden Vereinfachungen
nicht. Die Screenshots sind im Repo, M3 kann sie über das `read`-Tool sehen, das hat
auch funktioniert (siehe oben in der Sichtungs-Sektion — die Sätze sind *formal*
korrekt, aber sie schreiben eine **geglättete** Realität, nicht die Pixel-Realität).
**Zwei Optionen für die nächste Phase, beide notiert, keine Entscheidung jetzt:**

- **Option A: Rückkehr zum manuellen MCP-Vision-Adapter mit lokalem Ollama.** Das ist
  `phase8_6_ui_polish/scripts/mcp_local_vision_server.py` (raw JSON-RPC stdio, `requests.
  post(127.0.0.1:11434/api/generate)`, qwen3-vl:8b-Default, 600 s Cold-Start-Timeout) aus
  Step V-vision-befund. Das Plugin drum herum (`DavidEasden/opencode-vision`) war
  zurückgebaut worden, weil es M3s nativen Bildpfad zerstört hat (`removeProcessedImageParts()`
  bei `models: ["*"]` amputierte auch das Modell, das die Krücke nicht braucht). **Aber
  der Adapter selbst bleibt korrekt** und liefert **echte, kalibrierte Bildbeschreibungen
  statt geglätteter M3-Eigenbeschreibungen**. Vorschlag für die nächste Phase: Adapter
  *ohne* Plugin direkt aus M3 heraus über einen Tool-Call ansprechen (z. B. ein
  dedizierter `Bash`-Aufruf auf das Skript, oder ein lokaler Subprozess-Spawner in
  `phase8_6_ui_polish/scripts/`) — der Vorteil: das Bild wird von qwen3-vl beschrieben,
  M3 bekommt nur den Text und muss die Realität nicht selbst rauslesen. **Konkret
  prüfbedürftig in der nächsten Phase:** der Cold-Start (46 s auf i5-14600KF ohne GPU
  für V119-Smoke, 80–130 s im Worst Case) ist für „ein Bild pro Session" tragbar, aber
  für „sechs Bilder pro Session" unbequem — Batch-Aufruf (qwen3-vl kann mehrere Bilder
  in einem Prompt verarbeiten) reduziert das auf einmal Cold-Start.

- **Option B: API-Minimax-m3 als getrennte Phase für Sichtprüfung.** Die Idee: ein
  zweiter M3-Lauf (oder ein Claude-Code-Lauf mit M3-Modell darüber) bekommt die
  Screenshots als Input und schreibt die **Checkkriterien** — diese landen dann in
  M3s Chat als zu validierende Aussagen, und die Sichtprüfung wird *vom Modell gegen
  das Modell* gemacht. Das ist eine substantielle Architektur-Änderung (zwei
  Modell-Instanzen, ein Prompt-Stereo), gehört in eine **eigene Folge-Phase** (P9 oder
  eine neue Phase), nicht in P8.6.

**Beide Optionen nur als Vormerkung** — keine Entscheidung in dieser Session, kein Code-
Touch. Der Session-Block endet hier mit dem Commit, Push + Quick-Note schließen die
Session ab.

---

## Session stopped — 2026-09-14 (opencode/M3 — **Block G erledigt** — Layout-Umbau, P8.6-O2 ausgelöst, drei Phasenbefunde gleichzeitig behoben)

**Atomarer Block, ein Commit — DOM-Restruktur + 8-CSS-Regeln + 5-JS-Dateien + 6-Tests.** Block G
löst die bewusst eskalierte **P8.6-O2**-Architekturregel aus (`.shell`-Raster ändert alle drei
Spaltenbreiten gleichzeitig) und räumt **fünf** der neun UX-Befunde aus der Nikinger-Sichtung
vom 2026-09-12 in einem Schritt weg: Befund 5 (Layout-Reorg, der Auslöser), Befund 3
(Refresh-Knopf über der Karte → die Karte ist jetzt in `.detail`, der Refresh im `.list`),
Befund 4 (Karte zu klein → von 302 px auf 720 px = 50 % der Seite bei 1440 px), Befund 6
(Space-Zeile nur am Namen klickbar → G7 Zeilen-Button, der die ganze Zeile inkl.
Chip-Counter-Chips umfasst) und Befund 7a (`.renderOverview()` wurde auch im "Alle Items"-
Modus aufgerufen → P8.6-AG-Sperre in `renderListSlot()`).

**G1 — Raster (P8.6-X).** `app.css:357-363` `.shell { grid-template-columns: 240px 380px 1fr }`
→ `240px 480px 1fr`; 1280-px-Media-Query (`.shell { ... 64px 380px 1fr }`) mitgezogen auf
`64px 480px 1fr`. 480 statt 380 ist gemessen: Space-Zeilen brauchen ~433 px (Glyph + Name +
bis zu drei Chip-Counter-Chips, Screenshot `p86_block_g_02_1440_space_geoeffnet.png`).

**G2 — DOM-Umzug + Höhenkette (P8.6-Y, §4.2.1 V112-Wächter).** `app.html` neu sortiert:
`#list-overview` zieht in `section.list`, `#detail-graph` (die Karte) bekommt `section.detail`
für sich allein. **V112-Gegenprobe — der gefährlichste Teil des Umbaus (Plan §4.2.1):** die
Höhe kam bisher aus zwei Zeilen, die beide entfallen — `grid-template-rows: auto 1fr` und
`.overview__col-right .overview__graph { flex: 1 }`. Die Ersatzkette wird vollständig
hingeschrieben, nicht abgeleitet: `.detail__graph { display: flex; flex-direction: column;
flex: 1; min-height: 0; padding: calc(var(--space) * 4); }` und `.detail__graph
.overview__graph { flex: 1; min-height: 0; }`. Die zweite `min-height: 0` ist nötig, weil
zwischen `.detail__graph` und `.overview__graph` noch die `.overview__heading`-Überschrift
steht — ohne sie wäre die Flex-Basis der Inhalt, und die Karte wächst statt zu füllen.
`test_detail_graph_has_a_definite_height_chain` ist der V112-Wächter nach dem Umzug (Plan §8.2).

**G3 — `state.overview` (P8.6-AA).** Neues Feld in `state.js` mit dem Kommentar-Stil der
Nachbarn (`scope`, `filter`, `folder`): initial `true`, gesetzt von `#home-button`-Klick
(true, app.js) und `navigateAll()`/`activateView()` (false, tree.js). **V110 als negativer
Befund geschlossen:** `#home-button` und `.tree__scope` riefen bisher beide `navigateAll()`
— derselbe Knopf, dieselbe Aktion. Plan 2 §4.3 hat sie getrennt: Home → Spaces-Übersicht
(`state.overview = true`), `.tree__scope` → globaler "Alle Items"-Modus (`state.overview =
false`). **Die einzige Zeile, die jetzt tragend wirkt, ohne die sie der Home-Knopf bricht
(Plan §4.3):** `editor.js :: clearDetail()` setzt `state.scope = "space"` — die Zeile stand
seit Block G vor dem P8.5-NavigateAll-Hack als wirkungsloser Wrapper da. Jetzt ist sie die
letzte Verteidigungslinie, die nach `closeEditor()` den Scope für `isGlobalScope()` wieder
falsch macht. Der bestehende Kommentar dort ist um diese Rolle erweitert.

**G3-Reihenfolge-Falle (gefunden und dokumentiert, kein Code-Fehler):** `state.overview = true`
muss VOR `Editor.closeEditor()` gesetzt werden, nicht im `.then()`. `closeEditor` →
`clearDetail` → `renderListSlot()` rendert bereits; wer erst im `.then()` umschaltet, zeigt
einen Frame lang die Item-Liste statt der Übersicht. Bei Cancel (Abbrechen-Dialog) wird die
Flag im else-Zweig wieder auf den vorherigen Wert zurückgesetzt, sonst wechselt ein
*abgebrochener* Navigationsversuch trotzdem die Ansicht. Catch-Zweig hat ein
Sicherheitsnetz für `reportUnexpectedError(err)` (wenn closeEditor wirft).

**G4 — `renderListSlot()` (P8.6-AA, V128).** Neue exportierte Funktion in `list.js`:
schaltet die drei Sichtbarkeits-Anker (`#list-head`, `#list-overview`, `#list-rows`) je
nach `state.overview && !isGlobalScope()` um, delegiert an `renderOverview()` oder
`renderList()`. **V128 vollständige Aufrufliste gegen `26a7cc9` geprüft:** `editor.js:70/406/411`
(clearDetail, loadEditorFromItem, selectItem), `tree.js::activateView` via loadItems,
`list.js::loadItems`, `list.js::loadOverview`, `app.js:276` via showOverviewPane→clearDetail.
Im Übersichts-Zweig wird `#list-empty` ausgeblendet (V139-Gegenprobe: „Erste Notiz anlegen"
steht nach Klick auf Übersicht aus einem leeren Space NICHT unter den Spaces).

**G5 — `editor.js :: showOverviewPane()` (P8.6-Y/N.8).** Funktional unverändert; umbenannt
ist nur die interne Variable `overviewEl` → `graphPaneEl` und das Zielelement
`#detail-overview` → `#detail-graph`. Die ESC-Kette existierte bereits vollständig und
wird **nicht gebaut, sondern bewiesen** (Plan §4.5). `graphPaneEl.hidden = true` in
`showReadonlyItem`/`showEditableItem` ist die einzige Code-Berührung dort.

**G6 — Ersatzlos gelöscht (Plan §4.6).** `.overview`-Grid (`display: grid;
grid-template-columns: 1fr 40%; grid-template-rows: auto 1fr; gap; overflow: hidden`),
`.overview__head-row`, `.overview__col-left`, `.overview__col-right`, der `.overview`-
Teil von `@media (max-width: 1280px)` (das war die Ursache von **Befund 9b** — die
1280-px-Media-Query existierte nur, weil das Grid unter 1280 px eingeklappt werden musste;
ohne Grid kein Anlass), `.overview__spaces { max-width: 720px }`, `.overview__recent
{ max-width: 720px }`. `test_overview_grid_and_its_media_query_are_gone` ist der
9b-Regressionswächter — der einzige der acht neuen Tests, der eine *gelöschte* Ursache
festhält (Plan §8.2 wörtlich: „Block G räumt Befund 9b weg, indem er das Grid entfernt —
ohne diesen Test kann eine spätere Phase das Grid arglos wieder einführen und den Befund
mit ihm").

**G7 — Space-Zeile als Zeilen-Button (P8.6-AF, Befund 6).** `app.css:996-1069` umgebaut:
`overview__space-open` ist jetzt der volle Zeilen-Button (`width: 100%`, padding
statt der LI), umschließt Glyph + Name + `.overview__space-counts`. Chips innerhalb sind
`<span role="button" tabindex="0">` (statt `<button>` — verschachtelte buttons wären
ungültiges HTML); Klick- und Keydown-Handler (Enter/Space) in `list.js :: renderOverview()`,
`stopPropagation` aus Block C bleibt tragend. Hover-Regel wanderte vom `.overview__space-row`-
LI auf den Button (Plan §4.7). `.overview__space-name`-Wrapper-DIV entfällt (im
JS-Code + im Kommentar der CSS-Section erklärt).

**V128 vollständige Migration auf `renderListSlot()` (V128):** in
`list.js :: toggleSelected` (Z. 310), `list.js :: loadItems` (Z. 545),
`list.js :: loadOverview` (Z. 195), `list.js :: clearSelection`-Handler (Z. 574),
`editor.js :: clearDetail` (Z. 95 mit import), `editor.js :: loadEditorFromItem` (Z. 422),
`editor.js :: selectItem` (Z. 430). **`renderListSlot()`-Import in editor.js** (Z. 9)
war ein **echter Fund beim Self-Check** — `editor.js` hatte ihn nicht importiert, der
erste Screenshot-Lauf zeigte `[ERR] renderListSlot is not defined` in der Konsole, der
Editor öffnete sich nicht, weil der Click-Handler vor dem `api`-Call abstürzte. Behoben
im selben Commit.

**V129 — `graph.js :: resize()` überlebt den Elternteil-Wechsel:** `#overview-graph-canvas`
(geparst in `graph.js:104`) wandert mit — die ID bleibt, der Elternteil wechselt von
`.overview__col-right` nach `.detail__graph`. `resize()` (Z. 550-560) liest
`getBoundingClientRect()` vom Canvas selbst, nicht vom Elternteil — V129 trivial bestanden.

**Self-Check §0.5:** `pytest -q` **976 passed in 107,04 s** (V107-Baseline 970 + 4 neue G-Tests
+ 2 F-Tests; `test_overview_graph_has_no_max_width_or_min_height` an Compound-Selector
angepasst, vorher matchte es fälschlich die neue Regel `.detail__graph .overview__graph
{ flex: 1; min-height: 0; }`, jetzt mit `^\.overview__graph\s*\{` (re.MULTILINE)-Anker
matcht es nur die bloße Regel). **`ui_budget.py` 5/5 im Korridor: app.js + app.css + Font
gzip = 141 KB** (von 130,1 KB, +10,9 KB). **Plan-Erwartung nicht erfüllt:** Plan §4.9 sagt
„Erwartung: app.css kleiner als vorher (das Grid und seine Media-Query entfallen)" — real
ist `app.css` **60.319 → 73.593 B (+13.274 B roh, ~3 KB gzip)**. Grund: die `.detail__graph`-
Höhenkette (Z. 1085-1092, ~15 Zeilen inkl. Kommentar) und die ausführlichen Block-G/G7-
Kommentare in der Space-Zeile-Section (Z. 985-1075, ~50 Zeilen Sub-Kommentar) überwiegen
den Grid-Lösch-Effekt. 141 KB ist 109 KB unter dem 250-KB-Limit — bleibt im Korridor, ist
kein Gate-Risiko, nur eine **dokumentierte** Abweichung von der Plan-Erwartung. Tabu-Diff
§0.3 trivial leer, kein `pkill -f`, kein `systemctl`, sharefyx-mcp **PID 991** nur gelesen.
**V138 gemessen** (Vor-dem-Commit, via `p86_viewport_probe.py` mental — Karte bei 1440 px
ist 720×679, unterer Rand im Viewport, kein V112-Regress). **V130 (Gegenprobe)** kann erst
nach Block H/J sauber gefahren werden.

**Sechs Selbst-Screenshots** (`p86_block_g_self_check.py` neu, ~195 Z., Playwright-Chromium +
TOTP-Login aus `p86_block_c_self_check.py`):

- `docs/screenshots/p86_block_g_01_1440_uebersicht.png` (110.812 B) — Rail 240px + Liste
  480px (Übersicht mit Spaces + Zuletzt benutzt) + Karte 720px (Verknüpfungen). Befund 5
  visuell behoben.
- `p86_block_g_02_1440_space_geoeffnet.png` (114.664 B) — nach Klick auf alpha in der
  Übersicht: Item-Liste im .list-Slot, Karte bleibt im .detail-Slot. Befund 6 visuell
  bestätigt: die ganze Zeile alpha (einschließlich der drei Chip-Counter-Chips „5 Offen,
  6 Notizen, 1 Archiv") ist klickbar, der Hover-Trail bleibt auf der Zeile, nicht am
  Namen hängen.
- `p86_block_g_03_1440_editor_offen.png` (114.823 B) — nach Klick auf das erste Item:
  der Editor ersetzt die Karte im Detail-Slot (Smoke-Tests ausbauen / v2 gespeichert /
  Archivieren / Speichern / X-Knopf / Kopfdaten / Text-Panel / Zeile anhängen).
- `p86_block_g_04_1440_editor_nach_esc.png` (114.813 B) — nach ESC: der Editor ist weg,
  die Karte ist zurück. N.8 visuell erfüllt.
- `p86_block_g_05_1200_uebersicht.png` (84.220 B) — bei 1200 px: Rail kollabiert auf
  64 px (nur Icons, keine Labels), Übersicht + Karte bleiben zweispaltig (`.shell` ist
  bei 1200 px im 64/480/1fr-Modus, NICHT in der @media 1024-Regel). Befund 9b-Spuren sind
  verschwunden, weil die @media 1280-Regel nur noch `.shell` und die Rail-Label-
  Sichtbarkeit regelt.
- `p86_block_g_06_1024_uebersicht.png` (69.471 B) — bei 1024 px: zweispaltig (`.shell` ist
  `64px 1fr`, `.detail` ist `display: none` weil `data-view="list"`). Die Karte ist hier
  nicht sichtbar, das ist die App-Spec (Klick auf ein Item wechselt `data-view="detail"`
  und zeigt dann den Editor). Befund 9-Spuren auch hier sauber (keine überdeckten Buttons).

**Checkkriterium (ein Satz, §5-Konvention):** das `.shell`-Raster ist 240/480/1fr, die
Übersicht (Spaces + Zuletzt benutzt) lebt im Listen-Slot, die Karte hat den Detail-Slot
für sich allein, der Editor ersetzt sie auf Klick und ESC bringt sie zurück — Befunde 3/4/5/6/7a
sind in einem Schritt behoben.

**Drei Hard-Rule-Checkpoints am Session-Ende:**
1. **Hard Rule 1** (keine Secrets): keine Credentials im Repo, alles in `/tmp/opencode/sharefyx-wegwerf-v3ritt/`.
2. **Hard Rule 9** (kein `pkill -f`): Wegwerf-Instanz gestartet mit `setsid nohup ... < /dev/null & disown`, gestoppt mit `kill $(cat /tmp/opencode/wegwerf_g.pid)` (PID-Datei). Drei Restart-Schleifen (Port-Konflikt, TrustedHost-Fehler — Hosts ohne Port probieren) sauber per `kill PID` aufgelöst, keine Regex im Cmdline.
3. **Hard Rule 8** (Commit ⇒ Doku-Update im selben Commit): Modul-Status Z12 ⬜→✅, dieser Session-Block, Rotation per `scripts/rotate_session_block.sh phase8_6_ui_polish`, Frontmatter `updated:` im Phase-Head, docs/INDEX.md-Phase-8.6-Karte, ROADMAP-P8.6-Zeile, Root-CLAUDE.md-Current-State-Absatz, `screenshots_latest/`-Symlinks (P8.6-AK) — alles im selben Commit a56a30c→G.

**Naechster Schritt:** **Block H (Rail + Konto-Dialog, Befunde 7b + 2).** Plan §5: `.rail__account`
trägt wieder Einstellungen **und** Abmelden (Abmelden bleibt äußerster Knopf — Umkehr von
C1/N3-Lesart b, Nikinger-Entscheidung 2026-09-13 N.9). `.account-nav` bekommt eine
Navigations-Anmutung (die zwei Knöpfe fehlten nie, sie sahen nur nach Fließtext aus — Befund 2
war eine Selbsttäuschung der CSS-Form, nicht eine Knopf-Lücke). `test_rail_order_settings_and_
logout_at_the_end` wird umbenannt und umgekehrt. Reihenfolge-Empfehlung (P8.6-AH) bleibt F → G → H → J → Gate, jetzt mit G abgeschlossen.

## Session stopped — 2026-09-14 (opencode/M3 — **Block F erledigt** — Layering konsequent, zwei Wächter scharf)

**Atomarer Block, kein Mess-Overhead — `app.css` + zwei statische Tests.** Block F ist
Fundament für Block G: G verschiebt Flächen und würde ohne F dieselbe Arbeit zweimal machen
(Plan §0.2 P8.6-U + §3).

**F1 — Kopfdaten werden kühl (Befund 8).** `app.css:107-123`: `--panel-meta` `#1A1611` →
`var(--surface)` (`#14181D`), `--panel-meta-head` `#221C15` → `var(--surface-raised)`
(`#1B2027`), `--panel-meta-line` `rgba(229,169,60,.22)` → `var(--line)`. Der Kommentarblock
vor den Tokens ist datiert ersetzt — die Begründung „warmer Stich macht Kopfdaten erkennbar"
steht jetzt mit dem Vermerk, dass die Trennung seit Block F über Layer-Höhe läuft (P8.6-AB,
N.10). Die verworfene Alternative „kühl-blau statt warm-gelb" ist explizit benannt (würde
eine zweite Nicht-Akzent-Farbe einführen, Phase-8-Verbot 4).

**F2 — Editor-Layering.** Plan §3.2 sagt: "prüfen, nicht ändern" für `.panel--body`
(`--panel-body` schon Layer 3) und `.editor__textarea` (V127: kein eigener Hintergrund,
erbt von `.panel--body`). `.editor__append` (Layer 2 über Layer 3) trägt schon
`background: var(--surface)` + `border-top: 1px solid var(--line)`; **V127 geschlossen:
null B-Aufwand.** Kein Code-Touch an app.css für F2.

**F3 — Drei rohe Flächen-Hex auf Token.** Neue Tokens in `:root` (Z. 35-39, direkt unter
`--surface-raised`): `--rail-top: #0E1116` (`.rail`-Verlauf, `app.css:374`),
`--auth-glow: #131A23` (Login-Hintergrund, `app.css:1788`), `--auth-card-top: #1A2029`
(`.auth-card`-Verlauf, `app.css:1794`). `#fff` in `.qr-frame` (`app.css:1844`) bleibt mit
begründendem Kommentar ("QR-Code braucht echtes Weiß"). Vorher 17 rohe Hex außerhalb `:root`,
nachher 11 — alle dokumentiert (3 Space-Kategorie-Verläufe, QR `#fff`, plus die `--btn-primary`
`color: #fff`).

**F4 — Zwei Wächter (§8.2).** `test_no_raw_surface_hex_outside_root` (jede `background:`/
`gradient(`-Deklaration außerhalb `:root` nutzt Token oder ist in der EXEMPT_HEX-Liste;
Ausnahmen dokumentiert). `test_meta_panel_is_not_tinted_with_the_warning_colour`
(prüft gezielt die drei `--panel-meta*`-Tokens, nicht "alle 229,169,60" — die
Warnungs-Chips `.list__readonly`/`.detail__badge-readonly` mit `rgba(229,169,60,.10)`
referenzieren `var(--warn)` und sind legitim). Beide Tests sind byte-genau: jede künftige
Re-Tönung des Meta-Panels oder jedes neue rohe Flächen-Hex fällt auf.

**Self-Check §0.5:** `pytest -q` **972 passed in 111,52 s** (V107-Baseline 970 + 2 neue
Wächter), `ui_budget.py` 5/5 (130,1 KB → 130,1 KB im Korridor; `app.css` 60.201 → 60.319 B,
+118 B für die 3 Token-Kommentare und den aktualisierten Meta-Block), Tabu-Diff §0.3
trivial leer (`app.css` ist statisches Asset, Phase 5 P5-B erlaubt), kein `pkill -f`, kein
`systemctl`, sharefyx-mcp **PID 991** nur gelesen. **V127 geschlossen: 0** (textarea
erbt von panel-body, kein eigener Hintergrund). **V126 unverändert: 0** (1024 px
Daten-view-Mechanismus).

**Zwei Selbst-Screenshots** (`p86_block_f_self_check.py` neu, ~140 Z., Playwright-Chromium +
TOTP-Login aus `p86_block_c_self_check.py`):

- `docs/screenshots/p86_block_f_01_vorher_warm_meta.png` (124.242 B) — Editor mit
  `--panel-meta` zurück auf `#1A1611` (per `git stash` + manueller Revert für die Aufnahme,
  danach `git stash pop`; der Revert berührte nur app.css lokal, ist im Commit nicht
  enthalten) — sichtbar warmer Stich unter dem "Kopfdaten"-Header.
- `docs/screenshots/p86_block_f_02_nachher_cool_meta.png` (124.196 B) — selbe Ansicht mit
  F1-Werten: das Meta-Panel ist kühl, die Linie zwischen Head und Feldern ist die
  Standard-Haarlinie. Befund 8 visuell bestätigt weg.

**Checkkriterium (ein Satz, §5-Konvention):** das Meta-Panel zeigt eine kühle Layer-2-Fläche
(`--surface = #14181D`) statt der warmen `rgba(229,169,60,.22)`-Tönung -- Befund 8 weg.

**Naechster Schritt:** **Block G (Layout-Umbau, Befund 5 + 3/4/6/7a)** — löst P8.6-O2 aus
(bewusst), `.shell` wird `240px 480px 1fr`, Übersicht zieht in den `.list`-Slot, Karte bekommt
`.detail` allein, Editor ersetzt sie, **ESC bringt sie zurück** (N.8). Damit fällt auch
Befund 9b weg (`.overview`-Grid + 1280-px-Query entfallen). Reihenfolge-Empfehlung (P8.6-AH)
bleibt F → G, jetzt aber mit F abgeschlossen.

## Session stopped — 2026-09-14 (opencode/M3 — **Block E erledigt: E2a + E2b** mit Wegwerf-v3.0.1-Methodik-Wechsel)

**Reine Mess-Session, kein Produktcode-Touch.** Block E der Reihe nach: E1 Skript (E2a),
E2a Wegwerf auf aktuellem `main`, **E2b Wegwerf auf v3.0.1-Stand statt Produktion**
(Nikinger-Korrektur 2026-09-14: keine echten Creds, Wegwerf-Instanz als Vorabritts-Ersatz
genügt — ist exakt der Code, der auf der Produktion läuft).

**Methodik-Wechsel E2b:** statt Login gegen die echte Produktion eine zweite Wegwerf-Instanz
auf dem **gleichen** Setup, aber mit dem **v3.0.1-Stand** (`6f19a8f`, der Release vom
2026-09-05, der live ist; `/opt/sharefyx/current` → `releases/20260905T140325.378914Z`).
Vermeidet Hard Rule 1 (keine echten Creds im Repo) und Hard Rule 9 (kein Service-Touch)
**vollständig**, ohne den Mess-Punkt aufzugeben. Aufbau:
- `git worktree add -d /tmp/opencode/v301-worktree 6f19a8f` → HEAD bestätigt
- `ln -s /home/savefyx/dev/savefxy/.venv .venv` → Python 3.12.3, identischer Dep-Satz
- `wegwerf_setup_v3ritt.py cleanup + setup + seed-items + start` → PID 162337, Port 18773
- Sanity-Check: `grep -c "bg-void\|select-fill\|overview__col-right" phase5_ui/webui/static/app.css` = **0** (bestätigt Vor-Block-C)
- `p86_viewport_probe.py --base-url http://127.0.0.1:18773 --label v3.0.1 [--dismiss-banner]` — identisches Skript wie E2a, anderes Label

**E2b-Befunde (das ist der eigentliche Punkt — direkter Vergleich E2a vs E2b):**

| Breite | E2a (main, Block C) Geometrie | E2b (v3.0.1, kein Block C) Geometrie | Layout-blockiert E2a / E2b |
|---|---|---|---|
| 1024 | n/a (`data-view="list"`) | n/a (gleich) | **0 / 0** |
| 1200 mit Banner | col-left 692×284, col-right 692×284 (gestapelt) | **byte-identisch**: col-left 692×284, col-right 692×284 | 2 / 2 (`DB-Migration skript`+`Smoke-Tests ausbauen` / `Storybook einrichten`+`DB-Migration skript`) |
| 1200 ohne Banner | col-left 692×**383** | **byte-identisch**: col-left 692×383 | **0 / 0** |
| 1440 | col-left 430×731, col-right 302×731 (zwei-spaltig) | **byte-identisch**: col-left 430×731, col-right 302×731 | **0 / 0** |

**Visuelle Bestätigung** (`docs/screenshots/p86_probe_v3.0.1_{1200,1200-clean}.png`): mit
Banner ragt das 5. Recent-Item (`DB-Migration skript`) in die `VERKNÜPFUNGEN`-Überschrift
hinein — **exakt dasselbe Bild** wie auf Block C; ohne Banner sind alle 5 Recent-Items
sauber gestapelt, `VERKNÜPFUNGEN` klar getrennt.

**V125 — geschlossen: 9a = 9b, gleiche Ursache, falsche Plan-Annahme.** Die Behauptung
„9b durch Block C eingeführt (`overflow: hidden` + `flex: 1` schlägt `height: auto`)" stimmt
**nicht**: Block C hat weder die Layout-Geometrie noch die Container-Höhe geändert — bei
1200 px mit Banner sind die Maße **byte-identisch** zu v3.0.1. Was Block C geändert hat,
ist **welche** Recent-Items in welcher Reihenfolge erscheinen (deshalb die zwei blockierten
Items je Version), nicht das Layout. **Die wahre Ursache war schon immer die 140-px-Banner-
Höhe** und war schon auf v3.0.1 vorhanden — die Aufteilung in „9a (live) / 9b (Block-C-
eingeführt)" war eine **unbewiesene Hypothese**, die nie gegen v3.0.1 verifiziert wurde.
V126 (1024 px) bleibt erledigt: 0.

**Konsequenz für Plan 2** (für die nächste Claude-Code-Planungs-Session): Befund 9 ist
**ein** Bug, nicht zwei — und der Bug wird sowieso von Block G gelöst (`.overview`-Grid +
1280-px-Query entfallen dort, Plan 2 §0.1 P8.6-AA). Die E2b-Messung war trotzdem nötig,
weil sie die **falsche Diagnose** im Phase-Head ausgeräumt hat. Der Methodik-Wechsel
„Wegwerf-vor-Produktion für Befund-Reproduktion" wird in
`docs/concepts/sichtpruefung_automation_conventions.md` als §6 ergänzt — **nach** dieser
Session (kein Hard-Rule-Scope-Creep hier, die Konvention wird vom Nikinger in einer eigenen
Session freigegeben oder verworfen).

**Self-Check §0.5:** `pytest -q` **970 passed in 103,90 s** (V107-Baseline 969 + 1 Flake;
dieser Lauf hat den Flake nicht gezogen — der `authctl revoke --family-id`-Test hängt am
Zufallswert von `secrets.token_urlsafe`), kein Produkt-Code-Touch, Tabu-Diff §0.3 trivial
leer, `ui_budget.py` 5/5 (unverändert), kein `pkill -f`, kein `systemctl`. Wegwerf-Instanz
nach Messung sauber per PID-Datei gestoppt (PID 162337), Worktree `git worktree remove
--force`, venv-Symlink entfernt. sharefyx-mcp **PID 991** nur gelesen. **Kein Service-Touch.**

**Artefakte:** 6 neue Screenshots `docs/screenshots/p86_probe_v3.0.1{,-clean}_{1024,1200,1440}.png`,
2 neue Probe-JSONs `phase8_6_ui_polish/probes/e2b_v3.0.1{,_clean}.json` (~65 KB je),
Worktree-Verzeichnis nach Messung abgebaut. Keine `.md`- oder `.py`-Datei neu (Skript- und
Daten-Only-Session).

**Naechster Schritt:** **Block F (Layering, Befunde 1+8)** — ist von der Produktion
komplett unabhängig (reine Token-Arbeit in `phase5_ui/webui/static/app.css`, +2 statische
Tests), kann ohne zu warten starten. Reihenfolge-Empfehlung (P8.6-AH) bleibt E → F → G
→ H → J → Gate, jetzt aber mit E abgeschlossen.

---

## Session stopped — 2026-09-14 (opencode/M3 — **Block E erledigt: E2a**, E2b wartet auf Nikinger)

**Reine Mess-Session, kein Produktcode-Touch.** Block E der Reihe nach: E1 Skript geschrieben,
E2a gegen die Wegwerf gefahren, E3 Protokoll hier eingetragen. **E2b (Produktion)** kann
opencode/M3 nicht ausführen — es braucht die `SPACE_PUBLIC_BASE_URL` und die Produktions-
Zugangsdaten, die nicht im Repo liegen (Hard Rule 1) und die ich auch nicht erfinden darf.

**E1 — `phase8_6_ui_polish/scripts/p86_viewport_probe.py`** (neu, 421 Z. / 16 KB):
Playwright-Chromium-Probe nach Plan §2.2. CLI: `--base-url` (default `http://127.0.0.1:18773`),
`--widths 1024,1200,1440`, `--label <str>`, `--out <json|-` (Hard Rule 7 — JSON auf stdout,
Logging auf stderr), `--creds <pfad>`, `--no-login` (für manuelle Cookie-Sessions),
`--dismiss-banner` (Update-Banner vor jedem `probe()` wegklicken, damit der Layout-Befund
vom dismissable Banner getrennt wird — Plan §2.3-Vorbedingung). Pro Breite erhebt die Probe:
`rects` (BoundingClientRect für neun Selektoren aus Plan §2.2), `styles` (getComputedStyle
für `overflow`/`overflowY`/`height`/`display`/`gridTemplateRows`/`flex` an vier Containern),
`clipped` (scrollHeight>clientHeight && overflowY=='hidden'), `reachable` (elementFromPoint
am Knopf-Mittelpunkt — **beweist** "nicht mehr klickbar", statt es zu behaupten), `offscreen`
(rect.bottom > innerHeight || rect.top < 0). Plus ein Screenshot pro Breite nach
`docs/screenshots/p86_probe_<label>_<width>.png`. Login ist die TOTP-Routine aus
`p86_block_c_self_check.py` (35-s-Wartezeit auf frisches 30-s-Fenster, 401/429-Retry-Logik);
bei CSRF-Login-Fehler (`403` für Produktion via Reverse-Proxy, `tries_exhausted`) bricht die
Probe sauber ab und schreibt JSON mit `aborted_reason` — kein Workaround.

**E2a — gegen die Wegwerf auf Port 18773.** Wegwerf frisch hochgefahren
(`wegwerf_setup_v3ritt.py cleanup`+`setup`+`seed-items`+`start`, PID 156562, sauber per
PID-Datei gestoppt nach der Messung — Hard Rule 9-konform, kein `pkill -f`). Probe lief
**dreimal pro Lauf** (mit und ohne Banner), Login in Fenster 1 HTTP 200. Sechs Screenshots
in `docs/screenshots/p86_probe_{main,main-clean}_{1024,1200,1440}.png`, zwei Probe-JSONs
in `phase8_6_ui_polish/probes/e2a_{main,main_clean}.json` (je ~65 KB).

**E2a-Befunde (das ist der Punkt dieser Session — was wirklich kaputt ist):**

| Breite | `clipped` für `#detail-overview` | sichtbar-blockierte Buttons | Diagnose |
|---|---|---|---|
| **1024 px** | n/a (`#detail-overview` rect=0×0, `data-view="list"` aktiv) | **0** | 53 hidden-button-Treffer alle `rect=(0,0,0,0)` — Detail-Buttons vom data-view="list"-Mechanismus ausgeblendet, kein Layout-Befund. **V126 damit erledigt.** |
| **1200 px mit Banner** | `false` (scrollHeight passt in clientHeight) | **2**: `DB-Migration skript` (y=576), `Smoke-Tests ausbauen` (y=617) — beide Centerpoint trifft `DIV.overview__col-right` | **Befund 9b reproduziert.** Recent-Item "Smoke-Tests ausbauen" liegt visuell UNTER der "VERKNÜPFUNGEN"-Überschrift; nur die ersten 4 Recent-Items passen in col-left, der 5. fließt in col-right. Sichtbar in `p86_probe_main_1200.png` (VERKNÜPFUNGEN bei y≈617, Smoke-Tests bei y≈633). |
| **1200 px ohne Banner** | `false` | **0** | **Banner-abhängig, nicht unconditional.** Ohne die 140 px Banner-Höhe hat col-left eine auto-Row von **383 px** statt 284 px — alle 5 Recent-Items passen rein. Sichtbar in `p86_probe_main-clean_1200.png`. |
| **1440 px mit oder ohne Banner** | `false` | **0** (37 unsichtbare Treffer wegen `data-view="list"`-Mechanismus, kein Layout-Problem) | Zwei-Spalten-Grid (`grid-template-columns: 1fr 40%`) trägt sauber. col-left (x=652, width=430) und col-right (x=1105, width=302) berühren sich nicht. |

**V125 (gleiche Ursache 9a vs. 9b?) — partiell, E2b fehlt für 9a:** die Plan-Annahme
"9b = `overflow: hidden` + `flex: 1` schlägt `height: auto`" stimmt nur halb — `overflow:hidden`
und `flex:1` sind da, aber sie schlagen `height:auto` **erst dann**, wenn die verfügbare Höhe
klein genug wird, dass die col-left-auto-Row nicht mehr alle 5 Recent-Items aufnehmen kann.
**Der eigentliche Auslöser ist die Update-Banner-Höhe (140 px)**, die bei 1200 px das
Detail-Overview von 900 px auf 761 px drückt und damit col-left von 383 px auf 284 px. Ohne
Banner verschwindet 9b. **Konsequenz für Block G (Layout-Umbau):** 9b wird sowieso gelöst,
weil `.overview`-Grid + 1280-px-Query dort **entfallen** — der Fehler hat dann keine Bühne
mehr. Für die Frage "ist 9a dasselbe?" brauche ich E2b.

**E2b — wartet auf Nikinger.** Was ich brauche, in dieser Reihenfolge:
1. **`SPACE_PUBLIC_BASE_URL`** (z. B. `https://sharefyx.example.org` — die öffentliche URL,
   unter der die Produktion via Tailnet erreichbar ist; nicht der interne Cluster-Hostname).
2. **Produktions-Login-Credentials** für `alpha` (Passwort + `otpauth://`-URI mit
   `secret=…`). Diese landen **nicht im Repo** (Hard Rule 1); ich lese sie zur Laufzeit
   aus `--creds <pfad>` wie die Wegwerf-Credentials auch. Wenn Du die Daten lieber direkt
   in den Chat tippst statt in eine Datei, lege ich sie unter `/tmp/opencode/` ab
   (`chmod 600`), das Skript liest sie ohnehin von dort.
3. Eine Bestätigung, dass der read-only-Login gegen die Produktion okay ist. Hard Rule 9
   verbietet mir `systemctl`, `pkill -f` und dergleichen — die Probe tut nichts davon, sie
   loggt sich ein, **klickt nichts**, und loggt sich am Ende wieder aus (oder beendet den
   Browser-Kontext, was den Cookie ungültig macht). Wenn der Login am CSRF-Origin scheitert
   (Plan §7.2, Handover §4.3), melde ich das und breche ab — kein Workaround.

**Self-Check §0.5:** `pytest -q` **969 passed + 1 Flake** (unverändert, V107-Baseline), kein
Produkt-Code-Touch, Tabu-Diff §0.3 trivial leer, `ui_budget.py` 5/5 (Block E hat keine
CSS/JS-Änderung), kein `pkill -f`, kein `systemctl`, sharefyx-mcp **PID 991** nur gelesen.
Wegwerf-Instanz nach der Messung sauber per PID-Datei gestoppt (Plan §7.1 + Hard Rule 9).

**Naechster Schritt (zwei offene Wege):** (a) **E2b jetzt**, sobald URL + Creds da sind —
gleiches Skript, neues `--base-url` + `--creds`, output `phase8_6_ui_polish/probes/e2b_production.json`
+ `docs/screenshots/p86_probe_production_{1024,1200,1440}.png`. (b) **Block F** (Layering,
Befunde 1+8), wenn E2b warten muss — ist von der Produktion unabhängig, kann parallel laufen.
**Reihenfolge-Empfehlung** (P8.6-AH): E → F → G → H → J → Gate; E2b blockiert das nicht,
weil F die Token-Frage klärt und G die Geometrie umbaut. Sobald E2b durch ist, wandert
Block E Modul-Status auf ✅ und V125 wird ganz geschlossen.

---

## Session stopped — 2026-09-13 (Claude-Code-Planungssession — **Plan 2 geschrieben**, sechs Nikinger-Entscheidungen, ein neuer Produktionsfehler gefunden)

**Reine Planungssession, kein Produktcode-Touch.** Ergebnis: `docs/concepts/phase8_6_ui_polish_plan2.md`
(~69 KB, 📕-Snapshot gegen `main`@`26a7cc9`) — ausführungsreifer Plan für alle neun UX-Befunde,
mit Blöcken **E/F/G/H/J**, Locks **P8.6-W–P8.6-AL**, Abnahme **P8.6-33–P8.6-54**,
`[VERIFY]` **V123–V139**.

**Sechs Nikinger-Entscheidungen (N.7–N.12), alle in Plan 2 §0.1 datiert:**
**(N.7)** `.shell` wird **`240px 480px 1fr`** — die bewusste, vorgelegte und entschiedene
Auslösung von **P8.6-O2**; Begründung ist eine Messung (Space-Zeilen brauchen ~433 px, 380
reichen nicht). **(N.8)** Editor **ersetzt** die Karte, **ESC bringt sie zurück** — gilt auch
für den Klick auf einen Karten-Knoten; ist damit Abnahmekriterium P8.6-36. **(N.9)** Befund 7b
kehrt **C1 / N3-Lesart b** um: Einstellungen und Abmelden wieder unten, **Abmelden bleibt der
äußerste Knopf**. **(N.10)** Layering per **Tiefe statt Farbe** — der warme Stich der
Kopfdaten fällt weg. **(N.11)** Plan 2 ist ein **eigenes Dokument**; Plan 1 bleibt als 📕
unangetastet, der kanonische Closeout wandert nach Plan 2 §9 (**P8.6-W**). **(N.12)** Der
`pytest`-Flake wird **beidseitig** gefixt — Test *und* Produktionscode.

**Fünf der neun Befunde haben in dieser Session eine gemessene Ursache bekommen, statt einer
Vermutung:**

| Befund | Gemessene Ursache |
|---|---|
| **8** (YAML-Header „sieht wie Warnung aus") | `--panel-meta-line: rgba(229,169,60,.22)` **ist** `--warn: #E5A93C` bei 22 % — byte-genau dieselben Kanäle. Keine Wahrnehmungsfrage, eine Tokenfrage |
| **1** (verschiedene Grautöne) | **10 Flächen-Token in `:root` + 4 rohe Hex außerhalb**: `#0E1116` (`app.css:362`), `#131A23` (`:1776`), `#1A2029` (`:1782`), `#fff` (`:1829`, QR — bleibt). Die drei Verläufe bei `:487/492/497` sind Kategoriefarben, keine Grautöne |
| **2** (Konto-Dialog-Knöpfe „fehlen") | **Messfrage geschlossen: sie fehlen nicht.** `app.html:484-485` rendert beide, sichtbar in `p86_block_b_04_account_dialog.png` bei y≈306/358. `app.css:619-633` gibt ihnen `background: none; border: none` — sie lesen sich als Fließtext |
| **4** (Karte zu klein) | `1fr 40%` = 40 % des **Detail-Slots**, nicht der Seite: 756 px × 40 % = **302 px** bei 1440 px = 21 % der Seite. Vorhersage und Messung stimmen aufs Pixel. P8.6-K zitierte §1 mit „ca. 40 % der gesamten Seite" — das war nie erfüllt |
| **6** (Hover verrutscht) | **Lock-Abweichung, keine CSS-Wanze.** P8.6-P sagt „die Zeile als Ganzes klickbar"; C4 baute einen **inneren** Button. Der Hover-Fill endet in `p86_block_c_02` bei x=845, die Zeile reicht bis x=1083 |

**Befund 9 zerfällt in zwei Befunde** (Plan 2 §2.1): **9a** läuft live auf `v3.0.1`, wo Block C
gar nicht existiert — Ursache **unbekannt**, wird in Block E gemessen. **9b** ist von Block C
eingeführt (`overflow: hidden` + `flex: 1` schlägt `height: auto` in der 1280-px-Query ⇒ kein
Scroll-Container). **Die Falle, die Block E vermeidet:** 9b reparieren und „behoben" melden,
während 9a live stehen bleibt.

**Neuer Produktionsfehler, beim Messen der Baseline gefunden:** `pytest` ergab **969 passed +
1 failed**, nicht die dokumentierten 970. `phase4_auth/tests/test_authctl.py::test_revoke_kills_the_family`
scheitert an `argument --family-id: expected one argument`. Isoliert grün, das ganze
`phase4_auth/tests/` grün (261 passed) — **keine Reihenfolgenabhängigkeit**. Ursache:
`family_id = secrets.token_urlsafe(16)` (`store.py:393`) beginnt in **1,569 %** der Fälle
(200.000 Ziehungen gemessen) mit `-`, dann hält `argparse` den Wert für eine Option. Das
trifft nicht nur den Test, sondern **`authctl revoke --family-id <id>` für einen echten
Operator bei jeder 64. Familie**. Behandlung: Block J, beide Hälften, auf ausdrückliche
Anordnung (N.12) — und damit die erste **datierte Tabu-Ausnahme** der Phase (**P8.6-AJ**,
`phase4_auth/authserver/crypto.py` + zwei Zeilen `store.py`). **`phase1_storage/storage/**`
bleibt zu — keine neunte P1-Contract-Öffnung.**

**Ein weiterer Befund aus der Planung, der eine offene Frage schließt:** `#home-button` ruft
heute **`navigateAll()`** (`app.js:99-105`) — „Übersicht" und „Alle Items" sind **dieselbe
Aktion**. **V110** („ist der bestehende Mechanismus der Kippschalter?") ist damit als
*negativer* Befund beantwortet: es gibt keinen Zwei-Zustands-Schalter, es gibt zwei Knöpfe
für **einen** Zustand. Block G trennt sie (Plan 2 §4.3).

**Doku-Hygiene (Step 0' der Planungssession):** repo-weiter Scan über 109 `.md` — **0**
unauflösbare `up:`/`down:`-Links, **0** echte fehlende L1-Cards, **0** echte fehlende
INDEX-Zeilen (alle Treffer sind die vier dokumentierten Ausnahmen plus Test-Fixtures).
**„Nichts zu tun" war hier das Ergebnis** — mit einer Ausnahme: `docs/INDEX.md` stand bei
**38.815 B** gegen ein Kriterium von ≤ 38.912 B, also **97 B Luft**, und Plan 2 fügt eine
Zeile von 1,2 KB hinzu. Sieben Zeilen geschlossener Phasen gestrafft (**−1.549 B**), Plan-2-
Zeile + Abschnitts-Überschrift + `updated:` (**+1.205 B**) ⇒ **38.471 B, 441 B Luft**. Die
`updated:`-Kette war hier **nicht** die Quelle (nur 554 B) — anders als in der
Wurzel-`CLAUDE.md`, wo am 2026-09-13 69 % der Dateigröße darin steckten. Gemessen, nicht
angenommen.

**Anker-Drift belegt** (Plan 2 §1.5): P8.6-O2 nennt das `.shell`-Grid bei `app.css:327-332`,
real steht es bei **`345-350`**; `.overview__graph` ist von `915` auf **`1074`** gewandert;
`renderRail()` von `tree.js:242` auf **`297`**. V106 ist verbraucht, **V123** gegen
`26a7cc9` ist der neue Sammelmarker. Die drei Commits zwischen `bc2aa9f` und `26a7cc9` sind
reine Doku-Commits — `git diff --stat bc2aa9f..26a7cc9 -- phase5_ui/webui/static` ist leer.

**`ui_budget.py` 5/5** im Korridor (137,5 KB von 250 KB; `app.css` 21,1 KB gzip).
`GET /api/v1/overview` **372,9 ms** — bestätigt **V108** ein zweites Mal: die 863 ms vom
Phasenstart waren Last auf dem alten Mini-PC, keine Regression.

**Tabu-Diff §0.3 trivial leer** (kein Code-Touch). **Service-Touch 0** — `sharefyx-mcp`
wurde in dieser Session nicht angefasst, nur der `pytest`-Lauf mit gestrippten
`SHAREFYX_*`/`SFX_*`-Variablen gefahren (keine waren gesetzt). Kein `pkill`, kein `systemctl`.

## Session stopped — 2026-09-12 (Block-C-Sichtung Nikinger — 6 UX-Befund-Kategorien, Partial Closeout vorgeschlagen, kein Deploy, **Plan 2 für P8.6 erforderlich**)

**Nikinger-Sichtung der Screenshots** `docs/screenshots/p86_block_c_{01..06}_*.png`
am 2026-09-12 (Drei-Bedingungen-Regel, Bedingung 3 — Nikinger-Sichtung der Bilder).
**Befund: so nicht auslieferbar.** Nikinger schlägt „Partial Closeout" vor, der
einen neuen **2. Plan für P8.6** verlangt, bevor Block C deployed wird.

**Befund-Kategorien (sechs, plus ein B-Backlog aus rückblickender Sichtung):**

**B-Backlog (Block B, altes Material, bei Sichtung wieder aufgefallen):**

1. **Verschiedene Grautöne** fallen in mehreren Block-B-Screenshots auf — die
   Layering-Tokens (`--bg-void`/`--surface`/`--surface-raised`/`--bg-elevated`) aus
   Block A werden in der Praxis nicht konsequent durchgehalten. Welche Stellen
   betroffen sind, muss Block-A-Re-Audit zeigen.
2. **Konto-Dialog: „Update-Log ansehen" + „Spaces verwalten"-Buttons scheinen
   zu fehlen / nicht sichtbar.** Die `.account-nav`-Klasse wurde in Block B
   eingeführt (Navigation statt Knopf-Plastik); ob die Buttons im Dialog
   tatsächlich gerendert werden oder die Sichtung ein anderes Problem zeigt
   (z. B. außerhalb des Viewports), muss Block-B-Re-Sichtung am echten Gerät
   zeigen.

**Block-C-Befunde (neu, aus den p86_block_c-Screenshots):**

3. **Refresh-Button überlappt mit der Karte.** Der Refresh sitzt in
   `.overview__header` (Z. 88–94), die Karte in `.overview__col-right`. Auf
   1440px-Viewport ist der Header einspaltig über die ganze Breite und die
   Karte beginnt darunter — visuell wirkt es, als schwebe der Refresh-Button
   über der Karte. Vorschlag: Refresh in die Karte selbst verlegen
   (oben links, neben den Toggle-Checkboxen), oder Header auf zwei Spalten
   aufteilen.
4. **Karte ist „ziemlich klein"** bei 1440px-Viewport (`grid-template-columns:
   1fr 40%` mit Wrapper-DIVs `head-row`/`col-left`/`col-right`). Die rechte
   Spalte bekommt nur 40 % der Detail-Breite, und die Detail-Spalte ist
   durch das äußere `.shell`-Grid (`256px 380px 1fr` aus §4.1) ohnehin
   nicht riesig. 30 Knoten auf einer 500×700-Box werden gedrängt. Vorschlag:
   `grid-template-columns: 1fr 50%` oder `2fr 3fr` testen, oder die Karte
   ohne Spalten-Cap direkt `flex: 1` setzen (Wrapper-Layout dafür anpassen).
5. **Großer Vorschlag (Nikinger): Spaces-Übersicht + Zuletzt benutzt wandert
   in den Standard-Listen-Slot (links).** Auf der Übersicht zeigt der
   linke Slot die Spaces + zuletzt benutzte Items, der rechte Slot zeigt
   die Map. **Klick auf einen Space** schließt die Übersicht-Slots
   und öffnet die ganz normale Item-Liste des Spaces (im Listen-Slot).
   Solange nur auf Space (nicht auf Item) geklickt ist, bleibt der
   Editor-Slot rechts leer (mit der Karte als Default). **Klick auf ein
   Item in der Liste** öffnet den Editor dort, wo der Leerraum war
   (initial die Karte). Das ist eine substantielle Layout-Reorg, die
   das aktuelle „Übersicht immer = drei-Spalten (Spaces + Karte + Recent
   auf einer Seite)" ablöst.
6. **Hover-Effekt verrutscht** in Screenshot 02 (nach Klick auf Space, dann
   Hover). Vermutlich Layout-Inkonsistenz, weil nach dem Space-Wechsel die
   Listenansicht aktiv ist und der Mauszeiger noch auf einer Übersicht-Zeile
   ruht, deren Hover-Klasse jetzt auf `.list__row` umgebogen wird. Detail
   muss in Plan 2 geklärt werden.
7. **„Alle Items"-Modus: Spaces-Übersicht + Spacename + Zuletzt benutzt
   VERSCHWINDET** (Nikinger). Direkt nur noch „Übersicht" → Item-Liste
   + Map (die beiden Slots links + rechts). **Einstellungen + Abmelden
   rücken zusammen** (Einstellungen unten im Rail, direkt über Abmelden,
   kein eigener Header-Bereich dazwischen). Aktuell sind sie durch
   `#rail-tree` getrennt — das muss sich ändern, sobald die Spaces-Übersicht
   aus dem Übersicht-Slot verschwindet.
8. **Editor — Verschiedene Grautöne.** YAML-Header (`details.panel--meta` mit
   `.panel__head`) sieht „wie eine Warnung aus", gehört aber in **Layer 2
   grau** wie die Standard-Übersicht. Der Editor selbst (Textarea,
   Vorschau, Append) soll das einzige in **Layer 3** sein. „Zeile
   Einfügen" (`input#append-input` + Button) ebenfalls Layer 2 wie YAML.
   Das ist Layering-Konsistenz aus §5, die in der Implementierung
   wahrscheinlich nicht überall durchgehalten wurde.
9. **`p86_block_c_06_karte_unter_liste_1200px.png` — Karte sieht komisch aus,
   keine Buttons mehr in der schmalen Ansicht klickbar.** Nikinger hat das
   **selber auf der Produktion reproduziert** (nicht nur Wegwerf). Die
   `@media (max-width: 1280px)`-Regel kollabiert das Grid auf eine Spalte,
   aber die Buttons (`.btn` Knöpfe) werden in der schmalen Variante
   wahrscheinlich zu klein oder werden vom Grid überschnitten. Detail
   muss in Plan 2 untersucht werden (CDP-Probe gegen die Wegwerf-Instanz
   mit Viewport-Größen 1024/1200/1440).

**Anforderungen für P8.6 Plan 2 (Nikinger, zusammengefasst):**

- **Layout-Reorg** gemäß Befund 5: Spaces + Zuletzt benutzt links in den
  Standard-Listen-Slot, Map daneben, Klick auf Space öffnet Item-Liste
  statt Spaces-Übersicht, Klick auf Item öffnet Editor im rechten Slot.
- **„Alle Items"-Modus schlanker** gemäß Befund 7: ohne Spaces-Übersicht,
  ohne Spacename, ohne Zuletzt benutzt; nur Item-Liste + Map.
- **Rail-Reihenfolge anpassen**: Einstellungen unten, direkt über Abmelden
  (Befund 7 zweite Hälfte).
- **Karte angemessen groß** (Befund 4): `grid-template-columns`-Werte
  testen, evtl. `flex: 1` ohne Cap.
- **Refresh-Button umsetzen** (Befund 3): in die Karte oder Header teilen.
- **Layering-Konsistenz** (Befund 1, 8): drei Layer sauber definieren
  (`--bg-void`/`--surface`/`--surface-raised`/`--bg-elevated`), YAML-Header
  + Append → Layer 2, Editor-Textarea → Layer 3, Standard-Übersicht bleibt.
- **Schmaler-Viewport (≤1280px)** (Befund 9): Buttons bleiben klickbar,
  Layout bleibt sinnvoll — eigene Investigation nötig (vermutlich
  Touch-Target-Größe + Grid-Stapelung).
- **B-Backlog mitnehmen** (Befund 1, 2): Grauton-Konsistenz + Konto-Dialog-
  Buttons sichtbar.

**Status:** Block C bleibt formal ✅ (fünf Sub-Änderungen + D3-Nachzug + 3
Tests + 6 Screenshots geliefert), ist aber **nicht auslieferbar**. Diese
Session macht **nur Doku** — die nächste Session beginnt eine Claude-Code-
Planungssession für P8.6 Plan 2 (analog zur Phase-8.5-Planungssession
am 2026-09-08). **Kein Push + Deploy** in dieser Session — Lokalstand
bleibt 7 Commits voraus (Block A + D + V + V-plugin + V-vision-befund +
§5-Konvention + Block B + Block C), Nikinger entscheidet nach Plan 2,
ob die alte Schuld in einem einzigen großen Push oder mehreren
kleinen landet.

**Vormerkung neu** (in §Vormerkungen dieses Heads): **„p8.6 plan 2
(N.6)"** — Layout-Reorg + Layering-Konsistenz + schmaler-Viewport +
B-Backlog. Eigene Folge-Phase oder Sub-Phase von P8.6, je nach
Umfang des Plans. Ziel: einen **zweiten Vorabritt** + Deploy, der dann
alle sieben UX-Befunde abdeckt.

## Session stopped — 2026-09-12 (Block C ✅ — Struktur-Umbau: Einstellungen oben, Alle Items unten, Karte als rechte Spalte, klickbare Spaces, Ordner-Zähler)

**Auftrag (Nikinger 2026-09-12, aus Block-B-Sub-Block):** „Block C zuerst anfangen,
dann verifizierst du noch einmal mal. Bevor wir deployen, braucht es drei Sachen:
alle Code Tests grün, alle Bilder laut dir grün, ich habe über kritische Bilder noch
mal rüber geschaut." — Block C nach Plan §5 (C1 „Konto"→„Einstellungen", C2 „Alle
Items" unter den Spaces, C3 Map als rechte Spalte / volle Höhe, C4 Spaces in der
Übersicht klickbar, C5 Ordner-Zähler clientseitig aus `state.items`) + D3-Nachzug
(V112-Gegenprobe nach C3). Erst opencode/M3-Code-Touch seit Block B am
2026-09-11 (3 Tage vorher). **Kein Push + Deploy in dieser Session** — die
Drei-Bedingungen-Regel gilt für v3.0.2.

**Was in diesem Commit passiert ist (C1 + C2 + C3 + C4 + C5 + D3):**

1. **C1 — „Konto" → „Einstellungen", Reihenfolge im Rail (Plan §5.1).**
   `#account-button` wandert aus `.rail__account` heraus direkt unter `#home-button`
   (`app.html` Z. 30-34), Label „Konto" → „Einstellungen" (das Icon `#i-settings`
   war schon immer ein Zahnrad, der Name hinkte hinterher — N3-Lesart b, Einstellungen
   oben, Abmelden ans Rail-Ende). `#logout-button` bleibt in `.rail__account` als
   einziges Kind. Neue Modifikator-Klasse `.rail__action--account` (analog
   `.rail__home`) statt generischer `.rail__action`-Anpassung — damit Logout-Knopf
   als einziges Kind weiterhin die volle Breite einnimmt (`flex: 1` bleibt).

2. **C2 — „Alle Items" unter den Spaces (Plan §5.2).**
   `tree.js :: renderRail()` ruft `renderScopeRow()` jetzt **nach** den
   `foreign.forEach(renderSpaceNode)` (Z. 299+), nicht mehr davor. Neue
   `tree__group`-Überschrift „Alles" vor dem Button (analog „Mein Space" /
   „Verbundene Spaces"), damit der Wechsel nicht ohne Überschrift an den
   Spaces-Block klebt. `renderScopeRow()`-Kommentar wörtlich erhalten
   („Lieber keine Zahl als eine unwahre" — der Kommentar erklärt genau den
   Sonderfall, den C5 gleich für Folder erweitert).

3. **C3 — Map als rechte Spalte, volle Höhe (Plan §5.3).**
   `.overview` (`app.css` Z. 898+) wird ein zweispaltiges Grid
   (`grid-template-columns: 1fr 40%; grid-template-rows: auto 1fr; flex: 1;
   min-height: 0; overflow: hidden`). Direkte Kinder in drei logische Gruppen
   gefasst: `.overview__head-row` (Header + Legende, `grid-column: 1 / -1`),
   `.overview__col-left` (Spaces + „Zuletzt benutzt" + Recent, `overflow-y:
   auto`), `.overview__col-right` (Verknüpfungs-Heading + Graph, `flex: 1`).
   `.overview__graph` verliert `min-height: 55vh` und `max-width: 960px`
   (app.css Z. 1008+) — V112-Gegenprobe, „Karte schneidet unten ab" behoben.
   `@media (max-width: 1280px)` (`app.css` Z. 1859+) kollabiert das Grid auf
   eine Spalte, Map rutscht unter die Liste.

4. **C3 + V115 — `requestAnimationFrame(resize)` in `loadGraph()`.**
   `graph.js :: loadGraph()` (Z. 150+) ruft `resize()` jetzt in einem
   `requestAnimationFrame(...)`-Wrapper, NACHDEM die Knoten/Edges geladen sind —
   der ResizeObserver feuert zwar beim ersten `observe()` (Spec
   https://www.w3.org/TR/resize-observer/), aber zu diesem Zeitpunkt ist
   `.overview__graph` im neuen Grid möglicherweise 0x0 (CSS-Layout noch nicht
   committed); ohne den RAF würde `seedInitialPositions()` mit der 0x0-Box
   rechnen. V115 damit belegt: gemessen, dass der ResizeObserver allein beim
   ersten Mount nicht ausreicht — der Fix ist 8 Zeilen, kein neuer Mechanismus.

5. **C4 — Spaces in der Übersicht klickbar (Plan §5.4).**
   `.overview__space-row` bekommt ein `<button class="overview__space-open">`
   (innerhalb der `<li>`), das Name + Kategoriepunkt umschließt — Tastaturfokus +
   Screenreader-Rolle gratis. `event.stopPropagation()` auf den Counter-Chips
   bleibt (jetzt tragend: Eltern-Button würde sonst ebenfalls auslösen, mit
   anderer Semantik). Neue CSS-Klasse `.overview__space-open` mit eigenem
   Hover aus B1. `activateView()` wird **exportiert** und in `list.js`
   importiert (V116 — `activateView(name)` statt `navigate(name, "open")`,
   weil die Zeile den Bucket nicht explizit wählt).
   `closeEditor().then(proceed => activateView(name))`-Gating eingebaut — wie
   die Ordner-Buttons in `tree.js` (Phase-8-§9.3 Punkt 1). **Erster echter
   Bug, der das Skript während des Baus stoppte:** `activateView` war
   sowohl als `function` (Original) als auch als `export function` (C4) in
   `tree.js` definiert — `Identifier 'activateView' has already been declared`
   als `PAGE ERROR`, `overview__spaces` blieb leer. Original-Z. 20-33 entfernt,
   Page-Error behoben, danach gerendert sauber.

6. **C5 — Ordner-Zähler clientseitig aus `state.items` (Plan §5.5).**
   `state.js` bekommt `itemsLoaded: {}` — ein einfaches `Object`, das pro Space
   speichert, ob die Items dieses Spaces schon einmal geladen wurden. Drei Regeln
   aus §5.5, alle umgesetzt: (1) gezählt wird alles, was der Nutzer im Ordner
   **sehen** würde, inklusive `archived`; (2) nur direkte Kinder, kein
   rekursiver Zähler; (3) ohne `itemsLoaded[space.name]` kein Zähler („Lieber
   keine Zahl als eine unwahre"). `tree.js :: folderButton()` (Z. 156+)
   bekommt `folderItemCount(spaceName, folderPath)`-Helfer, der nach
   `item.space` UND `item.folder` filtert; `list.js :: loadItems()` (Z. 475+)
   setzt `itemsLoaded[space]` (im space-Modus) bzw. `itemsLoaded[item.space]`
   für jedes Item (im „all"-Modus) und ruft danach `renderRail()` auf, damit
   die Zähler die frischen Items sehen. `.tree__count` bekommt `margin-left:
   auto`, damit Eimer + echte Ordner rechtsbündig in ihren Buttons liegen.

7. **C5 Folge: V117-Reset in `activateView()` und `navigateAll()`.**
   `state.itemsLoaded = {}` wird in beiden Navigation-Funktionen vor
   `renderRail()` geleert — sonst zeigt das Rail für ein paar ms Counts aus
   dem falschen Pool (state.items wird erst in `loadItems()` umgeschaltet,
   renderRail() läuft aber ZUVOR). **Befund während des Self-Smoke:** ohne
   den Reset zeigte Screenshot 01 für alpha/Notizen den Counter 6 statt 3,
   weil der vorangegangene globale Modus Items aus beta/gamma mitgezählt
   hatte. Reset löst das; erste renderRail() zeigt bis zur loadItems-Auflösung
   leere Folder-Counter, danach sind sie korrekt für den neuen Space.

8. **D3-Nachzug:** die `.overview__graph`-Höhe ist implizit mit C3 verifiziert
   (Screenshots 01 + 06 zeigen die Karte in voller Spaltenhöhe, Screenshot 06
   unter 1200px zeigt Karte unter der Liste ohne Abschneiden).

9. **`+3` statische Tests** in `test_static_routes.py`:
   - `test_rail_order_settings_before_tree_logout_last` — prüft die exakte
     Reihenfolge der Tags im Markup (home < account < tree < logout).
   - `test_account_button_says_einstellungen` — Label „Einstellungen" im
     Button, „Konto" explizit nicht.
   - `test_overview_graph_has_no_max_width_or_min_height` — regex über alle
     `.overview__graph`-Blöcke, prüft Abwesenheit von `max-width` und
     `min-height` (V112-Regressionswächter).

**Selbstprüfung (§0.5):**

- **Tabu-Diff §0.3 leer.** `git diff --stat -- phase1_storage/storage
  phase4_auth/authserver phase2_mcp/mcpserver phase5_ui/webui/security.py
  phase5_ui/webui/api.py phase5_ui/webui/serializers.py phase5_ui/webui/permissions.py`
  liefert nichts. Erlaubte Pfade berührt: `phase5_ui/webui/static/app.{html,css}`,
  `phase5_ui/webui/static/js/{graph,list,state,tree}.js`, `phase5_ui/tests/
  test_static_routes.py`, `phase8_6_ui_polish/scripts/p86_block_c_self_check.py`
  (§0.3 whitelistet alle).
- **`pytest -q` 970 passed in 111 s.** 21 Tests in `test_static_routes.py`
  (V107: 967 → **970**, +3 für C1/C3/C5 in Plan §8.2 — die anderen zwei
  Tests aus der Liste waren in Block A/B).
- **`node --check` auf alle vier berührten JS-Dateien grün** (tree.js,
  list.js, graph.js, state.js — keine Syntax-Fehler).
- **`python phase5_ui/scripts/ui_budget.py` 5/5 im Korridor.** app.css
  21.1 KB, Bundle app.js+app.css+Font gzip **137.5 KB** von 250 KB (+4.4 KB
  gegen Block B 133.1 KB, durch C1/C3/C4-CSS-Erweiterungen). Erstaufruf
  146.7 KB von 400 KB. **`GET /api/v1/overview` 370 ms** — weiter unter dem
  Step-0-Stand von 863 ms (V108-Befund: 380→370 ms, kein P8.6-Auftrag).
- **`grep -nE 'rgba\(62,141,243'`** trifft nur die `:root`-Zeilen, die zwei
  Block-A-Wächter (`test_no_raw_accent_rgba_outside_root`,
  `test_every_css_var_reference_is_defined`) halten auch C3 sauber.
- **Service-Touch 0.** sharefyx-mcp **PID 991** über die gesamte Session
  unverändert (`systemctl show -p MainPID sharefyx-mcp` zu Beginn = 991, am
  Ende = 991). Eigener Wegwerf auf Port 18773 (PID-Datei, mehrfach
  cleanup+setup+seed-items+start durchgespielt für frische Datenlage + Reset
  des `login_attempts`-Rate-Limits; **kein `pkill -f` mit Regex** — alle
  Starts/Stops über PID-Datei aus `wegwerf_setup_v3ritt.py`).
- **Größenprüfung:** app.html 33 KB (Wrapper-DIVs für Grid-Layout +0.4 KB),
  app.css 21.1 KB (+1.3 KB), test_static_routes.py 25.5 KB (+0.1 KB),
  Phase-Head jetzt **~55 KB** nach Block-B-Rotation (vorher 50 KB, weiter
  über 40-KB-Softcap, benannt statt versteckt — Vorbild P8-P / Phase 6.5).
- **Sechs Selbst-Screenshots** unter `docs/screenshots/p86_block_c_{01..06}_*.png`
  zeigen die visuellen Ziele:
    - **01_übersicht.png** (1440×900): Rail mit „Einstellungen" oben +
      „Abmelden" am Ende, „Alle Items" mit „Alles"-Trenner UNTER den Spaces,
      Karte als rechte Spalte in voller Höhe (V112-Gegenprobe), Spaces mit
      Counter-Chips und Folder-Zähler im Rail („Offen 5", „Notizen 6",
      „Archiv 1", „notizen 3", „projekte 5", „backend 4", „frontend 1").
    - **02_after_space_click.png**: Klick auf Space-Zeile öffnet die
      Listenansicht des alpha-Space (state.filter Default „open" — V116).
    - **03_space_hover.png**: Hover über die Space-Zeile (B1 quiet-Selektion,
      nicht Voll-Füllung — B4-Regression-Check).
    - **04_alle_items_with_folder_counts.png**: „Alle Items"-Modus aktiv,
      Liste mit Items aus allen Spaces (Space-Name als Präfix + Punkt),
      Folder-Counter im Rail (nun mit Summe über alle Spaces: „projekte 7"
      = 5 alpha + 2 beta).
    - **05_editor_caution_regression.png**: Editor geöffnet,
      Archivieren-Knopf in Vorsicht-Farbe (B4-Regression-Check).
    - **06_karte_unter_liste_1200px.png**: Bei 1200px Breite kollabiert das
      Grid auf eine Spalte, Map rutscht unter die Liste, kein Abschneiden.

**Was bewusst NICHT in diesem Commit passiert ist:**

- **Kein Push + Deploy.** Die Drei-Bedingungen-Regel des Nikingers („alle
  Code-Tests grün ✓, alle Bilder laut dir grün ✓, ich habe über kritische
  Bilder noch mal rüber geschaut ⬜") ist erst zu zwei Dritteln erfüllt. Der
  Nikinger macht Push + Deploy selbst, sobald er die Screenshots gesichtet
  hat. Lokaler `main` ist damit **6 Commits voraus** (vor Block B Block A+D
  + Step V + Step V-plugin + Step V-vision-befund + §5-Konvention, jetzt
  Block C obendrauf).
- **Kein Gate-Skript** (Plan §7, `p86_polish_smoke.py` mit 12 Stationen) —
  folgt nach dem Deploy-Push.
- **Keine Tests in den anderen Testdateien** — C5 ist rein clientseitig,
  kein Server-Roundtrip nötig (P8.6-O). Die `test_static_routes.py`-Tests
  decken Markup + CSS ab; Verhalten wird über den Self-Smoke verifiziert.
- **Keine `.shell`-Grid-Änderung** (P8.6-O2-Eskalationsregel eingehalten —
  C3 verändert nur `.overview`, nicht das äußere Layout). Drei-Spalten-
  Grundraster aus §4.1 bleibt unverändert.

**Hard-Rule-8-Doku-Update im selben Commit:** Phase-Head Modul-Status Zeile 5 ✅
(Block C), Phase-Head `## Session stopped` neu (Block-B-Sub-Block nach
`SESSIONS_ARCHIVE.md` rotiert), Frontmatter `updated:`-Pipe,
`SESSIONS_ARCHIVE.md` mit rotiertem Block-B-Sub-Block + Frontmatter,
`docs/INDEX.md` (updated-Frontmatter + Phase-8.6-Zeile), `docs/concepts/
phase8_6_ui_polish_plan.md` §5 als ✅ markiert + Modul-Status-Zeile in der
Plan-Tabelle, `ROADMAP.md` P8.6-Status auf 🟡, Wurzel-`CLAUDE.md` Current-state-
Absatz oben ergänzt (mit ausdrücklicher Block-C-Verifikation — drei der drei
Bedingungen genannt). Alles in einem Commit.

**Commit-Message (geplant):**
`phase 8.6: Block C -- Einstellungen oben, Alle Items unten, Karte rechts voller Hoehe, klickbare Spaces, Ordner-Zaehler`

**Nächster Schritt (für die nächste Session):** **Nikinger-Sichtprüfung** der
sechs Screenshots (`docs/screenshots/p86_block_c_{01..06}_*.png`) — danach
Push + Deploy `v3.0.2` als Nikinger-Aktion (Hard Rule 9 + P8.6-R Patch-Bump),
danach **Gate** (Plan §7): `p86_polish_smoke.py` 12 Stationen in Chromium +
Firefox, fünf Nikinger-Sichtprüfungs-Entscheidungen (V110 §1, V114 §10.1,
V112 §2.3 [bereits erledigt in Block C], V116 §10.4 [bereits erledigt],
P8.6-R Versionierung), dann **Step Z** Closeout (Plan §9 füllen, Rotation,
kein separates Handover-Dokument — P8.6-B).

## Session stopped — 2026-09-11 (Block B ✅ — Selektion vereinheitlicht, Vorsicht-Kategorie)

**Auftrag (Nikinger 2026-09-11):** „Hello there, please go on atomically with the next step
according to plan." — Block B nach Plan §4 (Selektion vereinheitlichen, B4 Vorsicht-
Kategorie, B5 Radien), A vor B ist zwingend (P8.6-U). Erst opencode/M3-Code-Touch seit
Cluster 1 (P8.5-19 + P8.5-6 am 2026-09-07).

**Was in diesem Commit passiert ist (B1 + B2-Audit + B3 + B4 + B5):**

1. **B5 (eine Zeile, sofort erledigt).** `app.css:1293` `.link-picker-results`
   `border-radius: 6px` → `var(--radius-sm)`. Der einzige Token-Drift im Radien-Bestand
   (gemessen vom Phase-8.5-Closeout-Block: 37 Deklarationen, sieben Werte, einer davon
   hartkodiert). Plan §4.5 Tabelle sagt es, der Code bestätigt es, Implementierung steht.

2. **B1 (konsolidierte Hover-Regel).** Eine Regel ersetzt drei Flickenteppich-Fassungen:

   ```css
   .list__rows > li:not(.list__row--selected) .list__row:hover:not([aria-current="true"]),
   .rail__home:hover:not([aria-current="true"]),
   .rail__action:hover,
   .tree__space:hover,
   .tree__folder:hover:not([aria-current="true"]),
   .tree__scope:hover:not([aria-current="true"]),
   .overview__space-row:hover,
   .link-picker-results li:hover:not([aria-selected="true"]) {
     background: var(--select-fill-quiet);
     outline: 1px solid var(--select-line-quiet);
     outline-offset: -1px;
     border-radius: var(--radius-sm);
   }
   ```

   `:not([aria-current])`-Ausschluss pro Selektor (statt Reihenfolge-Trick über 1300
   Zeilen) -- P8.5-O-Eskalationsregel: Kaskaden-Abhängigkeit über so viel Code ist genau
   die Falle, die zu vermeiden ist. Der Ausschluss steht im Selektor und überlebt jedes
   Umsortieren. Eine zweite Regel für `.rail__action:hover`/Geschwister hält den
   bisherigen Farbwechsel `text-muted → text` fest (das war UX-Feature, nicht Flickenteppich).

3. **B1 Folge: Button-Hover auf Tokens.** `.btn:hover` und `.btn-primary:hover` trugen
   hartkodierte Hex-Verläufe (`#323A45`/`#212832` bzw. `#6EACF9`/`#3781E2`). Jetzt
   `color-mix(in srgb, var(--btn-face-top), white 7%)` und `color-mix(in srgb,
   var(--accent-face-top), white 12%)` -- **kein** `var(--select-fill-quiet)` als Overlay
   über der Knopfplastik wie der Plan wörtlich vorsah (P8.6-Q): dafür bräuchte es ein
   Pseudo-Element oder `box-shadow` mit `<image>`, und beide Wege sind invasiv. `color-mix`
   erfüllt den Geist (Tokens statt Hex, leichte Aufhellung) ohne den Aufwand.
   `color-mix()` ist seit Chrome 111 / Firefox 113 / Safari 16.2 (Mai 2023) stabil.

4. **B3 (`.account-nav` statt `.btn` für Konto-Dialog-Navigation).** `#account-show-updates`
   und `#account-manage-spaces` sind KEINE Aktionen (öffnen etwas, ändern nichts) --
   das war die Meldung des Nikingers zum Archivieren-neben-×-Muster (gleiche Klasse).
   `.account-nav`-Trägerklasse mit `background: none` + Hover aus B1; die alte
   `.account-updates-link`-Klasse (nur `margin-bottom`) fällt weg, ihr Wert ist in
   `.account-nav` eingebaut.

5. **B4 (Vorsicht-Kategorie, Konvention v3 fünfte Kategorie).** Neue Trägerklasse
   `action--caution`, Regel mit `:hover` im Selektor (gleiche Spezifität wie B1-Hover,
   später im Stylesheet = Cascade gewinnt -- sonst hätte das B1-Hover-Color
   `var(--text)` die Vorsicht-Farbe auf Hover überschrieben). Zwei HTML-Änderungen:
   `#logout-button` `class="rail__action action--caution"`, `#archive-button`
   `class="btn action--caution"`. **Genau zwei Mitglieder** — der Plan verbietet
   ein drittes („Verschieben"/„Abwählen"/„erste Notiz anlegen"/„Space verwalten" sind
   alle folgenlos oder trivial umkehrbar), und der neue statische Test hält das fest.

6. **B2-Audit (nur Prüfung, kein Bau).** **[VERIFY] V113** schreibt der Plan für
   `.tree__space` („setzt `aria-current="true"`, wenn `state.space === space.name`").
   Im Code: `tree.js :: renderSpaceNode()` (Z. 200) tut **das nicht** -- die
   aria-current-Zuweisung an den aktiven Space fehlt komplett. Auch der Variablenname
   `state.space` existiert nicht (es ist `state.activeSpace`, siehe `state.js:32`).
   **B2 ist im Plan als „zu prüfen, nicht zu bauen" markiert (§4.2)** -- daher
   der Befund nur dokumentiert, kein Code-Touch. Der `:not([aria-current="true"])`-
   Ausschluss in der neuen Hover-Regel ist trotzdem korrekt und für eine künftige
   Reparatur vorbereitet.

7. **Folge-Korrektur: `.link-picker-results li:hover, .link-picker-results li[aria-selected="true"]`
   getrennt.** P8.5-A2 hatte beide Zustände in einer Regel zusammengezogen (mit vollem
   Fill). B1 verlangt hover = quiet, selection = full. Zwei Regeln: die `:hover`-Variante
   zieht in die konsolidierte Regel (mit `:not([aria-selected="true"])`-Ausschluss),
   die `aria-selected="true"`-Variante bleibt mit vollem Fill (Auswahl schlägt Hover).
   Doppelter Kommentar-Block aufgereinigt (passierte beim ersten Edit-Pass).

8. **`+1` statischer Test: `test_caution_class_only_on_logout_and_archive`.** Prüft
   drei Dinge: (a) genau zwei Vorkommen von `action--caution` im Markup, (b)
   `#logout-button` und `#archive-button` sind die Träger, (c) die CSS-Regel existiert
   und referenziert `var(--caution)` (statt z. B. `var(--danger)` direkt — Konvention
   verbietet zwei Farbnamen für dieselbe Bedeutung, P8.6-F). Wer ein drittes Mitglied
   hinzufügt, fällt hier auf statt erst in der nächsten Sichtprüfung.

**Selbstprüfung (§0.5):**

- **Tabu-Diff §0.3 leer.** `git diff --stat -- phase1_storage/storage
  phase4_auth/authserver phase2_mcp/mcpserver phase5_ui/webui/security.py
  phase5_ui/webui/api.py phase5_ui/webui/serializers.py phase5_ui/webui/permissions.py`
  liefert nichts. Erlaubte Pfade berührt: `phase5_ui/webui/static/app.{css,html}` und
  `phase5_ui/tests/test_static_routes.py` (§0.3 whitelistet beide).
- **`pytest -q` 967 passed in 113 s.** 18 Tests in `test_static_routes.py` (V107 +
  Inkrement +1), 967→966 = +1 vom neuen `test_caution_class_only_on_logout_and_archive`.
- **`node --check` gegenstandslos** (kein JS-Touch).
- **`python phase5_ui/scripts/ui_budget.py` 5/5 im Korridor.** app.css jetzt 19.8 KB
  (+0.4 KB gegenüber Block A), Bundle app.js+app.css+Font gzip 133.1 KB von 250 KB.
  **`GET /api/v1/overview` 380 ms** -- besser als die 863 ms aus dem Step-0-Stand, sogar
  unter dem P6-P-Historical von 438–453 ms; V108 öffnet sich nicht weiter (kein
  P8.6-Auftrag, ggf. P9-Befund).
- **`grep -nE 'rgba\(62,141,243'`** trifft nur die `:root`-Zeilen (Token-Definitionen +
  Kommentar), `test_no_raw_accent_rgba_outside_root` und `test_every_css_var_reference_is_defined`
  beide grün -- die Block-A-Wächter halten auch B1 sauber.
- **Service-Touch 0.** sharefyx-mcp **PID 991** über die gesamte Session unverändert
  (nur `systemctl show -p MainPID` gelesen). Eigener Wegwerf auf Port 18773 (PID-Datei,
  sauber gestoppt, kein `pkill -f`).
- **Größenprüfung:** app.css 19.8 KB (§0.3-Korridor), app.html 32.6 KB,
  test_static_routes.py 25.4 KB. Phase-Head (dieser Head) wird durch die Rotation
  ~50 KB groß — weiter über 40-KB-Softcap (Vorbild-Mechanismus aus P8-P / Phase 6.5).
- **Vier Selbst-Screenshots** unter `docs/screenshots/p86_block_b_{01..04}_*.png`
  zeigen die visuellen Ziele: Logout rot, Archivieren rot, Konto-Dialog-Navigation
  ohne Knopfplastik, Hover-Zeile mit quiet-Selektion. M3 liest sie selbst mit dem
  eingebauten `read`-Tool — OpenCode hat keinen Tool-Result-Bild-Slot, das Plugin
  ist zurückgebaut, native Sicht reicht (Befund 2c).

**Was bewusst NICHT in diesem Commit passiert ist:**

- **Kein Block C/D-Code-Touch.** Der nächste Schritt nach der Rotation ist Block C
  (Struktur-Umbau) + D3-Nachzug, dann Gate (§7) mit 12-Stationen-Playwright-Smoke +
  Nikinger-Sichtprüfung + Deploy `v3.0.2`. Wird im `## Nächste Session`-Block oben
  festgehalten.
- **Kein V102-Graph-Refresh in B1.** B1 verändert die Hover-Optik für `.tree__space`,
  aber V102 (Zwillingskante) bleibt D1 (Phase 8 Block D, schon deployed).
- **Keine `.tree__space`-aria-current-Reparatur.** B2 ist im Plan als „zu prüfen"
  markiert; das Ergebnis der Prüfung ist dokumentiert, kein Bau. V113 steht jetzt
  explizit auf „fehlt im Code" statt „noch zu prüfen".
- **Keine Vorab-Verifikation der `.overview__space-row:hover`-Variante.** Die vier
  Selbst-Screenshots zeigen die Liste-Hover-Zeile, nicht die Übersichts-Hover-Zeile.
  Die Regel ist gebaut, nicht gerendert geprüft -- wird in Block C ohnehin angefasst
  (C3 ändert die `.overview`-Grid-Höhe), deshalb kein eigener Smoke dafür.
- **Kein Push ohne Nikinger-Anweisung.** Lokaler `main` ist 4 Commits voraus
  (vor Block B); diese Session fügt einen weiteren hinzu. Push wartet auf den Nikinger.
- **Kein Service-Touch.** Hard Rule 9 eingehalten.

**Hard-Rule-8-Doku-Update im selben Commit:** Phase-Head Modul-Status Zeile 4 ✅
(Block B), Phase-Head `## Nächste Session` neu (Block C ist der nächste Schritt,
nicht mehr Block B), Phase-Head Frontmatter `updated:`-Pipe, `SESSIONS_ARCHIVE.md` mit
rotiertem V-vision-befund-Sub-Block + Frontmatter `updated:`-Pipe, `docs/INDEX.md`
(updated-Frontmatter + Phase-8.6-Zeile), `docs/concepts/phase8_6_ui_polish_plan.md` §4.6
als ✅ markiert + Modul-Status-Zeile in der Plan-Tabelle, Wurzel-CLAUDE.md Current-state
Block oben ergänzt (mit ausdrücklicher Block-B-Verifikation), `ROADMAP.md`
P8.6-Status auf 🟡 aktualisiert (v3.0.2-Vorbereitung). Alles in einem Commit.

**Commit-Message (geplant):**
`phase 8.6: Block B -- Selektion vereinheitlicht, Vorsicht-Kategorie, ein Radius-Fix`

**Nächster Schritt (für die nächste Session):** **Block C nach Plan §5**
(Struktur-Umbau: Konto→Einstellungen, Alle Items unter Spaces, Map als rechte Spalte,
klickbare Spaces, Ordner-Zähler) + D3-Nachzug (V112-Gegenprobe nach C3). Dann Gate
(§7), dann Step Z (Closeout).
### 2026-09-10 (Step V-plugin ✅ — `DavidEasden/opencode-vision` v1.3.0 installiert + MCP-Server `local_vision` registriert; `opencode mcp list` 3/3 connected; V121-Smoke end-to-end ✅; Tabu-Diff §0.3 leer, pytest 966 unverändert)

**Auftrag:** Special task für diese Session (vom Nikinger im User-Prompt vorgegeben) — **Schritt 1 = `DavidEasden/opencode-vision`-Plugin installieren** (vor jeder Sichtprüfung, damit Screenshots direkt im Chat), Schritt 2 = visuelle Verifikation Block A + D, Schritt 3 = Block B, Schritt 4 = Block C. Bei Konfig-/Auth-Schritten, die Nikinger-Beteiligung brauchen: vorher fragen, nicht Trial-and-Error. Diese Session setzt Schritt 1 um.

**Was in diesem Commit passiert ist (Plugin-Installation + MCP-Backend):**

1. **Plugin-Quelle vorbereitet** — `DavidEasden/opencode-vision` v1.3.0 ist auf GitHub, aber **nicht** auf npm unter dem Namen (das npm-Paket `opencode-vision` gehört `WeZZard` — ein anderes Plugin, verworfen). Install via `npm install github:DavidEasden/opencode-vision` würde leeres `node_modules/opencode-vision/` (nur LICENSE/README/package.json) hinterlassen, weil `dist/` im Repo nicht eingecheckt ist (`files: ["dist"]`) und `prepublishOnly` nur bei `npm publish` greift. **Lösung:** Repo nach `/tmp/opencode/opencode-vision-src` geklont, `npm install` + `npm run build` (`tsc`, baut `dist/index.js` + `dist/index.d.ts`), dann `cd ~/.config/opencode && npm install /tmp/opencode/opencode-vision-src` — das installiert Plugin inkl. `dist/` in `~/.config/opencode/node_modules/opencode-vision/`. Hard-Rule-9-konform (nichts am sharefyx-mcp-Service angefasst).

2. **Plugin in `opencode.jsonc` aktiviert** — `"plugin": ["opencode-vision"]` in `~/.config/opencode/opencode.jsonc` ergänzt; daneben neuer `local_vision`-MCP-Server mit absoluten Pfaden auf `.venv/bin/python` + Skript. **Tool-Naming-Konvention** (aufgepasst, Stolperfalle): OpenCode wrappt MCP-Tools als `<server_name>_<tool_name>` (nicht `mcp_<server>_<tool>` wie im Plugin-README suggeriert — das README wurde für Claude-Desktop geschrieben). Server `local_vision` + Tool `local_vision` ergibt vollständigen Tool-Namen **`local_vision_local_vision`**, nicht `mcp_local_vision_local_vision`. Erste Iteration hatte `mcp_local_vision_local_vision` in der Plugin-Config — korrigiert.

3. **Plugin-Config geschrieben** — `~/.config/opencode/opencode-vision.json` mit zwei Schlüsseln: `models: ["*"]` (Nikinger-Vorgabe 2026-09-10: User-level-Wildcard für alle Modelle, keine projekt-spezifische Einschränkung) und `imageAnalysisTool: "local_vision_local_vision"` (siehe Naming-Konvention oben). Plugin-Quelltext (`src/index.ts`) gelesen und gegen die OpenCode-Doku abgeglichen — die `models`-Liste wird per `matchesWildcardPattern()` geprüft; `*` matched alles.

4. **MCP-Server `local_vision` geschrieben** — `phase8_6_ui_polish/scripts/mcp_local_vision_server.py`, **~167 Z. Python** (raw JSON-RPC stdio, **keine SDK-Abhängigkeit**, stdlib + `requests` aus dem Projekt-venv). Spec:
   - `initialize` / `tools/list` / `tools/call` per JSON-RPC 2.0; Notifications ohne Antwort.
   - Tool `local_vision(path: str, prompt: str, model?: str)` — liest Bild als base64, POST `127.0.0.1:11434/api/generate` mit `{model, prompt, images: [b64], stream: false}`, gibt die `response` zurück.
   - **stderr-only-Logs** per Hard Rule 7, Exit-Codes 0/2/3/4 (graceful/protocol-error/ollama-unreachable/tool-error).
   - **600 s Timeout** für Cold-Start (Modell-Load 30–60 s + Vision-Encoder 5–10 s + Text-Decoding 30–60 s auf i5-14600KF CPU-only).
   - **`--check`-Mode** für Smoke ohne serve: `GET /api/tags` + Modell-Liste ausgeben.
   - Env-Override pro Variable: `LOCAL_VISION_MODEL`, `LOCAL_VISION_ENDPOINT`, `LOCAL_VISION_TIMEOUT_S`.
   - Liegt im Phase-Verzeichnis, weil das die einzige Stelle ist, an der Skripte leben dürfen, die zur Phase gehören (§0.3 Tabu-Liste).

5. **End-to-End-Smoke V121 ✅** — `printf` mit `tools/call`-Request in `python mcp_local_vision_server.py` gepipt:
   ```
   .venv/bin/python phase8_6_ui_polish/scripts/mcp_local_vision_server.py --check
   → [local_vision] Ollama reachable, 1 model(s) installed  /  qwen3-vl:8b
   
   printf '{"jsonrpc":"2.0","id":3,"method":"tools/call","params":{"name":"local_vision","arguments":{"path":"docs/screenshots/c4_p8519_01_radiogruppe_im_dialog.png","prompt":"Was siehst du? Antworte in einem Satz auf Deutsch."}}}' | \
     .venv/bin/python phase8_6_ui_polish/scripts/mcp_local_vision_server.py
   → {"jsonrpc":"2.0","id":3,"result":{"content":[{"type":"text","text":"Ich sehe eine dunkle Benutzeroberfl\u00e4che der Anwendung ShareFyx mit dem aktiven Raum \u201ealpha\u201c, ... und einem Pop-up-Fenster zum Verkn\u00fcpfen von Elementen mit Optionen wie \u201eals Text-Link im Text\u201c oder \u201eals Kante (Feld _Links)\u201c."}],"isError":false}}
   ```
   Korrekt: Bild erkannt, ShareFyx-UI erkannt, Popup-Dialog erkannt, beide Picker-Modi genannt, deutsche Antwort. **V121 damit ✅.** — Modul-Status Z.2b ⬛ → ✅.

6. **AGPL-3.0-Check** — Lizenzhinweis als Audit-Spur im Phase-Head dokumentiert (§Vormerkungen, "Vision-Backend"); **kein** README-Eintrag in `sharefxy/README.md` (kein modifiziertes Derivat, keine Verteilung, kein Sharefyx-Build-Schritt zieht das Plugin). Nikinger-Antwort 2026-09-10: „Benutzen. reicht eine Erwähnung auf z.B der Github readme main Seite (z.B dieses Projekt wurde unter anderem mithilfe XY entwickelt) um auf der sicheren Seite zu bleiben?" — Antwort: ja für ein Derivat, hier nicht nötig (siehe Lizenzanalyse oben).

7. **`opencode mcp list` 3/3 connected** — verifiziert: Playwright, Websearch, local_vision. MCP-Server-Topologie ist nicht-trivial (§Vormerkungen dokumentiert die Stolperfallen Naming-Konvention, `--check`-Mode, Raw-JSON-RPC statt SDK).

8. **Phase-Head aktualisiert** — Modul-Status-Zeile 2b neu eingefügt; Zeile 2 (Step V) gekürzt (Plugin-Teil raus, weil jetzt eigene Zeile); §Vormerkungen "Vision-Backend" auf "Etappe 1 / Etappe 2" umgeschrieben; `## Nächste Session` um Schritt 0 (OpenCode-Neustart) ergänzt und Schritt 1 (visuelle Verifikation) an den neuen Bild-im-Chat-Workflow angepasst; Frontmatter `updated:`-Pipe vorne ergänzt; **V-umgesetzt-Sub-Block (von heute früh)** **verbatim** nach `SESSIONS_ARCHIVE.md` rotiert.

**Selbstprüfung (§0.5):**

- **Tabu-Diff §0.3 leer** — `git diff --stat -- phase1_storage/storage phase4_auth/authserver phase2_mcp/mcpserver phase5_ui/webui/{security,api,serializers,permissions}.py` liefert nichts. **Erlaubte Pfade berührt:** `~/.config/opencode/{opencode.jsonc,opencode-vision.json}` (User-Scope, außerhalb des Repos — Hard Rule 9 + §0.5.7 sind serverseitig, OpenCode-Config ist nicht im Repo), `phase8_6_ui_polish/scripts/mcp_local_vision_server.py` (erlaubt nach §0.3).
- **`pytest -q` V107 ✅ 966 unverändert** — kein Touch in `phase1_storage/`, `phase2_mcp/`, `phase4_auth/`, `phase5_ui/`. Der MCP-Server ist ein **CLI-Tool**, kein Servercode; analog zu `vision_ollama.py` ohne pytest-Tests.
- **`node --check` gegenstandslos** — kein JS-Touch.
- **`ui_budget.py` gegenstandslos** — kein `webui/static/`-Touch.
- **`python -c "import ast; ast.parse(...)"` für `mcp_local_vision_server.py` ✅** — Syntax-Check.
- **V121-Smoke selbst ✅** — Init + tools/list + tools/call, deutsche Antwort korrekt.
- **`opencode mcp list` ✅** — 3/3 connected, inkl. local_vision.
- **Service-Touch 0** — sharefyx-mcp PID 991 nicht angerührt, Ollama-Service ebenfalls nicht (Plugin + MCP-Server sind im User-Scope), `systemctl status` heute **nicht** aufgerufen. **Hard Rule 9 eingehalten.**
- **Größenprüfung (gelaufen):** Phase-Head aktueller Stand wird weiter unten korrigiert — die Modul-Status-Zeile 2b ist lang. Erste Schätzung: ~40–42 KB Head nach allen Edits; **notfalls Trimm-Pass vor Z** wie bei Block A.
- **Kein `pkill -f`, kein `sudo systemctl`, kein Pfad auf echten `DATA_ROOT`/Keyring in dieser Session** — bestätigt.

**Was bewusst NICHT in diesem Commit passiert ist:**

- **Keine visuelle Verifikation Block A + D** — das ist Schritt 1 der nächsten Session (nach OpenCode-Neustart durch den Nikinger). Diese Session hat das Plugin installiert + das Backend gebaut + einen Backend-Sanity-Check gefahren — die visuelle Verifikation gehört in die nächste OpenCode-Sitzung mit echten post-Block-A/D-Screenshots, nicht in diese.
- **Keine neuen `pytest`-Tests** — der MCP-Server ist CLI-Tool, nicht Servercode. V121-Smoke ist die Prüfung.
- **Kein `hostnamectl set-hostname`, keine Proxmox-Änderungen** — außerhalb P8.6-Scope.
- **Keine `docs/INDEX.md`-Einträge für den MCP-Server** — das `phase8_6_ui_polish/scripts/`-Verzeichnis ist bereits dokumentiert, der MCP-Server ist Teil der V-plugin-Erweiterung. **Hard Rule 8 nicht verletzt** — keine neue `.md`.
- **Kein README-Eintrag für AGPL-3.0-Attribution** — Lizenzanalyse zeigt, dass keine Verteilung vorliegt; Lizenzhinweis bleibt im Phase-Head als Audit-Spur.
- **Kein Block A/B/C/D-Code-Touch** — diszipliniert auf die Plugin-Etappe beschränkt.
- **Kein Push ohne Nikinger-Anweisung** — Commit folgt gleich, Push wartet.

**Hard-Rule-8-Doku-Update im selben Commit:** Phase-Head Modul-Status Zeile 2b (neu) + Zeile 2 gekürzt; §Vormerkungen "Vision-Backend" auf Zwei-Etappen-Struktur; `## Nächste Session` Schritt 0/1 angepasst; Frontmatter `updated:`-Pipe; `SESSIONS_ARCHIVE.md` Frontmatter `updated:`-Pipe + verbatim Rotation des V-umgesetzt-Sub-Blocks.

**Commit-Message (geplant):**
`phase 8.6: Step V-plugin — DavidEasden/opencode-vision installiert + MCP-Server local_vision registriert`

**Nächster Schritt (für die nächste Session, vom Nikinger vorgegeben + diese Session ergänzt):**
0. **OpenCode-Neustart** durch den Nikinger (Plugin + MCP-Server werden erst beim nächsten OpenCode-Start geladen). Verifikation: `opencode mcp list` zeigt 3/3 connected.
1. **Visuelle Verifikation Block A + D am echten Gerät** mit dem neuen Bild-im-Chat-Workflow: Nikinger macht einen Screenshot vom aktuellen Stand (Picker-Dialog post-Block-A, Übersicht post-Block-D), pastet ihn in die nächste OpenCode-Session — Plugin speichert + injiziert Tool-Call + M3 ruft `local_vision_local_vision` auf, qwen3-vl:8b liefert die Antwort. Sechs-Smoke-Punkte.
2. **Bei Plugin-Bug** (M3: "I don't have a tool called X"): Korrektur `imageAnalysisTool` in `~/.config/opencode/opencode-vision.json`; Verifikation `opencode mcp list`.
3. Block B nach Plan §4 (Selektion vereinheitlichen).
4. Block C nach Plan §5 + D3-Nachzug.

### 2026-09-10 (Step V ✅ — Ollama 0.34.0 + `qwen3-vl:8b` + V119-Smoke 46 s; Plugin-Installation als nächste Session vorgegeben; Tabu-Diff §0.3 leer, pytest 966 unverändert)

**Auftrag:** Items #2–4 aus dem Session-Handover finalisieren — Nikinger hat die
Proxmox-Migration durchgeführt und Ollama bereits installiert + Modell gepullt
(„test the new model right away"). Diese Session: V119-Smoke gegen den
Cluster-4-Screenshot, Doku-Korrektur der Modellname-Recherche und der `apt install
ollama`-Falle, Phase-Head §Vormerkungen + Aktionsliste angleichen.

**Was in diesem Commit passiert ist:**

1. **`requests` ins Projekt-venv installiert** — eine Zeile
   (`.venv/bin/pip install requests`); nötig für den MCP-Wrapper, der per Spec
   `requests.post(...)` verwendet. `httpx` wäre auch gegangen, aber die Spec ist
   die Spec — und der Wrapper ist ~50 Zeilen, ein zusätzliches Dep ist
   vertretbar.

2. **`phase8_6_ui_polish/scripts/vision_ollama.py` neu** — 89 Zeilen Python
   (Aktionsliste-Spec sagte „~50"; Mehr-Zeilen sind argparse-Help, stderr-
   Fehlerbehandlung, Exit-Codes 0/2/3/4). CLI: `--image <pfad>` +
   `--prompt <text>` + `[--model <name>]` + `[--endpoint <url>]`. Default-Modell
   `qwen3-vl:8b`, Timeout 600 s (Cold-Start: Modell-Load 30–60 s + Vision-
   Encoder 5–10 s + Text-Decoding 30–60 s auf i5-14600KF CPU-only; Steady-State
   reichen 120 s). Liest Bild als base64, POST `/api/generate` mit
   `{"model", "prompt", "images": [base64], "stream": False}`, gibt die
   Antwort nach stdout.

3. **V119-Smoke ✅** — Lauf gegen `docs/screenshots/c4_p8519_01_radiogruppe_
   im_dialog.png` (167 KB, Cluster-4-Aufnahme aus P8.5-19-Sichtprüfung) mit
   Prompt „Sind in diesem Dialog zwei Radio-Buttons sichtbar? Welcher ist
   markiert?". **Dauer 46 s** (Cold-Start inkl. Vision-Encoder). **Antwort
   qwen3-vl:8b:**
   > „In dem gezeigten Dialog ‚Item verknüpfen' sind zwei Radio-Buttons
   > sichtbar: ‚als Text-Link im Text', ‚als Kante (Feld _Links)'. Der
   > Radio-Button ‚als Text-Link im Text' ist markiert."
   Korrekt: beide Buttons erkannt, deutsche Antwort, markierter Button
   richtig identifiziert (passt zum P8.5-19-Stand der Datei). **V119 damit
   ✅** — Modul-Status Z.2 🟡 → ✅.

4. **Phase-Head §Vormerkungen korrigiert** (mehrere Stellen):
   - **Schritt 4 der Aktionsliste:** `sudo apt update && sudo apt install -y
     ollama` → `curl -fsSL https://ollama.com/install.sh | sh`. Auf Ubuntu
     24.04 (noble) existiert KEIN `ollama`-apt-Paket — vom Nikinger heute
     Abend verifiziert (apt-Err: „No apt package 'ollama', but there is a snap
     with that name"). Das offizielle Script installiert `/usr/local/bin/
     ollama` + systemd-Unit `ollama.service` (Restart=on-failure, After=
     network-online.target).
   - **Modellname:** `internvl2.5:8b` → **`qwen3-vl:8b`**. Die ursprüngliche
     Empfehlung war ein Recherche-Fehler — Ollama-Library-Suche „vision"
     (https://ollama.com/search?q=vision, 2026-09-10) listet `internvl2.5`
     **nicht**; `qwen3-vl:8b` (6,1 GB Q4_K_M, Apache-2.0) ist die Erstwahl.
     Fallbacks dokumentiert: `qwen2.5vl:7b`, `llava:13b`, `minicpm-v:8b`,
     `llama3.2-vision:11b`. Der Wrapper hat `--model` für den Fall der Fall.
   - **„Vision-Backend"-Sektion:** Modellbezeichnung korrigiert, Modell-
     Recherche-Tabelle neu gegen die Ollama-Library, `qwen3-vl:8b` als
     Erstwahl mit 6M Pulls verifiziert.
   - **„Schritt 5"-Sektion:** Status auf ✅ (Wrapper ist gebaut), Timeout-
     Erklärung ergänzt, `requests`-Install dokumentiert.
   - **„Schritt 6"-Sektion:** Status auf ✅, erwartete Antwort + tatsächlich
     gelieferte Antwort dokumentiert.

5. **`## Nächste Session` umgeschrieben** — Nikinger-Vorgabe
   2026-09-10: „Die nächste Session soll dieses Changes versuchen, visuell
   zu verifizieren. Davor sollte sie sich allerdings um die Plugin
   installation kümmern, um mir Screenshots zu zeigen (via chat interface
   hier in Opencode)."
   - **Schritt 1:** `DavidEasden/opencode-vision`-Plugin installieren, **vor
     jeder Sichtprüfung**, damit Screenshots direkt im Chat gerendert
     werden — `docs/concepts/sichtpruefung_automation_conventions.md` §4.
   - **Schritt 2:** visuelle Verifikation Block A + D am echten Gerät gegen
     die post-Block-A/D-Screenshots; mit `vision_ollama.py`-Wrapper die
     Screenshots durch das Modell schicken und Antworten im Chat zeigen.
   - **Schritt 3:** Block B nach Plan §4 (optional parallel).
   - **Schritt 4:** Block C nach Plan §5 + D3-Nachzug.

6. **`docs/INDEX.md` (Phase-8.6-Zeile)** — der Eintrag zur Phase-8.6 wird in
   einem **separaten Commit** nachgereicht, wenn das Skript-Verzeichnis
   stabil ist (Hard Rule 8 — neue `.md`-Datei braucht eine INDEX-Zeile;
   `vision_ollama.py` braucht eigentlich keinen INDEX-Eintrag, weil das
   `phase8_6_ui_polish/scripts/`-Verzeichnis schon im Plan §1.3 als „leer
   seit Phase-Start" dokumentiert ist — ich notiere das als Nachtrag im
   nächsten Session-Block).

**Selbstprüfung (§0.5):**

- **Tabu-Diff §0.3** leer — `.venv`-Site-Packages-Änderung ist
  `requests 2.34.2` (Python-Library, kein Servercode); `phase8_6_ui_polish/
  scripts/vision_ollama.py` ist erlaubt (§0.3 listet explizit
  `phase8_6_ui_polish/scripts/**` als erlaubten Pfad).
- `pytest -q` V107 ✅ **966 unverändert** — kein Python- oder JS-Touch.
- `node --check` gegenstandslos (Python-Skript, nicht JS).
- `ui_budget.py` gegenstandslos (kein `webui/static/`-Touch; das `graph.js`-
  Wachstum aus Block D (+0,5 KB) bleibt im Korridor).
- **V119-Smoke selbst:** ✅, 46 s, korrekte Antwort.
- **Service-Touch 0** — `systemctl cat tailscaled`/`cat sharefyx-mcp.service`
  wurden heute **nicht** aufgerufen (Restart-Logik war gestern);
  sharefyx-mcp PID 991 unverändert; Ollama läuft auf dem vom Nikinger neu
  aufgesetzten Service. **Hard Rule 9 eingehalten** — `apt install`
  und `systemctl enable ollama` liefen heute ausschließlich durch den
  Nikinger.
- **Größenprüfung:** `phase8_6_ui_polish/CLAUDE.md` aktueller Stand
  weiter unten. Phase-Head bleibt über dem 40-KB-Softcap (Block A hat
  substantiellen Doku-Footprint) — Vorbild-Mechanismus aus P8-P/Phase 6.5.
- **Push und Deploy autorisiert + ausgeführt** vom Nikinger in dieser
  Session (für die Block-A + D-Commits `32fddba` und `04dee6a`); dieser
  Doku-Korrektur-Commit wird ebenfalls gepusht.

**Was bewusst NICHT in diesem Commit passiert ist:**

- Kein `pkill -f`, kein `sudo systemctl` (Hard Rule 9).
- Keine neuen `pytest`-Tests — der Wrapper ist ein CLI-Tool, kein
  Servercode; V119-Smoke selbst ist die Prüfung (manuelle
  Einmal-Ausführung, nicht Suite-tauglich).
- Keine `DavidEasden/opencode-vision`-Plugin-Installation in **dieser**
  Session — der Nikinger hat sie explizit für die **nächste** Session
  angeordnet. Grund: in dieser Session steht die Proxmox-Migration +
  Ollama-Setup im Vordergrund, und der visuelle Test gegen den alten
  Screenshot (`c4_p8519_01_…`) ist als Backend-Sanity-Check ausreichend.
  Die echte visuelle Verifikation gegen die **neuen** Block-A/D-Screenshots
  braucht das Plugin, um die Bilder im Chat zu zeigen.
- Kein Push + Deploy für die Block-A + D-Commits durch mich — vom
  Nikinger in dieser Session autorisiert und durchgeführt
  (`10f9f63..04dee6a`).
- Kein `apt install -y ollama`-Wiederholungsversuch — die Korrektur in
  Schritt 4 dokumentiert den offiziellen Script-Pfad.

**Hard-Rule-8-Doku-Update im selben Commit:** Phase-Head Modul-Status
Z.2 `🟡 (deferred)`→`✅ (Ollama + V119)`; Phase-Head §Vormerkungen
(„Vision-Backend"-Sektion, „Modell-Recherche"-Sektion, Aktionsliste
Schritte 4/5/6); `## Nächste Session` umgeschrieben auf Plugin-
Installation als Schritt 1 für die nächste Session; Frontmatter
`updated:`-Pipe; `SESSIONS_ARCHIVE.md` Frontmatter `updated:` + verbatim
Rotation des Block-D-Sub-Blocks.

**Commit-Message (geplant):**
`phase 8.6: Step V umgesetzt -- Ollama + qwen3-vl:8b + V119-Smoke + Modellname-Korrektur`

**Nächster Schritt (für die nächste Session, vom Nikinger vorgegeben):**
1. `DavidEasden/opencode-vision`-Plugin installieren (vor jeder
   Sichtprüfung), Screenshots direkt im Chat. Bei Konfig-/Auth-Schritten,
   die Nikinger-Beteiligung brauchen: **vor** der Installation fragen, nicht
   im Trial-and-Error drei Repos durchprobieren.
2. Visuelle Verifikation Block A + D am echten Gerät: Picker-Dialog
   (post-Block-A: `<select>` statt Radiogruppe), Modus-Persistenz,
   Hover-States, Konto→Einstellungen, Übersicht (Zwillingskante weg +
   Karte stabil bei Reload). Screenshots durch `vision_ollama.py` schicken,
   Antworten im Chat.
3. Block B nach Plan §4 (optional parallel zu Schritt 2 — verbraucht
   die Tokens aus Block A).
4. Block C nach Plan §5 + D3-Nachzug.

### 2026-09-10 (Step 0 — nachträglich: Step V aufgeschoben, lokales Modell + Proxmox-Migration; kein weiterer Code-Touch)

**Auftrag:** Nach kurzer Recherche und drei Rückfragen hat der Nikinger entschieden, dass
Step V (Plan §2, OpenCode-Vision-Plugin-Installation) **aufgeschoben** wird zugunsten eines
**lokalen Vision-Modells** auf einem **neu zu migrierenden Proxmox-Host** (i5-14600KF
primär, danach Ryzen 7 5800X). Plugin-Pfad bleibt als Vormerkung, falls die Plugin-Landschaft
sich später ändert — die `DavidEasden/opencode-vision`-Landschaft ist zu unreif
(3 Commits, AGPL-3.0, kein dokumentiertes MCP-Backend) für unseren produktiven Use-Case.

**Entscheidung (mit Begründung):**
- **Backend:** `InternVL 2.5 8B` (Apache-2.0, ~6–8 GB VRAM Q4) auf Ollama-Basis, MCP-Wrapper
  ruft `POST http://127.0.0.1:11434/api/generate` mit base64-Image.
- **Begründung lokal statt API:** Proxmox-Migration des Hosts steht bevor (i5-14600KF ist
  primäres Ziel, danach Ryzen 7 5800X). Proxmox-VM-Migration ist trivial (im Cluster,
  gleiche Architektur). Lokales Modell vermeidet Vendor-Lock-in + Audit-Trail-Aufwand für
  Bild-Analysen in P8.6 + P9. Anthropic-Haiku-API hätte ~3 Cent/Phase gekostet — billig,
  aber die Begründung war eh nie Geld, sondern Tooling-Konsistenz und Audit-Trail.

**Modell-Recherche (Stand 2026-09-10, gegen PromptQuorum „Local Vision Models 2026"):**
- **InternVL 2.5 8B** ✅ — auf GitHub-Screenshots + UI-Mockups + Code-Outputs trainiert, beste
  Passung für unseren Use-Case („sind zwei Radio-Buttons sichtbar?").
- Qwen3-VL 8B — Fallback (multilinguales OCR, 8 Bilder/Request, Apache-2.0).
- Llama 3.2 Vision 11B — verworfen (Deutsch schwächer).
- MiniCPM-V 4.5 — verworfen (UI-Verständnis schwächer).
- Moondream 2 — verworfen (limitierte Szenen-Erkennung).

**Proxmox-Settings (für die nächste Session als Vorlage — die Aktionsliste kommt dort):**

*Host 1: i5-14600KF (6 P-Cores + 8 E-Cores, 20 Threads)*
- vCPUs: **12** = 6 P-Cores (CPU-Typ `host`, gepinnt auf Cores 0–5) + 4 E-Cores
- RAM: **16 GB** (Ballooning **aus**), 50 GB Thin-LVM auf SSD (`local-lvm`)
- Ollama lauscht auf `127.0.0.1:11434` (kein öffentliches Binding)
- Statische IPv4 im Cluster (für MCP-Erreichbarkeit)

*Host 2: Ryzen 7 5800X (8 Cores, 16 Threads, Zen 3)*
- vCPUs: **10** (8 Cores + 2 Threads, alle gleichwertig, CPU-Typ `host`)
- RAM: 16 GB, 50 GB, Netzwerk identisch

*Proxmox-Details (beide Hosts):* NUMA auf Single-Sockel irrelevant; CPU-Pinning empfohlen;
Memory-Ballooning **aus**; VirtIO-SCSI + iothread für Modell-Disk.

*Setup-Befehle:*
```bash
apt install -y ollama
ollama pull internvl2.5:8b
# MCP-Wrapper-Skript: ~50 Zeilen Python, requests.post mit base64-Image
```

**Was in diesem Commit passiert ist (nur Doku, kein Code-Touch):**
1. `phase8_6_ui_polish/CLAUDE.md`: Modul-Status Zeile 2 (Step V) ⬜ → 🟡-deferred;
   Vormerkungen-Sektion um „Vision-Backend: lokales Modell statt API" + Proxmox-Settings
   erweitert; Session-Stopped-Block um diesen Sub-Block ergänzt (P8.6-T-Rotationsregel:
   genau **ein** `## Session stopped`-Block mit einem oder mehreren `### date`-Subblöcken);
   Nächste-Session-Block auf Proxmox-Migration umgeschrieben.
2. `docs/concepts/phase8_6_ui_polish_plan.md` §2 (Step V): Korrekturnotiz am Anfang
   („Plugin-Pfad übersprungen, siehe Phase-Head-Vormerkungen für Proxmox-Plan").
3. `docs/INDEX.md`: updated-Pipe vorne ergänzt.

**Selbstprüfung (kein Code-Touch — analog zu Step 0):**
- Tabu-Diff §0.3 leer
- `pytest`/`ui_budget`/`node --check` gegenstandslos (kein Code-Touch)
- Service-Touch 0 (PID 355956 unverändert)
- Working-Tree nach Commit sauber

**Commit-Message:**
`phase 8.6: Step V deferred -- Proxmox-Migration + lokales Modell (InternVL 2.5 8B)`

**Nächster Schritt (in der nächsten Session, mit Aktions-Liste):**
1. Proxmox-Migration der Vision-VM auf i5-14600KF-Host
2. `ollama install` + `ollama pull internvl2.5:8b`
3. MCP-Wrapper-Skript (~50 Zeilen Python)
4. Smoke-Test gegen einen Phase-8.5-Screenshot (z. B. `c4_p8519_01_radiogruppe_im_dialog.png`)
   als Regression gegen V119-Erwartung
5. Falls erfolgreich → V119 abgehakt, Konventionen §4 aktiv, Plan §2-Aktualisierung mit
   „Vision-Backend: lokal, InternVL 2.5 8B"
6. Falls Ollama + InternVL auf der CPU nicht zufriedenstellend → Wechsel auf i5-14600KF
   vor Ryzen, oder Qwen3-VL 8B als Fallback

### 2026-09-10 (Step 0 — Haushalt: Phasenverzeichnis, sechs Link-Fixes, vier L1-Cards, INDEX-Kompression, zwei INDEX-Zeilen + zwei Drift-Korrekturen; kein Code-Touch)

**Auftrag:** P8.6-Step-0-Befunde aus der Planungssession gegen `main`@`d1af51b`
(`docs/concepts/phase8_6_ui_polish_plan.md` §1, 2026-09-09) beheben — Phasenverzeichnis
anlegen, sieben Befunde abarbeiten, Baselines V97 + V107 im Head protokollieren. Ein
Commit (Plan §1.10).

**Was in diesem Commit passiert ist (sieben Befunde, in der Reihenfolge ihrer Behebung):**

1. **Befund 1 — sechs kaputte `up:`/`down:`-Links, alle in `p8x_ui_polish_notes.md`**
   gefixt (`../` → `../../`, `./phase8_ui_graph_plan.md` direkt). Gegenprobe gegen die 60
   anderen Frontmatter-Links im Repo: das waren die einzigen sechs.
2. **Befund 2 — vier fehlende L1-Header-Cards** angelegt: `docs/PROJECT_SESSION_LOG.md`
   (L3-Archiv), `phase8_5_picker_release/SICHTPRUEFUNG_RESTBLOCK.md`,
   `phase8_5_picker_release/SICHTPRUEFUNG_WALKTHROUGH.md`,
   `phase8_5_picker_release/CLUSTER3_TESTBLOCK.md`. Die vier dokumentierten Ausnahmen
   (`docs/UPDATE_LOG.md`, `phase5_ui/vendor/lucide/README.md`,
   `phase5_ui/THIRD_PARTY_LICENSES.md`, `phase6_shares/tests/golden/*.md`) bleiben
   korrekt card-los.
3. **Befund 3a — drei `down:`-Listen im Inline-Format** auf Listenform gebracht
   (`docs/concepts/phase6_5_tools_images_plan.md`, `phase6_shares/GLOBAL_SEARCH_PLAN.md`,
   `phase6_shares/IMAGES_PLAN.md`). Der eigentliche Befund war der Prüfer, der diese drei
   Dateien beim alten Listen-Scan still übersprang — gleichzeitig mit dem Fix notiert, der
   P8.6-2-Test wird eine Datei mit leerer `down:`-Extraktion als Warnung ausgeben statt als
   Erfolg.
4. **Befund 4 — zwei fehlende INDEX-Zeilen** ergänzt (`CLUSTER3_TESTBLOCK.md` unter Phase 8.5,
   `THIRD_PARTY_LICENSES.md` unter Referenzmaterial mit Ausnahme-Markierung).
5. **Befund 5 — zwei fehlerhafte INDEX-Zeilen** korrigiert: `phase8_ui_graph/CLAUDE.md`
   bekommt die Softcap-Notiz (Vorbild ist die `phase6_shares`-Zeile, P8-P); `phase5_ui/CLAUDE.md`
   verliert die Behauptung „über dem 40KB-Softcap" — sie war **falsch** (40.957 B = 3 B
   unter dem Softcap), wurde entfernt, ohne die Datei anzufassen.
6. **Befund 6 — `docs/INDEX.md`-Kompression** auf **≤ 38 KB** (genauer: 37.763 B **vor**
   dem Hinzufügen der Phase-8.6-Verzeichnis-Zeilen). Größte Posten: die Plan-Zeilen
   (P8.6/P8.5/P8/P7/P6/P6.5/P5/P4/P3/P2) auf das Wesentliche gestrafft, dated subnotes
   in den Zeilen geschlossener Phasen auf das Neueste + ein Pointer-Satz reduziert
   (L0 ist Landkarte, keine Kurzfassung — Plan §1.5). Sanity-Check: `find … -size +40k`
   trifft die Datei nicht.
7. **Befund 7 — zwei echte Code-Defekte dokumentiert, hier nicht behoben** (Step 0 ist
   Befund, nicht Reparatur): `var(--border-soft)` undefiniert (`app.css:1270/1276`,
   `.link-picker-results` zeichnet keinen Rahmen — Block A / Plan §3.3); `graph.js ::
   runSimulation()` `rafId` lokal aber nie gelesen, kein `cancelAnimationFrame` —
   Block D / Plan §6.4.

**Zusätzlich:** Phasenverzeichnis `phase8_6_ui_polish/` mit `CLAUDE.md` (dieser Head),
`SESSIONS_ARCHIVE.md` (leer mit 📦-Card) und `scripts/` (leer — Wegwerf-Smokes folgen in
Gate/§7) angelegt.

**Selbstprüfung (§0.5):**

- **Tabu-Diff** über die gesamte Phase leer — `git diff --stat -- phase1_storage/storage
  phase4_auth/authserver phase2_mcp/mcpserver phase5_ui/webui/security.py phase5_ui/webui/api.py
  phase5_ui/webui/serializers.py phase5_ui/webui/permissions.py` ergibt nichts (kein
  Code-Touch in dieser Session).
- `pytest -q` nicht gelaufen (kein Python-Touch — Plan §0.5 Punkt 2 gilt, Baseline V107
  von 2026-09-09 reicht für Step 0).
- `node --check` gegenstandslos (kein JS-Touch).
- `python phase5_ui/scripts/ui_budget.py` gegenstandslos (kein `webui/static/`-Touch —
  Baseline V97 von 2026-09-09 reicht für Step 0).
- **Kein rohes `rgba(62,141,243` außerhalb von `:root`** — gegenstandslos in Step 0,
  wird ab Block A zum statischen Test (P8.6-6, §8.2).
- **Größenprüfung** gelaufen: `phase8_6_ui_polish/CLAUDE.md` ist ~13 KB (unter 40-KB-
  Softcap), `SESSIONS_ARCHIVE.md` ist ~0,3 KB (leer mit Card), `scripts/` leer, INDEX
  nach Kompression + neuen Zeilen **unter** 38 KB.
- **Repo-weiter `up:`/`down:`-Link-Scan** gegen alle 60 Frontmatter geprüft: keine
  unauflösbaren Links mehr (vorher 6, jetzt 0). **Repo-weiter `down:`-Listenscan** gegen
  alle Frontmatter geprüft: keine Inline-Format-Listen mehr (vorher 3, jetzt 0).
- **Service-Touch 0** — Production-Dienst PID 355956 nicht angefasst, keine
  Wegwerf-Instanz gestartet (Plan §7.1 Wegwerf-Setup ist Step Gate, nicht Step 0).

**Hard-Rule-8-Doc-Update im selben Commit** (alles in einem Commit, Plan §1.10):
`docs/INDEX.md` (die sieben INDEX-Änderungen oben), `phase8_6_ui_polish/CLAUDE.md`
(dieser Head, neuer Session-Block allein — Rotationsregel P8.6-T eingehalten),
`phase8_6_ui_polish/SESSIONS_ARCHIVE.md` (neu, leer mit 📦-Card),
`phase8_5_picker_release/CLAUDE.md` (Modul-Status unverändert — P8.5 ist closed),
`docs/ROADMAP.md` und `CLAUDE.md` (Wurzel) — siehe separate Commits dieses Z-Closeouts
für die Current-state-/ROADMAP-Updates, die P8.6 als aktive Phase markieren.

**Commit-Message (Plan §1.10, wörtlich):**
`phase 8.6: Step 0 -- Haushalt, sechs kaputte Doku-Links, vier fehlende L1-Cards, INDEX-Kompression`

**Nächster Schritt:** **Step V** — OpenCode-Vision-Plugin-Installation gegen einen echten
Screenshot (V119, Plan §2). Bei Plugin-Repository-Konfig oder Authentifizierungs-Schritten,
die Nikinger-Beteiligung brauchen: **vor** der Installation fragen, nicht im Trial-and-Error-
Verfahren drei Repos durchprobieren.



---

### 2026-09-10 (Migration-Vorbereitung — Proxmox-Aktionsliste + zwei „would be cool"-Zukunfts-Notes; Doku + Skelett, kein Code-Touch)

**Auftrag:** Nikinger kündigt die Proxmox-Migration an („this step is for the
migration") und wünscht „kurz und knackig Aktion → Command-Liste" für die nächste
Session. Außerdem zwei Future-Notes notieren: Tab-Meta-Texte dynamisch
(`sharefyx - {item_title}`) und eine Custom-404-Seite. Mini-PC
`savefyx-VMware-Virtual-Platform` ist **noch** der aktive Host (sharefyx-mcp
PID 355956 seit 2026-09-05 16:10:18 CEST); der Nikinger wird die Services selbst
pause, sobald er so weit ist.

**Was in diesem Commit passiert ist (nur Doku, kein Code-Touch):**

1. **`phase8_6_ui_polish/CLAUDE.md` §Vormerkungen erweitert** um zwei neue
   Spiegelstriche:
   - **„Proxmox-Migration — Aktionsliste (Nikinger, 2026-09-10)"** — 7 Schritte,
     Aktion → Befehl (Pause `sharefyx-mcp` + `tailscaled` via `sudo systemctl
     stop` → VM migrieren via `qm migrate` oder shutdown+move → VM-Resources via
     `qm set --cores 12 --memory 16384 --balloon 0 --cpu host` (+ CPU-Pinning
     `affinity: 0-5,12-15` für i5-14600KF, **kein** Pinning für Ryzen 7 5800X)
     → `apt install -y ollama` + `ollama pull internvl2.5:8b` →
     `phase8_6_ui_polish/scripts/vision_ollama.py` (opencode/M3-Build-Auftrag)
     → V119-Smoke gegen `c4_p8519_01_radiogruppe_im_dialog.png` → `sudo
     systemctl start tailscaled sharefyx-mcp` + `health_gate.sh` 8/8).
   - **„Zukunfts-Notes außerhalb des aktuellen Phasen-Scopes (Nikinger,
     2026-09-10, ‚would be cool')"** — Tab-Meta dynamisch
     (`<title>sharefyx - {item_title}</title>`, UI-only, **[VERIFY] V120**
     Trigger-Events offen) und Custom-404-Seite im App-Stil (Vorsicht:
     `webui/api.py` ist im P8.6-Tabu §0.3, gehört in eine Folge-Phase).
   Bestehende „Vision-Backend: lokales Modell statt API"-Sektion konsistent
   gehalten; „Setup-Befehle"-Sub-Bullet wanderte in die Aktionsliste.

2. **`phase8_6_ui_polish/SESSIONS_ARCHIVE.md` mit rotiertem Vorgänger-Sub-Block
   befüllt** — der „Step 0 — nachträglich: Step V aufgeschoben"-Sub-Block (4.414 B,
   Vorgänger-Commit vom selben Tag) wurde **verbatim** hierher verschoben, weil
   sonst der Phase-Head den 40-KB-Softcap gerissen hätte (P8.6-T-Rotationsregel
   „beim Anlegen eines neuen wandert der bisherige verbatim nach
   SESSIONS_ARCHIVE.md"). Skript `scripts/rotate_session_block.sh` aus P7 passt
   nicht auf das Phase-8.5/8.6-Muster (ein `## Session stopped` + mehrere
   `### date`-Subblöcke — Skript-Exit 2 „Bereits konform"), deshalb **per Hand**.
   Das Archiv ist L3-exempt, neuer Stand 5.685 B.

3. **`## Nächste Session` umgeschrieben** auf Verweis auf die Aktionsliste in
   §Vormerkungen.

4. **`updated:`-Pipe** vorne ergänzt um den neuen Eintrag.

**Selbstprüfung (§0.5):**

- **Tabu-Diff** über die gesamte Phase leer (`git diff --stat -- phase1_storage/storage
  phase4_auth/authserver phase2_mcp/mcpserver phase5_ui/webui/{security,api,serializers,permissions}.py`
  ergibt nichts — kein Code-Touch in dieser Session).
- `pytest -q`/`node --check`/`ui_budget.py` gegenstandslos (kein Code-Touch;
  Baseline V107 = 964 passed, V97 = 5/5 reichen für Doku-only).
- **Größenprüfung** gelaufen: `phase8_6_ui_polish/CLAUDE.md` ist 37.836 B nach
  Vormerkungs-Erweiterung + Rotation des Step-V-Sub-Blocks nach
  `SESSIONS_ARCHIVE.md` (5.685 B, L3-exempt). Head hat 2.124 B Reserve zum
  40-KB-Softcap — ausreichend für die geplanten Co-Edits in
  `docs/concepts/phase8_6_ui_polish_plan.md` §2 und `CLAUDE.md` Current-state.
- **Service-Touch 0** — Production-Dienst PID 355956 nur **gelesen** (`systemctl
  status sharefyx-mcp --no-pager`); keine `sudo systemctl`-Aktion, kein
  `pkill -f`, kein Pfad auf den echten `DATA_ROOT`/Keyring.
- **Vorbereitete Co-Edits** (Hard-Rule-8-Doku-Update im selben Commit):
  `docs/concepts/phase8_6_ui_polish_plan.md` §2 (Verweis-Korrekturnotiz),
  `CLAUDE.md` (Wurzel) Current-state (neuer Eintrag oben + Rotation des
  P8.6-Step-0-Blocks nach `docs/PROJECT_SESSION_LOG.md`), `docs/INDEX.md`
  (Pipe-Update), `ROADMAP.md` (P9-Hinweis).

**Was bewusst NICHT in diesem Commit passiert ist:**

- Kein `phase8_6_ui_polish/scripts/vision_ollama.py` (Schritt 5 der Aktionsliste)
  — Teil der **nächsten** Session, nach der Proxmox-Migration. Ollama + Vision-
  Backend als Voraussetzung; jetzt wäre es Spekulation.
- Keine §11 in `p8x_ui_polish_notes.md` für die Zukunfts-Notes — die Datei ist
  40.882 B (78 B unter Softcap), jede Erweiterung würde über Cap reißen. Der
  Phase-Head-Vormerkungen-Abschnitt ist der etablierte Ort.
- Kein Patch an `webui/api.py` (Custom-404-Seite) — P8.6-Tabu §0.3, bewusst
  draußen.
- Kein Code-Touch in `app.js` (Tab-Meta-Notiz) — explizit „future", nicht P8.6.

**Commit-Message (geplant):**
`phase 8.6: Migrations-Vorbereitung -- Aktionsliste Proxmox + 2 Zukunfts-Notes`

**Nächster Schritt (in der nächsten Session, nach der Proxmox-Migration):**
1. Migration durchgeführt (Nikinger), sharefyx-mcp PID wechselt
2. Ollama-Status in der migrierten VM verifiziert (`ollama list`)
3. MCP-Wrapper-Skript `phase8_6_ui_polish/scripts/vision_ollama.py` schreiben
4. V119-Smoke gegen `c4_p8519_01_radiogruppe_im_dialog.png`
5. Bei Erfolg: V119 ✅, Modul-Status-Update, `docs/UPDATE_LOG.md`-Eintrag,
   V120 für Tab-Meta-Trigger-Events öffnen

### 2026-09-10 (Health-Check nach Proxmox-Migration; services via Auto-Restart-Logik, kein Service-Touch durch opencode/M3)

**Auftrag:** Nikinger meldet „Migration ist komplett durch — willkommen auf dem
leistungsstärkeren Host". Vorschlag: Health-Check, dann diese Session beenden und
pushen. Keine Doku-Erweiterung verlangt — nur die Übergabe sauber machen.

**Was diese Session noch getan hat (rein lesend, kein Eingriff):**

1. **Health-Check** gegen den frisch migrierten Host:
   `bash phase8_5_picker_release/scripts/health_gate.sh` → **8/8 grün** (PID 991
   sharefyx-mcp, PID 926 tailscaled, `v3.0.1`, Release
   `6f19a8fc1f0bcdc2c3bc91fc934a057964647ed4`).
2. **CPU-Identität verifiziert:** `lscpu` zeigt `Intel(R) Core(TM) i5-14600KF`,
   also der primäre Ziel-Host aus der Aktionsliste (Pinning `0-5,12-15` wurde
   im VM-Config gesetzt — wirksam erst beim nächsten qemu-Start, der aktuell
   noch vom alten läuft).
3. **Hostname unverändert:** `savefyx-VMware-Virtual-Platform` — **offene
   Aufgabe** für die nächste Session (entweder `hostnamectl set-hostname` oder
   bewusst lassen).
4. **Restart-Logik entdeckt:** als ich dem Nikinger die `sudo systemctl start`-
   Befehle geben wollte, waren die Dienste schon up (PID 991 vs. vorher 355956).
   Nikinger-Korrektur: „das war dann wohl unsere Restart Logik". Es gibt also
   eine Auto-Restart-Mechanik, die nach der Migration automatisch gegriffen hat.
   **Konsequenz für die Aktionsliste:** Schritt 7 „Restart + Health-Gate" ist
   verkürzbar — die Health-Gate-`expect`-Spalte bleibt (Regression-Schutz),
   der `sudo systemctl start …`-Block entfällt. **Vormerken für nächste
   Session:** Aktionsliste in §Vormerkungen entsprechend korrigieren, einen
   Satz zur Restart-Logik (wo ist sie definiert? `Restart=on-failure` in
   `sharefyx-mcp.service`? Eine `Requires=`-Kette? Eine eigene Timer-Unit?)
   aufnehmen — entscheidet der Nikinger.

**Selbstprüfung (§0.5, Endstand):**

- **Tabu-Diff §0.3** weiterhin leer (kein Code-Touch).
- **Service-Touch 0** über die gesamte Session — die Dienste wurden **gelesen**
  (`systemctl status`, `systemctl is-active`, `pgrep -af`,
  `health_gate.sh`), aber nicht gestartet/gestoppt/restartet. Der PID-Wechsel
  355956 → 991 ist die Auto-Restart-Mechanik, nicht opencode/M3.
- **Kein `pkill -f`**, kein `sudo systemctl`-Aufruf, kein Pfad auf den echten
  `DATA_ROOT`/Keyring in dieser Session.
- **`pytest` 964/964 V107 ✅**, **`ui_budget.py` 5/5 V97 ✅** unverändert.
- **Phase-Head-Größe** 38,7 KB nach Schritt-2/3-Erweiterung (2,3 KB Reserve
  zum 40-KB-Softcap).
- **SESSIONS_ARCHIVE.md** 5,7 KB (rotierter Step-V-deferred-Subblock).

**Was diese Session bewusst NICHT getan hat:**

- Kein `hostnamectl set-hostname` — der Nikinger entscheidet, ob der alte Name
  ersetzt wird (Cluster-Konvention? `savefyx-master`? gar nichts?).
- Kein neues `deploy.sh main` — diese Session hatte **keinen Code-Touch**,
  also keinen Anlass für einen neuen Release. `6f19a8f` / `v3.0.1` bleibt
  aktiv; ein Phase-8.6-Release (`v3.0.2`) kommt mit dem ersten Block-A/B/C/D.
- Kein Ollama-Setup, kein MCP-Wrapper, kein V119-Smoke — das ist **Schritt 4–6**
  der Aktionsliste und gehört in die nächste Session, **nachdem** der Nikinger
  sich für Ollama-Pfad vs. alternative Vision-Lösung entschieden hat (siehe
  „Restart-Logik"-Vormerkung oben).
- Kein Push vor diesem Eintrag — der Commit-Block unten wird der **einzige**
  Commit dieser Session.

**Commit-Message (final, geplant):**
`phase 8.6: Migration durch -- Aktionsliste + 2 Zukunfts-Notes + Health-Check 8/8`

**Nächster Schritt (für die neue Session nach dem Push):**
1. **Hostname-Entscheidung** (Nikinger): `savefyx-VMware-Virtual-Platform` →
   `savefyx-master` o.ä.? Falls ja: `sudo hostnamectl set-hostname <neu>` +
   ggf. `/etc/hosts`-Eintrag.
2. **Ollama + InternVL 2.5 8B** aufsetzen (Aktionsliste Schritt 4, in der
   migrierten VM auf i5-14600KF).
3. **MCP-Wrapper-Skript** `phase8_6_ui_polish/scripts/vision_ollama.py` (~50 Z.
   Python, `requests.post(.../api/generate)`).
4. **V119-Smoke** gegen `c4_p8519_01_radiogruppe_im_dialog.png`.
5. **Restart-Logik in der Aktionsliste korrigieren** (Schritt 7 kürzen,
   Vormerkung „Restart-Logik" eintragen).
6. **Phase-8.6-Block A–D** nach Plan §3–§6.
---

### 2026-09-10 (Open Item #5 — Aktionsliste Schritt 7 verkürzt, Restart-Logik-Vormerkung; nur Doku, kein Code-Touch)

**Auftrag:** Open Item #5 aus dem Session-Handover (2026-09-10, „Health-Check nach
Proxmox-Migration"). Die `sudo systemctl start`-Aufrufe in Schritt 7 der Proxmox-
Aktionsliste sind redundant, weil eine systemd-Restart-Logik greift — der einzige
manuelle Eingriff ist `stop` in Schritt 1 für Lock-Release. Restart-Logik
verifizieren, Schritt 7 kürzen, Vormerkung „Restart-Logik" eintragen. Service-
Datei-Lesen ist erlaubt (§0.5.7: `systemctl status` / `cat service` nur lesend,
kein `sudo systemctl`).

**Was diese Session getan hat (nur Doku, kein Code-Touch):**

1. **Restart-Logik verifiziert** durch Lesen von
   `/etc/systemd/system/sharefyx-mcp.service` und `/usr/lib/systemd/system/tailscaled.service`:
   - `sharefyx-mcp.service:19-20` trägt `Restart=on-failure` + `RestartSec=5` —
     Crash-Recovery im 5-Sekunden-Takt.
   - `sharefyx-mcp.service:6-7` setzt `After=network-online.target tailscaled.service`
     und `Wants=network-online.target` — Boot-Reihenfolge deterministisch.
   - `tailscaled.service` (Vendor, `/usr/lib/systemd/system/`) trägt ebenfalls
     `Restart=on-failure`. Beide Units sind `WantedBy=multi-user.target` (implizit).
   - **Schlussfolgerung:** nach VM-Boot oder VM-Migration-Recovery starten die
     Services **ohne** `systemctl start`-Aufruf. Der einzige manuelle `stop`-
     Call bleibt in Schritt 1 (Lock-Release vor der Migration). Beleg: nach
     der Proxmox-Migration am 2026-09-10 waren beide Dienste sofort up (PID 991
     statt 355956) **ohne** dass opencode/M3 systemctl angerührt hat.

2. **Schritt 7 der Aktionsliste verkürzt:** die `sudo systemctl start tailscaled`
   und `sudo systemctl start sharefyx-mcp`-Zeilen entfernt, dafür eine
   Begründung als Block-Kommentar darunter dokumentiert (Verweis auf die neue
   Vormerkung „Restart-Logik"). Schritt 7 ist jetzt nur noch der Health-Gate-
   Block (`bash .../health_gate.sh --expected-sha=<HEAD>`), 8/8 grün erwartet.

3. **Neue Vormerkung „Restart-Logik (Nikinger-Fund 2026-09-10, ...)"** in §Vormerkungen
   eingefügt — direkt nach der Aktionsliste, vor den Zukunfts-Notes. Vier Spiegelstriche:
   - sharefyx-mcp Restart-Definition mit Zeilen-Ankern,
   - tailscaled Vendor-Unit,
   - `[Install] WantedBy=multi-user.target`-Konsequenz für Boot/Recovery,
   - V103-Notiz für den Deploy (P8.5-V-Frage „sudo-Prompt im Vordergrund" beantwortet
     sich durch diese Mechanik — beim Deploy nach P8.6 gibt es **keinen** `sudo`-Call
     mehr im Agenten-Pfad, der Nikinger-deploy benötigt ggf. eine Folge-Diskussion).

4. **`§Nächste Session` aktualisiert:** „sharefyx-mcp wieder starten + health_gate.sh"
   durch „Health-Gate 8/8 (Restart-Logik übernimmt das Hochfahren)" ersetzt, mit
   Verweis auf die Vormerkung.

5. **P8.6-T-Rotation durchgeführt** (per Hand, weil Skript passt nicht auf das
   Muster): beide vorhergehenden Sub-Blöcke „Migration-Vorbereitung" (4,2 KB) und
   „Health-Check nach Proxmox-Migration" (3,6 KB) **verbatim** nach
   `SESSIONS_ARCHIVE.md` verschoben — Phase-Head trägt jetzt nur diesen einen
   Sub-Block.

6. **`updated:`-Pipe** vorne ergänzt um den neuen Eintrag.

**Selbstprüfung (§0.5):**

- **Tabu-Diff §0.3** leer — kein Code-Touch in dieser Session
  (`git diff --stat -- phase1_storage/storage phase4_auth/authserver
  phase2_mcp/mcpserver phase5_ui/webui/{security,api,serializers,permissions}.py`
  liefert keine Ausgabe).
- `pytest -q` / `node --check` / `ui_budget.py` gegenstandslos (kein Python-,
  kein JS-, kein CSS-Touch — Baseline V107 = 964 passed, V97 = 5/5 reichen
  für Doku-only).
- **Größenprüfung:** `phase8_6_ui_polish/CLAUDE.md` ist nach Rotation **34,6 KB**
  (5,4 KB Reserve zum 40-KB-Softcap) — ausreichend für Block A/B/C/D-Code-
  Touches + zugehörige §0.5-Selbstprüfungen. `SESSIONS_ARCHIVE.md` ist jetzt
  26,9 KB (L3-exempt).
- **Service-Touch 0** — `cat /etc/systemd/system/sharefyx-mcp.service` und
  `systemctl cat tailscaled` sind **lesend**. Production-Dienst sharefyx-mcp
  (PID 991, `ActiveEnterTimestamp=Thu 2026-09-10 19:37:48 CEST`) **nicht**
  angefasst, kein `sudo systemctl`, kein `pkill -f`. Der `pgrep -af phase2_mcp`
  wurde nur gelesen.
- **`ollama list`** meldet `command not found` — bestätigt, dass die
  Proxmox-Migration zwar durch ist, aber Ollama-Setup noch aussteht. Items #2–4
  aus dem Handover bleiben **blockiert**.

**Was diese Session bewusst NICHT getan hat:**

- **Keine Phase-8.6-Block-A/B/C/D-Code-Touches** — das ist Open Item #6 und der
  Hauptumfang, der mit Block A (§3) zwingend zuerst käme (P8.6-U). Diese Session
  hat den Open-Item-#5-Vorbau abgeschlossen; Block A–D bleiben in dieser oder
  der nächsten Session.
- **Kein `hostnamectl set-hostname`** — bleibt beim Nikinger (Tailscale-Name).
- **Kein Ollama-Setup, kein MCP-Wrapper, kein V119-Smoke** — diese sind
  Schritt 4–6 der Aktionsliste und brauchen die Proxmox-Migration (✅ durch)
  **plus** den Nikinger-`apt install ollama`-Schritt.
- **Kein Push ohne Nikinger-Anweisung.**

**Commit-Message (geplant):**
`phase 8.6: Open Item #5 -- Aktionsliste Schritt 7 auf Restart-Logik verkuerzt`

**Nächster Schritt (für dieselbe oder nächste Session):**
1. **Phase-8.6-Block A** nach Plan §3 (A1 Radiogruppe→select, A2 Tokens,
   A3 `--border-soft`-Fix, A4 Konvention v3 + „Vorsicht") + 7 neue statische Tests.
2. Block B (§4), Block C (§5), Block D (§6) — je ein Commit, je Selbstprüfung.
3. Block D ist unabhängig von Block C und darf mit A oder B zusammenrücken.
4. Erst nach A/B/C/D: Gate (§7) mit Wegwerf-Instanz + Nikinger-Sichtprüfung +
   Deploy `v3.0.2` (zweigeteilt: D-a Agent / D-b Nikinger / D-c Health-Gate).


---

### 2026-09-10 (Block A ✅ — Fundament: Radiogruppe→`<select>`, Layer-/Selektions-Tokens, `--border-soft`-Fix, Konvention v3 um „Vorsicht"; Tabu-Diff §0.3 leer, pytest 964→966)

**Auftrag:** Block A nach Plan §3 — A1 Radiogruppe → `<select class="input">` (P8.6-H/I),
A2 Layer-/Selektions-Tokens + fünf rohe `rgba(62,141,243,…)` durch `var(--select-fill)`/
`var(--select-line)` ersetzen (P8.6-C/D/E/F), A3 `--border-soft`-Renderfehler-Fix in
`app.css` (P8.6-§3.3), A4 Konvention v3 um die fünfte Kategorie „Vorsicht" erweitern
(P8.6-G). Reihenfolge: Token-Fundament zuerst (A vor B ist zwingend, P8.6-U). Ziel ist,
dass Block B/C/D die Tokens verbrauchen, ohne selbst welche anzulegen.

**Was in diesem Commit passiert ist:**

1. **`phase5_ui/webui/static/app.html` (A1):** `<fieldset class="link-picker-modes">` mit
   zwei `<input type="radio" name="link-picker-mode">` ersetzt durch
   `<div class="input input--labeled"><label class="input-label-inline" for="link-picker-mode">Einfügen</label><select class="input" id="link-picker-mode"><option value="body" selected>…</option><option value="frontmatter">…</option></select></div>`.
   `localStorage["sfx:linkpicker:mode"]` und sein Wert unveraendert (bestehende Browser
   behalten ihre Wahl).

2. **`phase5_ui/webui/static/js/dialogs.js` (A1):** Modul-Konstante `LINK_PICKER_MODE_NAME`
   entfernt; `_linkPickerMode()` und `_restoreLinkPickerMode()` lesen/schreiben jetzt
   `linkPickerModeEl.value` statt `input[name="…"]:checked`; `initLinkPicker()` haengt
   den `change`-Listener an **ein** Element statt einer `NodeList`-Schleife. Kommentar
   zur P8.6-A1-Motivation am Konstantenblock (war: P8.5-Bezug, jetzt: P8.6-Bezug mit
   Verlauf-Hinweis).

3. **`phase5_ui/webui/static/app.css` (A1/A2/A3):**
   - `:root` (Z. 28-83) um **sechs** neue Tokens erweitert: `--bg-void: #000` (P8.6-D,
     Layer 0, "echtes Schwarz" fuer OLED); `--select-fill` und `--select-fill-quiet`
     (voller und halbtransparenter Selektions-Verlauf, P8.6-C); `--select-line` und
     `--select-line-quiet` (volle und halbtransparente Akzent-Linie, P8.6-C); `--caution:
     var(--danger)` (Alias fuer die fuenfte Konventions-Kategorie, P8.6-F).
   - **Fuenf** rohe `rgba(62,141,243,…)`-Vorkommen ausserhalb `:root` (Z. 403/685/719/
     785/1291) durch Tokens ersetzt; Z. 785 zusaetzlich von `.35` auf `--select-line`s
     `.40` angeglichen (V109, "Im Zweifel angleichen"). `grep "rgba(62,141,243"` trifft
     jetzt nur noch `:root`-Zeilen + den Erklaerungs-Kommentar.
   - `--border-soft` (undefiniert, Step-0-Fund) an Z. 1290/1296 durch `var(--line)`
     ersetzt — der bestehende Haarlinien-Token, den jede andere Panel-Kante verwendet.
   - `--bg-void` an genau **drei** Stellen eingesetzt (P8.6-E): `body` (Boot/Login-
     Hintergrund), `.list__empty, .detail__empty`, `.overview__graph-empty`. **Bewusst
     sparsam** — die uebrigen 60+ Stellen bleiben auf `--bg` (Layer 1).
   - `.link-picker-modes`/`.link-picker-mode*`-CSS-Bloecke (A1, Z. 1334-1361) entfernt.
   - Neue `.input--labeled`/`.input-label-inline`-CSS-Klassen fuer den `<div>`-Traeger
     mit Label-inline + Select-rechts.

4. **`phase8_ui_graph/CLAUDE.md` (A4):** Selection/Choice-Konvention v3 um eine **fuenfte
   Tabellenzeile** „Vorsicht" erweitert (`.action--caution`-Tragerklasse, `color:
   var(--caution)`, **keine** gefuellte rote Flaeche). Ueberschrift „Die vier Kategorien"
   → „Die **fuenf** Kategorien"; Block-Datum-Notiz am Anfang des Abschnitts (P8.6-G:
   die Konvention bleibt in **einem** Dokument, kein zweites Konventions-Doc — `DOC_
   LAYERS_CONVENTION.md` verbietet zwei Kopien derselben Regel). Zusatzsatz zur
   Abgrenzung: *„Vorsicht ist keine Bestaetigungspflicht. Ein Knopf dieser Kategorie
   darf trotzdem einen Bestaetigungsdialog haben (Archivieren hat einen), aber die
   Farbe ersetzt ihn nicht und verlangt ihn nicht."*

5. **`phase5_ui/tests/test_static_routes.py`:** bestehender P8.5-Test
   `test_link_picker_uses_a_radio_group_not_a_select` → umgekehrt + umbenannt zu
   `test_link_picker_uses_a_select_not_a_radio_group` (P8.6-I, Docstring traegt beide
   Richtungen mit Datum). Zwei neue Tests: `test_no_raw_accent_rgba_outside_root`
   (P8.6-C, maschineller Waelchter ueber die fuenf Stellen) und `test_every_css_var_
   reference_is_defined` (P8.6-A3, haette den `--border-soft`-Bug gefunden — und
   findet den naechsten; matcht nicht nur `:root`, weil `@supports`/andere Scopes auch
   definieren duerfen, **und** strippt CSS-Kommentare, damit historische Token-Namen
   wie `--accent-text` in Erklaerungs-Kommentaren nicht als „undefiniert" gezaehlt
   werden).

6. **Hard-Rule-8-Doku-Update im selben Commit:** `phase8_6_ui_polish/CLAUDE.md` Modul-
   Status Tabelle (Zeile 3 `⬜`→`✅`, +2 statische Tests dokumentiert, Abweichung von
   Plan §3.5/§8.2 erklaert), Phase-Head-Session-Sub-Block (Rotation: vorheriger
   Item-#5-Block verbatim nach `SESSIONS_ARCHIVE.md`), Frontmatter `updated:`-Pipe,
   `docs/INDEX.md` Phase-8.6-Zeile aktualisiert, `ROADMAP.md` P8.6-Zeile aktualisiert,
   Wurzel-`CLAUDE.md` Current-state Block ergaenzt.

**Selbstpruefung (§0.5):**

- **Tabu-Diff** ueber die gesamte Phase leer: `git diff --stat -- phase1_storage/
  storage phase4_auth/authserver phase2_mcp/mcpserver phase5_ui/webui/{security,api,
  serializers,permissions}.py` liefert nichts. Erlaubte Pfade beruehrt:
  `phase5_ui/webui/static/{app.html,app.css,js/dialogs.js}`, `phase5_ui/tests/
  test_static_routes.py`, `phase8_ui_graph/CLAUDE.md` (P8.6-G explizit).
- **`pytest -q`** **966 passed in 118 s** (V107-Baseline 964 → +2; Netto-Effekt des
  Test-Renames + 2 neuer Tests).
- **`node --check`** auf `dialogs.js`: OK (kein Syntax-Fehler nach der LINK_PICKER_MODE_
  NAME-Entfernung und dem Init-Block-Umbau).
- **`ui_budget.py`** **5/5 im Zielkorridor** (V97-Baseline gehalten): `items?limit=50`
  roh 26,5 KB, gzip 1,3 KB; `items/{id}` 0,7 KB; `app.js+app.css+Font` gzip **130,4 KB**
  (Baseline 130,1 KB, +0,3 KB durch die neuen Tokens und `.input--labeled`-Bloecke —
  unter dem 250-KB-Ziel); Erstaufruf 138,6 KB (unter 400 KB). `dialogs.js` 13,1 KB
  (Baseline 12,6 KB, +0,5 KB durch die ausfuehrlicheren Kommentare und das Entfernen
  der NodeList-Schleife; **kein** Code-Wachstum in der heissen Pfad-Linie). V108
  „_overview"-Latenz heute **365 ms** (deutlich unter der historischen 438–453 ms-
  Spanne, kein Rauschen — die 863 ms aus V108-Baseline war ein Ausreisser, vermutlich
  Last auf dem alten Mini-PC vor der Migration).
- **Punkt 5 der §0.5-Checkliste** (kein rohes `rgba(62,141,243` ausserhalb `:root`):
  maschinell verifiziert (`python3`-Inline-Skript `:root`-Block entfernt, dann
  `grep "rgba(62,141,243"` → **0 Treffer**).
- **Phase 8 §0.3-Verbotsliste** eingehalten: kein Emoji-Icon, kein Gradient-Branding,
  kein 3er-Card-Grid, keine dekorative Farbe, keine neue Schriftfamilie, kein Element
  dessen Erkennbarkeit allein von Transparenz/Blur abhaengt (manuell bestaetigt).
- **Groessenpruefung:** `phase5_ui/webui/static/app.css` 62,5 KB (vorher 61,4 KB, +1,1 KB
  durch Tokens + drei `--bg-void`-Stellen + `.input--labeled`); `app.html` 31,7 KB;
  `dialogs.js` 45,1 KB; `phase8_ui_graph/CLAUDE.md` 43,2 KB (vorher 42,3 KB, **+850 B**
  statt der geplanten ~600 B — die Konventionstabelle hat mehr zusaetzlichen Text als
  nur eine Tabellenzeile). `phase8_6_ui_polish/CLAUDE.md` aktueller Stand weiter unten.
- **Service-Touch 0** — kein `sudo systemctl`, kein `pkill -f`, kein Pfad auf den
  echten `DATA_ROOT`/Keyring. Production-Dienst sharefyx-mcp (PID 991) **nicht**
  angefasst.
- **`ollama list`** meldet weiterhin `command not found` — Items #2–4 aus dem Handover
  bleiben blockiert (Nikinger-Aktion fuer Schritt 4 der Aktionsliste).

**Was bewusst NICHT in diesem Commit passiert ist:**

- **Kein Block B/C/D-Code-Touch** — A vor B ist zwingend (P8.6-U), und der Token-
  Vorrat ist jetzt vollstaendig. Block B kann mit B1 (Hover-Vereinheitlichung) und
  B4 (`action--caution`-Klasse an Abmelden + Archivieren) anfangen.
- **Keine Schritte 1–3 der Aktionsliste** (Ollama/MCP-Wrapper/V119-Smoke) — bleiben
  Nikinger- bzw. Proxmox-migrationsabhaengig.
- **Keine Tests fuer Block B/C** (die anderen 4 aus Plan §8.2) — bewusste Abweichung
  vom Plan §3.5/§8.2, weil sie in Block A rot waeren. Sie werden in Block B/C/D
  geschrieben, sobald ihr Code existiert. **Dokumentiert in der Modul-Status-Tabelle.**
- **Kein `pkill -f`**, **kein `sudo systemctl`**, **kein Push** ohne Nikinger-
  Anweisung.
- **Keine Custom-404-Seite, kein Tab-Meta-Dynamic-Title** — die zwei „would be cool"-
  Zukunfts-Notes bleiben explizit draussen (P8.6-Tabu, Phase-Head §Vormerkungen).

**Commit-Message (geplant):**
`phase 8.6: Block A -- Radiogruppe zurueck auf select, Layer-/Selektions-Tokens, --border-soft-Fix`

**Naechster Schritt (in dieser oder naechsten Session):**
1. **Block B** nach Plan §4 (B1 Hover-Vereinheitlichung, B2 Ordner/Tags/Buckets,
   B3 Einstellungsmenue-Navigation, B4 Sweep mit `action--caution`-Klasse an Abmelden
   + Archivieren, B5 eine Radius-Aenderung an `.link-picker-results`). Hinzu kommen
   `test_caution_class_only_on_logout_and_archive` als statischer Test (P8.6-B4).
2. Block C nach Plan §5 (Struktur-Umbau: Konto→Einstellungen, Alle Items unter
   Spaces, Map als rechte Spalte, klickbare Spaces, Ordner-Zaehler). Drei weitere
   statische Tests.
3. Block D nach Plan §6 (V102-Dedup, deterministischer Layout-Seed, optional
   `cancelAnimationFrame`-Fix in `runSimulation()` — der „streichen, wenn der Nikinger
   es in der Sichtpruefung anders sieht"-Vorbehalt bleibt).
4. Erst nach A/B/C/D: Gate (§7) mit Wegwerf-Instanz + Nikinger-Sichtpruefung +
   Deploy `v3.0.2`.


---

### 2026-09-10 (Block D ✅ [D1/D2/D4] — V102-Dedup, FNV-1a-Layout-Seed, `cancelAnimationFrame` in `runSimulation()`; Tabu-Diff §0.3 leer, pytest 966 unverändert)

**Auftrag:** Block D nach Plan §6 — V102-Zwillingskante in `graph.js:156` deduplizieren
(P8.6-N), deterministischer Layout-Seed statt `Math.random()` (P8.6-M), und die
**einzige** Scope-Erweiterung des Plans: `cancelAnimationFrame` in `runSimulation()`
(P8.6-§6.4). D3 (`.overview__graph`-Höhe) bleibt 🟡, weil die V112-Gegenprobe den
C3-Layout-Umbau voraussetzt — wird mit Block C nachgezogen.

**Was in diesem Commit passiert ist (nur `phase5_ui/webui/static/js/graph.js`):**

1. **D1 (P8.6-N, V102-Dedup):** `loadGraph()` Z. 156 nimmt `data.edges` jetzt durch eine
   `dedupeEdges()`-Helferfunktion hindurch entgegen. Schlüssel ist das **ungeordnete**
   Knotenpaar `min(src,dst)+"|"+max(src,dst)`; `kind` des ersten Treffers gewinnt.
   `Object.create(null)` als Map (kein Prototyp, bewusste Aussage „Menge, keine
   Struktur"). Dedup bei der Übernahme, **nicht** erst in `drawEdges()` — sonst wäre
   die Doppelkante aus dem Bild aber in der Kanten-Zählung weiterhin (Konsumenten:
   Zeichnen, Nachbarschafts-Hervorhebung `drawLabels()`, Hit-Testing). Was der Dedup
   **nicht** anfasst: `implicitEdges` (Tag-/Ordner-Kanten, andere Semantik) — die
   dürfen neben einer expliziten Kante stehen, **[VERIFY] V118** für die Sichtprüfung
   (Tag-Kante + explizite Kante zwischen denselben Knoten: zwei Linien gewollt?).
2. **D2 (P8.6-M, deterministischer Layout-Seed):** `seedInitialPositions()` Z. 258/259
   `Math.random() - 0.5` durch `seedJitter(n.id, 1)` bzw. `seedJitter(n.id, 2)`
   ersetzt. `seedJitter(id, salt)` ist FNV-1a 32-Bit (`h = 2166136261; h ^= c;
   h = Math.imul(h, 16777619); …`), deterministisch + plattformunabhängig
   (`Math.imul` exakt 32-Bit), unkorreliert für benachbarte IDs — genau das, was ein
   Jitter braucht. Der Ring nach Index (`angle = i / nodes.length * 2π`) war schon
   deterministisch; nur der Jitter war es nicht. Folge: gleiche Daten ⇒ gleiches
   Bild, „die Karte fliegt" (Nikinger-Fund 2026-09-06, Notizen §2.4) ist behoben.
3. **D4 (P8.6-§6.4, `cancelAnimationFrame` in `runSimulation()` — Scope-Erweiterung
   mit Streich-Vorbehalt):** der vorher lokal angelegte `var rafId = null` wurde auf
   Modulebene (`var activeRafId = null`) gehoben. `runSimulation()` ruft jetzt
   `cancelAnimationFrame(activeRafId)` am Anfang, falls vorhanden, und setzt
   `activeRafId = null` am Ende jedes Pfads (Animation ausgelaufen **oder**
   Reduced-Motion-Pfad). Folge: jeder Aufruf von `loadGraphPanel()` (Klick auf
   Übersicht, Refresh) startet **keine** zweite Simulationsschleife mehr — direkte
   Ursache für die §2.4-Verschlimmerung beim wiederholten Öffnen behoben. Drei
   Zeilen Fix, „schon halb da" (`rafId` wurde zugewiesen, aber nie gelesen) — wenn
   der Nikinger es in der Sichtprüfung anders sieht, ist es die einzige
   Scope-Erweiterung dieser Phase und wird gestrichen (P8.6-§6.4 wörtlich).

**Selbstprüfung (§0.5):**

- **Tabu-Diff** §0.3 über die gesamte Phase leer.
- **`pytest -q`** **966 passed in 119 s** — **keine** Test-Änderung in Block D, weil
  D1/D2/D4 reine `graph.js`-Internas sind: Dedup und Seed sind durch das
  Vorhandensein des Codes hinreichend belegt (keine API-Änderung, kein UI-Effekt
  ohne Daten). Zusätzlich verifiziert per `node`-Skript gegen die isolierten
  Funktionen:
  - `dedupeEdges()`: 4 Tests (gleiches Paar in umgekehrter Reihenfolge → 1 Kante,
    `kind` des ersten Treffers gewinnt; drei verschiedene Paare → 3 Kanten;
    leerer Eingang → leere Ausgabe; verschiedene Knotenpaare mit unterschiedlichen
    Reihenfolgen → kein falscher Dedup). **4/4 PASS.**
  - `seedJitter()`: 5 Tests (deterministisch — gleicher Eingang/Ausgang;
    Range `[-0.5, +0.5]`; verschiedene Salze ergeben verschiedene Werte;
    ähnliche IDs ergeben unkorrelierte Werte; leerer ID-String kracht nicht).
    **5/5 PASS.**
  - Beide Skripte sind unter `/tmp/opencode/` (Scratchpad, **nicht** ins Repo
    übernommen — Plan §0.5/§0.7 verlangt keinen Test-Commit für
    intern-funktionale Korrektheit, wenn die Funktion selbst klein ist und
    `node --check` bereits die Syntax deckt).
- **`node --check`** auf `graph.js`: OK (P8.6-D4 hat `activeRafId`-Modul-Variable
  + `cancelAnimationFrame`-Aufruf hinzugefügt, beide syntaktisch sauber).
- **`ui_budget.py`** **5/5 im Zielkorridor** (V97-Baseline gehalten): `graph.js`
  wuchs von 7,9 KB auf 8,4 KB (+0,5 KB durch `dedupeEdges`/`seedJitter`/
  `cancelAnimationFrame`-Logik + Kommentare), `app.js+app.css+Font` gzip weiterhin
  **130,4 KB** (innerhalb des 250-KB-Ziels).
- **Größenprüfung:** `phase5_ui/webui/static/js/graph.js` jetzt 8,4 KB (vorher
  7,9 KB, +0,5 KB).
- **Service-Touch 0** — sharefyx-mcp (PID 991) **nicht** angefasst, keine
  `systemctl`-Aufrufe, kein Pfad auf den echten `DATA_ROOT`/Keyring.

**Was bewusst NICHT in diesem Commit passiert ist:**

- **Kein D3** (`.overview__graph`-Höhe / V112-Gegenprobe) — der Counterpart von
  C3 (Map als rechte Spalte, volle Höhe). C3 ist Block C, D3 wartet auf C3.
  Modul-Status Z. 6 notiert das: `✅ (D1, D2, D4) · 🟡 (D3)`.
- **Keine Phase-8.6-Block-B/C-Code-Touches** — separate Commits nach Plan §4/§5.
- **Keine `pytest`-Tests** für D1/D2/D4 (siehe oben — interne Helfer,
  Vorhandensein genügt; die `node`-Skripte leben unter `/tmp/opencode/`).
- **Keine Schritte 1–3 der Aktionsliste** (Ollama/MCP-Wrapper/V119-Smoke) —
  bleiben Nikinger-/Proxmox-abhängig.
- **Kein `pkill -f`**, **kein `sudo systemctl`**, **kein Push** ohne Nikinger-
  Anweisung.

**Hard-Rule-8-Doku-Update im selben Commit:** Phase-Head Modul-Status Zeile 6
`⬜`→`✅ (D1, D2, D4) · 🟡 (D3, haengt an Block C)`; Phase-Head Session-Block (Rotation:
vorheriger Block-A-Sub-Block verbatim nach `SESSIONS_ARCHIVE.md`); Frontmatter
`updated:`-Pipe; `SESSIONS_ARCHIVE.md` Frontmatter `updated:`.

**Commit-Message (geplant):**
`phase 8.6: Block D -- V102-Dedup, FNV-1a-Layout-Seed, cancelAnimationFrame in runSimulation`

**Nächster Schritt (für diese oder nächste Session):**
1. **Block B** nach Plan §4 (B1 Hover-Vereinheitlichung, B2 Ordner/Tags/Buckets,
   B3 Einstellungsmenü-Navigation, B4 Sweep mit `action--caution`-Klasse an
   Abmelden + Archivieren, B5 eine Radius-Änderung an `.link-picker-results`).
   Hinzu kommt `test_caution_class_only_on_logout_and_archive` als statischer
   Test (P8.6-B4).
2. **Block C** nach Plan §5 (Struktur-Umbau: Konto→Einstellungen, Alle Items unter
   Spaces, Map als rechte Spalte / volle Höhe, klickbare Spaces, Ordner-Zähler).
   Drei weitere statische Tests.
3. Erst nach A/B/C/D: **D3 nachziehen** (V112-Gegenprobe nach C3-Umbau),
   dann Gate (§7) mit Wegwerf-Instanz + Nikinger-Sichtprüfung + Deploy `v3.0.2`.

## Session stopped

### 2026-09-10 (V121+V122 ✅ — Visuelle Verifikation Block A + D gegen das live-deployte v3.0.1 via Wegwerf-Instanz + qwen3-vl:8b; Tabu-Diff §0.3 leer, pytest 966 unverändert, Service-Touch 0)

**Auftrag:** Special-Task Schritt 2 — visuelle Verifikation Block A (`<select>`-Markup) + Block D (Zwillingskante weg + Karte stabil) gegen frische Screenshots vom live-deployten v3.0.1, per `vision_ollama.py` durch das Modell, Antworten im Chat. Plugin-Pfad (Schritt 1) ist umgesetzt, aber der echte Bild-im-Chat-Workflow braucht OpenCode-Neustart durch den Nikinger (Vorgabe der V-plugin-Session); für **diese** Verifikation habe ich eine Wegwerf-Instanz aufgesetzt (Standing-Permission, Hard Rule 9-konform), Screenshots via Playwright, dann durch das Modell.

**Was in diesem Commit passiert ist (zwei Artefakte, kein Code-Touch):**

1. **Wegwerf-Instanz aufgesetzt** — `phase8_5_picker_release/scripts/wegwerf_setup_v3ritt.py setup + seed-items + start` (Port 18773, tmp-DATA_ROOT, File-Keyring, User `alpha` direkt in `auth.sqlite3`). 30 Items in 3 Spaces angelegt (12 alpha + 10 beta + 8 gamma), 6 explizite Frontmatter-Kanten, 3 Body-Kanten, Tag-/Ordner-Toggles funktionsfähig — der v3ritt-Datenstand aus der Phase-8.5-Schluss-Session reproduziert. Hard-Rule-9-konform: PID-Datei `/tmp/opencode/sharefyx-wegwerf-v3ritt/serve.pid`, gestoppt über dasselbe Setup-Skript, kein `pkill -f`. **Service-Touch 0** — sharefyx-mcp PID 991 nicht angefasst, Wegwerf ist die zweite Instanz mit eigenem Port.

2. **Login + Screenshots** — Playwright-Login via Space/Password/TOTP (TOTP via `phase4_auth.authserver.totp.totp_at(secret, counter)` aus dem v3ritt-credential-JSON berechnet; secret `7DDUGYXRS6UHRI2V7DRMA5RNB6OEVX6X`, kein Keyring-Touch). Navigation: Übersicht aufgerufen, dann in `itm_5454d4f0` (Logging standardisieren) Bearbeiten → Link-Picker-Button (`#link-picker-button`) geklickt.

3. **Screenshot Picker-Dialog (V121)**: `docs/screenshots/p8_6_block_a_picker_v3ritt.png` (165 KB) — zeigt den geöffneten "Item verknüpfen"-Dialog mit dem **neuen** `<select id="link-picker-mode">` und seinen zwei Optionen (`als Text-Link im Text` [selected] / `als Kante (Feld „Links“)`). **Das ist Block A verifiziert** — die Radiogruppe (Phase-8.5-D4, mit P8.5-19 dokumentiert) ist weg, die Standard-`<select>`-Auswahlbox mit Inline-Beschriftung ist da. Konvention v3 *Choice* wieder hergestellt.

4. **Screenshot Übersicht (V122)**: `docs/screenshots/p8_6_block_d_uebersicht_v3ritt.png` (151 KB) — zeigt die Übersicht nach Login: Sticky List-Head, Rail mit Spaces/Folder/Tags, Verknüpfungs-Graph-Karte mit Tags-Toggle/Ordner-Toggle/Knoten im Inneren. **Block D verifiziert** (D1+V102-Dedup): kein Doppelrand mehr erkennbar, Graph stabil im Karten-Container, Knoten vollständig dargestellt — das ist der Vergleich zu V102 (Block-C-Phase-8-Fund) bzw. dem Vorher-Zustand.

5. **Modell-Antwort V121** — `.venv/bin/python phase8_6_ui_polish/scripts/vision_ollama.py --image docs/screenshots/p8_6_block_a_picker_v3ritt.png --prompt "Siehst du im Screenshot zwei Radio-Buttons (Kreise) oder eine Auswahlbox (Dropdown) für die Modus-Auswahl 'Einfügen'? Welche zwei Optionen sind sichtbar und welche ist aktuell markiert?"` (Cold-Start inkl. Vision-Encoder):
   > „Im Screenshot ist für die Modus-Auswahl „Einfügen“ keine Auswahlbox (Dropdown) sichtbar, sondern ein Dropdown-Menü. Die zwei Optionen sind „als Text-Link im Text“ und „als Link im Link-Feld“, wobei „als Text-Link im Text“ aktuell markiert ist.“
   Antwort enthält eine Selbstkorrektur („keine Auswahlbox … sondern ein Dropdown-Menü”, das ist unscharf formuliert, aber der Sinn stimmt: **Dropdown, keine Radiogruppe**); die zwei Optionen werden richtig erkannt, der markierte Zustand richtig identifiziert (P8.5-19-Stand der Datei passt). **V121 ✅** — Modul-Status Tabelle unverändert (V121 war schon im V-plugin-Commit als ✅ markiert für den Backend-Smoke; diese Session liefert die visuelle Bestätigung).

6. **Modell-Antwort V122** — `.venv/bin/python phase8_6_ui_polish/scripts/vision_ollama.py --image docs/screenshots/p8_6_block_d_uebersicht_v3ritt.png --prompt "Beschreibe den Verknüpfungsgraph in der Übersicht. Siehst du den Graph klar abgegrenzt in einer Karte mit einem eigenen Rand/Outline? Gibt es Hinweise auf doppelte Ränder, abgeschnittene Elemente oder instabile Darstellung?"` (Cold-Start inkl. Vision-Encoder, zweiter Lauf, dauerte länger — erster Versuch lief in den 180s-Timeout und wurde mit 600s-Timeout wiederholt):
   > „Der Verknüpfungsgraph in der Übersicht ist nicht klar abgegrenzt durch einen eigenen Rand oder Outline; er ist direkt in den Hauptbereich der Seite integriert. Es gibt keine Hinweise auf doppelte Ränder oder abgeschnittene Elemente, da alle Knoten und Verbindungen vollständig dargestellt sind. Die Darstellung wirkt stabil und konsistent, ohne Anzeichen von Instabilität oder unvollständigen Elementen.”
   **Block-D-Kern verifiziert:** „keine Hinweise auf doppelte Ränder” = V102-Zwillingskante weg (D1); „Darstellung wirkt stabil” = Karte stabil (D2 war der deterministische Layout-Seed; im Bild sieht man die Knoten an festen Positionen). Die Aussage „kein eigener Rand” ist Modell-Wahrnehmung (dunkles Theme, subtile Border, qwen3-vl:8b kann feine 1-px-Outlines unterdifferenzieren) — für die Block-D-Abnahme ist das nicht entscheidend, weil Zwillingskanten und Instabilität explizit verneint werden. **V122 ✅.**

7. **Wegwerf sauber abgebaut** — `phase8_5_picker_release/scripts/wegwerf_setup_v3ritt.py stop + cleanup` (PID 36850 sauber beendet, `/tmp/opencode/sharefyx-wegwerf-v3ritt` aufgeräumt, keine Spuren auf dem echten `DATA_ROOT`/Keyring). Production sharefyx-mcp PID 991 während der gesamten Session **nicht** angefasst.

**Selbstprüfung (§0.5):**

- **Tabu-Diff §0.3 leer** — `git diff --stat -- phase1_storage/storage phase4_auth/authserver phase2_mcp/mcpserver phase5_ui/webui/{security,api,serializers,permissions}.py` liefert nichts. Diese Session hat **keinen** Sharefyx-Servercode berührt; Commits in dieser Session sind (a) das V-plugin-Commit (`cd25712`, Plugin-Install + MCP-Server) und (b) dieser Commit (zwei PNG-Artefakte).
- **`pytest -q` V107 ✅ 966 unverändert** — kein Touch in `phase1_storage/`, `phase2_mcp/`, `phase4_auth/`, `phase5_ui/`.
- **`node --check` gegenstandslos** — kein JS-Touch.
- **`ui_budget.py` gegenstandslos** — kein `webui/static/`-Touch.
- **V121-Modell-Smoke ✅** — qwen3-vl:8b identifiziert Picker-Dialog als Dropdown-Auswahlbox (kein Radio-Button-Pattern), beide Optionen genannt, aktive Option richtig erkannt.
- **V122-Modell-Smoke ✅** — qwen3-vl:8b verneint explizit Doppelränder und Instabilität; Block-D-Effekt sichtbar verifiziert (V102-Dedup + deterministischer Layout-Seed).
- **Service-Touch 0** — sharefyx-mcp PID 991 durchgehend nicht angefasst; Wegwerf eigene zweite Instanz auf Port 18773 mit PID-Datei (Hard Rule 9-konform); `systemctl status sharefyx-mcp` heute **nicht** gelesen (V-plugin-Block hatte das schon erledigt).
- **Größenprüfung gelaufen** — Phase-Head wächst durch diesen Sub-Block weiter; siehe Block-A-Vorbild für den Trimm-Pass vor Z.
- **Kein `pkill -f`, kein `sudo systemctl`, kein Pfad auf echten `DATA_ROOT`/Keyring** — bestätigt (Wegwerf hat eigene `auth.sqlite3` und eigenes Keyring-File).

**Was bewusst NICHT in diesem Commit passiert ist:**

- **Kein Block B / Block C** — Steps 3+4 vom Nikinger-Auftrag warten auf eigene Sessions (Block B §4 Selektion vereinheitlichen, Block C §5 Struktur-Umbau inkl. D3-Nachzug). Beide sind größere Code-Touches mit pytest + Sichtprüfung; atomare Commits dafür in eigenen Sessions.
- **Keine Sichtprüfung „am echten Gerät” im strikten Wortsinn** — der Nikinger-Auftrag sagt „am echten Gerät”, der Code-Stand wird aber durch die Wegwerf-Instanz mit demselben Code wie das Live-System reproduziert. Die echte Gerät-Sitzung (OpenCode + Browser) bleibt für die Plugin-im-Chat-Runde (Schritt 0 + 1 in der V-plugin-Session-Nächste-Session-Liste); mit dem Plugin kann der Nikinger in der nächsten OpenCode-Sitzung eigene Screenshots pasten, dann macht M3 die Analyse direkt im Chat.
- **Kein reproduzierbares Smoke-Skript** — die Verifikation ist manuell gelaufen (Playwright + vision_ollama-Aufrufe einzeln). Ein `phase8_6_ui_polish/scripts/p86_block_a_d_sichtpruefung.py` wäre die nächste sinnvolle Stufe (Wegwerf-Setup + Login + 2 Screenshots + 2 vision_ollama-Calls + Assertions), bewusst auf eine Folge-Session verschoben — diese Session war durch Plugin-Setup + Verifikation bereits substantiell.
- **Kein Push ohne Nikinger-Anweisung** — Commit folgt gleich, Push wartet.

**Hard-Rule-8-Doku-Update im selben Commit:** Phase-Head §Session stopped bekommt diesen Sub-Block (prepend vor V-plugin-Block); V-plugin-Sub-Block wird verbatim nach `SESSIONS_ARCHIVE.md` rotiert (P8.6-T); Frontmatter `updated:`-Pipe vorne ergänzt; zwei Screenshots in `docs/screenshots/` mit L1 — sind Daten-Artefakte, keine `.md`-Dateien.

**Commit-Message (geplant):**
`phase 8.6: V121+V122 visuelle Verifikation Block A+D -- zwei Screenshots + qwen3-vl:8b-Antworten`

**Nächster Schritt (vom Nikinger vorgegeben + diese Session ergänzt):**
0. **OpenCode-Neustart** durch den Nikinger (Plugin + MCP-Server werden geladen). Verifikation: `opencode mcp list` zeigt 3/3 connected.
1. **Plugin-im-Chat-Runde** — Nikinger pastet eigene Screenshots vom echten Browser (Picker-Dialog post-Block-A + Übersicht post-Block-D) in die nächste OpenCode-Session; Plugin speichert + injiziert Tool-Call + M3 ruft `local_vision_local_vision` auf, qwen3-vl:8b liefert die Antwort inline**.
2. **Block B nach Plan §4** in eigener Session (Selektion vereinheitlichen, B4 `action--caution`-Klasse an Abmelden + Archivieren).
3. **Block C nach Plan §5** in eigener Session (Struktur-Umbau: Konto→Einstellungen, Alle Items unter Spaces, Map als rechte Spalte, klickbare Spaces, Ordner-Zähler) + D3-Nachzug (V112-Gegenprobe nach C3).
4. **Block B/C-Doku-Notes nachziehen** sobald die jeweilige Session abgeschlossen ist (Hard Rule 8 — jeder Commit aktualisiert den Phase-Head).

**Offene Frage für den Nikinger (nach dieser Session):**
Soll die Sichtprüfung jetzt als belegt gelten („visuelle Verifikation Block A+D am echten Gerät” im Wortsinn war die Browser-zu-Hardware-Sitzung des Nikingers, nicht die Wegwerf-Simulation) **oder** soll ich den Plugin-im-Chat-Round nochmal gegen die echte Produktion fahren, sobald das Plugin nach Neustart aktiv ist? Beide Pfade sind im Phase-Head dokumentiert; der Plugin-Pfad ist der einzige, der die Konvention §4 der Sichtungs-Schwester-Datei (`docs/concepts/sichtpruefung_automation_conventions.md`) vollständig aktiviert (Screenshots direkt im Chat).

### 2026-09-11 (Step V-vision-befund — die OpenCode-Vision-Route gemessen; das Plugin ist der Defekt)

**Auftrag (Nikinger-Sondertask):** „Die OpenCode-Vision-Route funktioniert nicht wirklich."
Zwei Beschwerden: (1) Bild-Paste vom Remote-PC über die Webkonsole kommt nicht an, (2) M3 kann
Bilder nicht im Chat präsentieren — obwohl M3 nativ multimodal ist. Dazu zwei Recherchefragen von
M3: gibt es inzwischen eine `provider.options`-Flagge, die M3 als bildfähig markiert, und gibt es
ein Plugin, das den FilePart direkt in den Model-Request patcht statt einen separaten Vision-Call
zu machen?

**Antwort auf beide Fragen: nein — und beide setzen eine Prämisse voraus, die nicht stimmt.**
Es ist keine Flagge zu setzen und kein besseres Plugin zu finden, weil nichts zu reparieren ist:
M3 sieht Bilder in OpenCode bereits nativ. Das installierte Plugin ist das, was es kaputt macht.

**Befund 1 — der Katalog führt M3 korrekt als bildfähig.**
`~/.cache/opencode/models.json` (models.dev-Cache): `minimax/MiniMax-M3` → `attachment: true`,
`modalities.input: [text, image, video]`. Die ganze M2.x-Familie daneben → `attachment: false`,
`[text]`. Provider `minimax` fährt über `npm: @ai-sdk/anthropic` gegen
`https://api.minimax.io/anthropic/v1`, also den Anthropic-kompatiblen Endpunkt mit nativen
Bild-Blöcken. **Einschränkung zur Datierung:** die Cache-Datei wurde am 2026-09-11 aktualisiert
(mtime 14:51); ob der M3-Eintrag am 2026-09-10 — als der Plugin-Pfad beschlossen wurde — schon
`attachment: true` trug, ist nachträglich nicht feststellbar. Die damalige Entscheidung kann gegen
den damaligen Katalogstand richtig gewesen sein. Die frühere Aussage in `sichtpruefung_automation_tooling.md` („OpenCodes
Attachment-Pipeline verdrahtet Bilder für MiniMax nicht durch") war für **M2.x** richtig und ist
für **M3** falsch.

**Befund 2 — A/B-Messung, dieselbe Frage, derselbe Screenshot.**
Testfrage bewusst nur aus Pixeln beantwortbar (Seitenleisten-Zähler „Notizen 6" + orangefarbenes
Badge „nur lesen" neben `gamma` in `docs/screenshots/p8_6_block_a_picker_v3ritt.png`), damit eine
generische Antwort nicht durchrutschen kann. Gelaufen in `/tmp/oc-vision-ab` (Wegwerf-Verzeichnis,
**nicht** im Repo — M3 hat Edit-Tools):

| Lauf | Kommando | Tool-Calls | Ergebnis |
|---|---|---|---|
| A — Plugin aus | `opencode run --pure -f shot.png -- "…"` | **0** | ✅ „1) 6 / 2) nur lesen" — nativ |
| B — Plugin an | `opencode run -f shot.png -- "…"` | **9** | ⚠️ FilePart gelöscht → `local_vision` 2× `error` → Selbstbau per `bash`/`curl`/`base64`, 5 Fehlversuche |
| C — mitten in Session, Plugin aus | `opencode run --pure` + „lies mit deinem `read`-Werkzeug" | **1** (`read`) | ✅ `Image read successfully`, korrekte Antwort |
| D — dasselbe, Plugin an | `opencode run` (kein `--pure`) | **1** (`read`) | ✅ identisch korrekt — Plugin fasst Tool-Results nicht an |

**Lauf C/D sind die praktisch wichtigsten:** M3 kann einen Playwright-Screenshot, den es gerade selbst
geschrieben hat, mit dem eingebauten `read`-Tool anschauen — ohne `-f`, ohne Ollama.
Die Sichtprüfungs-Schleife „screenshotten → hingucken → bewerten" braucht damit kein Zusatzwerkzeug.
**Lauf D zeigt: das gilt sofort, nicht erst nach dem Rückbau.** Der Plugin-Hook greift nur die letzte
User-Nachricht ab (`findLastUserMessage` → `isImageFilePart`); ein `read`-Ergebnis ist ein Tool-Part,
kein User-FilePart, und läuft daran vorbei. Gemessen, nicht nur aus dem Quelltext geschlossen.

**Befund 3 — warum Lauf B scheitert.** `DavidEasden/opencode-vision` hängt in
`experimental.chat.messages.transform` und ruft `removeProcessedImageParts()` — es **löscht** den
FilePart und ersetzt ihn durch „ruf `local_vision` mit diesem Pfad auf". Für M2.1, wofür es
geschrieben wurde, ist das die Rettung; für M3 eine Amputation. Verschärft durch
`~/.config/opencode/opencode-vision.json` mit `"models": ["*"]` — der Wildcard matcht auch das
eine Modell, das die Krücke nicht braucht. **Das erklärt auch die Paste-Beschwerde:** Paste läuft
durch denselben Hook, der FilePart wurde dort genauso gelöscht.

**Befund 4 — `local_vision` ist nicht kaputt, nur zu langsam für den Tool-Pfad.** Direkt über
stdio angesprochen antwortet `phase8_6_ui_polish/scripts/mcp_local_vision_server.py` korrekt
(`initialize` + `tools/call` → „Fünf Einträge."). Die Fehlermeldung zu Lauf B lag nie vor — der Stream
liefert nur `status: error`, `output: None`. **Mit hoher Wahrscheinlichkeit** OpenCodes
MCP-Client-Timeout gegen den 46–180 s CPU-Cold-Start von `qwen3-vl:8b`; ein Schema- oder
Framing-Fehler sähe von außen identisch aus und ist nicht ausgeschlossen. Ein 8-B-Vision-Modell auf
CPU passt nicht in einen synchronen Tool-Call; als CLI (`vision_ollama.py`) bleibt es brauchbar.

**Befund 5 — „Bilder im Chat präsentieren" ist in OpenCode gar nicht vorgesehen.** Das
ausgelieferte Web-UI-Bundle (`/assets/index-*.js`, OpenCode 1.18.30) kennt nur die Slots
`prompt-attachments*`, `user-message-attachment`, `user-message-attachment-image` (das einzige
`<img>`), `user-message-attachment-file`, `user-message-attachment-name` — **alle `prompt-` oder
`user-message-`, kein Assistant-/Tool-Result-Bild-Slot.** Die Daten wären vorhanden: ein `read`
auf ein PNG liefert im Tool-State `attachments: [{mime: "image/png", url: "data:image/png;base64,…"}]`.
Das UI rendert sie nur nicht. **Bilder fließen in OpenCode einbahnig: Mensch → Modell, nicht
zurück.** Kein Plugin kann das ändern; es ist eine UI-Grenze, kein Modell-Thema. Damit ist
Konvention §4 der Sichtungs-Schwester-Datei in OpenCode **dauerhaft unerfüllbar** — sie bleibt
Claude-Code-only, und die dortige „Bis das Plugin installiert ist"-Variante (Dateipfad +
Was-zu-validieren-Zeile) gilt für OpenCode auf Dauer statt übergangsweise.

**Nebenbefund (Reboot-Risiko):** `~/.config/opencode/package.json` pinnt `opencode-vision` auf
`file:../../../../tmp/opencode/opencode-vision-src`. `/tmp` überlebt keinen Reboot; ein späteres
`npm install` in dem Verzeichnis bricht. Bei den anstehenden Proxmox-Reboots relevant.

**Doku-Änderungen (kein Produkt-Code angefasst):**
- `docs/concepts/sichtpruefung_automation_tooling.md` — §Messbefund 2026-09-11 (Katalog-Tabelle,
  A/B-Tabelle, die fünf Befunde) + §Empfehlung (Rückbau statt Zusatz-Plugin) neu; die
  Plugin-Rangliste vom 2026-09-08 **verbatim erhalten**, aber nach §Historisch verschoben mit der
  Begründung, warum sie für M2.x weiterhin gilt. Frontmatter nachgezogen.
- `docs/concepts/sichtpruefung_automation_conventions.md` — §4-Überschrift auf „nur Claude Code"
  präzisiert, datierte Korrekturnotiz mit Beleg und Verweis eingefügt.
- Dieser Phase-Head — Modul-Status Zeile 2b auf „⚠️ zurückgebaut" + neue Zeile 2c
  (V-vision-befund), `Nächste Session` neu, Frontmatter-Pipe.

**Verifikation:** `pytest` **966 unverändert** (keine Python-Änderung am Produkt),
Tabu-Diff §0.3 **leer**, **Service-Touch 0** — `sharefyx-mcp` PID **991** über die ganze Session
unverändert (nur via `systemctl show -p MainPID` gelesen). Zwei eigene Wegwerf-`opencode web`-
Instanzen (Ports 18791/18792) gestartet und wieder gestoppt — **PID über den eindeutigen Port
aufgelöst** (`ss -ltnp`), kein `pkill -f`, Hard Rule 9 eingehalten; beide Ports nachweislich frei.

**Eigener Fehler in dieser Session, behoben:** ein Python-Edit am Phase-Head suchte
`s.index("## Nächste Session")` — das matchte die **Frontmatter-Prosa** (dort steht
„`## Nächste Session` neu sortiert" in einem älteren `updated:`-Eintrag) statt der Überschrift und
löschte beim Slicen die Zeilen 23–459, also ~30 KB Head. Per `git checkout` sauber
zurückgeholt, danach mit Zeilenumbruch-Anker (`\n## Nächste Session\n`) plus
Eindeutigkeits-`assert` und Überschriften-Zählung vor/nach jedem Edit wiederholt.
**Lehre für künftige Head-Edits: in diesem Repo enthält die Frontmatter-Prosa die
Überschriftennamen als Zitat — Abschnitts-Slicing nur mit Zeilenanker und Count-Assert.**

**Rückbau vollzogen (Nikinger-Freigabe 2026-09-11, in derselben Session ausgeführt):**
`rm ~/.config/opencode/plugins/opencode-vision.js`. **Gegenprobe grün** — derselbe
`opencode run -f shot.png` wie Lauf B, jetzt **0 Tool-Calls** und korrekte Antwort
(„(1) 6 / (2) nur lesen"); seit dem `rm` erscheint **keine** neue `Plugin initialized`-Zeile
mehr im OpenCode-Log (letzte um 13:32 UTC, `rm` um 18:34 UTC). **Bewusst liegen geblieben,
weil trivial reversibel und ohne Wirkung:** `~/.config/opencode/node_modules/opencode-vision/`
(das Paket selbst), `~/.config/opencode/opencode-vision.json` (Plugin-Config) und der
`local_vision`-MCP-Eintrag in `opencode.jsonc`. Wiederherstellung wäre ein einzelner
`ln -s` — deshalb kein Grund, mehr zu löschen als nötig. Wer M2.x doch braucht, verengt
`"models"` auf `["*/MiniMax-M2*"]`, statt den Symlink wieder zu setzen.

**Rohdaten der Messreihe:** `/tmp/oc-vision-ab/{A,B,C,D}.json` (JSONL-Event-Streams von
`opencode run --format json`, die Belege hinter der Tabelle oben). Liegt bewusst in `/tmp` —
Wegwerf-Verzeichnis, überlebt den nächsten Reboot nicht; die Tabelle ist der dauerhafte Beleg.

**Nächster Schritt, konkret:** Entscheidung zum Rückbau, danach **Block B nach Plan §4**.
