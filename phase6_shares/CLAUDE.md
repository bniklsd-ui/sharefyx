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
  - ./SESSIONS_ARCHIVE.md                          # Steps 0-7 verbatim (sieben Eintraege), L3, kein Softcap
updated: 2026-08-14, achter + drei Nachtraege -- (Step 7 vollstaendig: Commits 0-6 inkl. 5a/5b-Split, siebter-Block rotiert; Pre-Deploy-Testschwelle vor v2.1 -- 747 pytest + 3 Smoke-Skripte + neu 30/30 echter Browser-E2E [Playwright, Scratchpad, nicht im Repo] gegen Step 7/7a, vier Harness-Fehler unterwegs gefunden+korrigiert, keine Produktbugs, UPDATE_LOG-Datumsluecke dem Nikinger vorgelegt+akzeptiert; Werkzeug-Ergonomie: die irrefuehrende patch_item-Fehlermeldung behoben (keine nummerierte Liste, Korrektur zum eigenen vorigen Nachtrag), fuenf Vormerkungspunkte bleiben offen; Gate B blockiert Step 8 architektonisch, noch nicht deployt)
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
| 15 | UI Dateisystem (Block B), Commit 5b/7 — Freigabe-Dialog + Re-Auth-Mini-Formular, kein Backend-Fund nötig (Gate seit Commit 5a live). `list.js`: neuer „⇄"-Freigeben-Knopf, GESCHWISTER von `.list__row`/`.list__row-move` (dieselbe Nested-Button-Regel), dieselbe `movable`-Bedingung. `dialogs.js`: `openShareDialog()`/`closeShareDialog()` (Picker aus `state.spaces`, drei-stufiges `<select>` pro fremdem Space: kein Zugriff/lesen/schreiben — `schreiben` impliziert `lesen` bereits über `decision_for()`s Vereinigung, keine doppelte Eintragung), `collectShareBody()`, Submit-Handler mit eingefrorenem `pendingShareBody` (Advisor-Vorgabe: erste Fassung beim ersten Absenden fixiert, nur `password`/`totp` werden bei jedem Retry frisch gelesen). `app.html`: `#share-dialog` (statische Hülle, `pw-field`/`pw-toggle` von `initPasswordToggles()` automatisch erfasst, kein neuer JS-Code dafür). `app.js`: `#share-dialog` in `anyOverlayOpen()`/Escape aufgenommen (dieselbe dokumentierte Abweichung wie Commit 3). `app.css`: `.list__row-share` teilt sich die Regel mit `.list__row-move`. **Bewusster Scope-Schnitt (Advisor bestätigt):** kein `visibility`-Feld im Dialog — der Chip zeigt sie bereits, niemand hat eine UI-Änderung dafür verlangt | 7 | ✅ **gebaut, noch nicht deployt** — Details, Advisor-Bestätigung und die Zwei-venv-Playwright-Verifikation: Session-Block unten | 0 (P5-T: JS/HTML/CSS bleiben unit-ungetestet; 746 gesamt unverändert, reiner Frontend-Commit — Tabu-Diff bestätigt nur `phase5_ui/webui/static/`) |
| 16 | UI Dateisystem (Block B), Commit 6/7 — `space_admin_enabled`-Stub, Seam ohne Implementierung (P5-Z-Kategorie), Step 7 damit vollständig. `config.py`: `UiSettings.space_admin_enabled: bool = False`, dieselbe Feld-statt-Env-Var-Konvention wie `hsts` — ohne Laufzeitwirkung, `app.html` ist statisch, kein Templating. `app.html`: neuer, hart `disabled` (nicht nur versteckter) Menüpunkt „Geteilte Spaces verwalten — kommt in Phase 7" im Konto-Dialog, Geschwister von „Update-Log ansehen" | 7 | ✅ **gebaut, noch nicht deployt, Step 7 vollständig** | +1 (`phase5_ui/tests/test_static_routes.py`, dokumentierte Abweichung vom Plan-Dateiwortlaut — der nennt `test_pages_markup.py`, das testet aber ausschließlich `webui/pages.py`s servergerenderte Seiten, nie `app.html`; `test_static_routes.py` liest `app.html` bereits direkt, dort ist der Test sachlich richtig); 747 gesamt |

