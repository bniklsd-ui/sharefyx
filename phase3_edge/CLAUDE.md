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
| 2 | Paketgerüst `phase3_edge/`, `SPACE_ALLOWED_HOSTS` in `config.py`/`app.py` | 1 | ⬜ | — |
| 3 | `mcpserver/request_log.py` (Tool- + HTTP-Log) | 2 | ⬜ | — |
| 4 | `credentials.py` LoadCredential-Pfad, `export_space_map.py` | 3 | ⬜ | — |
| 5 | systemd-Units, `install_units.sh` | 4 | ⬜ | — |
| 6 | Backup/Restore-Skripte, Backup-Timer | 5 | ⬜ | — |
| 7 | Runbooks, `diagnose.sh`, Cloudflare-Rückbau | 6 | ⬜ | — |
| 8 | Live-Abnahme (Nikinger) | 7 | ⬜ | — |

## Rotationsregel

Ab dem **zweiten** Session-Block läuft `scripts/rotate_session_block.sh phase3_edge` — nie von
Hand. Dieser erste Block bleibt hier stehen, bis der zweite ihn verdrängt.

## Runbooks

Werden in Step 6 (Diagnose/Disconnected) und Step 7 (Inbetriebnahme) befüllt — Platzhalter
bewusst leer, siehe Plan §4 Step 6/7.

---

## Session stopped — 2026-07-27 (Step 0: Doku-Drift, Verifikation, Umgebungsinventar)

**Ergebnis:** Step 0 abgeschlossen. Kein Feature-Code — Haushalt vor dem ersten Baustein.

**A · Doku-Drift geschlossen** (Quelle: `PHASE2_CLOSEOUT_HANDOVER.md` §6 + Plan §0.4/§6):
- Root-`CLAUDE.md`: R5 „OAuth ist Phase 5" → **Phase 4** korrigiert (deckt sich mit der
  ROADMAP-Korrektur vom 2026-07-25, die bereits vorher galt, aber in R5 nicht nachgezogen war).
- Root-`CLAUDE.md`: R4 um die datierte Ergänzung zu Tailscale Funnel erweitert (§0.4 des Plans,
  wörtlich übernommen) — der ursprüngliche Cloudflare-Satz bleibt stehen, er beschreibt weiterhin
  korrekt, was dort gilt.
- Root-`CLAUDE.md`, „Current state": aktive Phase auf **P3** umgestellt, P2 in einen eigenen
  ✅-Absatz nach dem Muster von Phase 1 verschoben (inkl. Hinweis, dass der formale
  Abschluss-Handover jetzt existiert — der Satz „Formaler Phasenabschluss … steht noch aus" war
  mit `PHASE2_CLOSEOUT_HANDOVER.md` bereits überholt). `down:`-Karte von `phase2_mcp/CLAUDE.md`
  auf `phase3_edge/CLAUDE.md` umgehängt.
- `ROADMAP.md` und `phase2_mcp/CLAUDE.md`: `` `fastmcp` über Streamable HTTP `[VERIFY]` `` →
  Marker entfernt (live widerlegt, siehe P2-Abnahme).
- `ROADMAP.md`, Header-Card `down:`: `phase2_mcp_plan.md` und `phase3_edge_plan.md` ergänzt.
- `ROADMAP.md`, P3-Zeile: ⬜ → 🔄.
- `ROADMAP.md`, „Zurückgestellt aus P2": MCP-Revisions-Eintrag von Datum auf **Trigger**
  umgestellt (P3-E) — „erstes `fastmcp`-Release mit Support", nicht der 2026-07-28-Termin.
- `docs/INDEX.md`: neuer Abschnitt „Active phase (3)" mit drei Zeilen (Plan, Phase-Head, leeres
  Archiv); P2-Abschnitt nach „Completed phases" verschoben (🔄 → 📗); Zeile für
  `PHASE2_CLOSEOUT_HANDOVER.md` ergänzt; „Concept docs"-Fußnote von „P3–P5"/„P1- und P2-Pläne"
  auf „P4–P5"/„P1-, P2- und P3-Pläne" korrigiert.
- `ROADMAP.md`, P2-Abschnitt: der Satz „Fehlt noch: der formale Phasenabschluss (Browser-Webchat)"
  war mit `PHASE2_CLOSEOUT_HANDOVER.md` bereits überholt und stand — anders als in Root-`CLAUDE.md`
  — noch drin. Ersetzt durch „Handover an P3: `docs/concepts/PHASE2_CLOSEOUT_HANDOVER.md`",
  spiegelt jetzt den P1-Abschnitt, der denselben Satz für P1→P2 trägt.
- `phase2_mcp/CLAUDE.md`: `updated:`-Feld der Header-Card war bei diesem Commit stehen geblieben
  (`2026-07-26 (B2 behoben)`), obwohl der Scope-Absatz sich änderte — auf 2026-07-27 nachgezogen.

**Abweichung vom Plan, benannt:** `phase3_edge/CLAUDE.md` und `SESSIONS_ARCHIVE.md` (Plan-Step 1)
wurden bereits in Step 0 angelegt — minimal (L1-Card, Modul-Status, dieser Block), Scope/Runbooks
folgen wie geplant in Step 1. Grund: Hard Rule 8 verlangt den Phase-Head im selben Commit wie
jeden Step-Abschluss, und `docs/INDEX.md` braucht in diesem Commit bereits einen realen
Link-Empfänger statt eines toten Links.

