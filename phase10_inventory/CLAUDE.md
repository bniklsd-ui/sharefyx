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
updated: 2026-10-19 (Claude Code: GLM-Open-Test ausgewertet → `docs/concepts/phase10_executor_review_glm.md`; M8-Runner + 2 Modelle committet, Fixture-Glitch ROTETING korrigiert; Session-Block rotiert) | 2026-10-18 (Sessionende GLM/Open-Test: M2-M6 + V204/V205 ✅, M7/M8 offen — M8-Fixtures + Pulls stehen; Session-Block rotiert) | 2026-10-18 (M6 gefahren: KA-1-Baseline + Lappenkosten — je Frame im 60-fps-Budget) | 2026-10-18 (M3 gefahren: DCR festgehalten + 400 invalid_redirect_uri, M3b negotiate 2025-03-26) | 2026-10-18 (M5 gefahren: BG-2/BG-3 im Browser gehalten, 14/14 Checks, TLS-Wegwerf nötig) | 2026-10-18 (M4 gefahren: BG-1 reproduziert, Wegwerf 8799 mit zwei Principals steht) | 2026-10-18 (M2 gemessen: Instrument + Grundlinie 2,4 s, P10-5 ✅ — Step 2 🟡) | 2026-10-18 (Sessionende: Logo D-6 = Leuchtbahn B, Ausführer Open-Test GLM 5.3 Flash; Integration über eurofyx-fleet) | 2026-10-18 (Step 3 ✅; zweiter Session-Block, erster nach SESSIONS_ARCHIVE rotiert) | 2026-10-16 (Plan finalisiert: D-1b = C2, V199 in die Exec-Session, BT-13 beantwortet; Nachtrag im Session-Block) | 2026-10-16 (angelegt — Phase 10 begonnen; Step 0 ✅, Step 1 Register-Entwurf ✅, Karten-Entwurf C gewählt)
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
| 2 | Messungen und Proben M1–M8 (Plan §4) | 🟡 **6 von 8** — **M2 ✅** (Instrument + Grundlinie 2,4 s, P10-5 ✅) · **M3 ✅** (opencode-DCR festgehalten, 400 invalid_redirect_uri; M3b authorize-Gate + Negotiation 2025-03-26) · **M4 ✅** (BG-1 reproduziert) · **M5 ✅** (BG-2/BG-3 im Browser, 14/14 Checks) · **M6 ✅** (KA-1-Baseline + Lappen-Pipeline je Frame im Budget) · je `probes/` + Register, Details im Session-Block. **V204 ✅ / V205 ✅** (Register LG-10/AL-1). Offen: **M1** (Browser des Nikingers) → dann D-3 · **M7** · **M8** 🟡 (Runner `probes/p10_m8_vision_probe.py` gegen CT 111; `qwen3-vl:8b` 6/6, `qwen2.5vl:7b` 5/6 — Fixtures **diskriminieren nicht**, echte Frage 7 aus `p9_settings_*` fehlt) · V203 (Fleet) · V199 (Exec-Session) |
| 3 | Entscheidungen D-1–D-18 (Register §12) | ✅ 2026-10-18 — **alle D-1–D-18 beantwortet** (Register §12); an Messungen hängen nur die Zielwerte (D-3 ← M1/M2) und das Vision-Modell (D-14 ← M8) |
| 4 | Plan P10.5 | ⬜ — beginnt, wenn D-3, D-4, D-8 stehen |
| Z | Closeout P10: Register-Freigabe (Tor), Bilanz | ⬜ |

## Offen beim Nikinger

