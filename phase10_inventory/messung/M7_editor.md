---
status: live
purpose: M7 (P10-Plan §4, Register ED-1, V201) — welche Editor-Bibliothek trägt Stufe 1 (Live-Darstellung über Markdown) ohne Build-Schritt? Drei Kandidaten gemessen Größe, Roundtrip, ui_budget-Fit
read-when: Plan P10.5 Block 11 (Editor) — D-4 ist seit 2026-10-18 beantwortet (Stufe 1 ja), die Bibliothekswahl steht hier mit Belegen
detail: L2
up: ../CLAUDE.md
updated: 2026-10-19 (angelegt — Claude Code + GLM 5.3; Messung im Scratchpad `~/.claude-code-tools/m7`, node v24 + jsdom)
---
# M7 — Editor-Bibliothek für Stufe 1, ohne Build-Schritt

> **Ergebnis zuerst.** **CodeMirror 5 + die bereits vorhandene Vorschau (`js/markdown.js`)** trägt
> Stufe 1: 65,6 KB gz zusätzlich, Roundtrip über alle 10 Fixtures byte-verlustfrei, Korridor
> 239,0 KB von 250 KB — passt. **EasyMDE** fällt am Korridor (282,1 KB), **markdown-it + Textarea**
> wäre die 0-Byte-Variante mit dem vorhandenen Renderer. Empfehlung und Zahlen unten.

## Messwerte

| Kandidat (Version) | vendorte Dateien | raw | **gz** | Roundtrip 10 Fixtures | ui_budget-Fit (Ist 175,0 KB + x, Korridor < 250 KB) |
|---|---|---|---|---|---|
| **CodeMirror 5.65.16** + Markdown-Mode | `codemirror.min.js` 174,0 KB · `markdown.min.js` 15,3 KB · `codemirror.css` 8,7 KB | 197,9 KB | **63,1 + 2,5 KB** | ✅ 10/10 byte-gleich (`setValue`→`getValue`) | ✅ **239,0 KB** — 11 KB Luft |
| **EasyMDE 2.18.0** | `easymde.min.js` 326,6 KB · `easymde.min.css` 12,9 KB | 339,5 KB | 106,5 + 3,1 KB | ✅ 10/10 byte-gleich (`value()`/`value(x)`) | ❌ **282,1 KB** — reißt V201 |
| **markdown-it 14.1.0** + Textarea | `markdown-it.min.js` 123,6 KB | 123,6 KB | 44,8 KB | ✅ per Konstruktion (Quelle bleibt die Textarea; `render()` schreibt nie zurück) | ✅ 218,8 KB — **redundant**: `js/markdown.js` (4,3 KB gz) rendert bereits |

**Ist-Budget nachgemessen** (gleiche Messart wie der `ui_budget`-Korridor „app.js + app.css +
Font, gzip < 250 KB"): 14 `js/`-Module + `app.css` + zwei Font-Subsets = **175,0 KB gz**. Der
zuletzt dokumentierte Wert 144,7 KB (v3.0.2, Single-File-Ära) ist überholt — seit P8 ist `js/`
modular und gewachsen. `[VERIFY]`-Rest: der offizielle `ui_budget.py`-Lauf in P10.5 gegen den
echten Kandidaten-Build.

**Roundtrip-Methode.** jsdom (Scratchpad `~/.claude-code-tools/m7`, node v24; **nicht im Repo** —
gleiche Kategorie wie die jsdom-Scratchpads seit P5 Step 10). Zwei jsdom-Stubs waren nötig
(`getBoundingClientRect`, `createRange` — jsdom liefert keine Geometrie; ein Harness-Befund,
kein Bibliotheken-Befund). Die 10 Fixtures: Frontmatter, Listen (verschachtelt, geordnet),
Tabelle, Code-Zäune, Links/Autolinks/Referenzen, `itm_…`-Referenzen, Tasklisten, Zitate/HR,
Unicode/Tabs, Whitespace inkl. Datei **ohne** Newline am Ende. Vergleich byte-genau.

**Tastatur.** CM5: volle Keymap, konfigurierbare Markdown-Shortcuts, Undo/Redo, Zeilen-
Operationen. Textarea: nativ. EasyMDE: Shortcuts vorhanden, aber durch das Budget disqualifiziert.

**P5-T (kein Build-Schritt).** Alle drei laden als einzelne vendorte Dateien per `<script>`-Tag
ohne Bundler — für CM5 und EasyMDE in der Messung tatsächlich so gelaufen. **bytemd** wurde vor
der Messung aussortiert: jsDelivr liefert für 1.21.8 keinen UMD-Dist (51-Byte-Stub) und die
Bibliothek zieht Peer-Dependences — nicht single-file-vendorfähig.

**Empfehlung (füttert ED-1/V201 und den Plan P10.5; die Wahl trifft der Plan, nicht diese
Messung):** Kandidat 1 = **CM5 + vorhandene `js/markdown.js`-Vorschau** (Side-by-Side ohne
Moduswechsel, 239 KB). Variante 0 = reine Textarea + vorhandene Vorschau (0 neue KB, P5-U-nah,
aber ohne Editor-Komfort). EasyMDE: am Korridor gemessen gescheitert — kein Kandidat.

**Nachweise:** `roundtrip.json` + Fixtures + Ladeskript im Scratchpad (siehe `updated:`);
Versionsnummern der Downloads in der Tabelle (jsDelivr).
