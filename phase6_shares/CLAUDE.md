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
  - ./SESSIONS_ARCHIVE.md                          # Steps 0-7 + v2.1-Deploy verbatim (neun Eintraege), L3, kein Softcap
updated: 2026-08-18 -- (Nachtrag zum elften Block: Abschluss-Review fand einen ungebauten Sec4.5-Pflichttest, nachgebaut, 765 pytest gruen; danach sophistizierter E2E-Lauf gegen eine Wegwerf-Instanz (Port 8799, eigenes venv) -- 11/12 Playwright-Pruefungen gruen, Zeilen 26/27/30-Mechanik bestaetigt, zwei echte UI-Reichweiten-Funde dokumentiert (movable nur eigener Space, Zeile-28-Szenario nur ueber Connector erreichbar); Kopfzeile 48KB, ueber dem 40KB-Softcap, Rotation ist ein No-op (nur ein Block) -- Nikinger-Entscheidung noetig, siehe Session-Ende)
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
| 8 | Lesbarkeit der Textfarben (`ITEM_MOVE_PLAN.md` §3 — **[2026-08-17 Korrektur]** dort ohne Entscheidungscode; „P6-AD/AE" war ein Kopierfehler aus §2, das sind tatsächlich Step-7b-Entscheidungen [`Store.move()`/Rechteregel], nicht Step 7as Textfarben): `phase5_ui/webui/static/app.css` — `--text-muted`/`--text-faint` kalibriert angehoben, neues `--text-placeholder`, `.input::placeholder` darauf umgehängt. **Nachtrag, Nikinger-Feedback vor dem Deploy:** Wortmarke „sharefyx" + Versionsbadge (jetzt `v2.1`, `app.html`) sowie alle Versionsnummern aus den Dateien (`recent-row__meta`, `.editor__version`, `.version-band__number`, `ro-meta`) jetzt `var(--text)` statt `--text-faint`/`--text-muted` — neue Klasse `.version-num` trennt die Versionsnummer farblich vom gedämpften Begleittext im selben Element (`app.css`/`app.js`) | 7a | ✅ **gebaut, Deploy beim Nikinger** — Kontrastwerte bereits in `ITEM_MOVE_PLAN.md` §3.1 protokolliert (durchgerechnet vor dieser Session); Sichtprobe zweimal per In-Process-Server + Screenshot gegen die echte `app.css`/`app.js` (Login-Seite, Liste mit Chips, Editor mit Meta-Panel — alle drei beide Male gesehen, nicht behauptet). Deploy braucht Sudo für den Neustart, außerhalb dessen, was Claude Code selbst kann (Präzedenz: Steps-4–6-Cutover, `SESSIONS_ARCHIVE.md`) | 0 (P5-T: JS/CSS bleiben unit-ungetestet; `pytest` unverändert als Regressionsprobe — 724 gesamt vor UND nach beiden Teilen dieser Session, keiner davon neu) |
| 9 | UI Dateisystem (Block B), Commit 0/7 — `app.js` (1525 Zeilen, ein `initShell()`-Closure) entlang der bestehenden Kommentar-Nahtstellen in zehn ES-Module unter `phase5_ui/webui/static/js/` aufgeteilt (`app`/`api`/`state`/`tree`/`list`/`editor`/`markdown`/`dialogs`/`toasts`/`updates`), `state.js` als einzelnes mutierbares Objekt (von allen Importern geteilt, Ersatz für den Closure-`state`), jedes Modul ein `init(deps)`, das der neue schlanke `app.js` beim Bootstrap der Reihe nach aufruft. Bisheriges Zwei-Skript-Modell (`js/updates.js` als globales Skript vor `app.js`, `window.SharefyxUpdates`) entfällt — `updates.js` ist jetzt selbst ein Modul, `app.html`/`pages.py` laden nur noch `<script type="module" src=".../js/app.js">`. `ui_budget.py` zählt die Nutzlast jetzt über `js/*.js`-Glob statt fester Namen | 7 | ✅ **gebaut, noch nicht deployt** — CSP (`script-src 'self'`) erlaubt Same-Origin-`type="module"` ohne Header-Änderung (V50 geschlossen); Sichtprobe golden path (Login → Liste → bestehendes Item öffnen+bearbeiten+speichern v1→v2 → neu anlegen) per Zwei-venv-Playwright-Skript, fünf Screenshots gesehen, nicht nur behauptet | 0 (P5-T: JS bleibt unit-ungetestet; fünf bestehende Tests in `test_static_routes.py` auf die neue Modulstruktur umgeschrieben, keiner neu; 724 gesamt unverändert) |
| 10 | UI Dateisystem (Block B), Commit 1/7 — echter Ordnerbaum, kein Backend-Fund nötig (`GET /api/v1/items?folder=` existierte bereits, `GET /api/v1/spaces` trug `folders`/`members` schon, nur `app.js` rief die Route nie ab). `list.js :: loadOverview()` holt jetzt `/overview`+`/spaces` per `Promise.all`, mischt `folders`/`members` nach Name in die Space-Objekte. `tree.js`: `buildFolderTree()` (flache Pfadliste → ≤2-stufiger Baum, reines Splitten auf „/", da `MAX_FOLDER_DEPTH` serverseitig gilt), `renderRealFolders()` reused `.tree__folder` (neue Modifier-Klasse `.tree__realfolder--child` nur für die Einrückung der zweiten Ebene), `navigate()`/`navigateFolder()` jetzt exklusiv (`state.folder`/`state.filter` nie beide gesetzt). `list.js`: `filterParams()`/`renderCrumb()`/Leerzustand-Text folder-bewusst gemacht | 7 | ✅ **gebaut, noch nicht deployt** — Sichtprobe mit zwei echten, verschachtelten Ordnern (`Projekte`/`Projekte/Backend`, serverseitig zu `projekte`/`projekte/backend` slugifiziert, P6-Q — Baumdarstellung ist davon unabhängig, reine String-Weiterreichung): Verschachtelung im Baum sichtbar, Klick navigiert **und** filtert exakt (nicht Präfix, V55) auf beiden Ebenen, per Playwright-Assertions auf die tatsächlich gerenderten Zeilentitel erzwungen, nicht nur der Screenshot. Advisor-Fund vor dem Commit, geprüft statt blind gefixt: `navigateFolder()` setzt `state.filter=null`, `dialogs.js :: openCreateDialog()` liest `state.meta.buckets[state.filter]` ungeschützt — JS stringifiziert einen `null`-Schlüssel zu `"null"`, kein `TypeError`, derselbe Fallback-Pfad wie beim typlosen Bucket „Archiv" heute schon; per Node-Check UND echtem Browserlauf (Konsolenfehler-Listener, „+" während `projekte/backend` aktiv) bestätigt, **kein Fix nötig**. Offen für Commit 3 (folder-bewusstes Anlegen): der aktuelle Fallback „leerer Ordner → Typ Notiz" ist ein stiller Default, keine bewusste Entscheidung für echte Ordner | 0 (P5-T: JS bleibt unit-ungetestet, kein jsdom-Zusatzlauf — die echte Browserprobe deckt strenger ab; 724 gesamt unverändert) |
| 11 | UI Dateisystem (Block B), Commit 2/7 — Sichtbarkeits-Chip, kein Backend-Fund nötig (`visibility`/`share_read`/`share_write` stehen bereits auf `summary_to_json()`, P6 Step 5). `list.js`: neue `visibilityLabel()`/`visibilityChip()`, in `renderList()`s Zeilen verdrahtet (`.list__row-meta` von reinem Text auf Flex mit Meta-Text + Chip umgebaut). `app.css`: `.visibility-chip`/`.visibility-chip--shared` (gedämpft vs. `--ok`-grün), reused `.list__row-meta`s bestehende Fläche | 7 | ✅ **gebaut, noch nicht deployt** — Sichtprobe mit vier Items (privat/nur-ich/geteilt/Randfall), alle drei geplanten Chip-Zustände + der Randfall per Playwright-Assertion auf gerenderten Chip-Text erzwungen (nicht nur Screenshot), Konsolenfehler-Listener sauber. **Benannte Abweichung vom Plan-Wortlaut, gefunden beim Nachlesen von `acl.py`/`permissions.py` vor dem Commit:** der Plan prüft `visibility` zuerst („private" → unbedingt „privat"), aber `acl.py :: decision_for()` verundet `share_read`/`share_write` immer in `AclDecision.read`/`write`, unabhängig von `visibility` — nur `Surface.AGENT` fragt `visibility` (P6-P), nie ein Mensch. Ein Item mit `visibility=private` UND einer echten Freigabe ist für den Freigegebenen faktisch lesbar, erreichbar schon heute über ein rohes `PATCH /api/v1/items/{id}` (`_items_patch` hat keine Feld-Whitelist) — nicht erst über Commit 5s künftigen Dialog. Dispatch umgestellt: `share_read`/`share_write` non-empty entscheidet zuerst, `visibility` nur als Fallback ohne Freigaben — ein vierter Testfall (`visibility=private`+`share_read=[fabian]`) beweist den Unterschied, zeigt korrekt „geteilt mit fabian" statt „privat". **Zweiter, nicht blockierender Punkt:** der Chip erscheint identisch für Items aus fremden, geteilten Spaces (`renderList()` ist derselbe Codepfad für jeden Space) — das sind ACL-Metadaten, keine Fließtext-Bodies, Hard Rule 4s `<untrusted_content>`-Wrapping betrifft das nicht (derselbe Schnitt wie `overview_row_to_json()`s `snippet`-Auslassung, nur umgekehrt: hier ist die Metadaten-Anzeige bewusst, nicht der Fließtext) | 0 (P5-T: JS bleibt unit-ungetestet, kein jsdom-Zusatzlauf — die echte Browserprobe deckt strenger ab; 724 gesamt unverändert) |
| 12 | UI Dateisystem (Block B), Commit 3/7 — Ordner anlegen + Verschieben per Menü, K4-Fix, erster echter Backend-Touch dieses Steps (P6-C erlaubt `storage/` explizit). `store.py :: ensure_folder(space, folder)` (neu, `mkdir(parents=True, exist_ok=True)` unter `self._lock`, kein Git-Commit, keine Content-Datei — reine Verzeichnisoperation). `api.py`: neue `POST /api/v1/spaces/{space}/folders` (Eigentümer-Riegel wie `_items_patch`s `folder`-Feld), `_items_post`-Whitelist um `"folder"` erweitert (K4). `tree.js`: „+ Ordner"-Zeile fürs eigene Space, öffnet `dialogs.js :: openNewFolderDialog()`. `list.js`: Verschieben-Knopf („→") pro Zeile — als GESCHWISTER von `.list__row`, nicht darin verschachtelt (zwei `<button>` ineinander ist ungültiges HTML), `<li>` deshalb neu Flex (`app.css`). `dialogs.js`: zwei neue Dialoge, `openNewFolderDialog()`/`openMoveDialog(item)`. `app.js`: kleine, dokumentierte Abweichung vom Plan-Dateiwortlaut — die beiden neuen Dialoge in `anyOverlayOpen()`/die Escape-Behandlung aufgenommen, dieselbe Konsistenz wie jeder andere Dialog hier | 7 | ✅ **gebaut, noch nicht deployt** — Details, beide Interpretationsentscheidungen und die zwei Advisor-Funde: Session-Block unten | +9 (4 `phase1_storage/tests/test_store.py`: `ensure_folder()` erstellt/idempotent/lehnt Tiefe>2 und leeren String ab + 5 `phase5_ui/tests/test_api.py`: `test_create_item_accepts_folder` [K4] + vier Endpunkt-Tests [erstellt sichtbaren leeren Ordner, lehnt fremden Space auch mit `write:`-Grant ab, lehnt Tiefe>2/reservierten Namen ab]); Charakterisierung erneut byte-identisch grün (P6-D); 733 gesamt |
| 13 | UI Dateisystem (Block B), Commit 4/7 — Drag & Drop, additiv auf Commit 3, kein neuer Backend-Pfad (P6-AB: Menü-Knopf bleibt Pflicht-Alternative). `list.js :: moveItemToFolder(item, folder)` (neu, aus `dialogs.js`s bisher dort inline stehendem `PATCH`-Aufruf extrahiert — geteilter Schreibpfad für Menü UND Drag & Drop, Erfolgs-/Fehler-Rückmeldung bleibt bewusst bei den beiden Aufrufern statt mitextrahiert, weil der Menü-Pfad einen Dialog offen halten muss und der Drag-Pfad keinen hat). `list.js`: `<li>` (nicht der Button) trägt `draggable`/`dragstart`/`dragend`, dieselbe `movable`-Bedingung wie der Menü-Knopf. `tree.js`: neue `bindFolderDropTarget()`, `dragover`/`dragleave`/`drop` nur auf `folderButton()`-Knoten im **eigenen** Space (`space.own`) — der Server lehnt fremde `folder`-Änderungen ohnehin ab, das Gating hier ist reine UX. `app.css`: Ziehgriff-Cursor + gedimmte Zeile während des Ziehens, gestrichelte Kontur am Drop-Ziel (bewusst optisch von `[aria-current]` unterschieden) | 7 | ✅ **gebaut, noch nicht deployt** — Details, inkl. des Refactor-Regressionsbeweises: Session-Block unten | 0 (P5-T: JS bleibt unit-ungetestet; 733 gesamt unverändert — Playwright-`drag_to()`-Lauf statt jsdom, siehe Session-Block, ist Entwicklungshilfe dieser Session, kein Teil der Suite) |
| 14 | UI Dateisystem (Block B), Commit 5a/7 — Re-Auth-Gate (Backend-Hälfte, P6-N), Freigabe-Dialog/Re-Auth-Mini-Formular auf Commit 5b verschoben (Session-Block begründet den Split). `storage/acl.py`: `AclDecision` bekommt rohe `share_read`/`share_write` (Defaults, bestehende Konstruktionsstellen unverändert). `webui/shares.py` (neu): `ShareState`, `widens()` (echte Obermenge auf `AclDecision.read`/`.write`, `visibility` fließt strukturell nie ein), `require_share_reauth()` (wirft `ApiError("reauth_required")`, Signatur um `body`/`userdir`/`throttle`/`auth_store` erweitert — die Plan-Skizze in §1.2.5 deckt die tatsächliche Credential-Prüfung nicht ab). `webui/errors.py`: elfter Code `reauth_required:403`. `webui/api.py :: _items_patch`: `before`/`after`-`ShareState` aus `acl`/Body gebaut, Gate läuft VOR `store.update()`; `password`/`totp` werden unabhängig vom Gate-Ausgang nie an `store.update()` weitergereicht (Advisor-Fund, sonst Frontmatter-Leck, Hard Rule 1); `api_routes()` bekommt sechsten Parameter `users: UserDirectory`. `mcpserver/app.py` zieht mit `oauth.users` nach | 7 | ✅ **gebaut, noch nicht deployt** — Details, Advisor-Fund und der Commit-5a/5b-Split: Session-Block unten | +13 (8 `phase6_shares/tests/test_shares.py` [neu, `widens()`-Wahrheitstabelle] + 5 `phase5_ui/tests/test_api.py` [Gate ausgelöst ohne/mit falschen Credentials, Gate erfüllt+Credential-Leck-Check, keine Auslösung bei Verkleinerung/reiner Inhaltsänderung]); Kollateralkorrekturen (kein neuer Test): `phase5_ui/tests/{conftest,test_overview}.py` + drei `test_api.py`-Fixtures um `confirmed_users` als sechstes `api_routes()`-Argument ergänzt, ein `mock_store.acl_reader.decision_for.return_value` gesetzt (unkonfigurierter `MagicMock` scheitert an `>` mit `TypeError`, nachgeprüft); `phase5_ui/scripts/{ui_budget,ui_smoke}.py` zogen ihre eigenen `api_routes()`-Aufrufe nach, beide real gegen ein Temp-`DATA_ROOT` gelaufen (12/12 bzw. `all_within_budget:true`); 746 gesamt |
| 15 | UI Dateisystem (Block B), Commit 5b/7 — Freigabe-Dialog + Re-Auth-Mini-Formular, kein Backend-Fund nötig (Gate seit Commit 5a live). `list.js`: neuer „⇄"-Freigeben-Knopf, GESCHWISTER von `.list__row`/`.list__row-move` (dieselbe Nested-Button-Regel), dieselbe `movable`-Bedingung. `dialogs.js`: `openShareDialog()`/`closeShareDialog()` (Picker aus `state.spaces`, drei-stufiges `<select>` pro fremdem Space: kein Zugriff/lesen/schreiben — `schreiben` impliziert `lesen` bereits über `decision_for()`s Vereinigung, keine doppelte Eintragung), `collectShareBody()`, Submit-Handler mit eingefrorenem `pendingShareBody` (Advisor-Vorgabe: erste Fassung beim ersten Absenden fixiert, nur `password`/`totp` werden bei jedem Retry frisch gelesen). `app.html`: `#share-dialog` (statische Hülle, `pw-field`/`pw-toggle` von `initPasswordToggles()` automatisch erfasst, kein neuer JS-Code dafür). `app.js`: `#share-dialog` in `anyOverlayOpen()`/Escape aufgenommen (dieselbe dokumentierte Abweichung wie Commit 3). `app.css`: `.list__row-share` teilt sich die Regel mit `.list__row-move`. **Bewusster Scope-Schnitt (Advisor bestätigt):** kein `visibility`-Feld im Dialog — der Chip zeigt sie bereits, niemand hat eine UI-Änderung dafür verlangt | 7 | ✅ **gebaut, noch nicht deployt** — Details, Advisor-Bestätigung und die Zwei-venv-Playwright-Verifikation: Session-Block unten | 0 (P5-T: JS/HTML/CSS bleiben unit-ungetestet; 746 gesamt unverändert, reiner Frontend-Commit — Tabu-Diff bestätigt nur `phase5_ui/webui/static/`) |
| 16 | UI Dateisystem (Block B), Commit 6/7 — `space_admin_enabled`-Stub, Seam ohne Implementierung (P5-Z-Kategorie), Step 7 damit vollständig. `config.py`: `UiSettings.space_admin_enabled: bool = False`, dieselbe Feld-statt-Env-Var-Konvention wie `hsts` — ohne Laufzeitwirkung, `app.html` ist statisch, kein Templating. `app.html`: neuer, hart `disabled` (nicht nur versteckter) Menüpunkt „Geteilte Spaces verwalten — kommt in Phase 7" im Konto-Dialog, Geschwister von „Update-Log ansehen" | 7 | ✅ **gebaut, noch nicht deployt, Step 7 vollständig** | +1 (`phase5_ui/tests/test_static_routes.py`, dokumentierte Abweichung vom Plan-Dateiwortlaut — der nennt `test_pages_markup.py`, das testet aber ausschließlich `webui/pages.py`s servergerenderte Seiten, nie `app.html`; `test_static_routes.py` liest `app.html` bereits direkt, dort ist der Test sachlich richtig); 747 gesamt |

## Geerbte Contracts

**[2026-08-09, P6 Step 0] Dritte, benannte Öffnung des P1-Contracts** (Plan §1.4): `models.py`
bekommt `folder`/`visibility`/`share_read`/`share_write`, `store.py` bekommt `acl_of()`/`patch()`/
erweiterte `create()`/`update()`/`search()`/`list_spaces()`. Wird in Step 4 umgesetzt, hier nur
angekündigt — nach Phasenabschluss (Step 10) wieder geschlossen, siehe `phase1_storage/CLAUDE.md`.

**[2026-08-17, Planungssession] Vierte, benannte Öffnung angekündigt:** `store.py` bekommt
`move(item_id, *, version, space=, folder=)` (`ITEM_MOVE_PLAN.md` §4.1, P6-AD). Additiv zur
dritten Öffnung, kein bestehendes Signatur wird geändert. Wird mit Step 7b umgesetzt, hier nur
angekündigt — schließt zusammen mit der dritten Öffnung nach Phasenabschluss.

## Vormerkungen (nicht Teil eines aktuellen Steps)

**[2026-08-14] UI-Feedback nach dem Live-Deploy von v2.1 (Nikinger, direkt nach der ersten
Nutzung) — ausdrücklich nur vormerken, nichts davon diese Session umgesetzt, kein Code
angefasst:**

1. **✅ Behoben (2026-08-16).** Dropdown-Lila war natives Browser-Rendering der `<option>`-Liste,
   kein `app.css`-Ton — `select.input { accent-color: var(--accent) }`, live per Playwright
   bestätigt. Volle Herleitung: `SESSIONS_ARCHIVE.md`, zehnter Block.
2. **✅ Gebaut (2026-08-17), Step 7b vollständig.** Space-zu-Space-Verschieben,
   `phase6_shares/ITEM_MOVE_PLAN.md` §4 (P6-AD–AJ). Drei Commits (Storage/Rechte/UI-Dialog) —
   Details `phase1_storage/`/`phase2_mcp/`/`phase5_ui/CLAUDE.md`s „[2026-08-17]"-Einträge.
   UI-Move per echtem Playwright-Lauf verifiziert. **Noch nicht deployt, keine
   Nikinger-Live-Probe** (Abnahmezeilen 25–30 bleiben offen bis dahin).
3. **✅ Subplan geschrieben (2026-08-17).** Mehrfachauswahl — jetzt **§9** in
   `phase6_shares/ITEM_MOVE_PLAN.md` (Entscheidungen **P6-AK–P6-AN**): gemeinsames Ziel für die
   ganze Auswahl, kein neuer Endpunkt/MCP-Tool (clientseitige Schleife über den Step-7b-Pfad),
   Re-Auth in max. zwei Runden. `moveItemToFolder()` (`list.js`→`_items_patch`) patcht weiterhin
   nur `folder`, `widens()` greift bei reinem Ordnerwechsel nie — In-Space-Mehrfachauswahl
   braucht deshalb keine neue Rechteprüfung (P6-AN). **Noch nicht gebaut, setzt Step 7b voraus.**
4. **✅ Behoben (2026-08-16).** `--ok` (Grün, Erfolgstoast + `.visibility-chip--shared`) auf
   `var(--accent)` (Blau) umgestellt, Token entfernt (ungenutzt danach). Orange „nur lesen"
   bewusst unangetastet — Nikinger noch unentschieden. Volle Herleitung: `SESSIONS_ARCHIVE.md`,
   zehnter Block.

**Punkte 1+4 umgesetzt (2026-08-16). Punkt 2 (Step 7b) vollständig gebaut (2026-08-17), noch
nicht deployt.** **Punkt 3 (§9 Mehrfachauswahl): Subplan gelockt, noch nicht angefangen.**

**[2026-08-14] MCP-Werkzeug-Ergonomie, Live-Feedback einer arbeitenden Claude-Instanz** — nach
einem sitzungsreichen Tag (Protokollierung eines OTOBO-Vorgangs, Item `itm_7cf94a2c`, 40+
`append_to_item`-Aufrufe für ein einziges, sequenziell wachsendes Log-Dokument). Vom Nikinger
verbatim weitergegeben, hier strukturiert, nichts davon in dieser Session geplant oder gebaut —
betrifft ausschließlich `mcpserver/tools.py` (P6-C erlaubt das, aber außerhalb des laufenden
Step-7-Scopes „UI Dateisystem").

**Technisch fehlend:**
- **Kein Bulk-Append.** Ein sequenziell wachsendes Log-Dokument lässt sich nicht komplett ohne
  Einzel-Calls schreiben, aber „mehrere Appends in einem Aufruf" wäre spürbar günstiger gewesen
  als 40+ Einzelaufrufe an einem Tag.
- **`list_spaces` schlecht auffindbar.** Die Instanz fand das Tool nicht in ihrer eigenen
  Tool-Exploration, bis sie gezielt danach suchte — und sagte dem Nikinger fälschlich „Claude
  kann nur im eigenen Space schreiben" (stimmt nur für einen Space mit `writable: false`, nicht
  generell). Eine falsche Aussage, die auf einer Lücke in der Tool-Auffindbarkeit beruhte, nicht
  auf einem Denkfehler.
- **`patch_item` vs. `update_item` nirgends zusammengefasst.** Die Aufgabenteilung (`patch_item`
  nur Body, `update_item` nur Frontmatter mit optionalem Body) musste über zwei Fehlversuche und
  einen Hinweis auf den Quellcode gelernt werden, statt aus den Tool-Beschreibungen ableitbar zu
  sein.

**Tokens/Zeit gekostet:**
- **`get_item` liefert immer den vollen Body**, auch wenn nur die aktuelle Versionsnummer für den
  nächsten Append gebraucht wird — gegen Ende der Session ein mehrere-tausend-Token-Dump für eine
  einzige Zahl. Ein `get_item_meta` (nur Frontmatter/Version, kein Body) wäre hier der Hebel.
- **Status-Enum-Werte nicht dokumentiert** — die Instanz riet „archiviert", bekam einen Fehler,
  riet dann richtig „archived". Ein Satz in der Tool-Beschreibung mit den erlaubten Werten hätte
  einen kompletten Roundtrip gespart.
- **Suchtreffer gelegentlich unzuverlässig** — mehrfach leere Ergebnisse bei plausiblen
  Suchbegriffen (Beispiel: eine Aufgabe erst beim dritten Versuch gefunden), kostete mehrere
  Suchrunden statt einer.

**Ein echter Bug, kein reiner Ergonomie-Wunsch:** die Fehlermeldung von `patch_item` bei einem
Frontmatter-Zugriffsversuch — `patch_failed: edits[0] fand 0 Treffer — lies das Item neu mit
get_item und prüfe den exakten Text` — ist irreführend. Sie suggeriert ein Textmatching-Problem
(„lies neu, prüf den Text"), obwohl die Ursache kategorisch ist: `patch_item` kann Frontmatter
grundsätzlich nicht erreichen, kein erneutes Lesen hätte geholfen. Eine Fehlermeldung, die in
diesem Fall „Frontmatter-Felder sind mit `patch_item` nicht erreichbar, nutze `update_item`"
sagt statt „0 Treffer, versuch's nochmal", hätte zwei Fehlversuche und zwei überflüssige
Nachrichten an den Nikinger erspart.

**Noch nicht geplant.** Kandidat für einen eigenen kleinen Werkzeug-Ergonomie-Schnitt, wenn eine
Planungssession dafür ansteht — dieselbe Kategorie wie das ursprüngliche `patch_item`-Feedback,
das P6 selbst mit ausgelöst hat (`docs/concepts/PHASE5_CLOSEOUT_HANDOVER.md` §4.6).

---

## Session stopped — 2026-08-17, elfter — (Planungssession „light": Step 7b gelockt, §9 Mehrfachauswahl neu — **[2026-08-17 Korrektur] Titel stimmte nur bis zum Nachtrag**: derselbe Block dokumentiert weiter unten den Bauauftrag, der Step 7b in drei Commits vollständig gebaut hat; Titel unverändert aus Historientreue, Klarstellung hier statt rückwirkendem Umschreiben)

**Auftrag:** Nikinger — die beiden noch offenen UI-Feedback-Punkte (2: Space-zu-Space-Move/Step
7b, 3: Mehrfachauswahl) bearbeiten. Nikinger-Rahmen für diese Session: „planning session light,
da es kein echter Plan ist" — erster Schritt ein Subplan für beide Punkte, plus bei Bedarf die
Tests, die für einen Abschluss von Phase 6 noch fehlen. Ausdrücklich bestätigt: „I confirm we
can work on all points."

**Vor dem Schreiben geklärt, nicht angenommen (Advisor-Konsultation vor jeder Substanzarbeit):**
`ITEM_MOVE_PLAN.md` §2 hatte P6-AD–AJ nie als gelockt dokumentiert — die Planungssession vom
2026-08-13 endete mit „ITEM_MOVE_PLAN.md vom Nikinger freigeben lassen" als offenem nächsten
Schritt, die einzige Folge-Session (2026-08-13, Step 7a) war ausdrücklich auf §3 verengt, und
root-`CLAUDE.md`s „Noch nicht entschieden" trug den Punkt bis zu dieser Session unverändert seit
2026-08-13 (`git log`/Archiv-Grep über alle Sessions dazwischen bestätigen: keine Freigabe
dokumentiert). Erst mit der Nikinger-Bestätigung dieser Session gilt §2 als gelockt — im
Plan-Dokument selbst datiert festgehalten, keine stille Annahme.

**Ergebnis: zwei Subplan-Erweiterungen in `phase6_shares/ITEM_MOVE_PLAN.md`, keine
Code-Änderung.**

1. **§2 (Step 7b) gelockt.** P6-AD–P6-AJ tragen jetzt einen datierten Freigabevermerk.
2. **V52–V55 gegen den inzwischen echten Step-7-Code geschlossen** (bei Plan-Erstellung
   2026-08-13 existierte Step 7 noch nicht, alle vier waren „wann: Step 7b/Step 7" offen):
   `reauth_required` ist exakt `ApiError("reauth_required", …)` (`webui/shares.py`), `ShareState`
   trägt bereits `space`/`folder` — Plan-Annahme in §4.3 hält unverändert. `os.replace()` bleibt
   über Space-Grenzen atomar: read-only gegen den echten `DATA_ROOT` geprüft (`stat -c %d`),
   `niklas`/`fabian`/`IT-Sekus-Projekt` liegen alle auf demselben ext4-Gerät (`2050`,
   `/dev/sda2`). **V54 anders gelöst als geplant, einfacher:** kein `folders`-Feld an
   `GET /api/v1/overview` nötig — `GET /api/v1/spaces` trägt `folders` bereits für jeden
   sichtbaren Space, `list.js :: loadOverview()` mischt das seit Step 7 Commit 1 in
   `state.spaces`, der bestehende `openMoveDialog()`-Code liest schon denselben Weg (§4.4 Punkt 1
   entsprechend präzisiert, kein Backend-Fund für den Verschieben-Dialog).
3. **Advisor-Fund vor dem Bauen, in §4.2/§4.3 nachgezogen:** der bestehende Eigentümer-Riegel
   gegen Nicht-Eigentümer-Ordnerwechsel (`tools.py:514-520`, analog `api.py`) prüft `folder is
   not None and acl.space != principal.space` — ohne Rücksicht auf `space`. Bei einem
   Cross-Space-Move MIT gleichzeitig gesetztem Zielordner (der reale Fall aus §4.4 Punkt 1) wäre
   diese Bedingung für praktisch jeden legitimen Move wahr (kein Principal heißt wie ein
   geteilter Space, P6-AE) — der alte Riegel hätte einen von P6-AE bereits erlaubten Move
   fälschlich blockiert. Plan-Text „ersetzt ihn" war codeseitig nicht verankert; jetzt eine
   explizite Bedingung (`space is None`) plus ein neuer Pflichttest in §4.5. **Noch nicht
   gebaut** — reine Plan-Präzisierung, kein Code in diesem Repo geändert außer den `.md`-Dateien.
4. **Neues §9 „Mehrfachauswahl" (P6-AK–AN), vollständig neu entworfen** (dafür lag vorher kein
   Plan vor, nur eine Nikinger-Vormerkung): ein gemeinsames Ziel für die ganze Auswahl (P6-AK),
   kein neuer Endpunkt/kein neues MCP-Tool — die Batch-Aktion ist eine clientseitige,
   sequenzielle Schleife über den bestehenden Step-7b-Einzelpfad, jeder Request durchläuft die
   volle, bereits gebaute Rechteprüfung unverändert (P6-AL). Re-Auth in maximal zwei Runden
   (erst alle Requests ohne Credentials, dann ein gemeinsames Formular nur für die
   zurückgewiesenen) statt der falschen Annahme „ein Ziel ⇒ ein `widens()`-Ergebnis für alle"
   (P6-AM — `widens()` hängt auch an der `visibility`/`share_*` des einzelnen Items, nicht nur
   am Ziel). In-Space-Mehrfachauswahl bleibt bestätigt ohne neue Rechteprüfung (P6-AN, bestätigt
   dieselbe grep-Prüfung, die schon die alte Vormerkung stützte). Vier neue Abnahmezeilen (31–34).
   **Keine neue Backend-Testdatei geplant** (§9.4) — reiner Frontend-Schnitt, Playwright-Sichtprobe
   beim Bauen wie bei jedem anderen JS-Schnitt dieser Phase.
5. **Tests, die für den Abschluss von Phase 6 noch fehlen (Nikinger-Frage dieser Session,
   beantwortet statt übergangen):** Block A+B sind vollständig gebaut, 747 Tests grün. Was fehlt,
   ist kein Testcode, sondern **live-Verifikation durch Menschen** — Gate B (Abnahmezeilen 8–18
   im Hauptplan) braucht weiterhin echten Alltag von Niklas **und** Fabian, nicht mehr
   Claude-Code-Sessions. Für Step 7b/§9 selbst: genau ein neuer Pflichttest (Punkt 3 oben) plus
   die bereits in `ITEM_MOVE_PLAN.md` §4.5 gelisteten 14 — beide noch ungeschrieben, weil noch
   nicht gebaut. **Block C (Bilder, Abnahmezeilen 19–22) ist separat und laut P6-A explizit die
   erste Stelle, die unter Druck wegfällt** — nicht Teil dieser beiden Feedback-Punkte, hier
   bewusst nicht mitgeplant; ob Block C für einen Phasenabschluss noch gebaut wird, bleibt
   Nikinger-Entscheidung.

**Nebenfund, im selben Commit korrigiert:** Modul-Status Zeile 8 zitierte „P6-AD/AE" für Step 7a
(Textfarben) — ein Kopierfehler, diese Codes gehören zu Step 7b (`Store.move()`/Rechteregel),
§3 (Textfarben) hat gar keine eigenen Entscheidungscodes. Datierte Korrekturnotiz statt
rückwirkendem Umschreiben.

**Contract-Ankündigung nachgezogen:** „Geerbte Contracts" bekommt eine vierte, benannte Öffnung
(`store.py :: move()`, additiv) — angekündigt, noch nicht umgesetzt, gleiche Konvention wie die
dritte Öffnung aus Step 0.

**Verifiziert:** keine Testsuite gelaufen (reine `.md`-Änderungen, kein Code). Tabu-Diff nicht
relevant. `git log`/`SESSIONS_ARCHIVE.md`-Grep für den Freigabe-Nachweis oben tatsächlich
ausgeführt, nicht behauptet (Befehle und Treffer: siehe Advisor-Konsultation dieser Session).
Dateigröße `ITEM_MOVE_PLAN.md` nach allen Ergänzungen: **~39,3 KB** — knapp unter dem 40-KB-
Softcap für 📗-Dokumente, keine Rotation/Auslagerung nötig, aber der nächste Zuwachs (z. B. eine
weitere Erweiterung) braucht eine Softcap-Prüfung vor dem Schreiben, nicht danach.

**Nächster Schritt:** Step 7b bauen (`ITEM_MOVE_PLAN.md` §4, jetzt gelockt) — danach erst §9
(Mehrfachauswahl setzt Step 7b architektonisch voraus, §9.1). Root-`CLAUDE.md`s „Noch nicht
entschieden"-Eintrag zum Item-Verschieben wird im selben Commit wie dieser Session-Block entfernt
(die Planungsfrage ist beantwortet, nur der Bau steht noch aus).

**Nachtrag, 2026-08-17, Bauauftrag „start atomically with the first step":** Step 7b **komplett
gebaut, drei Commits** (§4.1–§4.3/§4.4 je eine Schicht, wie im Plan vorgezeichnet). **1/3**
`storage/store.py :: move()` (vierte P1-Contract-Öffnung) · **2/3** `update_item(space=)`/
`_items_patch space=`, P6-AE-Rechtsprüfung, der in §4.2 vorhergesehene Guard-Routing-Fund
bestätigte sich real (`space is None`-Fix) · **3/3** Verschieben-Dialog + Space-Auswahl
(`dialogs.js`/`app.html`), **echt per Playwright verifiziert** (Login → Move `alpha`→`beta` →
Re-Auth-Formular → Erfolg, Screenshot gesehen) — dabei ein echter Fund: `closeMoveDialog()`
nullte `pendingMoveBody` vor dessen letzter Lesung, verschluckte die Erfolgsmeldung lautlos,
behoben. Details je Adapter: `phase1_storage/`/`phase2_mcp/`/`phase5_ui/CLAUDE.md`s
„[2026-08-17]"-Einträge, nicht doppelt hier. Ein eigener Fund dieser Session (kein Advisor-Fund):
ein zu grobes `old_string` beim Test-Einfügen schnitt einen bestehenden `test_api.py`-Test
versehentlich durch — per `git diff` bemerkt, nicht dem grünen Lauf vertraut, korrigiert.

**Verifiziert:** `pytest -q` 753→764 (Commits 1–2, Commit 3 ist reines JS/HTML, P5-T).
Charakterisierung grün. Tabu-Diff leer. Drag & Drop auf Space-Knoten (§4.4 Punkt 3) bewusst
nicht gebaut — P6-AB verlangt nur die Menüvariante als Pflichtweg.

**Step 7b DoD vollständig außer der Nikinger-Live-Probe** (echter Move über Connector UND UI,
Abnahmezeilen 25–30) — kein Deploy diese Session. **Nächster Schritt:** §9 (Mehrfachauswahl).

**Nachtrag, 2026-08-18, Abschluss-Review (der letzte Advisor-Call der Session, wie vom Nikinger
verlangt):** sechs Punkte geprüft, fünf grün ohne Codeänderung — Zielkollision beim Cross-Space-
Move ausgeschlossen (Dateiname trägt die global eindeutige Item-ID, `item_filename()`, Entscheidung
F aus P1; ein zweites Item mit derselben ID kann es per Index-`PRIMARY KEY` nicht geben), `version`/
`ConflictError` in `move()` vorhanden, kein verwaister Index-Eintrag im Quell-Space (`items.id
PRIMARY KEY`, `ON CONFLICT(id) DO UPDATE`, eine Zeile pro Item), `move_file()` fsynct Quell- UND
Zielverzeichnis, `visibility`/`share_read`/`share_write` bewusst unverändert mitziehend (P6-AH,
dokumentierte Entscheidung, kein Übersehen). **Ein echter Fund:** der in `ITEM_MOVE_PLAN.md` §4.5
gelistete Pflichttest `test_acl_decision_follows_the_item_into_the_target_space`
(`phase6_shares/tests/test_acl.py`) wurde in keinem der drei Step-7b-Commits gebaut — anders als
K4 (`test_create_item_accepts_folder`, Commit 2/3 dokumentiert explizit „bereits seit Step 7
Commit 3 erledigt") war diese Lücke nirgends vermerkt. Nachgebaut (kombiniert `Store.move()` mit
`Store.acl_of()`: Item wandert von `nikinger` — `write: [dritter]` — nach `fabian` — `read:
[vierter]` —, `acl_of()` danach liefert `fabian`s Grant, nicht mehr `dritter`s). 764→765, grün.
Zusätzlich der Titel des Session-Blocks oben datiert klargestellt (trug noch „keine Code-Änderung"
nach dem Bau-Nachtrag). Kein neuer Advisor-Call für diesen Fix — Budget dieser Session war mit der
Abschluss-Konsultation aufgebraucht, Fund + Behebung folgen direkt der Plan-Tabelle, keine neue
Designentscheidung. **Damit Step 7b DoD wirklich vollständig** (§4.5 jetzt 15/15 statt 14/15),
weiterhin nur die Nikinger-Live-Probe offen.

**Nachtrag, 2026-08-18, sophistizierter E2E-Lauf gegen eine echte Wegwerf-Instanz (Nikinger-
Auftrag, Standing Permission reconfirmt — siehe `docs/PROMPTS.md`s „Tests"-Absatz und
`[[feedback-throwaway-test-instance-permission]]`):** eigener Port 8799, eigenes `tmp`-
`DATA_ROOT`/`auth.sqlite3` (Scratchpad, kein Repo-Artefakt, `create_app()` direkt verdrahtet wie
`serve.py` es tut, aber mit einem selbst erzeugten DEK statt dem echten Keyring), zwei
Testprincipale `alpha`/`beta` + ein dritter geteilter Space `geteilt` (`write: [alpha, beta]`,
strukturell wie `IT-Sekus-Projekt`). Test-Tooling in einer neuen, eigenen venv
(`~/.claude-code-tools/e2e-venv`, Playwright+httpx), getrennt von `svg-venv` und der Projekt-
`.venv` — kein Vermischen von Testwerkzeugen mit Projekt- oder System-Python. Zwei echte
Stolperfallen beim Aufsetzen, beide behoben, keine Codeänderung am Produkt: (1) der CSRF-
Origin-Check (P5-H) verlangt eine `SPACE_PUBLIC_BASE_URL`, die exakt zum echten Browser-Origin
passt — `http://127.0.0.1:8799` funktioniert, weil Chromium `127.0.0.1` als vertrauenswürdigen
Ursprung behandelt und `__Host-`-Cookies dort trotz `http://` roundtripen; (2) TOTP-Replay-Schutz
ist pro Space global (`counter <= last_counter`), nicht pro Vorgang — ein Skript, das denselben
30-Sekunden-Code für Login UND einen Re-Auth-Dialog kurz danach wiederverwendet, bekommt den
zweiten Versuch abgelehnt; `totp_now()` blockiert jetzt bis zu einem echten neuen Zeitfenster.

**11 von 12 geskripteten Prüfungen grün, real im Chromium-Browser, gegen die echte laufende
App:** Verschieben-Dialog inkl. Space-Auswahl (own→shared) triggert Re-Auth korrekt, Abschluss
mit sichtbarem Erfolgs-Toast (der `pendingMoveBody`-Fund aus Commit 3/3 bleibt behoben), der
geleerte Quellordner verschwindet aus dem Baum (**Abnahmezeile 30 mechanisch bestätigt**),
`git log` im Wegwerf-`DATA_ROOT` zeigt exakt **einen** `move`-Commit (**Zeile 26s
Kernmechanik bestätigt**), beta sieht das von alpha verschobene Item im geteilten Space und kann
es speichern (**Zeile 27 mechanisch bestätigt**), In-Space-Drag-&-Drop funktioniert nach den
Step-7b-Änderungen an `dialogs.js`/`app.html` weiterhin (Regressionsprobe, `tree.js`/`list.js`
selbst unverändert), ein Drag auf einen fremden Space-Knoten löst nachweislich keine Anfrage aus
(bestätigt P6-ABs „Menü ist der einzige Pflichtweg" empirisch, nicht nur aus dem Code gelesen).
**Wichtig: dies ersetzt nicht die Nikinger-Live-Probe** (Abnahmezeilen 25–30 bleiben bei ihm/
Fabian als die maßgebliche Abnahme) — es ist eine Vorab-Erhärtung auf einer Wegwerf-Instanz,
kein Abhaken der Matrix.

**Zwei echte Funde, keine Erfindungen — beide code- UND empirisch bestätigt, nicht nur
vermutet:**

1. **Der Verschieben-/Freigeben-Knopf ist client-seitig an `item.space === state.ownSpace`
   gebunden** (`list.js`, `movable`-Variable, seit Step 7 unverändert, Step 7b hat sie nicht
   angefasst). Folge: sobald ein Item in einen geteilten Space wandert, sieht **niemand** —
   auch nicht, wer es verschoben hat — dort noch einen Verschieben-Knopf; ein Rückweg über die
   UI existiert nicht. Kollidiert mit keiner Abnahmezeile (25–30 verlangen nur die eine
   Richtung, nie den Rückweg über die UI), ist aber eine bewusste Einschränkung wert, dem
   Nikinger genannt zu werden statt stillschweigend zu bleiben — der Server selbst (`api.py`s
   `_items_patch`) verlangt diese Einschränkung nicht, nur `can_write` auf beiden Seiten.
2. **Abnahmezeile 28s Szenario (item-level `share_write` ohne space-level Grant) ist über die
   Web-UI nicht erreichbar, nicht nur nicht verschiebbar.** `GET /api/v1/spaces` filtert über
   `permissions.visible_spaces()` — reines space-level `can_read` aus `.share.yml`, ohne
   Rücksicht auf item-level `share_read`/`share_write`. Ein Space ohne space-level Grant taucht
   im Baum nie auf, und die Suche (`list.js`: `params.set("space", state.activeSpace)`) filtert
   serverseitig (`api.py :: _items_get` → `store.search(space=...)`) auf genau diesen einen
   Space — es gibt in der UI keinen „über alle lesbaren Items hinweg suchen"-Modus. Live
   bestätigt: `beta` fand das genau für dieses Szenario präparierte Item (`share_write:
   [beta]`, kein space-level Grant von `alpha`) über die Suche **nicht** (0 Treffer). Über den
   MCP-Connector funktioniert dasselbe Szenario nachweislich (`tools.py` filtert item-weise über
   `acl_of()`/`can_read_item`, unabhängig von Space-Sichtbarkeit — genau das prüft der
   bestehende Unit-Test `test_patch_item_level_share_write_holder_cannot_move_item_between_
   spaces`). **Frage an den Nikinger, keine Selbstentscheidung:** ist Zeile 28 als „über den
   Connector geprüft" gemeint (dann bereits erfüllt, nur nicht über die UI), oder ist ein
   „über alle lesbaren Items suchen"-Modus ein echter, bisher unentdeckter UI-Lückenschluss für
   eine spätere Phase? Keine Planänderung hier vorgenommen — reiner Befund.

**Kein Code-Fund am Produkt selbst** (beide Punkte sind Verhalten, nicht Bugs — der Server tut
in beiden Fällen genau das, was `permissions.py`/`api.py` vorsehen). Kein neuer Test im Repo
(die Prüfungen liefen ausschließlich gegen die Wegwerf-Instanz, Scratchpad, dieselbe Kategorie
wie die jsdom-/Playwright-Verifikationen aus P5 Steps 10/11 und P6 Step 3). `pytest` unverändert
765/765 (keine Produktänderung in diesem Nachtrag). Wegwerf-Instanz nach dem Lauf beendet, Port
8799 wieder frei, `~/.claude-code-tools/e2e-venv` bleibt als wiederverwendbares Werkzeug stehen
(dieselbe Kategorie wie `svg-venv`, Werkzeug-Ebene, kein Repo-Artefakt).
