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
updated: 2026-09-25 (V165 beantwortet: 580.173.02 kennt die neue `zone_device_page_init`-Signatur) | 2026-09-25 (Step C Diagnose bestätigt: kein `/dev/nvidia-uvm`, `cuInit = 999`) | 2026-09-25 (Step C Diagnose, Claude Code: CUDA fehlt, weil `nvidia-uvm` fehlt — C2-Trade-off-Satz datiert korrigiert, Modulstatus C nachgezogen, Nikinger-Entscheidung zum Host-Fix offen) | 2026-09-25 (Backlog aufgeräumt: „opencode via Tailscale" für sharefyx-VM per Nikinger-Update mittlerweile passiert, Eintrag aus der Backlog-Sektion entfernt; nur noch D1 zurückgestellt) | 2026-09-25 (Step C Teil 2 / C6 — `mcp_local_vision_server.py` Skript-Fixes aus Plan §5.3: `serve()` loggt aufgelösten Endpoint, `--endpoint` wirkt jetzt auch ohne `--check`; neue zentrale `resolve_endpoint(args)` mit Präzedenz `--endpoint` > `$LOCAL_VISION_ENDPOINT` > `DEFAULT_ENDPOINT`; `_CURRENT_ENDPOINT` als Modul-Globals wird in `serve()` einmal gesetzt und von `handle_tools_call` gelesen statt erneut die Umgebungsvariable; 9 neue Tests + Counter-Probe ohne den Fix 7/9 rot — exakt die zwei gemeldeten Bugs; LXC + Ollama + C5/C7/C8 stehen aus) | 2026-09-24 (Step C Teil 1 — NVIDIA-Host-Treiber 580.126.09 installiert mit `--no-unified-memory`; pve-no-subscription-Repo ergänzt; drei dokumentierte Fehlbarkeiten auf dem Weg (Header-Paket fehlte, Backports führten denselben Upstream, Nouveau-Konflikt, uvm_hmm.c gegen 7.0.2-6-pve-Mai-Patch); eigener autoremove-Vorfall mit sudo/dkms-Verlust am 2026-09-24 wieder behoben; LXC + Ollama stehen aus) | 2026-09-24 (Backlog: ~19-min mcp-proxy.anthropic.com-Ausfall dokumentiert und geschlossen — gemessen nicht CGNAT/sharefyx-VM-seitig, Nikinger-Anordnung) | 2026-09-24 (Backlog: "opencode via Tailscale"-Behandlung für sharefyx-/Trading-Bot-VM nachgetragen, Nikinger-Feedback aus Netzwerk-Diagnosesession, kein Produktcode-Touch) | 2026-09-23 (D1/ESC-Bug auf Nikinger-Anordnung zurückgestellt, `## Backlog` neu) | 2026-09-23 (Step D code-complete — Drop-Ziel Space-Wurzel, ESC/Vollbild-Guard gebaut, gebaut in Claude Code statt opencode/M3, benannte Abweichung von P9-Q) | 2026-09-20 (Step 0 abgeschlossen — Phasenverzeichnis, INDEX-Rotationsskript, vier geplante plus drei ungeplante Doku-Defekte repariert, `doc_health.py` als Test festgenagelt, Baseline gemessen)
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
| C | Vision-Dienst auf der RTX 3060 | 🟡 **Blockiert am Host-Modul `nvidia-uvm`, siehe Session-Block 2026-09-25 (2).** C1 Host-Treiber 580.126.09 ✅ (aber ohne `nvidia-uvm`, und damit **ohne CUDA**) · C6 ✅ · C2 LXC CT 111 `gpu-vision` ✅ · C3 Userspace + Ollama 0.34.4 + `qwen3-vl:8b` laufen, **Inferenz aber nur auf CPU** (`runner.vram="0 B"`) 🟡 · C7 23 s gemessen = **CPU-Lauf auf dem Ryzen, kein GPU-Gewinn** · C4/C5/C8/P9-26 offen |
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

**Zur Einordnung der Messwerte:** Die 23 s Cold-Start (C7) sind ein **CPU**-Lauf auf dem
Ryzen 7 5800X. Er ist schneller als die 46–180 s auf dem i5-VM-CPU-Pfad, aber **kein GPU-Gewinn**.
P9-23 darf damit nicht als erfüllt gelten.

**Doku in diesem Commit:** Modulstatus C nachgezogen · diese Korrektur · Rotation per Skript ·
INDEX-Phase-9-Zeile + `updated:`-Kette (per `rotate_index_updates.sh`) · V165 neu.

**Nächster Schritt:** Nikinger entscheidet den Host-Pfad: **(a)** neuerer 580er + neuerer
pve-Kernel, **(b)** Kernel-Pin auf eine 6.17er-Version oder **(c)** Versuch 3, also P9-26 auf CPU
mit 0,32 tok/s durchziehen und den GPU-Fix mit Messbefund nach P10 schieben. Vorher die
read-only-Runde oben.
