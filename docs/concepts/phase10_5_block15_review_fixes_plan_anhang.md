---
status: archive
purpose: L3-Anhang zum Plan Block 15 (Review-Fixes B1–B10) — die Anmerkungen der abgeschlossenen Schritte 15.1–15.3b, verbatim aus dem Plan verschoben, weil der Plan am Softcap stand.
read-when: wenn zu B1/B15, B2/B3/B20, B5/B8 oder E5 die Mess- und Baunotizen gebraucht werden — der Plan trägt §0–§5 und die Anmerkungen ab 15.4
detail: L3
up: ../../ROADMAP.md
down:
  - phase10_5_block15_review_fixes_plan.md   # 📗 der Plan (Befund-Stand, Schritte, Abnahme)
  - ../../phase10_5_finishing/CLAUDE.md       # der Phase-Head (Modulstatus Block 15)
updated: 2026-10-31 (Schritt 15.6: die Anmerkungen 15.1–15.3b hierher verschoben — der Plan stand bei 39.905 B)
---
# Anhang zum Plan Block 15 — Anmerkungen 15.1–15.3b

> **Warum dieses Archiv existiert (2026-10-31, Schritt 15.6).** Der Plan stand bei 39.905 B, 1.055 B
> unter dem Softcap; die Anmerkungen zu 15.6 passten nicht mehr hinein. Verschoben per
> `scripts/move_sections.py` — im Plan bleibt je Überschrift eine Zeigerzeile.

## Anmerkungen 15.1 — B1 (2026-10-30, Claude Code)

- **Reichweite, am Code gelesen (korrigiert nach dem Advisor-Hinweis):** über **MCP** ist B1 ein reiner
  **Lese**-Befund (`get_item_asset`) — **kein** MCP-Werkzeug ruft `delete_asset` auf; das **Verschieben**
  ist nur über den Store/CLI erreichbar, über REST nur als Wildcard (`*`), weil die Route kein `/`
  trägt. Kritisch bleibt es: die Auth-DB-Dateien und fremde Items sind lesbar.
- **Am Code bestätigt:** `get_asset`/`delete_asset` bauten `target_dir.glob(f"{asset_id}.*")`;
  `ASSET_ID_RE` wurde nur in `files.asset_path()` (Upload) und `list_assets()` angewandt. Die
  MCP-Zweige ohne Schreibrecht filtern über `list_assets()` — dort ging die ID nie in einen Pfad.
- **Warum der Fix im Store sitzt, nicht in Tool und Route:** MCP und REST rufen beide
  `store.get_asset`/`delete_asset`; eine Prüfung im Kern deckt beide **und** `space_cli`, eine im
  Adapter nur den einen. Die Route kann nach Starlettes Dekodierung kein `/` tragen, aber `*` —
  das war B15.
- **Warum „nicht gefunden" statt `ValidationError`:** die Adapter bilden `ItemNotFound` aus
  `get_asset` schon auf `asset_not_found`/404 ab. Eine formfalsche ID unterscheidbar zu machen von
  einer unbekannten hätte einen neuen Fehlerpfad **und** ein Orakel gebraucht, ohne einem
  ehrlichen Client zu helfen.
- **`$` → `\Z`:** `re.match(r"^ast_[0-9a-f]{8}$", "ast_01234567\n")` trifft — der Zeilenumbruch
  ginge in Glob und Dateinamen. `ITEM_ID_RE` hat dieselbe Form (`$`); dort erreicht eine ID den
  Pfad erst **nach** dem Index-Lookup, deshalb nicht Teil von B1 — als Härtung in 15.5 mitnehmen.
- **Gegenlauf (Fix per `git stash` entfernt):** 9 Wächter rot — Store ×6 (`../../../bob/.share`,
  `*`, `ast_*` je get/delete), MCP ×1 (Traversal liest fremdes Item), Store direkt ×1 (verschiebt fremde
  `.share.yml`), REST ×1 (`*` ⇒ 200 statt 404). Die übrigen Formen (`ast_0123456?`, leerer
  String, Traversal auf eine nicht existierende Datei) laufen **auch ohne Fix** durch, weil dort
  schlicht nichts passt — sie sind Regressionsschutz, kein Beweis; der Beweis sind die neun.


## Anmerkungen 15.2 — B2/B3/B20 (2026-10-30, Opus)

- **Am Code reproduziert (tmp-`DATA_ROOT`), alle drei:** B2 `rename_folder("alice", "projekte",
  "archiv/projekte")` ⇒ `FileNotFoundError`, Marker bleibt, `Store()` wirft erneut · B3
  `alice/README.md` ⇒ `rebuild_index()` wirft `FrontmatterError`, **0** Zeilen im Index, frischer
  Start wirft · B20 `parse("---\r\n…")` ⇒ `FrontmatterError`.
