---
status: live
purpose: Plan P10.5 Block 14 — Kartenlayout „Weltgenerator": zufällig, aber geordnet (Space-Regionen → Ordner → Items → kurze Entspannung → Kamera passt sich an). Ausführer opencode.
read-when: vor dem Bau von Block 14 (graph.js-Layout), oder wenn die Karte „durcheinander" aussieht
detail: L2
up: ../../phase10_5_finishing/CLAUDE.md
down:
  - ../../phase5_ui/webui/static/js/graph.js            # der einzige Produktcode, der sich ändert
  - ../../phase10_5_finishing/probes/p105_b15_screens.py # der 5×30-Seed, aus dem der Auftrag kam
  - phase10_5_finishing_plan.md                         # 📕 Hauptplan (§2.1 Vorbedingung, Block 8 = C2-Stil)
  - phase10_5_block14_kartenlayout_plan_anhang.md       # 📦 §0 (Befund), §3 (E1–E4), §6 (Startauftrag)
updated: 2026-10-27 (Schritt 14.4 erledigt: die Startwerte sind **gemessen**, nicht gesetzt — 37 Varianten, alle zehn Werte bleiben; der neue Gegenlauf `region` macht die Regionen-Zelle rot und schließt die Lücke von P10.5-66; §0, §3 und §6 sind in den Anhang gewandert, der Plan trägt wieder Luft) | 2026-10-27 (Schritt 14.35 erledigt: die Beschriftungen ohne Überlappung — 0 überlappende Paare, 3 von 13 weggelassen; der Gegenlauf `beschriftung` macht genau die Beschriftungs-Zelle rot; **datierte Änderung der Messung**: die gezeichneten Beschriftungen misst der Browser jetzt an den `fillText`-Aufrufen, nicht mehr an den Pixeln) | 2026-10-26 (Schritt 14.3 erledigt: die Kamera passt sich ein — `fitView()`, Füllgrad 93,6 %, Versatz 0,42 px; **E3: `ZOOM_MIN` bleibt 0,5** (68,8 % bei 201 Knoten); **datierte Korrektur** der Gegenlauf-Zuordnung: `fitview` ⇒ `kamera`, `querfeder` macht jetzt *zwei* Zellen rot; die C2-Probe nagelt die Kamera fest) | 2026-10-26 (Schritt 14.2 erledigt: die L4 ist gebaut und gemessen; **datierte Korrektur** der Gegenlauf-Zuordnung in §5; der Befund „die Entspannung ist chaotisch“ — der Node-Harness bleibt Seed-only) | 2026-10-26 (E1–E4 beantwortet: E1 entfällt — KA-2 nie live; E2 nein; E3/E4 frei + Beschriftungen in Block 14) | 2026-10-26 (Entwurf, Claude Code)
---
# P10.5 Block 14 — Kartenlayout: zufällig, aber geordnet

> **Auftrag (Nikinger, 2026-10-26, nach den 5×30-Bildern `p105_b15_0{3,4,5}`):** „die Karte selbst ist
> großartig, aber das Layout sieht einfach nicht gut aus. Wie Minecraft: Chunks werden zufällig
> generiert, aber nach einer bestimmten Logik angepasst — zufällig, aber in einer Ordnung."
> Plan von Claude Code, Bau durch opencode.

## §0 Befund — warum die Karte heute ein Knäuel ist (gelesen, nicht vermutet)
> **Verbatim verschoben** nach `phase10_5_block14_kartenlayout_plan_anhang.md` (`scripts/move_sections.py`) — dort unter derselben Überschrift.

**Gelockt** (die vollständige Liste im Anhang, §0): der C2-Stil (Lappen, Furchen, Bahnen, Zellen — Block 8; der Nikinger: „die Karte selbst ist großartig“) · die Farben je **Kategorie** (`nodeColor()` = Rail, P8-15) · handgerollt ohne Bibliothek (P8-D) · kein Serverzustand (die Karte ist reine Geometrie im Browser; `/api/v1/graph` liefert `space` und `folder` schon — **kein** Server-Eingriff).
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

