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
updated: 2026-10-28 (Schritt 14.6.0 gebaut: die Basislinie gemessen — 5 Komponenten, 0 Furche-Zellen, 35,0 ms bei 201 Knoten) | 2026-10-28 (Entwurf, Claude Code — nach der Sichtung der 14.5-Bilder)
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
| **14.6.1** | Der Algorithmus (§2.1) mit `LOBE_CLOSE_PX = 0` (= heute, §2.2) — dann die **Varianten** `--konstante=LOBE_CLOSE_PX=` **0 · 80 · 120 · 160 · 200 · 240**, je mit `--bilder=~/p105_b14_6_varianten/<D>/` (**außerhalb** des Repos). | Mit `0` ist das Bild gleich dem von heute (§2.2). Tabelle je Variante: Komponenten, Lappen je Space, Furche-Zellen, Reach je Seite, Luft, Zellgröße, `computeLobes()`-Zeit (152/201 Knoten). **STOPP — Bericht an den Nikinger (E1).** Commit mit `LOBE_CLOSE_PX = 0`. |
| **14.6.2** | Den gewählten Wert setzen (Kommentar „gewählt vom Nikinger am <Datum>, gemessen in 14.6.1"). C2-Wächter: neue Messung `koerper` in `p105_b8_c2_probe.mjs` an einem **festen** Eingang (3 Gruppen, Abstand so, dass sie sich bei `LOBE_CLOSE_PX = 0` **nicht** berühren — Muster `FESTE_POSITIONEN`, Z. ~407) + Gegenlauf `koerper` (`LOBE_CLOSE_PX` → 0) in `tests/test_graph_c2.py`. Die alte Furche-Messung bleibt. | `koerper` grün; der Gegenlauf `koerper` macht **genau diese** Messung rot, die acht alten Gegenläufe bleiben rot an genau ihrer Messung. |
| **14.6.3** | Belege: `p105_b14_layout_probe.py` neu (Normalfall) · `p105_b14_karte_bilder.py` neu (Bilder ersetzen `docs/screenshots/p105_b14_karte_0{1,2,3}_*.png`, dieselben Namen) · `p105_b8_karte_probe.py` neu · volle Suite, `scripts/doc_health.py`, `phase5_ui/scripts/ui_budget.py`. Doku: §4-Zeile hier, Head (Modulstatus, Abnahmezeile **P10.5-72**, Summe, Session-Block), INDEX. | Die Knotenpositionen der Layout-Probe sind **gleich** zu `p105_b14_layout_probe.json` (alle Zellen gleich bis auf `zeit`) ⇒ das Layout ist unberührt, die sechs Gegenläufe müssen **nicht** neu. `koerper` grün mit dem gewählten Wert. Suite grün, `doc_health` 0, `ui_budget` grün. |
| 14.6.4 | **Claude Code:** Update-Log-Zeile anpassen (sie sagt heute „eigene Insel"), Sichtung **P10.5-70** neu beim Nikinger | — |

### Die Schritte 14.6.0 bis 14.6.4 — die Anmerkungen

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
