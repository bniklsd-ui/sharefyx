---
status: snapshot
purpose: Mini-Plan Revision 1 zu Block G — vier Fixes aus der Nikinger-Sichtung der Block-G-Screenshots (Breakpoints 1200/1024, Layer-Ton, Editor-Head sticky)
read-when: Herkunft von Block G-R nachvollziehen — was die Sichtung fand und wie es behoben wurde
detail: L2
up: ../../phase8_6_ui_polish/CLAUDE.md
down:
  - ./phase8_6_ui_polish_plan2.md   # der übergeordnete Plan, dem G-R folgt
updated: 2026-09-14 (Mini-Plan geschrieben, Block G-R gebaut und abgenommen — Datei bleibt seither unverändert)
---

# Phase 8.6 — Block G-R (Revision nach Sichtung)

> **Block G-R — Datum 2026-09-14, opencode/M3.** Eigener Commit, kein Force-Push auf `081c432`
> (Nikinger-Entscheidung 2026-09-14: "Nein, bitte als G-R anhängen" — heißt: G-R ist ein
> eigener Block mit eigenem Commit, kein Patch auf Block G). Vier zusammenhängende Fixes aus
> der Sichtung der sechs Block-G-Screenshots `p86_block_g_{01..06}_*.png`.

---

## Auslöser

Nikinger-Sichtung der sechs Selbst-Screenshots aus Block G am 2026-09-14. Sechs Rückmeldungen,
gruppiert zu vier Fixes — Befund 9b lebt noch, der Map-Leerraum oben/unten ist neu, die
Layer-Töne driften weiter, und die Breakpoints passen nicht zur Designabsicht.

| Screenshot | Befund | Fix hier |
|---|---|---|
| 01, 02, 04 | Karte füllt `.detail`-Slot oben/unten nicht — `.detail__graph` hat 32-px-Rundum-Padding, der als schwarzer Leerraum sichtbar wird (Detail-Slot erbt `--bg-void` vom Body, Liste nutzt `--bg` → drei Töne für "Spalten-Hintergrund": `--bg`, `--bg-void`, `--surface`) | G-R.2 + G-R.4 |
| 03, 04 | Editor-YAML-Kopfzeile sitzt unter einer eigenen `.editor__head`-Leiste, die **nicht** sticky ist und nicht das Gewicht der `.list__head` trägt — visuell versetzt gegenüber Item-Zeilen | G-R.3 |
| 05 | Bei 1200 px ist die Rail auf 64 px kollabiert (Icons only, alle Texte weg), obwohl die Nikinger-Vorgabe war "Navigationspalte bleibt gleich" | G-R.1 |
| 06 | Bei 1024 px wird die Karte entfernt statt gestapelt — die Nikinger-Vorgabe war "Übersicht zusammenschieben und 'nav bar' weiterhin vollständig zeigen" | G-R.1 |
| 03, 04 (Wiederholung) | "Immer noch viele verschiedene Grau töne für gleiche layer" — F-Wächter fängt nur rohe Hex und warn-Tönung, nicht die Token-Drift innerhalb eines Layers | G-R.4 |

**Reihenfolge der Umsetzung:** G-R.1 → G-R.2 → G-R.3 → G-R.4 (Wächter zuletzt, sonst meldet er
während der Bauphasen Fehler die gerade entstehen — gleiche Regel wie Plan 2 §6.5).

---

## G-R.1 — Breakpoints (Nikinger-Vorgabe: Nav bleibt 240)

### Vorher (Block G Stand)

```css
/* app.css:1900 */
@media (max-width: 1280px) {
  .shell { grid-template-columns: 64px 480px 1fr; }
  .rail__label, .rail__brand, .tree__group, .tree__count, .tree__badge { display: none; }
  .rail__home, .rail__action { justify-content: center; }
  .tree__folder { padding-left: var(--space); }
  .rail__account { flex-direction: column; }
}

/* app.css:1912 */
@media (max-width: 1024px) {
  .shell { grid-template-columns: 64px 1fr; }
  .shell[data-view="list"] .detail { display: none; }
  .shell[data-view="detail"] .list { display: none; }
  .shell[data-view="detail"] .detail__back { display: block; }
}
```

Nikinger-Beobachtung live: bei 1200 px ist die Rail auf 64 px geschrumpft — "Navigationszeile
kracht zusammen". Bei 1024 px ist die Karte weg — die dritte Spalte wird ganz ausgeblendet.

### Nachher

