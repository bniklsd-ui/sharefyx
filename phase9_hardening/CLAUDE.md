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
updated: 2026-10-06 (**die zweite Bildsichtung gebaut, opencode/M3** — Abnahme **P9-103–P9-111** mit **9 ✅**, Probe **29/29**, **Gegenläufe G7–G12 6 von 6** wirksam; **der Auftrag widerruft P9-AN und die Fläche aus P9-AO**: die Menüpunkte tragen die **Standardknopf-Fläche** statt der des Eingabefeldes (sein Wort: „they are buttons and not fields to type something in"), ausgewählt die Akzentfläche · **G11 fand eine Messlücke** (ein geschrumpfter Knopf hält dieselben Kanten) und die Station misst jetzt die Eigenbreite an einer Kopie · **sechs Wächter umgeschrieben, keiner gelöscht** · **zwei eigene Fehler, beide „die erste Regel ist nicht die, die ich meine"** · **zwei Softcap-Überschreitungen neu benannt** (Matrix **84.161 B**, settings-Plan **49.655 B** — ein Kürzen wäre Nikinger-Entscheidung); Release `v3.1.3` unverändert, **kein Deploy**) | 2026-10-05 (**V188 beantwortet, opencode/M3 — vier Quellen, eine am Repo gemessen, und der Plan-§4-Wortlaut „meines Wissens nur in Chromium" ist jetzt eine Messung: `safari: false`**; daraus **P9-27 ⬜ → ⚠️**, D1 geschlossen, **kein Code gebaut** (Nikinger-Entscheidung 2026-10-05) · **drei falsche Sätze datiert korrigiert**, darunter „der Deploy `v3.1.1` schließe P9-15, denn `health_gate.sh` macht die Läufe" — **ein Health-Gate liefert Läufe ohne Kriterium**, denn P9-15 stellt gegen 372,9 ms, und der Wert ist nie über Funnel gemessen worden (V151) · **der letzte `KNOWN_OFFENDERS`-Eintrag gestrichen** (`docs/screenshots/README.md`, zwei Ausprägungen zugleich, in zwei Schritten repariert, sechs Fadeninhalte byteweise gegengeprüft) · **zwei Zeilen** in `test_acceptance_numbers.py` (Bilanz-Konstanten), **eine entfernt** in `test_updated_chain.py` · kein Test hinzugefügt, keiner umgedreht, Tabu-Diff §0.3 leer, Release `v3.1.3` unverändert, **kein Deploy**) | 2026-10-05 (**die sieben Punkte aus der Bildsichtung gebaut, opencode/M3** — Probe **56/56**, G4 → 2 rot · G5 → 2 rot · G6 → 3 rot, `pytest` 1233 → 1238, `ui_budget` 165,6 KB; **zwei Korrekturen an der Vorgabe, beide gemessen**: `text-align` ist auf dem Flex-Knopf ein No-op → `justify-content`, und das linke Polster musste vom 32-px-Wert der Baumzeile auf `--space` (Nikinger-Entscheidung); **ein Produktbefund gemeldet, nicht gebaut** (leere Space-Liste beim zu frühen Öffnen, wandert in die P10-Liste); Release `v3.1.3` unverändert, **kein Deploy**) | 2026-10-05 (**Block settings gebaut, opencode/M3 — drei Overlays sind eine Fensterkette, V118 hat eine Linie**; Release `v3.1.3` steht, **kein Deploy, kein Service-Touch**; `pytest` 1223 → 1233, `ui_budget` 5/5, Tabu-Diff leer, Probe **39/39**, G1 → 4 rot · G2 → 2 rot · G3 → rot · **zwei Code-Befunde aus dem Browser, nicht aus den Tests** (Schmal-Modus ließ zwei Panels stehen · der „Zurück“-Knopf des Details war nicht verdrahtet) · **der Gegenlauf hat den eigenen Messaufbaum widerlegt** (er las den Frame nach dem Toggle-Zurückschalten — mit dem Fix wäre der Test grün gewesen) · P9-94 ⬜ Portscan, V188 ⬜ · **danach: sieben UI-Punkte aus der Bildsichtung notiert, nicht gebaut — Mini-Plan §10, Locks P9-AM–P9-AS, Abnahme P9-96–P9-102**) | 2026-10-05 (Block 2026-10-04 aus dem Head verbatim hierher rotiert, per `scripts/rotate_session_block.sh`)
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
| T | **Zweite Bildsichtung** (Mini-Plan §11, Locks P9-AU–P9-AZ, Abnahme P9-103–P9-111) | 🟡 **gebaut 2026-10-06 (M3)**, Release `v3.1.3` steht (unverändert), **nicht deployt** — Probe **29/29**, **Gegenläufe G7–G12 6 von 6** wirksam, `pytest` 1238 → 1246. **Der Block dreht zwei Locks des Vortags: P9-AN und die Fläche aus P9-AO sind widerrufen** — die Menüpunkte tragen die **Standardknopf-Fläche** (`--btn-std-fill`), ausgewählt die **Akzentfläche** wie `.btn-primary` (Entscheidung aus der Rückfrage), und der Abstand ist 8 px (vorher 0 px). „Ändern" ist **Vorsicht** (rot wie „Archivieren"), „Abbrechen" → **„Schließen"** · Beschriftung der Space-Zeilen bündig mit dem Titel (vorher 33 px), Namensfeld im Detail beidseitig bündig (+12 px, als **Rasterfolge**, nicht als Zahl), Anlegezeile eine Zeile (vorher 80 px Versatz) · **sechs Wächter umgeschrieben** (4 settings, 2 static_routes), **keiner gelöscht**; **Gegenlauf G11 fand eine Messlücke** (siehe Session-Block) · **zwei Softcap-Überschreitungen neu benannt** (Matrix 84.161 B, Plan 49.655 B) — Details in der `ABNAHME_MATRIX.md` unter dem Nachtrag vom 2026-10-06 |
| R | **Rückmeldung aus der Bildsichtung** (Mini-Plan §10, Locks P9-AM–P9-AS, Abnahme P9-96–P9-102) | 🟡 **gebaut 2026-10-05 (M3)**, Release `v3.1.3` steht (unverändert derselbe, nicht deployt) — Probe **56/56**, G4 → 2 rot · G5 → 2 rot · G6 → 3 rot, `pytest` 1233 → 1238 · **zwei Korrekturen an der Vorgabe, beide gemessen**: `text-align: center` war auf dem Flex-Knopf ein **No-op** (Textmitte 8,5 px daneben) → `justify-content`, und das **linke Polster** musste vom 32-px-Wert der Baumzeile auf `--space` (Nikinger-Entscheidung), sonst bleibt die Beschriftung 12 px neben der Mitte · P9-96/98/100/101/102 ✅, **P9-97 und P9-99 ⚠️ mit benannter Abweichung** · **zwei Wächter an korrektem Code rot** (Klassenreihenfolge, `hidden` im `aria-hidden`) · **ein Produktbefund gemeldet, nicht gebaut:** die Space-Liste bleibt leer, wenn man sie vor `loadOverview()` öffnet — wandert in die P10-Liste (Plan §6) · Herleitung im L3-Archiv |
| Gate/Z | Abnahme, Closeout | 🟡 **beide Doku-Hälften erledigt** (2026-10-02) · `ABNAHME_MATRIX.md` ist der **eine** Ort der Abnahme- und `[VERIFY]`-Bilanz, nicht diese Zeile · **[2026-10-04] beide Rotationen gefahren** (Block 17.780 B verbatim, Kette 6 von 7 Fäden) und diese Tabelle ins L3-Archiv gezogen ⇒ **der Head ist unter dem 40-KiB-Softcap** · **offen:** zweites Claude-Konto (P9-13/V150) · Portscan P9-94/P9-11 · Übersichtsgrafik §12.4 · Phase auf ✅ — **P9-15 steht nicht mehr hier**, es ist seit dem 2026-10-03 gemessen (⚠️, Zeile A) · Herleitung im L3-Archiv |

