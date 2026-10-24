---
status: live
purpose: Phase-10.5-Head — Modulstatus der Blöcke 0–12/Z, Deploy-Tabelle A–D, Abnahmestand P10.5-1–61, offene Punkte beim Nikinger, aktueller Session-Block. Plan und Arbeitsliste stehen in eigenen Dateien.
read-when: Arbeiten in phase10_5_finishing/ — zuerst lesen, zusammen mit dem Session-Block unten
detail: L2
up: ../ROADMAP.md
down:
  - ../docs/concepts/phase10_5_finishing_plan.md    # 📕 der Plan: Locks P10.5-A–W, Blöcke 0–12/Z, Abnahme, [VERIFY] V207–V219
  - ../phase10_inventory/BAUSTELLENREGISTER.md      # 📗 die Arbeitsliste — hier wird abgehakt (P10-B)
  - ../phase10_inventory/ENTSCHEIDUNGEN_ARCHIVE.md  # 📦 §12 Entscheidungsliste D-1–D-18, verbatim
  - SESSIONS_ARCHIVE.md                             # 📦 ältere Session-Blöcke, verbatim, newest-first
  - UPDATES_ARCHIVE.md                              # 📦 die älteren `updated:`-Fäden dieses Heads, verbatim
  - STARTUPTRAG_ARCHIVE.md                          # 📦 die Startaufträge der Blöcke 7 und 9, verbatim
updated: 2026-10-24 (Block 9.1 RE-7 `created_by` gebaut und gemessen — zwölfte P1-Öffnung, Wegwerf-Probe 12/12, 4 Regel-Wächter mit Gegenläufen; Deploy C `v3.1.7` vorbereitet, `deploy.sh` beim Nikinger) | ältere Einträge: phase10_5_finishing/UPDATES_ARCHIVE.md
---
# Phase 10.5 — Finishing

> **Auftrag:** P10.5 schließt jede Baustelle, die im Register als „Ziel P10.5" steht — Betrieb, Fehler, Parität, Performance, MCP-Schicht, Anbieter-Unabhängigkeit, Darstellung, Gehirnkarte, Umbenennen, Suche, Realtime, Editor Stufe 1+2 und Doku. Die Phase endet erst, wenn ein Nicht-Claude-Client live `list_spaces` ausführt, mit zwei Modellanbietern (P10-J); neues Feature kommt erst in P11.

## Freigaben

| Was | Wann | Wer |
|---|---|---|
| Plan `docs/concepts/phase10_5_finishing_plan.md` (Locks P10.5-A–W) | 2026-10-21 | Nikinger |
| Register-Tor **P10-8** — die Spalte „Ziel" wird verbindlich, abgehakt wird im Register | 2026-10-21 | Nikinger |
| **P10-C** — Eingriff in `phase4_auth/` (Lock **P10.5-O**): Loopback-Redirect mit Port, `application_type`, CSP `form-action` | 2026-10-21 | Nikinger |
| **P10.5-N** — P10-I in **beiden** Richtungen: kein Item wandert *in* einen fremden Home-Space hinein **und** nicht *aus* einem heraus | 2026-10-21 | Nikinger |
| Kontextgrenze **400.000** für `MiniMax-M3` und `MiniMax-M3.1-Flash` (P10.5-C, gesetzt von eurofyx-fleet, Neustart 22.10.) | 2026-10-22 | eurofyx-fleet |
| **Alles Messbare an der Wegwerf-Instanz** — Tests gegen die Live-Umgebung (echter `DATA_ROOT`, echte `auth.sqlite3`, Keyring, laufender Dienst, Funnel/Domain) nur, wenn der Server das nicht selbst entscheiden kann; die Entscheidung trifft der Nikinger (Wurzel-`CLAUDE.md` §Working style) | 2026-10-22 | Nikinger |

## Modulstatus

