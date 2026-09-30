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
updated: 2026-09-30 (**Step H gebaut — der letzte Code-Step, und seine Plan-Prämisse war falsch: „installiert ist 3.4.4". Gemessen (read-only) lief der Live-Release bereits auf **3.4.7**, weil `deploy.sh:153` pro Release ein frisches venv baut und der Pin ein **Range** war — der stumme Patch-Drift, den P3-D verbieten wollte, hatte also schon stattgefunden. `phase2_mcp/pyproject.toml` pinnt jetzt **`fastmcp==3.4.7`** exakt (P3-D/P4-R, beide seit 2026-08 beschlossen und nie umgesetzt) + datierter Kommentar; **V163 beantwortet** mit drei Codepunkten statt einer Vermutung: CIMD ist per P4-E abgeschaltet (`metadata.py:19`), `token_endpoint_auth_methods_supported: ["none"]` (`metadata.py:32`), kein `OAuthProxy`/`JWTVerifier` in der benutzten Fläche — der 3.4.7-Fix ist inert, der Bump ist Hygiene. **P9-55 in der Form abweichend** (`==3.4.7` statt Range, Nikinger-Entscheidung 2026-09-30), im Plan §10 als Abweichung dokumentiert. **Der Riegel ist ein Test:** `test_the_installed_fastmcp_matches_the_pin` läuft im **Release-venv** mit (`deploy.sh:169` ruft dort `pytest -q` und bricht den Deploy ab) — ein Drift ist damit ein roter Deploy. 5 Wächter, Gegenprobe 4 Verstöße → 7 rote Assertions. `pytest` 1079 → **1084**, `ui_budget` 5/5. **Benannt, nicht gebaut:** transitives `mcp` bleibt ungepinnt (Dev 1.28.1, Live 1.30.0). Zwei eigene Fehler (ein `SpecifierSet.version`, das es nicht gibt; ein `edit`, das P2-Zeile 13 mitgefressen hat — beide im selben Commit behoben, der Diff ist der Nachweis). **Domain weiter nicht registriert** (NXDOMAIN + RDAP 404) → A4/A5/A7/A8 blockiert, Gate/Z wartet) | 2026-09-30 (**Step F gebaut — neunte und bis jetzt letzte P1-Contract-Öffnung, code-complete, nicht live-bewiesen**: `doing` wird ein Statuswert (nur bei `task`, `note` bleibt `{active, archived}`), `assignee` ein erstklassiges Feld mit Index-Spalte, `INDEX_SCHEMA_VERSION` 3 → 4, **keine Migration** (Hard Rule 2). **V160 vom Nikinger beantwortet: Space-Name, ohne Validierung** — eine Prüfung gegen die Space-Liste wäre eine zweite, nicht angekündigte Öffnung. **Plan §8.2 auf den Diff korrigiert: neun Stellen sind gemessen achtzehn Hunks** (F9 sind drei Statement-Teile plus ein Row-Dict, nicht eine Stelle), dazu drei vom Plan nicht genannte Pflichtstellen (`_summary()` F10, `update()` F11, `_coerce_assignee()`). Enge Probe §8.7 erfüllt: **genau drei Dateien**, die sechs Hartpfade leer; Gegenprobe mit vier eingebauten Verstößen → 10 Tests rot. `pytest` 1039 → **1062** (23 neu), `ui_budget` 5/5, `doc_health` 0, `node --check` grün. **Ein Befund bewusst NICHT behoben:** `_BUCKETS` kennt `doing` nicht — beide Fix-Kandidaten sind Darstellungsentscheidungen und P10-Arbeit (P9-P), der Befund steht im Code und ein Wächter pinnt ihn. **V161 mit synthetischem Vorabwert** (2,5–4,0 ms/Item; 153 reale Items ⇒ 0,4–0,6 s einmalig), P9-43 bleibt Nikinger-Schritt am echten DATA_ROOT. **V159 gemessen statt geglaubt:** richtig für den Editor-Dropdown, gegenstandslos für den Anlegen-Dialog (der hat keinen Status-Knopf)) | 2026-09-30 (Step A halb ausgeführt — **A1/A2/A3/A0b/A6 erledigt**: Domain bestellt, VPS `217.160.128.146` (Ubuntu 24.04.5), Policy + Beitritt mit `tag:sharefyx-edge` (von der Gegenseite belegt: Tags gesetzt, User=None), socat-Relay laufend mit identischer Härtung, Firewall `22` nur auf `tailscale0` mit Gegenprobe. **Kette blockiert an der Domain-Registrierung** — A4 braucht eine auflösende Domain fürs Zertifikat. Der Session-Fund: **mein eigenes A6 hätte den Betrieb gekappt** (`ufw default deny incoming` gilt auch auf `tailscale0`, SSH-Regel fehlte). Vier eigene Fehler dokumentiert, darunter ein erfundener Drift, der zurückgenommen wurde. V162/V163 neu offen, V151 Vorabwert 28–37 ms über DERP. 7 Tests + Gegenprobe 4/4) | 2026-09-29 (Step A: M3-Anteil gebaut, Ausführung liegt beim Nikinger — **Plan-A4 nachweislich unbaubar** (auf der Tailnet-IP lauscht nichts: `SPACE_HOST=127.0.0.1`, `ss -ltnp` belegt; `SPACE_HOST=0.0.0.0` wäre P3-B gebrochen) → **socat-Relay-Unit** `phase3_edge/systemd/sharefyx-tail-proxy.service` ohne `__REPO_ROOT__` im `ExecStart` (die Release-Pfad-Kopplung aus dem Step-B-Befund ist damit konstruktiv ausgeschlossen); Caddy-Vorlage + ACL-Fragment + `phase9_hardening/step_a/RUNBOOK_STEP_A.md` (A1–A9, ein Schritt pro Runde) + 7 Wächter, Gegenprobe 4/4; **V149 beantwortet** (alle Metadatenfelder abgeleitet, keines fest, kein `iss`-Check beim Einlösen), Befund 2 (`/health` statt `/healthz`) und Befund 3 (`ALLOWED_HOSTS` fehlt in Plan-A7) als Plan-Korrekturen, **Befund 5** = der Funnel bleibt nach A7 lesbar, aber nicht beschreibbar (CSRF-Origin exakt, `security.py:84`); **V162 neu offen** = ACL-Durchsetzung von `tailscale serve --tcp`, der Grund für die socat-Wahl; Step A ⬜→🟡) | 2026-09-28 (**Nachtrag**: §Vormerkung Vision-Modell — Messbefund aus Step E dokumentiert, Recherche in `docs/concepts/sichtpruefung_automation_tooling.md`, Schluss: ein Modellwechsel ist nicht der Hebel, die Zuständigkeitsgrenze ist es; kein P9-Block) | 2026-09-28 (Step E abgeschlossen ✅ — Reload-Overload der Karte: (a) kein zweiter `/graph`-Abruf ohne Datenänderung, Signatur aus dem `/overview`-Payload statt aus dem Graph-Payload (Plan-Korrektur: der Graph-Knoten hat kein `updated`, `api.py:698-708`), Erzeugung in `list.js :: loadOverview()` (deckt jeden Schreibpfad mit), Format in `state.js :: overviewToken()` (Blatt-Modul statt Zyklus), `force` nur am expliziten Refresh-Knopf; (b) bekannte Knoten behalten x/y über den Refetch. Sieben Tests (Node-Harness `graph_reload_probe.mjs` + statisch) und eine Browser-Probe (`p9e_reload_probe.py`, Wegwerf-Instanz Port 18768), beide mit Gegenprobe gegen HEAD: dort 1 statt 0 Abrufe und 10 statt 1 verschiedene Bilder in 1,5 s, im Node-Harness 467,6 px Positionssprung statt 0. V118 beantwortet (zwei Linien, eine gestrichelt) — Design-Frage eine-oder-zwei beim Nikinger. `pytest` 1031 passed + 1 failed (der Fehlschlag ist der Vortrag: `docs/INDEX.md` über der doc_health-Schwelle, auf HEAD genauso rot, gehört nach Step Z), `ui_budget` 5/5 (149,0 KB), Tabu-Bereichs-Diff leer, Wegwerf-Instanz über die PID-Datei gestoppt. Drei eigene Fehler dokumentiert (falsche erste Verdrahtung, Messgerät zählte sich selbst, Test scheiterte an eigenem Kommentar) | 2026-09-26 (Step B code-complete, install ausstehend: vier neue Dateien — `phase3_edge/scripts/tailscaled_watchdog.sh` + `phase3_edge/systemd/tailscaled-watchdog.{service,timer}` + `phase9_hardening/tests/test_tailscaled_watchdog.py` (5/5 grün); V152 beantwortet (kein Tailscale-eigenes Feature ohne kommerzielles Add-on), V153 als Empfehlung dokumentiert (Polkit `.rules`-Datei `/etc/polkit-1/rules.d/99-tailscaled-watchdog-restart.rules`, Sudoers-Fallback `/etc/sudoers.d/tailscaled-watchdog-restart`); Modulstatus Step B ⬜→🟡, Phase-9-###-Sub-Sektion ergänzt; Phase-9-Zeile in `docs/INDEX.md` nachgezogen; kein Touch an bestehendem Code, Hard Rule 8 (Doc-Update im selben Commit) und Hard Rule 9 (kein `systemctl` durch M3) eingehalten) | 2026-09-26 (Step C abgeschlossen: C8 `sudo systemctl disable --now ollama` Nikinger-Cobefehl, sharefyx-VM `inactive`/`disabled`, `curl 127.0.0.1:11434` → HTTP 000 exit 7 `Connection refused` (bestätigt aus dieser Shell als zweite Sichtprobe), binary + Modell bleiben als kalter Fallback bis Step Z; Host-Aufräumen pve: `/root/111.conf.new` (633 B, 2026-09-25 22:41) und `/root/111.conf.bak-p9c` (842 B, 2026-09-25 22:41) per `rm -f` entfernt, `/tmp/nv580173` und alter `NVIDIA-Linux-x86_64-580.126.09.run` waren bereits weg — PVE-9-tmpfs bzw. im Vorrundezweig schon entfernt; P9-22 deferred — kein externer Test möglich, architektonischer Beweis captured: 192.168.68.140 ist RFC1918, sharefyx-VM hat keine öffentliche IP (CGNAT via RUT X50, default route via 192.168.68.1), Tailscale-Funnel mappt nur `127.0.0.1:8765` (kein `*:11434` auf sharefyx-VM), kein Port-Forward auf RUT X50, der einzige 11434-Listener ist innerhalb CT 111; Step C 🟡→✅, Modulstatus nachgezogen, Session-Block 2026-09-26 angehängt) | 2026-09-25 (C4 ✅ DHCP-Reservierung im RUT X50, per `local_vision`-MCP-Aufruf gegen die GPU ausgelesen — erster echter Einsatz über den opencode-Pfad) | 2026-09-25 (zweite Reboot-Probe grün: CT-Knoten 20:54 > 20:42, Major 235 = `/proc/devices`, `cuInit = 0`, `size_vram` = `size` — Boot-Persistenz ✅) | 2026-09-25 (Reboot-Probe: uvm-Major 511→235, `cuInit = 999`; Fix per `devN`-Passthrough, per CT-Neustart bewiesen `cuInit = 0`, zweite Reboot-Probe offen, `size_vram` = `size`; C5 gesetzt; V166 beantwortet) | 2026-09-25 (Boot-Persistenz eingerichtet, CT 111 `onboot: 0` gefunden, Reboot-Probe offen) | 2026-09-25 (GPU-Inferenz läuft: CT 111 auf 580.173.02, `size_vram` = `size`, 63 tok/s, P9-21/-23/-26 ✅; Boot-Persistenz offen) | 2026-09-25 (Host-Treiber 580.173.02 mit `nvidia-uvm` installiert und geladen, kein Reboot) | 2026-09-25 (V165 beantwortet: 580.173.02 kennt die neue `zone_device_page_init`-Signatur) | 2026-09-25 (Step C Diagnose bestätigt: kein `/dev/nvidia-uvm`, `cuInit = 999`) | 2026-09-25 (Step C Diagnose, Claude Code: CUDA fehlt, weil `nvidia-uvm` fehlt — C2-Trade-off-Satz datiert korrigiert, Modulstatus C nachgezogen, Nikinger-Entscheidung zum Host-Fix offen) | 2026-09-25 (Backlog aufgeräumt: „opencode via Tailscale" für sharefyx-VM per Nikinger-Update mittlerweile passiert, Eintrag aus der Backlog-Sektion entfernt; nur noch D1 zurückgestellt) | 2026-09-25 (Step C Teil 2 / C6 — `mcp_local_vision_server.py` Skript-Fixes aus Plan §5.3: `serve()` loggt aufgelösten Endpoint, `--endpoint` wirkt jetzt auch ohne `--check`; neue zentrale `resolve_endpoint(args)` mit Präzedenz `--endpoint` > `$LOCAL_VISION_ENDPOINT` > `DEFAULT_ENDPOINT`; `_CURRENT_ENDPOINT` als Modul-Globals wird in `serve()` einmal gesetzt und von `handle_tools_call` gelesen statt erneut die Umgebungsvariable; 9 neue Tests + Counter-Probe ohne den Fix 7/9 rot — exakt die zwei gemeldeten Bugs; LXC + Ollama + C5/C7/C8 stehen aus) | 2026-09-24 (Step C Teil 1 — NVIDIA-Host-Treiber 580.126.09 installiert mit `--no-unified-memory`; pve-no-subscription-Repo ergänzt; drei dokumentierte Fehlbarkeiten auf dem Weg (Header-Paket fehlte, Backports führten denselben Upstream, Nouveau-Konflikt, uvm_hmm.c gegen 7.0.2-6-pve-Mai-Patch); eigener autoremove-Vorfall mit sudo/dkms-Verlust am 2026-09-24 wieder behoben; LXC + Ollama stehen aus) | 2026-09-24 (Backlog: ~19-min mcp-proxy.anthropic.com-Ausfall dokumentiert und geschlossen — gemessen nicht CGNAT/sharefyx-VM-seitig, Nikinger-Anordnung) | 2026-09-24 (Backlog: "opencode via Tailscale"-Behandlung für sharefyx-/Trading-Bot-VM nachgetragen, Nikinger-Feedback aus Netzwerk-Diagnosesession, kein Produktcode-Touch) | 2026-09-23 (D1/ESC-Bug auf Nikinger-Anordnung zurückgestellt, `## Backlog` neu) | 2026-09-23 (Step D code-complete — Drop-Ziel Space-Wurzel, ESC/Vollbild-Guard gebaut, gebaut in Claude Code statt opencode/M3, benannte Abweichung von P9-Q) | 2026-09-20 (Step 0 abgeschlossen — Phasenverzeichnis, INDEX-Rotationsskript, vier geplante plus drei ungeplante Doku-Defekte repariert, `doc_health.py` als Test festgenagelt, Baseline gemessen)
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
| G | Löschen (F2) nach `_trash/` | 🟡 **code-complete 2026-09-30 (M3), nicht live-bewiesen** — **der Lösch-Ort aus Plan §9.3 war unbaubar** (`<space>/_trash/` ⇒ Item nach `rebuild_index()` wieder da, `_trash` sogar als **Phantom-Space** in `list_spaces()`; `rebuild_index()` rglobbt ohne Skip, `RESERVED_DIR_NAMES` kennt `_trash` nicht) — Nikinger-Entscheidung: `DATA_ROOT/._trash/<space>/`, beide Scanner überspringen Punkt-Verzeichnisse, **null P1-Änderungen** · `Store.trash(item_id, *, version)` atomar + Git-Commit `trash`, `DELETE /api/v1/items/{id}` mit **serverseitigem** Titel-Gate (Muster `api.py:567`), `version` Pflicht, P9-K: kein MCP-Werkzeug, kein Bulk, kein Tastenkürzel, fremde Items gesperrt · 13 + 5 Tests, **Gegenprobe 4 Verstöße → 11 Tests rot**, **Browser 14/14** (eigene TLS-Wegwerf-Instanz) · §9.3 nannte 4 Dateien, gebaut wurden 7 (Markup, ESC, CSS und Icon sind durch das Getippte-Gate erzwungen) · `pytest` 1062 → **1078** |
| H | Abhängigkeits-Hygiene | 🟡 **code-complete 2026-09-30 (M3)** — **die Plan-Prämisse „installiert ist 3.4.4" war falsch, und genau das war der Fund:** der Live-Release lief bereits auf **3.4.7** (read-only gemessen an `/opt/sharefyx/current/.venv`), weil `deploy.sh:153` pro Release ein frisches venv baut und der Pin ein **Range** war — der stumme Patch-Drift, den P3-D verbieten wollte, hatte also schon stattgefunden. `phase2_mcp/pyproject.toml` pinnt jetzt **`fastmcp==3.4.7`** exakt (P3-D/P4-R, beide seit 2026-08 beschlossen und nie umgesetzt) + datierter Kommentar; **V163 beantwortet** (drei Codepunkte: CIMD per P4-E abgeschaltet, `token_endpoint_auth_methods_supported: ["none"]`, kein `OAuthProxy`/`JWTVerifier` — der Fix ist inert, der Bump ist Hygiene) · **P9-55 in der Form abweichend** (`==3.4.7` statt Range, Nikinger-Entscheidung 2026-09-30) · 5 Wächter in `phase9_hardening/tests/test_step_h_deps.py`, einer vergleicht installiert-gegen-deklariert und **läuft im Release-venv mit** (`deploy.sh:169`) — Gegenprobe 4 Verstöße → 7 rote Assertions. `pytest` 1079 → **1084**, `ui_budget` 5/5. **Benannt, nicht gebaut:** das transitive `mcp` bleibt ungepinnt (Dev 1.28.1, Live 1.30.0), P9-Backlog-Kandidat. Lock P9-R unangetastet, V79 bleibt |
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

