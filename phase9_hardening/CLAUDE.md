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
updated: 2026-10-05 (**die sieben Punkte aus der Bildsichtung gebaut, opencode/M3** — Probe **56/56**, G4 → 2 rot · G5 → 2 rot · G6 → 3 rot, `pytest` 1233 → 1238, `ui_budget` 165,6 KB; **zwei Korrekturen an der Vorgabe, beide gemessen**: `text-align` ist auf dem Flex-Knopf ein No-op → `justify-content`, und das linke Polster musste vom 32-px-Wert der Baumzeile auf `--space` (Nikinger-Entscheidung); **ein Produktbefund gemeldet, nicht gebaut** (leere Space-Liste beim zu frühen Öffnen, wandert in die P10-Liste); Release `v3.1.3` unverändert, **kein Deploy**) | 2026-10-05 (**Block settings gebaut, opencode/M3 — drei Overlays sind eine Fensterkette, V118 hat eine Linie**; Release `v3.1.3` steht, **kein Deploy, kein Service-Touch**; `pytest` 1223 → 1233, `ui_budget` 5/5, Tabu-Diff leer, Probe **39/39**, G1 → 4 rot · G2 → 2 rot · G3 → rot · **zwei Code-Befunde aus dem Browser, nicht aus den Tests** (Schmal-Modus ließ zwei Panels stehen · der „Zurück“-Knopf des Details war nicht verdrahtet) · **der Gegenlauf hat den eigenen Messaufbaum widerlegt** (er las den Frame nach dem Toggle-Zurückschalten — mit dem Fix wäre der Test grün gewesen) · P9-94 ⬜ Portscan, V188 ⬜ · **danach: sieben UI-Punkte aus der Bildsichtung notiert, nicht gebaut — Mini-Plan §10, Locks P9-AM–P9-AS, Abnahme P9-96–P9-102**) | 2026-10-05 (Block 2026-10-04 aus dem Head verbatim hierher rotiert, per `scripts/rotate_session_block.sh`)
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
| R | **Rückmeldung aus der Bildsichtung** (Mini-Plan §10, Locks P9-AM–P9-AS, Abnahme P9-96–P9-102) | 🟡 **gebaut 2026-10-05 (M3)**, Release `v3.1.3` steht (unverändert derselbe, nicht deployt) — Probe **56/56**, G4 → 2 rot · G5 → 2 rot · G6 → 3 rot, `pytest` 1233 → 1238 · **zwei Korrekturen an der Vorgabe, beide gemessen**: `text-align: center` war auf dem Flex-Knopf ein **No-op** (Textmitte 8,5 px daneben) → `justify-content`, und das **linke Polster** musste vom 32-px-Wert der Baumzeile auf `--space` (Nikinger-Entscheidung), sonst bleibt die Beschriftung 12 px neben der Mitte · P9-96/98/100/101/102 ✅, **P9-97 und P9-99 ⚠️ mit benannter Abweichung** · **zwei Wächter an korrektem Code rot** (Klassenreihenfolge, `hidden` im `aria-hidden`) · **ein Produktbefund gemeldet, nicht gebaut:** die Space-Liste bleibt leer, wenn man sie vor `loadOverview()` öffnet — wandert in die P10-Liste (Plan §6) · Herleitung im L3-Archiv |
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
- **Das lokale Vision-Modell ist als Werkzeug für Sichtprüfungen gestrichen — und das ist ein
  Posten für P10, kein Vorwurf an das Modell.** `qwen3-vl:8b` (Step C) hat am 2026-10-05 **zwei
  Fehlaussagen an einem Tag** geliefert: einmal eine Frage nicht beantwortet und dann behauptet,
  ein Menüpunkt sei blau markiert (es ist die Zeile in der Rail), und einmal bei einer **reinen
  Layout-Frage** **drei Panels mit erfundenen Inhalten** gemeldet — von denen **keines** im Bild
  stand (das Bild zeigt **ein** Panel). **Was daraus folgt, ist die Regel:** Zustand wird
  **gemessen** (`getComputedStyle`, `getBoundingClientRect`, `Range` über den Textknoten), und
  eine Modellantwort über Layout ist **ohne Gegenprobe kein Beleg** — die Quote „6 von 7 richtig"
  aus dem Vorblock ist kein Kriterium, derselbe Block hat beim siebten Bild dieselbe Frage falsch
  beantwortet. **Sichtprüfung bleibt beim Nikinger** (Regel in
  `docs/concepts/sichtpruefung_automation_conventions.md` §2). **P10-Posten:** das Modell gegen
  eine Alternative stellen — mit **einer** Frage, deren Antwort man schon kennt; ein Modell, das
  die verneint, ist gestrichen. Signatur + Prüfmuster: dieselbe Datei, neuer Abschnitt vom
  2026-10-05.
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

