---
status: live
purpose: Phase-Head Storage-Kern — Scope, harte Regeln, gelockte Entscheidungen, Modulstatus, aktueller Session-Handover
read-when: Arbeiten in phase1_storage/ — zuerst lesen, zusammen mit dem neuesten Session-stopped-Block
detail: L2
up: ../CLAUDE.md
down:
  - ../docs/concepts/phase1_storage_plan.md   # voller Plan, Entscheidungen A–H, Steps 0–7
  - SESSIONS_ARCHIVE.md                       # ältere Session-Blöcke
updated: 2026-08-23 (Phase 7 Step 0: sechste Contract-Oeffnung angekuendigt -- acl.py-Schreibseite, Extraktion aus spacectl.py, P7-M-Lock-Regel) | 2026-08-20 (Phase 6.5 Step B1: fuenfte Contract-Oeffnung gebaut -- Bild-Assets in models/files/store.py, 150 Tests nach drei Advisor-Fixes (Lock-Disziplin, created-Konsistenz, Sniff-Kosten), Zaehlkorrektur 126->130 vor Step B1)
---
# CLAUDE.md — Phase 1: Storage-Kern (`phase1_storage/`)

> Das Fundament: Dateien + Index + Versionierung. **Kein Netz, kein MCP, keine Auth.**
> **Quelle der Wahrheit ist der Code, nicht dieses Dokument.**
> Vollständiges Design + alle 8 gelockten Entscheidungen + Steps 0–7:
> `../docs/concepts/phase1_storage_plan.md`.

## Mission (zuerst lesen)

Phase 1 heißt „Storage", aber das Ziel ist **Koexistenz**: ein Mensch im Texteditor und
mehrere Claude-Instanzen schreiben gleichzeitig in dieselben Dateien, ohne dass jemand still
Daten verliert. „Ein paar Markdown-Dateien lesen und schreiben" ist **nicht** die Aufgabe. Der
harte Pfad ist der **Konfliktfall** — und der ist nur ohne Transportschicht sauber beweisbar,
deshalb enthält P1 kein Netzwerk.

## Bauprinzip (Projekt-Kernprinzip)

„Der Server ist dumm." **Phase 1 enthält KEINE AI** — kein LLM, keine Embeddings, keine
semantische Suche, kein Auto-Tagging. Alles ist deterministischer Code: Parsen, Schreiben,
Indizieren, Vergleichen, Sortieren. Wer hier ein Modell „verstehen/zusammenfassen/verschlagworten"
lassen will → **stop**, das gehört auf die Client-Seite.

## Scope

- **DRIN:** Frontmatter-Modelle mit Round-Trip-Treue, atomarer Datei-Store, SQLite-Index +
  Rebuild, optimistic Locking + Konflikterkennung, Drift-Erkennung bei externen Edits,
  Git-Commit je Write, Query-Layer (nur Frontmatter + Snippet), CLI als Beweis.
- **DRAUSSEN:** MCP, HTTP, Auth, Tunnel, UI, Volltextsuche über Bodies, Anhänge, Löschen,
  Cross-Space-Rechte (die Store-API kennt Spaces, aber keine Autorisierung — das ist P2).

## Build-Reihenfolge (verbindlich)

Skelett → Modelle/Roundtrip → Datei-Store → Index/Rebuild → **Versionierung/Konflikt** →
Git-Historie → Query-Layer → CLI. Unter Zeit-/Token-Druck fällt die CLI weg, **nie** die
Konfliktbehandlung. Step 4 ist der eigentliche Beweis der Phase; ohne seine vier Tests ist
P1 nicht abgeschlossen, egal wie viel Code existiert.

## Harte Regeln (nicht verhandelbar)

- **Dateien sind die Wahrheit.** Der SQLite-Index darf jederzeit gelöscht und rekonstruiert
  werden. Ein Index-Fehler fasst **nie** eine Datei an.
- **Kein Write ohne `version`.** Mismatch → `ConflictError` mit aktuellem Item im Fehler.
  Kein Last-Write-Wins, nirgends, auch nicht „vorläufig für den Test".
- **Atomar oder gar nicht.** tmp + `os.replace` + Verzeichnis-`fsync`. Nie eine halb
  geschriebene Zieldatei.
- **Round-Trip-Treue ist Pflicht.** Unbekannte Frontmatter-Felder, Umlaute und Body-Formatierung
  überleben jeden Schreibvorgang byte-identisch, wo sie nicht geändert wurden. Verliert die
  gewählte Bibliothek Felder → Bibliothek tauschen, nicht Regel lockern.
- **`now_fn` injiziert**, kein `datetime.now()` im Modulcode. Tests deterministisch, ohne echtes
  Dateisystem-Timing.
- **Kein Delete im Kern-API.** `status: archived` + `_archive/`. Hard Delete nur als separates,
  bestätigungspflichtiges Operator-Skript.
- Logging → **stderr**; stdout nur maschinenlesbares JSON. Atomic commits. Kein Subtask „done"
  ohne grünes `pytest` (gemockt, **kein Netz**).
