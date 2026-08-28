---
status: snapshot
purpose: Abschluss-Handover P7→P8 — Status, Delta seit dem P6.5-Handover, Abnahmestand (P7-1–P7-24), offene Entscheidungen, [VERIFY]-Bilanz V71–V80, P1-Contract, geänderte Arbeitsweise
read-when: vor der Planung von Phase 8 einmal ganz lesen — ersetzt das Nachlesen des Phase-7-Heads für alles außer der Detailhistorie
detail: L2
up: ../../ROADMAP.md
down:
  - ./phase7_spaces_admin_plan.md                  # Entscheidungen P7-A–P7-W, N1–N10 in §0.1 — Herkunft, nicht Ergebnis
  - ../../phase7_spaces_admin/CLAUDE.md            # Modul-Status, Abnahmestand mit Belegtexten, aktueller Session-Block
  - ../../phase7_spaces_admin/SESSIONS_ARCHIVE.md  # volle Phasenhistorie, verbatim, newest-first
  - ./PHASE6_5_CLOSEOUT_HANDOVER.md                # Vorgänger; P6.5-Herkunft
updated: 2026-08-28
---
# Phase 7 — Closeout-Handover (P7 → P8)

> **Für den kalten Leser, ohne Beschönigung.** Phase 7 ist **live deployt**
> (`main`@`e88a624`, 2026-08-27) und **✅ live-verifiziert**: die Abnahmematrix ist
> **vollständig durchgelaufen** — 24 von 24 Zeilen wurden real geprüft, **22 bestanden, 2 sind
> ❌**. Das ist die Kategorie, die P7 von P6 (27 Zeilen nie getestet) und P6.5 (13/14, eine Zeile
> strukturell unprüfbar) unterscheidet, und der Grund für den Glyph.
>
> **Der Sprung auf ✅ ist eine Nikinger-Entscheidung vom 2026-08-28**, getroffen in Kenntnis des
> Präzedenzfalls (P3 13/13, P4 16/16, P5 20/20 waren jeweils 100 %). Bedingung dieser
> Entscheidung: **die beiden ❌ verschwinden nicht, sie werden als benannte Defekte an Phase 8
> vererbt** — §4.1 und §4.3 dieses Dokuments sind der Ort, an dem sie stehen.
>
> **Was Phase 8 als erstes wissen muss:** es gibt einen **echten Mechanismus-Defekt** (P7-24,
> TOTP-Replay im Batch-Verschieben) und einen **Datenintegritäts-Fund aus dem Live-Betrieb**
> (`spacectl.py remove-space` reindiziert nicht — hat am 2026-08-27 real jeden Login mit einem
> `500` beantwortet). Beide sind klein zu beheben und beide sind noch nicht behoben.

---

## 1 Status in fünf Sätzen

1. **Alle vier Blöcke sind gebaut und live** — Step 0 (Haushalt/Doku-Audit), Block A (Fixes +
   formaler Abschluss von Phase 6.5), Block C (Space-Verwaltung in der Weboberfläche), Block B
   (Mehrfachauswahl). Die Fall-Reihenfolge A > C > B musste nie in Anspruch genommen werden.
2. **Ein Mensch verwaltet seine Spaces jetzt im Browser** — anlegen, Mitglieder hinzufügen und
   entfernen, Space entfernen; volle `spacectl.py`-Parität, Home-Spaces vom Anlegen/Entfernen
   ausgenommen. Das war die seit P6 Step 7 Commit 6 in `app.html` reservierte Phase-7-Fläche.
3. **Der P1-Contract wurde zweimal geöffnet und ist mit dieser Phase zweimal geschlossen** —
   `acl.py` bekam eine Schreibseite (sechste Öffnung), `store.move()` erlaubt den Space-Wechsel
   eines bereits archivierten Items (siebte, während der Phase auf Nikinger-Entscheidung
   nachgezogen). Details: §6.
