---
status: archive
purpose: L3-Archiv des Abschnitts „Geerbte Contracts" aus `phase1_storage/CLAUDE.md` — alle benannten P1-Contract-Öffnungen, verbatim, in der Reihenfolge des Originals
read-when: nur wenn ein P1-Contract geändert werden soll oder die Herkunft einer Öffnung rekonstruiert werden muss — welche Öffnung es ist, steht im Index des Phase-Head
detail: L3
up: ./CLAUDE.md
down:
updated: 2026-10-02 (erste Rotation, Gate/Z-Doku-Pflege P9-L — 388 Zeilen / 31.422 B verbatim aus dem Head in dieses Archiv verschoben; der Head trägt nur noch Index + Zusicherung. **Nichts gestrichen:** die Reihenfolge ist die des Originals, die vierte Öffnung steht darin weiterhin am Ende)
---
# Geerbte Contracts (verbatim aus `CLAUDE.md`)

> **Rotiert am 2026-10-02, Gate/Z-Doku-Pflege (P9-L).** Alles unter der Überschrift ist **wortgleich**
> aus `phase1_storage/CLAUDE.md` §„Geerbte Contracts" hierher verschoben, nicht abgetippt und nichts
> gekürzt — inklusive der Absätze, die eine Zusicherung über den Contract enthalten. Der Phase-Head
> behält den Abschnittsnamen (darauf verweisen `docs/concepts/phase6_shares_plan.md` §,
> `PHASE7_CLOSEOUT_HANDOVER.md` §4, P8-M und P9-Planverweise wörtlich), dort aber nur noch den Index
> der Öffnungen und den Abschluss-Satz. Grund der Rotation steht im Head und in `docs/INDEX.md`.

## Geerbte Contracts

> **[2026-09-30, benannt statt versteckt (P8-P)]** Diese Datei steht bei **42.638 B** und damit
> **1.678 B über dem 40-KiB-Softcap** — verursacht von den P9-Einträgen (F + G, zusammen ~4,3 KB),
> nicht von einem Versehen. Siehe `docs/INDEX.md` (gleiche Meldung, `doc_health.py` prüft sie).
> **Die Lösung ist eine Rotation, kein weiteres Kürzen:** neun Contract-Öffnungen an einem Ort sind
> die Ursache, und die zwei ältesten (P2/P6) sind längst geschlossen und stehen in
> `SESSIONS_ARCHIVE.md`. Das gehört in Step Z (P9-L) — dieselbe Art Arbeit wie die
> `docs/INDEX.md`-Rotation. **Bis dahin wird hier nichts gestrichen, was eine Zusicherung über den
> Contract entfernt.**


Keine — dies ist die erste Phase. **Die in Plan §1/§2 definierten Frontmatter-Felder und
Store-Signaturen werden mit Abschluss dieser Phase zum Contract für P2.** Eine Änderung daran
nach Phasenabschluss ist eine Scope-Änderung und braucht eine Entscheidung, kein Refactoring.

**[2026-07-25, P2 Step 2] Drei vom Nikinger freigegebene, einmalige Contract-Erweiterungen**
(`docs/concepts/phase2_mcp_plan.md` §0.4 Punkt L, §4 Step 2) — danach ist der Contract wieder
zu, keine stille Abweichung:
- `models.py`: `STATUS_VALUES`/`valid_statuses()` — Statusvokabular je `type`
  (`note`: `active`/`archived`; `task`: `open`/`doing`/`done`/`archived` — **`doing` kam am
  2026-09-30 mit P9 Step F hinzu, der Satz von 2026-07-25 nannte nur `open`/`done`/`archived`**).
  `store.py :: create()`/
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

**[2026-08-28, P7 Step Z] Öffnungen 6 und 7 geschlossen — keine achte angekündigt.** Phase 7 ist
formal abgeschlossen (✅ live-verifiziert, 22 von 24 Abnahmezeilen bestanden, zwei benannte
Defekte an Phase 8 vererbt — `docs/concepts/PHASE7_CLOSEOUT_HANDOVER.md`). Damit sind die
**sechste** Öffnung (`acl.py`-Schreibseite, P7 Step C1) und die **siebte** (`store.move()` für
archivierte Items, P7 Step C4) datiert **geschlossen**; die Modul-Status-Zeilen 14 und 15 oben
sind entsprechend nachgezogen. **Anders als bei den drei vorherigen Schließungen wird hier keine
Folgeöffnung mitgenannt** — es gibt zum Zeitpunkt dieses Satzes keinen Plan für Phase 8 und damit
keine angekündigte achte Öffnung. **Für die nächste Phase heißt das: jede Arbeit an `storage/`
braucht eine neue, benannte Öffnung mit eigenem Absatz hier, kein stiller Anbau.** Die
Charakterisierungstests (P6-D/P7-C, `phase6_shares/tests/test_characterization.py`, drei Golden
Files) blieben über beide Öffnungen byte-identisch grün und bleiben die Bedingung jedes künftigen
`storage/`-Umbaus.

