---
status: live
purpose: Phase-10-Head — Bestandsaufnahme (kein Produktcode): Modulstatus der Steps 0–4/Z, offene Fragen an den Nikinger, aktueller Session-Block. Register und Plan stehen in eigenen Dateien.
read-when: Arbeiten in phase10_inventory/ — zuerst lesen, zusammen mit dem Session-Block unten
detail: L2
up: ../CLAUDE.md
down:
  - BAUSTELLENREGISTER.md                         # das Register (76 Zeilen) + Entscheidungsliste D-1–D-18 (📗)
  - ../docs/concepts/phase10_inventory_plan.md    # Plan: Locks P10-A–K, Steps, Messungen M1–M8, Abnahme P10-1–12, V195–V206
  - ../docs/concepts/phase10_intake.md            # Sammelstelle (Herkunft), Fleet-Notizen §5–§7
  - ../docs/concepts/PHASE9_CLOSEOUT_HANDOVER.md  # Vorphase, §4 Posten, [VERIFY]-Erbe
updated: 2026-10-18 (Sessionende GLM/Open-Test: M2-M6 + V204/V205 ✅, M7/M8 offen — M8-Fixtures + Pulls stehen; Session-Block rotiert) | 2026-10-18 (M6 gefahren: KA-1-Baseline + Lappenkosten — je Frame im 60-fps-Budget) | 2026-10-18 (M3 gefahren: DCR festgehalten + 400 invalid_redirect_uri, M3b negotiate 2025-03-26) | 2026-10-18 (M5 gefahren: BG-2/BG-3 im Browser gehalten, 14/14 Checks, TLS-Wegwerf nötig) | 2026-10-18 (M4 gefahren: BG-1 reproduziert, Wegwerf 8799 mit zwei Principals steht) | 2026-10-18 (M2 gemessen: Instrument + Grundlinie 2,4 s, P10-5 ✅ — Step 2 🟡) | 2026-10-18 (Sessionende: Logo D-6 = Leuchtbahn B, Ausführer Open-Test GLM 5.3 Flash; Integration über eurofyx-fleet) | 2026-10-18 (Step 3 ✅; zweiter Session-Block, erster nach SESSIONS_ARCHIVE rotiert) | 2026-10-16 (Plan finalisiert: D-1b = C2, V199 in die Exec-Session, BT-13 beantwortet; Nachtrag im Session-Block) | 2026-10-16 (angelegt — Phase 10 begonnen; Step 0 ✅, Step 1 Register-Entwurf ✅, Karten-Entwurf C gewählt)
---
# Phase 10 — Bestandsaufnahme

> **Auftrag:** jede offene Baustelle einsammeln, messen, entscheiden lassen und daraus den Plan für **P10.5** schreiben —
> ohne Produktcode (Lock P10-H). **Tor zu P10.5:** die Freigabe des Registers durch den Nikinger (P10-A, Abnahme P10-8).
> Zwei Phasenziele des Nikingers vom 2026-10-16: **Anbieter-Unabhängigkeit** (Server/Connector, Abnahme am Ende von P10.5)
> und der **Karten-Umbau** (Gehirnkarte). Ausführer P10.5: **GLM 5.3 Flash als Open-Test** über opencode (P10-K, ersetzt P10-E; M3-Rückfall bis 2026-11-15).

## Modulstatus

