---
status: live
purpose: Archivierte Session-stopped-Blöcke aus phase6_5_tools_images/CLAUDE.md, verbatim, newest-first
read-when: Auditieren der vollen Phase-6.5-Historie — der aktuelle Session-Block lebt im Phase-Head, nicht hier
detail: L3
up: ./CLAUDE.md
down:
updated: 2026-08-20 (zweite Rotation -- Block-A-Session-Block verschoben, Head traegt seither den Block-B-Step-B1-Session-Block)
---
# SESSIONS_ARCHIVE.md — Phase 6.5: Werkzeug-Ergonomie und Bilder

Zwei Einträge, newest-first, verbatim aus `phase6_5_tools_images/CLAUDE.md` per
`scripts/rotate_session_block.sh phase6_5_tools_images`.

## Session stopped — 2026-08-20 (Block A gebaut: get_item_meta, Beschreibungen, in_body=)

**Auftrag:** Nikinger empfahl Block A zuerst (reine `tools.py`-Arbeit, keine Abhängigkeit von
Block B, „unter Druck fällt Block B weg, nie Block A" laut Plan-Mission) und bat um atomare
Schritte, damit `/context` dazwischen geprüft werden kann.

**Gebaut, Steps A1+A2+A4 in einem Durchgang** (A2 zieht `get_item`s Beschreibung auf
`get_item_meta` vor, das ohne A2 noch nicht existiert hätte — Forward-Reference vermieden statt
mit xfail/TODO offengelassen; A4 macht `search_items`s A1-Beschreibungssatz „…oder
`in_body=True` setzen" wahr, statt eine Beschreibung für einen noch nicht existierenden
Parameter zu schreiben):
- `mcpserver/tools.py` — `_status_hint()` (aus `storage.models.STATUS_VALUES` generiert, nie
  abgetippt, P6.5-C), `WRITE_TOOL_DIVISION`, `_LIST_SPACES_POINTER` als Modul-Helfer neben
  `compact_json()`. Beschreibungen von `list_spaces` (Falschaussage „nur eigener Space" raus,
  P6.5-B), `search_items` (Suchreichweite ehrlich benannt + `in_body`-Hinweis, P6.5-H),
  `get_item` (Verweis auf `get_item_meta`), `create_item`/`update_item`/`append_to_item`/
  `patch_item` (`WRITE_TOOL_DIVISION` + `_status_hint()` an den beiden erstgenannten,
  `_LIST_SPACES_POINTER` an `create_item`/`update_item`, Bulk-Append-Hinweis an
  `append_to_item`, P6.5-G).
- Achtes Tool `get_item_meta(item_id) -> str` (P6.5-E/F) — gleiche Reihenfolge wie `get_item`
  (`_authenticated_principal()` → `acl_of()` → `can_read_item` → `store.get(repair_drift=False)`
  → `compact_json`), `repair_drift=False` bewusst anders als `get_item` (reines Lesen soll nie
  einen Write auslösen, den die Antwort selbst nicht zeigt). `register()`s Rückgabedict um
  `"get_item_meta"` erweitert, Moduldocstring „sieben"→"acht Tools" nachgezogen.
- `storage/store.py :: search()` bekommt `in_body: bool = False` (P6.5-N4) — `item.body` ist
  über `_row_to_item()` ohnehin schon geladen, kein zusätzlicher Datei-Zugriff. `search_items`
  reicht es durch.
- `scripts/mcp_smoke.py` — neuer `get_item_meta`-Check direkt nach `get_item (eigen)`, 13→14.
- `phase2_mcp/tests/test_app.py` — `test_tools_list_returns_seven_tools` → `..._eight_tools`
  (Menge um `get_item_meta` erweitert), `test_all_seven_tools_are_callable_over_http` →
  `..._eight_tools_are_callable_over_http` (echter `get_item_meta`-Aufruf ergänzt, nicht nur
  umbenannt).

**Tests:** 15 neu (6 Beschreibungstests + 4 `get_item_meta` in `test_tools.py`, 2
`in_body`-Durchreichung in `test_tools.py`, 3 `in_body` in `phase1_storage/tests/test_store.py`)
— mehr als der Plan als Minimum nannte (14: A1 6 + A2 4 + A4 4), weil `in_body` sowohl auf
Store- als auch auf Tool-Ebene je einen Default- und einen Positiv-Fall bekam statt nur einen
Durchreichungstest. `pytest` 772→**787**, alle grün (zwei volle Läufe, kein Flake diesmal).
`mcp_smoke.py` 14/14 grün. Charakterisierungstests (P6-D/P6.5-U) vor und nach byte-identisch
grün. Tabu-Diff (`permissions.py`/`server.py`/`asgi.py`/`phase4_auth/**`/`index.py`/
`webui/security.py`/`webui/static/**`) leer.

**`_description_of()`-Testhelfer, V63 geschlossen:** gegen das reale `fastmcp==3.4.4` geprüft
statt angenommen — `mcp._tool_manager` existiert auf der öffentlichen `FastMCP`-Klasse nicht
mehr; der einzige Weg an eine Tool-Beschreibung ist das (async) `await mcp.get_tool(name)` →
`FunctionTool.description`. Anders als der Rest der Suite (die die zurückgegebenen Python-
Funktionen direkt aufruft/über `inspect.signature()` prüft) baut dieser eine Testblock deshalb
eine zweite, unregistrierte `FastMCP`-Instanz (`described_mcp`-Fixture) nur für die
Beschreibungs-Assertions.

**Verifiziert:** `pytest` 787/787 (zwei Läufe), `mcp_smoke.py` 14/14, `git diff` auf den Tabu-
Pfaden leer, Charakterisierung byte-identisch. Nicht verifiziert (bewusst, Gate A→B): eine echte
Connector-Probe durch den Nikinger — Block A ist gebaut, aber **nicht deployt**.

**Offen für die nächste Session:**
- Commit + Push (Nikinger-Freigabe ausstehend zum Zeitpunkt des Schreibens).
- Gate A→B: echte Connector-Probe durch den Nikinger, bevor Block A deployt wird — ein Deploy,
  das Beschreibungsfehler und den ersten Binärdatenpfad (Block B) bündelt, macht jede
  Fehlersuche danach zweideutig (Plan §3, Gate-Absatz).
- Block B Step B1 (Storage-Fundament, Bilder) kann parallel gebaut werden — P6.5-T ist
  angekündigt, keine Abhängigkeit von Block A.
- Bekannte Doku-Schuld (`phase6_shares/CLAUDE.md` Block-C-Text stale, near Softcap) und der
  `test_authctl.py`-Flake bleiben wie im vorherigen Block vermerkt, unverändert offen.

## Session stopped — 2026-08-20 (Step 0 gestartet)

**Herkunft:** Nikinger bat um eine Opus-Planungssession für die zwei tatsächlich noch offenen
QoS-Punkte (Werkzeug-Ergonomie-Rest, Block C Bilder) — der ursprüngliche Auftragstext listete
daneben drei Dinge als „zwingend", die bereits gebaut waren (`patch_item`, das neue Dateisystem,
Update-Banner); vor dem Start korrigiert, siehe Claude-Code-Session-Transkript. Ergebnis:
`docs/concepts/phase6_5_tools_images_plan.md` (Opus, Hintergrund, ~882s), sechs offene Fragen
N1–N6 (kein `AskUserQuestion` im Subagenten verfügbar).

