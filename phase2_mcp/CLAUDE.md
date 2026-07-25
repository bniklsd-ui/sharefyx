---
status: live
purpose: Phase-Head MCP-Server — Scope, harte Regeln, gelockte Entscheidungen, Modulstatus, aktueller Session-Handover
read-when: Arbeiten in phase2_mcp/ — zuerst lesen, zusammen mit dem neuesten Session-stopped-Block
detail: L2
up: ../CLAUDE.md
down:
  - ../docs/concepts/phase2_mcp_plan.md          # voller Plan, Entscheidungen P2-A–P2-N, Steps 0–7
  - ../docs/concepts/PHASE1_CLOSEOUT_HANDOVER.md # Herkunft der Entscheidungen D1–D6
  - SESSIONS_ARCHIVE.md                          # ältere Session-Blöcke, newest-first
updated: 2026-07-26 (Step 6)
---
# CLAUDE.md — Phase 2: MCP-Server (`phase2_mcp/`)

> **Claude kann lesen und schreiben — lokal, ohne Tunnel.** Ein dünner Adapter über dem in P1
> bewiesenen Storage-Kern: Transport (Streamable HTTP), Identität (Token → Space), Autorisierung
> (eigener Space schreibbar, fremde read-only).
> **Quelle der Wahrheit ist der Code, nicht dieses Dokument.**
> Vollständiges Design + alle 14 gelockten Entscheidungen (P2-A–P2-N) + Steps 0–7:
> `../docs/concepts/phase2_mcp_plan.md`.

## Mission (zuerst lesen)

Der eigentliche Härtetest der Phase ist nicht MCP, sondern **Rule 4**: ein Codepfad, über den
ein fremder Space beschrieben werden kann, existiert nach dieser Phase nicht — auch nicht
versehentlich, auch nicht über `get()`. Zwei gleichzeitige Requests mit zwei verschiedenen
Tokens müssen zwei verschiedene Spaces sehen; wenn dieser Test fällt, ist es ein
Cross-Space-Leak, kein Testproblem.

## Bauprinzip (Projekt-Kernprinzip)

„Der Server ist dumm." **Phase 2 enthält KEINE AI.** Die Tools reichen Store-Ergebnisse durch,
formatieren sie token-sparsam und entscheiden über Rechte. Mehr nicht. Wer hier ein LLM
einbauen will → **stop**.

## Scope

- **DRIN:** `fastmcp` über Streamable HTTP `[VERIFY]`, Token→Space-Auflösung, sechs Tools
  (`list_spaces`, `search_items`, `get_item`, `create_item`, `update_item`, `append_to_item`),
  `<untrusted_content>`-Wrapping fremder Bodies + Snippets, Token-Budget-Disziplin im Listing,
  `/health`.
- **DRAUSSEN:** Löschen (`status: archived` reicht), MCP Resources, MCP Prompts, OAuth,
  öffentliche Erreichbarkeit/Tunnel (P3), SQL-Filterung in `Store.search()` (D6, zurückgestellt).

## Harte Regeln (nicht verhandelbar)

- Alle Hard Rules aus Root-`CLAUDE.md` gelten unverändert — insbesondere: kein Secret in einer
  Datei (Tokens nur als sha256-Hash im Keyring, Service `nikinger-space`), kein Last-Write-Wins,
  kein offener Port am Router, Logging → stderr, stdout nur maschinenlesbares JSON.
- **Rule 4 ist architektonisch, nicht per `if`.** `create_item`/`update_item`/`append_to_item`
  haben keinen `space`-Parameter; der Ziel-Space ist immer der des Principals (P2-G).
- **Auth fail-closed.** Kein/unbekanntes Token → HTTP 401 ohne Detail, nie ein Tool-Fehler, nie
  unterscheidbar von „falsches Token" (P2-N).
- **`stateless_http=True` ab Tag 1** — Sicherheitsbedingung, keine Skalierungsoption (P2-B, §8
  Risiko 1).
- **Token nie im Log.** Uvicorn-Access-Log aus, Scrubbing-Filter auf jedem verbleibenden Logger.
- **Rotationsregel ab Tag 1.** Dieser Head trägt **genau einen** Session-Block. Beim Anlegen
  eines neuen wandert der bisherige **verbatim** nach `SESSIONS_ARCHIVE.md`, newest-first —
  Durchführung über `scripts/rotate_session_block.sh phase2_mcp`, nie von Hand.
