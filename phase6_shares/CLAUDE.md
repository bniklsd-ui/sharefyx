---
status: live
purpose: Phase-Head Freigaben, Ordner, Werkzeug-Ergonomie — Scope, harte Regeln, Modulstatus, aktueller Session-Handover
read-when: Arbeiten in phase6_shares/ oder an den in P6-C genannten Dateien in storage/mcpserver/webui — zuerst lesen, zusammen mit dem neuesten Session-stopped-Block
detail: L2
up: ../CLAUDE.md
down:
  - ../docs/concepts/phase6_shares_plan.md         # voller Plan, Entscheidungen P6-A–P6-AC, Steps 0–10
  - ./ITEM_MOVE_PLAN.md                            # Zusatzplan zu Step 7: Item-Verschieben (Ordner+Space) + Textfarben, P6-AD–P6-AJ
  - ../docs/concepts/PHASE5_CLOSEOUT_HANDOVER.md   # Herkunft der offenen Entscheidungen §4.1–§4.6, [VERIFY]-Bilanz V27–V38
  - ./SESSIONS_ARCHIVE.md                          # Steps 0-6 verbatim (sechs Eintraege), L3, kein Softcap
updated: 2026-08-13, siebter -- (Step 7 Commits 0+1+2+3+4+5a gebaut+verifiziert+committet: app.js in zehn ES-Module gesplittet, echter Ordnerbaum, Sichtbarkeits-Chip, Ordner anlegen+Verschieben per Menue (K4-Fix), Drag & Drop, Re-Auth-Gate Backend-Haelfte (5a, Freigabe-Dialog auf 5b verschoben -- Split-Begruendung im Session-Block, Advisor-Fund: password/totp duerfen nie in store.update() landen); Tabu-Diff-Regelfehler seit Commit 0 gefunden+korrigiert (P5-B statt P6-C geprueft, folgenlos); 746 gruen; atomarer Checkpoint nach jedem Commit, Nikinger-Weisung, ein Advisor-Aufruf pro Commit)
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
| 8 | Lesbarkeit der Textfarben (`ITEM_MOVE_PLAN.md` §3, P6-AD/AE): `phase5_ui/webui/static/app.css` — `--text-muted`/`--text-faint` kalibriert angehoben, neues `--text-placeholder`, `.input::placeholder` darauf umgehängt. **Nachtrag, Nikinger-Feedback vor dem Deploy:** Wortmarke „sharefyx" + Versionsbadge (jetzt `v2.1`, `app.html`) sowie alle Versionsnummern aus den Dateien (`recent-row__meta`, `.editor__version`, `.version-band__number`, `ro-meta`) jetzt `var(--text)` statt `--text-faint`/`--text-muted` — neue Klasse `.version-num` trennt die Versionsnummer farblich vom gedämpften Begleittext im selben Element (`app.css`/`app.js`) | 7a | ✅ **gebaut, Deploy beim Nikinger** — Kontrastwerte bereits in `ITEM_MOVE_PLAN.md` §3.1 protokolliert (durchgerechnet vor dieser Session); Sichtprobe zweimal per In-Process-Server + Screenshot gegen die echte `app.css`/`app.js` (Login-Seite, Liste mit Chips, Editor mit Meta-Panel — alle drei beide Male gesehen, nicht behauptet). Deploy braucht Sudo für den Neustart, außerhalb dessen, was Claude Code selbst kann (Präzedenz: Steps-4–6-Cutover, `SESSIONS_ARCHIVE.md`) | 0 (P5-T: JS/CSS bleiben unit-ungetestet; `pytest` unverändert als Regressionsprobe — 724 gesamt vor UND nach beiden Teilen dieser Session, keiner davon neu) |
| 9 | UI Dateisystem (Block B), Commit 0/7 — `app.js` (1525 Zeilen, ein `initShell()`-Closure) entlang der bestehenden Kommentar-Nahtstellen in zehn ES-Module unter `phase5_ui/webui/static/js/` aufgeteilt (`app`/`api`/`state`/`tree`/`list`/`editor`/`markdown`/`dialogs`/`toasts`/`updates`), `state.js` als einzelnes mutierbares Objekt (von allen Importern geteilt, Ersatz für den Closure-`state`), jedes Modul ein `init(deps)`, das der neue schlanke `app.js` beim Bootstrap der Reihe nach aufruft. Bisheriges Zwei-Skript-Modell (`js/updates.js` als globales Skript vor `app.js`, `window.SharefyxUpdates`) entfällt — `updates.js` ist jetzt selbst ein Modul, `app.html`/`pages.py` laden nur noch `<script type="module" src=".../js/app.js">`. `ui_budget.py` zählt die Nutzlast jetzt über `js/*.js`-Glob statt fester Namen | 7 | ✅ **gebaut, noch nicht deployt** — CSP (`script-src 'self'`) erlaubt Same-Origin-`type="module"` ohne Header-Änderung (V50 geschlossen); Sichtprobe golden path (Login → Liste → bestehendes Item öffnen+bearbeiten+speichern v1→v2 → neu anlegen) per Zwei-venv-Playwright-Skript, fünf Screenshots gesehen, nicht nur behauptet | 0 (P5-T: JS bleibt unit-ungetestet; fünf bestehende Tests in `test_static_routes.py` auf die neue Modulstruktur umgeschrieben, keiner neu; 724 gesamt unverändert) |
| 10 | UI Dateisystem (Block B), Commit 1/7 — echter Ordnerbaum, kein Backend-Fund nötig (`GET /api/v1/items?folder=` existierte bereits, `GET /api/v1/spaces` trug `folders`/`members` schon, nur `app.js` rief die Route nie ab). `list.js :: loadOverview()` holt jetzt `/overview`+`/spaces` per `Promise.all`, mischt `folders`/`members` nach Name in die Space-Objekte. `tree.js`: `buildFolderTree()` (flache Pfadliste → ≤2-stufiger Baum, reines Splitten auf „/", da `MAX_FOLDER_DEPTH` serverseitig gilt), `renderRealFolders()` reused `.tree__folder` (neue Modifier-Klasse `.tree__realfolder--child` nur für die Einrückung der zweiten Ebene), `navigate()`/`navigateFolder()` jetzt exklusiv (`state.folder`/`state.filter` nie beide gesetzt). `list.js`: `filterParams()`/`renderCrumb()`/Leerzustand-Text folder-bewusst gemacht | 7 | ✅ **gebaut, noch nicht deployt** — Sichtprobe mit zwei echten, verschachtelten Ordnern (`Projekte`/`Projekte/Backend`, serverseitig zu `projekte`/`projekte/backend` slugifiziert, P6-Q — Baumdarstellung ist davon unabhängig, reine String-Weiterreichung): Verschachtelung im Baum sichtbar, Klick navigiert **und** filtert exakt (nicht Präfix, V55) auf beiden Ebenen, per Playwright-Assertions auf die tatsächlich gerenderten Zeilentitel erzwungen, nicht nur der Screenshot. Advisor-Fund vor dem Commit, geprüft statt blind gefixt: `navigateFolder()` setzt `state.filter=null`, `dialogs.js :: openCreateDialog()` liest `state.meta.buckets[state.filter]` ungeschützt — JS stringifiziert einen `null`-Schlüssel zu `"null"`, kein `TypeError`, derselbe Fallback-Pfad wie beim typlosen Bucket „Archiv" heute schon; per Node-Check UND echtem Browserlauf (Konsolenfehler-Listener, „+" während `projekte/backend` aktiv) bestätigt, **kein Fix nötig**. Offen für Commit 3 (folder-bewusstes Anlegen): der aktuelle Fallback „leerer Ordner → Typ Notiz" ist ein stiller Default, keine bewusste Entscheidung für echte Ordner | 0 (P5-T: JS bleibt unit-ungetestet, kein jsdom-Zusatzlauf — die echte Browserprobe deckt strenger ab; 724 gesamt unverändert) |
| 11 | UI Dateisystem (Block B), Commit 2/7 — Sichtbarkeits-Chip, kein Backend-Fund nötig (`visibility`/`share_read`/`share_write` stehen bereits auf `summary_to_json()`, P6 Step 5). `list.js`: neue `visibilityLabel()`/`visibilityChip()`, in `renderList()`s Zeilen verdrahtet (`.list__row-meta` von reinem Text auf Flex mit Meta-Text + Chip umgebaut). `app.css`: `.visibility-chip`/`.visibility-chip--shared` (gedämpft vs. `--ok`-grün), reused `.list__row-meta`s bestehende Fläche | 7 | ✅ **gebaut, noch nicht deployt** — Sichtprobe mit vier Items (privat/nur-ich/geteilt/Randfall), alle drei geplanten Chip-Zustände + der Randfall per Playwright-Assertion auf gerenderten Chip-Text erzwungen (nicht nur Screenshot), Konsolenfehler-Listener sauber. **Benannte Abweichung vom Plan-Wortlaut, gefunden beim Nachlesen von `acl.py`/`permissions.py` vor dem Commit:** der Plan prüft `visibility` zuerst („private" → unbedingt „privat"), aber `acl.py :: decision_for()` verundet `share_read`/`share_write` immer in `AclDecision.read`/`write`, unabhängig von `visibility` — nur `Surface.AGENT` fragt `visibility` (P6-P), nie ein Mensch. Ein Item mit `visibility=private` UND einer echten Freigabe ist für den Freigegebenen faktisch lesbar, erreichbar schon heute über ein rohes `PATCH /api/v1/items/{id}` (`_items_patch` hat keine Feld-Whitelist) — nicht erst über Commit 5s künftigen Dialog. Dispatch umgestellt: `share_read`/`share_write` non-empty entscheidet zuerst, `visibility` nur als Fallback ohne Freigaben — ein vierter Testfall (`visibility=private`+`share_read=[fabian]`) beweist den Unterschied, zeigt korrekt „geteilt mit fabian" statt „privat". **Zweiter, nicht blockierender Punkt:** der Chip erscheint identisch für Items aus fremden, geteilten Spaces (`renderList()` ist derselbe Codepfad für jeden Space) — das sind ACL-Metadaten, keine Fließtext-Bodies, Hard Rule 4s `<untrusted_content>`-Wrapping betrifft das nicht (derselbe Schnitt wie `overview_row_to_json()`s `snippet`-Auslassung, nur umgekehrt: hier ist die Metadaten-Anzeige bewusst, nicht der Fließtext) | 0 (P5-T: JS bleibt unit-ungetestet, kein jsdom-Zusatzlauf — die echte Browserprobe deckt strenger ab; 724 gesamt unverändert) |
| 12 | UI Dateisystem (Block B), Commit 3/7 — Ordner anlegen + Verschieben per Menü, K4-Fix, erster echter Backend-Touch dieses Steps (P6-C erlaubt `storage/` explizit). `store.py :: ensure_folder(space, folder)` (neu, `mkdir(parents=True, exist_ok=True)` unter `self._lock`, kein Git-Commit, keine Content-Datei — reine Verzeichnisoperation). `api.py`: neue `POST /api/v1/spaces/{space}/folders` (Eigentümer-Riegel wie `_items_patch`s `folder`-Feld), `_items_post`-Whitelist um `"folder"` erweitert (K4). `tree.js`: „+ Ordner"-Zeile fürs eigene Space, öffnet `dialogs.js :: openNewFolderDialog()`. `list.js`: Verschieben-Knopf („→") pro Zeile — als GESCHWISTER von `.list__row`, nicht darin verschachtelt (zwei `<button>` ineinander ist ungültiges HTML), `<li>` deshalb neu Flex (`app.css`). `dialogs.js`: zwei neue Dialoge, `openNewFolderDialog()`/`openMoveDialog(item)`. `app.js`: kleine, dokumentierte Abweichung vom Plan-Dateiwortlaut — die beiden neuen Dialoge in `anyOverlayOpen()`/die Escape-Behandlung aufgenommen, dieselbe Konsistenz wie jeder andere Dialog hier | 7 | ✅ **gebaut, noch nicht deployt** — Details, beide Interpretationsentscheidungen und die zwei Advisor-Funde: Session-Block unten | +9 (4 `phase1_storage/tests/test_store.py`: `ensure_folder()` erstellt/idempotent/lehnt Tiefe>2 und leeren String ab + 5 `phase5_ui/tests/test_api.py`: `test_create_item_accepts_folder` [K4] + vier Endpunkt-Tests [erstellt sichtbaren leeren Ordner, lehnt fremden Space auch mit `write:`-Grant ab, lehnt Tiefe>2/reservierten Namen ab]); Charakterisierung erneut byte-identisch grün (P6-D); 733 gesamt |
| 13 | UI Dateisystem (Block B), Commit 4/7 — Drag & Drop, additiv auf Commit 3, kein neuer Backend-Pfad (P6-AB: Menü-Knopf bleibt Pflicht-Alternative). `list.js :: moveItemToFolder(item, folder)` (neu, aus `dialogs.js`s bisher dort inline stehendem `PATCH`-Aufruf extrahiert — geteilter Schreibpfad für Menü UND Drag & Drop, Erfolgs-/Fehler-Rückmeldung bleibt bewusst bei den beiden Aufrufern statt mitextrahiert, weil der Menü-Pfad einen Dialog offen halten muss und der Drag-Pfad keinen hat). `list.js`: `<li>` (nicht der Button) trägt `draggable`/`dragstart`/`dragend`, dieselbe `movable`-Bedingung wie der Menü-Knopf. `tree.js`: neue `bindFolderDropTarget()`, `dragover`/`dragleave`/`drop` nur auf `folderButton()`-Knoten im **eigenen** Space (`space.own`) — der Server lehnt fremde `folder`-Änderungen ohnehin ab, das Gating hier ist reine UX. `app.css`: Ziehgriff-Cursor + gedimmte Zeile während des Ziehens, gestrichelte Kontur am Drop-Ziel (bewusst optisch von `[aria-current]` unterschieden) | 7 | ✅ **gebaut, noch nicht deployt** — Details, inkl. des Refactor-Regressionsbeweises: Session-Block unten | 0 (P5-T: JS bleibt unit-ungetestet; 733 gesamt unverändert — Playwright-`drag_to()`-Lauf statt jsdom, siehe Session-Block, ist Entwicklungshilfe dieser Session, kein Teil der Suite) |
| 14 | UI Dateisystem (Block B), Commit 5a/7 — Re-Auth-Gate (Backend-Hälfte, P6-N), Freigabe-Dialog/Re-Auth-Mini-Formular auf Commit 5b verschoben (Session-Block begründet den Split). `storage/acl.py`: `AclDecision` bekommt rohe `share_read`/`share_write` (Defaults, bestehende Konstruktionsstellen unverändert). `webui/shares.py` (neu): `ShareState`, `widens()` (echte Obermenge auf `AclDecision.read`/`.write`, `visibility` fließt strukturell nie ein), `require_share_reauth()` (wirft `ApiError("reauth_required")`, Signatur um `body`/`userdir`/`throttle`/`auth_store` erweitert — die Plan-Skizze in §1.2.5 deckt die tatsächliche Credential-Prüfung nicht ab). `webui/errors.py`: elfter Code `reauth_required:403`. `webui/api.py :: _items_patch`: `before`/`after`-`ShareState` aus `acl`/Body gebaut, Gate läuft VOR `store.update()`; `password`/`totp` werden unabhängig vom Gate-Ausgang nie an `store.update()` weitergereicht (Advisor-Fund, sonst Frontmatter-Leck, Hard Rule 1); `api_routes()` bekommt sechsten Parameter `users: UserDirectory`. `mcpserver/app.py` zieht mit `oauth.users` nach | 7 | ✅ **gebaut, noch nicht deployt** — Details, Advisor-Fund und der Commit-5a/5b-Split: Session-Block unten | +13 (8 `phase6_shares/tests/test_shares.py` [neu, `widens()`-Wahrheitstabelle] + 5 `phase5_ui/tests/test_api.py` [Gate ausgelöst ohne/mit falschen Credentials, Gate erfüllt+Credential-Leck-Check, keine Auslösung bei Verkleinerung/reiner Inhaltsänderung]); Kollateralkorrekturen (kein neuer Test): `phase5_ui/tests/{conftest,test_overview}.py` + drei `test_api.py`-Fixtures um `confirmed_users` als sechstes `api_routes()`-Argument ergänzt, ein `mock_store.acl_reader.decision_for.return_value` gesetzt (unkonfigurierter `MagicMock` scheitert an `>` mit `TypeError`, nachgeprüft); `phase5_ui/scripts/{ui_budget,ui_smoke}.py` zogen ihre eigenen `api_routes()`-Aufrufe nach, beide real gegen ein Temp-`DATA_ROOT` gelaufen (12/12 bzw. `all_within_budget:true`); 746 gesamt |

## Geerbte Contracts

**[2026-08-09, P6 Step 0] Dritte, benannte Öffnung des P1-Contracts** (Plan §1.4): `models.py`
bekommt `folder`/`visibility`/`share_read`/`share_write`, `store.py` bekommt `acl_of()`/`patch()`/
erweiterte `create()`/`update()`/`search()`/`list_spaces()`. Wird in Step 4 umgesetzt, hier nur
angekündigt — nach Phasenabschluss (Step 10) wieder geschlossen, siehe `phase1_storage/CLAUDE.md`.

---

## Session stopped — 2026-08-13, siebter — (Step 7 Commit 0: JS-Split in ES-Module)

**Kontextbruch:** die vorige Session (dieser Auftrag, Commit 0 aus `serialized-seeking-aurora.md`)
lief in ein Kontextlimit, ihr letzter sichtbarer Output war „724/724 grün, Tabu-Diff sauber —
Advisor vor dem Schreiben der Doku konsultieren", aber ohne Doku-Update und ohne Commit. Diese
Session hat nichts blind übernommen — jede Behauptung wurde am echten Repo-Stand nachgeprüft, bevor
sie hier steht.

**Nachgeprüft, nicht nur behauptet:** `git status --short`/`git diff --stat` bestätigen exakt
Commit 0 aus dem Plan — `app.js` (1525 Zeilen) gelöscht, ersetzt durch zehn ES-Module unter
`js/` (`api`/`app`/`dialogs`/`editor`/`list`/`markdown`/`state`/`toasts`/`tree` neu, `updates.js`
umgebaut), `app.html`/`pages.py`/`ui_budget.py`/`test_static_routes.py` mitgezogen. Tabu-Diff:
`git diff --name-only` gegen `storage/`/`mcpserver/{tools,permissions,server}.py` liefert nichts
(P5-B unverletzt — dieser Commit rührt ausschließlich `phase5_ui/`/`docs/` an). `pytest -q` mit
env-gestrippter Shell (`SHAREFYX_*`/`SFX_*`, Lehre aus einem früheren Incident) selbst erneut
gelaufen: **724 passed**, deckungsgleich mit der Behauptung der vorigen Session.

**Sichtprobe (Pflicht laut Plan-DoD für Commit 0, „höchstrisikoreichster Commit"):** fünf
Screenshots aus der vorigen Session im Scratchpad gefunden und selbst angesehen (`Read`, nicht nur
Dateinamen vertraut) — `step7_split_{login,list,editor,after_create,after_save}.png`. Treiber
(`screenshot_client_split.py`) im Zwei-venv-Muster wie in Step 7a: Projekt-`.venv` startet den
echten `uvicorn` gegen ein Wegwerf-`DATA_ROOT`, `svg-venv`s Python treibt Playwright als separaten
Prozess — kein `pip install playwright` im Projekt-`.venv`, die in Step 7a korrigierte Grenze blieb
diesmal von Anfang an eingehalten. Abgedeckter Pfad, am Skript nachvollzogen: Login → Liste (Item
„Kontrast pruefen" sichtbar) → **bestehendes Item aus der Liste angeklickt** (`.nav-item`/
`.recent-row`/`[data-item-id]`, nicht der Anlegen-Dialog) → Text bearbeitet, gespeichert, v1→v2
bestätigt im Screenshot → separat: neues Item über den Anlegen-Dialog erzeugt. Advisor hat vor
diesem Block genau hier nachgehakt (Verwechslungsgefahr Anlegen- vs. Öffnen-Pfad, weil beide
Editor-Screenshots ähnlich aussehen) — am Treiberskript verifiziert: `step7_split_editor.png` ist
der Öffnen-Pfad (Zeilen 30-34 des Skripts, Klick auf ein Listenelement), `step7_split_after_create`
der separate Anlegen-Pfad. Beide DoD-Pfade (öffnen+bearbeiten+speichern, neu anlegen) damit
tatsächlich abgedeckt, nicht nur dem Namen nach.

**Nicht neu gebaut, nur geprüft:** der Code, die Tests und die Screenshots stammen aus der
vorigen (kontextlimitierten) Session — diese Session hat ausschließlich verifiziert, dokumentiert
und committet. Kein eigener Codebeitrag in diesem Block.

**Verifiziert:** `pytest -q` 724 passed (env-gestrippt, s. o.). Tabu-Diff sauber. Fünf
Golden-Path-Screenshots gesehen, Öffnen- vs. Anlegen-Pfad am Treiberskript disambiguiert. Advisor
vor diesem Commit konsultiert (Fund: Screenshot-Pfad-Verwechslungsgefahr, hier behoben, s. o.).

**Nächster Schritt (konkret):** Commit 0 ist fertig dokumentiert und wird jetzt committet. Laut
Plan (`serialized-seeking-aurora.md`, Nikinger-Entscheidung „self-pace gegen Kontextbudget,
checkpointen statt alle sieben Sub-Commits unbeaufsichtigt durchbauen") ist das der geplante
Checkpoint nach einem Kontextbruch — nicht blind in Commit 1 weiterlaufen. Für den Nikinger: Commit
0 ist grün und deploybar (zusammen mit Step 7a, das weiterhin auf den Sudo-Neustart wartet); ob
diese Session in Commit 1 (echter Ordnerbaum im Tree) weiterbaut oder hier für eine
Nikinger-Rückmeldung pausiert, ist eine Scope-Entscheidung, keine technische.

**Nachtrag, Commit 1/7 — echter Ordnerbaum, auf Nikinger-Weisung gebaut** ("Wenn alles grün ist,
baut diese Session den nächsten Schritt, allerdings atomar nach jedem Schritt stoppen" — dieselbe
Session, kein Kontextbruch, deshalb Nachtrag statt neuer Rotation). Umfang, Code, Verifikation:
Modul-Tabelle oben, Zeile 10. Kein Backend-Fund, kein Backend-Commit — reiner Frontend-Schnitt wie
geplant.

**Advisor-Runde, zweimal, beide vor diesem Commit:** erste Runde bestätigte den Merge/die
Baumlogik/die Exklusivität von `state.folder`/`state.filter`, benannte aber eine Lücke — die
Sichtprobe deckte den Anlegen-Knopf **während ein echter Ordner aktiv ist** nicht ab, und
`dialogs.js :: openCreateDialog()` (von diesem Commit nicht angefasst) liest
`state.meta.buckets[state.filter]` ohne Guard. Nachgeprüft statt geglaubt: ein Node-Einzeiler
zeigt, dass ein `null`-Objektschlüssel zu `"null"` stringifiziert wird (kein `TypeError`), und ein
echter Browserlauf mit `pageerror`/`console`-Listener bestätigt das live — Dialog öffnet sauber,
Typ fällt auf „Notiz" zurück, keine Konsolenfehler. **Zweite Runde bestand nur noch darauf, das
korrekt zu benennen** (kein Fund, kein Fix — die erste Formulierung „TypeError" war die Vermutung
des Advisors, nicht das tatsächliche Verhalten) und einen Satz für Commit 3 zu hinterlassen: der
„Notiz"-Fallback für Ordner ohne Typbezug ist ein stiller Default, keine bewusste Wahl.

**Verifiziert:** `pytest -q` 724 passed (env-gestrippt), unverändert. Tabu-Diff sauber (reiner
`phase5_ui/webui/static/`-Diff: `app.css`, `js/{list,state,tree}.js`). Zwei-venv-Playwright-Lauf
gegen ein Wegwerf-`DATA_ROOT` mit drei Items (kein Ordner, `projekte`, `projekte/backend`):
Baum zeigt beide Ebenen korrekt eingerückt, Klick auf `projekte` filtert exakt auf
„Projekt-Kickoff" (nicht auf das Backend-Item — bestätigt `search(folder=)`s Exaktheit statt
Präfix, V55), Klick auf `projekte/backend` exakt auf „API-Design", „+" während `projekte/backend`
aktiv öffnet den Dialog fehlerfrei. Alle Assertions am tatsächlich gerenderten DOM (Playwright-
Locators auf `data-folder`/Zeilentitel), nicht nur Screenshots angesehen.

**Nächster Schritt (konkret):** Checkpoint nach Nikinger-Weisung — Commit 1 ist fertig
dokumentiert und wird jetzt committet, dann stoppt diese Session wieder für eine Rückmeldung
(dieselbe atomare Taktung wie nach Commit 0). Commit 2 (Sichtbarkeits-Chip, reine Frontend-Anzeige,
keine Backend-Änderung laut Plan) ist der nächste Kandidat, falls der Nikinger weiterbauen lässt.

**Nachtrag, Commit 2/7 — Sichtbarkeits-Chip, auf Nikinger-Weisung gebaut** ("go on with next
step, atomar, stop before doing additional steps" — Nikinger schränkte diesmal zusätzlich ein:
nur EIN Advisor-Aufruf pro Arbeitszyklus, Kontextgründe). Umfang, Code, Verifikation:
Modul-Tabelle oben, Zeile 11.

**Ein echter Fund, kein Advisor-Aufruf gebraucht:** vor dem einzigen Advisor-Durchlauf dieser
Runde `acl.py`/`permissions.py` gelesen, um die Plan-Vorgabe („visibility zuerst prüfen") gegen
den echten Zugriffscode zu prüfen — `decision_for()` verundet Freigaben immer, unabhängig von
`visibility`; nur die Agentenfläche (P6-P) fragt `visibility` überhaupt. Ein `private`-Item mit
einer Freigabe ist für den Freigegebenen also real lesbar, und `_items_patch` hat keine
Feld-Whitelist — dieser Zustand ist heute über einen rohen `PATCH`-Aufruf erreichbar, nicht erst
über einen künftigen Freigabe-Dialog (Commit 5). Ein Chip, der dort „privat" zeigt, hätte den
Eigentümer belogen. Dispatch umgestellt (Freigabe entscheidet vor `visibility`), mit einem
vierten Testitem (`private`+`share_read`) bewiesen statt nur behauptet — Details, Fundstelle
und Begründung stehen bereits vollständig in der Modul-Tabelle, hier nicht verdoppelt.

**Der eine Advisor-Aufruf dieser Runde** bestätigte den bereits gebauten Code (Merge/Chip-Logik/
Screenshot-Disziplin) und markierte zwei Punkte: der oben beschriebene Dispatch-Fund (unabhängig
selbst gefunden, siehe oben) und einen zweiten, nicht-blockierenden Hinweis (Chip erscheint auch
für fremde, geteilte Spaces — geprüft, kein Rule-4-Problem, Metadaten nicht Fließtext, Notiz
in der Modul-Tabelle).

**Verifiziert:** `pytest -q` 724 passed (env-gestrippt), unverändert. Tabu-Diff sauber (reiner
`phase5_ui/webui/static/`-Diff: `app.css`, `js/list.js`). Zwei-venv-Playwright-Lauf gegen ein
Wegwerf-`DATA_ROOT` mit vier Items (privat/nur-ich/geteilt/Randfall privat+geteilt): alle vier
Chip-Texte per Playwright-Assertion auf den gerenderten DOM-Text erzwungen, nicht nur der
Screenshot — inklusive des Randfalls, der den Dispatch-Fund beweist. Kein Konsolenfehler.

**Nächster Schritt (konkret):** Checkpoint nach Nikinger-Weisung — Commit 2 ist fertig
dokumentiert und wird jetzt committet, dann stoppt diese Session wieder für eine Rückmeldung.
Commit 3 (Ordner-Anlegen+Verschieben über das Menü, K4-Fix — erste Backend-Berührung dieses
Steps: `store.py :: ensure_folder()`, `POST /api/v1/spaces/{space}/folders`, `_items_post`-
Whitelist um `folder`) ist der nächste Kandidat, falls der Nikinger weiterbauen lässt.

**Nachtrag, Commit 3/7 — Ordner anlegen + Verschieben per Menü, K4-Fix, auf Nikinger-Weisung
gebaut** ("go on with next step, atomar, stop before doing additional steps"; die vorige
Formulierung „ein Advisor-Aufruf pro Arbeitszyklus" wurde vom Nikinger korrigiert auf **einen
Advisor-Aufruf pro Commit**). Umfang, Code, Verifikation: Modul-Tabelle oben, Zeile 12.

**Korrektur, eigener Fund vor dem Advisor-Aufruf:** der Tabu-Diff-Check dieser Session prüfte
seit Commit 0 versehentlich die **P5-B**-Liste (`storage/`, `mcpserver/{tools,permissions,
server}.py`) statt der für P6 tatsächlich geltenden P6-C-Liste (`mcpserver/asgi.py`,
`authserver/{crypto,totp,passwords,resolver,flows}.py` — P6-C hebt P5-B für `storage/`/
`tools.py`/`permissions.py` ausdrücklich auf). Die Behauptungen „Tabu-Diff sauber" in den
Session-Blöcken zu Commit 0–2 bleiben **wahr**, waren aber gegen die falsche Regel geprüft —
zufällig folgenlos, weil keiner der drei Commits `storage/` anfasste. Ab diesem Commit (der
`storage/store.py` bewusst berührt, P6-C erlaubt das) läuft der Check gegen die korrekte Liste.

**Zwei Advisor-Funde, beide geprüft statt blind übernommen oder ignoriert:**
1. **Eigener Fund vor dem Advisor-Aufruf, vom Advisor nur bestätigt:** `dialogs.js` durfte
   `handleWriteError()`/`showConflictDialog()` aus `editor.js` NICHT für den Verschieben-Fehlerpfad
   wiederverwenden — beide sind an `state.editingSnapshot` gekoppelt (das im Editor offene Item).
   Ein Verschieben aus der Liste betrifft aber meist ein ANDERES Item, teils gar keines im Editor
   offen — `showConflictDialog()` hätte dort auf einem falschen oder `null`-Snapshot gesessen.
   Eigener, schlichter Fehlerpfad für Verschieben-Konflikte gebaut (Toast statt Konfliktdialog),
   keine Abkürzung.
2. **Space-Namen-Traversal, geprüft, kein Fund in diesem Commit:** `ensure_folder()` baut
   `data_root / space / folder` ohne eigene `space`-Validierung — dieselbe Vertrauensgrenze wie
   `files.item_path()` (Phase 1, seit dem allerersten Commit unverändert: JEDER `store.create()`/
   `update()`/`search()`-Aufruf vertraut `space` bereits so). Kein neues Risiko durch diesen
   Commit. **Echter, unabhängiger Fund dabei, außerhalb des Commit-3-Scopes:**
   `spacectl.py :: _cmd_create_space()` validiert Space-Namen (`"/" in name`, führender `.`,
   `RESERVED_DIR_NAMES` → Abbruch), aber `phase4_auth/scripts/authctl.py :: _cmd_invite()` —
   der tatsächliche Weg, wie ein neuer Mensch (z. B. Fabian) seinen Space bekommt — reicht
   `args.space` ungeprüft an `store.create_invite()` durch, keine Validierung. Ein Space-Name wie
   `".."` würde `spacectl.py` ablehnen, aber `authctl.py invite --space ".."` liefe durch und
   böte danach jedem `ensure_folder()`/`store.create()`-Aufruf dieser Sitzung einen Pfad aus dem
   `DATA_ROOT` heraus. **Kein Remote-Angriffsfläche** (Space-Namen sind Operator-Eingabe, nie
   von einem Nutzer selbst wählbar) und **kein Commit-3-Blocker** (Fix läge in
   `phase4_auth/scripts/authctl.py`, außerhalb dieses Steps/dieser Phase — `authctl.py` selbst
   steht nicht auf der P6-C-Tabu-Liste, aber ein Fix dort wäre trotzdem eine Scope-Erweiterung
   ohne Auftrag). Für den Nikinger vorgemerkt, nicht in `phase4_auth/CLAUDE.md`s S/O-Tabelle
   eingetragen (das wäre ein eigener, bewusster Schritt, kein Nebenprodukt dieses Commits).

**Zwei Interpretationsentscheidungen, benannt statt stillschweigend gewählt:**
- **"Neuer-Ordner-Knopf bei Tiefe 2 deaktiviert"** wurde als Eltern-Dropdown-Ausschluss gebaut,
  nicht als deaktivierter Knopf pro Baumzeile: EIN „+ Ordner"-Eintrag fürs eigene Space, dessen
  Dialog nur Tiefe-1-Ordner als Elternoption anbietet (ein Tiefe-2-Ordner erzeugte als Elternteil
  eine unzulässige Tiefe 3 und taucht deshalb gar nicht erst auf). Vermeidet, jede Baumzeile um
  einen zweiten, verschachtelten Button erweitern zu müssen — dieselbe Nested-Button-Falle wie bei
  den Listenzeilen. Per Browserlauf verifiziert: nach dem Anlegen von `projekte/backend` zeigt das
  Dropdown weiterhin nur `["(oberste Ebene)", "projekte"]`.
- **Verschieben lebt in `list.js`, nicht `editor.js`** (Plan-Dateiliste nennt `editor.js` nicht):
  ein „→"-Knopf pro Zeile, Ziel per Dropdown aus den Ordnern des Items-eigenen Space — Verschieben
  bleibt in diesem Step ausdrücklich space-intern (Cross-Space-Move ist Step 7b).

**Verifiziert:** `pytest -q` **733 passed** (env-gestrippt, +9 gegenüber 724 — vier
`ensure_folder()`-Tests + fünf API-Tests, deckungsgleich mit der Plan-Testliste). Tabu-Diff
sauber gegen die korrekte P6-C-Liste (s. o.). Charakterisierungstests erneut byte-identisch grün
(P6-D, `store.py` berührt). Zwei-venv-Playwright-Lauf gegen ein Wegwerf-`DATA_ROOT`: Ordner
„projekte" über das Menü angelegt, Unterordner „projekte/backend" über dieselbe Aktion mit
Elternauswahl, Tiefe-2-Ausschluss im Dropdown bestätigt, ein Item über den Verschieben-Knopf nach
„projekte" verschoben — die reale Datei lag danach unter `sichtprobe5/projekte/itm_...md` auf der
Platte (`server_setup3.py`s eigener `rglob`-Ausdruck nach dem Lauf gegengeprüft, nicht nur die
UI geglaubt). Ein Testskript-Fund unterwegs, kein App-Fund: die erste Fassung nahm an, ein
verschobenes Item verschwinde aus dem „Notizen"-Eimer — falsch, Eimer sind rein typ-/
statusbasiert (`api.py :: _BUCKETS`), nicht ordnerbewusst, ein Item bleibt dort sichtbar,
ordnerlos oder nicht. Korrigiert, keine App-Änderung nötig. Kein Konsolenfehler während des
gesamten Laufs.

**Nächster Schritt (konkret):** Checkpoint nach Nikinger-Weisung — Commit 3 ist fertig
dokumentiert und wird jetzt committet, dann stoppt diese Session wieder für eine Rückmeldung.
Commit 4 (Drag & Drop, additiv auf Commit 3, kein neuer Backend-Pfad) ist der nächste Kandidat,
falls der Nikinger weiterbauen lässt — Plan nennt ihn ausdrücklich „nur falls Kontextbudget
reicht", nach drei Commits mit Frontend+jetzt-auch-Backend-Umfang ist das eine Sache, die der
Nikinger einschätzen sollte, nicht diese Session allein.

**Nachtrag, Commit 4/7 — Drag & Drop, auf Nikinger-Weisung gebaut** (AskUserQuestion zu
Sessionbeginn: „Commit 4 bauen" gegen „direkt zu Commit 5 springen"/„hier pausieren" gewählt —
neue Session nach `/clear`, kein Kontextbruch mitten in Commit 3, deshalb Nachtrag statt neuer
Rotation, dieselbe Konvention wie Commits 1–3). Umfang, Code, Verifikation: Modul-Tabelle oben,
Zeile 13.

**Refactor als Nebeneffekt, nicht Beifang:** `dialogs.js`s Menü-Verschieben-Handler (Commit 3)
rief den `PATCH`-Aufruf bisher inline auf; Drag & Drop braucht denselben Aufruf aus `tree.js`
heraus. Statt ihn zu duplizieren, wurde er nach `list.js :: moveItemToFolder(item, folder)`
gezogen (reiner `PATCH`+Neuladen, ohne Rückmeldung) — Erfolgs-/Fehler-Toast blieb bewusst bei
den beiden Aufrufern, nicht mitextrahiert: der Menü-Pfad muss bei einem Fehler den Dialog offen
halten, der Drag-Pfad hat keinen Dialog, der offenbleiben könnte. Zu wenig gemeinsam für eine
gemeinsame Fehlerbehandlung (Root-`CLAUDE.md`: „drei ähnliche Zeilen sind besser als eine
verfrühte Abstraktion").

**Geprüft statt nur behauptet, dass der Refactor nichts kaputt gemacht hat:** dieselbe
Zwei-venv-Playwright-Disziplin wie die vorigen Commits, diesmal mit zwei eigens dafür angelegten
Fixture-Items (`server_setup4.py`/`screenshot_client4.py`, Scratchpad). Erster Teil des Laufs
wiederholt exakt Commit 3s Menü-Pfad (Ordner „projekte" diesmal per `ensure_folder()` direkt
gesetzt statt über die UI angelegt, kein Doppeltest von Commit 3s eigenem Anlegen-Pfad nötig) —
Toast „Verschoben nach projekte" erscheint, Item taucht im Ordner auf. Kein Rückschritt durch
den Refactor.

**Drag & Drop selbst, entgegen der Plan-Erwartung tatsächlich per Playwright messbar:** der Plan
(`serialized-seeking-aurora.md`, Commit-4-Abschnitt) warnt ausdrücklich, `drag_to()` sei für
native HTML5-Drag-Events unzuverlässig, und nennt einen manuellen Livecheck durch den Nikinger
als die eigentliche Abnahme für dieses Stück. Der Lauf dieser Session gelang trotzdem:
`drag_row.drag_to(drop_target)` löste `dragstart`/`dragover`/`drop` sauber aus, das Item landete
nach dem Ziehen real im Ordner — read-only gegen die Platte geprüft
(`sichtprobe6/projekte/itm_...__drag-verschieben.md` existiert, `server_setup4.py`s eigener
`rglob`-Ausdruck nach dem Lauf), nicht nur der Toast/Screenshot geglaubt. **Das ersetzt den
Nikinger-Livecheck trotzdem nicht — konkret zu prüfen, nicht nur pauschal:** die `<li>` ist der
Ziehgriff, aber ihre gesamte Fläche liegt unter zwei `<button>`s (`.list__row`, `.list__row-move`)
— ob ein Mousedown-Drag auf einem `<button>` an sein `draggable`-Elternelement durchgereicht
wird, ist enginespezifisch. Chromium tut es (genau das beweist der `drag_to()`-Lauf, dessen
Mittelpunkt auf `.list__row` liegt), andere Engines sind darin unzuverlässiger. Bleibt
`dragstart` dort aus, gibt es keinen sichtbaren Hinweis, warum — der „→"-Menü-Knopf funktioniert
unbeeinflusst weiter. **Konkreter Check für den Nikinger:** eine Zeile im tatsächlich benutzten
Browser ziehen und prüfen, ob überhaupt ein `dragstart` feuert (sichtbar am gedimmten
`.list__row-draggable--active`-Zustand der Zeile), nicht nur ob der Drop funktioniert.
Zweiter, kleiner Advisor-Fund vor diesem Commit, behoben statt nur benannt: Ablegen auf dem
eigenen Ausgangsordner löste einen leeren `PATCH` mit Versionssprung + Git-Commit für keine
tatsächliche Änderung aus (dieselbe Kategorie wie Fund V10, `toasts.js`s Kopfkommentar) — ein
`if ((item.folder || "") === folderPath) return;` am Anfang von `tree.js`s `drop`-Handler
verhindert das jetzt. Derselbe Leerlauf existiert im Menü-Pfad seit Commit 3 unverändert fort
(dort schwerer aus Versehen auszulösen, deshalb hier behoben und dort nur benannt, kein
Commit-3-Fix in diesem Commit-4-Schnitt).

**Verifiziert:** `pytest -q` 733 passed (env-gestrippt), unverändert — kein neuer serverseitiger
Test nötig (P5-T, kein neuer Backend-Pfad, Commit 4 rührt keine Datei außerhalb
`phase5_ui/webui/static/` an). Tabu-Diff sauber gegen die korrekte P6-C-Liste (`mcpserver/
asgi.py`, `authserver/{crypto,totp,passwords,resolver,flows}.py`) — nur `app.css`/`js/
{dialogs,list,tree}.js` geändert. Kein Konsolenfehler während des gesamten Laufs (Playwright
`pageerror`/`console`-Listener).

**Nächster Schritt (konkret):** Checkpoint nach Nikinger-Weisung — Commit 4 ist fertig
dokumentiert und wird jetzt committet, dann stoppt diese Session wieder für eine Rückmeldung.
Commit 5 (`webui/shares.py` + Re-Auth-Gate, Freigabe-Dialog) ist der nächste Kandidat, deutlich
größerer Umfang als die vorigen vier Commits (neue Datei, elfter Fehlercode `reauth_required`,
Re-Auth-Mini-Formular) — eine Sache, die der Nikinger einschätzen sollte, nicht diese Session
allein.

**Nachtrag, Commit 5a/7 — Re-Auth-Gate, nur die Backend-Hälfte, auf Nikinger-Weisung gebaut**
("Let's go on with the next commit", ein Advisor-Aufruf freigegeben). Umfang, Code, Verifikation:
Modul-Tabelle oben, Zeile 14.

**Advisor-Aufruf vor dem Schreiben, ein Split und ein Sicherheitsfund:**
1. **Split (angenommen, nicht selbst entschieden):** Commit 5 lief im Plan als eine Einheit
   (Gate + Freigabe-Dialog + Re-Auth-Mini-Formular). Der Advisor riet, die Backend-Hälfte
   (`shares.py`/`errors.py`/`api.py`/`acl.py`/`app.py`-Verdrahtung — vollständig `pytest`-
   verifizierbar, deckt sich mit dem Plan-eigenen Verifikations-Split) von der Frontend-Hälfte
   (Freigabe-Dialog, Re-Auth-Formular in `dialogs.js`/`app.html` — nur per Screenshot prüfbar,
   UND eine im Plan noch offene UI-Designfrage: wie ein Mensch ein Freigabeziel benennt) zu
   trennen — dieselbe Logik, die Commits 0–4 bereits atomar hielt. Umgesetzt: **dies ist Commit
   5a**, der Freigabe-Dialog (5b) ist ein eigener, noch ungebauter Schritt.
2. **Echter Fund, vor jeder Codezeile geprüft statt angenommen:** die Ausführungsplan-Skizze
   sieht vor, dass ein Client bei `reauth_required` denselben `PATCH`-Body erneut sendet, jetzt
   mit `password`/`totp` gemischt hinein. `store.update()`s `else: updated_extra[key] = value`
   (Zeile ~507, keine Feld-Whitelist) hätte beide Felder unverändert in `extra` — also in die
   Frontmatter-Datei UND in einen Git-Commit — geschrieben, wäre `_items_patch`s `changes`-Dict
   nicht korrigiert worden. **Hard Rule 1, kein Schönheitsfehler.** Behoben: `changes` filtert
   jetzt zusätzlich `password`/`totp` heraus, unabhängig davon, ob das Gate überhaupt auslöste.
   Test `test_widening_share_write_with_correct_credentials_succeeds` beweist die Abwesenheit
   sowohl in der API-Antwort als auch am tatsächlich auf der Platte liegenden Item.

**Plumbing-Frage aufgelöst, nicht neu entworfen:** die Plan-Skizze §1.2.5 nennt
`require_share_reauth(request, session, *, before, after, acl)` — das deckt nicht ab, WIE gegen
ein echtes Credential geprüft wird. `request` fiel als ungenutzt ganz weg; `body`/`userdir`/
`throttle`/`auth_store` kamen dazu, dieselben Bausteine wie `account.py :: _require_reauth()`.
`api_routes()` bekommt dafür einen sechsten Parameter `users: UserDirectory` (`oauth.users` an
der `mcpserver/app.py`-Aufrufstelle, bereits vorhanden für `account_routes()`), `LoginThrottle`
wird lokal aus `auth_store` gebaut, exakt wie `account_routes()` es selbst tut.

**AclDecision-Erweiterung statt zweitem Dateizugriff:** `before`-`ShareState` braucht Space,
Ordner, `visibility`, `share_read`, `share_write` — `store.acl_of()` (index-only, liest die
Item-Datei nicht) lieferte bisher nur die schon gemischte `read`/`write`-Menge. `AclDecision`
bekam zwei neue Felder (`share_read`/`share_write`, roh, mit `default_factory=frozenset`, damit
alle zwölf bestehenden `AclDecision(...)`-Testkonstruktionsstellen unverändert kompilieren) —
`decision_for()` hatte beide Werte ohnehin schon als lokale Variablen, reiner Rückgabewert-
Zusatz, kein neuer Lesezugriff. **`folder` wird vor der Verwendung normalisiert:** ein roher
`folder`-String mit `..`-Segmenten hätte `AclReader.grants_for_dir()` sonst einen Pfad außerhalb
des Space bauen lassen, bevor `store.update()` ihn je validiert — `files.validate_folder()`
läuft deshalb hier ein zweites Mal (reine Funktion, kein Doppelschreiben), bevor der Wert in
`ShareState` landet.

**Ein zweiter, unabhängig gefundener Testfund (kein App-Fehler):** `test_acl_of_is_called_
before_permission_check` benutzt einen unkonfigurierten `MagicMock(spec=Store)` — dessen
`.acl_reader.decision_for(...)` liefert ohne Konfiguration einen frischen `MagicMock`, und ein
bloßer `MagicMock() > MagicMock()` scheitert nachweislich mit `TypeError` (per Interpreter
nachgeprüft, nicht angenommen). Behoben: `mock_store.acl_reader.decision_for.return_value =
own_acl` gesetzt — der Body dieses Tests ändert keins der vier widen-relevanten Felder, `before`
und `after` sind also ohnehin identisch.

**Verifiziert:** `pytest -q` **746 passed** (env-gestrippt, +13 gegenüber 733 — 8
`test_shares.py` [`widens()`-Wahrheitstabelle, acht Fälle aus der Plan-Testliste] + 5
`test_api.py`). Tabu-Diff sauber gegen die korrekte P6-C-Liste. Beide von diesem Commit
berührten Betriebsskripte real gelaufen (kein `pytest`-Äquivalent, `ui_budget.py`/`ui_smoke.py`
haben nie eigene Unit-Tests gehabt): `ui_smoke.py --json` 12/12 grün, `ui_budget.py --json`
`all_within_budget:true`, beide Läufe schließen `_measure_latency()`s zweiten, separaten
`api_routes()`-Aufruf mit ein. **Ein echter Interaktionstest zwischen zwei Commits, per
Zwei-venv-Playwright-Lauf statt nur gelesen:** Commit 3s bestehender Verschieben-Dialog gegen
einen Ordner mit `.share.yml` (also einen echten Widen-Fall) — Server antwortet 403
`reauth_required`, `dialogs.js`s bestehender Fallback-Zweig (kein `conflict`, kein
`unauthenticated`) zeigt die echte Servermeldung als Toast, der Dialog bleibt offen, die reale
Datei blieb nachweislich außerhalb `geteilt/` liegen (`rglob`-Gegenprobe). Kein JS-Absturz, kein
`pageerror` — der einzige Playwright-„Konsolenfehler" war Chromiums eigenes Netzwerk-Log für die
403-Antwort selbst, keine unbehandelte Exception, am fehlenden `pageerror`-Ereignis unterschieden
statt geglaubt.

**Nächster Schritt (konkret):** Checkpoint nach Nikinger-Weisung — Commit 5a ist fertig
dokumentiert und wird jetzt committet, dann stoppt diese Session wieder für eine Rückmeldung.
Commit 5b (Freigabe-Dialog + Re-Auth-Mini-Formular in `dialogs.js`/`app.html`, `#reauth-dialog`-
Markup, `pw-field`/`pw-toggle`-Muster wiederverwendet) ist der nächste Kandidat — braucht vorher
eine UI-Designentscheidung, die dieser Commit bewusst nicht selbst getroffen hat: wie ein Mensch
ein Freigabeziel (eine andere Space) benennt (freies Textfeld vs. eine Auswahl aus bekannten
Spaces). Danach bleiben laut Plan nur noch Commit 6 (`space_admin_enabled`-Stub, klein) übrig.
