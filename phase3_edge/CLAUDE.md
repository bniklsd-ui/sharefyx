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
updated: 2026-07-28
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

## Session stopped — 2026-07-28 (Token-Rotation live bestätigt, Abschluss-Punkte erledigt)

**Für den nächsten, kalten Leser:** direkte Fortsetzung des vorigen Blocks vom 2026-07-27 —
der Nikinger hat die dort skizzierte Rotationsfolge (niklas zuerst, dann fabians Erstausgabe)
selbst ausgeführt und die Session neu geladen. Diese Session hat nur noch die Bestätigung
und den Abschluss-Aufräumschritt gemacht, keine neuen Findings.

**Was passiert ist:**
1. Der Nikinger hat alle vier Rotationsschritte (Revoke+Issue, Export, `systemd-creds
   encrypt`, `systemctl restart`) für niklas und für fabians erste reguläre Ausgabe
   ausgeführt, danach die Connector-URLs in beiden Claude-Accounts aktualisiert (neue
   Adapter-Namen: `phase_3_final_niklas_sharefyx`, `phase_3_final_sharefyx_fabian`) und die
   Session neu geladen.
2. Beide neuen Connectors live gegen `list_spaces` geprüft: niklas sieht `{fabian:
   item_count 1, writable:false}` + `{niklas: item_count 5, writable:true}`; fabian sieht
   das Spiegelbild. Rule 4 (fremd sichtbar, fremd nicht schreibbar) hält nach der Rotation
   unverändert. Für niklas ist das die geprüfte Tiefe (`list_spaces`, `writable:true` korrekt
   gesetzt); ein echter Write über den neuen niklas-Connector wurde diese Session nicht
   zusätzlich gefahren — derselbe Principal-Resolution-Pfad wie beim fabian-Write unten, aber
   nicht separat belegt.
3. `itm_2dda3690` (fabian-Testitem, zuletzt Beleg für Zeile 5) über den neuen fabian-Connector
   archiviert (`update_item`, `status: archived`, v1→v2 — ein echter Write, geprüft) — der
   temporäre `sharefyx_phase_3_fabian`-Adapter ist damit vollständig durch die reguläre Ausgabe
   ersetzt, keine offenen Wegwerf-Items mehr.

**Damit erledigt aus der „noch offen"-Liste des vorigen Blocks:** Token-Rotation aller drei
Token, Archivierung von `itm_2dda3690`, Ablösung des temporären Connectors. **Weiterhin offen,
unverändert:** Zeile 6 (Reboot, passive Beobachtung), Zeilen 12/13 (nächste Phase, siehe B5),
Zeile 14 (optional, V8 geerbt).

**Nächster Schritt (konkret):** nichts Aktives mehr für P3 — abwarten, bis ein echter Reboot
(geplant oder Vorfall) beobachtet wird, dann Zeile 6 nachtragen und `ROADMAP.md`/Phase-Head/
Index von 🟡 auf ✅ heben. Bis dahin bleibt P3 funktional beendet, aber nicht live-verifiziert
im Sinne der Statusglyphen-Definition.
