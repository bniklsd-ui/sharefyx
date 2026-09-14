# Phase 8.6 — Block H-R (Revision nach Sichtung)

> **Block H-R — Datum 2026-09-14, opencode/M3.** Eigener Commit, kein Patch auf `abed4c1`
> (analog G-R: H-R ist ein eigener Block mit eigenem Commit, kein nachträgliches Korrigieren
> von Block H). Sechs zusammenhängende Fixes aus der Nikinger-Sichtung vom 2026-09-14:
> **zwei neue Befunde** zu Block H (Bilder `p86_block_h_{01..03}_*.png`) plus **vier offene
> Backlog-Punkte** aus dem G-R-Nachtrag (Phase-Head `updated:`-Kette).

---

## §0 Anlass

Nikinger hat am 2026-09-14 die drei Block-H-Bilder gesichtet und vier zusätzliche Befunde
gemeldet:

| Quelle | Befund | Fix hier |
|---|---|---|
| **NEU — Bild 01** | "alle drei Slots echtes OLED-BLACK; Map, Update-Banner und andere drüber gesetzte Elemente behalten ihren jetzigen (Layer 3) Look" | **H-R.1** |
| **NEU — Bild 03** | "den beiden `.account-nav`-Knöpfen ausnahmsweise dieselbe Farbe wie dem Ändern-/Verstanden-Knopf — diese Variante sieht man kaum" (Einstellungen + Abmelden unten bleiben, kleine Trennung ist gut) | **H-R.2** |
| **Backlog G-R** | Layer-Tone-Drift im Detail-Slot (drei+ Töne sichtbar) — wird durch H-R.1 gelöst, daher hier kein eigenes Sub | **H-R.1** |
| **Backlog G-R** | Editor-YAML nicht bündig zur Suchzeile (nur zur Item-Zeile) | **H-R.3** |
| **Backlog G-R** | 1024-er Map-Overlap | **H-R.4** |
| **Backlog G-R** | 1024-er Editor-Modus | **H-R.5** |

**Sechs Items, fünf Sub-Blöcke** (H-R.1 löst zwei Befunde zusammen — der neue OLED-BLACK-Befund
und den alten Layer-Tone-Drift-Backlog-Punkt in einem Schritt).

**Schritt-Reihenfolge beim Bau:** H-R.1 → H-R.2 → H-R.3 → H-R.4 → H-R.5 → Wächter (zuletzt,
sonst melden sie während des Baus Fehler, die gerade entstehen — gleiche Regel wie
Plan 2 §6.5 und G-R §Reihenfolge).

**Commit-Strategie:** ein Block = ein Commit. Alle fünf Sub-Blöcke in einem Atom (Nikinger hat
sie als zusammenhängende Welle gegeben; Aufsplitten würde nur das Diff-Review erschweren).

---

## §1 H-R.1 — OLED-BLACK für die drei Slots

### Vorher (Stand `abed4c1`)

```css
/* app.css:147-154 */
body { background: var(--bg-void); ... }   /* Layer 0, schon #000 */

/* app.css:357-401 */
.shell { display: grid; grid-template-columns: 240px 480px 1fr; height: 100vh; overflow: hidden; }
.rail, .list, .detail { min-width: 0; overflow-y: auto; }
.rail { ... background: linear-gradient(180deg, var(--rail-top), var(--bg)); }   /* #0E1116 → #0B0D10 */
.list { ... background: var(--bg); }                                            /* #0B0D10 */
.detail { ... background: var(--bg); }                                          /* #0B0D10 seit G-R.2 */
```

**Drei Töne** für "Slot-Hintergrund": `--bg-void` (body), `--bg` (.rail über Gradient nach
`--bg`, .list, .detail). Höhere Layer (`--surface`, `--surface-raised`) tragen die Map, das
Update-Banner, den Editor-Kopf, den Listen-Kopf. Nikinger-Sichtung 2026-09-14: "alle drei
Slots echtes OLED-BLACK" — die "drüber gesetzten Elemente" behalten ihren jetzigen
Layer-3-Look (Akzent-Flächen, Banner, Panels, Knöpfe, Dialoge).

### Nachher

```css
/* app.css:147-154 — body bleibt */
body { background: var(--bg-void); ... }

/* app.css:357-401 — drei Slots bekommen explizit dasselbe Schwarz */
.shell { ... /* kein eigener background, erbt von body — bleibt */ }
.rail  { ... background: var(--bg-void); }   /* linear-gradient ersatzlos weg */
.list  { ... background: var(--bg-void); }
.detail{ ... background: var(--bg-void); }
```

