---
status: archive
purpose: L3-Archiv der `updated:`-Fäden des Phase-10.5-Heads — die älteren Einträge der Kette, verbatim, newest-first
read-when: beim Audit, wenn nachvollzogen werden soll, wann welcher Block der Phase 10.5 gebaut wurde
detail: L3
up: ./CLAUDE.md
down:
updated: 2026-10-24 (ein Faden der `updated:`-Kette des Phase-10.5-Heads rotiert — Block 11.2 folgt im Head) | 2026-10-24 (ein Faden der `updated:`-Kette des Phase-10.5-Heads rotiert — Block 11.1 folgt im Head) | 2026-10-24 (ein Faden der `updated:`-Kette des Phase-10.5-Heads rotiert — Block 10.5 folgt im Head) | 2026-10-24 (zwei Fäden der `updated:`-Kette des Phase-10.5-Heads rotiert — Block 10.3 LG-2 Realtime-Client folgt im Head) | 2026-10-24 (zwei Fäden der `updated:`-Kette des Phase-10.5-Heads rotiert — Block 10.2 LG-2 Realtime serverseitig folgt im Head) | 2026-10-24 (drei Fäden der `updated:`-Kette des Phase-10.5-Heads rotiert — Block 10.1 LG-1 Volltext folgt im Head) | 2026-10-24 (11 Fäden der `updated:`-Kette des Phase-10.5-Heads rotiert — der Head stand bei 43.545 B und damit über dem Softcap) | 2026-10-23 (angelegt — die `updated:`-Kette des Phase-10.5-Heads rotiert hierher; im Head bleibt der neueste Faden plus Zeiger)
---
- 2026-10-24 (Block 11.1: der vendorte Editor — CodeMirror 5.65.16, fünf Dateien statt drei (gemessen), 71.280 B gzip; Wächter mit Gegenprobe) | ältere Einträge: phase10_5_finishing/UPDATES_ARCHIVE.md
- 2026-10-24 (Block 10.5: die Probe ist grün — Volltext 0 → 1 Treffer, Latenz 141,1 ms, P10.5-S-Band, Shutdown 5,22 s; P10.5-45/46/47/48 ✅, Gegenlauf rot) | ältere Einträge: phase10_5_finishing/UPDATES_ARCHIVE.md
- 2026-10-24 (Block 10.3 LG-2 Realtime-Client gebaut — `realtime.js`, Poll-Rückfall 120 s, Hinweisband P10.5-S; 8 Wächter, ui_budget 5/5) | ältere Einträge: phase10_5_finishing/UPDATES_ARCHIVE.md
- 2026-10-24 (Block 10.2 LG-2 Realtime serverseitig gebaut — `webui/events.py`, Route `GET /api/v1/events`, Lifespan, `timeout_graceful_shutdown=5`; 16 neue Tests, 6 Gegenläufe) | ältere Einträge: phase10_5_finishing/UPDATES_ARCHIVE.md
- 2026-10-24 (Block 10.1 LG-1 Volltext gebaut — API-Parameter `in_body`, Schalter am Suchfeld, 2 Tests + 6 Wächter, 3 Gegenläufe rot) | ältere Einträge: phase10_5_finishing/UPDATES_ARCHIVE.md
- 2026-10-24 (Block 9.3 RE-3 `rename_space` gebaut und gemessen — nur Team-Spaces (P10.5-M), ein Commit, Fremdverweise gemeldet statt angefasst; Wegwerf 15/15)
- 2026-10-24 (Block 9.2 RE-4 `rename_folder` gebaut und gemessen — Kern + Web-Route `PATCH …/folders` + UI-Kontextaktion, Wegwerf-Probe 13/13; **der Plan-Testname `test_rename_folder_by_owner_and_team_writer` ist als zwei Tests gebaut** (Gegenlauf braucht getrennte Tests))
- 2026-10-24 (Block 9.1 RE-7 `created_by` gebaut und gemessen — zwölfte P1-Öffnung, Wegwerf-Probe 12/12, 4 Regel-Wächter mit Gegenläufen; Deploy C `v3.1.7` vorbereitet, `deploy.sh` beim Nikinger) | ältere Einträge: phase10_5_finishing/UPDATES_ARCHIVE.md
- 2026-10-24 (Deploy C `v3.1.7` vorbereitet — Badge, eigener `## 2026-10-24`-Block im Update-Log, Suite 1425 grün, `doc_health` 0, `ui_budget` 5/5; `deploy.sh` beim Nikinger)
- 2026-10-24 (Block 8 gebaut — die Gehirnkarte C2: Lappen/Furchen/Zellen/Aktivierung, KA-2 Layout merken, KA-3 Suche/Filter, reduced motion 0 Frames; Browser-Probe an der 200-Knoten-Wegwerf-Instanz 4/4 mit 3 roten Gegenläufen; **drei Fehler fand erst der Browser** (gezogener Knoten wurde zurückgezogen · Fokus überlebte den Zeiger · Layout-Hinweis überschrieb die Trefferzahl) — behoben und gewächtert; Smoke 5/5; Suite 1422 grün; Abnahmestand 34 ✅ · 0 ⚠️ · 27 ⬜)
- 2026-10-24 (Block 7.4 (UI-4) umgesetzt — die vier Posten der Sichtung gebaut und an der Wegwerf-Instanz gemessen: Wortmarken-Abstand 2,5 px · „Zugewiesen"-Auswahl mit den Kanten der Suchzeile · Update-Banner als einzeilige Leiste (49 px) mit dem Knopf „Alle Änderungen" · Versionsanzeige 11 px (Punkt 203/255 statt 155/255); Wächter 8/8 mit 4 Gegenproben, Probe 5/5 mit 5 roten Gegenläufen; P10.5-32 bleibt ⬜ bis zur Bestätigung)
- 2026-10-24 (Session-Schluss: Handover für 7.4-Umsetzung, Block 8, Deploy C; Rotations-Fallstrick notiert)
- 2026-10-24 (Block 7.4: Sichtungsliste des Nikingers notiert — 4 Posten im Archiv Schritt 7.4, Ausführer setzt um, Nachsichtung nach Block 11)
- 2026-10-24 (Block 7.5 Kontrast (`--caution` #F06A6E, Wächter), 7.6 Assignee-Filter (API + Auswahl), 7.7 KA-5 (Chip + Karten-Ring) gebaut; Probe an der Wegwerf-Instanz 6/6 mit zwei roten Gegenläufen; Suite 1396 grün; Abnahmestand 30 ✅ · 0 ⚠️ · 31 ⬜)
- 2026-10-23 (Block 7.3 (UI-3) gebaut: der Tab-Titel folgt der Ansicht — Übersicht, Space-Name, Item-Titel, Einstellungen; datierte Korrektur zum Plan (vier Zustände, nicht fünf); Probe an der Wegwerf-Instanz 6/6 mit rotem Gegenlauf; Abnahmestand 27 ✅ · 0 ⚠️ · 34 ⬜)
- 2026-10-23 (Block 7.2 (UI-2): die Wortmarke `static/logo.svg` — Variante B aus dem Logo-Board, pixelgleich gemessen; zwei Befunde nur durch Messung (XML-Kommentar, MIME-Typ); Probe an der Wegwerf-Instanz mit rotem Gegenlauf; Abnahmestand 26 ✅ · 0 ⚠️ · 35 ⬜)
- 2026-10-23 (Deploy B ist live: `v3.1.6`, Release `20261023T165838.591015Z`, SHA `e5c834e`, health_gate 9/9 OK; Block 7.1 (UI-1) gemergt (`f0e76b0`) — kommt mit `v3.1.7`)
- 2026-10-23 (Block 7.1 (UI-1) gebaut: HTML-404 für unbekannte `/ui`-Pfade + JSON-404 in der API — Branch `p105-block7`, nicht gemergt; 4 neue Tests, 4 Gegenläufe wirksam; Suite 1384 grün)
- 2026-10-23 (Ketten-Defekt in `SESSIONS_ARCHIVE.md` behoben — eine Zeile `)pdated:` → `) | `; Release-Tests wieder grün, Suite 1380 grün) | ältere Einträge: phase10_5_finishing/UPDATES_ARCHIVE.md
- 2026-10-23 (Block 7 Schritt 7.0: die Update-Log-ID — Zähler von unten, der Banner beim zweiten Deploy am selben Tag; Generalprobe 26/26 grün, Suite 1380 grün)
- 2026-10-23 (Deploy-B-Generalprobe 25/25 Zellen grün an der Wegwerf-Instanz — Probe `probes/p105_deploy_b_probe.py`, Suite 1376 grün; Deploy B beim Nikinger)
- 2026-10-23 (Deploy B `v3.1.6` vorbereitet — Badge, eigener `## 2026-10-23`-Block im Update-Log, Venv `fastmcp 4.1.3` = `constraints.txt`, Suite 1376 grün)
- 2026-10-23 (Deploy A `v3.1.5` live — Gate 9/9, Release `20261023T065010.377336Z`; P10.5-26 geklärt; Merge `p105-block5` → `main`)
- 2026-10-23 (P10.5-26 ✅ — opencode führt `list_spaces` aus; die zwei Auslöser lagen im Messgerät (Stub-Endlosschleife, `mcp debug` vor dem Lauf), kein Produktcode)
- 2026-10-22 (Block 6 ✅ — Anbieter PA-1/PA-2, `/mcp` ohne Slash, PA-6; V209/V197 gemessen, Suite 1374 grün)
- 2026-10-22 (Block 5 **abgeschlossen** — `fastmcp==4.1.3` + neu erzeugte `constraints.txt`, Suite 1354 grün mit Compat an und aus, `append_to_items` (LG-4) + Log-Feld `proto`, Protokoll-Probe beider Ären, Smoke 17/17; Abnahme 10-19/20/21 ✅, 10-22 beim Nikinger nach Deploy B)
- 2026-10-22 (Block 4 **abgeschlossen** — Schritt 4.6: M2-Bench **Median 107,3 ms** (Z1 ≤ 300 ms), Event-Loop-Probe `/health` hinter `/overview` **23 ms** (P10: 4757 ms), Browser-Probe Z2/Z3/Z4 (150 ms → kein Platzhalter, 400 ms → Platzhalter); Abnahme 10-14/15/16/17 ✅, 10-18 bleibt beim Nikinger nach Deploy A)
- 2026-10-22 (Block 4 Schritte 4.3/4.4: der Client holt nur noch `/overview`, `focus`/`visibilitychange` bekommen 10 s Mindestpause (PF-4) · neu `static/js/loading.js` (`withLoading`, 200 ms) + `.is-loading`-Gerüst in `app.css`, statisch unter `prefers-reduced-motion` (Z3/Z4) · 7 Wächter in `phase5_ui/tests/test_loading_state.py`)
- 2026-10-22 (Block 4 Schritte 4.1/4.2: `_overview()` in **einem** `store.search()`-Durchgang (P10.5-G) + `asyncio.to_thread` in `_overview`/`_items_get`/`_graph_get` (Z2); 4 neue Tests (Parität, Rückfall, folders/members, Event-Loop) + 5 Gegenläufe; Suite 1334 grün)
- 2026-10-22 (Block 3 Schritte 3.3–3.4: `scripts/asset_orphans.py` (LG-7) + 7 Tests + Wegwerf-Probe `p105_b3_assets_probe.py` **14/14 Zellen** — Abnahme 10-12/10-13 ✅)
- 2026-10-22 (Block 3 Schritt 3.2: `Store.put_asset()` ruft den Stripper — **eine** Stelle für Web und MCP; die Dummy-PNG-Fixtures mussten zu echten Bytes werden)
- 2026-10-22 (Block 3 Schritt 3.1: `files.strip_image_metadata()` — JPEG/PNG/WebP, GIF unverändert, fail-closed; 8 neue Tests)
- 2026-10-22 (Block-2-Nachzug: Item mit **neuem Ordner** im fremden Home-Space ist jetzt auf Web **und** MCP gesperrt (Nikinger-Entscheidung 2026-10-22) — P10.5-9 ⚠️ → ✅; `ui_budget.py`/`ui_smoke.py` haben das Home-Space-Prädikat, die `team`-Flags stimmen)
- 2026-10-22 (Block 2.5 — Proben Web × MCP 28/28, M4 BG-1 behoben; Block 2 ✅, Abnahme 10-8/10/9 ✅, 10-9 ⚠️ (Befund: neuer Ordner per Item-Anlage im fremden Home-Space))
- 2026-10-22 (Block 2 Schritte 2.1–2.4 gebaut — eine Regel für Web und MCP (RE-1/RE-2/P10-I/P10.5-N) und BG-1; **2.5 Proben offen, Claude Code**; Suite 1299 grün)
- 2026-10-22 (Block 2 Schritte 2.1–2.2: eine Regel für Web und MCP — SharePolicy mit Home-Space-Prädikat, RE-1 Ordner anlegen, RE-2 Ordner wechseln, P10-I/P10.5-N beide Richtungen; Suite 1296 grün)
- 2026-10-22 (Block 2 Schritt 2.1: SharePolicy kennt Home-Spaces und Team-Spaces, Prädikat aus der Auth-DB, eine Regel für Web und MCP)
- 2026-10-22 (Block 1 **abgeschlossen**: V200 vom Fleet-Lauf belegt — Unit installiert, `Result=success`, 0 failed units; Abnahme 10-5/6/7 ✅)
- 2026-10-22 (Block 1 Schritte 1.1/1.2: BT-1 — Caddy-Vorlage in Blockform mit den V199-Live-Werten (10s/15s/1s) + neuer Waechter; Abnahme 10-5 auf ✅)
- 2026-10-22 (Block 1 Schritt 1.4: BT-6 — `constraints.txt` aus dem Live-Freeze, `scripts/dev_install.sh` mit `-c`, zwei Wächter, Dev-venv neu; Suite 1282 gruen auf den Live-Versionen)
- 2026-10-22 (Block 1 Schritt 1.3: BT-2 — `SuccessExitStatus=143` in der Relay-Unit, Wächter 13/13, vier Gegenläufe; Block-0-Block rotiert)
- 2026-10-22 (Block 0 **abgeschlossen**: 0.6 ROADMAP-Zeile P10.5 auf 🔄, 0.7 Ausführer-Vorbedingung protokolliert — Abnahme P10.5-1–4 ✅)
- 2026-10-22 (Block 0: 0.2/0.3 — Phase-Head angelegt (Modulstatus, Deploy-Tabelle, Abnahmestand 61 Zeilen), DO-3-Wächter, `pytest.ini` ergänzt; davor 0.4 (ROADMAP-Wächter eingefroren), 0.5 (INDEX-Luft) und 0.8 (Register-Luft) gebaut — DO-2 vollständig; erster Block)
# Phase 10.5 — Updates-Archiv

Hier stehen die **älteren `updated:`-Fäden** des Phase-10.5-Heads, **verbatim** und newest-first —
rotiert am 2026-10-23 mit `scripts/rotate_index_updates.sh` (fünf Gegenproben vor dem Schreiben).

**Warum:** der Head trug 22 Fäden (4.471 B) in einer einzigen Frontmatter-Zeile — ein Drittel der
Datei, und jeder neue Block kam mit einem weiteren Faden darauf. Der Rotationsanker sieht nur den
Fadenanfang, deshalb bleibt im Head der **neueste** Faden stehen plus der Zeiger auf dieses
Archiv; die älteren wandern hierher. Dieselbe Form wie beim Phase-9-Head
(`phase9_hardening/UPDATES_ARCHIVE.md`).

**Die Kette im Head ist damit wieder kurz genug, dass DO-3 (Session-Block ≤ 4 KiB) die bindende
Grenze ist** und nicht der 40-KiB-Softcap des Heads.