- **Fund (nicht im Review): `links: [itm_x, itm_x]`** von Hand riss den Primärschlüssel von
  `item_links` (`IntegrityError`) — derselbe Startblocker wie B3. Fix an der einen Stelle, die
  Kanten schreibt (`index._replace_links_no_commit()`: Paare dedupliziert).
- **Fund: `yaml.YAMLError` ist kein `ValueError`.** Kaputtes YAML lief an jedem `except ValueError`
  im Kern vorbei — auch an dem in `_rewrite_space_frontmatter`. `parse()` übersetzt jetzt in
  `FrontmatterError`; damit greift jeder bestehende Fänger.
- **Fund: ein Wächter lief nie.** `test_rename_resumes_after_crash` stand **zweimal** in
  `phase1_storage/tests/test_store.py` (Ordner Z. 1385, Space Z. 1535) — die zweite Definition
  verdeckte die erste, der Ordner-Wiederaufnahme-Test war seit Block 9 nie gelaufen. Umbenannt in
  `test_rename_folder_resumes_after_crash`, gegen den **unveränderten** Code grün (kein versteckter
  Fehler). AST-Suche über alle Testdateien: **keine** weitere Doppelung.
- **B3, Bauform:** je Datei ein `SAVEPOINT` (keine halbe Zeile: Item ohne Kanten), der ganze
  Neuaufbau **eine** Transaktion (vorher committete `replace_item_links()` das `DELETE` beim ersten
  Item). **Datei-Fehler** (`OSError`, `ValueError`, `KeyError`, `TypeError`, `sqlite3.ProgrammingError`
  /`InterfaceError`/`IntegrityError` — gemessen: `title: [a]` wirft `ProgrammingError`, eine
  `DatabaseError`-Unterklasse) kosten die Datei, `CRITICAL` mit Pfad; **Umgebungs-Fehler**
  (`OperationalError`) rollen zurück, der alte Index steht vollständig. `IndexStats` bleibt
  unverändert (P1-Contract) — die Zahl der übersprungenen Dateien steht im Log.