## Session stopped — 2026-10-05 (fünfundzwanzigster Block: **die sieben Punkte aus der Bildsichtung gebaut — und zwei davon haben einen Fehler in der Vorgabe selbst gefunden**; Release `v3.1.3` unverändert, **kein Deploy, kein Service-Touch**)

**Ergebnis in einem Satz.** Alle sieben Punkte aus der Bildsichtung sind umgesetzt (Mini-Plan §10,
Locks P9-AM–P9-AS, Abnahme P9-96–P9-102), und die erste Browser-Probe hat **zweimal die
Vorgabe selbst widerlegt** statt den Bau: `text-align: center` ist auf einem Flex-Knopf ein
**No-op**, und „Text mittig" ist mit dem geerbten 32-px-Einzugspolster der Baumzeile **nicht**
erreichbar. `pytest` **1233 → 1238**, `ui_budget` 5/5 (**165,6 KB**), Tabu-Diff §0.3 leer,
Browser-Probe **56/56**, Gegenläufe **G4 → 2 rot · G5 → 2 rot · G6 → 3 rot**.

**Abnahme.** P9-96 ✅ · P9-97 **⚠️** · P9-98 ✅ · P9-99 **⚠️** · P9-100 ✅ · P9-101 ✅ · P9-102 ✅.
**Die beiden ⚠️ sind benannte Abweichungen, keine offenen Punkte** — P9-97 trägt die vom Nikinger
entschiedene Polster-Entscheidung, P9-99 den gemessenen Umweg. Zeilen und Belege je einzeln in
`ABNAHME_MATRIX.md`, Herleitung in §10.1–§10.3 des Mini-Plans. `[VERIFY]`-Bilanz unverändert
(V188 ⬜).

### Die zwei Stellen, an denen die Vorgabe falsch war — beide erst durch Messung

1. **`text-align: center` ist auf dem Menüknopf ein No-op.** Der Knopf ist `display: flex` (die
   Sammelregel mit `.tree__folder`) und sein einziges Kind ist ein **anonymer Flex-Item** — ein
   Textknoten. `text-align` wirkt auf Blockcontainer; im Flex-Item zentriert es einen Text in
   sich selbst. Die erste Fassung des Baus hatte genau das, und die erste Probe maß die Textmitte
   **8,5 px neben** der Knopfmitte. Gebaut ist `justify-content: center` — die Flex-Achse.
   **Sichtbarstark:** der Wächter verbietet `text-align` in einer eigenen Menüpunkt-Regel jetzt
   ausdrücklich, und prüft zusätzlich, dass der Knopf überhaupt `display: flex` trägt — sonst
   dürfte jemand die Sammelregel umstellen und der Wächter bliebe grün.
2. **„Text mittig" und „Polster = Baumzeile" können nicht beide gelten.** Als `.tree__folder`
   erbte der Menüpunkt `padding-left: 32px` — die *Einrückung* der Baumzeile — gegen 8 px rechts.
   Der Inhaltskasten lag damit **12 px** rechts, und der breiteste Menüpunkt hatte **0 px Spiel**.
   **Das war eine Frage an den Nikinger, Antwort: beidseitig `--space`.** Was das kostet, steht
   am Stylesheet und in S1: der Menüpunkt ist in *diesem* Wert nicht mehr die Baumzeile (Höhe,
   Polster oben/unten, Schrift, Rundung bleiben es), und die Messung nennt die 32 px **mit**.
   *Nicht* gebaut: die Einrückung an der Quelle auf die Rail einzuschränken — das hätte zusätzlich
   die Space-Zeilen verschoben, eine zweite, nicht beauftragte Änderung.

### Ein echter Produktbefund, gemeldet und **nicht** gebaut

