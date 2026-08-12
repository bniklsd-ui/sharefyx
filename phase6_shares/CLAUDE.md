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
updated: 2026-08-12 (Step 5 gebaut -- SharePolicy/Surface ersetzt OwnSpaceWritable, item-level ACL in tools.py/webui/api.py, Folder-Move-Fail-Closed [Nikinger-Entscheidung], 691 Tests gruen)
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
| 6 | Rechtepolitik (Block B): `storage/acl.py` +`grants_for_space()`/`decision_for()`, `store.py` +`acl_reader`-Property (kleine, dokumentierte Erweiterung über Step 5s Dateiliste hinaus), `mcpserver/permissions.py` (`Surface`, `SharePolicy` ersetzt `OwnSpaceWritable`), `mcpserver/app.py` (Verdrahtung über `store.acl_reader`), `mcpserver/tools.py` (alle sieben Tools auf `acl_of()`+`can_read_item`/`can_write_item` umgestellt, `search_items`/`list_spaces` item-weise statt space-weise gefiltert, `create_item(space=, folder=)`, `update_item(folder=)`), `webui/api.py`+`serializers.py` (dieselbe Umstellung, `Surface.HUMAN` über `SharePolicy.can_read_item_as_human()` gekapselt — P5-B erlaubt weiterhin nur ein `mcpserver`-Symbol) | 5 | ✅ **gebaut, 2026-08-12** — DoD aus Plan §4 Step 5 erfüllt, alle 12 Pflichttests + ein zusätzlicher Fail-Closed-Fund abgedeckt; noch nicht live geprüft (kein eigener Abnahmematrix-Punkt) | +9 `phase2_mcp/tests/test_tools.py` (30→39) + 7 `test_permissions.py` (3→10, Datei vollständig neu geschrieben) + 2 `phase5_ui/tests/test_api.py` (27→29) + 2 `test_serializers.py` (7→9), Kollateralkorrekturen in `phase2_mcp/tests/test_app.py`/`phase5_ui/tests/test_overview.py`/conftest-Fixtures (keine neuen Tests, nur Assertions auf die neue ACL nachgezogen); 691 gesamt |

## Geerbte Contracts

**[2026-08-09, P6 Step 0] Dritte, benannte Öffnung des P1-Contracts** (Plan §1.4): `models.py`
bekommt `folder`/`visibility`/`share_read`/`share_write`, `store.py` bekommt `acl_of()`/`patch()`/
erweiterte `create()`/`update()`/`search()`/`list_spaces()`. Wird in Step 4 umgesetzt, hier nur
angekündigt — nach Phasenabschluss (Step 10) wieder geschlossen, siehe `phase1_storage/CLAUDE.md`.

---

## Session stopped — 2026-08-12 (Step 5 — Rechtepolitik, Block B)

**Auftrag:** Step 5 aus `docs/concepts/phase6_shares_plan.md` §4 — `SharePolicy`/`Surface`
ersetzen `OwnSpaceWritable`, jeder item-level Lese-/Schreibpfad in `mcpserver/tools.py` und
`webui/api.py` wechselt von `space_of()`+space-level `can_read`/`can_write` auf `acl_of()`+
`can_read_item`/`can_write_item`. Vorbereitung: Advisor-Review des Plans vor dem Bau, gefolgt
von einer expliziten Nikinger-Entscheidung zu einem Fund außerhalb des Plan-Texts (siehe unten).

