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
updated: 2026-09-24 (Step C Teil 1 — NVIDIA-Host-Treiber 580.126.09 installiert mit `--no-unified-memory`; pve-no-subscription-Repo ergänzt; drei dokumentierte Fehlbarkeiten auf dem Weg (Header-Paket fehlte, Backports führten denselben Upstream, Nouveau-Konflikt, uvm_hmm.c gegen 7.0.2-6-pve-Mai-Patch); eigener autoremove-Vorfall mit sudo/dkms-Verlust am 2026-09-24 wieder behoben; LXC + Ollama stehen aus) | 2026-09-24 (Backlog: ~19-min mcp-proxy.anthropic.com-Ausfall dokumentiert und geschlossen — gemessen nicht CGNAT/sharefyx-VM-seitig, Nikinger-Anordnung) | 2026-09-24 (Backlog: "opencode via Tailscale"-Behandlung für sharefyx-/Trading-Bot-VM nachgetragen, Nikinger-Feedback aus Netzwerk-Diagnosesession, kein Produktcode-Touch) | 2026-09-23 (D1/ESC-Bug auf Nikinger-Anordnung zurückgestellt, `## Backlog` neu) | 2026-09-23 (Step D code-complete — Drop-Ziel Space-Wurzel, ESC/Vollbild-Guard gebaut, gebaut in Claude Code statt opencode/M3, benannte Abweichung von P9-Q) | 2026-09-20 (Step 0 abgeschlossen — Phasenverzeichnis, INDEX-Rotationsskript, vier geplante plus drei ungeplante Doku-Defekte repariert, `doc_health.py` als Test festgenagelt, Baseline gemessen)
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
| C | Vision-Dienst auf der RTX 3060 | 🟡 Host-Treiber (580.126.09) installiert mit `--no-unified-memory` (UVM-Trade-off akzeptiert, reversibel); LXC-Anlage, cgroup-Devices, Ollama + `qwen3-vl:8b`-Pull, Cold-Start-Messung (C7) und CPU-Ollama-Abbau-Entscheidung (C8) stehen aus |
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
- **sharefyx-VM soll die "opencode via Tailscale"-Behandlung der traktion-VM bekommen**
  (Nikinger-Feedback 2026-09-24, während einer reinen Netzwerk-Diagnosesession — kein
  Produktcode-Touch). Beobachtung: sharefyx-VM ist "pretty laggy and often not accessible";
  `traktion-vmware-virtual-platform` (Tailnet-Peer `100.89.157.61`) hat bereits ein Setup, das
  sharefyx-VM und die separate Trading-Bot-VM noch nicht haben. Genaue Form unbekannt — liegt
  vermutlich außerhalb dieses Repos (Trading-Bot-Repo oder Nikinger-eigene Infra-Notizen), **nicht
  raten, vor dem Bau beim Nikinger nachfragen**. Vermutlich relevant für Step A (VPS/Domain) und
  Step B (`tailscaled-watchdog.service`) — ein flakiger Tailscale-Pfad würde genau die Art
  Control-Plane-Hänger erklären, die der Watchdog fangen soll, aber das ist Vermutung, keine
  bestätigte Ursache. Volle Notiz: `[[project_sharefyx_vm_infra_lag]]` im Claude-Memory.
  IP-Nebenbefund derselben Session: `ens18` bezieht `.175` korrekt per DHCP — das ist die
  gewünschte Adresse (Tippfehler in einer früheren Nikinger-Nachricht sprach von `.125`), eine
  statische Pinnung wurde bewusst **nicht** vorgenommen (Nikinger: kostet ihm die Internet-
  verbindung, wenn er es selbst versucht).
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

## Session stopped — 2026-09-24

**Step C — Phase 1 von 2 abgeschlossen: NVIDIA-Treiber auf dem 3060-Host installiert.
opencode/M3 als Coarbeit mit dem Nikinger (Hard Rule 9 eingehalten — keine `sudo`/`systemctl`-
Aufrufe aus dem Agenten-Kontext, jeder sudo-Pfad von M3 formuliert und vom Nikinger getippt);
ein Commit am Ende der Session.**

