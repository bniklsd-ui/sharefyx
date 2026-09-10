
---
status: archive
purpose: Archiv der historischen `[YYYY-MM-DD]`-Session-Blöcke, die bis zum Z-Closeout in `CLAUDE.md` §Current state standen — Phase 1/2/3/4/5/6/6.5/7/8/8.5-Vorlauf + Hard-Rule-Korrekturen + Phase-5-Block-D-Detailnarrative + Deploy-Blocker/Funnel-Recovery-Notizen + diverse Korrekturen
read-when: Auditieren der vollen Wurzel-CLAUDE.md-Historie — der aktuelle Current-state-Absatz lebt im Wurzel-Head, nicht hier
detail: L3
up: ../CLAUDE.md
down:
updated: 2026-09-10 (P8.6 Step 0 Haushalt-Block aus Wurzel-`CLAUDE.md` §Current state rotiert — Migration-Vorbereitungs-Block brauchte Platz im Wurzel-Head, deshalb der Vorgänger nach hier verschoben; Project-Pattern: jeder neue Current-state-Eintrag rotiert den bisherigen verbatim hierher)
---

**[2026-09-10, P8.6 Step 0] Haushalt der neuen aktiven Phase 8.6 ausgeführt (Phase 8.5 abgeschlossen, Phase-8.6-Plan ausgeführt).** Plan §1.10 wörtlich umgesetzt: Phasenverzeichnis `phase8_6_ui_polish/` mit `CLAUDE.md` (~22 KB, mit Mission/Scope/Harte Regeln/Modul-Status 0–Z/Baselines V97/V107/V108/Vormerkungen/Step-0-Session-Block) + `SESSIONS_ARCHIVE.md` (📦 leer, mit L1-Card) + `scripts/` (leer, Wegwerf-Smokes folgen in Gate/§7) angelegt. **Sieben Befunde behoben:** (1) sechs unauflösbare `up:`/`down:`-Links — alle sechs in `p8x_ui_polish_notes.md`, von 187 Frontmatter-Links im Repo die einzigen kaputten (`../` → `../../`); (2) vier fehlende L1-Header-Cards ergänzt (`docs/PROJECT_SESSION_LOG.md` L3-Archiv-Card, `phase8_5_picker_release/{SICHTPRUEFUNG_RESTBLOCK,SICHTPRUEFUNG_WALKTHROUGH,CLUSTER3_TESTBLOCK}.md`); (3) drei `down:`-Listen vom Inline-Format (`·`-Trenner) auf Listenform (`phase6_5_tools_images_plan.md`, `phase6_shares/{GLOBAL_SEARCH,IMAGES}_PLAN.md`); (4) zwei fehlende INDEX-Zeilen ergänzt (`CLUSTER3_TESTBLOCK.md`, `THIRD_PARTY_LICENSES.md` mit Ausnahme-Markierung); (5) zwei INDEX-Drift-Korrekturen (`phase8_ui_graph/CLAUDE.md` bekommt die Softcap-Notiz wie `phase6_shares`, `phase5_ui/CLAUDE.md` verliert die falsche „über dem 40-KB-Softcap"-Aussage — real 40.957 B = 3 B unter Cap); (6) **`docs/INDEX.md` von 40.960 B auf 37.763 B** komprimiert (Plan-Zeilen P8.6/P8.5/P8/P7/P6/P6.5/P5/P4/P3/P2 auf Pointer-Form gestrafft — L0 ist Landkarte, keine Kurzfassung, Plan §1.5); (7) zwei echte Code-Defekte **dokumentiert, hier nicht behoben** (`var(--border-soft)` undefiniert an `app.css:1270/1276` → Block A §3.3, `graph.js :: runSimulation()` `rafId` lokal aber nie gelesen → Block D §6.4). **Verifikation:** Repo-weiter `up:`/`down:`-Link-Scan über 203 .md-Dateien **0 Fehler**; `find … -size +40k` für `docs/INDEX.md` ergibt nichts. **Selbstprüfung:** `pytest` **964/964** (V107 ✅), `ui_budget.py` **5/5, 130,1 KB** (V97 ✅), **V108 `_overview` ~863 ms offen** (vor Block C drei Läufe mitteln — Plan §1.7), **kein Code-Touch** (Tabu-Diff §0.3 leer), **Service-Touch 0** (PID 355956 nur gelesen, keine Wegwerf-Instanz gestartet — Step 0 ist Doku + Skelett, kein Lauf gegen den Server). **Nächster Schritt:** **Step V — OpenCode-Vision-Plugin-Installation** (`DavidEasden/opencode-vision`, Plan §2, Nikinger-Vorgabe 2026-09-08 „erster Punkt vor jedem Code-Touch"); bei Plugin-Repository-Konfig oder Authentifizierung **vor** der Installation fragen, nicht im Trial-and-Error. Step 0-Commit-Message wörtlich aus Plan §1.10: `phase 8.6: Step 0 -- Haushalt, sechs kaputte Doku-Links, vier fehlende L1-Cards, INDEX-Kompression`.

