---
status: snapshot
purpose: "Mini-Plan P9 Block doing — schließt das Eimer-Loch für `doing` per fünftem `_BUCKETS`-Eintrag „In Arbeit" (Lock P9-V), Voraussetzung für den Deploy `v3.1.0`. Locks P9-V–P9-X, Abnahme P9-59–P9-68, [VERIFY] V173–V178."
read-when: Bau des doing-Blocks (opencode/M3) oder Herkunft von P9-V nachvollziehen
detail: L2
up: ../../phase9_hardening/CLAUDE.md
down:
  - ./phase9_hardening_plan.md   # 📕 übergeordneter P9-Plan; P9-P §1, §8.3, §15 werden hier datiert korrigiert
updated: 2026-10-02 (Block **gebaut** von opencode/M3, §12 Ergebnis: 8 ✅ · 1 ⬜, `pytest` 1128, Browser 11/11 mit Gegenlauf 7 rot; Abweichung §12.3, Befunde B1–B4, ab hier nicht mehr editiert)
---

# Phase 9 — Block doing (fünfter Eimer „In Arbeit")

> **Ein Block, kein Phasenplan.** Anlass: der Deploy `v3.1.0` ist verschoben, weil nach ihm ein
> Mensch `doing` im Status-Feld wählen kann und die Aufgabe dann in **keinem** der vier Ordner
> und keinem Zähler auftaucht. Geschrieben 2026-10-02 gegen `main@97de3d6` von Claude Code.
> Gebaut wird der Block von **opencode/M3** in **einem** Commit, und zwar Code, Tests, Browser-Beleg
> und Doku zusammen (Hard Rule 8). Deployt wird er vom **Nikinger** (§8, Nachschub).
> Der übergeordnete Plan `phase9_hardening_plan.md` ist ein 📕-Snapshot und wird **nicht** editiert.
> Jede Korrektur an ihm steht hier, datiert, mit Verweis auf die Planstelle.

---

## §0 Rahmen

### 0.1 Auftrag in drei Sätzen

Eine Aufgabe mit `status: doing` bekommt einen eigenen Eimer: `_BUCKETS["doing"]`, Rail-Label
„In Arbeit". Danach erscheint sie in genau einem Zähler und in genau einem Ordner, und Zähler und
Liste stimmen für diesen Ordner per Konstruktion überein. Die Maschinenebene (Schema, REST, MCP)
bleibt unverändert roh, damit ein angeschlossenes LLM weiter `status: doing` und `assignee` liest.

### 0.2 Scope

**Drin:**
- `_BUCKETS`-Eintrag samt Kommentar-Neufassung (`phase5_ui/webui/api.py`)
- Rail-Label (`phase5_ui/webui/static/js/state.js`)
- Tests, darunter das Umdrehen eines bewusst gesetzten Step-F-Wächters
- ein Browser-Beleg mit Wegwerf-Instanz
- Doku im selben Commit

**Draußen**, mit Fundort:
- A7/A8, Gate/Z, D1 (ESC/Vollbild), `LEGACY_*`, `_trash`-Rückfrage, V118/V136 → P9-Plan bzw. Phase-Head
- Hervorhebung von `doing` auf der Übersicht, Assignee-Anzeige/-Picker → **P10, unverändert** (P9-P)
- Übersetzung der rohen Statuswerte in Select/Metazeile (`open`, `done`, …) → P10 (P9-W)
- Der Deploy selbst → Nikinger (§8)

### 0.3 Tabu (Bereichs-Diff über den Block-Commit)

Es gelten die Tabu-Liste aus P9-Plan §0.3 **und zusätzlich** `phase1_storage/`. Kandidat (a)
braucht keine Storage-Zeile. Damit gibt es **keine zehnte Contract-Öffnung**, und die Step-F-Ausnahme
(P9-G) wird hier nicht weiter benutzt.

```bash
git diff --stat HEAD~1..HEAD -- \
  phase1_storage phase2_mcp/mcpserver phase4_auth/authserver phase6_shares phase7_spaces_admin
# erwartet: leer
```

`phase2_mcp/mcpserver/` steht bewusst mit drin. Der Block ändert die MCP-Fläche **nicht**, weil
`doing` und `assignee` dort seit Step F vollständig sind (§3.3).

### 0.4 Selbstprüfung vor dem Commit (P9-Plan §0.4, unverändert, hier konkret)

1. `.venv/bin/python -m pytest -q`, Baseline **[V177]**. Jede Abweichung nach unten ist Abbruch,
   jede nach oben steht mit Zahl im Commit.
2. `.venv/bin/python phase5_ui/scripts/ui_budget.py` → 5/5 im Korridor.
3. `node --check phase5_ui/webui/static/js/state.js`
4. Tabu-Diff §0.3 → leer.
5. `.venv/bin/python scripts/doc_health.py` → **0 Befunde**.
6. Kein Service-Touch, kein `pkill -f`, kein `systemctl` (Hard Rule 9). Die Wegwerf-Instanz
   wird nur über `p9_doing_wegwerf.py stop` (PID-Datei) gestoppt.
7. Testumgebung ohne geerbte `SHAREFYX_*`/`SFX_*`-Variablen
   (`env | grep -E '^(SHAREFYX_|SFX_)'` muss leer sein).

### 0.5 Hard Rules, die der Block berührt

| Hard Rule | Wie der Block sie hält |
|---|---|
| Bauprinzip „der Server ist dumm" | Die Fixlogik ist ein Gleichheitsvergleich von Statuswerten, sonst nichts |
| HR 1, keine Secrets | Das Wegwerf-Skript erzeugt Passwort und TOTP-Seed zur Laufzeit unter `/tmp/opencode/…` mit `0600`, wie `p9_step_g_wegwerf.py`. **Nichts davon wird committet**, auch keine `credentials.json` und kein Screenshot mit sichtbarem QR/Seed |
| HR 3, kein Write ohne `version` | Der Block schreibt nur über den bestehenden Editor-Pfad (`saveItem()` → PATCH mit `version`). Kein neuer Schreibweg, keine Zähllogik mit eigenem Zustand |
| HR 8 | Doku im selben Commit (§7) |

---

## §1 Step 0: Verifikations-Durchlauf (2026-10-02, Claude Code)

**Ergebnis: an der Doku nichts zu reparieren.** Vier Plan-Prämissen sind datiert zu korrigieren,
und eine Größe ist bereits benannt.

| Prüfung | Befund |
|---|---|
| `scripts/doc_health.py` (Index-Zeilen, Header-Cards, `up:`/`down:`-Links, Oversize) | **0 Befunde** |
| Heads > 40 KB | `phase9_hardening/CLAUDE.md` **42.393 B**, im INDEX bereits als Überschreitung benannt (P8-P). Die Session-Rotation im Block-Commit verkleinert ihn, gemessen wird nach der Rotation |
| Doku ↔ Code | Alle Anker des Nikinger-Briefings stimmen am Code (Tabelle §3). Ausnahme: die **Zeilenverweise im `_BUCKETS`-Kommentar** sind gedriftet (`list.js:516` → real `:544`, `store.py:520` → real `:536`). Der Kommentar wird in D1 ohnehin neu geschrieben (K4) |

