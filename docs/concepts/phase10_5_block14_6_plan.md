---
status: live
purpose: Plan P10.5 Block 14.6 — der Körper der Gehirnkarte: aus fünf Inseln wird **ein** Körper mit Lappen und Furchen, ohne einen Knoten zu bewegen (nur die Körpermaske in `computeLobes()`). Ausführer opencode (M3.1 Flash).
read-when: vor dem Bau von 14.6, oder wenn die Karte „wie Inseln" statt „wie ein Gehirn" aussieht
detail: L2
up: ../../phase10_5_finishing/CLAUDE.md
down:
  - phase10_5_block14_kartenlayout_plan.md              # 📗 Block 14 (Layout, Kamera, Beschriftungen) — §2.5 der Rand-Fall
  - ../../phase5_ui/webui/static/js/graph.js            # der einzige Produktcode, der sich ändert: `computeLobes()`
  - ../../phase10_5_finishing/probes/p105_b14_karte_bilder.py  # die Bilder-Probe (Recorder, `--konstante`, `--bilder`)
  - ../../phase10_5_finishing/probes/p105_b8_c2_probe.mjs      # der C2-Wächter (feste Positionen, Messpflaster)
updated: 2026-10-28 (Schritt 14.6.2: der Wert steht — 160; der Wächter `koerper` beißt) | 2026-10-28 (Schritt 14.6.1: der Algorithmus steht, die sechs Varianten sind gemessen — der kleinste Wert mit EINER Komponente ist 160; STOPP E1) | 2026-10-28 (Schritt 14.6.0 gebaut: die Basislinie gemessen — 5 Komponenten, 0 Furche-Zellen) | 2026-10-28 (Entwurf, Claude Code — nach der Sichtung der 14.5-Bilder)
---
# P10.5 Block 14.6 — Der Körper: aus Inseln wird eine Gehirnkarte

> **Auftrag (Nikinger, 2026-10-28, nach den Bildern `p105_b14_karte_0{1,2,3}`):** „Die Screenshots
> sind technisch richtig … aber ehrlich: das sieht eher nach getrennten Inseln aus als nach einer
> echten Gehirnkarte." Entschieden: **Option B** — ein zusammenhängender Körper, das Layout bleibt.
> Plan von Claude Code, Bau durch opencode (M3.1 Flash).

## §0 Befund (gemessen, nicht vermutet)

- Die Zeichenregel C2 (Block 8) ist richtig: jede Rasterzelle gehört dem Space ihres **nächsten**
  Knotens, eine **Furche** liegt dort, wo ein 4-Nachbar einem anderen Space gehört
  (`graph.js :: computeLobes()`, Z. ~1440).
- Die **Körpermaske** ist aber nur `LOBE_REACH` = **48 px** um jeden Knoten (Z. 175).
- Das Layout aus Block 14 legt die Spaces **auseinander**: Schwerpunkte **≥ 346 px** voneinander
  (Head, Befund 14.2). ⇒ die Lappen berühren sich nie: **5** getrennte Inseln, **0** Furche-Zellen
  (C2-Probe auf dem Produktionslayout: 62 → 0).
- Das Layout ist **abgenommen** (P10.5-65–69, 71). Es bleibt. Falsch ist nur, **wie** der Körper
  gezeichnet wird.

## §1 Das Prinzip — schließen, nicht verschieben

Morphologisches **Schließen** der Körpermaske: erst um `D` **wachsen** lassen, dann um `D`
**schrumpfen**. Lücken schmaler als ~2·`D` füllen sich, der **äußere** Rand bleibt (fast) wo er
ist. Die gefüllten Zellen bekommen — wie jede Zelle heute — den Space ihres nächsten Knotens; die
Grenze zweier Spaces im gefüllten Streifen wird damit **von selbst** zur Furche. **Kein Knoten
bewegt sich.**

Warum nicht die Spaces zusammenziehen (Option A): das öffnet die abgenommenen Zellen 66/67/68/71
wieder, und enge Spaces bringen die überlappenden Beschriftungen zurück. Warum keine feste
Gehirn-Silhouette (Option C): größter Umbau, und die Karte wäre nicht mehr „zufällig, aber
geordnet".

