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
| 4 | `credentials.py` LoadCredential-Pfad, `export_space_map.py` | 3 | ✅ | 6 |
| 5 | systemd-Units, `install_units.sh`, `/health.uptime_s` (P3-I) | 4 | ✅ | 6 |
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

## Session stopped — 2026-07-27 (Step 4: systemd-Units)

**Ergebnis:** Step 4 abgeschlossen. `phase3_edge/systemd/sharefyx-mcp.service` (Platzhalter,
nicht auf der VM installiert), `phase3_edge/scripts/install_units.sh`, plus `/health` trägt jetzt
`uptime_s` (P3-I).

**`uptime_s` war im Plan §4 keinem Step zugewiesen — Lücke geschlossen, nicht stillschweigend
übersprungen (Advisor-Fund):** P3-I ("genau ein neues Feld") steht in §0.5, §1.1 und in Step 7s
Abnahmematrix (Zeile 1), aber in keinem der Steps 0–7 als Liefergegenstand. Step 6
(`diagnose.sh`, Prüfung 2) und der Disconnected-Runbook setzen das Feld aber voraus. Hier in
Step 4 gebaut, bevor Step 6 es braucht: `app.py :: create_app()` setzt `app.state.start_time =
time.monotonic()` **pro App-Instanz** (nicht Modulebene — sonst teilten sich mehrere
`create_app()`-Aufrufe, z. B. in Tests, einen Startzeitpunkt), `_health()` berechnet
`uptime_s = int(time.monotonic() - request.app.state.start_time)`. `app.py` steht in P3-Ns
Berührungsliste, keine Scope-Erweiterung.

**`test_health_ok` aus P2 korrekt rot geworden, wie von seinem eigenen Kommentar angekündigt:**
der Test prüft absichtlich die exakte Schlüsselmenge der `/health`-Antwort ("fängt eine spätere
Erweiterung um ein zusätzliches Feld ab"). Mit `uptime_s` dazu aktualisiert
(`{"status","service","version","uptime_s"}`), `isinstance(..., int)` und `>= 0` geprüft.
`test_health_leaks_no_space_names` bleibt unverändert grün — `uptime_s` leakt nichts.

**`local.env.example` trug echte Maschinenpfade dieser VM — korrigiert (Advisor-Fund):**
`REPO_ROOT`/`DATA_ROOT`/`VENV` zeigten auf `/home/savefyx/...`. P3-Js eigene Begründung für das
Platzhalterschema ist Maschinenunabhängigkeit ("der Kollege oder eine zweite VM sollen dasselbe
Repo benutzen können"), und §5 Akzeptanzkriterium 8 nennt „kein Maschinenzustand im Repo" — ein
kopiertes Beispiel mit dieser VMs echten Pfaden hätte plausibel, aber falsch ausgesehen. Jetzt
`/path/to/savefxy` etc.

**`install_units.sh` bricht vor jedem `/etc`- oder `systemctl`-Zugriff ab, wenn `local.env`
fehlt** — genau der Pfad, den der Test ausübt, ohne root-Rechte oder einen echten systemd
anzufassen. Verarbeitet generisch alle `*.service`/`*.timer` in `phase3_edge/systemd/` (Step 5
liefert die Backup-Units in dasselbe Verzeichnis, ohne dass dieses Skript sich ändern muss),
prüft nach der Platzhalter-Ersetzung per Regex, ob `__[A-Z_]+__` noch irgendwo übrig ist, und
löscht eine unvollständige Zieldatei sofort statt sie stehen zu lassen. **Die Unit ist nach
diesem Step bewusst noch nicht auf der VM installiert** — das ist Step 7.

**`V9` (`ProtectHome=read-only` + `ReadWritePaths` erlaubt Git-Commits im `DATA_ROOT`) bleibt
offen** — laut Plan nur zur Laufzeit prüfbar, `test_units.py` ist reines Textparsen. Der bereits
in Step 0 bestätigte Fund (Git-Identität `Space Server`/`space-server@localhost` liegt im
`DATA_ROOT` selbst, nicht nur in `~/.gitconfig`) ist der Ausgangspunkt für den ersten
Write-Test in Step 7 — dorthin verschoben, nicht hier vorweggenommen.

**Tests** (`phase3_edge/tests/test_units.py`, alle sechs aus dem Plan):
`test_unit_restarts_on_failure`, `test_unit_loads_credential_encrypted`,
`test_unit_binds_loopback_only`, `test_unit_has_no_secret_shaped_value`,
`test_unit_placeholders_are_unresolved_in_repo`,
`test_install_script_refuses_without_local_env` (kopiert `scripts/`+`systemd/` in ein
Wegwerf-Verzeichnis ohne `local.env` — hermetisch, unabhängig davon, ob auf dieser Maschine
zufällig ein echtes `phase3_edge/local.env` existiert). Plus die aktualisierten
`test_health_ok`/-Assertions in `phase2_mcp/tests/test_app.py`.

**Verifiziert:** `.venv/bin/python -m pytest -q` → **159/159 grün** (153 + 6 neue).

**Modul-Status oben nachgezogen** (Zeile 5: ⬜ → ✅, 6 Tests).

**Offen für den Nikinger (nicht blockierend für Steps 5–6, aber noch nicht gemeldet):**
1. `mcp_smoke.py`/P3-N-Grenzfrage aus Step 2 — ob `mcp_smoke.py` auf `configure_logging()`
   umgestellt werden soll (Zweizeiler), steht weiterhin offen.
2. Tailscale ist auf dieser VM weiterhin nicht installiert (Step 0) — einziges Gate vor Step 7.

**Nächster Schritt (konkret):** Step 5 — Backup- und Restore-Skripte (`git bundle` + Verify +
Retention), Backup-Timer. Beide Skripte laufen in Tests ausschließlich gegen Wegwerf-Git-Repos
unter `tmp_path`, nie gegen den echten `DATA_ROOT`.
