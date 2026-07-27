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
| 7 | Runbooks, `diagnose.sh`, Cloudflare-Rückbau | 6 | ✅ | 0 (Runbook/Skript, keine automatisierten Tests laut Plan) |
| 8 | Live-Abnahme (Nikinger) | 7 | 🔄 in Arbeit — 8/14 Zeilen belegt, B3+B4 gefunden und behoben | — |

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

### „Connector zeigt Disconnected"

`phase3_edge/scripts/diagnose.sh` automatisiert genau diesen Entscheidungsbaum — bei der ersten
fehlschlagenden Prüfung gibt es eine Diagnose plus einen Handlungssatz aus und stoppt. Von Hand
dieselbe Reihenfolge:

1. **`systemctl is-active sharefyx-mcp`** — nicht aktiv? → `journalctl -u sharefyx-mcp -n 50`.
   Das ist die häufigste Ursache und die billigste Prüfung, deshalb zuerst.
2. **`curl -sf http://127.0.0.1:8765/health`** — Dienst läuft, antwortet aber nicht? → Port
   belegt oder der Start hängt (z. B. `ProtectSystem`/`ReadWritePaths` verhindert einen
   Git-Commit im `DATA_ROOT`, siehe V9). `journalctl` prüfen.
3. **`tailscale status`** — Node offline? → Uplink oder `tailscaled` selbst prüfen. Das ist
   „deren Infrastruktur", nicht „unser Dienst" — P3 hat hierfür kein Monitoring (Risiko 1).
4. **`tailscale funnel status`** — Funnel aus? → `tailscale funnel --bg 8765`.
5. **`curl -sf https://<node>.<tailnet>.ts.net/health`** — lokal ok, öffentlich nicht?
   → **der dokumentierte Fallstrick:**

   > **`funnel status` sagt „on", aber öffentlich hängt der TLS-Handshake.** Symptom: aus dem
   > Tailnet antwortet `curl` sofort, von außen bleibt die Verbindung nach dem ClientHello
   > stehen. Ursache in fast allen berichteten Fällen: das **`funnel`-Attribut fehlt im
   > `nodeAttrs`-Block des Tailnet-Policy-Files**. Der lokale Status weiß davon nichts — er
   > zeigt „on", weil der lokale Teil der Konfiguration korrekt ist.

6. **`journalctl -u sharefyx-mcp --since -1h | grep '"status":401' | wc -l`** — reines
   Rauschen (Scanner, altes Bookmark) oder ein tatsächlich falsches/rotiertes Token, das ein
   `systemctl restart` vergessen hat (P3-M)?