- **Commit ⇒ Note-Update, im selben Commit** (Hard Rule 8): Modul-Tabelle unten + Session-Block.

## Die 14 Entscheidungen (P2-A – P2-N) — Kurzform (Details: Plan §0.4)

Bibliothek `fastmcp>=3.4,<3.5` (A) · Protokoll 2025-11-25, `stateless_http=True` (B) · Starlette-
Wurzel mit `Mount("/mcp")` (C) · Token im Pfad, Auflösung einmal pro Request (D) · Keyring
speichert nur Hashes (E) · `SpaceResolver`/`Permissions` getrennte Seams, beliebig viele Spaces
(F) · Schreib-Tools ohne `space`-Parameter (G) · `<untrusted_content>` mit Escaping (H) ·
kompaktes JSON / Dateitext als Ergebnisformate (I) · Token-Budget `limit=20`/`max=100` (J) ·
Archivieren nur über `update_item(status="archived")`, kein siebtes Tool (K) · drei einmalige
P1-Contract-Erweiterungen (L, Step 2) · OAuth bleibt hinter P3, Seam wird gebaut (M) ·
Fehlerabbildung mit handlungsfähigem Text (N).

## Modul-Status

| # | Modul | Step | Status | Tests |
|---|---|---|---|---|
| 1 | Haushalt, Verifikationsdurchlauf, Rotationsregel operationalisiert | 0 | ✅ | 0 (kein Feature-Code) |
| 2 | Paketgerüst `phase2_mcp/`, `mcpserver/config.py` | 1 | ✅ | 3 |
| 3 | P1-Contract-Erweiterungen (`space_of`, `repair_drift`, Statusvalidierung) | 2 | ✅ | 8 (in `phase1_storage/tests/`) |
| 4 | `credentials.py`, `scripts/issue_token.py` | 3 | ✅ (echter Keyring-Roundtrip vom Nikinger bestätigt) | 6 |
| 5 | `auth.py`, `permissions.py`, `context.py`, `asgi.py`, `logging_setup.py` | 4 | ✅ | 14 |
| 6 | `server.py`, `app.py`, `scripts/serve.py` | 5 | ✅ | 8 (`test_app.py`) |
| 7 | `tools.py` (die sechs Tools) | 6 | ✅ | 22 (`test_tools.py`) |
| 8 | `scripts/mcp_smoke.py`, Runbook, Größenmessung | 7 | ⬜ | — |

**Zeile 7, Step 6 abgeschlossen:** `search_items`, `get_item`, `create_item`, `update_item`,
`append_to_item` lösen ihre seit Step 5 bestehenden `NotImplementedError`-Platzhalter ein
(§3.2/§3.4/§3.5/§3.6) — `list_spaces` war seit Step 5 bereits fertig. Zeile 6 (`test_app.py`)
wuchs um einen sechsten Test (`test_all_six_tools_are_callable_over_http`), der Step 6s eigenes
Done-when „alle sechs Tools über den ASGI-Testclient aufrufbar" gegen den echten Stack aus
Step 5 beweist — `test_tools.py` allein kann das nicht, weil dort der Guard gemockt ist (siehe
Session-Block).

**Gesamt: 53 Tests** in `phase2_mcp/tests/` (3 `test_config.py` + 6 `test_credentials.py` + 4
`test_auth.py` + 3 `test_permissions.py` + 1 `test_logging.py` + 2 `test_context.py` + 4
`test_asgi.py` + 8 `test_app.py` + 22 `test_tools.py`). Acht weitere Tests aus Step 2 liegen in
`phase1_storage/tests/` (siehe Modul-Status Zeile 3 und `phase1_storage/CLAUDE.md`), werden dort
mitgezählt, nicht hier.

## Geerbte Contracts

Aus P1 (`phase1_storage/CLAUDE.md`, `docs/concepts/phase1_storage_plan.md` §1/§2): Frontmatter-
Schema, `Item`/`SpaceInfo`/`ItemSummary`/`SearchResult`/`IndexStats`, `Store`-Signaturen
(`list_spaces`/`search`/`get`/`create`/`update`/`append`/`archive`/`rebuild_index`),
Fehlertypen inkl. `ConflictError.current`. **[2026-07-25, Step 2 abgeschlossen]** Drei
einmalige, vom Nikinger freigegebene Erweiterungen sind eingebracht (`space_of()`,
`get(..., repair_drift=)`, Statusvalidierung über `models.STATUS_VALUES`) — Details, Tests und
Begründung stehen in `phase1_storage/CLAUDE.md` unter „Geerbte Contracts" (dort, nicht doppelt
hier, da Code-nah). **Der Contract ist ab jetzt wieder zu.**

