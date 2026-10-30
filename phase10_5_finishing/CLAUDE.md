---
status: live
purpose: Phase-10.5-Head — Modulstatus der Blöcke 0–13/Z, Deploy-Tabelle A–D, Abnahmestand P10.5-1–64, offene Punkte beim Nikinger, aktueller Session-Block. Plan und Arbeitsliste stehen in eigenen Dateien.
read-when: Arbeiten in phase10_5_finishing/ — zuerst lesen, zusammen mit dem Session-Block unten
detail: L2
up: ../ROADMAP.md
down:
  - ../docs/concepts/phase10_5_finishing_plan.md    # 📕 der Plan: Locks P10.5-A–W, Blöcke 0–12/Z, Abnahme, [VERIFY] V207–V219
  - ../docs/concepts/phase10_5_block15_ultra_plan.md  # 📕 Block 15 „Ultra“: Hotfix v3.1.7 + die 22 Befunde (Locks P10.5-X–AG, Abnahme 75–88, V220–V232)
  - ../docs/concepts/phase10_5_launch_film_plan.md    # 📗 Block 16: der Launch-Film (Locks P10.5-AH–AM, Abnahme 89–92)
  - ../phase10_inventory/BAUSTELLENREGISTER.md      # 📗 die Arbeitsliste — hier wird abgehakt (P10-B)
  - ../phase10_inventory/ENTSCHEIDUNGEN_ARCHIVE.md  # 📦 §12 Entscheidungsliste D-1–D-18, verbatim
  - SESSIONS_ARCHIVE.md                             # 📦 ältere Session-Blöcke, verbatim, newest-first
  - UPDATES_ARCHIVE.md                              # 📦 die älteren `updated:`-Fäden dieses Heads, verbatim
  - STARTUPTRAG_ARCHIVE.md                          # 📦 die Startaufträge der Blöcke 7 und 9, verbatim
  - MODULSTATUS_ARCHIVE.md                         # 📦 die ausführlichen Statusspalten der Blöcke 0–10, verbatim
  - ABNAHME_ARCHIVE.md                             # 📦 die geschlossenen Abnahmezeilen (P10.5-1–72), verbatim
  - FREIGABEN_ARCHIVE.md                           # 📦 die Freigaben der Phase, verbatim
