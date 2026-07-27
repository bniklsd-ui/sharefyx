---
status: live
purpose: Phase-Head Exposure & Betrieb — Scope, harte Regeln, Modulstatus, aktueller Session-Handover
read-when: Arbeiten in phase3_edge/ oder an den in P3-N genannten Dateien in phase2_mcp/mcpserver — zuerst lesen, zusammen mit dem neuesten Session-stopped-Block
detail: L2
up: ../CLAUDE.md
down:
  - ../docs/concepts/phase3_edge_plan.md          # voller Plan, Entscheidungen P3-A–P3-N, Steps 0–7
  - ../docs/concepts/PHASE2_CLOSEOUT_HANDOVER.md  # Herkunft der offenen Entscheidungen 1–8
  - SESSIONS_ARCHIVE.md                            # ältere Session-Blöcke, newest-first
updated: 2026-07-27
---

# CLAUDE.md — Phase 3: Exposure & Betrieb (`phase3_edge/`)

> **Der Connector steht in beiden Claude-Accounts und bleibt stehen.** P3 fügt dem in P2
> bewiesenen Server nichts Fachliches hinzu — nur eine dauerhafte Adresse, einen
> selbstheilenden Prozess und ein Protokoll über sein Verhalten.
> **Quelle der Wahrheit ist der Code, nicht dieses Dokument.**
> Vollständiges Design + alle 14 gelockten Entscheidungen (P3-A–P3-N) + Steps 0–7:
> `../docs/concepts/phase3_edge_plan.md`.

## Mission (zuerst lesen)

Der eigentliche Härtetest der Phase ist nicht der Tunnel, sondern die Wiederherstellbarkeit:
nach einem VM-Reboot, einem `kill -9` und einem Backup-Restore muss dieselbe URL dieselben
Daten liefern — ohne dass ein Mensch etwas nachträgt.

## Bauprinzip (Projekt-Kernprinzip)

„Der Server ist dumm." **Phase 3 enthält KEINE AI, keine neuen Tools, keine Fachlogik.** Wer
hier `tools.py` anfasst, ist in der falschen Phase.

## Scope (Kurzform, Details: Plan §0.5 P3-A–P3-N)

- **DRIN:** Tailscale Funnel (stabile Adresse), systemd-Unit (`Restart=on-failure`,
  `LoadCredentialEncrypted`), `/health` + `uptime_s`, strukturiertes Request-Log (Tool-Name +
  Dauer, `journald`), Backup (`git bundle`) + verifizierter Restore, Runbook „Connector zeigt
  Disconnected".
- **DRAUSSEN:** VPS-Migration, Monitoring/Alerting, OAuth (P4), neue Tools, D6, Migration auf
  MCP-Revision 2026-07-28 (Watch-Item mit Trigger statt Datum, P3-E).

## Harte Regeln dieser Phase (nicht verhandelbar)

- **P3-B — `SPACE_HOST` wird nie `0.0.0.0`.** Der Server lauscht unverändert auf
  `127.0.0.1:8765`; Funnel proxyt dorthin. Hard Rule 6 gilt damit nicht nur am Router, sondern
  am Host.
- **P3-N — Berührungsfläche.** P3 darf in `phase2_mcp/` genau anfassen: `mcpserver/config.py`,
  `mcpserver/logging_setup.py`, `mcpserver/app.py`, `mcpserver/credentials.py`,
  `scripts/serve.py`, plus **ein neues Modul** `mcpserver/request_log.py`. **Nicht anfassen:**
  `tools.py`, `permissions.py`, `auth.py`, `asgi.py`, `server.py`, `storage/*`. Änderungsbedarf
  dort ist ein Befund für den Nikinger, keine Aufgabe.
- **`phase3_edge/` ist kein Python-Paket** (bewusste Abweichung von P1/P2-Muster, Plan §1.2) —
  Servercode gehört nach `mcpserver`, hier stehen nur Units, Ops-Skripte, deren Tests und Doku.
  `scripts/dev_install.sh` überspringt das Verzeichnis bereits korrekt (kein `pyproject.toml`).

## Modul-Status

| # | Modul | Step | Status | Tests |
|---|---|---|---|---|
| 1 | Haushalt, Doku-Drift, Verifikationslauf, Umgebungsinventar | 0 | ✅ | 0 (kein Feature-Code) |
| 2 | Paketgerüst `phase3_edge/`, `SPACE_ALLOWED_HOSTS` in `config.py`/`app.py` | 1 | ✅ | 5 |
| 3 | `mcpserver/request_log.py` (Tool- + HTTP-Log) | 2 | ✅ | 9 (8 in `test_request_log.py`, 1 in `test_logging.py`) |
| 4 | `credentials.py` LoadCredential-Pfad, `export_space_map.py` | 3 | ⬜ | — |
| 5 | systemd-Units, `install_units.sh` | 4 | ⬜ | — |
| 6 | Backup/Restore-Skripte, Backup-Timer | 5 | ⬜ | — |
| 7 | Runbooks, `diagnose.sh`, Cloudflare-Rückbau | 6 | ⬜ | — |
| 8 | Live-Abnahme (Nikinger) | 7 | ⬜ | — |

