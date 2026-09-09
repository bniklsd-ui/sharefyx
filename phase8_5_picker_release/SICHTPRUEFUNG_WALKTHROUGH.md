# Sichtprüfungs-Walkthrough — Schritt für Schritt am Bildschirm

> **Wofür diese Datei:** `SICHTPRUEFUNG_RESTBLOCK.md` (27 KB) ist die technische
> Referenz — Tabellen, Code-Anker, Edge-Cases. Diese Datei ist der **Freundliche
> Begleiter für deine Tastatur**: ein konkreter Was-tust-du / Was-siehst-du-Flow
> für jede Sichtprüfung, mit den genauen Klicks, Tasten und DevTools-Befehlen.
> Beide Dateien sind Geschwister — diese hier geht mit, die andere wird
> referenziert.
>
> **Wichtig (Sichtungs-Konvention 2026-09-09):** wenn eine Sichtung **klickbare Links**
> prüft (Link-Picker-Einfügen, Markdown-Rendering mit `[…](…)`, Body-Links), muss
> das **Vorschau-Panel im Screenshot sichtbar eingeblendet** sein. Die
> Edit-Ansicht allein reicht nicht — du liest sonst nur den Markdown-Quelltext und
> kannst nicht entscheiden, ob das Rendering funktioniert (Lehre aus Phase 8.5 D4
> Bracket-Bug 2026-09-06). Volle Konvention:
> [`docs/concepts/sichtpruefung_automation_conventions.md` §1](../docs/concepts/sichtpruefung_automation_conventions.md).
>
> **Voraussetzungen:**
> - Du bist an deiner gewohnten VM mit Browser und DevTools.
> - Die zwei Wegwerf-Instanzen laufen (200-Knoten auf Port 18772, D2 auf
>   18768) und die Production v3.0.1 ist unverändert (PID 355956).
> - Falls du die Login-Snippets aus der vorherigen Antwort verlegt hast: sie
>   stehen am Ende dieser Datei noch einmal.

---

## Vorbereitung — 3 Tabs, ein Connector, ein Snippet-Block

### Tab 1: Production v3.0.1 (deine echten Daten)

1. **Neuer Tab**, URL: deine gewohnte Tailscale-Funnel-URL (z. B.
   `https://<dein-name>-<space>.<tail-net>.ts.net/`).
2. **Einloggen** wie immer: Passwort + TOTP (deine normale Authenticator-App).
3. **DevTools öffnen** in diesem Tab: `F12` oder `Cmd+Opt+I`. Lass die Console
   offen — du wirst sie brauchen.

### Tab 2: 200-Knoten-Wegwerf (für Cluster 3-Rest: P8-21 d + P8-22)

4. **Neuer Inkognito-Tab** (oder normales Tab, egal — Cookies sind pro Origin
   getrennt), URL: `http://127.0.0.1:18772/ui/login`.
5. **Login-Daten** in einem separaten Terminal abrufen (das Snippet steht am Ende
   dieser Datei unter "Login-Snippet"). Es gibt dir 4 Zeilen: `space`, `password`,
   `totp_now`, `login_url`.
6. **Im Browser**: `space` (hier `alpha`) eintippen, `password` eintippen (oder
   copy-paste), `totp_now` eintippen — alle drei schnell hintereinander, der Code
   gilt 30 s.
7. **Erwartung**: du landest auf einer Übersicht mit **200 Knoten** als dichtes
   Netzwerk — blau (eigene alpha), türkis (geteilte beta), grau (fremde gamma).
8. **DevTools → Console-Tab** offen lassen für später.

### Tab 3: D2-Wegwerf (für Cluster 3-Rest: P8-24)

9. **Noch ein Tab**, URL: `http://127.0.0.1:18768/ui/login`.
10. **Login-Daten** mit dem zweiten Snippet-Block (D2-Variante) abrufen.
11. **Im Browser**: wie oben einloggen.
12. **Erwartung**: eine kleine Übersicht mit nur **14 Knoten** (10 alpha + 4 beta),
    viel übersichtlicher, gut zum Testen von Klick- und Hover-Verhalten.

### Connector-Session (für Cluster 4: P8.5-3 + P8.5-4)

13. **In claude.ai oder Claude Code** (mit deinem Custom-Connector auf die
    Production v3.0.1) eine neue Session öffnen — oder die bestehende reicht,
    falls du noch eine frei hast.

**Sichtprüfung-Reihenfolge (alles in einer Sitzung machbar):**

```
C4-0  P8-16   Glass-Fallback       ~30 s    Tab 1
C4-1  P8.5-19 Radiogruppe          ~30 s    Tab 1
C4-2  P8.5-3+4 Hint + 4. A3-Probe ~3 Min   Connector
C4-3  P8.5-17 V105 Connector      ~1 Min   Connector
C3-1  P8-21d  Tag-Cutoff > 15      ~1 Min   Tab 2
C3-2  P8-22   Settle/Interaktion   ~3 Min   Tab 2
C3-3  P8-24   E2E-Ritt             ~3 Min   Tab 3
C5-1  P8-5    (fällt mit C4-2 zusammen)         —
C5-2  P8-8    Zweitnutzer (mit Fabian) ~10 Min getrennt
```

