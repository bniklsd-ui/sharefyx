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
updated: 2026-08-13, zweiter -- (Nikinger-Feedback: Wortmarke bekommt eine Versionsnummer, phase5_ui/webui/static, kosmetisch)
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
| 6 | Rechtepolitik (Block B): `storage/acl.py` +`grants_for_space()`/`decision_for()`, `store.py` +`acl_reader`-Property (kleine, dokumentierte Erweiterung über Step 5s Dateiliste hinaus), `mcpserver/permissions.py` (`Surface`, `SharePolicy` ersetzt `OwnSpaceWritable`), `mcpserver/app.py` (Verdrahtung über `store.acl_reader`), `mcpserver/tools.py` (alle sieben Tools auf `acl_of()`+`can_read_item`/`can_write_item` umgestellt, `search_items`/`list_spaces` item-weise statt space-weise gefiltert, `create_item(space=, folder=)`, `update_item(folder=)`), `webui/api.py`+`serializers.py` (dieselbe Umstellung, `Surface.HUMAN` über `SharePolicy.can_read_item_as_human()`/`can_write_item_as_human()` gekapselt — P5-B erlaubt weiterhin nur ein `mcpserver`-Symbol) | 5 | ✅ **gebaut, 2026-08-12** — DoD aus Plan §4 Step 5 erfüllt, alle 12 Pflichttests + Fail-Closed-Folder-Fund + `can_write_item`-visibility-Fix (Advisor-Fund nach dem ersten Commit) abgedeckt; noch nicht live geprüft (kein eigener Abnahmematrix-Punkt) | +10 `phase2_mcp/tests/test_tools.py` (30→40) + 9 `test_permissions.py` (3→12, Datei vollständig neu geschrieben) + 2 `phase5_ui/tests/test_api.py` (27→29) + 2 `test_serializers.py` (7→9), Kollateralkorrekturen in `phase2_mcp/tests/test_app.py`/`phase5_ui/tests/test_overview.py`/conftest-Fixtures (keine neuen Tests, nur Assertions auf die neue ACL nachgezogen); 694 gesamt |
| 7 | Verwaltung und Migration (Block B): `phase6_shares/scripts/spacectl.py` (neu — `create-space`/`list-spaces`/`show`/`add-member`/`remove-member`/`remove-space`/`check`), `phase6_shares/scripts/migrate_visibility.py` (neu — `--dry-run` Default, **kein** Versionssprung), `phase3_edge/scripts/diagnose.sh` Prüfung 12 (verwaiste/kaputte `.share.yml`-Referenzen über `spacectl.py check --json`, INFO/WARNUNG, kein Abbruchkriterium) | 6 | ✅ **gebaut, 2026-08-12** — Details, beide Plan-Abweichungen (DATA_ROOT-Auflösung, kein Index-Rebuild) und die Advisor-Runde davor: Session-Block unten. DoD-Live-Teil (realer dritter Nutzer, echter `diagnose.sh`-Lauf) bleibt Nikinger-Sache wie bei Steps 4/5 | +28 (20 `phase6_shares/tests/test_spacectl.py` [neu] + 8 `test_migrate_visibility.py` [neu]); 722 gesamt |

## Geerbte Contracts

**[2026-08-09, P6 Step 0] Dritte, benannte Öffnung des P1-Contracts** (Plan §1.4): `models.py`
bekommt `folder`/`visibility`/`share_read`/`share_write`, `store.py` bekommt `acl_of()`/`patch()`/
erweiterte `create()`/`update()`/`search()`/`list_spaces()`. Wird in Step 4 umgesetzt, hier nur
angekündigt — nach Phasenabschluss (Step 10) wieder geschlossen, siehe `phase1_storage/CLAUDE.md`.

---

## Session stopped — 2026-08-12, dritter — (Step 6 — Verwaltung und Migration, Block B)

