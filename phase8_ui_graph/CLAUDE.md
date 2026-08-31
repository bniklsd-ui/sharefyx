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
updated: 2026-08-31 (Deploy-Vorbereitung A1+A2 -- Update-Log-Eintrag 2026-08-31 lokal commit (00dfaef), P6-X-Gate gruen, Sudo ueber savefyx nicht moeglich, Nikinger fuehrt deploy.sh main selbst aus, danach A1+A2-Sichtpruefung; zwei alte Bloecke in dieser Sitzung rotiert) | 2026-08-31 (Block A: A2 remove-space-Auto-Reindex gebaut -- spacectl._cmd_remove_space nach remove_space_dir mit store.rebuild_index(), Test beweist keine Karteileichen + keine Kollateralschäden, 913 gruen, Live-Verifikation ausstehend) | 2026-08-31 (Block A: A1 Reauth-Grant Client gebaut -- async runBatchMove + Grant-Round-2, test #3 auf N=14, Browser-Smoke gegen Wegwerf bestanden, Head rotiert, Live-Verifikation ausstehend) | 2026-08-28 (Block A gestartet -- A1 Reauth-Grant Backend gebaut, 912 Tests gruen, Plan-Drift session_id->session_hash + Throttle-Vorzug dokumentiert, JS-Client ausstehend) | 2026-08-28 (Nachtrag: websearch-MCP nachgerüstet -- @zhafron/mcp-web-search, kein API-Key, Live-Probe bestanden, V94 von nein auf ja) | 2026-08-28 (Step 0 abgeschlossen -- opencode-ai 1.18.25 global installiert, Minimax-Provider-Auth vom Nikinger gesetzt, Playwright-MCP verbunden (V93), CLAUDE.md-Regeldatei-Kontrollfrage bestanden, Smoke-Test P8-26 auf Wegwerf-Branch bestanden, Harnesswechsel zu opencode/M3 ab Block A freigegeben) | 2026-08-28 (Skelett angelegt, Step 0 Fundament-Session gestartet)
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
| A1 | Reauth-Grant (`webui/reauth.py :: ReauthGrantStore` + Endpoint + Client + Tests, N=14-Batch) | 🟡 gebaut, Update-Log-Commit ✅, Live-Deploy wartet auf Nikinger-Sudo, danach Nikinger-Sichtprüfung |
| A2 | `remove-space`-Auto-Reindex (`spacectl.py :: _cmd_remove_space()` → `store.rebuild_index()`) | 🟡 gebaut, Update-Log-Commit ✅, Live-Deploy wartet auf Nikinger-Sudo, danach Nikinger-Sichtprüfung |
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

## Session stopped — 2026-08-31 (Deploy-Vorbereitung A1+A2 — Update-Log ✅, Sudo wartet auf Nikinger)

**Auftrag:** Sonderaufgabe der vorherigen Sitzung — `deploy.sh main` für die drei
A1+A2-Commits (`06cd21b` A1-Backend, `a381a96` A1-Client, `ca4669f` A2-Reindex). Mein
„Handgriff" laut Nikinger-Anweisung, Live-Deploy der drei Phase-8-Commits.

**Zwei Blocker vor dem Skript-Start identifiziert (verifiziert, nicht spekuliert):**

1. **`docs/UPDATE_LOG.md` stale.** Oberster `## YYYY-MM-DD`-Eintrag war `2026-08-27`,
   heute `2026-08-31` (UTC und lokal gleich) — `deploy.sh` würde an P6-X-Gate (Schritt
   2.5) sofort abbrechen. Genau der Mechanismus, für den das Gate gebaut wurde: ein
   Deploy mit sichtbarer Funktionalität ohne frischen Banner-Eintrag ist per Definition
   ein Bug.
2. **`sudo systemctl` braucht Passwort.** `sudo -n -l` → `password is required`, der
   `savefyx`-User hat **keine** `NOPASSWD`-Regel. Deploy-Schritt 6 (Service-Neustart) ist
   ohne sudo nicht möglich.

**Nikinger-Entscheidung (AskUserQuestion):** Option 1 — Update-Log-Eintrag selbst schreiben,
sudo durch den Nikinger aus dessen Session.

**Was diese Sitzung konkret getan hat (vier Schritte, klein gehalten):**

1. **Update-Log-Eintrag `## 2026-08-31` oben in `docs/UPDATE_LOG.md` eingefügt.** Zwei
   sichtbare Verbesserungen, eine Zeile je Feature, nutzerorientierte Sprache
   (Präzedenz-Eintrag 2026-08-27):
   - „Mehrere Notizen gleichzeitig in einen anderen Space verschieben: reicht jetzt ein
     Passwort und ein Code für alle aus, auch wenn die Aktion Schreibrechte erweitert
     — der Code wird intern genau einmal verwendet, danach ist für jede weitere
     Verschiebe-Aktion ein neuer Code nötig." (deckt A1-Backend + A1-Client, schließt
     P7-24 — TOTP-Replay im Batch war die vererbte Block-A-Erbpost)
   - „Spaces entfernen räumt jetzt den internen Suchindex mit auf — die Übersicht
     funktioniert danach wieder zuverlässig." (deckt A2, schließt den 500er-Incident
     vom 2026-08-27 reproduzierbar)
