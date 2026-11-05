---
status: live
purpose: Anhang zum Plan Editor 4.1.0 — Messgerät, Messtabellen (Byte-Stabilität, GFM-Konformität, Prototyp Tabellen-Widget, Tastenkosten, Klickgenauigkeit, Kontrast), Konstrukt×Fläche-Matrix, Bibliotheksgrößen, Bilder, Korrekturen zu den Haiku-Hypothesen, Zählbefehle für den Nikinger. Wiederholt den Plan nicht.
read-when: wenn eine Zahl im Plan nachgeprüft oder eine Probe in S0 nachgebaut wird
detail: L2
up: ./phase10_5_editor_4_1_plan.md
down:
  - ../../phase10_5_finishing/probes/p105_b14_layout_probe.py   # Muster der Wegwerf-Instanz
  - ../../phase10_5_finishing/probes/p105_b11_roundtrip_probe.py # Muster Roundtrip
updated: 2026-11-03 (angelegt — Opus-Planungsagent; alle Messungen an Wegwerf-Instanzen, Skripte im Scratchpad, nicht im Repo)
---
# Anhang — Editor 4.1.0

## A1. Messgerät und Instanzen

- **Wegwerf-Instanzen** (drei, nacheinander): eigener freier Port, tmp-`DATA_ROOT`, tmp-`auth.sqlite3`, eigener DEK,
  TLS selbstsigniert, Umgebung ohne `SHAREFYX_*`/`SFX_*`/`SPACE_*`, Stopp über die PID-Datei; Server = dieselbe App wie
  `serve.py` (Launcher-Muster b14), statische Dateien aus einer **Kopie** (`STATIC_DIR`) — `a` unverändert (`main@a22620d`),
  `p` mit Tabellen-Prototyp, `t` mit Prototyp + Typografie-CSS. Alle drei sind gestoppt.
- **Saat:** Spaces `alpha` (eigener, Konto `alpha` mit Passwort + TOTP) und `beta` (fremd, `alpha` nur Leserecht); je 16
  Items aus einem synthetischen Korpus (Zählungen des Bestands, **keine** echten Inhalte gelesen), feste IDs
  `itm_00000001…20`, feste Uhr.
- **Browser:** Playwright 1.62 (`~/.claude-code-tools/e2e-venv`), **Chromium 151.0.7922.34** und **Firefox 153.0**,
  kopflos, Software-Rasterung, 1600 × 1000. WebKit nicht lauffähig (Plan V-E1; der Download von 293 MB wurde danach
  wieder entfernt).
- **Skripte** (Scratchpad, nicht im Repo; S0 baut sie als Probe nach):
  `/tmp/claude-1000/-home-savefyx-dev-savefxy/abb73e26-ae82-56cd-a555-4fda8580b60f/scratchpad/wegwerf/` —
  `harness.py` (start/stop), `korpus.py`, `b.py` (Login, TOTP), `e1_bytes.py`, `e2_render.py`, `e3_entwurf.py`,
  `e3b_entwurf.py`, `e4_proto.py`, `e5_klick.py`, `e6_tasten.py`, `konf/konformitaet.py`, Prototyp `proto/proto_tabelle.js`
  + `proto/patch_tabelle.json`/`patch_typo.json`.
- Zeiten: je Messung **3 Läufe × 20 Tastenanschläge**, Median und p95; vor/nach am selben Rechner, nicht absolut.

## A2. Byte-Stabilität (E1, beide Browser gleich)

Je Item: Öffnen (CM schon geladen) → Editortext gegen `GET /api/v1/items/{id}` → `isDirty()` → Speichern-Knopf →
Strg+S → ein Zeichen tippen + löschen → neu öffnen.

