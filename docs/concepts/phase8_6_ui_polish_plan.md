---
status: snapshot
purpose: ausführungsreifer Plan für Phase 8.6 — Selektions-/Layering-Welle, Struktur-Reorg, drei Graph-Fixes, Radiogruppe-Rückbau, Deploy v3.0.2
read-when: vor jedem P8.6-Commit; §0.2 (Locks) und §0.3 (Tabu) vor dem ersten Code-Touch, danach der jeweilige Block-Abschnitt
detail: L2
up: ../../ROADMAP.md
down:
  - ./PHASE8_5_CLOSEOUT_HANDOVER.md                 # Einstieg, §4 = die offenen Entscheidungen, die hier gelockt werden
  - ./p8x_ui_polish_notes.md                        # Inhaltsquelle §1–§10; diese Datei erklärt sie, ersetzt sie nicht
  - ./phase8_5_picker_release_plan.md               # §9 P8.5-Closeout, P8.5-F = Herkunft des Radiogruppe-Streits
  - ./phase8_ui_graph_plan.md                       # §9 P8-Closeout, §0.3 Verbotsliste, §5 D2 Graph
  - ./sichtpruefung_automation_conventions.md       # Statusregel + Konventionen §1–§4
  - ./sichtpruefung_automation_tooling.md           # Vision-Plugin, Step V
updated: 2026-09-09 (Erstfassung, Claude-Code-Planungssession gegen main@d1af51b)
---

# Phase 8.6 — UI-Politur: Selektions-Welle + Layout (Plan)

> **Mission, ein Satz:** Die App bekommt **ein** Selektions-Design für alles Klickbare,
> ein benanntes Drei-Layer-System statt fünf duplizierter Blau-Verläufe, den Rail- und
> Übersichts-Umbau aus §1, drei Graph-Fixes und den Radiogruppe-Rückbau — und geht als
> **`v3.0.2`** live.
>
> **Ausführender:** opencode/M3, ohne Advisor (N4 aus P8, unverändert). Ersatz ist die
> Selbstprüf-Checkliste §0.5 plus die Nikinger-Sichtprüfung §7.
>
> **Planungsstand:** `main`@`d1af51b`, Arbeitsbaum sauber, Live-Instanz `v3.0.1`
> (Release `20260905T140325.378914Z`, PID 355956). Alle `Datei:Zeile`-Anker in diesem
> Plan sind gegen genau diesen SHA gemessen — **V106** ist der Sammelmarker dafür.

---

## §0 Rahmen

### §0.1 Die vier Nikinger-Fragen, beantwortet (2026-09-09)

| # | Frage | Antwort des Nikingers |
|---|---|---|
| **N1** | Wie groß ist P8.6? | **„Selektions-Welle + Layout"** — §5 Layering + §10.1–§10.7 + §6 + §3 + Radiogruppe-Rückbau **plus** §1 Spaces-Layout-Reorg + §10.4 klickbare Spaces + §2.3/§2.4 Map-Layout-Bugs. |
| **N2** | V102 — Zwillingskante? | **Dedup in `graph.js` beim Zeichnen.** Kein Server-Touch, **keine neunte P1-Contract-Öffnung.** |
| **N3** | §6 — welche Lesart des „Vertauschens"? | **(b) Beide neu platzieren:** „Einstellungen" nach oben, „Abmelden" ans Rail-Ende. |
| **N4** | §10.7 — Farbausnahme für Abmelden/Archivieren? | **Dritte Kategorie.** Die Selection/Choice-Konvention bekommt eine benannte Kategorie für Aktionen mit Rückweg-Kosten, nicht zwei Einzelfälle. |

**Nummern-Randnotiz (kein Plan-Bestandteil, aber gelockt):** der Nikinger hat die
Nummerierungsfrage aus `PHASE8_5_CLOSEOUT_HANDOVER.md` §4.5 entschieden — es gibt **kein
P8.7**. Sein „eher v3.1 also p8.7" meint das, was die Dokumente **P9 → `v3.1.0`** nennen.
Die verbundenen AI-Sessions (§10.8) sind damit **P9**, nicht P8.6. Nichts wird umbenannt.

### §0.2 Gelockte Entscheidungen

