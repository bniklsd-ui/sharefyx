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
| 8 | Live-Abnahme (Nikinger) | 7 | 🔄 in Arbeit — 7/13 Pflichtzeilen belegt (Zähler ohne optionale Zeile 14, keine Regression ggü. „8/14"), B3+B4 behoben, B5+B6 dokumentiert, V9 live geschlossen | — |

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

**Offene `[VERIFY]`, die nur unter echter Infrastruktur schließen:** `diagnose.sh` Prüfung 4s
Grep-Muster gegen `tailscale funnel status` (nie gegen ein echtes Tailscale getestet, siehe
„Umgebungsstand"). **V9 geschlossen** (2026-07-27, zweite Live-Abnahme-Session):
`ProtectHome=read-only` + `ReadWritePaths` erlaubt Git-Commits im `DATA_ROOT` — live bestätigt,
der `append_to_item`-Aufruf aus Zeile 2 der Abnahme erzeugte exakt zeitgleich (20:39:58) den
Top-Commit `a400221c` im `DATA_ROOT`. Details: `docs/concepts/P3_ABNAHME_2026-07-27.md` Befund B5.

---

## Session stopped — 2026-07-27 (zweite Session, sauberer Lauf gefahren: 7/13, zwei neue Befunde B5+B6, kein neuer Bug)

**Für den nächsten, kalten Leser:** dieser Block folgt direkt auf den vorigen vom selben Tag
(2026-07-27) — der vorige stammt aus der Session, die P3 Steps 0–6 gebaut und B3/B4 live
gefunden/behoben hat; dieser hier ist eine neue, separate Session, die den "sauberen Lauf" aus
dem vorigen Block nachgeholt hat. Ergebnis: **kein neuer Bug**, aber zwei neue Befunde (B5, B6),
die die restlichen Lücken erklären. Volles Protokoll:
`docs/concepts/P3_ABNAHME_2026-07-27.md` (jetzt mit echten Belegen statt Platzhaltern).

**Was diese Session gemacht hat, in Reihenfolge:**
1. `abnahme_run.sh start` gesetzt (Startzeitpunkt für `--since`).
2. Zeile 2 (Connector niklas Read+Write) **selbst** über die in dieser Session verfügbaren
   MCP-Connector-Tools gefahren (`savefyx_pashe_3_test`-Adapter) — echter `get_item` +
   `append_to_item` auf dem bestehenden Testitem `itm_53cf4e92` (v1→v2), kein neues Item
   angelegt. Vorher per `search_items` geprüft, dass die Testitems aus der vorigen Session noch
   da sind (`itm_53cf4e92`, `itm_cc4866f3`) — Wiederverwendung statt Duplikat, wie vom Nikinger
   angewiesen.
3. `abnahme_run.sh run </dev/null` (kein `--with-kill`: Zeile 7 bereits bestanden, außerdem
   kein passwordless sudo in dieser Shell verfügbar — der Nikinger hat beides bestätigt/für
   unnötig erklärt) gegen den echten Host gefahren.

**Ehrlicher Stand nach diesem Lauf** (Details + CLI-Beleg: `P3_ABNAHME_2026-07-27.md` §2/§3):

| # | Zeile | Status | Delta zum vorigen Block |
|---|---|---|---|
| 1 | `/health` außen | ✅ | unverändert |
| 2 | Connector niklas R+W | ✅ | **jetzt sauber belegt** (v1→v2, echter Aufruf aus dieser Session) statt nur behauptet |
| 3 | Connector fabian R+W | ⬜ | unverändert — **B6: kein fabian-Connector in dieser Session** |
| 4 | Cross-Space | ⬜ | unverändert — B6, muss **nach** Zeile 5 kommen (Reihenfolge!) |
| 5 | `list_spaces` leerer fabian | ⬜ | unverändert — B6, muss **vor** Zeile 3 kommen |
| 6 | Reboot-Test | ⬜ | unverändert — Nikinger |
| 7 | Kill-Test | ✅ | unverändert (bewusst nicht wiederholt) |
| 8 | Request-Log | ✅ | **jetzt vollständig belegt** — 3 echte Tool-Ereignisse im `--since`-Fenster (`get_item`, `append_to_item`, `search_items`), keine Zeitfenster-Lücke mehr |
| 9 | Token-Grep | ✅ | Beleg weiter aus dem 09:xx-Lauf, bewusst nicht wiederholt (kein Token in diesen Prozess füttern) |
| 10 | Titel-/Body-Grep | ✅ | frisch bestätigt, leer |
| 11 | Fremdzugriff → 401 | ✅ | frisch bestätigt |
| 12 | Backup-Timer | ⬜ **real offen** | unverändert — `LastTriggerUSec` leer, Timer feuert erst `2026-07-28T00:00:35` (`RandomizedDelaySec=900`); auf Nikinger-Entscheidung **akzeptiert, nicht abgewartet** |
| 13 | Restore-Nachweis | ❌ **neu, aber kein Bug — B5** | Skript-Check schlägt heute fehl, weil das einzige Bundle (11:12 UTC) älter ist als der aktuelle HEAD (u. a. durch Zeile 2 selbst) — Mechanismus war unmittelbar nach diesem Bundle bereits `status=0/SUCCESS` (voriger Block). Löst sich von selbst, sobald der Timer heute Nacht ein frisches Bundle zieht und der Check direkt danach läuft, ohne dazwischenliegende Schreibvorgänge |

**Nebenbefund (B6, Details im Protokoll):** `list_spaces` auf dem `niklas`-Token zeigt `fabian`
nicht einmal als fremden, lesbaren Space — nur `niklas` selbst. Erwartbar (fabian ist der Space
des Kollegen, eigener Connector in dessen eigenem Account, R2), aber `[VERIFY]` wert gegen Hard
Rule 4 / `tools.py`-Sichtbarkeitslogik bei Gelegenheit — außerhalb der P3-Berührungsfläche
(P3-N), hier nur notiert, nicht geprüft oder angefasst.

**Was noch offen ist, für den nächsten Schritt:**
- Zeilen 3–5 (fabian) — **nur der Nikinger**, in dessen eigenem Claude-Account mit
  fabian-Connector. Reihenfolge zwingend: **5 → 4 → 3** (fabian muss beim `list_spaces`-Test
  noch leer sein; Zeile 3 schreibt hinein).
- Zeile 6 (Reboot) — Nikinger-Zeitfrage, unverändert.
- Zeile 12 (Backup-Timer) — bewusst akzeptiert, nicht abgewartet (Nikinger-Entscheidung
  2026-07-27). Zeile 13 löst sich vermutlich mit demselben Timer-Lauf von selbst, wurde aber
  nicht eigens abgewartet.
- Zeile 14 (optional, Größenbudget) — weiterhin nicht angefasst.
- `phase3_edge/scripts/abnahme_run.sh` und `docs/concepts/P3_ABNAHME_2026-07-27.md` sind
  **weiterhin nicht von dieser Session verfasst** — diese Session hat nur den vom Nikinger
  autorisierten Teil editiert (Ausfüllen von §1–§4 im Protokoll mit echten Belegen). Das Skript
  selbst wurde nicht angefasst; der bekannte `SHAREFYX_BACKUP_DIR`-Default-Fehler (`/var/backups/
  sharefyx` statt `/var/lib/sharefyx-backup`) besteht im Skript weiterhin, wurde aber diesmal
  per Environment-Variable umgangen.
- Commit dieser Änderungen (dieser Head, `docs/INDEX.md`, das Abnahmeprotokoll) steht noch aus —
  bewusst zurückgestellt bis zur Rückmeldung des Nikinger, da Zeilen 3–6 und 12 real offen
  bleiben und der Abschluss (Token-Rotation, `ROADMAP.md`/Index/Head auf ✅) erst nach Zeilen
  3–6 sinnvoll ist.

**Nächster Schritt (konkret):** Nikinger fährt Zeilen 5→4→3 im fabian-Connector und Zeile 6
(Reboot) nach eigenem Zeitplan; danach zurück an Claude Code zum Eintragen in
`P3_ABNAHME_2026-07-27.md` und für den Abschluss (Token-Rotation, Testitems archivieren,
`ROADMAP.md`/`docs/INDEX.md`/dieser Phase-Head auf ✅, alles im selben Commit wie die
Doc-Aktualisierung, Hard Rule 8).
