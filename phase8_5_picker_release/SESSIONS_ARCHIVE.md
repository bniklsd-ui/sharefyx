---
status: live
purpose: Archivierte Session-stopped-Blöcke aus phase8_5_picker_release/CLAUDE.md, verbatim, newest-first
read-when: Auditieren der vollen Phase-8.5-Historie — der aktuelle Session-Block lebt im Phase-Head, nicht hier
detail: L3
up: ./CLAUDE.md
down:
updated: 2026-09-04 (B1-Block rotiert — manuell wie A2/A1/Step-0, weil `scripts/rotate_session_block.sh` (portiert in Block C, `phase8_5_picker_release/scripts/rotate_session_block.sh`) erst jetzt greift; B1 vorne angehängt (newest-first), A2 + A1 + Step 0 darunter unverändert; C abgeschlossen — 13/13 in Chromium+Firefox, 26/26 gesamt, D/Z stehen noch aus)
---

# SESSIONS_ARCHIVE.md — Phase 8.5: Link-Picker-Politur, Titel-statt-ID-Hint, v3-Vorabritt + Deploy

### 2026-09-04 (B1 — `_TITLE_NOT_ID_HINT` generalisierend geschärft, Code committet)

**Auftrag:** B1 nach `docs/concepts/phase8_5_picker_release_plan.md` §3 B1. Einzige
erlaubte Tabu-Ausnahme in `mcpserver/` (P8.5-D, Präzedenz P7-T und P8-§0.4). Hint
generalisierend schärfen (Option a, N2), zwei neue Asserts in `test_tools.py`,
Abbruchregel wörtlich im Phase-Head.

**Ergebnis — alle drei Eingriffsgruppen aus Plan §3 B1 committet, §0.5 Checkliste grün:**