## §2 Entwurf

### 2.1 Der Algorithmus (nur in `computeLobes()`)

1. **Raster polstern:** der Weltbereich ist heute „Knoten ± `LOBE_REACH`". Neu: „Knoten ±
   (`LOBE_REACH` + `LOBE_CLOSE_PX` + eine Zelle)". Ohne Polster schneidet das Schrumpfen den Rand
   des äußersten Lappens ab (das Raster endet dort, wo der Lappen endet — derselbe Rand, an dem
   14.5 den Konturfehler gefunden hat).
2. **Wachsen:** eine Zelle ist im gewachsenen Satz, wenn ihr Mittelpunkt höchstens `LOBE_REACH +
   LOBE_CLOSE_PX` vom nächsten Knoten entfernt ist. Der nächste Knoten (`best`/`bestD`) wird heute
   schon für **jede** Zelle berechnet — nur der Vergleich `bestD > reachSq` bekommt die neue
   Schwelle.
3. **Schrumpfen:** eine Zelle bleibt, wenn ihr euklidischer Abstand (in Zellen) zur nächsten Zelle
   **außerhalb** des gewachsenen Satzes **> `LOBE_CLOSE_PX / cell`** ist. Dazu eine exakte
   Distanztransformation auf dem Raster (Felzenszwalb–Huttenlocher, zwei 1-D-Durchläufe der
   quadrierten Abstände, O(Zellen)), als **eigene reine Funktion** neben `erode()`. Eine
   Chamfer-Näherung ist **nicht** zulässig: ihre Abweichung (bis ~8 %) erzeugt achteckige Ränder.
4. **Körper = geschlossener Satz ∪ heutige Maske** (`bestD ≤ reachSq`). Die Vereinigung fängt
   die Rasterungs-Kante ab: ohne sie könnte das Schließen eine Zelle der heutigen Maske verlieren.
5. `spaceOf` für jede Körperzelle = Space des nächsten Knotens (wie heute). **Furche, Kontur
   (`traceContour()`), innere Kontur (`erode(…, LOBE_INNER_CELLS)`), Füllung bleiben
   unverändert.**

### 2.2 Die Konstante

```js
const LOBE_CLOSE_PX = <Wert aus 14.6.1>;  // Schließ-Radius der Körpermaske (Plan 14.6 §2.1) — 0 = die Inseln von Block 14
```

**`LOBE_CLOSE_PX = 0` muss das heutige Bild exakt ergeben.** Mit `0` (Polster nur eine Zelle,
Schrumpfen um 0) ist der Körper die heutige Maske. Das ist die Regressionsprobe **und** der
Gegenlauf. Gemessen wird es an den Lappen-Konturen der Bilder-Probe (`je_lappe`): die
Weltkoordinaten der Konturpunkte sind **identisch** — das Polster verschiebt `minX`/`minY` um
ganze Zellen, die Zellgrenzen bleiben auf demselben 8-px-Gitter, also gibt es **keinen**
erlaubten Versatz. **Einzige Ausnahme:** schiebt das Polster die Spanne über `LOBE_MAX_CELLS`,
ändert sich die Zellgröße — dann **berichten**, nicht stillschweigend hinnehmen.

### 2.3 Was bleibt — nicht anfassen

Knotenpositionen, Layout (`computeRegions()`, `seedInitialPositions()`, `applyForces()`, alle
Block-14-Konstanten), `fitView()` und `FIT_MARGIN` (= 56), `traceContour()`/`chainEdges()`/
`simplifyLoop()`/`traceSmooth()` (Wächter `tests/test_lobe_kontur_geschlossen.py`),
`drawLobes()`, Farben/Deckungen, Bahnen, Zellen, Beschriftungen, `nodeColor()`, Server-Code,
`app.css`, `docs/UPDATE_LOG.md`.

### 2.4 Der Rand (Plan Block 14 §2.5)