**Gesamt: ~12 Min ohne Fabian, ~22 Min mit.**

---

## C4-0 · P8-16 — Glass-Fallback bei `prefers-reduced-transparency` (30 Sek)

**Was wird geprüft:** wenn dein System "weniger Transparenz" eingestellt hat
(oder du es im DevTools emulierst), soll die Oberfläche **solide** statt glasig
erscheinen, UND die Auswahl einer Notiz soll trotzdem klar erkennbar sein.

### Schritt für Schritt

1. **Tab 1** (Production), **Übersicht öffnen**.
2. **Schaue dir die Listen-Spalte an**: der Listenkopf oben hat einen leichten
   Glaseffekt (du siehst den Hintergrund leicht durchschimmern). **Das ist der
   Ausgangszustand.**

3. **DevTools öffnen** (F12) → Tab **"Rendering"** (nicht "Elements", nicht
   "Console"). Falls du den Rendering-Tab nicht siehst: auf die drei Punkte
   `⋮` oben rechts in den DevTools klicken → "Show Rendering" oder "More Tools
   → Rendering".

4. **Im Rendering-Tab nach unten scrollen** bis **"Emulate CSS media feature
   prefers-reduced-transparency"** — das ist eine Dropdown-Liste, die per
   Default auf **"no-preference"** steht.

5. **Auf "reduce" umstellen** (Dropdown → "reduce").

6. **Was du jetzt siehst** (alles in einem Wimpernschlag):
   - Der **Listenkopf** oben wird **solid dunkel** statt glasig — der leichte
     Schimmer ist weg, die Farbe ist jetzt ein flaches `rgb(27,32,39)`.
   - Die **Übersichts-Karten** rechts (ZULETZT-BENUTZT-Bereich) ebenfalls solid.
   - Das Detail-Paneel (falls geöffnet) ebenfalls solid.

7. **Klick auf irgendeine Notiz in der Liste**, sodass das Detail-Paneel sich
   öffnet und der Editor erscheint. **Prüfe**: ist die Auswahl (Listenzeile)
   **voll erkennbar**? Du solltest sehen:
   - Eine **Akzent-Füllung** (blauer Hintergrund auf der ausgewählten Zeile).
   - Eine **1-Pixel-Outline** (dünner blauer Rahmen).
   - Einen **3-Pixel-Akzent-Rand** links an der Zeile.
   - **Kein** Verschwimmen, kein Blur, alles gestochen scharf.

8. **Rendering-Tab zurück auf "no-preference"** stellen.

9. **Bestanden?** → ✅ notieren. Screenshot:
   `docs/screenshots/c4_p816_01_reduced_transparency_solid.png` (im reduced-Modus).

### DevTools-Befehl (optional, schneller als der Rendering-Tab-Weg)

Wenn du den Rendering-Tab nicht findest, geht auch dieser Console-Befehl:

```js
// Im Console-Tab von Tab 1:
document.documentElement.style.setProperty('color-scheme', 'light dark');
// oder einfacher:
window.matchMedia('(prefers-reduced-transparency: reduce)').matches
// → liefert "false". Für echten Wechsel brauchst du den Rendering-Tab.
```

Für die Sichtprüfung **musst du den visuellen Wechsel sehen** — die Console
hilft nur als Cross-Check, nicht als Ersatz.

### Was bei "knapp bestanden" zählt

- ✅ = Glas verschwindet komplett, Auswahl klar erkennbar, kein Blur-Effekt mehr.
- 🟡 = Glas verschwindet, aber Auswahl wirkt zu blass (z. B. Outline zu dünn).
- ❌ = Glas bleibt sichtbar trotz "reduce", oder Auswahl nicht mehr erkennbar.

---

## C4-1 · P8.5-19 — Radiogruppe statt Dropdown (30 Sek)

**Was wird geprüft:** der Link-Picker (Lupensymbol im Item-Editor) hat zwei
Modi — "als Text einfügen" und "als Kante" — und die **Bauform** muss eine
**Radiogruppe** sein (beide Optionen direkt sichtbar), kein verstecktes
Dropdown.

### Schritt für Schritt

1. **Tab 1** (Production), **beliebiges Item** im Editor öffnen (Doppelklick auf
   eine Notiz in der Liste, oder einfach eine Notiz anklicken und "Bearbeiten"
   wählen).

2. **Im Editor** das Lupensymbol 🔍 suchen — es steht in der Kopfdaten-Leiste
   oben neben "Links" (das ist das Feld, in dem deine Frontmatter-Verknüpfungen
   stehen). Das Lupensymbol öffnet den Link-Picker-Dialog.

