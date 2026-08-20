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
updated: 2026-08-20 (Block B Step B2 gebaut: REST-Flaeche Bilder in phase5_ui/webui, 818 pytest gruen, Charakterisierung gruen, Tabu-Diff leer, zweite Rotation gelaufen)
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
| Block A (Steps A1/A2/A4; A3 bewusst nicht gebaut, N3) | Werkzeug-Ergonomie (`mcpserver/tools.py`, `storage/store.py :: search(in_body=)`) | ✅ **gebaut**, noch nicht deployt — Gate A→B (echte Connector-Probe) steht aus |
| Block B Step B1 | Storage-Fundament Bilder (`storage/{files,store,models}.py`) | ✅ **gebaut** |
| Block B Step B2 | REST-Fläche Bilder (`phase5_ui/webui/{api,serializers}.py`) | ✅ **gebaut**, noch nicht deployt |
| Block B Steps B3–B5 | Markdown-Bildzweig/Editor-Upload, MCP-Asset-Tools | ⏳ nicht begonnen |

## Geerbte Contracts

Fünfte, benannte Öffnung des P1-Contracts (`storage/{files,store,models}.py`) — **gebaut**
2026-08-20 (Step B1), siehe `phase1_storage/CLAUDE.md` unter „Geerbte Contracts" (P6.5-T).
Details dort, nicht hier dupliziert.

---

## Session stopped — 2026-08-20 (Block B Step B2 gebaut: REST-Fläche Bilder in `phase5_ui/webui`)

**Auftrag:** Vorsitzung endete am Kontextlimit mitten in Step B2 — Route-Code lag bereits
geschrieben und ungetestet im Arbeitsverzeichnis vor (`webui/api.py`/`serializers.py`, Tests in
`phase5_ui/tests/test_api.py` + neuem `phase6_5_tools_images/tests/test_assets_acl.py`,
`pytest.ini` um den neuen Testpfad erweitert). Diese Session: Zustand rekonstruiert (`docs/
INDEX.md` → Phase-Head → `git status`/`git diff`), Code gegen Plan §3 Step B2 Zeile für Zeile
geprüft, volle Suite + Charakterisierung + Tabu-Diff gefahren, Advisor-Runde, drei Funde
behoben, Doku nachgezogen.

**Vorgefunden, exakt wie im Plan §3 Step B2 vorgezeichnet, keine Abweichung:**
- `webui/api.py` — `MAX_ASSET_BYTES = 5 * 1024 * 1024` (P6.5-L, eigene Konstante neben
  `MAX_BODY_BYTES`), `_raw_body()` (Gegenstück zu `_json_body()`, kein JSON-Parsing, ignoriert
  `Content-Type`, P6-AZ), vier Routen (`POST`/`GET`-Liste/`GET`-eins/`DELETE` auf
  `/api/v1/items/{item_id}/assets[/{asset_id}]`), jede mit `store.acl_of()` +
  `can_read_item_as_human()`/`can_write_item_as_human()` vor dem Store-Aufruf (P6-AW: ein Bild
  trägt keine eigene ACL, erbt die des Items). `X-Content-Type-Options: nosniff` explizit
  gesetzt (V67 unten).
- `webui/serializers.py` — `asset_to_json()` (neu), `item_to_json()` bekommt `assets=` (Default
  `None` → `[]`, bestehende Aufrufer bleiben byte-identisch — dieselbe Konvention wie
  `include_snippet` in Schritt G1).
- `phase6_5_tools_images/tests/test_assets_acl.py` (neu, Testheimat im neuen Phasenverzeichnis,
  nicht `phase6_shares/tests/` — P6.5-A) — vier Tests, `Store`+`SharePolicy` direkt, kein
  HTTP-Layer: Bild eines fremden, per `share_read` freigegebenen Items lesbar · ohne Grant
  verweigert · `share_read` allein erlaubt kein `POST` · Asset folgt dem Item über `store.move()`
  in den Zielspace und ist dort lesbar (Zwilling zu
  `test_acl_decision_follows_the_item_into_the_target_space`).

**`[VERIFY]` empirisch geschlossen, nicht nur aus dem Plan-Kommentar übernommen:**
- **V66** — `require_csrf()` (`webui/security.py` Z. 61-98) liest `Content-Type` nirgends, reine
  Origin-/Token-Prüfung über Header. `_require_csrf_json()` funktioniert für den rohen
  Bild-Body deshalb unverändert, kein Sonderfall nötig.
