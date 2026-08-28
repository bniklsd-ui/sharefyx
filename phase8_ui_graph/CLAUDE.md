---
status: live
purpose: Phase-Head UI-Neuanstrich v3, Verknüpfungs-Graph, drei P7-Erbposten — Scope, harte Regeln, Modulstatus, aktueller Session-Handover
read-when: Arbeiten in phase8_ui_graph/ oder an den in §0.4 des Plans genannten Dateien in storage/mcpserver/webui/scripts — zuerst lesen, zusammen mit dem neuesten Session-stopped-Block
detail: L2
up: ../CLAUDE.md
down:
  - ../docs/concepts/phase8_ui_graph_plan.md       # voller Plan, Entscheidungen P8-A–P8-Q, §0.1 gelockte N1–N12, Steps 0/A/B/C/D/Z
  - ../docs/concepts/PHASE7_CLOSEOUT_HANDOVER.md   # Herkunft der drei Erbposten (P7-24/remove-space/P7-4)
  - SESSIONS_ARCHIVE.md                             # ältere Session-Blöcke, newest-first
updated: 2026-08-28 (Step 0 abgeschlossen -- opencode-ai 1.18.25 global installiert, Minimax-Provider-Auth vom Nikinger gesetzt, Playwright-MCP verbunden (V93), CLAUDE.md-Regeldatei-Kontrollfrage bestanden, Smoke-Test P8-26 auf Wegwerf-Branch bestanden, Harnesswechsel zu opencode/M3 ab Block A freigegeben) | 2026-08-28 (Skelett angelegt, Step 0 Fundament-Session gestartet)
---

# CLAUDE.md — Phase 8: UI-Neuanstrich v3, Verknüpfungs-Graph, QoL (`phase8_ui_graph/`)

> Kein eigenes Python-Paket (wie `phase3_edge/`, `phase6_shares/`, `phase6_5_tools_images/`,
> `phase7_spaces_admin/`) — Servercode bleibt in `storage`/`mcpserver`/`webui`/`scripts`.
> **Quelle der Wahrheit ist der Code, nicht dieses Dokument.**

---

## Mission (zuerst lesen)

Vier Blöcke, Reihenfolge 0 → A → B → Gate → C → D → Z: **A** = drei P7-Erbposten schließen
(P7-24-TOTP-Replay per Reauth-Grant, `remove-space`-Auto-Reindex, P7-4-Zweitprobe) — fällt unter
Druck **nie**. **B** = Link-Fundament, achte P1-Contract-Öffnung (`storage/linkscan.py`,
`item_links`-Tabelle, `GET /api/v1/graph`). **C** = Design-Fundament v3, De-AI-isierung (IBM
Plex, Lucide-Sprite, Farblegende own/shared/foreign, Liquid-Glass-Akzente mit Pflicht-Fallback).
**D** = Übersicht tablos + handgerollter Canvas-Force-Graph.

**Erstmals opencode/M3 als Ausführender ab Block A** (P7-Handover §7) — Step 0 (diese Sitzung)
läuft noch in Claude Code, gemeinsam mit dem Nikinger, und stellt die opencode-Fähigkeits-Parität
her. **Kein Advisor während der Ausführung (P8-L, N12)** — Ersatz: Selbstprüf-Checkliste §0.6 des
Plans + zwei Nikinger-Sichtprüfpunkte.

## Scope

- **DRIN:** die drei P7-Erbposten, Link-Extraktion + Graph-Endpunkt, Design v3
  (Typografie/Icons/Farben/Glas), Übersicht tablos + Force-Graph, `AGENTS.md`-Entfernung,
  opencode-Einrichtung.
- **DRAUSSEN:** FastMCP-4/V79 (eigene Mini-Phase), Body-Volltextsuche, Rechteverwaltung über
  MCP-Tools, neues MCP-Tool für den Graph, Löschen von Items, `_trash/`-Räumung,
  Funnel-Watchdog, Mobile/Realtime, Light-Mode. Volle Liste: Plan §0.5 „DRAUSSEN".

Details, gelockte Entscheidungen P8-A–P8-Q, Verbots-/Tabu-Liste, Schritt-Sequenz, Testliste,
Abnahmezeilen: `docs/concepts/phase8_ui_graph_plan.md`.

**P8-N — ein Dokument pro Phase:** der Closeout wird §9 des Plans, kein separates Handover.

## Modul-Status