## Umgebungsstand (Step 0, Details im Archiv)

Vier Fakten, die spätere Steps direkt gaten — volle Inventartabelle in `SESSIONS_ARCHIVE.md`:

- venv für `ExecStart` (V6): `/home/savefyx/dev/savefxy/.venv/bin/python`.
- `fastmcp` **3.4.4** bereits installiert — deckt sich mit dem P3-D-Pin, keine Änderung nötig.
- `systemd-creds` vorhanden, `has-tpm2` → partial → `encrypt` läuft über Host-Key statt TPM2 (für
  P3-F ausreichend, siehe Plan-Begründung).
- **Tailscale ist auf dieser VM nicht installiert.** Blockiert nicht Steps 1–6, blockiert
  **Step 7** — Nikinger-Aktion vor der Live-Abnahme (installieren, Tailnet beitreten, MagicDNS +
  HTTPS-Zertifikate an, `nodeAttrs: funnel` im Policy-File).

## Rotationsregel

Ein Phase-Head trägt genau **einen** aktuellen `## Session stopped`-Block. Sobald ein neuer
dazukommt, läuft `scripts/rotate_session_block.sh phase3_edge` — nie von Hand — und verschiebt
den vorherigen Block verbatim nach `SESSIONS_ARCHIVE.md`.

## Runbooks

Werden in Step 6 (Diagnose/Disconnected) und Step 7 (Inbetriebnahme) befüllt — Platzhalter
bewusst leer, siehe Plan §4 Step 6/7.

---

## Session stopped — 2026-07-27 (Step 2: Request-Log)

**Ergebnis:** Step 2 abgeschlossen. `mcpserver/request_log.py` (neu) liefert beide Ereignisarten
aus Plan §3; `ToolCallLogMiddleware` läuft in `create_app()`, `AccessLogASGI` in `serve.py`.

**`[VERIFY]` V3 aufgelöst, gegen den echten `fastmcp==3.4.4`-Code, nicht nur die Doku geprüft:**
`Middleware.on_call_tool(context: MiddlewareContext[CallToolRequestParams], call_next)`,
`context.message.name` trägt den Tool-Namen, Registrierung über `mcp.add_middleware(...)` in
`app.py :: create_app()` — alles wie im Plan angenommen. **Eine Abweichung vom Plan-Wortlaut,
empirisch begründet:** `request_log.py`s Moduldocstring-Skizze nennt `ERROR_CLASSES:
dict[type[Exception], str]`. Das ist mit dem echten `FastMCP.call_tool()`-Pfad nicht umsetzbar —
gelesen bis in `server.py`: die Middleware-Kette ruft die Kernlogik über `call_next()` auf, und
jede dort erhobene `FastMCPError`/`ToolError` (`ToolError` erbt von `FastMCPError`) wird
unverändert weitergereicht. `tools.py :: map_storage_error()` hat die ursprüngliche
`storage`-Exception zu diesem Zeitpunkt bereits in eine `ToolError` mit Präfix-Text übersetzt
(`"conflict: …"`, `"item_not_found: …"`, …) — ein Typ-Dict würde hier immer denselben einen Typ
treffen. `classify_error()` parst deshalb den Nachrichtenpräfix vor dem ersten `":"` statt den
Exception-Typ zu prüfen. Volle Begründung im Moduldocstring von `request_log.py`.

**`space`-Feld — Semantik bewusst festgelegt, nicht nur implizit:** `_current_space()` liefert
den **authentifizierten Aufrufer** (`Principal.space`), nicht den Zielraum des Tool-Aufrufs. Bei
`get_item`/`update_item` gegen einen fremden Space steht im Log also weiterhin der eigene Space,
nicht der fremde. Das beantwortet Plan §3.4 Frage 2 ("mein Account oder der des Kollegen?")
korrekt; für einen Rule-4-Nachweis (wer hat wohin geschrieben) ist das Request-Log bewusst nicht
die Quelle — das leisten die Tool-Fehlerklasse (`write_denied`) und `test_tools.py`/`test_app.py`
(Advisor-Fund, sonst hätte ein kalter Leser beim Debuggen einer Cross-Space-Ablehnung den
Zielraum im Log vermutet).

**`err: "internal"` ist ein Sammelbecken, nicht nur der Whitelist-Fallback — festgehalten für
Step 7:** die Whitelist (`conflict`, `item_not_found`, `write_denied`, `invalid`) lässt
`auth_error`, `space_not_found` und FastMCPs generisches `"Error calling tool …"` alle in
`internal` fallen. Das ist Plan-konform, bedeutet aber: `err: "internal"` in `journald` kann
sowohl „ungültiger Token mitten im Aufruf" als auch „echter Store-Bug" heißen. Kein Blocker für
P3 (keine Abnahmezeile hängt an der Unterscheidung), aber falls Step 7 auf `internal`-Zeilen
stößt, ist das der erste Ort zum Nachschauen, nicht ein Bug im Logging.

