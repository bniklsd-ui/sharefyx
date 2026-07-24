---
status: live
purpose: Phase-Head Storage-Kern — Scope, harte Regeln, gelockte Entscheidungen, Modulstatus, aktueller Session-Handover
read-when: Arbeiten in phase1_storage/ — zuerst lesen, zusammen mit dem neuesten Session-stopped-Block
detail: L2
up: ../CLAUDE.md
down:
  - ../docs/concepts/phase1_storage_plan.md   # voller Plan, Entscheidungen A–H, Steps 0–7
  - SESSIONS_ARCHIVE.md                       # ältere Session-Blöcke (entsteht bei der 2. Session)
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
| 1 | Repo-Skelett, `pyproject.toml`, dev_install | 0 | ⬜ | – |
| 2 | `models.py`, `frontmatter.py` | 1 | ⬜ | – |
| 3 | `files.py` (atomarer Write, IDs, Slugs) | 2 | ⬜ | – |
| 4 | `index.py` (SQLite, Rebuild) | 3 | ⬜ | – |
| 5 | `store.py` (API, Lock, Versionierung) | 4 | ⬜ | – |
| 6 | `history.py` (Git) | 5 | ⬜ | – |
| 7 | Query-Layer in `store.py` | 6 | ⬜ | – |
| 8 | `scripts/space_cli.py` | 7 | ⬜ | – |

**Gesamt: 0 Tests.** Zielgröße am Phasenende: grob 60–90, davon mindestens die vier
Konflikt-Tests aus Step 4.

## Geerbte Contracts

Keine — dies ist die erste Phase. **Die in Plan §1/§2 definierten Frontmatter-Felder und
Store-Signaturen werden mit Abschluss dieser Phase zum Contract für P2.** Eine Änderung daran
nach Phasenabschluss ist eine Scope-Änderung und braucht eine Entscheidung, kein Refactoring.

---

## Session stopped — 2026-07-24 (Planung abgeschlossen, Bau noch nicht gestartet)

**Ergebnis:** Die initialen Projektdokumente wurden in einer Browser-Planungssession erstellt
(Root-`CLAUDE.md`, `AGENTS.md`, `README.md`, `ROADMAP.md`, `docs/INDEX.md`, dieser Phase-Head,
`docs/concepts/phase1_storage_plan.md`). Rahmenentscheidungen R1–R6 sind in der Root-`CLAUDE.md`
gelockt, die Phase-1-Entscheidungen A–H im Plan. **Es existiert noch kein Code und kein Repo.**

**Nächster Schritt (konkret):** In Claude Code Step 0 des Plans ausführen — Repo initialisieren,
diese Dokumente als ersten Commit einchecken, `pyproject.toml` mit Paket `storage` nested als
`phase1_storage/storage/` anlegen, `scripts/dev_install.sh` schreiben, `pytest` grün mit null
Tests. Danach Step 1.

**Vor dem Start zu erledigen (Blocker für Step 0):**
1. ~~`docs/DOC_LAYERS_CONVENTION.md` kopieren~~ → **erledigt 2026-07-24**, byte-identisch
   übernommen, Index-Zeile gesetzt.
2. **`DATA_ROOT`-Pfad festlegen** (konkreter Pfad auf der VM). Die Dateisystemfrage ist
   beantwortet: VMware-VM mit Ubuntu, lokale virtuelle Platte → **ext4**, `flock` verlässlich
   (Plan §3.2, `[VERIFY]` aufgelöst). Offen bleibt nur, *welches* Verzeichnis es wird — und die
   Zusage, es nicht auf einen Shared Folder oder ein Backup-Share zu legen.

**Offene `[VERIFY]` in diesem Track:** Round-Trip-Treue von `python-frontmatter` (Plan Step 1) ·
Namenskollision `IndexError_` (Plan §1) · Methode zur Dateisystem-Ermittlung unter Ubuntu
(Plan Step 3) · Snippet-/Listing-Größenziel 3 KB (Plan Step 6).
**Aufgelöst:** `flock` auf dem Ziel-Dateisystem (ext4 bestätigt, 2026-07-24).

**Ehrlich geflaggt:** Dieser Plan wurde **ohne** Repo geschrieben — es gibt nichts, wogegen die
Contracts verifiziert werden konnten. Jede Signatur hier ist ein Vorschlag der Planung, kein
verifizierter Repo-Stand. Abweichungen beim Bau sind erwartbar und gehören als datierte
Korrekturnotiz in dieses Dokument, nicht in einen stillen Fix.
