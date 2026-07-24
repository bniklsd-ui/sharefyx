---
status: live
purpose: Phase-Head Storage-Kern — Scope, harte Regeln, gelockte Entscheidungen, Modulstatus, aktueller Session-Handover
read-when: Arbeiten in phase1_storage/ — zuerst lesen, zusammen mit dem neuesten Session-stopped-Block
detail: L2
up: ../CLAUDE.md
down:
  - ../docs/concepts/phase1_storage_plan.md   # voller Plan, Entscheidungen A–H, Steps 0–7
  - SESSIONS_ARCHIVE.md                       # ältere Session-Blöcke
updated: 2026-07-24
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
  eines neuen wandert der bisherige **verbatim** (mechanisch, `sed -n 'A,Bp'`) nach
  `SESSIONS_ARCHIVE.md`, newest-first. Niemals abtippen.

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
| 3 | `files.py` (atomarer Write, IDs, Slugs) | 2 | ✅ | 12 |
| 4 | `index.py` (SQLite, Rebuild) | 3 | ✅ | 9 |
| 5 | `store.py` (API, Lock, Versionierung) | 4 | ✅ | 18 |
| 6 | `history.py` (Git) | 5 | ⬜ | – |
| 7 | Query-Layer in `store.py` | 6 | ⬜ | – |
| 8 | `scripts/space_cli.py` | 7 | ⬜ | – |

