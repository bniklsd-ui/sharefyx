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
updated: 2026-10-05 (**V188 beantwortet, opencode/M3 — vier Quellen, eine am Repo gemessen, und der Plan-§4-Wortlaut „meines Wissens nur in Chromium" ist jetzt eine Messung: `safari: false`**; daraus **P9-27 ⬜ → ⚠️**, D1 geschlossen, **kein Code gebaut** (Nikinger-Entscheidung 2026-10-05) · **drei falsche Sätze datiert korrigiert**, darunter „der Deploy `v3.1.1` schließe P9-15, denn `health_gate.sh` macht die Läufe" — **ein Health-Gate liefert Läufe ohne Kriterium**, denn P9-15 stellt gegen 372,9 ms, und der Wert ist nie über Funnel gemessen worden (V151) · **der letzte `KNOWN_OFFENDERS`-Eintrag gestrichen** (`docs/screenshots/README.md`, zwei Ausprägungen zugleich, in zwei Schritten repariert, sechs Fadeninhalte byteweise gegengeprüft) · **zwei Zeilen** in `test_acceptance_numbers.py` (Bilanz-Konstanten), **eine entfernt** in `test_updated_chain.py` · kein Test hinzugefügt, keiner umgedreht, Tabu-Diff §0.3 leer, Release `v3.1.3` unverändert, **kein Deploy**) | 2026-10-05 (**die sieben Punkte aus der Bildsichtung gebaut, opencode/M3** — Probe **56/56**, G4 → 2 rot · G5 → 2 rot · G6 → 3 rot, `pytest` 1233 → 1238, `ui_budget` 165,6 KB; **zwei Korrekturen an der Vorgabe, beide gemessen**: `text-align` ist auf dem Flex-Knopf ein No-op → `justify-content`, und das linke Polster musste vom 32-px-Wert der Baumzeile auf `--space` (Nikinger-Entscheidung); **ein Produktbefund gemeldet, nicht gebaut** (leere Space-Liste beim zu frühen Öffnen, wandert in die P10-Liste); Release `v3.1.3` unverändert, **kein Deploy**) | 2026-10-05 (**Block settings gebaut, opencode/M3 — drei Overlays sind eine Fensterkette, V118 hat eine Linie**; Release `v3.1.3` steht, **kein Deploy, kein Service-Touch**; `pytest` 1223 → 1233, `ui_budget` 5/5, Tabu-Diff leer, Probe **39/39**, G1 → 4 rot · G2 → 2 rot · G3 → rot · **zwei Code-Befunde aus dem Browser, nicht aus den Tests** (Schmal-Modus ließ zwei Panels stehen · der „Zurück“-Knopf des Details war nicht verdrahtet) · **der Gegenlauf hat den eigenen Messaufbaum widerlegt** (er las den Frame nach dem Toggle-Zurückschalten — mit dem Fix wäre der Test grün gewesen) · P9-94 ⬜ Portscan, V188 ⬜ · **danach: sieben UI-Punkte aus der Bildsichtung notiert, nicht gebaut — Mini-Plan §10, Locks P9-AM–P9-AS, Abnahme P9-96–P9-102**) | 2026-10-05 (Block 2026-10-04 aus dem Head verbatim hierher rotiert, per `scripts/rotate_session_block.sh`)
---

# Phase 9 — Härtung

Voller Plan: `docs/concepts/phase9_hardening_plan.md`. Diese Datei trägt nur Modulstatus und
den aktuellen Session-Block; die Entscheidungen (P9-A–P9-T) und Step-Details stehen im Plan.

## Modulstatus