| Block | Inhalt | Status |
|---|---|---|
| Step 0 | Fundament-Session (Haushalt, AGENTS.md weg, Skelett, opencode-Setup, Smoke-Test) | ✅ |
| Block A | Erbposten (Reauth-Grant, remove-space-Reindex, P7-4-Zweitprobe) | ⬜ |
| Block B | Link-Fundament (`linkscan.py`, `item_links`, `GET /api/v1/graph`) | ⬜ |
| Block C | Design-Fundament v3 (Typografie, Icons, Farben, Glas) | ⬜ |
| Block D | Übersicht tablos + Force-Graph | ⬜ |
| Step Z | Closeout | ⬜ |

## Geerbte Contracts

Achte P1-Contract-Öffnung (P8-M) wird in Block B benannt und gebaut — Eintrag folgt in
`phase1_storage/CLAUDE.md` §„Geerbte Contracts" im Öffnungs-Commit, nicht hier dupliziert.

## Abnahmestand (Plan §7, P8-1–P8-26)

**Statusregel wie in P5/P6/P6.5/P7: ✅ heißt live-verifiziert durch den Nikinger, nicht
„gebaut".** Noch keine Abnahmezeile geprüft — Step 0 läuft.

---

## Session stopped — 2026-08-28 (Step 0 abgeschlossen: Fundament-Session + opencode-Setup + Smoke-Test)

**Stand:** Fundament-Session läuft, Claude Code + Nikinger, interaktiv.

- 0.1 `pytest -q` → **904 passed**, bestätigt V81 (Erwartung aus der Planung war exakt 904).
- 0.2 Verifikationsdurchlauf:
  - (a) Stichprobe P7-Handover §4 gegen Code — **beide grep-prüfbaren Punkte bestätigt**:
    `list.js :: moveSelectedItems()` reicht dasselbe `credentials`-Objekt an jedes sequenzielle
    `PATCH` durch (Zeile 240/246); `spacectl.py :: _cmd_remove_space()` ruft `remove_space_dir()`
    aber nirgends `rebuild_index()` (Zeile 170–195). P7-4 ist eine Verhaltensbehauptung, nicht
    grep-prüfbar — unverändert offen für die A3-Zweitprobe.
  - (b) `up:`/`down:`-Linkauflösung über alle L1-Cards: **ein** unaufgelöster Link, erwartet —
    `docs/concepts/phase8_ui_graph_plan.md` zeigt auf `phase8_ui_graph/CLAUDE.md`, das erst in
    diesem Schritt entsteht.
  - (c) INDEX-Abdeckung: alle lebenden `.md` haben eine Zeile; die drei `phase6_shares/tests/golden/*.md`
    sind Test-Fixtures, keine lebenden Dokumente — bewusst ohne Zeile.
  - (d) Softcap-Scan: zwei Übergrößen bestätigt (`phase6_shares/CLAUDE.md` 41.032 B,
    `phase5_ui/CLAUDE.md` 40.957 B) — beide über der 40.000-B-Schwelle (dezimales KB, wie in der
    bestehenden `phase6_shares`-Notiz verwendet).
- 0.3 P8-P ausgeführt: `phase5_ui/CLAUDE.md`s INDEX-Zeile bekam dieselbe benannte Ausnahme-Notiz
  wie `phase6_shares/CLAUDE.md` (geschlossene Phase, ein Abschluss-Block, Rotation bricht mit
  `exit 2`); dabei zwei stale Größenangaben korrigiert (`~34KB`→`~41KB` bei phase5_ui,
  `~44KB`→`~41KB` bei phase6_shares — beide waren nie nachgemessen worden).
- 0.4 `AGENTS.md` entfernt (`git rm`), zugehörige INDEX-Zeile raus — Freigabe stand bereits in
  der INDEX-Zeile selbst (P7-Handover §7.2).
- 0.5 Dieses Skelett + `SESSIONS_ARCHIVE.md` angelegt.

- 0.6 **opencode installiert und Regeldatei-Verhalten verifiziert.** `npm install -g
  opencode-ai` (Nikinger-Handgriff), Ergebnis `opencode-ai@1.18.25`. Ein `postinstall`-Warnhinweis
  (`allow-scripts` blockierte `postinstall.mjs`) erwies sich als folgenlos — das Plattform-Binary
  kommt über ein separates optionales npm-Paket, nicht über das Skript; `opencode --version` /
  `--help` funktionieren sofort. Provider-Auth vom Nikinger selbst gesetzt (Minimax-Token-Plan,
  `opencode auth list` zeigt `MiniMax (minimax.io)`, Modell `minimax/MiniMax-M3` verfügbar).
  **Kontrollfrage statt Annahme** (Plan-Vorgabe): `opencode run --model minimax/MiniMax-M3` mit
  der Frage nach dem Nikinger-Codenamen + Hard Rule 6 — Antwort korrekt **„Nikinger"** + Hard
  Rule 6 wortgetreu zitiert. `CLAUDE.md` wird gelesen, keine Verdeckung mehr durch `AGENTS.md`
  (0.4 hat es entfernt).