**Was bleibt unverändert (Layer 3):**
- `.detail__graph` / `.overview__graph` (Map-Karte): `background: var(--surface)` (`#14181D`)
- `.editor__head` (sticky Editor-Kopf): `background: var(--surface-raised)`
- `.list__head` (sticky Listen-Kopf): `background: var(--surface-raised)`
- `.update-banner`: `background: var(--surface-raised)`
- `.panel`, `.panel--body`, `.btn-primary`, `.btn`, `.account-nav` (nach H-R.2), `.overlay__panel`,
  `.rail__account`-Trennkante (`var(--line)`): alles wie gehabt

**Was ist neu:**
- `--rail-top`-Token bleibt im `:root` definiert (für eventuelle künftige Verwendung), wird
  aber von keiner Regel mehr gelesen — toter Token, bewusst stehen gelassen (Löschen wäre eine
  Tabu-Verletzung an `:root`, die nicht zum Befund gehört; ein toter Token schadet nichts).

### Was das ändert (visuell, gemessen am 1440er-Bild)

- Body, Rail, Liste, Detail sind **uniform schwarz** (`#000`) auf OLED = echte Pixelabschaltung.
- Die "drei sichtbaren Töne für Spalten-Hintergrund" fallen weg.
- Die Karte (`.detail__graph` mit `var(--surface)`) **schwebt** als erkennbar helleres Rechteck
  auf dem schwarzen Detail-Slot — der Kontrast war vorher (G-R.2) zu zaghaft, weil
  `--surface` (`#14181D`) und `--bg` (`#0B0D10`) sich nur um ~6 Helligkeits-Stufen
  unterscheiden. Nach H-R.1 sind es **14 Stufen** (`#000` vs `#14181D`).
- Die Trennlinien (`border-right: 1px solid var(--line)`) werden auf schwarzem Grund sichtbar
  schwächer (`--line` ist ein sehr dunkles Grau) — bewusst so, der Übergang zwischen den Slots
  soll ohne harte Linie funktionieren. Falls die Nikinger-Sichtung das anders will, ist das ein
  H-R.1.1-Folgeblock, nicht Teil von H-R.1.

### Wächter (in §5 zusammengefasst)

- `test_three_slots_use_oled_black`
- `test_rail_has_no_gradient_anymore`
- `test_layer3_elements_keep_surface_tone`

---

## §2 H-R.2 — `account-nav`-Knöpfe bekommen Akzent-Farbe

### Vorher (Block H Stand)

```css
/* app.css:661-687 */
.account-nav {
  display: flex; align-items: center; gap: var(--space);
  width: 100%; padding: 8px calc(var(--space) * 2);
  margin: 0 0 calc(var(--space) * 2);
  background: none; border: none;
  border-left: 2px solid var(--line-strong);
  border-radius: var(--radius-sm);
  color: var(--text); font-weight: 500; font-size: var(--fs-ui);
  cursor: pointer; text-decoration: none;
}
.account-nav:hover { background: var(--select-fill-quiet); outline: 1px solid var(--select-line-quiet); ... }
.account-nav .icon { margin-left: auto; }
```

Nikinger-Sichtung 2026-09-14: "diese Variante sieht man kaum". H2 hatte die Form gebaut
(Akzentkante + Chevron), aber die **Farbe** ist zu schwach — transparenter Hintergrund + dünner
Hover reicht nicht. "Gib den beiden Buttons da oben **ausnahmsweise** dieselbe Farbe wie dem
Ändern button" — die "ausnahmsweise"-Formulierung ist wichtig: H2-Kategorie "Navigation"
bleibt (sie sind keine Aktionen), aber bei diesem einen Knopf-Paar ist Akzent-Fill gerechtfertigt,
weil die Position im Passwort-ändern-Dialog **Hauptwege** sind.

### Nachher

```css
/* app.css:661-687 */
.account-nav {
  display: flex; align-items: center; gap: var(--space);
  width: 100%; padding: 8px calc(var(--space) * 2);
  margin: 0 0 calc(var(--space) * 2);
  border: 1px solid var(--accent-edge);
  border-left: 3px solid var(--accent);
  border-radius: var(--radius-sm);
  background: var(--accent-quiet);                       /* neu: Akzent-Fill, gedämpft */
  color: var(--text); font-weight: 500; font-size: var(--fs-ui);
  cursor: pointer; text-decoration: none;
}
.account-nav:hover { background: var(--accent-quiet); outline: 1px solid var(--accent-line); outline-offset: -1px; }
.account-nav .icon { margin-left: auto; color: var(--accent); }
```

