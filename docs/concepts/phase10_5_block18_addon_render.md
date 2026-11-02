---
status: live
purpose: Addon zu Plan Block 18 — Render-Effizienz der Karte (`graph.js`: `draw()`/`drawEdges()`/Simulationsschleife). Gemessene Vorschläge, wie „beide an" (Tags + Ordner) auf ≤ 16,7 ms je Bild käme, unter der Entscheidung A (die Strichelung bleibt). Nichts gebaut, nur gemessen und vorgeschlagen.
read-when: vor einem Umbau von `draw()`/`drawEdges()`, und wenn der Nikinger über die Zelle `bildzeit` (Plan §5.5 Punkt 1) entscheidet — zuerst §1 (Ergebnis), dann §4 (Vorschläge) und §5 (offen)
detail: L2
up: ./phase10_5_block18_live_fixes_plan.md
down:
  - ../../phase10_5_finishing/probes/p105_b18_karte_messung.py   # die Probe, deren Mechanik (Saat, Pflaster, Wegwerf-Instanz) hier wiederverwendet wurde
updated: 2026-11-02 (Erstfassung, Claude Code — Messungen an der Wegwerf-Instanz, kein Produktcode geändert)
---
# Addon Block 18: Render-Effizienz der Karte

> **Auftrag (2026-11-02):** Wege finden und **vorschlagen** (nicht bauen), wie die Karte mit **allen** Schaltern an
> `draw()` ≤ 16,7 ms (60 fps) erreicht, gemessen mit der vorhandenen Probe; dazu eigene Zahlen für Hover, Pan und die
> Simulation (129 Bilder). Randbedingung: **Entscheidung A** — Tag-Kanten gestrichelt `[4,4]`, Ordner gepunktet `[1.5,3]`,
> explizite durchgezogen. Kein Produktcode, keine Probe und kein Test im Repo wurde geändert; diese Datei ist die einzige neue.

## 1. Ergebnis

**Unter A streng genommen: 60 fps nur für Bilder, in denen sich nichts bewegt.** Für das Einschwingen und den Hover-Wechsel reicht es nicht.