| Block | Inhalt (Register) | Wer | Deploy | Status |
|---|---|---|---|---|
| 0 | Haushalt: Verifikation, Phase-Head, INDEX-Luft, Register-Luft, DO-2, DO-3, Ausführer-Vorbedingung | Claude Code | — | ✅ 2026-10-22 — 0.1–0.8 gebaut, Abnahme P10.5-1–4 ✅ |
| 1 | Betrieb: BT-1, BT-2, BT-6 (+ `constraints.txt`) | Ausführer + Nikinger | A | ✅ 2026-10-22 — **1.1–1.4 gebaut und abgenommen** (V199 gelesen · BT-1 Caddy-Blockform · BT-2 `SuccessExitStatus=143`, live V200 ✅ · BT-6 `constraints.txt`); Abnahme 10-5/6/7 ✅, Suite 1283 grün |
| 2 | Fehler, Parität, Regel: BG-1, RE-1, RE-2, P10-I, AL-1 | Ausführer (+ Claude Code Proben) | A | ✅ 2026-10-22 — **2.1–2.5 gebaut und geprobt** (Probe 2.5: 28/28 Zellen Web × MCP, M4 0 → 3 Zeilen ohne neues Öffnen) · **Nachzug 2026-10-22 (Nikinger):** ein Item mit **neuem Ordner** im fremden Home-Space ist jetzt auf beiden Flächen gesperrt (RE-1-Parität) — P10.5-9 damit ✅ statt ⚠️ — eine Regel für Web und MCP: RE-1 Ordner anlegen, RE-2 Ordner wechseln, P10-I/P10.5-N kein Verschieben in **oder aus** einem fremden Home-Space; BG-1: die Space-Liste füllt sich nach, wenn `/overview` spät kommt) |
| 3 | Hygiene: LG-8 (P1-15), LG-7 | Ausführer | A | ✅ 2026-10-22 — **3.1–3.4 gebaut und geprobt**: `files.strip_image_metadata()` (JPEG/PNG/WebP, GIF unverändert, fail-closed `ValidationError`) + Aufruf in `Store.put_asset()` (**eine** Stelle für Web und MCP) · `scripts/asset_orphans.py` (LG-7, `--report`/`--move`, ein Commit) · 16 neue Tests · **Wegwerf 14/14 Zellen** (`probes/p105_b3_assets_probe.py`): GPS weg auf Web **und** MCP, Orientation bleibt, sauberes Bild byte-identisch, Waise gefunden und in den Papierkorb verschoben; Abnahme 10-12/10-13 ✅ |
| 4 | Performance: PF-1, PF-4, Z1–Z4 | Ausführer (+ Claude Code Proben) | A | ✅ 2026-10-22 — **4.1–4.6 gebaut und geprobt**: `_overview()` zählt alle Eimer aus **einem** `store.search()`-Durchgang (P10.5-G, Rückfall über `_STORE_FETCH_LIMIT`), `folders`/`members` wandern in die Antwort · `asyncio.to_thread` für `_overview`/`_items_get`/`_graph_get` (Z2) · Client: nur noch `/overview`, 10 s Mindestpause für `focus`/`visibilitychange` (PF-4) · neu `static/js/loading.js` + `.is-loading`-Gerüst (Z3/Z4) · **M2-Bench Median 107,3 ms** (vorher 2405,6) · **`/health` hinter `/overview` 23 ms** (P10: 4757 ms) · Browser: 150 ms → kein Platzhalter, 400 ms → Platzhalter; Abnahme 10-14/15/16/17 ✅, 10-18 beim Nikinger nach Deploy A |
| 5 | MCP-Schicht: PA-5 (FastMCP 4), LG-4 | Ausführer | B | ✅ 2026-10-22 — **5.1–5.6 gebaut und geprobt**: `fastmcp==4.1.3` (V207 ✅), `constraints.txt` neu aus frischem venv, Suite 1354 grün mit Compat an **und** aus (Warnungen als Fehler) · `proto` im Tool-Log (V219 ✅: `Context.request_context.protocol_version`) · neues Werkzeug `append_to_items` (LG-4, ≤ 20 Einträge, je Eintrag eigene `version`, Teilerfolg, Log `err:"partial"`) · Probe beider Ären in-process: `legacy` → `2025-11-25`, `auto` → `2026-07-28` · Smoke 17/17; Abnahme 10-19/20/21 ✅, 10-22 beim Nikinger nach Deploy B |
| 6 | Anbieter: PA-1, PA-2, `/mcp`, PA-6, P10-J | Ausführer + Claude Code + Nikinger | B | ✅ 2026-10-22 — **6.0–6.5 gebaut und gemessen**: zweite Vergleichsregel `http://127.0.0.1:<port>` (Port explizit, kein `localhost`/`[::1]`, P10.5-O) + `application_type` ∈ {fehlend, null, native, web} · CSP `form-action` mit `http://127.0.0.1:*` · `/mcp` **ohne** Slash exakt bedient (`_ExactMcpMount`, kein 307) · PA-6 (Wurzel-`CLAUDE.md` eine Zeile) · **V209 ✅** (opencode 1.19.4), **V197 ✅** (Chromium folgt dem Consent-Redirect) · **DCR-Gegenlauf**: derselbe Request 400 → **201** · Suite **1376 grün** (1354 + 22) · **10-23/10-24/10-25 ✅**, **10-26 ✅** (2026-10-23 geklärt: die zwei Auslöser lagen im Messgerät, kein Produktcode — siehe Session-Block), 10-27/28 beim Nikinger nach Deploy B |
| 7 | Darstellung: UI-1–UI-6, KA-5 | Ausführer (+ Claude Code Sichtung) | C | 🔄 2026-10-24 — **7.1–7.7 gebaut und gemessen** (HTML-404 für unbekannte `/ui`-Pfade · Wortmarke `static/logo.svg` · Tab-Titel folgt der Ansicht · vier Posten der Sichtung umgesetzt · Kontrast `--caution` 5,70:1 · Assignee-Filter in API und UI · `doing`-Ring auf der Karte) · Probe an der Wegwerf-Instanz, Gegenläufe je rot · **P10.5-32 bleibt ⬜ bis zur Bestätigung** — die Herleitung je Schritt steht im Session-Archiv (`SESSIONS_ARCHIVE.md`, Block 7.1–7.4) und in den Commits |
| 8 | Karte: Gehirnkarte C2 | Ausführer (+ Claude Code Smoke/Sichtung) | C | 🔄 2026-10-24 — **8.1–8.8 gebaut und gemessen** (Lappen/Furchen/Zellen/Aktivierung in `graph.js`, KA-2 Layout-Ablage, KA-3 Suche/Filter, reduced motion 0 Ticks) · **Browser-Probe `probes/p105_b8_karte_probe.py` an der 200-Knoten-Wegwerf-Instanz: 4/4 Messungen grün, 3 Gegenläufe je rot** · **Smoke `p8_22_smoke.py` 5/5** (Ruhe 2712,1 ms ≤ 3000, Frame p95 1,7 ms ≤ 16,7, reduced motion **0** Frames) · **drei Fehler hat erst der Browser gefunden** (gezogener Knoten wurde zurückgezogen · Fokus blieb nach dem Zeigerwechsel · Trefferzahl wurde vom Layout-Hinweis überschrieben) — alle drei behoben und gewächtert · **Abnahme 10-36/38/39/40 ✅, 10-37 wartet auf die Sichtung** (4 Screenshots liegen vor) · **Befund: das Plan-Budget für `graph.js` ist überschritten** (+11,1 KB gzip statt +8 KB; davon +9,8 KB Kommentar, der Code selbst +2,9 KB) — Entscheidung beim Nikinger · **drei Pfade außerhalb der §3-Liste** (bewusst, datiert): `phase9_hardening/scripts/graph_reload_probe.mjs` (der P9-Harness malt die alte Strichzeichnung — ohne Anpassung wäre der P9-Wächter rot) · `phase10_5_finishing/{probes,tests}/` (Plan 8.8 verlangt Proben und Wächter) · `docs/screenshots/p105_b8_*.png` (Plan 8.8 verlangt die vier Bilder für die Sichtung) |
| 9 | Rechte und Namen: RE-7 (P1-12), RE-4 (P1-13), RE-3 (P1-14) | Ausführer | D | 🔄 2026-10-24 — **9.1 RE-7 `created_by` gebaut und gemessen** (P1-Öffnung 12: `models.py`/`store.py`, MCP + Web + Editor-Metazeile; 8 neue Tests + 4 Regel-Wächter mit je einem Gegenlauf; Wegwerf-Probe **12/12**); **9.2/9.3 stehen aus** — Branch `p105-block9`, Merge **nach** Deploy C |
| 10 | Suche und Realtime: LG-1, LG-2 | Ausführer (+ Claude Code Proben) | D | ⬜ |
| 11 | Editor Stufe 1 + 2: ED-1, ED-2, ED-3 (P1-11), ED-5 | Ausführer (+ Claude Code Proben/Sichtung) | D | ⬜ |
| 12 | Doku und Altlasten: DO-1, LG-6, AL-1 (Rest), AL-3, BG-2/BG-3 | Claude Code | — | ⬜ |
| Z | Closeout P10.5 (Handover, Grafik, Rotationen) | Claude Code + Nikinger | — | ⬜ |

## Deploy-Tabelle

