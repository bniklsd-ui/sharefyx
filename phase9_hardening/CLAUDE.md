---
status: live
purpose: Phase-9-Head — Härtungsphase (Domain, Watchdog, Vision-Dienst, Doku-Rotation, zwei Bugs, Karten-Reload, neunte P1-Contract-Öffnung, `_trash/`-Löschen), Modulstatus, aktueller Session-Handover
read-when: Arbeiten in phase9_hardening/ — zuerst lesen, zusammen mit dem neuesten Session-stopped-Block
detail: L2
up: ../CLAUDE.md
down:
  - ../docs/concepts/phase9_hardening_plan.md    # voller Plan, Locks P9-A–P9-T, Steps 0–H
  - ../docs/concepts/PHASE8_6_CLOSEOUT_HANDOVER.md  # Herkunft der P9-Punkte
  - SESSIONS_ARCHIVE.md                          # ältere Session-Blöcke, newest-first
updated: 2026-09-30 (Step A halb ausgeführt — **A1/A2/A3/A0b/A6 erledigt**: Domain bestellt, VPS `217.160.128.146` (Ubuntu 24.04.5), Policy + Beitritt mit `tag:sharefyx-edge` (von der Gegenseite belegt: Tags gesetzt, User=None), socat-Relay laufend mit identischer Härtung, Firewall `22` nur auf `tailscale0` mit Gegenprobe. **Kette blockiert an der Domain-Registrierung** — A4 braucht eine auflösende Domain fürs Zertifikat. Der Session-Fund: **mein eigenes A6 hätte den Betrieb gekappt** (`ufw default deny incoming` gilt auch auf `tailscale0`, SSH-Regel fehlte). Vier eigene Fehler dokumentiert, darunter ein erfundener Drift, der zurückgenommen wurde. V162/V163 neu offen, V151 Vorabwert 28–37 ms über DERP. 7 Tests + Gegenprobe 4/4) | 2026-09-29 (Step A: M3-Anteil gebaut, Ausführung liegt beim Nikinger — **Plan-A4 nachweislich unbaubar** (auf der Tailnet-IP lauscht nichts: `SPACE_HOST=127.0.0.1`, `ss -ltnp` belegt; `SPACE_HOST=0.0.0.0` wäre P3-B gebrochen) → **socat-Relay-Unit** `phase3_edge/systemd/sharefyx-tail-proxy.service` ohne `__REPO_ROOT__` im `ExecStart` (die Release-Pfad-Kopplung aus dem Step-B-Befund ist damit konstruktiv ausgeschlossen); Caddy-Vorlage + ACL-Fragment + `phase9_hardening/step_a/RUNBOOK_STEP_A.md` (A1–A9, ein Schritt pro Runde) + 7 Wächter, Gegenprobe 4/4; **V149 beantwortet** (alle Metadatenfelder abgeleitet, keines fest, kein `iss`-Check beim Einlösen), Befund 2 (`/health` statt `/healthz`) und Befund 3 (`ALLOWED_HOSTS` fehlt in Plan-A7) als Plan-Korrekturen, **Befund 5** = der Funnel bleibt nach A7 lesbar, aber nicht beschreibbar (CSRF-Origin exakt, `security.py:84`); **V162 neu offen** = ACL-Durchsetzung von `tailscale serve --tcp`, der Grund für die socat-Wahl; Step A ⬜→🟡) | 2026-09-28 (**Nachtrag**: §Vormerkung Vision-Modell — Messbefund aus Step E dokumentiert, Recherche in `docs/concepts/sichtpruefung_automation_tooling.md`, Schluss: ein Modellwechsel ist nicht der Hebel, die Zuständigkeitsgrenze ist es; kein P9-Block) | 2026-09-28 (Step E abgeschlossen ✅ — Reload-Overload der Karte: (a) kein zweiter `/graph`-Abruf ohne Datenänderung, Signatur aus dem `/overview`-Payload statt aus dem Graph-Payload (Plan-Korrektur: der Graph-Knoten hat kein `updated`, `api.py:698-708`), Erzeugung in `list.js :: loadOverview()` (deckt jeden Schreibpfad mit), Format in `state.js :: overviewToken()` (Blatt-Modul statt Zyklus), `force` nur am expliziten Refresh-Knopf; (b) bekannte Knoten behalten x/y über den Refetch. Sieben Tests (Node-Harness `graph_reload_probe.mjs` + statisch) und eine Browser-Probe (`p9e_reload_probe.py`, Wegwerf-Instanz Port 18768), beide mit Gegenprobe gegen HEAD: dort 1 statt 0 Abrufe und 10 statt 1 verschiedene Bilder in 1,5 s, im Node-Harness 467,6 px Positionssprung statt 0. V118 beantwortet (zwei Linien, eine gestrichelt) — Design-Frage eine-oder-zwei beim Nikinger. `pytest` 1031 passed + 1 failed (der Fehlschlag ist der Vortrag: `docs/INDEX.md` über der doc_health-Schwelle, auf HEAD genauso rot, gehört nach Step Z), `ui_budget` 5/5 (149,0 KB), Tabu-Bereichs-Diff leer, Wegwerf-Instanz über die PID-Datei gestoppt. Drei eigene Fehler dokumentiert (falsche erste Verdrahtung, Messgerät zählte sich selbst, Test scheiterte an eigenem Kommentar) | 2026-09-26 (Step B code-complete, install ausstehend: vier neue Dateien — `phase3_edge/scripts/tailscaled_watchdog.sh` + `phase3_edge/systemd/tailscaled-watchdog.{service,timer}` + `phase9_hardening/tests/test_tailscaled_watchdog.py` (5/5 grün); V152 beantwortet (kein Tailscale-eigenes Feature ohne kommerzielles Add-on), V153 als Empfehlung dokumentiert (Polkit `.rules`-Datei `/etc/polkit-1/rules.d/99-tailscaled-watchdog-restart.rules`, Sudoers-Fallback `/etc/sudoers.d/tailscaled-watchdog-restart`); Modulstatus Step B ⬜→🟡, Phase-9-###-Sub-Sektion ergänzt; Phase-9-Zeile in `docs/INDEX.md` nachgezogen; kein Touch an bestehendem Code, Hard Rule 8 (Doc-Update im selben Commit) und Hard Rule 9 (kein `systemctl` durch M3) eingehalten) | 2026-09-26 (Step C abgeschlossen: C8 `sudo systemctl disable --now ollama` Nikinger-Cobefehl, sharefyx-VM `inactive`/`disabled`, `curl 127.0.0.1:11434` → HTTP 000 exit 7 `Connection refused` (bestätigt aus dieser Shell als zweite Sichtprobe), binary + Modell bleiben als kalter Fallback bis Step Z; Host-Aufräumen pve: `/root/111.conf.new` (633 B, 2026-09-25 22:41) und `/root/111.conf.bak-p9c` (842 B, 2026-09-25 22:41) per `rm -f` entfernt, `/tmp/nv580173` und alter `NVIDIA-Linux-x86_64-580.126.09.run` waren bereits weg — PVE-9-tmpfs bzw. im Vorrundezweig schon entfernt; P9-22 deferred — kein externer Test möglich, architektonischer Beweis captured: 192.168.68.140 ist RFC1918, sharefyx-VM hat keine öffentliche IP (CGNAT via RUT X50, default route via 192.168.68.1), Tailscale-Funnel mappt nur `127.0.0.1:8765` (kein `*:11434` auf sharefyx-VM), kein Port-Forward auf RUT X50, der einzige 11434-Listener ist innerhalb CT 111; Step C 🟡→✅, Modulstatus nachgezogen, Session-Block 2026-09-26 angehängt) | 2026-09-25 (C4 ✅ DHCP-Reservierung im RUT X50, per `local_vision`-MCP-Aufruf gegen die GPU ausgelesen — erster echter Einsatz über den opencode-Pfad) | 2026-09-25 (zweite Reboot-Probe grün: CT-Knoten 20:54 > 20:42, Major 235 = `/proc/devices`, `cuInit = 0`, `size_vram` = `size` — Boot-Persistenz ✅) | 2026-09-25 (Reboot-Probe: uvm-Major 511→235, `cuInit = 999`; Fix per `devN`-Passthrough, per CT-Neustart bewiesen `cuInit = 0`, zweite Reboot-Probe offen, `size_vram` = `size`; C5 gesetzt; V166 beantwortet) | 2026-09-25 (Boot-Persistenz eingerichtet, CT 111 `onboot: 0` gefunden, Reboot-Probe offen) | 2026-09-25 (GPU-Inferenz läuft: CT 111 auf 580.173.02, `size_vram` = `size`, 63 tok/s, P9-21/-23/-26 ✅; Boot-Persistenz offen) | 2026-09-25 (Host-Treiber 580.173.02 mit `nvidia-uvm` installiert und geladen, kein Reboot) | 2026-09-25 (V165 beantwortet: 580.173.02 kennt die neue `zone_device_page_init`-Signatur) | 2026-09-25 (Step C Diagnose bestätigt: kein `/dev/nvidia-uvm`, `cuInit = 999`) | 2026-09-25 (Step C Diagnose, Claude Code: CUDA fehlt, weil `nvidia-uvm` fehlt — C2-Trade-off-Satz datiert korrigiert, Modulstatus C nachgezogen, Nikinger-Entscheidung zum Host-Fix offen) | 2026-09-25 (Backlog aufgeräumt: „opencode via Tailscale" für sharefyx-VM per Nikinger-Update mittlerweile passiert, Eintrag aus der Backlog-Sektion entfernt; nur noch D1 zurückgestellt) | 2026-09-25 (Step C Teil 2 / C6 — `mcp_local_vision_server.py` Skript-Fixes aus Plan §5.3: `serve()` loggt aufgelösten Endpoint, `--endpoint` wirkt jetzt auch ohne `--check`; neue zentrale `resolve_endpoint(args)` mit Präzedenz `--endpoint` > `$LOCAL_VISION_ENDPOINT` > `DEFAULT_ENDPOINT`; `_CURRENT_ENDPOINT` als Modul-Globals wird in `serve()` einmal gesetzt und von `handle_tools_call` gelesen statt erneut die Umgebungsvariable; 9 neue Tests + Counter-Probe ohne den Fix 7/9 rot — exakt die zwei gemeldeten Bugs; LXC + Ollama + C5/C7/C8 stehen aus) | 2026-09-24 (Step C Teil 1 — NVIDIA-Host-Treiber 580.126.09 installiert mit `--no-unified-memory`; pve-no-subscription-Repo ergänzt; drei dokumentierte Fehlbarkeiten auf dem Weg (Header-Paket fehlte, Backports führten denselben Upstream, Nouveau-Konflikt, uvm_hmm.c gegen 7.0.2-6-pve-Mai-Patch); eigener autoremove-Vorfall mit sudo/dkms-Verlust am 2026-09-24 wieder behoben; LXC + Ollama stehen aus) | 2026-09-24 (Backlog: ~19-min mcp-proxy.anthropic.com-Ausfall dokumentiert und geschlossen — gemessen nicht CGNAT/sharefyx-VM-seitig, Nikinger-Anordnung) | 2026-09-24 (Backlog: "opencode via Tailscale"-Behandlung für sharefyx-/Trading-Bot-VM nachgetragen, Nikinger-Feedback aus Netzwerk-Diagnosesession, kein Produktcode-Touch) | 2026-09-23 (D1/ESC-Bug auf Nikinger-Anordnung zurückgestellt, `## Backlog` neu) | 2026-09-23 (Step D code-complete — Drop-Ziel Space-Wurzel, ESC/Vollbild-Guard gebaut, gebaut in Claude Code statt opencode/M3, benannte Abweichung von P9-Q) | 2026-09-20 (Step 0 abgeschlossen — Phasenverzeichnis, INDEX-Rotationsskript, vier geplante plus drei ungeplante Doku-Defekte repariert, `doc_health.py` als Test festgenagelt, Baseline gemessen)
---

# Phase 9 — Härtung

Voller Plan: `docs/concepts/phase9_hardening_plan.md`. Diese Datei trägt nur Modulstatus und
den aktuellen Session-Block; die Entscheidungen (P9-A–P9-T) und Step-Details stehen im Plan.

## Modulstatus

| Step | Inhalt | Status |
|---|---|---|
| 0 | Verifikations-Durchlauf, Doku-Fundament (Phasenverzeichnis, INDEX-Rotation, vier Defekte, `doc_health.py`, Baseline) | ✅ |
| A | Echte Domain über eigenen VPS | 🟡 **M3-Anteil gebaut 2026-09-29, **A1/A2/A3/A0b/A6 seit 2026-09-30 ausgeführt** (Domain bestellt, VPS `217.160.128.146`, Policy+Beitritt mit `tag:sharefyx-edge`, socat-Relay laufend, Firewall `22` nur auf `tailscale0`)** — **A5 wartet auf die Domain-Registrierung, A4/A7/A8 hängen daran** — `phase9_hardening/step_a/RUNBOOK_STEP_A.md` (der geführte Ablauf A1–A9 mit sechs gemessenen Befunden, die den Plan korrigiert haben) + `Caddyfile.template` (A4) + `tailscale-acl.draft.json` (A3) + `phase3_edge/systemd/sharefyx-tail-proxy.service` (der fehlende Erreichbarkeitsweg) + `phase9_hardening/tests/test_tail_proxy.py` (7/7 grün, Gegenprobe 4/4). **Befund 1 ist der teuerste: Plan-A4 ist unbaubar, auf der Tailnet-IP lauscht nichts** (`SPACE_HOST=127.0.0.1`, `ss -ltnp` belegt) — gelöst per socat-Relay, **ohne** P3-B zu brechen. A1/A2 (Domain, VPS) + A0b–A8 sind Nikinger-Schritte · **V149 beantwortet** (alle Metadatenfelder abgeleitet, keines fest) · **V162 neu offen** (ACL-Durchsetzung von `tailscale serve --tcp`, Grund für die socat-Wahl) |
| B | `tailscaled-watchdog.service` | 🟡 **Code-complete (M3-Anteil 2026-09-26)**, install ausstehend — Repo-Anteil: `phase3_edge/scripts/tailscaled_watchdog.sh` + `phase3_edge/systemd/tailscaled-watchdog.{service,timer}` + `phase9_hardening/tests/test_tailscaled_watchdog.py` (5/5 grün, drei Stufen + Rate-Limit, identische Härtungs-Direktiven wie `sharefyx-mcp.service`); Polkit/Sudoers-Pfad (V153) + `systemctl enable --now tailscaled-watchdog.timer` + Intended-Offline-Probe (P9-19) sind Nikinger-Schritte · V152 beantwortet (kein Tailscale-eigenes Feature ohne kommerzielles Add-on, `pragmaxim/tailscale-watchdog` macht denselben Job) |
| C | Vision-Dienst auf der RTX 3060 | ✅ **Step C abgeschlossen** (Session-Block 2026-09-26): GPU-Inferenz reboot-fest (Host + CT 111 auf 580.173.02 inkl. `nvidia-uvm`, uvm per `devN`-Passthrough, zweite Reboot-Probe grün) + C8 (`ollama` auf sharefyx-VM `inactive`/`disabled`, `curl 127.0.0.1:11434` → `Connection refused`, binary + Modell bleiben als kalter Fallback bis Step Z) + Host-Aufräumen pve (zwei `/root/111.conf.{new,bak-p9c}` per `rm -f` weg; `/tmp/nv580173` und alter `NVIDIA-Linux-x86_64-580.126.09.run` bereits weg — PVE-9-tmpfs bzw. im Vorrundezweig entfernt) · P9-21 ✅ · P9-23 ✅ · P9-26 ✅ · C4 ✅ · C5 ✅ · C6 ✅ · **P9-22 deferred** (Nikinger-Entscheidung 2026-09-26, kein externer Test möglich) — architektonischer Beweis statt externem Test: 192.168.68.140 ist RFC1918, sharefyx-VM hat keine öffentliche IP (CGNAT via RUT X50), Tailscale-Funnel mappt nur `127.0.0.1:8765` (kein `*:11434` auf sharefyx-VM), kein Port-Forward auf RUT X50, einziger 11434-Listener sitzt innerhalb CT 111; Revisit-Step **Step Z oder P10-Backlog** |
| D | Zwei gemeldete Bugs (ESC/Vollbild, Drop-Ziel Space-Wurzel) | 🟡 D2 fertig; D1 (ESC/Vollbild) **bewusst zurückgestellt** — Nikinger-Entscheidung 2026-09-23, kein aktiver Blocker mehr, siehe Backlog unten |
| E | Karte: Reload-Overload, V118 | ✅ **Step E abgeschlossen** (Session-Block 2026-09-28): (a) kein zweiter `/graph`-Abruf ohne Datenänderung — Signatur aus dem `/overview`-Payload, das der Client ohnehin holt (Plan §7.2(a) nannte den Graph-Payload; der hat **kein** `updated`, datierte Plan-Korrektur) · (b) bekannte Knoten behalten `x`/`y` über den Refetch · `force` nur am expliziten Refresh-Knopf · 7 Tests (Node-Harness + statisch) + Browser-Probe gegen die Wegwerf-Instanz, beide mit Gegenprobe gegen HEAD (dort 1 Abruf und 10 verschiedene Bilder in 1,5 s) · **P9-33/-34/-35 ✅** · **V118 beantwortet (zwei Linien, eine davon gestrichelt)** — die Design-Frage „eine oder zwei Linien" liegt beim Nikinger (P9-36) |
| F | Schema-Fundament (neunte P1-Contract-Öffnung: `doing`/`assignee`) | ⬜ |
| G | Löschen (F2) nach `_trash/` | ⬜ |
| H | Abhängigkeits-Hygiene | ⬜ |
| Gate/Z | Abnahme, Closeout | ⬜ |

## Backlog (bewusst zurückgestellt, kein Phasen-Blocker)

- **D1 — ESC im Vollbild schließt zusätzlich das Item.** Diagnose geklärt (macOS Safari,
  natives Vollbild über den grünen Knopf), Fix nicht — der gebaute
  `document.fullscreenElement`-Guard (Session 2026-09-23) sieht diesen Fall nicht, weil die
  Web-Fullscreen-API dort per Spezifikation nicht greift. **Nikinger-Entscheidung 2026-09-23:**
  zurückstellen, angehen, sobald genug Zeit da ist — kein aktiver Blocker für den Rest von P9.
  Ansatzpunkte für den nächsten Anlauf stehen im Session-Block 2026-09-23 unten (gegen echtes
  Safari messen, keine Heuristik raten).
- **Derselbe Vormittag, separater Vorfall, jetzt geschlossen: `mcp-proxy.anthropic.com`
  (Anthropics eigenes Connector-Relay für claude.ai) lieferte ~19 Minuten lang durchgehend
  Cloudflare-502 auf jeden `Sharefyx`-Connector-Call** (`list_spaces`, viermal probiert,
  09:35–09:41 CEST), danach ohne jede Aktion von unserer Seite wieder normal (09:41→später:
  `list_spaces` liefert sauber 4 Spaces). **Gemessen, nicht vermutet, dass es nicht an
  CGNAT/Mobilfunk (RUT X50) oder an der sharefyx-VM lag:** `journalctl -u sharefyx-mcp`
  zeigt für alle vier 502-Zeitpunkte **keinen einzigen eingehenden Request** — kein POST auf
  `/mcp`, nicht mal ein 4xx —, während `GET /health` über denselben eigenen Funnel-Endpoint
  in derselben Minute jedes Mal sofort 200 lieferte und ein `POST /mcp/` um 09:22 (vor dem
  Fenster) sauber 200 loggte. Die 502 kann also nicht vom eigenen Netz/Tunnel kommen, wenn der
  Request dort nie ankommt. Zwei Nikinger-Restarts (`sharefyx-mcp.service` + Funnel) während
  des Fensters haben nichts geändert — konsistent mit „Fehler liegt vor der eigenen
  Infrastruktur". `status.claude.com` zeigte zeitgleich keinen Incident, aber vier unabhängige
  `anthropics/claude-code`-GitHub-Issues (#48277, #48291, #94356, #69426) beschreiben exakt
  dasselbe Muster — wiederkehrende, nicht auf der Statusseite gelistete 502 an genau diesem
  Relay. **Eingestuft als: unbekannter, vorübergehender Ausfall bei Anthropic
  (`mcp-proxy.anthropic.com`), explizit nicht auf CGNAT/Mobilfunk-Setup oder die sharefyx-VM
  zurückzuführen** — Nikinger-Anordnung 2026-09-24, so dokumentieren und nicht weiter
  untersuchen.

## Session stopped — 2026-09-30

**Step A ist halb gelaufen: der Repo-Anteil ist gebaut, und der Nikinger hat A1, A2, A3, A0b
und A6 ausgeführt.** Die Kette hängt jetzt an genau einer Stelle — der Domain-Registrierung
für A5. A4 (Caddy) braucht eine auflösende Domain für das Let's-Encrypt-Zertifikat, A7 und A8
hängen an A4. **Kein Produktcode berührt**, `pytest` grün, Tabu-Bereichs-Diff leer, kein
`systemctl` von mir, `sharefyx-mcp` nur gelesen (Hard Rule 9).

### Der Befund, der die Bauform getragen hat — und der war teuer

Plan §3.2 A4 verlangt `reverse_proxy <heimvm-tailnet-name>:<port>`. **Das ist unbaubar.**
`sharefyx-mcp.service:13` setzt `SPACE_HOST=127.0.0.1`, `ss -ltnp` zeigte keinen Listener auf
`100.93.43.122:8765`, und der Funnel funktioniert nur, weil `tailscaled` auf derselben Maschine
in die Schleife connectet. Die naheliegende Reparatur `SPACE_HOST=0.0.0.0` verstößt gegen die
**gelockte P3-B-Entscheidung**. Statt dessen ein Relay, das die eine Lücke schließt ohne P3-B
zu brechen — und **ohne `__REPO_ROOT__` im `ExecStart`**, womit sich die Release-Pfad-Kopplung
aus dem Step-B-Befund gar nicht erst eintritt.

`tailscale serve --tcp` (1.102.4 kann es) wäre eleganter und ist **nicht** gewählt: die
ACL-Durchsetzung von Tailscale-TCP-Forwardern war nicht verifizierbar (kein Netzzugriff), und
eine offene Frage darf nicht die Grundlage einer Firewall-Entscheidung sein → **V162** offen.

### Sieben Befunde, alle mit Fundstelle (Volltext im Runbook §0)

`/health` statt `/healthz` (`app.py:216`) · `ALLOWED_HOSTS` fehlt in Plan-A7 (sonst 400 auf
*jede* Anfrage, Live-Incident 2026-09-18) · **V149 beantwortet**: `issuer` **ist** `base_url`
**ist** `SPACE_PUBLIC_BASE_URL`, kein `iss`-Check beim Einlösen, also invalidiert der Wechsel
keine Token-Familie · der Funnel bleibt nach A7 **lesbar, aber nicht beschreibbar** (CSRF-Origin
exakt, `security.py:84`) — die Präzisierung, die P9-14 braucht · `socat` fehlte · die
Tailnet-Policy erlaubt heute **alles** (`src/dst/ip` je `*`), unser Grant ist damit **zusätzlich
und nicht einschränkend** — benannt, nicht mitgenommen.

### Der Fund dieser Session, der am meisten zählt: mein eigenes A6 hätte den Betrieb gekappt

`ufw default deny incoming` gilt **auf allen Interfaces, auch `tailscale0`**. Meine erste
Fassung von A6 erlaubte 80/443, aber **kein SSH über das Tailnet** — wer über die Tailnet-IP
verbunden ist, verliert die Verbindung, und zurück kommt man nur über die IONOS-Webconsole.
Gefallen ist mir das **erst beim Durchdenken der Firewall-Semantik**, nicht beim Schreiben —
und der Nikinger hatte ausgerechnet vorher gefragt, ob die Schritte den laufenden Betrieb
überhaupt anfassen. Diese Frage war die bessere Prüfung als meine Checkliste.

### Vier eigene Fehler, alle vor dem Commit behoben

1. **`tailscale ping` als Beleg** — ich hatte ins Runbook geschrieben, er antworte „noch
   nicht". Falsch in die Richtung: der Befehl prüft den WireGuard-Pfad zwischen zwei
   `tailscaled`, nicht die Datenebene, auf der die ACL greift, und **kann grün sein, während
   die Regel fehlt**. Er ist kein Nachweis. Der echte Nachweis ist der ACL-Testharness.
2. **`acls` statt `grants`** — der Screenshot der Seite *Add rule* zeigte den Knopf
   **„Save grant"**. Die klassische Form hätte der Nikinger abtippen müssen, weil die GUI sie
   nicht erzeugt. Entwurf, Test und Runbook folgen jetzt der belegten Form.
3. **Ein erfundener Drift** — ich meldete dem Nikinger, `local.env` und die installierte Unit
   wichen im `DATA_ROOT` ab. **Falsch**: beide nennen `/home/savefyx/savefyx-data`, das
   Verzeichnis existiert. Ich hatte mein eigenes `cat`-Ergebnis falsch gelesen und die
   Differenz durch eine Diagnose bestätigt, die ich nicht gemacht hatte. Zurückgenommen, bevor
   daraus eine Aufgabe wurde.
4. **`space.` statt `sharefyx.`** — mein Vorschlag aus Kürzegründen war der schwächere: die
   Adresse wird an vier Stellen als exakter String verglichen, und ein Alltagswort ist das,
   was man falsch erinnert. Zurückgenommen, mit Begründung im Runbook.

Dazu eine **Warnung, die ich mir selbst nicht gegönnt habe**: `docs/INDEX.md` steht bei
**44.669 B** und damit ~6,6 KB über dem 40-KB-Schwellwert des Werkzeugs. Benannt statt
versteckt, wie in P8.6; die Lösung bleibt die INDEX-Rotation in Step Z (P9-L).

### Was gemessen wurde — und von wem

| Schritt | Nachweis |
|---|---|
| **A3** Beitritt | von der **Gegenseite**: die Heim-VM sieht `ubuntu` als `100.121.142.113` mit `Tags=['tag:sharefyx-edge']` und `User=None` — genau das beweist, dass der Tag griff und die Node nicht als Nutzergerät läuft |
| **A0b** Relay | `socat` 1.8.0.0, `ProtectSystem=strict`/`NoNewPrivileges`/`MemoryDenyWriteExecute` gesetzt, **zwei** Listener, `diagnose.sh` danach unverändert alle Prüfungen grün **inklusive des echten öffentlichen Pfads** — die Bestandspfade sind unberührt |
| **A6** Firewall | Gegenprobe von der Heim-VM (die weder im Tailnet des VPS noch in dessen LAN ist): Tailnet-SSH **offen**, öffentliches SSH **timeout** (ufw *droppt* still, `deny` ≠ `reject`), 443 **refused** (Paket kommt am Host an, lauscht noch nichts) |
| **V151** Vorabwert | `tailscale ping` → **28–37 ms über DERP Frankfurt**, nicht direkt (erwartbar hinter CGNAT). Das ist das Tailnet-Bein, nicht der ganze Weg; der Vergleich gegen 372,9 ms folgt in A7 |

**Die wechselnde PID ist aufgeklärt** (Reboot gestern Nacht): der Dienst startete 6 Sekunden
nach dem System-Boot — das gesunde Muster der P3-Rebootzeile 6, kein Incident. Ich hatte sie
zuvor als ungeklärt notiert, statt eine Erfindung zu liefern; die eine Messung
(`journalctl -b -u sharefyx-mcp`) hätte es sofort gezeigt.

### Tests und Selbstprüfung

`phase9_hardening/tests/test_tail_proxy.py`, 7 Wächter: Ziel bleibt Loopback · Bind ist eine
Tailnet-IP und nicht `0.0.0.0` · Härtung **identisch mit der MCP-Unit** · kein Repo-Pfad im
`ExecStart` · Port identisch mit `SPACE_PORT` · Health-Routen-Korrektur hält · ACL-Entwurf
fail-closed. **Gegenprobe: vier Verstöße eingebaut → 4/7 rot, exakt die vier zuständigen.**

`pytest -q` → siehe Commit-Body. `doc_health.py` → **0 Befunde**. Tabu-Bereichs-Diff leer.
Kein Service-Touch; die Wegwerf-Instanz gab es nicht, nur eine einzelne TCP-Verbindung auf Port
22 als Vorprüfung des VPS.

### Nächster Schritt

**Blockiert an einer Stelle: die Domain.** Sobald `eurofyx.<tld>` registriert ist:
**A5** (A-Record `sharefyx` → `217.160.128.146`, **kein** AAAA) → **A4** (Caddy, drei
Platzhalter in `step_a/Caddyfile.template` füllen) → **A7** (der riskante Schritt: fasst den
laufenden Prod-Dienst an) → **A8** (Connector in beiden Konten, echter `list_spaces`).

**Zwei Entscheidungen liegen beim Nikinger:** (1) die TLD, `.com` ist empfohlen; (2) falls die
Domain-Aktivierung länger dauert, **Step F** (Schema `doing`/`assignee`) vorziehen — reiner
Code-Step, braucht nur **V160**: `assignee` als **Space-Name**? Empfehlung ja, **ohne**
Validierung, weil eine Prüfung gegen die Space-Liste eine zweite, nicht angekündigte
Contract-Öffnung wäre.

**Uncommitted geblieben, absichtlich:** `screenshots_latest/` enthält drei Arbeitsdateien des
Nikingers (zwei Tailscale-Console-Screenshots + das als HTML gespeicherte Seitenquelltext).
Sie sind **nicht** im Repo und sollen es nicht werden: das HTML enthält die Knotenliste des
Tailnets mit Owner-Kontakten. Die `git add`-Aufrufe dieser Session nehmen `phase9_hardening/`
explizit, nicht `-A`.