| Item | Editor = API-Body | geändert beim Öffnen | Speichern aus | Strg+S-Requests | Tippen+Löschen sauber | Entwurf nach Öffnen geschrieben |
|---|---|---|---|---|---|---|
| tabelle-einfach | ✅ | nein | ✅ | 0 | ✅ | nein (erstes Item: CM noch nicht geladen) |
| tabelle-ki, tabelle-im-zitat, listen-verschachtelt, aufgaben, code, durchgestrichen-html, zitate-fussnoten, ueberschriften, format-konvention | ✅ | nein | ✅ | 0 | ✅ | **ja** (= Serverstand) |
| bytes-crlf, bytes-gemischt | ✅ (beide **ohne** CR — der Server liefert LF) | nein | ✅ | 0 | ✅ | ja |
| bytes-ohne-newline, bytes-whitespace (Doppel-Leerzeichen, Tabs, Leerzeilen am Ende), bytes-unicode (BOM im Body, U+2028, NBSP, ZWJ-Emoji, RTL) | ✅ | nein | ✅ | 0 | ✅ | ja |
| gross (2.005 Zeilen, 200-Zeilen-Tabelle) | ✅ | nein | ✅ | 0 | ✅ | ja |

**Echte Edits (E3, ein Zeichen am Ende von Zeile 1, Strg+S, Datei vorher/nachher):**

| Item | Body-Bytes vorher → nachher | CR vorher → nachher | nur das Zeichen eingefügt | Frontmatter-Diff |
|---|---|---|---|---|
| bytes-crlf | 59 → 54 | 6 → 0 | **nein** (alle CR weg) | `updated`, `version`, + `updated_by`, + `format: markdown` |
| bytes-whitespace | 95 → 96 | 0 → 0 | ✅ | dito |
| bytes-unicode | 134 → 135 | 0 → 0 | ✅ | dito |
| tabelle-einfach | 204 → 205 | 0 → 0 | ✅ | dito |

**Schicht festgenagelt** (drei Zeilen, ohne UI): `Store.create(body="a\r\nb\rc\n")` → Datei 2 CR, `create()` gibt 2 CR
zurück, `get()` gibt **0** CR zurück (`store.py:412/482/771` `Path.read_text`, universelle Zeilenenden);
`index.row_from_file` dekodiert `read_bytes()` (behält CR), nutzt den Body aber nur für `body_refs` — kein Widerspruch im Index.

**Entwurfsschutz (E3b, Chromium):**

| Fall | Ablauf | Ergebnis |
|---|---|---|
| 1 | Item B öffnen (CM lädt) → Item A: „ENTWURF-1" tippen → Seite neu laden → **B zuerst**, dann A | **kein** Dialog; Entwurf jetzt = Serverstand → getippter Text **verloren** |
| 2 | A: „ENTWURF-2" tippen → neu laden → **A zuerst** | Dialog „Ungespeicherter Entwurf … Wiederherstellen?" (Textarea-Pfad, CM noch nicht geladen) |
| 3 | A nur öffnen + schließen → neu laden → fremder PATCH (v2) → A zuerst | Dialog erscheint, obwohl nichts getippt wurde; „Wiederherstellen" + Strg+S → **v3 trägt den alten Text**, die fremde Fassung ist überschrieben (nur noch im Git-Verlauf) |

## A3. GFM-Konformität (Spec-Beispiele, kanonischer DOM-Vergleich, Chromium)

Quelle: `https://github.github.com/gfm/` („Version 0.29-gfm (2019-04-06)", SHA-256 der Seite beginnt `b153d814fdfc8624`,
Lizenz laut Seite Creative Commons BY-SA), Beispiele 1–677 aus `div.example` (Markdown aus `code.language-markdown`,
Soll aus `code.language-html`, `→` = Tab), Abschnitt = letzte `h2`/`h3` davor; nur die Abschnitte der Teilmenge (HTML-Abschnitte,
Entitäten, Referenzdefinitionen ausgenommen). Vergleich: beide Ausgaben über `<template>` geparst, Struktur + Text
(Leerraum zusammengefasst), Ausrichtung `align=`↔`ta-*`, Kästchen als `[ ]/[x]`; `href`/`src` ignoriert (Politik).

