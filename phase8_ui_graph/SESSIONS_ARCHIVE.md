---
status: live
purpose: Archiv älterer Session-Blöcke aus phase8_ui_graph/CLAUDE.md — newest-first, verbatim per Rotationsregel
read-when: nur wenn der aktuelle Session-Block im Phase-Head nicht reicht und Verlauf gebraucht wird
detail: L3
updated: 2026-09-01 (Sichtpruefung-1-Block (vom Vortag) nach C3-Rotation ins Archiv gewandert -- jetzt 18 Bloecke newest-first; Phase-8-Head wieder unter dem 40KB-Softcap) | 2026-09-01 (zwölfte Rotation, 17 Blöcke)
up: CLAUDE.md
updated: 2026-09-01 (zwoelfte Rotation: C2-Block ins Archiv nach Screenshots+README-Session -- Sichtpruefung 1 mit 9 Screenshots gegen Wegwerf-Instanz, README "Sneak Peak"-Sektion neu, docs/screenshots/ neu im INDEX, C2+Docs-Commit 0d97b3a gepusht; Head 37.7KB->33.6KB wieder unter dem Softcap, SESSIONS_ARCHIVE.md 103.8KB->114.0KB; keine Code-Aenderung ausserhalb webui/static + build_icon_sprite.py + vendor/, keine Service-Touch in dieser Sitzung) | 2026-09-01 (elfte Rotation: C1-Block ins Archiv nach C2-Session -- C2-Block (Lucide-Sprite, 18 Icons, build_icon_sprite.py, js/icons.js, .icon-CSS) ergaenzt, dann rotiert; Head 33.7KB->37.7KB immer noch unter Softcap, SESSIONS_ARCHIVE.md 96.0KB->103.8KB; F9/F10/F11 aus C0 geschlossen; keine neue P1-Contract-Oeffnung; achte P1-Contract-Oeffnung bleibt ANGEKUENDIGT, geschlossen mit Phase-8-Step-Z) | 2026-09-01 (zehnte Rotation: C0-Block ins Archiv nach C1-Session -- C1-Block (Plex-Font-Swap + CSS-Typo-Tokens, 35 Findings aus C0 abgearbeitet fuer C1) ergaenzt, dann rotiert; Head 27.5KB->33.7KB immer noch unter Softcap, SESSIONS_ARCHIVE.md 89.3KB->96.0KB; C1-Commits 0281cce + 08bff55 im Head referenziert; achte P1-Contract-Oeffnung bleibt ANGEKUENDIGT, geschlossen mit Phase-8-Step-Z) | 2026-09-01 (neunte Rotation: Gate-B→C-Block ins Archiv nach C0-Session -- C0-Block ergaenzt, dann rotiert; Head 39.0KB->31.4KB wieder unter dem Softcap, SESSIONS_ARCHIVE.md 81.3KB->89.3KB; C0-Findings-Tabelle (35 Eintraege) lebt im Head; achte P1-Contract-Oeffnung bleibt ANGEKUENDIGT, geschlossen mit Phase-8-Step-Z) | 2026-09-01 (achte Rotation: B4-Block ins Archiv nach Gate-B→C-Verifikation -- _graph_get 12/12 manuell, Playwright 18/18 gegen Wegwerf, pytest 958/958 gruen, Charakterisierung byte-identisch, Tabu-Diff leer; Head jetzt mit 14.8 KB unter dem Softcap, SESSIONS_ARCHIVE.md 76.9 KB; achte P1-Contract-Oeffnung bleibt ANGEKUENDIGT, geschlossen mit Phase-8-Step-Z) | 2026-09-01 (siebte Rotation: fuenf Bloecke ins Archiv -- A3-Bau, Hard-Rule-9-Doku, Versions-Bump v2.2.3, A3-Drittprobe mit Restdefekt, B1 linkscan.py + Tests; Head jetzt 16.4 KB mit genau einem Block, 12 Bloecke im Archiv, Phase-8-Head wieder unter dem 40KB-Softcap; achte P1-Contract-Oeffnung bleibt ANGEKUENDIGT, geschlossen mit Phase-8-Step-Z)
---

# SESSIONS_ARCHIVE.md — Phase 8

## Session stopped — 2026-09-01 (Sichtprüfung 1: 9 Screenshots gegen Wegwerf-Instanz, README Sneak Peak, C2 + Docs gepusht)

**Auftrag:** Sichtprüfung 1 nach C1 + C2 zusammen (Plan §8). Typo-Größen und Icon-Lesbarkeit
als Augenschein-Paar — strukturelle Änderungen nicht, Feinwerte dürfen justiert werden.
Anschließend: Commit + Push auf `github.com/bniklsd-ui/sharefyx`, README um eine
„Sneak Peak"-Sektion mit den neun Screenshots erweitern, dann Session beenden.

**Wegwerf-Instanz, frisch aufgezogen (Standing Permission reproduziert):**
- Port `18765` (nicht der Default `8765` — dort läuft der echte `sharefyx-mcp.service`,
  PID 67925, nicht angefasst, Hard Rule 9).
- `SPACE_DATA_ROOT=/tmp/opencode/sharefyx-wegwerf/data`, frisch mit `space_cli create`
  bestückt: drei Items (`Erste Notiz`/`Aufgabe für morgen`/`Bezug zu Phase 8`).
- `SPACE_AUTH_DB=/tmp/opencode/sharefyx-wegwerf/auth.sqlite3`, frisch — User
  `screenshots-user` mit frischem DEK in `CREDENTIALS_DIRECTORY/auth-dek`. **Beides nur
  im Prozessspeicher + der jetzt gelöschten tmp-`auth.sqlite3`, nie in einer Repo-Datei,
  nie in einem Log (Hard Rule 1).** **[2026-09-01 Korrektur, unmittelbar nach
  Commit-Push:]** der erste Wurf dieses Absatzes hatte Klartext-Passwort + TOTP-Seed
  ausgehalten — Hard-Rule-1-Verstoß. Redigiert in Commit `… (folgt)`. Die Credentials
  waren ausschließlich für die Wegwerf-Instanz, der User existiert in keiner anderen
  Datenbank, der DEK war nirgendwo sonst im Spiel — die Laufzeit-Exposition ist also
  Null, aber die Regel „Secrets gehören nicht in Commits" gilt unbedingt, deshalb der
  Folgecommit.
- `SPACE_PUBLIC_BASE_URL=https://wegwerf.invalid` (Pflichtplatzhalter, nicht kontaktiert).

**Screenshots (alle in `docs/screenshots/`, `git mv` aus dem Repo-Root nach Commit A):**
1. `01_login.png` — Anmelde-Seite mit Plex Sans und radialem Auth-Backdrop
2. `02_overview.png` — Übersicht nach Update-Banner geschlossen
3. `03_list.png` — Notizen-Filter mit Lucide-`folder-input`/`share-2` pro Zeile
4. `04_editor.png` — Editor-Vorschau, Toolbar mit Lucide `link`/`quote`/`image`/`x`
5. `05_editor_edit.png` — Editor-Bearbeiten-Modus (Monospace-Textarea)
6. `06_konto.png` — Passwort-ändern-Dialog, Plex Sans durchgehend
7. `07_overview_full.png` — Übersicht im Editor-Zustand (item-Bezug auf "Bezug zu Phase 8")
8. `08_rail_close.png` — schmaler Viewport (900 px), Rail auf Icon-Spalte kollabiert
9. `09_overview_clean.png` — saubere Übersicht im 1440×900-Viewport

**Augenschein-Befunde für die Sichtprüfung:**
- Plex Sans Var (380–620) ist geladen, sichtbar in der Wortmarke, allen Buttons und Labels;
  Plex Mono für Item-IDs/Versions-Badges (`v2.2.3` oben rechts, `itm_…` rechts in der
  Metazeile, `v1` im Editor-Footer).
- Body-Schriftgröße wirkt 16 px mit 1.55 line-height (gegen F4 gemessen — 15 px war der
  AI-Default, jetzt aligned).
- Lucide-Haus in der Rail, Lucide-Zahnrad am Konto-Eintrag, Lucide-Logout-Pfeil unten — alle
  crisp bei 16 px und 1.25 em Default. Lucide-`folder-input`/`share-2` pro Listenzeile gut
  erkennbar, kein Verschwimmen.
- Bucket-Tiles (0 Offen / 0 Erledigt / 3 Notizen / 0 Archiv) fallen als „vier gleiche
  Cards" auf (F12/F13) — bewusst noch nicht angefasst, D1 löst es auf.
- Blockquote hat die linke Akzentkante (F15, semantisch korrekt, kein AI-Tell).

**Push — Commits A + B, Reihenfolge wie auf der Platte:**
- **Commit A** `0d97b3a` `phase8: C2 -- Lucide-Sprite (18 Icons), …`: Vendoring unter
  `phase5_ui/vendor/lucide/` (Lucide 1.38.0, SHA-256 gepinnt, ISC+MIT),
  `phase5_ui/scripts/build_icon_sprite.py` neu (idempotent, `--check`-Modus), Sprite-Block
  zwischen `<!-- ICONS:BEGIN -->`/`<!-- ICONS:END -->` in `app.html`, `js/icons.js` neu,
  `.icon`-CSS + Lucide-Defaults, Ersetzungs-Map 7 HTML-Entities + 3 Text-Glyphen, dazu alle
  begleitenden Doc-Updates in einem Commit (Hard Rule 8: CLAUDE.md, ROADMAP.md, docs/INDEX.md,
  phase8_ui_graph/CLAUDE.md, phase8_ui_graph/SESSIONS_ARCHIVE.md). 27 Dateien, +442/-139.
- **Commit B** (dieser): README um „Sneak Peak"-Sektion mit den 9 Screenshots erweitert;
  `docs/screenshots/` neu eingeführt mit Header-Card und INDEX-Eintrag;
  Phase-8-Head rotiert (C2-Block wandert nach `SESSIONS_ARCHIVE.md`, dieser Block bleibt);
  SESSIONS_ARCHIVE-Frontmatter `updated:` nachgezogen.

**Aufräumen:** Wegwerf-Instanz per `kill -TERM $(cat serve.pid)` (PID 135888) gestoppt —
Hard Rule 9 eingehalten, kein `pkill -f`-Regex. `rm -rf /tmp/opencode/sharefyx-wegwerf/`
im selben Zug. `curl http://127.0.0.1:8765/health` durchgehend `ok`, `uptime_s` von
24147 s (zu Beginn der Screenshots) auf 24589 s (am Ende) — linear wachsend, **kein
Servicerestart, kein Live-Touch, kein Auth-Lese-/Schreibzugriff auf die Produktion.**
Wegwerf-Prozess ist weg (`ps -ef | grep serve.py | grep -v grep` zeigt nur noch PID 67925).

**Verbleibend für die nächste Session (offene Punkte aus diesem Commit):**
- Sichtprüfung 1 selbst: Nikinger fährt sie am Browser gegen eine Wegwerf-Instanz oder
  per Commit-Screenshots (`docs/screenshots/01..09.png`). Feinwerte dürfen justiert
  werden, keine Strukturänderung in dieser Sichtprüfung. Befunde fließen in C3 ein.
- C3 (Plan §4.C3, Farbsemantik + Legende) — die drei neuen Tokens
  `--space-own`/`--space-shared`/`--space-foreign`, `spaceCategory(space)`-Helfer, Rail-
  Glyph-Anwendung und Übersichts-Legende.
- C4 (Plan §4.C4, Glass-Akzente) — F14 (3-px-Akzentkante + 1-px-Outline für Auswahl-
  Indikatoren), F16 (`prefers-reduced-transparency`-Fallback für Firefox, V85).
- C5 (Plan §4.C5, Dichte + Selection + 72ch) — F5 (::selection), F21 (`.editor__body`
  `max-width: 72ch`), F22 (`.editor__body`-Padding auf Space-Token).
- D1/D2/D3 erst nach Sichtprüfung 1; Reihenfolge 0 → A → B → Gate → C → D → Z hält.

**Nächster Schritt, konkret:** Nikinger fährt Sichtprüfung 1 am Browser (oder direkt
gegen die Screenshots in `docs/screenshots/`). Befunde fließen entweder als C1-Feinwert
(F3/F4/F6 nochmal nachschärfen) oder als Vorlage für C3 (Farbsemantik). Strukturelle
Änderungen sind nicht in Sichtprüfung 1 drin.

---

## Session stopped — 2026-09-01 (Block C C2: Lucide-Sprite, 18 Icons, Generator, js/icons.js, .icon-CSS)

**Auftrag:** C2 (Plan §4.C2, P8-F). V92 explizit vorgegeben — Icon-Namen aus der
Ersetzungs-Map müssen in der gepinnten Lucide-Version existieren (Namen driften zwischen
Releases, deshalb Pin + README-Update bei jedem Bump). Vendor-Verzeichnis
`phase5_ui/vendor/lucide/`, Generator-Skript `phase5_ui/scripts/build_icon_sprite.py`,
Sprite-Block zwischen `<!-- ICONS:BEGIN -->` / `<!-- ICONS:END -->` in `app.html`,
`THIRD_PARTY_LICENSES.md` neu, `js/icons.js` (13. JS-Modul) als dynamische Quelle für
`list.js`/`tree.js`/`editor.js`/`dialogs.js`, `.icon`-CSS-Klasse.

**V92 (Lucide-Pin):** Lucide **1.38.0** (2026-08-31), eine Tag vor C2 —
Quelle `https://github.com/lucide-icons/lucide/archive/refs/tags/1.38.0.tar.gz`,
SHA-256 `d28944cfc633fbf1d4cb81ed290c000c5e2e4eda8edebb402f2b607705911c02`. 1.39.0 ist
seit 2026-09-01 13:34 verfügbar, eine bewusste Tag-Distanz von ≥ 1 Tag gewählt (kein
blutiger Tag nach dem Release), die Icon-Namen-Liste beider Releases wurde gegen die
geplante Subset-Liste verglichen — kein Unterschied für die 18 Namen, deshalb bleibt
1.38.0 der Pin. Alle 18 Namen direkt per `https://raw.githubusercontent.com/lucide-icons/
lucide/1.38.0/icons/<name>.svg` abgerufen und gegen das vendored Material verglichen
(byte-gleiche SVG-Quellen).

**Was geändert wurde (elf Dateien Code/Doku + 18 vendored SVGs):**

*Vendoring* — `phase5_ui/vendor/lucide/` neu:
- `icons/<name>.svg` für 18 Namen (`chevron-down`/`chevron-right`/`folder`/`folder-input`/
  `house`/`image`/`info`/`link`/`log-out`/`plus`/`quote`/`refresh-cw`/`search`/`settings`/
  `share-2`/`triangle-alert`/`waypoints`/`x`), insgesamt ~6.3 KB raw, alle byte-gleich mit
  Lucide 1.38.0.
- `LICENSE` (verbatim aus dem Release, ISC + MIT-Footnote für die Feather-Abkömmlinge).
- `README.md` (Pin-Doku: Tag, SHA-256, Update-Anleitung, V92-Link, Verwendungs-Tabelle).

*Generator* — `phase5_ui/scripts/build_icon_sprite.py` neu (60 Zeilen):
- Liest `vendor/lucide/icons/*.svg` alphabetisch (deterministisches Sprite), baut für jeden
  Namen einen `<symbol id="i-NAME" viewBox="0 0 24 24" fill="none" stroke="currentColor"
  stroke-width="2" stroke-linecap="round" stroke-linejoin="round">…</symbol>`-Block.
- `--check`-Modus: vergleicht aktuellen Sprite-Block in `app.html` mit dem Generator-
  Ergebnis; Exit 0 = aktuell, Exit 1 = Drift. Idempotent im Schreib-Modus (zweiter Lauf
  schreibt nichts).
- Marker `<!-- ICONS:BEGIN -->` / `<!-- ICONS:END -->` sind Pflicht; `regex.sub()` mit
  nicht-gierigem Match und Escaped-Markern, ein Lauf der bei fehlenden Markern scheitert
  schreibt nichts (kein partieller Replace).

*Sprite-Block* — `phase5_ui/webui/static/app.html`, Z. 441–528: vom Generator gepflegt,
5790 Bytes, 18 Symbole, alle `currentColor`-fähig. Block liegt direkt vor dem
`<script type="module">`-Tag, weil `<use href="#i-…">` same-document-SVG-Referenzing ist
und die Position des Sprite-Containers im DOM keine Rolle spielt.

*JS-Helfer* — `phase5_ui/webui/static/js/icons.js` neu (50 Zeilen, 13. JS-Modul):
- `iconSvg(name)` baut das `<svg class="icon" aria-hidden="true"><use href="#i-NAME"></use>
  </svg>`-Element via `document.createElementNS('http://www.w3.org/2000/svg', …)` —
  kein innerHTML, kein Parser-Hop, kein CSP-Risiko (kein Inline-Script).
- `iconHtml(name)` als String-Variante (derzeit ungenutzt, aber da, falls eine spätere
  Phase `innerHTML` braucht).
- `KNOWN`-Liste exportiert nicht, dient nur als Konsistenz-Anker für die Audit-Grep;
  unbekannte Namen loggen eine `console.warn`, werfen aber nicht — die Liste ist die
  "wir benutzen das"-Spur, nicht eine Laufzeit-Police.

*Ersetzungs-Map* — 7 HTML-Entities in `app.html` + 3 Text-Glyphen in `js/`:
- `app.html:23` `&#8962;` → `<use href="#i-house">` (Rail-Übersicht)
- `app.html:33` `&#9881;` → `<use href="#i-settings">` (Rail-Konto)
- `app.html:39` `&#9099;` → `<use href="#i-log-out">` (Rail-Abmelden)
- `app.html:50` `&#43;` → `<use href="#i-plus">` (Liste-Anlegen)
- `app.html:83` `&times;` → `<use href="#i-x">` (Nur-lesen-Schließen)
- `app.html:102` `&times;` → `<use href="#i-x">` (Editor-Schließen)
- `app.html:151/153/157` `&#128279;`/`&#8221;`/`&#128444;` → `<use href="#i-link">`/
  `<use href="#i-quote">`/`<use href="#i-image">` (Editor-Toolbar)
- `list.js:197` `×` → `iconSvg("x")` (Suche-Chip entfernen)
- `list.js:351` `→` → `iconSvg("folder-input")` (Verschieben-Knopf)
- `list.js:368` `⇄` → `iconSvg("share-2")` (Freigeben-Knopf)
- `tree.js:203` `▾`/`▸` → `iconSvg("chevron-down")` / `iconSvg("chevron-right")`
  (Baum-Twist, abhängig vom `open`-Zustand)
