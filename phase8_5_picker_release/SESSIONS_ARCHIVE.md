---
status: live
purpose: Archivierte Session-stopped-Blöcke aus phase8_5_picker_release/CLAUDE.md, verbatim, newest-first
read-when: Auditieren der vollen Phase-8.5-Historie — der aktuelle Session-Block lebt im Phase-Head, nicht hier
detail: L3
up: ./CLAUDE.md
down:
updated: 2026-09-04 (A1-Block rotiert — manuell wie Step-0, weil `scripts/rotate_session_block.sh` aus Phase 7 für `phase8_5_picker_release/` noch nicht portiert ist und YAGNI für eine zweite manuelle Rotation; A1 vorne angehängt (newest-first), Step 0 darunter unverändert; B1/C/D/Z stehen noch aus)
---

# SESSIONS_ARCHIVE.md — Phase 8.5: Link-Picker-Politur, Titel-statt-ID-Hint, v3-Vorabritt + Deploy

### 2026-09-04 (A1 — Picker-Modus-Umschalter + Body-Markdown-Link, Code committet)

**Auftrag:** A1 nach `docs/concepts/phase8_5_picker_release_plan.md` §2.A1. User-Auftrag
vom 2026-09-03 nannte die genauen Eingriffe (HTML, `dialogs.js:100-185`, `editor.js:88-100`,
`localStorage` unter `sfx:linkpicker:mode`); statische Tests + Block-C-Browser-Nachweis
wurden ausdrücklich zurückgestellt — Tabu-Diff bleibt leer, nur `webui/static/`.

**Ergebnis — alle vier Eingriffsgruppen aus Plan §2.A1 committet, §0.5 Checkliste grün:**

1. **`phase5_ui/webui/static/app.html`** (Zeilen 270–280). Hint-Text von „hängt die
   itm_…-ID an die Links" auf „Was der Klick einfügt, hängt vom Modus darunter ab"
   neutralisiert; neues `<label>Einfügen <select class="input" id="link-picker-mode">
   …</select></label>` **zwischen** Hint und Suchfeld eingefügt — barer `<label>` ohne
   `class="field"`, exakt nach dem Vorbild `#move-space-select` (`app.html:286-287`),
   um den 2026-09-02-Chevron-Eskalationsfall nicht zu reproduzieren
   (`.field .input { font-size: 13px }`); beide `<option>` mit Werten `body` (Default)
   und `frontmatter`. Suchfeld-Input um `role="combobox" aria-expanded="true"
   aria-controls="link-picker-results"` erweitert (A2-Vorbereitung — ohne
   `aria-controls` ist `aria-activedescendant` formal ungültig). Pflichtprüfung am
   Step-Ende aus Plan §2.A1 Punkt (1) — computed `font-size` und Chevron-Größe gegen
   `#move-space-select` — wird erst in Block C empirisch verglichen (kein jsdom-Harness
   im Projekt, verifiziert Plan §0.0); bei Abweichung Eskalation nach §0.0, kein
   symptomatisches Nachjustieren.

2. **`phase5_ui/webui/static/js/dialogs.js`**. Modul-Konstante
   `LINK_PICKER_MODE_KEY = "sfx:linkpicker:mode"` ergänzt (Präfix `sfx:` aus
   `editor.js :: draftKeyFor()`); `linkPickerModeEl` neu; `linkPickerButtonEl` ersatzlos
   entfernt — war in `dialogs.js` ungenutzt (`editor.js:47` hält die eigene). Zwei neue
   Helper: `_linkPickerMode()` (liefert `"body"`/`"frontmatter"`, fällt auf `body`
   zurück bei unerwartetem Wert) und `_restoreLinkPickerMode()` (liest `localStorage`
   in `try`/`catch` — privater Modus wirft `SecurityError`). `openLinkPicker` ruft
   `_restoreLinkPickerMode()` vor `linkPickerSearchEl.focus()`, Guard-Text auf
   `"openLinkPicker braucht { onPick({id, title, mode}) }"` aktualisiert; Klick-Listener
   in `_renderLinkPickerResults` liest den Modus **vor** `closeLinkPicker()` (Select wird
   mit Dialog versteckt; Reihenfolge hält die Lesung unabhängig von UI-Mutationen) und
   ruft `onPick({id, title, mode})`. Im `init()`-Block: `linkPickerModeEl` zugewiesen
   plus `change`-Handler, der die Wahl **beim Wechsel** in `try`/`catch` schreibt — so
   überlebt sie auch einen Abbruch via Escape.