| Abschnitt | n | markdown.js (heute) | marked 18.1.3 |
|---|---|---|---|
| Tables (extension) | 8 | 3 | 8 |
| Strikethrough (extension) | 3 | 2 | 3 |
| Task list items (extension) | 2 | 1 | 2 |
| Lists | 27 | 4 | 27 |
| List items | 48 | 7 | 48 |
| Block quotes | 25 | 5 | 25 |
| Fenced code blocks | 29 | 8 | 29 |
| ATX headings | 18 | 8 | 18 |
| Setext headings | 27 | 7 | 27 |
| Thematic breaks | 19 | 10 | 19 |
| Hard line breaks | 15 | 6 | 8 (V-E6) |
| Backslash escapes | 13 | 2 | 12 |
| Code spans | 22 | 11 | 22 |
| Paragraphs | 8 | 6 | 7 |
| Indented code blocks | 12 | 1 | 12 |
| Autolinks (extension) | 14 | 0 | 14 |
| Emphasis and strong emphasis | 131 | 59 | 131 |
| Links | 87 | 19 | 87 |
| Images | 22 | 1 | 22 |
| Soft line breaks / Tabs / Blank lines | 14 | 4 | 14 |
| **Summe** | **544** | **164 (30 %)** | **535 (98 %)** |

marked-Lexer: Summe der `raw` der obersten Tokens = Quelltext bei **14/16** Korpus-Texten (die zwei Abweichungen
tragen CR); Parsen der 2.005-Zeilen-Notiz in Node 13,3–21,5 ms (3 Läufe).

## A4. Prototyp Tabellen-Widget (Instanz `p`)

Mechanik: `js/proto_tabelle.js` (≈ 110 Zeilen) per `import()` aus der kopierten `editor.js` nach `cm.addOverlay`; ein
`blockScan(lines)` in der kopierten `markdown.js` (Schleifenreihenfolge von `_markdownZeilen`: `:::` → Zaun → Tabelle);
je Tabelle außerhalb von Cursor/Auswahl `cm.markText(von, bis, {replacedWith: <div class="preview">markdownToHtml(...)</div>,
clearOnEnter: true, handleMouseEvents: false})`; Abgleich per `setTimeout(0)` nach `changes`/`cursorActivity`; Klick auf
`td/th` → Zeile/Spalte → Zeichenposition der Zelle (beachtet `\|` und Codespans) → `mark.clear()` + `setCursor`.

| Prüfung | Chromium 151 | Firefox 153 |
|---|---|---|
| Text beim Öffnen unverändert, nicht geändert | ✅ | ✅ |
| Widget da (Cursor außerhalb) | 1 Tabelle | 1 Tabelle |
| Pfeil ↓ von der Leerzeile davor | Rohtext, Cursor **[6,40] = Tabellenende** ❌ (Korrektur S2) | dito |
| Pfeil ↓ aus der Tabelle hinaus | Widget wieder da | dito |
| Pfeil ↑ von unten hinein | Rohtext, Cursor [6,40] (letzte Zeile ✅) | dito |
| Klick auf „Anzahl der Versuche" | Cursor **[5,14]** = Zellbeginn ✅ | ✅ |
| „Z" tippen → nur diese Zelle geändert | ✅ `| \`retries\` | ZAnzahl der Versuche |` | ✅ |
| Strg+Z → Ursprung, sauber; Strg+Y → wieder | ✅ | ✅ |
| `getSelection()` über das sichtbare Widget = Quelle | ✅ 186 Zeichen | ✅ |
| Strg+A, Strg+C → Zwischenablage = Body | ✅ | (Rechte nur in Chromium) |
| Abgleich je Änderung (Median) | 0,2 ms | 0 ms (1-ms-Takt) |
| Zeichnen der 200-Zeilen-Tabelle | 10–11 ms | 10 ms |
| Verlassen der 200-Zeilen-Tabelle bis zum nächsten Bild | 16,5–22,9 ms | 38–39 ms |
| Seitenfehler | 0 | 0 |

Bild: Anhang A10 (`e4_widget_p_chromium.png`).

## A5. Tastenkosten (2.005-Zeilen-Notiz, `replaceRange` + erzwungenes Layout; 3 × 20)

