---
status: live
purpose: Phase-Head Werkzeug-Ergonomie + Bilder — Scope, harte Regeln, Modulstatus, aktueller Session-Handover
read-when: Arbeiten in phase6_5_tools_images/ oder an den in §2 des Plans genannten Dateien in mcpserver/storage/webui — zuerst lesen, zusammen mit dem neuesten Session-stopped-Block
detail: L2
up: ../CLAUDE.md
down:
  - ../docs/concepts/phase6_5_tools_images_plan.md   # voller Plan, Entscheidungen P6.5-A–P6.5-V, §0.0 gelockte N1–N6, Steps 0/A/B
  - ../phase6_shares/IMAGES_PLAN.md                  # Vorgänger-Zusatzplan, nachrangig seit 2026-08-20
  - SESSIONS_ARCHIVE.md                              # ältere Session-Blöcke, newest-first
updated: 2026-08-21 (Live-Deploy bestaetigt: Block A + Block B vollstaendig live, f96125e -- Gate A->B MCP-Rundlauf vom Nikinger freigegeben, noch nicht ausgefuehrt [Connector nicht verdrahtet], siebte Rotation gelaufen)
---
# CLAUDE.md — Phase 6.5: Werkzeug-Ergonomie und Bilder (`phase6_5_tools_images/`)

> Kein eigenes Python-Paket (wie `phase3_edge/`, `phase6_shares/`) — Servercode bleibt in
> `mcpserver`/`storage`/`webui`. **Quelle der Wahrheit ist der Code, nicht dieses Dokument.**

---

## Mission (zuerst lesen)

Zwei Blöcke: **(A)** eine arbeitende Claude-Instanz findet ihre Werkzeuge, versteht deren
Aufgabenteilung aus der Beschreibung und zahlt keine Tausende Token für eine Versionsnummer.
**(B)** ein Bild liegt im Space, ist im Dokument sichtbar, technisch nur ein Link — und Claude
sieht seine Bytes nur, wenn ein Mensch ausdrücklich danach fragt. Unter Druck fällt Block B weg,
nie Block A (reine Beschreibungs-/Tool-Arbeit ohne Datenformatänderung).

## Scope

- **DRIN:** die fünf offenen MCP-Werkzeug-Ergonomie-Punkte (2026-08-14-Live-Feedback),
  Abschluss Block C Bilder (`storage/`-Fundament, `webui`-Routen, MCP-Asset-Tools).
- **DRAUSSEN:** Bulk-Append-Tool, Body-Volltextsuche in der Web-UI, automatische
  `_trash/`-Räumung, Space-Admin-UI (bleibt Phase 7), Rechteverwaltung über MCP-Tools,
  HEIC/SVG/PDF, serverseitiges Bild-Rendering. Volle Liste: Plan §5 „Explizit draußen".

Details, gelockte Entscheidungen P6.5-A–P6.5-V, Berührungsfläche/Tabu-Dateien, Schritt-Sequenz,
Testliste, Abnahmezeilen: `docs/concepts/phase6_5_tools_images_plan.md`.

## Modul-Status

| Block | Inhalt | Status |
|---|---|---|
| Step 0 | Haushalt/Ankündigungen | ✅ |
| Block A (Steps A1/A2/A4; A3 bewusst nicht gebaut, N3) | Werkzeug-Ergonomie (`mcpserver/tools.py`, `storage/store.py :: search(in_body=)`) | ✅ **gebaut, live deployt 2026-08-21** — Gate A→B (echte Connector-Probe) steht weiterhin aus |
| Block B Step B1 | Storage-Fundament Bilder (`storage/{files,store,models}.py`) | ✅ **gebaut, live deployt 2026-08-21** |
| Block B Step B2 | REST-Fläche Bilder (`phase5_ui/webui/{api,serializers}.py`) | ✅ **gebaut, live deployt 2026-08-21** |
| Block B Step B3 | Web-UI Anzeigen/Einfügen (`phase5_ui/webui/static/{app.html,app.css,js/{markdown,editor}.js}`) | ✅ **gebaut, live deployt 2026-08-21**, Playwright vor dem Deploy grün+gesehen |
| Block B Step B4 | MCP-Fläche Bilder (`mcpserver/tools.py` — `get_item_asset`/`put_item_asset`) | ✅ **gebaut, live deployt 2026-08-21**, `mcp_smoke.py` 16/16 |
| Block B Step B5 | Betrieb/Deploy-Vorbereitung (`diagnose.sh` Prüfung 13, `UPDATE_LOG.md`, `ui_budget.py`) | ✅ **gebaut, Block B vollständig, live deployt 2026-08-21** |

## Geerbte Contracts

Fünfte, benannte Öffnung des P1-Contracts (`storage/{files,store,models}.py`) — **gebaut**
2026-08-20 (Step B1), siehe `phase1_storage/CLAUDE.md` unter „Geerbte Contracts" (P6.5-T).
Details dort, nicht hier dupliziert.

---

## Session stopped — 2026-08-21 (Live-Deploy bestätigt: Block A + Block B vollständig live)

**Auftrag:** Nikinger führte den in der Vorsitzung übergebenen Deploy-Befehl selbst live aus
(Sudo für den Neustart, außerhalb dessen, was Claude Code selbst kann — Präzedenz seit P6 Steps
4–6). Diese Session: Ergebnis read-only nachgeprüft, Doku nachgezogen (Hard Rule 8).

