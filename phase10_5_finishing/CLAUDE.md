---
status: live
purpose: Phase-10.5-Head — Modulstatus der Blöcke 0–13/Z, Deploy-Tabelle A–D, Abnahmestand P10.5-1–64, offene Punkte beim Nikinger, aktueller Session-Block. Plan und Arbeitsliste stehen in eigenen Dateien.
read-when: Arbeiten in phase10_5_finishing/ — zuerst lesen, zusammen mit dem Session-Block unten
detail: L2
up: ../ROADMAP.md
down:
  - ../docs/concepts/phase10_5_finishing_plan.md    # 📕 der Plan: Locks P10.5-A–W, Blöcke 0–12/Z, Abnahme, [VERIFY] V207–V219
  - ../phase10_inventory/BAUSTELLENREGISTER.md      # 📗 die Arbeitsliste — hier wird abgehakt (P10-B)
  - ../phase10_inventory/ENTSCHEIDUNGEN_ARCHIVE.md  # 📦 §12 Entscheidungsliste D-1–D-18, verbatim
  - SESSIONS_ARCHIVE.md                             # 📦 ältere Session-Blöcke, verbatim, newest-first
  - UPDATES_ARCHIVE.md                              # 📦 die älteren `updated:`-Fäden dieses Heads, verbatim
  - STARTUPTRAG_ARCHIVE.md                          # 📦 die Startaufträge der Blöcke 7 und 9, verbatim
  - MODULSTATUS_ARCHIVE.md                         # 📦 die ausführlichen Statusspalten der Blöcke 0–10 und 11–17, verbatim
  - ABNAHME_ARCHIVE.md                             # 📦 die geschlossenen Abnahmezeilen (P10.5-1–72), verbatim
  - FREIGABEN_ARCHIVE.md                           # 📦 die Freigaben der Phase, verbatim