| Instanz | Browser | Absatzzeile synchron Median / p95 | bis nach dem Abgleich Median / p95 | rohe Tabellenzeile synchron | Läufe (Median, synchron) |
|---|---|---|---|---|---|
| `a` (heute) | Chromium | 2,60 / 3,60 ms | 3,45 / 4,40 ms | 2,80 ms | 2,15 · 3,05 · 2,85 |
| `p` (Prototyp) | Chromium | 3,00 / 4,10 ms | 4,30 / 5,50 ms | 3,20 ms | 2,50 · 3,20 · 2,90 |
| `a` (heute) | Firefox | 3 / 5 ms | 5 / 8 ms | 3 ms | 3 · 4 · 3 |
| `p` (Prototyp) | Firefox | 3 / 4 ms | 5 / 6 ms | 3 ms | 2 · 3 · 3 |

Ergebnis: +0,4–0,9 ms in Chromium, in Firefox unter der Messauflösung. Kostentreiber heute schon je Taste:
`_todoMarkenAuffrischen` (`getValue().split`), `isDirty()` (`getValue`), `saveDraft()` (`JSON.stringify` + `sessionStorage`).
Öffnen der großen Notiz (inkl. API): 247 ms (heute) / 275–280 ms (Prototyp). Im DOM stehen **30 von 2.005** Zeilen.

## A6. Klickgenauigkeit (E5)

Methode: Ziel = Anfang des 2. Wortes je sichtbarer Zeile; Klick bei 25 % der Breite seines ersten Zeichens (DOM-`Range`,
nicht CMs eigene Koordinaten); „Q" tippen; Erwartung: genau vor diesem Zeichen; Undo.

| Instanz | Schrift | Chromium | Firefox |
|---|---|---|---|
| `a` | Plex Mono 13 px / 21 px (heute) | 38/38 | 38/38 |
| `t` | Plex Sans 16 px / 1,6, h1 22 px, h2 18 px, Code Mono 13 px, Listenzeichen sichtbar | 38/38 (Tabellenzeilen als Widget: 3/3) | 38/38 |

`visibility:hidden` der Formatzeichen hält die Position auch mit Proportionalschrift; der Preis bleibt der Einzug unter
versteckten `## ` (Bild `e5_t_tabelle-ki.png`). Ein CM-eigenes `markText({collapsed:true})` würde ihn vermeiden — nicht
gemessen, nicht geplant.

## A7. Konstrukt × Fläche

**Konstrukte** (Bestand = Dateien mit dem Konstrukt, von 267):