## Geerbte Contracts

**[2026-08-09, P6 Step 0] Dritte, benannte Öffnung des P1-Contracts** (Plan §1.4): `models.py`
bekommt `folder`/`visibility`/`share_read`/`share_write`, `store.py` bekommt `acl_of()`/`patch()`/
erweiterte `create()`/`update()`/`search()`/`list_spaces()`. Wird in Step 4 umgesetzt, hier nur
angekündigt — nach Phasenabschluss (Step 10) wieder geschlossen, siehe `phase1_storage/CLAUDE.md`.

## Vormerkungen (nicht Teil eines aktuellen Steps)

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

## Session stopped — 2026-08-14, achter — (Step 7 vollständig, Rotation, Werkzeug-Feedback vorgemerkt)

**Step 7 (UI Dateisystem, Block B) ist mit Commit 6 vollständig** — alle sieben Sub-Commits
(0–4, 5a, 5b, 6, der Plan zählt 5a+5b als den einen Commit 5) gebaut, verifiziert, committet.
Voller Verlauf, jeder einzelne Commit mit Code/Verifikation/Advisor-Funden:
`SESSIONS_ARCHIVE.md`, Block „siebter" (frisch rotiert, dieser Commit). Kurzfassung: `app.js` in
zehn ES-Module gesplittet · echter Ordnerbaum · Sichtbarkeits-Chip · Ordner anlegen+Verschieben
per Menü (K4-Fix) · Drag & Drop · Re-Auth-Gate (Backend `webui/shares.py`/`AclDecision`-
Erweiterung, Frontend Freigabe-Dialog) · `space_admin_enabled`-Stub. 747 Tests grün, Tabu-Diff
gegen die korrekte P6-C-Liste sauber bei jedem einzelnen Commit. **Noch nicht deployt** — Step 7a
(Textfarben-Token) wartet ebenfalls weiter auf den Sudo-Neustart des Nikingers.

**Rotation durchgeführt, diese Session:** der „siebter"-Block hatte acht Nachträge angesammelt,
~61 KB, weit über dem 40KB-Softcap. Das Rotationsskript (`scripts/rotate_session_block.sh`)
greift nur bei ≥2 Blöcken im Kopf; hier lag genau einer vor, deshalb von Hand nach derselben
Byte-Identitäts-Disziplin: verbatim per `sed` extrahiert, in `SESSIONS_ARCHIVE.md` eingefügt,
Körper (alles außer der bewusst präzisierten Titelzeile, gleiche Praxis wie die zweite Rotation)
byte-für-byte gegen das Original verglichen, `diff` lief leer. Herleitung + Rotationsvermerk:
`SESSIONS_ARCHIVE.md`s Kopf, „Sechste Rotation".

**Werkzeug-Ergonomie-Feedback vorgemerkt, nicht gebaut:** eine arbeitende Claude-Instanz meldete
nach einem sitzungsreichen Protokollierungstag sechs Punkte zu den MCP-Tools selbst (Bulk-Append,
`list_spaces`-Auffindbarkeit, `patch_item`-vs-`update_item`-Abgrenzung, `get_item`s immer-voller
Body, undokumentierte Status-Enum-Werte, `patch_item`s irreführende Fehlermeldung bei einem
Frontmatter-Zugriffsversuch) — vollständig in „Vormerkungen" oben festgehalten, Kurzfassung in
Root-`CLAUDE.md`s „Noch nicht entschieden". Betrifft `mcpserver/tools.py`, außerhalb des
Step-7-Scopes, nichts davon in dieser Session verändert.

**Verifiziert (Rotation selbst):** `diff` zwischen dem extrahierten Originalblock und seiner
neuen Position in `SESSIONS_ARCHIVE.md` leer (Körper), die übrigen fünf archivierten Blöcke
unverändert (`diff` gegen den alten Archivstand ebenfalls leer). `pytest` nicht erneut gelaufen
(reine Doku-Operation, keine Code-Änderung seit Commit 6s eigener Verifikation — 747 gesamt).

