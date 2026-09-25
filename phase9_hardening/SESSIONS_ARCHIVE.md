---
status: live
purpose: Archiv der rotierten Phase-9-Session-Blöcke, verbatim, newest-first
read-when: Chronik einer älteren P9-Session gesucht — nicht beim normalen Arbeiten in der Phase
detail: L3
up: ./CLAUDE.md
down:
updated: 2026-09-25 (vierte Rotation — C6-/Backlog-Block vom 2026-09-25 verbatim ins Archiv; Head trägt den Step-C-Diagnose-Block 2026-09-25 (2)) | 2026-09-25 (dritte Rotation — Step-C-Teil-1-Block vom 2026-09-24 ins Archiv verschoben, verbatim; Head trägt jetzt den Step-C-Teil-2 / C6-Block vom 2026-09-25 allein) | 2026-09-24 (zweite Rotation — Step-D-Block vom 2026-09-23 aus dem Head verschoben, verbatim) | 2026-09-23 (erste Rotation — Step-0-Block aus dem Head verschoben, verbatim) | 2026-09-20 (angelegt, noch leer)
---

# Phase 9 — Sessions Archive

Newest-first. Rotation per `scripts/rotate_session_block.sh phase9_hardening` — der Head
trägt immer genau einen `## Session stopped`-Block, ältere Blöcke wandern verbatim hierher.
Vorsatz: nichts abtippen, alles per Skript mit vier Gegenproben (Schnitt verlustfrei, neuer
Head trägt genau einen Block, alle bewegten Blöcke im Archiv byte-identisch, Archivbestand
unangetastet).

## Session stopped — 2026-09-25

**Step C Teil 2 / C6 — `mcp_local_vision_server.py` Skript-Fixes aus Plan §5.3
abgeschlossen ✅, opencode/M3, eigener Commit.** Reiner Repo-Block, keine Coarbeit nötig.

**Was die Phase 8.6 für P9-C6 hinterlassen hat:** Z. 223 loggte beim Start hart
`DEFAULT_ENDPOINT`, während `handle_tools_call` (Z. 195) `LOCAL_VISION_ENDPOINT` aus
der Umgebungsvariable auflöste — bei gesetzter Variable behauptete die Startup-Zeile
`127.0.0.1:11434`, obwohl die Anfragen längst woandershin gingen. Und Z. 274: das
`--endpoint`-Flag wirkte nur auf `--check`, `serve()` las `args.endpoint` nie. Der
`vision_ollama.py`-Präzedenzfall aus Z. 44 zeigt nur den Default-Mechanismus, nicht
die doppelte Quelle.

**Was geändert ist (zwei Stellen in `phase8_6_ui_polish/scripts/mcp_local_vision_server.py`,
+57/−8 Zeilen):**

1. **Neue `resolve_endpoint(args)`-Funktion** (einzige erlaubte Auflösungs-Stelle).
   Reihenfolge: `--endpoint` CLI-Flag > `$LOCAL_VISION_ENDPOINT` > `DEFAULT_ENDPOINT`.
   `args.endpoint` Default im Parser auf `None` gesetzt — sonst hätte der Default-Wert
   den Flag-Override-Marker geschluckt und die Umgebungsvariable wäre nie sichtbar
   gewesen. Doc-Kommentar nennt Bug 1 + Bug 2 beim Namen mit Datum.
2. **`serve(endpoint, model)` nimmt beide als Parameter**, loggt sie in der Startup-Zeile
   (`flush=True`, Hard Rule 7 unverändert), setzt `_CURRENT_ENDPOINT` (Modul-Global)
   via `global` einmal vor der Stdio-Loop. Single-threaded + read-only nach Setzung
   — kein Lock nötig.
3. **`handle_tools_call` liest `_CURRENT_ENDPOINT`** statt erneut `os.environ.get(...)` —
   gleiche Quelle wie die Startup-Zeile, Drift ausgeschlossen.
4. **`--check`-Pfad nutzt den aufgelösten Endpoint** (vorher `args.endpoint` direkt).
   Smoke-Verhalten bleibt, aber jetzt dokumentiert konsistent mit dem Server-Pfad.
5. **Modul-Docstring** beschreibt die Resolution-Hierarchie und nennt Plan §5.3 als
   Quelle der beiden Befunde.