> **[2026-10-26, Schritt 14.2 — datiert]** Die L4 wird **im Browser** gemessen, **nicht** im
> Node-Harness: die Entspannung ist **chaotisch** — dieselben Knoten in anderer Reihenfolge
> ergeben am Ende eine andere Karte (Median der Endpositions-Abweichung **56,5 px**, max.
> **190,2 px**). Der **Seed** ist davon **nicht** betroffen (reine Funktion der Daten, ohne
> Rundung) ⇒ der Node-Harness `probes/p105_b14_layout_probe.mjs` misst weiterhin **nur den
> Seed**; ein L4-Harness in Node wäre ein **Fehlgrün** (er misst eine andere Karte als der
> Browser). Die Startwerte (`ANCHOR_GRAVITY = 0.02`, `CROSS_SPRING_FACTOR = 0.15`,
> `CROSS_SPRING_LENGTH_FACTOR = 3`, `ALPHA_START_SEEDED = 0.5`) sind **Startwerte** — in 14.4
> werden sie **gemessen** (nicht gesetzt).
>
> **[2026-10-27, Schritt 14.4 — datiert] Die Startwerte sind gemessen, nicht gesetzt.** Der Treiber `probes/p105_b14_startwerte.py` fährt die Browser-Probe je Wert (5 Spaces, 152 Items, 201 Knoten in der Budget-Zelle) und vergleicht die Zellen; die Rohdaten stehen in `probes/p105_b14_startwerte_messung.json`. **Die Regel der Wahl:** der Wert bleibt, wenn er die **Stabilität** hält (Median ≤ 2 px **und** Maximum ≤ 3 px) *und* die größte **Trennungs-Marge** hat (der kleinste Abstand „eigener Space-Schwerpunkt minus nächster fremder" über alle Knoten — 0 hieße: die Zelle kippt beim nächsten Item).
>
> **Ergebnis: alle zehn Startwerte sind bestätigt** — jeder hat einen gemessenen Nachbarwert, der schlechter ist: `ANCHOR_GRAVITY` 0,04 ⇒ Maximum 18,8 px · 0,08 ⇒ Median 3,2 px · `CROSS_SPRING_FACTOR` 0,3 ⇒ Median 5,0 px · `CROSS_SPRING_LENGTH_FACTOR` 1 ⇒ Median 16,0 px · `ALPHA_START_SEEDED` 0,75 ⇒ Median 77,0 px · `REGION_ITEM_STEP` 30 ⇒ Median 26,4 px · `REGION_PAD` 50 ⇒ Maximum 23,8 px · `REGION_GAP` 0 ⇒ Maximum 28,3 px · `ISLAND_FACTOR` 0,35 ⇒ Median 29,2 px · `ITEM_STEP` 10 ⇒ Median 34,1 px · `ITEM_JITTER_PX` 4 ⇒ Maximum 47,9 px. **Kein Wert wurde gesetzt.**

### 2.5 Kamera einpassen (`fitView()`, neu)

- Nach dem **ersten** Einschwingen je `loadGraph()` (nicht nach einem Drag): Umriss der
  sichtbaren Knoten + `FIT_MARGIN` 40 px → `zoom = clamp(min(w/bw, h/bh), ZOOM_MIN, 1)`, Pan auf
  die Mitte. **Nie über 100 %** einpassen — eine kleine Karte wird nicht aufgeblasen.
- Hat der Nutzer in dieser Sitzung schon gezoomt oder verschoben, passt die Karte **nicht** neu
  ein (seine Ansicht gewinnt). Doppelklick (heute: „Ansicht zurück") = `fitView()`.
- **E3 (frei):** reicht `ZOOM_MIN` 0,5 bei 200 Knoten nicht, senkt der Ausführer ihn (Untergrenze
  0,2) und nennt Wert und Messung im Bericht.

> **[2026-10-26, Schritt 14.3 — erledigt]** Die Kamera ist gebaut (`phase5_ui/webui/static/js/graph.js`):
> `fitView()` (Umriss der **sichtbaren** Knoten + `FIT_MARGIN = 40` → `zoom = clamp(min(w/bw,
> h/bh), ZOOM_MIN, 1)`, Pan auf die **Mitte des Umrisses** — nicht auf den Ursprung, das ist der
> Anker des eigenen Space), `FIT_MARGIN` als benannte Konstante, ein Merker `viewFitted`
> (einmal je Kartenaufbau) und ein Merker `viewTouchedByUser` (der Nutzer hat selbst gezoomt
> oder verschoben ⇒ **seine Ansicht gewinnt**). Der **Doppelklick** ruft jetzt `fitView()` auf
> (vorher: „Ansicht zurück" = Zoom 1, Pan 0 — also die Sicht **ohne** Einpassen).
>
> **E3 — gemessen, nicht gesetzt:** `ZOOM_MIN` **bleibt 0,5**. Der Einpass-Zoom bei **201
> Knoten** ist **68,8 %** (der Rand von 40 px je Seite ist eingerechnet), der Inhalt passt und
> sitzt mittig (Versatz **0,43 px**). Der Klemmpunkt greift also **nicht** — bei 200 Knoten
> ist der Wert nicht zu senken. (Der Klemmpunkt *wäre* sichtbar: stünde die Anzeige genau auf
> 50 % und passte der Inhalt nicht mehr in die Leinwand.)
>
> **Gemessen an der Wegwerf-Instanz** (`probes/p105_b14_layout_probe.json`, 5 Spaces, 152
> Knoten): Füllgrad **93,6 %** (vorher 101,2 %), **passt**, Versatz **0,42 px** (vorher
> **32,3 px**), Unsicherheit der Bestimmung **0,68 px**. Der Gegenlauf `fitview` (die Kamera
> ist aus) stellt den alten Stand **exakt** wieder her (Versatz 32,32 px, Zoom 100 %) und
> macht **genau die** Kamera-Zelle rot.
>
> **Ein Rand-Fall für 14.5 (aus den Konstanten gerechnet, nicht gemessen):** `FIT_MARGIN` ist
> 40 px, die Lappen-Kontur reicht aber **48 px** (`LOBE_REACH`) plus eine Rasterzelle (8 px)
> über den äußersten Knoten — auf der **begrenzenden** Achse können bis zu **16 px** der
> Kontur am Leinwandrand abgeschnitten werden. Sollen die Lappen **geschlossen** bleiben,
> bräuchte der Rand ≥ 56 px (ein **neuer** Wert — der Plan sagt 40 px).

### 2.6 Die gemerkte Karte (B4) — **kein** Schlüsselwechsel

**[2026-10-26, E1 beantwortet]** Das Merken (KA-2, Block 8) fährt mit Deploy C/D und war **nie
live** (live ist `v3.1.6`, Deploy B — Deploy-Tabelle im Phase-Head). Kein echter Browser trägt
einen `sfx:graph:layout:v1:`-Eintrag; der Schlüssel bleibt `v1`, **keine** Migration, **keine**
Update-Log-Zeile dafür. (Der Entwurf hatte `v1` → `v2` vorgeschlagen — mit dieser Tatsache unnötig.)

### 2.7 Beschriftungen ohne Überlappung (B6, E4 = in Block 14)

In `drawLabels()`: die Beschriftungs-Rechtecke (Breite aus `ctx.measureText`, Höhe = Schrift) in
Zeichenreihenfolge sammeln; überlappt ein neues Rechteck ein schon gezeichnetes, wird es **nicht**
gezeichnet. Reihenfolge = **Vorrang**: Fokus → erster Ring → Suchtreffer → Rest nach Grad
absteigend. Der Fokus-Knoten verliert seine Beschriftung **nie**. Reine Zeichenlogik, kein
Einfluss auf die Positionen.

> **[2026-10-26, Schritt 14.35 — erledigt]** Die Regel ist gebaut (`phase5_ui/webui/static/js/graph.js`):
> `labelCandidates()` (die **Reihenfolge** nach Vorrang: Fokus → erster Ring → Suchtreffer → Rest
> nach Grad absteigend), `labelRectOverlaps()` (die Kollisionsprüfung) und die Rechtecke in
> `drawLabels()` (Breite aus `ctx.measureText`, Höhe = `LABEL_HEIGHT` = 12 px, Abstand
> `LABEL_OFFSET` = 6 px vom Knotenrand — dieselben drei Werte wie in der Rechnung der Probe).
> **Die Menge der beschrifteten Knoten ändert sich nicht** (Plan 8.6: Fokus + erster Ring immer,
> sonst erst ab `ZOOM_LABEL_THRESHOLD`) — die Suchtreffer sind eine *Stufe der Reihenfolge*,
> kein eigener Anlass. **Reine Zeichenlogik:** die Positionen der Knoten bleiben, die Kamera
> misst nach dem Umbau **unverändert** (Füllgrad 93,6 %, Versatz 0,42 px).
>
> **Gemessen an der Wegwerf-Instanz** (`probes/p105_b14_layout_probe.json`, 5 Spaces, 152
> Knoten, Fokus-Knoten mit **12** Nachbarn): **13** Kandidaten, **10** gezeichnet, **3**
> weggelassen, **0** überlappende Paare (der Stand 14.3 zählte **4** per Pixelvergleich — der
> Recorder zählt dieselbe Szene mit **5**), die Fokus-Beschriftung ist da und steht
> **am Pixel** nachgewiesen auf der Leinwand (69 Beschriftungspixel). Der Gegenlauf
> `beschriftung` (die Kollisionsprüfung aus) macht **genau diese** Zelle rot und stellt den
> Stand von 14.2 wieder her: **13** gezeichnet, **0** weggelassen, **5** überlappende Paare.
>
> **Datierte Änderung der Messung (2026-10-27, Schritt 14.35).** Die *Menge* der gezeichneten
> Beschriftungen misst der Browser jetzt an den **`fillText`-Aufrufen** des letzten Bildes (ein
> Recorder an der Leinwand-API des Browsers — **kein** Haken im Produktcode), **nicht** mehr an
> den Pixeln. Grund: die Regel lässt überlappende Beschriftungen **weg**, und an den Pixeln ist
> ein *weggelassenes* Rechteck nicht von einem *gezeichneten* zu unterscheiden (zwei
> überlappende Rechtecke teilen sich ihre Pixel). Der Pixelbeweis bleibt für die
> **Fokus-Beschriftung**. **Ein Nebenbefund:** der alte Pixelvergleich fand **4** Paare, der
> Recorder findet **5** — er zählt die Paare aus den Rechtecken, nicht aus den Pixeln.
>
> **Die Mindestzahl gezeichneter Beschriftungen** (vorher: „mindestens die Hälfte der im Bild
> liegenden Kandidaten") ist auf **zwei** gesenkt: die Hälfte wäre nach der neuen Regel der
> **falsche** Maßstab — eine Minderheit gezeichneter Beschriftungen ist ihr *Ergebnis*, kein
> Fehler. Der Wächter prüft zusätzlich, dass **mindestens eine** Beschriftung weggelassen
> wurde (sonst wäre die Zelle auch ohne die Regel grün).

## §3 Entscheidungen für den Nikinger (vor dem Bau)
> **Verbatim verschoben** nach `phase10_5_block14_kartenlayout_plan_anhang.md` (`scripts/move_sections.py`) — dort unter derselben Überschrift.

## §4 Schritte (je Schritt **eine** opencode-Session, Plan §2.1 / P10.5-C)

| Schritt | Inhalt | Fertig, wenn |
|---|---|---|
| **14.0** | Vorbedingung + **Basislinie**: Probe `probes/p105_b14_layout_probe.py` (aus `p105_b15_screens.py`: Wegwerf-Instanz, freier Port, eigener Datenbaum, PID-Datei; **152 Items** statt 5×30 — siehe die datierte Abweichung in §5) mit den Zellen aus §5, **gegen den heutigen Code** | Probe läuft; die Basislinie ist **rot** in `regionen`/`kamera`/`beschriftungen`/`stabilitaet` (das ist der Beleg, dass die Zellen messen) — JSON neben der Probe |
| **14.1** | L1–L3: `hashString()`, `computeRegions()`, neuer `seedInitialPositions()` | Determinismus-Zelle grün ✅ **2026-10-26** |
| **14.2** | L4: Anker-Gravitation, Querfedern, `ALPHA_START_SEEDED`; `CENTER_GRAVITY` raus | Regionen-Zelle grün **und** Stabilität-Zelle grün (P10.5-68: ein neues Item verschiebt die Anker nur, wenn es den größten Space vergrößert); Budget-Zelle grün ✅ **2026-10-26** — `regionen` **152/152 = 100 %**, `stabilitaet` **Median 0,0 px**, `budget` **201 Knoten in 2147 ms**; `kamera`/`beschriftungen` bleiben rot (⇒ 14.3 / 14.35) |
| **14.3** | `fitView()` + Doppelklick; ggf. `ZOOM_MIN` (E3) | Kamera-Zelle grün ✅ **2026-10-26** — Füllgrad **93,6 %**, Versatz **0,42 px** (vorher 32,3 px), `passt` ✅; **E3: `ZOOM_MIN` bleibt 0,5** (der Einpass-Zoom bei 201 Knoten ist **68,8 %**, der Klemmpunkt greift nicht); der Gegenlauf `fitview` macht **genau** die Kamera-Zelle rot |
| **14.35** | Beschriftungen ohne Überlappung (§2.7) | Beschriftungs-Zelle grün ✅ **2026-10-26** — **0** überlappende Paare (der Stand 14.3 zählte **4** per Pixelvergleich — der Recorder zählt dieselbe Szene mit **5**), **3** von **13** Beschriftungen weggelassen, die Fokus-Beschriftung ist am Pixel nachgewiesen da; der Gegenlauf `beschriftung` macht **genau diese** Zelle rot (13 gezeichnet, 5 Paare) |
| **14.4** | Konstanten justieren (nur §2-Konstanten), Gegenläufe, Block-8-Proben neu fahren | ✅ **2026-10-27** — **37 Varianten** gemessen (`probes/p105_b14_startwerte.py`): **alle zehn Werte bleiben**; der neue Gegenlauf `region` macht die **Regionen-Zelle** rot (92,1 % statt 95 %) — die Lücke von **P10.5-66** ist geschlossen; `p105_b8_karte_probe.py` **grün** (nach einer Korrektur der *Probe*, s. u.), `p105_b8_c2_probe.mjs` grün |
| **14.5** | **Claude Code:** Bilder (`p105_b15_screens.py` ohne die 16 Radschritte), Update-Log-Zeile (neues Kartenlayout), Head, Abnahmezeilen | drei Kartenbilder beim Nikinger |

**Messen über Positionen, nicht über Pixel:** nach dem Einschwingen schreibt `saveLayout()` alle
`x, y` in den `localStorage` — die Probe liest sie (`page.evaluate`) und verbindet sie mit
`/api/v1/graph` (Space, Ordner). **Kein** Test-Haken im Produktcode.

> **[2026-10-26, Schritt 14.0 — erledigt]** Die Basislinie steht: `probes/p105_b14_layout_probe.py`
> und `p105_b14_layout_probe.json` (Wegwerf-Instanz auf TLS, freier Port je Lauf, eigener
> Datenwurzelbaum und eigene `auth.sqlite3` je Lauf, Stopp nur über die PID-Datei). **Rot** in
> `regionen` (**57,2 %** statt 95 %), `kamera` (der Umriss sitzt **43,8 px** neben der Mitte),
> `beschriftungen` (**5** überlappende Paare, die Fokus-Beschriftung ist da) und `stabilitaet`
> (Median **327,9 px**; das neue Item liegt **164,2 px** von seinem Space entfernt, aber nur
> **118,4 px** von einem fremden). **Grün** in `determinismus` (**0,0 px** über 152 Knoten) und
> `budget` (**201** Knoten, **2,53 s** bis Ruhe, **0** Frames bei reduced motion, die Karte ist
> gemalt). Die Abweichungen vom Plan-Seed und die Mess-Befunde stehen in §0 und §5.
> **Der Beleg ist byteweise reproduzierbar** (zwei Läufe, dieselbe Datei bis auf den
> Zeitstempel) — das war erst nach dem Einfrieren von **Server-IDs und Server-Uhr** der Fall
> (§0, datierte Ergänzung).
>
> **[2026-10-26, Schritt 14.1 — erledigt]** L1–L3 sind gebaut: `hashString()` (FNV-1a als Zahl,
> herausgezogen aus `seedJitter()` — **bitidentisch**: der C2-Wächter misst die Fortsätze der
> Zellen an genau diesem Hash), `computeRegions()` (**rein, ohne DOM**: eine Region je Space,
> Ordner-Inseln, Item-Spirale) und der neue `seedInitialPositions()`.
> **Der Seed wird jetzt ohne Browser gemessen:** der Node-Harness `probes/p105_b14_layout_probe.mjs`
> lädt das echte Modul (Muster `p105_b8_c2_probe.mjs`) und misst die reine Geometrie —
> **fünf Zellen grün** (`regionen` **152/152**, `inseln` Faktor **2,78–2,80**, `spiralen`
> **20/20**, `stabilitaet` **0** Anker verschoben, `determinismus` **0,0 px**) und **fünf
> Gegenläufe, jeder rot an genau seiner Zelle** (Wächter `tests/test_b14_seed_probe.py`).
> Die Browser-Probe (das Plan-Instrument) bleibt im Determinismus grün (**0,0 px** über 152
> Knoten, zwei Läufe byteweise gleich) — und die Zahlen der **roten** Zellen **wandern**:
> `regionen` von **57,2 %** auf **82,2 %**, das neue Item liegt jetzt **in** der Region seines
> Space (vorher 118,4 px von einem fremden), die Kamera füllt **78,1 %** (vorher 68,5 %) und der
> Umriss sitzt **31,4 px** neben der Mitte (vorher 43,8 px). `stabilitaet` bleibt **rot**: die
> anderen Spaces verschieben sich noch **233 px** — das ist die Zentrums-Gravitation
> (Schritt 14.2). **Zwei Befunde an den Messungen selbst:** (a) die **Insel-Nachbarschaft ist
> mit den Startwerten knapp** — zwei Inselzentren liegen nur **66,3 px** auseinander (der
> Goldwinkel bringt die Inseln 1 und 4 auf 52,5° auseinander) ⇒ die Insel-Zelle misst jetzt die
> **Gruppenbildung** (Abstand *zwischen* Inseln gegen *innerhalb* einer Insel) statt „das
> nächste Inselzentrum", das an der Klinge kippte (35,95 px gegen 36,44 px); (b) der
> **wachsende Space verschiebt seine eigenen Inseln** um **1,1 px** (seine Region wächst mit) —
> die gewollte Wirkung; die Abnahme zählt ausdrücklich die Knoten **anderer** Spaces.
>
> **[2026-10-26, Schritt 14.2 — erledigt]** Die L4 ist gebaut (`phase5_ui/webui/static/js/graph.js`):
> `CENTER_GRAVITY` und `ALPHA_START` sind **ersetzt** (nicht ergänzt) — jetzt `ANCHOR_GRAVITY =
> 0.02` (Startwert, in **14.4** gemessen), `CROSS_SPRING_FACTOR = 0.15`,
> `CROSS_SPRING_LENGTH_FACTOR = 3`, `ALPHA_START_SEEDED = 0.5`; die Anker kommen aus
> `computeRegions()` (der neue Modulstate `spaceRegions` merkt sie sich beim Seed).
> **Gemessen an der Wegwerf-Instanz** (Browser-Probe, 5 Spaces, 201 Knoten): `regionen`
> **152/152 = 100 %** (Basislinie 57,2 %, 14.1: 82,2 %), `stabilitaet` **Median 0,0 px**
> (max. 2,24 px; Basislinie 327,9 px, 14.1: 233 px), `budget` **201 Knoten in 2147 ms**,
> **0** Frames bei reduced motion. `kamera` (Füllgrad 101,2 %, Versatz 32,3 px) und
> `beschriftungen` bleiben **rot** ⇒ **14.3** und **14.35**.
>
> **Drei Befunde an der Messung selbst — sie ändern den Plan, nicht nur den Bericht:**
>
> 1. **Die Zuordnung der Gegenläufe im Plan §5 war falsch (datierte Korrektur).** Der Plan
>    nennt für **P10.5-66** den Gegenlauf „`ANCHOR_GRAVITY` → Leinwandmitte". Gemessen:
>    **keine** Zelle wird rot — die Regionen-Zelle bleibt bei **100 %**. Der Gegenlauf wirkt
>    auf die **Weltgröße**: der Kamera-Füllgrad fällt von **101,2 %** auf **68,7 %** (und der
>    Versatz sinkt von 32,3 px auf 11,0 px). Die Anker-Gravitation ist damit **an der
>    Regionen-Zelle nicht nachweisbar** — der Plan hat die Wirkung der **Zentrums-Gravitation**
>    (14.1: 82,2 %) mit der Wirkung der **Anker-Gravitation** (100 %) verwechselt. Die
>    wirksamen Gegenläufe sind: **`querfeder`** ⇒ `stabilitaet` rot (Median 29,2 px) und
>    **`alpha`** ⇒ `budget` rot (15,3 s) **und** `stabilitaet` rot (Median 91,1 px). Alle drei
>    Gegenläufe fahren über eine **Kopie** von `phase5_ui/webui/static` — der Arbeitsbaum bleibt
>    unberührt.
> 2. **Die Entspannung ist chaotisch — der Node-Harness bleibt Seed-only.** Dieselben Knoten
>    in einer **anderen Reihenfolge** ergeben am Ende eine **andere** Karte: Median der
>    Endpositions-Abweichung **56,5 px**, max. **190,2 px**, **86 %** der Knoten weichen um mehr
>    als 20 px ab. Ursache: die Repulsion sammelt die Kräfte in der Reihenfolge der
>    Knotenliste; die Rundungsfehler (1e-16) wachsen in der Relaxation zu einem **anderen
>    Gleichgewicht**. Der **Seed** ist davon **nicht** betroffen (reine Funktion der Daten, ohne
>    Rundung) — deshalb misst der Node-Harness weiterhin **nur den Seed**. Ein
>    Node-Harness für die L4 würde eine **andere** Karte messen als der Browser: ein
>    **Fehlgrün ohne Aussage**.
> 3. **Ein „frischer" Lauf kann gepinnt sein — die Stabilitäts-Zelle wäre zwangsläufig grün.**
>    Die Karte merkt ihre Positionen im `localStorage`; lädt die Probe in ein **gefülltes**
>    `localStorage`, startet die Simulation **gepinnt** und die Stabilitäts-Zelle misst
>    „nichts bewegt sich" — **grün, ohne dass etwas geprüft wurde**. Die Probe liest jetzt
>    `pinned_beim_start` **direkt nach dem Reload** und bricht **ab**, wenn die Ablage schon
>    gefüllt war; der Beleg führt die Prüfsummen **vorher/nachher** mit, und die Zelle ist
>    nur grün, wenn sie sich **unterscheiden**.
>
> **[2026-10-26, Schritt 14.3 — erledigt]** Die Kamera ist gebaut und gemessen
> (`phase5_ui/webui/static/js/graph.js`): `fitView()`, `FIT_MARGIN = 40`, der Zoom
> `clamp(min(w/bw, h/bh), ZOOM_MIN, 1)`, der Pan auf die **Mitte des Umrisses**, einmal je
> Kartenaufbau; hat der Nutzer selbst gezoomt oder verschoben, **gewinnt seine Ansicht**; der
> **Doppelklick** passt die Kamera ein. **E3: `ZOOM_MIN` bleibt 0,5** (der Einpass-Zoom bei
> 201 Knoten ist **68,8 %** — der Klemmpunkt greift nicht).
>
> **Gemessen an der Wegwerf-Instanz** (5 Spaces, 152 Knoten): Füllgrad **93,6 %** (vorher
> 101,2 %), **passt**, Versatz **0,42 px** (vorher **32,3 px**), Unsicherheit **0,68 px**.
> Der Gegenlauf `fitview` macht **genau die** Kamera-Zelle rot und stellt den Stand von 14.2
> **exakt** wieder her.
>
> **Ein Fund an der *anderen* Probe (Block 8 gegen Block 14).** Die C2-Probe (`p105_b8_c2_probe.mjs`,
> Node) misst die **Zeichenregel** — Lappen, Furche, Bahnen, Zellen, Abdunklung. Ihr **Zeiger**
> war die Weltposition eines Knotens (der Canvas-Shim rechnet den Zoom/Pan **nicht** um) — mit
> der eingepassten Kamera trägt er den Knoten nicht mehr, und die Zelle `aktivierung` wäre
> **grün geblieben, ohne dass der Fehler wiederhergestellt war**. Dieselbe Art von
> Eingangs-Fixierung wie die festen Positionen (14.2): die Kamera wird auf **100 % / Pan 0**
> festgenagelt (`fitView()` ist aus). Die **Kamera selbst** misst der Browser-Wächter, nicht
> dieser.

> **[2026-10-27, Schritt 14.4 — erledigt]** Die Startwerte sind **gemessen**, nicht gesetzt: der
> Treiber `probes/p105_b14_startwerte.py` fährt die Browser-Probe **37 Mal** (jede der zehn
> §2-Konstanten: der Startwert und je zwei Nachbarn), patched die Konstante in einer **Kopie**
> der statischen Dateien (der Arbeitsbaum bleibt unberührt) und legt die Tabelle
> `probes/p105_b14_startwerte_messung.json` ab. **Die Regel der Wahl:** der Wert bleibt, wenn
> er die **Stabilität** hält (Median ≤ 2 px **und** Maximum ≤ 3 px) **und** die größte
> **Trennungs-Marge** hat (der kleinste Abstand „eigener Space-Schwerpunkt minus nächster
> fremder" über alle Knoten). **Ergebnis: alle zehn Werte bleiben** — jeder Nachbarwert ist
> schlechter (die Tabelle im Messbericht): `ANCHOR_GRAVITY` 0,04 ⇒ Maximum **18,8 px**, 0,08 ⇒
> Median **3,2 px** · `CROSS_SPRING_FACTOR` 0,3 ⇒ Median **5,0 px** (0 ⇒ die Welt wächst auf
> 1334 px) · `CROSS_SPRING_LENGTH_FACTOR` 1 ⇒ Median **16,0 px** · `ALPHA_START_SEEDED` 0,75 ⇒
> Median **77,0 px** (0,25 ⇒ 1769 ms) · dieselbe Regel bei den sechs **Seed**-Konstanten
> (`REGION_ITEM_STEP` 30 ⇒ **26,4 px** · `REGION_PAD` 50 ⇒ **23,8 px** · `REGION_GAP` 0 ⇒
> **28,3 px** · `ISLAND_FACTOR` 0,35 ⇒ **29,2 px** · `ITEM_STEP` 10 ⇒ **34,1 px** ·
> `ITEM_JITTER_PX` 4 ⇒ **47,9 px**). Der Code ändert sich **nur im Kommentar** — die Werte
> tragen jetzt ihre Herleitung.
>
> **Der fehlende Gegenlauf für die Regionen-Zelle (P10.5-66) ist geschlossen.** `region` legt
> **alle Space-Anker auf einen Punkt** ⇒ die Regionen-Zelle fällt auf **92,1 %** (140 von 152
> Knoten; die Trennungs-Marge wird **−99,3 px**), die Kamera-Zelle auf **56,6 %** und die
> Stabilitäts-Zelle auf **Median 278,1 px**. Er macht damit **drei** Zellen rot — die beiden
> anderen sind eine **echte, zweite Folge** (wie beim Gegenlauf `querfeder`, 14.3): bricht die
> Zuordnung der Anker, kippt die Karte insgesamt. **Vier Kandidaten sind verworfen**, weil sie
> nur die **Stabilität** rot machten (ein Space verschoben: 100 % · eine Insel gespalten: 97,4 % ·
> zwei Inseln: 98,7 % · zwei Anker: 99,3 %): die **Anker-Gravitation je Space** repariert eine
> verschobene Region — der Gegenlauf muss die **Zuordnung** der Anker brechen, nicht ihre Lage.
>
> **Ein Fund an der *anderen* Probe (Block 8) — die Zelle `layout` war rot, ohne dass das Merken
> kaputt war.** `p105_b8_karte_probe.py` wartete mit dem **Canvas-Hash** auf die Ruhe; der Hash
> ist aber **vor dem ersten Tick** stabil (die Karte wird zuerst zweimal unverändert gezeichnet —
> genau der Befund, den die Block-14-Probe schon benannt hat). Die Probe maß damit die
> **ungepasste Kamera** (Zoom 100 % statt des Einpass-Zooms 50 %) und nicht die gemerkte Ablage.
> Sie wartet jetzt auf dasselbe Signal wie die Block-14-Probe — der `requestAnimationFrame` **aus
> graph.js** hört auf ⇒ Zelle grün (13 Kernpixel am Zielpunkt vorher, **11** nachher).
> **Am Produktcode änderte sich nichts** — die Kamera passt sich auch nach dem Neuladen ein
> (gemessen: der Zoom nach dem Neuladen ist der Einpass-Zoom).
> **Randnotiz (kein Fehler, gemessen):** der normale Aufbaupfad startet die Simulation auch bei
> einer 0×0-Leinwand (der reduced-motion-Pfad wartet seit 8.7 auf die Box) — dann ginge der
> Einpass verloren. **Hier tritt der Fall nicht auf** (die Box steht, gemessen), deshalb bleibt
> der Produktcode unverändert.

## §5 Abnahme (neue Zeilen P10.5-65–71 — **stehen seit 2026-10-26 (Block 14.0) im Head**)

| # | Kriterium | Messung | Gegenlauf (muss rot werden) |
|---|---|---|---|
| **P10.5-65** | Determinismus: zwei frische Ladevorgänge (leerer Speicher) → max. Abweichung ≤ 1 px | Probe | `seedJitter` → `Math.random` |
| **P10.5-66** | Regionen: ≥ 95 % der Knoten liegen dem Schwerpunkt **ihres** Space am nächsten (5 Spaces, 30/32/30/30/30 — siehe die datierte Seed-Abweichung unten) | Probe | **`region`** (neu, **14.4**): alle Space-Anker auf einen Punkt ⇒ die Zelle wird **rot** (92,1 % statt 95 %) — **gemessen**; bis 14.4 gab es **keinen** wirksamen (die datierte Korrektur unten) |
| **P10.5-67** | Kamera: nach dem Einschwingen, **ohne** Rad, füllt der Inhalt ≥ 60 % der Leinwand auf mindestens einer Achse | Probe | `fitView()` aus — **gemessen** 14.3: macht genau die Kamera-Zelle rot (Versatz 32,32 px statt 0,42 px) |
| **P10.5-68** | Stabilität: +1 Item in einem nicht-größten Space → Median-Verschiebung der Knoten **anderer** Spaces ≤ 2 px (frischer Lauf); in einer **gemerkten** Karte landet das neue Item in der Region seines Space | Probe | `querfeder` (Querfeder-Faktor/Länge zurück auf 0) — **gemessen** 14.2; der geplante („Space-Reihenfolge nach Item-Zahl") ist ein **Seed**-Gegenlauf und gehört in den Node-Harness (`slot`) |
| **P10.5-69** | Budget und Bestand: 200 Knoten ≤ 3 s bis Ruhe · reduced motion 0 Frames (P10.5-40) · Block-8-Proben grün | Probe | `ALPHA_START_SEEDED` → 1 (Budget reißt) — **gemessen** 14.2: 15,3 s |
| **P10.5-70** | Sichtung: drei Kartenbilder (5 Spaces, 30/32/30/30/30) — „zufällig, aber geordnet" | Nikinger | — |
| **P10.5-71** | Beschriftungen: bei Fokus auf einen Knoten mit ≥ 5 Nachbarn überlappen sich **keine** zwei gezeichneten Beschriftungs-Rechtecke; die Fokus-Beschriftung ist immer da | Probe (Rechtecke über `measureText` nachgerechnet) | Kollisionsprüfung aus — **gemessen** 14.35: macht genau die Beschriftungs-Zelle rot (13 gezeichnet, 0 weggelassen, **5** überlappende Paare) |

> **Datierte Präzisierung der Kamera-Zelle (2026-10-26, Schritt 14.0).** „Füllt ≥ 60 %" allein
> kann die Zelle nicht tragen: wäre der Inhalt **größer** als die Leinwand, wäre der Füllgrad
> *über* 100 % und die Zelle grün, obwohl der Nutzer den größten Teil der Karte nie sieht.
> Gemessen werden deshalb **drei** Stücke: **Füllgrad** (≥ 60 % auf einer Achse), **Passung**
> (der Inhalt passt in die Leinwand) und **Zentrierung** (der Umriss liegt in der Mitte,
> ≤ 3 px) — die beiden letzten sind genau die Eigenschaften, die `fitView()` setzt (Plan §2.5:
> „Zoom so, dass der Inhalt passt, Pan auf die Mitte"). Erst damit ist der Gegenlauf
> „`fitView()` aus" überhaupt erkennbar.
>
> **Datierte Abweichung vom Seed (2026-10-26, Schritt 14.0).** Der Plan-Seed sagt „5×30". Die
> Probe sät **152** Items: `alpha` 30, `beta` **32**, `gamma` 30, `delta` 30, `epsilon` 30.
> Grund: §2.1 verlangt, dass ein neues Item die Anker **nur** verschiebt, wenn es den
> **größten** Space vergrößert — bei fünf gleich grossen Spaces wäre „nicht-größter Space"
> undefiniert und P10.5-68 unmöglich. **Und:** die Probe friert die Item-IDs
> (`files.generate_id()`) **und** die **Uhr** (`Store(now_fn=…)`) ein — sonst wäre der Datensatz
> und damit die Basislinie laufverschieden (§0). **Das gilt für den Server genauso:** die über
> die API angelegten Items bekommen im Wegwerf-Server ebenfalls feste IDs und eine
> **eingefrorene Uhr mit Zähler** — sonst wandert die Sortierung nach `-updated` über die
> Sekundengrenze und die Karte ist zwischen zwei Läufen eine andere (§0, datierte Ergänzung).
>
> **Datierte Präzisierung des Kamera-Werts (2026-10-26, Schritt 14.0).** Zoom und Pan kommen aus
> **einer** Bestimmung (dem Modus der Pan-Kandidaten): die Anzeige rundet auf ganze Prozent
> (`(zoom*100).toFixed(0)` = 1), die Rechnung braucht den **verfeinerten** Zoom (0,9994) —
> sonst rechnen Füllgrad und Zentrierung mit einem anderen Zoom als der Pan. Die Probe weist
> die **Unsicherheit** der Bestimmung aus (**0,65 px** — die Streuung der Pan-Kandidaten plus
> der Zoom-Rasterfehler); sie ist um eine Größenordnung kleiner als der gemessene Versatz
> (**43,8 px**) und trägt die Aussage nicht.
>
> **Datierte Korrektur der Gegenlauf-Zuordnung (2026-10-26, Schritt 14.2).** §5 nannte für
> **P10.5-66** den Gegenlauf „`ANCHOR_GRAVITY` → Leinwandmitte". **Gemessen: keine Zelle wird
> rot** — die Regionen-Zelle bleibt bei **100 %**, und der Gegenlauf wirkt auf die
> **Weltgröße** (Kamera-Füllgrad **101,2 % → 68,7 %**). Der Plan hat die Wirkung der
> **Zentrums-Gravitation** (14.1: 82,2 %) mit der Wirkung der **Anker-Gravitation** (100 %)
> verwechselt. **Gemessene** Zuordnung: `querfeder` ⇒ `stabilitaet` rot (Median 29,2 px) ·
> `alpha` ⇒ `budget` rot (15,3 s) **und** `stabilitaet` rot (Median 91,1 px) · `zentrum` ⇒
> **keine** Zelle rot (⇒ **kein** Gegenlauf für 66 in der Browser-Probe; der **Seed**-Gegenlauf
> `slot` im Node-Harness deckt die Reihenfolge ab). Ein Wächter ohne wirksamen Gegenlauf
> beweist nichts — die Lücke bleibt **offen** und wird in **14.4** mit einem Gegenlauf geschlossen,
> der die Regionen-Zelle **wirklich** rot macht (der Kandidat: die Regionen-Zuordnung des
> Spaces verschieben).
>
> **Datierte Korrektur der Gegenlauf-Zuordnung (2026-10-26, Schritt 14.3).** Zwei Änderungen,
> beide **gemessen**:
>
> 1. **`fitview` (neu) ⇒ `kamera`.** Der Gegenlauf zu P10.5-67 ist „`fitView()` aus" — er
>    patcht die **erste Zeile des Rumpfes** von `fitView()` (die Funktion wird zum No-op; der
>    Anker ist derselbe wie in der C2-Probe, die die Kamera aus demselben Grund festnagelt).
>    Er macht **genau die** Kamera-Zelle rot und stellt den Stand von 14.2 **exakt** wieder her
>    (Versatz **32,32 px**, Zoom 100 %) — die anderen fünf Zellen bleiben grün.
> 2. **`querfeder` macht jetzt *zwei* Zellen rot.** Die Querfeder auf „so stark und kurz wie
>    die Feder im Space" zu stellen, lässt die Spaces **zusammenlaufen**: die Welt wird
>    **676 px** breit (statt 1148 px), der Einpass-Zoom ist auf **100 % abgeklemmt**, und der
>    Füllgrad sinkt auf **59,6 %** — unter die 60-%-Schwelle der Abnahme P10.5-67. Die
>    Kamera-Zelle folgt damit **ihrer** Regel (sie misst, ob die Karte die Leinwand füllt);
>    das ist eine **zweite, echte** Folge, kein Fehler des Gegenlaufs. Die Erwartung im
>    Wächter ist die Dokumentation davon.
>
> **Datierte Ergänzung zur Wirkung des Gegenlaufs `zentrum` (2026-10-26, Schritt 14.3).** Seit
> die Kamera einpasst, ist die Wirkung an **zwei** Zahlen zu sehen: die Welt ist **779 px**
> breit statt 1148 px, **und** der Füllgrad sinkt von **93,6 %** auf **68,8 %** (die kleinere
> Welt passt auch bei 100 % Zoom nicht ganz in die Leinwand). Vor 14.3 war nur der Füllgrad zu
> sehen (101,2 % → 68,7 %), weil die Kamera nicht einpasste. Die Zelle bleibt grün — die
> Anker-Gravitation ist weiterhin **nicht** die Regel, die die Regionen-Zelle misst.
>
> **Datierte Ergänzung zur Beschriftungs-Zelle (2026-10-26, Schritt 14.35).** Zwei Dinge, die
> die **Messung** betreffen, nicht die Regel:
>
> 1. **Die Menge der gezeichneten Beschriftungen misst der Browser jetzt an den
>    `fillText`-Aufrufen** (ein Recorder an der Leinwand-API — **kein** Haken im Produktcode),
>    **nicht** mehr an den Pixeln. Die neue Regel lässt überlappende Beschriftungen **weg**,
>    und an den Pixeln ist ein *weggelassenes* Rechteck nicht von einem *gezeichneten* zu
>    unterscheiden: zwei überlappende Rechtecke teilen sich ihre Pixel. Der Pixelbeweis bleibt
>    für die **Fokus-Beschriftung** (sie muss am Pixel nachgewiesen auf der Leinwand stehen).
>    **Nebenbefund:** der alte Pixelvergleich zählte **4** überlappende Paare, der Recorder
>    zählt **5** — er zählt die Paare aus den Rechtecken, nicht aus den Pixeln.
> 2. **Die Mindestzahl gezeichneter Beschriftungen** (vorher „die Hälfte der im Bild liegenden
>    Kandidaten") ist **zwei**: die Hälfte wäre nach der neuen Regel der falsche Maßstab. Der
>    Wächter prüft zusätzlich, dass **mindestens eine** Beschriftung **weggelassen** wurde —
>    sonst wäre die Zelle auch ohne die Regel grün (der Gegenlauf `beschriftung` beweist die
>    Regel von der anderen Seite).
>
> **Gemessene Zahlen (14.35):** Fokus `itm_0000003f` („Gamma Plan 01") mit **12** Nachbarn ·
> **13** Kandidaten · **10** gezeichnet · **3** weggelassen · **0** überlappende Paare · die
> Fokus-Beschriftung steht mit **69** Beschriftungspixeln auf der Leinwand.
>
> **Datierte Korrektur der Gegenlauf-Zuordnung (2026-10-27, Schritt 14.4).** Für **P10.5-66**
> gibt es jetzt einen **wirksamen** Gegenlauf: `region` (alle Space-Anker auf einen Punkt) ⇒ die
> Regionen-Zelle fällt auf **92,1 %** (140 von 152 Knoten; die Trennungs-Marge wird **−99,3 px**),
> die Kamera-Zelle auf **56,6 %** und die Stabilitäts-Zelle auf **Median 278,1 px**. Die **drei
> Zellen** sind eine **echte, zweite Folge** (wie bei `querfeder`, 14.3): bricht die Zuordnung der
> Anker, kippt die Karte insgesamt. Vier Kandidaten sind **verworfen**, weil sie nur die
> **Stabilität** rot machten (ein Space verschoben: 100 % · eine Insel gespalten: 97,4 % · zwei
> Inseln: 98,7 % · zwei Anker: 99,3 %) — die **Anker-Gravitation je Space** repariert eine
> verschobene Region; der Gegenlauf muss die **Zuordnung** der Anker brechen, nicht ihre Lage.
> Damit ist die Lücke aus 14.2 („ein Wächter ohne wirksamen Gegenlauf beweist nichts")
> **geschlossen**.

## §6 Startauftrag — Block 14 · Ausführer (opencode)
> **Verbatim verschoben** nach `phase10_5_block14_kartenlayout_plan_anhang.md` (`scripts/move_sections.py`) — dort unter derselben Überschrift.
