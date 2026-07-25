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
| 3 | P1-Contract-Erweiterungen (`space_of`, `repair_drift`, Statusvalidierung) | 2 | ⬜ | — |
| 4 | `credentials.py`, `scripts/issue_token.py` | 3 | ⬜ | — |
| 5 | `auth.py`, `permissions.py`, `context.py`, `asgi.py`, `logging_setup.py` | 4 | ⬜ | — |
| 6 | `server.py`, `app.py`, `scripts/serve.py` | 5 | ⬜ | — |
| 7 | `tools.py` (die sechs Tools) | 6 | ⬜ | — |
| 8 | `scripts/mcp_smoke.py`, Runbook, Größenmessung | 7 | ⬜ | — |

**Gesamt: 3 Tests** (`test_config.py`). Step 2 (P1-Erweiterungen) fügt acht weitere Tests in
`phase1_storage/tests/` hinzu, nicht hier — dieser Head zählt nur `phase2_mcp/tests/`.

## Geerbte Contracts

Aus P1 (`phase1_storage/CLAUDE.md`, `docs/concepts/phase1_storage_plan.md` §1/§2): Frontmatter-
Schema, `Item`/`SpaceInfo`/`ItemSummary`/`SearchResult`/`IndexStats`, `Store`-Signaturen
(`list_spaces`/`search`/`get`/`create`/`update`/`append`/`archive`/`rebuild_index`),
Fehlertypen inkl. `ConflictError.current`. Drei einmalige, vom Nikinger freigegebene
Erweiterungen kommen in Step 2 dieser Phase (`space_of()`, `get(..., repair_drift=)`,
Statusvalidierung) — danach ist der Contract wieder zu.

**D1, festgehalten statt stillschweigend übernommen:** `docs/concepts/PHASE1_CLOSEOUT_HANDOVER.md`
verlangte ausdrücklich Gegenprüfung von `ItemSummary` und `SpaceInfo.name`/`.item_count` (beides
Claude-Code-Eigenentscheidungen aus P1, im P1-Plan nicht spezifiziert), bevor P2 darauf aufbaut.
Der P2-Plan (`docs/concepts/phase2_mcp_plan.md` §0.2) übernimmt beide bereits als „gegeben" —
das zählt als Bestätigung durch die Browser-Planungssession mit dem Nikinger. Hier trotzdem
explizit vermerkt: **gilt als bestätigt, wenn der Nikinger nicht widerspricht** (siehe
Step-0-Session-Block unten).

**Warum nur Hashes im Keyring** (vorgezogen aus Plan §2.3, wird in Step 3 mit Code belegt): der
Server muss ein Token nur *wiedererkennen*, nie *vorzeigen*. Wer diese Eigenschaft aufgibt, um
„das Token nochmal anzeigen" zu können, macht aus dem Keyring eine Passwortliste.

**Was der Pfad-Token nicht ist** (vorgezogen aus Plan §2.3): kein OAuth-Ersatz, kein Schutz
gegen Cloudflare (R4 — Cloudflare sieht bei P3 ohnehin Klartext), gültig bis P3+1. Siehe
P2-Plan §0.3 für die Begründung, warum OAuth trotzdem hinter P3 bleibt statt vorgezogen zu
werden.

**`version` in fremden Spaces** (vorgezogen aus Plan §3.4, wird in Step 3 wirksam): sobald
`get(..., repair_drift=)` existiert, ist `version` in fremden Spaces informativ, nicht
autoritativ — dort gibt es per Architektur keine Writes.

---

## Session stopped — 2026-07-25 (Step 1: Paketgerüst)

**Ergebnis:** `phase2_mcp/pyproject.toml` (Paket `mcpserver`, spiegelt
`phase1_storage/pyproject.toml` exakt bis auf Name/Description/Dependencies —
`dependencies = ["storage", "fastmcp>=3.4,<3.5", "keyring>=25"]`,
`dev = ["pytest", "pytest-asyncio", "httpx"]`), `mcpserver/__init__.py`
(`__version__ = "0.1.0"`), `mcpserver/config.py` (`Settings`-Dataclass `frozen, kw_only`:
`data_root: Path` Pflicht ohne Default, `host="127.0.0.1"`, `port=8765`, `log_level="INFO"`;
`load_settings(env)` liest `SPACE_DATA_ROOT`/`SPACE_HOST`/`SPACE_PORT`/`SPACE_LOG_LEVEL`, wirft
`ValueError` bei fehlendem `SPACE_DATA_ROOT` oder nicht-parsbarem `SPACE_PORT`). Kein Secret in
`Settings` — `config.py` kennt laut Modulübersicht „nichts", importiert entsprechend nur
Standardbibliothek.

**Drift gegenüber dem Plan, dated:** Plan §4 Step 1 nennt `tests/__init__.py` als Datei. P1 hat
in `phase1_storage/tests/` nie ein `__init__.py`, sondern ein leeres `conftest.py` als
Platzhalter (Step 0 des P1-Plans). Hier aus Konsistenzgründen mit dem bereits etablierten
Repo-Vorbild identisch gehalten: `phase2_mcp/tests/conftest.py` (leer) statt `__init__.py`.
Funktional gleichwertig für `pytest`-Discovery.

**Notwendige Ergänzung, die der Plan nicht auflistete:** `pytest.ini` (`testpaths =
phase1_storage/tests`) hätte `phase2_mcp/tests/` nie gefunden. Erweitert auf
`testpaths = phase1_storage/tests phase2_mcp/tests` — sonst wären alle P2-Tests ab hier
unsichtbar für `pytest` gewesen, ohne dass ein Fehler das angezeigt hätte.

**Verifiziert (live):** `./scripts/dev_install.sh` fand `phase2_mcp/` automatisch über den
`phase*_*/`-Glob (keine Änderung am Skript nötig, wie im Plan erwartet), installierte `storage`
und `mcpserver` editable, zog `fastmcp==3.4.4` (exakt die in Step 0 als aktuellste 3.4.x-Version
verifizierte) und `keyring==25.7.0` echt aus PyPI. `from mcpserver import __version__` →
`"0.1.0"`. `pytest -v` → **71/71 grün** (68 aus P1 + 3 neue in `test_config.py`:
`test_load_settings_requires_data_root`, `test_load_settings_defaults`,
`test_load_settings_port_invalid_raises`).

**V5 (Keyring-Backend) weiter aufgelöst, noch nicht endgültig:** `keyring --list-backends` nach
echter Installation zeigt `keyring.backends.SecretService.Keyring` mit Priorität 5 (höchste) —
das in Step 0 vermutete Backend ist real verfügbar, nicht nur plausibel. Endgültig verifiziert
ist V5 erst, wenn Step 3 tatsächlich einen Wert schreibt und zurückliest (`credentials.py`
existiert noch nicht).

**Nächster Schritt (konkret):** Step 2 — die drei freigegebenen P1-Contract-Erweiterungen
(`space_of()`, `get(..., repair_drift=)`, Statusvalidierung) in `phase1_storage/storage/`.
Kein weiterer Haltepunkt vorgesehen (Plan §4 Step 2 ist mechanisch, Erweiterungen sind bereits
freigegeben).