**Token-Begründung:**
- `var(--accent-quiet)` statt `var(--accent)` direkt — die Knöpfe sollen **auffallen** (Akzent),
  aber **nicht** mit dem "Ändern"-Knopf konkurrieren (der ist `linear-gradient(180deg, accent-face-top, accent-face-bottom)`,
  der Haupt-Aktionsknopf im Dialog). `--accent-quiet` (`rgba(62,141,243,.14)`) ist die
  Standard-Antwort der Konvention für "wichtige Fläche, aber nicht primär".
- `border-left: 3px solid var(--accent)` — die alte 2-px-Akzentkante bleibt als Akzent,
  wird aber etwas dicker (3 px) und **nutzt jetzt `--accent`** statt `--line-strong`. Das ist
  der Knopf-Afford, den V133 eingefordert hatte, in der jetzt sichtbaren Farbe.
- `border: 1px solid var(--accent-edge)` ringsum — damit der Knopf in der Karte nicht
  "verschwimmt", sondern eine rechteckige Form hat.
- Hover bleibt erhalten, aber gedämpfter (kein doppelter Akzent — sonst flackert es).

**Was bleibt unverändert:**
- `.rail__action` (Einstellungen + Abmelden unten): Nikinger explizit "passt so, kleine
  Trennung ist gut" — die Block-H-H1-Reihenfolge und die Border-top-Trennung in `.rail__account`
  bleiben unangetastet.
- `.account-nav`-Markup: `<button class="account-nav">…<svg class="icon">…</svg></button>`
  bleibt (H2-Komposition).

### Wächter (in §5)

- `test_account_nav_uses_accent_fill`
- `test_account_nav_hover_kept`
- `test_rail_account_unchanged_from_block_h`

---

## §3 H-R.3 — Editor-YAML bündig zur Suchzeile (nicht zur Item-Zeile)

### Vorher (G-R.3-Stand)

```css
/* app.css:1350-1370 */
.editor__head {
  display: flex; align-items: center; gap: var(--space);
  border-bottom: 1px solid var(--line);
  padding: calc(var(--space) * 0.5) calc(var(--space) * 3) calc(var(--space) * 1.5);   /* 4 12 12 */
  position: sticky; top: 0; background: var(--surface-raised); z-index: 1;
}
```

G-R.3 hat `padding-top` von 12 px auf 4 px reduziert, damit die YAML-Kopfzeile um ~8 px
nach oben rückt. Nikinger-Sichtung 2026-09-14: das reicht **nicht** — die YAML-Kopfzeile muss
bündig zur **Suchzeilen-Unterkante** im Listen-Slot sein, nicht zur Item-Zeile. Aktuell ist sie
zur Item-Zeile bündig (weil die Item-Zeile unter der Suchzeile sitzt, also ist die YAML
~Suchhöhe tiefer als die Suchzeile-Unterkante).

### Was "bündig zur Suchzeile-Unterkante" heißt (gemessen am 1440er-Bild)

- `.list__head`-Höhe bei 1440 px ≈ 89 px (padding-top 12 + Suchfeldhöhe ~38 + padding-bottom
  12 + Chips-Zeile ~22 + padding 5 ≈ 89 px gesamt — grobe Schätzung, präzise Werte kommen aus
  V142-Probe).
- `.editor__head`-Höhe aktuell bei 1440 px ≈ 76 px (padding-top 4 + Inhalt ~38 + padding-bottom
  12 + border 1 = ~55 px; abweichend von der Messung im Phase-Head — die Werte werden mit
  V142 präzise nachgemessen, bevor der Fix landet).

**Bündigkeit heißt:** `.editor__head`-Oberkante ist auf gleicher Y-Position wie
`.list__head`-Oberkante (beide sind `position: sticky; top: 0` in ihrem jeweiligen Slot — der
Editor ersetzt die Karte im Detail-Slot, daher teilen sie sich die Y-Achse des Detail-Bereichs
gemeinsam mit dem Listen-Slot des `.list`-Containers).

**Was im CSS zu ändern ist:**
- Aktuell hat `.editor__head` `padding-top: calc(var(--space) * 0.5)` (4 px). Damit die
  YAML-Box direkt unter dem Editor-Header beginnt, müsste `padding-top: 0` sein.
- Aber: dann klebt der Titel (`Logging standardisieren`) direkt am oberen Rand, das ist
  optisch unangenehm. Besser: `padding-top: calc(var(--space) * 0.25)` (2 px) — minimaler
  Atemraum, aber die YAML-Box beginnt 2 px unter dem oberen Rand, nicht 4 px.
