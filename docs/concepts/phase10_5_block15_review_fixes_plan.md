---
status: live
purpose: Plan P10.5 Block 15 — die Fixes aus dem Ultra-Review v4.0.0 (B1–B10), je Befund ein Wächter und ein Gegenlauf, vor Deploy D. Der Dienst darf nie an Daten scheitern, und eine Eingabe wird nie zum Pfad.
read-when: vor dem Bau eines Fix-Schritts 15.x, oder wenn ein Befund B1–B10 des Reviews zitiert wird
detail: L2
up: ../../phase10_5_finishing/CLAUDE.md
down:
  - phase10_5_ultra_review_v4.0.0.md                    # 📕 der Bericht, verbatim — die Befunde B1–B22
  - phase10_5_block14_7_plan.md                         # 📗 Muster dieses Plans (Schritte, Tor, Anmerkungen)
  - ../../phase1_storage/storage/store.py               # Kern: `_asset_matches()`, `rebuild_index()`, Rename-Wiederaufnahme
  - ../../phase5_ui/webui/api.py                        # REST: Typprüfung, Mitglieder-Routen
  - ../../phase2_mcp/mcpserver/tools.py                 # MCP: Space-Name, `offset`
updated: 2026-10-30 (Schritt 15.2 gebaut, Opus — B2/B3/B20 geschlossen, E2 wie empfohlen; Fund: doppelte `links:` = derselbe Startblocker) | 2026-10-30 (E1 Hotfix ja, E4 Opus — Nikinger) | 2026-10-30 (Entwurf + Schritt 15.1 gebaut, Claude Code — B1 geschlossen, am Code bestätigt und per Gegenlauf bewiesen)
---
# P10.5 Block 15 — Die Fixes aus dem Ultra-Review

> **Auftrag (Head, 2026-10-30):** „Plan + Fixes B1–B10 vor Deploy D; je Befund Wächter + Gegenlauf."
> Der Bericht ist eine **Aussage der Review-Session** (R = reproduziert, C = am Code belegt,
> V = vermutet). Dieser Plan **übernimmt keine Aussage ungeprüft**: jeder Schritt beginnt damit,
> den Befund am Code **nachzuvollziehen** (Hard Rule: Code ist die Quelle der Wahrheit).

## §0 Befund-Stand (was am Code gegengelesen ist)

| Befund | Review | Am Code gegengelesen | Stand |
|---|---|---|---|
| B1 asset_id → `glob()` | kritisch, R | **ja** (2026-10-30): `store.py :: get_asset/delete_asset`, `ASSET_ID_RE` nur beim Upload | **✅ 15.1 gebaut** |
| B15 `asset_id="*"` | niedrig, R | **ja** — fällt mit B1 | ✅ 15.1 |
| B2 Rename-Marker | hoch, R | **ja** (2026-10-30): reproduziert, `os.rename` ohne Elternordner, Wiederaufnahme wirft in `Store.__init__` | **✅ 15.2** |
| B3 fremde `.md` leert Index | hoch, R | **ja**: reproduziert, 0 von 3 indiziert, frischer Start wirft `FrontmatterError` | **✅ 15.2** |
| B20 CRLF = kein Frontmatter | niedrig, R | **ja**: reproduziert | **✅ 15.2** |
| B5 Nicht-String-Tags/Titel | hoch, R | offen — bei 15.3 | ⬜ |
| B8 REST ohne Typprüfung | mittel, R/C | offen — bei 15.3 | ⬜ |
| B4 Mitglieder fremder Home-Spaces | hoch, R | offen — bei 15.4 | ⬜ |
| B6 Space-Name ungeprüft | mittel, R | offen — bei 15.5 | ⬜ |
| B7 Titel-Länge → Dateiname | mittel, R | offen — bei 15.5 | ⬜ |
| B9 Einladungs-Token im Log | mittel, R | offen — bei 15.6 | ⬜ |
| B10 `search()` ohne Lock | mittel, R | offen — bei 15.6 | ⬜ |
| B11–B22 (ohne B15/B20) | mittel/niedrig | **Backlog** (Review-Empfehlung); B12 (Performance) ist kein Fix-Schnitt, sondern ein Messauftrag | ⬜ |

