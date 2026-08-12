---
status: live
purpose: L3-Archiv der Phase-6-Session-Bloecke -- Steps 0-4 (Haushalt, Werkzeug-Ergonomie, Betrieb, Update-Log/Banner, Storage-Fundament), verbatim aus phase6_shares/CLAUDE.md verschoben
read-when: Historie einer bereits abgeschlossenen Phase-6-Teilarbeit nachvollziehen -- nicht beim normalen Sessionstart lesen
detail: L3
up: ../phase6_shares/CLAUDE.md
updated: 2026-08-12
---

# SESSIONS_ARCHIVE.md — Phase 6 (`phase6_shares/`)

> Erste Rotation (2026-08-10, Nikinger-Auftrag): drei Nachträge (Steps 0/1/2 — Haushalt,
> Werkzeug-Ergonomie, Betrieb) waren seit Step 3 „settled, nicht mehr Arbeitskontext", der Kopf
> lag nahe am 40KB-Softcap. Rotationslogik wie `phase4_auth/CLAUDE.md`s Steps-0–6a-Verschiebung.
> **Zweite Rotation (2026-08-12,** `scripts/rotate_session_block.sh phase6_shares`**):** Kopf
> erreichte erneut den Softcap (39 KB), diesmal über `scripts/rotate_session_block.sh` statt von
> Hand — der neue Block (Steps 1–3, s. u.) wurde mechanisch verschoben, Byte-Identität geprüft,
> nur sein Titel danach korrigiert (siehe Hinweis im Block selbst). Newest zuoberst wie sonst
> überall in diesem Repo.
> **Dritte Rotation (2026-08-12, derselbe Tag, Step-5-Commit):** Step 4 (Storage-Fundament)
> wandert verbatim herein, wieder mechanisch über dasselbe Skript, Byte-Identität geprüft.

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

