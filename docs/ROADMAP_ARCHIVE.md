---
status: archive
purpose: L3-Archiv abgeschlossener Abschnitte von `ROADMAP.md` — verbatim, in Dokumentreihenfolge
read-when: beim Audit, wenn Scope oder Begründung einer abgeschlossenen Roadmap-Phase nachgelesen werden muss
detail: L3
up: ../ROADMAP.md
down:
updated: 2026-10-25 (angelegt in P10.5 Block 12 / LG-6 — `scripts/move_sections.py`, verbatim)
---

## Phase 8.5 — Link-Picker-Politur und v3-Release

**Mission:** drei 🟡-Restdefekte aus Phase-8-Closeout §9.4.1–§9.4.3 schließen, einen vollständigen
v3-Vorabritt über den nie ausgelieferten v3-Build fahren und ihn live deployen — diese Phase
**schließt Phase 8 formal mit ab** (N6, Präzedenz P7 Step A8 für Phase 6.5). ~~**Wichtige Korrektur zum Live-Stand:** v3.0 ist **nicht** ausgeliefert …~~
**[2026-09-05 erledigt]:** der Vorabritt lief 26/26, der Deploy ging durch — live seit
`main@6f19a8f`, Release `20260905T140325.378914Z`, Badge `v3.0.1`, Service-PID 355956.
Der Grund für den vollen 13-Stationen-Ritt (N5) bleibt der richtige: Block C/D waren ein
UI-Umbau, den nie ein echter Nutzer gesehen hatte.

- **DRIN:** Picker-Modus-Umschalter „Text-Link / Kante" mit `localStorage`-Persistenz
  (P8.5-§2 A1); Tastaturnavigation über `aria-activedescendant`-Muster (P8.5-§2 A2); Hint
  `_TITLE_NOT_ID_HINT` generalisierend geschärft mit verbindlicher Abbruchregel (P8.5-§3 B1);
  v3-Vorabritt gegen Wegwerf-Instanz mit 13 Stationen (P8.5-§4 C); Deploy `v3.0` → `v3.0.1`
  als **Nikinger-Aktion** (P8.5-§5 D2, Hard Rule 9); Phase-8-Closeout-Nachtrag
  (`phase8_ui_graph_plan.md` §9).
- **DRAUSSEN:** Phase-8-§9.4.6-Funde (Settle-Zeit / Foreign-Farbe / Knotenklick — bereits am
  2026-09-02 geschlossen), Phase-8-§9.4.7 Glyph-Entscheidung ✅/🟡 (Nikinger-Sache nach
  Live-Deploy + Sichtprüfung), geerbtes Phase-6/6.5/7-Ledger (`phase8_ui_graph_plan.md` §9.4.5),
  FastMCP-4/V79 (eigene Mini-Phase, P5-C), `_trash/`-Räumung, Funnel-Watchdog, Mobile/Realtime,
  Light-Mode, ~~Phase-8.5-Übersichtsgrafik (P8.5-S)~~ **[2026-09-09 aufgehoben, Nikinger]:**
  die Grafik existiert — `docs/concepts/phase8_5_picker_release_uebersicht.svg`, Korrekturnotiz
  im Plan §0.2.

