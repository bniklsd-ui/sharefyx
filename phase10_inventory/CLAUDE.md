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
updated: 2026-10-19 (Abend: GLM verworfen — Review §5, Fleet-Note Intake §8, Übergabe an M3/opencode; Block rotiert) | 2026-10-19 (Nachmittag 3: M7 ✅ (CM5 passt: 239 KB, Roundtrip 10/10 — `messung/M7_editor.md`) und M8 ✅ messfertig (qwen3-vl reproduziert die echte Falle, Empfehlung qwen2.5vl → D-14; llama3.2-vision unlauffähig: ollama 0.34.4 kennt mllama nicht); Step 2 damit 7 von 8, offen nur M1) | 2026-10-19 (Nachmittag 2: M8 Frage 7 gebaut und gefahren — echte Falle reproduziert am Incumbent (qwen3-vl 6/7 „Drei Panels"), qwen2.5vl 6/7; Konventions-Beispiel „linksbündig" datiert korrigiert (P9-AM: mittig); Register-Rotation unterlassen, Begründung im Session-Block; minicpm/llama3.2-Pull läuft) | 2026-10-19 (Nachmittag, Korrektur: `/context` (Nikinger) zeigt **200 K** — `CLAUDE_CODE_AUTO_COMPACT_WINDOW=1000000` wirkt in diesem Build nicht, Stopp aufgehoben, Arbeitsliste läuft; Offen-Posten entfernt) | 2026-10-19 (Nachmittag: erster Claude-Code+GLM-Lauf — Harness-Check fand `CLAUDE_CODE_AUTO_COMPACT_WINDOW=1000000` (200-K-Annahme widerlegt, Review §3.1) und keinen Remote-Control-Kanal; Arbeitsliste gestoppt, Entscheidung beim Nikinger) | 2026-10-19 (Claude Code: GLM-Open-Test ausgewertet → `docs/concepts/phase10_executor_review_glm.md`; M8-Runner + 2 Modelle committet, Fixture-Glitch ROTETING korrigiert; Session-Block rotiert) | 2026-10-18 (Sessionende GLM/Open-Test: M2-M6 + V204/V205 ✅, M7/M8 offen — M8-Fixtures + Pulls stehen; Session-Block rotiert) | 2026-10-18 (M6 gefahren: KA-1-Baseline + Lappenkosten — je Frame im 60-fps-Budget) | 2026-10-18 (M3 gefahren: DCR festgehalten + 400 invalid_redirect_uri, M3b negotiate 2025-03-26) | 2026-10-18 (M5 gefahren: BG-2/BG-3 im Browser gehalten, 14/14 Checks, TLS-Wegwerf nötig) | 2026-10-18 (M4 gefahren: BG-1 reproduziert, Wegwerf 8799 mit zwei Principals steht) | 2026-10-18 (M2 gemessen: Instrument + Grundlinie 2,4 s, P10-5 ✅ — Step 2 🟡) | 2026-10-18 (Sessionende: Logo D-6 = Leuchtbahn B, Ausführer Open-Test GLM 5.3 Flash; Integration über eurofyx-fleet) | 2026-10-18 (Step 3 ✅; zweiter Session-Block, erster nach SESSIONS_ARCHIVE rotiert) | 2026-10-16 (Plan finalisiert: D-1b = C2, V199 in die Exec-Session, BT-13 beantwortet; Nachtrag im Session-Block) | 2026-10-16 (angelegt — Phase 10 begonnen; Step 0 ✅, Step 1 Register-Entwurf ✅, Karten-Entwurf C gewählt)
---
# Phase 10 — Bestandsaufnahme

> **Auftrag:** jede offene Baustelle einsammeln, messen, entscheiden lassen und daraus den Plan für **P10.5** schreiben —
> ohne Produktcode (Lock P10-H). **Tor zu P10.5:** die Freigabe des Registers durch den Nikinger (P10-A, Abnahme P10-8).
> Zwei Phasenziele des Nikingers vom 2026-10-16: **Anbieter-Unabhängigkeit** (Server/Connector, Abnahme am Ende von P10.5)
> und der **Karten-Umbau** (Gehirnkarte). Ausführer P10.5: ~~GLM 5.3 Flash (P10-K)~~ **verworfen 2026-10-19** (Review §5) — **MiniMax M3 über opencode**, Marktblick ~2026-11-10.

## Modulstatus

| Step | Inhalt | Status |
|---|---|---|
| 0 | Verifikations-Durchlauf (Doku ↔ Code, Links, INDEX, Oversize) | ✅ 2026-10-16 — `doc_health` 0; drei Heads über dem Softcap benannt (DO-1); Drift ins Register (Plan §1) |
| 1 | Register-Entwurf, je Zeile ein Anker am Code | ✅ Entwurf 2026-10-16 — 76 Zeilen in elf Themen, D-1–D-18; bleibt offen für die `[VERIFY]` aus Step 2 |
| 2 | Messungen und Proben M1–M8 (Plan §4) | 🟡 **7 von 8** — **M2 ✅** (Instrument + Grundlinie 2,4 s, P10-5 ✅) · **M3 ✅** (opencode-DCR festgehalten, 400 invalid_redirect_uri; M3b authorize-Gate + Negotiation 2025-03-26) · **M4 ✅** (BG-1 reproduziert) · **M5 ✅** (BG-2/BG-3 im Browser, 14/14 Checks) · **M6 ✅** (KA-1-Baseline + Lappen-Pipeline je Frame im Budget) · **M7 ✅ 2026-10-19** (`messung/M7_editor.md`: **CM5** 65,6 KB gz, Roundtrip 10/10 verlustfrei, 239,0 KB < 250 KB Korridor; EasyMDE 282,1 KB ❌ V201; markdown-it redundant zum vorhandenen `js/markdown.js`) · **M8 ✅ 2026-10-19** (Frage 7 = die echte Falle vom 2026-10-05, `p9_settings_01`, known aus Code: ein Panel, Titel **mittig** — P9-AM-CSS, Konventions-Beispiel datiert korrigiert): `qwen3-vl:8b` **6/7, reproduziert die Falle exakt** („Drei Panels. Titel: alpha."), `qwen2.5vl:7b` **6/7** — echte Falle bestanden, **Empfehlung an D-14**; `minicpm-v:8b` 4/7; `llama3.2-vision:11b` unlauffähig (ollama 0.34.4 kennt `mllama` nicht) · je `probes/` + Register, Details im Session-Block. **V204 ✅ / V205 ✅** (Register LG-10/AL-1). Offen: **M1** (Browser des Nikingers) → dann D-3 · V203 (Fleet) · V199 (Exec-Session) |
| 3 | Entscheidungen D-1–D-18 (Register §12) | ✅ 2026-10-18 — **alle D-1–D-18 beantwortet** (Register §12); an Messungen hängen nur die Zielwerte (D-3 ← M1/M2) und das Vision-Modell (D-14 ← M8) |
| 4 | Plan P10.5 | ⬜ — beginnt, wenn D-3, D-4, D-8 stehen |
| Z | Closeout P10: Register-Freigabe (Tor), Bilanz | ⬜ |

## Offen beim Nikinger

- **M1** — Ladezeiten im eigenen Browser über Domain **und** Funnel, wie in Plan §4 (M1) beschrieben (bestätigt 2026-10-16); kein HAR ins Repo. **Danach steht D-3 fest** (M2 ist gemessen) — und damit kann Step 4 (Plan P10.5) beginnen (D-4/D-8 sind seit 2026-10-18 ✅).
- **V199** — in der Exec-Session (P10.5 Block 1): `curl localhost:2019/config/` auf der VPS, unmittelbar bevor die Caddy-Vorlage nachzieht (BT-1).
- **V203** — Funnel-Pfad von außen gewächter? Das Fleet-Repo liegt auf dieser VM nicht vor (`~/dev/` trägt nur dieses Repo) — Klärung eurofyx-fleet-Seite (BT-10/D-17-Umfang).

## Session stopped — 2026-10-19 (sechster Block: Kosten-Analyse der GLM-Session, GLM verworfen, Übergabe an M3/opencode)

**Ergebnis:** **GLM ist als Ausführer gestrichen** (Nikinger-Entscheidung, Review §5; Z.ai-Auto-Verlängerung gekündigt).
Ausführer P10.5 = **MiniMax M3 über opencode**; Neubewertung des Marktes ~**2026-11-10** (M3.1 Flash, DeepSeek-
Flash-Tokenplan u. a. — alles `[VERIFY]`), Messlatte in Review §5 vorab festgeschrieben. Note an Fleet: Intake §8
(Nachtrag „GLM verworfen"). Kein Produktcode, kein Service-Touch.

**Kosten-Analyse (Claude Code, `~/.claude/projects/…/7ad1d9ad….jsonl`):** der fünfte Block lief mit 98 Aufrufen,
Kontext p50 108 K / max 165 K, Summe 10,8 M, 99 % Cache-Treffer; ~45 K Grundlast je Aufruf; ein PNG-`Read`
lieferte 139 K Zeichen Base64. Der Nikinger meldet ~70 % des 5-h-Fensters — **lokal nicht herleitbar** (Prompt-
Abrechnung mit 2–3-fach-Multiplikator ergäbe ~15–22 % einer Lite-Rechnung); maßgeblich ist die Z.ai-Usage-Seite.

**Nächste Session — Ausführer MiniMax M3 in opencode (Übergabe):**
1. **Harness zuerst prüfen**, bevor Arbeit beginnt: in `~/.cache/opencode/models.json` das deklarierte
   `limit.context` des M3-Eintrags lesen. Steht dort ≥ 500 K, die Kompaktierung also praktisch nie greift, **stoppen und
   den Nikinger fragen** (das war der 86-M-Fehler des Open-Tests; Review §1.1). Ziel: Kontext ≤ 200 K, eine Session je Step.
2. **Lesen** (kleine Reads, immer `| cut -c1-200` oder `head -c 4000` — Langzeilen-Falle): Wurzel-`CLAUDE.md`,
   diesen Head, diesen Block, danach `BAUSTELLENREGISTER.md` §12 (D-1–D-18). Kein Ganz-Datei-Read alter Phasen-Skripte.
3. **Was zu tun ist:** Step 2 hängt allein an **M1** (Browser des Nikingers, beide Eingänge, Plan §4) → **D-3** → Step 4
   (Plan P10.5). Liefert der Nikinger die M1-Zahlen im Prompt: D-3 im Register §12 festhalten, Step 2 auf ✅, Head
   nachziehen, `doc_health`. **Ohne M1-Zahlen gibt es keine Pflichtarbeit** — dann nur D-14 (Empfehlung `qwen2.5vl:7b`,
   Messung `probes/p10_m8_vision.json`) beim Nikinger abholen und eintragen. **Step 4 (Plan P10.5) schreibt Claude
   Code**, nicht M3 (Planen = Claude Code, Ausführen = M3).
4. **Regeln:** ein Modell-Trailer je Commit; vor **jedem** Commit Glitch-Scan über Diff **und Betreffzeile**; kein
   `pkill -f`, kein Service-Touch, Tests ohne `SHAREFYX_*`/`SFX_*`-Env; Rotation nur per `scripts/rotate_session_block.sh`.
5. **Offen beim Nikinger bleibt:** M1, D-14, V203 (Fleet), V199 (P10.5 Block 1); Marktblick ~2026-11-10.
