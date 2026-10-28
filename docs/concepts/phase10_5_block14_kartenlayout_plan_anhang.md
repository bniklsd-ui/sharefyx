---
status: archive
purpose: L3-Anhang zum Plan des Kartenlayouts (Block 14) — die Abschnitte §0 (der Befund), §3 (die Entscheidungen des Nikingers), §6 (der Startauftrag) und die **Anmerkungen der Schritte 14.0–14.4**, verbatim aus dem Plan verschoben, weil der Plan über dem Softcap stand.
read-when: wenn zu Block 14 der Befund, die Entscheidungen E1–E4, der Startauftrag oder die Messnotizen der Schritte 14.0–14.4 gebraucht wird — der Plan trägt §1/§2/§4/§5
detail: L3
up: ../../ROADMAP.md
down:
  - phase10_5_block14_kartenlayout_plan.md   # 📗 der Plan (die Abschnitte, die hier stehen)
  - ../../phase10_5_finishing/CLAUDE.md       # der Phase-Head (Modulstatus Block 14)
updated: 2026-10-28 (Block 14.5: die **Anmerkungen der Schritte 14.0–14.4** hierher verschoben — der Plan stand bei 42.237 B; der Rand-Fall aus §2.5 ist gemessen: die Lappen-Kontur stand 3,8 px über dem Leinwandrand, `FIT_MARGIN` 40 → 56 px) | 2026-10-27 (Block 14.4: §0, §3 und §6 aus dem Plan hierher verschoben — der Plan stand bei 40.054 B und damit am Softcap)
---
# Anhang zum Kartenlayout-Plan (Block 14) — §0, §3, §6 und die Anmerkungen 14.0–14.4

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

### Die Schritte 14.0 bis 14.4 — die Anmerkungen (abgeschlossen)

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