**Advisor-Fund vor dem Build, dem Nikinger vorgelegt statt still entschieden:** `folder` ist
seit Step 4 agenten-setzbar (`store.py`s Kommentar an `update()`s `folder`-Zweig sagte das
bereits ausdrücklich). Ein `share_write`-Halter, der ein fremdes Item in einen Ordner mit
breiterer `.share.yml` verschiebt, hätte dessen effektive Sichtbarkeit erweitert, ohne dass
Step 7s `widens()`/Re-Auth-Gate das je sähe — dieses Gate existiert nur für den
Menschen/UI-Pfad, die Agentenfläche hat grundsätzlich keinen Re-Auth-Mechanismus. **Nikinger-
Entscheidung (AskUserQuestion, 2026-08-12):** ein Nicht-Eigentümer darf `folder` nie ändern,
dauerhaft, nicht nur bis Step 7. Umgesetzt in beiden Adaptern (`tools.py::update_item`,
`webui/api.py::_items_patch`), je ein `ValidationError`/`403 forbidden` **vor** dem Schreiben,
je ein Test (`test_share_write_cannot_move_item_to_a_different_folder` in beiden Test-Dateien).

**`storage/acl.py` + `store.py` — kleine, dokumentierte Erweiterung über Step 5s Dateiliste
hinaus** (P6-C erlaubt `storage/`-Touches in dieser Phase generell): `Store.__init__` baute
bisher einen privaten `AclReader` ohne Zugriffspunkt — der Plan verlangt "ein Handle, kein
zweiter" für `SharePolicy` und `Store`. `Store.acl_reader` (neue Property) gibt genau diese
Instanz zurück. `AclReader.grants_for_space()` (neu, dünner Wrapper um `grants_for_dir()` auf
der Space-Wurzel) und `AclReader.decision_for()` (neu — die Vereinigungslogik, die
`Store.acl_of()` vorher inline berechnete) sind die Basis für `SharePolicy`s space-level
`can_read`/`can_write` UND für die item-weise Filterung in `search_items`/`GET /api/v1/items`
(eine `AclDecision` je `ItemSummary`-Zeile aus einem bereits geladenen `store.search()`-Ergebnis,
kein zweiter Index-Roundtrip pro Treffer). `Store.acl_of()` delegiert jetzt an `decision_for()`
statt die Logik zu duplizieren. Reine Refaktorierung, kein Verhalten geändert — die drei
Charakterisierungs-Goldens liefen vor UND direkt nach dieser einen Änderung isoliert grün,
bevor der Rest des Steps begann (P6-D, gezielt statt erst am Ende geprüft).

**`mcpserver/permissions.py`:** `Surface(str, Enum)` (`AGENT`/`HUMAN`), `Permissions`-Protokoll
um `can_read_item`/`can_write_item` erweitert, `SharePolicy(acl: AclReader)` ersetzt
`OwnSpaceWritable` vollständig (nicht danebengestellt). **Ein Punkt, den der Plan-Text nicht
auflöst und der beim Bau auffiel:** P5-B erlaubt dem UI-Paket genau ein Symbol aus `mcpserver`
— der Plan sagt nur "das Symbol ändert sich zu `SharePolicy`", sagt aber nicht, wie der
REST-Adapter dann `surface=Surface.HUMAN` an `can_read_item` übergeben soll, ohne `Surface`
als zweites Symbol zu importieren. Gelöst über `SharePolicy.can_read_item_as_human()` — eine
`SharePolicy`-eigene Bequemlichkeitsmethode, nicht Teil des `Permissions`-Protokolls, die
`Surface.HUMAN` innerhalb von `mcpserver/permissions.py` kapselt. `test_webui_imports_exactly_
one_mcpserver_symbol` (`phase5_ui/tests/test_api.py`) hält das jetzt gegen `{"mcpserver.
permissions.SharePolicy"}` fest, nicht mehr gegen `OwnSpaceWritable`.

**`mcpserver/app.py`:** `own_space_writable = OwnSpaceWritable()` → `permissions =
SharePolicy(store.acl_reader)`, an `build_mcp()` und `api_routes()` unverändert durchgereicht
(kein Signaturbruch, wie vom Plan vorhergesagt).

