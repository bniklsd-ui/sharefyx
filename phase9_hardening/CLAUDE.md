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
updated: 2026-09-26 (Step C abgeschlossen: C8 `sudo systemctl disable --now ollama` Nikinger-Cobefehl, sharefyx-VM `inactive`/`disabled`, `curl 127.0.0.1:11434` → HTTP 000 exit 7 `Connection refused` (bestätigt aus dieser Shell als zweite Sichtprobe), binary + Modell bleiben als kalter Fallback bis Step Z; Host-Aufräumen pve: `/root/111.conf.new` (633 B, 2026-09-25 22:41) und `/root/111.conf.bak-p9c` (842 B, 2026-09-25 22:41) per `rm -f` entfernt, `/tmp/nv580173` und alter `NVIDIA-Linux-x86_64-580.126.09.run` waren bereits weg — PVE-9-tmpfs bzw. im Vorrundezweig schon entfernt; P9-22 deferred — kein externer Test möglich, architektonischer Beweis captured: 192.168.68.140 ist RFC1918, sharefyx-VM hat keine öffentliche IP (CGNAT via RUT X50, default route via 192.168.68.1), Tailscale-Funnel mappt nur `127.0.0.1:8765` (kein `*:11434` auf sharefyx-VM), kein Port-Forward auf RUT X50, der einzige 11434-Listener ist innerhalb CT 111; Step C 🟡→✅, Modulstatus nachgezogen, Session-Block 2026-09-26 angehängt) | 2026-09-25 (C4 ✅ DHCP-Reservierung im RUT X50, per `local_vision`-MCP-Aufruf gegen die GPU ausgelesen — erster echter Einsatz über den opencode-Pfad) | 2026-09-25 (zweite Reboot-Probe grün: CT-Knoten 20:54 > 20:42, Major 235 = `/proc/devices`, `cuInit = 0`, `size_vram` = `size` — Boot-Persistenz ✅) | 2026-09-25 (Reboot-Probe: uvm-Major 511→235, `cuInit = 999`; Fix per `devN`-Passthrough, per CT-Neustart bewiesen `cuInit = 0`, zweite Reboot-Probe offen, `size_vram` = `size`; C5 gesetzt; V166 beantwortet) | 2026-09-25 (Boot-Persistenz eingerichtet, CT 111 `onboot: 0` gefunden, Reboot-Probe offen) | 2026-09-25 (GPU-Inferenz läuft: CT 111 auf 580.173.02, `size_vram` = `size`, 63 tok/s, P9-21/-23/-26 ✅; Boot-Persistenz offen) | 2026-09-25 (Host-Treiber 580.173.02 mit `nvidia-uvm` installiert und geladen, kein Reboot) | 2026-09-25 (V165 beantwortet: 580.173.02 kennt die neue `zone_device_page_init`-Signatur) | 2026-09-25 (Step C Diagnose bestätigt: kein `/dev/nvidia-uvm`, `cuInit = 999`) | 2026-09-25 (Step C Diagnose, Claude Code: CUDA fehlt, weil `nvidia-uvm` fehlt — C2-Trade-off-Satz datiert korrigiert, Modulstatus C nachgezogen, Nikinger-Entscheidung zum Host-Fix offen) | 2026-09-25 (Backlog aufgeräumt: „opencode via Tailscale" für sharefyx-VM per Nikinger-Update mittlerweile passiert, Eintrag aus der Backlog-Sektion entfernt; nur noch D1 zurückgestellt) | 2026-09-25 (Step C Teil 2 / C6 — `mcp_local_vision_server.py` Skript-Fixes aus Plan §5.3: `serve()` loggt aufgelösten Endpoint, `--endpoint` wirkt jetzt auch ohne `--check`; neue zentrale `resolve_endpoint(args)` mit Präzedenz `--endpoint` > `$LOCAL_VISION_ENDPOINT` > `DEFAULT_ENDPOINT`; `_CURRENT_ENDPOINT` als Modul-Globals wird in `serve()` einmal gesetzt und von `handle_tools_call` gelesen statt erneut die Umgebungsvariable; 9 neue Tests + Counter-Probe ohne den Fix 7/9 rot — exakt die zwei gemeldeten Bugs; LXC + Ollama + C5/C7/C8 stehen aus) | 2026-09-24 (Step C Teil 1 — NVIDIA-Host-Treiber 580.126.09 installiert mit `--no-unified-memory`; pve-no-subscription-Repo ergänzt; drei dokumentierte Fehlbarkeiten auf dem Weg (Header-Paket fehlte, Backports führten denselben Upstream, Nouveau-Konflikt, uvm_hmm.c gegen 7.0.2-6-pve-Mai-Patch); eigener autoremove-Vorfall mit sudo/dkms-Verlust am 2026-09-24 wieder behoben; LXC + Ollama stehen aus) | 2026-09-24 (Backlog: ~19-min mcp-proxy.anthropic.com-Ausfall dokumentiert und geschlossen — gemessen nicht CGNAT/sharefyx-VM-seitig, Nikinger-Anordnung) | 2026-09-24 (Backlog: "opencode via Tailscale"-Behandlung für sharefyx-/Trading-Bot-VM nachgetragen, Nikinger-Feedback aus Netzwerk-Diagnosesession, kein Produktcode-Touch) | 2026-09-23 (D1/ESC-Bug auf Nikinger-Anordnung zurückgestellt, `## Backlog` neu) | 2026-09-23 (Step D code-complete — Drop-Ziel Space-Wurzel, ESC/Vollbild-Guard gebaut, gebaut in Claude Code statt opencode/M3, benannte Abweichung von P9-Q) | 2026-09-20 (Step 0 abgeschlossen — Phasenverzeichnis, INDEX-Rotationsskript, vier geplante plus drei ungeplante Doku-Defekte repariert, `doc_health.py` als Test festgenagelt, Baseline gemessen)
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
| C | Vision-Dienst auf der RTX 3060 | ✅ **Step C abgeschlossen** (Session-Block 2026-09-26): GPU-Inferenz reboot-fest (Host + CT 111 auf 580.173.02 inkl. `nvidia-uvm`, uvm per `devN`-Passthrough, zweite Reboot-Probe grün) + C8 (`ollama` auf sharefyx-VM `inactive`/`disabled`, `curl 127.0.0.1:11434` → `Connection refused`, binary + Modell bleiben als kalter Fallback bis Step Z) + Host-Aufräumen pve (zwei `/root/111.conf.{new,bak-p9c}` per `rm -f` weg; `/tmp/nv580173` und alter `NVIDIA-Linux-x86_64-580.126.09.run` bereits weg — PVE-9-tmpfs bzw. im Vorrundezweig entfernt) · P9-21 ✅ · P9-23 ✅ · P9-26 ✅ · C4 ✅ · C5 ✅ · C6 ✅ · **P9-22 deferred** (Nikinger-Entscheidung 2026-09-26, kein externer Test möglich) — architektonischer Beweis statt externem Test: 192.168.68.140 ist RFC1918, sharefyx-VM hat keine öffentliche IP (CGNAT via RUT X50), Tailscale-Funnel mappt nur `127.0.0.1:8765` (kein `*:11434` auf sharefyx-VM), kein Port-Forward auf RUT X50, einziger 11434-Listener sitzt innerhalb CT 111; Revisit-Step **Step Z oder P10-Backlog** |
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

## Session stopped — 2026-09-26

**Step C abgeschlossen ✅ — C8 + Host-Aufräumen pve + P9-22 deferred.** Coarbeit Claude Code
↔ Nikinger (P9-Q-Muster): drei Host-/Service-Schritte liefen auf Nikingers Seite (sharefyx-VM
`sudo` braucht Password, pve ist von sharefyx-VM aus nicht erreichbar, kein Test-Setup von
außerhalb des LAN verfügbar), jede Ausgabe zurückgespielt. Mein Anteil: Verifikation der
Verbindungs-Verweigerung, architektonischer Beweis für P9-22, Modulstatus + Session-Block +
Rotation. Kein Repo-Code-Touch, kein `pytest`, kein `ui_budget`, kein `systemctl` von meiner
Seite, sharefyx-mcp **unangetastet**.

### C8 — `ollama` CPU-Backend stilllegen (Nikinger, sharefyx-VM)

Verbatim-Ausgabe der Nikinger-Sequenz (Sharefyx-VM):

```
$ sudo systemctl disable --now ollama
[sudo] password for savefyx:
Removed "/etc/systemd/system/default.target.wants/ollama.service".

$ curl -sS --max-time 3 -o /dev/null -w "HTTP %{http_code} | exit=%{exitcode} | err=%{errormsg}\n" http://127.0.0.1:11434/
curl: (7) Failed to connect to 127.0.0.1 port 11434 after 0 ms: Couldn't connect to server
HTTP 000 | exit=7 | err=Failed to connect to 127.0.0.1 port 11434 after 0 ms: Couldn't connect to server
$ systemctl is-active ollama; systemctl is-enabled ollama
inactive
disabled
```

Mein zweiter Sichtproben-Lauf von dieser Shell (Claude Code, sharefyx-VM):

```
$ curl -sS --max-time 3 -o /dev/null -w "HTTP %{http_code} | exit=%{exitcode} | err=%{errormsg}\n" http://127.0.0.1:11434/
curl: (7) Failed to connect to 127.0.0.1 port 11434 after 0 ms: Couldn't connect to server
HTTP 000 | exit=7 | err=Failed to connect to 127.0.0.1 port 11434 after 0 ms: Couldn't connect to server
$ systemctl is-active ollama; systemctl is-enabled ollama
inactive
disabled
```

Unit noch auf Platte (`/etc/systemd/system/ollama.service`, 423 B, 2026-09-10), Binary auch
(`/usr/local/bin/ollama`, 40.014.640 B, 2026-09-10), Modell auch
(`/usr/share/ollama/.ollama/models/manifests/registry.ollama.ai/library/qwen3-vl`) — alles
bewusst stehen gelassen als **kalter Fallback bis Step Z**, dort `ollama rm qwen3-vl:8b` +
Deinstallation (Plan §5.4 Ende).

### Host-Aufräumen pve (Nikinger, Proxmox-Host)

Verbatim-Ausgabe der Nikinger-Sequenz (root@pve):

```
root@pve:~# ls -la /tmp/nv580173/ 2>&1
ls: cannot access '/tmp/nv580173/': No such file or directory
root@pve:~# ls -d /tmp/nv* 2>&1
ls: cannot access '/tmp/nv*': No such file or directory
root@pve:~# ls -la /root/111.conf.new /root/111.conf.bak-p9c 2>&1
-rw-r--r-- 1 root root 633 Sep 25 22:41 /root/111.conf.new
-rw-r----- 1 root root 842 Sep 25 22:41 /root/111.conf.bak-p9c
root@pve:~# ls -la /root/NVIDIA-Linux-x86_64-580.126.09.run /tmp/NVIDIA-Linux-x86_64-580.126.09.run 2>&1
ls: cannot access '/root/NVIDIA-Linux-x86_64-580.126.09.run': No such file or directory
ls: cannot access '/tmp/NVIDIA-Linux-x86_64-580.126.09.run': No such file or directory
root@pve:~# rm -rf /tmp/nv580173
root@pve:~# rm -f  /root/NVIDIA-Linux-x86_64-580.126.09.run /tmp/NVIDIA-Linux-x86_64-580.126.09.run
root@pve:~# rm -f  /root/111.conf.new /root/111.conf.bak-p9c
root@pve:~# ls /tmp/nv580173 /root/111.conf.new /root/111.conf.bak-p9c 2>&1
ls: cannot access '/tmp/nv580173': No such file or directory
ls: cannot access '/root/111.conf.new': No such file or directory
ls: cannot access '/root/111.conf.bak-p9c': No such file or directory
root@pve:~# ls /root/NVIDIA-Linux-x86_64-580.126.09.run /tmp/NVIDIA-Linux-x86_64-580.126.09.run 2>&1
ls: cannot access '/root/NVIDIA-Linux-x86_64-580.126.09.run': No such file or directory
ls: cannot access '/tmp/NVIDIA-Linux-x86_64-580.126.09.run': No such file or directory
```

Drei Befunde aus der Nikinger-Sequenz, die in den Plan-Doku-Stand zurückfließen:

1. **`/tmp/nv580173` und `/tmp/nv*` waren bereits weg** — bestätigt die im Session-Block 2026-09-25
   (3) offen gehaltene Vermerkung „PVE 9 hat evtl. tmpfs-`/tmp`" als Tatsache: das Verzeichnis
   wurde vermutlich beim letzten Host-Boot (oder durch das tmpfs-Verhalten selbst) abgeräumt. Die
   `rm -rf /tmp/nv580173` lief ins Leere und ist im Audit-Output trotzdem enthalten — nil-volens
   ist hier Beleg, nicht Schlamperei.
2. **`/root/111.conf.new` (633 B) und `/root/111.conf.bak-p9c` (842 B)** waren noch da, beide
   datiert 2026-09-25 22:41 (= Block (3) Runde 4a „Backup `/root/111.conf.bak-p9c`,
   `grep -v` nach Zeileninhalt → `/root/111.conf.new`"). Jetzt weg — der `devN`-Fix ist
   reboot-bewährt (zweite Reboot-Probe 2026-09-25 20:54 grün), das Rollback-Material wird nicht
   mehr gebraucht.
3. **Alter `NVIDIA-Linux-x86_64-580.126.09.run`-Installer war weder in `/root/` noch in `/tmp/`.**
   Wahrscheinlich beim Vorrundezweig-Umbau auf 580.173.02 (Session-Block 2026-09-25 (3) Runde 17)
   schon entfernt; nicht mehr nachvollziehbar, wann genau — der Plan hat ihn nicht eigens
   dokumentiert, also auch keinen Konflikt.

### P9-22 — deferred, architektonischer Beweis

**Nikinger-Entscheidung 2026-09-26:** kein externer Test möglich (kein Mobilfunk-Test-Setup zur
Hand, sharefyx-VM hat keinen LAN-Externen Pfad), P9-22 wird **deferred** statt offen gelassen.
Begründung: der architektonische Beweis deckt denselben Sachverhalt — dass
`192.168.68.140:11434` von außerhalb des Heim-LAN nicht erreichbar ist — aus fünf
voneinander unabhängigen Indikatoren ab:

| # | Indikator | Beleg |
|---|---|---|
| 1 | `192.168.68.0/24` ist RFC1918 — auf dem öffentlichen Internet nicht routbar | Definition, kein Messbedarf |
| 2 | sharefyx-VM hat **keine** öffentliche IP | `ip -4 addr` zeigt nur `192.168.68.175/24` (ens18, DHCP) + `100.93.43.122/32` (tailscale0); `ip route` default via `192.168.68.1` (RUT X50) |
| 3 | RUT X50 hat **kein** Port-Forwarding auf 11434 | Hard Rule 6 (Egress-only-Tunnel, CGNAT-Setup, niemals ein offener Port am Router) — etablierte Invariante, kein Befund dieser Session |
| 4 | sharefyx-VM-Tailscale-Funnel mappt **nicht** auf 11434 | `tailscale funnel status` zeigt genau eine Map: `https://savefyx-vmware-virtual-platform.tail4a8b49.ts.net → http://127.0.0.1:8765` (sharefyx-mcp). `:11434` kommt nicht vor |
| 5 | sharefyx-VM hat **keinen** `*:11434`-Listener und keine iptables/nft-Regel, die ihn weiterleiten würde | `ss -tlnp` zeigt kein 0.0.0.0:11434 und kein 100.93.43.122:11434 (rootless-Check für ufw/nft/iptables gescheitert mit „Permission denied", aber irrelevant: kein Listener = keine Regel kann ihn weiterleiten, weil nichts da ist, das ankommt) |

Was ein echter externer Test zusätzlich bewiesen hätte: eine konkrete Log-Zeile wie
„`Connection timed out` from `100.x.y.z (T-Mobile)`". Diese Probe-Lücke wird in **Step Z**
(oder im P10-Backlog) adressiert — nicht hier, weil das Hard-Rule-6-Fundament schon steht
und der Test ohne Mobilfunk-Setup technisch nicht ausführbar ist.

### Stand Step C für einen kalten Leser

Alle 7 P9-Abnahmezeilen von Step C (`docs/concepts/phase9_hardening_plan.md` §5.6) sind erledigt
oder mit architektonischem Ersatz belegt:

- **P9-21** ✅ Dienst antwortet von sharefyx-VM aus auf der internen Adresse — gemessen
  (Block (3) Runde 4b).
- **P9-22** ⚠️ **deferred** (s. o., Revisit Step Z oder P10-Backlog).
- **P9-23** ✅ Cold-Start gemessen und gegen 46–180 s gestellt (Block (3) Runde 4b: 19,9 s,
  Block (3) Runde 5: 19,7 s).
- **P9-24** ✅ Beide Skript-Fixes aus §5.3 im Code, Startzeile zeigt den echten Endpoint
  (Session-Block 2026-09-25 (2)).
- **P9-25** ✅ V154 und V156 beantwortet (im selben Block).
- **P9-26** ✅ Echter Sichtprüfungslauf gegen `c4_p8519_01_radiogruppe_im_dialog.png` liefert
  dieselbe Aussage wie der CPU-Lauf vom 2026-09-10 (Block (3) Runde 4b + Runde 5).

Modulstatus Step C: 🟡 → **✅** (in dieser Session nachgezogen).

### Rotation + Doku-Hygiene

`scripts/rotate_session_block.sh phase9_hardening` läuft im selben Commit: Session-Block
**2026-09-25 (3)** wandert verbatim nach `SESSIONS_ARCHIVE.md` (newest-first, oben an), Head
trägt danach exakt einen Session-Block (den heutigen). `SESSIONS_ARCHIVE.md`-Frontmatter
`updated:` wird per Hand nachgezogen (Skript-Logik-Zeile 163). `docs/INDEX.md`-Phase-9-Zeile
steht auf `Step 0 ✅ · **Step C ✅** · Step D 🟡 · A/B/E/F/G/H ⬜ · Gate/Z ⬜` mit aktualisierten
Größenangaben für Head und Archiv. INDEX-Größe selbst weiter über dem 38-KB-Softcap (V145
bleibt offen, keine Verschlechterung in dieser Session — der Modulstatus-Eintrag wurde nur
länger, weil die P9-22-Begründung jetzt mitläuft).

Kein Touch auf `phase5_ui/`, `phase1_storage/`, `tests/`, `webui/`, `docs/concepts/`,
`scripts/doc_health.py` — keine Test-Änderung, keine UI-Änderung, kein Frontend-Touch
(`mcp_local_vision_server.py` und `vision_ollama.py` sind seit C6 unverändert).

### Backlog

Unverändert seit Block 2026-09-25 (3): nur noch **D1 — ESC im Vollbild schließt zusätzlich das
Item** (Nikinger-Entscheidung 2026-09-23, zurückgestellt, kein aktiver Blocker). Der separate
„Anthropic-MCP-Proxy-502-Vorfall vom Vormittag 2026-09-24" ist weiterhin als „unbekannter,
vorübergehender Ausfall bei Anthropic, nicht auf CGNAT/Mobilfunk-Setup oder sharefyx-VM
zurückzuführen" abgelegt — kein neuer Vorfall in dieser Session.

### Nächster Schritt

**Step D — die zwei gemeldeten Bugs** ist weiterhin 🟡 (D2 fertig, D1 zurückgestellt) — keine
Veränderung. Der nächste **offene** Step nach C ist **A (echte Domain über eigenen VPS)** oder
**B (`tailscaled-watchdog.service`)**; das Handover §4.2 hatte die Domain als „einer der
ersten P9-Schritte" markiert, was begründet ist (Adressänderung zieht den Claude-Connector in
beiden Konten nach sich, wer sie ans Ende legt, macht den Schnitt zweimal). Wahl liegt beim
Nikinger — diese Session hat darauf keinen Zugriff genommen.
