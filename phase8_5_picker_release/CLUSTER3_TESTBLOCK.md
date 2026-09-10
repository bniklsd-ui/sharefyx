---
status: live
purpose: Schritt-für-Schritt-Testblock für Phase-8-Cluster-3-Sichtprüfung (P8-20/-21/-22/-24) gegen eine 200-Knoten-Wegwerf-Instanz — älter, vom Restblock abgelöst, bleibt als Audit-Quelle für Z erhalten
read-when: beim Nachvollziehen der Phase-8-Cluster-3-Verifikation; für aktuelle Sichtungen ist `SICHTPRUEFUNG_RESTBLOCK.md` maßgeblich
detail: L2
up: ./CLAUDE.md
down:
  - ./SICHTPRUEFUNG_RESTBLOCK.md   # konsolidierter Nachfolger, deckt auch Cluster 4 + 5 ab
updated: 2026-09-07 (Cluster-3-Teilverifikation — erste Nikinger-Live-Sichtprüfung nach Cluster 2; P8-20 ✅ + P8-21 a/b/c ✅; restliche Zeilen in Folge-Session)
---
# Cluster 3 — Testblock für P8-20 / P8-21 / P8-22 / P8-24

**Status:** ⬜ offen (alle vier Zeilen sind 🟡 in `phase8_ui_graph/CLAUDE.md` §7 — werfen-verifiziert, nicht live).
**Auftrag:** Phase-8-§7-Statusregel verlangt für den Sprung auf ✅ eine **Nikinger-Sichtprüfung am echten Gerät** gegen v3.0.1. Vier Zeilen, ~15 Min am Stück (eine Login-Sitzung), für P8-22 zusätzlich die 200-Knoten-Wegwerf parallel.

**Vorbedingung (Hard Rule 8 + Phase-§0):**

- Tailscale-Funnel-URL der laufenden v3.0.1 (Service-PID 355956, Release `20260905T140325.378914Z`, seit 2026-09-05 16:10:18 CEST aktiv). Login als `niklas` (oder `fabian` — beide haben Graph-Daten).
- Browser: **Chromium** (für die Screenshots vergleichbar mit den throwaway-Belegen); Firefox geht auch, Pfade sind dieselben.
- DevTools offen — der Graph ist `<canvas id="overview-graph-canvas">`, mit `getImageData()` lassen sich Knoten-Position und Farbe direkt auslesen (siehe `phase8_ui_graph/scripts/phase8_e2e_smoke.py` für die fertige Probe-Funktion).
- Für **P8-22**: parallel die **200-Knoten-Wegwerf starten** (Port 18772, eigener tmp-`DATA_ROOT` unter `/tmp/opencode/sharefyx-wegwerf-200knoten/`) — siehe Anhang A unten. Nikinger kann das vom opencode/M3 in einem zweiten Tab ausführen lassen (Standing-Permission aus den vorherigen Clustern) oder selbst starten.

**Konvention für die Screenshots:** unter `docs/screenshots/c3_*.png` ablegen, Name wie `c3_p820_01_overview_mit_graph.png` — damit sie der `grep`-Audit später leicht findet.

---

## P8-20 — Graph: Hover dimmt Nicht-Nachbarn, Klick öffnet das Item, Drag/Zoom/Pan funktioniert

**Abnahmekriterium (Plan §7):** drei Sub-Punkte in einer Anzeige.

**Setup:** Übersicht öffnen, sicherstellen dass der Verknüpfungs-Graph gerendert ist (mind. ein eigener + ein geteilter Knoten sichtbar — live ist das gegeben).

### P8-20a — Hover dimmt Nicht-Nachbarn

| Schritt | Aktion | Erwartung |
|---|---|---|
| 1 | Maus auf einen sichtbaren Knoten (z. B. einen blauen "eigenen" Knoten) | Nicht-Nachbarn werden sichtbar gedimmt (`opacity`/`fillAlpha` ≈ 0.15), der Hover-Knoten und seine direkten Nachbarn (1-Hop) bleiben voll deckend in ihrer C3-Farbe |
| 2 | Cursor außerhalb des Canvas | Knoten kehren zu voller Deckkraft zurück |
| 3 | Optional: zweiter Hover auf einen türkisen (geteilten) oder grauen (fremden) Knoten | gleiches Verhalten, gleiche Dimm-Stufe |