**Datierte Korrekturen am 📕 P9-Plan (2026-10-02):**

- **K1, Prämisse von P9-P (§1 Z. 184, §8.3, §15 Z. 1299):** Der Plan nahm an, `doing` sei „in
  keinem UI-Pfad" erreichbar. Für die *Hervorhebung* stimmt das, für die *Erreichbarkeit* nicht.
  Zwei Wege führen nach dem Deploy hin:
  - `editor.js:244 populateStatusSelect()` listet `state.meta.status_values[itemType]` roh, also
    mit `doing`.
  - **Gewichtiger:** Claude setzt `doing` per MCP `update_item(status="doing")`. Genau dafür
    existiert P9-H.
  
  Auch ein Select ohne `doing` hätte das Loch also nicht geschlossen. Das ist keine Fehlplanung:
  der Plan sah den Deploy-Fall nicht vor.
- **K2, Abnahme-Nummern:** Das Briefing schlug „ab P9-45" vor. P9-45 bis P9-52 gehören Step G,
  P9-53 bis P9-55 Step H, P9-56 bis P9-58 sind phasenweit (Plan §14). Dieser Block beginnt bei
  **P9-59**.
- **K3, Dateiname:** Lock P9-T verlangt `phase9_hardening_block_<X>_plan.md`. Der Briefing-Vorschlag
  `phase9_hardening_doing_bucket_plan.md` weicht davon ab, der Lock gewinnt. Daher heißt diese
  Datei `phase9_hardening_block_doing_plan.md`.
- **K4, `_BUCKETS`-Kommentar `api.py:130–148`:** Er nennt den Befund „bewusst NICHT behoben" und
  (a) „genau die Hervorhebung, die P9-P P10 zuteilt". Mit P9-V ist beides überholt. D1 schreibt den
  Absatz datiert neu, statt ihn stehen zu lassen.

---

## §2 Gelockte Entscheidungen

| Lock | Entscheidung | Begründung |
|---|---|---|
| **P9-V** | *(Nikinger, 2026-10-02)* **Kandidat (a): ein fünfter `_BUCKETS`-Eintrag `"doing": {"type": "task", "status": "doing"}`.** Damit wird **P9-P datiert eingeengt**: ein Eimer für einen Statuswert ist **Navigations-Vollständigkeit**, dieselbe Klasse wie `done` in P5 Step 7b (Kommentar `api.py:124–127`). Er ist keine Hervorhebung. P10 behält die prominente Darstellung auf der Übersicht, „aktuelle Aufgabe" und die Assignee-Anzeige bzw. den -Picker | Kosten gemessen: ein Rail-Ordner mehr pro Space, **immer** sichtbar, auch bei 0 (`tree.js:58` `renderFolders()` kennt keinen Zero-Skip). Ein Übersichts-Chip kommt **erst ab Zähler ≥ 1** dazu (`list.js:116` `if (!count) return`). Kein `storage/`-Touch, keine Vertragsänderung am `meta`-Payload, Zähler == Liste bleibt per Konstruktion wahr (`_overview()` ruft `store.search(**filters)` mit denselben Filtern auf, die `filterParams()` sendet). Verworfen sind (b) und (c), siehe §2.1 |
| **P9-W** | *(abgeleitet aus der Nikinger-Vorgabe, vom Nikinger bestätigt 2026-10-02)* **Drei Sprachebenen, nur die oberste wird übersetzt.** (1) Schema `STATUS_VALUES`: roher Wert `doing`. (2) API-Vertrag REST `/meta`, `/items`, `/overview` und MCP `search_items`/`get_item`: roh `status: "doing"` plus `assignee`. (3) UI: **nur** `BUCKET_LABELS.doing = "In Arbeit"`. Status-`<option>`, Listen-Metazeile, `roMeta` und `metaDigest` bleiben roh, wie heute für `open`/`done`/`active`/`archived` | Nikinger-Vorgabe 2026-10-02: die Übersetzung soll so sein, *„dass ein angeschlossenes LLM aus Ausgaben entnehmen kann, wem sie zugeteilt ist"*. Das verlangt, dass Ebene 1 und 2 nie übersetzt werden und das UI-Speichern `assignee` nicht verliert (P9-65). Eine Übersetzung aller Statuswerte hieße: neue `STATUS_LABELS`-Tabelle mit vier Konsumenten. Das ist ein eigener P10-Punkt, kein Teil des Lochs |
| **P9-X** | **`_BUCKETS`-Reihenfolge: `open`, `doing`, `done`, `note`, `archived`.** `archived` bleibt **letzter** Eintrag, `open` bleibt **erster** | `archived` zuletzt: `bucketFor()` (`list.js:544`) nimmt den ersten Treffer, Begründung im Kommentar `api.py:119–122`, gepinnt von `test_meta.py:60`. `open` zuerst: `app.js:295` fällt bei unbekanntem `state.filter` auf `names[0]` zurück, und `state.js:34` startet mit `filter: "open"`. `doing` steht zwischen `open` und `done`, weil das die Lebenslaufrichtung einer Aufgabe ist, und genau so liest man die Rail von oben nach unten |

### 2.1 Verworfene Kandidaten (Argument, kein Geschmack)

**(b) „Offen" = `{open, doing}`, beide Varianten.**
- `filterParams()` (`list.js:529`) gibt den Bucket über `new URLSearchParams(...)` (`:556`) weiter.
  Eine Liste wird dort zu `status=open%2Cdoing`.
- `_items_get` liest `status=q.get("status")` (`api.py:782`) als einen String. `store.search()`
  vergleicht exakt (`store.py:536`). Ergebnis: eine **stille leere Liste**.
- (b)(i) repariert das im Store, als zehnte P1-Contract-Öffnung.
- (b)(ii) repariert es in Web-UI und `_overview()` mit Mengenlogik **neben** `store.search()`.
  Damit bricht das Konstruktionsargument „Zähler == Liste" im Kommentar `api.py:629–633`.
- Beide kosten mehr als (a) und ändern den `meta`-Vertrag.

**(c) `doing` nicht ins Status-Select.** Das schließt das Loch **nicht**, aus zwei Gründen:
1. `doing` kommt per MCP herein (K1). Das Item fällt dann weiter durch alle vier Eimer.
2. Der Editor wird für jedes solche Item kaputt:
   - `editor.js:373` setzt `fieldStatusEl.value = "doing"`. Ohne passende `<option>` ist der Wert danach `""`.
   - `isDirty()` (`editor.js:182`) meldet das Item damit **beim Öffnen** schon als geändert, also fragt jedes Schließen „ungespeichert?".
   - Speichern sendet `status: ""`. `store.py:190` (`if status not in allowed`) lehnt das ab.
   
   Ein Mensch könnte eine von Claude gesetzte `doing`-Aufgabe also nicht mehr speichern. Das ist ein
   Defekt im Schreibpfad, keine Geschmacksfrage.

