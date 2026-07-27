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

## Session stopped — 2026-07-27 (Step 3: Credentials über systemd)

**Ergebnis:** Step 3 abgeschlossen. `credentials.py :: load_space_map()` liest jetzt zuerst ein
von systemd bereitgestelltes Credentials-Verzeichnis, Keyring bleibt Fallback.
`phase3_edge/scripts/export_space_map.py` (neu) exportiert die Space-Map aus dem Keyring als
JSON auf stdout, für `systemd-creds encrypt`.

**`[VERIFY]` V4 und V5 — bereits in Step 0 beantwortet, hier nur referenziert (kein zweiter
Inventarlauf):** V4 (`systemd-creds` vorhanden, systemd 255 ≥ 250, `has-tpm2` → partial →
Host-Key-Verschlüsselung) und V5 (`keyring.backends.SecretService.Keyring`, Priorität 5) stehen
im „Umgebungsstand"-Abschnitt oben und in `SESSIONS_ARCHIVE.md`, Step-0-Block.

**Plan §2.3 war mit sich selbst im Widerspruch — aufgelöst, nicht stillschweigend
weggelesen:** der Plantext sagt, `export_space_map.py` solle
„`credentials.load_space_map()` **aus dem Keyring** (explizit, nicht über die neue
Verzweigung)" lesen — aber `load_space_map()` **ist** ab diesem Step die neue Verzweigung, ein
Aufruf kann nicht zugleich sie selbst und ihre Umgehung sein. Auflösung (Advisor-Review): die
reine Keyring-Leselogik wurde in eine eigene Funktion `load_space_map_from_keyring()`
ausgelagert. `load_space_map()` ruft sie als Fallback; `export_space_map.py` ruft sie direkt.
Ein Leser, zwei Aufrufer, keine Verzweigung im Export-Pfad. `issue()`/`revoke()` bleiben laut
Plan-Vorgabe **unverändert** (0 Zeilen Diff) und rufen weiterhin `load_space_map()` auf — das ist
unschädlich, weil `$CREDENTIALS_DIRECTORY` in ihrem einzigen realen Aufrufkontext
(`issue_token.py`, interaktiv) nie gesetzt ist.

**Der Fallback-Warnhinweis geht auf den Modul-Logger, nicht auf `sharefyx.request`**
(Advisor-Fund): fehlt die Credential-Datei trotz gesetztem Verzeichnis, loggt `load_space_map()`
über `logging.getLogger(__name__)` — landet also auf dem normalen stderr-Handler aus
`configure_logging()`, nicht im JSON-Request-Log. Der Request-Logger ist laut Plan §3.1 für
`ev="tool"`/`ev="http"` reserviert; eine freie Textmeldung dort wäre zwar gültiges JSON
(`JsonLineFormatter` serialisiert auch einen bloßen String), aber strukturell falsch auf einem
Stream, dessen Vertrag eine Feld-Whitelist ist.

**Test-Ladepfad für `export_space_map.py` (Advisor-Fund):** `phase3_edge/` ist kein Python-Paket
(Plan §1.2), ein normaler `import` aus `phase2_mcp/tests/test_credentials.py` funktioniert
deshalb nicht. Geladen über `importlib.util.spec_from_file_location(...)` gegen den absoluten
Pfad — hält `capsys` für den stdout/stderr-Split nutzbar, im Unterschied zu einem
Subprocess-Aufruf. Da `export_space_map.py`s `from mcpserver import credentials` denselben
gecachten Modul-Objekt-Namen trifft wie der Testcode, wirkt der `fake_keyring`-Monkeypatch aus
`test_credentials.py` transparent auch dort — kein zweiter Fake nötig.

**Doku:** `README.md`, Abschnitt „Token ausgeben, rotieren, widerrufen" um „Rotation im
Dienstbetrieb (ab P3)" erweitert — der volle Vierschritt aus P3-M (Token neu ausgeben → Export →
`systemctl restart` → Connector-URL aktualisieren), inklusive des Satzes, dass ein vergessener
Restart wie „Connector kaputt" aussieht, aber ein 401 auf die alte Credential-Datei im tmpfs ist.

**Tests** (`phase2_mcp/tests/test_credentials.py`, alle sechs aus dem Plan, mit `monkeypatch`
auf `$CREDENTIALS_DIRECTORY` und dem bestehenden `fake_keyring`-Fixture — nie der echte
Keyring): `test_load_space_map_prefers_credentials_dir`,
`test_load_space_map_falls_back_when_credentials_dir_unset`,
`test_load_space_map_falls_back_when_credential_file_missing`,
`test_load_space_map_raises_on_malformed_credential`,
`test_export_writes_json_to_stdout_and_note_to_stderr`,
`test_export_contains_no_plaintext_token`.

**Verifiziert:** `.venv/bin/python -m pytest -q` → **153/153 grün** (147 + 6 neue). Alle
bestehenden `test_credentials.py`-Tests (die alte `load_space_map()`-Aufrufe machen) liefen
unverändert grün weiter — `$CREDENTIALS_DIRECTORY` ist in der Testumgebung nie gesetzt, der
Fallback greift transparent.

**Modul-Status oben nachgezogen** (Zeile 4: ⬜ → ✅, 6 Tests).

**Nächster Schritt (konkret):** Step 4 — systemd-Units (`sharefyx-mcp.service`,
`install_units.sh`). `test_unit_has_no_secret_shaped_value` ist die billigste Versicherung gegen
den Token-Klartext-Vorfall, der in P2 zweimal passiert ist.
