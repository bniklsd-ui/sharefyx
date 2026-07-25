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
| 4 | `credentials.py`, `scripts/issue_token.py` | 3 | ⬜ | — |
| 5 | `auth.py`, `permissions.py`, `context.py`, `asgi.py`, `logging_setup.py` | 4 | ⬜ | — |
| 6 | `server.py`, `app.py`, `scripts/serve.py` | 5 | ⬜ | — |
| 7 | `tools.py` (die sechs Tools) | 6 | ⬜ | — |
| 8 | `scripts/mcp_smoke.py`, Runbook, Größenmessung | 7 | ⬜ | — |

**Gesamt: 3 Tests** (`test_config.py`) — dieser Head zählt nur `phase2_mcp/tests/`. Step 2 fügte
acht weitere Tests in `phase1_storage/tests/` hinzu (siehe Modul-Status Zeile 3 und
`phase1_storage/CLAUDE.md`), die dort mitgezählt werden, nicht hier.

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

**Warum nur Hashes im Keyring** (vorgezogen aus Plan §2.3, wird in Step 3 mit Code belegt): der
Server muss ein Token nur *wiedererkennen*, nie *vorzeigen*. Wer diese Eigenschaft aufgibt, um
„das Token nochmal anzeigen" zu können, macht aus dem Keyring eine Passwortliste.

**Was der Pfad-Token nicht ist** (vorgezogen aus Plan §2.3): kein OAuth-Ersatz, kein Schutz
gegen Cloudflare (R4 — Cloudflare sieht bei P3 ohnehin Klartext), gültig bis P3+1. Siehe
P2-Plan §0.3 für die Begründung, warum OAuth trotzdem hinter P3 bleibt statt vorgezogen zu
werden.

**`version` in fremden Spaces** (Plan §3.4): `get(..., repair_drift=)` existiert seit Step 2 im
Store; genutzt wird es ab Step 6 (`tools.py :: get_item`, §3.4). Dort ist `version` in fremden
Spaces informativ, nicht autoritativ — es gibt dort per Architektur keine Writes.

---

## Session stopped — 2026-07-25 (Step 2: P1-Contract-Erweiterungen)

**Ergebnis:** Die drei vom Nikinger freigegebenen, einmaligen Erweiterungen (Plan §0.4 Punkt L,
§4 Step 2) in `phase1_storage/storage/` eingebracht:
- `models.py`: `STATUS_VALUES` (Statusvokabular je `type`) + `valid_statuses()`.
- `store.py`: neuer Helper `_check_type_and_status()`, aufgerufen aus `create()` und `update()`
  — wirft `ValidationError` bei unbekanntem `type` oder unerlaubtem `status` (D2).
- `store.py :: space_of(item_id)` — reiner Index-Lookup, kein Datei-Read, `ItemNotFound` bei
  unbekannter ID.
- `store.py :: get(item_id, *, repair_drift=True)` + `_reconcile_and_get_row(...,
  repair_drift=True)` — bei `repair_drift=False` und erkannter Drift wird nur der Index
  nachgezogen, kein Frontmatter-Rewrite, kein Git-Commit (D3). Default `True` lässt jedes
  bestehende P1-Verhalten unverändert.

**Details, Code-Anker und die vollständige Begründung stehen in `phase1_storage/CLAUDE.md`**
unter „Geerbte Contracts" (Code-nah, nicht hier dupliziert — Vorgabe aus diesem Head selbst,
„Was hier bewusst NICHT steht").

**Verifiziert (live):** acht neue Tests in `phase1_storage/tests/test_store.py`
(`test_space_of_returns_space`, `test_space_of_unknown_raises_item_not_found`,
`test_get_repair_drift_false_leaves_file_untouched`, `test_get_repair_drift_false_creates_no_commit`,
`test_get_repair_drift_true_still_bumps`, `test_create_rejects_unknown_status`,
`test_update_rejects_unknown_status`, `test_update_accepts_valid_status_per_type`). Gesamtsuite
`pytest -v` → **79/79 grün** (76 in `phase1_storage/tests/` inkl. dieser acht, 3 in
`phase2_mcp/tests/`). Keine bestehende P1-Test musste angepasst werden — die einzigen
Store-Aufrufe mit explizitem `status=` in `test_store.py` (`status="open"` auf einem `task`,
`status="done"` auf einem `task`) waren bereits typkonform.

**Nächster Schritt (konkret):** Step 3 — `credentials.py` + `scripts/issue_token.py`. Braucht
eine Nikinger-Rückmeldung, sobald der finale Funktionstest (`keyring`-Wert schreiben und
zurücklesen) gelaufen ist — V5 ist bis dahin „vielversprechend", nicht „bestätigt".
