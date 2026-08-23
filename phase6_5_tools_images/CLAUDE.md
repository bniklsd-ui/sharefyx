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
updated: 2026-08-23 (P6.5-6/9 bestanden per DATA_ROOT-Check, P6.5-7 teilweise -- 6 von 14 Zeilen, Rest braucht ein Browser-Tool oder den Nikinger selbst, elfte Rotation gelaufen)
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
| Block A (Steps A1/A2/A4; A3 bewusst nicht gebaut, N3) | Werkzeug-Ergonomie (`mcpserver/tools.py`, `storage/store.py :: search(in_body=)`) | ✅ **gebaut, live deployt 2026-08-21, Gate A→B bestanden, Abnahmematrix P6.5-1–4 vollständig 2026-08-23** — echte Connector-Proben, siehe Abnahmestand + Session-Block |
| Block B Step B1 | Storage-Fundament Bilder (`storage/{files,store,models}.py`) | ✅ **gebaut, live deployt 2026-08-21** |
| Block B Step B2 | REST-Fläche Bilder (`phase5_ui/webui/{api,serializers}.py`) | ✅ **gebaut, live deployt 2026-08-21** |
| Block B Step B3 | Web-UI Anzeigen/Einfügen (`phase5_ui/webui/static/{app.html,app.css,js/{markdown,editor}.js}`) | ✅ **gebaut, live deployt 2026-08-21**, Playwright vor dem Deploy grün+gesehen |
| Block B Step B4 | MCP-Fläche Bilder (`mcpserver/tools.py` — `get_item_asset`/`put_item_asset`) | ✅ **gebaut, live deployt 2026-08-21**, `mcp_smoke.py` 16/16 |
| Block B Step B5 | Betrieb/Deploy-Vorbereitung (`diagnose.sh` Prüfung 13, `UPDATE_LOG.md`, `ui_budget.py`) | ✅ **gebaut, Block B vollständig, live deployt 2026-08-21** |

## Geerbte Contracts

Fünfte, benannte Öffnung des P1-Contracts (`storage/{files,store,models}.py`) — **gebaut**
2026-08-20 (Step B1), siehe `phase1_storage/CLAUDE.md` unter „Geerbte Contracts" (P6.5-T).
Details dort, nicht hier dupliziert.

## Abnahmestand (Plan §6, P6.5-1–P6.5-14)

**Statusregel wie in P5/P6: ✅ heißt live-verifiziert durch den Nikinger, nicht „gebaut".** Der
Plan selbst (`docs/concepts/phase6_5_tools_images_plan.md`) ist ein 📕-Snapshot und wird nicht
mehr editiert — der laufende Abnahmestand lebt hier, wie bei jeder Vorgängerphase.

| # | Kriterium (Kurzform) | Block | Stand | Beleg |
|---|---|---|---|---|
| P6.5-1 | Frische Instanz sagt NICHT „nur eigener Space" | A | ✅ | Nikinger, echter Connector, 2026-08-23 — Instanz nannte `niklas` UND `IT-Sekus-Projekt` (`write: true`) korrekt, `fabian` korrekt read-only |
| P6.5-2 | Nennt erlaubte `status`-Werte ohne Fehlversuch | A | ✅ | Nikinger, echter Connector, 2026-08-23 — `note: active\|archived`, `task: archived\|done\|open`, exakter Treffer im ersten Versuch |
| P6.5-3 | Nutzt `get_item_meta` vor einem Folge-Append | A | ✅ | Nikinger, echter Connector, separates Gespräch, 2026-08-23 — Reihenfolge aus den Versionsnummern rekonstruiert: `search_items`→`get_item`(v1, echter Body-Bedarf)→`append`(v1→v2)→**`get_item_meta`**(bestätigt v2)→`append`(v2→v3) — für den reinen Versions-Check vor dem zweiten Append wurde das billige Tool gewählt, nicht `get_item` erneut |
| P6.5-4 | Erklärt `patch_item`/`update_item`/`append_to_item`-Aufgabenteilung aus den Beschreibungen | A | ✅ | Nikinger, echter Connector, 2026-08-23 — korrekt: nur `update_item` erreicht Frontmatter, `patch_item`/`append_to_item` brauchen `version`, `patch_item` verlangt exakt einen Treffer |
| P6.5-5 | Bild-Upload sichtbar im UI-Dokument | B | offen | Browser — kein Browser-Tool in dieser Session, braucht den Nikinger |
| P6.5-6 | `.md`-Datei enthält nur `asset:`-Referenz, kein Binär/base64 | B | ✅ | Claude Code, `cat` im echten `DATA_ROOT`, 2026-08-23 — `itm_e33d2906`s `.md` enthält exakt `![Testbild](asset:ast_c28583e6)`, keine Binärdaten |
| P6.5-7 | Bilddatei unter `_assets/<item_id>/`, kein UI-Ordner | B | teilweise | Pfad bestätigt (`niklas/_assets/itm_e33d2906/ast_c28583e6.png`, `file` bestätigt echtes PNG), `list_spaces`s `folders`-Feld listet `_assets` strukturell nicht — **„kein UI-Ordner" selbst noch nicht mit echten Augen im Browser gesehen** |
| P6.5-8 | Fabian sieht freigegebenes Bild, `403` ohne Freigabe | B | offen | Nikinger + Fabian, Browser + `curl` |
| P6.5-9 | Ein Upload = genau ein Git-Commit | B | ✅ | Claude Code, `git log --oneline`, 2026-08-23 — `320a737 asset itm_e33d2906 [niklas]`, ein einziger Commit für den Asset-Pfad, getrennt von `create`/`patch` |
| P6.5-10 | Cross-Space-Move nimmt Bild mit, ein Commit | B | offen | Browser + `git log` |
| P6.5-11 | Fremde `<img>`-URLs/`javascript:` kein Netzabruf, kein `<img>` | B | offen | DevTools Network-Tab — Client-Logik bereits gegen eine Wegwerf-Instanz Playwright-geprüft (Step B3), aber nicht dasselbe wie eine Live-Probe |
| P6.5-12 | Bild entfernbar, Referenz rendert danach als Alt-Text | B | offen | Browser — entfällt bei N5=„gar nicht" |
| P6.5-13 | Claude sieht fremdes Bild nur bei `share_write`, nicht bei reinem `share_read` | B | offen | Nikinger + Fabian, echter Connector |
| P6.5-14 | Kündigt jeden Upload an, lädt nie unaufgefordert | B | offen | Nikinger, echter Connector, zwei Gespräche — zwei Datenpunkte liegen vor (Gate-A→B-Sitzung + diese Sitzung, beide Male vor jedem `put_item_asset` angekündigt), aber die Kriterienbewertung selbst ist Sache des Nikingers |

