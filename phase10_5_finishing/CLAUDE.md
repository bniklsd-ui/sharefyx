---
status: live
purpose: Phase-10.5-Head — **Closeout Z erledigt 2026-11-07** (formaler Schluss beim Nikinger). Modulstatus der Blöcke 0–19/Z, Deploy-Tabelle A–F, Abnahmestand P10.5-1–86 (alle ✅), offene Punkte beim Nikinger (vollständig im Handover), Abschluss-Session-Block. Plan und Arbeitsliste stehen in eigenen Dateien.
read-when: Arbeiten in phase10_5_finishing/ — zuerst lesen, zusammen mit dem Session-Block unten
detail: L2
up: ../ROADMAP.md
down:
  - ../docs/concepts/PHASE10_5_CLOSEOUT_HANDOVER.md # 📕 Closeout-Handover P10.5 → P11 (2026-11-07)
  - ../docs/concepts/phase10_5_finishing_plan.md    # 📕 der Plan: Locks P10.5-A–W, Blöcke 0–12/Z, Abnahme, [VERIFY] V207–V219
  - ../phase10_inventory/BAUSTELLENREGISTER.md      # 📗 die Arbeitsliste — hier wird abgehakt (P10-B)
  - ../phase10_inventory/ENTSCHEIDUNGEN_ARCHIVE.md  # 📦 §12 Entscheidungsliste D-1–D-18, verbatim
  - SESSIONS_ARCHIVE.md                             # 📦 ältere Session-Blöcke, verbatim, newest-first
  - UPDATES_ARCHIVE.md                              # 📦 die älteren `updated:`-Fäden dieses Heads, verbatim
  - STARTUPTRAG_ARCHIVE.md                          # 📦 die Startaufträge der Blöcke 7 und 9, verbatim
  - MODULSTATUS_ARCHIVE.md                         # 📦 die ausführlichen Statusspalten der Blöcke 0–10 und 11–17, verbatim
  - ABNAHME_ARCHIVE.md                             # 📦 die geschlossenen Abnahmezeilen (P10.5-1–72), verbatim
  - FREIGABEN_ARCHIVE.md                           # 📦 die Freigaben der Phase, verbatim
updated: 2026-11-07 (Closeout Z: Phase 10.5 abgeschlossen — 86 ✅ · 0 ⚠️ · 0 ⬜, Handover + Grafik, Modulstatus 7/8/11/19 ✅, Vollzeilen 18/19 ins Archiv; Writer-Optik des Editors nicht erfüllt → P11; formaler Schluss beim Nikinger) | ältere Einträge: phase10_5_finishing/UPDATES_ARCHIVE.md
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
| 7 | Darstellung: UI-1–UI-6, KA-5 | Ausführer (+ Claude Code Sichtung) | C | ✅ 2026-10-26 (Sichtung P10.5-32) |
| 8 | Karte: Gehirnkarte C2 | Ausführer (+ Claude Code Smoke/Sichtung) | C | ✅ 2026-10-26 (Sichtung P10.5-37) |
| 9 | Rechte und Namen: RE-7 (P1-12), RE-4 (P1-13), RE-3 (P1-14) | Ausführer | D | ✅ 2026-10-24 |
| 10 | Suche und Realtime: LG-1, LG-2 | Ausführer (+ Claude Code Proben) | D | ✅ 2026-10-24 |
| 11 | Editor Stufe 1 + 2: ED-1, ED-2, ED-3 (P1-11), ED-5 | Ausführer (+ Claude Code Proben/Sichtung) | D | ✅ 2026-10-26 (Sichtung P10.5-51) — Maß der Zeit erfüllt; das Soll „sieht aus wie ein Writer-Dokument“ war nie Maß und ist **nicht** erfüllt → P11 (Handover §2) |
| 12 | Doku und Altlasten: DO-1, LG-6, AL-1 (Rest), AL-3, BG-2/BG-3 | Claude Code | — | ✅ 2026-10-25 |
| 13 | Aufträge des Nikingers: UI-8 (die Größen wirken live), UI-9 (die Knopfleiste nach Word), UI-10 (die Knopffarben) | Claude Code (Sichtung Nikinger) | D | ✅ 2026-10-25 — Maß der Zeit (Größen, Reihenfolge der Knöpfe, Farben); Writer-Optik siehe Block 11 |
| 14 | Kartenlayout „zufällig, aber geordnet“ (Nikinger 2026-10-26) — Plan `docs/concepts/phase10_5_block14_kartenlayout_plan.md` | Ausführer (opencode) + Claude Code (Bilder) | D | ✅ 2026-10-29 (Sichtung P10.5-70 abgenommen) |
| 15 | Fixes aus dem Ultra-Review B1–B10 — Plan `docs/concepts/phase10_5_block15_review_fixes_plan.md` | Claude Code | D | ✅ 2026-10-31 |
| 16 | Launch-Film v4.0.0 (Nikinger 2026-10-29/31) — Plan `docs/concepts/phase10_5_launch_film_plan.md` | Claude Code (Sichtung Nikinger) | vor D | ✅ 2026-11-01 |
| 17 | Film in die App (Nikinger 2026-11-01) — Plan `docs/concepts/phase10_5_block17_film_app_plan.md` | Claude Code | D | ✅ 2026-11-01 |
| 18 | Live-Funde nach D: Karte träge (Tags/Ordner), Ausreißer, Editor-Farben — Plan `docs/concepts/phase10_5_block18_live_fixes_plan.md` | eigene Session | v4.0.1 | ✅ live 2026-11-03 (`v4.0.1`, Deploy E) — P10.5-18/49/80–83 ✅; A1 (`ausreisser`) live nicht beobachtbar, kein Code → Handover §6 · Vollzeile im Archiv |
| 19 | Editor v4.0.2 — Hotfix aus dem Editor-Plan (S0 Render-Probe, S1 Entwurfsschutz, S2 Tabellen-Widget; Plan `docs/concepts/phase10_5_editor_4_1_plan.md`) | Claude Code | F | ✅ live 2026-11-06 (`v4.0.2`, Deploy F) — S0–S2R gebaut, P10.5-84–86 ✅ (85 live gesichtet 2026-11-07); S3a–S11 = P11 Block 1 · Vollzeile im Archiv |
| Z | Closeout P10.5 (Handover, Grafik, Rotationen) | Claude Code + Nikinger | — | ✅ 2026-11-07 — `docs/concepts/PHASE10_5_CLOSEOUT_HANDOVER.md`, `docs/concepts/phase10_5_finishing_uebersicht.svg` (zweimal gerendert und angesehen), Session-Block per Skript rotiert; formaler Schluss (ROADMAP, Wurzel) beim Nikinger |

