---
status: live
purpose: Phase-Head Freigaben, Ordner, Werkzeug-Ergonomie — Scope, harte Regeln, Modulstatus, aktueller Session-Handover
read-when: Arbeiten in phase6_shares/ oder an den in P6-C genannten Dateien in storage/mcpserver/webui — zuerst lesen, zusammen mit dem neuesten Session-stopped-Block
detail: L2
up: ../CLAUDE.md
down:
  - ../docs/concepts/phase6_shares_plan.md         # voller Plan, Entscheidungen P6-A–P6-AC, Steps 0–10
  - ../docs/concepts/PHASE5_CLOSEOUT_HANDOVER.md   # Herkunft der offenen Entscheidungen §4.1–§4.6, [VERIFY]-Bilanz V27–V38
  - ./SESSIONS_ARCHIVE.md                          # Steps 0-3 verbatim (zwei Eintraege), L3, kein Softcap
updated: 2026-08-12 (Step 4 gebaut -- acl.py/folder/visibility/share_*, index-Rebuild-Fix, 669 Tests gruen)
---

# CLAUDE.md — Phase 6: Freigaben, Ordner, Werkzeug-Ergonomie (`phase6_shares/`)

> **Drei Dinge, in dieser Reihenfolge beweisbar:** eine arbeitende Claude-Instanz kann eine
> Drei-Zeilen-Korrektur an einem großen Dokument machen, ohne es komplett neu zu schreiben; ein
> Mensch entscheidet pro Item, wer es sieht, und es gibt Orte, an denen mehrere gemeinsam
> schreiben; das System verträgt einen dritten Nutzer, ohne dass jemand eine Codezeile ändert.
> **Quelle der Wahrheit ist der Code, nicht dieses Dokument.**
> Vollständiges Design + alle 29 gelockten Entscheidungen (P6-A–P6-AC) + Steps 0–10:
> `../docs/concepts/phase6_shares_plan.md`.

## Mission (zuerst lesen)

Diese Phase steht in **keiner** Roadmap-Zeile — sie ist ein QoS-Schnitt aus echtem Betrieb
(`patch_item`-Feedback einer arbeitenden Claude-Instanz, Nikinger-Meldung zu Subspaces/Freigaben).
Drei Blöcke, ein hartes Gate dazwischen: A = Werkzeuge/Betrieb/Update-Banner, B = Dateisystem
(Ordner, Sichtbarkeit, Freigaben, geteilte Spaces), C = Bilder. Unter Druck fällt zuerst C weg,
dann Bs geteilte Spaces — **nie Block A** (P6-A).

## Bauprinzip (Projekt-Kernprinzip)

„Der Server ist dumm." Phase 6 enthält KEINE AI, kein serverseitiges Rendern fremder Bodies,
kein serverseitiges Verarbeiten von Bildern (nur validieren + ausliefern, P5-Y gilt fort).

## Scope (Kurzform, Details: Plan §0.5 P6-A–P6-AC)

- **DRIN:** `patch_item` (punktuelle Textersetzung statt Komplett-Rewrite), Quittungen statt
  Volltext für alle Schreib-Tools, Purge-Erweiterung (O2), Update-Log + Banner, Sichtbarkeitsstufen
  (`private`/`human`), Item- und Ordner-/Space-Freigaben (`.share.yml`, `share_read`/`share_write`),
  echte Ordner (Tiefe ≤2), Migration des Bestands auf `private`, ein dritter Nutzer live bewiesen,
  Bild-Assets (PNG/JPEG/WebP/GIF, Magic Bytes, 5 MiB, kein HEIC), `app.js`-Split ohne Build-Step.
- **DRAUSSEN:** Löschen von Items (bleibt `status: archived`), FastMCP-4/CIMD/DPoP, Volltext-/
  semantische Suche, Realtime/WebSocket, Mobilversion, SQL-Filterung im Store, Rechteverwaltung
  über MCP-Tools, serverseitiges Bild-Rendering/EXIF-Strip, HEIC-Transkodierung.