**`TokenScrubbingFilter` erweitert** (`logging_setup.py`, im P3-N-Berührungsbereich): scrubbt
jetzt auch String-Werte innerhalb eines Dict-`record.msg` (vorher nur reine String-Messages) —
sonst wäre der Filter auf dem Request-Log-Pfad ein stiller No-op gewesen, praktisch redundant zu
`AccessLogASGI`s eigener Pfad-Redaktion, aber echte Verteidigung in der Tiefe statt einer
Behauptung. Eigener Test in `test_logging.py`
(`test_scrubbing_filter_redacts_token_in_dict_message`), da die P3-Tests den Filter nicht über
`configure_logging()` einbinden.

**Zirkelimport vermieden:** `request_log.py` importiert `_TOKEN_SEGMENT_RE` aus
`logging_setup.py` auf Modulebene; `logging_setup.py :: configure_logging()` importiert
`JsonLineFormatter`/`LOGGER_NAME` aus `request_log.py` **lazy** (innerhalb der Funktion) — zum
Aufrufzeitpunkt ist `logging_setup` bereits vollständig geladen, kein Zirkelbezug beim
Modul-Import.

**`mcp_smoke.py` bewusst nicht angefasst — P3-N-Grenzfall, an den Nikinger gemeldet:** Step 2s
„Done when" verlangt einen manuellen `mcp_smoke.py`-Lauf mit sichtbaren JSON-Zeilen. `mcp_smoke.py`
ruft aber `logging.basicConfig()` statt `configure_logging()` und geht nie durch `serve.py`
(reines In-Process-`ASGITransport`, kein `AccessLogASGI`) — selbst mit funktionierendem
Tool-Log wäre die Ausgabe ein Python-Dict-Repr, kein JSON. `mcp_smoke.py` steht nicht in P3-Ns
„genau anfassen"-Liste; sie ist als abschließende Aufzählung gelesen worden (wie schon bei
`tools.py`/`server.py`), deshalb keine Änderung dort. Stattdessen manuell gegen ein Wegwerf-Skript
(nie eingecheckt, aus dem Scratchpad gelöscht) verifiziert, das genau den echten Produktionspfad
fährt — `configure_logging()` + `create_app()` + `AccessLogASGI`, `FakeResolver` statt echtem
Keyring, temporäres `DATA_ROOT`: `GET /health` und ein Fremdzugriff mit falschem Token erzeugten
korrekt geformte, redigierte JSON-Zeilen auf stderr (`{"ts":"…","ev":"http","method":"GET",
"path":"/health","status":200,"ms":0}` bzw. mit `path":"/mcp/<redacted>","status":401`). Das ist
strengeres Beweismaterial als `mcp_smoke.py` liefern könnte, weil es den echten `serve.py`-Pfad
inklusive `AccessLogASGI` prüft, den `mcp_smoke.py` konstruktionsbedingt nie durchläuft. Für den
Nikinger: falls `mcp_smoke.py` künftig JSON-Request-Logs zeigen soll, ist das eine bewusste
P3-N-Erweiterung (ein Zweizeiler: `logging.basicConfig` → `configure_logging`), keine
Kleinigkeit, die einfach nachgezogen wird.

**Tests** (alle acht aus dem Plan, `phase2_mcp/tests/test_request_log.py`, plus einer in
`test_logging.py` für die Filter-Erweiterung): `test_json_line_is_valid_json`,
`test_tool_event_has_tool_space_and_duration`, `test_tool_event_error_carries_class_not_message`,
`test_tool_event_never_contains_item_title` (gestärkt gegen eine Tautologie-Falle — prüft jetzt
zuerst `len(tool_events) == 6`, bevor die Abwesenheit des Markers behauptet wird; Advisor-Fund:
sonst wäre der Test identisch grün gegen eine Middleware geblieben, die gar nichts loggt),
`test_http_event_redacts_token_segment`, `test_http_event_logs_401_status`,
`test_logging_failure_does_not_break_tool_call`, `test_request_logger_does_not_propagate_to_root`,
`test_scrubbing_filter_redacts_token_in_dict_message`.

**Verifiziert:** `.venv/bin/python -m pytest -q` → **147/147 grün** (138 + 9 neue).

**Modul-Status oben nachgezogen** (Zeile 3: ⬜ → ✅, 9 Tests). Rotation läuft nach diesem Commit.

**Nächster Schritt (konkret):** Step 3 — `credentials.py` LoadCredential-Pfad,
`export_space_map.py`. Alle Tests mit `monkeypatch` auf `$CREDENTIALS_DIRECTORY` und einem
Fake-Keyring, nie der echte Keyring.