| Step | Inhalt | Status |
|---|---|---|
| 0 | Verifikations-Durchlauf, Doku-Fundament (Phasenverzeichnis, INDEX-Rotation, vier Defekte, `doc_health.py`, Baseline) | ✅ (Details im L3-Archiv) · Herleitung im L3-Archiv |
| A | Echte Domain über eigenen VPS | 🟡 **A7a + A7 ✅ 2026-10-03; A8 für Konto *niklas* ✅** — P9-10b ✅ · P9-12 ✅ · P9-14 ✅ · **P9-13/V150 ⬜ zurückgestellt, wandert nach P10, ist kein Blocker** (Nikinger 2026-10-04: ein Schritt, der nur ein Konto braucht, ist ein Termin, kein Blocker; Plan §0.1a) · **P9-15 ist ⚠️, nicht ⬜ — datierte Korrektur vom 2026-10-05**, die Zeile ist seit dem 2026-10-03 gemessen (drei Läufe `/api/v1/overview` mit echter UI-Session, beide Beine) und der Vergleich gegen 372,9 ms war nicht möglich (V151); der Deploy schließt sie **nicht**, `health_gate.sh` liefert Läufe ohne Kriterium. Übergangsfenster **unbefristet, live seit 2026-10-05** (`v3.1.2`, `LEGACY_UNTIL=open`, Nikinger-Entscheidung: Firmen-Proxy setzt die neue Domain zurück) · Herleitung im L3-Archiv |
| B | `tailscaled-watchdog.service` | ✅ **abgeschlossen 2026-10-01**, live; P9-16–P9-20 ✅, V152/V153 ✅. `socat` 1.8.0.0 + Unit laufen unter voller Härtung, `RuntimeDirectoryPreserve=yes` (Befund 7) und Systempfad (Befund `__REPO_ROOT__`) behoben · V153: `sudoers` unbaubar, polkit greift · Herleitung im L3-Archiv |
| C | Vision-Dienst auf der RTX 3060 | ✅ **abgeschlossen** (2026-09-26): GPU-Inferenz reboot-fest + C8 (`ollama` auf der VM `inactive`) · P9-21/-23/-26 ✅ · **P9-22 deferred** (Nikinger 2026-09-26, architektonisch belegt statt extern getestet) → Revisit Step Z oder P10 · Herleitung im L3-Archiv |
| D | Zwei gemeldete Bugs (ESC/Vollbild, Drop-Ziel Space-Wurzel) | 🟡 **D2 am Browser belegt 2026-10-03** (P9-28/-29/-30 ✅, Probe **16/16**); **D1 ist am 2026-10-05 geschlossen — P9-27 ⚠️, V188 ✅** (Nikinger-Entscheidung 2026-10-05: *kein Code*). Vier Quellen, und die Antwort ist **Betriebssystem-Verhalten**: ein immer wirkender Ausgang ist Pflicht (WHATWG Fullscreen §8, Anti-Spoofing), WICG Keyboard Lock §7 **darf** ihn nicht abschalten, §4.2 gilt nur für JS-initiiertes Vollbild, und MDN-`browser-compat-data` sagt `safari: false` — **auf dem MacBook existiert der einzige Hebel gar nicht**. Gemessen am Repo: `app.js:259` ist der einzige `fullscreen`-Bezug der App · Herleitung im L3-Archiv |
| E | Karte: Reload-Overload, V118 | ✅ **abgeschlossen** (2026-09-28): kein zweiter `/graph`-Abruf, bekannte Knoten behalten `x`/`y`, `force` nur am Refresh-Knopf · P9-33/-34/-35 ✅ · V118 beantwortet · die Design-Frage P9-36 („eine oder zwei Linien") liegt beim Nikinger · Herleitung im L3-Archiv |
| F | Schema-Fundament (neunte P1-Contract-Öffnung: `doing`/`assignee`) | 🟡 **code-complete 2026-09-30, live seit 2026-10-02** (`v3.1.0`) · P9-43 ✅ (≤ 1,05 s für 197 Items) · **der `doing`-Bereich ist seit 2026-10-02 geschlossen** (Lock P9-V) ⇒ **P9-P ist datiert eingeengt, nicht erledigt**: die prominente Darstellung bleibt P10 · P9-U (Space-Name, ohne Validierung) und P9-V stehen im Plan · Herleitung im L3-Archiv |
| G | Löschen (F2) nach `_trash/` | 🟡 **code-complete 2026-09-30, deployt 2026-10-02** (`v3.1.0`); **Live-Löschung noch nicht beobachtet** ⇒ V162 *(Lesart A)* ⬜ · der Lösch-Ort aus Plan §9.3 war unbaubar, Nikinger entschied `DATA_ROOT/._trash/<space>/` mit **null** P1-Änderungen · Herleitung im L3-Archiv |
| H | Abhängigkeits-Hygiene | 🟡 **code-complete 2026-09-30** · `fastmcp` **exakt** auf `3.4.7` gepinnt (P3-D/P4-R waren seit 2026-08 beschlossen und nie umgesetzt) · V163 ✅ (inert) · P9-55 ⚠️ in der Form (`==3.4.7` statt Range, Nikinger 2026-09-30) · **benannt, nicht gebaut:** das transitive `mcp` bleibt ungepinnt (P9-Backlog-Kandidat) · Herleitung im L3-Archiv |
| doing | Fünfter Eimer „In Arbeit" (Lock **P9-V**, Kandidat (a)) — Voraussetzung für den Deploy `v3.1.0` | ✅ **live seit 2026-10-02** (`v3.1.0`, Gate 9/9) · Locks P9-V/W/X · 6 Tests, Gegenlauf 7 rot, Browser 11/11 · Release-Commit `v3.1.1` **2026-10-03** · Herleitung im L3-Archiv |
| trace | Nachvollziehbarkeit: `assignee` sichtbar (UI + MCP, vom Client gefüllt, P9-Z) + `updated_by` + Git-Autor (P9-AA–AC); **zehnte P1-Contract-Öffnung** | 🟡 **code-complete 2026-10-02, seit 2026-10-03 live** (`v3.1.1`, Release `20261003T205843`, Gate 9/9) · Locks P9-Y–AD · **zehnte P1-Contract-Öffnung ohne Index-Schema-Sprung** ⇒ beim Deploy **kein** Neuaufbau (am Journal bestätigt) · 24 Tests, Browser 8/8 mit Zwei-Principalen-Instanz · Herleitung im L3-Archiv |
| E (Extra) | **Buttons ans Schema** (B17): die Knöpfe mit eigenen Flächen auf die Standard-Tokens `--btn-std-*` umstellen | ✅ **gebaut 2026-10-02 (B17), seit 2026-10-03 live** · die Backlog-Liste war an zwei Stellen falsch (15 statt 1 Knopf auf der alten Flächenfamilie) · `.btn.action--caution` trägt jetzt **exakt** die Standardfläche, nur die Beschriftung ist rot · Kontrast **4,38:1** bleibt unter WCAG-AA — **Design-Entscheidung, deine** · Herleitung im L3-Archiv |
| S | **Einstellungen als Fensterkette** + V118 eine Linie (Nikinger 2026-10-05) | 🟡 **gebaut 2026-10-05 (M3)**, Release `v3.1.3` steht, **nicht deployt** — `docs/concepts/phase9_hardening_block_settings_plan.md` (Locks P9-AE–AL, Abnahme P9-83–95) · **drei Overlays wurden eine Kette** (`#settings-overlay`, fünf Panels), **ein** Öffner (`settings.js` + `registerPanel`), Menüknöpfe tragen `.tree__folder` statt einer eigenen Optik · **zwei echte Befunde aus dem Browser, nicht aus dem Test**: der Schmal-Modus ließ bei offenem Detail **zwei** Panels stehen (zwei `:has()`-Regeln statt einer), und der „Zurück"-Knopf des Details war **nicht verdrahtet** (im breiten Modus unauffällig) · **V118 umgedreht**: der Test hieß `…_draw_two_lines` und heißt jetzt `test_a_tag_edge_beside_an_explicit_edge_draws_one_line`, Docstring mit beiden Lesarten und Datum · **Probe 39/39**, G1 → 4 rot, G2 → 2 rot, G3 → rot, **der Gegenlauf hat den eigenen Messaufbaum widerlegt** (er las den Frame *nach* dem Toggle-Zurückschalten) · `pytest` 1223 → 1233, `ui_budget` 5/5, Tabu-Diff leer · **P9-94 ⬜** (Portscan, Nikinger-Schritt) · Herleitung im L3-Archiv |
| R | **Rückmeldung aus der Bildsichtung** (Mini-Plan §10, Locks P9-AM–P9-AS, Abnahme P9-96–P9-102) | 🟡 **gebaut 2026-10-05 (M3)**, Release `v3.1.3` steht (unverändert derselbe, nicht deployt) — Probe **56/56**, G4 → 2 rot · G5 → 2 rot · G6 → 3 rot, `pytest` 1233 → 1238 · **zwei Korrekturen an der Vorgabe, beide gemessen**: `text-align: center` war auf dem Flex-Knopf ein **No-op** (Textmitte 8,5 px daneben) → `justify-content`, und das **linke Polster** musste vom 32-px-Wert der Baumzeile auf `--space` (Nikinger-Entscheidung), sonst bleibt die Beschriftung 12 px neben der Mitte · P9-96/98/100/101/102 ✅, **P9-97 und P9-99 ⚠️ mit benannter Abweichung** · **zwei Wächter an korrektem Code rot** (Klassenreihenfolge, `hidden` im `aria-hidden`) · **ein Produktbefund gemeldet, nicht gebaut:** die Space-Liste bleibt leer, wenn man sie vor `loadOverview()` öffnet — wandert in die P10-Liste (Plan §6) · Herleitung im L3-Archiv |
| Gate/Z | Abnahme, Closeout | 🟡 **beide Doku-Hälften erledigt** (2026-10-02) · `ABNAHME_MATRIX.md` ist der **eine** Ort der Abnahme- und `[VERIFY]`-Bilanz, nicht diese Zeile · **[2026-10-04] beide Rotationen gefahren** (Block 17.780 B verbatim, Kette 6 von 7 Fäden) und diese Tabelle ins L3-Archiv gezogen ⇒ **der Head ist unter dem 40-KiB-Softcap** · **offen:** zweites Claude-Konto (P9-13/V150) · Portscan P9-94/P9-11 · Übersichtsgrafik §12.4 · Phase auf ✅ — **P9-15 steht nicht mehr hier**, es ist seit dem 2026-10-03 gemessen (⚠️, Zeile A) · Herleitung im L3-Archiv |

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
- **D1 — ESC im Vollbild schließt zusätzlich das Item. ✅ GESCHLOSSEN am 2026-10-05, ohne Code.**
  Gemeldet 2026-09-23 (macOS Safari, natives Vollbild über den grünen Knopf), zurückgestellt am
  2026-09-23, entschieden am 2026-10-05: *kein Code*, **V188** beantworten, P9-27 auf ⚠️. Die
  Antwort ist **Betriebssystem-Verhalten**, und die Seite kann es nicht verhindern: ein immer
  wirkender Ausgang aus dem Vollbild ist Pflicht (WHATWG Fullscreen §8 — Anti-Spoofing), WICG
  Keyboard Lock §7 **darf** ihn nicht abschalten, auch nicht bei allen angeforderten Tasten, und
  der einzige Hebel verschiebt nur ESC auf „langer ESC" (> 2 s). Für den gemeldeten Fall ist er
  doppelt unbrauchbar: §4.2 gilt nur für JS-initiiertes Vollbild, und MDN-`browser-compat-data`
  sagt `Keyboard.lock` → **`safari: false`**. Am Repo gemessen: `app.js:259` ist der einzige
  `fullscreen`-Bezug der App, die Web-API greift im nativen Vollbild nicht. **Beleg:** P9-27-Zeile
  und V188-Zeile in `ABNAHME_MATRIX.md`, Kurzfassung in §9 des settings-Plans. **P9-28 bleibt ✅**
  und ist eine andere Frage: der Guard ist im *Web*-Vollbild richtig und am Browser beider
  Richtungen belegt.
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

## Session stopped — 2026-10-05 (sechsundzwanzigster Block: **V188 beantwortet — die Seite kann es
nicht verhindern, und auf dem MacBook existiert der einzige Hebel gar nicht**; dazu der
Doku-Drift-Teil des settings-Closeouts. **Kein Code, kein Deploy, kein Service-Touch**)

