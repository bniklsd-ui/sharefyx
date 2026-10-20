---
status: snapshot
purpose: "Abschluss-Handover P10 → P10.5 — kein Übergang an eine neue Mission, sondern an deren zweite Hälfte: Status, Delta seit dem P9-Handover, was der P10.5-Planungschat vor dem Blockschnitt wissen muss (Step 4 und das Register-Tor wandern dorthin), offene Entscheidungen, [VERIFY]-Bilanz. Phase 10 ist abgeschlossen, live bleibt v3.1.4."
read-when: zu Beginn des P10.5-Planungschats einmal ganz lesen, vor Register §12 und Plan P10 §7 — ersetzt das Nachlesen von Phase-Head und SESSIONS_ARCHIVE für alles außer der Detailhistorie
detail: L2
up: ../../ROADMAP.md
down:
  - ../../phase10_inventory/BAUSTELLENREGISTER.md   # 📗 die Arbeitsliste für P10.5 (76 Zeilen, D-1–D-18) — lebt weiter
  - ./phase10_inventory_plan.md                     # 📕 Locks P10-A–K, Messanordnung, §7 Vorschau, §8 kanonischer Closeout
  - ../../phase10_inventory/messung/M1_browser.md   # D-3 (Z1–Z4) + Probe Event-Loop/Fokus
  - ./phase10_executor_review_glm.md                # Ausführer: GLM verworfen, §5 Messlatte Marktblick
  - ./phase10_inventory_uebersicht.svg              # Übersichtsgrafik
