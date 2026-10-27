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
updated: 2026-10-26 (Schritt 14.3 erledigt: die Kamera passt sich ein — `fitView()`, Füllgrad 93,6 %, Versatz 0,42 px; **E3: `ZOOM_MIN` bleibt 0,5** (68,8 % bei 201 Knoten); **datierte Korrektur** der Gegenlauf-Zuordnung: `fitview` ⇒ `kamera`, `querfeder` macht jetzt *zwei* Zellen rot; die C2-Probe nagelt die Kamera fest) | 2026-10-26 (Schritt 14.2 erledigt: die L4 ist gebaut und gemessen; **datierte Korrektur** der Gegenlauf-Zuordnung in §5; der Befund „die Entspannung ist chaotisch“ — der Node-Harness bleibt Seed-only) | 2026-10-26 (E1–E4 beantwortet: E1 entfällt — KA-2 nie live; E2 nein; E3/E4 frei + Beschriftungen in Block 14) | 2026-10-26 (Entwurf, Claude Code)
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
| B4 | `saveLayout()` (Z. 1377) merkt **jeden** Knoten nach jedem Einschwingen; `seedInitialPositions()` hält gemerkte Knoten **fest** (`pinned`) | ein neues Item landet auf dem globalen Ring statt bei seinen Nachbarn (die gemerkten bleiben fest) |
| B6 | `drawLabels()` (Z. 923): jede Beschriftung wird gezeichnet, ohne Prüfung gegen die schon gezeichneten | Beschriftungen überdecken sich (Fokusbild: „Gamma Protokoll 28“ / „Gamma Frage 14“) |
| B5 | Keine Kamera-Anpassung; `ZOOM_MIN` 0,5 (Z. 141), Start-Zoom 1 | bei 151 Knoten füllt der Inhalt bei 50 % ≈ 40 % der Leinwand; die Probe musste 16 Radschritte „drehen" — **Korrektur 2026-10-26 (gemessen, Schritt 14.0):** die Karte **passt** bei 100 % und füllt **68,5 %** der Leinwand (Welt 777 × 494 px in 1134 × 1061 px). Die 16 Radschritte fuhren auf `ZOOM_MIN` (50 %) und **verkleinerten** die Karte — der Effekt ist im Bild (`p105_b15_03_map_ganz.png`) gut sichtbar (leere Ränder). Der Befund bleibt als **Ursache** richtig (es gibt keine Kamera-Anpassung), seine **Wirkung** war falsch gelesen: die Karte ist heute nicht zu groß, sie steht **schief** (der Umriss sitzt 43,8 px neben der Mitte — die Zentrums-Gravitation zieht den **Schwerpunkt**, nicht den Umriss) |

> **Datierte Korrektur an §0 B5 (2026-10-26, Schritt 14.0, `probes/p105_b14_layout_probe.py`):**
> gemessen, nicht vermutet — die Belegzahlen stehen in `phase10_5_finishing/probes/p105_b14_layout_probe.json`.
> Zwei weitere Befunde aus derselben Messung, die die **Planung** betreffen:
> **(a)** der Canvas-Hash taugt **nicht** als Ruhe-Signal (die Karte wird zuerst zweimal
> unverändert gezeichnet — der Seed steht, die Simulation hat noch nicht gerechnet; die erste
> Probe-Messung erklärte die Karte daraufhin für „zur Ruhe gekommen" und maß den **Saat-Ring**
> statt des Gleichgewichts: der Welt-Umriss war um die Hälfte zu klein); **(b)** `store.search()`
> sortiert nach `-updated`, und die Item-Zeitstempel sind die **Wanduhr** — die Knoten-Reihenfolge
> in `/api/v1/graph` und damit der Saat-Ring sind laufverschieden (gemessen: Welt-Umrisse zwischen
> 596 × 889 px und 463 × 1020 px). Beides ist **Datensatz**, nicht Produktcode: die Probe friert
> deshalb IDs (`files.generate_id()`) **und** Uhr (`Store(now_fn=…)`) ein.
>
> **Datierte Ergänzung (2026-10-26, Schritt 14.0, nach der Advisor-Runde):** das Einfrieren
> musste **auch den Server** treffen — die Items, die die Probe über die API anlegt, bekamen
> (1) **zufällige IDs** (`secrets.token_hex`) und (2) **Wanduhr-Zeitstempel**. Beides macht die
> Karte laufverschieden: der Saat-Jitter ist ein **Hash der ID**, und die Sortierung nach
> `-updated` wechselt, sobald zwei Items über eine Sekundengrenze fallen (gemessen: die 48
> Extra-Items standen im einen Lauf mit `0x91a…`, im anderen mit `0x92c…` vorn — zwei
> verschiedene Karten). Der Wegwerf-Server bekommt darum eine **eingefrorene Uhr mit Zähler**
> (jedes neue Item: 2026-01-02 12:00 + n Sekunden — jünger als der Seed-Stand) und
> **deterministische IDs** (`0x901` aufwärts). Seitdem ist der Beleg **byteweise
> reproduzierbar**: zwei Läufe hintereinander liefern dieselbe Datei (bis auf den Zeitstempel).

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

