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
updated: 2026-10-22 (Block 6 ✅ — Anbieter PA-1/PA-2, `/mcp` ohne Slash, PA-6; V209/V197 gemessen, Suite 1374 grün) | 2026-10-22 (Block 5 **abgeschlossen** — `fastmcp==4.1.3` + neu erzeugte `constraints.txt`, Suite 1354 grün mit Compat an und aus, `append_to_items` (LG-4) + Log-Feld `proto`, Protokoll-Probe beider Ären, Smoke 17/17; Abnahme 10-19/20/21 ✅, 10-22 beim Nikinger nach Deploy B) | 2026-10-22 (Block 4 **abgeschlossen** — Schritt 4.6: M2-Bench **Median 107,3 ms** (Z1 ≤ 300 ms), Event-Loop-Probe `/health` hinter `/overview` **23 ms** (P10: 4757 ms), Browser-Probe Z2/Z3/Z4 (150 ms → kein Platzhalter, 400 ms → Platzhalter); Abnahme 10-14/15/16/17 ✅, 10-18 bleibt beim Nikinger nach Deploy A) | 2026-10-22 (Block 4 Schritte 4.3/4.4: der Client holt nur noch `/overview`, `focus`/`visibilitychange` bekommen 10 s Mindestpause (PF-4) · neu `static/js/loading.js` (`withLoading`, 200 ms) + `.is-loading`-Gerüst in `app.css`, statisch unter `prefers-reduced-motion` (Z3/Z4) · 7 Wächter in `phase5_ui/tests/test_loading_state.py`) | 2026-10-22 (Block 4 Schritte 4.1/4.2: `_overview()` in **einem** `store.search()`-Durchgang (P10.5-G) + `asyncio.to_thread` in `_overview`/`_items_get`/`_graph_get` (Z2); 4 neue Tests (Parität, Rückfall, folders/members, Event-Loop) + 5 Gegenläufe; Suite 1334 grün) | 2026-10-22 (Block 3 Schritte 3.3–3.4: `scripts/asset_orphans.py` (LG-7) + 7 Tests + Wegwerf-Probe `p105_b3_assets_probe.py` **14/14 Zellen** — Abnahme 10-12/10-13 ✅) | 2026-10-22 (Block 3 Schritt 3.2: `Store.put_asset()` ruft den Stripper — **eine** Stelle für Web und MCP; die Dummy-PNG-Fixtures mussten zu echten Bytes werden) | 2026-10-22 (Block 3 Schritt 3.1: `files.strip_image_metadata()` — JPEG/PNG/WebP, GIF unverändert, fail-closed; 8 neue Tests) | 2026-10-22 (Block-2-Nachzug: Item mit **neuem Ordner** im fremden Home-Space ist jetzt auf Web **und** MCP gesperrt (Nikinger-Entscheidung 2026-10-22) — P10.5-9 ⚠️ → ✅; `ui_budget.py`/`ui_smoke.py` haben das Home-Space-Prädikat, die `team`-Flags stimmen) | 2026-10-22 (Block 2.5 — Proben Web × MCP 28/28, M4 BG-1 behoben; Block 2 ✅, Abnahme 10-8/10/9 ✅, 10-9 ⚠️ (Befund: neuer Ordner per Item-Anlage im fremden Home-Space)) | 2026-10-22 (Block 2 Schritte 2.1–2.4 gebaut — eine Regel für Web und MCP (RE-1/RE-2/P10-I/P10.5-N) und BG-1; **2.5 Proben offen, Claude Code**; Suite 1299 grün) | 2026-10-22 (Block 2 Schritte 2.1–2.2: eine Regel für Web und MCP — SharePolicy mit Home-Space-Prädikat, RE-1 Ordner anlegen, RE-2 Ordner wechseln, P10-I/P10.5-N beide Richtungen; Suite 1296 grün) | 2026-10-22 (Block 2 Schritt 2.1: SharePolicy kennt Home-Spaces und Team-Spaces, Prädikat aus der Auth-DB, eine Regel für Web und MCP) | 2026-10-22 (Block 1 **abgeschlossen**: V200 vom Fleet-Lauf belegt — Unit installiert, `Result=success`, 0 failed units; Abnahme 10-5/6/7 ✅) | 2026-10-22 (Block 1 Schritte 1.1/1.2: BT-1 — Caddy-Vorlage in Blockform mit den V199-Live-Werten (10s/15s/1s) + neuer Waechter; Abnahme 10-5 auf ✅) | 2026-10-22 (Block 1 Schritt 1.4: BT-6 — `constraints.txt` aus dem Live-Freeze, `scripts/dev_install.sh` mit `-c`, zwei Wächter, Dev-venv neu; Suite 1282 gruen auf den Live-Versionen) | 2026-10-22 (Block 1 Schritt 1.3: BT-2 — `SuccessExitStatus=143` in der Relay-Unit, Wächter 13/13, vier Gegenläufe; Block-0-Block rotiert) | 2026-10-22 (Block 0 **abgeschlossen**: 0.6 ROADMAP-Zeile P10.5 auf 🔄, 0.7 Ausführer-Vorbedingung protokolliert — Abnahme P10.5-1–4 ✅) | 2026-10-22 (Block 0: 0.2/0.3 — Phase-Head angelegt (Modulstatus, Deploy-Tabelle, Abnahmestand 61 Zeilen), DO-3-Wächter, `pytest.ini` ergänzt; davor 0.4 (ROADMAP-Wächter eingefroren), 0.5 (INDEX-Luft) und 0.8 (Register-Luft) gebaut — DO-2 vollständig; erster Block)
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