```css
/* ≤ 1200 px: Rail bleibt 240, Liste schrumpft auf 380, Karte füllt 1fr. Keine Rail-Kollaps --
   die Texte sind bei 380 px Listenbreite noch lesbar (Item-Titel 16px + Meta 12.5px passen). */
@media (max-width: 1200px) {
  .shell { grid-template-columns: 240px 380px 1fr; }
}

/* ≤ 1024 px: Rail bleibt 240, Liste und Karte STAPELN vertikal in der rechten Spalte.
   - grid-template-columns 240 + 1fr (zwei Spalten)
   - grid-template-rows 1fr + 1fr (zwei Zeilen gleicher Höhe)
   - rail spannt beide Zeilen (grid-row: 1 / span 2)
   - .detail kommt explizit in Zeile 2 Spalte 2 -- ohne das landet es in (2,1) statt (2,2),
     weil CSS-Grid Auto-Placement zeilenweise läuft. */
@media (max-width: 1024px) {
  .shell {
    grid-template-columns: 240px 1fr;
    grid-template-rows: 1fr 1fr;
  }
  .rail { grid-row: 1 / span 2; }
  .detail { grid-column: 2; grid-row: 2; }
}
```

### Was fällt weg

- `@media (max-width: 1280px)` (Rail-Kollaps) — ersatzlos gelöscht. Der 1200-er ersetzt die
  Layout-Aufteilung, behält aber Rail bei 240.
- `data-view`-Switching (`.shell[data-view="list"] .detail { display: none }` usw.) — bei
  1024 sind Liste **und** Karte gleichzeitig sichtbar (gestapelt), also kein View-Switch mehr
  nötig. Das `[data-view]`-Attribut auf `.shell` bleibt für andere Zwecke (Editor-Replace-
  Verhalten, Back-Button-Sichtbarkeit) unangetastet.

### Wächter (in G-R.4)

`test_shell_grid_is_240_480_1fr` aus Block G wird umgestellt: die Default-Regel
`240px 480px 1fr` bleibt unverändert (Akzeptanzkriterium), aber die Breakpoint-Prüfung
wechselt von `@media (max-width: 1280px)` auf `@media (max-width: 1200px)` und auf
`@media (max-width: 1024px)` — beide müssen die neuen Werte tragen.

### Nikinger-Sichtung (Erwartung)

- 1200 px: Rail 240 + Labels sichtbar (Übersicht, Einstellungen, Mein Space, Offen, etc.),
  Liste 380 + Spaces+Recent sichtbar, Karte 1fr + Verknüpfungen sichtbar — **kein Kollaps**.
- 1024 px: Rail 240 + Labels sichtbar, Liste oben (Spaces+Recent+Refresh+Legende), Karte
  darunter (Verknüpfungen mit Toolbar) — **gestapelt, nicht weg**.

---

## G-R.2 — Map-Leerraum + Layer-Tone-Vereinheitlichung

### Vorher

```css
/* app.css:388-392 */
.detail {
  display: flex;
  flex-direction: column;
  min-height: 0;
}

/* app.css:1085-1091 */
.detail__graph {
  display: flex;
  flex-direction: column;
  flex: 1;
  min-height: 0;
  padding: calc(var(--space) * 4);     /* 32 px rundum */
}
.detail__graph .overview__graph { flex: 1; min-height: 0; }
```

`.detail` hat **kein** explizites `background`. Es erbt von `.shell` → `body`
→ `var(--bg-void)` = `#000`. `.list` dagegen hat `background: var(--bg)` = `#0B0D10`. Die
drei sichtbaren Töne für "Spalten-Hintergrund" sind also:

| Bereich | Token | Hex |
|---|---|---|
| `.list` | `--bg` | `#0B0D10` |
| `.detail` (außerhalb Map) | `--bg-void` (erbt von body) | `#000` |
| `.overview__graph` (Map-Innenraum) | `--surface` | `#14181D` |

Das ist genau die Token-Drift, die der F-Wächter nicht fängt: drei **verschiedene** Token
für denselben konzeptuellen Layer "Spalten-Hintergrund". Der 32-px-Rundum-Padding von
`.detail__graph` macht die Drift **sichtbar** — rund um die Karte sieht der Nutzer einen
schwarzen Ring, der nirgends sonst in der UI vorkommt.

### Nachher