| Step | Inhalt | Status |
|---|---|---|
| 0 | Verifikations-Durchlauf (Doku ↔ Code, Links, INDEX, Oversize) | ✅ 2026-10-16 — `doc_health` 0; drei Heads über dem Softcap benannt (DO-1); Drift ins Register (Plan §1) |
| 1 | Register-Entwurf, je Zeile ein Anker am Code | ✅ Entwurf 2026-10-16 — 76 Zeilen in elf Themen, D-1–D-18; bleibt offen für die `[VERIFY]` aus Step 2 |
| 2 | Messungen und Proben M1–M8 (Plan §4) | 🟡 **6 von 8** — **M2 ✅** (Instrument + Grundlinie 2,4 s, P10-5 ✅) · **M3 ✅** (opencode-DCR festgehalten, 400 invalid_redirect_uri; M3b authorize-Gate + Negotiation 2025-03-26) · **M4 ✅** (BG-1 reproduziert) · **M5 ✅** (BG-2/BG-3 im Browser, 14/14 Checks) · **M6 ✅** (KA-1-Baseline + Lappen-Pipeline je Frame im Budget) · je `probes/` + Register, Details im Session-Block. **V204 ✅ / V205 ✅** (Register LG-10/AL-1). Offen: **M1** (Browser des Nikingers) → dann D-3 · **M7** · **M8** (Fixtures + ollama-Daemon stehen, Modell-Pulls laufen abgesetzt) · V203 (Fleet) · V199 (Exec-Session) |
| 3 | Entscheidungen D-1–D-18 (Register §12) | ✅ 2026-10-18 — **alle D-1–D-18 beantwortet** (Register §12); an Messungen hängen nur die Zielwerte (D-3 ← M1/M2) und das Vision-Modell (D-14 ← M8) |
| 4 | Plan P10.5 | ⬜ — beginnt, wenn D-3, D-4, D-8 stehen |
| Z | Closeout P10: Register-Freigabe (Tor), Bilanz | ⬜ |

## Offen beim Nikinger

- **M1** — Ladezeiten im eigenen Browser über Domain **und** Funnel, wie in Plan §4 (M1) beschrieben (bestätigt 2026-10-16); kein HAR ins Repo. **Danach steht D-3 fest** (M2 ist gemessen) — und damit kann Step 4 (Plan P10.5) beginnen (D-4/D-8 sind seit 2026-10-18 ✅).
- **V199** — in der Exec-Session (P10.5 Block 1): `curl localhost:2019/config/` auf der VPS, unmittelbar bevor die Caddy-Vorlage nachzieht (BT-1).
- **V203** — Funnel-Pfad von außen gewächter? Das Fleet-Repo liegt auf dieser VM nicht vor (`~/dev/` trägt nur dieses Repo) — Klärung eurofyx-fleet-Seite (BT-10/D-17-Umfang).

## Session stopped — 2026-10-18/-19 (dritter Block: Step 2 auf 6 von 8 Messungen gebracht — Ausführer erstmals GLM 5.3 Flash via opencode, P10-K Open-Test)

**Auftragstellung (Nikinger, Sessionbeginn):** Plan §3 nannte Claude Code als Step-2-Ausführer; der Nikinger entschied in der Session: M2–M8 **hier** fahren. Kein Produktcode (P10-H); Wegwerf-Arbeit auf Port 8799 (`probes/p10_wegwerf.py`, zwei Principals nach Technik 4).