Das Schließen mit einer Kreisscheibe bleibt in der konvexen Hülle der Maske. Damit reicht die Kontur
weiterhin höchstens `LOBE_REACH + cell/2` = **52 px** über den äußersten Knoten, und `FIT_MARGIN = 56`
genügt. **Das wird gemessen, nicht angenommen:** die Bilder-Probe schreibt den Reach je Seite.
**> 52 px oder Luft ≤ 0 ⇒ STOPP**, nicht `FIT_MARGIN` ändern, sondern berichten.

### 2.5 Kosten und Rasterdeckel

`computeLobes()` läuft **einmal** nach dem Einschwingen (`settle()`, Z. ~861) und nach jedem
Drag-Ende (Z. ~1945) — nie pro Frame. Das Polster vergrößert das Raster: bei `D` = 200 px ist die
Spanne ≈ 1240 + 2·(48 + 200 + 8) px ⇒ **> 200 Zellen** je Achse. `LOBE_MAX_CELLS` (= 200, Z. 176)
vergröbert dann die Zelle (> 8 px, die Kontur wird stufiger).
**Messen:** Zellgröße und Zeit von `computeLobes()` bei **152** und **201** Knoten — die Zeit per
`performance.now()` um den Aufruf, **im Messpflaster** (§4, 14.6.0), nicht im Produktcode.
**Grenze (Startwert, Nikinger kann ändern):** ≤ **50 ms** bei 201 Knoten.
`LOBE_MAX_CELLS` darf **nur** angehoben werden, wenn die Zeitgrenze dann noch hält — mit Messung im
Bericht.

## §3 Entscheidung des Nikingers