**Beleg:** Screenshot `c3_p820_01_hover_dimmt.png`, Cursor auf einem Knoten sichtbar.

**Throwaway-Vergleich:** `phase8_ui_graph/scripts/phase8_e2e_smoke.py :: test_station5_hover_dimmt_nicht_nachbarn` (Pixel-Count der voll-deckenden Knoten vor vs. nach Hover; auf live-Daten nicht erforderlich, der Smoke-Beleg reicht).

### P8-20b — Klick öffnet das Item (Fix C vom 2026-09-02, der wahrscheinliche Knackpunkt)

| Schritt | Aktion | Erwartung |
|---|---|---|
| 1 | Sicherstellen dass das Detail-Panel geschlossen ist (im linken Paneel oder Detail-Spalte leer) | rechte Spalte / Detail leer oder "Item auswählen"-Hinweis |
| 2 | **Einfacher Klick** auf einen blauen **eigenen** Knoten (linke Maustaste, sofort loslassen, ohne Bewegung) | Detail-Paneel öffnet das Item im **Editor** (`#detail-editor` sichtbar, `#detail-readonly` versteckt), der Titel des Knotens erscheint im Editor |
| 3 | Zurück zur Übersicht (z. B. `#home-button` oder `Esc`) | Graph ist wieder sichtbar, Detail-Paneel leer |
| 4 | **Einfacher Klick** auf einen türkisen **geteilten** Knoten | Detail-Paneel öffnet das Item in der **Nur-lesen-Ansicht** (`#detail-readonly` sichtbar, kein Edit-Button), Titel sichtbar |
| 5 | Zurück zur Übersicht | wie Schritt 3 |
| 6 | **Einfacher Klick** auf einen grauen **fremden** Knoten | Nur-lesen-Ansicht, kein Edit-Button |

**Sonderfall:** wenn das Live-Datenset nur eigene Knoten hat (selten, aber möglich), testen wir nur P8-20b-Schritte 1-3 + P8-21-Toggle um auf geteilte Knoten zu kommen.

**Beleg:** Screenshot `c3_p820_02_eigener_knoten_klick.png` (Editor offen), `c3_p820_03_geteilter_knoten_klick.png` (Readonly offen).

### P8-20c — Drag, Zoom, Pan

| Schritt | Aktion | Erwartung |
|---|---|---|
| 1 | **Drag** eines Knotens um ~50 px nach rechts (Maus gedrückt halten, ziehen, loslassen) | Knoten folgt dem Cursor; wenn losgelassen wird **nicht** der Detail-Paneel geöffnet — der Klick-vs-Drag-Heuristik (`CLICK_SLOP=4`) muss den Drag als solchen erkennen |
| 2 | **Pan** mit leerer Canvas-Stelle (Maus gedrückt, leerer Bereich ziehen) | gesamter Graph verschiebt sich, danach Physik-Simulation läuft kurz an und pendelt ein |
| 3 | **Zoom** mit Mausrad nach oben (über dem Canvas) | Graph wird größer, Zoom-Readout (z. B. "1.2×" oder prozentual) sichtbar in der Toolbar |
| 4 | **Zoom** mit Mausrad nach unten (über dem Canvas) | Graph wird kleiner, Zoom-Readout sinkt |
| 5 | **Pan + Klick in einem Rutsch** (Maus gedrückt auf Knoten, ~30 px ziehen, loslassen) | Drag gewinnt — Detail-Paneel bleibt zu. Kein Click-Event ausgelöst |

**Beleg:** kein Screenshot erforderlich (Drag/Pan/Zoom sind schwer screenshot-bar); die vier Heuristik-Schritte 1+5 sind der Knackpunkt.

**Wann gilt P8-20 als ✅:** alle drei Sub-Punkte bestanden + Screenshots 02/03 abgelegt.

---