- **Commit ⇒ Note-Update (zwingend, auch auf direkte Anweisung).** Jeder Step-Abschluss-Commit
  aktualisiert im **selben** Commit die Modul-Tabelle unten **und** den `## Session stopped`-Block.
- **Rotationsregel ab Tag 1.** Dieser Head trägt **genau einen** Session-Block. Beim Anlegen
  eines neuen wandert der bisherige **verbatim** nach `SESSIONS_ARCHIVE.md`, newest-first —
  Durchführung über `scripts/rotate_session_block.sh phase1_storage`, nie von Hand. Niemals
  abtippen.

## Die 8 Entscheidungen (A–H) — Kurzform (Details: Plan §0)

- **A** Datei = Wahrheit, SQLite = Ableitung, jederzeit rekonstruierbar.
- **B** Genau ein Item-Typ; `type: note|task` ist ein Feld, keine zweite Tabelle.
- **C** Optimistic Locking über `version:int`; `ConflictError` trägt das aktuelle Item.
- **D** Externe Edits über `(mtime, size, sha256)` erkennen; Datei gewinnt, `version` +1.
- **E** Atomarer Write + Git-Commit je Write; Git-Fehler best-effort, `logger.critical`, nie fatal.
- **F** `itm_<8hex>` unveränderlich, im Frontmatter **und** als Dateinamen-Präfix; Lookup nie über Dateinamen.
- **G** `rebuild_index()` öffentlich + beim Start; korrupter Index → Rebuild statt Crash.
- **H** Kein Delete im API; `archived` + `_archive/`; Hard Delete nur als Operator-Skript.

## Modul-Status

