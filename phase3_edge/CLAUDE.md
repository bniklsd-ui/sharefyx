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
| 3 | `mcpserver/request_log.py` (Tool- + HTTP-Log) | 2 | ⬜ | — |
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

## Session stopped — 2026-07-27 (Step 1: Gerüst und `SPACE_ALLOWED_HOSTS`)

**Ergebnis:** Step 1 abgeschlossen. `phase3_edge/` ist jetzt ein vollständiges (Nicht-Python-)
Verzeichnis mit Test-Anschluss; `SPACE_ALLOWED_HOSTS` existiert als Konfiguration statt
CLI-Zufall (P3-C).

**Dateien:**
- `phase3_edge/local.env.example` — Vorlage mit vier Platzhaltern (`REPO_ROOT`, `DATA_ROOT`,
  `VENV`, `ALLOWED_HOSTS`), ausschließlich Kommentare + Beispielpfade, kein echter Hostname,
  kein Token. `phase3_edge/local.env` selbst ist ab jetzt in `.gitignore` (Kommentar erklärt
  warum: Maschinenpfade, kein Geheimnis — der Hostname steht ohnehin in CT-Logs).
- `phase3_edge/tests/__init__.py` — leer, wie im Plan-Dateibaum vorgesehen (P1/P2 kommen ohne
  aus, P3 bekommt es laut Plan explizit, hier übernommen statt hinterfragt).
- `pytest.ini`: `testpaths` um `phase3_edge/tests` erweitert.
- `mcpserver/config.py`: `Settings.allowed_hosts: tuple[str, ...] = ()` neu, geparst über
  `_parse_allowed_hosts()` aus `SPACE_ALLOWED_HOSTS` (Komma-getrennt, `strip()`, leere Einträge
  verworfen, fehlende Variable → leeres Tupel — dieselbe Kein-Default-auf-echten-Wert-Logik wie
  bei `SPACE_DATA_ROOT`).
- `mcpserver/app.py`: `create_app()` berechnet `hosts = list(allowed_hosts) if allowed_hosts
  else (list(settings.allowed_hosts) or None)` — expliziter Parameter gewinnt, danach Settings,
  sonst FastMCPs eigener Default. Docstring ergänzt.
- `scripts/serve.py`: **unverändert**, wie geplant — `--allowed-host` bleibt `action="append"`,
  `default=None`; die neue Präzedenz lebt vollständig in `create_app()`.

**Tests** (`phase2_mcp/tests/test_config.py`, `test_app.py`, alle fünf aus dem Plan):
`test_allowed_hosts_defaults_to_empty`, `test_allowed_hosts_parses_comma_list`,
`test_allowed_hosts_strips_whitespace_and_drops_empties`,
`test_create_app_prefers_explicit_allowed_hosts_over_settings`,
`test_create_app_uses_settings_allowed_hosts`. Die beiden `app.py`-Tests patchen
`mcpserver.app.build_mcp` gegen eine `_CapturingFastMCP`-Stub-Klasse (`http_app()` zeichnet den
übergebenen `allowed_hosts`-Wert auf) statt den vollen FastMCP-Stack zu starten — Präzedenz ist
reine Verdrahtungslogik in `create_app()`, kein FastMCP-Verhalten (das deckt bereits
`test_asgi.py`/der Rest von `test_app.py` aus P2 ab).

**Verifiziert:**
- `.venv/bin/python -m pytest -q` → **138/138 grün** (133 Baseline + 5 neue).
- `bash scripts/dev_install.sh` (venv aktiviert) lief durch: nur `storage` und `mcpserver`
  editable installiert, `phase3_edge/` lautlos übersprungen (kein `pyproject.toml`) — Plan-Aussage
  in §1.2 damit real geprüft, nicht nur zitiert.

**Modul-Status oben nachgezogen** (Zeile 2: ⬜ → ✅, 5 Tests). Ab diesem Block gilt die
Rotationsregel: der Step-0-Block wandert über `scripts/rotate_session_block.sh phase3_edge`
nach `SESSIONS_ARCHIVE.md`.

**Nächster Schritt (konkret):** Step 2 — `mcpserver/request_log.py` (Tool- und HTTP-Log). Der
wichtigste Test dort ist `test_tool_event_never_contains_item_title` — er prüft eine Zusage,
keine Implementierung.