```css
/* app.css:388-393 */
.detail {
  display: flex;
  flex-direction: column;
  min-height: 0;
  background: var(--bg);          /* G-R.2: gleich wie .list -- eine Ton-Lage für "Spalte" */
}

/* app.css:1085-1092 */
.detail__graph {
  display: flex;
  flex-direction: column;
  flex: 1;
  min-height: 0;
  /* G-R.2: oben/unten 16 px statt 32 px -- die Karte reicht jetzt fast an die Slot-Kanten,
     statt von einem schwarzen Ring umgeben zu sein. Links/rechts bleiben bei 32 px, weil
     die Karte sonst den Text-Knopf-Toolbar (Plan §5 D2) an die Slot-Kante klebt. */
  padding: calc(var(--space) * 2) calc(var(--space) * 4);
}
.detail__graph .overview__graph { flex: 1; min-height: 0; }
```

### Was sich ändert

- `.detail`-Hintergrund ist jetzt `--bg` wie `.list`. Der schwarze Ring rund um die Karte
  verschwindet, weil der Ring jetzt denselben Ton hat wie die Liste daneben — er ist
  weiterhin sichtbar (wegen der `border: 1px solid var(--line)` der `.overview__graph`),
  aber als "gleiche Lage", nicht als "schwarze Höhle".
- `.detail__graph` oben/unten 16 px statt 32 px — die Karte füllt den Slot vertikal
  großzügiger aus, ohne die Slot-Kante zu berühren (für den Atmungs-Effekt bleibt 1× Spalte
  Luft).

### Was sich NICHT ändert

- V112-Wächter (Höhenkette `.detail__graph → .overview__graph`) bleibt scharf. Der Canvas
  füllt weiterhin via `flex: 1; min-height: 0` — der Padding-Reduktion ändert daran nichts.
- `requestAnimationFrame(resize)` in `graph.js` bleibt — die Karte rechnet weiterhin gegen
  den `.overview__graph`-Rect, nicht gegen den `.detail__graph`-Padding-Rect.

### Wächter (in G-R.4)

`test_detail_graph_has_a_definite_height_chain` bleibt unverändert (V112-Wächter nach Umzug).
Zusätzlich kommt ein neuer Test: `test_detail_uses_the_column_background_not_void`, der
prüft, dass `.detail` einen expliziten `background: var(--bg)` trägt.

---

## G-R.3 — Editor-YAML bündig zur Suchzeile

### Vorher

```css
/* app.css:1312-1318 */
.editor__head {
  display: flex;
  align-items: center;
  gap: var(--space);
  border-bottom: 1px solid var(--line);
  padding: calc(var(--space) * 1.5) calc(var(--space) * 3);   /* 12 px oben/unten */
}
```

Im Screenshot 03 beginnt die "Kopfdaten YAML-Frontmatter"-Leiste bei ungefähr y≈210 px.
Die Suchzeile im List-Slot endet bei ungefähr y≈185 px. Dazwischen liegen ~25 px
"editor__head"-Höhe. Der Nikinger-Wunsch: das obere Ende der YAML-Kopfzeile **schließt
bündig ab** mit dem unteren Ende der Suchzeile.

### Nachher

```css
/* app.css:1312-1325 */
.editor__head {
  display: flex;
  align-items: center;
  gap: var(--space);
  border-bottom: 1px solid var(--line);
  /* G-R.3: padding-top von 12 px auf 4 px reduziert (war 1.5*var(--space), wird 0.5*var) --
     die YAML-Kopfzeile rückt damit um ~8 px nach oben und liegt auf gleicher Höhe wie die
     Suchzeilen-Unterkante im List-Slot (gemessen mit Block-G Self-Check, exakt zu verifizieren
     im G-R Self-Check). padding-bottom bleibt 12 px, damit der Titel-Input nicht die untere
     Trennlinie berührt. */
  padding: calc(var(--space) * 0.5) calc(var(--space) * 3) calc(var(--space) * 1.5);

  /* G-R.3: position:sticky + bg --surface-raised + border-bottom --line (schon vorhanden) +
     z-index:1. Damit verhält sich der Editor-Kopf genauso wie der List-Kopf (sticky bei
     Scroll, gleicher Hintergrund-Ton, gleiche Trennlinie). Nutzer sieht beim Scrollen im
     Editor, dass der Titel stehen bleibt -- parallel zum Such-Verhalten in der Liste. */
  position: sticky;
  top: 0;
  background: var(--surface-raised);
  z-index: 1;
}

/* G-R.3: Panel-Head-Höhe an Item-Row-Höhe annähern (Nikinger-Vorgabe: "ziemlich genau so
   groß wie eine item Zeile"). .list__row hat padding 8 16 (Summe vertikal 16 px + Content
   ~25 px = 41 px). .panel__head hat padding 6 24 (Summe vertikal 12 px + Content ~19 px =
   31 px) -- 10 px kleiner. Auf 11 px oben/unten erhöhen → 41 px. */
.panel__head { padding: 11px calc(var(--space) * 3); }
```