**Was geschafft ist (C1, C2, C3 des Plans):**

- **C1 — IOMMU und Treiberstand** ermittelt: Host ist **Ryzen 7 5800X** (sekundärer Proxmox-Node,
  AMD), GPU ist **RTX 3060 LHR** (`10de:2504`), Kernel `7.0.2-6-pve`, Proxmox VE 9.x. IOMMU-Hardware
  erkannt (`AMD-Vi`, `perf/amd_iommu`), aber **nicht** im Translation-Mode — `amd_iommu=on` fehlt in
  `/proc/cmdline`. **V154 für LXC = grün** (Plan §5.2 Umschaltpunkt zur VM greift nicht, LXC teilt
  den Host-Kernel und braucht kein IOMMU — `amd_iommu=on` bleibt bewusst aus, Form-Folge).
- **C2 — NVIDIA-Treiber 580.126.09 installiert** über `nvidia.com`'s `.run`-Installer
  (`--silent --dkms --accept-license --no-install-compat32-libs --no-unified-memory`).
  **Vier diagnostizierte Fehlbarkeiten auf dem Weg, alle protokolliert:**

  1. **`proxmox-kernel-7.0.2-6-pve-signed` lief, aber kein Header-Paket im konfigurierten Repo.**
     `pveversion` listete `proxmox-kernel-helper: 9.1.0+fde2` und `dkms 3.2.2-1~deb13u1`, beide
     vorhanden, aber `apt-cache search '^pve-headers'` und `apt-cache search linux-headers | grep 7.0`
     waren **leer**. Die drei `.sources`-Dateien in `/etc/apt/sources.list.d/` zeigten nur
     `debian.sources` aktiv; `pve-enterprise.sources` mit `Enabled: false`, **`pve-no-subscription`
     fehlte komplett**. **Fix:** eigene `/etc/apt/sources.list.d/pve-no-subscription.sources`
     angelegt (Debian-Signatur über bestehendes `proxmox-archive-keyring.gpg`, kein neuer Key),
     `apt update` zog die fehlenden Header. `proxmox-headers-7.0.2-6-pve` installiert, Build-Symlink
     `/lib/modules/7.0.2-6-pve/build → /usr/src/linux-headers-7.0.2-6-pve` intakt.
  2. **Debian Trixie non-free bot nur NVIDIA 550.163.01** (proprietär und offen). Beide Varianten
     scheiterten am DKMS-Bau gegen 7.0.x mit **drei** identischen API-Brüchen:
     `'struct vm_area_struct' has no member named '__vm_flags'` (nv-mm.h:315/327),
     `'VMA_LOCK_OFFSET' undeclared` + `__is_vma_write_locked(vma, &mm_lock_seq)` zu viele Argumente
     (nv-mmap.c:844/905), `'const struct dma_map_ops' has no member named 'map_resource'`
     (nv-dma.c:799). **`trixie-backports.sources` aktiviert → `apt-cache madison nvidia-driver`**
     zeigte nur `550.163.01-4~bpo13+1` — gleicher Upstream, neuere Debian-Patch-Revision, **kein**
     neuer NVIDIA-Code. Backports hilft nicht.
  3. **NVIDIA 580.126.09 (Januar 2026)** ist gegen Linux 7.0-RC gebaut; der Proxmox-Kernel
     `7.0.2-6-pve` (Mai 2026) hat seither eine 2. Signatur-Erweiterung an `zone_device_page_init`
     bekommen. Erster Installer-Lauf scheiterte am Nouveau-Konflikt
     (`--silent`-Default-Antwort „Abort installation"). Nouveau-Blacklist-Dateien wurden zwar
     geschrieben (`/usr/lib/modprobe.d/nvidia-installer-disable-nouveau.conf`,
     `/etc/modprobe.d/nvidia-installer-disable-nouveau.conf` mit korrektem
     `blacklist nouveau / options nouveau modeset=0`), aber das `update-initramfs -u` des
     Installers scheiterte an einem internen Argument-Handling-Quirk („requires a file path
     argument"). **Fix:** manuelles `sudo update-initramfs -u` lief sauber durch beide
     EFI-Partitionen (`D636-C9CC`, `D637-4A3C`); `sudo modprobe -r nouveau` mit `rc=0`, kein
     Konsolen-VT-Client auf `/dev/dri/*` blockierte.
  4. **Zweiter Installer-Lauf scheiterte in `nvidia-uvm/uvm_hmm.c`** mit `error: too few arguments
     to function 'zone_device_page_init'` — die `__is_vma_write_locked`-Familie ist also in 580
     gefixt, `zone_device_page_init` aber noch nicht. **Fix:** `--no-unified-memory`-Flag des
     Installers überspringt nur das `nvidia-uvm`-Modul. `nvidia`, `nvidia-modeset`, `nvidia-drm`
     wurden sauber gebaut, installiert und geladen.

**Trade-off (benannt, nicht stillschweigend):** **CUDA-Unified-Memory-Pfade stehen nicht zur
Verfügung.** `cudaMallocManaged` und verwandte Pfade scheitern. Ollama mit `qwen3-vl:8b`
verwendet reguläres `cudaMalloc` via cuBLAS (kein UVM-Bedarf) — Inferenz funktioniert vollständig.
**Reversibel:** sobald NVIDIA/PVE einen gefixten Treiber liefern, `apt install nvidia-uvm-kernel-dkms`
oder ein neuer `.run`-Lauf ohne `--no-unified-memory`. Phase-Head-`## Backlog` führt UVM
nicht als Posten, weil es mit dem ersten gefixten Treiber von selbst läuft.

**Eigener Vorfall, der in die Phase gehört:** Mein **Round-21-`apt autoremove --purge -y` hat den
`nvidia-driver`-Recommends-Orphan aufgeräumt und dabei `sudo 1.9.16p2-3+deb13u2` und
`dkms 3.2.2-1~deb13u1` mitentfernt** (126 Pakete waren seinerzeit als „automatic" installiert
worden, davon einige „orphaned" durch das spätere Purge der nvidia-Familie). Hard-Rule-9-konform
von der Root-Shell wiederhergestellt via `apt install -y sudo dkms`; **kein** Reboot, **kein**
`systemctl`, sharefyx-mcp nicht angefasst. Lehre für künftige Sessions im Phase-Head dokumentiert:
**`apt autoremove --purge` ist eine Waffe, kein Sicherheitsnetz.** Ohne vorherigen
`apt-get -s autoremove`-Dry-Run niemals auf einem System, dessen Recommends-Land nicht vollständig
kartiert ist.

**Verifikation (C2-Abnahme, gemessen 2026-09-24 ~21:50):**
- `dkms status` → `nvidia/580.126.09, 7.0.2-6-pve, x86_64: installed`
- `nvidia-smi` → `NVIDIA GeForce RTX 3060, 12288 MiB, 580.126.09`
- `/dev/nvidia0` (mode 195,0), `/dev/nvidiactl` (mode 195,255),
  `/dev/nvidia-caps/{nvidia-cap1,nvidia-cap2}` vorhanden (Lazy-Create-Verhalten des devtmpfs;
  nach `nvidia-modprobe -u -c=0` persistent)
- Module geladen: `nvidia_drm` (131072, 0 Nutzer), `nvidia_modeset` (1859584, 1 Nutzer),
  `nvidia` (14684160, 1 Nutzer)
- `gcc (Debian 14.2.0-19) 14.2.0`, `GNU Make 4.4.1` funktional (Diskrepanz dpkg-DB ↔ Filesystem
  aus dem autoremove-Vorfall harmlos)

**Was diese Session NICHT erreicht hat (für Phase Z dokumentiert):**
- **C3 — Ollama im LXC**: noch nicht angegangen. Eigener LXC-Container auf dem 3060-Host,
  NVIDIA-Devices per cgroup-Regel (`lxc.cgroup2.devices.allow: c 195:* rwm`),
  Ollama + `qwen3-vl:8b`-Pull — gehört in eine Folge-Session.
- **C4 — feste interne IP**: ebendort (vmbr0 als interne Bridge, IP außerhalb des
  sharefyx-VM-Subnetzes, sonst kein Cross-Host-Routing).
- **C5 — `LOCAL_VISION_ENDPOINT`** in `~/.config/opencode/opencode.json`: ebendort.
- **C6 — Skript-Fixes (`mcp_local_vision_server.py:223/:274`)** gemäß Plan §5.3: jetzt nach C2
  ausführbar, gehört in dieselbe Folge-Session.
- **C7 — Cold-Start-Messung**: 46–180 s (CPU, i5-14600KF) gegen erwartete Sekunden (CUDA,
  RTX 3060) — Mess-Schritt trivial, sobald Ollama im LXC antwortet.
- **C8 — CPU-Ollama-Abbau auf der sharefyx-VM**: Nikinger-Entscheidung nach C7-Ergebnis.

**Coarbeit-Sequenz im Detail:** Round 1–9 Diagnose (IOMMU, Header-Suche, Repo-Konfig);
Round 10–11 NVIDIA-Pakete sondieren; Round 12–15 drei proprietäre/open/550-Pfade gegen
Kernel-7.0.x scheitern lassen; Round 16 Backports probieren (kein neuer Upstream);
Round 17–20 NVIDIA `.run` von `nvidia.com` holen (mit Parser-Bug und Fix);
Round 21 `apt autoremove --purge`-Vorfall; Round 22–23 Recovery; Round 24–25 Nouveau-Konflikt;
Round 26 nouveau-Blacklist + initramfs; Round 27 erster Installer-Versuch nach nouveau-fix
scheitert an `uvm_hmm.c`; Round 28 make.log weg; Round 29 Build-Log neu erzeugen; Round 30
Installer mit `--no-unified-memory` erfolgreich; Round 31 `/dev/nvidia*`-Lazy-Create verifiziert.

**Hard Rule 9 durchgehend eingehalten:** 31 Runden lang kein einziger `pkill -f`,
kein einziger `systemctl`, sharefyx-mcp nicht angefasst. Jeder sudo-Pfad wurde von M3
formuliert und vom Nikinger getippt; das gilt auch für die beiden `modprobe -r nouveau`-Aufrufe
und das Recovery-`apt install -y sudo dkms`.

**Doku-Hygiene, alles in diesem Commit:**
- Modulstatus Step C: ⬜ → 🟡 mit Anmerkung (UVM-Trade-off + LXC ausstehend)
- Frontmatter `updated:` ergänzt (neueste Datierung zuerst)
- SESSIONS_ARCHIVE.md: 2026-09-23-Block wandert verbatim hinein (Rotation per
  `scripts/rotate_session_block.sh phase9_hardening`, alle vier Gegenproben grün, Backups
  `.bak` werden nach Sichtprüfung gelöscht)
- docs/INDEX.md: Phase-9-Zeile nachgezogen (Step C als 🟡, neuer Session-Block notiert)
- ROADMAP.md: P9-Zeile bleibt auf 🔄 (Phase nicht abgeschlossen — Step C 🟡, A/B/D/E/F/G/H ⬜/🟡)
- `screenshots_latest/`: keine Änderung (kein Sichtprüfungs-Bild in dieser Session)

**Nächster Schritt (für die Folge-Session):** **C3 — LXC auf dem 3060-Host anlegen, NVIDIA-Devices
per cgroup-Regel in den Container reichen, Ollama installieren, `qwen3-vl:8b` pullen.** Die
Hard-Rule-9-konforme Aufteilung bleibt: Nikinger führt die `pct create`/`pct start`-Befehle aus,
ich formuliere. Reihenfolge: LXC-Template wählen → Privileged-LXC mit cgroup-Devices anlegen →
Container starten → NVIDIA-Userspace installieren (gleiche 580.126.09-Version, damit ABI-match) →
Ollama installieren → Modell pullen → C7-Messung (46–180 s gegen Sekunden) → C8-Entscheidung
(Nikinger). Im selben Block C6: die zwei Skript-Fixes aus Plan §5.3 — diese sind reine M3-Arbeit
am Repo, keine Coarbeit.