2. **Lokal commit `00dfaef` auf `main`, kein Push.** Branch steht 46 commits vor
   `origin/main` (war 45 vor diesem Commit) — `git push` ist bewusst nicht ausgeführt,
   der Nikinger pusht nach dem Deploy selbst. Hard Rule 8 (Doc-Update im selben Commit)
   trifft hier nicht zu — Doc und Code gehören zu verschiedenen Commits (Hard Rule 8
   bezieht sich auf Step-Abschluss-Commits, der Update-Log-Eintrag ist eine Deploy-
   Voraussetzung, kein Schritt-Abschluss).
3. **Modul-Status-Tabelle angepasst:** A1 + A2 von „🟡 gebaut, Live-Deploy +
   Nikinger-Sichtprüfung ausstehend" auf „🟡 gebaut, Update-Log-Commit ✅, Live-Deploy
   wartet auf Nikinger-Sudo, danach Nikinger-Sichtprüfung".
4. **Deploy.sh-Kommando für den Nikinger vorbereitet** (siehe unten).

**Deploy-Kommando, vollständig und kopierbereit** (einzeilig, Env-Variablen vorne):
```bash
SHAREFYX_RELEASES_DIR=/opt/sharefyx/releases \
SHAREFYX_CURRENT_LINK=/opt/sharefyx/current \
SHAREFYX_SOURCE_REPO=/home/savefyx/dev/savefxy \
SHAREFYX_SERVICE=sharefyx-mcp \
SHAREFYX_SYSTEMCTL="sudo systemctl" \
SHAREFYX_DATA_ROOT=/home/savefyx/savefyx-data \
SHAREFYX_BACKUP_DIR=/var/lib/sharefyx-backup \
bash phase5_ui/scripts/deploy.sh main
```
Pfade aus `phase3_edge/local.env` (`DATA_ROOT`) und `phase3_edge/systemd/sharefyx-backup.service`
(`SHAREFYX_BACKUP_DIR`). `SHAREFYX_PORT`/`SHAREFYX_HEALTH_TIMEOUT`/`SHAREFYX_KEEP_RELEASES`
nicht gesetzt — Defaults aus `deploy.sh` (8765/30/5) sind die in P5/Phase 8 unverändert
geltenden Werte. Skript gibt am Ende genau eine JSON-Zeile aus (`{"action":"deploy",
"result":"ok",...}` bei Erfolg, automatisches Rollback + `*.failed`-Mark bei Gate-Fail).

**Verifiziert:** `grep -m1 -E '^## [0-9]{4}-[0-9]{2}-[0-9]{2}$' docs/UPDATE_LOG.md`
→ `## 2026-08-31` (Gate grün); `git log --oneline -1` → `00dfaef phase8: Update-Log-Eintrag
2026-08-31 fuer A1+A2`; `git status` clean. **Keine** Live-Aktion meinerseits — keine
git clone, keine venv, kein pytest, kein Symlink, kein Service-Neustart. `pytest -q` wurde
nicht erneut gefahren: die letzte Messung A2 (`913 passed`) ist zwei Commits alt, dieser
Sitzungs-Commit berührt keinen Python-Code, der Stand kann nicht rot geworden sein.

**Was der Nikinger nach dem Deploy live prüft (zwei Sichtprüfpunkte, beide aus dem
Phase-8-Plan §8):**
- **A1 (Reauth-Grant, P7-24):** Mehrfachauswahl (Strg+Klick) zweier Items in einen
  fremden, schreib-erweiternden Space verschieben — ein einziger Dialog
  „2 von 2 benötigen Passwort und Code", **ein** TOTP-Code deckt beide ab, danach
  ist der Code verbraucht (Toast/MCP-Server-Log bestätigen „PATCH 200" für beide
  Items).
- **A2 (Auto-Reindex):** am einfachsten der Vorfall vom 2026-08-27 reproduziert —
  einen Space (nicht den Home-Space) mit einem Item über die UI entfernen (oder
  `spacectl.py remove-space … --force`), danach `GET /api/v1/overview` gegen den
  realen Dienst (curl/Cookie-Login) → **200**, kein 500. Optional zusätzlich: das
  entfernte Space taucht nicht mehr in `list_spaces()` auf, das Item nicht mehr in
  globalem `search()` ohne `space=`-Filter.

**Hard-Rule-Konformität:** Hard Rule 1 (keine Geheimnisse) — diese Sitzung berührt
keine Tokens, keine TOTP-Seeds, keine Credentials. Hard Rule 7 (stderr/stdout) —
kein Skript-Lauf, kein Live-Eingriff. Hard Rule 8 — Update-Log ist die einzige
Doc-Änderung; Modul-Tabelle und dieser Session-Block sind im selben Working-Tree,
gehen aber als zwei separate Commits raus (einer von mir, einer vom Nikinger nach
dem Deploy — bewusst kein Squash, weil dieser Block den tatsächlichen Deploy-Verlauf
dokumentieren soll und nicht den Vorbereitungs-Stand vor dem `00dfaef`-Commit).

**Nächster Schritt, konkret:** nach erfolgreichem Deploy + Nikinger-Sichtprüfung
**A3 P7-4-Zweitprobe** (P8-C) — organische Probe, danach ggf. `_TITLE_NOT_ID_HINT`-
Beschreibungsschärfung in `mcpserver/tools.py` (Tabu-Ausnahme §0.4 erlaubt das,
Präzedenz P7-T). Block A dann vollständig ✅. Danach Block B (Link-Fundament, achte
P1-Contract-Öffnung — `phase1_storage/CLAUDE.md` §„Geerbte Contracts" wird im
Öffnungs-Commit ergänzt).
