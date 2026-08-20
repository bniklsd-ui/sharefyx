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
updated: 2026-08-20 (Block B Step B1 gebaut: Bild-Assets in storage/, 807 pytest gruen nach drei Advisor-Fixes (Lock-Disziplin/created-Konsistenz/Sniff-Kosten), Zaehlkorrektur phase1_storage 126->130, Tabu-Diff leer)
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
| Block B Steps B2–B5 | `webui`-Routen, MCP-Asset-Tools, Markdown-Bildzweig | ⏳ nicht begonnen |

## Geerbte Contracts

Fünfte, benannte Öffnung des P1-Contracts (`storage/{files,store,models}.py`) — **gebaut**
2026-08-20 (Step B1), siehe `phase1_storage/CLAUDE.md` unter „Geerbte Contracts" (P6.5-T).
Details dort, nicht hier dupliziert.

---

## Session stopped — 2026-08-20 (Block B Step B1 gebaut: Bild-Assets in storage/)

**Auftrag:** Nikinger bestätigte Block B, weiterhin ein Schritt nach dem anderen für
`/context`-Checks dazwischen. Step B1 ist Storage-Fundament — kein Adapter, keine `webui`-Route,
kein MCP-Tool, reine `storage/`-Arbeit, P6.5-T (fünfte Contract-Öffnung) war bereits in Step 0
angekündigt.

**Gebaut, exakt wie im Plan §3 Step B1 vorgezeichnet, keine Abweichung:**
- `storage/models.py` — `AssetInfo` (neuer Dataclass: `id`/`mime`/`bytes`/`filename`/`created`).
- `storage/files.py` — `ASSET_ID_PREFIX`, `ITEM_ID_RE`/`ASSET_ID_RE` (V65 empirisch bestätigt:
  `generate_id()` liefert exakt `itm_[0-9a-f]{8}`), `new_asset_id()` (Zwilling zu
  `generate_id()`), `ASSET_MIME_TYPES` + `sniff_image_mime()` (PNG/JPEG/GIF-Präfix, WebP als
  Zweiteilprüfung RIFF+Offset-8-„WEBP" — kein reiner RIFF-Präfix-Check, sonst ließe er andere
  RIFF-Container wie WAV durch), `asset_dir()`/`asset_path()` (validieren IDs gegen die Regexe,
  `ValidationError` sonst), `move_asset_dir()` (No-op ohne Quellverzeichnis **und** bei
  `src==dst`, sonst `os.replace` + `fsync` auf beiden Elternverzeichnissen, propagiert
  `OSError(ENOTEMPTY)` unverändert bei einem nicht-leeren Ziel — P6.5-S), `atomic_write_bytes()`
  (binäres Gegenstück zu `atomic_write()`, eigene Funktion statt `bytes|str`-Zweig, damit die
  Textvariante ihre `encoding`-Semantik unangetastet behält, wie vom Plan empfohlen).
- `storage/store.py` — `put_asset()` (kein `version`-Parameter: Assets sind nicht Teil der
  Item-Versionierung, konkurrieren nie mit einem Text-Write um dieselbe `version`; genau ein
  Commit `"asset"`), `list_assets()` (kein Index, reines Verzeichnis-Listing, `_trash/`
  übersprungen, MIME erneut aus den Magic Bytes statt aus der Dateiendung), `get_asset()` (Bytes
  + MIME, dieselbe Nie-der-Endung-vertrauen-Regel), `delete_asset()` (N5: Verschieben nach
  `_trash/`, Entscheidung H bleibt formal unangetastet — kein Rewrite der Body-Referenz hier,
  das ist Sache der aufrufenden Schicht). `move()` ruft `files.move_asset_dir(...)`
  **innerhalb** der bestehenden Lock-Sektion, **vor** `_write_item_file()` (dem einzigen Ort,
  der committet) — ein Move mit Bildern erzeugt weiterhin genau einen Git-Commit, per Test
  bewiesen (`test_move_carries_the_asset_directory_and_still_produces_one_commit`). `archive()`
  unangetastet — `_assets/<item_id>/` bleibt liegen, wie geplant.

**Fund während der Umsetzung, kein Plan-Text:** `ItemNotFound` wird für einen fehlenden
`asset_id` wiederverwendet (`get_asset()`/`delete_asset()`), obwohl seine feste Fehlermeldung
„Item nicht gefunden" für ein Asset sachlich ungenau ist und `tools.py :: map_storage_error()`s
bestehender `ItemNotFound`-Zweig „prüfe die ID mit search_items" empfiehlt — für eine Asset-ID
unpassend. Bewusst nicht behoben: Step B1 ist reine Storage-Arbeit ohne MCP-Fehlerabbildung: die
eigentliche Fehlertextpflege gehört Step B4 (MCP-Asset-Tools), wo `map_storage_error()` ohnehin
angefasst wird. Vermerkt hier, damit es dort nicht übersehen wird.

**Drei Advisor-Funde vor dem Commit, alle behoben:**
1. **Lock-Disziplin:** `list_assets()`/`get_asset()` nahmen ursprünglich nur `self._lock`, nicht
   auch `self._file_write_lock()` — obwohl `_reconcile_and_get_row()`s eigener Docstring beide
   verlangt (sie kann auch bei `repair_drift=False` reindizieren, ein Index-Write außerhalb der
   Prozess-`flock`). `get()` (Z. 441) macht es richtig vor; die drei Asset-Lesemethoden jetzt auch.