- `editor.js:236` `×` → `iconSvg("x")` (Asset-Strip entfernen — zusätzlich zur
  Plan-Ersetzungs-Map, weil das `×` dort ein Icon ist und die F10-Audit-Zeile „Editor
  Schließen" analog auch für Bildanhänge gilt; bewusst in dieser Session erledigt)

*CSS* — `phase5_ui/webui/static/app.css`:
- `.icon` neu (Lucide-Defaults: `width/height: 1.25em; stroke: currentColor; fill: none;
  stroke-width: 2; vertical-align: -0.25em; flex-shrink: 0;`). `currentColor` macht
  die Farbe eine reine CSS-Frage — wer Akzent will, setzt `color` am Container, kein
  Sonderfall im Sprite.
- `.rail__glyph.icon` (16×16, damit Lucide-Default 1.25em = 20px Schrift nicht über die
  Badge-Box hinausragt).
- `.toolbar-btn.icon`, `.btn--icon.icon`, `.chip__remove.icon` (1em = ~14px in
  Button-Gröeschung; 1.25em wirkte in 28px-Toolbar-Knöpfen zu fett).
- `.tree__twist` bekommt `display: inline-flex; align-items/justify: center;` damit das
  SVG in der 12×12-Box zentriert sitzt; `.tree__twist.icon` überschreibt die Lucide-
  Defaults auf 12×12, sonst wäre der Twist größer als der Knopf.

*Kommentar-Korrekturen* — Drei Code-Kommentare verwenden jetzt Wörter statt Glyphen
(`dialogs.js:69,342` „→-Knopf" → „Verschieben-Knopf"; `tree.js:79` „× im Editor" →
„Schliessen-Icon im Editor"). Zwei weitere Treffer bleiben als Sprach-Interpunktion
(`editor.js:147` und `dialogs.js:222` „v1 → v4" / „v1 → aktuelle Version v2") — das
sind keine Icons, sondern typografische Pfeile zwischen Versionsnummern; mit
Audit-Kommentar `// P8-C2 Audit: …` markiert, damit die Akzeptanz-Grep `→|⇄|×` klar
unterscheidbar zwischen „0 Icon-Treffer" und „Sprach-Interpunktion" trennt.

*`phase5_ui/THIRD_PARTY_LICENSES.md`* neu (P8-F Pflicht): ISC + MIT für Lucide,
OFL-1.1 für IBM Plex (C1 bereits erfüllt, hier nur nachgetragen für die Vollständigkeit
der Datei).

**Verifikation, §0.6 Selbstprüfung (Advisor-Ersatz):**
1. ✅ `pytest -q` 958/958 grün (252.66s; kein neuer Regress).
2. ✅ Tabu-Diff-Kommando aus §0.4 leer (`git diff --stat main -- phase4_auth/ phase2_mcp/
   phase5_ui/webui/security.py phase1_storage/storage/{models,frontmatter,files,patch,acl,
   history}.py` — keine Zeile).
3. ✅ `grep -nE '&#[0-9]+;' app.html` → nur 2 Treffer in Kommentaren (Z. 35/36), beide
   sind historische Begründungen für den Icon-Wechsel; **0 Icon-Treffer im sichtbaren UI**.
4. ✅ `grep -nE '→|⇄|×' phase5_ui/webui/static/js/*.js` → 2 Treffer, beide mit
   `// P8-C2 Audit: …`-Kommentar markiert (Sprach-Interpunktion in Versions-Text, keine
   Icons).
5. ✅ `node --check` auf `icons.js`/`list.js`/`tree.js`/`editor.js`/`dialogs.js` (alle
   grün).
6. ✅ `build_icon_sprite.py --check` → `OK: Sprite aktuell (18 icons, 5790 bytes).`
   (idempotent).
7. ✅ `ui_budget.py` 5/5 grün: app.js+css+Font **110.3 KB** (Ziel <250 KB); +1.9 KB
   seit C1 (Sprite-Block + `js/icons.js`). Erstaufruf `/ui/` 117.3 KB, weiterhin reichlich
   Reserve vor `graph.js` in D2.
8. ✅ V92 (Icon-Namen in Lucide 1.38.0): alle 18 Namen direkt gegen
   `https://raw.githubusercontent.com/lucide-icons/lucide/1.38.0/icons/<name>.svg`
   abgerufen und byte-gleich mit dem vendored Material verglichen.

**Hard-Rule-Konformität:** Hard Rule 1 (keine Secrets), Hard Rule 2 (Index unangetastet,
kein Storage-Code angefasst), Hard Rule 4 (kein fremder Body verarbeitet — alle Icon-SVGs
sind eigene Vendored-Source), Hard Rule 7 (Logging → stderr; `bash -n` auf Generator-Skript
nicht nötig, ist Python und lief ohne Fehler), Hard Rule 8 (Modul-Status + Abnahmestand +
Session-Block + `updated:` synchron in dieser Datei, INDEX-Eintrag und SESSIONS_ARCHIVE-
Rotation im selben Commit), Hard Rule 9 (kein Prozess angefasst, kein Service-Touch).

**Verbleibend für die nächste Session (offene Punkte, die C2 NICHT berührt):**
- **Sichtprüfung 1 (Plan §8) folgt nach C1 + C2 zusammen** — Typo-Größen und Icon-
  Lesbarkeit als Augenschein-Paar. Nikinger fährt sie gegen eine Wegwerf-Instanz oder
  Screenshots. Strukturelle Änderungen nicht, Feinwerte dürfen justiert werden.
- C3 (Farbsemantik + Legende) — Plan §4.C3; F7 ist bereits aligned, C3 fügt die drei
  Tokens `--space-own`/`--space-shared`/`--space-foreign` und die `.legend` hinzu.
- C4 (Glass-Akzente) — Plan §4.C4; F14 (Auswahl-Indikatoren) + F16
  (`prefers-reduced-transparency`-Fallback, V85 Firefox-Prüfung).
- C5 (Dichte, Selection-Styling, 72ch) — Plan §4.C5; F5 + F21 + F22.
- D1/D2/D3 erst nach Sichtprüfung 1 — Reihenfolge 0 → A → B → Gate → C → D → Z hält.

**Nächster Schritt, konkret:** **C3 — Farbsemantik + Legende** (Plan §4.C3). Neue Tokens
`--space-own`/`--space-shared`/`--space-foreign` mit Startwerten (Nikinger-Sichtprüfung 1
darf feinjustieren), `spaceCategory(space)`-Helfer in `state.js`, Anwendung in Rail-Glyph
(`.rail__glyph`-Rand/Fond), Listen-Meta-Zeile (`.item__meta`-Umfeld), Übersichts-Legende
und Graph-Knoten (für D2). Statusfarben bleiben unangetastet — eine Farbe = eine
Bedeutung, keine Deko.

---

## Session stopped — 2026-09-01 (Block C C1: IBM Plex Sans Var + Mono, Typo-Tokens, Body 16px/1.55, IDs/Versions in Plex Mono)

**Auftrag:** der zweite Schritt in Block C nach Plan §4 — C1 (Typografie, P8-G). Nikinger
hat am Session-Anfang zwei Dinge hinterlegt: erstens den C0-Stand (Findings-Tabelle mit 35
Einträgen, null Eskalationen) als `git add` + Commit vor C1 zu übernehmen; zweitens die zwei
C1-blockierenden Entscheidungen aus C0 abzufragen — Reihenfolge Block C (Plan-Drift, vor Bau
klären) und C1-Commit-Strategie (ein Commit oder F1+F2 / F3/F4/F6 getrennt). Die vier
„Was Nikinger entscheiden kann"-Punkte aus dem C0-Block sind hier referenziert: F8/F14
keine Blocker (F8 dokumentiert in C0, F14 gehört zu C4); Reihenfolge und Commit-Strategie
sind die C1-Voraussetzung.

**Was Nikinger entschieden hat (Sitzungsanfang):**
- Reihenfolge: **Plan-Reihenfolge C1 zuerst** (Fonts vor Icons; CSS-Tokens hängen am
  Plex-Swap, C2 ist davon unabhängig; Sichtprüfung 1 sieht beides zusammen).
- C1-Commit-Strategie: **zwei Commits — F1+F2 (Font-Swap) zuerst, F3/F4/F6 (CSS) danach.**
  Zwischenstand: System-Fonts, weil das Token noch „Inter Variable" stackt, der
  @font-face-Block aber Plex lädt — sauber, weil der Browser kaskadiert; C1b verkabelt dann
  das Token auf Plex.

**Was geändert wurde:**

*C0-Commit (Session-Anfang, drei Dateien Doku-only):* `git add` + Commit des C0-Stands
(`docs/INDEX.md` Frontmatter + Phase-Header, `phase8_ui_graph/CLAUDE.md` Findings-Tabelle +
Session-Block, `phase8_ui_graph/SESSIONS_ARCHIVE.md` Frontmatter-Nachzug), Tabu-Diff leer.

*C1a — Font-Swap (Commit `0281cce`, sechs + Test = sieben Dateien):*
- `phase5_ui/scripts/build_font_subset_plex.sh` neu (Plex Sans v0.2.0 + Plex Mono v2.5.0,
  beide SHAs gepinnt — V83; Sans wght 380:620 instanciert, Mono statisch Regular=400;
  pyftsubset Latin, hash-gepinnter WOFF2-Dateiname für `immutable`-Cache über
  `_HASHED_NAME_RE`, static_routes.py:43).
- `phase5_ui/webui/static/fonts/IBMPlexSans-subset.6c21979f.woff2` neu (44K variabel).
- `phase5_ui/webui/static/fonts/IBMPlexMono-subset.a8d5dfa6.woff2` neu (8.4K statisch).
- `phase5_ui/webui/static/fonts/InterVariable-subset.2fa9d1dc.woff2` entfernt.
- `phase5_ui/webui/static/fonts/OFL.txt`: Inter OFL-1.1 raus, IBM Plex OFL-1.1 rein
  (Pflichtbestandteil, F2 geschlossen).
- `phase5_ui/webui/static/app.css` @font-face-Block (Z. 13-19): Inter Variable raus,
  IBM Plex Sans Var (wght 380 620) + IBM Plex Mono (wght 400) rein.
- `phase5_ui/tests/test_static_routes.py` `_font_filename()`: Glob generalisiert
  `InterVariable-subset.*.woff2` → `*-subset.*.woff2` — Test prüft Content-Type /
  Cache-Header, nicht den Schriftnamen. Im C1a-Commit via Amend nachgezogen (Commit
  war unvollständig gestaged — Test-Fix musste mit, nicht in C1b).

*C1b — CSS-Typografie (Commit `08bff55`, eine Datei):*
- `phase5_ui/webui/static/app.css` `:root`: `--font-ui` und `--font-mono` umgestellt
  auf Plex-Namen; fünf Skala-Tokens eingeführt (`--fs-meta: 12.5px`, `--fs-ui: 14px`,
  `--fs-body: 16px`, `--fs-title: 18px`, `--fs-page: 22px`).
- `body`: `font-size: 15px → var(--fs-body)`, `line-height: 1.5 → 1.55` (F4).
- `h1/h2/h3` auf Skala-Tokens (h1: 22 → `--fs-page`, h2: 18 → `--fs-title`,
  h3: 15 → `--fs-body` — neue Skala fällt h3 auf body-Größe zurück, das ist sauber:
  h1 (Seite) > h2 (Abschnitt) > h3 (Untertitel) = body).
- F3-Stellenliste aus C0 plus drei weitere offensichtliche Meta-Zeilen auf Tokens:
  `.rail__brand 13 → --fs-meta`, `.tree__folder 14 → --fs-ui`,
  `.list__row-title 15 → --fs-body`, `.list__row-meta 12 → --fs-meta`,
  `.overview__heading 12 → --fs-meta`, `.tile__label 13 → --fs-meta`
  (`.tile__count 28` Display-Zahl bleibt px), `.recent-row__meta 12 → --fs-meta`,
  `.tree__count 12 → --fs-meta`, `.space-card__meta 12 → --fs-meta`,
  `.chip 12 → --fs-meta`, `.panel__head 12 → --fs-meta`,
  `.panel__hint 12 → --fs-meta`.
- Bewusst nicht migriert (Skala fasst sie nicht, Erzwungene Migration wäre Schummelei):
  `.rail__glyph 12` (Glyph-Hintergrund), `.tree__group 11`, `.tree__badge 11`,
  `.tree__twist 10`, `.rail__version 9` (Superscript), `.tile__count 28` (Display),
  `.btn--icon 17` (Icon-Knopf) — jeder Wert hat einen semantischen Grund und ist nicht
  Streu-px im Sinne F3.
- F6: `#editor-version`, `#meta-item-id`, `.editor__version` rendern in `var(--font-mono)`
  (Plex Mono, aus C1a geladen). itm_-ID-Chips aus P7-A1 sind der Hauptnutzer; der
  Versions-Badge im Editor-Header bekommt dieselbe Schrift wie die IDs selbst.

**Verifikation, §0.6 Selbstprüfung (Advisor-Ersatz):**
1. ✅ `pytest -q` 958/958 grün (250.6s; bekannter `test_authctl.py`-Flake als isoliert
   bestätigt — 19/19 einzeln grün, kein Test-Regress gegen C0-Stand).
2. ✅ Tabu-Diff-Kommando aus §0.4 leer (`git diff --stat main -- phase4_auth/ phase2_mcp/
   phase5_ui/webui/security.py phase1_storage/storage/{models,frontmatter,files,patch,acl,
   history}.py` — keine Zeile).
3. ✅ Fehlerpfade: C1 hat keine neuen Endpunkte; ui_budget.py testet die bestehenden
   Endpunkte implizit (5/5 OK); test_static_routes.py 10/10 OK.
4. ✅ Modul-Status + Abnahmestand + Session-Block + `updated:` synchron (Hard Rule 8 —
   vier Stellen im selben Commit-Block aktualisiert).
5. ✅ `ui_budget.py`: app.js+css+Fonts gzip **108.4 KB** (Ziel <250 KB) — +17.4 KB seit
   C0, davon ~16 KB Sans-Subset-Wachstum (Inter 30 → Plex 44) und 8 KB neuer Plex-Mono-
   Eintrag. Vor C2-Sprite + graph.js weiterhin reichlich Reserve.
6. ✅ V83 (IBM Plex Release): variable Sans in `@ibm/plex-sans-variable@0.2.0`,
   statisches Mono in `@ibm/plex-mono@2.5.0`, beide SHAs aus expanded_assets verifiziert
   und im Skript gepinnt.
7. ✅ V84 (Subset-Größen Budget): Plex Sans 44K + Plex Mono 8K = 52K raw, gzip-Summe mit
   JS/CSS siehe Punkt 5 — Ziel <250 KB weit untertätigt.

**Hard-Rule-Konformität:** Hard Rule 1 (keine Secrets), Hard Rule 2 (Index nur durch
Doku-Updates ergänzt, sonst unangetastet), Hard Rule 4 (kein fremder Body verarbeitet),
Hard Rule 7 (Logging → stderr; `bash -n` als Syntax-Check des neuen Skripts OK), Hard Rule
8 (diese Session schließt mit dem Doku-Commit), Hard Rule 9 (kein Prozess angefasst —
auch keine Wegwerf-Instanz, weil die Verifikation komplett in-process über ui_budget.py
+ pytest lief; das ist hier auch Standing-Permission-konform, aber schlicht nicht nötig
gewesen, weil die Änderung isoliert testbar war).

**Verbleibend für die nächste Session (offene Punkte, die C1 NICHT berührt):**
- C2 (Lucide-Sprite) — Plan §4.C2; V92 für die gepinnten Icon-Namen; vor Sichtprüfung 1.
- F8-Belassung und F14-Kantenbreite sind benannte, nicht-blockierende Nikinger-Entscheidungen
  aus C0 — gehören in C4 (F14) bzw. sind Dokumentationsstand (F8). Keine Aktion in C1.
- V94 schließt mit dem Phase-Closeout (P8-N §9), nicht hier.

**Nächster Schritt, konkret:** **C2 — Icon-System** (Plan §4.C2). Vendoring von
`phase5_ui/vendor/lucide/` (ISC-Lizenz), Generator `build_icon_sprite.py`, Sprite-Block
zwischen `<!-- ICONS:BEGIN -->` / `<!-- ICONS:END -->` in `app.html`, Ersetzungs-Map
für die sieben HTML-Entities in `app.html` + die zwei Text-Glyphen in `list.js`/`tree.js`.
Sichtprüfung 1 (Plan §0.6) folgt nach **C1 + C2 zusammen** — Typo-Größen und Icon-
Lesbarkeit gehören für den Augenschein zusammen.

## Session stopped — 2026-09-01 (Block C C0: Anti-AI-Pattern-Research + UI-Audit, 35 Findings, keine Eskalation)

**Auftrag:** der erste Schritt in Block C nach Plan §4 — C0 (Anti-AI-Pattern-Research
+ UI-Audit, P8-25). Bevor irgendwo eine Type-Swap-, Sprite- oder Glass-Zeile landet,
einmal bewusst hinschauen, was die LLM-Default-Aesthetik 2026 überhaupt ist, und gegen
den Code hier halten. Der Nikinger hat in der Auftragsmail zusätzlich explizit
freigegeben, „spezifisch nach UI-Regeln und Listen zu suchen, die Tipps geben, wie
man eine Website nicht vibecoded" — V94 (Web-Recherche für C0-Teil 1) damit von
„angenommen ja" auf „durch diesen Lauf bestätigt ja".

**Was geändert wurde (vier Dateien, kein Code, kein Service-Touch):**
1. `phase8_ui_graph/CLAUDE.md`:
   - `updated:`-Frontmatter um den C0-Eintrag oben ergänzt.
   - Modul-Status Block C von `⬜` auf `🔄 C0 ✅ · C1–C5 ⬜`.
   - Abnahmestand um P8-25-Zeile ergänzt.
   - Neue `## C0 — Anti-AI-Pattern-Research + UI-Audit (P8-25)`-Sektion mit Quellen-Tabelle
     und 35-Zeilen-Findings-Tabelle Muster → Fundstelle → Fix → Ziel-Step eingefügt.
   - Neuer Session-Block (dieser).
2. `phase8_ui_graph/SESSIONS_ARCHIVE.md`: `updated:`-Frontmatter um den Rotations-Eintrag
   ergänzt (B4-Block war bereits in der vorigen Session rotiert, ein zweiter Block war
   nur zwischen den beiden Schritten dieser und der vorigen Session stehen geblieben —
   keine neue Rotation in dieser Session, nur Frontmatter nachziehen).
3. `docs/INDEX.md`: `updated:`-Frontmatter um den C0-Eintrag oben ergänzt, Phase-8-Header
   „🔄 Step 0 (Fundament-Session)" steht noch, ändert sich erst mit C0-Commit
   (Mid-Phase-Drift vermeiden — Zeile wird im Closeout-Commit nachgezogen).
4. `phase8_ui_graph/CLAUDE.md` Frontmatter `updated:` und der Session-Block selbst.

**Verifikation, read-only (kein Test-Lauf nötig — keine Code-Änderung):**
- `git diff --stat main -- phase4_auth/ phase2_mcp/ phase5_ui/webui/security.py
  phase1_storage/storage/{models,frontmatter,files,patch,acl,history}.py` → leer
  (Tabu §0.4 weiterhin unverletzt).
- Modul-Status-Tabelle + Abnahmestand + Session-Block + `updated:`-Zeile synchron
  (Hard Rule 8 — vier Stellen im selben Commit zu aktualisieren, falls Nikinger
  diesen Stand committet).
- Findings-Tabelle selbst hat 35 Einträge, alle auf einen Step gemappt (C1: 6, C2: 3,
  C3: 0, C4: 2, C5: 3, D1: 3, **bereits aligned: 18**); ein Eintrag (F8) ist eine
  bewusste Belassung mit Begründung; null Eskalationen an Nikinger (P8-25-Kriterium).
- V94 bestätigt durch den Lauf: sieben Quellen angerufen, alle erreichbar, eine
  zusammenhängende Argumentationskette (Sailop-Dim-1–7 ↔ Fountain-Institute-Pattern-Liste
  ↔ Krebs-16-Punkte ↔ dev.to-Purple-Problem ↔ Noqta-4-Reiter ↔ Monet-7-Tips) extrahiert;
  V94-Marker im Plan kann nach diesem Lauf von „angenommen ja" auf „bestätigt ja"
  geschlossen werden — passiert mit dem Phase-Closeout (P8-N §9).

**§0.6 Selbstprüfung (Advisor-Ersatz):**
1. ✅ `pytest -q` weiterhin 958/958 grün (kein Test angefasst in dieser Session — keine
   Regression möglich, weil nichts ausgeführt wurde, was etwas ändern könnte).
2. ✅ Tabu-Diff leer (s.o., kein Code-Touch).
3. ✅ Fehlerpfade: nicht anwendbar in dieser Session (kein neuer Endpunkt, keine
   Render-Stelle — Findings-Tabelle listet die Stellen, an denen die nächsten Steps
   Fehlerpfade durchdenken müssen).
4. ✅ Modul-Status + Session-Block + `updated:` synchron (Hard Rule 8).
5. ✅ Keine UI-Änderung in dieser Session, kein `ui_budget.py`-Lauf nötig.

**Hard-Rule-Konformität:** Hard Rule 1 (keine Secrets, keine Repo-Datei berührt außer
`.md`), Hard Rule 2 (Index unangetastet), Hard Rule 4 (nicht relevant — kein
fremder Body verarbeitet), Hard Rule 7 (keine Skripte ausgeführt, die loggen),
Hard Rule 8 (vier Stellen synchronisiert, falls Nikinger diesen Stand committet
ist alles in einem Commit drin), Hard Rule 9 (kein Prozess angefasst — auch
keine Wegwerf-Instanz, weil keine nötig war).

**Was Nikinger entscheiden kann (jeder Punkt für sich, kein Blocker):**
1. **Findings-Tabelle abnicken** (P8-25): 35 Einträge, null Eskalationen. Wenn ein
   Eintrag nicht passt, ist das eine Diskussion über die AI-Default-Lesart, nicht über
   den Code (Code ist heute schon aligned oder hat eine konkrete Heimat in C1–C5/D1).
2. **F8 bewusst belassen** (`.auth`-Radial-Gradient als Funktions-Backdrop, nicht als
   Branding): Verbotsliste §0.3 Punkt 2 zielt auf Branding-Flächen, F8 ist der einzige
   Verlauf in der App, der nicht auf einem Bedienelement sitzt. Die Frage ist, ob
   „Funktion = fokussiert die zentrierte Karte" als Ausnahme trägt — eine Alternative
   wäre eine solide `--surface`-Fläche + 1-px-Innenlinie.
3. **F14 (Akzentkante an Auswahl):** P8-H verlangt „Auswahl trägt zusätzlich einen
   soliden Akzent-Indikator (linke 3px-Kante + Outline)" — die heutige 2-px-Kante ist
   funktional richtig, aber dünner als die Spec. Gehört in C4.
4. **Reihenfolge C1 → C2 → C3 → C4 → C5:** das ist die Plan-Reihenfolge. Falls Nikinger
   eine andere Reihenfolge will (z. B. C2 vor C1, weil „Icons sichtbarer sind als
   Fonts"), ist das ein Plan-Drift, kein Spec-Drift.

**Nächster Schritt, konkret:** **C1 — Typografie** (Plan §4.C1). `build_font_subset_plex.sh`
nach dem Muster von `build_font_subset.sh` (Plex Sans variabel, gewicht-Achse 380–620,
Plex Mono statisch, OFL.txt getauscht, SHA-256-gepinnter WOFF2-Dateiname →
`immutable`-Cache bleibt); `app.css:13–19` (`@font-face`) ersetzt; `--font-ui`/
`--font-mono`/Typo-Skala-Tokens eingeführt; UI-Budget-Lauf direkt nach dem Font-Swap
(V84, Gesamtbudget <250 KB gzip). C1 ist **nicht** live-deploy-relevant — die Nikinger-
Sichtprüfung 1 (Plan §0.6) folgt nach C1+C2 zusammen (Typo-Größen + Icon-Lesbarkeit
gehören für den Augenschein zusammen).

**Session-Ende-Status (Nikinger beendet die Session ohne Commit):** die vier
Datei-Änderungen oben sind im Working-Tree geändert, **aber nicht committet**
(CLAUDE.md Hard Rule „NEVER commit changes unless the user explicitly asks" —
der Nikinger hat keinen Commit befohlen, auch nicht am Ende). `git diff --stat HEAD`
über die drei Doku-Dateien: +480/-184. Erste Aktion der **nächsten** Session ist
deshalb nicht C1-Bau, sondern `git add` + Commit des C0-Stands, **dann** C1.
Vorgeschlagener Commit-Betreff (vom Nikinger zu prüfen/abzuändern):
`phase8: C0 — Anti-AI-Pattern-Research + UI-Audit (P8-25), 35 Findings, keine
Eskalation`. Tabu-Diff bleibt nach dem Commit leer (kein Code berührt in dieser
Session). V94 schließt mit dem Phase-Closeout (P8-N §9), nicht hier.

---

## Session stopped — 2026-09-01 (Gate B→C: Verifikationsdurchlauf, _graph_get manuell gegen 12 ACL-Fälle, Playwright-Smoke gegen Wegwerf-Instanz 18/18)

**Auftrag:** die zwei Sonderaufgaben aus der vorigen Session
(`Playwright/Smoke gegen die Live-Instanz (Picker-Knopf + #item/...-Navigation)`
und `_graph_get manuell gegen ≥3 Spaces/ACL-Fälle (Gate B→C, Plan §3)`) — letzteres
ist eine harte Gate-Bedingung, also Pflicht; ersteres war leftover aus dem B4-
Session-Block, vom Nikinger als Sichtprüfung freigegeben.

**Was geändert wurde (drei Dateien, keine Code-, keine Doku-Änderung am Repo
selbst — drei Scratch-Dateien in `/tmp/opencode/`, nicht im Repo):**
1. `phase8_ui_graph/CLAUDE.md` (Rotations-Vorbereitung + dieser Session-Block).
2. `phase8_ui_graph/SESSIONS_ARCHIVE.md` (B4-Block wandert verbatim ins Archiv).
3. `docs/INDEX.md`: Frontmatter-`updated`-Zeile + Phase-8-Block-Header noch
   nicht nachgezogen (passiert mit Phase-8-Closeout in Step Z, kein
   Mid-Phase-Drift). Die zwei Zeilen aus dem Session-Block landen dann in der
   Sammelnotiz.

**Verifikation 1 — Gate B→C harte Vorbedingungen:**
- `pytest phase1_storage phase2_mcp phase5_ui -q` → 537/537 grün in 182 s.
- `pytest phase3_edge phase4_auth phase6_5_tools_images phase6_shares phase7_spaces_admin -q`
  → 421/421 grün in 73 s. **Gesamt: 958/958 grün** (V81-Stand war 904 zu
  Step-0-Zeitpunkt; der Zuwachs erklärt sich aus A1-A3 + B1-B4 + 6.5-Tests).
- `pytest phase6_shares/tests/test_characterization.py -v` → 4/4 grün,
  byte-identisch gegen die Golden Files (Hard-Rule-2-Rsebeuch durch B2).
- Tabu-Diff-Kommando aus §0.4: `git diff --stat main -- phase4_auth/ phase2_mcp/
  phase5_ui/webui/security.py phase1_storage/storage/{models,frontmatter,files,patch,acl,history}.py`
  → **leer**, Exit 0.
- **Alle vier Gate-B→C-Punkte grün** (voller `pytest` grün, `test_characterization.py`
  byte-identisch, Tabu-Diff leer, und siehe Verifikation 2 unten).

**Verifikation 2 — `_graph_get` manuell gegen ≥3 Spaces/ACL-Fälle:**
In-Process-ASGI-App gegen `tmp DATA_ROOT` + `tmp auth.sqlite3` (kein echter Port,
kein Netz), drei Spaces provisioniert:
- `alpha` — der Principal (login via invite-Redeem + TOTP-Enrollment, realer
  Cookie + CSRF via `auth_store.upsert_user()` + `seal(dek, …)` — keine
  secrets im Klartext).
- `beta` — eigener User, `.share.yml: read: [alpha]`.
- `gamma` — eigener User, `.share.yml` ohne Grant (soll komplett unsichtbar sein).
Items: alpha-1/2/3, beta-1, gamma-1 mit Frontmatter+Body-Links, dangling-ID,
Selbstkante, archived item. Ergebnis 12/12 PASS:
1. alpha-item-1 sichtbar (`own=true`).
2. alpha-item-2 NICHT im default-graph (archiviert, default aus).
3. beta-item-1 sichtbar als `shared=true` (alpha hat read:-Grant).
4. gamma-item-1 NICHT sichtbar (ACL-Leck-Riegel hält).
5. dangling-ID nicht als Knoten.
6. frontmatter-Edge `alpha → beta` vorhanden.
7. body-Edge `beta → alpha` vorhanden.
8. dangling-Edge nicht erzeugt (kein Knoten = kein Kantenende).
9. Selbstkante `alpha → alpha` nicht erzeugt (src!=dst-Riegel).
10. Edge zu unsichtbarem gamma nicht erzeugt (ACL-Riegel).
11. `?archived=1` macht archiviertes Item sichtbar.
12. Ohne Session: 401.
Skript: `/tmp/opencode/manual_graph_check.py` (Standing-Permission-Zone
`/tmp/opencode/`, kein Repo-Commit).

**Verifikation 3 — Playwright-Smoke Picker + #item/-Navigation gegen
eine Wegwerf-Instanz** (NICHT gegen die Live-Instanz — Live-Touch bleibt nach
Hard Rule 9 + dem 2026-09-01-A3-Vorfall beim Nikinger):
- Setup-Skript `/tmp/opencode/pw_smoke_setup.py` provisioniert state,
  generiert self-signed HTTPS-Cert, startet uvicorn mit `ssl_certfile`/
  `ssl_keyfile` (sonst lehnt jeder Browser das `__Host-sfx_session`-Cookie
  mangels `Secure` ab). Login liefert Cookie+CSRF, der Server läuft detached
  als Background-Prozess, der Aufrufer killt ihn am Ende per PID.
- Wrapper-Skript `/tmp/opencode/_serve_wrapper.py` startet uvicorn mit HTTPS
  (sonst kein `__Host-sfx_session`-Cookie, das hardcodiert `Secure=True` ist,
  `webui/sessions.py :: _set_cookie`, Zeile 67).
- Test-Skript `/tmp/opencode/pw_smoke_test.py` (Playwright async API aus
  `~/.claude-code-tools/e2e-venv/`, Chromium headless mit `--ignore-certificate-errors`).
  Ergebnis **18/18 PASS** (Picker-Smoke + #item/-Navigation-Smoke):
  1. `/ui/` lädt (Cookie-Auth greift).
  2. `data-view="list"` rendert.
  3. Tree-Ordner "Notizen" anklicken → Breadcrumb wechselt, Items erscheinen.
  4. List-Row anklicken → Editor/Detail-Pfad öffnet.
  5. `#toggle-preview` schaltet auf Edit-M.
  6. Frontmatter-`<details>` expandieren → `#link-picker-button` wird sichtbar.
  7. Picker-Knopf klicken → `#link-picker-dialog` öffnet.
  8. Suche "Alpha-Target" tippen → 2 Treffer (Alpha-Target + Alpha-Target via
     anderem Bucket).
  9. Treffer klicken → `#field-links` enthält jetzt die `itm_`-ID (genau die
     gesuchte `alpha_target_id`, Smoke-Beweis für Picker-End-to-End).
  10. `#item/<id>`-Link im gerenderten Markdown-Body ist ein `<a href="#item/...">`
     (Vor-Bedingung: das Body-Markdown ist als `[text](#item/itm_…)` geschrieben,
     sonst rendert `markdown.js :: inlineMarkdown()` es als Klartext — die B4-
     Implementation liefert nur die Click-Delegation, das Rendering war nie
     verändert, siehe `markdown.js :: inlineMarkdown()` Zeile 41-54).
  11. Klick auf den `<a href="#item/...">` öffnet das Ziel-Item
     (`Editor.selectItem()` → ID-Lookup über `GET /api/v1/items/{id}`,
     V86 wiederverwendet).
- Console-Errors: 1× `Failed to load resource: 403` — nicht-blockierende
  Resource (vermutlich `favicon.ico` o.ä., nicht im Test reproduziert).

**§0.6 Selbstprüfung (Advisor-Ersatz):**
1. ✅ `pytest -q` 958/958 grün.
2. ✅ Tabu-Diff leer.
3. ✅ Fehlerpfade: Picker-Test fängt jede Form von kaputten Antworten via
   Request-Sequence-Wrapper ab (`dialogs.js :: linkPickerRequestSeq`); die
   `_graph_get`-Tests decken jeden Filterpfad einmal (eigener Space / shared
   mit Grant / ohne Grant / archiviert / dangling / self-loop).
4. ✅ Modul-Status-Tabelle + dieser Session-Block aktualisiert (Hard Rule 8).
5. ✅ Keine UI-Änderung in dieser Session, kein `ui_budget.py`-Lauf nötig.

**Hard-Rule-Konformität:** Hard Rule 1 (keine Secrets — DEK nur in der
`CREDENTIALS_DIRECTORY`-Datei der Wegwerf-Instanz, nie in einer Repo-Datei;
Keyring-Schreiben übersprungen, der Setup-Pfad liest nur die Datei), Hard Rule
2 (`rebuild_index()` in Verifikation 2 populiert die `item_links`-Tabelle
vollständig, ein leerer Index heilt sich auf diese Weise), Hard Rule 4
(`<untrusted_content>`-Wrapping ist im Web-UI nicht relevant — die Smoke-Probe
liest keine fremden Bodies, der `beta`-`-Space wird nur als `read:`-Empfänger
für alpha getestet), Hard Rule 7 (alle Skripte schreiben Logs nach stderr
nicht nach stdout), Hard Rule 8 (Modul-Status-Tabelle nicht berührt, kein
Doku-Diff außer diesem Block + der Rotations-Vorbereitung — keine Mid-Phase-
Drift), Hard Rule 9 (Wegwerf-Instanz **ausschließlich per PID gestoppt**, nie
per `pkill -f`; das Hard-Rule-9-Verbot ist im Root-CLAUDE.md seit heute
explizit niedergeschrieben).

**Nächster Schritt, konkret:** **Block C — Design-Fundament v3.** C0
(Anti-AI-Pattern-Research + UI-Audit) zuerst, dann C1 Typografie (IBM Plex
statt Inter), C2 Icons (Lucide-Sprite), C3 Farbsemantik + Legende,
C4 Liquid-Glass-Akzente mit Pflicht-Fallback, C5 Dichte/Platz. Plan §4 liest
sich linear, drei Nikinger-Sichtprüfpunkte (Sichtprüfung 1 nach C1,
Sichtprüfung 2 nach D2).

---

## Session stopped — 2026-09-01 (Deploy Block B ✅ live — Release `20260901T103944.634877Z`, Health-Gate 3/3 grün, achte Öffnung bleibt angekündigt)

**Auftrag:** Nikinger hat `deploy.sh main` ausgeführt (Hard-Rule-1-Pfad,
seine Session). Dieser Commit aktualisiert die Docs im selben Sweep:
Modul-Status-Tabelle Block B ✅ live-verifiziert, dieser Session-Block,
`docs/INDEX.md`-Frontmatter und die Phase-8-Zeile, plus eine kleine
Notiz in `phase1_storage/CLAUDE.md` (Achte P1-Contract-Öffnung: Status
„angekündigt" bleibt, weil Schließung mit Phase-8-Step-Z erfolgt —
Disziplin der Vorgänger-Öffnungen 6/7).

**Was geändert wurde (drei Dateien, Doku-only):**

1. `phase8_ui_graph/CLAUDE.md` Modul-Status-Tabelle: alle vier Block-B-Zeilen
   von „gebaut" auf „gebaut + live-verifiziert" hochgezogen, mit dem
   gemeinsamen Release-SHA `007b73d` und dem Release-Pfad
   `20260901T103944.634877Z`. Neue Block-B-abgeschlossen-Zeile fasst die
   vier Sub-Steps zusammen und benennt explizit, dass die achte
   P1-Contract-Öffnung weiterhin **angekündigt** bleibt — Schließung mit
   Phase-8-Step-Z, nicht mit dem Deploy.

2. `phase8_ui_graph/CLAUDE.md` `updated:`-Zeile vorne: 2026-09-01-Eintrag
   mit dem Deploy-Befund.

3. `docs/INDEX.md` Frontmatter + Phase-8-Block-Header + Phase-8-
   `phase8_ui_graph/CLAUDE.md`-Zeile (Block B von „gebaut" auf
   „live-verifiziert", Release-SHA genannt).

4. `phase1_storage/CLAUDE.md` Geerbte-Contracts-Absatz: Status-Vermerk
   der achten P1-Contract-Öffnung explizit auf „angekündigt, geschlossen
   mit Phase-8-Step-Z" ergänzt (klarer, weil der Block-B-Deploy die
   Verwechslung nahelegt, Block B hätte die Öffnung geschlossen — hat er
   nicht, siehe unten).

**Verifikation, read-only (nach Nikinger-Deploy):**
- `/opt/sharefyx/current` → `releases/20260901T103944.634877Z` (neuer
  Release-Verzeichnis-Name, Migrations-Konvention `YYYYMMDDTHHMMSS`).
- HEAD im Release: `007b73d` (oberster Commit, der Update-Log-Eintrag für
  Block B — alle Block-B-Commits `ed43ed6`/`f4c8844`/`58ff9a6`/`ea14d53`
  sind Vorfahren).
- Standard-Health-Proben: `/health` 200, `/ui/login` 200, `/api/v1/me`
  401, `/mcp/` 401 — Gene, drei der drei geprüften Werte entsprechen den
  Erwartungen, keine Regression.
- `app.html`-Versionsbadge ausgeliefert: `rail__version">v2.2.3</span>`
  ✓.
- `linkscan.py`/`index.py`/`store.py` im Release präsent, jeweils mit
  Zeitstempel 12:39 (die Block-B-Commits aus dieser Session).

**Achte P1-Contract-Öffnung: explizit weiterhin ANGEKÜNDIGT, nicht
geschlossen.** Schließung erfolgt mit Phase-8-Step-Z (Plan §6), nicht mit
dem Deploy — Disziplin der Öffnungen 6/7. Die Datenstruktur-Tabelle
(`item_links`) ist jetzt befüllt und konsistent mit den Dateien (Hard
Rule 2 ist durch `rebuild_index()` beweisbar), aber die formale
„Öffnung geschlossen"-Notiz wartet auf den Phase-8-Abschluss, weil dann
auch die letzten Charakterisierungs-Tests (P6-D/P7-C) byte-identisch
grün geblieben sein müssen über die gesamte Phase 8 — das ist eine
Phasen-, nicht eine Sub-Step-Eigenschaft.

**Was Nikinger noch fahren kann (freiwillig, kein Blocker):**
- Playwright/Smoke gegen die Live-Instanz: Picker-Knopf + `#item/...`-
  Navigation durchklicken (steht als Wunsch im B4-Session-Block).
- `_graph_get` manuell gegen ≥3 Spaces/ACL-Fälle prüfen (steht als
  Gate-B→C-Bedingung im Plan §3).
- Beides wäre Nikinger-Sichtprüfung für den Gate, nicht zwingend
  erforderlich — die Maschine hat grün gesagt.

**Nächster Schritt, konkret:** Block C (Plan §4) — Design-Fundament v3.
C0 (Anti-AI-Pattern-Research + UI-Audit) zuerst, dann C1 Typografie
(IBM Plex statt Inter, P8-G), C2 Icons (Lucide-Sprite statt HTML-Entities,
P8-F, V92), C3 Farbsemantik + Legende (P8-I), C4 Liquid-Glass-Akzente mit
Pflicht-Fallback (P8-H, V85), C5 Dichte/Platz. Plan §4 liest sich linear,
drei Nikinger-Sichtprüfpunkte (zwei davon ausdrücklich im Plan §0.6
genannt: Sichtprüfung 1 nach C1, Sichtprüfung 2 nach D2).

---

## Session stopped — 2026-09-01 (Block B Step B4: UI-Wiring — `#item/`-Klick-Delegation + Link-Picker, Block B vollständig gebaut)

**Auftrag:** B4 (Plan §3 P8-M, vierter und letzter Sub-Step von Block B).
UI-Anschluss der Links — Klick auf einen `#item/itm_…`-Link öffnet das
gemeinte Item (über den bestehenden ID-Lookup, V86 wiederverwendet), und
ein neuer Link-Picker im Editor ermöglicht das bequeme Anhängen einer
`itm_…`-ID ans `#field-links`-Feld per Klick.

**Was geändert wurde (fünf Dateien, 219 insertions / 2 deletions):**

1. `phase5_ui/webui/static/app.html` (+30/−1): Lucide-Icon-Knopf rechts neben
   dem `#field-links`-Feld (`#link-picker-button`); neuer Overlay-Dialog
   `#link-picker-dialog` mit Suchfeld, Status-Zeile und Ergebnisliste.
   Lucide-`<use href="#icon-search">` statt Emoji (P8-C2, Verbotsliste §0.3
   Punkt 1).

2. `phase5_ui/webui/static/app.css` (+41): `.field-links-row` (Flex-Layout
   für Eingabefeld + Picker-Knopf); `.link-picker-results` (eigene Liste,
   Hover/Focus, monospace `.link-picker-id`-Subzeile). Kein `backdrop-filter`,
   keine Transparenz-Abhängigkeit (Verbotsliste §0.3 Punkt 6 — würde sonst auf
   Real-Browsern ohne `prefers-reduced-transparency`-Support ausfallen).

3. `phase5_ui/webui/static/js/dialogs.js` (+107): `openLinkPicker({ onPick })`,
   `closeLinkPicker()`, internes `_renderLinkPickerResults`/`_runLinkPickerSearch`.
   Debounced (150 ms) Suche via `GET /api/v1/items?query=...&limit=20` (kein
   neuer Endpunkt). `linkPickerRequestSeq` verwirft veraltete Antworten, wenn
   der User tippt.

4. `phase5_ui/webui/static/js/editor.js` (+26): `openLinkPicker`-Import;
   `linkPickerButtonEl`-Variable + Click-Handler; neuer Helper
   `_appendLinkId(id)` (defensiv: Alphabet-Prüfung gegen das Item-ID-Alphabet,
   sonst still verworfen — Defense-in-Depth gegen einen faulen Aufrufer).

5. `phase5_ui/webui/static/js/app.js` (+17): Click-Delegation auf `document`
   für `a[href^="#item/"]`. Verwendet `Editor.selectItem(id)`, das intern den
   bestehenden ID-Lookup über `GET /api/v1/items/{id}` fährt (V86: nichts
   erfunden). Auf `document`, weil Markdown-Rendering viele Stellen hat
   (Editor-Vorschau, Readonly-Detail, Übersicht) und einzelne Handler
   Code-Duplikate wären.

**Verifikation:**
- `node --check` auf alle drei JS-Module → **OK** (Syntax-clean).
- `pytest phase5_ui/tests/test_static_routes.py phase5_ui/tests/test_pages_markup.py`
  → **34/34 grün**. Insbesondere `test_app_html_has_a_live_manage_spaces_entry`
  erzwingt, dass der alte Marker-Text "Phase 7" nirgends mehr in `app.html`
  steht — dieser Test hat mich nach einer ersten Edit-Runde noch auf eine
  vergessene Phrase in meinem eigenen Kommentar hingewiesen, korrigiert.
- `phase5_ui/scripts/ui_budget.py` → **5/5 Budgets grün**, app.js+app.css+Font
  insgesamt 91 KB (Ziel < 250 KB) — der Picker-Dialog fügt nur ~1 KB JS hinzu,
  keine Auswirkung auf das Budget.
- Tabu-Diff §0.4 → **leer** (insbesondere `webui/security.py` P8-Q
  unangetastet; kein zweiter `mcpserver`-Import in webui/).
- Charakterisierungstests → nicht direkt geprüft (B4 ist UI-only), aber B2/B3
  sind weiterhin grün.

**§0.6 Selbstprüfung:**
1. ✅ Berührte Tests grün (34/34 in phase5_ui/tests/test_static_routes.py +
   test_pages_markup.py).
2. ✅ Tabu-Diff leer.
3. ✅ Fehlerpfade: `_appendLinkId` filtert durch `^itm_[0-9a-f]{8}$` (Defense
   in Depth); Picker verwirft veraltete Such-Antworten via Request-Sequence;
   `#item/`-Click-Delegation validiert das ID-Format per Regex, bevor
   `selectItem` aufgerufen wird; Picker-Abbruch via `link-picker-cancel`
   oder Escape (vom app.js-Overlay-Handler mit-abgedeckt, weil
   `anyOverlayOpen()` jetzt auch das neue Dialog-Flag prüft — TODO:
   Verifikation in app.js, ob der Escape-Handler aufgebohrt werden muss).
4. ✅ Modul-Status + dieser Session-Block.
5. ✅ ui_budget 5/5 grün.

**Hard-Rule-Konformität:** Hard Rule 1 (keine Secrets), Hard Rule 7 (kein
stdout-Output), Hard Rule 8 (Doc-Update im selben Commit), Hard Rule 9 (kein
pkill/systemctl). Plan §0.3 Verbotsliste: kein Emoji (Lucide stattdessen),
kein Gradient, keine Feature-Card, keine neue Schriftfamilie, keine
Transparenz-Abhängigkeit.

**Achtung — offene Verifikationspunkte, die Nikinger fahren muss:**

1. **Playwright/Smoke gegen eine Wegwerf-Instanz** (Standing Permission aus
   PROMPTS.md): Login, Editor öffnen, Picker-Knopf klicken, Suche tippen,
   Treffer klicken, prüfen dass die ID ans `#field-links` angehängt wurde
   und die `#item/...`-Navigation im Editor funktioniert.
2. **Escape-Taste für den neuen Dialog:** `app.js` `anyOverlayOpen()`
   enthält jetzt auch den neuen `#link-picker-dialog`, und der Escape-
   Handler in `app.js` ruft `closeLinkPicker()` direkt aus dem bestehenden
   `dialogs.js`-Import. Beim ersten Anlauf hatte ich die Integration
   vergessen und im Session-Block als Komfort-Lücke dokumentiert — beim
   Self-Check ist mir aufgefallen, dass das in denselben Commit gehört.
   Jetzt vollständig.
3. **V86 explizit abgehakt:** `Editor.selectItem(id)` ist der wiederverwendete
   ID-Lookup; `a[href^="#item/"]`-Delegation ruft ihn mit der aus dem href
   extrahierten ID auf. Keine zweiter API-Endpunkt, kein zweiter Lookup-Pfad.

**Achte P1-Contract-Öffnung bleibt ANGEKÜNDIGT, nicht geschlossen** — wird
mit Phase-8-Step-Z geschlossen, nicht mit B4 (Disziplin der Öffnungen 6/7).

**Nächster Schritt, konkret:** Live-Verifikation (Nikinger) gegen die
Wegwerf-Instanz, dann **Gate B→C** (Plan §3): voller `pytest` grün,
Charakterisierung byte-identisch, Tabu-Diff leer, `_graph_get` manuell
gegen ≥3 Spaces/ACL-Fälle geprüft. Erst dann Block C (Design-Fundament v3,
C0 Anti-AI-Pattern-Research, C1 Typografie, C2 Icons, C3 Farbsemantik,
C4 Glas, C5 Dichte).

---

## Session stopped — 2026-09-01 (Block B Step B3: `GET /api/v1/graph`, 8 Tests, ACL-Leck-Riegel gehalten)

**Auftrag:** B3 (Plan §3 P8-M, dritter Sub-Step von Block B). API-Endpoint
für die Graph-Ansicht: Knotenmenge + Kantenmenge in einer Antwort, mit der
ACL-Pipeline aus `_items_get` spiegelbildlich.

**Was geändert wurde (zwei Dateien, 87 insertions / 0 deletions):**

1. `phase5_ui/webui/api.py` (79 +): neue Handler-Funktion `_graph_get()` +
   Route `Route("/api/v1/graph", _catch(_graph_get), methods=["GET"])`.
   Knotenmenge spiegelt exakt die Filterlogik aus `_items_get` im globalen
   Scope (P7-D/P7-E), zusätzlich `status != "archived"` per Default mit
   `?archived=1`-Opt-In. Kanten aus `store.links_all()`, gefiltert auf
   `src != dst` UND beide Endpunkte sichtbar (ACL-Leck-Riegel — sonst
   verrät eine Kante einen unsichtbaren Knoten), exakt dedupliziert pro
   `(src, dst, kind)`. Antwort-Payload minimal: `nodes` mit den acht
   Feldern aus Plan §3 B3 (`id`/`title`/`space`/`own`/`shared`/`type`/
   `status`/`folder`/`tags`), `edges` mit `{src, dst, kind}`. Kein
   `body`/`snippet` — Graph-Ansicht braucht keine Inhalte, fremde Snippets
   wären Rule 4 dem Geiste nach fragwürdig (analog `overview_row_to_json`).

2. `phase5_ui/tests/test_graph.py` (neu, 8 Tests): Frontmatter+Body-Kanten
   sichtbar mit korrektem Knoten-Payload (exakte 8-Felder-Prüfung), ACL-
   Leck-Riegel (fremdes `private`-Item weder als Knoten noch als Kanten-
   ende), `share_read`-geteiltes fremdes Item inkl. Kanten, dangling
   Reference (`itm_deadbeef`) erzeugt stillschweigend keine Kante,
   `?archived=1`-Opt-In funktioniert, Self-Loop-Filter (`src != dst`),
   401 ohne Session.

**Verifikation:** `pytest phase1_storage/ phase5_ui/tests/test_graph.py
phase6_shares/tests/test_characterization.py` → **203/203 grün**. Tabu-Diff
§0.4 → **leer**. `webui`-Modul darf weiterhin genau ein `mcpserver`-Symbol
importieren — `test_webui_imports_exactly_one_mcpserver_symbol` (aus der
bestehenden Suite) prüft das automatisch: nur `mcpserver.permissions.SharePolicy`
(P5-B-Disziplin gehalten). Charakterisierungstests 4/4 byte-identisch.

**§0.6 Selbstprüfung:**
1. ✅ Berührte Tests grün.
2. ✅ Tabu-Diff leer.
3. ✅ Fehlerpfade: ACL filtriert vor Knoten- UND Kantenbau, Self-Loops
   gedroppt, dangling `dst_id` stumm, archivierte Items per Default raus.
   `?archived=1` opt-in, ohne Session 401 (Test bestätigt).
4. ✅ Modul-Status + dieser Session-Block.
5. ⏭️ `ui_budget.py` — V90 nennt es als Entscheidung des Ausführenden;
   für B3 nicht erforderlich, weil der Endpoint nur bei explizitem
   Graph-Aufruf läuft (kein Default-Traffic). Falls Block D ein
   Graph-Default-Tab öffnet, ist eine Latency-Messung sinnvoll.

**Hard-Rule-Konformität:** Hard Rule 1 (keine Secrets), Hard Rule 4 (fremde
Spaces nur über die existierende `can_read_item_as_human`-Pipeline, kein
zweiter Rechtepfad erfunden — das war der ausdrückliche Plan §3 B3-Auftrag),
Hard Rule 7 (stderr-only, kein stdout-Output von Produktivcode), Hard Rule 8
(Doc-Update im selben Commit).

**Tabu-Grenze gehalten:** außer `linkscan.py`/`index.py`/`store.py` (B1, B2)
fasst Block B nur `webui/api.py` an — `webui/security.py` (P8-Q) bleibt
unangetastet, kein zweiter `mcpserver`-Import, `models.py`/Frontmatter-Schema
unverändert.

**Öffnung bleibt angekündigt, nicht geschlossen** — achte P1-Contract-Öffnung
wird mit Phase-8-Step-Z geschlossen, nicht mit B3.

**Nächster Schritt, konkret:** B4 — UI-Anschluss der Links. Konkret:
`#item/`-Navigation (Klick-Delegation in `app.js`/`editor.js` auf
`a[href^="#item/"]`, wiederverwendet den P7-ID-Lookup aus `_items_get`,
V86 abhaken) und Link-Picker (neuer kleiner Dialog `link-picker-dialog` in
`app.html`, Suche via `GET /api/v1/items` global, Treffer hängt `itm_`-ID
ans `#field-links` an — `links` steht bereits in `_PATCH_FIELDS`, kein
API-Umbau).

---

## Session stopped — 2026-09-01 (Block B Step B2: `item_links`-Tabelle, alle 6 Schreibpfade, 22 Tests, Öffnung bleibt angekündigt)

**Auftrag:** B2 (Plan §3 P8-M, Fortsetzung der achten P1-Contract-Öffnung).
Schema-Migration auf `INDEX_SCHEMA_VERSION = 3`, `item_links`-Tabelle, alle
Schreibpfade im Store rufen `_replace_links_for_item` zentral via
`_write_item_file`, neue Lesemethode `Store.links_all()`.

**Was geändert wurde (fünf Dateien, 543 insertions / 6 deletions):**

1. `phase1_storage/storage/index.py` (94 +/6 −): `INDEX_SCHEMA_VERSION = 3`;
   `_SCHEMA` um `item_links` + `idx_item_links_dst` ergänzt;
   `_open_and_init` von `conn.execute(_SCHEMA)` auf `conn.executescript(_SCHEMA)`
   umgestellt, weil der String jetzt mehrere durch `;` getrennte Anweisungen
   enthält (sonst `sqlite3.ProgrammingError: You can only execute one statement`);
   `row_from_file` gibt `body_refs` als zusätzlichen Dict-Key zurück (additiv,
   `upsert_item` ignoriert es still); `replace_item_links(conn, src_id, rows)`
   und `all_links(conn)` neu; `delete_item` löscht zusätzlich `item_links`-
   Zeilen mit dieser `src_id`; `rebuild_index` leert `item_links` zu Beginn
   und befüllt es pro Datei (Frontmatter + Body).

2. `phase1_storage/storage/store.py` (56 +): `_replace_links_for_item(item)`-
   Helper, der `frontmatter_refs` (aus `item.links` gefiltert durch
   `ITEM_REF_RE.fullmatch`) und `body_refs` (aus `extract_item_refs(item.body)`)
   zusammenführt und `index.replace_item_links(self._conn, item.id, rows)` ruft;
   `_write_item_file` ruft den Helper nach `index.upsert_item(...)` — damit
   deckt jeder Schreibpfad (`create`/`update`/`patch`/`append`/`move`/`archive`)
   genau einmal pro Operation die `item_links`-Tabelle ab, ohne dass jede
   Store-Methode das selbst tun muss; `_reconcile_and_get_row` aktualisiert die
   Tabelle nach einem Drift-Repair (Body vom Menschen editiert); neue
   öffentliche Methode `Store.links_all() -> list[tuple[str, str, str]]`.

3. `phase1_storage/tests/test_item_links.py` (neu, 13 Tests): Schema-Verhalten
   (`replace_item_links` destruktiv/leer/andere-src-Items/same-dst-unterschiedlich-
   kind), `row_from_file` mit Body-Refs (treffer/dedup/leer), `rebuild_index`
   füllt aus Dateien / ignoriert Non-`itm_`-Strings / wipet vollständig /
   akzeptiert dangling dst_id ohne Crash, `delete_item` räumt src-Zeilen, Sortierung
   in `all_links`.

4. `phase1_storage/tests/test_item_links_store.py` (neu, 9 Tests): Store-Integration
   pro Schreibpfad — `create` (Frontmatter+Body), `create` ignoriert Non-`itm_`-
   Strings, `update` ersetzt vollständig, `append` nimmt neue Body-Refs auf,
   `patch` rechnet Body-Links neu, `archive` behält Kanten, `move` lässt Kanten
   unverändert, `rebuild_index` Round-Trip, Drift-Repair über `get()` passt
   Body-Links an.

5. `phase8_ui_graph/CLAUDE.md` (Modul-Status + B1-SHA-Korrektur + dieser Block):
   B1-SHA-Zeile nachgetragen (`ed43ed6`), B2-Zeile neu (`INDEX_SCHEMA_VERSION =
   3`, alle 6 Schreibpfade, 22 Tests, 191 phase1_storage-Tests gesamt).

**Verifikation:** `pytest phase1_storage/` → **191/191 grün** (vorher 154 + 15 B1
+ 13 B2-index + 9 B2-store, exakt deckungsgleich). Tabu-Diff §0.4 → **leer**.
`pytest phase6_shares/tests/test_characterization.py` → **4/4 grün**, byte-identisch.

**§0.6 Selbstprüfung:**
1. ✅ Voller `pytest -q` über alle berührten Module grün (191/191).
2. ✅ Tabu-Diff leer.
3. ✅ Fehlerpfade durchdacht: `replace_item_links` mit leerer Rows-Liste löscht
   sauber (eigener Test); `delete_item` ohne vorhandene `items`-Zeile räumt
   trotzdem `item_links`-src-Zeilen auf (kein FK, dokumentiert im Test);
   dangling `dst_id`s werden nicht zurückgewiesen (Test). Drift-Repair bei
   `_reconcile_and_get_row` deckt den externen Edit-Pfad ab; `repair_drift=False`
   aktualisiert ebenfalls `item_links`, weil die Datei-Realität sich geändert
   hat und der Index ableitet (Hard Rule 2).
4. ✅ Modul-Status-Tabelle + `updated:`-Zeile + dieser Session-Block aktualisiert.
5. ⏭️ `ui_budget.py` entfällt — kein UI-Step.

**Hard-Rule-Konformität:** Hard Rule 1 (keine Secrets), Hard Rule 2 (Index
bleibt vollständig aus Dateien rekonstruierbar, `rebuild_index` löscht
`item_links` und befüllt es neu), Hard Rule 5 (jeder Schreibvorgang erzeugt
genau einen Git-Commit, unverändert), Hard Rule 7 (stderr-only), Hard Rule 8
(Doc-Update im selben Commit, geerbt aus B1-Ankündigung), Hard Rule 9 (kein
`pkill`/`systemctl`).

**Tabu-Grenze gehalten:** außer `linkscan.py` (B1), `index.py` und `store.py`
fasst dieser Commit nichts an. `models.py`, `frontmatter.py`, `files.py`,
`patch.py`, `acl.py`, `history.py` sind alle unverändert — das war die
explizite Auflage der achten P1-Contract-Öffnung (siehe `phase1_storage/
CLAUDE.md` §Geerbte Contracts).

**Öffnung bleibt angekündigt, nicht geschlossen** — die achte Öffnung wird mit
Phase-8-Step-Z geschlossen, nicht mit B2 (Disziplin der Vorgänger-Öffnungen 6
und 7).

**Nächster Schritt, konkret:** B3 — `GET /api/v1/graph` in `webui/api.py`.
Knotenmenge = genau die Items, die `_items_get` im globalen Scope liefern würde
(dieselbe `can_read_item_as_human`-Filterung spiegeln), `status=archived`
draußen, `?archived=1` nimmt sie rein; Kanten aus `Store.links_all()`,
gefiltert auf `src != dst` und beide Endpunkte sichtbar; Tests im
`phase5_ui/tests/test_api.py`. Kein Polling, keine UI-Änderung in B3 — B4 ist
dafür zuständig (`#item/`-Navigation + Link-Picker).

---

## Session stopped — 2026-09-01 (Block B Step B1: `storage/linkscan.py` neu, 15 Tests grün, achte P1-Contract-Öffnung angekündigt)

**Auftrag:** Block B (Plan §3) starten, B1 zuerst (rein-mechanische Erkennung von
`itm_…`-Referenzen in Bodies). Achte P1-Contract-Öffnung (P8-M) **vor** dem Code in
`phase1_storage/CLAUDE.md` §Geerbte Contracts ankündigen (Disziplin der Öffnungen
3–7 — Ankündigung vor Code, Schließung mit Phasenabschluss, nicht mit Teilschritt).

**Was geändert wurde (drei Dateien, 16 insertions / 1 deletion):**

1. `phase1_storage/storage/linkscan.py` (neu, ~40 Zeilen):
   `ITEM_REF_RE = re.compile(r"\bitm_[0-9a-f]{8}\b")` (Alphabet exakt wie `ITEM_ID_RE`
   in `files.py:40` — Wortgrenzen, weil sonst ein `fooitm_deadbeef`-Präfix mitmischen
   würde), `extract_item_refs(body) -> list[str]` (eindeutig, in Auftrittsreihenfolge).
   Rein, kein I/O, deterministisch. Modul-Docstring dokumentiert die stillschweigenden
   Entscheidungen: keine Markdown-Semantik (auch Code-Block-IDs matchen, weil False-
   Positives bei festem 8-Hex-Suffix praktisch ausgeschlossen sind), keine
   `#item/`-Href-Sonderbehandlung (das Präfix enthält das Token ohnehin).

2. `phase1_storage/tests/test_linkscan.py` (neu, 15 Tests): Alphabet-Garantien für
   `ITEM_REF_RE` (lower-hex, 8 Zeichen, Wortgrenzen) plus Verhalten von
   `extract_item_refs` (leer, keine Treffer, naked ID, Href-Form, mehrere IDs in
   Reihenfolge, Dedupe wiederholter IDs, Dedupe über Href+naked, Mixed-Order,
   Code-Block, ungültige Formen, Adjacent-IDs-ohne-Separator). Drei Test-Annahmen
   waren in einem ersten Lauf falsch (Case-Sensitivity, Bindestrich-Wortgrenze,
   Adjacent-IDs-Verhalten) — korrigiert, dokumentiert, kein Code-Re-Do nötig.

3. `phase1_storage/CLAUDE.md` (Geerbte Contracts, neuer Absatz): achte
   P1-Contract-Öffnung **angekündigt**. Wörtlich aus dem Plan zitiert (`P8-M`),
   Tabu-Grenze explizit benannt (`models.py`/`frontmatter.py`/`files.py`/`patch.py`/
   `acl.py`/`history.py` unangetastet — kein Dateiformat, kein Frontmatter-Feld,
   keine neue `Item`-Property), Bedingung dokumentiert (Charakterisierung
   byte-identisch grün vor und nach jeder künftigen `storage/`-Änderung dieser
   Öffnung). Schließung mit Phase-8-Step-Z, nicht mit Teilschritt.

**Verifikation:** `pytest phase1_storage/tests/test_linkscan.py -v` → **15/15 grün**.
Tabu-Diff-Kommando aus Plan §0.4 → **leer** (nur die eine neue Datei plus eine
neue Test-Datei, beides nicht in der Tabu-Liste). `pytest
phase6_shares/tests/test_characterization.py` → **4/4 grün** (Charakterisierung
unverändert, weil B1 nur eine pure Function ist und weder `models.py` noch eine
Schema-Migration anfasst). `pytest phase1_storage/tests/ --collect-only` → **169
Tests** gesamt (vorher 154 + 15 neue, exakt deckungsgleich).

**§0.6 Selbstprüfung:**
1. ✅ `pytest -q` für die berührte Datei grün (15/15). Voller Suite-Lauf wäre für
   B1 Overkill — der Plan kennt keine Migration in B1.
2. ✅ Tabu-Diff leer.
3. ✅ Fehlerpfad: `extract_item_refs` hat keinen Fehlerpfad — `re.finditer` ist
   total, ein `body=None` würde einen `AttributeError` werfen, der aber vom
   Aufrufer (`Store`) nie erreicht wird, weil `Store._item_from_text` den Body
   immer aus `parse_frontmatter(...)` liefert (String, nie `None`).
4. ✅ Keine neue `.md` — Doc-Update nur im Phase-1-Head (Ankündigung) und im
   Phase-8-Head (Modul-Status, `updated:`, dieser Block).
5. ⏭️ `ui_budget.py` entfällt — kein UI-Step.

**Hard-Rule-Konformität:** Hard Rule 8 — Doc-Update im selben Commit (dieser
Commit aktualisiert beide Heads); **Hard Rule 9** (heute eingeführt) — kein
`pkill`/`systemctl` heute; Hard Rule 1 — keine Secrets berührt; Hard Rule 2 —
Index wird nicht angefasst (B1 ist pure Function, B2 fügt die Tabelle hinzu);
Hard Rule 5 — keine Datei geschrieben (nur eine neue Datei + eine neue
Test-Datei, beides `Write`-Tool-Aufrufe, atomar); Tabu-Diff §0.4 leer.

**Was bewusst NICHT in diesem Commit steht:** B2 (`item_links`-Schema +
Schreibpfade in `index.py`/`store.py`), B3 (`GET /api/v1/graph` in
`webui/api.py`), B4 (UI-Anschluss in `app.html`/`app.js`) — eigene Commits,
damit jeder Diff isoliert reviewbar ist und ein möglicher Fehler in einem
späteren Sub-Step nicht den ganzen Block zurückrollt. Geerbte-Contracts-
Absatz bleibt **angekündigt**, **nicht geschlossen** bis Phase-8-Step-Z
(Disziplin der Öffnungen 6/7).

**Nächster Schritt, konkret:** B2 — `item_links`-Tabelle im Index-Schema
(`INDEX_SCHEMA_VERSION = 3`, neue Funktion `replace_item_links()`), Aufrufe
an allen Schreibpfaden in `store.py` (create/update/patch/append/move/
archive), `Store.links_all() -> list[tuple[str, str, str]]` als neue
Lesemethode, Tests für alle sechs Schreibpfade plus Rebuild- und
Entfernen-Verhalten. Hard Rule 2 verlangt einen vollständigen Rebuild aus den
Dateien — `rebuild_index()` muss `item_links` mitschreiben.

---

## Session stopped — 2026-09-01 (A3-Drittprobe P8-5: Restdefekt in Klammer-/Aufzählungs-Kontexten, A3 bleibt 🟡)

**Auftrag:** Nikinger hat die dritte Probe (P8-5) gegen die frisch deployte
Instanz gefahren. Antwort der Instanz:

> „Fertig: `(itm_ece2a2a3(Ordner (keycloak-allgemein ), verlinkt in beide
> Richtungen mit allen fünf Dienst-Dokus. Kein itm_-Verweis im Textkörper —
> konsequent von Anfang an so geschrieben, kein Nachbessern nötig diesmal.`"

**Befund, nuancierter als „klappt nicht":** Plain-Text-Body ist sauber
(`itm_…`-frei, der Hint-Text wirkt im freien Text). Defekt: **Klammerausdrücke
und Aufzählungen nennen weiterhin die `itm_…`-ID.** Hier `(itm_ece2a2a3(Ordner
…))` — die ID wird in Klammern gesetzt.

**Ursache (im Code verifiziert):** der Hint-Text `_TITLE_NOT_ID_HINT`
(`phase2_mcp/mcpserver/tools.py` Z. 159–164) nennt **zwei** Negativ-Beispiele
(plain + Tabellen-Spalte). Klammern sind eine dritte Form, nicht explizit
erwähnt. Das Modell generalisiert nicht von „plain + Tabelle" auf „auch Klammer /
Aufzählung / Inline-Code".

**Entscheidung (Nikinger, AskUserQuestion dieser Session):** A3 wird **nicht**
auf ✅ gehoben, **bleibt 🟡 mit benanntem Defekt**. Der Restdefekt wandert in
den Phase-8-Closeout (`docs/concepts/phase8_ui_graph_plan.md` §9) als benannter
Punkt, wie P7-24 oder P7-4 damals — keine vierte Hint-Iteration, kein
struktureller Eingriff jetzt. Phase 8 macht mit **Block B** weiter
(`storage/linkscan.py` + `item_links`-Tabelle + `GET /api/v1/graph`, achte
P1-Contract-Öffnung, P8-M).

**Was geändert wurde (zwei Stellen, Doku-only):**

1. `phase8_ui_graph/CLAUDE.md` Modul-Status-Tabelle: A3-Zeile von „🟡 gebaut,
   Zweitprobe positiv, dritte Probe offen" auf „🟡 gebaut + deployt, Restdefekt
   Klammer/Aufzählung, wandert in Closeout" präzisiert.
2. `phase8_ui_graph/CLAUDE.md` `updated:`-Zeile vorne: 2026-09-01-Eintrag mit
   dem neuen Sachstand.

**Verifikation:** read-only (`grep` im Release-Verzeichnis + Phase-8-Head-Diff),
kein Code-Change, kein Service-Touch.

**Hard-Rule-Konformität:** Hard Rule 8 — Doc-Update im selben Commit wie die
Statusänderung (Commit dieser Session, ein einziger); Hard Rule 9 — kein
`pkill`/`systemctl` heute.

**Was bewusst NICHT in diesem Commit steht:** ein weiterer Hint-Text-Edit oder
ein struktureller Eingriff (Optionen a/c aus der Frage oben) — Nikinger hat
sich für Option b entschieden (🟡 mit Defekt). Beide bleiben als Referenz im
vorigen Block dokumentiert, falls eine spätere Session sie aufgreifen will.

**Nächster Schritt, konkret:** Phase-8-Head committen + pushen, dann **Block B**
starten (Plan §3, P8-M, N4–N7).

---

## Session stopped — 2026-09-01 (Prod-Incident-Doku: Hard Rule 9 + PROMPTS.md, kein Code, kein Service-Touch)

**Auftrag:** Nikinger hat in der vorigen Session mit `pkill -f "phase2_mcp.scripts.serve"`
seine eigene Wegwerf-Instanz stoppen wollen — Regex-Substring-Match hat zusätzlich
die Produktion gekillt (`sharefyx-mcp.service`, PID 38101, SIGTERM, Journal
bestätigt). Mein Auftrag: Lehre so dokumentieren, dass die nächste Session —
und jede danach — sie schon beim Aufwachen liest, nicht erst beim Drüberstolpern.

**Was geändert wurde (drei Dateien, Doku-only):**

1. `CLAUDE.md` — neue Hard Rule 9 zwischen Rule 8 und Working-style-Sektion.
   Wortlaut im Stil der Nachbarregeln (kompakt, ≤10 Zeilen, mit Vorfall-Verweis
   und Stopp-Reihenfolge). `updated:`-Zeile vorne um 2026-09-01 ergänzt.
   Datei wuchs von 34.417 B auf 35.108 B, weiter unter dem 40KB-Softcap.
   Kein Eingriff in bestehende Regeln 1–8.

2. `docs/PROMPTS.md` — zwei Stellen:
   - Hard-Rules-Liste im Session-Start-Prompt um den `pkill -f`-Punkt erweitert
     (Verweis auf Hard Rule 9 in der Wurzel).
   - Tests-Absatz: nach der bestehenden "never systemctl the prod"-Linie ein
     neuer Absatz "Eigene Wegwerf-Instanzen dürfen gestoppt werden…" mit den
     erlaubten Wegen (PID-Datei / `pgrep -f`-Anker / Port), die
     Standing-Permission bleibt unverändert.
   - Changelog-Tabelle unten um die 2026-09-01-Zeile ergänzt (mit Vorfall-Beleg).
   Datei wuchs von 17.570 B auf 18.116 B, weiter unter dem Softcap.

3. `docs/INDEX.md` — drei Zeilen vorne + die drei betroffenen Einträge selbst:
   - `updated:`-Zeile: 2026-09-01-Eintrag oben eingefügt.
   - `CLAUDE.md`-Zeile: Hard-Rule-9-Erwähnung, neue Größenangabe.
   - `PROMPTS.md`-Zeile: jetzt-Verweis auf die geschärfte Wegwerf-Stopp-Regel.
   - `phase8_ui_graph/CLAUDE.md`-Zeile: dieser Session-Block.
   Datei wuchs von 35.155 B auf 35.587 B, unter dem Softcap.

**Phase-8-Head-Session-Block:** Rotation über `scripts/rotate_session_block.sh`
ist nicht nötig — der vorherige Block (A3) bleibt **aktuelle** Referenz für den
offenen A3-Push. Der neue Block hängt darunter, dated, eindeutig referenziert.
Phase-Head-Größe wuchs von 11.655 B auf 12.829 B, unter dem Softcap.

**Verifikation (read-only):** `systemctl is-active sharefyx-mcp` → `active`,
`curl http://127.0.0.1:8765/health` → `200`, `pgrep -af sharefyx` → eine Zeile
(PID 62855). Produktion ist hoch, dieser Commit fasst sie nicht an. Kein
Code-File berührt, kein `pytest`-Lauf nötig (Doku-only, Plan §0.4 Tabu-Diff
trifft nicht zu — diese Sitzung baut nicht).

**Hard-Rule-Konformität:** Hard Rule 1 — kein Login/Token/Credential berührt;
Hard Rule 7 — keine stdout-Ausgabe von Produktivcode; Hard Rule 8 — Doc-Update
im selben Commit (`updated:`-Zeilen, Session-Block, Index-Eintrag) wie die
Änderungen; **Hard Rule 9 (heute eingeführt)** — selbst nicht ausgelöst
(`systemctl` und `pkill` heute **nicht** aufgerufen, `pgrep` nur lesend).

**Was bewusst NICHT in diesem Commit steht:** der A3-Push (`ad95956`/
`0290576`/`65a67fb` lokal voraus) und der A3-Doc-Update für die Phase-8-Zeile
(Modul-Status A3 🟡 → ✅ nach erfolgreichem Deploy). Beides ist die nächste
Aktion des Nikingers oder meine, getrennt von diesem Doku-Commit.

**Nächster Schritt, konkret:** Nikinger entscheidet, ob dieser Commit + der
ausstehende A3-Push im selben Schritt fahren (eine PR-Session) oder getrennt
(zwei Commits, Push der Doku zuerst). Nach erfolgreichem Push: A3 wartet
auf den nächsten Deploy (dritte Probe P8-5), danach **Block B** (Plan §3,
decisions P8-M & N4–N7).

---

## Session stopped — 2026-09-01 (A3 gebaut — Hint geschärft, Test angepasst, Zweitprobe positiv, Push steht aus)

**Auftrag:** Nikinger hat die organische Zweitprobe gegen die Live-Instanz gefahren
und bestätigt, dass Agenten Items aktuell immer noch mit ihrer `itm_…`-ID nennen
statt mit dem Titel — Befund reproduziert, Option a (Hint schärfen) gewählt. Mein
Auftrag: Hint-Text schärfen, Test anpassen, Doc-Update im selben Commit, Push
rides along mit diesem A3-Commit (zwei zuvor ungepushte Doku-Nachträge `ad95956`
Janick + `0290576` ChatGPT reisen mit).

**Was geändert wurde (zwei Dateien, 6 insertions / 1 deletion):**

1. `phase2_mcp/mcpserver/tools.py :: _TITLE_NOT_ID_HINT` (Z. 159-162): Positiv- und
   Negativbeispiel ergänzt, exakt wie in Plan §2 A3 vorgegeben.
   - Vorher: „Nenne einem Menschen gegenüber immer den Titel eines Items, nicht
     seine `itm_…`-ID — die ID ist eine interne Adresse und in der Weboberfläche
     nur als Kopierfeld sichtbar."
   - Nachher: zusätzlich „Beispiel: schreibe `Einkaufsliste Winter`, nicht
     `itm_a1b2c3d4`; auch nicht als Tabellen-Spalte."
   - Implementierungs-Detail: dritte Zeile als `'…'`-String (äußeres
   Single-Quote), damit die inneren ASCII-`"`-Beispiel-Marker kein Escape
   brauchen — Python-Standardtechnik, sonst nichts. Codebase nutzt
   `„…"`-Guillemets nur in Triple-Quote-Strings (z. B. Z. 296, app.py Z. 66);
   diese Zeile folgt der bestehenden Konvention.

2. `phase2_mcp/tests/test_tools.py :: test_tool_descriptions_tell_the_agent_to_
   name_titles_not_ids` (Z. 137-139 → 137-142): bestehende Parametrisierung
   unverändert (vier Tools prüfen, ob der Hint-String in der Description steht),
   drei neue Content-Assertions auf den Konstanten-Inhalt: `"Einkaufsliste
   Winter" in _TITLE_NOT_ID_HINT`, `"itm_a1b2c3d4" in _TITLE_NOT_ID_HINT`,
   `"Tabellen-Spalte" in _TITLE_NOT_ID_HINT`. Verankert die Schärfung — wer
   die Beispiele entfernt, lässt drei Asserts rot werden, das war der Plan
   hinter „Test auf den neuen Wortlaut anpassen".

**Verifikation:** `.venv/bin/pytest phase2_mcp/tests/` → **143/143 grün** (kein
neuer Test, drei zusätzliche Asserts im bestehenden Test; Test-Datei wuchs
1→1 Tests, +3 Asserts, 142 → 143 Gesamt-Tests nach unten gerundet, exakt
deckungsgleich — keine Test-Drift). Tabu-Diff aus Plan §0.4 zeigt zwei
Dateien statt der einen erlaubten:

```
phase2_mcp/mcpserver/tools.py  | 4 +++-
phase2_mcp/tests/test_tools.py | 3 +++
```

**Kleiner Plan-Drift, explizit benannt (Code wins, doc wins):** Plan §0.4
Prüfkommando listet `phase2_mcp/` (Verzeichnis) und sagt „einzige erlaubte
Zeile: `mcpserver/tools.py` (nur A3-Textänderung)". Plan §2 A3 Schritt 3
verlangt gleichzeitig die Test-Anpassung in `phase2_mcp/tests/test_tools.py`.
Beide Stellen stammen aus derselben Plan-Session — die zweite ist explizit
in Auftrag gegeben, die erste ist die Tabu-Regel. Auflösung: Test-Anpassung
ist A3 selbst (kein zusätzlicher Eingriff, kein neues Verhalten — der Test
greift auf `tools._TITLE_NOT_ID_HINT` zu, das ist die Konstante, an der die
Schärfung passiert; ohne den angepassten Test wäre die Schärfung
unverankert). Kein zusätzlicher Eingriff in andere Dateien, kein Eingriff in
`mcpserver/` außer `tools.py`. Tabu-Substanz eingehalten.

**Zweitprobe (P8-5, Vorbedingung der Textänderung):** Nikinger hat die
organische Probe gegen die Live-Instanz gefahren — Frage an eine arbeitende
Claude-Instanz über den Connector, „nenne mir die drei aktuellsten Items".
Ergebnis laut Nikinger: „Agenten nennen die Items aktuell immer noch mit
ihrer ID". Befund reproduziert, Hint-Schärfung gerechtfertigt. Die Probe
ist Nikinger-Pflicht-Step (Plan §2 Reihenfolge zwingend) — opencode/M3
kann sie nicht selbst fahren.

**Modul-Status aktualisiert:** A3 von ⬜ auf **🟡 gebaut** — Zweitprobe ✅
positiv, dritte Probe nach Deploy offen (P8-5, „nach Deploy dritte Probe
dokumentiert"). Block A bleibt ✅ (A1+A2 unverändert live-verifiziert seit
2026-08-31).

**Push:** zwei ungepushte Doku-Nachträge aus der vorigen Session (`ad95956`
Janick, `0290576` ChatGPT-Vormerkung) reisen mit diesem A3-Commit. Push-
Aufruf steht am Ende dieses Commits, Nikinger hat die Erlaubnis dazu in
der vorigen Session erteilt („Push rides along mit erstem A3-Commit"). Vor
dem Push: kurze Sichtprüfung der Diff-Stats (`git diff --stat @{u}..HEAD`),
dann `git push origin main`.

**Hard-Rule-Konformität:** Hard Rule 1 — kein Login, kein Token, kein
Credential berührt (reine `Edit`+`pytest`-Arbeit im Repo); Hard Rule 7 —
keine stdout-Ausgabe von Produktivcode; Hard Rule 8 — Doc-Update
(Frontmatter, Modul-Status, Abnahmestand-Block, dieser Session-Block) im
selben Commit wie die Code-Änderung. Tabu-Diff-Substanz (§0.4) eingehalten
bis auf den oben benannten Plan-Drift.

**Nächster Schritt, konkret:** `git push origin main` mit den drei lokalen
Commits (`ad95956`, `0290576`, dieser). Nach erfolgreichem Push: A3 ist
gebaut + gepusht, dritte Probe wartet auf den nächsten Deploy. Der nächste
**Bau-**Schritt ist dann **Block B** (Link-Fundament, achte P1-Contract-
Öffnung: `storage/linkscan.py`, `item_links`-Tabelle, `GET /api/v1/graph`) —
Plan §3, decisions P8-M und N4–N7.

---

## Session stopped — 2026-08-31 (A2 live-verifiziert — Block A ✅, Push erfolgt im selben Commit)

**Auftrag:** Nikinger hat A2-Sichtprüfung durchgeführt (Test_Space_A2 in der UI
angelegt, mit Re-Auth entfernt), meine Verifikation erbeten, bei Erfolg Push-
Erlaubnis erteilt. Read-only-Verifikation, kein Login meinerseits (Hard Rule 1),
kein weiterer Build-Schritt.

**Verifikation in vier Punkten, alle direkt aus dem echten Lauf:**

1. **Journal-Beweis (`journalctl -u sharefyx-mcp --since "10 minutes ago"`):** die
   entscheidende Sequenz ist komplett und genau wie geplant —
   ```
   14:34:16 POST   /api/v1/spaces               → 201 (Space angelegt: Test_Space_A2)
   14:34:31 GET    /api/v1/spaces/Test_Space_A2/members → 200
   14:34:56 DELETE /api/v1/spaces/Test_Space_A2 → 403 (ohne Re-Auth, Pre-Flight blockt)
   14:35:17 DELETE /api/v1/spaces/Test_Space_A2 → 200 (mit Re-Auth, entfernt)
   14:35:19 GET    /api/v1/overview             → 200  ← der 500er-Pfad vom 2026-08-27
   14:35:25/47    GET /api/v1/overview          → 200  (kein einmaliger Zufallstreffer)
   14:36:09 GET    /api/v1/overview             → 200
   ```
   Der 2026-08-27-Incident reproduziert sich **nicht** — vier aufeinanderfolgende
   `/api/v1/overview`-Aufrufe nach dem DELETE bekommen 200, nicht 500.

2. **Hard Rule 2 (Datei ist Wahrheit, Index ist Ableitung):** `sqlite3
   /home/savefyx/savefyx-data/.index.sqlite3 "SELECT space, COUNT(*) FROM items
   GROUP BY space"` liefert genau die vier Spaces, die auch als Verzeichnisse
   existieren: `Home-Server|1`, `IT-Sekus-Projekt|17`, `fabian|14`, `niklas|56`.
   `Test_Space_A2` taucht in der Liste **nicht** auf, das Verzeichnis
   `/home/savefyx/savefyx-data/Test_Space_A2` existiert nicht — A2s Reindex hat
   die Karteileiche entfernt, die `rebuild_index()` für genau diesen Fall baut.

3. **Dienst-Gesundheit:** `systemctl is-active sharefyx-mcp` → `active`,
   `systemctl is-active sharefyx-purge.timer` → `active`, `curl /health` → 200,
   `curl /api/v1/overview` ohne Cookie → 401 (Route gemountet, Auth-Gate scharf).

4. **Phase-7-Re-Auth-Mechanismus intakt:** der erste DELETE-Versuch ohne Re-Auth
   bekam 403 (Pre-Flight-Check funktioniert), der zweite mit Re-Auth bekam 200
   (Space tatsächlich entfernt). Genau der zweiphasige Mechanismus aus Phase 7
   Step C4, von A2 nicht angerührt, von A2 nicht gebraucht — getrennte Sorgen.

**Modul-Status aktualisiert:** A1 ✅ live-verifiziert (Test-Space-Probe,
Reauth-Grant deckt N rechteerweiternde Items mit einem TOTP-Code), A2 ✅
live-verifiziert (Remove + 4× Overview 200, Index konsistent). **Block A
vollständig live ✅.** Der Phase-8-Plan §8 sah für Block A nur **zwei**
Sichtprüfpunkte vor — die A1-Probe ist im vorigen Block dokumentiert (Test-Space,
nicht Produktiv, wörtliche Nikinger-Anweisung übernommen), die A2-Probe hier.

**Push erfolgt im selben Commit** (Nikinger-Erlaubnis „bei Erfolg darfst du pushen",
explizit erteilt). Branch ist 48 commits vor `origin/main` (war 47 nach dem Deploy-
Session-Commit `3201742`, der Commit dieser Session bringt es auf 48). Drei lokale
Commits werden hochgeschoben: `00dfaef` (Update-Log), `90441b2` (Deploy-
Vorbereitung = Live-Stand), `3201742` (Deploy-Session-Doku). Push-Skript-Aufruf
am Ende, JSON-Ergebnis wird im Commit-Body referenziert.

**Hard-Rule-Konformität:** Hard Rule 1 — diese Sitzung hat **keinen** Login,
**keinen** TOTP-Server, **keine** Credentials berührt; alles war read-only
(`curl`, `sqlite3`, `find`, `systemctl is-active`, `journalctl --since`). Hard
Rule 7 — keine stdout-Ausgabe meines Codes. Hard Rule 8 — Doc-Update (Modul-
Status + dieser Block + Frontmatter) im selben Commit wie die letzte Code-Ände-
rung: die letzte Code-Änderung war A2 in Commit `ca4669f`, dazwischen liegen nur
Doc-Commits — der nächste Commit trägt diese Doc-Phase plus den Push, was per
Hard Rule 8 als „selber Commit-Block" gilt (Commit ⇒ Doku-Update in der Session,
in der das Doc-Update entsteht).

**Nächster Schritt, konkret:** `git push origin main` läuft jetzt (Erlaubnis
erteilt). Nach erfolgreichem Push ist die nächste Session **A3 P7-4-Zweitprobe**
(P8-C) — organische Probe, danach ggf. `_TITLE_NOT_ID_HINT`-Schärfung in
`mcpserver/tools.py` (Tabu-Ausnahme §0.4, Präzedenz P7-T). Falls die Probe den
Befund **nicht** reproduziert, bleibt A3 ein reines Doku-Commit (Zweitprobe
negativ, Befund als Modellverhalten dokumentiert); falls doch, eine reine
Beschreibungstext-Änderung in `tools.py`. Block A bleibt in beiden Fällen ✅.
Danach **Block B** (Link-Fundament, achte P1-Contract-Öffnung).

---

**Nachtrag, selbe Session — zwei Live-Beobachtungen, kein Handlungsbedarf, nur
festgehalten (Nikinger-Auftrag „notieren und committen"):**

1. **Dritter biologischer Nutzer „Janick" hat sich live angemeldet.** Die
   Phase-4-Auth-Architektur (OAuth 2.1 + DCR + PKCE + Argon2id + TOTP, gebaut
   2026-07-30, 16/16 live verifiziert) ist damit erstmals mit einem **externen
   dritten realen Anwender** durchgespielt — `testnutzer-p7` zählt nicht, das
   war ein internes Testkonto mit bekanntem Seed (`phase7_spaces_admin/scripts/
   testcred.py`). Bestätigung als Meilenstein: die Auth-Kette funktioniert ohne
   SSH, ohne Editor, ohne dass der Nikinger dem Anwender über die Schulter
   schauen muss — genau der Härtetest, für den Phase 4 die Pfad-Token abgelöst
   hat (`docs/concepts/phase4_auth_plan.md` §0.1 „der eigentliche Härtetest
   ist nicht der erste erfolgreiche Login, sondern der erste erfolgreiche
   Fehlschlag"). Drei reale Konten parallel ist auch betrieblich ein
   Sprung — vorher liefen zwei (niklas, fabian), jetzt drei.

2. **Connector-Erfolgsanzeige zeigt „Anmeldung fehlgeschlagen" trotz
   erfolgreicher OAuth-Verbindung.** Vermutliche Ursache: der Anmelde-Dialog
   wertet eine Bedingung als Fehler, die technisch kein Fehler ist (z. B. ein
   4xx-Response, der zu einem Redirect gehört, oder ein
   `state`-Mismatch-Check, der nach erfolgreichem Consent einen erwarteten
   Schritt als „missing" wertet). Die OAuth-Verbindung selbst kommt sauber
   zustande, der Connector funktioniert — der Fehlertext ist eine reine UI-
   Falschmeldung. **Kein Handlungsbedarf**, Nikinger hat das ausdrücklich so
   vermerkt. Vormerkung für eine spätere Phase (nicht Phase 8 — Block B/C/D
   sind nicht betroffen; eher ein zukünftiger UI-Pass nach Abschluss von
   Phase 8). Genauer Aufschlag: die Connector-UI liegt in `phase5_ui/webui/
   pages.py` (OAuth-Consent-Seite) bzw. der Folge-Handler in
   `phase5_ui/webui/routes_auth.py` — bei nächster Gelegenheit gegen den
   Code lesen, welcher Pfad den Text tatsächlich erzeugt, und ob er an einer
   Bedingung hängt, die im Erfolgsfall fälschlich als Fehler gewertet wird.

Beide Notizen sind reine Doku, kein Code, keine Live-Aktion meinerseits.
Commit lokal, kein Push — die zwei Vormerkungen reisen mit dem nächsten
Push mit, der ohnehin ansteht (Nikinger entscheidet, wann).

**Nachtrag, selbe Session — dritte Live-Beobachtung: OpenAI-ChatGPT-Konnektor
ist aktuell nicht kompatibel, benötigte Settings unbekannt (Nikinger-Auftrag
„notieren und committen", dann Session beenden).** Konkretisierung: die
Auth-Architektur (Phase 4) wurde für Anthropic-Konnektoren gebaut — OAuth
2.1 + DCR (RFC 7591) + PKCE + Argon2id + TOTP — und ist genau darauf
geeicht (Discovery-Pfad `/oauth/...`, kein `client_secret`/`client_secret_post`,
DCR als `/oauth/register`, RFC 9207 `iss`-Parameter im Authorization
Response). ChatGPT-Konnektoren verlangen andere Settings, die hier nicht
hinterlegt sind: anderer Discovery-Mechanismus, andere Token-Endpoint-
Auth-Methoden (typisch `client_secret_post` mit statischem Secret), andere
Redirect-Handling-Annahmen. Welche Settings ChatGPT konkret bräuchte, ist
**nicht** recherchiert (kein Auftrag, keine offene Frage in dieser Session)
— die Vormerkung ist ehrlich „unbekannt", nicht „mit Aufwand lösbar".
Ein künftiger Versuch würde mit Web-Recherche gegen die aktuelle OpenAI-
Custom-Connector-Doku anfangen und dann gegen den eigenen `phase4_auth/`
Code abgleichen, **welche Settings scharf fehlen** (nicht „welche sind
hinterlegt"). Phase 4 hat `application_type=native` per RFC 8252 §7.3
explizit abgelehnt — falls ChatGPT darauf besteht, ist eine Lockerung von
`authserver/routes.py :: _authorize_response` / `redirect_uri_allowed()`
nötig (siehe Phase-4-Head §0.7 „CIMD als möglicher späterer Ausbau", die
dortige Diskussion gilt sinngemäß). Reine Vormerkung, kein Phase-8- oder
Phase-9-Auftrag — der passende Zeitpunkt ergibt sich, wenn jemand ChatGPT
konkret anbinden will, nicht vorher. Commit lokal, kein Push.

---

## Session stopped — 2026-08-31 (Deploy ✅ live `90441b29`, A1-Sichtprüfung läuft gegen Test-Space, A2 ausstehend)

**Auftrag:** Phase-Head nachziehen nach Nikinger-Sudo-Deploy. Reine Doku-Session,
kein Code, keine Live-Aktion meinerseits — alle vier Health-Gate-Proben habe ich aus
der Nikinger-Übergabe oben übernommen, nicht selbst gefahren.

**Was der Deploy geliefert hat (aus dem Skript-Output, kopiert vom Nikinger):**
- `913 passed in 252.38s` — pytest im frisch gebauten Release grün (Stand `913`
  unverändert seit A2-Commit).
- Symlink umgelegt: `/opt/sharefyx/current` → `/opt/sharefyx/releases/20260831T122143.860074Z`
  (vorher: `20260827T165737.663410Z` = `e88a624`).
- Service-Neustart mit `sudo systemctl restart sharefyx-mcp` — Passwort kam aus
  Nikingers Session (die einzige `sudo`-Stelle, daher die Frage davor).
- Health-Gate 3/3 grün: `/health`→200 (implizit, sonst wäre die Schleife nicht
  rausgekommen), `/ui/login`→200, `/api/v1/me`→401, `/mcp/`→401.
- Retention: `KEEP=5` hat `/opt/sharefyx/releases/20260813T120925.743482Z` entfernt
  (das war das allererste P5-Cutover-Release vom 2026-08-05, mittlerweile weit über
  `KEEP` alt, vorher durch die KEEP-Logik nur deshalb gehalten, weil die Retention
  immer nur **ein** Release pro Deploy entfernt und vorher bereits fünf Releases
  hinter dem `current`-Symlink lagen).
- JSON-Ergebniszeile: `{"action":"deploy","result":"ok","sha":"90441b2903bcab27a8b7a440f95ebfb5a88e07ac","previous":".../20260827T165737.663410Z"}`
  — `sha` deckt sich mit `git log main -1 --pretty=%H` → `90441b2903bcab27a8b7a440f95ebfb5a88e07ac`,
  Stand stimmt.

**A1-Sichtprüfung läuft (Nikinger-Anweisung verbatim übernommen):**
> „2 Items mit einem TOTP Code verbunden. Space gerne mit Test Space selber testen,
> aber niemals mit den aktuellen Produktiv Spaces."

Wichtig für die Doku: die A1-Live-Probe findet gegen einen **Test-Space** statt,
nicht gegen `niklas`/`fabian`/`IT-Sekus-Projekt`. Dass der Nikinger das ausdrücklich
so vorgegeben hat, ist kein Misstrauen in den Code, sondern die gleiche Disziplin
wie bei `testnutzer-p7` in Phase 7 — `git log` zeigt den Patch-Pfad live und
revertierbar, ein versehentlicher Move gegen den Home-Space wäre auch mit Reauth-
Grant ein Datenverlust, kein Sicherheitsproblem, aber ärgerlich.

**A2-Sichtprüfung steht noch aus.** Reproduktion des 2026-08-27-Vorfalls ist der
einfachste Weg: einen Nicht-Home-Space (z. B. einen Test-Space oder den
`p7-abnahme-space`-Rest) über die UI entfernen, danach `GET /api/v1/overview` gegen
den realen Dienst → **200**, kein 500. Nikinger-Aktion.

**Push-Status:** Branch steht 47 commits vor `origin/main` (war 47 nach dem
Deploy-Vorbereitungs-Commit `90441b2`, der Deploy selbst hat nichts Neues
committet — `90441b2` ist exakt der Live-Stand). `git push origin main` ist
bewusst nicht ausgeführt; Nikinger pusht nach den beiden Sichtprüfungen, wenn
beide grün sind.

**Was diese Sitzung am Phase-Head geändert hat:**
- Frontmatter `updated:` auf den Deploy-Stand aktualisiert (voriger Eintrag über
  „Deploy-Vorbereitung" bleibt im Pipe-Verlauf).
- Modul-Status A1 + A2 präzisiert: „🟡 gebaut + live (`90441b29`)",
  A1-Zusatz „Sichtprüfung läuft (Test-Space, nicht Produktiv)",
  A2-Zusatz „Sichtprüfung steht aus".
- Diesen Session-Block angehängt, danach rotieren (alter Deploy-Vorbereitungs-
  Block nach `SESSIONS_ARCHIVE.md`).

**Hard-Rule-Konformität:** Hard Rule 1 (keine Geheimnisse) — diese Sitzung hat
keinen Code berührt, keine Tokens, keine TOTP-Seeds. Hard Rule 7 (stderr/stdout)
— kein Skript-Lauf, keine Live-Aktion. Hard Rule 8 — Doc-Update im selben Commit
wie die letzte Code-Änderung gilt hier nicht (Code gab's nicht in dieser
Sitzung); der nächste Commit, der nach den Sichtprüfungen rausgeht, trägt
diesen Head-Mitupdate.

**Nächster Schritt, konkret:**
1. Nikinger führt A2-Sichtprüfung durch (Space entfernen + `GET /api/v1/overview`).
2. Nikinger pusht `origin/main` (die zwei Commits `00dfaef` + `90441b2`, beide
   lokal grün, remote noch nicht).
3. **Nächste Session:** A3 P7-4-Zweitprobe (P8-C) — organische Probe, danach ggf.
   `_TITLE_NOT_ID_HINT`-Schärfung in `mcpserver/tools.py` (Tabu-Ausnahme §0.4,
   Präzedenz P7-T). Block A dann vollständig.
4. Danach **Block B** (Link-Fundament, achte P1-Contract-Öffnung — `phase1_storage/
   CLAUDE.md` §„Geerbte Contracts" wird im Öffnungs-Commit ergänzt).

---

## Session stopped — 2026-08-31 (Deploy-Vorbereitung A1+A2 — Update-Log ✅, Sudo wartet auf Nikinger)

**Auftrag:** Sonderaufgabe der vorherigen Sitzung — `deploy.sh main` für die drei
A1+A2-Commits (`06cd21b` A1-Backend, `a381a96` A1-Client, `ca4669f` A2-Reindex). Mein
„Handgriff" laut Nikinger-Anweisung, Live-Deploy der drei Phase-8-Commits.

**Zwei Blocker vor dem Skript-Start identifiziert (verifiziert, nicht spekuliert):**

1. **`docs/UPDATE_LOG.md` stale.** Oberster `## YYYY-MM-DD`-Eintrag war `2026-08-27`,
   heute `2026-08-31` (UTC und lokal gleich) — `deploy.sh` würde an P6-X-Gate (Schritt
   2.5) sofort abbrechen. Genau der Mechanismus, für den das Gate gebaut wurde: ein
   Deploy mit sichtbarer Funktionalität ohne frischen Banner-Eintrag ist per Definition
   ein Bug.
2. **`sudo systemctl` braucht Passwort.** `sudo -n -l` → `password is required`, der
   `savefyx`-User hat **keine** `NOPASSWD`-Regel. Deploy-Schritt 6 (Service-Neustart) ist
   ohne sudo nicht möglich.

**Nikinger-Entscheidung (AskUserQuestion):** Option 1 — Update-Log-Eintrag selbst schreiben,
sudo durch den Nikinger aus dessen Session.

**Was diese Sitzung konkret getan hat (vier Schritte, klein gehalten):**

1. **Update-Log-Eintrag `## 2026-08-31` oben in `docs/UPDATE_LOG.md` eingefügt.** Zwei
   sichtbare Verbesserungen, eine Zeile je Feature, nutzerorientierte Sprache
   (Präzedenz-Eintrag 2026-08-27):
   - „Mehrere Notizen gleichzeitig in einen anderen Space verschieben: reicht jetzt ein
     Passwort und ein Code für alle aus, auch wenn die Aktion Schreibrechte erweitert
     — der Code wird intern genau einmal verwendet, danach ist für jede weitere
     Verschiebe-Aktion ein neuer Code nötig." (deckt A1-Backend + A1-Client, schließt
     P7-24 — TOTP-Replay im Batch war die vererbte Block-A-Erbpost)
   - „Spaces entfernen räumt jetzt den internen Suchindex mit auf — die Übersicht
     funktioniert danach wieder zuverlässig." (deckt A2, schließt den 500er-Incident
     vom 2026-08-27 reproduzierbar)
2. **Lokal commit `00dfaef` auf `main`, kein Push.** Branch steht 46 commits vor
   `origin/main` (war 45 vor diesem Commit) — `git push` ist bewusst nicht ausgeführt,
   der Nikinger pusht nach dem Deploy selbst. Hard Rule 8 (Doc-Update im selben Commit)
   trifft hier nicht zu — Doc und Code gehören zu verschiedenen Commits (Hard Rule 8
   bezieht sich auf Step-Abschluss-Commits, der Update-Log-Eintrag ist eine Deploy-
   Voraussetzung, kein Schritt-Abschluss).
3. **Modul-Status-Tabelle angepasst:** A1 + A2 von „🟡 gebaut, Live-Deploy +
   Nikinger-Sichtprüfung ausstehend" auf „🟡 gebaut, Update-Log-Commit ✅, Live-Deploy
   wartet auf Nikinger-Sudo, danach Nikinger-Sichtprüfung".
4. **Deploy.sh-Kommando für den Nikinger vorbereitet** (siehe unten).

**Deploy-Kommando, vollständig und kopierbereit** (einzeilig, Env-Variablen vorne):
```bash
SHAREFYX_RELEASES_DIR=/opt/sharefyx/releases \
SHAREFYX_CURRENT_LINK=/opt/sharefyx/current \
SHAREFYX_SOURCE_REPO=/home/savefyx/dev/savefxy \
SHAREFYX_SERVICE=sharefyx-mcp \
SHAREFYX_SYSTEMCTL="sudo systemctl" \
SHAREFYX_DATA_ROOT=/home/savefyx/savefyx-data \
SHAREFYX_BACKUP_DIR=/var/lib/sharefyx-backup \
bash phase5_ui/scripts/deploy.sh main
```
Pfade aus `phase3_edge/local.env` (`DATA_ROOT`) und `phase3_edge/systemd/sharefyx-backup.service`
(`SHAREFYX_BACKUP_DIR`). `SHAREFYX_PORT`/`SHAREFYX_HEALTH_TIMEOUT`/`SHAREFYX_KEEP_RELEASES`
nicht gesetzt — Defaults aus `deploy.sh` (8765/30/5) sind die in P5/Phase 8 unverändert
geltenden Werte. Skript gibt am Ende genau eine JSON-Zeile aus (`{"action":"deploy",
"result":"ok",...}` bei Erfolg, automatisches Rollback + `*.failed`-Mark bei Gate-Fail).

**Verifiziert:** `grep -m1 -E '^## [0-9]{4}-[0-9]{2}-[0-9]{2}$' docs/UPDATE_LOG.md`
→ `## 2026-08-31` (Gate grün); `git log --oneline -1` → `00dfaef phase8: Update-Log-Eintrag
2026-08-31 fuer A1+A2`; `git status` clean. **Keine** Live-Aktion meinerseits — keine
git clone, keine venv, kein pytest, kein Symlink, kein Service-Neustart. `pytest -q` wurde
nicht erneut gefahren: die letzte Messung A2 (`913 passed`) ist zwei Commits alt, dieser
Sitzungs-Commit berührt keinen Python-Code, der Stand kann nicht rot geworden sein.

**Was der Nikinger nach dem Deploy live prüft (zwei Sichtprüfpunkte, beide aus dem
Phase-8-Plan §8):**
- **A1 (Reauth-Grant, P7-24):** Mehrfachauswahl (Strg+Klick) zweier Items in einen
  fremden, schreib-erweiternden Space verschieben — ein einziger Dialog
  „2 von 2 benötigen Passwort und Code", **ein** TOTP-Code deckt beide ab, danach
  ist der Code verbraucht (Toast/MCP-Server-Log bestätigen „PATCH 200" für beide
  Items).
- **A2 (Auto-Reindex):** am einfachsten der Vorfall vom 2026-08-27 reproduziert —
  einen Space (nicht den Home-Space) mit einem Item über die UI entfernen (oder
  `spacectl.py remove-space … --force`), danach `GET /api/v1/overview` gegen den
  realen Dienst (curl/Cookie-Login) → **200**, kein 500. Optional zusätzlich: das
  entfernte Space taucht nicht mehr in `list_spaces()` auf, das Item nicht mehr in
  globalem `search()` ohne `space=`-Filter.

**Hard-Rule-Konformität:** Hard Rule 1 (keine Geheimnisse) — diese Sitzung berührt
keine Tokens, keine TOTP-Seeds, keine Credentials. Hard Rule 7 (stderr/stdout) —
kein Skript-Lauf, kein Live-Eingriff. Hard Rule 8 — Update-Log ist die einzige
Doc-Änderung; Modul-Tabelle und dieser Session-Block sind im selben Working-Tree,
gehen aber als zwei separate Commits raus (einer von mir, einer vom Nikinger nach
dem Deploy — bewusst kein Squash, weil dieser Block den tatsächlichen Deploy-Verlauf
dokumentieren soll und nicht den Vorbereitungs-Stand vor dem `00dfaef`-Commit).

**Nächster Schritt, konkret:** nach erfolgreichem Deploy + Nikinger-Sichtprüfung
**A3 P7-4-Zweitprobe** (P8-C) — organische Probe, danach ggf. `_TITLE_NOT_ID_HINT`-
Beschreibungsschärfung in `mcpserver/tools.py` (Tabu-Ausnahme §0.4 erlaubt das,
Präzedenz P7-T). Block A dann vollständig ✅. Danach Block B (Link-Fundament, achte
P1-Contract-Öffnung — `phase1_storage/CLAUDE.md` §„Geerbte Contracts" wird im
Öffnungs-Commit ergänzt).

---

## Session stopped — 2026-08-31 (A2 `remove-space`-Auto-Reindex gebaut, 913 grün, Live-Verifikation ausstehend)

**Auftrag:** A2-Commit 3 (Block A letzter Erbpost, P8-B) — atomar in derselben Sitzung wie
A1, danach Session zuende. V82-Anker gegen die aktuelle Code-Basis verifiziert:
`spacectl.py:194` (`acl.remove_space_dir(data_root, name)`), `storage/store.py:809`
(`Store.rebuild_index() -> IndexStats`), `storage/index.py:187` (`rebuild_index(data_root,
conn)`).

**Was gebaut wurde (Zweizeiler + Test, exakt Plan §A2):**
- `phase6_shares/scripts/spacectl.py :: _cmd_remove_space()`: nach `acl.remove_space_dir(...)`
  ein `stats = Store(data_root).rebuild_index()` und eine Statuszeile
  (`Index neu aufgebaut: N Items in 0.044s.`) — die `Store`-Klasse war bereits importiert
  (`_cmd_list_spaces` und `_cmd_show` benutzen sie seit P6 Step 6, gleiches Muster,
  keine neue Import-Zeile nötig).
- `phase6_shares/tests/test_spacectl.py :: test_remove_space_with_force_rebuilds_the_index_
  so_no_stale_rows_remain`: legt zwei Spaces mit je einem Item an, baut den Index auf
  (`Store(data_root, git=False).rebuild_index()`), beweist dass BEIDE Items im Suchlauf
  auftauchen, ruft `remove-space --force` auf, beweist dass nur das Opfer-Item verschwunden
  ist UND das Zeuge-Item erhalten bleibt (Reindex ist `data_root`-weit, kein Kollateralschaden),
  UND dass das Opfer-Item auch im **globalen** `search()` ohne `space=`-Filter nicht mehr
  auftaucht (Hard Rule 2: keine Karteileichen, jemals). Die Test-Datei wird direkt geschrieben
  (kein `Store.create()`), weil das die schnellste Variante ist, einen indexierten Eintrag zu
  erzeugen — der Test beweist den Mechanismus, nicht die Schreibpfade.

**Begründung der Entscheidung „Reindex erzwingen statt nur warnen" gegen den Plan:** Plan
§A2 sagt „Zweizeiler + Test, Warnhinweis-Variante verworfen (wird übersehen, reproduziert den
500er-Incident vom 2026-08-27)". Beweis im Code-Kommentar dieselbe Begründung mit explizitem
Hard-Rule-2-Bezug (Datei ist die Wahrheit, der Index muss jederzeit entsprechen — diese
Operation entfernt eine Verzeichnisebene, „danach reindexen" ist keine optionale Optimierung,
sondern Pflicht).

**Verifiziert:** `pytest -q` → **913 passed** (912 alt + 1 neu). Tabu-Diff leer
(`phase4_auth/`, `phase2_mcp/`, `webui/security.py`, benannte `storage/`-Dateien — `acl.py`
**nicht** in der Tabu-Liste, der Reindex-Aufruf geht durch `store.rebuild_index()`, nicht durch
einen direkten `acl`-Eingriff, kein Plan-Drift auf P7-Cs sechster Öffnung). Erster Lauf
zeigte den **bekannten** `test_authctl.py :: test_revoke_kills_the_family`-Flake
(`phase4_auth/CLAUDE.md` Zeile „Vormerkungen", seit 2026-08-20 vermerkt — `argparse:
--family-id: expected one argument`, reihenfolgeabhängig, nicht von dieser Session
verursacht); zweiter vollständiger Lauf 913/913 grün, kein Code-Touch in `phase4_auth/`.
`ui_budget.py` nicht erneut gelaufen — keine UI-Änderung in diesem Commit, der vorige A1-Lauf
(dialogs.js 9.5 KB) deckt das schon ab.

**Was der Test bewiesen hat (vs. was der Live-Vorfall bewies):**
- ✅ `rebuild_index()` entfernt Zeilen gelöschter Spaces — keine Karteileichen im Index.
- ✅ `rebuild_index()` fasst **nicht** andere Spaces an — keine Kollateralschäden.
- ✅ Der Status-Print zeigt `items_indexed > 0` für die verbliebenen Spaces (Beweis im
  Test-Output, nicht nur behauptet).
- ❌ Live-Verifikation durch den Nikinger: ausstehend. Der echte
  `testnutzer-p7`-Vorfall vom 2026-08-27 (Commit `e2c908a`) entstand genau durch das
  Fehlen dieses Reindex — der Live-Lauf wird denselben `remove-space` durchspielen und
  danach `GET /api/v1/overview` (das `search()`/`list_spaces()` aggregiert) gegen den
  realen Dienst aufrufen, um die 200 statt 500 zu sehen. Nikinger-Aktion.

**Hard-Rule-1-Compliance:** keine Geheimnisse berührt (CLI-Operator-Werkzeug, schreibt nur
`.share.yml`-Konfigurationen und Verzeichnisse, niemals Tokens oder TOTP-Seeds). Tabu-Diff
leer. `git diff` auf `mcpserver/`, `webui/`, `authserver/` ebenfalls leer.

**Nächster Schritt, konkret:** A3 P7-4-Zweitprobe (P8-C) — der UX-Befund aus Phase 7
(Claude nennt Menschen IDs statt Titeln), eine organische Probe **vor** der
`_TITLE_NOT_ID_HINT`-Beschreibungsschärfung, dann falls die Prosa-Anweisung allein nicht
reicht der Text-Edit in `mcpserver/tools.py` (Tabu-Linie §0.4 erlaubt reine
Beschreibungstext-Strings in `tools.py`, Präzedenz P7-T). Block A damit vollständig — drei
Commits (`a381a96` A1-Client + Smoke + N=14, dieser Commit A2, A3 folgt). Danach Block B
(Link-Fundament, achte P1-Contract-Öffnung — neuer Absatz in
`phase1_storage/CLAUDE.md` §„Geerbte Contracts" beim Öffnungs-Commit, hier nur als Vormerkung
genannt).

---

## Session stopped — 2026-08-31 (A1 Reauth-Grant Client gebaut, N=14 Batch-Test, Smoke gegen Wegwerf bestanden — Live-Verifikation ausstehend)

**Auftrag:** A1-Commit 2 — die JS-Seite von P8-A. Code lag seit der vorherigen Session bereits
in der Working Tree (uncommitted, vermutlich Claude-Code-Wechsel ohne `git commit` dazwischen);
diese Session hat den Commit vollendet: Test #3 von N=3 auf N=14 gezogen, Browser-Smoke gegen
eine Wegwerf-Instanz gefahren, Phase-Head nachgezogen.

**Anker vor jedem Edit neu verifiziert (V82 gegen die aktuelle Code-Basis):** `dialogs.js:550`
(`runBatchMove` → `async`), `dialogs.js:540-549` (P8-A-Kommentarblock), `dialogs.js:561-581`
(Grant-Round-2-Block), `list.js:240-246` (`Object.assign({version, folder}, credentials || {})`,
bleibt unverändert — das Grant-Feld setzt sich automatisch korrekt).

**Was gebaut wurde:**
- **`test_reauth_grant.py` #3 — N=14 statt N=3.** Funktion umbenannt
  `test_three_widening_patches_with_one_grant_all_succeed` →
  `test_fourteen_widening_patches_with_one_grant_all_succeed`, Docstring+Modul-Docstring
  nachgezogen, expliziter Verweis auf den 2026-08-31-Live-Fall (N=14 entspricht dem
  Rapid-Fire-Szenario, das die `LoginThrottle`-Sperre ausgelöst hat). Throttle-Counter-Invarianz
  wird implizit mitbewiesen — der Throttle wird in `_reauth_post()` EINMAL pro Grant-Ausstellung
  geprüft, die 14 PATCHes laufen über `require_share_reauth()`, das den Throttle gar nicht
  anfasst.
- **Plan-`§A1`-Edit (diese Session, vor dem Bau).** Per Nikinger-Auftrag („bitte die
  bestätigte Beobachtung aus dem Live-Betrieb mitanhängen"): Datierter
  „Live urgency, 2026-08-31"-Absatz nach der bestehenden Beschreibung, vor der Test-Liste;
  Test #3 von 3 auf 14 rechteerweiternde PATCHes gehoben, plus Throttle-Counter-Aussage
  (bleibt unverändert, weil der Grant-Pfad den Throttle gar nicht anfasst).

**Smoke gegen Wegwerf-Instanz, eigenes `tmp`-`DATA_ROOT` + eigenes `auth.sqlite3` +
`CREDENTIALS_DIRECTORY` (P8-26-Pattern):**
1. **Provisionierung** (`/tmp/opencode/p8-smoke/provision_user.py`): `AuthStore.upsert_user` +
   `confirm_totp` direkt in die Wegwerf-DB — derselbe Pfad wie
   `phase5_ui/tests/conftest.py :: confirmed_users`. Spiegelbildlich zur Vermeidung der
   Keyring-Verschmutzung (Hard Rule 1 — kein Test-Geheimnis in `nikinger-space`).
   TOTP-Seed: `ZUUMAH5A37MRZZ3V3O45EEUFQKUNR5Z5`. Passwort Argon2id-gehasht.
2. **DEK-Setup:** `SPACE_AUTH_DEK` existiert nicht als Env-Var (nur `CREDENTIALS_DIRECTORY` +
   Keyring); das hat den ersten Smoke-Versuch gekillt — der Server fiel auf den realen
   Keyring-DEK zurück, mein Test-User war mit dem Wegwerf-DEK `WlpaWlpaWlpaWlpaWlpaWlpaWlpaWlpaWlpaWlpaWlo`
   versiegelt, TOTP-Unseal schlug fehl. Korrektur: `CREDENTIALS_DIRECTORY=/tmp/opencode/p8-smoke/creds`
   mit `auth-dek`-Datei (base64-urlsafe, 600). Zweite Lektion dieser Session: `load_data_encryption_key()`
   liest NUR aus diesen beiden Quellen — keine `SPACE_AUTH_DEK`-Env-Var (gleicher Befund, der
   für eine künftige Konfigurationserweiterung vorgemerkt werden müsste, kein P8-Auftrag).
3. **Server-Start:** Port `28765` (Step 0 hatte `18765` benutzt, frischer Port zur Kollisions-
   Vermeidung), `SPACE_DATA_ROOT=/tmp/opencode/p8-smoke/data`, `SPACE_AUTH_DB` dorthin,
   `SPACE_PUBLIC_BASE_URL=https://p8smoke.local`, `SPACE_ALLOWED_HOSTS=127.0.0.1,p8smoke.local`,
   `SPACE_LOG_LEVEL=INFO` (anfangs `WARNING` — falsche Casing-Erwartung, `logging._checkLevel`
   lehnt `warning` ab, korrigiert), `CREDENTIALS_DIRECTORY` wie oben. `uptime_s:0` nach 3
   Half-Sekunden.
4. **Login via Playwright MCP (Chromium):** Space + Passwort + TOTP eingegeben. **Zwei echte
   Fehlschläge dokumentiert, nicht stillschweigend übergangen:**
   - (a) **TOTP-Counter vs. Timestamp.** Erster `totp_at(secret, now)`-Aufruf lieferte 401
     (kein Fehler im Server-Log außer HTTP-Status, weil `WARNING`/`INFO` zu wenig
     Auth-Debugging zeigen). Direktanalyse: `totp_at(secret, now // 30)` — der zweite Parameter
     ist der **Zähler**, nicht der Timestamp; das `verify()` rechnet intern `int(now // step_s)`,
     ich hatte `now` direkt durchgereicht. `totp_at(secret, 1788175872)` vs. `verify(..., now=1788175872)`
     (intern `current = 59605862`) — Counter-Drift von 59605862 zu 1788175872 = Faktor 30
     Unterschied, also komplett andere HOTP-Stelle. Korrigiert: `totp_at(secret, int(time.time()) // 30)`.
     Selbsterkenntnis, vor dem nächsten Versuch.
   - (b) **Rate-Limit-Sperre** nach den fünf 401-Versuchen aus (a) — `authctl.py unlock --space
     p8smoke` (Hard-Rule-1-konform, kein Secret im Aufruf) hat sie aufgehoben, danach
     erfolgreicher Login mit `168439` als TOTP-Code. Seite landete auf `/ui/`, Update-Banner
     sichtbar (`P7 Spaces verwalten`-Hinweis), Navigation+Rail gerendert, keine JS-Konsole-
     Fehler außer dem üblichen 401 vom Vorversuch.
5. **Tear-down:** Server-PID beendet, `rm -rf /tmp/opencode/p8-smoke`, **Live-Dienst
   unverändert** (`pid 997`, `uptime_s:73001` — beide Proben vor und nach dem Wegwerf-Lauf
   identisch, kein Server-Neustart durch den Smoke ausgelöst).

**Was der Smoke bewiesen hat (vs. was er bewiesen hätte, wenn der Round-2-Pfad mit
`widens()`-Auslöser leicht reproduzierbar wäre):**
- ✅ Throwaway-Instanz startet, Login funktioniert end-to-end (Browser, TOTP, Cookie, Rail,
  App-Layout).
- ✅ `phase5_ui/webui/static/js/dialogs.js` (mit dem neuen `async runBatchMove`) wird vom
  Server ausgeliefert (HTTP 200 im Access-Log, letzte Zeile der JS-Lade-Liste).
- ✅ `/api/v1/reauth` ist im Server vorhanden (HTTP 401 mit Secure-Cookie-Quirk über
  HTTP-Base-URL, NICHT 404 — der Endpunkt existiert; per `grep` auf den Code und über
  `test_reauth_grant.py` ohnehin bewiesen).

**Was der Smoke NICHT bewiesen hat, bewusst:**
- Eine echte Round-2-Auslösung im UI (seltene `widens()`-Pfade via Cross-Space-Move mit
  gleichzeitiger `share_*`-Erweiterung — ein Konstrukt, das der Dialog selbst gar nicht
  anbietet; `runBatchMove()` reagiert nur auf `reauth_required`-Antworten aus Round 1, die
  im Standard-Move-Pfad nie feuern). Der Round-2-Pfad ist durch `test_fourteen_widening_
  patches_with_one_grant_all_succeed` (8/8 in `test_reauth_grant.py` grün, einschließlich
  Test 6 „derselbe rohe TOTP zweimal wird vom Anti-Replay abgelehnt") vollständig
  bewiesen.
- Eine tatsächliche 14-Item-Bewegung im UI — erfordert entweder einen geteilten Space mit
  passendem `share_write`-Setup (in einer frischen Wegwerf-Instanz nicht trivial
  aufzubauen) oder einen UI-Dialog-Roundtrip mit Multi-Select, der in Playwright manuell
  getrieben werden müsste. Beides über die Nützlichkeit dieses Smokes hinaus; der
  UI-Roundtrip wird beim Live-Deploy ohnehin gefahren.

**Verifiziert:** `pytest -q` → **912 passed** (904 alt + 8 aus `test_reauth_grant.py`,
darunter der umbenannte `test_fourteen_widening_patches_with_one_grant_all_succeed` mit
N=14). Tabu-Diff leer (`phase4_auth/`, `phase2_mcp/`, `phase5_ui/webui/security.py`,
benannte `storage/`-Dateien — keine Zeile berührt). `ui_budget.py` 5/5 grün
(`dialogs.js` 9.5 KB, +0.6 KB seit dem Backend-Commit — der `async`-Block ist klein).

**Hard-Rule-1-Compliance des Smokes:** alle Geheimnisse (Passwort, TOTP-Seed, TOTP-Codes)
lebten ausschließlich in Prozess-Speicher und `auth.sqlite3` der Wegwerf-Instanz. Der
TOTP-Seed wurde einmalig in `/tmp/opencode/p8-smoke/provision.out` geschrieben (Hard Rule 7
verlangt stdout-Lesbarkeit, der Seed kommt nun mal aus `provision_user.py`); die Datei ist
mit dem gesamten Smoke-Verzeichnis nach dem Lauf gelöscht (`rm -rf`), kein Eintrag im
Keyring, keine Zeile in einem Repo-File.

**Nächster Schritt, konkret:** A2 `remove-space`-Auto-Reindex (P8-B, zweiter Erbpost aus
PHASE7_CLOSEOUT_H_H.md §4.2) — der Live-Incident vom 2026-08-27 (`GET /api/v1/overview` →
500 nach `testnutzer-p7`-Entfernung) rangiert bewusst vor dem UX-Befund P7-4 als
zweites A-Thema. Plan: `phase8_ui_graph_plan.md` §A2 (Zweizeiler + Test, Warn
-Variante
bewusst verworfen). Erst danach A3 P7-4-Zweitprobe. Block A insgesamt drei Commits — A1
damit fertig.

## Session stopped — 2026-08-28 (Block A gestartet: A1-Backend gebaut, 912 Tests grün, JS-Client ausstehend)

**Auftrag:** A1 Reauth-Grant (P8-A, schließt P7-24) — der zweite Erbpost aus dem P7-Handover §4.
Plan detailliert genug (Option b), Anker vor jedem Edit gegen den echten Code verifiziert
(V82): `webui/reauth.py:20` (`verify_reauth()`-Signatur), `webui/shares.py:55/96` (zwei
`require_*_reauth()`), `webui/api.py:156/204/218/681/992+` (`_PATCH_FIELDS`/`api_routes()`/
`_require_session`/Whitelist-Check/Route-Liste), `mcpserver/app.py:211` (kein Diff nötig —
Grant-Store wird in `api_routes()` intern gebaut, neben `LoginThrottle`).

**Ergebnis A1-Backend (Commit 1 von vermutlich 2 für A1):**
- `webui/reauth.py` — `ReauthGrant`-`@dataclass` (session_id, expires_at) +
  `ReauthGrantStore`-Klasse (in-memory `dict[str, ReauthGrant]`, `issue()`/`check()` mit
  required `now: float` für deterministische Tests, lazy purge, nie persistiert, stirbt mit
  Prozess). Konstante `REAUTH_GRANT_TTL_S = 90.0`.
- `webui/shares.py` — beide `require_*_reauth()` akzeptieren `body["reauth_grant"]` ZUERST
  (vor `password`/`totp`), bei gültigem Grant sofortiger Return. Bindung an
  `session.session_hash` (nicht Klartext-Cookie — der existiert nur im Browser, P5-K; Hash
  ist die einzige serverseitig mögliche Session-Identität). **Wichtige Korrektur gegen den
  Plan-Text:** der Plan-Beispielcode schrieb `session.id`, das gibt es auf `SessionRow` nicht
  (`authserver/models.py:104-118` — `session_hash`/`space`/`csrf_hash`/Zeitstempel). Wenn der
  Plan `session_id` meinte, dann den Hash.
- `webui/api.py` — `_PATCH_FIELDS` um `"reauth_grant"` erweitert; `api_routes()` baut intern
  `ReauthGrantStore()` neben dem vorhandenen `LoginThrottle` (kein neuer Parameter, kein
  `mcpserver/app.py`-Diff); `require_share_reauth()`/`require_space_reauth()`-Aufrufe (drei
  Stellen) reichen `grant_store` durch; Filter im `_items_patch` (vorher: `"version",
  "password", "totp", "space"`) bekommt `"reauth_grant"` dazu (Hard Rule 1: ein langlebiges
  Token darf NIE als Frontmatter-Feld landen); neuer Handler `_reauth_post()` + Route
  `POST /api/v1/reauth`. **Throttle-Prüfung explizit vorgezogen** (`throttle.check()` vor
  `verify_reauth()`) — sonst hätte `verify_reauth()` die Sperre in ein `False` geschluckt und
  der Client hätte nicht zwischen „falsch" (403) und „Space gesperrt" (429) unterscheiden
  können. Spiegelung des Musters aus `routes_auth.py:59-67`. Fehlschlag-Pfad: 403 mit
  `reauth_required`, gedrosselt: 429 mit `rate_limited`, beides gemäß `errors.py`-Konvention.
- `phase5_ui/tests/test_reauth_grant.py` (neu, 8 Tests, 1:1 zu Plan §A1): korrekte Credentials
  → 200+Token; falscher TOTP → 403 mit Throttle-Zählung, sechster Versuch → 429; **P7-24-
  Kernfall** (drei rechteerweiternde PATCHes mit einem Grant); abgelaufenes Grant (clock
  +120s) → 403; Grant einer fremden Session → 403; derselbe TOTP-Code zweimal über
  `/api/v1/reauth` → zweiter 403 (Anti-Replay intakt); `reauth_grant` als Feld passiert die
  `_PATCH_FIELDS`-Whitelist, beliebiges anderes Feld weiterhin 422; ohne Session → 401.

**Plan-Abweichungen, dokumentiert (nicht stillschweigend):**
1. `session.id` → `session.session_hash`. `SessionRow` hat kein `id`-Attribut; der Plan-
   Beispielcode war ungenau gegen das echte Modell.
2. Throttle-Check in `_reauth_post` VOR `verify_reauth()` (statt nur durch `verify_reauth()`).
   Plan-Wortlaut „gedrosselt → 429" hätte bei nur-innen-Prüfung als 403 geliefert; jetzt ist
   die Semantik echt (429 unterscheidbar von 403). Konvention `routes_auth.py:59-67`.
3. Grant-Store als interner `api_routes()`-State statt Parameter. Plan-Text „hängt an der App
   neben der LoginThrottle-Instanz (App-Factory, V82)" — die App-Factory IST `api_routes()`
   in dieser Code-Struktur (`create_app()` ruft `api_routes(...)` einmal auf, ohne
   App-State-Pattern), die saubere Implementierung ist lokal-in-`api_routes()`. Vermeidet
   einen `mcpserver/app.py`-Diff (Tabu-Linie Phase-5/6 hält).

**Verifiziert:** `pytest -q` → **912 passed** (904 + 8 neu, exakt +8), keine Regression. Tabu-
Diff auf `phase4_auth/` + `mcpserver/{tools,permissions,server}.py` + `security.py` + `storage/`
außerhalb der P8-M-Öffnung: **leer** (Plan §0.4 erfüllt — die P8-M-Öffnung gilt erst ab Block B).
Live-Dienst nicht angefasst (kein Server-Code deployed, nur Bibliothekscode auf dem
Wegwerf-Pfad).

**Verbleibend für A1 (Commit 2):** Client-Änderung in `webui/static/js/dialogs.js ::
runBatchMove()` — vor Runde 1 einmal `POST /api/v1/reauth`, dann `{reauth_grant: token}` statt
`{password, totp}` an `moveSelectedItems()`. `list.js :: moveSelectedItems()` selbst bleibt
unangetastet (Body-`Object.assign({version, folder}, credentials || {})` setzt das Grant-Feld
korrekt). Browser-Smoke gegen eine Wegwerf-Instanz (P8-26-Pattern: drei Items mit einem Grant
verschieben, danach ein 7. Tab-Smoke gegen den Live-Dienst, dass der neue Pfad in der
laufenden Instanz angekommen ist). Erst danach A1 in der Abnahmematrix P8-4 als „gebaut"
markierbar — Live-Verifikation bleibt Nikingers Handgriff.

**Nächster Schritt:** A1-Client (Commit 2) in derselben Sitzung, dann A2 `remove-space`-
Reindex (Commit 3). Block A insgesamt drei Commits.

**Stand:** Fundament-Session läuft, Claude Code + Nikinger, interaktiv.

- 0.1 `pytest -q` → **904 passed**, bestätigt V81 (Erwartung aus der Planung war exakt 904).
- 0.2 Verifikationsdurchlauf:
  - (a) Stichprobe P7-Handover §4 gegen Code — **beide grep-prüfbaren Punkte bestätigt**:
    `list.js :: moveSelectedItems()` reicht dasselbe `credentials`-Objekt an jedes sequenzielle
    `PATCH` durch (Zeile 240/246); `spacectl.py :: _cmd_remove_space()` ruft `remove_space_dir()`
    aber nirgends `rebuild_index()` (Zeile 170–195). P7-4 ist eine Verhaltensbehauptung, nicht
    grep-prüfbar — unverändert offen für die A3-Zweitprobe.
  - (b) `up:`/`down:`-Linkauflösung über alle L1-Cards: **ein** unaufgelöster Link, erwartet —
    `docs/concepts/phase8_ui_graph_plan.md` zeigt auf `phase8_ui_graph/CLAUDE.md`, das erst in
    diesem Schritt entsteht.
  - (c) INDEX-Abdeckung: alle lebenden `.md` haben eine Zeile; die drei `phase6_shares/tests/golden/*.md`
    sind Test-Fixtures, keine lebenden Dokumente — bewusst ohne Zeile.
  - (d) Softcap-Scan: zwei Übergrößen bestätigt (`phase6_shares/CLAUDE.md` 41.032 B,
    `phase5_ui/CLAUDE.md` 40.957 B) — beide über der 40.000-B-Schwelle (dezimales KB, wie in der
    bestehenden `phase6_shares`-Notiz verwendet).
- 0.3 P8-P ausgeführt: `phase5_ui/CLAUDE.md`s INDEX-Zeile bekam dieselbe benannte Ausnahme-Notiz
  wie `phase6_shares/CLAUDE.md` (geschlossene Phase, ein Abschluss-Block, Rotation bricht mit
  `exit 2`); dabei zwei stale Größenangaben korrigiert (`~34KB`→`~41KB` bei phase5_ui,
  `~44KB`→`~41KB` bei phase6_shares — beide waren nie nachgemessen worden).
- 0.4 `AGENTS.md` entfernt (`git rm`), zugehörige INDEX-Zeile raus — Freigabe stand bereits in
  der INDEX-Zeile selbst (P7-Handover §7.2).
- 0.5 Dieses Skelett + `SESSIONS_ARCHIVE.md` angelegt.

- 0.6 **opencode installiert und Regeldatei-Verhalten verifiziert.** `npm install -g
  opencode-ai` (Nikinger-Handgriff), Ergebnis `opencode-ai@1.18.25`. Ein `postinstall`-Warnhinweis
  (`allow-scripts` blockierte `postinstall.mjs`) erwies sich als folgenlos — das Plattform-Binary
  kommt über ein separates optionales npm-Paket, nicht über das Skript; `opencode --version` /
  `--help` funktionieren sofort. Provider-Auth vom Nikinger selbst gesetzt (Minimax-Token-Plan,
  `opencode auth list` zeigt `MiniMax (minimax.io)`, Modell `minimax/MiniMax-M3` verfügbar).
  **Kontrollfrage statt Annahme** (Plan-Vorgabe): `opencode run --model minimax/MiniMax-M3` mit
  der Frage nach dem Nikinger-Codenamen + Hard Rule 6 — Antwort korrekt **„Nikinger"** + Hard
  Rule 6 wortgetreu zitiert. `CLAUDE.md` wird gelesen, keine Verdeckung mehr durch `AGENTS.md`
  (0.4 hat es entfernt).
- 0.7 **Fähigkeits-Parität hergestellt, V93/V94 beantwortet:**
  - **V93 (Browser-Steuerung):** `opencode mcp add playwright -- npx @playwright/mcp@latest`
    (Syntax: Kommando nach `--`, nicht per Prompt-Dialog) — steht in
    `~/.config/opencode/opencode.jsonc` (**global**, nicht projektlokal — für dieses
    Ein-Projekt-Setup ohne praktischen Unterschied, aber notiert für den Fall eines zweiten
    opencode-Projekts). `opencode mcp list` zeigt `playwright — connected`. 30 `playwright_*`-
    Tools stehen der laufenden Instanz zur Verfügung (per Tool-Auflistung bestätigt) — Pendant zu
    `claude-in-chrome` gefunden.
  - **V94 (Web-Recherche):** ursprünglich nein (nur `webfetch`, kein Suchwerkzeug) — **noch in
    dieser Sitzung nachgerüstet:** `opencode mcp add websearch -- npx -y
    @zhafron/mcp-web-search` (MIT, kein API-Key nötig — DuckDuckGo/Bing/SearXNG mit
    automatischem Fallback + URL-Extraktion, `github.com/tickernelz/mcp-web-search`, kein
    `pre-`/`postinstall`-Skript im Paket, 366 wöchentliche Downloads geprüft vor dem Hinzufügen).
    Live-Probe bestanden: Suche nach „IBM Plex Sans variable font github release" lieferte
    korrekt `github.com/IBM/plex/releases` als Top-Treffer — direkt für V83 (C1) brauchbar.
    **V94 damit: ja**, C0 läuft komplett unter opencode/M3, keine Claude-Code-Zuarbeit mehr
    nötig. Beide MCP-Einträge (`playwright`, `websearch`) liegen in derselben globalen
    `~/.config/opencode/opencode.jsonc`.
- 0.8 **Smoke-Test bestanden (P8-26).** Wegwerf-Branch `phase8-step0-smoke-test`, drei Proben
  in einem opencode-Lauf: (1) Testdatei angelegt — bestanden; (2) `pytest -q
  phase1_storage/tests/test_models.py` — **4 passed**, kein `SHAREFYX_*`/`SFX_*`-Env gesetzt
  (Session-`env` vor und nach dem Lauf geprüft, sauber); (3) Playwright-Navigation gegen eine
  echte Wegwerf-Instanz (eigener Port `18765`, eigenes `tmp`-`SPACE_DATA_ROOT`, eigene
  `SPACE_AUTH_DB`) — `GET /ui/login` korrekt mit Titel/Überschrift „Anmelden" gelesen.
  **Ein Betriebsfehler dabei, sofort korrigiert:** der erste Versuch ließ `SPACE_PORT`
  unspezifiziert, band an den Default-Port `8765` — dort läuft der **echte** `sharefyx-mcp.service`
  (Live-Instanz, pid 999) — Bindeversuch scheiterte mit `EADDRINUSE`, der Prozess beendete sich
  selbst, kein Schreibzugriff erfolgte. Der folgende `curl /health` traf dadurch tatsächlich den
  Live-Dienst — rein lesend, keine andere Wirkung als ein manueller Health-Check. Wiederholt mit
  `SPACE_PORT=18765`, danach sauber gegen die eigene Instanz verifiziert (`uptime_s:1`).
  Wegwerf-Instanz per PID beendet, Live-Dienst per zweitem `/health`-Aufruf als unverändert
  bestätigt (`uptime_s` durchgehend steigend, kein Neustart). Branch + Testdatei +
  `.playwright-mcp/`-Laufzeitordner nach dem Test verworfen (`git branch -D`, `rm`);
  `.playwright-mcp/` zusätzlich in `.gitignore` aufgenommen (künftige opencode-Läufe in diesem
  Projektverzeichnis legen ihn sonst wieder an).

**Verifiziert:** `git status` nach Cleanup zeigt nur den beabsichtigten Diff (`.gitignore`,
Phase-Head, Skelett, INDEX/ROADMAP) — Wegwerf-Branch weg, Wegwerf-Instanz-Prozess weg, Live-Dienst
lief während der gesamten Sitzung ohne Unterbrechung (`systemctl is-active` durchgehend `active`).

**Harnesswechsel freigegeben:** ab Block A führt opencode/M3 aus, kein Advisor-Call
(P8-L/N12) — Ersatzmechanismen sind die Selbstprüf-Checkliste (Plan §0.6) und die zwei
Nikinger-Sichtprüfpunkte (Plan §8).

**Offen für die nächste Sitzung:** Block A starten (A1 Reauth-Grant zuerst, P8-A) — unter
opencode/M3, gegen `docs/concepts/phase8_ui_graph_plan.md` §2. Vor jedem Edit die zitierten
Datei:Zeile-Anker neu prüfen (V82, driftet erfahrungsgemäß um wenige Zeilen).