## P8-21 — Tag-/Ordner-Toggles wirken; Default nur explizite Kanten; >15-Knoten-Tag erzeugt keine Clique

**Abnahmekriterium (Plan §7):** drei Sub-Punkte am selben Graph.

**Setup:** Übersicht mit Graph (gleiche Sitzung wie P8-20).

### P8-21a — Default zeigt nur explizite Kanten

| Schritt | Aktion | Erwartung |
|---|---|---|
| 1 | Übersicht öffnen, Graph ansehen | nur explizite Frontmatter-`links:`- und `itm_…`-Body-Kanten sichtbar (solide Linien, `strokeStyle` per `graph.js :: drawEdges`); **keine** Tag-Kanten (gestrichelt) und **keine** Ordner-Kanten (gepunktet) |
| 2 | Knotenzähler im Kopf der Toolbar zählt die sichtbaren Kanten — gegen das DevTools-Network-Panel: `GET /api/v1/graph` enthält im Response-`edges`-Feld nur Kanten mit `kind: "link"` oder `kind: "body"` | Bestätigung der Default-Semantik |

**Beleg:** Screenshot `c3_p821_01_default_nur_explizit.png`.

### P8-21b — Tag-Toggle erweitert sichtbar

| Schritt | Aktion | Erwartung |
|---|---|---|
| 1 | Toolbar-Knopf **"Tags"** anklicken (Checkbox-Toggle, ID `#overview-graph-toggle-tags` o. ä. — siehe `phase8_ui_graph/scripts/d2_playwright_smoke.py :: step5_tag_toggle` für den genauen Selector) | zusätzliche gestrichelte Kanten erscheinen — eine pro Tag-Knoten-Paar; sichtbar mehr Kanten als im Default |
| 2 | **Tags** nochmal anklicken (Toggle aus) | gestrichelte Kanten verschwinden wieder, Default-Zustand kehrt zurück |
| 3 | Wieder **Tags** einschalten für die nächsten Sub-Punkte | |

**Beleg:** Screenshot `c3_p821_02_tag_toggle_ein.png`.

### P8-21c — Ordner-Toggle erweitert sichtbar

| Schritt | Aktion | Erwartung |
|---|---|---|
| 1 | Toolbar-Knopf **"Ordner"** anklicken (zweite Toggle-Box) | gepunktete Kanten erscheinen — eine pro Ordner-Gemeinschafts-Paar (Items im selben Ordner) |
| 2 | nochmal anklicken → aus | gepunktete Kanten verschwinden |
| 3 | **Ordner** wieder einschalten für den nächsten Sub-Punkt | |

**Beleg:** Screenshot `c3_p821_03_ordner_toggle_ein.png`.

### P8-21d — >15-Knoten-Riegel (`TAG_CLIQUE_LIMIT = 15` in `graph.js:88`)

Dieser Sub-Punkt ist am **Live-Datensatz nur prüfbar, wenn ein Tag mit > 15 Items existiert** — in der Realität eher unwahrscheinlich. **Workaround:** in den 200-Knoten-Wegwerf-Tab wechseln, dort gibt es das Tag `spitze` (genau 5 Knoten, 10 Paare, kommt durch) und das Tag `last-200` (alle 200 Knoten, wird vom Riegel ausgeschlossen). Für P8-22 dort:

| Schritt | Aktion | Erwartung |
|---|---|---|
| 1 | 200-Knoten-Wegwerf öffnen (Port 18772), Graph ansehen | Default: nur explizite Ring-Kanten sichtbar |
| 2 | Tags-Toggle einschalten | zusätzliche Kanten erscheinen — **NICHT** für `last-200` (sollte unsichtbar bleiben, sonst wären es 19 900 Kanten), **NICHT** für `gruppe-NN` (12 Gruppen à ~16 Knoten, alle ausgeschlossen), **JA** für `spitze` (10 Paare sichtbar) |
| 3 | Optionale Verifikation im DevTools-Consolentab: `await fetch("/api/v1/graph?tag_edges=1").then(r => r.json()).then(g => g.edges.filter(e => e.kind === "tag").length)` | Anzahl der Tag-Kanten im Response (liegt im niedrigen dreistelligen Bereich, NICHT 19 900) |

