---
status: live
purpose: Phase-8.6-Block-H-R-3-Escalation-Report — drei Nikinger-Befunde aus Sichtung der H-R-Teil-2-Screenshots (2026-09-15), Mini-Plan-Vorschlag mit drei Locks (H-R.6/H-R.7/H-R.8) und zwei offenen Klärungsfragen für Claude Code zum Direkt-Einstieg
read-when: Claude Code übernimmt Phase-8.6-Block-H-R-3 (oder eine Folge-Phase); opencode/M3 nicht in der Lage, Pixel-Befunde zuverlässig selbst zu verifizieren (V-vision-befund 2026-09-11 — der Plugin-Pfad zerstört M3s nativen Bildpfad, der `read`-Tool-Pfad liefert nur 1 von 16 Bildern korrekt)
detail: L2
up: ../phase8_6_ui_polish/CLAUDE.md               # aktive Phase (Stand: 2026-09-15, Block H-R-Teil-2 ✅, Watchdog-Vormerkung in §Vormerkungen)
down:
  - ../docs/concepts/phase8_6_ui_polish_plan2.md   # aktiver Plan; §3 Block G/H/J-Locks, §5 Self-Check
  - ../docs/concepts/phase8_6_ui_polish_block_h_r_plan.md  # was H-R-Teil-2 gebaut hat (5 Sub-Blöcke)
  - ../docs/concepts/sichtpruefung_automation_tooling.md  # V-vision-befund, warum M3 für Pixel-Befunde ausscheidet
  - ../phase8_6_ui_polish/SESSIONS_ARCHIVE.md      # rotierte H-R-Teil-2 + Watchdog-Session-Blöcke
updated: 2026-09-15 (Escalation-Report neu — drei Nikinger-Befunde aus Sichtung der fünf H-R-Teil-2-Screenshots vom 2026-09-15; Mini-Plan-Vorschlag Block H-R-3 mit drei Locks H-R.6 (1024 px ohne Map = Umkehr von G-R.1) + H-R.7 (1024 px Editor-fullview) + H-R.8 (1440 px Listen-Slot bei Editor-open, Lesart-Klärung nötig); zwei offene Klärungsfragen für Claude Code vor dem Bau)
---

# Phase 8.6 — Block H-R-3 — Escalation-Report

## Anlass

Nikinger-Sichtung der fünf `p86_block_h_r_{01..05}_*.png`-Screenshots am
**2026-09-15** hat drei neue UX-Befunde ergeben, die über Block H-R-Teil-2
(gestern gebaut, ✅) hinausgehen. Block H-R-Teil-2 selbst wurde abgenommen
(Screenshots 01/02 super, 03 mit Vorbehalt, 04/05 mit Korrektur).

| # | Befund | Auswirkung |
|---|---|---|
| 1 | Bei 1440 px mit Editor offen — Listen-Slot zeigt Übersicht (oder beide Rail-Knöpfe „Übersicht" + „Alle Items" führen zur selben Aktion, V110-Status) — redundant zum Editor | Konzept + Layout, **Klärungsbedarf** |
| 2 | Bei 1024 px **keine Map** — Block G-R G-R.1 zeigt aktuell Liste + Karte gestapelt, soll aber ohne Map sein | Layout, **Umkehr von G-R.1** |
| 3 | Bei 1024 px Editor-open = **nur Editor im Viewport**, Navbar + Liste + Karte alle weg, ESC / × zurück zur vorherigen Ansicht | Layout, neue Variante (Editor-fullview) |