> **Die ausführlichen Statusspalten der Blöcke 0–10 und 11–17 stehen verbatim in
> [`MODULSTATUS_ARCHIVE.md`](MODULSTATUS_ARCHIVE.md) (L3) — hier trägt der Modulstatus den
> **Kurzstand**. Grund: der Head stand beim Bau von Block 11.4 über dem Softcap; die
> Details der geschlossenen Blöcke bleiben im Archiv nachlesbar, der Head bleibt der
> *live* Stand.

## Deploy-Tabelle

| # | Version | SHA | `health_gate` | Ausgabe |
|---|---|---|---|---|
| A | `v3.1.5` | `7358f22` | **9/9 OK** | nach Block 1–4 — **live seit 2026-10-23**, Release `20261023T065010.377336Z` |
| B | `v3.1.6` | `e5c834e` | **9/9 OK** | nach Block 5–6 (+ **Block 7.0**, die Update-Log-ID) — **live seit 2026-10-23**, Release `20261023T165838.591015Z` · **Deploy beim Nikinger** (Hard Rule 9, `sudo`; `deploy.sh main` → Release-Tests **1380 grün** (340,7 s) → Symlink-Wechsel → Dienst neu gestartet) · `health_gate.sh --expected-version=v3.1.6 --require-todays-update-log --expected-sha=e5c834e` → **9/9 OK** (`.rail__version` v3.1.6, Release-SHA `e5c834e…`, Update-Log 2026-10-23) · **Block 7.1 (UI-1) ist gemergt** (`f0e76b0`, aus `p105-block7`) — **nicht** in diesem Release, sondern in `v3.1.7` |
| C | `v3.1.7` | — | — | nach Block 7–8 — **2026-10-24 vorbereitet** (Badge, eigener `## 2026-10-24`-Block im Update-Log, Suite 1425 grün, `doc_health` 0, `ui_budget` 5/5), **`deploy.sh` beim Nikinger** · **[2026-11-07, Closeout]** nie einzeln ausgeliefert — der Badge `v4.0.0` stand schon auf dem Branch, C ist in D enthalten |
| D | `v4.0.0` (vorher `v3.1.8`; Nikinger 2026-10-26) | `2eb697f` | **9/9 OK** | **live seit 2026-11-01**, Release `20261101T172738.984499Z` (Release-Tests 1842 grün; Deploy beim Nikinger; enthält C) · nach Block 9–11 **+ 13** + Nachzug 2026-10-26 (**enthält RE-4 `rename_folder` und RE-3 `rename_space`**) (die UI-Änderungen aus Block 13 fahren mit) · **+ Block 14.7** (Karte kompakt/verteilt/glatt, 2026-10-29 geplant) · **+ Block 15** (Review-Fixes B1–B10 inkl. B1 — **kein** Hotfix vorab, Nikinger 2026-10-30: Deploy nach allen Fixes, Wochenende) · **+ Block 17** (Film in der App, ✅ 2026-11-01) · Update-Log `## 2026-11-01` · **`deploy.sh` + `health_gate.sh` beim Nikinger** |
| E | `v4.0.1` | `0e317cf` | **9/9 OK** | **live seit 2026-11-03**, Release `20261103T064426.832031Z` (Release-Tests 1862 grün; Deploy beim Nikinger) · Block 18: Karte flüssig (Stern, Mindestdistanz, Zwischenspeicher), Update-Log `## 2026-11-03` · Nikinger live: „Layout zurücksetzen“ mehrfach — das Bild bleibt gut; Gefühl **flüssig** bestätigt (Bild mit beiden Schaltern, kein Einzelpunkt weit draußen) |
| F | `v4.0.2` | `d2ca573` | **8/9** (Folgetag, Datumsartefakt) | nach Block 19 (Editor-Hotfix S0–S2) — **2026-11-06 vorbereitet** (Badge `v4.0.2`, Update-Log `## 2026-11-06` mit drei Zeilen, Suite grün, `doc_health` 0, `ui_budget` 6/6, Probe Chromium + Firefox rot 26 wie erwartet, 0 Abweichungen), **`deploy.sh` beim Nikinger** — **live seit 2026-11-06**, Release `20261106T153734.706504Z`, SHA `d2ca573` (Nikinger: „looks good“); **`health_gate` am 2026-11-07 09:18 UTC (einen Tag nach dem Deploy) = 8 von 9 OK, 1× FEHLER:** der Update-Log-Check erwartete wegen `--require-todays-update-log` den 2026-11-07, der oberste Eintrag trägt (richtig) den Deploy-Tag 2026-11-06 — ein **Datumsartefakt des verspäteten Laufs**, kein Fehler im Release (`/health` 200, `/ui/login` 200, `/api/v1/me` 401, `/mcp/` 401, `.rail__version` v4.0.2, Symlink, Release-SHA gleich `--expected-sha` alles OK); ein sauberer Lauf ohne das Flag steht aus; live gesichtet 2026-11-07 (P10.5-85 ✅) |

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

