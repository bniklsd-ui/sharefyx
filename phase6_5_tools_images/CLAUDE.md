---
status: live
purpose: Phase-Head Werkzeug-Ergonomie + Bilder — Scope, harte Regeln, Modulstatus, aktueller Session-Handover
read-when: Arbeiten in phase6_5_tools_images/ oder an den in §2 des Plans genannten Dateien in mcpserver/storage/webui — zuerst lesen, zusammen mit dem neuesten Session-stopped-Block
detail: L2
up: ../CLAUDE.md
down:
  - ../docs/concepts/phase6_5_tools_images_plan.md   # voller Plan, Entscheidungen P6.5-A–P6.5-V, §0.0 gelockte N1–N6, Steps 0/A/B
  - ../phase6_shares/IMAGES_PLAN.md                  # Vorgänger-Zusatzplan, nachrangig seit 2026-08-20
  - SESSIONS_ARCHIVE.md                              # ältere Session-Blöcke, newest-first
updated: 2026-08-20 (Block A gebaut: achtes Tool get_item_meta, Beschreibungskorrekturen, search in_body=, 787 pytest gruen, mcp_smoke.py 14/14, Tabu-Diff leer, noch nicht deployt)
---
# CLAUDE.md — Phase 6.5: Werkzeug-Ergonomie und Bilder (`phase6_5_tools_images/`)

> Kein eigenes Python-Paket (wie `phase3_edge/`, `phase6_shares/`) — Servercode bleibt in
> `mcpserver`/`storage`/`webui`. **Quelle der Wahrheit ist der Code, nicht dieses Dokument.**

---

## Mission (zuerst lesen)

Zwei Blöcke: **(A)** eine arbeitende Claude-Instanz findet ihre Werkzeuge, versteht deren
Aufgabenteilung aus der Beschreibung und zahlt keine Tausende Token für eine Versionsnummer.
**(B)** ein Bild liegt im Space, ist im Dokument sichtbar, technisch nur ein Link — und Claude
sieht seine Bytes nur, wenn ein Mensch ausdrücklich danach fragt. Unter Druck fällt Block B weg,
nie Block A (reine Beschreibungs-/Tool-Arbeit ohne Datenformatänderung).

## Scope

- **DRIN:** die fünf offenen MCP-Werkzeug-Ergonomie-Punkte (2026-08-14-Live-Feedback),
  Abschluss Block C Bilder (`storage/`-Fundament, `webui`-Routen, MCP-Asset-Tools).
- **DRAUSSEN:** Bulk-Append-Tool, Body-Volltextsuche in der Web-UI, automatische
  `_trash/`-Räumung, Space-Admin-UI (bleibt Phase 7), Rechteverwaltung über MCP-Tools,
  HEIC/SVG/PDF, serverseitiges Bild-Rendering. Volle Liste: Plan §5 „Explizit draußen".

Details, gelockte Entscheidungen P6.5-A–P6.5-V, Berührungsfläche/Tabu-Dateien, Schritt-Sequenz,
Testliste, Abnahmezeilen: `docs/concepts/phase6_5_tools_images_plan.md`.

## Modul-Status

| Block | Inhalt | Status |
|---|---|---|
| Step 0 | Haushalt/Ankündigungen | ✅ |
| Block A (Steps A1/A2/A4; A3 bewusst nicht gebaut, N3) | Werkzeug-Ergonomie (`mcpserver/tools.py`, `storage/store.py :: search(in_body=)`) | ✅ **gebaut**, noch nicht deployt — Gate A→B (echte Connector-Probe) steht aus |
| Block B (Steps B1–B5) | Bilder (`storage/`, `webui/`, MCP-Asset-Tools) | ⏳ nicht begonnen |

## Geerbte Contracts

Fünfte, benannte Öffnung des P1-Contracts (`storage/{files,store,models}.py`) — angekündigt
2026-08-20 in `phase1_storage/CLAUDE.md` unter „Geerbte Contracts", **vor** jedem Step-B1-Code
(P6.5-T). Details dort, nicht hier dupliziert.

---

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
