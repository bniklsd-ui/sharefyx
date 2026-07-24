---
status: plan (ausführungsreif)
purpose: Phase 1 — Storage-Kern. Entscheidungen A–H gelockt, Steps 0–7 sequenziert, Namen fixiert. Direkt an Claude Code übergebbar.
read-when: Ausführung von Phase 1; NICHT bei Session-Start anderer Phasen
detail: L2
up: ../../phase1_storage/CLAUDE.md
updated: 2026-07-24
---
# Phase 1 — Storage-Kern
## Implementierungsplan für Claude Code

> **Author:** Browser-Planungssession, 2026-07-24.
> **Audience:** Claude Code. Dieser Plan ist ausführungsreif — Entscheidungen sind gelockt,
> Schritte sequenziert, Namen fixiert. Nichts hier muss neu hergeleitet werden.
> **Drift-Konvention:** Alles, was gegen den echten Repo-Stand oder eine externe Bibliothek
> geprüft werden muss, ist **`[VERIFY]`** markiert — bei Ausführung verifizieren, nie als
> gesichert übernehmen. Der Planungschat hatte **kein** Repo — es existiert noch keines.
> **Doc-Layers-Konvention gilt:** jede neue `.md` bekommt eine L1-Header-Card (≤15 Zeilen YAML)
> und einen One-Liner in `docs/INDEX.md` **im selben Commit**.

---

## §0 Mission + gelockte Entscheidungen

**Mission P1:** Ein Datenmodell, das ein Mensch im Texteditor und mehrere Claude-Instanzen über
Tools **gleichzeitig** benutzen können, ohne dass jemand still Daten verliert. Phase 1 enthält
**kein Netzwerk, kein MCP, keine Auth** — sie ist vollständig offline testbar. Das ist Absicht:
der Konfliktfall ist der schwierige Teil, und er lässt sich nur ohne Transportschicht sauber
beweisen.

**Bauprinzip-Erinnerung:** Der Server ist dumm. P1 enthält **keine AI**, keine Embeddings, keine
semantische Suche. Wer hier ein LLM einbauen will → stop.

### Gelockte Entscheidungen (A–H)

| # | Thema | Festlegung |
|---|---|---|
| **A** | Source of Truth | **Markdown-Datei mit YAML-Frontmatter** auf der Platte. SQLite ist ein **derivierter Index**, jederzeit löschbar und vollständig rekonstruierbar. Nie umgekehrt. |
| **B** | Ein Item-Typ | Genau **eine** Entität `Item`. `type: note \| task` ist ein Feld, keine zweite Tabelle, keine Subklasse. Eine Aufgabe ist ein Item mit `status` und optionalem `due`. |
| **C** | Optimistic Locking | `version: int`, beginnt bei 1, +1 je erfolgreichem Write. Jeder Write verlangt die gelesene Version. Mismatch → `ConflictError`, der das **aktuelle** Item mitführt (der Client kann so ohne Zusatz-Roundtrip mergen). **Kein Last-Write-Wins.** |
| **D** | Externe Edits | Der Mensch editiert Dateien direkt und bumpt `version` **nicht**. Erkennung über `(mtime, size, sha256)` im Index: Abweichung → Datei ist Wahrheit, Item wird reindiziert und `version` +1 gesetzt. Ein danach eintreffender Write mit alter Version läuft korrekt in `ConflictError`. |
| **E** | Atomarität + Historie | Write = Temp-Datei im selben Verzeichnis → `os.replace` → `fsync` auf dem Verzeichnis. Danach **ein Git-Commit** im Datenverzeichnis (`git -C <data> commit`), Message `<op> <item_id> [<space>]`. Damit ist kein Write unwiederbringlich. Git-Fehler sind **best-effort, nie fatal** für den Write — aber `logger.critical`. |
| **F** | IDs & Dateinamen | `id = "itm_" + 8 hex` (aus `secrets.token_hex(4)`), **unveränderlich**, steht im Frontmatter **und** als Präfix im Dateinamen: `<id>__<slug>.md`. Der Slug darf sich bei Titeländerung ändern, die ID nie. Lookup **immer** über ID/Index, **nie** über Dateinamen-Parsing. |
| **G** | Index-Rebuild | `rebuild_index()` ist ein öffentliches Kommando **und** läuft beim Start. Ein korrupter oder fehlender Index ist **nie** fatal: löschen, neu bauen, weiter. Ein Index-Fehler darf niemals eine Datei anfassen. |
| **H** | Kein Löschen | Es gibt **keine** Delete-Operation im Kern-API. `status: archived` + Verschieben nach `<space>/_archive/`. Hard Delete ist ein separates Operator-Skript (`scripts/purge.py`), das explizit bestätigt werden muss — und wird **nie** als Tool exponiert (P2 Scope-Lock). |

