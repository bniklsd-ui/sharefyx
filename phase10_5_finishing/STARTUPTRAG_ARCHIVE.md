---
status: archive
purpose: L3-Archiv der Startaufträge der Blöcke 7 (Darstellung) und 9 (Rechte und Namen) — verbatim aus dem Phase-Head verschoben, weil der Head über dem Softcap stand.
read-when: wenn die Schritte 7.4–7.7 oder 9.2/9.3 gebaut werden — hier stehen die Korrekturen zum 📕-Plan, die dort fehlen, und die Ankündigung der drei P1-Öffnungen
detail: L3
up: ../ROADMAP.md
down:
  - CLAUDE.md                                          # der Phase-Head, aus dem die Abschnitte verschoben wurden
  - ../docs/concepts/phase10_5_finishing_plan.md       # 📕 der Plan (Schritte 7.4–7.7 wortgleich, aber ohne die Korrekturen)
updated: 2026-10-24 (der Startauftrag von Block 9 — die Ankündigung der drei P1-Öffnungen — ist aus dem Head hierher gewandert; der Head stand bei 43.545 B und damit über dem Softcap) | 2026-10-23 (aus dem Phase-Head verschoben: der Head stand bei 41.847 B und damit über dem Softcap; die Schritte 7.4–7.7 stehen hier weiter)
---
# Startauftrag-Archiv — die Blöcke 7 (Darstellung) und 9 (Rechte und Namen)

> **Warum dieses Archiv existiert (2026-10-23).** Der Phase-Head war beim Bau von Block 7.3
> auf **41.847 B** gewachsen — über dem Softcap (40.960 B), damit `doc_health` rot und das
> Deploy-Gate zu. Der Head nannte den Hebel selbst: der „Startauftrag" (5,8 KB) wandert nach
> Block 7 ins L3-Archiv. Er ist **hierher** gewandert, **verbatim** (`scripts/move_sections.py`).
>
> **Was noch offen ist:** **nichts mehr im Bau** — Schritt **7.4** ist am 2026-10-24 umgesetzt
> (die vier Posten der Sichtung; **P10.5-32 wartet auf die Bestätigung des Nikingers**). **7.1 bis 7.3
> sind gebaut und gemergt, 7.5 bis 7.7 gebaut (2026-10-24)** (deren Abnahmestand steht in der
> Abnahmetabelle des Heads).
>
> **Zwei Korrekturen gegen den 📕-Plan stehen nur hier** (der Plan ist ein Snapshot und wird
> nicht geändert): `--caution` ist der **Text**-Farbwert, nicht die Knopffläche (Schritt 7.5) ·
> `_items_get` steht in `api.py:932`, nicht 821 (Schritt 7.6). Wer die Schritte baut, liest
> **diese** Datei, nicht den Plan.

## Startauftrag — Block 7 (Darstellung: UI-1–UI-6, KA-5) · Ausführer

