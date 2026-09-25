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
updated: 2026-09-25 (C4 ✅ DHCP-Reservierung im RUT X50, per `local_vision`-MCP-Aufruf gegen die GPU ausgelesen — erster echter Einsatz über den opencode-Pfad) | 2026-09-25 (zweite Reboot-Probe grün: CT-Knoten 20:54 > 20:42, Major 235 = `/proc/devices`, `cuInit = 0`, `size_vram` = `size` — Boot-Persistenz ✅) | 2026-09-25 (Reboot-Probe: uvm-Major 511→235, `cuInit = 999`; Fix per `devN`-Passthrough, per CT-Neustart bewiesen `cuInit = 0`, zweite Reboot-Probe offen, `size_vram` = `size`; C5 gesetzt; V166 beantwortet) | 2026-09-25 (Boot-Persistenz eingerichtet, CT 111 `onboot: 0` gefunden, Reboot-Probe offen) | 2026-09-25 (GPU-Inferenz läuft: CT 111 auf 580.173.02, `size_vram` = `size`, 63 tok/s, P9-21/-23/-26 ✅; Boot-Persistenz offen) | 2026-09-25 (Host-Treiber 580.173.02 mit `nvidia-uvm` installiert und geladen, kein Reboot) | 2026-09-25 (V165 beantwortet: 580.173.02 kennt die neue `zone_device_page_init`-Signatur) | 2026-09-25 (Step C Diagnose bestätigt: kein `/dev/nvidia-uvm`, `cuInit = 999`) | 2026-09-25 (Step C Diagnose, Claude Code: CUDA fehlt, weil `nvidia-uvm` fehlt — C2-Trade-off-Satz datiert korrigiert, Modulstatus C nachgezogen, Nikinger-Entscheidung zum Host-Fix offen) | 2026-09-25 (Backlog aufgeräumt: „opencode via Tailscale" für sharefyx-VM per Nikinger-Update mittlerweile passiert, Eintrag aus der Backlog-Sektion entfernt; nur noch D1 zurückgestellt) | 2026-09-25 (Step C Teil 2 / C6 — `mcp_local_vision_server.py` Skript-Fixes aus Plan §5.3: `serve()` loggt aufgelösten Endpoint, `--endpoint` wirkt jetzt auch ohne `--check`; neue zentrale `resolve_endpoint(args)` mit Präzedenz `--endpoint` > `$LOCAL_VISION_ENDPOINT` > `DEFAULT_ENDPOINT`; `_CURRENT_ENDPOINT` als Modul-Globals wird in `serve()` einmal gesetzt und von `handle_tools_call` gelesen statt erneut die Umgebungsvariable; 9 neue Tests + Counter-Probe ohne den Fix 7/9 rot — exakt die zwei gemeldeten Bugs; LXC + Ollama + C5/C7/C8 stehen aus) | 2026-09-24 (Step C Teil 1 — NVIDIA-Host-Treiber 580.126.09 installiert mit `--no-unified-memory`; pve-no-subscription-Repo ergänzt; drei dokumentierte Fehlbarkeiten auf dem Weg (Header-Paket fehlte, Backports führten denselben Upstream, Nouveau-Konflikt, uvm_hmm.c gegen 7.0.2-6-pve-Mai-Patch); eigener autoremove-Vorfall mit sudo/dkms-Verlust am 2026-09-24 wieder behoben; LXC + Ollama stehen aus) | 2026-09-24 (Backlog: ~19-min mcp-proxy.anthropic.com-Ausfall dokumentiert und geschlossen — gemessen nicht CGNAT/sharefyx-VM-seitig, Nikinger-Anordnung) | 2026-09-24 (Backlog: "opencode via Tailscale"-Behandlung für sharefyx-/Trading-Bot-VM nachgetragen, Nikinger-Feedback aus Netzwerk-Diagnosesession, kein Produktcode-Touch) | 2026-09-23 (D1/ESC-Bug auf Nikinger-Anordnung zurückgestellt, `## Backlog` neu) | 2026-09-23 (Step D code-complete — Drop-Ziel Space-Wurzel, ESC/Vollbild-Guard gebaut, gebaut in Claude Code statt opencode/M3, benannte Abweichung von P9-Q) | 2026-09-20 (Step 0 abgeschlossen — Phasenverzeichnis, INDEX-Rotationsskript, vier geplante plus drei ungeplante Doku-Defekte repariert, `doc_health.py` als Test festgenagelt, Baseline gemessen)
---

# Phase 9 — Härtung

Voller Plan: `docs/concepts/phase9_hardening_plan.md`. Diese Datei trägt nur Modulstatus und
den aktuellen Session-Block; die Entscheidungen (P9-A–P9-T) und Step-Details stehen im Plan.

## Modulstatus

| Step | Inhalt | Status |
|---|---|---|
| 0 | Verifikations-Durchlauf, Doku-Fundament (Phasenverzeichnis, INDEX-Rotation, vier Defekte, `doc_health.py`, Baseline) | ✅ |
| A | Echte Domain über eigenen VPS | ⬜ |
| B | `tailscaled-watchdog.service` | ⬜ |
| C | Vision-Dienst auf der RTX 3060 | 🟡 **GPU-Inferenz reboot-fest ✅** (Session-Block 2026-09-25 (3)): Host + CT 111 auf 580.173.02 inkl. `nvidia-uvm`, uvm per `devN`-Passthrough statt fester Major; erste Reboot-Probe fand die Major-Falle (511→235), zweite Reboot-Probe mit `devN` grün (`cuInit = 0`, `size_vram` = `size`) · P9-21 ✅ · P9-23 ✅ · P9-26 ✅ · C4 ✅ · C5 ✅ · C6 ✅ · **offen:** C8 CPU-Ollama stilllegen, Host-Aufräumen, P9-22-Nachweis |
| D | Zwei gemeldete Bugs (ESC/Vollbild, Drop-Ziel Space-Wurzel) | 🟡 D2 fertig; D1 (ESC/Vollbild) **bewusst zurückgestellt** — Nikinger-Entscheidung 2026-09-23, kein aktiver Blocker mehr, siehe Backlog unten |
| E | Karte: Reload-Overload, V118 | ⬜ |
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

## Session stopped — 2026-09-25 (3)

**Step C: die GPU-Inferenz übersteht einen Host-Reboot ✅ — nach einem zweiten Fix, den die erste
Reboot-Probe erzwungen hat; die zweite Reboot-Probe hat ihn bestätigt.** Coarbeit Claude Code ↔ Nikinger (dieselbe benannte
P9-Q-Abweichung wie Block (2), archiviert): jeder Host-Befehl vom Nikinger als root auf `pve`
ausgeführt, jede Ausgabe gelesen. Kein Repo-Code-Touch, kein `systemctl` aus dieser Session.

**Die Reboot-Probe ist zuerst gescheitert, und genau dafür war sie da.** Nach `pct set 111
--onboot 1` + Reboot: `nvidia-uvm-nodes.service` active, `nvidia_uvm` geladen, beide Knoten da,
CT 111 `running` (onboot greift) — aber **`235 nvidia-uvm`** statt 511, und im CT **`cuInit =
999`**. Die uvm-Major ist dynamisch und hängt an der Ladereihenfolge: 511 beim Hand-`modprobe` im
laufenden System, 235 beim Laden über `modules-load.d` beim Boot. `lxc.cgroup2.devices.allow: c
511:* rwm` ließ den Container den Knoten sehen, aber nicht öffnen.

**Fix: Proxmox-Device-Passthrough (`devN`) statt einer festgeschriebenen Major.** Verworfen wurde
511→235 umschreiben: hält nur, bis sich die Ladereihenfolge ändert (Kernel-/Treiber-Update), und
das Symptom ist dann wieder der stille CPU-Fallback, der eine ganze Session gekostet hat. `devN`
liest Major/Minor beim CT-Start vom Host-Knoten und setzt die cgroup-Regel selbst.
**V166 beantwortet ✅** (`devN` für LXC braucht PVE ≥ 8.1): `pve-manager/9.2.2`.

| Runde | Befehl (Kern) | Ergebnis |
|---|---|---|
| 4a | `pct stop 111`, Backup `/root/111.conf.bak-p9c`, `grep -v` nach Zeileninhalt → `/root/111.conf.new`, `diff` | genau die drei Zeilen 19–21 weg (`c 511:*` + zwei uvm-`mount.entry`), sonst nichts |
| 4b | `cat /root/111.conf.new > /etc/pve/lxc/111.conf` (kein Rename auf pmxcfs), `pct set 111 --dev0 /dev/nvidia-uvm,mode=0666 --dev1 /dev/nvidia-uvm-tools,mode=0666`, `pct start 111` | `dev0`/`dev1` in Zeile 5/6, im CT `crw-rw-rw- 235,0/235,1`, **`cuInit = 0`** |

`mode=0666` explizit, weil der alte Bind-Mount die Host-Rechte `crw-rw-rw-` mitbrachte und der
`devN`-Default nicht gemessen ist — ein root-only-Knoten hätte bei Ollama als Nicht-root-Nutzer
dasselbe Symptom erzeugt wie der Major-Fehler.

**Messung von der sharefyx-VM aus, nach dem `devN`-Fix (CT-Neustart, kein Host-Reboot):** `vision_ollama.py --endpoint
http://192.168.68.140:11434` gegen `c4_p8519_01_radiogruppe_im_dialog.png` → „Der markierte
Radio-Button im Dialog ist „als Text-Link im Text"." (**gleiche Aussage**, P9-26) in **19,9 s**
Wand (Modell kalt nach CT-Neustart); `/api/ps`: `size_vram` = `size` = 5.793.780.858 B.

**Stand CT 111 (`gpu-vision`) nach dieser Session, für einen kalten Leser:**
Host 580.173.02 (offene Module, DKMS gegen `7.0.2-6-pve`) · `/etc/modules-load.d/nvidia.conf`
(`nvidia`, `nvidia-uvm`) · `nvidia-uvm-nodes.service` (Oneshot `nvidia-modprobe -c=0 -u`,
`Before=pve-guests.service`) · `111.conf`: `onboot: 1`, cgroup-Allow `c 195:*` + Bind-Mounts
`nvidia0`/`nvidiactl`/`nvidia-caps` (Major 195 ist fest), **uvm über `dev0`/`dev1`** · CT-Userspace
580.173.02 `--no-kernel-module` · Ollama 0.34.4 auf `0.0.0.0:11434`, `qwen3-vl:8b`.

**C5 ✅:** `~/.config/opencode/opencode.jsonc` → `mcp.local_vision.environment.LOCAL_VISION_ENDPOINT
= http://192.168.68.140:11434` (nicht im Repo, P9-Plan §5.4). `mcp_local_vision_server.py
--check` mit diesem Wert: *„Ollama reachable, 1 model(s) installed
(endpoint=http://192.168.68.140:11434)"*. Dass opencode die `environment`-Map an den Prozess
durchreicht, zeigt erst die Startzeile beim nächsten opencode-Start (`opencode` ist aus der
Claude-Code-Shell nicht im `PATH`) — dort `endpoint=http://192.168.68.140:…` erwarten.

**Offen, Reihenfolge:**
**Zweite Reboot-Probe ✅ (Nikinger, 2026-09-25):** `nvidia-uvm-nodes.service` active ·
`235 nvidia-uvm` · CT 111 `running` · `dev0`/`dev1` in der Config · im CT `crw-rw-rw- 235,0/235,1`
mit Zeitstempel **20:54** (nach dem Reboot, gegenüber 20:42 aus Runde 4b — belegt, dass die Knoten
aus diesem Boot stammen, nicht aus der Vorsitzung) · **`cuInit = 0`**. Nötig war sie, weil `devN`
anders als der alte Bind-Mount (`optional,create=file`) bei fehlendem `/dev/nvidia-uvm` den CT-Start
verhindern kann; `Before=pve-guests.service` hat die Reihenfolge gehalten. Danach von der sharefyx-VM:
Vision-Lauf 19,7 s Wand, „Der Radio-Button „als Text-Link im Text" ist im Dialog markiert." (P9-26
gleich), `size_vram` = `size` = 5.793.780.858 B.

1. ~~**C4**~~ **✅ (Nikinger, 2026-09-25):** Static Lease im RUT X50 angelegt. **Ausgelesen nicht von
   Claude, sondern über den Vision-Dienst selbst** (Nikinger-Vorgabe: „nicht selbst ansehen"):
   `mcp_local_vision_server.py` per stdio-JSON-RPC (`initialize` → `tools/call local_vision`), Env
   nur `LOCAL_VISION_ENDPOINT` aus `opencode.jsonc` — derselbe Pfad, den opencode startet.
   Startzeile `endpoint=http://192.168.68.140:11434` (C6-Fix sichtbar), 50,8 s Wand für eine lange
   Volltranskription. Gelesen: Tab IPv4, Abschnitt „Static lease", **eine** Zeile `BC:24:11:FB:EA:CD
   (gpu-vision.lan)` → `192.168.68.140`, Hostname `gpu-vision.lan` — MAC und IP stimmen exakt mit
   `pct config 111` / C5 überein. Grenze: ein Screenshot zeigt nicht, ob „Save & Apply" gedrückt
   wurde, und die Reservierung entspricht dem laufenden Lease, ändert also nichts Messbares — der
   Nachweis ist die Nikinger-Aussage plus der nächste Lease-Wechsel. Ursprüngliche Begründung: C5
   schreibt `.140` fest, die Adresse war bis dahin nur ein DHCP-Lease. `net0` ist `ip=dhcp`, MAC `BC:24:11:FB:EA:CD`, Gateway `192.168.68.1`; auch die
   sharefyx-VM selbst hängt per DHCP im LAN. Empfehlung: **DHCP-Reservierung im RUT X50** (MAC →
   `.140`) statt statischer IP in `pct config` — eine statische `.140` im DHCP-Pool des Routers
   kann der Router einem anderen Gerät geben, die Reservierung hält die Adresse an der einen
   Stelle, die das LAN ohnehin verwaltet.
2. **C8 (Claude-Code-Entscheidung, Nikinger-Auftrag):** CPU-Ollama auf der sharefyx-VM
   **stilllegen, noch nicht löschen** — `sudo systemctl disable --now ollama` (Nikinger).
   Grund: ohne gesetzten Endpoint fällt das Skript still auf `127.0.0.1` zurück, ein 180-s-CPU-
   Lauf sieht dann aus wie ein funktionierender Dienst — dieselbe Fehlerklasse, die das fehlende
   `nvidia-uvm` verdeckt hat. Gestoppt heißt: Fehlkonfiguration = sofort `connection refused`.
   Binary + Modell (6,14 GB, Platte 14 GB frei) bleiben als kalter Fallback bis Step Z, dort
   `ollama rm qwen3-vl:8b` + Deinstallation.
3. **Aufräumen Host** (erst `ls`, PVE 9 hat evtl. tmpfs-`/tmp`): `/tmp/nv580173`, alter
   580.126.09-Installer, `/root/111.conf.new`, `/root/111.conf.bak-p9c` (zweite Reboot-Probe grün, Rollback nicht mehr
   nötig).
4. **P9-22** (von außen nicht erreichbar) weiterhin ohne ausdrücklichen Test.
5. **Benannt, nicht behoben: `docs/INDEX.md` steht bei 39.391 B** gegen das Kriterium ≤ 38 KB
   (V145: < 38.912 B) — schon vor dieser Session drüber, dieser Commit hat es um ~0,3 KB
   vergrößert. `doc_health.py` prüft die Größe nicht; eine Lücke im Step-0-Test, kein Freispruch.