**Die Space-Liste kann leer bleiben, wenn man sie zu früh öffnet.** `renderSpaceList()` rendert aus
`state.spaces`, und das steht erst nach `loadOverview()` fest; neu gerendert wird nur beim nächsten
Öffnen. „Einstellungen → Spaces verwalten" in den ersten Sekunden nach dem Laden zeigt deshalb
**nichts**. Die Wahrscheinlichkeit **wächst linear mit den sichtbaren Spaces** (P9-15 vom
2026-10-03) — im Harness mit zwölf Spaces ist das der Normalfall: der erste Lauf dieser Session
maß S1 gegen eine **leere** Rail und meldete die Station rot, ohne dass sich am Menü etwas
geändert hätte. **Warum nicht gebaut:** die Reparatur ist eine *Zustandsentscheidung* (ein zweiter
Hook neben `registerPanel` oder ein Ereignis zwischen `loadOverview()` und den Panel-Eigentümern),
keine Zeilenänderung, und der Auftrag umfasste sie nicht. **Steht in der P10-Liste** (Plan §6, 3.).

### Was der Wächter-Teil dieser Session gekostet hat — fünf eigene Fehler, alle vom selben Typ

Die Fehlerklasse war durchgehend: **ein Wächter oder eine Messung, die am Muster scheitert, sieht
wie ein Befund aus.** Konkret, alle fünf:

1. `class="btn settings-back"` mit **fester Klassenreihenfolge** — der Knopf heißt jetzt
   `btn btn--icon settings-back`, und der Wächter meldete vier Panels *ohne* Zurück-Knopf, während
   er sichtbar neben dem Test stand.
2. Der `hidden`-Test lief über das **ganze** Element — das neue `<svg aria-hidden="true">`
   enthält das Wort. Jetzt nur der öffnende Tag, mit `(?<![\w-])hidden\b`.
3. `re.escape()` auf einen **bereits regexartigen** String (wie am 2026-10-05 in der Probe) ⇒ null
   Treffer ohne Fehlermeldung.
4. **Eine Zeilenannahme statt einer Regel-Lesemaschine:** `^([^{}]*text-align:…)\{` findet eine
   Regel nicht, die über mehrere Zeilen geschrieben ist — und der Wächter meldete „nicht gebaut".
   Der Wächter las außerdem den *Body* der `.settings-chain`-Regel als wären er ihr Selektor.
   Ersatz: `_alle_regeln()` als **eine** Lesemaschine für das ganze Modul.
5. **Eine Regel-Lesemaschine, die die Zustandsregel mit der eigenen Regel verwechselte:** wer nach
   `aria-current="true"` sucht, findet auch `:not([aria-current="true"])` — P9-AO wäre als
   „umgestellt" gemeldet worden, obwohl die Auswahlregel unverändert ist.

Dazu **fünf Zeilen Test, der den Wächter prüft statt ihn zu glauben**
(`test_the_menu_item_watchdog_bites_on_built_in_violations`): zwölf eingebaute Verstöße, jeder
muss rot werden — darunter `background: #0C1015` (Farbe statt Token) und `padding-left: 24px`
(eigener Wert). Und **ein Gegenlauf auf der Testseite**: `background` aus der eigenen Regel
entfernt ⇒ 2 Wächter rot, `background: #0C1015` statt Token ⇒ 2 rot.

### Belege

- `pytest` **1233 → 1238** (5 neue Tests in `test_settings_chain.py`, keiner umgedreht, 2 am
  Wächter korrigiert); `ui_budget` **5/5** (165,6 KB; `app.css` 30,7 KB gzip); `node --check` grün
- **Tabu-Diff §0.3 leer** — `api.py`, `security.py`, `phase4_auth/` unberührt, der Block ist reines
  Frontend. Keine API-Route angefasst
- Browser-Probe `p9_settings_chain_probe.py` **56/56** gegen die TLS-Wegwerf-Instanz auf 18775,
  gestoppt über die PID-Datei. **Gegenläufe:** G4 (P9-AP raus) → **2 rot** · G5 (P9-AS raus) →
  **2 rot** · G6 (P9-AN mit eigener Höhe) → **3 rot**. **Die Plan-Aussage zu G6 war falsch
  benannt:** eine eigene Höhe trifft nicht die Flächen-Zeile (P9-97), sondern die
  **Geometrie**-Zeile **P9-84** (S1, `h=40` gegen `h=35.69`) — im Plan §10.2 Punkt 5 korrigiert
- **Drei Messkorrekturen in der Probe**, jede mit derselben Lehre: `compareDocumentPosition` prüfte
  die Gegenrichtung und übersprang genau die Elemente, die gesucht waren (S13 fand nichts); S14
  verglich die *Inhaltskante* eines Knopfes mit der Inhaltskante seines Panels (das sind zwei
  Kästen, die 15 px waren `.btn`s eigenes Polster); S15 maß einen **gesperrten** Knopf mit
  0 × 0 Rechteck bei (0,0) und meldete eine grüne Station **ohne Aussage**