**[2026-09-01, Phase 8 Block B Step B1] Achte P1-Contract-Öffnung angekündigt** (vor Code,
Disziplin der Vorgänger-Öffnungen 3–7): `storage/linkscan.py` (neu) trägt `ITEM_REF_RE` und
`extract_item_refs(body) -> list[str]` (rein, kein I/O, deterministisch); `storage/index.py`
bekommt im Schema-Block die Tabelle `item_links` (`src_id`, `dst_id`, `kind` ∈ `frontmatter`/
`body`, PRIMARY KEY `(src_id, dst_id, kind)`) + Index `idx_item_links_dst` + neue Funktion
`replace_item_links(conn, src_id, rows)`; `storage/store.py` ruft `replace_item_links()` an
jedem Schreibpfad, der heute `upsert_item()` ruft (create/update/patch/append/move/archive,
V82), und stellt `Store.links_all() -> list[tuple[str, str, str]]` (src, dst, kind) als neue
Lesemethode bereit. **Außerhalb des Scopes dieser Öffnung:** `models.py`, `frontmatter.py`,
`files.py`, `patch.py`, `acl.py`, `history.py` bleiben unangetastet — das Dateiformat ändert
sich nicht, das Frontmatter-Schema nicht, kein neues Feld, keine neue `Item`-Property;
Charakterisierung (P6-D/P7-C, `phase6_shares/tests/test_characterization.py`, drei Golden
Files) muss vor und nach dieser Öffnung byte-identisch grün bleiben, das ist die
Bedingung — Plan §3 P8-M, dokumentiert in `docs/concepts/phase8_ui_graph_plan.md` §3 + §0.4
Tabu-Liste. Die Schließung dieser Öffnung folgt mit dem Phase-8-Abschluss (Step Z, Plan §6),
nicht mit dem ersten Teilschritt — dieselbe Disziplin wie bei 6 und 7.

**[2026-09-01, Phase 8 Block B Deploy] Achte Öffnung bleibt ANGEKÜNDIGT nach
Deploy.** Block B (B1 `linkscan.py` + 15 Tests, B2 `item_links`-Tabelle +
alle 6 Schreibpfade + 22 Tests, B3 `GET /api/v1/graph` + 8 Tests, B4
UI-Wiring `#item/`-Nav + Link-Picker) ist seit `main@007b73d` live
verifiziert (`releases/20260901T103944.634877Z`, Health-Gate 3/3 grün,
Versionsbadge v2.2.3, Tabu-Diff §0.4 leer, Charakterisierungstests
bleiben byte-identisch grün). Die formale „Öffnung geschlossen"-Notiz
kommt weiterhin mit Phase-8-Step-Z — die achte Öffnung umfasst die
gesamte Phase 8, und die Schließungsbedingung ist nicht der Block-B-
Deploy, sondern die byte-identische Charakterisierung über ALLE
`storage/`-Änderungen der Phase. Aktueller Stand: B1/B2 fertig +
live, keine weiteren `storage/`-Änderungen in Block C/D geplant —
Schließung wird mit dem Phase-8-Abschluss erfolgen, nicht früher.