3. **Klick auf die Lupe**. Es öffnet sich ein **Overlay-Dialog** mit einem
   Suchfeld oben.

4. **Was du sehen sollst:**
   - Ein **Suchfeld** ("Titel oder itm_…" als Platzhalter).
   - **Darunter**: **zwei Radio-Buttons** (kleine runde Knöpfe, keine
     Dropdown-Pfeile). Sie sollten Labels haben wie "als Text-Link" und "als
     Kante" — die genauen Wörter können leicht abweichen, aber es sind genau
     **zwei** Optionen.
   - **Einer davon ist markiert** (blauer Kreis mit Punkt innen) — das ist der
     aktive Modus. Falls du den Picker zum ersten Mal in dieser Session
     öffnest, ist es typischerweise der Standard ("body" = als Text-Link).

5. **Klick auf den anderen Radio** (z. B. den "als Kante"-Knopf).

6. **Was passieren soll:**
   - Der zuvor markierte Kreis ist jetzt leer, der neue ist markiert.
   - Wenn du den Dialog schließt und wieder öffnest, ist die **Auswahl
     erhalten geblieben** (das ist die `localStorage`-Persistenz, die wir
     committet haben — Modus überlebt Tab-Schließen).

7. **Optional Console-Check** in Tab 1:
   ```js
   localStorage.getItem('sfx:linkpicker:mode')
   ```
   → liefert `"body"` oder `"frontmatter"`. Wenn du den Modus gerade gewechselt
   hast, sollte der letzte Wert hier stehen.

8. **Bestanden?** → ✅ notieren. Screenshot:
   `docs/screenshots/c4_p8519_01_radiogruppe_im_dialog.png`.

### Was bei "knapp bestanden" zählt

- ✅ = Zwei Radios sichtbar, beide beschriftet, einer markiert, Auswahl persistent.
- 🟡 = Radios sichtbar, aber Modus wird beim Schließen nicht gespeichert.
- ❌ = Es ist ein `<select>`-Dropdown (Klick öffnet ein Auswahlmenü) — dann
  ist das Pre-Z-Tausch-Commit vom 2026-09-07 nicht aktiv (würde auf einen
  Fehler im Live-Deploy hindeuten).

---

## C4-2 · P8.5-3 + P8.5-4 — Hint-Generalisierung + Vierte A3-Probe (~3 Min)