**[2026-09-09, P8.6-Planungssession] Phase 8.6 geplant und ausführungsreif — Reichweite vom Nikinger aus vier geschachtelten Bündeln gewählt, drei offene Entscheidungen des P8.5-Handovers gelockt, sieben Step-0-Befunde gemessen statt geraten.** Neu: `docs/concepts/phase8_6_ui_polish_plan.md` (~66 KB, 📕-Snapshot, gegen `main@d1af51b`), Verzeichnis gelockt als **`phase8_6_ui_polish/`** (P8.6-A), Deploy-Ziel `v3.0.2`. **Reichweite „Selektions-Welle + Layout"** (N1): §5 Layering-Tokens + §10.1–§10.7 Selektions-Vereinheitlichung + §6 „Konto"→„Einstellungen" (Lesart b: Einstellungen nach oben, Abmelden ans Rail-Ende) + §3 Ordner-Zähler + §1 Rail-/Übersichts-Reorg + §10.4 klickbare Spaces + §2.3/§2.4 Map-Fixes + Radiogruppe-Rückbau auf `<select>`. **Drei Nikinger-Entscheidungen:** (1) **es gibt kein P8.7** — sein „eher v3.1 also p8.7" meint das dokumentierte **P9 → `v3.1.0`**, die AI-Sessions-Anzeige ist damit P9-Inhalt, umbenannt wurde nichts; (2) **V102 dedupliziert im Frontend** (`graph.js:156`, bei der Übernahme statt in `drawEdges()`) — bewusst **keine neunte P1-Contract-Öffnung**, `storage/` bleibt in P8.6 unangetastet; (3) **§10.7 wird eine fünfte Konventions-Kategorie „Vorsicht"** statt zweier Einzelfälle, umgesetzt als `--caution: var(--danger)` — derselbe Wert, zweiter Name, weil der Kommentar an `--danger` (`app.css:57`) die Kategorie längst benennt („Widerruf, Archivieren"). **Step 0 wurde in dieser Session bereits durchgeführt, die Befunde stehen im Plan §1:** sechs unauflösbare `up:`/`down:`-Links — **alle sechs in `p8x_ui_polish_notes.md`**, ausgerechnet der Inhaltsquelle der Phase (`../` statt `../../`); von 187 Frontmatter-Links im ganzen Repo sind das die einzigen kaputten. Vier fehlende L1-Header-Cards, zwei fehlende INDEX-Zeilen, drei `down:`-Cards im Inline-
statt Listenformat (deren Ziele auflösen — der Befund ist der Prüfer, der sie **still
überspringt** und trotzdem „sauber" meldet). **Und ein stiller Softcap-Verstoß:**
`phase8_ui_graph/CLAUDE.md` liegt mit 42.343 B über dem Cap und ist — anders als
`phase6_shares/CLAUDE.md` — **nirgends als Ausnahme benannt**; die Konvention duldet einen
benannten Verstoß und verbietet einen stillen. Umgekehrt behauptet die INDEX-Zeile von
`phase5_ui/CLAUDE.md` seit dem 2026-08-28, die Datei liege über dem Cap — sie liegt mit
40.957 B **darunter**. **Zwei echte Code-Defekte:** `var(--border-soft)` ist an `app.css:1270/1276` referenziert, aber **nirgends definiert** — nach CSS-Spezifikation wird die `border`-Kurzform damit ungültig und `.link-picker-results` zeichnet **gar keinen** Rahmen; und `graph.js :: runSimulation()` pflegt ein lokales `rafId`, das es nie liest — es gibt kein `cancelAnimationFrame`, also stapeln wiederholte Übersicht-Klicks nebenläufige `tick()`-Schleifen. **Zwei Baselines gemessen, nicht geschätzt:** `pytest -q` **964 passed in 257 s** (mit ausgehängten `SHAREFYX_*`/`SFX_*`) und `ui_budget.py` **5/5**, 130,1/250 KB — damit sind **V97 (geerbt) und V107 geschlossen**. **`docs/INDEX.md` ist praktisch voll:** sie stand auf exakt 40.960 B, und schon die *eine* Zeile für diesen Plan erzwang das Straffen von drei anderen Einträgen; es bleiben **32 Byte Luft**, der Head- und Archiv-Eintrag der Phase passen nicht mehr — Step 0 hat den ausdrücklichen Auftrag, auf ≤38 KB zu komprimieren. **Kein Code-Touch**, Tabu-Diff §0.3 leer, **Service-Touch 0** (Produktions-PID 355956 nicht angefasst, keine Wegwerf-Instanz gestartet). **Nächster Schritt:** Ausführung in opencode/M3 nach Plan §1–§8, Reihenfolge Step 0 → Step V (Vision-Plugin) → Block A → B → C/D → Gate → Deploy → Step Z; der Closeout wird Plan **§9**.

**[2026-09-09, Phase-8.5-Z-Closeout] Phase 8.5 mit Step Z vollständig abgeschlossen — Übersichtsgrafik und Handover als bewusste Umkehr zweier eigener Locks, Plan §9 gefüllt, vier Doku-Drifts behoben.** Der Phasen-Abschluss-Prompt lief zum ersten Mal gegen eine Phase, die ihre eigenen Closeout-Artefakte ausgeschlossen hatte: **P8.5-S** („keine Übersichtsgrafik") und **P8.5-R** („kein neues Handover-Dokument") standen seit dem 2026-09-03 gelockt im Plan. Der Nikinger hat beide im Closeout-Auftrag selbst aufgehoben — beide tragen jetzt eine durchgestrichene Altfassung plus datierte Korrekturnotiz in `docs/concepts/phase8_5_picker_release_plan.md` §0.2; **P8.5-T bleibt unangetastet**, §9 ist gefüllt und bleibt der kanonische Closeout, das Handover verweist darauf statt es zu ersetzen. **Neu:** `docs/concepts/phase8_5_picker_release_uebersicht.svg` (1080×1080, headless-Chromium gerendert und visuell gegengeprüft) + `docs/concepts/PHASE8_5_CLOSEOUT_HANDOVER.md` (Einstieg für die P8.6-Planung, §4 = offene Entscheidungen, §5 = `[VERIFY]`-Bilanz V95–V105). **Vier Drifts im selben Commit behoben:** Modul-Status-Zeilen 2–7 standen auf 🟡/⬜, während der Abnahmestand darunter 20/20 ✅ meldete; Plan §9 war leer, obwohl P8.5-T ihn als Closeout festlegt; Modul-Status Zeile 2 nannte `<select>` statt der seit dem 2026-09-07 gebauten Radiogruppe; `p8x_ui_polish_notes.md` §A führte die vierte A3-Probe noch als „wird in D5 entschieden" (sie lief am 2026-09-08, ✅). **Neun Nikinger-Feedback-Punkte** sind als `p8x_ui_polish_notes.md` **§10** abgelegt (Zitat + Code-Anker, ungewichtet) — sieben davon Verschärfungen von §5/§6; **§B: die Mobile-Hälfte der Außenkante „Mobile/Realtime" ist datiert aufgehoben** (Hochkant-UI wird benanntes Zukunfts-Item, Realtime bleibt draußen); die Nummern-Frage „eher v3.1 also p8.7" gegen die dokumentierte Reihe P8.6 → `v3.0.2` / P9 → `v3.1.0` wurde **bewusst nicht selbst entschieden**. **Rotation:** der Head trug einen `## Session stopped` mit zwei datierten `###`-Unterblöcken — `scripts/rotate_session_block.sh` zählt `##`-Überschriften und hätte „bereits konform" gemeldet; rotiert wurde per `sed`-Schnitt mit dreifacher `cmp`-Gegenlesung, dazu 19 von 22 `updated:`-Frontmatter-Einträgen verbatim ins Archiv (**Head 52.6 → 26.0 KB**, Archiv 172 → 205 KB, INDEX erstmals wieder unter dem Softcap mit 40.9 KB). **Kein Code-Touch**, pytest **964/964** (267 s), Tabu-Diff §0.3 leer, Service-Touch 0 (PID 355956, 3 Tage Uptime, nur gelesen). **Nächster Schritt:** P8.6-Planungs-Session in Claude Code — Einstiegsdokument ist das Handover §4, erster Punkt der Phase bleibt die OpenCode-Vision-Plugin-Installation.
**[2026-09-09, P8.5-6-Folge-Smoke] Bracket-Pfad live-verifiziert, Bilanz 19/1/0 → 20/0/0, Phase 8.5 vollständig abgeschlossen.** v3ritt-Wegwerf frisch hochgefahren (PID 461074, Port 18773, eigener tmp-`DATA_ROOT`), Item `itm_b8b989a1` „Vercel [Hosting]" via `storage.Store.create()` in alpha angelegt, neuer Mini-Smoke `phase8_5_picker_release/scripts/p856_bracket_mini_smoke.py` (~75 Z., Playwright) führt den kompletten P8.5-6-Bracket-Pfad aus — Login + Edit-Mode + Picker + Link einfügen + **zwei Screenshots** (`p856_bracket_edit_view.png` mit `\[…\]`-Escapes im Quelltext + `p856_bracket_preview.png` mit „Vercel [Hosting]" als **klickbarem blauen Hyperlink**), programmatische Quittung per Regex auf `<a href="#item/itm_b8b989a1">Vercel [Hosting]</a>` True. Wegwerf sauber per PID-Datei gestoppt (kein `pkill -f`); Production-PID 355956 unverändert. **Phase 8.5 ✅ formal vollständig abgeschlossen.** **Doc-Updates in diesem Commit:** `phase8_5_picker_release/CLAUDE.md` §Abnahmestand Bilanz → **20/0/0**, §Nächste Session auf P8.6-Planung umgeschrieben, Sichtungs-Session-Block um P8.5-6-Folge-Smoke ergänzt (kein neuer Block, Konvention „genau ein Session-Block" gehalten); `phase8_5_picker_release/SESSIONS_ARCHIVE.md` Matrix-Zeile P8.5-6 auf ✅ mit Folge-Smoke-Beleg, §Abnahmematrix-Archiv-Header aktualisiert; `docs/INDEX.md` + `docs/ROADMAP.md` Frontmatter-updated. **Kein Code-Touch**, pytest unverändert 964/964, Tabu-Diff §0.3 leer, Service-Touch 0 (Production-PID 355956 unverändert). **Nächster Schritt:** P8.6-Planung in Claude Code mit OpenCode-Vision-Plugin-Installation als erstem Punkt — neue Konvention §4 aus den Sichtungs-Sub-Sessions greift dort sofort.
**[2026-09-09, Sichtung 10 P8.5-🟡] 9 von 10 Zeilen auf ✅, P8.5-6 bleibt 🟡 (Vorschau-Screenshot des Bracket-Pfads fehlt); vier neue Sichtungs-Konventionen notiert (Vorschau-Pflicht / Code-vs-Visuell / Deploy-nach-Test / Screenshots-im-Chat nach opencode-vision-Install).** Methodik: opencode/M3 sichtet die Block-C-Screenshots + Smoke-Asserts + statische Tests grün (Vision über `Read`-Tool), Nikinger bewertet pro Zeile. Nikinger-Vertrauens-Regel: (C)-Code-Test-Beweise sind durch den ausführenden Agenten verifiziert, kein zusätzlicher Sichtungs-Schritt nötig; (W)-Wegwerf-Beweise mit Nikinger-Vertrauen auf dokumentierten Beleg. **Phase-8.5-Bilanz 10 ✅ · 10 🟡 · 0 ⬜ → 19 ✅ · 1 🟡 · 0 ⬜** (P8.5-7/-8/-9/-10/-11/-12/-13/-14/-15 neu ✅; P8.5-6 bleibt 🟡). **Was P8.5-6 zum ✅ braucht:** Mini-Smoke gegen v3ritt-Wegwerf mit `[…]`-Titel-Item + Vorschau-Panel-sichtbar-Screenshot, sodass der gerenderte Link als klickbarer Hyperlink sichtbar wird (statt nur in der Markdown-Quelle). **Oder** direkt Sprung zu P8.6-Planung mit OpenCode-Vision-Plugin-Installation als erstem Schritt — dann eröffnen sich dieselben Sichtungs-Erleichterungen und P8.5-6-Brake-Pfad kann inline mitlaufen. **Doc-Updates in diesem Commit:** `phase8_5_picker_release/CLAUDE.md` §Abnahmestand + §Nächste Session + neuer Session-Block (alter Z-Closeout-Block manuell nach `SESSIONS_ARCHIVE.md` rotiert, Skript passt nicht auf Phase-8.5-Muster mit einem `## Session stopped` + mehreren `### date`-Subblöcken) + 10 Matrix-Zeilen mit Nikinger-Vermerk; `docs/concepts/sichtpruefung_automation_conventions.md` §1-§4 neu; `docs/concepts/sichtpruefung_automation_tooling.md` Plugin-Empfehlung auf P8.6 first step verschärft; `phase8_5_picker_release/SICHTPRUEFUNG_WALKTHROUGH.md` + `SICHTPRUEFUNG_RESTBLOCK.md` Top-Notiz „Vorschau-Pflicht"; `docs/INDEX.md` + `docs/ROADMAP.md` Frontmatter-updated. **Kein Code-Touch**, pytest unverändert 964/964, Tabu-Diff §0.3 leer, Service-Touch 0 (Production-PID 355956 unverändert, keine Wegwerf-Instanzen gestartet).
**[2026-09-08, scope-reversal] Nikinger-Entscheidung: die 10 P8.5-🟡-Sichtungen (P8.5-6, -7, -8, -9, -10, -11, -12, -13, -14, -15 — Browser-verifiziert in Chromium+Firefox, throwaway-qualifiziert, aber Screenshots vom Nikinger noch nicht selbst gesichtet) wandern NICHT nach P8.6, sondern bleiben in Phase 8.5 — als erste Sache der nächsten Session. Anlass: der Z-Closeout-Stand-Summary-Text hatte „Guter erster Kandidat für eine kurze Nachprüfung in P8.6, kein neuer Code nötig — nur eine Sichtung der bereits vorliegenden Block-C-Belege gegen die neue Regel" geschrieben; der Nikinger hat das beim Review umgesteuert (Phase 8.5 hier abschließen, nicht auf eine Folge-Phase schieben). Konkrete Anleitung: `phase8_5_picker_release/SICHTPRUEFUNG_WALKTHROUGH.md` + `SICHTPRUEFUNG_RESTBLOCK.md`. Bei Erfolg: Phase 8.5 springt von 10 ✅ auf 20 ✅ · 0 🟡 · 0 ⬜, Phase 8.5 dann formal vollständig abgeschlossen. Kein Code-Touch, kein Deploy. Phase 8.5 head hat eine neue Sektion „## Nächste Session" bekommen mit den 10 Zeilen einzeln aufgelistet + Werkzeug-Setup-Stand.

**[2026-09-08, Z-Closeout] Phase 8 ✅ + Phase 8.5 ✅ — formal abgeschlossen, Statusregel geändert, zwei Folgephasen (P8.6 → v3.0.2, P9 → v3.1.0) vorgemerkt.** Sichtprüfungs-Automatisierungs-Sub-Session: 9 von 9 Sichtprüfungs-Punkten aus dem D5/Cluster-4/Cluster-5-Restblock durchgelaufen — teils gegen Wegwerf-Instanzen (Canvas-Instrumentierung für den exakten Tag-Kanten-Zähler, CDP-Medien-Emulation für Glass-Fallback, ein neu gebautes Zwei-Principal-Wegwerf-Setup für den echten Zweitnutzer-ACL-Nachweis über OAuth+MCP), teils gegen die echte Produktion (der reconnectete sharefyx-MCP-Connector: `list_spaces` + ein echter claude.ai-Chat des Nikingers, der ein Item korrekt beim Titel statt bei der `itm_…`-ID nannte). **Statusregel-Änderung, Nikinger-Entscheidung:** eine vom Nikinger selbst geprüfte Wegwerf-Instanz-Automatisierung (byte-identischer Git-Checkout wie Produktion, Unterschied nur `DATA_ROOT`/`auth.sqlite3`/Identität) zählt jetzt als „live-verifiziert" — Details, Begründung, wiederverwendbare Techniken: `docs/concepts/sichtpruefung_automation_conventions.md` (neu, samt Schwester-Datei `sichtpruefung_automation_tooling.md` für Werkzeug-/Plugin-Empfehlungen). Phase-8-Bilanz **26 ✅ · 0 🟡 · 0 ⬜**, Phase-8.5-Bilanz **10 ✅ · 10 🟡 · 0 ⬜** (die verbleibenden 🟡 sind Block-C-Belege von 2026-09-04, die der Nikinger unter der neuen Regel noch nicht gesichtet hat — kein neuer Code nötig, nur eine Sichtung). Drei Wegwerf-Instanzen (200-Knoten, D2, das neue Zwei-Principal-Setup) sauber abgebaut, PID-Datei-basiert, kein `pkill -f`, Produktion durchgehend unangetastet (PID 355956). **Zwei Folgephasen besprochen, noch nicht geplant:** **P8.6** (Arbeitsname, → `v3.0.2`) bündelt die restlichen `p8x_ui_polish_notes.md`-Punkte + einen Radiogruppe-Rückbau auf `<select>` (Nikinger kehrt seine eigene D4-Entscheidung um, Design-Konsistenz) — **erster Punkt darin: das OpenCode-Vision-Plugin installieren** (`DavidEasden/opencode-vision`), damit künftige Sichtprüfungsrunden davon profitieren; **P9** (Arbeitsname, → `v3.1.0`) ist der Obsidian-Map-/Graph-Umbau, laut Nikinger voraussichtlich der letzte große UI-Umbau. Volle Herleitung, Matrix-Zeilen, Screenshots: `phase8_ui_graph/CLAUDE.md` §Abnahmestand, `phase8_5_picker_release/CLAUDE.md` Abnahmestand + „Nächste Phasen"-Abschnitt.

**[2026-09-08, Folge 2] Phase 8.5 — 🔄 Doku-Sub-Session: freundlicher Walkthrough für die Sichtprüfung geschrieben, ⬜ Sichtprüfung selbst durch Nikinger.** Auf Bitte des Nikingers nach mehr Detailtiefe: neue Datei `phase8_5_picker_release/SICHTPRUEFUNG_WALKTHROUGH.md` (29 KB / 727 Zeilen) als **Geschwister** zum bestehenden technischen `SICHTPRUEFUNG_RESTBLOCK.md`. Walkthrough-Struktur: Vorbereitung (drei Tabs + Connector), dann pro Schritt "Was tust du" + "Was siehst du" + optionale DevTools-/Console-Befehle + Pass/Fail-Beschreibung. Deckt C4-0 (P8-16 Glass-Fallback via Rendering-Tab), C4-1 (P8.5-19 Radiogruppe mit `localStorage`-Cross-Check), C4-2 (P8.5-3+4 Hint + Vierte A3-Probe — Tipp: jede Form in eigene Anfrage packen, damit der Connector nicht alle vier vereint), C4-3 (P8.5-17 V105 Connector-Check), C3-1 (P8-21d Tag-Cutoff mit Console-Cross-Check `fetch('/api/v1/graph').then(g => g.edges.filter(e => e.kind === 'tag').length)`), C3-2 (P8-22 mit Stoppuhr-Anleitung für Settle-Zeit < 3 s), C3-3 (P8-24 E2E-Ritt gegen D2 in sechs Stationen), C5-1 (P8-5 = C4-2), C5-2 (P8-8 mit Fabian-Koordination). Login-Snippet und TOTP-Secrets am Dateiende noch einmal komplett. Ergebnis-Tabelle zum Ausfüllen mit Bestanden-Spalte pro Punkt + Notizen-Feld für Restdefekte. **Kein Code-Touch**, **pytest 964/964 unverändert**, **Tabu-Diff §0.3 leer**, **Service-Touch 0**. **Größen-Stand:** Walkthrough **29 KB** neu (separate Datei, kein Softcap-Druck); Phase-8.5-Head jetzt **~80 KB** (drei Sub-Sessions vom 2026-09-08 im Head — Phase-8.5-Muster mit `## Session stopped` + mehreren `### date`-Subblöcken ist etabliert; weiter deutlich über 40-KB-Softcap, Auflösung bleibt Z-Arbeit); `docs/INDEX.md` ~64.8 KB. **Nächster Schritt:** Nikinger-Live-Sichtprüfung mit dem Walkthrough am Bildschirm (~12 Min ohne Fabian, ~22 Min mit). Nach dem Lauf: Status-Updates der Phase-Heads + INDEX + Commit + Cleanup-Befehle (Hard Rule 9, PID-Datei-basiert). **Danach: Z** (Phase-8.5-Closeout).

**[2026-09-08, Folge] Phase 8.5 — 🔄 Doku-Sub-Session: Restblock-Sichtprüfungs-Testblock geschrieben + D2-Wegwerf parallel hochgefahren, ⬜ Sichtprüfungen selbst durch Nikinger.** Zusätzlich zum 200-Knoten-Wegwerf (Port 18772, PID 436596) wurde der **D2-Wegwerf hochgefahren** auf Port 18768 (PID 438765, 14 Knoten, 6 Kanten — der richtige Datensatz für P8-24, weil der 200-Knoten-Datensatz für Station-3-Idempotenz bei `DEFAULT_LIMIT=50` driftet). Beide Wegwerf-Instanzen laufen jetzt parallel, Production-Dienst unverändert (PID 355956). **Neue Datei `phase8_5_picker_release/SICHTPRUEFUNG_RESTBLOCK.md`** (27.5 KB, 471 Zeilen) — der konsolidierte Schritt-für-Schritt-Testblock für **alle restlichen Sichtprüfungen**: Cluster 3-Rest (Phase 8) P8-21 d + P8-22 + P8-24 gegen die zwei Wegwerf-Instanzen, Cluster 4 (Phase 8.5) P8-16 + P8.5-3 + P8.5-4 + P8.5-17 + P8.5-19 gegen Production v3.0.1, Cluster 5 (Phase 8) P8-5 (fällt mit C4-2 zusammen) + P8-8 (braucht Fabian für Zweitnutzer-Token). Re-runnables Login-Snippet mit aktuellem TOTP-Code für beide Instanzen (rollt alle 30 s, vor jeder Sichtprüfung neu ausführen), Screenshots-Konvention, Ergebnis-Tabellen je Cluster, Reihenfolge-Empfehlung (11 Schritte, ~15–30 Min), Hard-Rule-9-konformer Cleanup-Befehl. **Cluster-3-Rest-Block** ist neu geschrieben — vorher gab es nur `CLUSTER3_TESTBLOCK.md` für P8-20/21/22/24 gegen die Wegwerf-Instanzen, jetzt konsolidiert + erweitert um Cluster 4 + 5 + Login-Workflow. **Doku-Updates im selben Sub-Session-Zyklus (Hard Rule 8):** `phase8_5_picker_release/CLAUDE.md` Folge-Sub-Session-Block neu im Head (gleichberechtigt zum ersten 2026-09-08-Block, beide unter `## Session stopped`-Header — Phase-8.5-Muster erlaubt mehrere `### date`-Subblöcke); `docs/INDEX.md` neue Datei-Zeile; **kein Code-Touch**, **pytest 964/964 unverändert**, **Tabu-Diff §0.3 leer**, **Service-Touch 0**. **Größen-Stand:** Phase-8.5-Head **65.3 KB** (+24.4 KB durch den 2026-09-08-Folge-Block, schon vorher deutlich über dem 40-KB-Softcap, Auflösung bleibt Z-Arbeit — bewusst nicht stiller Trimm); `SICHTPRUEFUNG_RESTBLOCK.md` **27.5 KB** neu; `docs/INDEX.md` **64.0 KB** (+0.7 KB); `p8x_ui_polish_notes.md` 37.5 KB unverändert; `SESSIONS_ARCHIVE.md` ~128 KB unverändert. **Nächster Schritt:** Sichtprüfungen selbst durch den Nikinger am echten Gerät nach `SICHTPRUEFUNG_RESTBLOCK.md`-Anleitung (~15 Min ohne Fabian / ~30 Min mit). Cluster 5 (P8-8 Zweitnutzer) braucht Fabian. **Cleanup nach dem Lauf:** `.venv/bin/python phase8_ui_graph/scripts/wegwerf_setup_d2.py cleanup` + `…_200knoten.py cleanup` (Hard Rule 9, PID-Datei-basiert, **niemals** `pkill -f`). **Danach: Z** (Phase-8.5-Closeout) hebt die abgehakten Zeilen auf ✅ und schließt Phase 8 + 8.5 formal mit ab.

**[2026-09-08] Phase 8.5 — 🔄 Doku-Sub-Session (Wegwerf gestartet + 3 User-Feedback-Punkte), ⬜ Cluster 4 + 5 + Z als Nächstes.** 200-Knoten-Wegwerf-Instanz per Standing-Permission gestartet (Port 18772, PID 436596, User `alpha`, Credentials unter `/tmp/opencode/sharefyx-wegwerf-200knoten/credentials.json`); Production-Dienst unverändert PID 355956 (seit 2026-09-05 16:10:18 CEST); **drei weitere User-Feedback-Punkte** in `docs/concepts/p8x_ui_polish_notes.md` ergänzt: §6 Konto/Einstellungen-Rename + Positions-Tausch mit Logout re-affirmiert mit drei Vertausch-Lesarten a/b/c gegen `app.html:31-41` (Klärung in der Planungs-Session, nicht raten); **§8 NEU customizable Tags for tasks (kosmetisch) + Standard-Tag „blocked"** mit Aufteilung in §8.1 (User-Palette als `localStorage["sfx:tags:palette"]`, Server unverändert, „only cosmetic") und §8.2 (fester Code-Tag, offen ob kosmetisch oder mit Bucket-Semantik); **§9 NEU direkter User-Feedback-Button** mit drei plausiblen Senken (User-Space-Item via bestehende REST-API / `/var/log/sharefyx/feedback/` mit neuem Server-Write-Pfad / externer Endpunkt = Architektur-Frage) + UI-Platzierungs-Vorschlag (Rail unter Einstellungen + Abmelden, oder Read-View-Footer) + Klärungsfragen zur Planungs-Session (anonyme Variante, Throttling, „Was darf mitgeschickt werden" — explizit kein TOTP/Passwort/Recovery); §C (offene Fragen) und §E (chronologische Tabelle) ebenfalls ergänzt. Cluster-3-Block aus Phase-8.5-Head per Hand nach `SESSIONS_ARCHIVE.md` rotiert (Skript passt nicht auf Phase-8.5-Muster, bewährtes Vorgehen), 2026-09-08-Doku-Block neu im Head. **Login-Daten-Befehl für den Nikinger** (gibt bei jedem Lauf den aktuellen Satz aus, da das Passwort per `secrets.token_urlsafe(8)` jedes Mal neu gewürfelt wird): `cd /home/savefyx/dev/savefxy && .venv/bin/python -c '...'` (vollständiger Block im Phase-8.5-Head Session-Block). **Größen-Stand:** Polish-Notes **37.5 KB** (knapp unter 40-KB-Softcap, **+12 KB**), Phase-8.5-Head **53.8 KB** (+3 KB, weiter über Softcap — Auflösung bleibt Z), Phase-8.5-SESSIONS_ARCHIVE **121.8 KB** (+13 KB durch rotierten Cluster-3-Block, L3 exempt), Phase-8-Head **94.3 KB** unverändert, `docs/INDEX.md` **63.3 KB** (+1.7 KB), Wurzel-`CLAUDE.md` **72.2 KB** (+1 KB). **pytest unverändert 964/964** (kein Python-Touch), **Tabu-Diff §0.3 leer**, **Service-Touch 0**. **Nächster Schritt:** Cluster 3-Rest (P8-21 d / P8-22 / P8-24 Nikinger-Aktion) + Cluster 4 (Connector: P8.5-3 + P8.5-4 + P8.5-17 V105 + P8.5-19 Bauform-Bestätigung Radiogruppe) + Cluster 5 (Fabian: P8-5 + P8-8) + Z.

**[2026-09-03] Phase 8.5 geplant — ⬜ nicht gestartet.** Link-Picker-Politur, Titel-statt-ID-Hint,
v3-Vorabritt und Deploy (`phase8_5_picker_release/`, kein eigenes Python-Paket). Plan:
`docs/concepts/phase8_5_picker_release_plan.md` (N1–N7 gelockt, P8.5-A–P8.5-T, Abnahme
P8.5-1–P8.5-20, `[VERIFY]` V95–V105). Schließt die drei Restdefekte aus
`phase8_ui_graph_plan.md` §9.4.1–§9.4.3 und **beendet Phase 8 formal mit** (N6, Präzedenz
P7 Step A8 für Phase 6.5) — deshalb 8.5 und nicht 9. **Wichtige Korrektur zum Live-Stand:**
v3.0 ist **nicht** ausgeliefert — `/opt/sharefyx/current` zeigt auf `007b73d` (Block B),
Badge `v2.2.3`; Block C (Design v3) und Block D (Graph, tabellose Übersicht) liegen nur im
Repo. Deshalb ist ein **voller 13-Stationen-Vorabritt gegen eine Wegwerf-Instanz vor dem
Deploy** Teil dieser Phase (N5), nicht nur die drei Fixes. Kernbefund der Planung, im Code
verifiziert: ein Body-Link `[Titel](#item/itm_…)` ist bereits eine Graph-Kante
(`storage/linkscan.py`) — der Picker bekommt deshalb einen **Modus-Umschalter** statt eines
Kombi-Klicks. **Ausführung wieder opencode/M3 ohne Advisor** (N4), mit neuer
Eskalationsregel: Kaskaden-Ursachen gehen an Claude Code (Lehre vom 2026-09-02).

**[2026-09-03] Phase 8.5 — 🔄 Step 0 abgeschlossen, ⬜ A1 noch nicht angefangen.** Skelett
angelegt (`phase8_5_picker_release/{CLAUDE.md, SESSIONS_ARCHIVE.md, scripts/}` mit L1-Cards,
Modul-Status-Tabelle für Step 0/A/B/C/D/Z, Abnahmematrix nach §7-Muster, leerer
`## Session stopped`-Block), die vier vom Plan §1 benannten Funde abgearbeitet:
`docs/INDEX.md` 52.911 B → 40.917 B (Kürzung `updated:` auf die 5 neuesten Einträge +
Schlusszeile „ältere Einträge: phase*/SESSIONS_ARCHIVE.md", jetzt 43 B unter dem eigenen
40 KB-Softcap, Ausnahmenliste kompakt gehalten wegen der Mehrbelastung), vier card-lose
`.md` als korrekte Ausnahmen dokumentiert (Harness, Test-Fixtures, maschinell geparst,
Vendor/Lizenz), Doku/Code-Drift „Büroklammer" → „Lupe" in
`phase8_ui_graph/CLAUDE.md:440` mit datierter Korrekturnotiz, Phase-8-Abnahmebilanz
**15/10/0 → 14/12/0** maschinell korrigiert und awk-Kommando im Phase-8-Head Bilanz-Abschnitt
verankert (zählmaschinell nachprüfbar, statt weiterer Drift). ROADMAP-Abschnitt „Phase 8.5",
Wurzel-CLAUDE.md-`down:` auf `phase8_5_picker_release/CLAUDE.md` umgestellt, drei INDEX-Zeilen
unter „Phase 8.5 — 🔄 …" — alles im selben Commit (Hard Rule 8). **`pytest` unverändert
959/959 grün** (kein Python-Touch in dieser Session), Tabu-Diff §0.3 leer, kein Service-Touch
(PID 195922, ActiveEnterTimestamp 2026-09-02 11:51:57 CEST — nur gelesen). Nächster Schritt:
Block A / A1 (Picker-Modus-Umschalter).

**[2026-09-04] Phase 8.5 — 🔄 A1 committet, Drift nachgezogen, ⬜ A2 als Nächstes.** A1
(Picker-Modus-Umschalter + Body-Markdown-Link-Helper + `localStorage` unter
`sfx:linkpicker:mode`) gebaut und committet (`499d9be`, vollständiger Session-Block in
`phase8_5_picker_release/CLAUDE.md`); Modul-Status A1 `⬜` → `🟡` (Tests ⬜, Browser-Nachweis
folgt in Block C Station 6/8). **Drift-Korrektur in diesem Commit:** Wurzel-Current-state
+ `docs/INDEX.md` Phase-8.5-Eintrag + `ROADMAP.md` Phase-8.5-Absatz waren seit dem A1-Commit
versehentlich nicht nachgezogen — Phase-eigene Hard-Rule-8-Erweiterung (INDEX-Zeile +
ROADMAP + Wurzel-Current-state im selben Commit) verlangt das eigentlich; INDEX-Bullet-
Lücke (`phase8_5_picker_release/CLAUDE.md` + `SESSIONS_ARCHIVE.md` fehlen komplett unter
„Phase 8.5 — 🔄 …") geht auf die Planungs-Commit-Widmung im Step-0-Block zurück („drei
INDEX-Zeilen … bereits durch den Nikinger angelegt" — die dritte Zeile fehlte real).
Auflösung in einem Folge-Commit mit INDEX-Trimmung. **`pytest` 959/959 unverändert**,
Tabu-Diff §0.3 leer (kein Code-Touch in beiden Commits), ui_budget 5/5 (127.6 KB nach A1
+1.8 KB), `node --check` grün auf dialogs.js/editor.js/app.js, Service-Touch 0 (PID 195922,
ActiveEnterTimestamp 2026-09-02 11:51:57 CEST — nur gelesen). Nächster Schritt: A2
(Tastaturnavigation + CSS-Block-Entdopplung am Picker, `app.js` tabu).

**[2026-09-04] Phase 8.5 — 🔄 A2 committet, 🟡, ⬜ B1 als Nächstes.** A2 (`aria-activedescendant`-
Tastaturnavigation + gemeinsamer Pick-Pfad `_pickLinkPickerAt` + CSS-Block-Entdopplung am
Picker) gebaut und committet (vollständiger Session-Block im Phase-Head, A1-Block nach
`SESSIONS_ARCHIVE.md` rotiert); `dialogs.js` neue Modul-Variablen `linkPickerItems`/
`linkPickerCursor`, neuer `_renderLinkPickerResults`-Aufbau mit State-Reset ganz oben,
neue Helper `_setLinkPickerCursor`/`_pickLinkPickerAt`, neuer keydown-Handler am
Suchfeld (ArrowDown/ArrowUp/Enter, kein Wrap, kein Home/End, kein Raten; Escape bleibt
beim globalen Handler); `app.css` zwei identische Auswahl-Blöcke zusammengezogen, totes
`:focus` raus; drei neue statische Tests in `test_static_routes.py`
(`test_link_picker_css_has_one_selection_block` P8.5-14, `test_link_picker_picks_run_
through_a_single_helper` P8.5-12, `test_insertAtCursor_defined_exactly_once_at_module_level`
P8.5-9 nachgezogen — A1 hatte diese drei statisch zu belegen zurückgestellt); Modul-Status
A2 `⬜` → `🟡`, Abnahmestand **3 ✅ · 3 🟡 · 14 ⬜ von 20**. **`pytest` 962/962** (959 + 3 neu,
keine Regressionen), Tabu-Diff §0.3 leer (kein `storage/`/`mcpserver/`/`security.py`/`api.py`/
`serializers.py`/`permissions.py`-Touch), ui_budget 5/5 (128.7 KB, +1.1 KB durch `dialogs.js`
11.7 → 12.6 KB), `node --check` grün auf `dialogs.js`, Service-Touch 0 (PID 195922,
ActiveEnterTimestamp 2026-09-02 11:51:57 CEST — nur gelesen). Nächster Schritt: B1
(`_TITLE_NOT_ID_HINT` generalisierend schärfen in `mcpserver/tools.py:159-164`, einzige
erlaubte Tabu-Ausnahme).

**[2026-09-05] Phase 8.5 — 🔄 D1 committet, 🟡, ⬜ D2–D5 als Nächstes.** Release-
Vorbereitung opencode/M3 (Hard Rule 8 im selben Commit): Badge `v3.0` → `v3.0.1` in
`phase5_ui/webui/static/app.html:20` (P8.5-N7, statisches HTML ist nicht im Tabu §0.3);
neuer `## 2026-09-05`-Block in `docs/UPDATE_LOG.md` mit drei menschenlesbaren Zeilen
(Picker-Modi, Tastatur, Generalisierter Hint). **Datums-Drift ausdrücklich dokumentiert:**
Block-C-Absatz von gestern hatte noch `## 2026-09-04` vorgeschlagen — heute ist
`date +%F`/`date -u +%F` = 2026-09-05, und `deploy.sh` Z. 117–131 verlangt strikt
`today_utc`/`today_local` als oberstes Datum, sonst Gate-Abbruch. Block-C-Block per Hand
nach `SESSIONS_ARCHIVE.md` rotiert (newest-first, vor B1); Skript
`scripts/rotate_session_block.sh` passt nicht auf das Phase-8.5-Muster mit einem
`## Session stopped`-Header + mehreren `### date`-Subblöcken (Skript zählt nur den
`## Session stopped`-Marker und sieht immer genau einen → Exit 2 „Bereits konform").
Modul-Status D `⬜` → `🟡` mit D2–D5 als Nikinger-Aktionen vermerkt. **`pytest` nicht
gelaufen** (kein Python-Touch), Tabu-Diff §0.3 leer (`app.html` und `docs/UPDATE_LOG.md`
nicht tabu), Service-Touch **0** (PID 195922 / ActiveEnterTimestamp 2026-09-02 11:51:57
CEST nur gelesen). **Nächster Schritt:** D2 — Deploy als **Nikinger-Aktion** (`sudo
systemctl ... deploy.sh main` in interaktiver Vordergrund-Shell, V103 prüft den
`sudo`-Prompt; Hard Rule 9 — niemals `sudo systemctl` durch opencode/M3), danach D3
Health-Gate 3/3 + V105, D4 Sichtprüfung am echten Gerät + P8.5-19-Abnahme, D5 Vierte
A3-Probe (entscheidet §9.4.1 Abbruchregel aus N2), Z Closeout.

**[2026-09-06] Phase 8.5 — 🔄 D4-Sichtprobe-Folgesession durch den Nikinger (Notiz-Session, kein Code-Touch in dieser opencode/M3-Session), ⬜ D5/V105 als Nächstes, dann Z.** Im
Anschluss an D4 hat der Nikinger mit Fabian **sieben neue Themen-Cluster** aus
der Sichtprobe gesammelt, die über den D4-Sichtprüfungs-Scope hinausgehen und in
**p8.X** gehören: §1 Spaces-Layout-Reorg [„Alle Items"-Leiste unter Spaces +
Kippschalter, Map 40 % Breite/volle Höhe, keine Duplikate]; §2 Obsidian-Map fünf
Sub-Punkte [Performance-Reload, Landkarten-Stil, Field schneidet ab, Reload-Drift,
Collapsible mit Abhängigkeiten]; §3 Anzahl-Anzeige Ordner; §4 Edit-in-Place-Vision
[„Bearbeiten"-Knopf überflüssig, Word-ähnlich im Read-View editieren — harter
Konflikt mit Hard Rule 3 „kein Last-Write-Wins" und P7-24-Reauth-Grant-Mid-Edit];
§5 Layering-Design-System [3 Layer: echtes Schwarz / aktueller Standard /
Liquid Glass + Selektion explizit blau auf Hover, Note-Select, Checkbox,
größter Brocken]; §6 „Konto"→„Einstellungen"-Rename + Positions-Tausch mit
Logout; §7 De-AI-ierung-Lauf 2 [nach **neuen** Kriterien, dann positive
Erstellungs-Regeln]. **Neue Datei `docs/concepts/p8x_ui_polish_notes.md`** (L2,
25 KB, 2026-09-06) sammelt alle 16 Themen — fünf bereits in D4 dokumentierte
p8.X-Punkte + die sieben neuen Cluster + vier Sub-Punkte aus §2; Anhang §A–§E
(D4-Duplikat-Verweise, klare Außenkanten, sechs offene Fragen für die
Planungs-Session, Namens-Konvention, chronologische Tabelle). **Bewusst kein
Plan, kein Locking, keine Tabu-Aufhebung** — Sammlung, Strukturierung, kein
Phase-8.5-Scope-Touch. Doku-Updates im selben Zyklus: `phase8_5_picker_release/
CLAUDE.md` aktiver Block auf Folgesession umgestellt, D4-Block nach
`SESSIONS_ARCHIVE.md` rotiert; `docs/INDEX.md` neue Sektion „## Phase 8.X" +
Phase-8.5-Header-Hinweis; `ROADMAP.md` neue Sektion + Tabellen-Zeilen P8.5 + P8.X
(korrigiert); `phase8_ui_graph_plan.md §9.4.7` Anker auf neue Notizen-Datei
(folgt); pytest nicht gelaufen (kein Python-Touch), Tabu-Diff §0.3 leer,
Service-Touch 0 (letzter Stand 2026-09-05 16:10:18 CEST / PID 355956,
Hard Rule 9 + §0.5.7 — diese Session ist reine Doku, kein `sudo systemctl`).
**Nächster Schritt:** D5 (Vierte A3-Probe, Nikinger, entscheidet §9.4.1
Abbruchregel) + V105 (Connector-Check, Nikinger); optional vor Z durch
opencode/M3: Radiogruppe-Tausch + Bracket-Fix, damit Z die Endabnahme-Zeilen
P8.5-6 + P8.5-19 auf ✅ heben kann; dann Z (Phase-8.5-Closeout) mit
Phase-8-✅-Nachtrag + p8.X-Ankündigung, jetzt mit Verweis auf
`docs/concepts/p8x_ui_polish_notes.md` als Wahrheits-Quelle.

**Größenstand am Session-Ende (Ist-Werte, Notiz für die nächste Session /
für Z):** `CLAUDE.md` (Wurzel) **55.014 B** (+7.015 B durch diese Session,
deutlich über dem 40-KB-Softcap, signifikantes Wachstum — Wurzel-CLAUDE.md
näher am 56-KB als am 40-KB-Cap, Auflösung bleibt eine Phase-8-Z-Entscheidung
aus Z wie schon D3 dokumentiert hat); `ROADMAP.md` 43.819 B (neu über dem
Softcap, erstmals so notiert, **+1.406 B** durch neue Phase-8.X-Sektion + zwei
Tabellenzeilen); `docs/INDEX.md` 49.556 B (war schon über Cap, **+4.772 B**
durch neue Phase-8.X-Sektion + L0-Zeile); `docs/concepts/p8x_ui_polish_notes.md`
neu, 25.489 B; `phase8_5_picker_release/CLAUDE.md` 39.679 B (**knapp unter
Cap**, +1.641 B); `phase8_5_picker_release/SESSIONS_ARCHIVE.md` 75.330 B (L3,
exempt). **Kein** stilles Trimming — Pattern wie schon D3/D4: dokumentieren,
nicht kürzen; Auflösung ist Z-Arbeit.

**[2026-09-06] Phase 8.5 — 🔄 D4 Sichtprüfung am echten Gerät durch den Nikinger, alles nur dokumentiert, ⬜ D5/V105 als Nächstes, dann Z.** Block 1–7 + Vorbereitung komplett durchgelaufen, beide Accounts in Firefox+Chrome+Safari; Update-Banner `## 2026-09-05` mit drei Zeilen sichtbar ✅, beide Picker-Modi funktional ✅ (eigenes `localStorage["sfx:linkpicker:mode"]` bestätigt), Tastaturnavigation geht über die Mindestanforderung Chromium+Firefox hinaus, Insert-at-cursor-Hub Bild-Knopf ✅, Settle-Zeit 2 s unter 3 s-Ziel, alle drei Graph-Farben, Knotenklick öffnet das Item, Conflict-Dialog gegen Speicherbutton-Spam bewährt (Hard Rule 3 „kein Last-Write-Wins" hält). **Drei echte Findings — Scope-Entscheidungen alle in dieser Session getroffen, Fixe in Folge-Sessions:** (1) **P8.5-19 Radiogruppe statt `<select>`** — Nikinger-Präferenz „deutlich angenehmer", P8.5-F-Planer-Substitution raus, Tausch 5 Z. in `dialogs.js:584`+`app.html:277` ausstehend, Lucide-Icons `link-2`+`pilcrow`/`text-cursor-input` als Vorschlag offen; (2) **P8.5-6 Bracket-Renderer-Bug** — Source-Escape `\[`/`\]` korrekt im Body, aber `markdown.js`-Link-Parser bricht in Vorschau (eckige Klammern ja, runde nein), §0.3 erlaubt `webui/static/js/`, Hard-Rule-9-Eskalation greift nicht (Ursache liegt genau im Fix-Pfad), Fix-Pfad vor Z; (3) **UX-2-Step-Knotenklick** — neues Feature „erster Klick Readonly-Vorschau, zweiter Klick vollständig" für p8.X parkiert, Fabi sammelt gerade. Drei Parken-bestätigt (vom D3-Handover übernommen): Map-Field schneidet unten ab, Map fliegt bei jedem Reload, Save-Button-YAML-Header-Issue (wahrscheinlich p8.X, Verifikation ob außerhalb Header-Kontext steht aus). **Phase 8 ✅ + p8.X als Folge-Phase** als Nikinger-Entscheidung für Z vorgemerkt. Modul-Status Zeile 6 Block D jetzt D1 ✅ + D2 ✅ + D3 ✅ + D4 ✅, D5 ⬜ + V105 ⬜ weiter Nikinger; P8.5-6 mit Bracket-Caveat, P8.5-17 Update-Banner-Teil ✅; Summary 3 ✅ · 14 🟡 · 3 ⬜. D3-Block per Hand nach `phase8_5_picker_release/SESSIONS_ARCHIVE.md` rotiert (Skript passt nicht auf Phase-8.5-Muster). **Nächster Schritt:** D5 (Vierte A3-Probe, Nikinger, entscheidet §9.4.1 Abbruchregel) + V105 (Connector-Check, Nikinger); optional vor Z durch opencode/M3: Radiogruppe-Tausch + Bracket-Fix, damit Z die Endabnahme-Zeilen auf ✅ heben kann; dann Z (Phase-8.5-Closeout) mit `phase8_ui_graph_plan.md §9` + Phase-8-✅-Nachtrag.

**[2026-09-05] Phase 8.5 — 🔄 D2 vom Nikinger zwischen D1 und D3 + D3-Prep, 🟡, ⬜ D4/D5/V105/Z als Nächstes.** D2 ist **zwischen D1 (Commit heute früh) und D3 (diese Session) still durch den Nikinger gelaufen** — Entdeckung kam erst beim ersten Probe-Lauf des Health-Gate-Skripts: `/opt/sharefyx/current` → `20260905T140325.378914Z` → HEAD `6f19a8f` (D1), Service-PID **355956** (statt der im D1-Block notierten 195922 — D2-Deploy hat den Dienst erwartungsgemäß neu gestartet), `ExecMainStartTimestamp=2026-09-05 16:10:18 CEST`. Damit ist D3 nicht mehr Vorbereitung, sondern **Verifikation des bereits deployten v3.0.1**. Neu gebaut: `phase8_5_picker_release/scripts/health_gate.sh` (134 Zeilen bash, `set -uo pipefail`, JSON auf stdout / Details auf stderr nach Hard Rule 7), acht Gates — `/health` 200 mit Retry-Loop, `/ui/login` 200, `/api/v1/me` 401, `/mcp/` 401, `.rail__version` aus `/ui/static/app.html` (**nicht** `/ui/login` — `pages.py`s Auth-Template ohne Rail, erste Iteration fiel darauf herein, gefixt), `/opt/sharefyx/current` → Release mit `.git`, optional `--require-todays-update-log` (UTC/local wie `deploy.sh` Z. 127-131), optional `--expected-sha=<hex>` (Short- oder Full-Form per Prefix-Vergleich). **Lauf-Beleg 2026-09-05 15:19:53Z** mit `--require-todays-update-log --expected-sha=6f19a8f`: **8/8 grün**, Exit 0, JSON auf stdout (`result:"ok"`, `actual_version:"v3.0.1"`, `release_sha:"6f19a8f..."`, `active_release:"/opt/sharefyx/releases/20260905T140325.378914Z"`, `port:8765`). Drei Negativproben separat verifiziert (Port 9999 → Gate 1 rot, `--expected-version=v9.9.9` → Gate 5 rot, `--expected-sha=0000000` → Gate 8 rot). **P8.5-17 teilweise abgehakt:** Deploy gelaufen ✅, Health-Gate 8/8 ✅, Badge `v3.0.1` live ✅, Update-Banner-Live-Anzeige ⬜ (braucht Auth, Nikinger), V105 ⬜ (echter Anthropic-Connector, Nikinger). Modul-Status-Zeile 6 Block D um D2 ✅ + D3 🟡 erweitert; Abnahmestand-Zeile P8.5-17 Health-Gate-Teil 🟡; Summary **3 ✅ · 14 🟡 · 3 ⬜ von 20**; D1-Block (111 Zeilen) per Hand nach `SESSIONS_ARCHIVE.md` rotiert (Skript passt nicht auf das Phase-8.5-Muster — bewährtes Vorgehen aus D1 selbst). `pytest` nicht gelaufen (kein Python-Touch), `bash -n` OK, shellcheck nicht verfügbar (übersprungen, keine Konvention im Repo), Tabu-Diff §0.3 leer, Service-Touch 0 (PID 355956 nur gelesen). **Nächster Schritt:** D4 — Sichtprüfung am echten Gerät durch den Nikinger (`## 2026-09-05`-Eintrag im Update-Banner sichtbar, `<select class="input" id="link-picker-mode">` im Picker vorhanden — P8.5-19-Abnahme: Radiogruppe oder `<select>`-Bestätigung), D5 Vierte A3-Probe (entscheidet §9.4.1 Abbruchregel aus N2), V105-Connector-Check, Z Closeout.

**[2026-09-04] Phase 8.5 — 🔄 Block C committet, 🟡, ⬜ Block D + Z als Nächstes.** Voller
v3-Vorabritt (Plan §4) gegen eine Wegwerf-Instanz auf Port 18773 gefahren:
`phase8_5_picker_release/scripts/wegwerf_setup_v3ritt.py` (Wegwerf-Setup mit Standing-
Permission-Muster aus Phase 8: eigener Port, tmp-`DATA_ROOT`/tmp-`auth.sqlite3`/File-
Keyring; 30 Items über drei Spaces — 12 alpha + 10 beta + 8 gamma; ein archiviertes
Item, ein Item mit item-level `share_read=["gamma"]` (Deploy-Blocker-Fall aus P6 §35–
39), ein Item mit Bild-Asset (`ast_351d4217` per `put_asset()`); 11 explizite Kanten,
darunter die für V102 präparierte Zwillings-Kante body+frontmatter zwischen
`alpha:Buecherliste Q4` und `alpha:Empfehlungen Nikinger`); 16 Screenshots
`docs/screenshots/v3ritt_{chromium,firefox}_NN_*.png`. **`v3_ritt_playwright_smoke.py`:
13/13 Stationen grün in Chromium UND Firefox — 26/26 gesamt** (V101 beantwortet für beide
Browser). Drei **echte Befunde**, keine Code-Fixes im Tabu-Bereich nötig:
- **Smoke-Bug** (gefixt in dieser Session): Edge-Keys waren `src`/`dst` (konsistent mit
  `graph.js:325/394`), nicht `src_id`/`dst_id` wie im Smoke angenommen; ist beim
  V102-Vergleich aufgefallen, Smoke korrigiert, **kein Server-Bug**.
- **CSRF-Origin-Mismatch** zwischen Wegwerf-UI (`http://127.0.0.1:18773`) und
  konfiguriertem `SPACE_PUBLIC_BASE_URL` (`https://wegwerf-v3ritt.invalid`); `_validate_base_url`
  erzwingt https. Konsequenz: jeder `fetch()` mit POST/PATCH aus dem Browser-Kontext
  wird abgewiesen, das macht Station 13 (P8-1-Reauth-Grant-Mechanismus) im Wegwerf
  unscharf — der Live-Nikinger-Domain-Test in Block D fängt das auf. **Befund für
  Step Z / Plan-§4.C3.**
- **Pickstation 12 nur strukturell** (`@media (prefers-reduced-motion)` als Regel im
  CSS gefunden, aber keine echte Browser-Probe mit umgeschaltetem UA). War schon in
  Phase 8 `p8_22_smoke.py` throwaway-verifiziert (Fix A, 2,7 s statt 5,95 s); bleibt
  so.
- Modus-Selektor `<select>` vs. N3-Vorschau-`<input type="radio">`: **nicht als Befund
  behandelt** — die N3-Entscheidung war „Umschalter im Dialog" (P8.5-E), die Bauform
  `<select>` ist eine Planer-Substitution (P8.5-F), die der Nikinger in Block D4 am
  echten Gerät abnimmt (Abnahmezeile P8.5-19). Modul-Status C `⬜` → `🟡`, Abnahme-
  stand **3 ✅ · 13 🟡 · 4 ⬜ von 20** (P8.5-5, -6, -7, -8, -10, -11, -13, -15, -16 alle
  `⬜` → `🟡`; P8.5-3 bleibt `🟡` mit Klammer-Anmerkung für Live-D5). **`pytest` 962/962**
  unverändert (kein Python-Touch im Block-C-Setup, kein `phase5_ui/webui/`-Touch im
  Smoke), Tabu-Diff §0.3 leer, Wegwerf sauber abgebaut (`kill -TERM $(cat serve.pid)`,
  Hard Rule 9-konform), Produktion nachweislich unangetastet (PID 195922 / ActiveEnter
  2026-09-02 11:51:57 CEST vor/nach identisch). Nächster Schritt: **Block D** —
  Release-Vorbereitung (`.rail__version` `v3.0` → `v3.0.1`, neuer `## 2026-09-04`-Block
  in `docs/UPDATE_LOG.md`, drei Zeilen menschenlesbar zum Phase-8.5-Deploy), D2 Deploy
  als **Nikinger-Aktion** (Hard Rule 9 + P8.5-Q, niemals `sudo systemctl restart
  sharefyx-mcp` durch opencode/M3), D3 Health-Gate, D4 Sichtprüfung am echten Gerät,
  D5 Vierte A3-Probe (an der die Abbruchregel §9.4.1 fällt oder hält).

**[2026-09-04] Phase 8.5 — 🔄 B1 committet, 🟡, ⬜ Block C als Nächstes.** B1 (Hint generalisierend

**[2026-09-01] Phase 8 — 🔄 Block A + B ✅ live-verifiziert, Gate B→C bestanden.** UI-Neuanstrich v3,
Verknüpfungs-Graph (`GET /api/v1/graph` + `item_links`-Tabelle + `linkscan.py` + UI-Wiring), drei
P7-Erbposten (P7-24 Reauth-Grant ✅, `remove-space`-Auto-Reindex ✅, P7-4 Zweitprobe 🟡 mit
benanntem Restdefekt Klammer/Aufzählung). Plan: `docs/concepts/phase8_ui_graph_plan.md` (N1–N12
gelockt, P8-A–P8-Q, Abnahme P8-1–P8-24, `[VERIFY]` V81–V92). Kernentscheidungen: P7-24-Fix als
**Reauth-Grant** (vierte Option, in der Planung gefunden — kein Aufweichen des Anti-Replay),
**achte P1-Contract-Öffnung benannt** (Link-Extraktion beim Indexieren für den Graphen), Design
v3 (IBM Plex, Lucide-Sprite, Farblegende own/shared/foreign, Glass-Akzente mit Fallback).
**Ausführung erstmals opencode/M3, ohne Advisor-Stufe (N12)** — Ersatz: Plan §0.6 +
zwei Nikinger-Sichtprüfpunkte. Closeout wird §9 des Plans (ein Dokument pro Phase, P8-N).
**Gate B→C (2026-09-01)** alle vier Bedingungen grün: 958/958 pytest, Charakterisierung
byte-identisch, Tabu-Diff leer, `_graph_get` manuell gegen 3 Spaces + 12 ACL-Fälle 12/12,
Playwright-Smoke gegen Wegwerf-Instanz 18/18 (Picker + `#item/`-Navigation).
**Nächster Schritt:** Block C (Design-Fundament v3, Plan §4) — C0 Anti-AI-Research →
C1 Plex → C2 Lucide → C3 Farbsemantik → C4 Glass → C5 Dichte.

**[2026-08-28] Phase 8 geplant — ⬜ nicht gestartet.** UI-Neuanstrich v3, Verknüpfungs-Graph,
drei P7-Erbposten. Plan: `docs/concepts/phase8_ui_graph_plan.md` (N1–N12 gelockt, P8-A–P8-Q,
Abnahme P8-1–P8-24, `[VERIFY]` V81–V92). Kernentscheidungen: P7-24-Fix als **Reauth-Grant**
(vierte Option, in der Planung gefunden — kein Aufweichen des Anti-Replay), **achte
P1-Contract-Öffnung benannt** (Link-Extraktion beim Indexieren für den Graphen), Design v3
(IBM Plex, Lucide-Sprite, Farblegende own/shared/foreign, Glass-Akzente mit Fallback).
**Ausführung erstmals opencode/M3, ohne Advisor-Stufe (N12)** — Ersatz: Plan §0.6 +
zwei Nikinger-Sichtprüfpunkte. Closeout wird §9 des Plans (ein Dokument pro Phase, P8-N).

**[2026-08-28] Phase 7 abgeschlossen — ✅ live-verifiziert.** Space-Verwaltung in der
Weboberfläche, Mehrfachauswahl, Konsolidierung (`phase7_spaces_admin/`, kein eigenes Python-Paket)
sind gebaut, live deployt (`main`@`e88a624`, 2026-08-27) und abgenommen. **Abnahmestand: 22 von 24
Zeilen ✅, 2 ❌, 0 ungeprüft** — die Matrix ist vollständig durchgelaufen; das unterscheidet diese
Phase von P6/P6.5, wo Zeilen ungeprüft blieben. **Der Sprung auf ✅ ist eine Nikinger-Entscheidung
vom 2026-08-28** unter der Bedingung, dass die beiden ❌ als benannte Defekte an Phase 8 vererbt
werden: **P7-24** (`list.js :: moveSelectedItems()` reicht denselben TOTP-Code an jedes
sequenzielle PATCH einer Batch-Runde — der Server lehnt den Replay korrekt ab, ein Batch mit N
rechteerweiternden Items braucht real N Codes statt einem; echter Mechanismus-Defekt, Fix
bewusst in P8) und **P7-4** (Claude nennt Menschen gegenüber IDs statt Titeln, trotz der Anweisung
in vier Tool-Beschreibungen — kein Code-Fehler). **Dritter Erbposten aus dem Live-Betrieb:
`spacectl.py remove-space` reindiziert den SQLite-Index nicht** — der Incident vom 2026-08-27
(`GET /api/v1/overview` → 500 für jeden eingeloggten Nutzer) kam genau daher; der Zustand ist
per `space_cli.py reindex` behoben, die Ursache nicht. Sechste und siebte P1-Contract-Öffnung mit
dieser Phase geschlossen, keine achte angekündigt. **Einstiegsdokument für die Phase-8-Planung:
`docs/concepts/PHASE7_CLOSEOUT_HANDOVER.md`** (dort §4 die offenen Entscheidungen, §7 die
geänderte Arbeitsweise: Claude Code plant, opencode/M3 führt aus). Übersichtsgrafik:
`docs/concepts/phase7_spaces_admin_uebersicht.svg`. **Die folgenden Absätze bleiben als
Verlaufsdokumentation stehen.**

**[2026-08-23] Phase 7 aktiv — Space-Verwaltung, Mehrfachauswahl, Konsolidierung**
(`phase7_spaces_admin/`, kein eigenes Python-Paket) — **🔄, Block A weit fortgeschritten.** Step 0
(Haushalt + Doku-Audit) ✅, danach A1/A2 (Item-ID sichtbar+auffindbar)/A3 (Bild-Entfernen-Knopf,
schließt P6.5-12)/A4 (Feld-Whitelist, schließt O6) gebaut, A5 (Sichtbarkeits-Migration) live
`--apply` gefahren, A7/A7b (dritter Principal `testnutzer-p7` + `testcred.py`) live angelegt,
**A8 (formaler Abschluss Phase 6.5) durchgeführt** — siehe unten. Verbleibend in Block A: A6
(Purge-Gate, kalendarisch frühestens 2026-08-28). Plan: `docs/concepts/
phase7_spaces_admin_plan.md` (Entscheidungen P7-A–P7-W, alle zehn Nikinger-Fragen N1–N10 gelockt
in §0.1). Phase-Head: `phase7_spaces_admin/CLAUDE.md`.

**[2026-08-27 Korrektur]** Der Absatz oben blieb seit dem Phasenstart stehen und ist überholt.
**Phase 7 ist inhaltlich vollständig** — Block A (inkl. A8, Phase 6.5 formal abgeschlossen),
Gate A→C, Block C (C1–C5, Space-Verwaltung in der Weboberfläche) und Block B (Mehrfachauswahl,
`ITEM_MOVE_PLAN.md` §9) sind alle gebaut. **Live deployt, 2026-08-27, Nikinger-Lauf:**
`/opt/sharefyx/current` → `e88a6244d8eebb5d08d1d93c4a2725f84a2f5971`, Health-Gate 3/3 grün
(`/ui/login`→200, `/api/v1/me`→401, `/mcp/`→401 — alle drei die erwarteten Antworten, kein
Fehlschlag). **[2026-08-28 Korrektur]** Abnahmezeilen 31–34 (`ITEM_MOVE_PLAN.md` §9.5) sind seither
vom Nikinger selbst live gegen die echte Instanz bestätigt — 32/33/34 ohne Vorbehalt, 31 mit dem
bereits bekannten P7-24-TOTP-Vorbehalt (kein neuer Fund, Fix in der nächsten Phase). **A6
(Purge-Gate/P7-9) ebenfalls gefahren** — `token_families` 35→31, `clients` unverändert 54 wie
erwartet (90-Tage-Fenster erst 2026-10-27). **Kein offener Test/Gate mehr.** Verbleibend: Step Z
Rest (Phase-7-Closeout-Dokumente, Übersichtsgrafik, Rotationsprüfung). **Noch nicht ✅** — „✅
heißt live-verifiziert, nicht gebaut", der formale Sprung folgt erst mit dem Closeout. Details:
`phase7_spaces_admin/CLAUDE.md`, aktueller Session-Block.

**[2026-08-23, P7 Step A8] Phase 6.5 formal abgeschlossen als 🟡 — code-complete und live
deployt, aber NICHT vollständig live-verifiziert.** Bewusst **nicht** ✅: **12 von 14
Abnahmezeilen** live, davon zwei (P6.5-8/13) über eine im P7-Plan §A8.1 gebilligte Substitution
— `testnutzer-p7` statt Fabian, derselbe serverseitige Rechte-Code-Pfad. Verbleibend offen:
P6.5-12 (Entfernen-Knopf jetzt von P7 Step A3 gebaut, kein Browser-Klick-Nachweis) und P6.5-14
(Nikingers eigene Bewertung, kein Selbstzertifizierungs-Kriterium — bleibt strukturell offen).
Handover: `docs/concepts/PHASE6_5_CLOSEOUT_HANDOVER.md`. Übersichtsgrafik:
`docs/concepts/phase6_5_tools_images_uebersicht.svg`. **Der untenstehende Absatz vom
Phasenstart (2026-08-20) bleibt als Verlaufsdokumentation stehen, ist inzwischen überholt.**

**[2026-08-20] Zweite aktive Phase gestartet: Phase 6.5 — Werkzeug-Ergonomie und Bilder**
(`phase6_5_tools_images/`, kein eigenes Python-Paket) — **🔄 Step 0.** Sitzt bewusst zwischen der
noch laufenden Phase 6 und der reservierten Phase 7 (Space-Admin-UI, `app.html` unverändert).
Deckt die fünf noch offenen MCP-Werkzeug-Ergonomie-Punkte (siehe „Noch nicht entschieden" unten —
**jetzt geplant, nicht mehr offen**) und den Abschluss von Block C Bilder ab (löst
`phase6_shares/IMAGES_PLAN.md` als maßgebliche Quelle ab). Plan: `docs/concepts/
phase6_5_tools_images_plan.md` (Entscheidungen P6.5-A–P6.5-V, alle sechs Nikinger-Fragen N1–N6
gelockt in §0.0). Phase-Head: `phase6_5_tools_images/CLAUDE.md`.

**[2026-08-23] Phase 6 abgeschlossen als 🟡 — code-complete und live deployt, aber NICHT
vollständig live-verifiziert.** Bewusst **nicht** ✅: nur **12 von 39 Abnahmezeilen** sind
live-verifiziert, vier (31–34, §9 Mehrfachauswahl) wurden nie gebaut, Block C ist nach Phase 6.5
ausgewandert, sieben Zeilen hängen an einer Sitzung mit Fabians eigenem Login. Es gibt bewusst
**kein** `P6_ABNAHME_<datum>.md` — der Zeilenstatus steht in
`docs/concepts/PHASE6_CLOSEOUT_HANDOVER.md` §3. **Der Sprung auf ✅ ist eine offene
Nikinger-Entscheidung.** Zwei Aufgaben sind vom Nikinger ausdrücklich für die nächste Phase
benannt: (1) **Doku-Audit** der Modul-Status-Zeilen 8–16 in `phase6_shares/CLAUDE.md`, die noch
„gebaut, noch nicht deployt" tragen — vermutlich stale, wie sich am 2026-08-23 schon für die
globale Suche zeigte, aber **zu prüfen, nicht zu raten**; (2) **kein Entfernen-Knopf für Bilder**
in `phase5_ui/webui/static/js/editor.js`, obwohl N5 gelockt ist und der `DELETE`-Endpunkt
existiert (blockiert P6.5-12). Übersichtsgrafik: `docs/concepts/phase6_shares_uebersicht.svg`.
**Phase 6.5 ist davon unberührt und läuft weiter.** Der folgende Absatz bleibt als
Verlaufsdokumentation stehen.

**Phase 6 — Freigaben, Ordner, Werkzeug-Ergonomie** (`phase6_shares/`, kein
eigenes Python-Paket) — **offen/Kompakt:** Phase 6 abgeschlossen als `phase6_shares/CLAUDE.md`.
Verlaufsdokumentation zweier Blöcke (Block A Werkzeuge/Betrieb/Update-Banner, Block B
Dateisystem mit SharePolicy-Cutover; Block C Bilder nach 6.5 ausgewandert) ist dort —
Steps 0–3 (patch_item, ua-Feld, Update-Log-Banner) gebaut, Steps 4–6 (Storage-Fundament +
Rechtepolitik + Verwaltung) 2026-08-13 live deployed (`main`@`d068d1c`), IT-Sekus-UI-Fund
(writable-Badge + acht `ownSpaceActive()` zu `activeSpaceWritable()`) geschlossen,
Closeout-Handover `docs/concepts/PHASE6_CLOSEOUT_HANDOVER.md` mit 12-von-39-Live-Bilanz.
**Hard Rule 8:** Phase-6-/6.5-/7-Block-Detailnarrative werden hier nicht mehr dupliziert —
maßgebliche Quelle: die jeweilige `phase*/CLAUDE.md`.

**Deploy-Blocker (2026-08-18) + Funnel-Recovery (2026-08-19) — kompakt:**
Der 2026-08-18 entdeckte UI-Fund („kein über-alle-lesbaren-Items-Suchmodus", item-level-only
`share_*` über Web-UI unauffindbar, nur Connector-Zugriff) wurde 2026-08-19 geplant
(`phase6_shares/GLOBAL_SEARCH_PLAN.md`, P6-AO–AT; Q1: Titel/Tags-only, kein Body-Fulltext) —
Kernbefund im Code verifiziert: `GET /api/v1/items` *ohne* `space`-Parameter ist bereits die
globale, item-weise ACL-gefilterte Suche, es fehlte nur die UI-Fläche (kein neuer
Endpunkt). Steps G1–G2 gebaut (Playwright 10/10 gegen Wegwerf, Advisor-Fund
`editor.js :: clearDetail()` Scope-Reset mitgefixt), `d348e2e` 2026-08-23 zu `f96125e`
korrigiert (Closeout-Sweep) und live deployt. Der 2026-08-19-Funnel-Reboot-Fund (`tailscaled`-
Restart nach VM-Reboot, MagicDNS hatte den öffentlichen Pfad verdeckt) hat
`diagnose.sh`-Prüfung 5 korrigiert; Watchdog/Selbstheilung bewusst offen. Volle
Herleitung beider Punkte: `phase6_shares/CLAUDE.md` Session-Block 2026-08-23 bzw.
`phase3_edge/CLAUDE.md` Abschnitt 2026-08-19.

**[2026-08-19] Block C (Bilder) ist geplant:** `phase6_shares/IMAGES_PLAN.md` (Entscheidungen
**P6-AU–P6-BB**, Abnahmezeilen 40–47) — **fünf offene Nikinger-Entscheidungen B1–B5** (Binärblobs
in der Git-Historie des `DATA_ROOT` vs. Hard Rule 5, Größenriegel, Bildbytes fremder Items vor
einem sehenden Modell als Injektionskanal, den `<untrusted_content>` strukturell nicht erreicht,
MCP-Upload, Löschen eines Bildes vs. Entscheidung H/„kein Delete im Kern-API"). Vor dem Bau
einzuholen, nicht von Claude zu entscheiden.

**Phase 5 — Web-UI, REST-API und Auth-Selbstverwaltung** (`phase5_ui/`, Paket `webui`) — **✅
abgeschlossen, 2026-08-09 — 20/20 Abnahmezeilen live bestanden, 0 teilweise, 0 offen.** Zwei
Blöcke (A = Sicherheit + Auth-Selbstverwaltung, B = REST-API + UI) mit hartem Gate dazwischen,
beide durchlaufen. Menschen setzen ihr Passwort jetzt selbst im Browser, ohne SSH und ohne
Neustart (schließt Betriebsnotiz O1 auch live). Cutover auf `/opt/sharefyx/current` seit
2026-08-05, `deploy.sh`-Zyklus läuft. `git diff` auf `storage/`,
`mcpserver/{tools,permissions,server}.py` blieb über die gesamte Phase leer (Kriterium 18) —
derselbe Seam-Beweis wie in Phase 4, eine API-Fläche höher.

Vollständige Matrix, Modul-Status je Step und die gesamte Live-Debugging-Historie (u. a. der
Origin/CSRF-Fund am Block-A-Gate, die Step-7b-Revision von Plan §4.1/§4.3, Sicherheitsbefund S9)
stehen in `phase5_ui/CLAUDE.md` — read + newest Session-stopped-Block first, das ist die
maßgebliche Quelle für diese Phase, nicht diese Zeile hier. Ältere Session-Blöcke:
`phase5_ui/SESSIONS_ARCHIVE.md`.

Plan: `docs/concepts/phase5_ui_plan.md` (Entscheidungen P5-A–P5-AE, Steps 0–9). Herkunft/offene
Entscheidungen: `docs/concepts/PHASE4_CLOSEOUT_HANDOVER.md`. Abnahmeprotokoll:
`docs/concepts/P5_ABNAHME_2026-08-09.md`. Formaler Abschluss-Handover an P6:
`docs/concepts/PHASE5_CLOSEOUT_HANDOVER.md`.

**[2026-08-09 erledigt]** Vor-Phase-6-Vormerkungen F1 (Subspaces/Shared Spaces), F2 (kein Löschen, nur Archivieren), Client-Surface-Logging (ua-Feld), `patch_item` (gezielter Patch statt Volltext-Rewrite) sind alle in Phase 6 gelandet (`phase6_shares_plan.md`: F1 zu P6-J/K/Q/T, F2 zu §0.5 weiterhin draußen, Logging zu P6-A5/Step 2, `patch_item` zu P6-E/F/G/Step 1, gebaut als siebtes MCP-Tool 2026-08-09). F1b (Space, in dem alle unabhängig volle Rechte haben) bleibt wegen Hard Rule 4 bewusst draußen. Volltext: `phase6_shares/CLAUDE.md` Vormerkungen-Abschnitt.

**Phase 4 — OAuth 2.1 + DCR** (`phase4_auth/`, Paket `authserver`) — **✅ abgeschlossen,
2026-07-30 — 16/16 Abnahmezeilen live bestanden, Schnitt vollzogen.** Der Pfad-Token ist
verschwunden; ein eigener, im selben Prozess laufender Authorization Server (Discovery, Dynamic
Client Registration, PKCE, Argon2id + TOTP, opake rotierende Token) authentifiziert seither jeden
Connector. Kritischer Fund in Step 0: ein nie widerrufener Keyring-Token für einen seit P2
umbenannten dritten Space (`nikinger`) — live und schreibfähig, aber ohne zugehöriges
Verzeichnis; noch vor dem Schnitt widerrufen und live gegen `diagnose.sh`/
`export_space_map.py` bestätigt (Details: `docs/concepts/PHASE3_CLOSEOUT_HANDOVER.md` §5).

Sicherheitsbefunde **S1–S10 / O1–O2** (S1–S8 und S10 geschlossen; O1 strukturell durch P5
geschlossen; **O2 offen** — `clients`/`token_families` werden nie abgeräumt) stehen mit vollem
Verlauf und Fundstellen in `phase4_auth/CLAUDE.md`, ebenso der Modul-Status aller acht Steps und
das ausgeführte Inbetriebnahme-Runbook.

Plan: `docs/concepts/phase4_auth_plan.md` (Entscheidungen P4-A–P4-R, Steps 0–7 — geschrieben ohne
frischen Repo-Zugriff, siehe Plan-Kopf). Herkunft/offene Entscheidungen:
`docs/concepts/PHASE3_CLOSEOUT_HANDOVER.md`. Abnahmeprotokoll:
`docs/concepts/P4_ABNAHME_2026-07-29.md`. Sicherheits-Review vor der Abnahme:
`docs/concepts/P4_SECURITY_REVIEW_2026-07-29.md`. Formaler Abschluss-Handover an P5:
`docs/concepts/PHASE4_CLOSEOUT_HANDOVER.md`.

**Phase 3 — Exposure & Betrieb** (`phase3_edge/`, kein eigenes Python-Paket — Servercode bleibt
in `mcpserver`): ✅ **live-verifiziert, 13/13** — Ursprungsstand 10/13
(`docs/concepts/P3_ABNAHME_2026-07-27.md`). Zeile 6 (Reboot) löste sich am 2026-07-29 durch
einen unbeabsichtigten Reboot der VM (Windows-Host-Neustart des Nikingers), Zeile 12
(Backup-Timer-Lauf) durch einen realen Timer-Lauf in P4 Step 0. **[2026-08-02, P5 Step 0:]**
Zeile 13 (Restore-Nachweis) ist die letzte gefallen — Claude Code fuhr `restore_check.sh`
zunächst selbst als Kandidatenbeleg, der Nikinger führte denselben Lauf danach selbst aus
(identischer HEAD, `ok:true`) — echte Abnahme. **Phase 3 damit vollständig ✅.** Formaler
Abschluss-Handover an P4: `docs/concepts/PHASE3_CLOSEOUT_HANDOVER.md`. Plan: `docs/concepts/
phase3_edge_plan.md` (Entscheidungen P3-A–P3-N gelockt, Steps 0–7). Phase-Head:
`phase3_edge/CLAUDE.md`.

**Phase 2 — MCP-Server** (`phase2_mcp/`, Paket `mcpserver`): ✅ **abgeschlossen,
live-verifiziert seit 2026-07-26** — Quick-Tunnel-Probe + vollständige Adapter-Abnahme über den
echten Custom Connector durch den Nikinger, 21/21 Prüfungen, siehe
`docs/concepts/P2_ADAPTER_ABNAHME_2026-07-26.md`. Claude liest und schreibt über einen lokalen
`fastmcp`-Server auf den P1-Storage-Kern — Token→Space-Auflösung, sechs Tools,
`<untrusted_content>`-Wrapping fremder Bodies. Formaler Abschluss-Handover an P3:
`docs/concepts/PHASE2_CLOSEOUT_HANDOVER.md`. Plan: `docs/concepts/phase2_mcp_plan.md`
(Entscheidungen P2-A–P2-N, Steps 0–7). Phase-Head: `phase2_mcp/CLAUDE.md`.

**Phase 1 — Storage-Kern** (`phase1_storage/`, Paket `storage`): ✅ **abgeschlossen,
live-verifiziert.** Alle acht Module (Steps 0–7), 68 Tests grün (70 bei Phasenabschluss, minus
zwei bei Entfernung toten Codes in P2 Step 0 — siehe `phase1_storage/CLAUDE.md`) —
Frontmatter/Modelle, atomarer Datei-Store, SQLite-Index, Versionierung + Konfliktbehandlung,
Git-Commit je Write, Query-Layer, `space_cli.py` als Beweis. Der Nikinger hat den Lauf gegen den
echten `DATA_ROOT` (`/home/savefyx/savefyx-data`) selbst ausgeführt (2026-07-25, Hard Rule: kein
Test gegen den echten DATA_ROOT durch Claude Code). Details + Transkript:
`phase1_storage/CLAUDE.md`, Session-Block. Plan: `docs/concepts/phase1_storage_plan.md`
(Entscheidungen A–H gelockt, Steps 0–7). Die dort definierten Frontmatter-Felder und
`Store`-Signaturen sind ab jetzt Contract für P2 (drei einmalige, freigegebene Erweiterungen in
P2 Step 2 — siehe P2-Plan §0.4 Punkt L).

**Gelockte Rahmenentscheidungen (Nikinger, 2026-07-24, Browser-Planung):**

| # | Thema | Lock |
|---|---|---|
| R1 | Plan/Ausführung | Planung im Browser-Chat, Ausführung in Claude Code — wie im Trading-Bot-Projekt. |
| R2 | Plan-Tier | Beide Nutzer auf **Claude Pro**. Custom Connectors sind auf Pro verfügbar; jeder fügt seinen Connector selbst hinzu (kein Owner-Gate wie bei Team/Enterprise). `[VERIFY]` bei Ausführung gegen die aktuelle Doku. |
| R3 | Erreichbarkeit | **CGNAT** (RUT X50, Mobilfunk). Start mit **Cloudflare Tunnel** (schnellster Weg zum ersten Erlebnis), Migration auf **VPS + WireGuard** als P3-Option. Der MCP-Server ändert sich dabei nicht. **[2026-07-28 Ergänzung, P4 Step 0]:** Gebaut wurde stattdessen **Tailscale Funnel** (P3-A) — weder Cloudflare Tunnel noch VPS+WireGuard. Die Beschlusslage oben bleibt historisch korrekt stehen; Details zum tatsächlichen Weg: `docs/concepts/phase3_edge_plan.md` §0.4. |
| R4 | Vertraulichkeit | Bewusst akzeptiert: bei Cloudflare Tunnel terminiert Cloudflare TLS und sieht Klartext. **Kein E2E.** Der Server muss lesen können, damit Claude lesen kann — das schließt das Krypto-Modell des `Notizheft_example.html` aus. **[2026-07-27 Ergänzung, P3 Step 0]:** Ab P3 läuft der Weg über Tailscale Funnel; dort terminiert die Node selbst TLS, siehe `docs/concepts/phase3_edge_plan.md` §0.4. Der Relay-Betreiber sieht Notizinhalte damit nicht mehr im Klartext — „kein E2E" bleibt trotzdem richtig, denn Tailscale bleibt vertrauenswürdige Infrastruktur (Koordinationsserver, DNS, Relays). |
| R5 | Auth v0 | Token im Pfad (`/mcp/<token>`), Token = Identität = Space. Ehrlich benannter Kompromiss (Bearer-Passwort in einer URL, landet in Logs). **OAuth 2.1 + DCR ist Phase 4**, nicht optional-für-immer. **[2026-07-30 abgelöst, P4 Schnitt:]** Der Pfad-Token existiert nicht mehr — `TokenPathASGI` ist aus dem Code entfernt, beide Pfad-Token live widerrufen, `SPACE_AUTH_MODE` lässt nur noch `oauth` zu. Der Connector authentifiziert sich seither über OAuth 2.1 + DCR (Passwort + TOTP), siehe P4. |
| R6 | Zweck | **Lernprojekt**, später evtl. Arbeitswerkzeug. Bei Zielkonflikt gewinnt Lerneffekt über Bequemlichkeit — außer bei Safety/Secrets, dort gewinnt immer die sichere Variante. |

**Noch nicht entschieden (bewusst offen, für spätere Planungssessions):**
- ~~MCP-Werkzeug-Ergonomie, fünf offene Punkte~~ **[2026-08-20 geplant und gelockt]** — jetzt
  Block A von Phase 6.5 (`docs/concepts/phase6_5_tools_images_plan.md` §3, Entscheidungen
  P6.5-A–P6.5-H u. a.). Kein offener Planungsbedarf mehr — nur noch **nicht gebaut**. Der
  Absatz unten bleibt als Herkunftsnachweis stehen.
- ~~Item-Verschieben zwischen Ordnern und Spaces~~ **[2026-08-17 geplant und gelockt]** —
  `phase6_shares/ITEM_MOVE_PLAN.md` §4 (Step 7b, Space-Move, Entscheidungen P6-AD–AJ) + §9
  (Mehrfachauswahl, P6-AK–AN) sind ausführungsreif und per Nikinger-Freigabe gelockt. Kein
  offener Planungsbedarf mehr — nur noch **nicht gebaut**. Details:
  `phase6_shares/CLAUDE.md`s aktuellem Session-Block.
- **MCP-Werkzeug-Ergonomie, Live-Feedback (2026-08-14, sechs Punkte):** Bulk-Append, `list_spaces` auffindbarer, `patch_item`-vs-`update_item`-Aufgabenteilung, `get_item_meta`-Trennung vom vollen Body, Status-Enum-Doku in der Tool-Beschreibung, Suchtreffer-Robustheit. Der eine Bug (irreführende `patch_item`-Fehlermeldung „0 Treffer — lies das Item neu“ auf Frontmatter-Feldern; `patch_item` erreicht Frontmatter grundsätzlich nicht) ist am 2026-08-14 behoben (Text nennt jetzt die Ursache + `update_item` als Alternative, keine Frontmatter-Erkennungslogik). Übrige fünf Punkte: Phase 6.5 Block A, gelockt in `phase6_5_tools_images_plan.md` Abschnitt 3. Volltext: `phase6_shares/CLAUDE.md` Vormerkungen.

**[2026-08-02 Korrektur]** Web-UI-Planungs-Entscheidung **P5-V** (Neubau mit Ernte aus `notiz_heft_example.html`): Layout + `sanitizeHtml`/`markdownToHtml` übernommen; Vault-Encryption (R4-inkompatibel), `localStorage` und `connect-src 'none'` verworfen. **[2026-07-28 Korrektur]** Kollege-Frage (eigener Prozess vs. eigener Space) ist seit P3-G entschieden und live bewiesen: **ein Prozess, ein Space je Person** — zwei Spaces real (`niklas`, `fabian`) über denselben `sharefyx-mcp.service`.
