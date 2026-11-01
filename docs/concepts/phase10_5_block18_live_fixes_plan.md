---
status: live
purpose: Mini-Plan Block 18 „Live-Funde nach Deploy D" — Karte ruckelt mit Tags/Ordnern, einzelne Punkte weit draußen, Editor-Farben (Wahl). Befunde am Code, Hypothesen, Schritte 18.0–18.5, Entscheidungen E1–E4 (beantwortet). Ausführer: eine eigene Session.
read-when: Ausführung von Block 18 — zuerst §1 (Auftrag), §4 (Entscheidungen) und §3 (Schritte)
detail: L2
up: ../../phase10_5_finishing/CLAUDE.md
down:
  - ./phase10_5_block14_7_plan.md   # 📗 die Kartengeometrie (Hex-Anker, LOBE_SCALE), auf der 18.2 aufsetzt
updated: 2026-11-01 (18.0 gemessen: §5 gefüllt, K1–K4/A1–A3 mit Befund, neuer Befund N1 — Schleuder-Instabilität im Tag-Zustand) | 2026-11-01 (E1–E4 beantwortet: Stern, Farben → P11, v4.0.1, Zeilen 18/49 als Wegwerf-Probe 18.5) | 2026-11-01 (Mini-Plan, Claude Code — Live-Sichtung des Nikingers nach Deploy D)
---
# Live-Funde nach Deploy D (Plan Block 18)

> **Auftrag (Nikinger, 2026-11-01, nach dem Live-Test von `v4.0.0`, sinngemäß zitiert):** die Karte ist
> **sehr träge**, sobald Ordner und/oder Tags an sind · der Fehler „ein oder wenige Punkte liegen weit
> weg" ist **noch da** (Bildschirmfoto: ein Einzelpunkt in eigenem Umriss weit unten, die Karte deshalb
> auf 50 % gezoomt) · der neue Editor ist der richtige Schritt, aber nicht das Ende (echte RGB-Fläche
> zum Wählen, mehr Farben — **nach P11**, E2). „Since this space should be a real step": **sofort beheben** — Mini-Plan
> hier, Ausführung in einer anderen Session.

## 1. Was der Ausführer wissen muss

- Code ist die Wahrheit; jede Hypothese unten ist **am Code gelesen, nicht gemessen**. 18.0 misst zuerst.
- Gemessen wird **nur** an einer Wegwerf-Instanz (Root-`CLAUDE.md`, Working style). Muster für die Saat
  und die Karte: `phase10_5_finishing/probes/p105_b14_layout_probe.py` (feste IDs, feste Uhr) und
  `film/wegwerf.py`. Eine frische Instanz zeigt seit Block 17 zuerst das Film-Startbild:
  `add_init_script("localStorage.setItem('sfx:film:gesehen','4.0.0')")`.
