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
updated: 2026-08-23 (P7 Step A8.1 -- P6.5-8/13 per testnutzer-p7-Substitution geschlossen, 12 von 14 Zeilen, P6.5-12-Status auf "gebaut, ungeprueft" korrigiert nach P7 Step A3, Details in phase7_spaces_admin/CLAUDE.md) | 2026-08-23 (P6.5-5/7/10/11 per echtem Chrome-Connector bestanden -- 10 von 14 Zeilen, ein echter Lueckenfund: kein Entfernen-Knopf in editor.js trotz gebautem DELETE-Endpoint, P6.5-12 dadurch blockiert, zwoelfte Rotation gelaufen)
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
| P6.5-5 | Bild-Upload sichtbar im UI-Dokument | B | ✅ | Claude Code, echter `claude-in-chrome`-Connector, 2026-08-23 — `itm_de2e4fd8`, 4×4-PNG rendert sichtbar (per `naturalWidth`/`naturalHeight` + Zoom-Screenshot bestätigt); erster Upload-Versuch war ein selbst erzeugtes korruptes PNG (PIL bestätigte `cannot identify image file`) — kein Server-Bug, eigener Fixture-Fehler, mit PIL-erzeugtem echten PNG wiederholt |
| P6.5-6 | `.md`-Datei enthält nur `asset:`-Referenz, kein Binär/base64 | B | ✅ | Claude Code, `cat` im echten `DATA_ROOT`, 2026-08-23 — `itm_e33d2906`s `.md` enthält exakt `![Testbild](asset:ast_c28583e6)`, keine Binärdaten |
| P6.5-7 | Bilddatei unter `_assets/<item_id>/`, kein UI-Ordner | B | ✅ | Pfad+Datei per Bash bestätigt (Vorsitzung); **[2026-08-23]** Browser-Teil geschlossen — echte DOM-/Accessibility-Tree-Probe des `niklas`-Baums UND das Space-Auswahl-`<select>` im Verschieben-Dialog listen beide identisch nur `nvidia-avo-harness`, `otobo`, `+ Ordner` — kein `_assets`-Eintrag an keiner Stelle der echten UI |
| P6.5-8 | Fabian sieht freigegebenes Bild, `403` ohne Freigabe | B | ✅ (via `testnutzer-p7`) | **[2026-08-23, P7-Plan §A8.1 gebilligte Substitution]** `testnutzer-p7` statt Fabian (kein Bug, dieselbe serverseitige Rechteprüfung) — `phase7_spaces_admin/scripts/p7_13_ui_asset_probe.py` gegen `/ui/login`-Cookie-Session, drei Zustände desselben Items durchgespielt: `share_read` allein → `200`/`image/png` (HUMAN-Fläche braucht nur Leserecht, P6-AW — asymmetrisch zu AGENT, siehe P6.5-13); **ganz ohne Freigabe (`share_read`/`share_write` beide leer) → `403`, deckungsgleich mit dem Plan-Text.** **[Korrektur, selber Tag, Advisor-Fund:** ein erster Testlauf verwechselte „keine Session" (`401`, reine Authentifizierung, bereits durch P5 Zeile 19 bewiesen) mit „keine Freigabe" (`403`, die tatsächlich hier geprüfte Autorisierung) — der ursprüngliche „401 statt 403"-Befund war dadurch selbst der Fehler, nicht der Plan-Text; mit dem korrekten Testfall nachgeholt.] Kein echter Browser-Klick-Nachweis (Bild sichtbar im DOM) — Login-Credentials in eine `computer`-Type-Aktion zu tippen hätte sie im sichtbaren Werkzeugverlauf exponiert (Hard Rule 1), Skript-Ebene bewusst gewählt statt dessen |
| P6.5-9 | Ein Upload = genau ein Git-Commit | B | ✅ | Claude Code, `git log --oneline`, 2026-08-23 — `320a737 asset itm_e33d2906 [niklas]`, ein einziger Commit für den Asset-Pfad, getrennt von `create`/`patch` |
| P6.5-10 | Cross-Space-Move nimmt Bild mit, ein Commit | B | ✅ | Nikinger (echter Login, TOTP), Claude Code verifiziert per `git log` + Browser, 2026-08-23 — `5d06187 move itm_de2e4fd8 [IT-Sekus-Projekt]` trägt `.md` UND `_assets/itm_de2e4fd8/` in einem Commit, Bild rendert nach dem Move im neuen Space sichtbar |
| P6.5-11 | Fremde `<img>`-URLs/`javascript:` kein Netzabruf, kein `<img>` | B | ✅ | Claude Code, echter `claude-in-chrome`-Connector + `read_network_requests`, 2026-08-23 — Body testweise um eine `example.com`-URL und eine `javascript:`-URL erweitert (danach zurückgesetzt): DOM zeigt exakt ein `<img>` (die echte `asset:`-Referenz), kein Request an `example.com`, kein zweites `<img>`-Element |
| P6.5-12 | Bild entfernbar, Referenz rendert danach als Alt-Text | B | 🟡 gebaut, ungeprüft | **[2026-08-23 Korrektur, P7 Step A3]** die „nicht testbar/keine Lücke mehr"-Aussage unten war stale — P7s Step A3 hat den Entfernen-Knopf gebaut (`renderAssetStrip()`/`assetIds`-Kontextschlüssel, `editor.js`/`markdown.js`), siehe `phase7_spaces_admin/CLAUDE.md`. **Backend-/Store-Verhalten nur per `pytest` bewiesen, kein echter Browser-Klick diese Session** — bleibt deckungsgleich mit P7-5 (⬜ dort, 🟡 hier: der Knopf existiert, ist aber unverifiziert, kein reiner Blocker mehr) |
| P6.5-13 | Claude sieht fremdes Bild nur bei `share_write`, nicht bei reinem `share_read` | B | ✅ (via `testnutzer-p7`) | **[2026-08-23, P7-Plan §A8.1 gebilligte Substitution]** `phase7_spaces_admin/scripts/p7_13_asset_share_gate_probe.py`, echter OAuth-Fluss: `share_read` allein → `get_item_asset` liefert `bytes_available:false` (nur Metadaten); nach Erweiterung auf `share_write` → echte Bild-Bytes (`image/png`). Genau das in `tools.py :: get_item_asset()` kommentierte P6.5-M-Verhalten, empirisch bestätigt, kein neuer Sicherheitsbefund |
| P6.5-14 | Kündigt jeden Upload an, lädt nie unaufgefordert | B | offen | Nikinger, echter Connector, zwei Gespräche — zwei Datenpunkte liegen vor (Gate-A→B-Sitzung + diese Sitzung, beide Male vor jedem `put_item_asset` angekündigt), aber die Kriterienbewertung selbst ist Sache des Nikingers |

**[2026-08-23 Korrektur, P7 Step A8.1] 12 von 14 live bestanden, Block A vollständig, Block B
größtenteils** (Block A: 4 von 4, Block B: 8 von 10) — P6.5-8/13 per gebilligter
`testnutzer-p7`-Substitution geschlossen (siehe Zeilen oben), **nicht** wie zuvor hier
festgehalten „brauchen Fabians eigenes Login" — das war der Stand vor P7s dritten Principal.
Verbleibend offen: **P6.5-12** (Knopf jetzt gebaut, aber ungeprüft — kein Blocker mehr, siehe
oben) und **P6.5-14** (Nikingers eigene Bewertung, kein Selbstzertifizierungs-Kriterium — bleibt
grundsätzlich außerhalb dessen, was ein Skript oder ein zweiter Testprincipal je schließen kann).
Volle Herleitung der beiden neuen Proben: `phase7_spaces_admin/CLAUDE.md`s Session-Block
2026-08-23 (A8). Geerbte, in dieser Phase nicht gelöste Live-Proben aus P6 (Abnahmezeilen
25–30/35–39, Gate A→B Punkt 3, `diagnose.sh` vor jedem Deploy): unverändert offen, siehe Plan §6
Fußnote.

---

## Session stopped — 2026-08-23 (P6.5-5/7/10/11 per echtem Chrome-Connector bestanden, echte Werkzeug-Lücke bei P6.5-12 gefunden)

**Auftrag:** Nikinger bestätigte, der Chrome-Connector (`claude-in-chrome`) sei jetzt nutzbar,
und bat, die in der Vorsitzung liegen gebliebenen Browser-Abnahmezeilen anzugehen. Session lief
als generischer Standard-Kickoff-Prompt an, der sich als versehentlich falsch eingefügtes
Trading-Bot-Template herausstellte — vor dem Start geklärt und korrigiert, kein Zeitverlust.

**Setup:** `niklas` war bereits in einer manuell vom Nikinger geöffneten Chrome-Session
eingeloggt. Eine neue, per `claude-in-chrome` erzeugte Tab wiederverwendete dasselbe
Cookie-authentifizierte Profil erfolgreich für Lesezugriffe (`/ui/` zeigte sofort den
`niklas`-Space, kein Login nötig).

**Test-Fixture:** ein Item angelegt (`itm_de2e4fd8`, Space `niklas`), Bild hochgeladen
(`put_item_asset`, jedes Mal vor dem Aufruf angekündigt), `asset:`-Referenz per `patch_item`
eingefügt.

**Geprüft, mit echtem Browser:**
- **P6.5-5 ✅** — erster Upload-Versuch war ein von Hand aus Hex getipptes PNG, das der Browser
  als kaputtes Bild zeigte (`naturalWidth`/`naturalHeight` = 0 trotz `200`/korrektem
  `Content-Type` vom Server — **kein Server-Bug**, `PIL.Image.open()` bestätigte das Bild selbst
  als ungültig). Mit einem echten, PIL-erzeugten 4×4-PNG erneut hochgeladen — rendert sichtbar,
  per Zoom-Screenshot bestätigt.
- **P6.5-7 (Browser-Teil) ✅** — Ordnerbaum in der echten Accessibility-Tree-Probe UND das
  Space-Auswahl-`<select>` im Verschieben-Dialog zeigen beide identisch nur
  `nvidia-avo-harness`/`otobo`/`+ Ordner` — kein `_assets`-Eintrag.
- **P6.5-11 ✅** — Body testweise um eine `example.com`-Bild-URL und eine `javascript:`-URL
  erweitert, per `read_network_requests` + DOM-Query geprüft: kein Request an `example.com`,
  genau ein `<img>`-Element im DOM (die echte `asset:`-Referenz). Danach zurückgesetzt.
- **P6.5-10 ✅** — eigener Move-Versuch scheiterte zunächst dreifach an `403 CSRF-Token fehlt`
  (`PATCH .../items/{id}`, auch ein einfacher `append` schlug fehl) — Ursache gefunden, kein
  sharefyx-Bug: `sfx:csrf` wird nur EIN einziges Mal auf der Login-Bootstrap-Seite in
  `sessionStorage` abgelegt (`webui/pages.py :: render_logged_in_page()`,
  `static/js/app.js:33-39`) — `sessionStorage` ist pro Tab, eine frisch erzeugte Tab, die nur das
  Auth-Cookie erbt, hat nie einen Token. Der Nikinger fragte zu Recht zurück, dass der Move
  ohnehin TOTP+Passwort braucht — hat ihn selbst in seiner eigenen Tab ausgeführt. Verifiziert:
  `git log --oneline -- .../itm_de2e4fd8*` zeigt genau `5d06187 move itm_de2e4fd8
  [IT-Sekus-Projekt]`, `.md` UND `_assets/itm_de2e4fd8/` im selben Commit; Bild rendert nach dem
  Move im neuen Space sichtbar (Browser-Screenshot nach dem Move).

**Echter Fund, kein Test-Artefakt: P6.5-12 nicht baubar in dieser Form.** `editor.js` hat keinen
Entfernen-Knopf für Bilder — grep auf `trash|entfern|delete.*asset` liefert null Treffer im
gesamten Skript, obwohl N5 = „Verschieben statt Entfernen" (nicht „gar nicht") gelockt ist und
der Server-Endpunkt bereits existiert (`store.delete_asset()`,
`DELETE /api/v1/items/{item_id}/assets/{asset_id}`, `webui/api.py:703,756-760`). Dem Nikinger
gemeldet, bevor er in seiner Tab danach gesucht hätte. **Nikinger-Entscheidung: nur vermerken,
nicht in dieser Sitzung bauen.**

