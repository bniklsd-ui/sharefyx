---
status: live
purpose: Phase-Head Werkzeug-Ergonomie + Bilder — Scope, harte Regeln, Modulstatus, aktueller Session-Handover
read-when: Arbeiten in phase6_5_tools_images/ oder an den in §2 des Plans genannten Dateien in mcpserver/storage/webui — zuerst lesen, zusammen mit dem neuesten Session-stopped-Block
detail: L2
up: ../CLAUDE.md
down:
  - ../docs/concepts/phase6_5_tools_images_plan.md   # voller Plan, Entscheidungen P6.5-A–P6.5-V, §0.0 gelockte N1–N6, Steps 0/A/B
  - ../phase6_shares/IMAGES_PLAN.md                  # Vorgänger-Zusatzplan, nachrangig seit 2026-08-20
  - SESSIONS_ARCHIVE.md                              # ältere Session-Blöcke, newest-first
updated: 2026-08-21 (Gate A->B bestanden: echter Connector-Rundlauf ueber den live deployten sharefyx-MCP-Server, V60 geschlossen, achte Rotation gelaufen -- Phase 6.5 hat keine offenen Bau-/Verifikationsschritte mehr)
---
# CLAUDE.md — Phase 6.5: Werkzeug-Ergonomie und Bilder (`phase6_5_tools_images/`)

> Kein eigenes Python-Paket (wie `phase3_edge/`, `phase6_shares/`) — Servercode bleibt in
> `mcpserver`/`storage`/`webui`. **Quelle der Wahrheit ist der Code, nicht dieses Dokument.**

---

## Mission (zuerst lesen)

Zwei Blöcke: **(A)** eine arbeitende Claude-Instanz findet ihre Werkzeuge, versteht deren
Aufgabenteilung aus der Beschreibung und zahlt keine Tausende Token für eine Versionsnummer.
**(B)** ein Bild liegt im Space, ist im Dokument sichtbar, technisch nur ein Link — und Claude
sieht seine Bytes nur, wenn ein Mensch ausdrücklich danach fragt. Unter Druck fällt Block B weg,
nie Block A (reine Beschreibungs-/Tool-Arbeit ohne Datenformatänderung).

## Scope

- **DRIN:** die fünf offenen MCP-Werkzeug-Ergonomie-Punkte (2026-08-14-Live-Feedback),
  Abschluss Block C Bilder (`storage/`-Fundament, `webui`-Routen, MCP-Asset-Tools).
- **DRAUSSEN:** Bulk-Append-Tool, Body-Volltextsuche in der Web-UI, automatische
  `_trash/`-Räumung, Space-Admin-UI (bleibt Phase 7), Rechteverwaltung über MCP-Tools,
  HEIC/SVG/PDF, serverseitiges Bild-Rendering. Volle Liste: Plan §5 „Explizit draußen".

Details, gelockte Entscheidungen P6.5-A–P6.5-V, Berührungsfläche/Tabu-Dateien, Schritt-Sequenz,
Testliste, Abnahmezeilen: `docs/concepts/phase6_5_tools_images_plan.md`.

## Modul-Status

| Block | Inhalt | Status |
|---|---|---|
| Step 0 | Haushalt/Ankündigungen | ✅ |
| Block A (Steps A1/A2/A4; A3 bewusst nicht gebaut, N3) | Werkzeug-Ergonomie (`mcpserver/tools.py`, `storage/store.py :: search(in_body=)`) | ✅ **gebaut, live deployt 2026-08-21, Gate A→B bestanden 2026-08-21** — echte Connector-Probe über claude.ai/Claude-Code-Connector, siehe Session-Block |
| Block B Step B1 | Storage-Fundament Bilder (`storage/{files,store,models}.py`) | ✅ **gebaut, live deployt 2026-08-21** |
| Block B Step B2 | REST-Fläche Bilder (`phase5_ui/webui/{api,serializers}.py`) | ✅ **gebaut, live deployt 2026-08-21** |
| Block B Step B3 | Web-UI Anzeigen/Einfügen (`phase5_ui/webui/static/{app.html,app.css,js/{markdown,editor}.js}`) | ✅ **gebaut, live deployt 2026-08-21**, Playwright vor dem Deploy grün+gesehen |
| Block B Step B4 | MCP-Fläche Bilder (`mcpserver/tools.py` — `get_item_asset`/`put_item_asset`) | ✅ **gebaut, live deployt 2026-08-21**, `mcp_smoke.py` 16/16 |
| Block B Step B5 | Betrieb/Deploy-Vorbereitung (`diagnose.sh` Prüfung 13, `UPDATE_LOG.md`, `ui_budget.py`) | ✅ **gebaut, Block B vollständig, live deployt 2026-08-21** |

## Geerbte Contracts

Fünfte, benannte Öffnung des P1-Contracts (`storage/{files,store,models}.py`) — **gebaut**
2026-08-20 (Step B1), siehe `phase1_storage/CLAUDE.md` unter „Geerbte Contracts" (P6.5-T).
Details dort, nicht hier dupliziert.

---

## Session stopped — 2026-08-21 (Gate A→B bestanden: echter Connector-Rundlauf, V60 geschlossen)

