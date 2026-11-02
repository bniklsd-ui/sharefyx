---
status: live
purpose: Addon zu Block 18 — die „ferne Insel" (ein Punkt / eine kleine Gruppe weit draußen, eigener Umriss). Reproduziert auf v4.0.0 und HEAD (Node + Browser), Mechanismus mit Code-Ankern, Lösungsvorschlag (Abstoßung mit Mindestabstand), Zellen- und Gegenlauf-Entwurf. Kein Produktcode geändert.
read-when: bevor 18.2 (Ausreißer) weitergebaut oder die Zelle `ausreisser` neu gefasst wird; wenn auf der Live-Karte ein Punkt in eigenem Umriss weit draußen liegt
detail: L2
up: ./phase10_5_block18_live_fixes_plan.md
down:
  - ../../phase5_ui/webui/static/js/graph.js   # applyForces() :1033, integrate() :1098, computeRegions() :777/:795
  - ./phase10_5_block14_7_plan.md              # die Geometrie (Hex-Anker, LOBE_SCALE), auf der die Saat liegt
updated: 2026-11-02 (Addon-Agent, Claude Code: Reproduktion Node + Browser auf v4.0.0 und HEAD, zwei Saaten; Mechanismus; Vorschlag ε = 6 px; Zelle `insel` + Gegenlauf `tritt`; Fund: Gegenlauf `schleuder` würde nach dem Vorschlag zahnlos)
---
# Addon Block 18 — die ferne Insel

> Auftrag (Koordinator, 2026-11-02): reproduzieren, erklären, Lösung vorschlagen — **nichts bauen**. Gemessen an
> **Kopien** von `graph.js` (Node-Harness und Wegwerf-Instanz); Arbeitsbaum, Belege und Tests unberührt. Experiment-
> Skripte liegen **außerhalb** des Repos unter `/tmp/insel/` (flüchtig — die Befehle stehen unten zum Nachbauen).

## 1. Ergebnis (BLUF)

**Zwei Mechanismen mit einer Wurzel.** Die Abstoßung in `applyForces()` ist **fast singulär**
(`dist2 = dx² + dy² + 0.01`, Kraft `2700 / dist2` im eigenen Space). Kommen sich zwei Knoten auf wenige Pixel nahe —
schon in der **Saat** (überlappende Ordner-Inseln) oder im Durchflug —, bekommt einer einen **Tritt**, rollt mit
`DAMPING` weiter und bleibt liegen, weil `alpha` abklingt, bevor die Anker-Gravitation ihn zurückholt.

| | v4.0.0 (live, `2eb697f`) | HEAD (`8dc106c`, Stern + `MAX_SPEED`) |
|---|---|---|
| **Gruppe** fliegt weg (Bild 2: ≈ 6–12 Knoten eines Space, dichter Knäuel, ein langer Bogen) | **ja** — 3–13 % der Läufe im Tag-/Ordner-Zustand, Lücke 300–8.000 px | **nein** — 0 von 720 Läufen |
| **Einzelpunkt** in eigenem Umriss | **ja** — in **allen** Zuständen, auch „aus"; Lücke bis > 10.000 px | **ja, gedeckelt** — 13–70 % der Läufe je Form, Lücke **≤ 1.052 px**, auch im Zustand „aus" |

* **Bild 2 des Nikingers ist N1 auf v4.0.0 — in HEAD behoben**, noch nicht deployt. Sicherheit: **hoch** für den
  Mechanismus (Node = Browser auf die Kommastelle, §2.1), **mittel** für „genau dieses Bild" (seine Daten kenne ich nur
  als Form).
* **Ein zweiter Fehler überlebt HEAD:** der Einzelpunkt-Tritt. `MAX_SPEED = 600` deckelt ihn, beseitigt ihn nicht.
  Auf der 18.0-Saat **selbst** liegt einer: `itm_0000002f` (eigener Space alpha, Grad 0), **490,7 px** vom Körper,
  eigener Umriss, Zustand **„aus"**, nach „Layout zurücksetzen" byte-gleich wieder da (Browser, §2.2). Die 18.0-Zelle
  `schleuder` (≤ 1.300 px vom Median) sieht ihn nicht, die Zelle `ausreisser` misst nur `epsilon`.