- **M1** — Ladezeiten im eigenen Browser über Domain **und** Funnel, wie in Plan §4 (M1) beschrieben (bestätigt 2026-10-16); kein HAR ins Repo. **Danach steht D-3 fest** (M2 ist gemessen) — und damit kann Step 4 (Plan P10.5) beginnen (D-4/D-8 sind seit 2026-10-18 ✅).
- **V199** — in der Exec-Session (P10.5 Block 1): `curl localhost:2019/config/` auf der VPS, unmittelbar bevor die Caddy-Vorlage nachzieht (BT-1).
- **V203** — Funnel-Pfad von außen gewächter? Das Fleet-Repo liegt auf dieser VM nicht vor (`~/dev/` trägt nur dieses Repo) — Klärung eurofyx-fleet-Seite (BT-10/D-17-Umfang).

## Session stopped — 2026-10-19 (vierter Block: GLM-Open-Test ausgewertet, unvollendete GLM-5.3-Session geschlossen — Ausführer Claude Code)

**Auftragstellung (Nikinger, Sessionbeginn):** GLM 5.3 Flash „deutlich unterdimensioniert", Kontingent gesprengt; GLM 5.3 (Default) besser, aber unter Haiku-Niveau, musste auf den Vision-Container gestoßen werden; die GLM-5.3-Session endete am 5-h-Limit. Auftrag: herausfinden, was so viel kostet, ob Claude Code + GLM besser passt, und die Qualität ansehen.

**Ergebnis.** Auswertung in **`docs/concepts/phase10_executor_review_glm.md`** (neu, aus `~/.local/share/opencode/opencode.db` read-only): **eine** Flash-Session, 278 Aufrufe, Kontext p50 **326 K**, max **567 K**, Summe **86,1 M** Tokens, **nie kompaktiert** — opencode deklariert `glm-5.3(-flash)` mit 1 M Kontext. Deckel 250 K hätte −28 %, 150 K −54 % gespart. GLM 5.3 war kein Kostenfall (32 Aufrufe, max 129 K), es erbte das von Flash geleerte Fenster. Qualität Q1–Q6 (Review §2): CT 111 trotz Plan + MCP-Konfiguration übersehen, falsche Statusaussage, kaputte Rotation (Flash); Token-Glitches in committetem Text (`ROTETING`, `tirelessly窗外`). Claude Code + GLM: Memory und 200-K-Kompaktierung kämen mit — Vergleichslauf empfohlen, **Entscheidung Nikinger (P10-K)**.

**M8 weitergeführt.** GLM-5.3-Runner `probes/p10_m8_vision_probe.py` committet (Docstring-Glitches korrigiert), Fixture-Frage `color_nuance` von „ROTETING-Punkt" auf „ROTEN Punkt" korrigiert, beide auf CT 111 vorhandenen Modelle neu gefahren → `probes/p10_m8_vision.json`: **`qwen3-vl:8b` 6/6**, **`qwen2.5vl:7b` 5/6** (fällt `overlapping`). Befund: die synthetischen Fixtures reproduzieren den Fehler vom 2026-10-05 **nicht** — M8 ist erst aussagekräftig mit der echten Frage 7 (`docs/screenshots/p9_settings_0*`, Wortlaut der damaligen Frage: `sichtpruefung_automation_conventions.md` Vision-Abschnitt). `minicpm-v:8b`, `llama3.2-vision:11b` nicht gezogen.

**Dauerhaft festgehalten:** CT-111-Adresse `192.168.68.140:11434` im Vision-Abschnitt der Sichtprüfungs-Konventionen (stand nur in einem rotierenden Block).

**Verifiziert:** `pytest` **1268** grün (Umgebung ohne `SHAREFYX_*`/`SFX_*`), `doc_health` 0, beide Rotationen per Skript (alle Gegenproben OK); kein Service-Touch, kein `pkill`, kein Produktcode; Register (39,4 KB) nicht angefasst.

**Nächster Schritt.** (1) Nikinger: P10-K — Flash raus; Vergleichslauf Claude Code + GLM 5.3 ja/nein. (2) M8 Frage 7 bauen (bekannte Antwort aus dem Bild selbst festhalten), dann die zwei fehlenden Modelle auf CT 111 sequenziell. (3) M7. (4) M1 beim Nikinger → D-3 → Step 4. Vorher Register rotieren (39,4 KB).