**Routing-Hinweis Nikinger 2026-09-15** (verbatim, „Evtl sollte sich Claude
Code darum kümmern, solange das Vision plugin bzw die Weiterleitung der
Bilder an dich nicht 100% funktioniert"): opencode/M3 ist für
Pixel-Befunde nicht der richtige Adressat. Diese Runde ist explizit
**Claude-Code-Territorium** — M3 kann die Locks ableiten und die
Wächter-Kriterien formulieren, aber nicht die Pixel-Verifikation am
laufenden System.

## Was bereits steht (für Claude Code zum Direkt-Einstieg)

- **Block H-R-Teil-2 ✅** (CSS-Fix `padding-bottom: calc(var(--space) * 5)`
  = 40 px in `app.css:1385`; V142-CDP-Probe pre 27,14 → post 0,86 px
  innerhalb der 2-px-Toleranz; H-R.4/.5 keine Fixes nötig, nur Wächter
  + 5 Selbst-Screenshots).
- **Tailscaled-Watchdog-Vormerkung ✅** in §Vormerkungen des Phase-Heads
  (drei Lösungs-Ansätze für „Control-Plane lange nicht erreichbar"-Fall;
  Mini-Phase nach P8.6 Gate, **nicht** P-R.6-Entscheidung).
- **Phase-Head `## Session stopped — 2026-09-15`** trägt den
  Watchdog-Session-Block (Diagnose) — wird vor diesem Commit per
  `scripts/rotate_session_block.sh phase8_6_ui_polish` ins Archiv rotiert;
  danach steht der heutige Escalation-Session-Block allein im Head.
- **`pytest` 991 grün**, **`ui_budget` 5/5 (143,7 KB)**, **`health_gate.sh
  --expected-version=v3.0.1 --expected-sha=6f19a8f` 8/8 grün**, Release-SHA
  `6f19a8f` (P8.5 vom 2026-09-05) unverändert — **kein P8.6-Deploy**.
- Nikinger-Vorgabe vom 2026-09-13: **„Push ja, Deploy nein"** — gilt
  weiter. Live bleibt v3.0.1 bis Plan-2/3-Konsolidation und Gate.
- Hard-Rule-Checkliste (Phase-Head §0.5) am Commit-Ende: pytest grün,
  Tabu-Diff leer, `node --check` auf jede berührte JS-Datei, ui_budget
  5/5, keine rohen `rgba(62,141,243)` außerhalb `:root`, neue `.md`
  haben L1-Card + INDEX-Zeile, kein Service-Touch.

## Mini-Plan-Vorschlag Block H-R-3

Drei Locks, drei Wächter, ein Commit. **Zwei Lesarten brauchen Klärung
vor dem Bau** (siehe §Offene Klärungsfragen).

### Lock H-R.6 — 1024 px ohne Map (Befund 2)

`@media (max-width: 1024px)` ändert sich:

| | Vorher (G-R.1) | Nachher (H-R.6) |
|---|---|---|
| Grid | `grid-template-rows: 1fr 1fr` | `grid-template-rows: 1fr` |
| `.rail` | `grid-row: 1 / span 2` | `grid-row: 1` |
| `.detail` | `grid-column: 2; grid-row: 2` | `grid-column: 2; grid-row: 1` |
| `.detail__graph` | sichtbar | unsichtbar (entweder über `.detail`-Wegfall oder `display: none` direkt) |

Konsequenz: bei 1024 px zeigt der Viewport Navbar links + Liste rechts;
kein Map-Slot mehr.

**Wächter:** `test_1024_no_overlap_in_css` aus H-R-Teil-2 muss
umgeschrieben werden — Stapel-Properties (`grid-template-rows: 1fr 1fr`
+ `.rail { grid-row: 1 / span 2 }`) sind obsolet. Neuer Wächter prüft
stattdessen `grid-template-rows: 1fr` + `.rail { grid-row: 1 }` +
`.detail__graph { display: none }` (oder gleichwertig).

### Lock H-R.7 — 1024 px Editor-fullview (Befund 3)

Bei ≤1024 px UND `data-view="editor"`:

```css
@media (max-width: 1024px) {
  body[data-view="editor"] .rail,
  body[data-view="editor"] .list,
  body[data-view="editor"] .detail__graph { display: none; }
  body[data-view="editor"] .editor { width: 100vw; height: 100vh; }
}
```

ESC und `#close-button` (×) togglen zurück auf `data-view="list"` (oder
vorherige View).

**Zwei Umsetzungsvarianten, gleichwertig:**

- **(a) CSS-only** via `data-view`-Attribut auf `<body>` oder `<main
  class="shell">`. Sauber, kein JS-Touch für die Layout-Logik. Markup-
  Change (Attribut setzen), JS nur für den Toggle (klein).
- **(b) JS-gesteuert** via Editor-open-Funktion, die bei ≤1024 px
  explizit das `data-view` setzt. Expliziter, aber mehr JS-Touch.

Empfehlung: **(a)** — weniger Bruchfläche, kein neuer JS-State, die
`@media`-Query entscheidet ohnehin.

**Wächter:** `test_1024_editor_fullview_hides_other_slots` neu —
Markup-Check für `data-view="editor"`-Pfad + CSS-Check für die
`display: none`-Regel im `@media (max-width: 1024px)`-Block +
CSS-Check für `width: 100vw` auf `.editor`.

### Lock H-R.8 — 1440 px Listen-Slot bei Editor-open (Befund 1, KLÄRUNGSBEDARF)

Zwei mögliche Lesarten — Nikinger hat sich noch nicht festgelegt
(verbatim: „wollten wir nicht 'alle Items' mit der Übersicht ersetzen?
Ist etwas doppelt gemoppelt, aber da bin ich mir nicht so sicher"):

**Lesart a — Rail-Konsolidierung (kleiner Diff):** `#rail-tree > button[data-action="all-items"]` wird ersatzlos gelöscht (V110-Status: führt ohnehin zur selben Aktion wie Home). `tree.js :: renderRail()` verzichtet auf den doppelten Knopf. Listen-Slot zeigt bei Editor-open weiterhin Items des selektierten Spaces, keine Layout-Änderung. **Wächter:** `test_rail_has_only_one_home_or_all_items_button` neu (genau einer von beiden existiert; `home-button` ist im Markup fix, `all-items`-Button wird per `data-action="all-items"` o. ä. identifiziert).

**Lesart b — Layout-Wechsel:** Bei Editor-open wird der Listen-Slot auf `display: none` gesetzt, **auch bei 1440 px**. Editor fullview unabhängig von Viewport-Breite, mit ESC/×-Rückkehr zur Liste. H-R.7 wird dann nicht nur für 1024 px, sondern für alle Breakpoints aktiv. **Wächter:** `test_editor_open_hides_list_at_all_viewports` neu (Markup-Check für `body[data-view="editor"] .list { display: none }` ohne Media-Query-Wrapper, oder gleichwertig).

**Wahrscheinliche Antwort** (Nikinger-Wahrscheinlichkeit, nicht festgelegt): **beides** — Rail-Konsolidierung ist ein 1-Zeilen-Diff, Layout-Wechsel ist der Hauptaufwand. **Vor dem Bau klären.**

## Offene Klärungsfragen (zwingend vor dem Bau)

1. **H-R.8 Lesart a vs. b** (siehe oben). Welche der beiden, oder beide?
2. **G-R.1 raus?** — wenn H-R.6 die 1024-er-Stapel-Logik auflöst, ist
   G-R.1 obsolet. Wächter `test_1024_no_overlap_in_css` muss umgeschrieben
   werden. Bestätigung: ja, G-R.1 darf raus (oder behalten + H-R.6 als
   Override drauf)? Wahrscheinlich: G-R.1 raus, sauberer Schnitt.

## Technischer Scope

| Datei | Änderung |
|---|---|
| `phase5_ui/webui/static/app.css` | `@media (max-width: 1024px)`-Block umschreiben (H-R.6) + `body[data-view="editor"]`-Regel hinzufügen (H-R.7) + ggf. `body[data-view="editor"] .list { display: none }` ohne Media-Query (H-R.8 Lesart b) |
| `phase5_ui/webui/static/app.html` | `data-view` Attribut auf `<body>` oder `<main class="shell">` initialisieren (Default `"list"`) |
| `phase5_ui/webui/static/app.js` + `js/editor.js` | bei Editor-open `data-view` auf `"editor"` setzen, bei Close auf vorherigen Wert zurück — minimaler JS-Touch, ~5–10 Zeilen |
| `phase5_ui/webui/static/tree.js` | Falls H-R.8 Lesart a: `#rail-tree > button[data-action="all-items"]`-Render-Pfad entfernen — 1-Zeilen-Diff |
| `phase5_ui/tests/test_static_routes.py` | drei Wächter: `test_1024_no_overlap_in_css` umschreiben (G-R.1-Erbe), `test_1024_editor_fullview_hides_other_slots` neu, `test_editor_open_hides_list_at_all_viewports` neu (nur falls H-R.8 Lesart b) — bzw. `test_rail_has_only_one_home_or_all_items_button` neu (nur falls H-R.8 Lesart a) |

## P8.6-Tabu §0.3 — Verträglichkeit

Alle fünf betroffenen Dateien sind explizit **erlaubt** (Phase-Head §0.3
verbatim):

- `phase5_ui/webui/static/{app.css, app.html, app.js, tree.js}` — erlaubt
  (Arbeitsfläche der Phase; JS-Dateien sind nicht in der Tabu-Liste)
- `phase5_ui/tests/test_static_routes.py` — erlaubt (Tests)

Keine `phase1_storage/storage/**`-, `phase4_auth/authserver/**`-,
`phase2_mcp/mcpserver/**`-Berührung; keine
`phase5_ui/webui/{security,api,serializers,permissions}.py`-Berührung.
**Tabu-Diff bleibt leer.**

```bash
# Verifikations-Befehl am Step-Ende (Phase-Head §0.3 verbatim):
git diff --stat -- phase1_storage/storage phase4_auth/authserver \
  phase2_mcp/mcpserver phase5_ui/webui/security.py \
  phase5_ui/webui/api.py phase5_ui/webui/serializers.py \
  phase5_ui/webui/permissions.py
# Erwartete Ausgabe: leer
```

## Erwartete Kennzahlen nach Bau

- **pytest:** 991 unverändert (3 Wächter umgeschrieben / neu, kein Test
  umbenannt; ein Test ggf. ersetzt)
- **ui_budget:** 5/5 im Korridor (app.css voraussichtlich +1–2 KB roh für
  die neuen Media-Query-Regeln)
- **Tabu-Diff §0.3:** leer (Verifikations-Befehl oben)
- **`node --check`** auf `app.js`, `editor.js`, `tree.js` ✅
- **Commits:** ein atomarer Block, ein Commit nach Bau + Verifikation
- **Doku:** Phase-Head Session-Block rotiert (dieser Eintrag wandert nach
  `SESSIONS_ARCHIVE.md` sobald H-R-3 abgeschlossen ist), `docs/INDEX.md`-
  Zeile für die neuen Screenshots nachgezogen, ROADMAP-Absatz aktualisiert
- **Screenshots:** 4–5 neue Selbst-Screenshots als
  `docs/screenshots/p86_block_h_r_3_{01..05}_*.png` + Symlinks in
  `screenshots_latest/`. Empfohlene Auswahl:
  - `01_1440_editor_open.png` — Editor im Detail-Slot bei 1440 px, **mit
    Klärung der H-R.8-Lesart im Klartext** (entweder Listen-Slot weg oder
    Items statt Übersicht)
  - `02_1440_editor_open_no_list.png` (nur bei Lesart b) — gleicher Viewport,
    aber Listen-Slot leer/weg
  - `03_1024_list_only.png` — bei 1024 px nur Navbar + Liste, **kein
    Map-Slot** (H-R.6 Fix sichtbar)
  - `04_1024_editor_fullview.png` — bei 1024 px Editor füllt 100vw×100vh,
    Navbar + Liste + Karte weg (H-R.7 Fix sichtbar)
  - `05_1200_editor_open.png` — bei 1200 px wie 1440 (Verhalten
    unverändert; Kontrolle, dass H-R.7 nicht versehentlich auch bei 1200
    greift)

## Empfohlene Reihenfolge (P8.6-AH nach diesem Escalation-Report)

```
G ✅ → G-R ✅ → H ✅ → H-R-Teil-1 ✅ → H-R-Teil-2 ✅ →
[Klärung der zwei Fragen mit dem Nikinger] →
H-R-3 ⬜ (Mini-Plan, drei Locks H-R.6/H-R.7/H-R.8) →
J ⬜ (pytest-Flake, datierte Tabu-Ausnahme phase4_auth/authserver) →
Gate ⬜ (Wegwerf + Smoke + Nikinger-Sichtprüfung, diesmal mit Claude Code) →
Z ⬜ (Closeout)
```

## Empfehlung Modellwahl (für die Claude-Code-Session)

**Sonnet 4.5** ist die Standard-Empfehlung — Workhorse für UI-Revisionen,
gutes Preis-Leistungs-Verhältnis, ausreichend für die CSS/JS-Touches +
Lock-Definition + Wächter-Bau. **Opus 4.1** ist die vorsichtigere Wahl,
wenn die Lock-Definition selbst nochmal gründlich deliberiert werden soll
(höhere Reasoning-Tiefe für „was wenn der Nikinger in der nächsten
Sichtung wieder etwas umwirft"-Szenarien); Aufpreis ~5×, lohnt sich für
eine Planungs-Session, nicht zwingend für den Bau. **Haiku 4.5** ist zu
dünn für UI-Architektur-Diskussionen mit Pixel-Befund-Bezug — nicht
empfohlen.

## Referenzen

- **Phase-Head:** `phase8_6_ui_polish/CLAUDE.md` (Modul-Status Zeile 14
  = H-R; aktuelle Session-Blöcke rotiert nach `SESSIONS_ARCHIVE.md`; die
  fünf Sub-Blöcke H-R.1/.2/.3/.4/.5 sind alle ✅; Tailscaled-Watchdog
  in §Vormerkungen; Phase bleibt 🔄, nicht ausgeliefert, v3.0.1 / 6f19a8f
  live)
- **Plan 2 (Lock-Liste, Locks P8.6-W–P8.6-AL):** `docs/concepts/phase8_6_ui_polish_plan2.md`
- **H-R-Plan (vorhanden, fünf Sub-Blöcke bereits gebaut):**
  `docs/concepts/phase8_6_ui_polish_block_h_r_plan.md`
- **Screenshots, die diese Befunde ausgelöst haben:**
  `screenshots_latest/{01..05}_*.png` (Symlinks) bzw.
  `docs/screenshots/p86_block_h_r_{01..05}_*.png` (Originale)
- **V-vision-befund 2026-09-11** (warum M3 nicht der richtige Adressat
  für Pixel-Befunde ist): `docs/concepts/sichtpruefung_automation_tooling.md`
  §Messbefund
- **Härte Regeln dieser Phase (P8.6):** Phase-Head §0.3 Tabu-Liste +
  §0.5 Selbstprüf-Checkliste + §0.5.7 kein Service-Touch — alle
  unverändert gültig
- **Hard Rules Wurzel:** Hard Rule 1 (keine Secrets), Hard Rule 8
  (Commit ⇒ Doku-Update im selben Commit), Hard Rule 9 (kein `pkill -f`,
  kein Service-Touch durch M3/Claude Code) — alle gelten weiter
