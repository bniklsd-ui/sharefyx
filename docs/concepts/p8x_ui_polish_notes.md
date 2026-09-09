---
status: live
purpose: Notizen-Sammlung für die p8.X-Folge-Phase — UI-Polish, Layout, Settings, Design-System-Layering, Edit-in-Place-Vision; Findings aus Sichtprobe-Folgesession 2026-09-06 (Nikinger + Fabian, post Phase 8.5 D4)
read-when: Planung der p8.X-Phase, Scan der noch offenen UI-Wünsche nach Phase 8.5-Z; **nicht** eine Lese-Anweisung pro Commit — das macht der Phase-Head
detail: L2
up: ../CLAUDE.md
down:
  - ../phase8_ui_graph/CLAUDE.md                       # Phase 8 — Vorgänger, Closeout-§9.4.7 ist p8.X-Anker
  - ../phase8_5_picker_release/CLAUDE.md              # Phase 8.5 — Vorgänger, D4-Block + dieser Sichtprobe-Folgesession-Block
  - ../phase8_5_picker_release/SESSIONS_ARCHIVE.md     # Phase-8.5-Historie (D4 archiviert)
  - ../docs/concepts/phase8_ui_graph_plan.md            # §9.4.7 Phase-Status + p8.X-Übergabepunkt
  - ../phase8_ui_graph/SESSIONS_ARCHIVE.md              # §9.4.6 drei Restdefekte (Settle-Zeit / Foreign-Farbe / Knotenklick — bereits am 2026-09-02 geschlossen, hier referenziert)
updated: 2026-09-09 (Phase-8.5-Closeout-Session — **§10 NEU**: neun Nikinger-Feedback-Punkte aus dem Closeout-Prompt [Icon-Radien, Hover-Auswahl, Ordner-/Tags-Auswahl, klickbare Spaces, Einstellungsmenü, alles Klickbare mit Farbausnahme Abmelden/Archivieren, AI-Sessions, **Hochkant-/Handy-UI**], sieben davon Verschärfungen von §5/§6; §5 + §6 + §C-2 auf §10 verwiesen; **§B: „Mobile" durchgestrichen** — Nikinger-Aufhebung, Realtime bleibt draußen; §E +9 Zeilen; `updated:`-Pipe zweimal komprimiert wegen Softcap-Nähe; kein Code-Touch) | 2026-09-08 (Sichtprüfungs-Folge-Sitzung — §6 re-affirmiert [Lesarten a/b/c gegen `app.html:31-41`], §8 NEU Tags, §9 NEU Feedback-Button, §E +3) | 2026-09-06 (Sichtprobe-Folgesession Nikinger + Fabian — neue Datei, §1–§7 angelegt, fünf D4-Punkte zusammengeführt)
---

# p8.X — UI-Polish & Iterations (Notizen, keine Planung)

> **Stand:** Sammlung von Findings, kein Plan. Phase 8 ✅ + Phase 8.5 ✅ sind seit dem
> 2026-09-08/-09 formal geschlossen; die Folge-Phase heißt inzwischen **P8.6** (→ `v3.0.2`),
> der große Graph-Umbau **P9** (→ `v3.1.0`). Anker im Phase-8-Plan: §9.4.7.
>
> **Diese Datei ist die einzige Schreib-Stelle**, bis eine Planungs-Session stattgefunden
> hat (Claude Code, weil §5 Layering design-system-weit ist). Neue Punkte hier anhängen,
> nicht im Head einer abgeschlossenen Phase. Verzeichnis- und Plan-Dateiname sind weiter
> offen (§D) — `p8x-…` bleibt bis dahin der formlose Kurzname.

---

## Provenance / Herkunft

Zwei Quellen münden hier:

1. **Phase 8.5 D4-Block** (2026-09-06, Nikinger am echten Gerät gegen v3.0.1-Deploy) hat
   fünf p8.X-Punkte dokumentiert: UX-2-Step-Knotenklick, Map-Field schneidet unten ab,
   Map fliegt bei jedem Reload, Save-Button-YAML-Header (Verifikation außenstehend),
   Fabis Sammelliste. Quelle: `phase8_5_picker_release/CLAUDE.md` Session-Block.
2. **Sichtprobe-Folgesession** (2026-09-06, Nikinger + Fabian am echten Gerät, im selben
   Sichtprobe-Komplex) hat **sieben weitere Themen-Cluster** aufgemacht, die D4 nicht
   gesehen hat — siehe §1–§7 unten. Quelle: Bericht des Nikingers aus dieser opencode/M3-
   Session (`Special task / note from last session` im Sitzungs-Prompt).

Alle Punkte hier sind **konzeptuell**, nicht implementiert. Kein Code-Touch, kein
Commit, keine Phase-8.5-Berührung.

---

## §1 Spaces-Übersicht Layout (Reorganisation)

**Finding (Nikinger, 2026-09-06, Sichtprobe-Folgesession):**

> Aktuelle Leiste mit „alle Items" lieber **unter** die aktuelle Spaces-Ansicht schieben,
> mit Kippschalter umschaltbar. „Obsidian Map" erhält ca. 40 % der gesamten Seite (wenn
> Übersicht geöffnet ist) und **gesamte Höhe**. Sonst doppelte Elemente.

**Was das meint (Interpretation, **nicht** autoritativ — mit dem Nikinger zu validieren):**

- Die linke Rail hat heute oben „Spaces" und darunter „Alle Items" als zwei separate,
  dauerhaft sichtbare Bereiche. Künftig: Spaces oben, „Alle Items" darunter — und ein
  Kippschalter, der bestimmt, was im Hauptbereich angezeigt wird (vermutlich Spaces-
  Liste vs. globale Items-Liste).
- Die Obsidian-Map übernimmt **40 % der Seitenbreite und die volle Höhe**, **wenn die
  Übersicht geöffnet ist**. Außerhalb dieses Modus keine doppelten Elemente — d. h.
  entweder Liste **oder** Map, nicht beides nebeneinander, je nach Sichtbarkeit der
  Übersicht.

**Offene Entscheidungen:**

- Was ist mit dem globalen Items-Modus aus `phase6_shares/GLOBAL_SEARCH_PLAN.md`? Der
  Kippschalter ersetzt vermutlich den aktuellen „Home"-Toggle — gleicher Mechanismus,
  andere Bezeichnung?
- Welche Map-Höhe gilt im Spaces-Modus? Volle Höhe bleibt vermutlich nur für die Map;
  im Listen-Modus füllt die Liste die Höhe — kein Höhensprung beim Umschalten.