| Konstrukt (Bestand) | Lesesicht heute | Editor heute | Ziel 4.1 (beide Sichten) |
|---|---|---|---|
| Tabelle (84) | `<table>` ✅, aber `\|` teilt, Ex. 202–204 falsch | Rohtext | Widget = Lesesicht (marked) |
| `\|` in Tabelle (7) | Zelle zerbricht | Rohtext | eine Zelle mit `|` |
| Tabelle im Zitat (1) | Rohtext in Absätzen | Rohtext | Lesesicht Tabelle; Editor Rohtext |
| verschachtelte Liste (45) | Absatz „- verschachtelt A - …" | eingerückt, **ohne** Listenzeichen; Ebene 3 lila 1,94 : 1 | `ul > li > ul`; Editor Zeichen sichtbar, Kontrast ✅ |
| Aufgabe (66) | Kästchen (nur oberste Ebene) | Kästchen-Widget (alle Ebenen, `-*+`) | GFM: jede Ebene, auch `1. [ ]` |
| `- [x]{.rot}` | Kästchen + „{.rot} …" | Kästchen, `{.rot}` versteckt | kein Kästchen, rotes „x" (GFM: Leerraum nach `]`) |
| ```` ``` ````-Zaun (53) | `<pre>`, Sprache verworfen | Code | gleich |
| `~~~`, Einzugs-Code | Absatz | Code | Code |
| `~~durch~~` (31) | wörtlich | wörtlich | `<del>`; Editor `cm-strikethrough` |
| verschachteltes Zitat (11) | `> Ebene 2` als Text | Zitat-Klassen | `blockquote blockquote` |
| Fußnote (8) | wörtlich | wörtlich | `<sup>` + Liste am Ende (E7) |
| Setext (5) | „Titel ====" / Absatz + `<hr>` | Überschrift (Linie versteckt) | Überschrift |
| h5/h6 | Absatz (zwei zu einem verschmolzen) | Überschrift | `h5`/`h6` |
| `* * *`, `- - -` | `<ul><li><em> </em>` / `<ul><li>- -` | Text | `<hr>` |
| Inline-HTML (68) | als Text (escaped) | xml-Farben, 1,7–3,3 : 1 | Text; nur `<br>` nach E4 |
| harter Umbruch (2 Leerzeichen) | verschluckt | — | `<br>` |
| nackte URL | Text | Text | Link (GFM-Autolink) |
| `[Text]{.rot}` | `span.md-c-rot` ✅ | gefärbt ✅ | gleich |
| `[x]{.rot}` im Codespan | Code ✅ | **rot gefärbt** | Code |
| `![[alt]{.rot}](asset:…)` (Bilder 8) | Bild **zerstört** | Bild-Syntax zerlegt | Bild, Alt = Text |
| `::: {.zentriert}` | `div.md-a-zentriert` ✅ | `:::`-Zeilen versteckt | gleich + zentriert im Editor |
| `::: {.warnung}` (unbekannt) | wörtlich ✅ | **Zeilen unsichtbar** | wörtlich in beiden |
| `<script>`, `onerror` | Text, kein Element ✅ | Text | Text; zwei Zellen §4.3 |

**Flächen**, die Body-Text zeigen:

| Fläche | heute | Arbeit in 4.1 |
|---|---|---|
| Lesesicht fremder Items (`editor.js:766-796`) | `markdownToHtml` | über die Fassade (S3a) |
| Update-Log-Dialog + Banner (`updates.js:41/67`) | `markdownToHtml` | über die Fassade, nach `ensureRenderer()` (S3a) |
| eigener Editor | CM5-Modus + Overlay + Kästchen | S2/S4/S5a |
| MCP `get_item`/`search_items` | Rohtext / Snippet `" ".join(body.split())`, 160 Zeichen (`store.py:226`) | keine (KI liest Markdown); optional E9 |
| Liste/Suche in der UI | nur Titel/Meta (`textContent`) | keine |
| Konfliktdialog (`dialogs.js:452-459`) | nur Versionsnummern | optional Zeilen-Diff (E11) |
| Versionsband | Nummer | keine |
| Entwurf (`sessionStorage sfx:draft:<id>`) | F7 | S1 |
| Druck/Export | nicht vorhanden | keine |

**Speicher-Schlüssel des Editors:** `sessionStorage`: `sfx:draft:<id>`, `sfx:csrf`; `localStorage`: `sfx:film:gesehen`,
Link-Picker-Modus (`dialogs.js`), Kartenlayout (`graph.js`) — nur `sfx:draft:` gehört zum Editor.

## A8. Bibliotheksgrößen (heruntergeladen nach `/tmp`, `gzip -9`)

| Datei | Version | roh | gz | Lizenz / Bemerkung |
|---|---|---|---|---|
| CM5 vendort gesamt (`ui_budget`) | 5.65.16 | — | **69,7 KB** | heute |
| `addon/search/searchcursor.min.js` | 5.65.16 | 5.692 B | 2.235 B | Such-Engine (Regex, mehrzeilig) |
| `addon/search/search.min.js` + `dialog.min.js` + `.css` | 5.65.16 | 9.739 B | 4.196 B | nicht empfohlen (englische UI, eigenes Feld statt dessen) |
| `addon/edit/continuelist.min.js` | 5.65.16 | 1.901 B | 1.107 B | Listen fortsetzen |
| `addon/edit/closebrackets.min.js` | 5.65.16 | 3.918 B | 1.779 B | nicht geplant |
| `mode/gfm/gfm.min.js` (+ `overlay.min.js` 790 B) | 5.65.16 | 3.090 B | 1.738 B | **unnötig**: der Markdown-Modus hat `strikethrough`/`taskLists` |
| **marked** `lib/marked.esm.js` (zu vendoren) | **18.1.3** | 49.668 B | **14.934 B** | MIT; SHA-256 beginnt `e76f3b37046a5d29`; endet mit `sourceMappingURL` (wie CM5) |
| marked `lib/marked.umd.js` | 18.1.3 | 50.548 B | 15.323 B | mit esbuild minimiert 15.055 B — 1,7 % Gewinn, kein Grund für einen Build-Schritt |
| `marked-footnote` `dist/index.js` | 1.4.0 | 4.101 B | 1.702 B | MIT; setzt IDs → E7 |
| markdown-it `dist/browser/markdown-it.umd.min.js` | 15.0.3 | 100.786 B | 41.283 B | MIT; zu groß |
| CM6 schlank (state, view, commands, language, search, `@lezer/markdown`+GFM), esbuild `--minify` | view 6.43.15 | 339.667 B | **110.310 B** | Bündel = Build-Artefakt |
| CM6 voll (+ `@codemirror/lang-markdown` 6.5.2 → html/css/js) | — | 533.805 B | 182.503 B | — |
| `@susisu/mte-kernel` (Tabellen-Kern) | 2.1.1 | 599 KB entpackt | — | nicht nötig (eigene Zeilen-Operationen) |
| Prototyp `proto_tabelle.js` (109 Zeilen) | — | 4.101 B | 1.739 B | Richtwert für `js/editor/tabellen.js` (mit Bearbeiten ~5 KB) |

CM5 5.65.17–.21 (bis 2026-02-07): Fixes nur in Modi (crystal, dart, groovy, gherkin, pascal, sql, kotlin), `show-hint`,
Konfiguration mit Null-Prototyp — kein Grund zum Sprung. Das `search.js`-Feld setzt `style` per `element.style = …`
(CSSOM, unter der CSP erlaubt); `dialog.js` benutzt `innerHTML` nur für String-Vorlagen.

## A9. Kontrast (Editorfarben gegen `--editor-bg #0C1017`, WCAG-Formel)