**Ergebnis in einem Satz.** Die beiden Punkte, die M3 machen konnte, sind erledigt: **V188 ✅** mit
vier Quellen (drei nachgelesen, eine am Repo gemessen) ⇒ **P9-27 ⚠️, D1 geschlossen, kein Code
gebaut** — genau die Entscheidung, die das gestrige Plan-§4 unter dieser Bedingung zugelassen hat;
und der **letzte `KNOWN_OFFENDERS`-Eintrag** ist repariert und aus der Ausnahmeliste gestrichen.
Dabei sind **drei falsche Sätze** gefunden und datiert korrigiert, von denen einer behauptete, ein
Deploy schließe eine Abnahmezeile, die er nachweislich nicht schließen kann.

### V188 — die Antwort, und die zwei Stellen, an denen sie schärfer ist als die Frage

**Betriebssystem-Verhalten; die Seite kann es nicht verhindern, nur verschieben — und die
Verschiebung gibt es auf dem MacBook nicht.** Vier Belege, jeder mit Ort; die vollständige Kette
mit wörtlichen Zitaten steht in der P9-27-Zeile der `ABNAHME_MATRIX.md` (dort, nicht hier, weil
die Quelle an einer Stelle stehen soll):

1. **Der Fall ist nicht einmal die Web-API** — und das ist **gemessen, nicht vermutet**.
   `grep -rn fullscreen phase5_ui/webui/static/js/app.js` liefert **eine** Zeile: `app.js:259`,
   `if (document.fullscreenElement) return;`. Die App ruft `requestFullscreen()` nirgends auf ⇒
   der gemeldete Fall (grüner Knopf / Ctrl+Cmd+F) ist natives macOS-Vollbild, und dafür gibt es
   keine Web-API: `fullscreenElement` bleibt `null`, kein `fullscreenchange`. Der Guard ist für
   genau diesen Fall ein No-op — das stand in der Matrix bis heute als „mit hoher Sicherheit".