## §1 Das Prinzip — zwei Sätze

1. **Eine Eingabe wird nie zum Pfad.** Jede ID, jeder Space-Name, jeder Titel, der in einen
   Dateinamen oder Glob fließt, geht durch **eine** Prüfung an **einer** Stelle im Kern
   (`Store`/`files`) — nicht je Adapter eine Kopie, die auseinanderläuft. Die Adapter dürfen
   zusätzlich früh ablehnen (bessere Fehlermeldung), verlassen sich aber nicht darauf.
2. **Der Dienststart scheitert nie an Daten.** Eine von Hand editierte Datei (Phase-1-Mission: der
   Mensch darf im Verzeichnis arbeiten), ein liegengebliebener Marker, ein CRLF-Zeilenende dürfen
   **eine** Datei kosten — nie den Index und nie den Start. Fehler je Datei: fangen,
   `logger.critical` mit Pfad, weiter (Muster: `_rewrite_space_frontmatter`).

## §2 Entscheidungen

| # | Entscheidung | Wer | Stand |
|---|---|---|---|
| **E1** | **B1 als Hotfix vorab live, oder mit Deploy D?** B1 steht seit 2026-08-20 im Live-Dienst (live: Release `20261023T165838…` = Deploy B, SHA `e5c834e`, am Symlink `/opt/sharefyx/current` gelesen). **Wichtig: `deploy.sh main` ist KEIN Hotfix** — `main` trägt alles seit `v3.1.6` (u. a. `rename_folder`, den Pfad hinter B2) und damit genau das, was das Review „nicht freigabefähig“ nannte. **Weg:** Branch ab `e5c834e`, nur die Code- und Testdateien des Fixes (Doku-Hunks lassen sich nicht auf den alten Stand übertragen), eigener `docs/UPDATE_LOG.md`-Eintrag und eigene Version (**Versionsstufe = Entscheidung des Nikingers**), dann `deploy.sh <ref>` — das Skript nimmt jede Git-Ref. **Bewiesen (2026-10-30, Wegwerf-Worktree auf `e5c834e`):** der Fix-Patch (Store, Files, 4 Testdateien) lässt sich sauber anwenden, die 50 Asset-Tests sind grün, ohne den Fix sind dieselben 9 Wächter rot — der Fehler steckt also auch im Live-Stand. **Empfehlung: Hotfix.** Der Deploy läuft beim Nikinger (Hard Rule 9). | **Nikinger** | ✅ 2026-10-30: **Hotfix, ja** — Branch `hotfix-b1` ab `e5c834e` vorbereitet, Deploy + Version beim Nikinger |
| **E2** | B3: eine nicht parsebare Datei wird **übersprungen + `CRITICAL` mit Pfad** (Empfehlung) statt den Neuaufbau abzubrechen. Folge: so eine Datei ist im Index unsichtbar, bis sie repariert ist — sichtbar nur im Log. | Claude Code (Empfehlung), Nikinger widerspricht, falls anders gewollt | ✅ 2026-10-30: **so gebaut** (15.2) — Widerspruch bleibt möglich |
| **E3** | B7: Titel-Höchstlänge. Die Grenze ist ein **Schätzwert** (Dateiname ≤ 255 Byte, `itm_xxxxxxxx__` + `.md` = 17 Byte; Slug auf ≤ 100 Zeichen kürzen, Titel selbst ≤ 300 Zeichen) — bei 15.5 **gegen `os.statvfs().f_namemax`** und UTF-8-Bytes messen, nicht Zeichen zählen. | Claude Code, bei 15.5 gemessen | [VERIFY] |
| **E4** | **Wer baut 15.2–15.7?** Dieser Plan nennt Claude Code; eine datierte Nikinger-Entscheidung dazu gibt es nicht (Standard der Phase: opencode, 14.7 war eine ausdrückliche Ausnahme). **15.2** (Index-Neuaufbau, Dienststart) und **15.3** (Typkoerzion im Kern) berühren den Startpfad und jede Lese-/Schreibfläche — Kandidaten für Opus. | **Nikinger** | ✅ 2026-10-30: **Opus** baut 15.2–15.7 (eigene Session je Schritt) |