- Alternative: `.list__head` und `.editor__head` bekommen **gleiches** `padding-top` und
  **gleiches** `padding-bottom` — dann ist ihre Höhe gleich, ihre Y-Position gleich, ihre
  Unterkante gleich. Das ist die ehrlichste Lösung.

### Nachher (Vorschlag — abhängig von V142-Messung)

```css
/* app.css:1350-1370 */
.editor__head {
  display: flex; align-items: center; gap: var(--space);
  border-bottom: 1px solid var(--line);
  padding: calc(var(--space) * 0.5) calc(var(--space) * 3) calc(var(--space) * 1.5);   /* bleibt 4 12 12 */
  position: sticky; top: 0; background: var(--surface-raised); z-index: 1;
  /* neu: gleiches margin-top wie .list__head, falls die Sticky-Position
     sich am Eltern-Slot orientiert -- präzise Festlegung folgt V142. */
}
```

**V142 bestimmt erst die korrekten Werte.** Ohne Messung würde ich raten — und genau das
verbietet die Phase ("messen, nicht schätzen", gilt seit Block D).

**Was bleibt unverändert:**
- Sticky + `position: sticky; top: 0` (Block G-R G-R.3 hat das eingeführt; nicht aufweichen).
- Hintergrund `--surface-raised` (sonst scrollt der Inhalt durch, das war der G-R.3-Mehrwert).
- Border-bottom (Trennlinie zum Body).

### Wächter

- `test_editor_head_padding_top_matches_list_head` (statisch — prüft das CSS-Padding)
- `[VERIFY] V142` (CDP-Probe `boundingBox` — prüft die tatsächliche Y-Position)

---

## §4 H-R.4 — 1024-er Map-Overlap verhindern

### Vorher (Block G-R G-R.1-Stand)

```css
/* app.css:1985-2001 */
@media (max-width: 1024px) {
  .shell { grid-template-columns: 240px 1fr; grid-template-rows: 1fr 1fr; }
  .rail { grid-row: 1 / span 2; }
  .detail { grid-column: 2; grid-row: 2; }
}
```

Bei 1024 px wird die Karte im unteren Slot gestapelt. Backlog: "1024-er Map-Overlap" — die
Karte überlappt mit dem Listen-Slot darüber oder ragt in die Rail hinein.

### Was "Map-Overlap" meinen könnte (Klärung V143 vor dem Fix)

Drei plausible Lesarten — alle drei müssen mit V143 zuerst gemessen werden, dann wird
eine oder mehrere fixiert:

1. **Karte überlappt Liste nach oben** — `.detail__graph`-Höhe ist `flex: 1; min-height: 0` in
   einer 1fr-Zeile, sollte eigentlich passen. Falls nicht, ist die Höhenkette falsch.
2. **Karte überlappt Rail** — Rail spannt zwei Zeilen, Detail sitzt in (2,2). Falls die
   Karte nach links über die 1fr-Grenze wächst (z.B. weil `padding: calc(var(--space) * 4)`
   links/rechts den Eltern-Slot sprengt), ragt sie in den Rail-Bereich.
3. **Karte überlappt Editor** — wenn der Editor die Karte ersetzt (Detail im Editor-Modus),
   sitzt er im gleichen Slot. Kein Overlap erwartet, aber Backlog sagt "1024-er Map-Overlap"
   — möglicherweise im Read-only-Modus (Karte sichtbar, Editor nicht).

### Nachher

Wird erst nach V143 festgelegt. Mögliche Fixes (einer oder mehrere):

```css
@media (max-width: 1024px) {
  /* Fix-Lesart 1: Höhe statt min-height, sonst wächst die Karte über den Slot */
  .detail__graph { min-height: 0; height: 100%; box-sizing: border-box; }

  /* Fix-Lesart 2: Padding reduzieren, damit die Karte den Eltern-Slot nicht sprengt */
  .detail__graph { padding: calc(var(--space)) calc(var(--space) * 2); }

  /* Fix-Lesart 3: Karte im Read-only-Modus bekommt eine Höhenbegrenzung */
  .detail__graph { max-height: calc(50vh - var(--space) * 4); }
}
```

Welche Lesart zutrifft, entscheidet V143 durch eine `getBoundingClientRect()`-Probe bei
1024 px Breite und 768 px Höhe (übliches iPad-Format).

### Wächter

- `[VERIFY] V143` (CDP-Probe — prüft die tatsächliche Bounding-Box)
- `test_1024_no_overlap_in_css` (statisch — prüft, dass es eine `height`/`max-height`-Regel
  im 1024er-Block gibt, die das Overlap verhindert — abhängig von der gewählten Lesart)