| # | Version | SHA | `health_gate` | Ausgabe |
|---|---|---|---|---|
| A | `v3.1.5` | `7358f22` | **9/9 OK** | nach Block 1–4 — **live seit 2026-10-23**, Release `20261023T065010.377336Z` |
| B | `v3.1.6` | `e5c834e` | **9/9 OK** | nach Block 5–6 (+ **Block 7.0**, die Update-Log-ID) — **live seit 2026-10-23**, Release `20261023T165838.591015Z` · **Deploy beim Nikinger** (Hard Rule 9, `sudo`; `deploy.sh main` → Release-Tests **1380 grün** (340,7 s) → Symlink-Wechsel → Dienst neu gestartet) · `health_gate.sh --expected-version=v3.1.6 --require-todays-update-log --expected-sha=e5c834e` → **9/9 OK** (`.rail__version` v3.1.6, Release-SHA `e5c834e…`, Update-Log 2026-10-23) · **Block 7.1 (UI-1) ist gemergt** (`f0e76b0`, aus `p105-block7`) — **nicht** in diesem Release, sondern in `v3.1.7` |
| C | `v3.1.7` | — | — | nach Block 7–8 — **2026-10-24 vorbereitet** (Badge, eigener `## 2026-10-24`-Block im Update-Log, Suite 1425 grün, `doc_health` 0, `ui_budget` 5/5), **`deploy.sh` beim Nikinger** |
| D | `v3.1.8` | — | — | nach Block 9–11 |

