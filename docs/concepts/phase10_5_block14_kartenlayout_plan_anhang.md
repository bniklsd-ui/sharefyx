---
status: archive
purpose: L3-Anhang zum Plan des Kartenlayouts (Block 14) — die Abschnitte §0 (der Befund), §3 (die Entscheidungen des Nikingers) und §6 (der Startauftrag), verbatim aus dem Plan verschoben, weil der Plan über dem Softcap stand.
read-when: wenn zu Block 14 der Befund, die Entscheidungen E1–E4 oder der Startauftrag gebraucht wird — der Plan trägt §1/§2/§4/§5
detail: L3
up: ../../ROADMAP.md
down:
  - phase10_5_block14_kartenlayout_plan.md   # 📗 der Plan (die Abschnitte, die hier stehen)
  - ../../phase10_5_finishing/CLAUDE.md       # der Phase-Head (Modulstatus Block 14)
updated: 2026-10-27 (Block 14.4: §0, §3 und §6 aus dem Plan hierher verschoben — der Plan stand bei 40.054 B und damit am Softcap)
---
# Anhang zum Kartenlayout-Plan (Block 14) — §0, §3, §6

> **Warum dieses Archiv existiert (2026-10-27, Schritt 14.4).** Der Plan
> `docs/concepts/phase10_5_block14_kartenlayout_plan.md` stand beim Bau von Schritt 14.4 bei
> **40.054 B** — am Softcap (40.960 B). Der 14.4-Schritt (die Messung der Startwerte) und die
> datierten Korrekturen der Abnahme-Zelle P10.5-66 (der wirksame Gegenlauf) wären über die
> Grenze gegangen. Die drei Abschnitte, die **vor dem Bau** stehen und mit dem Bau nichts mehr
> zu tun haben, sind deshalb **hierher gewandert — verbatim** (`scripts/move_sections.py`,
> mit Byte-Gegenprobe). Im Plan bleibt an jeder Stelle die **Überschrift** stehen, darunter ein
> Zeiger: Querverweise wie „Plan §0" landen weiter auf einer Überschrift.
>
> **Was im Plan bleibt:** §1 (das Prinzip), §2 (der Entwurf im Detail), §4 (die Schritte mit
> ihren datierten Notizen) und §5 (die Abnahme P10.5-65–71) — sowie eine **Kurzfassung** der
> gelockten Entscheidungen unter §0. **Was hier steht:** der Befund (§0, mit den datierten
> Korrekturen und der vollständigen Liste der gelockten Entscheidungen), die Entscheidungen des
> Nikingers vor dem Bau (§3, E1–E4) und der Startauftrag des Ausführers (§6, mit den
> Anker-Zeilennummern).

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

## §3 Entscheidungen für den Nikinger (vor dem Bau)

| # | Frage | Empfehlung |
|---|---|---|
| **E1** | Schlüssel `v1` → `v2`? | **Entfällt** (Nikinger 2026-10-26: „no browser has yet seen the new design“ — KA-2 nie live, §2.6) |
| **E2** | Eigene Farbtöne je fremdem Space? | **Nein** — nach den neuen Bildern neu entscheiden (Nikinger 2026-10-26) |
| **E3** | `ZOOM_MIN` senken, falls 200 Knoten bei 0,5 nicht passen? | **Frei** (Nikinger 2026-10-26) — der Ausführer senkt bei Bedarf, nennt Wert und Messung im Bericht |
| **E4** | Überlappende Beschriftungen? | **In Block 14** (Nikinger 2026-10-26) — §2.7, Schritt 14.35 |


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
