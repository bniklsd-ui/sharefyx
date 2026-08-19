---
status: live
purpose: Zusatzplan zu P6 Block C — Bilder in Items (Speicherung, Referenzschema, UI-Anzeige, MCP-Fläche, Freigaben)
read-when: bevor Block C gebaut wird, oder wenn geklärt werden muss, wie ein Bild physisch liegt und wer es sehen darf
detail: L2
up: ./CLAUDE.md
down: ../docs/concepts/phase6_shares_plan.md (Block C, nur stichwortartig) · ./GLOBAL_SEARCH_PLAN.md
updated: 2026-08-19 (neu geschrieben, Planungssession; gelockt P6-AU–P6-BB, FÜNF offene Nikinger-Entscheidungen B1–B5, Abnahmezeilen 40–47)
---

# IMAGES_PLAN.md — Block C: Bilder (P6, Zusatzplan)

> **Die einzige inhaltliche Vorgabe aus `docs/concepts/phase6_shares_plan.md`** (Block C ist dort
> nur stichwortartig skizziert, nicht ausführungsreif):
> *„Bilder können visuell im Dokument gesehen werden, technisch aber nur ein Link, Speicherlogik
> von der .md-Logik entkoppelt, effizient für Claude."*
> Alles Übrige in diesem Dokument ist Planungsarbeit dieser Session.
>
> **Muster:** Zusatzplan im Phase-Verzeichnis wie `ITEM_MOVE_PLAN.md`, kein Trio. Eigenes Dokument
> statt Erweiterung von `phase6_shares_plan.md`: jener ist ein **📕-Snapshot** und wird nicht
> editiert.

---

## ⚠️ §0 FÜNF offene Entscheidungen — vor dem Bau vom Nikinger einzuholen

> Diese Planungssession hatte **kein** interaktives Frage-Werkzeug. Die fünf Punkte unten sind
> **bewusst nicht** still aufgelöst worden, um das Dokument „fertig" aussehen zu lassen — sie sind
> echte Produkt-/Risikoentscheidungen, keine Codefragen. **Der Rest des Plans ist unter jeder
> Antwort baubar**; wo eine Antwort den Text ändert, steht es ausdrücklich dabei.

