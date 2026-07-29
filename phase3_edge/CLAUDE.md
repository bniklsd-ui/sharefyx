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
updated: 2026-07-29
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
| 8 | Live-Abnahme (Nikinger) | 7 | 🟡 funktional beendet — 10/13 live, Zeilen 6/12/13 auf nächste Phase verschoben (Nikinger-Entscheidung 2026-07-27), B3–B6 dokumentiert, V9 live geschlossen, Token-Rotation live bestätigt (2026-07-28); ✅ erst nach beobachtetem echtem Reboot | — |

**[2026-07-29 Korrektur, P4 Step 7]:** Zeile 5 nennt „systemd-Units" — `sharefyx-mcp.service`
ist davon inzwischen nicht mehr eine. Die MCP-Unit zog nach `phase4_auth/systemd/` um (Plan §5
Step 7: „ERSETZT die P3-Fassung", inhaltlich jetzt eine P4-Unit — `StateDirectory`, zweites
Credential für die Auth-Nutzerakten, zwei neue `Environment=`-Zeilen für `SPACE_AUTH_MODE`/
`SPACE_PUBLIC_BASE_URL`). Die beiden Backup-Units (`sharefyx-backup.service`/`.timer`, Zeile 6)
bleiben unverändert unter `phase3_edge/systemd/`. `install_units.sh` bleibt P3-Eigentum, liest
jetzt aber aus **beiden** Verzeichnissen (`phase3_edge/local.env.example` um `AUTH_MODE`/
`PUBLIC_BASE_URL` ergänzt). `phase3_edge/tests/test_units.py` folgt dem neuen Pfad — keine
Test-Semantik geändert, nur der Quellort; die historischen Zähl-Zeilen 5/6 oben bleiben
unangetastet (dieselbe Regel wie in `phase2_mcp/CLAUDE.md`s Korrekturen: nur die driftende
Aussage wird korrigiert, nicht die abgeschlossene Historie umgeschrieben). Details, Session-Block
in `phase4_auth/CLAUDE.md`.