* **Vorschlag:** Mindestabstand in der Abstoßung — `dist2 = Math.max(dx² + dy² + 0.01, REPULSION_MIN_DIST²)`,
  `REPULSION_MIN_DIST = 6`. Gemessen (Node): Tritt-Inseln **40 % → 0 %** auf 6 Live-Formen (720 Läufe), auf 2
  Stressformen 52,5 % → 1,3 % — und dieser Rest ist **nur** der Ein-Item-Space auf seinem Hex-Platz (A1, ≤ 379 px),
  kein Tritt mehr. Browser: Block-14-Probe **6/6 grün**, 152-Item-Szene **byte-gleich** (P10.5-65/68 unberührt),
  18.0-Saat in allen Zuständen **eine** Komponente. ε = 4 reicht auf den Live-Formen auch, lässt auf der Stressform
  `dense` aber einen Tritt mit ≈ 400 px Lücke stehen (§4.1). Die 18.0-Saat „aus" ändert sich zwangsläufig — sie
  **enthält** den Fehler (§4.3).

## 2. Reproduktion

### 2.1 Werkzeug und Gegenprobe Node ↔ Browser

`/tmp/insel/harness.mjs` lädt eine Kopie von `graph.js` (HEAD aus dem Arbeitsbaum, v4.0.0 per
`git show 2eb697f:phase5_ui/webui/static/js/graph.js`) mit dem DOM-Shim von `probes/p105_b14_layout_probe.mjs` und hängt
`__sim()` an: Payload wie `loadGraph()`, `rebuildImplicitEdges()`, `seedInitialPositions()`, dann die Schleife aus
`runSimulation()` (129 Ticks), danach `computeLobes()`. **Insel-Maß = Komponenten der Körpermaske** (`koerper` aus
`computeLobes()`, 4-Nachbarschaft) — der Umriss, den der Nikinger sieht. Insel = jede Komponente außer der größten;
ihre **Lücke** = kleinster Knotenabstand zur größten.

**Gegenprobe:** HEAD, 18.0-Saat, weitester Knoten „aus"/„Tags"/„Ordner"/„beide" Node **973 / 662 / 919 / 596 px** —
Browser-Beleg 972,8 / 661,7 / 918,9 / 595,6; v4.0.0 Tags Spitze **28.104 px/Tick in Tick 5** (Plan §5.3). v4.0.0 als
Patch auf HEAD (`MAX_SPEED` → 1e9, `starEdges()` → Clique mit `seen`) ist in Node **positionsgleich** zu v4.0.0
(Abweichung 0,0 px, 5 Saaten × 4 Zustände) — so läuft v4.0.0 im Browser.

### 2.2 Browser (Wegwerf-Instanz), 18.0-Saat

`cd <repo> && env -u SHAREFYX_SYSTEMCTL .venv/bin/python /tmp/insel/browser_insel.py <head|v400|eps4> /tmp/insel/br_<v>_b18.json`
— Server, Konto und Stopp aus `p105_b14_layout_probe.py` (eigener Port, tmp-`DATA_ROOT`/`auth.sqlite3`, TLS, Stopp über
die PID-Datei), Saat `p105_b18_karte_messung.spec()`, deren Messpflaster + ein Körper-Haken; Film-Startbild per
`add_init_script` unterdrückt. Je Zustand: Schalter setzen, „Layout zurücksetzen", einschwingen, messen. `pinned_beim_start` = 0.

| Zustand | HEAD: Komponenten / Insel / weitester | v4.0.0 | Vorschlag ε = 4 |
|---|---|---|---|
| Laden (alles aus) | **2** / `itm_0000002f` alpha, 490,7 px / 972,8 | **2** / dieselbe, 491 px / 973 | **1** / — / 907 |
| aus (Reset) | **2** / dieselbe / 972,8 | **2** / dieselbe / 973 | 1 / — / 907 |
| Tags | 1 / — / 661,7 | **3** / **24 Knoten** (4 Spaces), **1.644 px** + 27 Knoten, 712 px / 2.783, Zoom 50 % | 1 / — / 613 |
| Ordner | 1 / — / 918,9 | 1 / — / 941 | 1 / — / 918 |
| beide | 1 / — / 595,6 | 1 / — / 866 | 1 / — / 606 |
| aus (2. Reset) | **2** / dieselbe, **byte-gleich** / 972,8 | **2** / dieselbe | 1 / — / 907 |