**Auftrag:** Nikinger-Sonderauftrag zu Sessionbeginn — vor jedem Deploy des Sichtbarkeits-
Cutovers mindestens Step 6 bauen (`spacectl.py`/`migrate_visibility.py`), damit die Umstellung
mit richtigem Werkzeug statt einer von Hand editierten `.share.yml` landet. Plan §4 Step 6 war
bereits ausführungsreif (Dateiliste, Unterbefehle, Report-Format, DoD) — per Root-Prompt-Regel
("wenn der Plan detailliert genug ist, das feststellen und atomar entlang seiner Schritte
vorgehen") direkt umgesetzt, kein eigener Planungsdurchlauf nötig. Vor dem ersten Code
`advisor()` konsultiert (Auftrag: unaufgefordert vor substanzieller Arbeit).

**Advisor-Runde vor dem Bau, vier Punkte übernommen:**
1. **Kein `version`-Sprung in `migrate_visibility.py`.** Ursprüngliche Annahme dieser Session
   ("ein Versionssprung wäre vertretbar") war falsch — ein fehlendes `visibility`-Feld hat schon
   vor der Migration den Default `private` (`models.py :: DEFAULT_VISIBILITY`, Frontmatter-
   Vertrag §2.1), nichts Beobachtbares ändert sich. Ein Versionssprung hätte jeder laufenden
   Claude-Instanz mit einer gerade gelesenen `version` einen `ConflictError` untergeschoben, der
   keiner ist — am Tag des Cutovers, an dem Abnahmezeile 8 getestet wird. Bestimmt die gesamte
   Architektur des Skripts: es ruft deshalb nie `Store.update()` auf (das würde pro Item
   committen), sondern schreibt über `storage.files.atomic_write` direkt.
2. **Kein Index-Rebuild nach `--apply` nötig — geprüft, nicht angenommen.** `storage/index.py ::
   row_from_file()` gibt einem fehlenden `visibility`-Feld bereits denselben Default (`"private"`,
   `fields.get("visibility", "private")`) — Datei und Index sagen vor und nach dem Lauf für jedes
   Item dasselbe. Kein `store.rebuild_index()`-Aufruf im Skript.
3. **`STATE_DIRECTORY`-Konvention aus dem Plan ist wörtlich unpassend, sinngemäß richtig.**
   Gegengeprüft: `phase4_auth/systemd/sharefyx-mcp.service` setzt `SPACE_DATA_ROOT` über eine
   eigene, direkt gesetzte `Environment=`-Zeile — unabhängig von `StateDirectory=sharefyx` (das
   trägt nur die Auth-DB). Gemeint war die **Haltung** von `authctl.py :: resolve_db_path()`
   ("aus der Umgebung auflösen, kein stiller Fallback ins Arbeitsverzeichnis"), nicht die
   wörtliche Variable. `mcpserver.config.load_settings()` wäre wiederverwendbar gewesen, aber
   Advisor riet zu einer eigenen vierzeiligen `_resolve_data_root()` je Skript statt einer neuen
   `phase6_shares → phase2_mcp`-Importabhängigkeit für ein einzelnes Feld — kein bestehender
   Code-Pfad außerhalb von `phase2_mcp`/`phase4_auth` importiert `mcpserver.config` bisher
   (gegengeprüft per `grep`), diese Abhängigkeit wäre neu und unbegründet gewesen. Umgesetzt:
   `--data-root`-Flag hat Vorrang, sonst `SPACE_DATA_ROOT` (Pflicht), in beiden Skripten identisch.
4. **Lock einmal für den gesamten `--apply`-Lauf, nicht je Datei.** Ein Flock auf
   `<data_root>/.write.lock` (dieselbe Datei wie `Store._file_write_lock()`, hier eigenständig
   reimplementiert statt als neue `Store`-Fläche exportiert — dieselbe Zurückhaltung wie P6
   Step 5) wird für die komplette Migration bzw. jeden `spacectl.py`-Schreibbefehl gehalten. Ein
   über mehrere Locks interleaved halbmigrierter Zustand mit einem parallel schreibenden Dienst
   wäre schwerer zu erklären als ein kurzzeitig blockierter Dienst.

**`phase6_shares/scripts/migrate_visibility.py` (neu):** `scan()` liest jedes `*.md` unter jedem
Space (inkl. `_archive/` — archivierte Items brauchen `visibility` genauso), meldet nur Items
ohne das Feld. `apply()` schreibt `visibility: private` je gemeldetem Item über
`frontmatter.parse`/`serialize` + `files.atomic_write`, dann **ein** `history.commit()` je Space
(`migrate visibility [<space>]`) — nicht je Item, wie Plan §2.3 verlangt (200 Commits wären
Lärm). `history.ensure_repo()` wird defensiv selbst aufgerufen (nicht von einem vorherigen
`Store()`-Aufruf vorausgesetzt) — sonst würde `history.commit()` gegen ein Verzeichnis ohne
`.git` nur `logger.critical` loggen (nie fatal) und der geforderte Commit bliebe stillschweigend
aus. `--dry-run` ist Default; Report als JSON-Zeilen (`{"id":…,"space":…,"path":…,"before":null,
"after":"private"}`) plus eine Summenzeile (`items_migrated`, `spaces_touched`) auf stdout.

**`phase6_shares/scripts/spacectl.py` (neu):** sieben Unterbefehle. `create-space` legt nur ein
Verzeichnis an — **kein eigener Commit** (Git kennt keine leeren Verzeichnisse, der erste
Item-Write erzeugt den ersten echten Commit), **aber jeder schreibende Unterbefehl inklusive
`create-space` initialisiert über `_DataRootLock.__enter__()` beiläufig ein Git-Repo**
(`history.ensure_repo()`, idempotent — derselbe Aufruf, den `Store.__init__` bei jedem
Dienststart ohnehin macht), falls noch keins existiert. Bewusst genannt statt nur im Code
sichtbar: `create-space` gegen ein brandneues `DATA_ROOT` initialisiert damit Git als
Seiteneffekt, ohne selbst zu committen. `list-spaces`/`show` lesen über `Store`/`AclReader` (Wiederverwendung
statt zweiter Lesepfad). `add-member`/`remove-member` schreiben `<space>/.share.yml` direkt
(eigener, lauter YAML-Loader — anders als `AclReader`, der bei einem kaputten Bestand fail-closed
still eine leere `Grant` zurückgibt, soll ein Operator, der gerade eine Freigabe bearbeitet, einen
kaputten Bestand sofort sehen, nicht stillschweigend überschreiben); `write:` impliziert `read:`
(Plan §1.2.2) — `add-member --write` trägt den Namen deshalb nur in `write:` ein, keine Dopplung
in `read:`. `remove-member` entfernt aus beiden Listen (vollständiger Widerruf, kein Flag nötig)
und löscht die Datei ganz, wenn danach nichts Nennenswertes übrig bleibt (`.share.yml`s eigene
"leer = nicht vorhanden"-Disziplin, analog Frontmatter §2.1). `remove-space --force` löscht den
Verzeichnisbaum (`shutil.rmtree` + ein Commit) — **nicht** ohne `--force` (Trockenlauf-Default,
druckt nur eine Vorschau), warnt immer, dass Git-Historie/Backups den Inhalt trotzdem behalten
(Hard Rule 4/F2), und scannt **vor** dem Löschen alle `.share.yml` im Bestand auf verbleibende
Referenzen auf den zu löschenden Space (Advisor-Fund: sonst produziert `remove-space` selbst
genau die verwaisten Namen, die `check`/Abnahmezeile 24 später melden). `check` (neu, nicht im
Plan-Text benannt, aber von der Step-6-DoD verlangt — "`diagnose.sh` meldet keine verwaisten
Namen" kann nur berichten, was ein YAML-Parser ausgewertet hat, kein zweiter Parser in Bash,
§2.2/V51) meldet `orphan_count`/`broken_count` als JSON.

**`phase3_edge/scripts/diagnose.sh`, Prüfung 12 (neu):** liest `DATA_ROOT`/`VENV` aus
`local.env` (dasselbe Sourcing-Muster wie Prüfung 5), ruft `spacectl.py check --json` über den
venv-Python auf, wertet `orphan_count + broken_count` aus (`python -c` auf dem JSON-Strom,
dasselbe Muster wie `abnahme_run.sh` — kein `jq`, kein zweiter JSON-Parser im Repo). INFO/
WARNUNG-Kategorie wie Prüfung 9/11, kein Abbruchkriterium — DATA_ROOT ist unter dem Dienst
gesetzt, nicht unter der Bash-Session, ein fehlendes `local.env` ist kein Fehlerzustand für
dieses Skript. **Manuell simuliert, nicht nur `bash -n`:** ein Wegwerf-`DATA_ROOT` mit zwei
Spaces und einer Freigabe angelegt, den geteilten Space per `shutil.rmtree` entfernt, Block 12
Zeile für Zeile gegen dieses Szenario gefahren — `orphan_count: 1`, korrekt den entfernten
Namen benannt. Scratch-Verzeichnis danach entfernt.

**Tests, beide Dateien neu (`importlib.util.spec_from_file_location`-Ladepfad wie
`test_authctl.py`, Skripte liegen in keinem Python-Paket):** `test_spacectl.py` (20 Tests:
DATA_ROOT-Auflösung, create/list/show, add/remove-member inkl. write-impliziert-read und
Verwaisungswarnung, remove-space Dry-Run vs. `--force`, `check` sauber/verwaist/kaputt) +
`test_migrate_visibility.py` (8 Tests: Dry-Run-Default schreibt nichts, Report-Inhalt, Version
bleibt unverändert, bereits gesetztes `visibility` bleibt unangetastet, ein Commit je Space bei
mehreren Items, zwei Commits bei zwei Spaces, DATA_ROOT-Auflösung). Beide Dateien injizieren
`env` in `main()` (nie `os.environ` direkt) und filtern `SHAREFYX_*`/`SFX_*` vor dem Aufruf
(P5-Lehre, memory `feedback_test_harness_never_inherits_env` — hier ohne reale Wirkung, da
keines der Skripte `systemctl` aufruft, aber dieselbe Disziplin durchgehalten, nicht erst bei
Bedarf nachgerüstet).

**Zweite Advisor-Runde, nach dem ersten Entwurf, vor dem Commit — ein Fund übernommen:**
`_cmd_remove_member` prüfte anders als `_cmd_add_member` nie, ob der Ziel-Space überhaupt
existiert — bei einem Tippfehler im Space-Namen liefert `_load_share_file()` `{}` (Datei fehlt
ja tatsächlich), `removed` bleibt leer, das Skript druckt „war in keiner Liste" und `EXIT_OK`.
Harmlos im Ergebnis, aber aus dem falschen Grund: die „kein Schreibzugriff"-Eigenschaft hing an
einer leeren Liste, nicht an einer Prüfung — ein Operator, der `remove-member niklsa fabian`
tippt, bekommt eine fröhliche Erfolgsmeldung und glaubt, die Freigabe sei weg, obwohl nie ein
echter Space namens `niklsa` existierte. Behoben: derselbe `ABBRUCH`-Guard wie in `add-member`,
plus `test_remove_member_on_unknown_space_aborts_instead_of_false_success`. **20 statt 19 Tests
in `test_spacectl.py`, 28 statt 27 insgesamt** — Zahlen unten schon korrigiert, nicht als
spätere Drift stehen gelassen (die elf dokumentierten Instanzen dieser Drift-Kategorie in
`phase2_mcp/CLAUDE.md` waren Warnung genug).

**Verifiziert:** `pytest -q` (gesamtes Repo) → **722 passed** (694 + 20 + 8, keine Regression),
Zahl der beiden neuen Dateien per `pytest --collect-only -q` nachgezählt, nicht aus dem
Schreibprozess geschätzt. `git status --short` nach den Testläufen zeigt außerhalb der neuen
Dateien nur `phase6_shares/CLAUDE.md`/`docs/INDEX.md` (Doc-Update) und `phase3_edge/scripts/
diagnose.sh` — kein `storage/`/`mcpserver/`/`authserver/`-Touch, wie für einen reinen
Tooling-Step erwartet.

**Status:** Step 6 ist **gebaut und unit-verifiziert**, nicht live geprüft — insbesondere ist
`migrate_visibility.py --apply` bisher ausschließlich gegen `tmp_path`-Wegwerfverzeichnisse
gelaufen, nie gegen den echten `DATA_ROOT` (Hard Rule: kein Test gegen den echten `DATA_ROOT`
durch Claude Code). DoD hat einen Live-Anteil, der laut Root-Prompt Sache des Nikingers ist
(echter dritter Nutzer, echter `diagnose.sh`-Lauf gegen den realen `DATA_ROOT`) — dieselbe
Aufteilung wie bei Steps 4/5 ("noch nicht live geprüft, kein eigener Abnahmematrix-Punkt"). Kein
MCP-Tool/`storage`-Kern-Code geändert — reine neue Operator-Skripte plus eine
`diagnose.sh`-Prüfung, wie geplant.

**Nächster Schritt (konkret):** Sonderauftrag ("mindestens Step 6") ist erfüllt — Rückmeldung an
den Nikinger vor Fortsetzung. **Empfehlung für den ersten echten Lauf, bevor der
Sichtbarkeits-Cutover live geht:** `migrate_visibility.py --data-root <echter DATA_ROOT>`
(Default `--dry-run`) einmal gegen den realen Bestand laufen lassen, den JSON-Report durchsehen
(Anzahl migrierter Items plausibel? welche Spaces betroffen?), **erst danach** `--apply` — genau
der Grund, warum dieses Skript existiert statt einer von Hand editierten `.share.yml`. Falls
weiter im Plan: Step 7 (UI Dateisystem, `webui/shares.py`, `app.js`-Split, Freigabedialog +
Re-Auth) ist der nächste Schritt, deutlich größerer Umfang (JS ohne Unit-Tests laut
P5-Konvention, `[VERIFY]` V43/V50) — kein Selbstläufer aus dieser Session heraus.
Gate-A→B-Punkt-3-Erinnerung bleibt unverändert gültig (frühestens 2026-08-28).

**Nachtrag 2026-08-13, vor Step 7:** der Nikinger brachte zwei Betriebs-Reports einer
arbeitenden Claude-Instanz mit — vermeintlich kein Weg, `status`/`links` ohne `patch_item`/
`append_to_item` zu ändern. Geprüft statt übernommen: `update_item` konnte das schon seit P6
Step 1 (alle Felder unabhängig optional, `body` weglassen rührt den Body nicht an) — die
Instanz griff nur zu den zwei Tools, deren Namen „gezielt" suggerieren, weil deren
Beschreibung das nicht ausschloss. Kein Code-/Schema-Fix nötig, nur die drei
Tool-Descriptions in `mcpserver/tools.py` präzisiert (Details + Testlauf:
`phase2_mcp/CLAUDE.md`s Korrekturnotiz vom selben Datum). Kein eigener Plan-Step, kein
Einfluss auf Step 7.

**Nachtrag 2026-08-13, zweiter — UI-Kleinigkeit „on the fly":** der Nikinger meldete direkt im
Anschluss, die Wortmarke oben links zeige keine Versionsnummer, mit Vorschlag (dieselbe
Schriftart, kleiner, Phase 6 = v2). Umgesetzt in `phase5_ui/webui/static/{app.html,app.css}`
(`.rail__version`-Span neben `.rail__brand`, erbt `font-family`, 9px/60% Deckkraft) — Details,
Begründung der Breakpoint-Interaktion und Testabdeckung stehen in `phase5_ui/CLAUDE.md`s
Korrekturnotiz vom selben Datum, nicht doppelt hier. Visuell gegengeprüft: Playwright/Chromium
headless gegen die echte `app.css` (Datei-URI, `link href` temporär auf einen absoluten Pfad
umgeschrieben, damit `file://` die Stylesheet-Referenz auflöst — Serverstart wäre für eine reine
CSS-Sichtprobe unverhältnismäßig gewesen), Screenshot zeigt „SHAREFYX ᵛ²" wie gewünscht, danach
verworfen (kein Repo-Artefakt). Reine `webui/static/`-Änderung, kein Python-Code — `pytest`
722/722 unverändert als Regressionsprobe, kein neuer Test (JS/CSS bleiben laut P5-T
unit-ungetestet).