4. **Der dritte Principal `testnutzer-p7` hat getan, wozu er angelegt wurde, und ist entsorgt** —
   er hat den Fall „Empfänger mit item-level Share ohne jede Space-Mitgliedschaft" real
   durchgespielt, den Fabian strukturell nie zeigen konnte. Damit sind auch die P6-Zeilen 36/37
   geschlossen (datierte Korrektur in `phase6_shares/CLAUDE.md`).
5. **904 Tests grün, Tabu-Diff über die gesamte Phase leer** — `mcpserver/asgi.py`,
   `mcpserver/{server,permissions}.py` und die fünf `authserver/`-Kryptomodule wurden nie
   angefasst, obwohl diese Phase eine Rechteverwaltungsfläche gebaut hat.

---

## 2 Delta seit dem P6.5-Handover

| Was | Wo im Code | Bemerkung |
|---|---|---|
| ID sichtbar und **per ID auffindbar** | `webui/api.py :: _items_get`, `editor.js :: idChip()` | ID-Lookup an der API-Fläche, nicht in `store.search()` (P7-D); ignoriert Space-/Ordnerfilter (P7-E); ohne Leserecht `total: 0`, nie 403/404 |
| Bild-Entfernen-Knopf | `editor.js :: renderAssetStrip()`, `markdown.js` (`assetIds`) | schließt P6.5-12; ohne den `assetIds`-Schlüssel hätte ein entferntes Bild ein kaputtes `<img>` gerendert statt Alt-Text |
| Feld-Whitelist an `PATCH` | `webui/api.py :: _PATCH_FIELDS` | schließt **O6**; Prüfung vor jeder Rechteprüfung; Zurückweisung ist `422`, nicht `400` |
| Sichtbarkeits-Migration live | `migrate_visibility.py --apply` | 73/73 Items, 3 Commits, 0 Dateien ohne `visibility:` |
| Sechste Contract-Öffnung: Schreibseite `.share.yml` | `storage/acl.py` | Extraktion aus `spacectl.py`, die 20 bestehenden `test_spacectl.py`-Tests blieben unverändert grün (Regressionsbeweis) |
| Siebte Contract-Öffnung: archiviertes Item wechselt den Space | `storage/store.py :: move()`, `_write_item_file()`, `create()` | ersetzt einen fail-closed-Riegel, der jeden Space mit Nutzungshistorie dauerhaft unentfernbar gemacht hätte |
| Fünf REST-Routen für Space-Verwaltung | `webui/api.py` (`_spaces_post`, `_space_members_get/post`, `_space_member_delete`, `_spaces_delete`), `webui/shares.py :: require_space_reauth()` | Re-Auth beim Hinzufügen, keins beim Entfernen (P6-N); Entfernen eines Space verlangt Re-Auth **und** getippten Namen (P7-N) |
| Elftes JS-Modul | `webui/static/js/spaces.js` | kein Anbau an `dialogs.js` (P7-Q); `space_admin_enabled` Default `False`→`True`, Kill-Switch wirkt server- **und** menüseitig |
| Mehrfachauswahl | `state.js`/`list.js`/`dialogs.js`/`tree.js`/`toasts.js`/`app.html` | reiner Frontend-Schnitt (P6-AL) — `webui/api.py` bewusst unangetastet, kein neuer Endpunkt, kein neues MCP-Tool (P7-T) |
| Testhelfer für den dritten Principal | `phase7_spaces_admin/scripts/testcred.py` + sieben Live-Probe-Skripte | hart auf `testnutzer-p7`/`nikinger-space` verdrahtet (P7-W); Keyring-Eintrag mit `purge` entfernt |

**Nicht angefasst:** `mcpserver/tools.py` außer **Beschreibungstexten** (P7-T), `mcpserver/app.py`
gar nicht, `store.search()`s Haystack unverändert (P7-D).

---

## 3 Abnahmestand (P7-1–P7-24 plus P7-12b, Stand 2026-08-28)

**Statusregel wie in P4/P5/P6/6.5: ✅ heißt live-verifiziert durch einen Menschen (oder einen
gebilligt substituierten Testprincipal), nicht „gebaut".** Volle Belegtexte je Zeile:
`phase7_spaces_admin/CLAUDE.md` §„Abnahmestand" — hier nur die Bilanz.