**Was wird geprüft:** Claude (in deinem Connector) soll in **vier** Textformen
Notizen mit dem **Titel** nennen, nicht mit der `itm_…`-ID. Die vier Formen:
Fließtext, Tabelle, Klammer-Kontext, Aufzählung. Wenn eine **fünfte** Form
auftaucht, in der die ID durchrutscht, ist die Abbruchregel §9.4.1 erfüllt
(Plan §3 B1 wörtlich: "wird §9.4.1 als Modellverhalten dokumentiert und
geschlossen", kein Code-Fix).

### Schritt für Schritt

1. **Connector-Session** öffnen (claude.ai mit Custom-Connector auf die
   Production-URL, oder Claude Code mit MCP-Setup auf die URL).

2. **Erste Suche**: im Connector-Prompt schreiben:
   ```
   Liste mir alle Notizen, die "Auth" im Titel haben. Gib sie in vier Formen aus:
   (a) als Fließtext mit Titel,
   (b) als Tabelle mit Spalte "Titel",
   (c) in Klammern hinter dem Titel: (Titel),
   (d) als Aufzählung mit Titel als Bullet.
   ```
   (Den genauen Suchbegriff anpassen — was es bei dir gibt. "Auth" ist ein
   Beispiel; nimm was du in deiner Sammlung findest.)

3. **Was du erwarten solltest:**
   - In **jeder** der vier Formen taucht der **vollständige Titel** auf.
   - **Niemals** steht da `itm_de30c6c9` oder ähnliches — immer "Notiz zum
     Auth-Service refactoren" oder wie auch immer dein Titel heißt.

4. **Zweite Suche** (anderes Item, zur Sicherheit):
   ```
   Suche nach Notizen mit dem Tag "Projekte" und liste sie nochmal in den
   gleichen vier Formen.
   ```

5. **Bestanden?** → ✅ notieren mit Notiz "vier Formen gehalten" — die Zeile
   P8.5-3 in der Abnahmematrix wandert auf ✅.

6. **ODER — falls eine ID durchrutscht** in einer der vier (oder einer
   bisher nicht getesteten **fünften**) Form:
   - Genau aufschreiben, **welche Form** es war (für die Z-Doku).
   - **Bestanden?** trotzdem als "🟡 mit Befund" markieren.
   - Der Phase-8.5-Z-Closeout wird das als "Modellverhalten dokumentiert"
     abschließen, **nicht** durch einen weiteren Hint-Edit reparieren.

7. **Bestanden oder Befund?** → notieren. Screenshot:
   `docs/screenshots/c4_p853_01_hint_vier_formen.png` (Connector-Screenshot
   mit deiner Antwort).

### Tipp: wie du alle vier Formen erzwingst

Wenn dein Connector-Claude "zu schlau" ist und alle vier Varianten in einem
vereint, hilft es, jede Form in eine separate Anfrage zu packen:

```
"Liste Notizen mit Tag 'Projekte' — NUR als Fließtext mit Titel, eins pro Zeile."

"Liste Notizen mit Tag 'Projekte' — NUR als Markdown-Tabelle."

"Liste Notizen mit Tag 'Projekte' — NUR als Aufzählung, Titel als Bullet."

"Liste Notizen mit Tag 'Projekte' — NUR als Klammerliste: (Titel) pro Zeile."
```

Vier Anfragen, eine Form pro Antwort, eindeutige Beobachtung.

---

## C4-3 · P8.5-17 — Connector-Check V105 (~1 Min)

**Was wird geprüft:** der echte Anthropic-Connector (oder dein Claude-Code-
MCP) verbindet sich nach dem v3.0.1-Deploy weiterhin mit der laufenden
Instanz. Es geht um genau **diesen** Verbindungspfad — nicht um den Browser.

### Schritt für Schritt

1. **Connector-Übersicht** (je nach Client) aufrufen:
   - **claude.ai**: Settings → Connectors → "sharefyx" sollte "Connected" /
     grün sein, mit einem letzten Auth-Datum.
   - **Claude Code**: MCP-Settings oder `claude mcp list` im Terminal — der
     `sharefyx`-Eintrag sollte Status "connected" zeigen.

2. **Eine echte Tool-Anfrage** absetzen, im Connector-Prompt:
   ```
   Was sind die Spaces, auf die ich Zugriff habe?
   ```
   (Wenn der Connector `list_spaces` anbietet — die meisten Custom-Connectors
   bieten das.)

3. **Was du erwarten solltest:**
   - Eine **grüne Antwort** mit den Spaces (z. B. `niklas`, `fabian`,
     `IT-Sekus-Projekt`, je nach Mitgliedschaft).
   - **Kein** roter Fehler, kein "tool not found", kein "auth failed".

4. **Optional, zweite Probe:**
   ```
   Suche nach Notizen mit "Test" im Titel.
   ```
   Sollte wieder grüne Antwort liefern, möglicherweise mit oder ohne Treffern.

5. **Bestanden?** → ✅ notieren. Falls der Connector einen Spec-Drift zeigt
   (rote Fehlermeldung, "tool nicht erkannt", "auth expired"): 🟡 mit
   genauer Fehlermeldung im Notizen-Feld, weil das dann Z-Stoff ist.

6. Screenshot: `docs/screenshots/c4_p8517_01_connector_verbunden.png`.

---

## C3-1 · P8-21 d — Tag-Cutoff bei >15 Knoten (1 Min)

**Was wird geprüft:** wenn ein Tag **mehr als 15 Knoten** hätte, soll der
Graph **keine** Tag-Kanten für diesen Tag zeichnen (sonst werden es zu viele
Linien und die Übersicht wird unleserlich). Wir testen das gegen den
200-Knoten-Datensatz, wo das Tag `last-200` auf **allen 200** Knoten liegt
— das **muss** vom Cutoff ausgeschlossen sein. Das Tag `spitze` liegt auf
genau 5 Knoten — das **muss** durchkommen.

### Schritt für Schritt

1. **Tab 2** (200-Knoten-Wegwerf), Übersicht mit dem Graph.

2. **Erst ohne Toggle**: der Graph zeigt nur die expliziten Ring-Kanten
   (solide Linien zwischen aufeinanderfolgenden Knoten im Ring).

3. **Toolbar-Toggle "Tags"** suchen — in der Toolbar oberhalb des Graph-Panels
   steht eine Checkbox "Tags" (oder ein ähnlicher Knopf). **Klick darauf**.

4. **Was du sehen solltest:**
   - **Zusätzliche gestrichelte Linien** erscheinen (Tag-Kanten sind gestrichelt).
   - Die **Anzahl** ist überschaubar — du siehst nicht plötzlich 19 900
     Linien.
   - Es gibt **gestrichelte Kanten für `spitze`** (Tag liegt auf 5 Knoten, also
     10 Verbindungen = 10 Linien).
   - Es gibt **keine** gestrichelten Kanten für `last-200` (das wären 19 900,
     und die Cutoff-Regel unterdrückt sie).
   - Es gibt **keine** gestrichelten Kanten für `gruppe-00` bis `gruppe-11`
     (12 Gruppen à ca. 16-17 Knoten, alle über dem Limit).

5. **Console-Cross-Check** (Tab 2 Console-Tab):
   ```js
   await fetch('/api/v1/graph').then(r => r.json()).then(g => 
     g.edges.filter(e => e.kind === 'tag').length
   )
   ```
   → liefert die **Anzahl Tag-Kanten im Payload**. Sollte im niedrigen
   dreistelligen Bereich sein (≈ 10 von `spitze`), **nicht** 19 900.

6. **Toggle nochmal anklicken** → aus. **Toggle wieder an**. Toggle ist symmetrisch.

7. **Bestanden?** → ✅ notieren. Screenshot:
   `docs/screenshots/c3rest_p821d_01_200knoten_tag_clique_limit.png`.

### Was bei "knapp bestanden" zählt

- ✅ = Tag-Cutoff greift, sichtbar **viel weniger** Kanten als 19 900, kein
  Performance-Hänger.
- 🟡 = Cutoff greift, aber du siehst Kanten für ein Tag, das eigentlich
  ausgeschlossen sein sollte (z. B. ein `gruppe-XX`-Tag mit 16 Knoten, das
  durchrutscht).
- ❌ = Cutoff greift nicht — du siehst alle 19 900 Kanten und der Browser
  hängt.

---

## C3-2 · P8-22 — Settle-Zeit, Hakelfreiheit, Reduced-Motion (3 Min)

**Was wird geprüft:** der 200-Knoten-Graph soll sich **schnell beruhigen** (unter
3 Sekunden), Interaktion (Hover/Drag/Zoom/Pan) soll **ohne Ruckler** laufen, und
im `prefers-reduced-motion`-Modus soll der Graph **statisch** rendern (keine
Animation).

### Schritt für Schritt — P8-22a (Settle-Zeit)

1. **Tab 2**, **Übersicht** öffnen — der Graph startet die Animation.

2. **Stoppuhr** (z. B. Handy oder Browser-Extension) **starten, sobald der erste
   sichtbare Frame kommt** — nicht beim Klick auf "Übersicht", sondern wenn
   sich der erste Knoten sichtbar bewegt.

3. **Beobachten**: Knoten pendeln kurz aus, werden langsamer, bleiben stehen.

4. **Stoppuhr stoppen**, wenn die Bewegung **subjektiv** aufgehört hat (kein
   erkennbares Zittern mehr). **Budget: < 3 Sekunden**. Wir erwarten ca. **2.5 bis
   2.7 Sekunden** im Live-Browser (Throwaway-Smoke maß 2.69 s).

5. **Notiere** die gemessene Zeit (z. B. "2.6 s") in der
   Ergebnis-Tabelle.

### Schritt für Schritt — P8-22b (Interaktion ohne Hakeln)

6. **Hover** mit der Maus über **mehrere Knoten** (5–10 verschiedene). Jede
   Bewegung der Maus sollte **sofortige Reaktion** zeigen — der Knoten unter
   dem Cursor wird hervorgehoben, Nicht-Nachbarn werden leicht grau
   (gedimmt). Wenn du 60 fps gewohnt bist, sollte nichts ruckeln.

7. **Drag**: klicke und halte einen Knoten, ziehe ihn um ca. 50 Pixel, lass
   los. Der Knoten sollte **der Maus folgen**. Beim Loslassen sollte **kein
   Detail-Paneel** aufgehen — das ist die Klick-vs-Drag-Heuristik, die wir
   am 2026-09-02 gefixt haben.

8. **Zoom mit Mausrad**: 10 Stufen nach oben (über dem Canvas), 10 Stufen
   nach unten. Jede Stufe greift. Zoom-Readout in der Toolbar (z. B. "1.5×")
   ändert sich pro Stufe.

9. **Pan**: klicke auf eine **leere** Stelle im Canvas (nicht auf einen
   Knoten), halte gedrückt, ziehe. Der ganze Graph verschiebt sich.

10. **Bestanden?** → ✅ notieren, falls subjektiv kein Hakeln.

### Schritt für Schritt — P8-22c (Reduced-Motion)

11. **DevTools → Rendering-Tab** (wie bei C4-0). **"Emulate CSS media feature
    prefers-reduced-motion"** auf **"reduce"** stellen.

12. **Übersicht neu laden** (F5). Der Graph wird **direkt statisch** gerendert
    — du siehst **keine** Animation, die Knoten sind sofort an ihrer
    End-Position.

13. **Console-Cross-Check** in Tab 2:
    ```js
    await fetch('/api/v1/graph').then(r => r.json()).then(g => g.nodes.length)
    ```
    → liefert **200** (das Datenset ist da, nur die Animation ist aus).

14. **Rendering-Tab zurück auf "no-preference"** stellen, **neu laden** (F5).
    Graph startet wieder normal mit Animation.

15. **Bestanden?** → ✅ notieren. Drei Screenshots:
    - `c3rest_p822a_01_settled.png` (nach Settle in P8-22a)
    - `c3rest_p822b_01_interaktion_ohne_hakeln.png` (nach den 10 Zoom-Stufen)
    - `c3rest_p822c_01_reduced_motion_static.png` (statische Wiedergabe)

### Was bei "knapp bestanden" zählt

- ✅ a: Stoppuhr < 3 s, subjektiv keine Bewegung mehr.
- ✅ b: Hover/Drag/Zoom/Pan flüssig, kein Aufhänger.
- ✅ c: Reduced-Motion rendert statisch, Datenset komplett.
- 🟡 wenn **eines** davon wackelt (z. B. Settle dauert 3.5 s oder Zoom
  hängt alle 4-5 Stufen).

---

## C3-3 · P8-24 — Kombinierter E2E-Ritt gegen D2-Wegwerf (3 Min)

**Was wird geprüft:** ein durchgehender Ritt durch die App — Login, Übersicht
mit Graph, globaler Scope, Knoten-Hover, Knoten-Klick öffnet das Item.
**Wir nehmen den D2-Datensatz (14 Knoten)**, nicht den 200-Knoten-Datensatz,
weil Station 3 dort mit `DEFAULT_LIMIT=50` driftet.

### Schritt für Schritt

1. **Tab 3** (D2-Wegwerf), **Übersicht** ist schon offen.

#### Station 2 — Übersicht

2. **Schaue die Übersicht an**: tabellose Space-Zeilen mit Counter-Chips
   (alpha hat z. B. 4 Notizen + 3 Aufgaben + 2 Archiv, beta hat 2 Notizen + 1
   Aufgabe + 1 Archiv). Rechts oben Mini-Legende (● Eigener Space blau,
   ● Geteilter Space türkis). Graph-Panel mit Knoten + Kanten.

3. **Bestanden?** wenn die tabellose Übersicht da ist und die Legende sichtbar.

#### Station 3 — Globaler Scope

4. **Klick auf den Home-Knopf** in der Rail (links, oben, sieht aus wie ein
   Haus-Symbol, oder wie der Name deines Home-Spaces). Die Listen-Spalte
   zeigt jetzt **"Alle Items"** als Header, mit Items aus **allen** Spaces
   gemischt.

5. **Notiere die Zeilenzahl** (z. B. 9 Items sichtbar).

6. **Erneuter Klick auf Home**. Die Zeilenzahl bleibt **identisch** zur
   ersten Lesung. Das ist die Idempotenz.

7. **Bestanden?** wenn die zweite Lesung exakt dieselbe Zahl zeigt.

#### Station 4 — Graph rendert

8. **DevTools → Network-Tab** (oder Console-Tab mit Cross-Check). Suche den
   Request `GET /api/v1/graph` (im Network-Tab nach "graph" filtern). Klick
   drauf → Response.

9. **Was du sehen solltest:**
   - **14 Knoten** (10 alpha + 4 beta, oder vergleichbar — `nodes.length`).
   - **6 Kanten** (Frontmatter + Body-Links, gemischt).

10. **Bestanden?** wenn das Payload stimmt.

#### Station 5 — Hover dimmt

11. **Maus auf einen blauen Knoten** (eigener alpha-Knoten).

12. **Was passieren soll:**
    - Der Knoten unter dem Cursor bleibt voll deckend.
    - **Andere Knoten** werden leicht grau (gedimmt, ~15 % Alpha).
    - Wenn du den Cursor wegbewegst, kehren alle zur vollen Deckkraft zurück.

13. **Bestanden?** wenn der Hover-Effekt funktioniert.

#### Station 6 — Knoten-Klick öffnet das Item

14. **Einfacher Klick** auf einen **blauen** Knoten (eigenes alpha-Item):
    **Klick → loslassen** (kein Ziehen, sonst gilt es als Drag).

15. **Was passieren soll:**
    - Die Übersicht verschwindet.
    - Das **Detail-Paneel** rechts zeigt den **Editor** (`#detail-editor`).
    - Der Titel des Items steht oben im Editor.
    - Der Body ist in der Textarea sichtbar.

16. **ESC drücken** → zurück zur Übersicht.

17. **Klick auf einen türkisen Knoten** (beta-Item): **Klick → loslassen**.

18. **Was passieren soll:**
    - Das Detail-Paneel zeigt die **Nur-lesen-Ansicht** (`#detail-readonly`).
    - **Kein** Edit-Button sichtbar (du kannst nicht schreiben, weil es nicht
      dein Space ist).
    - Der Titel steht oben.

19. **ESC drücken** → zurück zur Übersicht.

20. **Bestanden?** wenn beide Pfade (Editor und Readonly) korrekt öffnen.

### Vier Screenshots

- `c3rest_p824_01_uebersicht.png` (Station 2)
- `c3rest_p824_02_alle_items_scope.png` (Station 3)
- `c3rest_p824_03_graph_hover.png` (Station 5)
- `c3rest_p824_04_knoten_geoeffnet.png` (Station 6)

### Was bei "knapp bestanden" zählt

- ✅ alle 6 Stationen, 4 Screenshots, kein Fehler.
- 🟡 wenn **eine** Station wackelt (z. B. ESC bringt nicht zurück zur
  Übersicht, oder Klick auf einen fremden Knoten öffnet den Editor statt
  Readonly).

---

## C5-1 · P8-5 — Drittprobe (= Vierte A3-Probe aus C4-2)

Diese Zeile **fällt mit C4-2 zusammen**. Wenn dort der Hint in allen vier
(vier oder fünf) Formen hält, ist P8-5 gleichzeitig erledigt. Kein
zusätzlicher Aufwand.

Falls du sie explizit separat protokollieren willst:

| Schritt | Aktion |
|---|---|
| 1 | Connector-Session, `search_items` auf mehrere bekannte Items |
| 2 | Antwort lesen — Titel in jeder Form, **keine** `itm_…`-ID |

**Bestanden?** ✅ notieren in der Cluster-5-Tabelle.

---

## C5-2 · P8-8 — Zweitnutzer-Pass-Through (mit Fabian)

**Diese Zeile braucht einen zweiten Menschen.** Du kannst sie nicht alleine
heute abnehmen.

### Was zu tun ist (mit Fabian)

1. **Termin mit Fabian** für eine zweite Sitzung (~10 Min).

2. **Beide Nutzer einloggen** — du als `niklas`, Fabian als `fabian`. Falls
   Fabian kein aktiver Connector-Login hat, kann er das vorher einrichten
   (sein Token ist seit Phase 5 live; Connector-Doku in `docs/concepts/
   phase5_ui_plan.md` §3).

3. **Im Production-Connector (Nikinger)**: `search_items` auf ein Item, das
   nur in `niklas` existiert (also keine `share_read`-Markierung). Die Antwort
   enthält das Item.

4. **Im Production-Connector (Fabian)**: dieselbe Suche. Das **private**
   `niklas`-Item darf **nicht** in Fabians Antwort auftauchen.

5. **Im Production-Connector (Nikinger)**: `get_item` auf ein Item mit
   `share_read: ["fabian"]`. Antwort enthält Body.

6. **Im Production-Connector (Fabian)**: dasselbe `get_item`. Antwort enthält
   Body, **readonly: true** (Fabian darf lesen, aber nicht schreiben).

7. **Im Production-Connector (Fabian)**: `update_item` auf dasselbe
   `share_read`-Item. Sollte **403 oder 404** liefern.

8. **Bestanden?** ✅ wenn alle fünf Punkte halten.

### Alternative (ohne Fabians Termin)

Falls Fabian kurzfristig nicht verfügbar ist: **verschiebe** P8-8 in eine
eigene Fabian-Sitzung (Hard Rule 4 verbietet Cross-Space-Tests mit nur
einem Token). Markiere als 🟡 mit Notiz "Fabian-Slot nötig" und mach
weiter mit Z.

---

## Ergebnis-Tabelle (am Ende der Sichtprüfung ausfüllen)

| # | Kriterium | Sub-Punkte | Bestanden? | Notizen |
|---|---|---|---|---|
| **C4-0** | P8-16 Glass-Fallback | reduced + Auswahl | ⬜ | |
| **C4-1** | P8.5-19 Radiogruppe | 2 Radio + persistent | ⬜ | |
| **C4-2** | P8.5-3 + P8.5-4 Hint | 4 Formen | ⬜ | Welche 4? Gibt es eine 5.? |
| **C4-3** | P8.5-17 V105 | Connector grün | ⬜ | |
| **C3-1** | P8-21d Tag-Cutoff | spitze ja, last-200 nein | ⬜ | Console-Cross-Check-Zahl: ___ |
| **C3-2a** | P8-22a Settle | < 3 s | ⬜ | Stoppuhr: ___ s |
| **C3-2b** | P8-22b Interaktion | hover/drag/zoom/pan | ⬜ | |
| **C3-2c** | P8-22c Reduced-Motion | statisch | ⬜ | |
| **C3-3** | P8-24 E2E-Ritt (D2) | 6 Stationen | ⬜ | |
| **C5-1** | P8-5 (= C4-2) | (= C4-2) | ⬜ | |
| **C5-2** | P8-8 Zweitnutzer | mit Fabian | ⬜ | |

**Wenn alles ✅ (außer P8-8 mit Fabian):** Phase-8-Bilanz **20 ✅ · 6 🟡 →
24 ✅ · 2 🟡** (P8-5, P8-16, P8-21d, P8-22, P8-24 wandern auf ✅; P8-5 ist neu,
weil bisher noch 🟡). **Cluster 3 komplett abgeschlossen + Cluster 4
abgeschlossen + P8-5 erledigt.** Nur noch P8-8 wartet auf Fabian.

**Wenn etwas 🟡 bleibt:** jeden Fail als benannten Restdefekt notieren —
nicht stillschweigend überspringen.

---

## Was passiert nach dem Lauf (Hard Rule 8, der nächste Commit)

Pro Sichtprüfungs-Sitzung (oder als ein Commit, wenn alles in einer
Sitzung ablief):

1. **Screenshots** ablegen unter `docs/screenshots/c4_*.png` /
   `c3rest_*.png` (Namen stehen bei jedem Punkt oben).

2. **`phase8_ui_graph/CLAUDE.md` §7-Matrix** updaten — die abgehakten Zeilen
   wandern von 🟡 auf ✅ mit Belegs-Spalte ("Nikinger-Sichtprüfung
   2026-09-XX live gegen v3.0.1: ..."). Für die noch nicht erledigten
   Punkte bleibt 🟡.

3. **`phase8_ui_graph/CLAUDE.md` Modul-Status Block D** und
   **Bilanz-Abschnitt** updaten. awk-Kommando aus dem Phase-Head-Bilanz-
   Abschnitt erneut laufen lassen, ergibt den neuen `Zeilen=26 ✅=XX 🟡=YY
   ⬜=ZZ`-Wert.

4. **`phase8_5_picker_release/CLAUDE.md` Modul-Status** und
   **Abnahmestand-Tabelle** P8.5-3 / P8.5-4 / P8.5-17 / P8.5-19 auf den
   neuen Stand. Bilanz-Zeile nachziehen.

5. **`docs/INDEX.md`** Phase-8-Header + Phase-8.5-Header um die neue
   Sub-Session ergänzen, `updated:` vorne im Frontmatter nachziehen.

6. **Commit-Message** (ein Sub-Session-Commit reicht):
   ```
   phase 8/8.5: Sichtprüfung am echten v3.0.1 + 200-Knoten + D2 -- C4-0/1/2/3 + C3-1/2/3 + C5-1 ✅
   ```

7. **Cleanup** der Wegwerf-Instanzen (Hard Rule 9, PID-Datei-basiert):
   ```bash
   .venv/bin/python phase8_ui_graph/scripts/wegwerf_setup_d2.py cleanup
   .venv/bin/python phase8_ui_graph/scripts/wegwerf_setup_200knoten.py cleanup
   ```
   **Niemals** `pkill -f`.

8. **Dannach: Z** (Phase-8.5-Closeout) — der hebt die Phase-8-✅-Entscheidung
   auf ✅ und schließt Phase 8 + 8.5 formal mit ab.

---

## Login-Snippet (falls verlegt)

Beide Snippets laufen am Session-Anfang einmal, geben dir die aktuellen
Login-Daten für die jeweilige Wegwerf-Instanz.

### 200-Knoten-Wegwerf (Port 18772)

```bash
.venv/bin/python -c '
import json, sys, time
from urllib.parse import urlparse, parse_qs
sys.path.insert(0, ".")
from authserver.totp import totp_at
creds = json.loads(open("/tmp/opencode/sharefyx-wegwerf-200knoten/credentials.json").read())
secret = parse_qs(urlparse(creds["otpauth_uri"]).query)["secret"][0]
print(f"  space:     {creds[\"space\"]}")
print(f"  password:  {creds[\"password\"]}")
print(f"  totp_now:  {totp_at(secret, int(time.time()) // 30)}")
print(f"  login_url: http://127.0.0.1:18772/ui/login")
'
```

### D2-Wegwerf (Port 18768)

```bash
.venv/bin/python -c '
import json, sys, time
from urllib.parse import urlparse, parse_qs
sys.path.insert(0, ".")
from authserver.totp import totp_at
creds = json.loads(open("/tmp/opencode/sharefyx-wegwerf-d2/credentials.json").read())
secret = parse_qs(urlparse(creds["otpauth_uri"]).query)["secret"][0]
print(f"  space:     {creds[\"space\"]}")
print(f"  password:  {creds[\"password\"]}")
print(f"  totp_now:  {totp_at(secret, int(time.time()) // 30)}")
print(f"  login_url: http://127.0.0.1:18768/ui/login")
'
```

Aktueller Stand (würfelt pro Setup neu):

```
200-Knoten (Port 18772)   alpha / wegwerf-200k-SkuZiBeEoqw
D2          (Port 18768)   alpha / wegwerf-d2-d3atnRRo79k
```

**TOTP-Secrets zum einmaligen Scan in eine Authenticator-App** (statt jeden
Lauf das Snippet zu bemühen):
- 200-Knoten: `7ABD6SI6OVJ6TWMW4IMVJOOOMHKX4TSM` (Base32, issuer `sharefyx`)
- D2: `Z5V3ZP2P3ZGDHOCLWGVLW5HPI5Y3LAOI` (Base32, issuer `sharefyx`)

---

## Größen-Hinweis

- `phase8_5_picker_release/SICHTPRUEFUNG_WALKTHROUGH.md` (diese Datei): ~16 KB
  neu (separate Datei, kein Softcap-Risiko).
- `phase8_5_picker_release/SICHTPRUEFUNG_RESTBLOCK.md` (technische Referenz):
  27.5 KB unverändert.
- `phase8_5_picker_release/CLAUDE.md`: ~70 KB nach diesem Sub-Session (Head
  rotiert mit neuem Block, Auflösung des 40-KB-Softcaps bleibt Z-Arbeit).
- `docs/INDEX.md`: ~64 KB (+1 Zeile).
