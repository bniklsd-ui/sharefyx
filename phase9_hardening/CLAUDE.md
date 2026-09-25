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
updated: 2026-09-25 (Boot-Persistenz eingerichtet, CT 111 `onboot: 0` gefunden, Reboot-Probe offen) | 2026-09-25 (GPU-Inferenz läuft: CT 111 auf 580.173.02, `size_vram` = `size`, 63 tok/s, P9-21/-23/-26 ✅; Boot-Persistenz offen) | 2026-09-25 (Host-Treiber 580.173.02 mit `nvidia-uvm` installiert und geladen, kein Reboot) | 2026-09-25 (V165 beantwortet: 580.173.02 kennt die neue `zone_device_page_init`-Signatur) | 2026-09-25 (Step C Diagnose bestätigt: kein `/dev/nvidia-uvm`, `cuInit = 999`) | 2026-09-25 (Step C Diagnose, Claude Code: CUDA fehlt, weil `nvidia-uvm` fehlt — C2-Trade-off-Satz datiert korrigiert, Modulstatus C nachgezogen, Nikinger-Entscheidung zum Host-Fix offen) | 2026-09-25 (Backlog aufgeräumt: „opencode via Tailscale" für sharefyx-VM per Nikinger-Update mittlerweile passiert, Eintrag aus der Backlog-Sektion entfernt; nur noch D1 zurückgestellt) | 2026-09-25 (Step C Teil 2 / C6 — `mcp_local_vision_server.py` Skript-Fixes aus Plan §5.3: `serve()` loggt aufgelösten Endpoint, `--endpoint` wirkt jetzt auch ohne `--check`; neue zentrale `resolve_endpoint(args)` mit Präzedenz `--endpoint` > `$LOCAL_VISION_ENDPOINT` > `DEFAULT_ENDPOINT`; `_CURRENT_ENDPOINT` als Modul-Globals wird in `serve()` einmal gesetzt und von `handle_tools_call` gelesen statt erneut die Umgebungsvariable; 9 neue Tests + Counter-Probe ohne den Fix 7/9 rot — exakt die zwei gemeldeten Bugs; LXC + Ollama + C5/C7/C8 stehen aus) | 2026-09-24 (Step C Teil 1 — NVIDIA-Host-Treiber 580.126.09 installiert mit `--no-unified-memory`; pve-no-subscription-Repo ergänzt; drei dokumentierte Fehlbarkeiten auf dem Weg (Header-Paket fehlte, Backports führten denselben Upstream, Nouveau-Konflikt, uvm_hmm.c gegen 7.0.2-6-pve-Mai-Patch); eigener autoremove-Vorfall mit sudo/dkms-Verlust am 2026-09-24 wieder behoben; LXC + Ollama stehen aus) | 2026-09-24 (Backlog: ~19-min mcp-proxy.anthropic.com-Ausfall dokumentiert und geschlossen — gemessen nicht CGNAT/sharefyx-VM-seitig, Nikinger-Anordnung) | 2026-09-24 (Backlog: "opencode via Tailscale"-Behandlung für sharefyx-/Trading-Bot-VM nachgetragen, Nikinger-Feedback aus Netzwerk-Diagnosesession, kein Produktcode-Touch) | 2026-09-23 (D1/ESC-Bug auf Nikinger-Anordnung zurückgestellt, `## Backlog` neu) | 2026-09-23 (Step D code-complete — Drop-Ziel Space-Wurzel, ESC/Vollbild-Guard gebaut, gebaut in Claude Code statt opencode/M3, benannte Abweichung von P9-Q) | 2026-09-20 (Step 0 abgeschlossen — Phasenverzeichnis, INDEX-Rotationsskript, vier geplante plus drei ungeplante Doku-Defekte repariert, `doc_health.py` als Test festgenagelt, Baseline gemessen)
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
| C | Vision-Dienst auf der RTX 3060 | 🟡 **GPU-Inferenz läuft ✅** (Session-Block 2026-09-25 (2)): Host + CT 111 auf 580.173.02 inkl. `nvidia-uvm`, `size_vram` = `size`, 63 tok/s statt 0,35 · P9-21 ✅ · P9-23 ✅ (Cold 26,8 s, warm 7,0 s) · P9-26 ✅ · C6 ✅ · **offen:** Boot-Persistenz (`nvidia-uvm` + Knoten), C4 feste IP, C5 opencode-Config, C8, P9-22-Nachweis |
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

## Session stopped — 2026-09-25 (2)

**Step C Diagnose: die GPU rechnet nicht, weil CUDA gar nicht startet. Ursache ist das fehlende
Host-Modul `nvidia-uvm`, nicht Ollama und nicht das Modell.** Claude-Code-Session auf
Nikinger-Wunsch („Opus-Eskalation") — **benannte P9-Q-Abweichung**, Infra-Coarbeit war opencode/M3
zugeteilt. Kein Code-Touch, kein Service-Touch, kein `pct`/`systemctl` aus dieser Session. Gelesen
wurden nur das opencode-Protokoll der Vorsession (read-only aus `opencode.db`) und die
Ollama-API auf CT 111.

**Stand, den die Vorsession (opencode/M3, 2026-09-24/25) erreicht, aber nicht ins Repo geschrieben
hat — hier nachgetragen, Quelle: echte Ausgaben im opencode-Verlauf:**

| Punkt | Wert |
|---|---|
| Container | CT 111, Hostname `gpu-vision`, cgroup2-Allow `c 195:*`, Bind-Mounts `nvidia0`/`nvidiactl`/`nvidia-caps` |
| Adresse | `192.168.68.140/24` — **DHCP-Lease, nicht fest** (C4 offen) |
| Userspace | 580.126.09 `--no-kernel-module --no-unified-memory`, `INSTALL_EXIT=0`, `nvidia-smi -L` sieht die RTX 3060 |
| Ollama | 0.34.4 auf `0.0.0.0:11434`; von der sharefyx-VM aus gemessen 2026-09-25: `/api/version` = `0.34.4`, `/api/tags` listet `qwen3-vl:8b` (Q4_K_M, 6.140.415.879 B) |
| Last | `runner.size="5.8 GiB" runner.vram="0 B"`, `clip_ctx: CLIP using CPU backend`, `nvidia-smi` 0 MiB / 2 % |
| Durchsatz | 0,32–0,35 tok/s, Load 19,9 s, Cold-Start 23 s |
| Probiert, ohne Wirkung | fünf Env-Overrides (u. a. `OLLAMA_NUM_GPU=999`, `CUDA_VISIBLE_DEVICES=0`), `ldconfig` für die Ollama-CUDA-Libs (harmlos, zurückgelassen) |

**Die Ursache, und warum die Vorsession sie übersehen hat.** Der Container-Installer hat es
selbst gesagt: *„WARNING: The nvidia-uvm module will not be installed. As a result, CUDA will not
function with this installation of the NVIDIA driver."* Unter Linux braucht `cuInit()`
`/dev/nvidia-uvm`. Fehlt das Gerät, scheitert die CUDA-Initialisierung, und Ollama fällt still auf
CPU zurück. `nvidia-smi` redet nur über `nvidiactl`/`nvidia0`. Darum zeigte es die Karte, obwohl
CUDA nie lief. Genau diese Lücke hat „end-to-end funktioniert" vorgetäuscht.

**Datierte Korrektur [2026-09-25] zum C2-Block (Archiv, 2026-09-24, verbatim, dort nicht editiert):**
Der Satz „Ollama mit `qwen3-vl:8b` verwendet reguläres `cudaMalloc` via cuBLAS (kein UVM-Bedarf) —
Inferenz funktioniert vollständig" ist **falsch**. Ohne `nvidia-uvm` gibt es gar kein CUDA, auch
kein `cudaMalloc`. Der Trade-off „`--no-unified-memory`" war also kein Verzicht auf eine
Randfunktion, sondern der Verzicht auf die GPU-Rechnung selbst.

**Folge für den Handover-Plan „Opus-Eskalation": Versuch 1 und 2 laufen ins Leere, gemessen an
ihrer Voraussetzung.** Alle drei Hebel aus Versuch 1 (neue Ollama-Version, Modelfile
`num_gpu 999`, direkter `llama-server`) und alle drei Modelle aus Versuch 2 brauchen ein
funktionierendes `cuInit`. Keiner davon wurde ausgeführt. Dazu kommt: Hebel 1 ist in sich
verdreht. Ollama zählt 0.5 < 0.34, „0.5.x" wäre also ein Downgrade, und `install.sh` holt ohnehin
nur die neueste Version.

**Was ein echter Fix braucht, drei Schichten (Nikinger-Entscheidung, keine davon gestartet):**

1. **Host:** ein `nvidia-uvm`, das gegen den laufenden Kernel baut. Der Bruch ist
   `uvm_hmm.c: too few arguments to function 'zone_device_page_init'` gegen `7.0.2-6-pve`.
   Kandidaten: ein neuerer 580-Treiber, vermutlich zusammen mit einem neueren pve-Kernel, **oder**
   ein angepinnter älterer Kernel (6.17er), gegen den 580.126.09 vollständig baut. Beides heißt
   Reboot des 3060-Nodes.
   `[VERIFY] V165` — Forum-Angabe (Proxmox-Forum, Thread 183421): 580.159.04 / 580.173.02 bauen
   auf `7.0.14-4-pve` und neuer. Der Thread sagt **nicht** ausdrücklich, dass `nvidia-uvm` dabei
   mitbaut. Vor dem Download im entpackten Quellbaum (`--extract-only`) die Signatur von
   `zone_device_page_init` in `nvidia-uvm/uvm_hmm.c` prüfen.
2. **Container:** Userspace auf **dieselbe** neue Version, ABI-Match wie bisher, diesmal ohne
   `--no-unified-memory`.
3. **LXC-Config:** Bind-Mounts für `/dev/nvidia-uvm` und `/dev/nvidia-uvm-tools` plus ein
   cgroup2-Allow für die **uvm-Major-Nummer**. Die ist dynamisch, nicht 195. Ablesen per
   `grep nvidia-uvm /proc/devices`, nachdem das Modul geladen ist. Die Knoten müssen **vor** dem
   CT-Start auf dem Host existieren (`nvidia-modprobe -u -c=0` beim Boot). Ohne diese Schicht
   bleibt `vram=0`, auch mit repariertem Host-Treiber.

**Erste Coarbeit-Runde (read-only, bestätigt oder widerlegt die Diagnose), auf dem Host als root:**

```bash
ls -la /dev/nvidia-uvm* ; lsmod | grep -E '^nvidia' ; pct exec 111 -- python3 -c "import ctypes; print('cuInit =', ctypes.CDLL('libcuda.so.1').cuInit(0))"
```

Erwartung, wenn die Diagnose stimmt: kein `/dev/nvidia-uvm`, kein `nvidia_uvm` in `lsmod`,
`cuInit` ≠ 0 (typisch 999 oder 100). Fehlt `python3` im Template, stattdessen im Ollama-Journal
seit Boot nach den GPU-Discovery-Zeilen greppen.

**Ergebnis der read-only-Runde (Nikinger, 2026-09-25) — Diagnose bestätigt ✅:**

```
ls: cannot access '/dev/nvidia-uvm*': No such file or directory
nvidia_drm            131072  0
nvidia_modeset       1859584  1 nvidia_drm
nvidia              14684160  1 nvidia_modeset
cuInit = 999
```

Kein Gerätknoten, kein `nvidia_uvm` geladen (nur `nvidia`/`nvidia_modeset`/`nvidia_drm`),
`cuInit` liefert `999` = `CUDA_ERROR_UNKNOWN`. Alle drei Erwartungen sind eingetroffen, die
Ursache ist damit gemessen und nicht mehr nur hergeleitet.

**Zwei weitere read-only-Runden (Nikinger, 2026-09-25):**

- **Kernel:** installiert ist nur `7.0.2-6-pve` (kein Pin); verfügbar `7.0.14-15` … `7.0.14-19-pve`.
  Eine 6.17er ist nicht installiert — Option (b) Kernel-Pin entfällt praktisch.
- **V165 beantwortet ✅ (für die Bruchstelle):** 580.173.02 (Juni 2026) entpackt
  (`--extract-only`, nichts installiert). `kernel-open/conftest.sh:1428` trägt den Test
  `zone_device_page_init_has_pgmap_and_order_args`, `kernel-open/nvidia-uvm/uvm_hmm.c:81-86`
  wählt per Wrapper `nv_zone_device_page_init()` zwischen der 3-Argument-Form
  `(page, page_pgmap(page), 0)` und der alten 1-Argument-Form. Genau die Stelle, an der
  580.126.09 gebrochen ist. Ob der Rest von `nvidia-uvm` gegen `7.0.2-6-pve` baut, zeigt erst
  der DKMS-Lauf.
- **Richtung:** Treiber-Upgrade auf 580.173.02 **auf dem laufenden Kernel**, ohne
  Kernel-Wechsel — eine bewegliche Schicht statt zwei.

**Host-Fix ausgeführt (Nikinger, 2026-09-25, 22:16–22:18) ✅:**

| Runde | Ergebnis |
|---|---|
| Modul-Variante | `modinfo -F license nvidia` = `Dual MIT/GPL` (offene Module, dort sitzt der Fix) |
| Entladen | `pct stop 111`, `rmmod nvidia_drm nvidia_modeset nvidia` rc=0 — **kein Reboot nötig** |
| Install | `580.173.02 --silent --dkms --kernel-module-type=open`, **ohne** `--no-unified-memory`: `INSTALL_EXIT=0`, `dkms status` = `nvidia/580.173.02, 7.0.2-6-pve: installed`, `nvidia-uvm.ko` 62.505.432 B gebaut. Zwei Warnungen (X-Pfad, libglvnd-EGL), beide irrelevant ohne X |
| Laden | `modprobe nvidia && modprobe nvidia-uvm && nvidia-modprobe -u -c=0` rc=0; `/dev/nvidia-uvm` (511,0) + `/dev/nvidia-uvm-tools` (511,1); `nvidia-smi` = `RTX 3060, 580.173.02` |

**uvm-Major = 511, dynamisch vergeben** (nicht fest wie 195) — nach dem nächsten Host-Reboot
gegen `/proc/devices` gegenprüfen. Offen: `111.conf` um Major 511 + zwei Bind-Mounts ergänzen,
Container-Userspace auf 580.173.02 (ABI-Match), Laden von `nvidia-uvm` + Knoten beim Boot, Messung.

**Container-Seite und Messung (2026-09-25, 20:18–20:29 UTC) ✅:**

- `111.conf` +3 Zeilen: `lxc.cgroup2.devices.allow: c 511:* rwm` plus Bind-Mounts
  `/dev/nvidia-uvm` und `/dev/nvidia-uvm-tools` (`optional,create=file`). Danach zwei
  `devices.allow` und fünf `mount.entry`, keine Dubletten.
- Userspace im CT: 580.173.02 `--no-kernel-module` (ohne `--no-unified-memory`),
  `INSTALL_EXIT=0`, im CT `cuInit = 0` (vorher 999).
- Ollama-Discovery, Debug-Instanz auf `127.0.0.1:11435`: `inference compute … library=CUDA
  … RTX 3060 … libdirs=ollama,cuda_v13 driver=13.0 total="11.6 GiB"`. Die erste
  Service-Journalzeile nach dem Start zeigte noch `library=cpu total="8.0 GiB"` — das waren die
  8 GiB **Container-RAM** unter dem CPU-Eintrag. Warum ausgerechnet dieser Start (PID 147) keine
  GPU fand, ist **nicht geklärt**; ab dem nächsten Service-Start stimmt es (Messung unten).
- Die Env-Overrides der Vorsession stehen **nicht mehr** in der Unit (`systemctl cat` zeigt nur
  `PATH`, `OLLAMA_HOST=0.0.0.0:11434`, `OLLAMA_ORIGINS=*`).

**Messung von der sharefyx-VM aus (Claude Code, `vision_ollama.py --endpoint http://192.168.68.140:11434`):**

| Messung | Vorher | Jetzt |
|---|---|---|
| `/api/ps` | `size_vram` 0 | `size_vram` = `size` = 5.793.780.858 B — **komplett im VRAM** |
| Decode | 0,32–0,35 tok/s | **63,15 tok/s** |
| Erster Load nach Service-Start (Platte kalt) | — | 48,3 s Wand, davon 33,4 s Load |
| Vision-Lauf, Modell entladen (`keep_alive:0`), Cold-Start | 46–180 s (i5-CPU, 2026-09-10) | **26,8 s** |
| Vision-Lauf, Modell geladen | — | **7,0 s** |
| P9-26-Aussage (`c4_p8519_01_radiogruppe_im_dialog.png`) | „Der Radio-Button ‚als Text-Link im Text' ist markiert" | „Der Radio-Button „als Text-Link im Text" ist im Dialog markiert." — **gleiche Aussage** |

Abnahme damit: **P9-21 ✅** (antwortet von der sharefyx-VM aus) · **P9-23 ✅** · **P9-26 ✅** ·
V156: beim alten Modell geblieben, wie empfohlen, damit der Gewinn zuzuordnen ist.
**P9-22 nicht nachgewiesen:** `0.0.0.0:11434` hängt nur im Heim-LAN hinter CGNAT, ohne
Funnel und ohne Port-Forward. Ein ausdrücklicher Test von außen fehlt noch. `OLLAMA_ORIGINS=*`
ist im LAN hinnehmbar, notiert.

**Offen, und ohne diesen Punkt überlebt der Fix keinen Host-Reboot:** `nvidia-uvm` wird heute von
Hand geladen, die Knoten legt `nvidia-modprobe -u -c=0` von Hand an. Nötig sind:
`/etc/modules-load.d/` mit `nvidia` + `nvidia-uvm` und eine Oneshot-Unit, die
`nvidia-modprobe -u -c=0` **vor** dem CT-Autostart ausführt. Danach die uvm-Major
gegen `/proc/devices` gegenprüfen (511 ist dynamisch vergeben). Außerdem offen: C4 feste IP ·
C5 `LOCAL_VISION_ENDPOINT` in `~/.config/opencode/` · C8 CPU-Ollama auf der sharefyx-VM
(läuft weiter auf `127.0.0.1:11434`) · `/tmp/nv580173` und der alte 580.126.09-Installer auf dem
Host löschen.

**Zur Einordnung der Messwerte:** Die 23 s Cold-Start (C7) sind ein **CPU**-Lauf auf dem
Ryzen 7 5800X. Er ist schneller als die 46–180 s auf dem i5-VM-CPU-Pfad, aber **kein GPU-Gewinn**.
P9-23 darf damit nicht als erfüllt gelten.

**Doku in diesem Commit:** Modulstatus C nachgezogen · diese Korrektur · Rotation per Skript ·
INDEX-Phase-9-Zeile + `updated:`-Kette (per `rotate_index_updates.sh`) · V165 neu.

**Boot-Persistenz eingerichtet (Nikinger, 2026-09-25) — Reboot-Probe steht aus:**
`/etc/modules-load.d/nvidia.conf` (`nvidia`, `nvidia-uvm`) · `/etc/systemd/system/nvidia-uvm-nodes.service`
(Oneshot, `ExecStart=/usr/bin/nvidia-modprobe -c=0 -u`, `After=systemd-modules-load.service`,
`Before=pve-guests.service`, `enabled`) · CT 111 stand auf **`onboot: 0`**, wäre also nach einem
Reboot gar nicht gestartet.

**Nächster Schritt (Folge-Session, Coarbeit):** Die GPU-Inferenz läuft **jetzt** auch ohne Reboot.
Der Reboot beweist nur, dass sie ihn übersteht. Auf dem 3060-Host als root:

```bash
pct set 111 --onboot 1 && pct config 111 | grep -E '^onboot' && reboot
```

Danach, alles read-only:

```bash
systemctl is-active nvidia-uvm-nodes.service; lsmod | grep -E '^nvidia_uvm'; grep nvidia-uvm /proc/devices; ls -la /dev/nvidia-uvm*; pct status 111; pct exec 111 -- python3 -c "import ctypes; print('cuInit =', ctypes.CDLL('libcuda.so.1').cuInit(0))"
```

Erwartet: `active` · `nvidia_uvm` geladen · **`511 nvidia-uvm`** (sonst stimmt
`lxc.cgroup2.devices.allow: c 511:*` in `111.conf` nicht mehr) · beide Knoten · `running` ·
`cuInit = 0`. Danach von der sharefyx-VM aus `curl http://192.168.68.140:11434/api/ps` nach
einem Lauf: `size_vram` = `size`. Dann C4 → C5 → C8, Aufräumen `/tmp/nv580173` + alter
580.126.09-Installer auf dem Host. Der Host-Pfad ist entschieden: **(a) nur Treiber-Upgrade,
ohne Kernel-Wechsel**, und er lief ohne Reboot.
