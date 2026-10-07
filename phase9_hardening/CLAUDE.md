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
updated: 2026-10-06 (**die dritte Sichtprüfung — siebenmal ✅, ein Punkt aus Bild 08**, opencode/M3 — Abnahme **P9-120** mit **1 ✅**, Probe **50/50**, **Gegenläufe G13–G16/G18/G19 7 von 7** wirksam, `pytest` 1245 → **1246**, Release `v3.1.3` unverändert, **kein Deploy**) · **P9-BF**: die Space-Zeile trug `padding-left: 0` (P9-AX) und damit **innen 1 px links gegen 9 px rechts** — die **Folge von P9-BC**, seit das Kästchen sein Label umklammert. Gebaut `padding-left: var(--space)` **plus** `margin-left: calc(var(--space) * -1)`: allein `0` ist sein Befund, allein das Polster bricht P9-AX. Innen jetzt **9/9**, Kästchen **−8 px**, Beschriftung **1 px** bündig · **04 zurückgenommen** (*„man muss scrollen, passt so"*) · **ein Wächter neu, drei umgeschrieben**: die Kopplung wird als Formel geprüft, der Abstand-Wächter **namensgenau** statt per Substring, und **`margin-bottom` stand auf keiner Verbotsliste** — dieselbe Lücke wie `padding-block` (Vortag) und `border-box` (heute), zum dritten Mal · **alle acht Bilder neu**, **08** ist die einzige verlangte Neuerstellung | 2026-10-06 (**der Block „Kästchen enger" gebaut, opencode/M3** — Abnahme **P9-116–P9-119** mit **4 ✅**, Probe **48/48**, **Gegenläufe G13–G18 6 von 6** wirksam, `pytest` 1241 → **1245**, `ui_budget` 5/5, Tabu-Diff leer; Release `v3.1.3` unverändert, **kein Deploy**) · **der Nikinger hat den Auftrag selbst eingeschränkt** — *„nur bei Spaces verwalten, dort die Buttons der einzelnen Spaces nach Links, und das Fenster rechts verkleinern, aber nur dieses"* ⇒ **P9-BA widerrufen** (die Menüpunkte behalten 131 px) und **P9-BE** als **neuer Lock** (Fenster 338 statt 380 px, nur dieses, im Schmal-Modus zurückgenommen) · **P9-BB (b)**: Menüpunkte **flacher**, 4 px Polster, **31,69 px** statt 35,69 px · **P9-BC**: Space-Zeilen umklammern ihr Label (92–147 statt 330 px, rechts 9 statt 192–245 px, Text unverändert 1 px bündig) · **Bild 04** nennt jetzt die Position (y 205..246), **Bild 07** rollt auf (`scrollIntoView`) und nimmt die Anlegezeile mit · **vier eigene Fehler**, drei davon „eine Regel, die nicht die ist, die ich meine": `box-sizing: border-box` (min/max gelten dem **Rahmen**), `width: 100%` in der **Sammelregel**, und eine Station, die den eigenen Fehler nicht bemerkte (jetzt Feldanteil ≥ 45 %, **G18** ist er als Mutation rot) · **ein Gegenlauf blieb grün** (G17) und wurde zum Anlass, den Ausgangszustand messbar zu machen · **datierte Korrektur:** die 1246 des Vortages sind **1241** gemessen (`pytest --collect-only`) | 2026-10-06 (**die zweite Bildsichtung gebaut, opencode/M3** — Abnahme **P9-103–P9-111** mit **9 ✅**, Probe **29/29**, **Gegenläufe G7–G12 6 von 6** wirksam; **der Auftrag widerruft P9-AN und die Fläche aus P9-AO**: die Menüpunkte tragen die **Standardknopf-Fläche** statt der des Eingabefeldes (sein Wort: „they are buttons and not fields to type something in"), ausgewählt die Akzentfläche · **G11 fand eine Messlücke** (ein geschrumpfter Knopf hält dieselben Kanten) und die Station misst jetzt die Eigenbreite an einer Kopie · **sechs Wächter umgeschrieben, keiner gelöscht** · **zwei eigene Fehler, beide „die erste Regel ist nicht die, die ich meine"** · **zwei Softcap-Überschreitungen neu benannt** (Matrix **84.161 B**, settings-Plan **49.655 B** — ein Kürzen wäre Nikinger-Entscheidung); Release `v3.1.3` unverändert, **kein Deploy**) | 2026-10-05 (**V188 beantwortet, opencode/M3 — vier Quellen, eine am Repo gemessen, und der Plan-§4-Wortlaut „meines Wissens nur in Chromium" ist jetzt eine Messung: `safari: false`**; daraus **P9-27 ⬜ → ⚠️**, D1 geschlossen, **kein Code gebaut** (Nikinger-Entscheidung 2026-10-05) · **drei falsche Sätze datiert korrigiert**, darunter „der Deploy `v3.1.1` schließe P9-15, denn `health_gate.sh` macht die Läufe" — **ein Health-Gate liefert Läufe ohne Kriterium**, denn P9-15 stellt gegen 372,9 ms, und der Wert ist nie über Funnel gemessen worden (V151) · **der letzte `KNOWN_OFFENDERS`-Eintrag gestrichen** (`docs/screenshots/README.md`, zwei Ausprägungen zugleich, in zwei Schritten repariert, sechs Fadeninhalte byteweise gegengeprüft) · **zwei Zeilen** in `test_acceptance_numbers.py` (Bilanz-Konstanten), **eine entfernt** in `test_updated_chain.py` · kein Test hinzugefügt, keiner umgedreht, Tabu-Diff §0.3 leer, Release `v3.1.3` unverändert, **kein Deploy**) | 2026-10-05 (**die sieben Punkte aus der Bildsichtung gebaut, opencode/M3** — Probe **56/56**, G4 → 2 rot · G5 → 2 rot · G6 → 3 rot, `pytest` 1233 → 1238, `ui_budget` 165,6 KB; **zwei Korrekturen an der Vorgabe, beide gemessen**: `text-align` ist auf dem Flex-Knopf ein No-op → `justify-content`, und das linke Polster musste vom 32-px-Wert der Baumzeile auf `--space` (Nikinger-Entscheidung); **ein Produktbefund gemeldet, nicht gebaut** (leere Space-Liste beim zu frühen Öffnen, wandert in die P10-Liste); Release `v3.1.3` unverändert, **kein Deploy**) | 2026-10-05 (**Block settings gebaut, opencode/M3 — drei Overlays sind eine Fensterkette, V118 hat eine Linie**; Release `v3.1.3` steht, **kein Deploy, kein Service-Touch**; `pytest` 1223 → 1233, `ui_budget` 5/5, Tabu-Diff leer, Probe **39/39**, G1 → 4 rot · G2 → 2 rot · G3 → rot · **zwei Code-Befunde aus dem Browser, nicht aus den Tests** (Schmal-Modus ließ zwei Panels stehen · der „Zurück“-Knopf des Details war nicht verdrahtet) · **der Gegenlauf hat den eigenen Messaufbaum widerlegt** (er las den Frame nach dem Toggle-Zurückschalten — mit dem Fix wäre der Test grün gewesen) · P9-94 ⬜ Portscan, V188 ⬜ · **danach: sieben UI-Punkte aus der Bildsichtung notiert, nicht gebaut — Mini-Plan §10, Locks P9-AM–P9-AS, Abnahme P9-96–P9-102**) | 2026-10-05 (Block 2026-10-04 aus dem Head verbatim hierher rotiert, per `scripts/rotate_session_block.sh`)
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
| U | **„Kästchen enger“ — die dritte Bildsichtung** (Mini-Plan §12.1, Locks P9-BB/BC/BD/**BE**, Abnahme **P9-116–P9-119**) | 🟡 **gebaut 2026-10-06 (M3)**, Release `v3.1.3` steht (unverändert), **nicht deployt** — Probe **48/48**, **Gegenläufe G13–G18 6 von 6** wirksam, `pytest` 1241 → **1245**. **Der Nikinger hat den Auftrag selbst eingeschränkt:** *„nur bei Spaces verwalten … aber nur dieses“* ⇒ **P9-BA widerrufen** (die Menüpunkte behalten ihre 131 px) und **P9-BE** als **neuer** Lock entstanden (Fenster verkleinern). Menüpunkte **flacher** (b): 4 px Polster, **31,69 px** statt 35,69 px · Space-Zeilen **umklammern ihr Label** (92–147 px statt 330 px, rechts 9 statt 192–245 px, Text 1 px bündig) · **Spaces-Fenster 338 statt 380 px**, Feld 138 px von 288 px Inhalt, Knopf 142 px, im Schmal-Modus zurückgenommen (422 px) · Bild 04 nennt jetzt die **Position** (y 205..246), Bild 07 **rollt auf** (`scrollIntoView`) und nimmt die Anlegezeile mit · **vier eigene Fehler**, drei davon „eine Regel, die nicht die ist, die ich meine“ (`box-sizing: border-box`, `width: 100%` in der **Sammelregel**, eine Station, die den eigenen Fehler nicht bemerkte) · **ein Gegenlauf blieb grün** (G17) und wurde zum Anlass, den Ausgangszustand messbar zu machen · **P9-112 widerrufen**, P9-113/114/115 abgelöst (Zuordnung in der Matrix) · **[2026-10-06 Nachsatz, Lock P9-BF, Abnahme P9-120 ✅]:** **dritte Sichtprüfung — siebenmal ✅, ein Punkt aus Bild 08**: die Space-Zeile hält innen wieder den Standardabstand (**9 px links wie rechts**, vorher 1 gegen 9), gebaut als `padding-left: var(--space)` **plus** `margin-left: calc(var(--space) * -1)` — beide Locks halten nur zusammen; der Einwand zu Bild 04 ist am selben Tag zurückgenommen („man muss scrollen“). Probe **50/50**, **Gegenläufe 7 von 7**, `pytest` 1246 — Details im Session-Block und in der `ABNAHME_MATRIX.md` |
| Gate/Z | Abnahme, Closeout | 🟡 **beide Doku-Hälften erledigt** (2026-10-02) · `ABNAHME_MATRIX.md` ist der **eine** Ort der Abnahme- und `[VERIFY]`-Bilanz, nicht diese Zeile · **[2026-10-04] beide Rotationen gefahren** (Block 17.780 B verbatim, Kette 6 von 7 Fäden) und diese Tabelle ins L3-Archiv gezogen ⇒ **der Head ist unter dem 40-KiB-Softcap** · **offen:** zweites Claude-Konto (P9-13/V150) · Portscan P9-94/P9-11 · ~~Übersichtsgrafik §12.4~~ ✅ **2026-10-07** (`docs/concepts/phase9_hardening_uebersicht.svg`, gerendert und angesehen, Sonnet 5.5/Claude Code) · Phase auf ✅ (wartet nur noch auf den Portscan; **`v3.1.3` live seit 2026-10-07, Gate 9/9**; **2026-10-07:** `## 2026-10-05` im `UPDATE_LOG` auf `## 2026-10-07` datiert, damit das Update-Log-Gate ohne `ALLOW_STALE` greift) — **P9-15 steht nicht mehr hier**, es ist seit dem 2026-10-03 gemessen (⚠️, Zeile A) · Herleitung im L3-Archiv |

## Backlog (bewusst zurückgestellt, kein Phasen-Blocker)

- **„Kürzen notieren" — Nikinger-Anordnung vom 2026-10-06, nach der Sichtprüfung.** Zwei Dokumente
  stehen **über** dem 40-KiB-Softcap, und **beides ist neu**: der settings-Mini-Plan ist erst
  **durch** den Block vom 2026-10-06 darüber gekommen (§11 + §11.1 sind **10.679 B**, die
  `updated:`-Kette nur 1.205 B), die Abnahmematrix durch die neun Zeilen der zweiten Bildsichtung.
  **Gemessen, nicht geschätzt** — und **seit dem 2026-10-06 weiter gewachsen**, weil der Block
  „Kästchen enger“ (Plan §12.1, Matrix) beide Dateien wieder verlängert hat: Plan **61.237 B**
  (+19.754 B seit der ersten Meldung), Matrix **92.601 B** (+51.702 B).
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

## Session stopped — 2026-10-06 (achtundzwanzigster Block: **die dritte Sichtprüfung — siebenmal ✅, ein Punkt aus Bild 08 (Lock P9-BF)**; Probe **50/50**, **Gegenläufe 7 von 7**. Kein Deploy, kein Service-Touch)

**Ergebnis in einem Satz.** Der Nikinger hat die acht Bilder angesehen: **01 · 02 · 03 · 05 · 06 · 07
freigegeben**, **04 mit einem Einwand, den er am selben Tag zurücknahm** (*„ah, nehme 04 zurück,
man muss scrollen. Passt so"*), und **08 mit genau einem Punkt** — daraus ein **neuer Lock P9-BF**
und die Abnahme **P9-120**.

| Bild | Urteil |
|---|---|
| 01 | ✅ *„passt"* — die Menüpunkte sind **31,69 px** hoch statt 35,69 px |
| 02 | ✅ *„sieht für mich passend aus"* |
| 03 | ✅ *„sieht gut aus"* |
| 04 | ✅ *„ja"* — der erste Einwand zurückgenommen (die Bedienzeile der Members liegt unterhalb, man scrollt) |
| 05 | ✅ *„yo, passt"* |
| 06 | ✅ *„identisch zu 1, passt"* |
| 07 | ✅ *„passt so"* — das **aufgerollte** Bild mit der neuen Zeile **und** der Anlegezeile |
| 08 | **ein Punkt → gebaut** (siehe unten); dieses Bild ist die **einzige** verlangte Neuerstellung |

### P9-BF: „ein paar Px nach links erweitern, damit der Text innen wieder den Standardabstand hält"

**Gemessen vorher:** innen **1 px links** gegen **9 px rechts** — die Beschriftung klebte an der
linken Kästchenkante. **Das ist die Folge von P9-BC**: bei 330 px Breite fiel der linke Rand nie auf,
und seit das Kästchen sein Label umklammert (92–155 px), **ist** die linke Innenkante sichtbar. Der
Befund ist damit **genau die Kehrseite des Locks vom Vortag** — und er wäre nur sichtbar geworden,
weil die Bilder neu aufgenommen wurden.

**Gebaut:** `padding-left: var(--space)` **plus** `margin-left: calc(var(--space) * -1)` an
**derselben** Kante. **Warum beides, und nicht eines:** `padding-left: 0` allein ist sein Befund;
`padding-left: var(--space)` allein schiebt die Beschriftung **8 px nach rechts** und bricht **P9-AX**
(die Beschriftung gehört auf dieselbe Kante wie der Panel-Titel). Nur Polster **und** negativer
Außenabstand in derselben Höhe bewegen das **Kästchen**, nicht den Text.

**Gemessen nachher:** innen **9 px links wie rechts**, das Kästchen ragt **−8 px** in das 24-px-
Panelpolster (ohne abgeschnitten zu werden), die Beschriftung bleibt **1,0 px** bündig mit dem Titel.

### Wächter: einer neu, drei umgeschrieben, keiner gelöscht — **und dieselbe Lücke zum dritten Mal**

1. **Neu:** `test_the_space_rows_keep_the_standard_gap_inside_on_both_sides()` prüft die **Kopplung**
   als Formel (`margin-left == -(padding-left)`), nicht als zwei Zahlen. Zwei unabhängige Werte wären
   zwei Locks — die Kombination ist der Punkt.
2. **Der Abstand-Wächter prüft jetzt namensgenau.** Vorher stand dort `assert "margin" not in body` —
   und die Zeile trägt seit P9-BF einen **negativen** `margin-left`. Ein Substring-Test hätte den
   Lock **verboten statt geprüft**: er kannte „irgendwo ein margin", nicht **welches** und nicht
   **mit welchem Wert**.
3. **`margin-bottom` stand auf keiner Verbotsliste**, obwohl der Test behauptete, er würde es melden —
   die Liste wird namensgenau geprüft, und `margin\s*:` matcht `margin-bottom` nicht. **Dieselbe
   Lücke wie `padding-block` (Vortag) und `border-box` (heute früh)**: eine Eigenschaft, die kein
   Wächter kennt, meldet kein Wächter. Die drei `margin`-Langformen stehen jetzt auf der Liste.
4. **Die Station P9-117 rechnet jetzt beide Polster** — sie kannte nur `padR`, weil links `0` stand.
   Dieselbe Lücke ein drittes Mal, diesmal an der Formel statt an der Regel.

**Belege:** Probe `p9_settings_kastchen_probe.py` **50/50**, **Gegenläufe G13–G16, G18, G19 7 von 7
wirksam** (`g19` ist P9-BF als Mutation: `padding-left` zurück auf `0`), `pytest` 1245 → **1246**
(+1), `ui_budget` 5/5, Tabu-Diff §0.3 leer, Release `v3.1.3` **unverändert**, **kein Deploy**.
**Die durchgestrichene Masse im L3-Archiv bleibt 229 B** und ist weiterhin kein Hebel; der Head liegt bei ~32 KB und bleibt **unter** dem Cap. **Acht Bilder neu aufgenommen**, davon ist **08** die verlangte.

### Offen, in dieser Reihenfolge

1. ~~**Deploy `v3.1.3`**~~ ✅ **live seit 2026-10-07** (Nikinger; Release `20261007T095118.935939Z`, SHA `bb400d7f13ae133642ada480e9a02c35f2737937`, vorher `20261005T101727.915085Z`; `deploy.sh` 1246 passed, `health_gate.sh --expected-version=v3.1.3 --require-todays-update-log --expected-sha=bb400d7…` **9/9 OK**, Ausgabe vom Nikinger eingefügt). Ursprünglich: Badge und `## 2026-10-05`-Block stehen unverändert; dieser Block hat
   nichts am Release geändert, später `SHAREFYX_ALLOW_STALE_UPDATELOG=1` oder ein neuer `##`-Block
2. **P9-94 / P9-11** — der Portscan (MacBook, Handy-Hotspot, vier Ziele, Mini-Plan §5)
3. **P9-13 / V150** — zweites Claude-Konto; wandert nach P10, **kein Blocker**
4. **Softcap: settings-Plan 64.996 B und Abnahmematrix 95.152 B** — „kürzen notieren" ist angeordnet
   und im §Backlog notiert; das Kürzen selbst ist Nikinger-Entscheidung
5. **Gate/Z-Rest:** ~~Übersichtsgrafik §12.4~~ **erledigt 2026-10-07** (Sonnet 5.5/Claude Code übernimmt den Abschluss nach dem MiniMax-Ausfall; Grafik 1080×740, gerendert und angesehen, Titel-Überlappung mit dem Zähler-Badge gefunden und behoben) · `ROADMAP`-Zeile P9 → ✅ und Phase auf ✅ **erst nach 1 + 2** (Entscheidung Nikinger: oder jetzt schließen und beide als ⬜ mit Termin führen)
