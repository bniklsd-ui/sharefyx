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
  - ../docs/concepts/PHASE10_CLOSEOUT_HANDOVER.md # Abschluss → P10.5-Planung (Step 4 + Tor wandern)
  - ../docs/concepts/PHASE9_CLOSEOUT_HANDOVER.md  # Vorphase, §4 Posten, [VERIFY]-Erbe
updated: 2026-10-21 (Step 4 ✅: Plan P10.5 geschrieben und freigegeben, Tor P10-8 offen; zehnter Block, neunter rotiert) | 2026-10-20 (Closeout P10: Phase ✅, Bilanz 9 ✅ · 1 ⚠️ · 2 ⬜; Step 4 und Tor wandern in den P10.5-Planungschat; neunter Block, achter rotiert) | 2026-10-20 (Sessionende: achter Block, siebter nach SESSIONS_ARCHIVE rotiert) | 2026-10-20 (Wegwerf-Probe gefahren: Loop-Blockade bewiesen, Mitlauf-`overview` = Fokus-Handler) | 2026-10-20 (Sessionende: Übergabe geschärft) | 2026-10-20 (M1 gemessen, D-3 + D-14 beantwortet: Step 2 ✅, Step 4 beginnt; Block rotiert) | 2026-10-19 (Abend: GLM verworfen — Review §5, Fleet-Note Intake §8, Übergabe an M3/opencode; Block rotiert) | 2026-10-19 (Nachmittag 3: M7 ✅ (CM5 passt: 239 KB, Roundtrip 10/10 — `messung/M7_editor.md`) und M8 ✅ messfertig (qwen3-vl reproduziert die echte Falle, Empfehlung qwen2.5vl → D-14; llama3.2-vision unlauffähig: ollama 0.34.4 kennt mllama nicht); Step 2 damit 7 von 8, offen nur M1) | 2026-10-19 (Nachmittag 2: M8 Frage 7 gebaut und gefahren — echte Falle reproduziert am Incumbent (qwen3-vl 6/7 „Drei Panels"), qwen2.5vl 6/7; Konventions-Beispiel „linksbündig" datiert korrigiert (P9-AM: mittig); Register-Rotation unterlassen, Begründung im Session-Block; minicpm/llama3.2-Pull läuft) | 2026-10-19 (Nachmittag, Korrektur: `/context` (Nikinger) zeigt **200 K** — `CLAUDE_CODE_AUTO_COMPACT_WINDOW=1000000` wirkt in diesem Build nicht, Stopp aufgehoben, Arbeitsliste läuft; Offen-Posten entfernt) | 2026-10-19 (Nachmittag: erster Claude-Code+GLM-Lauf — Harness-Check fand `CLAUDE_CODE_AUTO_COMPACT_WINDOW=1000000` (200-K-Annahme widerlegt, Review §3.1) und keinen Remote-Control-Kanal; Arbeitsliste gestoppt, Entscheidung beim Nikinger) | 2026-10-19 (Claude Code: GLM-Open-Test ausgewertet → `docs/concepts/phase10_executor_review_glm.md`; M8-Runner + 2 Modelle committet, Fixture-Glitch ROTETING korrigiert; Session-Block rotiert) | 2026-10-18 (Sessionende GLM/Open-Test: M2-M6 + V204/V205 ✅, M7/M8 offen — M8-Fixtures + Pulls stehen; Session-Block rotiert) | 2026-10-18 (M6 gefahren: KA-1-Baseline + Lappenkosten — je Frame im 60-fps-Budget) | 2026-10-18 (M3 gefahren: DCR festgehalten + 400 invalid_redirect_uri, M3b negotiate 2025-03-26) | 2026-10-18 (M5 gefahren: BG-2/BG-3 im Browser gehalten, 14/14 Checks, TLS-Wegwerf nötig) | 2026-10-18 (M4 gefahren: BG-1 reproduziert, Wegwerf 8799 mit zwei Principals steht) | 2026-10-18 (M2 gemessen: Instrument + Grundlinie 2,4 s, P10-5 ✅ — Step 2 🟡) | 2026-10-18 (Sessionende: Logo D-6 = Leuchtbahn B, Ausführer Open-Test GLM 5.3 Flash; Integration über eurofyx-fleet) | 2026-10-18 (Step 3 ✅; zweiter Session-Block, erster nach SESSIONS_ARCHIVE rotiert) | 2026-10-16 (Plan finalisiert: D-1b = C2, V199 in die Exec-Session, BT-13 beantwortet; Nachtrag im Session-Block) | 2026-10-16 (angelegt — Phase 10 begonnen; Step 0 ✅, Step 1 Register-Entwurf ✅, Karten-Entwurf C gewählt)
---
# Phase 10 — Bestandsaufnahme

> **Auftrag:** jede offene Baustelle einsammeln, messen, entscheiden lassen und daraus den Plan für **P10.5** schreiben —
> ohne Produktcode (Lock P10-H). **Tor zu P10.5:** die Freigabe des Registers durch den Nikinger (P10-A, Abnahme P10-8).
> Zwei Phasenziele des Nikingers vom 2026-10-16: **Anbieter-Unabhängigkeit** (Server/Connector, Abnahme am Ende von P10.5)
> und der **Karten-Umbau** (Gehirnkarte). Ausführer P10.5: ~~GLM 5.3 Flash~~ verworfen 2026-10-19 — **MiniMax M3.1 Flash (Open-Test), Rückfall M3** (Plan P10.5-B).

## Modulstatus

| Step | Inhalt | Status |
|---|---|---|
| 0 | Verifikations-Durchlauf (Doku ↔ Code, Links, INDEX, Oversize) | ✅ 2026-10-16 — `doc_health` 0; drei Heads über dem Softcap benannt (DO-1); Drift ins Register (Plan §1) |
| 1 | Register-Entwurf, je Zeile ein Anker am Code | ✅ Entwurf 2026-10-16 — 76 Zeilen in elf Themen, D-1–D-18; bleibt offen für die `[VERIFY]` aus Step 2 |
| 2 | Messungen und Proben M1–M8 (Plan §4) | ✅ **8 von 8, 2026-10-20** — M2–M8 wie am 2026-10-19 (Details je `probes/`, `messung/` und Register) · **M1 ✅ 2026-10-20** (`messung/M1_browser.md`): drei Reihen (Funnel Arbeit/Firefox, Funnel mobil/Safari, Domain mobil/Safari); `/overview` **4,8–5,2 s auf allen Wegen** (kein Eingangsunterschied), `spaces`/`items` warten hinter `overview` (frei 0,2–0,3 s, gestaut bis 14,2 s), freier Item-Wert 95,8 ms; **V204 ✅ / V205 ✅**. **Abweichungen von Plan §4 M1** (S2 nur Arbeitsnetz, Domain nur mobil, Lücken) stehen in `M1_browser.md` — P10-4 mit Vorbehalt. **Probe 2026-10-20 gefahren** (Wegwerf 8799, `M1_browser.md` §Probe): `/overview` blockiert den Event-Loop (`/health` 4,3–4,8 s dahinter) · Mitlauf-`overview` = `focus`-Handler (Item öffnen 0, Fokus +1). Offen: V203 (Fleet) · V199 (Exec-Session) |
| 3 | Entscheidungen D-1–D-18 (Register §12) | ✅ 2026-10-18 — **alle D-1–D-18 beantwortet** (Register §12); D-3 ✅ 2026-10-20 (Z1–Z4: `/overview` ≤ 300 ms, kein Request hinter `/overview`, Gerüst ≤ 1 s, > 200 ms Ladeanimation) · D-14 ✅ `qwen2.5vl:7b` |
| 4 | Plan P10.5 | ✅ **2026-10-21** — `docs/concepts/phase10_5_finishing_plan.md` (P10.5-Planungschat, Opus), freigegeben samt P10-C (Lock P10.5-O) und Tor P10-8 |
| Z | Closeout P10: Register-Freigabe (Tor), Bilanz | ✅ 2026-10-20 — **9 ✅ · 1 ⚠️ · 2 ⬜** (Plan §8); P10-8/P10-10 am 2026-10-21 nachgeholt → **11 ✅ · 1 ⚠️** · Grafik `phase10_inventory_uebersicht.svg` |

## Offen beim Nikinger

- **Tor P10-8 offen seit 2026-10-21** (Register-Kopf). P10.5 läuft nach `phase10_5_finishing_plan.md`; Einstieg Block 0 (Claude Code).
- **V199** — P10.5 Block 1.1: `curl localhost:2019/config/` auf der VPS, unmittelbar bevor die Caddy-Vorlage nachzieht (BT-1).
- **V203** — Funnel-Pfad von außen gewächter? Das Fleet-Repo liegt auf dieser VM nicht vor (`~/dev/` trägt nur dieses Repo) — Klärung eurofyx-fleet-Seite (BT-10/D-17-Umfang).

## Session stopped — 2026-10-21 (zehnter Block: P10.5-Planungschat — Plan geschrieben und freigegeben, Tor P10-8 offen)

**Ergebnis:** Step 4 ✅. `docs/concepts/phase10_5_finishing_plan.md` (📕, ~89 KB): Locks P10.5-A–W, Blöcke 0–12 + Z, Deploys A–D,
Abnahme P10.5-1–61, `[VERIFY]` V207–V219. Freigegeben vom Nikinger am 2026-10-21, zusammen mit P10-C (Lock P10.5-O, Eingriff in
`phase4_auth/`), P10.5-N (beide Richtungen) und dem **Tor P10-8** (Register-Kopf). P10-Bilanz damit **11 ✅ · 1 ⚠️**. Claude Code (Opus),
kein Produktcode, kein Service-Touch.

**Antworten des Nikingers (Fragerunden 2026-10-20):** PF-1 = ein Durchgang im Adapter · drei weitere P1-Öffnungen frei (Ordner und
Team-Space umbenennen, EXIF in `put_asset`) · Editor CM5, nachgeladen · Stufe 2 = Pandoc-Attribute · LG-4 = `append_to_items` · alles in
einem Plan · Kontextgrenze **400 K**, gesetzt durch Fleet (Note Intake §9) · P10-J zweiter Anbieter **lokal über Ollama auf CT 111**.
Ausführer: MiniMax M3.1 Flash (Open-Test), Rückfall M3; die Bewertung macht Trading-Bot/eurofyx-fleet.

**Gemessen:** `doc_health` 0 (Step-0-Befund: nichts zu tun außer INDEX-Luft → Block 0) · FastMCP 4.1.2 trocken (Wegwerf-venv
`~/.claude-code-tools/p105-fmcp4-venv`): Suite 1267/1268, mit Compat aus 3 rot (Pin-Wächter + 2 Tests lesen camelCase), Smokes grün,
beide Protokoll-Ären · PF-1 im M2-Seed: 2.436 ms → 109 ms (ein Durchgang), Index 0,4 ms · live `mcp 1.30.0` kennt Protokolle nur bis
`2025-11-25` · opencode deklariert M3/M3.1 Flash mit 1 M Kontext → Stopp-Regel P10.5-C.

**Geliefert:** Plan · Register-Kopf (Tor) · Intake §9 · INDEX (Plan-Zeile; 40.772 B) · ROADMAP-Zeile P10.5 · Wurzel-Current-state und
der neunte Block hier per Skript rotiert.

**Nächste Session — P10.5 Block 0 (Claude Code, Prompt 1):** Plan §0–§2 + Block 0 lesen, `phase10_5_finishing/` anlegen, INDEX-Luft
≥ 3 KB schaffen (heute 188 B), ROADMAP-Wächter einfrieren, Ausführer-Vorbedingung prüfen. Blocker vor Block 1: Fleet setzt 400 K.