ε = 6 (`browser_insel.py eps6`): **1** Komponente in allen sechs Messpunkten, weitester 905 / 905 / 617 / 919 / 598 / 905 px.

**Zweite Saat, Live-Form mit grauem Fabian-Space** (`live5`, Saat 12, IDs mit Versatz, nur `read:` für `fabian`;
`browser_insel.py <v> … /tmp/insel/grey_live5_12.json`). Node sagte für v4.0.0/Tags eine Gruppe aus **6 Fabian-Knoten
8.161 px** voraus. Der Browser trifft **dieses** Bild nicht (die Rechnung ist chaotisch; die Reihenfolge der Tags aus dem
Store weicht ab, `[VERIFY]`), zeigt aber dieselbe Klasse:

| Zustand | v4.0.0 | HEAD |
|---|---|---|
| Laden / aus / aus2 | 1 Komponente, weitester 1.024 px | 1, 1.024 px |
| Tags | **12** Komponenten: 11 Inseln (1–2 Knoten, Team-Space) bei **491–5.264 px**, weitester 6.352 px, Zoom 50 % | **1**, 1.000 px |
| Ordner | **3**: eine **Gruppe aus 53 Knoten** (50 eines Space + 3) in eigenem Umriss, 363 px, und ein Punkt bei 2.323 px; Zoom 50 % | **1**, 1.040 px |
| beide | 1, 1.037 px | 1, 997 px |

Das Bild „aus" (HEAD) zeigt den Punkt **blau** unten rechts in eigenem Umriss — das ist die Szene, die 18.0 §5.2 (A1)
dem Ein-Item-Space `epsilon` zuschrieb; `epsilon` ist türkis und hängt am Körper. **[2026-11-02, Korrekturhinweis für
§5.2 A1 — nicht von mir eingetragen, `[VERIFY]` am Bild `b18_0_aus.png`, das nicht im Repo liegt.]** Der zweite Reset
zeigt E7: der Punkt **bleibt**, weil Saat (ID-Hash) und Simulation deterministisch sind — kein Speicherrest.

### 2.3 Spur des Tritts, 18.0-Saat, Zustand „aus" (`node /tmp/insel/trace2.mjs`)

| Tick | α | nächster Nachbar von `itm_0000004c` | Abstand | Kraft vom Nachbarn | Schritt |
|---|---|---|---|---|---|
| 6 | 0,416 | `itm_0000005c` (alpha) | 3,8 px | 182 | 70 px |
| 9 | 0,380 | `itm_0000002f` (alpha) | **2,24 px** | **535** | **184 px** |
| 10–13 | 0,37–0,34 | allein (38–80 px) | — | < 1 | 153 / 127 / 104 / 85 px |

Beide werden getreten: `itm_0000004c` endet 973 px vom Median (am Körper), `itm_0000002f` mit 490,7 px Lücke **in
eigenem Umriss**. Spitze 456 px/Tick < `MAX_SPEED` — die Grenze greift nicht; darum ist „aus" in HEAD = v4.0.0.

### 2.4 Formen-Scan (Node), beide Stände (`node /tmp/insel/scan.mjs 30`)

Sechs Formen (`/tmp/insel/shapes.mjs`) × 30 Saaten × 4 Zustände (Reset mit den Schaltern an). Je Saat zufällige Tags
(Pool 40, ≤ 2 je Item, 30 % space-übergreifend; Gruppen > 15 fallen wie im Code weg), Verknüpfungen (jedes 4. Item im
Space, 10 quer), **eigene IDs** und gemischte Knotenreihenfolge (der Browser sortiert nach `store.search()`: Status,
Fälligkeit, `updated` — darum sind Node-Zahlen eigener Saaten **Raten**, keine Einzelfälle). Formen: `live5` (eigener
100 [Ordner 40/20, 40 Wurzel], Team 80 [50], Team 50 [30], **Fabian grau 30 [12]**, klein 3), `fab12folder` (Fabian 12,
alle in einem Ordner; klein 1), `live7` (7 Spaces), `live9` (9 Spaces, Hex-Ring 2), `nofolders`, `sparse` (≤ 1 Tag,
wenige Kanten).

