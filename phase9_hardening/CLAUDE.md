---
status: live
purpose: Phase-9-Head — Härtungsphase (Domain, Watchdog, Vision-Dienst, Doku-Rotation, zwei Bugs, Karten-Reload, neunte P1-Contract-Öffnung, `_trash/`-Löschen), Modulstatus, aktueller Session-Handover
read-when: Arbeiten in phase9_hardening/ — zuerst lesen, zusammen mit dem neuesten Session-stopped-Block
detail: L2
up: ../CLAUDE.md
down:
  - ../docs/concepts/phase9_hardening_plan.md    # voller Plan, Locks P9-A–P9-T, Steps 0–H
  - ../docs/concepts/phase9_hardening_block_doing_plan.md  # Mini-Plan doing-Block, Locks P9-V–P9-X
  - ../docs/concepts/PHASE8_6_CLOSEOUT_HANDOVER.md  # Herkunft der P9-Punkte
  - ABNAHME_MATRIX.md                            # P9-1 – P9-82 mit Stand und Beleg + [VERIFY]-Bilanz (2026-10-03)
  - SESSIONS_ARCHIVE.md                          # ältere Session-Blöcke, newest-first
  - UPDATES_ARCHIVE.md                          # ältere `updated:`-Fäden dieses Heads, verbatim (2026-10-03, 36 von 37)
  - MODULE_STATUS_ARCHIVE.md                   # ausführliche Statusspalten der §-Modulstatus-Tabelle, verbatim (2026-10-04)
updated: 2026-10-05 (**Block settings gebaut, opencode/M3 — drei Overlays sind eine Fensterkette, V118 hat eine Linie**; Release `v3.1.3` steht, **kein Deploy, kein Service-Touch**; `pytest` 1223 → 1233, `ui_budget` 5/5, Tabu-Diff leer, Probe **39/39**, G1 → 4 rot · G2 → 2 rot · G3 → rot · **zwei Code-Befunde aus dem Browser, nicht aus den Tests** (Schmal-Modus ließ zwei Panels stehen · der „Zurück“-Knopf des Details war nicht verdrahtet) · **der Gegenlauf hat den eigenen Messaufbaum widerlegt** (er las den Frame nach dem Toggle-Zurückschalten — mit dem Fix wäre der Test grün gewesen) · P9-94 ⬜ Portscan, V188 ⬜) | 2026-10-05 (Block 2026-10-04 aus dem Head verbatim hierher rotiert, per `scripts/rotate_session_block.sh`)
---

# Phase 9 — Härtung

Voller Plan: `docs/concepts/phase9_hardening_plan.md`. Diese Datei trägt nur Modulstatus und
den aktuellen Session-Block; die Entscheidungen (P9-A–P9-T) und Step-Details stehen im Plan.

## Modulstatus