**Ergebnis.** **M2** ✅ — Instrument `probes/p10_overview_bench.py` (+3 Wächter in `phase10_inventory/tests/`, pytest 1265 → **1268**): `/overview` bei 4 Spaces × 50 Items Median **2405,6 / 2438,4 / 2414,3 ms** über drei Instrument-Läufe (±1 %, P10-5 ✅), deckungsgleich mit V151s 2,4 s. **M3** ✅ — opencode-DCR über einen Logging-Proxy festgehalten: `application_type: null` (nicht „native"), Loopback `http://127.0.0.1:19876/mcp/oauth/callback`, Auth-Methode `none` → **4× `400 {"error":"invalid_redirect_uri"}`**. M3b: ein direkt registrierter Loopback-Client scheitert auch an `/oauth/authorize` (`flows.py:98` ruft denselben `[SEAM]`) — das Gate steht zweimal, eine Funktion reicht für P10.5; `initialize` handelte **2025-03-26** aus (SSE, fastmcp 3.4.7; `/mcp/` mit Slash nötig). **M4** ✅ — BG-1 **reproduziert** (verzögertes `/overview` → 0 Zeilen, auch nach Lieferung 0, nach Zu/Auf 2; Gegenlauf 2). **M5** ✅ — BG-2 (Kopie trägt `space=gamma`) und BG-3 (Enter in allen neun erreichbaren Overlays) **gehalten**, 14/14 Checks, je Station Gegenlauf; legacy-host im Wegwerf unerreichbar (https-Pflicht des Legacy-Parsers, benannt). **M6** ✅ — Baseline: sichtbare Ruhe **2694,6 ms** (< 3 s), 153 Ticks, Frame-Abstand p50 16,7 ms, Interaktion p95 ≤ 0,3 ms; die naive Lappen-Pipeline kostet **0,2–1,9 ms** (real 66 Cluster bzw. synthetische 200-Punkt-Obergrenze) — **je Frame im 60-fps-Budget**, KA-1s Größe kommt aus Gestalt, nicht aus der Rechnung. Nebenbefund: reduced-motion zeigt **1 rAF-Tick** statt 0 (Bild statisch; vermutlich initiale Zeichnung über rAF) → P10.5 Block 8. **V204** ✅ (LG-10 gegenstandslos — letzte Griffe an allen P6/P6.5-Glyphen: P8-C2 `0d97b3a`; 0 lebende Treffer). **V205** ✅ (AL-1: 7 Zeilen mit P7–P9-Belegen schließbar, 3 offen mit Weg: 14 geteilte-Space-Hälfte, 15 Migration, 29 Connector-Move).

**Offen geblieben.** M1 (Browser des Nikingers) → danach D-3 → Step 4. **M7** ungefahren. **M8** halb vorbereitet: 6 Fixtures mit bekannter Antwort unter `probes/fixtures/` (+ `questions.json`), ollama-Daemon als Nutzerprozess, die vier Modell-Pulls laufen **abgesetzt** weiter (Log `/tmp/opencode/m8_pulls.log`; Ziel: qwen3-vl:8b, qwen2.5vl:7b, minicpm-v:8b, llama3.2-vision:11b — **CPU-only, diese VM hat kein nvidia-smi**). V203: Fleet-Repo liegt hier nicht; V199: Exec-Session. **[2026-10-19 Korrektur, GLM 5.3 — nachgetragen beim Aufräumen des Working Tree:]** die Pulls liefen beim Schreiben bereits nicht mehr (Log endet 07:08, kein Prozess) — sie starben mit der Session, und sie liefen außerdem **auf der falschen Kiste**: Vision-Inferenz gehört auf **CT 111** (`192.168.68.140:11434`, RTX 3060, einziger 11434-Listener laut P9-22-Beweis; P9-C8), nicht auf diese VM (5,8 GiB RAM, keine GPU). `qwen3-vl:8b` steht dort schon (6,1 GB, Q4_K_M, probehalber verifiziert). Die USER-seitigen Partial-Blobs (2,7 GB, redundanter Ziehversuch desselben Modells) sind gelöscht; die **systemweiten** ~8 GB (Binary + Modell, kalter Fallback aus Step C „bis Step Z" — Step Z ist seit 2026-10-08 durch) bleiben unangetastet — Entfernen ist Nikinger-Entscheidung (sudo). M8 läuft gegen CT 111; die Pulls der drei Mitbewerber gehen dorthin, sequenziell mit `rm` zwischendurch.

**Eigene Fehler dieser Session (alle vor dem Commit gefangen, außen dokumentiert):** asyncio-Proxy fraß sich an `read(n)` fest, kein Keep-Alive-/Chunked-Handling, Header-Rewrite ersetzte nur den Body; Seed nannte das falsche Konflikt-Item; Rotations-Skript per python statt bash gerufen. Zwei Betriebsbefunde der Messung selbst im Register PA-7: Bun/opencode ehrt keine CA-Env-Variable im OAuth-Pfad (Messung lief deshalb über plain-http-Proxy mit Issuer-Rewrite — Messinstrument, Serververhalten unverändert).

**Verifiziert:** `pytest` **1268** (nach M2; seither nur Probe-Skripte/Doku), `doc_health` 0, Tabu-Diff P10-11 leer, beide Wegwerf-Instanzen per PID-Datei gestoppt, kein `pkill -f`, kein `systemctl`. Ausführer-Tag: **GLM 5.3 Flash / opencode** (P10-K Open-Test) — Rückfallebene M3 bleibt bis 2026-11-15.

**Nächster Schritt.** M8-Runner schreiben und die vier Modelle gegen die Fixtures fahren, dann M7; parallel M1 beim Nikinger → D-3 → **Step 4 (Plan P10.5)**.