**Nikinger-Entscheidungen (`AskUserQuestion`, live in der Claude-Code-Session), in Plan §0.0
gelockt:**
- **N1:** Phase **6.5**, nicht 7/8 — sitzt zwischen der gebauten Phase 6 und der reservierten
  Phase 7 (Space-Admin-UI). Keine Kollision mit `app.html`s „kommt in Phase 7"-Zeichenkette, die
  bleibt unangetastet.
- **N2:** Verzeichnis `phase6_5_tools_images/` (dieses hier).
- **N3:** Bulk-Append **nicht** bauen — Befund: heute schon über mehrzeiligen Text in einem
  `append_to_item`-Aufruf möglich, nur ein Beschreibungssatz nötig.
- **N4:** Body-Volltextsuche für die MCP-Fläche **als Opt-in** bauen (`in_body: bool = False`) —
  `Store.search()` lädt jede Datei ohnehin vollständig, kostet nichts zusätzlich. Q1 (Web-UI,
  keine Body-Suche) bleibt unangetastet.
- **N5 (=B5):** Bild entfernen per **Verschieben** nach `_assets/<item_id>/_trash/`, Entscheidung H
  bleibt formal unangetastet. **Nikinger-Vormerkung, kein Auftrag dieser Phase:** `_trash/` wird
  nie automatisch geräumt — anders als kB-große `.md`-Dateien können MB-große Bilder Git-Historie/
  `DATA_ROOT` über Zeit zu GB-Größen aufwachsen lassen. Braucht mittelfristig eine eigene
  operative Lösung (`diagnose.sh`-Meldung ab Schwelle, oder Operator-Purge-Skript analog zum
  Hard-Delete-Muster aus P1 Entscheidung H).