| Form | v4.0.0 Inselquote aus/Tags/Ordner/beide | v4.0.0 größte Lücke | v4.0.0 Gruppen ≥ 5 | HEAD Inselquote | HEAD größte Lücke | HEAD Gruppen |
|---|---|---|---|---|---|---|
| live5 | 73/100/67/87 % | 36.208 px | Tags 10 % (z. B. **6 Fabian-Knoten, 8.161 px**) | 67/57/57/50 % | 909 px | 0 |
| fab12folder | 73/97/73/87 % | 85.091 px | Tags 7 % (10 eines Space, 3.432 px), Ordner 3 % | 70/67/67/47 % | 874 px | 0 |
| live7 | 30/87/27/67 % | 48.503 px | Tags 3 % | 23/30/20/13 % | 1.052 px | 0 |
| live9 | 30/67/33/37 % | 37.027 px | Tags 3 %, beide 3 % (25 Fabian) | 20/37/13/23 % | 882 px | 0 |
| nofolders | **0**/83/**0**/83 % | 29.534 px | Tags 3 % | **0**/33/**0**/33 % | 705 px | 0 |
| sparse | 77/83/83/77 % | 102.838 px | Tags 13 %, beide 3 % | 70/50/63/50 % | 945 px | 0 |

Lesart: (1) **ohne Ordner kein Tritt in „aus"** (`nofolders`) — die Saat-Nähe kommt aus überlappenden Ordner-Inseln
(§3.2); (2) v4.0.0 wirft **Gruppen**, HEAD nie; (3) HEAD wirft **Einzelpunkte** (Grad 0 oder nur Querfedern), ≤ 1,05 km.
**Grenzen der Suche:** 3–9 Spaces, 263–276 Items, ein Tag-Generator, Grad-0-Items nur als Zufall der Saat; nicht
variiert: archivierte Items, gemerkte Ablage mit gepinnten Knoten, Drag, `prefers-reduced-motion` (rechnet dieselbe
Schleife synchron, :999 — gleiche Zahlen erwartet, **nicht gemessen**).

## 3. Erklärung

### 3.1 Der Tritt (beide Stände)

* `applyForces()` :1033 `var dist2 = dx * dx + dy * dy + 0.01;`, :1036 `force = REPULSION_SAME_SPACE / dist2` (2.700,
  :279). Bei 2 px Abstand 675 je Tick, bei 1 px 2.673, bei 0 px 270.000 — `+ 0.01` verhindert nur die Division durch 0.
* `integrate()` :1098 — `x += vx · α`, dann `vx *= DAMPING` (0,85, :134). Ein Tritt `v₀` rollt
  ≈ `v₀ · α₀ / (1 − 0,85 · 0,97)` = **5,7 · v₀ · α₀** weit; an der Grenze `MAX_SPEED` (:141) bei α = 0,5 ≈ **1.700 px**.
* Zurück holt ihn nur die Anker-Gravitation :1087 (`ANCHOR_GRAVITY` 0,02 · α, :295), über `x += v · α` also mit **α²**;
  α klingt mit 0,97 je Tick ab (:150). Ein Knoten mit Grad 0 hat sonst nichts. Gemessen: `itm_0000004c` holt von
  1.024 px (Tick 32) nur 51 px zurück.
* `LOBE_CLOSE_PX = 160` (:202) schließt zwischen zwei Einzelknoten nur bis ≈ 2 · √(208² − 160²) ≈ **266 px** — wer
  weiter liegt, bekommt **eigenen Umriss**.

### 3.2 Woher die Nähe kommt

