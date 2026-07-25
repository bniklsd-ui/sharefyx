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
updated: 2026-07-26
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
| 6 | `server.py`, `app.py`, `scripts/serve.py` | 5 | ✅ | 7 (`test_app.py`) |
| 7 | `tools.py` (die sechs Tools) | 6 | ⬜ (siehe Anmerkung) | — |
| 8 | `scripts/mcp_smoke.py`, Runbook, Größenmessung | 7 | ⬜ | — |

**Anmerkung zu Zeile 7 — kein stiller Contract-Vorgriff:** `mcpserver/tools.py` existiert bereits
seit Step 5, nicht erst seit Step 6. Grund: `server.py :: build_mcp()` registriert die sechs
Tools, und Step 5s eigenes Done-when (`tools/list` liefert sechs Tools mit Annotations,
`test_principal_isolation_under_concurrency`) braucht dafür sowohl alle sechs Registrierungen
(Name/Signatur/Titel/Annotations) als auch **ein** echt funktionierendes Tool. `list_spaces` ist
deshalb bereits vollständig implementiert (Plan §3.2); die übrigen fünf (`search_items`,
`get_item`, `create_item`, `update_item`, `append_to_item`) sind mit finaler Signatur und
Annotations registriert, werfen aber bewusst `NotImplementedError` — ihre Semantik (Wrapping
§3.5, Fehlerabbildung §3.6, Token-Budget P2-J) bleibt Step 6. Zeile 7 wird erst mit Step 6 auf
✅ gehoben.

**Gesamt: 30 Tests** in `phase2_mcp/tests/` (3 `test_config.py` + 6 `test_credentials.py` + 4
`test_auth.py` + 3 `test_permissions.py` + 1 `test_logging.py` + 2 `test_context.py` + 4
`test_asgi.py` + 7 `test_app.py`). Acht weitere Tests aus Step 2 liegen in
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

## Session stopped — 2026-07-26 (Step 5: Server und App)

**Ergebnis:** `server.py` (`build_mcp(store, permissions, *, name=...)`), `app.py`
(`create_app(*, settings, resolver, store, allowed_hosts=None)` — `OwnSpaceWritable()` wird
dort instanziiert, nicht injiziert, per Plan §2.2 Erweiterungspfad), `scripts/serve.py`
(`--allowed-host`, `access_log=False`). `mcpserver/tools.py` musste dafür bereits entstehen
(siehe Modul-Status-Anmerkung Zeile 7 — kein stiller Contract-Vorgriff): `list_spaces` ist
vollständig implementiert, die übrigen fünf Tools sind mit finaler Signatur/Annotations
registriert und werfen `NotImplementedError` bis Step 6.