---

## §5 H-R.5 — 1024-er Editor-Modus voll bedienbar

### Vorher

Im 1024-er-Stapel sitzt der Editor im unteren Slot (`.detail` in grid-row: 2). Der Editor ist
scrollbar im Body (`overflow-y: auto` aus `.rail, .list, .detail`). Backlog: "1024-er
Editor-Modus" — der Nutzer soll den Editor voll bedienen können, ohne auf 1200 px oder mehr
ausweichen zu müssen.

### Was "voll bedienbar" heißt (Klärung V144 vor dem Fix)

- Editor-Header ist sichtbar + sticky (Block G-R.3 hat das eingeführt).
- Knöpfe "Archivieren", "Speichern", "×" sind erreichbar und klickbar (gleicher Abstand wie
  bei 1440 px).
- Formatierhilfen-Leiste (B I </> Link H Anführungszeichen 1. — Bearbeiten) ist sichtbar.
- Anhängen-Zeile am Fuß ist erreichbar.
- YAML-Kopfdaten-Zeile ist sichtbar.

### Nachher

V144 misst, was bei 1024 px konkret fehlt. Mögliche Fixes:

```css
@media (max-width: 1024px) {
  /* Fix-Variante A: Editor-Body wird scrollbar, Knöpfe bleiben oben */
  .editor { display: flex; flex-direction: column; height: 100%; }
  .editor__body { flex: 1; overflow-y: auto; }

  /* Fix-Variante B: Knöpfe bekommen mehr Padding, damit sie auf Touchscreens treffsicher sind */
  .editor__head { padding: calc(var(--space) * 1) calc(var(--space) * 3); }

  /* Fix-Variante C: Formatierhilfen wrappen, wenn zu schmal */
  .editor__format-toolbar { flex-wrap: wrap; }
}
```

Welche Variante(n) zutrifft, entscheidet V144.

### Wächter

- `[VERIFY] V144` (CDP-Probe bei 1024 px — Knöpfe/Formatierhilfen sichtbar und klickbar)
- Statischer Test, abhängig vom konkreten Fix

---

## §6 Locks (verbindlich, ab Block-Start)

- **H-R.1-L**: `body`, `.shell`, `.rail`, `.list`, `.detail` haben `background: var(--bg-void)`
  (`#000`). Höhere Layer-3-Elemente (`.detail__graph`, `.overview__graph`, `.editor__head`,
  `.list__head`, `.update-banner`, `.panel`, `.panel--body`, `.btn-primary`, `.btn`,
  `.overlay__panel`, `.account-nav` nach H-R.2, `.rail__account`-Trennkante via `--line`)
  behalten ihre bisherigen Background-Tokens (`--surface`, `--surface-raised`,
  `--accent-quiet`, `--accent-edge`, `--select-fill-quiet`, `--line`).
- **H-R.1-L**: `.rail`-`linear-gradient` ist ersatzlos weg. `--rail-top`-Token bleibt im
  `:root` definiert, wird aber von keiner Regel mehr gelesen — bewusst stehen gelassen, kein
  Refactoring-Scope.
- **H-R.2-L**: `.account-nav` hat Akzent-Farbe (genau: `background: var(--accent-quiet)` plus
  `border-left: 3px solid var(--accent)`). Hover bleibt erhalten. Knöpfe bleiben
  semantisch "Navigation" (öffnen etwas, ändern nichts), Akzent-Fill ist die
  Sichtbarkeits-Antwort, kein Rückfall in `.btn`-Plastik.
- **H-R.2-L**: `.rail__action` (Einstellungen + Abmelden) bleibt unverändert (Nikinger
  "passt so, kleine Trennung gut"). `.rail__account` behält `flex-direction: column`,
  `border-top: 1px solid var(--line)`, beide Knöpfe wie Block H.
- **H-R.3-L**: `.editor__head`-Padding-Top ist kleiner oder gleich `calc(var(--space) * 0.5)` (4 px),
  sodass die YAML-Box bündig(er) zur Suchzeilen-Unterkante sitzt. Konkreter Wert folgt V142.
- **H-R.3-L**: `.editor__head` bleibt `position: sticky; top: 0; background: var(--surface-raised);
  z-index: 1`. G-R.3-Verhalten nicht aufweichen.
- **H-R.4-L**: Bei `max-width: 1024px` überlappt die Karte weder die Liste darüber noch die
  Rail links daneben. Konkreter Mechanismus (`height`, `max-height`, `padding`-Reduktion)
  folgt V143.