## Harte Regeln dieser Phase (nicht verhandelbar)

- Alle Hard Rules aus Root-`CLAUDE.md` gelten unverändert.
- **P6-C — Berührungsfläche.** `storage/`, `mcpserver/tools.py`, `mcpserver/permissions.py` sind
  ausdrücklich **auf** — das hebt P5-B auf (P5s Akzeptanzkriterium 18 ist damit gegenstandslos).
  Weiterhin **tabu**: `mcpserver/asgi.py`, `authserver/{crypto,totp,passwords,resolver,flows}.py`
  (Ausnahme: additive Schema-3-Migration, P6-X).
- **P6-D — Ersatz für den Seam-Beweis.** Charakterisierungstests (Golden Files, byte-identisch)
  **vor** jedem Umbau an `storage/`. Kein Step-Abschluss in Block B ohne grüne Charakterisierung.
- **P6-G — kein inhaltsverankerter Merge.** `patch_item` respektiert `version`-Mismatch wie jeder
  andere Schreibpfad — `ConflictError`, ohne Ausnahme, auch wenn alle Anker noch eindeutig wären.
- **P6-M — Freigaben nur durch Menschen.** Kein MCP-Tool kann `share_read`/`share_write`/
  `visibility` setzen. `update_item` lehnt diese Felder mit `ValidationError` ab.
- **Rotationsregel ab Tag 1.** Dieser Head trägt **genau einen** Session-Block. Beim Anlegen
  eines neuen wandert der bisherige **verbatim** nach `SESSIONS_ARCHIVE.md` —
  `scripts/rotate_session_block.sh phase6_shares`, nie von Hand.
- **Commit ⇒ Note-Update, im selben Commit** (Hard Rule 8): Modul-Tabelle unten + Session-Block.

## Die gelockten Entscheidungen (P6-A – P6-AC) — Kurzform (Details: Plan §0.5)

Drei Blöcke, ein hartes Gate, Block A fällt nie (A) · kein neues Python-Paket, `phase6_shares/`
trägt nur `tests`/`scripts`/`CLAUDE.md` (B) · `storage`/`tools.py`/`permissions.py` auf, P5-B
aufgehoben (C) · Charakterisierungstests als Seam-Ersatz (D) · `patch_item(id, version, edits,
return_body=False)`, Liste sequenzieller `{old_text, new_text}` (E) · exakter Byte-Match, kein
Fuzzy (F) · `version`-Mismatch ⇒ `ConflictError`, kein Ausnahme-Merge (G) · alle vier Schreib-Tools
liefern eine kompakte Quittung statt Volltext, `return_body` holt ihn zurück (H) · kein
`section=`-Lesen, stattdessen `ui_budget.py` misst (I) · zwei Sichtbarkeitsstufen `private`/`human`
(J) · Item-Freigaben `share_read`/`share_write` (K) · Bestand wird `private`, Migrationsreport,
Update-Banner vor der Migration (L) · nur Menschen/UI/Re-Auth ändern Freigaben (M) · Re-Auth bei
Erweiterung, nicht bei Rücknahme (N) · `<untrusted_content>` gilt auch für geteilte Spaces (O) ·
`visibility: human` für die Agentenfläche vollständig nicht existent (P) · echte Verzeichnisse,
Tiefe ≤2, `folder` abgeleitet (Q) · Archiv bleibt flach (R) · SQL-Filterung draußen, aber gemessen
(S) · Mitgliedschaft in `.share.yml`, Datei nicht Datenbank (T) · Hard Rule 4 neu gefasst, nur
`create_item` bekommt `space=` (U) · geteilte Spaces per CLI verwaltet, UI gebaut aber abgeschaltet
(V) · dritter Nutzer live angelegt und wieder entfernt (W) · Update-Log strenges Format, `deploy.sh`
bricht ohne aktuellen Eintrag ab (X) · Assets unter `_assets/`, 5 MiB, relative Markdown-Links (Y) ·
PNG/JPEG/WebP/GIF über Magic Bytes, kein HEIC (Z) · Claude referenziert Assets, lädt nicht hoch,
löscht nicht (AA) · Drag & Drop mit Pflicht-Alternative (AB) · `app.js` in ES-Module aufgeteilt,
weiter ohne Build-Step (AC).