**[2026-07-29 Korrektur, Reboot passiv beobachtet]:** Zeile 6 der Abnahmematrix (`docs/concepts/
P3_ABNAHME_2026-07-27.md` §2, „nach `sudo reboot` ohne Handgriff erreichbar, URL unverändert")
ist jetzt ✅ — der Windows-Host des Nikingers ist neu gestartet, die VM lief als Gast mit und
rebootete unbeabsichtigt mit (genau der reale Vorfall, den die Nikinger-Entscheidung vom
2026-07-27 als Prüffall vorgesehen hatte, kein `sudo reboot`). Belege, alle read-only erhoben,
kein Handgriff nötig: `uptime -s` → Boot 2026-07-29 07:20:45; `systemctl is-enabled
sharefyx-mcp.service` → `enabled`; `ActiveEnterTimestamp` 07:20:51 (6 s nach Boot, ohne
Nikinger-Zutun); `journalctl -b -u sharefyx-mcp.service` zeigt echten MCP-Tool-Traffic um 07:57
und 08:02 (Status 200/202) — der Dienst hat nach dem Reboot echte Arbeit gemacht, nicht nur
`active` gemeldet; Funnel-URL identisch zu der in `P3_ABNAHME_2026-07-27.md` Zeile 84 notierten
(`savefyx-vmware-virtual-platform.tail89fc2a.ts.net`); `curl -sf .../health` → `HTTP 200`,
live zum Zeitpunkt dieser Korrektur. Die installierte Unit war zu diesem Zeitpunkt noch die
P3-Fassung (der P4-Step-7-Umzug nach `phase4_auth/systemd/` ist uncommitted, nicht installiert)
— genau die Unit, die Zeile 6 prüfen soll, also gültiger Beleg, nicht der neuen Fassung
zuzuschreiben. `docs/concepts/P3_ABNAHME_2026-07-27.md` bleibt als 📕-Snapshot unangetastet
(dokumentiert nur den Stand ihrer eigenen Session); dieser Fund lebt hier plus im neuen
Session-Block unten. Zusammen mit Zeile 12 (P4 Step 0, siehe oben) sind jetzt **12 von 13**
Abnahmezeilen live bestanden — einzig Zeile 13 (Restore-Nachweis, braucht ein frisches Bundle)
blockiert noch den Wechsel von 🟡 auf ✅. `ROADMAP.md`, Root-`CLAUDE.md` und `docs/INDEX.md`
im selben Commit nachgezogen.

## Umgebungsstand (Step 0, Details im Archiv)

Vier Fakten, die spätere Steps direkt gaten — volle Inventartabelle in `SESSIONS_ARCHIVE.md`:

- venv für `ExecStart` (V6): `/home/savefyx/dev/savefxy/.venv/bin/python`.
- `fastmcp` **3.4.4** bereits installiert — deckt sich mit dem P3-D-Pin, keine Änderung nötig.
- `systemd-creds` vorhanden, `has-tpm2` → partial → `encrypt` läuft über Host-Key statt TPM2 (für
  P3-F ausreichend, siehe Plan-Begründung).
- **Tailscale ist auf dieser VM nicht installiert.** Blockiert nicht Steps 1–6, blockiert
  **Step 7** — Nikinger-Aktion vor der Live-Abnahme (installieren, Tailnet beitreten, MagicDNS +
  HTTPS-Zertifikate an, `nodeAttrs: funnel` im Policy-File). **[2026-07-28 Korrektur, P4 Step
  0]:** Stand aus Step 0, inzwischen falsch — Tailscale ist installiert, der Funnel läuft
  öffentlich (siehe V13 unten).

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

**V13 geschlossen (2026-07-28, P4 Step 0):** `diagnose.sh` einmal komplett gegen das reale
`tailscale funnel status` gelaufen lassen — alle sechs Prüfungen grün, Schritt 4s Grep-Muster
matcht die echte Ausgabe unverändert. Kein Korrekturbedarf am Skript.

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
1. ✅ **Erledigt (2026-07-28).** Alle drei Token rotiert (`--revoke` + neu — für `fabian` war
   das die erste reguläre Ausgabe, kein Vorgänger), exportiert, `systemctl restart`,
   Connector-URLs in beiden Accounts aktualisiert (neue Adapter: `phase_3_final_niklas_sharefyx`,
   `phase_3_final_sharefyx_fabian`) — live gegen `list_spaces` bestätigt. **Vom Nikinger
   ausgeführt** (Keyring + `sudo systemd-creds` + Connector-URLs in den Claude-Accounts).
2. ✅ **Erledigt (2026-07-27).** Abnahmeprotokoll `docs/concepts/P3_ABNAHME_2026-07-27.md` mit
   L1-Card, Prüfmatrix, Belegen und Indexzeile — Konvention aus P2
   (`P2_ADAPTER_ABNAHME_2026-07-26.md`).
3. ✅ **Erledigt (2026-07-27, seither laufend nachgezogen).** `ROADMAP.md` P3 auf 🟡,
   `docs/INDEX.md` und dieser Phase-Head nachgezogen. **Nikinger-Entscheidung 2026-07-27:**
   Zeilen 6/12/13 auf die nächste Phase verschoben statt aktiv nachgeholt (Details:
   Abnahmeprotokoll §1). ✅ erst nach einem beobachteten echten Reboot (Statusglyphen-Definition
   in `ROADMAP.md`: ✅ = „live-verifiziert").

**Offene `[VERIFY]`, die nur unter echter Infrastruktur schließen:** `diagnose.sh` Prüfung 4s
Grep-Muster gegen `tailscale funnel status` (nie gegen ein echtes Tailscale getestet, siehe
„Umgebungsstand"). **V9 geschlossen** (2026-07-27, zweite Live-Abnahme-Session):
`ProtectHome=read-only` + `ReadWritePaths` erlaubt Git-Commits im `DATA_ROOT` — live bestätigt,
der `append_to_item`-Aufruf aus Zeile 2 der Abnahme erzeugte exakt zeitgleich (20:39:58) den
Top-Commit `a400221c` im `DATA_ROOT`. Details: `docs/concepts/P3_ABNAHME_2026-07-27.md` Befund B5.

---

## Session stopped — 2026-07-29 (Zeile 6 passiv erfüllt — unbeabsichtigter Reboot)

**Für den nächsten, kalten Leser:** kein aktiver P3-Arbeitsschritt — diese Session lief in P4
(Step 7, siehe `phase4_auth/CLAUDE.md`), fand aber genau den in der vorigen Notiz erwarteten
Auslöser vor: der Windows-Host des Nikingers startete neu (Absturz/Neustart), die VM als Gast
rebootete unbeabsichtigt mit. Auftrag des Nikingers: nachsehen, ob das die ausstehende
Reboot-Zeile erfüllt, bevor die Journal-Evidenz mit dem nächsten Boot verfällt.

**Was geprüft wurde (alles read-only, kein Handgriff, kein `sudo reboot` nötig):**
1. `uptime -s` / `who -b` → Boot 2026-07-29 07:20:45.
2. `systemctl is-enabled sharefyx-mcp.service` → `enabled`; `systemctl show -p
   ActiveEnterTimestamp,ActiveState,SubState` → aktiv seit 07:20:51, 6 s nach Boot, ohne
   Nikinger-Zutun.
3. `journalctl -b -u sharefyx-mcp.service` → Start um 07:20:51, danach echter Tool-Traffic
   (POST `/mcp/<redacted>`, Status 200/202) um 07:57 und 08:02 — kein bloßes „active", echte
   Nutzung nach dem Reboot.
4. `tailscale funnel status` → `https://savefyx-vmware-virtual-platform.tail89fc2a.ts.net`,
   identisch zur in `P3_ABNAHME_2026-07-27.md` Zeile 84 notierten URL.
5. `curl -sf https://savefyx-vmware-virtual-platform.tail89fc2a.ts.net/health` → `HTTP 200`,
   live zum Prüfzeitpunkt.
6. Zur Einordnung nebenbei geprüft, nicht der eigentliche Auftrag: `systemctl list-timers` zeigt
   `sharefyx-backup.timer` mit echtem `LAST` (2026-07-29 00:13:22) — deckt sich mit der bereits
   in `phase4_auth/CLAUDE.md`/Root-`CLAUDE.md` dokumentierten P4-Step-0-Bestätigung von Zeile 12,
   kein neuer Fund.

**Ergebnis:** Zeile 6 der P3-Abnahmematrix ist damit ✅ — Nikinger-Entscheidung vom 2026-07-27
sah genau diesen unbeabsichtigten Vorfall als Prüffall vor, kein erzwungener `sudo reboot`.
Zusammen mit Zeile 12 (bereits P4 Step 0) stehen jetzt 12/13 Abnahmezeilen. Root-`CLAUDE.md`,
`ROADMAP.md` und `docs/INDEX.md` im selben Commit nachgezogen. `docs/concepts/
P3_ABNAHME_2026-07-27.md` bleibt als 📕-Snapshot unangetastet — die Evidenz lebt hier und in der
Korrekturnotiz oben im Modul-Status-Abschnitt.

**Ausdrücklich nicht behauptet:** dass die neue `phase4_auth/systemd/`-Unit (P4 Step 7,
uncommitted) einen Reboot überlebt hat — installiert war zum Boot-Zeitpunkt noch die P3-Fassung.
Das ist exakt die Unit, die Zeile 6 prüfen soll, also ein gültiger Beleg für P3, aber kein
Beleg für den späteren P4-Unit-Umzug.

**Weiterhin offen, unverändert:** Zeile 13 (Restore-Nachweis, braucht ein frisches Bundle,
siehe B5) — einzige verbleibende Blockade für den Wechsel von 🟡 auf ✅. Zeile 14 (optional, V8
geerbt) unverändert offen.

**Nächster Schritt (konkret):** nichts Aktives für P3 — Zeile 13 löst sich mit einem frischen
Backup-Bundle + `restore_check.sh`-Lauf (Sache einer künftigen Session oder des nächsten
regulären Zyklus, siehe B5). Danach P3 formal auf ✅ heben.