| Bereich | Zeilen | Stand |
|---|---|---|
| Block A — ID/Bilder/Whitelist/Migration/Purge/Testprincipal | P7-1 … P7-13, P7-12b | **12 ✅, 1 ❌** (P7-4) |
| Block C — Space-Verwaltung | P7-14 … P7-22 | **9 ✅** (P7-20 mit Vorbehalt, s. u.) |
| Block B — Mehrfachauswahl | P7-23, P7-24 | **1 ✅, 1 ❌** (P7-24) |
| **Summe** | **24 (+P7-12b)** | **22 ✅ · 2 ❌ · 0 ungeprüft** |

Drei Zeilen brauchen eine Erläuterung, damit sie nicht falsch gelesen werden:

- **P7-20 ✅ mit Vorbehalt.** Der Vorlauf-Blocker „ein nicht schreibbares Item verhindert die
  Entfernung" ist mit echten `.share.yml`-Daten **unerreichbar** — `AclReader.grants_for_dir()`
  unioniert immer den Space-Root-Grant, ein P7-L-autorisierter Ausführender darf damit jedes Item
  im Space. Der Test beweist den Pfad über eine simulierte Divergenz. Der zweite Teil derselben
  Zeile (bereits archiviertes Item) ist dagegen real erreichbar und eigenständig getestet.
- **P7-9** wurde kalendarisch geblockt, nicht technisch: das 30-Tage-Fenster für `token_families`
  öffnete erst am 2026-08-28. Ergebnis: 35→31. `clients` bleibt bei 54, bis das 90-Tage-Fenster
  am **2026-10-27** öffnet — das ist erwartetes Verhalten, kein offener Punkt, aber ein Datum,
  das eine spätere Phase gegenprüfen kann.
- **Geerbt und in dieser Phase nicht adressiert:** P6-Zeilen 7, 9, 14–17, 23, 25, 29, 30 sowie
  P6.5-14. **Kein stilles Abhaken** — sie stehen unverändert offen, siehe §4.5.

---

## 4 Offene Entscheidungen für die Planung von Phase 8

### 4.1 P7-24 — TOTP-Replay im Batch-Verschieben (echter Defekt, Kopfpunkt)

`list.js :: moveSelectedItems()` ruft `PATCH /api/v1/items/{id}` sequenziell je Item auf und
reicht dabei **dasselbe** `credentials`-Objekt (ein Passwort, **ein** TOTP-Code) an jeden
Request durch. Der Server lehnt den wiederverwendeten Code korrekt als Replay ab — jedes zweite
und weitere re-auth-pflichtige Item einer Runde scheitert deshalb **strukturell**, nicht
zufällig. Das Zweirunden-Design aus P6-AM degeneriert real Richtung „bis zu N Runden".