> **[2026-11-07, Closeout Z]** Keine offene Zeile mehr — P10.5-61 steht seitdem im Archiv; die Tabelle der offenen Zeilen ist leer.

**Summe:** 86 ✅ · 0 ⚠️ · 0 ⬜ (von 86). **[2026-11-07, Closeout Z]** +1 ✅ (10-61 Closeout-Dokumente + Rotationen) ⇒ 86 ✅ · 0 ⚠️ · 0 ⬜ — die Writer-Optik des Editors war **keine** Zeile und ist **nicht** gezählt (Handover §2; eine Zeile öffnen = Entscheidung des Nikingers). **[2026-11-07, Sichtung]** +1 ✅ (10-85 Tabellen-Widget live gesichtet) ⇒ 85 ✅ · 0 ⚠️ · 1 ⬜ (offen: 10-61 Closeout). **[2026-11-07, eurofleet-Rückmeldung]** +3 ✅ (10-27 Lauf 1, 10-28 Lauf 2, 10-60 zweimal live) ⇒ 84 ✅ · 0 ⚠️ · 2 ⬜ (offen: 10-61 Closeout, 10-85 Tabelle live). **[2026-11-06, Block 19]** +2 ✅ (10-84 Entwurf, 10-86 Byte-Vertrag) und +1 Zeile (10-85 Tabellen-Widget, Sichtung live) ⇒ 81 ✅ · 0 ⚠️ · 5 ⬜. **[2026-11-03, live v4.0.1]** +2 ✅ (10-18 `/overview` Waiting und Space-Wechsel, 10-49 Ereignisse über beide Eingänge — Wegwerf-Probe 18.5, Zahlen vom Nikinger angenommen) ⇒ 79 ✅ · 0 ⚠️ · 4 ⬜. **[2026-11-03, Sichtung]** +1 ✅ (10-83 V3/V4, Bild vom Nikinger gesichtet) ⇒ 77 ✅ · 0 ⚠️ · 6 ⬜. **[2026-11-02, Block 18]** +3 ✅ (10-80 Stern, 10-81 Mindestdistanz/`insel`, 10-82 Zwischenspeicher) und +1 Zeile (10-83 V3/V4, Sichtung) ⇒ 76 ✅ · 0 ⚠️ · 7 ⬜. **[2026-11-01, live]** +1 ✅ (10-22 Connector, `proto` 2026-07-28) ⇒ 73 ✅ · 0 ⚠️ · 6 ⬜. **[2026-10-31, Block 15.7]** +1 ✅ (10-79 B6/B7/B9/B10) ⇒ 72 ✅ · 0 ⚠️ · 7 ⬜. **[2026-10-30, Block 15.4]** +1 ✅ (10-78 B4 Mitglieder) ⇒ 71 ✅ · 0 ⚠️ · 8 ⬜. **[2026-10-30, Block 15.3]** +1 ✅ (10-77 B5/B8 Typen) ⇒ 70 ✅ · 0 ⚠️ · 9 ⬜. **[2026-10-30, Block 15.2]** +1 ✅ (10-76 B2/B3/B20 Dienststart) ⇒ 69 ✅ · 0 ⚠️ · 10 ⬜. **[2026-10-30, Block 15.1]** +1 ✅ (10-75 B1/B15 `asset_id`) und +4 Zeilen (76–79, Plan Block 15 §4) ⇒ 68 ✅ · 0 ⚠️ · 11 ⬜. **[2026-10-29, Sichtung]** +1 ✅ (10-70 die drei Kartenbilder von Block 14.7, vom Nikinger abgenommen) ⇒ 67 ✅ · 0 ⚠️ · 7 ⬜. **[2026-10-29, Block 14.7.5]** +2 ✅ (10-73 kompakt und verteilt — Solidität 0,830, NN 35,95 px; 10-74 glatt — Zusatzkrümmung 1,86) ⇒ 66 ✅ · 0 ⚠️ · 8 ⬜. **[2026-10-29, Block 14.7.0]** +2 Zeilen (73/74 — Form und Kontur der Karte, Plan `docs/concepts/phase10_5_block14_7_plan.md` §5; die Basislinie ist rot, das ist der Befund) ⇒ 64 ✅ · 0 ⚠️ · 10 ⬜. **[2026-10-28, Block 14.6.3]** +1 ✅ (10-72 der **Körper** — die Körpermaske aller Spaces ist **eine** Komponente (6274 Zellen), jeder Space hat **genau einen** Lappen, **146** Furche-Zellen, **4** Paare, Reach **47,9 / 44,1 / 48,4 / 44,6 px**, Luft **7,2 / 10,7 / 82,9 / 85,6 px**, `computeLobes()` **30,8 ms** (152) · **34,6 ms** (201 Knoten) — der Gegenlauf `koerper` macht **genau diese** Zelle rot) ⇒ 64 ✅ · 0 ⚠️ · 8 ⬜. **[2026-10-27, Block 14.35]** +1 ✅ (10-71 die Beschriftungen — **0** überlappende Paare (der Stand 14.3 zählte **4** per Pixelvergleich — der Recorder zählt dieselbe Szene mit **5**), **3** von **13** Beschriftungen weggelassen, die Fokus-Beschriftung am Pixel nachgewiesen da; der Gegenlauf `beschriftung` macht **genau diese** Zelle rot) ⇒ 63 ✅ · 0 ⚠️ · 8 ⬜. **[2026-10-26, Block 14.3]** +1 ✅ (10-67 die Kamera — Füllgrad **93,6 %**, der Inhalt passt, der Umriss sitzt **0,42 px** neben der Mitte statt 32,3 px) ⇒ 62 ✅ · 0 ⚠️ · 9 ⬜. **[2026-10-26, Block 14.2]** +3 ✅ (10-66 die Regionen — **152/152 = 100 %**; 10-68 die Stabilität — Median **0,0 px**; 10-69 das Budget —
 201 Knoten in **2147 ms**, 0 Frames) ⇒ 61 ✅ · 0 ⚠️ · 10 ⬜. **[2026-10-26, Block 14.1]** +1 ✅ (10-65 der Determinismus — zwei frische Ladevorgänge, **0,0 px** über 152 Knoten, der Beleg byteweise reproduzierbar; der Gegenlauf `seedJitter` → `Math.random()` macht **genau diese** Zelle rot) ⇒ 58 ✅ · 0 ⚠️ · 13 ⬜. **[2026-10-26, Block 14.0]** +7 Zeilen (65–71 — das Kartenlayout; die **Basislinie** ist in `regionen`, `kamera`, `beschriftungen` und `stabilitaet` **rot**, das ist gewollt und gemessen) ⇒ 57 ✅ · 0 ⚠️ · 14 ⬜. **[2026-10-26, Nikinger-Sichtung]** +3 ✅ (10-32 UI-4, 10-37 C2-Stil, 10-51 Editor live) ⇒ 57 ✅ · 0 ⚠️ · 7 ⬜. **[2026-10-25, Block 13]** +3 ✅ (10-62 die Editor-Größen, 10-63 die Knopfleiste nach Word, 10-64 die Knopffarben) ⇒ 54 ✅ · 0 ⚠️ · 10 ⬜. **[2026-10-25, Block 12]** +3 ✅ (10-57 Oversize, 10-58 ROADMAP, 10-59 Register-Bilanz) ⇒ 51 ✅ · 0 ⚠️ · 10 ⬜. **[2026-10-25, Block 11.6]** +2 ✅ (10-54 ED-3 die Format-Konvention, 10-56 die P1-Ankündigung) ⇒ 48 ✅ · 0 ⚠️ · 13 ⬜. **[2026-10-25, Block 11.8]** +2 ✅ (10-52 der Roundtrip, 10-55 der Rohmodus) ⇒ 46 ✅ · 0 ⚠️ · 15 ⬜. **[2026-10-25, Block 11.5]** +1 ✅ (10-53, ED-2 die To-do-Kästchen) ⇒ 44 ✅ · 0 ⚠️ · 17 ⬜. **[2026-10-25, Block 11.7]** +1 ✅ (10-50, das Budget) ⇒ 43 ✅ · 0 ⚠️ · 18 ⬜. **[2026-10-24, Block 10.5]** +4 ✅ (10-45, 10-46, 10-47, 10-48) ⇒ 42 ✅ · 0 ⚠️ · 19 ⬜. **[2026-10-24, Block 9.3]** +2 ✅ (10-43, 10-44) ⇒ 38 ✅ · 0 ⚠️ · 23 ⬜. **[2026-10-24, Block 9.2]** +1 ✅ (10-42, RE-4 `rename_folder`) ⇒ 36 ✅ · 0 ⚠️ · 25 ⬜. **[2026-10-24, Block 9.1]** +1 ✅ (10-41, RE-7 `created_by`) ⇒ 35 ✅ · 0 ⚠️ · 26 ⬜. **[2026-10-24, Block 8]** +4 ✅ (10-36, 10-38, 10-39, 10-40) ⇒ 34 ✅ · 0 ⚠️ · 27 ⬜. **[Stand 2026-10-24, Block 7.5–7.7]** 33, 34 und 35 ✅. **[Korrektur 2026-10-22, Block 6]** Die Zeile stand vorher auf „21 ✅ · 0 ⚠️ · 40 ⬜“ — die Tabelle trug aber **20** ✅ (der Zähler war schon vor diesem Block falsch; Block 5 hat eine Zeile auf ✅ gezogen und die Summe nicht nachgezogen). Neu: **23**, weil Block 6 drei Zeilen (10-23/24/25) auf ✅ gesetzt hat. Ein Wächter prüft die Summe jetzt gegen die Tabelle (`tests/test_head_rules.py`) — **über beide Dateien**, seit die geschlossenen Zeilen im Archiv stehen. **[2026-10-23, Block 7.1]** +1 ✅ (10-29, UI-1) ⇒ 25 ✅ · 0 ⚠️ · 36 ⬜. **[2026-10-23, Block 7.2]** +1 ✅ (10-30, UI-2) ⇒ 26 ✅ · 0 ⚠️ · 35 ⬜. **[2026-10-23, Block 7.3]** +1 ✅ (10-31, UI-3) ⇒ 27 ✅ · 0 ⚠️ · 34 ⬜.