---

## §3 Abhakliste: jede Stelle, die Eimer oder Status liest

### 3.1 Die sechs `state.meta.buckets`-Konsumenten (Briefing §5)

| # | Stelle (gemessen 2026-10-02) | Was sie mit `doing` tut | Änderung |
|---|---|---|---|
| 1 | `app.js:294–295`: `names = Object.keys(meta.buckets)`, Fallback `names[0]` | `names[0]` bleibt `"open"` (P9-X) | keine |
| 2 | `dialogs.js:451–452`: Typ-Vorgabe im Anlegen-Dialog | `buckets.doing.type === "task"`, also ist „Aufgabe" vorbelegt | keine. **Benannt:** die neue Aufgabe bekommt `status: open` (POST ohne Status, `dialogs.js:1068`), `bucketFor()` springt danach nach „Offen", nicht nach „In Arbeit". Das ist dasselbe Verhalten wie heute beim Anlegen aus „Erledigt", also konsistent und kein Fix |
| 3 | `list.js:389–391`: Leermeldung, Typ des Anlegen-Knopfs | Ergibt „Erste Aufgabe anlegen" und „Noch nichts unter „In Arbeit"" (`:382`) | keine |
| 4 | `list.js:540–542`: `filterParams()` | `{type: "task", status: "doing"}` wird zu `?type=task&status=doing`. `_items_get` (`api.py:782`) liest das als String, `store.search` vergleicht exakt. Korrekt | keine |
| 5 | `list.js:544–553`: `bucketFor()` | Ein `doing`-Task trifft den 2. Eintrag. Ein archivierter Task trifft nur `archived`, weil `doing.status ≠ archived` | keine |
| 6 | `tree.js:16–17`: `bucketNames()` | 5 Namen. `renderFolders()` (`:58`) baut 5 Ordner, Label aus `BUCKET_LABELS` (`:72`) | keine (Label: D2) |

### 3.2 Weitere Leser, ebenfalls abgehakt

| Stelle | Befund | Änderung |
|---|---|---|
| `list.js:81`, `:116–127` Übersichts-Chips | Chip „N In Arbeit" nur bei N ≥ 1 | keine |
| `list.js:169` `openFromOverview()`, `dialogs.js:1074` | `bucketFor()` liefert jetzt `"doing"` statt `null`, der `|| state.filter`-Rückfall greift für `doing` nicht mehr | keine |
| `list.js:274` Brotkrumen, `:382` Leermeldung, `:124/:126` Chip-Text, `tree.js:72` Rail | lesen `BUCKET_LABELS[b] \|\| b`. Ohne D2 stünde dort roh „doing" | **D2** |
| `editor.js:244–252` `populateStatusSelect()` | listet `doing` roh als Option (P9-W) | keine |
| `editor.js:190` `metaDigest`, `:350` `roMeta`, `list.js:214` `itemMetaLine()` | zeigen `doing` roh (P9-W, Status quo für alle Werte) | keine |
| `editor.js:165–174` `currentFormValues()` → `saveItem()` (`:499`) | sendet **kein** `assignee`, also bleibt es beim PATCH unberührt (`store.update` ändert nur übergebene Felder) | keine, aber Test T5 |
| `api.py:353–356` `/meta` | gibt `_BUCKETS` verbatim heraus | über D1 |
| `api.py:628–659` `_overview()` | zählt über `_BUCKETS.items()`, `doing` wird damit automatisch gezählt | über D1 |
| `state.js:34` `filter: "open"` | Startordner unverändert | keine |
| `graph.js` | liest keinen Status (grep 2026-10-02) | keine |

### 3.3 Der `store.search`-Pfad und `phase1_storage`

`store.py:536` (`if status is not None and item.status != status`) bleibt ein Gleichheitsvergleich.
Unter (a) ist das **richtig**, denn jeder Eimer hat genau einen Statuswert. Keine Änderung in
`phase1_storage/`. Folglich muss der Contract-Absatz in `phase1_storage/CLAUDE.md` §Geerbte
Contracts **nicht** mitgezogen werden **[V174]**.

MCP: `search_items` liefert `status` und `assignee` im Summary (`tools.py:219`, `:230`), `get_item`
in `:561`. Bewiesen von `phase2_mcp/tests/test_tools.py:1047`
(`test_create_item_accepts_the_doing_status_and_the_assignee`, liest `assignee` über
`search_items` zurück). P9-W Ebene 2 ist damit bereits erfüllt, der Block muss nur verhindern, dass
das UI-Speichern sie bricht (T5).

---

## §4 Bauschritte (opencode/M3, ein Commit)

### D1: `phase5_ui/webui/api.py`

1. In `_BUCKETS` (`:149–154`) nach `"open"` einfügen:
   ```python
       "doing": {"type": "task", "status": "doing"},
   ```
   Ergebnis-Reihenfolge `open, doing, done, note, archived` (P9-X). Typannotation unverändert.
2. Den Kommentarblock **`:130–148`** (beginnt `# [P9 Step F, 2026-09-30 — **BEFUND, bewusst NICHT
   hier behoben…`) **ersetzen** durch einen datierten Absatz. Die Zeilen `:115–127` (Herkunft,
   `archived`-zuletzt-Begründung, `done`-Fund) bleiben **wörtlich** stehen. Inhalt des neuen Absatzes:
   - `[P9 Block doing, 2026-10-02 — Lock P9-V]`: `doing` hätte dasselbe Loch wie `done` in Step 7b
     wieder aufgerissen. Geschlossen per fünftem Eintrag.
   - Ein Eimer pro Statuswert ist Navigations-Vollständigkeit, keine Hervorhebung. Die bleibt P10 (P9-P eingeengt).
   - Die Mengen-Variante „Offen = {open, doing}" ist verworfen: `URLSearchParams` macht daraus
     `open%2Cdoing`, und `store.search` vergleicht exakt. Das ergäbe eine stille leere Liste
     (Plan §2.1).
   - Wächter: `phase9_hardening/tests/test_doing_bucket.py` (Partition aus `STATUS_VALUES`).
   - **Keine Zeilennummern** in den Kommentar schreiben, nur Funktionsnamen. Die gedrifteten
     Nummern waren genau K4.

### D2: `phase5_ui/webui/static/js/state.js`

In `BUCKET_LABELS` (`:12–17`) zwischen `open` und `done` einfügen:
```js
  doing: "In Arbeit",
```
Keine weitere JS-Änderung. `editor.js` bleibt unberührt, damit bleibt Wächter #14 in
`test_step_f_schema.py` (`editor.js` nennt `doing` nicht) **unverändert grün**, und das ist gewollt (P9-W).

### D3: Tests (Liste §5)

### D4: Browser-Beleg (§6)

### D5: Doku (§7)

---

## §5 Testliste