## Modulstatus

| Block | Inhalt (Register) | Wer | Deploy | Status |
|---|---|---|---|---|
| 0 | Haushalt: Verifikation, Phase-Head, INDEX-Luft, Register-Luft, DO-2, DO-3, Ausführer-Vorbedingung | Claude Code | — | ✅ 2026-10-22 — 0.1–0.8 gebaut, Abnahme P10.5-1–4 ✅ |
| 1 | Betrieb: BT-1, BT-2, BT-6 (+ `constraints.txt`) | Ausführer + Nikinger | A | ✅ 2026-10-22 — **1.1–1.4 gebaut und abgenommen** (V199 gelesen · BT-1 Caddy-Blockform · BT-2 `SuccessExitStatus=143`, live V200 ✅ · BT-6 `constraints.txt`); Abnahme 10-5/6/7 ✅, Suite 1283 grün |
| 2 | Fehler, Parität, Regel: BG-1, RE-1, RE-2, P10-I, AL-1 | Ausführer (+ Claude Code Proben) | A | ✅ 2026-10-22 — **2.1–2.5 gebaut und geprobt** (Probe 2.5: 28/28 Zellen Web × MCP, M4 0 → 3 Zeilen ohne neues Öffnen) · **Nachzug 2026-10-22 (Nikinger):** ein Item mit **neuem Ordner** im fremden Home-Space ist jetzt auf beiden Flächen gesperrt (RE-1-Parität) — P10.5-9 damit ✅ statt ⚠️ — eine Regel für Web und MCP: RE-1 Ordner anlegen, RE-2 Ordner wechseln, P10-I/P10.5-N kein Verschieben in **oder aus** einem fremden Home-Space; BG-1: die Space-Liste füllt sich nach, wenn `/overview` spät kommt) |
| 3 | Hygiene: LG-8 (P1-15), LG-7 | Ausführer | A | ✅ 2026-10-22 — **3.1–3.4 gebaut und geprobt**: `files.strip_image_metadata()` (JPEG/PNG/WebP, GIF unverändert, fail-closed `ValidationError`) + Aufruf in `Store.put_asset()` (**eine** Stelle für Web und MCP) · `scripts/asset_orphans.py` (LG-7, `--report`/`--move`, ein Commit) · 16 neue Tests · **Wegwerf 14/14 Zellen** (`probes/p105_b3_assets_probe.py`): GPS weg auf Web **und** MCP, Orientation bleibt, sauberes Bild byte-identisch, Waise gefunden und in den Papierkorb verschoben; Abnahme 10-12/10-13 ✅ |
| 4 | Performance: PF-1, PF-4, Z1–Z4 | Ausführer (+ Claude Code Proben) | A | ✅ 2026-10-22 — **4.1–4.6 gebaut und geprobt**: `_overview()` zählt alle Eimer aus **einem** `store.search()`-Durchgang (P10.5-G, Rückfall über `_STORE_FETCH_LIMIT`), `folders`/`members` wandern in die Antwort · `asyncio.to_thread` für `_overview`/`_items_get`/`_graph_get` (Z2) · Client: nur noch `/overview`, 10 s Mindestpause für `focus`/`visibilitychange` (PF-4) · neu `static/js/loading.js` + `.is-loading`-Gerüst (Z3/Z4) · **M2-Bench Median 107,3 ms** (vorher 2405,6) · **`/health` hinter `/overview` 23 ms** (P10: 4757 ms) · Browser: 150 ms → kein Platzhalter, 400 ms → Platzhalter; Abnahme 10-14/15/16/17 ✅, 10-18 beim Nikinger nach Deploy A |
| 5 | MCP-Schicht: PA-5 (FastMCP 4), LG-4 | Ausführer | B | ✅ 2026-10-22 — **5.1–5.6 gebaut und geprobt**: `fastmcp==4.1.3` (V207 ✅), `constraints.txt` neu aus frischem venv, Suite 1354 grün mit Compat an **und** aus (Warnungen als Fehler) · `proto` im Tool-Log (V219 ✅: `Context.request_context.protocol_version`) · neues Werkzeug `append_to_items` (LG-4, ≤ 20 Einträge, je Eintrag eigene `version`, Teilerfolg, Log `err:"partial"`) · Probe beider Ären in-process: `legacy` → `2025-11-25`, `auto` → `2026-07-28` · Smoke 17/17; Abnahme 10-19/20/21 ✅, 10-22 beim Nikinger nach Deploy B |
| 6 | Anbieter: PA-1, PA-2, `/mcp`, PA-6, P10-J | Ausführer + Claude Code + Nikinger | B | ✅ 2026-10-22 — **6.0–6.5 gebaut und gemessen**: zweite Vergleichsregel `http://127.0.0.1:<port>` (Port explizit, kein `localhost`/`[::1]`, P10.5-O) + `application_type` ∈ {fehlend, null, native, web} · CSP `form-action` mit `http://127.0.0.1:*` · `/mcp` **ohne** Slash exakt bedient (`_ExactMcpMount`, kein 307) · PA-6 (Wurzel-`CLAUDE.md` eine Zeile) · **V209 ✅** (opencode 1.19.4), **V197 ✅** (Chromium folgt dem Consent-Redirect) · **DCR-Gegenlauf**: derselbe Request 400 → **201** · Suite **1376 grün** (1354 + 22) · **10-23/10-24/10-25 ✅**, **10-26 ⬜** (Werkzeugaufruf serverseitig belegt, opencode-Sitzung läuft nicht weiter — `GET /mcp` → 405, siehe Session-Block), 10-27/28 beim Nikinger nach Deploy B |
| 7 | Darstellung: UI-1–UI-6, KA-5 | Ausführer (+ Claude Code Sichtung) | C | ⬜ |
| 8 | Karte: Gehirnkarte C2 | Ausführer (+ Claude Code Smoke/Sichtung) | C | ⬜ |
| 9 | Rechte und Namen: RE-7 (P1-12), RE-4 (P1-13), RE-3 (P1-14) | Ausführer | D | ⬜ |
| 10 | Suche und Realtime: LG-1, LG-2 | Ausführer (+ Claude Code Proben) | D | ⬜ |
| 11 | Editor Stufe 1 + 2: ED-1, ED-2, ED-3 (P1-11), ED-5 | Ausführer (+ Claude Code Proben/Sichtung) | D | ⬜ |
| 12 | Doku und Altlasten: DO-1, LG-6, AL-1 (Rest), AL-3, BG-2/BG-3 | Claude Code | — | ⬜ |
| Z | Closeout P10.5 (Handover, Grafik, Rotationen) | Claude Code + Nikinger | — | ⬜ |