### Was sich ändert

- `.editor__head` ist jetzt sticky mit `--surface-raised`-Hintergrund — verhält sich wie
  `.list__head`. Visuelles Gewicht der beiden Spalten-Köpfe ist identisch.
- `.editor__head` padding-top von 12 px auf 4 px reduziert: -8 px Höhe, YAML-Kopfzeile rückt
  nach oben.
- `.panel__head` padding vertikal von 6 px auf 11 px erhöht: +10 px, damit der collapsed
  Header genauso hoch ist wie eine Item-Row (~41 px vs. ~41 px).

### Was sich NICHT ändert

- Die Tastatur-Reihenfolge bleibt: Titel-Input (Tab 1) → Buttons → YAML-Input-Felder. Die
  sticky-Position ändert nichts am Fokus-Flow.
- Die "Archivieren"-Position (Nikinger-2026-09-08-Meldung) bleibt: `.editor__close-button`
  mit `margin-left: var(--space) * 1.5` aus Block B bleibt unverändert.

### Wächter (in G-R.4)

Zwei neue Tests:

- `test_editor_head_is_sticky_with_the_list_head_background`: prüft, dass `.editor__head`
  `position: sticky`, `background: var(--surface-raised)` und `border-bottom: 1px solid
  var(--line)` trägt.
- `test_panel_head_height_matches_a_list_row`: prüft, dass `.panel__head` ein padding-top
  und padding-bottom von 11 px trägt (item-row-Höhe ~41 px, panel-head-Höhe nach G-R.3
  ~41 px).

### Nikinger-Sichtung (Erwartung)

- Im 1440-px-Screenshot 03: "Kopfdaten YAML-Frontmatter" beginnt auf gleicher Höhe wie das
  Ende der Suchzeile im List-Slot (Item-Zeile 1 beginnt direkt darunter, alle drei in einer
  visuellen Linie). "Text Markdown"-Leiste darunter ebenfalls.
- Beim Scrollen im Editor: `.editor__head` bleibt am oberen Rand kleben, parallel zu
  `.list__head`-Verhalten.

---

## G-R.4 — Wächter (Layer-Tone-Drift + neue Breakpoint-Werte)

### Vier neue Tests in `test_static_routes.py`

1. **`test_detail_uses_the_column_background_not_void`** — G-R.2-Beleg: `.detail` trägt
   `background: var(--bg)`. Wer das rausnimmt (oder auf `--bg-void` zurückdreht), fängt
   diesen Test.

2. **`test_1200_breakpoint_keeps_rail_at_240`** — G-R.1-Beleg: in `@media (max-width:
   1200px)` darf `.shell` NICHT `64px` als erste Spalte haben (Rail-Kollaps-Verbot), und
   `.rail__label` darf NICHT `display: none` haben.

3. **`test_1024_breakpoint_stacks_list_over_detail`** — G-R.1-Beleg: in `@media (max-width:
   1024px)` hat `.shell` `grid-template-rows: 1fr 1fr` UND `.rail` trägt
   `grid-row: 1 / span 2` UND `.detail` trägt `grid-column: 2; grid-row: 2`. Das alte
   `[data-view]-Switching` ist weg.

4. **`test_editor_head_is_sticky_with_the_list_head_background`** und
   **`test_panel_head_height_matches_a_list_row`** — siehe G-R.3 oben.

### Umstellung von Block-G-Test

`test_shell_grid_is_240_480_1fr` aus Block G ändert sich:

- Default-Block-Anker bleibt: `240px 480px 1fr` unverändert.
- Statt `@media (max-width: 1280px)` wird jetzt `@media (max-width: 1200px)` und
  `@media (max-width: 1024px)` geprüft.
- Beide neuen Media-Queries müssen `240px` als erste Spalte tragen.
- Die 1200-er Query muss `380px` als zweite Spalte tragen.
- Die 1024-er Query muss `1fr` als zweite Spalte tragen.

---

## Was Block G-R NICHT tut (bewusst ausgeschlossen)

