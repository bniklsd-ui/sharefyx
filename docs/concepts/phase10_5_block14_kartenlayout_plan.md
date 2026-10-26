---
status: draft
purpose: Plan P10.5 Block 14 — Kartenlayout „Weltgenerator": zufällig, aber geordnet (Space-Regionen → Ordner → Items → kurze Entspannung → Kamera passt sich an). Ausführer opencode.
read-when: vor dem Bau von Block 14 (graph.js-Layout), oder wenn die Karte „durcheinander" aussieht
detail: L2
up: ../../phase10_5_finishing/CLAUDE.md
down:
  - ../../phase5_ui/webui/static/js/graph.js            # der einzige Produktcode, der sich ändert
  - ../../phase10_5_finishing/probes/p105_b15_screens.py # der 5×30-Seed, aus dem der Auftrag kam
  - phase10_5_finishing_plan.md                         # 📕 Hauptplan (§2.1 Vorbedingung, Block 8 = C2-Stil)
updated: 2026-10-26 (Entwurf, Claude Code; wartet auf Freigabe + E1–E4)
---
# P10.5 Block 14 — Kartenlayout: zufällig, aber geordnet

> **Auftrag (Nikinger, 2026-10-26, nach den 5×30-Bildern `p105_b15_0{3,4,5}`):** „die Karte selbst ist
> großartig, aber das Layout sieht einfach nicht gut aus. Wie Minecraft: Chunks werden zufällig
> generiert, aber nach einer bestimmten Logik angepasst — zufällig, aber in einer Ordnung."
> Plan von Claude Code, Bau durch opencode.

## §0 Befund — warum die Karte heute ein Knäuel ist (gelesen, nicht vermutet)

| # | Stelle (`graph.js`, Stand `59ca205`) | Wirkung |
|---|---|---|
| B1 | `seedInitialPositions()` (Z. 477–510): **ein Ring** aller Knoten um die Leinwandmitte, Reihenfolge = API-Reihenfolge, nur Hash-Jitter ±15 px | Space und Ordner spielen beim Säen keine Rolle — alles startet gemischt |
| B2 | `applyForces()` Schritt 3 (Z. 650–657): **eine** Zentrums-Gravitation (`CENTER_GRAVITY` 0,012) zur Leinwandmitte | zieht alle Spaces auf denselben Punkt — die Regionen verschmelzen |
| B3 | Federn (Z. 627–648): Kanten **quer** zwischen Spaces sind genauso stark und kurz wie Kanten im Space | jede Querverbindung zieht zwei Spaces ineinander |
| B4 | `saveLayout()` (Z. ~1375) merkt **jeden** Knoten nach jedem Einschwingen; `seedInitialPositions()` hält gemerkte Knoten **fest** (`pinned`) | einmal geöffnet, bleibt das Knäuel **für immer** im Browser — und ein neues Item landet auf dem globalen Ring statt bei seinen Nachbarn |
| B5 | Keine Kamera-Anpassung; `ZOOM_MIN` 0,5 (Z. 141), Start-Zoom 1 | bei 151 Knoten füllt der Inhalt bei 50 % ≈ 40 % der Leinwand; die Probe musste 16 Radschritte „drehen" |

**Was bleibt, wie es ist (gelockt):** der C2-Stil (Lappen, Furchen, Bahnen, Zellen — Block 8; der
Nikinger: „die Karte selbst ist großartig"), die Farben je **Kategorie** (`nodeColor()` = Rail,
P8-15), handgerollt ohne Bibliothek (P8-D), kein Serverzustand, der Server bleibt dumm (die Karte
ist reine Geometrie im Browser; `/api/v1/graph` liefert `space` und `folder` schon — **kein**
Server-Eingriff).

## §1 Das Prinzip — vier Schichten, wie ein Weltgenerator

Minecraft würfelt nicht frei: ein **Seed** bestimmt deterministisch zuerst die groben Regionen
(Biome), darin die Strukturen, darin das Detail — und jede Schicht folgt Regeln. Übertragen:

| Schicht | Minecraft | hier | Regel |
|---|---|---|---|
| L1 Welt | Biome | **eine Region je Space** | eigener Space in der Mitte; die anderen auf einer Goldwinkel-Spirale darum (137,508°), Reihenfolge = **Hash des Space-Namens** (nicht die Item-Zahl → stabil) |
| L2 Struktur | Dörfer, Höhlen | **Ordner-Inseln** in der Region | Wurzel-Items (`folder: ""`) im Zentrum, Ordner auf einer kleinen Spirale, Reihenfolge = Hash des Ordnernamens |
| L3 Detail | Blöcke, Bäume | **Items** um ihre Ordner-Insel | Goldwinkel-Spirale (Sonnenblumenmuster: dicht, ohne Überlappung), Reihenfolge = Hash der Item-ID, plus `seedJitter` — **zufällig aussehend, reproduzierbar** |
| L4 Anpassung | Glättung der Chunk-Grenzen | **kurze Entspannung** (die bestehende Kraftsimulation, umgebaut) | jeder Knoten zieht zu **seinem** Space-Anker statt zur Leinwandmitte; Querkanten schwach und lang |
| — Kamera | — | **Einpassen** nach dem ersten Einschwingen | Inhalt füllt die Leinwand; der Nutzer kann danach frei zoomen |

