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
updated: 2026-09-29 (Step A: M3-Anteil gebaut, Ausführung liegt beim Nikinger — **Plan-A4 nachweislich unbaubar** (auf der Tailnet-IP lauscht nichts: `SPACE_HOST=127.0.0.1`, `ss -ltnp` belegt; `SPACE_HOST=0.0.0.0` wäre P3-B gebrochen) → **socat-Relay-Unit** `phase3_edge/systemd/sharefyx-tail-proxy.service` ohne `__REPO_ROOT__` im `ExecStart` (die Release-Pfad-Kopplung aus dem Step-B-Befund ist damit konstruktiv ausgeschlossen); Caddy-Vorlage + ACL-Fragment + `phase9_hardening/step_a/RUNBOOK_STEP_A.md` (A1–A9, ein Schritt pro Runde) + 7 Wächter, Gegenprobe 4/4; **V149 beantwortet** (alle Metadatenfelder abgeleitet, keines fest, kein `iss`-Check beim Einlösen), Befund 2 (`/health` statt `/healthz`) und Befund 3 (`ALLOWED_HOSTS` fehlt in Plan-A7) als Plan-Korrekturen, **Befund 5** = der Funnel bleibt nach A7 lesbar, aber nicht beschreibbar (CSRF-Origin exakt, `security.py:84`); **V162 neu offen** = ACL-Durchsetzung von `tailscale serve --tcp`, der Grund für die socat-Wahl; Step A ⬜→🟡) | 2026-09-28 (**Nachtrag**: §Vormerkung Vision-Modell — Messbefund aus Step E dokumentiert, Recherche in `docs/concepts/sichtpruefung_automation_tooling.md`, Schluss: ein Modellwechsel ist nicht der Hebel, die Zuständigkeitsgrenze ist es; kein P9-Block) | 2026-09-28 (Step E abgeschlossen ✅ — Reload-Overload der Karte: (a) kein zweiter `/graph`-Abruf ohne Datenänderung, Signatur aus dem `/overview`-Payload statt aus dem Graph-Payload (Plan-Korrektur: der Graph-Knoten hat kein `updated`, `api.py:698-708`), Erzeugung in `list.js :: loadOverview()` (deckt jeden Schreibpfad mit), Format in `state.js :: overviewToken()` (Blatt-Modul statt Zyklus), `force` nur am expliziten Refresh-Knopf; (b) bekannte Knoten behalten x/y über den Refetch. Sieben Tests (Node-Harness `graph_reload_probe.mjs` + statisch) und eine Browser-Probe (`p9e_reload_probe.py`, Wegwerf-Instanz Port 18768), beide mit Gegenprobe gegen HEAD: dort 1 statt 0 Abrufe und 10 statt 1 verschiedene Bilder in 1,5 s, im Node-Harness 467,6 px Positionssprung statt 0. V118 beantwortet (zwei Linien, eine gestrichelt) — Design-Frage eine-oder-zwei beim Nikinger. `pytest` 1031 passed + 1 failed (der Fehlschlag ist der Vortrag: `docs/INDEX.md` über der doc_health-Schwelle, auf HEAD genauso rot, gehört nach Step Z), `ui_budget` 5/5 (149,0 KB), Tabu-Bereichs-Diff leer, Wegwerf-Instanz über die PID-Datei gestoppt. Drei eigene Fehler dokumentiert (falsche erste Verdrahtung, Messgerät zählte sich selbst, Test scheiterte an eigenem Kommentar) | 2026-09-26 (Step B code-complete, install ausstehend: vier neue Dateien — `phase3_edge/scripts/tailscaled_watchdog.sh` + `phase3_edge/systemd/tailscaled-watchdog.{service,timer}` + `phase9_hardening/tests/test_tailscaled_watchdog.py` (5/5 grün); V152 beantwortet (kein Tailscale-eigenes Feature ohne kommerzielles Add-on), V153 als Empfehlung dokumentiert (Polkit `.rules`-Datei `/etc/polkit-1/rules.d/99-tailscaled-watchdog-restart.rules`, Sudoers-Fallback `/etc/sudoers.d/tailscaled-watchdog-restart`); Modulstatus Step B ⬜→🟡, Phase-9-###-Sub-Sektion ergänzt; Phase-9-Zeile in `docs/INDEX.md` nachgezogen; kein Touch an bestehendem Code, Hard Rule 8 (Doc-Update im selben Commit) und Hard Rule 9 (kein `systemctl` durch M3) eingehalten) | 2026-09-26 (Step C abgeschlossen: C8 `sudo systemctl disable --now ollama` Nikinger-Cobefehl, sharefyx-VM `inactive`/`disabled`, `curl 127.0.0.1:11434` → HTTP 000 exit 7 `Connection refused` (bestätigt aus dieser Shell als zweite Sichtprobe), binary + Modell bleiben als kalter Fallback bis Step Z; Host-Aufräumen pve: `/root/111.conf.new` (633 B, 2026-09-25 22:41) und `/root/111.conf.bak-p9c` (842 B, 2026-09-25 22:41) per `rm -f` entfernt, `/tmp/nv580173` und alter `NVIDIA-Linux-x86_64-580.126.09.run` waren bereits weg — PVE-9-tmpfs bzw. im Vorrundezweig schon entfernt; P9-22 deferred — kein externer Test möglich, architektonischer Beweis captured: 192.168.68.140 ist RFC1918, sharefyx-VM hat keine öffentliche IP (CGNAT via RUT X50, default route via 192.168.68.1), Tailscale-Funnel mappt nur `127.0.0.1:8765` (kein `*:11434` auf sharefyx-VM), kein Port-Forward auf RUT X50, der einzige 11434-Listener ist innerhalb CT 111; Step C 🟡→✅, Modulstatus nachgezogen, Session-Block 2026-09-26 angehängt) | 2026-09-25 (C4 ✅ DHCP-Reservierung im RUT X50, per `local_vision`-MCP-Aufruf gegen die GPU ausgelesen — erster echter Einsatz über den opencode-Pfad) | 2026-09-25 (zweite Reboot-Probe grün: CT-Knoten 20:54 > 20:42, Major 235 = `/proc/devices`, `cuInit = 0`, `size_vram` = `size` — Boot-Persistenz ✅) | 2026-09-25 (Reboot-Probe: uvm-Major 511→235, `cuInit = 999`; Fix per `devN`-Passthrough, per CT-Neustart bewiesen `cuInit = 0`, zweite Reboot-Probe offen, `size_vram` = `size`; C5 gesetzt; V166 beantwortet) | 2026-09-25 (Boot-Persistenz eingerichtet, CT 111 `onboot: 0` gefunden, Reboot-Probe offen) | 2026-09-25 (GPU-Inferenz läuft: CT 111 auf 580.173.02, `size_vram` = `size`, 63 tok/s, P9-21/-23/-26 ✅; Boot-Persistenz offen) | 2026-09-25 (Host-Treiber 580.173.02 mit `nvidia-uvm` installiert und geladen, kein Reboot) | 2026-09-25 (V165 beantwortet: 580.173.02 kennt die neue `zone_device_page_init`-Signatur) | 2026-09-25 (Step C Diagnose bestätigt: kein `/dev/nvidia-uvm`, `cuInit = 999`) | 2026-09-25 (Step C Diagnose, Claude Code: CUDA fehlt, weil `nvidia-uvm` fehlt — C2-Trade-off-Satz datiert korrigiert, Modulstatus C nachgezogen, Nikinger-Entscheidung zum Host-Fix offen) | 2026-09-25 (Backlog aufgeräumt: „opencode via Tailscale" für sharefyx-VM per Nikinger-Update mittlerweile passiert, Eintrag aus der Backlog-Sektion entfernt; nur noch D1 zurückgestellt) | 2026-09-25 (Step C Teil 2 / C6 — `mcp_local_vision_server.py` Skript-Fixes aus Plan §5.3: `serve()` loggt aufgelösten Endpoint, `--endpoint` wirkt jetzt auch ohne `--check`; neue zentrale `resolve_endpoint(args)` mit Präzedenz `--endpoint` > `$LOCAL_VISION_ENDPOINT` > `DEFAULT_ENDPOINT`; `_CURRENT_ENDPOINT` als Modul-Globals wird in `serve()` einmal gesetzt und von `handle_tools_call` gelesen statt erneut die Umgebungsvariable; 9 neue Tests + Counter-Probe ohne den Fix 7/9 rot — exakt die zwei gemeldeten Bugs; LXC + Ollama + C5/C7/C8 stehen aus) | 2026-09-24 (Step C Teil 1 — NVIDIA-Host-Treiber 580.126.09 installiert mit `--no-unified-memory`; pve-no-subscription-Repo ergänzt; drei dokumentierte Fehlbarkeiten auf dem Weg (Header-Paket fehlte, Backports führten denselben Upstream, Nouveau-Konflikt, uvm_hmm.c gegen 7.0.2-6-pve-Mai-Patch); eigener autoremove-Vorfall mit sudo/dkms-Verlust am 2026-09-24 wieder behoben; LXC + Ollama stehen aus) | 2026-09-24 (Backlog: ~19-min mcp-proxy.anthropic.com-Ausfall dokumentiert und geschlossen — gemessen nicht CGNAT/sharefyx-VM-seitig, Nikinger-Anordnung) | 2026-09-24 (Backlog: "opencode via Tailscale"-Behandlung für sharefyx-/Trading-Bot-VM nachgetragen, Nikinger-Feedback aus Netzwerk-Diagnosesession, kein Produktcode-Touch) | 2026-09-23 (D1/ESC-Bug auf Nikinger-Anordnung zurückgestellt, `## Backlog` neu) | 2026-09-23 (Step D code-complete — Drop-Ziel Space-Wurzel, ESC/Vollbild-Guard gebaut, gebaut in Claude Code statt opencode/M3, benannte Abweichung von P9-Q) | 2026-09-20 (Step 0 abgeschlossen — Phasenverzeichnis, INDEX-Rotationsskript, vier geplante plus drei ungeplante Doku-Defekte repariert, `doc_health.py` als Test festgenagelt, Baseline gemessen)
---

# Phase 9 — Härtung

Voller Plan: `docs/concepts/phase9_hardening_plan.md`. Diese Datei trägt nur Modulstatus und
den aktuellen Session-Block; die Entscheidungen (P9-A–P9-T) und Step-Details stehen im Plan.

## Modulstatus

| Step | Inhalt | Status |
|---|---|---|
| 0 | Verifikations-Durchlauf, Doku-Fundament (Phasenverzeichnis, INDEX-Rotation, vier Defekte, `doc_health.py`, Baseline) | ✅ |
| A | Echte Domain über eigenen VPS | 🟡 **M3-Anteil gebaut 2026-09-29, Ausführung Nikinger-Schritte** — `phase9_hardening/step_a/RUNBOOK_STEP_A.md` (der geführte Ablauf A1–A9 mit sechs gemessenen Befunden, die den Plan korrigiert haben) + `Caddyfile.template` (A4) + `tailscale-acl.draft.json` (A3) + `phase3_edge/systemd/sharefyx-tail-proxy.service` (der fehlende Erreichbarkeitsweg) + `phase9_hardening/tests/test_tail_proxy.py` (7/7 grün, Gegenprobe 4/4). **Befund 1 ist der teuerste: Plan-A4 ist unbaubar, auf der Tailnet-IP lauscht nichts** (`SPACE_HOST=127.0.0.1`, `ss -ltnp` belegt) — gelöst per socat-Relay, **ohne** P3-B zu brechen. A1/A2 (Domain, VPS) + A0b–A8 sind Nikinger-Schritte · **V149 beantwortet** (alle Metadatenfelder abgeleitet, keines fest) · **V162 neu offen** (ACL-Durchsetzung von `tailscale serve --tcp`, Grund für die socat-Wahl) |
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

## Session stopped — 2026-09-29

**Step A: der M3-Anteil ist gebaut, ausgeführt wird er vom Nikinger.** Kein Produktcode
berührt, kein Service-Touch, `pytest` grün, Tabu-Bereichs-Diff leer (Hard Rule 9 durchgehend:
kein `systemctl` von mir, nur `ss`/`tailscale status` als lesende Messung).

**Erste Handlung dieser Session war eine Rückfrage, kein Code.** Die Notiz aus der letzten
Runde lautete „Schritt f — die feste Domain". Der Plan trägt **A** = Domain (§3) und **F** =
Schema `doing`/`assignee` (§8) — zwei völlig verschiedene Arbeiten. Bevor ich etwas baue, wurde
gemessen, ob der Vorlauf von Step A überhaupt stattgefunden hat: `tailscale status` zeigt sieben
Nodes, **keiner ist ein Terminator**; `phase3_edge/local.env` trägt `PUBLIC_BASE_URL` und
`ALLOWED_HOSTS` weiter auf `…tail4a8b49.ts.net`. Der Vorlauf fehlt also, und der Plan sagt
ausdrücklich, dass Beschaffung **kein** Agenten-Auftrag ist. Nikinger-Antwort: **Step A,
mein Anteil vorbereiten.**

### Der Befund, der die Bauform gerettet hat

**Plan §3.2 A4 ist unbaubar, und zwar nicht wegen einer Kleinigkeit.** Die Anweisung lautet
`reverse_proxy <heimvm-tailnet-name>:<port>`. Gemessen:

- `phase4_auth/systemd/sharefyx-mcp.service:13` — `Environment=SPACE_HOST=127.0.0.1`
- `ss -ltnp` — `LISTEN 127.0.0.1:8765` und **kein** Listener auf `100.93.43.122:8765`
- `tailscale serve status` — der Funnel proxyt auf `http://127.0.0.1:8765`; er funktioniert
  genau deshalb, weil `tailscaled` auf derselben Maschine in die Schleife connectet

Auf der Tailnet-Adresse gibt es nichts, womit ein VPS sich verbinden könnte. Die naheliegende
Reparatur — `SPACE_HOST=0.0.0.0` — ist die **gelockte P3-B-Entscheidung** („wird nie
`0.0.0.0`", gilt am Host, nicht nur am Router). Sie zu brechen, um einen Proxy zu retten,
wäre genau die stille Abweichung, die P8.6 zweimal gekostet hat.

**Gebaut: ein Relay, das die eine Lücke schließt, ohne P3-B zu brechen.**
`phase3_edge/systemd/sharefyx-tail-proxy.service` macht `100.93.43.122:8765 → 127.0.0.1:8765`
mit `socat`; die App bindet unverändert auf Loopback. Bewusst **ohne** `__REPO_ROOT__` im
`ExecStart` — genau damit ist die Kopplung konstruktiv ausgeschlossen, die beim Watchdog zum
Befund wurde (dort zeigte `ExecStart` auf ein Release, das die Datei nicht enthält,
Session-Block 2026-09-28). `install_units.sh` wurde dafür **nicht** angefasst: das ist
P3-Code, und der Commit bleibt additiv; das Runbook installiert die Unit mit
`sudo install -m 0644`.

**Die Alternative wurde nicht aus Bequemlichkeit verworfen.** Tailscale **1.102.4** kann
`tailscale serve --tcp` (gemessen an `serve --help`) — kein zusätzlicher Prozess, der
elegantere Weg. Ob Tailscale-TCP-Forwarder die Tailnet-ACLs durchsetzen, war in dieser
Session **nicht verifizierbar** (kein Netzzugriff: `tailscale.com` per DNS nicht auflösbar,
Suchprovider leer). Eine offene Frage darf nicht die Grundlage einer Firewall-Entscheidung
sein → der Relay ist ein gewöhnlicher Listener auf `tailscale0`, für den das ACL-Modell ohne
Zusatzannahme gilt. Als **V162** offen notiert, mit der Frage und wo sie zu beantworten ist.

### Vier weitere Befunde, alle mit Fundstelle

1. **Die Health-Route heißt `/health`, nicht `/healthz`.** `app.py:216` registriert genau
   eine. Plan §3.4 (P9-10) nennt den falschen Pfad — Abnahmezeile mit datierter Korrektur.
2. **`ALLOWED_HOSTS` fehlt in Plan-A7.** Caddy reicht den Host-Header durch, die
   `TrustedHostMiddleware` (`app.py:214`) antwortet sonst auf **jede** Anfrage mit
   `400 Invalid host header`. Keine Theorie: der Live-Incident vom 2026-09-18 war genau das.
3. **V149 beantwortet:** `AuthSettings.issuer` **ist** `base_url` **ist**
   `SPACE_PUBLIC_BASE_URL` (`config.py:45`), `metadata.py:24-29` leitet vier Felder daraus ab,
   `resource` ebenso, und `allowed_redirect_origins` hat einen eigenen Default — die
   Redirect-URIs der Claude-Clients bleiben also unberührt. **Kein Feld steht fest.** A7 ist
   damit eine Handvoll Env-Werte; die §3.3-Falle bleibt trotzdem real, weil der `iss` Teil der
   Client-Registrierung ist (RFC 9207, `routes.py:154`) → **A7 vor A8**. Und: es gibt
   **nirgends** eine `iss`-Prüfung beim Einlösen (`resolver.py` enthält kein `iss`) — der
   Wechsel invalidiert keine bestehende Token-Familie.
4. **Der Funnel bleibt nach A7 lesbar, aber nicht beschreibbar.** `security.py:84` prüft
   `origin != settings.base_url` **exakt**. Nach A7 schickt ein Browser am alten
   Funnel-Host `Origin: …ts.net` → jeder Schreibvorgang 403, GETs laufen. Das ist die
   Präzisierung, die P9-14 braucht. Ein echter Dual-Betrieb bräuchte eine zweite erlaubte
   Origin im Code, `UiSettings` hat genau ein `base_url`-Feld — **das wird nicht gebaut**
   (außerhalb Step A). Der Funnel ist der Rückfallweg für „VPS weg"; Lesen und ein
   intakter Connector reichen dafür.

### Tests

`phase9_hardening/tests/test_tail_proxy.py`, 7 Wächter: Ziel bleibt Loopback · Bind ist eine
Tailnet-IP und nicht `0.0.0.0` · Härtungs-Direktiven **identisch mit der MCP-Unit** (die
Behauptung aus dem Step-B-Block wird hier gemessen statt geglaubt) · kein Repo-Pfad im
`ExecStart` · Port identisch mit `SPACE_PORT` · Health-Routen-Korrektur hält · ACL-Entwurf
fail-closed (genau eine Regel, genau ein Port, genau eine Adresse).

**Gegenprobe:** vier Verstöße eingebaut (`TAILNET_ADDR=0.0.0.0`, `APP_ADDR=0.0.0.0`,
`ProtectSystem=false`, `APP_PORT=9999`) → **4 von 7 rot, exakt die vier dafür zuständigen**;
nach dem Zurücksetzen 7/7 grün. Ein Wächter, der bei einem eingebauten Verstoß grün bleibt,
ist eine Behauptung.

### Vier eigene Fehler, alle vor dem Commit behoben

1. `_env_value` verglich gegen `^NAME=` und vergaß das `Environment=`-Präfix — **drei** Tests
   schlugen aus einem Grund rot, den sie nicht prüfen sollten.
2. `addr in ip_address("100.64.0.0/10")` — ein Netz ist keine Adresse, `ValueError` statt
   Aussage. `ip_network` ist die richtige Funktion.
3. Der `/healthz`-Wächter schlug an einem **eigenen Kommentar** an, der die Korrektur
   erklärt. Dieselbe Klasse wie in Step E (`test_graph_module_does_not_touch_the_api_
   contract`): ein Kommentar darf eine Route nennen, eine Anweisung nicht — der Wächter
   prüft jetzt nur die Nicht-Kommentar-Zeilen.
4. In den ACL-Entwurf rutschten zwei chinesische Zeichen (`古典`) in einen Nebensatz. Der
   Absatz ist ersetzt, JSON parsebar geprüft, die Datei auf Zeichen außerhalb des
   lateinischen/typografischen Bereichs geprüft.

### Selbstprüfung §0.4

1. `pytest -q` → siehe Commit-Body (Baseline 1031 + 7 aus diesem Commit).
2. `ui_budget` **nicht nötig** — `phase5_ui/webui/static/**` unberührt.
3. `node --check` **nicht nötig** — keine JS-Datei berührt.
4. Tabu-Bereichs-Diff leer für `permissions.py`, `server.py`, `authserver/`, `phase6_shares`,
   `phase7_spaces_admin` (Bereichs-Diff, nicht Working-Tree).
5. Doc-Update im selben Commit: dieser Block, Modulstatus, Rotation, INDEX-Zeile,
   `phase3_edge/CLAUDE.md`-Notiz (die neue Unit liegt in dessen Verzeichnis).
6. Kein Service-Touch. `sharefyx-mcp` nur **gelesen** (`ss`, `tailscale status`); die
   Live-Unit wurde nicht angefasst, kein `pkill -f`, kein `systemctl`.

### Nächster Schritt — beim Nikinger, nicht bei mir

**A1 (Domain) und A2 (VPS) sind Beschaffung und ausdrücklich kein Agenten-Auftrag.** Danach
läuft die Kette, ein Schritt pro Runde: **A3** (VPS ins Tailnet + ACL-Fragment) → **A0b**
(`socat` + Relay, sonst geht A4 nicht) → **A5** (DNS-A-Record) → **A4** (Caddy) → **A6**
(Firewall) → **A7** (Basis-URL + `ALLOWED_HOSTS`) → **A8** (Connector in beiden Konten, echter
`list_spaces`) → **A9** (Rückfall, Inhalt steht im Runbook) → P9-10–P9-15.

**Offen für den Nikinger, drei Entscheidungen:** (1) **A6-SSH** — die Firewall-Anweisung
lässt 22 bewusst zu; wer die Kiste nicht nur über Tailscale erreichbar haben will, entscheidet
das. (2) **Befund 5** — ob der Funnel nach A7 als **Lese**-Fallback genügt (Empfehlung) oder
ob ein echter Dual-Betrieb gewünscht ist (dann ist das eine Codeänderung, die außerhalb
Step A liegt und eine eigene Entscheidung braucht). (3) **`assignee`** (V160) für Step F —
unabhängig von A, aber es ist die einzige Frage, die F vor dem Bauen braucht.