**Auftrag:** direkter Anschluss an die Vorsitzung — der Nikinger verband den sharefyx-Connector
neu (`/mcp`, „Reconnected to claude.ai sharefyx"; Standardschritt nach jedem Deploy, kein Fund)
und gab den in der Vorsitzung blockierten MCP-Werkzeug-Rundlauf frei, mit der Auflage, jedes
angelegte Item danach zu archivieren.

**Rundlauf, alle Aufrufe über den echten, live deployten Connector, kein In-Process-Test:**
1. `list_spaces` — `writable:true` korrekt für den eigenen Space (`niklas`) UND den geteilten
   Space `IT-Sekus-Projekt` (item-level `write:`), `writable:false` korrekt für `fabian`. Beweist
   live, was P6.5-B beschreibungsseitig korrigiert hatte.
2. `create_item(type=note, ...)` in `niklas` — Quittung statt Volltext, `itm_676b26b8`.
3. `get_item_meta` — Frontmatter+Version ohne Body, `assets: []` vor dem ersten Upload.
4. `put_item_asset` — **erster Versuch mit einem verbreiteten „1×1-PNG"-Copy-Paste-Fixture
   scheiterte**, Client zeigte „[Image removed — rejected by API]". **Root Cause gefunden, kein
   Server-/Connector-Fund:** dieses spezifische Fixture (aus dem Gedächtnis zitiert, nicht aus
   dem Repo) hat einen falschen CRC im `IDAT`-Chunk — per Byte-Parser bestätigt. `sniff_image_
   mime()` prüft bewusst nur Magic Bytes (P6-AZ, kein serverseitiges Bildverarbeiten), speicherte
   die kaputten Bytes also unverändert; der Client-Decoder lehnte sie beim Rendern korrekt ab.
   Kein Fix nötig — das ist exakt das entworfene Verhalten (garbage in, garbage out, keine
   serverseitige Validierung über Magic Bytes hinaus). Mit einem korrekt CRC'd 4×4-PNG (eigener
   Encoder, derselbe wie in der Step-B3-Playwright-Probe) wiederholt: **Bild wurde korrekt
   gerendert** (sichtbares blaues Quadrat).
5. `patch_item` — alter Text exakt einmal getroffen, Ersetzung korrekt, Quittung ohne Volltext.
6. `update_item(status="archived")` — Item archiviert, `get_item_meta` bestätigt
   `status:"archived"`, `version:3`, beide Assets weiterhin gelistet.

**`[VERIFY]` empirisch geschlossen:**
- **V60 — geschlossen.** Der claude.ai/Claude-Code-Connector rendert `ImageContent` für ein
  gültiges Bild korrekt (gesehen, nicht nur behauptet — das Quadrat war sichtbar). Für ein
  Bild mit ungültiger interner Struktur (falscher Chunk-CRC) lehnt der Client-Decoder korrekt
  ab, statt es als kaputtes Bild anzuzeigen — kein serverseitiger Fund, siehe oben.
- **V64 — Teildatenpunkt, nicht abschließend geschlossen.** Zwei `put_item_asset`-Aufrufe
  (`destructiveHint: True`) liefen ohne sichtbare wiederholte Rückfrage zwischen den Aufrufen.
  Das ist ein Hinweis, keine vollständige Antwort — eine einzelne Sitzung mit zwei Aufrufen
  beweist nicht das UI-Verhalten über mehrere Sitzungen/Tage hinweg; bleibt „beobachtet, nicht
  abschließend verifiziert" im Register.

**Live bestätigter, bereits dreimal dokumentierter Fund, jetzt auch außerhalb der Testsuite
gesehen:** `filename` wird weiterhin nicht persistiert — `put_item_asset(..., filename=
"gate-probe-valid.png")` gefolgt von `get_item_meta` zeigt `filename:""` für exakt dieses
Asset. Keine neue Information, aber die erste Live-Bestätigung außerhalb von `pytest`/
`mcp_smoke.py` — verstärkt den Fall für eine Entscheidung, ändert aber nichts an der offenen
Frage selbst.

**Aufräumen:** `itm_676b26b8` ist `status:"archived"` (nicht hart gelöscht, Entscheidung H/Hard
Rule 5 unverändert) — bleibt im Archiv-Ordner des Space `niklas` liegen, wie jedes andere
archivierte Item auch. Kein weiterer Aufräumschritt nötig oder vorgesehen.

**Ergebnis: Gate A→B ist bestanden.** Block A ist damit nicht nur gebaut und deployt, sondern
auch die einzige noch fehlende Abnahmebedingung (echte Connector-Probe) ist erfüllt. Modul-
Status-Tabelle oben nachgezogen.

**Verifiziert:** kein Code-Diff in dieser Session (reiner Live-Rundlauf über den Connector +
Doku-Nachpflege) — `pytest` nicht erneut gelaufen, war seit dem letzten Lauf unverändert.
`git status` zeigt ausschließlich den Phase-Head + `SESSIONS_ARCHIVE.md` + `docs/INDEX.md`.

**Offen für die nächste Session:**
- V64 bleibt ein offener Registereintrag — braucht mehrere echte Sitzungen über Zeit, kein
  Ein-Aufwasch-Test.
- `filename`-Persistenzfrage (jetzt viermal berührt: B1/B2/B4/live) bleibt offen, weiterhin
  keine Entscheidung getroffen.
- Phase 6.5 hat damit keine offenen Bau- oder Verifikationsschritte mehr — nur noch die beiden
  bekannten Vormerkungen oben (Doku-Schuld `phase6_shares/CLAUDE.md`, `test_authctl.py`-Flake).