## Session stopped — 2026-09-30 (vierter Block, Step H)

**Step H ist gebaut, und die Reihenfolge entschied sich an einer Messung: die Domain ist nicht
registriert.** `eurofyx.com` liefert `NXDOMAIN` **und** `rdap.verisign.com` 404, dieselbe Antwort
für `.de`/`.tech`/`.app`/`.cloud`/`.net`/`.org`/`.eu` — A4 braucht eine auflösende Domain fürs
Zertifikat, also bleiben A4/A5/A7/A8 blockiert und der letzte Code-Step wird gezogen. `pytest`
**1084**, `ui_budget` 5/5, kein Service-Touch.

### Der Fund: die Plan-Prämisse „installiert ist 3.4.4" war falsch — der Drift hatte schon stattgefunden

| Ort | `fastmcp` | `mcp` |
|---|---|---|
| Live-Release `/opt/sharefyx/current/.venv` (read-only) | **3.4.7** | 1.30.0 |
| Dev-`.venv` (vorher) | 3.4.4 | 1.28.1 |
| `phase2_mcp/pyproject.toml` — seit dem ersten Commit `1c131c2` | `>=3.4,<3.5` | — |

`deploy.sh:153` baut pro Release ein **frisches** venv, `scripts/dev_install.sh:9-13` installiert
editable — ein Range-Pin löst bei jedem Deploy auf das **damalige** neueste 3.4.x auf. Der
Patch-Wechsel hat also unbemerkt stattgefunden, mit dem Release vom 2026-09-18. P3-D
(`phase3_edge_plan.md:106`) wollte genau das verbieten („unter einem Dauerdienst darf sich das
nicht unbemerkt bewegen"), P4-R wiederholte es — **im Code stand nie ein exakter Pin.** Zwei
Pläne, eine Entscheidung, null Umsetzung; das war der Drift, nicht der Bump.

**Gebaut:** `fastmcp==3.4.7` exakt, mit datiertem Kommentar an der Zeile (Grund, Messung,
P9-R/V79/V163). Das ist die Einlösung von P3-D, keine neue Entscheidung — Präzedenz ist
`phase4_auth/pyproject.toml` mit `argon2-cffi==25.1.0` und `cryptography==49.0.0`.
**P9-55 verlangte wörtlich „weiterhin `<3.5`"**; gebaut ist `==3.4.7`, oberhalb jeder 3.4-Version,
also innerhalb P9-R, aber ohne die Range-Form — **Nikinger-Entscheidung 2026-09-30**, weil die
Range-Form der Mechanismus des gemessenen Drifts ist. Als Abweichung im Plan §10 dokumentiert,
nicht stillschweigend.

**Der eigentliche Riegel ist ein Test.** `test_the_installed_fastmcp_matches_the_pin` vergleicht
die installierte Version mit der Pin-Zeile — und läuft im **Release-venv** mit, weil `deploy.sh:169`
dort `pytest -q` aufruft und den Deploy bei Fehlschlag abbricht. Ein Patch-Drift ist damit ein
roter Deploy statt einer Randnotiz. Fünf Wächter, **Gegenprobe mit vier eingebauten Verstößen →
7 rote Assertions über vier Tests**: Range-Pin (3 rot), Pin auf 4.x (2 rot), `V79` aus dem
Kommentar entfernt (1 rot), zweiter Pin in `phase4_auth` (1 rot). Alles zurückgebaut, 5/5 grün.

### V163 ist beantwortet — drei Codepunkte statt einer Vermutung aus dem Aufrufbild

1. `phase4_auth/authserver/metadata.py:19` lässt `client_id_metadata_document_supported`
   **bewusst abwesend** — CIMD ist aus, Claude nimmt DCR (P4-E, V14). Der Fix betrifft CIMD.
2. `metadata.py:32`: `token_endpoint_auth_methods_supported: ["none"]` — öffentlicher Client, es
   werden gar keine Client-Assertions erzeugt.
3. Die benutzte fastmcp-Fläche ist `FastMCP`/`Client`/`StreamableHttpTransport`/`ToolError`/
   `Image`/`Middleware`/`get_http_request`/`http_app` — **kein `OAuthProxy`, kein `JWTVerifier`**;
   Auth trägt der eigene `BearerAuthASGI` (`asgi.py:40`).

Die drei Releases dazwischen (3.4.5 JWKS-Key-Skip, 3.4.6 Trusted-Proxy für SSRF-Metadaten, 3.4.7
CIMD-Audience) liegen alle auf Pfaden, die dieses Projekt nicht benutzt. **Der Fix ist inert, der
Bump ist Hygiene** — genau wie am 2026-09-19 vermutet, jetzt gemessen. Dass er trotzdem prod-seitig
stattgefunden hat, ist der Grund, warum der Step nicht nur ein Kommentar war.

### Ein eigener Fehler, beim Wächter-Schreiben

`req.specifier.version` gibt es nicht (`SpecifierSet` hat kein `.version`) — zwei Tests rot, bevor
der Helper existierte. Genau die Klasse Fehler, die der Wächter verhindern soll, hat mich der
Wächter zuerst einmal selbst gekostet. Beim selben Durchgang: ein `edit` auf die P2-Modulstatus-
Tabelle hat **Zeile 13 mitgefressen** (Anker war der Zeilenanfang statt des Zeilenendes). Beides
gesehen, weil `git diff` nach dem Edit **rein additiv** hätte sein müssen — der Nachweis steht
jetzt im Diff (13 Zeilen rein, 0 raus).

### Was gemessen wurde

| Gegenstand | Nachweis |
|---|---|
| **Domain** | `dig +short eurofyx.<tld> @1.1.1.1` → **NXDOMAIN** für alle sieben Kandidaten; `rdap.verisign.com/com/v1/domain/eurofyx.com` → **404** |
| **Prod-Version** | read-only über `/opt/sharefyx/current/.venv/bin/python` → `fastmcp 3.4.7`, `mcp 1.30.0` — **nur gelesen**, kein `systemctl`, kein Restart |
| **Gegenprobe** | vier Verstöße eingebaut → 7 rote Assertions, danach per `cp` aus dem Backup zurückgebaut; `git diff --stat` zeigt nur `phase2_mcp/pyproject.toml` |
| **Tests** | 5 neue in `phase9_hardening/tests/test_step_h_deps.py`; `pytest` 1079 → **1084** in 186 s (Bestand unverändert, **mit** 3.4.7 im Dev-venv) · `ui_budget` **5/5** (151,8 KB; `search_items` 128,6 ms / `get_item` 4,7 ms über den echten MCP-Stack, also der 3.4.7-Pfad wirklich gelaufen) · `doc_health` 0 Befunde |
| **P1-Tabu** | nichts in `phase1_storage/` berührt — der Pin ist Phase-2-Terrrain, die Tabu-Liste nicht |

**Benannt, nicht gebaut:** das transitive `mcp` ist weiterhin **nicht** gepinnt (Dev 1.28.1, Live
1.30.0). Ein expliziter `mcp`-Pin wäre eine Lock-Entscheidung, die kein Plan getragen hat —
P9-Backlog-Kandidat, kein Blocker.

### Nächster Schritt

**Step A wartet auf die Domain-Registrierung** — das ist jetzt die einzige offene Kette in P9 und
der Grund, warum H gezogen wurde, bevor Gate/Z kam. Sobald `eurofyx.<tld>` auflöst: A4 (Caddyfile,
drei Platzhalter) → A5 DNS → **A7 ist der riskante Schritt** (drei gemessene Fallen:
`ALLOWED_HOSTS` braucht neue Domain **und** Funnel-Host **und** `127.0.0.1`, `/health` statt
`/healthz`, und nach `install_units.sh` ein eigener `restart sharefyx-mcp`) → A8 Connector in
beiden Konten. **Gate/Z** kann ohne A4–A8 nicht abgeschlossen werden; die beiden Doku-Posten
daraus (INDEX-Rotation P9-L bei 50.033 B, Contract-Rotation in `phase1_storage/CLAUDE.md` bei
43.333 B) sind strukturell und nicht durch Kürzen lösbar.