| Bildart („beide an", 1920 × 1200) | heute | bester Weg **ohne** sichtbare Änderung | ≤ 16,7 ms? |
|---|---|---|---|
| **Ruhe / Pan** (Kamera bewegt sich, Knoten nicht) | 34,5 ms (dpr 1) · 56,2 ms (dpr 2) | **Kanten-/Lappen-Schicht im Zwischenspeicher** (V1): **2,3 ms** · **6,2 ms** | **ja** (dpr 1 und 2) |
| **Hover-Wechsel** (ein Bild je neuem Fokus) | 34,8 ms | keiner gefunden; das Bild beim **Verlassen** des Fokus wird mit V1 ein Speichertreffer (≈ 2,3 ms) | **nein** |
| **Einschwingen** (129 Bilder) | 34,6 ms/Bild, 4,5 s | streng bildgleich: keiner (Untergrenze = heute, 34,6 ms). Mit V4 (nicht pixelgleich, §5 Punkt 3): 29,3 ms/Bild, 3,8 s | **nein** |

Was die Untergrenze trägt: ohne Kanten kostet das Bild ≈ 5,2 ms (Lappen + Knoten); 60 fps beim Einschwingen verlangen also
Kanten ≤ ≈ 11 ms, d. h. **2,6 × weniger** als heute (29,2 ms). Kein bildgleicher Weg kommt da hin (§3); die Untergrenze unter A
ist **34,6 ms** streng bzw. **29,3 ms**, wenn der Nikinger V4 noch als „Strichelung bleibt" gelten lässt. Was das Einschwingen schafft,
**ändert das Bild** und ist eine Option für den Nikinger, kein Vorschlag (§5 Punkt 1: LOD ohne Striche 11,2 ms, gerade Kanten +
eckige Kappen 15,4 ms).
Mehrere Simulationsschritte je Bild (V3) halbieren die **Dauer** (2,3 s statt 4,5 s, Endlage byte-gleich), die einzelnen Bilder bleiben aber 35 ms lang.

**Achtung, dpr 2:** auf einem Retina-Bildschirm (vermutlich der Mac des Nikingers, `[VERIFY]` V-A1) braucht das Einschwingen
**auch ohne Strichelung** 22,4 ms je Bild. Mit Software-Rasterung ist 60 fps beim Einschwingen dort **selbst ohne Strichelung
unerreichbar**. Ob die GPU-Rasterung im echten Browser das ändert, ist **nicht gemessen**.

**Die Zelle `bildzeit` der Probe würde mit V1 trivial grün**, denn sie misst wiederholte `draw()` ohne Zustandswechsel, also den
Speichertreffer. Vor V1 muss sie in drei Zellen geteilt werden (§4 V1).

## 2. Methode und Messgerät

* **Wegwerf-Instanz** über die Mechanik der Probe `p105_b18_karte_messung.py` (als Modul geladen; dieselbe Saat mit
  263 Items und 5 Spaces, dasselbe Pflaster `__sfx18`, `b14._setup/_serve/_stop`, freier Port, tmp-`DATA_ROOT`/`auth.sqlite3`,
  TLS, Umgebung ohne `SHAREFYX_*`/`SFX_*`/`SPACE_*`, Stopp **nur** über die PID-Datei). Zusätzlich hängt ein eigener Haken
  `__sfxA` an derselben **Kopie** von `graph.js` (eingefügt vor `function fitView()`). Er ersetzt `drawEdges` je Variante
  (`drawEdges = function …`, wie das Pflaster `integrate` umhängt) und enthält den Zwischenspeicher, den Pixelvergleich und
  eine synchrone Simulation. Werkzeug und Rohdaten liegen außerhalb des Repos (nicht versioniert) in
  `~/.claude-code-tools/b18addon/` (`result_1_2.json`, `check_1_2.json`, `result_lauf1_dpr1.json`, Bilder). Playwright aus dem
  `e2e-venv`, mit `add_init_script(sfx:film:gesehen=4.0.0)`.
* **Messgerät:** kopfloses Chromium **151.0.7922.34**, Software-Rasterung, Fenster 1920 × 1200 (Leinwand 1134 × 1061 CSS-px),
  **dpr 1 und dpr 2** (`device_scale_factor`). Die Zahlen sind nur **untereinander** vergleichbar.
* **Je Bild ein Flush** (`getImageData(0,0,1,1)`, die Falle aus Plan §5.1). 30 Bilder je Messung, **3 Wiederholungen,
  verschränkt** (A B C … A B C …, nicht A A A). Angegeben ist der Median, in Klammern die Spanne, wo sie zählt.
* **Pixelvergleich:** volles `getImageData` der Leinwand gegen das Bild des unveränderten Codes am selben Ort. Gezählt werden
  die abweichenden Pixel und die größte Kanalabweichung.
* **Simulation:** (a) **synchron**: `simSync()` setzt wie `clearStoredLayout()` zurück und rechnet dieselben 129 Schritte
  (`applyForces`/`integrate`/`ALPHA_DECAY`), mit `draw()` + Flush je Bild. Am Ende steht ein **FNV-Hash aller Positionen**.
  (b) **echt**: der Knopf „Layout zurücksetzen" mit der rAF-Schleife des Produkts (Funktion `simulation()` der Probe).
* **Last:** vor den Läufen 1,2–1,4 (4 Kerne; `gnome-shell`/`Xorg`, keine fremde Messung), während der Läufe bis 2,6 (der eigene
  Browser). **Rauschen:** Lauf 1 maß „aus" mit 5,8 ms, Lauf 2 und die Probe mit 3,7 ms; „beide" lag in beiden Läufen bei
  34,1–34,5 ms. Die Zoom-Messung bei 2,5 schwankt zwischen den Läufen (48 bzw. 61 ms) und ist **nicht belastbar**.

## 3. Messtabelle

### 3.1 Je Zustand (dpr 1, Lauf 2, Median aus 3 × 30 Bildern; „Sim" = echter Reset-Weg)

| Zustand | `draw()` heute | Pan heute | **Pan mit V1** | V1-Neuaufbau | Hover-Wechsel heute | Sim heute (Dauer / je Bild) |
|---|---|---|---|---|---|---|
| aus | 3,66 | 3,65 | **1,77** | 5,92 | 3,66 | 2,12 s / 16,6 ms |
| Tags | 23,44 | 23,52 | **2,18** | 26,26 | 23,41 | 2,68 s / 20,9 ms |
| Ordner | 10,91 | 11,07 | **1,96** | 13,28 | 11,10 | 2,11 s / 16,5 ms |
| beide | 34,45 | 34,53 | **2,31** | 37,32 | 34,82 | 3,92 s / 30,7 ms |
| *dpr 2:* aus | 10,49 | 10,30 | **4,40** | 20,03 | 10,75 | 2,13 s / 16,6 ms |
| *dpr 2:* Tags | 42,03 | 42,21 | **5,65** | 51,45 | 42,13 | 4,32 s / 33,8 ms |
| *dpr 2:* Ordner | 20,03 | 19,92 | **5,06** | 30,58 | 20,21 | 2,94 s / 23,0 ms |
| *dpr 2:* beide | 56,52 | 56,22 | **6,19** | 68,46 | 56,49 | 6,07 s / 47,4 ms |

**Varianten je Zustand** (`draw()` ms, Median; „—" = nicht gemessen):

| Zustand | heute | V4 | `butt` | `butt`+V4 | gerade+`butt`+V4 | ohne Striche |
|---|---|---|---|---|---|---|
| aus (dpr 1) | 3,66 | 3,60 | 3,55 | 3,56 | — | 3,61 |
| Tags (dpr 1) | 23,44 | 23,21 | 17,05 | 16,90 | — | 8,33 |
| Ordner (dpr 1) | 10,91 | 10,32 | 7,84 | 7,43 | — | 4,52 |
| beide (dpr 1) | 34,45 | 29,09 | 23,81 | 21,16 | 15,11 | 10,91 |
| Tags / Ordner (dpr 2) | 42,03 / 20,03 | — | — | 32,10 / 15,12 | — | 21,61 / 10,92 |
| beide (dpr 2) | 56,52 | 48,62 | 38,05 | 33,84 | 26,87 | 22,24 |

### 3.2 Zeichenvarianten „beide an" (dpr 1; `draw()` / nur Kanten / Pixel anders von 1.203.174)

| Variante | `draw()` ms | Kanten ms | Pixel anders (Ø Kanal) | sichtbar? |
|---|---|---|---|---|
| heute (`orig`) | 34,45 | 29,20 | 0 | — |
| **V4** geschlossene Lücke → durchgezogen | **29,09** | 23,88 | 28.282 (20,6) | im Ausschnitt nicht zu sehen (§4 V4) |
| Kanten nach Stil sortiert, ein `stroke()` je Kante | 34,54 | 29,02 | 36.424 (1,1) | nein — **kein Gewinn** |
| Sichtfeld-Auslese (`cull`) bei eingepasster Ansicht | 34,39 | 29,12 | 0 | nein — **kein Gewinn** |
| Strichelung von Hand (JS), ein Pfad je Stil | 47,59 | 41,79 | 112.029 | **langsamer** |
| dasselbe, geschlossene Lücken durchgezogen | 41,41 | 35,70 | 113.610 | **langsamer** |
| Strichelung von Hand, ein Pfad je Kante | 36,00 | 30,73 | 105.498 | **langsamer** |
| eckige Kappen (`butt`) | 23,81 | 18,53 | 125.660 (73) | **ja**: Striche kürzer, Lücken größer |
| `butt`, Strich um `w` verlängert (Ausgleich) | 28,22 | 22,96 | 135.112 | Kappen eckig |
| `butt` + V4 | 21,16 | 15,62 | 116.424 | ja |
| gerade Kanten, runde Kappen | 28,09¹ | 22,87¹ | 242.157 | **ja**: keine Bögen |
| gerade + `butt` | 17,00 | 11,79 | 237.034 | ja |
| gerade + `butt` + V4 | 15,11 | 9,84 | 234.563 | ja |
| ohne Strichelung (Untergrenze, Option B des Plans) | 10,91 | 5,79 | 133.595 | ja: Arten nicht unterscheidbar |

¹ Lauf 1. Bilder der Varianten: `~/.claude-code-tools/b18addon/bilder/`, Ausschnitt `vergleich3.png`.

**Kanten nach Art** („beide", Sehnenlänge in Welt-px): Tag, Lücke offen: 278 Kanten / 83.026 px · Tag, Lücke geschlossen: 14 / 2.726 ·
Ordner, offen: 67 / 11.114 · Ordner, geschlossen: 121 / 15.593 · explizit: 93 / 14.705. Die Summe der impliziten Kanten ergibt
112.459 px, wie in Plan §5.5. **Die offenen Tag-Striche tragen den Großteil der Kosten.**

### 3.3 Einschwingen „beide an" (129 Schritte; synchron: Bild-Median, Summe; echt: Reset-Knopf)

| Variante | dpr 1 je Bild | dpr 1 Summe | dpr 1 echt | dpr 2 je Bild | dpr 2 echt | Positions-Hash |
|---|---|---|---|---|---|---|
| heute | 34,6 ms | 4,49 s | 4,57 s | 56,1 ms | 7,57 s | 4030472295 |
| V4 geschlossene Lücke | 29,3 | 3,79 s | — | 48,2 | — | gleich |
| `butt` | 24,0 | 3,12 s | — | 38,0 | — | gleich |
| `butt` + V4 | 21,1 | 2,74 s | 2,76 s | 33,9 | 5,33 s | gleich |
| gerade + `butt` | 17,2 | 2,23 s | — | 29,6 | — | gleich |
| gerade + `butt` + V4 | **15,4** | 1,99 s | 2,15 s | 26,8 | 3,52 s | gleich |
| ohne Strichelung | **11,2** | 1,45 s | 2,13 s | 22,4 | 2,87 s | gleich |
| heute, **2 Schritte je Bild** (V3) | 34,9 | **2,28 s** (65 Bilder) | — | 55,9 | — | gleich |
| nur Physik, ohne Zeichnen | 0,24 | 0,03 s | — | — | — | gleich |

**Alle Varianten ergeben denselben Positions-Hash wie die Physik ohne Zeichnen.** Das Zeichnen wirkt nicht auf das Layout zurück:
keine Variante fasst die Block-14-Wächter (Determinismus P10.5-65, Stabilität P10.5-68) an. Der echte Reset-Weg ist rAF-gebunden
(Boden ≈ 16,6 ms/Bild = 2,1 s); deshalb liegen „ohne Strichelung" und „gerade + `butt` + V4" dort beide bei ≈ 2,1 s.

### 3.4 Zoom, Hover, Mausrad (dpr 1, „beide")

* **Strichkosten gegen Zoom** (`draw()` heute / `butt` / ohne Striche): 0,5 → 22,7 / 15,3 / 5,6 ms · 1,0 → 35,3 / 24,6 / 11,4 ·
  1,5 → 45,5 / 30,9 / 17,0 · 2,5 → 48–61 (Rauschen) / 30,3 / 18,1. Die Kosten wachsen mit der **sichtbaren Länge in
  Gerätepixeln**. Die Auslese in JS (`cull`) brachte bei keiner Stufe einen belastbaren Gewinn (Pixel gleich, Zeit ±). Skia
  verwirft unsichtbare Geometrie offenbar schon selbst billig (`[VERIFY]` V-A4, am Mechanismus nicht geprüft).
* **Hover:** `onMouseMove()` zeichnet nur, wenn sich `hoverId` ändert; ein ruhender Hover kostet nichts. Der **Wechsel**
  kostet ein volles Bild (34,8 ms). Mit V1 ohne Hover im Schlüssel bleibt das so (direkt gezeichnet), und das Verlassen des Fokus
  wird ein Treffer. Hängt der Hover am Schlüssel (`hoverId` im Schlüssel), kostet der Wechsel 37,2 ms (+2,4 ms Aufbau) und
  ein Pan mit festem Hover danach 2,55 ms.
  Die **Dim-Schicht mit Ring-Overlay** (alle Kanten mit 0,45 vorgerendert, Ringkanten mit umgerechnetem Alpha darüber) kostet im
  Median über 10 Fokusknoten 13,9 ms, ist aber **nicht bildgleich**: 155.347 Pixel anders, weil Überlappungen anders
  zusammengesetzt werden. Für den Hub bringt sie nichts, denn beim Hub liegen **507 von 573 Kanten** in den Ringen.
  **Verworfen.**
* **Mausrad:** jeder Rad-Schritt ändert den Zoom. Ein **skalierter Blit** der alten Schicht kostet 4,1 ms (dpr 2: 14,0 ms),
  ist aber bis zum Neuzeichnen unscharf; das ist eine sichtbare Änderung und nur eine Option.

## 4. Vorschläge, gereiht

### V1 — Kanten-/Lappen-Schicht im Zwischenspeicher (Ruhe, Pan) · **empfohlen**

* **Gewinn:** Pan „beide" **34,5 → 2,3 ms** (dpr 1), **56,2 → 6,2 ms** (dpr 2). Alle vier Zustände ≤ 6,2 ms. Ein Bild **mit**
  Neuaufbau kostet +2,9 ms (dpr 1) bzw. +12 ms (dpr 2, 68,5 statt 56,5).
* **Bau-Regel (wichtig, sonst wird es langsamer als heute):** das Bild, in dem sich der Schlüssel ändert, wird **direkt** gezeichnet
  (wie heute). Gebaut wird die Schicht erst, wenn der Schlüssel ein Bild lang stabil war, bzw. im Leerlauf (nach `settle()`, nach
  dem letzten Rad-Schritt). Sonst zahlte **jeder** Mausrad-Schritt, Schalter und Filter die +2,9/+12 ms (dpr 2: Rad 56 → 68 ms,
  ≈ 21 % schlechter). Nie während der Simulation oder eines Drags. Dass interaktive Bilder dann nie den Aufbau zahlen, ist
  **aus dieser Reihenfolge gefolgert, nicht gemessen**.
* **Bau** (`graph.js`): `draw()` (:1115) bekommt einen Zweig. Wenn die Simulation ruht (`activeRafId === null`), kein Drag läuft
  und `hoverId === null`, werden `drawLobes`+`drawEdges` in eine Offscreen-Leinwand über dem **Welt-Umriss** gerendert
  (Knoten, Kontrollpunkte, Lappen, + Rand). Diese Leinwand wird auf **ganze Gerätepixel** geblittet, Knoten und Beschriftungen
  bleiben live. Ein Rand jenseits der Leinwand ist nötig, sonst zeigt der Pan leere Streifen. Der Schlüssel besteht aus
  `zoom`, `dpr`, `frac(dpr·panX/Y)`, `tagsEnabled`/`foldersEnabled`, `filterType`/`filterStatus`, `lobeCache.key` und einem
  **Positionszähler**. Der Zähler wird erhöht in `integrate()` (:1098), im Drag-Zweig von `onMouseMove()` (:2160), in
  `clearStoredLayout()` (:2050), in `rebuildImplicitEdges()` (:540, auch weil `recomputeDegrees()` die Breiten ändert) und
  beim Neuladen des Graphen. Dazu kommen `resize()` (:1484) und `onWheel()` (:2242, Zoom = neuer Schlüssel). `searchQuery`
  wirkt nur auf Knoten und gehört **nicht** in den Schlüssel.
* **Speicher:** die Schicht hat die Größe des Welt-Umrisses × Zoom × dpr. „Beide" eingepasst: 1149 × 1051 px ≈ 4,8 MB (dpr 1),
  2295 × 2099 ≈ 19 MB (dpr 2). Beim Zoom 2,5 wüchse sie grob auf das 7-Fache. Deshalb braucht es einen **Deckel** (Vorschlag:
  über ≈ 16 Mio. Gerätepixeln direkt zeichnen), Zahl `[VERIFY]` V-A3.
* **Fund dabei, unabhängig von V1:** `drawNodes()` **erbt** `lineCap = "round"` aus `drawEdges()`, denn beide laufen im selben
  `save()`-Block. Zeichnet man die Kanten woanders, bekommen die Zell-Fortsätze eckige Kappen: im ersten Lauf 5–7 Tausend
  Pixel anders. Wer V1 baut, setzt `lineCap`/`lineJoin` vor `drawNodes()` **ausdrücklich**.
* **Bildgleichheit:** Treffer gegen einen **frisch gebauten** Zwischenspeicher am selben Ort: **0 Pixel** nach Pan, Drag mit
  Zähler und Zoom (dpr 1 und 2). Gegen den **direkten** Weg bleibt ein Rest: Ruhe 12 Pixel (dpr 2: 35), nach Pan 471 (3.797),
  nach Zoom 3.369 (8.612) von 1,2 bzw. 4,8 Mio., also ≤ 0,3 %, max. Kanal 255. Der Rest tritt **auch ohne Strichelung** auf.
  Die Vermutung „Skia schneidet Striche am Rand anders ab" ist damit **widerlegt**. Ursache nicht bestimmt; eine **Vermutung**
  ist, dass Pfade, die den Leinwandrand kreuzen, anders gerastert werden (`[VERIFY]` V-A2: Lage der Pixel ansehen).
* **Wächter (Probe-Erweiterung, Vorschlag):** die Zelle `bildzeit` wird geteilt in:
  * `bildzeit_ruhe`: Pan-Bild ≤ 16,7 ms;
  * `bildzeit_hover`: Hover-Wechsel, gemessen und berichtet; die Schwelle setzt der Nikinger;
  * `bildzeit_sim`: Bild-Median beim Einschwingen.

  Neue Zelle **`zwischenspeicher`**: nach jedem Auslöser (Schalter, Filter, Drag, Zoom, Resize, Reset, Neuladen) ist das
  Speicherbild **gleich** einem frisch gebauten (0 Pixel). Der Vergleich gegen den direkten Weg taugt **nicht** als Schwelle, weil
  der Rest nach Zoom (3.369) in derselben Größenordnung liegt wie ein echter Fehler.
* **Gegenläufe:**
  * `veraltet`: die Erhöhung des Zählers im Drag-Zweig von `onMouseMove()` entfernen. Gemessen: 11.951 Pixel (dpr 1) bzw.
    31.791 (dpr 2) statt 0. Rot wird **nur** `zwischenspeicher`.
  * `ohne_speicher`: der Schlüssel ist jedes Mal neu. Rot wird **nur** `bildzeit_ruhe` (37 statt 2,3 ms).
* **Risiko, gebrochenes dpr:** der Schlüssel enthält `frac(dpr·pan)`, Mausdeltas sind ganze CSS-Pixel. Bei dpr 1,25/1,5/2,2
  (Browser-Zoom, auch am Mac) bekäme **jedes** Pan-Bild einen neuen Schlüssel, und der Pan wäre mit Neuaufbau **langsamer** als
  heute. Ausweg: auf gerundeten Versatz blitten (Verschiebung ≤ 0,5 Gerätepixel, dann **nicht** pixelgleich) oder bei
  nicht-ganzzahligem `dpr` ohne Zwischenspeicher zeichnen. Gemessen sind nur dpr 1 und 2 (`[VERIFY]` V-A1).
* **Risiko:** ein vergessener Auslöser zeigt ein veraltetes Bild. Davor schützt der Gegenlauf `veraltet` nur für den Drag; jeder
  weitere Auslöser braucht seine eigene Zeile in der Zelle. Die Beschriftungs-Probe (P10.5-71, `fillText`-Recorder) bleibt
  unberührt, denn Beschriftungen bleiben live. Barrierefreiheit: keine Änderung (Leinwand, gleiche Inhalte).
* **GPU:** ein Blit statt ≈ 600 Strich-Pfaden hilft vermutlich in jedem Rasterweg (**Annahme**).
* **Aufwand:** mittel, ≈ 60–80 Zeilen in `graph.js`, dazu die drei Zellen und zwei Gegenläufe in der Probe.

### V2 — Hover-Wechsel: nichts Bildgleiches gefunden

Gemessen: direkt 34,8 ms · Neuaufbau mit Hover im Schlüssel 37,2 ms · Dim-Schicht mit Overlay 13,9 ms, aber nicht bildgleich und
beim Hub wirkungslos (§3.4). **Vorschlag:** Hover-Bilder direkt zeichnen (wie heute) und die Ruhe-Schicht **nicht** verwerfen.
Das Verlassen des Fokus ist dann ein Treffer (aus dem Bau gefolgert, nicht eigens gemessen; ein Treffer kostet 2,3 ms). Ein Hover-Wechsel bleibt **ein** Bild von ≈ 35 ms (dpr 2: ≈ 56 ms), also ein
verlorenes Bild je Fokuswechsel und kein Dauerruckeln.

### V3 — Simulation an die Uhr koppeln (mehrere Schritte je Bild)

* **Gewinn:** mit 2 Schritten je Bild dauert das Einschwingen 2,28 s statt 4,49 s; die Endlage ist **byte-gleich** (Hash).
  Adaptiv (`Schritte = ceil(letztes Bild / 16,7 ms)`) bliebe die Dauer auf jedem Rechner bei ≈ 129 × 16,7 ms ≈ 2,15 s,
  so lange wie heute im Zustand „aus" (**Rechnung, nicht gemessen**).
* **Was es nicht tut:** das einzelne Bild bleibt 35 ms; die Animation läuft mit ≈ 29 fps und doppelt so großen Sprüngen.
  Das betrifft die Bewegung, nicht den Strich, und ist mit A vereinbar. Der Nikinger sollte es trotzdem einmal sehen.
* **Bau:** `tick()` in `runSimulation()` (:981): die Zeilen `applyForces`/`integrate`/`alpha *= ALPHA_DECAY` in eine Schleife.
  Der reduced-motion-Pfad (:999) ist unberührt.
* **Wächter:** Positions-Hash gleich (Block-14-Probe `determinismus`, P10.5-65); Zelle `sim_dauer` ≤ 2,5 s „beide".
  **Gegenlauf** `ein_schritt`: Schritte fest 1, rot wird nur `sim_dauer` (gemessen 3,9–4,6 s). Geprüft (2026-11-02, `grep`): weder `tests/test_b18_karte_messung.py` noch die
  Block-14-Probe/-Tests erwarten fest 129 Bilder. Die Budget-Zelle (P10.5-69) prüft `ruhe_ms ≤ 3000`, `test_graph_c2.py:176`
  `raf_calls == 0` nur im reduced-motion-Pfad (unberührt). Der Gegenlauf `alpha` der Block-14-Probe (≈ 780 Schritte) bliebe
  mit 2 Schritten/Bild rot (≈ 390 Bilder ≈ 6,5 s, gerechnet). **Lücke:** zieht der Nutzer **während** des Einschwingens, landet
  der Zug relativ zur Physik anders (zwei Schritte je Mausbild); der Hash-Wächter deckt nur Läufe ohne Eingriff ab.
* **Aufwand:** klein (≈ 10 Zeilen).

### V4 — Kanten, deren Lücke die runden Kappen schon schließen, durchgezogen zeichnen

* **Begründung:** mit `lineCap = "round"` ist die sichtbare Lücke `Lücke − Breite`, und die Breite ist
  `1 + log2(1 + min(deg))` (:1239). Ordner `[1.5,3]` schließt ab Breite 3 (min. Grad ≥ 3), Tag `[4,4]` ab Breite 4
  (Grad ≥ 7). Diese Kanten **sehen schon durchgezogen aus**, kosten aber die volle Strichelung: in der Saat 121 Ordner- und
  14 Tag-Kanten.
* **Gewinn:** `draw()` 34,45 → 29,09 ms (dpr 1), 56,5 → 48,6 ms (dpr 2); Einschwingen 4,49 → 3,79 s. **Erreicht das Ziel allein nicht.**
* **Bildgleichheit:** **nicht** pixelgleich. 28.282 Pixel sind anders (Ø Kanalabweichung 20,6), weil eine Kette runder Kappen
  einen leicht gewellten Rand hat und der durchgezogene Strich einen glatten. Im Bildausschnitt (`vergleich3.png`) ist kein
  Unterschied zu sehen. Ob das unter A zulässig ist, entscheidet der Nikinger (§5 Punkt 3).
* **Bau:** in `drawEdges()` (:1240–1246) vor `setLineDash` die Bedingung `gap − lineWidth ≤ 0 ⇒ []`.
* **Wächter:** Zelle `strichbild`. Ein Recorder an `setLineDash` (Muster: der `fillText`-Recorder der Block-14-Probe) zählt die
  Kanten, die ein **anderes** Muster bekommen, als die aus dem Payload nachgerechnete Regel verlangt; grün bei 0. **Gegenlauf**
  `alle_durchgezogen`: die Bedingung gilt für **alle** gestrichelten Kanten. Erwartet werden 345 falsche Kanten (278 Tag + 67
  Ordner mit offener Lücke, aus §3.2 gerechnet, nicht gelaufen); als Stellvertreter gemessen sind 133.595 statt 28.282 Pixel
  anders. Nebenwirkung: derselbe Gegenlauf macht `bildzeit` **grün** (≈ 10,9 ms). Er ändert also eine zweite Zelle, wenn auch
  nicht nach rot; das gehört in die Gegenlauf-Tabelle der Probe.
* **Risiko:** gering; die Regel hängt an der Breitenformel und muss mitwandern, wenn sich diese ändert. **Aufwand:** klein.

### Gemessen und verworfen (nicht wieder vorschlagen)

| Idee | Ergebnis | Beleg |
|---|---|---|
| Strichelung in JS selbst erzeugen (Bézier abflachen, Striche als Teilpfade) | **langsamer**: 36,0–47,6 statt 34,5 ms | §3.2 |
| Sichtfeld-Auslese in JS | kein belastbarer Gewinn, auch nicht beim Zoom | §3.2, §3.4 |
| Kanten nach Stil sortieren (weniger Zustandswechsel) | 34,54 statt 34,45 ms | §3.2 |
| Dim-Schicht + Ring-Overlay für Hover | nicht bildgleich, beim Hub wirkungslos | §3.4 |
| `butt` mit verlängertem Strich (Ausgleich der Kappen) | 28,2 ms, Kappen trotzdem eckig | §3.2 |
| Bündeln je Stil (Block 18.1 b) | schon in 18.1 verworfen (37,6 statt 29,1 ms) | Plan §5.5 |

**Nicht gemessen, nur eingeordnet:**
* `Path2D`/Bézier-Rechnung sparen: kaum Gewinn, die Physik samt Geometrie kostet 0,24 ms je Schritt.
* Mausereignisse per rAF bündeln (Plan 18.1 d) senkt nicht die Kosten je Bild. Chromium bündelt `mousemove` ohnehin auf das
  Bild genau (`[VERIFY]` V-A5).
* **OffscreenCanvas im Worker:** verschiebt das Rastern vom Hauptfaden, senkt es nicht (Karte weiter ≈ 29 fps). Dazu kämen ein
  Worker-Modul ohne Build-Schritt (P5-T), Zustandsübergabe und ein zweiter Hit-Test. **Nicht empfohlen.**

## 5. Nicht gelöst / offen — Entscheidung des Nikingers

1. **Einschwingen und Hover-Wechsel unter A: Untergrenze ≈ 29 ms (dpr 1) bzw. ≈ 48 ms (dpr 2) je Bild.** Mögliche Wege, die das
   Bild **ändern**:
   * **(L1) LOD beim Einschwingen:** solange die Simulation läuft, ohne Striche; in Ruhe gestrichelt. 11,2 ms je Bild, echte
     Dauer 2,13 s. Der Strich „springt" am Ende in die Strichelung, nach ≈ 2 s. Im dpr-2-Fall (22,4 ms) reicht auch das nicht.
   * **(L2) LOD mit geraden Kanten + eckigen Kappen + V4 beim Einschwingen:** 15,4 ms je Bild (dpr 1 ✅, dpr 2 26,8 ✗). Die
     Arten bleiben unterscheidbar, die Bögen fehlen während der Bewegung.
   * **(L3) eckige Kappen dauerhaft** (`butt` + V4): 21,2 ms in Ruhe, 21,1 ms beim Einschwingen. Die Striche sind sichtbar
     kürzer bzw. feiner. ✗ beim Ziel.
   * **(C) Striche 3 × länger** (Plan §5.5): ≈ 19 ms ✗.
   * **Oder:** das 60-fps-Ziel gilt nur für Ruhe/Pan (V1) und **V3** verkürzt das Einschwingen auf ≈ 2,2 s.
   **Empfehlung:** V1 + V3 (+ V4, wenn Punkt 3 zustimmt), **ohne** LOD. Das Bild bleibt, wie es ist. Ruckeln gibt es nur noch
   während ≈ 2 s Einschwingen und je Fokuswechsel ein Bild.
2. **Die Zelle `bildzeit`** muss vor V1 geteilt werden (§1, §4 V1). Sonst wird sie durch den Zwischenspeicher grün, ohne dass
   das Einschwingen schneller wäre.
3. **V4 ist nicht pixelgleich** (gewellter gegen glatten Rand bei Kanten, die schon durchgezogen aussehen). Fällt das noch unter
   „die Strichelung bleibt"? Ein Bildvergleich in voller Größe beim Nikinger steht aus.
4. **Mausrad:** skalierter Blit (4 ms, kurz unscharf) oder Neuaufbau je Rad-Schritt (≈ 37 ms, scharf)? Ohne Entscheidung bleibt
   es beim Neuaufbau.

## 6. [VERIFY]

| # | Was | warum offen |
|---|---|---|
| V-A1 | dpr und Browser des Nikingers (Retina? Safari/Firefox/Chrome?) | entscheidet, ob die dpr-2-Spalte die maßgebliche ist |
| V-A2 | Lage der 12–8.612 Pixel Rest zwischen Speicher- und direktem Bild | Ursache unbestimmt; Vermutung: Pfade, die den Leinwandrand kreuzen |
| V-A3 | Deckel für die Größe der Schicht (Vorschlag ≈ 16 Mio. Gerätepixel) | Speicher bei Zoom 2,5 / dpr 2 nicht gemessen |
| V-A4 | dass Skia unsichtbare Striche selbst verwirft | nur aus „Auslese bringt nichts" geschlossen, nicht im Quelltext geprüft |
| V-A5 | dass Chromium/Firefox/Safari `mousemove` auf das Bild bündeln | nicht gemessen; nur relevant, wenn Pan nach V1 noch ruckelt |
| V-A6 | **GPU-Rasterung** (echter Browser): Kosten der Strichelung, des Blits, des Einschwingens | alle Zahlen hier sind Software-Rasterung; dass die GPU die Strichelung billiger macht, ist eine **Annahme** |
| V-A7 | adaptive Schritte je Bild (V3) im echten rAF-Weg | gemessen nur synchron mit fest 2 Schritten |
