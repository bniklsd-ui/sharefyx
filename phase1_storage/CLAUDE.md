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
| 6 | `history.py` (Git) | 5 | ✅ | 11 |
| 7 | Query-Layer in `store.py` | 6 | ✅ | 2 (in `test_store.py`) |
| 8 | `scripts/space_cli.py` | 7 | ⬜ | – |

**Gesamt: 61 Tests.** Zielgröße am Phasenende: grob 60–90, davon mindestens die vier
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

**Step 5 Ergebnis:** `storage/history.py` — `ensure_repo()` (init `.git` in `DATA_ROOT` falls
nötig, schreibt dabei `.gitignore` mit `.index.sqlite3*` inkl. WAL-/SHM-Sidecars und
`.write.lock` — sonst hätte der erste Commit den derivierten Index eingecheckt, direkter
Verstoß gegen Entscheidung A) und `commit()` (`git add -A` + `git commit -m <message>`). Beide
über `subprocess.run(["git", "-C", ...])`, nie fatal: jeder Fehlerpfad (Binary fehlt, kaputtes
Repo, nichts zu committen) landet in `logger.critical`, nie in einer Exception — ein Write darf
nie an Git scheitern (Entscheidung E).

**Verifiziert auf Nikinger-Hinweis (SSH-Key + `gh auth login` vorhanden):** `gh auth status`
zeigt nur GitHub-Auth fürs Pushen/Pullen (SSH, Account `bniklsd-ui`) — orthogonal zur lokalen
Commit-Identity. Kein `~/.gitconfig`, kein `/etc/gitconfig`, keine `GIT_AUTHOR_*`/
`GIT_COMMITTER_*`-Env-Vars gefunden; einzige existierende `user.name`/`user.email` ist lokal im
Code-Repo (`savefxy/.git/config`, `Nikinger`/`nikinger@savefyx.local`, extra für dieses Repo
gesetzt). Deshalb setzt `ensure_repo()` in `DATA_ROOT` eine **eigene** lokale Identity
(`Space Server <space-server@localhost>`) — aber nur wenn dort noch **keine** existiert (auch
wenn `.git` schon von Hand angelegt wurde, nicht nur beim frischen Init), sonst würde jeder
Commit für immer fehlschlagen und `critical` spammen. Überschreibt nie eine vorhandene Identity.

**Anschluss in `store.py`:** alle **fünf** Schreibstellen aus dem Nachtrag oben sind jetzt
verdrahtet — `_write_item_file()` bekam einen `op`-Parameter (`"create"`/`"update"`/`"append"`)
und committet am Ende selbst; `archive()` (eigener Schreibpfad, nicht über `_write_item_file`)
committet direkt danach; `_reconcile_and_get_row()` committet mit `op="drift"` direkt nach
`_rewrite_version_in_file()` im echten-Drift-Zweig. Neuer `Store._commit(op, item_id, space)`-
Helper baut die Message `<op> <item_id> [<space>]` (Entscheidung E) und ruft `history.commit()`
nur wenn `self._git_enabled`. **Wichtig, als Kommentar im Code festgehalten:** `_commit()` wird
ausschließlich aus Aufrufern heraus benutzt, die bereits `self._file_write_lock()` halten — das
serialisiert Git-Aufrufe auch über Prozessgrenzen hinweg und verhindert, dass zwei gleichzeitige
`git commit`-Prozesse sich über `.git/index.lock` in die Quere kommen.

**Bewusst nicht extra behandelt (eine Zeile statt Extra-Code):** ein leerer Commit ist von
keinem Store-Pfad aus erreichbar (`version`/`updated` ändern den Dateitext bei jedem Write), ein
Nicht-Null-Exit wird trotzdem einheitlich als `critical` behandelt; `git add -A` erfasst auch
einen zeitgleichen menschlichen Edit mit — laut Entscheidung E ist das "ein Git-Commit im
Datenverzeichnis", kein Commit nur der eigenen Änderung, und die Undo-Historie bleibt vollständig.