- **V67** — `ui_security_headers()` wird ausschließlich in `routes_auth.py`/`static_routes.py`
  aufgerufen (`grep` bestätigt), nie in `api.py` — erreicht `/api/v1/**` also grundsätzlich
  nicht. Der explizite `X-Content-Type-Options: nosniff` in `_assets_get_one()` ist deshalb
  nötig, nicht redundant, wie im Code-Kommentar behauptet.

**Zwei Advisor-Funde vor dem Commit, beide behoben:**
1. **`filename` ein zweites Mal still übersprungen.** B1s Session-Block hatte den Punkt
   ausdrücklich für B2/B4 vorgemerkt (`put_asset()`s `filename`-Parameter wird nirgends
   persistiert, `list_assets()` liefert `filename=""`); der vorgefundene B2-Code rief
   `store.put_asset(item_id, data=data)` ohne Übernahme dieser Vormerkung auf, ohne Kommentar.
   Jetzt ein Kommentar an der Aufrufstelle: der Plan spezifiziert rohe Bytes ohne
   Multipart-Feld, es gibt hier nichts zu lesen — B3 (Editor-Upload, kennt den echten
   Dateinamen aus `<input type="file">`) ist der frühestmögliche Ort für eine echte
   Entscheidung (persistieren vs. Parameter streichen). Bewusst zum zweiten Mal vertagt, jetzt
   mit Papierspur statt stillem Verschwinden.
2. **Testname überversprach.** `test_asset_of_foreign_nonexistent_item_gives_no_existence_
   signal` behauptete „kein Existenzunterschied", prüfte aber nur den nichtexistenten Fall
   (404) — ein fremdes, existierendes Item ohne Freigabe liefert tatsächlich `403`
   (`_items_get_one`s eigenes, kopiertes Verhalten, siehe `test_get_item_from_foreign_space_
   without_share_is_forbidden`). Der Plantext (Step-B2-Tabelle) behauptet „denselben
   Statuscode für beide Fälle" — das trifft auf `_items_get_one` selbst nicht zu, ist also eine
   Plan-Ungenauigkeit, kein Code-Fund. Aufgeteilt in zwei Tests mit korrekten Namen/Codes
   (`test_asset_of_nonexistent_item_is_404`, `test_asset_of_foreign_ungranted_item_is_403_not_
   404`), Docstring benennt die Plan-Abweichung.

**Tests:** 11 neu (7 `phase5_ui/tests/test_api.py`, davon 6 aus dem Plan + der zusätzliche
403-Test aus Advisor-Fund 2, 50→57; 4 `phase6_5_tools_images/tests/test_assets_acl.py`, neue
Datei — DoD-Zahl aus dem Plan war „+10", real +11 wegen des zusätzlichen 403-Tests, keine
Abweichung von Substanz). `pytest` 807→**818**, mehrere volle Läufe grün. Charakterisierung
(`phase6_shares/tests/test_characterization.py`) unverändert grün — Step B2 fasst `storage/`
nicht an. Tabu-Diff (`storage/**`, `mcpserver/**`, `phase4_auth/**`,
`phase5_ui/webui/security.py`, `phase5_ui/webui/static/**`): leer — `git status` zeigt
ausschließlich `phase5_ui/webui/{api,serializers}.py`, `phase5_ui/tests/test_api.py`,
`pytest.ini` und die neue `phase6_5_tools_images/tests/`.

**Verifiziert:** `pytest` 818/818, Charakterisierung grün, Tabu-Diff leer, `git status` passt
zur erwarteten Step-B2-Berührungsfläche.

**Offen für die nächste Session:**
- Commit + Push (Nikinger-Freigabe ausstehend zum Zeitpunkt des Schreibens).
- Block B Step B3 (Web-UI: Anzeigen und Einfügen, `markdown.js`/`editor.js`) ist der nächste
  Schritt, atomar wie bisher — Playwright gegen eine Wegwerf-Instanz (P5-T), kein Unit-Test.
- Für Step B4 (MCP-Asset-Tools) weiterhin vorgemerkt: der `ItemNotFound`-Fehlertext-Fund aus
  B1 und die `filename`-Persistenzfrage (jetzt zweimal vertagt, siehe oben).
- Gate A→B (echte Connector-Probe für Block A) steht weiterhin aus, unverändert — Block B darf
  weitergebaut, aber nicht vor diesem Gate deployt werden.
- Bekannte Doku-Schuld (`phase6_shares/CLAUDE.md` Block-C-Text stale) und der
  `test_authctl.py`-Flake bleiben unverändert offen.
