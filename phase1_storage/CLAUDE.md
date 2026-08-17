---
status: live
purpose: Phase-Head Storage-Kern — Scope, harte Regeln, gelockte Entscheidungen, Modulstatus, aktueller Session-Handover
read-when: Arbeiten in phase1_storage/ — zuerst lesen, zusammen mit dem neuesten Session-stopped-Block
detail: L2
up: ../CLAUDE.md
down:
  - ../docs/concepts/phase1_storage_plan.md   # voller Plan, Entscheidungen A–H, Steps 0–7
  - SESSIONS_ARCHIVE.md                       # ältere Session-Blöcke
updated: 2026-08-17 (P6 Step 7b Commit 1/3 -- vierte Contract-Oeffnung: store.py :: move() + _cleanup_emptied_folders(), 123 Tests)
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

**Gesamt: 123 Tests** (`70 Tests` war der Stand bei Phasenabschluss; **[2026-07-25 Korrektur,
P2 Step 0]:** `rename_for_new_slug()` samt zweier Tests entfernt, 70→68; **[2026-07-25,
P2 Step 2]:** acht neue Tests für die drei freigegebenen Contract-Erweiterungen, 68→76 — siehe
„Geerbte Contracts" unten; **[2026-08-09, P6 Step 1]:** fünf neue Tests für `Store.patch()`
(dritte, benannte Contract-Öffnung, siehe unten), 76→81; **[2026-08-12, P6 Step 4]:** 36 neue
Tests für `folder`/`visibility`/`share_*`/`acl_of()`/`list_spaces()` (Fortsetzung derselben
dritten Öffnung, siehe unten), 81→117; **[2026-08-17, P6 Step 7b Commit 1]:** sechs neue Tests
für `Store.move()` (vierte, benannte Contract-Öffnung, siehe unten), 117→123). Zielgröße am
Phasenende: grob 60–90,
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
