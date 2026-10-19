---
status: archive
purpose: L3-Archiv der Session-Blöcke des Phase-10-Heads, verbatim, newest-first — jede Rotation per scripts/rotate_session_block.sh
read-when: nur beim Nachvollziehen der Phasenhistorie; der aktuelle Stand steht im Head
detail: L3
up: ./CLAUDE.md
down: []
updated: 2026-10-19 (dritter Block „GLM 5.3 Flash Step 2" verbatim rotiert — Claude-Code-Auswertungssession) | 2026-10-19 (Block 2026-10-18 zweiter Block verbatim rotiert — GLM/opencode Step-2-Session) | 2026-10-18 (angelegt für die erste Rotation)
---
# Phase 10 — Session-Archiv
## Session stopped — 2026-10-18/-19 (dritter Block: Step 2 auf 6 von 8 Messungen gebracht — Ausführer erstmals GLM 5.3 Flash via opencode, P10-K Open-Test)

**Auftragstellung (Nikinger, Sessionbeginn):** Plan §3 nannte Claude Code als Step-2-Ausführer; der Nikinger entschied in der Session: M2–M8 **hier** fahren. Kein Produktcode (P10-H); Wegwerf-Arbeit auf Port 8799 (`probes/p10_wegwerf.py`, zwei Principals nach Technik 4).

**Ergebnis.** **M2** ✅ — Instrument `probes/p10_overview_bench.py` (+3 Wächter in `phase10_inventory/tests/`, pytest 1265 → **1268**): `/overview` bei 4 Spaces × 50 Items Median **2405,6 / 2438,4 / 2414,3 ms** über drei Instrument-Läufe (±1 %, P10-5 ✅), deckungsgleich mit V151s 2,4 s. **M3** ✅ — opencode-DCR über einen Logging-Proxy festgehalten: `application_type: null` (nicht „native"), Loopback `http://127.0.0.1:19876/mcp/oauth/callback`, Auth-Methode `none` → **4× `400 {"error":"invalid_redirect_uri"}`**. M3b: ein direkt registrierter Loopback-Client scheitert auch an `/oauth/authorize` (`flows.py:98` ruft denselben `[SEAM]`) — das Gate steht zweimal, eine Funktion reicht für P10.5; `initialize` handelte **2025-03-26** aus (SSE, fastmcp 3.4.7; `/mcp/` mit Slash nötig). **M4** ✅ — BG-1 **reproduziert** (verzögertes `/overview` → 0 Zeilen, auch nach Lieferung 0, nach Zu/Auf 2; Gegenlauf 2). **M5** ✅ — BG-2 (Kopie trägt `space=gamma`) und BG-3 (Enter in allen neun erreichbaren Overlays) **gehalten**, 14/14 Checks, je Station Gegenlauf; legacy-host im Wegwerf unerreichbar (https-Pflicht des Legacy-Parsers, benannt). **M6** ✅ — Baseline: sichtbare Ruhe **2694,6 ms** (< 3 s), 153 Ticks, Frame-Abstand p50 16,7 ms, Interaktion p95 ≤ 0,3 ms; die naive Lappen-Pipeline kostet **0,2–1,9 ms** (real 66 Cluster bzw. synthetische 200-Punkt-Obergrenze) — **je Frame im 60-fps-Budget**, KA-1s Größe kommt aus Gestalt, nicht aus der Rechnung. Nebenbefund: reduced-motion zeigt **1 rAF-Tick** statt 0 (Bild statisch; vermutlich initiale Zeichnung über rAF) → P10.5 Block 8. **V204** ✅ (LG-10 gegenstandslos — letzte Griffe an allen P6/P6.5-Glyphen: P8-C2 `0d97b3a`; 0 lebende Treffer). **V205** ✅ (AL-1: 7 Zeilen mit P7–P9-Belegen schließbar, 3 offen mit Weg: 14 geteilte-Space-Hälfte, 15 Migration, 29 Connector-Move).

**Offen geblieben.** M1 (Browser des Nikingers) → danach D-3 → Step 4. **M7** ungefahren. **M8** halb vorbereitet: 6 Fixtures mit bekannter Antwort unter `probes/fixtures/` (+ `questions.json`), ollama-Daemon als Nutzerprozess, die vier Modell-Pulls laufen **abgesetzt** weiter (Log `/tmp/opencode/m8_pulls.log`; Ziel: qwen3-vl:8b, qwen2.5vl:7b, minicpm-v:8b, llama3.2-vision:11b — **CPU-only, diese VM hat kein nvidia-smi**). V203: Fleet-Repo liegt hier nicht; V199: Exec-Session. **[2026-10-19 Korrektur, GLM 5.3 — nachgetragen beim Aufräumen des Working Tree:]** die Pulls liefen beim Schreiben bereits nicht mehr (Log endet 07:08, kein Prozess) — sie starben mit der Session, und sie liefen außerdem **auf der falschen Kiste**: Vision-Inferenz gehört auf **CT 111** (`192.168.68.140:11434`, RTX 3060, einziger 11434-Listener laut P9-22-Beweis; P9-C8), nicht auf diese VM (5,8 GiB RAM, keine GPU). `qwen3-vl:8b` steht dort schon (6,1 GB, Q4_K_M, probehalber verifiziert). Die USER-seitigen Partial-Blobs (2,7 GB, redundanter Ziehversuch desselben Modells) sind gelöscht; die **systemweiten** ~8 GB (Binary + Modell, kalter Fallback aus Step C „bis Step Z" — Step Z ist seit 2026-10-08 durch) bleiben unangetastet — Entfernen ist Nikinger-Entscheidung (sudo). M8 läuft gegen CT 111; die Pulls der drei Mitbewerber gehen dorthin, sequenziell mit `rm` zwischendurch.

**Eigene Fehler dieser Session (alle vor dem Commit gefangen, außen dokumentiert):** asyncio-Proxy fraß sich an `read(n)` fest, kein Keep-Alive-/Chunked-Handling, Header-Rewrite ersetzte nur den Body; Seed nannte das falsche Konflikt-Item; Rotations-Skript per python statt bash gerufen. Zwei Betriebsbefunde der Messung selbst im Register PA-7: Bun/opencode ehrt keine CA-Env-Variable im OAuth-Pfad (Messung lief deshalb über plain-http-Proxy mit Issuer-Rewrite — Messinstrument, Serververhalten unverändert).

**Verifiziert:** `pytest` **1268** (nach M2; seither nur Probe-Skripte/Doku), `doc_health` 0, Tabu-Diff P10-11 leer, beide Wegwerf-Instanzen per PID-Datei gestoppt, kein `pkill -f`, kein `systemctl`. Ausführer-Tag: **GLM 5.3 Flash / opencode** (P10-K Open-Test) — Rückfallebene M3 bleibt bis 2026-11-15.

**Nächster Schritt.** M8-Runner schreiben und die vier Modelle gegen die Fixtures fahren, dann M7; parallel M1 beim Nikinger → D-3 → **Step 4 (Plan P10.5)**.

## Session stopped — 2026-10-18 (zweiter Block: alle Entscheidungen D-1–D-18 eingeholt und eingearbeitet; kein Produktcode)

**Ergebnis.** Der Nikinger hat in fünf Fragerunden alle offenen Entscheidungen beantwortet; sie stehen je Zeile im Register §12 und
haben die Ziel-Spalte gesetzt: **P10.5 39** · P10 9 · P11 4 · verworfen 6 · Wissen 6 · Termin 3 · erledigt 3 · an Fleet 2 · 4 ohne Bau
(per Skript gezählt). Zwei neue Locks im Plan §0.2: **P10-I** (niemand verschiebt in den Home-Space eines anderen — destruktiv wie
Löschen) und **P10-J** (Abnahme Anbieter-Ziel: opencode mit M3 **und** mit einem zweiten Modellanbieter). Neue Messung **M8**
(4 Vision-Modelle × 5 gemeine Screenshots, D-14). V206 beantwortet: O7 = P6-Zeile 30, seit P6-AF gebaut.

**Befund für P10.5.** Der Umfang ist deutlich gewachsen: FastMCP 4 / MCP 2026-07-28, Realtime, Bulk-Append-Werkzeug, Space
umbenennen, Editor Stufe 1 + 2 (P5-U aufgehoben) und `created_by` — zwei P1-Öffnungen (elfte, zwölfte). Plan §7 schneidet daraus
zwölf Blöcke; fünf davon sind „L" und brauchen je einen Mini-Plan.

**Nachtrag 2026-10-18 (Sessionende).** Logo D-6 in vier Runden entschieden: **Leuchtbahn, Variante B** (Eselsohr überlagert,
ohne den Fortsatz, der hinausragte) — `docs/concepts/phase10_logo_entwuerfe_final.svg`. Ausführer P10.5 geändert: **Open-Test
GLM 5.3 Flash** (Lock P10-K, ersetzt P10-E; M3-Rückfall bis 2026-11-15). **Die Integration von z.ai/GLM in opencode läuft über
`eurofyx-fleet`, getrennt von diesem Plan** — Sharefyx setzt nur voraus, dass opencode den Ausführer stellt.

**Nächster Schritt.** Step 2: M2–M8 in Claude Code gegen die Wegwerf-Instanz, M1 im Browser
des Nikingers. Dann Step 4 (Plan P10.5).

## Session stopped — 2026-10-16 (erster Block: Phase 10 begonnen — Register-Entwurf, Plan, Karten-Entwürfe; kein Produktcode)

**Ergebnis.** Vier Grundsatzantworten des Nikingers vorab eingeholt: Zweiteilung P10/P10.5 bestätigt (Register zuerst, P10.5-Plan
danach), Anbieter-Unabhängigkeit auf Server-/Connector-Ebene, Karten-Umbau mit Stil + Layout merken + Interaktion („gehirnartiger"),
Ausführer M3 Thinking. Geschrieben: das Register (76 Zeilen, jede mit Anker am Code), der P10-Plan, sechs Karten-SVGs (erste Runde A/B/C →
**C gewählt**, zweite Runde C1–C3). Der „verlorene" Planungsprompt ist `docs/PROMPTS.md` Prompt 2 (Commit `0a7aaf4`, mit den drei
Fleet-Notizen aus intake §5–§7).

**Funde (alle im Register).** Die Caddy-Quelle `Caddyfile.template:65` hinkt dem Live-Fix nach (BT-1, dringend). Sieben Ledger-Posten
fielen beim Übergang P8.6 → P9 ohne Schließvermerk aus der Kette (AL-1, AL-4, LG-7–LG-10, BT-10). Der Editor-Wunsch widerspricht dem
gelockten P5-U (ED-1). MCP 2026-07-28 ist die aktuelle Spec-Version (nicht mehr RC wie in P8 §0.5 notiert) und führt DCR als *deprecated*; Sharefyx lehnt native Clients mit
Loopback-Redirect ab (PA-1). Root-`CLAUDE.md` nannte im `down:` noch P8.6 als aktive Phase — korrigiert. Ein P9-Wächter koppelt die geschlossene Zeile P9-6 an die lebende ROADMAP-Größe und lief im Commit rot: eigene ROADMAP-Zeilen gekürzt statt P9-Testcode anzufassen (DO-2).

**Belege.** `doc_health` 0 Befunde; `test_index_archive` + `test_updated_chain` + `test_doc_health` grün (Commit-Ausgabe); kein
Produktcode-Diff (P10-11). Karten-SVGs mit headless Chromium gerendert und angesehen; Vorschau-Seite (privat):
`https://claude.ai/artifact/Grr7UELUVeh5BecbU239cQ`.

**Nachtrag 2026-10-16 — Plan finalisiert** (Auftrag „only finalize the plan", kein Step 2 in dieser Session). Antworten des
Nikingers: D-1b = **C2 Nervenbahnen**; M1 wie vorgeschlagen; V199 erst in der Exec-Session; BT-13 beantwortet (ja, versehentlich — die
Repo-Auswahl in opencode laggt, Klicks landen daneben); Push freigegeben.

**Nächster Schritt.** Step 2 und 3 parallel: M2–M7 baut und fährt Claude Code (Wegwerf-Instanz, Port 8799); der Nikinger misst M1
nach Plan §4. V199 wandert in die Exec-Session (P10.5 Block 1). Danach Step 4 (Plan P10.5).