* **Saat:** `computeRegions()` legt die Wurzel-Insel (`folder: ""`) **auf** den Anker und die Ordner-Inseln bei
  `radius · 0,55 · √((j+1)/F) · 1,5` (:777–778); jede Insel hat eine eigene Goldwinkel-Spirale (:794–800, Radius
  `14 · √t · 1,5`, Jitter ± 4 px aus dem ID-Hash). Die Spiralen **überlappen** — zwei Items verschiedener Inseln können
  fast aufeinander liegen. Beispiel `live5`, Saat 2: `itm_0000003f` liegt in der Saat **1,40 px** neben `itm_0000000d`
  ⇒ Tritt in Tick 0 (v4.0.0 1.162 px/Tick, Lücke 2.244 px; HEAD gedeckelt, Lücke 774 px).
* **Durchflug:** in den ersten Ticks laufen Knoten mit 50–180 px je Tick durch ihre Region — mehr als der Punktabstand
  (≈ 21 px). Begegnungen unter 3 px sind dann häufig (18.0-Saat: Tick 9, §2.3).
* Deterministisch: dieselben Daten ⇒ derselbe Punkt, nach jedem „Layout zurücksetzen" (`clearStoredLayout()` :2050).

### 3.3 Warum v4.0.0 ganze Gruppen wirft (N1) und HEAD nicht

v4.0.0: Tags/Ordner als **Clique** (k(k−1)/2 Federn à 0,05), keine Geschwindigkeitsgrenze. Trifft ein Tritt einen
Knoten der Clique, ziehen die vielen starken Federn die **ganze** Clique mit — sie fliegt als Ball (Bild 2: Knäuel,
eigener Umriss, **ein** langer Bogen = eine Tag- oder Querkante). Spitzen bis 97.000 px/Tick. HEAD: Stern (k − 1
Federn) + `MAX_SPEED` — die Gruppe bleibt; ein getretenes Blatt holt seine Sternfeder zurück. Übrig: Knoten **ohne**
starke Feder (Grad 0 oder nur Querfedern, `CROSS_SPRING_FACTOR` 0,15 ⇒ 0,0075).
**Neu zur Ursache von N1:** v4.0.0 (Clique, keine Grenze) **mit** dem Mindestabstand ε = 4 wirft in 240 Läufen
**keine** Gruppe mehr (Inselquote 0,4 %, Lücke ≤ 411 px). Der Auslöser von N1 ist damit vor allem die singuläre
Abstoßung (der Code-Kommentar :136 nennt sie schon), weniger die Euler-Instabilität „Feder × Grad" aus Plan §5.3.

### 3.4 Für die Sichtung: Umschalten rechnet nicht neu

Die Schalter Tags/Ordner (`init()` :364–373) rufen nur `rebuildImplicitEdges()` und `draw()`. Gerechnet wird beim
Laden (`loadGraph()`, auch nach einem Poll mit neuer Signatur — dann mit den **aktuellen** Schaltern) und bei „Layout
zurücksetzen". Ein Einzelpunkt aus „aus" bleibt beim Einschalten liegen und bekommt **lange gestrichelte Kanten** —
so fällt er „mit Tags/Ordnern" auf, obwohl er im Zustand „aus" entsteht.

## 4. Lösungsvorschlag

### 4.1 Empfehlung: Mindestabstand der Abstoßung (eine Regel, eine Zeile)

```js
// graph.js, bei den Kräfte-Konstanten (:131 ff.)
const REPULSION_MIN_DIST = 6;   // Addon Block 18: unter 6 px rechnet die Abstoßung mit 6 px (gegen den Tritt)
// applyForces() :1033 -- statt `var dist2 = dx * dx + dy * dy + 0.01;`
var dist2 = Math.max(dx * dx + dy * dy + 0.01, REPULSION_MIN_DIST * REPULSION_MIN_DIST);
```

`dist` (:1034) kommt weiter aus `dist2`; so ist es gemessen. Höchste Abstoßung je Paar: 2.700 / 36 = 75 statt 270.000.
Für **jedes Paar ≥ 6 px ist die Rechnung bitgleich** — das Layout ändert sich nur, wo sich zwei Knoten je näher als
6 px kamen.