## Backlog (bewusst zurückgestellt, kein Phasen-Blocker)

- **„Kürzen notieren" — Nikinger-Anordnung vom 2026-10-06, nach der Sichtprüfung.** Zwei Dokumente
  stehen **über** dem 40-KiB-Softcap, und **beides ist neu**: der settings-Mini-Plan ist erst
  **durch** den Block vom 2026-10-06 darüber gekommen (§11 + §11.1 sind **10.679 B**, die
  `updated:`-Kette nur 1.205 B), die Abnahmematrix durch die neun Zeilen der zweiten Bildsichtung.
  **Gemessen, nicht geschätzt:** Plan **49.655 B** (+8.695 B), Matrix **84.161 B** (+43.201 B).
  **Nicht** gekürzt, weil ein Kürzen in ein L3-Archiv eine **Nikinger-Entscheidung** ist (P8-P) —
  und weil die beiden Dateien verschiedene Rollen haben: die **Matrix** ist der *eine* Ort der
  Abnahme- und der `[VERIFY]`-Bilanz (dorthin darf sie nicht wandern), der **Plan** trägt drei
  ausgeführte Blöcke. **Die Kandidaten, wenn er entscheidet:** (a) die §-Ergebnisabschnitte
  (§10.1–§10.3, §11.1) des Plans wandern **verbatim** in ein L3-Archiv — dieselbe Roundtrip-
  Gegenprobe wie beim Modulstatus-Split vom 2026-10-04; (b) die `updated:`-Kette des Plans rotieren
  (1.205 B, also **kein** ausreichender Hebel); (c) die **Abnahmematrix** braucht eine andere Form
  als „Zeilen", denn jede Zeile ist ein Beleg mit Ort — das ist der eigentliche Befund, und er
  gehört nicht diesem Block, sondern einer Matrix, die 116 Zeilen mit Belegen trägt.

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