**[2026-09-02, Phase 8 Step Z] Achte P1-Contract-Öffnung geschlossen** (gemäß der
Anweisung in `docs/concepts/phase8_ui_graph_plan.md` §9.6: "Schließung folgt im selben
Commit wie §9: datierte Notiz hier mit dem Eintrag ‚Achte Öffnung geschlossen mit
Phase-8-Step-Z'"). **Schließungsbeleg:** `rebuild_index()` rekonstruiert `item_links`
vollständig aus den `.md`-Dateien — 13 `phase1_storage/tests/test_index.py`-Tests
(B2-Indexblock) sind grün, `test_characterization.py` (P6-D/P7-C) bleibt über die
gesamte Phase 8 byte-identisch grün. Hard Rule 2 gehalten: der Index ist jederzeit aus
den Dateien rekonstruierbar. **Schließungsbedingung über ALLE Phase-8-`storage/`-
Änderungen erfüllt:** es gab in Block C/D keine weiteren `storage/`-Edits — Phase 8 hat
ausschließlich in `mcpserver/`/`webui/`/`scripts/` und in `phase5_ui/webui/static/js/`
gearbeitet. Damit ist die achte Öffnung mit B1 + B2 vollständig abgedeckt. **Drei
Phase-8-Befunde aus der 200-Knoten- und E2E-Smoke-Sitzung** (`graph.js` ALPHA_DECAY /
`api.py :: _graph_get` `writable`-Feld / `graph.js` Klick-nach-Item-Pfad) liegen in
`phase5_ui/webui/`, nicht in `storage/`. **Keine neunte Öffnung nötig** — die Befunde
gehören in eine P9-Planung, nicht in einen `storage/`-Umbau. Die P1-Contract-Disziplin
der Vorgänger-Öffnungen 3–7 gilt weiter: jede künftige P9-Arbeit an `storage/` braucht
eine neue, benannte Öffnung mit eigenem Absatz hier, kein stiller Anbau.

**[2026-09-30, P9 Step F] Neunte, benannte P1-Contract-Öffnung gebaut** — angekündigt am
2026-09-19 mit Plan und Datum (P9-G, `docs/concepts/phase9_hardening_plan.md` §8), also
**abgearbeitet, nicht entdeckt**. Umfang am Diff gemessen: **18 Hunks in genau drei Dateien**
(`models.py` 4, `store.py` 8, `index.py` 6) — die enge Probe §8.7 erfüllt, die sechs Hartpfade
`acl/linkscan/patch/files/history/frontmatter` unberührt.
- `models.py`: `STATUS_VALUES["task"]` → `{open, doing, done, archived}`, **`note` bleibt
  `{active, archived}`** (eine Notiz kennt keine Arbeit); `Item`/`ItemSummary` bekommen
  `assignee: str = ""`.
- `store.py`: `"assignee"` in `_KNOWN_FIELDS` (sonst `Item.extra`); `create()` poppt und reicht
  durch; `_item_to_text()` schreibt **nur bei nicht-leer** (Muster `visibility`/`share_*` — sonst
  bekäme jeder Altbestand-Item ein stilles `assignee: ""`); neu `_coerce_assignee()`.
- `index.py`: Spalte `assignee TEXT NOT NULL DEFAULT ''`, `INDEX_SCHEMA_VERSION` **3 → 4**,
  `row_from_file()` plus **alle drei** Statement-Teile von `_upsert_no_commit()`. **Keine
  Migration** — `connect()` verwirft einen Index mit abweichender `user_version`,
  `Store.__init__` ruft `rebuild_index()`. Hard Rule 2 in Aktion, und der Grund, warum diese
  Öffnung billig ist.

**V160 (2026-09-30, Nikinger): `assignee` ist ein Space-Name, ohne Validierung** — eine Prüfung
gegen die Space-Liste wäre eine **zweite**, nicht angekündigte Öffnung (der Schreibpfad müsste
den Space auflösen, mit dem ein Item in einem fremden Space belegt sein könnte).

**Drei Stellen, die der Plan nicht nannte und ohne die es nicht funktioniert hätte:** `_summary()`
(**F10** — ohne sie stünde in jeder Trefferliste dauerhaft `""`, F3 wäre ein totes Feld),
`update()` (**F11** — ohne sie wanderte der Wert über den `else`-Zweig nach `Item.extra`: er landete
**trotzdem** in der Datei, `item.assignee` bliebe auf `""` und F6 feuerte nie; der am leichtesten
übersehene Fall, weil „es funktioniert" hier kein Beweis ist) und `_coerce_assignee()` (Typprüfung
einmal im Kern statt in drei Adaptern).

23 neue Tests (17 `test_step_f_schema.py`, 4 `test_tools.py`, 2 `test_api.py`), `pytest`
1039 → **1062**. **Zwei Alt-Tests mussten mitgezogen werden:** `test_index.py::
test_upsert_get_delete_roundtrip` (handgebaute Zeile ohne den neuen Key — benannte Parameter
schlagen **laut** fehl, was richtig ist) und der kalibrierte JSON-Bound, dessen Docstring eine
`ItemSummary`-Feldsatz-Änderung ausdrücklich für **nicht still** erklärt: gemessen **16.390 B**
gegen 16.300 B ohne das Feld (+16 B/Item), Band 12–16 KB → **13–18 KB** mit der alten Marge.

**Nicht in `storage/` behobener Befund:** `_BUCKETS` (`webui/api.py`) kennt `doing` nicht, und
`bucketFor()` vergleicht exakt — eine `doing`-Aufgabe fällt durch alle vier Eimer. Beide
Fix-Kandidaten sind Darstellungsentscheidungen und stehen als P10-Posten in
`docs/concepts/phase9_hardening_plan.md` §15; ein Wächter pinnt den Befund. Steht hier nur als
Eintrag, der **keinen** `storage/`-Code betrifft — die Herleitung wäre sonst an vier Stellen.

**[2026-09-30, P9 Step G] `Store.trash(item_id, *, version) -> None` — Löschen ist Verschieben,
kein `unlink`.** `version` ist **Pflicht** (Hard Rule 3). Ablauf wie `archive()`: beide Sperren →
`_reconcile_and_get_row` → Versionsprüfung → `files.move_file()` (`os.replace` + fsync auf Quelle
**und** Ziel) → `index.delete_item()` → Git-Commit `trash`. Autorisierung passiert **nicht** im
Store, wie überall — der Aufrufer prüft sie vorher (`webui/api.py :: _items_delete`, P9-K: nur
eigene Items).

**Ziel ist `DATA_ROOT/._trash/<space>/` (neue Modulkonstante `TRASH_DIR`) — gemessen, nicht
gewählt.** `rebuild_index()` rglobbt **ohne Skip** und `list_spaces()` führt jedes Nicht-Punkt-
Verzeichnis unter `DATA_ROOT` als Space: der im P9-Plan vorgesehene Ort **im** Space
(`<space>/_trash/`) ließ das gelöschte Item beim nächsten Neuaufbau **wieder auftauchen**
(`folder="_trash"`) und erzeugte zusätzlich einen **Phantom-Space** `['_trash', 'sp']`. Der
Punkt-Präfix auf `DATA_ROOT`-Ebene wird von beiden Scans bereits übersprungen (auch nach
`rebuild_index()` leer). So bleibt der P1-Fußabdruck **eine Datei**; die Alternative hätte
`index.py` **und** `files.py` gebraucht, also eine **zehnte** Öffnung ohne Ankündigung.

**Ausgehende `item_links` werden mitgeräumt, eingehende nicht** — `delete_item()` löscht nur
Zeilen mit dieser `src_id`; eine dangling `dst_id`-Zeile bleibt stehen und wird von `_graph_get`
weggefiltert (dort müssen **beide** Endpunkte in der sichtbaren Knotenmenge sein). Die
**Asset-Dateien** des Items wandern bewusst **nicht** mit — sie bleiben unerreichbar unter
`<space>/_assets/<item_id>/`, weil ein zweiter Move aus einer atomaren Operation zwei halbe
machte. Herleitung und Browserbeleg: `phase9_hardening/CLAUDE.md` (Block 2026-09-30) und die
datierte Korrekturnotiz in `docs/concepts/phase9_hardening_plan.md` §9.

**Ein hier NICHT behobener Befund:** `_BUCKETS` (`phase5_ui/webui/api.py`, außerhalb dieses
Pakets) kennt `doing` nicht, `bucketFor()` vergleicht exakt — eine `doing`-Aufgabe fällt durch
alle vier Eimer (derselbe Fund wie bei `done` im Phase-5-Step-7b). Beide Kandidaten sind
Darstellungsentscheidungen, die P9-P P10 zuteilt; vollständig mit beiden Kandidaten im Code
kommentiert, ein Wächter pinnt, dass der Befund nicht verschwindet, ohne dass P10 ihn behoben hat.

**[2026-10-02, P9 Block trace] Zehnte, benannte P1-Contract-Öffnung gebaut** — angekündigt am
2026-10-02 mit dem Mini-Plan und Datum (P9-AA–P9-AD,
`docs/concepts/phase9_hardening_block_trace_plan.md` §3), also **abgearbeitet, nicht entdeckt**.
Umfang am Diff gemessen: **genau drei Dateien** (`models.py` 2, `store.py` +`history.py`),
die enge Probe §0.4 erfüllt, die sechs Hartpfade `index/frontmatter/acl/files/patch/linkscan`
unberührt. **Kein Index-Schema-Sprung** — im Gegensatz zur neunten Öffnung ist das Feld
überhaupt nicht im Index, weil niemand danach filtert (P9-AA); die Trefferzeilen kommen aus
`_summary()` (F10-Pendant), also beim Deploy kein Neuaufbau.
- `models.py`: `Item`/`ItemSummary` bekommen `updated_by: str = ""`.
- `store.py`: `"updated_by"` in `_KNOWN_FIELDS` (sonst `Item.extra`, F4) **und** in
  `_SYSTEM_MANAGED_FIELDS` (sonst über `**fields`/`**changes` setzbar, P9-AA) · `_item_to_text()`
  schreibt **nur bei nicht-leer** (dritte Wiederholung des F6-Musters: ein leeres
  `updated_by:` wäre hier schlimmer als bei `assignee`, weil die UI es **liest**); `_summary()`
  reicht es durch; `create/update/append/patch/archive/move` nehmen `actor: str = ""` und setzen
  `updated_by` nur bei **nicht-leerem** Akteur (P9-AB: leer = unbekannt = **unverändert lassen**,
  lieber der alte, wahre Wert als ein erfundener) · `_write_item_file()`/`_commit()` reichen den
  Akteur an `history.commit(author=)` durch, ebenso die direkten `_commit`-Aufrufe in `archive`,
  `put_asset`, `delete_asset`, `trash`. **Drift-Commits bekommen bewusst keinen** — eine
  Fremdänderung hat per Definition keinen Akteur durch diesen Prozess.
- `history.py`: `commit(data_root, message, author="")` setzt `--author "<name> <name@sharefyx.invalid>"`;
  der **Committer** bleibt `Space Server` (P9-AC). Ein Name mit `<`, `>` oder Zeilenumbruch ⇒
  kein `--author`, `logger.warning`, der Commit läuft **trotzdem** — `history.py`s Vertrag
  („ein Write scheitert nie an Git") hat Vorrang vor einer hübscheren Zuschreibung.

**Drei Entscheidungen, die am Code auffielen und nicht im Plan standen (alle datiert im Code):**
1. **`actor` ist ein reservierter Name in `create`/`update`.** `update(id, version=1, actor="x")`
   setzt `updated_by` und legt **kein** Feld `actor` in die Datei. P9-AD hat die Optionalität
   bewusst gewählt (294 Testaufrufe), damit ist der Preis bekannt; ein Item mit einem echten
   Frontmatter-Feld `actor` kann so nicht mehr geschrieben werden. Kein solches Feld existiert.
2. **`put_asset`/`delete_asset` setzen `updated_by` nicht**, nur den Git-Autor — ein Bild-Upload
   fasst den Item-Text nicht an. Ebenso `trash`: die Datei wird verschoben, nicht geschrieben, im
   Papierkorb steht der letzte *Editor*, der Löschende steht im Git-Log. **So gewollt, nicht
   nachbessern.**
3. **Ein Altbestand-Item ohne Feld bekommt auch durch einen schreibenden Zugriff keine leere
   Zeile** — dieselbe Eigenschaft wie P9-42/F6, hier mit eigener Test-Absicherung (`test_store.py`).

**Test-Trennung, die die Fixture-Lage erzwang:** T1–T5 liegen in `test_store.py`, T6 in
`test_history.py`, die **strukturellen** Wächter (AST über *jedes* Nicht-Test-Modul in
`mcpserver/` und `webui/`, plus die Rolle von `_SYSTEM_MANAGED_FIELDS`) in
`phase9_hardening/tests/test_trace_block.py`, T8/T9 in `test_tools.py` (dort wohnen die
MCP-Fixtures), T10 in `test_api.py`, T11 in `test_static_routes.py`. `pytest` **1128 → 1152** (24 neu).
**Ein bestehender Wächter wurde datiert zugeschnitten, nicht entfernt:**
`test_step_f_schema.py::test_the_editor_status_dropdown_reads_the_vocabulary` verbot previously
jedes Vorkommen von `assignee|doing` in `editor.js` — P9-Z verlangt genau das Gegenteil, weil
sich „bei `doing` füllen" nicht ohne den Namen des Statuswerts ausdrücken lässt. Jetzt gilt:
keine abgetippte Vokabular-*Liste*, aber genau **eine** benannte Verzweigung mit Leer-Prüfung.

**Nicht in `storage/` gebaut, mit Argument:** eine Verlaufsansicht („wer hat wann was geändert",
aus `git log`) — P9-Y, vom Nikinger nicht gewählt, P10-Kandidat. `created_by` wäre ein zweites
Feld für eine Angabe, die bereits im ersten Git-Commit **des Items** als Autor steht.

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