**Wenn am Live-Datensatz kein Tag mit > 15 Items existiert:** nur Code-Pfad bestätigen (`graph.js:210 if (ids.length > TAG_CLIQUE_LIMIT) return;` per Read, kein Browser-Test nötig — der throwaway-Smoke deckt den empirischen Teil bereits ab).

**Beleg:** Screenshot `c3_p821_04_200knoten_tag_clique_limit.png`.

**Wann gilt P8-21 als ✅:** P8-21a/b/c bestanden + (falls Live-Daten herhalten) P8-21d bestanden, sonst P8-21d mit Hinweis "Code-Pfad in `graph.js:210` plus throwaway-Smoke in `p8_22_smoke.py` reichen".

---

## P8-22 — 200-Knoten-Wegwerf: Simulation kommt < 3 s zur Ruhe, Interaktion ohne Hakeln; `prefers-reduced-motion` rendert statisch

**Abnahmekriterium (Plan §7):** drei Sub-Punkte gegen den 200-Knoten-Wegwerf.

**Live-Daten reichen nicht** — Niklas hat ~29 Items, IT-Sekus 64, gesamt ~100. **Anhang A: 200-Knoten-Wegwerf starten**, dann gegen `http://127.0.0.1:18772` arbeiten.

### P8-22a — Settle-Zeit < 3 s

| Schritt | Aktion | Erwartung |
|---|---|---|
| 1 | 200-Knoten-Wegwerf öffnen, Übersicht mit Graph | nach dem ersten Frame ist eine sichtbare Animation zu sehen, Knoten pendeln ein |
| 2 | Stoppuhr ab dem **ersten sichtbaren Animationsframe** (nicht ab dem Reload) | Bewegung kommt **vor 3 s** zur Ruhe — subjektiv kein erkennbares Zittern mehr |
| 3 | Optionale Verifikation in den DevTools-Performance-Tools: `graph.js`-Frames sollten spätestens nach ~2.7 s keine Layout-Änderungen mehr zeigen | (nicht zwingend — die subjektive Beobachtung reicht, der throwaway-Smoke hat **2.69 s** gemessen) |

**Beleg:** Screenshot `c3_p822_01_settled.png` (sichtbare Ruhe, gleicher Ausschnitt wie `p8_22_01_200_knoten.png` aus dem Throwaway-Lauf).

### P8-22b — Interaktion ohne Hakeln

| Schritt | Aktion | Erwartung |
|---|---|---|
| 1 | Hover über mehrere Knoten | jede Bewegung reagiert ohne spürbare Latenz (< 16 ms pro Frame ist 60 fps, das Budget sollte nicht reißen) |
| 2 | Drag eines Knotens | Knoten folgt der Maus ohne Verzögerung; beim Loslassen öffnet sich das Detail-Paneel **nicht** (Drag-vs-Klick-Heuristik, Fix C) |
| 3 | Zoom mit Mausrad (10 Stufen rauf, 10 Stufen runter) | keine Ruckler, jede Stufe greift |
| 4 | Pan mit leerer Canvas-Stelle | keine Ruckler |

**Beleg:** subjektiv, kein Screenshot erforderlich.

### P8-22c — `prefers-reduced-motion: reduce` rendert statisch

| Schritt | Aktion | Erwartung |
|---|---|---|
| 1 | In DevTools: `Rendering`-Tab → "Emulate CSS media feature prefers-reduced-motion: reduce" einschalten (oder im Konsolen-Tab: `await chrome.debugger` o. ä. — oder einfacher: System-Preference setzen, dann Browser neu starten, je nach Plattform) | Graph wird **ohne Animation** gerendert — direkt im Ruhezustand, kein Tick, keine Bewegung |
| 2 | Pflicht-Verifikation im DevTools-Console: `await fetch("/api/v1/graph").then(r => r.json()).then(g => g.nodes.length)` | 200 (das Datenset ist da, nur die Animation ist aus) |
| 3 | Schalter zurück auf "no-preference" | Graph startet wieder normal mit Animation |