- 0.7 **Fähigkeits-Parität hergestellt, V93/V94 beantwortet:**
  - **V93 (Browser-Steuerung):** `opencode mcp add playwright -- npx @playwright/mcp@latest`
    (Syntax: Kommando nach `--`, nicht per Prompt-Dialog) — steht in
    `~/.config/opencode/opencode.jsonc` (**global**, nicht projektlokal — für dieses
    Ein-Projekt-Setup ohne praktischen Unterschied, aber notiert für den Fall eines zweiten
    opencode-Projekts). `opencode mcp list` zeigt `playwright — connected`. 30 `playwright_*`-
    Tools stehen der laufenden Instanz zur Verfügung (per Tool-Auflistung bestätigt) — Pendant zu
    `claude-in-chrome` gefunden.
  - **V94 (Web-Recherche):** **nein, nur `webfetch`** (Einzel-URL-Abruf), keine Web-Suche. Für
    C0 (Anti-AI-Pattern-Research) bedeutet das: **Teil 1 (Recherche/Katalog) läuft als
    Claude-Code-Zuarbeit**, opencode/M3 bekommt nur den fertigen Fund-Katalog — genau der in
    V94 vorgesehene Ausweichpfad, keine neue Entscheidung nötig.
- 0.8 **Smoke-Test bestanden (P8-26).** Wegwerf-Branch `phase8-step0-smoke-test`, drei Proben
  in einem opencode-Lauf: (1) Testdatei angelegt — bestanden; (2) `pytest -q
  phase1_storage/tests/test_models.py` — **4 passed**, kein `SHAREFYX_*`/`SFX_*`-Env gesetzt
  (Session-`env` vor und nach dem Lauf geprüft, sauber); (3) Playwright-Navigation gegen eine
  echte Wegwerf-Instanz (eigener Port `18765`, eigenes `tmp`-`SPACE_DATA_ROOT`, eigene
  `SPACE_AUTH_DB`) — `GET /ui/login` korrekt mit Titel/Überschrift „Anmelden" gelesen.
  **Ein Betriebsfehler dabei, sofort korrigiert:** der erste Versuch ließ `SPACE_PORT`
  unspezifiziert, band an den Default-Port `8765` — dort läuft der **echte** `sharefyx-mcp.service`
  (Live-Instanz, pid 999) — Bindeversuch scheiterte mit `EADDRINUSE`, der Prozess beendete sich
  selbst, kein Schreibzugriff erfolgte. Der folgende `curl /health` traf dadurch tatsächlich den
  Live-Dienst — rein lesend, keine andere Wirkung als ein manueller Health-Check. Wiederholt mit
  `SPACE_PORT=18765`, danach sauber gegen die eigene Instanz verifiziert (`uptime_s:1`).
  Wegwerf-Instanz per PID beendet, Live-Dienst per zweitem `/health`-Aufruf als unverändert
  bestätigt (`uptime_s` durchgehend steigend, kein Neustart). Branch + Testdatei +
  `.playwright-mcp/`-Laufzeitordner nach dem Test verworfen (`git branch -D`, `rm`);
  `.playwright-mcp/` zusätzlich in `.gitignore` aufgenommen (künftige opencode-Läufe in diesem
  Projektverzeichnis legen ihn sonst wieder an).

**Verifiziert:** `git status` nach Cleanup zeigt nur den beabsichtigten Diff (`.gitignore`,
Phase-Head, Skelett, INDEX/ROADMAP) — Wegwerf-Branch weg, Wegwerf-Instanz-Prozess weg, Live-Dienst
lief während der gesamten Sitzung ohne Unterbrechung (`systemctl is-active` durchgehend `active`).

**Harnesswechsel freigegeben:** ab Block A führt opencode/M3 aus, kein Advisor-Call
(P8-L/N12) — Ersatzmechanismen sind die Selbstprüf-Checkliste (Plan §0.6) und die zwei
Nikinger-Sichtprüfpunkte (Plan §8).

**Offen für die nächste Sitzung:** Block A starten (A1 Reauth-Grant zuerst, P8-A) — unter
opencode/M3, gegen `docs/concepts/phase8_ui_graph_plan.md` §2. Vor jedem Edit die zitierten
Datei:Zeile-Anker neu prüfen (V82, driftet erfahrungsgemäß um wenige Zeilen).