**6 von 14 live bestanden, Block A vollständig, Block B angefangen** (Block A: 4 von 4, Block B:
2 von 10 voll + 1 teilweise). Geerbte, in dieser Phase
nicht gelöste Live-Proben aus P6 (Abnahmezeilen 25–30/35–39, Gate A→B Punkt 3, `diagnose.sh`
vor jedem Deploy): unverändert offen, siehe Plan §6 Fußnote.

---

## Session stopped — 2026-08-23 (P6.5-6/9 bestanden, P6.5-7 teilweise — Grenzen ohne Browser-Tool sichtbar)

**Auftrag:** Nikinger bat, die restlichen Abnahmezeilen anzugehen, „besonders die UI-Tests
nochmal". Vor dem Start geprüft: diese Sitzung hat weder `claude-in-chrome` noch ein anderes
Browser-Automatisierungswerkzeug geladen (`ToolSearch` liefert nichts) — nur den sharefyx-MCP-
Connector und Bash auf der echten VM. Das setzt eine harte Grenze: alles, was echtes Rendern im
Browser braucht (P6.5-5/8/10/11/12/13), kann diese Sitzung nicht selbst erledigen.

**Was diese Grenze trotzdem zulässt, genutzt:** ein Test-Item über den echten Connector angelegt
(`itm_e33d2906`, Space `niklas`), ein echtes Bild hochgeladen (`put_item_asset`, angekündigt vor
dem Aufruf), die `asset:`-Referenz per `patch_item` in den Body eingefügt — danach den echten
`DATA_ROOT` read-only per Bash geprüft (kein Schreibzugriff auf den Live-Dienst, nur Lesen).

**Geprüft, exakt mit der im Plan §6 vorgeschriebenen Methode:**
- **P6.5-6 ✅** — `cat` auf die reale `.md`-Datei zeigt exakt `![Testbild](asset:ast_c28583e6)`
  im Body, keine Binärdaten, kein base64.
- **P6.5-9 ✅** — `git log --oneline -- niklas/_assets/itm_e33d2906/ast_c28583e6.png` zeigt genau
  einen Commit (`320a737 asset itm_e33d2906 [niklas]`), getrennt von `create`/`patch`.
- **P6.5-7 teilweise** — Pfad bestätigt (`niklas/_assets/itm_e33d2906/ast_c28583e6.png`, `file`
  bestätigt ein echtes 4×4-PNG), `list_spaces`s `folders`-Feld listet `_assets` strukturell
  nicht mit. **Nicht dasselbe wie die im Plan verlangte Browser-Probe** — ehrlich als „teilweise"
  markiert statt aufgerundet, weil niemand tatsächlich in die UI geschaut hat.

**Aufräumen:** `itm_e33d2906` ist `status:"archived"` (v3, `get_item_meta` bestätigt), bleibt
liegen wie jedes andere archivierte Item.

**Ergebnis, ehrlich benannt:** 6 von 14 statt vorher 4 von 14 — aber die verbleibenden 8 Zeilen
(P6.5-5/8/10/11/12/13 voll, P6.5-7 der Browser-Teil) sind strukturell nicht ohne echten Browser
zu schließen. Kein Weg, das über MCP/Bash zu umgehen, ohne die Abnahmezeile selbst zu verwässern
— genau die Art von „aufgerundetem" Fund, den Ponytail/Military-Brief-Disziplin verbietet.

**Verifiziert:** kein Code-Diff (reine Doku- + Live-Datensession über den Connector). `git
status` zeigt ausschließlich den Phase-Head + `SESSIONS_ARCHIVE.md` + `docs/INDEX.md`.

**Offen für die nächste Session:**
- P6.5-5/8/10/11/12/13 (Browser/`curl`, teils + Fabian) und der Browser-Teil von P6.5-7 —
  brauchen entweder den Nikinger selbst am echten Browser, oder ein Browser-Tool in einer
  künftigen Sitzung (`claude-in-chrome` o. Ä., falls verfügbar gemacht).
- P6.5-14 hat jetzt zwei Datenpunkte (Gate-A→B-Sitzung + diese Sitzung, beide Male vor jedem
  `put_item_asset` angekündigt) — Bewertung bleibt beim Nikinger, keine Selbstzertifizierung.
- V64, `filename`-Persistenzfrage, Doku-Schuld, `test_authctl.py`-Flake: unverändert offen.