| # | Frage | Warum es eine Nikinger-Entscheidung ist | Claudes Empfehlung (**nicht** gelockt) |
|---|---|---|---|
| **B1** | **Binärdaten in der Git-Historie des `DATA_ROOT` — ja oder nein?** Hard Rule 5 verlangt „jeder erfolgreiche Write erzeugt einen Git-Commit". Bilder sind Blobs; Git speichert jede Version vollständig. Ein 20× ersetztes 2-MB-Bild = 40 MB, die nie wieder schrumpfen. Das trifft `phase3_edge`s Backup-Timer, `restore_check.sh` und die Dauer jedes `git`-Aufrufs. | Betriebsentscheidung mit irreversibler Konsequenz (Historie umschreiben ist danach teuer). Hard Rule 5 zu beugen ist außerdem eine Regeländerung, die ausdrücklich dem Nikinger gehört — nicht Claude. | **Ja, mit Größenriegel** (B2): Bilder werden mitcommittet, dafür harte Obergrenze je Datei. Undo/Historie „kostenlos" ist der Grund, warum Hard Rule 5 existiert; ein Bild, das man nicht zurückholen kann, ist genau der Verlust, gegen den sie schützt. |
| **B2** | **Obergrenze je Bild und je Space?** Heute gilt `MAX_BODY_BYTES = 1 MiB` für JSON-Bodies (`webui/api.py` Z. 105) — ein Upload-Weg braucht seine eigene Zahl. | Reine Nutzungsfrage (was für Bilder legst du ab: Screenshots? Fotos?), Claude hat dazu keine Datenbasis. | **2 MiB je Bild**, kein Space-Gesamtbudget in v1 (`diagnose.sh` meldet die Größe stattdessen operativ — messen vor deckeln). |
| **B3** | **Darf Claude über MCP die echten Bildbytes eines Items aus einem FREMDEN Space holen?** | **Sicherheitsentscheidung, nicht Ergonomie.** Hard Rule 4s `<untrusted_content>`-Wrapping schützt **Text**. Bildbytes vor einem sehenden Modell sind ein Prompt-Injection-Kanal, den kein Text-Wrapper einfasst (Anweisungen im Bild). Genau die Bedrohung, gegen die Hard Rule 4 geschrieben wurde, nur in einem Format, das sie nicht abdeckt. | **Nein in v1.** `get_item_asset` liefert Bytes nur für Items im **eigenen** Space; für fremde Items nur Metadaten (Name, Größe, MIME) plus ein Klartext-Hinweis. Restriktiv anfangen ist reversibel, andersherum nicht. |
| **B4** | **Darf Claude Bilder HOCHLADEN (MCP-Schreibweg), oder ist Hochladen v1 ausschließlich Web-UI?** | Scope-Frage. „Effizient für Claude" in der Vorgabe bezieht sich sprachlich aufs **Lesen**; ob Schreiben gemeint war, kann Claude nicht raten. | **Nur Web-UI in v1.** Ein Bild per base64 durch ein MCP-Tool zu schieben ist token-teuer und hat keinen genannten Anwendungsfall. Der Seam bleibt (P6-BB). |
| **B5** | **Darf ein Bild wieder ENTFERNT werden — und wenn ja, wie?** `phase1_storage/CLAUDE.md` lockt Entscheidung **H**: *„Kein Delete im Kern-API. `status: archived` + `_archive/`. Hard Delete nur als separates, bestätigungspflichtiges Operator-Skript."* `phase6_shares_plan.md` §0.5 (F2) hält vollständiges Löschen ausdrücklich draußen. Ein `store.delete_asset()` wäre die **erste** Löschoperation im Kern-API. | **Regelaufweichung an einer gelockten Entscheidung** — gehört per Working-Style („Gelockte Entscheidungen bleiben gelockt") dem Nikinger, nicht Claude. Ein versehentlich hochgeladenes Bild ist andererseits ein Blob, kein Wissensträger; „nie entfernbar" ist bei Binärdaten eine andere Aussage als bei einer Notiz. | **Verschieben statt Entfernen:** `_assets/<item_id>/_trash/`. Damit bleibt H unangetastet (dieselbe Bauart wie `_archive/`), die Referenz im Body läuft ins Leere und rendert als Alt-Text, und ein echtes Hard Delete bleibt Operator-Skript-Sache. |

**B5 und B1 hängen zusammen** — und zwar so, dass die Reihenfolge zählt: **wenn B1 = ja** (Blobs
werden mitcommittet), gibt ein Entfernen die Bytes **nicht** frei, sie bleiben in der Git-Historie.
Ein „Löschen" ist dann ausschließlich eine Aufräum-/Anzeigefrage, **keine** Platzfrage — und das
`_trash/`-Verschieben aus der Empfehlung kostet gegenüber einem echten `unlink` faktisch nichts.
**Wenn B1 = nein**, ist es umgekehrt: dann ist Entfernen der einzige Weg, Platz zurückzubekommen,
und ein `_trash/` ohne späteres Aufräumen verschiebt das Problem nur.

**Wenn B1 = nein:** `_assets/` wandert in die `.gitignore` des `DATA_ROOT`, `history.py` bleibt
unangetastet, und Abnahmezeile 43 entfällt ersatzlos. Alles Übrige bleibt gleich.
**Wenn B3 = ja:** §4 Punkt 1s Fail-closed-Zweig wird zu einer Warnung, und Abnahmezeile 46 dreht
sich um.
**Wenn B5 = „gar nicht":** `delete_asset()` und `DELETE /api/v1/items/{id}/assets/{id}` entfallen
ersatzlos; alles Übrige bleibt gleich.

---

## §1 Gelockte Entscheidungen (P6-AU – P6-BB)

Diese acht sind **keine** offenen Fragen: sie folgen entweder zwingend aus bestehenden Hard Rules
und bereits im Code vorhandenen Nahtstellen, oder es sind reine Formatfestlegungen ohne
Nikinger-Stake.

