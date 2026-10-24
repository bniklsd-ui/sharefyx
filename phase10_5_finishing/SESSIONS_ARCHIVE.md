---
status: archive
purpose: L3-Archiv der älteren Session-Blöcke des Phase-10.5-Heads — verbatim, newest-first
read-when: beim Audit, wenn der Stand eines früheren Blocks dieser Phase gebraucht wird
detail: L3
up: ./CLAUDE.md
down:
updated: 2026-10-24 (Session-Block Block 11.2 rotiert — der Nachlader; Block 11.3 folgt im Head) | 2026-10-24 (Session-Block Block 11.1 rotiert — der vendorte Editor; Block 11.2 folgt im Head) | 2026-10-24 (Session-Block Block 10.5 rotiert — die Probe ist grün; Block 11.1 folgt im Head) | 2026-10-24 (Session-Block Block 10.3 rotiert — LG-2 Realtime-Client gebaut; Block 10.5 folgt im Head) | 2026-10-24 (Session-Block Block 10.2 rotiert — LG-2 Realtime serverseitig gebaut; Block 10.3 LG-2 Client folgt im Head) | 2026-10-24 (Session-Block Block 10.1 rotiert — LG-1 Volltext gebaut; Block 10.2 LG-2 Realtime serverseitig folgt im Head) | 2026-10-24 (Session-Block Block 9.3 rotiert — RE-3 `rename_space` gebaut und gemessen; Block 10.1 LG-1 Volltext folgt im Head) | 2026-10-24 (Session-Block Block 9.2 rotiert — RE-4 `rename_folder` gebaut und gemessen) | 2026-10-24 (Session-Block Block 9.1 rotiert — RE-7 `created_by` gebaut und gemessen; Block 9.2 `rename_folder` folgt im Head) | 2026-10-24 (Session-Block Deploy C vorbereitet rotiert — Block 9.1 RE-7 `created_by` gebaut und gemessen) | 2026-10-24 (Session-Block Block 8 rotiert — Deploy C `v3.1.7` vorbereitet: Badge, eigener Update-Log-Block, Suite 1425 grün) | 2026-10-24 (Session-Block 7.4 rotiert — Block 8 gebaut: die Gehirnkarte C2; drei Fehler fand erst der Browser) | 2026-10-24 (Session-Block 7.5-7.7 rotiert — Block 7.4 umgesetzt: die vier Posten der Sichtung gebaut und an der Wegwerf-Instanz gemessen; P10.5-32 wartet auf die Bestätigung) | 2026-10-24 (Session-Block Deploy B live und Block 7.1–7.3 rotiert) | 2026-10-23 (Generalprobe-Block rotiert — Ketten-Defekt in derselben Zeile behoben: `pdated:` → ` | `) | 2026-10-23 (Deploy-B-Generalprobe-Block rotiert — 25/25 Zellen an der Wegwerf-Instanz) | 2026-10-23 (Deploy-A-live-Block rotiert — Deploy B `v3.1.6` vorbereitet) | 2026-10-23 (Deploy-A-Vorbereitungs-Block und P10.5-26-Block rotiert — Deploy A live, Merge von `p105-block5`) | 2026-10-23 (Block-6-Block rotiert — P10.5-26 geklärt: opencode führt `list_spaces` aus) | 2026-10-22 (Block-5-Block rotiert — Block 6 gebaut: Anbieter PA-1/PA-2, `/mcp` ohne Slash, PA-6) | 2026-10-22 (Block-4-Block rotiert — Block 5 begonnen: MCP-Schicht PA-5/LG-4) | 2026-10-22 (Block-3-Block rotiert — Block 4 begonnen: Performance PF-1/PF-4, Z1–Z4) | 2026-10-22 (Block-2.5-Block rotiert — Block-2-Nachzug + Block 3 begonnen) | 2026-10-22 (Block-2-Block (2.1–2.4) rotiert — Block 2.5 Proben) | 2026-10-22 (Block-1-Block rotiert — Block 2 begonnen) | 2026-10-22 (Block 1, Schritt 1.3: erster Block rotiert — der Block-0-Block vom 2026-10-22, verbatim) | 2026-10-22 (angelegt — P10.5 Block 0, Schritt 0.2; noch kein Block rotiert, der erste steht im Head)
---
# Phase 10.5 — Session-Archiv

Hier stehen die älteren `## Session stopped`-Blöcke des Phase-10.5-Heads, **verbatim** und
newest-first — der neueste Block steht im Head (`../CLAUDE.md`), dieser Abschnitt trägt die Chronik.

**Warum es ein Archiv gibt:** die Doc-Layers-Konvention verlangt genau **einen** Session-Block pro
Phase-Head (Rotationsregel ab Tag 1, `scripts/rotate_session_block.sh`). Wer einen älteren Block
sucht, findet ihn hier — nicht im Head.

**Größe:** jeder Block ist auf **4 KiB** begrenzt (Lock P10.5-T, DO-3), geprüft von
`phase10_5_finishing/tests/test_head_rules.py`. Das ist die Lehre aus Phase 9: die alten Blöcke
trugen 10–17 KB, das P9-Archiv wuchs auf 396 KB — der teuerste Abschnitt einer Datei, den jede
Lesesitzung zuerst liest.

## Session stopped — 2026-10-24 (Block 11.2: der Nachlader — CSS, dann der Kern, dann die Modus-Dateien)

**Ergebnis.** `static/js/editor_cm.js` (neu) lädt den Editor **nach**: erst das CSS, dann
`codemirror.min.js`, dann `meta.min.js`, `xml.min.js` und zuletzt `markdown.min.js`. Das
Promise wird **gecacht** (ein zweiter Aufruf wartet auf dasselbe Laden), und ein Fehler
löst mit `null` auf — **der Editor bleibt dann die Textarea**, also der Rohmodus (ED-5).
Ein Wurf nach oben wäre die falsche Richtung: der Editor ist ein Komfort, kein Pfad.

**Sechs Wächter** (`tests/test_editor_cm.py`), darunter der wichtigste: die Dateiliste des
Laders muss **exakt** den Dateien im Verzeichnis `static/vendor/codemirror/` entsprechen —
ein Vendor-File, das der Lader nicht kennt, wäre sonst ein stiller Fehler (der Editor liefe
ohne den Modus, und nichts würde rot). Zusammen mit dem SHA-Wächter aus 11.1 ist der
Vendor-Pfad jetzt von beiden Seiten geschlossen.

**Was noch nicht gebaut ist.** Der Editor selbst: `editor.js` wird auf `getBody()`/`setBody()`
umgestellt (ohne Moduswechsel, ED-1), die Live-Darstellung (11.4), ED-2 (To-do-Kästchen),
ED-3 (Stufe 2), das Budget (11.7) und der Roundtrip (11.8).

Suite **1513 grün** (345,0 s), `doc_health` 0.

**Nächster Schritt.** 11.3: `editor.js` — alle Zugriffe auf `editorTextareaEl.value` gehen
über `getBody()`/`setBody(text)` (CM vorhanden → `cm.getValue()`/`cm.setValue()`, sonst
Textarea); `setEditorMode` wird `setRawMode(on)`, der Knopf heißt „Rohtext", und beim Öffnen
ist der **Live**-Modus die Vorgabe.

## Session stopped — 2026-10-24 (Block 11.1: der vendorte Editor — **fünf** Dateien, nicht drei)

**Ergebnis.** `phase5_ui/webui/static/vendor/codemirror/` liegt im Baum: CodeMirror **5.65.16**
(von jsDelivr), die SHA-256-Summe jeder Datei und der MIT-Lizenztext in
`phase5_ui/THIRD_PARTY_LICENSES.md`. **71.280 B gzip** — das Budget „Editor nachgeladen ≤ 80 KB"
(P10.5-50) hält mit 8,7 KB Luft. Ein Wächter (`tests/test_codemirror_vendor.py`, 4 Tests)
vergleicht den Baum mit dem Lizenzdokument — **mit Gegenprobe**: ein untergeschobener
CodeMirror (gleichlang, gleicher Name) muss rot werden, sonst prüft der Wächter ins Leere.
Suite **1507 grün** (351,1 s), `doc_health` 0.

**Der Plan nennt drei Dateien, gemessen sind es fünf.** Die gebaute `markdown.min.js` ist ein
**UMD-Wrapper**; im Browser-Zweig ruft sie nur `t(CodeMirror)` auf — die beiden `require(...)`
Zweige (`require("../xml/xml")`, `require("../meta")`) werden **nicht** abgearbeitet. Im echten
Chromium gemessen: mit den drei Dateien registriert sich der Modus zwar
(`CodeMirror.modes.markdown` ist eine Funktion, **null** Seitenfehler), aber der HTML/XML-Teil
des Markdown-Modus fehlt — `xml.min.js` ist **kein** Zusatz, sondern die fehlende Hälfte.
Mit allen fünf Dateien bleibt das Verhalten identisch und vollständig. Der Zuschlag beträgt
**6.499 B gzip** und ist damit im Budget.

**Was noch nicht gebaut ist.** Der Editor selbst: `js/editor_cm.js` (Nachladen), der Umbau von
`editor.js` auf `getBody()`/`setBody()` (ohne Moduswechsel), die Live-Darstellung, ED-2
(To-do-Kästchen), ED-3 (Stufe 2), das Budget und der Roundtrip (11.2–11.8).

**Nächster Schritt.** 11.2: `js/editor_cm.js` — die CSS und dann beide Skripte laden, das
Promise gecacht, bei einem Fehler `null` (der Editor bleibt Textarea = Rohmodus, ED-5).

## Session stopped — 2026-10-24 (Block 10.5: die Probe ist grün — Volltext, Latenz, P10.5-S und Shutdown an der Wegwerf-Instanz)

**Ergebnis.** Die Probe `probes/p105_b10_realtime_probe.py` fährt gegen die Wegwerf-Instanz
(Port 18810, TLS, eigene PID-Datei) und misst **11 von 11 Zellen grün**: Volltext **0 → 1
Treffer** mit dem Schalter · das Ereignis kommt an · **Latenz 141,1 ms** (Grenze 2000) · der
getippte Text bleibt stehen, das Band erscheint · ein unsichtbarer Space löst **kein** Ereignis
aus · **Shutdown 5,22 s** (Grenze 10). Der **Gegenlauf** (Ereignis-Filter in `api.py` aus) ist
**rot** — genau an der Zelle, die er brechen soll. Belege: `p105_b10_realtime.json` (grün),
`p105_b10_realtime_gegenlauf.json` (rot). **Abnahme P10.5-45, 46, 47, 48 ✅** — Block 10 ist
fertig.

**Vier Fehler lagen im Messgerät, nicht im Produkt** (jeder hätte die Probe rot gemeldet, ohne
den Defekt zu zeigen): (1) Das Flag-Protokoll war verdreht — der Browser wartete auf
`ready.flag`, das er selbst schreiben sollte. (2) Der **CSRF-Origin** passte nicht:
`require_csrf()` vergleicht ihn gegen `SPACE_PUBLIC_BASE_URL`, die Auth-Konfiguration erzwingt
https ⇒ die Wegwerf-Instanz braucht **TLS** (derselbe Weg wie `p10_wegwerf.py`). (3) Der Editor
öffnet in der **Vorschau** (die Textarea ist unsichtbar), und die Zeile in der Liste zeigt den
**Titel**, nicht den Text. (4) Die Shutdown-Messung sah einen **Zombie** (ein beendeter
Prozess bleibt in `/proc`); die erste Fassung meldete 30,03 s.

**Eine Frage an die Attrappe.** Die erste Fassung der Probe startete eine **Kopie** des
App-Aufbaus — damit hätte sie die Frist `timeout_graceful_shutdown=5` mitkopiert oder
weggelassen; weggelassen hätte die Probe **grün** gemeldet, obwohl der Produktivpfad
unbegrenzt auf offene Streams wartet. Die Probe startet jetzt **den Produktiv-Code**
(`phase2_mcp/scripts/serve.py`) und ergänzt nur die beiden TLS-Parameter. Der Write läuft über
die **Web-API**, nicht über MCP (der Plan nennt einen MCP-Write) — nach dem Adapter ist der
Serverpfad derselbe (datierte Abweichung, im Probekopf benannt).

**Gemessen.** 38 neue Tests (2 API + 6 Volltext-Wächter + 15 Events + 2 `phase2_mcp` + 8
Client-Wächter + 5 Probe-Wächter) · Suite **1503 grün** (350,8 s) · `doc_health` 0 ·
`ui_budget` 5/5 (198,7 KB gzip). Der Abschnitt „Freigaben" ist aus dem Head nach
`FREIGABEN_ARCHIVE.md` gewandert (verbatim) — der Head stand bei 41.343 B, über dem Softcap.

**Nächster Schritt.** Deploy C (`v3.1.7`) beim Nikinger (`deploy.sh`, Hard Rule 9) ·
`health_gate.sh` mit echter Ausgabe · Merge `p105-block9` → `main` · danach Block 11 (Editor).

## Session stopped — 2026-10-24 (Block 10.3 LG-2 Realtime-Client gebaut — der Editor wird nie überschrieben)

**Ergebnis.** Die Client-Hälfte steht: `static/js/realtime.js` (neu) öffnet den Ereignis-Stream,
`app.js` macht den 20-s-Poll zum **Rückfall** (120 s), `editor.js` bekommt das Hinweisband
(P10.5-S) und `app.html`/`app.css` die Strippe dazu.