**Beleg:** Screenshot `c3_p822_02_reduced_motion_static.png` (Pixel-Inhalt identisch zu c3_p822_01 nach Settle, nur ohne Animationsphase dazwischen).

**Wann gilt P8-22 als ✅:** alle drei Sub-Punkte bestanden. **Optional:** subjektive Beobachtung in Sekunden mit Uhr messen (Stoppuhr), nicht schätzen.

---

## P8-24 — Kombinierter E2E-Ritt: Übersicht → Scope → Graph → Knotenklick → Item

**Abnahmekriterium (Plan §7):** sechs Stationen am Stück in einer Login-Sitzung — gegen das **Live v3.0.1** reicht (Throwaway-Smoke gegen D2-Wegwerf hat 6/6, derselbe Pfad).

**Setup:** Tab mit v3.0.1, eingeloggt als `niklas` (oder `fabian`).

| # | Station | Erwartung |
|---|---|---|
| 1 | **Login** auf `/ui/` | Cookie-Session (kein Bearer), Redirect zurück auf die Übersicht |
| 2 | **Übersicht** | tabellose Space-Zeilen mit Counter-Chips (P8-18), Mini-Legende rechts oben (P8-15), Graph-Panel mit den drei Knotenfarben + Legende |
| 3 | **Globaler Scope** | Home-Knopf klicken → Listen-Spalte zeigt "Alle Items"-Header, Space-Spalten werden gemischt (P8-19). Zweiter Klick auf Home: idempotent, kein Sprung zurück in einen einzelnen Space |
| 4 | **Graph** | `/api/v1/graph` (im DevTools-Network-Tab nachprüfbar) liefert Knoten + Kanten-Liste, Empty-Hint ist versteckt, Canvas ist bebildert (mind. 500 nicht-transparente Pixel im Throwaway-Smoke-Check) |
| 5 | **Hover** | ein Knoten unter dem Cursor dimmt die Nicht-Nachbarn (P8-20a) |
| 6 | **Knotenklick → Item** | Klick auf einen **eigenen** Knoten öffnet den **Editor** (`#detail-editor` mit Titel und Body-Textarea); Klick auf einen **geteilten/fremden** Knoten öffnet die **Nur-lesen-Ansicht** (`#detail-readonly`); nach Klick ist die Übersicht verschwunden und das Detail-Paneel voll (Fix C, 2026-09-02) |

**Beleg:** vier Screenshots entlang des Ritts:
- `c3_p824_01_uebersicht.png` (Station 2)
- `c3_p824_02_alle_items_scope.png` (Station 3)
- `c3_p824_03_graph_hover.png` (Station 5)
- `c3_p824_04_knoten_geoeffnet.png` (Station 6 — Editor oder Readonly sichtbar)

**Wann gilt P8-24 als ✅:** alle sechs Stationen bestanden, vier Screenshots abgelegt.

---

## Ergebnis-Tabelle zum Ausfüllen

| # | Kriterium | Sub-Punkte | Bestanden? | Notizen |
|---|---|---|---|---|
| P8-20 | Graph-Verhalten | a/b/c | ⬜ | |
| P8-21 | Tag-/Ordner-Toggles | a/b/c (d optional) | ⬜ | |
| P8-22 | 200-Knoten-Settle | a/b/c (nur gegen Wegwerf) | ⬜ | |
| P8-24 | Kombinierter E2E-Ritt | Stationen 1-6 | ⬜ | |

**Wenn alles ✅:** Phase-8-Bilanz **19 ✅ · 7 🟡 · 0 ⬜ → 22 ✅ · 4 🟡 · 0 ⬜** (drei der vier Zeilen auf ✅; **P8-22** wandert je nach Wurf auf ✅, behält sonst 🟡 mit throwaway-Beleg). **Cluster 3 abgeschlossen** — nächster Schritt ist **Cluster 4** (Connector: P8.5-3 + P8.5-4 + P8.5-17 V105 + P8.5-19 Bauform-Bestätigung) oder direkt **Z** (Phase-8.5-Closeout), wenn auch das Pre-Z-Tausch-Beiwerk (Cluster 2) durch Nikinger-Live bestätigt wurde.

