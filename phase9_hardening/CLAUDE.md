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
updated: 2026-09-28 (Step E abgeschlossen ✅ — Reload-Overload der Karte: (a) kein zweiter `/graph`-Abruf ohne Datenänderung, Signatur aus dem `/overview`-Payload statt aus dem Graph-Payload (Plan-Korrektur: der Graph-Knoten hat kein `updated`, `api.py:698-708`), Erzeugung in `list.js :: loadOverview()` (deckt jeden Schreibpfad mit), Format in `state.js :: overviewToken()` (Blatt-Modul statt Zyklus), `force` nur am expliziten Refresh-Knopf; (b) bekannte Knoten behalten x/y über den Refetch. Sieben Tests (Node-Harness `graph_reload_probe.mjs` + statisch) und eine Browser-Probe (`p9e_reload_probe.py`, Wegwerf-Instanz Port 18768), beide mit Gegenprobe gegen HEAD: dort 1 statt 0 Abrufe und 10 statt 1 verschiedene Bilder in 1,5 s, im Node-Harness 467,6 px Positionssprung statt 0. V118 beantwortet (zwei Linien, eine gestrichelt) — Design-Frage eine-oder-zwei beim Nikinger. `pytest` 1031 passed + 1 failed (der Fehlschlag ist der Vortrag: `docs/INDEX.md` über der doc_health-Schwelle, auf HEAD genauso rot, gehört nach Step Z), `ui_budget` 5/5 (149,0 KB), Tabu-Bereichs-Diff leer, Wegwerf-Instanz über die PID-Datei gestoppt. Drei eigene Fehler dokumentiert (falsche erste Verdrahtung, Messgerät zählte sich selbst, Test scheiterte an eigenem Kommentar) | 2026-09-26 (Step B code-complete, install ausstehend: vier neue Dateien — `phase3_edge/scripts/tailscaled_watchdog.sh` + `phase3_edge/systemd/tailscaled-watchdog.{service,timer}` + `phase9_hardening/tests/test_tailscaled_watchdog.py` (5/5 grün); V152 beantwortet (kein Tailscale-eigenes Feature ohne kommerzielles Add-on), V153 als Empfehlung dokumentiert (Polkit `.rules`-Datei `/etc/polkit-1/rules.d/99-tailscaled-watchdog-restart.rules`, Sudoers-Fallback `/etc/sudoers.d/tailscaled-watchdog-restart`); Modulstatus Step B ⬜→🟡, Phase-9-###-Sub-Sektion ergänzt; Phase-9-Zeile in `docs/INDEX.md` nachgezogen; kein Touch an bestehendem Code, Hard Rule 8 (Doc-Update im selben Commit) und Hard Rule 9 (kein `systemctl` durch M3) eingehalten) | 2026-09-26 (Step C abgeschlossen: C8 `sudo systemctl disable --now ollama` Nikinger-Cobefehl, sharefyx-VM `inactive`/`disabled`, `curl 127.0.0.1:11434` → HTTP 000 exit 7 `Connection refused` (bestätigt aus dieser Shell als zweite Sichtprobe), binary + Modell bleiben als kalter Fallback bis Step Z; Host-Aufräumen pve: `/root/111.conf.new` (633 B, 2026-09-25 22:41) und `/root/111.conf.bak-p9c` (842 B, 2026-09-25 22:41) per `rm -f` entfernt, `/tmp/nv580173` und alter `NVIDIA-Linux-x86_64-580.126.09.run` waren bereits weg — PVE-9-tmpfs bzw. im Vorrundezweig schon entfernt; P9-22 deferred — kein externer Test möglich, architektonischer Beweis captured: 192.168.68.140 ist RFC1918, sharefyx-VM hat keine öffentliche IP (CGNAT via RUT X50, default route via 192.168.68.1), Tailscale-Funnel mappt nur `127.0.0.1:8765` (kein `*:11434` auf sharefyx-VM), kein Port-Forward auf RUT X50, der einzige 11434-Listener ist innerhalb CT 111; Step C 🟡→✅, Modulstatus nachgezogen, Session-Block 2026-09-26 angehängt) | 2026-09-25 (C4 ✅ DHCP-Reservierung im RUT X50, per `local_vision`-MCP-Aufruf gegen die GPU ausgelesen — erster echter Einsatz über den opencode-Pfad) | 2026-09-25 (zweite Reboot-Probe grün: CT-Knoten 20:54 > 20:42, Major 235 = `/proc/devices`, `cuInit = 0`, `size_vram` = `size` — Boot-Persistenz ✅) | 2026-09-25 (Reboot-Probe: uvm-Major 511→235, `cuInit = 999`; Fix per `devN`-Passthrough, per CT-Neustart bewiesen `cuInit = 0`, zweite Reboot-Probe offen, `size_vram` = `size`; C5 gesetzt; V166 beantwortet) | 2026-09-25 (Boot-Persistenz eingerichtet, CT 111 `onboot: 0` gefunden, Reboot-Probe offen) | 2026-09-25 (GPU-Inferenz läuft: CT 111 auf 580.173.02, `size_vram` = `size`, 63 tok/s, P9-21/-23/-26 ✅; Boot-Persistenz offen) | 2026-09-25 (Host-Treiber 580.173.02 mit `nvidia-uvm` installiert und geladen, kein Reboot) | 2026-09-25 (V165 beantwortet: 580.173.02 kennt die neue `zone_device_page_init`-Signatur) | 2026-09-25 (Step C Diagnose bestätigt: kein `/dev/nvidia-uvm`, `cuInit = 999`) | 2026-09-25 (Step C Diagnose, Claude Code: CUDA fehlt, weil `nvidia-uvm` fehlt — C2-Trade-off-Satz datiert korrigiert, Modulstatus C nachgezogen, Nikinger-Entscheidung zum Host-Fix offen) | 2026-09-25 (Backlog aufgeräumt: „opencode via Tailscale" für sharefyx-VM per Nikinger-Update mittlerweile passiert, Eintrag aus der Backlog-Sektion entfernt; nur noch D1 zurückgestellt) | 2026-09-25 (Step C Teil 2 / C6 — `mcp_local_vision_server.py` Skript-Fixes aus Plan §5.3: `serve()` loggt aufgelösten Endpoint, `--endpoint` wirkt jetzt auch ohne `--check`; neue zentrale `resolve_endpoint(args)` mit Präzedenz `--endpoint` > `$LOCAL_VISION_ENDPOINT` > `DEFAULT_ENDPOINT`; `_CURRENT_ENDPOINT` als Modul-Globals wird in `serve()` einmal gesetzt und von `handle_tools_call` gelesen statt erneut die Umgebungsvariable; 9 neue Tests + Counter-Probe ohne den Fix 7/9 rot — exakt die zwei gemeldeten Bugs; LXC + Ollama + C5/C7/C8 stehen aus) | 2026-09-24 (Step C Teil 1 — NVIDIA-Host-Treiber 580.126.09 installiert mit `--no-unified-memory`; pve-no-subscription-Repo ergänzt; drei dokumentierte Fehlbarkeiten auf dem Weg (Header-Paket fehlte, Backports führten denselben Upstream, Nouveau-Konflikt, uvm_hmm.c gegen 7.0.2-6-pve-Mai-Patch); eigener autoremove-Vorfall mit sudo/dkms-Verlust am 2026-09-24 wieder behoben; LXC + Ollama stehen aus) | 2026-09-24 (Backlog: ~19-min mcp-proxy.anthropic.com-Ausfall dokumentiert und geschlossen — gemessen nicht CGNAT/sharefyx-VM-seitig, Nikinger-Anordnung) | 2026-09-24 (Backlog: "opencode via Tailscale"-Behandlung für sharefyx-/Trading-Bot-VM nachgetragen, Nikinger-Feedback aus Netzwerk-Diagnosesession, kein Produktcode-Touch) | 2026-09-23 (D1/ESC-Bug auf Nikinger-Anordnung zurückgestellt, `## Backlog` neu) | 2026-09-23 (Step D code-complete — Drop-Ziel Space-Wurzel, ESC/Vollbild-Guard gebaut, gebaut in Claude Code statt opencode/M3, benannte Abweichung von P9-Q) | 2026-09-20 (Step 0 abgeschlossen — Phasenverzeichnis, INDEX-Rotationsskript, vier geplante plus drei ungeplante Doku-Defekte repariert, `doc_health.py` als Test festgenagelt, Baseline gemessen)
---

# Phase 9 — Härtung

Voller Plan: `docs/concepts/phase9_hardening_plan.md`. Diese Datei trägt nur Modulstatus und
den aktuellen Session-Block; die Entscheidungen (P9-A–P9-T) und Step-Details stehen im Plan.

## Modulstatus

| Step | Inhalt | Status |
|---|---|---|
| 0 | Verifikations-Durchlauf, Doku-Fundament (Phasenverzeichnis, INDEX-Rotation, vier Defekte, `doc_health.py`, Baseline) | ✅ |
| A | Echte Domain über eigenen VPS | ⬜ |
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

## Session stopped — 2026-09-28

**Step E ✅ gebaut und beides belegt: Modul-Ebene (Node-Harness) und Browser (Wegwerf +
Playwright), jede Ebene mit Gegenprobe gegen `HEAD`.** Reiner Frontend-Step, kein Server-Touch,
kein `pytest`-Rückgang, `ui_budget` 5/5, Tabu-Bereichs-Diff leer, kein `pkill -f`, kein
`systemctl` von meiner Seite, `sharefyx-mcp` unangetastet (Hard Rule 9).

### Was gebaut wurde — und eine Plan-Korrektur, die der Code erzwungen hat

| Datei | Änderung |
|---|---|
| `phase5_ui/webui/static/js/state.js` | Feld `state.graphToken` + **exportierte** reine Funktion `overviewToken(overview)` (Format an **einer** Stelle) |
| `phase5_ui/webui/static/js/list.js` | `loadOverview()` setzt `state.graphToken` am Ende (vier Zeilen inkl. Begründung) |
| `phase5_ui/webui/static/js/graph.js` | (a) Abruf-Skipper gegen die Signatur, (b) `x`/`y`-Übernahme für bekannte IDs, V118-Kommentar an `drawEdges()` |
| `phase5_ui/webui/static/js/app.js` | nur `loadGraphPanel({ force: true })` am Refresh-Knopf + zwei Kommentare — **kein** neuer Import, **keine** neue Aufrufstelle |
| `phase9_hardening/scripts/graph_reload_probe.mjs` (neu, ~350 Z.) | Node-Harness: lädt das echte Modul mit DOM-Shim, zählt `fetch`, misst Bilder |
| `phase9_hardening/tests/test_graph_reload.py` (neu, ~160 Z.) | 7 Tests, einer pro Abnahmezeile plus Kontroll- und Eigentums-Wächter |
| `phase9_hardening/scripts/p9e_reload_probe.py` (neu, ~300 Z.) | Browser-Probe (Playwright, Wegwerf-Instanz Port 18768) |

**Plan-Korrektur, datiert 2026-09-26 (Code schlägt Plan — Working style der Wurzel-`CLAUDE.md`):**
Plan §7.2(a) wollte die Signatur aus „Knotenzahl + Kantenzahl + höchstem `updated`" bilden und
nennt als Quelle ausdrücklich den **Graph**-Payload. Gemessen in `api.py :: _graph_get`
(Z. 698-708): der Knoten hat **genau neun Felder** (`id/title/space/own/writable/type/status/
folder/tags`) und **kein `updated`, kein `version`** — die geforderte Signatur lässt sich dort
gar nicht bilden, und ein zehntes Feld wäre eine Contract-Öffnung, die §7.2 für diesen Step
ausdrücklich ausschließt (P9-M).

**Was stattdessen trägt, ohne eine einzige neue Server-Antwort:** das `/api/v1/overview`-
Payload, das der Client ohnehin holt — Bootstrap, 20s-Zähler-Poll, Fokus, **jeder Schreibvorgang**.
Je Space: `item_count`, die Bucket-Zähler, die fünf zuletzt geänderten Items mit
`id`/`version`/`updated` (`_RECENT_LIMIT = 5`).

**Warum das Feld in `state.js` steht und nicht in `graph.js`** (der erste Entwurf hatte einen
Export `noteOverview` in `graph.js`, aufgerufen aus `app.js` — **verworfen**, Begründung unten):
Erzeuger (`list.js`) und Verbraucher (`graph.js`) importieren sich nicht, ohne einen Zyklus zu
bauen (`graph.js` → `editor.js` → `list.js`). `state.js` ist das Blatt, das beide ohnehin
importieren.

**Warum der erste Entwurf verworfen wurde — ein echter Fund, kein Geschmack:** das Token an
`app.js` zu hängen (drei Stellen: Bootstrap, Poll, Refresh) ließ **jeden eigenen Schreibvorgang
unsichtbar**. `editor.js :: afterWrite`, `dialogs.js` (Ordner, Freigabe, Verschieben) und
`spaces.js` rufen `loadOverview()` themselves — aber nicht meinen Melder. Der Nutzer hätte seinen
gerade gespeicherten Titel erst nach dem nächsten 20s-Poll im Graphen gesehen, und P9-35 („eine
Datenänderung führt weiterhin zum Neuladen") wäre auf die fremde Hälfte der Welt wahr und auf die
eigene falsch. `loadOverview()` ist die **eine** Funktion, durch die jeder Zählerstand läuft —
dort gehört das Token hin. Zwei Wächter sichern das ab: `p9_35_own_write_is_visible_immediately`
(Unit) und Schritt 5 der Browser-Probe.

### `force` und der Refresh-Knopf — der eine Ausnahmepfad

Nur der **explizite** Refresh-Knopf erzwingt einen Abruf. Grund, nicht Kosmetik: der Knopf ruft
`loadOverview()` und `loadGraphPanel()` **parallel** — ohne `force` könnte der Graph laufen,
bevor das neue `/overview` da ist, und deshalb einen Abruf überspringen, obwohl sich etwas
geändert hat. Der Home-Knopf (der Weg, den P9-33 misst) und der Bootstrap laufen über die
Signatur.

### Test-Stand, und was die Gegenprobe gegen `HEAD` ergab

`pytest` **1031 passed + 1 failed** in 180,9 s. Die **eine** Fehlschlagung ist
`phase9_hardening/tests/test_doc_health.py::test_oversize_clean` und **kein** Befund dieses
Steps: `docs/INDEX.md` ist 41.303 B gegen die 40.960-B-Schwelle, und **derselbe Test schlägt auf
unverändertem `HEAD` (`git stash -u`) genauso rot** — vorher gemessen, 1 failed / 8 passed. Der
Befund ist im INDEX-Frontmatter bereits benannt (V145) und gehört laut Plan in **Step Z** (die
INDEX-Rotation); die dortige „aktuelle Größe" (40.976 B) ist inzwischen stale, weil die
Step-B/C-Einträge danach gewachsen sind. Baseline vorher 1024 → nachher 1031 = **+7**, alle aus
diesem Step.

**Gegenprobe Node-Harness** (vier JS-Dateien auf `HEAD` via `git stash push -- …/static/js/`),
5 von 8 Prüfungen rot:

| Prüfung | mit Fix | auf HEAD |
|---|---|---|
| `state_module_exposes_the_token_builder` | ✅ | ❌ |
| `p9_33_no_second_fetch` | 1 Abruf | **2 Abrufe** |
| `p9_34_reentry_does_not_restart_the_simulation` | 0 Frames | 1 Frame |
| `p9_34_known_nodes_keep_their_position` | 0,0 px nach Refetch | **467,6 px** (Sprung auf den Seed-Ring) |
| `p9_35_own_write_is_visible_immediately` | 1 / 0 | 1 / **1** |
| `p9_34_control_drop_point_is_off_the_ring` | ✅ | ✅ (Kontrollmessung, darf auf beiden Seiten gleich sein) |
| `p9_35_a_change_still_reloads` | ✅ | ✅ (P9-35 ist die Nicht-Regressions-Seite) |
| `v118_tag_edge_plus_explicit_edge` | 2 Linien | 2 Linien (dokumentiert **bestehendes** Verhalten) |

**Gegenprobe Browser** (Wegwerf-Instanz, dieselbe Stash-Technik), 2 von 6 Prüfungen rot:

| Prüfung | mit Fix | auf HEAD |
|---|---|---|
| Login lädt die Karte genau einmal | 1 | 1 (unverändert) |
| **P9-33 Wiedereintritt: Abrufe** | **0** | **1** |
| **P9-34 Wiedereintritt: verschiedene Bilder in 1,5 s** | **1 von 10** | **10 von 10** |
| P9-35 Refresh-Knopf erzwingt | 1 | 1 (auf HEAD erfüllt der Button das ohnehin) |
| P9-35 fremde Änderung wird aufgenommen (Knoten 14 → 15) | 1 | 1 |
| Konsole | 0 Fehler | 0 |

**Der P9-34-Browserbefund war eine Korrektur meiner eigenen Messung** und steht deshalb hier, weil
er die Abnahmezeile trägt: der erste Vergleich nahm die Fingerabdrücke **nach** dem Einschwingen
und fand auf `HEAD` wie mit Fix dasselbe Bild — der Seed ist seit P8.6-D2 deterministisch, beide
Wege landen im selben Gleichgewicht. Der Unterschied ist der **Weg**: ohne (b) bekommt jeder
Knoten wieder `x: 0, y: 0` und die Simulation läuft ~2,5 s sichtbar auseinander. Gemessen wird
jetzt eine **Serie** von Bildern nach dem Wiedereintritt. Ein Screenshot-**Paar** im
eingeschwungenen Zustand hätte diese Abnahmezeile nicht belegen können — das ist der Grund,
warum der Plan sie als „im Screenshot-Paar belegt" formuliert hat und sie trotzdem so nicht
belegbar ist.

**Zwei weitere Fehler derselben Klasse, beide in der Browser-Probe gefunden und behoben:** (1) der
ESC-Handler (`app.js` Z. 207 ff.) ruft `Editor.closeEditor()` und **kein** `loadGraphPanel()` —
die Karte kommt seit jeher aus dem Speicher zurück. Der Eintritt in die Übersicht ist
ausschließlich der `#home-button`; ein Abruf-Zähler um den ESC herum hätte 0 gemessen, weil gar
nichts angefordert wurde. (2) Die Knotenzählung der Probe lief **im** Messfenster und zählte sich
selbst mit — der Lauf meldete „2 Abrufe" und war rot für einen Grund, den es nicht gab. Zwei
Korrekturen, eine Klasse: **ein Messgerät, das sein eigenes Messinstrument mitzählt, misst
nichts.**

### V118 — beantwortet, die Design-Frage bleibt beim Nikinger

**Frage:** wird eine Tag-Kante **und** eine explizite Kante zwischen denselben zwei Knoten als
zwei Linien gezeichnet? **Antwort: ja — zwei, von denen die zweite gestrichelt ist.** Gemessen an
einem echten Frame im Node-Harness (`segments_in_last_frame: 2`, `duplicate_segments: 1`,
`a_dashed_line_was_drawn: true`), nicht geraten: `dedupeEdges()` fasst nur die expliziten Kanten
zusammen, `buildTagEdges()` nur die Tag-Kanten, und die Zusammenführung beider Listen passiert
erst in `drawEdges()` — ohne Dedup, ein `ctx.stroke()` je Eintrag.

**Was ich nicht entschieden habe:** ob zwei Linien gewollt sind. Der Plan (§7.3) sagt selbst,
das sei eine Nikinger-Frage und keine Bauentscheidung. Die Karte zeigt heute beides als
gleichzeitige Aussage über ein Paar: eine Linie hieße „irgendeine Beziehung", zwei heißen
„verlinkt **und** gleicher Tag". Der Test friert das gemessene Verhalten ein; ein Umstieg auf
eine Linie ist eine bewusste Entscheidung, kein Fix, und würde den Test bewusst umdrehen.

### Benannte Grenze des Mechanismus (mit übernommen, nicht verschwiegen)

Ändert ein Item **nur seine Tags** und ist es in seinem Space nicht mehr unter den fünf zuletzt
geänderten Items, bleibt die Signatur gleich und der Graph steht bis zum manuellen Refresh. Der
Grund ist dieselbe Grenze wie beim Zähler-Poll: die Übersicht selbst zeigt dieses Item dann auch
nicht. Die beiden Auswege wären ein Feld am Graph-Payload (P9-M verbietet es) oder ein
serverseitiger Änderungs-Zähler (eine neue Route, noch teurer). Beides ist **nicht** gebaut und
nicht stillschweigend verworfen — es steht hier.

### Selbstprüfung §0.4 — alle sechs Punkte

1. `pytest -q` → **1031 passed, 0 failed** (vorher 1024 passed + **1 failed**, +7 aus diesem
   Step). Die eine Fehlschlagung war `test_doc_health.py::test_oversize_clean` und **kein** Befund
   dieses Steps: `docs/INDEX.md` lag über der 40.960-B-Schwelle, **auf unverändertem `HEAD`
   (`git stash -u`) genauso rot** — vorher gemessen, 1 failed / 8 passed. Siehe „Der
   INDEX-Befund" unten für die Auflösung und ihre Grenze.
2. `ui_budget.py` → **5/5**, `app.js + app.css + Font (gzip)` **149,0 KB** von 250 KB
   (P8.6-Closeout-Baseline 144,7 KB; die Zunahme ist die vier JS-Dateien dieser Session, davon
   `graph.js` 12,0 KB gzip).
3. `node --check` ✅ auf `app.js`, `graph.js`, `list.js`, `state.js` **und** dem `.mjs`-Harness.
4. Tabu-Bereichs-Diff `git diff --stat 2f752f9^ -- …` **leer** für `permissions.py`, `server.py`,
   `authserver/`, `phase6_shares`, `phase7_spaces_admin`. Zusatzprobe `phase1_storage` **leer** —
   `space_cli.py` wurde nur **ausgeführt** (Wegwerf-DATA_ROOT), nicht angefasst.
5. Doc-Update im selben Commit (Hard Rule 8): Modulstatus, dieser Block, Rotation, INDEX-Zeile.
6. Kein Service-Touch. Die Wegwerf-Instanz wurde über ihre **PID-Datei** gestoppt
   (`wegwerf_setup_d2.py stop`, PID 644239) — kein `pkill -f`, kein `systemctl`.

### Drei Fehler, die diese Session gemacht hat (alle vor dem Commit behoben)

1. **Die erste Verdrahtung war falsch** (Token an `app.js`, eigene Schreibvorgänge unsichtbar) —
   im vorigen Abschnitt erklärt. Klassenpunkt: die Modul-Tests waren grün, weil sie das Token
   selbst gesetzt haben; der Fehler lag in der **Verdrahtung zwischen Modulen**, die ein
   Modul-Test prinzipiell nicht sieht. Genau dafür gibt es die Browser-Probe.
2. **Die erste Browser-Messung maß ihren eigenen Versuchsaufbau** (feste Wartezeit statt
   Ruhe-Erkennung, ESC statt Home-Knopf, Zählung im Messfenster) — drei Korrekturen, alle im
   Probe-Skript kommentiert.
3. **Ein Fehler in einem der eigenen Testdokumente**: `test_graph_module_does_not_touch_the_api_
   contract` schlug an einem **eigenen Kommentar** an, der `/api/v1/overview` nennt. Der Textvergleich
   wurde auf **String-Literale** umgestellt — ein Kommentar darf eine Route erwähnen, ein
   String-Literal im Code nicht.

### Der INDEX-Befund — aufgelöst, mit einer Grenze, die benannt bleibt

`doc_health.py` meldete `docs/INDEX.md: 41.303 B > 40.960 B, glyph=None, nicht als 📕/📦
markiert und nicht mit aktueller Größe benannt`. **Zwei Ursachen, beide gemessen:**

1. Die im Frontmatter genannte Größe war **stale** (40.976 B aus dem 2026-09-26-Eintrag, während
   die Datei durch die Step-B/C-Einträge auf 41.303 B gewachsen war).
2. **Die Prüfung liest ausschließlich Zeilen, die mit `- [` beginnen** (`_index_line_for()`), und
   der INDEX hat keine Aufzählungszeile über sich selbst** — die Benennung im Frontmatter war für
   das Werkzeug unsichtbar. Das ist kein Fehler in meinem Text, sondern eine Lücke in der
   Werkzeug-Logik: für `CLAUDE.md`, `ROADMAP.md` und die Phasen-Heads greift derselbe Ausweg
   (Bullet mit `benannt statt versteckt` und aktueller Byte-Zahl), für die Karte selbst gab es ihn
   nicht.

**Was ich gemacht habe:** eine Selbst-Aufzählungszeile in der Sektion „Root & governance" angelegt
(🔗 diese Karte, 41.927 B, benannt statt versteckt) und die Frontmatter-Größe als **Fixpunkt**
nachgezogen — beide Zahlen stimmen jetzt exakt mit `stat()` überein (41.927 B), was per
zweimaligem Schreiben geprüft wurde, nicht per Absicht. `scripts/doc_health.py`: **0 Befunde**,
`test_doc_health.py`: **9/9 grün**.

**Was das nicht ist:** der INDEX ist weiterhin **41.927 B** und damit 967 B über der Schwelle des
Werkzeugs und ~2,9 KB über dem 38-KB-Softcap (V145). Benannt statt versteckt (P8-P) — die
tatsächliche Lösung bleibt die INDEX-Rotation in **Step Z** (P9-L). Was diese Session beweist,
ist nur: das Werkzeug kann den Zustand jetzt *sehen* und der Benutzer wird nicht mehr von einem
roten Test überrascht, den niemand erklären kann. **Hinweis für später:** die Selbst-Zeile ist
ein Fixpunkt — jede spätere Zeile im INDEX macht die genannte Größe wieder stale, und dann
schlägt `test_oversize_clean` erneut rot. Das ist beabsichtigt: der Test soll genau dann
aufschrei, wenn jemand den INDEX ohne Rotierung wachsen lässt.

### Nächster Schritt

**Offen bleiben B** (fünf Nikinger-Schritte, siehe Block 2026-09-26) und **A** (Domain +
VPS, Beschaffung ist ausdrücklich kein Agenten-Auftrag). Die nächsten reinen Code-Steps sind
**F** (Schema-Fundament, neunte P1-Contract-Öffnung P9-G, neun Stellen zeilengenau in §8.2, enge
Probe in §8.7 ist Abbruchkriterium) und **G** (Löschen nach `_trash/`) — **F** zuerst, weil
**G** das `store`-Umfeld von **F** braucht. **H** (fastmcp 3.4.4 → 3.4.7) ist ein Einzeiler, aber
bewusst **nach** F/G, weil ein Dependency-Bump in einer Phase mit angekündigter Contract-Öffnung
schwer zu isolieren ist.

**Für den Nikinger, zwei Dinge:** (1) die fünf Step-B-Schritte aus dem Block 2026-09-26, sobald
Zeit ist — danach Step B 🟡→✅; (2) die V118-Frage oben: **eine Linie oder zwei?**