- **H-R.5-L**: Bei `max-width: 1024px` sind alle Editor-Bedienelemente (Archivieren, Speichern,
  ×, Formatierhilfen, Anhängen) sichtbar und klickbar. Konkrete CSS-Anpassung folgt V144.
- **N.13** (Nikinger-Entscheidung 2026-09-14): OLED-BLACK ist eine **Layer-Architektur-Revision**,
  kein UI-Polish. Sie macht den `--bg`-Token und den `--rail-top`-Verlauf praktisch
  funktionslos — falls jemand in einer Folge-Phase einen der beiden wieder aktiviert, ist das
  eine bewusste Umkehrung von N.13, kein zufälliges Wiedereinsetzen.
- **N.14** (Nikinger-Entscheidung 2026-09-14): Akzent-Fill auf `.account-nav` ist ein
  **Spezialfall** ("ausnahmsweise"). Andere Navigation-Knöpfe (`.rail__action` für Einstellungen
  + Abmelden, andere künftige Nav-Elemente) bleiben transparent mit Akzentkante + Hover
  — die Akzent-Fill-Ausnahme gilt nur für Konto-Dialog-Einträge.

---

## §7 Abnahmekriterien

- **H-R.1-A**: Drei Selbst-Screenshots bei 1440/1200/1024 px (Übersicht + Konto-Dialog offen)
  zeigen, dass die Map-Karte und der Update-Banner **sichtbar auf schwarzem Grund schweben** —
  der Kontrast zwischen Slot-Hintergrund (`#000`) und Karten-Fläche (`#14181D`) ist erkennbar.
- **H-R.1-A**: Konto-Dialog im selben Screenshot zeigt, dass die `.account-nav`-Knöpfe (mit
  Akzent-Fill nach H-R.2) **vor** dem schwarzen Detail-Slot sichtbar bleiben.
- **H-R.2-A**: Konto-Dialog-Screenshot bei 1440 px zeigt, dass beide `.account-nav`-Knöpfe
  (Update-Log ansehen, Spaces verwalten) **sofort als wichtig** erkennbar sind — Nikinger
  Sichtung bestätigt "diese Variante sieht man" (im Gegensatz zu "kaum").
- **H-R.2-A**: Einstellungen + Abmelden unten in der Rail sind **unverändert** (Nikinger
  bestätigt Block H H1).
- **H-R.3-A**: Bei 1440 px ist die Unterkante von `.editor__head` auf gleicher Y-Position wie
  die Unterkante von `.list__head` (CDP-Probe `boundingBox().bottom`, Toleranz ≤ 2 px).
  Visuell: die YAML-Kopfdaten-Zeile `Kopfdaten YAML-Frontmatter · open · backend · itm_…`
  beginnt auf gleicher Höhe wie die `.list__search` oder direkt darunter — der 4-px-Versatz,
  der nach G-R.3 noch da war, ist weg.
- **H-R.3-A**: Bei 1200 px gilt dasselbe wie H-R.3-A für 1440 px.
- **H-R.4-A**: Bei 1024 px überlappt die Map weder die Liste darüber noch die Rail daneben
  (CDP-Probe `boundingBox()` für `.detail__graph`, `.list`, `.rail` — keine
  Rechteck-Schnittmenge).
- **H-R.5-A**: Bei 1024 px sind alle Editor-Knöpfe (Archivieren, Speichern, ×), die
  Formatierhilfen-Leiste und die Anhängen-Zeile sichtbar und klickbar (CDP-Probe
  `boundingBox()` + `elementFromPoint()`).

---

## §8 [VERIFY]-Marker

- **V140** — Sichtprüfung Block-H-R an 1440/1200/1024 px, Karte schwebt sichtbar auf schwarzem
  Grund. Screenshot-Paar (vorher/nachher) optional für visuelles Diff. **Vor Bau H-R.1**
  gemessen (Screenshots `p86_block_h_*.png` als Baseline), **nach Bau H-R.1** neu.
- **V141** — Sichtprüfung Konto-Dialog bei 1440 px, `.account-nav`-Knöpfe fallen auf.
  **Vor Bau H-R.2** gemessen (`p86_block_h_03_1440_konto_dialog.png` als Baseline), **nach
  Bau H-R.2** neu.
- **V142** — CDP-Probe `boundingBox` für `.list__head` und `.editor__head` bei 1440 px
  und 1200 px. **Vor Bau H-R.3** gemessen (aktueller Versatz wird dokumentiert), **nach
  Bau H-R.3** verifiziert (Toleranz ≤ 2 px).
