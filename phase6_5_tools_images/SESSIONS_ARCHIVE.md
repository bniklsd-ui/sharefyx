---
status: live
purpose: Archivierte Session-stopped-Blöcke aus phase6_5_tools_images/CLAUDE.md, verbatim, newest-first
read-when: Auditieren der vollen Phase-6.5-Historie — der aktuelle Session-Block lebt im Phase-Head, nicht hier
detail: L3
up: ./CLAUDE.md
down:
updated: 2026-08-20 (sechste Rotation -- Block-B-Step-B4-Session-Block verschoben, Head traegt seither den Block-B-Step-B5-Session-Block)
---
# SESSIONS_ARCHIVE.md — Phase 6.5: Werkzeug-Ergonomie und Bilder

Sechs Einträge, newest-first, verbatim aus `phase6_5_tools_images/CLAUDE.md` per
`scripts/rotate_session_block.sh phase6_5_tools_images`.

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

## Session stopped — 2026-08-20 (Block B Step B3 gebaut: Markdown-Bildzweig + Editor-Upload)

**Auftrag:** direkter Anschluss an Step B2, Nikinger-Wunsch „nächster Schritt, atomar" für
Context-Checks dazwischen. Step B3 aus Plan §3: `markdown.js`s Bildzweig, Sanitizer-Erweiterung
um `IMG`, „Bild einfügen"-Knopf im Editor, `.md-body img`-CSS-Regel, Playwright-Pflichtfälle.

