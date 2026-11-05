---
status: live
purpose: Plan Editor 4.1.0 („der neue Editor“) — Auslöser: GFM-Tabellen erscheinen im Live-Editor als Rohtext. Befunde am Code und im Browser (Wegwerf-Instanz), Architektur (CM5-Hybrid + marked als eine Darstellungs-Wahrheit), Verträge (Byte-Stabilität, Sanitizer), Schritte S0–S11, Abnahmezeilen, Darstellungs-Gate, Entscheidungen E1–E12, [VERIFY]-Liste. Nichts gebaut.
read-when: vor jedem Schritt von Editor 4.1 — zuerst BLUF, §1, §8 (Entscheidungen), dann den Schritt in §5 und seine Verträge in §4
detail: L2
up: ../../phase10_5_finishing/CLAUDE.md
down:
  - ./phase10_5_editor_4_1_plan_anhang.md   # 📗 Messtabellen, Prototyp, Konstrukt×Fläche-Matrix, Bibliotheksgrößen, Korrekturen H1–H4
  - ./phase10_5_block18_live_fixes_plan.md  # 📗 Vorbild für Form und Proben-Muster
  - ../../phase10_inventory/messung/M7_editor.md  # 📗 Herkunft der CM5-Wahl (Block 11)
updated: 2026-11-05 (§8: E1–E3, E5 entschieden, E10 beantwortet, Tag-Zählung) | 2026-11-03 (angelegt — Opus-Planungsagent; Messungen an drei Wegwerf-Instanzen, Chromium 151 + Firefox 153; nichts gebaut, kein Commit)
---
# Editor 4.1.0 — der neue Editor (Plan)

> **Auftrag (Nikinger, 2026-11-03, sinngemäß):** Tabellen erscheinen im v4.0-Live-Editor als `|`-Rohtext — „pretty
> important". Kein Flicken: der **ganze neue Editor als `v4.1.0`**. Keine Datei darf Nacharbeit brauchen; gespeichert wird
> weiter reines Markdown + YAML-Frontmatter; Darstellung ist eine **Sicht**. Später (nicht 4.1): Kommentare,
> Änderungsverfolgung, verbundene Zellen, Bildgröße/Bildunterschrift.

## BLUF

1. **Reproduziert** (Wegwerf, Bild im Anhang A10): der eigene Editor zeigt Tabellen als Rohtext, die Lesesicht eines
   fremden Items rendert dieselbe Tabelle. Ursache: seit `0cf72a1` (Block 11.3) hat der **eigene** Editor keinen
   Darstellungsweg mehr — `markdownToHtml()` läuft nur für fremde Items (`editor.js:793`) und das Update-Log
   (`updates.js:41/67`). Block 11/13 haben ohne Tabelle als Sichtkriterium abgenommen (Lücke im Maß, Head „Offen").
2. **Laut, gegen die Erwartung:** `markdown.js` besteht nur **164 von 544** GFM-Spec-Beispielen der Abschnitte, die
   der Bestand braucht (30 %); **marked 18.1.3** (MIT, 14,9 KB gz) besteht **535/544** (98 %). „`markdown.js`
   erweitern" ist deshalb der falsche Weg — **den Parser ersetzen, den Sanitizer behalten** (§3, E2).
3. **Zwei Live-Fehler im Entwurfsschutz** (unabhängig von Tabellen, gemessen): ein getippter Entwurf geht nach
   Neuladen verloren, wenn zuerst ein anderes Item geöffnet wird; ein bloß geöffnetes Item bietet nach einer fremden
   Änderung „Wiederherstellen?" an — Wiederherstellen + Strg+S setzt die KI-Änderung **still** zurück (v3 trägt den
   alten Text) — clientseitiges Last-Write-Wins (Geist von Hard Rule 3) → erster Schnitt.
4. **CRLF normalisiert der Server, nicht CM5** (`store.py:412/482/771` `read_text`): Öffnen ist byte-stabil
   **gegenüber dem API-Body**; der erste Write *jedes* Clients macht eine CRLF-Datei ganz zu LF. Der Kommentar
   `frontmatter.py:18-20` und die B20-Zeile im Phase-1-Head behaupten anderes (Doku-Fix, E6). Bestand: 0 CRLF.
5. **Editor heute, gemessen:** Listen ohne Spiegelstrich/Nummer, Ebene 3 und Inline-HTML mit **1,7–3,3 : 1**
   Kontrast, Tab fügt `\t` ein, Enter setzt keine Liste fort, Strg+F sieht ~30 von 2005 Zeilen.
6. **Architektur:** bei **CM5** bleiben, Tabellen als Widget (Prototyp gemessen: Klick → Zelle exakt, Undo/Redo,
   Kopieren = Quelle, **+0,4–0,9 ms** je Taste, 200-Zeilen-Tabelle in 10 ms gezeichnet). CM6 kostet **+40 KB gz** und
   einen Bündel-Schritt, ohne gemessenen Bedarf.
7. **Kleinster Schnitt:** `v4.0.2` = S0–S2 + Release S2R (Probe, Entwurf, Tabellen-Widget mit dem heutigen Renderer),
   vier Sitzungen. Voller `v4.1.0` = S3a–S11. **Größtes Risiko:** der Umbau der Sicherheitskette (Vor-Escaping → HTML-Token als
   Text) — zwei Testschichten mit je eigenem Gegenlauf (§4.3).

## 1. Was der Ausführer wissen muss

- **Code ist die Wahrheit.** Jeder Befund in §2 ist am Code gelesen **und** an einer Wegwerf-Instanz gemessen
  (Messgerät: Anhang A1). Weicht der Code beim Bauen ab, gilt der Code — datierte Notiz in den Plan.
- **Nur Wegwerf** (Root-`CLAUDE.md`, Working style): eigener Port, tmp-`DATA_ROOT`/`auth.sqlite3`/DEK, TLS selbstsigniert,
  Umgebung ohne `SHAREFYX_*`/`SFX_*`/`SPACE_*`, Stopp nur über die PID-Datei (Hard Rule 9). Muster:
  `probes/p105_b14_layout_probe.py` (`_setup`/`_serve`/`_stop`, Kopie der statischen Dateien) und
  `probes/p105_b11_roundtrip_probe.py`. Playwright aus `~/.claude-code-tools/e2e-venv`;
  `add_init_script("localStorage.setItem('sfx:film:gesehen','4.0.0')")`, sonst frisst das Film-Startbild die Klicks.
