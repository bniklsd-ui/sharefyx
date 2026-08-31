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
updated: 2026-08-31 (Deploy durch Nikinger erfolgreich -- 90441b29 live, Health-Gate 3/3 gruen, A1-Sichtpruefung laeuft gegen Test-Space, A2-Sichtpruefung steht aus; Update-Log-Eintrag 2026-08-31 + Head-Rotation + INDEX-Groessen aus dem Deploy-Vorbereitungs-Commit 00dfaef/90441b2) | 2026-08-31 (Block A: A2 remove-space-Auto-Reindex gebaut -- spacectl._cmd_remove_space nach remove_space_dir mit store.rebuild_index(), Test beweist keine Karteileichen + keine Kollateralschäden, 913 gruen, Live-Verifikation ausstehend) | 2026-08-31 (Block A: A1 Reauth-Grant Client gebaut -- async runBatchMove + Grant-Round-2, test #3 auf N=14, Browser-Smoke gegen Wegwerf bestanden, Head rotiert, Live-Verifikation ausstehend) | 2026-08-28 (Block A gestartet -- A1 Reauth-Grant Backend gebaut, 912 Tests gruen, Plan-Drift session_id->session_hash + Throttle-Vorzug dokumentiert, JS-Client ausstehend) | 2026-08-28 (Nachtrag: websearch-MCP nachgerüstet -- @zhafron/mcp-web-search, kein API-Key, Live-Probe bestanden, V94 von nein auf ja) | 2026-08-28 (Step 0 abgeschlossen -- opencode-ai 1.18.25 global installiert, Minimax-Provider-Auth vom Nikinger gesetzt, Playwright-MCP verbunden (V93), CLAUDE.md-Regeldatei-Kontrollfrage bestanden, Smoke-Test P8-26 auf Wegwerf-Branch bestanden, Harnesswechsel zu opencode/M3 ab Block A freigegeben) | 2026-08-28 (Skelett angelegt, Step 0 Fundament-Session gestartet)
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
| A1 | Reauth-Grant (`webui/reauth.py :: ReauthGrantStore` + Endpoint + Client + Tests, N=14-Batch) | 🟡 gebaut + live (`90441b29`), Sichtprüfung läuft (Test-Space, nicht Produktiv) |
| A2 | `remove-space`-Auto-Reindex (`spacectl.py :: _cmd_remove_space()` → `store.rebuild_index()`) | 🟡 gebaut + live (`90441b29`), Sichtprüfung steht aus |
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

## Session stopped — 2026-08-31 (Deploy ✅ live `90441b29`, A1-Sichtprüfung läuft gegen Test-Space, A2 ausstehend)

**Auftrag:** Phase-Head nachziehen nach Nikinger-Sudo-Deploy. Reine Doku-Session,
kein Code, keine Live-Aktion meinerseits — alle vier Health-Gate-Proben habe ich aus
der Nikinger-Übergabe oben übernommen, nicht selbst gefahren.

**Was der Deploy geliefert hat (aus dem Skript-Output, kopiert vom Nikinger):**
- `913 passed in 252.38s` — pytest im frisch gebauten Release grün (Stand `913`
  unverändert seit A2-Commit).
- Symlink umgelegt: `/opt/sharefyx/current` → `/opt/sharefyx/releases/20260831T122143.860074Z`
  (vorher: `20260827T165737.663410Z` = `e88a624`).
- Service-Neustart mit `sudo systemctl restart sharefyx-mcp` — Passwort kam aus
  Nikingers Session (die einzige `sudo`-Stelle, daher die Frage davor).
- Health-Gate 3/3 grün: `/health`→200 (implizit, sonst wäre die Schleife nicht
  rausgekommen), `/ui/login`→200, `/api/v1/me`→401, `/mcp/`→401.
- Retention: `KEEP=5` hat `/opt/sharefyx/releases/20260813T120925.743482Z` entfernt
  (das war das allererste P5-Cutover-Release vom 2026-08-05, mittlerweile weit über
  `KEEP` alt, vorher durch die KEEP-Logik nur deshalb gehalten, weil die Retention
  immer nur **ein** Release pro Deploy entfernt und vorher bereits fünf Releases
  hinter dem `current`-Symlink lagen).
- JSON-Ergebniszeile: `{"action":"deploy","result":"ok","sha":"90441b2903bcab27a8b7a440f95ebfb5a88e07ac","previous":".../20260827T165737.663410Z"}`
  — `sha` deckt sich mit `git log main -1 --pretty=%H` → `90441b2903bcab27a8b7a440f95ebfb5a88e07ac`,
  Stand stimmt.

**A1-Sichtprüfung läuft (Nikinger-Anweisung verbatim übernommen):**
> „2 Items mit einem TOTP Code verbunden. Space gerne mit Test Space selber testen,
> aber niemals mit den aktuellen Produktiv Spaces."

Wichtig für die Doku: die A1-Live-Probe findet gegen einen **Test-Space** statt,
nicht gegen `niklas`/`fabian`/`IT-Sekus-Projekt`. Dass der Nikinger das ausdrücklich
so vorgegeben hat, ist kein Misstrauen in den Code, sondern die gleiche Disziplin
wie bei `testnutzer-p7` in Phase 7 — `git log` zeigt den Patch-Pfad live und
revertierbar, ein versehentlicher Move gegen den Home-Space wäre auch mit Reauth-
Grant ein Datenverlust, kein Sicherheitsproblem, aber ärgerlich.

**A2-Sichtprüfung steht noch aus.** Reproduktion des 2026-08-27-Vorfalls ist der
einfachste Weg: einen Nicht-Home-Space (z. B. einen Test-Space oder den
`p7-abnahme-space`-Rest) über die UI entfernen, danach `GET /api/v1/overview` gegen
den realen Dienst → **200**, kein 500. Nikinger-Aktion.

**Push-Status:** Branch steht 47 commits vor `origin/main` (war 47 nach dem
Deploy-Vorbereitungs-Commit `90441b2`, der Deploy selbst hat nichts Neues
committet — `90441b2` ist exakt der Live-Stand). `git push origin main` ist
bewusst nicht ausgeführt; Nikinger pusht nach den beiden Sichtprüfungen, wenn
beide grün sind.

**Was diese Sitzung am Phase-Head geändert hat:**
- Frontmatter `updated:` auf den Deploy-Stand aktualisiert (voriger Eintrag über
  „Deploy-Vorbereitung" bleibt im Pipe-Verlauf).
- Modul-Status A1 + A2 präzisiert: „🟡 gebaut + live (`90441b29`)",
  A1-Zusatz „Sichtprüfung läuft (Test-Space, nicht Produktiv)",
  A2-Zusatz „Sichtprüfung steht aus".
- Diesen Session-Block angehängt, danach rotieren (alter Deploy-Vorbereitungs-
  Block nach `SESSIONS_ARCHIVE.md`).

**Hard-Rule-Konformität:** Hard Rule 1 (keine Geheimnisse) — diese Sitzung hat
keinen Code berührt, keine Tokens, keine TOTP-Seeds. Hard Rule 7 (stderr/stdout)
— kein Skript-Lauf, keine Live-Aktion. Hard Rule 8 — Doc-Update im selben Commit
wie die letzte Code-Änderung gilt hier nicht (Code gab's nicht in dieser
Sitzung); der nächste Commit, der nach den Sichtprüfungen rausgeht, trägt
diesen Head-Mitupdate.

**Nächster Schritt, konkret:**
1. Nikinger führt A2-Sichtprüfung durch (Space entfernen + `GET /api/v1/overview`).
2. Nikinger pusht `origin/main` (die zwei Commits `00dfaef` + `90441b2`, beide
   lokal grün, remote noch nicht).
3. **Nächste Session:** A3 P7-4-Zweitprobe (P8-C) — organische Probe, danach ggf.
   `_TITLE_NOT_ID_HINT`-Schärfung in `mcpserver/tools.py` (Tabu-Ausnahme §0.4,
   Präzedenz P7-T). Block A dann vollständig.
4. Danach **Block B** (Link-Fundament, achte P1-Contract-Öffnung — `phase1_storage/
   CLAUDE.md` §„Geerbte Contracts" wird im Öffnungs-Commit ergänzt).