- **Keine Änderung an `graph.js`.** Die Karte rendert weiterhin auf `<canvas>` (nicht
  SVG), `requestAnimationFrame(resize)` und ResizeObserver bleiben. Der Canvas füllt via
  `.overview__graph { flex: 1; min-height: 0 }` weiterhin den Parent — Block G-R ändert
  NUR den Padding rundherum, nicht den Canvas selbst.
- **Keine Änderung am d3-Layout.** Die Knoten-Position innerhalb des Canvas wird weiterhin
  von der Force-Simulation bestimmt; dass einige Knoten weiter oben clustern und unten Luft
  bleibt, ist ein **Layout-Verhalten**, nicht ein **CSS-Bug**. Wer die Karte "richtig voll"
  sehen will, muss das d3-Force-Layout anfassen — das ist Block J (P8.6-§6.4 hat D4 als
  einzige Scope-Erweiterung dort verbucht) oder eine eigene Sub-Phase.
- **Keine Änderung an `.editor__head`-Inhalt.** Der Titel-Input und die drei Buttons
  bleiben in derselben Reihenfolge; was sich ändert, ist nur Position+Hintergrund.
- **Keine Änderung am `[data-view]`-Attribut oder an `clearDetail`/`showOverviewPane`.**
  Die JS-Logik bleibt; nur die CSS-Regel, die bei 1024 px das View-Switching erzwingt,
  fällt weg.

---

## Akzeptanzkriterien (lauffähig im G-R Self-Check)

1. `pytest` läuft mit **vier neuen + einem angepassten** Wächter, 976 + 5 = **981** Tests.
2. `ui_budget` 5/5, app.css wächst um ~600-800 B (zwei neue Media-Queries + Sticky-Head
   + Panel-Padding — geschätzt).
3. Sechs Selbst-Screenshots `p86_block_g_r_{01..06}_*.png`:
   - 01: 1440-Übersicht — `.detail` hat jetzt `--bg`-Hintergrund, der schwarze Ring rund
     um die Karte ist weg.
   - 02: 1440-Editor-offen — "Kopfdaten YAML-Frontmatter" beginnt auf gleicher Höhe wie
     Suchzeilen-Unterkante im List-Slot.
   - 03: 1200-Übersicht — Rail 240 px mit Labels sichtbar, Liste 380, Karte ~640.
   - 04: 1024-Übersicht — Rail 240 px mit Labels sichtbar, Liste oben, Karte darunter
     gestapelt (kein View-Switch).
   - 05 + 06: Detail-Checks (Editor auf 1200 / 1024 analog).
4. Visuelle Selbstprüfung mit `local_vision` (qwen3-vl:8b) gegen die Screenshots --
   "schwarzer Ring weg" und "YAML auf Suchzeilen-Höhe" als messbares Kriterium.

---

## Lock-Liste (was G-R öffnet/schließt)

| Lock | Status | Wirkung |
|---|---|---|
| P8.6-X (Grid 240/480/1fr) | bleibt | Default-Block unverändert |
| P8.6-Y (DOM-Umzug) | bleibt | Liste in section.list, Karte in section.detail |
| P8.6-P (Space-Zeile klickbar) | bleibt | nicht berührt |
| V112-Wächter | bleibt | Höhenkette scharf |
| P8.6-AB (Befund 8, Layer-Tiefe statt Farbe) | bleibt | Meta-Panel weiterhin kühl |
| P8.6-AD (Befund 1, rohe Hex nur in :root) | bleibt | durch F-Wächter geschützt |
| **NEU G-R.1** (Nav bleibt 240 in beiden Breakpoints) | öffnet | ersetzt 1280-er Regel |
| **NEU G-R.2** (Map-Padding + Layer-Tone) | öffnet | schließt drei sichtbare Töne auf einen |
| **NEU G-R.3** (Editor-Head sticky + YAML bündig) | öffnet | parallele Header-Logik zu .list__head |

Drei neue Locks, alle durch vier Wächter (G-R.4) abgesichert. Block H (Rail + Konto) bleibt
unverändert danach.

---

## Offene Punkte für nächste Session

- **d3-Layout-Tuning** (Knoten gleichmäßig im Canvas verteilen): nicht in G-R, weil Block
  G-R CSS-only ist. Wäre eine eigene Sub-Phase oder Block J.
- **Update-Banner-Overlap mit `.shell`-Top**: der Banner schiebt `.shell` um seine Höhe
  nach unten (`body.has-update-banner`); bei einem kürzeren Banner wird der Leerraum oben
  sichtbar. Nicht in G-R.
- **`.rail__account`-Anmutung**: kommt mit Block H (N.9, P8.6-Plan 2 §5).
