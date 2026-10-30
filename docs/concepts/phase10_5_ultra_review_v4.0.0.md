---
status: snapshot
purpose: Ultra-Review des Release-Kandidaten v4.0.0 (Stand 5798e19) — 22 Befunde (1 kritisch, 4 hoch, 7 mittel, 10 niedrig), Urteil „nicht freigabefähig", Reihenfolge B1–B10 vor Deploy D. Verbatim aus der Review-Session.
read-when: vor dem Fix-Block nach dem Review, vor Deploy D, oder wenn ein Befund B1–B22 zitiert wird
detail: L3
up: ../../phase10_5_finishing/CLAUDE.md
down:
  - ../PROMPTS.md   # Prompt 4 — der Auftrag dieses Reviews
updated: 2026-10-30 (gesichert von Claude Code — verbatim aus dem Ergebnis der Cloud-Session „Sharefyx v4.0.0 Code Review", 2026-10-30 06:12 UTC; die Session lag nach einem Abbruch durch einen Sicherheitsfilter still und wurde vom Nikinger fortgesetzt)
---
> **Herkunft (Claude Code, 2026-10-30):** Der folgende Text ist das **Ergebnis** der Review-Session
> (`/code-review ultra` mit Prompt 4), **verbatim** übernommen — nicht bearbeitet, nicht geprüft.
> Die Befunde sind **Aussagen der Review-Session**; die Gewissheit steht je Befund (R/C/V). Pfade
> sind relativ zu den Paketwurzeln (`storage/` = `phase1_storage/storage/`, `mcpserver/` =
> `phase2_mcp/mcpserver/`, `webui/` = `phase5_ui/webui/`, `authserver/` = `phase4_auth/authserver/`).
> Die Probeskripte und Wegwerf-Daten der Session liegen in ihrem Container, **nicht** im Repo.

# Ultra-Review Sharefyx v4.0.0 (Stand 5798e19)

**Ergebnis zuerst:** v4.0.0 ist in dieser Form nicht freigabefähig. Es gibt einen kritischen Befund (Pfad-Traversal über `asset_id`: liest und verschiebt beliebige Dateien des Dienstnutzers) und vier hohe Befunde. Zwei davon legen den Dienst nach einem Neustart dauerhaft lahm, einer bricht alle Textsuchen für alle Nutzer, einer ist eine Rechte-Inkonsistenz an fremden Home-Spaces. Der Kern ist solide: Versionierung, atomare Writes, Commit je Write, OAuth/PKCE/TOTP, CSRF, Sanitizer. Die Lücken liegen an den Rändern: fehlende Eingabevalidierung in den Adaptern, fehlende Behandlung von Dateisystemfehlern, Robustheit gegen von Hand editierte Dateien.

**Prüfweg:** vollständige Lektüre der vier Produktpakete inklusive JS, Units und Betriebsskripte. Alles Messbare lief an einer Wegwerf-Instanz im Scratchpad: tmp-`DATA_ROOT`, tmp-`auth.sqlite3`, echte `create_app()` mit In-Process-TestClient, MCP-Tools direkt aufgerufen wie in der Testsuite. Kein laufender Dienst, kein echter `DATA_ROOT`, kein Keyring, kein Tunnel, nichts committet. Testsuite im Scratchpad-venv: 1654 bestanden, 5 rot. Alle fünf scheitern nur, weil in diesem Container das `sqlite3`-Binary fehlt. Das ist kein Codebefund.

Gewissheit: **R** = reproduziert an der Wegwerf-Instanz, **C** = am Code belegt, **V** = vermutet.

## Befunde nach Schweregrad

| Nr | Schwere | Datei:Zeile | Befund | Gew. |
|---|---|---|---|---|
| B1 | kritisch | `storage/store.py:1483`, `:1501`; `mcpserver/tools.py:1065`, `:1107` | `asset_id` geht ungeprüft in `Path.glob()`. Über MCP `get_item_asset` liest jeder Principal mit einem eigenen Item beliebige Dateien (fremde Items, `.share.yml`, Auth-DB-Dateien) und verschiebt sie per `delete_asset` in seinen Papierkorb. | R |
| B2 | hoch | `store.py:612`, `:816`; `webui/api.py:792` | Ordner-Umbenennen in nicht existierenden Elternordner wirft `FileNotFoundError`, Marker bleibt, jeder `Store()`-Start scheitert erneut. Dienst startet nicht mehr. | R |
| B3 | hoch | `storage/index.py:285`, `:291`; `store.py:321` | Eine nicht parsebare `.md` im Space (etwa `README.md`) bricht den Index-Neuaufbau nach dem bereits committeten `DELETE` ab. Index leer, Dienststart mit frischem Index scheitert. | R |
| B4 | hoch | `api.py:876`, `:897` | Mitglieder eines fremden Home-Space hinzufügen oder entfernen prüft nur `can_write`, nicht `manages_space`. Ein Schreib-Gast ändert die Rechteliste des Eigentümers. | R |
| B5 | hoch | `store.py:1054`, `:133`; `api.py:1326`; `tools.py:524` | Ein Nicht-String-Tag (Hand-Edit `tags: [2026]` oder REST `tags: [1,2]`, angenommen mit 201) lässt jede Textsuche aller Nutzer mit `TypeError` sterben. `title: 2026` bricht jedes Update. | R |
| B6 | mittel | `tools.py:702`, `:891`; `api.py:1293` | Space-Name wird nicht geprüft. `space="team/"` passiert `can_write`, Datei trägt `space: team/`, Index `team`. Das eigene Item gilt als fremd und wird als `<untrusted_content>` gewrappt. | R |
| B7 | mittel | `storage/files.py:351`; `api.py:321` | Kein Titel-Längenlimit, der Slug wird Dateiname. Ab etwa 240 Bytes `OSError`, REST 500, MCP `internal_error`. Beim Update ist die Datei schon neu geschrieben, nur das Umbenennen scheitert. | R |
| B8 | mittel | `api.py:1443`, `:1480`, `:1326`; `store.py:489` | REST ohne Typprüfung: `title:123` und `folder:123` geben 500. `body:5` schreibt Datei und Index, wirft danach, kein Commit, Client sieht 500. `tags:"abc"` wird zur Buchstabenliste. | R / C |
| B9 | mittel | `mcpserver/request_log.py:221`; `logging_setup.py:11` | Einladungs-Token steht im Klartext im Request-Log (`/ui/invite/<token>`). Redigiert wird nur `/mcp/<token>`. | R |
| B10 | mittel | `store.py:1032` | `search()` gibt das Lock nach dem Index-Read frei und liest Dateien ohne Lock. Paralleles Umbenennen (Titel-Update, `trash`) gibt `FileNotFoundError` beim Leser. FastMCP 4 führt Tools im Threadpool aus, die Nebenläufigkeit ist real. | R |
| B11 | mittel | `store.py:1372` | `move()` verschiebt das Asset-Verzeichnis vor dem Item-Write. Scheitert der Write, liegen Bilder im Ziel, das Item in der Quelle. Kein Rollback. | C |
| B12 | mittel | `store.py:1016`; `tools.py:461`, `:512`; `api.py:1225` | Jeder Such- und Listenaufruf liest jede Item-Datei. Über 5000 Items wird stillschweigend abgeschnitten und `total` ist falsch. Messwerte unten. | R |
| B13 | niedrig | `store.py:1129` | `create()` prüft die zufällige ID nicht gegen den Index. Bei Kollision überschreibt das neue Item die Indexzeile des alten, das alte wird unsichtbar, die Datei bleibt. | R |
| B14 | niedrig | `tools.py:541` | `search_items(offset=-3)` liefert über Negativ-Slicing falsche Seiten und `truncated: true`. REST klemmt den Offset auf 0, MCP nicht. | R |
| B15 | niedrig | `store.py:1483` | `asset_id="*"` liefert das erste Asset des Items. Entfällt mit dem Fix zu B1. | R |
| B16 | niedrig | `webui/static/js/editor.js` (`populateStatusSelect`, Zeile 290); `store.py:1165` | Kein Weg zurück aus `archived`: MCP und REST antworten 422. Der Editor bietet `archived` trotzdem in der Status-Auswahl an und öffnet eigene archivierte Items editierbar, jedes Speichern scheitert. | R (API) / C (UI) |
| B17 | niedrig | `mcpserver/__init__.py:1`; `webui/static/app.html:25` | `/health` meldet `version: 0.1.0`, die UI `v4.0.0`, der Health-Gate liest die HTML-Zeichenkette. Zwei Versionsquellen. | R |
| B18 | niedrig | `README.md:145` | „Fährt die sechs Tools einmal komplett durch“: es sind elf Tools, der Smoke prüft 17 Punkte. | C |
| B19 | niedrig | `storage/history.py:15`; `files.py:412` | Die `.gitignore` des `DATA_ROOT` ignoriert die tmp-Dateien von `atomic_write` nicht. Nach einem harten Kill committet der nächste `git add -A` verwaiste tmp-Dateien. | C |
| B20 | niedrig | `storage/frontmatter.py:15` | CRLF-Dateien sind kein gültiges Frontmatter. Zusammen mit B3 ein Startblocker. | R |
| B21 | niedrig | `authserver/store.py:328`; `routes.py` (`GET /oauth/authorize`) | Jeder unauthentifizierte Authorize-Aufruf mit registrierter `client_id` legt eine `auth_requests`-Zeile mit frei gewähltem `state`/`code_challenge` an. Purge nur täglich, kein Limit je Client oder IP. | V |
| B22 | niedrig | `history.py` (`commit`) | `rename_folder` eines leeren Ordners hat für Git nichts zu committen. `git commit` schlägt fehl und erzeugt eine falsche CRITICAL-Logzeile. | C |

Messwerte zu B12 (Wegwerf-Instanz, 1500 Items mit 400-Byte-Bodies):

| Aufruf | Dauer |
|---|---|
| `search(limit=20)` | 916 ms |
| `search(query=…)` | 872 ms |
| `list_spaces()` | 13 ms |
| Git-Commit je Write, 2 wie 1500 Dateien | 85 bis 105 ms |

## Die Befunde im Einzelnen

**B1, kritisch.** `get_asset` und `delete_asset` bauen `target_dir.glob(f"{asset_id}.*")`, und `pathlib` behandelt `..` als normales Segment. Reproduziert als `alice` mit einem eigenen Item und ohne Leserecht auf `bob`, dessen `get_item` korrekt `write_denied` liefert:
- `get_item_asset(asset_id="../../../bob/itm_…__bob-geheim")` liefert ein `Image` mit Bobs vollständigem Dateitext.
- `../../../bob/.share` liefert Bobs `.share.yml`. `../../../../auth` liefert die WAL-Datei der Auth-Datenbank.
- `delete_asset("../../../bob/.share")` verschiebt Bobs `.share.yml` in Alices Asset-Papierkorb. Bobs Freigaben sind weg, der Vorgang wird als `asset_trash` committet.
- Produktiv liegt die Auth-DB im `StateDirectory` desselben Dienstnutzers. Lesbar ist sie damit sicher. Verschiebbar ist sie, wenn `/var/lib` und `DATA_ROOT` auf demselben Dateisystem liegen. Das habe ich nicht geprüft, nur am Code belegt.
- REST ist nur begrenzt betroffen. Starlette dekodiert vor dem Routing, der Pfadparameter kann kein `/` tragen, geprüft: 404. Wildcards gehen, siehe B15.
- Fix: `ASSET_ID_RE` in beiden Store-Methoden erzwingen und den Pfad konstruieren statt zu globben. Zusätzlich im Tool und in der Route validieren.

**B2, hoch.** `PATCH /api/v1/spaces/alice/folders {"from":"projekte","to":"archiv/projekte"}` bei fehlendem `archiv/`. `os.rename` wirft, die Route fängt nur `ValidationError` und `ValueError` und antwortet 500, der Marker bleibt. Jeder folgende `Store()`-Aufruf läuft in der Wiederaufnahme in denselben Fehler. Unter systemd mit `Restart=on-failure` ist das eine Crash-Schleife, bis jemand den Marker auf der VM löscht. Auslöser ist ein einziger legitimer Klick eines Space-Verwalters, verschachtelte Zielnamen sind erlaubt. Fix: Elternverzeichnis vor dem Rename anlegen oder ein fehlendes als `ValidationError` ablehnen. Die Wiederaufnahme beim Start darf den Start nie verhindern.

**B3, hoch.** `rebuild_index` committet den `DELETE` beim ersten Links-Commit und bricht beim ersten `FrontmatterError` oder `KeyError` ab. Reproduziert mit `alice/README.md`: null von drei Items indiziert, `get()` liefert `ItemNotFound`, Neustart mit frischem Index wirft aus `Store.__init__`. Ein Neuaufbau passiert bei jedem Schema-Sprung im Deploy, bei korruptem Index, bei der Rename-Wiederaufnahme und bei `space_cli reindex`. Die Phase-1-Mission erlaubt dem Menschen ausdrücklich, im Verzeichnis zu arbeiten. Fix: je Datei fangen und `logger.critical`, wie `_rewrite_space_frontmatter` es bereits tut, und den Neuaufbau in einer Transaktion halten.

**B4, hoch.** Bob gewährt Alice `write:` auf seinen Home-Space. Reproduziert: Alice legt über die Mitglieder-Route „mallory“ mit Schreibrecht an (200, `.share.yml` enthält danach `mallory`), entfernt Mitglieder (200), die Mitgliederabfrage meldet `manageable: true`. Dieselbe Alice darf dort weder Ordner anlegen noch Items löschen, beides 403 nach P10-I und P9-K. Ein Gast ändert damit die Rechteliste des Eigentümers, die Re-Auth ist nur die eigene. Fix: `manages_space` statt `can_write` in beiden Routen.

**B5, hoch.** `_item_from_text` übernimmt Frontmatter-Werte ohne Typkoerzion, und die Suche verkettet Tags als Strings. Reproduziert dreifach: Hand-Edit `tags: [2026]` bricht `search(query)` mit `TypeError`. `POST /api/v1/items {"tags":[1,2]}` wird mit 201 angenommen, danach liefert die Web-Suche 500 und `search_items(query=…)` einen Fehler. Hand-Edit `title: 2026` bricht jedes Update mit `AttributeError`. Ein einziges Item blockiert die Suche für beide Nutzer und beide Flächen. Fix: im Kern koerzieren oder mit Dateipfad im Log ablehnen, in REST die Typen prüfen wie der MCP-Adapter über pydantic.

**B6, mittel.** `create_item(space="team/")` als Team-Mitglied: `can_write` liest `team//.share.yml` und sagt ja. Quittung `space: team/`, Frontmatter `team/`, Index `team`, `get_item_meta own: false`, der eigene Body kommt gewrappt zurück. Dasselbe über REST und über `update_item(space=…)`. Folgeschaden: das Space-Umbenennen überspringt die Datei, die Indexzeile zeigt danach ins Leere. Fix: eine Validierung für Space-Namen im Store oder an beiden Adaptern.

**B7, mittel.** Reproduziert: 200 Umlaute im Titel geben `OSError 36`, REST 500, MCP `internal_error`. 100 CJK-Zeichen im Update: Datei an alter Stelle neu geschrieben mit neuem Titel und Version 2, Umbenennen scheitert, Dateiname bleibt `…__kurz.md`, kein Commit. Fix: Slug kürzen, Titel-Höchstlänge prüfen, `OSError` sauber abbilden.

**B8, mittel.** Reproduziert: `title:123` gibt 500 vor dem Write. `folder:123` gibt 500 in `validate_folder`, der POST-Pfad hat dafür schon einen Fix, der PATCH-Pfad nicht. `body:5` läuft durch `atomic_write` und `upsert_item`, erst die Link-Extraktion wirft, kein Git-Commit, der Client bekommt 500, das Item steht aber auf Version 2. Der folgende PATCH mit Version 1 lieferte 409. Fix: Typen in beiden Routen prüfen und die Link-Extraktion vor dem Schreiben rechnen, damit ein Fehler nie nach dem Write kommt.

**B9, mittel.** Reproduziert über den ASGI-Wrapper: `GET /ui/invite/Qm9z…` erscheint vollständig in der `ev="http"`-Zeile. Das Token ist ein Einmal-Geheimnis mit Stunden Gültigkeit. Wer das Journal lesen kann, löst die Einladung ein. Fix: Invite-Pfad in die Redaktion und in `_SECRET_PATTERNS` aufnehmen.

**B10, mittel.** Reproduziert mit drei Such-Threads gegen 300 Titeländerungen: `FileNotFoundError` im Leser. Fix: fehlende Datei je Zeile überspringen oder das Lock über den Lesevorgang halten.

**B11 und B12, mittel.** B11 ist nur am Code belegt. Zu B12: `list_spaces` ruft `store.search(limit=5000)` nur zum Zählen von `visibility: human`, die REST-Liste je Seite einen Vollscan. Der Git-Commit je Write läuft in den REST-Schreibrouten synchron auf dem Event-Loop. Für heute rund 200 Items unkritisch, aber linear wachsend.

**B13 bis B22, niedrig.** Zu B13: die Reproduktion erzwang die Kollision per Monkeypatch. Zu B16: der Editor baut die Status-Auswahl aus allen Statuswerten des Typs inklusive `archived` und sendet `status` im PATCH. Ob ein eigenes archiviertes Item im Browser tatsächlich editierbar erscheint, ist nicht im Browser geprüft, nur am Code: `readonly` ist ACL-basiert, nicht statusbasiert. Zu B21: nicht gemessen.

## Kategorien ohne Befund, mit Prüfumfang

- **Korrektheit, Grenzfälle:** Zeitstempel durchgehend UTC, Übergangsfenster bewusst Ortszeit Berlin, Deploy-Gate akzeptiert UTC und lokal. Frontmatter-Roundtrip mit `---` im Titel und Unicode geprüft, korrekt. `apply_edits` ist alles-oder-nichts. Sortierung stabil. Gleitkomma nur beim mtime-Vergleich aus derselben Quelle. Die Grenzfall-Treffer stehen oben.
- **Datenintegrität:** alle neun Store-Schreibmethoden tragen `version` oder sind bewusst versionsfrei (Assets, dokumentiert). Kein Last-Write-Wins in MCP oder REST. `atomic_write` macht tmp, fsync, replace und Verzeichnis-fsync, `move_file` fsynct Quelle und Ziel. Ein Commit je Write. Pfad und Ordner immer aus dem Dateipfad abgeleitet. Space-Rename idempotent und markergesichert.
- **Sicherheit, OAuth und Login:** PKCE nur S256, Redirect byteweise gegen Registrierung plus Allowlist, Loopback nur `127.0.0.1` mit Port, Code einmalig mit Familien-Widerruf bei Replay, Refresh-Rotation mit Replay-Erkennung und Client-Prüfung, `resource` und `scope` beim Zugriff geprüft, TOTP mit Replay-Zähler nur nach vollem Erfolg, Recovery-Codes nur bei richtigem Passwort verbraucht, Argon2id-Dummy gegen Enumeration, Sperre je Space, Reset widerruft Familien und Sitzungen, `disabled` in beiden Login-Wegen geprüft.
- **Sicherheit, Sitzungen und Header:** `__Host-`-Cookie Secure, HttpOnly, SameSite=Strict, Rotation beim Login, Double-Submit plus Origin-Prüfung, Re-Auth vor jeder Rechteerweiterung inklusive Ordnerwechsel, CSP ohne `unsafe-inline` und keine Inline-Styles, statische Pfade gegen Traversal gesichert, `/mcp` ohne Cookies, `/api` ohne Bearer.
- **Prompt-Injection:** fremde Bodies und Snippets werden gewrappt, das Closing-Tag wird entschärft, Metadaten bleiben außerhalb. REST rendert nie serverseitig. Der Client-Sanitizer arbeitet mit Whitelists für Tags, Attribute und Klassen, `href` nur `http(s)`, `mailto` und `#item/`, `img src` nur die eigene Asset-Route, kein `data:`. Bildbytes aus fremden Spaces nur bei Schreibrecht.
- **Secrets:** repo-weit keine echten Hashes, Seeds, Schlüssel oder Tokens, nur Platzhalter in Tests und Plan. Logging mit Feld-Whitelist und Scrubbing, Access-Log aus. Einziger Treffer ist B9.
- **Abhängigkeiten:** alle transitiven Versionen gepinnt, ein Wächter vergleicht die Installation. Nicht geprüft: Prüfsummen der vendored CodeMirror-Dateien und der CVE-Stand der Pins.
- **API- und Protokollverträge:** Tool-Schemas über pydantic, Fehlerpräfixe stabil, 401 mit `WWW-Authenticate` und Resource-Metadata, `/mcp` mit und ohne Slash, beide Protokoll-Ären bedient und geloggt. REST-Fehlerform mit elf Codes stabil, JSON-404 im API-Präfix. Index-Schema 4 seit v3.1 unverändert, Update-Log-IDs zählen von unten (einmaliges erneutes Anzeigen eines alten Blocks ist dokumentiert), Graph-Layout je eigenem Space mit Versionsfeld.
- **Performance:** Re-Auth-Grants und Event-Streams begrenzt, die Graph-Schleife bricht den Vorgänger ab, kein Timer-Leck. Offen nur B12. Papierkorb und Asset-Historie wachsen unbegrenzt, das ist als V162 bereits benannt.
- **Frontend:** 401 führt zur Sitzungs-Karte, Fehler zu Toasts, Konflikt in den Konfliktdialog, Entwurfsschutz, SSE mit Poll-Rückfall. 33 `aria-label`, zwei `aria-live`-Regionen, `focus-visible`, `prefers-reduced-motion` in CSS und JS. Kein Browserlauf in dieser Sitzung, Sichtprüfung nicht durchgeführt.
- **Betrieb:** Release-Verzeichnis, eigenes venv, Tests im Release, atomarer Symlink-Tausch, Health-Gate mit Auth-Proben und Auto-Rollback, `.failed`-Markierung, minimaler Rollback, verifizierte Git-Bundles mit Restore-Check, verschlüsseltes Auth-Backup mit Rücklese-Prüfung, gehärtete Units, persistente Timer, ratenbegrenzter Watchdog. Nicht live prüfbar hier. Die Backup-Skripte brauchen das `sqlite3`-CLI auf der VM.
- **Tests:** 1659 gesammelt, ohne Netz, ohne echte Daten. Gegenläufe stichprobenartig vorhanden. Ungetestet sind genau die Flächen von B1, B2, B3, B5 und B9.
- **Architektur:** keine LLM-Aufrufe, keine Inhaltsdeutung, keine Embeddings. Dubletten sind dokumentiert und bewusst. Kleine Drift: der Docstring von `_write_item_file` zählt `archive()` zu seinen Aufrufern, `archive()` hat aber einen eigenen Schreibpfad, ohne Folgen.
- **Dokumentation:** Hard Rules und Phasen-Köpfe stimmen mit dem Code überein, `docs/INDEX.md` unter dem Softcap, Update-Log-Format eingehalten. Abweichungen nur B17 und B18.

## Empfohlene Reihenfolge vor Deploy D

1. B1: Validierung der `asset_id`, zwei Zeilen im Store plus Tests.
2. B2 und B3: der Dienststart darf nie an Daten scheitern.
3. B5 und B8: Typkoerzion im Kern, Typprüfung in REST.
4. B4: `manages_space` in den Mitglieder-Routen.
5. B6, B7, B9, B10 im selben Schnitt, der Rest als Backlog.

Die Wegwerf-Daten und Probeskripte liegen im Scratchpad, nichts davon ist im Repo, es wurde kein Commit gemacht.