2. **Der Ausgang ist Pflicht, und das ist Anti-Spoofing.** WHATWG Fullscreen §4: *„The user agent
   may end any fullscreen session without a close request or call to `exitFullscreen()` whenever
   the user agent deems it necessary."* §8: *„User agents should provide a means of exiting
   fullscreen that always works and advertise this to the user. This is to prevent a site from
   spoofing the end user …"*
3. **Der einzige Hebel verschiebt nur.** WICG Keyboard Lock §7: *„the user agent MUST provide a
   way for the user to exit from keyboard lock **even if all of the keys are requested by the
   API**"* (+ langes ESC > 2 s, §3.2). WHATWG §6: *„User agents should reserve an additional
   input for the purposes of exiting fullscreen"*. MDN `Element.requestFullscreen()`: *„Most
   browsers use the Esc key to exit normal fullscreen mode, and a long-press Esc key to exit
   keyboard lock."*
4. **Der Hebel ist doppelt unbrauchbar — und hier wurde die Gedächtnisaussage des Plans zur
   Messung.** **(a)** WICG §4.2: Keyboard Lock gilt nur für JS-initiiertes Vollbild, *„During F11
   fullscreen, no Keyboard Lock processing of keyboard events will take place."* **(b)**
   Browser-Support aus **MDNs `browser-compat-data`** (`api/Navigator.json`, `api/Keyboard.json`,
   Branch `main`): `navigator.keyboard`, `Keyboard.lock`, `Keyboard.unlock` → Chrome/Chromium ab
   68, Edge/Opera `mirror`, **`firefox: false`**, **`safari: false`** (damit auch iOS).
   Das Plan-§4-Wort „**meines Wissens** nur in Chromium" ist damit nicht widerlegt, sondern
   **gemessen** — und für den Anwendungsfall schärfer: **gar nicht vorhanden.**