| ID | Entscheidung | Begründung |
|---|---|---|
| **P8.6-A** | Phasenverzeichnis **`phase8_6_ui_polish/`**, Plan-Doc **`docs/concepts/phase8_6_ui_polish_plan.md`**, Head **`phase8_6_ui_polish/CLAUDE.md`**. | Fortführung des Schemas `phase<N>_<slug>/`. Schließt die offene Namensfrage aus `p8x_ui_polish_notes.md` §D und `PHASE8_5_CLOSEOUT_HANDOVER.md` §4.5. `phase9_ui_polish/` fällt weg — P9 ist der Graph-Umbau, nicht diese Phase. |
| **P8.6-B** | **Ein Dokument pro Phase.** Dieser Plan ist Konzept, Plan und (ab Step Z) Closeout in einem; §9 wird gefüllt. Ein separates Handover-Dokument entsteht **nur**, wenn der Nikinger es im Closeout-Auftrag ausdrücklich anordnet. | P8-N, unverändert. Präzedenz für die Ausnahme: P8.5-R wurde 2026-09-09 vom Nikinger selbst umgekehrt — das war eine Anordnung, kein Default. |
| **P8.6-C** | **Ein neuer Token `--select-fill`** ersetzt die **fünf** rohen `rgba(62,141,243,…)`-Vorkommen außerhalb `:root` (`app.css:403`, `:685`, `:719`, `:785`, `:1291`). Hover bekommt `--select-fill-quiet` (derselbe Verlauf, halbe Deckkraft). | §10.2/§10.5 verlangen „Hover = Standardauswahl, nur transparenter". Das ist **kein zweites Design**, sondern ein zweiter Alpha-Wert — also ein zweiter Token auf demselben Blau, nicht ein zweiter Blauton. Der Ist-Zustand hat denselben Verlauf **viermal wörtlich** dupliziert; jede künftige Änderung müsste vier Stellen treffen. |
| **P8.6-D** | **Layer-Tokens werden benannt, aber nicht umbenannt.** Neu: `--bg-void: #000`. Bestehend bleibt: `--bg` (#0B0D10) = Layer 1, `--glass-*` = Layer 2. **Kein Rename von `--bg`/`--surface`.** | §5 will drei benannte Layer. Ein Rename von `--bg` träfe ~40 Stellen für null sichtbaren Gewinn und würde den Diff unlesbar machen. Der fehlende Teil ist nur Layer 0 — genau **ein** neuer Token. Die Dokumentation der Zuordnung passiert im `:root`-Kommentar, nicht durch Umbenennung. |
| **P8.6-E** | **`--bg-void` wird sparsam eingesetzt:** genau drei Stellen — Login-/Boot-Hintergrund, `.list__empty`, `.overview__graph-empty`. Keine weitere. | §5 sagt „wenig vorhanden, auf echten OLED-Displays cool". Ein Layer, der überall liegt, ist kein Layer, sondern der neue Standard. Die drei gewählten Stellen sind alle „nichts da" — genau der Zustand, für den echtes Schwarz die richtige Aussage ist. |
| **P8.6-F** | **Dritte Kategorie heißt „Vorsicht" (`--caution`), und sie ist `--danger` unter neuem Namen — kein neuer Farbwert.** `--danger: #E5484D` trägt bereits den Kommentar `/* Widerruf, Archivieren */` (`app.css:57`). `--caution` wird als Alias daneben definiert und für „Abmelden"/„Archivieren" verwendet; `--danger` bleibt für Fehler/Toasts. | N4. Der Kommentar an `--danger` zeigt, dass die Kategorie **konzeptuell schon existiert** und nur nie angewendet wurde. Einen zweiten Rotton zu erfinden wäre Farbe ohne Bedeutung — Phase-8-§0.3-Verbot Punkt 4. **Zwei Namen auf einem Wert** ist die ehrliche Abbildung: gleiche Farbe, zwei Anlässe. |
| **P8.6-G** | Die Kategorie „Vorsicht" wird **als fünfte Kategorie in die Selection/Choice-Konvention v3** geschrieben (`phase8_ui_graph/CLAUDE.md:254 ff.`), nicht in ein neues Dokument. | Die Konvention ist der etablierte Ort und wird ohnehin bei jedem UI-Commit gelesen. Ein zweites Konventions-Dokument wäre die zweite Kopie derselben Regel — genau das, was `DOC_LAYERS_CONVENTION.md` verbietet. |
| **P8.6-H** | **Radiogruppe → `<select class="input">`**, Beschriftung **in** der Box (erste `<option>` als Label-Träger entfällt; stattdessen `<label class="input-label-inline">` im selben `.input`-Träger). `localStorage["sfx:linkpicker:mode"]` bleibt unverändert. | Nikinger-Anordnung 2026-09-08, Handover §4.2. Das stellt die Selection/Choice-Konvention wieder her (Kategorie *Choice* = nativ `<select>`), von der P8.5-19 die dokumentierte Ausnahme war. Der Persistenz-Key bleibt, damit bestehende Browser ihre Wahl behalten. |
| **P8.6-I** | Der Test `test_link_picker_uses_a_radio_group_not_a_select` (`phase5_ui/tests/test_static_routes.py:258`) wird **umgekehrt und umbenannt** zu `test_link_picker_uses_a_select_not_a_radio_group`, Docstring trägt die Historie beider Richtungen. | Handover §4.2 wörtlich: „der Testname wird sonst zur Lüge". Löschen wäre schlechter als umkehren — der Test ist der einzige Ort, an dem die Bauform-Entscheidung maschinell festgehalten ist. |
| **P8.6-J** | **§1 Kippschalter:** „Alle Items" wandert im Rail **unter** die Spaces (ein Aufruf-Umzug in `tree.js :: renderRail()`), und wird **kein** neuer Kippschalter. Der „Kippschalter" des Nikingers **ist** der bestehende `#home-button`/`.tree__scope`-Mechanismus. | `renderRail()` (`tree.js:242-255`) ruft `renderScopeRow()` heute als **erstes** auf (Z. 244) — daher steht „Alle Items" oben. Der Umzug ist **eine verschobene Zeile**. Ein *zusätzlicher* Kippschalter neben `#home-button` und `.tree__scope` wäre ein drittes Element für dieselbe Frage — das ist genau das „doppelte Elemente", das der Nikinger vermeiden will. **[VERIFY] V110** — in der Sichtprüfung bestätigen lassen. |
| **P8.6-K** | **§1 Map-Breite:** `.overview__graph` verliert `max-width: 960px` und wird im Übersichts-Modus zur rechten Spalte eines zweispaltigen `.overview`-Grids (`grid-template-columns: 1fr 40%`, `grid-template-rows: auto 1fr`). `.overview` selbst holt seine Höhe über **`flex: 1; min-height: 0`** aus dem `.detail`-Flex-Container — **nicht** über `height: 100%`. | §1 wörtlich: „ca. 40 % der gesamten Seite … und gesamte Höhe". Grid **innen**, damit die Zeile `1fr` eine definite Höhe an das Canvas weitergibt; Flex **außen**, weil `.overview` Geschwister in `.detail` hat und eine Prozenthöhe gegen deren Präsenz rechnen würde. Ausführlich: §5.3. Das ist zugleich der Fix für §2.3 (P8.6-L). |
| **P8.6-L** | **§2.3 (Map schneidet unten ab) ist ein Höhen-Bug, kein Overflow-Bug.** `.overview__graph` (`app.css:915-924`) hat `min-height: 55vh` und **keine** `height`; das Kind `canvas` hat `height: 100%` (`app.css:928`) — ein Prozent-Wert gegen eine indefinite Höhe. Fix ist die definite Höhe aus P8.6-K, **nicht** ein `overflow`-Tausch. | Prozentuale Höhen brauchen einen Elternteil mit definiter Höhe; `min-height` ist keine. Das Canvas fällt damit auf seine Attribut-Höhe zurück, während `resize()` (`graph.js:474-484`) die Attribute aus `getBoundingClientRect()` setzt — eine Rückkopplung, die je nach Reihenfolge unten abschneidet. **[VERIFY] V112** — vor dem Fix messen, nicht nur reparieren. |
| **P8.6-M** | **§2.4 (Map fliegt) wird über einen deterministischen Seed gelöst, nicht über gespeicherte Positionen.** `seedInitialPositions()` (`graph.js:248-263`) ersetzt `Math.random()` (Z. 260/261) durch einen Hash der Item-ID. | Ein `localStorage`-Layout-Snapshot löst ein anderes Problem („Position beim Wiederöffnen behalten") und bringt ein Invalidierungs-Problem mit (Knoten kommen und gehen). Der Seed ist ~8 Zeilen und behebt genau das gemeldete Symptom: gleiche Daten ⇒ gleiches Bild. |
| **P8.6-N** | **V102-Dedup in `graph.js:156`**, unmittelbar bei der Übernahme von `data.edges` — nicht erst in `drawEdges()`. Schlüssel ist das ungeordnete Paar `min(src,dst)+"|"+max(src,dst)`; `kind` des ersten Treffers gewinnt. | N2. Bei der Übernahme, weil dann **jeder** Konsument im Frontend (Zeichnen, Nachbarschafts-Hervorhebung `drawLabels()`, Hit-Testing) dieselbe deduplizierte Liste sieht. Ein Dedup erst in `drawEdges()` (`graph.js:389`) würde die Doppelkante aus dem Bild nehmen, aber in der Kanten-Zählung stehen lassen. |
| **P8.6-O** | **§3 Ordner-Anzahl wird clientseitig aus bereits geladenen Daten abgeleitet — kein neuer Endpunkt, keine Erweiterung von `_overview`.** | `_overview` (`api.py:594-623`) macht heute schon **eine `store.search()` pro Bucket pro sichtbarem Space** plus eine für „Zuletzt benutzt" (`api.py:603-614`). In der Budget-Messung ist das der teuerste UI-Endpunkt (~863 ms, siehe §1.7). Ordner-Counts dort anzuhängen würde die Suchaufruf-Zahl noch einmal mit der Ordnerzahl multiplizieren. |
| **P8.6-P** | **§10.4 klickbare Spaces:** die Zeile `.overview__space-row` wird als Ganzes klickbar (Navigation in den Space), die bestehenden `.overview__space-count`-Chips behalten ihr `stopPropagation()` (`list.js:67-79`). | Ohne das wäre ein Space mit lauter Null-Zählern **überhaupt nicht** anklickbar — `list.js:66` überspringt Null-Chips (`if (!count) return;`). Genau dieser Fall ist der Grund für den Wunsch. Kategorie ist *Navigation* nach der Konvention v3, nicht *Choice*. |
| **P8.6-Q** | **`.btn:hover` und `.btn-primary:hover` verlieren ihre hartkodierten Hex-Verläufe** (`app.css:219` `#323A45,#212832`; `app.css:238` `#6EACF9,#3781E2`) und bekommen Token. | §10.7 („alles Klickbare selbiges Design") ist nicht durchsetzbar, solange die beiden meistbenutzten Knopf-Klassen ihre Hover-Farbe an den Token vorbei setzen. Fällt beim Selektions-Sweep ohnehin an. |
| **P8.6-R** | **Deploy-Ziel bleibt `v3.0.2`** (Patch-Bump), obwohl P8.6 das `.shell`/`.overview`-Layout anfasst. | ROADMAP-Zeile 38 und `project_ui_version_scheme` sind eindeutig; die Größenklassen-Regel bindet den Minor-Bump an P9 (Graph-Umbau). §1 verschiebt Flächen, ändert aber **keine** Informationsarchitektur — Rail, Liste und Detail bleiben, was sie sind. **Wenn der Nikinger es in der Sichtprüfung anders sieht, ist `v3.1.0` seine Entscheidung, nicht die des Ausführenden.** |
| **P8.6-S** | **Keine neunte P1-Contract-Öffnung.** `storage/` wird in dieser Phase nicht angefasst. | N2 hat den Server-Weg für V102 verworfen; §3 kommt ohne Index-Änderung aus (P8.6-O). Damit gibt es in P8.6 keinen Anlass — und ohne Anlass wird nicht geöffnet. |
| **P8.6-T** | **Ein `## Session stopped`-Block pro Session** im Phase-Head, danach `scripts/rotate_session_block.sh`. **Nicht** das Phase-8.5-Muster (ein `##` mit mehreren `###`). | Das Skript zählt `##`-Überschriften (`rotate_session_block.sh:31,44-45`) und meldet beim P8.5-Muster fälschlich „bereits konform" — Handover §8. Die Konvention ans Werkzeug anzupassen ist billiger, als das Werkzeug für jede Phase neu zu prüfen. |
| **P8.6-U** | **Reihenfolge ist Fundament → Fläche → Struktur → Graph.** Block A legt Tokens, Block B verbraucht sie, Block C baut um, Block D repariert den Graphen. Kein Block überspringt seinen Vorgänger. | Wer §10.1–§10.7 vor dem Token-Fundament baut, schreibt fünf Mal denselben Verlauf ein sechstes Mal hin. Blocks C und D sind unabhängig voneinander und **dürfen** getauscht werden; A vor B ist zwingend. |

### §0.3 Tabu — was in dieser Phase nicht angefasst wird

Übernommen aus Phase 8.5 §0.3, für P8.6 neu bewertet und **unverändert bestätigt**
(`p8x_ui_polish_notes.md` §C-6 hat das ausdrücklich verlangt):

| Pfad | Status in P8.6 |
|---|---|
| `phase1_storage/storage/**` | **Tabu.** Keine Ausnahme (P8.6-S). |
| `phase4_auth/authserver/**` | **Tabu.** Keine Ausnahme. |
| `phase2_mcp/mcpserver/**` | **Tabu.** Keine Ausnahme — auch nicht der Hint-Text (das war eine P8.5-Ausnahme mit eigener Begründung). |
| `phase5_ui/webui/{security,api,serializers,permissions}.py` | **Tabu.** §3 kommt clientseitig aus (P8.6-O). |
| `phase5_ui/webui/static/**` | **Erlaubt** — das ist die Arbeitsfläche der Phase. |
| `phase5_ui/webui/pages.py` | **Erlaubt, aber nur für Template-/Routing-Trivialitäten.** Wenn ein Schritt hier mehr als eine Zeile braucht: an den Nikinger eskalieren. |
| `phase5_ui/tests/**`, `phase8_6_ui_polish/scripts/**` | **Erlaubt.** |

**Tabu-Diff-Pflicht:** vor jedem Commit
`git diff --stat -- phase1_storage/storage phase4_auth/authserver phase2_mcp/mcpserver phase5_ui/webui/security.py phase5_ui/webui/api.py phase5_ui/webui/serializers.py phase5_ui/webui/permissions.py`
— die Ausgabe muss **leer** sein. Eine nicht-leere Ausgabe ist ein Abbruchgrund, kein Kommentar-Anlass.

### §0.4 Was draußen bleibt

**Aus `p8x_ui_polish_notes.md`, bewusst nicht in P8.6:**

- **§2.1 Map-Performance („Reload-Overload")** und **§2.2 Map-Stil („Landkarte")** und
  **§2.5 Karte einklappen** → **P9**, der Graph-Umbau. P8.6 fasst am Graphen nur die drei
  benannten Defekte an (V102, §2.3, §2.4).
  **Eine Ausnahme, benannt statt versteckt:** der nicht abgebrochene
  `requestAnimationFrame`-Lauf (§6.4 unten) ist §2.1-Gebiet, wird aber mitgenommen —
  Begründung dort.
- **§4 Edit-in-Place** → eigene Phase. Berührt Hard Rule 3 und P7-24; das ist keine Politur.
- **§7 De-AI-ierung Lauf 2** → eigene, recherchelastige Claude-Code-Session. Der positive
  Regelsatz, den §7 will, kann nicht nebenbei entstehen.
- **§8 Tags** und **§9 Feedback-Button** → nach P8.6. Beide brauchen laut §C-6/§C-8 eine
  **neue** Tabu-Bewertung (Server-Fläche); P8.6 wollte gerade keine.
- **§10.8 verbundene AI-Sessions** → **P9 / `v3.1.0`** (Nikinger-Entscheidung, §0.1).
- **§10.9 Hochkant-/Handy-UI** → benanntes Zukunfts-Item, **kein P8.6-Auftrag**
  (Handover §4.6).
- **„Ordner umbenennen"** → **bewusst draußen, mit Analyse** (Nikinger-Frage 2026-09-10,
  §0.4.1 unten). Kurz: die billige Fassung hat zwei stille Fehlermodi, einer davon ändert
  Rechte als Nebenwirkung.
- **§4.3 des Handovers (CSRF-Origin-Mismatch bei Wegwerf-Instanzen)** → kein Reverse-Proxy,
  kein TLS-Terminator für Wegwerf-Setups. POST-Pfade bleiben live-only.
  **Begründung:** die Sichtprüfung dieser Phase ist zu 90 % GET-/Render-Prüfung; ein
  TLS-Terminator wäre Infrastruktur für einen Nutzen, den P8.6 nicht hat. Der Punkt bleibt
  offen und wandert unverändert in §9.

#### §0.4.1 „Ordner umbenennen" — warum nicht in P8.6 (Analyse vom 2026-09-10)

**Der Befund, der alles entscheidet:** ein Ordner ist ein **echtes Verzeichnis** unter
`DATA_ROOT/<space>/<folder>/`. Das Feld `folder` steht **nie im Frontmatter** — es wird bei
jedem Lesen aus dem Dateipfad abgeleitet (`storage/files.py:156-159`, `folder_from_path()`,
ausdrücklich „`folder` ist immer abgeleitet, nie Frontmatter"). Umbenennen heißt also:
**jede Datei im Ordner physisch verschieben.** Es gibt im gesamten Code **kein** Umbenennen
und **kein** Löschen von Ordnern — `Store.ensure_folder()` (`store.py:377-390`) ist ein
reines `mkdir`.

**Was trotzdem schon da ist, und mehr als erwartet:**

| Baustein | Anker | Bedeutung |
|---|---|---|
| `Store.move(id, version=, folder=)` | `store.py:682-751` | verschiebt **ein** Item, genau ein Git-Commit, genau ein Versionssprung |
| `PATCH /api/v1/items/{id}` mit `folder` | `api.py:895-948` | die Fläche dafür existiert, Eigentümer-Space-only (`api.py:876-879`) |
| **`_cleanup_emptied_folders()`** | `store.py:753-770` (P6-AF) | räumt nach jedem Move **leer gewordene Quellordner** auf, aufwärts bis zur Space-Wurzel |
| Mehrfachauswahl + Verschieben-Dialog + `#move-progress` | `app.html:306`, `dialogs.js:656-658` | Fortschritts- und Teilfehler-Anzeige existiert bereits |
| `MAX_FOLDER_DEPTH = 2` | `files.py:19` | höchstens `a/b` — das Unterordner-Problem ist klein und endlich |

**Damit wäre eine reine Frontend-Umbenennung möglich:** alle Items des Ordners einsammeln,
je ein `PATCH` mit neuem `folder` und der gelesenen `version`, fertig — der Quellordner
verschwindet von selbst. **Kein `storage/`-Touch, keine neunte P1-Contract-Öffnung.**
Aufwand realistisch **60–80 Zeilen JS**, weil Dialog, Fortschritt und Move-Maschinerie schon
stehen. Nebenbei: **umbenennen geht heute schon von Hand** — Mehrfachauswahl → Verschieben →
Zielordner. Es ist eine Ergonomie-Lücke, keine Fähigkeitslücke.

**Und genau deshalb wird sie hier nicht gebaut. Die billige Fassung hat zwei Löcher, die
man nur serverseitig schließt:**

1. **Ein leerer Ordner lässt sich nicht umbenennen.** Es gibt nichts zu verschieben,
   `_cleanup_emptied_folders()` feuert nie, und ein `rmdir` an der API gibt es nicht. Das
   Ergebnis wäre: neuer Ordner angelegt, **alter bleibt für immer stehen**. Der
   `rglob`-Walk in `store.spaces()` (`store.py:364-369`) listet ihn weiter, weil ein leeres
   Verzeichnis dort ein vollwertiger Ordner ist.
2. **Ein geteilter Ordner verliert still seine Freigabe.** `_cleanup_emptied_folders()`
   bricht **absichtlich** ab, wenn eine `.share.yml` im Verzeichnis liegt (der Kommentar
   dort sagt warum: „eine bewusste Freigabe eines Menschen ist kein Rest"). Nach der
   Umbenennung lägen die Items im **neuen** Ordner — **ohne** `.share.yml` —, und die
   `.share.yml` bliebe im alten, jetzt leeren. **Die Freigabe gilt danach für nichts mehr.**
   Das ist eine Rechteänderung als Nebenwirkung einer Umbenennung, also genau die Klasse
   von Fehler, gegen die Hard Rule 4 geschrieben wurde.

**Loch 2 ist der Grund für die Vertagung, nicht der Aufwand.** Eine Umbenennung, die eine
Freigabe still fallen lässt, ist schlechter als keine Umbenennung — der Nutzer sieht einen
Erfolg und hat einen Rechteverlust. Eine Fassung, die geteilte und leere Ordner mit einer
klaren Meldung **ablehnt**, wäre ehrlich, aber ein Umbenennen, das bei den interessanten
Ordnern nicht geht, ist ein halbes Feature in einer Politur-Phase.

**Zwei kleinere Punkte, für die spätere Planung festgehalten:**
- **Es gibt keinen Anzeigenamen.** `validate_folder()` (`files.py:128-153`) slugifiziert
  jedes Segment — „Meine Projekte" *ist* `meine-projekte`. Umbenennen ist also
  Re-Slugifizieren; die Oberfläche muss zeigen, was daraus wird, bevor sie es tut.
- **Teilabbruch ist der Normalfall, nicht die Ausnahme.** N Items = N Schreibvorgänge mit
  je eigener `version`. Ein `ConflictError` bei Item 17 von 40 hinterlässt einen halb
  umbenannten Ordner. Es gibt keine Transaktion und kann keine geben (Hard Rule 3, Hard
  Rule 5). Die Oberfläche muss „23 von 40 verschoben" berichten können — `#move-progress`
  ist dafür schon da.

**Der vollständige Weg** wäre ein `Store.rename_folder()`, das das Verzeichnis umbenennt,
die `.share.yml` mitnimmt und den Index nachzieht — **die neunte P1-Contract-Öffnung**, die
**P8.6-S** gerade zugesperrt hat. Das ist eine bewusste Planungsentscheidung einer
Folgephase, kein Nachtrag.

**Empfehlung: notiert für P9 oder danach.** Diese Analyse ist der Ersatz für die
Wiederholung der Untersuchung — wer das Feature plant, startet hier und nicht bei null.

**Unverändert aus `p8x_ui_polish_notes.md` §B (Außenkanten):** Body-Volltextsuche (Q1),
Rechteverwaltung über MCP-Tools (P6-M), Löschen von Items (F2), FastMCP-4 (V79),
Funnel-Watchdog, **Realtime**, Light-Mode (P5-X), Glyph-Entscheidungen P6/P6.5,
Bulk-Append-MCP-Tool.

**Geerbtes Ledger** (Handover §4.7): P6-Zeilen 7/9/14–17/23/25/29/30, P6.5-14, O4/O5/O7,
`_trash/`-Räumung. P8.6 fasst davon **nichts** an und räumt **nichts** still ab.

### §0.5 Selbstprüf-Checkliste (Advisor-Ersatz)

Vor **jedem** Commit, in dieser Reihenfolge:

1. **Tabu-Diff** aus §0.3 — leer?
2. **`pytest -q`** grün? (Baseline §1.6.)
3. **`phase5_ui/scripts/ui_budget.py`** — 5/5 im Zielkorridor? (Baseline §1.7.)
4. **Verbotsliste Phase 8 §0.3** eingehalten? Kein Emoji-Icon, kein Gradient-Branding,
   kein 3er-Card-Grid, keine dekorative Farbe, keine neue Schriftfamilie, **kein Element,
   dessen Erkennbarkeit allein von Transparenz/Blur abhängt**.
5. **Kein rohes `rgba(62,141,243`** außerhalb von `:root` — `grep -n "rgba(62,141,243" phase5_ui/webui/static/app.css`
   darf ab Block A nur noch die `:root`-Zeilen treffen. Ab Block A ist das ein statischer Test (§8.2).
6. **Doc-Update im selben Commit** (Hard Rule 8): Modul-/Status-Tabelle **und**
   `## Session stopped`-Block im Phase-Head. Neue `.md` ⇒ Zeile in `docs/INDEX.md`.
7. **Kein `pkill -f`, kein `systemctl`** (Hard Rule 9). Wegwerf-Instanzen nur über
   PID-Datei oder Port stoppen.

**Eskalationsregel P8.5-O gilt weiter:** ein Fund, dessen Ursache in einer *früheren*
CSS-Regel oder in der Kaskade liegt, wird **nicht** symptomatisch gepatcht, sondern an
Claude Code eskaliert. Erkennungsmerkmal: „der Wert stimmt im Quelltext, sieht im Browser
aber anders aus."

**Neue Eskalationsregel P8.6-O2:** wenn ein Schritt aus Block C das `.shell`-Grid
(`app.css:327-332`) in einer Weise ändern will, die Rail-, Listen- **und** Detail-Breite
gleichzeitig betrifft, ist das ein Architektur-Schnitt und keine Politur → eskalieren.
Begründung: das 240px/380px/1fr-Raster ist seit Phase 5 die Grundlage jedes Screenshots
und jeder Sichtprüfung; es zu verschieben entwertet die gesamte Beweislage rückwirkend.

---

## §1 Step 0 — Haushalt und Verifikation

**Dieser Schritt ist bereits durchgeführt worden** (Planungssession, 2026-09-09, gegen
`main`@`d1af51b`). Die Befunde stehen unten; der ausführende Agent **behebt** sie, er
sucht sie nicht erneut.

### §1.1 Phasenverzeichnis anlegen

```
phase8_6_ui_polish/
  CLAUDE.md          # Phase-Head, L1-Card + Modul-Status-Tabelle + ein "## Session stopped"
  SESSIONS_ARCHIVE.md # leer angelegt, mit L1-Card (📦)
  scripts/           # Wegwerf-Smokes, siehe §7
```

Beide `.md` bekommen im **selben** Commit eine Zeile in `docs/INDEX.md`.

**Und eine Zeile in diesem Plan:** die `down:`-Liste im Frontmatter oben bekommt
`- ../../phase8_6_ui_polish/CLAUDE.md   # Phase-Head` **erst dann**, wenn die Datei
existiert. Sie steht dort bewusst noch nicht — ein Vorwärts-Verweis auf eine nicht
existierende Datei wäre genau der Befund, den §1.2 gerade abräumt, und würde die
Abnahmezeile P8.6-2 (Re-Scan meldet 0 Bruchstellen) reihenfolgeabhängig machen.

### §1.2 Befund 1 — sechs unauflösbare `up:`/`down:`-Links, alle in einer Datei

`docs/concepts/p8x_ui_polish_notes.md` — die Inhaltsquelle dieser Phase — hat **alle sechs**
Frontmatter-Links mit `../` statt `../../` geschrieben. Die Datei liegt in `docs/concepts/`,
die Pfade wurden aber notiert, als läge sie in `docs/`.

| Zeile | Ist | Soll |
|---|---|---|
| `up:` | `../CLAUDE.md` | `../../CLAUDE.md` |
| `down:` #1 | `../phase8_ui_graph/CLAUDE.md` | `../../phase8_ui_graph/CLAUDE.md` |
| `down:` #2 | `../phase8_5_picker_release/CLAUDE.md` | `../../phase8_5_picker_release/CLAUDE.md` |
| `down:` #3 | `../phase8_5_picker_release/SESSIONS_ARCHIVE.md` | `../../phase8_5_picker_release/SESSIONS_ARCHIVE.md` |
| `down:` #4 | `../docs/concepts/phase8_ui_graph_plan.md` | `./phase8_ui_graph_plan.md` |
| `down:` #5 | `../phase8_ui_graph/SESSIONS_ARCHIVE.md` | `../../phase8_ui_graph/SESSIONS_ARCHIVE.md` |

**Gegenprobe (60 Dateien mit Frontmatter geprüft): das sind die einzigen sechs im ganzen
Repo.** Alle anderen `up:`/`down:`-Ziele lösen auf.

### §1.3 Befund 2 — vier fehlende L1-Header-Cards

| Datei | Bewertung |
|---|---|
| `docs/PROJECT_SESSION_LOG.md` | **Card fehlt, gehört hin.** L3-Archiv, aber kein dokumentierter Ausnahmefall — `docs/INDEX.md` nennt vier Ausnahmen (Harness, Test-Fixtures, maschinell geparst, Vendor-Text); dies ist keine davon. |
| `phase8_5_picker_release/SICHTPRUEFUNG_RESTBLOCK.md` | **Card fehlt, gehört hin.** 📗, 28 KB, im INDEX gelistet. |
| `phase8_5_picker_release/SICHTPRUEFUNG_WALKTHROUGH.md` | **Card fehlt, gehört hin.** 📗, 29 KB, im INDEX gelistet. |
| `phase8_5_picker_release/CLUSTER3_TESTBLOCK.md` | **Card fehlt UND keine INDEX-Zeile.** Der einzige Doppel-Verstoß. |

**Kein Verstoß, korrekt so:** `docs/UPDATE_LOG.md` (maschinell geparst von
`webui/updates.py :: parse_update_log()`), `phase5_ui/vendor/lucide/README.md` (Vendor-Text),
`phase5_ui/THIRD_PARTY_LICENSES.md` (Lizenztext), `.claude/RESUME.md` (Harness),
`phase6_shares/tests/golden/*.md` (Test-Fixtures — eine Card bräche den Byte-Vergleich).

### §1.4 Befund 3a — drei `down:`-Listen im falschen Format

`docs/concepts/phase6_5_tools_images_plan.md`, `phase6_shares/GLOBAL_SEARCH_PLAN.md` und
`phase6_shares/IMAGES_PLAN.md` schreiben `down:` als **eine Zeile mit `·`-Trennern** statt
als YAML-Liste. **Alle Ziele lösen auf** — das ist kein toter Link, sondern ein
Schema-Verstoß gegen die L1-Card.

**Der eigentliche Befund ist aber der Prüfer, nicht die Datei:** ein Scanner, der nur
`- `-Listeneinträge liest, **überspringt diese drei Dateien stillschweigend** und meldet
trotzdem „alles sauber". Genau das ist beim ersten Durchgang dieser Planungssession passiert.

**Auftrag:** die drei Cards auf Listenform bringen — **und** den Scanner in P8.6-2 so
schreiben, dass er eine Datei mit `down:`-Inhalt, aus dem er **null** Ziele extrahiert,
als **Warnung** ausgibt statt als Erfolg. Ein Prüfer, der beim Nicht-Verstehen schweigt,
ist schlimmer als keiner.

### §1.4 Befund 3 — fehlende INDEX-Zeilen

- `phase8_5_picker_release/CLUSTER3_TESTBLOCK.md` — **fehlt, nachtragen.**
- `phase5_ui/THIRD_PARTY_LICENSES.md` — fehlt, **aber**: Lizenztext, dokumentierte Ausnahme
  von der Card-Pflicht. Die INDEX-Zeile ist trotzdem fällig (die Ausnahme betrifft die Card,
  nicht den Index). **Nachtragen, als Ausnahme markiert.**

### §1.5 Befund 4 — Softcap

| Datei | Größe | Bewertung |
|---|---|---|
| `docs/INDEX.md` | **war 40.960 B, ist 40.928 B** | **Exakt am Cap.** `find … -size +40k` findet sie **nicht** (40.960 ist nicht > 40.960) — sie ist trotzdem voll. **Die Planungssession hat drei Einträge straffen müssen, nur um die *eine* Zeile für diesen Plan unterzubringen** (P8.5-Plan-Eintrag −750 B, `p8x`-Notizen-Eintrag −400 B, der eigene `updated:`-Pipe −450 B). **Es bleiben 32 Byte Luft.** Head, Archiv und ein möglicher Grafik-Eintrag dieser Phase passen damit **nicht** mehr hinein. |
| `phase8_ui_graph/CLAUDE.md` | 42.343 B | Über dem Cap, **📗 einer abgeschlossenen Phase — und im Gegensatz zu `phase6_shares/CLAUDE.md` nirgends als Ausnahme benannt.** Seine INDEX-Zeile (Z. 53) erwähnt den Softcap mit keinem Wort. **Das ist der einzige *stille* Verstoß im Repo** — Block A schreibt außerdem ~600 B hinein (§3.4). |
| `phase6_shares/CLAUDE.md` | 41.032 B | Über dem Cap, seit P8 Step 0.3 **korrekt als benannter Verstoß dokumentiert** (P8-P). Vorbild für die Behandlung der Zeile darüber. |
| `phase5_ui/CLAUDE.md` | 40.957 B | **3 Bytes unter dem Cap** — aber die INDEX-Zeile (Z. 91) behauptet seit dem 2026-08-28 „über dem 40KB-Softcap, benannt statt versteckt". **Doku-Drift:** die Prosa widerspricht dem mechanischen Check, den `docs/INDEX.md` selbst vorschreibt (`find … -size +40k` findet die Datei nicht). Korrigieren, nicht die Datei anfassen. |

**Auftrag für Step 0, konkret:** vor der ersten neuen INDEX-Zeile (Head, Archiv) einen
echten Kompressions-Pass fahren — Ziel **≤ 38 KB**, nicht „gerade so drunter". Die
Planungssession hat bewusst nur so viel komprimiert, wie sie selbst verbraucht hat; das
Aufräumen der 68 Einträge ist Step-0-Arbeit, nicht Planungsarbeit. **Die ergiebigsten
Kandidaten sind die Einträge geschlossener Phasen**, deren Index-Zeile den Inhalt des
Dokuments zusammenfasst, statt darauf zu zeigen — L0 ist eine Landkarte, keine
Kurzfassung (`docs/INDEX.md` Kopfzeile: „one line each").

Die drei Phase-Heads bleiben inhaltlich, wie sie sind — **begründet:** ein künstlicher
Session-Block in einer geschlossenen Phase, nur damit `rotate_session_block.sh` greift, wäre
schlimmer als die Übergröße (P8-P, wörtlich übernommen).

**Zwei INDEX-Zeilen werden aber korrigiert**, denn beide sagen heute etwas Falsches:

1. **`phase8_ui_graph/CLAUDE.md`** bekommt die Softcap-Notiz, die ihm fehlt — nach dem
   Muster der `phase6_shares`-Zeile, plus dem Hinweis, dass Block A ihn wachsen lässt.
   **Warum das kein Formalismus ist:** die Konvention duldet einen benannten Verstoß und
   verbietet einen stillen. Ein stiller Verstoß ist beim nächsten Step 0 ununterscheidbar
   von einem Versehen, und genau deshalb wurde er hier auch erst im zweiten Anlauf gefunden.
2. **`phase5_ui/CLAUDE.md`** verliert die Behauptung, über dem Cap zu liegen. Sie ist es
   nicht (40.957 B), und die Datei wird in P8.6 nicht angefasst.

### §1.6 Befund 5 — Testbaseline

Baseline-Lauf dieser Planungssession, Kommando:
`env -u SHAREFYX_DATA_ROOT -u SFX_DATA_ROOT .venv/bin/python -m pytest -q`

**Ergebnis: `964 passed in 257.42s`, Exit 0.** Damit ist die Baseline **gemessen, nicht
angenommen** — sie deckt sich exakt mit dem letzten dokumentierten Stand (Phase 8.5 Z,
964 in 267 s). **V107 ist geschlossen.**

**Der Lauf muss mit ausgehängten `SHAREFYX_*`/`SFX_*`-Variablen erfolgen** — ein Lauf, der
die Umgebung dieser Box erbt, hat schon einmal die Produktion 52× neu gestartet. (In dieser
Box waren zum Planungszeitpunkt **keine** solchen Variablen gesetzt — geprüft.) Der
ausführende Agent wiederholt das Kommando unverändert vor jedem Commit (§0.5 Punkt 2).

### §1.7 Befund 6 — UI-Budget-Baseline (gemessen, nicht geschätzt)

`.venv/bin/python phase5_ui/scripts/ui_budget.py`, Lauf 2026-09-09, **5/5 im Zielkorridor**:

| Messgröße | Ist | Ziel |
|---|---|---|
| `GET /api/v1/items?limit=50` roh | 26,5 KB | < 64 KB |
| `GET /api/v1/items?limit=50` gzip | 1,3 KB | < 12 KB |
| `GET /api/v1/items/{id}` typisch | 0,7 KB | < 8 KB |
| `app.js + app.css + Font` gzip | **130,1 KB** | < 250 KB |
| Erstaufruf `/ui/` bis interaktiv | 138,3 KB | < 400 KB |

**Damit ist V97 aus dem P8.5-Handover geschlossen:** die dort nie gegengeprüfte Ausgangszahl
„125,8 KB" ist heute 130,1 KB — plausibel gewachsen, weit im Korridor.

**Informativ, kein Gate, aber der Grund für P8.6-O:** `GET /api/v1/overview` ~863 ms in
diesem Lauf (historisch dokumentiert 438–453 ms). Der Endpunkt macht eine `store.search()`
pro Bucket pro Space plus eine für „Zuletzt benutzt" (`api.py:603-614`). **[VERIFY] V108** —
ist die Verdopplung Messrauschen oder eine echte Regression? Vor Block C einmal drei Läufe
mitteln. **Wenn es echt ist, ist das ein Befund für P9, kein P8.6-Auftrag.**

### §1.8 Befund 7 — ein undefinierter CSS-Token (echter Renderfehler)

`app.css:1270` und `app.css:1276` referenzieren `var(--border-soft)` — **dieser Token ist
nirgends definiert.** Nach CSS-Spezifikation macht ein `var()` auf eine undefinierte
Custom-Property ohne Fallback die **gesamte Deklaration** ungültig; bei den Kurzformen
`border` / `border-bottom` heißt das: **der Rahmen wird gar nicht gezeichnet.**

Betroffen: `.link-picker-results` und `.link-picker-results li`. Fix in **Block A**
(§3.3), nicht hier — Step 0 ist Befund, nicht Reparatur.

### §1.9 Was nichts zu tun ergab

- **Session-Block-Konvention:** alle zehn Phase-Heads tragen **genau einen**
  `## Session stopped`-Block. Nur `phase8_5_picker_release/CLAUDE.md` hat darunter einen
  `###`-Unterblock — das ist das im Handover §8 beschriebene Muster, es betrifft aber eine
  abgeschlossene Phase und wird nicht nachträglich umgebaut. **Nichts zu tun.**
- **Tote INDEX-Einträge:** keine. Jeder aus `docs/INDEX.md` verlinkte Pfad existiert.
- **`docs/screenshots/README.md`** hat keine eigene INDEX-Zeile, wird aber in der Prosa der
  `docs/screenshots/`-Verzeichniszeile genannt („L1-Header-Card in …"). **Weicher Treffer,
  bewusst nichts zu tun** — das Verzeichnis ist der Index-Eintrag, die README ist seine Card.
- **`.claude/RESUME.md`** hat keine INDEX-Zeile. **Korrekt so** — Harness-Datei, erste der
  vier in `docs/INDEX.md` genannten Ausnahmen. **Nichts zu tun.**
- **`rotate_session_block.sh`-Exit-Codes, für Step Z zu kennen:** `0` = rotiert,
  `1` = abgebrochen (eine der drei `cmp`-Gegenlesungen schlug fehl, **nichts geschrieben**),
  `2` = nichts zu tun. **`2` bedeutet ausdrücklich nicht „erfolgreich"** — es umfasst auch
  den Fall „genau ein Block, aber eine mehrdeutige `##`-Sektion danach". Bei `2` also lesen,
  was das Skript auf stderr sagt, statt es als Erfolg zu verbuchen.
- **Arbeitsbaum:** sauber bei `d1af51b`.

### §1.10 Abschluss Step 0

Ein Commit, Nachricht `phase 8.6: Step 0 -- Haushalt, sechs kaputte Doku-Links, vier fehlende L1-Cards, INDEX-Kompression`.
Enthält: Phasenverzeichnis + Head + Archiv, die sechs Link-Fixes, die vier Cards, die zwei
INDEX-Zeilen, die INDEX-Kompression, und die Baselines V107/V108 im Head.

---

## §2 Step V — OpenCode-Vision-Plugin (erster Schritt der Phase)

**Nikinger-Vorgabe vom 2026-09-08, unverändert** (`sichtpruefung_automation_tooling.md`,
Handover §4.4): dies ist der **erste** Schritt, vor jedem Code-Touch.

1. `DavidEasden/opencode-vision` installieren
   (https://github.com/DavidEasden/opencode-vision), als Plugin in `opencode.json`
   registrieren.
   **Existenz am 2026-09-09 in der Planungssession geprüft** — das Repo existiert, Lizenz
   **AGPL-3.0**, Demo-Videos von Januar 2026. **Es hat drei Commits.** Das Plugin fängt
   eingefügte Bilder ab und leitet sie über ein konfiguriertes MCP-Bildanalyse-Werkzeug
   (`local_vision`) weiter — es ist also **keine** reine Modell-Verdrahtung, sondern
   braucht zusätzlich ein solches Werkzeug. Das steht so **nicht** in
   `sichtpruefung_automation_tooling.md` und ist beim Einrichten die erste Hürde.
   **Drei Commits und AGPL sind kein Ausschlussgrund, aber ein Grund, Punkt 4 unten ernst
   zu nehmen** — dieses Plugin ist nicht erwiesenermaßen tragfähige Infrastruktur.
2. **Abnahme-Probe:** das Plugin gegen genau einen bestehenden Screenshot laufen lassen —
   `docs/screenshots/c4_p8519_01_radiogruppe_im_dialog.png`. Die Frage, die es beantworten
   muss: *„sind zwei Radio-Buttons sichtbar, ist einer markiert?"* Antwort **ja/ja** ist die
   Abnahme. **[VERIFY] V119** — der Dateiname ist aus dem Tooling-Doc übernommen; wenn er
   nicht existiert, irgendeinen `c4_*`- oder `sp2_*`-Screenshot nehmen und den echten Namen
   protokollieren.
3. **Wenn es nicht funktioniert:** Kandidat 2 (`JochenYang/opencode-vision`), dann Kandidat 3
   (`alfaoz/opencode-see-image`). **Kandidat 4 (`oh-my-opencode-slim`) nicht** — eine
   Multi-Agent-Suite für ein Bildproblem zu installieren ist die falsche Größenordnung.
4. **Wenn alle drei scheitern:** das ist ein Befund, kein Blocker. Protokollieren, mit dem
   bisherigen Verfahren weitermachen (Screenshot in Datei, Nikinger öffnet ihn), und in §9
   vermerken. **P8.6 wartet nicht auf das Plugin.**

Sobald es steht, gilt `sichtpruefung_automation_conventions.md` **§4**: Screenshots direkt
im Chat zeigen, darunter eine Zeile „Was zu validieren ist".

**Kein Code-Commit.** Ergebnis wird im Phase-Head protokolliert.

---

## §3 Block A — Radiogruppe-Rückbau und Token-Fundament

*Fundament. Block B verbraucht, was hier entsteht.*

### §3.1 A1 — Radiogruppe zurück auf `<select class="input">`

**Was heute da ist:**

| Ort | Anker |
|---|---|
| Markup | `app.html:276-286` — `<fieldset class="link-picker-modes">` mit zwei `<input type="radio" name="link-picker-mode">` (`value="body"` checked, `value="frontmatter"`) |
| JS-Konstante | `dialogs.js:116` — `var LINK_PICKER_MODE_NAME = "link-picker-mode";` |
| JS-Leser | `dialogs.js:234` — `function _linkPickerMode()` |
| JS-Restore | `dialogs.js:244` — `function _restoreLinkPickerMode()`, liest `localStorage` |
| JS-Verkabelung | `dialogs.js:601-609` — `querySelectorAll('input[name="…"]')` + `change`-Listener, Persistenz in Z. 608 |
| Persistenz-Key | `dialogs.js:115` — `LINK_PICKER_MODE_KEY = "sfx:linkpicker:mode"` |
| CSS | `app.css:1312` `.link-picker-modes`, `:1323` `legend`, `:1329` `.link-picker-mode`, `:1336` `input[type="radio"]` |
| Test | `phase5_ui/tests/test_static_routes.py:258-312` |

**Was daraus wird:**

- **Markup** `app.html:276-286` → ein `<select class="input" id="link-picker-mode">` mit
  zwei `<option value="body">` / `<option value="frontmatter">`. **Die Beschriftung steht
  in der Box** (P8.6-H): kein externes `<label>` daneben, sondern ein `<label>`-Element
  **innerhalb** des `.input`-Trägers, links vom Select, wie eine Eingabe-Präfix-Beschriftung.
  Neue CSS-Klasse `.input--labeled` mit `display: flex; align-items: center;` — der Select
  selbst verliert seinen eigenen Rahmen und erbt ihn vom Träger.
- **JS:** `LINK_PICKER_MODE_NAME` (Z. 116) entfällt; `_linkPickerMode()` (Z. 234) liest
  `linkPickerModeEl.value`; `_restoreLinkPickerMode()` (Z. 244) setzt `.value`;
  `dialogs.js:601-609` wird **ein** `change`-Listener auf **einem** Element statt einer
  `NodeList`-Schleife. **`LINK_PICKER_MODE_KEY` und der `localStorage`-Wert bleiben
  unverändert** — Nutzer behalten ihre Wahl.
- **CSS:** die vier `.link-picker-mode*`-Blöcke (`app.css:1312-1339`) entfallen; der Select
  erbt die bestehende `select.input`-Regel (Chevron-Data-URL, `accent-color`).
- **Test** (P8.6-I): `test_link_picker_uses_a_radio_group_not_a_select` →
  `test_link_picker_uses_a_select_not_a_radio_group`. Assertions umkehren:
  fordern `<select` mit `id="link-picker-mode"` und genau zwei `<option>` in der Reihenfolge
  `body`, `frontmatter`; verbieten `class="link-picker-modes"` und
  `input[name="link-picker-mode"]`. **Docstring trägt beide Richtungen mit Datum** — 2026-09-06
  Radiogruppe angeordnet, 2026-09-08 zurückgenommen.

**Warum dieser Schritt zuerst:** er stellt die *Choice*-Kategorie der Selection/Choice-Konvention
wieder her, von der P8.5-19 die dokumentierte Ausnahme war. Block B verallgemeinert diese
Konvention auf die ganze App — mit einer offenen Ausnahme im Picker wäre das eine Regel mit
eingebautem Gegenbeispiel.

### §3.2 A2 — Layer- und Selektions-Tokens

In `app.css` `:root` (Z. 28-108):

```css
/* Layer 0 — echtes Schwarz. Bewusst sparsam (P8.6-E): nur dort, wo "nichts da ist".
   Auf OLED echte Pixelabschaltung, auf LCD ein sichtbar tieferer Grund als --bg. */
--bg-void: #000;

/* Selektion. EIN Blau, zwei Deckkraft-Stufen. Ersetzt fuenf rohe rgba(62,141,243,...)
   ausserhalb dieses Blocks (P8.6-C). Hover ist dieselbe Optik, halb so deckend
   (Nikinger 2026-09-09, Notizen 10.5) -- kein zweiter Farbton. */
--select-fill:        linear-gradient(180deg, rgba(62,141,243,.20), rgba(62,141,243,.08));
--select-fill-quiet:  linear-gradient(180deg, rgba(62,141,243,.10), rgba(62,141,243,.04));
--select-line:        var(--accent-line);
--select-line-quiet:  rgba(62,141,243,.20);

/* Vorsicht — Aktionen mit Rueckweg-Kosten (Abmelden, Archivieren). Gleicher Wert wie
   --danger, anderer Anlass: --danger meldet, dass etwas schiefging; --caution warnt,
   bevor etwas passiert. Zwei Namen auf einem Wert ist hier ehrlicher als ein zweiter
   Rotton (P8.6-F, Phase-8-Verbot 4: Farbe nur mit Bedeutung). */
--caution: var(--danger);
```

**Ersetzungen (exakte Zeilen, gegen `d1af51b`):**

| Zeile | Selektor (heute) | Neu |
|---|---|---|
| `app.css:403` | `.rail__home[aria-current], .tree__folder[aria-current], .tree__scope[aria-current]` | `background: var(--select-fill);` |
| `app.css:685` | `.list__row[aria-current="true"]` | `background: var(--select-fill);` |
| `app.css:719` | `.list__rows > li.list__row--selected` | `background: var(--select-fill);` |
| `app.css:785` | (`border-color: rgba(62,141,243,.35)`) | `border-color: var(--select-line);` — **[VERIFY] V109**: `.35` vs. `--accent-line`s `.40`. Wenn der Unterschied sichtbar ist, eigenen Token; wenn nicht, angleichen. Im Zweifel angleichen. |
| `app.css:1291` | `.link-picker-results li:hover, …[aria-selected="true"]` | `background: var(--select-fill);` |

**Grund für die Konsolidierung, nicht nur für die Ordnung:** §10.5 verlangt eine
*transparentere* Hover-Variante. Bei vier wörtlich duplizierten Verläufen hieße das, an
vier Stellen einen zweiten Verlauf danebenzuschreiben — acht Deklarationen für zwei
Zustände. Mit Token sind es zwei.

### §3.3 A3 — `--border-soft`-Renderfehler beheben

`app.css:1270` und `:1276`: `var(--border-soft)` ist undefiniert (§1.8). **Ersetzen durch
`var(--line)`** — das ist der Haarlinien-Token, den jede andere Panel-Kante der App
verwendet; `.link-picker-results` ist ein Panel.

**Warum nicht `--border-soft` definieren:** dann hätte die App zwei Tokens für dieselbe
Haarlinie, und der nächste Leser müsste raten, wann welcher gilt. Der Bug ist entstanden,
weil ein Token benutzt wurde, den es nie gab — die Reparatur ist, den vorhandenen zu nehmen.

### §3.4 A4 — Konvention v3 um die Kategorie „Vorsicht" erweitern

In `phase8_ui_graph/CLAUDE.md`, Abschnitt „Selection/Choice Konvention v3" (ab Z. 254), eine
fünfte Tabellenzeile:

| Kategorie | Was es macht | Vorbild (Code, Selector) | Visuelle Sprache |
|---|---|---|---|
| **Vorsicht** | Aktion mit **Rückweg-Kosten** — nicht zerstörend, aber teuer rückgängig zu machen | `#logout-button`, `#archive-button` | Standard-Knopfplastik, aber `color: var(--caution)` auf Label und Glyph; **keine** gefüllte rote Fläche |

**Dazu ein Satz, der die Abgrenzung festhält:** *„Vorsicht ist keine Bestätigungspflicht.
Ein Knopf dieser Kategorie darf trotzdem einen Bestätigungsdialog haben (Archivieren hat
einen), aber die Farbe ersetzt ihn nicht und verlangt ihn nicht."*

**Achtung, hier wächst ein bereits übergroßer Head:** 42.343 B, und die fünf neuen Zeilen
machen ihn ~600 B größer. Das ist **kein Grund, die Konvention woanders hinzuschreiben** —
sie gehört dorthin, wo sie gelesen wird. Aber: dieser Head ist der **einzige stille**
Softcap-Verstoß im Repo (§1.5). **Step 0 muss die INDEX-Zeile vorher benannt haben**,
sonst schreibt Block A in einen undokumentierten Verstoß hinein und vergrößert ihn.
Reihenfolge ist hier tragend, nicht kosmetisch. Danach die neue Größe im INDEX nachziehen.

### §3.5 Abschluss Block A

Ein Commit: `phase 8.6: Block A -- Radiogruppe zurueck auf select, Layer-/Selektions-Tokens, --border-soft-Fix`.
Selbstprüf-Checkliste §0.5 vollständig, insbesondere Punkt 5.

---

## §4 Block B — Selektion vereinheitlichen (§5, §10.1–§10.7)

*Verbraucht die Tokens aus Block A. Kein neuer Token entsteht hier.*

### §4.1 B1 — Hover ist die leise Standardauswahl (§10.2, §10.5)

Heute sind die Hover-Zustände ein Flickenteppich: `.list__row:hover` setzt
`background: var(--surface)` (`app.css:668`), `.rail__home:hover` und Geschwister teilen eine
Regel bei `app.css:397`, `.btn:hover` einen hartkodierten Grauverlauf (`app.css:219`).
**Drei verschiedene Antworten auf „was passiert beim Darüberfahren".**

Neu, überall dasselbe:

```css
.list__row:hover,
.rail__home:hover, .rail__action:hover,
.tree__space:hover, .tree__folder:hover, .tree__scope:hover,
.overview__space-row:hover,
.link-picker-results li:hover {
  background: var(--select-fill-quiet);
  outline: 1px solid var(--select-line-quiet);
  outline-offset: -1px;
  border-radius: var(--radius-sm);
}
```

**Kollisionsregel, wichtig:** ein Element, das **gleichzeitig** `[aria-current="true"]` und
`:hover` ist, muss die **volle** Auswahl zeigen, nicht die leise. Die
`[aria-current]`-Regeln stehen im Stylesheet **vor** den Hover-Regeln — bei gleicher
Spezifität gewinnt die spätere. Deshalb: die Hover-Regel bekommt
`:not([aria-current="true"]):not(.list__row--selected)`.

**Warum als Ausschluss und nicht über Reihenfolge:** eine Reihenfolge-Abhängigkeit über
1300 Zeilen Stylesheet ist genau die Kaskadenfalle, für die es die Eskalationsregel P8.5-O
gibt. Der Ausschluss steht im Selektor und überlebt jedes Umsortieren.

**Zu entfernen:** `app.css:219` (`.btn:hover` Hex-Verlauf) und `app.css:238`
(`.btn-primary:hover` Hex-Verlauf) → Token (P8.6-Q). `.btn:hover` bekommt
`var(--select-fill-quiet)` über der Knopfplastik; `.btn-primary:hover` behält seinen
Akzentverlauf, aber aus `--accent-face-top/-bottom` aufgehellt statt aus zwei Hex-Werten.

### §4.2 B2 — Ordner, Tags und Buckets auf die Standardauswahl (§10.3)

- **Ordner** (`.tree__folder`, `app.css:517`) und **Buckets** (`.tree__scope`, `app.css:488`)
  haben bereits `[aria-current]` → nach B1/A2 automatisch korrekt. **Zu prüfen, nicht zu
  bauen.**
- **`.tree__space`** (`app.css:487`) hat **kein** `[aria-current]` — ein ausgewählter Space
  ist heute nicht als ausgewählt erkennbar. `tree.js :: renderSpaceNode()` (Z. 200) setzt
  `aria-current="true"`, wenn `state.space === space.name`. **[VERIFY] V113** — im Code
  gegenprüfen, ob `state.space` an dieser Stelle den richtigen Namen trägt.
- **Tags:** es gibt heute **keine** Tag-Auswahl-Fläche. Tags werden als Klartext gerendert
  (`list.js:144`, `item.tags.join(", ")` in `itemMetaLine()`), und im Editor stehen sie in
  einem freien `<input>` (`editor.js:154`/`:352`). **§10.3 „Tags-Auswahl auf den Standard"
  hat damit heute kein Objekt.**
  **Entscheidung:** die Filter-Chips in `#list-chips` (`app.html:52`) sind die nächstgelegene
  „Tags-Auswahl" und bekommen die Standardauswahl. Eine **echte** Tag-Auswahlfläche ist §8
  und liegt außerhalb dieser Phase (§0.4).
  **Das ist eine Interpretation, kein Lock — in der Sichtprüfung bestätigen lassen (§7).**

### §4.3 B3 — Einstellungsmenü auf die Standardauswahl (§10.6)

Der Dialog `#account-dialog` (`app.html:446-478`) enthält heute:
`#account-show-updates` (`.btn`, Z. 451), `#account-manage-spaces` (`.btn`, Z. 452), vier
`.input`-Felder (Z. 456, 461, 465, 471), `#account-submit` (`.btn-primary`, Z. 476),
`#account-cancel` (`.btn`, Z. 477).

Nach B1 erben alle `.btn`/`.btn-primary` den vereinheitlichten Hover automatisch. **Was
bleibt:** `#account-show-updates` und `#account-manage-spaces` sind *Navigation*, keine
*Aktion* — sie öffnen etwas, sie ändern nichts. Sie bekommen die Navigations-Sprache der
Konvention v3 (Akzent-Fill bei `aria-current`, sonst transparent), nicht die Knopfplastik.

**Warum das mehr als Kosmetik ist:** ein Dialog, in dem „Update-Log ansehen" und „Ändern"
identisch aussehen, lädt zum Fehlklick ein — dasselbe Muster, das der Nikinger schon einmal
beim Archivieren-neben-× gemeldet hat (`app.html:143`, Kommentar dort).

### §4.4 B4 — Alles Klickbare, plus die Kategorie „Vorsicht" (§10.7)

**Sweep-Kommando** (in den Phase-Head protokollieren, nicht nur ausführen):

```
grep -nE 'addEventListener\("click"|onclick|<button|<a href|role="button"' \
  phase5_ui/webui/static/app.html phase5_ui/webui/static/js/*.js
```

Jeder Treffer bekommt genau eine der fünf Kategorien der Konvention v3 zugeordnet
(Choice / Toggle / Status / Navigation / **Vorsicht**). **Die Zuordnungstabelle gehört in
den Phase-Head** — sie ist der Beleg für „alles Klickbare geprüft", und sie ist beim
nächsten UI-Commit die Nachschlagestelle.

**Die zwei „Vorsicht"-Mitglieder:**

**Die Kennzeichnung ist eine Klasse, kein ID-Selektor:** `class="action--caution"`, dazu
**eine** CSS-Regel:

```css
/* Kategorie "Vorsicht" (Konvention v3, fuenfte Kategorie). Traegerklasse statt
   ID-Selektor: nur so ist "genau zwei Mitglieder" maschinell pruefbar (Test §8.2), und
   die dritte destruktive Aktion erbt die Farbe, statt sie neu zu erfinden. */
.action--caution, .action--caution .rail__label, .action--caution .rail__glyph {
  color: var(--caution);
}
```

| Element | Anker | Änderung |
|---|---|---|
| Abmelden | `app.html:38-40` (`#logout-button`), Handler `app.js:125-129` | `class="rail__action action--caution"`; Knopfplastik bleibt |
| Archivieren | `app.html:147` (`#archive-button`, heute schlichtes `.btn`), Handler `editor.js:554-576` | `class="btn action--caution"`; der bestehende Bestätigungsdialog (`editor.js:559-561`) bleibt unverändert |

**Kein drittes Mitglied.** „Verschieben", „Abwählen", „Erste Notiz anlegen", „Space
verwalten" sind alle folgenlos oder trivial umkehrbar.

### §4.5 B5 — Radien vereinheitlichen (§10.1)

**Gemessener Ist-Stand** (`grep -c` liefert 37, davon **2 Kommentar-Erwähnungen** in
`app.css:681` und `:683` — **35 echte Deklarationen**, **7** verschiedene Werte):

| Wert | Anzahl | Bewertung |
|---|---|---|
| `var(--radius-sm)` (6px) | 22 | **Der Standard.** Bleibt. |
| `999px` | 4 | Pillen (`app.css:513, 623, 636, 777`) — **korrekt so**, eine Pille ist keine Karte. |
| `var(--radius)` (10px) | 4 | Große Flächen (`:920, 1079, 1514, 1634`) — **korrekt so**. |
| `50%` | 2 | Kreise (`:762, 826`) — **korrekt so**. |
| `0` | 1 | `.tree__scope` (`:493`) — **korrekt so**, die Zeile hat eine Unterkante statt einer Kontur. |
| **`6px` hartkodiert** | 1 | `.link-picker-results` (`:1271`) — **Fehler, am Token vorbei.** → `var(--radius-sm)`. |
| `0 var(--radius-sm) var(--radius-sm) 0` | 1 | `:1073` — **korrekt so**, ein angesetztes Element. |

**Ergebnis: genau eine Änderung.** Der Rest ist ein begründetes System, kein Wildwuchs.

**Wichtig für die Sichtprüfung:** §10.1 sagt „alle **Icons** auf selbe abgerundete Ecken".
Icons tragen in dieser App **selbst keinen Radius** — sie erben ihn von der Trägerfläche
(`.rail__glyph`, `app.css:409`; `.icon`, `:456`). Der Wunsch ist also mit hoher
Wahrscheinlichkeit ein **Trägerflächen**-Wunsch. **[VERIFY] V114** — am Screenshot mit dem
Nikinger klären, welche zwei Flächen er nebeneinander gesehen hat. **Nicht raten und
flächendeckend Radien angleichen** — die vier `999px`-Pillen und die zwei `50%`-Kreise sind
absichtlich anders.

### §4.6 Abschluss Block B

Ein Commit: `phase 8.6: Block B -- eine Selektionssprache fuer alles Klickbare, Kategorie Vorsicht, ein Radius-Fix`.

---

## §5 Block C — Struktur (§6, §1, §10.4, §3)

### §5.1 C1 — „Konto" → „Einstellungen", beide neu platziert (§6, N3-Lesart b)

**Ist-Stand** `app.html:31-41`: `.rail__account` enthält `#account-button` („Konto",
Icon `#i-settings`) **vor** `#logout-button` („Abmelden", Icon `#i-log-out`).

**Soll:**

- `#account-button`-Label „Konto" → **„Einstellungen"** (`app.html:33`). Icon bleibt
  `#i-settings` — es war schon immer ein Zahnrad, der Name hinkte hinterher.
- **`#account-button` wandert nach oben:** aus `.rail__account` heraus, direkt **unter**
  `#home-button` (also nach `app.html:24`, vor `#rail-tree`).
- **`#logout-button` bleibt in `.rail__account`** am Rail-Ende, jetzt als einziges Kind.
  `.rail__action { width: auto; flex: 1; }` (`app.css:395`) muss angepasst werden — mit nur
  einem Kind ist `flex: 1` gegenstandslos, und der Knopf würde die volle Breite nehmen.
- `.rail__account` (`app.css:544`) verliert seine Zwei-Kinder-Annahme.

**Warum das die richtige Lesart ist:** ein wörtlicher Tausch würde „Abmelden" — die
seltenste und teuerste Aktion — an die prominenteste Stelle des Blocks setzen. Der Nikinger
begründet den Wunsch mit „that's more suiting"; das ist ein Ergonomie-Argument, kein
Positions-Argument. **Lesart (b) ist bestätigt** (N3), nicht geraten.

**i18n:** die App hat keine Übersetzungsschicht, Strings stehen im HTML. Ein
`grep -rn "Konto" phase5_ui/webui/ phase5_ui/tests/` **vor** der Änderung — es kann Tests
geben, die auf dem Wort stehen.

### §5.2 C2 — „Alle Items" unter die Spaces (§1)

**Eine Zeile.** `tree.js :: renderRail()` (Z. 242-255) ruft `renderScopeRow()` heute als
erstes auf (Z. 244). Der Aufruf wandert **hinter** die `foreign.forEach(renderSpaceNode)`-Schleife
(hinter Z. 253).

Dazu ein Trenner: `renderScopeRow()` (Z. 227-239) bekommt vor dem Button ein
`el("div", "tree__group", "Alles")`-Geschwister — sonst klebt „Alle Items" ohne Überschrift
an den „Verbundene Spaces"-Block.

**Kein neuer Kippschalter** (P8.6-J). Der bestehende Mechanismus ist der Kippschalter.

**Was ausdrücklich bleibt:** der Kommentar `tree.js:224-226` erklärt, warum diese Zeile
**keinen** Zähler trägt („Lieber keine Zahl als eine unwahre"). Er bleibt wörtlich stehen —
er ist die Antwort auf die Frage, die C4 gleich für die Ordner stellt.

### §5.3 C3 — Map als rechte Spalte, volle Höhe (§1, §2.3)

`.overview` (`app.css:802-806`) wird zweispaltig:

```css
.overview {
  display: grid;
  grid-template-columns: 1fr 40%;
  grid-template-rows: auto 1fr;
  gap: calc(var(--space) * 3);
  flex: 1;               /* .detail ist flex-column (app.css:354-358) -- der Flex-Anteil
                            liefert die definite Hoehe, NICHT height:100% */
  min-height: 0;         /* ohne das ist die Mindesthoehe eines Flex-Items sein Inhalt,
                            und die Zeile "1fr" waechst statt zu scrollen */
  overflow: hidden;      /* die Spalten scrollen, nicht die Seite */
  padding: calc(var(--space) * 4);
}
```

**Warum `flex: 1; min-height: 0` und ausdrücklich *nicht* `height: 100%`:** `.overview` ist
**nicht** das einzige Kind von `.detail`. Daneben liegen `.detail__back` (`app.html:67`),
`#detail-readonly` (`app.html:125`) und der Editor-Teilbaum. Ein `height: 100%` würde gegen
`.detail`s Höhe rechnen — sobald ein Geschwister sichtbar ist und Höhe verbraucht, läuft
`.overview` genau um diesen Betrag über, `.detail`s `overflow-y: auto` (`app.css:334-337`)
scrollt, und **die Karte schneidet wieder unten ab** — derselbe Defekt über einen anderen Weg.
`flex: 1` fragt nicht nach einem Prozentsatz, sondern nimmt, was übrig ist.

**Gemessen, nicht angenommen:** `.detail__back` ist `display: none` (`app.css:1110-1111`) und
wird **nur** unter `@media (max-width: 1024px)` mit `[data-view="detail"]` sichtbar
(`app.css:1733`). `#detail-readonly` und der Editor sind `hidden`, solange die Übersicht
steht. **Oberhalb von 1024px ist `.overview` also tatsächlich das einzige sichtbare Kind** —
der `height: 100%`-Weg *würde* dort funktionieren. Er wird trotzdem nicht genommen, weil er
unter 1024px bricht, und genau dort greift die Ein-Spalten-Regel unten.

- Kopfzeile (`.overview__header`, `app.html:76`) über beide Spalten.
- Linke Spalte: `.overview__spaces` + „Zuletzt benutzt", eigenes `overflow-y: auto`.
- Rechte Spalte: `.overview__graph` — **`max-width: 960px` entfällt** (`app.css:918`),
  **`min-height: 55vh` entfällt** (`:917`), und **es kommt keine `height` dazu**: als
  Grid-Item in der `1fr`-Zeile füllt es sie per Definition. Nur `min-height: 0` dazu, damit
  das Canvas die Zeile nicht aufblähen kann.
- `.overview__graph canvas` (`:925-929`) bleibt `width/height: 100%` — jetzt gegen einen
  Elternteil mit definiter Höhe, und damit erstmals korrekt.

**Warum Grid innen und Flex außen:** die Zeile `1fr` eines Grids ist eine **definite** Höhe —
`.overview__graph` als Grid-Item bekommt sie ohne Prozentrechnung, und `canvas { height: 100% }`
funktioniert erstmals. Nach außen bleibt es Flex, weil `.detail` bereits `display: flex;
flex-direction: column` ist (`app.css:354-358`) und `flex: 1` dort die richtige Frage stellt
(„nimm den Rest") statt der falschen („nimm 100 % wovon?"). Das ist derselbe Bug wie §2.3 —
hier an der Wurzel gelöst, statt mit `overflow` übertüncht.

**Reihenfolge-Hinweis:** `graph.js :: resize()` (Z. 474-484) liest
`getBoundingClientRect()` und setzt daraus die Canvas-Attribute. Nach dem Layout-Umbau muss
`resize()` **nach** dem ersten Layout laufen. Es gibt bereits einen `ResizeObserver`
(`graph.js:147`) — **[VERIFY] V115**: greift der auch beim ersten Öffnen, oder braucht es
einen zusätzlichen `resize()`-Aufruf in `loadGraph()` (Z. 150)?

**Unter 1280px Breite** kollabiert das Grid auf eine Spalte (`@media (max-width: 1280px)`),
Map unter die Liste. **Das ist keine Mobile-Arbeit** (§0.4) — es ist die Absicherung, dass
das bestehende 16:9-Layout aus `app.css:326` nicht auf schmalen Fenstern zerbricht.

### §5.4 C4 — Spaces in der Übersicht klickbar (§10.4)

`list.js :: renderOverview()` (Z. 31-104). Heute hat `.overview__space-row` (Z. 48) **keinen**
Click-Handler; nur die `.overview__space-count`-Chips (Z. 67-79) sind klickbar, und Null-Chips
werden übersprungen (Z. 66).

**Neu:** die Zeile bekommt einen Handler, der in den Space navigiert
(`tree.js :: activateView(space.name)` oder `navigate(space.name, "open")` — **[VERIFY] V116**,
welche der beiden das erwartete Ziel ist; `activateView` ist die naheliegendere).

Die Chips behalten `event.stopPropagation()` (Z. 69) — das ist bereits da und wird jetzt
tragend statt dekorativ.

**Barrierefreiheit:** eine klickbare `<li>` ist keine. `.overview__space-row` bekommt ein
inneres `<button class="overview__space-open">`, das Name und Kategoriepunkt umschließt —
Tastaturfokus und Screenreader-Rolle gratis. **Kein `role="button"` auf dem `<li>`** — das
wäre ein Element, dessen Klickbarkeit nur eine Behauptung ist.

Kategorie nach Konvention v3: **Navigation** (P8.6-P).

### §5.5 C5 — Anzahl der Items pro Ordner (§3)

**Ist-Stand:** `tree.js :: renderFolders()` (Z. 62-88) zeigt Zähler — aber nur für die vier
festen **Buckets** (`open`/`done`/`note`/`archived`), gespeist aus `space.counts[bucket]`
(`api.py:128-133`), gerendert als `<span class="tree__count">` (`tree.js:72`).
**Echte, vom Nutzer angelegte Ordner** (`tree.js :: folderButton()`, Z. 156-174) haben
**kein** Zähler-Element.

**Neu, clientseitig (P8.6-O):** `folderButton()` hängt ein `<span class="tree__count">` an,
gespeist aus einer Zählung über `state.items` nach `folder`-Präfix.

**Drei Entscheidungen, die die Notizen offen ließen:**

1. **Was wird gezählt?** Alles, was der Nutzer in diesem Ordner **sehen** würde, wenn er ihn
   öffnet — also dieselbe Filterung wie die Listenansicht, inklusive `archived`.
   **Begründung:** ein Zähler, der etwas anderes zählt als die Liste darunter zeigt, ist ein
   Bug-Report in Warteschleife.
2. **Unterordner?** Nein — nur direkte Kinder. Ein rekursiver Zähler bräuchte eine
   Baumsummierung, und `buildFolderTree()` (Z. 95) liefert die Struktur, aber die Summe wäre
   für den Nutzer mehrdeutig („15" an einem Ordner, der selbst 2 enthält).
3. **Wenn die Item-Liste dieses Space noch nicht geladen ist?** **Kein Zähler**, nicht „0".
   Exakt die Begründung aus `tree.js:224-226`: *„Lieber keine Zahl als eine unwahre."*
   Das ist die Regel dieses Projekts für genau diesen Fall, und sie steht drei Zeilen über
   der Stelle, die hier geändert wird.

**[VERIFY] V117** — trägt `state.items` beim Rendern des Rails überhaupt die Items des
Spaces, oder nur die der gerade offenen Ansicht? Wenn Letzteres, ist der Zähler nur für den
aktiven Space korrekt — und dann gilt Regel 3 für alle anderen. **Vor dem Bauen messen.**

### §5.6 Abschluss Block C

Ein Commit: `phase 8.6: Block C -- Einstellungen nach oben, Alle-Items nach unten, Map als volle rechte Spalte, klickbare Spaces, Ordner-Zaehler`.

---

## §6 Block D — Graph-Fixes (V102, §2.4, plus ein benannter Zusatz)

*Unabhängig von Block C. Reihenfolge C↔D frei (P8.6-U).*

### §6.1 D1 — V102: Zwillingskante dedupliziert (N2)

`graph.js:156` — `explicitEdges = data.edges || [];`

Wird zu einer Dedup-Übernahme über das **ungeordnete** Knotenpaar:

```js
// V102 (gemessen in Phase 8.5 Block C an "Buecherliste Q4" <-> "Empfehlungen Nikinger"):
// dieselbe Beziehung, einmal als Body-Link und einmal als frontmatter-Eintrag, liefert
// zwei Kanten aus `store.links_all()` (api.py:712) -- der Server dedupliziert bewusst
// nicht (kein Cross-`kind`-Dedup in `index.py :: replace_item_links`). Hier zusammenfassen
// und nicht dort: eine neunte P1-Contract-Oeffnung waere das teuerste Mittel fuer einen
// Zeichenfehler (Nikinger-Entscheidung 2026-09-09, Plan P8.6-N).
explicitEdges = dedupeEdges(data.edges || []);
```

```js
function dedupeEdges(edges) {
  var seen = Object.create(null);
  var out = [];
  for (var i = 0; i < edges.length; i++) {
    var e = edges[i];
    var key = e.src < e.dst ? e.src + "|" + e.dst : e.dst + "|" + e.src;
    if (seen[key]) continue;
    seen[key] = true;
    out.push(e);
  }
  return out;
}
```

**`Object.create(null)` statt `{}`:** Item-IDs sind `itm_…`-Strings und kollidieren nicht mit
`Object.prototype`-Namen — aber ein Prototyp-loses Objekt macht die Aussage „das ist eine
Menge, keine Struktur" explizit und kostet nichts.

**Was der Dedup nicht anfasst:** `implicitEdges` (Tag-/Ordner-Kanten, `graph.js:206-245`).
Die haben eine andere Semantik und dürfen neben einer expliziten Kante stehen.
**[VERIFY] V118** — wenn eine Tag-Kante **und** eine explizite Kante dieselben zwei Knoten
verbindet, zeichnet die App weiterhin zwei Linien. Ist das gewollt? In der Sichtprüfung
zeigen. Vermutlich ja (unterschiedliche Farben, `drawEdges()` Z. 399-401), aber es ist
dieselbe Frage wie V102 auf einer anderen Ebene.

### §6.2 D2 — Deterministischer Layout-Seed (§2.4, P8.6-M)

`graph.js :: seedInitialPositions()` (Z. 248-263). Zeilen 260/261 verwenden `Math.random()`
für den Jitter:

```js
n.x = cx + Math.cos(angle) * spread + (Math.random() - 0.5) * 30;
n.y = cy + Math.sin(angle) * spread + (Math.random() - 0.5) * 30;
```

Der Ring selbst (`angle` nach Index) ist bereits deterministisch — **nur der Jitter ist es
nicht.** Ersetzen durch einen Hash der Knoten-ID:

```js
// FNV-1a, 32 Bit. Zweck ist nicht Kryptographie, sondern Reproduzierbarkeit: dieselbe
// Item-ID muss ueber Reloads hinweg denselben Jitter ergeben, sonst "fliegt" die Karte
// bei jedem Oeffnen neu (Nikinger 2026-09-06, Notizen §2.4).
function seedJitter(id, salt) {
  var h = 2166136261;
  for (var i = 0; i < id.length; i++) { h ^= id.charCodeAt(i); h = Math.imul(h, 16777619); }
  h ^= salt;
  return ((h >>> 0) / 4294967295) - 0.5;   // -0.5 .. +0.5, wie (Math.random() - 0.5)
}
```

Aufruf: `seedJitter(n.id, 1) * 30` für x, `seedJitter(n.id, 2) * 30` für y.

**Warum FNV-1a und kein `Math.sin`-Trick:** FNV-1a ist acht Zeilen, hat keine
Plattformabhängigkeit (`Math.imul` ist exakt 32-Bit) und liefert für benachbarte IDs
unkorrelierte Werte — genau das, was ein Jitter braucht. Ein `Math.sin(seed)*10000 % 1`
korreliert bei ähnlichen Eingaben, und `itm_`-IDs sind einander ähnlich.

**Was das nicht löst:** die Karte sieht nach dem Hinzufügen eines Items **anders** aus als
vorher — der Ring wird nach Index vergeben. Das ist §2.1/P9-Gebiet.

### §6.3 D3 — `.overview__graph`-Höhe

Bereits in **C3** erledigt (P8.6-L). Hier nur die Gegenprobe: nach C3 muss der Canvas die
volle Spaltenhöhe füllen und der untere Rand sichtbar sein. **Vor** C3 einen
Screenshot machen, damit der Fix belegbar ist (**[VERIFY] V112**).

### §6.4 D4 — Der nicht abgebrochene Animations-Lauf (benannte Scope-Erweiterung)

**Befund:** `graph.js :: runSimulation()` (Z. 266-291) legt `var rafId = null;` **lokal** an
(Z. 268) und weist ihn in Z. 277 und Z. 290 zu — aber **liest ihn nie**. Ein
`cancelAnimationFrame` existiert in der ganzen Datei nicht. Jeder Aufruf von
`loadGraphPanel()` — bei jedem Klick auf Übersicht (`app.js:99-105`), bei jedem Refresh
(`app.js:136-139`) — startet eine **zusätzliche** `requestAnimationFrame`-Schleife. Solange
die vorige noch über `ALPHA_MIN` liegt, laufen **zwei `tick()`-Schleifen gleichzeitig**,
beide rufen `draw()`.

**Das ist streng genommen §2.1-Gebiet (P9)** und damit außerhalb des Scopes aus §0.4. Es wird
trotzdem mitgenommen, aus drei Gründen:

1. Es ist die **direkte Ursache** dafür, dass §2.4 („die Karte fliegt") sich beim
   wiederholten Öffnen verschlimmert — zwei Simulationen mit unterschiedlichem `alpha`
   ziehen an denselben Knoten.
2. Der Fix ist **drei Zeilen**: `rafId` auf Modulebene, `if (rafId) cancelAnimationFrame(rafId);`
   am Anfang von `runSimulation()`.
3. Er ist **schon halb da** — die Variable existiert und wird gepflegt. Jemand hat den
   Abbruch geplant und nicht zu Ende geschrieben.

**Wenn der Nikinger das anders sieht, ist es zu streichen** — es ist die einzige
Scope-Erweiterung dieses Plans, und sie steht hier, damit sie streichbar ist statt
unbemerkt mitzulaufen.

### §6.5 Abschluss Block D

Ein Commit: `phase 8.6: Block D -- V102-Dedup, deterministischer Layout-Seed, Animationslauf abbrechen`.

---

## §7 Gate — Wegwerf-Ritt, Sichtprüfung, Deploy

### §7.1 G1 — Wegwerf-Instanz

Nach dem Muster aus Phase 8.5 (`phase8_5_picker_release/scripts/`): eigener Port, eigener
tmp-`DATA_ROOT`, eigene `auth.sqlite3`, **PID-Datei**.

**Hard Rule 9, ohne Ausnahme:** Stoppen **ausschließlich** über die PID-Datei oder den
eindeutigen Port. **Kein `pkill -f`.** Der Produktions-Dienst `sharefyx-mcp.service` wird
in dieser Phase **nicht** angefasst — nicht gestartet, nicht gestoppt, nicht neu geladen.
Am 2026-09-01 hat genau ein `pkill -f "phase2_mcp.scripts.serve"` die Produktion mitgenommen.

### §7.2 G2 — Smoke-Skript

`phase8_6_ui_polish/scripts/p86_polish_smoke.py` (Playwright, venv
`~/.claude-code-tools/e2e-venv`). Stationen, je ein Screenshot nach
`docs/screenshots/p86_*.png`:

| # | Station | Prüft |
|---|---|---|
| 1 | Login + Übersicht | Rail-Reihenfolge: `#home-button`, „Einstellungen", Spaces, **dann** „Alle Items" |
| 2 | Übersicht mit Graph | Map als rechte Spalte, **unterer Rand sichtbar** (§2.3) |
| 3 | Zweimal Übersicht öffnen | Identisches Kartenbild (§2.4, Pixel-Vergleich zweier Screenshots) |
| 4 | Zwillingskanten-Item | **Eine** Linie statt zwei (V102) |
| 5 | Hover über Listenzeile | Leiser Blau-Fill, kein `--surface`-Grau (§10.2/§10.5) |
| 6 | Zeile ausgewählt **und** gehovert | Voller Fill, nicht der leise (Kollisionsregel §4.1) |
| 7 | Space-Zeile in der Übersicht klicken | Navigiert (§10.4), auch bei Null-Zählern |
| 8 | Ordner im Rail | Zähler sichtbar (§3) |
| 9 | Einstellungen-Dialog | Alle Knöpfe in der richtigen Kategorie (§10.6) |
| 10 | Abmelden + Archivieren | `--caution`-Farbe, sonst Standardplastik (§10.7) |
| 11 | Link-Picker öffnen | `<select>` mit Beschriftung **in** der Box, Chevron sichtbar |
| 12 | Picker-Modus wechseln, Dialog neu öffnen | Wahl aus `localStorage` wiederhergestellt |

**Beide Browser** (Chromium + Firefox) für Station 2, 5, 6, 11 — das sind die Stationen mit
CSS-Verhalten, das auseinanderlaufen kann.

**CSRF-Grenze beachten** (Handover §4.3): Wegwerf läuft auf `http://127.0.0.1:<port>`, die
`Origin` passt nicht zu `SPACE_PUBLIC_BASE_URL` → **jeder POST/PATCH aus dem Browser-Kontext
wird abgewiesen.** Stationen, die schreiben, werden per `storage.Store` vorbereitet, nicht
per UI-Klick. Stationen 1–12 oben sind bewusst alle Lese-/Render-Stationen.

### §7.3 G3 — Nikinger-Sichtprüfung

Nach `sichtpruefung_automation_conventions.md`:

- **§2:** Code und automatisierte Tests sind Agenten-Sache. **Visuelles ist
  Nikinger-Sache.** Der Agent zertifiziert nicht selbst, dass etwas „schöner" aussieht.
- **§4:** Screenshots **im Chat** zeigen (Vision-Plugin aus Step V), darunter je eine Zeile
  „Was zu validieren ist".
- **§1 Vorschau-Pflicht:** wo etwas klickbar wird, den **gerenderten** Zustand zeigen, nicht
  den Quelltext.
- **§3: Deploy erst nach Testauswertung.**

**Die fünf Punkte, die der Nikinger entscheiden muss** (nicht der Agent):

1. §10.1 — welche Trägerflächen meinte er? (**V114**)
2. §4.2 — sind die Filter-Chips die „Tags-Auswahl"? (Interpretation aus B2)
3. §1 — ist der bestehende Mechanismus der „Kippschalter"? (**V110**, P8.6-J)
4. §6.4 — bleibt der `cancelAnimationFrame`-Fix drin? (Scope-Erweiterung)
5. P8.6-R — reicht `v3.0.2`, oder ist der Layout-Umbau ein `v3.1.0` wert?

**Statusregel** (`sichtpruefung_automation_conventions.md`, seit 2026-09-08): eine vom
Nikinger geprüfte Wegwerf-Automatisierung zählt als **live-verifiziert (✅)**, nicht als 🟡.
Das gilt **nicht** für identitätsförmige Kriterien.

### §7.4 G4 — Deploy `v3.0.2`

**Zweiteilig, wegen Hard Rule 9:**

| Schritt | Wer | Was |
|---|---|---|
| D-a | Agent | Badge `app.html:20` `v3.0.1` → `v3.0.2`; **obersten Block in `docs/UPDATE_LOG.md` mit dem heutigen Datum** — `deploy.sh` bricht sonst ab (P6-X); Commit |
| D-b | **Nikinger** | `deploy.sh` ausführen. **Kein Agent fasst `systemctl` an.** |
| D-c | Agent | `health_gate.sh` (aus `phase8_5_picker_release/scripts/`) gegen die Produktion — reine `curl`-GETs, 8/8 erwartet |

**[VERIFY] V103 aus P8.5 wird hier mitprotokolliert** — sie war in P8.5 unbeantwortet, weil
D2 still durchlief: *ist der `sudo`-Prompt im Vordergrund sichtbar?* Der Nikinger notiert
beim Deploy einen Satz dazu, dann ist die Frage nach zwei Phasen zu.

---

## §8 Abnahme, Tests, `[VERIFY]`-Register

### §8.1 Abnahmematrix

Art: **(C)** Code/Test, vom Agenten belegbar · **(W)** Wegwerf-Instanz + Nikinger-Sichtung ·
**(L)** nur live entscheidbar.

| # | Kriterium | Art |
|---|---|---|
| P8.6-1 | Phasenverzeichnis `phase8_6_ui_polish/` mit Head + Archiv, beide mit L1-Card und INDEX-Zeile | (C) |
| P8.6-2 | Die sechs `up:`/`down:`-Links in `p8x_ui_polish_notes.md` lösen auf; die drei Inline-`down:`-Cards sind auf Listenform; Repo-weiter Re-Scan meldet **0** Bruchstellen **und 0 stille Übersprünge** (§1.4/3a) | (C) |
| P8.6-3 | Die vier fehlenden L1-Cards existieren; `CLUSTER3_TESTBLOCK.md` + `THIRD_PARTY_LICENSES.md` haben INDEX-Zeilen | (C) |
| P8.6-4 | `docs/INDEX.md` nach Kompression **und** nach allen neuen Zeilen der Phase **≤ 38 KB** (nicht bloß unter 40.960 B) | (C) |
| P8.6-5 | Vision-Plugin installiert und an einem echten Screenshot verifiziert — **oder** protokolliertes Scheitern aller drei Kandidaten | (C) |
| P8.6-6 | `grep -n "rgba(62,141,243" app.css` trifft **nur noch** `:root`-Zeilen | (C) |
| P8.6-7 | `--border-soft` kommt in `app.css` nicht mehr vor; `.link-picker-results` hat einen sichtbaren Rahmen | (C+W) |
| P8.6-8 | Link-Picker ist ein `<select class="input">`, Beschriftung **in** der Box; Chevron sichtbar | (W) |
| P8.6-9 | `test_link_picker_uses_a_select_not_a_radio_group` grün, Docstring trägt beide Richtungen | (C) |
| P8.6-10 | Picker-Moduswahl überlebt Dialog-Schließen und Reload (`localStorage`-Key unverändert) | (W) |
| P8.6-11 | Konvention v3 im Phase-8-Head trägt die fünfte Kategorie „Vorsicht" | (C) |
| P8.6-12 | Hover zeigt überall dieselbe leise Standardauswahl — Liste, Rail, Ordner, Buckets, Picker, Space-Zeilen | (W) |
| P8.6-13 | Ausgewählt **und** gehovert zeigt die **volle** Auswahl, nicht die leise | (W) |
| P8.6-14 | `.btn:hover` und `.btn-primary:hover` ohne hartkodierte Hex-Verläufe | (C) |
| P8.6-15 | Der Klickbarkeits-Sweep aus §4.4 liegt als Zuordnungstabelle im Phase-Head | (C) |
| P8.6-16 | Genau zwei Elemente tragen `.action--caution` (Abmelden, Archivieren); maschinell geprüft, nicht nur gesichtet | (C+W) |
| P8.6-17 | `.link-picker-results` nutzt `var(--radius-sm)`; kein hartkodierter Radius mehr in `app.css` | (C) |
| P8.6-18 | Rail-Reihenfolge: Übersicht · Einstellungen · Mein Space · Verbundene Spaces · Alle Items | (W) |
| P8.6-19 | „Abmelden" steht am Rail-Ende, allein in `.rail__account` | (W) |
| P8.6-20 | Kein Vorkommen von „Konto" mehr in `webui/` und `tests/` | (C) |
| P8.6-21 | Map ist rechte Spalte, ~40 % Breite, **unterer Rand sichtbar** | (W) |
| P8.6-22 | Unter 1280px kollabiert die Übersicht auf eine Spalte ohne Überlappung | (W) |
| P8.6-23 | Space-Zeilen sind klickbar — **auch bei lauter Null-Zählern** —, per Tastatur erreichbar | (W) |
| P8.6-24 | Echte Ordner tragen einen Zähler; ungeladene Spaces zeigen **keinen**, nicht „0" | (W) |
| P8.6-25 | Zwillingskante zeichnet **eine** Linie (V102) | (W) |
| P8.6-26 | Zwei Reloads der Übersicht liefern ein identisches Kartenbild (§2.4) | (W) |
| P8.6-27 | Wiederholtes Öffnen startet **keine** zweite Simulationsschleife (§6.4) | (C+W) |
| P8.6-28 | `pytest` grün, **≥ 964 passed** (Baseline §1.6) | (C) |
| P8.6-29 | `ui_budget.py` 5/5 im Korridor; `app.js+app.css+Font` gzip unter 250 KB | (C) |
| P8.6-30 | Tabu-Diff §0.3 über die **gesamte** Phase leer — keine neunte P1-Contract-Öffnung | (C) |
| P8.6-31 | `v3.0.2` live, Badge sichtbar, `health_gate.sh` 8/8 | (L) |
| P8.6-32 | Service-Touch durch einen Agenten: **0**. Wegwerf-Instanzen nur per PID-Datei/Port gestoppt | (C) |

### §8.2 Testliste (neu zu schreiben)

Alle in `phase5_ui/tests/test_static_routes.py`, dem etablierten Ort für statische
UI-Zusicherungen:

| Testname | Prüft |
|---|---|
| `test_link_picker_uses_a_select_not_a_radio_group` | **Umkehrung** von Z. 258 (P8.6-I) |
| `test_no_raw_accent_rgba_outside_root` | `rgba(62,141,243` kommt in `app.css` nur zwischen `:root {` und der schließenden Klammer vor — der maschinelle Wächter über P8.6-C |
| `test_every_css_var_reference_is_defined` | jedes `var(--x)` in `app.css` hat **irgendwo in der Datei** ein `--x:` — **nicht** auf `:root` einengen: `@supports`-Blöcke und andere Scopes definieren zulässigerweise Tokens außerhalb (Phase-8-Glass-Fallback), und `--caution: var(--danger)` ist selbst eine `var()`-Referenz *innerhalb* `:root`. **Hätte den `--border-soft`-Bug gefunden**, und findet den nächsten |
| `test_rail_order_settings_before_tree_logout_last` | `#account-button` steht in `app.html` vor `#rail-tree`, `#logout-button` danach |
| `test_account_button_says_einstellungen` | Label ist „Einstellungen", nicht „Konto" |
| `test_caution_class_only_on_logout_and_archive` | genau zwei Elemente tragen die Vorsicht-Kennzeichnung (P8.6-F/§4.4) |
| `test_overview_graph_has_no_max_width` | `.overview__graph` hat weder `max-width` noch `min-height` (der §2.3-Regressionswächter) |

**`test_every_css_var_reference_is_defined` ist der wichtigste der sieben.** Er ist der
einzige, der eine ganze Fehlerklasse schließt statt einer Instanz — und die Fehlerklasse
ist bewiesen, weil sie in `d1af51b` zweimal live steht (§1.8).

### §8.3 `[VERIFY]`-Register

| # | Frage | Wann |
|---|---|---|
| **V106** | Sammelmarker: alle `Datei:Zeile`-Anker dieses Plans gegen `main`@`d1af51b`. **Bei Drift: melden, nicht raten.** | vor jedem Block |
| **V119** | Existiert `docs/screenshots/c4_p8519_01_radiogruppe_im_dialog.png`? | Step V |
| **V108** | `_overview` ~863 ms: Rauschen oder Regression gegen die dokumentierten 438–453 ms? | Step 0, drei Läufe |
| **V109** | `app.css:785` nutzt `rgba(…,.35)`, `--accent-line` ist `.40`. Sichtbarer Unterschied? | Block A |
| **V110** | Ist der bestehende `#home-button`/`.tree__scope`-Mechanismus der „Kippschalter" aus §1? | Sichtprüfung |
| **V111** | Phase-8-Head 42.343 B + ~600 B Konvention — im INDEX nachgezogen? | Block A |
| **V112** | §2.3: schneidet die Map **vor** dem Fix messbar ab? Screenshot vorher/nachher | vor Block C |
| **V113** | Setzt `renderSpaceNode()` (`tree.js:200`) `aria-current` korrekt aus `state.space`? | Block B |
| **V114** | §10.1: **welche** Trägerflächen meinte der Nikinger? | Sichtprüfung |
| **V115** | Greift der `ResizeObserver` (`graph.js:147`) beim ersten Öffnen, oder braucht `loadGraph()` einen `resize()`? | Block C |
| **V116** | `activateView(name)` oder `navigate(name, "open")` für den Space-Klick? | Block C |
| **V117** | Trägt `state.items` beim Rail-Rendern die Items **aller** Spaces oder nur der offenen Ansicht? | vor C5 |
| **V118** | Tag-Kante + explizite Kante zwischen denselben Knoten: zwei Linien gewollt? | Sichtprüfung |
| **V103** *(geerbt)* | `deploy.sh`: `sudo`-Prompt im Vordergrund sichtbar? | Deploy |

**Geschlossen durch diese Planungssession, vor dem ersten Code-Touch:**
**V97** (`ui_budget.py`, aus dem P8.5-Handover geerbt) — 5/5 gemessen, 130,1 KB von 250 KB,
§1.7. **V107** (`pytest`-Baseline) — 964 passed in 257 s, §1.6. **V104** bleibt
gegenstandslos. Damit startet P8.6 mit **zwei** gemessenen Baselines statt zwei Annahmen.

---

## §9 Closeout

*Leer bis Step Z. Dieser Abschnitt ist nach P8.6-B/P8-N der **kanonische** Abschluss der
Phase — Status in fünf Sätzen, Delta, Abnahmestand, Restdefekte, `[VERIFY]`-Bilanz
V106–V119, P1-Contract-Aussage, und was nicht enthalten ist.*

*Bekannte Punkte, die hier landen werden, weil P8.6 sie bewusst nicht anfasst: der
CSRF-Origin-Mismatch für Wegwerf-Instanzen (§0.4), das geerbte Ledger (§0.4), und die
P9-Übergabe für §2.1/§2.2/§2.5/§4/§7/§8/§9/§10.8.*