| Variante (Node) | Inselquote 6 Formen (720) | Stressformen (240)¹ | größte Ferne | Spitze px/Tick | Block-14-Saat |
|---|---|---|---|---|---|
| HEAD | 40 % (Lücke ≤ 1.052) | 52,5 % (≤ 1.020) | 2.100 | 510 | — |
| ε = 4 | 0 % | 2,5 % (≤ 396; 2 davon Tritt) | 1.415 | 326 | byte-gleich |
| **ε = 6** | **0 %** | **1,3 % (≤ 379; nur A1)** | 1.332 | 257 | **byte-gleich** (Browser: 6/6 grün) |
| ε = 8 / 10 / 15 | 0 % | ε = 10: 2,1 % (≤ 384) | 1.328 | 180 | Δ 106 / 128 / 156 px |
| `MAX_SPEED` 200 | 0 % | 2,5 % (≤ 384) | 1.443 | 170 | byte-gleich |
| `MAX_SPEED` 100 | 0 % | 1,3 % (≤ 370) | 1.332 | 85 | byte-gleich |

¹ `dense` (eigener Space 160 Items mit Ordnern 60/40 + 60 Wurzel) und `manyfolders` (5 Ordner à 15). Bei ε = 4 sind
4 der 6 Reste der **Ein-Item-Space** auf seinem Hex-Platz (314–384 px) — **A1** (Ankerabstand, Plan §5.5 Punkt 2),
kein Tritt; die anderen 2 sind **ein** Tritt (`dense`, Saat 24, „aus" und „Ordner"): Begegnung **2,4–3,1 px in Tick 2**
(unter ε = 4, also gekappt), Spitze 335–366 px/Tick (mehrere Nachbarn zugleich), Flug ≈ 850 px, Lücke 375/396 px.
ε = 6 (auch 10, 20) und `MAX_SPEED` 200/100 nehmen diesen Fall weg; bei ε = 6 bleiben nur die 3 A1-Fälle.

**Wächter:**
* **Block-14-Probe** (`p105_b14_layout_probe.py`, als Modul mit dem ε-Patch, Beleg nach `/tmp`,
  `/tmp/insel/b14_variant.py`): **alle sechs Zellen grün**, für ε = 4 **und** ε = 6 (je ein Lauf). Zahlen unten für
  ε = 4; ε = 6 identisch bis auf die Budget-Szene (Prüfsumme 3527367083, Welt 1.271 × 1.245, Zoom 0,78). 152-Item-Szene (Determinismus, Regionen, Stabilität, Kamera, Beschriftungen) **byte-gleich** zum
  Repo-Beleg — dort kommen sich nie zwei Knoten näher als **6,64 px** (Node, alle Ticks, alle Zustände). Einzige
  Änderung: die 200-Knoten-Budget-Szene (`pos_pruefsumme` 199672332 → 1890691864, Welt 1.277 × 1.349 → 1.276 × 1.250,
  Zoom 0,73 → 0,78; `ruhe_ms` 2.147 statt 2.146, Rauschen) — dort lag also auch ein Tritt. Derselbe Lauf mit HEAD: Prüfsumme
  und Welt gleich dem Repo-Beleg (die Messung misst, was der Beleg misst).
* **P10.5-65** (Determinismus): bleibt — die Regel ist deterministisch, Zelle grün. **P10.5-68** (Stabilität): grün,
  byte-gleich.
* **`test_b14_*`**: lesen die Belege; nur `p105_b14_layout_probe.json` (Budget-Szene) wäre neu zu schreiben.
  `[VERIFY]` mit einem echten Suite-Lauf nach dem Bau.
* **`test_b18_karte_messung.py` :72–75** behauptet „der ruhige Zustand ist unberührt" (Welt „aus" = Basislinie 18.0).
  Mit ε ändert sich die 18.0-Saat „aus" (weitester 973 → 907 px, Komponenten 2 → 1) — die Zusicherung kodiert den
  **alten, fehlerhaften** Zustand und müsste mit datierter Notiz der neuen Welt folgen (Memory „honest counter-runs":
  Schwellen, die nur einen alten Zustand kodieren, folgen dem neuen).

### 4.2 Alternativen, und warum niedriger