**Folge:** P9-27 ⬜ → ⚠️ (die Zeile ist nicht *erfüllt*, sondern **gegenstandslos geworden** — die
Frage dahinter ist beantwortet, die Messung am echten Gerät bleibt für das native Vollbild offen
und ist per Spezifikation nicht automatisierbar). **P9-28 bleibt ✅**: dessen ✅ gilt der
Web-API-Seite des Guards, und das ist eine andere Frage. **D1 ist geschlossen, es wurde kein Code
gebaut** — der gebaute Guard bleibt, weil er für den Web-Fullscreen-Fall genau richtig ist.

### Drei falsche Sätze, alle aus dem settings-Closeout §6.1, alle datiert korrigiert

1. **„Der Deploy `v3.1.1` schließt P9-15, denn `health_gate.sh` macht die
   `/api/v1/overview`-Läufe"** — in `ABNAHME_MATRIX.md`s datiertem „Reihenfolge"-Block. **Falsch,
   und es ist keine Formulierung, sondern ein Zustand:** P9-15 stellt gegen **372,9 ms**, und
   dieser Wert ist **nie über Funnel gemessen worden** (V151: in-process auf synthetischem
   Bestand, 8,3× zu niedrig). Ein Health-Gate liefert Läufe **ohne Kriterium**. Die Zeile selbst
   stand schon am selben Tag korrekt auf ⚠️ — der Block daneben nicht.
2. **„P9-15 ist der authentifizierte Latenzvergleich und gehört an den Deploy-Tag"** — im
   „Stand in einem Satz" **derselben** Datei, also zwei Ebenen unter der, die schon richtig war.
   Korrigiert und mitgezählt: die 3 offenen Zeilen sind **P9-11, P9-13/V150, P9-94**; der
   Modulstatus-Head und der Wurzel-Block trugen denselben Fehler.
3. **„Seit dem 2026-10-04 ist kein ⬜ ein Personenschritt"** — im selben Absatz, und mit P9-94
   **falsch geworden**: zwei der drei ⬜ brauchen ein MacBook mit Handy-Hotspot. Richtig und
   tragend ist der zweite Satz, und der steht jetzt allein: **kein ⬜ ist offene Code-Arbeit, und
   keiner blockiert die Phase.** Der Satz davor war außerdem **im Repo ungrammatisch** — ein
   angebrochener Halbsatz („… ein Konto, kein Code" / „als zurückgestelltem Backlog-Posten"),
   sichtbar beim Lesen der Nachbarzeile.