## Modul-Status

| # | Modul | Step | Status | Tests |
|---|---|---|---|---|
| 1 | Haushalt, Verifikationsdurchlauf (V39/V40/V41), Regeländerungen (§0.7 a/b/c), Phase-Head angelegt | 0 | ✅ **vollständig** | 0 (bewusst — reines Skelett, wie P1 Step 0; `phase6_shares/tests/conftest.py` leer angelegt) |
| 2 | Werkzeug-Ergonomie: `storage/patch.py` (neu), `storage/store.py :: patch()`, `mcpserver/receipts.py` (neu), siebtes Tool `patch_item`, `return_body` an allen vier Schreib-Tools, `update_item` lehnt `visibility`/`share_read`/`share_write` ab | 1 | ✅ **vollständig** — `mcp_smoke.py` 13/13 grün | +17 (5 `phase6_shares/tests/test_patch.py`, neue Datei + 5 `phase1_storage/tests/test_store.py` + 7 `phase2_mcp/tests/test_tools.py`); 593 gesamt |
| 3 | Betrieb: O2 (`authserver/store.py :: purge_expired()` räumt `token_families`/`clients` ab, zwei neue Retention-Konstanten), Client-Surface-Logging (`ua`-Feld auf `AccessLogASGI`, **V42 geschlossen, 2026-08-12** — Befund unten), `diagnose.sh` Prüfung 11 (Purge-Frische, INFO), `ui_budget.py :: _measure_latency()` (P6-I/P6-S, eigene `LatencyMetric`, kein Exit-Code-Einfluss) | 2 | ✅ **gebaut, ein Live-Teil beim Nikinger** — Gate-A→B-Punkt 3 (realer Purge-Lauf, `clients`-Zeilenzahl sinkt) bleibt live-Aufgabe, frühestens 2026-08-28 | +11 (8 `phase4_auth/tests/test_authserver_store.py` + 2 `phase2_mcp/tests/test_request_log.py` + 1 `phase2_mcp/tests/test_logging.py`); 604 gesamt |
| 4 | Update-Log und Banner: `authserver/store.py` Schema 3 (`users.seen_update_id`), `webui/updates.py` (neu, Parser), `webui/api.py` (+`GET /api/v1/updates`, +`POST /api/v1/updates/seen`), `webui/static/js/updates.js` (neu, Banner + Konto-Dialog-Link), `app.html`/`app.css`, `deploy.sh`-Gate (P6-X), `docs/UPDATE_LOG.md` (neu, erster Eintrag) | 3 | ✅ **gebaut, Gate-A→B-Punkt 4 vollständig live bestanden** (Banner-Hälfte 2026-08-10, Fabian-Hälfte 2026-08-11, siehe Session-Block) | +16 (3 `phase4_auth/tests/test_authserver_store.py` [258→261] + 7 `phase6_shares/tests/test_updates.py` [neue Datei] + 2 `phase5_ui/tests/test_api.py` + 3 `phase5_ui/tests/test_deploy_scripts.py` + 1 `phase5_ui/tests/test_static_routes.py`); 620 gesamt |
| 5 | Storage-Fundament (Block B): Charakterisierungstests + Goldens zuerst (P6-D), `storage/acl.py` (neu), `models.py`/`files.py`/`index.py`/`store.py`-Erweiterung (`folder`/`visibility`/`share_*`, `acl_of()`, `list_spaces()`), `index.py`-Rebuild-Fix (V46), zweiter Advisor-Durchlauf: `folder` jetzt pfadabgeleitet statt indexvertraut | 4 | ✅ **gebaut, 2026-08-12** — Charakterisierung vor+nach byte-identisch grün, DoD aus Plan §4 Step 4 erfüllt; noch nicht live geprüft (kein eigener Abnahmematrix-Punkt für diesen Step) | +36 `phase1_storage/` (1 `test_models.py` + 11 `test_files.py` + 4 `test_index.py` + 20 `test_store.py`) + 10 `phase6_shares/tests/test_acl.py`; 671 gesamt |

