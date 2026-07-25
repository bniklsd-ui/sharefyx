---
status: live
purpose: Phase-Head MCP-Server — Scope, harte Regeln, gelockte Entscheidungen, Modulstatus, aktueller Session-Handover
read-when: Arbeiten in phase2_mcp/ — zuerst lesen, zusammen mit dem neuesten Session-stopped-Block
detail: L2
up: ../CLAUDE.md
down:
  - ../docs/concepts/phase2_mcp_plan.md          # voller Plan, Entscheidungen P2-A–P2-N, Steps 0–7
  - ../docs/concepts/PHASE1_CLOSEOUT_HANDOVER.md # Herkunft der Entscheidungen D1–D6
  - SESSIONS_ARCHIVE.md                          # ältere Session-Blöcke (noch leer)
updated: 2026-07-25
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
| 6 | `server.py`, `app.py`, `scripts/serve.py` | 5 | ⬜ | — |
| 7 | `tools.py` (die sechs Tools) | 6 | ⬜ | — |
| 8 | `scripts/mcp_smoke.py`, Runbook, Größenmessung | 7 | ⬜ | — |

**Gesamt: 23 Tests** in `phase2_mcp/tests/` (3 `test_config.py` + 6 `test_credentials.py` + 4
`test_auth.py` + 3 `test_permissions.py` + 1 `test_logging.py` + 2 `test_context.py` + 4
`test_asgi.py`). Acht weitere Tests aus Step 2 liegen in `phase1_storage/tests/` (siehe
Modul-Status Zeile 3 und `phase1_storage/CLAUDE.md`), werden dort mitgezählt, nicht hier.

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

## Session stopped — 2026-07-25 (Step 4: Auth, Rechte, Request-Kontext)

**Ergebnis:** `auth.py` (`Principal` frozen dataclass mit gekürztem `__repr__`,
`AuthError`, `SpaceResolver`-Protokoll, `KeyringTokenResolver` mit injiziertem `load_map`,
Dict-Lookup über `sha256(credential)`), `permissions.py` (`Permissions`-Protokoll,
`OwnSpaceWritable`), `logging_setup.py` (`configure_logging()`, `TokenScrubbingFilter` —
ersetzt `/mcp/<segment>` durch `/mcp/<redacted>` in Message **und** Args), `context.py` +
`asgi.py` (`TokenPathASGI`, Details siehe **wichtiger Fund** unten).

**V3 aufgelöst:** `fastmcp.server.dependencies.get_http_request` importiert sauber gegen das
echte `fastmcp==3.4.4` — der im Plan dokumentierte Importpfad stimmt, `fastmcp.dependencies.
CurrentRequest()` ist eine andere (Dependency-Injection-)API für denselben Zweck, nicht die
hier gebrauchte direkte Funktion.

**Wichtiger Fund (empirisch, nicht nur gelesen) — §2.4 ist an einer Stelle nicht umsetzbar wie
geschrieben:** Der Plan beschreibt `assert_principal_matches_request()` als „zieht das
Token-Segment aus dessen Pfad". Das geht nicht: `TokenPathASGI` muss das Token-Segment aus dem
Pfad entfernen, **bevor** es an die innere FastMCP-App delegiert (sonst sieht FastMCPs eigenes
Routing das Segment als Teil des MCP-Pfads und die Anfrage schlägt fehl). Ein Tool, das während
seiner Ausführung `get_http_request().url.path` liest, sieht deshalb nur noch den bereinigten
Pfad.

Zwei ASGI-Mounting-Techniken gegen ein echtes `fastmcp==3.4.4` + `starlette`-Setup
(`httpx.ASGITransport`/`starlette.testclient.TestClient`) durchprobiert:
1. **`root_path`-Akkumulation** (Starlettes eigene Technik, `scope["path"]` bleibt unverändert,
   nur `root_path` wächst) — scheitert an `redirect_slashes`: ein Credential-Segment ohne
   nachfolgenden Pfad lässt `route_path` leer statt `"/"` werden, Starlette antwortet mit 307
   auf eine URL mit angehängtem `/`, bevor die innere App je läuft.
2. **Direkte `path`/`raw_path`-Kürzung** (Plan-Wortlaut) — funktioniert für das Routing
   (kein Redirect, Tool wird aufgerufen), aber `get_http_request().url.path` liefert dann
   nachweislich `"/mcp/"`, nicht das Token — bestätigt das Problem oben empirisch, nicht nur
   theoretisch.

**Lösung:** `TokenPathASGI` hinterlegt `token_hash` in `scope["state"]`, **bevor** es den Pfad
kürzt (Technik 2 bleibt fürs Routing). `scope["state"]` überlebt die Weiterleitung unverändert —
Starlettes offizieller Mechanismus, um Zustand über eine ASGI-Kette hinweg mitzugeben, per
Testprobe bestätigt: `request.state.token_hash` kam im Tool korrekt an. Die
Sicherheitseigenschaft ist identisch zur Plan-Absicht: der Guard vergleicht „was hat unsere
eigene ASGI-Schicht für DIESEN Request aufgelöst" (`scope["state"]["token_hash"]`, gesetzt von
`TokenPathASGI`) gegen „was liefert `get_http_request()` gerade zurück" (`current_principal()`
aus dem ContextVar) und schlägt bei jeder Abweichung laut fehl (`AuthError`) — nicht mehr über
den Pfad, aber mit derselben Garantie. Vollständige Begründung im Docstring von `context.py`.
**Kein Test dafür in Step 4** (braucht einen echten laufenden Request-Kontext) — end-to-end
geprüft in Step 5 über `test_app.py::test_principal_isolation_under_concurrency`.

**Verifiziert (live):** 14 neue Tests (`test_auth.py` ×4, `test_permissions.py` ×3,
`test_logging.py` ×1, `test_context.py` ×2 — nicht im Plan gefordert, aber `current_principal`/
`set_principal`/`reset_principal` sind eigenständige, netzunabhängige Logik —,
`test_asgi.py` ×4 gegen einen Fake-Resolver + Fake-Innen-App, keine echte FastMCP-App nötig für
diese Schicht). `pytest -v` → **99/99 grün** (76 P1 + 23 P2). `test_principal_reset_after_request`
bestätigt: nach dem Request wirft `current_principal()` wieder `AuthError` — kein Leck zwischen
Requests.

**Anmerkung des Advisors, hier festgehalten statt in Step 6 neu zu entdecken:** P2-N sagt
„`AuthError` → HTTP 401, nie ein Tool-Fehler". Der Guard läuft aber *innerhalb* eines
Tool-Aufrufs (§3.3 Schritt 2) — das 401-Fenster ist zu diesem Zeitpunkt vorbei, ein
Guard-`AuthError` muss also zwangsläufig als Tool-Fehler auftauchen. Das ist kein Defekt (immer
noch fail-closed, keine fremden Daten), aber `map_storage_error()` in Step 6 muss diese
Abbildung bewusst treffen, nicht zufällig.

**Nächster Schritt (konkret):** Step 5 — `server.py`, `app.py`, `scripts/serve.py`. Das ist die
Stelle, an der `TokenPathASGI` erstmals gegen eine echte FastMCP-App läuft — V4 (`Mount`-
Verhalten) und der `assert_principal_matches_request()`-Guard werden dort erstmals end-to-end
statt isoliert geprüft.
