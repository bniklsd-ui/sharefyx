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
updated: 2026-08-31 (Block A: A2 remove-space-Auto-Reindex gebaut -- spacectl._cmd_remove_space nach remove_space_dir mit store.rebuild_index(), Test beweist keine Karteileichen + keine Kollateralschäden, 913 gruen, Live-Verifikation ausstehend) | 2026-08-31 (Block A: A1 Reauth-Grant Client gebaut -- async runBatchMove + Grant-Round-2, test #3 auf N=14, Browser-Smoke gegen Wegwerf bestanden, Head rotiert, Live-Verifikation ausstehend) | 2026-08-28 (Block A gestartet -- A1 Reauth-Grant Backend gebaut, 912 Tests gruen, Plan-Drift session_id->session_hash + Throttle-Vorzug dokumentiert, JS-Client ausstehend) | 2026-08-28 (Nachtrag: websearch-MCP nachgerüstet -- @zhafron/mcp-web-search, kein API-Key, Live-Probe bestanden, V94 von nein auf ja) | 2026-08-28 (Step 0 abgeschlossen -- opencode-ai 1.18.25 global installiert, Minimax-Provider-Auth vom Nikinger gesetzt, Playwright-MCP verbunden (V93), CLAUDE.md-Regeldatei-Kontrollfrage bestanden, Smoke-Test P8-26 auf Wegwerf-Branch bestanden, Harnesswechsel zu opencode/M3 ab Block A freigegeben) | 2026-08-28 (Skelett angelegt, Step 0 Fundament-Session gestartet)
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
| A1 | Reauth-Grant (`webui/reauth.py :: ReauthGrantStore` + Endpoint + Client + Tests, N=14-Batch) | 🟡 gebaut, Live-Deploy + Nikinger-Sichtprüfung ausstehend |
| A2 | `remove-space`-Auto-Reindex (`spacectl.py :: _cmd_remove_space()` → `store.rebuild_index()`) | 🟡 gebaut, Live-Deploy + Nikinger-Sichtprüfung ausstehend |
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

## Session stopped — 2026-08-31 (A2 `remove-space`-Auto-Reindex gebaut, 913 grün, Live-Verifikation ausstehend)

**Auftrag:** A2-Commit 3 (Block A letzter Erbpost, P8-B) — atomar in derselben Sitzung wie
A1, danach Session zuende. V82-Anker gegen die aktuelle Code-Basis verifiziert:
`spacectl.py:194` (`acl.remove_space_dir(data_root, name)`), `storage/store.py:809`
(`Store.rebuild_index() -> IndexStats`), `storage/index.py:187` (`rebuild_index(data_root,
conn)`).

**Was gebaut wurde (Zweizeiler + Test, exakt Plan §A2):**
- `phase6_shares/scripts/spacectl.py :: _cmd_remove_space()`: nach `acl.remove_space_dir(...)`
  ein `stats = Store(data_root).rebuild_index()` und eine Statuszeile
  (`Index neu aufgebaut: N Items in 0.044s.`) — die `Store`-Klasse war bereits importiert
  (`_cmd_list_spaces` und `_cmd_show` benutzen sie seit P6 Step 6, gleiches Muster,
  keine neue Import-Zeile nötig).
- `phase6_shares/tests/test_spacectl.py :: test_remove_space_with_force_rebuilds_the_index_
  so_no_stale_rows_remain`: legt zwei Spaces mit je einem Item an, baut den Index auf
  (`Store(data_root, git=False).rebuild_index()`), beweist dass BEIDE Items im Suchlauf
  auftauchen, ruft `remove-space --force` auf, beweist dass nur das Opfer-Item verschwunden
  ist UND das Zeuge-Item erhalten bleibt (Reindex ist `data_root`-weit, kein Kollateralschaden),
  UND dass das Opfer-Item auch im **globalen** `search()` ohne `space=`-Filter nicht mehr
  auftaucht (Hard Rule 2: keine Karteileichen, jemals). Die Test-Datei wird direkt geschrieben
  (kein `Store.create()`), weil das die schnellste Variante ist, einen indexierten Eintrag zu
  erzeugen — der Test beweist den Mechanismus, nicht die Schreibpfade.

**Begründung der Entscheidung „Reindex erzwingen statt nur warnen" gegen den Plan:** Plan
§A2 sagt „Zweizeiler + Test, Warnhinweis-Variante verworfen (wird übersehen, reproduziert den
500er-Incident vom 2026-08-27)". Beweis im Code-Kommentar dieselbe Begründung mit explizitem
Hard-Rule-2-Bezug (Datei ist die Wahrheit, der Index muss jederzeit entsprechen — diese
Operation entfernt eine Verzeichnisebene, „danach reindexen" ist keine optionale Optimierung,
sondern Pflicht).

**Verifiziert:** `pytest -q` → **913 passed** (912 alt + 1 neu). Tabu-Diff leer
(`phase4_auth/`, `phase2_mcp/`, `webui/security.py`, benannte `storage/`-Dateien — `acl.py`
**nicht** in der Tabu-Liste, der Reindex-Aufruf geht durch `store.rebuild_index()`, nicht durch
einen direkten `acl`-Eingriff, kein Plan-Drift auf P7-Cs sechster Öffnung). Erster Lauf
zeigte den **bekannten** `test_authctl.py :: test_revoke_kills_the_family`-Flake
(`phase4_auth/CLAUDE.md` Zeile „Vormerkungen", seit 2026-08-20 vermerkt — `argparse:
--family-id: expected one argument`, reihenfolgeabhängig, nicht von dieser Session
verursacht); zweiter vollständiger Lauf 913/913 grün, kein Code-Touch in `phase4_auth/`.
`ui_budget.py` nicht erneut gelaufen — keine UI-Änderung in diesem Commit, der vorige A1-Lauf
(dialogs.js 9.5 KB) deckt das schon ab.

**Was der Test bewiesen hat (vs. was der Live-Vorfall bewies):**
- ✅ `rebuild_index()` entfernt Zeilen gelöschter Spaces — keine Karteileichen im Index.
- ✅ `rebuild_index()` fasst **nicht** andere Spaces an — keine Kollateralschäden.
- ✅ Der Status-Print zeigt `items_indexed > 0` für die verbliebenen Spaces (Beweis im
  Test-Output, nicht nur behauptet).
- ❌ Live-Verifikation durch den Nikinger: ausstehend. Der echte
  `testnutzer-p7`-Vorfall vom 2026-08-27 (Commit `e2c908a`) entstand genau durch das
  Fehlen dieses Reindex — der Live-Lauf wird denselben `remove-space` durchspielen und
  danach `GET /api/v1/overview` (das `search()`/`list_spaces()` aggregiert) gegen den
  realen Dienst aufrufen, um die 200 statt 500 zu sehen. Nikinger-Aktion.

**Hard-Rule-1-Compliance:** keine Geheimnisse berührt (CLI-Operator-Werkzeug, schreibt nur
`.share.yml`-Konfigurationen und Verzeichnisse, niemals Tokens oder TOTP-Seeds). Tabu-Diff
leer. `git diff` auf `mcpserver/`, `webui/`, `authserver/` ebenfalls leer.

**Nächster Schritt, konkret:** A3 P7-4-Zweitprobe (P8-C) — der UX-Befund aus Phase 7
(Claude nennt Menschen IDs statt Titeln), eine organische Probe **vor** der
`_TITLE_NOT_ID_HINT`-Beschreibungsschärfung, dann falls die Prosa-Anweisung allein nicht
reicht der Text-Edit in `mcpserver/tools.py` (Tabu-Linie §0.4 erlaubt reine
Beschreibungstext-Strings in `tools.py`, Präzedenz P7-T). Block A damit vollständig — drei
Commits (`a381a96` A1-Client + Smoke + N=14, dieser Commit A2, A3 folgt). Danach Block B
(Link-Fundament, achte P1-Contract-Öffnung — neuer Absatz in
`phase1_storage/CLAUDE.md` §„Geerbte Contracts" beim Öffnungs-Commit, hier nur als Vormerkung
genannt).