| # | Alternative | Gemessen | Warum niedriger |
|---|---|---|---|
| B | `MAX_SPEED` 600 → 200 (oder 100) | auf den Live-Formen wie ε (0 %, byte-gleich auf Block 14); Stress 2,5 % / 1,3 % (Reste nicht einzeln aufgeschlüsselt) | deckelt die **Folge**, nicht die Kraft; ein Tritt an der Grenze rollt weiter ≈ 5,7 · 200 · 0,5 ≈ 570 px > 266 px (Schließ-Grenze) — bei dichteren Daten wieder eine Insel. Bremst außerdem **jede** schnelle Bewegung (Anker-/Federzug in großen Welten); 600 war in 18.2 bewusst so gewählt, dass die Grenze im ruhigen Zustand nicht greift |
| C | Saat ohne Überlappung (Mindestabstand in `computeRegions()`) | nicht gebaut | heilt nur die Saat-Nähe; der Durchflug-Tritt der 18.0-Saat (Tick 9) bleibt; fasst die Saat an ⇒ Regionen/P10.5-68 neu |
| D | Anker-Zug für Grad-0-Knoten ohne α, oder mehr Ticks | nicht gebaut | ändert die Physik aller Knoten bzw. die Dauer (Budget ≤ 3 s, P10.5-69) |
| E | `fitView()` ignoriert Ausreißer | — | kosmetisch: die Insel bleibt, nur der Zoom nicht |

**Warum 6 und nicht 4:** 6 nimmt auch den Stress-Tritt weg (Spitzenkraft 2.700 / 36 = 75 statt 169) und ist auf
Block 14 noch byte-gleich. Preis: der Rand zu den 6,64 px der Block-14-Szene ist klein — ein neues Item dort könnte die
Regel einmal auslösen und die Szene um ein paar Pixel verschieben (kein Fehler, aber ein neuer Beleg). Wer diesen Rand
will, nimmt 4 und lebt mit dem seltenen ≈ 400-px-Tritt auf sehr dichten Spaces. Größere ε (8–15) brechen die
Byte-Gleichheit (Δ 106–156 px) ohne messbaren Gewinn.

### 4.3 Was nicht byte-gleich bleiben kann

Die Regel „ruhiges Layout byte-gleich" hält für die **Block-14-Szene** (152 Items), **nicht** für die 18.0-Saat:
deren ruhiges Layout **ist** der Fehler (Punkt in eigenem Umriss). Wer dort Byte-Gleichheit verlangt, verlangt die Insel.

### 4.4 Fund: Gegenlauf `schleuder` wird mit ε zahnlos

Mit ε greift `MAX_SPEED` auf keiner gemessenen Saat mehr (Spitze ≤ 326 px/Tick in 960 Läufen). Node, 18.0-Saat:
„ε = 4" und „ε = 4 **ohne** `MAX_SPEED`" sind **positionsgleich** in allen vier Zuständen — der bestehende Gegenlauf
`schleuder` (`MAX_SPEED = 1e9`) bliebe also **grün**. Zwei ehrliche Wege (Nikinger):
1. `MAX_SPEED` als **zweiten Gurt** behalten und für `schleuder` erst eine **neue Szene suchen**, in der die Grenze
   greift. Ich habe keine gefunden: Spitze ≤ 326 px/Tick (ε = 4) bzw. ≤ 257 (ε = 6) in allen 960 Läufen, und selbst
   v4.0.0-Cliquen **mit** ε = 4 bleiben bei 566 < 600. Ziehen taugt nicht als Szene — ein Zug rechnet keine Simulation
   (`onMouseMove` setzt nur x/y, `onMouseUp` pinnt). Findet sich keine, ist die Grenze unter ε **wirkungslos**, und das
   gehört so in den Beleg.
2. `MAX_SPEED` als überflüssig **streichen**; dann färbt der Gegenlauf `tritt` (§5) **zwei** Zellen rot (Node: ohne ε
   und ohne Grenze wird auch `schleuder` rot, Tags 1.474 px) — eine Regel, ein Gegenlauf, aber nicht mehr „genau eine Zelle".

## 5. Zellen- und Gegenlauf-Entwurf