## Geerbte Contracts

**[2026-08-09, P6 Step 0] Dritte, benannte Öffnung des P1-Contracts** (Plan §1.4): `models.py`
bekommt `folder`/`visibility`/`share_read`/`share_write`, `store.py` bekommt `acl_of()`/`patch()`/
erweiterte `create()`/`update()`/`search()`/`list_spaces()`. Wird in Step 4 umgesetzt, hier nur
angekündigt — nach Phasenabschluss (Step 10) wieder geschlossen, siehe `phase1_storage/CLAUDE.md`.

---

## Session stopped — 2026-08-12 (Step 4 — Storage-Fundament, Block B)

**Nachtrag, 2026-08-12, elfter — Step 4 (Storage-Fundament) begonnen, Charakterisierung zuerst
(P6-D).** Vor dem Umbau: Advisor-Review des Ausführungsplans holte einen echten operativen Fund
zutage, der weder im Plan noch beim ersten Lesen auffiel — `Store.__init__` ruft `rebuild_index()`
nie auf, und `phase2_mcp/scripts/serve.py` (der reale Diensteinstieg) auch nicht; einziger
Aufrufer heute ist der manuelle `space_cli.py`-Befehl (per `grep -rn "rebuild_index"` bestätigt).
Ein `INDEX_SCHEMA_VERSION`-Sprung, der `index.connect()` beim nächsten echten Deploy zum
Verwerfen+Leer-Neuanlegen zwingt (wie heute schon bei Korruption), würde den Produktivindex leer
zurücklassen, bis jemand von Hand reindiziert — jeder `get()` würde bis dahin `ItemNotFound`
werfen. Wird beim eigentlichen `index.py`-Umbau geschlossen: `connect()` liefert künftig
`(conn, rebuilt: bool)`, `Store.__init__` ruft bei `rebuilt=True` sofort selbst
`self.rebuild_index()` — dieselbe „Index ist billig, Dateien sind die Wahrheit"-Logik aus Hard
Rule 2, nur diesmal auch tatsächlich verdrahtet.

**Charakterisierung gebaut:** `phase6_shares/tests/test_characterization.py` (neu) + drei Golden
Files unter `phase6_shares/tests/golden/` (`roundtrip_create.md`, `drift_repaired.md`,
`archived.md`), byte-verglichen. Vier Fälle, wie im Plan gefordert — die beiden reinen
Verhaltensfälle (`ConflictError.current`, die vier Commit-Messages `create|update|append|archive`)
laufen als direkte Assertions statt eigener Golden-Dateien, gleiche Testkategorie wie
`phase1_storage/tests/test_store.py` es für dieselben Fälle schon tut, kein eigener Dateiinhalt
zu vergleichen. Goldens einmalig gegen den unveränderten HEAD-Code erzeugt (Scratchpad-Skript,
nicht im Repo — gleiche Kategorie wie P5 Steps 10/11 und der jsdom-Durchlauf aus Step 3),
`generate_id()` und `now_fn` deterministisch gemacht (`monkeypatch`), sonst wäre jeder Lauf ein
anderes Golden. **Ein echter Stolperstein dabei:** die erste Capture-Runde benutzte einen
gemeinsamen ID-Zähler über alle vier Fälle hinweg (`itm_00000001`…`itm_00000004`) — die echten
pytest-Fixtures sind aber function-scoped, jeder Test bekommt seinen eigenen frischen Zähler bei
1. Golden gegen den echten Testlauf verglichen schlug prompt fehl (`itm_00000001` erwartet,
`itm_00000004` bekommen); zweite Capture-Runde mit einem frischen Zähler je Fall behoben. Zwei
echte, jetzt eingefrorene Warzen dokumentiert, nicht korrigiert: CRLF im Body bleibt beim
Schreiben roh erhalten (`atomic_write`s Textmodus übersetzt nur `\n`, unter POSIX ein No-Op),
`store.get().body` normalisiert es beim Lesen trotzdem auf `\n` (`read_text()` vs. `read_bytes()`
in `index.row_from_file`) — dieselbe Diskrepanz, die der Advisor vorab benannt hatte.
`slugify("Ümlaut Café")` würde `é` unverändert (klein) im Dateinamen belassen (`isalnum()` ist
Unicode-bewusst) — im Golden-Fall bewusst mit ASCII-Titel umgangen, um den Dateinamen
vorhersagbar zu halten; kein Fund, nur eine Beobachtung am Rand.