**Wenn etwas 🟡 bleibt:** jeder Fail-Punkt als Phase-8-Restdefekt in §9 eintragen (Bauart-Options a/b/c wie bei den drei Fixes A/B/C vom 2026-09-02), nicht stillschweigend überspringen.

---

## Anhang A — 200-Knoten-Wegwerf starten (für P8-22, optional opencode/M3)

Falls Nikinger den Setup nicht selbst machen will — Standing-Permission aus den vorherigen Clustern erlaubt opencode/M3, das in einem zweiten Tab zu erledigen. Aufruf:

```bash
.venv/bin/python phase8_ui_graph/scripts/wegwerf_setup_200knoten.py setup
.venv/bin/python phase8_ui_graph/scripts/wegwerf_setup_200knoten.py seed
.venv/bin/python phase8_ui_graph/scripts/wegwerf_setup_200knoten.py start
```

Die drei Schritte laufen **nacheinander** (setup erstellt tmp-`DATA_ROOT`, seed legt die 200 Items + 206 Kanten an, start startet den Dienst auf Port 18772 mit File-Keyring). Nikinger kann sich dann im Browser auf `http://127.0.0.1:18772` einloggen (User-Daten werden vom Setup-Skript ausgegeben).

**Aufräumen nach P8-22:**

```bash
.venv/bin/python phase8_ui_graph/scripts/wegwerf_setup_200knoten.py cleanup
```

(Hard Rule 9 — kein `pkill -f` mit Regex, das Skript nutzt die eigene PID-Datei.)

**Wenn stattdessen der D2-Wegwerf (Port 18768, 14 Knoten) reicht:** analog mit `phase8_ui_graph/scripts/wegwerf_setup_d2.py` (setup/seed/start/cleanup). Der D2-Datensatz hat zu wenig Knoten für P8-22 (< 200), reicht aber für P8-20/21/24 als kleinerer Datensatz (für mehr Daten am Live-Bildschirm).

---

## Anhang B — Wo die Ergebnisse hin müssen

**Im selben Schritt (Hard Rule 8 — Commit ⇒ Note-Update):**

1. Screenshots in `docs/screenshots/` ablegen (Namen wie oben vorgegeben).
2. `phase8_ui_graph/CLAUDE.md` §7-Matrix aktualisieren: P8-20/21/22/24-Zeilen mit Belegs-Spalte "Nikinger-Sichtprüfung 2026-09-XX live gegen v3.0.1: …" — die vier Zeilen wandern auf ✅, sofern keine Sub-Punkte rot waren.
3. `phase8_ui_graph/CLAUDE.md` Modul-Status Block-D-Zeile updaten ("Cluster 3 abgeschlossen, Nikinger-live-verifiziert").
4. Bilanz-Zeile updaten — neuer Lauf des awk-Kommandos (im §7-Bilanz-Abschnitt der Phase-8-Head-Datei dokumentiert) ergibt dann `Zeilen=26 ✅=23 🟡=3 ⬜=0` oder ähnlich.
5. Sichtprüfungs-Status-Tabelle (Plan §8) updaten.
6. Phase-8-Glyph-Entscheidung ✅/🟡 fällig — Vorschlag aus dem aktuellen Head: **🟡 vorerst**, weil Cluster 5 (P8-5/P8-8) noch offen ist; nach Cluster 5 → ✅.

**Commit-Message-Vorschlag:**

```
phase8.5: Cluster-3-Live-Verifikation -- P8-20/21/22/24 ✅
```

(P8.5-Repo, weil Cluster 3 Teil der Phase-8.5-Closeout-Vorbereitung ist; touch ggf. nur `phase8_ui_graph/CLAUDE.md`, keine Code-Änderung.)

**Wenn opencode/M3 den Status-Update macht:** `Phase-8.5`-Head-Session-Block ergänzen, Cluster-1-Block rotiert lassen, neuer Block "Cluster 3 (2026-09-XX)" — analog zum Cluster-2-Block vom 2026-09-07.