---

## §1 Datenmodell (Contract — spätere Phasen hängen daran)

### Verzeichnislayout

```
<DATA_ROOT>/                 # git-Repository, NICHT das Code-Repo
  nikinger/                  # ein Space = ein Verzeichnis
    itm_a1b2c3d4__mcp-server-geruest.md
    itm_9f8e7d6c__einkaufsliste.md
    _archive/
      itm_00112233__alter-kram.md
  kollege/
    ...
  .index.sqlite3             # derivativ, in .gitignore
```

### Frontmatter-Schema

```markdown
---
id: itm_a1b2c3d4          # str, unveränderlich, Pflicht
space: nikinger           # str, Pflicht, == Verzeichnisname
type: task                # "note" | "task", Pflicht
title: MCP-Server Grundgerüst
status: open              # note: "active"|"archived"; task: "open"|"done"|"archived"
due: 2026-08-02           # ISO date oder datetime, optional (nur sinnvoll bei type=task)
tags: [infra, mcp]        # list[str], optional, default []
links: [itm_9f8e7d6c]     # list[item-id], optional, default [] — der rudimentäre Graph
created: 2026-07-24T18:20:00Z
updated: 2026-07-24T18:20:00Z
version: 4                # int, ≥1
---
Body als Markdown. Alles unterhalb des zweiten `---`.
```

**Warum diese Felder und keine mehr:** jedes Frontmatter-Feld wird bei *jedem* Listing über
*alle* Treffer übertragen. Ein Feld mehr kostet Tokens in jeder Suche, für immer. Zusatzfelder
kommen nur mit einer expliziten Entscheidung dazu.

**Unbekannte Frontmatter-Felder werden beim Lesen bewahrt und beim Schreiben zurückgeschrieben**
(Round-Trip-Treue). Ein Mensch, der ein eigenes Feld ergänzt, darf es nicht durch einen
Claude-Write verlieren.

### Fehlertypen (`storage/errors.py`)

`SpaceError` (Basis) · `ItemNotFound` · `SpaceNotFound` · `ConflictError` (trägt `current: Item`)
· `ValidationError` · `IndexError_` `[VERIFY: Name kollidiert mit Builtin — beim Bau final
festlegen, z.B. IndexCorrupt]`

---

## §2 Öffentliche API des Pakets `storage`

Diese Signaturen sind der **Contract für Phase 2**. Änderungen daran sind eine Scope-Änderung,
kein Implementierungsdetail.

```python
class Store:
    def __init__(self, data_root: Path, *, now_fn=..., git: bool = True) -> None: ...

    def list_spaces(self) -> list[SpaceInfo]: ...
    def search(self, query: str | None = None, *, space: str | None = None,
               type: str | None = None, status: str | None = None,
               tag: str | None = None, due_before: date | None = None,
               limit: int = 50, offset: int = 0) -> SearchResult: ...
    def get(self, item_id: str) -> Item: ...
    def create(self, space: str, *, type: str, title: str, body: str = "",
               **fields) -> Item: ...
    def update(self, item_id: str, *, version: int, **changes) -> Item: ...
    def append(self, item_id: str, *, version: int, text: str) -> Item: ...
    def archive(self, item_id: str, *, version: int) -> Item: ...
    def rebuild_index(self) -> IndexStats: ...
```

**`SearchResult` trägt ausschließlich Frontmatter plus einen Snippet — niemals volle Bodies.**
Das ist die zentrale Token-Sparmaßnahme des gesamten Projekts und keine Optimierung, die man
später nachrüstet. Ein Listing über 30 Items muss in wenigen hundert Tokens passen.

**`now_fn` ist injiziert.** Kein `datetime.now()` irgendwo im Modulcode — Tests müssen
Zeitstempel deterministisch setzen können.

---

## §3 Nebenläufigkeit (der Kern der Phase)

Drei Schreiber sind gleichzeitig denkbar: zwei Claude-Instanzen und ein Mensch im Editor.

1. **Prozessweiter Write-Lock.** Alle Writes serialisieren über einen einzigen Lock. Der Server
   ist ein Prozess; das reicht und ist trivial korrekt.