> **[2026-10-26, Schritt 14.2 — datiert]** Die L4 wird **im Browser** gemessen, **nicht** im
> Node-Harness: die Entspannung ist **chaotisch** — dieselben Knoten in anderer Reihenfolge
> ergeben am Ende eine andere Karte (Median der Endpositions-Abweichung **56,5 px**, max.
> **190,2 px**). Der **Seed** ist davon **nicht** betroffen (reine Funktion der Daten, ohne
> Rundung) ⇒ der Node-Harness `probes/p105_b14_layout_probe.mjs` misst weiterhin **nur den
> Seed**; ein L4-Harness in Node wäre ein **Fehlgrün** (er misst eine andere Karte als der
> Browser). Die Startwerte (`ANCHOR_GRAVITY = 0.02`, `CROSS_SPRING_FACTOR = 0.15`,
> `CROSS_SPRING_LENGTH_FACTOR = 3`, `ALPHA_START_SEEDED = 0.5`) sind **Startwerte** — in 14.4
> werden sie **gemessen** (nicht gesetzt).

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

## §3 Entscheidungen für den Nikinger (vor dem Bau)

| # | Frage | Empfehlung |
|---|---|---|
| **E1** | Schlüssel `v1` → `v2`? | **Entfällt** (Nikinger 2026-10-26: „no browser has yet seen the new design“ — KA-2 nie live, §2.6) |
| **E2** | Eigene Farbtöne je fremdem Space? | **Nein** — nach den neuen Bildern neu entscheiden (Nikinger 2026-10-26) |
| **E3** | `ZOOM_MIN` senken, falls 200 Knoten bei 0,5 nicht passen? | **Frei** (Nikinger 2026-10-26) — der Ausführer senkt bei Bedarf, nennt Wert und Messung im Bericht |
| **E4** | Überlappende Beschriftungen? | **In Block 14** (Nikinger 2026-10-26) — §2.7, Schritt 14.35 |

## §4 Schritte (je Schritt **eine** opencode-Session, Plan §2.1 / P10.5-C)

| Schritt | Inhalt | Fertig, wenn |
|---|---|---|
| **14.0** | Vorbedingung + **Basislinie**: Probe `probes/p105_b14_layout_probe.py` (aus `p105_b15_screens.py`: Wegwerf-Instanz, freier Port, eigener Datenbaum, PID-Datei; **152 Items** statt 5×30 — siehe die datierte Abweichung in §5) mit den Zellen aus §5, **gegen den heutigen Code** | Probe läuft; die Basislinie ist **rot** in `regionen`/`kamera`/`beschriftungen`/`stabilitaet` (das ist der Beleg, dass die Zellen messen) — JSON neben der Probe |
| **14.1** | L1–L3: `hashString()`, `computeRegions()`, neuer `seedInitialPositions()` | Determinismus-Zelle grün ✅ **2026-10-26** |
| **14.2** | L4: Anker-Gravitation, Querfedern, `ALPHA_START_SEEDED`; `CENTER_GRAVITY` raus | Regionen-Zelle grün **und** Stabilität-Zelle grün (P10.5-68: ein neues Item verschiebt die Anker nur, wenn es den größten Space vergrößert); Budget-Zelle grün ✅ **2026-10-26** — `regionen` **152/152 = 100 %**, `stabilitaet` **Median 0,0 px**, `budget` **201 Knoten in 2147 ms**; `kamera`/`beschriftungen` bleiben rot (⇒ 14.3 / 14.35) |
| **14.3** | `fitView()` + Doppelklick; ggf. `ZOOM_MIN` (E3) | Kamera-Zelle grün ✅ **2026-10-26** — Füllgrad **93,6 %**, Versatz **0,42 px** (vorher 32,3 px), `passt` ✅; **E3: `ZOOM_MIN` bleibt 0,5** (der Einpass-Zoom bei 201 Knoten ist **68,8 %**, der Klemmpunkt greift nicht); der Gegenlauf `fitview` macht **genau** die Kamera-Zelle rot |
| **14.35** | Beschriftungen ohne Überlappung (§2.7) | Beschriftungs-Zelle grün |
| **14.4** | Konstanten justieren (nur §2-Konstanten), Gegenläufe, Block-8-Proben neu fahren | alle Zellen grün, jeder Gegenlauf rot an **genau** seiner Zelle; `p105_b8_karte_probe.py` + `p105_b8_c2_probe.mjs` grün |
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

## §5 Abnahme (neue Zeilen P10.5-65–71 — **stehen seit 2026-10-26 (Block 14.0) im Head**)