**Sicherheits-Check vor dem Commit:** Die drei neuen, unversionierten Dateien
(`PHASE2_CLOSEOUT_HANDOVER.md`, `phase3_edge_plan.md`, `phase2_mcp_uebersicht.svg`) wurden vor
dem Staging mit `grep -aoE '[A-Za-z0-9_-]{32,}'` auf token-förmige Strings geprüft — Treffer
waren ausschließlich Testfunktionsnamen aus dem Plan. Das SVG (P2-Architekturdiagramm) enthält
nur den literalen Platzhalter `‹token›`, keinen echten Wert. Die SVG ist kein `.md` und damit
laut `docs/INDEX.md`-Scope („L0 map of every project .md") nicht indexpflichtig — bewusst nicht
aufgenommen, hier vermerkt statt stillschweigend übergangen.

**B · Verifikationsdurchlauf:**
- `git status` vor dem Commit: nur die drei erwarteten neuen Dateien untracked, sonst sauber.
- `docs/test-results/` existiert nicht (per `ls`, nicht per Doku-Aussage geprüft).
- Oversize-Check (`find … -size +40k`): zwei Treffer, `phase2_mcp_plan.md` und
  `phase3_edge_plan.md` — beide 📕, damit erlaubt.
- `pytest -q` über `.venv/bin/python -m pytest` (nicht System-Python): **133/133 grün**, deckt
  sich mit ROADMAP/Handover-Baseline.

**C · Umgebungsinventar** (alles `[VERIFY]`, read-only, kein Eingriff in echten `DATA_ROOT`/Keyring/Token):

| Prüfung | Ergebnis |
|---|---|
| Python | 3.12.3 |
| venv (für `ExecStart`, V6) | `/home/savefyx/dev/savefxy/.venv/bin/python` — Symlink-Kette über `python3` → System-`/usr/bin/python3.12`; der venv-Pfad selbst ist der korrekte `ExecStart`-Wert (aktiviert `pyvenv.cfg`/site-packages), nicht das Symlink-Ziel |
| `fastmcp` (V2) | **3.4.4 exakt installiert** — deckt sich bereits mit dem P3-D-Pin, keine Änderung nötig |
| Keyring-Backend (V5) | `keyring.backends.SecretService.Keyring` (priority 5), Chainer als Default-Frontend — deckt sich mit dem in P2 vom Nikinger bestätigten Roundtrip |
| systemd (V4) | Version 255 (≥250 ✓) |
| `systemd-creds` (V4) | vorhanden; `has-tpm2` → **„partial"**, kein volles TPM2-Sealing verfügbar (`+system`/`+subsystem`/`+libraries`, `-firmware`/`-driver`), Exit 3. `systemd-creds encrypt` fällt in diesem Fall auf Host-Key-Verschlüsselung zurück — für P3-F ausreichend (die Datei ist eine Hash-Map, kein umkehrbares Geheimnis; siehe Plan-Begründung) |
| Tailscale (V7) | **NICHT installiert** — `tailscale: command not found`. Echter Befund, kein „nichts zu tun": vor Step 7 (und vor jedem Live-Test von Step 4/6 gegen einen echten Funnel) muss der Nikinger Tailscale installieren, dem Tailnet beitreten, MagicDNS + HTTPS-Zertifikate aktivieren und `nodeAttrs: funnel` im Policy-File setzen. Blockiert **nicht** Steps 1–6 (reiner Code/Test-Weg), blockiert **Step 7**. |
| Dateisystem `DATA_ROOT` | `ext4` bestätigt — P1-Bedingung für `flock` weiterhin erfüllt |
| `cloudflared` | vorhanden unter `/usr/local/bin/cloudflared`, **kein** systemd-Service registriert (nur die P2-Quick-Tunnel-Nutzung von Hand) — Rückbau bleibt wie geplant Aufgabe von Step 6 |
| Git-Identität in `DATA_ROOT` | vorhanden (`Space Server` / `space-server@localhost`) — relevant für den in Plan §4 Step 4 benannten `ProtectSystem=strict`/Git-Commit-Fallstrick, dort real zu prüfen |

**Verifiziert:** `pytest -q` (via `.venv/bin/python -m pytest`) → 133/133 grün. `git status` vor
Commit sauber bis auf die drei erwarteten neuen Dateien. Secret-Scan der drei Dateien negativ.

**Nächster Schritt (konkret):** Step 1 — `phase3_edge/`-Gerüst vervollständigen
(`local.env.example`, `tests/__init__.py`, `.gitignore`-Ergänzung, `pytest.ini`-Erweiterung) und
Konfiguration (`SPACE_ALLOWED_HOSTS` in `config.py`/`app.py`, fünf Tests laut Plan). **Vor
Step 7** braucht es zusätzlich eine Nikinger-Aktion außerhalb des Plans selbst: Tailscale auf
dieser VM installieren und die Tailnet-Voraussetzungen (V7) einrichten — sonst lässt sich der
Runbook-Teil aus Step 7 nicht gegenprüfen.