`[VERIFY]`: Schritt 4/`diagnose.sh`s Grep-Muster gegen `tailscale funnel status` ist bisher
**nicht** gegen ein echtes Tailscale auf dieser VM geprüft (Tailscale fehlt, siehe
„Umgebungsstand" oben) — beim ersten echten Lauf in Step 7 verifizieren, bei Abweichung
`diagnose.sh` korrigieren.

### Cloudflare-Rückbau (führt der Nikinger aus, nicht Claude Code)

`cloudflared` ist auf dieser VM installiert (Step 0 C: `/usr/local/bin/cloudflared`, kein
systemd-Service — nur die manuelle P2-Quick-Tunnel-Nutzung). Zwei parallele Wege nach außen sind
ein Diagnoseproblem, kein Fallback (Plan §4 Step 6). Deinstallation ist eine destruktive Aktion
auf der realen Maschine, außerhalb des Repos — deshalb hier nur der Befehl, nicht ausgeführt:

```bash
sudo rm -f /usr/local/bin/cloudflared
# Falls Weg A (apt-Repo) benutzt wurde statt des Einzel-Binaries:
#   sudo apt remove cloudflared
#   sudo rm -f /etc/apt/sources.list.d/cloudflared.list /usr/share/keyrings/cloudflare-main.gpg
```

Cloudflare Named Tunnel bleibt als dokumentierter Ausweichweg bestehen (`phase2_mcp/CLAUDE.md`)
— dieser Rückbau betrifft nur den installierten `cloudflared`-Client, nicht die Doku-Option.

### „Inbetriebnahme" (einmalig, führt der Nikinger aus, nicht Claude Code)

Claude Code liefert diese Befehlsfolge und wertet die Ergebnisse aus; alles, was den echten
`DATA_ROOT`, den echten Keyring, echte Token oder die Claude-Accounts berührt, führt der
Nikinger selbst aus (Plan §4 Step 7). Angepasst an das tatsächlich Gebaute — vier Variablen in
`local.env` (nicht mehr), zwei Backup-Units, `diagnose.sh` als Vorab-Check.

```
# 0) Tailnet-Voraussetzungen (Tailscale Admin-Konsole, einmalig)
#    MagicDNS an · HTTPS-Zertifikate an · nodeAttrs: "funnel" für diesen Node
tailscale status                       # Node-Name und Tailnet-Name notieren

# 1) Funnel dauerhaft einschalten
tailscale funnel --bg 8765
tailscale funnel status                # muss den Node-Namen und Port 443 zeigen

# 2) Konfiguration eintragen
cp phase3_edge/local.env.example phase3_edge/local.env
#    REPO_ROOT, DATA_ROOT, VENV, ALLOWED_HOSTS=<node>.<tailnet>.ts.net

# 3) Token für beide Spaces ausgeben (je einmal anzeigen, sicher notieren)
python phase2_mcp/scripts/issue_token.py --space niklas
python phase2_mcp/scripts/issue_token.py --space fabian

# 4) Space-Map verschlüsselt bereitstellen — ohne Klartext auf Platte
sudo mkdir -p /etc/sharefyx
python phase3_edge/scripts/export_space_map.py \
  | sudo systemd-creds encrypt --name=spaces - /etc/sharefyx/spaces.cred
sudo chmod 600 /etc/sharefyx/spaces.cred

# 5) Units installieren und starten (sharefyx-mcp + die beiden Backup-Units aus Step 5)
sudo phase3_edge/scripts/install_units.sh
systemctl status sharefyx-mcp
sudo systemctl enable --now sharefyx-backup.timer

# 6) Vorab-Diagnose, bevor von außen getestet wird
phase3_edge/scripts/diagnose.sh

# 7) Erreichbarkeit
curl -s http://127.0.0.1:8765/health
curl -s https://<node>.<tailnet>.ts.net/health

# 8) Connector in beiden Accounts
#    https://<node>.<tailnet>.ts.net/mcp/<token>
```

**Abnahmematrix** — jede Zeile mit Beleg (Ausgabe oder Screenshot **ohne Token**):

| # | Prüfung | Erwartung |
|---|---|---|
| 1 | `/health` von außen | `{"status":"ok",…,"uptime_s":…}` |
| 2 | Connector `niklas` | Ein Read und ein Write erfolgreich |
| 3 | Connector `fabian` | Ein Read und ein Write erfolgreich, **eigener Space** |
| 4 | Cross-Space | `fabian` sieht `niklas` gewrappt und darf dort nicht schreiben |
| 5 | `list_spaces` bei leerem `fabian` | Eigener Space erscheint mit `item_count: 0` (B1-Fix, P2) |
| 6 | **Reboot-Test** | VM neu starten, ohne Handgriff: Connector funktioniert, URL unverändert |
| 7 | **Kill-Test** | `sudo systemctl kill -s KILL sharefyx-mcp` → binnen 10 s wieder `ok` |
| 8 | Request-Log | `journalctl -u sharefyx-mcp` zeigt je Tool-Aufruf Name, Space, `ms` |
| 9 | **Token-Grep** | `journalctl -u sharefyx-mcp --since <Start> \| grep -F "<token>"` → **leer** |
| 10 | Titel-Grep | Ein Item mit markantem Titel anlegen, danach im Log suchen → **leer** |
| 11 | Fremdzugriff | `curl https://<host>/mcp/falsch` → 401, Logzeile mit `<redacted>` |
| 12 | Backup-Timer | `systemctl list-timers sharefyx-backup` zeigt einen Lauf |
| 13 | **Restore-Nachweis** | `restore_check.sh` grün, HEAD identisch |
| 14 | Größenbudget | `search_items` gegen den echten Bestand — geerbtes `[VERIFY]` V8 aus P2 |

**Abschluss, in dieser Reihenfolge:**
1. Beide Token rotieren (`--revoke` + neu), exportieren, `systemctl restart`, Connector-URLs in
   beiden Accounts aktualisieren (P3-M — README.md, Abschnitt „Rotation im Dienstbetrieb").
2. Abnahmeprotokoll `docs/concepts/P3_ABNAHME_<YYYY-MM-DD>.md` mit L1-Card, Prüfmatrix, Belegen
   und Indexzeile — Konvention aus P2 (`P2_ADAPTER_ABNAHME_2026-07-26.md`).
3. `ROADMAP.md` P3 auf ✅, `docs/INDEX.md` und dieser Phase-Head nachziehen.

**Offene `[VERIFY]`, die nur unter echter Infrastruktur schließen:** V9 (`ProtectHome=read-only`
+ `ReadWritePaths` erlaubt Git-Commits im `DATA_ROOT`) und `diagnose.sh` Prüfung 4s Grep-Muster
gegen `tailscale funnel status` (nie gegen ein echtes Tailscale getestet, siehe „Umgebungsstand").

---

## Session stopped — 2026-07-27 (Live-Abnahme im Gang, für kalten Leser: 8/14 belegt, keine offenen Bugs)

**Für den nächsten, kalten Leser (Mensch oder Claude): das Wichtigste zuerst.** B3 und B4 sind
**behoben und in Produktion bestätigt** — `systemctl status sharefyx-backup.service` zeigt
für **beide** `ExecStart`-Prozesse `status=0/SUCCESS`. Die drei `FEHLER`-Zeilen im letzten
`abnahme_run.sh`-Lauf (#8, #12, #13) sind **keine neuen Bugs** — sie erklären sich vollständig
aus der Art, wie der Lauf aufgerufen wurde (siehe unten). Nicht erneut debuggen, nur korrekt
aufrufen.

**Woher das kommt:** dieselbe Session hat P3 Steps 0–6 gebaut (Commits `eb2038a`…`b228bcd`),
dann live gegen die echte VM abgenommen (Commits `7368f57` B3, `d05464e` B4). Ein **zweiter,
paralleler** Claude-Chat hat `phase3_edge/scripts/abnahme_run.sh` (Test-Runner) und
`docs/concepts/P3_ABNAHME_2026-07-27.md` (Protokollvorlage) geschrieben — beide geprüft
(kein Prompt-Injection-Risiko, kein `sudo`-Missbrauch), beide noch **uncommitted**, gehören
nicht dieser Session.

**Ehrlicher Stand der 14 Abnahmezeilen** (Plan §4 Step 7 / `phase3_edge/CLAUDE.md` Runbook):

| # | Zeile | Status | Beleg |
|---|---|---|---|
| 1 | `/health` außen | ✅ | mehrfach bestätigt, `uptime_s` vorhanden |
| 2 | Connector `niklas` R+W | ✅ | `itm_53cf4e92`/`itm_cc4866f3` real angelegt — kein sauberer Einzel-Lauf-Beleg |
| 3 | Connector `fabian` R+W | ⬜ | **noch nicht gemacht** |
| 4 | Cross-Space | ⬜ | **noch nicht gemacht** |
| 5 | `list_spaces` leerer `fabian` | ⬜ | **noch nicht gemacht** |
| 6 | Reboot-Test | ⬜ | Nikinger: „noch nicht möglich" (Stand vor dieser Notiz) |
| 7 | Kill-Test | ✅ | `abnahme_run.sh --with-kill`-Lauf: „wieder gesund", `uptime_s: 4` |
| 8 | Request-Log | ✅ **funktional**, ⬜ **im Skript unbewiesen** | 3 echte `"ev":"tool"`-Zeilen direkt im Journal gefunden (`list_spaces`, 2× `create_item`) — liegen nur außerhalb des `--since`-Fensters, weil Tests 2–5 nie unmittelbar vor einem `run` gemacht wurden |
| 9 | Token-Grep | ✅ | mehrfach leer |
| 10 | Titel-/Body-Grep | ✅ | mehrfach leer |
| 11 | Fremdzugriff → 401 | ✅ | 401 + `<redacted>` im Log |
| 12 | Backup-Timer | ⬜ **echt offen** | Timer nie selbst ausgelöst (nur der Service manuell) — `LastTriggerUSec` bleibt leer, bis der Timer selbst feuert (`NEXT` laut `list-timers`: 2026-07-28 00:04:56 CEST, `RandomizedDelaySec=900`) |
| 13 | Restore-Nachweis | ✅ **mechanisch bewiesen**, Skript-Check zeigt trotzdem FEHLER | `systemctl status` zweifelsfrei `status=0/SUCCESS` für `restore_check.sh` — `abnahme_run.sh`s **eigener** Default für `SHAREFYX_BACKUP_DIR` ist noch `/var/backups/sharefyx` (alt), nicht `/var/lib/sharefyx-backup` (B3-Fix); ohne `export SHAREFYX_BACKUP_DIR=/var/lib/sharefyx-backup` findet der Skript-Check das Bundle nicht — das Skript gehört nicht dieser Session, wurde bewusst nicht selbst editiert |
| 14 | Größenbudget | ⬜ | optional, noch nicht angefasst |

**Für den nächsten sauberen Lauf, in dieser Reihenfolge:**

```bash
export SHAREFYX_HOST=savefyx-vmware-virtual-platform.tail89fc2a.ts.net
export SHAREFYX_DATA_ROOT=/home/savefyx/savefyx-data
export SHAREFYX_BACKUP_DIR=/var/lib/sharefyx-backup   # B3-Fix — abnahme_run.sh kennt den neuen Pfad nicht selbst
./phase3_edge/scripts/abnahme_run.sh start
# → JETZT sofort, ohne Pause: Connector-Tests 2–5 fahren (niklas UND fabian, Cross-Space,
#   list_spaces bei leerem fabian) — das füllt gleichzeitig #2–#5 UND liefert die Tool-Events,
#   die #8 im richtigen Zeitfenster braucht
sudo -E ./phase3_edge/scripts/abnahme_run.sh run --with-kill | tee /tmp/p3-abnahme.txt
```

Danach bleibt real nur noch offen: #6 (Reboot, Nikinger-Zeitfrage), #12 (Timer muss selbst
feuern — warten oder als „Mechanismus bewiesen, Zeitplan nicht" akzeptieren, siehe §4 des
Protokolls), #14 (optional). Ergebnis in `docs/concepts/P3_ABNAHME_2026-07-27.md` §3.1 kleben,
dann an diese Session zurückgeben — Abschluss (Token-Rotation, Protokoll fertigstellen,
`ROADMAP.md`/`docs/INDEX.md`/dieser Phase-Head auf ✅) ist der letzte Schritt.

**Nächster Schritt (konkret):** wie oben — sauberer Lauf, dann zurück an Claude Code für den
Abschluss.