updated: 2026-10-30 (Planungssession „Ultra“: Plan Block 15 (Hotfix v3.1.7 + 22 Befunde) und Plan Block 16 (Launch-Film) geschrieben; Locks P10.5-X–AM; Modulzeilen 11/13/14 ins Archiv, Zeilen 15/16 neu) | 2026-10-30 (Ultra-Review gesichert: 22 Befunde, B1 kritisch auch live — nächster Block die Fixes) | 2026-10-29 (Session-Ende: Block 14 ✅; Ultra-Review-Prompt und Launch-Film-Notiz) | 2026-10-29 (Sichtung P10.5-70 ✅ — 67 ✅ · 0 ⚠️ · 7 ⬜; Block 14 fertig) | 2026-10-29 (14.7.5: P10.5-73/74 ✅ — 66 ✅ · 0 ⚠️ · 8 ⬜ von 74; Update-Log) | 2026-10-29 (14.7.3/14.7.4: Werte gesetzt, Wächter und Gegenläufe nachgezogen) | 2026-10-29 (14.7.2: Raster gemessen, Konturfehler bei krummer Zellgröße behoben — STOPP E1 + E2) | 2026-10-29 (14.7.1: die Hebel gebaut, Nullwerte = Block 14) | 2026-10-29 (14.7.0 (a)+(c): Basislinie der Form, P10.5-73/74 ⬜ — 64 ✅ · 0 ⚠️ · 10 ⬜; Plan §2.2 neu: `LOBE_SCALE`) | 2026-10-29 (14.7.0 (b): Ursache B4 = Chaos, nicht Überlauf — STOPP, Vorschlag beim Nikinger) | 2026-10-29 (Plan 14.7: kompakt + verteilt + glatt — Ausführung Claude Code, Nikinger-Entscheidung) | 2026-10-29 (14.6.4, Claude Code: Update-Log-Zeile „ein Gebilde“ statt „eigene Insel“; Vorbefund der Bilder für P10.5-70 — „geordnet“ ja, „gehirn-ähnlich“ nein) | 2026-10-28 (Block 14.6.3: die Belege neu — **P10.5-72** ✅, 64 ✅ · 0 ⚠️ · 8 ⬜) | 2026-10-28 (Block 14.6.2: der Wert steht — 160; der Wächter `koerper` beißt) | 2026-10-28 (Block 14.6.1: der Algorithmus steht, die sechs Varianten sind gemessen — der kleinste Wert mit EINER Komponente ist 160; STOPP E1) | 2026-10-28 (Block 14.6.0: die Basislinie der Karte gemessen — 5 Komponenten, 0 Furche-Zellen, 35,0 ms bei 201 Knoten) | 2026-10-28 (Plan 14.6: aus Inseln wird ein Körper — Nikinger-Entscheidung Option B, Ausführer M3.1 Flash) | 2026-10-28 (Nachzug 14.5: die Lappen-Kontur am Rasterrand war **offen** — beim Sichten der Bilder gefunden, behoben, Bilder neu; Update-Log-Zeile geschrieben) | 2026-10-28 (Block 14.5: die drei Kartenbilder — und der **gemessene** Rand-Fall aus §2.5: die Lappen-Kontur stand 3,8 px über dem Leinwandrand ⇒ `FIT_MARGIN` 40 → 56 px, jetzt 10,7 px Luft; Füllgrad 93,6 % → 91,1 %; P10.5-70 wartet auf die Sichtung) | 2026-10-27 (Block 14.4: die Startwerte gemessen — 37 Varianten, alle zehn Werte bleiben; der Gegenlauf `region` schließt die Lücke von P10.5-66; die Block-8-Probe wartet jetzt auf das richtige Ruhe-Signal) | 2026-10-27 (Block 14.35: die Beschriftungen ohne Überlappung — 0 überlappende Paare, 3 von 13 weggelassen, der Fokus bleibt; P10.5-71 ✅) | 2026-10-26 (Block 14.3: die Kamera — `fitView()`; Füllgrad 93,6 %, Versatz 0,42 px; E3: `ZOOM_MIN` bleibt 0,5; P10.5-67 ✅) | 2026-10-26 (Block 14.2: die L4 — Anker-Gravitation, Querfedern, `ALPHA_START_SEEDED`; Regionen 152/152, Stabilität Median 0,0 px, Budget 201 Knoten/2147 ms; P10.5-66/68/69 ✅) | 2026-10-26 (Block 14.1: L1–L3 — der Seed wird zum Weltgenerator; fünf Seed-Zellen grün, fünf Gegenläufe rot an genau ihrer Zelle; P10.5-65 geschlossen) | 2026-10-26 (Block 14.0: die Basislinie des Kartenlayouts — die Probe steht, die Abnahmezeilen 65–71 sind im Head; rot in Regionen/Kamera/Beschriftungen/Stabilität, grün in Determinismus/Budget; B5 widerlegt) | 2026-10-25 (Block 13: die vier Aufträge des Nikingers gebaut — Editor-Größen live, Knopfleiste nach Word, Knopffarben transparent-blau, ganze Gehirnkarte; P10.5-62/63/64 ✅, 54 ✅ · 10 ⬜) | 2026-10-25 (Block 12: Doku und Altlasten — DO-1, LG-6, AL-1/AL-3, BG-2/BG-3, Register-Bilanz per Skript; P10.5-57/58/59 ✅, 51 ✅ · 10 ⬜) | ältere Einträge: phase10_5_finishing/UPDATES_ARCHIVE.md
---
# Phase 10.5 — Finishing

> **Auftrag:** P10.5 schließt jede Baustelle, die im Register als „Ziel P10.5" steht — Betrieb, Fehler, Parität, Performance, MCP-Schicht, Anbieter-Unabhängigkeit, Darstellung, Gehirnkarte, Umbenennen, Suche, Realtime, Editor Stufe 1+2 und Doku. Die Phase endet erst, wenn ein Nicht-Claude-Client live `list_spaces` ausführt, mit zwei Modellanbietern (P10-J); neues Feature kommt erst in P11.

## Freigaben
> **Verbatim verschoben** nach `FREIGABEN_ARCHIVE.md` (`scripts/move_sections.py`) — dort unter derselben Überschrift.

## Modulstatus

