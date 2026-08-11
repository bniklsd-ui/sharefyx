---
status: live
purpose: Phase-Head Freigaben, Ordner, Werkzeug-Ergonomie — Scope, harte Regeln, Modulstatus, aktueller Session-Handover
read-when: Arbeiten in phase6_shares/ oder an den in P6-C genannten Dateien in storage/mcpserver/webui — zuerst lesen, zusammen mit dem neuesten Session-stopped-Block
detail: L2
up: ../CLAUDE.md
down:
  - ../docs/concepts/phase6_shares_plan.md         # voller Plan, Entscheidungen P6-A–P6-AC, Steps 0–10
  - ../docs/concepts/PHASE5_CLOSEOUT_HANDOVER.md   # Herkunft der offenen Entscheidungen §4.1–§4.6, [VERIFY]-Bilanz V27–V38
  - ./SESSIONS_ARCHIVE.md                          # Steps 0-2 verbatim, L3, kein Softcap
updated: 2026-08-10 (Kopf unter Softcap rotiert -- Steps 0-2 nach SESSIONS_ARCHIVE.md; V42-Fenster startet 2026-08-10)
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
| 3 | Betrieb: O2 (`authserver/store.py :: purge_expired()` räumt `token_families`/`clients` ab, zwei neue Retention-Konstanten), Client-Surface-Logging (`ua`-Feld auf `AccessLogASGI`, V42), `diagnose.sh` Prüfung 11 (Purge-Frische, INFO), `ui_budget.py :: _measure_latency()` (P6-I/P6-S, eigene `LatencyMetric`, kein Exit-Code-Einfluss) | 2 | ✅ **gebaut, Live-Teile beim Nikinger** — V42 (echtes journald, zwei Tage) und Gate-A→B-Punkt 3 (realer Purge-Lauf, `clients`-Zeilenzahl sinkt) sind live-Aufgaben, nicht in dieser Session baubar | +11 (8 `phase4_auth/tests/test_authserver_store.py` + 2 `phase2_mcp/tests/test_request_log.py` + 1 `phase2_mcp/tests/test_logging.py`); 604 gesamt |
| 4 | Update-Log und Banner: `authserver/store.py` Schema 3 (`users.seen_update_id`), `webui/updates.py` (neu, Parser), `webui/api.py` (+`GET /api/v1/updates`, +`POST /api/v1/updates/seen`), `webui/static/js/updates.js` (neu, Banner + Konto-Dialog-Link), `app.html`/`app.css`, `deploy.sh`-Gate (P6-X), `docs/UPDATE_LOG.md` (neu, erster Eintrag) | 3 | ✅ **gebaut, Gate-A→B-Punkt 4 vollständig live bestanden** (Banner-Hälfte 2026-08-10, Fabian-Hälfte 2026-08-11, siehe Session-Block) | +16 (3 `phase4_auth/tests/test_authserver_store.py` [258→261] + 7 `phase6_shares/tests/test_updates.py` [neue Datei] + 2 `phase5_ui/tests/test_api.py` + 3 `phase5_ui/tests/test_deploy_scripts.py` + 1 `phase5_ui/tests/test_static_routes.py`); 620 gesamt |

## Geerbte Contracts

**[2026-08-09, P6 Step 0] Dritte, benannte Öffnung des P1-Contracts** (Plan §1.4): `models.py`
bekommt `folder`/`visibility`/`share_read`/`share_write`, `store.py` bekommt `acl_of()`/`patch()`/
erweiterte `create()`/`update()`/`search()`/`list_spaces()`. Wird in Step 4 umgesetzt, hier nur
angekündigt — nach Phasenabschluss (Step 10) wieder geschlossen, siehe `phase1_storage/CLAUDE.md`.

---

## Session stopped — 2026-08-09 (Step 0 — Haushalt, Verifikation, Regeländerungen)

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
5. **V42 (Step 2, weiterhin offen) — Fenster startet 2026-08-10, nicht erst „irgendwann in den
   nächsten zwei Tagen".** Der Deploy/Restart vom 2026-08-09 hat `journald` faktisch geleert
   (neuer Prozess, PID-Wechsel); der erste Tag mit durchgehend echtem Traffic unter dem neuen
   `ua`-Feld ist heute. Frühestens **2026-08-12** prüfen (`grep '"ev":"http"'` in den Logs,
   `ua`-Werte über beide Oberflächen — claude.ai/Desktop vs. Claude Code — vergleichen).
   **Aktive Nutzung während des Fensters ist erwünscht, nicht zu vermeiden** — V42 fragt genau
   danach, ob echte Clients zuverlässig einen `User-Agent` senden; ein künstlich ruhiger VM-
   Zeitraum würde weniger Signal liefern, nicht mehr. Diese Session selbst hat bereits reale
   `ua`-Werte erzeugt (Connector-Reconnect, `patch_item`-Tests) — die zählen mit.
6. **Gate-A→B-Punkt 3** — **versucht, 2026-08-09, korrekt noch nicht abgeschlossen** (Nachtrag
   unten): `clients`/`token_families` sind noch zu jung für die 30/90-Tage-Grenze. Frühestens
   ab 2026-08-28 erneut prüfen (`authctl.py purge-expired`, gegen den echten Zeilenrückgang).

Erst wenn alle vier Gate-Punkte stehen, beginnt Step 4 (Storage-Fundament, Block B) — nicht
vorher, das Gate ist im Plan hart. V42 blockiert das Gate nicht, sollte aber nicht vergessen
werden.

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

**Softcap-Warnung:** dieser Kopf ist nahe am 40KB-Softcap. Wenn Step 4 einen neuen `## Session
stopped`-Block eröffnet, sind die Step-0/1/2-Nachträge die Kompressionskandidaten — verbatim
nach `SESSIONS_ARCHIVE.md` (neue Datei), Muster wie `phase4_auth/CLAUDE.md`s Steps-0–6a-
Verschiebung: `sed -n`, Byte-Identität vor dem Löschen geprüft.