## Deploy-Tabelle

| # | Version | SHA | `health_gate` | Ausgabe |
|---|---|---|---|---|
| A | `v3.1.5` | — | — | nach Block 1–4 |
| B | `v3.1.6` | — | — | nach Block 5–6 |
| C | `v3.1.7` | — | — | nach Block 7–8 |
| D | `v3.1.8` | — | — | nach Block 9–11 |

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
| P10.5-26 | Wegwerf-E2E: opencode führt `list_spaces` aus | ⬜ | **offen** — der Werkzeugaufruf ist serverseitig **bewiesen** (Wegwerf-Log: `ev=tool, tool=list_spaces, ok=true, proto=2025-11-25`), opencode setzt die Sitzung danach aber **nicht fort** (kein weiterer Modellaufruf). Verdacht: opencode öffnet `GET /mcp` (SSE-Strom) und bekommt **405** (unser stateless Server kennt nur POST/DELETE, P2-B). Nicht gebaut: ein GET-Strom wäre ein Eingriff in P2-B und **gehört nicht in Block 6** → Entscheidung beim Nikinger, **vor** der Live-Abnahme 10-27/28 |
| P10.5-27 | **Live P10-J Lauf 1** (M3.1 Flash) | ⬜ | — |
| P10.5-28 | **Live P10-J Lauf 2** (lokales Modell, CT 111) — mit 27 die Abschlussbedingung der Phase | ⬜ | — |
| P10.5-29 | UI-1: HTML-404 für unbekannte `/ui`-Pfade | ⬜ | — |
| P10.5-30 | UI-2: Logo an beiden Stellen + Favicon aus einer Datei | ⬜ | — |
| P10.5-31 | UI-3: deutscher Titel je Ansicht (V120 ✅) | ⬜ | — |
| P10.5-32 | UI-4: Sichtungsliste abgearbeitet (Nikinger bestätigt) | ⬜ | — |
| P10.5-33 | UI-5: Kontrast ≥ 4,5:1 | ⬜ | — |
| P10.5-34 | UI-6: Filter in API und UI | ⬜ | — |
| P10.5-35 | KA-5 sichtbar auf Übersicht und Karte | ⬜ | — |
| P10.5-36 | 200 Knoten: Ruhe ≤ 3 s, Frame p95 ≤ 16,7 ms | ⬜ | — |
| P10.5-37 | C2-Stil: Lappen, Furchen, Zellen, Aktivierung (Nikinger-Sichtung) | ⬜ | — |
| P10.5-38 | KA-2: Layout überlebt das Neuladen | ⬜ | — |
| P10.5-39 | KA-3: Suche/Filter/Titel | ⬜ | — |
| P10.5-40 | reduced motion: statisch, 0 Ticks | ⬜ | — |
| P10.5-41 | RE-7: `created_by` auf neuen Items über Web und MCP sichtbar | ⬜ | — |
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