updated: 2026-10-20 (angelegt — Closeout P10, Nikinger-Entscheidung „P10 ✅, Freigabe im Planungschat")
---
# Phase 10 — Closeout-Handover (P10 → P10.5)

> **Phase 10 ist abgeschlossen** (2026-10-20, Nikinger). Gebaut wurde nichts, und das war der Auftrag: Live läuft unverändert
> **`v3.1.4`** (`d04c0ec`), der Tabu-Diff `0a7aaf4..HEAD` ist leer, `pytest` steht bei **1268** (+3 Wächter für das Messinstrument).
> Bilanz **9 ✅ · 1 ⚠️ · 2 ⬜** von 12 (Plan §8). **Die zwei ⬜ sind der Auftrag des nächsten Chats:**
> den P10.5-Plan schreiben (P10-10) und das Register-Tor öffnen (P10-8).

## 1 Status in fünf Sätzen

1. P10 hat in **fünf Tagen und 27 Commits** jede offene Baustelle eingesammelt: **76 Registerzeilen** in elf Themen, je Zeile ein Anker am
   Code, dazu sieben Ledger-Posten, die beim Übergang P8.6 → P9 ohne Vermerk verschwunden waren.
2. Der Nikinger hat **alle D-1–D-18** beantwortet. Danach sind **39 Zeilen Ziel P10.5**. Der Umfang ist größer als die Sammelstelle vorsah:
   FastMCP 4, Realtime, Editor Stufe 1+2 (P5-U aufgehoben), `created_by`. Zwei P1-Öffnungen sind entschieden, die elfte und die zwölfte.
3. **Alle acht Messungen sind gefahren**, dazu eine Probe. Die wichtigste: `/overview` blockiert den **ganzen Event-Loop**. Das erklärt,
   warum jeder Space-Wechsel und jedes Item-Öffnen live 4–14 s hinter ihm wartet. Die Zielwerte Z1–Z4 (D-3) stehen.
4. Der zweite Ausführer-Test ist **gescheitert und verworfen**: GLM 5.3 (Flash) über opencode, dann über Claude Code. Ausführer
   für P10.5 ist **MiniMax M3 über opencode**.
5. **Step 4 (Plan P10.5) ist mit Absicht nicht geschrieben.** Er ist Opus-Arbeit (Sondervermerk des Nikingers) und wandert zusammen mit
   der Register-Freigabe in den Planungschat.

## 2 Warum dieser Handover anders ist: P10 und P10.5 sind eine Mission

- **Keine Übergabe an eine neue Mission.** Das Bild des Nikingers (intake, Kopf) gilt für beide Hälften zusammen: das Haus fertig bauen und
  dämmen, bevor P11 an eine Garage denkt. Die Regel „Phase 10 endet erst, wenn es keine offene Baustelle mehr gibt" endet also mit
  **P10.5**, nicht mit diesem Closeout.
- **Das Register lebt weiter (📗).** P10.5 plant gegen `BAUSTELLENREGISTER.md` und hakt dort ab. Es entsteht **kein zweites Register**
  (Lock P10-B). Der P10-Plan bleibt 📕; seine §7 ist die unverbindliche Vorschau auf den Blockschnitt.
- **Step 4 wandert, er wird nicht nachgeholt.** Der Planungschat übernimmt Plan §3 Step 4 wörtlich: Locks, Blöcke, Abnahme je Block mit
  Probe **und** Gegenlauf, `[VERIFY]`, Rückgabe-Auslöser für den Ausführer, INDEX-Zeile. Prompt: `docs/PROMPTS.md` Prompt 2.
- **Das Tor (P10-8) öffnet der Nikinger im Planungschat**, nach dem Blockschnitt. Das Datum gehört in den Register-Kopf, und dort ist
  kein Platz (§4.4).
- **Nummerierung setzt fort (P10-G):** Locks `P10.5-A…`, Abnahme `P10.5-1…`, nächste freie `[VERIFY]`-Nummer **V207**
  (repo-weit gegrept 2026-10-20).
- **Namen:** Plan `docs/concepts/phase10_5_<kurzname>_plan.md` (Plan §3). Verzeichnis nach Schema `phase6_5_tools_images/`,
  `phase8_5_picker_release/` → `phase10_5_<kurzname>/`. Der Kurzname ist offen (§5).

## 3 Delta seit dem P9-Handover

| Step | Ergebnis | Zeiger |
|---|---|---|
| 0 Verifikation | `doc_health` 0; drei Heads über dem Softcap benannt; Drift: Caddy-Quelle hinkt dem Live-Fix nach (BT-1, **dringend**), Ledger-Lücke, Editor-Wunsch gegen P5-U | Plan §1 |
| 1 Register | 76 Zeilen, je Zeile Herkunft, Anker, Größe, Risiko, Entscheidung, Ziel | `BAUSTELLENREGISTER.md` |
| 3 Entscheidungen | D-1–D-18; Locks **P10-I** (nie in den Home-Space eines anderen verschieben) und **P10-J** (Abnahme Anbieter-Ziel); Karte **C2 Nervenbahnen**; Logo **Leuchtbahn B** | Register §12, Plan §0.2, `phase10_karte_c_stil_2.svg`, `phase10_logo_entwuerfe_final.svg` |
| 2 Messungen | M1–M8 + Probe, Belege unter `messung/` und `probes/` | Register je Zeile |
| Ausführer | P10-E (M3) → P10-K (GLM Open-Test) → GLM verworfen → M3 | Review §5 |
| Z | Plan §8 gefüllt, Grafik, dieser Handover | Plan §8 |

**Messungen, je ein Satz** (Details stehen in der jeweiligen Registerzeile):
M1 `/overview` live 4,8–5,2 s auf jedem Weg; der Eingang ändert den Server-Boden nicht · M2 Instrument `probes/p10_overview_bench.py`,
Median 2,4 s (wird die PF-1-Abnahme) · M3 opencode registriert sich mit `application_type: null` und Loopback-Redirect und bekommt
`400 invalid_redirect_uri`; das Gate steht zweimal über **eine** Funktion · M4 BG-1 reproduziert · M5 BG-2/BG-3 im Browser gehalten,
14/14 · M6 Karte: Ruhe 2694,6 ms; die Lappen-Pipeline kostet 0,2–1,9 ms je Frame, die Größe von KA-1 kommt also aus der Gestalt, nicht aus
der Rechnung · M7 CodeMirror 5 trägt Stufe 1 (239 KB im 250-KB-Korridor, Roundtrip 10/10) · M8 `qwen2.5vl:7b` besteht die echte Falle
vom 2026-10-05, `qwen3-vl:8b` reproduziert sie (D-14).

## 4 Für den Planungschat — was der Plan wissen muss

### 4.1 Lesereihenfolge (minimal)
Dieser Handover → Register §12 und die Ziel-Spalte → Plan P10 §0/§0.2 (Locks) und §7 (Vorschau) → `messung/M1_browser.md` §D-3 und
§Probe → `messung/M7_editor.md` → Review §5. Der Phase-Head trägt nur noch den Abschlussblock.

### 4.2 Was weiter gilt
- **P10-C/P10-J:** Anbieter-Unabhängigkeit blockiert keinen Block, nur den **Abschluss von P10.5**. Abnahme: opencode führt `list_spaces`
  live über die echte Adresse aus, einmal mit M3 und einmal mit einem zweiten Modellanbieter.
- **P10-C, zweiter Teil:** Der Eingriff in `phase4_auth/` (Sicherheitscode außerhalb der Phase) wird dem Nikinger **mit dem Plan
  vorgelegt**. Erst seine Freigabe gilt.
- **P10-D:** Gehirnkarte C2. Datenquelle bleibt `GET /api/v1/graph` mit neun Feldern; ein zehntes wäre eine eigene Entscheidung.
- **P10-I:** Verschieben in fremde Home-Spaces ist verboten. P10.5 belegt per Probe, dass Web **und** MCP es durchsetzen.
- **Zwei P1-Öffnungen** (D-4 Stufe 2 Dateiformat, D-16 `created_by`): ankündigen und eng proben wie die neunte und zehnte in P9
  (Abbruchkriterium `git diff --stat -- phase1_storage/storage`).
- **Hard Rule 3 gegen Z4:** Ein Platzhalter oder zwischengespeicherter Stand trägt nie eine `version` in einen Write (M1 §D-3).

### 4.3 Befunde, die den Blockschnitt formen
- **Performance (PF-1/PF-4, D-3):** `api.py:685 _overview` ist `async def` mit synchronem `store.search()` und hält den Loop. Ein
  `asyncio.to_thread` adressiert **Z2**. **Z1** (≤ 300 ms) braucht den Zählumbau, weil `/overview` allein 4,4–4,9 s bleibt. Ob
  `to_thread` hilft, ist **unverifiziert** (GIL, CPU-gebundenes `search()`): erst bauen, dann mit M2 und einer Parallel-Probe messen. Das
  Mitlauf-`overview` kommt vom Fokus-Handler `app.js:417` (`window.addEventListener("focus", pollCounters)`), nicht vom Item-Öffnen.
- **Anbieter (PA-1/PA-2/PA-5):** Registrierung und `/oauth/authorize` prüfen beide über `clients.py:18 redirect_uri_allowed()` (`[SEAM]`).
  Eine Funktion reicht. CSP `form-action` muss den Loopback kennen (V197, Klasse des P4-Live-Funds 8c). §7 setzt die MCP-Schicht
  (FastMCP 4, Block 5) **vor** die Anbieter-Arbeit (Block 6). `initialize` braucht `/mcp/` mit Slash. opencode (Bun) ignoriert
  CA-Umgebungsvariablen im OAuth-Pfad, darum lief die Messung über einen plain-http-Proxy.
- **Betrieb:** BT-1 ist dringend (`Caddyfile.template:65`). V199 liest der Nikinger unmittelbar davor. Nichts darf eurofyx-fleet stören.
- **Editor:** CM5 hat 11 KB Luft im Korridor; der offizielle `ui_budget.py`-Lauf gegen den echten Build steht aus.
- **Wegwerf-Falle:** `/tmp/opencode/sharefyx-wegwerf-p10` trägt **500 Bulk-Items** in alpha. M4/M5 sähen dort andere Daten, also vor
  einer Wiederholung neu anlegen.

### 4.4 Größen, die beim Planen zählen
Register **40.956 B**, 4 B unter dem Softcap: Das Freigabe-Datum braucht vorher Platz (`scripts/move_sections.py`, Belege nach
`messung/`) · `docs/INDEX.md` nahe an der harten Grenze 40.960 B, Ketten nur per `prepend_updated_chain.sh` + `rotate_index_updates.sh` ·
D-17: Session-Block **≤ 4 KB** als Planregel (DO-3) · der ROADMAP-Größenwächter an P9-6 lief zu P10-Beginn rot (DO-2), ROADMAP-Änderungen
also netto klein halten.

## 5 Offene Entscheidungen

| # | Frage | Wer | Anker |
|---|---|---|---|
| 1 | **Register freigeben** (Tor P10-8) | Nikinger, im Planungschat | Plan §8 |
| 2 | **Zweiter Modellanbieter für P10-J:** Kandidat war „z.ai GLM Free Tier". GLM ist verworfen, der Z.ai-Plan gekündigt | Nikinger, nach dem Marktblick ~2026-11-10 | Plan §0.2, Review §5 |
| 3 | **Ausführer über die Zeitgrenze:** Der M3-Endpunkt ist nur bis **2026-11-15** zugesagt, der Marktblick liegt um den 2026-11-10. Der Plan muss für einen Ausführer geschrieben sein, der nicht geplant hat, und ohne Planänderung den Ausführer wechseln können (P10-K-Satz). Vor dem ersten Block in `~/.cache/opencode/models.json` `limit.context` des M3-Eintrags prüfen; ab ≥ 500 K stoppen (Review §1.1) | Planungschat + Nikinger | Review §5, SESSIONS_ARCHIVE 6. Block |
| 4 | **PF-1-Weg:** über den Index zählen (berührt den P1-Kern `storage/`, wäre eine Öffnung) oder ein Durchgang je Space mit Zählung im Adapter | Planungschat legt vor, Nikinger entscheidet | Register PF-1 |
| 5 | **Z1 machbar?** Bleibt der Bench nach PF-1 über 300 ms, entscheidet der Nikinger neu (Messbefund, kein Fehler) | Nikinger, nach Block 4 | M1 §D-3 |
| 6 | Kurzname von P10.5 (Verzeichnis + Plan) | Planungschat | §2 |
| 7 | Termine, keine Blocker: Arbeitslaptop um den **2026-11-02** testen, dann `LEGACY_UNTIL` setzen (D-15) · Fabian-Zeilen (AL-2, V150) · einmalige Bewertung P6.5-14 (AL-4) | Nikinger | Register BT-5, AL-2, AL-4 |

## 6 `[VERIFY]`-Bilanz

**V195–V206 (P10):** 6 ✅ · 1 ⚠️ · 4 ⬜ · 1 entfällt.

| V | Stand | Ort |
|---|---|---|
| V195 | ✅ opencode-DCR festgehalten (M3) | Register PA-1 |
| V196 | entfällt — D-8: kein ChatGPT | Register PA-3 |
| V197 | ⬜ → P10.5: Chromium und Loopback-Redirect gegen `form-action`, Gegenlauf im Browser | Register PA-2 |
| V198 | ⚠️ Wegwerf (fastmcp 3.4.7) handelt `2025-03-26` aus; was **live** `mcp 1.30.0` mit einem `2026-07-28`-Angebot tut, ist offen → P10.5-Abnahme | Register PA-5 |
| V199 | ⬜ → P10.5 Block 1: der Nikinger liest `curl localhost:2019/config/` auf der VPS | Register BT-1 |
| V200 | ⬜ → P10.5: `socat` Exit 143 und `SuccessExitStatus=143` | Register BT-2 |
| V201 | ✅ M7 (CM5); Rest: der offizielle `ui_budget.py`-Lauf in P10.5 | `messung/M7_editor.md` |
| V202 | ✅ BG-1 reproduziert (M4) | Register BG-1 |
| V203 | ⬜ → eurofyx-fleet: prüft jemand den **Funnel**-Pfad von außen? Das Fleet-Repo liegt nicht auf dieser VM | Register BT-10 |
| V204 · V205 · V206 | ✅ Glyphen gegenstandslos · AL-1: 7 schließbar, 3 offen mit Weg · O7 = P6-Zeile 30 | Register LG-10, AL-1, LG-9 |

**Geerbt:** V150 Termin (AL-6) · V193/V194 → P10.5 (RE-4/RE-3) · V120 → P10.5 (UI-3) · V157 und V162 B gegenstandslos (AL-7, D-9).
**Ohne Nummer, noch offen:** der zweite Modellanbieter (Plan P10-J, §5 Nr. 2) · der `ui_budget`-Rest (M7) · die Marktkandidaten
~2026-11-10 (Review §5). **Ohne Nummer, aufgelöst:** Claude Code + GLM kompaktiert bei 200 K (`/context`, Review §3.1) ·
Remote Control mit Z.ai-Endpunkt geht nicht (Review §3.1) · Z.ai-Endpunkt und Modell-Mapping bestätigt (intake §8).

## 7 Arbeitsweise — was getragen hat

- **Messen vor Bauen (P10-F) hat sich ausgezahlt:** Ohne M1 und die Probe wäre P10.5 mit einem Cache (PF-3) gestartet. Die Ursache ist aber
  ein blockierter Loop.
- **Wegwerf mit zwei Principals** (Port 8799, PID-Datei) trug M3–M5 und die Probe. Es gab keinen einzigen Service-Touch.
- **Eine Session je Step, Kontext ≤ 200 K, Gegenlesen vor jedem Commit, auch der Betreffzeile.** Das sind die Lehren aus den 86 M Tokens.
  Sie gelten für jeden Ausführer.
- **Langzeilen-Falle:** Die Doku hat Absätze als Einzelzeilen. Ausgaben deshalb mit `| cut -c1-200` begrenzen.

## 8 Was dieser Handover nicht enthält

Die Registerzeilen selbst, die Messtabellen, die Locks im Wortlaut und die Vorschau auf den Blockschnitt. Sie stehen an den Orten in
`down:` und werden dort gelesen, nicht hier kopiert. Die Phasenhistorie steht in `phase10_inventory/SESSIONS_ARCHIVE.md`.