| Block | Inhalt (Register) | Wer | Deploy | Status |
|---|---|---|---|---|
| 0 | Haushalt: Verifikation, Phase-Head, INDEX-Luft, Register-Luft, DO-2, DO-3, Ausführer-Vorbedingung | Claude Code | — | ✅ 2026-10-22 |
| 1 | Betrieb: BT-1, BT-2, BT-6 (+ `constraints.txt`) | Ausführer + Nikinger | A | ✅ 2026-10-22 |
| 2 | Fehler, Parität, Regel: BG-1, RE-1, RE-2, P10-I, AL-1 | Ausführer (+ Claude Code Proben) | A | ✅ 2026-10-22 |
| 3 | Hygiene: LG-8 (P1-15), LG-7 | Ausführer | A | ✅ 2026-10-22 |
| 4 | Performance: PF-1, PF-4, Z1–Z4 | Ausführer (+ Claude Code Proben) | A | ✅ 2026-10-22 |
| 5 | MCP-Schicht: PA-5 (FastMCP 4), LG-4 | Ausführer | B | ✅ 2026-10-22 |
| 6 | Anbieter: PA-1, PA-2, `/mcp`, PA-6, P10-J | Ausführer + Claude Code + Nikinger | B | ✅ 2026-10-22 |
| 7 | Darstellung: UI-1–UI-6, KA-5 | Ausführer (+ Claude Code Sichtung) | C | 🔄 2026-10-24 |
| 8 | Karte: Gehirnkarte C2 | Ausführer (+ Claude Code Smoke/Sichtung) | C | 🔄 2026-10-24 |
| 9 | Rechte und Namen: RE-7 (P1-12), RE-4 (P1-13), RE-3 (P1-14) | Ausführer | D | ✅ 2026-10-24 |
| 10 | Suche und Realtime: LG-1, LG-2 | Ausführer (+ Claude Code Proben) | D | ✅ 2026-10-24 |
| 11 | Editor Stufe 1 + 2: ED-1, ED-2, ED-3 (P1-11), ED-5 | Ausführer (+ Claude Code Proben/Sichtung) | D | ✅ 2026-10-26 — 11.1–11.8 gebaut und geprobt, Sichtung P10.5-51 ✅ 2026-10-26 (Status-Korrektur 2026-10-30: die Zeile stand noch auf 🔄, alle Schritte und Zeilen waren ✅); Details verbatim in `MODULSTATUS_ARCHIVE.md` (2026-10-30 verschoben) |
| 12 | Doku und Altlasten: DO-1, LG-6, AL-1 (Rest), AL-3, BG-2/BG-3 | Claude Code | — | ✅ 2026-10-25 — **DO-1** (die drei Heads: 8.6 109.230 → 23.614 B, 8 47.861 → 34.225 B, 6 41.032 → 34.801 B; verbatim per `move_sections.py`, die 33-KB-Kette von 8.6 per Skript in `UPDATES_ARCHIVE.md`) · **LG-6** (`ROADMAP.md` 37.197 → 26.457 B, Phase 8.5 → `docs/ROADMAP_ARCHIVE.md`) · **AL-1/AL-3** (P6-Nachzug in `phase6_shares/CLAUDE.md`) · **BG-2/BG-3** (P9-124/127 ⚠️ → ✅, Bilanz 123/10/1) · **Register-Bilanz** per `scripts/register_bilanz.py` (46 P10.5-Zeilen: 40 ✅ · 6 ⬜) |
| 13 | Aufträge des Nikingers: UI-8 (die Größen wirken live), UI-9 (die Knopfleiste nach Word), UI-10 (die Knopffarben) | Claude Code (Sichtung Nikinger) | D | ✅ 2026-10-25 — 13.1–13.4 gebaut und gemessen, P10.5-62/63/64 ✅; Details verbatim in `MODULSTATUS_ARCHIVE.md` (2026-10-30 verschoben) |
| 14 | Kartenlayout „zufällig, aber geordnet“ (Nikinger 2026-10-26) — Plan `docs/concepts/phase10_5_block14_kartenlayout_plan.md` | Ausführer (opencode) + Claude Code (Bilder) | D | ✅ 2026-10-29 — 14.0–14.7.5 gebaut und gemessen, P10.5-65–74 ✅, Sichtung P10.5-70 ✅ 2026-10-29; Pläne `docs/concepts/phase10_5_block14_{kartenlayout,6,7}_plan.md`; Details verbatim in `MODULSTATUS_ARCHIVE.md` (2026-10-30 verschoben) |
| 15 | **Ultra**: Hotfix `v3.1.7` (B1) + die 22 Befunde des Ultra-Reviews B1–B22 — Plan `docs/concepts/phase10_5_block15_ultra_plan.md` | Claude Code (Hotfix-Deploy, Freigaben, Live-Proben: Nikinger) | H + D | ⬜ geplant 2026-10-30 — nächster Schritt **H0** (Branch `hotfix/v3.1.7-b1` von `e5c834e`), danach 15.0 |
| 16 | Launch-Film „Sharefyx 4.0“ (≈ 40 s, Deutsch; beim ersten Start im Vollbild, Wiederaufruf im Update-Log) — Plan `docs/concepts/phase10_5_launch_film_plan.md` | Claude Code (Sichtungen E1/E2: Nikinger) | D | ⬜ geplant 2026-10-30 — Start nach Block 15, Budget eine Woche; 16.0 = Storyboard-Sichtung |
| Z | Closeout P10.5 (Handover, Grafik, Rotationen) | Claude Code + Nikinger | — | ⬜ |

> **Die ausführlichen Statusspalten der Blöcke 0–10 stehen verbatim in
> [`MODULSTATUS_ARCHIVE.md`](MODULSTATUS_ARCHIVE.md) (L3) — hier trägt der Modulstatus den
> **Kurzstand**. Grund: der Head stand beim Bau von Block 11.4 über dem Softcap; die
> Details der geschlossenen Blöcke bleiben im Archiv nachlesbar, der Head bleibt der
> *live* Stand.

## Deploy-Tabelle