Zwei Orte, nach dem Step-G-Präzedenzfall: **statische und Partitions-Wächter** in der neuen
Datei **`phase9_hardening/tests/test_doing_bucket.py`** (Serienname wie `test_step_f_schema.py`).
**HTTP-Tests** kommen nach **`phase5_ui/tests/test_overview.py`**. `phase9_hardening/tests/` hat
kein `conftest.py`, die App-Fixtures (`overview_app`, `ticking_store`, `seeded`, `totp_code`) leben
nur unter `phase5_ui/tests/`. Step G hat seine Route-Tests aus demselben Grund in `test_api.py`
gelegt (V176).

| # | Test (exakter Name) | Ort | Prüft | Art |
|---|---|---|---|---|
| T1 | `test_bucket_order_is_open_doing_done_note_archived` | `test_doing_bucket.py` | `list(_BUCKETS) == ["open", "doing", "done", "note", "archived"]` (P9-X) | (a) statisch |
| T2 | `test_every_status_value_lands_in_exactly_one_bucket` | `test_doing_bucket.py` | **aus `STATUS_VALUES` generiert**: Für jedes `(type, status)` wird die Filterbedingung von `bucketFor()` in Python nachgebildet (`(not f.get("type") or f["type"] == t) and (not f.get("status") or f["status"] == s)`). Erwartet: **genau ein** passender Eimer. Hätte `done` (Step 7b) und `doing` gefangen, und schlägt beim nächsten neuen Statuswert laut an | (a) Partition |
| T3 | `test_doing_task_counts_in_doing_and_nowhere_else` | `phase5_ui/tests/test_overview.py` (Fixture `seeded`, nach T8) | Seed = `seeded`: 1 `open`, 1 `doing` (`assignee=SPACE`, T8), 1 `done`, 1 `note`, 2 `archived`. `GET /api/v1/overview` liefert für `SPACE` `counts == {"open":1, "doing":1, "done":1, "note":1, "archived":2}` **exakt** (Dict-Gleichheit, nicht nur `["doing"]`). Zusätzlich `sum(counts.values()) == own["item_count"]` (== 6; `item_count` zählt alle Indexzeilen des Space, `store.py:405–407`): kein Item fällt durch, keins zählt doppelt | (b) API mit echtem `doing`-Item |
| T4 | `test_doing_counter_equals_doing_list` | `phase5_ui/tests/test_overview.py` | Gleicher Seed. `GET /api/v1/items?type=task&status=doing&space=niklas` liefert `total == counts["doing"] == 1`, und `items[0]["title"] == "laufende Aufgabe"` (das konkrete Item, nicht nur die Zahl) | (c) Zähler ↔ Liste |
| T5 | `test_ui_shaped_patch_keeps_doing_and_assignee` | `phase5_ui/tests/test_overview.py` (eigenes Item in `ticking_store`, PATCH mit CSRF wie in `test_api.py`s PATCH-Tests) | Ein `doing`-Item mit `assignee` wird per PATCH mit **genau** dem Feldsatz von `saveItem()` bearbeitet (`version, format, title, body, status, due, tags, links`, **ohne** `assignee`, Titel geändert). Danach liefern `GET /api/v1/items/{id}` **und** `store.search(status="doing").items[0]` `status == "doing"` und `assignee == "niklas"` (P9-W, LLM-Lesbarkeit) | Regressionswächter |
| T6 | `test_every_bucket_has_a_german_label` | `test_doing_bucket.py` | Parst die Schlüssel von `export var BUCKET_LABELS = {…}` aus `state.js` per Regex. Erwartet: `set(labels) == set(_BUCKETS)` und `labels["doing"] == "In Arbeit"` | (a) statisch |
| T7 | **umbenannt**: `test_the_bucket_hole_for_doing_is_named_not_silently_fixed` → **`test_the_doing_bucket_closes_the_hole`** | `phase9_hardening/tests/test_step_f_schema.py:303` | Assertion **umdrehen**: `'"doing"' in buckets.group(1)`. Der Marker wird `"P9-V" in source.split("_BUCKETS:")[0]` statt `"P9 Step F"`. Der Docstring trägt **beide** Richtungen mit Datum (2026-09-30 bewusst offen → 2026-10-02 geschlossen per P9-V). Modul-Docstring-Liste Z. 32–33 nachziehen. Umbenennen nach P8.6-I-Mechanik: der alte Name wäre sonst eine Lüge | (a) Wächter-Umkehr |
| T8 | `seeded`-Fixture erweitern | `phase5_ui/tests/test_overview.py:72` | Eine Zeile `ticking_store.create(SPACE, type="task", title="laufende Aufgabe", status="doing", assignee=SPACE)` als **erste** Anweisung des Fixtures. Grund: `ticking_store` rückt pro Schreibvorgang eine Minute vor, und `_RECENT_LIMIT = 5`. Als ältestes Item verdrängt es keins der fünf bisherigen aus `recent`. `test_recent_is_newest_first_and_carries_no_snippet` prüft nur Sortierung und `≤ 5`, würde also auch sonst nicht rot (gemessen 2026-10-02), aber die Position hält den Datenstand der übrigen `seeded`-Tests unverändert. Den Fixture-Docstring („Ein Item je Ordner plus…") im selben Edit um den `doing`-Task ergänzen. Ohne sie läuft `test_counts_match_the_item_list_for_the_same_bucket` (`:98`) für `doing` **vakuös** (0 == 0). Dazu in `test_archived_task_lands_in_archive_and_done_task_is_not_lost` (`:115`) die Zeile `assert counts["doing"] == 1` ergänzen. `counts["open"] == 1` bleibt, und das belegt, dass `doing` **nicht** in „Offen" zählt | (c) bestehender Konsistenztest scharf |

`test_meta.py:46` (`buckets == _BUCKETS`, `archived` zuletzt) bleibt **unverändert** und läuft mit.

**Gegenlauf (Pflicht, Zahlen in den Commit):** Jeden Verstoß einzeln einbauen, `.venv/bin/python -m pytest
phase9_hardening/tests/test_doing_bucket.py phase9_hardening/tests/test_step_f_schema.py
phase5_ui/tests/test_overview.py phase5_ui/tests/test_meta.py -q` laufen lassen und die roten Tests
notieren. Danach zurückbauen und `git diff` prüfen: leer gegenüber dem Bau-Stand.

| Verstoß | erwartet rot (mindestens) |
|---|---|
| G1 `"doing"`-Eintrag aus `_BUCKETS` entfernt | T1, T2, T3, T4, T6, T7, T8 |
| G2 `"archived"` vor `"doing"` verschoben | T1, `test_meta.py` (archived zuletzt) |
| G3 `_BUCKETS["doing"]["status"] = "open"` (Duplikat) | T2 (zwei Treffer bzw. `doing` ohne Treffer), T3, T4 |
| G4 `doing: "In Arbeit"` aus `BUCKET_LABELS` entfernt | T6 |
| G5 im T5-Test der PATCH-Body um `"assignee": ""` ergänzt (simuliert ein UI, das das Feld mitschickt) | T5 |

Wird ein Verstoß **nicht** rot, ist der zugehörige Wächter wertlos und muss neu geschnitten werden.
Das ist dann ein Befund, nicht stillschweigend weiterbauen.

---

## §6 Browser-Beleg (Pflicht, Standing-Permission)

Kein statischer Test beweist, dass ein Rail-Zähler im Browser umspringt. Zwei neue Skripte folgen
der Step-G-Serie, als **Kopie mit geänderten Konstanten**, nicht als Import. Die Step-G-Skripte
hängen an Modulkonstanten (`ROOT`, `PORT`, `PROBE_TITEL`), ein Import würde sie verbiegen.

**`phase9_hardening/scripts/p9_doing_wegwerf.py`**, Kopie von `p9_step_g_wegwerf.py`:
- `ROOT = Path("/tmp/opencode/p9-doing-wegwerf")`, `PORT = 18776` **[V175]**
- dieselbe TLS-Harness-Begründung (`require_csrf` braucht exaktes `https`-Origin, Docstring übernehmen)
- Seed in Space `alpha`, **bei jedem Start neu** (frisches `DATA_ROOT` löschen + anlegen, damit Zähler deterministisch sind):
  - `"Offene Probe"`: task, open, `assignee="alpha"`
  - `"Laufende Probe"`: task, doing, `assignee="alpha"`
  - `"Erledigte Probe"`: task, done
  - `"Probe-Notiz"`: note
- `start` / `stop`; `stop` ausschließlich über `serve.pid`

**`phase9_hardening/scripts/p9_doing_self_check.py`**, Kopie der Login-/API-Teile von
`p9_step_g_self_check.py` (`_generate_totp`, `login`, `_api`, TOTP-Fensterwarten):

| Station | Handlung | Prüfung (`pruefe(...)`) |
|---|---|---|
| S1 | Login, Übersicht | Zeile `alpha` trägt einen Chip mit `data-bucket="doing"` und Text `1 In Arbeit` |
| S2 | `alpha` öffnen (`.overview__space-open`) | `.tree__folder[data-space="alpha"][data-bucket]` liefert **5** Knöpfe (der `[data-bucket]`-Filter verhindert, dass echte Ordner mitgezählt werden), `data-bucket` in Reihenfolge `open, doing, done, note, archived`. Labels `Offen, In Arbeit, Erledigt, Notizen, Archiv`. Kein Label ist roh `doing` |
| S3 | Zähler lesen | `.tree__count` von `open` = `1`, `doing` = `1` |
| S4 | Ordner „In Arbeit" klicken | Liste enthält genau `Laufende Probe`, Brotkrumen `alpha › In Arbeit` |
| S5 | Ordner „Offen", `Offene Probe` öffnen, `#meta-panel` aufklappen (`<details>`, `summary` klicken), `#field-status` auf `doing` setzen (`select_option`), `#save-button` | Toast „Gespeichert" |
| S6 | **ohne Reload** Zähler neu lesen | `open` = `0`, `doing` = `2`. **Das ist der Kernbeleg** (`afterWrite()` → `loadOverview()`, `editor.js:468`) |
| S7 | API-Gegenprobe mit derselben Sitzung | `GET /api/v1/overview` → `counts` für `alpha` == die Rail-Texte aus S6. `GET /api/v1/items?type=task&status=doing&space=alpha` → `total == 2` |
| S8 | `GET /api/v1/items/<id von Offene Probe>` | `status == "doing"`, `assignee == "alpha"`: das UI-Speichern hat die Zuweisung nicht verloren (P9-W) |

Screenshots nach `docs/screenshots/` (1440×900):
- `p9_doing_01_uebersicht_chip.png` (S1)
- `p9_doing_02_rail_fuenf_ordner.png` (S2/S3)
- `p9_doing_03_liste_in_arbeit.png` (S4)
- `p9_doing_04_nach_statuswechsel.png` (S6)

**Kein** Screenshot zeigt den Login-QR oder die `credentials.json`. `screenshots_latest/` wird auf
`p9_doing_*` umgehängt, nach demselben Muster wie `p9_btn2_*`.

**Browser-Gegenlauf:** Einmal mit `git stash push -- phase5_ui/webui/api.py phase5_ui/webui/static/js/state.js` (nur D1 und D2 zurückgenommen; ein nacktes `git stash` nähme auch Tests und Doku mit). Danach die Instanz neu starten
laufen lassen. Erwartet rot: S1 (kein Chip), S2 (4 Ordner), S6 (`doing`-Zähler fehlt). Zahl der
roten Stationen in den Commit, danach `git stash pop` und `git diff --stat` gegen den Bau-Stand prüfen. Der Lauf ohne Fix beweist, dass das Skript
das Loch überhaupt sehen kann.

Ablauf: `python phase9_hardening/scripts/p9_doing_wegwerf.py start` →
`… p9_doing_self_check.py` → `… p9_doing_wegwerf.py stop`. Erwartung: **8/8 Stationen grün**.

---

## §7 Doku im selben Commit (Hard Rule 8)

1. **`phase9_hardening/CLAUDE.md`**:
   - Modulstatus: die **bestehende** Zeile `doing` (vom Plan-Commit als „⬜ geplant" angelegt) auf `✅ code-complete, nicht deployt` setzen und mit Zahlen füllen (pytest, Gegenlauf, Browser 8/8). **Keine** zweite Zeile anlegen
   - Zeile F: der Satz „ein Befund bewusst NICHT behoben" bekommt den datierten Nachsatz „geschlossen 2026-10-02 per P9-V"
   - Neuer `## Session stopped — <Datum> (…)`-Block **unter** den bestehenden anhängen, dann `scripts/rotate_session_block.sh phase9_hardening` (rotiert den alten verbatim). Danach die Head-Größe messen. Liegt sie ≤ 40 KB, die INDEX-Zeile entsprechend korrigieren, sonst die neue Zahl benennen
2. **Diese Datei**: `status: snapshot`, `updated:` nachziehen und einen neuen Abschnitt `§12 Ergebnis` anhängen: jede Abnahmezeile aus §9 mit ✅/⚠️/⬜ und dem konkreten Beleg (Testname, Zahl, Screenshot). Danach wird sie nicht mehr editiert
3. **`docs/INDEX.md`**: die Zeile dieser Datei (🔄 → 📕) und die Phase-9-Head-Zeile nachziehen. Rotation per `scripts/rotate_index_updates.sh`, falls die `updated:`-Kette es verlangt (P9-L)
4. **`CLAUDE.md`** §Current state: neuer Kurzblock oben (Ergebnis zuerst, nächster Schritt = Deploy durch den Nikinger)
5. **`docs/UPDATE_LOG.md`: NICHT anfassen.** Ein heute datierter Block ließe das `deploy.sh`-Gate (P6-X) bei einem späteren Deploy-Tag abbrennen. Der Eintrag gehört in den Deploy-Commit (§8)
6. **Badge `app.html:20`: NICHT anfassen**, ebenfalls Deploy-Commit

---

## §8 Nachschub: Deploy `v3.1.0` (Nikinger, NICHT Teil des Blocks)

`sudo`, `systemctl` und `deploy.sh` sind ausschließlich Nikinger-Schritte (Hard Rule 9, P9-S).
Reihenfolge am Deploy-Tag:

1. **Release-Commit — opencode/M3** (Nikinger-Festlegung 2026-10-02: M3 bearbeitet Badge und `UPDATE_LOG`, am Deploy-Tag, als eigener Commit nach dem Block-Commit):
   - `phase5_ui/webui/static/app.html:20` `v3.0.2` → `v3.1.0`
   - **neuer** Block `## <Deploy-Tag YYYY-MM-DD>` **oben** in `docs/UPDATE_LOG.md`, unter dem
     Format-Kommentar. **Jede Aussage eine einzige `- `-Zeile**: `parse_update_log()` liest jede
     `- `-Zeile als eigenen Eintrag und verwirft umbrochene Fortsetzungen. Zum Beispiel:
     - `- Aufgaben haben einen neuen Status „In Arbeit" mit eigenem Ordner in der Navigation.`
     - weitere Zeilen für die übrigen seit `v3.0.2` gebauten Steps (D2, E, G, `.toolbar-btn` …),
       jeweils eine Zeile. Den Wortlaut legt der Nikinger fest
   - `pytest` grün, `ui_budget` 5/5, Push
2. **Nikinger:** `sudo /opt/sharefyx/… /deploy.sh main` (Pfad wie am 2026-09-18, siehe
   `phase5_ui/scripts/deploy.sh` und Phase-8.6-Gate-Protokoll).
3. **Nikinger:** `phase8_5_picker_release/scripts/health_gate.sh --expected-version=v3.1.0
   --require-todays-update-log --expected-sha=<sha des Release-Commits>` → alle Prüfungen grün.
4. **Bei diesem Deploy mitnehmen, weil es der erste mit Step F ist:** die Dauer des
   Index-Neuaufbaus am echten `DATA_ROOT` notieren (**P9-43**, V161 hat nur den synthetischen
   Vorabwert 0,4–0,6 s).
5. Kurzer Augenschein im echten Browser: Rail zeigt „In Arbeit" in jedem Space.

---

## §9 Abnahme (P9-59 – P9-68)

| Zeile | Kriterium | Beleg (nicht nur „Test grün") |
|---|---|---|
| **P9-59** | Eine `doing`-Aufgabe zählt in „In Arbeit" und in **keinem** anderen Eimer | T3 Dict-Gleichheit aller fünf Zähler + Browser S3 |
| **P9-60** | Zähler == Liste für „In Arbeit", mit nichtleerem Bestand | T4 (ID-Gleichheit) + T8 (bestehender Konsistenztest, jetzt nicht vakuös) + Browser S7 |
| **P9-61** | Jede `(type, status)`-Kombination aus `STATUS_VALUES` landet in genau einem Eimer | T2, Gegenlauf G1/G3 rot |
| **P9-62** | Reihenfolge `open, doing, done, note, archived`, `archived` zuletzt, `open` zuerst | T1 + `test_meta.py:60`, Gegenlauf G2 rot + Browser S2 (`data-bucket`-Folge im DOM) |
| **P9-63** | Rail und Chips zeigen „In Arbeit", nirgends roh `doing` | T6 + Browser S1/S2 + Screenshot `p9_doing_02` |
| **P9-64** | Statuswechsel `open` → `doing` im Editor lässt die Rail-Zähler **ohne Reload** umspringen | Browser S5/S6 (`1/1` → `0/2`) + Screenshot `p9_doing_04` + Browser-Gegenlauf |
| **P9-65** | Maschinenebene roh und vollständig: REST/MCP liefern `status: "doing"` + `assignee`, und UI-Speichern verliert `assignee` nicht | T5 + `test_tools.py:1047` + Browser S8 |
| **P9-66** | Kein `storage/`-, MCP- oder Tabu-Touch, keine zehnte Contract-Öffnung | Tabu-Diff §0.3 leer, Ausgabe im Commit |
| **P9-67** | Jeder neue bzw. umgedrehte Wächter wird an einem eingebauten Verstoß rot | Gegenlauf-Tabelle §5 mit gemessenen Zahlen im Commit |
| **P9-68** | *(Nikinger-Schritt, nach dem Block)* `v3.1.0` live, `health_gate` grün, P9-43 gemessen | `health_gate.sh`-Ausgabe + Rebuild-Dauer im Phase-Head |

---

## §10 `[VERIFY]`

| ID | Frage | Stand |
|---|---|---|
| V173 | Steht außer den in §3 genannten Stellen irgendwo ein Eimer-Name oder ein Status-Anzeigewort fest im Code? | **Gemessen 2026-10-02:** `grep -rn -E '"(open\|done\|doing\|archived\|active)"' phase5_ui/webui/static/js` trifft nur `state.js:34` (`filter: "open"`). `grep -rn "Offen\|Erledigt\|In Arbeit"` trifft nur einen Kommentar (`list.js:385`) und **Archiv-Skripte** in `phase8_6_ui_polish/scripts/`, die nicht erneut laufen. Die alten Smokes (`d1_playwright_smoke.py`, `v3_ritt_playwright_smoke.py`) nehmen `.overview__space-count.first`, die Chip-Reihenfolge ändert sich für sie nur, wenn ein `doing`-Item existiert. `app.html`/`app.css` wurden für Status-Wörter geprüft: nur `#field-status` (`app.html:178`) und ein Kommentar (`app.css:342`), kein Eimer-Name, keine `data-bucket`-Regel. **Beim Bau wiederholen**, weil seit 97de3d6 Commits dazugekommen sein können: `grep -rn -E 'data-bucket\|"(open\|done\|doing\|note\|archived)"\|Offen\|Erledigt\|In Arbeit' phase5_ui/webui/static` |
| V174 | Muss `phase1_storage/CLAUDE.md` §Geerbte Contracts mitgezogen werden? | **Nein, solange P9-66 hält.** Prüfen per `git diff --stat HEAD~1..HEAD -- phase1_storage` → leer. Ist es nicht leer, Abbruch und Rückfrage |
| V175 | Port 18776 frei? | im Repo unbenutzt (grep 2026-10-02: 18765–18775, 18780 belegt). Zur Laufzeit `ss -ltn \| grep 18776` → leer, sonst nächsten freien nehmen und im Skript-Docstring nennen |
| V176 | Lassen sich die App-Fixtures in `phase9_hardening/tests/` benutzen? | **Gemessen 2026-10-02: nein.** Dort gibt es kein `conftest.py`, und es gibt kein Wurzel-`conftest.py`. `test_step_g_trash.py` testet nur den Store, die Route-Tests von Step G liegen in `phase5_ui/tests/test_api.py`. Deshalb stehen T3–T5 in `phase5_ui/tests/test_overview.py` (§5). **Erledigt** |
| V177 | `pytest`-Baseline am Bau-Tag | **Gemessen 2026-10-02: 1122 passed in 200,9 s** (bereinigtes Env), deckt sich mit dem Phase-Head. Am Bau-Tag neu messen. Erwartung nach dem Block: 1122 + 6 neue Tests (T1–T6), T7/T8 ändern nur Bestehendes |
| V178 | Ist `#field-status` im Vorschau-Modus bedienbar? | **Gemessen am Code:** `setEditorMode()` (`editor.js:254`) deaktiviert nur `[data-md]`-Knöpfe, nicht das Select. Das Select sitzt im zugeklappten `<details id="meta-panel">` (`app.html:168`), deshalb klappt S5 es explizit auf. Im Browser bestätigen |

---

## §11 Baseline dieser Planungssession

`main@97de3d6`, Arbeitsbaum sauber vor diesem Plan-Commit. `doc_health` **0 Befunde**. `pytest`
**1122 passed in 200,9 s** (ohne `SHAREFYX_*`/`SFX_*` im Env). Kein Code-Touch, kein Service-Touch.

---

## §12 Ergebnis (Block gebaut 2026-10-02, opencode/M3)

Gebaut in **einem** Commit, gegen `main@92a0cfa`. Doku, Tests, Browser-Beleg und dieses Ergebnis
gehören dazu (Hard Rule 8). Nach diesem Abschnitt wird die Datei **nicht mehr editiert** — sie ist
ab jetzt ein 📕-Snapshot. Jede Korrektur an ihr steht hier, datiert.

### 12.1 Abnahmematrix §9

| Zeile | Stand | Beleg (nicht nur „Test grün") |
|---|---|---|
| **P9-59** | ✅ | **T3** `test_doing_task_counts_in_doing_and_nowhere_else` — `counts == {"open":1,"doing":1,"done":1,"note":1,"archived":2}` als **Dict-Gleichheit**, `sum == item_count == 6`, und die **Mitgliedschaften** der fünf Eimer schließen sich paarweise aus und decken zusammen alle sechs Items. Browser **S3** (vor dem Schreibvorgang `1/1`) + **S6** (danach `0/2`) |
| **P9-60** | ✅ | **T4** `test_doing_counter_equals_doing_list` — `total == counts["doing"] == 1` **und** `items[0].title == "laufende Aufgabe"` (das konkrete Item, nicht nur die Zahl). **T8**: `seeded` hat jetzt ein `doing`-Item, deshalb läuft der Altbestand `test_counts_match_the_item_list_for_the_same_bucket` für diesen Eimer **nicht mehr vakuös** (0 == 0) — und `counts["open"] == 1` steht weiter, belegt das *Nicht*-Mitzählen in „Offen". Browser **S7** (`total == 2` nach dem Statuswechsel) |
| **P9-61** | ✅ | **T2** `test_every_status_value_lands_in_exactly_one_bucket` — **aus `STATUS_VALUES` generiert** (6 Kombinationen), `bucketFor()`s Bedingung in Python nachgebildet, plus die Umkehrung „jeder Eimer wird von mindestens einer Kombination erreicht". Gegenlauf **G1 → 7 rot**, **G3 → 2 rot** |
| **P9-62** | ✅ | **T1** (Reihenfolge aus dem **Quelltext** gelesen, plus Abgleich mit dem, was der Server ausliefert) + `test_meta.py:60` (`archived` zuletzt). Gegenlauf **G2 → 2 rot**. Browser **S2**: `data-bucket` im DOM in Reihenfolge `open, doing, done, note, archived` |
| **P9-63** | ✅ | **T6** `test_every_bucket_has_a_german_label` — Label-Menge == Eimer-Menge (der `BUCKET_LABELS[b] \|\| b`-Rückfall in `tree.js` ist sonst kein Fehler, er sieht nur aus wie ein Feature) und `labels["doing"] == "In Arbeit"`. Browser **S1** (Chip „1 In Arbeit") + **S2** (kein Label roh `doing`) + Screenshot `p9_doing_02_rail_fuenf_ordner.png`. Sichtprüfung qualitativ: nichts abgeschnitten, nichts überlappt |
| **P9-64** | ✅ | Browser **S5/S6**: Statuswechsel `open → doing` im Editor, Toast „Gespeichert · v2“, danach **ohne Reload** `offen 1 → 0` und `in Arbeit 1 → 2`. Screenshot `p9_doing_04_nach_statuswechsel.png`. Gegenlauf: **rot**, weil es den Ordner gar nicht gibt |
| **P9-65** | ✅ | **T5** `test_ui_shaped_patch_keeps_doing_and_assignee` — PATCH mit **exakt** `editor.js :: saveItem()`s Feldsatz (`version, format, title, body, status, due, tags, links`, **ohne** `assignee`; am `currentFormValues()`/`saveItem()`-Quelltext verifiziert), danach `status == "doing"` und `assignee == "niklas"` über **drei** Lesepfade (API-Antwort, `GET`, `store.search`). Bestehend `phase2_mcp/tests/test_tools.py:1047` für die MCP-Seite. Browser **S8**: `status == "doing"`, `assignee == "alpha"`. Gegenlauf **G5 → rot** (wenn der Body `assignee` mitschickt) |
| **P9-66** | ✅ | `git diff --stat -- phase1_storage phase2_mcp/mcpserver phase4_auth/authserver phase6_shares phase7_spaces_admin` → **leer**, im Commit ausgegeben. Damit V174 beantwortet: `phase1_storage/CLAUDE.md` §Geerbte Contracts musste **nicht** mitgezogen werden, und es ist keine zehnte Contract-Öffnung entstanden |
| **P9-67** | ✅ | Alle fünf Verstöße einzeln eingebaut, G0 als Kontrolllauf: **G0 0 · G1 7 · G2 2 · G3 2 · G4 1 · G5 1** (§12.2) |
| **P9-68** | ⬜ | **Nikinger-Schritt.** Deploy `v3.1.0` + `health_gate.sh` + P9-43, Ablauf §8 |

**Bilanz: 8 ✅ · 0 ⚠️ · 1 ⬜** (P9-68 hängt per Konstruktion am Deploy, der nicht Teil des
Blocks ist).

### 12.2 Gegenlauf §5 — gemessene Zahlen

Kontrolllauf **G0 (Bau-Stand) = 0 rot** steht in derselben Tabelle als Zeile, weil ein
Gegenlauf ohne Kontrolllauf nicht zeigt, ob die Testauswahl selbst schuld war.

| Verstoß | rot | welche Wächter |
|---|---|---|
| G0 Bau-Stand (Kontrolle) | **0** | — |
| G1 `"doing"`-Eintrag aus `_BUCKETS` entfernt | **7** | T1, T2, T3, T4, T6, T7, T8 |
| G2 `"archived"` **vor** `"doing"` | **2** | T1, `test_meta.py:60` |
| G3 `_BUCKETS["doing"]["status"] = "open"` (Duplikat) | **2** | T2, **T3 — erst nach dem Nachschnitt unten** |
| G4 `doing: "In Arbeit"` aus `BUCKET_LABELS` entfernt | **1** | T6 |
| G5 im T5-PATCH-Body `"assignee": ""` | **1** | T5 |

**Browser-Gegenlauf: 7 von 11 Stationen rot** (nur D1+D2 per
`git stash push -- phase5_ui/webui/api.py phase5_ui/webui/static/js/state.js` zurückgenommen,
frisch gesätet, `git stash pop` danach). Rot: S1, S2 (2 Prüfungen), S3, S4 (2), S6. **Grün
bleiben S5, S7, S8** — siehe den Befund in §12.4.

### 12.3 Abweichung vom Plan (eine, mit Begründung)

**§5 T3/T4 sind schärfer geschnitten als beschrieben.** Der Plan sagte, G3 mache **T2, T3 und T4**
rot. Gemessen: **nur T2**. Grund: der `seeded`-Datensatz hat je **eine** offene und **eine**
laufende Aufgabe, also stehen „die Zahl der Aufgaben mit Status `open`" und „die Zahl der
Aufgaben mit Status `doing`" beide auf 1 — und ein Duplikat-Filter ändert daran nichts. T3 und T4
prüften **Zahlen**, und die Duplikat-Eigenschaft ist keine Zahl, sondern eine **Mitgliedschaft**.

Der Plan hat dafür eine eigene Regel (§5, letzter Absatz): *„Wird ein Verstoß nicht rot, ist der
zugehörige Wächter wertlos und muss neu geschnitten werden. Das ist dann ein Befund, nicht
stillschweigend weiterbauen."* Also neu geschnitten: **T3 holt jetzt die Item-Mengen** der fünf
Eimer (fünf Listenabfragen) und beweist paarweise Disjunktheit + Vollständigkeit. Damit ist
„zählt in „In Arbeit" und in **keinem** anderen Eimer" (P9-59) **behavioural** bewiesen statt
behauptet, und G3 ist rot.

**T4 bleibt unter G3 grün — und das ist richtig, nicht ein Loch.** T4 trägt P9-60 („Zähler == Liste
für „In Arbeit“"), und unter G3 gilt Zähler == Liste. Die Duplikat-Eigenschaft tragen T2 (statisch,
über die Gesamtregel) und T3 (behavioural, über die Mitgliedschaft).

### 12.4 Befunde, die der Block erbracht hat

**B1 — das Loch war rein navigativ, und der Gegenlauf beweist es.** Im Browser-Gegenlauf bleiben
**S5, S7 und S8 grün**: der Statuswechsel auf `doing` ließ sich **schon ohne diesen Block**
speichern, `/overview` und `/items` lieferten `doing` roh, und `assignee` überlebte den
Editor-Pfad. P9-W stand als Behauptung im Plan; hier ist es ein Messlauf. Konsequenz für P10: die
Hervorhebung von „In Arbeit“ braucht **keine** Arbeit an der Maschinenebene.

**B2 — dieselbe Repo-Lehre zum sechsten Mal, diesmal im eigenen Prüfskript.** Der erste
Browser-Gegenlauf **stürzte ab**, statt rot zu melden: ein `click()` auf den Ordner „In Arbeit",
den es ohne den Fix nicht gibt, ist ein 30-Sekunden-Timeout, kein Befund — und ein Skript, das
beim Beweis seines eigenen Lochs stirbt, beweist nichts. Nachgebessert: S4/S5/S8 prüfen jetzt
zuerst auf Existenz und melden sich mit Begründung rot. Danach beide Läufe neu gefahren
(grün 11/11 mit dem gehärteten Skript, rot 7/11 im Gegenlauf).

**B3 — §1 dieses Plans ist an einer Stelle falsch, und der Fehler war die Überschreitung.**
§1 behauptet, `phase9_hardening/CLAUDE.md` sei **42.393 B** und damit über dem Softcap. Gemessen
am Bau-Tag: **`git show HEAD:phase9_hardening/CLAUDE.md | wc -c` = 35.794 B**, also knapp *unter*
dem Softcap, und `doc_health` meldete zu Recht **0** Befunde. Die 42.393 B waren ein **Zustand vor
der siebzehnten Rotation**; §1 hat sie nach der Rotation weitergetragen. Die Überschreitung ist
trotzdem entstanden — aber erst durch den **zehnten Block** (Rotationsbilanz 44.508 B → 41.192 B,
232 B über), nicht vorher. Sie ist jetzt im INDEX benannt (P8-P), wie es die Konvention verlangt.

**B4 — K5, eine kleine Abweichung von §4 D1.** §4 verlangte, die Zeilen `api.py:115–127`
**wörtlich** stehen zu lassen. Zwei davon tragen aber eine **Anzahl** („Die **drei** Ordner des
Navigationsbaums", „**Vier** Ordner statt drei schließen das Loch") — die wäre nach dem fünften
Eintrag eine Lüge gewesen, und ein Kommentar, der das Gegenteil des Codes behauptet, ist schlechter
als keiner (dieselbe Regel, an der T7 festhing). **Nur die Zahlen korrigiert, alle
Begründungen wörtlich.**

### 12.5 Selbstprüfung §0.4

| Schritt | Ergebnis |
|---|---|
| `pytest -q` | **1128 passed in 202,4 s** (Baseline 1122 = V177, **+6** neu: T1, T2, T6, T3, T4, T5; T7 umbenannt, T8 an Bestehendem) |
| `ui_budget.py` | **5/5** im Korridor, `app.js + app.css + Font (gzip)` **153,2 KB** (153,0 KB vorher) |
| `node --check state.js` | ✅ (und alle 13 übrigen JS-Dateien mitgeprüft) |
| Tabu-Diff §0.3 | **leer** |
| `doc_health.py` | **0 Befunde** (nach dem Bau; **1** während, der Head lag 232 B über dem Softcap — INDEX-Zeile entsprechend benannt, s. B3) |
| Service-Touch | **kein** `systemctl`, **kein** `pkill -f`, **kein** Deploy. Wegwerf-Instanz nur über `p9_doing_wegwerf.py stop` (PID-Datei) gestoppt |
| Env | `env \| grep -E '^(SHAREFYX_\|SFX_)'` **leer** |

### 12.6 Screenshots

`docs/screenshots/p9_doing_{01_uebersicht_chip, 02_rail_fuenf_ordner, 03_liste_in_arbeit,
04_nach_statuswechsel}.png` (1440×900, 56/42/42/60 KB). **Keiner** zeigt den Login-QR oder die
`credentials.json` (Hard Rule 1: Passwort und TOTP-Seed werden zur Laufzeit unter
`/tmp/opencode/p9-doing-wegwerf/` mit `0600` erzeugt und nichts davon ist committet).
`screenshots_latest/` auf `p9_doing_*` umgehängt.

Qualitative Sichtprüfung mit dem lokalen Vision-Modell: Rail zeigt `Offen, In Arbeit, Erledigt,
Notizen, Archiv` + „+ Ordner“, **nichts abgeschnitten, nichts überlappt**; Bild 04 zeigt
`Offen 0` / `In Arbeit 2`, deckungsgleich mit S6. **Gezählt wurde nicht** (dokumentierte
VLM-Schwachstelle, `docs/concepts/sichtpruefung_automation_tooling.md`) — **gezählt haben die
Stationen**, aus dem echten DOM.
