---
status: live
purpose: Phase-10-Head — Bestandsaufnahme (kein Produktcode): Modulstatus der Steps 0–4/Z, offene Fragen an den Nikinger, aktueller Session-Block. Register und Plan stehen in eigenen Dateien.
read-when: Arbeiten in phase10_inventory/ — zuerst lesen, zusammen mit dem Session-Block unten
detail: L2
up: ../CLAUDE.md
down:
  - BAUSTELLENREGISTER.md                         # das Register (76 Zeilen) + Entscheidungsliste D-1–D-18 (📗)
  - ../docs/concepts/phase10_inventory_plan.md    # Plan: Locks P10-A–H, Steps, Messungen M1–M7, Abnahme P10-1–12, V195–V206
  - ../docs/concepts/phase10_intake.md            # Sammelstelle (Herkunft), Fleet-Notizen §5–§7
  - ../docs/concepts/PHASE9_CLOSEOUT_HANDOVER.md  # Vorphase, §4 Posten, [VERIFY]-Erbe
updated: 2026-10-16 (angelegt — Phase 10 begonnen; Step 0 ✅, Step 1 Register-Entwurf ✅, Karten-Entwurf C gewählt)
---
# Phase 10 — Bestandsaufnahme

> **Auftrag:** jede offene Baustelle einsammeln, messen, entscheiden lassen und daraus den Plan für **P10.5** schreiben —
> ohne Produktcode (Lock P10-H). **Tor zu P10.5:** die Freigabe des Registers durch den Nikinger (P10-A, Abnahme P10-8).
> Zwei Phasenziele des Nikingers vom 2026-10-16: **Anbieter-Unabhängigkeit** (Server/Connector, Abnahme am Ende von P10.5)
> und der **Karten-Umbau** (Gehirnkarte). Ausführer P10.5: M3 Thinking über opencode (P10-E).

## Modulstatus

| Step | Inhalt | Status |
|---|---|---|
| 0 | Verifikations-Durchlauf (Doku ↔ Code, Links, INDEX, Oversize) | ✅ 2026-10-16 — `doc_health` 0; drei Heads über dem Softcap benannt (DO-1); Drift ins Register (Plan §1) |
| 1 | Register-Entwurf, je Zeile ein Anker am Code | ✅ Entwurf 2026-10-16 — 76 Zeilen in elf Themen, D-1–D-18; bleibt offen für die `[VERIFY]` aus Step 2 |
| 2 | Messungen und Proben M1–M7 (Plan §4) | ⬜ — M1 braucht den Browser des Nikingers (beide Eingänge), M2–M7 Claude Code gegen eine Wegwerf-Instanz |
| 3 | Entscheidungen D-1–D-18 (Register §12) | 🟡 — **D-1 entschieden: C (Gehirnkarte)**; D-1b (Stil C1/C2/C3) und der Rest offen |
| 4 | Plan P10.5 | ⬜ — beginnt, wenn D-1b, D-3, D-4, D-8 stehen |
| Z | Closeout P10: Register-Freigabe (Tor), Bilanz | ⬜ |

## Offen beim Nikinger

- **D-1b** — Stil der Gehirnkarte: C1 Flächen · C2 Nervenbahnen · C3 Höhenlinien (`docs/concepts/phase10_karte_c_stil_{1,2,3}.svg`).
- **M1** — Ladezeiten im eigenen Browser über Domain **und** Funnel (Anleitung: Plan §4, M1); kein HAR ins Repo.
- **V199** — `curl localhost:2019/config/` auf der VPS, bevor die Caddy-Vorlage nachzieht (BT-1, dringend).
- **BT-13** — wurde am 2026-09-04 ein Agent im echten Datenverzeichnis gestartet (`savefyx-data/.git/opencode`)?
- Die übrigen Entscheidungen D-2–D-18 mit Empfehlung: Register §12.

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

**Nächster Schritt.** Step 2 und 3 parallel: M2–M7 baut und fährt Claude Code (Wegwerf-Instanz, Port 8799); der Nikinger misst M1,
liest V199 und beantwortet D-1b. Danach Step 4 (Plan P10.5).