**Summe:** 23 ✅ · 0 ⚠️ · 38 ⬜ (von 61). **[Korrektur 2026-10-22, Block 6]** Die Zeile stand vorher auf „21 ✅ · 0 ⚠️ · 40 ⬜“ — die Tabelle trug aber **20** ✅ (der Zähler war schon vor diesem Block falsch; Block 5 hat eine Zeile auf ✅ gezogen und die Summe nicht nachgezogen). Neu: **23**, weil Block 6 drei Zeilen (10-23/24/25) auf ✅ gesetzt hat. Ein Wächter prüft die Summe jetzt gegen die Tabelle (`tests/test_head_rules.py`).

## Offen beim Nikinger

- ~~**V199**~~ ✅ 2026-10-22 (Block 1.1) — Live-Werte auf dem VPS: `dial_timeout` 10 s, `try_duration` 15 s, `try_interval` 1 s, Upstream `100.93.43.122:8765`. Die Vorlage trägt jetzt genau diese Werte.
- ~~**V200**~~ ✅ 2026-10-22 (Block 1.3) — Fleet-Playbook auf VM 200: `ok=11 changed=3 failed=0`, `sharefyx-tail-proxy` **active** mit `SuccessExitStatus=143`, nach dem Stopp **`Result=success`**, **0 failed units**, zweiter `--check` meldet `changed=0`. **Nicht gemessen:** der Domain-Weg während des Stopps (der Stopp dauerte Sekunden; der öffentliche Pfad war nicht beteiligt). Die alte Unit liegt als Kopie mit Suffix `~` unter `/etc/systemd/system/` — systemd liest sie nicht.
- **V203** — Funnel-Pfad von außen gewacht? (BT-10, Klärung eurofyx-fleet).
- **P10.5-26 vor P10.5-27/28** (Block 6, 2026-10-22) — der Werkzeugaufruf von opencode **gelingt**
  serverseitig (Wegwerf-Log: `ev=tool, tool=list_spaces, ok=true`), die opencode-Sitzung läuft danach
  aber nicht weiter. Verdacht: opencode öffnet `GET /mcp` (SSE-Strom) und bekommt **405** — unser
  stateless Server registriert nur POST/DELETE (P2-B). **Nicht gebaut** (ein GET-Strom wäre ein
  Eingriff in die gelockte P2-B-Entscheidung und gehört nicht in Block 6). Entscheidung: vor der
  Live-Abnahme mit zwei Modellanbietern klären, sonst hängt dieselbe Stelle.
