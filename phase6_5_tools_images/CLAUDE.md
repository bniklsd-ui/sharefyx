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
updated: 2026-08-20 (Block B Step B4 gebaut: MCP-Flaeche Bilder, get_item_asset/put_item_asset, 828 pytest gruen, mcp_smoke.py 16/16, fuenfte Rotation gelaufen)
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
| Block B Step B3 | Web-UI Anzeigen/Einfügen (`phase5_ui/webui/static/{app.html,app.css,js/{markdown,editor}.js}`) | ✅ **gebaut**, Playwright grün+gesehen, noch nicht deployt |
| Block B Step B4 | MCP-Fläche Bilder (`mcpserver/tools.py` — `get_item_asset`/`put_item_asset`) | ✅ **gebaut**, `mcp_smoke.py` 16/16, noch nicht deployt |
| Block B Step B5 | Betrieb/Deploy-Vorbereitung (`diagnose.sh` Prüfung 13, `UPDATE_LOG.md`) | ⏳ nicht begonnen |

## Geerbte Contracts

Fünfte, benannte Öffnung des P1-Contracts (`storage/{files,store,models}.py`) — **gebaut**
2026-08-20 (Step B1), siehe `phase1_storage/CLAUDE.md` unter „Geerbte Contracts" (P6.5-T).
Details dort, nicht hier dupliziert.

---

## Session stopped — 2026-08-20 (Block B Step B4 gebaut: MCP-Fläche Bilder, `get_item_asset`/`put_item_asset`)

**Auftrag:** direkter Anschluss an Step B3, Nikinger-Wunsch „nächster Schritt, atomar" für
Context-Checks dazwischen. Step B4 aus Plan §3: neuntes/zehntes Tool, `get_item_meta`s
`assets`-Liste, `AssetNotFound` (B1s liegen gebliebener Fund), MCP-eigener Größenriegel N6.

**Gebaut, exakt wie im Plan §3 Step B4 vorgezeichnet:**
- `mcpserver/tools.py` — `MAX_MCP_ASSET_BYTES = 1 MiB` (N6, Rohgröße NACH Base64-Dekodierung,
  eigener kleinerer Riegel als der Web-UI-Weg). `AssetNotFound` (neu, P2-eigen wie
  `PermissionDenied`) + `map_storage_error()`-Zweig — schließt B1s Advisor-Fund: `Store.
  get_asset()` wirft `ItemNotFound` für ZWEI Ursachen (fehlendes Item, fehlendes Asset) mit
  identischer Klasse; da jeder Aufrufer `acl_of(item_id)` zuerst prüft, kann ein `ItemNotFound`
  aus dem nachfolgenden `get_asset()`-Aufruf sich nur noch auf die `asset_id` beziehen — die
  Docstring-Begründung steht jetzt direkt an der Klasse. `get_item_meta` bekommt eine
  `assets`-Liste (id/mime/bytes/filename, NIE Bytes — `store.list_assets()` ohnehin schon
  Magic-Byte-basiert und ohne vollständiges Einlesen, B1).
- **Neuntes Tool `get_item_asset(item_id, asset_id) -> Image | str`** (P6.5-M/N): `acl_of()` →
  `can_read_item` (sonst `PermissionDenied`) → P6.5-M-Bedingung `own or can_write_item` — nur
  DANN echte Bytes (`Image(data=data, format=mime.split("/")[-1])`, V69 unten). Sonst
  Metadaten+Klartexthinweis, keine Bytes (nach dem Advisor-Fix unten: erst Existenz prüfen).
- **Zehntes Tool `put_item_asset(item_id, data_base64, filename=None) -> str`** (P6.5-O/P):
  Ankündigungspflicht als erster Satz der Beschreibung (P6.5-O, „VOR JEDEM Aufruf", V64 bleibt
  Client-Verhalten von claude.ai, nicht vom Server erzwingbar). `can_write_item` (dieselbe
  Zeile wie `append_to_item`, kein eigener Rechteweg, P6.5-P). `base64.b64decode(...,
  validate=True)` (→ `binascii.Error` ⇒ `ValidationError`), Größenprüfung NACH der Dekodierung
  (N6-Reihenfolge). Kein `write_receipt()` (das nimmt ein `Item`+einen der vier Text-`op`-Werte,
  P6-H — ein Asset-Upload ist keins davon), eigene `compact_json`-Quittung nach demselben Muster
  (`op="asset"`, `asset_id`, `mime`, `bytes`, `item_version` unverändert, Hinweis auf die
  manuelle Body-Referenzierung).
- `register()`s Rückgabedict + Moduldocstring auf zehn Tools nachgezogen.

**`[VERIFY]` V69 empirisch geprüft (nicht nur aus dem Plan-Kommentar übernommen):**
`fastmcp.utilities.types.Image._get_mime_type()` baut aus `format` ausschließlich
`f"image/{format.lower()}"` — da `mime` hier immer exakt einer von `sniff_image_mime()`s vier
Werten ist (`"image/png"|"image/jpeg"|"image/gif"|"image/webp"`), rekonstruiert der
Split-Join-Roundtrip denselben String byte-identisch. Kein `to_image_content(mime_type=...)`
nötig. Bestätigt durch den echten `mcp_smoke.py`-Roundtrip (28 Bytes rein, 28 Bytes raus,
`image/png` in beide Richtungen).