**Nachtrag, 2026-08-12, dreizehnter — Punkt 3 entschieden, Nikinger-Bestätigung.** „Fehlend ==
`private`" erfüllt Abnahmezeile 8 — **kein Sticky-Write**, keine Änderung an `_item_to_text`
nötig. Begründung, vom Nikinger nach Abwägung bestätigt: der Wert ist zur Laufzeit nie
mehrdeutig (`fields.get("visibility", DEFAULT_VISIBILITY)` ist derselbe Codepfad, ob das Feld
in der Datei steht oder nicht — ACL-Auflösung, `visibility: human`-Agentensperre (P6-P) und
API/UI-Anzeige unterscheiden „fehlt" nie von „explizit `private`"), und das Muster deckt sich mit
der bereits gelockten Konvention für `share_read`/`share_write` (§2.1: „leer = nicht vorhanden") —
`visibility` anders zu behandeln wäre die Inkonsistenz, nicht die Konsistenz. Einzige Konsequenz:
Abnahmezeile 8 wird künftig über `get_item`/die API gelesen (löst zu `private` auf), nicht über
ein rohes `grep visibility:` auf der `.md`-Datei — steht jetzt hier, damit es bei der Step-6-
Abnahme nicht überrascht. Punkt damit **geschlossen**, keine offene Aufgabe mehr für Step 6.

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

---

## Session stopped — 2026-08-09 bis 2026-08-12 (Steps 1–3 — Werkzeug-Ergonomie, Betrieb, Update-Log/Banner)

**Umbenannt bei der Rotation vom 2026-08-12** (dieser Block trug beim Verschieben noch den Titel
des allerersten Session-Blocks, „Step 0" — inhaltlich beginnt er aber mit der Steps-0–2-
Kurzfassung und geht dann vollständig in Steps 1–3 über; Titel korrigiert, damit er sich vom
darunterliegenden, tatsächlichen Step-0-Eintrag unterscheidet. Reiner Titel-Fix, kein Satz Prosa
darunter verändert.)

**Steps 0–2 (Haushalt/Verifikation, Werkzeug-Ergonomie, Betrieb) sind komprimiert und nach
`SESSIONS_ARCHIVE.md` verschoben** (2026-08-10, Nikinger-Auftrag) — dieselbe Rotationslogik wie
`phase4_auth/CLAUDE.md`s Steps-0–6a-Verschiebung: verbatim per `sed -n`, Byte-Identität vor dem
Löschen geprüft, nicht neu zusammengefasst. Die Modul-Status-Tabelle oben bleibt vollständig;
nur die Prosa darunter ist gewandert. **Kurzfassung des Archivierten:** Step 0 verifizierte den
P5-Übergabestand (576/576, V39–V41 geschlossen) und dokumentierte drei Regeländerungen (§0.7
a/b/c, u. a. Hard Rule 4 neu gefasst). Step 1 baute `patch_item` (`storage/patch.py`,
`mcpserver/receipts.py`, Quittungen statt Volltext an allen Schreib-Tools, V48 empirisch
geschlossen). Step 2 schloss O2 (`purge_expired()` räumt `token_families`/`clients` ab) und
ergänzte Client-Surface-Logging (`ua`-Feld, V42), `diagnose.sh` Prüfung 11, `ui_budget.py`s
Latenzmessung — Status blieb „gebaut, Live-Teile beim Nikinger" (V42, Gate-A→B-Punkt 3), beide
inzwischen in Steps 3s eigenen Nachträgen weitergeführt (siehe unten).


**Nachtrag, 2026-08-09, sechster — Step 3 (Update-Log und Banner) fertig, in derselben Sitzung
fortgesetzt.** Advisor-Review **vor** der Umsetzung eingeholt (Auftrag: „letzten machbaren Step
zu Ende bringen, Rest als Kommandos für den Nikinger"), vier Punkte daraus direkt übernommen,
nicht erst am Ende nachgezogen.

**Schema 3** (`authserver/store.py`): `users.seen_update_id TEXT`, additiv — anders als V1→V2
(nur neue Tabellen) muss diese Migration eine **bereits gefüllte** Tabelle erweitern; SQLite
kennt für `ALTER TABLE ADD COLUMN` kein `IF NOT EXISTS`, `_apply_schema_v3()` prüft deshalb
`PRAGMA table_info()` selbst. `SCHEMA_VERSION` → `"3"`. Zwei neue Methoden
(`get_seen_update_id`/`set_seen_update_id`), bewusst **nicht** als `UserRow`-Feld (Advisor-Fund:
`authctl.py`/`userdir.py`/`import_users_to_db.py` konsumieren `UserRow`, keines braucht diesen
Zustand). Drei bestehende Tests hätten sonst mit der falschen `schema_version`-Zahl weiter
gegrünt (`"2"` statt `"3"`) — beim ersten `pytest`-Lauf gefunden und korrigiert, nicht vom
Advisor: `test_schema_is_created_and_versioned`, die V1→V2-Migrationsprobe (endet nach Schema 3
zwangsläufig bei `"3"`, nicht `"2"`) und die dedizierte Versionsprobe selbst (umbenannt zu
`test_schema_version_is_three_after_initialise`). +3 Tests in `test_authserver_store.py`
(258→261): der v2→v3-Migrationstest (gleiches Muster wie der bestehende v1→v2-Test — Schema 2
von Hand gebaut, über `AuthStore` geöffnet, Spalte + Version geprüft) und zwei
`seen_update_id`-Roundtrip-Tests.

**`webui/updates.py`** (neu): `parse_update_log()`/`UpdateEntry`/`load_update_log()`. Strikt nach
Plan §2.4: `## <ISO-Datum>` beginnt einen Eintrag, `- ` eine Zeile, alles andere wird ignoriert.
ID = `"<Datum>#<n>"`, `n` zählt Wiederholungen desselben Datums in Dateireihenfolge (disambiguiert
zwei `## <selbes Datum>`-Blöcke). **Reihenfolge = Dateireihenfolge, nicht sortiert** — neue
Einträge werden oben eingefügt wie ein Changelog, `entries[0]` ist der neueste; das ist die
Prämisse, auf der sowohl `deploy.sh`s Gate („oberste Überschrift") als auch `api.py`s `latest_id`
aufbauen. `load_update_log()` fail-soft (fehlende/kaputte Datei ⇒ leere Liste ⇒ kein Banner, nie
ein 500) — kein Markdown-Rendering hier, das macht `app.js` mit dem vorhandenen Sanitizer (Hard
Rule 7 sinngemäß: der Server bleibt dumm, auch bei einem Log-Parser). +7 Tests
(`phase6_shares/tests/test_updates.py`, neue Datei — reine Funktionstests, kein Store, gleiche
Kategorie wie `test_patch.py`).

**`webui/api.py`**: `GET /api/v1/updates` (Einträge + `latest_id` + `seen_update_id` der
Sitzung), `POST /api/v1/updates/seen` (schreibt den **serverseitig berechneten** `latest_id`, nie
eine vom Client geschickte ID — Advisor-Vorgabe: unnötige Validierungsfläche und ein
Stale-Client-Rennen sonst umsonst). `api_routes()` bekommt dafür einen fünften Parameter,
`auth_store: AuthStore` — der gesehen-Zustand lebt in der Auth-SQLite, nicht im `storage`-Kern.
**Dokumentierte Ein-Zeilen-Abweichung** von Step 3s Plan-Dateiliste (nennt nur `webui/api.py`,
nicht `mcpserver/app.py`): `create_app()` muss den neuen Parameter durchreichen (`oauth.store`,
dieselbe Instanz wie `account_routes()`, kein zweiter DB-Handle) — acht weitere direkte
`api_routes(...)`-Aufrufer (`conftest.py` × 1, `test_api.py` × 3, `test_overview.py` × 1,
`ui_budget.py` × 2, `ui_smoke.py` × 1) mussten denselben fünften Parameter nachziehen. Per
`grep -rn "api_routes("` **vollständig** gefunden, nicht stichprobenartig — die ersten beiden
`pytest`-Läufe fingen nur die Testdateien ab; `ui_budget.py --json` real ausgeführt deckte den
gemockten Suite-Blindspot (Skripte laufen nie unter `pytest`) auf, `TypeError: api_routes()
missing 1 required positional argument`.

**`webui/static/js/updates.js`** (neu): `window.SharefyxUpdates.init({api, toast})`, injiziert
von `app.js`s `initShell()` an dessen eigenem Ende. **Muss vor `app.js` geladen werden**
(`app.html`, beide `defer`) — `updates.js` ruft `app.js`s globale `markdownToHtml()`/
`sanitizeHtml()` (Top-Level-Funktionen, kein IIFE, deshalb window-Properties trotz `"use
strict"`), umgekehrt bräuchte `app.js` sonst einen noch nicht existierenden
`window.SharefyxUpdates`. Advisor-Fund **vor** der Umsetzung, sonst hätte ein stiller No-Op das
Banner nie gezeigt, `pytest` bliebe grün (JS bleibt laut Plan unit-ungetestet, P5) — der
Nikinger hätte es im Browser gefunden, nicht die Suite.

**Node/jsdom-Simulation** (Scratchpad, nicht im Repo, gleiche Kategorie wie P5 Step 10/11):
erster Versuch mit `window.eval(appJs)` + `window.eval(updatesJs)` warf fälschlich
`ReferenceError: markdownToHtml is not defined` — **echter Befund über die Testmethode, kein
Bug im Code:** Strict-Mode-Direct-`eval()` isoliert Top-Level-Deklarationen von der aufrufenden
Umgebung (ECMAScript-Spezialfall genau für `eval()`), ein reales `<script defer>`-Tag tut das
nicht. Zweiter Versuch mit echten, ins DOM eingehängten `<script>`-Elementen (treue
Nachbildung von `<script src=... defer>`) lief sauber durch: Banner erscheint mit gerendertem
Markdown (`**Eintrag**` → `<strong>`), setzt `body.has-update-banner`, „Verstanden" versteckt
es und postet `/updates/seen`, „Update-Log ansehen" öffnet den Dialog mit denselben Einträgen,
ein bereits gesehener `latest_id` unterdrückt das Banner beim erneuten Laden vollständig.

**`deploy.sh`-Gate (P6-X):** läuft direkt nach `release_sha` (vor venv/pip/pytest — ein sicher
vermeidbarer Abbruch soll in Sekunden kommen, nicht nach dem teuersten Skriptteil), akzeptiert
UTC- **oder** lokales Datum (ein Deploy kurz nach Mitternacht Lokalzeit läge in UTC noch am
Vortag — ein falscher Abbruch bei einem legitimen Eintrag wäre der schlechtere Fehler als eine
zu großzügige Prüfung). `SHAREFYX_ALLOW_STALE_UPDATELOG=1` überspringt es. **Live-Fund beim
ersten Testlauf** (nicht Advisor): die `grep | sed`-Pipeline unter `pipefail` warf bei einer
fehlenden/leeren Datei einen rohen Bash-Fehler statt der eigenen ABBRUCH-Zeile — `grep` liefert
1 bei keinem Treffer, `pipefail` reicht das durch, `set -e` bricht die Zuweisung sofort ab,
bevor die eigene `if`-Prüfung überhaupt läuft. Mit `|| true` behoben. `test_deploy_scripts.py`s
`_env()`-Helfer setzt die Override-Variable jetzt als Default (die `source_repo`-Fixture trägt
kein `docs/UPDATE_LOG.md`, ohne Default wären alle ~18 bestehenden Deploy-Tests am neuen Gate
gescheitert, nicht nur die drei, die es gezielt prüfen) — dieselbe `_clean_environ()`-Disziplin,
die die Testliste (Plan §5) für jede neue Skript-Testdatei vorschreibt. +3 Tests: Gate blockiert
(kein Log), Gate lässt einen echten heute datierten Eintrag durch (Positivpfad, nicht nur der
Fehlerfall), Override umgeht ein fehlendes Log. Meta-Test
`test_harness_ignores_ambient_sharefyx_configuration` um die neue Env-Var ergänzt (hätte sonst
seinerseits falsch geschlagen).

**`docs/UPDATE_LOG.md`** (neu): erster Eintrag, datiert 2026-08-09, kündigt die künftige
Sichtbarkeitsumstellung an (P6-L, H1 — Pflichtinhalt laut Plan). **Ehrlich zum Gate:** dieser
Eintrag ist nur am 2026-08-09 selbst „frisch" — deployt der Nikinger an einem späteren Tag ohne
neuen Eintrag, blockiert `deploy.sh` by design (Override oder neuer Eintrag), das ist keine
Regression, sondern der Zweck des Gates.

**Schema-3-Rollback-Sicherheit geprüft** (`deploy.sh` rollt bei einem gerissenen Health-Gate auf
altes Binary zurück — „altes Binary gegen Schema-3-DB" ist ein realer Pfad). `upsert_user()`/
`_user_from_row()` benennen Spalten immer schon explizit, die neue Spalte ist für altes Binary
inert. **Eine echte, harmlose Nebenwirkung:** altes Binärs `initialise()` kennt
`_apply_schema_v3()` nicht und schreibt `schema_meta.schema_version` beim Start zurück auf
„2" (Spalte bleibt physisch stehen) — bis der nächste erfolgreiche Deploy wieder „3" schreibt.

**Kleine Design-Entscheidung:** Banner als `position: fixed` statt einer Grid-Zeile in `.shell`
(§4.1s Drei-Spalten-Layout bleibt unverändert); „Update-Log ansehen" sitzt im bestehenden
Konto-Dialog statt einen zweiten Einstellungs-Einstiegspunkt zu erfinden.

**Verifiziert:** `pytest -q` → **620 passed** (604 + 16 neue, deckt sich exakt: 3
`test_authserver_store.py` + 7 `test_updates.py` + 2 `test_api.py` + 3
`test_deploy_scripts.py` + 1 `test_static_routes.py` — der letzte aus dem zweiten Advisor-
Durchlauf, siehe unten). `mcp_smoke.py --json` weiterhin 13/13. `ui_budget.py --json` und
`ui_smoke.py --json` real ausgeführt, beide sauber (erst NACH dem Signatur-Fix — vorher der
`TypeError`-Fund oben). `node --check` auf `app.js`/`updates.js`. Tabu-Diff: `mcpserver/app.py`
ist eine dokumentierte Ein-Zeilen-Abweichung (siehe oben), sonst nur `phase4_auth/authserver/
store.py`, `phase5_ui/webui/{updates,api,config}.py`, `phase5_ui/webui/static/*`,
`phase5_ui/scripts/deploy.sh`, `phase5_ui/scripts/{ui_budget,ui_smoke}.py`, `docs/UPDATE_LOG.md`,
Testdateien — genau die in Step 3s Plan-Dateiliste plus die eine dokumentierte Abweichung.

**Zweiter Advisor-Durchlauf, vier Funde vor dem Commit behoben:** (1) Bannerhöhe war fest
(`44px`) statt am realen, mehrzeiligen Eintragstext gemessen — Fix + Begründung stehen jetzt als
Kommentar in `app.css`/`updates.js` (`syncBannerHeight()`). (2) „sechs weitere Aufrufer" war
falsch gezählt, tatsächlich acht (`grep`-Beleg oben) — korrigiert. (3) Die `updates.js`-vor-
`app.js`-Reihenfolge stand nur in Docstrings, kein Test bewies sie — zwei Ergänzungen in
`test_static_routes.py` (Content-Type-Tabelle + `test_updates_js_loads_before_app_js`). (4)
Schema-3-Rollback-Sicherheit tatsächlich geprüft, nicht nur behauptet — Ergebnis + der eine
harmlose Fund (`schema_version` fällt nach einem Rollback vorübergehend auf „2") stehen im
Absatz direkt darüber.

**Status ehrlich, nicht optimistisch:** Step 3 kann nicht ✅ schließen. **Gate-A→B-Punkt 4 ist
seit 2026-08-11 vollständig geschlossen** — Banner (nach dem Content-Fix vollständig lesbar) UND
Fabians Bestätigung (Update-Banner inklusive Sichtbarkeitsumstellungs-Ankündigung bei ihm
ebenfalls einwandfrei) sind beide bestätigt, technische Seite bei beiden Nutzern ohne Befund.
Einziger noch offener Gate-Punkt: **Punkt 3** (Purge-Zeilenrückgang, frühestens 2026-08-28).
Status bewusst **„gebaut, ein Live-Teil beim Nikinger"** — der eine verbleibende Teil ist rein
zeitgebunden, keine offene Aufgabe.

**Nächster Schritt (konkret):** Block A (Steps 0–3) ist damit vollständig **gebaut**, nichts
davon ist live. Vor Block B steht **GATE A→B** (Plan §4, vier Punkte) — konsolidierte
Reihenfolge für den Nikinger, über Step 2 und Step 3 hinweg, nicht nur Step 3 isoliert:

1. **Frisches Auth-Backup vor dem Deploy** — dieser Deploy migriert die laufende `auth.sqlite3`
   auf Schema 3 (additiv, aber ein frisches Backup unmittelbar davor kostet nichts und deckt
   genau den Fall ab, den `deploy.sh`s eigenes Pre-Deploy-Bundle NICHT abdeckt — das sichert nur
   `DATA_ROOT`, nicht `auth.sqlite3`): `sudo systemctl start sharefyx-authbackup.service`
   (bereits installierter Oneshot, `phase5_ui/systemd/sharefyx-authbackup.service`) — kein
   manueller `authbackup.sh`-Aufruf mit Env-Vars nötig.
2. **Deploy** — `phase5_ui/scripts/deploy.sh main` (oder der passende Ref). Bricht ohne einen
   heute datierten `docs/UPDATE_LOG.md`-Eintrag ab (P6-X) — der vorhandene Eintrag ist auf
   2026-08-09 datiert, trägt also nur am Tag des tatsächlichen Deploys; an einem späteren Tag
   entweder einen neuen Eintrag ergänzen oder `SHAREFYX_ALLOW_STALE_UPDATELOG=1` setzen (bewusst
   so, kein Bug).
3. ~~Gate-A→B-Punkt 1+2~~ — **✅ live bestanden, 2026-08-09** (Nachtrag unten).
4. ~~Gate-A→B-Punkt 4~~ — **✅ vollständig live bestanden, 2026-08-11.** Banner-Hälfte seit
   2026-08-10 (nach einem echten Fund, Nachtrag „achter" unten: Content-Bug in
   `docs/UPDATE_LOG.md`, nicht im Parser — behoben + Regressionstest). Fabian-Hälfte seit
   2026-08-11: bei ihm technisch einwandfrei, Banner inklusive Ankündigung der
   Sichtbarkeitsumstellung gesehen und bestätigt (Nachtrag unten).
5. ~~V42~~ — **geschlossen, 2026-08-12** (Nachtrag unten): `ua` wird von echten MCP-Clients
   zuverlässig gesetzt, unterscheidet aber **nicht** zwischen Claude-Oberflächen — alle senden
   `"Claude-User"`. Negativer, aber definitiver Befund, kein offener Punkt mehr.
6. **Gate-A→B-Punkt 3** — **versucht, 2026-08-09, korrekt noch nicht abgeschlossen** (Nachtrag
   unten): `clients`/`token_families` sind noch zu jung für die 30/90-Tage-Grenze. Frühestens
   ab 2026-08-28 erneut prüfen (`authctl.py purge-expired`, gegen den echten Zeilenrückgang).

Erst wenn alle vier Gate-Punkte stehen, beginnt Step 4 (Storage-Fundament, Block B) — nicht
vorher, das Gate ist im Plan hart. V42 war ohnehin kein Gate-Blocker; jetzt zusätzlich
geschlossen.

**[2026-08-12 Korrektur, Nikinger-Entscheidung]:** Der Nikinger hat explizit angewiesen, Step 4
jetzt zu beginnen und Punkt 3 als offenen, mitlaufenden Punkt zu tragen, statt bis 2026-08-28 zu
warten — eine bewusste, benannte Übersteuerung des Gates, keine stille Abweichung. Punkt 3 bleibt
unten als offen stehen (frühestens 2026-08-28), Step 2 bleibt „gebaut, ein Live-Teil beim
Nikinger" und Abnahmezeile 4 bleibt unverändert **nicht** ✅ — §6s Statusregel („✅ heißt
live-verifiziert, nicht gebaut") gilt unverändert fort. Diese Entscheidung überschreibt nur die
Reihenfolge (Step 4 vor Gate-Abschluss), nicht die Abnahmekriterien selbst.

**Nachtrag, 2026-08-09, siebter — Gate-A→B-Punkte 1–3 live geprüft** (Claude Code direkt auf der
VM, Connector zuvor vom Nikinger neu verbunden — die alte Verbindung hatte noch den 6-Tool-Stand
von vor P6). **Punkte 1+2 ✅:** an `itm_1b4fd59e` (Wegwerf-Testitem, danach archiviert) —
mehrdeutiger `old_text` schlägt fehl (`"edits[0] fand 2 Treffer (Zeilen 2, 4)"`), Datei
unverändert (`version` blieb 1); drei Ersetzungen über zwei Aufrufe, erster ohne `return_body`
liefert eine Quittung (`{"op":"patch",...,"replacements":2,"lines":[1,4],"bytes":{...}}`), zweiter
mit `return_body=true` den vollen Text. Vier eigene Git-Commits in `DATA_ROOT` bestätigt (`create`/
`patch`×2/`archive`). **Punkt 3 — Mechanismus bestätigt, Zahl noch nicht gesunken:**
`SPACE_AUTH_DB=/var/lib/sharefyx/auth.sqlite3 authctl.py purge-expired` lief sauber, 7 reale
abgelaufene Zeilen entfernt (1 `auth_codes` + 6 `access_tokens`) — aber `clients`/`token_families`
beide `0`, **ehrlicher Grund, kein Fehlschlag:** die älteste tote Familie ist vom 2026-07-29, elf
Tage alt, unter der 30-Tage-Grenze; kein Client ist 90 Tage alt (Dienst existiert erst seit
2026-07-24/29). Zeitgleich stiegen `clients`/`token_families` sogar leicht (39→40, 22→23) — der
Nikinger-Reconnect des Connectors registrierte einen neuen DCR-Client, reine Nebenwirkung der
Live-Prüfung selbst. `journalctl -u sharefyx-purge.service` bestätigt zusätzlich: der tägliche
Timer lief zuletzt Aug 9 00:04 (VOR dem heutigen Deploy) noch mit dem alten Purge-Code (Ausgabe
ohne `token_families`/`clients`-Schlüssel) — der heutige manuelle Lauf war der erste mit dem neuen
O2-Code, der nächste Timer-Lauf (Aug 10 00:02) läuft bereits dagegen. **Ob Schritt 1
(Auth-Backup vor dem Deploy) lief, ist aus dem Chat nicht ersichtlich** — der Nikinger postete
nur die `deploy.sh`-Ausgabe. Kein Vorfall, falls übersprungen (additive Migration, kein
Datenverlustrisiko), aber im Nachhinein nicht mehr sinnvoll nachholbar — beim nächsten Deploy
nicht vergessen.

**Nachtrag, 2026-08-10, achter — Gate-A→B-Punkt 4: Content-Bug im Banner gefunden+behoben,
Timer-Bestätigung nachgezogen.** Nikinger-Meldung: Banner sichtbar, Text abgeschnitten bei
„…und alles Neue ist nach". **Kein Parser-Bug** (tut exakt, was Plan §2.4 verlangt: nur `## `/
`- `-Zeilen zählen) — **ein Content-Bug:** der erste `docs/UPDATE_LOG.md`-Eintrag war weich
umgebrochener Fließtext über vier physische Zeilen, der Parser verschluckte die drei
Fortsetzungszeilen stillschweigend. Behoben: zwei echte `- `-Zeilen (je eine physische Zeile) +
ein `<!-- -->`-Formathinweis am Dateianfang. **Regressionstest ergänzt, nicht nur die Datei
gefixt:** `test_real_update_log_has_no_swallowed_continuation_lines` liest die REALE Datei, kein
Test hatte das bis dahin getan. +1 Test (`test_updates.py` 7→8, 621 gesamt). Parser-Gegenprobe:
beide Zeilen jetzt vollständig. **Purge-Timer bestätigt:** Lauf vom 2026-08-10 00:02 mit dem
neuen O2-Code (`token_families`/`clients` beide `0`, konsistent — noch nichts alt genug).
**Nachtrag, 2026-08-10, zweiter Teil:** Nikinger bestätigt Banner jetzt vollständig lesbar,
gerenderter Text stimmt mit dem korrigierten `docs/UPDATE_LOG.md` überein — Banner-Hälfte von
Gate-A→B-Punkt 4 damit ✅. **Nebenbefund während der Live-Prüfung, kein Vorfall:** zwei
transiente Connector-Aussetzer, beide Male griff der Retry, kein Datenverlust — Netzwerk-
Flakiness (Nikingers Einschätzung), kein Server-Fund; `journalctl` zeigte im fraglichen Fenster
keine Exceptions, keine Neustarts.

**Nachtrag, 2026-08-11 — Gate-A→B-Punkt 4 vollständig geschlossen.** Fabians Seite lief
störungsfrei — Connector/UI technisch einwandfrei, und er hat das Update-Banner samt Ankündigung
der Sichtbarkeitsumstellung gesehen und bestätigt (dem Nikinger gegenüber, nicht direkt Claude
Code). Damit ist die zweite, bis dahin einzig offene Hälfte von Punkt 4 geschlossen — **Gate-A→B
hat jetzt nur noch einen offenen Punkt: Punkt 3** (Purge-Zeilenrückgang, frühestens 2026-08-28,
siehe oben). Kein Code-/Testlauf diese Session — reine Statuspflege auf Nikinger-Bitte
(„downtime" vor Arbeitsbeginn morgen genutzt).

**Nachtrag, 2026-08-12 — V42 geschlossen, echtes journald-Fenster ausgewertet.** Fenster war
2026-08-10 00:00 bis heute (~2 Tage echter Betrieb, Deploy vom 08-09 hatte `journald` faktisch
geleert). `journalctl -u sharefyx-mcp --since "2026-08-10 00:00:00" | grep -o '"ua":"[^"]*"' |
sort | uniq -c`: 285 `/mcp`-Requests insgesamt, davon **278 mit `"ua":"Claude-User"`** — jeder
einzelne echte MCP-Tool-Aufruf in diesem Fenster (Rest: 4 eigene `python-httpx`-Testläufe, 2
`CensysInspect`, 1 `curl`, alles kein echter Claude-Client). **Befund: `ua` wird von echten
MCP-Clients zuverlässig gesetzt (nie leer/fehlend) — unterscheidet aber NICHT zwischen
Claude-Oberflächen.** Claude Code und claude.ai (Web/Desktop) senden auf der `/mcp`-Ebene
denselben generischen String, keine surface-spezifische Variante. Zusätzlich beobachtet auf
`/ui/*` (Browser, nicht MCP): 3393 Firefox-, 748 Chrome-, 13 Android-, 1 Safari-Aufruf — echte,
vielfältige menschliche Nutzung über die Testtage, bestätigt aber nur Browser-Diversität, nicht
MCP-Surface-Diversität. **V42 damit geschlossen** — negativer, aber definitiver Befund (P6 Step
2s Client-Surface-Logging liefert kein brauchbares Unterscheidungsmerkmal auf `ev="http"`; eine
Unterscheidung bräuchte eine andere Signalquelle, kein Scope dieser Phase). Kein Code-/Testlauf,
reine Log-Auswertung.

---

## Session stopped — 2026-08-09 (Step 0 — Haushalt, Verifikation, Regeländerungen)

**Auftrag:** Nikinger startete Phase 6 direkt in Claude Code (kein Browser-Planungsauftrag nötig —
`docs/concepts/phase6_shares_plan.md` lag bereits ausführungsreif und untracked im Repo, aus einer
Browser-Planungssession vom selben Tag gegen den Drive-Snapshot `2026_08_09_sharefyx-main`
geschrieben). Gearbeitet wurde Plan §4 Step 0, Punkte 1–6.

**Verifikationsdurchlauf (Plan-Punkt 1):**
- `pytest -q`: **576 passed** — deckt sich exakt mit der Plan-Behauptung. **V39 geschlossen.**
- `git status`: sauber bis auf das untracked `docs/concepts/phase6_shares_plan.md` (jetzt
  hinzugefügt). `HEAD` == `origin/main` (5524a42) — Push-Stand sauber.
- `find . -name "*.md" -size +40k`: keine neuen Treffer durch diesen Commit; bestehende Treffer
  sind bereits 📕/📦 (unverändert seit P5).
- `up:`/`down:`-Links: alle in diesem Commit neu gesetzten (`phase6_shares/CLAUDE.md` ↔
  `docs/concepts/phase6_shares_plan.md`, `docs/INDEX.md`-Zeilen) lösen auf.

**V40 — CVE-2026-48710 („BadHost"):** `pip show starlette` → **1.3.1**, ≥ 1.0.1. **Nicht
betroffen, geprüft-in-Ordnung.** Kein Pin-Update nötig, kein Befund S11.

**V41 — Anthropic-Connector-Doku (Nachfolger V33, seit P4 Step 0 mehrfach durchgereicht ohne
Bearbeitung — siehe `PHASE5_CLOSEOUT_HANDOVER.md` V33-Zeile):** **Diesmal tatsächlich gelesen**,
und zwar die richtige Fläche — dieses Projekt nutzt **Custom Connectors auf claude.ai/Desktop**
(R2), nicht die API-seitige `mcp_servers`/`mcp_toolset`-Fläche. `support.claude.com/en/articles/
11175166` (Custom-Connector-Guide) **nennt keine** Grenze für Tool-Anzahl, Beschreibungslänge oder
Schemaform — auch nichts zu Array-of-Objects-Parametern (relevant für `patch_item`s
`edits: list[TypedDict]`, Step 1). Zwei Drittquellen (sunpeak.ai, startdebugging.net, zur API-
Fläche, nicht zu Custom Connectors) behaupten ein 2KB-Deskriptionslimit bzw. Genauigkeitsverlust
ab 30–50 Tools — **unbestätigt für diese Fläche, nicht übernommen**, nur als Kontext notiert.
sechs → sieben Tools bleibt so oder so weit im unauffälligen Bereich. **V41 geschlossen**, echtes
Schemaform-Verhalten (`list[TypedDict]` durch `fastmcp` 3.4.x) bleibt V48, Step 1, empirisch zu
prüfen.

**Regeländerungen §0.7:**
- **(a) Hard Rule 4** in Root-`CLAUDE.md` neu gefasst, alter Wortlaut durchgestrichen stehen
  gelassen. **Zusatz gegenüber dem Plantext:** ein Satz, dass die neue Regel **erst mit Step 5**
  scharf wird (`.share.yml`/`share_write`/`SharePolicy` existieren vor Step 4/5 nicht im Code) —
  bis dahin gilt faktisch weiter die durchgestrichene Fassung. Reiner Zusatz, ändert die gelockte
  Formulierung nicht. Der `<untrusted_content>`-Satz der alten Regel bleibt **unverändert aktuell**
  (P6-O bestätigt ihn), nur der Cross-Space-Write-Satz wird ersetzt.
- **(b) `ROADMAP.md`:** neue P6-Zeile (🔄) plus datierte Korrekturen an „Feingranulare Rechte" und
  „Mehrmandantenfähigkeit" unter „Bewusst nicht auf der Roadmap".
- **(c) Handover §4.5:** der Plan-Widerspruch (P5 Step 9 „frische Einladung" vs. Plan §2.6 „reine
  Credential-Migration") wird hier festgehalten, nicht im 📕-Snapshot `phase5_ui_plan.md`:
  **gelebt wurde der Step-9-Weg** (frische Einladung). Damit geschlossen.

**V37 (Plan-Punkt 6) — „Exakte Abschnittsüberschriften in `docs/INDEX.md`":** laut
`PHASE5_CLOSEOUT_HANDOVER.md` (📕, nicht editierbar) „faktisch erledigt, nie explizit vermerkt".
**Hier formal abgehakt:** die Active-phase-Überschrift folgt in diesem Commit wieder demselben
Muster (`## Active phase (6 — …)`), wie es P5 in Step 0 anlegte.

**Minor Drift, inline korrigiert (kein Nikinger-Entscheid nötig):**
- `pytest.ini`s `testpaths` nennt Verzeichnisse explizit (kein Glob) — der Plan erwähnt das
  Nachziehen nirgends. `phase6_shares/tests` ergänzt, sonst würde Step 1 seine eigenen Tests nie
  einsammeln.
- Plan-Punkt 5 wollte `docs/INDEX.md` in diesem Commit auch um eine Zeile für `docs/UPDATE_LOG.md`
  ergänzen — diese Datei existiert erst ab Step 3. INDEX' eigene Regel („neue `.md` ⇒ Zeile im
  selben Commit") verbietet das Vorgreifen. Verschoben auf Step 3.
- `phase6_shares/tests/conftest.py` bewusst leer angelegt (P1-Step-0-Präzedenzfall: „Step 0 hat
  bewusst keine Tests, reines Skelett" — `phase1_storage/tests/conftest.py` ist bis heute leer).
- Plan-Punkt 5 nennt auch `scripts/` als Step-0-Deliverable. Git verfolgt keine leeren
  Verzeichnisse, und der erste reale Inhalt (`spacectl.py`/`migrate_visibility.py`) entsteht laut
  Plan erst in Step 6 — `scripts/` entsteht implizit mit der ersten Datei dort, nicht als leerer
  Platzhalter in diesem Commit.

**Phase-Head angelegt** (dieses Dokument), `docs/INDEX.md` um Plan + Phase-Head ergänzt, Root-
`CLAUDE.md`s „Current state" auf 🔄 Phase 6 gestellt.

**Verifiziert:** `pytest -q` nach allen Änderungen erneut grün (siehe Verifikations-Task, Ergebnis
oben) — Änderungen dieser Session sind ausschließlich Dokumentation + eine leere `conftest.py` +
eine `pytest.ini`-Zeile, kein Feature-Code.

**Nachtrag, 2026-08-09, zweiter — Advisor-Review vor Sessionende, vier Funde behoben** (Kurzform,
settled): `docs/INDEX.md`s `ROADMAP.md`-Zeile war stale, korrigiert; Vollständigkeitsprüfung
„jede `.md` hat eine INDEX-Zeile" nachgeholt, alle 32 verlinkt; Staleness-Grep über
`README.md`/`AGENTS.md`/`docs/PROMPTS.md`/`phase5_ui/CLAUDE.md` — keine weiteren Funde;
`ROADMAP.md`s „Mehrmandantenfähigkeit"-Absatz hatte sich selbst widersprochen, korrigiert.
`pytest -q` → 576/576, Size-Sweep sauber.

**Nachtrag, 2026-08-09, dritter — Step 1 (Werkzeug-Ergonomie) fertig** (Kurzform, settled):
`storage/patch.py` (neu: `TextEdit`/`PatchError`/`PatchResult`/`apply_edits()`), `Store.patch()`,
`mcpserver/receipts.py` (neu), siebtes Tool `patch_item`, `return_body` an allen vier
Schreib-Tools, `update_item` lehnt `visibility`/`share_read`/`share_write` ab. `mcp_smoke.py`
13/13. **V48 geschlossen:** `list[TypedDict]` rendert per `fastmcp` 3.4.4 zu einem brauchbaren
Schema, kein Fallback nötig — belegt über den echten `fastmcp.Client`. Drei Advisor-Funde vor
dem Commit: Kollateralschaden durch Quittungen-als-Default (sieben Tests auf JSON umgestellt),
`update_item`s Riegel war ohne die drei echten Parameter wirkungslos (ergänzt, `fastmcp` hätte
sonst vorher abgelehnt), Plan-Testdateinamen wären fixture-los gewesen (Fixtures folgen §5s
Tabelle, nicht dem Fließtext). Kleine Quittungs-Abweichungen von Plan §1.5.3 dokumentiert:
kein `folder` vor Step 4, Archivieren liefert `op="update"` nicht `op="archive"`. `pytest -q` →
**593 passed** (+17: 5 `test_patch.py` + 5 `test_store.py` + 7 `test_tools.py`). Tabu-Diff
gewahrt: nur `storage/`, `mcpserver/{tools,receipts}.py`, drei Testdateien.

**Nachtrag, 2026-08-09, vierter — zweiter Advisor-Durchlauf, zwei Funde vor Sessionende
behoben:** (1) Hard Rule 8 verlangte `phase1_storage/CLAUDE.md` und `phase2_mcp/CLAUDE.md` im
**selben** Commit wie `storage/patch.py`/`tools.py` — waren stattdessen einen Commit zu spät
nachgezogen. Beide jetzt aktuell: Modul-Status-Zeilen (P6 Step 1 als Zeile 9 je Paket),
Testzahlen 81/92 (`pytest --collect-only -q` nachgezählt), `phase2_mcp/CLAUDE.md`s P2-K-
Entscheidung („kein siebtes Tool") mit datierter Korrektur versehen, dritte Contract-Öffnung in
`phase1_storage/CLAUDE.md` dokumentiert. (2) `test_patch_creates_exactly_one_git_commit` prüfte
`len(log) == 2` (absolute Commitzahl im ganzen Test-Repo) statt das Delta — wäre auch bei einem
Bug in `create()`s Commit-Anzahl grün geblieben. Auf Vorher/Nachher-Differenz umgestellt. 593/593
weiterhin grün, eigener Commit (nicht `--amend`).

**Nachtrag, 2026-08-09, fünfter — Step 2 (Betrieb) fertig, in derselben Sitzung fortgesetzt.**
Plan §4 Step 2 (`docs/concepts/phase6_shares_plan.md:694-709`) ist der einzige Block-A-Step ohne
DoD/Testliste im Plandokument — vier Prosa-Punkte, keine Spezifikation. Zwei Advisor-Pässe vor
bzw. nach der Umsetzung eingeholt (Details unten je Punkt und im Verifiziert-Absatz); die
Ausführungsplanung selbst lag nur als Session-lokale Skizze vor und ist hier vollständig
nacherzählt, kein separates Dokument im Repo.

**1. O2** — `authserver/store.py :: purge_expired()` räumt jetzt auch `token_families` (tot =
nach dem bestehenden Ablauf-Sweep keine Kind-Zeile mehr in `access_tokens`/`refresh_tokens`/
`auth_codes` — deckt widerrufen, natürlich abgelaufen UND abgebrochene Autorisierung mit einem
Prädikat ab, letzteres nennt der Plan-Text nicht explizit, bewusste Erweiterung) und `clients`
(kein verbleibender `token_families`-Eintrag) ab, je mit eigener Altersgrenze:
`TOKEN_FAMILY_RETENTION_S` (30 Tage) und **länger** `CLIENT_RETENTION_S` (90 Tage) — eine
`clients`-Zeile ist die Registrierung, die ein Connector im Claude-Account weiter vorzeigt, und
P5-Q widerruft bei einem Passwortwechsel sofort alle Familien; zu kurze Client-Retention riskiert
„unknown client" beim nächsten Autorisierungsversuch statt eines einfachen Re-Auth. `NOT EXISTS`
statt `NOT IN` (immun gegen NULL-in-Subquery, auch wenn die FK-Spalten heute `NOT NULL` sind).
Reihenfolge zwingend wegen `PRAGMA foreign_keys=ON` (store.py:218): Familien zuerst, dann
Clients, in derselben Transaktion. Die 30-Tage-Grenze zählt ab `COALESCE(revoked_at,
created_at)`, nicht ab `created_at` allein — **zweiter Advisor-Durchlauf, echter Fund vor dem
Commit:** eine per Replay-Erkennung getötete Familie (der Härtetest aus der Phase-4-Mission,
`revoked_reason='refresh_replay'`) wäre unter der `created_at`-only-Fassung binnen 24h wieder
verschwunden, wenn sie schon Wochen alt war — ihr einziger forensischer Beleg gelöscht statt 30
Tage aufbewahrt. `ui_sessions`/`invites` daneben zählten schon immer richtig ab ihrem Ereignis;
`token_families` war beim ersten Entwurf die Ausnahme, jetzt korrigiert, mit eigenem
Regressionstest (`test_purge_expired_keeps_a_family_revoked_today_even_if_born_long_ago`).
+8 Tests in `test_authserver_store.py` (250→258).

**2. Client-Surface-Logging (`ua`, V42)** — landet ausschließlich auf `AccessLogASGI`s
`ev="http"`-Zeile (`_ALLOWED_FIELDS` + 120-Zeichen-Kürzung), nicht auf `ev="tool"`:
`ToolCallLogMiddleware` hat keinen ASGI-Scope-Zugriff, `context.py` steht nicht auf Step 2s
Berührungsliste. Geteilter Zeitstempel mit der `ev="tool"`-Zeile reicht für V42 (welche
Oberfläche stellte diese Anfrage). Verifiziert (nicht nur vom Advisor vermutet):
`TokenScrubbingFilter` (`logging_setup.py:65-77`) scrubbt Dict-**Werte** vor dem Formatter, ist
am `sharefyx.request`-Handler angeschlagen (`_configure_request_logger`) — `ua` bekommt beide
Verteidigungen (Kürzung + Muster-Scrub), nicht nur eine. +3 Tests (`test_request_log.py` 11→13,
`test_logging.py` 8→9).

**3. `diagnose.sh`** — Prüfung 11, INFO-Kategorie (kein `diagnose()`-Abbruch, gleiche Einordnung
wie die Backup-Frische-Prüfung direkt daneben): Alter von `sharefyx-purge.timer`s letztem Lauf
über `systemctl show ... --property=LastTriggerUSec`, WARNUNG mit Enable-Befehl falls nie
gelaufen, sonst WARNUNG ab > 48h. Der zweite Plan-Punkt (verwaiste Space-Namen in `.share.yml`)
bewusst nicht gebaut — die Datei existiert erst ab Step 4, der Plan selbst nennt das „ab Block
B". Kein Unit-Test (Skript hat wie der Rest von `diagnose.sh` keine automatisierten Tests) —
**aber real gegen den echten, auf dieser Maschine laufenden `sharefyx-purge.timer` geprüft**
(Advisor-Vorgabe, zweiter Durchlauf: `bash -n` beweist nur Syntax, nicht Ausgabeformat, genau der
Fehler hinter V13 „Ausgabeformat nie live geprüft"). Diese Session lief zufällig direkt auf der
Heim-VM (bestätigt über `hostname`/`DATA_ROOT`/`systemctl is-active sharefyx-mcp`, siehe
Projekt-Memory) — read-only `systemctl show sharefyx-purge.timer --property=LastTriggerUSec`
lieferte einen echten Zeitstempel (`LoadState=loaded`, `ActiveState=active`), das neue Skript-
Fragment korrekt gegengerechnet: Alter ≈ 18,6h, unter 48h, INFO-Zweig korrekt genommen — sowie
gegen einen nicht existierenden Unit-Namen (leere Ausgabe, `LoadState=not-found`), WARNUNG-Zweig
korrekt genommen. Kein Schreibzugriff, kein `restart`/`enable` — bleibt Nikinger-Sache.

**4. `ui_budget.py`** — neue, eigenständige `_measure_latency()` + `LatencyMetric`-Dataclass
(kein `budget_bytes`/`ok`, eigene JSON-Sektion `"latency"`) für `search_items`/`get_item` (MCP,
echter `mcpserver.app::create_app()`, gleicher Client/Transport-Stack wie `mcp_smoke.py`) und
`GET /api/v1/overview` (Session-Cookie direkt über `AuthStore.create_session()` gemintet, kein
Login-Umweg). Bewusst getrennt von den vier bestehenden Größen-`Metric`s: die hätten
`main()`s Exit-Code — ein live-verifiziertes Abnahme-Artefakt (P5 Zeile 15) — zeitabhängig
gemacht. Jede der drei Messungen macht einen verworfenen Aufwärmlauf vor dem gemessenen Aufruf
(Advisor-Fund, zweiter Durchlauf) — ohne den hätte ein einzelner kalter Aufruf Routen-Setup/
Session-Verhandlung mitgemessen, nicht die eigentliche Frage von P6-I/P6-S beantwortet. Echter
Lauf gegen ein temporäres `DATA_ROOT` (220 Items, dieselbe Saat wie `_measure()`, Hard Rule 2:
Index rekonstruiert sich immer aus den Dateien), **dreifach reproduziert:** `search_items`
95–96 ms/20 KB, `get_item` 5 ms/0,5 KB, `GET /api/v1/overview` **438–453 ms/1,5 KB** — konstant
über alle drei Läufe hinweg, also kein Kaltstart-Artefakt, sondern eine echte, reproduzierbare
Kostenstelle. `/api/v1/overview` aggregiert vermutlich über den vollen Index (P6-S, `Store.
search()` liest weiterhin jede Datei) — genau die Zahl, die die nächste Entscheidung laut Plan
haben sollte, kein Zufallsfund. Kein neuer Test (`ui_budget.py` hatte nie welche, gleiche
Kategorie wie `mcp_smoke.py`).

**Hard Rule 8, fünf Köpfe im selben Commit:** `phase4_auth/CLAUDE.md` (O2-Zeile geschlossen),
`phase2_mcp/CLAUDE.md` (Modul-Status Zeile 10 + „Gesamt"-Zeile neunte Drift-Instanz, 92→95),
`phase3_edge/CLAUDE.md` (Prüfung-11-Ergänzung), `phase5_ui/CLAUDE.md` (`ui_budget.py`-Ergänzung),
dieser Kopf. `docs/INDEX.md`s `phase2_mcp`-Zeile im selben Commit nachgezogen (Testzahl,
Step-2-Erwähnung).

**Verifiziert:** `pytest -q` → **604 passed** (593 + 11 neue, deckt sich exakt). Volle
Testsuite gelaufen, nicht nur die vier neuen Dateien. `ui_budget.py` real ausgeführt (Text UND
`--json`) — Zahlen oben sind aus diesem echten Lauf, keine Schätzung. `mcp_smoke.py --json`
weiterhin 13/13 (Step-1-Baseline unangetastet). `authctl.py purge-expired` nicht gesondert
gegen eine Temp-DB nachgestellt — bereits vollständig über die neuen `purge_expired()`-Tests
abgedeckt, ein zusätzlicher CLI-Probelauf hätte denselben Code-Pfad kein zweites Mal geprüft.

**Status ehrlich, nicht optimistisch:** Step 2 kann nicht ✅ schließen. V42 braucht zwei echte
Tage journald auf der Live-VM; Gate A→B Punkt 3 braucht einen echten Purge-Lauf mit sinkender
`clients`-Zeilenzahl. Beide sind Nikinger-Sache, nicht in dieser Session baubar — Status bewusst
**„gebaut, Live-Teile beim Nikinger"** (P5 Step 8s Präzedenzformulierung), V42 in der
Modul-Status-Tabelle namentlich offen.