| # | Kriterium | Messung | Gegenlauf (muss rot werden) |
|---|---|---|---|
| **P10.5-65** | Determinismus: zwei frische Ladevorgänge (leerer Speicher) → max. Abweichung ≤ 1 px | Probe | `seedJitter` → `Math.random` |
| **P10.5-66** | Regionen: ≥ 95 % der Knoten liegen dem Schwerpunkt **ihres** Space am nächsten (5 Spaces, 30/32/30/30/30 — siehe die datierte Seed-Abweichung unten) | Probe | ⚠️ **kein wirksamer Gegenlauf** (14.2) — der geplante lässt die Zelle **grün**; die datierte Korrektur steht unten |
| **P10.5-67** | Kamera: nach dem Einschwingen, **ohne** Rad, füllt der Inhalt ≥ 60 % der Leinwand auf mindestens einer Achse | Probe | `fitView()` aus — **gemessen** 14.3: macht genau die Kamera-Zelle rot (Versatz 32,32 px statt 0,42 px) |
| **P10.5-68** | Stabilität: +1 Item in einem nicht-größten Space → Median-Verschiebung der Knoten **anderer** Spaces ≤ 2 px (frischer Lauf); in einer **gemerkten** Karte landet das neue Item in der Region seines Space | Probe | `querfeder` (Querfeder-Faktor/Länge zurück auf 0) — **gemessen** 14.2; der geplante („Space-Reihenfolge nach Item-Zahl") ist ein **Seed**-Gegenlauf und gehört in den Node-Harness (`slot`) |
| **P10.5-69** | Budget und Bestand: 200 Knoten ≤ 3 s bis Ruhe · reduced motion 0 Frames (P10.5-40) · Block-8-Proben grün | Probe | `ALPHA_START_SEEDED` → 1 (Budget reißt) — **gemessen** 14.2: 15,3 s |
| **P10.5-70** | Sichtung: drei Kartenbilder (5 Spaces, 30/32/30/30/30) — „zufällig, aber geordnet" | Nikinger | — |
| **P10.5-71** | Beschriftungen: bei Fokus auf einen Knoten mit ≥ 5 Nachbarn überlappen sich **keine** zwei gezeichneten Beschriftungs-Rechtecke; die Fokus-Beschriftung ist immer da | Probe (Rechtecke über `measureText` nachgerechnet) | Kollisionsprüfung aus |

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

## §6 Startauftrag — Block 14 · Ausführer (opencode)

**Vorher (Plan §2.1):** `limit.context` ≤ 400.000 prüfen · `git status` sauber · Blockbasis = HEAD
· E1–E4 sind beantwortet (§3, 2026-10-26).

**Erlaubte Pfade:** `phase5_ui/webui/static/js/graph.js` · `phase10_5_finishing/probes/**` ·
`phase10_5_finishing/tests/**`. **Nicht:** Server-Code, `app.css`, `nodeColor()`, die Lappen-/
Bahnen-/Zellen-Zeichnung (Block 8), `docs/UPDATE_LOG.md` (14.5, Claude Code).

**Anker (Stand `59ca205`, **Zeilen nach 14.3 in Klammern**):** `seedInitialPositions()` Z. 477
(706) · `startLayout()` Z. 514 (752) · `seedJitter()` Z. 530 (785) · `runSimulation()` Z. 540 (790) /
`settle()` Z. 561 (813) · `applyForces()` Z. 603 (873) (Gravitation Z. 650 · 924) · Konstanten
Z. 120–141 (131–160, die Block-14-Konstanten 200–232) · `LAYOUT_KEY_PREFIX` Z. 170 (183) ·
`loadStoredLayout()`/`saveLayout()` Z. 1364/1377 (1646/1659) · `drawLabels()` Z. 923 (1205) ·
`onWheel()` Z. 1563 (1886) · **neu 14.3:** `fitView()` Z. 1739 · `onDoubleClick()` Z. 1904.

**Regeln:** Proben **nur** an der Wegwerf-Instanz (eigener Port, tmp-`DATA_ROOT`,
tmp-`auth.sqlite3`, Playwright aus `~/.claude-code-tools/e2e-venv`), Stopp **nur** über die
PID-Datei (Hard Rule 9) · Umgebung ohne `SHAREFYX_*`/`SFX_*` · jede Konstante aus §2 bleibt eine
**benannte** Konstante mit Kommentar „Startwert, gemessen in 14.4" · ein Commit je Schritt, Head
im selben Commit (Hard Rule 8) · volle Suite grün vor dem Commit.

**Bericht je Schritt:** die Zellen der Probe (JSON), bei 14.4 die Gegenläufe, bei 14.3 die
E3-Zahl. Rohdaten, keine Bewertung (Memory: Ausführer-Auswertung macht Fleet).
