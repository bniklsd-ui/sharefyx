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
updated: 2026-09-25 (Step C Teil 2 / C6 — `mcp_local_vision_server.py` Skript-Fixes aus Plan §5.3: `serve()` loggt aufgelösten Endpoint, `--endpoint` wirkt jetzt auch ohne `--check`; neue zentrale `resolve_endpoint(args)` mit Präzedenz `--endpoint` > `$LOCAL_VISION_ENDPOINT` > `DEFAULT_ENDPOINT`; `_CURRENT_ENDPOINT` als Modul-Globals wird in `serve()` einmal gesetzt und von `handle_tools_call` gelesen statt erneut die Umgebungsvariable; 9 neue Tests + Counter-Probe ohne den Fix 7/9 rot — exakt die zwei gemeldeten Bugs; LXC + Ollama + C5/C7/C8 stehen aus) | 2026-09-24 (Step C Teil 1 — NVIDIA-Host-Treiber 580.126.09 installiert mit `--no-unified-memory`; pve-no-subscription-Repo ergänzt; drei dokumentierte Fehlbarkeiten auf dem Weg (Header-Paket fehlte, Backports führten denselben Upstream, Nouveau-Konflikt, uvm_hmm.c gegen 7.0.2-6-pve-Mai-Patch); eigener autoremove-Vorfall mit sudo/dkms-Verlust am 2026-09-24 wieder behoben; LXC + Ollama stehen aus) | 2026-09-24 (Backlog: ~19-min mcp-proxy.anthropic.com-Ausfall dokumentiert und geschlossen — gemessen nicht CGNAT/sharefyx-VM-seitig, Nikinger-Anordnung) | 2026-09-24 (Backlog: "opencode via Tailscale"-Behandlung für sharefyx-/Trading-Bot-VM nachgetragen, Nikinger-Feedback aus Netzwerk-Diagnosesession, kein Produktcode-Touch) | 2026-09-23 (D1/ESC-Bug auf Nikinger-Anordnung zurückgestellt, `## Backlog` neu) | 2026-09-23 (Step D code-complete — Drop-Ziel Space-Wurzel, ESC/Vollbild-Guard gebaut, gebaut in Claude Code statt opencode/M3, benannte Abweichung von P9-Q) | 2026-09-20 (Step 0 abgeschlossen — Phasenverzeichnis, INDEX-Rotationsskript, vier geplante plus drei ungeplante Doku-Defekte repariert, `doc_health.py` als Test festgenagelt, Baseline gemessen)
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
| C | Vision-Dienst auf der RTX 3060 | 🟡 Host-Treiber (580.126.09) installiert mit `--no-unified-memory` (UVM-Trade-off akzeptiert, reversibel) ✅; **C6 Skript-Fixes aus Plan §5.3 ✅** (aufgelöster Endpoint im Startup-Log, `--endpoint` wirkt auch im Server-Modus); LXC-Anlage, cgroup-Devices, Ollama + `qwen3-vl:8b`-Pull, Cold-Start-Messung (C7) und CPU-Ollama-Abbau-Entscheidung (C8) stehen aus |
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

