---
status: archive
purpose: Archiv der historischen `[YYYY-MM-DD]`-Session-Blöcke, die bis zum Z-Closeout in `CLAUDE.md` §Current state standen — Phase 1/2/3/4/5/6/6.5/7/8/8.5-Vorlauf + Hard-Rule-Korrekturen + Phase-5-Block-D-Detailnarrative + Deploy-Blocker/Funnel-Recovery-Notizen + diverse Korrekturen
read-when: Auditieren der vollen Wurzel-CLAUDE.md-Historie — der aktuelle Current-state-Absatz lebt im Wurzel-Head, nicht hier
detail: L3
up: ../CLAUDE.md
down:
updated: 2026-10-08 (Wurzel-Block vom **2026-10-08** (B2/E1a/B3) verbatim hierher rotiert, per `scripts/rotate_root_current_state.sh` (K=1); Archiv **221.128 → 222.099 B**) | 2026-10-08 (Wurzel-Block vom **2026-10-07** (Portscan, Oversize-Fix, feedback-Plan) verbatim hierher rotiert, per `scripts/rotate_root_current_state.sh` (K=1) — dessen Nachprüfung zählte bis heute die ganze Datei und brach am datierten Absatz in §Doku-Hygiene ab; Archiv **218.793 → 221.128 B**) | 2026-10-07 (Wurzel-Block vom **2026-10-06** (dritte Sichtprüfung, Lock **P9-BF**) verbatim hierher rotiert, per `scripts/rotate_root_current_state.sh` (K=1); Archiv **216.302 → 218.561 B**, Wurzel-Head **33.821 → 31.562 B**) | 2026-10-06 (Block vom **2026-10-06** (dritte Sichtprüfung, Lock **P9-BF**, Abnahme **P9-120**) verbatim hierher rotiert, per `scripts/rotate_root_current_state.sh` (K=1); Archiv **212.643 → 216.057 B**, Wurzel-Head **32.439 → 31.268 B**) | 2026-10-06 (Block vom **2026-10-06** („Kästchen enger", Mini-Plan §12.1, Locks P9-BB/BC/BD/BE, Abnahme P9-116–P9-119) verbatim hierher rotiert, per `scripts/rotate_root_current_state.sh` (K=1); Archiv **208.146 → 212.370 B**, Wurzel-Head **31.879 → 32.107 B**) | 2026-10-06 (Block „V188 ist beantwortet" verbatim hierher rotiert, per `scripts/rotate_root_current_state.sh` mit K=1 — sechs Gegenproben, darunter die byteweise Reassemblierung und das Nachlesen jedes Blocks; die Byte-Buchhaltung ging auf 237.864 B vorher == 237.864 B nachher) | 2026-10-05 (Block „die sieben Punkte aus der Bildsichtung sind gebaut" verbatim hierher rotiert, per `scripts/rotate_root_current_state.sh` mit K=1 — sechs Gegenproben, darunter die byteweise Reassemblierung und das Nachlesen jedes Blocks; die Byte-Buchhaltung ging auf 234.680 B vorher == 234.680 B nachher) | 2026-10-05 (der Block „die alte Adresse darf unbefristet schreiben" verbatim hierher rotiert, per `scripts/rotate_root_current_state.sh` K=1 — der neue Block über ihm behandelt die sieben Punkte aus der Bildsichtung; **Achtung für den nächsten Faden:** ein Datum mit Leerzeichen und Klammer im Faden **Text** ist für den Anker unsichtbar, das Skript bricht dann mit exit 1 ab) | 2026-10-05 (2 Blöcke der Wurzel verbatim hierher rotiert — der Block vom 2026-10-04 und die datierte Namenskorrektur —, per `scripts/rotate_root_current_state.sh`; die stehende Rotationsregel lebt jetzt als Präambel vor dem ersten Block, damit sie nicht mitrotiert) | 2026-10-04 (**24 Blöcke der Wurzel-`CLAUDE.md` §Current state verbatim hierher**, per `scripts/rotate_root_current_state.sh` K=1; KEEP ist der **neueste** Block, weil die Wurzel newest-**first** ist — im Phase-Head ist es umgekehrt, und die erste Fassung des Skripts hat den ältesten behalten; **sechs Gegenproben**, darunter die byteweise Reassemblierung und die Nachlese jedes Blocks, **221.957 B vorher == 221.957 B nachher**) | 2026-09-10 (P8.6 Step 0 Haushalt-Block aus Wurzel-`CLAUDE.md` §Current state rotiert — Migration-Vorbereitungs-Block brauchte Platz im Wurzel-Head, deshalb der Vorgänger nach hier verschoben; Project-Pattern: jeder neue Current-state-Eintrag rotiert den bisherigen verbatim hierher)
---


## Frontmatter-Archiv — `updated:`-Kette der Wurzel-`CLAUDE.md`

Verbatim rotiert am 2026-09-13. Anlass: die Kette war mit **28.090 B in 30 Eintraegen**
auf **69 %** der Datei gewachsen, waehrend der eigentliche Body nur 12.845 B ausmacht —
derselbe Mechanismus, den die Vormerkung im P8.6-Head fuer `docs/INDEX.md` beschreibt.
Die Eintraege [12]/[17], [13]/[18] und [14]/[19] der Altkette waren **glatte Duplikate**
(3.290 B); sie sind hier bewusst **unveraendert** erhalten, weil Rotation verbatim ist.
Newest-first, genau wie sie im Kopf standen:

1. 2026-09-11 (P8.6 Block B ✅ — Selektion vereinheitlicht + Vorsicht-Kategorie + ein Radius-Fix; `pytest` 967 V107, `ui_budget` V97 5/5 133,1 KB; vier Selbst-Screenshots `p86_block_b_*.png` zeigen alle vier visuellen Ziele; sharefyx-mcp PID 991 unverändert; **Push + Deploy wartet auf Nikinger-Anweisung**)
2. 2026-09-10 (P8.6 Step V deferred — Nikinger-Entscheidung nach kurzer Recherche: lokales Vision-Modell auf neu zu migrierendem Proxmox-Host (i5-14600KF, danach Ryzen 7 5800X) statt Anthropic-Haiku-API. **Backend:** `InternVL 2.5 8B` (Apache-2.0, Q4, ~6–8 GB VRAM) auf Ollama; MCP-Wrapper ruft `POST /api/generate` mit base64-Image. Plugin-Pfad aus Plan §2 als Vormerkung zurückgestellt — die `DavidEasden/opencode-vision`-Landschaft ist zu unreif (3 Commits, AGPL-3.0) für unseren produktiven Use-Case. **Vollständiger Proxmox-Plan + Modell-Recherche:** `phase8_6_ui_polish/CLAUDE.md` §Vormerkungen + Modul-Status Zeile 2. **Nächster Schritt der nächsten Session:** Proxmox-Migration + Ollama-Setup + MCP-Wrapper-Skript, kurze Aktions-Liste nach Nikinger-Wunsch. Kein Code-Touch — nur Doku-Updates in `phase8_6_ui_polish/CLAUDE.md` + `phase8_6_ui_polish_plan.md` §2-Korrekturnotiz + `docs/INDEX.md`-Pipe)
3. 2026-09-10 (P8.6 Step 0 — Haushalt der neuen aktiven Phase 8.6 (Phase 8.5 abgeschlossen, Phase-8.6-Plan ausgeführt); Phasenverzeichnis `phase8_6_ui_polish/` + `CLAUDE.md` (~13 KB, mit Mission/Scope/Harte Regeln/Modul-Status 0–Z/Baselines V97/V107/V108/Vormerkungen/Step-0-Session-Block) + `SESSIONS_ARCHIVE.md` (📦 leer) + `scripts/` (leer, Wegwerf-Smokes folgen in Gate) angelegt; sechs kaputte `up:`/`down:`-Links in `p8x_ui_polish_notes.md` gefixt (`../` → `../../`, war die **einzige** unauflösbare Datei im Repo, von 187 Frontmatter-Links); vier fehlende L1-Header-Cards ergänzt (`docs/PROJECT_SESSION_LOG.md`, `phase8_5_picker_release/{SICHTPRUEFUNG_RESTBLOCK,SICHTPRUEFUNG_WALKTHROUGH,CLUSTER3_TESTBLOCK}.md`); drei `down:`-Listen vom Inline-Format (`·`-Trenner) auf Listenform (`phase6_5_tools_images_plan.md`, `phase6_shares/{GLOBAL_SEARCH,IMAGES}_PLAN.md`); `docs/INDEX.md` von 40.960 B auf **37.763 B** komprimiert (Plan-Zeilen P8.6/P8.5/P8/P7/P6/P6.5/P5/P4/P3/P2 auf Pointer-Form gestrafft — L0 ist Landkarte, keine Kurzfassung, Plan §1.5); zwei fehlende INDEX-Zeilen ergänzt (`CLUSTER3_TESTBLOCK.md`, `THIRD_PARTY_LICENSES.md` mit Ausnahme-Markierung); zwei INDEX-Drift-Korrekturen (`phase8_ui_graph/CLAUDE.md` bekommt die Softcap-Notiz wie `phase6_shares`, `phase5_ui/CLAUDE.md` verliert die falsche „über dem 40"-"-Aussage — real 40.957 B = 3 B unter Cap); zwei echte Code-Defekte **dokumentiert, hier nicht behoben** (`var(--border-soft)` undefiniert an `app.css:1270/1276` → Block A §3.3, `graph.js :: runSimulation()` `rafId` lokal aber nie gelesen → Block D §6.4); `pytest` **964/964** (V107 ✅), `ui_budget.py` **5/5, 130,1 KB** (V97 ✅), **V108 `_overview` ~863 ms offen** (vor Block C drei Läufe mitteln), **kein Code-Touch** (Tabu-Diff §0.3 leer), **Service-Touch 0** (PID 355956 nur gelesen, keine Wegwerf-Instanz gestartet — Step 0 ist Doku + Skelett, kein Lauf gegen den Server); Repo-weiter `up:`/`down:`-Link-Scan: 0 Fehler bei 203 .md-Dateien; **kein Push ohne Nikinger-Anweisung**
4. 2026-09-09 (Phase-8.5-Z-Closeout — Übersichtsgrafik + `PHASE8_5_CLOSEOUT_HANDOVER.md` neu als datierte Umkehr der Locks P8.5-S/P8.5-R, Plan §9 gefüllt; vier Doku-Drifts behoben; `p8x_ui_polish_notes.md` §10 mit neun Nikinger-Punkten + §B-Mobile-Außenkante aufgehoben; Phase-8.5-Head 52.6 → 26.0 KB und Wurzel-Current-state −2 Blöcke nach `PROJECT_SESSION_LOG.md` rotiert, beides per `sed`+`cmp`; pytest 964/964, Tabu-Diff leer, Service-Touch 0)
5. 2026-09-09 (P8.5-6-Folge-Smoke-Sub-Session — Bracket-Pfad live-verifiziert, Phase 8.5 **vollständig abgeschlossen** Bilanz 19/1/0 → **20/0/0**; v3ritt-Wegwerf frisch hochgefahren + Item `itm_b8b989a1` „Vercel [Hosting]" via `storage.Store.create()` angelegt, Mini-Smoke `phase8_5_picker_release/scripts/p856_bracket_mini_smoke.py` neu (~75 Z., Playwright), Screenshot `docs/screenshots/p856_bracket_preview.png` zeigt „Vercel [Hosting]" als klickbaren blauen Hyperlink — programmatische Quittung per Regex True; Wegwerf sauber per PID-Datei gestoppt, kein `pkill -f`; §Abnahmestand Bilanz → **20/0/0**, §Nächste Session auf P8.6-Planung umgeschrieben, Matrix-Zeile P8.5-6 in `SESSIONS_ARCHIVE.md` auf ✅; Frontmatter-Updates in Head + SESSIONS_ARCHIVE + INDEX + ROADMAP; **kein Code-Touch**, pytest unverändert 964/964, Tabu-Diff §0.3 leer, Service-Touch 0 [PID 355956 unverändert])
6. 2026-09-09 (Sichtungs-Sub-Session — 10 P8.5-🟡-Zeilen sichtet, 9 ✅, P8.5-6 bleibt 🟡 wegen fehlendem Vorschau-Screenshot des Bracket-Pfads; vier neue Sichtungs-Konventionen in `docs/concepts/sichtpruefung_automation_conventions.md` §1-§4 notiert [Vorschau-Pflicht / Code-vs-Visuell / Deploy-nach-Test / Screenshots-im-Chat nach opencode-vision-Install]; Phase-8.5-Bilanz 10/10/0 → 19/1/0; alle 9 Dateien aktualisiert — Head + SESSIONS_ARCHIVE (Z-Closeout rotiert) + Konzepte (conventions + tooling) + Walkthrough/Restblock (Vorschau-Top-Notiz) + INDEX + ROADMAP; **kein Code-Touch**, pytest unverändert 964/964, Tabu-Diff §0.3 leer, Service-Touch 0 [PID 355956 unverändert], keine Wegwerf-Instanzen gestartet)
7. 2026-09-08 (Scope-Reversal: 10 P8.5-🟡-Sichtungen bleiben in Phase 8.5 [nicht P8.6 wie Z-Closeout-Summary schrieb]; Current-State-Absatz oben ergänzt; Frontmatter vorne ergänzt; **kein Code-Touch**; pytest unverändert 964/964, Tabu-Diff 0.3 leer, Service-Touch 0 [PID 355956 unverändert])
8. 2026-09-08 (Z-Final: Current-State-Sektion [428 Zeilen, ~48 KB historische Session-Blöcke aus P1-P8.5] nach `docs/PROJECT_SESSION_LOG.md` rotiert [neues L3-Archiv]; Kopf jetzt 166 Zeilen / ~34 KB — **unter dem 40-KB-Softcap**; Frontmatter vorne ergänzt; aktive Phase weiterhin phase8_5_picker_release/CLAUDE.md, die Phase-8/8.5-Heads sind in derselben Z-Final-Runde separat komprimiert worden)
9. 2026-09-08 (Phase 8.5 Z-Closeout — Sichtprüfungs-Automatisierung gegen Wegwerf + echte Produktion, Statusregel geändert (Nikinger-geprüfte Wegwerf-Automatisierung zählt als live-verifiziert), Bilanz 26 ✅ · 0 🟡 · 0 ⬜ für Phase 8 und 10 ✅ · 10 🟡 · 0 ⬜ für Phase 8.5; P8.6 (→v3.0.2) + P9 (→v3.1.0) als Folgephasen vorgemerkt; sechs Wegwerf-Instanzen sauber abgebaut, Produktion PID 355956 durchgehend unangetastet)
10. 2026-09-07 (Cluster-3-Teilverifikation — **P8-20 ✅ + P8-21 a/b/c ✅ am echten v3.0.1** durch den Nikinger in einer Login-Sitzung; P8-20 (Hover dimmt Nicht-Nachbarn + Klick öffnet Editor/Readonly via Fix C vom 2026-09-02 + Drag/Zoom/Pan) und P8-21 (Default nur explizite Kanten + Tag-Toggle + Ordner-Toggle) ohne Befund; P8-21 d + P8-22 + P8-24 in eine Folge-Session verschoben, weil alle drei die 200-Knoten-Wegwerf brauchen (Nikinger-Aktion); Phase-8-Bilanz **19 ✅ · 7 🟡 → 20 ✅ · 6 🟡** (P8-20 🟡 → ✅, P8-21 a/b/c bestätigt bei Beschreibung); `phase8_ui_graph/CLAUDE.md` §7 + Bilanz + Modul-Status Block D nachgezogen; `phase8_5_picker_release/CLUSTER3_TESTBLOCK.md` neu (17 KB, vollständiger Schritt-für-Schritt-Testblock für die Cluster-3-Prüfungen, Audit-Quelle für Z); pytest unverändert 964/964, Tabu-Diff §0.3 leer, Service-Touch 0 (PID 355956 nur gelesen, kein `sudo systemctl`); **Nikinger-Aktion in derselben Sub-Session:** Sean-Einladung — `authctl.py invite sean --purpose initial --ttl 86400` schreibt in die echte `auth.sqlite3` des `sharefyx-mcp.service` (Hard Rule 9 + §0.5.7 verbieten opencode/M3 den Eingriff), Link wird auf stdout einmalig ausgegeben; nächster Schritt Cluster 4 + 5 + Z, nach allen Clustern dann Phase-8-✅-Nachtrag + p8.X-Ankündigung im Z-Closeout)
11. 2026-09-07 (Phase 8.5 Pre-Z-Tausch — **erste opencode/M3-Code-Touch-Session seit Cluster 1**; P8.5-19 (Bauform Radiogruppe statt `<select>`) + P8.5-6 (Bracket-Renderer-Fix in `markdown.js`) committet, beide Zeilen jetzt mit Code + statischem Test; `dialogs.js` (`linkPickerModeEl` raus, neue Modul-Konstante `LINK_PICKER_MODE_NAME`, Selektor-Wechsel von `getElementById` auf `querySelector[All]('input[name="link-picker-mode"]')`, change-Listener iteriert die zwei Radios), `app.html` (`<fieldset class="link-picker-modes">` mit `<legend>Einfügen</legend>` + 2× `<input type="radio" name="link-picker-mode" value="…">` ersetzt `<select id="link-picker-mode">`), `app.css` neuer Block `.link-picker-modes`/`.link-picker-mode` mit `accent-color: var(--accent-line)`, `markdown.js` Link- und Bild-Regex tolerieren jetzt `\[` / `\]` als Escape-Einheit via `\\[\[\]]` (zwei Zeichen), danach `\\([\[\]])` → `$1` zum Unescapen des Title/Alt; `phase5_ui/tests/test_static_routes.py` +2 (`test_link_picker_uses_a_radio_group_not_a_select` P8.5-19, `test_markdown_link_regex_allows_escaped_brackets` P8.5-6 mit Regressionstest gegen die alte `[^\]]+`-Form); pytest 962 → **964** grün (254 s Gesamtlauf), `node --check` grün auf `dialogs.js` + `markdown.js`, `ui_budget.py` 5/5 im Korridor (dialogs.js 12.6 → 13.2 KB, markdown.js 4.2 KB, app.css +0.4 KB), Tabu-Diff §0.3 leer (alle Änderungen unter `phase5_ui/webui/static/` + `phase5_ui/tests/`, kein Servercode-Tabu-Auslöser), node-Probe gegen `markdown.js` mit Mock-`document`: 8 Test-Cases rendern wie erwartet — darunter D4-Fund-Beispiel `[Vercel \[Hosting\](#item/itm_67bb0565)` → `<a href="#item/itm_67bb0565">Vercel [Hosting]</a>`; Phase-8.5-Summary **5 ✅ · 13 🟡 · 2 ⬜ → 5 ✅ · 14 🟡 · 1 ⬜** (P8.5-19 ⬜ → 🟡, P8.5-5/-6-Beschreibungen aktualisiert); Phase-8-Bilanz unverändert 19/7/0; Phase-8.5-Head rotiert (Cluster-1-Block per Hand nach `SESSIONS_ARCHIVE.md`, dieser Pre-Z-Tausch-Block neu im Head, **~49 KB deutlich über 40-KB-Softcap** — Auflösung bleibt Z-Arbeit oder Trimm-Pass vor Z, gleiche Linie wie D3/D4 dokumentiert); Working Tree jetzt 7 uncommittete Dateien [5 Code/Tests + 2 Doku-Updates]; nächster Schritt unverändert Cluster 3+4+5 (Nikinger-Aktionen) + Z, mit optionaler P8.5-6-Wegwerf-Re-Probe in Cluster 4)
12. 2026-09-07 (Phase 8.5 + Phase 8 Cluster-2 — **erste echte Live-Verifikations-Welle seit D3**; Nikinger gegen v3.0.1 bestätigt: P8-14, P8-15, P8-18, P8-19, P8-23 (Screenshot `phase8_5_picker_release/screenshots/Bildschirmfoto 2026-09-07 um 17.08.37.png` zeigt tabellose Space-Zeilen + Zähler-Chips + VERKNÜPFUNGEN-Graph in eigen blau/geteilt türkis/fremd grau + ZULETZT-BENUTZT-Sektion + Badge `SHAREFYX v3.0.1`); P8.5-18 jetzt ✅ als Umbrella; Phase-8-Bilanz 14/12/0 → **19/7/0**, Phase-8.5-Bilanz 4/13/3 → **5/13/2** (P8.5-18 von ⬜ auf ✅); Phase-8-Glyph-Entscheidung noch offen (Vorschlag vorerst 🟡 bis Cluster 3/5); P8-20/21/22/24 + P8-5/8 bleiben 🟡 für Cluster 3/5; keine Code-Änderung in dieser Sub-Session — alle Updates sind Doku; Phase 8.5 Head rotiert (40.5 KB unter Cap); Working Tree jetzt 14 uncommittete Dateien [7 von D4+Sichtprobe-Folgesession + 7 von Cluster 1+2]
13. 2026-09-07 (Phase 8.5 Cluster-1 der Sichtprüfungen — **erste echte Code-Touch-Session seit D1**; `phase8_ui_graph/scripts/p8_16_glass_fallback_probe.py` + `wegwerf_setup_p8_16.py` neu (Port 18775, Standing-Permission-Muster reproduziert), vier Screenshots `docs/screenshots/p8_16_{01..04}_*.png`; CDP-Switch `prefers-reduced-transparency: reduce` über `Emulation.setEmulatedMedia` — beide Glass-Träger `.list__head`+`.overlay__panel` wechseln sauber `blur(14px) saturate(1.5)`+`rgba(27,32,39,0.55)` → `backdrop-filter: none`+`rgb(27,32,39)`, Selektion im Solid-Modus voll erkennbar mit Akzent-Fill+Outline; **P8.5-16 jetzt ✅**, doppelt mit Phase 8 P8-16 die selbe Evidenz; Phase-8-P8-16 bleibt 🟡 bis Nikinger-Sichtprüfung; Phase-8.5-Summary 3 ✅ · 14 🟡 · 3 ⬜ → **4 ✅ · 13 🟡 · 3 ⬜**; Phase-8.5-Head rotiert (40.579 B, 381 B unter 40-KB-Softcap); Working Tree jetzt 13 uncommittete Dateien [7 von D4+Sichtprobe-Folgesession + 6 von Cluster 1]; `pytest`/`node --check`/`ui_budget.py` nicht gelaufen (irrelevant), Tabu-Diff §0.3 leer (Phase-8.5-Tabu greift nicht für `phase8_ui_graph/scripts/`), Service-Touch 0 nur gelesen (PID 355956 unverändert seit 2026-09-05 16:10:18 CEST); nächster Schritt Cluster 2-5 je nach Nikinger)
14. 2026-09-06 (Phase 8.5 D4-Sichtprobe-Folgesession — **nur dokumentiert, kein Code-Touch in dieser opencode/M3-Session**; sieben neue Themen-Cluster aus der Sichtprobe mit Fabian nach D4 dokumentiert: **Spaces-Layout-Reorg** [„Alle Items"-Leiste unter Spaces + Kippschalter, Map 40 % Breite/volle Höhe, keine Duplikate], **Obsidian-Map** fünf Sub-Punkte [Performance-Reload, Landkarten-Stil, Field schneidet ab, Reload-Drift, Collapsible mit Abhängigkeiten], **Anzahl-Anzeige Ordner**, **Edit-in-Place-Vision** [„Bearbeiten"-Knopf überflüssig], **Layering-Design-System** [3 Layer: echtes Schwarz / aktueller Standard / Liquid Glass + Selektion explizit blau auf Hover, Note-Select, Checkbox], **„Konto"→„Einstellungen"-Rename** + Positions-Tausch mit Logout, **De-AI-ierung-Lauf 2** nach neuen Kriterien; neue Datei `docs/concepts/p8x_ui_polish_notes.md` 25 KB L2 mit allen 16 Themen — fünf bereits in D4 dokumentierte p8.X-Punkte [UX-2-Step-Knotenklick, Map-Field schneidet ab, Map fliegt, Save-Button-YAML-Header, Fabis Sammelliste] + sieben Sichtprobe-Folgesession-Cluster + vier Sub-Punkte aus §2 Obsidian-Map; Anhang §A–§E für die Planungs-Session in Claude Code; **kein Phase-8/8.5-Scope-Touch**, **keine** neuen Tabu-Aufhebungen, **kein** Locking — Sammlung, kein Plan; D4-Block per Hand nach `SESSIONS_ARCHIVE.md` rotiert (Skript passt nicht auf Phase-8.5-Muster, bewährtes Vorgehen); Modul-Status P8.5 unverändert (3 ✅ · 14 🟡 · 3 ⬜); pytest nicht gelaufen, Tabu-Diff §0.3 leer, Service-Touch 0; nächster Schritt unverändert D5 + V105 + optional vor Z Radiogruppe + Bracket, dann Z)
15. 2026-09-06 (Phase 8.5 D4 Sichtprüfung am echten Gerät durch den Nikinger — **nur dokumentiert, kein Code-Touch in dieser opencode/M3-Session**; Block 1–7 + Vorbereitung komplett durchgelaufen, Login beide Accounts ✅, Tastaturnavigation in Firefox+Chrome+Safari auf zwei Accounts ✅, Block 2/4/5-Kern ohne Befund, drei echte Funde dokumentiert: **P8.5-19-Entscheidung Radiogruppe** [User-Präferenz „deut... (line truncated to 2000 chars)
16. 2026-09-05 (Phase 8.5 D2 vom Nikinger zwischen D1 und D3 + D3-Prep, 🟡, ⬜ D4/D5/V105/Z als Nächstes. D2 ist **zwischen D1 (Commit heute früh) und D3 (diese Session) still durch den Nikinger gelaufen** — Entdeckung kam erst beim ersten Probe-Lauf des Health-Gate-Skripts: `/opt/sharefyx/current` → `20260905T140325.378914Z` → HEAD `6f19a8f` (D1), Service-PID **355956** (statt der im D1-Block notierten 195922 — D2-Deploy hat den Dienst erwartungsgemäß neu gestartet), `ExecMainStartTimestamp=2026-09-05 16:10:18 CEST`. Damit ist D3 nicht mehr Vorbereitung, sondern **Verifikation des bereits deployten v3.0.1**. Neu gebaut: `phase8_5_picker_release/scripts/health_gate.sh` (134 Zeilen bash, `set -uo pipefail`, JSON auf stdout / Details auf stderr nach Hard Rule 7), acht Gates — `/health` 200 mit Retry-Loop, `/ui/login` 200, `/api/v1/me` 401, `/mcp/` 401, `.rail__version` aus `/ui/static/app.html` (**nicht** `/ui/login` — `pages.py`s Auth-Template ohne Rail, erste Iteration fiel darauf herein, gefixt), `/opt/sharefyx/current` → Release mit `.git`, optional `--require-todays-update-log` (UTC/local wie `deploy.sh` Z. 127-131), optional `--expected-sha=<hex>` (Short- oder Full-Form per Prefix-Vergleich). **Lauf-Beleg 2026-09-05 15:19:53Z** mit `--require-todays-update-log --expected-sha=6f19a8f`: **8/8 grün**, Exit 0, JSON auf stdout (`result:"ok"`, `actual_version:"v3.0.1"`, `release_sha:"6f19a8f..."`, `active_release:"/opt/sharefyx/releases/20260905T140325.378914Z"`, `port:8765`). Drei Negativproben separat verifiziert (Port 9999 → Gate 1 rot, `--expected-version=v9.9.9` → Gate 5 rot, `--expected-sha=0000000` → Gate 8 rot). **P8.5-17 teilweise abgehakt:** Deploy gelaufen ✅, Health-Gate 8/8 ✅, Badge `v3.0.1` live ✅, Update-Banner-Live-Anzeige ⬜ (braucht Auth, Nikinger), V105 ⬜ (echter Anthropic-Connector, Nikinger). Modul-Status-Zeile 6 Block D um D2 ✅ + D3 🟡 erweitert; Abnahmestand-Zeile P8.5-17 Health-Gate-Teil 🟡; Summary **3 ✅ · 14 🟡 · 3 ⬜ von 20**; D1-Block (111 Zeilen) per Hand nach `SESSIONS_ARCHIVE.md` rotiert (Skript passt nicht auf das Phase-8.5-Muster — bewährtes Vorgehen aus D1 selbst). `pytest` nicht gelaufen (kein Python-Touch), `bash -n` OK, shellcheck nicht verfügbar (übersprungen, keine Konvention im Repo), Tabu-Diff §0.3 leer, Service-Touch 0 (PID 355956 nur gelesen). **Nächster Schritt:** D4 — Sichtprüfung am echten Gerät durch den Nikinger (`## 2026-09-05`-Eintrag im Update-Banner sichtbar, `<select class="input" id="link-picker-mode">` im Picker vorhanden — P8.5-19-Abnahme: Radiogruppe oder `<select>`-Bestätigung), D5 Vierte A3-Probe (entscheidet §9.4.1 Abbruchregel aus N2), V105-Connector-Check, Z Closeout. 2026-09-07 (Phase 8.5 Pre-Z-Tausch — **erste opencode/M3-Code-Touch-Session seit Cluster 1**; P8.5-19 (Bauform Radiogruppe statt `<select>`) + P8.5-6 (Bracket-Renderer-Fix in `markdown.js`) committet, beide Zeilen jetzt mit Code + statischem Test; `dialogs.js` (`linkPickerModeEl` raus, neue Modul-Konstante `LINK_PICKER_MODE_NAME`, Selektor-Wechsel von `getElementById` auf `querySelector[All]('input[name="link-picker-mode"]')`, change-Listener iteriert die zwei Radios), `app.html` (`<fieldset class="link-picker-modes">` mit `<legend>Einfügen</legend>` + 2× `<input type="radio" name="link-picker-mode" value="…">` ersetzt `<select id="link-picker-mode">`), `app.css` neuer Block `.link-picker-modes`/`.link-picker-mode` mit `accent-color: var(--accent-line)`, `markdown.js` Link- und Bild-Regex tolerieren jetzt `\[` / `\]` als Escape-Einheit via `\\[\[\]]` (zwei Zeichen), danach `\\([\[\]])` → `$1` zum Unescapen des Title/Alt; `phase5_ui/tests/test_static_routes.py` +2 (`test_link_picker_uses_a_radio_group_not_a_select` P8.5-19, `test_markdown_link_regex_allows_escaped_brackets` P8.5-6 mit Regressionstest gegen die alte `[^\]]+`-Form); pytest 962 → **964** grün (254 s Gesamtlauf), `node --check` grün auf `dialogs.js` + `markdown.js`, `ui_budget.py` 5/5 im Korridor (dialogs.js 12.6 → 13.2 KB, markdown.js 4.2 KB, app.css +0.4 KB), Tabu-Diff §0.3 leer (alle Änderungen unter `phase5_ui/webui/static/` + `phase5_ui/tests/`, kein Servercode-Tabu-Auslöser), node-Probe gegen `markdown.js` mit Mock-`document`: 8 Test-Cases rendern wie erwartet — darunter D4-Fund-Beispiel `[Vercel \[Hosting\](#item/itm_67bb0565)` → `<a href="#item/itm_67bb0565">Vercel [Hosting]</a>` (vor dem Fix kaputt); Phase-8.5-Summary **5 ✅ · 13 🟡 · 2 ⬜ → 5 ✅ · 14 🟡 · 1 ⬜** (P8.5-19 ⬜ → 🟡, P8.5-5/-6-Beschreibungen aktualisiert); Phase-8-Bilanz unverändert 19/7/0; Phase-8.5-Head rotiert (Cluster-1-Block per Hand nach `SESSIONS_ARCHIVE.md`, dieser Pre-Z-Tausch-Block neu im Head, **~49 KB deutlich über 40-KB-Softcap** — Auflösung bleibt Z-Arbeit oder Trimm-Pass vor Z, gleiche Linie wie D3/D4 dokumentiert); Working Tree jetzt 7 uncommittete Dateien [5 Code/Tests + 2 Doku-Updates]; nächster Schritt unverändert Cluster 3+4+5 (Nikinger-Aktionen) + Z, mit optionaler P8.5-6-Wegwerf-Re-Probe in Cluster 4)
17. 2026-09-07 (Phase 8.5 + Phase 8 Cluster-2 — **erste echte Live-Verifikations-Welle seit D3**; Nikinger gegen v3.0.1 bestätigt: P8-14, P8-15, P8-18, P8-19, P8-23 (Screenshot `phase8_5_picker_release/screenshots/Bildschirmfoto 2026-09-07 um 17.08.37.png` zeigt tabellose Space-Zeilen + Zähler-Chips + VERKNÜPFUNGEN-Graph in eigen blau/geteilt türkis/fremd grau + ZULETZT-BENUTZT-Sektion + Badge `SHAREFYX v3.0.1`); P8.5-18 jetzt ✅ als Umbrella; Phase-8-Bilanz 14/12/0 → **19/7/0**, Phase-8.5-Bilanz 4/13/3 → **5/13/2** (P8.5-18 von ⬜ auf ✅); Phase-8-Glyph-Entscheidung noch offen (Vorschlag vorerst 🟡 bis Cluster 3/5); P8-20/21/22/24 + P8-5/8 bleiben 🟡 für Cluster 3/5; keine Code-Änderung in dieser Sub-Session — alle Updates sind Doku; Phase 8.5 Head rotiert (40.5 KB unter Cap); Working Tree jetzt 14 uncommittete Dateien [7 von D4+Sichtprobe-Folgesession + 7 von Cluster 1+2]
18. 2026-09-07 (Phase 8.5 Cluster-1 der Sichtprüfungen — **erste echte Code-Touch-Session seit D1**; `phase8_ui_graph/scripts/p8_16_glass_fallback_probe.py` + `wegwerf_setup_p8_16.py` neu (Port 18775, Standing-Permission-Muster reproduziert), vier Screenshots `docs/screenshots/p8_16_{01..04}_*.png`; CDP-Switch `prefers-reduced-transparency: reduce` über `Emulation.setEmulatedMedia` — beide Glass-Träger `.list__head`+`.overlay__panel` wechseln sauber `blur(14px) saturate(1.5)`+`rgba(27,32,39,0.55)` → `backdrop-filter: none`+`rgb(27,32,39)`, Selektion im Solid-Modus voll erkennbar mit Akzent-Fill+Outline; **P8.5-16 jetzt ✅**, doppelt mit Phase 8 P8-16 die selbe Evidenz; Phase-8-P8-16 bleibt 🟡 bis Nikinger-Live-Sichtprüfung; Phase-8.5-Summary 3 ✅ · 14 🟡 · 3 ⬜ → **4 ✅ · 13 🟡 · 3 ⬜**; Phase-8.5-Head rotiert (40.579 B, 381 B unter 40-KB-Softcap); Working Tree jetzt 13 uncommittete Dateien [7 von D4+Sichtprobe-Folgesession + 6 von Cluster 1]; `pytest`/`node --check`/`ui_budget.py` nicht gelaufen (irrelevant), Tabu-Diff §0.3 leer (Phase-8.5-Tabu greift nicht für `phase8_ui_graph/scripts/`), Service-Touch 0 nur gelesen (PID 355956 unverändert seit 2026-09-05 16:10:18 CEST); nächster Schritt Cluster 2-5 je nach Nikinger)
19. 2026-09-06 (Phase 8.5 D4-Sichtprobe-Folgesession — **nur dokumentiert, kein Code-Touch in dieser opencode/M3-Session**; sieben neue Themen-Cluster aus der Sichtprobe mit Fabian dokumentiert: Spaces-Layout-Reorg, Obsidian-Map [5 Sub-Punkte], Anzahl-Anzeige Ordner, Edit-in-Place-Vision, Layering-Design-System [3 Layer + Selektion blau], „Konto"→„Einstellungen"-Rename, De-AI-ierung-Lauf 2; neue Datei `docs/concepts/p8x_ui_polish_notes.md` 25 KB L2 mit allen 16 Themen — fünf D4-Punkte + sieben Sichtprobe-Folgesession-Cluster + vier Sub-Punkte aus §2 Obsidian-Map; Anhang §A–§E für die Planungs-Session; **kein Plan, kein Locking, keine Tabu-Aufhebung** — Sammlung; neue ROOT-Current-State-Zeile für die Folgesession ergänzt; `phase8_5_picker_release/CLAUDE.md` aktiver Block auf D4-Sichtprobe-Folgesession umgestellt, D4-Block per Hand nach `SESSIONS_ARCHIVE.md` rotiert (Skript passt nicht auf Phase-8.5-Muster); keine Code-Tests, kein Service-Touch; nächster Schritt D5 Vierte A3-Probe + V105 Connector-Check — beides Nikinger; optional vor Z Radiogruppe-Tausch + Bracket-Fix durch opencode/M3)
20. 2026-09-06 (Phase 8.5 D4 Sichtprüfung durch den Nikinger — **nur dokumentiert, kein Code-Touch in dieser opencode/M3-Session**; Block 1–7 + Vorbereitung komplett durchgelaufen, drei echte Findings: **P8.5-19 Radiogruppe statt `<select>`** [Tausch 5 Z. ausstehend], **P8.5-6 Bracket-Renderer-Bug in `markdown.js`** [Fix ausstehend], **UX-2-Step-Knotenklick als neues Feature für p8.X** [parkiert]; Phase 8 ✅ + p8.X als Nikinger-Entscheidung für Z vorgemerkt; Modul-Status Zeile 6 Block D um D4 ✅ erweitert; Summary 3 ✅ · 14 🟡 · 3 ⬜; D3-Block per Hand nach SESSIONS_ARCHIVE.md rotiert; keine Code-Tests, kein Service-Touch; nächster Schritt D5 Vierte A3-Probe + V105 Connector-Check — beides Nikinger; optional vor Z Radiogruppe-Tausch + Bracket-Fix durch opencode/M3)
21. 2026-09-05 (Phase 8.5 D3-Prep — `scripts/health_gate.sh` neu, 134 Zeilen bash, acht Gates; **Lauf 2026-09-05 15:19:53Z 8/8 grün** gegen den frischen Deploy; **D2 lief zwischen D1 und D3 still durch den Nikinger** (PID 355956 statt 195922, Release `20260905T140325.378914Z`, ExecMainStartTimestamp `2026-09-05 16:10:18 CEST`) — D3 ist Verifikation statt Vorbereitung; D1-Block per Hand nach `SESSIONS_ARCHIVE.md` rotiert; Modul-Status Zeile 6 um D2 ✅ + D3 🟡 erweitert; Abnahmestand P8.5-17 Health-Gate-Teil 🟡, Summary-Zeile 3 ✅ · 14 🟡 · 3 ⬜; pytest nicht gelaufen (kein Python-Touch), bash -n OK, shellcheck nicht verfügbar (übersprungen, keine Konvention im Repo), Tabu-Diff §0.3 leer, Service-Touch 0; nächster Schritt D4 Sichtprüfung am echten Gerät — Nikinger-Aktion)
22. 2026-09-05 (Phase 8.5 D1 committet — Badge `v3.0`→`v3.0.1` in `phase5_ui/webui/static/app.html:20` (P8.5-N7, statisches HTML nicht im Tabu §0.3); neuer `## 2026-09-05`-Block in `docs/UPDATE_LOG.md` mit drei Zeilen Picker-Modi/Tastatur/Generalisierter-Hint — **Datums-Drift dokumentiert**: Block-C-Absatz schlug `## 2026-09-04` vor, `date +%F`/`date -u +%F` ist heute 2026-09-05, `deploy.sh` Z. 117–131 verlangt strikt `today_utc`/`today_local`, sonst Gate-Abbruch; Block-C-Block per Hand nach `SESSIONS_ARCHIVE.md` rotiert (Skript passt nicht auf Phase-8.5-Muster mit einem `## Session stopped` + mehreren `### date`-Subblöcken → Exit 2 „Bereits konform"); Modul-Status D `⬜`→`🟡` mit D2–D5 als Nikinger-Aktionen vermerkt; `pytest` nicht gelaufen (kein Python-Touch), Tabu-Diff §0.3 leer, Service-Touch 0 (PID 195922 / ActiveEnterTimestamp 2026-09-02 11:51:57 CEST nur gelesen); nächster Schritt D2 = `sudo systemctl ... deploy.sh main`)
23. 2026-09-04 (Wurzel-CLAUDE.md komprimiert -- Phase-6-Verlaufsdokumentation + Phase-6/6.5-Vormerkungen + Funnel-Reboot + MCP-Werkzeug-Ergonomie + End-Korrekturen P5/P4 auf Pointer-Form gestaucht; ~5 KB freigemacht, aktueller Stand ~39.7 KB unter Cap; Phase-8.5-Work-Abschnitt aktualisiert auf A1+A2, A1-Block rotiert nach Archiv)
24. 2026-09-04 (Phase 8.5 B1 committet -- `_TITLE_NOT_ID_HINT` in `phase2_mcp/mcpserver/tools.py:159-164` generalisiert, „Das gilt in jeder Textform -- auch nicht als Tabellen-Spalte, nicht in Klammern hinter dem Titel und nicht in Aufzählungs-Zeilen" wörtlich aus Plan §3 B1; `test_tools.py` zwei Asserts (`in jeder Textform`/`Klammern`); neuer Phase-Head-Abschnitt `## Abbruchregel §9.4.1 (N2, verbindlich)`; Modul-Status B1 + P8.5-3, A2-Block nach `SESSIONS_ARCHIVE.md` rotiert; pytest 962/962 unverändert, Tabu-Diff zeigt **genau** `tools.py +5/-2` und `test_tools.py +2`, kein Service-Touch)
25. 2026-09-04 (Phase 8.5 A2 committet `7ce0be0` -- Tastaturnavigation `aria-activedescendant` + `_pickLinkPickerAt` + CSS-Block-Entdopplung am Picker; +3 statische Tests in `test_static_routes.py`; A1-Block nach `SESSIONS_ARCHIVE.md` rotiert)
26. 2026-09-04 (Phase 8.5 Drift nachgezogen `4424310` + A1 committet `499d9be` -- Picker-Modus-Umschalter + `localStorage` `sfx:linkpicker:mode`; V99 `session` zu `local` als Eskalation wegen P8.5-G; erste `localStorage`-Nutzung des Projekts)
27. 2026-09-03 (Phase 8.5 Step 0 -- Skelett phase8_5_picker_release/{CLAUDE.md, SESSIONS_ARCHIVE.md, scripts/} angelegt; vier Paragraph-1-Funde: INDEX 52.911 zu 40.917 B unter Cap, Bueroklammer-zu-Lupe-Drift in phase8_ui_graph/CLAUDE.md:440, Phase-8-Bilanz korrigiert; ROADMAP-Abschnitt neu; Wurzel-`down:` umgestellt)
28. 2026-09-01 (Phase 8 Sichtpruefung 1 + Gate B zu C bestanden; **Hard Rule 9 ergaenzt** -- kein `pkill -f` mit Regex, niemals den systemd-Dienst anfassen, Lehre aus dem Prod-Vorfall 2026-09-01 Phase 8 Step A3 Nachbereitung)

**[2026-10-08, feedback-Block B4–B6 gebaut — Mitgliederzeilen, Titelzeile im Löschdialog, Enter-Handler; dazu ein echter Fund im Löschdialog]** Claude Code, vier Commits, kein Deploy, kein Service-Touch. **B4:** die Mitgliederzeilen sitzen 8 px auseinander, „Entfernen" rechtsbündig (Sichtprüfung des Nikingers) — P9-130. **B5:** der Löschdialog zeigt den Titel als eigene Zeile über dem Feld, per `textContent` — P9-129. **B6:** Enter löst in den Overlays die Primäraktion aus, gesperrte Knöpfe bleiben folgenlos (P9-128 ✅, **P9-127 ⚠️**: im Browser belegt sind Anlegen, Löschen, `<select>`, Passwort-Panel). **Fund:** nach „Abbrechen" blieb im Löschdialog der Absenden-Listener stehen, der nächste Löschvorgang schickte **zwei** DELETEs — behoben, Gegenlauf rot. Matrix 116 ✅ · 13 ⚠️ · 1 ⬜, `pytest` 1264. **Nächster Schritt B7** (Übersicht: Name vor den Zählern), dann B8 (Ladezeit **messen**), Übergabe im Phase-9-Head. Beim Nikinger: Sichtprüfung, Deploy `v3.1.4`.

**[2026-10-08, feedback-Block B2, E1a und B3 gebaut — Team-Spaces sind jetzt gemeinsame Ordner]** Claude Code, vier Commits, kein Deploy, kein Service-Touch. **B2:** der Anlegen-Dialog nennt sein Ziel (P9-125). **E1a:** in einem Team-Space (kein Home-Space eines Nutzers) verschiebt, zieht und löscht jedes Mitglied mit `write:` auch fremde Items; fremde Home-Spaces bleiben bei P9-K; der Löschdialog nennt `updated_by`, der Papierkorb-Commit trägt den Löschenden (P9-135–137). Dabei **ein Loch seit Step 7b behoben**: ein PATCH, der den eigenen Space wiederholt, umging beide Ordner-Riegel. **B3:** „Schließen" im Einstellungsmenü (P9-131). Matrix 113 ✅ · 12 ⚠️ · 1 ⬜ (neuer Teil `ABNAHME_MATRIX_FEEDBACK.md`), `pytest` 1261. **Nächster Schritt B4**, Übergabe im Phase-9-Head.

**[2026-10-07, der Portscan von außen ist gelaufen — P9-11 und P9-94 ✅, und der einzige Ausreißer war der Mobilfunkpfad]** Claude Code, ein Commit, kein Code, kein Deploy, kein Service-Touch. Der Nikinger fuhr die vier Läufe aus Mini-Plan §5 vom MacBook (Hotspot ohne Tailscale für Heim-IP und VPS, Hotspot mit Tailscale für die Tailnet-IP, Heim-WLAN für das LAN). Heim-IP `176.2.194.125`: 999 `filtered`; VPS: nur 80/443 offen, 22 zu; LAN: 8765 nicht offen. **Beide öffentlichen Ziele zeigten zusätzlich `21/tcp open`** — ein **Kontrolllauf gegen `1.1.1.1` und `9.9.9.9`** zeigt dasselbe `21 open … syn-ack`, also beantwortet etwas auf dem Mobilfunkpfad Port 21 für jedes Ziel. Das ist eine **benannte Grenze**, kein Befund: auf der VM lauscht nichts auf 21, und sie hat keine globale IPv6. **Zwei echte Punkte für P10:** Lauf 4 (`100.93.43.122:8765` vom MacBook) ist **`open`** und widerlegt die Plan-Prämisse, die ACL lasse nur den VPS durch — im Tailnet sind Auth und Host-Prüfung der App die einzige Sperre; und ein Vollscan des LAN zeigt **sechs Ports auf `0.0.0.0`** (Sunshine plus 7070/7777). Matrix eine offene Zeile (P9-13/V150, wandert nach P10), Rohausgabe `phase9_hardening/probes/p9_11_portscan_2026-10-07.txt`. **Nichts blockiert den P9-Closeout mehr — die Entscheidung liegt beim Nikinger.** **Am selben Tag der Oversize-Fix:** Abnahmematrix (98.782 B) in Hub + drei lebende Teile geteilt, settings-Plan und Step-A-Runbook auf 29,5 / 17,5 KB, alles verbatim per neuem `scripts/move_sections.py`; Danach `ROADMAP.md` 48,5 → 35,7 KB (Kette mit vier eingebetteten `updated: `-Präfixen repariert und rotiert, **P9-6 ⚠️ → ✅**). Offen und benannt: die Heads von P8.6/P8/P6; `docs/INDEX.md` liegt ~170 B unter dem Cap — der nächste Engpass. **Abends:** die Nutzer-Rückmeldung als Plan `phase9_hardening_block_feedback_plan.md`. Der Nikinger hat E1 freigegeben (Team-Spaces, Eigentum über den Git-Autor) und E2/E3 nach P10 gelegt. **Closeout P9 erst nach dem Bau dieses Blocks.**

**[2026-10-06, die dritte Sichtprüfung: siebenmal ✅, ein Punkt aus Bild 08 — und dieser Punkt ist die Kehrseite des Locks vom Vortag]** opencode/M3, ein Commit, reines CSS (eine Regel), kein Deploy, kein Service-Touch. Freigegeben: **01** *„passt"* · **02** *„sieht für mich passend aus"* · **03** *„sieht gut aus"* · **05** *„yo, passt"* · **06** *„identisch zu 1, passt"* · **07** *„passt so"* — und **04 mit dem ersten Einwand, am selben Tag zurückgenommen** (*„ah, nehme 04 zurück, man muss scrollen. Passt so"*). Aus **08** kam ein **neuer Lock (P9-BF)** und die Abnahme **P9-120**: *„den Auswahl buttons der einzelnen Spaces bitte ein paar Px nach links erweitern, sodass innerliegender Text und Button Grenze den Standard Abstand einhalten"*. **Gemessen vorher:** innen **1 px links** gegen **9 px rechts** — und das ist **die Folge des Locks von gestern**: bei 330 px Breite fiel der linke Rand nie auf, seit das Kästchen sein Label umklammert (92–155 px), **ist** die linke Innenkante sichtbar. Gebaut als `padding-left: var(--space)` **plus** `margin-left: calc(var(--space) * -1)` an derselben Kante, weil **beides nötig ist**: `0` allein ist sein Befund, das Polster allein schiebt die Beschriftung 8 px nach rechts und bricht P9-AX. Nachher innen **9 px wie rechts**, Kästchen **−8 px** in das Panelpolster, Beschriftung weiter **1 px** bündig. Probe **50/50**, **Gegenläufe 7 von 7** (`g19` ist der neue Lock als Mutation), `pytest` 1245 → **1246**, `ui_budget` 5/5, Tabu-Diff leer. **Ein Wächter neu, drei umgeschrieben, keiner gelöscht** — und **dieselbe Lücke zum dritten Mal in diesem Projekt**: `margin-bottom` stand auf **keiner** Verbotsliste, obwohl der Test behauptete, er würde es melden (die Liste wird namensgenau geprüft, `margin\s*:` matcht `margin-bottom` nicht) — genau wie vorher `padding-block` und `border-box`; eine Eigenschaft, die kein Wächter kennt, meldet kein Wächter. Der Abstand-Wächter prüft jetzt **namensgenau** statt per Substring, und die Station P9-117 rechnet **beide** Polster, weil links nicht mehr `0` steht. **Alle acht Bilder neu aufgenommen, 08 ist die einzige verlangte Neuerstellung — und danach *„perfekt, passt“*: der Block ist durch.**

**[2026-10-06, der Block „Kästchen enger“ ist gebaut — drei Korrekturen, und der Auftrag hat sich selbst eingeschränkt]** opencode/M3, ein Commit, reines Frontend (eine `.css`-Regelgruppe, **eine** `.html`-Zeile), kein Deploy, kein Service-Touch. Der Nikinger hat auf **zwei** Rückfragen mit **je einem Wort** geantwortet und dabei den Auftrag aus Bild 08 **selbst eingegrenzt**: *„nur bei Spaces verwalten, dort die Buttons der einzelnen Spaces nach Links, und das Fenster rechts verkleinern, aber nur dieses“* ⇒ **P9-BA ist widerrufen** (die Menüpunkte behalten ihre 131 px) und das *Fenster verkleinern* ist ein **neuer Lock P9-BE**. Zu Bild 01 wählte er **(b) zusätzlich flacher**: die Menüpunkte tragen jetzt `padding-block: calc(var(--space) * 0.5)` und messen **31,69 px** statt 35,69 px — die erste bewusste Abweichung von P9-AF, das die Höhe an `.tree__folder` band, im Wächter an **einen** Wert gebunden. Die Space-Zeilen **umklammern ihr eigenes Label** (92–147 px statt 330 px, rechts 9 px statt 192–245 px, die Beschriftung bleibt 1 px bündig mit dem Titel), und **nur** das Spaces-Fenster wird schmaler (**338 statt 380 px**, im Schmal-Modus zurückgenommen — 422 px, das Panel flext). Bild 04 nennt jetzt die **Position** der Hinzufügen-Optionen (y 205..246; *„where did the space hinzufügen options go?“ war ein **Kriteriumfehler**, kein Defekt), Bild 07 **rollt die neue Zeile auf** (`scrollIntoView`, Ausgangszustand messbar: vorher y 1704 bei `scrollTop` 0, also unterhalb des Folds) und nimmt die Anlegezeile mit. **Abnahme P9-116–P9-119 mit 4 ✅**, Probe **48/48**, **Gegenläufe G13–G18 6 von 6** wirksam, `pytest` **1241 → 1245** (+4, keiner gelöscht, keiner umgedreht), `ui_budget` 5/5, Tabu-Diff §0.3 leer. **Fünf eigene Fehler, vier davon derselbe Typ — *eine Regel, die nicht die ist, die ich meine*: (1)** `min-width`/`max-width` sind bei `box-sizing: border-box` die Breite des **Rahmens** (288 px ergaben 240 px Inhalt und ein 88-px-Feld — die Browser-Probe meldete es, der Wächter nicht, er verglich „schmaler als die Basis“ und war mit 288 gegen 340 **auf der falschen Seite**); (2)** `width: 100%` stand in der **Sammelregel**, nicht in der eigenen Regel (G15 maß 28 Kästchen auf 238 px); (3)** eine Station, die den eigenen Fehler nicht bemerkte (jetzt Feldanteil ≥ 45 %, **G18** ist der eigene Fehler als Mutation); (4)** eine feste Wartezeit schloss die Kette an der falschen Stelle; **(5)** das **Gegenlauf-Rig selbst**: es
zählte den Exit-Code statt der Station **und** startete die mutierte Datei statt der Probe, also waren vier
der sechs Mutationen **nie gelaufen** und die erste „6/6“ eine Behauptung — jetzt prüft es die erwartete
Station in der JSON (**6 von 6**, jede mit benannter roter Station). **Ein Gegenlauf blieb grün** (G17) und wurde zum Anlass, den Ausgangszustand messbar zu machen — dieselbe Lehre wie G11 am Vortag. **P9-112 widerrufen**, P9-113/114/115 abgelöst (die Zuordnung steht vollständig in der Matrix), **datierte Korrektur:** die im Vortagesblock notierten 1246 `pytest`-Tests sind **1241** gemessen (`pytest --collect-only`). Die **beiden Softcap-Überschreitungen wachsen** weiter und sind **benannt statt versteckt**: settings-Mini-Plan **61.237 B**, Abnahmematrix **92.601 B** — „kürzen notieren“ ist angeordnet, das Kürzen selbst bleibt Nikinger-Entscheidung.

**[2026-10-05, die zweite Bildsichtung ist gebaut — vier Punkte, und der Auftrag hat zwei Locks vom
Vortag widerrufen — opencode/M3, ein Commit, reines Frontend, kein Deploy, kein Service-Touch.]**
Der Nikinger hat die vier Bilder aus `screenshots_latest/` angesehen und vier Punkte notiert
(Mini-Plan §11, Locks **P9-AU–P9-AZ**, Abnahme **P9-103–P9-111** mit **9 ✅**). **Der Kern des
Blocks ist eine Umkehr:** *„since they are buttons and not fields to type something in"* — damit
ist **P9-AN widerrufen** (die Menüpunkte trugen die Fläche des **Eingabefeldes**), und die
ausgewählte Fläche aus **P9-AO** auch. Die unausgewählten Punkte tragen jetzt die
**Standardknopf-Fläche** (`--btn-std-fill`), der ausgewählte die **Akzentfläche** wie ein
Hauptknopf — **seine ausdrückliche Entscheidung aus der Rückfrage**, gegen die Alternative
„Standard + Rail-Akzent". Weitere Punkte: **8 px Abstand** zwischen den Menüpunkten (gemessen
vorher **0 px** — „glued to each other"), **„Ändern" rot** wie „Archivieren" (Vorsicht: teuer
rückgängig zu machen) und **„Schließen"** statt „Abbrechen", Beschriftung der Space-Zeilen bündig
mit dem Panel-Titel (vorher **33 px**), Namensfeld im Detail **beidseitig bündig** (vorher 12 px zu
schmal, als **Rasterfolge** gebaut und **nicht** als Breite), Anlegezeile **eine Zeile** (vorher
80 px Versatz). **Ein Gegenlauf fand eine Messlücke statt eines Defekts:** G11 blieb grün, weil ein
**geschrumpfter** Knopf dieselben Kanten hält, obwohl der Lock wörtlich „Space anlegen in seiner
Größe gleich lassen" verlangt — die Station misst jetzt die Eigenbreite an einer Kopie. **Sechs
Wächter umgeschrieben, keiner gelöscht**, jeder mit beiden Lesarten und Datum; **zwei eigene
Fehler** dieses Blocks, beide „die erste Regel ist nicht die, die ich meine" (ein Wächter riss
`rgba(255,255,255,.06)` an jedem Komma auseinander, ein Helper nahm die Übergangs-Sammelregel
statt der Flächenregel). **Zwei Softcap-Überschreitungen neu benannt statt versteckt:**
Abnahmematrix **84.161 B**, settings-Mini-Plan **49.655 B** — **der Plan ist erst durch diesen
Block über den Cap gekommen**, und ein Kürzen in ein L3-Archiv wäre **Nikinger-Entscheidung**,
deshalb gemeldet statt getan. `pytest` **1238 → 1246**, Probe **29/29**, **Gegenläufe G7–G12 6 von
6**, `ui_budget` 5/5, Tabu-Diff §0.3 leer. **Bilder:** `screenshots_latest/` auf **acht**
Symlinks rotiert (seine Anordnung: „give me all 8"), README mit Kriterium je Bild — **offen bleibt
der eine Punkt, den die Bilder nicht tragen können**: die Mitgliederliste, im Harness ohne Mitglieder
also aus dem Browser-Standard abgeleitet statt gemessen. **Danach Sichtprüfung am selben Tag (Nachtrag, Phase-9-Head):** **02 · 03 · 05 · 06 freigegeben**
(„looks fine now" ×2, „great", „yes"), **01 · 04 · 07 · 08 mit vier neuen Punkten** — als
**P9-BA–P9-BD** (Abnahme **P9-112–P9-115**) in §12 des settings-Plans **nicht gebaut, aber mit
allen Messwerten notiert**: alle drei Menüpunkte messen **131 × 35,69 px** bei Beschriftungen von
**106 / 113 / 77 px**, die Space-Zeilen haben **184–239 px** Leerraum rechts bei bereits bündigem
Text; **in Bild 04 sind die „Hinzufügen"-Optionen im eingecheckten PNG nachgewiesen**
(Fläche y 207..231) — sie stehen nur **oben**, weil der Mitgliederbereich im Harness leer ist,
und mein Kriterium sagte dir nicht, wo suchen; **Bild 07 zeigt die neue Zeile gar nicht**, weil
das Spaces-Panel **scrollt** (1417 px Inhalt bei 834 px Höhe) und ein neu angehängter Eintrag
unterhalb des Sichtbereichs landet — **die Ursache war nicht die Bündigkeit**. Aus **Bild 01**
bleibt **ein Wort von ihm offen**: „bigger" heißt Leerraum, „decrease its height" passt nicht dazu
(alle drei Höhen gleich). **„kürzen notieren" angeordnet** und im §Backlog mit Kandidaten
notiert. **Offen, in dieser Reihenfolge:**
Block „Kästchen enger" (P9-112–P9-115, **eine Klärung offen**) · Deploy `v3.1.3` ·
P9-94/P9-11-Portscan · P9-13/V150 (wandert nach P10, kein Blocker) · Softcap-Kürzung (angeordnet,
nicht ausgeführt) · V162 *(Lesart A)* · Gate/Z-Rest (Übersichtsgrafik, ROADMAP-Zeile, Phase auf ✅).

**[2026-10-05, V188 ist beantwortet — die Seite **kann** das Beenden des macOS-Vollbilds per ESC
nicht verhindern, und auf dem MacBook existiert der einzige Hebel dafür gar nicht; dazu der letzte
`KNOWN_OFFENDERS`-Eintrag und drei datierte Korrekturen am Doku-Drift aus dem settings-Closeout —
ein Commit, reine Doku, kein Code, kein Deploy, kein Service-Touch.]** Die beiden Sichtprüfungs-
und Deploy-Schritte bleiben Nikinger-Arbeit; die zwei Punkte, die M3 machen konnte, sind erledigt.
**V188 ✅ mit vier Quellen** (drei nachgelesen, eine am Repo gemessen) ⇒ **P9-27 ⬜ → ⚠️, D1
geschlossen, kein Code gebaut** — genau die Entscheidung, die das Plan-§4 unter dieser Bedingung
zugelassen hat. Die Kette: `app.js:259` ist der **einzige** `fullscreen`-Bezug der ganzen App, die
Web-Fullscreen-API greift im nativen macOS-Vollbild nicht ⇒ **das Vorhandensein eines immer
wirkenden Ausgangs ist Pflicht** (WHATWG Fullscreen §8, Anti-Spoofing) · WICG Keyboard Lock §7
**darf** ihn nicht abschalten, auch nicht bei *allen* angeforderten Tasten, und verschiebt nur
(„langer ESC" > 2 s) · §4.2 gilt nur für JS-initiiertes Vollbild · und MDNs `browser-compat-data`
sagt `Keyboard.lock` → **`safari: false`**. Das Plan-Wort „*meines Wissens* nur in Chromium" ist
damit **gemessen statt geglaubt**, und für den Anwendungsfall schärfer als die Frage. **P9-28
bleibt ✅** — der Guard ist für das *Web*-Vollbild richtig, das ist eine andere Frage.
**Drei falsche Sätze korrigiert, alle aus dem settings-Closeout §6.1:** (1) die Matrix behauptete im
datierten „Reihenfolge"-Block, der Deploy `v3.1.1` schließe **P9-15**, weil `health_gate.sh` die
`/api/v1/overview`-Läufe mache — **ein Health-Gate liefert Läufe ohne Kriterium**, denn P9-15 stellt
gegen 372,9 ms und der Wert ist nie über Funnel gemessen worden (V151); (2) zwei Ebenen darunter
sagte derselbe Absatz, P9-15 sei „Arbeit des Deploy-Tags" — die Zeile ist **seit dem 2026-10-03
gemessen** (⚠️), und Modulstatus und Wurzel trugen denselben Fehler; (3) „seit dem 2026-10-04 ist
kein ⬜ ein Personenschritt" war mit **P9-94 falsch geworden** — zwei der drei ⬜ brauchen ein
MacBook mit Hotspot, und der Satz davor war im Repo **ungrammatisch** (angebrochener Halbsatz).
**Der letzte `KNOWN_OFFENDERS`-Eintrag ist gestrichen:** `docs/screenshots/README.md` trug **beide**
Ausprägungen zugleich (Feld **fehlt ganz** + zwei von sechs Fäden mit `updated: `-Präfix, für das
der Rotationsanker blind ist); repariert in zwei Schritten, weil `prepend_updated_chain.sh` ein
vorhandenes `^updated: ` **verlangt** — die sechs Fadeninhalte **byteweise** gegengeprüft.
**Zwei Zeilen** in `test_acceptance_numbers.py` (Bilanz-Konstanten, **vor** dem Schreiben gesetzt,
sonst wäre der Wächter eine Tautologie), **eine Zeile entfernt** in `test_updated_chain.py`. Kein
Test hinzugefügt, keiner umgedreht, Tabu-Diff §0.3 leer, Release `v3.1.3` unverändert.
**Offen, in dieser Reihenfolge:** Sichtprüfung der acht Bilder (entscheidet P9-97/P9-99) · Deploy
`v3.1.3` · P9-94/P9-11-Portscan · P9-13/V150 (wandert nach P10, kein Blocker) · V162 *(Lesart A)* ·
Gate/Z-Rest (Übersichtsgrafik, ROADMAP-Zeile, Phase auf ✅).

**[2026-10-05, die sieben Punkte aus der Bildsichtung sind gebaut — und zwei davon haben die Vorgabe
selbst widerlegt — ein Commit, reines Frontend, kein Deploy, kein Service-Touch.]** Der Nikinger hat
am selben Tag die Probe-Bilder des settings-Blocks angesehen und sieben Punkte notiert (Mini-Plan §10,
Locks P9-AM–P9-AS, Abnahme P9-96–P9-102). **Alle sieben sind umgesetzt**, Release `v3.1.3` steht
**unverändert** und ist **nicht deployt**. Die erste Browser-Probe hat **zweimal nicht den Bau,
sondern die Vorgabe** widerlegt: **`text-align: center` ist auf dem Menüknopf ein No-op** — er ist
`display: flex` mit einem anonymen Flex-Item, und `text-align` wirkt auf Blockcontainer (gemessen:
Textmitte **8,5 px neben** der Knopfmitte); gebaut ist `justify-content: center`, die Flex-Achse
(**0 px**). Und **„Text mittig" ist mit „Polster = Baumzeile" nicht gleichzeitig erreichbar** — als
`.tree__folder` erbte der Menüpunkt die 32-px-Einrückung und lag 12 px neben seiner Mitte;
**Nikinger-Entscheidung: beidseitig `--space`**, Preis benannt am Stylesheet, in S1 und in der
Matrix (P9-97 ⚠️). Bilanz: **P9-96/98/100/101/102 ✅, P9-99 ⚠️** (anderer Weg, gleiche Wirkung) —
**beide ⚠️ sind benannte Abweichungen, keine offenen Punkte**. `pytest` 1233 → 1238, `ui_budget` 5/5
(165,6 KB), Tabu-Diff leer, Probe **56/56**, G4 → 2 rot · G5 → 2 rot · G6 → 3 rot — und **die
Plan-Aussage zu G6 war falsch benannt** (eine eigene Höhe trifft P9-84, nicht P9-97).
**Ein Produktbefund gemeldet, nicht gebaut:** die Space-Liste bleibt **leer**, wenn man sie vor
`loadOverview()` öffnet (Wahrscheinlichkeit wächst linear mit den sichtbaren Spaces, P9-15) —
wandert in die **P10-Liste**. **Fünf eigene Fehler, alle derselben Klasse** (Wächter oder Messung
scheitert am Muster und sieht wie ein Befund aus) plus **zwölf eingebaute Verstöße** im neuen
Wächtertest, damit „erlaubt" nicht zu „alles erlaubt" wird. **Offen, in dieser Reihenfolge:**
Sichtprüfung der acht Bilder (sie entscheidet die beiden ⚠️) · Deploy `v3.1.3` · P9-94-Portscan ·
V188 · P9-15 ⬜.

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

**[2026-10-04, datierte Namenskorrektur]** Der Ausdruck „P9-A-Umkehr" im Block vom 2026-10-03 und in
mehreren `updated:`-Fäden war ein **Fehlname**: **P9-A** ist im Plan der **Scope-Lock** „P9 ist eine
Härtungsphase" (§1) und ist durch eine Wurzel-Rotation **nicht berührt**. Der Fehlname entstand am
2026-10-03 und überlebte zwei Sessions, weil beide ihn abgeschrieben statt nachgeschlagen haben:
`grep P9-A` im Plan findet vier Stellen, und keine handelt von Blöcken in der Wurzel.

**[2026-10-04, die Wurzel-Rotation ist auf K=1 umgekehrt und die drei Doku-Strukturen sind rotiert — der letzte offene
Hebel gegen die Softcap-Überschreitungen war eine Tabelle, kein Block — opencode/M3 — zwei Commits,
kein Produktcode-Touch, kein Deploy.]** **Umgekehrt:** die Wurzel trug **24** Session-Blöcke in
`## Current state` (**91.123 B** von 114.771 B) und steht jetzt bei **einem** — die älteren 23
wandern **verbatim** nach `docs/PROJECT_SESSION_LOG.md` (L3), wohin die Wurzel seit 2026-09-08
selbst zeigt. **Das ist **keine** Umkehr von P9-A: P9-A ist der Scope-Lock „P9 ist eine
Härtungsphase" (Plan §1) und bleibt unberührt — der Fehlname „P9-A-Umkehr" ist unten datiert
korrigiert. Umgekehrt wurde die **Rotationsregel der Wurzel-`CLAUDE.md` auf K=1** —
Nikinger-Entscheidung 2026-10-04, eine Entscheidung der Doc-Layers-Konvention und **kein Lock**,
und sie steht deshalb hier und nicht im Plan. Die
Byte-Buchhaltung geht **auf das Byte auf**: 216.221 B in beiden Dateien vorher, 216.221 B nachher.

**Und die Antwort, die dabei herauskam, ist die, die zwei Sessions offen geblieben war: es sind
nicht die Blöcke.** Der Phase-9-Head stand bei **56.860 B = 15.900 B über** dem 40-KiB-Softcap;
nach Session-Block-Rotation (17.780 B verbatim) **und** `updated:`-Kettenrotation (6 von 7 Fäden)
blieben **49.033 B** — und **rund 14 KB über**, weil die **§-Modulstatus-Tabelle allein 30.564 B in
14 Zeilen** trug, davon **15.041 B in drei Zeilen** (Gate/Z 6.075 · A 4.915 · B 4.050). **K=1 ist die
Konvention, und selbst K=1 passt nicht**, weil nicht die *Anzahl* der Blöcke das Problem ist,
sondern die Breite einer Tabelle. Die ausführlichen Statusspalten stehen jetzt **verbatim** in
`phase9_hardening/MODULE_STATUS_ARCHIVE.md` (L3, eine Sektion je Step), im Head steht je Step ein
Kurzstand mit Marker, Zustand, Offenem und Zeiger — **der Phase-9-Head liegt damit zum ersten Mal
unter dem Softcap.** Derselbe Weg, am 2026-10-02 an zwei anderen Stellen erprobt
(`phase1_storage/CONTRACTS_ARCHIVE.md`, `phase5_ui/ABNAHME_MATRIX_ARCHIVE.md`).

**Drei Doku-Befunde, die dabei auffielen, und alle drei waren live schlechter, als es aussah.**
(1) **Zwei von dreizehn Statuszellen waren unsichtbarer Text:** ein rohes ` | ` im Text der
Statusspalte gibt GFM **vier** statt drei Zellen und legt den Rest in eine **Phantom-Spalte** —
**4.097 B**, darunter der komplette V153-Block des Step B. In einer Textausgabe sieht eine Tabelle
mit mehr Zellen als ihr Kopf nicht kaputt aus, sie sieht nach einer Spalte aus. (2) Der Zahlen-Wächter
`test_acceptance_numbers.py` **verwarf den Marker der zweiten `[VERIFY]`-Lesart** — V162 *(Lesart B)*
konnte von ⬜ auf ⚠️ wechseln, ohne dass ein Wächter es bemerkte, weil die Zählregel „eine doppelt
vergebene Nummer zählt einmal, mit Lesart A" die zweite Zeile wegwirft und sie damit in **keiner**
Bilanz sichtbar war. (3) `prepend_updated_chain.sh` fand **drei verklebte Fäden** in
`SESSIONS_ARCHIVE.md` und **einen** in `ABNAHME_MATRIX.md`, beide Dateien in dieser Phase — Fäden, die
für den Rotations-Anker nicht existieren. Das ist die **dritte Ausprägung derselben Fehlerklasse in
dieser Phase** (nach dem ` · `-Trenner und dem fehlenden `updated:`-Feld) und dieselbe Lehre:
**eine maschinell gepflegte Struktur braucht einen Wächter, nicht Aufmerksamkeit** — und einen
*passenden* Wächter: der erste Wächter, der ich schrieb, meldete **grün**, als ich genau den Defekt
reproduzierte, den er verhindern sollte, weil er die Daten an der falschen Stelle las.

**V162 *(Lesart B)* von ⬜ auf ⚠️, mit Zitat und mit der Grenze des Zitats:** die Tailscale-Doku sagt
wörtlich *„access control rules apply to Serve just like any other service"* (validiert 20.01.2026);
für `--tcp`/`--tls-terminated-tcp` nennt die CLI-Referenz **kein** ACL-Verhalten in **keine**
Richtung. Ein Gegenlauf braucht eine *abgelehnte* Verbindung von einem zweiten Tailnet-Knoten — auf
der Heim-VM kann ich auf keinem fremden Knoten Kommandos ausführen. **Die `socat`-Wahl ist damit
nicht widerlegt, sondern gedeckt:** die elegante Alternative ist nur für den HTTP-Modus belegt, und
eine offene Frage soll keine Firewall-Entscheidung tragen.

**Stand der Phase 9:** `v3.1.1` ist **live** (Release `20261003T205843`, Health-Gate **9/9**), ohne
Index-Neuaufbau. Abnahme **71 ✅ · 10 ⚠️ · 2 ⬜** · `[VERIFY]` **31 ✅ · 3 ⚠️ · 1 ⬜** — beide Zahlen
stehen in `phase9_hardening/ABNAHME_MATRIX.md` und **nur** dort, weil die zweite Kopie erfahrungsgemäß
die veraltete ist (vier Fundstellen, drei Zahlen, zwei Tage lang). **Kein ⬜ ist offene
Code-Arbeit.** Und seit dem **2026-10-04** ist **kein offener Rest ein Personenschritt**: die beiden
Benennungen sind entschieden und gebaut (beide Heads unter dem Softcap), und **P9-13/V150 — das zweite
Claude-Konto — sind zurückgestellt und wandern nach P10**, weil ein Schritt, den nur ein Konto braucht,
kein Blocker ist, sondern ein Termin (Regel in §Working style, Plan §0.1a). **Was bleibt, ist eine
Aufgabe: P9-15** — drei Läufe `/api/v1/overview` mit echter UI-Session, **Arbeit der nächsten
Session**; ein Cookie-Jar mit echten Zugangsdaten gehört nicht in eine Datei (Hard Rule 1), der Weg
dafür steht im Nachtrag des Phase-9-Heads. Danach Übersichtsgrafik §12.4
**gerendert und angesehen**, ROADMAP-Zeile, Phase auf ✅. **Fester Termin: am 2026-10-18 schließt
das Übergangsfenster von selbst** — die alte Funnel-Adresse liest dann nur noch, schreibt nicht
mehr. Absicht, kein Versehen.

**Details, Herleitungen, Gegenproben und die dreizehn eigenen Fehler dieses Tages: der
`## Session stopped`-Block vom 2026-10-04 in `phase9_hardening/CLAUDE.md`.** Was hier nicht steht,
steht dort; umgekehrt gilt: **was hier steht, ist der Stand, und es ist eine Zusammenfassung.**

*Neue Session-Blöcke wachsen **oben** in dieser Sektion; die älteren rotieren **verbatim** nach
`docs/PROJECT_SESSION_LOG.md` — per `scripts/rotate_root_current_state.sh` (K=1, sechs Gegenproben,
u. a. byteweise Reassemblierung und Nachlesen jedes Blocks), **nie von Hand**. Die vollständige
Chronik der Phasen 1–8, der Hard-Rule-Korrekturen und der älteren Blöcke: `docs/PROJECT_SESSION_LOG.md` (L3).*

**[2026-09-10, P8.6 Block A ✅ — Fundament:** Radiogruppe→`<select>`, sechs neue Tokens (`--bg-void`/`--select-fill`/`--select-line`/`--caution` u. a.), `--border-soft`→`var(--line)`, Konvention v3 um „Vorsicht". Erste echte Code-Touch-Session der Phase. Tabu-Diff §0.3 leer, `pytest` 964→966, `ui_budget.py` 5/5. Nikinger hat die P8.5-19-Radiogruppe am 2026-09-08 selbst zurückgenommen. +2 statische Tests (P8.5-Test ersetzt, `test_no_raw_accent_rgba_outside_root`, `test_every_css_var_reference_is_defined` — hätte `--border-soft`-Bug gefunden). **Abweichung von Plan §3.5/§8.2 dokumentiert:** die anderen 4 Tests gehören zu Block B/C.

_Vollständige Chronik der älteren Einträge (Phase 8, Phase 8.5-Vorlauf, Phase 7/6.5/6-Abschluss,
Phase-5/4/3/2/1-Zusammenfassungen, Hard-Rule-Korrekturen): `docs/PROJECT_SESSION_LOG.md` (L3).
Neue Session-Blöcke wachsen oben in dieser Current-state-Sektion; ältere Blöcke rotieren
verbatim nach `PROJECT_SESSION_LOG.md`. **[2026-09-13]** Eine Ein-Block-Regel wurde erwogen und
**verworfen**: gemessen steckten 69 % der Dateigröße in der `updated:`-Frontmatter-Kette
(28.090 B über 30 Einträge, davon 3.290 B glatte Duplikate), nicht in dieser Sektion
(3.376 B). Die Kette ist verbatim nach `PROJECT_SESSION_LOG.md` §Frontmatter-Archiv rotiert —
dieselbe Lösungsrichtung, die für `docs/INDEX.md` vorgemerkt ist._



**[2026-09-10, P8.6 Block D ✅ [D1/D2/D4]** — Reiner `graph.js`-Commit (8,4 KB, +0,5 KB). D1 V102-Dedup (`dedupeEdges()` ungeordnetes Knotenpaar, P8.6-N, keine neunte P1-Contract-Öffnung), D2 FNV-1a-Layout-Seed (`seedJitter(id, salt)`, P8.6-M, „Karte fliegt" behoben), D4 `cancelAnimationFrame` in `runSimulation()` (P8.6-§6.4, **einzige Scope-Erweiterung**, streichbar). D3 🟡 wartet auf Block C. `pytest` 966 unverändert, `ui_budget` 5/5, Tabu-Diff §0.3 leer, Service-Touch 0. Items #2/3/4 aus dem Handover blockiert (Ollama-Migration steht bevor).

**[2026-09-10, P8.6 Step V ✅ — Ollama + `qwen3-vl:8b` + V119-Smoke 46 s, Modellname-Korrektur + Plugin-Pfad für nächste Session.** Proxmox-Migration ✅ durch (i5-14600KF, sharefyx-mcp PID 991 nach Auto-Restart), Nikinger hat Ollama 0.34.0 via offizielles `curl | sh`-Script installiert (apt-Paket existiert auf Ubuntu 24.04 nicht — Korrektur in §Vormerkungen), `qwen3-vl:8b` (Q4_K_M, 6,1 GB) gepullt + V119-Smoke ✅ in 46 s gegen `c4_p8519_01_radiogruppe_im_dialog.png` (qwen3-vl:8b Cold-Start inkl. Vision-Encoder; deutsche Antwort korrekt: „Der Radio-Button ‚als Text-Link im Text' ist markiert"). `requests 2.34.2` ins Projekt-venv installiert; `phase8_6_ui_polish/scripts/vision_ollama.py` (89 Z., `requests.post(/api/generate)`, 600s-Timeout). **Modellname-Korrektur:** `internvl2.5:8b` (ursprüngliche Empfehlung) existiert nicht auf Ollama-Library — Recherche-Fehler von mir korrigiert auf `qwen3-vl:8b`. Phase-Head §Vormerkungen + Aktionsliste + Vision-Backend-Sektion entsprechend korrigiert. `pytest` V107 ✅ **966 unverändert**, `ui_budget` V97 ✅ 5/5, Tabu-Diff §0.3 leer, Service-Touch 0. **Push + Deploy** für Block A + D-Commits (`32fddba`, `04dee6a`) vom Nikinger in dieser Session autorisiert + ausgeführt (`10f9f63..04dee6a`). **Nächster Schritt** (Nikinger-Vorgabe 2026-09-10): **Schritt 1 = `DavidEasden/opencode-vision`-Plugin installieren** (vor jeder Sichtprüfung, damit Screenshots direkt im Chat gerendert werden — `docs/concepts/sichtpruefung_automation_conventions.md` §4), **Schritt 2 = visuelle Verifikation Block A + D** am echten Gerät gegen die neuen Screenshots (post-Block-A: `<select>`-Markup, post-Block-D: Zwillingskante weg + Karte stabil); Schritt 3 = Block B nach Plan §4; Schritt 4 = Block C nach Plan §5 + D3-Nachzug.

**[2026-09-12, P8.6 Block C ✅ — Struktur-Umbau: Einstellungen oben, Alle Items unten, Karte rechts voller Hoehe, klickbare Spaces, Ordner-Zaehler.** Erst opencode/M3-Code-Touch seit Block B am 2026-09-11. **C1** `#account-button` raus aus `.rail__account` direkt unter `#home-button` + Label „Konto"→„Einstellungen" (N3-Lesart b, das `#i-settings`-Icon war schon immer ein Zahnrad). **C2** `tree.js :: renderRail()` ruft `renderScopeRow()` jetzt HINTER die Spaces + neue `tree__group`-Überschrift „Alles"; bestehende Kommentar zu „Lieber keine Zahl als eine unwahre" bleibt wörtlich erhalten (er ist die Antwort auf C5). **C3** `.overview` wird zweispaltiges Grid (`grid-template-columns: 1fr 40%` ab ≥1281px, Wrapper-DIVs `head-row`/`col-left`/`col-right`, `.overview__graph` ohne `max-width`/`min-height` [V112-Gegenprobe], `@media (max-width: 1280px)` kollabiert auf eine Spalte — Map rutscht unter die Liste); `requestAnimationFrame(resize)` in `loadGraph()` [V115] damit `seedInitialPositions()` nach dem nächsten Layout-Pass die endgültige Kartengröße hat. **C4** `.overview__space-open` als innerer `<button>` mit B1-hover + V116 `activateView`-Export (semantisch „in den Space wechseln ohne Bucket zu setzen") + `closeEditor().then(proceed => ...)`-Gating (dieselbe Disziplin wie Ordner-Buttons). **C5** `state.itemsLoaded`-Flag + `folderItemCount()`-Helfer + neuer V117-Reset in `activateView`/`navigateAll` (sonst zeigt das Rail für ein paar ms Counts aus dem falschen Pool); `.tree__count` bekommt `margin-left: auto` (gilt für Eimer + echte Ordner). **Drei Befunde/Abweichungen während Baus dokumentiert:** `activateView` doppelt definiert (Original-`function` plus neuer `export function`) → `PAGE ERROR: already declared` → `overview__spaces` blieb leer → Original entfernt; V117-Reset in beiden Navigation-Funktionen eingebaut; `requestAnimationFrame(resize)` als V115-Fix. **`pytest` 970 V107 ✅ (+3 statische Tests `test_rail_order_settings_before_tree_logout_last`/`test_account_button_says_einstellungen`/`test_overview_graph_has_no_max_width_or_min_height`), `ui_budget` V97 ✅ 5/5 (137,5 KB, +4,4 KB durch C1/C3/C4-CSS)**, Tabu-Diff §0.3 leer, Service-Touch 0 — sharefyx-mcp **PID 991** durchgehend unverändert. **Sechs Selbst-Screenshots** in `docs/screenshots/p86_block_c_{01..06}_*.png` zeigen alle fünf Sub-Ziele (Rail-Reihenfolge, „Alle Items" am Rail-Ende, Karte als rechte Spalte, klickbare Space-Zeile, Folder-Zähler) + B4-Vorsicht-Regression. Eigenes Self-Skript `phase8_6_ui_polish/scripts/p86_block_c_self_check.py` (~250 Z., Playwright + Login mit TOTP-Window-Retry + 6 Screenshots); Wegwerf-Setup reproduziert den v3ritt-Datenstand auf Port 18773, gestoppt über PID-Datei (Hard Rule 9-konform, kein `pkill -f`; `login_attempts`-Rate-Limit durch `cleanup`+`setup`+`seed-items`+`start` zurückgesetzt — das war nötig, nachdem drei fehlgeschlagene Login-Attempts die Bremse ausgelöst hatten). **Push + Deploy** für Block C wartet noch auf Dich (Drei-Bedingungen-Regel zu zwei Dritteln erfüllt — Code-Tests grün ✓, Bilder grün ✓, Nikinger-Sichtung ⬜).

**[2026-09-13, P8.6 Partial Closeout — die Phase ist NICHT abgeschlossen und NICHT ausgeliefert.** Reine Doku-Session. **Klarstellung zum Stand:** `origin/main` steht auf `2a93e67`, lokal liegen **zwei** ungepushte Commits (`90c72e2` Block C, `bc2aa9f` Partial Closeout) — die Behauptung „7 Commits voraus" aus dem 2026-09-12-Block war falsch, per `git fetch` geprüft. Badge steht auf `v3.0.1`, Gate ⬜ **angehalten**, Step Z ⬜. **Neu:** `docs/concepts/PHASE8_6_CLOSEOUT_HANDOVER.md` (Teil-Stand, Delta, §4 ordnet die neun UX-Befunde den Locks zu, die sie öffnen — **P8.6-O2** `.shell`-Grid für Befund 5, **C1/N3-Lesart b** für Befund 7, **P8.6-E** für Befund 1+8, plus die Versionsfrage **P8.6-R**; §5 `[VERIFY]`-Bilanz 14 zu / 5 offen) + `docs/concepts/phase8_6_ui_polish_uebersicht.svg` (1080×1080, gerendert und visuell gegengeprüft, Badge **PARTIAL CLOSEOUT**). Beide existieren per **ausdrücklicher Nikinger-Anordnung vom 2026-09-13** — die in **P8.6-B** vorgesehene Ausnahme; **Plan §9 bleibt bewusst leer**, weil §9 der kanonische Abschluss ist und die Phase nicht abgeschlossen ist. **Rotation:** der Head verletzte **P8.6-T** (ein `## Session stopped` **plus** ein zweiter Session-Block als `###` — das Muster, bei dem `rotate_session_block.sh` fälschlich „bereits konform" meldet); `###` aufs `## Session stopped — <Datum>`-Schema gebracht, dann das Skript gelaufen: alle vier Gegenproben grün, Head **72.958 → 59.797 B**. **Archiv-Reparatur:** der Block-D-Sub-Block war seit der Hand-Rotation vom 2026-09-10 **mitten im Satz abgeschnitten** — **72 Zeilen / 4.403 B** fehlten; mechanisch aus `04dee6a:phase8_6_ui_polish/CLAUDE.md` wiederhergestellt, `cmp` byte-identisch, Altbestand nachweislich unverändert. **Drei weitere Drifts behoben:** Modul-Status Zeile 5 (Block C) stand auf ⬜, obwohl Commit `90c72e2` ihren Nachzug behauptet — Hard-Rule-8-Miss; `docs/INDEX.md` verletzte **P8.6-4** (40.870 B gegen ≤ 38 KB) → sechs Zeilen geschlossener Phasen gestrafft, zwei neue Zeilen aufgenommen, jetzt **38.822 B**, Kriterium erstmals seit Block A erfüllt; der Frontmatter-Closer `---` des INDEX klebte am Ende der `updated:`-Zeile statt auf einer eigenen — Frontmatter war formal kaputt. **`pytest` 970 passed in 116 s ✅** (V107-Baseline 964), Tabu-Diff §0.3 leer, Service-Touch 0 — sharefyx-mcp **PID 991** nur gelesen. **Nächster Schritt: Claude-Code-Planungssession für P8.6 Plan 2.** Empfohlene Reihenfolge (im Handover begründet): Befund 9 zuerst, weil er als einziger **auf der Produktion** reproduziert ist und damit nicht am P8.6-Deploy hängt — und zwar messen (CDP-Probe bei 1024/1200/1440), bevor repariert wird.  **Nikinger-Entscheidungen vom 2026-09-13:** **(a)** Deploy-Ziel bleibt **`v3.0.2`** — P8.6-R ist damit bestätigt, nicht überstimmt. **(b)** **Block C geht einzeln raus**, nicht in einem Sammel-Push nach Plan 2. **(c)** Die Ein-Block-Regel für die Current-state-Sektion hat er mir überlassen — **ich rate ab und habe sie verworfen**: sie hätte 3,4 KB gebracht und beim nächsten Session-Block wieder gerissen, weil **69 % der Datei in der `updated:`-Kette** steckten (28.090 B über 30 Einträge, davon 3.290 B glatte Duplikate) und nur 3.376 B in dieser Sektion. Die Kette ist stattdessen verbatim nach `PROJECT_SESSION_LOG.md` §Frontmatter-Archiv rotiert: **47.094 → 23.007 B**, alle fünf Session-Blöcke bleiben erhalten. **(d)** **Push ja, Deploy nein** (Nikinger, 2026-09-13, nachdem die Tatsachenlage aus §4.6 vorlag): die Commits gehen nach `origin/main`, **ausgeliefert wird nicht**. Live bleibt damit `6f19a8f` (P8.5). Ein Push ändert nichts an der Produktion — die drei von Block C neu eingeführten Befunde 3/4/6 erreichen keinen Nutzer, bis Plan 2 sie abgearbeitet hat. **Siebter Drift, in dieser Runde gefunden und der folgenreichste: von Phase 8.6 ist NICHTS live.** Phase-Head und der Step-V-Block unten behaupten „Push + Deploy für Block A + D vom Nikinger ausgeführt (`10f9f63..04dee6a`), `health_gate.sh --expected-sha=04dee6a` 8/8 grün". Das Werkzeug ist dabei in Ordnung: `health_gate.sh` liest den Release-SHA aus `/opt/sharefyx/current` (Z. 134/160); die Gegenprobe am 2026-09-13 meldet 7 OK + 1 FEHLER — das „8/8" ist nie so gelaufen. Gemessen am Server: `/opt/sharefyx/current` → `releases/20260905T140325.378914Z`, `git rev-parse HEAD` dort = **`6f19a8f`** — das ist der **P8.5**-Release vom 2026-09-05. Gegenprobe über sechs Block-Marker (`bg-void`, `select-fill`, `dedupeEdges`, `seedJitter`, `account-nav`, `overview__col-right`): **0 Treffer live, alle im Repo.** Das jüngste Verzeichnis unter `/opt/sharefyx/releases/` ist ebenfalls das vom 2026-09-05, und `deploy.sh:107` legt pro Lauf ein neues an — es hat also **kein** P8.6-Deploy gegeben. **Konsequenz für Entscheidung (b):** ein Deploy, der „nur Block C" ausliefert, existiert nicht — `deploy.sh` liefert `main` aus, also A+B+C+D zusammen. Der Push ist davon unberührt und läuft wie entschieden einzeln. **ROADMAP und diese Datei bleiben auf 🔄** — der formale Phasenschluss wäre eine stille Abweichung, solange Gate und Step Z offen sind.

**[2026-09-13, P8.6 Plan 2 geschrieben — Claude-Code-Planungssession, kein Produktcode-Touch.]** Ergebnis: `docs/concepts/phase8_6_ui_polish_plan2.md` (~69 KB, 📕-Snapshot gegen `main`@`26a7cc9`) — ausfuehrungsreif fuer alle neun UX-Befunde, Bloecke **E/F/G/H/J**, Locks **P8.6-W–P8.6-AL**, Abnahme **P8.6-33–P8.6-54**, `[VERIFY]` **V123–V139**. Die Phase bleibt **🔄 und nicht ausgeliefert**; live ist weiter `6f19a8f` (P8.5). **Sechs Nikinger-Entscheidungen (N.7–N.12):** **(N.7)** `.shell` wird **`240px 480px 1fr`** — die bewusste, vorgelegte und entschiedene Ausloesung von **P8.6-O2** (Messung: Space-Zeilen brauchen ~433 px, 380 reichen nicht). **(N.8)** Editor **ersetzt** die Karte, **ESC bringt sie zurueck** — auch nach Klick auf einen Karten-Knoten; ist Abnahmekriterium, nicht Nebenwirkung. **(N.9)** Befund 7b kehrt **C1 / N3-Lesart b** um (Einstellungen + Abmelden wieder unten, **Abmelden bleibt aeusserster Knopf**) — datierte Umkehr einer beantworteten Frage, keine stille Abweichung. **(N.10)** Layering per **Tiefe statt Farbe**. **(N.11)** Plan 2 ist ein eigenes Dokument; Plan 1 bleibt 📕 unangetastet, der **kanonische Closeout wandert nach Plan 2 §9** (P8.6-W). **(N.12)** Der `pytest`-Flake wird beidseitig gefixt. **Fuenf der neun Befunde haben jetzt eine gemessene Ursache statt einer Vermutung:** Befund 8 — `--panel-meta-line: rgba(229,169,60,.22)` **ist** `--warn: #E5A93C` bei 22 %, byte-genau; Befund 1 — 10 Flaechen-Token in `:root` plus **4 rohe Hex ausserhalb** (`#0E1116`/`#131A23`/`#1A2029`, dazu `#fff` im QR, das bleibt); **Befund 2 ist als Messfrage geschlossen — die Knoepfe fehlen nicht**, `app.html:484-485` rendert beide (sichtbar in `p86_block_b_04_account_dialog.png`), sie lesen sich wegen `background: none; border: none` nur als Fliesstext; Befund 4 — `1fr 40%` meint 40 % des **Detail-Slots**, also 302 px bei 1440 = 21 % der Seite, nicht die in P8.6-K zitierten „~40 % der gesamten Seite"; Befund 6 — **Lock-Abweichung, keine CSS-Wanze**: P8.6-P forderte die ganze Zeile klickbar, C4 baute einen inneren Button. **Befund 9 zerfaellt in zwei:** **9a** laeuft live auf `v3.0.1`, wo Block C gar nicht existiert (Ursache **unbekannt**, Block E misst sie), **9b** ist von Block C eingefuehrt (`overflow: hidden` + `flex: 1` schlaegt `height: auto`). Die Falle, die Block E vermeidet: 9b reparieren und „behoben" melden, waehrend 9a live stehen bleibt. **Neuer Produktionsfehler, beim Messen der Baseline gefunden:** `pytest` ergibt **969 passed + 1 failed**, nicht die dokumentierten 970 — `secrets.token_urlsafe(16)` liefert in **1,569 %** der Faelle ein fuehrendes `-`, dann haelt `argparse` den Wert fuer eine Option und `authctl revoke --family-id <id>` bricht ab; das trifft auch einen echten Operator bei jeder 64. Familie. Behandlung in Block J auf ausdrueckliche Anordnung — und damit die **erste datierte Tabu-Ausnahme** der Phase (**P8.6-AJ**: `phase4_auth/authserver/crypto.py` + zwei Zeilen `store.py`). **`phase1_storage/storage/**` bleibt zu — keine neunte P1-Contract-Oeffnung.** **V110 als negativer Befund geschlossen:** `#home-button` ruft heute `navigateAll()` (`app.js:99-105`) — „Uebersicht" und „Alle Items" sind **dieselbe Aktion**; es gibt keinen Zwei-Zustands-Schalter, sondern zwei Knoepfe fuer **einen** Zustand. **Doku-Hygiene:** 109 `.md` gescannt — 0 kaputte Links, 0 fehlende Cards, 0 fehlende INDEX-Zeilen; „nichts zu tun" war das Ergebnis, mit **einer** Ausnahme: `docs/INDEX.md` hatte gegen das ≤-38-KB-Kriterium nur **97 B Luft**, sieben geschlossene Phasen-Zeilen gestrafft (−1.549 B) ⇒ **38.473 B, 439 B Luft**. Rotation **per Skript** (P8.6-T), alle vier Gegenproben gruen, Head 72.808 → 65.666 B. `ui_budget` 5/5 (137,5 KB), `/api/v1/overview` **372,9 ms** (bestaetigt V108 ein zweites Mal). Tabu-Diff trivial leer, **Service-Touch 0**. **Naechster Schritt: opencode/M3 beginnt bei Block E — messen, nicht bauen.**

**[2026-09-14, P8.6 Block F erledigt: Layering konsequent, zwei Wächter scharf ✅ — opencode/M3 — atomarer Block, kein Mess-Overhead.** `phase5_ui/webui/static/app.css` F1-F3: `--panel-meta/--panel-meta-head/--panel-meta-line` entkoppelt (Befund 8, P8.6-AB N.10 — meta jetzt Layer 2 kühl, nicht mehr warm-getönt mit `rgba(229,169,60,.22)`); drei neue Token `--rail-top/--auth-glow/--auth-card-top` für die rohen Flächen-Hex `#0E1116/#131A23/#1A2029` (P8.6-AD); `.editor__append` trug schon `var(--surface) + border-top: var(--line)` (F2 null B-Aufwand, V127: 0). `phase5_ui/tests/test_static_routes.py` F4: **zwei neue Wächter als byte-genaue Regressionssperre** — `test_no_raw_surface_hex_outside_root` (jede `background:`/`gradient(`-Deklaration außerhalb `:root` nutzt Token; EXEMPT_HEX dokumentiert `#fff` QR + 9 Space-Kategorie-Hex) + `test_meta_panel_is_not_tinted_with_the_warning_colour` (prüft gezielt die drei `--panel-meta*`-Tokens, lässt legitime Warn-Themed-Chips mit `var(--warn)` zu). `#fff` in `.qr-frame` mit begründendem Kommentar ("QR-Code braucht echtes Weiß"); 9 Space-Kategorie-Hex in `.rail__glyph--own/--shared/--foreign` bleiben per Plan §3.3 explizit ausgenommen. Zwei Selbst-Screenshots `p86_block_f_{01_vorher_warm_meta,02_nachher_cool_meta}.png` (Vorher per `git stash`-Revert für die Aufnahme, danach pop — der Revert berührte nur app.css lokal, ist im Commit nicht enthalten); Checkkriterium in einem Satz: "das Meta-Panel zeigt eine kühle Layer-2-Fläche (`--surface = #14181D`) statt der warmen `rgba(229,169,60,.22)`-Tönung -- Befund 8 weg". **Selbstprüfung:** `pytest` 970 → **972** in 111,52 s (Baseline 970 + 2 neue Wächter), `ui_budget` 5/5 (130,1 KB, app.css 60.201 → 60.319 B, +118 B), Tabu-Diff §0.3 trivial leer, kein `pkill -f`, kein `systemctl`, sharefyx-mcp PID 991 nur gelesen. **Doku-Hygiene:** Modul-Status Z11 ⬜→✅, Phase-Head-`updated:` mit F-Eintrag ergänzt, SESSIONS_ARCHIVE.md-`updated:` mit Rotations-Eintrag, ROADMAP-P8.6-Zeile + docs/INDEX.md Phase-8.6-Karten nachzuziehen. Rotation per `scripts/rotate_session_block.sh phase8_6_ui_polish`, E2b-Sub-Block (78 Z. / 5.058 B) verbatim ins Archiv, Head 67.798 → 68.956 B. **Naechster Schritt: Block G (Layout-Umbau, Befund 5 + 3/4/6/7a) — löst P8.6-O2 aus, .shell → 240px 480px 1fr, ESC bringt Karte zurück.** Reihenfolge P8.6-AH: F → G → H → J → Gate, jetzt mit F abgeschlossen.**

**[2026-09-14, P8.6 Block G erledigt: Layout-Umbau, fünf Befunde in einem Schritt behoben ✅ — opencode/M3 — atomarer Block, ein Commit.** `.shell` `240px 380px 1fr` → **`240px 480px 1fr`** per **P8.6-O2-Auslösung** (N.7 entschieden — gemessen brauchen Space-Zeilen ~433 px, 380 reichte nicht); DOM-Umzug `#list-overview` in `section.list` + `#detail-graph` (die Karte) in `section.detail` allein. **Befund 9b-Ursache weg:** `.overview`-Grid + 1280-px-Media-Query ersatzlos gelöscht. **V112-Wächter nach Umzug:** `.detail__graph { display: flex; flex-direction: column; flex: 1; min-height: 0; padding: ... }` + `.detail__graph .overview__graph { flex: 1; min-height: 0 }`. `state.overview: true` als neues Feld (P8.6-AA), `#home-button` setzt es **vor** `closeEditor()` (sonst rendert clearDetail mit altem Wert), mit Revert im else-Zweig (Cancel) und catch-Sicherheitsnetz. **Befund 6 behoben:** `.overview__space-open` ist jetzt der volle Zeilen-Button (width: 100%, padding statt LI), umschließt Glyph + Name + Chip-Counter-Chips als `<span role="button" tabindex="0">` (verschachtelte `<button>` wären ungültiges HTML). Hover-Regel wanderte vom LI auf den Button (P8.6-P wiederhergestellt). `renderListSlot()` neu exportiert (P8.6-AA); **alle Render-Aufrufer** (`loadItems`/`loadOverview`/`toggleSelected`/`clearSelection`/`clearDetail`/`loadEditorFromItem`/`selectItem`) umgestellt (V128 vollständig). **Editor ersetzt die Karte, ESC bringt sie zurück** (N.8) — visuell in Screenshots 03/04 bestätigt. **Vier neue statische Tests** in `test_static_routes.py` (G8): `test_shell_grid_is_240_480_1fr` (P8.6-X), `test_overview_lives_in_the_list_slot` (P8.6-Y), `test_detail_graph_has_a_definite_height_chain` (V112-Wächter nach Umzug), `test_overview_grid_and_its_media_query_are_gone` (9b-Regressionswächter); `test_overview_graph_has_no_max_width_or_min_height` an Compound-Selector angepasst (`^\.overview__graph\s*\{` mit `re.MULTILINE`, sonst hätte die neue `.detail__graph .overview__graph`-Regel ihn fälschlich gebrochen). **Echter Fund beim Self-Check (im selben Commit behoben):** `editor.js` rief `renderListSlot()` ohne Import → `[ERR] renderListSlot is not defined` in der Browser-Konsole, Editor öffnete sich nicht, erste Screenshot-Aufnahme zeigte es. Behoben durch Import-Ergänzung in editor.js Z. 9. **Sechs Selbst-Screenshots** `p86_block_g_{01..06}_*.png` (110-115 KB / 84 / 69 KB): 1440-Übersicht, 1440-Space-geöffnet, 1440-Editor-offen, 1440-Editor-nach-ESC, 1200-Übersicht, 1024-Übersicht. **Selbstprüfung §0.5:** `pytest` 970 → **976** in 107,04 s (Baseline 970 + 4 neue G-Tests + 2 F-Tests), `ui_budget` 5/5 im Korridor (**141 KB statt 130 KB** — Plan §4.9-Erwartung „app.css kleiner" **nicht erfüllt**, dokumentierte Abweichung: die `.detail__graph`-Höhenkette und ausführliche G7-Kommentare überwiegen den Grid-Lösch-Effekt), Tabu-Diff §0.3 trivial leer, kein `pkill -f`, kein `systemctl`, sharefyx-mcp PID 991 nur gelesen. **Doku-Hygiene:** Modul-Status Z12 ⬜→✅, Session-Block mit Block-G-Protokoll, Rotation per `scripts/rotate_session_block.sh phase8_6_ui_polish` (Block-F-Sub-Block 64 Z./4.382 B verbatim ins Archiv), docs/INDEX.md Phase-8.6-Karte nachgezogen, ROADMAP-P8.6-Zeile + Frontmatter nachgezogen, dieser Current-State-Absatz. **Nächster Schritt: Block H (Rail + Konto-Dialog, Befunde 7b + 2).** Plan §5: `.rail__account` trägt wieder Einstellungen **und** Abmelden (Abmelden bleibt äußerster Knopf — Umkehr von C1/N3-Lesart b, Nikinger-Entscheidung 2026-09-13 N.9). `.account-nav` bekommt eine Navigations-Anmutung (die zwei Knöpfe fehlten nie, sie sahen nur nach Fließtext aus — Befund 2 war eine Selbsttäuschung der CSS-Form, nicht eine Knopf-Lücke). `test_rail_order_settings_and_logout_at_the_end` wird umbenannt und umgekehrt. Reihenfolge-Empfehlung (P8.6-AH) bleibt F → G → H → J → Gate, jetzt mit G abgeschlossen.**

**[2026-09-14, P8.6 Block H erledigt: Rail + Konto-Dialog, zwei Befunde in einem Schritt behoben ✅ — opencode/M3 — atomarer Block, ein Commit.** `phase5_ui/webui/static/app.html:19-53` H1 P8.6-AE/N.9: DOM-Reihenfolge im `.rail` ist wieder `.rail__brand` → `#home-button` → `#rail-tree` → **`.rail__account` mit zwei Knöpfen** (`#account-button` zuerst, `#logout-button` zuletzt). Umkehr von Block C C1 (N3-Lesart b hatte `#account-button` oben unter `#home-button` gesetzt) — Nikinger-Vorgabe 2026-09-13: „Abmelden bleibt weiterhin der äußerste Knopf." Vorzeichen aus Block C erhalten: „Einstellungen" statt „Konto" (Zahnrad-Icon), `#logout-button` weiter mit `class="action--caution"` (B4-Farbe aus Konvention v3). `phase5_ui/webui/static/app.css:634-657` `.rail__account` ist jetzt `flex-direction: column` als **Normalfall**, nicht als Sonderregel in einer Media-Query — die Sonderregel `@media (max-width:1280px) {.rail__account {flex-direction: column}}` aus dem Plan §5.1 war bereits von Block G-R gelöscht (G-R.1 hat die 1280-px-Query ersatzlos entfernt); die Spalten-Anordnung ist damit der einzige Pfad in allen Breakpoints. `.rail__action--account`-Regel ersatzlos weg (V137 geklärt — sie war Rest der Oben-Platzierung mit `margin: 0 var(--space) var(--space); width: auto;`, nach der Rückkehr in `.rail__account` reicht die Basis-Regel `.rail__action`). `app.css:670-708` H2 Befund 2: `.account-nav` jetzt `display: flex; align-items: center; gap: var(--space)` (statt `display: block; text-align: left`) + `border-left: 2px solid var(--line-strong)` als sichtbare Akzentkante; B3-Hover (`background: var(--select-fill-quiet)` + `outline`) bleibt unverändert; `.account-nav .icon { margin-left: auto; }` schiebt das Chevron-Icon an den rechten Rand (gleiche Mechanik wie `.tree__count` aus Block C C5). `app.html:464-468` beide `.account-nav`-Buttons tragen jetzt `<svg class="icon"><use href="#i-chevron-right"></use></svg>` als letztes Kind (Symbol existierte schon, `tree.js:229` nutzt es für `tree__twist`, kein neuer Asset). **Kein** Rückfall in `.btn` (B3-Kategorie „Navigation" trägt — die Knöpfe öffnen etwas, ändern nichts; der fehlende Afford war das Problem, nicht die Kategorie). V133 erledigt: `elementFromPoint` liefert jetzt das Button-Element statt `null` (die Knöpfe fehlten nie — sie hatten keinen sichtbaren Afford). **Wächter:** `test_rail_order_settings_before_tree_logout_last` umbenannt + umgekehrt zu `test_rail_order_settings_and_logout_at_the_end` (P8.6-I-Mechanik, „der Testname wird sonst zur Lüge"), Assertions `#home-button < #rail-tree < #account-button < #logout-button` plus zusätzliche Assertion `#logout-button == html.rfind('id="logout-button"')` als harter „Abmelden ist letzter"-Wächter, Docstring trägt **beide** Richtungen mit Datum (2026-09-09 N3-Lesart b → 2026-09-13 N.9); `test_app_html_has_a_live_manage_spaces_entry`-Regex `[^<]*` durch `.*?` mit `re.DOTALL` ersetzt (nested `<svg>`), separate Label-Assertion bleibt. **Drei echte Funde beim Bau (alle im selben Commit behoben):** (1) `test_shell_grid_is_240_480_1fr` (G-R-Wächter) schlug rot an, weil mein erster `.rail__account`-Kommentar das Literale `@media (max-width:1280px)` enthielt — der Wächter matchte den Kommentar-Text. Behoben durch allgemeinere Formulierung („die schmale-Query ist weg"). (2) `test_app_html_has_a_live_manage_spaces_entry` schlug nach dem H2-Markup-Touch rot an (`AssertionError: Menüpunkt 'Spaces verwalten' fehlt`), alte Regex mochte nested `<svg>` nicht — `.*?` mit `re.DOTALL` + separate Label-Assertion. (3) `scripts/rotate_session_block.sh phase8_6_ui_polish` lief nur, nachdem ich den neuen Block-H-Sub-Block an den Head angehängt hatte (Skript-Logik Z. 60-74: genau ein Block → exit 2, ≥2 Blöcke → rotieren); der G-R-Sub-Block wanderte verbatim ins Archiv, der Head trägt jetzt genau einen Block H. **Selbstprüfung §0.5:** `pytest -q` **981 passed in 108 s** (V107-Baseline 981 unverändert — Block H ändert keine Test-Zahl, 1 Test umbenannt + 1 minimal angepasst), `node --check` auf alle 13 JS-Dateien ✅ (keine JS-Änderungen), `ui_budget.py` **5/5 im Korridor**, 143,1 KB gzip, app.css jetzt **24,2 KB** gzip (vs. G-R 24,0 KB, +0,2 KB für die `.rail__account`-Spalten-Anordnung + `.account-nav`-Flex-Container + Chevron-Icon-Rule + die ausführlichen Block-H-Kommentare; app.css bleibt deutlich unter 250 KB), Tabu-Diff §0.3 **leer** (nur `phase5_ui/webui/static/{app.html,app.css}` und `phase5_ui/tests/test_static_routes.py` berührt). Kein `pkill -f`, kein `systemctl`, sharefyx-mcp **PID 991** nur gelesen. **Drei Selbst-Screenshots** `docs/screenshots/p86_block_h_{01..03}_*.png` (111/110/141 KB): Rail bei 1440 mit beiden Knöpfen unten, Rail bei 1200 mit gleicher Anordnung (kein Kollaps), Konto-Dialog offen mit Akzentkante + Chevron auf beiden Knöpfen. **Doku-Hygiene:** Modul-Status Z13 ⬜→✅ (Reihenfolge jetzt G → G-R ✅ → **H ✅** → J → Gate), dieser Session-Block, Rotation per `scripts/rotate_session_block.sh phase8_6_ui_polish` (G-R-Sub-Block 235 Z./18.073 B verbatim ins Archiv), Frontmatter `updated:` im Phase-Head (H-Eintrag voran), `docs/INDEX.md`-Phase-8.6-Karte nachgezogen, `screenshots_latest/`-Symlinks Block-G → Block-H (P8.6-AK blockweise — diese Symlinks waren seit Block G nicht aktualisiert worden, jetzt nachgeholt), dieser Current-State-Absatz — alles im selben Commit. **Nächster Schritt: Block J** (der `pytest`-Flake, P8.6-AJ, datierte Tabu-Ausnahme für `phase4_auth/authserver/{crypto.py,store.py}` — neue Funktion `new_public_id()` mit Rejection-Sampling gegen führendes `-` + zwei Aufrufe in `store.py:294/393`, `authctl.py:199` bekommt `help`-Text für den Altbestand). Plan §6.4 engere Tabu-Probe: `git diff --stat -- phase4_auth/authserver` zeigt **genau zwei Dateien**, `store.py` genau 2 Zeilen — jede Abweichung ist Abbruchgrund.

**[2026-09-17, P8.6 Block J erledigt: `pytest`-Flake behoben (P8.6-AJ, datierte Tabu-Ausnahme) ✅ — Claude Code — eigener Commit, getrennt von jedem UI-Commit.** **Vorab-Korrektur:** die drei Commits zwischen dem letzten hier eingetragenen Stand (Block H) und diesem — Block H-R-3 (drei Locks H-R.6/.7/.8), der Rail-Exklusivitäts-Nachtrag und jetzt Block J — hatten diesen Current-state-Absatz nie nachgezogen, nur den Phase-Head; dieser Eintrag holt den Sprung nach, ohne die Zwischenschritte einzeln auszubuchstabieren (volle Herleitung: `phase8_6_ui_polish/CLAUDE.md` Session-Block 2026-09-17). **Block J selbst:** `phase4_auth/authserver/crypto.py` bekommt `new_public_id(nbytes: int = 16)` — Rejection-Sampling (`while value.startswith("-")`) statt Umkodierung, damit Alphabet/Länge zu `new_secret` identisch bleiben; behebt den seit 2026-08-20 als „reihenfolgeabhängiger Flake" fehldiagnostizierten Bug in `test_authctl.py::test_revoke_kills_the_family` — die echte Ursache (gemessen 2026-09-13, P8.6 Plan 2 §1.3): `secrets.token_urlsafe(16)` liefert in **1,569 %** der Ziehungen ein führendes `-`, `argparse` liest das als Optionsflag statt als Wert. `store.py:294` (`create_client` → `client_id`) und `store.py:393` (`create_family` → `family_id`) auf `crypto.new_public_id(16)` umgestellt — genau die zwei Stellen, deren Wert je auf einer Kommandozeile landet (`authctl revoke --family-id <ID>`); die zehn übrigen `new_secret`-Aufrufstellen bleiben unverändert, sie erzeugen opake Geheimnisse, die nie eine Kommandozeile sehen. `phase4_auth/scripts/authctl.py`s `--family-id`-Argument bekommt einen `help`-Text für den Altbestand (IDs von vor dem Fix können noch mit `-` beginnen — Gleichheitsform `--family-id=-abc`). **Drei Tests:** `test_revoke_kills_the_family` auf `--family-id=` umgestellt (Verteidigung in der Tiefe), neu `test_revoke_accepts_a_family_id_starting_with_a_dash` (Altbestands-Pfad) und `test_new_public_id_never_starts_with_a_dash` (5.000 Ziehungen, plus Länge/Alphabet-Gleichheit zu `new_secret`). **Enge Tabu-Probe (P8.6-AJ/§6.4) exakt erfüllt:** `git diff --stat -- phase4_auth/authserver` zeigt **genau zwei Dateien** (`crypto.py`, `store.py`), `store.py` **genau 2 geänderte Zeilen**; die breitere Tabu-Probe (§0.3) blieb ebenfalls leer — keine neunte P1-Contract-Öffnung. **Selbstprüfung:** `pytest -q` **994 passed in 111,5 s** (992 + 2 netto), `phase4_auth/tests/{test_crypto,test_authctl}.py` isoliert 26/26 grün, kein `ui_budget`-Touch nötig (kein `phase5_ui/webui/static/**`-Berührung), kein `pkill -f`, kein `systemctl`, sharefyx-mcp **PID 991** nicht angefasst. **Doku-Hygiene:** Phase-Head Modul-Status Zeile 15 ⬜→✅ + Session-Block-Nachtrag + Frontmatter-`updated:`-Kettenkorrektur, `docs/INDEX.md`-Phase-8.6-Zeilen (Kopf + Plan-Karten) nachgezogen, `phase4_auth/CLAUDE.md`s Flake-Notiz von „bekannt, nicht untersucht" auf „behoben, Ursache + Fix verlinkt" korrigiert, dieser Current-State-Absatz — alles im selben Commit. **Nächster Schritt: Gate** (Wegwerf-Ritt + `p86_polish_smoke.py`, 14 Stationen aus Plan 2 §7.2, Nikinger-Sichtprüfung mit fünf offenen Entscheidungen §7.3, danach Deploy `v3.0.2`) — Reihenfolge P8.6-AH ist damit **G → G-R → H → H-R (alle Teile) → J alle ✅, nur noch Gate → Z offen.**

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


**[2026-09-30, P9 Step B (zweiter Teil) — V153 entschieden, und einer der beiden Wege im Plan ist
nachweislich unbaubar — opencode/M3 — Repo-Seite fertig, Ausführung bleibt beim Nikinger.]**
`pytest` **1091** (1084 + 7 Wächter), kein `systemctl` durch einen Agenten, kein Service-Touch. **Befund 1: der
`sudoers`-Weg aus Plan §4.2 funktioniert auf dieser VM nicht.** Die Unit setzt
`NoNewPrivileges=true`, und sudo lebt vom setuid-Bit — gemessen: `setpriv --no-new-privs --
sudo -n -l` → `sudo: The "no new privileges" flag is set, which prevents sudo from running as
root.` Ein `NOPASSWD:`-Fragment wäre wirkungslos, und es zu retten hieße, die Härtung
abzuschwächen. **Es bleibt polkit — V153 entschieden, und zwar per Messung statt Präferenz.**
**Befund 2: polkit kann es auf dieser Box nicht eng genug, und das steht in keinem Plan.**
`systemctl --version` → **255.4-1ubuntu8.17**, und der lokal installierte Manpage-Abschnitt
*Security* in `org.freedesktop.systemd1(5)` nennt für `StartUnit()`/`StopUnit()`/`RestartUnit()`
**eine gemeinsame** Aktion: `org.freedesktop.systemd1.manage-units`. Die feingranularen
`manager.restart-unit` gibt es erst ab neuerem systemd — ein `<defaults>`-Eintrag kann danach
**gar nicht** nach Unit filtern. Ob systemd 255 der Aktion ein `unit`-Attribut mitgibt, ist
unprivilegiert **nicht** auslesbar (`pkcheck` sagt *not registered*, weil systemd die Aktion erst
zur Laufzeit bei polkitd registriert) — ein Fehlversuch wäre also nur am echten Neustart zu
entdecken. **Gebaut ist die Form, die in beiden Fällen das Richtige tut:**
`phase3_edge/polkit/49-tailscaled-watchdog-restart.rules` als **JS**-Regel (nur sie kann auf
`action.lookup("unit")` prüfen), die `manage-units` **und** die feingranulare Aktion abdeckt, in
beiden Blöcken zusätzlich `unit == "tailscaled.service"` und `subject.user == "savefyx"`. Fehlt
das Attribut, greift die Regel **nicht** und der Watchdog loggt seine vorhandene Zeile —
sicherheitsseitig der gewünschte Fehlerfall. **Ohne** den Unit-Abgleich hätte `savefyx` das
Management **aller** Units, auch aus `sharefyx-mcp` heraus; das wäre in einer Härtungsphase eine
**Befund 3 (ausgeführt, Ergebnis da): die Probe, die die Restfrage
entscheidet, ohne `tailscaled` anzufassen** — `phase9_hardening/step_b/` mit einer Wegwerf-Unit
(`ExecStart=/bin/true`, dieselbe Härtung) und einer Wegwerf-Regel, die *diese* Unit freigibt.
Ergebnis: `systemctl restart sharefyx-watchdog-probe.service` → **`AUTORISIERT`**, Journal
`Starting … Deactivated successfully … Finished` bei `User=root` — ohne polkit hätte `savefyx` diese
root-Unit nicht starten können, also war polkit das Tor, und **systemd 255.4 schickt das
`unit`-Detail doch**: die enge Regel trägt. Nebenbefund mit praktischem Wert: eine Verweigerung
kostet hier **25 s** (kein polkit-Agent, headless → Agent-Timeout), ein künftiges Nichtgreifen der
Regel zeigt sich also als Hänger, nicht als schnelles „restart fehlgeschlag".
**Befund 7 (2026-10-01, P9-19 geschlossen): das Rate-Limit hält, live bewiesen.** Nach dem Fix im
zweiten Fenster: 18:05:31 Stop → **18:05:40 Restart (9 s)**, State-Datei real (`1790870740`) →
18:09:28 zweiter Stop → **zehn Takte `rate-limited` (256s → 829s, Fenster 900 s) ohne einen einzigen
Restart**, `tailscaled` blieb dabei ~10 min unten, um 18:20:33 wieder `healthy`. **Nebenfund:** um
18:19:29 lief der Pfad über `unhealthy: Self.Online=false` statt `status unclear` (Dienst lief, noch
nicht online) — damit ist **auch der `false`-Zweig von Stufe 1 live belegt**, den vorher nur Mocks
kannten. **Benannt, nicht erzwungen:** der Pfad „Fenster abgelaufen ⇒ wieder ein Restart" fehlt (es
hätte 15 Minuten absichtlichen Ausfall bedeutet). **Und ein eigener Messfehler, der ins Protokoll
gehört:** ich meldete kurz nach `install_units.sh` „`/run/tailscaled-watchdog/` fehlt", weil ich
parallel zum 60-s-Takt prüfte statt danach — der Lauf eine Minute später legte es an und ließ es
stehen. **Merksatz: erst den Takt abwarten, dann messen.** **Damit ist Step B ✅.**

**Befund 6 (2026-10-01, P9-19sgeführt und beim ersten Mal gescheitert): die Units waren installiert — und der Dienst startete ins Leere.** `install_units.sh` lief durch, der Timer wurde `enabled`, `list-timers` zeigte ihn, und trotzdem **`status=203/EXEC` in jedem Takt**. Ursache: `local.env` setzt `REPO_ROOT=/opt/sharefyx/current` (und `install_units.sh:53` verlangt die Variable bewusst), der `__REPO_ROOT__` in der Unit zeigte also aufs **Release** `20260918T183907` — und dort liegt `tailscaled_watchdog.sh` nicht, weil das Skript erst am 2026-09-26 ins Repo kam. Ein Scan über alle installierten Units traf **genau eine** mit totem Pfad: **es ist eine Verzögerung, keine Pfadlogik — und sie trifft zuerst jede neu hinzugekommene operative Datei.** Der Befund stand wörtlich im Repo: `phase3_edge/CLAUDE.md` notiert ihn seit 2026-09-28 („der Watchdog startete dadurch ins Leere"), und der tail-proxy wurde am 2026-09-29 genau deshalb **ohne** `__REPO_ROOT__` gebaut. Nur die watchdog-Unit (Code vom 26.09., einen Tag älter als der Befund) hat die Lehre nicht bekommen. **Nikinger-Entscheidung 2026-10-01: Systempfad** — `ExecStart=/usr/local/libexec/sharefyx/tailscaled_watchdog.sh`, `Documentation=` fällt mit derselben Begründung, Installation per `sudo install -D -m 0755` **vor** `install_units.sh`; elfter Wächter (`test_execstart_carries_no_repo_path`, 10/10, Gegenprobe 2 Verstöße → 2 rot). **Gelöst im dritten Takt** (B2a + B2 wiederholt): Journal `tailscaled_watchdog.sh[…]: healthy: Self.Online=true` + `Finished`, Timer `enabled` **und** `active`. Die Zeile belegt mehr als den Pfad — die Unit läuft als `savefyx` unter voller Härtung und findet `tailscale`, `python3`, `date`, `timeout` im Sandbox-PATH. **Stufe 1 und der gesunde Normalfall sind live; Stufe 2 (netcheck) und Stufe 3 (Restart) warten auf B3.** **Und die Lehre über den Betrieb:** `203/EXEC` war harmlos, aber ein **laufender Timer beweist nicht, dass ein Dienst arbeitet** — der Abschluss ist jetzt die `healthy: Self.Online=true`-Zeile. **Befund 6 (2026-10-01, P9-19 — und das ist der Grund, warum diese Abnahmezeile existiert): das Rate-Limit war nie in Kraft.** Der erste Teil lief exakt wie vorhergesagt — `status unclear → netcheck failed → tailscaled restarted`, polkit-Pfad, Journal-Beleg, Neustart **29 s** nach dem Stop. Der zweite Teil schlug fehl: **zwei Restarts 189 s auseinander**, und `ls /run/tailscaled-watchdog/` → *No such file or directory*. `systemctl show -p RuntimeDirectoryPreserve` → **`no`**: die Unit legt das Verzeichnis vor `ExecStart` an und **löscht es beim Deaktivieren wieder**, bei einem Timer-`Type=oneshot` also nach *jedem* Takt. Das Skript schreibt seine State-Datei genau dorthin — das Schreiben gelingt (die Log-Zeile danach beweist es), Sekundenbruchteile später ist sie weg. **Plan §4.2 wollte das Rate-Limit, „weil ohne das ein Watchdog eine Restart-Schleife baut, die den Ausfall verlängert statt ihn zu beheben" — genau die Schleife wäre aktiv gewesen.** Und der bittere Teil: **`test_restart_is_rate_limited_to_once_per_15_minutes` war grün**, weil sein Mock die State-Datei in `tmp_path` legt, wo sie zwischen zwei Läufen überlebt. **Ein Test, der einen Zustandsspeicher simuliert, den es live nicht gibt, meldet Grünes über eine Eigenschaft, die nicht existiert** — und bei jedem Zustand, den ein Test mockt, ist die Frage, wer ihn im echten Betrieb bereitstellt. Gebaut: `RuntimeDirectoryPreserve=yes` + zwei Wächter (die Direktive, und die Kopplung State-Datei ⊂ RuntimeDirectory), Gegenprobe 2 Verstöße → 2 rot. **Merksatz für jede künftige Unit in diesem Bereich: `RuntimeDirectory=` allein ist ein Arbeitsverzeichnis, kein Speicher — wer Zustand über Takte braucht, braucht `RuntimeDirectoryPreserve=yes`.**

**Befund 5: C0 ist sauber, nachdem ich selbst einmal ein Nachlade-Rennen produziert hatte** — die erste Wiederholung nach dem Löschen der Probe-Regel ergab `rc=0`, die zweite `rc=1` nach 25 s (polkitd hält die gelöschte Regel kurz im Speicher). Damit ist B0 vollständig bewiesen: mit Regel autorisiert, ohne Regel verweigert. 

**Befund 4: die Units sind auf der VM überhaupt nicht installiert** (`ls
/etc/systemd/system/tailscaled-watchdog.*` → *No such file*, `systemctl list-timers` → 0 Timer;
der Deploy vom 2026-09-18 liegt vor dem Step-B-Code vom 2026-09-26). **Vier neue Wächter** in
`phase9_hardening/tests/test_tailscaled_watchdog.py` (**12/12 grün**, Gegenprobe mit vier
eingebauten Verstößen → **6 rote Assertions**): Form jedes Blocks (Aktion+Unit+User, genau ein
`YES` und das als letzter Ausgang), **Kopplung** zwischen Regel, Skript
(`systemctl restart tailscaled.service`) und Unit (`User=savefyx`), die drei Nachbar-Aktionen
bleiben unberührt, und die Probe darf `tailscaled` nicht nennen — **alle vier filtern
Kommentarzeilen vorher heraus**, weil die Regel dieselben Begriffe in ihren Befund-Kommentaren
nennt (dritte Wiederholung derselben Falle: P8.6 Block H, P9 Step G). `phase3_edge/polkit/` ist
bewusst ein **eigenes Verzeichnis** und nicht `systemd/`: eine polkit-Regel ist keine Unit, und
`install_units.sh` globbt `systemd/*.service|timer` — eine `.rules`-Datei dort wäre eine Falle
für den Nächsten, der den Glob erweitert. **Ablauf für den Nikinger:**
`phase9_hardening/step_b/RUNBOOK_STEP_B.md` §2 B0–B3, mit den zwei bekannten Fallen
(`install_units.sh` aktiviert nur `sharefyx-mcp` **und startet es dabei neu**; der Watchdog-Timer
braucht ein eigenes `systemctl enable --now`) und drei Induktions-Varianten für P9-19 samt
Risiko. **Benannt, nicht entschieden:** die beiden Alternativen, falls die Probe `VERWEIGERT`
sagt, berühren die Härtung (breites `manage-units` = abgelehnt; `User=root` = PATH-aufgelöste
Binaries mit Root-Rechten) — das ist eine Entscheidung des Ningkers, und der dritte, sauberere Weg
(fixer Root-Oneshot mit hartkodiertem `ExecStart`, per Flag angestoßen) wäre echte
Umfangserweiterung und ist **nicht** gebaut. **Nächster Schritt:** B0 — drei `sudo install` plus
ein `systemctl restart` auf die Wegwerf-Unit, danach aufräumen. Unverändert gilt: Step A wartet
auf die Domain, Gate/Z auf A4–A8.

 — `fastmcp` exakt gepinnt, und die Reihenfolge entschied sich an
einer Domain-Messung — opencode/M3 — ein Commit, kein Service-Touch.]** **Erst die Domain
geprüft, wie der Handover es verlangte: sie ist nicht registriert.** `eurofyx.com` liefert
`NXDOMAIN` **und** `rdap.verisign.com` 404, dieselbe Antwort für `.de`/`.tech`/`.app`/`.cloud`/
`.net`/`.org`/`.eu` — A4 braucht eine auflösende Domain fürs Zertifikat, also bleiben A4/A5/A7/A8
blockiert, und der letzte Code-Step wurde gezogen. **Der Fund des Steps: die Plan-Prämisse
„installiert ist 3.4.4" war falsch, und der Fehler war das Ergebnis.** `deploy.sh:153` baut pro
Release ein **frisches** venv, `scripts/dev_install.sh:9-13` installiert editable — der Pin
`>=3.4,<3.5` löste also bei jedem Deploy auf das damalige neueste 3.4.x auf. Gemessen read-only
über `/opt/sharefyx/current/.venv`: der **Live-Release lief bereits auf `fastmcp` 3.4.7 / `mcp`
1.30.0** (Release `20260918T183907`), das Dev-venv noch auf 3.4.4. **Der stumme Patch-Drift, den
P3-D (`phase3_edge_plan.md:106`) verbieten wollte („unter einem Dauerdienst darf sich das nicht
unbemerkt bewegen"), hatte also schon stattgefunden** — und P3-D wie P4-R behaupteten beide einen
exakten Pin, **den der Code seit dem ersten Commit `1c131c2` nie hatte.** Zwei Pläne, eine
Entscheidung, null Umsetzung. **Gebaut:** `fastmcp==3.4.7` exakt in `phase2_mcp/pyproject.toml`
mit datiertem Kommentar an der Zeile (Grund, Messung, P9-R/V79/V163), Präzedenz
`argon2-cffi==25.1.0`/`cryptography==49.0.0` aus `phase4_auth`. **P9-55 verlangte wörtlich
„weiterhin `<3.5`"** — gebaut ist `==3.4.7`, oberhalb jeder 3.4-Version, also innerhalb P9-R,
aber ohne die Range-Form, weil die Range-Form der Mechanismus des gemessenen Drifts ist:
**Nikinger-Entscheidung 2026-09-30**, im Plan §10 als Abweichung dokumentiert, nicht
stillschweigend. **V163 beantwortet, mit drei Codepunkten statt der Vermutung aus der
Planungssession:** `metadata.py:19` lässt `client_id_metadata_document_supported` bewusst
**abwesend** (CIMD aus, P4-E/V14), `metadata.py:32` führt `token_endpoint_auth_methods_supported:
["none"]` (öffentlicher Client, gar keine Client-Assertions), und die benutzte fastmcp-Fläche
enthält weder `OAuthProxy` noch `JWTVerifier` — Auth trägt der eigene `BearerAuthASGI`. Die drei
Releases 3.4.5/3.4.6/3.4.7 liegen auf OAuth-/SSRF-/JWKS-Pfaden, die dieses Projekt nicht benutzt:
**Fix inert, Bump Hygiene.** **Der eigentliche Riegel ist ein Test:**
`test_the_installed_fastmcp_matches_the_pin` vergleicht installiert gegen deklariert und **läuft im
Release-venv mit**, weil `deploy.sh:169` dort `pytest -q` aufruft und den Deploy abbricht — ein
Drift ist damit ein roter Deploy statt einer Randnotiz. Fünf Wächter in
`phase9_hardening/tests/test_step_h_deps.py`, **Gegenprobe mit vier eingebauten Verstößen → 7 rote
Assertions über vier Tests**, danach zurückgebaut. `pytest` 1079 → **1084** in 186 s (Bestand
unverändert grün **mit** 3.4.7), `ui_budget` **5/5** (151,8 KB; `search_items` 128,6 ms /
`get_item` 4,7 ms über den echten MCP-Stack, der 3.4.7-Pfad ist also wirklich gelaufen),
`doc_health` 0 Befunde, **kein `pkill -f`, kein `systemctl`**, `sharefyx-mcp` nur gelesen. **Zwei
eigene Fehler, beide im selben Commit behoben:** `req.specifier.version` gibt es nicht
(`SpecifierSet` hat kein `.version` — zwei Tests rot, bevor der Helper existierte), und ein
`edit` auf die P2-Modulstatus-Tabelle hat Zeile 13 mitgefressen, weil der Anker am Zeilenanfang
statt am Zeilenende saß; der Diff (13 Zeilen rein, 0 raus) ist der Nachweis. **Benannt, nicht
gebaut:** das transitive `mcp` bleibt ungepinnt (Dev 1.28.1, Live 1.30.0 — P9-Backlog-Kandidat,
kein Blocker). Kollateral-Korrekturen mitgezogen, weil sie sonst falsche Behauptungen
festgeschrieben hätten: `phase3_edge/CLAUDE.md:148` („`fastmcp` 3.4.4 installiert — keine Änderung
nötig") war seit P3 Step 0 stehengeblieben und ist jetzt datiert korrigiert, `phase2_mcp/CLAUDE.md`
Modul-Status Zeile 14 neu. **Nächster Schritt: nichts im Code** — Gate/Z wartet auf A4–A8, und
dessen zwei Doku-Posten sind strukturell, nicht durch Kürzen lösbar: INDEX-Rotation (P9-L, jetzt
48.118 B, 7.158 B über dem Softcap) und die Contract-Sektion in `phase1_storage/CLAUDE.md`
(43.333 B).

 — Haertungsphase, `docs/concepts/phase9_hardening_plan.md` geschrieben — Claude Code — reine Planungssession, kein Produktcode-Touch.]** **Vier Nikinger-Entscheidungen, alle im Plan §1 gelockt:** **(1) P9 ist eine Haertungsphase, kein UI-Umbau** (**P9-A**) — die ROADMAP-P9-Zeile („Obsidian-Map-Umbau + verbundene AI-Sessions, letzter grosser UI-Umbau") ist **ersetzt, nicht erledigt**; der Inhalt geht nach P10, die Liste steht in Plan §15. **(2) Die Domain kommt ueber einen eigenen VPS als TLS-Terminator**, der per Tailscale im Tailnet haengt und intern zur Heim-VM proxyt; der Funnel-Hostname bleibt betriebsbereiter, dokumentierter Fallback (**P9-C**). **(3) Neunte P1-Contract-Oeffnung, angekuendigt und datiert** (**P9-G/P9-H**): `doing` als Statuswert und `assignee` als erstklassiges Feld mit Index-Spalte — neun Stellen in `models.py`/`store.py`/`index.py`, die enge Probe (`git diff --stat -- phase1_storage/storage` = genau drei Dateien) ist Abbruchkriterium. **(4) Loeschen (F2) = Verschieben nach `_trash/`** nach dem bestehenden Asset-Muster (Lock N5, `store.py:849`), **fuer Nutzer unsichtbar** (kein Papierkorb-UI, keine Wiederherstellung im UI), human-only, Gate = zweifache Rueckfrage **plus** Eintippen des Item-Titels (**P9-I/J/K**). **Zwei Planungsbefunde, die Annahmen aus dem P8.6-Handover widerlegen — beide gemessen, nicht vermutet:** **(a) Tailscale Funnel kann keine eigene Domain bedienen.** Die Doku ist eindeutig (*„Funnel can only use DNS names in your tailnet's domain"*), ein CNAME darauf erzeugt einen TLS-Namens-Mismatch (tailscale/tailscale#16478) — **Option (a) aus Handover §4.2 existiert nicht** (**P9-E**). Der billige Ersatz Cloudflare Tunnel ist per **P9-D** ausgeschlossen, und zwar mit Beleg statt Geschmack: `phase3_edge_plan.md` §0.4 hat R4 datiert korrigiert, weil bei Funnel **die Node selbst** TLS terminiert — ein Wechsel zu Cloudflare waere ein gemessener Rueckschritt, keine neutrale Umstellung. **(b) `SharePolicy` ist bereits gebaut** (`storage/acl.py`, `webui/shares.py`, `share_write`-Fixtures in `phase7_spaces_admin/scripts/`): das Cross-Space-Rechte-Thema aus Handover §4.1b braucht **kein** fertiges P6 — es ist billiger als dort vermutet, bleibt aber Hard-Rule-4-Arbeit und geht als **benannter** Posten nach P10 (Plan §0.6). **Step 0 ist bereits gelaufen und war nicht leer** — vier gemessene Doku-Defekte: 5 kaputte `up:`/`down:`-Links in `phase8_6_ui_polish_block_h_r_3_escalation.md` (die Karte nutzt `../`, braucht `../../`) · zwei Mini-Plaene ohne L1-Card · die `ROADMAP.md`-INDEX-Zeile stale („~26KB · Phasen 1–8", real 41.784 B inkl. P9) · **zwei** `screenshots_latest/`-Verzeichnisse. Step 0 repariert sie und nagelt den Scan als `scripts/doc_health.py` + Test fest. **Die INDEX-Rotation ist in dieser Session begonnen worden, weil sie Voraussetzung der eigenen Lieferung war:** `docs/INDEX.md` hatte **156 B Luft**, die `updated:`-Kette (916 B) liegt jetzt verbatim in `docs/INDEX_UPDATES_ARCHIVE.md`, die Datei steht bei **38.822 B** (90 B Luft). Das **Skript** `scripts/rotate_index_updates.sh` baut Step 0.1 (**P9-L**) — die Handarbeit hat jetzt viermal nicht getragen. **Weitere Recherchebefunde, im Plan als `[VERIFY]` statt als Gewissheit abgelegt:** `fastmcp` 3.4.4 installiert, 3.4.7 (2026-08-10) traegt einen Security-Fix fuer CIMD/`private_key_jwt` im **OAuthProxy** — den dieses Projekt nicht benutzt (eigener `BearerAuthASGI` gegen `phase4_auth`), der Bump ist also Hygiene (Step H, V163) · FastMCP 4.0.0 (2026-08-31) bringt die MCP-Revision `2026-07-28` (zustandslos, kein `initialize`-Handshake, kein `Mcp-Session-Id`), Alt-Clients laufen per Aushandlung weiter — **V79 bleibt eigene Mini-Phase** (**P9-R**), eine Protokollmigration mitten in einer Haertungsphase ist genau die Vermischung, die P8.6 zwei Plaene gekostet hat · CIMD ist bei claude.ai inzwischen der empfohlene Connector-Modus vor DCR, vorgemerkt, nicht eingeplant. **Fuenfte Vorgabe desselben Tages (P9-Q):** die Infra-Steps A/B/C laufen als **Coarbeit in opencode** — M3 leitet Schritt fuer Schritt an, der Nikinger fuehrt aus und liefert jede echte Ausgabe zurueck; dasselbe Muster wie Proxmox-Migration und Ollama-Setup. Ein Schritt pro Runde, weil bei DNS, Zertifikaten und Treibern jeder Schritt an der Ausgabe des vorigen haengt — und weil eine nur quittierte statt gelesene Ausgabe genau die Klasse Fehler durchlaesst, die der `umask 0177`-Deploy-Blocker war. **Naechster Schritt: P9 Step 0** (Phasenverzeichnis `phase9_hardening/` anlegen, Rotationsskript bauen, die vier Doku-Defekte reparieren, Baseline `pytest` 995 / `ui_budget` 5/5 messen). Ausfuehrungsteilung pro Step in Plan §0.5.

**[2026-10-01, P9 Step A — Domain live, A5 ✅, und eine Korrektur, die A7/A8 zusammenlegt — Claude
Code.]** `sharefyx.eurofyx.com` → `217.160.128.146` (IONOS, kein CAA, kein Wildcard). **Runbook-Befund 4
war falsch:** Tokens sind an `resource = {base_url}/mcp` gebunden (`resolver.py:49`), der A7-Restart
kappt also beide Connectoren sofort — **Nikinger: harter Schnitt, A7+A8 in einer Sitzung**, kein
Eingriff in `phase4_auth/authserver/`. **Befund 5 umentschieden und gebaut:** UI-Übergangsfenster für
die alte Funnel-Adresse (eine zusätzliche CSRF-Origin bis `SPACE_UI_LEGACY_UNTIL`, Uhr pro Anfrage,
fail-closed; Warndialog in `.account-nav`-Form bei jedem Laden), 23 Tests + Browser 16/16, `pytest`
**1114**. **Offen beim Nikinger:** Deploy vor A7 (liefert P9 D–H mit), Badge-Version. Nächster Schritt
A4 (Caddy). Details: `phase9_hardening/CLAUDE.md`.
**Nachtrag Session-Ende:** Standardknöpfe tragen jetzt das exakte Bild des Übersicht-Knopfs
(deckende Tokens `--btn-std-*`, pixelgeprüft). **Nikinger: noch kein Deploy; der nächste trägt
`v3.1.0`.** Nächste Session: A4 → Deploy `v3.1.0` → A7+A8 in einer Sitzung.

**[2026-10-01, P9 Step A — A4 vorbereitet: zwei Befunde, ein Vorlagen-Defekt, ein Testfund —
opencode/M3 — ein Commit, kein Eingriff in einen laufenden Dienst.]** Cooperation-Runde (P9-Q,
ein Schritt pro Runde): A4 ist ein `sudo`-Schritt auf dem VPS, also war meine Aufgabe die Vorlage,
die Befunde und die Erwartungshaltung. **Befund 8 — P9-10 ist bis A7 nicht erfüllbar:** die
Abnahmezeile verlangt *200 **und** LE-Zertifikat*, aber die Zertifikats-Hälfte gehört Caddy und
die `200` gehört `SPACE_ALLOWED_HOSTS` (A7). Gemessen am laufenden Dienst: `curl -H "Host:
sharefyx.eurofyx.com" http://127.0.0.1:8765/health` → `400 Invalid host header`. **Die ganze Kette
einmal mit echtem Caddy davor gespielt** (Ubuntu-Paket entpackt, `caddy 2.6.2` auf Wegwerf-Port vor
die Relay-Adresse `100.93.43.122:8765`, also exakt die Strecke des VPS): neuer Host 400,
`100.93.43.122` 400, erlaubter ts.net-Host **200 mit `{"status":"ok",…}`** — damit sind **das Relay
funktionierend** und **Caddys Host-Durchreich** belegt, wo vorher nur „Caddy-Default" stand. Folge:
**P9-10 ist in P9-10a (Zertifikat, A4) und P9-10b (`200`, nach `ALLOWED_HOSTS`) geteilt**, die 400 ist
in A4 das erwartete Ergebnis. **Befund 9 — auf dem VPS ist kein Caddy** (`ubuntu`/100.121.142.113,
Tag `tag:sharefyx-edge`, 80+443 ohne Listener) und A4 fing mit `install … /etc/caddy/Caddyfile` an:
**A4 ist jetzt A4a (messen, `apt install -y caddy`, Paket ist 2.6.2, `validate` → `Valid
configuration`, `postinst` legt `/var/log/caddy` an) + A4b (Konfiguration, `validate`, Restart)**;
**kein `admin off`**, weil die Paket-Unit `ExecReload=… caddy reload …` hat und der Reload ohne
Admin-API measured `connection refused` gibt. **Vorlagen-Defekt:** der Platzhalter `<vps-tailnet>` war
als Adresse *des VPS* beschrieben, während `reverse_proxy` die **Heim-VM** meint → jetzt
`<heimvm-tailnet>` mit der gemessenen Ziel-IP im Kommentar. **5 neue Wächter**
(`phase9_hardening/tests/test_tail_proxy.py`, **12/12**, Gegenprobe 4 Verstöße → 5 rot),
`pytest` 1115 → **1120**, `ui_budget` 5/5, `doc_health` 0 (der Runbook-Zuwachs von Befund 8+9 ist
in der INDEX als Oversize benannt, P8-P). **Vorgeschlagen, nicht entschieden: A7a** —
`ALLOWED_HOSTS` vor A7 ziehen, dort wechselt kein `resource` (Befund 4), also bleiben beide
Connectoren gültig und Fabian ist nicht nötig; ein Neustart des Produktionsdiensts ist
Nikinger-Sache. **A4 ist danach ausgeführt** (A4a `2.6.2` via apt, A4b `Valid configuration` + `certificate obtained successfully`, LE `YE1`, CN `sharefyx.eurofyx.com`; extern `400 Invalid host header` = Befund 8, und derselbe `400` als `status=400 ua=curl/8.7.1` im Journal der Heim-VM belegt VPS → Tailnet → Relay → App) ⇒ **P9-10a ✅**; **Befund 10** = `caddy validate` liest den Adapter aus dem Dateinamen; der ACME-Platzhalter ist per `sed` ersetzt, `notBefore` blieb unverändert. **Und mein Datum war ein Tag falsch:** der erste Commit war durchgehend mit 2026-10-02 datiert, ohne dass ich das Datum gemessen hatte — die Gegenprobe kam erst mit dem LE-Zertifikat `notBefore=Oct 1`; 41 Fundstellen, ein Korrektur-Commit. **Offen:** Deploy `v3.1.0` (sonst ist das `LEGACY_*`-Fenster
wirkungslos), dann A7+A8 in einer Sitzung. Details: `phase9_hardening/CLAUDE.md`.

**[2026-10-01, P9 — Deploy `v3.1.0` **verschoben**, `.toolbar-btn` in Standardoptik, vier
Tailscale-Bilder geklärt — opencode/M3 — zwei Commits, kein Deploy, kein Eingriff in einen laufenden
Dienst.]** Der Auftrag war Punkt 1 der Übergabe (Release-Vorbereitung). Beim Durchgehen des Codes für
einen **ehrlichen** Changelog-Eintrag kam der Befund, der ihn kippt: **`doing` ist im Deploy-Fall für
einen Menschen erreichbar, und genau seine Eigenschaft ist der offene Befund.** `models.py ::
STATUS_VALUES["task"]` trägt `doing`, und `editor.js :: populateStatusSelect()` füllt das
Status-Feld der Kopfdaten aus `state.meta.status_values` — **rohe Werte**. Nach dem Deploy kann ein
Mensch `doing` wählen; und dann passt der Wert auf keinen der vier `_BUCKETS`-Einträge
(`bucketFor()` vergleicht exakt, `_overview()` zählt per `store.search`), die Aufgabe erscheint in
**keinem** Ordner-Zähler und in keinem der vier Rail-Ordner, findet sich aber über „Alle Items" und
die Suche. Das ist P9-P, das der Plan als Darstellungsentscheidung nach P10 verwies — als „in keinem
UI-Pfad sichtbar" vertretbar, per Deploy eine Eigenschaft, mit der ein Mensch rechnen muss.
**Nikinger-Entscheidung: Mini-Plan von Opus (Claude Code), dann bauen + deployen.** **Deshalb kein
Release-Vorbereitungs-Commit** — zwei gemessene Gründe, nicht Vorsicht: ein heute datierter
`## <Datum>`-Block in `docs/UPDATE_LOG.md` lässt das `deploy.sh`-Gate (P6-X) bei einem späteren
Deploy abbrennen, und der Changelog-Text ist ohne die `doing`-Entscheidung nicht schreibbar (ein
Eintrag, den man später ersetzt, steht zwei Commits lang in einem Menschen-Banner).
**Gebaut wurde Punkt 2 der Übergabe:** `.toolbar-btn` (zehn Formatierhilfen + Vorschau) war nach
`.btn` und `.account-nav` der **letzte** echte Knopf auf der alten grauen Plastik — jetzt dieselben
deckenden `--btn-std-*`-Tokens, `:disabled` bleibt `--surface` (in der Vorschau abgeschaltet, soll
„inaktiv lesbar" heißen), `.rail__glyph` bleibt als Badge bewusst alt. Beleg ist die Messung:
`p9_btn2_toolbar_probe.py` **13/13** (gerechnete Fläche stringgleich mit `.btn`, drei Verlaufshöhen
Δ ≤ 2, Randpixel Δ = 0, deaktiviert **flach** statt „heller"), Gegenprobe 1 Verstoß → 5 rot.
**Fünfte Wiederholung derselben Repo-Lehre in der eigenen Probe:** `count() == 1` für
`#home-button[aria-current]` war wertlos — Selektoren matchen das Attribut, nicht den Wert, der
Knopf trug `"false"`; ein Pixelvergleich bei `fx = fy = 0.5` traf die Beschriftung von „Anhängen"
(Δ 34); und die Verlaufsmessung des aktiven Knopfs stand im Deaktiviert-Block. Dazu die
Produktinvariante, die zwei davon ausgelöst hat: **der Editor öffnet per P5-Entscheidung in der
Vorschau** — die Formatierhilfen sind dort `:disabled`, jetzt behauptet statt angenommen.
**Punkt 4b geklärt:** vier unversionierte Tailscale-Kopien (Leerzeichen im Dateinamen) liegen jetzt
als `docs/screenshots/p9_step_a_01..04_*` versioniert (Infra-Beleg zu A3, keine Sichtprüfung), die
fünfte Datei `Machines - Tailscale.html` ist **gelöscht** — die gespeicherte Seite war die leere
SPA-Hülle (`tailscale-api-prefetch` = `{}`, 2,7 KB, keine Geheimnisse: geprüft, nicht vermutet);
eine leere Hülle ist kein Beweis, nur eine Datei, die jemand irgendwann für einen hält.
`screenshots_latest/` rotiert auf `p9_btn2_*`. **Was die Release-Vorbereitung dann umfasst:** Badge
`v3.0.2` → `v3.1.0` in `app.html:20` + neuer `## <Deploy-Tag>`-Block, dann `deploy.sh main` und
`health_gate.sh --expected-version=v3.1.0 --require-todays-update-log --expected-sha=<sha>`.
`pytest` **1122**, `ui_budget` 5/5 (153,0 KB), `doc_health` 0, Tabu-Pfade leer, **kein `systemctl`,
kein `pkill -f`** (Wegwerf-Instanz nur über ihre PID-Datei gestoppt). Details:
`phase9_hardening/CLAUDE.md`.

**[2026-10-02, P9 Block doing: Mini-Plan geschritten, Kandidat (a) entschieden — Claude Code — reine Planungssession, kein Code- oder Service-Touch.]** `docs/concepts/phase9_hardening_block_doing_plan.md` ist ausführungsreif für opencode/M3. **Nikinger-Entscheidung P9-V:** `doing` bekommt einen fünften `_BUCKETS`-Eintrag mit Rail-Label „In Arbeit" (Reihenfolge `open, doing, done, note, archived`, P9-X). P9-P ist damit datiert eingeengt: ein Eimer pro Statuswert ist Navigations-Vollständigkeit, die Hervorhebung bleibt P10. **P9-W:** nur das Rail-Label wird übersetzt, REST und MCP bleiben roh, damit ein angeschlossenes LLM `status: doing` und `assignee` liest. **Verworfen mit Argument:** (b) „Offen = {open, doing}" ergibt über `URLSearchParams` stillschweigend `open%2Cdoing` und damit eine leere Liste. (c) „`doing` nicht ins Select" schließt das Loch nicht, weil `doing` per MCP kommt, und es zerbricht den Editor für genau diese Items (Select-Wert `""`, beim Öffnen „ungespeichert", Speichern abgelehnt). **Korrigiert:** die Abnahme beginnt bei **P9-59** (P9-45–58 sind vergeben), der Dateiname folgt P9-T. `pytest` **1122**, `doc_health` 0. `phase9_hardening/CLAUDE.md` ist nach der Rotation wieder unter dem Softcap (~35 KB). **Plan vom Nikinger bestätigt, P9-W eingeschlossen.** **Nächster Schritt:** M3 baut den Block (ein Commit, Browser-Beleg 8/8). Danach macht M3 den Release-Commit (Badge `v3.1.0` und `UPDATE_LOG`), und der Nikinger führt den Deploy aus (Mini-Plan §8). Details: `phase9_hardening/CLAUDE.md`.

**[2026-10-02, P9 Block doing gebaut — das Eimer-Loch ist zu, `v3.1.0` ist freigegeben — opencode/M3 — ein Commit, kein Deploy, kein Service-Touch.]** Eine Aufgabe mit `status: doing` hat jetzt ihren eigenen Navigationsordner „In Arbeit": `_BUCKETS["doing"]` in `api.py` (Reihenfolge `open, doing, done, note, archived`, P9-X), Rail-Label in `state.js`. Danach erscheint sie in **genau einem** Zähler und **genau einem** Ordner, und Zähler == Liste gilt per Konstruktion, weil beide dieselben Filter benutzen. **P9-W:** übersetzt wird nur die Navigationsebene — Schema, REST und MCP liefern weiter roh `status: "doing"` plus `assignee`. **Der Step-F-Wächter ist umgedreht** (`test_the_bucket_hole_for_doing_is_named_not_silently_fixed` → `test_the_doing_bucket_closes_the_hole`, Docstring trägt beide Richtungen mit Datum; ein Testname, der die Behauptung umkehrt, wäre eine Lüge). **6 neue Tests** (T1/T2/T6 in `phase9_hardening/tests/test_doing_bucket.py`, T3/T4/T5 in `phase5_ui/tests/test_overview.py`), `pytest` 1122 → **1128**, `ui_budget` 5/5 (153,2 KB), Tabu-Diff **leer** ⇒ **keine zehnte P1-Contract-Öffnung** (V174: `phase1_storage/CLAUDE.md` §Geerbte Contracts bleibt unberührt). **Gegenlauf 5 Verstöße:** G1 → 7 rot, G2 → 2, G3 → 2, G4 → 1, G5 → 1, Kontrolllauf G0 = 0. **Browser 11/11** gegen eine eigene TLS-Wegwerf-Instanz (Port 18776); Kernbeleg: die Rail-Zähler springen nach einem Statuswechsel im Editor **ohne Reload** von `1/1` auf `0/2`. **Browser-Gegenlauf 7 von 11 rot** — und **S5/S7/S8 bleiben grün**, weil sie die Maschinenebene prüfen: die war schon vorher korrekt, das Loch war **rein navigativ**. **Befund beim Bauen:** der Plan sagte, das Duplikat-Filter-Verstöß G3 mache drei Wächter rot, gemessen machte es **einen** — Zähler und Listen prüfen **Zahlen**, und bei je einer offenen und einer laufenden Aufgabe stehen die beiden Duplikat-Zähler beide auf 1. Nach der Plan-Regel („nicht rot ⇒ Wächter wertlos ⇒ neu schneiden") holt T3 jetzt die **Item-Mitgliedschaften** aller fünf Eimer und beweist Disjunktheit + Vollständigkeit; damit ist P9-59 behavioural statt behauptet. **Und:** der erste Browser-Gegenlauf **stürzte ab**, statt rot zu melden (ein Klick auf einen Ordner, den es ohne den Fix nicht gibt) — dieselbe Repo-Lehre zum sechsten Mal, diesmal im eigenen Prüfskript; nachgebessert und beide Läufe neu gefahren. Vier Screenshots `p9_doing_*`, `screenshots_latest/` darauf umgehängt. `doc_health` 0. **Nächster Schritt, mit Zuständigkeit:** (1) **opencode/M3** macht am Deploy-Tag den Release-Commit — Badge `v3.1.0` (`app.html:20`) + neuer `## <Deploy-Tag>`-Block in `docs/UPDATE_LOG.md`; (2) **Nikinger** führt `deploy.sh` + `health_gate.sh` aus und misst dabei **P9-43** (erster Deploy mit Step F: Dauer des Index-Neuaufbaus am echten DATA_ROOT); (3) **Nikinger** kurzer Augenschein im echten Browser. Ablauf: `docs/concepts/phase9_hardening_block_doing_plan.md` §8. Details: `phase9_hardening/CLAUDE.md`.

**[2026-10-02, P9 — `v3.1.0` ist LIVE ✅ (Release `5414cb7`, Nikinger-Deploy 3:55 min, Health-Gate 9/9, P9-43 ✅ ≤ 1,05 s für 197 Items) — davor: erster `v3.1.0`-Deploy abgebrochen, Ursache behoben — Claude Code.]** `deploy.sh` brach in `pytest` im Release ab (`4 failed, 1119 passed, 5 errors`), alle neun in `phase9_hardening/tests/test_mcp_local_vision_server.py` mit `ModuleNotFoundError: requests`; das Release wurde entfernt, der Symlink blieb stehen, **live ist weiter `v3.0.2`**. **Ursache:** `requests` steht in keinem `pyproject.toml`, es kam 2026-09-10 (P8.6 Step V) von Hand ins Dev-venv; `deploy.sh` baut pro Release ein frisches venv. **Fix:** `phase8_6_ui_polish/scripts/mcp_local_vision_server.py` ist stdlib-only (`urllib`), der Test patcht `urlopen`. **Beleg am Gate selbst:** frischer Baum + frisches venv + `dev_install.sh` → **1128/1128** (ein Prüfaufbau-Artefakt — `git bundle verify` ohne Repo — nach `git init` grün), `import requests` dort nachweislich rot. **Benannt:** `vision_ollama.py` (CLI) braucht `requests` weiter, kein Gate betroffen. **Nächster Schritt (Nikinger):** Augenschein im echten Browser (Rail „In Arbeit", Badge `v3.1.0`), dann Step A: A7+A8 in einer Sitzung. Details: `phase9_hardening/CLAUDE.md`.

**[2026-10-02, P9 Block trace geplant — Claude Code — reine Planungssession.]** `docs/concepts/phase9_hardening_block_trace_plan.md`: `assignee` wird in UI und MCP sichtbar und beim Wechsel auf „In Arbeit" vom **Client** gefüllt (P9-Z, nie überschreibend); neues server-verwaltetes `updated_by` aus dem Principal plus Git-Autor im DATA_ROOT (P9-AA–AC) — heute zeichnet **nichts** den Schreiber auf. **Zehnte P1-Contract-Öffnung angekündigt** (`models.py`/`store.py`/`history.py`, kein Index-Schema-Sprung, kein Neuaufbau beim Deploy). Umfang und Auto-Füllen vom Nikinger entschieden. **Nächster Schritt:** opencode/M3 baut den Block (ein Commit). Der fehlende Warndialog auf der Funnel-Adresse ist Absicht bis A7.

**[2026-10-02, P9 Block trace gebaut — opencode/M3 — ein Commit, kein Deploy, kein
Service-Touch.]** Die Frage nach dem Deploy `v3.1.0`: was bedeutet `doing` in einem Space mit
zwei Personen? Vorher: der Status ist geteilt, aber **niemand wird aufgezeichnet**. Jetzt
beides, für Menschen und für ein angeschlossenes LLM. `assignee` wird in Liste und Editor
sichtbar, und der **Client** füllt es beim Wechsel auf „In Arbeit" (P9-Z — dem Server
Statussemantik zu geben, wäre das Kernprinzip auf den Kopf; er kennt Token → Space); neu ist
das server-verwaltete `updated_by` (Home-Space des authentifizierten Principals, über **keinen**
Kanal setzbar) plus der Git-**Autor** (`--author`, Committer bleibt `Space Server`, P9-AC).
**Zehnte P1-Contract-Öffnung** (`models.py`/`store.py`/`history.py`, enge Probe erfüllt) mit
**keinem Index-Schema-Sprung** ⇒ beim Deploy **kein** Neuaufbau, anders als nach Step F.
**24 neue Tests** (gezählt, nicht addiert: 5 `test_store.py` + 4 `test_history.py` + 6 `test_trace_block.py` + 4 `test_tools.py` + 1 `test_api.py` + 4 `test_static_routes.py`), `pytest` 1128 → **1152**, `ui_budget` 5/5 (155,1 KB), Tabu-Diff leer,
`doc_health` 0. **Gegenlauf** G1 → 1 · G2 → 2 · G3 → 1 · G4 → 2 · G5 → 4 rote Tests.
**Browser 8/8** gegen eine eigene TLS-Wegwerf-Instanz mit **zwei Principals und echter
Git-Historie** (Port 18777): B sieht „Zuletzt geändert von A", schreibt selbst, danach steht B —
während „Bei" **A** bleibt. Die Gegenprobe ist der eigentliche Beleg: ohne die Leer-Prüfung im
P9-Z-Zweig springt der Assignee einer A zugewiesenen Aufgabe von `alpha` auf `beta`. **Zwei
Bestandstests kamen mit:** einer in `test_app.py` (exakte Quittungs-Assertion) und einer, der
**datiert zugeschnitten statt entfernt** wurde (`test_step_f_schema.py` — er verbot jedes
`doing`/`assignee` in `editor.js`, P9-Z verlangt genau das Gegenteil); dazu ein Fund drei
Phasen entfernt: eine Test-Attrappe für `Store.move()` mit eigener Signatur wurde vom neuen
`actor=`-Keyword zu einem HTTP 500 mitten im Space-Entfernen — **ein optionales Keyword
hält Aufrufstellen heil, nicht Attrappen mit eigener Signatur.** **Eine Plan-Klammer war
ungenau** (POST verwirft `updated_by` lautlos statt 422; PATCH und der Kern lehnen ab) und
**eine Datei mehr als geplant** (`mcpserver/receipts.py`, weil die Standard-Schreibantwort die
Quittung ist). **Nächster Schritt (Nikinger):** Release-Commit (Badge + `UPDATE_LOG`) und
Deploy **`v3.1.1`**, danach A7+A8 in einer Sitzung. Details: `phase9_hardening/CLAUDE.md`.

**[2026-10-02, Gate/Z-Doku-Hälfte — die zwei benannten Softcap-Überschreitungen sind weg, und ein Rotationsskript hat beim ersten echten Lauf die Hälfte seiner Arbeit als Erfolg gemeldet — opencode/M3 — ein Commit, kein Deploy, kein Code-Touch, kein Service-Touch.]** Kein Code-Schritt war offen; die Posten der Übergabe, die nicht dem Nikinger gehören, waren Doku-Arbeit. Also die Doku-Hälfte von Gate/Z, und zwei **Section-Rotationen** statt eines Kürzens: `phase1_storage/CLAUDE.md` §„Geerbte Contracts“ (388 Zeilen / 31.422 B) → `CONTRACTS_ARCHIVE.md`, `phase5_ui/CLAUDE.md` §„Abnahmestand“ (99 Zeilen / 12.195 B, inkl. der Kurzfassung, der beiden späteren Nachträge (2026-08-13-Korrektur, 2026-10-02 trace-Block) und der Cutover-Notiz) → `ABNAHME_MATRIX_ARCHIVE.md`. Beide **verbatim** (`python`-Schnitt, Roundtrip-Gegenprobe vor dem Schreiben, byte-identitäts-Gegenlesen danach), beide neu mit L1-Card, beide mit INDEX-Zeile im selben Commit. In den **Heads bleibt genau das, was jemand zum Entscheiden braucht**: die Abschluss-Zusicherung im Wortlaut („Eine Änderung daran nach Phasenabschluss ist eine Scope-Änderung“) plus ein Index der Öffnungen — und der **Abschnittsname bleibt stehen**, weil `phase6_shares_plan.md`, `PHASE7_CLOSEOUT_HANDOVER.md` §4, P8-M und die P9-Pläne wörtlich auf „§Geerbte Contracts“ verweisen; ein toter Verweis wäre eine stille Lüge im Doku-Layer. **47.570 → 20.212 B** und **43.801 → 33.126 B**: beide Überschreitungen betreffen geschlossene Phasen und sind damit Pflichtpflege einer laufenden Phase (so hat es die Übergabe benannt, und `phase1_storage/CLAUDE.md` hatte die Lösung seit 2026-09-30 selbst notiert).

**Der Fund ist der Grund, warum diese Session einen Test und keine nur eine Drehung hinterlässt.** Der erste echte Lauf von `scripts/rotate_index_updates.sh` (P9-L, 2026-09-30 gebaut) meldete „Split ist verlustfrei“ — und rotierte **1 von 3** Einträgen der INDEX-`updated:`-Kette. Der Split-Anker ist `' | (?=\d{4}-\d{2}-\d{2})'`; einer der Fäden begann mit **`updated: `**, sieht für den Anker also nicht wie ein Kettenanfang aus und blieb stehen. „Verlustfrei“ war die Aussage nur *innerhalb* des geschnittenen Teils — die Kette sah danach konform aus, also hätte niemand nachgesehen. **Siebte Wiederholung derselben Repo-Lehre**, und die bisher teuerste: ein Wächter, der die Richtigkeit *seiner eigenen* Byte-Bilanz meldet. Gebaut: **Gegenprobe (e)** im Skript (abbruch mit klarer Meldung, wenn die Kette ein zweites `updated: `-Präfix trägt) und **zwei Tests** — einer prüft den Abbruch, einer ist die Gegenprobe, dass ein sauberer Lauf *alle* älteren Fäden rotiert (sonst könnte (e) auch alles ablehnen und niemand merkte es). **Gegenprobe am Wächter selbst:** (e) entfernt → genau der Abbruch-Test rot. Das Fremd-Präfix kam aus Handarbeit und steht in **derselben Form bis heute in der `updated:`-Kette der Wurzel-`CLAUDE.md`** — dieselbe Ursache, andere Datei, dort nicht rotierbar und deshalb hier nur benannt.

**Nicht getan, mit Zahlen statt Bauchgefühl:** `phase9_hardening/CLAUDE.md` steht nach Rotation **über** dem Softcap (44.360 B). Der Rest ist der Modulstatus (18.217 B) mit **7.467 B durchgestrichenen Statusabsätzen** — überholte Zustände („install + P9-19 ausstehend“), deren Befund die aktuelle Spalte schon trägt. Streichen brächte den Head sicher unter die Grenze, ist aber eine **Nikinger-Entscheidung**, weil es 7 KB aus dem Head der *laufenden* Phase nimmt ⇒ **vorgeschlagen, nicht getan**. Ebenso unangetastet: die Wurzel-`CLAUDE.md` selbst (**~103 KB**, davon §Current state der Löwenanteil — benannte Lösung ist die Rotation der Current-state-Abschnitte nach `docs/PROJECT_SESSION_LOG.md`; die exakte Bytezahl steht in der INDEX-Zeile, hier absichtlich gerundet, weil jeder Eintrag in diesem Absatz die Zahl sofort wieder veraltet) und `docs/INDEX.md` (**~57 KB, heute größer als vorher**: zwei Pflicht-Zeilen für die neuen Archive +1.432 B, Ketten-Rotation −347 B netto, dieser Eintrag +~1,3 KB — **gemessen und benannt statt als Erfolg verbucht**). Alle drei bleiben **benannt statt versteckt** (P8-P).

**Eigener Fehler, im selben Commit behoben und hier genannt, weil er eine Lehre trägt:** mein erster INDEX-Schreibvorgang hat die Datei **um 13,5 KB gekürzt** — `t[:i] + neu + t[i:j][…]` ohne `+ t[j:]`. Der Schnitt war als Trockenlauf mit einer *Größen*-Erwartung abgesichert, und die expectation traf zu: die Datei wurde kleiner. Richtig wäre eine **Struktur**-Erwartung gewesen (Zeilenzahl, Linkziele, Frontmatter), nicht eine Größe — die wäre bei einem *echten* Kürzen derselbe Fehler durchgegangen. `INDEX.md` wurde aus `HEAD` reproduzierbar neu gebaut (alle Schritte sind Skript-Aufrufe), das Archiv des Rotationslaufs war dabei zweimal dupliziert und wurde bereinigt (Gegenprobe: jeder Faden genau einmal).

**Selbstprüfung:** `doc_health` 0 Befunde (dazwischen die zwei erwarteten „keine Zeile in docs/INDEX.md“ für die neuen Archive, nach deren Eintrag wieder 0) · `pytest` **1152 → 1162** (10 neu: 2 für die Skript-Gegenprobe (e) + 8 Rotations-Wächter in `phase9_hardening/tests/test_doc_rotations.py` — **Gegenprobe: fünf eingebaute Verstöße → fünf rote Tests**; ein erster Entwurf schrieb *2* und wäre bei einem echten Kürzen derselbe Fehler gewesen) · `ui_budget` 5/5 unberührt (kein `phase5_ui/webui/static/**`-Touch) · Tabu-Diff auf die sechs Hartpfade **leer** · kein `systemctl`, kein `pkill -f`, keine Wegwerf-Instanz, `sharefyx-mcp` nicht berührt.

**Sichtung vom 2026-10-02: abgenommen, mit Restbefund** — der Nikinger hat die sechs `p9_trace_*`-Bilder freigegeben **mit der Notiz, dass noch nicht alle Knöpfe an das Schema angepasst sind.** Das ist als **B17** im Backlog von `phase9_hardening/CLAUDE.md` abgelegt, und zwar **mit der gemessenen Liste** statt allgemein: von 77 Knöpfen im Markup laufen **62 auf den Standard-Tokens** `--btn-std-*`; **15 nicht** — `.btn-primary` (13) auf `--accent-face-*` und `.btn.action--caution` (2) auf der **alten** `--btn-face-*`-Familie, die der btn2-Block für `.btn` abgelöst hat. **Kein Renderfehler** (alle Tokens definiert, 0 verwaiste `var()`), also Konsistenz-Lücke; ob die beiden Klassen semantisch abweichen *sollen* (Konvention v3: Aktion vs. Vorsicht), ist offen und bleibt es — **kein Code in dieser Session angefasst**.

**B17 ist als potentieller Extra-Schritt dokumentiert** (Phase-9-Head, Modulstatus-Zeile „E (Extra)“), **nicht entschieden** — der einzige Punkt, der ohne deine Infra-Schritte liegen bleiben kann.

**Nächster Schritt, weiterhin Nikinger:** (1) ~~Sichtung~~ **erledigt 2026-10-02**; es bleibt (2) **Release-Commit + Deploy `v3.1.1`** — Badge und `##`-Block müssen **am Deploy-Tag** entstehen, ein heute datierter Block ließe das `deploy.sh`-Gate (P6-X) bei einem späteren Deploy abbrennen; (3) **A7+A8 in einer Sitzung** (Befund 4: der A7-Restart kappt beide Connectoren), danach ist SP9-10b geschlossen und der Warndialog auf der alten Funnel-Adresse darf sterben. Danach der Rest von Gate/Z: Abnahmematrix P9-1–P9-82 und die `[VERIFY]`-Bilanz V145–V184. Details: `phase9_hardening/CLAUDE.md`.

**[2026-10-02, P9 B17 gebaut — deine Sichtprüfungs-Notiz war ein Knopf, nicht fünfzehn, und die
Zahl im Backlog war falsch — opencode/M3 — ein Commit, kein Deploy, kein Service-Touch.]** Die
Sichtung vom 2026-10-02 hatte als Restbefund notiert, „noch nicht alle Knöpfe ans Schema
angepasst", und der Backlog daraus maß **15 Knöpfe** in zwei Klassen. **Vor dem Bauen gemessen, nicht
geglaubt** (Markup *und* CSS): es war **ein** Knopf mit einem Befund. `.btn.action--caution` trägt
**1** Fläche, nicht 2 — der Selektor matcht nur `#archive-button`; der zweite Träger
`#logout-button` ist ein `.rail__action` (`background: none`) und trägt die Vorsicht nur an der
**Farbe**, er hatte nie eine Fläche. Und die **13** `.btn-primary` sind **kein Reststand**, sondern
deine dokumentierte Ausnahme vom 2026-10-01. **Dasselbe Zählen über Klassen-Präsenz statt über den
Selektor** wie beim btn2-Fund mit `count() == 1` für `[aria-current]`.

**Der Befund, der beim Messen entstanden ist, war eine Helligkeit, kein Token:** `--btn-face-top`
`#2A313A` ist **heller** als die Standardfläche `--btn-std-fill` `#0C1C31`. „Vorsicht" war damit der
**auffälligste** Knopf der Editor-Fußzeile statt des Standards — das Gegenteil dessen, was der
Wächter beschrieb, dessen Namen ich deshalb **datiert umgedreht** habe (mit beiden Richtungen im
Docstring, Muster wie beim doing-Wächter desselben Tages). Gebaut ist die kleinstmögliche Änderung:
die drei `.btn.action--caution`-Regeln sind **gelöscht**, nicht umgeschrieben — `.btn` *ist* die
Standardfläche, und eine eigene Kopie davon wäre die „zweite Knopfoptik im selben Panel", die
derselbe Tag am 2026-10-01 an `.account-nav` abgestellt hatte. `:root` unberührt, kein Token verwaist,
die alte Familie hängt jetzt **badge-only** am `.rail__glyph`.

**Und ein Lock-Konflikt, den ich zurückgestellt habe, statt ihn stillschweigend zu brechen.** Mein
Vorschlag war eine eigene, rot getönte Flächenfamilie `--caution-std-*` (deckend, dunkel — die
„Vorsicht-Farbtiefe" des Standards). Du hast sie gewählt; beim Vorbereiten des Blocks stieß ich auf
zwei gelockte Zeilen, die sie bricht: die Selection/Choice-Konvention v3 sagt wörtlich *Standard-
Knopfplastik, aber `color: var(--caution)` auf Label und Glyph; **keine** gefüllte rote Fläche*, und
deine P9-Notiz vom 2026-10-01 führt `.action--caution` als Ausnahme, die „behält die graue Plastik".
**Eine rot getönte Fläche *ist* die gefüllte rote Fläche** — das war keine Interpretationsfrage.
Nach der Rückfrage: **exakt die Standardfläche**, wortgleich v3, ohne Konventionsänderung. Beide
Stellen in `phase8_ui_graph/CLAUDE.md` sind datiert korrigiert (die Konvention war zwischen dem
2026-10-01 und dem 2026-10-02 tatsächlich **nicht eingehalten**, und das steht jetzt dort).

**Belegt, nicht behauptet:** **3 Wächter** in `phase5_ui/tests/test_static_routes.py` (1 umgedreht,
2 neu: einer zählt die **Markup**-Träger, damit „keine eigene Fläche" nicht vakuös grün ist, der
andere macht die alte Familie badge-only und strippt vorher die Kommentare) · **Gegenprobe 4
eingebaute Verstöße → 8 rote Assertions**, Kontrolllauf 0, danach byte-identisch wiederhergestellt ·
**Pixel-Probe `p9_btn3_caution_probe.py` 14/14** gegen eine eigene TLS-Wegwerf-Instanz (Port 18775,
über die **PID-Datei** gestoppt, kein `pkill -f`): die berechneten `backgroundImage`-Strings sind
stringgleich, vier Pixelproben an der glyphenfreien Spalte mit **max |Δ| = 1**, die Vorsichtfarbe
sitzt in der Beschriftung. **Gegenlauf:** alte Fläche zurück → 6 von 13 Stationen rot, Δ 25–28.
**Drei eigene Fehler, alle im selben Commit behoben:** mein `.btn`-Kommentar enthielt eine `{ }`-
Klammer (`_block_body` schneidet mit `[^}]*`, er schnitt mir den Block ab) **und** hätte den neuen
Vorschrift-Wächter grün gemacht, weil er `color: var(--caution)` im Klartext *nennt* — der Wächter
strippt jetzt die Kommentare vorher, sonst hätte ich beim siebten Mal dieselbe Repo-Lehre gebaut. Der
Dateiname des ersten Bildes behauptete „footer" und zeigte die Formatierleiste; die Aufnahme ist jetzt
der Zuschnitt der Knopfleiste. Und der **Vision-Adapter** hat dasselbe Bild **vertaucht** (rote
*Beschriftung* als roter Hintergrund, „Speichern" hellgrau) — das ist als **eigene Fehlerklasse**
dokumentiert: ein VLM ist als Farbmessgerät an *einem* Element brauchbar, als **Zuordner über mehrere
Elemente** unbrauchbar (neue Zeile in
`docs/concepts/sichtpruefung_automation_tooling.md`).

**Selbstprüfung:** `pytest` **1167 → 1169** (Baseline vorab gemessen, nicht aus der Doku übernommen) ·
`ui_budget` **5/5**, und die Zahl **per Stash-Gegenprobe gemessen**: **165,0 KB auf HEAD gegen 165,2 KB
mit diesem Block** — die hier protokollierte **155,1 KB war also schon veraltet**, sie stammt aus dem
trace-Block; mein Anteil ist +0,2 KB · `doc_health` **0** · Tabu-Diff auf die sechs Hartpfade leer.

**Benannt, nicht entschieden:** der Kontrast der Vorschrift-Beschriftung liegt bei **4,38:1** (vorher
3,36:1) — besser und **weiterhin kein WCAG-AA** (4,5:1 für normalgroßen Text, 14 px/500 ist kein
„large text"). Ich habe ihn als *Verschlechterungsverbot* in die Probe genommen, nicht als
Bestandenheitsschwelle; hellere Schrift oder eine 1-px-Kante sind deine Design-Entscheidung.

**Doku-Hygiene:** Phase-9-Head 53.968 B (Rotation des dreizehnten Blocks per Skript, **53.968 B =
13.008 B über dem Softcap, benannt statt versteckt** — die 7.467 B durchgestrichenen Statusabsätze im
Modulstatus habe ich **nicht** angefasst, das bleibt deine Entscheidung), `docs/INDEX.md` **60.793 B
(≈60 KB)** — fünf Pflichtzeilen nachgezogen, darunter die `phase8_ui_graph`-Zeile, die **schon auf
HEAD** über der Grenze lag (45.365 B) und nur noch im Toleranzfenster des Wächters stand,
`screenshots_latest/` auf die vier B17-Belege rotiert (die sechs `p9_trace_*` sind abgenommen und
versioniert) — alles im selben Commit.

**Nächster Schritt, unverändert deine Zuständigkeiten:** (1) **Release-Commit + Deploy `v3.1.1`** —
Badge `app.html:20` + `##`-Block in `docs/UPDATE_LOG.md`, **beides erst am Deploy-Tag**, sonst
brennt das `deploy.sh`-Gate P6-X ab; dieser Block kommt mit, ist aber eine reine CSS-Änderung und
braucht **keinen** Index-Neuaufbau. (2) **A7+A8 in einer Sitzung** (Befund 4: der A7-Restart kappt
beide Connectoren), danach ist SP9-10b geschlossen. (3) Danach der Rest von Gate/Z: Abnahmematrix
P9-1–P9-82 und `[VERIFY]`-Bilanz V145–V184.

**[2026-09-10, P8.6 Open Item #5 — Aktionsliste Schritt 7 auf Restart-Logik verkürzt; nur Doku, kein Code-Touch.** Restart-Logik verifiziert durch Lesen von `/etc/systemd/system/sharefyx-mcp.service` (`Restart=on-failure` + `RestartSec=5`) und `/usr/lib/systemd/system/tailscaled.service`; beide `WantedBy=multi-user.target`. Tabu-Diff §0.3 leer, Service-Touch 0 — sharefyx-mcp PID 991 unverändert.

**[2026-09-10, P8.6 Step 0] Haushalt der neuen aktiven Phase 8.6 ausgeführt (Phase 8.5 abgeschlossen, Phase-8.6-Plan ausgeführt).** Plan §1.10 wörtlich umgesetzt: Phasenverzeichnis `phase8_6_ui_polish/` mit `CLAUDE.md` (~22 KB, mit Mission/Scope/Harte Regeln/Modul-Status 0–Z/Baselines V97/V107/V108/Vormerkungen/Step-0-Session-Block) + `SESSIONS_ARCHIVE.md` (📦 leer, mit L1-Card) + `scripts/` (leer, Wegwerf-Smokes folgen in Gate/§7) angelegt. **Sieben Befunde behoben:** (1) sechs unauflösbare `up:`/`down:`-Links — alle sechs in `p8x_ui_polish_notes.md`, von 187 Frontmatter-Links im Repo die einzigen kaputten (`../` → `../../`); (2) vier fehlende L1-Header-Cards ergänzt (`docs/PROJECT_SESSION_LOG.md` L3-Archiv-Card, `phase8_5_picker_release/{SICHTPRUEFUNG_RESTBLOCK,SICHTPRUEFUNG_WALKTHROUGH,CLUSTER3_TESTBLOCK}.md`); (3) drei `down:`-Listen vom Inline-Format (`·`-Trenner) auf Listenform (`phase6_5_tools_images_plan.md`, `phase6_shares/{GLOBAL_SEARCH,IMAGES}_PLAN.md`); (4) zwei fehlende INDEX-Zeilen ergänzt (`CLUSTER3_TESTBLOCK.md`, `THIRD_PARTY_LICENSES.md` mit Ausnahme-Markierung); (5) zwei INDEX-Drift-Korrekturen (`phase8_ui_graph/CLAUDE.md` bekommt die Softcap-Notiz wie `phase6_shares`, `phase5_ui/CLAUDE.md` verliert die falsche „über dem 40-KB-Softcap"-Aussage — real 40.957 B = 3 B unter Cap); (6) **`docs/INDEX.md` von 40.960 B auf 37.763 B** komprimiert (Plan-Zeilen P8.6/P8.5/P8/P7/P6/P6.5/P5/P4/P3/P2 auf Pointer-Form gestrafft — L0 ist Landkarte, keine Kurzfassung, Plan §1.5); (7) zwei echte Code-Defekte **dokumentiert, hier nicht behoben** (`var(--border-soft)` undefiniert an `app.css:1270/1276` → Block A §3.3, `graph.js :: runSimulation()` `rafId` lokal aber nie gelesen → Block D §6.4). **Verifikation:** Repo-weiter `up:`/`down:`-Link-Scan über 203 .md-Dateien **0 Fehler**; `find … -size +40k` für `docs/INDEX.md` ergibt nichts. **Selbstprüfung:** `pytest` **964/964** (V107 ✅), `ui_budget.py` **5/5, 130,1 KB** (V97 ✅), **V108 `_overview` ~863 ms offen** (vor Block C drei Läufe mitteln — Plan §1.7), **kein Code-Touch** (Tabu-Diff §0.3 leer), **Service-Touch 0** (PID 355956 nur gelesen, keine Wegwerf-Instanz gestartet — Step 0 ist Doku + Skelett, kein Lauf gegen den Server). **Nächster Schritt:** **Step V — OpenCode-Vision-Plugin-Installation** (`DavidEasden/opencode-vision`, Plan §2, Nikinger-Vorgabe 2026-09-08 „erster Punkt vor jedem Code-Touch"); bei Plugin-Repository-Konfig oder Authentifizierung **vor** der Installation fragen, nicht im Trial-and-Error. Step 0-Commit-Message wörtlich aus Plan §1.10: `phase 8.6: Step 0 -- Haushalt, sechs kaputte Doku-Links, vier fehlende L1-Cards, INDEX-Kompression`.

**[2026-09-09, P8.6-Planungssession] Phase 8.6 geplant und ausführungsreif — Reichweite vom Nikinger aus vier geschachtelten Bündeln gewählt, drei offene Entscheidungen des P8.5-Handovers gelockt, sieben Step-0-Befunde gemessen statt geraten.** Neu: `docs/concepts/phase8_6_ui_polish_plan.md` (~66 KB, 📕-Snapshot, gegen `main@d1af51b`), Verzeichnis gelockt als **`phase8_6_ui_polish/`** (P8.6-A), Deploy-Ziel `v3.0.2`. **Reichweite „Selektions-Welle + Layout"** (N1): §5 Layering-Tokens + §10.1–§10.7 Selektions-Vereinheitlichung + §6 „Konto"→„Einstellungen" (Lesart b: Einstellungen nach oben, Abmelden ans Rail-Ende) + §3 Ordner-Zähler + §1 Rail-/Übersichts-Reorg + §10.4 klickbare Spaces + §2.3/§2.4 Map-Fixes + Radiogruppe-Rückbau auf `<select>`. **Drei Nikinger-Entscheidungen:** (1) **es gibt kein P8.7** — sein „eher v3.1 also p8.7" meint das dokumentierte **P9 → `v3.1.0`**, die AI-Sessions-Anzeige ist damit P9-Inhalt, umbenannt wurde nichts; (2) **V102 dedupliziert im Frontend** (`graph.js:156`, bei der Übernahme statt in `drawEdges()`) — bewusst **keine neunte P1-Contract-Öffnung**, `storage/` bleibt in P8.6 unangetastet; (3) **§10.7 wird eine fünfte Konventions-Kategorie „Vorsicht"** statt zweier Einzelfälle, umgesetzt als `--caution: var(--danger)` — derselbe Wert, zweiter Name, weil der Kommentar an `--danger` (`app.css:57`) die Kategorie längst benennt („Widerruf, Archivieren"). **Step 0 wurde in dieser Session bereits durchgeführt, die Befunde stehen im Plan §1:** sechs unauflösbare `up:`/`down:`-Links — **alle sechs in `p8x_ui_polish_notes.md`**, ausgerechnet der Inhaltsquelle der Phase (`../` statt `../../`); von 187 Frontmatter-Links im ganzen Repo sind das die einzigen kaputten. Vier fehlende L1-Header-Cards, zwei fehlende INDEX-Zeilen, drei `down:`-Cards im Inline-
statt Listenformat (deren Ziele auflösen — der Befund ist der Prüfer, der sie **still
überspringt** und trotzdem „sauber" meldet). **Und ein stiller Softcap-Verstoß:**
`phase8_ui_graph/CLAUDE.md` liegt mit 42.343 B über dem Cap und ist — anders als
`phase6_shares/CLAUDE.md` — **nirgends als Ausnahme benannt**; die Konvention duldet einen
benannten Verstoß und verbietet einen stillen. Umgekehrt behauptet die INDEX-Zeile von
`phase5_ui/CLAUDE.md` seit dem 2026-08-28, die Datei liege über dem Cap — sie liegt mit
40.957 B **darunter**. **Zwei echte Code-Defekte:** `var(--border-soft)` ist an `app.css:1270/1276` referenziert, aber **nirgends definiert** — nach CSS-Spezifikation wird die `border`-Kurzform damit ungültig und `.link-picker-results` zeichnet **gar keinen** Rahmen; und `graph.js :: runSimulation()` pflegt ein lokales `rafId`, das es nie liest — es gibt kein `cancelAnimationFrame`, also stapeln wiederholte Übersicht-Klicks nebenläufige `tick()`-Schleifen. **Zwei Baselines gemessen, nicht geschätzt:** `pytest -q` **964 passed in 257 s** (mit ausgehängten `SHAREFYX_*`/`SFX_*`) und `ui_budget.py` **5/5**, 130,1/250 KB — damit sind **V97 (geerbt) und V107 geschlossen**. **`docs/INDEX.md` ist praktisch voll:** sie stand auf exakt 40.960 B, und schon die *eine* Zeile für diesen Plan erzwang das Straffen von drei anderen Einträgen; es bleiben **32 Byte Luft**, der Head- und Archiv-Eintrag der Phase passen nicht mehr — Step 0 hat den ausdrücklichen Auftrag, auf ≤38 KB zu komprimieren. **Kein Code-Touch**, Tabu-Diff §0.3 leer, **Service-Touch 0** (Produktions-PID 355956 nicht angefasst, keine Wegwerf-Instanz gestartet). **Nächster Schritt:** Ausführung in opencode/M3 nach Plan §1–§8, Reihenfolge Step 0 → Step V (Vision-Plugin) → Block A → B → C/D → Gate → Deploy → Step Z; der Closeout wird Plan **§9**.

**[2026-09-09, Phase-8.5-Z-Closeout] Phase 8.5 mit Step Z vollständig abgeschlossen — Übersichtsgrafik und Handover als bewusste Umkehr zweier eigener Locks, Plan §9 gefüllt, vier Doku-Drifts behoben.** Der Phasen-Abschluss-Prompt lief zum ersten Mal gegen eine Phase, die ihre eigenen Closeout-Artefakte ausgeschlossen hatte: **P8.5-S** („keine Übersichtsgrafik") und **P8.5-R** („kein neues Handover-Dokument") standen seit dem 2026-09-03 gelockt im Plan. Der Nikinger hat beide im Closeout-Auftrag selbst aufgehoben — beide tragen jetzt eine durchgestrichene Altfassung plus datierte Korrekturnotiz in `docs/concepts/phase8_5_picker_release_plan.md` §0.2; **P8.5-T bleibt unangetastet**, §9 ist gefüllt und bleibt der kanonische Closeout, das Handover verweist darauf statt es zu ersetzen. **Neu:** `docs/concepts/phase8_5_picker_release_uebersicht.svg` (1080×1080, headless-Chromium gerendert und visuell gegengeprüft) + `docs/concepts/PHASE8_5_CLOSEOUT_HANDOVER.md` (Einstieg für die P8.6-Planung, §4 = offene Entscheidungen, §5 = `[VERIFY]`-Bilanz V95–V105). **Vier Drifts im selben Commit behoben:** Modul-Status-Zeilen 2–7 standen auf 🟡/⬜, während der Abnahmestand darunter 20/20 ✅ meldete; Plan §9 war leer, obwohl P8.5-T ihn als Closeout festlegt; Modul-Status Zeile 2 nannte `<select>` statt der seit dem 2026-09-07 gebauten Radiogruppe; `p8x_ui_polish_notes.md` §A führte die vierte A3-Probe noch als „wird in D5 entschieden" (sie lief am 2026-09-08, ✅). **Neun Nikinger-Feedback-Punkte** sind als `p8x_ui_polish_notes.md` **§10** abgelegt (Zitat + Code-Anker, ungewichtet) — sieben davon Verschärfungen von §5/§6; **§B: die Mobile-Hälfte der Außenkante „Mobile/Realtime" ist datiert aufgehoben** (Hochkant-UI wird benanntes Zukunfts-Item, Realtime bleibt draußen); die Nummern-Frage „eher v3.1 also p8.7" gegen die dokumentierte Reihe P8.6 → `v3.0.2` / P9 → `v3.1.0` wurde **bewusst nicht selbst entschieden**. **Rotation:** der Head trug einen `## Session stopped` mit zwei datierten `###`-Unterblöcken — `scripts/rotate_session_block.sh` zählt `##`-Überschriften und hätte „bereits konform" gemeldet; rotiert wurde per `sed`-Schnitt mit dreifacher `cmp`-Gegenlesung, dazu 19 von 22 `updated:`-Frontmatter-Einträgen verbatim ins Archiv (**Head 52.6 → 26.0 KB**, Archiv 172 → 205 KB, INDEX erstmals wieder unter dem Softcap mit 40.9 KB). **Kein Code-Touch**, pytest **964/964** (267 s), Tabu-Diff §0.3 leer, Service-Touch 0 (PID 355956, 3 Tage Uptime, nur gelesen). **Nächster Schritt:** P8.6-Planungs-Session in Claude Code — Einstiegsdokument ist das Handover §4, erster Punkt der Phase bleibt die OpenCode-Vision-Plugin-Installation.
**[2026-09-09, P8.5-6-Folge-Smoke] Bracket-Pfad live-verifiziert, Bilanz 19/1/0 → 20/0/0, Phase 8.5 vollständig abgeschlossen.** v3ritt-Wegwerf frisch hochgefahren (PID 461074, Port 18773, eigener tmp-`DATA_ROOT`), Item `itm_b8b989a1` „Vercel [Hosting]" via `storage.Store.create()` in alpha angelegt, neuer Mini-Smoke `phase8_5_picker_release/scripts/p856_bracket_mini_smoke.py` (~75 Z., Playwright) führt den kompletten P8.5-6-Bracket-Pfad aus — Login + Edit-Mode + Picker + Link einfügen + **zwei Screenshots** (`p856_bracket_edit_view.png` mit `\[…\]`-Escapes im Quelltext + `p856_bracket_preview.png` mit „Vercel [Hosting]" als **klickbarem blauen Hyperlink**), programmatische Quittung per Regex auf `<a href="#item/itm_b8b989a1">Vercel [Hosting]</a>` True. Wegwerf sauber per PID-Datei gestoppt (kein `pkill -f`); Production-PID 355956 unverändert. **Phase 8.5 ✅ formal vollständig abgeschlossen.** **Doc-Updates in diesem Commit:** `phase8_5_picker_release/CLAUDE.md` §Abnahmestand Bilanz → **20/0/0**, §Nächste Session auf P8.6-Planung umgeschrieben, Sichtungs-Session-Block um P8.5-6-Folge-Smoke ergänzt (kein neuer Block, Konvention „genau ein Session-Block" gehalten); `phase8_5_picker_release/SESSIONS_ARCHIVE.md` Matrix-Zeile P8.5-6 auf ✅ mit Folge-Smoke-Beleg, §Abnahmematrix-Archiv-Header aktualisiert; `docs/INDEX.md` + `docs/ROADMAP.md` Frontmatter-updated. **Kein Code-Touch**, pytest unverändert 964/964, Tabu-Diff §0.3 leer, Service-Touch 0 (Production-PID 355956 unverändert). **Nächster Schritt:** P8.6-Planung in Claude Code mit OpenCode-Vision-Plugin-Installation als erstem Punkt — neue Konvention §4 aus den Sichtungs-Sub-Sessions greift dort sofort.
**[2026-09-09, Sichtung 10 P8.5-🟡] 9 von 10 Zeilen auf ✅, P8.5-6 bleibt 🟡 (Vorschau-Screenshot des Bracket-Pfads fehlt); vier neue Sichtungs-Konventionen notiert (Vorschau-Pflicht / Code-vs-Visuell / Deploy-nach-Test / Screenshots-im-Chat nach opencode-vision-Install).** Methodik: opencode/M3 sichtet die Block-C-Screenshots + Smoke-Asserts + statische Tests grün (Vision über `Read`-Tool), Nikinger bewertet pro Zeile. Nikinger-Vertrauens-Regel: (C)-Code-Test-Beweise sind durch den ausführenden Agenten verifiziert, kein zusätzlicher Sichtungs-Schritt nötig; (W)-Wegwerf-Beweise mit Nikinger-Vertrauen auf dokumentierten Beleg. **Phase-8.5-Bilanz 10 ✅ · 10 🟡 · 0 ⬜ → 19 ✅ · 1 🟡 · 0 ⬜** (P8.5-7/-8/-9/-10/-11/-12/-13/-14/-15 neu ✅; P8.5-6 bleibt 🟡). **Was P8.5-6 zum ✅ braucht:** Mini-Smoke gegen v3ritt-Wegwerf mit `[…]`-Titel-Item + Vorschau-Panel-sichtbar-Screenshot, sodass der gerenderte Link als klickbarer Hyperlink sichtbar wird (statt nur in der Markdown-Quelle). **Oder** direkt Sprung zu P8.6-Planung mit OpenCode-Vision-Plugin-Installation als erstem Schritt — dann eröffnen sich dieselben Sichtungs-Erleichterungen und P8.5-6-Brake-Pfad kann inline mitlaufen. **Doc-Updates in diesem Commit:** `phase8_5_picker_release/CLAUDE.md` §Abnahmestand + §Nächste Session + neuer Session-Block (alter Z-Closeout-Block manuell nach `SESSIONS_ARCHIVE.md` rotiert, Skript passt nicht auf Phase-8.5-Muster mit einem `## Session stopped` + mehreren `### date`-Subblöcken) + 10 Matrix-Zeilen mit Nikinger-Vermerk; `docs/concepts/sichtpruefung_automation_conventions.md` §1-§4 neu; `docs/concepts/sichtpruefung_automation_tooling.md` Plugin-Empfehlung auf P8.6 first step verschärft; `phase8_5_picker_release/SICHTPRUEFUNG_WALKTHROUGH.md` + `SICHTPRUEFUNG_RESTBLOCK.md` Top-Notiz „Vorschau-Pflicht"; `docs/INDEX.md` + `docs/ROADMAP.md` Frontmatter-updated. **Kein Code-Touch**, pytest unverändert 964/964, Tabu-Diff §0.3 leer, Service-Touch 0 (Production-PID 355956 unverändert, keine Wegwerf-Instanzen gestartet).
**[2026-09-08, scope-reversal] Nikinger-Entscheidung: die 10 P8.5-🟡-Sichtungen (P8.5-6, -7, -8, -9, -10, -11, -12, -13, -14, -15 — Browser-verifiziert in Chromium+Firefox, throwaway-qualifiziert, aber Screenshots vom Nikinger noch nicht selbst gesichtet) wandern NICHT nach P8.6, sondern bleiben in Phase 8.5 — als erste Sache der nächsten Session. Anlass: der Z-Closeout-Stand-Summary-Text hatte „Guter erster Kandidat für eine kurze Nachprüfung in P8.6, kein neuer Code nötig — nur eine Sichtung der bereits vorliegenden Block-C-Belege gegen die neue Regel" geschrieben; der Nikinger hat das beim Review umgesteuert (Phase 8.5 hier abschließen, nicht auf eine Folge-Phase schieben). Konkrete Anleitung: `phase8_5_picker_release/SICHTPRUEFUNG_WALKTHROUGH.md` + `SICHTPRUEFUNG_RESTBLOCK.md`. Bei Erfolg: Phase 8.5 springt von 10 ✅ auf 20 ✅ · 0 🟡 · 0 ⬜, Phase 8.5 dann formal vollständig abgeschlossen. Kein Code-Touch, kein Deploy. Phase 8.5 head hat eine neue Sektion „## Nächste Session" bekommen mit den 10 Zeilen einzeln aufgelistet + Werkzeug-Setup-Stand.

**[2026-09-08, Z-Closeout] Phase 8 ✅ + Phase 8.5 ✅ — formal abgeschlossen, Statusregel geändert, zwei Folgephasen (P8.6 → v3.0.2, P9 → v3.1.0) vorgemerkt.** Sichtprüfungs-Automatisierungs-Sub-Session: 9 von 9 Sichtprüfungs-Punkten aus dem D5/Cluster-4/Cluster-5-Restblock durchgelaufen — teils gegen Wegwerf-Instanzen (Canvas-Instrumentierung für den exakten Tag-Kanten-Zähler, CDP-Medien-Emulation für Glass-Fallback, ein neu gebautes Zwei-Principal-Wegwerf-Setup für den echten Zweitnutzer-ACL-Nachweis über OAuth+MCP), teils gegen die echte Produktion (der reconnectete sharefyx-MCP-Connector: `list_spaces` + ein echter claude.ai-Chat des Nikingers, der ein Item korrekt beim Titel statt bei der `itm_…`-ID nannte). **Statusregel-Änderung, Nikinger-Entscheidung:** eine vom Nikinger selbst geprüfte Wegwerf-Instanz-Automatisierung (byte-identischer Git-Checkout wie Produktion, Unterschied nur `DATA_ROOT`/`auth.sqlite3`/Identität) zählt jetzt als „live-verifiziert" — Details, Begründung, wiederverwendbare Techniken: `docs/concepts/sichtpruefung_automation_conventions.md` (neu, samt Schwester-Datei `sichtpruefung_automation_tooling.md` für Werkzeug-/Plugin-Empfehlungen). Phase-8-Bilanz **26 ✅ · 0 🟡 · 0 ⬜**, Phase-8.5-Bilanz **10 ✅ · 10 🟡 · 0 ⬜** (die verbleibenden 🟡 sind Block-C-Belege von 2026-09-04, die der Nikinger unter der neuen Regel noch nicht gesichtet hat — kein neuer Code nötig, nur eine Sichtung). Drei Wegwerf-Instanzen (200-Knoten, D2, das neue Zwei-Principal-Setup) sauber abgebaut, PID-Datei-basiert, kein `pkill -f`, Produktion durchgehend unangetastet (PID 355956). **Zwei Folgephasen besprochen, noch nicht geplant:** **P8.6** (Arbeitsname, → `v3.0.2`) bündelt die restlichen `p8x_ui_polish_notes.md`-Punkte + einen Radiogruppe-Rückbau auf `<select>` (Nikinger kehrt seine eigene D4-Entscheidung um, Design-Konsistenz) — **erster Punkt darin: das OpenCode-Vision-Plugin installieren** (`DavidEasden/opencode-vision`), damit künftige Sichtprüfungsrunden davon profitieren; **P9** (Arbeitsname, → `v3.1.0`) ist der Obsidian-Map-/Graph-Umbau, laut Nikinger voraussichtlich der letzte große UI-Umbau. Volle Herleitung, Matrix-Zeilen, Screenshots: `phase8_ui_graph/CLAUDE.md` §Abnahmestand, `phase8_5_picker_release/CLAUDE.md` Abnahmestand + „Nächste Phasen"-Abschnitt.

**[2026-09-08, Folge 2] Phase 8.5 — 🔄 Doku-Sub-Session: freundlicher Walkthrough für die Sichtprüfung geschrieben, ⬜ Sichtprüfung selbst durch Nikinger.** Auf Bitte des Nikingers nach mehr Detailtiefe: neue Datei `phase8_5_picker_release/SICHTPRUEFUNG_WALKTHROUGH.md` (29 KB / 727 Zeilen) als **Geschwister** zum bestehenden technischen `SICHTPRUEFUNG_RESTBLOCK.md`. Walkthrough-Struktur: Vorbereitung (drei Tabs + Connector), dann pro Schritt "Was tust du" + "Was siehst du" + optionale DevTools-/Console-Befehle + Pass/Fail-Beschreibung. Deckt C4-0 (P8-16 Glass-Fallback via Rendering-Tab), C4-1 (P8.5-19 Radiogruppe mit `localStorage`-Cross-Check), C4-2 (P8.5-3+4 Hint + Vierte A3-Probe — Tipp: jede Form in eigene Anfrage packen, damit der Connector nicht alle vier vereint), C4-3 (P8.5-17 V105 Connector-Check), C3-1 (P8-21d Tag-Cutoff mit Console-Cross-Check `fetch('/api/v1/graph').then(g => g.edges.filter(e => e.kind === 'tag').length)`), C3-2 (P8-22 mit Stoppuhr-Anleitung für Settle-Zeit < 3 s), C3-3 (P8-24 E2E-Ritt gegen D2 in sechs Stationen), C5-1 (P8-5 = C4-2), C5-2 (P8-8 mit Fabian-Koordination). Login-Snippet und TOTP-Secrets am Dateiende noch einmal komplett. Ergebnis-Tabelle zum Ausfüllen mit Bestanden-Spalte pro Punkt + Notizen-Feld für Restdefekte. **Kein Code-Touch**, **pytest 964/964 unverändert**, **Tabu-Diff §0.3 leer**, **Service-Touch 0**. **Größen-Stand:** Walkthrough **29 KB** neu (separate Datei, kein Softcap-Druck); Phase-8.5-Head jetzt **~80 KB** (drei Sub-Sessions vom 2026-09-08 im Head — Phase-8.5-Muster mit `## Session stopped` + mehreren `### date`-Subblöcken ist etabliert; weiter deutlich über 40-KB-Softcap, Auflösung bleibt Z-Arbeit); `docs/INDEX.md` ~64.8 KB. **Nächster Schritt:** Nikinger-Live-Sichtprüfung mit dem Walkthrough am Bildschirm (~12 Min ohne Fabian, ~22 Min mit). Nach dem Lauf: Status-Updates der Phase-Heads + INDEX + Commit + Cleanup-Befehle (Hard Rule 9, PID-Datei-basiert). **Danach: Z** (Phase-8.5-Closeout).

**[2026-09-08, Folge] Phase 8.5 — 🔄 Doku-Sub-Session: Restblock-Sichtprüfungs-Testblock geschrieben + D2-Wegwerf parallel hochgefahren, ⬜ Sichtprüfungen selbst durch Nikinger.** Zusätzlich zum 200-Knoten-Wegwerf (Port 18772, PID 436596) wurde der **D2-Wegwerf hochgefahren** auf Port 18768 (PID 438765, 14 Knoten, 6 Kanten — der richtige Datensatz für P8-24, weil der 200-Knoten-Datensatz für Station-3-Idempotenz bei `DEFAULT_LIMIT=50` driftet). Beide Wegwerf-Instanzen laufen jetzt parallel, Production-Dienst unverändert (PID 355956). **Neue Datei `phase8_5_picker_release/SICHTPRUEFUNG_RESTBLOCK.md`** (27.5 KB, 471 Zeilen) — der konsolidierte Schritt-für-Schritt-Testblock für **alle restlichen Sichtprüfungen**: Cluster 3-Rest (Phase 8) P8-21 d + P8-22 + P8-24 gegen die zwei Wegwerf-Instanzen, Cluster 4 (Phase 8.5) P8-16 + P8.5-3 + P8.5-4 + P8.5-17 + P8.5-19 gegen Production v3.0.1, Cluster 5 (Phase 8) P8-5 (fällt mit C4-2 zusammen) + P8-8 (braucht Fabian für Zweitnutzer-Token). Re-runnables Login-Snippet mit aktuellem TOTP-Code für beide Instanzen (rollt alle 30 s, vor jeder Sichtprüfung neu ausführen), Screenshots-Konvention, Ergebnis-Tabellen je Cluster, Reihenfolge-Empfehlung (11 Schritte, ~15–30 Min), Hard-Rule-9-konformer Cleanup-Befehl. **Cluster-3-Rest-Block** ist neu geschrieben — vorher gab es nur `CLUSTER3_TESTBLOCK.md` für P8-20/21/22/24 gegen die Wegwerf-Instanzen, jetzt konsolidiert + erweitert um Cluster 4 + 5 + Login-Workflow. **Doku-Updates im selben Sub-Session-Zyklus (Hard Rule 8):** `phase8_5_picker_release/CLAUDE.md` Folge-Sub-Session-Block neu im Head (gleichberechtigt zum ersten 2026-09-08-Block, beide unter `## Session stopped`-Header — Phase-8.5-Muster erlaubt mehrere `### date`-Subblöcke); `docs/INDEX.md` neue Datei-Zeile; **kein Code-Touch**, **pytest 964/964 unverändert**, **Tabu-Diff §0.3 leer**, **Service-Touch 0**. **Größen-Stand:** Phase-8.5-Head **65.3 KB** (+24.4 KB durch den 2026-09-08-Folge-Block, schon vorher deutlich über dem 40-KB-Softcap, Auflösung bleibt Z-Arbeit — bewusst nicht stiller Trimm); `SICHTPRUEFUNG_RESTBLOCK.md` **27.5 KB** neu; `docs/INDEX.md` **64.0 KB** (+0.7 KB); `p8x_ui_polish_notes.md` 37.5 KB unverändert; `SESSIONS_ARCHIVE.md` ~128 KB unverändert. **Nächster Schritt:** Sichtprüfungen selbst durch den Nikinger am echten Gerät nach `SICHTPRUEFUNG_RESTBLOCK.md`-Anleitung (~15 Min ohne Fabian / ~30 Min mit). Cluster 5 (P8-8 Zweitnutzer) braucht Fabian. **Cleanup nach dem Lauf:** `.venv/bin/python phase8_ui_graph/scripts/wegwerf_setup_d2.py cleanup` + `…_200knoten.py cleanup` (Hard Rule 9, PID-Datei-basiert, **niemals** `pkill -f`). **Danach: Z** (Phase-8.5-Closeout) hebt die abgehakten Zeilen auf ✅ und schließt Phase 8 + 8.5 formal mit ab.

**[2026-09-08] Phase 8.5 — 🔄 Doku-Sub-Session (Wegwerf gestartet + 3 User-Feedback-Punkte), ⬜ Cluster 4 + 5 + Z als Nächstes.** 200-Knoten-Wegwerf-Instanz per Standing-Permission gestartet (Port 18772, PID 436596, User `alpha`, Credentials unter `/tmp/opencode/sharefyx-wegwerf-200knoten/credentials.json`); Production-Dienst unverändert PID 355956 (seit 2026-09-05 16:10:18 CEST); **drei weitere User-Feedback-Punkte** in `docs/concepts/p8x_ui_polish_notes.md` ergänzt: §6 Konto/Einstellungen-Rename + Positions-Tausch mit Logout re-affirmiert mit drei Vertausch-Lesarten a/b/c gegen `app.html:31-41` (Klärung in der Planungs-Session, nicht raten); **§8 NEU customizable Tags for tasks (kosmetisch) + Standard-Tag „blocked"** mit Aufteilung in §8.1 (User-Palette als `localStorage["sfx:tags:palette"]`, Server unverändert, „only cosmetic") und §8.2 (fester Code-Tag, offen ob kosmetisch oder mit Bucket-Semantik); **§9 NEU direkter User-Feedback-Button** mit drei plausiblen Senken (User-Space-Item via bestehende REST-API / `/var/log/sharefyx/feedback/` mit neuem Server-Write-Pfad / externer Endpunkt = Architektur-Frage) + UI-Platzierungs-Vorschlag (Rail unter Einstellungen + Abmelden, oder Read-View-Footer) + Klärungsfragen zur Planungs-Session (anonyme Variante, Throttling, „Was darf mitgeschickt werden" — explizit kein TOTP/Passwort/Recovery); §C (offene Fragen) und §E (chronologische Tabelle) ebenfalls ergänzt. Cluster-3-Block aus Phase-8.5-Head per Hand nach `SESSIONS_ARCHIVE.md` rotiert (Skript passt nicht auf Phase-8.5-Muster, bewährtes Vorgehen), 2026-09-08-Doku-Block neu im Head. **Login-Daten-Befehl für den Nikinger** (gibt bei jedem Lauf den aktuellen Satz aus, da das Passwort per `secrets.token_urlsafe(8)` jedes Mal neu gewürfelt wird): `cd /home/savefyx/dev/savefxy && .venv/bin/python -c '...'` (vollständiger Block im Phase-8.5-Head Session-Block). **Größen-Stand:** Polish-Notes **37.5 KB** (knapp unter 40-KB-Softcap, **+12 KB**), Phase-8.5-Head **53.8 KB** (+3 KB, weiter über Softcap — Auflösung bleibt Z), Phase-8.5-SESSIONS_ARCHIVE **121.8 KB** (+13 KB durch rotierten Cluster-3-Block, L3 exempt), Phase-8-Head **94.3 KB** unverändert, `docs/INDEX.md` **63.3 KB** (+1.7 KB), Wurzel-`CLAUDE.md` **72.2 KB** (+1 KB). **pytest unverändert 964/964** (kein Python-Touch), **Tabu-Diff §0.3 leer**, **Service-Touch 0**. **Nächster Schritt:** Cluster 3-Rest (P8-21 d / P8-22 / P8-24 Nikinger-Aktion) + Cluster 4 (Connector: P8.5-3 + P8.5-4 + P8.5-17 V105 + P8.5-19 Bauform-Bestätigung Radiogruppe) + Cluster 5 (Fabian: P8-5 + P8-8) + Z.

**[2026-09-03] Phase 8.5 geplant — ⬜ nicht gestartet.** Link-Picker-Politur, Titel-statt-ID-Hint,
v3-Vorabritt und Deploy (`phase8_5_picker_release/`, kein eigenes Python-Paket). Plan:
`docs/concepts/phase8_5_picker_release_plan.md` (N1–N7 gelockt, P8.5-A–P8.5-T, Abnahme
P8.5-1–P8.5-20, `[VERIFY]` V95–V105). Schließt die drei Restdefekte aus
`phase8_ui_graph_plan.md` §9.4.1–§9.4.3 und **beendet Phase 8 formal mit** (N6, Präzedenz
P7 Step A8 für Phase 6.5) — deshalb 8.5 und nicht 9. **Wichtige Korrektur zum Live-Stand:**
v3.0 ist **nicht** ausgeliefert — `/opt/sharefyx/current` zeigt auf `007b73d` (Block B),
Badge `v2.2.3`; Block C (Design v3) und Block D (Graph, tabellose Übersicht) liegen nur im
Repo. Deshalb ist ein **voller 13-Stationen-Vorabritt gegen eine Wegwerf-Instanz vor dem
Deploy** Teil dieser Phase (N5), nicht nur die drei Fixes. Kernbefund der Planung, im Code
verifiziert: ein Body-Link `[Titel](#item/itm_…)` ist bereits eine Graph-Kante
(`storage/linkscan.py`) — der Picker bekommt deshalb einen **Modus-Umschalter** statt eines
Kombi-Klicks. **Ausführung wieder opencode/M3 ohne Advisor** (N4), mit neuer
Eskalationsregel: Kaskaden-Ursachen gehen an Claude Code (Lehre vom 2026-09-02).

**[2026-09-03] Phase 8.5 — 🔄 Step 0 abgeschlossen, ⬜ A1 noch nicht angefangen.** Skelett
angelegt (`phase8_5_picker_release/{CLAUDE.md, SESSIONS_ARCHIVE.md, scripts/}` mit L1-Cards,
Modul-Status-Tabelle für Step 0/A/B/C/D/Z, Abnahmematrix nach §7-Muster, leerer
`## Session stopped`-Block), die vier vom Plan §1 benannten Funde abgearbeitet:
`docs/INDEX.md` 52.911 B → 40.917 B (Kürzung `updated:` auf die 5 neuesten Einträge +
Schlusszeile „ältere Einträge: phase*/SESSIONS_ARCHIVE.md", jetzt 43 B unter dem eigenen
40 KB-Softcap, Ausnahmenliste kompakt gehalten wegen der Mehrbelastung), vier card-lose
`.md` als korrekte Ausnahmen dokumentiert (Harness, Test-Fixtures, maschinell geparst,
Vendor/Lizenz), Doku/Code-Drift „Büroklammer" → „Lupe" in
`phase8_ui_graph/CLAUDE.md:440` mit datierter Korrekturnotiz, Phase-8-Abnahmebilanz
**15/10/0 → 14/12/0** maschinell korrigiert und awk-Kommando im Phase-8-Head Bilanz-Abschnitt
verankert (zählmaschinell nachprüfbar, statt weiterer Drift). ROADMAP-Abschnitt „Phase 8.5",
Wurzel-CLAUDE.md-`down:` auf `phase8_5_picker_release/CLAUDE.md` umgestellt, drei INDEX-Zeilen
unter „Phase 8.5 — 🔄 …" — alles im selben Commit (Hard Rule 8). **`pytest` unverändert
959/959 grün** (kein Python-Touch in dieser Session), Tabu-Diff §0.3 leer, kein Service-Touch
(PID 195922, ActiveEnterTimestamp 2026-09-02 11:51:57 CEST — nur gelesen). Nächster Schritt:
Block A / A1 (Picker-Modus-Umschalter).

**[2026-09-04] Phase 8.5 — 🔄 A1 committet, Drift nachgezogen, ⬜ A2 als Nächstes.** A1
(Picker-Modus-Umschalter + Body-Markdown-Link-Helper + `localStorage` unter
`sfx:linkpicker:mode`) gebaut und committet (`499d9be`, vollständiger Session-Block in
`phase8_5_picker_release/CLAUDE.md`); Modul-Status A1 `⬜` → `🟡` (Tests ⬜, Browser-Nachweis
folgt in Block C Station 6/8). **Drift-Korrektur in diesem Commit:** Wurzel-Current-state
+ `docs/INDEX.md` Phase-8.5-Eintrag + `ROADMAP.md` Phase-8.5-Absatz waren seit dem A1-Commit
versehentlich nicht nachgezogen — Phase-eigene Hard-Rule-8-Erweiterung (INDEX-Zeile +
ROADMAP + Wurzel-Current-state im selben Commit) verlangt das eigentlich; INDEX-Bullet-
Lücke (`phase8_5_picker_release/CLAUDE.md` + `SESSIONS_ARCHIVE.md` fehlen komplett unter
„Phase 8.5 — 🔄 …") geht auf die Planungs-Commit-Widmung im Step-0-Block zurück („drei
INDEX-Zeilen … bereits durch den Nikinger angelegt" — die dritte Zeile fehlte real).
Auflösung in einem Folge-Commit mit INDEX-Trimmung. **`pytest` 959/959 unverändert**,
Tabu-Diff §0.3 leer (kein Code-Touch in beiden Commits), ui_budget 5/5 (127.6 KB nach A1
+1.8 KB), `node --check` grün auf dialogs.js/editor.js/app.js, Service-Touch 0 (PID 195922,
ActiveEnterTimestamp 2026-09-02 11:51:57 CEST — nur gelesen). Nächster Schritt: A2
(Tastaturnavigation + CSS-Block-Entdopplung am Picker, `app.js` tabu).

**[2026-09-04] Phase 8.5 — 🔄 A2 committet, 🟡, ⬜ B1 als Nächstes.** A2 (`aria-activedescendant`-
Tastaturnavigation + gemeinsamer Pick-Pfad `_pickLinkPickerAt` + CSS-Block-Entdopplung am
Picker) gebaut und committet (vollständiger Session-Block im Phase-Head, A1-Block nach
`SESSIONS_ARCHIVE.md` rotiert); `dialogs.js` neue Modul-Variablen `linkPickerItems`/
`linkPickerCursor`, neuer `_renderLinkPickerResults`-Aufbau mit State-Reset ganz oben,
neue Helper `_setLinkPickerCursor`/`_pickLinkPickerAt`, neuer keydown-Handler am
Suchfeld (ArrowDown/ArrowUp/Enter, kein Wrap, kein Home/End, kein Raten; Escape bleibt
beim globalen Handler); `app.css` zwei identische Auswahl-Blöcke zusammengezogen, totes
`:focus` raus; drei neue statische Tests in `test_static_routes.py`
(`test_link_picker_css_has_one_selection_block` P8.5-14, `test_link_picker_picks_run_
through_a_single_helper` P8.5-12, `test_insertAtCursor_defined_exactly_once_at_module_level`
P8.5-9 nachgezogen — A1 hatte diese drei statisch zu belegen zurückgestellt); Modul-Status
A2 `⬜` → `🟡`, Abnahmestand **3 ✅ · 3 🟡 · 14 ⬜ von 20**. **`pytest` 962/962** (959 + 3 neu,
keine Regressionen), Tabu-Diff §0.3 leer (kein `storage/`/`mcpserver/`/`security.py`/`api.py`/
`serializers.py`/`permissions.py`-Touch), ui_budget 5/5 (128.7 KB, +1.1 KB durch `dialogs.js`
11.7 → 12.6 KB), `node --check` grün auf `dialogs.js`, Service-Touch 0 (PID 195922,
ActiveEnterTimestamp 2026-09-02 11:51:57 CEST — nur gelesen). Nächster Schritt: B1
(`_TITLE_NOT_ID_HINT` generalisierend schärfen in `mcpserver/tools.py:159-164`, einzige
erlaubte Tabu-Ausnahme).

**[2026-09-05] Phase 8.5 — 🔄 D1 committet, 🟡, ⬜ D2–D5 als Nächstes.** Release-
Vorbereitung opencode/M3 (Hard Rule 8 im selben Commit): Badge `v3.0` → `v3.0.1` in
`phase5_ui/webui/static/app.html:20` (P8.5-N7, statisches HTML ist nicht im Tabu §0.3);
neuer `## 2026-09-05`-Block in `docs/UPDATE_LOG.md` mit drei menschenlesbaren Zeilen
(Picker-Modi, Tastatur, Generalisierter Hint). **Datums-Drift ausdrücklich dokumentiert:**
Block-C-Absatz von gestern hatte noch `## 2026-09-04` vorgeschlagen — heute ist
`date +%F`/`date -u +%F` = 2026-09-05, und `deploy.sh` Z. 117–131 verlangt strikt
`today_utc`/`today_local` als oberstes Datum, sonst Gate-Abbruch. Block-C-Block per Hand
nach `SESSIONS_ARCHIVE.md` rotiert (newest-first, vor B1); Skript
`scripts/rotate_session_block.sh` passt nicht auf das Phase-8.5-Muster mit einem
`## Session stopped`-Header + mehreren `### date`-Subblöcken (Skript zählt nur den
`## Session stopped`-Marker und sieht immer genau einen → Exit 2 „Bereits konform").
Modul-Status D `⬜` → `🟡` mit D2–D5 als Nikinger-Aktionen vermerkt. **`pytest` nicht
gelaufen** (kein Python-Touch), Tabu-Diff §0.3 leer (`app.html` und `docs/UPDATE_LOG.md`
nicht tabu), Service-Touch **0** (PID 195922 / ActiveEnterTimestamp 2026-09-02 11:51:57
CEST nur gelesen). **Nächster Schritt:** D2 — Deploy als **Nikinger-Aktion** (`sudo
systemctl ... deploy.sh main` in interaktiver Vordergrund-Shell, V103 prüft den
`sudo`-Prompt; Hard Rule 9 — niemals `sudo systemctl` durch opencode/M3), danach D3
Health-Gate 3/3 + V105, D4 Sichtprüfung am echten Gerät + P8.5-19-Abnahme, D5 Vierte
A3-Probe (entscheidet §9.4.1 Abbruchregel aus N2), Z Closeout.

**[2026-09-06] Phase 8.5 — 🔄 D4-Sichtprobe-Folgesession durch den Nikinger (Notiz-Session, kein Code-Touch in dieser opencode/M3-Session), ⬜ D5/V105 als Nächstes, dann Z.** Im
Anschluss an D4 hat der Nikinger mit Fabian **sieben neue Themen-Cluster** aus
der Sichtprobe gesammelt, die über den D4-Sichtprüfungs-Scope hinausgehen und in
**p8.X** gehören: §1 Spaces-Layout-Reorg [„Alle Items"-Leiste unter Spaces +
Kippschalter, Map 40 % Breite/volle Höhe, keine Duplikate]; §2 Obsidian-Map fünf
Sub-Punkte [Performance-Reload, Landkarten-Stil, Field schneidet ab, Reload-Drift,
Collapsible mit Abhängigkeiten]; §3 Anzahl-Anzeige Ordner; §4 Edit-in-Place-Vision
[„Bearbeiten"-Knopf überflüssig, Word-ähnlich im Read-View editieren — harter
Konflikt mit Hard Rule 3 „kein Last-Write-Wins" und P7-24-Reauth-Grant-Mid-Edit];
§5 Layering-Design-System [3 Layer: echtes Schwarz / aktueller Standard /
Liquid Glass + Selektion explizit blau auf Hover, Note-Select, Checkbox,
größter Brocken]; §6 „Konto"→„Einstellungen"-Rename + Positions-Tausch mit
Logout; §7 De-AI-ierung-Lauf 2 [nach **neuen** Kriterien, dann positive
Erstellungs-Regeln]. **Neue Datei `docs/concepts/p8x_ui_polish_notes.md`** (L2,
25 KB, 2026-09-06) sammelt alle 16 Themen — fünf bereits in D4 dokumentierte
p8.X-Punkte + die sieben neuen Cluster + vier Sub-Punkte aus §2; Anhang §A–§E
(D4-Duplikat-Verweise, klare Außenkanten, sechs offene Fragen für die
Planungs-Session, Namens-Konvention, chronologische Tabelle). **Bewusst kein
Plan, kein Locking, keine Tabu-Aufhebung** — Sammlung, Strukturierung, kein
Phase-8.5-Scope-Touch. Doku-Updates im selben Zyklus: `phase8_5_picker_release/
CLAUDE.md` aktiver Block auf Folgesession umgestellt, D4-Block nach
`SESSIONS_ARCHIVE.md` rotiert; `docs/INDEX.md` neue Sektion „## Phase 8.X" +
Phase-8.5-Header-Hinweis; `ROADMAP.md` neue Sektion + Tabellen-Zeilen P8.5 + P8.X
(korrigiert); `phase8_ui_graph_plan.md §9.4.7` Anker auf neue Notizen-Datei
(folgt); pytest nicht gelaufen (kein Python-Touch), Tabu-Diff §0.3 leer,
Service-Touch 0 (letzter Stand 2026-09-05 16:10:18 CEST / PID 355956,
Hard Rule 9 + §0.5.7 — diese Session ist reine Doku, kein `sudo systemctl`).
**Nächster Schritt:** D5 (Vierte A3-Probe, Nikinger, entscheidet §9.4.1
Abbruchregel) + V105 (Connector-Check, Nikinger); optional vor Z durch
opencode/M3: Radiogruppe-Tausch + Bracket-Fix, damit Z die Endabnahme-Zeilen
P8.5-6 + P8.5-19 auf ✅ heben kann; dann Z (Phase-8.5-Closeout) mit
Phase-8-✅-Nachtrag + p8.X-Ankündigung, jetzt mit Verweis auf
`docs/concepts/p8x_ui_polish_notes.md` als Wahrheits-Quelle.

**Größenstand am Session-Ende (Ist-Werte, Notiz für die nächste Session /
für Z):** `CLAUDE.md` (Wurzel) **55.014 B** (+7.015 B durch diese Session,
deutlich über dem 40-KB-Softcap, signifikantes Wachstum — Wurzel-CLAUDE.md
näher am 56-KB als am 40-KB-Cap, Auflösung bleibt eine Phase-8-Z-Entscheidung
aus Z wie schon D3 dokumentiert hat); `ROADMAP.md` 43.819 B (neu über dem
Softcap, erstmals so notiert, **+1.406 B** durch neue Phase-8.X-Sektion + zwei
Tabellenzeilen); `docs/INDEX.md` 49.556 B (war schon über Cap, **+4.772 B**
durch neue Phase-8.X-Sektion + L0-Zeile); `docs/concepts/p8x_ui_polish_notes.md`
neu, 25.489 B; `phase8_5_picker_release/CLAUDE.md` 39.679 B (**knapp unter
Cap**, +1.641 B); `phase8_5_picker_release/SESSIONS_ARCHIVE.md` 75.330 B (L3,
exempt). **Kein** stilles Trimming — Pattern wie schon D3/D4: dokumentieren,
nicht kürzen; Auflösung ist Z-Arbeit.

**[2026-09-06] Phase 8.5 — 🔄 D4 Sichtprüfung am echten Gerät durch den Nikinger, alles nur dokumentiert, ⬜ D5/V105 als Nächstes, dann Z.** Block 1–7 + Vorbereitung komplett durchgelaufen, beide Accounts in Firefox+Chrome+Safari; Update-Banner `## 2026-09-05` mit drei Zeilen sichtbar ✅, beide Picker-Modi funktional ✅ (eigenes `localStorage["sfx:linkpicker:mode"]` bestätigt), Tastaturnavigation geht über die Mindestanforderung Chromium+Firefox hinaus, Insert-at-cursor-Hub Bild-Knopf ✅, Settle-Zeit 2 s unter 3 s-Ziel, alle drei Graph-Farben, Knotenklick öffnet das Item, Conflict-Dialog gegen Speicherbutton-Spam bewährt (Hard Rule 3 „kein Last-Write-Wins" hält). **Drei echte Findings — Scope-Entscheidungen alle in dieser Session getroffen, Fixe in Folge-Sessions:** (1) **P8.5-19 Radiogruppe statt `<select>`** — Nikinger-Präferenz „deutlich angenehmer", P8.5-F-Planer-Substitution raus, Tausch 5 Z. in `dialogs.js:584`+`app.html:277` ausstehend, Lucide-Icons `link-2`+`pilcrow`/`text-cursor-input` als Vorschlag offen; (2) **P8.5-6 Bracket-Renderer-Bug** — Source-Escape `\[`/`\]` korrekt im Body, aber `markdown.js`-Link-Parser bricht in Vorschau (eckige Klammern ja, runde nein), §0.3 erlaubt `webui/static/js/`, Hard-Rule-9-Eskalation greift nicht (Ursache liegt genau im Fix-Pfad), Fix-Pfad vor Z; (3) **UX-2-Step-Knotenklick** — neues Feature „erster Klick Readonly-Vorschau, zweiter Klick vollständig" für p8.X parkiert, Fabi sammelt gerade. Drei Parken-bestätigt (vom D3-Handover übernommen): Map-Field schneidet unten ab, Map fliegt bei jedem Reload, Save-Button-YAML-Header-Issue (wahrscheinlich p8.X, Verifikation ob außerhalb Header-Kontext steht aus). **Phase 8 ✅ + p8.X als Folge-Phase** als Nikinger-Entscheidung für Z vorgemerkt. Modul-Status Zeile 6 Block D jetzt D1 ✅ + D2 ✅ + D3 ✅ + D4 ✅, D5 ⬜ + V105 ⬜ weiter Nikinger; P8.5-6 mit Bracket-Caveat, P8.5-17 Update-Banner-Teil ✅; Summary 3 ✅ · 14 🟡 · 3 ⬜. D3-Block per Hand nach `phase8_5_picker_release/SESSIONS_ARCHIVE.md` rotiert (Skript passt nicht auf Phase-8.5-Muster). **Nächster Schritt:** D5 (Vierte A3-Probe, Nikinger, entscheidet §9.4.1 Abbruchregel) + V105 (Connector-Check, Nikinger); optional vor Z durch opencode/M3: Radiogruppe-Tausch + Bracket-Fix, damit Z die Endabnahme-Zeilen auf ✅ heben kann; dann Z (Phase-8.5-Closeout) mit `phase8_ui_graph_plan.md §9` + Phase-8-✅-Nachtrag.

**[2026-09-05] Phase 8.5 — 🔄 D2 vom Nikinger zwischen D1 und D3 + D3-Prep, 🟡, ⬜ D4/D5/V105/Z als Nächstes.** D2 ist **zwischen D1 (Commit heute früh) und D3 (diese Session) still durch den Nikinger gelaufen** — Entdeckung kam erst beim ersten Probe-Lauf des Health-Gate-Skripts: `/opt/sharefyx/current` → `20260905T140325.378914Z` → HEAD `6f19a8f` (D1), Service-PID **355956** (statt der im D1-Block notierten 195922 — D2-Deploy hat den Dienst erwartungsgemäß neu gestartet), `ExecMainStartTimestamp=2026-09-05 16:10:18 CEST`. Damit ist D3 nicht mehr Vorbereitung, sondern **Verifikation des bereits deployten v3.0.1**. Neu gebaut: `phase8_5_picker_release/scripts/health_gate.sh` (134 Zeilen bash, `set -uo pipefail`, JSON auf stdout / Details auf stderr nach Hard Rule 7), acht Gates — `/health` 200 mit Retry-Loop, `/ui/login` 200, `/api/v1/me` 401, `/mcp/` 401, `.rail__version` aus `/ui/static/app.html` (**nicht** `/ui/login` — `pages.py`s Auth-Template ohne Rail, erste Iteration fiel darauf herein, gefixt), `/opt/sharefyx/current` → Release mit `.git`, optional `--require-todays-update-log` (UTC/local wie `deploy.sh` Z. 127-131), optional `--expected-sha=<hex>` (Short- oder Full-Form per Prefix-Vergleich). **Lauf-Beleg 2026-09-05 15:19:53Z** mit `--require-todays-update-log --expected-sha=6f19a8f`: **8/8 grün**, Exit 0, JSON auf stdout (`result:"ok"`, `actual_version:"v3.0.1"`, `release_sha:"6f19a8f..."`, `active_release:"/opt/sharefyx/releases/20260905T140325.378914Z"`, `port:8765`). Drei Negativproben separat verifiziert (Port 9999 → Gate 1 rot, `--expected-version=v9.9.9` → Gate 5 rot, `--expected-sha=0000000` → Gate 8 rot). **P8.5-17 teilweise abgehakt:** Deploy gelaufen ✅, Health-Gate 8/8 ✅, Badge `v3.0.1` live ✅, Update-Banner-Live-Anzeige ⬜ (braucht Auth, Nikinger), V105 ⬜ (echter Anthropic-Connector, Nikinger). Modul-Status-Zeile 6 Block D um D2 ✅ + D3 🟡 erweitert; Abnahmestand-Zeile P8.5-17 Health-Gate-Teil 🟡; Summary **3 ✅ · 14 🟡 · 3 ⬜ von 20**; D1-Block (111 Zeilen) per Hand nach `SESSIONS_ARCHIVE.md` rotiert (Skript passt nicht auf das Phase-8.5-Muster — bewährtes Vorgehen aus D1 selbst). `pytest` nicht gelaufen (kein Python-Touch), `bash -n` OK, shellcheck nicht verfügbar (übersprungen, keine Konvention im Repo), Tabu-Diff §0.3 leer, Service-Touch 0 (PID 355956 nur gelesen). **Nächster Schritt:** D4 — Sichtprüfung am echten Gerät durch den Nikinger (`## 2026-09-05`-Eintrag im Update-Banner sichtbar, `<select class="input" id="link-picker-mode">` im Picker vorhanden — P8.5-19-Abnahme: Radiogruppe oder `<select>`-Bestätigung), D5 Vierte A3-Probe (entscheidet §9.4.1 Abbruchregel aus N2), V105-Connector-Check, Z Closeout.

**[2026-09-04] Phase 8.5 — 🔄 Block C committet, 🟡, ⬜ Block D + Z als Nächstes.** Voller
v3-Vorabritt (Plan §4) gegen eine Wegwerf-Instanz auf Port 18773 gefahren:
`phase8_5_picker_release/scripts/wegwerf_setup_v3ritt.py` (Wegwerf-Setup mit Standing-
Permission-Muster aus Phase 8: eigener Port, tmp-`DATA_ROOT`/tmp-`auth.sqlite3`/File-
Keyring; 30 Items über drei Spaces — 12 alpha + 10 beta + 8 gamma; ein archiviertes
Item, ein Item mit item-level `share_read=["gamma"]` (Deploy-Blocker-Fall aus P6 §35–
39), ein Item mit Bild-Asset (`ast_351d4217` per `put_asset()`); 11 explizite Kanten,
darunter die für V102 präparierte Zwillings-Kante body+frontmatter zwischen
`alpha:Buecherliste Q4` und `alpha:Empfehlungen Nikinger`); 16 Screenshots
`docs/screenshots/v3ritt_{chromium,firefox}_NN_*.png`. **`v3_ritt_playwright_smoke.py`:
13/13 Stationen grün in Chromium UND Firefox — 26/26 gesamt** (V101 beantwortet für beide
Browser). Drei **echte Befunde**, keine Code-Fixes im Tabu-Bereich nötig:
- **Smoke-Bug** (gefixt in dieser Session): Edge-Keys waren `src`/`dst` (konsistent mit
  `graph.js:325/394`), nicht `src_id`/`dst_id` wie im Smoke angenommen; ist beim
  V102-Vergleich aufgefallen, Smoke korrigiert, **kein Server-Bug**.
- **CSRF-Origin-Mismatch** zwischen Wegwerf-UI (`http://127.0.0.1:18773`) und
  konfiguriertem `SPACE_PUBLIC_BASE_URL` (`https://wegwerf-v3ritt.invalid`); `_validate_base_url`
  erzwingt https. Konsequenz: jeder `fetch()` mit POST/PATCH aus dem Browser-Kontext
  wird abgewiesen, das macht Station 13 (P8-1-Reauth-Grant-Mechanismus) im Wegwerf
  unscharf — der Live-Nikinger-Domain-Test in Block D fängt das auf. **Befund für
  Step Z / Plan-§4.C3.**
- **Pickstation 12 nur strukturell** (`@media (prefers-reduced-motion)` als Regel im
  CSS gefunden, aber keine echte Browser-Probe mit umgeschaltetem UA). War schon in
  Phase 8 `p8_22_smoke.py` throwaway-verifiziert (Fix A, 2,7 s statt 5,95 s); bleibt
  so.
- Modus-Selektor `<select>` vs. N3-Vorschau-`<input type="radio">`: **nicht als Befund
  behandelt** — die N3-Entscheidung war „Umschalter im Dialog" (P8.5-E), die Bauform
  `<select>` ist eine Planer-Substitution (P8.5-F), die der Nikinger in Block D4 am
  echten Gerät abnimmt (Abnahmezeile P8.5-19). Modul-Status C `⬜` → `🟡`, Abnahme-
  stand **3 ✅ · 13 🟡 · 4 ⬜ von 20** (P8.5-5, -6, -7, -8, -10, -11, -13, -15, -16 alle
  `⬜` → `🟡`; P8.5-3 bleibt `🟡` mit Klammer-Anmerkung für Live-D5). **`pytest` 962/962**
  unverändert (kein Python-Touch im Block-C-Setup, kein `phase5_ui/webui/`-Touch im
  Smoke), Tabu-Diff §0.3 leer, Wegwerf sauber abgebaut (`kill -TERM $(cat serve.pid)`,
  Hard Rule 9-konform), Produktion nachweislich unangetastet (PID 195922 / ActiveEnter
  2026-09-02 11:51:57 CEST vor/nach identisch). Nächster Schritt: **Block D** —
  Release-Vorbereitung (`.rail__version` `v3.0` → `v3.0.1`, neuer `## 2026-09-04`-Block
  in `docs/UPDATE_LOG.md`, drei Zeilen menschenlesbar zum Phase-8.5-Deploy), D2 Deploy
  als **Nikinger-Aktion** (Hard Rule 9 + P8.5-Q, niemals `sudo systemctl restart
  sharefyx-mcp` durch opencode/M3), D3 Health-Gate, D4 Sichtprüfung am echten Gerät,
  D5 Vierte A3-Probe (an der die Abbruchregel §9.4.1 fällt oder hält).

**[2026-09-04] Phase 8.5 — 🔄 B1 committet, 🟡, ⬜ Block C als Nächstes.** B1 (Hint generalisierend

**[2026-09-01] Phase 8 — 🔄 Block A + B ✅ live-verifiziert, Gate B→C bestanden.** UI-Neuanstrich v3,
Verknüpfungs-Graph (`GET /api/v1/graph` + `item_links`-Tabelle + `linkscan.py` + UI-Wiring), drei
P7-Erbposten (P7-24 Reauth-Grant ✅, `remove-space`-Auto-Reindex ✅, P7-4 Zweitprobe 🟡 mit
benanntem Restdefekt Klammer/Aufzählung). Plan: `docs/concepts/phase8_ui_graph_plan.md` (N1–N12
gelockt, P8-A–P8-Q, Abnahme P8-1–P8-24, `[VERIFY]` V81–V92). Kernentscheidungen: P7-24-Fix als
**Reauth-Grant** (vierte Option, in der Planung gefunden — kein Aufweichen des Anti-Replay),
**achte P1-Contract-Öffnung benannt** (Link-Extraktion beim Indexieren für den Graphen), Design
v3 (IBM Plex, Lucide-Sprite, Farblegende own/shared/foreign, Glass-Akzente mit Fallback).
**Ausführung erstmals opencode/M3, ohne Advisor-Stufe (N12)** — Ersatz: Plan §0.6 +
zwei Nikinger-Sichtprüfpunkte. Closeout wird §9 des Plans (ein Dokument pro Phase, P8-N).
**Gate B→C (2026-09-01)** alle vier Bedingungen grün: 958/958 pytest, Charakterisierung
byte-identisch, Tabu-Diff leer, `_graph_get` manuell gegen 3 Spaces + 12 ACL-Fälle 12/12,
Playwright-Smoke gegen Wegwerf-Instanz 18/18 (Picker + `#item/`-Navigation).
**Nächster Schritt:** Block C (Design-Fundament v3, Plan §4) — C0 Anti-AI-Research →
C1 Plex → C2 Lucide → C3 Farbsemantik → C4 Glass → C5 Dichte.

**[2026-08-28] Phase 8 geplant — ⬜ nicht gestartet.** UI-Neuanstrich v3, Verknüpfungs-Graph,
drei P7-Erbposten. Plan: `docs/concepts/phase8_ui_graph_plan.md` (N1–N12 gelockt, P8-A–P8-Q,
Abnahme P8-1–P8-24, `[VERIFY]` V81–V92). Kernentscheidungen: P7-24-Fix als **Reauth-Grant**
(vierte Option, in der Planung gefunden — kein Aufweichen des Anti-Replay), **achte
P1-Contract-Öffnung benannt** (Link-Extraktion beim Indexieren für den Graphen), Design v3
(IBM Plex, Lucide-Sprite, Farblegende own/shared/foreign, Glass-Akzente mit Fallback).
**Ausführung erstmals opencode/M3, ohne Advisor-Stufe (N12)** — Ersatz: Plan §0.6 +
zwei Nikinger-Sichtprüfpunkte. Closeout wird §9 des Plans (ein Dokument pro Phase, P8-N).

**[2026-08-28] Phase 7 abgeschlossen — ✅ live-verifiziert.** Space-Verwaltung in der
Weboberfläche, Mehrfachauswahl, Konsolidierung (`phase7_spaces_admin/`, kein eigenes Python-Paket)
sind gebaut, live deployt (`main`@`e88a624`, 2026-08-27) und abgenommen. **Abnahmestand: 22 von 24
Zeilen ✅, 2 ❌, 0 ungeprüft** — die Matrix ist vollständig durchgelaufen; das unterscheidet diese
Phase von P6/P6.5, wo Zeilen ungeprüft blieben. **Der Sprung auf ✅ ist eine Nikinger-Entscheidung
vom 2026-08-28** unter der Bedingung, dass die beiden ❌ als benannte Defekte an Phase 8 vererbt
werden: **P7-24** (`list.js :: moveSelectedItems()` reicht denselben TOTP-Code an jedes
sequenzielle PATCH einer Batch-Runde — der Server lehnt den Replay korrekt ab, ein Batch mit N
rechteerweiternden Items braucht real N Codes statt einem; echter Mechanismus-Defekt, Fix
bewusst in P8) und **P7-4** (Claude nennt Menschen gegenüber IDs statt Titeln, trotz der Anweisung
in vier Tool-Beschreibungen — kein Code-Fehler). **Dritter Erbposten aus dem Live-Betrieb:
`spacectl.py remove-space` reindiziert den SQLite-Index nicht** — der Incident vom 2026-08-27
(`GET /api/v1/overview` → 500 für jeden eingeloggten Nutzer) kam genau daher; der Zustand ist
per `space_cli.py reindex` behoben, die Ursache nicht. Sechste und siebte P1-Contract-Öffnung mit
dieser Phase geschlossen, keine achte angekündigt. **Einstiegsdokument für die Phase-8-Planung:
`docs/concepts/PHASE7_CLOSEOUT_HANDOVER.md`** (dort §4 die offenen Entscheidungen, §7 die
geänderte Arbeitsweise: Claude Code plant, opencode/M3 führt aus). Übersichtsgrafik:
`docs/concepts/phase7_spaces_admin_uebersicht.svg`. **Die folgenden Absätze bleiben als
Verlaufsdokumentation stehen.**

**[2026-08-23] Phase 7 aktiv — Space-Verwaltung, Mehrfachauswahl, Konsolidierung**
(`phase7_spaces_admin/`, kein eigenes Python-Paket) — **🔄, Block A weit fortgeschritten.** Step 0
(Haushalt + Doku-Audit) ✅, danach A1/A2 (Item-ID sichtbar+auffindbar)/A3 (Bild-Entfernen-Knopf,
schließt P6.5-12)/A4 (Feld-Whitelist, schließt O6) gebaut, A5 (Sichtbarkeits-Migration) live
`--apply` gefahren, A7/A7b (dritter Principal `testnutzer-p7` + `testcred.py`) live angelegt,
**A8 (formaler Abschluss Phase 6.5) durchgeführt** — siehe unten. Verbleibend in Block A: A6
(Purge-Gate, kalendarisch frühestens 2026-08-28). Plan: `docs/concepts/
phase7_spaces_admin_plan.md` (Entscheidungen P7-A–P7-W, alle zehn Nikinger-Fragen N1–N10 gelockt
in §0.1). Phase-Head: `phase7_spaces_admin/CLAUDE.md`.

**[2026-08-27 Korrektur]** Der Absatz oben blieb seit dem Phasenstart stehen und ist überholt.
**Phase 7 ist inhaltlich vollständig** — Block A (inkl. A8, Phase 6.5 formal abgeschlossen),
Gate A→C, Block C (C1–C5, Space-Verwaltung in der Weboberfläche) und Block B (Mehrfachauswahl,
`ITEM_MOVE_PLAN.md` §9) sind alle gebaut. **Live deployt, 2026-08-27, Nikinger-Lauf:**
`/opt/sharefyx/current` → `e88a6244d8eebb5d08d1d93c4a2725f84a2f5971`, Health-Gate 3/3 grün
(`/ui/login`→200, `/api/v1/me`→401, `/mcp/`→401 — alle drei die erwarteten Antworten, kein
Fehlschlag). **[2026-08-28 Korrektur]** Abnahmezeilen 31–34 (`ITEM_MOVE_PLAN.md` §9.5) sind seither
vom Nikinger selbst live gegen die echte Instanz bestätigt — 32/33/34 ohne Vorbehalt, 31 mit dem
bereits bekannten P7-24-TOTP-Vorbehalt (kein neuer Fund, Fix in der nächsten Phase). **A6
(Purge-Gate/P7-9) ebenfalls gefahren** — `token_families` 35→31, `clients` unverändert 54 wie
erwartet (90-Tage-Fenster erst 2026-10-27). **Kein offener Test/Gate mehr.** Verbleibend: Step Z
Rest (Phase-7-Closeout-Dokumente, Übersichtsgrafik, Rotationsprüfung). **Noch nicht ✅** — „✅
heißt live-verifiziert, nicht gebaut", der formale Sprung folgt erst mit dem Closeout. Details:
`phase7_spaces_admin/CLAUDE.md`, aktueller Session-Block.

**[2026-08-23, P7 Step A8] Phase 6.5 formal abgeschlossen als 🟡 — code-complete und live
deployt, aber NICHT vollständig live-verifiziert.** Bewusst **nicht** ✅: **12 von 14
Abnahmezeilen** live, davon zwei (P6.5-8/13) über eine im P7-Plan §A8.1 gebilligte Substitution
— `testnutzer-p7` statt Fabian, derselbe serverseitige Rechte-Code-Pfad. Verbleibend offen:
P6.5-12 (Entfernen-Knopf jetzt von P7 Step A3 gebaut, kein Browser-Klick-Nachweis) und P6.5-14
(Nikingers eigene Bewertung, kein Selbstzertifizierungs-Kriterium — bleibt strukturell offen).
Handover: `docs/concepts/PHASE6_5_CLOSEOUT_HANDOVER.md`. Übersichtsgrafik:
`docs/concepts/phase6_5_tools_images_uebersicht.svg`. **Der untenstehende Absatz vom
Phasenstart (2026-08-20) bleibt als Verlaufsdokumentation stehen, ist inzwischen überholt.**

**[2026-08-20] Zweite aktive Phase gestartet: Phase 6.5 — Werkzeug-Ergonomie und Bilder**
(`phase6_5_tools_images/`, kein eigenes Python-Paket) — **🔄 Step 0.** Sitzt bewusst zwischen der
noch laufenden Phase 6 und der reservierten Phase 7 (Space-Admin-UI, `app.html` unverändert).
Deckt die fünf noch offenen MCP-Werkzeug-Ergonomie-Punkte (siehe „Noch nicht entschieden" unten —
**jetzt geplant, nicht mehr offen**) und den Abschluss von Block C Bilder ab (löst
`phase6_shares/IMAGES_PLAN.md` als maßgebliche Quelle ab). Plan: `docs/concepts/
phase6_5_tools_images_plan.md` (Entscheidungen P6.5-A–P6.5-V, alle sechs Nikinger-Fragen N1–N6
gelockt in §0.0). Phase-Head: `phase6_5_tools_images/CLAUDE.md`.

**[2026-08-23] Phase 6 abgeschlossen als 🟡 — code-complete und live deployt, aber NICHT
vollständig live-verifiziert.** Bewusst **nicht** ✅: nur **12 von 39 Abnahmezeilen** sind
live-verifiziert, vier (31–34, §9 Mehrfachauswahl) wurden nie gebaut, Block C ist nach Phase 6.5
ausgewandert, sieben Zeilen hängen an einer Sitzung mit Fabians eigenem Login. Es gibt bewusst
**kein** `P6_ABNAHME_<datum>.md` — der Zeilenstatus steht in
`docs/concepts/PHASE6_CLOSEOUT_HANDOVER.md` §3. **Der Sprung auf ✅ ist eine offene
Nikinger-Entscheidung.** Zwei Aufgaben sind vom Nikinger ausdrücklich für die nächste Phase
benannt: (1) **Doku-Audit** der Modul-Status-Zeilen 8–16 in `phase6_shares/CLAUDE.md`, die noch
„gebaut, noch nicht deployt" tragen — vermutlich stale, wie sich am 2026-08-23 schon für die
globale Suche zeigte, aber **zu prüfen, nicht zu raten**; (2) **kein Entfernen-Knopf für Bilder**
in `phase5_ui/webui/static/js/editor.js`, obwohl N5 gelockt ist und der `DELETE`-Endpunkt
existiert (blockiert P6.5-12). Übersichtsgrafik: `docs/concepts/phase6_shares_uebersicht.svg`.
**Phase 6.5 ist davon unberührt und läuft weiter.** Der folgende Absatz bleibt als
Verlaufsdokumentation stehen.

**Phase 6 — Freigaben, Ordner, Werkzeug-Ergonomie** (`phase6_shares/`, kein
eigenes Python-Paket) — **offen/Kompakt:** Phase 6 abgeschlossen als `phase6_shares/CLAUDE.md`.
Verlaufsdokumentation zweier Blöcke (Block A Werkzeuge/Betrieb/Update-Banner, Block B
Dateisystem mit SharePolicy-Cutover; Block C Bilder nach 6.5 ausgewandert) ist dort —
Steps 0–3 (patch_item, ua-Feld, Update-Log-Banner) gebaut, Steps 4–6 (Storage-Fundament +
Rechtepolitik + Verwaltung) 2026-08-13 live deployed (`main`@`d068d1c`), IT-Sekus-UI-Fund
(writable-Badge + acht `ownSpaceActive()` zu `activeSpaceWritable()`) geschlossen,
Closeout-Handover `docs/concepts/PHASE6_CLOSEOUT_HANDOVER.md` mit 12-von-39-Live-Bilanz.
**Hard Rule 8:** Phase-6-/6.5-/7-Block-Detailnarrative werden hier nicht mehr dupliziert —
maßgebliche Quelle: die jeweilige `phase*/CLAUDE.md`.

**Deploy-Blocker (2026-08-18) + Funnel-Recovery (2026-08-19) — kompakt:**
Der 2026-08-18 entdeckte UI-Fund („kein über-alle-lesbaren-Items-Suchmodus", item-level-only
`share_*` über Web-UI unauffindbar, nur Connector-Zugriff) wurde 2026-08-19 geplant
(`phase6_shares/GLOBAL_SEARCH_PLAN.md`, P6-AO–AT; Q1: Titel/Tags-only, kein Body-Fulltext) —
Kernbefund im Code verifiziert: `GET /api/v1/items` *ohne* `space`-Parameter ist bereits die
globale, item-weise ACL-gefilterte Suche, es fehlte nur die UI-Fläche (kein neuer
Endpunkt). Steps G1–G2 gebaut (Playwright 10/10 gegen Wegwerf, Advisor-Fund
`editor.js :: clearDetail()` Scope-Reset mitgefixt), `d348e2e` 2026-08-23 zu `f96125e`
korrigiert (Closeout-Sweep) und live deployt. Der 2026-08-19-Funnel-Reboot-Fund (`tailscaled`-
Restart nach VM-Reboot, MagicDNS hatte den öffentlichen Pfad verdeckt) hat
`diagnose.sh`-Prüfung 5 korrigiert; Watchdog/Selbstheilung bewusst offen. Volle
Herleitung beider Punkte: `phase6_shares/CLAUDE.md` Session-Block 2026-08-23 bzw.
`phase3_edge/CLAUDE.md` Abschnitt 2026-08-19.

**[2026-08-19] Block C (Bilder) ist geplant:** `phase6_shares/IMAGES_PLAN.md` (Entscheidungen
**P6-AU–P6-BB**, Abnahmezeilen 40–47) — **fünf offene Nikinger-Entscheidungen B1–B5** (Binärblobs
in der Git-Historie des `DATA_ROOT` vs. Hard Rule 5, Größenriegel, Bildbytes fremder Items vor
einem sehenden Modell als Injektionskanal, den `<untrusted_content>` strukturell nicht erreicht,
MCP-Upload, Löschen eines Bildes vs. Entscheidung H/„kein Delete im Kern-API"). Vor dem Bau
einzuholen, nicht von Claude zu entscheiden.

**Phase 5 — Web-UI, REST-API und Auth-Selbstverwaltung** (`phase5_ui/`, Paket `webui`) — **✅
abgeschlossen, 2026-08-09 — 20/20 Abnahmezeilen live bestanden, 0 teilweise, 0 offen.** Zwei
Blöcke (A = Sicherheit + Auth-Selbstverwaltung, B = REST-API + UI) mit hartem Gate dazwischen,
beide durchlaufen. Menschen setzen ihr Passwort jetzt selbst im Browser, ohne SSH und ohne
Neustart (schließt Betriebsnotiz O1 auch live). Cutover auf `/opt/sharefyx/current` seit
2026-08-05, `deploy.sh`-Zyklus läuft. `git diff` auf `storage/`,
`mcpserver/{tools,permissions,server}.py` blieb über die gesamte Phase leer (Kriterium 18) —
derselbe Seam-Beweis wie in Phase 4, eine API-Fläche höher.

Vollständige Matrix, Modul-Status je Step und die gesamte Live-Debugging-Historie (u. a. der
Origin/CSRF-Fund am Block-A-Gate, die Step-7b-Revision von Plan §4.1/§4.3, Sicherheitsbefund S9)
stehen in `phase5_ui/CLAUDE.md` — read + newest Session-stopped-Block first, das ist die
maßgebliche Quelle für diese Phase, nicht diese Zeile hier. Ältere Session-Blöcke:
`phase5_ui/SESSIONS_ARCHIVE.md`.

Plan: `docs/concepts/phase5_ui_plan.md` (Entscheidungen P5-A–P5-AE, Steps 0–9). Herkunft/offene
Entscheidungen: `docs/concepts/PHASE4_CLOSEOUT_HANDOVER.md`. Abnahmeprotokoll:
`docs/concepts/P5_ABNAHME_2026-08-09.md`. Formaler Abschluss-Handover an P6:
`docs/concepts/PHASE5_CLOSEOUT_HANDOVER.md`.

**[2026-08-09 erledigt]** Vor-Phase-6-Vormerkungen F1 (Subspaces/Shared Spaces), F2 (kein Löschen, nur Archivieren), Client-Surface-Logging (ua-Feld), `patch_item` (gezielter Patch statt Volltext-Rewrite) sind alle in Phase 6 gelandet (`phase6_shares_plan.md`: F1 zu P6-J/K/Q/T, F2 zu §0.5 weiterhin draußen, Logging zu P6-A5/Step 2, `patch_item` zu P6-E/F/G/Step 1, gebaut als siebtes MCP-Tool 2026-08-09). F1b (Space, in dem alle unabhängig volle Rechte haben) bleibt wegen Hard Rule 4 bewusst draußen. Volltext: `phase6_shares/CLAUDE.md` Vormerkungen-Abschnitt.

**Phase 4 — OAuth 2.1 + DCR** (`phase4_auth/`, Paket `authserver`) — **✅ abgeschlossen,
2026-07-30 — 16/16 Abnahmezeilen live bestanden, Schnitt vollzogen.** Der Pfad-Token ist
verschwunden; ein eigener, im selben Prozess laufender Authorization Server (Discovery, Dynamic
Client Registration, PKCE, Argon2id + TOTP, opake rotierende Token) authentifiziert seither jeden
Connector. Kritischer Fund in Step 0: ein nie widerrufener Keyring-Token für einen seit P2
umbenannten dritten Space (`nikinger`) — live und schreibfähig, aber ohne zugehöriges
Verzeichnis; noch vor dem Schnitt widerrufen und live gegen `diagnose.sh`/
`export_space_map.py` bestätigt (Details: `docs/concepts/PHASE3_CLOSEOUT_HANDOVER.md` §5).

Sicherheitsbefunde **S1–S10 / O1–O2** (S1–S8 und S10 geschlossen; O1 strukturell durch P5
geschlossen; **O2 offen** — `clients`/`token_families` werden nie abgeräumt) stehen mit vollem
Verlauf und Fundstellen in `phase4_auth/CLAUDE.md`, ebenso der Modul-Status aller acht Steps und
das ausgeführte Inbetriebnahme-Runbook.

Plan: `docs/concepts/phase4_auth_plan.md` (Entscheidungen P4-A–P4-R, Steps 0–7 — geschrieben ohne
frischen Repo-Zugriff, siehe Plan-Kopf). Herkunft/offene Entscheidungen:
`docs/concepts/PHASE3_CLOSEOUT_HANDOVER.md`. Abnahmeprotokoll:
`docs/concepts/P4_ABNAHME_2026-07-29.md`. Sicherheits-Review vor der Abnahme:
`docs/concepts/P4_SECURITY_REVIEW_2026-07-29.md`. Formaler Abschluss-Handover an P5:
`docs/concepts/PHASE4_CLOSEOUT_HANDOVER.md`.

**Phase 3 — Exposure & Betrieb** (`phase3_edge/`, kein eigenes Python-Paket — Servercode bleibt
in `mcpserver`): ✅ **live-verifiziert, 13/13** — Ursprungsstand 10/13
(`docs/concepts/P3_ABNAHME_2026-07-27.md`). Zeile 6 (Reboot) löste sich am 2026-07-29 durch
einen unbeabsichtigten Reboot der VM (Windows-Host-Neustart des Nikingers), Zeile 12
(Backup-Timer-Lauf) durch einen realen Timer-Lauf in P4 Step 0. **[2026-08-02, P5 Step 0:]**
Zeile 13 (Restore-Nachweis) ist die letzte gefallen — Claude Code fuhr `restore_check.sh`
zunächst selbst als Kandidatenbeleg, der Nikinger führte denselben Lauf danach selbst aus
(identischer HEAD, `ok:true`) — echte Abnahme. **Phase 3 damit vollständig ✅.** Formaler
Abschluss-Handover an P4: `docs/concepts/PHASE3_CLOSEOUT_HANDOVER.md`. Plan: `docs/concepts/
phase3_edge_plan.md` (Entscheidungen P3-A–P3-N gelockt, Steps 0–7). Phase-Head:
`phase3_edge/CLAUDE.md`.

**Phase 2 — MCP-Server** (`phase2_mcp/`, Paket `mcpserver`): ✅ **abgeschlossen,
live-verifiziert seit 2026-07-26** — Quick-Tunnel-Probe + vollständige Adapter-Abnahme über den
echten Custom Connector durch den Nikinger, 21/21 Prüfungen, siehe
`docs/concepts/P2_ADAPTER_ABNAHME_2026-07-26.md`. Claude liest und schreibt über einen lokalen
`fastmcp`-Server auf den P1-Storage-Kern — Token→Space-Auflösung, sechs Tools,
`<untrusted_content>`-Wrapping fremder Bodies. Formaler Abschluss-Handover an P3:
`docs/concepts/PHASE2_CLOSEOUT_HANDOVER.md`. Plan: `docs/concepts/phase2_mcp_plan.md`
(Entscheidungen P2-A–P2-N, Steps 0–7). Phase-Head: `phase2_mcp/CLAUDE.md`.

**Phase 1 — Storage-Kern** (`phase1_storage/`, Paket `storage`): ✅ **abgeschlossen,
live-verifiziert.** Alle acht Module (Steps 0–7), 68 Tests grün (70 bei Phasenabschluss, minus
zwei bei Entfernung toten Codes in P2 Step 0 — siehe `phase1_storage/CLAUDE.md`) —
Frontmatter/Modelle, atomarer Datei-Store, SQLite-Index, Versionierung + Konfliktbehandlung,
Git-Commit je Write, Query-Layer, `space_cli.py` als Beweis. Der Nikinger hat den Lauf gegen den
echten `DATA_ROOT` (`/home/savefyx/savefyx-data`) selbst ausgeführt (2026-07-25, Hard Rule: kein
Test gegen den echten DATA_ROOT durch Claude Code). Details + Transkript:
`phase1_storage/CLAUDE.md`, Session-Block. Plan: `docs/concepts/phase1_storage_plan.md`
(Entscheidungen A–H gelockt, Steps 0–7). Die dort definierten Frontmatter-Felder und
`Store`-Signaturen sind ab jetzt Contract für P2 (drei einmalige, freigegebene Erweiterungen in
P2 Step 2 — siehe P2-Plan §0.4 Punkt L).

**Gelockte Rahmenentscheidungen (Nikinger, 2026-07-24, Browser-Planung):**

| # | Thema | Lock |
|---|---|---|
| R1 | Plan/Ausführung | Planung im Browser-Chat, Ausführung in Claude Code — wie im Trading-Bot-Projekt. |
| R2 | Plan-Tier | Beide Nutzer auf **Claude Pro**. Custom Connectors sind auf Pro verfügbar; jeder fügt seinen Connector selbst hinzu (kein Owner-Gate wie bei Team/Enterprise). `[VERIFY]` bei Ausführung gegen die aktuelle Doku. |
| R3 | Erreichbarkeit | **CGNAT** (RUT X50, Mobilfunk). Start mit **Cloudflare Tunnel** (schnellster Weg zum ersten Erlebnis), Migration auf **VPS + WireGuard** als P3-Option. Der MCP-Server ändert sich dabei nicht. **[2026-07-28 Ergänzung, P4 Step 0]:** Gebaut wurde stattdessen **Tailscale Funnel** (P3-A) — weder Cloudflare Tunnel noch VPS+WireGuard. Die Beschlusslage oben bleibt historisch korrekt stehen; Details zum tatsächlichen Weg: `docs/concepts/phase3_edge_plan.md` §0.4. |
| R4 | Vertraulichkeit | Bewusst akzeptiert: bei Cloudflare Tunnel terminiert Cloudflare TLS und sieht Klartext. **Kein E2E.** Der Server muss lesen können, damit Claude lesen kann — das schließt das Krypto-Modell des `Notizheft_example.html` aus. **[2026-07-27 Ergänzung, P3 Step 0]:** Ab P3 läuft der Weg über Tailscale Funnel; dort terminiert die Node selbst TLS, siehe `docs/concepts/phase3_edge_plan.md` §0.4. Der Relay-Betreiber sieht Notizinhalte damit nicht mehr im Klartext — „kein E2E" bleibt trotzdem richtig, denn Tailscale bleibt vertrauenswürdige Infrastruktur (Koordinationsserver, DNS, Relays). |
| R5 | Auth v0 | Token im Pfad (`/mcp/<token>`), Token = Identität = Space. Ehrlich benannter Kompromiss (Bearer-Passwort in einer URL, landet in Logs). **OAuth 2.1 + DCR ist Phase 4**, nicht optional-für-immer. **[2026-07-30 abgelöst, P4 Schnitt:]** Der Pfad-Token existiert nicht mehr — `TokenPathASGI` ist aus dem Code entfernt, beide Pfad-Token live widerrufen, `SPACE_AUTH_MODE` lässt nur noch `oauth` zu. Der Connector authentifiziert sich seither über OAuth 2.1 + DCR (Passwort + TOTP), siehe P4. |
| R6 | Zweck | **Lernprojekt**, später evtl. Arbeitswerkzeug. Bei Zielkonflikt gewinnt Lerneffekt über Bequemlichkeit — außer bei Safety/Secrets, dort gewinnt immer die sichere Variante. |

**Noch nicht entschieden (bewusst offen, für spätere Planungssessions):**
- ~~MCP-Werkzeug-Ergonomie, fünf offene Punkte~~ **[2026-08-20 geplant und gelockt]** — jetzt
  Block A von Phase 6.5 (`docs/concepts/phase6_5_tools_images_plan.md` §3, Entscheidungen
  P6.5-A–P6.5-H u. a.). Kein offener Planungsbedarf mehr — nur noch **nicht gebaut**. Der
  Absatz unten bleibt als Herkunftsnachweis stehen.
- ~~Item-Verschieben zwischen Ordnern und Spaces~~ **[2026-08-17 geplant und gelockt]** —
  `phase6_shares/ITEM_MOVE_PLAN.md` §4 (Step 7b, Space-Move, Entscheidungen P6-AD–AJ) + §9
  (Mehrfachauswahl, P6-AK–AN) sind ausführungsreif und per Nikinger-Freigabe gelockt. Kein
  offener Planungsbedarf mehr — nur noch **nicht gebaut**. Details:
  `phase6_shares/CLAUDE.md`s aktuellem Session-Block.
- **MCP-Werkzeug-Ergonomie, Live-Feedback (2026-08-14, sechs Punkte):** Bulk-Append, `list_spaces` auffindbarer, `patch_item`-vs-`update_item`-Aufgabenteilung, `get_item_meta`-Trennung vom vollen Body, Status-Enum-Doku in der Tool-Beschreibung, Suchtreffer-Robustheit. Der eine Bug (irreführende `patch_item`-Fehlermeldung „0 Treffer — lies das Item neu“ auf Frontmatter-Feldern; `patch_item` erreicht Frontmatter grundsätzlich nicht) ist am 2026-08-14 behoben (Text nennt jetzt die Ursache + `update_item` als Alternative, keine Frontmatter-Erkennungslogik). Übrige fünf Punkte: Phase 6.5 Block A, gelockt in `phase6_5_tools_images_plan.md` Abschnitt 3. Volltext: `phase6_shares/CLAUDE.md` Vormerkungen.

**[2026-08-02 Korrektur]** Web-UI-Planungs-Entscheidung **P5-V** (Neubau mit Ernte aus `notiz_heft_example.html`): Layout + `sanitizeHtml`/`markdownToHtml` übernommen; Vault-Encryption (R4-inkompatibel), `localStorage` und `connect-src 'none'` verworfen. **[2026-07-28 Korrektur]** Kollege-Frage (eigener Prozess vs. eigener Space) ist seit P3-G entschieden und live bewiesen: **ein Prozess, ein Space je Person** — zwei Spaces real (`niklas`, `fabian`) über denselben `sharefyx-mcp.service`.

---

**[2026-09-10, P8.6 Migration-Vorbereitung — Proxmox-Aktionsliste dokumentiert, Mini-PC → Proxmox i5-14600KF steht bevor; zwei „would be cool"-Zukunfts-Notes notiert; nur Doku, kein Code-Touch.** Mini-PC `savefyx-VMware-Virtual-Platform` ist **noch** der aktive Host (sharefyx-mcp.service PID 355956, `ActiveEnterTimestamp=2026-09-05 16:10:18 CEST`); der Nikinger wird die Services selbst pause, sobald er so weit ist. **7-Schritte-Aktionsliste** (Aktion → Befehl, Nikinger-fokussiert) jetzt im Phase-Head §Vormerkungen unter „Proxmox-Migration — Aktionsliste (Nikinger, 2026-09-10)": (1) `sudo systemctl stop sharefyx-mcp` + `tailscaled`; (2) VM migrieren (`qm migrate` oder shutdown+move); (3) `qm set --cores 12 --memory 16384 --balloon 0 --cpu host` + CPU-Pinning `affinity: 0-5,12-15` für i5-14600KF (Ryzen 7 5800X ohne Pinning); (4) `apt install -y ollama` + `ollama pull internvl2.5:8b` (in der migrierten VM); (5) `phase8_6_ui_polish/scripts/vision_ollama.py` als opencode/M3-Build-Auftrag (~50 Z. Python, `POST /api/generate` mit base64); (6) V119-Smoke gegen `c4_p8519_01_radiogruppe_im_dialog.png`; (7) `sudo systemctl start tailscaled sharefyx-mcp` + `health_gate.sh` 8/8. **Zwei Nikinger-„would be cool"-Zukunfts-Notes** (§Vormerkungen „Zukunfts-Notes außerhalb des aktuellen Phasen-Scopes"): (1) **Tab-Meta-Texte dynamisch** (`<title>sharefyx - {item_title}</title>`, UI-only, **[VERIFY] V120** Trigger-Events offen); (2) **Custom 404-Seite** im App-Stil (Vorsicht: `webui/api.py` ist im P8.6-Tabu §0.3, gehört in eine Folge-Phase P9+). **Co-Edits im selben Commit** (Hard-Rule-8): `phase8_6_ui_polish/CLAUDE.md` §Vormerkungen erweitert + neuer Session-Subblock; `phase8_6_ui_polish/SESSIONS_ARCHIVE.md` mit rotiertem Step-V-deferred-Vorgänger befüllt (P8.6-T-Rotationsregel); `docs/concepts/phase8_6_ui_polish_plan.md` §2 Korrekturnotiz um Verweis auf die Aktionsliste ergänzt; `docs/PROJECT_SESSION_LOG.md` mit rotiertem P8.6-Step-0-Vorgänger befüllt. **Selbstprüfung:** `pytest` 964/964 (V107 ✅, kein Python-Touch), `ui_budget.py` 5/5 130,1 KB (V97 ✅, kein `webui/static/`-Touch), Tabu-Diff §0.3 leer, Service-Touch 0 — PID 355956 nur gelesen via `systemctl status --no-pager`. Vorheriger Current-state-Absatz (P8.6 Step 0) verbatim nach `docs/PROJECT_SESSION_LOG.md` rotiert.

**[2026-09-10, P8.6 Step V deferred — Proxmox-Migration + lokales Modell (InternVL 2.5 8B); Plugin-Pfad übersprungen.** Nikinger-Entscheidung: `InternVL 2.5 8B` (Apache-2.0, Q4, ~6–8 GB VRAM) auf Ollama-Basis statt Anthropic-Haiku-API. Begründung: Proxmox-VM-Migration trivial, lokales Modell vermeidet Vendor-Lock-in + Audit-Trail-Aufwand. Proxmox-Settings (i5-14600KF primär, Ryzen 7 5800X sekundär) + Modell-Recherche (InternVL/Qwen3-VL/Llama/MiniCPM/Moondream) im Phase-Head §Vormerkungen. **Nächster Schritt:** Proxmox-Migration + Ollama-Setup + MCP-Wrapper-Skript (jetzt in dieser Session dokumentiert).

---

**[2026-09-10, P8.6 Block A ✅ — Fundament: Radiogruppe→`<select>`, sechs neue Tokens, `--border-soft`→`var(--line)`, Konvention v3 um „Vorsicht".** Erste echte Code-Touch-Session der Phase. **Tabu-Diff §0.3 leer, `pytest` 964→966, `ui_budget.py` 5/5 (130,4 KB gzip).** Nikinger hat die P8.5-19-Radiogruppe am 2026-09-08 selbst zurückgenommen. A1 `<select class="input">` mit Beschriftung-in-der-Box, `localStorage["sfx:linkpicker:mode"]` unverändert. A2 sechs neue Tokens in `:root`, fünf rohe `rgba(62,141,243,…)` außerhalb `:root` (`app.css:421/703/737/805/1311`) durch Tokens ersetzt, Z. 805 zusätzlich von `.35` auf `--select-line` (`.40`) angeglichen (V109); `--bg-void` an genau drei Stellen (body, `.list__empty`, `.overview__graph-empty`, P8.6-E). A3 `--border-soft` (undefiniert, Step-0-Fund) an `app.css:1290/1296` durch `var(--line)` ersetzt. A4 Konvention v3 um die **fünfte** Kategorie „Vorsicht" (`color: var(--caution)`, **keine** gefüllte rote Fläche). **+2 statische Tests** (P8.5-Test ersetzt, `test_no_raw_accent_rgba_outside_root` P8.6-C, `test_every_css_var_reference_is_defined` P8.6-A3 — hätte `--border-soft`-Bug gefunden). **Abweichung von Plan §3.5/§8.2 dokumentiert:** die anderen 4 Tests gehören zu Block B/C und werden dort geschrieben. Phase-Head + INDEX + Wurzel-`CLAUDE.md` jeweils über dem 40-KB-Softcap (Vorbild-Mechanismus aus P8-P/Phase 6.5).

**[2026-09-10, P8.6 Open Item #5 — Aktionsliste Schritt 7 auf Restart-Logik verkürzt; nur Doku, kein Code-Touch.** Restart-Logik verifiziert durch Lesen von `/etc/systemd/system/sharefyx-mcp.service` (`Restart=on-failure` + `RestartSec=5`) und `/usr/lib/systemd/system/tailscaled.service` (Vendor-Unit, ebenfalls `Restart=on-failure`); beide `WantedBy=multi-user.target`. Schritt 7 auf nur Health-Gate reduziert; neue Vormerkung „Restart-Logik" mit V103-Notiz für den späteren Deploy; `## Nächste Session` aktualisiert. Phase-Head-Sub-Blöcke verbatim nach `SESSIONS_ARCHIVE.md` rotiert (P8.6-T). Tabu-Diff §0.3 leer, Service-Touch 0 — sharefyx-mcp PID 991 unverändert.

---

**[2026-09-10, P8.6 Block D ✅ [D1/D2/D4] — V102-Dedup, FNV-1a-Layout-Seed, `cancelAnimationFrame` in `runSimulation()`; Tabu-Diff §0.3 leer, pytest 966 unverändert.** Reiner `graph.js`-Commit (8,4 KB, +0,5 KB). **D1 (P8.6-N):** `dedupeEdges()` mit ungeordnetem Knotenpaar als Schlüssel (`Object.create(null)` als Map, `kind` des ersten Treffers gewinnt) ersetzt die Roh-Übernahme in `loadGraph()` — keine neunte P1-Contract-Öffnung (Server dedupliziert bewusst nicht). **D2 (P8.6-M):** `seedJitter(id, salt)` als FNV-1a 32-Bit ersetzt `Math.random()-0.5` in `seedInitialPositions()` — Ring nach Index war schon deterministisch, nur der Jitter war es nicht; „Karte fliegt" (Nikinger 2026-09-06) ist behoben, **selbe Daten ⇒ selbes Bild**. **D4 (P8.6-§6.4, einzige Scope-Erweiterung des Plans):** `activeRafId` von lokal auf Modulebene gehoben, `runSimulation()` ruft am Anfang `cancelAnimationFrame(activeRafId)` (sofern vorhanden) — jedes wiederholte Öffnen der Übersicht startet **keine** zweite Simulationsschleife mehr; direkte Ursache der §2.4-Verschlimmerung behoben, drei Zeilen Fix, „schon halb da". Streichen, wenn der Nikinger es in der Sichtprüfung anders sieht. **D3 🟡** wartet auf Block C (V112-Gegenprobe nach C3-Umbau). **Keine** neuen `pytest`-Tests (dedup + seed + cancel sind interne `graph.js`-Helfer, Vorhandensein + `node`-Skript-Probe 9/9 ausreichend). **Hard-Rule-8-Doku-Update:** Phase-Head Modul-Status Z.6 `⬜`→`✅ (D1, D2, D4) · 🟡 (D3)`; Phase-Head Session-Block (Block A → `SESSIONS_ARCHIVE.md`); Frontmatter-Pipe; `docs/INDEX.md` Phase-8.6-Zeile + Frontmatter-Pipe; `ROADMAP.md` P8.6-Zeile. **Selbstprüfung §0.5:** Tabu-Diff leer; `pytest` V107 ✅ **966 unverändert**; `node --check` auf `graph.js` OK; `ui_budget.py` V97 ✅ 5/5 (130,4 KB gzip); Service-Touch 0. **Nächster Schritt:** Block B nach Plan §4 (B1 Hover-Vereinheitlichung, B4 `action--caution`-Klasse an Abmelden + Archivieren) oder Block C nach Plan §5 (Struktur-Umbau: Konto→Einstellungen, Alle Items unter Spaces, Map als rechte Spalte, klickbare Spaces, Ordner-Zähler — danach D3-Nachzug). Items #2/3/4 aus dem Handover bleiben blockiert (`ollama list` → `command not found`).