| Step | Inhalt | Status |
|---|---|---|
| 0 | Verifikations-Durchlauf, Doku-Fundament (Phasenverzeichnis, INDEX-Rotation, vier Defekte, `doc_health.py`, Baseline) | ✅ (Details im L3-Archiv) · Herleitung im L3-Archiv |
| A | Echte Domain über eigenen VPS | 🟡 **A7a + A7 ✅ 2026-10-03; A8 für Konto *niklas* ✅** — P9-10b ✅ · P9-12 ✅ · P9-14 ✅ · **P9-13/V150 ⬜ zurückgestellt, wandert nach P10, ist kein Blocker** (Nikinger 2026-10-04: ein Schritt, der nur ein Konto braucht, ist ein Termin, kein Blocker; Plan §0.1a) · **P9-15 ⬜ = Arbeit der nächsten Session** (drei Läufe `/api/v1/overview` mit echter UI-Session). Übergangsfenster **unbefristet, live seit 2026-10-05** (`v3.1.2`, `LEGACY_UNTIL=open`, Nikinger-Entscheidung: Firmen-Proxy setzt die neue Domain zurück) · Herleitung im L3-Archiv |
| B | `tailscaled-watchdog.service` | ✅ **abgeschlossen 2026-10-01**, live; P9-16–P9-20 ✅, V152/V153 ✅. `socat` 1.8.0.0 + Unit laufen unter voller Härtung, `RuntimeDirectoryPreserve=yes` (Befund 7) und Systempfad (Befund `__REPO_ROOT__`) behoben · V153: `sudoers` unbaubar, polkit greift · Herleitung im L3-Archiv |
| C | Vision-Dienst auf der RTX 3060 | ✅ **abgeschlossen** (2026-09-26): GPU-Inferenz reboot-fest + C8 (`ollama` auf der VM `inactive`) · P9-21/-23/-26 ✅ · **P9-22 deferred** (Nikinger 2026-09-26, architektonisch belegt statt extern getestet) → Revisit Step Z oder P10 · Herleitung im L3-Archiv |
| D | Zwei gemeldete Bugs (ESC/Vollbild, Drop-Ziel Space-Wurzel) | 🟡 **D2 am Browser belegt 2026-10-03** (P9-28/-29/-30 ✅, Probe **16/16**); **D1 bewusst zurückgestellt** (Nikinger 2026-09-23) · **P9-27 ⬜** und bleibt es: natives macOS-Vollbild ist nicht automatisierbar, der `fullscreenElement`-Guard ist dafür ein No-op · Herleitung im L3-Archiv |
| E | Karte: Reload-Overload, V118 | ✅ **abgeschlossen** (2026-09-28): kein zweiter `/graph`-Abruf, bekannte Knoten behalten `x`/`y`, `force` nur am Refresh-Knopf · P9-33/-34/-35 ✅ · V118 beantwortet · die Design-Frage P9-36 („eine oder zwei Linien") liegt beim Nikinger · Herleitung im L3-Archiv |
| F | Schema-Fundament (neunte P1-Contract-Öffnung: `doing`/`assignee`) | 🟡 **code-complete 2026-09-30, live seit 2026-10-02** (`v3.1.0`) · P9-43 ✅ (≤ 1,05 s für 197 Items) · **der `doing`-Bereich ist seit 2026-10-02 geschlossen** (Lock P9-V) ⇒ **P9-P ist datiert eingeengt, nicht erledigt**: die prominente Darstellung bleibt P10 · P9-U (Space-Name, ohne Validierung) und P9-V stehen im Plan · Herleitung im L3-Archiv |
| G | Löschen (F2) nach `_trash/` | 🟡 **code-complete 2026-09-30, deployt 2026-10-02** (`v3.1.0`); **Live-Löschung noch nicht beobachtet** ⇒ V162 *(Lesart A)* ⬜ · der Lösch-Ort aus Plan §9.3 war unbaubar, Nikinger entschied `DATA_ROOT/._trash/<space>/` mit **null** P1-Änderungen · Herleitung im L3-Archiv |
| H | Abhängigkeits-Hygiene | 🟡 **code-complete 2026-09-30** · `fastmcp` **exakt** auf `3.4.7` gepinnt (P3-D/P4-R waren seit 2026-08 beschlossen und nie umgesetzt) · V163 ✅ (inert) · P9-55 ⚠️ in der Form (`==3.4.7` statt Range, Nikinger 2026-09-30) · **benannt, nicht gebaut:** das transitive `mcp` bleibt ungepinnt (P9-Backlog-Kandidat) · Herleitung im L3-Archiv |
| doing | Fünfter Eimer „In Arbeit" (Lock **P9-V**, Kandidat (a)) — Voraussetzung für den Deploy `v3.1.0` | ✅ **live seit 2026-10-02** (`v3.1.0`, Gate 9/9) · Locks P9-V/W/X · 6 Tests, Gegenlauf 7 rot, Browser 11/11 · Release-Commit `v3.1.1` **2026-10-03** · Herleitung im L3-Archiv |
| trace | Nachvollziehbarkeit: `assignee` sichtbar (UI + MCP, vom Client gefüllt, P9-Z) + `updated_by` + Git-Autor (P9-AA–AC); **zehnte P1-Contract-Öffnung** | 🟡 **code-complete 2026-10-02, seit 2026-10-03 live** (`v3.1.1`, Release `20261003T205843`, Gate 9/9) · Locks P9-Y–AD · **zehnte P1-Contract-Öffnung ohne Index-Schema-Sprung** ⇒ beim Deploy **kein** Neuaufbau (am Journal bestätigt) · 24 Tests, Browser 8/8 mit Zwei-Principalen-Instanz · Herleitung im L3-Archiv |
| E (Extra) | **Buttons ans Schema** (B17): die Knöpfe mit eigenen Flächen auf die Standard-Tokens `--btn-std-*` umstellen | ✅ **gebaut 2026-10-02 (B17), seit 2026-10-03 live** · die Backlog-Liste war an zwei Stellen falsch (15 statt 1 Knopf auf der alten Flächenfamilie) · `.btn.action--caution` trägt jetzt **exakt** die Standardfläche, nur die Beschriftung ist rot · Kontrast **4,38:1** bleibt unter WCAG-AA — **Design-Entscheidung, deine** · Herleitung im L3-Archiv |
| S | **Einstellungen als Fensterkette** + V118 eine Linie (Nikinger 2026-10-05) | 🟡 **gebaut 2026-10-05 (M3)**, Release `v3.1.3` steht, **nicht deployt** — `docs/concepts/phase9_hardening_block_settings_plan.md` (Locks P9-AE–AL, Abnahme P9-83–95) · **drei Overlays wurden eine Kette** (`#settings-overlay`, fünf Panels), **ein** Öffner (`settings.js` + `registerPanel`), Menüknöpfe tragen `.tree__folder` statt einer eigenen Optik · **zwei echte Befunde aus dem Browser, nicht aus dem Test**: der Schmal-Modus ließ bei offenem Detail **zwei** Panels stehen (zwei `:has()`-Regeln statt einer), und der „Zurück"-Knopf des Details war **nicht verdrahtet** (im breiten Modus unauffällig) · **V118 umgedreht**: der Test hieß `…_draw_two_lines` und heißt jetzt `test_a_tag_edge_beside_an_explicit_edge_draws_one_line`, Docstring mit beiden Lesarten und Datum · **Probe 39/39**, G1 → 4 rot, G2 → 2 rot, G3 → rot, **der Gegenlauf hat den eigenen Messaufbaum widerlegt** (er las den Frame *nach* dem Toggle-Zurückschalten) · `pytest` 1223 → 1233, `ui_budget` 5/5, Tabu-Diff leer · **P9-94 ⬜** (Portscan, Nikinger-Schritt) · Herleitung im L3-Archiv |
| Gate/Z | Abnahme, Closeout | 🟡 **beide Doku-Hälften erledigt** (2026-10-02) · `ABNAHME_MATRIX.md` ist der **eine** Ort der Abnahme- und `[VERIFY]`-Bilanz, nicht diese Zeile · **[2026-10-04] beide Rotationen gefahren** (Block 17.780 B verbatim, Kette 6 von 7 Fäden) und diese Tabelle ins L3-Archiv gezogen ⇒ **der Head ist unter dem 40-KiB-Softcap** · **offen:** zweites Claude-Konto (P9-13/V150) · P9-15 ⬜ · Übersichtsgrafik §12.4 · Phase auf ✅ · Herleitung im L3-Archiv |

## Backlog (bewusst zurückgestellt, kein Phasen-Blocker)

- **B17 — ✅ GESCHLOSSEN am 2026-10-02** (war: „potentieller Extra-Schritt", in der Modulstatus-Tabelle
  als „E (Extra)" geführt). **Alle Knöpfe tragen jetzt eine Fläche aus einem Schema, und die zwei
  verbleibenden Ausnahmen sind je eine Klasse mit eigener Bedeutung.** Die Details, die Messungen und
  der Gegenlauf stehen in der Modulstatus-Zeile und im Session-Block 2026-10-02; hier bleiben die
  drei Punkte, die ein späterer Leser sonst falsch wüsste:
  1. **Die Liste dieses Eintrags war an zwei Stellen falsch** — sie nannte 15 Knöpfe und
     „`.btn.action--caution` (2 Knöpfe)". Richtig sind **1 Knopf** auf der alten Familie
     (`#archive-button`; der zweite Träger `#logout-button` ist ein `.rail__action` und hat keine
     Fläche) und **13** auf `--accent-face-*` (`.btn-primary`). Die 13 sind **kein Reststand**:
     Hauptaktion ist eine dokumentierte Ausnahme der Nikinger-Entscheidung vom 2026-10-01.
  2. **`.btn.action--caution` trägt exakt die Standardfläche**, nur die Beschriftung ist rot
     (`--caution`). Das ist wortgleich die Konvention-v3-Zeile „Standard-Knopfplastik, aber
     `color: var(--caution)`; **keine** gefüllte rote Fläche" — und die Konvention war zwischen
     dem 2026-10-01 und dem 2026-10-02 **nicht eingehalten** (die alte graue Fläche ist heller als
     die Standardfläche). Beide Stellen in `phase8_ui_graph/CLAUDE.md` sind datiert korrigiert.
  3. **Benannt, nicht entschieden:** der Kontrast der Vorsicht-Beschriftung liegt bei
     **4,38:1** (vorher 3,36:1 auf der grauen Plastik) — **unter** WCAG-AA 4,5:1 für normalgroßen
     Text (14 px/500 ist kein „large text"). Besser als vorher ist das keine Erfüllung. Die
     Kandidaten (hellere Vorschriftfarbe wie `--btn-std-line` als Text, oder die Kategorie doch an
     eine 1-px-Kante hängen) sind Design-Entscheidungen und gehören dem Nikinger.
  **Was ausdrücklich nicht gebaut wurde:** die eigene rot getönte Flächenfamilie `--caution-std-*`
  — sie *wäre* die gefüllte rote Fläche, die die Konvention ausschließt, und fiel deshalb.

- **P9-15 / V151 gemessen am 2026-10-03 — und der Befund ist größer als die Abnahmezeile:**
  **`/api/v1/overview` kostet live ~3,1 s**, davon **~2,4 s reine Serverarbeit.** Die
  Aufschlüsselung steht in `ABNAHME_MATRIX.md` (P9-15, V151) und ist in einem Satz hier: **`_overview()` wiederholt das ganze 6-Durchgänge-Muster pro sichtbarem Space** — ein `store.search()` pro Bucket plus einer für die Liste, und jeder Durchgang liest **jede** indizierte Datei neu (`limit` ist egal, ~100 ms). Bei 4 sichtbaren Spaces sind das **24 vollständige Durchgänge** über 197 Items; die Kosten wachsen **linear mit den Spaces**, nicht mit den Items. **Gemessen, nicht geraten:** in-process in der echten Form 2.388–2.407 ms in `/tmp` gegen 2.417–2.426 ms auf der VM-Platte (die Platte ist es also **nicht**), plus ein in-process Instrument (`ui_budget.py`, 1 Space / 220 Items), das den echten Endpunkt **3,3×** zu niedrig misst — 713 ms heute gegen 372,9 ms am 2026-09-13 auf **identischem** Instrument.
  **Nikinger-Entscheidung 2026-10-03: Inhalt einer neuen Phase, jetzt nicht weiter verfolgen.** Kein Code-Touch in P9, kein Backlog-Posten in dieser Phase. Zwei Dinge, die die neue Phase nicht neu messen muss: die **Ursache ist identifiziert** (die Per-Space-Schleife in `api.py`) und die **Messlatte ist falsch** (der 372,9-ms-Wert kommt aus einem anderen Instrument — Plan §3.3 erinnert seine Provenienz falsch). · **V151 selbst ist ✅**: der VPS-Weg kostet 76–113 ms auf ~3,1 s, also 2,4–3,6 % — *nicht relevant*. Der Weg war nie das Problem.
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

## Session stopped — 2026-10-05 (vierundzwanzigster Block: **Block settings gebaut — die drei Overlays sind eine Fensterkette, und V118 hat jetzt eine Linie**; Release `v3.1.3` steht, **kein Deploy, kein Service-Touch**)

**Ergebnis in einem Satz.** Drei eigenständige Overlays (`#account-dialog`,
`#space-admin-dialog`, `#update-log-dialog`) sind **eine** Kette: ein Menü, daneben das gewählte
Unterfenster, daneben bei Spaces das Detail; das Menü bleibt sichtbar und der Menüpunkt des offenen
Fensters trägt denselben Auswahlzustand wie eine Baumzeile in der Rail. V118 zeigt **eine** Linie,
weil die ausdrückliche Kante gewinnt. `pytest` **1223 → 1233**, `ui_budget` 5/5 (163,4 KB), Tabu-Diff
§0.3 leer, Browser-Probe **39/39**.

**Abnahme.** P9-83 – P9-93 ✅, P9-95 ✅, **P9-94 ⬜** (der Portscan aus §5 des Mini-Plans — ein
Schritt am MacBook des Nikingers, **durch keinen Test ersetzbar** und deshalb ⬜ statt ⚠️).
`[VERIFY]`: V185/V186/V187 ✅, **V188 ⬜** (P9-27/D1 bleibt ⚠️, bis eine Quelle statt einer Erinnerung
dasteht). Details je Zeile in `ABNAHME_MATRIX.md`, Herleitung im Mini-Plan §9.

### Zwei Zahlen, die mit wandern — der Wächter hat mich beim Schreiben darauf gestoßen

Der Zahlen-Wächter verlangt, dass der neueste Block **beide** benennt: die gemessene **gestrichene
Masse 229 B** (die im L3-Archiv liegt, nicht im Modulstatus) und den Grund, warum sie kein Hebel
ist. Der Block vom 2026-10-04 hatte beides; ein neuer Block ohne diese Zeile wäre stillschweigend
weniger gewesen, und der Wächter hätte **zu Recht** gemeldet. **Der Head liegt bei 22.196 B** —
unter dem 40-KiB-Softcap, zum ersten Mal seit dem Phasenstart (am 2026-10-04 durch die Rotation des
Modulstatus ins L3-Archiv). Beide Zahlen stehen hier, damit der nächste Block sie nicht verliert.

### Die zwei Befunde, die aus dem **Browser** kamen und aus den Tests nicht

1. **Der Schmal-Modus ließ zwei Panels stehen.** Die erste CSS-Fassung blendete nur das Menü aus.
   Bei offenem Space-Detail blieben die Spaces-Liste *und* das Detail nebeneinander sichtbar —
   genau die zwei, die P9-AI verbietet. Die Regel braucht **zwei** `:has()`-Regeln, nicht eine:
   „welches Panel ist das rechteste" steht im Zustand (`hidden`), nicht im Markup, weil das Menü im
   DOM zuerst steht. Wächter prüft die Form, die Probe die Wirkung.
2. **Der „Zurück"-Knopf des Details war tot.** `settings.js` verdrahtete ihn nur für die Stufen 2.
   Im breiten Modus fällt das nicht auf, weil ESC und „Schließen" denselben Weg nehmen — im
   **Schmal**-Modus ist das Detail das einzige Panel, also war sein „Zurück" der einzige Weg
   zurück. Wächter: `test_every_stage_has_a_wired_back_button`, der ausdrücklich prüft, dass die
   Ausnahme **nur** das Menü betrifft.

### Der Gegenlauf hat den eigenen Messaufbaum widerlegt — zum zweiten Mal in Phase 9

`graph_reload_probe.mjs` las für V118 den Frame **nach** dem Zurückschalten des Tag-Toggles, also
einen, in dem die Zwillingskante nicht mehr existiert. **Mit dem Fix aus wäre der Test grün
gewesen.** Behoben auf zwei Ebenen: der Shim führt jetzt `frames` (`clearRect()` ist die echte
Frame-Grenze, nicht ein Slice mit geratener Länge), und die Frames werden **vor** dem
Toggle-Zurückschalten gesichert. Das ist dieselbe Fehlerklasse wie der am 2026-10-02
eingecheckte Gegenlauf-Beleg: die Messung lief, aber an der falschen Stelle — und diesmal hat sie
sich selbst widerlegt, bevor sie jemand anders ertappt.

### Ein Öffner statt drei Listener (nicht im Plan, beim Bauen gefunden)

Beim Umbau hingen **zwei** `click`-Listener auf `#account-manage-spaces`: `app.js` öffnete
`openSpaceAdminDialog()`, `settings.js` schaltete um — der Knopf hätte sich **nie** geschlossen.
Jetzt hört nur `settings.js` zu, und die drei Eigentümer (`dialogs.js`, `spaces.js`, `updates.js`)
liefern ihren Zustands-Reset über `registerPanel(name, prepare)`. Die Lehre ist nicht „kein
Doppel-Listener", sondern **es gibt genau einen Öffner**; Wächter
`test_only_one_module_opens_a_panel`.

### Wächter, die umgeschrieben statt gelöscht wurden

- `test_app_html_has_a_live_manage_spaces_entry`: die Chevron-Assertion entfällt (es gibt kein
  Chevron mehr), `disabled` und `Phase 7` bleiben wörtlich.
- `test_account_nav_and_standard_button_wear_the_rail_selection_look` trägt jetzt nur noch die
  `.btn`-Hälfte; die Formregel steht in `test_account_nav_stays_layout_only_on_the_legacy_dialog`,
  das zusätzlich prüft, dass `.account-nav` **genau einen** Träger hat.
- `test_a_tag_edge_and_an_explicit_edge_draw_two_lines` → **umgedreht und umbenannt** zu
  `test_a_tag_edge_beside_an_explicit_edge_draws_one_line`, Docstring mit **beiden** Lesarten und
  Datum. Ein Testname, der das Gegenteil behauptet, wäre eine Lüge.
- **Drei 1024er-Wächter** lasen die 1024er Media-Query als *ersten* Treffer. Seit diesem Block gibt
  es **zwei** (der Schmal-Modus der Kette), und die drei wurden sofort rot, ohne dass sich am
  Shell-Grid etwas geändert hätte. Die Reparatur ist nicht „die Reihenfolge der Blöcke", sondern
  `_media_query_bodies()`: **alle** Blöcke sammeln und in der Gesamtheit suchen. Eine Breite ist
  eine Bedingung, keine Eigenschaft genau eines Blocks.
- Der Zahlen-Wächter hat **meine eigenen** neuen Gegenlauf-Dateien rot gemeldet, weil sie unter dem
  Erfolgsnamen lagen. Der Dateiname folgt jetzt **dem Ergebnis**: ein roter Lauf landet in
  `*_gegenprobe*.json` (`test_committed_probe_evidence.py` verlangt das Suffix am **Ende** — die
  erste Fassung setzte es davor und blieb rot).

### Zwei eigene Fehler in derselben Stunde, beide beim Messen

- Die erste Fassung der Regel-Lesemaschine `re.escape(condition)` auf einen bereits regexartigen
  String ⇒ **null Treffer** ohne Fehlermeldung; die drei Wächter blieben rot „ohne Grund".
- S7 der Probe wartete eine **feste** Sekundenzahl. Der Wegwerf-Harness sammelt Spaces über die
  Läufe, und `/api/v1/overview` kostet **linear mit deren Zahl** — der P9-15-Befund vom 2026-10-03,
  unerwartet wiederbelebt. Bei acht Spaces 2,1 s statt 1,5 s. Jetzt wird auf die **Bedingung**
  gewartet (`warte_bis`), nicht auf eine Uhr.

### Belege

- `pytest` **1223 → 1233** (**10** neue: 9 in `test_settings_chain.py` + 1 neue
  `test_account_nav_stays_layout_only_on_the_legacy_dialog`; 1 Test umgedreht, 3 umgeschrieben); `ui_budget` **5/5** (163,4 KB, `js/settings.js` 3,0 KB gzip); `node --check` grün
- **Tabu-Diff §0.3 leer** — auch `api.py`, `security.py` und `phase4_auth/` unberührt, der Block ist
  reines Frontend. Keine API-Route wurde angefasst, die Routen sind byte-identisch
- Browser-Probe `p9_settings_chain_probe.py` **39/39** gegen die TLS-Wegwerf-Instanz auf 18775,
  gestoppt über die PID-Datei. **Gegenläufe:** G1 (aria-current stumm) → **4 rot** · G2
  (`closeRightmost` schließt alles) → **2 rot** · G3 (implizite Kante nicht verworfen) → **rot**.
  Die statischen Wächter bleiben bei G1 **grün** — genau die Arbeitsteilung, die der Docstring der
  Testdatei begründet: statisch die *Ursache*, im Browser die *Wirkung*.
- **Bilder angesehen**, nicht nur geschossen: `p9_settings_01…04` (1440 px) und `05` (1024 px). Das
  Menü misst **202 px** bei `min-width: 0` — der Grund für „viel breiter als nötig" ist weg; die
  Feldreihenfolge mit TOTP **zuletzt** ist im Bild bestätigt; bei 1024 px ist genau ein Panel da.
- **Die Gegenlauf-Bilder sind gelöscht, nicht eingecheckt.** Sie hießen `p9_settings_g1*`/`g2*` und
  lagen im selben Verzeichnis wie die Erfolgsbelege — der Fehler, den der trace-Block am 2026-10-02
  gemacht hat, wäre sonst wiederholt worden. Die **JSON**-Gegenläufe sind rot eingecheckt
  (`*_g1_gegenprobe.json`, `*_g2_gegenprobe.json`), denn rot gehört dokumentiert.

### Offen, in dieser Reihenfolge

1. **Deploy `v3.1.3`** (Nikinger). Badge und `## 2026-10-05`-Block stehen. Das `deploy.sh`-Gate
   verlangt einen Datumsblock am Deploy-Tag — bei einem späteren Deploy `SHAREFYX_ALLOW_STALE_
   UPDATELOG=1` oder einen neuen `##`-Block. **Kein Index-Neuaufbau** zu erwarten: der Block fasst
   keine Contract-Datei an.
2. **P9-94 / P9-11** — der Portscan, Anleitung Mini-Plan §5 (MacBook, Handy-Hotspot, vier Ziele).
3. **V188** — eine Quelle, kein Code: das Beenden des macOS-Vollbilds per ESC ist
   Betriebssystem-/Browser-Verhalten. Der Keyboard-Lock-Weg steht in der Matrix ausdrücklich als
   *aus dem Gedächtnis, nicht nachgelesen*.
4. **P9-15 ⬜** (drei Läufe `/api/v1/overview` mit echter Sitzung) — unverändert, gehört an einen
   Deploy-Tag mit `health_gate.sh`.
