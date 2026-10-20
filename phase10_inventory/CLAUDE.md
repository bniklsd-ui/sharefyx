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
updated: 2026-10-20 (M1 gemessen, D-3 + D-14 beantwortet: Step 2 ✅, Step 4 beginnt; Block rotiert) | 2026-10-19 (Abend: GLM verworfen — Review §5, Fleet-Note Intake §8, Übergabe an M3/opencode; Block rotiert) | 2026-10-19 (Nachmittag 3: M7 ✅ (CM5 passt: 239 KB, Roundtrip 10/10 — `messung/M7_editor.md`) und M8 ✅ messfertig (qwen3-vl reproduziert die echte Falle, Empfehlung qwen2.5vl → D-14; llama3.2-vision unlauffähig: ollama 0.34.4 kennt mllama nicht); Step 2 damit 7 von 8, offen nur M1) | 2026-10-19 (Nachmittag 2: M8 Frage 7 gebaut und gefahren — echte Falle reproduziert am Incumbent (qwen3-vl 6/7 „Drei Panels"), qwen2.5vl 6/7; Konventions-Beispiel „linksbündig" datiert korrigiert (P9-AM: mittig); Register-Rotation unterlassen, Begründung im Session-Block; minicpm/llama3.2-Pull läuft) | 2026-10-19 (Nachmittag, Korrektur: `/context` (Nikinger) zeigt **200 K** — `CLAUDE_CODE_AUTO_COMPACT_WINDOW=1000000` wirkt in diesem Build nicht, Stopp aufgehoben, Arbeitsliste läuft; Offen-Posten entfernt) | 2026-10-19 (Nachmittag: erster Claude-Code+GLM-Lauf — Harness-Check fand `CLAUDE_CODE_AUTO_COMPACT_WINDOW=1000000` (200-K-Annahme widerlegt, Review §3.1) und keinen Remote-Control-Kanal; Arbeitsliste gestoppt, Entscheidung beim Nikinger) | 2026-10-19 (Claude Code: GLM-Open-Test ausgewertet → `docs/concepts/phase10_executor_review_glm.md`; M8-Runner + 2 Modelle committet, Fixture-Glitch ROTETING korrigiert; Session-Block rotiert) | 2026-10-18 (Sessionende GLM/Open-Test: M2-M6 + V204/V205 ✅, M7/M8 offen — M8-Fixtures + Pulls stehen; Session-Block rotiert) | 2026-10-18 (M6 gefahren: KA-1-Baseline + Lappenkosten — je Frame im 60-fps-Budget) | 2026-10-18 (M3 gefahren: DCR festgehalten + 400 invalid_redirect_uri, M3b negotiate 2025-03-26) | 2026-10-18 (M5 gefahren: BG-2/BG-3 im Browser gehalten, 14/14 Checks, TLS-Wegwerf nötig) | 2026-10-18 (M4 gefahren: BG-1 reproduziert, Wegwerf 8799 mit zwei Principals steht) | 2026-10-18 (M2 gemessen: Instrument + Grundlinie 2,4 s, P10-5 ✅ — Step 2 🟡) | 2026-10-18 (Sessionende: Logo D-6 = Leuchtbahn B, Ausführer Open-Test GLM 5.3 Flash; Integration über eurofyx-fleet) | 2026-10-18 (Step 3 ✅; zweiter Session-Block, erster nach SESSIONS_ARCHIVE rotiert) | 2026-10-16 (Plan finalisiert: D-1b = C2, V199 in die Exec-Session, BT-13 beantwortet; Nachtrag im Session-Block) | 2026-10-16 (angelegt — Phase 10 begonnen; Step 0 ✅, Step 1 Register-Entwurf ✅, Karten-Entwurf C gewählt)
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
| 2 | Messungen und Proben M1–M8 (Plan §4) | ✅ **8 von 8, 2026-10-20** — M2–M8 wie am 2026-10-19 (Details je `probes/`, `messung/` und Register) · **M1 ✅ 2026-10-20** (`messung/M1_browser.md`): drei Reihen (Funnel Arbeit/Firefox, Funnel mobil/Safari, Domain mobil/Safari); `/overview` **4,8–5,2 s auf allen Wegen** (kein Eingangsunterschied), `spaces`/`items` warten hinter `overview` (frei 0,2–0,3 s, gestaut bis 14,2 s), freier Item-Wert 95,8 ms; **V204 ✅ / V205 ✅**. **Abweichungen von Plan §4 M1** (S2 nur Arbeitsnetz, Domain nur mobil, Lücken) stehen in `M1_browser.md` — P10-4 mit Vorbehalt. Offen: V203 (Fleet) · V199 (Exec-Session) · Probe Event-Loop + Mitlauf-`overview` (nicht gefahren) |
| 3 | Entscheidungen D-1–D-18 (Register §12) | ✅ 2026-10-18 — **alle D-1–D-18 beantwortet** (Register §12); D-3 ✅ 2026-10-20 (Z1–Z4: `/overview` ≤ 300 ms, kein Request hinter `/overview`, Gerüst ≤ 1 s, > 200 ms Ladeanimation) · D-14 ✅ `qwen2.5vl:7b` |
| 4 | Plan P10.5 | ⬜ — **D-3, D-4, D-8 stehen, Beginn frei** (Claude Code schreibt ihn) |
| Z | Closeout P10: Register-Freigabe (Tor), Bilanz | ⬜ |

## Offen beim Nikinger

- **Nichts Pflichtiges** (M1 und D-14 seit 2026-10-20 erledigt). Freigabe des Registers (Tor P10-A) folgt nach Step 4.
- **V199** — in der Exec-Session (P10.5 Block 1): `curl localhost:2019/config/` auf der VPS, unmittelbar bevor die Caddy-Vorlage nachzieht (BT-1).
- **V203** — Funnel-Pfad von außen gewächter? Das Fleet-Repo liegt auf dieser VM nicht vor (`~/dev/` trägt nur dieses Repo) — Klärung eurofyx-fleet-Seite (BT-10/D-17-Umfang).

## Session stopped — 2026-10-20 (siebter Block: M1 im Browser des Nikingers gemessen, D-3 und D-14 beantwortet, Step 2 ✅)

**Ergebnis:** **Step 2 ist 8 von 8** und **Step 4 (Plan P10.5) hat freie Bahn**. Claude Code, mit dem Nikinger
live im Netzwerk-Tab (Firefox Dev Edition Arbeitsnetz, Safari MacBook mobil; Screenshots, kein HAR). Kein
Produktcode, kein Service-Touch.

**Befund (`messung/M1_browser.md`, drei Reihen):** `/api/v1/overview` kostet **4,8–5,2 s auf allen drei Wegen** (Funnel
Arbeit, Funnel mobil, Domain mobil) — der Eingang ändert den Server-Boden nicht, nur `/ui/` (mobil 0,25 s warm bis
6,3 s kalt). `spaces`, `items` und Item-Anfragen **warten hinter `overview`**: frei 0,2–0,3 s, gestaut 4–14 s; ein
freier Item-Wert 95,8 ms. Der Code passt dazu (`api.py:685 _overview` ist `async def` mit synchronem `store.search()`,
kein `to_thread`) — **als Ursache noch nicht bewiesen**. Der 20-s-Poll belegt rund ein Viertel der Zeit.

**Entschieden (Nikinger):** **D-3** = Z1–Z4 (`/overview` ≤ 300 ms live · kein Request hinter `/overview` · Gerüst ≤ 1 s ·
Ladeanimation-Regel: **> 200 ms bekommt einen Ladezustand, < 200 ms geht sofort durch**) — Wortlaut und Abnahme in
`messung/M1_browser.md` §D-3. **D-14** = `qwen2.5vl:7b`.

**Korrigiert:** meine Vermutung, der zweite `overview` nach dem Laden sei der Fokus-Handler, war für die
Dauerläufe falsch (es war der Poll). **Offen bleibt** ein Mitlauf-`overview` bei jedem Item-Öffnen (4 von 4 im
Arbeitsnetz, 3 von 3 Domain) — Hypothese Fokus-Handler (Rückkehr aus dem Inspektor), ungeprüft.

**Nächste Session — Step 4 (Plan P10.5), Claude Code:**
1. Wurzel-`CLAUDE.md`, diesen Head und diesen Block, dann `messung/M1_browser.md` und Register §12 lesen.
2. **Vorab eine Probe** (Wegwerf-Instanz, eigener Port, tmp-`DATA_ROOT`, Hard Rule 9): (a) zwei parallele Anfragen
   gegen `/overview` beweisen oder widerlegen die Event-Loop-Blockade; (b) Item öffnen mit/ohne Fokuswechsel zählt die
   `overview`-Aufrufe. Ergebnis nach `probes/` und Register PF-1/PF-4.
3. **Plan P10.5 schreiben** nach Plan §7 (unverbindliche Vorschau): Blockschnitt mit D-3 (Z1–Z4) als Abnahmezeilen;
   Ladeanimation als UI-Block (Skeleton, Hard Rule 3 beachten); Anbieter-Unabhängigkeit, Karten-Umbau, Editor Stufe 1+2.
4. **Offen beim Nikinger:** V203 (Fleet), V199 (P10.5 Block 1), Freigabe des Registers (Tor P10-A); Marktblick ~2026-11-10.