| Klasse (Quelle) | Farbe | Kontrast | wo im Bestand |
|---|---|---|---|
| `.cm-s-default .cm-keyword` (vendort) | `#708` | **1,94 : 1** | 3. Listenebene |
| `.cm-s-default .cm-attribute` | `#00c` | **1,70 : 1** | Inline-HTML-Attribute |
| `.cm-s-default .cm-string` | `#a11` | **2,54 : 1** | Inline-HTML-Werte |
| `.cm-s-default .cm-tag` | `#170` | **3,32 : 1** | Inline-HTML-Tags |
| `.cm-s-default .cm-meta` / `.cm-number` / `.cm-atom` | `#555` / `#164` / `#219` | 2,56 / 2,73 / 1,46 | (Code-Modi, heute nicht geladen) |
| `.cm-s-default .cm-hr` / `.cm-bracket` | `#999` / `#997` | 6,69 / 6,51 | Trennlinie / Klammern |
| `cm-header`, `cm-link`, `cm-quote`, `cm-comment`, `cm-variable-2/3` | über `app.css` überschrieben | ✅ | — |

## A10. Bilder (Scratchpad, nicht im Repo)

Verzeichnis `/tmp/claude-1000/-home-savefyx-dev-savefxy/abb73e26-ae82-56cd-a555-4fda8580b60f/scratchpad/wegwerf/shots/`:
`e1_editor_tabelle_{chromium,firefox}.png` (der Fehler), `e1_lesesicht_tabelle_*.png` (dieselbe Tabelle gerendert),
`e2_editor_*.png` / `e2_lesesicht_*.png` (neun Konstrukte, beide Sichten), `e2_editor_listen-verschachtelt.png`
(Listen ohne Zeichen, Ebene 3 lila), `e4_widget_p_{chromium,firefox}.png` (Prototyp-Widget), `e5_t_*.png`
(Typografie-Prototyp). Für eine Sichtung beim Nikinger in S0 neu erzeugen (der Scratchpad ist sitzungsgebunden).

## A11. Korrekturen zu den Haiku-Hypothesen