**Verifiziert (live):** `pytest -v` → 59/59 grün (7 neue in `test_history.py`: Init/Idempotenz/
Identity-gesetzt-wenn-fehlt/Identity-nicht-überschrieben/Commit-Message exakt/kaputtes-Repo-
loggt-critical/Git-Binary-fehlt-loggt-critical; 4 neue in `test_store.py` mit neuer
`store_git`-Fixture: 3 Writes → 3 Commits mit erwarteten Messages in Reihenfolge,
`append`-Commit, `drift`-Commit nach externem Edit + `get()`, **echt** kaputtes Repo
`.git`-Verzeichnis durch Datei ersetzt → `create()` liefert trotzdem ein valides Item, Datei
existiert, `caplog` enthält `critical`). Die vier Pflicht-Tests aus Step 4 bleiben unverändert
auf `git=False` — Konfliktlogik, kein Git-Test. Manueller Smoke-Test zusätzlich live
nachvollzogen: `Store(tmp_path, git=True)` → ein `create()` → `git log --oneline` zeigt genau
einen Commit (Step-5-Done-when wörtlich).

**Nachtrag zu Step 5 — Advisor-Fund, noch im selben Schritt gefixt:** `ensure_repo()` schrieb
die `.gitignore` nur im frischen-Init-Zweig. Ein von Hand angelegtes oder aus einem Backup
wiederhergestelltes `DATA_ROOT`-Repo (bereits `.git`, kein Init-Zweig durchlaufen) hätte damit
nie eine `.gitignore` bekommen — der erste `commit()` hätte `.index.sqlite3` samt WAL/SHM und
`.write.lock` mit eingecheckt, derselbe Entscheidung-A-Verstoß, den die Identity-Fix-Diskussion
schon einmal aufgeworfen hatte. Fix: `.gitignore`-Schreibung aus dem Init-Zweig herausgezogen,
läuft jetzt unconditional (wie die Identity-Prüfung). `test_ensure_repo_does_not_overwrite_existing_identity`
um eine `.gitignore`-Assertion ergänzt — empirisch bestätigt: schlägt gegen den alten Code fehl,
grün gegen den Fix (diskriminierender Test, nicht nur Feel-Good). Zusätzlich `test_git_enabled_commits_one_per_write_with_expected_messages`
um `len(log) == 3` verschärft (Done-when nennt explizit die Anzahl). 59/59 weiterhin grün, keine
neuen Tests, nur verschärfte Assertions.

**Kleine Korrektur (Doc-Drift):** `docs/INDEX.md` Zeile 34 stand seit Steps 1–4 auf dem
veralteten „Step 0 ✅, Steps 1–7 offen" — beim Session-Einstieg dieser Session bemerkt, hier
mit Datum korrigiert (2026-07-24) und auf den echten Stand nach Step 5 gebracht.

**Step 6 Ergebnis:** Query-Layer geprüft statt neu gebaut — `search()` erfüllte bereits seit
Step 4 alle Anforderungen (Volltext nur über `title`+`tags`, nie Bodies; Snippet via
`_snippet()`; Paginierung; Sortierung `status offen zuerst → due aufsteigend → updated
absteigend`). Kein Produktivcode geändert, `store.py` unangetastet (per Diff verifiziert) —
Step 6 war reines Testen/Kalibrieren/Verbindlich-Machen, kein Bau.

**`[VERIFY]` 3-KB-Ziel empirisch aufgelöst — Schätzung war strukturell nicht erreichbar, nicht
nur ungenau:** Drei Stufen gegen `ItemSummary` (12 Felder) gemessen, jeweils 30 Items,
korrekte ISO-Z-Zeitstempel (`%Y-%m-%dT%H:%M:%SZ`, nicht Pythons `str(datetime)` — letzteres
kostet 5 B/Feld extra):
- **Floor** (leerer Titel, kein Tag, kein `due`, leerer Body): ~7,0 KB (~233 B/Item) — allein
  der JSON-Rahmen der 12 Felder (Keys, Anführungszeichen, Klammern) ohne jeden Inhalt.