**Zelle `insel`** (für `p105_b18_karte_messung.py`, neben `schleuder`/`ausreisser`): in **jedem** Zustand (Laden,
aus, Tags, Ordner, beide) hat die Körpermaske von `computeLobes()` **genau eine** Komponente. Haken (Messpflaster, wie
in `/tmp/insel/browser_insel.py`): am Ende von `computeLobes()` vor `return { key: lobeKey(shown), lobes: lobes };`
`globalThis.__body = {koerper, cols, rows, cell, minX, minY}` ablegen; eine Funktion `__insel()` flutet `koerper`
(4-Nachbarschaft) und liefert Komponentenzahl, je Insel Knoten, Lücke, Spaces, Grad.

```python
"insel": all(z["geometrie"]["koerper_komponenten"] == 1 for z in zs.values()),
```

**Gegenlauf `tritt`** — patcht genau die neue Regel zurück:
`"var dist2 = Math.max(dx * dx + dy * dy + 0.01, REPULSION_MIN_DIST * REPULSION_MIN_DIST);"` →
`"var dist2 = dx * dx + dy * dy + 0.01;"`.

**Gezeigt (Browser, §2.2):** der Gegenlauf **ist** HEAD (HEAD = Vorschlag minus diese Zeile; die Konstante bliebe
unbenutzt). Ergebnis: `insel` **rot** (Laden/aus/aus2: 2 Komponenten, `itm_0000002f` 490,7 px), `schleuder` grün
(≤ 973 px), `kanten` unberührt (nicht gemessen, sondern gelesen: Stern und Mitte hängen an `updated`, nicht an Positionen). Mit der Regel (ε = 4, Browser): **1
Komponente in allen sechs Messpunkten** ⇒ `insel` grün, `schleuder` grün (≤ 918 px); ebenso mit ε = 6 (≤ 919 px). Die Zelle fällt also auf dem
fehlerhaften Code und steht auf dem korrigierten — und sie wäre auch auf v4.0.0 rot (2–3 Komponenten).

## 6. Offenes für den Nikinger

* **Entscheidung:** ε-Regel in `v4.0.1` aufnehmen (Physik-Änderung, Scope von 18.2) — ja/nein; dazu §4.4 (Weg 1 oder 2).
* **Live-Prüfung nach dem Deploy, zwei Schritte** (Umschalten allein rechnet nicht neu, §3.4 — darum jedes Mal Reset):
  1. Tags **und** Ordner **aus**, „Layout zurücksetzen", herauszoomen: liegt ein Punkt in **eigenem** Umriss neben dem
     Körper? (v4.0.1 **ohne** ε: möglich, bis ≈ 1 km Welt; **mit** ε: nicht erwartet.)
  2. Tags **und** Ordner **an**, „Layout zurücksetzen": keine **Gruppe** grauer Knoten in eigenem Umriss, kein Bogen über
     mehrere Bildschirmbreiten. Ist die Gruppe aus Bild 2 weg, ist „Bild 2 = N1" live bestätigt.
* A1 (Ein-Item-Space auf seinem Hex-Platz) bleibt ein eigenes Thema (§4.1 Fußnote; Plan §5.5 Punkt 2).

## 7. [VERIFY]

* Live-Form: ob die echten Spaces **Wurzel-Items und Ordner zugleich** haben (die Quelle der Saat-Nähe) — angenommen.
* Bild 2 = N1 auf v4.0.0: aus Form, Farbe und Abstand geschlossen, nicht an seinen Daten gemessen. Eine **graue**
  Gruppe im Browser habe ich nicht getroffen (Node: 2 von 360 Läufen in Browser-Reihenfolge; Browser auf Saat 12: Gruppen
  und Punkte anderer Spaces, §2.2) — daher „mittel".
* Node-Raten eigener Saaten: Knotenreihenfolge gemischt, nicht die `store.search()`-Ordnung; Browser bestätigt nur die
  18.0-Saat (drei Code-Stände). Firefox/Safari des Nikingers nicht gemessen (kopfloses Chromium 151; die Physik ist
  reine Gleitkomma-Arithmetik, Abweichungen zwischen Engines `[VERIFY]`).
* `test_b14_*`/`test_b18_*` nach dem Bau mit der vollen Suite; die Budget-Szene braucht einen neuen Beleg.
* §2.2: Zuordnung „Einzelpunkt unten rechts" in 18.0 §5.2 (A1) zu `epsilon` — am Bild `b18_0_aus.png` prüfen.