- Jede Änderung bekommt einen Gegenlauf, der **die neue Szene** prüft (Memory „honest counter-runs").
- Deploy: eigener Patch-Deploy **`v4.0.1`** nach Block 18 (E3).

## 2. Befunde am Code (`main@<HEAD nach Deploy D>`, `phase5_ui/webui/static/js/graph.js`)

> **[2026-11-01, 18.0 gemessen — Urteil je Befund in §5.2.]** K1/K2 **bestätigt** (die Kosten sind das Zeichnen der Kanten), K3/K4 **widerlegt** als Kostenquelle, A1 **nur teilweise**, A2 **nicht die Ursache**, A3 **offen** (Nikinger). **Neu: N1** — im Tag-Zustand schleudert die Simulation Knoten tausende Pixel weit (§5.3); davon steht in den Hypothesen unten nichts.

| # | Ort | Befund | Folge (Hypothese) |
|---|---|---|---|
| K1 | `buildFolderEdges()` :612 | Ordner-Kanten sind eine **volle Clique** je `(space, folder)` — **ohne** Obergrenze. Tags haben eine (`TAG_CLIQUE_LIMIT = 15`, :163) | ein Ordner mit k Items ⇒ k(k−1)/2 Kanten; 60 Items ⇒ 1.770 Kanten. Tags mit ≤ 15 Knoten bleiben ≤ 105 je Tag, summieren sich aber |
| K2 | `drawEdges()` :1170 | **ein `stroke()` je Kante**, dazu `setLineDash()`, `globalAlpha`, `lineWidth` je Kante, Bézier je Kante | Zeichenkosten wachsen linear mit K1 — tausende Zustandswechsel je Bild |
| K3 | `draw()` :1080 | jeder `draw()` baut `explicitEdges.concat(implicitEdges)` neu, `neighborRings()` (:1425) läuft **zweimal über alle Kanten** je Bild, sobald ein Knoten unter der Maus liegt | Hover/Pan/Zoom kosten O(E) **pro Bild**, unabhängig vom Zeichnen |
| K4 | `applyForces()` :994 | Federn laufen über **alle** Kanten, Abstoßung O(n²) | jede Simulation (Drag, Reset) wird mit K1 langsamer und die Cliquen ziehen Ordner zu Klumpen |
| A1 | `computeRegions()` :698 | `slot = 2 * maxR + REGION_GAP` — **ein** Abstand für alle Anker, bemessen am **größten** Space; Anker auf dem Hex-Gitter (`hexPlatz`) | ein Space mit 1 Item sitzt auf seinem Gitterplatz, so weit draußen wie ein großer Space — ohne Kante, die ihn heranzieht (Anker-Gravitation zieht ihn nur zu **seinem** Anker). Passt zum Foto: Einzelpunkt in eigenem Umriss, weit unten |
| A2 | `fitView()` :2054 | rahmt **alle** sichtbaren Knoten ein | **ein** Ausreißer drückt den Zoom der ganzen Karte (Foto: 50 %) |
| A3 | `loadStoredLayout()` :1961 | gemerkte Positionen (`v: 1`) werden als `pinned` übernommen | Alternative Ursache: eine alte, gemerkte Position. Unterscheidung in 18.0 per „Layout zurücksetzen" |
| E1 | `markdown.js :: FORMAT_FARBEN` :47 | **vier** feste Farben als Klassen (`[Text]{.rot}`), Regex `\.[a-z]+` | mehr Farben = mehr Klassen (einfach). Freie RGB-Farbe: die CSP verbietet `style=`-Attribute (`style-src 'self'`); möglich wäre nur, dass der Renderer eine **geprüfte** Hex-Farbe per CSSOM (`el.style.color`) setzt — neue Syntax, neuer Sanitizer-Pfad |

## 3. Schritte

| # | Inhalt | Fertig, wenn |
|---|---|---|
| 18.0 ✅ | **Messen** an der Wegwerf-Instanz mit einer Saat in Live-Form (≈ 200 Items, 5–7 Spaces, 2–3 Ordner mit 40–80 Items, ein Space mit **1** Item, Tags wie live). Je Zustand (aus / Tags / Ordner / beide): Kantenzahl, ms je `draw()` (`performance.now()` um `draw`, 60 Bilder Pan), Dauer der Simulation. Ausreißer: reproduzieren, dann „Layout zurücksetzen" — bleibt er (A1) oder geht er (A3)? Die Saatzahlen vorher beim Nikinger erfragen (er kennt die Live-Form; **kein** Lesen des echten `DATA_ROOT`) | Tabelle im Plan §5, Ursache für Ausreißer benannt — **✅ 2026-11-01** (§5; Ursache: N1 im Tag-Zustand, A1 nur teilweise, A3 wartet auf den Nikinger) |
| 18.1 | **Karte flüssig.** In der Reihenfolge der gemessenen Kosten: (a) Ordner-Kanten als **Stern** um das zuletzt geänderte Item (k−1 Kanten statt Clique, E1); (b) Kanten **gebündelt** zeichnen: je Stil (Art × Fokus × Breitenstufe) **ein** Pfad, **ein** `stroke()`; (c) `all` und Nachbarringe nur bei Änderung neu bauen (Kantenliste beim Toggle, Ringe je `hoverId`); (d) `draw()` aus Mausereignissen per `requestAnimationFrame` bündeln | `draw()` ≤ 16 ms bei „beide an" auf der Saat (Zahl vorher/nachher); bestehende Kartenwächter grün (`phase10_5_finishing/tests/test_graph_c2.py`, `test_b14_*`); Gegenlauf je Teilschritt |
| 18.2 | **Kein Punkt weit draußen.** Bei A1: der Ankerabstand richtet sich nach den **echten** Radien der Nachbarn (eng gepackt: `r_eigen + r_k + REGION_GAP`, kleine Spaces auf die inneren Plätze), nicht nach dem größten Space. Bei A3: Ablage auf `v: 2` heben (alte Positionen verfallen einmal). Zusätzlich robust: `fitView()` darf einen einzelnen Ausreißer nicht die ganze Karte verkleinern lassen (Vorschlag: einrahmen nach Umrissen, nicht nach Knoten — **nur** wenn 18.0 zeigt, dass A1/A3 allein nicht reichen) | Saat mit 1-Item-Space: größter Abstand Punkt ↔ nächster Nachbarumriss ≤ 2 × `REGION_GAP` (Zahl in §5); Zoom nach dem Öffnen > 50 %; Determinismus-Wächter (P10.5-65) bleibt grün |
| 18.3 | ~~Editor-Farben~~ — **nach P11** (E2) | — |
| 18.5 | **P10.5-18 und P10.5-49 als Wegwerf-Probe, automatisch und bleibend** (E4). Eine Probe im Repo (`probes/p105_b18_live_zeilen_probe.py`, JSON daneben, jederzeit wiederholbar): **18** — `/api/v1/overview` Waiting ≤ 300 ms und Space-Wechsel während des Polls ≤ 1 s, gemessen im Browser (Playwright, `PerformanceResourceTiming.responseStart − requestStart`) mit der Saat aus 18.0; **49** — zwei Browser-Kontexte, ein Write im einen, das Ereignis kommt im anderen an (≤ 2 s). Je **beide Eingänge**: direkt (Loopback, wie der Funnel auf den Dienst zeigt `[VERIFY]` an `phase3_edge/`) **und** hinter einem lokalen Caddy aus `phase9_hardening/step_a/Caddyfile.template` in der Live-Version 2.6.2 (Netzwerk-Werkzeuge sind erlaubt, E4). Werkzeug in eigenem Verzeichnis unter `~/.claude-code-tools/`, nie im Projekt-`.venv` | beide Zeilen ✅ mit Zahlen und Gegenlauf (z. B. Caddy mit `flush_interval` aus ⇒ 49 rot; künstliche Verzögerung im Poll ⇒ 18 rot); Probe vom Nikinger gesichtet (Memory „throwaway evidence counts as live") |
| 18.4 | Update-Log-Zeile(n), volle Suite, `doc_health`, `ui_budget`, Commit + Push; Sichtung beim Nikinger (Bild der Karte, „beide an"); Deploy `v4.0.1` beim Nikinger | Abnahmezeile(n) P10.5-80 ff. im Head |

## 4. Entscheidungen (Nikinger, 2026-11-01)

| # | Frage | Antwort |
|---|---|---|
| E1 | Ordner-Kanten: Kette/Stern oder Clique mit Obergrenze? | **Stern** um das zuletzt geänderte Item des Ordners (k−1 Kanten) — Empfehlung angenommen |
| E2 | Editor-Farben jetzt oder in P11? | **P11** — „if I'd like to do it fully": Farbraster **und** freie RGB-Fläche zusammen, als Editor Stufe 3. **P11-Vormerkung** (Closeout Z übernimmt sie in den Handover); Befund E1 in §2 bleibt die Grundlage (CSP: freie Farbe nur per CSSOM) |
| E3 | Eigener Deploy `v4.0.1` nach Block 18? | **ja** |
| E4 | Prüfungen automatisch und bleibend: die Live-Zeilen **P10.5-18** und **P10.5-49** werden **Wegwerf-Proben** (Schritt 18.5). „Keine externen Werkzeuge, so wenige wie möglich" gilt für die **Software selbst**, nicht für Netzwerk-Werkzeuge beim Testen (lokaler Caddy usw. erlaubt) | angenommen. Außerdem: **P10.5-22** und **P10.5-27** macht der Nikinger, **P10.5-28** geht an **eurofleet** (verwaltet die Container) — Notiz `docs/concepts/phase10_5_p10j_lauf2_eurofleet.md` |

## 5. Messungen (18.0, 2026-11-01)

Beleg: `phase10_5_finishing/probes/p105_b18_karte_messung.py` → `p105_b18_karte_messung.json` (jederzeit wiederholbar,
~3 Minuten). Wegwerf-Instanz (eigener Port, tmp-`DATA_ROOT`/`auth.sqlite3`, TLS, Stopp über die PID-Datei), Messpflaster
auf einer **Kopie** von `graph.js` (Arbeitsbaum unberührt). **Messgerät:** kopfloses Chromium 151 (Linux, **Software-
Rasterung**, 1920 × 1200) — die Zahlen sind **nur untereinander** (vorher/nachher am selben Rechner) vergleichbar, nicht mit
dem Firefox/Safari des Nikingers. **Saat** (Nikinger: „ungefähr 5 Spaces", Ordner/Tags nach Plan-Maß): 5 Spaces mit
100/80/50/32/**1** = 263 Items, Ordner 80/60/40/12, 40 Tags mit ≤ 14 Knoten, 93 explizite Kanten, der Ein-Item-Space ohne Kante.
**Annahmen, nicht gemessen:** Tag-Verteilung und Verknüpfungsdichte der echten Karte.

**Gegenrechnung der Kanten** (Python-Spiegel von `buildTagEdges`/`buildFolderEdges` aus der **Saat**, nicht aus der Seite):
Seite = Saat in allen vier Zuständen ✅ (0 / 1.598 / 5.728 / 7.326 implizite, je 93 explizite) — der Messhaken liest das Richtige.

### 5.1 Kosten (ms) und Dauer der Simulation

| Zustand | Kanten | `draw()` | davon nur `drawEdges()` | `draw()` mit Hover | `neighborRings()` | `applyForces()` | Simulation (129 Bilder) |
|---|---|---|---|---|---|---|---|
| aus | 93 | **3,7** | 0,6 | 3,8 | 0,003 | 0,28 | **2,1 s** |
| Tags | 1.691 | **43,3** | 41,9 | 43,2 | 0,02 | 0,32 | **8,4 s** |
| Ordner | 5.821 | **183,7** | 180,1 | 183,5 | 0,07 | 0,44 | **41,0 s** |
| beide | 7.419 | **309,4** | 303,4 | 309,8 | 0,10 | 0,48 | **55,5 s** |

`draw()` je Bild **mit** Flush (`getImageData`): jedes `draw()` beginnt mit `clearRect`; ohne Flush verwirft Chromium die noch
nicht gerasterten Befehle der Vorbilder — der **erste** Lauf der Probe zeigte deshalb 9,9 ms für „beide" statt 309 ms (Falle, in der
Probe dokumentiert). Je Kante: durchgezogen ≈ 6 µs, **gestrichelt** ≈ 25–31 µs (Tag `[4,4]`, Ordner `[1.5,3]`) — die Strichelung
ist ein Mehrfaches der Kosten **je Kante**.

### 5.2 Urteil je Hypothese (§2)

| # | Urteil | Beleg |
|---|---|---|
| K1 | **bestätigt** | Ordner-Cliquen: 5.728 Kanten bei vier Ordnern (80/60/40/12); allein sie kosten 180 ms je Bild |
| K2 | **bestätigt — die Hauptkosten** | `drawEdges()` = 98 % von `draw()` (303 von 309 ms); ein `stroke()` je Kante, Strichelung teuer |
| K3 | **widerlegt** | `neighborRings()` 0,1 ms bei 7.419 Kanten; Hover kostet **nichts** extra (309,8 vs 309,4). 18.1 (c) entfällt als Kostenhebel |
| K4 | **widerlegt als Kosten, bestätigt als Form** | `applyForces()` 0,5 ms; die Simulation dauert **nur**, weil jedes der 129 Bilder `draw()` ruft (129 × 309 ms ≈ 40 s + Planung). Das Bild zeigt aber: mit Ordnern zieht die Clique je Ordner **alle Items zu einem Klumpen**, weg von der Region des Spaces (`b18_0_ordner.png`) |
| A1 | **nur teilweise** | `slot` = 2 · 250 + 40 = 540 px (der größte Space hat Radius 250), der Ein-Item-Space (Radius 52) sitzt auf dem Gitterplatz. Gemessen: Abstand seines Punkts zum nächsten **fremden Umriss** 63 px = **1,6 × `REGION_GAP`** im Zustand „aus" — also schon **unter** dem Ziel von 18.2 (≤ 2 ×); im Zustand „Ordner" 129 px = 3,2 ×. Das Bild „aus" zeigt den Einzelpunkt unten rechts in eigenem Umriss — **so** sieht das Foto des Nikingers aus, aber nicht **so weit** draußen |
| A2 | **nicht die Ursache** | Der Zoom ohne die drei weitesten Knoten wäre 0,69 statt 0,6 („aus"); der Ein-Item-Space ist **nicht** der Rand der Welt. Im Tag-Zustand ändert das Weglassen **nichts** (0,5 bleibt, §5.3) |
| A3 | **offen** | Die Wegwerf-Instanz hat keine gemerkte Ablage (`pinned_beim_start` = 0) — A3 lässt sich hier **nicht** zeigen. Entscheidend ist der Gegentest des Nikingers: im Live-Browser einmal „Layout zurücksetzen" (nur `localStorage`, nichts am Server) — **Antwort steht aus** |

### 5.3 N1 — neuer Befund: im Tag-Zustand wird die Karte auseinandergeschleudert

Im Zustand „Tags" ist die Welt **1.876 × 4.344 px** groß (sonst ≈ 1.500 × 1.650), der Zoom klemmt auf `ZOOM_MIN` = 50 %, und das
Bild zeigt einen riesigen Bogen quer durch die Karte (`b18_0_tags.png`). **Spur der Simulation** (`tags_spur` im Beleg, Hook um
`integrate()`): schon im **5. Bild** (alpha 0,43) hat ein Knoten die Geschwindigkeit **28.104 px je Bild**; der Abstand des
weitesten Knotens vom Ursprung springt von 1.249 px (Bild 0) auf **30.867 px** (Bild 10), pendelt gedämpft zurück und bleibt bei
**≈ 2.950 px** stehen. Die drei weitesten Knoten (alle `deg` 11–12, im Tag-Zustand der höchste Grad) liegen 2.757–2.790 px vom Median.
**Das ist ein Ausreißer-Mechanismus, den weder A1 noch A2 noch A3 erklärt** — und er passt auf die Beobachtung des Nikingers („erst mit
Ordnern/Tags", „Zoom 50 %", „Einzelpunkt in eigenem Umriss": ein weggeschleuderter Knoten bekommt seinen **eigenen** Lappen).
**Hypothese (nicht bewiesen):** Instabilität des expliziten Euler-Schritts — Federkraft × Grad übersteigt die Stabilitätsgrenze, der
Schritt ist nicht begrenzt. Test für 18.2: Geschwindigkeits-/Schrittgrenze oder Federstärke je Grad; Messgröße = größte Geschwindigkeit
je Bild und Welt-Umriss.

### 5.4 Folgerung für 18.1/18.2

* **18.1 (a) allein reicht nicht:** der Stern macht aus 5.728 Ordner-Kanten **188** (79 + 59 + 39 + 11), die **1.598 Tag-Kanten**
  kosten im Tag-Zustand **allein 42 ms** (> 16 ms-Ziel). Hebel in der Reihenfolge der Kosten: **Strichelung** (4–5 × je Kante),
  gebündeltes Zeichnen (b), und eine Entscheidung zur **Tag-Clique** (Stern auch für Tags? `TAG_CLIQUE_LIMIT` senken?) — **Nikinger**.
* **18.1 (c) entfällt** (K3 widerlegt), (d) nur wenn nach (a)+(b) noch nötig.
* **18.2 ist größer als geplant:** N1 braucht einen Eingriff in die **Kräfte** (nicht in die Anker). Das ändert die Karten-Physik von Block 14
  (Determinismus-Wächter P10.5-65, Stabilität P10.5-68) — Scope-Änderung ⇒ **Nikinger entscheidet** (Frage im Session-Block).