*Stand 2026-10-22, nach Block 6. Die Schritte stehen wortgleich im Plan (📕
`docs/concepts/phase10_5_finishing_plan.md` §Block 7, Zeilen 685–735); **hier stehen die heute
geprüften Anker** — der Plan nennt vier Zeilen, die inzwischen gedriftet sind (siehe „Drift").*

**Vorher (Block-Start, Plan §2.1):** `limit.context` ≤ 400.000 prüfen (`opencode.json`:
`MiniMax-M3.1-Flash` → 400000 ✓) · `git status` sauber · Blockbasis = HEAD · **erlaubte Pfade**
(Plan §3): `phase5_ui/webui/**`, `phase2_mcp/mcpserver/app.py` (**eine** Route), Tests.
**Proben laufen an der Wegwerf-Instanz** (Freigabe vom 2026-10-22): eigener Port, tmp-`DATA_ROOT`,
tmp-`auth.sqlite3`, Playwright aus `~/.claude-code-tools/e2e-venv` — **nicht** gegen den laufenden
Dienst.

**Schritte (in dieser Reihenfolge):**

1. **7.1 UI-1 — HTML-404.** ✅ **2026-10-23** (Branch `p105-block7`, nicht gemergt) — `phase5_ui/webui/pages.py`: neu `render_not_found_page()` über
   `_page(title="Nicht gefunden", body=…)` (**`_page` steht heute in `pages.py:49`**), Text „Diese
   Seite gibt es nicht." + Link „Zur Übersicht" (`/ui/`). Route `Route("/ui/{rest:path}", …,
   methods=["GET"])` in `mcpserver/app.py` **nach** allen `/ui`-Routen (nach `api_routes(...)`) —
   sonst überdeckt der Fänger `account_routes`. Status 404, `Cache-Control: no-store`;
   `/ui/static/<fehlt>` bleibt Klartext (`static_routes.py:86`), API und `/mcp` bleiben JSON.
   Tests: `test_static_routes.py` — `test_unknown_ui_path_renders_html_404`,
   `test_known_ui_routes_win_over_the_catch_all` (login/invite/account),
   `test_missing_static_file_stays_plain_text`, `test_api_404_stays_json`.
2. **7.2 UI-2 — Logo (D-6, Variante B „Überlagert").** ✅ **2026-10-23** — `docs/concepts/phase10_logo_entwuerfe_final.svg`
   → **eine** Datei `phase5_ui/webui/static/logo.svg` (der einzige Austauschpunkt); Farben als
   `currentColor` bzw. über `--select-fill`/`--select-line`, sonst stimmt der Dunkelmodus nicht.
   Marke „S" + „harefyx": `static/app.html:20` (heute `<div class="rail__brand">sharefyx<span
   class="rail__version">v3.1.4</span></div>` — **das `brand__mark`-`<img>` fehlt noch**) und
   `pages.py` (Login-/Fehlerseite). Favicon: `<link rel="icon" type="image/svg+xml"
   href="/ui/static/logo.svg">` in `app.html` **und** `_page` (`pages.py:39`) — `[VERIFY V215]`
   Safari. Test: `test_pages_markup.py::test_brand_uses_the_single_logo_file` (beide Stellen auf
   dieselbe Datei).
3. **7.3 UI-3 — Tab-Titel je Ansicht (V120, D-5 deutsch).** ✅ **2026-10-23** — **`setViewTitle()` existiert heute
   nicht** (`document.title` steht nur statisch in `app.html:6`) — das ist eine **Bau-Aufgabe**, kein
   Verdrahtungs-Fix. `state.js`: `export function setViewTitle(part) { document.title = part ?
   part + " · sharefyx" : "sharefyx"; }`. Aufrufe: Übersicht (`editor.js:59 showOverviewPane`)
   „Übersicht", Space-Liste = Space-Name, Item (`editor.js:469 loadEditorFromItem`) = Titel, Karte
   (`graph.js:186 loadGraph`) „Karte", Einstellungen „Einstellungen".
4. **7.4 UI-4 — Sichtung, dann Fix.** **Nicht der Ausführer:** Claude Code macht die Screenshots
   der acht Hauptansichten (Konventionen: `docs/concepts/sichtpruefung_automation_conventions.md`),
   der Nikinger liefert daraus **höchstens 10** Posten, der Ausführer setzt sie in `app.css` um
   (Auswahl-Konvention v3, `phase8_ui_graph/CLAUDE.md`). Alles über 10 Posten wandert nach P11.
   **Screenshots gemacht 2026-10-24** (acht Ansichten, Wegwerf-Instanz mit 5 Beispiel-Items; liegen
   nur in `/tmp/opencode/sichtung-7-4/`, nicht im Repo). **Sichtungsliste des Nikingers (4 von 10 Posten,
   für den Ausführer, nur `app.css`/Markup):**
   1. **Wortmarke:** der Abstand zwischen Logo-Zeichen und „harefyx" wird **kleiner** (`.rail__brand`
      `app.css:456` und `.auth__brand`; das Zeichen **ist** das S — `app.html:21` `alt="S"`).
   2. **„Zugewiesen"-Auswahl** (`#list-assignee`, 7.6): Innenabstand/Breite wie das Suchfeld darüber
      angleichen — sie läuft bündig an den Listenrand.
   3. **Update-Banner** verdeckt oben ~140 px jeder angemeldeten Ansicht und schiebt das Layout: **kompakter**
      machen (Nikinger: echter Mangel; Form ist Sache des Ausführers, Vorschlag mit Begründung).
   4. **Versionsanzeige** `.rail__version` (`app.css:476`) liest sich als „v316" — Punkte nicht erkennbar
      (Quelle ist `v3.1.6`): Schriftgröße/Laufweite prüfen (Nikinger: echter Mangel).
   **Nachsichtung:** der Nikinger macht eine **zweite Sichtung der Gestaltung**, sobald der
   Alles-in-einem-Editor (Block 11) steht — weitere Posten bis zur Grenze 10 kommen dann dazu.
   **✅ 2026-10-24 — der Ausführer hat alle vier Posten umgesetzt** (Wächter
   `phase10_5_finishing/tests/test_sichtung_7_4.py`, 8 Tests mit **4 Gegenproben**; Probe
   `phase10_5_finishing/probes/p105_b7_sichtung_probe.py` an der Wegwerf-Instanz **18793**:
   **5/5 Kriterien**, **5 Gegenläufe** rot). **Gemessen:** (1) Abstand **2,5 px** (vorher 5,6 px;
   `.45em` → `.2em`, eine Klasse für Rail **und** Anmeldeseite) · (2) die Auswahl trägt jetzt die
   Kanten der Suchzeile (**0 px** Versatz links wie rechts) · (3) der Banner ist eine **einzeilige
   Leiste (49 px statt ~140 px)**: Schlagzeile (erste Zeile des Eintrags) + Knopf **„Alle
   Änderungen"**, der den Update-Log in den Einstellungen öffnet (gemessen: 20 Einträge sichtbar) ·
   (4) die Versionsanzeige ist 11 px mit `.03em` Laufweite — der hellste Pixel des Punktes steigt
   von **155/255 auf 203/255** (bei 9 px verblasste er in den Grund: das ist der Befund „v316").
   **Befund für den Nikinger:** ein *quadratischer* Punkt braucht in dieser Schrift **13 px** — größer
   als die Wortmarke (12,5 px). Eine eigene Schriftart (Monospace) für die Version würde es runden,
   **widerspricht aber der gelockten Entscheidung P6 vom 2026-08-13** („keine eigene Schriftart").
   **P10.5-32 bleibt ⬜**, bis der Nikinger die Umsetzung bestätigt.
5. **7.5 UI-5 — Kontrast (D-7).** ✅ **2026-10-24** — **Drift gegen den Plan:** im Code ist `--caution` **selbst der
   Text-Farbwert** (`app.css:92`: `--caution: var(--danger)`), nicht die Knopffläche — der Plan
   spricht von einem „neuen Token `--caution-text` (heller als `--caution`)". **Der Code gewinnt:**
   Ziel ist ein **hellerer Text** auf der Standardfläche, ohne eine eigene Flächen-Familie
   (`--caution-std-*` wäre ausgeschlossen, P9-B17). Wächter
   `phase10_5_finishing/tests/test_contrast.py::test_caution_text_meets_wcag_aa()`: liest die
   Token-Werte aus `app.css`, rechnet WCAG gegen den Knopfhintergrund, ≥ 4,5:1 — das alte Token
   liefert **4,38:1** (Gegenlauf: rot).
6. **7.6 UI-6 — Assignee-Filter.** ✅ **2026-10-24** — `phase5_ui/webui/api.py:932 _items_get` (Plan sagt 821 —
   **Drift**) nimmt `assignee=<space>` an und filtert **im Adapter** (`i.assignee == value`), **vor**
   der Paginierung; `ItemSummary.assignee` existiert (`storage/models.py:90`). UI: Auswahl
   „Zugewiesen" in der Listenkopfzeile (`list.js:56` `<header class="list__head" id="list-head">`)
   mit den Spaces aus `state.spaces` + „alle". Tests: `test_api.py::test_items_filter_by_assignee`,
   `test_items_assignee_filter_respects_acl`.
7. **7.7 KA-5 — `doing` hervorheben.** ✅ **2026-10-24** — Übersicht: der Eimer „In Arbeit" bekommt die Akzentklasse
   (`app.css`; die Eimer kommen generisch aus `meta.buckets` — `static/js/app.js:371`) · Karte:
   `doing`-Knoten tragen einen statischen Akzentring, **ohne** Animation.

**Vier Drifts zwischen Plan und Code (Korrektur im Plan wäre eine 📕-Änderung — hier festgehalten,
der Code gewinnt):** `_items_get` steht heute in `api.py:932` (Plan 821) · `showOverviewPane` in
`editor.js:59` (Plan 56) · `loadEditorFromItem` in `editor.js:469` (Plan 466) · `loadGraph` in
`graph.js:186` (Plan 182). Dazu die zwei Sachbefunde: `--caution` ist der **Text**-Farbwert (Plan
liest es als Fläche) und `setViewTitle` **existiert noch nicht**.

**Abnahme (Plan §Block 7):** 10-29 (404-Seite) · 10-30 (Logo + Favicon aus einer Datei) · 10-31
(Titel je Ansicht) · 10-32 (Sichtungsliste, **beim Nikinger**) · 10-33 (Kontrast ≥ 4,5:1) · 10-34
(Filter in API und UI) · 10-35 (KA-5 sichtbar). **Proben:** Playwright liest `document.title` je
Ansicht; Screenshots für 10-30/10-32/10-35; **Wegwerf statt Live** (Freigabe 2026-10-22).

## Startauftrag — Block 9 (Rechte und Namen: RE-7, RE-4, RE-3) · Ausführer
> **Ankündigung der drei P1-Öffnungen** (Plan §Block 9: „Ankündigung im Phase-Head vor dem ersten
> Commit mit den drei Öffnungen und den betroffenen Dateien"). Der 📕-Plan bleibt ein Snapshot; die
> Herleitung steht in `docs/concepts/phase10_5_finishing_plan.md` §„Block 9".
>
> **Die drei Öffnungen** (elfte, zwölfte, dreizehnte P1-Contract-Öffnung; die elfte war P9-F
> `assignee`):
> 1. **(12) RE-7 `created_by`** — `Item.created_by` / `ItemSummary.created_by`, wie `updated_by`
>    (P9 Block trace): vom Server gesetzt, **über keinen Kanal setzbar**, **kein Backfill**
>    (P10.5-W): ein Altbestand-Item ohne Feld bleibt ohne Feld, und ein leeres Feld wird **nie**
>    erfunden. Kein Index-Schema-Sprung (wie `updated_by`).
> 2. **(13) RE-4 `Store.rename_folder()`** — Ordner stehen **nicht** im Frontmatter (P6 Step 4),
>    also wird **keine Item-Datei umgeschrieben** und **keine `version` erhöht**. Die
>    `.share.yml` im Ordner **wandert mit** (das ist der Fund aus P8.6 §0.4.1: die billige
>    Frontend-Fassung ließ sie zurück).
> 3. **(14) RE-3 `Store.rename_space()`** — `space` steht **im Frontmatter** jeder Datei, also
>    gilt die Semantik von `move()`: jede Item-Datei des Spaces bekommt `space=new`,
>    `version+1`, `updated=now` — **ein** Commit für den ganzen Space. **Nur Team-Spaces**
>    (P10.5-M): ein Home-Space-Name ist Identität (Auth-DB, Token-Familien, `assignee`,
>    `updated_by`) und wird in P10.5 nie umbenannt.
>
> **Betroffene Dateien in `phase1_storage/storage/`:** `models.py` und `store.py`. `index.py`
> **bleibt unberührt** — die Index-Zeilen werden über das bestehende `index.row_from_file()` /
> `index.upsert_item()` nachgezogen, es gibt **keinen** Schema-Sprung (Hard Rule 2: der Index
> ist Ableitung, kein Ort für eigene Wahrheiten). Das ist eine **Teilmenge** der angekündigten
> Liste (`models.py`, `store.py`, `index.py`) — zulässig, denn das Abbruchkriterium ist „nur die
> angekündigten Dateien", nicht „alle angekündigten Dateien".
>
> **Abbruchprüfung am Blockende (P10.5-E/F):** `git diff --stat <block-basis>..HEAD -- . ':!<erlaubte Pfade>'`
> muss leer sein (außer `.md`-Doku) und `git diff --stat -- phase1_storage/storage` darf **nur**
> `models.py` und `store.py` nennen. Erlaubte Pfade (Plan §3, Block 9): `phase1_storage/storage/{models,store,index}.py`,
> `phase2_mcp/mcpserver/tools.py`, `phase5_ui/webui/**`, Tests.
>
> **Wichtig für die Reihenfolge:** `deploy.sh` klont das **lokale `main`**. Block 9 wird deshalb auf
> einem eigenen Branch (`p105-block9`) gebaut und **erst nach dem Deploy C** nach `main` gemergt —
> sonst liefert `v3.1.7` den Block-9-Stand mit aus.

## Startauftrag — Block 7 (Darstellung: UI-1–UI-6, KA-5) · Ausführer
> **Gebaut** (7.1–7.7, 2026-10-23/24) · die ausführliche Fassung und die **zwei Korrekturen gegen den
> 📕-Plan** stehen in `STARTUPTRAG_ARCHIVE.md`. **P10.5-32 bleibt ⬜ bis zur Bestätigung des
> Nikingers**; nichts davon ist deployed — `v3.1.7` steht aus.


## Startauftrag — Block 9 (Rechte und Namen: RE-7, RE-4, RE-3) · Ausführer
> **Gebaut** (9.1–9.3, 2026-10-24) · die ausführliche **Ankündigung der drei P1-Öffnungen**
> (12) RE-7 `created_by` · (13) RE-4 `Store.rename_folder()` · (14) RE-3 `Store.rename_space()`
> — steht verbatim in `STARTUPTRAG_ARCHIVE.md`. **P10.5-41/42/43/44 ✅.** Der Branch `p105-block9`
> wird **erst nach dem Deploy C** nach `main` gemergt (`deploy.sh` klont das lokale `main` —
> sonst liefert `v3.1.7` den Block-9-Stand mit aus).