| # | Modul | Step | Status | Tests |
|---|---|---|---|---|
| 1 | Repo-Skelett, `pyproject.toml`, dev_install | 0 | ✅ | 0 |
| 2 | `models.py`, `frontmatter.py` | 1 | ✅ | 9 |
| 3 | `files.py` (atomarer Write, IDs, Slugs) | 2 | ✅ | 10 |
| 4 | `index.py` (SQLite, Rebuild) | 3 | ✅ | 9 |
| 5 | `store.py` (API, Lock, Versionierung) | 4 | ✅ | 26 |
| 6 | `history.py` (Git) | 5 | ✅ | 11 |
| 7 | Query-Layer in `store.py` | 6 | ✅ | 2 (in `test_store.py`) |
| 8 | `scripts/space_cli.py` | 7 | ✅ | 9 |
| 9 | `patch.py` (neu) + `store.py :: patch()` | P6 Step 1 | ✅ | 5 (in `test_store.py`; die vier reinen `apply_edits()`-Funktionstests liegen in `phase6_shares/tests/test_patch.py`, außerhalb dieses Pakets) |
| 10 | `acl.py` (neu) + `folder`/`visibility`/`share_read`/`share_write` in `models.py`/`store.py`/`index.py`/`files.py` — `Store.acl_of()`, `list_spaces()` verzeichnisbasiert, `index.connect()` liefert `(conn, rebuilt)` | P6 Step 4 | ✅ | 36 (1 `test_models.py` + 11 `test_files.py` + 4 `test_index.py` + 20 `test_store.py`) + 10 `phase6_shares/tests/test_acl.py` (außerhalb dieses Pakets) |
| 11 | `store.py :: move()` (neu) + `_cleanup_emptied_folders()` (intern, P6-AF) — Space-/Ordner-Move additiv zu `update()`/`archive()`, `space` bleibt in `_SYSTEM_MANAGED_FIELDS` | P6 Step 7b, Commit 1/3 | ✅ | 6 (in `test_store.py`) |
| 12 | `store.py :: search()` bekommt `in_body: bool = False` (P6.5-N4) — additiv zum bestehenden Contract, keine benannte Öffnung wie #9/#10/#11 (kein neues Modul, kein neuer Store-Aufruf, nur ein optionales Keyword an einer bereits kontraktierten Signatur) | Phase 6.5 Step A4 | ✅ | 3 (in `test_store.py`) |
| 13 | Fünfte, benannte Contract-Öffnung (angekündigt Step 0, siehe „Geerbte Contracts"): `AssetInfo` (neu, `models.py`), `files.py` (`new_asset_id()`, `ITEM_ID_RE`/`ASSET_ID_RE`, `ASSET_MIME_TYPES`/`sniff_image_mime()`, `asset_dir()`/`asset_path()`, `move_asset_dir()`, `atomic_write_bytes()`), `store.py` (`put_asset()`/`list_assets()`/`get_asset()`/`delete_asset()`, `move()` zieht das Asset-Verzeichnis mit — ein Move bleibt ein Commit) | Phase 6.5 Step B1 | ✅ | 20 (12 `test_files.py` + 8 `test_store.py`) |
| 14 | Sechste, benannte Contract-Öffnung (angekündigt P7 Step 0, siehe „Geerbte Contracts"): `acl.py` bekommt eine Schreibseite — `read_share_file()`/`write_share_file()`/`add_member()`/`remove_member()`/`create_space()`/`remove_space_dir()`/`spaces_referencing()`/`AclWriteError` — byte-identische Extraktion aus `spacectl.py` (P7-P), kein neues Verhalten | P7 Step C1 | ✅ **gebaut, Phase noch nicht abgeschlossen** (siehe „Geerbte Contracts" unten) | 24 (außerhalb dieses Pakets, `phase7_spaces_admin/tests/test_acl_write.py` — gleiche Kategorie wie Zeile 10s `phase6_shares/tests/test_acl.py`) |
| 15 | Siebte, benannte Contract-Öffnung, angekündigt **und** gebaut in derselben Sitzung (P7 Step C4, Advisor-Fund): `store.py :: move()` erlaubt jetzt einen reinen Space-Wechsel für bereits archivierte Items (ein echter Ordner-Wechsel bleibt verboten); `_write_item_file()` legt ein archiviertes Item dabei ins Ziel-`_archive/`, nicht an die Space-Wurzel (`files.item_path()` kennt `_archive/` nicht — dieselbe Sonderbehandlung, die `archive()` bisher exklusiv hatte). Zweiter Advisor-Fund: `create(status="archived")` (über MCP/REST erreichbar, `STATUS_VALUES` erlaubt `archived` für beide Typen seit P2 Step 2) lief bis dahin am selben Riegel vorbei — jetzt landet auch ein direkt als `archived` angelegtes Item sofort unter `_archive/`, ein mitgeschicktes `folder` wird verworfen, dieselbe Zurücksetzung wie in `archive()` | P7 Step C4 | ✅ **gebaut, Phase noch nicht abgeschlossen** — schließt eine strukturelle Lücke, die C4s Space-Entfernen sonst bei jedem Space mit `_archive/`-Inhalt (also jedem Space mit echter Historie) permanent blockiert hätte | 4 (in `test_store.py`: `test_move_of_archived_item_between_spaces_relocates_to_target_archive`, `test_move_of_archived_item_produces_exactly_one_commit`, `test_move_of_archived_item_rejects_a_real_folder_change` — ersetzt den bisherigen `test_move_of_archived_item_is_rejected` —, `test_create_with_status_archived_lands_directly_in_archive_and_drops_folder`) |

**Gesamt: 154 Tests** (`70 Tests` war der Stand bei Phasenabschluss; **[2026-07-25 Korrektur,
P2 Step 0]:** `rename_for_new_slug()` samt zweier Tests entfernt, 70→68; **[2026-07-25,
P2 Step 2]:** acht neue Tests für die drei freigegebenen Contract-Erweiterungen, 68→76 — siehe
„Geerbte Contracts" unten; **[2026-08-09, P6 Step 1]:** fünf neue Tests für `Store.patch()`
(dritte, benannte Contract-Öffnung, siehe unten), 76→81; **[2026-08-12, P6 Step 4]:** 36 neue
Tests für `folder`/`visibility`/`share_*`/`acl_of()`/`list_spaces()` (Fortsetzung derselben
dritten Öffnung, siehe unten), 81→117; **[2026-08-17, P6 Step 7b Commit 1]:** sechs neue Tests
für `Store.move()` (vierte, benannte Contract-Öffnung, siehe unten), 117→123);
**[2026-08-20, Phase 6.5 Step A4]:** drei neue Tests für `search(in_body=)`, 123→126 — **Korrektur
im selben Tag, Step B1:** 126 war falsch, aus einer Delta-Rechnung ohne vollen Gegenzähler
übernommen; ein `pytest --collect-only -q` über **alle** `phase1_storage/tests/*.py` ergab **130**
vor Step B1, nicht 126 — vierzehnte Instanz derselben Drift-Kategorie wie die drei Korrekturen in
`phase2_mcp/CLAUDE.md`, diesmal von Claude Code selbst verursacht und noch am selben Tag beim
nächsten vollen Recount aufgefallen, nicht erst später gefunden; **[2026-08-20, Phase 6.5 Step
B1]:** 20 neue Tests für die fünfte Contract-Öffnung (Bild-Assets, siehe Zeile 13; 19 im ersten
Durchgang + 1 nach einem Advisor-Fund, siehe unten), 130→150. **[2026-08-25 Korrektur, P7 Step
C4]:** 150 war bereits leicht stale — P7 Step C2 (`Store.data_root`-Property, Modul-Status-Zeile
10 der Phase-7-Tabelle) hatte einen Test in `test_store.py` ergänzt, ohne dass diese Gesamtzahl
hier nachgezogen wurde (kein neuer Contract-Absatz, deshalb übersehen). Ein
`pytest --collect-only -q` über **alle** `phase1_storage/tests/*.py` ergab **154** — real
gezählt, nicht addiert: 151 (korrigierte Baseline) + 3 netto aus der siebten Öffnung (ein
bestehender Test ersetzt durch drei + ein neuer, siehe Zeile 15), 151→154.**
Zielgröße
am Phasenende: grob 60–90,
davon mindestens die vier Konflikt-Tests aus Step 4 — diese Zielgröße galt für den P1-Abschluss,
P6 öffnet den Contract erneut benannt, siehe unten. Step 0 hat bewusst keine Tests (reines
Skelett) — `pytest` lief dort grün mit `exit 5` („no tests ran", nicht `exit 0`); das ist die
korrekte Bedeutung von „0 Tests", kein Fehlerzustand.

## Geerbte Contracts

Keine — dies ist die erste Phase. **Die in Plan §1/§2 definierten Frontmatter-Felder und
Store-Signaturen werden mit Abschluss dieser Phase zum Contract für P2.** Eine Änderung daran
nach Phasenabschluss ist eine Scope-Änderung und braucht eine Entscheidung, kein Refactoring.

**[2026-07-25, P2 Step 2] Drei vom Nikinger freigegebene, einmalige Contract-Erweiterungen**
(`docs/concepts/phase2_mcp_plan.md` §0.4 Punkt L, §4 Step 2) — danach ist der Contract wieder
zu, keine stille Abweichung:
- `models.py`: `STATUS_VALUES`/`valid_statuses()` — Statusvokabular je `type`
  (`note`: `active`/`archived`; `task`: `open`/`done`/`archived`). `store.py :: create()`/
  `update()` werfen jetzt `ValidationError` bei unbekanntem `type` oder unerlaubtem `status`
  statt es unvalidiert durchzulassen (Entscheidung D2) — die CLI hielt das bisher nur über
  `argparse choices` ab, ein zweiter Adapter (MCP) wäre daran vorbeigelaufen.
- `store.py :: space_of(item_id)` — Space eines Items ausschließlich über den Index, kein
  Datei-Lesezugriff. Für die P2-Autorisierungsschicht: sie muss wissen, welchem Space ein Item
  gehört, **bevor** feststeht, ob der Zugriff überhaupt erlaubt ist.
- `store.py :: get(item_id, *, repair_drift=True)` / `_reconcile_and_get_row(...,
  repair_drift=True)` — bei `repair_drift=False` wird eine erkannte externe Inhaltsänderung
  **nur** im Index nachgezogen, nicht ins Frontmatter zurückgeschrieben und ohne Git-Commit
  (Entscheidung D3). Für fremde Spaces: ein Lesezugriff dort fasst keine Datei an (Rule 4);
  `version` ist dort informativ, nicht autoritativ, weil es dort per Architektur keine Writes
  gibt. Default bleibt `True` — jedes bestehende P1-Verhalten (inkl. CLI) ist unverändert.

**[2026-08-09, P6 Step 1] Dritte, benannte Contract-Öffnung** (`docs/concepts/phase6_shares_plan.md`
§1.4, angekündigt bereits in `phase6_shares/CLAUDE.md`s Step-0-Block) — `store.py :: patch(item_id,
*, version, edits) -> PatchResult` (neu, punktuelle Textersetzung statt Komplett-Rewrite, P6-E) und
das neue Modul `patch.py` (`TextEdit`/`PatchError`/`PatchResult`/`apply_edits()`). Rest der P6-Step-
4-Erweiterung (`folder`/`visibility`/`share_*`, `acl_of()`, `list_spaces()`-Verzeichnisbasis) folgt
erst dort — diese Öffnung deckt nur Step 1. Fünf neue Tests in `test_store.py`.

Acht neue Tests in `phase1_storage/tests/test_store.py`, alle 76 Tests grün (siehe Modul-Status
oben).

**[2026-08-12, P6 Step 4] Fortsetzung derselben dritten Öffnung** (Plan §1.4, nicht eine vierte —
Step 1 und Step 4 sind ein zusammenhängender, benannter Ausschlag desselben Contracts, siehe
`phase6_shares/CLAUDE.md`s Step-0-Ankündigung). Deckt jetzt auch den Rest:
- `models.py`: `VISIBILITY_VALUES`/`DEFAULT_VISIBILITY`; `Item`/`ItemSummary` bekommen `folder`
  (abgeleitet, NIE Frontmatter), `visibility`, `share_read`, `share_write`; `SpaceInfo` bekommt
  `members`/`folders`.
- `acl.py` (neu): `Grant`/`AclDecision`/`AclReader` — löst `.share.yml`-Freigaben auf, fail-closed,
  `stat()`-invalidierter Cache. `RESERVED_DIR_NAMES`/`MAX_FOLDER_DEPTH` leben bewusst in `files.py`
  statt hier (Ordnerpfad-Validierung ist bereits dessen Job) — kleine, dokumentierte Abweichung vom
  Plan-Snippet in §1.2.3, `acl.py` importiert von dort.
- `files.py`: `item_path(..., folder="")`, `validate_folder()`, `folder_from_path()`.
- `index.py`: vier neue Spalten (`folder`/`visibility`/`share_read_json`/`share_write_json`),
  `INDEX_SCHEMA_VERSION = 2` über `PRAGMA user_version` (V46 geschlossen).
- `store.py :: acl_of(item_id) -> AclDecision` (neu, index-only wie `space_of()`) · `create()`/
  `update()` akzeptieren `folder`/`visibility`/`share_read`/`share_write` · `search()` bekommt
  `spaces=`/`folder=` · `list_spaces()` jetzt verzeichnis- UND indexbasiert, mit `members`/`folders`.

**Zweiter Advisor-Fund vor dem Commit:** `_row_to_item()`/`acl_of()` übernahmen `row["folder"]`
zunächst direkt aus dem Index statt es aus dem Pfad neu abzuleiten — ein Verstoß gegen Entscheidung
**A**/Hard Rule 2 in diesem Kopf oben ("Ein Index-Fehler fasst nie eine Datei an"): ein veralteter
oder falscher Spaltenwert hätte beim nächsten `update()` die Datei bewegt. Behoben: beide rufen
jetzt `files.folder_from_path()` auf dem echten Pfad; `acl_of()` bleibt dabei index-only (reine
Pfad-Arithmetik, kein Datei-Lesezugriff). Details + der Rollback-Pfad, der das real erreichbar
macht (altes Binary gegen v2-Index), stehen in `phase6_shares/CLAUDE.md`s Session-Block.

**Ein echter operativer Fund während der Umsetzung, kein Plan-Text:** `Store.__init__` rief
`rebuild_index()` nie auf, und `phase2_mcp/scripts/serve.py` (der reale Diensteinstieg) auch
nicht — einziger Aufrufer war der manuelle `space_cli.py`-Befehl. Ein reiner Schema-Sprung hätte
den Produktivindex beim nächsten Deploy leer zurückgelassen. Behoben als Teil dieser Öffnung:
`index.connect()` liefert jetzt `(conn, rebuilt: bool)`, `Store.__init__` ruft bei `rebuilt=True`
selbst `rebuild_index()`. Das erfüllt tatsächlich Entscheidung **G** aus P1 (`rebuild_index()`
öffentlich **und beim Start**) — die zweite Hälfte war dokumentiert, aber nie verdrahtet, bis
jetzt. Live bestätigt (nicht nur in `pytest`, das jeden `tmp_path` immer frisch auf Schema-Version
2 startet und den Fehlerfall verdeckt hätte): `phase5_ui/scripts/ui_budget.py --json` gegen ein
brandneues Temp-`DATA_ROOT` geloggt exakt `Index ... hat Schema-Version 0 (erwartet 2) — wird
verworfen und leer neu angelegt`, danach lief der komplette Lauf (220 Items, echte MCP- und
REST-Requests) sauber durch.

Charakterisierungstests (P6-D, `phase6_shares/tests/test_characterization.py`, drei Golden Files)
liefen vor UND nach dieser Öffnung byte-identisch grün — das ist der Seam-Beweis für diesen
Umbau, siehe `phase6_shares/CLAUDE.md`. 36 neue Tests in `phase1_storage/` (1 `test_models.py` +
11 `test_files.py` + 4 `test_index.py` + 20 `test_store.py` — die zwei zusätzlichen
`test_files.py`-Tests pinnen `validate_folder()`s Traversal-Verhalten, zweiter Advisor-Fund) + 10 in
`phase6_shares/tests/test_acl.py` (außerhalb dieses Pakets, gleiche Kategorie wie
`test_patch.py`/`test_updates.py`). `git diff` auf `mcpserver/`/`webui/`/`authserver/` blieb leer
— Step 4 bleibt vollständig innerhalb `storage/`, wie geplant (P6-C).

**[2026-08-20, Phase 6.5 Step B1] Fünfte, benannte Contract-Öffnung gebaut** — wie unten
angekündigt, ohne Abweichung. `put_asset()` löst `sniff_image_mime()` selbst auf (kein
`filename`-Vertrauen), `_commit("asset", ...)` erzeugt genau einen Commit je Upload, unabhängig
von der Item-`version` (Assets konkurrieren nie mit einem Text-Write um dieselbe Version).
`list_assets()`/`get_asset()`/`delete_asset()` nehmen wie `get()` **beide** Sperren
(`self._lock` UND `self._file_write_lock()`) — `_reconcile_and_get_row()` kann auch bei
`repair_drift=False` reindizieren, das ist ein Index-Write außerhalb der Prozess-`flock`, wenn
nur `self._lock` gehalten wird. **Drei Advisor-Funde vor dem Commit behoben:** (1) genau diese
Lock-Lücke in `list_assets()`/`get_asset()` (ursprünglich nur `self._lock`); (2) `created` kam in
`put_asset()` aus `self._now_fn()`, in `list_assets()` aus der Datei-mtime — dasselbe Asset zeigte
zwei verschiedene Werte, weil nichts den Upload-Zeitpunkt separat persistiert; behoben, indem
`put_asset()` jetzt ebenfalls die mtime liest, plus ein Pflichttest, der beide Werte gegeneinander
pinnt; (3) `list_assets()` las für die MIME-Erkennung jedes Bild vollständig ein (`sniff_image_
mime()` braucht maximal 12 Bytes) — bei mehreren Bildern hätte das genau das Kostenversprechen von
`get_item_meta` („um Größenordnungen billiger") unterlaufen, jetzt `path.open("rb").read(12)`. 20
neue Tests (12 `test_files.py` + 8 `test_store.py`), Charakterisierung (P6-D) vor/nach
byte-identisch grün. Volle Herleitung, inkl. der `126`-vs-`130`-Zählkorrektur desselben Tages:
`phase6_5_tools_images/CLAUDE.md`s Session-Block.

**[2026-08-20, Phase 6.5 Step 0] Fünfte, benannte Contract-Öffnung angekündigt** (noch kein Code —
Ankündigung **vor** Step B1, `docs/concepts/phase6_5_tools_images_plan.md` §3 Step B1, P6.5-T),
Block C (Bilder): `models.py` bekommt `AssetInfo` (neuer Dataclass: `id`/`mime`/`bytes`/
`filename`/`created`); `files.py` bekommt `new_asset_id()`, `sniff_image_mime()` (Magic-Byte-
Erkennung PNG/JPEG/GIF/WebP, **kein** SVG/HEIC/PDF — P6-AZ), `asset_dir()`/`asset_path()`,
`move_asset_dir()` (No-op ohne Quellverzeichnis, sonst `os.replace` + `fsync` wie überall);
`store.py` bekommt `put_asset()`/`list_assets()`/`get_asset()`/`delete_asset()` (letzteres nur bei
Phase-6.5-Entscheidung N5 ≠ „gar nicht") sowie eine Erweiterung von `move()` um
`files.move_asset_dir(...)` **innerhalb** derselben Lock-Sektion, damit ein Move weiterhin genau
**einen** Git-Commit erzeugt. **Datierte Notiz zu Entscheidung H** (kein Delete im Kern-API):
Phase 6.5 löst N5 als „Verschieben statt Entfernen" (`_assets/<item_id>/_trash/`, dieselbe Bauart
wie `_archive/`) — Entscheidung H bleibt damit formal unangetastet, `delete_asset()` löscht nie,
es verschiebt. Charakterisierungstests (P6-D) laufen vor **und** nach dieser Öffnung
byte-identisch grün, dieselbe Disziplin wie bei den vier Vorgängern.

**[2026-08-23, Phase 7 Step 0] Sechste, benannte Contract-Öffnung angekündigt** (noch kein Code —
Ankündigung **vor** Block C Step C1, `docs/concepts/phase7_spaces_admin_plan.md` §4 C1, P7-P):
`storage/acl.py` bekommt eine Schreibseite — `read_share_file(data_root, space) -> dict[str,
list[str]]`, `write_share_file(data_root, space, data) -> None`, `add_member(data_root, space,
name, *, write) -> bool`, `remove_member(data_root, space, name) -> list[str]`,
`create_space(data_root, name) -> Path`, `remove_space_dir(data_root, name) -> None`,
`spaces_referencing(data_root, name, *, exclude=None) -> list[str]`, `class AclWriteError
(ValueError)`. **Extraktion aus `phase6_shares/scripts/spacectl.py`, keine Neuentwicklung**
(Referenz: `spacectl.py:90–107, 113–127, 133–148, 185–242`) — Ausgabetexte und Exit-Codes von
`spacectl.py` müssen byte-identisch bleiben, das ist die Bedingung, unter der die 20 bestehenden
`test_spacectl.py`-Tests der Regressionsbeweis für den Umbau sind. `create_space()` lehnt `/`,
führenden `.` und `files.RESERVED_DIR_NAMES` ab. Jede schreibende Funktion nimmt `flock` auf
`.write.lock` selbst, gibt ihn vor der Rückkehr frei, und ruft **keine** `Store`-Methode auf
(P7-M: zwei `open()` auf denselben Lock im selben Prozess blockieren einander). Charakterisierungs-
tests (P6-D) laufen vor **und** nach dieser Öffnung byte-identisch grün, dieselbe Disziplin wie
bei den fünf Vorgängern.

**[2026-08-23, P7 Step A8.5] Öffnungen 3, 4 und 5 geschlossen — Öffnung 6 bleibt offen, in
demselben Absatz genannt.** Dritte (`patch()`, P6 Step 1), vierte (`move()`, P6 Step 7b Commit 1)
und fünfte (Bild-Assets, Phase 6.5 Step B1) Öffnung sind mit ihren jeweiligen Phasenabschlüssen
datiert geschlossen (Phase 6 formal 🟡, Phase 6.5 formal 🟡, beide code-complete und live deployt
— siehe `docs/concepts/PHASE6_CLOSEOUT_HANDOVER.md`/`PHASE6_5_CLOSEOUT_HANDOVER.md`). **Die sechste
Öffnung (P7, `storage/acl.py`-Schreibseite, oben angekündigt) ist zum Zeitpunkt dieses Satzes
NICHT geschlossen** — Block C dieser Phase baut sie erst noch. Ein Schließen ohne diesen Satz
wäre dieselbe Falschaussage, die `PHASE6_CLOSEOUT_HANDOVER.md` §5.6 bereits vermieden hat.

**[2026-08-25, P7 Step C1] Sechste Öffnung: Code gebaut, bleibt formal offen bis Phasenabschluss.**
`acl.py` trägt jetzt `read_share_file`/`write_share_file`/`add_member`/`remove_member`/
`create_space`/`remove_space_dir`/`spaces_referencing`/`AclWriteError` — exakt wie oben
angekündigt, byte-identische Extraktion aus `spacectl.py` (20 bestehende `test_spacectl.py`-Tests
unverändert grün, Charakterisierung P6-D/P7-C vor+nach byte-identisch). 19 neue Tests in
`phase7_spaces_admin/tests/test_acl_write.py`. **Weiterhin nicht geschlossen** — Block C ist erst
mit C1 begonnen (C2–C5 folgen), dieselbe Disziplin wie oben: geschlossen wird erst mit dem
formalen Phase-7-Abschluss, nicht mit dem ersten Teilschritt.

**[2026-08-25, P7 Step C2] Kleine additive Erweiterung, keine siebte Öffnung.** `store.py`
bekommt `Store.data_root -> Path` (neue, reine Read-Property neben `acl_reader`) — kein neues
Verhalten, nur ein Zugriffspfad für `webui/api.py`s neue Space-Verwaltungsrouten, die `acl.py`s
Schreibseite (C1) direkt aufrufen und dafür den rohen `DATA_ROOT`-Pfad brauchen, den `Store`
bisher nur privat hielt. Kein eigener Absatz nötig gewesen, wird hier trotzdem benannt, damit
kein Leser eine unbelegte öffentliche Property vorfindet.

**[2026-08-25, P7 Step C4] Siebte, benannte Contract-Öffnung — angekündigt und gebaut in
derselben Sitzung, kein separater Ankündigungs-Absatz (Nikinger-Entscheidung im laufenden
Gespräch, nicht als eigener Plan-Step vorgeplant).** Ausgangspunkt war der P7-20-Fund im
Advisor-Review von Step C4 (`webui/api.py :: _spaces_delete`): `store.move()` verbot jeden Move
eines bereits archivierten Items pauschal, was einen Space mit `_archive/`-Inhalt — also jeden
Space mit echter Historie — strukturell unentfernbar gemacht hätte. **`store.py :: move()`**
erlaubt jetzt einen reinen Space-Wechsel für archivierte Items (kein `folder=` außer `""`); ein
echter Ordner-Wechsel bleibt verboten, weil ein archiviertes Item nie eine Ordnerposition trägt.
**`_write_item_file()`** legt ein archiviertes Item dabei ins Ziel-`_archive/`, nicht an die
Space-Wurzel — `files.item_path()` kennt diesen Sonderfall nicht, vorher war das exklusiv
`archive()`s eigene, separate Pfad-Berechnung. **Zweiter Advisor-Fund, vor demselben Commit:**
`create(status="archived")` — erreichbar über `POST /api/v1/items` (`webui/api.py`, `status`
steht in dessen Feld-Whitelist) und über MCP, `STATUS_VALUES` erlaubt `archived` für beide Typen
seit der P2-Öffnung — lief bisher am ursprünglichen Riegel vorbei und hätte mit dem `_write_
item_file()`-Fix eine Divergenz erzeugt (Datei landet in `_archive/`, `folder` im Frontmatter
bliebe der angeforderte Wert, den der nächste `get()` ohnehin verwirft, weil `folder` immer aus
dem realen Pfad abgeleitet wird — nie aus dem Frontmatter). **Entschieden:** `create()` setzt
`folder=""` jetzt selbst, sobald `status="archived"`, dieselbe Zurücksetzung wie in `archive()`
— ein Space mit direkt archiviert angelegten Items verhält sich damit identisch zu einem, dessen
Items später archiviert wurden, kein Sonderfall. Charakterisierung (P6-D/P7-C) lief vor und nach
byte-identisch grün. Vier neue/ersetzte Tests in `test_store.py` (siehe Modul-Status-Zeile 15).
**Bleibt formal offen bis zum Phase-7-Abschluss**, dieselbe Disziplin wie Öffnung 6.

**[2026-08-17, P6 Step 7b Commit 1/3] Vierte, benannte Contract-Öffnung gebaut** (angekündigt in
`phase6_shares/CLAUDE.md`s Session-Block vom selben Tag, `phase6_shares/ITEM_MOVE_PLAN.md` §4.1,
P6-AD): `store.py :: move(item_id, *, version, space=, folder=) -> Item` (neu) + intern
`_cleanup_emptied_folders()` (P6-AF). Additiv zu `update()`/`archive()` — `space` bleibt in
`_SYSTEM_MANAGED_FIELDS`, ein Move ist eine eigene Methode, kein Feld an `update()` (P6-AD,
verhindert dieselbe Divergenz-Klasse wie Fund B2 der P2-Adapter-Abnahme). Charakterisierung
(`phase6_shares/tests/test_characterization.py`) lief vor und nach byte-identisch grün. Sechs
neue Tests in `test_store.py`, `git diff` auf `mcpserver/`/`webui/`/`authserver/` leer — reiner
`storage/`-Commit. Autorisierung (P6-AE, Schreibrecht auf Quelle **und** Ziel) passiert bewusst
NICHT hier, wie überall im Store — Commit 2/3 (`mcpserver/tools.py`, `webui/api.py`) baut die
Rechteprüfung eine Schicht höher.

---

## Session stopped — 2026-07-25 (Phase 1 live-verifiziert, Phase abgeschlossen)

**Live-Verify durch den Nikinger (2026-07-25), gegen den echten `DATA_ROOT`
(`/home/savefyx/savefyx-data`), nicht Claude Code (Hard Rule):**

```
$ space_cli --data-root /home/savefyx/savefyx-data create nikinger --type task \
    --title "Erster echter Space-Server-Eintrag" --tag test
itm_7a6f9f7f  [nikinger]  task  v1  status=open
$ space_cli --data-root /home/savefyx/savefyx-data list
nikinger: 1 Item(s)
$ space_cli --data-root /home/savefyx/savefyx-data search
1 Treffer (zeige 1, offset=0, limit=50)
  itm_7a6f9f7f  [nikinger]  open  tags=test  Erster echter Space-Server-Eintrag
$ git -C /home/savefyx/savefyx-data log --oneline
4e2eb29 (HEAD -> master) create itm_7a6f9f7f [nikinger]
```

**Claude Code hat den entstandenen Zustand danach read-only nachgeprüft** (kein Write meinerseits
gegen den echten `DATA_ROOT`, nur Lesen/`git status`/`git log`):
- Datei `nikinger/itm_7a6f9f7f__erster-echter-space-server-eintrag.md` — Frontmatter exakt wie
  erwartet (`id`/`space`/`type`/`title`/`status`/`tags`/`links`/`created`/`updated`/`version`,
  ISO-Z-Zeitstempel).
- `.gitignore` korrekt angelegt (`.index.sqlite3*`, `.write.lock`) — **das ist die reale Probe
  auf den Advisor-Fund aus Step 5**: `git status` im Datenverzeichnis ist clean, obwohl
  `.index.sqlite3` und `.write.lock` auf der Platte liegen. Ohne den Fix wären beide hier jetzt
  im ersten Commit gelandet.
- Commit-Identity `Space Server <space-server@localhost>` — genau wie in `ensure_repo()`
  vorgesehen, weil diese Maschine keine globale Git-Identity hat (bereits in Step 5 geprüft).
- Dateisystem `ext4` (per `findmnt`), wie seit Step 0/3 angenommen.
- Branch im Datenverzeichnis heißt `master` (Git-Default ohne `init.defaultBranch`, nicht `main`
  wie im Code-Repo) — kosmetisch, kein Fix nötig: dieses Repo hat keinen Remote, niemand
  referenziert den Branchnamen.

Damit ist Phase 1 nicht nur code-complete, sondern **live-bewiesen** — Status auf ✅ gehoben
(siehe Modul-Status/ROADMAP.md, beide im selben Commit aktualisiert).

**Geerbte Contracts für P2 jetzt final** (siehe „Geerbte Contracts" oben, Plan §1/§2): Frontmatter-
Schema, `Item`/`SpaceInfo`/`ItemSummary`/`SearchResult`/`IndexStats`, `Store`-Signaturen. Änderung
daran nach diesem Punkt ist eine Scope-Änderung, kein Refactoring.

**Nächster Schritt (konkret):** Der offizielle Phasen-Abschluss läuft laut `docs/PROMPTS.md` als
eigener Prompt im Browser-Webchat (Nikinger, direkt im Anschluss an diese Session) — dieser
Commit liefert dafür den fertigen, live-verifizierten Stand. Danach: neue Browser-
Planungssession für Phase 2 (MCP-Server, Auth, Cross-Space-Autorisierung — siehe `ROADMAP.md`).
Bis dahin: keine P2-Arbeit vorziehen, auch wenn der Contract jetzt feststeht.

**Aufgelöst seit Step 0–4:** `flock` auf ext4 (Step 0) · `python-frontmatter`-Roundtrip →
verworfen, eigener Parser (Step 1) · Dateisystem-Ermittlung via `/proc/mounts` (Step 3) ·
`IndexError_` → `IndexCorrupt` (Step 4).

**Kleine Korrektur zum Plan:** „`pytest` grün mit null Tests" (Step 0, Done-when) bedeutet in der
Praxis `exit 5` („no tests ran"), nicht `exit 0` — pytest markiert eine leere Testsammlung so.
Kein Fehler, nur eine Präzisierung; siehe Modul-Status-Tabelle oben.

**Der vorherige Session-Block (Planungsabschluss) ist verbatim nach `SESSIONS_ARCHIVE.md`
gewandert — Rotationsregel, ab dieser (zweiten) Session aktiv.**