updated: 2026-11-02 (Block 18.2b/18.3 gebaut: Mindestdistanz, Zwischenspeicher, V3/V4; nächste Session: 18.5, 18.4) | 2026-11-02 (Block 18.1/18.2 gebaut: Stern, MAX_SPEED; offen: Strichelung, Ausreißer-Zelle) | 2026-11-01 (Block 18.0 gemessen: Kosten = Kantenzeichnen, N1 Schleuder-Fund; STOPP vor 18.1/18.2) | 2026-11-01 (Live-Sichtung: Film ✅; Block 18 geplant) | ältere Einträge: phase10_5_finishing/UPDATES_ARCHIVE.md
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
| 11 | Editor Stufe 1 + 2: ED-1, ED-2, ED-3 (P1-11), ED-5 | Ausführer (+ Claude Code Proben/Sichtung) | D | 🔄 2026-10-24 |
| 12 | Doku und Altlasten: DO-1, LG-6, AL-1 (Rest), AL-3, BG-2/BG-3 | Claude Code | — | ✅ 2026-10-25 |
| 13 | Aufträge des Nikingers: UI-8 (die Größen wirken live), UI-9 (die Knopfleiste nach Word), UI-10 (die Knopffarben) | Claude Code (Sichtung Nikinger) | D | ✅ 2026-10-25 |
| 14 | Kartenlayout „zufällig, aber geordnet“ (Nikinger 2026-10-26) — Plan `docs/concepts/phase10_5_block14_kartenlayout_plan.md` | Ausführer (opencode) + Claude Code (Bilder) | D | ✅ 2026-10-29 (Sichtung P10.5-70 abgenommen) |
| 15 | Fixes aus dem Ultra-Review B1–B10 — Plan `docs/concepts/phase10_5_block15_review_fixes_plan.md` | Claude Code | D | ✅ 2026-10-31 |
| 16 | Launch-Film v4.0.0 (Nikinger 2026-10-29/31) — Plan `docs/concepts/phase10_5_launch_film_plan.md` | Claude Code (Sichtung Nikinger) | vor D | ✅ 2026-11-01 |
| 17 | Film in die App (Nikinger 2026-11-01) — Plan `docs/concepts/phase10_5_block17_film_app_plan.md` | Claude Code | D | ✅ 2026-11-01 |
| 18 | Live-Funde nach D: Karte träge (Tags/Ordner), Ausreißer, Editor-Farben — Plan `docs/concepts/phase10_5_block18_live_fixes_plan.md` | eigene Session | v4.0.1 | ✅ live 2026-11-03 (`v4.0.1`) — **18.0–18.3 ✅** (Stern, `MAX_SPEED`, Mindestdistanz, Zwischenspeicher, V3/V4: „beide an“ Ruhe/Pan **2,3 ms** (309), Einschwingen **1,6 s** (55 s), je Regel ein Gegenlauf; P10.5-80–83 ✅; 18/49 ✅ nach der Annahme) · **18.5 ✅** `probes/p105_b18_live_zeilen_probe.py` (P10.5-18/49, beide Eingänge, Caddy 2.6.2, Gegenläufe `poll`/`stream`; Sichtung beim Nikinger) · **18.4 ✅** deployt (Deploy E), `health_gate` 9/9 · **Live-Schritte ✅** (Schalter aus/an: kein Einzelpunkt, Fabians Cluster sitzt im Körper) · **A1:** live nicht zu beobachten (Nikinger), Zelle `ausreisser` bleibt in der Wegwerf-Saat rot, kein Code — Plan §5.7–§6 |
| 19 | Editor v4.0.2 — Hotfix aus dem Editor-Plan (S0 Render-Probe, S1 Entwurfsschutz, S2 Tabellen-Widget; Plan `docs/concepts/phase10_5_editor_4_1_plan.md`) | Claude Code | F | 🔄 2026-11-05 — **S0 ✅** (Probe `probes/p105_ed41_darstellung_probe.py` + 28 Fixtures `fixtures_ed41/` mit SHA-Manifest: Basislinie Chromium **und** Firefox je **30 von 57 Zellen rot**, 0 Abweichungen; Selbsttest: 3 Gegenläufe, je nur die eigenen Zellen; Wächter `tests/test_ed41_probe.py` 23) · **S1 ✅ (2026-11-06)** Entwurfsschutz: Entwurf `{…, version, gespeichert}`, nur bei Nutzeränderung, vor `setBody` gelesen, veralteter Entwurf ⇒ Konfliktdialog statt stillem Zurücksetzen (Hard Rule 3); drei Zellen grün (Chromium + Firefox, 30 → 27 rot), Gegenläufe `s1_ohne_ursprung`/`s1_ohne_version` je nur ihre Zelle · **S2 ✅ (2026-11-06)** Tabellen-Widget (`js/editor/tabellen.js`, nur per `import()`, Cursor außerhalb ⇒ Tabelle aus demselben Renderer, Klick → Zelle, Pfeile → erste/letzte Zeile, Undo, Kopieren = Quelle, Bytes gleich; Rückfall = Rohtext): acht Zellen grün, rot 27 → 26 (Chromium + Firefox, vom Hauptagenten neu gefahren), Tastenkosten Basis + ~1 ms, Budget grün (nachgeladen 74,0 von 80 KB), Suite 1939 grün · **nächster Schritt S2R** (Release `v4.0.2`) · Nikinger: E4 ✅ |
| Z | Closeout P10.5 (Handover, Grafik, Rotationen) | Claude Code + Nikinger | — | ⬜ |

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
| C | `v3.1.7` | — | — | nach Block 7–8 — **2026-10-24 vorbereitet** (Badge, eigener `## 2026-10-24`-Block im Update-Log, Suite 1425 grün, `doc_health` 0, `ui_budget` 5/5), **`deploy.sh` beim Nikinger** |
| D | `v4.0.0` (vorher `v3.1.8`; Nikinger 2026-10-26) | `2eb697f` | **9/9 OK** | **live seit 2026-11-01**, Release `20261101T172738.984499Z` (Release-Tests 1842 grün; Deploy beim Nikinger; enthält C) · nach Block 9–11 **+ 13** + Nachzug 2026-10-26 (**enthält RE-4 `rename_folder` und RE-3 `rename_space`**) (die UI-Änderungen aus Block 13 fahren mit) · **+ Block 14.7** (Karte kompakt/verteilt/glatt, 2026-10-29 geplant) · **+ Block 15** (Review-Fixes B1–B10 inkl. B1 — **kein** Hotfix vorab, Nikinger 2026-10-30: Deploy nach allen Fixes, Wochenende) · **+ Block 17** (Film in der App, ✅ 2026-11-01) · Update-Log `## 2026-11-01` · **`deploy.sh` + `health_gate.sh` beim Nikinger** |
| E | `v4.0.1` | `0e317cf` | **9/9 OK** | **live seit 2026-11-03**, Release `20261103T064426.832031Z` (Release-Tests 1862 grün; Deploy beim Nikinger) · Block 18: Karte flüssig (Stern, Mindestdistanz, Zwischenspeicher), Update-Log `## 2026-11-03` · Nikinger live: „Layout zurücksetzen“ mehrfach — das Bild bleibt gut; Gefühl **flüssig** bestätigt (Bild mit beiden Schaltern, kein Einzelpunkt weit draußen) |

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
| P10.5-27 | **Live P10-J Lauf 1** (M3.1 Flash) — **eurofleet** | ⬜ | Generalprobe an der Wegwerf-Instanz **grün** (2026-11-03, `probes/p105_p10j_lauf1_wegwerf.py`: das Modell ruft `list_spaces` selbst, Server `ev=tool ok=true`; Gegenlauf `--skip-auth` rot) — **Live-Lauf jetzt bei eurofleet** (Nikinger 2026-11-03), Rezept `docs/concepts/phase10_5_p10j_lauf2_eurofleet.md` §6 + Plan Block 18 §5.9 |
| P10.5-28 | **Live P10-J Lauf 2** (lokales Modell, CT 111) — mit 27 die Abschlussbedingung der Phase | ⬜ | eurofleet, Notiz `docs/concepts/phase10_5_p10j_lauf2_eurofleet.md` |
| P10.5-60 | P10-J zweimal live belegt | ⬜ | — |
| P10.5-61 | Closeout-Dokumente + Rotationen per Skript | ⬜ | — |