**Verifiziert:** `pytest -q` → **625 passed** (621 + 4 neue, exakt die vier
`test_characterization.py`-Fälle). Kein `storage/`-Produktivcode in diesem Commit angefasst — nur
Tests, Goldens, dieser Head. Das ist der P6-D-Ausgangspunkt: jeder künftige Diff in diesem Step
muss diese vier Goldens byte-identisch lassen, außer dort, wo der Plan `visibility`/`share_read`/
`share_write` ausdrücklich als Subjekt einer Änderung benennt (keiner der drei aktuellen Goldens
berührt diese Felder).

**Nachtrag, 2026-08-12, zwölfter — Step 4 (Storage-Fundament) fertig gebaut, in derselben Sitzung
fortgesetzt.** Reihenfolge wie angekündigt: `files.py` zuerst (liefert `RESERVED_DIR_NAMES`/
`MAX_FOLDER_DEPTH`/`validate_folder()`/`folder_from_path()`, `acl.py` braucht die Konstante),
dann `acl.py` (neu), `models.py`, `index.py`, zuletzt `store.py` — jeder Schritt einzeln gegen
`pytest` verifiziert, die drei Goldens aus dem letzten Nachtrag liefen nach jedem Schritt mit.

**`files.py`:** `item_path(..., folder="")`, `validate_folder()`, `folder_from_path()`. Ein
echter Fund beim ersten Testlauf: `slugify("_archive")` strippt das führende `_` (kein
`isalnum()`-Zeichen) und würde `"archive"` liefern — ein Reserviert-Check NACH dem Slugifizieren
hätte nie gegriffen. Behoben: der Check läuft auf dem rohen, nur lowercased Segment, vor dem
Slugifizieren.

**`storage/acl.py`** (neu): `Grant`/`AclDecision`/`AclReader`, `yaml.safe_load` direkt (kein
zweiter Loader nötig, V51 — PyYAML ist bereits Dependency, `frontmatter.py` benutzt es schon).
`RESERVED_DIR_NAMES`/`MAX_FOLDER_DEPTH` bewusst in `files.py` statt hier (dokumentierte kleine
Abweichung vom Plan-Snippet §1.2.3 — Ordnerpfad-Validierung ist schon dessen Job). Fail-closed
überall: kaputtes/nicht-Mapping-`.share.yml` → `logger.critical` + leere `Grant`, nie eine
Exception im Lesepfad. Cache `dict[(path,mtime,size)->Grant]`, `invalidate()` für Tests/
`spacectl.py`.

**`models.py`:** `VISIBILITY_VALUES`/`DEFAULT_VISIBILITY`, `Item`/`ItemSummary` bekommen `folder`/
`visibility`/`share_read`/`share_write`, `SpaceInfo` bekommt `members`/`folders`.

**`index.py`:** vier neue Spalten, `INDEX_SCHEMA_VERSION = 2` über `PRAGMA user_version` (V46
geschlossen). **Der eine Fund, der über den Plan-Text hinausging** (Advisor-Review vor der
Umsetzung): `Store.__init__` rief `rebuild_index()` nie auf, `serve.py` (der reale
Diensteinstieg) auch nicht — nur `space_cli.py` von Hand. Ein reiner Schema-Sprung hätte den
Produktivindex nach dem nächsten Deploy leer zurückgelassen, jeder `get()` hätte `ItemNotFound`
geworfen, bis jemand manuell reindiziert. Behoben: `index.connect()` liefert jetzt
`(conn, rebuilt: bool)`, `Store.__init__` ruft bei `rebuilt=True` selbst `self.rebuild_index()`.
Erfüllt tatsächlich Entscheidung **G** aus `phase1_storage/CLAUDE.md` (`rebuild_index()`
öffentlich **und beim Start**) — die zweite Hälfte stand dort schon immer, war aber nie
verdrahtet.