**Zwei Advisor-Funde vor dem Commit, beide behoben:**
1. **Existenz-Asymmetrie im `may_see_bytes=False`-Zweig.** Der ursprüngliche Code gab für JEDE
   `asset_id` — auch eine frei erfundene, auf einem Item ganz ohne Assets — eine „erfolgreiche"
   Metadaten-Antwort (`bytes_available: false`) zurück, während derselbe Aufruf mit Schreibrecht
   für dieselbe erfundene ID korrekt `asset_not_found` geworfen hätte. Ein `share_read`-Halter
   bekam damit eine andere (unehrliche) Existenzauskunft als ein `share_write`-Halter für
   dieselbe ID. Kein Rechteproblem (die echte Liste ist über `get_item_meta` ohnehin für jeden
   Leser einsehbar) — trotzdem ein `bytes_available`-Feld, das log, wenn das Asset nicht
   existiert. Behoben: `store.list_assets(item_id)` zuerst, `AssetNotFound`, falls die ID nicht
   darunter ist; die zurückgegebenen Metadaten (`mime`/`bytes`/`filename`) stammen jetzt aus
   diesem echten Treffer statt erfunden zu sein. Neuer Test pinnt die Symmetrie.
2. **Der P6.5-N-Struktur-Test bewies nur zufällig, was er beweisen sollte.** `_PNG` (28 Bytes)
   ist so kurz, dass ein Leck fast zwangsläufig als vollständiger Base64-String im Response-Text
   aufgetaucht wäre — das Testdesign selbst bewies nichts Grundsätzliches. Plan-Vorgabe „Assertion
   gegen den bekannten Bytes-Marker" wörtlich umgesetzt: eigenes Bild mit einem unverwechselbaren
   ASCII-Marker im Bildinhalt, Prüfung gegen den vollen Base64-String UND den Klartext-Marker
   separat (fängt zusätzlich den Fehlerfall „jemand gibt rohe statt kodierte Bytes zurück" ab,
   den eine reine Base64-Suche nicht abdecken würde).

**Tests:** 10 neu in `test_tools.py` (58→68 — 7 aus der Plan-Testliste + 1 `AssetNotFound`-
Test [B1s Fund, nicht im Plan-Text, aber ausdrücklich für diesen Step vorgemerkt] + 2 aus den
beiden Advisor-Funden oben). `test_app.py`s Achttool-Test auf `test_all_ten_tools_are_callable_
over_http` erweitert (Asset-Roundtrip vor dem Archivieren des Test-Items eingefügt, keine neue
Testfunktion). `mcp_smoke.py` 14→16 Prüfungen (`put_item_asset`/`get_item_asset` auf
`created_ids[1]`, nicht `[0]` — das ist seit Check 7 archiviert), echter base64-dekodierter
Byte-Roundtrip verifiziert, nicht nur behauptet. `pytest` 818→**828**. Charakterisierung
unverändert grün (Step B4 fasst `storage/` nicht an). Tabu-Diff (`mcpserver/{permissions,
server,asgi}.py`, `phase4_auth/**`, `storage/index.py`, `webui/security.py`): leer.

**Verifiziert:** `pytest` 828/828, `mcp_smoke.py` 16/16 (echter In-Process-Lauf, Rohantworten
gesehen — Größentabelle zeigt `get_item_asset` 28 B, exakt die Testbildgröße), Charakterisierung
grün, Tabu-Diff leer, `git status` passt zur erwarteten Step-B4-Berührungsfläche
(`mcpserver/tools.py`, `scripts/mcp_smoke.py`, zwei Testdateien).

**Offen für die nächste Session:**
- Commit + Push (Nikinger-Freigabe ausstehend zum Zeitpunkt des Schreibens).
- Block B Step B5 (Betrieb/Deploy-Vorbereitung — `diagnose.sh` Prüfung 13, `docs/UPDATE_LOG.md`-
  Eintrag, `ui_budget.py`-Lauf) ist der letzte Schritt von Block B.
- V64 (löst `destructiveHint: True` bei claude.ai tatsächlich eine Rückfrage pro Aufruf aus?)
  bleibt offen — Server-Verhalten kann das nicht erzwingen, nur anbieten; braucht eine echte
  Connector-Probe durch den Nikinger, kein Unit-Test kann das schließen.
- Gate A→B (echte Connector-Probe für Block A) steht weiterhin aus, unverändert — Block B darf
  weitergebaut, aber nicht vor diesem Gate deployt werden.
- **`filename`-Persistenzfrage aus B1/B2 bleibt offen, jetzt ein drittes Mal berührt.**
  `put_item_asset(item_id, data_base64, filename=None)` reicht `filename` an `store.
  put_asset(..., filename=filename)` durch — genau wie B2s REST-Route. Der Wert erscheint
  dadurch in DIESER EINEN Antwort (`AssetInfo.filename`), aber `store.list_assets()` liest ihn
  nie aus einer Datei zurück (nichts persistiert ihn, B1s Fund) — ein späteres `get_item_meta`
  zeigt `filename: ""` für exakt dasselbe Asset. Zwei Aufrufer füttern jetzt denselben
  nicht-persistenten Parameter, die zugrundeliegende Frage (persistieren vs. Parameter ganz
  streichen) ist immer noch nicht getroffen — vorgemerkt für B5 oder eine eigene Kleinigkeit.
- Bekannte Doku-Schuld (`phase6_shares/CLAUDE.md` Block-C-Text stale) und der
  `test_authctl.py`-Flake bleiben unverändert offen.