**Vom Advisor vor Beginn geprüfte Spannung im Plan-Text, aufgelöst statt blind übernommen:**
Step 5s eigenes „Done when" verlangt `tools/list` mit sechs annotierten Tools und einen
Isolationstest mit echtem Tool-Verhalten — Step 5s Dateiliste nennt aber nur
`server.py`/`app.py`/`serve.py`, `tools.py` steht explizit unter Step 6. Auflösung (bestätigt
gegen §1.2 Abhängigkeitstabelle „`server.py` kennt `tools`" und §7-Warnung vor Vorziehen):
`tools.py` wird in Step 5 mit allen sechs Registrierungen angelegt, aber nur so viel echtem
Verhalten wie der Isolationstest braucht (`list_spaces`) — Step 6 bleibt für Wrapping/
Fehlerabbildung/Token-Budget zuständig, keine Vorwegnahme.

**V2 final bestätigt (nicht nur `[VERIFY]` übernommen):** `fastmcp==3.4.4`,
`FastMCP.http_app(path=…, stateless_http=…, allowed_hosts=…, …)` — Signatur exakt wie geplant,
per `inspect.signature` gegen das echte Paket geprüft, nicht nur gelesen.

**V4 aufgelöst, empirisch gegen eine echte FastMCP-App, nicht nur gegen den Fake-Innen-App aus
Step 4:** die in `asgi.py` (Step 4) implementierte Pfad-Arithmetik (`route_path =
path[len(root_path):]`, `new_path = root_path + "/" + rest if rest else root_path + "/"`)
funktioniert unverändert, wenn `TokenPathASGI` zusätzlich hinter einem echten
`Mount("/mcp", …)` sitzt. Grund, empirisch nachvollzogen: Starlettes `Mount.matches()` ändert
`scope["path"]` **nicht** — nur `scope["root_path"]` wächst um den Mount-Präfix (`""` → `"/mcp"`).
Für den Normalfall `POST /mcp/<token>` (kein weiteres Pfadsegment) liefert die Arithmetik
`rest=""` und damit `new_path = "/mcp/"` — genau der `route_path == "/"`, den die innere
FastMCP-App erwartet (erzeugt mit `path="/"`). Verifiziert per Wegwerfskript gegen ein echtes
`FastMCP`+`Starlette`-Setup (kein Fake): `GET /health` → 200, `POST /mcp/<gültiges-token>` mit
einer echten `initialize`-Anfrage → 200 mit korrekter MCP-Antwort, `POST /mcp/<unbekannt>` →
401 leer. Keine Code-Änderung an `asgi.py`/`context.py` nötig — Step 4s Lösung trägt durch den
echten Mount hindurch.

**Isolationstest (`test_app.py::test_principal_isolation_under_concurrency`) — die wichtigste
Zusicherung der Phase, jetzt grün gegen eine echte, laufende FastMCP-App:** zehn `list_spaces`-
Aufrufe über `asyncio.gather`, alternierend zwei Tokens (`alpha`/`beta`, Fixture-Namen statt
Nikinger/Kollege — Plan §2.2), echte Nebenläufigkeit auf einem Event-Loop (nicht sequenziell).
Jeder Aufruf sieht `writable=true` exakt für den eigenen und `writable=false` für den fremden
Space — kein Cross-Space-Leak. Technischer Unterbau: `httpx.ASGITransport` (kein echter Port,
kein Netz) + `fastmcp.Client`/`StreamableHttpTransport` mit injiziertem
`httpx_client_factory`; Lifespan manuell über `app.router.lifespan_context(app)` statt
simulierter ASGI-Lifespan-Nachrichten — Starlettes eigener Mechanismus, ohne
Zusatzabhängigkeit (`asgi-lifespan` ist nicht installiert und wurde bewusst nicht ergänzt).

**Advisor-Review vor dem Commit — ein Fund korrigiert, einer verschärft:**
1. `test_mcp_requires_token` deckte `POST /mcp/` (leeres Credential → unser 401) und
   `POST /mcp/<unbekannt>` ab, aber nicht `POST /mcp` **ohne** Trailing-Slash. Empirisch geprüft:
   das trifft Starlettes eigenes `redirect_slashes` **vor** `TokenPathASGI` und antwortet mit
   **307** nach `/mcp/`, leerer Body, `Location`-Header ohne Space-/Pfad-/Tokendaten.
   Kein Verstoß gegen P2-N (das 307 sagt nichts über Tokengültigkeit — in diesem Request gibt es
   noch gar kein Token-Segment), aber eine dritte, von außen unterscheidbare Antwortform, die
   sonst erst bei der Live-Tunnel-Probe aufgefallen wäre. Jetzt eigener Test:
   `test_mcp_bare_mount_redirects_without_leaking`.
2. `test_health_leaks_no_space_names` prüfte nur auf Teilstrings (`"alpha" not in body_text`)
   gegen eine Antwort, die strukturell gar keine Space-Daten enthalten kann — vacuous. `test_health_ok`
   prüft jetzt zusätzlich die exakte Schlüsselmenge (`{"status","service","version"}`), das
   fängt eine spätere Feldergänzung ab, nicht nur zufällig gewählte Fixture-Namen.

**Verifiziert (live):** 7 Tests in `test_app.py` — `test_health_ok`,
`test_health_leaks_no_space_names`, `test_mcp_requires_token`,
`test_mcp_bare_mount_redirects_without_leaking`, `test_tools_list_returns_six_tools`,
`test_tools_list_annotations_present`, `test_principal_isolation_under_concurrency`.
`pytest -v` → **106/106 grün** (76 P1 + 30 P2).

**Nächster Schritt (konkret):** Step 6 — `mcpserver/tools.py` fertigstellen: `search_items`,
`get_item`, `create_item`, `update_item`, `append_to_item` (§3.2/§3.4), `<untrusted_content>`-
Wrapping + Escaping (§3.5), Fehlerabbildung inkl. des in Step 4 vermerkten
`AuthError`-als-Tool-Fehler-Falls (§3.6), Token-Budget-Klemmung (`DEFAULT_LIMIT`/`MAX_LIMIT`,
bereits als Modulkonstanten in `tools.py` vorhanden). `test_tools.py` neu, `list_spaces`
braucht dort keine erneute Grundimplementierung, nur ggf. Härtung/Formatkonsistenz mit den
anderen fünf Tools.