**Gebaut, exakt wie im Plan §3 Step B3 vorgezeichnet, zwei dokumentierte Namensabweichungen
(siehe unten):**
- `webui/static/js/markdown.js` — Bildzweig in `inlineMarkdown()` **vor** dem Link-Replace
  (P6.5-J), `resolveAssetSrc()` löst `asset:<id>` nur bei gesetztem `itemId` auf; `itemId` wird
  durch `markdownToHtml(src, options)` an alle sieben `inlineMarkdown()`-Aufrufstellen
  durchgereicht (Paragraph/Tabellenzellen/Überschrift/Zitat/beide Listenarten). `ALLOWED_TAGS`
  +`IMG`, `ALLOWED_ATTRS.IMG = {src, alt}`. `safeSrc()` (neu, neben `safeHref()`) akzeptiert
  ausschließlich `/^\/api\/v1\/items\/itm_[0-9a-f]{8}\/assets\/ast_[0-9a-f]{8}$/` — kein
  `data:`, keine fremde Domain (P6.5-V). `sanitizeHtml()`s `walk()` ersetzt ein `<img>` ohne
  gültiges `src` durch seinen Alt-Text-Knoten (nicht nur das Attribut entfernen — toter Knoten
  sonst), exakt derselbe Mechanismus deckt `javascript:`, fremde Domains, `data:`-URIs UND
  unaufgelöste `asset:`-Marker ab (`updates.js`s „fallende Kante", kein Sonderfall nötig). Kopf-
  kommentar korrigiert (P6.5-K — IMG/`asset:` sind nicht mehr „bewusst nicht übernommen").
- `webui/static/js/editor.js` — `insertAtCursor()` (neuer Helfer neben `wrapSelection()`/
  `insertLinePrefix()`), Upload-Handler auf `#insert-image-input` (`change`): rohe Bytes per
  `api()` an `POST .../assets`, Erfolg fügt `![<Dateiname>](asset:<id>)` an der Cursorposition
  ein, Preview wird nachgezogen, falls gerade sichtbar. Beide `markdownToHtml()`-Aufrufstellen
  (Vorschau-Umschalter, Entwurf-Wiederherstellung) bekommen jetzt `{ itemId:
  state.editingSnapshot.id }`; `showReadonlyItem()` bekommt `{ itemId: item.id }`.
- `webui/static/app.html` — neuer Knopf `#insert-image-button` (`data-md="image"` — bewusst,
  damit er automatisch an der bestehenden Preview-Disable-Schleife und am generischen
  No-Op-Klick-Listener teilnimmt, ohne beides zu duplizieren) + verstecktes `#insert-image-input`
  (`accept="image/png,image/jpeg,image/gif,image/webp"`), zwischen „Trennlinie" und dem
  Vorschau-Umschalter.
- `webui/static/app.css` — `.preview img { max-width: 100%; height: auto; }`.

**Zwei dokumentierte Abweichungen vom Plan-Wortlaut, keine Abweichung von der Absicht:**
1. Plan nennt die Zielklasse `.md-body` — diese Klasse existiert im Repo nicht, die echte
   Vorschau-Klasse heißt `.preview` (dieselbe Drift-Kategorie wie der frühere `--border`-Fund in
   P6 Step G1). Regel an `.preview` gehängt, Kommentar verweist auf die Abweichung.
2. Kein `<input type="file">` mit sichtbarem Dateiauswahl-Button im Sinne des Plantexts, sondern
   ein `hidden`-Input, den der Werkzeugleisten-Knopf per `.click()` auslöst — gleiche
   Nutzerinteraktion (ein Klick, ein Dateidialog), aber der sichtbare Knopf bleibt optisch
   konsistent mit den übrigen `toolbar-btn`-Elementen statt eines rohen Browser-Datei-Inputs.

**Advisor-Runde vor dem Commit, drei Funde, alle behoben, ein vierter dokumentiert statt
gefixt:**
1. **Update-Banner-DoD lief nur auf Argumentation, nicht auf einem echten Lauf.** Plan §3 Step
   B3 verlangt explizit „ein `asset:`-Link im Update-Banner crasht nicht" als eigene Zeile —
   ursprünglich mit dem (korrekten, aber unzureichenden) Argument übersprungen, derselbe
   `safeSrc()`/`walk()`-Pfad decke das schon ab. Dieselbe Fundklasse wie der G3-Skip im
   Deploy-Blocker (2026-08-19, „schon im Unit-Test abgedeckt" war dort auch falsch). Behoben:
   Wegwerf-Instanz bekommt jetzt ein eigenes, temporäres `UPDATE_LOG.md` (`UiSettings.
   update_log_path` überschrieben — Default hätte sonst das ECHTE `docs/UPDATE_LOG.md` des Repos
   geladen, dessen Banner-Text nichts mit diesem Test zu tun hat, wie der erste Lauf zeigte) mit
   einem Eintrag, der einen `asset:`-Marker enthält. Drei neue Prüfungen: kein `<img>` im
   Banner, Alt-/Fließtext sichtbar, keine Konsolenfehler.
2. **1×1-Testbild machte zwei Prüfungen wirkungslos.** `naturalWidth=1` bewies den echten
   Byte-Roundtrip, aber weder griff `.preview img { max-width: 100% }` bei einem 1px-Bild, noch
   war der Screenshot auswertbar (ein Farbfleck von 1×1px ist im Bild unsichtbar). Behoben:
   echtes 900×200-PNG (eigener kleiner PNG-Encoder im Skript, `zlib`/`struct`, keine neue
   Abhängigkeit), zwei neue Prüfungen (`naturalWidth == 900`, gerenderte Breite ≤ Panelbreite).
   Screenshot danach tatsächlich ausgewertet, nicht nur „geschrieben" behauptet — zeigt ein
   korrekt auf die Panelbreite begrenztes blaues Rechteck unter dem Absatztext.
3. **Tabu-Diff-Kommando war zu eng.** Lief bisher nur gegen `storage mcpserver phase4_auth`;
   `phase5_ui/webui/security.py` gehört ebenfalls zur Tabu-Liste dieser Phase (nur
   `static/**`/`api.py`/`serializers.py` sind für Bilder geöffnet) und fehlte im Kommando. Leer,
   aber jetzt mit dem vollständigen Satz geprüft.
4. **Dokumentiert, bewusst nicht behoben — kein Sicherheitsfund, aber ein falsches Plan-Modell:**
   `resolveAssetSrc()` schreibt ausschließlich `asset:<id>`-Marker um; ein händisch eingetragener
   Pfad wie `![x](/api/v1/items/itm_ANDERES/assets/ast_XYZ)` läuft an dieser Auflösung vorbei und
   besteht `safeSrc()`s Regex trotzdem, weil die Regex nur die **Form** prüft, nicht die
   Herkunft aus einem `asset:`-Marker. Das widerspricht dem Plan-Mentalmodell „`src` stammt immer
   aus einer Marker-Auflösung". **Kein Eskalationspfad:** `_assets_get_one` (Step B2) löst die
   ACL ausschließlich über die `item_id` **im Pfad** auf, nicht über das Item, in dessen Body der
   Link steht — ein Leser kann so nur Assets laden, für die er ohnehin schon `can_read_item_
   as_human()` besteht, und es gibt keinen Rückkanal, über den ein Autor das Ergebnis beobachten
   könnte (kein Exfil-Kanal). Vorgemerkt für B4/B5, falls dort eine Markdown-Erzeugung durch
   Claude selbst hinzukommt — dann würde die Form-statt-Herkunft-Lücke relevanter.

**Playwright gegen eine Wegwerf-Instanz (Standing Permission, Port 8799, `tmp`-`DATA_ROOT`,
eigene `AuthStore`/`DEK`, eigenes `UPDATE_LOG.md`, echter `uvicorn`-Prozess + echter Chromium,
kein Repo-Artefakt):** 13/13 grün — Einladung/TOTP/Login-Roundtrip, Update-Banner mit
`asset:`-Marker (drei Prüfungen, Fund 1 oben), Bild-Upload-Roundtrip (`201`, Marker in der
Textarea), Vorschau zeigt das Bild mit den echten Abmessungen, `max-width`-Begrenzung wirkt,
Screenshot geschrieben UND angesehen, `javascript:`/fremde Domain werden weder als `<img src>`
übernommen noch lösen sie einen Netzabruf aus, keine Konsolenfehler über den gesamten Lauf.
Skript liegt im Scratchpad (`/tmp/.../e2e_asset_upload.py`), kein Repo-Artefakt, P5-T gilt
unverändert (kein Unit-Test für JS).

**Tests:** `pytest` 818 unverändert (P5-T: JS bleibt unit-ungetestet, keine neue Python-Datei
in diesem Step). Tabu-Diff (`storage/**`, `mcpserver/**`, `phase4_auth/**`,
`phase5_ui/webui/security.py`) — jetzt mit dem vollständigen Satz geprüft (Advisor-Fund 3): leer.

**Verifiziert:** `pytest` 818/818 (Regressionsprobe, unverändert), Playwright 13/13 grün und
per Screenshot gesehen, Tabu-Diff (vollständiger Satz) leer, `git status` passt zur erwarteten
Step-B3-Berührungsfläche (`webui/static/{app.html,app.css,js/{markdown,editor}.js}`).

**Offen für die nächste Session:**
- Commit + Push (Nikinger-Freigabe ausstehend zum Zeitpunkt des Schreibens).
- Block B Step B4 (MCP-Asset-Tools, `mcpserver/tools.py`) ist der nächste Schritt — dort auch
  der `ItemNotFound`-Fehlertext-Fund aus B1, die `filename`-Persistenzfrage (zweimal vertagt)
  und Advisor-Fund 4 oben (Form-statt-Herkunft-Lücke in `safeSrc()`) mitdenken.
- Gate A→B (echte Connector-Probe für Block A) steht weiterhin aus, unverändert — Block B darf
  weitergebaut, aber nicht vor diesem Gate deployt werden.
- Bekannte Doku-Schuld (`phase6_shares/CLAUDE.md` Block-C-Text stale) und der
  `test_authctl.py`-Flake bleiben unverändert offen.

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

## Session stopped — 2026-08-20 (Block A gebaut: get_item_meta, Beschreibungen, in_body=)

**Auftrag:** Nikinger empfahl Block A zuerst (reine `tools.py`-Arbeit, keine Abhängigkeit von
Block B, „unter Druck fällt Block B weg, nie Block A" laut Plan-Mission) und bat um atomare
Schritte, damit `/context` dazwischen geprüft werden kann.

**Gebaut, Steps A1+A2+A4 in einem Durchgang** (A2 zieht `get_item`s Beschreibung auf
`get_item_meta` vor, das ohne A2 noch nicht existiert hätte — Forward-Reference vermieden statt
mit xfail/TODO offengelassen; A4 macht `search_items`s A1-Beschreibungssatz „…oder
`in_body=True` setzen" wahr, statt eine Beschreibung für einen noch nicht existierenden
Parameter zu schreiben):
- `mcpserver/tools.py` — `_status_hint()` (aus `storage.models.STATUS_VALUES` generiert, nie
  abgetippt, P6.5-C), `WRITE_TOOL_DIVISION`, `_LIST_SPACES_POINTER` als Modul-Helfer neben
  `compact_json()`. Beschreibungen von `list_spaces` (Falschaussage „nur eigener Space" raus,
  P6.5-B), `search_items` (Suchreichweite ehrlich benannt + `in_body`-Hinweis, P6.5-H),
  `get_item` (Verweis auf `get_item_meta`), `create_item`/`update_item`/`append_to_item`/
  `patch_item` (`WRITE_TOOL_DIVISION` + `_status_hint()` an den beiden erstgenannten,
  `_LIST_SPACES_POINTER` an `create_item`/`update_item`, Bulk-Append-Hinweis an
  `append_to_item`, P6.5-G).
- Achtes Tool `get_item_meta(item_id) -> str` (P6.5-E/F) — gleiche Reihenfolge wie `get_item`
  (`_authenticated_principal()` → `acl_of()` → `can_read_item` → `store.get(repair_drift=False)`
  → `compact_json`), `repair_drift=False` bewusst anders als `get_item` (reines Lesen soll nie
  einen Write auslösen, den die Antwort selbst nicht zeigt). `register()`s Rückgabedict um
  `"get_item_meta"` erweitert, Moduldocstring „sieben"→"acht Tools" nachgezogen.
- `storage/store.py :: search()` bekommt `in_body: bool = False` (P6.5-N4) — `item.body` ist
  über `_row_to_item()` ohnehin schon geladen, kein zusätzlicher Datei-Zugriff. `search_items`
  reicht es durch.
- `scripts/mcp_smoke.py` — neuer `get_item_meta`-Check direkt nach `get_item (eigen)`, 13→14.
- `phase2_mcp/tests/test_app.py` — `test_tools_list_returns_seven_tools` → `..._eight_tools`
  (Menge um `get_item_meta` erweitert), `test_all_seven_tools_are_callable_over_http` →
  `..._eight_tools_are_callable_over_http` (echter `get_item_meta`-Aufruf ergänzt, nicht nur
  umbenannt).

**Tests:** 15 neu (6 Beschreibungstests + 4 `get_item_meta` in `test_tools.py`, 2
`in_body`-Durchreichung in `test_tools.py`, 3 `in_body` in `phase1_storage/tests/test_store.py`)
— mehr als der Plan als Minimum nannte (14: A1 6 + A2 4 + A4 4), weil `in_body` sowohl auf
Store- als auch auf Tool-Ebene je einen Default- und einen Positiv-Fall bekam statt nur einen
Durchreichungstest. `pytest` 772→**787**, alle grün (zwei volle Läufe, kein Flake diesmal).
`mcp_smoke.py` 14/14 grün. Charakterisierungstests (P6-D/P6.5-U) vor und nach byte-identisch
grün. Tabu-Diff (`permissions.py`/`server.py`/`asgi.py`/`phase4_auth/**`/`index.py`/
`webui/security.py`/`webui/static/**`) leer.

**`_description_of()`-Testhelfer, V63 geschlossen:** gegen das reale `fastmcp==3.4.4` geprüft
statt angenommen — `mcp._tool_manager` existiert auf der öffentlichen `FastMCP`-Klasse nicht
mehr; der einzige Weg an eine Tool-Beschreibung ist das (async) `await mcp.get_tool(name)` →
`FunctionTool.description`. Anders als der Rest der Suite (die die zurückgegebenen Python-
Funktionen direkt aufruft/über `inspect.signature()` prüft) baut dieser eine Testblock deshalb
eine zweite, unregistrierte `FastMCP`-Instanz (`described_mcp`-Fixture) nur für die
Beschreibungs-Assertions.

**Verifiziert:** `pytest` 787/787 (zwei Läufe), `mcp_smoke.py` 14/14, `git diff` auf den Tabu-
Pfaden leer, Charakterisierung byte-identisch. Nicht verifiziert (bewusst, Gate A→B): eine echte
Connector-Probe durch den Nikinger — Block A ist gebaut, aber **nicht deployt**.

**Offen für die nächste Session:**
- Commit + Push (Nikinger-Freigabe ausstehend zum Zeitpunkt des Schreibens).
- Gate A→B: echte Connector-Probe durch den Nikinger, bevor Block A deployt wird — ein Deploy,
  das Beschreibungsfehler und den ersten Binärdatenpfad (Block B) bündelt, macht jede
  Fehlersuche danach zweideutig (Plan §3, Gate-Absatz).
- Block B Step B1 (Storage-Fundament, Bilder) kann parallel gebaut werden — P6.5-T ist
  angekündigt, keine Abhängigkeit von Block A.
- Bekannte Doku-Schuld (`phase6_shares/CLAUDE.md` Block-C-Text stale, near Softcap) und der
  `test_authctl.py`-Flake bleiben wie im vorherigen Block vermerkt, unverändert offen.

## Session stopped — 2026-08-20 (Step 0 gestartet)

**Herkunft:** Nikinger bat um eine Opus-Planungssession für die zwei tatsächlich noch offenen
QoS-Punkte (Werkzeug-Ergonomie-Rest, Block C Bilder) — der ursprüngliche Auftragstext listete
daneben drei Dinge als „zwingend", die bereits gebaut waren (`patch_item`, das neue Dateisystem,
Update-Banner); vor dem Start korrigiert, siehe Claude-Code-Session-Transkript. Ergebnis:
`docs/concepts/phase6_5_tools_images_plan.md` (Opus, Hintergrund, ~882s), sechs offene Fragen
N1–N6 (kein `AskUserQuestion` im Subagenten verfügbar).

**Nikinger-Entscheidungen (`AskUserQuestion`, live in der Claude-Code-Session), in Plan §0.0
gelockt:**
- **N1:** Phase **6.5**, nicht 7/8 — sitzt zwischen der gebauten Phase 6 und der reservierten
  Phase 7 (Space-Admin-UI). Keine Kollision mit `app.html`s „kommt in Phase 7"-Zeichenkette, die
  bleibt unangetastet.
- **N2:** Verzeichnis `phase6_5_tools_images/` (dieses hier).
- **N3:** Bulk-Append **nicht** bauen — Befund: heute schon über mehrzeiligen Text in einem
  `append_to_item`-Aufruf möglich, nur ein Beschreibungssatz nötig.
- **N4:** Body-Volltextsuche für die MCP-Fläche **als Opt-in** bauen (`in_body: bool = False`) —
  `Store.search()` lädt jede Datei ohnehin vollständig, kostet nichts zusätzlich. Q1 (Web-UI,
  keine Body-Suche) bleibt unangetastet.
- **N5 (=B5):** Bild entfernen per **Verschieben** nach `_assets/<item_id>/_trash/`, Entscheidung H
  bleibt formal unangetastet. **Nikinger-Vormerkung, kein Auftrag dieser Phase:** `_trash/` wird
  nie automatisch geräumt — anders als kB-große `.md`-Dateien können MB-große Bilder Git-Historie/
  `DATA_ROOT` über Zeit zu GB-Größen aufwachsen lassen. Braucht mittelfristig eine eigene
  operative Lösung (`diagnose.sh`-Meldung ab Schwelle, oder Operator-Purge-Skript analog zum
  Hard-Delete-Muster aus P1 Entscheidung H).
- **N6:** `MAX_MCP_ASSET_BYTES = 1 MiB` für MCP-Uploads (Web-UI bleibt bei 5 MiB, B2) — Nikinger-
  Begründung: Claude wird über MCP nur selbst erzeugte SVGs oder kleine Screenshots hochladen,
  keine großformatigen Fotos.

**Vier der fünf `IMAGES_PLAN.md`-Fragen (B1–B4) waren bereits vorher entschieden** und in den
Planungsauftrag eingearbeitet: B1 Blobs in Git-Historie ja (mit Größenriegel), B2 5 MiB je Bild
(Web-UI), B3 Bildbytes fremder Items nur bei Schreibrecht **und** nie automatisch — auch nicht bei
eigenen Items, nur auf direkte Anfrage, B4 MCP-Upload erlaubt, aber Ankündigungspflicht bei
**jedem** Aufruf (keine Dauererlaubnis).

**Step 0 heute ausgeführt:**
- `pytest`-Baseline real gemessen (nicht nur aus der Doku übernommen): erster Lauf 771 passed/1
  failed (`phase4_auth/tests/test_authctl.py::test_revoke_kills_the_family`), isoliert grün, auf
  einem zweiten vollen Lauf **772/772 grün** — ein reihenfolgeabhängiger Flake, kein durch diese
  Session verursachter Schaden (keine Codeänderung angefasst). Baseline bestätigt: **772**.
- Fünfte Contract-Öffnung angekündigt (`phase1_storage/CLAUDE.md`, siehe „Geerbte Contracts").
- `phase6_shares/IMAGES_PLAN.md` als nachrangig markiert, V-Register-Übernahme (V59–V62 →
  dieselben Nummern im neuen Plan, kein Duplikat) dort explizit vermerkt.
- `ROADMAP.md`: neue Phase-6.5-Sektion ergänzt.
- `docs/INDEX.md`: Eintrag von „Next phase" auf den jetzt existierenden Phase-Head umgestellt.
- `app.html` Z. 281 **nicht** angefasst (N1-Ergebnis macht das unnötig, gegen den echten Code
  verifiziert).

**Offen für die nächste Session:**
- Diesen Session-stopped-Block + `docs/INDEX.md`/`ROADMAP.md` committen (Nikinger-Freigabe
  ausstehend zum Zeitpunkt des Schreibens).
- Step 0 Rest: keiner — alle acht Punkte des Plans sind entweder erledigt oder als „keine Aktion
  nötig" verifiziert (N1/`app.html`).
- Block A (Steps A1–A4) kann direkt beginnen — keine Abhängigkeit von Block B.
- Block B Step B1 (Storage-Fundament) kann beginnen — P6.5-T ist angekündigt.
- **Bekannte Doku-Schuld, nicht in diesem Step behoben:** `phase6_shares/CLAUDE.md` nennt Block C
  weiterhin als „geplant, nicht gebaut (`IMAGES_PLAN.md`, fünf offene B1–B5)" — stale seit der
  heutigen Nachrangig-Markierung von `IMAGES_PLAN.md`. Der Head liegt bei ~40.863 Bytes, ~100
  unter dem Softcap — eine Korrektur dort braucht zuerst eine Rotation
  (`scripts/rotate_session_block.sh`), bewusst nicht in diesem Docs-Commit mitgemacht, um zwei
  unabhängige mechanische Vorgänge nicht zu vermischen. Vor der nächsten Änderung an diesem Head
  einplanen.
- **Bekannter Flake, nicht Scope dieser Phase:** `phase4_auth/tests/test_authctl.py::
  test_revoke_kills_the_family` schlug im ersten vollen `pytest`-Lauf dieser Session fehl,
  isoliert und im Re-Run grün — reihenfolgeabhängig. Vermerkt in `phase4_auth/CLAUDE.md`, damit
  ein künftiges „Subtask nicht grün" nicht neu diagnostiziert werden muss.

