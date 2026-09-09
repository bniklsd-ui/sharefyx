---
status: snapshot
purpose: Abschluss-Handover P8.5 → P8.6 — Status, Delta seit dem P7-Handover (P8 hatte keines), Abnahmestand, offene Entscheidungen, [VERIFY]-Bilanz V95–V105, zwei umgekehrte Locks
read-when: vor der Planung von Phase 8.6 einmal ganz lesen — ersetzt das Nachlesen der Phase-8- und Phase-8.5-Heads für alles außer der Detailhistorie
detail: L2
up: ../../ROADMAP.md
down:
  - ./phase8_5_picker_release_plan.md               # §9 = der kanonische Closeout, N1–N7 + P8.5-A–P8.5-T in §0.1/§0.2
  - ./phase8_ui_graph_plan.md                       # Phase-8-Closeout in §9 (P8-N, kein eigenes Handover)
  - ../../phase8_5_picker_release/CLAUDE.md         # Modul-Status, Abnahmestand, aktueller Session-Block
  - ../../phase8_5_picker_release/SESSIONS_ARCHIVE.md  # volle Phasenhistorie + Abnahmematrix-Archiv, verbatim
  - ./p8x_ui_polish_notes.md                        # Themen-Sammlung für P8.6, §1–§10 + Anhang; §10 = Feedback 2026-09-09
  - ./sichtpruefung_automation_conventions.md       # Statusregel + vier Sichtungs-Konventionen §1–§4
  - ./PHASE7_CLOSEOUT_HANDOVER.md                   # Vorgänger; alles dazwischen liegt in den beiden Plan-§9
updated: 2026-09-09
---
# Phase 8.5 — Closeout-Handover (P8.5 → P8.6)

> **Für den kalten Leser, ohne Beschönigung.** Phase 8.5 ist **live deployt**
> (`main`@`6f19a8f`, Release `20260905T140325.378914Z`, Badge `v3.0.1`, Service-PID 355956)
> und **✅ vollständig verifiziert**: **20 von 20** Abnahmezeilen. Sie schließt **Phase 8
> formal mit ab** (N6/P8.5-R) — Phase 8 steht bei **26 von 26**. Das ist der erste
> Handover seit P7; Phase 8 hat keinen, weil P8-N „ein Dokument pro Phase" festlegt und
> ihr Closeout in `phase8_ui_graph_plan.md` §9 steht.

> **Dieser Handover ist kein zweiter Plan.** Der kanonische Closeout ist
> `phase8_5_picker_release_plan.md` **§9**. Hier steht nur, was die P8.6-Planung wissen
> muss, bevor sie den ersten Absatz schreibt.

---

## 1 Status in fünf Sätzen

1. **Die drei Phase-8-Restdefekte sind zu.** §9.4.2 (Picker füllte nur `links:`) ist ein
   Modus-Umschalter im Dialog geworden, §9.4.3 (keine Tastaturnavigation) ein
   `aria-activedescendant`-Muster ohne `tabindex`, §9.4.1 (`itm_…`-ID rutscht in
   Klammer-/Aufzählungs-Kontexten durch) ein generalisierter Hint-Text **plus einer
   schriftlichen Abbruchregel**, die eine fünfte Runde von vornherein ausschließt.
2. **Der v3-Build ist ausgeliefert.** Block C fuhr 13 Stationen × 2 Browser = **26/26**
   gegen eine Wegwerf-Instanz, bevor irgendetwas live ging; D2 war eine Nikinger-Aktion
   (Hard Rule 9), D3 lief mit einem neuen `health_gate.sh` **8/8** grün.
3. **Mitten in der Phase hat sich die Statusregel geändert.** Seit 2026-09-08 zählt eine
   vom Nikinger geprüfte Wegwerf-Instanz-Automatisierung als „live-verifiziert" — die
   Wegwerf ist byte-identischer Git-Checkout, Unterschied nur `DATA_ROOT`/`auth.sqlite3`/
   Identität. Das ist der Grund, warum P8 von 15/9/2 auf 26/0/0 und P8.5 auf 20/0/0 kam,
   ohne dass eine Zeile Code dafür geschrieben wurde. Herleitung:
   `sichtpruefung_automation_conventions.md`.