## Offen beim Nikinger

> **[2026-11-07, Closeout Z]** Was hier noch offen ist, steht vollständig und mit Fundstelle im Handover `docs/concepts/PHASE10_5_CLOSEOUT_HANDOVER.md` (§6 Vormerkungen, §8 Entscheidungen); dieser Abschnitt bleibt als Quelle.

- ~~**Vor Deploy D (15.5): Space-Durchsicht**~~ ✅ 2026-10-30 (Claude Code, Nikinger-Auftrag, read-only): **0** Treffer bei 263 Items. **E3** ✅ Nikinger: Titel ≤ **256** Zeichen (15.5c).
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
- ~~**P10.5-18**~~ ✅ 2026-11-03 (Probe 18.5, Zahlen angenommen) — (Deploy A) Live-Messung nach dem Deploy: `/overview` Waiting ≤ 300 ms, Space-Wechsel
  während des Polls ≤ 1 s (beide Eingänge, DevTools). Dazu die drei Live-Checks aus Plan
  §Deploy A: eine Zeile Caddy (V199 bleibt Fleet-Sache) · Handyfoto-Upload (EXIF weg, richtig
  gedreht) · Spaces-Panel direkt nach dem Laden (BG-1).
- ~~**P10.5-27/28**~~ ✅ 2026-11-06 (eurofleet, P10.5-60) — Live-Abnahme P10-J: zwei Modellanbieter, ein Server, ein Werkzeug (`list_spaces`) — Block 6 und Z. **Voraussetzung ist erfüllt:** die Wegwerf-E2E (P10.5-26) zeigt, dass ein Nicht-Claude-Client (`list_spaces` gelingt) — offen ist nur noch der **Live**-Lauf mit zwei Modellanbietern.
- **Handover-Posten (Nikinger 2026-11-03): Green/Blue-Instanz für künftige Entwicklung.** Die Wegwerf-Instanz deckt alles, was der Server selbst entscheidet (Messung, Wächter, Proxy-Verhalten mit lokalem Caddy). **Nicht** deckbar: die **Form der echten Daten** (Fabians Home-Space, graue Knoten — B18 A3 ließ sich nur mit seinen Bildern klären), der echte Funnel/die Domain, `deploy.sh`/`health_gate.sh` gegen den **echten** Dienst und GPU/Firefox/Safari. Vorschlag für P11/Closeout: eine zweite, dauerhaft laufende Instanz (**green**) auf einem eigenen Port mit einer **Kopie** der Daten (nie der echte `DATA_ROOT`/Keyring), die zuerst deployt wird; erst nach Sichtung + `health_gate` schaltet der Symlink/Funnel um (**blue** = bisherige Live-Version bleibt als Rückfall). Der Seam steht seit P5-AC (`SHAREFYX_PORT` in genau einer Variablen, `deploy.sh`). Nicht gebaut — Entscheidung beim Nikinger.
- **NEUER FUND (Nikinger 2026-11-03, „pretty important“): Markdown-Tabellen erscheinen im v4.0-Live-Editor nicht mehr als Tabellen** — im Bild des Nikingers stehen `| Einstellung | Bedeutung |`-Zeilen samt `|---|---|` als Rohtext in Festbreitenschrift, dazwischen hervorgehobene Spans (Code, Fettdruck). **Aus dem Code gelesen, im Browser nicht nachgestellt:** der Tabellen-Renderer lebt in `phase5_ui/webui/static/js/markdown.js` (`<table>`-Ausgabe, GFM-Tabellen seit P5), `editor_cm.js` hat **keinen** Tabellenbezug, und den Vorschau-Schalter (Block 11: „Rohtext“) gibt es seit v4.0 nicht mehr — vermutlich ist damit der einzige Weg zur Tabellendarstellung weggefallen. **Nicht behoben** (Nikinger: als Posten notieren). Vor dem Fix: reproduzieren (Wegwerf-Instanz, Item mit Tabelle), klären, wo `markdownToHtml()` heute noch läuft (Nur-lesen-Ansicht? Item-Vorschau?), und ob der Editor Tabellen als Widget zeigen soll (Stufe 3 / P11) oder ein Vorschau-Weg zurückkommt. **Eigener Befund:** Block 11/13 haben „der Editor zeigt Markdown richtig“ mit dem Roundtrip (10/10) und Bildern der Live-Hervorhebung abgenommen, **nicht** mit einer Tabelle als Sichtkriterium — eine Lücke im Abnahmemaß, kein Einzelfehler.
- **Editor-Plan liegt vor (2026-11-05, Opus 5.5 max, Haiku-Vorarbeit):** `docs/concepts/phase10_5_editor_4_1_plan.md` (+ `…_anhang.md`). **Nikinger entschied:** E1 **geteilt** — `v4.0.2` (S0–S2 + S2R: Render-Probe, Entwurfsschutz-Fehler, Tabellen-Widget mit dem heutigen Renderer; ~4 Sitzungen) **in P10.5 als Block 19**, der Rest (S3a–S11, `v4.1.0`, ~11 Sitzungen) **als P11 Block 1** · E2 marked 18.1.3 vendoren · E3 Budget „nachgeladen“ zwei Zeilen (Editor ≤ 100 KB, Renderer ≤ 20 KB) · E5 Editor-Fließtext Plex Sans 16 px. **Neu aus dem Plan, vor Block 19 zu wissen:** zwei **Live**-Fehler im Entwurfsschutz (Entwurf geht nach Neuladen verloren, wenn zuerst ein anderes Item geöffnet wird; „Wiederherstellen?“ nach einer fremden Änderung setzt die KI-Änderung still zurück = Last-Write-Wins im Client), CRLF normalisiert der **Server** (`read_text`), nicht CM5 (Doku-Fix E6). Offen beim Nikinger: E4, E6–E9, E11, E12 (Plan §8).
- **Befunde aus den Live-Läufen (eurofleet 2026-11-06/07, Notiz §7) — für P11:** (1) `ev=tool` im Serverjournal trägt **keine `client_id`** (nur `ev=http` den User-Agent) — der Beleg nach §3 gelang über `ua`; ein kleiner Logging-Fix (Server, reiner Logtext) wäre sauberer. (2) Das Rezept „`agent.build.tools = {"sharefyx_*": true}`“ aus Plan Block 18 §5.9/Notiz §6 schaltet **alle** Sharefyx-Werkzeuge frei, auch schreibende — gemessen **nicht nötig** (`mcp.sharefyx` allein genügt). (3) **Sicherheits-Hinweis:** seit 2026-11-07 steht `mcp.sharefyx` dauerhaft **lesend und schreibend** in `~/.config/opencode/opencode.json` dieser VM (Nikinger-Entscheidung), das Token (Konto des Nikinger) liegt in `~/.local/share/opencode/mcp-auth.json`; die Agenten von `opencode serve` (Tailnet, Port 4096) können damit in seinem Home-Space schreiben — Hard Rule 4 (fremde Inhalte = Daten, `<untrusted_content>`) bleibt die einzige Schranke gegen Prompt-Injection; zu bedenken: ein eigener, nur lesender Principal für Agenten (Konto, kein Servercode). (4) Ollama nutzt standardmäßig 4096 Token Kontext — ein abgeleitetes Modell mit `num_ctx 16384` ist nötig; `opencode run` liest stdin (`</dev/null`). (5) Trading-VM: Eintrag und Login offen; Traktion-VM bewusst nicht angebunden. (6) **Nikinger 2026-11-07:** Lesezugriff ist gewollt — Sharefyx soll künftig über verschiedene Projekte hinweg genutzt werden; ein nur lesender Agenten-Principal für **Schreib**-Begrenzung bleibt eine offene Idee, keine Entscheidung.
- **Schreibtest der drei Modelle (Nikinger, 2026-11-07; vom Hauptagenten read-only nachgesehen, eurofleets Bericht liegt noch nicht in der Notiz):** drei Items im Home-Space `niklas`, je `version 1`, `created_by niklas`, Tag `p10j-test`, **kein Ordner** (der Prompt verlangte `folder: p10j-test` — in **keinem** Item gesetzt): `[P10-J Test] MiniMax-M3.1-Flash` (09:48Z, saubere GFM-Tabelle mit Leerzeile davor), `[P10-J Test] qwen3-vl:8b-ctx32k` (09:57Z, **Tabelle ohne Leerzeile direkt unter der Textzeile**, Trennzeile `|---…|`), `[P10-J Test] gpt-oss:20b-ctx20k` (15:40Z, saubere Tabelle, keine Schlusszeile). Alle drei Modelle haben also **schreibend** über Sharefyx gearbeitet. Die Modellnamen weichen von der Bitte ab (abgeleitete Modelle mit ctx20k/ctx32k statt 16k). **Erledigt (Nikinger 2026-11-07):** die drei Items angesehen — alle Tabellen erscheinen im Editor als Tabelle, auch die der qwen-Notiz (**P10.5-85 ✅**) — und archiviert. **Korpus-Lücke (P11/S3), bleibt:** keine der 28 Fixtures hat eine Tabelle **direkt unter** einer Textzeile; der Fall funktioniert live im Widget, gehört aber als Fixture in den Korpus (und in die Lesesicht-Prüfung).
- **P11-Vormerkungen des Nikingers (2026-11-06):** (1) **„Nahtloses“ Bearbeiten — eine Tabelle bleibt beim Bearbeiten eine Tabelle** (Zellen direkt im Gitter ändern, kein Umschalten auf Rohtext; heute zeigt das Widget aus `v4.0.2` beim Klick den Quelltext). Folgt aus Plan S6 (Tabellen bearbeiten), ist dort aber noch „im Rohtext“ gedacht — **im P11-Plan neu entscheiden** (Byte-Vertrag V1–V6 gilt weiter: nur die geänderte Zelle ändert Bytes). (2) **Ein „Feedback“-Knopf** in der Web-Oberfläche (Wunsch, noch ohne Entwurf: Wohin geht die Rückmeldung? Server speichert nur — ein Item in einem Feedback-Space oder ein Link, Entscheidung offen; kein LLM, Hard Rule 1: kein Secret im Client).
- **Neuer Posten für P11/Handover: ein wiederkehrender Darstellungs-Check bei jedem Update** (Nikinger 2026-11-03: „somehow worked into a regular healthcheck for future updates“). Vorschlag, nicht gebaut: (a) eine **Render-Probe** an der Wegwerf-Instanz (Playwright, bestehendes Muster `p105_b11_markdown_probe.py`) mit **einem** Fixture-Item, das jedes Markdown-Konstrukt trägt (Tabelle, Liste, To-do-Kästchen, Code, Zitat, Bild, Farb-/Größen-Spans, Überschriften h1–h4) und im DOM von **Editor und Nur-lesen-Ansicht** prüft, dass es als das entsprechende Element erscheint (`<table>`, `<input type=checkbox>` …); sie läuft als **fester Schritt jeder Deploy-Vorbereitung** (Plan §2.5, vor dem Commit) und hat je Konstrukt einen Gegenlauf; (b) leichtgewichtig im `health_gate.sh`: Prüfung, dass die ausgelieferten `markdown.js`/`editor_cm.js` das Konstrukt noch kennen (statisch, ohne Browser). (b) fängt nur Löschungen, (a) die Regression — beides zusammen ist das „Gate“. Ursache der Lücke: die Zeilen 10-50…10-64 messen Größen und Knopfleiste, kein Konstrukt-Katalog.
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