**E1 — der Wert von `LOBE_CLOSE_PX`.** Nach 14.6.1 liegen Bilder je Variante vor. Der Nikinger wählt
nach Auge.
**Delegiert er die Wahl** („nimm den Standard"), gilt: der **kleinste** Wert des Rasters, bei dem
der Körper **eine** Komponente ist und jeder Space **genau einen** Lappen hat. Gibt es keinen
solchen Wert: STOPP, berichten.

## §4 Schritte (je Schritt **eine** opencode-Session, ein Commit, Head im selben Commit)

| Schritt | Inhalt | Fertig, wenn |
|---|---|---|
| **14.6.0** ✅ 2026-10-28 | **Messung zuerst:** die Bilder-Probe `p105_b14_karte_bilder.py` bekommt die Zelle `koerper` (§5) — gemessen über ein **Messpflaster in einer Kopie** von `graph.js` (Muster `p105_b8_c2_probe.mjs` Z. ~95, `globalThis.__furrowCells`; **kein** Haken im Produktcode). **Zwei Durchgänge je Lauf:** die **Bilder** und der Rand (Reach/Luft) aus den **ungepatchten** Dateien (die Bilder im Repo zeigen Produktcode — `test_b14_karte_bilder.py`), die `koerper`-Zahlen und die `computeLobes()`-Zeit aus einem **eigenen**, gepatchten Durchgang. Dazu `LOBE_CLOSE_PX` in `BLOCK14_KONSTANTEN` (`p105_b14_layout_probe.py` Z. 253), damit `--konstante=` es meldet. **Gegen den heutigen Code.** | `koerper` ist **rot** an der Basislinie: **5** Komponenten, **0** Furche-Zellen (das ist der gemessene Befund aus §0). Alle übrigen Zellen der Probe unverändert. **✅ erfüllt** — die Anmerkungen unten. |
| **14.6.1** ✅ 2026-10-28 | Der Algorithmus (§2.1) mit `LOBE_CLOSE_PX = 0` (= heute, §2.2) — dann die **Varianten** `--konstante=LOBE_CLOSE_PX=` **0 · 80 · 120 · 160 · 200 · 240**, je mit `--bilder=~/p105_b14_6_varianten/<D>/` (**außerhalb** des Repos). | Mit `0` ist das Bild gleich dem von heute (§2.2). Tabelle je Variante: Komponenten, Lappen je Space, Furche-Zellen, Reach je Seite, Luft, Zellgröße, `computeLobes()`-Zeit (152/201 Knoten). **STOPP — Bericht an den Nikinger (E1).** Commit mit `LOBE_CLOSE_PX = 0`. **✅ erfüllt** — die Bilder bei `0` sind **byteweise identisch** mit den drei im Repo; die Tabelle und der Befund stehen unten. |
| **14.6.2** ✅ 2026-10-28 | Den gewählten Wert setzen (Kommentar „gewählt vom Nikinger am <Datum>, gemessen in 14.6.1"). C2-Wächter: neue Messung `koerper` in `p105_b8_c2_probe.mjs` an einem **festen** Eingang (3 Gruppen, Abstand so, dass sie sich bei `LOBE_CLOSE_PX = 0` **nicht** berühren — Muster `FESTE_POSITIONEN`, Z. ~407) + Gegenlauf `koerper` (`LOBE_CLOSE_PX` → 0) in `tests/test_graph_c2.py`. Die alte Furche-Messung bleibt. | `koerper` grün; der Gegenlauf `koerper` macht **genau diese** Messung rot, die acht alten Gegenläufe bleiben rot an genau ihrer Messung. |
| **14.6.3** | Belege: `p105_b14_layout_probe.py` neu (Normalfall) · `p105_b14_karte_bilder.py` neu (Bilder ersetzen `docs/screenshots/p105_b14_karte_0{1,2,3}_*.png`, dieselben Namen) · `p105_b8_karte_probe.py` neu · volle Suite, `scripts/doc_health.py`, `phase5_ui/scripts/ui_budget.py`. Doku: §4-Zeile hier, Head (Modulstatus, Abnahmezeile **P10.5-72**, Summe, Session-Block), INDEX. | Die Knotenpositionen der Layout-Probe sind **gleich** zu `p105_b14_layout_probe.json` (alle Zellen gleich bis auf `zeit`) ⇒ das Layout ist unberührt, die sechs Gegenläufe müssen **nicht** neu. `koerper` grün mit dem gewählten Wert. Suite grün, `doc_health` 0, `ui_budget` grün. |
| 14.6.4 | **Claude Code:** Update-Log-Zeile anpassen (sie sagt heute „eigene Insel"), Sichtung **P10.5-70** neu beim Nikinger | — |

### Die Schritte 14.6.0 bis 14.6.4 — die Anmerkungen

#### 14.6.1 ✅ 2026-10-28 — der Algorithmus und die sechs Varianten

**Der Algorithmus steht** (§2.1): das Polster (`LOBE_REACH` + `LOBE_CLOSE_PX` + eine Zelle),
das **Wachsen** (dieselbe Schleife wie bisher, nur die Schwelle `LOBE_REACH + LOBE_CLOSE_PX`),
das **Schrumpfen** (die **exakte** euklidische Distanztransformation — Felzenszwalb–Huttenlocher,
zwei 1-D-Durchläufe) und der **Körper** = geschlossener Satz ∪ heutige Maske. **Kein Knoten
bewegt sich**, die Kontur-/Furchen-/Beschriftungslogik ist unberührt.

**Die Regressionsprobe ist erfüllt:** bei `LOBE_CLOSE_PX = 0` sind die drei Bilder **byteweise
identisch** mit den drei im Repo (`cmp` sagt: identisch), und die Konturpunkte der Lappen
(`je_lappe`) sind dieselben. Das Polster verschiebt das Raster um **ganze Zellen** — die
Zellgrenzen bleiben auf demselben 8-px-Gitter.

**Die Tabelle** (`probes/p105_b14_6_varianten_messung.json`, der Beleg; die Bilder liegen
**außerhalb** des Repos unter `~/p105_b14_6_varianten/<D>/`):

| `LOBE_CLOSE_PX` | Komponenten | Furche-Zellen | Paare | Raster | Zellgröße | Zeit 152 / 201 | Reach max | Luft min | Kriterien |
|---|---|---|---|---|---|---|---|---|---|
| 0 | **5** | 0 | 0 | 158 × 127 | 8,00 px | 13,3 / 34,8 ms | 48,4 px | 7,2 px | rot (Basislinie) |
| 80 | 3 | 40 | 2 | 178 × 147 | 8,00 px | 21,1 / 42,6 ms | 48,4 px | 7,2 px | rot |
| 120 | 3 | 64 | 2 | 188 × 157 | 8,00 px | 28,8 / 34,2 ms | 48,4 px | 7,2 px | rot |
| **160** | **1** | 146 | **4** | 198 × 167 | 8,00 px | **28,4 / 36,3 ms** | 48,4 px | 7,2 px | **grün** |
| 200 | 1 | 234 | 5 | 200 × 171 | 8,30 px | 36,3 / 33,3 ms | 48,6 px | 6,5 px | grün |
| 240 | 1 | 247 | 6 | 200 × 172 | 8,71 px | 35,6 / 33,6 ms | **52,8 px** | 2,8 px | rot (Reach > 52) |

**Drei Befunde, die die Wahl tragen.**
1. **Der kleinste Wert mit *einer* Komponente ist 160.** 80 und 120 ergeben **drei** Komponenten
   (nur `alpha`|`delta` und `alpha`|`beta` verbinden sich) — das deckt sich mit der Basislinie:
   die gewachsenen Masken überlappen erst, wenn `2 · (48 + D) ≥ 183`, also ab **43,5 px**; bis
   120 reicht das für **zwei** Nachbarschaften, ab 160 für **alle vier**.
2. **Ab 200 werden die Lappen von der Furche aufgefressen.** Der Reach misst die **gezeichnete**
   Kontur, und die Furche-Zellen gehören zu **keinem** Lappen: bei 200 wird der Reach **rechts
   −3,9 px** (die Kontur liegt **innerhalb** des Knoten-Umrisses), bei 240 **oben −89,5 px**.
   Das ist ein **Verlust**, den die Abnahme-Kriterien des Plans (§5) **nicht** fangen — sie
   prüfen den Reach nur als **Obergrenze**. Der Plan §5 ist damit an dieser Stelle zu
   schwach; die Wahl von **160** ist durch den **negativen** Reach begründet, nicht durch die
   Obergrenze allein.
3. **Die Zeit ist kein Selbstgeschätzt, aber ein einzelner Aufruf ist verrauscht.** Der erste
   Lauf (ein Aufruf je Messpunkt) meldete 24,2 / 35,0 ms bei `D = 0` und **50,7** / 47,2 ms bei
   `D = 160` — die **größere** Variante `D = 200` (Raster 200 × 171) war mit **29,8** ms
   *schneller*: das ist kein Trend, das ist Rauschen (JIT, GC, Last). Das Messpflaster misst
   deshalb jetzt **fünf** Aufrufe und der **Median** trägt die Entscheidung. Der Median bleibt
   bei allen sechs Varianten unter der Grenze von **50 ms** (der höchste: **36,3 ms** bei 201
   Knoten).

**Der Befund, den der Plan nicht erwartet hat:** die **Zeitgrenze** (50 ms bei 201 Knoten) war
**vor** dem Schließen schon zu **70 %** ausgeschöpft (34,8 ms bei `D = 0`). Das Schließen
kostet **+1,5 ms** (36,3 ms bei `D = 160`) — die Reserve ist echt, aber sie war knapper als
vermutet.

**STOPP — Bericht an den Nikinger (E1).** Die Bilder liegen unter
`~/p105_b14_6_varianten/<D>/` (**außerhalb** des Repos). Der **Standard** nach §3 wäre **160**
(der kleinste Wert mit einer Komponente und einem Lappen je Space). Der Commit trägt
`LOBE_CLOSE_PX = 0` — gesetzt wird der Wert in **14.6.2**.

#### 14.6.2 ✅ 2026-10-28 — der Wert steht, der Wächter beißt

**E1 ist entschieden: `LOBE_CLOSE_PX = 160`.** Der Nikinger hat am 2026-10-28 die **Standardregel
des Plans** (§3) entschieden: der kleinste Wert, bei dem der Körper **eine** Komponente ist und
jeder Space **einen** Lappen hat. Der Wert steht im Produktcode mit dem Kommentar
„gewählt vom Nikinger am 2026-10-28, gemessen in 14.6.1".

**Der Wächter `koerper` (neue Messung in `p105_b8_c2_probe.mjs`).** Die alte Furche-Messung
bleibt; neu ist eine **neunte** Messung mit einem **zweiten festen Eingang**
(`KOERPER_POSITIONEN`): drei Gruppen mit den Abständen **190 px** (alpha|beta), **130,8 px**
(alpha|gamma) und **161,2 px** (beta|gamma) — alle **größer** als zwei Reach-Radien (96 px),
damit die Masken bei `LOBE_CLOSE_PX = 0` getrennt bleiben, und alle **kleiner** als zwei
Schließ-Radien (416 px), damit sie bei 160 verschmelzen.

**Warum ein zweiter Eingang (der Plan verlangt dieselbe Art von Eingangs-Fixierung).** Die
alten `FESTE_POSITIONEN` lassen alpha und beta **berühren** (30 px) — dort gäbe es bei *jeder*
Schließung einen Körper, und der Gegenlauf (`LOBE_CLOSE_PX` → 0) bliebe **grün**, ohne dass der
Fehler wiederhergestellt wäre. Genau das ist die Fehlerklasse, die dieser Ordner zweimal
gesehen hat: eine grüne Messung ohne Gegenlauf beweist, dass der Wächter läuft, nicht dass er
die richtige Sache misst.

**Die Zahlen (Normalfall):** `components` **1**, `lobes` **3**, `furrow_cells` **53** → grün.
**Der Gegenlauf `koerper`** (`LOBE_CLOSE_PX` → 0): `components` **3**, `furrow_cells` **0** →
rot — und **nur** diese Messung; die acht alten bleiben grün (der Anker des Gegenlaufs ist die
**Konstante**, und ein fehlender Anker bricht die Probe **laut** ab).

**Datierte Korrektur zum Plan (§4, Schritt 14.6.2).** Der Plan verlangt die neue Messung „an
einem **festen** Eingang (3 Gruppen …) — Muster `FESTE_POSITIONEN`". Das **Muster** ist
übernommen (ein fester, in der Ablage liegender Positionssatz), aber die **Positionen** sind
**andere**: die alten lassen zwei Gruppen berühren. Beide Sätze stehen jetzt nebeneinander im
Probe-File (`FESTE_POSITIONEN` für die acht alten Messungen, `KOERPER_POSITIONEN` für die
neue).

**Der Browser bestätigt den Wert (ein Lauf, die Bilder außerhalb des Repos).** 201 Knoten:
`components` **1**, `lobes_je_space` **1** je Space, **146** Furche-Zellen, **4** Paare,
Reach **47,9 / 44,1 / 48,4 / 44,6 px** (Grenze 52), Luft **7,2 / 10,7 / 82,9 / 85,6 px**,
Zeit **29,7 ms** (152) und **43,0 ms** (201 Knoten, Median aus fünf Aufrufen — Grenze 50).
Die Sichtprüfung des Bildes bestätigt: **ein** zusammenhängendes, gehirn-ähnliches Gebilde mit
Lappen und Furchen.

#### 14.6.0 ✅ 2026-10-28 — die Basislinie, gemessen

**Der Befund aus §0 ist bestätigt — und er ist genau der erwartete.** Der Körper besteht aus
**5** 4-zusammenhängenden Komponenten (die fünf Inseln), es gibt **0** Furche-Zellen, und **kein**
Paar von Spaces liegt an einer Furche. Die Zelle `koerper` ist damit **rot** — wie der Plan sie
für die Basislinie verlangt. **Kein Produktcode angefasst.**

| Zahl | Wert |
|---|---|
| Komponenten (152 Knoten) | **5** (Größen 1815 / 1670 / 1656 / 1651 / 1538 Zellen) |
| Lappen je Space | **1** (jeder Space genau einer) |
| Furche-Zellen | **0** |
| Paare mit Furche | **0** |
| Körperzellen | 4360 (Raster 156 × 125, Zellgröße **8 px**) |
| kleinster Abstand zweier Spaces | **183,0 px** |
| `computeLobes()` | **20,1 ms** (152 Knoten) · **35,0 ms** (201 Knoten) — Grenze 50 ms |

**Drei Zahlen, die die Wahl des `LOBE_CLOSE_PX` (E1) entscheiden.**
1. **Der kleinste Abstand zweier Knoten verschiedener Spaces ist 183,0 px.** Die gewachsenen
   Masken (Radius `LOBE_REACH + D`) überlappen erst, wenn `2 · (48 + D) ≥ 183` — also ab
   **D = 43,5 px**. Der kleinste Wert, der die Inseln überhaupt verbinden kann, liegt damit
   **oberhalb** von 40 px; die Variantenliste (80 … 240) deckt das ab.
2. **Die Zeitgrenze ist kein Selbstgeschätzt.** Der **heutige** Code braucht bei **201** Knoten
   **35,0 ms** von den erlaubten 50 ms. Das Schließen kommt **obendrauf** (die
   Distanztransformation kostet zwei Durchgänge über das Raster) — die Reserve ist echt, aber
   **nicht groß**.
3. **Die Rasterzelle wächst mit `D`** (der Deckel `LOBE_MAX_CELLS` = 200 gilt für die
   **gepolsterte** Spanne): bei 201 Knoten sind es heute **8,23 px** — die Spanne ist dort
   **schon gedeckelt**. Jede Variante muss deshalb die **Zellgröße** mitprotokollieren (die
   Kontur wird mit größerer Zelle **stufiger**).

**Zwei Befunde am Werkzeug, die sonst stillschweigend falsch gemessen hätten.**
- **Der Wegwerf-Server „beendete sich nicht".** Die PID bleibt als **Zombie** stehen, wenn der
  Elternprozess sein Kind nicht abräumt — `os.kill(pid, 0)` sagt trotzdem „lebt". Der Stopp
  wartete **zehn Sekunden** auf einen Prozess, den es nicht mehr gab, und meldete dann
  fälschlich „SIGKILL". Der Stopp prüft jetzt den **Zustand** in `/proc/<pid>/stat`
  (`p105_b14_layout_probe.py :: _lebt()`).
- **Die Bilder sind byteweise identisch geblieben.** Der Lauf hat die drei Bilder neu erzeugt —
  **unverändert** (`git` sagt nichts). Das ist der Beweis, dass der Messpflaster-Durchgang das
  Bild **nicht** verändert: die Bilder im Repo zeigen den **Produktcode**.

**Datierte Korrektur zum Plan (§4, Schritt 14.6.0).** Der Plan verlangt, `LOBE_CLOSE_PX` in
`BLOCK14_KONSTANTEN` zu tragen, „damit `--konstante=` es meldet". Die Konstante steht aber
erst ab **14.6.1** in `graph.js` — dort kommt der Algorithmus. `_konstanten_werte()` liest die
Werte aus dem **echten** Quelltext (fehlende Konstanten fehlen im Beleg, ohne dass ein Lauf
still scheitert), und `_konstanten_patch()` sagt **laut** Bescheid, wenn jemand einen Wert
setzen will, den es noch nicht gibt. Der Widerspruch ist damit **ohne Nebenwirkung** — und
verschwindet von selbst in 14.6.1.

## §5 Abnahme — neue Zeile P10.5-72 (und P10.5-70 neu)

**P10.5-72 — die Karte ist ein Körper.** Bei 5 Spaces (30/32/30/30/30 = 152 Items, Saat der
Abnahme) gilt alles Folgende:
- die Körperzellen aller Spaces bilden **eine** 4-zusammenhängende Komponente — gezählt **mit**
  den Furche-Zellen (sie gehören zum Körper, nur zu keinem Lappen; ohne sie zerfiele der Körper
  bei **jedem** Wert in 5 Teile und die Zelle wäre nie grün);
- jeder Space hat **genau einen** Lappen — gezählt über seine Zellen **ohne** Furche (eine
  4-zusammenhängende Komponente);
- zwischen je zwei Spaces, deren Lappen sich berühren, liegt eine Furche (> 0 Zellen), und mindestens
  **4** solcher Paare existieren;
- die Kontur reicht ≤ 52 px über den äußersten Knoten, mit Luft > 0 px zur Leinwand;
- die Knotenpositionen sind gleich zum Stand 14.5;
- `computeLobes()` braucht ≤ 50 ms bei 201 Knoten.

**Gegenlauf `koerper`** (`LOBE_CLOSE_PX` → 0) macht **genau diese** Zelle rot.

**P10.5-70** (Sichtung) bleibt ⬜. Gesichtet werden die **neuen** Bilder. Die Summe im Head wird
**72 Zeilen**, und `tests/test_head_rules.py` prüft sie gegen Head und `ABNAHME_ARCHIVE.md`.

## §6 Startauftrag — Block 14.6 · Ausführer (opencode, M3.1 Flash)

**Vorher:** `limit.context` ≤ 400.000 prüfen · `git status` sauber · Blockbasis = HEAD · diesen
Plan ganz lesen, dazu Block-14-Plan §2.5 und den Session-Block im Phase-Head.

**Erlaubte Pfade:** `phase5_ui/webui/static/js/graph.js` (**nur** `computeLobes()`, eine neue reine
Distanz-Funktion daneben, die Konstante `LOBE_CLOSE_PX`; `LOBE_MAX_CELLS` nur nach §2.5) ·
`phase10_5_finishing/probes/**` · `phase10_5_finishing/tests/**` · Doku: dieser Plan (§4),
`phase10_5_finishing/CLAUDE.md`, `phase10_5_finishing/SESSIONS_ARCHIVE.md` (nur über das Skript),
`docs/INDEX.md`.
**Nicht:** alles aus §2.3, `FIT_MARGIN`, `docs/UPDATE_LOG.md` (14.6.4, Claude Code).

**Anker (Stand dieses Plans):**

| Was | Wo |
|---|---|
| Lappen-Konstanten | `graph.js` Z. 174–178 |
| `FIT_MARGIN` | `graph.js` Z. 283 |
| `settle()` | `graph.js` Z. ~861 |
| `computeLobes()` | `graph.js` Z. 1440 |
| `erode()` / `traceContour()` | `graph.js` direkt darunter |
| Drag-Ende | `graph.js` Z. ~1945 |
| `BLOCK14_KONSTANTEN` | `p105_b14_layout_probe.py` Z. 253 |
| `--konstante` / `--bilder` | `p105_b14_karte_bilder.py` (Docstring) |
| Messpflaster / `FESTE_POSITIONEN` | `p105_b8_c2_probe.mjs` Z. ~95 / ~407 |

**Regeln:**
- Proben **nur** an der Wegwerf-Instanz: eigener Port, tmp-`DATA_ROOT`, tmp-`auth.sqlite3`,
  Playwright aus `~/.claude-code-tools/e2e-venv`.
- Gestoppt wird **nur** über die PID-Datei. **Nie** `pkill -f`, **nie** `systemctl` (Hard Rule 9).
- Umgebung ohne `SHAREFYX_*`/`SFX_*`.
- Ein Commit je Schritt, Head im selben Commit (Hard Rule 8). Volle Suite grün vor dem Commit.
- **Session-Block:** den neuen Block **ans Ende** des Heads schreiben, **dann**
  `scripts/rotate_session_block.sh phase10_5_finishing`. Das Skript hält den **untersten** Block für
  den neuesten (Fund 2026-10-28).
- **INDEX:** die Reserve ist 3.000 B unter dem Softcap (`test_register_archive.py`). Fehlt Luft,
  rotiert `scripts/rotate_index_updates.sh` einen `updated:`-Faden.

**STOPP-Punkte:** nach 14.6.1 (E1) · Reach > 52 px oder Luft ≤ 0 · `computeLobes()` > 50 ms bei 201
Knoten · kein Wert erfüllt die Standardregel (§3) · eine Layout-Zelle ändert sich in 14.6.3.

**Bericht je Schritt:** die Zellen der Probe als JSON, die Varianten-Tabelle (14.6.1) und die
Gegenläufe (14.6.2). Nur Rohdaten, keine Bewertung — die Auswertung des Ausführers macht Fleet.