- **Bilder:** `p9_settings_01..08` neu aufgenommen (die sieben vom Vortag tragen den neuen Stand),
  `screenshots_latest/` rotiert (drei Symlinks unverändert, der dritte zeigt jetzt `08` statt des
  Duplikats `04`). **Die Gegenlauf-Bilder sind gelöscht, nicht eingecheckt** — der Fehler, den der
  trace-Block am 2026-10-02 gemacht hätte; die JSON-Gegenläufe liegen rot im Repo
- **Das lokale Vision-Modell hat zum zweiten Mal in Folge nicht geantwortet — diesmal mit erfundenem
  Inhalt.** Die Frage nach dem Layout von `p9_settings_01_menue_1440.png` (ein einziges Panel,
  drei Knöpfe) wurde beantwortet mit „drei Panels nebeneinander: Übersicht, alpha, VERKNÜPFUNGEN" —
  **diese Inhalte stehen in keinem der acht Bilder.** Die Dateien sind gültige PNGs der
  erwarteten Größen aus diesem Lauf (1440×900 / 1024×768, 15:46). **Es gibt also von dieser
  Session keine Sichtaussage**, weder für noch gegen den Bau; die gemessenen Werte (0 px Textmitte,
  24 px Titelabstand, 0,0 px Knopfkante) stammen aus der Probe, nicht aus einem Bild. **Die
  Sichtprüfung ist der Nikinger-Schritt** — Dateinamen und Checkkriterien stehen in
  `screenshots_latest/README.md`. Der Befund bestätigt die Regel vom 2026-10-05 (dort ein
  Frage-abbruch, hier eine Fehlaussage): **das Bild belegt Wirkung, nie Zustand — und ein Modell,
  das den Inhalt erfindet, belegt gar nichts**
- **Zahlen, die mit wandern:** die gestrichene Masse bleibt **229 B** und liegt im L3-Archiv
  (`MODULE_STATUS_ARCHIVE.md`), nicht im Modulstatus — sie ist auch heute **kein Hebel**, denn der
  Head liegt mit ~28 KB **unter** dem 40-KiB-Softcap. `ABNAHME_MATRIX.md` ist auf **103 Zeilen /
  88 ✅ · 11 ⚠️ · 4 ⬜** gewachsen und benennt sich damit selbst (P8-P, „benannt statt versteckt")

### Offen, in dieser Reihenfolge

1. **Deploy `v3.1.3`** (Nikinger). Badge und `## 2026-10-05`-Block stehen unverändert; dieser Block
   hat **keine** Release-Änderung gebracht. Das `deploy.sh`-Gate verlangt einen Datumsblock am
   Deploy-Tag — bei einem späteren Deploy `SHAREFYX_ALLOW_STALE_UPDATELOG=1` oder ein neuer
   `##`-Block
2. **Sichtprüfung der acht neuen Bilder** — das ist der eigentliche Abnahmeschritt dieses Blocks.
   Die **beiden ⚠️** sind es, die die Sichtung entscheidet: steht der Text mittig (P9-99) und ist
   die Fläche so, wie er sie im Bild meinte (P9-97)
3. **P9-94 / P9-11** — der Portscan, Anleitung Mini-Plan §5 (MacBook, Handy-Hotspot, vier Ziele)
4. **V188** — eine Quelle, kein Code (P9-27/D1)
5. **P9-15 ⬜** (drei Läufe `/api/v1/overview` mit echter Sitzung) — gehört an einen Deploy-Tag mit
   `health_gate.sh`
6. **Doku-Drift, klein und nicht angefasst:** `docs/screenshots/README.md` und
   `screenshots_latest/README.md` stehen in `test_updated_chain.py :: KNOWN_OFFENDERS` (fehlendes
   `updated:`-Feld bzw. zwei Fäden mit `updated: `-Präfix). `screenshots_latest/` ist in diesem
   Commit **repariert** (Fäden ohne Präfix, Eintrag gestrichen), `docs/screenshots/README.md`
   nicht — dort fehlt das Feld ganz, und die Datei nennt in ihrer Kette eigene Bytes. **Kein
   Test meldet es**; die Reparatur gehört zum Doku-Fundament, nicht zu diesem Block