**Bezug:** Phase-8-Block-D-Übersicht (`docs/concepts/phase8_ui_graph_plan.md` §5 D1).
Layer-Z-Übersichtsgrafik (`docs/concepts/phase8_ui_graph_uebersicht.svg`) ist die
aktuelle Wahrheit und zeigt den heutigen Doppel-Element-Stand.

---

## §2 Obsidian-Map — Performance, Style, Layout

Vier Findings + eine Vision aus dem Bericht, plus drei aus D4 übernommen:

### §2.1 Performance: Reload-Overload

**Finding (Nikinger, 2026-09-06):** Jeder Klick auf Übersicht lädt die Map neu →
überlastet schnell.

**Vermutung:** Die Map wird in `phase5_ui/webui/static/js/graph.js` bei jedem
Öffnen der Übersicht komplett neu aufgebaut (Canvas leeren, Nodes neu berechnen,
Kräfte neu starten) statt z. B. einmal zu mounten und nur die Daten aus dem
`_graph_get` zu aktualisieren.

**Entscheidungen nötig:** Lebenszyklus der Map-Komponente — wird sie einmal
gemountet und nur Daten/Position aktualisiert, oder jedes Mal neu instanziiert?
Falls zweiteres: warum?

**Bezug:** Phase 8 §5 D2 (Canvas-Force-Graph). V102 hat bereits die Zwillings-Kante
`body+frontmatter` gemessen — dort gibt es ersten Smoke-Code, an dem eine
Performance-Session andocken könnte.

### §2.2 Style: Landkarte statt Netz

**Finding (Nikinger, 2026-09-06):** Aktuelle Farben + übernehmen (außer Hintergrund),
**aber eher wie eine Landkarte aufbereiten, schöner stilisieren und in den aktuellen
Gesamt-Style übernehmen**.

**Interpretation:** Heute ist der Graph ein Force-Layout mit Knoten + Kanten auf
neutralem Hintergrund. „Landkarte" deutet auf stärkere räumliche Komposition hin:
Gruppen/Cluster sichtbarer, Regionen/Hintergründe, evtl. Pfade/Verbindungs-Hierarchie.
„Aktuelle Farben übernehmen" heißt: `--space-own` / `--space-shared` / `--space-foreign`
bleiben, der Hintergrund **nicht** (siehe §5 Layering — Hintergrund wird ein eigener
Layer, nicht der Map-Background).

