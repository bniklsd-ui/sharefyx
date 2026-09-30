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
updated: 2026-09-30 (**Step F gebaut — neunte und bis jetzt letzte P1-Contract-Öffnung, code-complete, nicht live-bewiesen**: `doing` wird ein Statuswert (nur bei `task`, `note` bleibt `{active, archived}`), `assignee` ein erstklassiges Feld mit Index-Spalte, `INDEX_SCHEMA_VERSION` 3 → 4, **keine Migration** (Hard Rule 2). **V160 vom Nikinger beantwortet: Space-Name, ohne Validierung** — eine Prüfung gegen die Space-Liste wäre eine zweite, nicht angekündigte Öffnung. **Plan §8.2 auf den Diff korrigiert: neun Stellen sind gemessen achtzehn Hunks** (F9 sind drei Statement-Teile plus ein Row-Dict, nicht eine Stelle), dazu drei vom Plan nicht genannte Pflichtstellen (`_summary()` F10, `update()` F11, `_coerce_assignee()`). Enge Probe §8.7 erfüllt: **genau drei Dateien**, die sechs Hartpfade leer; Gegenprobe mit vier eingebauten Verstößen → 10 Tests rot. `pytest` 1039 → **1062** (23 neu), `ui_budget` 5/5, `doc_health` 0, `node --check` grün. **Ein Befund bewusst NICHT behoben:** `_BUCKETS` kennt `doing` nicht — beide Fix-Kandidaten sind Darstellungsentscheidungen und P10-Arbeit (P9-P), der Befund steht im Code und ein Wächter pinnt ihn. **V161 mit synthetischem Vorabwert** (2,5–4,0 ms/Item; 153 reale Items ⇒ 0,4–0,6 s einmalig), P9-43 bleibt Nikinger-Schritt am echten DATA_ROOT. **V159 gemessen statt geglaubt:** richtig für den Editor-Dropdown, gegenstandslos für den Anlegen-Dialog (der hat keinen Status-Knopf)) | 2026-09-30 (Step A halb ausgeführt — **A1/A2/A3/A0b/A6 erledigt**: Domain bestellt, VPS `217.160.128.146` (Ubuntu 24.04.5), Policy + Beitritt mit `tag:sharefyx-edge` (von der Gegenseite belegt: Tags gesetzt, User=None), socat-Relay laufend mit identischer Härtung, Firewall `22` nur auf `tailscale0` mit Gegenprobe. **Kette blockiert an der Domain-Registrierung** — A4 braucht eine auflösende Domain fürs Zertifikat. Der Session-Fund: **mein eigenes A6 hätte den Betrieb gekappt** (`ufw default deny incoming` gilt auch auf `tailscale0`, SSH-Regel fehlte). Vier eigene Fehler dokumentiert, darunter ein erfundener Drift, der zurückgenommen wurde. V162/V163 neu offen, V151 Vorabwert 28–37 ms über DERP. 7 Tests + Gegenprobe 4/4) | 2026-09-29 (Step A: M3-Anteil gebaut, Ausführung liegt beim Nikinger — **Plan-A4 nachweislich unbaubar** (auf der Tailnet-IP lauscht nichts: `SPACE_HOST=127.0.0.1`, `ss -ltnp` belegt; `SPACE_HOST=0.0.0.0` wäre P3-B gebrochen) → **socat-Relay-Unit** `phase3_edge/systemd/sharefyx-tail-proxy.service` ohne `__REPO_ROOT__` im `ExecStart` (die Release-Pfad-Kopplung aus dem Step-B-Befund ist damit konstruktiv ausgeschlossen); Caddy-Vorlage + ACL-Fragment + `phase9_hardening/step_a/RUNBOOK_STEP_A.md` (A1–A9, ein Schritt pro Runde) + 7 Wächter, Gegenprobe 4/4; **V149 beantwortet** (alle Metadatenfelder abgeleitet, keines fest, kein `iss`-Check beim Einlösen), Befund 2 (`/health` statt `/healthz`) und Befund 3 (`ALLOWED_HOSTS` fehlt in Plan-A7) als Plan-Korrekturen, **Befund 5** = der Funnel bleibt nach A7 lesbar, aber nicht beschreibbar (CSRF-Origin exakt, `security.py:84`); **V162 neu offen** = ACL-Durchsetzung von `tailscale serve --tcp`, der Grund für die socat-Wahl; Step A ⬜→🟡) | 2026-09-28 (**Nachtrag**: §Vormerkung Vision-Modell — Messbefund aus Step E dokumentiert, Recherche in `docs/concepts/sichtpruefung_automation_tooling.md`, Schluss: ein Modellwechsel ist nicht der Hebel, die Zuständigkeitsgrenze ist es; kein P9-Block) | 2026-09-28 (Step E abgeschlossen ✅ — Reload-Overload der Karte: (a) kein zweiter `/graph`-Abruf ohne Datenänderung, Signatur aus dem `/overview`-Payload statt aus dem Graph-Payload (Plan-Korrektur: der Graph-Knoten hat kein `updated`, `api.py:698-708`), Erzeugung in `list.js :: loadOverview()` (deckt jeden Schreibpfad mit), Format in `state.js :: overviewToken()` (Blatt-Modul statt Zyklus), `force` nur am expliziten Refresh-Knopf; (b) bekannte Knoten behalten x/y über den Refetch. Sieben Tests (Node-Harness `graph_reload_probe.mjs` + statisch) und eine Browser-Probe (`p9e_reload_probe.py`, Wegwerf-Instanz Port 18768), beide mit Gegenprobe gegen HEAD: dort 1 statt 0 Abrufe und 10 statt 1 verschiedene Bilder in 1,5 s, im Node-Harness 467,6 px Positionssprung statt 0. V118 beantwortet (zwei Linien, eine gestrichelt) — Design-Frage eine-oder-zwei beim Nikinger. `pytest` 1031 passed + 1 failed (der Fehlschlag ist der Vortrag: `docs/INDEX.md` über der doc_health-Schwelle, auf HEAD genauso rot, gehört nach Step Z), `ui_budget` 5/5 (149,0 KB), Tabu-Bereichs-Diff leer, Wegwerf-Instanz über die PID-Datei gestoppt. Drei eigene Fehler dokumentiert (falsche erste Verdrahtung, Messgerät zählte sich selbst, Test scheiterte an eigenem Kommentar) | 2026-09-26 (Step B code-complete, install ausstehend: vier neue Dateien — `phase3_edge/scripts/tailscaled_watchdog.sh` + `phase3_edge/systemd/tailscaled-watchdog.{service,timer}` + `phase9_hardening/tests/test_tailscaled_watchdog.py` (5/5 grün); V152 beantwortet (kein Tailscale-eigenes Feature ohne kommerzielles Add-on), V153 als Empfehlung dokumentiert (Polkit `.rules`-Datei `/etc/polkit-1/rules.d/99-tailscaled-watchdog-restart.rules`, Sudoers-Fallback `/etc/sudoers.d/tailscaled-watchdog-restart`); Modulstatus Step B ⬜→🟡, Phase-9-###-Sub-Sektion ergänzt; Phase-9-Zeile in `docs/INDEX.md` nachgezogen; kein Touch an bestehendem Code, Hard Rule 8 (Doc-Update im selben Commit) und Hard Rule 9 (kein `systemctl` durch M3) eingehalten) | 2026-09-26 (Step C abgeschlossen: C8 `sudo systemctl disable --now ollama` Nikinger-Cobefehl, sharefyx-VM `inactive`/`disabled`, `curl 127.0.0.1:11434` → HTTP 000 exit 7 `Connection refused` (bestätigt aus dieser Shell als zweite Sichtprobe), binary + Modell bleiben als kalter Fallback bis Step Z; Host-Aufräumen pve: `/root/111.conf.new` (633 B, 2026-09-25 22:41) und `/root/111.conf.bak-p9c` (842 B, 2026-09-25 22:41) per `rm -f` entfernt, `/tmp/nv580173` und alter `NVIDIA-Linux-x86_64-580.126.09.run` waren bereits weg — PVE-9-tmpfs bzw. im Vorrundezweig schon entfernt; P9-22 deferred — kein externer Test möglich, architektonischer Beweis captured: 192.168.68.140 ist RFC1918, sharefyx-VM hat keine öffentliche IP (CGNAT via RUT X50, default route via 192.168.68.1), Tailscale-Funnel mappt nur `127.0.0.1:8765` (kein `*:11434` auf sharefyx-VM), kein Port-Forward auf RUT X50, der einzige 11434-Listener ist innerhalb CT 111; Step C 🟡→✅, Modulstatus nachgezogen, Session-Block 2026-09-26 angehängt) | 2026-09-25 (C4 ✅ DHCP-Reservierung im RUT X50, per `local_vision`-MCP-Aufruf gegen die GPU ausgelesen — erster echter Einsatz über den opencode-Pfad) | 2026-09-25 (zweite Reboot-Probe grün: CT-Knoten 20:54 > 20:42, Major 235 = `/proc/devices`, `cuInit = 0`, `size_vram` = `size` — Boot-Persistenz ✅) | 2026-09-25 (Reboot-Probe: uvm-Major 511→235, `cuInit = 999`; Fix per `devN`-Passthrough, per CT-Neustart bewiesen `cuInit = 0`, zweite Reboot-Probe offen, `size_vram` = `size`; C5 gesetzt; V166 beantwortet) | 2026-09-25 (Boot-Persistenz eingerichtet, CT 111 `onboot: 0` gefunden, Reboot-Probe offen) | 2026-09-25 (GPU-Inferenz läuft: CT 111 auf 580.173.02, `size_vram` = `size`, 63 tok/s, P9-21/-23/-26 ✅; Boot-Persistenz offen) | 2026-09-25 (Host-Treiber 580.173.02 mit `nvidia-uvm` installiert und geladen, kein Reboot) | 2026-09-25 (V165 beantwortet: 580.173.02 kennt die neue `zone_device_page_init`-Signatur) | 2026-09-25 (Step C Diagnose bestätigt: kein `/dev/nvidia-uvm`, `cuInit = 999`) | 2026-09-25 (Step C Diagnose, Claude Code: CUDA fehlt, weil `nvidia-uvm` fehlt — C2-Trade-off-Satz datiert korrigiert, Modulstatus C nachgezogen, Nikinger-Entscheidung zum Host-Fix offen) | 2026-09-25 (Backlog aufgeräumt: „opencode via Tailscale" für sharefyx-VM per Nikinger-Update mittlerweile passiert, Eintrag aus der Backlog-Sektion entfernt; nur noch D1 zurückgestellt) | 2026-09-25 (Step C Teil 2 / C6 — `mcp_local_vision_server.py` Skript-Fixes aus Plan §5.3: `serve()` loggt aufgelösten Endpoint, `--endpoint` wirkt jetzt auch ohne `--check`; neue zentrale `resolve_endpoint(args)` mit Präzedenz `--endpoint` > `$LOCAL_VISION_ENDPOINT` > `DEFAULT_ENDPOINT`; `_CURRENT_ENDPOINT` als Modul-Globals wird in `serve()` einmal gesetzt und von `handle_tools_call` gelesen statt erneut die Umgebungsvariable; 9 neue Tests + Counter-Probe ohne den Fix 7/9 rot — exakt die zwei gemeldeten Bugs; LXC + Ollama + C5/C7/C8 stehen aus) | 2026-09-24 (Step C Teil 1 — NVIDIA-Host-Treiber 580.126.09 installiert mit `--no-unified-memory`; pve-no-subscription-Repo ergänzt; drei dokumentierte Fehlbarkeiten auf dem Weg (Header-Paket fehlte, Backports führten denselben Upstream, Nouveau-Konflikt, uvm_hmm.c gegen 7.0.2-6-pve-Mai-Patch); eigener autoremove-Vorfall mit sudo/dkms-Verlust am 2026-09-24 wieder behoben; LXC + Ollama stehen aus) | 2026-09-24 (Backlog: ~19-min mcp-proxy.anthropic.com-Ausfall dokumentiert und geschlossen — gemessen nicht CGNAT/sharefyx-VM-seitig, Nikinger-Anordnung) | 2026-09-24 (Backlog: "opencode via Tailscale"-Behandlung für sharefyx-/Trading-Bot-VM nachgetragen, Nikinger-Feedback aus Netzwerk-Diagnosesession, kein Produktcode-Touch) | 2026-09-23 (D1/ESC-Bug auf Nikinger-Anordnung zurückgestellt, `## Backlog` neu) | 2026-09-23 (Step D code-complete — Drop-Ziel Space-Wurzel, ESC/Vollbild-Guard gebaut, gebaut in Claude Code statt opencode/M3, benannte Abweichung von P9-Q) | 2026-09-20 (Step 0 abgeschlossen — Phasenverzeichnis, INDEX-Rotationsskript, vier geplante plus drei ungeplante Doku-Defekte repariert, `doc_health.py` als Test festgenagelt, Baseline gemessen)
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
| F | Schema-Fundament (neunte P1-Contract-Öffnung: `doing`/`assignee`) | 🟡 **code-complete 2026-09-30 (M3), nicht live-bewiesen** — V160 vom Nikinger beantwortet (**Space-Name, ohne Validierung**), Plan §8.2 auf **18 Hunks in genau drei Dateien** korrigiert (die Probe §8.7 erfüllt: `models.py`/`store.py`/`index.py`, sonst nichts); drei vom Plan nicht genannte Stellen ergänzt (`_summary()` = F10, `update()` = F11, `_coerce_assignee()`) · **ein Befund bewusst NICHT behoben**: `_BUCKETS` kennt `doing` nicht, beide Kandidaten sind Darstellungsentscheidungen und damit P10 (P9-P) · `pytest` 1039 → **1062** (23 neu), `ui_budget` 5/5, Tabu-Hartpfade unberührt. Der Contract-Absatz steht in `phase1_storage/CLAUDE.md` §Geerbte Contracts · **V161 mit synthetischem Vorabwert** (2,5–4,0 ms/Item gemessen, 153 reale Items ⇒ **0,4–0,6 s** einmalige Startkosten; P9-43 selbst bleibt Nikinger-Schritt am echten DATA_ROOT) |
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

## Session stopped — 2026-09-30 (zweiter Block, Step F)

**Step F ist gebaut: `doing` wird ein Statuswert, `assignee` ein erstklassiges Feld mit
Index-Spalte — die neunte und bis jetzt letzte P1-Contract-Öffnung.** Der Domain-Block hängt
weiter an der Registrierung; F war der einzige Step, der neben ihm ohne externe Abhängigkeit
lag. Kein Service-Touch, `pytest` grün, Tabu-Hartpfade unberührt.

### V160 ist beantwortet: `assignee` ist ein Space-Name, ohne Validierung

Der Plan (§8.4) hat die Frage gestellt und die Empfehlung offengelassen; der Nikinger hat
2026-09-30 die Empfehlung bestätigt. `_coerce_assignee()` prüft **nur den Typ**. Warum keine
Prüfung gegen die Space-Liste: das wäre eine **zweite**, nicht angekündigte Contract-Öffnung —
der Schreibpfad müsste den Space auflösen, mit dem ein Item in einem fremden Space belegt sein
könnte. Die Formulierung, die ich mir gemerkt habe: ein toter Space-Name ist ein Anzeigefehler,
ein *erfundener* Zweiter Space wäre es nicht.

### Der Plan sagte neun Stellen, der Diff hat achtzehn

Plan §8.2 listet F1–F9 in genau drei Dateien. Gemessen am Diff: **18 Hunks** (`models.py` 4,
`store.py` 8, `index.py` 6). Die Differenz ist kein Pfusch, sondern eine Lücke in der Liste:
**F9 („Upsert") sind drei Statement-Teile plus ein Row-Dict**, nicht eine Stelle — nur das
Row-Dict zu ändern hätte den Index mit `ProgrammingError` laufen lassen. Dazu kamen **drei
Stellen, die der Plan nicht nannte und ohne die es nicht funktioniert hätte**:

| # | Stelle | Was ohne sie passiert wäre |
|---|---|---|
| **F10** | `store._summary()` | `get()` kennt den Wert, **jede Liste und jede Suche** stünde dauerhaft auf `""`. F3 wäre ein totes Feld — und kein Test hätte es gemerkt, weil beide Seiten „funktionieren" |
| **F11** | `store.update()` | Der Wert **würde** in die Datei gelangen (über `Item.extra` → `fields.update()`), `item.assignee` bliebe auf `""`, F6 (`if item.assignee`) feuerte nie. Der am leichtesten übersehene Fall, weil „es funktioniert" hier kein Beweis ist |
| — | `store._coerce_assignee()` | Die Typprüfung einmal im Kern statt dreimal in den Adaptern — dieselbe Begründung wie `_check_type_and_status()` (D2) |

Die Kette dahinter ist immer dieselbe: ein Feld, das nur halb verdrahtet ist, sieht fertig aus.

### Ein Befund, den ich gefunden, gemessen und **nicht** behoben habe

`_BUCKETS` in `api.py` kennt kein `doing`. `bucketFor()` (`list.js:516`) vergleicht
`f.status === item.status` **exakt**, eine `doing`-Aufgabe passt auf keinen der vier Eimer,
`bucketFor()` liefert `null`, beide Aufrufer fallen auf `|| state.filter` zurück: sie fehlt in
jedem Zähler und ist in der Liste nur sichtbar, wenn man zufällig im passenden Filter steht.
**Derselbe Fund wie bei `done` im Phase-5-Step-7b**, eine Statusversion später.

Ich habe den Fix gebaut und dann **verworfen**, weil beide Kandidaten Darstellungsentscheidungen
sind, die P9-P ausdrücklich P10 zuteilt: ein fünfter `_BUCKETS`-Eintrag erzeugt über
`bucketNames() = Object.keys(state.meta.buckets)` und `tree.js:72` einen **fünften Rail-Eintrag
mit unübersetztem Label** — das ist genau die Hervorhebung, die nicht in diesen Step gehört. Der
Befund steht vollständig mit beiden Kandidaten im Code, und ein Wächter pinnt, dass er nicht
verschwindet, ohne dass P10 ihn behoben hat.

### Zwei Alt-Tests, die mitgezogen werden mussten — und was sie über Kalibrierung lehren

`test_upsert_get_delete_roundtrip` baut seine Indexzeile von Hand und schlug mit
`ProgrammingError: missing parameter` fehl. **Das ist richtig so** — benannte Parameter schlagen
laut fehl, statt still einen Default zu nehmen. Der Test trägt den Key jetzt und prüft zusätzlich
den `ON CONFLICT`-Zweig.

Der zweite war der lehrreichere: `test_search_listing_of_30_items_stays_within_calibrated_json_bound`
sagt in seinem eigenen Docstring, dass eine `ItemSummary`-Feldsatz-Änderung **Nikinger-Sache und
kein stiller Nebeneffekt** ist. Also gemessen statt erhöht: **16.390 B** mit Feld gegen **16.300 B**
ohne, exakt **+16 B/Item** (`"assignee": "",`). Band 12–16 KB → **13–18 KB**, mit ungefähr
gleicher Marge. Der Test hat die echte Zunahme bemerkt, statt eine Toleranz zu schlucken.

Eine eigene Fehlannahme unterwegs: ich hatte `400` für einen Validierungsfehler erwartet, die API
liefert `422` (`errors.py:50`). Der Code hatte recht, mein Test nicht.

### V161: mit einem synthetischen Vorabwert beantwortet, P9-43 bleibt beim Nikinger

`rebuild_index()` über 500/1500/3000 Items in `tmp_path`: **2,45 / 2,48 / 4,01 ms pro Item** —
bis 1500 linear, bei 3000 etwas schlechter. Der echte `DATA_ROOT` (nur gelesen) hat **153 Items**
außerhalb `_archive`, 197 mit: **0,4–0,6 s** einmalige Startkosten beim Schema-Sprung 3 → 4.
Das ist der Vorabwert, den die Plan-Session brauchte; **P9-43 bleibt die Messung am echten
`DATA_ROOT` beim Deploy**, denn ein `rebuild_index()` dort ist ein Schreibzugriff auf Produktivdaten.

### Was gemessen wurde

| Gegenstand | Nachweis |
|---|---|
| **Enge Probe §8.7** | `git diff --stat -- phase1_storage/storage` = **genau drei Dateien**; die sechs Hartpfade `acl.py`/`linkscan.py`/`patch.py`/`files.py`/`history.py`/`frontmatter.py` leer |
| **Gegenprobe** | vier Verstöße eingebaut (F10 raus, F11 raus, Version zurück auf 3, F6 ohne `if`) → **10 Tests rot**, exakt die zuständigen; danach zurückgebaut |
| **`doing` in der Oberfläche** | **V159 gemessen, nicht geglaubt**: `editor.js:246` liest `state.meta.status_values[itemType]` und rendert rohe Werte — `doing` erscheint im Editor-Dropdown ohne JS-Änderung. Die Plan-Behauptung zu `dialogs.js:323` ist **halb richtig**: dort iteriert `Object.keys(state.meta.status_values)`, also das **Typ**-Vokabular, und der Anlegen-Dialog hat gar keinen Status-Knopf (`createStatus` existiert nicht) — für ihn ist die Aussage gegenstandslos |
| **Tests** | `pytest` **1039 → 1062** in 186,8 s (23 neu: 17 `test_step_f_schema.py`, 4 `test_tools.py`, 2 `test_api.py`), davon 191 in `phase1_storage`; `ui_budget` 5/5; `doc_health.py` 0 Befunde; `node --check` über alle 13 JS-Dateien grün (keine JS-Datei geändert) |

### Nächster Schritt

**Zwei Kandidaten, und sie sind nicht gleichwertig:**

1. **Warten auf die Domain** (A5 → A4 → A7 → A8), sobald `eurofyx.<tld>` registriert ist. Die
   Kette ist unberührt und der Nikinger hatte sie zuletzt in der Hand.
2. **Step G** (Löschen nach `_trash/`, P9-I/J/K) — der andere reine Code-Step. **Achtung, die
   Reihenfolge ist nicht beliebig:** §8.7 warnt ausdrücklich davor, F und G zu vermischen, weil
   G `store.py` erneut anfasst (`Store.trash()`); der enge Diff gegen **diesen** Commit bleibt
   sauber, solange G ein eigener Commit ist. **V160-analoge Frage für G:** `delete` für
   wen sichtbar? Der Plan sagt human-only und für Nutzer unsichtbar, das wäre also geklärt.