**Plan:** `docs/concepts/phase8_5_picker_release_plan.md` (744 Zeilen, geschrieben 2026-09-03
gegen `main@6272cad`). N1–N7 in §0.1 gelockt, Entscheidungen P8.5-A–P8.5-T, Steps 0/A/B/C/D/Z,
Abnahmezeilen P8.5-1–P8.5-20, `[VERIFY]` V95–V105. **Closeout ist §9 des Plans (gefüllt
2026-09-09, kanonisch); Einstieg für die P8.6-Planung ist
`docs/concepts/PHASE8_5_CLOSEOUT_HANDOVER.md` §4.** **Step 0
abgeschlossen** (Haushalt-Funde, Skelett, Größenkorrekturen); **A1 committet** (`499d9be`,
2026-09-04, Picker-Modus-Umschalter + Body-Markdown-Link-Helper + `localStorage`,
Modul-Status 🟡, Tests ⬜, vollständiger Session-Block im Phase-Head); **Drift nachgezogen**
in einem separaten Folge-Commit (Wurzel-Current-state, dieser Absatz, INDEX-Header);
**A2 committet** (Tastaturnavigation + gemeinsamer Pick-Pfad `_pickLinkPickerAt` +
CSS-Block-Entdopplung am Picker; drei neue statische Tests; Modul-Status 🟡; A1-Block
nach `SESSIONS_ARCHIVE.md` rotiert); **B1 committet** (`_TITLE_NOT_ID_HINT` generalisiert
in `mcpserver/tools.py:159-164` — Schlußsatz „Das gilt in jeder Textform" wörtlich aus
Plan §3 B1; zwei Asserts in `test_tools.py`; Abbruchregel-Abschnitt im Phase-Head;
Modul-Status 🟡; A2-Block nach `SESSIONS_ARCHIVE.md` rotiert); Abnahmestand
**3 ✅ · 4 🟡 · 13 ⬜ von 20**. **nächster Schritt:** **Block C** — v3-Vorabritt gegen
eine Wegwerf-Instanz (Plan §4, 13 Stationen Playwright-Smoke gegen den nie ausgelieferten
v3-Build; Wegwerf-Setup mit tmp `DATA_ROOT`/`auth.sqlite3`/eigenem Port, inkl. Portierung
von `scripts/rotate_session_block.sh` aus Phase 7 für `phase8_5_picker_release/`).

**[2026-09-04, Block C committet]** v3-Vorabritt gegen Wegwerf Port 18773 (V98) gefahren:
`phase8_5_picker_release/scripts/wegwerf_setup_v3ritt.py` (Standing-Permission-Muster aus
Phase 8 reproduziert — eigener Port, tmp `DATA_ROOT`/`auth.sqlite3`, File-Keyring; 30
Items über 3 Spaces alpha/beta/gamma inkl. 1 archiviertes, 1 mit item-level `share_read=
["gamma"]` (P6-§35-39-Deploy-Blocker-Fall), 1 mit Bild-Asset via `put_asset()`; 11
explizite Kanten inkl. V102-Zwillings-Kante Buecherliste ↔ Empfehlungen Nikinger);
`scripts/rotate_session_block.sh` aus `scripts/` nach `phase8_5_picker_release/scripts/`
portiert, YAGNI aus A1/A2 geschlossen; `phase8_5_picker_release/scripts/
v3_ritt_playwright_smoke.py` neu (~720 Zeilen, `pyotp`+`async_playwright`). **Ergebnis:
26/26 Stationen grün** (Chromium 13/13 + Firefox 13/13, V101 für beide Browser
bestätigt); drei echte Befunde vorgelegt, **keine Code-Fixes im Tabu-Bereich nötig**:
(1) Smoke-Bug Edge-Keys `src_id`/`dst_id` → `src`/`dst` (gefixt im Smoke, kein
Server-Bug — passt zu `graph.js:325/394` und `webui/api.py:719`), (2) CSRF-Origin-
Mismatch zwischen `http://127.0.0.1:18773` und `SPACE_PUBLIC_BASE_URL=
https://wegwerf-v3ritt.invalid` wegen `_validate_base_url`-Pflicht (Befund für Step Z /
Plan §4.C3, **nicht** in dieser Phase lösbar ohne Server-Code-Touch), (3) Station 12
nur strukturell (`prefers-reduced-motion`-Regel im CSS gefunden, keine echte
Browser-Probe mit umgeschaltetem UA — bleibt, throwaway-verifiziert in Phase 8
`p8_22_smoke.py`); Modus-Selektor `<select>` vs. N3-Vorschau-Radio nicht als Befund
behandelt (P8.5-F-Planer-Substitution, P8.5-19-Sichtprüfung). Abnahmestand jetzt
**3 ✅ · 13 🟡 · 4 ⬜ von 20** (P8.5-5/-6/-7/-8/-10/-11/-13/-15/-16 aus Block C
`⬜`→`🟡`). 16 Screenshots `docs/screenshots/v3ritt_{chromium,firefox}_NN_*.png` neu.
`pytest -q` 962/962 unverändert (kein Python-Touch im Block-C-Setup), Tabu-Diff §0.3
leer, Service-Touch 0 (PID 195922 / ActiveEnterTimestamp 2026-09-02 11:51:57 CEST
nur gelesen; Wegwerf PID 337447 sauber abgebaut via `kill -TERM $(cat serve.pid)`,
Hard Rule 9-konform). **nächster Schritt:** **Block D** — Release-Vorbereitung
(`v3.0` → `v3.0.1`, neuer `## 2026-09-04`-Block in `docs/UPDATE_LOG.md` mit drei
menschenlesbaren Zeilen), D2 Deploy als **Nikinger-Aktion** (Hard Rule 9 + P8.5-Q,
niemals `sudo systemctl restart sharefyx-mcp` durch opencode/M3), D3 Health-Gate,
D4 Sichtprüfung am echten Gerät, D5 Vierte A3-Probe (an der die Abbruchregel §9.4.1
(N2) fällt oder hält).