**D1, festgehalten statt stillschweigend übernommen:** `docs/concepts/PHASE1_CLOSEOUT_HANDOVER.md`
verlangte ausdrücklich Gegenprüfung von `ItemSummary` und `SpaceInfo.name`/`.item_count` (beides
Claude-Code-Eigenentscheidungen aus P1, im P1-Plan nicht spezifiziert), bevor P2 darauf aufbaut.
Der P2-Plan (`docs/concepts/phase2_mcp_plan.md` §0.2) übernimmt beide bereits als „gegeben" —
das zählt als Bestätigung durch die Browser-Planungssession mit dem Nikinger. Hier trotzdem
explizit vermerkt: **gilt als bestätigt, wenn der Nikinger nicht widerspricht** (siehe
Step-0-Session-Block unten).

**Warum nur Hashes im Keyring** (Plan §2.3, seit Step 3 in `mcpserver/credentials.py` real
umgesetzt): der Server muss ein Token nur *wiedererkennen*, nie *vorzeigen*. `issue()` gibt das
Token genau einmal zurück; ab dann existiert im Keyring nur noch
`{sha256(token): space}`. Wer diese Eigenschaft aufgibt, um „das Token nochmal anzeigen" zu
können, macht aus dem Keyring eine Passwortliste.

**Was der Pfad-Token nicht ist** (Plan §2.3): kein OAuth-Ersatz, kein Schutz gegen Cloudflare
(R4 — Cloudflare sieht bei P3 ohnehin Klartext), gültig bis P3+1. Siehe P2-Plan §0.3 für die
Begründung, warum OAuth trotzdem hinter P3 bleibt statt vorgezogen zu werden.

**`version` in fremden Spaces** (Plan §3.4): `get(..., repair_drift=)` existiert seit Step 2 im
Store; genutzt wird es ab Step 6 (`tools.py :: get_item`, §3.4). Dort ist `version` in fremden
Spaces informativ, nicht autoritativ — es gibt dort per Architektur keine Writes.

---

## Session stopped — 2026-07-26 (Step 6: Die sechs Tools)