**Bezug:** Phase 8 §0.3 Verbotsliste Pkt. 4 („Farbe nur mit Bedeutung"). Landkarten-
Stilisierung muss mit der Legende konsistent bleiben — sonst zurück zur
AI-Template-Falle.

### §2.3 Layout: Map-Field schneidet unten ab

**Finding (Nikinger, 2026-09-06, D4-Block bestätigt):** Im Übersicht-Modus ragt die
Map über den sichtbaren Bereich hinaus; der untere Teil ist abgeschnitten.

**Verdacht:** Canvas-Höhe wird im CSS auf `100%` oder eine Konstante gesetzt, aber
der Container hat ein `overflow: hidden` ohne Flex-/Grid-Layout, sodass die Map
nicht mitwächst. Direkter Link auf den Code fehlt — Phase-8-Block-D-Smoke müsste
das messen, bevor ein Fix vorgeschlagen wird.

**Bezug:** `phase5_ui/webui/static/js/graph.js` und `app.css` (Container-Layout).

### §2.4 Layout: Map-Reload-Drift (Fliegen)

**Finding (Nikinger, 2026-09-06, D4-Block bestätigt):** Map „fliegt" bei jedem Reload
durcheinander — kein persistenter Layout-Seed, jeder Mount startet mit frischen
Random-Kräften.

**Vermutung:** Force-Simulation verwendet nicht-deterministische Initial-Kräfte
(wahrscheinlich `Math.random()` für die Startpositionen). Lösung: deterministischer
Seed auf Basis der Item-ID (z. B. Hash der IDs → stabile Startpositionen) oder ein
in `localStorage` gespeicherter „letzter Layout-Snapshot".

**Entscheidungen nötig:** Seed-Determinismus oder persistente Snapshots? Ersteres ist
trivial und reicht vermutlich; letzteres brächte „Position beibehalten beim
Wiederöffnen" — was vermutlich mehr will, aber deutlich mehr Code.

### §2.5 UX: Karte einklappen mit Abhängigkeiten

**Finding (Nikinger, 2026-09-06, Sichtprobe-Folgesession):** „Karte einklappen mit
den Abhängigkeiten".

**Interpretation:** Die Map soll einklappbar sein, **und im eingeklappten Zustand
sollen Abhängigkeiten sichtbar bleiben**. Vermutlich: zugeklappt = Mini-Ansicht mit
nur den Items + einer verdichteten Kanten-Repräsentation (z. B. Kanten-Counts pro
Item-Hover); aufgeklappt = volle Karte.

**Offen:** Was genau ist mit „Abhängigkeiten" gemeint? Verknüpfungs-Kanten aus
`storage/linkscan.py`? Tag-/Ordner-Beziehungen? Voraussetzung/Wahlverwandtschaft?

### §2.6 §2-Bezug: alles §2 ist Phase-8-Block-D-Code

`phase5_ui/webui/static/js/graph.js` ist der zentrale Anker. `app.css` für Layout
und Container. Beide sind nicht im Phase-8.5-Tabu §0.3 — ein Phase-9/p8.X-Eingriff
ist hier ungehindert möglich, sofern die Phase-8-§0.3-Verbotsliste weiterhin
respektiert wird (kein Gradient-Branding, keine dekorativen Farben, kein 3er-Card-
Grid, Plex Sans/Mono bleibt, keine Transparenz-Abhängigkeit).

---

## §3 Anzahl-Anzeige „Aufgaben / Notizen im Ordner"

**Finding (Nikinger, 2026-09-06, Sichtprobe-Folgesession):** „Anzahl der Aufgaben und
Notizen, die in einem Ordner sind" soll angezeigt werden.

**Offene Entscheidungen:**

- **Wo?** Im Ordner-Tab der Liste (jeder Folder-Eintrag bekommt einen Count-Chip),
  im Detail-Header des geöffneten Ordners, oder beides?
- **Wie zählen?** Nur `status=active`? Auch `archived`? Nach Typ (Task/Note)?
- **Rechte:** Ein fremder Share-Read-Ordner zeigt vermutlich nur lesbare Items —
  dieselbe Filter-Logik wie der `GET /api/v1/items`-Endpunkt mit `folder=`-Filter.
- **Performance:** Index-Tabelle zählt bereits (`item_links`-Tabelle ist ein Vorbild
  für O(1)-Lookups); ein `folder`-Count ist eine triviale Aggregation, kein neuer
  Endpunkt nötig.

**Bezug:** P6 Step 7b (Ordner in Spaces), P7 (Space-Verwaltung). Index-Eintrag in
`storage/index.py` ist der Bauplatz, sofern nicht ohnehin schon ein Folder-Count
mitläuft — zu prüfen, nicht zu raten.

---

## §4 Edit-in-Place (Zukunftsnotiz)

**Finding (Nikinger, 2026-09-06, Sichtprobe-Folgesession):**

> Zukunftsnotiz: „bearbeiten" Knopf soll überflüssig werden und nur im Hintergrund
> technisch ablaufen. User bearbeitet wie z. B. in Word direkt in der aktuellen
> „Übersichtsansicht".

**Was das meint (Interpretation, **nicht** autoritativ):** Statt Klick auf „Bearbeiten"
→ Editor öffnet sich → tippen → „Speichern" → Editor schließt sich, soll der
Bearbeitungs-Modus **ohne** Modus-Wechsel funktionieren: der Text im Read-View ist
direkt editierbar, das Speichern passiert automatisch im Hintergrund.

**Harte Probleme — nicht-trivial:**

1. **Hard Rule 3 (kein Last-Write-Wins).** Auto-Save bei jeder Tastatureingabe
   erzeugt viele konkurrierende PATCHes; der Server lehnt jeden Replay korrekt ab,
   der User bekommt einen Konflikt-Dialog **während des Tippens**. Lösung vermutlich:
   Debounce + Edit-Lock pro Item (Holding-Pattern).
2. **P7-24 (TOTP-Replay im Batch).** Wenn Auto-Save einen Patch auslöst, der
   Schreibrechte erweitert (z. B. Ordner-Wechsel eines Items in einen geteilten
   Space), braucht es einen Reauth-Grant. Der existiert seit Phase 8 A1, aber ein
   Mid-Edit-Reauth-Dialog ist UX-feindlich.
3. **Rückweg.** Was, wenn der User den Bearbeitungs-Modus explizit verlassen will?
   „Fertig"-Knopf? Klick außerhalb? Escape-Taste? Letzteres kollidiert mit dem
   Editor-Verhalten.

**Entscheidungen nötig (größerer Brocken — eventuell eigene Phase):**

- Ist Edit-in-Place eine Vision, die vor einer Planung erstmal mit einem Klick-
  Prototyp im `editor.js` ausprobiert wird?
- Oder ist es ein vollständiger UX-Reset, der Phase 8 + 8.5 designtechnisch
  ablöst?
- Beziehung zum UX-2-Step-Knotenklick (§5.5 unten): der Knotenklick ist die
  Readonly-Vorstufe von Edit-in-Place — beide Features teilen sich die Vorarbeit.

**Bezug:** Phase 5 (`editor.js` Edit-Modus), Phase 8 A1 (Reauth-Grant).

---

## §5 Layering-Design-System (POLITIK)

**Finding (Nikinger, 2026-09-06, Sichtprobe-Folgesession):**

> **UI Design Politik: Layering:** hinterster Layer echtes Schwarz (wenig vorhanden,
> auf echten OLED-Displays cool), dann 2. Layer (den wir aktuell als Standard haben) →
> verwendet für z. B. Map-Hintergrund, Schreib-Hintergrund. **Auswahl-Box zählt nicht
> als Layer, daher blau.** Jegliche Auswahl-Elemente bitte darauf anpassen, auch
> Hover-Auswahl, auch Notiz-Auswahl bei Space-Übersicht, oberster Layer liquid glass,
> ggf. checken ob das aktuell auch wirklich überall so ist (z. B. verwendet für
> Auswahlboxen).

**Drei explizite Layer:**

| # | Layer | Verwendung | Farbe heute |
|---|---|---|---|
| 0 (back) | Echtes Schwarz | Sparsam, OLED-Display-Highlight | `--rail-bg` / dunkler Body-BG, evtl. nicht 0/0/0 |
| 1 (mid)  | Aktueller Standard | Map-Hintergrund, Schreib-Hintergrund (Editor) | aktuelle Standard-CSS-Variablen |
| 2 (top)  | Liquid Glass | Modale Dialoge, evtl. Aktionsleisten | bereits Phase 8 C4 (`.dialog`, Glass-Fallback `@supports`) |

**Auswahl zählt NICHT als Layer — sie ist immer blau.** Konkret:

- **Hover-Auswahl** (Maus über Item): blau, nicht Glass
- **Notiz-Auswahl in Space-Übersicht**: blau, nicht Glass
- **Auswahl-Box (Checkbox / Multi-Select)**: blau, schon korrekt (?)
- **Auswahl-Boxen allgemein**: blau, prüfen ob überall konsistent

**Aktuelle Lage (Annahme, im Code zu verifizieren):** Phase 8 C4 hat
`.list__row[aria-current]` + `.list__row--selected` mit Auswahl-Sheen (3 px +
Outline) eingeführt; die Farbe ist `--accent` (blau), aber die Glass-Akzente
kommen daneben auch vor. **Audit nötig:** Welche Auswahl-Elemente verwenden
heute versehentlich Glass statt Blau? — `grep`-Sweep über `app.css` +
`dialogs.js` + `editor.js` nach Glass-Farben in Selektoren, die `.selected` /
`[aria-current]` / `:hover` enthalten.

**Entscheidungen nötig:**

- Echtes Schwarz (`#000` oder `--bg-void`): in welchen Komponenten? Vorschlag:
  Boot-/Loading-Screen, leere Zustände (`__empty`), System-Banner. **Wenig
  vorhanden** ist explizit gewollt.
- Layer-Token-System: `--bg-void` / `--bg-standard` / `--bg-glass` als verbindliche
  Schreibweise in `app.css`?
- Glass-Layer: bleibt bei Modals/Dialogen (C4) — keine Änderung.
- **Selektions-Farbe vereinheitlichen:** ein einziger Token (vermutlich `--accent`)
  für **alle** Auswahl-Zustände. Hover, Focus, Selected, Checkbox.

**Bezug:** Phase 8 §0.3 Verbotsliste Pkt. 6 (kein Element, dessen Erkennbarkeit
allein von Transparenz/Blur abhängt). Die Politik ist konsistent mit dieser Regel
— Selektion ist nie glass-only.

**[2026-09-09] §10 verschärft diese Politik** um sieben konkrete Stellen (Hover als
transparentere Standardauswahl, Ordner-/Tags-/Einstellungs-Auswahl, alles Klickbare) —
§5 und §10 zusammen lesen, nicht getrennt planen.

**Größter Brocken der Sichtprobe-Folgesession.** Diese Politik zu implementieren
heißt: alle UI-Komponenten einmal auditieren, Glass-Tokens korrekt zuordnen,
Selektions-Farbe vereinheitlichen. Vermutlich eine eigene Planungs-Session in
Claude Code, weil Layout-übergreifend.

---

## §6 Settings/Navigation — „Konto" → „Einstellungen"

**Finding (Nikinger, 2026-09-06, Sichtprobe-Folgesession):**

> „Konto" zu „Einstellungen" ändern, **Position mit Abmelden-Knopf vertauschen**.

**Was das meint (Interpretation, **nicht** autoritativ):** Der Menüpunkt heißt heute
„Konto" und steht vermutlich oben; er soll „Einstellungen" heißen und die Position
mit dem Logout-Button tauschen. **Resultat vermutlich:** Einstellungen oben (häufiger
gebraucht), Logout unten (selten gebraucht, weniger prominent).

**[2026-09-08, Re-Affirmation durch den Nikinger]** in der Phase-8.5-Sichtprüfungs-
Folge-Sitzung am echten Gerät — der Punkt ist weiterhin offen und gewollt, kein
Seiteneffekt einer anderen Änderung. Wortlaut aus dem Sitzungs-Prompt: „change the
„Konto" and „abmelden" Button Position and change „Konto" to „Einstellungen" that's
more suiting."

**Offene Fragen:**

- Genauer Tausch: nur die zwei Buttons, oder Reihenfolge aller Punkte im
  Account-Menü?
- Sind weitere Menüpunkte betroffen? (TOTP-Reset, Passwort-Änderung,
  Recovery-Code, Space-Wechsel — hängen die an „Konto" oder „Einstellungen"?)
- **Aktueller Code-Stand:** `app.html:31-41` rendert Konto (Zeile 32-34) **vor**
  Abmelden (Zeile 38-40) im Block `.rail__account`. „Vertauschen" kann also nur
  bedeuten: (a) Abmelden über Konto setzen (Logout oben, Einstellungen unten —
  widerspricht der Interpretation oben), (b) Konto/Logout **beide** an eine andere
  Stelle im Rail verschieben (z. B. „Einstellungen" ganz oben, „Abmelden" ans
  Rail-Ende), oder (c) den Konto-Knopf vom Logout-Knopf durch eine visuelle
  Trennung klarer unterscheiden (Konto gefüllt/Sektion-Header, Logout als
  Sekundäraktion). **Klärung in der Planungs-Session nötig**, nicht raten.

**[2026-09-09] §10 hängt zwei Dinge an diesen Punkt:** §10.6 (das ganze
Einstellungsmenü bekommt die Standardauswahl) und §10.8 (verbundene AI-Sessions
anzeigen, vom Nikinger nach hinten gelegt).

**Bezug:** Phase 5 Block A (Auth-Selbstverwaltung, `phase5_ui/webui/static/
app.html` / `pages.py`). Kleiner Fix, vermutlich 5–10 Zeilen + ein i18n-String-
Update.

---

## §7 De-AI-ierung — weiterer Lauf nach neuen Kriterien

**Finding (Nikinger, 2026-09-06, Sichtprobe-Folgesession):**

> weiterer Lauf zur „ent-AI-isierung" der UI erforderlich, nach **neuen Kriterien**
> suchen. Danach Lauf zu wirklichen Erstellungs-Regeln von UI, mein Layer-Vorschlag
> war nur einer von vielen.

**Stand Phase 8 §0.3 (was schon verboten ist):**

1. Keine Emoji und keine HTML-Entity-Zeichen als Icons — nur das Lucide-Sprite.
2. Kein Indigo/Violett-Gradient, überhaupt kein Gradient als Flächen-Branding.
3. Keine generischen 3er-Feature-Card-Grids; Struktur über Dichte/Whitespace.
4. Farbe nur mit Bedeutung — nie dekorativ.
5. Keine neuen Schriftfamilien außer Plex Sans/Mono.
6. Kein Element, dessen Erkennbarkeit allein von Transparenz/Blur abhängt.

**Was „nach neuen Kriterien suchen" meint:** Diese sechs Verbote fangen offensichtliche
AI-Template-Marker ab. Ein **zweiter Pass** muss subtilere Marker prüfen:

- Hover-Verhalten: AI-Templates lieben 200–400 ms ease-in-out auf allem. Menschliche
  UIs haben unterschiedliche Timing-Kurven je nach Element.
- Klickbarkeit: AI-Templates markieren klickbare Elemente durchgehend mit
  Border-Highlight. Echte UIs unterscheiden — manche sind nur per Cursor erkennbar.
- Spacing-Skala: AI-Templates verwenden 8-px-Multiplikatoren starr. Echte UIs haben
  unregelmäßige Abstände.
- Iconographie: Lucide ist gut, aber die Auswahl verrät — AI wählt immer dieselben
  30 Symbole. Echte Designer kuratieren.
- Typografie-Gewichtungen: AI neigt zu Medium/Regular auf allem, Bold nur für
  H1. Echte UIs haben differenzierte Gewichtungen.

**Dann: „Lauf zu wirklichen Erstellungs-Regeln von UI".** Aus den Verboten +
Kriterien soll ein **positiver** Regelsatz entstehen: was tun, nicht nur was nicht.
Vermutlich eine Session in Claude Code (researchlastig), keine opencode/M3-Session.

**Offene Entscheidungen:**

- Wer macht den zweiten Pass? Nikinger allein (subjektive Bewertung), oder mit
  Fabian zusammen, oder als externe Recherche?
- Wann? Vermutlich vor p8.X, weil die Regeln dann in den p8.X-Plan einfließen.

---

## §8 Tags für Aufgaben — konfigurierbar + Standard „blocked" (2026-09-08)

**Finding (Nikinger, 2026-09-08, Phase-8.5-Sichtprüfungs-Folge-Sitzung am echten
Gerät):**

> 1. customizable Tags for tasks (only cosmetic) as well as a „blocked" Standard Tag.

**Zwei Teilpunkte:**

### §8.1 Customizable Tags (kosmetisch)

Heute ist das Tag-Feld ein freier Texteingabe (`#field-tags`, `editor.js:154`/`352`)
mit Komma-Trennung — alles geht, nichts ist „kanonisch". Die Wunschvorstellung:
nutzer-kuratierte Tag-Liste, aus der im Editor bequem gewählt werden kann
(Klick → Tag togglen, statt tippen), mit selbst-definierten Farben oder
zumindest unterscheidbaren Chips. **„Only cosmetic":** die Tag-Auswahl ist **rein
visuell / organisatorisch** — keine Server-Semantik, keine Filterlogik im
Graphen ändert sich, keine Rechteauswirkung. Der Server kennt weiterhin nur
eine Liste von Strings pro Item; die App kuratiert die *Eingabe*, nicht die
*Interpretation*.

**Heutiger Stand (Code, vor jedem Build zu lesen):** `editor.js:154`
`tags: fieldTagsEl.value.split(",").map(s => s.trim()).filter(Boolean)` —
reiner String-Split, keine Autocomplete-Logik, keine Tag-Wissen. `list.js:144`
zeigt die Tags im Read-View als komma-separierte Liste; im Editor steht der
Wert 1:1 in einem `<input type="text">`.

**Mögliche Umsetzung (zur Diskussion, nicht autoritativ):**

- `localStorage["sfx:tags:palette"]` als Array `[{name, color?}]`, vom User
  im Settings-Dialog pflegbar (vermutlich in dem Dialog, der mit §6
  „Einstellungen" gemeint ist).
- Im Tag-`<input>`: Vorschlagsliste (Datalist oder kleines Popover)
  gefiltert auf die Palette, neue Tags jederzeit möglich (Palette bleibt
  gewachsen).
- Keine Server-Änderung — Phase-8-Tabu-Liste §0.4 bleibt zu prüfen, aber
  die Tags-Speicherung in `Store` (`storage/store.py`) ist nicht betroffen.

### §8.2 Standard-Tag „blocked"

Ein vom System *bereitgestellter*, immer verfügbarer Tag — kein User-pflegbarer,
sondern fest im Code: „blocked". **Wofür?** Aus dem Kontext der Sichtprüfung
wahrscheinlich: ein Status-Tag für Aufgaben-Items (`type: task`), die
bewusst pausiert / wartend markiert sind, bis eine Bedingung erfüllt ist
(Person X antwortet, anderes Item wird erledigt, etc.). „Standard" impl
vermutlich: (a) immer in der Palette vorhanden, auch ohne explizites
Hinzufügen, (b) im Editor mit einem festen visuellen Signal versehen
(auffällige Farbe / Warn-Icon), (c) optional mit Sonderverhalten in
irgendeiner Liste (z. B. Buckets „Offen / blocked / Erledigt / Notizen").

**Offene Fragen (Klärung in der Planungs-Session):**

- Hat „blocked" **Semantik** oder bleibt es „nur ein weiterer Tag"?
  - „Nur kosmetisch": gleiche Code-Pfad wie jeder andere Tag, nur
    vordefinierter Name + Farbe. **Wahrscheinlichste Lesart** — passt zur
    Einschränkung „only cosmetic" in §8.1.
  - „Mit Semantik": Item mit Tag „blocked" wandert in einen eigenen Bucket
    oder bekommt einen Filter-Chip in der Liste. **Größerer Eingriff** —
    berührt `list.js :: renderItems()`, `GET /api/v1/overview`-Buckets
    (`webui/api.py :: _overview_get`), vermutlich auch die
    Frontmatter-Validierung in `storage/frontmatter.py` (gibt es eine
    Allowlist für besondere Tag-Werte?). Tabu-Frage für p8.X.
- Reihenfolge der Chips / Position des „blocked"-Tags in der Palette
  (oben, weil wichtig? unten, weil selten?).
- Falls §8.1 umgesetzt wird: ist „blocked" ein **immer vorhandener
  Standard-Tag** (im Code hartcodiert) oder ein **erster Eintrag der
  Default-Palette**, den der User löschen kann? Ersteres ist
  vorhersagbarer (jeder Nutzer sieht ihn), zweiteres ist sauberer
  (Customizing = Customizing).

**Bezug:** `phase5_ui/webui/static/js/editor.js` (`#field-tags`,
`fieldTagsEl.value.split(",")`), `phase5_ui/webui/static/js/list.js:144`
(`item.tags.join(", ")`-Render), `phase5_ui/webui/static/app.css`
(Chip-Styles — soweit vorhanden, vermutlich generisch). Server unverändert,
sofern §8.2 kosmetisch bleibt.

---

## §9 Direkter User-Feedback-Button (2026-09-08)

**Finding (Nikinger, 2026-09-08, Phase-8.5-Sichtprüfungs-Folge-Sitzung am echten
Gerät):**

> 2. a direkt User Feedback Button.

**Was das meint (Interpretation, **nicht** autoritativ):** ein einfach
auffindbarer Button in der UI, der es dem User erlaubt, *direkt* ein Feedback
abzugeben — Bug, Verbesserungsidee, Verständnisfrage — ohne den Workflow
zu verlassen (kein „öffne GitHub, schreibe ein Issue, paste den Stacktrace").
Heutige Realität: User müssen den Nikinger ansprechen (im Raum oder im
Chat), oder selbst zur Tastatur greifen und die Mail an
`nikinger@…` schreiben. Das skaliert nicht, bremst Fabi + Nikinger, und
verschwindet still im Chat-Verlauf.

**Was „direkt" wahrscheinlich meint (zur Diskussion):**

- **Aus der App heraus, ohne externen Browser-Wechsel.** Vermutlich ein
  Klick auf einen Button in der Rail oder im Settings-Dialog öffnet ein
  Overlay/Formular mit: Freitext-Feld + optional Titel + optional
  Screenshot-Knopf (Browser-native, nicht aus der App heraus) +
  „Senden"-Knopf.
- **An wen?** Drei plausible Senken:
  - **In eine Datei im Sharefyx** (eigener Space „Feedback", Item-Type
    „note", vom Nikinger periodisch gelesen) — *im Repo-Kern*, Hard
    Rule 4 („fremde Spaces sind read-only") bewusst umgangen, weil
    der User sein **eigener** Space ist.
  - **In eine Datei auf der Platte der VM** außerhalb des `DATA_ROOT`
    (`/var/log/sharefyx/feedback/…md`) — getrennt vom User-Storage,
    Nikinger-only lesbar.
  - **An einen externen Endpunkt** (E-Mail, Matrix-Bot, Webhook) — dann
    ist der Server nicht mehr „dumm", und die Server-Tabu-Liste aus
    Phase 8 §0.4 müsste neu bewertet werden (ein Webhook ist ein
    *ausgehender* Call, nicht verboten, aber neu).
- **Was darf mitgeschickt werden?** Freitext (Pflicht), User-Space (zur
  Identifikation, kein Auth-Token), Browser/User-Agent, App-Version
  (`v3.0.1` heute), aktuelle URL. **Kein** TOTP-Code, **kein** Passwort,
  **kein** Recovery-Code, **kein** Session-Cookie — Feedback-Button ist
  eine **Mensch-Aktion**, die nichts Sicherheitsrelevantes anfasst.

**Was diese Phase NICHT macht (zur Klärung, damit es kein Default-Blocker wird):**

- Eine Server-Implementierung. p8.X umreißt das Feature; die
  Implementierung folgt in der Phase, die p8.X ablöst.
- Eine UI-Komponente. Der Button-Ort ist nicht entschieden (Rail-Block?
  Help-Menü? Settings-Dialog? Konto/Einstellungen-Dialog? Footer im
  Read-View eines Items?).
- Eine Selbsttest-Schleife („kann ich mich selber anpingen?"). Vermutlich
  will der Nikinger nur die *Möglichkeit*, nicht eine sofortige Antwort.

**Bezug:** „Direkt" deutet auf UI-Affordance, die keinen Umweg über Mail/
GitHub/Chat verlangt. Phase-8-Tabu-Liste ist heute nicht betroffen (kein
Server-Code, kein API-Endpoint, keine Schema-Änderung), solange die
gewählte Senke im bestehenden `DATA_ROOT` (User-Space) liegt.

**Offene Fragen:**

- Wo wird der Button platziert? (Vorschlag: Rail unter „Einstellungen"
  und „Abmelden", oder im Read-View-Header eines Items, oder beides.)
- Senke: Sharefyx-Space-Feedback-Item, `/var/log/sharefyx/feedback/`,
  oder externer Endpunkt?
- Soll es ein **anonymer** Modus existieren (kein Space-Name)?
  Wahrscheinlich nicht, weil der Nikinger dann nicht antworten kann —
  aber: fragen, nicht entscheiden.
- Throttling? (Spam-Schutz: ein Feedback pro 5 Minuten pro Space?)
  Vermutlich überzogen, aber: Hard Rule 7-Disziplin („kein Spam, kein
  versehentlicher DoS").

---

## §10 Auswahl-, Klick- und Form-Vereinheitlichung (Nikinger, 2026-09-09)

**Herkunft:** Feedback im Phase-8.5-Closeout-Auftrag, gesammelt „in der Zwischenzeit" am
echten Gerät. **Sieben der neun Punkte sind keine neuen Themen, sondern die konkrete
Ausformung von §5 (Layering / Selektion ist blau) und §6 (Settings)** — wer §10 plant,
liest §5 zuerst. Zwei Punkte sind neu: AI-Sessions (§10.8) und Hochkant-UI (§10.9).

| # | Punkt (Nikinger-Wortlaut, gekürzt) | Bezug | Art |
|---|---|---|---|
| 10.1 | „Alle Icons auf selbe abgerundete Ecken anpassen" | neu, formal | Radien-Audit |
| 10.2 | „auch hover auswahl unserer „Standard" Auswahl anpassen" | §5 | Selektion |
| 10.3 | „auch die „Ordner" und „Tags" auswahl zur Standard auswahl anpassen" | §5 | Selektion |
| 10.4 | „Spaces in der übersicht clickable" | §1 | Interaktion |
| 10.5 | „Vorschlag für Hoverauswahl: standardauswahl aber etwas transparenter" | §5 | Selektion |
| 10.6 | „gesamtes Einstellungsmenü … ebenfalls mit der Standard auswahl versehen" | §6 | Selektion |
| 10.7 | „alle Buttons …, inklusive clickable Links, Item zahl bei der Übersicht, generell alles was clickable ist selbiges design, nur „abmelden" und „archivieren" evtl andere Farbe" | §5 | Selektion |
| 10.8 | „In Einstellungen … verbundene AI Sessions anzeigen (Zukunft, eher v3.1 also p8.7)" | §6 | Feature |
| 10.9 | „Hochkant bzw Handy version der UI als wichtiges Item der Zukunft notieren" | §B-Umkehr | Layout |

**§10.1 — Ausgangslage (im Code geprüft, 2026-09-09):** `app.css` trägt **37**
`border-radius`-Deklarationen mit **sechs** Werten — `var(--radius)` 10px,
`var(--radius-sm)` 6px, `999px`, `50%`, ein **hartkodiertes `6px`** in
`.link-picker-results` (am Token vorbei) und `0` in `.tree__scope`. Icons tragen meist
selbst keinen Radius, sie erben ihn von der Trägerfläche. **Vermutlich also ein
Trägerflächen-Audit, kein Icon-Audit** — am Screenshot verifizieren, nicht aus dieser
Notiz übernehmen.

**§10.2 + §10.5 — Hover als transparentere Standardauswahl.** Verschärfung von §5 („blau,
nicht Glass"): §10.5 sagt jetzt *wie* blau — dieselbe Optik, reduzierte Deckkraft. Das
braucht **keinen zweiten Token**, nur einen Alpha-Wert auf dem bestehenden. Offen: Alpha
auf Fill, Outline oder beidem?

**§10.7 — die Farbausnahme ist die eigentliche Entscheidung.** „Alles Klickbare gleich" ist
billig; interessant ist, dass **„Abmelden" und „Archivieren" ausdrücklich anders sein
dürfen**. Beides sind Aktionen mit Rückweg-Kosten. Zu klären: ist das eine dritte
Button-Kategorie („destruktiv/irreversibel") im Sinne der Selection/Choice-Konvention v3,
oder zwei Einzelfälle? **Nicht raten** — der Nikinger schreibt „evtl.".

**§10.8 — verbundene AI-Sessions.** Zeitlich vom Nikinger selbst nach hinten gelegt
(„Zukunft, eher v3.1 also p8.7"). **Achtung, Nummern-Konflikt:** die Dokumente kennen kein
P8.7 — dort steht P8.6 → `v3.0.2` und P9 → `v3.1.0`. Der Wortlaut ist hier zitiert, es wurde
**nichts umbenannt**; die Planungs-Session klärt, ob „p8.7" ein neuer Zwischenschritt ist
oder das meint, was heute P9 heißt. Inhaltlich: eine Anzeige der aktiven OAuth-Grants/
Sessions in den Einstellungen — das ist **kein reines UI-Thema**, es braucht eine Leseseite
auf `authserver/`-Daten und fällt damit unter die Tabu-Frage (§C-6).

**§10.9 — Hochkant/Handy hebt eine Außenkante auf.** Bis heute stand „Mobile/Realtime" in
§B und im ROADMAP-Abschnitt als bewusst draußen. Der Nikinger hebt die **Mobile-Hälfte**
auf: die Hochkant-Ansicht soll als wichtiges Zukunfts-Item notiert sein, damit eine spätere,
freiere Phasenplanung sie berücksichtigt. **Realtime bleibt draußen.** Ausdrücklich **kein
P8.6-Auftrag** — ein Merkposten für die Phase danach.

**Reihenfolge-Hinweis:** §10.1–§10.7 fassen dieselben Selektoren an wie §5 und gehören
plausibel in dieselbe Welle. Entscheidung: Planungs-Session (§C-2).

---

## §A Anhang: bereits in Phase 8.5 D4 dokumentierte p8.X-Punkte

Aus dem D4-Block (`phase8_5_picker_release/CLAUDE.md`), hier zusammengeführt +
Duplikatverweis auf den Originalblock:

| # | Punkt | Status | Verweis |
|---|---|---|---|
| **D4-1** | **UX-2-Step-Knotenklick**: erster Klick öffnet Readonly-Scroll-Vorschau (ESC/Outside-Click schließt), zweiter Klick öffnet vollständig | Parkiert, p8.X | Phase 8.5 D4 §Drei echte Findings #3 |
| **D4-2** | Map-Field schneidet unten ab | Parkiert, p8.X | Phase 8.5 D4 §Vier kleinere Punkte + identisch §2.3 hier |
| **D4-3** | Map „fliegt" bei jedem Reload (persistente Layout-Seed) | Parkiert, p8.X | Phase 8.5 D4 §Vier kleinere Punkte + identisch §2.4 hier |
| **D4-4** | Save-Button-YAML-Header-Issue (Picker → `#field-links` modifiziert, aber Save-Button unlockt nicht, wenn Cursor im YAML-Header; Workaround „Leerzeichen einfügen") | Parkiert, **Verifikation außenstehend**: wenn gleicher Bug auch außerhalb Header-Kontext, dann Phase-8.5-Fix, sonst p8.X | Phase 8.5 D4 §Vier kleinere Punkte |
| **D4-5** | Fabis Sammelliste (laufend) | Parkiert, p8.X | Phase 8.5 D4 §Block 7 + §Phase-8-Closeout-Entscheidung |

**Phase 8 §9.4.6 drei Restdefekte (Settle-Zeit / Foreign-Farbe / Knotenklick) wurden
bereits am 2026-09-02 in Phase 8 D2-Session geschlossen** (Nikinger-Entscheidung
Option (a) für alle drei) — **nicht** p8.X, **nicht** hier referenziert als offen.
Quelle: `phase8_ui_graph/SESSIONS_ARCHIVE.md` Session-Block 2026-09-02.

**Phase 8 §9.4.1 A3** ist **erledigt, nicht p8.X**: die vierte A3-Probe lief am
2026-09-08 über den echten Connector ohne ID-Leck (P8.5-3/-4 ✅).

---

## §B Was NICHT in p8.X gehört (klare Außenkanten)

Verbotsliste für die Planungs-Session, damit p8.X nicht zur Wundertüte wird:

- Body-Volltextsuche in der Web-UI (Q1 gelockt seit P6)
- Rechteverwaltung über MCP-Tools (P6-M)
- Löschen von Items (F2)
- FastMCP-4/V79 (eigene Mini-Phase per P5-C)
- Funnel-Watchdog (P3-Erbposten, eigene Zeit)
- ~~Mobile/Realtime (nie angekündigt)~~ **[2026-09-09 Nikinger-Aufhebung, nur die
  Mobile-Hälfte]:** die Hochkant-/Handy-Ansicht ist ab sofort ein benanntes
  Zukunfts-Item (§10.9) — kein P8.6-Auftrag, aber in einer freieren Phasenplanung zu
  berücksichtigen. **Realtime bleibt draußen.**
- Light-Mode (Designsystem bleibt Dunkel-first, P5-X)
- Glyph-Entscheidungen P6/P6.5 (offene Nikinger-Entscheidungen, kein P8/p8.X-Auftrag)
- Bulk-Append-MCP-Tool (P6.5 bewusst draußen, geht heute schon mehrzeilig)
- Phase-8.5-Verbotsliste-Tabus (`storage/`, `authserver/`, `mcpserver/` außer dem
  Hint, `webui/{security,api,serializers,permissions}.py`) — die Tabus sind
  Phase-8.5-spezifisch, müssen für p8.X neu bewertet werden, **gelten aber
  vorerst weiter**, bis die Planungs-Session sie aufhebt. **§9 Variante (b)
  (`/var/log/sharefyx/feedback/`) und §9 Variante (c) (externer Endpunkt)
  würden diese Verbotsliste *bewusst* berühren — kein Default-Ausschluss,
  sondern explizite Planungs-Entscheidung.**

---

## §C Offene Fragen für die Planungs-Session (vermutlich Claude Code)

Wenn die Planungs-Session startet (vermutlich nach Phase 8.5 Z), sind diese
Fragen zu klären, **bevor** ein Plan-Doc entsteht:

1. **Reichweite.** Ist p8.X ein einziger Block („Polish") oder zerfällt es
   natürlich in mehrere Sub-Phasen (z. B. „Settings-Refactor" + „Layering" +
   „Edit-in-Place-Vision")?
2. **Reihenfolge.** Was sind Quick-Wins, was sind Big-Rocks? Vorschlag:
   §6 (Settings-Rename, 30 min) + §3 (Anzahl-Anzeige, 1–2 h) zuerst; §1
   (Layout) + §2.3+§2.4 (Map-Layout) als zweite Welle; §5 (Layering) +
   §7 (De-AI-ierung-Lauf 2) + §4 (Edit-in-Place) als dritte Welle, jede
   potenziell eigene Planung. **§8 (Tags) + §9 (Feedback-Button)** sind neue
   Kandidaten für die erste Welle, falls der Planungs-Session die Reihenfolge
   „klein vor groß" wichtiger ist als der ursprüngliche Vorschlag — beide
   sind UI-only ohne Server-Eingriff, §8 zudem strikt „only cosmetic".
3. **Aufwand-Schätzung.** Was ist in einer opencode/M3-Session machbar (≤1 Tag)?
   Was braucht Claude Code (mehrere Tage, Research)?
4. **Fabian-Koordination.** Fabi sammelt seit D4. Welcher Prozess — Fabi gibt
   in dieses Doc, Nikinger kuratiert, oder ein separates Tracker-Doc?
5. **Layering-Verifikation.** Bevor §5 umgesetzt wird: alle Selektoren
   in `app.css` + `js/dialogs.js` + `js/editor.js` listen, die `selected` /
   `aria-current` / `hover` matchen, und prüfen, welche versehentlich Glass-
   Farben verwenden. Output: ein `grep`-Fund-Report, kein Code-Touch.
6. **Phase-9-Tabu-Frage.** Übernehmen wir die Phase-8/8.5-Tabus für p8.X?
   `storage/` bleibt vermutlich tabu (keine neunte P1-Contract-Öffnung
   angekündigt), `authserver/` vermutlich auch. `webui/static/js/` ist seit
   P8.5-D4 explizit erlaubt (Bracket-Renderer-Fix als Präzedenz) — die
   Erlaubnis gilt weiter. **§8 (Tags) und §9 (Feedback-Button) brauchen
   wahrscheinlich beide einen neuen Server-Endpoint (oder eine neue
   Storage-Lokation für Feedback) — die Tabu-Frage ist hier *anders* zu
   beantworten als für den Rest:** bewusst früh in der Planungs-Session,
   nicht erst beim Bauen.
7. **§8-Tags — Palette-Format.** Eine kurze JSON-Schema-Skizze für
   `localStorage["sfx:tags:palette"]` reicht vermutlich — `{name: string,
   color?: string}` (CSS-Farbwert, optional). Wenn „blocked" ein fester
   Standard-Tag sein soll, ist die Frage: hartcodiert in der App-Initialisierung
   *zusätzlich* zur User-Palette, oder ausschließlich hartcodiert und nicht
   entfernbar?
8. **§9-Feedback — Server-Touch.** Variante (a) User-Space-Item braucht
   *keinen* neuen Endpoint (User nutzt `create_item` via bestehender
   REST-API, der Button löst einen POST aus). Variante (b)
   `/var/log/sharefyx/feedback/` braucht einen neuen Server-Write-Pfad in
   `webui/api.py` (Tabu-Frage). Variante (c) externer Endpunkt ist eine
   ganze Architektur-Frage (Phase-9-Tabu §0.4 verbietet aktuell ausgehende
   Server-Calls implizit über „der Server ist dumm"). Empfehlung in der
   Planungs-Session treffen.

---

## §D Namens- und Datei-Konvention für die Planungs-Session

Wenn aus diesen Notizen ein Plan wird:

- **Verzeichnis:** `phase9_ui_polish/` oder `phase8_x_ui_polish/` — Entscheidung
  der Planungs-Session. „p8.X" hier ist nur der vorläufige Arbeitstitel.
- **Plan-Doc:** `docs/concepts/phase9_ui_polish_plan.md` oder
  `docs/concepts/phase8_x_ui_polish_plan.md`.
- **Head-Doc:** `phase9_ui_polish/CLAUDE.md` oder analog.
- **Diese Notiz-Datei** bleibt als L3-Snapshot stehen (siehe Konvention:
  Plan-Snapshot bleibt unverändert); wird im INDEX-Hinweis als „Vorgänger der
  Phase-9-Planung" markiert, dann nicht mehr weitergepflegt.

---

## §E Erstes Auftauchen der einzelnen Punkte (chronologisch, Nikinger-Audit)

| Datum | Punkt | Herkunft |
|---|---|---|
| 2026-09-06 | D4-1 UX-2-Step-Knotenklick | Phase 8.5 D4-Block, §Drei echte Findings #3 |
| 2026-09-06 | D4-2 Map-Field schneidet ab | Phase 8.5 D4-Block, §Vier kleinere Punkte |
| 2026-09-06 | D4-3 Map-Reload-Drift | Phase 8.5 D4-Block, §Vier kleinere Punkte |
| 2026-09-06 | D4-4 Save-Button-YAML-Header | Phase 8.5 D4-Block, §Vier kleinere Punkte |
| 2026-09-06 | D4-5 Fabis Sammelliste | Phase 8.5 D4-Block, §Block 7 |
| 2026-09-06 | §1 Spaces-Layout-Reorganisation | Sichtprobe-Folgesession 2026-09-06 |
| 2026-09-06 | §2.1 Map-Performance-Reload | Sichtprobe-Folgesession 2026-09-06 |
| 2026-09-06 | §2.2 Map-Stil „Landkarte" | Sichtprobe-Folgesession 2026-09-06 |
| 2026-09-06 | §2.3 Map-Field schneidet ab | Sichtprobe-Folgesession 2026-09-06 (= D4-2) |
| 2026-09-06 | §2.4 Map-Reload-Drift | Sichtprobe-Folgesession 2026-09-06 (= D4-3) |
| 2026-09-06 | §2.5 Karte einklappen mit Abhängigkeiten | Sichtprobe-Folgesession 2026-09-06 |
| 2026-09-06 | §3 Anzahl-Anzeige Ordner | Sichtprobe-Folgesession 2026-09-06 |
| 2026-09-06 | §4 Edit-in-Place | Sichtprobe-Folgesession 2026-09-06 |
| 2026-09-06 | §5 Layering-Design-System | Sichtprobe-Folgesession 2026-09-06 |
| 2026-09-06 | §6 Settings/Navigation | Sichtprobe-Folgesession 2026-09-06 |
| 2026-09-06 | §7 De-AI-ierung Lauf 2 | Sichtprobe-Folgesession 2026-09-06 |
| 2026-09-08 | §6 re-affirmiert (Klarstellung der drei Vertausch-Lesarten a/b/c) | Phase-8.5-Sichtprüfungs-Folge-Sitzung 2026-09-08 |
| 2026-09-08 | §8.1 customizable Tags for tasks (kosmetisch) | Phase-8.5-Sichtprüfungs-Folge-Sitzung 2026-09-08 |
| 2026-09-08 | §8.2 Standard-Tag „blocked" | Phase-8.5-Sichtprüfungs-Folge-Sitzung 2026-09-08 |
| 2026-09-08 | §9 direkter User-Feedback-Button | Phase-8.5-Sichtprüfungs-Folge-Sitzung 2026-09-08 |
| 2026-09-09 | §10.1–§10.9 (neun Punkte: Icon-Radien, Hover, Ordner/Tags, klickbare Spaces, Einstellungsmenü, alles Klickbare, AI-Sessions, Hochkant-UI) | Phase-8.5-Closeout-Auftrag 2026-09-09 |

Die Sichtprobe-Folgesession vom 2026-09-06 und die Sichtprüfungs-Folge-Sitzung
vom 2026-09-08 sind beides Folge-Sessions nach dem Phase-8.5-D4-Lauf, aber
zeitlich getrennt — der Nikinger hat zwischen den beiden Tagen weitere Punkte
am echten Gerät gesammelt. Eine chronologische Trennung gibt es innerhalb
der beiden Tage nicht; die Punkte aus 2026-09-06 sind in einer Sitzung
aufgekommen, die drei Punkte aus 2026-09-08 in einer weiteren.