**Was live passierte, per Transkript, nicht nur behauptet:**
1. `diagnose.sh` scheiterte zunächst an Prüfung 4 (`tailscale funnel status` zeigte Port 8765
   nicht als aktiv) — ein anderer, einfacherer Fund als der 2026-08-19-Fallstrick (Prüfung 5,
   Backhaul-Problem): hier fehlte die Funnel-Weiterleitung selbst, wahrscheinlich nach einem
   zwischenzeitlichen Neustart/Session-Reset nicht neu aufgebaut. `sudo tailscale funnel --bg
   8765` (Sudo nötig, weil kein `tailscale set --operator=savefyx` gesetzt ist — Betriebsnotiz,
   kein Bug) behob es, danach lief `diagnose.sh` sauber durch (nicht im Transkript wiederholt,
   aber der Deploy-Lauf direkt danach setzt eine funktionierende Prüfung voraus).
2. `sudo systemctl start sharefyx-authbackup.service` — frisches Auth-Backup vor der
   `auth.sqlite3`-Migration (kein neues Schema in diesem Release, aber Standardvorsicht).
3. `SHAREFYX_RELEASES_DIR=/opt/sharefyx/releases SHAREFYX_CURRENT_LINK=/opt/sharefyx/current
   SHAREFYX_DATA_ROOT=/home/savefyx/savefyx-data SHAREFYX_BACKUP_DIR=/var/lib/sharefyx-backup
   SHAREFYX_SYSTEMCTL="sudo systemctl" phase5_ui/scripts/deploy.sh main` — 828/828 Tests im
   Release-Build grün, `docs/UPDATE_LOG.md`-Gate (P6-X) bestand ohne Override (Datum war auf
   2026-08-21 vorbereitet, siehe vorherige Session), Health-Gate `/ui/login`→200,
   `/api/v1/me`→401, `/mcp/`→401, Retention entfernte das älteste Release (`20260810...`,
   KEEP=5), JSON bestätigt `"result":"ok"`.
4. **Read-only gegengeprüft, nicht nur die JSON-Zeile vertraut:** `readlink -f
   /opt/sharefyx/current` → `/opt/sharefyx/releases/20260821T183341.270842Z`; `git log
   --oneline -1` darin → `f96125e`, identisch mit dem `main`-HEAD zum Deploy-Zeitpunkt (der
   Commit mit dem korrigierten `UPDATE_LOG.md`-Datum aus der Vorsitzung).

**Ergebnis: Block A und Block B (Steps B1–B5) sind live**, nicht nur gebaut — Modul-Status-Tabelle
oben nachgezogen (jede Zeile trägt jetzt „live deployt 2026-08-21").

**Was live sein UND nicht sein bedeutet:** der Deploy selbst schließt Gate A→B nicht. Gate A→B
ist definiert als eine echte Claude-Connector-Probe (claude.ai/Desktop gegen den echten OAuth-
Connector) — das ist ein Nutzungsereignis, kein Deploy-Ereignis. V60 (rendert der Connector
`ImageContent`?) und V64 (löst `destructiveHint: True` eine wiederholte Rückfrage aus?) bleiben
beide offen, aus demselben Grund: Client-Verhalten, das nur eine echte Sitzung beantworten kann.

**Vom Nikinger für diese Session freigegeben, noch nicht ausgeführt:** ein MCP-Werkzeug-Rundlauf
gegen den echten, jetzt live deployten Connector — ausdrücklich mit der Auflage, jedes dabei
angelegte Item danach zu archivieren (`update_item(status="archived")`, nie Hard-Delete, Hard
Rule 5/Entscheidung H). **Blockiert:** diese Claude-Code-Sitzung hat den sharefyx-MCP-Server
nicht als Tool verdrahtet (`ToolSearch` liefert keinen Treffer, keine `.mcp.json`/kein
MCP-Server-Eintrag in den Settings dieser Session) — die OAuth-Autorisierung (Passwort + TOTP,
Browser-Flow) kann diese Sitzung nicht selbst durchlaufen, das ist absichtlich so gebaut (Hard
Rule: kein Secret, das den Server umgeht). Der Rundlauf braucht entweder (a) den Nikinger, der
den Connector selbst gegen den echten Prompt fährt und berichtet, oder (b) `claude mcp add`
gegen die echte `PUBLIC_BASE_URL` mit einer echten, vom Nikinger im Browser abgeschlossenen
OAuth-Anmeldung, danach könnte DIESE Sitzung die zehn Tools nativ aufrufen. Noch keins von
beidem geschehen — für die nächste Session vorgemerkt, kein stiller Rückzug vom Auftrag.

**Verifiziert:** keine Testsuite in dieser Session gelaufen (reine Doku-Nachpflege, kein
Code-Diff). `git status` zeigt ausschließlich den Phase-Head + `SESSIONS_ARCHIVE.md` +
`docs/INDEX.md`.

**Offen für die nächste Session:**
- Gate A→B: entweder Nikinger-Live-Probe oder `claude mcp add` mit echter OAuth-Anmeldung, dann
  der zugesagte Werkzeug-Rundlauf inkl. Archivieren jedes Test-Items.
- V60/V64 bleiben offen, an dieselbe Probe gekoppelt.
- `filename`-Persistenzfrage, Doku-Schuld, `test_authctl.py`-Flake: unverändert offen.