**Nächster Schritt (konkret):** Deploy von Step 7 ist die größte offene Live-Aufgabe der Phase —
eine bewusste Nikinger-Entscheidung, wann, kein beiläufiger Nebeneffekt eines Commits. Danach:
Step 8 (Bilder, Block C) oder das vorgemerkte Werkzeug-Ergonomie-Feedback, Priorisierung liegt
beim Nikinger. Rotationsprüfung für die nächste Session: dieser Kopf trägt jetzt wieder genau
einen, kompakten Session-Block — kein weiterer Rotationsbedarf, bis er selbst wieder wächst.

**Nachtrag, 2026-08-14 — Pre-Deploy-Testschwelle vor v2.1 (Nikinger-Auftrag „test everything
possible in throwaway instances"):** vor dem gebündelten Deploy von Step 7 + Step 7a einmal
alles Erreichbare geprüft, nicht nur `pytest` behauptet. Vier Ebenen: `pytest` (747/747, keine
Drift), die drei bestehenden Smoke-Skripte (`mcp_smoke.py` 13/13, `oauth_smoke.py` 11/11,
`ui_smoke.py` 12/12 — alle gegen ein temporäres `DATA_ROOT`/`AuthStore`, nie das echte), und
**neu:** ein echter Browser-E2E-Lauf gegen eine temporäre, TLS-terminierte `uvicorn`-Instanz
(Playwright, headless Chromium), weil die ersten drei Ebenen die zehn seit Step 7 gesplitteten
JS-Module (`app.js` → zehn Dateien) nie tatsächlich ausführen — `pytest` ist Python, `ui_smoke.py`
läuft über `httpx.ASGITransport`, keins von beiden rendert eine Seite. Skripte
(`throwaway_server.py`, `e2e_step7.py`) bewusst **nicht** ins Repo übernommen — dieselbe
Disziplin wie die jsdom-/Playwright-Simulationen aus P5 Step 10/11/13 (Scratchpad, nicht
versioniert), gedeckt durch P5-T (JS bleibt laut Plan unit-ungetestet, kein Build-Step).
`playwright==1.62.0` lokal ins Projekt-`.venv` installiert (kein Download nötig, Chromium-Build
war bereits unter `~/.cache/ms-playwright` gecacht, sichtbar an Commit 5bs eigener Erwähnung
einer Playwright-Verifikation) — kein Repo-Code importiert es, berührt also auch den
`pytest`-Lauf im Deploy-Release nicht.

**Ergebnis, zwei stabile Läufe hintereinander: 30/30 Prüfungen grün**, viele davon gegen
Server-Wahrheit gegengeprüft statt nur gegen "der Dialog hat sich geschlossen" — Ordner-
Verschieben per Menü UND per Drag & Drop landet tatsächlich auf der Platte, der No-op-Drop-Guard
(benannter Advisor-Fund aus Commit 4) bumpt wirklich keine Version, ein falsches Re-Auth am
Freigeben-Dialog schreibt nachweislich nichts (Version unverändert), ein richtiges landet genau
einen PATCH (`version_before + 1`, `share_write=['beta']`), der Sichtbarkeits-Chip springt
sichtbar auf „geteilt mit beta", die Textfarben aus Step 7a bestehen 16,5:1 gegen ihren
tatsächlich gemalten Hintergrund (WCAG-AA-Schwelle 4,5:1), und der fremde Space `beta` zeigt
`+`/`+ Ordner` nachweislich **nicht im DOM**, nicht nur `hidden` (P5-Abnahmezeile 12, derselbe
Code-Pfad `activeSpaceWritable()`, der am 2026-08-13 zweimal traf).

**Nebenfund, korrigiert eine Aussage aus Commit 4s eigener Commit-Message:** die dortige Notiz
nannte nur Commit 5b als real-browser-verifiziert. Mit diesem Lauf sind Drag & Drop UND der
No-op-Drop-Guard aus Commit 4 jetzt ebenfalls über einen echten (headless) Chromium bestätigt —
`page.mouse.down/move/up` reichte aus, Chromium synthetisiert daraus die nativen HTML5-
Drag-Events selbst, kein `DragEvent`-Konstrukt nötig.

**Vier Harness-Fehler unterwegs gefunden und korrigiert, festgehalten als wiederverwendbares
Wissen für den nächsten, der diesen Aufbau erneut braucht:**
1. Fehlender `static_routes()`-Mount → jede statische Datei `404` — `ui_smoke.py` navigiert nie
   real, ein echter Browser schon.
2. `wait_for_selector("...[hidden]")` wartet per Default auf „sichtbar" — ein Element mit
   `hidden`-Attribut kann das nie erfüllen, braucht `state="attached"`.
3. Der „Bucket"-Filter in der Liste filtert nach Typ, nicht nach Ordner — ein bereits
   verschobenes Item bleibt im alten Bucket sichtbar und sortiert (nach `-updated`) sogar zuerst.
   Ein blindes `.first` als Drag-Quelle traf deshalb zuerst das falsche (schon verschobene) Item
   — `tree.js`s No-op-Drop-Guard (Commit-4-Advisor-Fund) griff korrekt und tat nichts, was wie
   ein Bug aussah, aber keiner war. Quelle jetzt über Server-Wahrheit (`folder == ""`) gewählt,
   nicht blind über Listenposition.
4. Zwei Prüfungen waren anfangs Tautologien (`count() >= 0`; ein globaler Selektor, der auch
   das eigene, immer gerenderte „+ Ordner" des eigenen Space traf, unabhängig vom aktiven
   Space) — beide auf echte, falsifizierbare Aussagen umgestellt (Kontrast gegen den
   tatsächlich gemalten Vorfahren statt gegen reines Schwarz; Zähl-Erwartung auf „genau 1, für
   Alpha" statt „0").

**Zwei Punkte dem Nikinger vorgelegt, einer akzeptiert:**
- `docs/UPDATE_LOG.md`s oberster Eintrag stand auf `2026-08-13`, zum Zeitpunkt der Prüfung war
  bereits `2026-08-14` — `deploy.sh`s P6-X-Gate bricht ohne einen auf den Deploy-Tag datierten
  obersten Eintrag ab. **Vom Nikinger akzeptiert** (kein neuer Eintrag von Claude Code
  geschrieben — welcher Änderungstext dort steht, ist eine Autorenentscheidung des Nikingers,
  kein Rateversuch), Deploy-Tag entscheidet, welches Datum tatsächlich hinein muss.
- Ein gebündeltes Deploy aus Step 7 + Step 7a bedeutet: `deploy.sh`s Auto-Rollback nimmt bei
  einem Health-Gate-Fehlschlag beide zusammen zurück. Nikinger-Entscheidung, mitgetragen.

**Verifiziert:** `pytest -q` 747/747 (Baseline, vor jeder Änderung dieser Session). Alle drei
Smoke-Skripte grün (Zahlen oben). Browser-E2E 30/30, zwei Läufe hintereinander stabil. Kein
Produktcode in dieser Teilsession geändert (`git status` vor dem folgenden Werkzeug-Ergonomie-
Fix leer) — reine Verifikation, kein Fund, der einen Fix gebraucht hätte, bis auf den eigenen
Harness (oben, nie Produktcode).

**Nächster Schritt (aktualisiert):** Deploy bleibt beim Nikinger. Block C (Step 8, Bilder) ist
architektonisch durch **Gate B** blockiert (`docs/concepts/phase6_shares_plan.md` §4, „🚦 GATE B" —
Niklas allein, danach eine gemeinsame Sitzung mit Fabian, dritter Space live, Abnahmezeilen
8–18) — dieses Gate braucht den echten Deploy und echte Live-Sitzungen, keine Claude-Code-Session
kann es passieren. Der Deploy ist damit die entsperrende Aktion für Gate B, nicht etwas, das sich
durch mehr Vorab-Arbeit umgehen lässt. Was **nicht** hinter Gate B liegt und heute noch bearbeitet
werden kann: die vorgemerkte Werkzeug-Ergonomie-Feedback-Liste (`mcpserver/tools.py` ist laut
P6-C offen) — siehe eigener Nachtrag unten für den einen Punkt, der in dieser Session bereits
behoben wurde.

**Nachtrag, 2026-08-14 — Werkzeug-Ergonomie: die irreführende `patch_item`-Fehlermeldung
behoben.** **Korrekturnotiz zum vorigen Nachtrag:** dort stand „Punkt 6" — es gibt keine
nummerierte Liste, der Bug ist die im Vormerkungen-Abschnitt gesondert hervorgehobene, schärfere
Lesart von Punkt 3 (`patch_item` vs. `update_item` nirgends zusammengefasst), keine siebte,
eigenständige Position. `mcpserver/tools.py :: map_storage_error()` gab bei `PatchError.found
== 0` bisher „lies das Item neu mit get_item und prüfe den exakten Text" zurück — klingt nach
einem Textmatching-Problem, obwohl `patch_item` Frontmatter-Felder kategorisch nie erreicht
(operiert ausschließlich auf dem Body-String); ein erneutes Lesen hätte in diesem Fall nie
geholfen. **Minimalster Fix, kein Feature:** die Meldung nennt jetzt den tatsächlichen Grund
(„patch_item durchsucht nur den Body-Text, nie das Frontmatter") und die konkrete Alternative
(„für title/status/tags/due/links/folder/visibility/share_read/share_write nutze update_item")
— **keine** Frontmatter-Erkennungs-Logik ergänzt (Advisor-Vorgabe: `patch_item` kennt
Frontmatter nicht, eine Heuristik über `old_text`s vermutete Herkunft wäre Raten, kein Wissen).
Bestehender Test `test_patch_item_zero_match_error_maps_to_patch_failed_tool_error`
(`phase2_mcp/tests/test_tools.py`) um zwei Assertions erweitert (`"Body-Text"`, `"update_item"`
in der Meldung), kein neuer Test nötig — reine Textänderung an derselben Fehlerklasse.
`pytest phase2_mcp/tests/test_tools.py` 40/40, volle Suite weiterhin 747/747 (keine neuen
Tests, nur erweiterte Assertions). Die übrigen fünf Vormerkungspunkte (Bulk-Append,
`list_spaces`-Auffindbarkeit, `get_item_meta`, Status-Enum-Dokumentation, Suchtreffer-
Zuverlässigkeit) bleiben unverändert offen — größerer Zuschnitt, nicht in dieser Session
angefasst.

**Nachtrag, 2026-08-14 — UPDATE_LOG.md-Flag geschlossen, Deploy heute:** der Nikinger deployt
v2.1 noch am selben Tag, damit ist die vorher offene Datumslücke gegenstandslos — neuer,
oberster Eintrag `## 2026-08-14` in `docs/UPDATE_LOG.md` ergänzt (drei Zeilen: echte Ordner
+Verschieben, Sichtbarkeits-Anzeige pro Notiz, Freigeben-Knopf mit Re-Auth bei Erweiterung),
Wortlaut diesmal von Claude Code formuliert statt offengelassen — der Nikinger hat das
ausdrücklich beauftragt (anders als beim Flag selbst, das bewusst nicht vorweggenommen wurde).
`deploy.sh`s P6-X-Gate ist damit ohne `SHAREFYX_ALLOW_STALE_UPDATELOG=1` passierbar. Zusätzlich
`git push` (lokal 11 Commits vor `origin/main`) — technisch nicht nötig, `deploy.sh` klont vom
lokalen Repo, nie von GitHub (`SHAREFYX_SOURCE_REPO`-Default), aber sinnvolles Backup, da diese
VM sonst die einzige Kopie dieser Historie ist. Auf Nikinger-Wunsch, kein `--force`, reiner
Fast-Forward.