**Drei Folgen eines Ereignisses.** (1) `List.loadOverview()` — Zähler und Übersicht; das setzt
auch `state.graphToken`, an dem die Karte hängt (P9-33), die Karte braucht keinen eigenen
Abruf. (2) `List.loadItems()` — **nur**, wenn der aktive Space betroffen ist; im globalen
Modus („Alle Items") immer. (3) Das **offene Item**.

**P10.5-S: ein geänderter Editor wird nie überschrieben.** Sauberer Editor → der
Serverstand wird geholt, und bei neuerer `version` neu geladen (**Inhalt und Version
zusammen** — sonst zeigte der Editor eine Version, die es nicht gibt). Geänderter Editor →
ein Hinweisband „Geändert von X — neu laden?"; der Mensch entscheidet, und das Speichern
läuft über die alte Version in den Konfliktdialog (Hard Rule 3).

**Eine datierte Korrektur an einem Kommentar.** `app.js` behauptete im Absatz über den
Zähler-Poll, das Polling sei „der einzige Weg der Zähler-Synchronisation" — seit diesem
Block trägt der Ereignis-Stream die Änderungen, der Poll ist der Rückfall. Der Kommentar
sagt das jetzt (datierte Korrektur, 2026-10-24).

**Gemessen.** 8 Verdrahtungs-Wächter in `phase10_5_finishing/tests/test_realtime_client.py`
(Markup, `EventSource`, die drei Folgen, „nie überschreiben", Poll-Rückfall) · `ui_budget`
**5/5** (Erstaufruf 198,7 KB gzip — `realtime.js` 1,5 KB) · JS-Syntax mit `node --check`
geprüft (alle fünf berührten Module) · Suite **1497 grün** (366,0 s).

**Ausführer-Daten.** `opencode/MiniMax-M3.1-Flash`, Kontextgrenze 400.000 (P10.5-C erfüllt),
keine Eingriffe des Nikingers in dieser Session.

**Stand.** Branch `p105-block9`. **P10.5-45/46/47/48 bleiben ⬜** — die Abnahme verlangt
Playwright bzw. die Wegwerf-Probe (10.5).

**Nächster Schritt.** (1) 10.5: die Probe an der Wegwerf-Instanz — Volltext, Änderung ≤ 2 s,
unsichtbarer Space, SIGTERM ≤ 10 s. (2) Danach Deploy C (`v3.1.7`) beim Nikinger, Merge,
dann Block 11 (Editor).

## Session stopped — 2026-10-24 (Block 10.2 LG-2 Realtime serverseitig gebaut — der Git-HEAD ist die Quelle)

**Ergebnis.** Die Server-Hälfte von Realtime steht: `phase5_ui/webui/events.py` (neu) mit
`read_git_head()`, `changed_spaces()` und `ChangeFeed`, die Route `GET /api/v1/events`
(SSE), der umhüllte Lifespan und `timeout_graceful_shutdown=5` in `serve.py`.

**Die Quelle ist der Git-HEAD, nicht ein Write-Hook.** Hard Rule 5 macht aus jedem
erfolgreichen Write einen Commit — „HEAD hat sich bewegt" heißt also genau „die Daten haben
sich geändert", für Web, MCP und Hand-Edit gleichermaßen. Ein Eingriff in
`Store.create()`/`update()`/`append()` wäre doppelt schlecht: er säße im `storage/`-Kern
(P10.5-F) und sähe eine Hand-Edit von außen nicht.

**Was der Server meldet: Space-Namen und ein Commit-Hash. Sonst nichts.** Kein Body, kein
Titel — der Client holt sich die Daten über die normale API, die ihre Rechte prüft. Jeder
Space-Name wird gegen `_visible_space_infos()` gefiltert: **ein unsichtbarer Space-Name
verlässt den Server nie.**

**Der Heartschlag** (alle 25 s) prüft die Sitzung neu; eine abgelaufene beendet den Stream.
**Höchstens drei Streams je Sitzung**, darüber 429 — gezählt über den Request-Task, damit ein
abgebrochener Client nicht als „belegt" zählt.

**Zwei Abweichungen vom 📕-Plan, datiert.** (1) `subscribe()` liefert ein Tupel
`(head, spaces)` statt `set[str]` — der Route sonst den Kopf des *nächsten* Ereignisses lesen
müsste (ein Rennen bei zwei schnellen Schreibvorgängen). (2) Der Feed wird **außerhalb** von
`api_routes()` gebaut und als **optionaler** siebter Parameter durchgereicht: die App muss
ihn beim Shutdown schließen, und die Route kann das nicht.

**Ein Fehler, den erst der Abbruch-Test fand.** `aclose()` auf einen Generator, in dem
gerade `__anext__()` läuft, ist ein `RuntimeError` — und genau das passiert, wenn der Client
abbricht. Gefixt: erst die wartende Aufgabe abbrechen, dann den Generator schließen.

**Gemessen.** 14 neue Tests in `phase5_ui/tests/test_events.py` (echtes tmp-Git, echter
`Store(git=True)`-Write, ASGI-Harness statt `httpx.ASGITransport` — der sammelt den ganzen
Body und käme bei einem endlosen Stream nie zurück) + 2 in `phase2_mcp` (Route in der echten
App, Feed-Schluss beim Shutdown, `timeout_graceful_shutdown`). **Sechs Gegenläufe rot:**
Sichtbarkeits-Filter, Stream-Grenze, Herzschlag-Prüfung, Papierkorb-Zuordnung, gepackte Refs,
Volltext-Parameter. Suite **1489 grün** (338,4 s).

**Ausführer-Daten.** `opencode/MiniMax-M3.1-Flash`, Kontextgrenze 400.000 (P10.5-C erfüllt),
keine Eingriffe des Nikingers in dieser Session.

**Stand.** Branch `p105-block9`. **P10.5-46/47/48 bleiben ⬜** — sie verlangen den Client
(10.3) und die Wegwerf-Proben (10.5).

**Nächster Schritt.** (1) 10.3 Client: `realtime.js`, Poll-Rückfall 120 s, Hinweisband
(P10.5-S). (2) 10.5 Proben: ≤ 2 s bis zur Änderung, unsichtbarer Space, SIGTERM ≤ 10 s.

## Session stopped — 2026-10-24 (Block 10.1 LG-1 Volltext gebaut — die Suche erreicht jetzt auch den Text)

**Ergebnis.** Block 10.1 steht: die Web-UI kann jetzt **im Text** der Notizen und Aufgaben
suchen. Der Schalter „Volltext" sitzt links am Suchfeld; ohne ihn sucht die Liste wie bisher
nur Titel und Tags, mit ihm kommt der Body dazu — auf der Agentenfläche war das seit
P6.5-N4 (`search_items(in_body=True)`) möglich, auf der Web-Fläche gab es diese Möglichkeit
nie (Register LG-1).

**Was der Server daraus macht.** `api.py :: _items_get()` liest den Query-Parameter `in_body`
als **Wahrheitswert** (`_parse_bool`: `1`/`true`/`yes`/`on`, sonst aus) und reicht ihn an
`store.search(..., in_body=True)` durch. Bewusst kein `bool(value)` — `in_body=0` ist „aus",
ein fehlender Parameter ist „aus". Die **ACL-Filterung bleibt unverändert** danach: gefunden
wird nur, was die Sitzung lesen darf (Hard Rule 4) — der Volltext ist eine Suchart, keine
Rechteausnahme.

**Gemessen.** 2 API-Tests (`test_items_query_in_body_only_when_requested`,
`test_in_body_search_never_returns_unreadable_items`) gegen den echten Store + 6
Verdrahtungs-Wächter in `phase10_5_finishing/tests/test_fulltext.py` (Markup, Zustand,
Parameter, globaler Modus, Server). **Gegenlauf:** `in_body=in_body` aus `api.py` entfernt
und `params.set("in_body", "1")` aus `list.js` entfernt ⇒ **3 Tests rot** (der API-Test und
zwei Wächter) — die Wächter prüfen etwas anderes als sie behaupten.

**Eine Design-Entscheidung, die der Plan nicht vorgibt.** Der Parameter gehört **nicht** in
`filterParams()` (das ist der Raum der Filter: Bucket/Ordner/Zugewiesen), sondern direkt in
`loadItems()` — der Volltext ist eine *Suchart* und gilt im globalen Modus („Alle Items")
genauso wie im Space-Modus. Ein Wächter prüft genau das (`in_body` darf nicht an
`isGlobalScope()` hängen).

**Ausführer-Daten.** `opencode/MiniMax-M3.1-Flash`, Kontextgrenze 400.000 (P10.5-C erfüllt),
keine Eingriffe des Nikingers in dieser Session.

**Stand.** Branch `p105-block9` (Block 10 läuft darauf weiter), Suite grün auf den berührten
Dateien. **P10.5-45 bleibt ⬜** — die Abnahme verlangt Tests **und** Playwright; die Probe
kommt mit Schritt 10.5.

**Nächster Schritt.** (1) 10.2 LG-2 Realtime serverseitig (`webui/events.py`, Route
`GET /api/v1/events`, Lifespan, `timeout_graceful_shutdown`). (2) 10.3 Client
(`realtime.js`, Poll-Rückfall 120 s, Hinweisband P10.5-S). (3) 10.5 Proben.

## Session stopped — 2026-10-24 (Block 9.3 RE-3 `rename_space` gebaut und gemessen)

**Ergebnis.** Block 9.3 steht: `Store.rename_space(old, new, *, actor="") -> int` im Kern, die
Web-Route `PATCH /api/v1/spaces/{space}` und der Knopf „Space umbenennen" im Space-Detail-Panel
mit eigenem Dialog. **Damit ist Block 9 vollständig gebaut** — RE-7, RE-4 und RE-3 sind alle drei
gemessen.

**Was der Kern tut (anders als beim Ordner, RE-4).** Der Space-Name steht **im Frontmatter**
jeder Item-Datei — er ist keine abgeleitete Größe. Verzeichnis und Frontmatter dürfen nie
auseinanderlaufen (B2-Schutz), also gilt die Semantik von `move()`: jedes Item bekommt
`space=new`, `version+1`, `updated=now`, `updated_by=actor` (oder den bisherigen Wert). Der
Ablauf: Name validieren (dieselbe Regel wie `acl.create_space()`) → **Marker** → `os.rename`
+ `fsync` → jede Item-Datei unter `new/` (inkl. `_archive/`) atomar umschreiben, **ohne**
Einzel-Commit → `._trash/old` → `._trash/new` (Dateien dort **unverändert**: Historie) →
Index-Zeilen aus den **Dateien** neu gelesen → **ein** Commit `rename-space <old>→<new>` →
Marker löschen.

**Gemessen.** Wegwerf-Probe `probes/p105_b9_rename_space_probe.py` **15/15 Zellen** (Port 8799,
PID-Datei): HTTP 200 mit `from`/`to`/`items` · das Verzeichnis steht unter dem neuen Namen · das
Frontmatter nennt ihn · die Version springt **genau einmal** (1 → 2) · **ein** Commit
`rename-space team→team-neu` · der Index stimmt · **Fremdverweise werden gemeldet, nicht
angefasst** (`orphan_refs` + `assignee_refs`; die fremde `.share.yml` bleibt, wie sie ist) ·
**Gegenläufe**: Home-Space → **403**, vergebener Zielname → **422**, jeweils nichts bewegt. Der
**Absturz** trägt `test_rename_resumes_after_crash`: ein Monkeypatch wirft nach der ersten Datei,
ein neuer `Store` führt den Rename zu Ende — konsistenter Endzustand, Marker weg, und die
bereits umgeschriebene Datei bekommt **keinen** zweiten Versionssprung (die Idempotenz).
11 neue Tests (`test_store.py` × 5, `test_api.py` × 5, `test_static_routes.py` × 2).

**Fremdverweise: gemeldet, nicht repariert.** Eine fremde `.share.yml`, die den alten Namen
nennt, und Items mit `assignee == <alter Name>` bleiben, wie sie sind. Sie zu „reparieren" wäre
eine **stille Rechteänderung** — sie stehen deshalb in der Antwort, damit der Mensch sie kennt.

**Nur Team-Spaces (P10.5-M).** Ein Home-Space trägt den Namen seines Principals; die Auth-DB
kennt ihn unter diesem Namen. Ein Umbenennen würde Verzeichnis und Auth-DB trennen — der
Server lehnt es ab (403), der Knopf wird gar nicht erst angeboten.

**Ein Drift gegen den Plan, datiert.** Der Plan listet
`test_rename_space_reports_foreign_references_without_touching_them` bei den **Storage**-Tests;
der Test liegt in `phase5_ui/tests/test_api.py` — das Melden passiert in der **Antwort der
Web-Fläche** (wie `orphan_refs` beim Space-Entfernen), und `acl.spaces_referencing()` ist keine
Kern-Aufgabe des Stores. Nachtrag in Plan §9.5.

**P10.5-44 ✅.** `git diff --stat 2c841cf -- phase1_storage/storage` nennt **nur** `models.py`
und `store.py` — beide angekündigt, `index.py` unberührt (kein Schema-Sprung).

**Ausführer-Daten.** `opencode/MiniMax-M3.1-Flash`, Kontextgrenze **400.000** (P10.5-C
erfüllt), keine Eingriffe des Nikingers in dieser Session.

**Stand.** Branch `p105-block9`, Wegwerf-Instanz gestoppt und aufgeräumt. Suite **1465 grün**
(343,7 s), `doc_health` 0, `ui_budget` 5/5. **P10.5-37 und P10.5-32 bleiben ⬜** (Augen-Urteil);
das **Budget für `graph.js`** entscheidet der Nikinger.

**Nächster Schritt.** (1) Deploy C (`v3.1.7`) durch den Nikinger, dann `health_gate.sh` mit
echter Ausgabe in den Commit. (2) Merge `p105-block9` → `main` **nach** dem Deploy.

## Session stopped — 2026-10-24 (Block 9.2 RE-4 `rename_folder` gebaut und gemessen)

**Ergebnis.** Block 9.2 steht: `Store.rename_folder(space, old, new, *, actor="") -> int` im
Kern, die Web-Route `PATCH /api/v1/spaces/{space}/folders` und die Kontextaktion „Umbenennen"
am Ordner im Baum (Rechtsklick → ein Menü mit einem Eintrag). **RE-4 ist damit im Kern
geschlossen** — die billige Frontend-Fassung, die die `.share.yml` eines geteilten Ordners
zurückließ, gibt es nicht mehr: die Freigabe wandert mit dem Verzeichnis.

**Was der Kern tut.** Die Ordner stehen **nicht** im Frontmatter (der Pfad wird abgeleitet) —
deshalb wird **keine** Item-Datei umgeschrieben und **keine** Version angehoben. Ablauf unter
beiden Locks: beide Namen über `files.validate_folder()` → `old` muss existieren, `new` darf
nicht existieren, `new` darf nicht unter `old` liegen → **Marker** (`DATA_ROOT/
.rename-pending.json`, 9.4) → `os.rename` + `fsync` des Elternverzeichnisses → Index-Zeilen
(`folder`, `path`) nachziehen → **ein** Commit `rename-folder <space>:<old>→<new>` → Marker
löschen. Rückgabe: die Zahl der betroffenen Items.

**Gemessen.** Wegwerf-Probe `probes/p105_b9_rename_folder_probe.py` **13/13 Zellen** (Port
8799, PID-Datei, Stopp nur über die PID-Datei): HTTP 200 und `items == 1` · die Datei liegt am
**neuen** Pfad, der alte Ordner ist weg · `version:` **1 → 1** · die `.share.yml` wandert mit ·
**ein** Commit `rename-folder alpha:projekte→vorhaben` · der Index meldet `folder ==
"vorhaben"` · **Gegenlauf**: Ziel existiert → **422** und **nichts** bewegt · Ziel unter dem
alten Ordner → 422 · ohne CSRF → **403**, nichts bewegt. 11 neue Tests (`test_store.py` × 5,
`test_api.py` × 4, `test_static_routes.py` × 2).

**Ein Fund beim Bauen — das Register stand an der Grenze.** Die Abhakung von RE-4 hat das
Baustellenregister über **40.960 B** gehoben (40.958 B — **2 B Luft**). Der Hebel war die
`updated:`-Kette im L1-Kopf: neu `phase10_inventory/UPDATES_ARCHIVE.md` (L3, verbatim), 17
Fäden rotiert (Skript `scripts/rotate_index_updates.sh`, sechs Gegenproben grün), Register
**40.958 → 39.117 B**. Ein Archiv entsteht, ein Posten wird nicht gekürzt.

**Ein Drift gegen den Plan, datiert.** Der Plan nennt **einen** Test
`test_rename_folder_by_owner_and_team_writer` (Plan §9.5). Gebaut sind **zwei**
(`…_by_owner`, `…_in_team_space_is_allowed`): der Gegenlauf zum gesperrten fremden
Home-Space braucht getrennte Tests, sonst ist der „Gegenlauf" dieselbe Behauptung. Der
Plan-Eintrag bekommt einen `[Nachtrag 2026-10-24]`.

**Bewusst nicht gebaut:** kein MCP-Werkzeug (Lock P10.5-M: das Umbenennen ist **human-only**,
RE-6-Linie) — der Agent darf Ordner nicht umbenennen.

**Ausführer-Daten.** `opencode/MiniMax-M3.1-Flash`, Kontextgrenze **400.000** (P10.5-C
erfüllt), keine Eingriffe des Nikingers in dieser Session.

**Stand.** Branch `p105-block9`, Wegwerf-Instanz gestoppt und aufgeräumt. **P10.5-37 und
P10.5-32 bleiben ⬜** (Augen-Urteil); das **Budget für `graph.js`** entscheidet der Nikinger.

**Nächster Schritt.** (1) Deploy C (`v3.1.7`) durch den Nikinger, dann `health_gate.sh` mit
echter Ausgabe in den Commit. (2) **Block 9.3** `Store.rename_space()` (RE-3, nur Team-Spaces,
Frontmatter-Umschreiben, ein Commit) + der Space-Teil des Absturz-Markers. (3) Merge
`p105-block9` → `main` **nach** dem Deploy.

## Session stopped — 2026-10-24 (Deploy C `v3.1.7` vorbereitet · Block 9.1 RE-7 `created_by` gebaut und gemessen)

**Ergebnis.** Zwei Dinge. **(1) Deploy C ist vorbereitet, nicht ausgeführt** — Badge `v3.1.7`,
ein eigener `## 2026-10-24`-Block in `docs/UPDATE_LOG.md` (9 Zeilen für Menschen), Suite **1425
grün**, `doc_health` **0**, `ui_budget` **5/5**. Commit `7d8c28e`, gepusht. **`deploy.sh` liegt
beim Nikinger** (Hard Rule 9):

    SHAREFYX_RELEASES_DIR=/opt/sharefyx/releases SHAREFYX_CURRENT_LINK=/opt/sharefyx/current \
    SHAREFYX_DATA_ROOT=/home/savefyx/savefyx-data SHAREFYX_BACKUP_DIR=/var/lib/sharefyx-backup \
    SHAREFYX_SYSTEMCTL="sudo systemctl" phase5_ui/scripts/deploy.sh main

Danach lese ich `health_gate.sh --expected-version=v3.1.7 --require-todays-update-log
--expected-sha=<sha>` und lege die **echte** Ausgabe in den Commit.

**(2) Block 9.1 (RE-7 `created_by`) ist gebaut und gemessen** — die zwölfte P1-Öffnung:
`Item.created_by` / `ItemSummary.created_by`, dieselbe Klasse wie `updated_by` (P9 Block trace):
serververwaltet, über **keinen** Kanal setzbar, **kein Backfill** (Lock P10.5-W). Betroffene
Dateien: `phase1_storage/storage/{models,store}.py` (der P1-Diff nennt **nur** diese beiden),
`phase2_mcp/mcpserver/tools.py`, `phase5_ui/webui/serializers.py`,
`phase5_ui/webui/static/{app.html,js/editor.js}` (eine **eigene** Lesezeile „Erstellt von X" —
eine leere `created_by` (Altbestand) darf die `updated_by`-Zeile nicht verschlucken).

**Gemessen.** Wegwerf-Probe `probes/p105_b9_created_by_probe.py` **12/12 Zellen** (Port 8799,
PID-Datei): Web-Anlage → Antwort **und** Datei nennen `created_by: alpha` · MCP-Anlage →
`get_item_meta` **und** Datei nennen ihn · **Altbestand**: `""`, **keine** Zeile in der Datei —
auch **nach** einem Write nicht (nichts erfunden) · Fälschung per PATCH → **422**, per POST → der
Wert bleibt der eingeloggte Mensch. 8 neue Tests (`test_store.py` × 5, `test_tools.py` × 3,
`test_api.py` × 2) und **4 Regel-Wächter mit je einem Gegenlauf**
(`tests/test_created_by_rules.py`: `_KNOWN_FIELDS` · `_SYSTEM_MANAGED_FIELDS` · `_summary()` ·
die Leerwert-Bedingung — jeder Gegenlauf macht **genau** seinen Defekt sichtbar).

**Ein Fund beim Bauen — die Probe selbst:** die Zelle „Altbestand nach einem Write" war
**vakuos**: der Titelwechsel benennt die Datei um (Slug!), der zwischengespeicherte Pfad zeigte
ins Leere, und „`created_by` nicht in ''" wäre grün gewesen. Der Pfad wird jetzt **neu geholt**
(`rglob` über die ID) und die Zelle prüft zusätzlich, dass die Datei **nicht leer** ist.

**Bewusst nicht gebaut:** `receipts.py :: write_receipt()` trägt `created_by` **nicht** —
`phase2_mcp/mcpserver/receipts.py` steht **nicht** auf der Block-9-Erlaubnisliste (Plan §3), und
`test_app.py` prüft die Patch-Quittung als **exaktes** Dict (eine Zeile mehr wäre dort ein
Testbruch). Beim Anlegen ist nichts verloren: die Quittung trägt `updated_by` = denselben Actor.

**Ausführer-Daten.** `opencode/MiniMax-M3.1-Flash`, Kontextgrenze **400.000** (P10.5-C erfüllt,
`~/.config/opencode/opencode.json`), keine Eingriffe des Nikingers in dieser Session, **ein**
Fehler beim Gegenlesen gefunden (die vakuose Zelle oben) und behoben.

**Stand.** Branch `p105-block9`, Baum sauber, Wegwerf-Instanz gestoppt. **P10.5-37 und P10.5-32
bleiben ⬜** (Augen-Urteil des Nikingers); das **Budget für `graph.js`** (+11,1 KB gzip statt
+8 KB) entscheidet der Nikinger.

**Nächster Schritt.** (1) Deploy C durch den Nikinger, dann `health_gate.sh` mit echter Ausgabe
in den Commit. (2) **Block 9.2** `Store.rename_folder()` (RE-4) und **9.3**
`Store.rename_space()` (RE-3), beide mit dem Absturz-Marker aus 9.4. (3) Merge `p105-block9` →
`main` **nach** dem Deploy.

## Session stopped — 2026-10-24 (Deploy C `v3.1.7` vorbereitet — Badge, Update-Log, Suite 1425 grün)

**Ergebnis.** Deploy C ist **vorbereitet, nicht ausgeführt**: Badge `v3.1.7`
(`phase5_ui/webui/static/app.html:25`) und ein eigener `## 2026-10-24`-Block in
`docs/UPDATE_LOG.md` — **9 Zeilen für Menschen**: die Karte im neuen Look, Suche/Filter und
„bleibt liegen" auf der Karte, die 404-Seite, die Wortmarke, der Tab-Titel, der „Zugewiesen"-Filter,
die doing-Hervorhebung, das einzeilige Update-Banner und die lesbarere Versionsanzeige. Das
Deploy-Gate (P6-X) liest den **obersten** Block: `2026-10-24` = heute ✓.

**Gemessen (Basis `45d3616`):** `pytest` **1425 grün** (332,6 s) · `doc_health` **0** ·
`ui_budget` **5/5** (app.js+css+Font **192,2 KB**, Erstaufruf **204,5 KB**) ·
`parse_update_log()` liest den neuen Block als `2026-10-24#1`, alle **21** IDs eindeutig.

**Was jetzt beim Nikinger liegt — der Deploy-Aufruf** (Hard Rule 9, `sudo`):

    SHAREFYX_RELEASES_DIR=/opt/sharefyx/releases SHAREFYX_CURRENT_LINK=/opt/sharefyx/current \
    SHAREFYX_DATA_ROOT=/home/savefyx/savefyx-data SHAREFYX_BACKUP_DIR=/var/lib/sharefyx-backup \
    SHAREFYX_SYSTEMCTL="sudo systemctl" phase5_ui/scripts/deploy.sh main

Danach lese ich `health_gate.sh --expected-version=v3.1.7 --require-todays-update-log
--expected-sha=<sha>` und lege die **echte** Ausgabe in den Commit — nie die Behauptung.
Live-Prüfungen laut Plan §Deploy C: Karte mit echten Daten (Sichtung), Logo/Favicon in Firefox
und Safari, 404-Seite, Titel.

**Drei Dinge warten weiter auf Dein Augen-Urteil bzw. Deine Entscheidung:**
1. **P10.5-37** — die vier Kartenbilder `docs/screenshots/p105_b8_0{1..4}_*.png` (C2-Stil).
2. **P10.5-32** — die Bestätigung der vier Sichtungsposten aus 7.4.
3. **Das Budget für `graph.js`** — erlaubt +8 KB gzip, gemessen **+11,1 KB** (davon +9,8 KB
   Kommentar, der Code selbst +2,9 KB): Budget anheben oder Kommentare kürzen.

**Reihenfolge-Hinweis für Block 9.** Block 9 (RE-7/RE-4/RE-3) wird auf einem **eigenen Branch**
(`p105-block9`) gebaut, **nicht** in `main`: `deploy.sh` klont das lokale `main`, ein Merge vor
dem Deploy würde Block 9 mit `v3.1.7` ausliefern. Erst der Merge **nach** dem Deploy.

**Beim Nikinger offen (unverändert):** P10.5-22 · 25 · 27/28 · 18 · AL-1 Zeile 15 · V203 ·
5.7 (Fabian Bescheid) · die Schriftart der Versionsanzeige.

## Session stopped — 2026-10-24 (Block 8 gebaut — die Gehirnkarte C2; drei Fehler fand erst der Browser)

**Ergebnis.** Die Karte trägt jetzt den Stil C2 (`docs/concepts/phase10_karte_c_stil_2.svg`):
**Lappen** (der Körper, in Space-Gruppen geteilt, mit Innenlinie), **Furchen** (die
Space-Grenze), **Bahnen** (quadratische Bézier, Breite `1 + log2(1 + min(deg))`), **Zellen**
(Kreis, Membranring 2 px, 2–4 deterministische Fortsätze), **Aktivierung** (Fokus hell, erster
Ring 1, zweiter Ring 0,5, Rest 0,45 — in Ruhe voll deckend), **KA-2** (Layout merken:
`localStorage`, gedrosselt 1 s), **KA-3** (Suche, Typ-/Statusfilter, Titel ohne Zoom) und
**reduced motion mit 0 Animationsframes** (M6-Nebenbefund „1 Tick statt 0" erledigt). Nichts
deployed — `v3.1.7` steht aus.

**Drei Fehler, die erst der Browser fand** (der Node-Harness sieht die Zeichenbefehle, aber
keinen echten Zeiger und keine echte Zeit): (1) der **gezogene Knoten wurde wieder
freigegeben** (`fixed = false`) — die Simulation zog ihn zurück, die Ablage speicherte die
zurückgezogene Position, der Zug des Menschen war beim nächsten Öffnen weg; er wird jetzt
**gepinnt**. (2) **Der Fokus überlebte den Zeiger** (`onMouseLeave()` räumte `hoverId` nicht ab):
die Karte blieb abgedunkelt (26 164 statt 13 989 Kernpixel) — Plan 8.4 sagt „Ruhezustand ohne
Fokus: alles voll deckend". (3) **Der Layout-Hinweis hat die Trefferzahl überschrieben** (sie stand
in derselben Statuszeile): sie hat jetzt ein **eigenes** Feld (`#overview-graph-hits`).
Alle drei sind behoben und in `tests/test_graph_c2.py` gewächtert (Anker: die **Regeln**).

**Zwei Befunde für den Nikinger.**
- **Das Plan-Budget für `graph.js` ist überschritten:** erlaubt +8 KB gzip, gemessen **+11,1 KB**
  — davon **+9,8 KB Kommentar**, der **Code** wächst nur **+2,9 KB**. Die *Gesamt*budgets halten
  (`ui_budget` **5/5**, app.js+css+Font **192,7 KB**, Erstaufruf **205 KB**). Kürzen ginge nur
  auf Kosten der datierten P8/P9-Kommentare. Entscheidung: Budget anheben oder Kommentare
  kürzen.
- **Die Lappen brauchen räumlich zusammenhängende Spaces** — die Furche liegt an der
  Space-Grenze; liegen die Spaces **ineinander** (der Phase-8-Seed verlinkt die 200 Knoten zu
  *einem* Ring über alle Spaces), zerfallen die Lappen zu Fragmenten (252 px, im Bild nicht als
  Fläche erkennbar). Für die Screenshots habe ich die Wegwerf-Instanz deshalb **je Space
  gebündelt** verlinkt (`probes/p105_b8_cluster_links.py` — nur die Kanten der Wegwerf-Daten):
  **137 492 px** Lappenfläche, drei getrennte Gruppen, im Bild erkennbar.

**Belege.** Browser-Probe `probes/p105_b8_karte_probe.py` an der 200-Knoten-Wegwerf-Instanz
(Port 18772, tmp-`DATA_ROOT`, PID-Datei): **4/4 Messungen grün**, **3 Gegenläufe je rot**
(`lappen` → 0 Pixel, `layout` → 0 Kernpixel am Ziel, `filter` → wirkungslos). Node-Harness
`probes/p105_b8_c2_probe.mjs`: 8 Messungen, 8 Gegenläufe. Wächter `tests/test_graph_c2.py`
**21 Tests** grün. Smoke `p8_22_smoke.py`: **5/5**. Suite **1422 grün**, `ui_budget` **5/5**,
`doc_health` 0. Screenshots `docs/screenshots/p105_b8_0{1..4}_*.png` (die P8-22-Bilder sind
durch den Smoke-Lauf erneuert — mit C2-Look).

**Datierte Abweichung vom 📕-Plan (Code schlägt Plan).** Der Plan nennt nur den *Saatpunkt* der
gemerkten Position — ohne Festhalten schiebt die Simulation die gemerkte Karte auseinander und
KA-2 wäre nicht erfüllt: ein gemerkter Knoten wird **gepinnt**.

**Stand.** `main`, Baum sauber, Wegwerf-Instanz gestoppt. **P10.5-37 bleibt ⬜** — die Zeile wird
erst ✅, wenn Du die vier Screenshots beurteilt hast.

**Nächste Session.** (1) **Deploy C `v3.1.7`**: Suite + `doc_health` + `ui_budget` grün · Badge
und `docs/UPDATE_LOG.md` · Commit + Push · **`deploy.sh` durch den Nikinger** (Hard Rule 9) ·
`health_gate.sh` mit echter Ausgabe. (2) **P10.5-37**: Sichtung der vier Screenshots.
(3) **Nachsichtung** (≤ 6 Posten) — nach Block 11.

**Beim Nikinger offen:** siehe *Offen beim Nikinger* oben — **neu: das Budget für `graph.js`
(Block 8)**.

## Session stopped — 2026-10-24 (Block 7.4 umgesetzt — die vier Posten der Sichtung; P10.5-32 wartet auf die Bestätigung)

**Ergebnis.** Die vier Posten aus `STARTUPTRAG_ARCHIVE.md` Schritt 7.4 sind gebaut und an der
Wegwerf-Instanz gemessen. **1 Wortmarke:** der Abstand zwischen Zeichen und Wortrest war
`.45em` (5,6 px), jetzt `.2em` — **gemessen 2,5 px** (eine Klasse, also Rail **und**
Anmeldeseite). **2 „Zugewiesen"-Auswahl:** sie lief bündig an den Listenrand (x = 0), die
Suchzeile darüber mit 16 px Innenabstand; jetzt dieselben Kanten — **gemessen: linke Kante
identisch mit dem Suchfeld (0 px Versatz), rechte Kante identisch mit dem „+"-Knopf (0 px)**.
**3 Update-Banner:** er war bis zu ~140 px hoch (alle Zeilen des neuesten Eintrags) und schob
jede angemeldete Ansicht nach unten; jetzt eine **einzeilige Leiste (49 px)**: die erste Zeile
des Eintrags als Schlagzeile, der Rest über den neuen Knopf **„Alle Änderungen"**, der den
Update-Log in den Einstellungen öffnet (**gemessen: der Log öffnet, 20 Einträge sichtbar**).
**4 Versionsanzeige:** „v3.1.6" las sich als „v316" — bei 9 px war der hellste Pixel des
Punktes **155/255 (61 %)**, er verblasste in den Grund; jetzt 11 px und `.03em` Laufweite →
**203/255 (80 %)**.

**Befund für den Nikinger.** Der Punkt wird in dieser Schrift erst bei **13 px** ein Quadrat
(2 × 2 px statt 1 × 2) — 13 px wären größer als die Wortmarke (12,5 px). Mit der
vorgeschlagenen Schriftgröße ist der Punkt **erkennbar, aber nicht quadratisch**; eine eigene
Schriftart für die Version (Monospace) würde es runden, **widerspricht aber der gelockten
Entscheidung P6 vom 2026-08-13** („keine eigene Schriftart") — das ist Deine Entscheidung.
Das Auge entscheidet bei der Nachsichtung.

**Belege.** Wächter `phase10_5_finishing/tests/test_sichtung_7_4.py` (8 Tests, **4 Gegenproben
im Wächter selbst**: der alte Wert muss rot werden — die Anker sind die *Regeln*, nicht die
Werte, weil `margin-right: .2em;` auch im Kommentar stand und der erste Gegenlauf deshalb
den Kommentar gepatcht hätte). Probe `probes/p105_b7_sichtung_probe.py` (Wegwerf-Instanz
**18793**, PID-Datei): **5/5 Kriterien** grün, **5 Gegenläufe** (`mark`/`auswahl`/`banner`/
`version`/`alle`) je rot — der erste Entwurf des Gegenlaufs stellte die Datei **halb** wieder
her (die Restore-Logik schrieb die Zwischensätze) und der Anker traf den Kommentar; beides
gemessen und behoben. Suite **1404 grün** (1396 + 8), `doc_health` 0, `ui_budget` **5/5** (192,7 KB).

**Stand.** `main`, Baum sauber, keine Wegwerf-Instanz läuft. **P10.5-32 bleibt ⬜** — die Zeile
wird erst ✅, wenn Du die vier Posten bestätigt hast.

**Nächste Session, in dieser Reihenfolge.**
1. **Block 8** (Karte C2): Plan § „Block 8"; Abnahme P10.5-36/37. Vorher `git log` auf Stand
   prüfen und die Kontextgrenze 400 K (P10.5-C) bestätigen.
2. **Deploy C `v3.1.7`** nach Block 7–8: Suite + `doc_health` + `ui_budget`, Badge und
   `docs/UPDATE_LOG.md`, Commit + Push, **`deploy.sh` durch den Nikinger** (Hard Rule 9),
   `health_gate.sh` mit echter Ausgabe.
3. **Nachsichtung** (Sichtung des Nikingers, ≤ 6 weitere Posten) — nach Block 11, denn der
   Alles-in-einem-Editor ändert das Bild.

**Beim Nikinger unverändert offen:** P10.5-22 · 25 · 27/28 · 18 · AL-1 Zeile 15 · V203 ·
5.7 (Fabian Bescheid) · **neu: die Schriftart der Versionsanzeige** (Befund oben).

## Session stopped — 2026-10-24 (Block 7.5–7.7 gebaut und gepusht; 7.4 Sichtungsliste liegt beim Ausführer)

**Ergebnis.** Drei Schritte gebaut, Suite **1396 grün**, `ui_budget` 5/5 OK, `doc_health` 0.
**7.5 (UI-5):** `--caution` ist nicht mehr `var(--danger)`, sondern `#F06A6E` — Text auf der
Standardknopf-Fläche: Ruhe **5,70:1** (vorher 4,38), Hover **4,81:1** (vorher 3,69). Wächter
`tests/test_contrast.py` liest die Tokens aus `app.css`; Gegenlauf mit dem alten Wert **rot** (4,376).
**7.6 (UI-6):** `api.py :: _items_get` filtert `?assignee=` **nach** dem Leserechtfilter und **vor** der
Paginierung (kein Orakel über unsichtbare Items); Auswahl `#list-assignee` in der Listenkopfzeile aus
`state.spaces`, im globalen Modus ausgeblendet. 2 Tests, Gegenlauf rot. **7.7 (KA-5):** Chip „In Arbeit"
trägt `overview__space-count--doing`; `doing`-Knoten der Karte bekommen einen statischen Ring.
**Probe** `probes/p105_b7_filter_probe.py` (Wegwerf-Instanz, Port 18792, PID-Datei): 6/6 ✓, Gegenläufe `filter` und `ring` rot (ein Lauf lief in einen Selektor-Timeout, seither `wait_for_selector`).

**Befund für den Nikinger.** 7.5 hebt **P8.6-F** („zwei Namen auf einem Wert") auf — gedeckt durch D-7,
aber eine gelockte Entscheidung, die sich bewegt. Der Ring nutzt `--accent` (`#3E8DF3`), nicht `spaceOwn`
(`#4A93F0`): sonst wäre er auf eigenen Knoten farbgleich zur Füllung. Der Filter gilt auch bei ID-Suche
(wie `type`/`status`). **P10.5-35 ✅**: Canvas-Probe zählt 44 Ringpixel, ohne Ring 0.

**Stand beim Schluss.** `main` = `origin/main` (Commits `a56d52d` 7.5–7.7, `94d5df2` Sichtungsliste), Baum sauber,
keine Wegwerf-Instanz läuft (PID-Dateien weg). Nichts deployed — `v3.1.7` steht aus.

**Nächste Session, in dieser Reihenfolge.**
1. **7.4 umsetzen** (Ausführer): die **4 Posten** aus `STARTUPTRAG_ARCHIVE.md` Schritt 7.4 — Wortmarken-Abstand,
   „Zugewiesen"-Auswahl, Update-Banner kompakter, Versionsanzeige. Danach P10.5-32 erst ⬜ → ✅, wenn der
   Nikinger bestätigt; die **Nachsichtung** (≤ 6 weitere Posten) kommt nach Block 11.
2. **Block 8** (Karte C2): Plan `docs/concepts/phase10_5_finishing_plan.md` § „Block 8"; Abnahme P10.5-36/37.
   Vorher `git log` auf Stand prüfen und die Kontextgrenze 400 K (P10.5-C) bestätigen.
3. **Deploy C `v3.1.7`** nach Block 7–8: Suite + `doc_health` + `ui_budget`, Badge und `docs/UPDATE_LOG.md`,
   Commit + Push, **`deploy.sh` durch den Nikinger** (Hard Rule 9), `health_gate.sh` mit echter Ausgabe.

**Beim Nikinger unverändert offen:** P10.5-22 · 25 · 27/28 · 18 · AL-1 Zeile 15 · V203 · 5.7 (Fabian Bescheid).
**Fallstrick für die Rotation:** `rotate_session_block.sh` behält den **letzten** Block der Datei, nicht den
obersten — den neuen Block **unter** den alten setzen, dann rotieren.

## Session stopped — 2026-10-23 (Deploy B live; Block 7.1 (UI-1), 7.2 (UI-2) und 7.3 (UI-3) gebaut)

**Ergebnis.** Der Deploy-Befehl der letzten Session war **korrekt** — rot waren die **Release-Tests**,
der Grund lag in **einer verklebten Zeile**: `phase10_5_finishing/SESSIONS_ARCHIVE.md:8` trug die
`updated:`-Kette als `…Wegwerf-Instanz)pdated: 2026-10-23 (…` — der Trenner ` | ` war als `pdated: `
verschluckt ⇒ der Wächter `test_no_thread_is_invisible_to_the_rotation_anchor` stand rot ⇒
`deploy.sh` bricht in Schritt 4 ab, **vor** dem Symlink-Wechsel (gemessen: ein Release-Checkout auf
`a7fe62c` ist rot — **nichts** deployed, **nichts** beschädigt). **Reparatur: eine Zeile**
(`)pdated:` → `) | `, −5 B); `chain_defects` → `(False, 0, 0)`, `blind_positions` → `[]`, **12** Fäden
sichtbar, `test_updated_chain.py` **7/7**. **Release-Stand vorab am Klon geprüft** (frisches venv, `constraints.txt`): **1380 grün**
(337,2 s) — an der Stufe konnte der Deploy nicht mehr scheitern.

**Der Deploy lief beim Nikinger (Hard Rule 9, `sudo`).** `sudo -n true` sagt „a password is
required" — auch in einem pty; das Journal zeigte **keine** erfolgreiche `savefyx`-sudo seit
Deploy A ⇒ der Deploy gehört ins Terminal des Ningkers. **Ein Deploy ohne Neustart wäre eine
stille Halbdeplosion:** `static_routes.py` liest `app.html` pro Anfrage von der Platte — der
Symlink stünde schon auf `v3.1.6`, der Prozess liefe aber mit dem alten Code; das Gate wäre
**grün und falsch**.

**Deploy B ist live.** Release-Tests im Release **1380 grün** (340,7 s) → Symlink auf
`/opt/sharefyx/releases/20261023T165838.591015Z` → Dienst neu gestartet. Mein Gate danach:
`health_gate.sh --expected-version=v3.1.6 --require-todays-update-log --expected-sha=e5c834e` →
**9/9 OK** (`.rail__version` v3.1.6, Release-SHA `e5c834e…`, Update-Log 2026-10-23).
**Block 7.1 ist gemergt** (`f0e76b0`) — im Release B **nicht** dabei, das kommt mit `v3.1.7`.

**Block 7.1 (UI-1): die HTML-404.** `pages.py :: render_not_found_page()` und die Route
`Route("/ui/{rest:path}", …)` **nach** allen `/ui`-Routen. **Datierte Korrektur zum Plan:** „API bleibt
JSON" war gemessen **falsch** (unbekannter `/api/v1/…`-Pfad ⇒ Starlette-Klartext) ⇒ JSON-404 in der
API-Fehlerform. 4 neue Tests gegen die **echte** `create_app()`, **4 Gegenläufe wirksam**.

**Block 7.2 (UI-2): die Wortmarke.** `static/logo.svg` — Variante B („Überlagert") aus dem
Logo-Board, **pixelgleich** gemessen (190 px 0,13/255 · 32 px 0,39/255 · 16 px **0,00**/255). Die
Farben sind die App-Tokens **mit Ersatzwert**, weil `<img>` und Favicon **keine** Seiten-Variablen
erben. **Zwei Befunde nur durch Messung:** `--` im XML-Kommentar ⇒ die Fehlerseite statt des
Zeichens; `.svg` fehlte in der MIME-Tabelle ⇒ **der Browser rendert ein SVG mit falschem MIME-Typ
nicht**. Probe an der Wegwerf-Instanz: `naturalWidth` 100, gerendert **16 × 16**, **Gegenlauf rot**.

**Block 7.3 (UI-3): der Tab-Titel.** `state.js :: setViewTitle(part)` + `setPanelTitle(open)` — der
Titel folgt der **Ansicht** (Übersicht · Space-Name · Item-Titel · Einstellungen), das Panel liegt
als Overlay darüber und gibt den Ansichts-Titel zurück. **Datierte Korrektur zum Plan:** er nennt
fünf Titel, gemessen sind es **vier Zustände** — die Karte ist kein eigener Zustand (Kontextbereich
neben der Liste; `loadGraph()` läuft bei jedem Spacewechsel und würde den Item-Titel überschreiben).
Probe an der Wegwerf-Instanz: **6/6 Schritte** ✓, **Gegenlauf rot** ✓.

**Raum-Budget:** der Head stand bei **40.968 B** ⇒ die 24 älteren `updated:`-Fäden rotierten nach
`UPDATES_ARCHIVE.md` ⇒ Basis 32.572 B — jetzt bindet wieder **DO-3** (Block ≤ 4.096 B). Nächster
Hebel: der „Startauftrag" (5,8 KB) → L3-Archiv.

**Offen / nächster Schritt.** Abzunehmen: **P10.5-22** · **P10.5-25** · **P10.5-27/28** (Live
P10-J, zwei Modellanbieter) · **P10.5-18** · AL-1 Zeile 15 · V203. **5.7:** Fabian Bescheid.
Baulich: **Block 7.4** (Sichtung, Claude Code) — `v3.1.7` folgt nach Block 7–8.

## Session stopped — 2026-10-23 (Deploy-B-Generalprobe 26/26 Zellen grün · Update-Log-ID (Block 7.0) behoben)

**Ergebnis.** Die Generalprobe vor Deploy B (`v3.1.6`) ist gebaut und gefahren:
`phase10_5_finishing/probes/p105_deploy_b_probe.py` — **26 von 26 Zellen grün** gegen den Stand,
der deployt werden soll (`main` mit Block 5 + 6, `fastmcp 4.1.3`), an der Wegwerf-Instanz (Port
8799, tmp-`DATA_ROOT`, tmp-`auth.sqlite3`, selbstsigniertes TLS, File-Keyring) — **nicht** gegen
den laufenden Dienst. **Der Befund, den sie gefunden hat, ist behoben** (Block 7, Schritt 7.0).

**Fünf Gruppen.** **A · die Tore des `health_gate.sh` (1–5 + 7), an der Wegwerf-Instanz statt
live** — Gate 4 (`/mcp/` → 401) ist das Tor, das Deploy B hätte reißen können: Block 6 bedient
`/mcp` **ohne** Slash exakt (`_ExactMcpMount`), der Mount **mit** Slash muss weiter 401 liefern.
**B · Transport `/mcp`**: 401 mit Challenge, **kein 307** (P10.5-25). **C · der MCP-Weg über
HTTP**: 11 Werkzeuge, `append_to_items` → `ok:1, failed:1`. **D · das Log-Feld `proto`**: es zeigt
die *Anfrage*, nicht die Aushandlung — ohne `MCP-Protocol-Version`-Header der Server-Standard
(`2025-03-26`), mit Header die Version des Clients (`2025-11-25`). **E · der Update-Log-Banner**
(siehe unten).

**Gemessen.** `pytest` **1380 grün** (306 s) · `doc_health` 0 · `ui_budget` 5/5 (188,5 KB) ·
**opencode 1.19.4** (Wegwerf-E2E): Login + TOTP + Consent im Chromium → **11** MCP-Werkzeuge im
Modell-Request → `ev=tool, tool=list_spaces, ok=true, proto=2025-11-25` · **DCR**: derselbe
Request **201** · `mcp_smoke.py` **17/17** · Protokoll-Probe: beide Ären · Browser: Z3 **58,3 ms**,
Z4 beide Seiten der 200-ms-Grenze, Z2 **44 ms**/**68 ms**.

**Der Befund aus Gruppe E (Bezug: das Session-Ende vom 2026-10-23) — behoben.** Die Update-Log-IDs
zählten die Blöcke eines Datums **von oben** — ein zweiter Deploy **am selben Tag** bekam damit die
ID `#1`, die der erste schon hatte ⇒ `latest_id == seen_update_id` ⇒ **kein Banner**. Gemessen:
`latest=2026-10-23#1 seen=2026-10-23#1 banner=False` (Alt-Schema) gegen
`latest=2026-10-23#2 … banner=True` (Zähler von unten). **`webui/updates.py` zählt jetzt von
unten** (Block 7, Schritt 7.0 — dort sind Code-Pfade erlaubt, Block 12 darf nur `.md`
anfassen): die IDs der bestehenden Blöcke **bleiben** stehen, ein neu oben eingefügter Block
bekommt eine **neue**. Vier neue Wächter in `phase10_5_finishing/tests/test_update_log_ids.py`;
der alte Basistest in `phase6_shares/tests/test_updates.py` trug die alte Zählung und wurde mit
datierter Notiz nachgezogen. **Ein Sonderfall bleibt benannt:** bei einem Datum mit zwei Blöcken
tauschen die beiden IDs ihre Plätze — wer damals den oberen Block gesehen hat, sieht ihn **einmal**
wieder (harmlos).

**Zwei eigene Fehler der Messung, beide behoben** (ein Messgerät, das etwas anderes misst als es
behauptet, ist schlimmer als gar kein Messgerät): erstens trug das Token der Probe die
**Metadata-Adresse** statt `<base_url>/mcp` als Ressource ⇒ 401 (der Resolver prüft die Audience,
RFC 8707); zweitens war der `append_to_items`-Fall **nicht wiederholbar** — nach einem Lauf war
das Item eine Version weiter, der „gute" Eintrag scheiterte also selbst am Konflikt (jetzt liest
die Probe die Version vorher über `get_item_meta`).

**Offen / nächster Schritt.** Deploy B ist beim Nikinger (Hard Rule 9, `sudo`): derselbe Aufruf
wie bei Deploy A, danach `health_gate.sh --expected-version=v3.1.6 --require-todays-update-log
--expected-sha=<SHA>` — die **echte** Ausgabe in den Session-Block, nie die Behauptung. Live danach:
**P10.5-22** (Connector-Werkzeuge, Log-Feld `proto`) · **P10.5-25** (`POST …/mcp` → 401 mit
Challenge) · **P10.5-27/28** (Live P10-J, zwei Modellanbieter). **5.7:** Fabian kurz Bescheid.
**Danach:** Block 7, Schritte 7.1–7.7 (UI-1–UI-6, KA-5) auf einem Zweig `p105-block7` — **nicht**
vor dem Deploy B auf `main`, sonst liefert `deploy.sh main` den Block-7-Stand unter `v3.1.6`.

## Session stopped — 2026-10-23 (Deploy B `v3.1.6` vorbereitet — Badge, Update-Log, Suite 1376 grün)

**Ergebnis.** Deploy B ist **vorbereitet, nicht ausgeführt**: Badge `v3.1.6`
(`phase5_ui/webui/static/app.html:20`), ein **eigener** `## 2026-10-23`-Block in
`docs/UPDATE_LOG.md` (3 Zeilen für Menschen — der zweite Deploy am selben Tag bekommt seinen
eigenen Block, nicht stillschweigend eine Ergänzung im ersten; Konvention `parse_update_log()`),
und der Dev-venv trägt jetzt `fastmcp 4.1.3` / `mcp 2.3.0` / `starlette 1.9.0` — **identisch mit
`constraints.txt`** (Block 5 hat die Datei neu erzeugt; `main` pinnte vorher noch 3.4.7).

**Gemessen (Basis `2fdff03` = `main` nach dem Merge):** `pytest` **1376 grün** (338,9 s) ·
`doc_health` 0 · `ui_budget` 5/5 (188,5 KB Erstaufruf) · `pip freeze` **byteweise** gleich
`constraints.txt`.

**Ein Nebenbefund, der in Block 7 oder 12 gehört (kein Produktcode hier).** Die Update-Log-IDs
zählen die Blöcke **eines Datums in Dateireihenfolge** (`webui/updates.py :: parse_update_log()`),
und der gesehen-Zustand hängt an genau dieser ID (`users.seen_update_id`). Ein **zweiter Deploy am
selben Tag** bekommt den neuen Block oben — und damit die ID `#1`, die der erste Block **schon
hatte** (`latest_id == seen_update_id` ⇒ **kein Banner**). Der neue Eintrag ist damit für den
Benutzer stumm. Das ist ein Altbestand aus P6 (nicht von diesem Deploy erzeugt) — als Befund
notiert, die Entscheidung (ID um die Inhaltslänge ergänzen? Zähler nach Einfüge-Reihenfolge?)
gehört nicht in einen Deploy-Commit.

**Nikinger-Entscheidung 2026-10-23 (Session-Ende): Deploy B wird jetzt **nicht** ausgeführt.**
Die Vorbereitung steht (Commit `b75c446`) und wartet; der Deploy läuft erst, wenn die nächste
Session **zuerst gründlich an der Wegwerf-Instanz** getestet hat — live wird erst danach
deployt. Die Reihenfolge ist damit: **Wegwerf-Test → Deploy B → Live-Abnahmen** (10-22, 10-25,
10-27/28).

**Offen / nächster Schritt.** **Deploy B ist beim Nikinger**, sobald der Wegwerf-Test durch ist
(Hard Rule 9, `sudo`): derselbe
Aufruf wie bei Deploy A, danach `health_gate.sh --expected-version=v3.1.6
--require-todays-update-log --expected-sha=<SHA>`. Live-Checks (Plan §Deploy B): **P10.5-22**
(claude.ai-Connector `list_spaces`/`search_items`/`get_item`/`update_item`, Log-Feld `proto` zeigt
die Ära, V208) · **P10.5-25** (`curl -si -X POST …/mcp` → **401 mit Challenge**, nicht 307) ·
**P10.5-27/28** (Live P10-J, zwei Modellanbieter). **5.7:** Der Nikinger sagt Fabian Bescheid
(„kurzer Neustart; der Connector sollte ohne neue Anmeldung weiterlaufen") — Token, Issuer und
Auth-DB bleiben unverändert, also ist kein Re-Auth zu erwarten.

## Session stopped — 2026-10-23 (Deploy A `v3.1.5` **live** (Gate 9/9) · P10.5-26 ✅ geklärt · Merge `p105-block5` → `main`)

**Ergebnis.** Drei Dinge an einem Tag: **Deploy A ist live** (`v3.1.5`, Release
`20261023T065010.377336Z`, SHA `7358f22`, `health_gate` **9/9 OK**), **P10.5-26 ist geklärt**
(opencode 1.19.4 führt `list_spaces` aus — der Auslöser lag im **Messgerät**, nicht im Server),
und der Branch `p105-block5` (Block 5 + 6 + P10.5-26) ist **nach `main` gemergt**.

**Deploy A — die echte Gate-Ausgabe** (`health_gate.sh --expected-version=v3.1.5
--require-todays-update-log --expected-sha=7358f22`, gelesen ohne Rechte):

```
OK  /health -> 200
OK  /ui/login -> 200
OK  /api/v1/me -> 401
OK  /mcp/ -> 401
OK  .rail__version -> v3.1.5
OK  /opt/sharefyx/current -> /opt/sharefyx/releases/20261023T065010.377336Z
OK  Release-SHA: 7358f227d75438c16b6f18b0ee38e77a5d83de07
OK  docs/UPDATE_LOG.md oberster Eintrag: 2026-10-23
OK  Release-SHA 7358f227d75438c16b6f18b0ee38e77a5d83de07 matched --expected-sha=7358f22
{"ts":"2026-10-23T06:58:27.290Z","action":"health_gate","result":"ok","expected_version":"v3.1.5","actual_version":"v3.1.5","active_release":"/opt/sharefyx/releases/20261023T065010.377336Z","release_sha":"7358f227d75438c16b6f18b0ee38e77a5d83de07","port":8765}
```

**P10.5-26 in einem Satz.** Beide Verdachtsmomente vom 2026-10-22 sind **widerlegt**: der `405`
auf `GET /mcp` ist nicht die Ursache (offener FastMCP-Server mit *und* ohne SSE-Strom: opencode
arbeitet einwandfrei), und der behauptete serverseitige Werkzeugaufruf war **nicht belegt** (null
`ev=tool` in der Wegwerf-Logdatei). Der Auslöser lag im Messgerät: der Stub-Prototyp lief endlos
und der `mcp debug`-Schritt stand vor dem Werkzeuglauf. Beleg: `ev=tool, tool=list_spaces,
ok=true, proto=2025-11-25` im Log **desselben** Laufs. **Kein Produktcode** — P2-B bleibt.

**Reihenfolge (Nikinger-Entscheidung 2026-10-23).** Deploy A **zuerst** aus `main`
(`fastmcp 3.4.7` im Dev-venv), **danach** der Merge, **dann** Deploy B (`v3.1.6`,
`fastmcp 4.1.3`). Grund: `deploy.sh main` liefert aus, was auf `main` steht — ein Merge vor dem
Deploy A hätte den Block-5/6-Stand unter der Nummer `v3.1.5` ausgeliefert.

**Offen / nächster Schritt.** **Deploy B (`v3.1.6`)**: Badge + `docs/UPDATE_LOG.md` + Dev-venv neu
(`fastmcp 4.1.3`) + Suite, dann der Deploy durch den Nikinger (Hard Rule 9). Beim Nikinger:
**P10.5-18** (Live-Messung nach Deploy A), **P10.5-27/28** (Live P10-J, zwei Modellanbieter),
AL-1 Zeile 15, V203.

## Session stopped — 2026-10-23 (P10.5-26 ✅ — opencode führt `list_spaces` aus; der Auslöser lag im Messgerät)

**Ergebnis.** opencode 1.19.4 ruft gegen unseren Wegwerf-Server `list_spaces` auf — serverseitig
belegt: `ev=tool, tool=list_spaces, ok=true, proto=2025-11-25`. **Kein Produktcode angefasst,
P2-B unberührt.** Zwei Fehler lagen im **Messgerät**, nicht im Server:

1. **Der Stub-Prototyp lief endlos.** Er erkannte sein eigenes Werkzeug-Ergebnis an der
   Zeichenkette `list_spaces` **im Ergebnisinhalt** — dort steht sie nie (das Ergebnis ist die
   Liste der Spaces). Der Name steht in der `tool_calls`-Liste der vorangegangenen
   Assistenten-Nachricht. Folge: 1500 Nachrichten in 120 s, dann Timeout — der „Timeout" der
   Notiz vom 2026-10-22 war **das Messgerät**, nicht der Client.
2. **Der `opencode mcp debug`-Schritt stand vor dem Werkzeuglauf** und hat ihn kaputt gemacht:
   direkt danach sah der Modell-Request **kein** MCP-Werkzeug, und der Server-Log enthielt
   **null** `ev=tool`-Zeilen (in der ganzen Datei). Reihenfolge jetzt: Auth → Werkzeuglauf →
   Debug.

**Die zwei Verdachtsmomente sind widerlegt — gemessen, nicht behauptet.**
- **„`GET /mcp` → 405 ist die Ursache"** (2026-10-22): **nein.** Gegen einen offenen
  FastMCP-Server (`stateless_http` true **und** false) arbeitet opencode einwandfrei; der 405
  steht auch im **erfolgreichen** Lauf gegen unseren Server im Log.
- **„Der Werkzeugaufruf gelang serverseitig"** (2026-10-22): **damals nicht belegt** — die
  Wegwerf-`serve.log` enthielt bis heute **null** `ev=tool`-Zeilen (die Zeile kam aus einem
  anderen Lauf). Jetzt steht sie im Log **desselben** Laufs.

**Weitere Messungen (Wegwerf, `phase10_5_finishing/probes/`).**
- `p105_b6_transport_probe.py`: zwei FastMCP-Server (POST-only vs. POST+SSE) — **beide**
  funktionieren; der Beleg ist die Werkzeugliste des Modell-Requests.
- `p105_b6_opencode_matrix_probe.py`: vier Varianten gegen **unseren** Server (OAuth-Default,
  statischer Bearer, `protocol: auto`, `protocol: 2026-07-28`) — **alle vier** sehen die 11
  MCP-Werkzeuge. Der Wegwerf-Bearer-Token wird nirgends ausgegeben (maskiert).

**Offen / nächster Schritt.** **P10.5-27/28** (Live P10-J, zwei Modellanbieter) bleiben beim
Nikinger — nach Deploy B (`v3.1.6`). Die Live-Sichtprüfungen zu Deploy A (P10.5-18, Caddy-Zeile,
Handyfoto-Upload, Spaces-Panel) ebenfalls beim Nikinger.

## Session stopped — 2026-10-23 (Deploy A `v3.1.5` vorbereitet — Badge, Update-Log, Suite 1335 grün)

**Ergebnis.** Deploy A ist **vorbereitet, nicht ausgeführt**: Badge `v3.1.5`
(`phase5_ui/webui/static/app.html:20`), neuer `## 2026-10-23`-Block in `docs/UPDATE_LOG.md`
(5 Zeilen für Menschen, am echten `parse_update_log()` gegengeprüft), Dev-venv **frisch** aus
`main` gebaut — `main` pinnt `fastmcp 3.4.7`, das Venv trug vorher 4.1.3 aus dem Branch
(zwei Wächter wären rot gewesen, P10.5-Q).

**Gemessen (Basis `a1cc523` = `main`):** `pytest` **1335 grün** (337,9 s) · `doc_health` 0 ·
`ui_budget` 5/5 (176,9 KB gzip; Erstaufruf 188,5 KB) · `pip freeze` = `constraints.txt`
(`fastmcp 3.4.7`, `mcp 1.30.0`, `starlette 1.7.0`) — der Wächter
`test_every_installed_distribution_matches_the_constraints` ist grün.

**Ein Doku-Befund (Drift, behoben).** Die Summenzeile der Abnahmetabelle stand auf
`18 ✅ · 0 ⚠️ · 43 ⬜`, die Tabelle trug **17** ✅ und **44** ⬜ → Zähler nachgezogen. Auf
`p105-block5` ist dieselbe Zeile bereits richtig (23 ✅, Korrekturnotiz vom 2026-10-22) — nach
dem Merge gilt deren Stand.

**Offen / nächster Schritt.** **Deploy A ist beim Nikinger** (Hard Rule 9, `sudo`); der Aufruf
steht wörtlich unter „Offen beim Nikinger", danach liest Claude Code `health_gate.sh` mit
**echter Ausgabe**. **Reihenfolge (Nikinger-Entscheidung 2026-10-23): Deploy A aus `main`
zuerst, dann der Merge von `p105-block5` nach `main`, dann Deploy B (`v3.1.6`)** — der Merge
darf **nicht** vor dem Deploy A auf `main` landen, sonst deployt `deploy.sh main` den
Block-5/6-Stand unter der Nummer `v3.1.5`. Merge-Konflikt absehbar in der Phase-Head-Datei
(beide Seiten haben sie umgeschrieben) — von Hand auflösen, dann den Session-Block rotieren.
**P10.5-26 bleibt ⬜** und ist **vor** 10-27/28 zu klären (der Werkzeugaufruf gelingt
serverseitig, opencode setzt die Sitzung nicht fort).

**Ausführer-Daten.** opencode/MiniMax-M3.1-Flash · Kontextgrenze 400.000 (P10.5-C erfüllt) ·
kein `systemctl`, kein `sudo`, kein echter `DATA_ROOT`, kein Keyring, kein `pkill -f`;
`/opt/sharefyx/current` nur **gelesen** (Release `20261008T201607.460757Z`).

## Session stopped — 2026-10-22 (Block 6 ✅ — Anbieter: PA-1, PA-2, `/mcp` ohne Slash, PA-6)

**Ergebnis.** Die zweite Vergleichsregel ist gebaut (`http://127.0.0.1:<port>`, Port explizit, P10.5-O),
`application_type` kennt {fehlend, null, native, web}, die CSP `form-action` trägt `http://127.0.0.1:*`,
und `/mcp` wird **ohne** Slash exakt bedient (kein 307). **V209 ✅** (opencode 1.19.4), **V197 ✅**
(Chromium folgt dem Loopback-Redirect), **PA-6 ✅** (Wurzel-`CLAUDE.md`).

**Geliefert.** `clients.py` (zweite Regel + `application_type`), `config.py` (CSP), `app.py`
(`_ExactMcpMount` + `Route("/mcp")`), `CLAUDE.md` (eine Zeile), 22 neue Tests, drei Proben
(`p105_b6_dcr_probe.py`, `p105_b6_opencode_e2e.py`, `p105_b6_consent_browser.py`).

**Gemessen.** `pytest` **1376 grün** (1354 + 22) · `doc_health` 0 · `ui_budget` 5/5 · sieben Gegenläufe
wirksam · **DCR**: derselbe opencode-Request → vorher 400 `invalid_redirect_uri`, jetzt **201** ·
**V197**: Chromium folgt dem 302 auf `http://127.0.0.1:19876/…` (keine CSP-Verletzung); Gegenlauf ohne
den CSP-Eintrag: Chromium blockiert das Formular lautlos, der Callback kommt nicht an · **`/mcp` ohne
Slash**: opencode geht direkt auf `/mcp` (vorher 307 → zweiter Versuch auf `/mcp/`).

**Vier Befunde.** (1) Der Issuer-Rewrite-Proxy aus M3 ist für diese Messung **schädlich**: er schreibt
den `resource`-Parameter auf `http://…`, der Server erwartet `https://…` → opencode bricht mit
„resource stimmt nicht mit der erwarteten Ressource überein" ab. **Der Server hat recht, der Proxy
hat gelogen** — deshalb diese Messung ohne Proxy. (2) opencode 1.19.4 fährt mit
`NODE_TLS_REJECT_UNAUTHORIZED=0` **auch im OAuth-Pfad** gegen ein selbstsigniertes Zertifikat — die
M3-Messung (1.18.33) galt für 1.18.33. (3) Die MCP-Werkzeuge des `build`-Agenten sind **nicht**
standardmäßig aktiv; das Muster ist `"<server>_*"` (`sharefyx_list_spaces`). (4) **`GET /mcp` → 405**:
opencode öffnet einen SSE-Strom, unser stateless Server kennt nur POST/DELETE (P2-B). Der
Werkzeugaufruf **selbst gelingt** (eigenes Log: `ev=tool, tool=list_spaces, ok=true`), opencode setzt
die Sitzung danach aber nicht fort.

**Nächster Block:** 7 (Darstellung) — der Startauftrag mit den **heute geprüften Ankern**
steht oben in diesem Head.

**Offen / nächster Schritt.** **P10.5-26 bleibt ⬜** (siehe „Offen beim Nikinger"): der Werkzeugaufruf
ist serverseitig bewiesen, die opencode-Sitzung läuft nicht weiter — **vor** der Live-Abnahme
10-27/28 zu klären. `phase4_auth/scripts/abnahme_run.sh:110` trägt einen Kommentar zum alten
307-Verhalten (außerhalb der erlaubten Pfade → nicht angefasst). Deploy B (`v3.1.6`) steht aus
(Block 5 + 6 zusammen); die Merge-Reihenfolge entscheidet der Nikinger.

**Ein Dateigrößen-Befund (für Block 12).** Zwei lebende Dokumente stehen knapp unter der
40-KiB-Grenze: `phase2_mcp/CLAUDE.md` (40.631 B, **329 B** Luft) und
`phase10_inventory/BAUSTELLENREGISTER.md` (39.802 B, 1.158 B Luft — Block 0.8 hatte 3.386 B
freigeräumt, Block 5 hat 1.676 B verbraucht, Block 6 0.5 B). Die Blöcke 7–12 haken im Register
je Zeile ab: **ohne Rotation/Rotation der Langtexte läuft es über die Grenze.** Beide Dateien
tragen jetzt einen Kürzungs-Weg, aber **kein automatischer** — das ist Doku-Arbeit, kein
Code-Eingriff.

**Auslegung von P10.5-E (hier offengelegt, nicht stillschweigend):** die drei Probe-Dateien
liegen in `phase10_5_finishing/probes/` — der Blockkopf nennt den Ordner nicht, **Schritt 6.6 aber
den Dateinamen** (`p105_b6_opencode_e2e.py`). Weitere Eingriffe außerhalb der Blockpfade: keine.

**Ausführer-Daten.** opencode/MiniMax-M3.1-Flash (Open-Test, P10.5-B) · Kontextgrenze 400 K geprüft
(`~/.config/opencode/opencode.json`: `MiniMax-M3.1-Flash` → `limit.context` 400000) · keine Eingriffe
Nikinger · keine Claude-Code-Session in diesem Block · kein `systemctl`/`sudo`, kein echter
`DATA_ROOT`, kein Zugriff auf die echte `auth.sqlite3` oder den Keyring.

## Session stopped — 2026-10-22 (Block 5 ✅ — MCP-Schicht: PA-5 FastMCP 4, LG-4)

**Ergebnis.** `fastmcp` steht exakt auf **4.1.3** (`mcp 2.3.0`, `starlette 1.9.0`); der Server bedient
beide Protokoll-Ären (`legacy` `2025-11-25`, `auto` `2026-07-28`). Neu: Werkzeug `append_to_items`
(LG-4, Lock P10.5-J) und das Log-Feld `proto`. **V207 ✅** (Changelog 4.1.1–4.1.3: keine Änderung an
`http_app`/`Middleware`/`get_http_request`/`ToolError`/`Image`), **V219 ✅** (`Context.request_context.protocol_version`).

**Geliefert.** `pyproject.toml` (Pin + datierte Ablösung von P9-R) · `constraints.txt` neu aus frischem
venv · `request_log.py` (`proto`, `err:"partial"`) · `tools.py` (`AppendEntry`, `_append_checked` als
**ein** Schreibpfad für beide Append-Werkzeuge, `append_to_items`) · Tests: 5 `append_to_items`, 3 Log,
8 Probe-Wächter, `test_app.py` (11 Werkzeuge, snake_case), `test_step_h_deps.py` (4.1-Linie statt 3.4) ·
`mcp_smoke.py` Check 17 · `probes/p105_b5_protocol_probe.py` + JSON.

**Gemessen.** `pytest` **1354 grün** — mit Compat an, und mit `FASTMCP_MCP_CAMELCASE_COMPAT=false` +
`-W error::DeprecationWarning` · `doc_health` 0 · Smoke **17/17** · Gegenläufe alle wirksam
(`extra="forbid"`, `proto`, `partial` — auch durch den echten Stack, `mcp 2.2.0` → Constraint-Wächter rot) ·
`constraints.txt`: −22/+25 Zeilen, u. a. `mcp 1.30→2.3`, `starlette 1.7→1.9`, `Authlib 1.8→1.9.1`,
`joserfc 1.7.5→1.7.7`, `pydantic 2.14.0→2.14.1`, `certifi` neu, `truststore` neu; `cryptography`/`uvicorn`/`anyio` unverändert.

**Vier Befunde.** (1) Der dokumentierte Kopf-Befehl `sed -n '1,/^$/p' constraints.txt` kopiert die
**ganze** Datei (sie hat keine Leerzeile) — jetzt `grep '^#'`. (2) Beim Umbau von `append_to_item` rutschte
der `@mcp.tool`-Decorator auf den Hilfsfunktions-Namen: **nur** der Smoke und `test_app.py` fingen es, die
Unit-Tests rufen rohe Funktionen — Lehre: Registrierung gehört in einen Test über `tools/list`. (3) Planzeilen
waren gedriftet (`test_app.py:438–441`, `test_tools.py:1062` statt 384–387/921) und ein Wächter, den der Plan
nicht nannte (`…stays_inside_the_three_line`, plus der Kommentar-Wächter) war rot: Code gewinnt. (4) Unbekannte
Version bei `initialize` → Antwort mit der eigenen Version, **kein** Fehler (der Plantext gilt nur für die
zustandslose Ära, dort `-32022`). Nicht angefasst: `phase7_spaces_admin/scripts/p7_13_…probe.py:149` liest
`mimeType` per `getattr` (liefert unter 4.x `None`) — Wegwerf-Skript außerhalb der erlaubten Pfade.

**Ausführer-Daten.** **Abweichung:** diese Session lief als Claude Code, nicht als
opencode/M3.1 Flash — kein Modell-Trailer des Open-Tests, P10.5-C (400 K) nicht anwendbar · Wanduhrzeit nicht
gemessen · keine Eingriffe Nikinger · kein `systemctl`/`sudo`, kein echter `DATA_ROOT`, keine Wegwerf-Instanz.

**Offen / nächster Schritt.** **Dieser Stand liegt auf dem Zweig `p105-block5`, nicht auf `main`** — `deploy.sh main`
würde sonst FastMCP 4 in Deploy A mitnehmen (P10.5-R: vier getrennte Deploys; P10.5-18 messen). Ob/wann er nach
`main` geht, entscheidet der Nikinger. **Auf `main` zuerst das Dev-venv neu bauen** (`.venv` trägt `fastmcp 4.1.3`,
`main` pinnt `3.4.7` → zwei Wächter rot). Deploy A (`v3.1.5`, Block 1–4) steht aus, Deploy B nach Block 6.
P10.5-E-Prüfung: ein Treffer außerhalb der Blockpfade, `tests/test_protocol_probe.py` (Plan 5.6 nennt ihn).
**Vor Deploy B (5.7):** der Nikinger sagt Fabian Bescheid (kurzer Neustart, kein Re-Auth erwartet); live
`.venv` im Release wird mit `-c constraints.txt` gebaut. **Beim Nikinger:** P10.5-18, P10.5-22 (Connector +
Log-Feld `proto`, V208), AL-1 Zeile 15, V203, P10.5-27/28. Nächster Block: **6** (Anbieter: PA-1, PA-2, `/mcp`, PA-6).

## Session stopped — 2026-10-22 (Block 4 ✅ — Performance: PF-1, PF-4, Z1–Z4)

**Ergebnis.** `_overview()` zählt alle fünf Eimer aus **einem** `store.search()`-Durchgang
(P10.5-G) statt aus einem Aufruf je Eimer **und** je Space; `folders`/`members` wandern in
dieselbe Antwort. `asyncio.to_thread` für `_overview`, `_items_get` und `_graph_get` (Z2). Der
Client holt nur noch `/overview`; `focus`/`visibilitychange` bekommen 10 s Mindestpause (PF-4).
Neu: `static/js/loading.js` (`withLoading(el, promise, {delayMs: 200})`) + `.is-loading`-Gerüst
in `app.css` — statisch unter `prefers-reduced-motion`.

**Geliefert (Commits).** 4.1/4.2 `webui/api.py` (ein Durchgang + Rückfall über
`_STORE_FETCH_LIMIT` + `to_thread`) + 4 Tests in `phase5_ui/tests/test_overview.py` · 4.3/4.4
`static/js/{list,app,editor,graph}.js`, `static/js/loading.js` (neu), `static/app.css` +
8 Wächter in `phase5_ui/tests/test_loading_state.py` · 4.6 drei Proben unter
`phase10_5_finishing/probes/` (M2-Bench, Event-Loop, Browser).

**Gemessen** (Basis `37186d5`): `pytest` **1335 grün** · `doc_health` 0 · `ui_budget` 5/5
(176,6 KB gzip) · **M2-Bench Median 107,3 ms** (Grundlinie 2405,6 ms — 22,4×) · **Event-Loop:
`/health` hinter `/overview` 23 ms** (P10: 4757 ms), `blockade_health` false (P10: true) ·
**Browser:** `DOMContentLoaded` 142,2 ms · 150 ms → **kein** Platzhalter, 400 ms → Platzhalter
sichtbar · `/overview` 2 s verzögert: Space-Wechsel 0,315 s, Item-Öffnen 0,053 s · **dreizehn
Gegenläufe**, alle wirksam (davon zwei an der 200-ms-Grenze selbst).

**Zwei eigene Befunde.** (1) Der erste Entwurf von `withLoading()` nahm die Klasse im
`done()`-Zweig **immer** ab — bei zwei gleichzeitigen Abrufen (Poll + Schreibvorgang) hätte
der schnellere den Ladezustand des langsameren gelöscht. Jetzt läuft ein Zähler je Element
(`WeakMap`), die Klasse fällt erst beim letzten Abruf. (2) Die erste Fassung der Browser-Probe
maß **Route-Verzögerung plus Serverzeit** — die 200-ms-Grenze war damit nicht prüfbar; die
Route liefert jetzt eine **kontrollierte** Antwort (`route.fulfill`), die Serverzeit ist
ausgeschlossen.

**Ausführer-Daten.** opencode/MiniMax-M3.1-Flash · Kontextgrenze 400.000 (P10.5-C erfüllt) ·
keine Advisor-Runde · Eingriffe Nikinger/Claude Code: 0 · kein `systemctl`, kein `sudo`, kein
echter `DATA_ROOT` · Wegwerf-Instanz nur über die PID-Datei gestoppt (Hard Rule 9), Port 8799
danach frei.

**Offen / nächster Schritt.** Deploy A (`v3.1.5`) nach Block 1–4 — Badge + `UPDATE_LOG` +
`health_gate.sh` sind Nikinger-/Claude-Code-Arbeit. **Beim Nikinger offen:** P10.5-18 (Live-Messung
nach Deploy A: `/overview` Waiting ≤ 300 ms, Space-Wechsel während des Polls ≤ 1 s, beide
Eingänge), AL-1 Zeile 15 (Migration + Live-Check), V203, P10.5-27/28. Nächster Block: 5
(MCP-Schicht: PA-5 FastMCP 4, LG-4).

## Session stopped — 2026-10-22 (Block 2-Nachzug + Block 3 ✅ — RE-1-Parität, EXIF-Strip, Waisen)

**Ergebnis (Nachzug).** Der Befund aus Probe 2.5 ist geschlossen (Nikinger 2026-10-22: „ja"):
ein Item mit **neuem Ordner** in einem fremden Home-Space legt den Ordner nicht mehr an — Web
**und** MCP. Regel: `permissions.manages_space()` (eigener Space oder Team-Space mit
Schreibrecht), dieselbe wie RE-1 und RE-2. Ohne `folder` bleibt das Anlegen an der
Space-Wurzel erlaubt (P6-U). `ui_budget.py`/`ui_smoke.py` bekommen das Home-Space-Prädikat —
ohne es waren ihre `team`-Flags **immer** `false`.

**Ergebnis (Block 3 ✅).** LG-8: `files.strip_image_metadata()` (JPEG/PNG/WebP, GIF unverändert,
**fail-closed**) + Aufruf in `Store.put_asset()` — **eine** Stelle für Web und MCP. LG-7:
`scripts/asset_orphans.py` (`--report`/`--move`, **ein** Commit, nie gelöscht).

**Geliefert (Commits).** 3.1 `files.py` + 8 Tests · 3.2 `store.py` + 9 Tests + die
Dummy-PNG-Fixtures (acht Dateien in fünf Paketen → jetzt **eine** Fixture in
`phase1_storage/tests/sharefyx_image_bytes.py`, `pytest.ini` setzt `pythonpath`) · 3.3/3.4
`asset_orphans.py` + 7 Tests + `probes/p105_b3_assets_probe.py`.

**Gemessen** (Basis `725215f`): `pytest` **1316 grün** (304 s) · **Wegwerf 8799: 14/14 Zellen**
(`probes/p105_b3_assets.json`): Web 148 B → 94 B, GPS weg, Orientation 6 bleibt, ICC bleibt ·
MCP 94 B, GPS weg, Orientation 6 · sauberes Bild byte-identisch (45 B = 45 B) · Waise gefunden
(und nur sie), `--move` → Papierkorb, **ein** Commit (5 → 6), lebende Assets unberührt ·
`doc_health` 0 · `ui_smoke` 13/13 · `ui_budget` 5/5.

**Ausführer-Daten.** opencode/MiniMax-M3.1-Flash · Kontextgrenze 400.000 (P10.5-C erfüllt) ·
keine Advisor-Runde · Eingriffe Nikinger/Claude Code: 0 · kein `systemctl`, kein `sudo`, kein
echter `DATA_ROOT` · Wegwerf-Instanz nur über die PID-Datei gestoppt (Hard Rule 9), Port 8799
danach frei.

**Plan-Drift, datiert 2026-10-22.** (1) Der Plan sagt „im **Index** keine Item-Zeile" — der
Code prüft gegen die **Dateien** (Hard Rule 2): ein veralteter Index würde die Assets
**lebender** Items als verwaist melden und in den Papierkorb schieben. (2) Der Plan sah die
Proben bei Claude Code; ich habe sie selbst gefahren (stehende Erlaubnis, Wegwerf erlaubt).
(3) `pytest.ini` (eine Zeile `pythonpath`) und acht Testdateien in fünf Pakaten wurden
angefasst — die Dummy-PNG-Header waren nach 3.2 **keine Bilder mehr** (fail-closed).
(4) Die Option heißt `--git-author`, nicht `--author`: der P9-Wächter
`test_only_history_builds_the_git_author_arguments` erlaubt das Literal `--author` nur in
`storage/history.py` (dort wird der Git-Autor **gebaut**; das Skript reicht den Namen nur
durch) — der Wächter bleibt unangetastet.

**Abbruchprüfung (P10.5-E, Basis `45c507b`).** `git diff --stat` nennt neben den erlaubten
Pfaden **sechs** Dateien: `phase2_mcp/scripts/mcp_smoke.py` und fünf Testdateien — alle
**Fixture-Reparaturen** (Dummy-PNG → echte Bytes), keine Produktlogik; `pytest.ini` eine
Zeile. P10.5-F ist sauber: unter `phase1_storage/storage` nur `files.py` und `store.py`.

**Offen / nächster Schritt.** Block 4 (Performance: PF-1, PF-4, Z1–Z4) — Deploy A (`v3.1.5`)
danach. Beim Nikinger offen: AL-1 Zeile 15 (Migration + Live-Check), V203, P10.5-27/28.

## Session stopped — 2026-10-22 (Block 2.5 — Proben Web × MCP und M4; Block 2 ✅ mit einem Befund)

**Ergebnis.** Die Regel aus 2.1–2.4 hält auf einer Wegwerf-Instanz. **28 von 28** bewerteten
Zellen bestehen, und jedes ❌ scheitert mit dem **erwarteten Text** (nicht an einer älteren
Prüfung). BG-1 ist behoben. **Ein Befund:** Ein Item mit **neuem** Ordner in einem fremden
Home-Space mit `write:` anzulegen (`create_item(space=, folder=)`, Web `POST /api/v1/items`)
legt den Ordner an — auf **beiden** Flächen. Damit ist die Parität gewahrt, aber RE-1 hat eine
Hintertür. Deshalb steht P10.5-9 auf ⚠️.

**Geliefert (Commits).** Dieser Commit:
- `probes/p105_b2_rights_probe.py`: Wegwerf 8799, eigene Wurzel, Maschinerie aus
  `p10_wegwerf.py`. Seed: alpha · beta (Home B, `write: [alpha]`) · gamma (Team, write) ·
  delta (Team, nur read).
- `probes/p105_m4_bg1_probe.py`: M4 über TLS, Bestehensregel umgedreht.
- Rohwerte in den beiden `.json` daneben.

**Gemessen** (HEAD `b299968`):

| Matrix | Web | MCP |
|---|---|---|
| Ordner anlegen: eigen/Team ✅ · fremder Home mit `write:` ❌ · read-Team ❌ | ✅ | (kein Werkzeug) |
| Ordner wechseln: eigen/Team ✅ · fremder Home ❌ | ✅ | ✅ |
| Verschieben alpha→gamma ✅ (AL-1 Z. 29) · alpha→beta ❌ · beta→alpha ❌ · beta→gamma ❌ | ✅ | ✅ |
| delta schreiben ❌ · fremder Body gewrappt, eigener nicht (AL-1 Z. 14) | ✅ | ✅ |

- Jede ✅-Zelle ist von der Platte zurückgelesen (`<space>/<ordner>/<id>__*.md`).
- Jedes ❌ hat das Item an der Quelle belassen.
- **M4:** 4 s verzögert → 0 Zeilen beim Öffnen, **3 Zeilen** nach der Antwort, ohne neu zu
  öffnen. Gegenlauf ohne Verzögerung: 3.
- **Gegenlauf der Probe:** ohne `dispatchEvent` → 0 nach der Verzögerung. `list.js` ist
  danach per `git checkout` zurück.
- Prod (8765, PID 1069) unberührt; 8799 nach dem Stopp frei.

**Plan-Drift, datiert 2026-10-22** (der Plan ist 📕, deshalb steht die Drift hier):
1. P6-Zeile 14 heißt im Original „fremder Body auch im geteilten Space gewrappt"
   (`phase6_shares_plan.md:919`), nicht „Schreiben ❌". Beides ist geprüft.
2. M4 erwartet 3 statt 2 Zeilen: beta ist hier beschreibbar.
3. Die MCP-Fläche hat kein Werkzeug „Ordner anlegen".

**Ausführer-Daten.** Claude Code (Proben). Eine Advisor-Runde vor dem Bau. Eingriffe: 0.

**Offen / nächster Schritt.**
- **Nikinger:** Den Befund schließen (`create_item`/`POST /items` mit neuem Ordner nur, wenn
  `manages_space()`)? Das ist Code in `tools.py`/`api.py`. Bremst Block 3 nicht.
- **Nikinger:** Die offene Frage zu `ui_budget.py`/`ui_smoke.py` ohne Home-Space-Prädikat.
- **Ausführer (opencode) — Block 3, Startauftrag** (Plan „Block 3", §2.1–§2.2):
  - Vorher: `limit.context` ≤ 400.000 prüfen · `git status` sauber · Blockbasis = HEAD.
  - **Angekündigt hiermit (2026-10-22): P1-Öffnung 15:** `files.strip_image_metadata()` + Aufruf in
    `Store.put_asset()`. Keine weitere Datei unter `phase1_storage/storage/`.
  - 3.1 `strip_image_metadata(data, mime)` in `files.py` (JPEG/PNG/WebP, GIF unverändert,
    fail-closed `ValidationError`) · 3.2 Aufruf in `put_asset()` nach `sniff_image_mime()`
    (heute **`store.py:943`**, Plan sagt 944) · 3.3 `scripts/asset_orphans.py`
    (Docstring V162 heute `store.py:1045`) · Tests nach Plan 3.4, Fixtures als Bytes.
  - Proben P10.5-12/13 (Wegwerf) macht danach Claude Code.

## Session stopped — 2026-10-22 (Block 2 — Fehler, Parität, Regel: BG-1, RE-1, RE-2, P10-I; **2.1–2.4 gebaut**, 2.5 Proben offen)

**Ergebnis.** Die Schritte 2.1–2.4 stehen — **eine** Regel für Web und MCP, und die
Space-Liste füllt sich nach, wenn das `/overview` spät kommt.

**Die Regel.** `SharePolicy` kennt Home-Spaces (ein Space, der einem Nutzer gehört) und
Team-Spaces (ein geteilter Space, der niemandem gehört); die Policy bekommt dafür ein Prädikat
(`is_home_space`), das `mcpserver/app.py :: create_app()` aus der Auth-DB setzt
(`oauth.store.get_user(space) is not None` — Zeilenabfrage **ohne** TOTP-Entschlüsselung).
`webui/api.py :: _is_team_space()` und `_team_writer()` sind Einzeiler auf die Policy — die
Home-Space-Abfrage gibt es im Code nur noch **einmal**. Durchgesetzt: **RE-1** (Ordner anlegen
im Team-Space, Web), **RE-2** (Ordner wechseln im Team-Space, MCP), **P10-I** (kein Item
wandert in den Home-Space eines anderen) und **P10.5-N** (auch nicht **aus** einem heraus —
Nikinger 2026-10-21). **Fail-closed:** ohne Prädikat kennt die Policy **keinen** Home-Space
und damit auch keinen Team-Space — wer kein Prädikat liefert, sperrt sich selbst.

**BG-1 (2.3).** `list.js` feuert nach dem Füllen von `state.spaces` das Ereignis
`sfx:overview-loaded`; `spaces.js` hört darauf und zeichnet die Liste neu, **wenn** das Panel
offen ist (`#settings-spaces` nicht `hidden`). Der Weg läuft über ein Ereignis, nicht über einen
Import — `spaces.js` importiert `loadOverview()` aus `list.js`, ein Import zurück wäre ein
Zyklus.

**Ein Plan-Befund, datiert:** Schritt 2.4 („Tests") ist kein eigener Commit — die Tests kamen
mit ihrer Regel (2.1–2.3), sonst gäbe es einen Commit mit Code ohne Beweis. Und: die
Test-Fixtures brauchten das Prädikat **auch** dort, wo es die Regel noch nicht prüft (webui,
P7) — ohne Prädikat hätten die Web-Tests nach der Umstellung **keine** Team-Spaces mehr.

**Geliefert (Commits).** `4f6e878` — 2.1. `f4c63b6` — 2.2. `486acda` — 2.3 (BG-1). `da92731` —
Wurzel-Current-state (Block-2-Block oben, Block-1-Block per Skript rotiert).

**Gemessen.** Suite **1299 grün** (280 s). `doc_health` 0 · `ui_budget` 5/5 (173,8 KB gzip).
**Sieben Gegenläufe, alle wirksam:** alte Web-Regel → Ordner-Test rot · P10-I-Prüfung
entfernt → zwei Move-Tests rot · alte MCP-Regel → RE-2-Test rot · MCP-P10-I entfernt → zwei
Tests rot · Quellseite aus `may_move_between()` gestrichen → drei Tests rot · Ereignis aus
`list.js` entfernt → Wächter rot · Prädikat aus `app.py` entfernt → zwei Integrations-Tests
rot.

**Ein Bestandstest musste umgeschrieben werden, mit Begründung:** `test_update_item_with_space_
and_folder_together_uses_space_level_check_not_owner_guard` (2026-08-17, Advisor-Fund) schob
ein Item aus dem Home-Space `alpha` heraus — das verbietet P10.5-N jetzt. Der Testzweck (der
Eigentümer-Riegel darf einen legitimen Cross-Space-Move mit `folder=` nicht blockieren) bleibt,
die Quelle ist jetzt ein Team-Space.

**Ausführer-Daten.** **MiniMax M3.1 Flash** über opencode (P10.5-B), `limit.context`
**400.000** (P10.5-C ✅). Wanduhrzeit: rund **55 min** für 2.1–2.4 (11:44 → 12:39), davon
drei volle Suitenläufe (je ≈ 5 min) und sieben Gegenläufe. Aufrufe/Kontingent:
**nicht sichtbar**. Eingriffe: **0** vom Nikinger, **0** von Claude Code. Trailer je Commit:
`Co-Authored-By: opencode/MiniMax-M3.1-Flash <noreply@minimax.io>`.

**Offen / nächster Schritt.** **2.5 — die Proben** (Plan Schritt 2.5, **Claude Code**):
`phase10_5_finishing/probes/p105_b2_rights_probe.py` auf einer Wegwerf-Instanz (zwei Principale
+ ein Team-Space), Matrix Web × MCP, danach M4 erneut gegen die neue Instanz. Abnahme
**10-8/10-9/10-10/10-11** bleiben ⬜, bis die Probe läuft; AL-1 Zeile 15 bleibt beim Nikinger.
Danach: Deploy A (`v3.1.5`) nach Block 3–4.

## Session stopped — 2026-10-22 (Block 1 — Betrieb: BT-1, BT-2, BT-6; **✅ abgeschlossen**)

**Ergebnis.** Block 1 ist fertig: 1.1 (V199) · 1.2 (BT-1, Caddy-Blockform) · 1.3 (BT-2,
`SuccessExitStatus=143`) · 1.4 (BT-6, `constraints.txt`). Abnahme **P10.5-5 ✅ · 10-6 ✅ · 10-7 ✅**.
**Ein Plan-Befund, datiert:** die Schritte stehen als 1.1 → 1.2 → 1.3 → 1.4, aber 1.1/1.2 hängen an
Ausgaben des Nikingers, 1.3/1.4 nicht — deshalb liefen 1.3/1.4 zuerst. **Deploy A ist laut Plan „nach
Block 1–4" fällig, also nicht jetzt.**

**Geliefert (Commits).** `4fc8d9a` — 1.3 (BT-2). `52b4eec` — 1.4 (BT-6). `f3846e8` + `71e904e` — 1.1/1.2
(BT-1). `60a191a` — INDEX-Größe. (dieser Commit) — V200 abgehakt.

**V199 (1.1), Ausgabe des Nikingers auf der VPS:** `dial_timeout` 10000000000 ns (10 s) ·
`try_duration` 15000000000 ns (15 s) · `try_interval` 1000000000 ns (1 s) · `upstreams[0].dial` =
`100.93.43.122:8765` — die Plan-Annahme, und der Upstream passt zu `<heimvm-tailnet>:8765`.

**V200 (1.3), Lauf vom 2026-10-22 (Fleet-Playbook auf VM 200, `ok=11 changed=3 failed=0`):**
`sharefyx-tail-proxy` **active**, trägt `SuccessExitStatus=143`, nach dem Stopp **`Result=success`**,
**0 failed units** — genau das, was der Fleet-Healthcheck liest. Relay auf `100.93.43.122:8765`, App auf
`127.0.0.1:8765`. **Idempotenz: der zweite `--check` meldet `changed=0`.** Die alte Unit liegt als
Kopie mit Suffix `~` in `/etc/systemd/system/` (systemd liest sie nicht). **Nicht gemessen:** der
Domain-Weg während des Stopps — der Stopp-Start dauerte laut Ansible nur Sekunden, und der öffentliche
Pfad war in den Prüfschritten nicht beteiligt.

**Gemessen.** Suite **1283 grün** (308 s) auf `mcp 1.30.0` / `starlette 1.7.0`. `pip check` grün,
`doc_health` 0. **Gegenläufe, alle wirksam (Details in den Commits):** BT-1 — alte Einzeilenform ·
`dial_timeout 3s` · Direktive außerhalb des Blocks. BT-2 — Zeile fehlt · Zahl 144 · Zeile nicht unter
`Restart=on-failure` · Zeile in der MCP-Unit. BT-6 — Wegwerf-venv mit `starlette 1.3.1` · `-c`
entfernt · Abbruchblock entfernt. Die neuen Wächter laufen im **Release-venv** grün (deploy.sh:169) —
sonst bricht Deploy A.

**Ausführer-Daten.** **MiniMax M3.1 Flash** über opencode (P10.5-B), `limit.context` **400.000**
(P10.5-C ✅). Wanduhrzeit: rund **1 h 40 min** für 1.1–1.4 (10:05 → 11:45), davon vier volle
Suitenläufe (je ≈ 5 min). Aufrufe/Kontingent: **nicht sichtbar**. Eingriffe: **2** vom Nikinger
(V199-Ausgabe, V200-Lauf über Fleet), **0** von Claude Code. Trailer je Commit:
`Co-Authored-By: opencode/MiniMax-M3.1-Flash <noreply@minimax.io>`.

**Gegenlese-Funde — zwei eigene Fehler dieser Session.** (1) `cp -a .venv` kopiert die Skriptshebangs
mit — der erste Gegenlauf traf dadurch das **echte** Dev-venv (dort wurde `starlette` auf 1.3.1
heruntergesetzt). Lehre: eine venv-Kopie nur über `venv/bin/python -m pip` anfassen. (2) Die
Verhaltensprobe war grün, ohne den Abbruch zu prüfen — im PATH der Testumgebung gibt es kein
`python`, das Skript endete vorher mit „command not found"; jetzt hat die Probe einen `python`-Stub.

**Offen / nächster Schritt.** **Block 2** (Fehler, Parität, Regel: BG-1, RE-1, RE-2, P10-I, AL-1) —
Zeile 15 (AL-1) bleibt Nikinger-Arbeit. Beim Nikinger offen: der Caddy-Befehl auf der VPS (Fleet
wartet auf eine Einzelfreigabe) — **von Sharefyx wird dort nichts gebraucht**: die Live-Config trägt
die Werte bereits, und die Quelle zieht jetzt nach.

## Session stopped — 2026-10-22 (erster Block: Block 0 — Haushalt und Vorbereitung, **abgeschlossen**)

**Ergebnis.** Block 0 abgeschlossen, **DO-2 vollständig erledigt:** Karte `docs/INDEX.md` 37.946 B (3.014 B Luft gegen 40.960 B, vorher 188 B), Register 37.574 B (3.386 B Luft, vorher 6 B), ROADMAP-Wächter P9-6 eingefroren. **Ein Plan-Befund:** der Hebel des Plans (die acht Abschnittsköpfe, zusammen 2.478 B) hätte allein **nicht** gereicht — die geforderten 3.000 B waren daraus nicht erreichbar; der Zielwert blieb, der Hebel wurde erweitert (zwei Abweichungen im Plan-Nachtrag).

**Geliefert (Commits).** `d5f6081` — 0.5: Skript `shorten_index_headings.py` (vier Gegenproben) + Archiv `docs/INDEX_KURZUNG_ARCHIVE.md`, Karte 40.772 → 36.601 B. `3e15f9e` — 0.8: §12 des Registers verbatim nach `phase10_inventory/ENTSCHEIDUNGEN_ARCHIVE.md`. `f7ad5d9` — 0.4: P9-6 eingefroren + Gegenprobe, DO-2 → `✅ 10.5-2 (B0)`. `3586566` — 0.2/0.3: Phase-Head, `SESSIONS_ARCHIVE.md`, DO-3-Wächter, `pytest.ini`. `9ad1c22` — 0.6/0.7: ROADMAP-Zeile + 🔄, Kette rotiert, Ausführer-Vorbedingung protokolliert.

**Gemessen.** `doc_health` **0**; volle Suite **1268 → 1270 → 1279 grün** (289/284/281 s). Neu: `test_index_shortening.py` **5/5** (Rundeweg byteweise, Abbruch ohne Zielberührung) und `test_head_rules.py` **4/4** (ein Session-Block ≤ 4 KiB, Gegenprobe mit 5-KiB-Block).

**Ausführer-Daten.** Modell **MiniMax M3.1 Flash** über opencode (P10.5-B, Open-Test) — wirksamer `limit.context` **400.000** (`~/.config/opencode/opencode.json`, für `MiniMax-M3` und `MiniMax-M3.1-Flash`), von eurofyx-fleet gesetzt (Neustart 22.10.); **P10.5-C ist erfüllt**, Block 1 darf starten. Aufrufe/Kontingent: **nicht sichtbar**. Wanduhrzeit: rund **2 h** für 0.1–0.8. Eingriffe: **1** vom Nikinger (Rollenfrage; Antwort: ich baue Block 0 selbst — die Abweichung von Lock P10.5-D ist datiert festgehalten), **0** von Claude Code. Trailer je Commit: `Co-Authored-By: opencode/MiniMax-M3.1-Flash <noreply@minimax.io>`.

**Gegenlese-Funde.** (1) der Plan-Hebel zu klein (oben); (2) ein falsch gebauter `updated:`-Faden im Plan („ | updated: 2026-10-21") — vom Wächter `test_updated_chain.py` gefangen; (3) ein Syntaxfehler im eigenen Skript (ein gerades `"` in einem deutschen Zitat); (4) ein Test rot nach der Kürzung der Archiv-Größe (45.703 B stand in der Abbildung statt 46.456 B); (5) **ein Paketnamenskonflikt:** `phase10_5_finishing/tests/__init__.py` (vom Plan verlangt) heißt das Modul `tests` — wie `phase3_edge/tests` —, die Sammlung brach mit `ModuleNotFoundError` ab, gelöst mit `phase10_5_finishing/__init__.py`; (6) **für Block 12:** die `updated:`-Kette der Wurzel-`CLAUDE.md` trägt **20.532 B von 33.226 B** (am 2026-09-13 rotiert: 47.094 → 23.007 B, seither wieder gewachsen) — unter der Grenze, aber dieselbe Form wie LG-6.

**Offen / nächster Schritt — Block 1 (Betrieb: BT-1, BT-2, BT-6).** Start mit **1.1 V199** (Ausgabe des Nikinger): `curl -s localhost:2019/config/ | python3 -m json.tool | grep -nE 'dial_timeout|try_duration|try_interval' | head -20` auf dem VPS — erwartet 10 s / 15 s / 1 s; weicht ein Wert ab, zieht die Vorlage die **Live**-Werte nach. Danach: **1.2** `phase9_hardening/step_a/Caddyfile.template:65` → Blockform; drei Tests in `test_tail_proxy.py` lernen sie (`:294`, `:325`, `:389`), neu `test_the_upstream_block_carries_the_fleet_timeouts()`. **1.3** `phase3_edge/systemd/sharefyx-tail-proxy.service`: `SuccessExitStatus=143` unter `Restart=on-failure` + Test; **Installation ist Nikinger-Arbeit** (Hard Rule 9), danach V200. **1.4** `pip freeze --exclude-editable` aus `/opt/sharefyx/current/.venv` (lesbar, gemessen) → `constraints.txt`; `scripts/dev_install.sh` mit `-c`; Wächter in `test_step_h_deps.py`; **Dev-venv neu aufsetzen** (vorher sichern, danach volle Suite). Erlaubte Pfade: Plan §3. **Danach Deploy A (`v3.1.5`)** — Badge, `docs/UPDATE_LOG.md`, Commit, `deploy.sh` **durch den Nikinger**, `health_gate.sh` mit echter Ausgabe (Plan §2.5). Abnahme P10.5-5/6/7.