**Bilanz:** die Abnahme- und die `[VERIFY]`-Tabelle haben je eine Zeile bewegt, die **Matrix ist
die Quelle** (`test_acceptance_numbers.py` zählt nach und vergleicht mit dem Fließtext — die beiden
Konstanten wurden **vor** dem Schreiben gesetzt, sonst wäre der Wächter eine Tautologie; er stand
beim Zurückschreiben des Fließtexts rot und wurde danach grün).

### Der letzte `KNOWN_OFFENDERS`-Eintrag ist weg — und die Reparatur brauchte zwei Schritte

`docs/screenshots/README.md` stand mit **beiden** Ausprägungen zugleich in der Ausnahmeliste: das
`updated:`-Feld fehlte **ganz** (`missing=True`) **und** zwei von sechs Fäden trugen ein
`updated: `-Präfix, für das der Rotationsanker von `rotate_index_updates.sh` blind ist. **Erst
repariert, dann der neue Faden** — weil `scripts/prepend_updated_chain.sh` ein vorhandenes
`^updated: ` **verlangt** und bei dieser Datei sonst mit exit 1 abbricht (Gegenprobe (e)). Die
sechs Fadeninhalte wurden dabei **byteweise** gegen die alte Zeile gestellt, nicht nur „sieht noch
gut aus". Der Eintrag ist **gestrichen**, nicht auf 0/0 gesetzt: mit `0, 0` wäre er eine unsichtbare
Ausnahme, deren Verschwinden kein Test bemerkt. `ROADMAP.md` (4 Fäden hinter ` · `) und die beiden
Dekumentationen (📕 bzw. abgeschlossene Phase) bleiben **bewusst** drin.

### Belege

- **`pytest`:** kein Test hinzugefügt, **keiner umgedreht** — dieser Block ändert keine Zeile
  Produktcode. Die Wächter, die den Block betreffen, sind grün: `test_acceptance_numbers.py`
  (7), `test_updated_chain.py` (7), `test_table_shape.py`, `test_doc_health.py`, `test_doc_rotations.py`
- **Tabu-Diff §0.3 leer** — `api.py`, `security.py`, `phase4_auth/`, `storage/` unberührt. Reine Doku
  plus **zwei Zeilen** in `test_acceptance_numbers.py` (zwei Bilanz-Konstanten) und **einer Zeile
  entfernt** in `test_updated_chain.py` (der Ausnahme-Eintrag)
- **Kein Deploy, kein `systemctl`, kein Tunnel, kein Portscan** — Release `v3.1.3` steht unverändert
- **Zahlen, die mitwandern:** die durchgestrichene Masse im L3-Archiv bleibt **229 B** und ist
  **kein Hebel** — der Head liegt bei ~31 KB, **unter** dem 40-KiB-Softcap. `ABNAHME_MATRIX.md` ist
  gewachsen und benennt sich damit selbst (P8-P: *benannt statt versteckt*)

### Offen, in dieser Reihenfolge

1. **Sichtprüfung der acht Bilder** — der eigentliche Abnahmeschritt des Vortags, entscheidet die
   beiden ⚠️ (P9-97 Fläche, P9-99 Textmitte). Dateinamen und Checkkriterien:
   `screenshots_latest/README.md`
2. **Deploy `v3.1.3`** (Nikinger). Badge und `## 2026-10-05`-Block stehen unverändert; dieser Block
   hat **keine** Release-Änderung gebracht. `deploy.sh` verlangt einen Datumsblock am Deploy-Tag —
   später `SHAREFYX_ALLOW_STALE_UPDATELOG=1` oder ein neuer `##`-Block
3. **P9-94 / P9-11** — der Portscan, Anleitung Mini-Plan §5 (MacBook, Firmen-VPN aus, Handy-Hotspot,
   vier Ziele). **Von keinem Test ersetzbar** und deshalb ⬜, nicht ⚠️
4. **P9-13 / V150** — zweites Claude-Konto; wandert nach P10, **kein Blocker** (Plan §0.1a)
5. **V162 *(Lesart A)*** — eine live beobachtete Löschung; kommt mit einem Deploy-Tag
6. **Gate/Z-Rest:** Übersichtsgrafik `docs/concepts/phase9_hardening_uebersicht.svg` (gerendert **und
   angesehen**), `ROADMAP`-Zeile P9 → ✅, Phase auf ✅