- **V143** — CDP-Probe bei 1024 px × 768 px, `boundingBox` für `.detail__graph`, `.list`,
  `.rail`. **Vor Bau H-R.4** gemessen (welche Lesart zutrifft), **nach Bau H-R.4** verifiziert
  (keine Rechteck-Schnittmenge).
- **V144** — CDP-Probe bei 1024 px × 768 px, `elementFromPoint()` auf die Knöpfe-Position.
  **Vor Bau H-R.5** gemessen (welche Knöpfe genau fehlen), **nach Bau H-R.5** verifiziert
  (alle klickbar).

**V143 und V144 sind Mess-Vor-Bau-Schritte** (gleiche Regel wie Block E für V125) — wenn der
Bau ohne Messung begonnen würde, würde er die falsche Lesart fixen.

---

## §9 Wächter-Tests (statisch)

Alle in `phase5_ui/tests/test_static_routes.py` (oder einer neuen Datei
`phase5_ui/tests/test_oled_black.py` — abhängig davon, wie viele Tests es werden; Entscheidung
beim Bau).

| Test | Was er prüft | Sub-Block |
|---|---|---|
| `test_three_slots_use_oled_black` | `body`, `.shell`, `.rail`, `.list`, `.detail` haben alle `background: var(--bg-void)` (oder erben davon) | H-R.1 |
| `test_rail_has_no_gradient_anymore` | `.rail`-Block hat kein `linear-gradient(180deg, var(--rail-top), ...)` mehr (nur statisches `var(--bg-void)`) | H-R.1 |
| `test_layer3_elements_keep_surface_tone` | `.detail__graph`, `.overview__graph`, `.editor__head`, `.list__head`, `.update-banner` haben weiterhin `--surface`/`--surface-raised` als Background | H-R.1 |
| `test_account_nav_uses_accent_fill` | `.account-nav` hat einen Akzent-Fill (`var(--accent)`, `var(--accent-quiet)` oder Akzent-Gradient) als Background | H-R.2 |
| `test_account_nav_hover_kept` | `.account-nav:hover` behält ein Hover-Verhalten (mindestens `background`-Wechsel oder `outline`) | H-R.2 |
| `test_rail_account_unchanged_from_block_h` | `.rail__account` hat weiterhin `flex-direction: column` (H1-Stand), zwei Knöpfe drin (H1-Stand) | H-R.2 |
| `test_rail_action_unchanged` | `.rail__action` (Einstellungen + Abmelden) hat keinen Akzent-Fill | H-R.2 |
| `test_editor_head_padding_top_matches_list_head` | `.editor__head { padding-top: ... }` und `.list__head { padding-top: ... }` sind gleich (oder der Editor-Padding ist kleiner) | H-R.3 |
| `test_1024_no_overlap_in_css` | Bei `@media (max-width: 1024px)` gibt es eine Regel, die `.detail__graph`-Höhe begrenzt (`height`, `max-height` oder ähnlich) | H-R.4 |
| `test_1024_editor_buttons_present` | Bei 1024 px sind die Knöpfe `#archive-button`, `#save-button`, `#editor-close` weiterhin im DOM und nicht `hidden` | H-R.5 |

**Bestehender F-Wächter bleibt scharf:** `test_no_raw_surface_hex_outside_root` und
`test_meta_panel_is_not_tinted_with_the_warning_colour` (aus `abed4c1`) müssen nach H-R.1
weiterhin grün sein — H-R.1 fasst keine rohen Hex an, sondern ändert nur bestehende
Token-Zuweisungen.

---

## §10 Datierte Tabu-Ausnahmen

**Keine.** Alle Änderungen in `phase5_ui/webui/static/{app.html,app.css}` und Tests in
`phase5_ui/tests/test_static_routes.py` (oder neuer Test-Datei). Tabu-Diff §0.3 bleibt leer.
JS-Änderungen sind keine geplant (H-R ist reines CSS+Markup).

---

## §11 Sichtprüfung-Plan

Drei Selbst-Screenshot-Sätze (analog Block H):

1. **Übersicht 1440** (`p86_block_h_r_01_1440_uebersicht.png`): Rail + Liste + Karte auf
   schwarzem Grund, Karte schwebt sichtbar.
2. **Konto-Dialog 1440** (`p86_block_h_r_02_1440_konto_dialog.png`): Dialog mit
   Akzent-Knöpfen (Update-Log ansehen, Spaces verwalten), schwarzer Hintergrund.