2. **Datei-Lock gegen fremde Prozesse.** `fcntl.flock` auf `<DATA_ROOT>/.write.lock` für die
   Dauer einer Write-Transaktion.
   > **Aufgelöst 2026-07-24 (Nikinger):** Zielsystem ist eine VMware-VM mit Ubuntu, `DATA_ROOT`
   > liegt auf **ext4** (lokal). `flock` ist dort verlässlich — das ursprüngliche `[VERIFY]`
   > entfällt. **Bleibende Bedingung:** ext4 gilt nur, solange `DATA_ROOT` auf der virtuellen
   > Platte liegt. Ein VMware Shared Folder (`vmhgfs`), ein NFS-/SMB-Mount oder ein
   > Backup-Share als Datenverzeichnis kippt diese Annahme. Step 3 baut deshalb einen
   > Startup-Check ein, der das Dateisystem von `DATA_ROOT` prüft und bei allem außer
   > ext4/xfs/btrfs `logger.critical` schreibt — ein stiller Wechsel des Mounts darf nicht
   > unbemerkt bleiben.

   **Grenze, die nicht wegdiskutiert wird:** `flock` ist ein *advisory* Lock. Es wirkt nur
   zwischen Prozessen, die es ebenfalls nehmen — also zwischen Server-Instanzen und den eigenen
   Ops-Skripten. **Der Texteditor des Menschen nimmt es nicht.** Gegen den Menschen schützt
   ausschließlich Entscheidung D (Drift-Erkennung über Hash), nicht der Lock. Wer `flock` im
   Code als „jetzt kann niemand mehr dazwischenschreiben" kommentiert, hat es missverstanden.
3. **Read-Modify-Write ist immer:** Lock nehmen → Datei lesen → `version` vergleichen → bei
   Mismatch `ConflictError` → sonst schreiben, Index aktualisieren, committen → Lock freigeben.

**Nicht wegabstrahieren:** Der Mensch kann zwischen zwei Server-Reads speichern. Entscheidung D
fängt das ab, indem der Index den Dateizustand hasht statt ihm zu vertrauen.

---

## §4 Steps (sequenziell, je ein Commit)

Jeder Step endet mit grünem `pytest` (gemockt, kein Netz), aktualisierter Modul-Tabelle im
Phase-Head und aktualisiertem `## Session stopped`-Block — im **selben** Commit.

### Step 0 — Repo-Skelett
Verzeichnisstruktur, `pyproject.toml` (Paket `storage`, nested als `phase1_storage/storage/`,
Konvention wie im Trading-Bot-Repo), `scripts/dev_install.sh` (editable install, **kein
`sys.path`-Hack**), `.gitignore` (`.index.sqlite3`, `.venv`, `__pycache__`), leeres
`tests/`, `pytest.ini`.
**Done when:** `pip install -e .` läuft, `pytest` läuft grün (0 Tests), `from storage import __version__` importiert.

### Step 1 — Modelle + Frontmatter-Roundtrip
`storage/models.py` (`Item`, `SpaceInfo`, `SearchResult`, `IndexStats` — Dataclasses),
`storage/frontmatter.py` (parse/serialize). Bibliothek: `python-frontmatter` **oder** eigener
Parser über `PyYAML` `[VERIFY: python-frontmatter erhält unbekannte Felder und Feldreihenfolge
beim Roundtrip? Wenn nicht → eigener Parser, Entscheidung A/Round-Trip-Treue ist nicht verhandelbar]`.
**Done when:** Property-artiger Test: `serialize(parse(x)) == x` byte-identisch für ein Fixture
mit Umlauten, mehrzeiligem Body, unbekanntem Zusatzfeld und leerem Body.

### Step 2 — Datei-Store (Schreibpfad)
`storage/files.py`: ID-Erzeugung, Slugify (deutsche Umlaute korrekt: `ä→ae`), Pfadauflösung,
atomarer Write (tmp + `os.replace` + Verzeichnis-`fsync`), Umbenennung bei Titeländerung.
**Done when:** Test schreibt 200 Items, `kill -9`-Simulation via Monkeypatch zwischen tmp und
replace hinterlässt **keine** halb geschriebene Zieldatei; Slug-Kollisionen erzeugen keine
Überschreibung (ID im Namen garantiert Eindeutigkeit).

### Step 3 — SQLite-Index + Rebuild
`storage/index.py`: Schema (`items(id PK, space, type, title, status, due, tags_json,
links_json, created, updated, version, path, mtime, size, sha256)`), Insert/Update/Delete,
`rebuild_index()` (Verzeichnis scannen, alles neu). WAL-Modus. Zusätzlich der
**Startup-Dateisystem-Check** aus §3.2: Dateisystem von `DATA_ROOT` ermitteln
(`/proc/mounts` auswerten `[VERIFY: einfachste zuverlässige Methode unter Ubuntu — `os.statvfs`
liefert den Typ nicht direkt]`), bei allem außer `ext4`/`xfs`/`btrfs` → `logger.critical`,
aber **kein** Abbruch.
**Done when:** Index löschen → `rebuild_index()` → `search()` liefert identische Ergebnisse wie
vorher; ein manuell korrumpierter Index führt zu automatischem Rebuild statt zu einem Crash;
ein Test mit gemocktem Mount-Typ `nfs4` erzeugt genau eine `critical`-Zeile und läuft weiter.