4. **Ein Befund wurde bewusst gemessen und nicht gefixt:** V102 — eine Body-Kante und eine
   Frontmatter-Kante zwischen denselben zwei Knoten zeichnen **zwei** Linien. Das war so
   geplant (§0.4 DRAUSSEN, „nur messen") und ist jetzt der Kopfpunkt in §4.1.
5. **Kein Code-Touch im Tabu-Bereich über die gesamte Phase.** `storage/`, `authserver/`,
   `webui/{security,api,serializers,permissions}.py` sind unangetastet; die einzige
   erlaubte Zeile war der Beschreibungstext `_TITLE_NOT_ID_HINT`. Keine neunte
   P1-Contract-Öffnung.

---

## 2 Delta seit dem P7-Handover

Zwei Phasen liegen dazwischen. **Phase 8** ist in `phase8_ui_graph_plan.md` §9.2 tabellarisch
abgehandelt (Reauth-Grant, `remove-space`-Auto-Reindex, achte P1-Contract-Öffnung mit
`linkscan.py` + `item_links` + `GET /api/v1/graph`, Design-Fundament v3 mit Plex/Lucide/
Farbsemantik/Glass, tabellose Übersicht, handgerollter Canvas-Force-Graph) — **das wird hier
nicht wiederholt.** Nur der Phase-8.5-Anteil:

| Was | Wo | Bemerkung |
|---|---|---|
| Picker-Modus-Umschalter (Body / Kante) | `webui/static/js/dialogs.js`, `app.html`, `app.css` | `499d9be`; Moduswahl in `localStorage["sfx:linkpicker:mode"]` — **erste `localStorage`-Nutzung des Projekts** (V99-Korrektur, siehe §5) |
| `insertAtCursor` auf Modulebene gehoben | `webui/static/js/editor.js` | `499d9be`; **eine** Implementierung, keine zweite Kopie (P8.5-I) |
| Tastaturnavigation + `_pickLinkPickerAt` | `dialogs.js`, `app.css` | `7ce0be0`; ein Auswahlpfad für Maus und Enter, `app.js` unangetastet (P8.5-L) |
| `_TITLE_NOT_ID_HINT` generalisiert | `phase2_mcp/mcpserver/tools.py` (nur Beschreibungstext) | `5fee41e`; einzige Tabu-Ausnahme der Phase, Präzedenz P7-T/P8-§0.4 |
| Bracket-Renderer-Fix | `webui/static/js/markdown.js` | `14dcc3c`; Link-/Bild-Regex in `inlineMarkdown()` toleriert `\[`/`\]` als Escape-Einheit — ein Titel mit eckigen Klammern brach vorher die Vorschau |
| Radiogruppe statt `<select>` | `app.html`, `app.css`, `dialogs.js`, `phase5_ui/tests/test_static_routes.py` | `14dcc3c`; **am selben Tag vom Nikinger wieder umgekehrt** — siehe §4.2 |
| Badge `v3.0` → `v3.0.1` + UPDATE_LOG-Block | `app.html:20`, `docs/UPDATE_LOG.md` | `6f19a8f`; `deploy.sh` verlangt strikt ein tagesaktuelles Datum im obersten Log-Block |
| `health_gate.sh` (8 Gates) | `phase8_5_picker_release/scripts/` | `59d9bc3`; Lauf 2026-09-05 15:19:53Z **8/8** gegen den frischen Deploy |
| Wegwerf-Setup + Smokes | `phase8_5_picker_release/scripts/` | `v3_ritt_playwright_smoke.py` (~720 Z.), `p8519_radiogroup_probe.py`, `p856_bracket_mini_smoke.py`; 16 + 2 Screenshots unter `docs/screenshots/` |
| Zwei neue Konventions-Dokumente | `docs/concepts/sichtpruefung_automation_{conventions,tooling}.md` | `6b9c7e0` + `e4c9834`; Statusregel-Herleitung + vier Sichtungs-Konventionen §1–§4 |

**Deploy-Stand:** live seit 2026-09-05, PID **355956**, Uptime 3 Tage zum Zeitpunkt dieses
Handovers. Seit dem Deploy **kein** Service-Touch aus einer Agenten-Session.

---

## 3 Abnahmestand

**20 ✅ · 0 🟡 · 0 ⬜** von 20 (Art: 8× (C) Code/Test, 8× (W) Wegwerf-Instanz, 4× (L) nur
live). Die kanonische Tabelle mit Beleg, Commit-SHA, Screenshot-Verweis und
Nikinger-Sichtungsvermerk pro Zeile steht in
`phase8_5_picker_release/SESSIONS_ARCHIVE.md` §Abnahmematrix-Archiv — **hier nicht
dupliziert.**

Zwei Zeilen brauchen eine Erläuterung, damit sie nicht falsch gelesen werden:

- **P8.5-19 ist ✅ und gleichzeitig überholt.** Der Nikinger hat am 2026-09-06 die
  Radiogruppe angeordnet („deutlich angenehmer"), sie wurde gebaut und verifiziert — und
  am 2026-09-08 hat er die eigene Entscheidung zugunsten der Konventions-Konsistenz wieder
  umgekehrt. Die Zeile bleibt ✅ (die Frage „welche Bauform?" *wurde* beantwortet), trägt
  aber den Supersession-Marker. Rückbau ist P8.6-Arbeit, §4.2.
- **P8.5-6 war die letzte 🟡-Zeile und ist am 2026-09-09 gefallen**, nachdem die neue
  Konvention §1 („Vorschau-Pflicht bei klickbaren Links") einen Screenshot des
  *gerenderten* Links verlangte statt nur der Markdown-Quelle. Der Mini-Smoke
  `p856_bracket_mini_smoke.py` liefert ihn.

**Phase 8** steht bei **26 ✅ · 0 🟡 · 0 ⬜** (Zählung maschinell, `awk`-Kommando im
Phase-8-Head — der Zähler war dreimal von Hand gedriftet, das war der Fix dagegen).

---

## 4 Offene Entscheidungen für die Planung von Phase 8.6

### 4.1 V102 — Zwillingskante zeichnet zwei Linien (Kopfpunkt)

Body-Link und Frontmatter-Eintrag zwischen denselben zwei Knoten erzeugen zwei Einträge in
`item_links` mit `kind='body'` bzw. `kind='frontmatter'`; `_graph_get` und `graph.js`
zeichnen beide. Gemessen in Block C an `Buecherliste Q4` ↔ `Empfehlungen Nikinger`.
**Kein Bug, sondern eine fehlende Entscheidung:** `index.py :: replace_item_links` hat kein
Cross-`kind`-Dedup, und Phase 8.5 durfte es nicht einbauen (`storage/` steht unter Tabu, und
§0.4 sagte ausdrücklich „nur messen").

**Zu entscheiden:** dedupliziert der Server (`storage/` — das wäre die **neunte**
P1-Contract-Öffnung, aktuell nicht angekündigt), dedupliziert `graph.js` beim Zeichnen
(reiner Frontend-Schnitt, kein Contract), oder bleiben zwei Linien absichtlich stehen, weil
sie zwei echte Beziehungen abbilden? Die Frontend-Variante ist die billigste und rührt
keinen Contract an — sie ist der Vorschlag, nicht der Lock.

### 4.2 Radiogruppe zurück auf `<select>` — der Nikinger dreht seine eigene Entscheidung

Angeordnet 2026-09-08, umzusetzen in P8.6. Betroffen: `app.html` (`<fieldset>` + 2×
`<input type="radio">` → `<select id="link-picker-mode">`), `dialogs.js` (Selektor),
`app.css` (Radiogruppen-Block raus), `phase5_ui/tests/test_static_routes.py`
(`test_link_picker_uses_a_radio_group_not_a_select` **umkehren und umbenennen** — der
Testname wird sonst zur Lüge). Neu gegenüber der ursprünglichen `<select>`-Fassung: die
Beschriftung soll **in** der Box stehen, nicht als externes `<label>` daneben. Volle
Vormerkung im Phase-8.5-Head §Vormerkung.

### 4.3 CSRF-Origin-Mismatch macht Wegwerf-Instanzen für POST-Pfade blind

`webui/security.py :: require_csrf` erwartet die `Origin` aus `SPACE_PUBLIC_BASE_URL`, und
`authserver/config.py :: _validate_base_url` erzwingt dort `https://`. Eine Wegwerf auf
`http://127.0.0.1:18773` sendet also immer die falsche Origin — **jeder `fetch()` mit
POST/PATCH aus dem Browser-Kontext wird abgewiesen.** Konsequenz in Block C: Station 13
(Reauth-Grant) war nur strukturell prüfbar. Das ist eine **Setup-Frage, kein Server-Bug**;
zu entscheiden ist, ob künftige Wegwerf-Setups einen Reverse-Proxy mit TLS-Terminierung
bekommen oder ob POST-Pfade weiter live-only bleiben.

### 4.4 P8.6-Inhalt: zehn Abschnitte, davon einer neu

`docs/concepts/p8x_ui_polish_notes.md` ist die Sammelquelle — **zehn Abschnitte §1–§10** plus
Anhang §A–§E. (Ältere Doku sprach von „16 Themen"; die Zahl war seit §8/§9 stale und ist am
2026-09-09 überall auf die Abschnittszählung umgestellt.)
**Neu am 2026-09-09 (§10):** neun Nikinger-Feedback-Punkte aus dem Closeout-Prompt —
einheitliche Ecken-Radien für alle Icons, Hover-Auswahl als transparentere Standardauswahl,
Ordner-/Tags-Auswahl auf den Standard, klickbare Spaces in der Übersicht, das gesamte
Einstellungsmenü auf den Standard, **alles Klickbare** auf dasselbe Design (mit „Abmelden"
und „Archivieren" als bewusste Farbausnahme), verbundene AI-Sessions in den Einstellungen
und die Hochkant-/Handy-UI. Sieben davon sind Verschärfungen von §5 (Layering) und §6
(Settings) — **kein neuer Cluster, sondern die konkrete Ausformung eines bereits notierten**.
Die Planungs-Session sollte §5 und §10 zusammen lesen.

**Nikinger-Vorgabe, unverändert:** erster Punkt in P8.6 ist die Installation des
OpenCode-Vision-Plugins (`DavidEasden/opencode-vision`, siehe
`sichtpruefung_automation_tooling.md`) — nicht Teil der UI-Politur, aber bewusst früh, damit
die nächste Sichtungsrunde Screenshots direkt im Chat zeigen kann (Konvention §4).

### 4.5 Zwei Nummerierungs-Fragen, die niemand still entscheiden sollte

- **„v3.1 also p8.7".** Der Nikinger ordnet die AI-Sessions-Anzeige in seinem Feedback
  „eher v3.1 also p8.7" ein. Die Dokumente kennen aber **kein P8.7**: dort steht P8.6 →
  `v3.0.2` und P9 → `v3.1.0`. Entweder ist „p8.7" ein neuer Zwischenschritt, oder es meint
  das, was heute P9 heißt. **Nicht raten** — in der Planungs-Session klären; solange
  unklar, ist der Punkt in `p8x_ui_polish_notes.md` §10 unter dem Zitat des Nikinger
  abgelegt, ohne dass etwas umbenannt wurde.
- **Verzeichnisname.** `p8x_ui_polish_notes.md` §D lässt `phase9_ui_polish/` und
  `phase8_x_ui_polish/` offen; die Phase heißt inzwischen durchgehend P8.6. Der
  Verzeichnisname ist damit vermutlich `phase8_6_ui_polish/`, ist aber nirgends gelockt.

### 4.6 Mobile/Hochkant ist keine Außenkante mehr

`p8x_ui_polish_notes.md` §B und der ROADMAP-Abschnitt „Phase 8.X" führten **„Mobile/Realtime"
bisher als bewusst draußen**. Der Nikinger hat das am 2026-09-09 für die Mobile-Hälfte
aufgehoben: die Hochkant-/Handy-Ansicht soll als wichtiges Zukunfts-Item notiert sein, damit
eine spätere, freiere Phasenplanung sie berücksichtigt. **Realtime bleibt draußen.** Beide
Stellen tragen jetzt die durchgestrichene Altfassung plus datierte Notiz — die Aufhebung ist
eine benannte Entscheidung, kein stilles Verschwinden.

### 4.7 Geerbtes Ledger — unverändert offen

Die P6-Zeilen 7/9/14–17/23/25/29/30, P6.5-14, O4/O5/O7, `_trash/`-Räumung, die
Glyph-Entscheidungen P6/P6.5, FastMCP-4 (**V79**, eigene Mini-Phase per P5-C), Q1
(Body-Volltextsuche), P6-M (Rechteverwaltung über MCP-Tools), F2 (Löschen von Items) und der
Funnel-Watchdog stehen unverändert. Phase 8.5 hat davon nichts angefasst und nichts still
abgeräumt. Quelle: `phase8_ui_graph_plan.md` §9.4.5.

---

## 5 `[VERIFY]`-Bilanz V95–V105

| # | Frage | Ergebnis |
|---|---|---|
| V95 | Sammelmarker: alle `Datei:Zeile`-Anker gegen `main`@`6272cad` | ✅ gehalten — kein Anker-Drift-Fund über die Phase |
| V96 | pytest-Ausgangsstand real 959? | ✅ **959 passed** in Step 0 gemessen; heute 964 |
| V97 | `ui_budget.py` 125.8/250 KB, 5/5 grün? | 🟡 **teilweise** — Step 0 hat es als „irrelevant" übersprungen; gelaufen erst 2026-09-08 (**5/5 im Zielkorridor**, `dialogs.js` 12.6 → 13.2 KB). Die Ausgangszahl 125.8 KB wurde nie gegengeprüft |
| V98 | Port 18773 frei? | ✅ ja, C1 hat ihn belegt |
| V99 | Nutzt das Projekt `localStorage`? | ❗ **korrigiert** — nein. Der Plan tippte auf `sfx:draft:`, das ist aber `sessionStorage`. `localStorage` ist eine **Eskalation** gegenüber der Projekt-Konvention, gerechtfertigt durch P8.5-G, im Code dokumentiert (`dialogs.js:107`, `185-191`) |
| V100 | `insertAtCursor` anderswo geshadowed? | ✅ nein — per statischem Test P8.5-9 belegt |
| V101 | `role="combobox"` + `aria-activedescendant` in Chromium **und** Firefox | ✅ beide; Station 7 grün 13/13 + 13/13 |
| V102 | Eine Linie oder zwei? | ❗ **zwei** (`kinds=['body','frontmatter']`), kein Cross-`kind`-Dedup → **benannter Befund, §4.1** |
| V103 | `deploy.sh` geändert? `sudo`-Prompt sichtbar im Vordergrund? | ⬜ **unbeantwortet** — D2 lief still durch den Nikinger zwischen D1 und D3; der Deploy ist nachweislich gelungen (Release-Stempel, PID, Badge), die Prompt-Beobachtung selbst wurde nie protokolliert |
| V104 | Playwright-MCP unter opencode noch verbunden? | ⬜ **gegenstandslos** — Block C lief als geschriebenes Playwright-Skript (`v3_ritt_playwright_smoke.py`), nicht über MCP; die Frage hat sich nicht gestellt |
| V105 | Verbindet der echte Anthropic-Connector nach dem Deploy? | ✅ ja, 2026-09-08 — `list_spaces` lieferte die vier echten Spaces, dazu ein echter claude.ai-Chat des Nikingers über denselben Connector |

**Kurzfassung: 8 beantwortet, davon 2 mit einem anderen Ergebnis als erwartet (V99, V102).
Drei offen — V97 halb, V103 nie beobachtet, V104 gegenstandslos.** Keiner der drei ist ein
Blocker für P8.6; V103 sollte beim nächsten Deploy einfach mitprotokolliert werden.

---

## 6 P1-Contract

Die **achte** Öffnung (`linkscan.py`/`item_links`/`Store.links_all`/`GET /api/v1/graph`) ist
seit dem 2026-09-02 geschlossen (`phase8_ui_graph_plan.md` §9.6). Phase 8.5 hat **keine
neunte** geöffnet und keine angekündigt — der Tabu-Diff über `storage/` war über die gesamte
Phase leer. **Achtung für P8.6:** die V102-Server-Variante aus §4.1 *wäre* die neunte
Öffnung. Wer sie will, kündigt sie in der Planung an, statt sie beim Bauen zu entdecken.

---

## 7 Zwei Locks, die dieser Closeout bewusst umkehrt

Beide standen seit dem 2026-09-03 in `phase8_5_picker_release_plan.md` §0.2 und sind am
2026-09-09 vom Nikinger im Closeout-Auftrag selbst aufgehoben worden. Beide tragen dort
jetzt eine durchgestrichene Altfassung plus datierte Korrekturnotiz:

- **P8.5-S** („keine Übersichtsgrafik für Phase 8.5") → die Grafik existiert:
  `docs/concepts/phase8_5_picker_release_uebersicht.svg`.
- **P8.5-R/P8.5-T** („kein neues Handover-Dokument, Closeout wird §9") → §9 **ist** gefüllt
  und bleibt der kanonische Closeout; dieses Dokument tritt **daneben**, nicht an seine
  Stelle. Es ist der Einstiegspunkt für die P8.6-Planung, §9 ist der Beleg.

Das ist ausdrücklich kein Präzedenzfall für stille Lock-Aufweichung: die Umkehr kam vom
Menschen, der die Locks gesetzt hat, und ist an beiden Stellen datiert.

---

## 8 Arbeitsweise und Werkzeug-Stand

Unverändert seit P7 §7: **Claude Code plant, opencode/M3 führt aus, kein Advisor in der
Ausführung** (N4). Ersatz ist die §0.5-Selbstprüf-Checkliste plus die Sichtprüfung. Neu in
dieser Phase:

- **Eskalationsregel P8.5-O:** ein Fund, dessen Ursache in einer *früheren* CSS-Regel oder
  in der Kaskade liegt, wird nicht symptomatisch gepatcht, sondern an Claude Code eskaliert.
  Erkennungsmerkmal: „der Wert stimmt im Quelltext, sieht im Browser aber anders aus."
- **Vier Sichtungs-Konventionen** (`sichtpruefung_automation_conventions.md` §1–§4):
  Vorschau-Pflicht bei klickbaren Links · Code/automatisierte Tests sind Agenten-Sache,
  Visuelles ist Nikinger-Sache · Deploy erst nach Testauswertung · Screenshots im Chat,
  sobald das Vision-Plugin steht.
- **Rotation:** der Phase-8.5-Head trägt **einen** `## Session stopped` mit *mehreren*
  datierten `###`-Unterblöcken. `scripts/rotate_session_block.sh` erkennt dieses Muster
  nicht (es zählt `##`-Überschriften) und meldet „bereits konform". Rotiert wurde deshalb
  per `sed`-Schnitt mit `cmp`-Gegenlesung — dasselbe Prinzip, andere Ausführung. Wer das
  Skript in P8.6 nutzen will, legt pro Session einen eigenen `##`-Block an.

---

## 9 Was dieser Handover nicht enthält

- **Die Implementierungsdetails.** Sie stehen im Code und in
  `phase8_5_picker_release_plan.md` §2–§5. Wer wissen will, *warum* `<select>` statt
  Radiogruppe geplant war, liest P8.5-F — dort steht auch das Gegenargument, das bewusst
  nicht weggeredet wurde.
- **Die Phase-8-Historie.** `phase8_ui_graph_plan.md` §9, `phase8_ui_graph/CLAUDE.md`,
  `phase8_ui_graph/SESSIONS_ARCHIVE.md`.
- **Die vollständige Abnahmematrix.** `phase8_5_picker_release/SESSIONS_ARCHIVE.md`
  §Abnahmematrix-Archiv, 20 Zeilen mit Beleg und Sichtungsvermerk.
- **Einen P8.6-Plan.** Dieser Handover benennt Entscheidungen; er trifft keine. Das Locking
  ist die Aufgabe der Planungs-Session.