- **B2, Bauform:** Elternordner wird angelegt (wie `files.move_file()` es für Dateien tut; die Option
  „`ValidationError`" hätte einen legitimen Klick verboten). Scheitert der Rename, **bevor** etwas
  wanderte (am **Plattenstand** entschieden: `alt` steht, `neu` fehlt), wird der Marker gelöscht —
  sonst führte der nächste Start einen Rename aus, den der Aufrufer als Fehler sah. Die
  Wiederaufnahme fängt jeden Fehler: `CRITICAL`, Marker bleibt, Index aus der Platte neu, Start geht
  weiter. **Neu dadurch (Advisor):** ein liegender Marker bei laufendem Dienst — deshalb lehnen
  `rename_folder`/`rename_space` mit `ValidationError` ab, solange er liegt (sonst überschriebe der
  nächste Rename die einzige Spur). Rest: ein so angelegter, danach leerer Elternordner bleibt liegen
  (unsichtbar, Ordner leiten sich aus Items ab).
- **B20, Bauform:** die drei Begrenzer akzeptieren `\r?\n`; `parse()` gibt dieselbe Form zurück
  (P1-Contract). Ein Update schreibt das Frontmatter mit `\n`, der Body behält `\r\n` — **gemischte
  Zeilenenden** nach dem ersten Schreiben, Datei bleibt lesbar (Wächter `test_crlf_item_survives_update`).
  Ein UTF-8-BOM ist **nicht** abgedeckt (eigene Fehlerklasse, kostet jetzt nur die Datei).
- **Gegenlauf, je Quelldatei einzeln** (Advisor: sonst verdeckt B3 den B20-Fix und die
  Wiederaufnahme den Elternordner-Fix): ohne `frontmatter.py` **6 rot**, ohne `index.py` **5 rot**,
  ohne `store.py` **5 rot** — jede Datei hat eigene rote Wächter, keiner verdeckt einen anderen.


## Anmerkungen 15.3 — B5/B8 (2026-10-30, Opus)

- **Am Code reproduziert (tmp-`DATA_ROOT`), acht Hand-Edit-Fälle, Neuaufbau ehrlich erzwungen**
  (ein zweiter `Store()` auf demselben Index baut **nicht** neu — der erste Probelauf war dadurch
  wertlos, Advisor-Fund): `tags: [2026]` ⇒ Textsuche `TypeError` · `title: 2026` ⇒ Update
  `AttributeError` · `title: [a, b]` und `title:` ⇒ nach `rebuild_index()` **unsichtbar** (15.2
  überspringt sie) · `tags: abc` ⇒ drei Tags · `tags: [[x]]` ⇒ Suche `TypeError` · **Fund:**
  `links: [1]` ⇒ `get()` und Update `TypeError` (`ITEM_REF_RE` auf `int`). REST: `body:5` schrieb
  Datei und Index, warf danach.
- **Zwei Funktionen, nie eine** (Advisor): **Lesen ist nachsichtig** —
  `frontmatter.normalize_item_fields()` macht `title` zum String und `tags`/`links` zu
  String-Listen, aufgerufen von **beiden** Lesepfaden (`store._item_from_text()`,
  `index.row_from_file()`), damit Index und `get()` nie auseinanderlaufen. **Schreiben ist streng**
  — `store._check_write_types()` in `create()`/`update()` (`title`/`body` String, `tags`/`links`/
  `share_*` String-Liste) plus `type`/`status` in `_check_type_and_status()`; REST bildet die
  `ValidationError` schon auf 422 ab. Teilten beide eine Funktion, würde `tags: [1, 2]` über REST
  still zu `["1", "2"]` statt 422.
- **Koerzion = „wie es im YAML stand"** (`frontmatter.inline_text()`): `2026` → `"2026"`, `true` →
  `"true"` (nicht `True`), `[a, b]` → `"[a, b]"` (nicht `['a', 'b']`). Ein Skalar in `tags`/`links`
  wird **ein** Eintrag (`tags: abc` → `["abc"]`), `~` fällt weg. `parse()` bleibt roh —
  `_write_version_only` schreibt zurück, was der Mensch schrieb.
- **Folge (wie gemischte Zeilenenden in 15.2):** erst der nächste echte Write normalisiert die Datei
  — aus `tags: [2026]` wird `tags: ['2026']`, aus `title: 2026` wird `title: '2026'`.
- **Kein Fehler nach dem Write** (B8, strukturell): `_write_item_file()` rechnet Text und Kanten
  (`_link_rows()`, vorher `_replace_links_for_item()`) **vor** `atomic_write`. Wächter erzwingt
  einen Wurf in der Link-Extraktion: Datei, Version, Git-Historie unverändert.
- **REST:** nur, was **vor** dem Kern gebraucht wird — `visibility` String, `share_read`/
  `share_write` String-Liste (das Re-Auth-Gate baut daraus einen `ShareState`; `frozenset(5)` war
  500). `files.validate_folder()` lehnt Nicht-Strings mit `ValidationError` ab (vorher
  `AttributeError` im PATCH). Der Rest prüft der Kern.
- **Bewusst nicht gemacht — Befund für den Nikinger:** `share_read: fabian` (Hand-Edit, ohne
  Liste) wird heute zu `frozenset("fabian")` = Freigabe an die Spaces `f`, `a`, `b`, … — zufällig
  **fail-closed** (Fabian sieht nichts). Dieselbe Koerzion wie bei `tags` machte daraus eine echte
  Freigabe an `fabian` **ohne Re-Auth**. Rechteerweiterung ist keine Typfrage → in 15.3 unverändert
  gelassen. **[Korrektur, gleicher Tag]:** „unverändert" stimmte nur für den Zugriff — der erste
  gewöhnliche Write schreibt die Buchstabenliste auf die Platte (am Code bestätigt). Entschieden
  als **E5 = A**, gebaut in 15.3b.
- **15.2-Wächter umgezielt:** `test_rebuild_skips_a_title_sqlite_cannot_bind` prüfte, dass
  `title: [a, b]` die Datei kostet — genau das ändert 15.3. Jetzt
  `test_rebuild_skips_a_value_sqlite_cannot_bind` mit `status: [a, b]` (der `ProgrammingError`-Zweig
  bleibt bezeugt).
- **Gegenlauf je Fix, im Code neutralisiert** (ein `git stash` von `frontmatter.py` bräche nur den
  Import — alles rot, nichts bewiesen): Normalisierung aus **8 rot** · nur Index ohne **3** · nur
  Store-Lesen ohne **7** · Schreib-Typprüfung aus **21** · Links nach dem Write **1** ·
  `validate_folder` ohne Typprüfung **2** · REST-Frühprüfung aus **3**. Jeder Fix hat eigene rote
  Wächter.


## Anmerkungen 15.3b — E5 (2026-10-30, Opus)

- **Am Code nachvollzogen, vor dem Fix:** `normalize_item_fields()` liess `share_read`/`share_write`
  roh durch; `_item_from_text()` machte daraus `list("fabian")`, `row_from_file()` schrieb
  `json.dumps("fabian")` = `'"fabian"'` in den Index, `acl_of()` las `frozenset("fabian")` — sechs
  Ein-Buchstaben-Freigaben auf **beiden** Lesepfaden.
- **Bauform:** `share_read`/`share_write` laufen durch dasselbe `_text_list()` wie `tags`/`links`
  (Skalar = ein Eintrag, `~`/leer = keine Freigabe, Elemente wie im YAML). Neu:
  `normalize_item_fields(fields, *, source=None)` — `source` steht **nur** in der Warnung;
  `index.row_from_file()` und `store._item_from_text()` (beide Aufrufer: `_row_to_item`, die
  Space-Umbenennung) reichen den Pfad. `WARNING` nur beim **Skalar** (die Rechteerweiterung), nicht
  bei der Listenform und nicht bei leerem Feld. Logger `storage.frontmatter`.
- **Warum `WARNING` bei jedem Lesen, nicht einmal:** die Warnung hört von selbst auf, sobald der
  nächste Write die Datei in Listenform bringt (`share_read:\n- fabian`) — ein „schon gemeldet“-
  Zustand wäre neuer Zustand im dummen Server, für einen Fall, den es nur per Hand-Edit gibt.
- **Übergang beim Deploy (am Code gelesen, nicht gemessen):** `acl_of()` liest **nur den Index**
  und gleicht nicht ab; der Dienststart baut den Index nur bei Schema-Sprung neu, und 15.3b
  ändert `INDEX_SCHEMA_VERSION` nicht. Eine **vor** Deploy D geschriebene Indexzeile mit
  `'"fabian"'` gibt deshalb weiter die Buchstaben (fail-closed), während `get()` schon
  `["fabian"]` zeigt — bis die Datei sich ändert (Abgleich in `_reconcile_and_get_row`) oder
  `rebuild_index()` läuft. **Folge für die Durchsicht vor Deploy D:** ein Treffer wird am besten
  **vor** dem Deploy von Hand in Listenform gebracht — dann gibt es keine Koerzion und keinen
  Übergang.
- **Wächter (5 neu + 1 umgezielt):** `test_store.py` — `share_read`/`share_write` je: Hand-Edit Skalar ⇒ `WARNING`
  mit Pfad und Feldname, `acl_of()` = `{fabian}`, `get()` = `["fabian"]`, Update schreibt
  `- fabian`, `acl_of()` danach unverändert; Listenform / leer / `~` ⇒ keine Warnung (3, reiner
  Regressionsschutz — laufen auch ohne Fix grün). `test_frontmatter.py` — der alte Wächter
  „`share_*` bleibt roh“ ist **umgezielt** auf die neue Regel (exakter Warnungstext, Eingabe
  unverändert).
- **Gegenlauf, im Code neutralisiert** (wie 15.3): `share_*` aus der Schleife ⇒ **3 rot** (beide
  Store-Wächter + Frontmatter) · Warnung stummgeschaltet, Koerzion bleibt ⇒ **3 rot** · Pfad im
  Index-Lesepfad nicht gereicht ⇒ **2 rot** (Warnung beim Neuaufbau) · Pfad in `_row_to_item` nicht
  gereicht ⇒ **2 rot** (Warnung bei `get()` — der Weg, auf dem sie im Betrieb fällt, Advisor-Fund).
- **Sichtbarkeit im Betrieb, am Code gelesen:** `SPACE_LOG_LEVEL=INFO` (Unit `sharefyx-mcp.service`),
  `configure_logging()` setzt den Root-Logger darauf — ein `WARNING` erreicht das Journal.
  `deploy.sh` und die Unit rufen kein `rebuild_index()` (gegrept) — der Übergang oben gilt.
  **Folge (kein Blocker):** `search()` liest jede Datei, ein unbehobener Skalar warnt also bei jeder
  Suche und jedem `/overview`-Poll — gewollt laut E5, und gegenstandslos, wenn Treffer vor dem Deploy
  von Hand behoben werden.
- **Durchsicht vor Deploy D — der Befehl (Nikinger, read-only, nicht aus dieser Session gefahren):**
  `grep -rnE --include='*.md' --exclude-dir='.*' '^share_(read|write):[[:space:]]*[^[:space:][~#]' /home/savefyx/savefyx-data`
  Trifft jeden Skalar (ohne oder mit Anführungszeichen), nicht die Listenform `[…]`, nicht die
  Blockliste (`share_read:` + `- x`-Zeilen), nicht leer, nicht `~`, nicht `._trash/`. **Harmloser
  Fehltreffer:** `share_read: null` (liest sich als keine Freigabe). Jeder echte Treffer: von Hand
  auf `[name]` umschreiben, **vor** dem Deploy.