- **Gegenläufe** patchen eine **Kopie** der statischen Dateien (`STATIC_DIR`), nie den Arbeitsbaum; jeder Anker muss
  **genau einmal** vorkommen (Falle aus 18.2b: ein doppelter Anker beißt still nicht). Ein zahnloser Gegenlauf wird für die
  neue Szene neu gebaut (Memory „honest counter-runs").
- **Kein Server-Code**, außer E6/E9 werden ausdrücklich so entschieden. Kein LLM, kein „Verstehen" — alles Rendern
  läuft im Browser (P5-Y).
- **Kein Build-Schritt** (P5-T): Bibliotheken werden als **die Datei vendort, die das npm-Paket ausliefert**
  (SHA-256, Lizenz, Quelle in `phase5_ui/THIRD_PARTY_LICENSES.md`, wie CM5 in 11.1). Kein Bundler, keine CDN-Laufzeit.
- **CSP bleibt** (`webui/security.py:46-50`, `style-src 'self'`): keine `style=`-Attribute/`<style>` im Markup; Farben und
  Größen nur über Klassen; CSSOM aus JS ist erlaubt (so arbeitet CM5 heute schon).
- **Budget-Regel** (§4.4): neuer Editor-Code liegt in `js/editor/*.js` und wird **nur per `import()`** geladen.
- **Ausführer:** CSS-lastige Schritte (S4, S5a) besser Claude Code (Memory: Kaskaden-Ursachen sind die bekannte
  Schwäche des opencode-Ausführers); die übrigen kann opencode bauen. Jede Sitzung = ein Schritt.
- **Tests:** pytest-Wächter (statisch, gemockt, kein Netz) + Playwright-Proben an der Wegwerf-Instanz; volle Suite nur am
  Schrittende. Bestehende Wächter, die heutiges Verhalten festnageln und **mit Absicht** geändert werden:
  `test_editor_format.py::test_the_inline_rule_comes_before_the_links` (Ursache von F4c),
  `test_static_routes.py::test_markdown_link_regex_allows_escaped_brackets` (Regex-Text → wird Probe-Zelle),
  `test_editor_cm.py::test_the_script_list_matches_the_vendor_directory` (neue Addons → `VENDOR_SCRIPTS`).

## 2. Befunde am Code (`main@a22620d`, gemessen 2026-11-03)

| # | Ort | Befund (gemessen) | Folge |
|---|---|---|---|
| F1 | `editor.js:793`, `updates.js:41/67`; `0cf72a1` | `markdownToHtml()` läuft nur für **fremde** Items und das Update-Log; der eigene Editor (CM5, `editor.js:512-518`) hat keinen Darstellungsweg | der Tabellen-Fehler; jede Darstellung eigener Notizen fehlt |
| F2 | `markdown.js:203-374` | GFM-Spec-Beispiele (544, Abschnitte der Teilmenge, kanonischer DOM-Vergleich): **164 ✅**; marked 18.1.3: **535 ✅** (Anhang A3) | Erweitern heißt einen CommonMark-Parser schreiben (Hervorhebung allein: 59/131) |
| F3 | `markdown.js:172-177, 278-302, 304, 313-369` | gemessen falsch: verschachtelte Listen werden Absätze „- verschachtelt A - …"; `\|` teilt die Zelle; zeilenlose Fortsetzung, Kopf/Trenner-Zahl, ungleiche Zeilen weichen von GFM Ex. 202–204 ab; Tabelle im Zitat = Rohtext; h5/h6, Setext, Tilde-/Einzugs-Code = Absatz; `* * *` → `<ul><li><em> </em>`; verschachteltes Zitat zeigt `>`; `~~x~~`, Fußnoten, harte Umbrüche, Inline-HTML wörtlich | KI-geschriebene Notizen (Tabellen 84, Aufgaben 66, Zäune 53, verschachtelte Listen 45, `~~` 31 Dateien) zeigen falsch |
| F4 | `editor.js:435-495, 477, 585`; `markdown.js:152/160/167, 335` | Editor ↔ Lesesicht widersprechen sich: **(a)** `::: {.warnung}`-Zeilen im Editor unsichtbar, in der Lesesicht wörtlich; **(b)** der Overlay färbt `[x]{.rot}` **im** Codespan; **(c)** `![[alt]{.rot}](asset:…)` zerstört das **Bild** in beiden Sichten (`!` + Link ohne `href`); **(d)** `- [x]{.rot} …`: Kästchen + `{.rot}` im Editor versteckt, in der Lesesicht Kästchen + „{.rot} …" (GFM verlangt Leerraum nach `]`); **(e)** `1. [ ]`: Klammern versteckt, kein Kästchen; **(f)** Setext-Linie, Tilde-/Einzugs-Code: Editor erkennt, Lesesicht nicht | „eine Wahrheit" (§4.1) |
| F5 | `app.css:2099` | `.cm-formatting {visibility:hidden}` trifft auch `cm-formatting-list` → **keine** Spiegelstriche/Nummern außerhalb der Cursorzeile (Bild A10) | Listen sehen aus wie eingerückter Text |
| F6 | vendortes `codemirror.min.css` | `.cm-s-default .cm-keyword #708` (3. Listenebene) **1,94 : 1**; Inline-HTML über den xml-Modus: `cm-attribute` **1,70**, `cm-string` **2,54**, `cm-tag` **3,32** auf `--editor-bg #0C1017` | WCAG 4,5 : 1 verfehlt (Anhang A9) |
| F7 | `editor.js:519, 566-569, 358-361, 827 vor 835` | **(a)** `setValue` feuert `change` → `saveDraft()`: jedes Öffnen schreibt einen „Entwurf"; ist CM schon geladen, überschreibt das Öffnen einen echten Entwurf, **bevor** `loadDraftIfAny()` ihn liest (gemessen: getippter Text nach Neuladen weg). **(b)** der Entwurf trägt keine Basisversion → nach fremder Änderung „Wiederherstellen?" → Strg+S speichert den alten Text als v3 | Datenverlust; stilles Zurücksetzen fremder Writes |
| F8 | `store.py:412/482/771`; `files.py:460`; `frontmatter.py:18-20` | Öffnen ändert nie Bytes (16 Korpus-Items × 2 Browser: Editor = API-Body, nicht geändert, Speichern aus, Strg+S = 0 Requests, Tippen+Löschen = sauber). **Aber:** `read_text()` übersetzt CR/CRLF → der API-Body hat nie CR; jeder Write schreibt LF (CRLF-Datei: 6 CR → 0 nach einem Zeichen). Erster UI-Write ergänzt `format: markdown` + `updated_by` | Byte-Vertrag gilt gegen den **API-Body** (§4.2); Doku-Fix E6 |
| F9 | CM5-Voreinstellung | Tab fügt ein **`\t`** ein (Umschalt+Tab: nichts); Enter setzt Listen nicht fort; Strg+B/I/K tun nichts; Einfügen ist reiner Text (Textarea-Eingabe) — **sicher** | §5 S7 |
| F10 | `editor.js:517` (`viewportMargin: 20`) | in einer 2005-Zeilen-Notiz stehen ~30 Zeilen im DOM → Strg+F des Browsers findet den Rest nicht | Suchen im Editor ist Pflicht (S8) |
| F11 | `app.css:1981-1998, 2022-2062, 1509-1558` | die 72ch-Grenze sitzt an der versteckten Textarea → CM läuft volle Breite; Editor Plex Mono 13 px/21 px, Lesesicht Plex Sans 16 px/1,6; Überschriften 1,3/1,18/1,08 em von 13 px gegen 22/18/16 px | ein typografisches System (S5a) |
| F12 | `fonts/*.woff2`, `build_font_subset_plex.sh:32` | **beide** Teilmengen ohne `←` `→` `✓` `✗` `●` `★`, ohne Rahmenzeichen (↑↓ vorhanden); Mono statisch 400 → fett/kursiv synthetisch | Pfeile aus KI-Notizen in Fremdschrift |
| F13 | `ui_budget.py:138-141`, `test_budget_coverage.py` | Erstaufruf **236,7/250 KB** (jede `js/*.js`, auch nur per `import()` geladene); nachgeladen **69,7/80 KB** (`vendor/**`); ein Unterordner `js/x/` steht in keiner Liste → Wächter rot | Regel §4.4, Entscheidung E3 |
| F14 | `app.html:365`, `editor.js:53/1024`, `app.css:1918` | tot im Produkt: `#editor-preview`, `editorPreviewEl`, `.toolbar-btn--wide`. **Nicht tot:** `setRawMode` (Aufrufer `editor.js:539/833`, drei Test-Assertions), `.glass` (P8-Smoke prüft es) | Aufräumen in S5a |

Korrekturen zu den Haiku-Hypothesen (Tab, `setRawMode`, CRLF, Pipe im Codespan, Kontrast): Anhang A11.

## 3. Architektur (Entscheidung mit Zahlen)

| Option | Editor | Renderer | gz nachgeladen (heute 69,7) | GFM-Teilmenge | Aufwand | Größtes Risiko |
|---|---|---|---|---|---|---|
| **A (empfohlen)** | CM5 5.65.16 + Tabellen-Widget (`markText` `replacedWith`) | **marked 18.1.3** vendort (ESM, lazy) + eigene Erweiterungen + **unser** Sanitizer | ≈ 69,7 + 14,9 + 2,2 (searchcursor) + ~10 eigene ≈ **97 KB** | **98 %** (535/544) | S0–S11 (mit S2R, S3a/b, S5a/b), ~15 Sitzungen | Widget-Semantik an Grenzen (IME, Mehrfachauswahl) — Pfeil/Klick/Undo/Kopieren gemessen ✅ |
| A′ | wie A | `markdown.js` selbst erweitert | ≈ 82 KB, aber +4–8 KB **Erstaufruf** (13,3 KB Luft) | heute 30 %; Ziel unbelegt | +2–3 Sitzungen Parser | endlose Randfälle; jede KI-Variante ein Fund |
| B | CM6 (state/view/commands/language/search + `@lezer/markdown`), **einmal offline gebündelt** | marked | **110,3 KB** nur Editor (mit `lang-markdown` **182,5**) → ≈ 135 KB | 98 % | +3–4 Sitzungen (Todo, Overlay, Format neu) | Bündel ist ein Build-Artefakt außerhalb des Repos; CSP-Verhalten von `style-mod` [VERIFY] |
| C | Lesen/Bearbeiten-Schalter für eigene Notizen | heutiger/marked | +~1 KB | wie Renderer | 1 Sitzung | bringt den Moduswechsel zurück, den der Nikinger entfernt hat (`0cf72a1`, `8aba4d4`) — nur Rückfall |

**Empfehlung A.** Der Prototyp (Anhang A4) hält in Chromium **und** Firefox: Text beim Öffnen unverändert, Klick auf
„Anzahl der Versuche" setzt den Cursor auf Zeile 5 / Spalte 14, ein getipptes Zeichen ändert **nur** diese Zelle,
Undo/Redo stimmen, `getSelection()` und Strg+A/Strg+C liefern die **Quelle**, Abgleich 0,2 ms, Taste 3,0 ms (Basis 2,6 ms). **Einziger
Fehlgriff:** Pfeil ↓ in die Tabelle landet am **Tabellenende** (CM rechnet die Zielspalte gegen die Widget-Zeile) — die
Korrektur ist ein `beforeCursorEnter`-Handler, der je nach Herkunft auf die erste/letzte Tabellenzeile setzt (S2).
CM6 wäre der bessere Editor für Mobilgeräte und Barrierefreiheit — beides ist nicht gefordert (P5-W Desktop zuerst) und
kostet 40 KB plus einen Bündel-Schritt. **Renderer:** marked statt Eigenbau, weil die Konformitätszahl (30 % → 98 %) die
Abnahmebedingung „keine Datei braucht Nacharbeit" erst messbar macht; der Sanitizer bleibt die letzte, unveränderte
Schranke. **Größtes Risiko von A:** CM5 ist im Wartungsmodus (letzte Version 2026-02-07, nur Modus-Fixes) — unser
Widget nutzt nur dokumentierte APIs (`markText`, `beforeCursorEnter`, `addLineClass`), die auch die Kästchen seit
Block 11.5 tragen.

## 4. Verträge

### 4.1 Eine Darstellungs-Wahrheit

- **Ein Parser:** marked 18.1.3 (`gfm: true`, `breaks: false`) liefert die Blockstruktur für **beide** Sichten.
  `js/markdown.js` bleibt die Fassade (gleiche Exporte, gleiche Importeure) und bekommt:
  `ensureRenderer(): Promise` (lädt `vendor/marked/marked.esm.js` per `import()`, einmal, gecacht),
  `markdownToHtml(src, {itemId, assetIds})` (nach `ensureRenderer()` synchron; vorher `null` → Aufrufer wartet),
  `blockRanges(src) → [{typ, von, bis}]` (Zeilenbereiche der **obersten** Tokens aus der Summe ihrer `raw`-Längen —
  gemessen 14/16 Korpus-Texte exakt; die zwei Abweichungen tragen CR, die der Server nie liefert, F8),
  `FORMAT_VOKABULAR` (unverändert die eine Quelle), `KATALOG` (Liste der unterstützten Konstrukte, §7).
- **Editor:** Widgets **nur** für oberste `table`-Tokens (Inhalt = `markdownToHtml()` desselben Quelltexts) und die
  bestehenden Kästchen; Zitat, Code, `:::` bekommen **Zeilenklassen** aus `blockRanges()`; der CM5-Modus färbt nur
  noch Quellzeilen. Eine Tabelle in einem Zitat bleibt im Editor Rohtext (Bestand: 1 Datei), in der Lesesicht Tabelle.
- **Unterstützte Teilmenge** (= `KATALOG`): Absätze, harte Umbrüche (zwei Leerzeichen/`\`), Überschriften h1–h6
  (ATX + Setext), Hervorhebung `*`/`_`/`**`/`__` nach GFM-Regeln, `~~durch~~`, Codespans, Zäune ```` ``` ````/`~~~`
  (Sprache wird ignoriert), eingerückter Code, Zitate (verschachtelt), Listen (verschachtelt, geordnet ab `n`),
  Aufgaben (auch in geordneten Listen, Leerraum nach `]` Pflicht), Tabellen (GFM Ex. 198–205), Trennlinien,
  Links/Bilder/Autolinks (GFM-Erweiterung), Backslash-Escapes, Fußnoten (eigene Minimal-Erweiterung, E7),
  Format-Konvention `[Text]{.rot .gross}` und `::: {.zentriert}` … `:::` (marked-Erweiterungen; Bild vor Format,
  Codespan schützt).
- **Bewusst wörtlich:** rohes HTML (Ausnahme nach E4), unbekannte `{.klasse}`/`:::`-Klassen (beide Sichten zeigen den
  Text, **keine** Zeile verschwindet), Mathe, Wiki-Links, Emoji-Kürzel.
- **Sichtbare Änderung durch GFM** (Bytes unberührt): Entitäten wie `&amp;`/`&nbsp;` erscheinen als Zeichen (heute
  wörtlich — gemessen: das Vor-Escaping machte `&amp;amp;` daraus), `- [x]{.rot}` ist kein Kästchen mehr (F4d).

### 4.2 Byte-Vertrag („keine Datei braucht Nacharbeit", messbar)

| # | Regel | gemessen heute |
|---|---|---|
| V1 | Öffnen schreibt nie; Editortext === API-Body (inkl. fehlendem Newline am Ende, Tabs, Doppel-Leerzeichen, BOM, U+2028) | ✅ 16/16, beide Browser |
| V2 | ohne echte Änderung kein Write: Speichern aus, Strg+S = 0 Requests, Tippen+Löschen = sauber | ✅ |
| V3 | ein Edit ändert im Body **nur** die editierten Zeichen; Tabellen-/Listen-Befehle ändern nur ihre Zeilen | ✅ (Prototyp: Zelle) |
| V4 | Rendern, Widgets, Öffnen polstern nie auf, nummerieren nie um; „Tabelle formatieren" nur als ausdrücklicher Befehl; keine Autokorrektur, Smart Quotes oder Klammerpaare (sie schrieben Zeichen, die niemand getippt hat) | Pflicht ab S2 |
| V5 | Zeilenenden: der Server liefert LF (F8); der Editor schreibt, was er bekommt; das Newline am Ende wird nie ergänzt/entfernt | ✅ |
| V6 | ein echter Write ändert im Frontmatter genau `updated`, `version`, `updated_by` und beim ersten UI-Write `format: markdown` | ✅ (gemessen) |
| V7 | Entwurf nur bei **Nutzer**-Änderung (`change`-Ursprung ≠ `setValue`) und `isDirty()`; trägt `version` + Zeitpunkt; Wiederherstellen nur bei gleicher Version, sonst Konfliktweg; sauberes Schließen löscht ihn | ❌ (F7) |

### 4.3 Sicherheitskette (P5-Y, XSS — Hard-Rule-nah)

Heute: Vor-Escaping der **ganzen** Quelle → eigener Parser → Sanitizer (`markdown.js:376-500`). Mit marked entfällt das
Vor-Escaping (gemessen: es macht aus `` `a<b` `` ein `a&amp;lt;b`); an seine Stelle tritt **SI1**:

- **SI1** marked-`html`-Token (Block und Inline) werden als **Text** gerendert (`escapeHtml(token.raw)`), ausgenommen
  genau die Formen aus E4. **SI2** der Sanitizer bleibt die letzte Schranke, Allowlist erweitert nur um `DEL`, `H5`, `H6`,
  `SUP`, `BR` (und E4); Attribute wie heute (`ALLOWED_ATTRS`), Tabellen-Ausrichtung als Klasse `ta-l/ta-c/ta-r` (marked
  schreibt `align=` → Renderer-Override). **SI3** `safeHref`/`safeSrc` unverändert (http(s)/mailto/`#item/`; Bilder nur
  `asset:` → Asset-Route). **SI4** Kästchen in der Lesesicht erzwungen `disabled`. **SI5** nie `id`, `style`, `on*`
  (Fußnoten ohne Anker, E7). **SI6** Rendern nur im Browser.
- **Fixtures** (Probe + pytest-Textprüfung): `<script>`, `<img src=x onerror=…>`, `<svg onload=…>`, `<iframe>`,
  `<style>`, `<a href="javascript:…">`, `[x](javascript:…)`, `![x](data:…)`, `<javascript:…>`, `&lt;script&gt;`, HTML-Kommentar,
  `<noscript><p title="</noscript><img src=x onerror=…>">` (mXSS-Klassiker).
- **Zwei Zellen, zwei Gegenläufe:** `html_als_text` (das `<b>` steht als Text da) bricht nur, wenn SI1 fehlt;
  `keine_aktiven` (kein `script`/`iframe`/`on*`/`javascript:` im DOM) bricht nur, wenn der Sanitizer `onerror` erlaubt.
  Ein einzelner Gegenlauf wäre zahnlos — die zweite Schicht fängt die erste ab.

### 4.4 Budget-Regel

`js/*.js` = Erstaufruf (≤ 250 KB, heute 236,7); **`js/editor/*.js` = nachgeladen**, geladen nur per `import()`
(nie statisch importiert); `vendor/**` = nachgeladen. `static_payload_files()` (`ui_budget.py:120`) lernt `js/editor/`; neuer
Wächter: kein **statischer** `import` einer `js/editor/`-Datei aus einem Erstaufruf-Modul. Erwartung nachgeladen:
CM5 69,7 + marked 14,9 + searchcursor 2,2 + eigene Module ~10 (Tabelle ~5, Listen ~2, Suche ~2, Einfügen ~1) ≈ **97 KB**
→ Korridor-Entscheidung E3. `editor.js` darf nicht wachsen (19,6 KB gz): neue Funktion gehört in `js/editor/`.

## 5. Schritte (je eine Sitzung)

> **Zählung:** S0–S2 + S2R = `v4.0.2` (Hotfix), S3a–S11 = `v4.1.0`. Ob das P10.5 Block 19 oder P11 Block 1 heißt, entscheidet
> E1; Pfade unten nennen `phase10_5_finishing/` und wandern mit, falls E1 = P11.

| # | Inhalt | Fertig, wenn | Gegenlauf (macht genau seine Zelle rot) | Tests / Proben |
|---|---|---|---|---|
| **S0** | **Probe + Korpus, kein Produktcode.** Fixtures `probes/fixtures_ed41/` (byte-genau): die 10 M7-Fixtures + ≥ 12 aus Anhang A7 (KI-Tabellen ohne Außen-Pipes/mit `\|`/ungleich, verschachtelte Listen 2/4 Spaces, Aufgaben inkl. `1. [ ]` und `[x]{.rot}`, Zäune mit Sprache/`~~~`, Setext, h5/h6, Fußnoten, Inline-HTML, XSS-Liste, `:::` bekannt/unbekannt, Datei ohne Newline am Ende, Tabs, Doppel-Leerzeichen, U+2028/BOM, 2.000-Zeilen-Notiz mit 200-Zeilen-Tabelle) + **ein** Katalog-Item mit allen Konstrukten. Probe `probes/p105_ed41_darstellung_probe.py` (Muster b14/b11) mit Zellen je Konstrukt × {Lesesicht, Editor} + Byte-Zellen V1–V3 + Entwurfs-Zellen + Kontrast | Probe läuft; Basislinie ist **rot** in den erwarteten Zellen (Editor-Tabelle, Listenzeichen, Entwurf, F4a–f, Kontrast) — **das ist der Befund**; JSON neben der Probe | Probe-Selbsttest: ein absichtlich falsches Soll in einer Kopie → genau die Zelle rot | `tests/test_ed41_probe.py` (Probe-JSON-Schema, Zellnamen, jeder Gegenlauf-Anker genau einmal) |
| **S1** | **Entwurfsschutz** (V7, F7): `_editorGeaendert(cm, change)` speichert nur bei Ursprung ≠ `setValue` **und** `isDirty()`; Entwurf `{…, version, gespeichert}`; `showEditableItem` liest den Entwurf **vor** `setBody`; Version ≠ → Dialog „Entwurf zu v1, aktuell v3" mit Entwurf verwerfen / Entwurf als neues Item anlegen (vorhandener Pfad `conflict-save-as-new`); `clearDetail()` löscht einen sauberen Entwurf | Zellen `entwurf_ueberlebt_neuladen` (anderes Item zuerst geöffnet) und `kein_stilles_zurueck` grün, Chromium + Firefox | (1) Ursprungsprüfung raus → nur `entwurf_ueberlebt_neuladen` rot; (2) Versionsprüfung raus → nur `kein_stilles_zurueck` rot | pytest statisch: Entwurf enthält `version`; `loadDraftIfAny` vor `setBody` |
| **S2** | **Tabellen-Widget** (mit dem **heutigen** Renderer — darum Hotfix-fähig): `js/editor/tabellen.js` (per `import()` aus `editor.js` nach `fromTextArea`), `blockRanges` (Interim: Scanner nach der Schleifenreihenfolge von `_markdownZeilen`, Prototyp Anhang A4); Widget = `.preview`-Tabelle; Klick → Zelle; Pfeil ↓/↑ → erste/letzte Tabellenzeile (`beforeCursorEnter`); Widget nur bei Cursor/Auswahl **außerhalb**; `setRawMode(true)` → keine Widgets; das Widget bekommt keinen eigenen Fokus (Tastatur = Pfeile, Bildschirmleser liest die echte `<table>`); Budget-Regel §4.4 umgesetzt | Zellen `tabelle_widget`, `klick_zelle`, `pfeil_erste_zeile`, `pfeil_letzte_zeile`, `undo`, `kopieren_quelle`, `bytes_gleich`, `bytes_zelle` grün (beide Browser); Tastenkosten in der 2000-Zeilen-Notiz ≤ Basis + 2 ms (Median, 3 × 20) | (1) Installation aus → `tabelle_widget` rot; (2) Eintritts-Korrektur aus → `pfeil_erste_zeile` rot; (3) statischer Import von `js/editor/` → Budget-Wächter rot; (4) `setBody` mit `trimEnd()` → nur `bytes_gleich` rot | `test_budget_coverage.py` erweitert; `tests/test_ed41_import_graph.py` |
| **S2R** | **Release `v4.0.2`** (wenn E1 = Hotfix): Update-Log-Zeile (menschlich, Datum = Deploy-Tag), Badge `v4.0.2`, volle Suite, `doc_health`, `ui_budget`, Darstellungs-Probe (Stand S2: Entwurf-, Tabellen-, Byte-Zellen grün, Rest als Basislinie rot dokumentiert); Deploy + `health_gate` **beim Nikinger**; live eine echte Notiz mit Tabelle öffnen | Zeilen 84–86 ✅ (84/86 aus der Wegwerf-Probe, 85 nach Sichtung live) | — | — |
| **S3a** | **Renderer-Fassade + Sicherheit** (E2): `vendor/marked/marked.esm.js` 18.1.3 **unverändert** (49.668 B, 14,9 KB gz, SHA-256 = npm-Datei, MIT; die `sourceMappingURL`-Zeile bleibt wie bei CM5, keine `.map`); `markdown.js` = Fassade (`ensureRenderer()` im Leerlauf nach dem Login, `markdownToHtml()`, `blockRanges()`); Lesesicht (`editor.js:793`) und Update-Log (`updates.js:41/67`) warten auf `ensureRenderer()`; SI1 + Sanitizer-Allowlist SI2 (§4.3); XSS-Fixtures | Korpus in Lesesicht + Update-Log ohne Seitenfehler; `html_als_text`, `keine_aktiven` grün | (1) html-Override raus → nur `html_als_text` rot; (2) Sanitizer erlaubt `onerror` → nur `keine_aktiven` rot | pytest: Vendor-SHA = Lizenzdatei; XSS-Fixtures in Probe **und** Wächter |
| **S3b** | **Erweiterungen + Konformität**: marked-Erweiterungen Format inline/Block, Fußnoten (E7); Overrides Tabellen-Klassen, Kästchen, `asset:`-Bilder, Links; S2-Widget auf die Fassade; Spec-Fixture `probes/fixtures_ed41/gfm_0.29_beispiele.json` **einmal** extrahiert (Quelle `https://github.github.com/gfm/`, „Version 0.29-gfm (2019-04-06)", SHA-256 der Quelldatei, Lizenz laut Seite CC BY-SA → `THIRD_PARTY_LICENSES.md`; Extraktor-Regeln und Zählweise Anhang A3) — die Probe liest nur die Datei (kein Netz); Budget-Zeilen nach E3 | `konformitaet` ≥ 95 % (Abschnitte + Kanonisierung wie A3); Katalog-Zellen der Lesesicht grün; `ui_budget` grün | (1) Format-Erweiterung raus → `format_*` rot; (2) Align-Override raus → `tabelle_ausrichtung` rot; (3) alter Renderer → `konformitaet` rot | — |
| **S4** | **Editor-Anzeige = Wahrheit** (F4–F6): `theme: "sfx"` (die `.cm-s-default`-Farben greifen nicht mehr) + `.cm-s-sfx .cm-*` über Tokens; Moduloptionen `strikethrough`, `taskLists`, `xml: false`; Listenzeichen sichtbar (gedimmt); Overlay ignoriert Codespans; `:::`-Zeilen nur bei gültigem Block versteckt (Zeilenklasse aus `blockRanges`), Ausrichtung als Zeilenklasse; Kästchen-Regel = GFM (Leerraum nach `]`, auch `1.`) | Zellen F4a–f und `listenzeichen` grün; `kontrast`: jede Editor-Tokenfarbe ≥ 4,5 : 1 gegen `--editor-bg` (in der Probe aus `getComputedStyle` gerechnet) | je Regel ein Patch (z. B. Overlay ohne Codespan-Prüfung → `konflikt_code` rot; `theme` zurück auf `default` → `kontrast` rot) | — |
| **S5a** | **Ein typografisches System** (E5): Editor-Fließtext Plex Sans 16 px/1,6, Überschriften = Lesesicht (22/18/16 px), Code Plex Mono 13 px, Zitat-/Codezeilen über Zeilenklassen wie `.preview`; gemeinsame Lesebreite (Editor + Lesesicht, Wert in der Sitzung messen); breite Tabellen scrollen im Widget/`.preview` (`overflow-x: auto`); Fokusring am `.CodeMirror-focused`; tote Teile weg (F14) | Klickgenauigkeit **100 %** (≥ 30 Ziele, Überschrift/Liste/Zitat/umbrochene Zeile, beide Browser; Methode A6); Sichtung (Bilder) beim Nikinger; `ui_budget` grün | Formatzeichen per `display:none` statt `visibility` (der Block-11.4-Fehler) → `klick` rot | `test_editor_live.py` an den Rückbau anpassen |
| **S5b** | **Schriften:** `build_font_subset_plex.sh:32` um U+2190–2193, U+21D2, U+2713, U+2717, U+2264/2265, U+2248 erweitern, beide Teilmengen neu bauen (`pyftsubset` + `brotli`, V-E9), Hash-Dateinamen + `@font-face` nachziehen | Zelle `glyphen`: Breite von `→ ✓ ≤` in `"IBM Plex Sans Var", monospace` = in `…, serif` (gleich nur, wenn Plex das Zeichen hat), ebenso Mono; Erstaufruf + < 2 KB | alte Teilmenge → `glyphen` rot | Font-Dateinamen-Wächter (falls vorhanden) nachziehen |
| **S6** | **Tabellen bearbeiten** (im Rohtext): Tab/Umschalt+Tab = nächste/vorige Zelle; Enter in der letzten Zeile = neue Zeile; Zeile/Spalte einfügen/löschen, Ausrichtung (setzt nur die Trennerzelle), „Tabelle formatieren" (nur Befehl; formatiert nur die eine Tabelle); „Tabelle einfügen" (3 × 2); Einfügen von TSV und HTML-Tabellen → Markdown-Tabelle (`DOMParser`, nur `textContent`, nie Markup) | je Befehl: Body-Diff = erwartete Zeilen (Zellen `tab_op_*`); Formatieren einer schon formatierten Tabelle = 0 Bytes; Einfügen einer HTML-Tabelle mit `<script>` → nur Text | je Befehl ein Patch | — |
| **S7** | **Listen und Tasten**: Enter setzt Listen/Aufgaben fort (`continuelist` 5.65.16 vendort, 1,1 KB, oder eigen), leerer Punkt beendet; Tab/Umschalt+Tab in Listen = Ebene auf die Inhaltsspalte des Elternpunkts (`- ` → 2, `1. ` → 3); außerhalb von Listen/Tabellen fügt Tab **zwei Leerzeichen** statt `\t` ein (E8b); Strg/Cmd+B/I/K, Knöpfe Durchgestrichen und Aufgabe; Umnummerieren nur bei Enter/Tab in der eigenen Liste | Zellen `liste_*`, `taste_*` grün | je Regel ein Patch | `test_editor_cm.py` (Skriptliste) |
| **S8** | **Suchen/Ersetzen** im Editor: `searchcursor` 5.65.16 (2,2 KB) + eigenes Feld (deutsch, `app.html`/`app.css`, kein `dialog.js`): Groß/klein, Regex, nächste/vorige, ersetzen, alle ersetzen (= **ein** Undo-Schritt, `cm.operation`); Strg/Cmd+F/H nur bei Fokus im Editor; Esc schließt zuerst das Feld (`app.js:317-337`) | findet „Absatzzeile 1500" in der 2000-Zeilen-Notiz; alle ersetzen + Strg+Z = Ursprung; Esc lässt den Editor offen | je Regel ein Patch | — |
| **S9** | **Komfort**: Gliederung aus Überschriften (`blockRanges`), Wort-/Zeichenzahl, Strg/Cmd+Klick folgt Links (`#item/` über `closeEditor()`-Rückfrage, http(s) neuer Tab `noopener`); Konfliktdialog mit Zeilen-Diff (E11); optional `[[` öffnet den vorhandenen Link-Picker (`openLinkPicker`) | Zellen `gliederung`, `link_folgen_fragt` grün | je Regel | — |
| **S10** | **Darstellungs-Gate** (§7): Probe fertig (alle Gegenläufe), Katalog-Wächter, `health_gate.sh --render-katalog`; Text für den Deploy-Ablauf (Plan §2.5 / Head — der Hauptagent trägt ein) | alle Zellen grün, jeder Gegenlauf rot in genau seiner Zelle | Katalog-Konstrukt ohne Fixture → Wächter rot | `tests/test_ed41_katalog.py` |
| **S11** | **Release**: Update-Log (menschlich), Badge (Version des Nikingers), volle Suite, `doc_health`, `ui_budget`, Darstellungs-Probe, Sichtung; Deploy + `health_gate` **beim Nikinger** | Abnahme §6 | — | — |

## 6. Abnahmezeilen (Vorschlag; Nummern nach E1)

Jede Zeile gilt erst mit ihren Gegenläufen aus §5 (je Regel genau eine rote Zelle).

| # | Kriterium | Beleg |
|---|---|---|
| P10.5-84 | Entwurf: Öffnen schreibt keinen; getippter Entwurf überlebt Neuladen auch nach einem anderen Item; ein veralteter wird nie still wiederhergestellt | Probe S1 |
| P10.5-85 | Tabellen im eigenen Editor als Tabelle; Eintritt per Pfeil in die erste/letzte Zeile, Klick in die Zelle; Undo/Redo; Kopieren = Quelle | Probe S2 |
| P10.5-86 | Byte-Vertrag V1–V6 auf dem Korpus (≥ 22 Fixtures, beide Browser) | Probe S0/S2 |
| P10.5-87 | Eine Wahrheit: Lesesicht und Editor-Widget aus derselben Fassade; GFM-Teilmenge ≥ 95 % | Probe S3b |
| P10.5-88 | Sicherheit zweischichtig (§4.3) | Probe + pytest |
| P10.5-89 | keine Widersprüche F4a–f; Listenzeichen sichtbar; Kontrast ≥ 4,5 : 1 | Probe S4 |
| P10.5-90 | ein typografisches System; Klickgenauigkeit 100 %; Pfeile/Häkchen aus Plex; Sichtung | Probe S5a/S5b + Bilder |
| P10.5-91 | Tabellen bearbeiten inkl. Einfügen TSV/HTML | Probe S6 |
| P10.5-92 | Listen/Tasten | Probe S7 |
| P10.5-93 | Suchen/Ersetzen | Probe S8 |
| P10.5-94 | Darstellungs-Gate in der Deploy-Vorbereitung verankert | Lauf + Doku |
| P10.5-95 | Budget (E3) + jede Datei gezählt + kein statischer Import aus `js/editor/` | `ui_budget.py` + Wächter |
| P10.5-96 | Live `v4.1.0`: Deploy + `health_gate` (dann 10/10) + Sichtung mit echten Notizen (Tabelle, Liste, Aufgabe) | Nikinger |

## 7. Darstellungs-Check (wiederkehrend, für jedes Update)

**Drei Schichten, weil jede etwas anderes fängt** (Vorschlag des Nikingers aus dem Head, konkret gemacht):

1. **Render-Probe** `probes/p105_ed41_darstellung_probe.py` an einer **Wegwerf-Instanz**: das Katalog-Item (alle
   Konstrukte aus `KATALOG`) einmal im eigenen Space (Editor) und einmal in einem fremden Space mit Leserecht
   (Lesesicht). Zellen: je Konstrukt das erwartete DOM in **beiden** Sichten (z. B. Lesesicht `table > thead > tr > th.ta-c`,
   `ul > li > ul`, `del`, `input[type=checkbox][disabled]`, `h5`, `blockquote blockquote`, `span.md-c-rot`,
   `div.md-a-zentriert`, `sup`; Editor `.sfx-tabelle-widget table`, `.sfx-todo`, sichtbares Listenzeichen,
   `.cm-header-1`, `.cm-strikethrough`, gültiger `:::` versteckt / unbekannter sichtbar), dazu V1–V3, die beiden
   Sicherheitszellen, Kontrast und Konformität. Je Zelle ein Gegenlauf in einer Kopie. Laufzeit-Ziel ≤ 3 Minuten.
   **Wo:** fester Schritt der **Deploy-Vorbereitung** (Plan §2.5, vor dem Commit; Claude Code), Ergebnis-JSON im
   Release-Commit. **Nie** gegen den Live-Dienst — die Probe schreibt (Entwurf, Zellen-Edit).
2. **Katalog-Wächter** `tests/test_ed41_katalog.py` (pytest, statisch, kein Browser): jedes Konstrukt in `KATALOG`
   hat einen Fixture-Abschnitt, eine Probe-Zelle und einen Gegenlauf; Vendor-SHA-256 = `THIRD_PARTY_LICENSES.md`.
   Läuft in der Suite **und** in den Release-Tests von `deploy.sh` (dort schon jeder pytest).
3. **`health_gate.sh` Gate 9** (optional, `--render-katalog`, nach dem Deploy beim Nikinger): `curl` auf die
   **öffentliche** Static-Route (wie Gate 5, `health_gate.sh:101-119`) — `js/markdown.js` enthält `KATALOG_VERSION`
   und jeden Konstruktnamen, `vendor/marked/marked.esm.js` hat den SHA-256 des Releases. Nur lesende GETs.

Schicht 3 fängt nur Löschungen und falsch ausgelieferte Dateien, Schicht 2 vergessene Fälle, **nur Schicht 1** die
Regression aus diesem Auftrag (ein Konstrukt, das nicht mehr erscheint). Darum ist Schicht 1 Pflicht vor jedem Deploy,
der `static/` berührt.

## 8. Entscheidungen für den Nikinger (je mit Empfehlung)

> **Entschieden (Nikinger 2026-11-05):** **E1** geteilt (`v4.0.2` in P10.5, Rest = P11 Block 1) · **E2** marked ✅ · **E3** ✅ „wenn es die Leistung nicht stark berührt“ — gemessen +0,4–0,9 ms je Taste, die Bibliotheken laden **nach** dem Erstaufruf (250 KB bleiben) · **E5** ✅. **E4** (nur `<br>`) auf Rückfrage erklärt, Antwort offen. Zählung außerhalb von Code (nur Tag-Namen): `<br>` 6× in **1** Datei, sonst nur Platzhalter wie `<domain>`/`<repo>`/`<site>`/`<redacted>` (je 1–2×, **bleiben Text**) ⇒ die Allowlist `<br>` verliert nichts. **E10** beantwortet: größte echte Notiz **1836 Zeilen / 112.821 B** (unter den gemessenen 2.005 Zeilen). E6–E9, E11, E12: offen, Empfehlungen unten.

| # | Frage | Empfehlung |
|---|---|---|
| **E1** | Platzierung: alles als P10.5 Block 19 (Zeilen 84 ff.) oder Hotfix S0–S2 + S2R in P10.5 und S3a–S11 als **P11 Block 1**? | **Geteilt.** S0–S2 + S2R = `v4.0.2` in P10.5 (Regression + Datenverlust); S3a–S11 = P11 Block 1 → `v4.1.0`. Der Head sagt „neues Feature kommt erst in P11"; Closeout Z wartet sonst ~12 Sitzungen |
| **E2** | Renderer: marked 18.1.3 vendoren oder `markdown.js` erweitern? | **marked** (98 % gegen 30 %, 14,9 KB gz nachgeladen, MIT, ESM ohne Build). Zweite Laufzeit-Bibliothek neben CM5 — bewusst gegen „so wenige wie möglich", weil der Eigenbau die Abnahme nicht erreicht. **Pflegeregel:** Versionssprung nur als eigener Schritt — vorher die GitHub-Sicherheitshinweise lesen (marked hatte ReDoS-Fälle), danach Konformitäts- und Sicherheitszellen; Entscheidung beim Nikinger |
| **E3** | Budget „nachgeladen" (heute 80 KB, 69,7 belegt) | **zwei Zeilen:** „Editor nachgeladen" ≤ **100 KB** (CM5 + Addons + `js/editor/`), „Renderer nachgeladen" ≤ **20 KB** (marked). Erstaufruf bleibt 250 KB |
| **E4** | Inline-HTML (68 Dateien): weiter Text oder kleine Allowlist? | **nur `<br>`** (genau `<br>`, `<br/>`, `<br />`, typisch in KI-Tabellen) als Umbruch, alles andere Text — **nach** einer Zählung nur der Tag-Namen (Befehl Anhang A12, keine Inhalte) |
| **E5** | Editor-Fließtext Plex Sans 16 px wie die Lesesicht (Mono nur für Code)? | **ja** — gemessen: Klickgenauigkeit 38/38 in Chromium und Firefox, auch mit größeren Überschriften (Anhang A6) |
| **E6** | CRLF/CR: Server-Normalisierung dokumentieren oder P1-Öffnung (`open(newline="")`)? | **dokumentieren** (Kommentar `frontmatter.py:18-20`, Zeile B20 im Phase-1-Head korrigieren; 0 CRLF im Bestand). Kein Code |
| **E7** | Fußnoten (8 Dateien): eigene Minimal-Erweiterung (Verweis `<sup>`, Liste am Ende, **keine** IDs/Anker) oder `marked-footnote` (1,7 KB, setzt IDs)? | **eigene** — keine IDs im Nutzerinhalt (DOM-Clobbering, §4.3 SI5) |
| **E8** | (a) Rechtschreibprüfung (braucht CM5 `inputStyle: "contenteditable"`)? (b) Tab außerhalb von Listen: zwei Leerzeichen statt `\t`? | (a) **nicht in 4.1** (anderes Eingabemodell, IME-Risiko). (b) **ja** |
| **E9** | MCP-Beschreibung um einen Satz zur unterstützten Teilmenge ergänzen (`tools.py :: _FORMAT_HINT`, nur Text)? | **ja** — KI-Clients schreiben dann innerhalb der Teilmenge; reine Textänderung, kein Verhalten |
| **E10** | Größe der größten echten Notiz (nur Zahl: Zeilen/Bytes) | erfragen; bis dahin gilt: Taste ≤ 16 ms bis 5.000 Zeilen und 200-Zeilen-Tabelle (gemessen bei 2.005 Zeilen: 3–5 ms) |
| **E11** | Konfliktdialog mit Zeilen-Diff (S9)? | **ja**, klein (LCS über Zeilen, nur Anzeige) |
| **E12** | Lesen/Bearbeiten-Schalter (Option C)? | **nein** — nur Rückfall, falls S2 an seiner Abnahme scheitert |

**Für später vorbereiten (nicht 4.1):** Kommentare/Änderungsverfolgung brauchen eine Speicherentscheidung; der
billigste Weg ist eine **Versionsansicht aus dem Git-Verlauf** des Datenverzeichnisses (jeder Write ist ein Commit) —
das wäre ein neuer Lese-Endpunkt und damit Server-Code (P11-Entscheidung). Verbundene Zellen und Bildgröße passen nicht
in GFM; das Widget aus S2 ist der Ort, an dem sie später als Darstellung hängen könnten. **Nicht in 4.1, weil schon
entschieden:** Farbraster + freie RGB-Farbe (Block 18 E2 → P11, Editor Stufe 3); Bilder per Ziehen/Einfügen (P6-AB:
nur der Knopf) — eine Änderung wäre eine neue Nikinger-Entscheidung.

## 9. [VERIFY]

| # | Was | Warum offen |
|---|---|---|
| V-E1 | Safari/WebKit | WebKit startet hier nicht: fehlende Systembibliotheken (`libevent-2.1-7t64`, `libgstreamer-plugins-bad1.0-0`, `libflite1`, `libavif16`, `gstreamer1.0-libav`, `sudo` = Nikinger). Alle Widget-Zahlen nur Chromium 151 + Firefox 153 |
| V-E2 | IME/Komposition an der Widget-Grenze | headless nicht messbar; Risiko gering, weil nur CM5s eigene Eingabe editiert (keine editierbaren Zellen) |
| V-E3 | Touch/Mobil | nicht gemessen (P5-W) |
| V-E4 | marked unter der App-CSP | gemessen nur auf einer Testseite ohne CSP; `script-src 'self'` erlaubt Modul-`import()` — in S3a im echten Seitenkontext prüfen |
| V-E5 | `blockRanges` für verschachtelte Container (Tabelle im Zitat) | nur oberste Tokens gemessen |
| V-E6 | Harte Umbrüche: marked 8/15 im Vergleich | vermutlich mein Kanonisierer (`<br>` + Zeilenumbruch); in S3b prüfen |
| V-E7 | Eintritts-Korrektur `beforeCursorEnter` | entworfen, nicht im Prototyp gebaut |
| V-E8 | `xml: false` im CM5-Markdown-Modus, ggf. `xml.min.js` streichen | Modusverhalten nicht gemessen |
| V-E9 | `pyftsubset` + `brotli` für den Font-Neubau | `fontTools 4.68` liegt im `film-venv`, `brotli` ungeprüft |
| V-E10 | echte Datenform: Tag-Namen der 68 HTML-Dateien, größte Notiz, `<br>` in Tabellen | nur der Nikinger darf zählen (Anhang A12) |
| V-E11 | Zeiten auf echter Hardware | kopflos, Software-Rasterung — nur vorher/nachher vergleichbar |
| V-E12 | CM6/`style-mod` unter `style-src 'self'` | nur relevant, falls je Option B |
| V-E13 | Konformitätsvergleich ignoriert `href`/`src` und Attribute außer Ausrichtung | Absicht (Politik weicht ab); echte Links prüft die Probe |
| V-E14 | Lizenz der GFM-Spec-Beispiele (Fixture S3b) | die Seite nennt „licensed under Creative Commons BY-SA" (auf der CommonMark-Spec beruhend); Version/Wortlaut in S3b prüfen, Eintrag in `THIRD_PARTY_LICENSES.md` |