2. **`created`-Divergenz:** `put_asset()` nahm `self._now_fn()` (injizierte Uhr), `list_assets()`
   die Datei-mtime — dasselbe Asset zeigte zwei verschiedene Werte, unbemerkt, weil kein Test sie
   gegeneinander prüfte. `put_asset()` liest jetzt ebenfalls die mtime nach dem Write; neuer
   Pflichttest `test_put_asset_created_matches_list_assets_created` pinnt das.
3. **Sniff-Kosten:** `list_assets()` las für die MIME-Erkennung jedes Bild vollständig ein,
   obwohl `sniff_image_mime()` maximal 12 Bytes braucht — bei mehreren/großen Bildern hätte das
   `get_item_meta`s eigenes Kostenversprechen („um Größenordnungen billiger" als `get_item`)
   unterlaufen, sobald Step B4 `assets` dort einblendet. Jetzt `path.open("rb").read(12)`.

**Tests:** 20 neu (12 `test_files.py`: 5 parametrisierte MIME-Erkennungsfälle + WebP-Offset-Fall
+ unbekannte Bytes + SVG-Ablehnung + ungültige IDs + `move_asset_dir` No-op + `move_asset_dir`
echter Move + `new_asset_id`-Format/Eindeutigkeit; 8 `test_store.py`: `put_asset` schreibt
atomar + genau ein Commit, `put_asset` lehnt unbekannte Bytes ab, `list_assets` leer ohne Bilder,
`get_asset` liefert Bytes+MIME, `delete_asset` verschiebt statt löscht, `move()` zieht Assets mit
+ weiterhin ein Commit, `move()` ohne Assets unverändert, `put_asset`/`list_assets`-`created`-
Konsistenz). `pytest` 787→**807**, alle grün, mehrere volle Läufe. Charakterisierung
(P6-D/P6.5-U) vor/nach byte-identisch. Tabu-Diff (`mcpserver/`/`phase4_auth/`/
`webui/security.py`/`webui/static/**`) leer — reiner `storage/`-Commit, wie Step B1 es verlangt.

**Vierter Advisor-Punkt, bewusst nicht behoben, für B2/B4 vorgemerkt:** `put_asset()`s
`filename`-Parameter wird in der Antwort zurückgegeben, aber nirgends persistiert —
`list_assets()` liefert für jedes Asset danach `filename=""`. P6-AZ sagt, der Pfad kommt aus der
Asset-ID, nie aus dem Namen — ob/wie der Originaldateiname trotzdem irgendwo überleben soll
(oder der Parameter ganz entfällt), ist eine Plan-Frage für Step B2/B4, keine Storage-Frage.

**Zählkorrektur, noch am selben Tag gefunden:** der vorherige Session-Block (Block A) hatte
`phase1_storage`s Testtotal per Delta-Rechnung auf **126** fortgeschrieben (123 + 3 `in_body`-
Tests), ohne einen vollen `pytest --collect-only -q` über alle `phase1_storage/tests/*.py` als
Gegenprobe zu fahren. Vor Step B1 lag die reale Summe bei **130**, nicht 126 — dieselbe
Drift-Kategorie, die `phase2_mcp/CLAUDE.md` bereits mehrfach dokumentiert (dort fremdverursacht
durch nicht nachgezogene Commits; hier selbstverursacht durch eine Delta-Rechnung ohne
Vollzähler). In `phase1_storage/CLAUDE.md`s Testzahl-Historie korrigiert, nicht stillschweigend
überschrieben. Lehre für den Rest dieser Phase: Testtotals per `pytest --collect-only -q` **über
das ganze Testverzeichnis** verifizieren, nicht nur die eigene Delta-Behauptung fortschreiben.

**Verifiziert:** `pytest` 807/807 (mehrere Läufe), Charakterisierung byte-identisch, Tabu-Diff
leer, `git status` zeigt ausschließlich die erwarteten `storage/`- und Test-Dateien plus Doku.

**Offen für die nächste Session:**
- Commit + Push (Nikinger-Freigabe ausstehend zum Zeitpunkt des Schreibens).
- Block B Step B2 (`webui`-Routen: Upload/Download/Delete-Endpunkte) ist der nächste Schritt,
  atomar wie bisher.
- Für Step B4 (MCP-Asset-Tools) vorgemerkt, nicht jetzt zu beheben: der `ItemNotFound`-
  Fehlertext-Fund (Asset-Fehlermeldung sagt „prüfe die ID mit search_items", unpassend für eine
  Asset-ID) und die `filename`-Persistenzfrage (Advisor-Punkt 4 oben).
- Gate A→B (echte Connector-Probe für Block A) steht weiterhin aus, unverändert — Block B darf
  weitergebaut, aber nicht vor diesem Gate deployt werden.
- Bekannte Doku-Schuld (`phase6_shares/CLAUDE.md` Block-C-Text stale) und der
  `test_authctl.py`-Flake bleiben unverändert offen.