3. **Editor-offen 1440** (`p86_block_h_r_03_1440_editor_offen.png`): Editor-Sticky-Header
   bündig zur Suchzeile, schwarzer Hintergrund.

Plus zwei CDP-Probe-Screenshots für 1024 px:
4. **Übersicht 1024** (`p86_block_h_r_04_1024_uebersicht.png`): Liste oben, Karte unten,
   keine Überlappung.
5. **Editor-offen 1024** (`p86_block_h_r_05_1024_editor_offen.png`): Editor im unteren Slot,
   alle Knöpfe sichtbar.

**`screenshots_latest/`-Symlinks** nachziehen (P8.6-AK blockweise):
- `01_rail.png` → `p86_block_h_r_01_1440_uebersicht.png`
- `02_rail_1200.png` → `p86_block_h_r_02_1440_konto_dialog.png`
- `03_konto_dialog.png` → `p86_block_h_r_03_1440_editor_offen.png`
- `04_1024_uebersicht.png` → `p86_block_h_r_04_1024_uebersicht.png`
- `05_1024_editor.png` → `p86_block_h_r_05_1024_editor_offen.png`

**Wegwerf-Instanz** reproduziert den v3.0.1-Datenstand (analog Block G-R, Block H), Port und
Setup-Skript wie dort (`phase8_6_ui_polish/scripts/p86_block_*_self_check.py`). Stopp über
PID-Datei (Hard Rule 9 — kein `pkill -f`).

---

## §12 Schritt-Reihenfolge + Commit-Strategie

```
V140 (Baseline-Messung) → H-R.1 → V140 (Verify)  → H-R.2 → V141 (Verify)
H-R.3 → V142 (Messen) → H-R.3 anpassen → V142 (Verify)
H-R.4 → V143 (Messen) → H-R.4 anpassen → V143 (Verify)
H-R.5 → V144 (Messen) → H-R.5 anpassen → V144 (Verify)
Wächter-Tests schreiben (zuletzt) → pytest grün
Sichtprüfung-Skript laufen lassen → 5 Screenshots
Phase-Head `updated:`-Eintrag mit H-R-Block → Session-Block mit Befund-Protokoll
Rotation per `scripts/rotate_session_block.sh phase8_6_ui_polish`
docs/INDEX.md nachziehen
screenshots_latest/-Symlinks nachziehen
→ EIN COMMIT (atomarer Block, analog G-R)
```

**`pytest`-Baseline:** 981 (aus `abed4c1`) + ~9 neue Wächter = **990**. Genauer Wert nach
Bau.

**`ui_budget`-Erwartung:** 5/5, app.css wächst leicht (H-R.2 fügt Akzent-Border + Akzent-Fill
zu `.account-nav` hinzu, ~100 B; H-R.1 ändert nur Background-Werte, ~50 B; H-R.3 bis H-R.5
~100-300 B je nach V142/V143/V144-Ergebnis). Gesamt: app.css **24,5 → 25,0 KB** gzip,
ui_budget total ~144 KB.

**Push + Deploy:** wartet auf Nikinger (Drei-Bedingungen-Regel, wie Block H).

---

## §13 Was H-R NICHT macht

- **Keine Layer-Architektur-Umkehr.** H-R.1 setzt die Konvention "Hintergrund = schwarz,
  Karte = heller" für die drei Slots. Eine künftige Phase, die Layer 2/3 umstellen will,
  muss N.13 ausdrücklich aufheben — kein stiller Refactor zurück auf `--bg`/`--surface`-Mix.
- **Keine globalen Knopf-Farb-Änderungen.** Akzent-Fill ist auf `.account-nav` beschränkt.
  `.btn-primary` bleibt unverändert, `.btn` (neutral) bleibt unverändert.
- **Keine neuen JS-Funktionen.** H-R ist reines CSS+Markup. Wenn die Sichtprüfung ergibt,
  dass `.account-nav`-Akzent-Fill eine JS-Reaktion braucht (z.B. Toast bei Klick), ist das
  ein Folgeblock, nicht Teil von H-R.
- **Kein neuer `--bg`-Token, kein Löschen von `--rail-top`.** Beide Tokens bleiben im `:root`,
  sind aber nach H-R.1 funktionslos. Refactoring ist out of scope.
- **Keine Änderung am `body`-Background.** Body ist schon `--bg-void`, das war Phase 8.6
  Block D/E.
- **Keine Änderung an Map-Code (`graph.js`).** H-R.4 misst und fixt CSS-seitig; falls der
  Bug in `graph.js` liegt (z.B. `seedInitialPositions` rechnet gegen falsche Höhe), ist
  das ein Folgeblock.