- **Merge-Reihenfolge** (unverändert offen): `p105-block5` (Block 5) vor oder nach Deploy A? Vor
  Deploy A muss das Dev-venv auf `main` neu gebaut werden (`main` pinnt `fastmcp 3.4.7`, das venv
  trägt 4.1.3 → zwei Wächter rot). Block 6 liegt jetzt auf demselben Zweig wie Block 5.
- **P10.5-27/28** — Live-Abnahme P10-J: zwei Modellanbieter, ein Server, ein Werkzeug (`list_spaces`) — Block 6 und Z.
- **Block 2, Zeile 15 (AL-1)** — Migration + Live-Check beim Nikinger.
- ~~**Befund 2.5 (P10.5-9 ⚠️)**~~ ✅ 2026-10-22 (Block-2-Nachzug, Nikinger-Entscheidung „ja") — `create_item(space=, folder=<neu>)` und `POST /api/v1/items` legen im fremden Home-Space mit `write:` **keinen** neuen Ordner mehr an; die Regel ist `permissions.manages_space()` (eigener Space oder Team-Space mit Schreibrecht), auf beiden Flächen. Ohne `folder` bleibt das Anlegen an der Space-Wurzel erlaubt (P6-U).

## Session stopped — 2026-10-22 (Block 6 ✅ — Anbieter: PA-1, PA-2, `/mcp` ohne Slash, PA-6)

**Ergebnis.** Die zweite Vergleichsregel ist gebaut (`http://127.0.0.1:<port>`, Port explizit, P10.5-O),
`application_type` kennt {fehlend, null, native, web}, die CSP `form-action` trägt `http://127.0.0.1:*`,
und `/mcp` wird **ohne** Slash exakt bedient (kein 307). **V209 ✅** (opencode 1.19.4), **V197 ✅**
(Chromium folgt dem Loopback-Redirect), **PA-6 ✅** (Wurzel-`CLAUDE.md`).

**Geliefert.** `clients.py` (zweite Regel + `application_type`), `config.py` (CSP), `app.py`
(`_ExactMcpMount` + `Route("/mcp")`), `CLAUDE.md` (eine Zeile), 22 neue Tests, drei Proben
(`p105_b6_dcr_probe.py`, `p105_b6_opencode_e2e.py`, `p105_b6_consent_browser.py`).

**Gemessen.** `pytest` **1376 grün** (1354 + 22) · `doc_health` 0 · `ui_budget` 5/5 · sieben Gegenläufe
wirksam · **DCR**: derselbe opencode-Request → vorher 400 `invalid_redirect_uri`, jetzt **201** ·
**V197**: Chromium folgt dem 302 auf `http://127.0.0.1:19876/…` (keine CSP-Verletzung); Gegenlauf ohne
den CSP-Eintrag: Chromium blockiert das Formular lautlos, der Callback kommt nicht an · **`/mcp` ohne
Slash**: opencode geht direkt auf `/mcp` (vorher 307 → zweiter Versuch auf `/mcp/`).

**Vier Befunde.** (1) Der Issuer-Rewrite-Proxy aus M3 ist für diese Messung **schädlich**: er schreibt
den `resource`-Parameter auf `http://…`, der Server erwartet `https://…` → opencode bricht mit
„resource stimmt nicht mit der erwarteten Ressource überein" ab. **Der Server hat recht, der Proxy
hat gelogen** — deshalb diese Messung ohne Proxy. (2) opencode 1.19.4 fährt mit
`NODE_TLS_REJECT_UNAUTHORIZED=0` **auch im OAuth-Pfad** gegen ein selbstsigniertes Zertifikat — die
M3-Messung (1.18.33) galt für 1.18.33. (3) Die MCP-Werkzeuge des `build`-Agenten sind **nicht**
standardmäßig aktiv; das Muster ist `"<server>_*"` (`sharefyx_list_spaces`). (4) **`GET /mcp` → 405**:
opencode öffnet einen SSE-Strom, unser stateless Server kennt nur POST/DELETE (P2-B). Der
Werkzeugaufruf **selbst gelingt** (eigenes Log: `ev=tool, tool=list_spaces, ok=true`), opencode setzt
die Sitzung danach aber nicht fort.

**Offen / nächster Schritt.** **P10.5-26 bleibt ⬜** (siehe „Offen beim Nikinger"): der Werkzeugaufruf
ist serverseitig bewiesen, die opencode-Sitzung läuft nicht weiter — **vor** der Live-Abnahme
10-27/28 zu klären. `phase4_auth/scripts/abnahme_run.sh:110` trägt einen Kommentar zum alten
307-Verhalten (außerhalb der erlaubten Pfade → nicht angefasst). Deploy B (`v3.1.6`) steht aus
(Block 5 + 6 zusammen); die Merge-Reihenfolge entscheidet der Nikinger.

**Ein Dateigrößen-Befund (für Block 12).** Zwei lebende Dokumente stehen knapp unter der
40-KiB-Grenze: `phase2_mcp/CLAUDE.md` (40.631 B, **329 B** Luft) und
`phase10_inventory/BAUSTELLENREGISTER.md` (39.802 B, 1.158 B Luft — Block 0.8 hatte 3.386 B
freigeräumt, Block 5 hat 1.676 B verbraucht, Block 6 0.5 B). Die Blöcke 7–12 haken im Register
je Zeile ab: **ohne Rotation/Rotation der Langtexte läuft es über die Grenze.** Beide Dateien
tragen jetzt einen Kürzungs-Weg, aber **kein automatischer** — das ist Doku-Arbeit, kein
Code-Eingriff.

**Auslegung von P10.5-E (hier offengelegt, nicht stillschweigend):** die drei Probe-Dateien
liegen in `phase10_5_finishing/probes/` — der Blockkopf nennt den Ordner nicht, **Schritt 6.6 aber
den Dateinamen** (`p105_b6_opencode_e2e.py`). Weitere Eingriffe außerhalb der Blockpfade: keine.

**Ausführer-Daten.** opencode/MiniMax-M3.1-Flash (Open-Test, P10.5-B) · Kontextgrenze 400 K geprüft
(`~/.config/opencode/opencode.json`: `MiniMax-M3.1-Flash` → `limit.context` 400000) · keine Eingriffe
Nikinger · keine Claude-Code-Session in diesem Block · kein `systemctl`/`sudo`, kein echter
`DATA_ROOT`, kein Zugriff auf die echte `auth.sqlite3` oder den Keyring.
