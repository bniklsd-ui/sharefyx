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
| 6 | Backup/Restore-Skripte, Backup-Timer | 5 | ✅ | 9 (7 in `test_backup_scripts.py`, 2 in `test_units.py`) |
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

## Session stopped — 2026-07-27 (Step 5: Backup und Restore-Nachweis)

**Ergebnis:** Step 5 abgeschlossen. `backup_data_root.sh` (git bundle + Verify + Retention),
`restore_check.sh` (Klon + HEAD/Tree-Vergleich), `sharefyx-backup.service`/`.timer` (Platzhalter,
nicht installiert — Step 7).

**`git bundle create` schlägt auf einem leeren Repo fehl** ("Refusing to create empty bundle") —
jede Testfixture (`data_root`) legt deshalb einen echten Commit an, nicht nur ein leeres
`git init`.

**Zeitstempel-Kollisionsfalle umgangen, nicht nur vermieden (Advisor-Fund, dieselbe Klasse Fehler
wie `mcp_smoke.py` in P2, siehe archivierter Step-7-Block):** `test_backup_retention_keeps_newest_n`
läuft das Skript **nicht** in einer Schleife (bei Sekundenauflösung würden mehrere Bundles
denselben Dateinamen bekommen und sich überschreiben). Stattdessen legt der Test fünf Fake-Bundles
mit distinktem, sortierbarem Namen vor und ruft das Skript nur einmal für das echte, aktuelle
Bundle auf. Der Dateiname selbst trägt jetzt zusätzlich Mikrosekunden (`%6N`, keine Doppelpunkte)
statt nur Sekunden — doppelte Absicherung für den Fall eines künftigen Schleifen-Aufrufs.

**`test_backup_fails_and_cleans_up_on_corrupt_bundle` — echte Korruption, nicht simuliert
(Advisor-Vorschlag umgesetzt):** ein frisch geschriebenes, gültiges Bundle besteht die eigene
`git bundle verify` selbstverständlich. Der Test schiebt stattdessen einen Fake-`git`-Wrapper vor
den echten auf `$PATH`, der `bundle verify` immer mit Exit 1 abbrechen lässt und alles andere an
das echte `git` durchreicht — prüft damit den tatsächlichen Cleanup-Zweig (`rm -f` + Exit ≠ 0),
nicht nur seine Absicht.

**`git bundle verify` schreibt die Ref-Liste auf stdout, die Bestätigung auf stderr** (empirisch
geprüft, nicht angenommen) — im Skript deshalb explizit `>&2` umgeleitet, sonst hätte Hard Rule 7
(stdout nur maschinenlesbares JSON) auf einem Zwischenschritt gebrochen, den der Plan nicht
erwähnt.

**`SHAREFYX_BACKUP_DIR` ist Konfiguration im Skript (Umgebungsvariable, kein Literal), aber ein
fester Wert in der Unit** (`/var/backups/sharefyx`, Plan §4 Step 5 "Ziel ist Konfiguration ...,
kein Literal im Skript"). Bewusst **kein** fünfter Platzhalter/`local.env`-Eintrag: anders als
`REPO_ROOT`/`DATA_ROOT` ist ein Backup-Zielverzeichnis kein Wert, der zwischen Maschinen
tatsächlich variieren muss — ein FHS-üblicher Pfad reicht, ohne `install_units.sh` und
`local.env.example` um eine fünfte Variable zu erweitern.

**`install_units.sh` unverändert lauffähig für die neuen Units:** es verarbeitet generisch alle
`*.service`/`*.timer` in `phase3_edge/systemd/` (so in Step 4 vorbereitet) — die zwei neuen
Backup-Units laufen ohne Skriptänderung durch dieselbe Platzhalter-Ersetzung und
Unresolved-Placeholder-Prüfung.

**`test_units.py` (Step 4) erweitert, nicht dupliziert:** zwei neue Tests
(`test_all_units_have_no_secret_shaped_value`, `test_all_units_have_no_hardcoded_machine_paths`)
laufen über **alle** Unit-Dateien im Verzeichnis, nicht nur die MCP-Unit — sonst hätte die
Token-Klartext-Versicherung aus Step 4 die beiden neuen Backup-Units stillschweigend
ausgenommen.

**Tests** (`phase3_edge/tests/test_backup_scripts.py`, alle sieben aus dem Plan, gegen
Wegwerf-Git-Repos unter `tmp_path`, nie den echten `DATA_ROOT`): `test_backup_creates_verifiable_bundle`,
`test_backup_emits_single_json_line_on_stdout`, `test_backup_retention_keeps_newest_n`,
`test_backup_fails_and_cleans_up_on_corrupt_bundle`, `test_restore_check_matches_head_and_tree`,
`test_restore_check_detects_divergence`, `test_scripts_have_no_hardcoded_paths`. Plus zwei in
`phase3_edge/tests/test_units.py` (siehe oben).

**Verifiziert:** `.venv/bin/python -m pytest -q` → **168/168 grün** (159 + 9 neue).

**Modul-Status oben nachgezogen** (Zeile 6: ⬜ → ✅, 9 Tests).

**Offen für den Nikinger, weiterhin unverändert:**
1. `mcp_smoke.py`/P3-N-Grenzfrage aus Step 2.
2. Tailscale ist auf dieser VM weiterhin nicht installiert — einziges Gate vor Step 7.

**Nächster Schritt (konkret):** Step 6 — Runbooks, `diagnose.sh`, Cloudflare-Rückbau. Der
Cloudflare-Uninstall selbst ist ein Befehl **für den Nikinger** (destruktive Aktion auf der
realen Maschine, außerhalb des Repos) — Claude Code liefert nur den Runbook-Text, führt ihn
nicht aus.