**Summe:** 79 ✅ · 0 ⚠️ · 4 ⬜ (von 83). **[2026-11-03, live v4.0.1]** +2 ✅ (10-18 `/overview` Waiting und Space-Wechsel, 10-49 Ereignisse über beide Eingänge — Wegwerf-Probe 18.5, Zahlen vom Nikinger angenommen) ⇒ 79 ✅ · 0 ⚠️ · 4 ⬜. **[2026-11-03, Sichtung]** +1 ✅ (10-83 V3/V4, Bild vom Nikinger gesichtet) ⇒ 77 ✅ · 0 ⚠️ · 6 ⬜. **[2026-11-02, Block 18]** +3 ✅ (10-80 Stern, 10-81 Mindestdistanz/`insel`, 10-82 Zwischenspeicher) und +1 Zeile (10-83 V3/V4, Sichtung) ⇒ 76 ✅ · 0 ⚠️ · 7 ⬜. **[2026-11-01, live]** +1 ✅ (10-22 Connector, `proto` 2026-07-28) ⇒ 73 ✅ · 0 ⚠️ · 6 ⬜. **[2026-10-31, Block 15.7]** +1 ✅ (10-79 B6/B7/B9/B10) ⇒ 72 ✅ · 0 ⚠️ · 7 ⬜. **[2026-10-30, Block 15.4]** +1 ✅ (10-78 B4 Mitglieder) ⇒ 71 ✅ · 0 ⚠️ · 8 ⬜. **[2026-10-30, Block 15.3]** +1 ✅ (10-77 B5/B8 Typen) ⇒ 70 ✅ · 0 ⚠️ · 9 ⬜. **[2026-10-30, Block 15.2]** +1 ✅ (10-76 B2/B3/B20 Dienststart) ⇒ 69 ✅ · 0 ⚠️ · 10 ⬜. **[2026-10-30, Block 15.1]** +1 ✅ (10-75 B1/B15 `asset_id`) und +4 Zeilen (76–79, Plan Block 15 §4) ⇒ 68 ✅ · 0 ⚠️ · 11 ⬜. **[2026-10-29, Sichtung]** +1 ✅ (10-70 die drei Kartenbilder von Block 14.7, vom Nikinger abgenommen) ⇒ 67 ✅ · 0 ⚠️ · 7 ⬜. **[2026-10-29, Block 14.7.5]** +2 ✅ (10-73 kompakt und verteilt — Solidität 0,830, NN 35,95 px; 10-74 glatt — Zusatzkrümmung 1,86) ⇒ 66 ✅ · 0 ⚠️ · 8 ⬜. **[2026-10-29, Block 14.7.0]** +2 Zeilen (73/74 — Form und Kontur der Karte, Plan `docs/concepts/phase10_5_block14_7_plan.md` §5; die Basislinie ist rot, das ist der Befund) ⇒ 64 ✅ · 0 ⚠️ · 10 ⬜. **[2026-10-28, Block 14.6.3]** +1 ✅ (10-72 der **Körper** — die Körpermaske aller Spaces ist **eine** Komponente (6274 Zellen), jeder Space hat **genau einen** Lappen, **146** Furche-Zellen, **4** Paare, Reach **47,9 / 44,1 / 48,4 / 44,6 px**, Luft **7,2 / 10,7 / 82,9 / 85,6 px**, `computeLobes()` **30,8 ms** (152) · **34,6 ms** (201 Knoten) — der Gegenlauf `koerper` macht **genau diese** Zelle rot) ⇒ 64 ✅ · 0 ⚠️ · 8 ⬜. **[2026-10-27, Block 14.35]** +1 ✅ (10-71 die Beschriftungen — **0** überlappende Paare (der Stand 14.3 zählte **4** per Pixelvergleich — der Recorder zählt dieselbe Szene mit **5**), **3** von **13** Beschriftungen weggelassen, die Fokus-Beschriftung am Pixel nachgewiesen da; der Gegenlauf `beschriftung` macht **genau diese** Zelle rot) ⇒ 63 ✅ · 0 ⚠️ · 8 ⬜. **[2026-10-26, Block 14.3]** +1 ✅ (10-67 die Kamera — Füllgrad **93,6 %**, der Inhalt passt, der Umriss sitzt **0,42 px** neben der Mitte statt 32,3 px) ⇒ 62 ✅ · 0 ⚠️ · 9 ⬜. **[2026-10-26, Block 14.2]** +3 ✅ (10-66 die Regionen — **152/152 = 100 %**; 10-68 die Stabilität — Median **0,0 px**; 10-69 das Budget —
 201 Knoten in **2147 ms**, 0 Frames) ⇒ 61 ✅ · 0 ⚠️ · 10 ⬜. **[2026-10-26, Block 14.1]** +1 ✅ (10-65 der Determinismus — zwei frische Ladevorgänge, **0,0 px** über 152 Knoten, der Beleg byteweise reproduzierbar; der Gegenlauf `seedJitter` → `Math.random()` macht **genau diese** Zelle rot) ⇒ 58 ✅ · 0 ⚠️ · 13 ⬜. **[2026-10-26, Block 14.0]** +7 Zeilen (65–71 — das Kartenlayout; die **Basislinie** ist in `regionen`, `kamera`, `beschriftungen` und `stabilitaet` **rot**, das ist gewollt und gemessen) ⇒ 57 ✅ · 0 ⚠️ · 14 ⬜. **[2026-10-26, Nikinger-Sichtung]** +3 ✅ (10-32 UI-4, 10-37 C2-Stil, 10-51 Editor live) ⇒ 57 ✅ · 0 ⚠️ · 7 ⬜. **[2026-10-25, Block 13]** +3 ✅ (10-62 die Editor-Größen, 10-63 die Knopfleiste nach Word, 10-64 die Knopffarben) ⇒ 54 ✅ · 0 ⚠️ · 10 ⬜. **[2026-10-25, Block 12]** +3 ✅ (10-57 Oversize, 10-58 ROADMAP, 10-59 Register-Bilanz) ⇒ 51 ✅ · 0 ⚠️ · 10 ⬜. **[2026-10-25, Block 11.6]** +2 ✅ (10-54 ED-3 die Format-Konvention, 10-56 die P1-Ankündigung) ⇒ 48 ✅ · 0 ⚠️ · 13 ⬜. **[2026-10-25, Block 11.8]** +2 ✅ (10-52 der Roundtrip, 10-55 der Rohmodus) ⇒ 46 ✅ · 0 ⚠️ · 15 ⬜. **[2026-10-25, Block 11.5]** +1 ✅ (10-53, ED-2 die To-do-Kästchen) ⇒ 44 ✅ · 0 ⚠️ · 17 ⬜. **[2026-10-25, Block 11.7]** +1 ✅ (10-50, das Budget) ⇒ 43 ✅ · 0 ⚠️ · 18 ⬜. **[2026-10-24, Block 10.5]** +4 ✅ (10-45, 10-46, 10-47, 10-48) ⇒ 42 ✅ · 0 ⚠️ · 19 ⬜. **[2026-10-24, Block 9.3]** +2 ✅ (10-43, 10-44) ⇒ 38 ✅ · 0 ⚠️ · 23 ⬜. **[2026-10-24, Block 9.2]** +1 ✅ (10-42, RE-4 `rename_folder`) ⇒ 36 ✅ · 0 ⚠️ · 25 ⬜. **[2026-10-24, Block 9.1]** +1 ✅ (10-41, RE-7 `created_by`) ⇒ 35 ✅ · 0 ⚠️ · 26 ⬜. **[2026-10-24, Block 8]** +4 ✅ (10-36, 10-38, 10-39, 10-40) ⇒ 34 ✅ · 0 ⚠️ · 27 ⬜. **[Stand 2026-10-24, Block 7.5–7.7]** 33, 34 und 35 ✅. **[Korrektur 2026-10-22, Block 6]** Die Zeile stand vorher auf „21 ✅ · 0 ⚠️ · 40 ⬜“ — die Tabelle trug aber **20** ✅ (der Zähler war schon vor diesem Block falsch; Block 5 hat eine Zeile auf ✅ gezogen und die Summe nicht nachgezogen). Neu: **23**, weil Block 6 drei Zeilen (10-23/24/25) auf ✅ gesetzt hat. Ein Wächter prüft die Summe jetzt gegen die Tabelle (`tests/test_head_rules.py`) — **über beide Dateien**, seit die geschlossenen Zeilen im Archiv stehen. **[2026-10-23, Block 7.1]** +1 ✅ (10-29, UI-1) ⇒ 25 ✅ · 0 ⚠️ · 36 ⬜. **[2026-10-23, Block 7.2]** +1 ✅ (10-30, UI-2) ⇒ 26 ✅ · 0 ⚠️ · 35 ⬜. **[2026-10-23, Block 7.3]** +1 ✅ (10-31, UI-3) ⇒ 27 ✅ · 0 ⚠️ · 34 ⬜.