**Zufall = `seedJitter(id, salt)`** (FNV-1a, Z. 530 — existiert, wird wiederverwendet). Kein
`Math.random()` (P8.6-D2: die Karte darf beim Öffnen nicht „fliegen").

## §2 Entwurf im Detail

### 2.1 L1 — Space-Regionen (`computeRegions(nodes)`, neu, rein, ohne DOM)

- `n_s` = Knoten je Space. Regionsradius `R_s = REGION_ITEM_STEP · sqrt(n_s) + REGION_PAD`
  (Startwerte `REGION_ITEM_STEP = 22`, `REGION_PAD = 30` — **Startwerte, durch Messung in 14.4
  justiert**, nicht geschätzt übernommen).
- Reihenfolge: `state.ownSpace` zuerst (Index 0, Anker im Ursprung), dann alle anderen nach
  `hash(space)` aufsteigend (FNV-1a über den Namen — dieselbe Funktion wie `seedJitter`, als
  `hashString()` herausgezogen).
- Anker `k ≥ 1`: Winkel `θ_k = θ0 + k · 137,508°`, Abstand `r_k = SLOT · sqrt(k)`, mit
  `SLOT = 2 · max_s(R_s) + REGION_GAP` (`REGION_GAP = 40`). `θ0 = hash(ownSpace)` → jede Person
  sieht „ihre" Welt, immer dieselbe.
- **Stabilität (Abnahme 10-68):** ein neues Item verschiebt die Anker **nur**, wenn es den
  **größten** Space vergrößert (dann wächst `SLOT`). Sonst bleiben alle Anker byte-gleich.
- Welt → Leinwand: Ursprung = Leinwandmitte (wie bisher `cx, cy`).

### 2.2 L2 — Ordner-Inseln

- Je Space: Ordner nach `hash(folder)` sortiert; Wurzel (`""`) am Anker.
- Ordner `j` (1…F): Winkel `θ0_s + j · 137,508°`, Abstand `R_s · 0,55 · sqrt(j / F)`.

### 2.3 L3 — Items

- Je Ordner-Insel: Items nach `hash(id)` sortiert; Item `i`: Winkel `i · 137,508°`, Abstand
  `ITEM_STEP · sqrt(i)` (`ITEM_STEP = 14`), plus `seedJitter(id, 1|2) · 8` px.
- **Neue Items in einer gemerkten Karte** (B4) landen so **in ihrer Ordner-Insel** statt auf dem
  globalen Ring — die gemerkten Nachbarn bleiben fest, das Neue findet seinen Platz.

### 2.4 L4 — Entspannung (Umbau von `applyForces()`)

| Kraft | heute | neu |
|---|---|---|
| Abstoßung | paarweise, `REPULSION_STRENGTH` 800 | **unverändert** |
| Federn im Space | `SPRING_LENGTH` 60, `SPRING_STRENGTH` 0,05 | **unverändert** |
| Federn quer (Space ≠ Space) | wie im Space | Stärke × `CROSS_SPRING_FACTOR` (0,15), Länge × `CROSS_SPRING_LENGTH_FACTOR` (3) |
| Gravitation | zur Leinwandmitte, `CENTER_GRAVITY` 0,012 | zum **eigenen Space-Anker**, `ANCHOR_GRAVITY` (Start 0,02) |
| Startenergie | `ALPHA_START` 1 | `ALPHA_START_SEEDED` 0,5 — der Seed liegt schon nah am Ziel; weniger Ticks |

`CENTER_GRAVITY` entfällt (ersetzt, nicht zusätzlich). Das 3-s-Budget bei 200 Knoten (Kopf von
`graph.js`) gilt weiter und wird **gemessen** (10-69).

### 2.5 Kamera einpassen (`fitView()`, neu)

- Nach dem **ersten** Einschwingen je `loadGraph()` (nicht nach einem Drag): Umriss der
  sichtbaren Knoten + `FIT_MARGIN` 40 px → `zoom = clamp(min(w/bw, h/bh), ZOOM_MIN, 1)`, Pan auf
  die Mitte. **Nie über 100 %** einpassen — eine kleine Karte wird nicht aufgeblasen.
- Hat der Nutzer in dieser Sitzung schon gezoomt oder verschoben, passt die Karte **nicht** neu
  ein (seine Ansicht gewinnt). Doppelklick (heute: „Ansicht zurück") = `fitView()`.
- **E3:** reicht `ZOOM_MIN` 0,5 bei 200 Knoten nicht, wird das in 14.3 **gemessen** und dem
  Nikinger vorgelegt — nicht still gesenkt.

### 2.6 Die gemerkte Karte (B4) — Schlüssel `v1` → `v2`

`LAYOUT_KEY_PREFIX` `sfx:graph:layout:v1:` → `…:v2:` (Wert-Feld `v: 2`). Ohne diesen Schritt sieht
**jeder Browser, der die Karte schon geöffnet hat** — der des Nikingers, Fabians — das alte
Knäuel weiter; eine frische Wegwerf-Probe würde das nie zeigen. Der alte Eintrag wird beim ersten
Laden **gelöscht** (kein toter Speicher). **E1:** dabei gehen auch **von Hand gezogene**
Positionen verloren — der Code kann sie von automatisch gemerkten nicht unterscheiden. Eine Zeile
im Update-Log sagt es.

## §3 Entscheidungen für den Nikinger (vor dem Bau)

| # | Frage | Empfehlung |
|---|---|---|
| **E1** | Schlüssel `v1` → `v2`: alle gemerkten Karten (auch von Hand gezogene Knoten) einmalig verwerfen? | **Ja** — sonst wirkt der neue Generator in keinem bestehenden Browser; Update-Log-Zeile |
| **E2** | Eigene Farbtöne je fremdem Space (heute alle vier grau, P8-15 = Rail-Parität)? | **Nein, erst messen** — getrennte Regionen machen die Furchen sichtbar; nach den Bildern neu entscheiden |
| **E3** | `ZOOM_MIN` senken, falls 200 Knoten bei 0,5 nicht passen? | **Nur nach Messung** (14.3 legt die Zahl vor) |
| **E4** | Überlappende Beschriftungen (Fokusbild: „Gamma Protokoll 28" / „Gamma Frage 14")? | **Nicht in Block 14** — eigener Posten (P10.6/P11); getrennte Regionen entschärfen es ohnehin |

## §4 Schritte (je Schritt **eine** opencode-Session, Plan §2.1 / P10.5-C)

| Schritt | Inhalt | Fertig, wenn |
|---|---|---|
| **14.0** | Vorbedingung + **Basislinie**: Probe `probes/p105_b14_layout_probe.py` (aus `p105_b15_screens.py`: Wegwerf-Instanz, freier Port, eigener Datenbaum, PID-Datei; 5×30-Seed) mit den Zellen aus §5, **gegen den heutigen Code** | Probe läuft; die Basislinie ist **rot** in Regionen/Kamera (das ist der Beleg, dass die Zellen messen) — JSON neben der Probe |
| **14.1** | L1–L3: `hashString()`, `computeRegions()`, neuer `seedInitialPositions()`; Schlüssel `v2` + Löschen von `v1` | Determinismus-Zelle grün; v1-Zelle grün |
| **14.2** | L4: Anker-Gravitation, Querfedern, `ALPHA_START_SEEDED`; `CENTER_GRAVITY` raus | Regionen-Zelle grün; Budget-Zelle grün |
| **14.3** | `fitView()` + Doppelklick; Messung E3 | Kamera-Zelle grün; E3-Zahl im Bericht |
| **14.4** | Konstanten justieren (nur §2-Konstanten), Gegenläufe, Block-8-Proben neu fahren | alle Zellen grün, jeder Gegenlauf rot an **genau** seiner Zelle; `p105_b8_karte_probe.py` + `p105_b8_c2_probe.mjs` grün (deren `layout:v1`-Schlüssel auf `v2` nachgezogen) |
| **14.5** | **Claude Code:** Bilder (`p105_b15_screens.py` ohne die 16 Radschritte), Update-Log-Zeile (E1), Head, Abnahmezeilen | drei Kartenbilder beim Nikinger |

**Messen über Positionen, nicht über Pixel:** nach dem Einschwingen schreibt `saveLayout()` alle
`x, y` in den `localStorage` — die Probe liest sie (`page.evaluate`) und verbindet sie mit
`/api/v1/graph` (Space, Ordner). **Kein** Test-Haken im Produktcode.

## §5 Abnahme (neue Zeilen P10.5-65–70, kommen bei Freigabe in den Head)

| # | Kriterium | Messung | Gegenlauf (muss rot werden) |
|---|---|---|---|
| **P10.5-65** | Determinismus: zwei frische Ladevorgänge (leerer Speicher) → max. Abweichung ≤ 1 px | Probe | `seedJitter` → `Math.random` |
| **P10.5-66** | Regionen: ≥ 95 % der Knoten liegen dem Schwerpunkt **ihres** Space am nächsten (5×30) | Probe | `ANCHOR_GRAVITY` → Leinwandmitte |
| **P10.5-67** | Kamera: nach dem Einschwingen, **ohne** Rad, füllt der Inhalt ≥ 60 % der Leinwand auf mindestens einer Achse | Probe | `fitView()` aus |
| **P10.5-68** | Stabilität: +1 Item in einem nicht-größten Space → Median-Verschiebung der Knoten **anderer** Spaces ≤ 2 px (frischer Lauf); in einer **gemerkten** Karte landet das neue Item in der Region seines Space | Probe | Space-Reihenfolge nach Item-Zahl statt Hash |
| **P10.5-69** | Budget und Bestand: 200 Knoten ≤ 3 s bis Ruhe · reduced motion 0 Frames (P10.5-40) · Block-8-Proben grün · v1-Eintrag vorbelegt → die neue Anordnung erscheint | Probe | `v1` nicht löschen |
| **P10.5-70** | Sichtung: drei Kartenbilder (5×30) — „zufällig, aber geordnet" | Nikinger | — |

## §6 Startauftrag — Block 14 · Ausführer (opencode)

**Vorher (Plan §2.1):** `limit.context` ≤ 400.000 prüfen · `git status` sauber · Blockbasis = HEAD
· **E1–E4 beantwortet** (§3; ohne E1 nicht starten).

**Erlaubte Pfade:** `phase5_ui/webui/static/js/graph.js` · `phase10_5_finishing/probes/**` ·
`phase10_5_finishing/tests/**`. **Nicht:** Server-Code, `app.css`, `nodeColor()`, die Lappen-/
Bahnen-/Zellen-Zeichnung (Block 8), `docs/UPDATE_LOG.md` (14.5, Claude Code).

**Anker (Stand `59ca205`):** `seedInitialPositions()` Z. 477 · `startLayout()` Z. 514 ·
`seedJitter()` Z. 530 · `runSimulation()` Z. 540 / `settle()` Z. 561 · `applyForces()` Z. 603
(Gravitation Z. 650) · Konstanten Z. 120–141 · `LAYOUT_KEY_PREFIX` Z. 170 · `loadStoredLayout()`/
`saveLayout()` ab Z. ~1362 · `onWheel()` Z. 1563 · `p105_b8_c2_probe.mjs` Z. 525 (`layout:v1`).

**Regeln:** Proben **nur** an der Wegwerf-Instanz (eigener Port, tmp-`DATA_ROOT`,
tmp-`auth.sqlite3`, Playwright aus `~/.claude-code-tools/e2e-venv`), Stopp **nur** über die
PID-Datei (Hard Rule 9) · Umgebung ohne `SHAREFYX_*`/`SFX_*` · jede Konstante aus §2 bleibt eine
**benannte** Konstante mit Kommentar „Startwert, gemessen in 14.4" · ein Commit je Schritt, Head
im selben Commit (Hard Rule 8) · volle Suite grün vor dem Commit.

**Bericht je Schritt:** die Zellen der Probe (JSON), bei 14.4 die Gegenläufe, bei 14.3 die
E3-Zahl. Rohdaten, keine Bewertung (Memory: Ausführer-Auswertung macht Fleet).