**Ergebnis:** `mcpserver/tools.py` fertig — `search_items`, `get_item`, `create_item`,
`update_item`, `append_to_item` lösen ihre `NotImplementedError`-Platzhalter aus Step 5 ein.
Neue Modul-Helfer wie im Plan gefordert: `wrap_untrusted()` (§3.5, Ersatzstring wörtlich aus
dem Plan übernommen), `summary_to_dict()`, `item_to_filetext()` (dupliziert bewusst
`storage.store._item_to_text`s Feldreihenfolge — der P1-Contract ist seit Step 2 „wieder zu",
eine weitere Erweiterung wäre keine „einmalige" mehr), `compact_json()`, `map_storage_error()`
(§3.6, alle sechs Fehlerfälle inkl. `PermissionDenied` als P2-eigenem Typ). `test_tools.py` neu
mit allen 20 im Plan benannten Tests plus zwei zusätzlichen (siehe unten). `test_app.py` bekam
einen siebten … achten Test: `test_all_six_tools_are_callable_over_http`, der Step 6s eigenes
Done-when „alle sechs Tools über den ASGI-Testclient aufrufbar" gegen den echten Stack aus
Step 5 beweist (ein voller Rundlauf: `list_spaces` → `create_item` → `search_items` →
`get_item` eigen/fremd → `append_to_item` → `update_item`-Konflikt → `update_item(status=
archived)`).

**Testdesign-Entscheidung, hier festgehalten statt stillschweigend:** `test_tools.py` mockt
`context.assert_principal_matches_request` auf ein No-op (autouse-Fixture) und ruft die von
`tools.register()` zurückgegebenen rohen Tool-Funktionen direkt auf — `@mcp.tool(...)` gibt die
unveränderte Python-Funktion zurück, nicht ein `FunctionTool`-Objekt (empirisch geprüft, nicht
angenommen: ein `type(foo)` nach der Dekoration ist weiterhin `function`). Begründung: die
komplette HTTP/ASGI/Guard-Kette ist bereits in `test_app.py::test_principal_isolation_under_
concurrency` (Step 5) end-to-end bewiesen; zwanzig Tests bräuchten sonst zwanzigmal eine echte
FastMCP-App. `test_create_item_has_no_space_parameter` prüft deshalb `inspect.signature()`
direkt auf der zurückgegebenen Funktion.

**Echter Fund während der Implementierung, nicht nur ein Advisor-Verdacht bestätigt:** die
Step-4-Advisor-Notiz („`map_storage_error()` in Step 6 muss die `AuthError`-als-Tool-Fehler-
Abbildung bewusst treffen, nicht zufällig") war zunächst NICHT umgesetzt — jeder Tool-Body rief
`context.current_principal()` + `context.assert_principal_matches_request()` direkt auf, außerhalb
jedes `try`/`except`. Ein Guard-`AuthError` wäre also roh durchgefallen statt über
`map_storage_error()` zu laufen. Gefunden im Advisor-Review vor dem Commit, behoben durch
`_authenticated_principal()` (bündelt Schritt 1+2 aus §3.3, fängt `AuthError` und wirft den
gemappten `ToolError`). Regressionstest `test_guard_auth_error_is_mapped_to_tool_error` beweist
es. **Kleinere Selbstkorrektur direkt danach:** ein automatisiertes Suchen/Ersetzen beim Umbau
auf `_authenticated_principal()` hatte dessen eigenen Funktionskörper versehentlich auf sich
selbst umgeschrieben (Endlosrekursion) — vor dem ersten Testlauf bemerkt und korrigiert, aber
festgehalten, weil genau der neue Regressionstest diesen Fehler auch bei einem stillen Commit
gefangen hätte.

**Advisor-Review vor dem Commit, drei weitere Funde, alle behoben:**
1. `test_search_limit_is_clamped_to_max` prüfte nur das im Payload echoete `limit`-Feld gegen
   einem Store mit einem einzigen Item — hätte auch mit einem ungeklemmten Limit bestanden.
   Jetzt >100 Items, Assertion zusätzlich auf `len(payload["items"]) == MAX_LIMIT`.
2. Plan §2.2 nennt `search_items` ausdrücklich als den Pfad, an dem `total`/Paginierung falsch
   werden, sobald `can_read` nicht mehr konstant `True` ist — der `_OwnSpaceOnlyVisible`-Test-
   Double bewies den Seam bisher nur für `list_spaces`. Neuer Test
   `test_search_filters_by_can_read_and_reports_filtered_total` beweist ihn jetzt auch für
   `search_items` (`total` zählt die gefilterte, nicht die rohe Trefferzahl).
3. `test_search_result_size_budget` maß den günstigsten Fall (leere Bodies → leere Snippets).
   Fixture jetzt mit realistischer Body-Länge (volles 160-Zeichen-Snippet) und einer Mischung
   aus eigenem und fremdem Space (Wrap-Overhead fließt ins Budget ein) — Budget hält weiterhin.

**Bekannte, dokumentierte Grenze (kein Bug):** `search_items` holt bis zu `_STORE_FETCH_LIMIT =
5000` Treffer vom Store (der ohnehin jede Datei pro Aufruf scannt, D6), filtert/paginiert
`include_archived`/Rechte/`offset`/`limit` selbst in `tools.py`. Über dieser Grenze würde
`total` still unterzählen — für den Zwei-Personen-Space-Server um Größenordnungen entfernt,
als `[SEAM]`-Kommentar im Code und hier festgehalten statt später neu entdeckt zu werden.

**Verifiziert (live):** 22 Tests in `test_tools.py`, `test_app.py` von 7 auf 8 gewachsen.
`pytest -v` → **129/129 grün** (76 P1 + 53 P2).

**Nächster Schritt (konkret):** Step 7 — `scripts/mcp_smoke.py` (Gegenstück zu `space_cli.py`
aus P1, temporäres `DATA_ROOT`, nie das echte), README-Runbook „Quick-Tunnel-Probe", Größen-
messung im Session-Block. Der Tunnel-Schritt selbst läuft beim Nikinger, nicht in Claude Code
(kein Skript/Config/Hostname wird committet). Danach ist Phase 2 code-complete; die Quick-
Tunnel-Probe (ein Read, ein Write über den echten Claude-Connector) macht sie live-verifiziert.
