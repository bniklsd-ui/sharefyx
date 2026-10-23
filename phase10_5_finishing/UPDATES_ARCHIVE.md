---
status: archive
purpose: L3-Archiv der `updated:`-Fäden des Phase-10.5-Heads — die älteren Einträge der Kette, verbatim, newest-first
read-when: beim Audit, wenn nachvollzogen werden soll, wann welcher Block der Phase 10.5 gebaut wurde
detail: L3
up: ./CLAUDE.md
down:
updated: 2026-10-23 (angelegt — die `updated:`-Kette des Phase-10.5-Heads rotiert hierher; im Head bleibt der neueste Faden plus Zeiger)
---
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