## Offen beim Nikinger

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
- **P10.5-18** (Deploy A) — Live-Messung nach dem Deploy: `/overview` Waiting ≤ 300 ms, Space-Wechsel
  während des Polls ≤ 1 s (beide Eingänge, DevTools). Dazu die drei Live-Checks aus Plan
  §Deploy A: eine Zeile Caddy (V199 bleibt Fleet-Sache) · Handyfoto-Upload (EXIF weg, richtig
  gedreht) · Spaces-Panel direkt nach dem Laden (BG-1).
- **P10.5-27/28** — Live-Abnahme P10-J: zwei Modellanbieter, ein Server, ein Werkzeug (`list_spaces`) — Block 6 und Z. **Voraussetzung ist erfüllt:** die Wegwerf-E2E (P10.5-26) zeigt, dass ein Nicht-Claude-Client (`list_spaces` gelingt) — offen ist nur noch der **Live**-Lauf mit zwei Modellanbietern.
- **Handover-Posten (Nikinger 2026-11-03): Green/Blue-Instanz für künftige Entwicklung.** Die Wegwerf-Instanz deckt alles, was der Server selbst entscheidet (Messung, Wächter, Proxy-Verhalten mit lokalem Caddy). **Nicht** deckbar: die **Form der echten Daten** (Fabians Home-Space, graue Knoten — B18 A3 ließ sich nur mit seinen Bildern klären), der echte Funnel/die Domain, `deploy.sh`/`health_gate.sh` gegen den **echten** Dienst und GPU/Firefox/Safari. Vorschlag für P11/Closeout: eine zweite, dauerhaft laufende Instanz (**green**) auf einem eigenen Port mit einer **Kopie** der Daten (nie der echte `DATA_ROOT`/Keyring), die zuerst deployt wird; erst nach Sichtung + `health_gate` schaltet der Symlink/Funnel um (**blue** = bisherige Live-Version bleibt als Rückfall). Der Seam steht seit P5-AC (`SHAREFYX_PORT` in genau einer Variablen, `deploy.sh`). Nicht gebaut — Entscheidung beim Nikinger.
- **NEUER FUND (Nikinger 2026-11-03, „pretty important“): Markdown-Tabellen erscheinen im v4.0-Live-Editor nicht mehr als Tabellen** — im Bild des Nikingers stehen `| Einstellung | Bedeutung |`-Zeilen samt `|---|---|` als Rohtext in Festbreitenschrift, dazwischen hervorgehobene Spans (Code, Fettdruck). **Aus dem Code gelesen, im Browser nicht nachgestellt:** der Tabellen-Renderer lebt in `phase5_ui/webui/static/js/markdown.js` (`<table>`-Ausgabe, GFM-Tabellen seit P5), `editor_cm.js` hat **keinen** Tabellenbezug, und den Vorschau-Schalter (Block 11: „Rohtext“) gibt es seit v4.0 nicht mehr — vermutlich ist damit der einzige Weg zur Tabellendarstellung weggefallen. **Nicht behoben** (Nikinger: als Posten notieren). Vor dem Fix: reproduzieren (Wegwerf-Instanz, Item mit Tabelle), klären, wo `markdownToHtml()` heute noch läuft (Nur-lesen-Ansicht? Item-Vorschau?), und ob der Editor Tabellen als Widget zeigen soll (Stufe 3 / P11) oder ein Vorschau-Weg zurückkommt. **Eigener Befund:** Block 11/13 haben „der Editor zeigt Markdown richtig“ mit dem Roundtrip (10/10) und Bildern der Live-Hervorhebung abgenommen, **nicht** mit einer Tabelle als Sichtkriterium — eine Lücke im Abnahmemaß, kein Einzelfehler.
- **Editor-Plan liegt vor (2026-11-05, Opus 5.5 max, Haiku-Vorarbeit):** `docs/concepts/phase10_5_editor_4_1_plan.md` (+ `…_anhang.md`). **Nikinger entschied:** E1 **geteilt** — `v4.0.2` (S0–S2 + S2R: Render-Probe, Entwurfsschutz-Fehler, Tabellen-Widget mit dem heutigen Renderer; ~4 Sitzungen) **in P10.5 als Block 19**, der Rest (S3a–S11, `v4.1.0`, ~11 Sitzungen) **als P11 Block 1** · E2 marked 18.1.3 vendoren · E3 Budget „nachgeladen“ zwei Zeilen (Editor ≤ 100 KB, Renderer ≤ 20 KB) · E5 Editor-Fließtext Plex Sans 16 px. **Neu aus dem Plan, vor Block 19 zu wissen:** zwei **Live**-Fehler im Entwurfsschutz (Entwurf geht nach Neuladen verloren, wenn zuerst ein anderes Item geöffnet wird; „Wiederherstellen?“ nach einer fremden Änderung setzt die KI-Änderung still zurück = Last-Write-Wins im Client), CRLF normalisiert der **Server** (`read_text`), nicht CM5 (Doku-Fix E6). Offen beim Nikinger: E4, E6–E9, E11, E12 (Plan §8).
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

