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

## Session stopped — 2026-07-27 (Step 6: Runbooks, `diagnose.sh`, Cloudflare-Rückbau)

**Ergebnis:** Step 6 abgeschlossen. `phase3_edge/scripts/diagnose.sh` (sechs Prüfungen,
degradiert sauber), Runbook „Connector zeigt Disconnected" + „Cloudflare-Rückbau" +
„Inbetriebnahme"-Platzhalter im Phase-Head. `phase2_mcp/CLAUDE.md`s Quick-Tunnel-Runbook durch
einen Verweis ersetzt.

**`diagnose.sh` real auf dieser VM gelaufen (read-only, kein Schreibzugriff):** Ergebnis —
Prüfung 1 (`systemctl is-active sharefyx-mcp`) schlägt korrekt fehl, weil die Unit hier noch
nicht installiert ist (Step 7). Ausgabe: `DIAGNOSE: sharefyx-mcp ist nicht aktiv (oder nicht
installiert). NÄCHSTER SCHRITT: journalctl -u sharefyx-mcp -n 50`, Exit 1. Das ist ein
korrekter, sauberer Abbruch — **nicht** das im Plan beschriebene „läuft durch, auch mit
absichtlich gestopptem Dienst" (dafür bräuchte es einen tatsächlich laufenden und dann gestoppten
Dienst). Die vollständige Prüfung aller sechs Schritte gegen einen echten, installierten Dienst
verschiebt sich damit explizit nach Step 7 — hier festgehalten, nicht stillschweigend als „Done"
gemeldet.

**`[VERIFY]` neu, benannt statt verschwiegen:** Prüfung 4s Grep-Muster gegen
`tailscale funnel status` (`"127.0.0.1:8765"`) beruht auf Tailscales dokumentiertem
Ausgabeformat, war aber auf dieser VM nie gegen ein echtes Tailscale zu verifizieren (Tailscale
fehlt seit Step 0). Erster echter Test in Step 7; bei Abweichung `diagnose.sh` dort korrigieren,
nicht den Fund hier überschreiben.

**Check 6s Grep-Muster (`'"status":401'`) passt zum echten `AccessLogASGI`-Output** — geprüft
gegen `request_log.py`s kompaktes `json.dumps(..., separators=(",", ":"))` (kein Leerzeichen
nach dem Doppelpunkt), nicht nur angenommen.

**Cloudflare-Rückbau ist ein Runbook-Eintrag, keine ausgeführte Aktion (Advisor-Vorgabe,
dieselbe Klasse wie `install_units.sh`):** `cloudflared` ist auf dieser VM installiert
(Step 0 C), aber die Deinstallation ist destruktiv und außerhalb des Repos — der Befehl steht im
Phase-Head-Runbook, der Nikinger führt ihn selbst aus.

**`phase2_mcp/CLAUDE.md` — Quick-Tunnel-Runbook ersetzt, nicht gelöscht:** die historischen
Abschnitte „Live-Stand"/„Sicherheitsvorfall" standen bereits vollständig in
`docs/concepts/P2_ADAPTER_ABNAHME_2026-07-26.md` und im archivierten P2-Step-7-Session-Block
(`phase2_mcp/SESSIONS_ARCHIVE.md`) — kein Informationsverlust durch das Kürzen. Die
Überschrift behält bewusst den Wortlaut „Quick-Tunnel-Probe", damit der bestehende Verweis
weiter oben im selben Dokument („Runbook „Quick-Tunnel-Probe" oben") gültig bleibt, statt eine
zweite Textstelle mitziehen zu müssen. Ersetzt durch einen dreiteiligen Verweis (P2-Nachweis,
P3-Betriebsweg, Verweis `phase3_edge/CLAUDE.md`) plus einem eigenen Absatz zu Cloudflare Named
Tunnel als dokumentiertem Ausweichweg — wie im Plan gefordert.

**Größenänderung:** `phase2_mcp/CLAUDE.md` von ~23KB auf ~19KB (Kürzung um die Cloudflare-
Voraussetzungen), `docs/INDEX.md`-Zeile nachgezogen.

**Tests:** keine neuen — Plan sieht für Step 6 keine automatisierten Tests vor (Runbook-Text und
ein Bash-Skript, das gegen eine echte Infrastruktur läuft). `.venv/bin/python -m pytest -q` →
**168/168 grün**, unverändert gegenüber Step 5 (Kontrollzahl, keine Regression durch die
Doku-Änderungen).

**Modul-Status oben nachgezogen** (Zeile 7: ⬜ → ✅, 0 Tests — begründet).