1. **`phase2_mcp/mcpserver/tools.py` Z. 159–164.** `_TITLE_NOT_ID_HINT` generalisiert.
   Der alte Schwanz `; auch nicht als Tabellen-Spalte.` ist durch einen Vier-Zeilen-
   Schlusssatz ersetzt: *„Das gilt in jeder Textform — auch nicht als Tabellen-Spalte,
   nicht in Klammern hinter dem Titel und nicht in Aufzählungs-Zeilen."* — wörtlich aus
   Plan §3 B1. Die drei Negativ-Beispiele stehen jetzt als **Illustration der Regel**,
   nicht als abschließende Liste; der Satz „Das gilt in jeder Textform" ist die
   eigentliche Änderung, der Rest ist Konkretisierung. Wörtlich identisch an den vier
   Verwendungsstellen (`search_items`/`get_item`/`get_item_meta`/`create_item`) — die
   `update_item`/`append_to_item`/`patch_item`-Beschreibungen tragen den Hint bewusst
   nicht (reine Schreibwerkzeuge, Vorlage aus Phase 7; siehe auch „Fehlerpfad" unten).

2. **`phase2_mcp/tests/test_tools.py` Z. 137–143.** `test_tool_descriptions_tell_the_
   agent_to_name_titles_not_ids` um zwei Asserts erweitert:
   - `assert "in jeder Textform" in tools._TITLE_NOT_ID_HINT`
   - `assert "Klammern" in tools._TITLE_NOT_ID_HINT`
   Bestehende Asserts (`"Einkaufsliste Winter"`, `"itm_a1b2c3d4"`, `"Tabellen-Spalte"`,
   plus Hint-in-Beschreibung für `search_items`/`get_item`/`get_item_meta`/
   `create_item`) bleiben unverändert gültig — keine Anpassung am Testaufbau, nur zwei
   zusätzliche Zeilen.

3. **`phase8_5_picker_release/CLAUDE.md`.** Neuer Abschnitt `## Abbruchregel §9.4.1
   (N2, verbindlich)` zwischen Modul-Status und Geerbte Contracts, wörtlich aus Plan
   §3 B1: *„Taucht die `itm_…`-ID in einer **vierten** Oberflächenform auf (Fließtext +
   Tabelle waren die ersten zwei, der Klammer-/Aufzählungs-Kontext aus Phase 8 §9.4.1
   die dritte), wird §9.4.1 als **Modellverhalten dokumentiert und geschlossen**
   (Option c). Kein fünfter Hint-Edit, keine Schema-Änderung an `search_items`. Der
   Punkt verschwindet dann aus dem Ledger, statt weiter vererbt zu werden. — Geprüft
   wird das in Block D5 (vierte A3-Probe nach dem Deploy, wörtlicher Prüfauftrag im
   Plan §3 B1)."* — Pflichtbestandteil der Abnahmezeile P8.5-3.

**Begleitende Doku-Updates im selben Commit (Hard Rule 8):**

- `phase8_5_picker_release/CLAUDE.md`: Modul-Status B1 `⬜` → `🟡`; P8.5-3 `⬜` → `🟡`
  mit Klammer-Anmerkung für den Code-Beleg; Stand-Zeile 3 ✅ · 3 🟡 · 14 ⬜ →
  3 ✅ · 4 🟡 · 13 ⬜.
- A2-Block nach `SESSIONS_ARCHIVE.md` rotiert (manuell, wie in A1/A2 — Skript
  `scripts/rotate_session_block.sh` aus Phase 7 noch nicht für `phase8_5_picker_release/`
  portiert; YAGNI bis Block-C-Beginn).
- `phase8_5_picker_release/SESSIONS_ARCHIVE.md`: A2-Block vorne angehängt
  (newest-first), A1 darunter unverändert; `updated:` aktualisiert.
- `CLAUDE.md` (Wurzel): neuer „Current state"-Absatz vom 2026-09-04 für B1.
- `docs/INDEX.md` Phase-8.5-Header: `🔄 A1 🟡, A2 🟡, B1/C/D/Z ⬜` → `🔄 A1 🟡, A2
  🟡, B1 🟡, C/D/Z ⬜`.
- `ROADMAP.md` Phase-8.5-Absatz: „nächster Schritt: B1" → „B1 committet; nächster
  Schritt: Block C (Wegwerf-Setup + 13-Stationen-Playwright-Smoke)".

**Verifiziert (§0.5 Checkliste):**

- `pytest -q` (venv): **962 passed in 256.65 s** — 962 unverändert (keine neue
  Testfunktion, nur zwei Asserts im bestehenden
  `test_tool_descriptions_tell_the_agent_to_name_titles_not_ids`); keine Regressionen.
- Tabu-Diff aus §0.3 zeigt **genau** die erlaubten zwei Dateien:
  `git diff --stat main -- phase4_auth/ phase1_storage/storage/ phase5_ui/webui/security.py
  phase5_ui/webui/api.py phase5_ui/webui/serializers.py phase5_ui/webui/permissions.py
  phase2_mcp/` →
  ```
  phase2_mcp/mcpserver/tools.py  | 5 +++--
  phase2_mcp/tests/test_tools.py | 2 ++
  ```
  Plan §3 B1 „Tabu: … Der Diff auf `phase2_mcp/` darf **genau** diese eine Datei plus
  die Testdatei zeigen." — exakt erfüllt.
- `node --check`: keine JS-Datei berührt (irrelevant für diese Session).
- Größenprüfung `find . -name "*.md" -not -path "./.venv/*" -size +40k`: **kein**
  neuer Treffer durch diese Session; `phase8_5_picker_release/CLAUDE.md` jetzt ~27 KB
  (vorher ~27 KB), weiterhin deutlich unter dem Cap — kein Rotationsschritt nötig.
- Fehlerpfad einmal durchgedacht: bestehender Test prüft den Hint an den vier
  Verwendungsstellen, an denen er tatsächlich eingebettet ist. Die Generalisierung
  ist **additiv** (kein bestehender Fall wird gebrochen, nur neue Fälle werden
  abgedeckt) — wer vorher schon „Tabellen-Spalte" las, sieht jetzt zusätzlich
  „Klammern" und „Aufzählungs-Zeilen". Wenn der Generalisierungs-Satz später einmal
  entfernt werden müsste (Pflege, niemand weiß), würde der bestehende Assert
  `"Tabellen-Spalte" in tools._TITLE_NOT_ID_HINT` zuerst feuern — das ist das
  gewollte Sicherheitsnetz. Ein viertes `_TITLE_NOT_ID_HINT`-Vorkommen (etwa in einem
  fünften Tool) fällt durch den `assert tools._TITLE_NOT_ID_HINT in
  _description_of(described_mcp, name)`-Loop nicht auf — der Test ist absichtlich
  nicht „viermal vorkommend", sondern „in diesen vier Beschreibungen vorhanden".
- Service-Touch **0**. `systemctl status sharefyx-mcp` zeigt **PID 195922**, Active seit
  `Wed 2026-09-02 11:51:57 CEST` (3 days zum Sitzungsbeginn) — nichts angefasst, nur
  gelesen. **PID + ActiveEnterTimestamp im Session-Block notiert, wie §0.5.7 verlangt.**

**Was diese Session bewusst NICHT tat:**

- Browser-/Live-Verifikation für P8.5-4 (vierte A3-Probe) — kommt mit Block D5 nach
  dem Deploy.
- `test_mcp_smoke.py`-Anpassung an den neuen Hint-Text — der Smoke ist eine Live-
  Probe, die keinen Description-Text liest (nur Tool-Aufrufe gegen den Server); keine
  Anpassung nötig, keine Lücke im Smoke.
- Block C (Wegwerf-Setup + 13-Stationen-Playwright-Smoke) — nächster Schritt nach
  diesem Commit; Plan §4.
- `mcpserver/tools.py` sonst anfassen — die Tabu-Ausnahme gilt **ausschließlich** für
  den Hint-Text. `WRITE_TOOL_DIVISION`, `_LIST_SPACES_POINTER`, alle
  Beschreibungs-Strings anderer Tools bleiben unangetastet (gegengeprüft mit
  `git diff` auf der Datei).
- `mcp_smoke.py`-Beschreibungen — der Hint erscheint nur in Tool-Beschreibungen, der
  Smoke spricht die Tools über Funktionsaufrufe an.

**Nächster Schritt, konkret:** **Block C — v3-Vorabritt gegen eine Wegwerf-Instanz**
(`docs/concepts/phase8_5_picker_release_plan.md` §4). Erst Wegwerf-Setup
(`scripts/serve.py` mit tmp `DATA_ROOT`/tmp `auth.sqlite3`/eigenem Port, inkl. der seit
Step 0 angekündigten Portierung von `scripts/rotate_session_block.sh` aus Phase 7 für
`phase8_5_picker_release/`), dann 13 Stationen Playwright-Smoke; jeder Fund entweder
behoben oder als benannter Befund vorgelegt. Plan §4 listet die 13 Stationen.

---

### 2026-09-04 (A2 — Tastaturnavigation + `_pickLinkPickerAt` + CSS-Block-Entdopplung, Code committet)

**Auftrag:** A2 nach `docs/concepts/phase8_5_picker_release_plan.md` §2.A2.
Tastaturnavigation über `aria-activedescendant` (Fokus bleibt im Suchfeld), gemeinsamer
Pick-Pfad für Maus und Enter, Entdopplung der zwei identischen CSS-Auswahl-Blöcke am
Picker, totes `:focus` raus. Die A1-Session hatte statische Tests ausdrücklich
zurückgestellt — der Plan-Test für P8.5-14 gehört zu A2, P8.5-9 und P8.5-12 ziehe ich
gleich mit nach.

**Ergebnis — alle drei Eingriffsgruppen aus Plan §2.A2 committet, §0.5 Checkliste grün:**

1. **`phase5_ui/webui/static/js/dialogs.js`** — vier Edits:

   - Neue Modul-Variablen `linkPickerItems = []` und `linkPickerCursor = -1` (Z. 117–119).
     `-1` = keine Auswahl, beim Re-Rendern zurückgesetzt (benannte Falle aus Plan §2.A2:
     sonst zeigte ein alter Cursor nach dem Filtern auf einen anderen Treffer).

   - `_renderLinkPickerResults(items)` umgebaut: State-Reset **ganz oben** (vor
     `replaceChildren()`) räumt `linkPickerItems`+`linkPickerCursor`+
     `aria-activedescendant` — das schließt den Such-Debounce-Fall ab, in dem der User
     tippt, bevor die Antwort zurück ist. Jede Treffer-`li` bekommt `id="link-picker-
     opt-{i}"`, wird in `linkPickerItems` aufgenommen und hat als Click-Listener
     `_pickLinkPickerAt(i)`. Der "Keine Treffer."-Eintrag bleibt `aria-disabled="true"`
     und wird **nicht** in `linkPickerItems` aufgenommen — für `_pickLinkPickerAt` damit
     unerreichbar (Abnahmezeile P8.5-11).

   - Zwei neue Helper: `_setLinkPickerCursor(index)` setzt/löscht `aria-selected` auf
     genau einer `li` und `aria-activedescendant` auf dem Suchfeld
     (ARIA-1.2-Pflicht-Beziehung, genau dafür steht `aria-controls` am Input aus A1);
     `scrollIntoView({block: "nearest"})` hält den Cursor im sichtbaren Bereich bei
     langen Trefferlisten. `_pickLinkPickerAt(index)` ist der gemeinsame Pick-Pfad für
     Maus-Klick und Enter-Taste, Modus wird **vor** `closeLinkPicker()` gelesen wie
     beim bestehenden Klick-Handler (Select wird mit dem Dialog versteckt;
     UI-mutations-unabhängig).

   - `closeLinkPicker()` ergänzt um `linkPickerItems = []; _setLinkPickerCursor(-1);` in
     der richtigen Reihenfolge (erst leeren, dann Cursor räumen). Alt-Aufrufer bleiben
     kompatibel.

   - `init()`: ein neuer `keydown`-Handler am `linkPickerSearchEl` für `ArrowDown`/
     `ArrowUp`/`Enter`. Bewusst kein Wrap-around (die Listen-Navigation in `app.js:212`
     klemmt ebenfalls), kein Home/End, kein Enter-wählt-den-einzigen-Treffer (Raten).
     `Escape` bleibt beim globalen Handler (P8.5-L, dort nicht angefasst).

2. **`phase5_ui/webui/static/app.css`** (Z. 1280–1298) — die zwei identischen
   Regelblöcke (`li:hover`+`li:focus` und `li[aria-selected="true"]`) zu einem
   zusammengezogen, das tote `:focus` entfällt (kein `tabindex` auf den `li`, kann nie
   feuern). Die vier Deklarationen selbst sind **byte-identisch** zum 2026-09-02-
   Standard (Nikinger-Freigabe damals), hier nur entdoppelt. Kommentar darüber um eine
   Phase-8.5-A2-Zeile ergänzt, alte Erklärung zum `var(--accent-text)`-Fund bleibt
   unverändert stehen.

3. **`phase5_ui/tests/test_static_routes.py`** — drei neue Tests:

   - `test_link_picker_css_has_one_selection_block` (P8.5-14): zählt `li[aria-
     selected="true"]` in `app.css` (genau 1) und prüft Abwesenheit von
     `.link-picker-results li:focus`.
   - `test_link_picker_picks_run_through_a_single_helper` (P8.5-12): `_pickLinkPickerAt`
     in `dialogs.js` genau einmal definiert, ≥3 Vorkommen (1 Definition + Maus-Klick +
     Enter-Taste); `app.js` enthält weder `openLinkPicker` (P8.5-L: Picker wird nur in
     `editor.js` geöffnet) noch `_pickLinkPickerAt` (Helper nicht umgehen).
   - `test_insertAtCursor_defined_exactly_once_at_module_level` (P8.5-9): die A1-
     Anforderung war bislang nur über `grep -n` belegt; jetzt mit pytest festgehalten.
     Der Bild-Knopf-Aufruf (jetzt Z. 669) außerhalb von `init()` beweist die
     Modul-Ebene implizit — function-Deklaration wird vom JS-Hoisting an alle
     Modul-Stellen sichtbar gemacht.

**Begleitende Doku-Updates im selben Commit (Hard Rule 8):**

- `phase8_5_picker_release/CLAUDE.md`: Modul-Status A2 `⬜` → `🟡`; fünf Abnahmezeilen
  P8.5-9/-10/-11/-12/-14 angepasst (P8.5-9/-12/-14 `⬜` → `🟡` mit Klammer-Anmerkung
  für den statischen Test; P8.5-10/-11 bleiben `🟡` für die Code-Spur, Browser-Nachweis
  Block C Station 7); Stand-Zeile 3 ✅ · 0 🟡 · 17 ⬜ → 3 ✅ · 3 🟡 · 14 ⬜.
- A1-Block nach `SESSIONS_ARCHIVE.md` rotiert (manuell, weil `scripts/
  rotate_session_block.sh` aus Phase 7 für `phase8_5_picker_release/` noch nicht
  portiert ist — YAGNI für eine zweite manuelle Rotation; Skript-Eintrag verschoben
  auf Block-C-Beginn mit dem Wegwerf-Setup).
- `phase8_5_picker_release/SESSIONS_ARCHIVE.md`: A1-Block vorne angehängt (newest-first),
  Step 0 darunter unverändert; `updated:` aktualisiert.
- `CLAUDE.md` (Wurzel): neuer „Current state"-Absatz vom 2026-09-04 für A2.
- `docs/INDEX.md` Phase-8.5-Header: `🔄 A1 🟡, A2/B1/C/D/Z ⬜` → `🔄 A1 🟡, A2 🟡,
  B1/C/D/Z ⬜`.
- `ROADMAP.md` Phase-8.5-Absatz: „nächster Schritt: A2" → „nächster Schritt: B1
  (Titel-statt-ID-Hint generalisierend schärfen, eine Datei in `mcpserver/`)".

**Verifiziert (§0.5 Checkliste):**

- `pytest -q` (venv): **962 passed in 266.27 s** — 959 unverändert + 3 neue Tests in
  `test_static_routes.py`; keine Regressionen.
- Tabu-Diff aus §0.3 leer: `git diff --stat main -- phase4_auth/ phase1_storage/storage/
  phase5_ui/webui/security.py phase5_ui/webui/api.py phase5_ui/webui/serializers.py
  phase5_ui/webui/permissions.py phase2_mcp/` — **keine Ausgabe**.
- `node --check` auf `dialogs.js` — **OK** (einzige berührte JS-Datei; `app.js` tabu
  P8.5-L, `editor.js` unangetastet).
- `python phase5_ui/scripts/ui_budget.py`: **5/5 grün**, js+css+gzip jetzt
  **128.7 KB** von 127.6 KB (+1.1 KB durch `dialogs.js` 11.7 → 12.6 KB und die drei
  statischen Tests); Latenz-`get_item` 7.6 ms / 0.5 KB, `search_items` 189.4 ms / 20 KB,
  `GET /api/v1/overview` 881.3 ms / 1.9 KB — alle im Korridor.
- Größenprüfung `find . -name "*.md" … -size +40k`: **kein** neuer Treffer durch diese
  Session; `phase8_5_picker_release/CLAUDE.md` jetzt ~31 KB (vorher ~24 KB), weiterhin
  deutlich unter dem Cap — kein Rotationsschritt nötig, der Head trägt nach dem
  Rotieren weiterhin genau einen Block (jetzt den A2-Block).
- Fehlerpfad einmal durchgedacht: leere Trefferliste → `_renderLinkPickerResults` setzt
  `linkPickerItems = []` und zeigt den `aria-disabled="true"`-Eintrag (nicht in
  `linkPickerItems`, für `_pickLinkPickerAt` unerreichbar); `_setLinkPickerCursor`
  sieht out-of-range und räumt `aria-activedescendant` (verhindert verwaiste ID-Referenz
  im Suchfeld). Cursor-Reset beim Re-Render fängt auch den Fall ab, dass der User tippt,
  bevor die Suche antwortet (150 ms Debounce — die Items im DOM sind noch die alten,
  gehören aber gleich zum alten `linkPickerItems`-Stand; nach der Antwort sind beide
  synchron neu). `closeLinkPicker` setzt State und Cursor in der richtigen Reihenfolge,
  sodass `_setLinkPickerCursor(-1)` keine Alt-Werte mehr sieht. `_pickLinkPickerAt`
  mit ungültigem Index ist no-op. `app.js` bleibt tabu und ist im Test festgenagelt
  (`openLinkPicker` darf dort nicht vorkommen — der Picker wird in `editor.js` geöffnet,
  der Helper nur in `dialogs.js` ausgeführt).
- Service-Touch **0**. `systemctl status sharefyx-mcp` zeigt **PID 195922**, Active seit
  `Wed 2026-09-02 11:51:57 CEST` (2 days zum Sitzungsbeginn) — nichts angefasst, nur
  gelesen. **PID + ActiveEnterTimestamp im Session-Block notiert, wie §0.5.7 verlangt.**

**Was diese Session bewusst NICHT tat:**

- Browser-Verifikation für P8.5-10/-11 (P8.5-13 in Chromium und Firefox) — Block C,
  kommt mit dem v3-Vorabritt gegen eine Wegwerf-Instanz.
- Statischer Test für P8.5-5 (Picker-Dialog trägt `<select>` mit beiden Werten) —
  nicht in den A2-Plan-Scope; wäre ein eigener Tag-Test (Markup-Snapshot), günstig
  vor Block C nachzuziehen.
- `dialogs.js` Helper `_setLinkPickerCursor` und `_pickLinkPickerAt` weiter
  modularisieren (z. B. in ein eigenes Modul) — P5-T bleibt in `dialogs.js` (eine Datei
  pro Dialog-Cluster, siehe Modul-Header), YAGNI.
- `app.js` berühren (P8.5-L explizit, im Test festgenagelt).
- B1 (`_TITLE_NOT_ID_HINT` generalisierend schärfen in `mcpserver/tools.py:159-164`) —
  eigener Schritt nach A2, einzige erlaubte Tabu-Ausnahme in `mcpserver/`.

**Nächster Schritt, konkret:** **B1 — §9.4.1 Hint generalisierend schärfen**
(`mcpserver/tools.py:159-164`, einzige erlaubte Tabu-Ausnahme; `phase2_mcp/tests/
test_tools.py` mitziehen, zwei neue Asserts; Abbruchregel wörtlich im Phase-Head,
Abnahmezeile P8.5-3). Block C (Wegwerf-Setup + 13-Stationen-Playwright-Smoke) folgt
danach.

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