3. **`phase5_ui/webui/static/js/editor.js`**. **`insertAtCursor` (bisher Zeile 548–557,
   innerhalb `init()`) auf Modulebene gehoben** (P8.5-I) — direkt hinter `_appendLinkId`
   (jetzt Zeile 107), Körper byte-identisch, schließt über nichts aus `init()`
   (`textarea` ist Parameter), Alt-Aufruf Bild-Knopf (jetzt Zeile 669) sieht die
   Modulebene via Hoisting. Bestätigt: `grep -n 'function insertAtCursor' editor.js`
   liefert **genau einen** Treffer. Drei neue Funktionen: `_linkTextFor(title)`
   (kollabiert Whitespace, maskiert `[`/`]` mit Backslash, leerer String signalisiert
   „kein Titel"), `_appendLinkMarkdown(title, id)` (ruft `insertAtCursor` mit
   `"[" + label + "](#item/" + id + ")"`, gleiche `itm_[0-9a-f]{8}`-Defense-in-Depth
   wie `_appendLinkId`), `_onLinkPicked(picked)` (Router: `mode === "frontmatter"` →
   `_appendLinkId`, sonst → `_appendLinkMarkdown`). Wiring (jetzt Zeile 530):
   `openLinkPicker({ onPick: _appendLinkId })` →
   `openLinkPicker({ onPick: _onLinkPicked })`.

4. **`localStorage` unter `sfx:linkpicker:mode`** (P8.5-G). **Erste `localStorage`-
   Nutzung im Projekt** — bisher nur `sessionStorage` (CSRF, Drafts). Begründung: die
   Moduswahl muss Tab-/Fenster-Schließen überleben, das ist mit `sessionStorage` nicht
   möglich. `try`/`catch` deckt den SecurityError im privaten Modus ab. **V99-Korrektur
   im Session-Block festgehalten** (kein stiller Drift): der Plan hatte „ja,
   `sfx:draft:`" als Erwartung — das traf für den **Präfix** zu, aber nicht für den
   Storage; die Substantiv-Korrektur (`local`- statt `session`Storage) ist die einzige
   Abweichung vom Plan-Wortlaut und folgt direkt aus P8.5-G.

**Begleitende Doku-Updates im selben Commit (Hard Rule 8):**