**Stand 2026-10-24 (Abend):** Deploy A ist **live** (`v3.1.5`, Release `20261023T065010.377336Z`, SHA `7358f22`, `health_gate` **9/9 OK**); der Branch `p105-block5` (Block 5 + 6 + P10.5-26) ist **gemergt**. **Deploy B ist ebenfalls live**: `v3.1.6`, Release `20261023T165838.591015Z`, SHA `e5c834e`, `health_gate` **9/9 OK** (aus `main` mit `fastmcp 4.1.3`; der Deploy lief beim Nikinger, die Release-Tests im Release **1380 grün** in 340,7 s). **Block 7.1 (UI-1) ist gemergt** (`f0e76b0`) und damit ab `v3.1.7` dabei. **Deploy C (`v3.1.7`) ist vorbereitet** — Badge, eigener Update-Log-Block `## 2026-10-24` (9 Zeilen für Menschen), Suite **1425 grün** (332,6 s), `doc_health` 0, `ui_budget` **5/5** (Erstaufruf 204,5 KB); **`deploy.sh` liegt beim Nikinger**. **Die Generalprobe davor ist gefahren: 26/26 Zellen grün an der Wegwerf-Instanz** (Details im Session-Block unten; die Zeile stand vorher auf „25/25" — **datierte Korrektur**, der Block-7.0-Commit hat die Probe um eine Zelle erweitert). **Der Deploy-Aufruf der letzten Session ist an den Release-Tests gescheitert — nicht am Befehl:** eine verklebte `updated:`-Zeile in `SESSIONS_ARCHIVE.md` (behoben, Details im Session-Block) — es fehlt nur noch der Deploy-Aufruf durch den Nikinger. **Block 7.1 (UI-1) ist gebaut** auf dem Branch `p105-block7` — **nicht gemergt** (Nikinger-Entscheidung: Deploy A vor dem Branch-Merge); der Merge wartet auf Deploy A/B.

**Ein Deploy ist vier Schritte, kein Commit** (Plan §2.5): volle Suite + `doc_health` + `ui_budget` grün · Badge und `docs/UPDATE_LOG.md` · Commit + Push · **`deploy.sh` durch den Nikinger** (Hard Rule 9) · `health_gate.sh` mit **echter Ausgabe** in den Commit — nie die Behauptung.

## Abnahmestand

**61 Zeilen** (P10.5-1–61). Zählregel (Plan §5): ✅ erfüllt mit Beleg am Ort · ⚠️ erfüllt in anderer Form, Abweichung benannt · ⬜ offen. Die Kriterien stehen wortgleich im Plan (je Block am Ende); die **Belegte** stehen im Commit und im Session-Block.

| # | Kriterium | Status | Beleg |
|---|---|---|---|
| P10.5-1 | Step-0-Bericht steht im Session-Block, `doc_health` 0 | ✅ | d5f6081 · doc_health 0 |
| P10.5-2 | DO-2: INDEX ≥ 3.000 B unter der Grenze; ROADMAP-Wächter eingefroren; **[Nachtrag 2026-10-21]** Register ≥ 3.000 B unter der Grenze (0.8); Suite grün | ✅ | d5f6081 · 3e15f9e · f7ad5d9 |
| P10.5-3 | DO-3: Wächter grün auf dem echten Head | ✅ | dieser Commit |
| P10.5-4 | Ausführer-Vorbedingung erfüllt und protokolliert (≤ 400 K) | ✅ | dieser Commit |
| P10.5-5 | BT-1: Vorlage trägt die Live-Werte (V199 ✅) | ✅ | 1.2 · this commit · V199: dial_timeout 10 s · try_duration 15 s · try_interval 1 s |
| P10.5-6 | BT-2: Unit installiert, `Result=success` bei Exit 143 (V200 ✅) | ✅ | 1.3 · Fleet-Lauf 2026-10-22: `Result=success`, 0 failed units, active |
| P10.5-7 | `constraints.txt` = Live-Stand; Dev-venv daraus grün; Wächter grün | ✅ | 1.4 · this commit · Freeze byte-identisch zur Datei, Suite 1282 grün auf `mcp 1.30.0` / `starlette 1.7.0` |
| P10.5-8 | BG-1: Die Liste füllt sich, sobald das verzögerte `/overview` ankommt, ohne Panel neu zu öffnen | ✅ | 2.5 · `probes/p105_m4_bg1.json`: 0 beim Öffnen → 3 nach 4 s, ohne neu zu öffnen; Gegenlauf 3; ohne Ereignis 0 |
| P10.5-9 | RE-1/RE-2: dieselbe Matrix auf Web und MCP | ✅ | 2.5 · `probes/p105_b2_rights.json`: Matrix gleich auf beiden Flächen, fremder Home mit `write:` ❌ für Ordner-Endpunkt und Ordnerwechsel · **Nachzug 2026-10-22 (Nikinger):** auch ein Item mit **neuem Ordner** im fremden Home-Space legt den Ordner nicht mehr an (Web 403 `forbidden`, MCP `write_denied`) — 3 neue MCP-Tests + 4 neue Web-Tests, Suite 1306 grün |
| P10.5-10 | P10-I auf beiden Flächen durchgesetzt | ✅ | 2.5 · `probes/p105_b2_rights.json`: in/aus fremdem Home ❌ (Web + MCP, Item bleibt an der Quelle), Team-Ziel ✅ |
| P10.5-11 | AL-1: Zeilen 14 und 29 geschlossen; Zeile 15 mit Weg beim Nikinger (Migration + Live-Check) | ✅ | 2.5 · Zeile 29: MCP-Move alpha→gamma ✅ · Zeile 14: fremder Body im geteilten read-Space gewrappt, Schreiben ❌ · Zeile 15 beim Nikinger |
| P10.5-12 | EXIF weg nach Upload über Web **und** MCP; Orientierung bleibt | ✅ | 3.1–3.2 + Wegwerf `probes/p105_b3_assets.json` (14/14): Web-Upload 148 B → 94 B, GPS-Marker **weg**, Orientation 6 **bleibt**, ICC bleibt · MCP-Upload 94 B, GPS weg, Orientation 6 · Gegenlauf: Bild ohne Metadaten byte-identisch (45 B = 45 B) |
| P10.5-13 | Verwaiste Asset-Ordner werden gefunden und nur auf Wunsch in den Papierkorb verschoben | ✅ | 3.3/3.4 + Wegwerf `probes/p105_b3_assets.json`: Item mit Bild → `DELETE` (Web) → `store.trash()` → `--report` findet **genau** die Waise (die lebenden Assets nicht) → `--move` verschiebt sie nach `._trash/<space>/_assets/<id>/` (nie gelöscht) mit **einem** Commit (5 → 6) · 7 neue Tests in `phase10_5_finishing/tests/test_asset_orphans.py` |
| P10.5-14 | Z1 im Bench: Median ≤ 300 ms (heute 2.405 ms) | ✅ | 4.6 · M2-Bench `p10_overview_bench.py` (4 Spaces × 50 Items, alle sichtbar): **Median 107,3 ms** (Läufe 106,2–109,7 ms, Streuung 3,2 %) — **22×** unter dem Ziel, **22,4×** schneller als die Grundlinie 2405,6 ms |
| P10.5-15 | Parität: neue Zähler = alte `search().total` je Eimer | ✅ | 4.1 — `test_one_pass_counts_equal_per_bucket_search_totals` (3 Spaces, alle fünf Eimer, leer) + `test_overview_falls_back_beyond_fetch_limit` (Grenze per Monkeypatch auf 2) · **fünf Gegenläufe**: Eimer `archived` ausgelassen → rot · kein Rückfall → rot · `folders`/`members` entfernt → rot · `to_thread` entfernt → rot · zweiter Durchgang → rot |
| P10.5-16 | Z2: kein Request wartet hinter `/overview` | ✅ | 4.6 · Event-Loop-Probe `probes/p105_b4_eventloop_probe.py`: `/health` hinter `/overview` **23 ms** (P10: 4757 ms), `blockade_health` **false** (P10: true) · Browser-Probe `probes/p105_b4_loading_probe.py`: `/overview` 2 s verzögert → Space-Wechsel **0,315 s**, Item-Öffnen **0,053 s** (Grenze 1 s) |
| P10.5-17 | Z3/Z4: Gerüst ≤ 1 s; Ladezustand genau ab 200 ms | ✅ | 4.6 · Browser-Probe: `DOMContentLoaded` **142,2 ms** (Grenze 1000 ms) · Z4 **beide Seiten der Grenze**: 150 ms → **kein** `is-loading` (0 Elemente), 400 ms → `is-loading` an `#list-overview`, sichtbar · **zwei Gegenläufe**: `delayMs` 0 → 150-ms-Fall rot · `delayMs` 1000 → 400-ms-Fall rot |
| P10.5-18 | Live nach Deploy A: `/overview` Waiting ≤ 300 ms, Space-Wechsel während des Polls ≤ 1 s (Nikinger, DevTools, beide Eingänge) | ⬜ | — |
| P10.5-19 | Suite grün mit Compat aus; Pin = installiert; `constraints.txt` neu erzeugt und Wächter grün | ✅ | 5.2 · `fastmcp 4.1.3` / `mcp 2.3.0` / `starlette 1.9.0`; Suite **1354 grün** mit `FASTMCP_MCP_CAMELCASE_COMPAT=false` und `-W error::DeprecationWarning`, ebenso mit Compat an · Dev-venv neu über `dev_install.sh -c constraints.txt`, Freeze = Constraints · **Gegenlauf:** `mcp 2.2.0` im Wegwerf-venv → `test_every_installed_distribution_matches_the_constraints` rot |
| P10.5-20 | Beide Ären in-process: `legacy` → `2025-11-25`, `auto` → `2026-07-28`, `list_spaces` ok | ✅ | 5.6 · `probes/p105_b5_protocol.json`, 8 Wächter in `tests/test_protocol_probe.py` · **Gegenlauf, gemessen statt angenommen:** `initialize` mit `1999-01-01` → der Server antwortet mit **seiner** `2025-11-25` (Handshake-Aushandlung, kein Fehler — der Plantext „`UnsupportedProtocolVersion`-Fehler" gilt nur für die zustandslose Ära) · `tools/list` mit Header + Envelope `1999-01-01` → `-32022 Unsupported protocol version`, `supported: ["2026-07-28"]` |
| P10.5-21 | LG-4: Tests + Smoke 17/17 | ✅ | 5.4/5.5 · 5 Tests `test_append_to_items_*` in `test_tools.py` (Gegenlauf `extra="forbid"` → `ignore` rot), 5 Log-Tests (`proto`, ohne Kontext, `partial` mit Fake und durch den echten Stack, Erfolg; beide Features per Gegenlauf wirksam), `test_app.py` zählt 11 Werkzeuge · `mcp_smoke.py` **17/17** (Check 17: ein Eintrag mit falscher `version` → `ok:1, failed:1`) |
| P10.5-22 | Live nach Deploy B: claude.ai-Connector `list_spaces`/`search_items`/`get_item`/`update_item` ok (Nikinger); Log-Feld `proto` zeigt die Ära (V208) | ⬜ | — |
| P10.5-23 | DCR: `native`/fehlend + `http://127.0.0.1:<port>/…` angenommen; `web` + Loopback, `localhost`, `[::1]`, ohne Port, `http://` fremd → abgelehnt; https-Regeln unverändert | ✅ | 6.1/6.5 · `clients.py` (zweite Regel + `application_type`), 16 neue Tests in `test_clients.py` + 2 in `test_flows.py` · **V209**: opencode 1.19.4 schickt `redirect_uris: ["http://127.0.0.1:19876/mcp/oauth/callback"]`, `application_type` **fehlt** → P10.5-O steht wie geschrieben (kein `localhost`, kein `[::1]`, kein Rückgabe-Auslöser) · **Gegenlauf am echten Client**: derselbe DCR-Request → vorher **400 `invalid_redirect_uri`**, jetzt **201** (`probes/p105_b6_dcr.json`, Baseline `p105_b6_dcr_baseline.json`) |
| P10.5-24 | V197: Chromium folgt dem Consent-Redirect zu 127.0.0.1 | ✅ | 6.2/6.6 · CSP `form-action 'self' https://claude.ai https://claude.com http://127.0.0.1:*` · **Chromium (Playwright) macht den Consent**: Login (Passwort + TOTP) → 302 auf `http://127.0.0.1:19876/mcp/oauth/callback` → Callback **erreicht**, opencode meldet „Authentication successful!“, **keine** CSP-Verletzung in der Konsole (`probes/p105_b6_opencode_e2e.json`) · **Gegenlauf:** ohne den CSP-Eintrag blockiert Chromium das Formular lautlos (`Sending form data to … violates … form-action`), der Callback kommt nicht an |
| P10.5-25 | `/mcp` ohne Slash: 200 mit Bearer, 401 ohne; kein 307 | ✅ | 6.3/6.5 · `_ExactMcpMount` + `Route("/mcp", …)` vor dem Mount (`mcpserver/app.py`) · Unit: `POST /mcp` **401 + WWW-Authenticate** (ohne Token), mit Token **kein 307** · Scope-Gleichheitstest gegen Starlettes `Mount` (root_path, app_root_path, `get_route_path()`) · **am echten Client**: opencode geht jetzt auf `POST /mcp` — vorher 307 und ein zweiter Versuch auf `/mcp/` (Proxy-Log vor/nach dem Fix) · **Gegenlauf:** exakte Route raus → beide Tests rot |
| P10.5-26 | Wegwerf-E2E: opencode führt `list_spaces` aus | ✅ | **2026-10-23** · `probes/p105_b6_opencode_e2e.json`: der Modell-Request trägt **11** MCP-Werkzeuge, opencode ruft `sharefyx_list_spaces` · Server-Log: `ev=tool, tool=list_spaces, ok=true, proto=2025-11-25` · **beide Verdachtsmomente vom 2026-10-22 sind widerlegt** (der `405` auf `GET /mcp` ist **nicht** die Ursache · der behauptete Werkzeugaufruf war **nicht** belegt — null `ev=tool` in der Logdatei) · **zwei Auslöser lagen im Messgerät** (Stub-Endlosschleife · `mcp debug` vor dem Werkzeuglauf) — **kein Produktcode**, P2-B unberührt |
| P10.5-27 | **Live P10-J Lauf 1** (M3.1 Flash) | ⬜ | — |
| P10.5-28 | **Live P10-J Lauf 2** (lokales Modell, CT 111) — mit 27 die Abschlussbedingung der Phase | ⬜ | — |
| P10.5-29 | UI-1: HTML-404 für unbekannte `/ui`-Pfade | ✅ | 7.1 · `phase5_ui/webui/pages.py :: render_not_found_page()` + `phase2_mcp/mcpserver/app.py` (Route **nach** allen `/ui`-Routen) · 4 neue Tests in `phase5_ui/tests/test_static_routes.py` gegen die **echte** `create_app()` · **4 Gegenläufe wirksam** (Fänger entfernt / vor die bekannten Routen / API-404 entfernt / global statt `/ui`) · **datierte Korrektur zum Plan**: „API bleibt JSON" war gemessen falsch ⇒ `api.py` antwortet jetzt JSON |
| P10.5-30 | UI-2: Logo an beiden Stellen + Favicon aus einer Datei | ✅ | 7.2 · `phase5_ui/webui/static/logo.svg` (Variante B aus `docs/concepts/phase10_logo_entwuerfe_final.svg`, **pixelgleich** zum Board gemessen: 190 px 0,13/255 · 32 px 0,39/255 · 16 px **0,00**/255) · Rail (`app.html`) **und** Anmeldeseite (`pages.py`) binden dieselbe Datei ein, dazu das Favicon · Farben = App-Tokens **mit Ersatzwert** (`var(--accent, #3E8DF3)`), weil `<img>` und Favicon keine Seiten-Variablen erben · 3 neue Tests in `phase5_ui/tests/test_pages_markup.py` + 1 in `test_static_routes.py` (**4 Gegenläufe wirksam**) · Probe `probes/p105_b7_logo_probe.py` an der Wegwerf-Instanz: `naturalWidth` 100, gerendert **16 × 16**, **Gegenlauf rot** (`naturalWidth` 0) |
| P10.5-31 | UI-3: deutscher Titel je Ansicht (V120 ✅) | ✅ | 7.3 · `state.js :: setViewTitle(part)` + `setPanelTitle(open)` (der Titel folgt der **Ansicht**; das Panel liegt als Overlay darüber) · Aufrufe: `editor.js :: showOverviewPane` (Listen-Titel), `editor.js :: loadEditorFromItem` (Item-Titel), `tree.js :: navigateAll`/`activateView`, `app.js` (Zurück-Knopf), `settings.js :: show` (Panel) · Format **„Titel · sharefyx"** (Plan §Block 7, Schritt 7.3) · Probe `probes/p105_b7_titel_probe.py` an der Wegwerf-Instanz: **6/6 Schritte** ✓ (Übersicht · Space-Name · Item-Titel · Einstellungen · zurück), **Gegenlauf rot** ✓ (ohne `setViewTitle(item.title)` bleibt der Space-Name stehen) · 4 Wächter in `phase10_5_finishing/tests/test_view_titles.py` |
| P10.5-32 | UI-4: Sichtungsliste abgearbeitet (Nikinger bestätigt) | ⬜ | 7.4 · 8 Screenshots gemacht, **4 Posten** vom Nikinger (Wortmarken-Abstand, „Zugewiesen"-Auswahl, Update-Banner, Versionsanzeige) — Liste in `STARTUPTRAG_ARCHIVE.md` Schritt 7.4 · **2026-10-24: der Ausführer hat alle vier umgesetzt** (Wächter `tests/test_sichtung_7_4.py` 8/8, Probe `probes/p105_b7_sichtung_probe.py` 5/5 mit 5 roten Gegenläufen an der Wegwerf-Instanz 18793) — **die Zeile wird erst ✅, wenn der Nikinger die Umsetzung bestätigt**; die **Nachsichtung** (≤ 6 weitere Posten) kommt nach Block 11 |
| P10.5-33 | UI-5: Kontrast ≥ 4,5:1 | ✅ | 7.5 · `--caution` `#F06A6E`: 5,70:1 Ruhe, 4,81:1 Hover · `tests/test_contrast.py` (Gegenlauf mit altem Wert rot) |
| P10.5-34 | UI-6: Filter in API und UI | ✅ | 7.6 · `test_items_filter_by_assignee`, `test_items_assignee_filter_respects_acl` · Probe `p105_b7_filter_probe.py`: Auswahl sichtbar, Filter verengt, „alle" stellt her; Gegenlauf rot |
| P10.5-35 | KA-5 sichtbar auf Übersicht und Karte | ✅ | 7.7 · Chip trägt `rgb(62,141,243)` (= `--accent`), die anderen nicht · Karte: Canvas-Probe zählt 44 Ringpixel in der Akzentfarbe, Gegenlauf (Ring abgeschaltet) 0 · Augen-Urteil bleibt der Sichtung (7.4) |
| P10.5-36 | 200 Knoten: Ruhe ≤ 3 s, Frame p95 ≤ 16,7 ms | ✅ | 8.8 · `p8_22_smoke.py` **5/5**: Ruhe **2712,1 ms** (Budget 3000, M6-Baseline 2694,6) · Frame p95 **1,7 ms** (Grenze 16,7) · 200 Knoten, 1006 Kanten · reduced motion **0** Frames bei gemaltem Canvas |
| P10.5-37 | C2-Stil: Lappen, Furchen, Zellen, Aktivierung (Nikinger-Sichtung) | ⬜ | 8.1–8.4 gebaut und **gemessen**: Lappenfläche **137 492 px** (Deckung 5 % wie die Vorlage), Kontur 55 %, Zellen mit Membranring und 2–4 Fortsätzen, drei Aktivierungsstufen · Screenshots `docs/screenshots/p105_b8_0{1..4}_*.png` — **die Zeile wird erst ✅, wenn der Nikinger das Bild beurteilt hat** |
| P10.5-38 | KA-2: Layout überlebt das Neuladen | ✅ | 8.5/8.8 · Browser-Probe: der gezogene Knoten steht **nach dem Neuladen** noch dort (**106 Kernpixel** am Ziel) · **Gegenlauf**: 0 → rot · Node-Harness: Abweichung **≤ 0,71 px** (die Ablage rundet auf ganze Pixel) |
| P10.5-39 | KA-3: Suche/Filter/Titel | ✅ | 8.6/8.8 · Browser-Probe: „**10 Treffer**", Nicht-Treffer gedimmt (7280 px), Typfilter blendet Knoten **und** Bahnen aus (26165 → 4364 px) · **Gegenlauf**: wirkungslos → rot · Node-Harness: Zellen 6 → 3, Kanten 5 → 1 |
| P10.5-40 | reduced motion: statisch, 0 Ticks | ✅ | 8.7/8.8 · Browser-Probe: **0** rAF-Aufrufe aus `graph.js`, **13989** Kernpixel gemalt · Node-Harness: `raf_calls = 0` · **der M6-Nebenbefund („1 Tick statt 0") ist erledigt** |
| P10.5-41 | RE-7: `created_by` auf neuen Items über Web und MCP sichtbar | ✅ | 9.1 · **Wegwerf `probes/p105_b9_created_by_probe.py` 12/12 Zellen**: Web-Anlage → Antwort **und** Datei nennen `created_by: alpha` · MCP-Anlage → `get_item_meta` **und** Datei nennen ihn · **Altbestand**: `get_item_meta` liefert `""`, die Datei trägt **keine** Zeile — auch **nach** einem Write nicht (nichts erfunden, P10.5-W) · Fälschung: PATCH → **422**, POST → der Wert bleibt der eingeloggte Mensch · 8 neue Tests (`test_store.py` × 5, `test_tools.py` × 3, `test_api.py` × 2) · **4 Regel-Wächter mit je einem Gegenlauf** (`tests/test_created_by_rules.py`: `_KNOWN_FIELDS` / `_SYSTEM_MANAGED_FIELDS` / `_summary()` / die Leerwert-Bedingung — jeder Gegenlauf macht **genau** seinen Defekt sichtbar) |
| P10.5-42 | RE-4 atomar (V193 ✅): ein Commit, Versionen unverändert, Freigabe wandert mit | ⬜ | — |
| P10.5-43 | RE-3 nur Team-Space (V194 ✅): Frontmatter = Verzeichnis, ein Commit, Absturz wird wiederaufgenommen | ⬜ | — |
| P10.5-44 | P1-Diff nennt nur die angekündigten Dateien | ⬜ | — |
| P10.5-45 | LG-1: Volltext in der UI | ⬜ | — |
| P10.5-46 | Realtime: Änderung ≤ 2 s sichtbar | ⬜ | — |
| P10.5-47 | P10.5-S: geänderter Editor nie überschrieben; Neuladen trägt frische `version` | ⬜ | — |
| P10.5-48 | Shutdown ≤ 10 s mit offenen Streams | ⬜ | — |
| P10.5-49 | Live nach Deploy D: Ereignisse kommen über **beide** Eingänge an (V212 ✅) | ⬜ | — |
| P10.5-50 | Budget: Erstaufruf ≤ 250 KB, Editor ≤ 80 KB, jede Datei gezählt | ⬜ | — |
| P10.5-51 | ED-1: kein Moduswechsel, Live-Darstellung (Nikinger-Sichtung) | ⬜ | — |
| P10.5-52 | Roundtrip 10/10 byte-identisch, Öffnen macht nie „geändert" | ⬜ | — |
| P10.5-53 | ED-2: Klick bei sauberem Editor schreibt mit `version`; bei geändertem nur Puffer | ⬜ | — |
| P10.5-54 | ED-3: Vokabular gerendert, unbekannte Klasse wörtlich; `get_item` zeigt Rohtext | ⬜ | — |
| P10.5-55 | ED-5: Rohtext-Schalter zeigt jedes Zeichen | ⬜ | — |
| P10.5-56 | P1-11 dokumentiert; `git diff -- phase1_storage/storage` für ED-3 leer | ⬜ | — |
| P10.5-57 | keine 📗/🔄/🟡-Datei > 40 KB (`doc_health` 0, Oversize-`find`) | ⬜ | — |
| P10.5-58 | `ROADMAP.md` < 30 KB, Wächter grün | ⬜ | — |
| P10.5-59 | Register-Bilanz per Skript, jede P10.5-Zeile mit Beleg | ⬜ | — |
| P10.5-60 | P10-J zweimal live belegt | ⬜ | — |
| P10.5-61 | Closeout-Dokumente + Rotationen per Skript | ⬜ | — |

**Summe:** 35 ✅ · 0 ⚠️ · 26 ⬜ (von 61). **[2026-10-24, Block 9.1]** +1 ✅ (10-41, RE-7 `created_by`) ⇒ 35 ✅ · 0 ⚠️ · 26 ⬜. **[2026-10-24, Block 8]** +4 ✅ (10-36, 10-38, 10-39, 10-40) ⇒ 34 ✅ · 0 ⚠️ · 27 ⬜. **[Stand 2026-10-24, Block 7.5–7.7]** 33, 34 und 35 ✅. **[Korrektur 2026-10-22, Block 6]** Die Zeile stand vorher auf „21 ✅ · 0 ⚠️ · 40 ⬜“ — die Tabelle trug aber **20** ✅ (der Zähler war schon vor diesem Block falsch; Block 5 hat eine Zeile auf ✅ gezogen und die Summe nicht nachgezogen). Neu: **23**, weil Block 6 drei Zeilen (10-23/24/25) auf ✅ gesetzt hat. Ein Wächter prüft die Summe jetzt gegen die Tabelle (`tests/test_head_rules.py`). **[2026-10-23, Block 7.1]** +1 ✅ (10-29, UI-1) ⇒ 25 ✅ · 0 ⚠️ · 36 ⬜. **[2026-10-23, Block 7.2]** +1 ✅ (10-30, UI-2) ⇒ 26 ✅ · 0 ⚠️ · 35 ⬜. **[2026-10-23, Block 7.3]** +1 ✅ (10-31, UI-3) ⇒ 27 ✅ · 0 ⚠️ · 34 ⬜.

## Offen beim Nikinger

- ~~**V199**~~ ✅ 2026-10-22 (Block 1.1) — Live-Werte auf dem VPS: `dial_timeout` 10 s, `try_duration` 15 s, `try_interval` 1 s, Upstream `100.93.43.122:8765`. Die Vorlage trägt jetzt genau diese Werte.
- ~~**V200**~~ ✅ 2026-10-22 (Block 1.3) — Fleet-Playbook auf VM 200: `ok=11 changed=3 failed=0`, `sharefyx-tail-proxy` **active** mit `SuccessExitStatus=143`, nach dem Stopp **`Result=success`**, **0 failed units**, zweiter `--check` meldet `changed=0`. **Nicht gemessen:** der Domain-Weg während des Stopps (der Stopp dauerte Sekunden; der öffentliche Pfad war nicht beteiligt). Die alte Unit liegt als Kopie mit Suffix `~` unter `/etc/systemd/system/` — systemd liest sie nicht.
- **V203** — Funnel-Pfad von außen gewacht? (BT-10, Klärung eurofyx-fleet).
- ~~**P10.5-26 vor P10.5-27/28**~~ ✅ 2026-10-23 — **widerlegt, und zwar beide Verdachtsmomente.**
  Der `405` auf `GET /mcp` ist **nicht** die Ursache (gegen einen offenen FastMCP-Server mit *und*
  ohne SSE-Strom arbeitet opencode einwandfrei; der 405 steht auch im **erfolgreichen** Lauf gegen
  unseren Server im Log), und der behauptete serverseitige Werkzeugaufruf war **nicht belegt** —
  die Wegwerf-`serve.log` enthielt bis zum 2026-10-23 **null** `ev=tool`-Zeilen. Der Auslöser lag
  im **Messgerät**: der Stub-Prototyp lief endlos, und der `mcp debug`-Schritt stand vor dem
  Werkzeuglauf. Beleg: `probes/p105_b6_opencode_e2e.json` (`ev=tool, tool=list_spaces, ok=true`).
  **Kein Produktcode angefasst** — P2-B (`stateless_http=True`) bleibt, wie gelockt.
- ~~**Merge-Reihenfolge**~~ ✅ 2026-10-23 (Nikinger-Entscheidung) — **Deploy A zuerst, dann der
  Merge**: Deploy A lief aus `main` (`7358f22`, `fastmcp 3.4.7` im Dev-venv), **danach** ist
  `p105-block5` (Block 5 + 6 + P10.5-26) nach `main` gemergt. Der Merge durfte **nicht** vor
  dem Deploy A auf `main` landen, sonst hätte `deploy.sh main` den Block-5/6-Stand unter der
  Nummer `v3.1.5` ausgeliefert.
- **P10.5-18** (Deploy A) — Live-Messung nach dem Deploy: `/overview` Waiting ≤ 300 ms, Space-Wechsel
  während des Polls ≤ 1 s (beide Eingänge, DevTools). Dazu die drei Live-Checks aus Plan
  §Deploy A: eine Zeile Caddy (V199 bleibt Fleet-Sache) · Handyfoto-Upload (EXIF weg, richtig
  gedreht) · Spaces-Panel direkt nach dem Laden (BG-1).
- **P10.5-27/28** — Live-Abnahme P10-J: zwei Modellanbieter, ein Server, ein Werkzeug (`list_spaces`) — Block 6 und Z. **Voraussetzung ist erfüllt:** die Wegwerf-E2E (P10.5-26) zeigt, dass ein Nicht-Claude-Client (`list_spaces` gelingt) — offen ist nur noch der **Live**-Lauf mit zwei Modellanbietern.
- **Block 2, Zeile 15 (AL-1)** — Migration + Live-Check beim Nikinger.
- ~~**Deploy B (`v3.1.6`)**~~ ✅ **2026-10-23** — **live**: Release `20261023T165838.591015Z`, SHA
  `e5c834e`, `health_gate` **9/9 OK** (`.rail__version` v3.1.6). Die Release-Tests im Release
  **1380 grün** (340,7 s), Symlink-Wechsel, Dienst neu gestartet — Details im Session-Block.
  **Live danach:** **P10.5-22** (claude.ai-Connector
  `list_spaces`/`search_items`/`get_item`/`update_item`, Log-Feld `proto` zeigt die Ära, V208) ·
  **P10.5-25** (`curl -si -X POST …/mcp` → **401 mit Challenge**, kein 307) · **P10.5-27/28**
  (Live P10-J, zwei Modellanbieter). **5.7:** Fabian kurz Bescheid („kurzer Neustart; der
  Connector sollte ohne neue Anmeldung weiterlaufen").
- ~~**Befund 2.5 (P10.5-9 ⚠️)**~~ ✅ 2026-10-22 (Block-2-Nachzug, Nikinger-Entscheidung „ja") — `create_item(space=, folder=<neu>)` und `POST /api/v1/items` legen im fremden Home-Space mit `write:` **keinen** neuen Ordner mehr an; die Regel ist `permissions.manages_space()` (eigener Space oder Team-Space mit Schreibrecht), auf beiden Flächen. Ohne `folder` bleibt das Anlegen an der Space-Wurzel erlaubt (P6-U).

## Startauftrag — Block 7 (Darstellung: UI-1–UI-6, KA-5) · Ausführer
> **Gebaut** (7.1–7.7, 2026-10-23/24) · die ausführliche Fassung und die **zwei Korrekturen gegen den
> 📕-Plan** (`--caution` ist der **Text**-Farbwert, nicht die Knopffläche · `_items_get` steht in
> `api.py:932`, nicht 821) stehen in `STARTUPTRAG_ARCHIVE.md`. **P10.5-32 bleibt ⬜ bis zur Bestätigung
> des Nikingers**; nichts davon ist deployed — `v3.1.7` steht aus.

## Startauftrag — Block 9 (Rechte und Namen: RE-7, RE-4, RE-3) · Ausführer
> **Ankündigung der drei P1-Öffnungen** (Plan §Block 9; Herleitung:
> `docs/concepts/phase10_5_finishing_plan.md` §„Block 9"). **Die drei Öffnungen:**
> **(12) RE-7 `created_by`** (wie `updated_by`: serververwaltet, über keinen Kanal setzbar, kein Backfill,
> P10.5-W) · **(13) RE-4 `Store.rename_folder()`** (Ordner stehen nicht im Frontmatter: keine
> Item-Datei wird umgeschrieben, keine `version` erhöht; die `.share.yml` wandert mit) ·
> **(14) RE-3 `Store.rename_space()`** (`space` steht im Frontmatter, also die Semantik von `move()`:
> ein Commit für den ganzen Space; **nur Team-Spaces**, P10.5-M).
>
> **Betroffene Dateien in `phase1_storage/storage/`:** `models.py` und `store.py`. `index.py` bleibt
> unberührt — die Index-Zeilen kommen über das bestehende `row_from_file()`/`upsert_item()`, **kein**
> Schema-Sprung (Hard Rule 2). Das ist eine **Teilmenge** der angekündigten Liste: das
> Abbruchkriterium ist „nur die angekündigten Dateien", nicht „alle angekündigten Dateien".
> **Abbruchprüfung (P10.5-E/F):** `git diff --stat <basis>..HEAD -- . ':!<erlaubte Pfade>'` leer
> (ausser `.md`-Doku) und `git diff --stat -- phase1_storage/storage` nennt **nur** `models.py` und
> `store.py`. Erlaubte Pfade (Plan §3): `phase1_storage/storage/{models,store,index}.py`,
> `phase2_mcp/mcpserver/tools.py`, `phase5_ui/webui/**`, Tests.
>
> **Wichtig für die Reihenfolge:** `deploy.sh` klont das **lokale `main`**. Block 9 wird deshalb auf
> einem eigenen Branch (`p105-block9`) gebaut und **erst nach dem Deploy C** nach `main` gemergt —
> sonst liefert `v3.1.7` den Block-9-Stand mit aus.

## Session stopped — 2026-10-24 (Deploy C `v3.1.7` vorbereitet · Block 9.1 RE-7 `created_by` gebaut und gemessen)

**Ergebnis.** Zwei Dinge. **(1) Deploy C ist vorbereitet, nicht ausgeführt** — Badge `v3.1.7`,
ein eigener `## 2026-10-24`-Block in `docs/UPDATE_LOG.md` (9 Zeilen für Menschen), Suite **1425
grün**, `doc_health` **0**, `ui_budget` **5/5**. Commit `7d8c28e`, gepusht. **`deploy.sh` liegt
beim Nikinger** (Hard Rule 9):

    SHAREFYX_RELEASES_DIR=/opt/sharefyx/releases SHAREFYX_CURRENT_LINK=/opt/sharefyx/current \
    SHAREFYX_DATA_ROOT=/home/savefyx/savefyx-data SHAREFYX_BACKUP_DIR=/var/lib/sharefyx-backup \
    SHAREFYX_SYSTEMCTL="sudo systemctl" phase5_ui/scripts/deploy.sh main

Danach lese ich `health_gate.sh --expected-version=v3.1.7 --require-todays-update-log
--expected-sha=<sha>` und lege die **echte** Ausgabe in den Commit.

**(2) Block 9.1 (RE-7 `created_by`) ist gebaut und gemessen** — die zwölfte P1-Öffnung:
`Item.created_by` / `ItemSummary.created_by`, dieselbe Klasse wie `updated_by` (P9 Block trace):
serververwaltet, über **keinen** Kanal setzbar, **kein Backfill** (Lock P10.5-W). Betroffene
Dateien: `phase1_storage/storage/{models,store}.py` (der P1-Diff nennt **nur** diese beiden),
`phase2_mcp/mcpserver/tools.py`, `phase5_ui/webui/serializers.py`,
`phase5_ui/webui/static/{app.html,js/editor.js}` (eine **eigene** Lesezeile „Erstellt von X" —
eine leere `created_by` (Altbestand) darf die `updated_by`-Zeile nicht verschlucken).

**Gemessen.** Wegwerf-Probe `probes/p105_b9_created_by_probe.py` **12/12 Zellen** (Port 8799,
PID-Datei): Web-Anlage → Antwort **und** Datei nennen `created_by: alpha` · MCP-Anlage →
`get_item_meta` **und** Datei nennen ihn · **Altbestand**: `""`, **keine** Zeile in der Datei —
auch **nach** einem Write nicht (nichts erfunden) · Fälschung per PATCH → **422**, per POST → der
Wert bleibt der eingeloggte Mensch. 8 neue Tests (`test_store.py` × 5, `test_tools.py` × 3,
`test_api.py` × 2) und **4 Regel-Wächter mit je einem Gegenlauf**
(`tests/test_created_by_rules.py`: `_KNOWN_FIELDS` · `_SYSTEM_MANAGED_FIELDS` · `_summary()` ·
die Leerwert-Bedingung — jeder Gegenlauf macht **genau** seinen Defekt sichtbar).

**Ein Fund beim Bauen — die Probe selbst:** die Zelle „Altbestand nach einem Write" war
**vakuos**: der Titelwechsel benennt die Datei um (Slug!), der zwischengespeicherte Pfad zeigte
ins Leere, und „`created_by` nicht in ''" wäre grün gewesen. Der Pfad wird jetzt **neu geholt**
(`rglob` über die ID) und die Zelle prüft zusätzlich, dass die Datei **nicht leer** ist.

**Bewusst nicht gebaut:** `receipts.py :: write_receipt()` trägt `created_by` **nicht** —
`phase2_mcp/mcpserver/receipts.py` steht **nicht** auf der Block-9-Erlaubnisliste (Plan §3), und
`test_app.py` prüft die Patch-Quittung als **exaktes** Dict (eine Zeile mehr wäre dort ein
Testbruch). Beim Anlegen ist nichts verloren: die Quittung trägt `updated_by` = denselben Actor.

**Ausführer-Daten.** `opencode/MiniMax-M3.1-Flash`, Kontextgrenze **400.000** (P10.5-C erfüllt,
`~/.config/opencode/opencode.json`), keine Eingriffe des Nikingers in dieser Session, **ein**
Fehler beim Gegenlesen gefunden (die vakuose Zelle oben) und behoben.

**Stand.** Branch `p105-block9`, Baum sauber, Wegwerf-Instanz gestoppt. **P10.5-37 und P10.5-32
bleiben ⬜** (Augen-Urteil des Nikingers); das **Budget für `graph.js`** (+11,1 KB gzip statt
+8 KB) entscheidet der Nikinger.

**Nächster Schritt.** (1) Deploy C durch den Nikinger, dann `health_gate.sh` mit echter Ausgabe
in den Commit. (2) **Block 9.2** `Store.rename_folder()` (RE-4) und **9.3**
`Store.rename_space()` (RE-3), beide mit dem Absturz-Marker aus 9.4. (3) Merge `p105-block9` →
`main` **nach** dem Deploy.