**Offen für den Nikinger, vor Step 7 zu klären (Zusammenfassung, unverändert seit früheren
Steps, hier gebündelt vor dem Abschlussbericht):**
1. `mcp_smoke.py`/P3-N-Grenzfrage (Step 2) — `logging.basicConfig` → `configure_logging`
   umstellen oder nicht.
2. Tailscale-Installation + Tailnet-Voraussetzungen (Step 0) — einziges echtes Gate vor Step 7.
3. Cloudflare-Rückbau (dieser Step) — Befehl steht im Runbook, Ausführung ist Sache des
   Nikingers.

**Nachtrag zu diesem Block (Advisor-Fund, nach dem ursprünglichen Commit ergänzt):** der
„Inbetriebnahme"-Runbook-Abschnitt oben war noch der leere Platzhalter aus Step 0/1 —
nachgezogen mit der vollständigen Befehlsfolge und der 14-Zeilen-Abnahmematrix aus Plan §4
Step 7, angepasst an das tatsächlich Gebaute (vier `local.env`-Variablen, zwei Backup-Units,
`diagnose.sh` als Vorab-Check vor Schritt 7). Ohne diese Ergänzung hätte der Nikinger für Step 7
den 46KB-Plan öffnen müssen, obwohl der Phase-Head genau dafür da ist. Reine Doku-Ergänzung,
kein Code, keine neuen Tests — `pytest` bleibt bei 168/168.

**Nächster Schritt (konkret):** Step 7 — Live-Abnahme. Läuft komplett beim Nikinger gegen die
echte Infrastruktur; Claude Code liefert die Befehlsfolge aus dem Plan und wertet die
Ergebnisse aus, führt aber nichts davon selbst aus (echter `DATA_ROOT`, echter Keyring, echte
Token, echte Claude-Accounts).

**[2026-07-27, während der Live-Abnahme] Fund B3, behoben — `sharefyx-backup.service` scheiterte
real auf der VM:** `mkdir: cannot create directory '/var/backups/sharefyx': Permission denied`.
Ursache: der Dienst läuft als unprivilegierter `User=savefyx`; `/var/backups` gehört auf
Debian/Ubuntu root und ist für andere Nutzer nicht beschreibbar. Kein Unit-Test hat das
gefangen, weil `test_units.py` reines Textparsen ist und nie einen echten systemd-Prozess unter
echtem `User=`-Sandbox startet — genau die Klasse Fund, die laut Plan nur unter echter
Infrastruktur (V9-Nachbarschaft) sichtbar wird.

**Behoben:** `phase3_edge/systemd/sharefyx-backup.service` benutzt jetzt `StateDirectory=
sharefyx-backup` statt eines literalen `/var/backups/sharefyx`. systemd legt
`/var/lib/sharefyx-backup` bei **jedem** Start selbst an, bereits mit der richtigen
Eigentümerschaft (`User=`/`Group=` des Dienstes) — kein manuelles `chown`, auf keiner Maschine,
jemals nötig (dieselbe Maschinenunabhängigkeits-Logik wie bei den vier `local.env`-Variablen).
`SHAREFYX_BACKUP_DIR` zeigt entsprechend jetzt auf `/var/lib/sharefyx-backup` statt
`/var/backups/sharefyx` — `/var/lib` ist ohnehin die FHS-korrekte Konvention für
dienst-verwaltete Zustandsdaten, `/var/backups` eher für administrator-initiierte Backups mit
Root-Rechten gedacht.

**Auf der VM anzuwenden:** `sudo phase3_edge/scripts/install_units.sh` erneut laufen lassen
(re-templated die Unit, `daemon-reload`, `sharefyx-mcp` erneut `enable --now` — unschädlich,
bereits laufend), danach `sudo systemctl start sharefyx-backup.service` erneut versuchen.

**Nebenbefund, nicht behoben (gehört nicht mir):** `phase3_edge/scripts/abnahme_run.sh` — vom
Nikinger über eine parallele Claude-Sitzung geschrieben, nicht Teil dieser Session — hat
weiterhin `/var/backups/sharefyx` als Default für `SHAREFYX_BACKUP_DIR` (Zeile 27). Beim nächsten
Lauf `SHAREFYX_BACKUP_DIR=/var/lib/sharefyx-backup` explizit exportieren, sonst findet Test 13
das neue Bundle nicht. Bewusst nicht eigenmächtig editiert — das Skript gehört einer anderen
Sitzung, die den Nikinger direkt informiert bekommt.

**Tests:** keine Änderung nötig, `.venv/bin/python -m pytest -q` → weiterhin **168/168 grün**
(kein Test prüfte den literalen Pfadwert, nur Secret-Shape und `/home/savefyx`-Freiheit).