- `phase8_5_picker_release/CLAUDE.md`: Modul-Status A1 `⬜` → `🟡` (Tests noch `⬜`);
  fünf Abnahmezeilen P8.5-5/-6/-7/-8/-9 mit kurzen Klammer-Anmerkungen versehen („Code
  committet; Browser-Nachweis Block C Station …"); Stand-Zeile unverändert
  (3 ✅ · 0 🟡 · 17 ⬜, P8.5-1/-2/-20 aus Step 0).
- Step-0-Block nach `SESSIONS_ARCHIVE.md` rotiert (manuell, weil das Skript nur 2+→1
  kann und das Archiv initial keinen `## Session stopped`-Anker hatte — Platzhalter
  entfernt, Frontmatter-`updated:` aktualisiert).
- `phase8_5_picker_release/SESSIONS_ARCHIVE.md`: Platzhalter-Hinweis „noch leer"
  entfernt (jetzt nicht mehr zutreffend), `updated:` auf 2026-09-04.

**Verifiziert (§0.5 Checkliste):**

- `pytest -q` (venv): **959 passed in 258.19 s** — unverändert, kein Python-Touch
  (Phase 8.5 baut **keine** API-Fläche, Plan §0.3).
- Tabu-Diff aus §0.3 leer: `git diff --stat main -- phase4_auth/ phase1_storage/storage/
  phase5_ui/webui/security.py phase5_ui/webui/api.py phase5_ui/webui/serializers.py
  phase5_ui/webui/permissions.py phase2_mcp/` — **keine Ausgabe**.
- `node --check` auf `dialogs.js` + `editor.js` + `app.js` (Sicherheitsgespann) — alle
  drei **OK**.
- `python phase5_ui/scripts/ui_budget.py`: **5/5 grün**, js+css+gzip jetzt
  **127.6 KB** von 125.8 KB (+1.8 KB durch `dialogs.js` 11.0 → 11.7 KB und
  `editor.js` 7.9 → 8.8 KB); Latenz-`get_item` 7.8 ms / 0.5 KB, `search_items`
  185.6 ms / 20 KB, `GET /api/v1/overview` 867.9 ms / 1.9 KB — alle im Korridor.
- Größenprüfung `find . -name "*.md" … -size +40k`: **kein** neuer Treffer durch diese
  Session; `phase8_5_picker_release/CLAUDE.md` bleibt deutlich unter dem Cap.
- Fehlerpfad einmal durchdacht: leeres Suchergebnis → `_renderLinkPickerResults`
  rendert den `aria-disabled="true"`-Eintrag wie bisher (kein Code-Link auf
  `linkPickerItems`, A2 fügt das später hinzu); `localStorage`-Wurf → `saved = null`
  → `body`-Default; `closeLinkPicker()` läuft vor `onPick`-Aufruf, Modus-Lesung VOR
  `closeLinkPicker` ist dadurch UI-mutations-unabhängig; `picked` ist `null`/kein
  String → `_onLinkPicked` macht nichts; `_linkTextFor` kollabiert Whitespace und
  maskiert `[`/`]` (Titel „Notiz [Entwurf]" zerreißt den Markdown-Link nicht).
- Service-Touch **0**. `systemctl status sharefyx-mcp` zeigt **PID 195922**, Active seit
  `Wed 2026-09-02 11:51:57 CEST` (1 day 23h zum Sitzungsbeginn — uptime wuchs leicht
  gegenüber dem Step-0-Stand) — nichts angefasst, nur gelesen. **PID +
  ActiveEnterTimestamp im Session-Block notiert, wie §0.5.7 verlangt.**

**Zwei Drift-Funde im Verlauf der Sitzung, im Block festgehalten, kein stiller Patch:**

1. **`\u00b7` vs. `·` in `dialogs.js`:** die Datei speichert das Middle-Dot als JS-
   Escape (`\u00b7`), nicht als Literal-Zeichen. Mein erster `edit` traf den
   `oldString` mit literalem `·` nicht; zweiter Versuch mit dem Escape klappte.
   **Lehre für künftige Picker-Edits:** in dieser Datei konsequent die Escape-Form
   verwenden oder das ganze Vorkommen vor dem Edit auf `xxd`/Pipe-Substitution
   umstellen — kein Code-Fix nötig, ist ein Editor-/Tooling-Detail.
2. **`sessionStorage` vs. `localStorage`:** V99 im Plan war ungenau — der Plan tippte
   auf „ja, `sfx:draft:`" als Präfix-Begründung, verschwieg aber, dass
   `draftKeyFor` selbst `sessionStorage` nutzt. Die Wahl von `localStorage` ist
   deshalb eine **Eskalation** gegenüber der Projekt-Konvention, keine triviale
   Fortführung; gerechtfertigt durch P8.5-Gs Anforderung „überlebt Tab-Schließen".
   Im Code dokumentiert (`dialogs.js:107`/`185-191`).

**Was diese Session bewusst NICHT tat:**

- Statische Tests in `phase5_ui/tests/test_static_routes.py` (P8.5-5/-9) — User-Auftrag
  beschränkte die Session auf `webui/static/`; Tests werden mit Block-C-Vorbereitung
  oder vor A2 nachgezogen.
- Block C (Wegwerf-Setup + 13-Stationen-Playwright-Smoke) — kommt als eigener Schritt.
- A2 (`aria-activedescendant`, Tastaturnavigation, `_pickLinkPickerAt`,
  CSS-Block-Entdopplung) — eigene Aktion, Reihenfolge A1 → A2 nach §8.
- B1 (Hint generalisierend) — nach A2, eigene Datei (`mcpserver/tools.py:159-164`).

**Nächster Schritt, konkret:** **A2 — §9.4.3 Tastaturnavigation und `aria-selected`**
(`dialogs.js` `linkPickerItems`/`linkPickerCursor` + `_setLinkPickerCursor` +
`_pickLinkPickerAt` + keydown-Handler am Suchfeld; `app.css` zwei identische Blöcke zu
einem zusammenziehen, totes `:focus` raus; `app.js` **nicht** anfassen, P8.5-L). Block C
kommt **nach** A2 — beide landen in `_renderLinkPickerResults` und im Auswahlpfad,
ein Skript-Paar deckt beide ab (Plan §8).

### 2026-09-03 (Step 0 — Skelett + vier Haushalt-Funde abgearbeitet)

**Auftrag:** Step 0 nach `docs/concepts/phase8_5_picker_release_plan.md` §1. Verifikations-
Durchlauf war bereits 2026-09-03 vom Nikinger (Planungssession) gefahren — vier Funde
benannt, davon drei Doku-only, einer ein Bilanz-Zähler-Drift. opencode/M3 wiederholt die
Messung nicht, sondern arbeitet die Funde ab und legt das Skelett an.

**Ergebnis — alle vier Funde aus Plan §1 abgearbeitet, alle fünf Schritte grün:**

1. **Fund 1 — `docs/INDEX.md` über 40 KB-Softcap** (Plan §1.2). Zeile 8 war eine
   15.472-Zeichen-Pipe-Kette aus ~40 datierten Einträgen, verantwortlich für den Löwenanteil
   der Datei (52.911 B bei Übernahme). **Kürzung auf 5 neueste Einträge + Schlusszeile**
   „ältere Einträge: die jeweilige phase*/SESSIONS_ARCHIVE.md". Die vollständige Historie
   steht in den jeweiligen `phase*/SESSIONS_ARCHIVE.md`. Größenverlauf: **52.911 B → 40.917 B**
   (−11.994 B, −23 %; aktueller Stand nach Step 0.2: **40.917 B, 43 B unter dem 40-KB-Softcap
   = 40 × 1024 B**).
2. **Fund 2 — vier `.md` ohne Card/Indexzeile, korrekt so** (Plan §1.3). Regel-Präzisierung
   im Wartungsblock von `docs/INDEX.md` (Zeilen 21–23): Harness-Dateien
   (`.claude/RESUME.md`), Test-Fixtures (`phase6_shares/tests/golden/*.md` — Card bräche den
   Byte-Vergleich), maschinell geparste Dateien (`docs/UPDATE_LOG.md`), Vendor-/Lizenztext
   (`phase5_ui/THIRD_PARTY_LICENSES.md`, `phase5_ui/vendor/lucide/README.md`). Bewusst als
   kompakter Dreizeiler formuliert (Plan §1.3 liefert nur die vier Kategorien; ausführliche
   Begründung pro Datei bleibt im Plan §1.3-Tabelle).
3. **Fund 3 — Doku/Code-Drift „Büroklammer" vs. „Lupe"** (Plan §1.4).
   `phase8_ui_graph/CLAUDE.md:440` nannte das Picker-Symbol „Büroklammer", `app.html:183`
   rendert `<use href="#i-search">` (Lucide-Suche, eingeführt in Phase 8 Block C2). Der
   `UPDATE_LOG.md`-Eintrag vom 2026-09-01 sagte bereits korrekt „Lupe". **Korrektur mit
   datierter Notiz** am 2026-09-03 im selben Block, damit der nächste Leser sieht, dass es
   kein Tippfehler war, sondern eine echte Korrektur.
4. **Fund 4 — Phase-8-Abnahmebilanz zum dritten Mal gedriftet** (Plan §1.5). Die Zeile trug
   seit dem 2026-09-02-Block „15 ✅ · 10 🟡 · 0 ⬜", die Aufzählung darunter listete unter
   „15 ✅" genau **vierzehn** Zeilennummern. Maschinell nachgezählt über die §7-Matrix
   selbst:
   ```
   awk '/^\| P8-[0-9]+ /{ if (/\| ✅ \|/) g++; else if (/\| 🟡 \|/) y++; else if (/\| ⬜ \|/) o++; n++ } \
     END {printf "Zeilen=%d ✅=%d 🟡=%d ⬜=%d\n", n, g, y, o}' phase8_ui_graph/CLAUDE.md
   ```
   Lauf 2026-09-03: **`Zeilen=26 ✅=14 🟡=12 ⬜=0`**. Bilanz-Zeile auf **14 ✅ · 12 🟡 · 0 ⬜**
   korrigiert; das awk-Kommando in den Bilanz-Abschnitt geschrieben, sodass künftige
   Schreibvorgänge die Zahl ableiten statt pflegen. Aufzählung gegen das Ergebnis abgeglichen
   (passt: 14/12-Zerlegung stimmt mit den aufgezählten IDs überein).

**Skelett angelegt (Step 0.5):**

- `phase8_5_picker_release/CLAUDE.md` — L1-Card, Mission, Scope (DRIN/DRAUSSEN), Harte Regeln
  (§0.3 Tabu-Liste verbatim übernommen + explizit `webui/{api,serializers,permissions}.py` als
  Tabu ergänzt), Modul-Status-Tabelle (Step 0 / A1 / A2 / B1 / C / D / Z mit aktuellem
  Status), Abnahmestand-Tabelle nach §7-Muster (P8.5-1–P8.5-20, P8.5-1/-2/-20 aus Step 0
  bereits ✅), Geerbte Contracts, leerer Session-Block. **12.128 B** — deutlich unter dem
  40-KB-Softcap.
- `phase8_5_picker_release/SESSIONS_ARCHIVE.md` — L1-Card, leerer Body mit Hinweis, dass der
  erste rotierte Block hierher wandert, sobald die zweite Session den Step-0-Block ablöst.
  **555 B**.
- `phase8_5_picker_release/scripts/` — leeres Verzeichnis, wird in Block C gefüllt
  (Wegwerf-Setup + Playwright-Ritt).

**Begleitende Doku-Updates im selben Commit (Hard Rule 8):**

- `ROADMAP.md` — neuer Abschnitt „Phase 8.5 — Link-Picker-Politur und v3-Release" eingefügt
  **vor** „Bewusst nicht auf der Roadmap" (Plan §1.6 Zeile 352). Status: „Step 0
  abgeschlossen", nächster Schritt „A1".
- `CLAUDE.md` (Wurzel) — `down:`-Zeile zeigt jetzt auf `phase8_5_picker_release/CLAUDE.md`
  (vorher `phase8_ui_graph/CLAUDE.md` — Umstellung nach Skelett-Anlage, wie der 2026-09-03-
  Absatz in „Current state" angekündigt hatte). Neuer Absatz unter Phase 8.5 mit Step-0-
  Zusammenfassung; `updated:`-Kette um den Step-0-Eintrag am Anfang verlängert. **41.462 B** —
  damit 502 B **über** dem 40-KB-Softcap. Das war bereits vor Step 0 absehbar (Kandidat für
  dieselbe Kompression wie 2026-08-08, INDEX.md-Zeile 27); kein Step-0-Auftrag, kein
  Step-0-Aufräumschritt — Vermerk in `docs/INDEX.md` bleibt korrekt.
- `docs/INDEX.md` — `## Phase 8.5 — 🔄 …`-Abschnitt mit drei INDEX-Zeilen war bereits durch
  den Nikinger angelegt (Planungs-Commit 2026-09-03); Step 0 hat daran nichts geändert.
  Dateigröße 40.917 B — 43 B unter dem Cap, **nicht** 264 B wie nach Fund 1 alleine, weil
  Fund 2 die Ausnahmenliste hinzugefügt hat.

**Verifiziert (§0.5 Checkliste):**

- `pytest -q` (venv): **959 passed in 270.79 s** — unverändert, kein Python-Touch in
  dieser Session (nur `.md` und Skelett-`.md`).
- Tabu-Diff aus §0.3 leer:
  `git diff --stat main -- phase4_auth/ phase1_storage/storage/ phase5_ui/webui/security.py
  phase5_ui/webui/api.py phase5_ui/webui/serializers.py phase5_ui/webui/permissions.py
  phase2_mcp/` — **keine Ausgabe**.
- `node --check` auf JS-Dateien: keine berührt.
- `python phase5_ui/scripts/ui_budget.py`: keine UI-Änderung, irrelevant für Step 0.
- Service-Touch **0**. `systemctl status sharefyx-mcp` zeigt **PID 195922**, Active seit
  `Wed 2026-09-02 11:51:57 CEST` (1 day 21h zum Sitzungsbeginn), CPU 18min 33s — nichts
  angefasst, nur gelesen. **PID + ActiveEnterTimestamp im Session-Block notiert, wie §0.5.7
  verlangt.**
- Größenprüfung `find . -name "*.md" -not -path "./.venv/*" -not -path "*/.pytest_cache/*"
  -size +40k` (Plan §6 Step Z Punkt 6 — vorab geprüft, weil Step 0 schon Doku-Maße ändert):
  jeder Treffer ist entweder 📕 (Plan-Snapshot, `docs/concepts/*_plan.md`) oder bereits
  vorher als „über 40KB-Softcap benannt" markiert (`phase8_ui_graph/CLAUDE.md` 93.562 B,
  `phase6_shares/CLAUDE.md` 41.032 B, `CLAUDE.md` 41.462 B seit diesem Schritt). **Neu durch
  Step 0** ist der Eintrag für `CLAUDE.md` — siehe oben.

**Eine Korrektur am Plan, im Session-Block festgehalten, kein stille Abweichung:**

Fund 1 + Fund 2 zusammen landeten **zunächst 75 B über dem Cap**. Der Plan nennt
„neuesten fünf" explizit, hatte aber die zusätzlichen Bytes der Fund-2-Ausnahmenliste nicht
mitgerechnet (seine Schätzung „mit ihr ~52,7 KB" war ein Vorher-Wert, kein Nachher-Wert).
**Lösung:** Fund 2 als Drei- statt Vierzeiler formuliert, Datei landete auf 40.917 B
(43 B unter dem Cap). Beide Anforderungen — fünf Einträge **und** Ausnahmen dokumentiert —
gehalten, Plan-Wortlaut im Session-Block nicht gebrochen. Wer den Plan liest und `updated:`
als Pipe-getrennte Liste erwartet, sieht sie weiterhin (Schlusszeile ist erkennbar, weil
„ältere Einträge: …" mit Doppelpunkt beginnt).

**Nächster Schritt, konkret:** Block A / **A1 — §9.4.2 Picker-Modus-Umschalter**.
`docs/concepts/phase8_5_picker_release_plan.md` §2.A1 enthält die genauen Eingriffe
(`app.html` Zeile 270–280 mit `<select class="input" id="link-picker-mode">`, `dialogs.js`
Zeile 100–185, `editor.js` Zeile 88–100 + 548–557, `localStorage`-Persistenz unter
`sfx:linkpicker:mode`). Tabu-Diff-Kommando am Step-Ende weiter leer halten — A1 berührt
nur `webui/static/{app.html,app.css,js/dialogs.js,js/editor.js}`.