## Session stopped — 2026-10-06 (sechsundzwanzigster Block: **die zweite Bildsichtung gebaut — vier Punkte, und der Auftrag hat zwei Locks vom Vortag widerrufen**; Probe **29/29**, Gegenläufe **6 von 6** wirksam. Kein Deploy, kein Service-Touch)

**Ergebnis in einem Satz.** Der Nikinger hat die vier Bilder angesehen und vier Punkte notiert
(Mini-Plan §11, Locks **P9-AU–P9-AZ**, Abnahme **P9-103–P9-111** mit **9 ✅**); **P9-AV hat P9-AN
und die Fläche aus P9-AO widerrufen** — die Menüpunkte tragen jetzt die **Standardknopf-Fläche**
statt der des Eingabefeldes (sein Wort: *„they are buttons and not fields to type something in"*),
ausgewählt die Akzentfläche. **Zwei Softcap-Überschreitungen sind neu entstanden und benannt**,
nicht versteckt.

### Was er gesagt hat — und was daraus gebaut wurde

| Punkt | Seine Worte | Gebaut | Gemessen |
|---|---|---|---|
| 01 | *„the buttons shouldn't be glued to each other"* | Wrapper `.settings-menu__list` mit `gap: var(--space)` | **8,0 / 8,0 px**, vorher **0,0**; **identisch** mit `rowGap` von `#space-admin-list` (8px) |
| 01 | *„use the unselect and select design from e.g the 'schließen', 'Space anlegen' buttons"* | unausgewählt `--btn-std-fill` + `--btn-std-line` + Innenschatten, ausgewählt `--accent-face-*` + `--accent-edge` | berechnet gegen **eingefügte Vergleichspunkte** derselben Klassen: Verlauf, Kante und Schatten **identisch** |
| 02 | *„copying the 'archivieren' Buttons style (so 'Ändern' Becomes red) … a password change is [irreversible]"* | `.btn action--caution` statt `.btn-primary` | Farbe `rgb(229,72,77)` == Vorsichtsfarbe, Fläche == Standardfläche (**keine gefüllte rote**) |
| 02 | *„change 'abbrechen' to 'schließen'"* | Text umgestellt | im Panel kein „Abbrechen" mehr, drei andere Fenster tragen dasselbe Wort |
| 03/04 | *„make 'Name' align with the selection button (currently on 'lesen' align, by adding a few pixels on the left"* | Raster `repeat(2, max-content)` + `grid-column: 1 / -1` | **0,0 px** auf **beiden** Kanten, bei 1440 **und** 1024; vorher 12 px zu schmal (sein Rundwert: +10 px) |
| 03 | *„make the text from the space buttons and the menu title align. I suggest actually moving them to the left too"* | `padding-left: 0` **im Panel** (in der Rail bleibt die Einrückung) | **1,0 px** (der Rahmen), vorher **33 px** |
| Rückfrage | Anlegezeile: Feld und „Space anlegen" **in eine Zeile**, bündig mit der Linie darüber, *„Space anlegen in seiner Größe gleich lassen"* | `flex: 1` + `nowrap` | gleiche Zeile, bündig links/rechts **1,0 px**, Knopf **142 px** == seine Eigenbreite |

**Zwei Dinge, die ich nicht getan habe, weil sie nicht sein Auftrag waren:** die Einrückung der
**Rail**-Zeilen bleibt (dort ist sie Hierarchie), und die `#space-member-list` habe ich **aus dem
Browser-Standard abgeleitet** (Disc + 40 px Einzug), **nicht gemessen** — im Wegwerf-Harness hat der
einzige eigene Space keine Mitglieder. Das steht so im Bild-README, weil es der einzige Punkt
ist, den die acht Bilder nicht tragen können.

### Sechs Wächter umgeschrieben, keiner gelöscht — und **G11 hat die Messung korrigiert**

**Die Umkehr macht Altlasten grün-rot, und die Regel ist: im selben Commit.** Fünf Wächter waren an
korrektem Code rot: zwei in `test_static_routes.py` (die Zählung der Vorsichtsklasse 2 → 3, und
„genau **ein** Knopf **mit** Fläche" → 2) und drei in `test_settings_chain.py` (Eingabefeld-Fläche,
Auswahl-Fill, `box-shadow`/`color` auf der Verbotsliste). **Keiner wurde gelöscht**, jeder trägt
beide Lesarten mit Datum im Docstring — die Widerrufene bleibt im Repo stehen, sonst wird sie zur
Grundlage der nächsten Änderung.

**Zwei eigene Fehler dieses Blocks, beide vom selben Typ (ein Wächter, der etwas anderes prüft als
er behauptet):**

1. **`_schatten_verstoss` hat an jedem Komma getrennt** und damit `rgba(255,255,255,.06)` in drei
   Stücke gerissen — der Wächter meldete **korrekten** Code als Verstoß. Jetzt `_ebenen()` mit
   Klammer-Tiefe.
2. **`_farbe_von_btn_primary` nahm `_bare_rule_bodies(".btn-primary")[0]`** — und `[0]` ist die
   **Übergangs-Sammelregel** (`.btn-primary` steht als zweiter Selektor darin), also `None`. Jetzt
   `_koerper_mit()`: der erste Body, der die Eigenschaft überhaupt nennt. **Dieselbe Falle ein
   zweites Mal** an derselben Datei, und beide Male war der Fehler „die erste Regel ist nicht die,
   die ich meine".

**Und der Gegenlauf, der eine Messlücke fand:** **G11 blieb grün.** Ohne `flex: 1` nimmt das Feld
seine Eigenbreite (194,89 px), der Knopf **schrumpft auf 127,11 px** — und die Paarbreite ist
wieder exakt die Inhaltsbreite, also bleiben **beide** Bündigkeits-Stationen grün. Der Lock aber
verlangt zusätzlich wörtlich *„Space anlegen in seiner Größe gleich lassen"*, und **das war nicht
gemessen**. Die Station misst jetzt die **Eigenbreite an einer Kopie desselben Knopfes außerhalb
der Flex-Zeile**; danach ist G11 rot. **Ein grüner Gegenlauf ist ein Befund: entweder ist der
Lock falsch oder die Messung — hier die zweite.**

### Belege

- `pytest` **1238 → 1246** (8 neue Tests, 6 umgeschrieben, **keiner gelöscht, keiner umgedreht**),
  voller Lauf grün · `ui_budget` 5/5 · Tabu-Diff §0.3 leer (`api.py`, `security.py`, `phase4_auth/`,
  `storage/` unberührt) · **reines Frontend plus eine `.html`-Zeile**
- Browser-Probe **`p9_settings_polish_probe.py` 29/29** gegen die TLS-Wegwerf-Instanz auf 18775,
  gestoppt über die PID-Datei. **Gegenläufe G7–G12: 6 von 6 wirksam** (0 → rot bei jeder Mutation).
  Ein **eigenes** Skript statt eines Umbaus, aus V187: der §10-Lauf ist der Beleg für P9-AN, und
  P9-AV hat genau diese Fläche widerrufen
- **Bilder:** `p9_settings_01..08` **neu aufgenommen** (alle acht tragen den neuen Stand),
  `screenshots_latest/` auf **acht** Symlinks rotiert (Nikinger-Anordnung: *„give me all 8"*), README
  mit einer Zeile und einem Checkkriterium je Bild. Die **Gegenlauf-Bilder sind gelöscht**,
  die sechs roten JSON-Gegenläufe liegen im Repo
- **Zwei Softcap-Überschreitungen, beide benannt:** Abnahmematrix **84.161 B** (+43.201 B über),
  settings-Mini-Plan **49.655 B** (+8.695 B über). **Der Plan ist erst durch diesen Block über den
  Cap gekommen** (§11 + §11.1 sind 10.679 B, die `updated:`-Kette nur 1.205 B) — **ein Kürzen in ein
  L3-Archiv wäre Nikinger-Entscheidung**, deshalb **gemeldet statt getan**. Der Phase-9-Head liegt
  bei ~31 KB und bleibt **unter** dem Cap; die durchgestrichene Masse im L3-Archiv bleibt **229 B**
  und ist weiterhin kein Hebel

### Nachtrag vom 2026-10-06 — die Sichtprüfung: **4 ✅, 4 neue Punkte, und alle vier sind gemessen**

Der Nikinger hat die acht Bilder angesehen: **02 · 03 · 05 · 06 freigegeben** (*„looks fine now"*
×2, *„great"*, *„yes"*), **01 · 04 · 07 · 08 mit neuen Punkten**. Diese vier sind in **§12** des
settings-Plans als Locks **P9-BA–P9-BD** mit Abnahme **P9-112–P9-115** notiert, **nicht gebaut** —
die Grundlage ist jede Zahl, die heute gemessen wurde:

- **01** *„the update-log button is still bigger … decrease its height"* — **die Höhe ist bei allen
  dreien gleich (35,69 px)** und im Bild ist **nichts ausgewählt** (0 Akzentpixel). „Bigger" heißt am
  Bild **19 px Leerraum je Seite** (Kästchen 131 px, Beschriftung 77 px). **P9-BB braucht ein Wort
  von ihm:** dieselbe Korrektur wie in 08 (Kästchen enger) oder zusätzlich flachere Knöpfe?
- **04** *„where did the space hinzufügen options go?"* — **die Optionen sind im Bild**, am
  eingecheckten PNG nachgewiesen: Standardfläche **y 207..231, x 958..1181**, „Hinzufügen"-Text
  bis x 1165, „lesen" und „Hinzufügen" auf **einer** Zeile. Sie stehen im Detail-Panel **oben**,
  weil der Mitgliederbereich leer ist (Home-Space). **Kein Defekt, ein Kriteriumfehler:** das
  Kriterium sagte nicht, wo im Bild man nachsehen soll.
- **07** *„I honestly don't see that"* — **die Ursache ist nicht die Bündigkeit, sondern das
  Scrollen:** `scrollHeight` 1417 gegen `clientHeight` 834, ein neu angehängter Eintrag landet
  **unterhalb des Sichtbereichs**. Das Bild *kann* die Zeile nicht zeigen. Bild 07 zeigt zudem nach
  dem Klick auf die erste Zeile das **Detail-Panel**, nicht die Liste — mein Checkkriterium war
  ungenau.
- **08** *„move the button borders a little bit further to the left, leave the text where it is now.
  Cut the not used space from the right"* — **gemessen:** die Menüpunkte haben 19 px, die
  **Space-Zeilen 184–239 px** Leerraum rechts bei bereits bündigem Text (P9-AX ✅). Die Korrektur
  ist damit an **beiden** Stellen dieselbe und **Text und Höhe bleiben unangetastet**.

**Und der Softcap-Posten, von ihm angeordnet: „kürzen notieren"** — siehe §Backlog.


### Offen, in dieser Reihenfolge

1. **Block „Kästchen enger" (Plan §12, Locks P9-BA–P9-BD, Abnahme P9-112–P9-115)** — vier Punkte aus
   der Sichtprüfung, **alle vier gemessen**, nichts davon gebaut. **Braucht vorher eine Antwort
   in einem Wort:** Bild 01, „bigger" heißt Leerraum, „decrease its height" passt nicht dazu
2. **Deploy `v3.1.3`** (Nikinger) — Badge und `## 2026-10-05`-Block stehen unverändert; später
   `SHAREFYX_ALLOW_STALE_UPDATELOG=1` oder ein neuer `##`-Block
3. **P9-94 / P9-11** — der Portscan, Anleitung Mini-Plan §5 (MacBook, Handy-Hotspot, vier Ziele)
4. **P9-13 / V150** — zweites Claude-Konto; wandert nach P10, **kein Blocker**
5. **Softcap: settings-Plan 49.655 B und Abnahmematrix 84.161 B** — **„kürzen notieren" ist
   angeordnet und im §Backlog notiert**; das Kürzen selbst ist Nikinger-Entscheidung
6. **Gate/Z-Rest:** Übersichtsgrafik §12.4, `ROADMAP`-Zeile P9 → ✅, Phase auf ✅
