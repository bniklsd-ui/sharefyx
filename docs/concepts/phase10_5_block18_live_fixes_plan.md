---
status: live
purpose: Mini-Plan Block 18 „Live-Funde nach Deploy D" — Karte ruckelt mit Tags/Ordnern, einzelne Punkte weit draußen, Editor-Farben (Wahl). Befunde am Code, Hypothesen, Schritte 18.0–18.5, Entscheidungen E1–E4 (beantwortet). Ausführer: eine eigene Session.
read-when: Ausführung von Block 18 — zuerst §1 (Auftrag), §4 (Entscheidungen) und §3 (Schritte)
detail: L2
up: ../../phase10_5_finishing/CLAUDE.md
down:
  - ./phase10_5_block14_7_plan.md   # 📗 die Kartengeometrie (Hex-Anker, LOBE_SCALE), auf der 18.2 aufsetzt
updated: 2026-11-01 (E1–E4 beantwortet: Stern, Farben → P11, v4.0.1, Zeilen 18/49 als Wegwerf-Probe 18.5) | 2026-11-01 (Mini-Plan, Claude Code — Live-Sichtung des Nikingers nach Deploy D)
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
| 18.0 | **Messen** an der Wegwerf-Instanz mit einer Saat in Live-Form (≈ 200 Items, 5–7 Spaces, 2–3 Ordner mit 40–80 Items, ein Space mit **1** Item, Tags wie live). Je Zustand (aus / Tags / Ordner / beide): Kantenzahl, ms je `draw()` (`performance.now()` um `draw`, 60 Bilder Pan), Dauer der Simulation. Ausreißer: reproduzieren, dann „Layout zurücksetzen" — bleibt er (A1) oder geht er (A3)? Die Saatzahlen vorher beim Nikinger erfragen (er kennt die Live-Form; **kein** Lesen des echten `DATA_ROOT`) | Tabelle im Plan §5, Ursache für Ausreißer benannt |
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

## 5. Messungen (füllt der Ausführer)

*(leer — 18.0)*