**`mcpserver/tools.py`, alle sieben Tools:** `get_item`/`update_item`/`append_to_item`/
`patch_item` lösen ihre Rechte jetzt über `store.acl_of(item_id)` statt `store.space_of(item_id)`
auf. `get_item` hält die „eigen"-Frage bewusst in zwei Variablen (Advisor-Fund, siehe Planungs-
Session): `writable` (steuert `repair_drift`) ist nicht dasselbe wie „gehört der Space" (steuert
den `<untrusted_content>`-Wrap, P6-O — ein geteiltes, aber schreibbares Item bleibt trotzdem
gewrappt). `search_items` filtert jetzt item-weise über `can_read_item` statt space-weise über
`visible_spaces` (Pflicht, nicht Komfort — sonst würde ein einzeln freigegebenes Item entweder
seinen ganzen Ordner mit sichtbar machen oder space-weise verschwinden, je nachdem wie
vorgefiltert würde) und bekommt einen `folder`-Parameter. `list_spaces` zeigt jetzt `members`/
`folders` je Space und zieht `visibility: human`-Items aus den `item_count`-Zählern ab (P6-P
gilt wörtlich auch für diese Zähler, nicht nur für `search_items/total`). `create_item` bekommt
`space=`/`folder=` (P6-U: Ziel-Space per Default die eigene, ein anderer nur mit `write:` in
deren `.share.yml`). `update_item` bekommt `folder=` (mit dem Fail-Closed-Riegel von oben);
`visibility`/`share_read`/`share_write` bleiben verboten (P6-M, unverändert). Die generische
`PermissionDenied`-Fehlermeldung (`map_storage_error`) wurde umformuliert — sie deckt jetzt drei
Ursachen ab (fremder Space, ungeteiltes Item, `visibility: human`), die alte Formulierung
("ist nicht dein Space") wäre für den dritten Fall (eigener Space, aber `visibility: human`)
schlicht falsch gewesen.

**`webui/api.py` + `webui/serializers.py`:** dieselbe Umstellung mit `Surface.HUMAN` (über
`can_read_item_as_human()`, siehe oben). `_items_get` filtert item-weise (inkl. `folder`-Query-
Parameter); `_items_get_one`/`_items_patch`/`_items_append`/`_items_archive` auf `acl_of()`+
`can_write_item` umgestellt. `serializers.py`: `item_to_json`/`summary_to_json` bekommen
`folder`/`visibility`/`share_read`/`share_write`/`shared`; `readonly` wird weiterhin vom
Aufrufer übergeben (keine Store-Aufrufe in `serializers.py`), jetzt aber ACL-basiert statt
reiner Space-Identität. `search_to_json()` ist auf eine dünne Hülle um bereits fertige
Item-Dicts geschrumpft (die ACL-Auflösung braucht `store.acl_reader`, das gehört in `api.py`,
nicht in die reine Übersetzungsschicht). `space_to_json` bekommt `members`/`folders`.
**Bewusst nicht Teil dieses Steps** (Step 5s Dateiliste nennt sie nicht, gehören zu Steps 7/8):
`kind: own|shared|foreign` auf Spaces, `/api/v1/meta`s neue Felder, `/api/v1/items/{id}/share`,
`GET /api/v1/overview`s `human`-Zähler (bräuchte einen `Store.search(visibility=)`-Filter, den
es nicht gibt, oder einen Rohscan — `_overview()` bleibt unangetastet).

