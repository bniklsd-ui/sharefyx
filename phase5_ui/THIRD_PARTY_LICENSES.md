# Drittanbieter-Lizenzen

Self-gehostete Bibliotheken und Asset-Sammlungen, die unter `phase5_ui/` eingebunden sind.
Jede Quelle steht in einem eigenen Verzeichnis unter `phase5_ui/vendor/`, die Lizenztexte
liegen jeweils daneben (`LICENSE` oder `OFL.txt`).

## Lucide Icons

- **Quelle:** https://github.com/lucide-icons/lucide, Release-Tag `1.38.0` (2026-08-31)
- **Pfad:** `phase5_ui/vendor/lucide/` (Icons unter `icons/*.svg`, Lizenz in `LICENSE`)
- **Verwendung:** Vendored Inline-SVG-Sprite zwischen `<!-- ICONS:BEGIN -->` /
  `<!-- ICONS:END -->` in `phase5_ui/webui/static/app.html`, generiert durch
  `phase5_ui/scripts/build_icon_sprite.py`
- **Lizenz:** ISC-Lizenz fuer neue Icons; MIT-Lizenz (Cole Bemis, 2013-) als Erbe des
  Feather-Projekts fuer die Icons, die Lucide aus Feather uebernommen hat -- konkret in
  unserem Subset: `chevron-down`, `chevron-right`, `info`, `link`, `log-out`, `plus`,
  `search`, `x`. Volltext im vendored `LICENSE`.

## IBM Plex Sans + Mono

- **Quelle:** https://github.com/IBM/plex, Release `@ibm/plex-sans-variable@0.2.0` (Sans,
  variabel) und `@ibm/plex-mono@2.5.0` (Mono, statisch)
- **Pfad:** `phase5_ui/webui/static/fonts/` (gehashte WOFF2-Subsets, Lizenz in `OFL.txt`)
- **Verwendung:** `@font-face`-Bloecke in `phase5_ui/webui/static/app.css`, gebaut durch
  `phase5_ui/scripts/build_font_subset_plex.sh`
- **Lizenz:** SIL Open Font License 1.1 (OFL-1.1). Volltext im vendored `OFL.txt`.
  OFL-1.1 erlaubt Selbst-Hosting, Einbettung und kommerzielle Nutzung; Bedingung ist nur,
  dass der Lizenztext mit der Schrift mitgeliefert wird.

## CodeMirror 5 (Editor Stufe 1+2)

- **Quelle:** https://cdn.jsdelivr.net/npm/codemirror@5.65.16/ — **CodeMirror 5.65.16**
  (MIT; der Upstream ist https://github.com/codemirror/codemirror5, Tag `5.65.16`)
- **Pfad:** `phase5_ui/webui/static/vendor/codemirror/`
- **Verwendung:** der Live-Editor (P10.5 Block 11, ED-1) — **nachgeladen**, nicht Teil des
  Erstaufrufs (`js/editor_cm.js`); der Budget-Wächter zählt die Dateien als „Editor
  nachgeladen" (≤ 80 KB gzip)
- **Lizenz:** MIT (Copyright (C) 2017 by Marijn Haverbeke <marijn@haverbeke.berlin> and
  others). Volltext unten.

| Datei | SHA-256 | raw | gzip |
|---|---|---|---|
| `codemirror.min.js` | `d230e4614ed889647dc357e34f343bde5669ca37a0a14d05121e04d0d5ae435a` | 173.953 B | 57.352 B |
| `codemirror.min.css` | `c176f3906cb706151ddbfe37b7856f17b4e612c6c6583a56a290561c9f5996a7` | 6.378 B | 1.850 B |
| `markdown.min.js` | `432666afda166008f9328b81a78215e2cb5c8b3f36df41dec1f90540f1c99041` | 15.256 B | 5.579 B |
| `xml.min.js` | `4b95c039e814f16c4196a3514d040feb2a53795465d9f700cbaa5b394b270a32` | 6.376 B | 2.632 B |
| `meta.min.js` | `e3ef4a4d329b03930888090c5b4ab99e0659684d0c1fd0a743f1728aad6f312a` | 13.154 B | 3.867 B |

**Fünf Dateien, nicht drei — gemessen, nicht angenommen (2026-10-24, P10.5 Block 11,
Schritt 11.1).** Der Plan nennt `codemirror.min.js`, `markdown.min.js` (Mode) und
`codemirror.min.css`. Die gebaute `markdown.min.js` ist aber ein **UMD-Wrapper**, und im
Browser-Zweig ruft sie nur `t(CodeMirror)` auf — die beiden `require(...)`-Zweige
(`require("../xml/xml")`, `require("../meta")`) werden im Browser **nicht** abgearbeitet.
Gemessen im echten Chromium: mit den drei Dateien registriert sich der Modus zwar
(`CodeMirror.modes.markdown` ist eine Funktion, **keine** Seitenfehler), aber der
HTML/XML-Teil des Markdown-Modus fehlt — die Datei `xml.min.js` ist **kein**
Zusatz, sondern die fehlende Hälfte des Modus. Mit allen fünf Dateien bleibt das Verhalten
identisch und vollständig. Der Zuschlag beträgt **6.499 B gzip** (71.280 B statt 64.781 B) —
das Budget „Editor nachgeladen ≤ 80 KB" hält.

```
MIT License

Copyright (C) 2017 by Marijn Haverbeke <marijn@haverbeke.berlin> and others

Permission is hereby granted, free of charge, to any person obtaining a copy
of this software and associated documentation files (the "Software"), to deal
in the Software without restriction, including without limitation the rights
to use, copy, modify, merge, publish, distribute, sublicense, and/or sell
copies of the Software, and to permit persons to whom the Software is
furnished to do so, subject to the following conditions:

The above copyright notice and this permission notice shall be included in
all copies or substantial portions of the Software.

THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR
IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY,
FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE
AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER
LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM,
OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN THE
SOFTWARE.
```