| Hypothese | Korrektur (gemessen/gelesen) |
|---|---|
| H1 „Tab = indent (unit 2)" | **falsch:** Tab fügt `\t` ein, Umschalt+Tab ohne Wirkung; `indentUnit 2` gilt nur für Auto-Einzug (Plan E8b, S7) |
| H1 „`setRawMode` ohne Aufrufer" | **falsch:** Aufrufer `editor.js:539` und `:833`, Assertions `test_editor_live.py:95/110`, `test_editor_todo.py:176`; nur der Knopf ist weg (`8aba4d4`) |
| H1 tote Reste `#editor-preview`, `editorPreviewEl` | ✅ tot im Produkt; nur alte Skripte (`p856_bracket_mini_smoke.py`, `p9_btn2_toolbar_probe.py`) fragen sie ab — keine pytest-Tests |
| H2 „Tabellenzellen brechen an `\|` **und** an `|` im Codespan" | halb: GFM Ex. 200 teilt an einem **unmaskierten** `|` auch im Codespan — das tut `markdown.js` richtig; falsch ist nur `\|`. **Neu:** Ex. 202–204 (zeilenlose Fortsetzung, Kopf/Trenner-Zahl, ungleiche Zeilen) |
| H3 (3) „Format vor Bild kann Alt verderben" | **schlimmer:** das Bild verschwindet in **beiden** Sichten; die Reihenfolge ist durch `test_the_inline_rule_comes_before_the_links` festgenagelt |
| H3 (4) `- [x]{.rot}` | bestätigt; zusätzlich versteckt der Editor `{.rot}` |
| H3 (5) „CM5 normalisiert CRLF" | **falsch zugeordnet:** der Server liefert schon LF (`read_text`); CM5 bekommt nie CR; der erste Write jedes Clients macht die Datei LF |
| H3 Farbnamen im alten Plan | Code gewinnt: `rot`, `blau`, `gruen`, `gelb` (`markdown.js:32-37`) |
| H4 Kontrast „ungemessen" | gemessen A9; Überschrift/Link/Zitat/Kommentar sind überschrieben, `keyword`/`tag`/`attribute`/`string` nicht |
| H4 „Mono-Teilmenge ohne U+2192" | **beide** Teilmengen ohne `←→✓✗●★`; ↑↓ vorhanden |
| H4 tote CSS-Liste | `.toolbar-btn--wide` tot; `.glass` wird von `phase8_ui_graph/scripts/c4c5_playwright_smoke.py:64` geprüft → bleibt; `.toolbar-btn:disabled` in S5 per grep prüfen |
| W1 Rechtschreibprüfung „browser-nativ" | in CM5 nur mit `inputStyle: "contenteditable"` (heute `textarea`, `spellcheck: false` gemessen) |
| W2 CM6 ohne Browser-Build | bestätigt; Größen jetzt gemessen (A8) |
| W2 „Atomic/Joplin spleißen Bereiche" | im Prototyp nachgebaut: Klick → Zelle → nur deren Bytes ändern sich ✅ |

## A12. Zählbefehle für den Nikinger (nur Zahlen, keine Inhalte; nicht durch Agenten)

```bash
D=/home/savefyx/savefyx-data
# 1) Tag-Namen in Notizen (Anzahl Dateien je Tag) — für E4
for t in br b i u s del kbd sub sup mark span div details summary img a table p; do
  printf '%-8s %s\n' "$t" "$(grep -rliE "<$t([ />]|$)" --include='*.md' --exclude-dir=.git "$D" | wc -l)"; done
# 2) Zeilen mit <br> in Tabellenzeilen (Anzahl)
grep -rhE '^\s*\|.*<br ?/?>' --include='*.md' --exclude-dir=.git "$D" | wc -l
# 3) Größte Notiz (Bytes und Zeilen) — für E10
find "$D" -name '*.md' -not -path '*/.git/*' -printf '%s\n' | sort -n | tail -1
find "$D" -name '*.md' -not -path '*/.git/*' -exec wc -l {} + | grep -v ' total$' | sort -n | tail -1 | awk '{print $1}'
```