**Gesamt: 48 Tests.** Zielgröße am Phasenende: grob 60–90, davon mindestens die vier
Konflikt-Tests aus Step 4. Step 0 hat bewusst keine Tests (reines Skelett) — `pytest`
lief dort grün mit `exit 5` („no tests ran", nicht `exit 0`); das ist die korrekte
Bedeutung von „0 Tests", kein Fehlerzustand.

## Geerbte Contracts

Keine — dies ist die erste Phase. **Die in Plan §1/§2 definierten Frontmatter-Felder und
Store-Signaturen werden mit Abschluss dieser Phase zum Contract für P2.** Eine Änderung daran
nach Phasenabschluss ist eine Scope-Änderung und braucht eine Entscheidung, kein Refactoring.

---

## Session stopped — 2026-07-24 (Step 0–4 abgeschlossen — der Phasenbeweis steht)

**Ergebnis:** Code-Repo initialisiert (`git init` in `/home/savefyx/dev/savefxy`, lokale Git-Identity
gesetzt, da auf der Maschine keine existierte). Erster Commit checkt die Projektdokumente aus der
Browser-Planungssession ein; zweiter Commit liefert das Step-0-Skelett: `phase1_storage/pyproject.toml`
(Paket `storage`, editable installierbar), `phase1_storage/storage/__init__.py` (`__version__ = "0.1.0"`),
`phase1_storage/tests/` (leer, `conftest.py` als Platzhalter), Root-`pytest.ini`
(`testpaths = phase1_storage/tests`), Root-`scripts/dev_install.sh` (installiert alle `phase*_*/`-Pakete
editable, generisch für kommende Phasen), Root-`.gitignore` (`.venv`, `__pycache__`, `*.egg-info`,
`.index.sqlite3`, `.pytest_cache`, plus `.claude/`/`.agents/`/Lockfiles als Harness-lokaler Zustand).

**Verifiziert (live, nicht nur gelesen):** `python3 -m venv .venv && ./scripts/dev_install.sh` lief
durch; `pytest` läuft grün mit `exit 5` / „no tests ran" (0 Tests, korrekt für ein reines Skelett);
`from storage import __version__` importiert `"0.1.0"`.

**Blocker aufgelöst:** `DATA_ROOT = /home/savefyx/savefyx-data` (Nikinger-Entscheidung, ext4,
lokale Platte, kein Shared Folder). System-Dependency-Lücke (`pip`/`ensurepip` fehlten unter Ubuntu)
über `sudo apt install python3-venv python3-pip -y` durch den Nikinger behoben — Claude Code hat
in dieser Sandbox kein `sudo`.

**Step 1 Ergebnis:** `[VERIFY]` zu `python-frontmatter` empirisch aufgelöst — **verworfen**.
Probe (`frontmatter.loads`/`dumps` auf einem Fixture mit Umlauten, unbekanntem Feld,
ISO-Timestamp) zeigte zwei Verstöße gegen Entscheidung A: Keys werden alphabetisch sortiert
(`sort_keys` nicht exponiert) und Timestamps werden zu `datetime` gecastet und in einem anderen
Format zurückgeschrieben (`2026-07-24T18:20:00Z` → `2026-07-24 18:20:00+00:00`). Stattdessen:
eigener, dünner Parser in `storage/frontmatter.py` über PyYAML — `SafeLoader`/`SafeDumper` mit
entferntem Timestamp-Resolver (auf **beiden** Seiten, sonst quotet der Dumper datumsartige
Strings trotzdem, da sein `Resolver` unabhängig vom Loader ist), `sort_keys=False`,
`allow_unicode=True`. `storage/models.py` liefert `Item`, `SpaceInfo`, `ItemSummary`,
`SearchResult`, `IndexStats` als `@dataclass(kw_only=True)` — `kw_only` vermeiden das
Default-Reihenfolge-Problem bei Pflichtfeldern wie `created`/`updated` ohne Default neben
optionalen wie `due`.

**Implementierungsentscheidung (Plan unterspezifiziert, hier getroffen):** Plan §4 Step 1 nennt
nur vier Dataclasses, aber `SearchResult` soll laut Plan §2 „ausschließlich Frontmatter plus
Snippet, niemals volle Bodies" tragen — dafür reicht `Item` nicht (hat `body`, kein `snippet`).
Deshalb zusätzlich `ItemSummary` (Frontmatter-Felder + `snippet: str`, kein `body`) als
Element-Typ von `SearchResult.items`. `SpaceInfo` bekam `name: str` + `item_count: int`
(im Plan nicht spezifiziert, aber ohne Count ist ein Space-Listing nutzlos). Beides ist ab
Phasenende Contract für P2 (siehe „Geerbte Contracts" oben) — **bei Bedarf mit dem Nikinger
gegenprüfen, bevor P2 darauf aufbaut.**

**Verifiziert (live):** `pytest -v` → 9/9 grün (6 `test_frontmatter.py`, davon die geforderte
Property-Test-Fixture mit Umlauten/mehrzeiligem Body/unbekanntem Feld/leerem Body; 3
`test_models.py` als Konstruktions-Smoke-Test).

**Step 2 Ergebnis:** `storage/files.py` — `generate_id()` (`itm_` + 8 Hex aus
`secrets.token_hex(4)`), `slugify()` (deutsche Umlaute per `str.translate`-Tabelle: `ä→ae`,
`ö→oe`, `ü→ue`, `ß→ss`, dann lowercase, non-alnum → `-`, Kollaps + Strip, Fallback `"item"` bei
leerem Ergebnis), `item_filename`/`item_path` (`<id>__<slug>.md`), `atomic_write()` (tmp im
selben Verzeichnis + fsync der Datei + `os.replace` + fsync des Verzeichnisses — bei Exception
Best-effort-Cleanup der tmp-Datei, Ziel bleibt garantiert unangetastet, da `os.replace` eine
atomare Rename-Syscall ist), `rename_for_new_slug()` (gleiche Replace+fsync-Logik für
Titeländerungen, No-op wenn sich der Slug nicht ändert). `files.py` kennt bewusst kein
YAML/Frontmatter — bekommt fertigen Dateitext von der aufrufenden Schicht.

**Verifiziert (live):** `pytest -v` → 21/21 grün (12 neue in `test_files.py`): 200-Item-Write-Test,
`kill -9`-Simulation per `monkeypatch.setattr("storage.files.os.replace", boom)` in zwei Varianten
(neue Datei bleibt inexistent / bestehende Datei bleibt beim alten Inhalt), Slug-Kollision zweier
Items mit identischem Titel überschreibt nichts (unterschiedliche IDs im Dateinamen), Rename-Test.

**Step 3 Ergebnis:** `storage/index.py` — Schema exakt wie im Plan (`items` mit `tags_json`/
`links_json` als JSON-Strings), `connect()` (WAL-Modus, Schema-Anlage, **Selbstheilung**: ein
korrupter DB-File wird bei jedem der beiden möglichen Fehlerorte — `PRAGMA`/Schema-Erzeugung
oder der nachgelagerten Sanity-Probe `SELECT COUNT(*)` — abgefangen, verworfen samt
`-wal`/`-shm`-Sidecars, und leer neu angelegt; kein Crash, keine Eskalation), `upsert_item`/
`delete_item`/`get_item_row`/`all_rows` als CRUD-Grundlage für `store.py`, `row_from_file()`
(liest eine Datei rein lesend, berechnet `sha256` über die Rohbytes für Entscheidung D),
`rebuild_index()` (löscht Tabelleninhalt, scannt alle Space-Verzeichnisse **inklusive
`_archive/`** rekursiv nach `*.md`, baut alles neu — liefert `IndexStats` aus `models.py`).
`space` wird für jede Zeile aus dem Pfad abgeleitet (erstes Segment relativ zu `data_root`), nicht
aus dem Frontmatter-Feld — konsistent mit „Dateien sind die Wahrheit": ein Mensch kann `space:`
im Frontmatter verstellen, der Ordner lügt nicht.

**`[VERIFY]` Dateisystem-Ermittlung aufgelöst:** `os.statvfs` liefert den Typ tatsächlich nicht
direkt (bestätigt); `/proc/mounts` zeilenweise parsen und den am tiefsten passenden Mountpoint
nehmen ist zuverlässig und funktioniert ohne Subprocess/Zusatzpaket. `detect_filesystem_type()`
macht genau das; `check_filesystem()` nimmt zusätzlich ein `fstype`-Override für Tests, damit sie
nicht auf `/proc/mounts` angewiesen sind. Live gegen `tmp_path` verifiziert: liefert `"ext4"`
(kein Verstoß gegen „nie gegen DATA_ROOT testen" — `tmp_path` ist pytest-eigen).

**Verifiziert (live):** `pytest -v` → 30/30 grün (9 neue in `test_index.py`): CRUD-Roundtrip,
Rebuild == manuelle Upserts (inkl. archivierter Items), Rebuild-vor/nach-Löschen liefert
identische Zeilen, korrupter Index-File crasht `connect()` nicht und lässt sich anschließend
per `rebuild_index()` befüllen, `check_filesystem()` loggt bei `nfs4` genau eine
`critical`-Zeile und bei `ext4` keine, `detect_filesystem_type(tmp_path)` liefert real `"ext4"`.

**Erledigt nebenbei:** `DATA_ROOT` (`/home/savefyx/savefyx-data`) angelegt, per `findmnt`
bestätigt `ext4` (Nikinger-Wunsch, `mkdir` statt Aufschieben).

**Step 4 Ergebnis — der Phasenbeweis steht:** `storage/errors.py` (neu: `SpaceError`,
`ItemNotFound`, `SpaceNotFound`, `ConflictError` trägt `current: Item`, `ValidationError`,
`IndexCorrupt` — `IndexError_` wie geplant umbenannt, da Kollision mit dem Python-Builtin
`IndexError`; bislang ungenutzt, `index.connect()` heilt Korruption still). `storage/store.py`:
volle API aus Plan §2 (`list_spaces`, `search`, `get`, `create`, `update`, `append`, `archive`,
`rebuild_index`). Ein `threading.RLock()` serialisiert **jeden** Store-Aufruf innerhalb des
Prozesses (Plan §3.1: „ein Prozess reicht"), zusätzlich `fcntl.flock` auf
`<DATA_ROOT>/.write.lock` nur um die eigentlichen Dateischreibvorgänge (create/update/append/
archive) — schützt gegen andere Prozesse, nicht gegen den Menschen im Editor (siehe Plan §3.2,
weiterhin gültig). `Item.version` wird beim Lesen **immer aus dem Index** genommen, nicht aus
dem rohen Frontmatter-Feld — dadurch funktioniert Drift-Erkennung (Entscheidung D) sauber: bei
`(mtime, size)`-Abweichung wird `sha256` nachgerechnet, bei echter Änderung `version` im Index
+1 gesetzt, ohne die Datei anzufassen; der nächste offizielle Write schreibt die gebumpte Version
dann auch ins Frontmatter zurück und bringt beides wieder in Sync.

**Zwei Bugs vor dem ersten Testlauf gefunden und gefixt (Design-Review, nicht Testfund):**
(1) `due` kam aus `**fields`/`**changes` ungefiltert durch — ein ISO-String hätte beim Schreiben
an `item.due.isoformat()` gecrasht. Fix: `_coerce_due()` akzeptiert `date`, ISO-String oder
`None`. (2) System-verwaltete Felder (`id`, `space`, `created`, `updated`, `version`) landeten
bei unbekannten Keys in `Item.extra` — und `_item_to_text()` schreibt `fields.update(item.extra)`
**nach** den berechneten Werten, hätte sie also lautlos überschrieben. Fix:
`_SYSTEM_MANAGED_FIELDS`-Guard in `create()` und `update()`, wirft `ValidationError` statt
still zu korrumpieren.

**Ein echter Testfund:** `sqlite3.connect()` lehnt standardmäßig Zugriffe aus einem anderen
Thread ab als dem, der die Connection geöffnet hat — Test 3 (zwei Threads) crashte beide Threads
mit `ProgrammingError`, nicht mit dem erwarteten `ConflictError`. Fix in `index.py`:
`check_same_thread=False` beim `connect()`, mit Kommentar warum das hier sicher ist (Store
serialisiert bereits selbst über sein eigenes Lock). `test_3` 20× wiederholt laufen lassen,
keine Flakiness.

**Verifiziert (live):** `pytest -v` → 47/47 grün (17 neue in `test_store.py`, davon die vier
Pflicht-Tests namentlich `test_1_…` bis `test_4_…`). Zusätzlich Basisabdeckung: Status-Defaults
nach `type`, Rename bei Titeländerung, `extra`-Felder überleben Updates, `archive()` verschiebt
nach `_archive/`, `search()` liefert nur Summaries (kein `body`-Attribut), `list_spaces()`
zählt korrekt pro Space.

**Nachtrag zu Step 4 — Advisor-Fund, per Nikinger-Entscheidung gefixt (noch vor Step 5):**
Der Advisor (Opus 4.8, vom Nikinger nach der Review-Pause aktiviert) fand einen echten
Konflikt zwischen zwei gelockten Entscheidungen, den `store.py` lautlos aufgelöst hatte, statt
ihn sichtbar zu machen — genau der Fall, den die Root-`CLAUDE.md` mit „Widersprechende Evidenz
wird ein expliziter Befund für den Menschen, nie eine stille Abweichung" adressiert:

Die durch Drift-Erkennung (Entscheidung D) erhöhte Version lebte **nur im Index**. Ein
`rebuild_index()` (Entscheidung A, „jederzeit erlaubt" — und läuft laut Entscheidung G bei
jedem Start) liest die Version aus dem Frontmatter, das der Mensch nie angefasst hat, und setzt
sie damit lautlos wieder auf den alten Stand zurück. Da `version` der Lock-Guard selbst ist,
öffnet das nach jedem Neustart erneut ein Fenster, in dem ein Client mit veralteter `version`
einen menschlichen Edit überschreiben kann, ohne dass `ConflictError` greift. Empirisch
reproduziert (`get()` nach externem Edit → Version 2, nach `rebuild_index()` → zurück auf 1).

**Nikinger-Entscheidung (2026-07-24):** Die Datei bleibt die Wahrheit — der Bump wird ins
Frontmatter zurückgeschrieben. Umgesetzt: `_reconcile_and_get_row()` schreibt bei echter
Inhaltsänderung (`sha256` weicht ab) nur das `version`-Feld neu (`_rewrite_version_in_file()`,
minimaler Fußabdruck, alles andere bleibt byte-identisch). Locking dafür neu geordnet:
`get()` hält jetzt **auch** `self._file_write_lock()` (nicht mehr nur `self._lock`), und
`_reconcile_and_get_row`/`_rewrite_version_in_file` verwalten **kein eigenes** Lock mehr —
verschachteltes `flock` auf demselben Lockfile hätte sich selbst blockiert, sobald
`update`/`append`/`archive` (die den Write-Lock bereits halten) intern hier reinlaufen.
Regressionstest `test_drift_bumped_version_survives_rebuild_index` in `test_store.py` fixiert
das Verhalten. Re-verifiziert: 48/48 grün.

**Für Step 5 vorgemerkt:** `get()` ist jetzt ein potenzieller Writer (wenn Drift real bumpt).
Sobald `history.py` an die vier bekannten Schreibstellen angeschlossen wird, muss diese
fünfte — bislang unsichtbare — Schreibstelle mitgedacht werden, sonst fehlt für einen
drift-ausgelösten Rewrite der Git-Commit.

**Bewusst nicht Step-4-fertig (gehört zu Step 6):** `search()` existiert und funktioniert
(Filter, einfache Sortierung, Snippet via `_snippet()`), ist aber **nicht** gegen das
3-KB-Listing-Ziel kalibriert und die Sortierstabilität ist ein Platzhalter
(`status != open/active` zuerst, dann `due`, dann `updated` absteigend) — Plan Step 6 macht das
verbindlich. Modul-Status-Zeile 7 bleibt deshalb ⬜.

**Nächster Schritt (konkret):** Step 5 — `storage/history.py`: Git-Repo-Init in `DATA_ROOT`
falls nötig, ein Commit nach jedem erfolgreichen Write (`<op> <item_id> [<space>]`), `git: bool`-
Schalter (in `Store.__init__` bereits als `self._git_enabled` vorhanden, aber noch **folgenlos**
— Step 5 muss `store.py` an den **fünf** Schreibstellen tatsächlich an `history.py` anschließen:
`_write_item_file()` (create/update/append), `archive()`, **und** `_rewrite_version_in_file()`
im Drift-Pfad von `_reconcile_and_get_row()` — die fünfte kam erst nach der Step-4-Review dazu,
siehe Nachtrag oben). Git-Fehler → `logger.critical`, niemals den Write abbrechen.
Done-Kriterium: 3 Writes → `git log` zeigt 3 Commits mit erwarteten Messages; ein kaputtes
Git-Repo lässt Writes weiterlaufen und loggt `critical`.

**Offene `[VERIFY]` in diesem Track:** Snippet-/Listing-Größenziel 3 KB (Plan Step 6 — jetzt der
nächste inhaltliche Block nach Step 5).
**Aufgelöst seit Step 0–4:** `flock` auf ext4 (Step 0) · `python-frontmatter`-Roundtrip →
verworfen, eigener Parser (Step 1) · Dateisystem-Ermittlung via `/proc/mounts` (Step 3) ·
`IndexError_` → `IndexCorrupt` (Step 4).

**Kleine Korrektur zum Plan:** „`pytest` grün mit null Tests" (Step 0, Done-when) bedeutet in der
Praxis `exit 5` („no tests ran"), nicht `exit 0` — pytest markiert eine leere Testsammlung so.
Kein Fehler, nur eine Präzisierung; siehe Modul-Status-Tabelle oben.

**Der vorherige Session-Block (Planungsabschluss) ist verbatim nach `SESSIONS_ARCHIVE.md`
gewandert — Rotationsregel, ab dieser (zweiten) Session aktiv.**