- **N6:** `MAX_MCP_ASSET_BYTES = 1 MiB` für MCP-Uploads (Web-UI bleibt bei 5 MiB, B2) — Nikinger-
  Begründung: Claude wird über MCP nur selbst erzeugte SVGs oder kleine Screenshots hochladen,
  keine großformatigen Fotos.

**Vier der fünf `IMAGES_PLAN.md`-Fragen (B1–B4) waren bereits vorher entschieden** und in den
Planungsauftrag eingearbeitet: B1 Blobs in Git-Historie ja (mit Größenriegel), B2 5 MiB je Bild
(Web-UI), B3 Bildbytes fremder Items nur bei Schreibrecht **und** nie automatisch — auch nicht bei
eigenen Items, nur auf direkte Anfrage, B4 MCP-Upload erlaubt, aber Ankündigungspflicht bei
**jedem** Aufruf (keine Dauererlaubnis).

**Step 0 heute ausgeführt:**
- `pytest`-Baseline real gemessen (nicht nur aus der Doku übernommen): erster Lauf 771 passed/1
  failed (`phase4_auth/tests/test_authctl.py::test_revoke_kills_the_family`), isoliert grün, auf
  einem zweiten vollen Lauf **772/772 grün** — ein reihenfolgeabhängiger Flake, kein durch diese
  Session verursachter Schaden (keine Codeänderung angefasst). Baseline bestätigt: **772**.
- Fünfte Contract-Öffnung angekündigt (`phase1_storage/CLAUDE.md`, siehe „Geerbte Contracts").
- `phase6_shares/IMAGES_PLAN.md` als nachrangig markiert, V-Register-Übernahme (V59–V62 →
  dieselben Nummern im neuen Plan, kein Duplikat) dort explizit vermerkt.
- `ROADMAP.md`: neue Phase-6.5-Sektion ergänzt.
- `docs/INDEX.md`: Eintrag von „Next phase" auf den jetzt existierenden Phase-Head umgestellt.
- `app.html` Z. 281 **nicht** angefasst (N1-Ergebnis macht das unnötig, gegen den echten Code
  verifiziert).

**Offen für die nächste Session:**
- Diesen Session-stopped-Block + `docs/INDEX.md`/`ROADMAP.md` committen (Nikinger-Freigabe
  ausstehend zum Zeitpunkt des Schreibens).
- Step 0 Rest: keiner — alle acht Punkte des Plans sind entweder erledigt oder als „keine Aktion
  nötig" verifiziert (N1/`app.html`).
- Block A (Steps A1–A4) kann direkt beginnen — keine Abhängigkeit von Block B.
- Block B Step B1 (Storage-Fundament) kann beginnen — P6.5-T ist angekündigt.
- **Bekannte Doku-Schuld, nicht in diesem Step behoben:** `phase6_shares/CLAUDE.md` nennt Block C
  weiterhin als „geplant, nicht gebaut (`IMAGES_PLAN.md`, fünf offene B1–B5)" — stale seit der
  heutigen Nachrangig-Markierung von `IMAGES_PLAN.md`. Der Head liegt bei ~40.863 Bytes, ~100
  unter dem Softcap — eine Korrektur dort braucht zuerst eine Rotation
  (`scripts/rotate_session_block.sh`), bewusst nicht in diesem Docs-Commit mitgemacht, um zwei
  unabhängige mechanische Vorgänge nicht zu vermischen. Vor der nächsten Änderung an diesem Head
  einplanen.
- **Bekannter Flake, nicht Scope dieser Phase:** `phase4_auth/tests/test_authctl.py::
  test_revoke_kills_the_family` schlug im ersten vollen `pytest`-Lauf dieser Session fehl,
  isoliert und im Re-Run grün — reihenfolgeabhängig. Vermerkt in `phase4_auth/CLAUDE.md`, damit
  ein künftiges „Subtask nicht grün" nicht neu diagnostiziert werden muss.