| # | Entscheidung | Begründung / Beleg im Code |
|---|---|---|
| **P6-AU** | **Bilder liegen unter `<DATA_ROOT>/<space>/_assets/<item_id>/<asset_id>.<ext>`** — pro **Item**, nicht pro Space, nicht in einem globalen Pool. | `_assets` steht **bereits** in `RESERVED_DIR_NAMES` (`storage/files.py` Z. 17, neben `_archive`) und wird von `Store.list_spaces()`s `rglob`-Walk bereits ausgefiltert (`store.py` Z. 316–321, Test `test_list_spaces_excludes_archive_and_assets_from_folders`). **Der Seam existiert seit P6 Step 4 und wurde nie belegt.** Kein neuer reservierter Name, keine Änderung an `validate_folder()`, kein Bild taucht als Nutzer-Ordner im Baum auf. |
| **P6-AV** | **Ein Cross-Space-Move zieht das Bildverzeichnis mit** — `Store.move()` verschiebt zusätzlich `<quelle>/_assets/<item_id>/` nach `<ziel>/_assets/<item_id>/`, per `os.replace` des **Verzeichnisses**, mit `fsync` auf Quell- und Zielelternverzeichnis (dasselbe Muster wie `files.move_file()`). Keine Byte-Kopie, keine Referenzumschreibung im Body. | Genau der Grund für die Pro-Item-Ablage aus P6-AU. Die Alternative (Bilder pro Space gepoolt) erzwingt entweder eine Byte-Kopie plus Rewrite aller `asset:`-Referenzen im Body — beides fehleranfällig und nicht atomar — oder einen space-übergreifenden Auslieferungsweg mit einer **zweiten**, eigenen ACL. Eine zweite Rechteoberfläche ist genau das, was `SharePolicy` in Step 5 zusammengeführt hat. |
| **P6-AW** | **Ein Bild hat keine eigene ACL. Es erbt die des referenzierenden Items, über die Route.** Auslieferung ausschließlich über `GET /api/v1/items/{item_id}/assets/{asset_id}` mit `store.acl_of(item_id)` + `permissions.can_read_item_as_human(...)` — **derselbe** Codepfad wie `_items_get_one` (`api.py` Z. 400–409). | „Wer das Item lesen darf, darf seine Bilder sehen" ist die einzige Regel, die man nicht auseinanderlaufen lassen kann. Ein eigenes ACL-Feld für Assets wäre eine dritte Wahrheit neben `.share.yml` und `share_read`/`share_write`. |
| **P6-AX** | **Referenzschema im Markdown: `![Alt](asset:<asset_id>)`.** Ein eigenes, nicht-auflösbares Schema — kein relativer Pfad, keine `http(s)`-URL. `asset_id` ist `ast_<8hex>`, gleiche Bauart wie `itm_<8hex>` (Entscheidung F aus P1). | Ein relativer Pfad würde im Editor, im Browser und in Claudes Kontext je etwas anderes bedeuten. Ein `asset:`-Präfix ist an jeder Stelle eindeutig als „das muss aufgelöst werden" erkennbar und kann **niemals** versehentlich ein Live-Abruf nach außen werden — die Datei bleibt roh und portabel, „technisch aber nur ein Link" wörtlich erfüllt. |
| **P6-AY** | **Die Datei bleibt die Wahrheit, auch für Bilder.** Kein Asset-Eintrag im SQLite-Index, keine neue Tabelle, keine neue Spalte. Die Liste der Assets eines Items ist ein `iterdir()` auf `_assets/<item_id>/`. | Hard Rule 2 wörtlich. Ein Index über Assets wäre eine Ableitung, die ohne Not zusätzlich driften kann; die Verzeichnisauflistung ist billig und immer wahr. |
| **P6-AZ** | **Schreiben atomar und fail-closed:** `tmp`-Datei im Zielverzeichnis, `os.replace`, `fsync` auf dem Verzeichnis — die bestehende `files.py`-Mechanik, kein zweiter Schreibpfad. MIME-Typ wird aus den **Magic Bytes** bestimmt, nie aus Dateiendung oder `Content-Type` des Clients. Zulässig: **PNG, JPEG, GIF, WebP**. Alles andere → `422`. | Hard Rule 5. Der Magic-Byte-Riegel schließt „SVG mit eingebettetem Script" und „`.png`, das HTML ist" — `nosniff` allein reicht nicht, weil der Server den Typ selbst setzt. **SVG ist bewusst ausgeschlossen** (aktives Format). |
| **P6-BA** | **Kein serverseitiges Bildverarbeiten.** Kein Skalieren, kein Re-Encoding, keine Thumbnails, keine EXIF-Auswertung, keine Bilderkennung. Der Server legt Bytes ab und gibt Bytes zurück. Anzeigegröße ist CSS. | Core Principle („Der Server ist dumm") plus: jede Bildbibliothek ist eine neue Angriffsfläche für einen Dienst, der sonst nur Text parst. Wer hier Pillow einbauen will → **stop**. |
| **P6-BB** | **Hochladen läuft in v1 über die Web-UI**, nicht über MCP (vorbehaltlich **B4**). Auf der MCP-Seite ist der Standardweg **Link-only**: `get_item` liefert weiterhin nur den Body-Text mit `asset:`-Referenzen plus eine kompakte `assets:`-Liste (id/MIME/Bytes) in der Quittung. Echte Bildbytes gibt es nur über ein **eigenes, ausdrücklich aufgerufenes** Tool. | „Effizient für Claude" ist die Vorgabe. Base64 in jeder `get_item`-Antwort wäre das genaue Gegenteil — dieselbe Kostenklasse wie der bereits gemeldete `get_item`-Volltext-Befund (Vormerkung 2026-08-14). |

---

## §2 Berührungsfläche

**Erlaubt:**
- `phase1_storage/storage/{files,store}.py` — **fünfte, benannte Contract-Öffnung** (P6-C erlaubt
  `storage/` in dieser Phase; die Öffnung ist in `phase1_storage/CLAUDE.md` unter „Geerbte
  Contracts" **anzukündigen, bevor** Code entsteht — dieselbe Disziplin wie bei `patch()`,
  `acl_of()` und `move()`).
- `phase5_ui/webui/{api,serializers,static_routes}.py`, `webui/static/**`.
- `phase2_mcp/mcpserver/tools.py` (P6-C erlaubt es ausdrücklich).
- `phase3_edge/scripts/diagnose.sh` (neue Prüfung).

**Tabu, `git diff` leer:** `phase2_mcp/mcpserver/permissions.py` (die Rechtepolitik bekommt für
Bilder **nichts** Neues — das ist P6-AW), `phase2_mcp/mcpserver/server.py`, `phase4_auth/**`,
`phase1_storage/storage/index.py` (P6-AY).

**Kein CSP-Eingriff nötig:** `webui/security.py` Z. 43–47 liefert bereits
`img-src 'self' data:`. Bilder von derselben Herkunft sind damit **heute schon** erlaubt.
Wer diesen Header anfasst, hat etwas falsch gemacht.

---

## §3 Schritt-Sequenz

### Step C1 — Storage-Fundament (`storage/`, kein Adapter)

`phase1_storage/storage/files.py`:
- `ASSET_ID_PREFIX = "ast_"`, `new_asset_id()` (Zwilling zu `new_item_id()`).
- `ASSET_MIME_TYPES: dict[bytes, str]` — Magic-Byte-Präfix → MIME, für die vier Formate aus P6-AZ.
  `sniff_image_mime(data: bytes) -> str | None`.
- `asset_dir(data_root, space, item_id) -> Path` → `<data_root>/<space>/_assets/<item_id>`.
- `asset_path(data_root, space, item_id, asset_id, ext) -> Path`.
- `move_asset_dir(src_dir, dst_dir)` — `os.replace` des Verzeichnisses + `fsync` beider
  Elternverzeichnisse. **No-op, wenn `src_dir` nicht existiert** (der Normalfall: die meisten Items
  haben keine Bilder).

`phase1_storage/storage/store.py` (neu, alle unter `self._lock`, alle mit Git-Commit gemäß **B1**):
- `put_asset(item_id, *, data: bytes, filename: str | None = None) -> AssetInfo`
- `list_assets(item_id) -> list[AssetInfo]` — reines `iterdir()`, sortiert (P6-AY).
- `get_asset(item_id, asset_id) -> tuple[bytes, str]` (Bytes + MIME)
- `delete_asset(item_id, asset_id) -> None` — **Gestalt und Existenz hängen an offener Entscheidung
  B5** (§0), nicht an dieser Zeile. Empfehlung dort: nach `_assets/<item_id>/_trash/` verschieben
  statt `unlink`, damit Entscheidung **H** („kein Delete im Kern-API") unangetastet bleibt. **Nicht
  bauen, bevor B5 beantwortet ist** — und bei jeder Antwort außer „gar nicht" gehört eine datierte
  Notiz in `phase1_storage/CLAUDE.md` unter „Geerbte Contracts", weil H eine gelockte P1-
  Entscheidung ist.
- `move()` (existiert seit Step 7b) ruft zusätzlich `files.move_asset_dir(...)` — **innerhalb**
  derselben Lock-Sektion und **vor** dem Git-Commit, damit ein Move genau **einen** Commit erzeugt
  (Abnahmezeile 26s bestätigte Mechanik bleibt erhalten).
- `archive()` lässt `_assets/<item_id>/` **stehen** und zieht es nicht nach `_archive/` — das Item
  behält seine Referenzen, ein Wiederherstellen findet die Bilder unverändert vor.

`AssetInfo` (neu, in `storage/models.py`): `id`, `mime`, `bytes`, `filename` (bereinigt, rein
kosmetisch — **nie** für die Pfadbildung verwendet), `created`.

### Step C2 — REST-Fläche (`webui/`)

| Route | Rechteprüfung | Anmerkung |
|---|---|---|
| `POST /api/v1/items/{item_id}/assets` | `acl_of` + `can_write_item_as_human` | Rohe Bytes im Request-Body (**kein** multipart, kein base64 — kein Parser-Zuwachs). `Content-Type` wird **ignoriert** (P6-AZ). Eigener Größenriegel `MAX_ASSET_BYTES` (**B2**), unabhängig von `MAX_BODY_BYTES`. CSRF wie jeder Schreibpfad (`_require_csrf_json`s Herkunftsprüfung). `201` mit `AssetInfo`-JSON. |
| `GET /api/v1/items/{item_id}/assets/{asset_id}` | `acl_of` + `can_read_item_as_human` (**P6-AW**) | Antwort: rohe Bytes, `Content-Type` aus den Magic Bytes, `X-Content-Type-Options: nosniff` (kommt bereits aus `ui_security_headers()`), `Content-Disposition: inline`, `Cache-Control: no-store` (Standard — der Inhalt ist ACL-abhängig, ein `immutable`-Cache wäre hier falsch, anders als bei den gehashten Font-Assets in `static_routes.py`). |
| `GET /api/v1/items/{item_id}/assets` | wie Lesen | Liste für den Editor. |
| `DELETE /api/v1/items/{item_id}/assets/{asset_id}` | wie Schreiben | Siehe `delete_asset()`-Vorbehalt in C1. |

`item_to_json()` bekommt `"assets": [...]` (`serializers.py`) — Metadaten, kein Fließtext, damit
unproblematisch auch für fremde Items (dieselbe Einstufung wie der Sichtbarkeits-Chip, Step 7
Commit 2).

### Step C3 — Web-UI: Anzeigen und Einfügen

`phase5_ui/webui/static/js/markdown.js` — **die einzige Stelle, an der heute Bilder sterben:**
- `ALLOWED_TAGS` (Z. 186–189) um `"IMG"` erweitern.
- `ALLOWED_ATTRS` (Z. 190–194) um `IMG: new Set(["src", "alt"])`.
- Neue `safeSrc(src)` neben `safeHref()` (Z. 197–202): akzeptiert **ausschließlich** einen Pfad,
  der exakt auf `/api/v1/items/<itm_…>/assets/<ast_…>` passt (strenges Regex, wie `safeHref`s
  `#item/`-Zweig). Alles andere → Attribut entfernen und das `<img>` durch seinen `alt`-Text
  ersetzen. **Keine `data:`-URIs im Body**, obwohl die CSP sie erlaubt (die Lockerung dort gilt dem
  Inline-SVG-QR-Code aus P4, nicht Nutzerinhalt).
- Im `markdownToHtml()`-Bildzweig wird `asset:<asset_id>` beim Rendern zu
  `/api/v1/items/<aktuelles item>/assets/<asset_id>` aufgelöst. Die Auflösung braucht die Item-ID
  ⇒ `markdownToHtml(src, options)` bekommt einen optionalen zweiten Parameter. **Fallende
  Kante beachten:** `updates.js` ruft `markdownToHtml()` ohne Item-Kontext — dort muss ein
  `asset:` schlicht **nicht** auflösen und als Alt-Text erscheinen, nicht crashen.
- **P5-Y bleibt unangetastet:** kein serverseitiges HTML-Rendern, nichts davon wandert in Python.

`editor.js`: „Bild einfügen"-Knopf in der Formatierhilfen-Leiste — Dateiauswahl → `POST` →
`![<Dateiname>](asset:<id>)` an der Cursorposition einfügen (dieselbe Mechanik wie der bestehende
Link-Einfüger, `editor.js` Z. 465–466). Einfügen per Zwischenablage/Drag&Drop ist **v2**, nicht
v1 — der Knopf ist der Pflichtweg (dieselbe Regel wie P6-AB beim Verschieben).

`app.css`: `.md-body img { max-width: 100%; height: auto; }` — mehr nicht (P6-BA).

### Step C4 — MCP-Fläche (`mcpserver/tools.py`)

- `get_item` bekommt in der Quittung eine `assets`-Liste (id/MIME/Bytes). **Kein** base64, **keine**
  Änderung am Body-Text — der trägt die `asset:`-Referenzen ohnehin schon (P6-BB).
- **Achtes Tool `get_item_asset(item_id, asset_id)`** — liefert das Bild als MCP-`ImageContent`
  (base64 + `mimeType`). Rechteprüfung: `acl_of()` + `can_read_item(..., surface=Surface.AGENT)`,
  **plus** der Fail-closed-Riegel aus **B3** (Empfehlung: fremde Items → nur Metadaten + Klartext-
  Hinweis, keine Bytes). Beschreibung nennt die Kosten ausdrücklich („teuer, nur aufrufen, wenn der
  Bildinhalt wirklich gebraucht wird").
- `create_item`/`update_item`/`patch_item` bekommen **nichts** (B4 = nur Web-UI).

**`[VERIFY]` V59:** ob `fastmcp>=3.4,<3.5` (P2-A, gepinnt) das Zurückgeben von `ImageContent` aus
einem Tool überhaupt unterstützt, und in welcher Form. **`[VERIFY]` V60:** ob claude.ai-
Custom-Connectors `ImageContent` bzw. `resource_link` aus einem Tool-Ergebnis tatsächlich
anzeigen/verarbeiten. Beide Punkte stammen aus einer Spec-Recherche dieser Session
(MCP 2025-06-18 kennt `type:"image"` mit base64+`mimeType` sowie `type:"resource_link"`; 2025-11-25
ergänzt u. a. Icons/Tasks) — **das ist die Spezifikation, nicht die Implementierung.** Nicht als
gesichert übernehmen; **wenn V59 negativ ausfällt, entfällt Step C4s zweiter Punkt ersatzlos** und
die MCP-Seite bleibt Link-only. Der Rest des Plans ist davon unabhängig.

### Step C5 — Betrieb

- `phase3_edge/scripts/diagnose.sh`, Prüfung 13: Gesamtgröße aller `_assets/`-Verzeichnisse und
  Größe des `.git`-Verzeichnisses im `DATA_ROOT`, als **INFO** (kein Abbruchkriterium) — dieselbe
  Kategorie wie Prüfung 12.
- `docs/UPDATE_LOG.md`: Eintrag vor dem Deploy (P6-X-Gate in `deploy.sh` erzwingt das ohnehin).
- Wenn **B1 = nein**: `_assets/` in die `.gitignore` des `DATA_ROOT` (die `history.py` bereits
  anlegt) — und dann **muss** in `phase3_edge/CLAUDE.md` stehen, dass Bilder ausschließlich über
  das Dateisystem-Backup abgedeckt sind, nicht über Git.

---

## §4 Sicherheitsbetrachtung (nicht optional, hier zusammengefasst)

1. **Hard Rule 4 und Bilder.** `<untrusted_content>` wrappt **Text**. Ein fremdes Bild vor einem
   sehenden Modell ist ein Injektionskanal, den dieser Wrapper strukturell nicht erreicht — die
   Bedrohung ist dieselbe, das Gegenmittel greift nicht. Deshalb **B3**, und deshalb ist die
   Empfehlung dort restriktiv. **Das darf nicht als „durch bestehende Regeln abgedeckt"
   durchrutschen.**
2. **Auslieferungsroute.** Genau **eine** ACL-Prüfung, auf demselben Pfad wie `_items_get_one`
   (P6-AW). Kein Weg, ein Asset ohne Item-ID zu adressieren — eine geratene `ast_`-ID nützt nichts,
   ohne auch die passende `itm_`-ID zu kennen **und** Leserecht darauf zu haben.
3. **Typverwirrung.** Magic Bytes statt Client-Angabe, `nosniff`, kein SVG (P6-AZ).
4. **Pfad-Traversal.** `asset_id`/`item_id` werden **nie** aus Nutzereingaben zusammengesetzt;
   beide müssen gegen `^(ast|itm)_[0-9a-f]{8}$` validiert werden, bevor sie in einen `Path`
   fließen — dieselbe Disziplin wie `_resolve_static_path()` (`static_routes.py`).
5. **Speicherverbrauch.** Rohe Bytes gehen komplett in den Speicher (wie `_json_body()` heute
   auch). Bei **B2** = 2 MiB unkritisch; eine spätere Erhöhung braucht Streaming.
6. **Kein neues Geheimnis.** Hard Rule 1 ist von diesem Plan nicht berührt: es entstehen keine
   Tokens, Keys oder Credentials. `filename` wird bereinigt gespeichert und nie zur Pfadbildung
   benutzt.

---

## §5 Testliste (Pflicht)

`phase1_storage/tests/test_files.py` (+5): Magic-Byte-Erkennung je Format · unbekannte Bytes → `None`
· SVG wird abgelehnt · `asset_path()` verweigert eine ungültige ID · `move_asset_dir()` ist ein
No-op ohne Quellverzeichnis.

`phase1_storage/tests/test_store.py` (+8): `put_asset()` legt atomar an und erzeugt genau einen
Git-Commit (B1) · `list_assets()` ist leer für ein Item ohne Bilder · `get_asset()` liefert Bytes
und MIME · `delete_asset()` entfernt · **`move()` zieht das Asset-Verzeichnis mit und erzeugt
weiterhin genau EINEN Commit** (P6-AV, der wichtigste Test dieses Plans) · `move()` ohne Assets
verhält sich unverändert (Regression gegen die sechs Step-7b-Tests) · `archive()` lässt Assets
liegen · `list_spaces()` zeigt `_assets` weiterhin nicht als Ordner (bestehender Test, muss grün
bleiben).

`phase6_shares/tests/test_assets_acl.py` (neu, +4): fremdes Item mit `share_read` → Bild lesbar ·
fremdes Item ohne Grant → `403` · `share_read` allein erlaubt kein `POST` · Asset folgt dem Item in
den Zielspace und ist danach für die **Ziel**-Space-Mitglieder lesbar (Zwilling zu
`test_acl_decision_follows_the_item_into_the_target_space`).

`phase5_ui/tests/test_api.py` (+6): Upload/Download-Roundtrip · zu groß → `413` · falscher Typ →
`422` · `DELETE` · fremde Item-ID → `404`/`403` ohne Existenzunterschied · Assets erscheinen in
`item_to_json()`.

`phase2_mcp/tests/test_tools.py` (+3, entfällt bei V59 negativ): `get_item` listet Assets ohne
Bytes · `get_item_asset` liefert Bildinhalt für ein eigenes Item · B3-Riegel für ein fremdes Item.

Frontend: kein Unit-Test (P5-T). Stattdessen **echter Playwright-Lauf gegen eine Wegwerf-Instanz**
(Standing Permission): Bild hochladen, im gerenderten Markdown **sichtbar** (auf `naturalWidth > 0`
prüfen, nicht nur auf die Existenz des `<img>` — ein kaputter Pfad rendert trotzdem ein Element),
Screenshot ansehen, Konsolenfehler-Listener sauber. Zusätzlich: ein `![x](javascript:…)` und ein
`![x](https://fremde.example/pixel.png)` im Body werden vom Sanitizer entfernt.

**Charakterisierung** (`phase6_shares/tests/test_characterization.py`, P6-D) muss byte-identisch
grün bleiben — ein Ausschlag dort ist ein Befund, kein anzupassender Golden File.

---

## §6 Abnahmekriterien (Zeilen 40–47)

> ✅ heißt live-verifiziert durch den Nikinger, nicht gebaut.

| # | Kriterium | Wie geprüft |
|---|---|---|
| 40 | Bild in der Web-UI hochgeladen, erscheint **sichtbar** im gerenderten Dokument | Nikinger, Browser |
| 41 | Die `.md`-Datei im `DATA_ROOT` enthält nur `![…](asset:ast_…)`, keine Binärdaten, keine base64 | Nikinger, `cat` im Datenverzeichnis |
| 42 | Die Bilddatei liegt unter `<space>/_assets/<item_id>/` und taucht in der UI **nicht** als Ordner auf | Nikinger, `ls` + Browser |
| 43 | Ein Upload erzeugt genau einen Git-Commit im `DATA_ROOT` *(entfällt bei B1 = nein)* | Nikinger, `git log --oneline` |
| 44 | Fabian öffnet ein ihm freigegebenes Item mit Bild und **sieht** das Bild; ohne Freigabe liefert dieselbe Bild-URL `403` | Nikinger + Fabian, Browser + `curl` |
| 45 | Ein Cross-Space-Move nimmt das Bild mit; das Bild ist danach im Zielspace sichtbar, im Quellspace weg — **ein** Git-Commit | Nikinger, Browser + `git log` |
| 46 | Claude über den echten Connector: `get_item` zeigt Bilder als Liste ohne Bytes; `get_item_asset` verhält sich gemäß **B3** *(entfällt bei V59 negativ)* | Nikinger, echter Connector |
| 47 | Ein `![x](https://fremde.example/…)` oder `![x](javascript:…)` im Body erzeugt **keinen** Netzabruf und kein `<img>` | Nikinger, DevTools-Netzwerktab |

---

## §7 Ausdrücklich draußen

Thumbnails/Skalieren/EXIF (P6-BA) · SVG (P6-AZ) · Video/Audio/PDF/beliebige Anhänge (P5-AA bleibt
zu; dies ist ein **Bild**-Schnitt, kein Anhang-Schnitt) · Zwischenablage-/Drag&Drop-Einfügen (v2) ·
Bild-Upload über MCP (B4) · Deduplizierung gleicher Bilder über Items hinweg · ein Space-weiter
Bild-Browser · Bildsuche jeder Art (Core Principle).

---

## §8 `[VERIFY]`-Register

| # | Zu prüfen | Warum unsicher |
|---|---|---|
| **V59** | `fastmcp>=3.4,<3.5` kann `ImageContent` aus einem Tool zurückgeben | Aus der MCP-**Spec** abgeleitet, nicht gegen die gepinnte Bibliothek geprüft. Negativ ⇒ Step C4 Punkt 2 und Zeile 46 entfallen. |
| **V60** | claude.ai-Custom-Connectors zeigen/verarbeiten `ImageContent` bzw. `resource_link` | Client-Verhalten, nicht Spec. Nur über eine echte Connector-Probe klärbar (Kategorie wie V33). |
| **V61** | `os.replace` auf einem **Verzeichnis** ist auf `ext4` atomar, solange Quelle und Ziel dasselbe Dateisystem teilen und das Ziel nicht existiert | Für Dateien in P1 belegt (`ext4` per `findmnt` bestätigt), für Verzeichnisse hier angenommen. Vor dem Bau gegen die Python-Doku **und** einen echten Lauf gegenprüfen. |
| **V62** | Alle Zeilennummern in diesem Dokument | Stand 2026-08-19, `main`@`2b155ce`. Funktionsnamen sind die belastbaren Anker. |
