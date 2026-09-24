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
updated: 2026-09-24 (Backlog: ~19-min mcp-proxy.anthropic.com-Ausfall dokumentiert und geschlossen — gemessen nicht CGNAT/sharefyx-VM-seitig, Nikinger-Anordnung) | 2026-09-24 (Backlog: "opencode via Tailscale"-Behandlung für sharefyx-/Trading-Bot-VM nachgetragen, Nikinger-Feedback aus Netzwerk-Diagnosesession, kein Produktcode-Touch) | 2026-09-23 (D1/ESC-Bug auf Nikinger-Anordnung zurückgestellt, `## Backlog` neu) | 2026-09-23 (Step D code-complete — Drop-Ziel Space-Wurzel, ESC/Vollbild-Guard gebaut, gebaut in Claude Code statt opencode/M3, benannte Abweichung von P9-Q) | 2026-09-20 (Step 0 abgeschlossen — Phasenverzeichnis, INDEX-Rotationsskript, vier geplante plus drei ungeplante Doku-Defekte repariert, `doc_health.py` als Test festgenagelt, Baseline gemessen)
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
| C | Vision-Dienst auf der RTX 3060 | ⬜ |
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