**[2026-09-05, D1 committet]** Release-Vorbereitung opencode/M3: Badge `v3.0` →
`v3.0.1` in `phase5_ui/webui/static/app.html:20` (P8.5-N7); neuer `## 2026-09-05`-
Block in `docs/UPDATE_LOG.md` mit drei Zeilen (Picker-Modi / Tastatur / Generalisierter
Hint). **Datums-Drift zur Block-C-Spec ausdrücklich dokumentiert:** Block-C-Absatz oben
hatte noch `## 2026-09-04` vorgeschlagen (geschrieben am 2026-09-04, dem Tag von Block C);
heute ist `date +%F`/`date -u +%F` = 2026-09-05, und `deploy.sh` Z. 117–131 verlangt strikt
`today_utc` oder `today_local` als oberstes Datum, sonst Gate-Abbruch — Eintrag deshalb auf
2026-09-05 datiert. Block-C-Block per Hand nach `SESSIONS_ARCHIVE.md` rotiert
(newest-first, vor B1); Skript `scripts/rotate_session_block.sh` passt nicht auf das
Phase-8.5-Muster mit einem `## Session stopped`-Header + mehreren `### date`-Subblöcken
(Skript zählt `## Session stopped`-Header und sieht immer genau einen → Exit 2 „Bereits
konform"). Modul-Status D `⬜` → `🟡` mit D2–D5 als Nikinger-Aktionen vermerkt. `pytest`
nicht gelaufen (kein Python-Touch), Tabu-Diff §0.3 leer (`app.html` und `docs/UPDATE_LOG.md`
nicht tabu), Service-Touch 0 (PID 195922/ActiveEnterTimestamp 2026-09-02 11:51:57 CEST nur
gelesen). **nächster Schritt:** D2 — Deploy als Nikinger-Aktion
(`SHAREFYX_SYSTEMCTL="sudo systemctl" phase5_ui/scripts/deploy.sh main` in interaktiver
Vordergrund-Shell, V103 prüft den `sudo`-Prompt; Hard Rule 9 — niemals `sudo systemctl`
durch opencode/M3), D3 Health-Gate 3/3 + V105, D4 Sichtprüfung am echten Gerät +
P8.5-19-Abnahme des `<select>`-Modus-Selektors, D5 Vierte A3-Probe (entscheidet §9.4.1
Abbruchregel aus N2).

**[2026-09-05, D2 vom Nikinger zwischen D1 und D3 + D3-Prep committet]** D2 ist zwischen
D1 (Commit heute früh) und D3 (diese Session) **still durch den Nikinger gelaufen** —
Entdeckung kam erst beim ersten Probe-Lauf des Health-Gate-Skripts:
`/opt/sharefyx/current` → `20260905T140325.378914Z` → HEAD `6f19a8f` (D1), Service-PID
**355956** (statt der im D1-Block notierten 195922 — D2-Deploy hat den Dienst erwartungsgemäß
neu gestartet), `ExecMainStartTimestamp=2026-09-05 16:10:18 CEST`. Damit ist D3 nicht mehr
Vorbereitung, sondern **Verifikation des bereits deployten v3.0.1**. Neu gebaut:
`phase8_5_picker_release/scripts/health_gate.sh` (134 Zeilen bash, `set -uo pipefail`,
JSON auf stdout / Details auf stderr nach Hard Rule 7), acht Gates — `/health` 200 mit
Retry-Loop (max `--max-wait` Sekunden, Default 30, wie `deploy.sh` Z. 192-200), `/ui/login`
200, `/api/v1/me` 401, `/mcp/` 401 (wie `deploy.sh` Z. 202-217), `.rail__version` aus
`/ui/static/app.html` (**nicht** `/ui/login` — das ist `pages.py`s Auth-Template und enthält
keine Rail; erste Iteration fiel darauf herein, dann gefixt), `/opt/sharefyx/current` →
Release-Verzeichnis mit `.git`, optional `--require-todays-update-log` (oberster
`## YYYY-MM-DD` in `docs/UPDATE_LOG.md` == heute UTC/local, wie `deploy.sh` Z. 127-131),
optional `--expected-sha=<hex>` (Release-SHA matched Short- oder Full-Form per
Prefix-Vergleich). **Lauf-Beleg 2026-09-05 15:19:53Z** mit `--require-todays-update-log
--expected-sha=6f19a8f`: **8/8 grün**, Exit 0, JSON auf stdout
(`{"action":"health_gate","result":"ok","expected_version":"v3.0.1",
"actual_version":"v3.0.1","active_release":"/opt/sharefyx/releases/20260905T140325.378914Z",
"release_sha":"6f19a8fc1f0bcdc2c3bc91fc934a057964647ed4","port":8765}`). Drei Negativproben
separat verifiziert (Port 9999 → Gate 1 rot, `--expected-version=v9.9.9` → Gate 5 rot,
`--expected-sha=0000000` → Gate 8 rot). **P8.5-17 teilweise abgehakt:** Deploy gelaufen ✅,
Health-Gate 8/8 ✅, Badge `v3.0.1` live ✅, Update-Banner-Live-Anzeige ⬜ (braucht Auth,
Nikinger), V105 ⬜ (echter Anthropic-Connector, Nikinger). Modul-Status-Zeile 6 Block D um
D2 ✅ + D3 🟡 erweitert; Abnahmestand-Zeile P8.5-17 Health-Gate-Teil 🟡; Summary
**3 ✅ · 14 🟡 · 3 ⬜ von 20**; D1-Block (111 Zeilen) per Hand nach `SESSIONS_ARCHIVE.md`
rotiert (Skript passt nicht auf das Phase-8.5-Muster — bewährtes Vorgehen aus D1 selbst).
`pytest` nicht gelaufen (kein Python-Touch), `bash -n` OK, shellcheck nicht verfügbar
(übersprungen, keine Konvention im Repo), Tabu-Diff §0.3 leer, Service-Touch 0 (PID 355956
nur gelesen). **nächster Schritt:** **D4 ✅ erledigt 2026-09-06** (Sichtprüfung am echten Gerät durch den Nikinger,
Update-Banner sichtbar, beide Picker-Modi funktional, drei echte Findings dokumentiert: **P8.5-19
Radiogruppe** statt `<select>` — Tausch 5 Z. ausstehend; **P8.5-6 Bracket-Renderer-Bug** in
`markdown.js` — Fix ausstehend; **UX-2-Step-Knotenklick** als neues Feature für p8.X parkiert;
**Phase 8 ✅ + p8.X** als Nikinger-Entscheidung für Z vorgemerkt); **D5 Vierte A3-Probe**
(entscheidet §9.4.1 Abbruchregel aus N2 — Nikinger-Aktion); **V105-Connector-Check** (echter
Anthropic-Connector — Nikinger-Aktion); **optional vor Z** durch opencode/M3: Radiogruppe-Tausch
(P8.5-19) + Bracket-Renderer-Fix (P8.5-6); dann **Z (Closeout)** mit Phase-8-✅-Eintrag +
p8.X-Ankündigung in `phase8_ui_graph_plan.md §9.4.7`.

---