**`store.py`:** `acl_of(item_id)` (index-only wie `space_of()`), `create()`/`update()` mit
`folder`/`visibility`/`share_read`/`share_write`, `search(spaces=, folder=)`, `list_spaces()`
verzeichnis- UND indexbasiert mit `members`/`folders`. `_item_to_text` schreibt `visibility` nur
bei Abweichung vom Default, `share_read`/`share_write` nur wenn nicht leer — sonst hätte jedes
bestehende Item beim nächsten Write ein stilles `visibility: private` bekommen, obwohl das
`migrate_visibility.py`s Job ist (Step 6). **Ein echter Bug, von den eigenen Tests gefangen:**
`acl_of()` unionte `share_write` zuerst nicht in `read` — ein Item mit `share_write: [x]` aber
leerem `share_read` hätte einen Schreiber ohne Leserecht gehabt. `test_acl_of_unions_item_shares_
with_share_yml` schlug beim ersten Lauf fehl, Fix: „write impliziert read" gilt jetzt auch für
die Item-eigenen Freigaben, nicht nur für `.share.yml`.

**Verifiziert, mehrstufig:** `pytest -q` → **671 passed** (625 + 46 neue: 36 in `phase1_storage/`
+ 10 `test_acl.py` — die 36 schließen die zwei `validate_folder()`-Traversal-Tests aus dem
zweiten Advisor-Durchlauf mit ein, siehe unten). Die drei Charakterisierungs-Goldens liefen VOR
und NACH dem gesamten Umbau
byte-identisch grün (P6-D erfüllt). `git diff --stat` auf `phase2_mcp/mcpserver`,
`phase5_ui/webui`, `phase4_auth/authserver` blieb **leer** — Step 4 bleibt vollständig innerhalb
`storage/` (P6-C eingehalten). **Real ausgeführt, nicht nur `pytest`** (das jeden `tmp_path`
immer frisch auf Schema-Version 2 startet und den Rebuild-Fix nie geprüft hätte):
`phase2_mcp/scripts/mcp_smoke.py --json` (alle 12 Schritte `ok:true`), `phase5_ui/scripts/
ui_budget.py --json` (alle Budgets `ok:true`, `all_within_budget:true`, echte 220-Item-Messung),
`phase5_ui/scripts/ui_smoke.py --json` (alle 11 Schritte `ok:true`). `ui_budget.py`s Log zeigt
den Rebuild-Fix live: gegen ein brandneues Temp-`DATA_ROOT` genau die erwartete Zeile
(`Index ... hat Schema-Version 0 (erwartet 2) — wird verworfen und leer neu angelegt`), danach
lief der komplette Lauf sauber durch.

Contract-Erweiterung in `phase1_storage/CLAUDE.md` unter „Geerbte Contracts" dokumentiert
(Fortsetzung der P6-Step-1-Öffnung, nicht eine vierte — siehe dort), Modul-Status-Tabelle dort um
Zeile 10 ergänzt.

**Zweiter Advisor-Durchlauf, vor dem Commit — zwei echte Funde, ein benannter offener Punkt:**