**Testfolge, mandatiert vom Plan (§4 Step 5, zwölf Pflichttests) plus der eine Fail-Closed-
Ergänzung:** elf der zwölf sind neu in `phase2_mcp/tests/test_tools.py`/`test_permissions.py`
gebaut (die zwölfte, `test_acl_of_does_not_read_the_item_file`, existierte schon seit Step 4 in
`phase1_storage/tests/test_store.py`). Mehrere bestehende Tests mussten auf die neuen Semantiken
umgeschrieben werden, nicht nur die Fixtures — das ist die eigentliche Substanz dieser Session,
kein Nebeneffekt: `OwnSpaceWritable` machte jeden fremden Space universell lesbar
(`readonly=True`, aber `200`); ohne Freigabe ist ein fremdes Item jetzt unsichtbar/`403`
(`test_get_item_from_foreign_space_without_share_is_forbidden` ersetzt das alte "immer
lesbar"-Verhalten, `test_spaces_omits_foreign_space_without_a_share` ebenso auf der REST-Seite).
Betroffen waren auch die beiden Isolationstests in `phase2_mcp/tests/test_app.py`
(`test_principal_isolation_under_concurrency`, `test_all_seven_tools_are_callable_over_http`) —
Ersterer bekam eine STRENGERE Zusicherung (fremder Space fehlt jetzt ganz, statt nur
`writable=False`), Letzterer eine `.share.yml`, weil er den fremden Lese-Pfad ausdrücklich
demonstriert. Dieselbe Anpassung war für `phase2_mcp/scripts/mcp_smoke.py` und
`phase5_ui/scripts/ui_smoke.py` nötig (beide seeden seit P2/P5 einen fremden Space, ohne den
wären ihre eigenen „fremd lesen"-Prüfungen ab jetzt am neuen Fail-Closed-Default gescheitert,
nicht an einem Bug) — beide Skripte demonstrieren den Lese-Pfad in einen geteilten Space
absichtlich, deshalb hier bewusst `read: [<eigener Space>]` gesetzt statt den Test zu entschärfen.

**Verifiziert:** `pytest -q` (gesamtes Repo) → **691 passed** (671 + 9 `test_tools.py` + 7
`test_permissions.py` + 2 `test_api.py` + 2 `test_serializers.py`, keine Regression sonst).
Charakterisierungs-Goldens liefen isoliert vor+direkt nach dem `storage/acl.py`/`store.py`-Schritt
grün (oben) UND am Ende erneut. `git status --short` zeigt ausschließlich `storage/`,
`mcpserver/`, `phase2_mcp/{scripts,tests}`, `phase5_ui/{scripts,tests,webui}` — kein
`authserver/`-Touch, wie erwartet (P6-C erlaubt `storage`/`mcpserver`/`tools.py`/
`permissions.py`, nicht `authserver`). **Real ausgeführt, nicht nur `pytest`** (`SHAREFYX_*`/
`SFX_*` aus der Umgebung entfernt, wie nach dem 52-Neustart-Vorfall Pflicht): `phase2_mcp/
scripts/mcp_smoke.py --json` (13/13 `ok:true`), `phase5_ui/scripts/ui_smoke.py --json` (12/12
`ok:true`), `phase5_ui/scripts/ui_budget.py --json` (alle Budgets `ok:true`, echte
220-Item-Messung, `all_within_budget:true`).

**Status:** Step 5 ist damit **gebaut**, DoD aus Plan §4 Step 5 erfüllt (zwölf Pflichttests +
Fail-Closed-Ergänzung grün, reale Skript-Läufe grün). Kein eigener Abnahmematrix-Punkt für
diesen Step — die Live-Prüfung kommt mit den nutzerseitig sichtbaren Steps 6/7 (Verwaltung/
Migration, UI), Zeilen 8–18 der Abnahmematrix.

**Nächster Schritt (konkret):** Step 6 (Verwaltung und Migration) — `phase6_shares/scripts/
spacectl.py` (neu, `create-space`/`list-spaces`/`add-member`/`remove-member`/`show`/
`remove-space`), `phase6_shares/scripts/migrate_visibility.py` (neu, `--dry-run` Default,
schreibt `visibility: private` in Bestandsdateien ohne das Feld), `phase3_edge/scripts/
diagnose.sh`-Erweiterung. DoD: ein geteilter Space existiert real, ein dritter Nutzer ist
angelegt, `diagnose.sh` meldet keine verwaisten Namen. Gate-A→B-Punkt-3-Erinnerung bleibt
gültig (frühestens 2026-08-28), unabhängig vom Baufortschritt hier.