**Aufräumen:** `itm_de2e4fd8` ist `status:"archived"` (v7, per `update_item`), liegt jetzt in
`IT-Sekus-Projekt` (Move war Teil des Tests). Beide MCP-Chrome-Tabs geschlossen.

**Ergebnis, ehrlich benannt:** 10 von 14 statt vorher 6 von 14. Verbleibend offen: P6.5-8/13
(brauchen Fabians eigenes Login, vom Nikinger als nicht-blockierend bestätigt — „werden von ihm
getestet, wenn er Zeit hat"), P6.5-14 (Nikingers eigene Bewertung), P6.5-12 (echte Werkzeug-Lücke,
siehe oben — kein Testproblem, ein Baufund).

**Verifiziert:** kein Code-Diff (reine Doku- + Live-Datensession über Connector + Browser). `git
status` zeigt ausschließlich den Phase-Head + `SESSIONS_ARCHIVE.md` + `docs/INDEX.md`.

**Offen für die nächste Session:**
- P6.5-12: Entfernen-Knopf in `editor.js` bauen (kleine, phaseneigene Änderung — DELETE-Endpoint
  existiert bereits) — Nikinger-Entscheidung noch ausständig, ob/wann.
- P6.5-8/13: Fabians eigenes Login, sobald er Zeit hat.
- P6.5-14: Nikingers eigene Bewertung, zwei Datenpunkte liegen vor (Vorsitzung + diese Sitzung).
- V64, `filename`-Persistenzfrage, Doku-Schuld, `test_authctl.py`-Flake: unverändert offen.
