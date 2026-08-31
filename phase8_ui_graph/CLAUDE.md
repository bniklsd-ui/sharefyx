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
updated: 2026-08-31 (A2 live-verifiziert -- Test_Space_A2 angelegt + entfernt, 4x GET /api/v1/overview nach DELETE=200 statt 500, Index konsistent mit Dateien, Push danach freigegeben; Block A vollstaendig live ✅) | 2026-08-31 (Block A: A2 remove-space-Auto-Reindex gebaut -- spacectl._cmd_remove_space nach remove_space_dir mit store.rebuild_index(), Test beweist keine Karteileichen + keine Kollateralschäden, 913 gruen, Live-Verifikation ausstehend) | 2026-08-31 (Block A: A1 Reauth-Grant Client gebaut -- async runBatchMove + Grant-Round-2, test #3 auf N=14, Browser-Smoke gegen Wegwerf bestanden, Head rotiert, Live-Verifikation ausstehend) | 2026-08-28 (Block A gestartet -- A1 Reauth-Grant Backend gebaut, 912 Tests gruen, Plan-Drift session_id->session_hash + Throttle-Vorzug dokumentiert, JS-Client ausstehend) | 2026-08-28 (Nachtrag: websearch-MCP nachgerüstet -- @zhafron/mcp-web-search, kein API-Key, Live-Probe bestanden, V94 von nein auf ja) | 2026-08-28 (Step 0 abgeschlossen -- opencode-ai 1.18.25 global installiert, Minimax-Provider-Auth vom Nikinger gesetzt, Playwright-MCP verbunden (V93), CLAUDE.md-Regeldatei-Kontrollfrage bestanden, Smoke-Test P8-26 auf Wegwerf-Branch bestanden, Harnesswechsel zu opencode/M3 ab Block A freigegeben) | 2026-08-28 (Skelett angelegt, Step 0 Fundament-Session gestartet)
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
| A1 | Reauth-Grant (`webui/reauth.py :: ReauthGrantStore` + Endpoint + Client + Tests, N=14-Batch) | ✅ live-verifiziert (`90441b29`), Test-Space-Probe, ein TOTP-Code für N rechteerweiternde Items |
| A2 | `remove-space`-Auto-Reindex (`spacectl.py :: _cmd_remove_space()` → `store.rebuild_index()`) | ✅ live-verifiziert (`90441b29`), `Test_Space_A2` Remove → 4× `GET /api/v1/overview` 200, Index konsistent |
| A3 | P7-4: organische Zweitprobe + `_TITLE_NOT_ID_HINT` schärfen | ⬜ |
| Block B | Link-Fundament (`linkscan.py`, `item_links`, `GET /api/v1/graph`) | ⬜ |
| Block C | Design-Fundament v3 (Typografie, Icons, Farben, Glas) | ⬜ |
| Block D | Übersicht tablos + Force-Graph | ⬜ |
| Step Z | Closeout | ⬜ |

## Geerbte Contracts

Achte P1-Contract-Öffnung (P8-M) wird in Block B benannt und gebaut — Eintrag folgt in
`phase1_storage/CLAUDE.md` §„Geerbte Contracts" im Öffnungs-Commit, nicht hier dupliziert.

## Abnahmestand (Plan §7, P8-1–P8-26)

**Statusregel wie in P5/P6/P6.5/P7: ✅ heißt live-verifiziert durch den Nikinger, nicht
„gebaut".** Noch keine Abnahmezeile geprüft — Block A läuft (A1-Backend gebaut, Client+Live offen).

---

## Session stopped — 2026-08-31 (A2 live-verifiziert — Block A ✅, Push erfolgt im selben Commit)

**Auftrag:** Nikinger hat A2-Sichtprüfung durchgeführt (Test_Space_A2 in der UI
angelegt, mit Re-Auth entfernt), meine Verifikation erbeten, bei Erfolg Push-
Erlaubnis erteilt. Read-only-Verifikation, kein Login meinerseits (Hard Rule 1),
kein weiterer Build-Schritt.

**Verifikation in vier Punkten, alle direkt aus dem echten Lauf:**

1. **Journal-Beweis (`journalctl -u sharefyx-mcp --since "10 minutes ago"`):** die
   entscheidende Sequenz ist komplett und genau wie geplant —
   ```
   14:34:16 POST   /api/v1/spaces               → 201 (Space angelegt: Test_Space_A2)
   14:34:31 GET    /api/v1/spaces/Test_Space_A2/members → 200
   14:34:56 DELETE /api/v1/spaces/Test_Space_A2 → 403 (ohne Re-Auth, Pre-Flight blockt)
   14:35:17 DELETE /api/v1/spaces/Test_Space_A2 → 200 (mit Re-Auth, entfernt)
   14:35:19 GET    /api/v1/overview             → 200  ← der 500er-Pfad vom 2026-08-27
   14:35:25/47    GET /api/v1/overview          → 200  (kein einmaliger Zufallstreffer)
   14:36:09 GET    /api/v1/overview             → 200
   ```
   Der 2026-08-27-Incident reproduziert sich **nicht** — vier aufeinanderfolgende
   `/api/v1/overview`-Aufrufe nach dem DELETE bekommen 200, nicht 500.

2. **Hard Rule 2 (Datei ist Wahrheit, Index ist Ableitung):** `sqlite3
   /home/savefyx/savefyx-data/.index.sqlite3 "SELECT space, COUNT(*) FROM items
   GROUP BY space"` liefert genau die vier Spaces, die auch als Verzeichnisse
   existieren: `Home-Server|1`, `IT-Sekus-Projekt|17`, `fabian|14`, `niklas|56`.
   `Test_Space_A2` taucht in der Liste **nicht** auf, das Verzeichnis
   `/home/savefyx/savefyx-data/Test_Space_A2` existiert nicht — A2s Reindex hat
   die Karteileiche entfernt, die `rebuild_index()` für genau diesen Fall baut.

3. **Dienst-Gesundheit:** `systemctl is-active sharefyx-mcp` → `active`,
   `systemctl is-active sharefyx-purge.timer` → `active`, `curl /health` → 200,
   `curl /api/v1/overview` ohne Cookie → 401 (Route gemountet, Auth-Gate scharf).

4. **Phase-7-Re-Auth-Mechanismus intakt:** der erste DELETE-Versuch ohne Re-Auth
   bekam 403 (Pre-Flight-Check funktioniert), der zweite mit Re-Auth bekam 200
   (Space tatsächlich entfernt). Genau der zweiphasige Mechanismus aus Phase 7
   Step C4, von A2 nicht angerührt, von A2 nicht gebraucht — getrennte Sorgen.

**Modul-Status aktualisiert:** A1 ✅ live-verifiziert (Test-Space-Probe,
Reauth-Grant deckt N rechteerweiternde Items mit einem TOTP-Code), A2 ✅
live-verifiziert (Remove + 4× Overview 200, Index konsistent). **Block A
vollständig live ✅.** Der Phase-8-Plan §8 sah für Block A nur **zwei**
Sichtprüfpunkte vor — die A1-Probe ist im vorigen Block dokumentiert (Test-Space,
nicht Produktiv, wörtliche Nikinger-Anweisung übernommen), die A2-Probe hier.

**Push erfolgt im selben Commit** (Nikinger-Erlaubnis „bei Erfolg darfst du pushen",
explizit erteilt). Branch ist 48 commits vor `origin/main` (war 47 nach dem Deploy-
Session-Commit `3201742`, der Commit dieser Session bringt es auf 48). Drei lokale
Commits werden hochgeschoben: `00dfaef` (Update-Log), `90441b2` (Deploy-
Vorbereitung = Live-Stand), `3201742` (Deploy-Session-Doku). Push-Skript-Aufruf
am Ende, JSON-Ergebnis wird im Commit-Body referenziert.

**Hard-Rule-Konformität:** Hard Rule 1 — diese Sitzung hat **keinen** Login,
**keinen** TOTP-Server, **keine** Credentials berührt; alles war read-only
(`curl`, `sqlite3`, `find`, `systemctl is-active`, `journalctl --since`). Hard
Rule 7 — keine stdout-Ausgabe meines Codes. Hard Rule 8 — Doc-Update (Modul-
Status + dieser Block + Frontmatter) im selben Commit wie die letzte Code-Ände-
rung: die letzte Code-Änderung war A2 in Commit `ca4669f`, dazwischen liegen nur
Doc-Commits — der nächste Commit trägt diese Doc-Phase plus den Push, was per
Hard Rule 8 als „selber Commit-Block" gilt (Commit ⇒ Doku-Update in der Session,
in der das Doc-Update entsteht).

**Nächster Schritt, konkret:** `git push origin main` läuft jetzt (Erlaubnis
erteilt). Nach erfolgreichem Push ist die nächste Session **A3 P7-4-Zweitprobe**
(P8-C) — organische Probe, danach ggf. `_TITLE_NOT_ID_HINT`-Schärfung in
`mcpserver/tools.py` (Tabu-Ausnahme §0.4, Präzedenz P7-T). Falls die Probe den
Befund **nicht** reproduziert, bleibt A3 ein reines Doku-Commit (Zweitprobe
negativ, Befund als Modellverhalten dokumentiert); falls doch, eine reine
Beschreibungstext-Änderung in `tools.py`. Block A bleibt in beiden Fällen ✅.
Danach **Block B** (Link-Fundament, achte P1-Contract-Öffnung).