## Session stopped — 2026-11-06 (Block 19, S2: Tabellen-Widget — gebaut, Suite 1939 grün)

**Ergebnis.** **S2 ✅** (Opus-Ausführer, nach einem zweiten Rate-Limit-Abbruch aus dem Transkript fortgesetzt; Diff gelesen, Probe von mir neu gefahren). Eigene Notizen zeigen **Tabellen wieder als Tabelle**: `js/editor/tabellen.js` (nur per `import()`, Rückfall bei Ladefehler = Rohtext) ersetzt eine GFM-Tabelle per `markText`, wenn Cursor/Auswahl **außerhalb** stehen — mit **demselben** `markdownToHtml()` wie die Lesesicht; Klick in eine Zelle ⇒ Rohtext mit dem Cursor in genau dieser Zelle; Pfeil ↓/↑ ⇒ erste/letzte Zeile; Undo, Kopieren = Quelltext. Das Widget ist nur eine **Sicht**: Öffnen, Anzeigen, Ausblenden und Speichern ohne Änderung lassen die Bytes gleich (`bytes_gleich`, `bytes_zelle` grün). Geändert: `editor.js` (+11), `app.css` (+15), `ui_budget.py` (+4).
**Messung** (Chromium 151, Firefox 153): acht S2-Zellen grün, rot **27 → 26**, 0 Abweichungen, 0 Seitenfehler; Gegenläufe `s2_ohne_installation`, `s2_ohne_eintritt`, `s2_ohne_klickziel`, `s2_polstert` je nur ihre Zellen; Tastenkosten Chromium 2,3–2,8 ms / Firefox 3 ms (Basis 1,6–2,2 / 2–3), `ui_budget` grün (Erstaufruf 238,1 von 250 KB, nachgeladen 74,0 von 80 KB — Plan sieht 100 vor, wird mit S3 angehoben), Suite **1939 grün**.
**Bekannte Lücken, die v4.0.2 noch zeigt (Renderer, S3/E4):** `<br>` in Zellen erscheint als Text, maskierter Strich `\|` teilt falsch, Tabellen in Zitat/`:::` bleiben Rohtext, `~~~` wird behandelt wie der Renderer es tut. Plan-Anhang A15 (Korrekturen, Entscheidungen, Flake der S1-Zelle).
**Ehrlich offen:** Rohmodus im Browser (nur Wächter), WebKit, IME, Touch, Umschalt+Pfeil in ein Widget.
**Nächste Session:** S2R — Update-Log (Datum = Deploy-Tag), Badge `v4.0.2`, Suite, `doc_health`, `ui_budget`, Probe; Deploy + `health_gate` **durch den Nikinger**; live eine echte Notiz mit Tabelle öffnen.