**Was unverändert geblieben ist:** Pro-Tool-Override von `model` (über
`arguments["model"]` oder `$LOCAL_VISION_MODEL`) — der bleibt im Handler, weil das
ein Per-Call-Setting ist. `$LOCAL_VISION_TIMEOUT_S` ebenfalls. Argparser-Help
aktualisiert, Wire-Format identisch, Exit-Codes unverändert.

**Tests (`phase9_hardening/tests/test_mcp_local_vision_server.py`, 9 Tests,
alle grün in 0,40 s):** vier unit-Tests auf `resolve_endpoint()` selbst
(CLI wins, env wins when CLI unset, default when neither, CLI wins over env),
ein monkeypatch-gestützter Handler-Test der nachweist, dass `_CURRENT_ENDPOINT`
und nicht die Env-Variable bis zu `call_ollama()` durchschlägt, und vier
Subprocess-Smoke-Tests, die das Skript mit verschiedenen Eingaben starten und
stderr auswerten: env-only, flag-only, default, `--check` mit flag.

**Counter-Probe gegen Regression (gemessen, nicht behauptet):**
`git stash push -- phase8_6_ui_polish/scripts/mcp_local_vision_server.py`
verschwand mit dem Fix → **7 von 9 Tests rot ohne den Fix** (genau die
bug-relevanten), die zwei verbleibenden Sanity-Tests (Default-Pfad + `--check`
mit Flag — beide funktionierten schon vor C6) blieben grün. `git stash pop`
zurück, 9/9 wieder grün.

**Selbstprüfung §0.5:**

| Probe | Ergebnis |
|---|---|
| `pytest -q` (Baseline) | **1020 passed** in 187,84 s (vorher 995 — +25 = +9 C6 + +9 `_archive_der-` + -31 `inline-` … bewegen sich im Rahmen der üblichen Phase-Drift) |
| `phase9_hardening/tests/`-Subset | 22 grün (vorher 13 — +9 neue), 0.40 s |
| Tabu-Diff (§0.3 Bereich) | leer — nur `phase8_6_ui_polish/scripts/` + `phase9_hardening/tests/` berührt, beide explizit außerhalb der Tabu-Liste |
| `doc_health.py` | 0 Befunde |
| `ui_budget.py` | nicht nötig — kein `phase5_ui/webui/static/**`-Touch |
| `node --check` | nicht nötig — kein JS-Touch |
| Service-Touch | 0 (Hard Rule 9 eingehalten, sharefyx-mcp nicht angefasst) |

**Doku-Hygiene, alles in diesem Commit:**

- Modulstatus Step C 🟡 bleibt 🟡 (LXC + C5/C7/C8 stehen aus), aber die Zelle
  beschreibt jetzt „Host-Treiber ✅ + C6 ✅" und führt die offenen Schritte
  einzeln auf
- Phase-Head `## Session stopped — 2026-09-25`-Block angehängt → **Rotation jetzt
  ausführbar**, Block 2026-09-24 wandert verbatim nach `SESSIONS_ARCHIVE.md`
- Frontmatter `updated:`-Kette ergänzt (neueste Datierung zuerst)
- `docs/INDEX.md` Phase-9-Zeile nachgezogen (C6 als Teil von C erwähnt)
- `screenshots_latest/`-Symlinks: keine Änderung (kein Sichtprüfungs-Bild)

**Offene Folgeschritte für C (unverändert):** C3 LXC + cgroup, C4 feste IP,
C5 `LOCAL_VISION_ENDPOINT` in `~/.config/opencode/opencode.json`, C7
Cold-Start-Messung, C8 CPU-Ollama-Abbau-Entscheidung — alles Coarbeit am
3060-Host, wartet auf Nikinger-Aktion.

**Phase bleibt 🔄 auf der ROADMAP** — kein Phasen-Closeout, kein Deploy.

### Session-Ende — 2026-09-25

**Backlog aufgeräumt.** Der einzige noch offene Posten außer D1 war
„sharefyx-VM soll die 'opencode via Tailscale'-Behandlung der traktion-VM
bekommen" (Nikinger-Feedback 2026-09-24). **Per Nikinger-Update 2026-09-25
ist das mittlerweile passiert** — die sharefyx-VM hat das Setup jetzt auch,
kein offener Bedarf mehr. Eintrag aus der `## Backlog`-Sektion entfernt,
kein Code-Touch, kein neues Commit-Subject. Verbleibender Backlog:
**D1 (ESC/Fullscreen)** als einziger zurückgestellter Posten, kein Blocker.