Das gezeigte Formular ist korrekt („2 von 2 benötigen Passwort und Code", **ein** Dialog) — der
Defekt sitzt eine Ebene tiefer im Mechanismus. Vom Nikinger am 2026-08-27 als echter Defekt
anerkannt, Fix ausdrücklich in die nächste Phase verschoben.

Drei Fix-Optionen liegen ausformuliert im Phase-Head (P7-24-Zeile), **keine davon ist gewählt**:
(a) TOTP-Fenster serverseitig innerhalb eines Batches tolerant machen — schwächt Anti-Replay,
riskant; (b) Client wartet auf einen neuen 30-s-Tick und fragt pro Fenster einmal — langsam;
(c) das Kriterium selbst nachschärfen und die Realität ehrlich dokumentieren.

**Das ist eine Nikinger-Entscheidung, keine Claude-Ableitung.**

### 4.2 `spacectl.py remove-space` reindiziert nicht — Datenintegrität, nicht Komfort

`_cmd_remove_space()` löscht über `acl.remove_space_dir()` nur das Verzeichnis; der SQLite-Index
wird **nie** angefasst. Der P7-12-Abbau von `testnutzer-p7` hinterließ dadurch Karteileichen im
Index — jede Anfrage, die sie berührte (`GET /api/v1/overview` iteriert über alle Buckets),
antwortete mit `500`, **für jeden eingeloggten Nutzer**. Behoben wurde der Zustand am 2026-08-27
mit `space_cli.py reindex` (durch Hard Rule 2 vorab autorisiert, 78 Items, 0,044 s).

**Die Ursache ist nicht behoben.** Jeder künftige `remove-space --force`-Lauf reproduziert sie.
Offene Entscheidung: automatischer `store.rebuild_index()`-Aufruf am Ende von
`_cmd_remove_space()` (ein Zweizeiler, dieselbe Datei) **oder** nur eine Warnmeldung („führe
danach `reindex` aus"). Der Phase-7-Head stuft das als kleinen, in-scope Fix ohne eigene
Planungsrunde ein.

**Anmerkung für die Planung:** dieselbe Lücke betrifft die neue Weboberfläche nicht —
`_spaces_delete` bewegt jedes Item einzeln über `store.move()`/`store.archive()`, der Index bleibt
dabei konsistent. Der Fund ist **CLI-spezifisch**.

### 4.3 P7-4 — Claude nennt Menschen gegenüber IDs statt Titeln

Die Prosa-Anweisung („Nenne einem Menschen gegenüber immer den Titel eines Items, nicht seine
`itm_…`-ID") steht seit A2 wortgleich in vier Tool-Beschreibungen. Sie hielt in einer organischen,
ungestellten Probe **nicht**: auf „welche 3 Items sind die aktuellsten" kam eine Tabelle, deren
Item-Spalte jede Zeile mit der rohen ID einleitete. Kein Code-Fehler; die Vermutung ist, dass
`search_items`' eigenes Rückgabefeld `id` als Zeilenanker naheliegt.

Offen: ob die Beschreibung geschärft, das Rückgabeschema geändert (teurer, berührt den Contract)
oder der Befund als Modellverhalten hingenommen wird. **Ein Datenpunkt, kein Muster** — eine
zweite Probe vor einer Entscheidung wäre billig.

### 4.4 Zwei bewusst akzeptierte Konsequenzen, die weiterhin gelten

- **Selbstaussperrung** (§0.4 Punkt 1 des Plans, Folge aus N7): das letzte `write:`-Mitglied darf
  sich selbst aus einem Space entfernen; der Space ist danach über die Weboberfläche für niemanden
  mehr verwaltbar. **Kein Guard, bewusst.** Rückweg: `spacectl.py add-member <space> <user>
  --write` im Terminal. Nicht stillschweigend nachrüsten — das war eine Entscheidung, kein
  Versehen.
- **Beim Entfernen eines Space stirbt die Space-Zuordnung**, nie ein Item (N8). Was mit dem
  `rmtree` fällt: `_trash/`-Inhalte und verwaiste `_assets/`-Verzeichnisse. Beides ist per
  Definition Müll und lebt in der Git-Historie des `DATA_ROOT` weiter.

### 4.5 Geerbtes Ledger — unverändert offen, damit nichts still verschwindet

| Posten | Herkunft | Stand |
|---|---|---|
| **P6-Zeilen 7, 9, 14–17, 23, 25, 29, 30** | P6 | offen, in P7 nicht adressiert |
| **P6.5-14** — Nikingers eigene Bewertung der Upload-Ankündigungsdisziplin | 6.5 | strukturell offen, kein Testlauf kann es schließen |
| **Glyph-Entscheidung P6 (🟡) und P6.5 (🟡)** | P6/6.5 | beide unverändert offen; P6.5 steht inzwischen bei **13/14** |
| **O4** verwaiste Assets · **O5** kein EXIF-Strippen · **O7** leere Ordner überleben einen Move | P6 | offen; P7 hat keinen davon angefasst |
| **`_trash/`-Räumung** | 6.5 | bewusst nicht automatisiert; mittelfristig eigene Lösung nötig |
| **V12/V49** Uplink-Datenlimit | P3/P6 | offen seit Phase 3, nie bewertet |
| **V64** claude.ai-Verhalten bei `destructiveHint: True` | 6.5 | offen, Client-Verhalten |
| **`filename`-Persistenzfrage** · **`test_authctl.py`-Flake** | 6.5 | offen; bei einem roten Lauf **zuerst prüfen, ob es der Flake ist** |
| **Funnel-Watchdog / Selbstheilung** | P3 | bewusst offene Entscheidung, kein Auftrag |
| **`GET /api/v1/overview` kostet ~440–490 ms**, alle 20 s gepollt | P6-S | bekannte Kostenstelle, kein Auftrag |
| **Kein UI-Rückweg aus einem geteilten Space** | P6 | „kein Bug, nicht blockierend", bleibt so |
| **O6** unbekannte Frontmatter-Schlüssel | `ITEM_MOVE_PLAN.md` §112 | **geschlossen durch A4** |

**Was P7 ausdrücklich draußen ließ und was dadurch nicht Phase 8 verpflichtet:** FastMCP-4-Umstieg
(P5-C reserviert eine eigene Mini-Phase), `owner:`-Feld (N7 schließt es aus), Löschen von Items
(F2, seit P5 draußen), Rechteverwaltung über MCP-Tools (P6-M), Body-Volltextsuche in der Web-UI
(Q1 aus `GLOBAL_SEARCH_PLAN.md`), Mehrfachauswahl für andere Aktionen als Verschieben.

---

## 5 `[VERIFY]`-Bilanz (V71–V80)

**Nummernkreis-Hinweis:** die Frontmatter des Plans nennt „V71–V79", das Register in §7 desselben
Dokuments führt **V80** zusätzlich auf. Der Registereintrag ist maßgeblich; die
Frontmatter-Zeile ist eine Zählfehler-Drift aus der Planungssession. Der 📕-Snapshot bleibt
unverändert, diese Zeile ist die Korrektur.

| # | Frage | Status |
|---|---|---|
| V71 | Realer `pytest`-Ausgangsstand (Erwartung 828) | ✅ geschlossen — real 828, Step 0.1 |
| V72 | Muster, wie `test_tools.py` an Tool-Beschreibungen kommt | ✅ geschlossen — Muster aus 6.5 übernommen, `test_tool_descriptions_tell_the_agent_to_name_titles_not_ids` |
| V73 | Was `markdownToHtml()` mit einer `asset:`-Referenz ohne Asset macht | ✅ geschlossen — rendert ein **kaputtes `<img>`**, deshalb der `assetIds`-Schlüssel in A3 |
| V74 | Welche Schlüssel die UI im PATCH-Body sendet | ✅ geschlossen — **`format` fehlte im Plan-Entwurf**; ohne die Korrektur hätte A4 jedes UI-Speichern mit 422 gebrochen |
| V75 | Bindestrich im Space-Namen | ✅ geschlossen gegen eine Wegwerf-Instanz — Anlegen/Schreiben/Suchen alle unauffällig |
| V76 | Wie `UserDirectory` nach der Existenz eines Principals gefragt wird | ✅ geschlossen — `users.get(space) is not None` (`webui/api.py`), Methode übernommen, keine erfunden |
| V77 | `ui_budget.py --json` nach dem elften JS-Modul | ✅ geschlossen — Pre-Deploy-Lauf 2026-08-27, `all_within_budget: true` |
| V78 | `_STORE_FETCH_LIMIT` weiterhin 5000, `search()`s `total` unabhängig von `limit` | ✅ geschlossen — Wert bestätigt (`api.py:145`, Plan nannte 144); **Nebenbefund: `total` zählt archivierte Items mit** — genau daraus entstand die siebte Contract-Öffnung |
| V79 | MCP-Revision `2026-07-28` / `fastmcp 4` | **offen, bewusst** — laut P5-C eine eigene Mini-Phase; der Connector spricht weiterhin `fastmcp 3.4.4` und funktioniert |
| V80 | Keyring aus der Claude-Code-Umgebung les- und schreibbar | ✅ geschlossen — `testcred.py store/password/totp/purge` liefen über die gesamte Phase real |

**Einziger offener Marker: V79.** Er ist kein Restrisiko dieser Phase, sondern eine reservierte
Aufgabe (P5-C).

---

## 6 P1-Contract — beide Öffnungen dieser Phase geschlossen

| Öffnung | Was | Stand |
|---|---|---|
| **sechste** | Schreibseite von `.share.yml` in `storage/acl.py` (`read_share_file`/`write_share_file`/`add_member`/`remove_member`/`create_space`/`remove_space_dir`/`spaces_referencing`/`AclWriteError`) | **geschlossen mit dieser Phase** |
| **siebte** | `store.move()` erlaubt reinen Space-Wechsel archivierter Items; `_write_item_file()` routet sie ins Ziel-`_archive/`; `create(status="archived")` setzt `folder=""` | **geschlossen mit dieser Phase** |

Beide Schließungen sind in `phase1_storage/CLAUDE.md` §„Geerbte Contracts" datiert vermerkt, im
selben Commit wie dieser Handover. **Es ist derzeit keine achte Öffnung angekündigt** — anders als
beim P6.5-Handover, der die sechste bereits offen weiterreichte. Jede Phase-8-Arbeit an
`storage/` braucht eine **neue, benannte** Öffnung; kein stiller Anbau.

`phase6_shares/tests/test_characterization.py` (drei Golden Files, P6-D/P7-C) blieb über alle
`storage/`-Umbauten dieser Phase byte-identisch grün. Diese Regel gilt unverändert weiter.

---

## 7 Geänderte Arbeitsweise ab Phase 8 (Nikinger-Vorgabe, 2026-08-28)

Sharefyx übernimmt als letztes Projekt die in anderen Projekten bereits eingefahrene Teilung:
**Claude Code (Opus) plant und löst sehr schwierige Bugs; die Ausführung läuft in opencode
(Minimax M3 Thinking).** Eigene Messungen oder Vergleichsläufe dafür sind ausdrücklich **nicht**
nötig — die sind in den anderen Projekten über ganze Meta-Phasen entstanden.

**Was das für den P8-Plan bedeutet, konkret:**

- Der Plan wird für einen **ausführenden Agenten geschrieben, der nicht mitgeplant hat**. Das ist
  keine neue Anforderung — die P7-Plan-Kopfzeile („so geschrieben, dass nichts neu hergeleitet
  werden muss: exakte Funktions- und Typnamen, `Datei:Zeile`-Anker, Testliste") war bereits genau
  das. Sie wird jetzt nur härter bindend.
- **Anker gegen den echten Code prüfen bleibt Pflicht des Ausführenden.** In P7 wichen die
  Zeilennummern in C1/C2/C4 jedes Mal um wenige Zeilen ab, die Funktionsnamen nie. Diese Regel hat
  sich dreimal bewährt und gehört unverändert in den P8-Plan.
- **Der Advisor-Call vor jedem Commit ist die Qualitätsstufe, die in dieser Phase am meisten
  gefunden hat** — mindestens elf echte Funde, mehrere davon Blocker (ungeschützter
  `GET .../members`, eingefrorene Re-Auth-Fassung gegen den falschen Space, nicht eingefrorenes
  Batch-Ziel, `ValidationError` mitten im Space-Entfernen-Durchlauf). Wie diese Stufe im
  opencode-Ablauf abgebildet wird, ist eine **offene Frage an die P8-Planung**, keine erledigte.

---

## 8 Was dieser Handover nicht enthält

Keine Implementierungsdetails, die bereits im Code, in den Tests oder im Plan stehen. Wer die
volle Herleitung eines Fundes braucht — die beiden Advisor-Runden vor C2, die Root-Cause-Analyse
des Browser-Harness-Problems, den Git-Zwischenfall vom 2026-08-25 mit acht 0-Byte-Objekten, die
Cookie-Kollision zwischen zwei Tabs derselben `claude-in-chrome`-Session — findet sie in
`phase7_spaces_admin/SESSIONS_ARCHIVE.md`, verbatim und newest-first.