| # | Version | SHA | `health_gate` | Ausgabe |
|---|---|---|---|---|
| A | `v3.1.5` | `7358f22` | **9/9 OK** | nach Block 1–4 — **live seit 2026-10-23**, Release `20261023T065010.377336Z` |
| B | `v3.1.6` | `e5c834e` | **9/9 OK** | nach Block 5–6 (+ **Block 7.0**, die Update-Log-ID) — **live seit 2026-10-23**, Release `20261023T165838.591015Z` · **Deploy beim Nikinger** (Hard Rule 9, `sudo`; `deploy.sh main` → Release-Tests **1380 grün** (340,7 s) → Symlink-Wechsel → Dienst neu gestartet) · `health_gate.sh --expected-version=v3.1.6 --require-todays-update-log --expected-sha=e5c834e` → **9/9 OK** (`.rail__version` v3.1.6, Release-SHA `e5c834e…`, Update-Log 2026-10-23) · **Block 7.1 (UI-1) ist gemergt** (`f0e76b0`, aus `p105-block7`) — **nicht** in diesem Release, sondern in `v3.1.7` |
| C | `v3.1.7` | — | — | nach Block 7–8 — **2026-10-24 vorbereitet** (Badge, eigener `## 2026-10-24`-Block im Update-Log, Suite 1425 grün, `doc_health` 0, `ui_budget` 5/5), **`deploy.sh` beim Nikinger** |
| D | `v4.0.0` (vorher `v3.1.8`; Nikinger 2026-10-26) | — | — | nach Block 9–11 **+ 13** + Nachzug 2026-10-26 (**enthält RE-4 `rename_folder` und RE-3 `rename_space`**) (die UI-Änderungen aus Block 13 fahren mit) · **+ Block 14.7** (Karte kompakt/verteilt/glatt, 2026-10-29 geplant) |
| H | `v3.1.7` | — | — | **Hotfix B1** (Plan Block 15 §3, Lock P10.5-X): Branch `hotfix/v3.1.7-b1` von `e5c834e`, nur die `asset_id`-Validierung; `deploy.sh hotfix/v3.1.7-b1` beim Nikinger, danach Merge nach `main` |

