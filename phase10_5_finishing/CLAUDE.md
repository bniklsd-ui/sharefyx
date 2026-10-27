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
  - MODULSTATUS_ARCHIVE.md                         # 📦 die ausführlichen Statusspalten der Blöcke 0–10, verbatim
  - ABNAHME_ARCHIVE.md                             # 📦 die geschlossenen Abnahmezeilen (P10.5-1–71), verbatim
  - FREIGABEN_ARCHIVE.md                           # 📦 die Freigaben der Phase, verbatim
updated: 2026-10-27 (Block 14.35: die Beschriftungen ohne Überlappung — 0 überlappende Paare, 3 von 13 weggelassen, der Fokus bleibt; P10.5-71 ✅) | 2026-10-26 (Block 14.3: die Kamera — `fitView()`; Füllgrad 93,6 %, Versatz 0,42 px; E3: `ZOOM_MIN` bleibt 0,5; P10.5-67 ✅) | 2026-10-26 (Block 14.2: die L4 — Anker-Gravitation, Querfedern, `ALPHA_START_SEEDED`; Regionen 152/152, Stabilität Median 0,0 px, Budget 201 Knoten/2147 ms; P10.5-66/68/69 ✅) | 2026-10-26 (Block 14.1: L1–L3 — der Seed wird zum Weltgenerator; fünf Seed-Zellen grün, fünf Gegenläufe rot an genau ihrer Zelle; P10.5-65 geschlossen) | 2026-10-26 (Block 14.0: die Basislinie des Kartenlayouts — die Probe steht, die Abnahmezeilen 65–71 sind im Head; rot in Regionen/Kamera/Beschriftungen/Stabilität, grün in Determinismus/Budget; B5 widerlegt) | 2026-10-25 (Block 13: die vier Aufträge des Nikingers gebaut — Editor-Größen live, Knopfleiste nach Word, Knopffarben transparent-blau, ganze Gehirnkarte; P10.5-62/63/64 ✅, 54 ✅ · 10 ⬜) | 2026-10-25 (Block 12: Doku und Altlasten — DO-1, LG-6, AL-1/AL-3, BG-2/BG-3, Register-Bilanz per Skript; P10.5-57/58/59 ✅, 51 ✅ · 10 ⬜) | ältere Einträge: phase10_5_finishing/UPDATES_ARCHIVE.md
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
| 11 | Editor Stufe 1 + 2: ED-1, ED-2, ED-3 (P1-11), ED-5 | Ausführer (+ Claude Code Proben/Sichtung) | D | 🔄 2026-10-24 — **11.1 Vendor** (CodeMirror 5.65.16, **fünf** Dateien statt drei — gemessen: der UMD-Browser-Zweig der `markdown.min.js` löst `require("../xml/xml")` **nicht** auf) · **11.2 Nachlader** (`js/editor_cm.js`: CSS → Kern → Modus-Dateien, Promise gecacht, Fehler → `null` = Textarea/Rohmodus) · **11.3 Live-Editor** (`editor.js`: `getBody()`/`setBody()`, `setRawMode(on)`, Schalter „Rohtext", Probe 12/12 grün) · **11.4 Live-Darstellung** (V211 **gemessen**: `visibility: hidden` hält die Cursorposition, `display: none`/`font-size: 0` rücken sie 2 Zeichen vor; Probe 15/15 grün) · **11.5 To-do-Kästchen** (ED-2: `cm.markText(…, {replacedWith: <checkbox>, atomic: true})` — der **Text** bleibt die Quelle; Klick bei sauberem Editor speichert **sofort** mit `version`, bei geändertem nur der Puffer; Lesesicht **deaktiviert**; Probe 8/8 grün, Gegenlauf bricht genau die Schreibzelle) · **11.7 Budget** (`ui_budget.py`: `static_payload_files()` — **jede Datei genau einmal**; Erstaufruf **209,3 KB** ≤ 250 KB, Editor **69,7 KB** ≤ 80 KB; Wächter `tests/test_budget_coverage.py` mit Gegenprobe) · **11.8 Roundtrip** (V201-Rest: die **zehn** M7-Fixtures **10/10 byte-identisch**, Öffnen macht den Editor **nicht** geändert, Dateien auf der Platte byte-identisch) · **11.6 Format-Konvention** (ED-3: `markdown.js` — Vokabular **Farbe** (rot/blau/gruen/gelb) · **Größe** (klein/normal/gross) · **Ausrichtung** (links/zentriert/rechts); Inline `[Text]{.rot}`, Block `::: {.zentriert}` … `:::`; eine **unbekannte** Klasse bleibt **wörtlich**; der Sanitizer lässt `span`/`div` nur mit Klassen aus der festen Menge durch; die **Codespans** sind ausgeschnitten (darin wird **nichts** formatiert — das behebt einen Alt-Fehler); Editor: drei Felder in der Werkzeugleiste + ein **CM5-Overlay**, das `[…]{.rot}` schon beim Schreiben färbt; MCP: `_FORMAT_HINT` **wörtlich identisch** an allen fünf Body-Schreib-Werkzeugen; Probe `probes/p105_b11_markdown_probe.py`: **9/9 Zellen grün**, der Gegenlauf bricht genau die Zelle „unbekannte Klasse wörtlich“) |
| 12 | Doku und Altlasten: DO-1, LG-6, AL-1 (Rest), AL-3, BG-2/BG-3 | Claude Code | — | ✅ 2026-10-25 — **DO-1** (die drei Heads: 8.6 109.230 → 23.614 B, 8 47.861 → 34.225 B, 6 41.032 → 34.801 B; verbatim per `move_sections.py`, die 33-KB-Kette von 8.6 per Skript in `UPDATES_ARCHIVE.md`) · **LG-6** (`ROADMAP.md` 37.197 → 26.457 B, Phase 8.5 → `docs/ROADMAP_ARCHIVE.md`) · **AL-1/AL-3** (P6-Nachzug in `phase6_shares/CLAUDE.md`) · **BG-2/BG-3** (P9-124/127 ⚠️ → ✅, Bilanz 123/10/1) · **Register-Bilanz** per `scripts/register_bilanz.py` (46 P10.5-Zeilen: 40 ✅ · 6 ⬜) |
| 13 | Aufträge des Nikingers: UI-8 (die Größen wirken live), UI-9 (die Knopfleiste nach Word), UI-10 (die Knopffarben) | Claude Code (Sichtung Nikinger) | D | ✅ 2026-10-25 — **13.1** (die Stufen wirken im **Live-Editor**: Basis 13 px, `klein` 11,05 px, `normal` 13 px, `groß` 15,6 px; die **Zeilenhöhe bleibt 21 px** in allen drei Stufen — die Ursache war die Prozent-`line-height`: CM5 rechnet `defaultTextHeight` **einmal** (aus 50 Zeilen); der Overlay liefert Farbe **und** Größe in beliebiger Reihenfolge) · **13.2** (die Leiste: **fünf** Gruppen in Words Ribbon-Reihenfolge, alle Knöpfe 26 × 24 px, Trenner dazwischen, **keine** HTML-Entity-Zeichen als Icons; **B** und **I** bleiben Buchstaben; die fünf neuen Icons aus dem Lucide-Tarball **1.38.0**, SHA-256 **verifiziert**) · **13.3** (die Fläche: `--btn-std-fill` = `rgba(62,141,243,.20)` — die **datierte Umkehr** der P9-Entscheidung vom 2026-10-01; `--caution` `#F06A6E` → **`#FF8A8E`**, Kontrast **nachgerechnet**: 4,76:1 statt 3,59:1) · **13.4** (die **ganze** Karte: 1920 × 1200, Zoom 50 % — die Welt der Knoten vollständig im Bild) · Probe `probes/p105_b13_knopfleiste_probe.py` **8/8 grün**, der Gegenlauf **5 Zellen rot**; Wächter `tests/test_knopfleiste_word.py` (9) und `tests/test_contrast.py` (3) grün · **Fund:** `i-chevron-left` stand im Sprite, die Quelldatei war **nie** vendored — der Sprite war damit nicht aus dem Bestand reproduzierbar; nachgetragen und **alle 25** vendored Dateien byteweise gegen den Tarball geprüft |
| 14 | Kartenlayout „zufällig, aber geordnet“ (Nikinger 2026-10-26) — Plan `docs/concepts/phase10_5_block14_kartenlayout_plan.md` | Ausführer (opencode) + Claude Code (Bilder) | D | 🔄 2026-10-27 — **14.0 (Basislinie) ✅**: die Probe `probes/p105_b14_layout_probe.py` steht (Wegwerf auf **TLS**, freier Port je Lauf, eigener Datenbaum und eigene `auth.sqlite3` je Lauf, Stopp nur über die PID-Datei; 5 Spaces, 152 Items, **IDs und Uhr eingefroren** — auch **im Server**, sonst war die Basislinie laufverschieden) und misst **gegen den heutigen Code**: **rot** in `regionen` (**57,2 %** statt 95 %), `kamera` (der Umriss sitzt **43,8 px** neben der Mitte, Unsicherheit **0,65 px**), `beschriftungen` (**5** überlappende Paare) und `stabilitaet` (Median **327,9 px**; das neue Item **164,2 px** von seinem Space, **118,4 px** von einem fremden); **grün** in `determinismus` (**0,0 px** über 152 Knoten) und `budget` (**201** Knoten, **2,53 s**, **0** Frames bei reduced motion, die Karte ist gemalt) · **sechs Befunde an der Messung selbst** (im Plan §0/§5 datiert nachgezogen): der Canvas-Hash taugt **nicht** als Ruhe-Signal (die Karte wird zuerst zweimal unverändert gezeichnet → „Ruhe“ vor dem ersten Tick), `store.search()` sortiert nach `updated` (die Wanduhr macht die Knoten-Reihenfolge und damit den Saat-Ring laufverschieden), die **serverseitig** erzeugten Items trugen **zufällige IDs** und **Wanduhr-Zeitstempel** (der Saat-Jitter ist ein Hash der ID — die Karte war zwischen zwei Läufen eine andere), und **B5 ist widerlegt** (die Karte passt bei 100 % und füllt 68,5 %; die 16 Radschritte des B15-Skripts fuhren auf `ZOOM_MIN` und verkleinerten sie) · **vier Falsch-Grün-Pfade geschlossen** (Advisor-Runde): die Beschriftungs-Zelle war grün, wenn die App nur die Fokus-Beschriftung zeichnet; die Determinismus-Zelle zählte die gemeinsamen Knoten nicht; die Ruhe-Messung trennte den Burst bei *jedem* Abstand > 300 ms (eine Lastspitze hätte die Budget-Zelle grün gemacht); ein Seitenfehler im Graph-Code machte keine Zelle rot · **Wächter** `tests/test_b14_layout_probe.py` (7 Tests: die Zellen-Zuordnung, die **Zahlen** hinter den Zellen, drei Gegenproben — darunter eine, die **dieselbe** Testfunktion mit untergeschobenem Beleg aufruft) · Suite **1590** grün · **14.1 (L1–L3) ✅ 2026-10-26**: `hashString()` (FNV-1a als Zahl, aus `seedJitter()` herausgezogen — **bitidentisch**, der C2-Wächter hängt an genau diesem Hash), `computeRegions()` (**rein, ohne DOM**: eine Region je Space → Ordner-Inseln → Item-Spirale) und der neue `seedInitialPositions()`; **gemessen wird der Seed jetzt ohne Browser** — der Node-Harness `probes/p105_b14_layout_probe.mjs` (Muster `p105_b8_c2_probe.mjs`) lädt das echte Modul: **fünf Zellen grün** (`regionen` **152/152**, `inseln` Faktor **2,78–2,80**, `spiralen` **20/20**, `stabilitaet` **0** Anker verschoben, `determinismus` **0,0 px**) und **fünf Gegenläufe, jeder rot an genau seiner Zelle** (Wächter `tests/test_b14_seed_probe.py`, 9 Tests) · die **Browser-Probe** bleibt im Determinismus grün (**0,0 px** über 152 Knoten, zwei Läufe byteweise gleich) und die Zahlen der roten Zellen **wandern**: `regionen` **57,2 % → 82,2 %**, das neue Item liegt jetzt **in** der Region seines Space (vorher 118,4 px von einem fremden), Kamera **78,1 %** Füllgrad (vorher 68,5 %) und **31,4 px** Versatz (vorher 43,8 px); `stabilitaet` bleibt rot (die anderen Spaces verschieben sich noch **233 px** — die Zentrums-Gravitation, Schritt 14.2) · **zwei Befunde an den Messungen**: die **Insel-Nachbarschaft ist mit den Startwerten knapp** (zwei Inselzentren nur **66,3 px** auseinander — der Goldwinkel bringt die Inseln 1 und 4 auf 52,5°) ⇒ die Insel-Zelle misst jetzt die **Gruppenbildung** statt „das nächste Inselzentrum" (das an der Klinge kippte: 35,95 px gegen 36,44 px); und der **wachsende Space verschiebt seine eigenen Inseln** um **1,1 px** (seine Region wächst mit — die Abnahme zählt die Knoten **anderer** Spaces) · `graph.js` **23,2 → 26,4 KB gz**, der Erstaufruf **220,8 KB** von 250 KB · Suite **1602** grün, `doc_health` 0 · **14.2 (L4) ✅ 2026-10-26**: `graph.js` — die **Zentrums-Gravitation** ist durch die **Anker-Gravitation** (`ANCHOR_GRAVITY = 0.02`, Startwert, in 14.4 gemessen) ersetzt: jeder Knoten zieht zu seinem **Space-Anker** (`computeRegions()`); die **Querfeder** (`CROSS_SPRING_FACTOR = 0.15`, `CROSS_SPRING_LENGTH_FACTOR = 3`) hält die Spaces **weit auseinander** (schwach, aber lang); der Startfaktor ist `ALPHA_START_SEEDED = 0.5` · **gemessen an der Wegwerf-Instanz** (Browser-Probe, 5 Spaces, 201 Knoten): `regionen` **152/152 = 100 %** (Basislinie 57,2 %, 14.1: 82,2 %), `stabilitaet` **Median 0,0 px** (max. 2,24 px; Basislinie 327,9 px, 14.1: 233 px), `budget` **201 Knoten in 2147 ms**, **0** Frames bei reduced motion; `kamera` und `beschriftungen` bleiben **rot** (⇒ **14.3** und **14.35**) · **drei Gegenläufe, jeder rot an genau seiner Zelle**: `querfeder` → `stabilitaet` rot (Median 29,2 px), `alpha` → `budget` rot (15,3 s) **und** `stabilitaet` rot, `zentrum` → **keine** Zelle rot (die Anker-Gravitation wirkt auf die **Weltgröße**, nicht auf die Regionen-Zelle: der Kamera-Füllgrad fällt von 101,2 % auf 68,7 %) ⇒ **datierte Korrektur** zum Plan §5 · **zwei Befunde an der Messung selbst**: (1) die Entspannung ist **chaotisch** — dieselben Knoten in anderer Reihenfolge ⇒ Endpositionen Median 56,5 px, max. 190,2 px ⇒ ein **Node-Harness** für die L4 wäre ein **Fehlgrün** (er misst eine andere Karte); der Node-Harness bleibt **Seed-only**; (2) ein „frischer“ Lauf kann **gepinnt** sein (die Ablage stand schon da) ⇒ die Stabilitäts-Zelle wäre zwangsläufig grün — die Probe liest jetzt `pinned_beim_start` direkt nach dem Reload und bricht ab, wenn die Ablage schon gefüllt war · Wächter `tests/test_b14_layout_probe.py` **10/10 grün** (die Zellen-Zuordnung, die Zahlen, die Prüfsummen, `pinned_beim_start`, die drei Gegenläufe, vier Manipulations-Gegenproben) · **14.3 (die Kamera) ✅ 2026-10-26**: `fitView()` (Umriss der sichtbaren Knoten + `FIT_MARGIN = 40` → `zoom = clamp(min(w/bw, h/bh), ZOOM_MIN, 1)`, Pan auf die **Mitte des Umrisses**), `viewFitted` (einmal je Kartenaufbau), `viewTouchedByUser` (hat der Nutzer selbst gezoomt oder verschoben, **gewinnt seine Ansicht**), der **Doppelklick** ruft `fitView()` · **gemessen** (5 Spaces, 152 Knoten): Füllgrad **93,6 %** (vorher 101,2 %), `passt` ✅, Versatz **0,42 px** (vorher **32,3 px**), Unsicherheit **0,68 px** · **E3: `ZOOM_MIN` bleibt 0,5** (der Einpass-Zoom bei **201** Knoten ist **68,8 %** — der Klemmpunkt greift nicht) · der Gegenlauf `fitview` macht **genau die** Kamera-Zelle rot und stellt den Stand von 14.2 **exakt** wieder her · **zwei Befunde**: (1) der Gegenlauf `querfeder` macht jetzt **zwei** Zellen rot (die zusammen gelaufenen Spaces ⇒ Welt **676 px**, Einpass-Zoom auf 100 % abgeklemmt, Füllgrad **59,6 %** < 60 %) ⇒ **datierte Korrektur** zum Plan §5; (2) die **C2-Probe** (Block 8) brach: ihr Zeiger war die *Weltposition* eines Knotens (der Canvas-Shim rechnet den Zoom nicht um) ⇒ mit der eingepassten Kamera trägt er den Knoten nicht mehr, und die Zelle `aktivierung` wäre grün geblieben, ohne dass der Fehler wiederhergestellt war ⇒ die Kamera wird dort festgenagelt (100 %/Pan 0), wie die festen Positionen in 14.2 · **14.35 (die Beschriftungen) ✅ 2026-10-27**: `graph.js` — `drawLabels()` sammelt die Beschriftungs-Rechtecke (Breite aus `ctx.measureText`, Höhe `LABEL_HEIGHT` = 12 px, Abstand `LABEL_OFFSET` = 6 px) und zeichnet **nur**, was kein schon gezeichnetes Rechteck überlappt; die Reihenfolge ist der **Vorrang** (Fokus → erster Ring → Suchtreffer → Rest nach Grad absteigend), der Fokus verliert seine Beschriftung **nie** (Plan §2.7) · **gemessen** (5 Spaces, 152 Knoten, Fokus mit **12** Nachbarn): **13** Kandidaten, **10** gezeichnet, **3** weggelassen, **0** überlappende Paare — der Stand 14.3 zählte **4** (Pixelvergleich), der Recorder zählt dieselbe Szene mit **5**; die Fokus-Beschriftung am Pixel nachgewiesen da (69 Pixel) · **datierte Änderung der Messung:** die gezeichneten Beschriftungen misst der Browser jetzt an den **`fillText`-Aufrufen** des letzten Bildes (Recorder an der Leinwand-API, **kein** Haken im Produktcode), **nicht** mehr an den Pixeln — die Regel lässt überlappende Beschriftungen weg, und an den Pixeln ist ein *weggelassenes* Rechteck nicht von einem *gezeichneten* zu unterscheiden (Nebenbefund: der alte Pixelvergleich zählte **4** Paare, der Recorder zählt **5**) · **Gegenlauf** `beschriftung` (die Kollisionsprüfung aus) macht **genau diese** Zelle rot (13 gezeichnet, 0 weggelassen, 5 Paare) · **nächster Schritt: 14.4** (die Startwerte messen) und 14.5 (die Bilder) |
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
| D | `v4.0.0` (vorher `v3.1.8`; Nikinger 2026-10-26) | — | — | nach Block 9–11 **+ 13** + Nachzug 2026-10-26 (**enthält RE-4 `rename_folder` und RE-3 `rename_space`**) (die UI-Änderungen aus Block 13 fahren mit) |

**Stand 2026-10-24 (Abend):** Deploy A ist **live** (`v3.1.5`, Release `20261023T065010.377336Z`, SHA `7358f22`, `health_gate` **9/9 OK**); der Branch `p105-block5` (Block 5 + 6 + P10.5-26) ist **gemergt**. **Deploy B ist ebenfalls live**: `v3.1.6`, Release `20261023T165838.591015Z`, SHA `e5c834e`, `health_gate` **9/9 OK** (aus `main` mit `fastmcp 4.1.3`; der Deploy lief beim Nikinger, die Release-Tests im Release **1380 grün** in 340,7 s). **Block 7.1 (UI-1) ist gemergt** (`f0e76b0`) und damit ab `v3.1.7` dabei. **Deploy C (`v3.1.7`) ist vorbereitet** — Badge, eigener Update-Log-Block `## 2026-10-24` (9 Zeilen für Menschen), Suite **1425 grün** (332,6 s), `doc_health` 0, `ui_budget` **5/5** (Erstaufruf 204,5 KB); **`deploy.sh` liegt beim Nikinger**. **Die Generalprobe davor ist gefahren: 26/26 Zellen grün an der Wegwerf-Instanz** (Details im Session-Block unten; die Zeile stand vorher auf „25/25" — **datierte Korrektur**, der Block-7.0-Commit hat die Probe um eine Zelle erweitert). **Der Deploy-Aufruf der letzten Session ist an den Release-Tests gescheitert — nicht am Befehl:** eine verklebte `updated:`-Zeile in `SESSIONS_ARCHIVE.md` (behoben, Details im Session-Block) — es fehlt nur noch der Deploy-Aufruf durch den Nikinger. **Block 7.1 (UI-1) ist gebaut** auf dem Branch `p105-block7` — **nicht gemergt** (Nikinger-Entscheidung: Deploy A vor dem Branch-Merge); der Merge wartet auf Deploy A/B.

**Ein Deploy ist vier Schritte, kein Commit** (Plan §2.5): volle Suite + `doc_health` + `ui_budget` grün · Badge und `docs/UPDATE_LOG.md` · Commit + Push · **`deploy.sh` durch den Nikinger** (Hard Rule 9) · `health_gate.sh` mit **echter Ausgabe** in den Commit — nie die Behauptung.

## Abnahmestand

**71 Zeilen** (P10.5-1–71) — **geteilt**: die **geschlossenen** Zeilen (✅/⚠️) stehen
**verbatim** in [`ABNAHME_ARCHIVE.md`](ABNAHME_ARCHIVE.md) (L3), hier stehen die **offenen**
(⬜) und die Summe. **[2026-10-27, Block 14.35]** die Beschriftungs-Zeile des Kartenlayouts ist
**geschlossen**: **P10.5-71** (keine zwei gezeichneten Beschriftungs-Rechtecke überlappen
sich — **0** Paare statt 5, **3** von **13** Beschriftungen weggelassen, die Fokus-
Beschriftung ist am Pixel nachgewiesen da) steht jetzt im Archiv, mit ihrem Beleg; die
Zeilen 68/69 sind geschlossen, **70 wartet auf die Bilder**. **[2026-10-26, Block 14.3]**
die Kamera-Zeile: **P10.5-67** (der Inhalt füllt **93,6 %** der Leinwand, passt **in** sie
und sitzt **0,42 px** neben der Mitte — vorher 32,3 px) steht jetzt im Archiv, mit ihrem
Beleg; die Zeilen 68/69/71 bleiben offen, 70 wartet auf die Bilder. **[2026-10-26, Block 14.1]** die
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
| P10.5-70 | Sichtung: drei Kartenbilder (5 Spaces, 30/32/30/30/30) — „zufällig, aber geordnet" | ⬜ | — |

**Summe:** 63 ✅ · 0 ⚠️ · 8 ⬜ (von 71). **[2026-10-27, Block 14.35]** +1 ✅ (10-71 die Beschriftungen — **0** überlappende Paare (der Stand 14.3 zählte **4** per Pixelvergleich — der Recorder zählt dieselbe Szene mit **5**), **3** von **13** Beschriftungen weggelassen, die Fokus-Beschriftung am Pixel nachgewiesen da; der Gegenlauf `beschriftung` macht **genau diese** Zelle rot) ⇒ 63 ✅ · 0 ⚠️ · 8 ⬜. **[2026-10-26, Block 14.3]** +1 ✅ (10-67 die Kamera — Füllgrad **93,6 %**, der Inhalt passt, der Umriss sitzt **0,42 px** neben der Mitte statt 32,3 px) ⇒ 62 ✅ · 0 ⚠️ · 9 ⬜. **[2026-10-26, Block 14.2]** +3 ✅ (10-66 die Regionen — **152/152 = 100 %**; 10-68 die Stabilität — Median **0,0 px**; 10-69 das Budget —
 201 Knoten in **2147 ms**, 0 Frames) ⇒ 61 ✅ · 0 ⚠️ · 10 ⬜. **[2026-10-26, Block 14.1]** +1 ✅ (10-65 der Determinismus — zwei frische Ladevorgänge, **0,0 px** über 152 Knoten, der Beleg byteweise reproduzierbar; der Gegenlauf `seedJitter` → `Math.random()` macht **genau diese** Zelle rot) ⇒ 58 ✅ · 0 ⚠️ · 13 ⬜. **[2026-10-26, Block 14.0]** +7 Zeilen (65–71 — das Kartenlayout; die **Basislinie** ist in `regionen`, `kamera`, `beschriftungen` und `stabilitaet` **rot**, das ist gewollt und gemessen) ⇒ 57 ✅ · 0 ⚠️ · 14 ⬜. **[2026-10-26, Nikinger-Sichtung]** +3 ✅ (10-32 UI-4, 10-37 C2-Stil, 10-51 Editor live) ⇒ 57 ✅ · 0 ⚠️ · 7 ⬜. **[2026-10-25, Block 13]** +3 ✅ (10-62 die Editor-Größen, 10-63 die Knopfleiste nach Word, 10-64 die Knopffarben) ⇒ 54 ✅ · 0 ⚠️ · 10 ⬜. **[2026-10-25, Block 12]** +3 ✅ (10-57 Oversize, 10-58 ROADMAP, 10-59 Register-Bilanz) ⇒ 51 ✅ · 0 ⚠️ · 10 ⬜. **[2026-10-25, Block 11.6]** +2 ✅ (10-54 ED-3 die Format-Konvention, 10-56 die P1-Ankündigung) ⇒ 48 ✅ · 0 ⚠️ · 13 ⬜. **[2026-10-25, Block 11.8]** +2 ✅ (10-52 der Roundtrip, 10-55 der Rohmodus) ⇒ 46 ✅ · 0 ⚠️ · 15 ⬜. **[2026-10-25, Block 11.5]** +1 ✅ (10-53, ED-2 die To-do-Kästchen) ⇒ 44 ✅ · 0 ⚠️ · 17 ⬜. **[2026-10-25, Block 11.7]** +1 ✅ (10-50, das Budget) ⇒ 43 ✅ · 0 ⚠️ · 18 ⬜. **[2026-10-24, Block 10.5]** +4 ✅ (10-45, 10-46, 10-47, 10-48) ⇒ 42 ✅ · 0 ⚠️ · 19 ⬜. **[2026-10-24, Block 9.3]** +2 ✅ (10-43, 10-44) ⇒ 38 ✅ · 0 ⚠️ · 23 ⬜. **[2026-10-24, Block 9.2]** +1 ✅ (10-42, RE-4 `rename_folder`) ⇒ 36 ✅ · 0 ⚠️ · 25 ⬜. **[2026-10-24, Block 9.1]** +1 ✅ (10-41, RE-7 `created_by`) ⇒ 35 ✅ · 0 ⚠️ · 26 ⬜. **[2026-10-24, Block 8]** +4 ✅ (10-36, 10-38, 10-39, 10-40) ⇒ 34 ✅ · 0 ⚠️ · 27 ⬜. **[Stand 2026-10-24, Block 7.5–7.7]** 33, 34 und 35 ✅. **[Korrektur 2026-10-22, Block 6]** Die Zeile stand vorher auf „21 ✅ · 0 ⚠️ · 40 ⬜“ — die Tabelle trug aber **20** ✅ (der Zähler war schon vor diesem Block falsch; Block 5 hat eine Zeile auf ✅ gezogen und die Summe nicht nachgezogen). Neu: **23**, weil Block 6 drei Zeilen (10-23/24/25) auf ✅ gesetzt hat. Ein Wächter prüft die Summe jetzt gegen die Tabelle (`tests/test_head_rules.py`) — **über beide Dateien**, seit die geschlossenen Zeilen im Archiv stehen. **[2026-10-23, Block 7.1]** +1 ✅ (10-29, UI-1) ⇒ 25 ✅ · 0 ⚠️ · 36 ⬜. **[2026-10-23, Block 7.2]** +1 ✅ (10-30, UI-2) ⇒ 26 ✅ · 0 ⚠️ · 35 ⬜. **[2026-10-23, Block 7.3]** +1 ✅ (10-31, UI-3) ⇒ 27 ✅ · 0 ⚠️ · 34 ⬜.

## Offen beim Nikinger

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
- **NEU 2026-10-26 (Block 14.2): die „Gehirnkarte“ wird zu Inseln — die C2-Furche hat im neuen
  Layout keinen Gegenstand.** Die neue L4 (Anker-Gravitation + Querfedern) rückt die Spaces
  **auseinander**: die Lappen zweier Spaces **berühren** sich nicht mehr. **Gemessen:** die
  Furche-Zellen in der C2-Probe **62 → 0**; in der Produktionskarte (5 Spaces) liegen die
  Schwerpunkte der Spaces **mindestens 346 px** auseinander, der Radius der Körpermaske ist
  **48 px** ⇒ dort kann keine Furche entstehen. Die **C2-Zeichenregel** ist damit im Alltag
  **nicht mehr sichtbar** (die Furchen zwischen den Lappen), die Bahnen zwischen den Spaces
  werden **lang**. **Kein Fehler, eine Folge des beauftragten Layouts** — aber eine **sichtbare
  Änderung** der in Block 8/9 abgenommenen Optik. **Was der Nikinger entscheiden muss:** die
  Bilder in **14.5** zeigen die Inseln; soll die C2-Optik (Furchen, Bahnen) an die Inseln
  angepasst werden (eigener Schritt nach 14.4) oder so bleiben? **Bis dahin** ist der C2-Wächter
  auf einen **festen Eingang** gestellt (zwei Spaces **berühren** sich dort, wo die Furche etwas
  zu trennen hat) — er prüft damit die **Zeichenregel**, nicht das Layout; ohne diese Reparatur
  wäre der Gegenlauf „Furche aus“ **grün** geblieben, ohne dass der Fehler wiederhergestellt
  war (`probes/p105_b8_c2_probe.mjs`, datierter Kommentar; `tests/test_graph_c2.py`).
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

> **Stand 2026-10-25 (Block 13):** die vier Aufträge sind gebaut **und gemessen** (Belege im
> Modulstatus, Abnahmezeilen P10.5-62/63/64). **Offen ist die Sichtung**, nicht die Arbeit.

1. ~~**Größe im Editor**~~ ✅ **Block 13.1** — die Stufen wirken im Live-Editor, und die Zeilenhöhe
   springt **nicht** mehr (die Ursache: CM5 rechnet die Zeilenhöhe einmal — eine Prozent-`line-height`
   im Span macht die Zeile höher als berechnet).
2. ~~**Knopffarben**~~ ✅ **Block 13.3** — das blaue, halbtransparente Design; die Vorsichtfarbe
   entsprechend **nachgerechnet** (`#FF8A8E`, 4,76:1).
3. ~~**Die ganze Knopfleiste nach Word**~~ ✅ **Block 13.2** — fünf Gruppen in Words Reihenfolge,
   gleiche Knöpfe, keine Entity-Icons. **Erst die Leiste, dann die Farben** — die Reihenfolge, die
   der Nikinger vorgegeben hat („erst Punkt 3 ansehen").
4. ~~**Screenshots der ganzen Gehirnkarte**~~ ✅ **Block 13.4** —
   `docs/screenshots/p105_b13_0{3,4,5}_*.png` (1920 × 1200, Zoom 50 %: die Welt der Knoten
   vollständig im Bild) — **die Sichtung steht aus** (P10.5-37 bleibt ⬜ bis zum Urteil).

**Für den nächsten Block offen:** die drei **Sichtungen** **P10.5-37** (C2-Stil der Karte),
**P10.5-51** (Editor Stufe 1) und **P10.5-32** (UI-4) — drei Bilder, drei Urteile; die Deploys
**C** (`v3.1.7`) und **D** (`v3.1.8`, jetzt **mit** den Änderungen aus Block 13) liegen beim Nikinger.

## Session stopped — 2026-10-27 (Block 14.35: die Beschriftungen ohne Überlappung)

**Ergebnis.** Schritt **14.35** des Plans: die Beschriftungen überlappen sich nicht mehr.
Beleg: `probes/p105_b14_layout_probe.json` (Browser, Wegwerf) + `…_gegenlauf_beschriftung.json`.

**Der Code** (`phase5_ui/webui/static/js/graph.js`, der einzige Produktcode): `drawLabels()`
sammelt die Beschriftungs-Rechtecke (Breite aus `ctx.measureText`, Höhe `LABEL_HEIGHT` = 12 px,
Abstand `LABEL_OFFSET` = 6 px vom Knotenrand) und zeichnet **nur**, was kein schon gezeichnetes
Rechteck überlappt (`labelRectOverlaps()`). Die Reihenfolge ist der **Vorrang** (Plan §2.7):
Fokus → erster Ring → Suchtreffer → Rest nach Grad absteigend (`labelCandidates()`); der Fokus
verliert seine Beschriftung **nie**. **Reine Zeichenlogik** — die Positionen der Knoten bleiben,
die Kamera misst nach dem Umbau **unverändert** (Füllgrad 93,6 %, Versatz 0,42 px). Die *Menge*
der beschrifteten Knoten ändert sich **nicht** (Plan 8.6: Fokus + erster Ring immer, sonst erst ab
`ZOOM_LABEL_THRESHOLD`); die Suchtreffer sind eine *Stufe der Reihenfolge*, kein eigener Anlass.

**Die Messung** (Wegwerf-Instanz, 5 Spaces, 152 Knoten, Fokus `itm_0000003f` mit **12** Nachbarn):
**13** Kandidaten, **10** gezeichnet, **3** weggelassen, **0** überlappende Paare — der Stand
14.3 zählte **4** per Pixelvergleich, der Recorder zählt dieselbe Szene mit **5**; die
Fokus-Beschriftung steht am **Pixel** nachgewiesen auf der Leinwand (69 Pixel). Der
Gegenlauf `beschriftung` (die Kollisionsprüfung aus) macht **genau diese** Zelle rot und stellt
den Stand von 14.2 wieder her: 13 gezeichnet, 0 weggelassen, **5** Paare.

**Ein Befund an der Messung selbst — er ändert die Messung, nicht die Regel.** Die *Menge* der
gezeichneten Beschriftungen misst der Browser jetzt an den **`fillText`-Aufrufen** des letzten
Bildes (ein Recorder an der Leinwand-API — **kein** Haken im Produktcode), **nicht** mehr an den
Pixeln: die neue Regel lässt überlappende Beschriftungen **weg**, und an den Pixeln ist ein
*weggelassenes* Rechteck nicht von einem *gezeichneten* zu unterscheiden (zwei überlappende
Rechtecke teilen sich ihre Pixel). Der Pixelbeweis bleibt für die Fokus-Beschriftung.
**Nebenbefund:** der alte Pixelvergleich zählte **4** Paare, der Recorder zählt **5** — er zählt
die Paare aus den Rechtecken, nicht aus den Pixeln. Die Mindestzahl gezeichneter Beschriftungen
(„die Hälfte der Kandidaten") ist auf **zwei** gesenkt: die Hälfte wäre nach der neuen Regel der
**falsche** Maßstab; der Wächter prüft zusätzlich, dass **mindestens eine** weggelassen wurde.

**Abnahme.** **P10.5-71 geschlossen** (die Beschriftungen) → **63 ✅ · 0 ⚠️ · 8 ⬜**. Wächter
`tests/test_b14_layout_probe.py` **15/15** (Zellen, Zahlen, Prüfsummen, fünf Gegenläufe, sieben
Manipulations-Gegenproben), `tests/test_graph_c2.py` **21/21**. Suite **1610** grün, `doc_health`
0, `ui_budget` **6/6** (Erstaufruf **238,9 KB**; `graph.js` **28,9 → 29,8 KB** gz).

**Datierte Anmerkung:** der 14.3-Block trägt das Datum **2026-10-26**, sein Commit und sein
Beleg dagegen **2026-10-27** (UTC) — der Block ist einen Tag zu früh datiert; hier steht das
richtige Datum.

**Nächster Schritt:** **14.4** (die Startwerte messen: `ANCHOR_GRAVITY` 0,02 · `CROSS_SPRING_FACTOR`
0,15 · `CROSS_SPRING_LENGTH_FACTOR` 3 · `ALPHA_START_SEEDED` 0,5 — und den fehlenden Gegenlauf
für die Regionen-Zelle schließen), dann **14.5** (die Bilder beim Nikinger).