### Step 4 — Versionierung + Konflikt (der eigentliche Beweis)
`storage/store.py`: die API aus §2, Write-Lock, Versionsprüfung, `ConflictError`,
Drift-Erkennung nach Entscheidung D.
**Done when — diese vier Tests müssen existieren und grün sein:**
1. Zwei sequenzielle `update` mit derselben Version → zweiter wirft `ConflictError` und der
   Fehler trägt das aktuelle Item.
2. Externer Edit der Datei (Test schreibt direkt) → nächster `get` liefert den neuen Inhalt mit
   erhöhter `version`, und ein `update` mit der *alten* Version wirft `ConflictError`.
3. Zwei parallele `update` aus zwei Threads → **genau einer** gewinnt, der andere wirft
   `ConflictError`; die Datei ist danach valide.
4. `update` auf ein archiviertes Item wirft, statt es stillschweigend zu reaktivieren.

### Step 5 — Git-Commit je Write
`storage/history.py`: Repo-Init falls nötig, Commit nach jedem erfolgreichen Write,
`git: bool`-Schalter für Tests. Fehler → `logger.critical`, **kein** Abbruch des Writes.
**Done when:** nach 3 Writes zeigt `git log` 3 Commits mit den erwarteten Messages; mit einem
kaputt gemachten Git-Repo laufen die Writes weiter durch und loggen `critical`.

### Step 6 — Query-Layer
`Store.search()` vollständig: Filter, Volltext über `title` + `tags` (**nicht** über Bodies —
das ist P2-Scope-fremd und kostet Index-Komplexität), Snippet-Erzeugung (erste ~160 Zeichen des
Bodies, an Wortgrenze), Paginierung, stabile Sortierung (`status` offen zuerst, dann `due`,
dann `updated` absteigend).
**Done when:** Ein Listing über 30 Items serialisiert zu <3 KB JSON; ein Test misst das und
schlägt fehl, wenn die Grenze reißt. `[VERIFY: 3 KB ist eine geschätzte Zielgröße — beim Bau
gegen echte Beispieldaten kalibrieren und den Wert hier korrigieren]`

### Step 7 — CLI als Beweis
`scripts/space_cli.py`: `create`, `list`, `search`, `show`, `update`, `archive`, `reindex`.
Logging → stderr, Ausgabe wahlweise Text oder `--json` auf stdout.
**Done when:** Ein manueller Durchlauf legt einen Space an, erstellt drei Items, findet sie
wieder, provoziert bewusst einen Konflikt und zeigt ihn verständlich an — komplett ohne Netz.

---

## §5 Was Phase 1 explizit NICHT tut

MCP · HTTP · Auth · Tunnel · UI · Volltextsuche über Bodies · Anhänge/Bilder · Cross-Space-Logik
(die Store-API kennt Spaces, aber keine Rechte — Autorisierung ist P2) · Löschen.

Wer während P1 anfängt, eines dieser Themen „schon mal vorzubereiten": **stop**. Der häufigste
Weg, eine Phase zu versenken, ist das Vorziehen der nächsten.

## §6 Bekannte Risiken dieser Phase

- **`DATA_ROOT` wandert auf ein anderes Dateisystem.** ext4 ist bestätigt (§3.2), aber die
  Annahme hält nur, solange niemand das Datenverzeichnis auf einen Shared Folder oder ein
  Netzlaufwerk legt — was beim Einrichten eines Backups naheliegt. Der Startup-Check aus
  Step 3 macht das sichtbar; ihn zu entfernen, weil er „nervt", wäre der Fehler.
- **`flock` schützt nicht gegen den Menschen.** Advisory Lock, siehe §3.2. Der einzige Schutz
  gegen einen parallel schreibenden Editor ist Entscheidung D. Wenn Step 4 Test 2 fehlschlägt,
  ist das kein Testproblem, sondern der Nachweis eines echten Datenverlustpfads.
- **Git-Repo-Wachstum.** Ein Commit je Write bei intensiver Nutzung erzeugt viele kleine
  Commits. Bei zwei Nutzern unkritisch; wird es je zum Problem, ist Squashing ein Ops-Thema,
  keine Änderung an Entscheidung E.
- **Round-Trip-Treue des Frontmatter-Parsers.** Siehe Step 1. Wenn die Bibliothek Felder
  umsortiert oder Kommentare frisst, verliert der Mensch bei jedem Claude-Write Formatierung.
  Das ist ein Blocker, kein Schönheitsfehler.