## Session stopped — 2026-11-07 (Closeout Z: Phase 10.5 abgeschlossen — Handover, Grafik, Rotationen; formaler Schluss beim Nikinger)

**Ergebnis.** Abnahme **86 ✅ · 0 ⚠️ · 0 ⬜ von 86** (P10.5-61 ✅, ins Archiv), Register **48 ✅ · 1 ⬜** (AL-1 Zeile 15), live `v4.0.2`. Neu: `docs/concepts/PHASE10_5_CLOSEOUT_HANDOVER.md` (Status, Delta, **Leitziel P11**, alle Vormerkungen mit Fundstelle, Editor-Plan E1–E12, [VERIFY] V207–V219, nächste freie **V220**) und `docs/concepts/phase10_5_finishing_uebersicht.svg` (zweimal gerendert und angesehen). **Nachtrag des Nikingers (2026-11-07), technisch nicht erfüllt:** der Editor soll aussehen wie ein Word-/Writer-Dokument bei Markdown/HTML-Kern — heute Festbreitenschrift, rohe Marker, Kästchen, überlaufende Tabelle. Blöcke 11/13 erfüllten das Maß ihrer Zeit; das Soll war nie Maß. Eine Abnahmezeile dafür ist **seine** Entscheidung und **nicht** gezählt (Handover §2).
**Nachgezogen (Doku ≠ Stand, datiert).** Modulstatus 7/8/11 🔄 → ✅ (Sichtungen 2026-10-26), 19 ✅; Vollzeilen 18/19 verbatim ins Modulstatus-Archiv; Deploy C (nie einzeln, in D) und F (`d2ca573`, 8/9); Register PF-3, PA-7, KA-1, ED-1, UI-4 ⬜ → ✅; README Review-B18 (elf Tools, nicht sechs).
**Formaler Schluss — vorbereitet, Bestätigung des Nikingers:** `ROADMAP.md` P10.5 ✅ und Wurzel-„Current state" (neuer Block, der alte per `scripts/rotate_root_current_state.sh` nach `docs/PROJECT_SESSION_LOG.md`).
**Nächste Session:** P11-Planung (Prompt 2), Einstieg der Handover; erst planen, dann bauen. Vorher beim Nikinger: `health_gate` für F ohne `--require-todays-update-log`.