**Stand 2026-10-24 (Abend):** Deploy A ist **live** (`v3.1.5`, Release `20261023T065010.377336Z`, SHA `7358f22`, `health_gate` **9/9 OK**); der Branch `p105-block5` (Block 5 + 6 + P10.5-26) ist **gemergt**. **Deploy B ist ebenfalls live**: `v3.1.6`, Release `20261023T165838.591015Z`, SHA `e5c834e`, `health_gate` **9/9 OK** (aus `main` mit `fastmcp 4.1.3`; der Deploy lief beim Nikinger, die Release-Tests im Release **1380 grün** in 340,7 s). **Block 7.1 (UI-1) ist gemergt** (`f0e76b0`) und damit ab `v3.1.7` dabei. **Deploy C (`v3.1.7`) ist vorbereitet** — Badge, eigener Update-Log-Block `## 2026-10-24` (9 Zeilen für Menschen), Suite **1425 grün** (332,6 s), `doc_health` 0, `ui_budget` **5/5** (Erstaufruf 204,5 KB); **`deploy.sh` liegt beim Nikinger**. **Die Generalprobe davor ist gefahren: 26/26 Zellen grün an der Wegwerf-Instanz** (Details im Session-Block unten; die Zeile stand vorher auf „25/25" — **datierte Korrektur**, der Block-7.0-Commit hat die Probe um eine Zelle erweitert). **Der Deploy-Aufruf der letzten Session ist an den Release-Tests gescheitert — nicht am Befehl:** eine verklebte `updated:`-Zeile in `SESSIONS_ARCHIVE.md` (behoben, Details im Session-Block) — es fehlt nur noch der Deploy-Aufruf durch den Nikinger. **Block 7.1 (UI-1) ist gebaut** auf dem Branch `p105-block7` — **nicht gemergt** (Nikinger-Entscheidung: Deploy A vor dem Branch-Merge); der Merge wartet auf Deploy A/B.

**Ein Deploy ist vier Schritte, kein Commit** (Plan §2.5): volle Suite + `doc_health` + `ui_budget` grün · Badge und `docs/UPDATE_LOG.md` · Commit + Push · **`deploy.sh` durch den Nikinger** (Hard Rule 9) · `health_gate.sh` mit **echter Ausgabe** in den Commit — nie die Behauptung.

## Abnahmestand

**72 Zeilen** (P10.5-1–72) — **geteilt**: die **geschlossenen** Zeilen (✅/⚠️) stehen
**verbatim** in [`ABNAHME_ARCHIVE.md`](ABNAHME_ARCHIVE.md) (L3), hier stehen die **offenen**
(⬜) und die Summe. **[2026-10-27, Block 14.35]** die Beschriftungs-Zeile des Kartenlayouts ist
**geschlossen**: **P10.5-71** (keine zwei gezeichneten Beschriftungs-Rechtecke überlappen
sich — **0** Paare statt 5, **3** von **13** Beschriftungen weggelassen, die Fokus-
Beschriftung ist am Pixel nachgewiesen da) steht jetzt im Archiv, mit ihrem Beleg; die
Zeilen 68/69 sind geschlossen, **70 wartet auf die Bilder**. **[2026-10-26, Block 14.3]**
die Kamera-Zeile: **P10.5-67** (der Inhalt füllt **93,6 %** der Leinwand, passt **in** sie
und sitzt **0,42 px** neben der Mitte — vorher 32,3 px) steht jetzt im Archiv, mit ihrem
Beleg; die Zeilen 68/69/71 bleiben offen, 70 wartet auf die Bilder.
**[2026-10-28, Block 14.5 — datierte Änderung der Zahlen]** der Rand der Kamera ist von
**40 px** auf **56 px** gewachsen (die Lappen-Kontur stand sonst **3,8 px** über dem
Leinwandrand — der Plan §2.5); der Füllgrad ist deshalb **91,1 %** statt 93,6 % und der
Versatz **0,49 px** statt 0,42 px. Die **Abnahmezeile** P10.5-67 (≥ 60 %) bleibt davon
**unberührt** ✅. **[2026-10-26, Block 14.1]** die
erste Zeile des Kartenlayouts ist geschlossen: **P10.5-65** (der Determinismus — zwei frische
Ladevorgänge, **0,0 px** über 152 Knoten). **[2026-10-25, Block 13]** +3 Zeilen (62/63/64) —
die älteren Zeilen unverändert. **[2026-10-26, Block 14.0]** +7 Zeilen (65–71 — die
Abnahmezeilen des Kartenlayouts, aus dem Plan
`docs/concepts/phase10_5_block14_kartenlayout_plan.md` §5).
Zählregel (Plan §5): ✅ erfüllt mit Beleg am Ort · ⚠️ erfüllt in anderer Form, Abweichung
benannt · ⬜ offen. Die Kriterien der Blöcke 14 stehen **wortgleich** im Plan
(`docs/concepts/phase10_5_block14_kartenlayout_plan.md` §5), die älteren Zeilen sind Kurzfassungen
(je Block am Ende des jeweiligen Plans); die **Belegte**
stehen im Commit und im Session-Block.

> **Datierte Korrektur zum Plan (2026-10-25, Block 11.8).** Der Plan §5 sagt „**61 Zeilen**,
> gezählt im Phase-Head". Der Head stand beim Bau von Block 11.8 bei **41.398 B** — über dem
> Softcap (40.960 B). Die geschlossenen Zeilen wandern deshalb **verbatim** in ein L3-Archiv
> (derselbe Schnitt wie beim Modulstatus in Block 11.4); **gezählt** werden die 61 Zeilen
> weiterhin — im Head **und** im Archiv.

| # | Kriterium | Status | Beleg |
|---|---|---|---|
| P10.5-18 | Live nach Deploy A: `/overview` Waiting ≤ 300 ms, Space-Wechsel während des Polls ≤ 1 s (Nikinger, DevTools, beide Eingänge) | ⬜ | — |
| P10.5-22 | Live nach Deploy B: claude.ai-Connector `list_spaces`/`search_items`/`get_item`/`update_item` ok (Nikinger); Log-Feld `proto` zeigt die Ära (V208) | ⬜ | — |
| P10.5-27 | **Live P10-J Lauf 1** (M3.1 Flash) | ⬜ | — |
| P10.5-28 | **Live P10-J Lauf 2** (lokales Modell, CT 111) — mit 27 die Abschlussbedingung der Phase | ⬜ | — |
| P10.5-49 | Live nach Deploy D: Ereignisse kommen über **beide** Eingänge an (V212 ✅) | ⬜ | — |

| P10.5-60 | P10-J zweimal live belegt | ⬜ | — |
| P10.5-61 | Closeout-Dokumente + Rotationen per Skript | ⬜ | — |

**Summe:** 67 ✅ · 0 ⚠️ · 7 ⬜ (von 74). **[2026-10-29, Sichtung]** +1 ✅ (10-70 die drei Kartenbilder von Block 14.7, vom Nikinger abgenommen) ⇒ 67 ✅ · 0 ⚠️ · 7 ⬜. **[2026-10-29, Block 14.7.5]** +2 ✅ (10-73 kompakt und verteilt — Solidität 0,830, NN 35,95 px; 10-74 glatt — Zusatzkrümmung 1,86) ⇒ 66 ✅ · 0 ⚠️ · 8 ⬜. **[2026-10-29, Block 14.7.0]** +2 Zeilen (73/74 — Form und Kontur der Karte, Plan `docs/concepts/phase10_5_block14_7_plan.md` §5; die Basislinie ist rot, das ist der Befund) ⇒ 64 ✅ · 0 ⚠️ · 10 ⬜. **[2026-10-28, Block 14.6.3]** +1 ✅ (10-72 der **Körper** — die Körpermaske aller Spaces ist **eine** Komponente (6274 Zellen), jeder Space hat **genau einen** Lappen, **146** Furche-Zellen, **4** Paare, Reach **47,9 / 44,1 / 48,4 / 44,6 px**, Luft **7,2 / 10,7 / 82,9 / 85,6 px**, `computeLobes()` **30,8 ms** (152) · **34,6 ms** (201 Knoten) — der Gegenlauf `koerper` macht **genau diese** Zelle rot) ⇒ 64 ✅ · 0 ⚠️ · 8 ⬜. **[2026-10-27, Block 14.35]** +1 ✅ (10-71 die Beschriftungen — **0** überlappende Paare (der Stand 14.3 zählte **4** per Pixelvergleich — der Recorder zählt dieselbe Szene mit **5**), **3** von **13** Beschriftungen weggelassen, die Fokus-Beschriftung am Pixel nachgewiesen da; der Gegenlauf `beschriftung` macht **genau diese** Zelle rot) ⇒ 63 ✅ · 0 ⚠️ · 8 ⬜. **[2026-10-26, Block 14.3]** +1 ✅ (10-67 die Kamera — Füllgrad **93,6 %**, der Inhalt passt, der Umriss sitzt **0,42 px** neben der Mitte statt 32,3 px) ⇒ 62 ✅ · 0 ⚠️ · 9 ⬜. **[2026-10-26, Block 14.2]** +3 ✅ (10-66 die Regionen — **152/152 = 100 %**; 10-68 die Stabilität — Median **0,0 px**; 10-69 das Budget —
 201 Knoten in **2147 ms**, 0 Frames) ⇒ 61 ✅ · 0 ⚠️ · 10 ⬜. **[2026-10-26, Block 14.1]** +1 ✅ (10-65 der Determinismus — zwei frische Ladevorgänge, **0,0 px** über 152 Knoten, der Beleg byteweise reproduzierbar; der Gegenlauf `seedJitter` → `Math.random()` macht **genau diese** Zelle rot) ⇒ 58 ✅ · 0 ⚠️ · 13 ⬜. **[2026-10-26, Block 14.0]** +7 Zeilen (65–71 — das Kartenlayout; die **Basislinie** ist in `regionen`, `kamera`, `beschriftungen` und `stabilitaet` **rot**, das ist gewollt und gemessen) ⇒ 57 ✅ · 0 ⚠️ · 14 ⬜. **[2026-10-26, Nikinger-Sichtung]** +3 ✅ (10-32 UI-4, 10-37 C2-Stil, 10-51 Editor live) ⇒ 57 ✅ · 0 ⚠️ · 7 ⬜. **[2026-10-25, Block 13]** +3 ✅ (10-62 die Editor-Größen, 10-63 die Knopfleiste nach Word, 10-64 die Knopffarben) ⇒ 54 ✅ · 0 ⚠️ · 10 ⬜. **[2026-10-25, Block 12]** +3 ✅ (10-57 Oversize, 10-58 ROADMAP, 10-59 Register-Bilanz) ⇒ 51 ✅ · 0 ⚠️ · 10 ⬜. **[2026-10-25, Block 11.6]** +2 ✅ (10-54 ED-3 die Format-Konvention, 10-56 die P1-Ankündigung) ⇒ 48 ✅ · 0 ⚠️ · 13 ⬜. **[2026-10-25, Block 11.8]** +2 ✅ (10-52 der Roundtrip, 10-55 der Rohmodus) ⇒ 46 ✅ · 0 ⚠️ · 15 ⬜. **[2026-10-25, Block 11.5]** +1 ✅ (10-53, ED-2 die To-do-Kästchen) ⇒ 44 ✅ · 0 ⚠️ · 17 ⬜. **[2026-10-25, Block 11.7]** +1 ✅ (10-50, das Budget) ⇒ 43 ✅ · 0 ⚠️ · 18 ⬜. **[2026-10-24, Block 10.5]** +4 ✅ (10-45, 10-46, 10-47, 10-48) ⇒ 42 ✅ · 0 ⚠️ · 19 ⬜. **[2026-10-24, Block 9.3]** +2 ✅ (10-43, 10-44) ⇒ 38 ✅ · 0 ⚠️ · 23 ⬜. **[2026-10-24, Block 9.2]** +1 ✅ (10-42, RE-4 `rename_folder`) ⇒ 36 ✅ · 0 ⚠️ · 25 ⬜. **[2026-10-24, Block 9.1]** +1 ✅ (10-41, RE-7 `created_by`) ⇒ 35 ✅ · 0 ⚠️ · 26 ⬜. **[2026-10-24, Block 8]** +4 ✅ (10-36, 10-38, 10-39, 10-40) ⇒ 34 ✅ · 0 ⚠️ · 27 ⬜. **[Stand 2026-10-24, Block 7.5–7.7]** 33, 34 und 35 ✅. **[Korrektur 2026-10-22, Block 6]** Die Zeile stand vorher auf „21 ✅ · 0 ⚠️ · 40 ⬜“ — die Tabelle trug aber **20** ✅ (der Zähler war schon vor diesem Block falsch; Block 5 hat eine Zeile auf ✅ gezogen und die Summe nicht nachgezogen). Neu: **23**, weil Block 6 drei Zeilen (10-23/24/25) auf ✅ gesetzt hat. Ein Wächter prüft die Summe jetzt gegen die Tabelle (`tests/test_head_rules.py`) — **über beide Dateien**, seit die geschlossenen Zeilen im Archiv stehen. **[2026-10-23, Block 7.1]** +1 ✅ (10-29, UI-1) ⇒ 25 ✅ · 0 ⚠️ · 36 ⬜. **[2026-10-23, Block 7.2]** +1 ✅ (10-30, UI-2) ⇒ 26 ✅ · 0 ⚠️ · 35 ⬜. **[2026-10-23, Block 7.3]** +1 ✅ (10-31, UI-3) ⇒ 27 ✅ · 0 ⚠️ · 34 ⬜.

## Offen beim Nikinger

- **Block 15 (2026-10-30, entschieden):** B1 als **Hotfix `v3.1.7`** vorab (H3: `deploy.sh` + `health_gate.sh` + Live-Probe `get_item_asset(asset_id="../../../x")` → `invalid:`); Ausführer Claude Code (Modell: Empfehlung Opus 5.5 für Kern/Auth, Sonnet 5.5 für Haushalt/Doku/Film); P1-Öffnung 16 frei; B21-Eingriff in `phase4_auth/` frei (P10.5-AD). Offen: V230 (Live-Zählung `auth_requests`, nur lesend) und der OS-Truststore der VM (P10.5-AG).
- **Block 16 (2026-10-30):** Sichtung E1 (Storyboard, Schritt 16.0) und E2 (Film, 16.5); Medienverzeichnis `/var/lib/sharefyx-media` + Unit-Umgebung vor Deploy D (Film-Plan §3).
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
- **Handover-Posten (Regelkandidat, Nikinger 2026-10-25):** Sichtungen **zuerst als Bilder an der Wegwerf-Instanz**, live nur, was der Server nicht selbst entscheiden kann — steht als Arbeitsweise schon in der Wurzel-`CLAUDE.md` (2026-10-22); für den Closeout-Handover als feste Regel prüfen.
- **Block 2, Zeile 15 (AL-1)** — Migration + Live-Check beim Nikinger.
- **[2026-10-28 entschieden: Option B — ein Körper, das Layout bleibt; Plan 14.6 `docs/concepts/phase10_5_block14_6_plan.md`]** **NEU 2026-10-26 (Block 14.2): die „Gehirnkarte“ wird zu Inseln — die C2-Furche hat im neuen
  Layout keinen Gegenstand.** Die neue L4 (Anker-Gravitation + Querfedern) rückt die Spaces
  **auseinander**: die Lappen zweier Spaces **berühren** sich nicht mehr. **Gemessen:** die
  Furche-Zellen in der C2-Probe **62 → 0**; in der Produktionskarte (5 Spaces) liegen die
  Schwerpunkte der Spaces **mindestens 346 px** auseinander, der Radius der Körpermaske ist
  **48 px** ⇒ dort kann keine Furche entstehen. Die **C2-Zeichenregel** ist damit im Alltag
  **nicht mehr sichtbar** (die Furchen zwischen den Lappen), die Bahnen zwischen den Spaces
  werden **lang**. **Kein Fehler, eine Folge des beauftragten Layouts** — aber eine **sichtbare
  Änderung** der in Block 8/9 abgenommenen Optik. **Was der Nikinger entscheiden muss:** die
  Bilder aus **14.5** zeigen die Inseln (gemessen: **5** Lappen, **0** Furche-Zellen — die
  Inseln berühren sich nicht); soll die C2-Optik (Furchen, Bahnen) an die Inseln
  angepasst werden (eigener Schritt nach 14.5) oder so bleiben? **Bis dahin** ist der C2-Wächter
  auf einen **festen Eingang** gestellt (zwei Spaces **berühren** sich dort, wo die Furche etwas
  zu trennen hat) — er prüft damit die **Zeichenregel**, nicht das Layout; ohne diese Reparatur
  wäre der Gegenlauf „Furche aus“ **grün** geblieben, ohne dass der Fehler wiederhergestellt
  war (`probes/p105_b8_c2_probe.mjs`, datierter Kommentar; `tests/test_graph_c2.py`).
  **Stand 2026-10-28 (Block 14.6): die Frage ist beantwortet — Option B ist umgesetzt.** Der
  Körper ist geschlossen (`LOBE_CLOSE_PX = 160`; die sechs Varianten in 14.6.1, der Wert vom
  Nikinger nach der Standardregel des Plans §3 entschieden), die Karte ist **ein Körper** mit
  Lappen und Furchen, **kein Knoten** hat seinen Platz gewechselt. **P10.5-72** ist ✅ (der
  Beleg: `probes/p105_b14_karte_bilder.json`). **Offen bleibt die Sichtung P10.5-70** — die
  drei Bilder im Repo sind die **neuen** (Schritt 14.6.3).
- **2026-10-28 (Block 14.5): die Update-Log-Zeile für das neue Kartenlayout** ist **geschrieben**
  (Nachzug 14.5, im Block `## 2026-10-26` — dem Block des Deploys D). **Bleibt beim Deploy:**
  das `deploy.sh`-Gate verlangt, dass die
  **oberste** `##`-Überschrift in `docs/UPDATE_LOG.md` **das Datum des Deploy-Tages** trägt
  (jetzt `## 2026-10-26`) — der Block muss am Deploy-Tag **umdatiert** werden, sonst bricht
  das Gate ab (`SHAREFYX_ALLOW_STALE_UPDATELOG=1` überspringt es, ist aber nicht die Absicht).
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
> **Verbatim verschoben** nach `STARTUPTRAG_ARCHIVE.md` (`scripts/move_sections.py`) — dort unter derselben Überschrift.

## Startauftrag — Block 9 (Rechte und Namen: RE-7, RE-4, RE-3) · Ausführer
> **Verbatim verschoben** nach `STARTUPTRAG_ARCHIVE.md` (`scripts/move_sections.py`) — dort unter derselben Überschrift.

## Nächste Session — Aufträge des Nikingers (2026-10-25): **alle vier gebaut** (Block 13)

> **Stand 2026-10-27:** die vier Aufträge (Editor-Größen, Knopfleiste nach Word, Knopffarben, die
> ganze Gehirnkarte) sind gebaut **und gemessen** — Belege im Modulstatus, Abnahmezeilen
> P10.5-62/63/64, die Aufträge **wortgleich** im Session-Archiv (`SESSIONS_ARCHIVE.md`, Block 13).
> **Offen ist die Sichtung**, nicht die Arbeit: die drei **Sichtungen** **P10.5-37** (C2-Stil der
> Karte), **P10.5-51** (Editor Stufe 1) und **P10.5-32** (UI-4) — drei Bilder, drei Urteile; die
> Deploys **C** (`v3.1.7`) und **D** (`v3.1.8`, jetzt **mit** den Änderungen aus Block 13) liegen
> beim Nikinger.

## Session stopped — 2026-10-30 (Planungssession „Ultra“: Block 15 Fixes + Hotfix, Block 16 Launch-Film — Pläne stehen)

**Ergebnis.** Zwei Pläne, ausführungsreif gegen `main@2d45e66`: **Block 15** (`docs/concepts/phase10_5_block15_ultra_plan.md`, 📕) schließt **alle 22 Befunde** des Ultra-Reviews, davor der **Hotfix `v3.1.7`** für B1 (Branch von `e5c834e`; der verwundbare Code ist dort byteweise derselbe). **Block 16** (`docs/concepts/phase10_5_launch_film_plan.md`, aus der Notiz zum Plan geworden) baut den Launch-Film: ein Film ≈ 40 s, Deutsch, echte Oberfläche von der Wegwerf-Instanz in einer stilisierten Ebene, Playwright-Frames + ffmpeg (Rückfall Remotion), In-App beim ersten Start, Wiederaufruf im Update-Log. Locks **P10.5-X–AM**, Abnahme **P10.5-75–92** (18 Zeilen, kommen in 15.0 in den Head), `[VERIFY]` **V220–V232**. Die Planungssession lief als Cloud-Session (Fable 5.1, Branch `nikinger_claude/elegant-volta-gnyarh`).

**Entscheidungen des Nikingers (2026-10-30):** alles wie empfohlen; Unarchive wird gebaut (P10.5-AB); B12 und B21 im Block (P10.5-AC/AD); kein FastMCP-Bump (4.1.4 geprüft — nichts für uns); Film 40 s mit Luft, Publikum alle Nutzer, Mehraufwand In-App akzeptiert, Musik optional, Budget eine Woche; Reihenfolge Hotfix → 15 → 16 → Deploy D.

**Step 0 (Verifikation):** `doc_health` 0, Oversize nur 📕/📦, Indexzeilen vollständig — **nichts zu tun außer Luft:** INDEX 5 B unter dem Reserve-Wächter, P2-Head 329 B unter dem Softcap, dieser Head 1.478 B. Heute geschaffen: Zeilen 11/13/14 verbatim nach `MODULSTATUS_ARCHIVE.md` (Head 39.482 → ~31 KB), INDEX-Zeile 122 (p8x-Notizen) ins Kürzungs-Archiv; der P2-Head ist Schritt 15.0.

**Gemessen:** alle 22 Anker verifiziert; B1 (`pathlib.glob` mit `..`), B20 (CRLF) und die YAML-Typen zu B5 nachgestellt; Threadpool zu B10 in FastMCP 4.1.3 bestätigt. Testbasis (Scratchpad-venv aus `constraints.txt`): **1654 grün, 5 rot** (nur `sqlite3`-Binary fehlt im Container — wie im Review). PyPI: fastmcp 4.1.4/4.2.0a1, starlette 1.10.0, pydantic 2.14.2; MCP 2026-07-28 bleibt „Current“.

**Nächster Schritt:** Branch mergen, dann **H0** (Hotfix-Branch, Claude Code auf der VM, Modell nach Empfehlung Opus 5.5), H3 beim Nikinger; danach 15.0.