- **Realistisch** (normaler Titel, 2 Tags, `due`, kurzer Body → kurzer Snippet): ~10,3 KB
  (~345 B/Item).
- **Ceiling** (langer Titel, 3 Tags, `due`, Body lang genug für vollen 160-Zeichen-Snippet):
  ~14,0 KB (~467 B/Item), davon allein ~4,7 KB (34 %) der volle Snippet-Anteil.
Selbst der Floor liegt über dem Doppelten des geschätzten Ziels — 3 KB war bei diesem
Feldsatz kein erreichbarer Wert, kein Kalibrierungsfehler um ein bisschen. **Kalibrierter,
jetzt verbindlich getesteter Wert: <16 KB** (Marge über dem gemessenen Ceiling),
`test_search_listing_of_30_items_stays_within_calibrated_json_bound` pinnt Titel/Tags/Body/Uhr
fest (nicht abhängig davon, was `create()` gerade produziert — sonst liefe die Schwelle der
Fixture hinterher statt etwas zu prüfen).

**Befund für den Nikinger (keine eigenmächtige Änderung, nur Empfehlung):** Plan §2 behauptet
„Ein Listing über 30 Items muss in wenigen hundert Tokens passen" als Design-Eigenschaft der
Token-Sparmaßnahme (keine volle Bodies in `SearchResult`). Das stimmt in der Tendenz (Bodies
wären um Größenordnungen teurer), aber die konkrete Zahl hält nicht: 30 Items landen real bei
~2.500–3.500 Tokens (grobe 4-Zeichen/Token-Schätzung), nicht bei „ein paar hundert". Größter
Hebel, falls das zu grob ist: der 160-Zeichen-Snippet-Cap (34 % vom Ceiling) oder ein kleinerer
Default-`limit`. Beides wäre eine `ItemSummary`/API-Entscheidung, also Nikinger-Sache — aktueller
Feldsatz bleibt unverändert, bis das entschieden ist.

**Sortierung verbindlich gemacht:** `test_search_sort_order_locks_status_then_due_then_updated_desc`
pinnt die seit Step 4 als „Platzhalter" markierte Reihenfolge fest — empirisch verifiziert:
Test bricht, wenn das `updated`-Tiebreak-Vorzeichen kippt (Regressionsschutz bestätigt, nicht
nur angenommen).

**Verifiziert (live):** `pytest -v` → 61/61 grün (2 neue in `test_store.py`, kein neues Modul).
`git diff` bestätigt: nur `tests/test_store.py` geändert, `storage/` unangetastet.

**Nächster Schritt (konkret):** Step 7 — `scripts/space_cli.py`: `create`, `list`, `search`,
`show`, `update`, `archive`, `reindex`. Logging → stderr, Ausgabe wahlweise Text oder `--json`
auf stdout — das ist die erste Stelle, an der `ItemSummary`/`SearchResult` tatsächlich zu JSON
serialisiert werden (Step 6 hat das nur test-lokal nachgebaut, keine öffentliche Serialisierung
eingeführt). Done-Kriterium: ein manueller Durchlauf legt einen Space an, erstellt drei Items,
findet sie wieder, provoziert bewusst einen Konflikt und zeigt ihn verständlich an — komplett
ohne Netz.

**Aufgelöst seit Step 0–4:** `flock` auf ext4 (Step 0) · `python-frontmatter`-Roundtrip →
verworfen, eigener Parser (Step 1) · Dateisystem-Ermittlung via `/proc/mounts` (Step 3) ·
`IndexError_` → `IndexCorrupt` (Step 4).

**Kleine Korrektur zum Plan:** „`pytest` grün mit null Tests" (Step 0, Done-when) bedeutet in der
Praxis `exit 5` („no tests ran"), nicht `exit 0` — pytest markiert eine leere Testsammlung so.
Kein Fehler, nur eine Präzisierung; siehe Modul-Status-Tabelle oben.

**Der vorherige Session-Block (Planungsabschluss) ist verbatim nach `SESSIONS_ARCHIVE.md`
gewandert — Rotationsregel, ab dieser (zweiten) Session aktiv.**