## §3 Schritte — je Schritt ein Commit, Head im selben Commit (Hard Rule 8)

Jeder Schritt: **(a)** Befund am Code nachvollziehen · **(b)** Wächter schreiben, der **vor** dem Fix
rot ist · **(c)** Fix · **(d)** **Gegenlauf**: Fix entfernen (`git stash` nur der Quelldateien), die
neuen Wächter müssen genau an diesem Befund rot werden · **(e)** volle Suite grün · **(f)** Head.

| Schritt | Befunde | Fix (Kern zuerst) | Wächter |
|---|---|---|---|
| **15.1 ✅** | B1, B15 | `Store._asset_matches()`: formfalsche ID ⇒ `ItemNotFound` (= „nicht gefunden", kein Orakel); `ASSET_ID_RE` auf `\Z` (`$` ließ einen Zeilenumbruch durch) | Store (get/delete × 7 ID-Formen), MCP (Traversal liest fremdes Item), Store direkt (Traversal verschiebt fremde `.share.yml`), REST (`*`), `ASSET_ID_RE` |
| **15.2 ✅** | B2, B3, B20 | Rename: Elternordner vor `os.rename` anlegen **oder** `ValidationError`; die Wiederaufnahme beim Start fängt jeden Fehler und startet trotzdem (Marker bleibt, `CRITICAL`). `rebuild_index`: je Datei fangen, Transaktion statt Teil-`DELETE`; CRLF im Frontmatter tolerieren | Marker-Szenario (Neustart nach fehlgeschlagenem Rename), `README.md` im Space (Index zählt die übrigen), CRLF-Datei |
| **15.3** | B5, B8 | Kern: Frontmatter-Werte beim Lesen koerzieren (Tags → `str`, Titel → `str`), sonst Datei mit Pfad ablehnen; REST: Typprüfung in POST **und** PATCH (`title`/`folder`/`body`/`tags`); Link-Extraktion **vor** dem Schreiben rechnen, damit ein Fehler nie nach dem Write kommt | Hand-Edit `tags: [2026]` ⇒ Suche lebt; REST `tags:[1,2]` ⇒ 422; `body:5` ⇒ 422 **und** Datei unverändert, kein Versionssprung |
| **15.4** | B4 | `manages_space` statt `can_write` in beiden Mitglieder-Routen | Schreib-Gast ⇒ 403 auf add **und** remove; Eigentümer ⇒ 200 |
| **15.5** | B6, B7 | Space-Name-Validierung an **einer** Stelle im Kern, aufgerufen von MCP- und REST-Schreibpfaden; Slug kürzen, Titel-Höchstlänge, `OSError` sauber abbilden | `space="team/"` ⇒ abgelehnt; 200 Umlaute im Titel ⇒ weder 500 noch halber Write |
| **15.6** | B9, B10 | Einladungs-Pfad in die Redaktion (`request_log.py`, `logging_setup.py`); `search()` überspringt eine zwischenzeitlich verschwundene Datei | Log enthält den Token nicht; Such-Threads gegen Umbenennungen ⇒ kein `FileNotFoundError` |
| **15.7** | — | Volle Suite, `doc_health`, Update-Log-Zeile (nur Menschen-relevantes), Head-Bilanz | — |

## §4 Abnahme — neue Zeilen P10.5-75 bis P10.5-79

| # | Kriterium |
|---|---|
| P10.5-75 | B1/B15: keine `asset_id` wird je zum Pfad — Traversal und Wildcard liefern „nicht gefunden", nichts wird gelesen oder verschoben (Store, MCP, REST); der Gegenlauf macht genau diese Wächter rot |
| P10.5-76 | B2/B3/B20: ein fehlgeschlagener Ordner-Rename und eine fremde/CRLF-`.md` verhindern weder den Neuaufbau noch den Dienststart |
| P10.5-77 | B5/B8: kein Nicht-String-Wert in Tags/Titel/Ordner/Body bricht Suche oder Update; ein Fehler kommt nie **nach** dem Write |
| P10.5-78 | B4: Mitglieder eines fremden Home-Space ändert nur, wer ihn verwaltet |
| P10.5-79 | B6/B7/B9/B10: Space-Name und Titellänge geprüft, kein Einladungs-Token im Log, Suche übersteht paralleles Umbenennen |

**Live-Anteil (Nikinger, nicht Claude Code):** nach dem Deploy je ein Aufruf des Connectors
(`get_item_asset` mit einer erfundenen ID ⇒ `asset_not_found`) — Wegwerf-Instanz zuerst, live nur,
was der Server nicht selbst entscheiden kann (Working style, 2026-10-22).

## §5 Was dieser Plan **nicht** tut

- **B11–B22** (außer B15/B20): Backlog, wie vom Review empfohlen. B12 braucht eine Messung (Index
  statt Vollscan), keinen Schnellfix; B16 (`archived` im Editor) ist UI-Arbeit; B17 (zwei
  Versionsquellen) und B18 (README) sind Doku-Drift und gehören in den Closeout (Block Z).
- **Kein Deploy.** Weder Hotfix noch Deploy D laufen aus dieser Session (Hard Rule 9).

## Anmerkungen 15.1 — B1 (2026-10-30, Claude Code)

- **Reichweite, am Code gelesen (korrigiert nach dem Advisor-Hinweis):** über **MCP** ist B1 ein reiner
  **Lese**-Befund (`get_item_asset`) — **kein** MCP-Werkzeug ruft `delete_asset` auf; das **Verschieben**
  ist nur über den Store/CLI erreichbar, über REST nur als Wildcard (`*`), weil die Route kein `/`
  trägt. Kritisch bleibt es: die Auth-DB-Dateien und fremde Items sind lesbar.
- **Am Code bestätigt:** `get_asset`/`delete_asset` bauten `target_dir.glob(f"{asset_id}.*")`;
  `ASSET_ID_RE` wurde nur in `files.asset_path()` (Upload) und `list_assets()` angewandt. Die
  MCP-Zweige ohne Schreibrecht filtern über `list_assets()` — dort ging die ID nie in einen Pfad.
- **Warum der Fix im Store sitzt, nicht in Tool und Route:** MCP und REST rufen beide
  `store.get_asset`/`delete_asset`; eine Prüfung im Kern deckt beide **und** `space_cli`, eine im
  Adapter nur den einen. Die Route kann nach Starlettes Dekodierung kein `/` tragen, aber `*` —
  das war B15.
- **Warum „nicht gefunden" statt `ValidationError`:** die Adapter bilden `ItemNotFound` aus
  `get_asset` schon auf `asset_not_found`/404 ab. Eine formfalsche ID unterscheidbar zu machen von
  einer unbekannten hätte einen neuen Fehlerpfad **und** ein Orakel gebraucht, ohne einem
  ehrlichen Client zu helfen.
- **`$` → `\Z`:** `re.match(r"^ast_[0-9a-f]{8}$", "ast_01234567\n")` trifft — der Zeilenumbruch
  ginge in Glob und Dateinamen. `ITEM_ID_RE` hat dieselbe Form (`$`); dort erreicht eine ID den
  Pfad erst **nach** dem Index-Lookup, deshalb nicht Teil von B1 — als Härtung in 15.5 mitnehmen.
- **Gegenlauf (Fix per `git stash` entfernt):** 9 Wächter rot — Store ×6 (`../../../bob/.share`,
  `*`, `ast_*` je get/delete), MCP ×1 (Traversal liest fremdes Item), Store direkt ×1 (verschiebt fremde
  `.share.yml`), REST ×1 (`*` ⇒ 200 statt 404). Die übrigen Formen (`ast_0123456?`, leerer
  String, Traversal auf eine nicht existierende Datei) laufen **auch ohne Fix** durch, weil dort
  schlicht nichts passt — sie sind Regressionsschutz, kein Beweis; der Beweis sind die neun.

## Anmerkungen 15.2 — B2/B3/B20 (2026-10-30, Opus)

- **Am Code reproduziert (tmp-`DATA_ROOT`), alle drei:** B2 `rename_folder("alice", "projekte",
  "archiv/projekte")` ⇒ `FileNotFoundError`, Marker bleibt, `Store()` wirft erneut · B3
  `alice/README.md` ⇒ `rebuild_index()` wirft `FrontmatterError`, **0** Zeilen im Index, frischer
  Start wirft · B20 `parse("---\r\n…")` ⇒ `FrontmatterError`.
- **Fund (nicht im Review): `links: [itm_x, itm_x]`** von Hand riss den Primärschlüssel von
  `item_links` (`IntegrityError`) — derselbe Startblocker wie B3. Fix an der einen Stelle, die
  Kanten schreibt (`index._replace_links_no_commit()`: Paare dedupliziert).
- **Fund: `yaml.YAMLError` ist kein `ValueError`.** Kaputtes YAML lief an jedem `except ValueError`
  im Kern vorbei — auch an dem in `_rewrite_space_frontmatter`. `parse()` übersetzt jetzt in
  `FrontmatterError`; damit greift jeder bestehende Fänger.
- **Fund: ein Wächter lief nie.** `test_rename_resumes_after_crash` stand **zweimal** in
  `phase1_storage/tests/test_store.py` (Ordner Z. 1385, Space Z. 1535) — die zweite Definition
  verdeckte die erste, der Ordner-Wiederaufnahme-Test war seit Block 9 nie gelaufen. Umbenannt in
  `test_rename_folder_resumes_after_crash`, gegen den **unveränderten** Code grün (kein versteckter
  Fehler). AST-Suche über alle Testdateien: **keine** weitere Doppelung.
- **B3, Bauform:** je Datei ein `SAVEPOINT` (keine halbe Zeile: Item ohne Kanten), der ganze
  Neuaufbau **eine** Transaktion (vorher committete `replace_item_links()` das `DELETE` beim ersten
  Item). **Datei-Fehler** (`OSError`, `ValueError`, `KeyError`, `TypeError`, `sqlite3.ProgrammingError`
  /`InterfaceError`/`IntegrityError` — gemessen: `title: [a]` wirft `ProgrammingError`, eine
  `DatabaseError`-Unterklasse) kosten die Datei, `CRITICAL` mit Pfad; **Umgebungs-Fehler**
  (`OperationalError`) rollen zurück, der alte Index steht vollständig. `IndexStats` bleibt
  unverändert (P1-Contract) — die Zahl der übersprungenen Dateien steht im Log.
- **B2, Bauform:** Elternordner wird angelegt (wie `files.move_file()` es für Dateien tut; die Option
  „`ValidationError`" hätte einen legitimen Klick verboten). Scheitert der Rename, **bevor** etwas
  wanderte (am **Plattenstand** entschieden: `alt` steht, `neu` fehlt), wird der Marker gelöscht —
  sonst führte der nächste Start einen Rename aus, den der Aufrufer als Fehler sah. Die
  Wiederaufnahme fängt jeden Fehler: `CRITICAL`, Marker bleibt, Index aus der Platte neu, Start geht
  weiter. **Neu dadurch (Advisor):** ein liegender Marker bei laufendem Dienst — deshalb lehnen
  `rename_folder`/`rename_space` mit `ValidationError` ab, solange er liegt (sonst überschriebe der
  nächste Rename die einzige Spur). Rest: ein so angelegter, danach leerer Elternordner bleibt liegen
  (unsichtbar, Ordner leiten sich aus Items ab).
- **B20, Bauform:** die drei Begrenzer akzeptieren `\r?\n`; `parse()` gibt dieselbe Form zurück
  (P1-Contract). Ein Update schreibt das Frontmatter mit `\n`, der Body behält `\r\n` — **gemischte
  Zeilenenden** nach dem ersten Schreiben, Datei bleibt lesbar (Wächter `test_crlf_item_survives_update`).
  Ein UTF-8-BOM ist **nicht** abgedeckt (eigene Fehlerklasse, kostet jetzt nur die Datei).
- **Gegenlauf, je Quelldatei einzeln** (Advisor: sonst verdeckt B3 den B20-Fix und die
  Wiederaufnahme den Elternordner-Fix): ohne `frontmatter.py` **6 rot**, ohne `index.py` **5 rot**,
  ohne `store.py` **5 rot** — jede Datei hat eigene rote Wächter, keiner verdeckt einen anderen.

