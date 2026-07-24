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
| 3 | `files.py` (atomarer Write, IDs, Slugs) | 2 | ⬜ | – |
| 4 | `index.py` (SQLite, Rebuild) | 3 | ⬜ | – |
| 5 | `store.py` (API, Lock, Versionierung) | 4 | ⬜ | – |
| 6 | `history.py` (Git) | 5 | ⬜ | – |
| 7 | Query-Layer in `store.py` | 6 | ⬜ | – |
| 8 | `scripts/space_cli.py` | 7 | ⬜ | – |

**Gesamt: 9 Tests.** Zielgröße am Phasenende: grob 60–90, davon mindestens die vier
Konflikt-Tests aus Step 4. Step 0 hat bewusst keine Tests (reines Skelett) — `pytest`
lief dort grün mit `exit 5` („no tests ran", nicht `exit 0`); das ist die korrekte
Bedeutung von „0 Tests", kein Fehlerzustand.

## Geerbte Contracts

Keine — dies ist die erste Phase. **Die in Plan §1/§2 definierten Frontmatter-Felder und
Store-Signaturen werden mit Abschluss dieser Phase zum Contract für P2.** Eine Änderung daran
nach Phasenabschluss ist eine Scope-Änderung und braucht eine Entscheidung, kein Refactoring.

---

## Session stopped — 2026-07-24 (Step 0 + Step 1 abgeschlossen)

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

**Nächster Schritt (konkret):** Step 2 — `storage/files.py`: ID-Erzeugung (`itm_` + 8 Hex aus
`secrets.token_hex(4)`), Slugify mit korrekter Umlaut-Transliteration (`ä→ae` etc.),
Pfadauflösung `<id>__<slug>.md`, atomarer Write (tmp + `os.replace` + Verzeichnis-`fsync`),
Umbenennung bei Titeländerung. Done-Kriterium laut Plan: Test schreibt 200 Items, eine
`kill -9`-Simulation per Monkeypatch zwischen tmp und `replace` hinterlässt keine halb
geschriebene Zieldatei, Slug-Kollisionen überschreiben nichts (ID im Namen garantiert
Eindeutigkeit).

**Offene `[VERIFY]` in diesem Track:** Namenskollision `IndexError_` (Plan §1, noch nicht
gebraucht — `errors.py` existiert erst ab dem Step, der den ersten Fehlertyp braucht) · Methode
zur Dateisystem-Ermittlung unter Ubuntu (Plan Step 3) · Snippet-/Listing-Größenziel 3 KB (Plan
Step 6).
**Aufgelöst seit Step 0/1:** `flock` auf ext4 (Step 0) · `python-frontmatter`-Roundtrip → verworfen,
eigener Parser (Step 1, siehe oben).

**Kleine Korrektur zum Plan:** „`pytest` grün mit null Tests" (Step 0, Done-when) bedeutet in der
Praxis `exit 5` („no tests ran"), nicht `exit 0` — pytest markiert eine leere Testsammlung so.
Kein Fehler, nur eine Präzisierung; siehe Modul-Status-Tabelle oben.

**Der vorherige Session-Block (Planungsabschluss) ist verbatim nach `SESSIONS_ARCHIVE.md`
gewandert — Rotationsregel, ab dieser (zweiten) Session aktiv.**