1. **Behoben:** `_row_to_item()`/`acl_of()` übernahmen `row["folder"]` direkt aus dem Index statt
   es aus dem Pfad neu abzuleiten. Der Index ist reine Ableitung (Hard Rule 2/„ein Index-Fehler
   fasst nie eine Datei an", `phase1_storage/CLAUDE.md`) — ein veralteter/falscher Spaltenwert
   hätte beim nächsten `update()` über `_write_item_file`s Zielpfad-Berechnung die Datei bewegt.
   Nicht über `pytest` mit frischem `tmp_path` erreichbar (Index und Datei entstehen dort immer
   zusammen), aber real: ein altes Binary gegen einen v2-Index schreibt `folder=''` in jede
   Zeile, die es anfasst (15-Spalten-`INSERT` ohne die vier neuen Spalten) — ab Step 5, sobald
   ein Adapter `folder` überhaupt setzt, ein echter Rollback-Pfad. Fix: beide Methoden rufen
   jetzt `files.folder_from_path()` auf dem tatsächlichen Pfad — bei `acl_of()` weiterhin reine
   Pfad-Arithmetik, kein Datei-Lesezugriff, der „liest die Item-Datei nicht"-Vertrag bleibt
   stehen. Alle 669 Tests weiterhin grün, Goldens weiterhin byte-identisch.
2. **Gepinnt, nicht verändert:** `validate_folder("../x")` lehnt nicht ab, sondern liefert
   `"item/x"` (`slugify("..")` fällt auf den `"item"`-Fallback zurück, kein `..`-Segment
   überlebt) — kein echter Traversal (der Pfad bleibt immer unter `data_root/space`), aber eine
   stille Umbenennung statt eines Fehlers. Tiefere Versuche (`"../../etc"`) fallen über den
   Tiefen-Check, nicht über einen dedizierten Traversal-Check. Zwei neue Tests in
   `test_files.py` pinnen genau dieses Verhalten, statt es unbeobachtet zu lassen — `folder`
   wird ab Step 5 Agenten-Eingabe.
3. **Offener Punkt, nicht diese Phase's Aufgabe:** `_item_to_text`s „nur bei Abweichung vom
   Default schreiben"-Regel (siehe oben) heißt, dass eine explizit gesetzte
   `visibility: private` beim nächsten `update()` wieder aus der Datei verschwindet (Default wird
   nie geschrieben, auch nicht wenn er vorher explizit dastand). Funktional harmlos — fehlend und
   `private` sind für `_item_from_text`/`row_from_file` dasselbe — aber Abnahmezeile 8 sagt
   „jedes Item trägt `visibility`" und wird vom Nikinger live gelesen; P6-L sagt, die Migration
   (Step 6) schreibt das Feld. Zwei mögliche Auflösungen, beide bewusst nicht hier entschieden:
   entweder der Nikinger akzeptiert „fehlend == private" als Erfüllung von Zeile 8, oder
   `visibility` wird „sticky" (geschrieben, sobald es einmal in der Quelldatei stand) — dann aber
   zusammen mit `migrate_visibility.py` in Step 6, nicht isoliert hier (würde sonst die drei
   Goldens aus diesem Step erneut anfassen). Kommentar sitzt zusätzlich direkt am betroffenen Test
   (`test_create_defaults_visibility_and_share_fields_and_omits_them_from_file`).

**Status:** Step 4 ist damit **gebaut**, DoD aus Plan §4 Step 4 erfüllt (Charakterisierung grün +
Contract dokumentiert). Kein eigener Abnahmematrix-Punkt für diesen Step — die Live-Prüfung
kommt erst mit den nutzerseitig sichtbaren Steps 5–7 (Rechtepolitik, Verwaltung/Migration, UI).

**Nächster Schritt (konkret):** Step 5 (Rechtepolitik) — `mcpserver/permissions.py`
(`SharePolicy`, `Surface`, `OwnSpaceWritable` entfernen), `mcpserver/tools.py` (alle Lese-/
Schreibpfade auf `acl_of()`/`can_read_item`/`can_write_item` umstellen, `search_items` filtert
`visibility: human` inkl. `total`), `mcpserver/app.py` (`AclReader` einmal bauen, mit `Store`
teilen), `webui/api.py`/`webui/serializers.py` (dasselbe mit `Surface.HUMAN`). Das ist der erste
Step, der `mcpserver`/`webui` tatsächlich anfasst — Gate-A→B-Punkt-3-Erinnerung bleibt gültig
(frühestens 2026-08-28, siehe oben), unabhängig vom Baufortschritt hier.
