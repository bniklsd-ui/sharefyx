---
status: live
purpose: Phase-Head Storage-Kern — Scope, harte Regeln, gelockte Entscheidungen, Modulstatus, aktueller Session-Handover
read-when: Arbeiten in phase1_storage/ — zuerst lesen, zusammen mit dem neuesten Session-stopped-Block
detail: L2
up: ../CLAUDE.md
down:
  - ../docs/concepts/phase1_storage_plan.md   # voller Plan, Entscheidungen A–H, Steps 0–7
  - CONTRACTS_ARCHIVE.md                      # §Geerbte Contracts, verbatim rotiert 2026-10-02
  - SESSIONS_ARCHIVE.md                       # ältere Session-Blöcke
updated: 2026-10-02 (**§Geerbte Contracts rotiert** — Gate/Z-Doku-Pflege P9-L: die 388 Zeilen / 31.422 B wandern **verbatim** nach `CONTRACTS_ARCHIVE.md` (neu, L3, mit L1-Card), der Head trägt nur noch den Öffnungs-Index + die Abschluss-Zusicherung. **Nichts gestrichen** — Roundtrip-Gegenprobe vor dem Schreiben, danach byte-identisch gegengelesen; der Abschnittsname bleibt, weil `phase6_shares_plan.md` §, `PHASE7_CLOSEOUT_HANDOVER.md` §4, P8-M und die P9-Pläne wörtlich darauf verweisen. **47.570 B ~20 KB**, damit erstmals seit 2026-09-30 unter dem 40-KiB-Softcap. Reiner Doku-Schritt, kein `storage/`-Touch) | 2026-09-02 (achte Contract-Oeffnung geschlossen mit Phase-8-Step-Z -- P8-7 bestaetigt: 13 B2-index-Tests gruen, rebuild_index rekonstruiert item_links vollstaendig; Charakterisierung byte-identisch gruen; keine neunte angekuendigt; drei P8-Befunde aus der 200-Knoten/P8-24-Smoke-Sitzung (graph.js-ALPHA_DECAY / api.py-_graph_get-writable-Feld / graph.js-Knotenklick-SelectItem-Pfad) wurden NICHT in storage/ gebaut -- sie liegen in webui/ und sind dort Phase-9-Kandidaten, keine neue storage/-Oeffnung noetig) | 2026-08-28 (P7 Step Z: sechste und siebte Contract-Oeffnung geschlossen, keine achte angekuendigt -- jede P8-Arbeit an storage/ braucht eine neue benannte Oeffnung) | 2026-08-23 (Phase 7 Step 0: sechste Contract-Oeffnung angekuendigt -- acl.py-Schreibseite, Extraktion aus spacectl.py, P7-M-Lock-Regel) | 2026-08-20 (Phase 6.5 Step B1: fuenfte Contract-Oeffnung gebaut -- Bild-Assets in models/files/store.py, 150 Tests nach drei Advisor-Fixes (Lock-Disziplin, created-Konsistenz, Sniff-Kosten), Zaehlkorrektur 126->130 vor Step B1)
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
| 14 | Sechste, benannte Contract-Öffnung (angekündigt P7 Step 0, siehe „Geerbte Contracts"): `acl.py` bekommt eine Schreibseite — `read_share_file()`/`write_share_file()`/`add_member()`/`remove_member()`/`create_space()`/`remove_space_dir()`/`spaces_referencing()`/`AclWriteError` — byte-identische Extraktion aus `spacectl.py` (P7-P), kein neues Verhalten | P7 Step C1 | ✅ **geschlossen mit dem Phase-7-Abschluss, 2026-08-28** | 24 (außerhalb dieses Pakets, `phase7_spaces_admin/tests/test_acl_write.py` — gleiche Kategorie wie Zeile 10s `phase6_shares/tests/test_acl.py`) |
| 15 | Siebte, benannte Contract-Öffnung, angekündigt **und** gebaut in derselben Sitzung (P7 Step C4, Advisor-Fund): `store.py :: move()` erlaubt jetzt einen reinen Space-Wechsel für bereits archivierte Items (ein echter Ordner-Wechsel bleibt verboten); `_write_item_file()` legt ein archiviertes Item dabei ins Ziel-`_archive/`, nicht an die Space-Wurzel (`files.item_path()` kennt `_archive/` nicht — dieselbe Sonderbehandlung, die `archive()` bisher exklusiv hatte). Zweiter Advisor-Fund: `create(status="archived")` (über MCP/REST erreichbar, `STATUS_VALUES` erlaubt `archived` für beide Typen seit P2 Step 2) lief bis dahin am selben Riegel vorbei — jetzt landet auch ein direkt als `archived` angelegtes Item sofort unter `_archive/`, ein mitgeschicktes `folder` wird verworfen, dieselbe Zurücksetzung wie in `archive()` | P7 Step C4 | ✅ **geschlossen mit dem Phase-7-Abschluss, 2026-08-28** — schließt eine strukturelle Lücke, die C4s Space-Entfernen sonst bei jedem Space mit `_archive/`-Inhalt (also jedem Space mit echter Historie) permanent blockiert hätte | 4 (in `test_store.py`: `test_move_of_archived_item_between_spaces_relocates_to_target_archive`, `test_move_of_archived_item_produces_exactly_one_commit`, `test_move_of_archived_item_rejects_a_real_folder_change` — ersetzt den bisherigen `test_move_of_archived_item_is_rejected` —, `test_create_with_status_archived_lands_directly_in_archive_and_drops_folder`) |

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

> **[2026-10-02, rotiert (Gate/Z-Doku-Pflege, P9-L)]** Der **vollständige Wortlaut** aller
> Contract-Öffnungen steht ab jetzt **verbatim** in `CONTRACTS_ARCHIVE.md` (L3, 📦) — 388 Zeilen /
> 31.422 B. Diese Datei trägt nur noch den Index und die Zusicherung, dass **nichts verloren** ist:
> jeder Absatz steht wortgleich im Archiv, in derselben Reihenfolge (die vierte Öffnung steht dort
> wie hier am Ende — das war schon so).
> **Warum rotiert und nicht gekürzt:** der Vermerk vom 2026-09-30 oben hat die Ursache benannt (zehn
> Öffnungen an einem Ort) und die Lösung festgelegt. Die Doc-Layers-Regel sagt dasselbe: Historie wird
> **verschoben**, nicht gestrichen.

**Die Zusicherung, unverändert:** Keine — dies ist die erste Phase. **Die in Plan §1/§2 definierten
Frontmatter-Felder und Store-Signaturen werden mit Abschluss dieser Phase zum Contract für P2.** Eine
Änderung daran nach Phasenabschluss ist eine Scope-Änderung und braucht eine Entscheidung, kein
Refactoring.

**Index der Öffnungen** — welche Zeile wo steht, steht im Archiv unter der jeweiligen Datums-
Überschrift. Keine Nummerierung hier, weil das Original zwei Zählweisen mischt (P2s drei Erweiterungen
heißen wörtlich „Drei ... Erweiterungen", P6 Step 1 danach „Dritte, benannte Contract-Öffnung"):

| Datum / Phase | Gegenstand | Stand |
|---|---|---|
| 2026-07-25, P1 | Abschluss-Contract: Frontmatter-Felder, `Item`/`SpaceInfo`/`ItemSummary`/`SearchResult`/`IndexStats`, `Store`-Signaturen | **geschlossen** |
| 2026-07-25, P2 Step 2 | drei einmalige, freigegebene Erweiterungen: `STATUS_VALUES`/`valid_statuses()`, `store.py :: space_of()`, `store.py :: get(..., repair_drift=)` — danach wieder zu | **geschlossen** |
| 2026-08-09 + 08-12, P6 Steps 1+4 | `Store.patch()` + `patch.py`; dann `VISIBILITY_VALUES`, `folder`/`visibility`/`share_*`, `acl.py` (`Grant`/`AclDecision`/`AclReader`), `acl_of()`, Index-Spalten, `INDEX_SCHEMA_VERSION = 2` | ✅ |
| 2026-08-17, P6 Step 7b | `Store.move(item_id, *, version, space=, folder=)` + `_cleanup_emptied_folders()` | ✅ |
| 2026-08-20, P6.5 Step 0/B1 | `AssetInfo` (`models.py`), `files.py`-Helfer (`new_asset_id()`, `asset_dir()`/`asset_path()`, `atomic_write_bytes()`), `store.py`-Asset-Methoden | ✅ |
| 2026-08-23 + 08-25, P7 C1/C2 | `acl.py`-Schreibseite (`create_space()`, `add_member()`, …) — byte-identische Extraktion aus `spacectl.py`, kein neues Verhalten | ✅ geschlossen 2026-08-28 |
| 2026-08-25, P7 C4 | `store.py :: move()`: Space-Wechsel für archivierte Items | ✅ geschlossen 2026-08-28 |
| 2026-09-01 + 09-02, P8 B1/Z | `storage/linkscan.py` + `index.py`-Tabelle `item_links` | ✅ geschlossen 2026-09-02 |
| 2026-09-30, P9 Step F | `doing` als Task-Status, `assignee` mit Index-Spalte, `INDEX_SCHEMA_VERSION` 3 → 4 (keine Migration) | 🟡 live (`v3.1.0`) |
| 2026-09-30, P9 Step G | `Store.trash(item_id, *, version)` — Löschen ist Verschieben nach `DATA_ROOT/._trash/<space>/`; **bewusst keine elfte Öffnung**, weil der Punkt-Präfix beide Scans ohne Eingriff überspringt | 🟡 live (`v3.1.0`) |
| 2026-10-02, P9 Block trace | `updated_by` in `Item`/`ItemSummary`, `actor: str = ""` an allen neun Store-Schreibmethoden, `history.commit(author=)`; **kein Index-Schema-Sprung** | 🟡 code-complete, Deploy `v3.1.1` steht aus |

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