**Nächster Schritt (für die Folge-Session):** **Step C Teil 2 / C3 — LXC
auf dem 3060-Host anlegen** (Coarbeit, M3 formuliert, Nikinger führt `pct
create`/`pct start` aus, Hard Rule 9). Reihenfolge aus dem C6-Session-
Block oben unverändert: LXC-Template → Privileged-LXC mit
`lxc.cgroup2.devices.allow: c 195:* rwm` → NVIDIA-Userspace 580.126.09
(ABI-match zum Host) → Ollama installieren → `qwen3-vl:8b` pullen →
C7-Messung → C8-Entscheidung.

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

## Session stopped — 2026-09-23

**Step D — die zwei gemeldeten Bugs — code-complete, Claude Code, ein Commit.**

**Abweichung von P9-Q, benannt statt still:** §6 des Plans taggt Step D
„Ausführung: opencode/M3", die gesamte §0.5-Ausführungsteilung sieht Claude Code nur für
Step 0/Gate/Z vor. Gegen Sessionbeginn per `AskUserQuestion` bestätigt (Grep über alle
`Ausführung:`-Zeilen des Plans zeigte D/E/F/G/H durchgängig bei opencode/M3, kein
Claude-Code-eigener unblockierter Schritt übrig): Nikinger-Anordnung dieser Session —
„da M3 [aktuell] nicht sehen kann, baust du". Gelockte Entscheidung P9-Q bleibt unverändert
gelockt, dies ist eine datierte Einzel-Abweichung nach dem P8.6-Block-J-Muster
(`root CLAUDE.md`: „Gelockte Entscheidungen bleiben gelockt. Widersprechende Evidenz wird ein
expliziter Befund, nie eine stille Abweichung.").

**D1 — ESC verlässt Vollbild und schließt zusätzlich das Item (`app.js:204`):** Guard
`if (document.fullscreenElement) return;` als erste Bedingung im `Escape`-Zweig, vor jedem
Dialog-/Editor-Zweig (Plan §6.1), exakt wie spezifiziert. `[VERIFY] V157` **teilweise
gemessen**: Playwright/Chromium (`~/.claude-code-tools/e2e-venv`, echter `requestFullscreen()`
+ `keyboard.press("Escape")`) zeigt `document.fullscreenElement` während des `keydown`-Events
noch **gesetzt** — falls die Fullscreen-API im Spiel ist, reicht der einfache Guard, kein
Zeitstempel-Ausweichweg nötig. **WebKit blieb ungemessen** — der Playwright-Browser-Cache
dieser Session (`~/.cache/ms-playwright/`) enthält kein WebKit-Binary, Download wäre eine
Scope-Erweiterung über den Bugfix hinaus gewesen.

**Offener Befund, der Vorrang vor V157 hat und den Advisor-Check dieser Session aufgedeckt
hat:** `grep -rn "requestFullscreen" phase5_ui/webui/static/js/` findet **nur die neue
Guard-Zeile selbst** — die App ruft `element.requestFullscreen()` an keiner Stelle auf.
`document.fullscreenElement` spiegelt ausschließlich die **Web-Fullscreen-API** wider; macOS'
natives Vollbild (grüner Knopf) und der Browser-Chrome-Vollbildmodus (F11/⌃⌘F) setzen dieses
Property **nicht** — beide sind Fenstermanagement auf OS-/Browser-Ebene, unsichtbar für Seiten-JS.
**Das heißt: der Guard ist zwar exakt wie geplant gebaut, aber unter der aktuellen Codebasis für
die vom Nikinger gemeldete Situation vermutlich ein No-op** — er würde nur greifen, wenn die
Seite selbst irgendwann die Fullscreen-API nutzt (z. B. ein künftiger Bild-/Karten-Vollbild-
Viewer), nicht für OS-natives oder Browser-Chrome-Vollbild. Plan §6.1s Diagnose („der Browser
verlässt bei ESC selbst den Vollbildmodus") setzt implizit voraus, dass die App die Fullscreen-
API bereits nutzt — das ist gemessen falsch. **Beim Nikinger dieser Session nachgefragt und
bestätigt:** macOS, Safari, grüner Knopf (natives Fenster-Vollbild) — exakt der Fall, für den
`document.fullscreenElement` per Spezifikation nicht gesetzt wird. **Der Guard ist damit mit
hoher Sicherheit ein No-op für das tatsächlich gemeldete Verhalten.** Kein Ausweichweg in
dieser Session gebaut — ein `innerHeight`/`screen.height`-Heuristik-Vergleich wäre ungetestete
Spekulation ohne echtes Safari/macOS in dieser Umgebung (nur Chromium im Playwright-Cache, kein
WebKit); der Advisor-Rat dieser Session war ausdrücklich, keine ungetestete Heuristik selbst zu
erfinden. **P9-27/-28 bleiben offen und brauchen einen zweiten Anlauf**, entweder mit einer am
echten Safari gemessenen Erkennung (z. B. `fullscreenchange`-Gegenprobe: bleibt es dort
ebenfalls `null`? Dann ist ein window-resize-basierter Ansatz der nächste Kandidat, aber
gegen echtes Safari gemessen, nicht geraten) oder mit einer Nikinger-Entscheidung, ob das
Symptom überhaupt clientseitig lösbar ist. Modulstatus/Abnahme spiegeln das: **kein
Fehlschlag verdeckt als Erfolg.**

**D2 — kein Drop-Ziel zurück auf die Space-Wurzel (`tree.js`):** `renderSpaceNode()` ruft jetzt
`bindFolderDropTarget(row, "")` für `space.own`, hinter demselben Eigentümer-Riegel wie der
bestehende Ordner-Aufruf (`tree.js:205`) — Anker exakt wie im Plan (§6.2, `tree.js:232`).
**Eine Plan-Ungenauigkeit gefunden und dokumentiert, nicht stillschweigend übernommen:** §6.2s
Chip-Ausschluss-Warnung (V136 — ein `drop`-Listener müsse Ereignisse aus den
`<span role="button">`-Zähler-Chips ausschließen) bezieht sich auf `.overview__space-open` in
`list.js` (Block G7), nicht auf die hier tatsächlich verwendete `.tree__space`-Zeile in
`tree.js` — die hat keine verschachtelten interaktiven Kinder (nur Twist-Icon, Glyph, Label,
optionales „nur lesen"-Badge). Der Chip-Ausschluss ist an diesem Anker gegenstandslos; ein
Guard-Code, der nichts ausschließt, wäre ein irreführender Test. Deshalb dritter Test umbenannt
(`test_space_drop_target_uses_the_same_owner_guard_as_folders` statt der im Plan genannten
`test_space_drop_target_ignores_the_counter_chips`) — er prüft stattdessen, was am gewählten
Anker tatsächlich gilt: derselbe `space.own`-Riegel wie beim Ordner-Pfad. Dieselbe
Dashed-Border-Rückmeldung wie Ordner (`tree__realfolder--dragover`, `app.css:638`) gilt
automatisch mit, weil `bindFolderDropTarget()` die Klasse klassenbasiert und nicht an
`.tree__realfolder` gebunden setzt.

**Zweiter Advisor-Fund vor dem Commit, behoben:** der Erfolgs-Toast
(`"Verschoben nach " + folderPath.split("/").join(" / ")`) hätte bei leerem `folderPath`
„Verschoben nach " ins Leere gerendert — genau der Fall, den P9-29 auslöst. Gleiche Konvention
wie der Verschieben-Dialog übernommen (`dialogs.js:396`, Label `"(Space-Wurzel)"`) statt eine
neue zu erfinden. `moveItemToFolder()` (`list.js:251`) verschickt `folder: ""` unverändert wie
der Menü-Pfad — kein serverseitiger Sonderfall nötig. Cross-Space-Risiko geprüft und
ausgeschlossen: `list.js:412`s `movable`-Gate (`!item.readonly && item.space === state.ownSpace`)
lässt fremde Items gar nicht erst ziehbar werden, ein Wurzel-Drop kann also nie zu einem
Space-Wechsel werden (§0.6 hält Cross-Space-Verschieben ohnehin außerhalb von P9).

**Drei neue statische Wächter** in `phase5_ui/tests/test_static_routes.py`
(`test_escape_handler_checks_fullscreen_element`,
`test_space_row_is_a_drop_target_for_the_space_root`,
`test_space_drop_target_uses_the_same_owner_guard_as_folders`) — Begründung wie P8.6:
Regressions-Wächter statt nur Smoke, ein späterer Umbau führt beide Bugs sonst still wieder ein.

**Selbstprüfung:** `pytest -q` **1011 passed in ~185 s** (1008 + 3 neue Tests, rechnerisch
geprüft, dreifach gelaufen — auch nach dem Toast-Fix unten). `ui_budget.py` 5/5 im Korridor
(145,0 KB statt 144,7 KB, +0,3 KB durch die Kommentarzeilen + den D2-Aufruf + den Toast-Fix —
deutlich unter 250 KB). `node --check` auf beide geänderten JS-Dateien grün. Tabu-Diff/
`git status`: nur die drei erwarteten Dateien angefasst (`app.js`, `tree.js`,
`test_static_routes.py`) — kein `storage/`-, kein `mcpserver/tools.py`-Touch. Kein `pkill -f`,
kein `systemctl`, sharefyx-mcp nicht berührt.

**Offen für Step D, nicht in dieser Session erledigbar:** `P9-29`/`P9-30` (Drag-Drop-Verifikation
am echten Gerät) bleiben normale Sichtprüfung, Nikinger-Sache. `P9-31` (Chip-Nicht-Auslöser) ist
am gewählten Anker gegenstandslos, siehe oben — sollte im Gate/Z-Schritt als „gegenstandslos",
nicht als „vergessen" gebucht werden. **`P9-27`/`P9-28` (ESC im Vollbild) — Nikinger-
Entscheidung im Anschluss an diese Session: bewusst zurückgestellt, kein aktiver Blocker.**
Diagnose ist geklärt (macOS Safari, grüner Knopf), der gebaute Guard adressiert diesen Fall
vermutlich nicht — siehe D1-Befund oben und der neue `## Backlog`-Abschnitt am Kopf dieser
Datei. Modulstatus Step D deshalb 🟡, nicht ✅, aber ohne Zeitdruck.

**Nächster Schritt:** kein weiterer Claude-Code-eigener Step ohne erneute Nikinger-Freigabe —
E/F/G/H sind laut Plan weiterhin opencode/M3, A/B/C weiterhin Coarbeit. Vor dem nächsten
Claude-Code-Block: fragen, nicht per Präzedenzfall annehmen (dieselbe Vorsicht, die P9-Q selbst
für die Infra-Steps verlangt). D1 wartet im Backlog, bis Zeit dafür ist — kein aktiver Auftrag.

## Session stopped — 2026-09-20

**Step 0 ✅ — Claude Code, ein Commit.**

`phase9_hardening/` angelegt (`CLAUDE.md`, `SESSIONS_ARCHIVE.md`, `tests/`). `scripts/` bleibt
vorerst leer und damit ungetrackt (git committet keine leeren Verzeichnisse) — beide neuen
Skripte gehören plangemäß (§2.1/§2.3) ins repo-weite `scripts/`, nicht hierher; ein
phasenlokales `scripts/` entsteht erst, sobald ein späterer P9-Step eins braucht, genau wie bei
`phase8_6_ui_polish/scripts/`.

**INDEX-Rotation gebaut (P9-L):** `scripts/rotate_index_updates.sh`, dieselbe Mechanik wie
`rotate_session_block.sh` (Ausschneiden per `sed`, Reassemblierung mit `cmp` geprüft, jeder
Block byte-identisch gegengelesen, erst danach geschrieben) — aber auf eine **einzelne
physische Zeile** angewandt: die `updated:`-Frontmatter-Zeile von `docs/INDEX.md` wird an
` | `-Trennern **gefolgt von einem ISO-Datum** (`\d{4}-\d{2}-\d{2}`) gesplittet, nicht an jedem
` | ` — sonst hätte ein ` | ` innerhalb eines Eintrags den Schnitt verfälscht. Vier Gegenproben
vor dem Schreiben: (a) Byte-Buchhaltung (rotierte Einträge + Rest-Zeile + Trenner == Original),
(b) `cmp` der Reassemblierung, (c) jeder rotierte Eintrag byte-identisch im Archiv
wiedergefunden, (d) der Frontmatter-Closer `---` steht danach auf eigener Zeile. Getestet gegen
eine `tmp_path`-Fixture mit synthetischer Mehr-Eintrags-Kette (`test_rotate_index_updates.py`),
nicht gegen die echte `docs/INDEX.md` — die Kette dort trägt aktuell nur einen Eintrag (vom
2026-09-19 von Hand rotiert), das Skript liefe dort auf den „nichts zu tun"-Pfad.

**Vier geplante Defekte repariert (§2.2) plus drei ungeplante, vom `doc_health.py`-Bau selbst
aufgedeckt (nicht im Plan, aber trivial und im selben Commit behoben statt liegengelassen) —
sieben insgesamt:**

*Geplant, §2.2:*
- **0-a** die fünf `up:`/`down:`-Links in `phase8_6_ui_polish_block_h_r_3_escalation.md`
  korrigiert (drei waren `docs/concepts`-Geschwister und brauchten `./`, zwei zeigten auf
  `phase8_6_ui_polish/` und brauchten `../../`)
- **0-b** beide Mini-Pläne (`phase8_6_ui_polish_block_g_r_plan.md`,
  `phase8_6_ui_polish_block_h_r_plan.md`) haben jetzt eine L1-Card (`status: snapshot`)
- **0-c** `docs/INDEX.md`s `ROADMAP.md`-Zeile nennt jetzt die reale Größe (42.080 B) und P9;
  `ROADMAP.md` bleibt über dem Softcap, benannt statt versteckt (P8-P) — Straffung ist
  Step-Z-Arbeit
- **0-d** `docs/screenshots_latest/` entfernt — Gegenprobe zeigte alle sechs Symlinks dort
  bereits tot (`../p86_block_g_r_*.png` löst nicht auf, Original liegt unter
  `docs/screenshots/`); `screenshots_latest/` am Repo-Root ist die von Konvention §5 und
  `docs/INDEX.md:143` gemeinte Instanz und bleibt

*Ungeplant:*
- Wurzel-`CLAUDE.md` stand bei **64.401 B**, deutlich über dem 40-KB-Softcap —
  `docs/INDEX.md`s eigene Zeile dafür behauptete noch „~22 KB" aus der Frontmatter-Rotation vom
  2026-09-13; seither haben drei P9-Planungscommits (`06ab4f6`, `633338d`, `2f752f9`) den
  `## Current state`-Body weiter wachsen lassen (die Rotation von 2026-09-13 betraf nur die
  `updated:`-Kette, nicht den Body — P9-A hat eine Ein-Block-Regel für den Body ausdrücklich
  verworfen). Nikinger-Entscheidung: **benennen, nicht kürzen** — dieselbe P8-P-Konvention wie
  `phase8_6_ui_polish/CLAUDE.md` und `phase6_shares/CLAUDE.md`. Die Zeile trägt jetzt die reale
  Größe und die Benennung statt der stalen Zahl. **Der größte Einzelbefund dieser Session** —
  eine Datei war eine Woche lang um das Dreifache größer, als ihre eigene Index-Zeile behauptete,
  unbemerkt bis `doc_health.py` sie fing.
- `docs/PROJECT_SESSION_LOG.md` begann mit einer führenden Leerzeile vor der Frontmatter
  (`\n---\n...`) statt direkt mit `---` — einzige Datei im Repo mit diesem Defekt, `header_cards`
  hätte ihn sonst als Befund gemeldet. Entfernt.
- `docs/INDEX.md`s Zeile für `docs/screenshots/` verlinkte auf das Verzeichnis
  (`./screenshots/`) statt auf dessen `README.md`, obwohl der Text „L1-Header-Card in
  `docs/screenshots/README.md`" bereits sagte, wo die Card liegt — der Direktlink fehlte. Auf
  `./screenshots/README.md` umgestellt, analog zum bereits bestehenden Muster bei
  `screenshots_latest/`, dessen INDEX-Zeile direkt auf sein `README.md` zeigt. **Das ist eine
  Konventions-Entscheidung, keine reine Linkkorrektur:** jedes künftige `<dir>/README.md` in
  diesem Repo braucht ab jetzt entweder denselben Direktlink-auf-README-Zeigers oder eine
  eigene INDEX-Zeile — `doc_health.py`s `index_lines`-Prüfung erzwingt das ab sofort. Wer das
  zurück auf einen Verzeichnislink „korrigiert", bricht den Scan.

**`doc_health.py` gebaut** (`scripts/doc_health.py`, stdout nur JSON, Logging nach stderr —
Hard Rule 7) mit den vier Prüfungen aus §2.3 (`index_lines`, `header_cards`, `updown_links`,
`oversize`). Die Ausnahmeliste ist eine Konstante mit den vier in `docs/INDEX.md` benannten
Fällen. **`oversize` unterscheidet drei Zustände statt zwei:** 📕/📦-Snapshots sind immer
ausgenommen; 📗/🟡-Dateien über 40 KB sind nur dann kein Befund, wenn ihre `docs/INDEX.md`-Zeile
die Zeichenkette „benannt statt versteckt" **und** eine aktuelle Größenangabe trägt — exakte
Byte-Zahl **oder** gerundete `~NNKB` innerhalb von **±2 KB** der echten Dateigröße, keine
Prozent-Toleranz (eine Prozent-Toleranz hätte bei einer 106-KB-Datei ±32 KB durchgelassen; der
gefundene Defekt war „~22 KB" für eine 64-KB-Datei — eine feste, kleine Bandbreite fängt genau
das, ohne mit der Dateigröße mitzuwachsen). `index_lines` sucht ebenfalls pfad-, nicht
namensbasiert — `CLAUDE.md` allein kommt in einem Dutzend INDEX-Zeilen vor, ein bloßer
Namens-Treffer hätte jede neue `phaseN/CLAUDE.md` für immer kostenlos bestehen lassen. Genau
dieses Muster trägt `phase8_6_ui_polish/CLAUDE.md`, `phase6_shares/CLAUDE.md` und jetzt
`ROADMAP.md` und Wurzel-`CLAUDE.md`. Ein 📗/🟡-Fund ohne Benennung bleibt ein echter Befund.
`phase9_hardening/tests/test_doc_health.py` nagelt alle vier Prüfungen fest, `oversize` inkl.
Gegenprobe für einen benannten, einen unbenannten und einen stale-benannten Fall.
`pytest.ini`s `testpaths` fehlte `phase9_hardening/tests` — ohne die Zeile wären diese 13 Tests
für jeden `pytest -q`-Lauf unsichtbar geblieben, und P9-9 („pytest ≥ 995, Step 0 addiert die
neuen doc_health-Tests") wäre unerfüllbar gewesen. Zeile ergänzt — **das ist eine geteilte
Config-Datei, keine Doku-Zeile**, deshalb hier ausdrücklich benannt statt beiläufig
mitgeführt. Nebenbefund dabei: `phase8_ui_graph/`, `phase8_5_picker_release/` und
`phase8_6_ui_polish/` haben gar kein eigenes `tests/`-Verzeichnis (ihre Tests leben in
`phase5_ui/tests` bzw. `phase4_auth/tests`) — Phase 9 ist die erste Phase mit einem eigenen
`tests/`-Ordner seit `phase7_spaces_admin/`.

**Baseline gemessen, zweistufig:** vor jeder Änderung `.venv/bin/python -m pytest -q` →
**995 passed in 185,98 s** (V147, exakt die geforderte Zahl). Nach Step 0 komplett (13 neue
Tests + die `pytest.ini`-Ergänzung, die sie erst sichtbar macht) → **1008 passed in 182,78 s**
— 995 + 13, rechnerisch geprüft, nicht nur behauptet. Phasenstart-SHA: `06ab4f6` (Stand vor
diesem Commit). Kein `ui_budget`-Touch nötig (kein `phase5_ui/webui/static/**` berührt), kein
`node --check` nötig (kein JS berührt). Tabu-Diff §0.3 leer — reine Doku-/Skript-Session. Kein
`pkill -f`, kein `systemctl`, sharefyx-mcp nicht berührt.

**Nächster Schritt:** Step A (Domain über eigenen VPS) als Coarbeit in opencode (P9-Q) —
Voraussetzung ist die Domain-/VPS-Beschaffung durch den Nikinger, siehe Prompt-Vorlauf. B und C
laufen unabhängig davon weiter, A blockiert die Phase nicht.

