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
updated: 2026-10-30 (Schritt 15.4b gebaut — B4′ + Selbst-Austragen; E1 überholt: Deploy D nach allen Fixes; E5-Durchsicht 0 Treffer) | 2026-10-30 (Schritt 15.4 gebaut, Opus — B4 geschlossen, drei Stellen statt zwei) | 2026-10-30 (Schritt 15.3b gebaut, Opus — E5: `share_*`-Skalar = eine Freigabe, `WARNING` mit Pfad) | 2026-10-30 (E5 entschieden — `share_*`-Skalar = eine Freigabe, Schritt 15.3b) | 2026-10-30 (Schritt 15.3 gebaut, Opus — B5/B8 geschlossen: Lesen nachsichtig, Schreiben streng, kein Fehler nach dem Write; Fund `links: [1]`) | 2026-10-30 (Schritt 15.2 gebaut, Opus — B2/B3/B20 geschlossen, E2 wie empfohlen; Fund: doppelte `links:` = derselbe Startblocker) | 2026-10-30 (E1 Hotfix ja, E4 Opus — Nikinger) | 2026-10-30 (Entwurf + Schritt 15.1 gebaut, Claude Code — B1 geschlossen, am Code bestätigt und per Gegenlauf bewiesen)
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
| B5 Nicht-String-Tags/Titel | hoch, R | **ja** (2026-10-30): reproduziert, 8 Hand-Edit-Fälle; `title: [a, b]`/`title:` nach dem Neuaufbau unsichtbar | **✅ 15.3** |
| B8 REST ohne Typprüfung | mittel, R/C | **ja**: `body:5` schrieb vor dem Wurf, `folder:123` = `AttributeError` | **✅ 15.3** |
| B4 Mitglieder fremder Home-Spaces | hoch, R | **ja** (2026-10-30): reproduziert, add/remove 200, `manageable: true` | **✅ 15.4** |
| B4′ `share_*` fremder Home-Space-Items (Fund 15.4) | — (nicht im Review), C | **ja**: `_items_patch` prüft nur `can_write_item_as_human` + eigene Re-Auth; in 15.4b **reproduziert** (R): Gast setzt `share_read`/`share_write`/`visibility` auf Bobs Item ⇒ 200 | **✅ 15.4b** |
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
| **E1** | **B1 als Hotfix vorab live, oder mit Deploy D?** B1 steht seit 2026-08-20 im Live-Dienst (live: Release `20261023T165838…` = Deploy B, SHA `e5c834e`, am Symlink `/opt/sharefyx/current` gelesen). **Wichtig: `deploy.sh main` ist KEIN Hotfix** — `main` trägt alles seit `v3.1.6` (u. a. `rename_folder`, den Pfad hinter B2) und damit genau das, was das Review „nicht freigabefähig“ nannte. **Weg:** Branch ab `e5c834e`, nur die Code- und Testdateien des Fixes (Doku-Hunks lassen sich nicht auf den alten Stand übertragen), eigener `docs/UPDATE_LOG.md`-Eintrag und eigene Version (**Versionsstufe = Entscheidung des Nikingers**), dann `deploy.sh <ref>` — das Skript nimmt jede Git-Ref. **Bewiesen (2026-10-30, Wegwerf-Worktree auf `e5c834e`):** der Fix-Patch (Store, Files, 4 Testdateien) lässt sich sauber anwenden, die 50 Asset-Tests sind grün, ohne den Fix sind dieselben 9 Wächter rot — der Fehler steckt also auch im Live-Stand. **Empfehlung: Hotfix.** Der Deploy läuft beim Nikinger (Hard Rule 9). | **Nikinger** | ✅ 2026-10-30: **Hotfix, ja** — Branch `hotfix-b1` ab `e5c834e` vorbereitet, Deploy + Version beim Nikinger · **[2026-10-30, später] überholt (Nikinger):** **kein** Hotfix vorab — Deploy D nach **allen** Fixes, an einem Wochenende ohne Nutzung außer dem Nikinger; B1 fährt mit. `hotfix-b1` bleibt als Branch liegen (ungenutzt) |
| **E2** | B3: eine nicht parsebare Datei wird **übersprungen + `CRITICAL` mit Pfad** (Empfehlung) statt den Neuaufbau abzubrechen. Folge: so eine Datei ist im Index unsichtbar, bis sie repariert ist — sichtbar nur im Log. | Claude Code (Empfehlung), Nikinger widerspricht, falls anders gewollt | ✅ 2026-10-30: **so gebaut** (15.2) — Widerspruch bleibt möglich |
| **E3** | B7: Titel-Höchstlänge. Die Grenze ist ein **Schätzwert** (Dateiname ≤ 255 Byte, `itm_xxxxxxxx__` + `.md` = 17 Byte; Slug auf ≤ 100 Zeichen kürzen, Titel selbst ≤ 300 Zeichen) — bei 15.5 **gegen `os.statvfs().f_namemax`** und UTF-8-Bytes messen, nicht Zeichen zählen. | Claude Code, bei 15.5 gemessen | [VERIFY] |
| **E5** | **`share_read: fabian` (Hand-Edit, Skalar statt Liste).** Heute: gelesen als `['f','a','b','i','a','n']`, und der **erste** gewöhnliche Write schreibt diese Buchstabenliste auf die Platte (am Code bestätigt 2026-10-30: `update(status="done")` ⇒ `share_read: [f, a, b, i, a, n]`, Re-Auth sieht vorher == nachher). Optionen: **A** eine Freigabe (`["fabian"]`) · B verwerfen + Log · C Datei überspringen · D lassen. **Empfehlung A:** das Re-Auth-Gate schützt UI/API vor einer gestohlenen Sitzung, der Datei-Weg lag nie dahinter — `share_read: [fabian]` von Hand gilt schon heute sofort (Hard Rule 2). Seit 15.3 erreicht ein Skalar den Kern nur über einen Hand-Edit. | **Nikinger** | ✅ 2026-10-30: **A** — gebaut in **15.3b**: `share_read`/`share_write` in `normalize_item_fields()`, `WARNING` mit Pfad bei jeder Skalar-Koerzion; **vor Deploy D** liest der Nikinger den Live-`DATA_ROOT` read-only auf Skalar-`share_*` durch · **Durchsicht gefahren (Nikinger, 2026-10-30): 0 Treffer** im Live-`DATA_ROOT` — kein Übergang, keine Koerzion beim Deploy |
| **E4** | **Wer baut 15.2–15.7?** Dieser Plan nennt Claude Code; eine datierte Nikinger-Entscheidung dazu gibt es nicht (Standard der Phase: opencode, 14.7 war eine ausdrückliche Ausnahme). **15.2** (Index-Neuaufbau, Dienststart) und **15.3** (Typkoerzion im Kern) berühren den Startpfad und jede Lese-/Schreibfläche — Kandidaten für Opus. | **Nikinger** | ✅ 2026-10-30: **Opus** baut 15.2–15.7 (eigene Session je Schritt) |
| **E6** | **15.4 sperrt dem Gast auch das Selbst-Austragen** aus einem fremden Home-Space (Folge der Abweichung von P7-L/N7). Erlauben? | **Nikinger** | ✅ 2026-10-30: **ja** — gebaut in **15.4b** (mit `can_read`, kein Austragen aus unsichtbaren Spaces) · **B4′ fixen: ja** (15.4b) |

## §3 Schritte — je Schritt ein Commit, Head im selben Commit (Hard Rule 8)

Jeder Schritt: **(a)** Befund am Code nachvollziehen · **(b)** Wächter schreiben, der **vor** dem Fix
rot ist · **(c)** Fix · **(d)** **Gegenlauf**: Fix entfernen (`git stash` nur der Quelldateien), die
neuen Wächter müssen genau an diesem Befund rot werden · **(e)** volle Suite grün · **(f)** Head.

| Schritt | Befunde | Fix (Kern zuerst) | Wächter |
|---|---|---|---|
| **15.1 ✅** | B1, B15 | `Store._asset_matches()`: formfalsche ID ⇒ `ItemNotFound` (= „nicht gefunden", kein Orakel); `ASSET_ID_RE` auf `\Z` (`$` ließ einen Zeilenumbruch durch) | Store (get/delete × 7 ID-Formen), MCP (Traversal liest fremdes Item), Store direkt (Traversal verschiebt fremde `.share.yml`), REST (`*`), `ASSET_ID_RE` |
| **15.2 ✅** | B2, B3, B20 | Rename: Elternordner vor `os.rename` anlegen **oder** `ValidationError`; die Wiederaufnahme beim Start fängt jeden Fehler und startet trotzdem (Marker bleibt, `CRITICAL`). `rebuild_index`: je Datei fangen, Transaktion statt Teil-`DELETE`; CRLF im Frontmatter tolerieren | Marker-Szenario (Neustart nach fehlgeschlagenem Rename), `README.md` im Space (Index zählt die übrigen), CRLF-Datei |
| **15.3 ✅** | B5, B8 | Kern: Frontmatter-Werte beim Lesen koerzieren (Tags → `str`, Titel → `str`), sonst Datei mit Pfad ablehnen; REST: Typprüfung in POST **und** PATCH (`title`/`folder`/`body`/`tags`); Link-Extraktion **vor** dem Schreiben rechnen, damit ein Fehler nie nach dem Write kommt | Hand-Edit `tags: [2026]` ⇒ Suche lebt; REST `tags:[1,2]` ⇒ 422; `body:5` ⇒ 422 **und** Datei unverändert, kein Versionssprung |
| **15.3b ✅** | E5 | `share_read`/`share_write` in `normalize_item_fields()` (Skalar = eine Freigabe), `WARNING` mit Pfad; Docstring-Satz „bewusst nicht“ ersetzen | Hand-Edit `share_read: fabian` ⇒ `acl_of()` = `{fabian}`, Update schreibt `[fabian]`, Log trägt den Pfad |
| **15.4 ✅** | B4 | `manages_space` statt `can_write` in beiden Mitglieder-Routen | Schreib-Gast ⇒ 403 auf add **und** remove; Eigentümer ⇒ 200 |
| **15.4b ✅** | B4′, E6 | REST-`PATCH` von `share_read`/`share_write`/`visibility` nur mit `manages_space` auf den Item-Space; `DELETE …/members/<eigener Name>` erlaubt mit `can_read` | Gast ⇒ 403 je Feld, Datei byteweise gleich; Gast schreibt Body weiter; Team-Schreiber teilt weiter; Selbst-Austragen 200, ohne Leserecht 403 |
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

## Anmerkungen 15.3 — B5/B8 (2026-10-30, Opus)

- **Am Code reproduziert (tmp-`DATA_ROOT`), acht Hand-Edit-Fälle, Neuaufbau ehrlich erzwungen**
  (ein zweiter `Store()` auf demselben Index baut **nicht** neu — der erste Probelauf war dadurch
  wertlos, Advisor-Fund): `tags: [2026]` ⇒ Textsuche `TypeError` · `title: 2026` ⇒ Update
  `AttributeError` · `title: [a, b]` und `title:` ⇒ nach `rebuild_index()` **unsichtbar** (15.2
  überspringt sie) · `tags: abc` ⇒ drei Tags · `tags: [[x]]` ⇒ Suche `TypeError` · **Fund:**
  `links: [1]` ⇒ `get()` und Update `TypeError` (`ITEM_REF_RE` auf `int`). REST: `body:5` schrieb
  Datei und Index, warf danach.
- **Zwei Funktionen, nie eine** (Advisor): **Lesen ist nachsichtig** —
  `frontmatter.normalize_item_fields()` macht `title` zum String und `tags`/`links` zu
  String-Listen, aufgerufen von **beiden** Lesepfaden (`store._item_from_text()`,
  `index.row_from_file()`), damit Index und `get()` nie auseinanderlaufen. **Schreiben ist streng**
  — `store._check_write_types()` in `create()`/`update()` (`title`/`body` String, `tags`/`links`/
  `share_*` String-Liste) plus `type`/`status` in `_check_type_and_status()`; REST bildet die
  `ValidationError` schon auf 422 ab. Teilten beide eine Funktion, würde `tags: [1, 2]` über REST
  still zu `["1", "2"]` statt 422.
- **Koerzion = „wie es im YAML stand"** (`frontmatter.inline_text()`): `2026` → `"2026"`, `true` →
  `"true"` (nicht `True`), `[a, b]` → `"[a, b]"` (nicht `['a', 'b']`). Ein Skalar in `tags`/`links`
  wird **ein** Eintrag (`tags: abc` → `["abc"]`), `~` fällt weg. `parse()` bleibt roh —
  `_write_version_only` schreibt zurück, was der Mensch schrieb.
- **Folge (wie gemischte Zeilenenden in 15.2):** erst der nächste echte Write normalisiert die Datei
  — aus `tags: [2026]` wird `tags: ['2026']`, aus `title: 2026` wird `title: '2026'`.
- **Kein Fehler nach dem Write** (B8, strukturell): `_write_item_file()` rechnet Text und Kanten
  (`_link_rows()`, vorher `_replace_links_for_item()`) **vor** `atomic_write`. Wächter erzwingt
  einen Wurf in der Link-Extraktion: Datei, Version, Git-Historie unverändert.
- **REST:** nur, was **vor** dem Kern gebraucht wird — `visibility` String, `share_read`/
  `share_write` String-Liste (das Re-Auth-Gate baut daraus einen `ShareState`; `frozenset(5)` war
  500). `files.validate_folder()` lehnt Nicht-Strings mit `ValidationError` ab (vorher
  `AttributeError` im PATCH). Der Rest prüft der Kern.
- **Bewusst nicht gemacht — Befund für den Nikinger:** `share_read: fabian` (Hand-Edit, ohne
  Liste) wird heute zu `frozenset("fabian")` = Freigabe an die Spaces `f`, `a`, `b`, … — zufällig
  **fail-closed** (Fabian sieht nichts). Dieselbe Koerzion wie bei `tags` machte daraus eine echte
  Freigabe an `fabian` **ohne Re-Auth**. Rechteerweiterung ist keine Typfrage → in 15.3 unverändert
  gelassen. **[Korrektur, gleicher Tag]:** „unverändert" stimmte nur für den Zugriff — der erste
  gewöhnliche Write schreibt die Buchstabenliste auf die Platte (am Code bestätigt). Entschieden
  als **E5 = A**, gebaut in 15.3b.
- **15.2-Wächter umgezielt:** `test_rebuild_skips_a_title_sqlite_cannot_bind` prüfte, dass
  `title: [a, b]` die Datei kostet — genau das ändert 15.3. Jetzt
  `test_rebuild_skips_a_value_sqlite_cannot_bind` mit `status: [a, b]` (der `ProgrammingError`-Zweig
  bleibt bezeugt).
- **Gegenlauf je Fix, im Code neutralisiert** (ein `git stash` von `frontmatter.py` bräche nur den
  Import — alles rot, nichts bewiesen): Normalisierung aus **8 rot** · nur Index ohne **3** · nur
  Store-Lesen ohne **7** · Schreib-Typprüfung aus **21** · Links nach dem Write **1** ·
  `validate_folder` ohne Typprüfung **2** · REST-Frühprüfung aus **3**. Jeder Fix hat eigene rote
  Wächter.

## Anmerkungen 15.3b — E5 (2026-10-30, Opus)

- **Am Code nachvollzogen, vor dem Fix:** `normalize_item_fields()` liess `share_read`/`share_write`
  roh durch; `_item_from_text()` machte daraus `list("fabian")`, `row_from_file()` schrieb
  `json.dumps("fabian")` = `'"fabian"'` in den Index, `acl_of()` las `frozenset("fabian")` — sechs
  Ein-Buchstaben-Freigaben auf **beiden** Lesepfaden.
- **Bauform:** `share_read`/`share_write` laufen durch dasselbe `_text_list()` wie `tags`/`links`
  (Skalar = ein Eintrag, `~`/leer = keine Freigabe, Elemente wie im YAML). Neu:
  `normalize_item_fields(fields, *, source=None)` — `source` steht **nur** in der Warnung;
  `index.row_from_file()` und `store._item_from_text()` (beide Aufrufer: `_row_to_item`, die
  Space-Umbenennung) reichen den Pfad. `WARNING` nur beim **Skalar** (die Rechteerweiterung), nicht
  bei der Listenform und nicht bei leerem Feld. Logger `storage.frontmatter`.
- **Warum `WARNING` bei jedem Lesen, nicht einmal:** die Warnung hört von selbst auf, sobald der
  nächste Write die Datei in Listenform bringt (`share_read:\n- fabian`) — ein „schon gemeldet“-
  Zustand wäre neuer Zustand im dummen Server, für einen Fall, den es nur per Hand-Edit gibt.
- **Übergang beim Deploy (am Code gelesen, nicht gemessen):** `acl_of()` liest **nur den Index**
  und gleicht nicht ab; der Dienststart baut den Index nur bei Schema-Sprung neu, und 15.3b
  ändert `INDEX_SCHEMA_VERSION` nicht. Eine **vor** Deploy D geschriebene Indexzeile mit
  `'"fabian"'` gibt deshalb weiter die Buchstaben (fail-closed), während `get()` schon
  `["fabian"]` zeigt — bis die Datei sich ändert (Abgleich in `_reconcile_and_get_row`) oder
  `rebuild_index()` läuft. **Folge für die Durchsicht vor Deploy D:** ein Treffer wird am besten
  **vor** dem Deploy von Hand in Listenform gebracht — dann gibt es keine Koerzion und keinen
  Übergang.
- **Wächter (5 neu + 1 umgezielt):** `test_store.py` — `share_read`/`share_write` je: Hand-Edit Skalar ⇒ `WARNING`
  mit Pfad und Feldname, `acl_of()` = `{fabian}`, `get()` = `["fabian"]`, Update schreibt
  `- fabian`, `acl_of()` danach unverändert; Listenform / leer / `~` ⇒ keine Warnung (3, reiner
  Regressionsschutz — laufen auch ohne Fix grün). `test_frontmatter.py` — der alte Wächter
  „`share_*` bleibt roh“ ist **umgezielt** auf die neue Regel (exakter Warnungstext, Eingabe
  unverändert).
- **Gegenlauf, im Code neutralisiert** (wie 15.3): `share_*` aus der Schleife ⇒ **3 rot** (beide
  Store-Wächter + Frontmatter) · Warnung stummgeschaltet, Koerzion bleibt ⇒ **3 rot** · Pfad im
  Index-Lesepfad nicht gereicht ⇒ **2 rot** (Warnung beim Neuaufbau) · Pfad in `_row_to_item` nicht
  gereicht ⇒ **2 rot** (Warnung bei `get()` — der Weg, auf dem sie im Betrieb fällt, Advisor-Fund).
- **Sichtbarkeit im Betrieb, am Code gelesen:** `SPACE_LOG_LEVEL=INFO` (Unit `sharefyx-mcp.service`),
  `configure_logging()` setzt den Root-Logger darauf — ein `WARNING` erreicht das Journal.
  `deploy.sh` und die Unit rufen kein `rebuild_index()` (gegrept) — der Übergang oben gilt.
  **Folge (kein Blocker):** `search()` liest jede Datei, ein unbehobener Skalar warnt also bei jeder
  Suche und jedem `/overview`-Poll — gewollt laut E5, und gegenstandslos, wenn Treffer vor dem Deploy
  von Hand behoben werden.
- **Durchsicht vor Deploy D — der Befehl (Nikinger, read-only, nicht aus dieser Session gefahren):**
  `grep -rnE --include='*.md' --exclude-dir='.*' '^share_(read|write):[[:space:]]*[^[:space:][~#]' /home/savefyx/savefyx-data`
  Trifft jeden Skalar (ohne oder mit Anführungszeichen), nicht die Listenform `[…]`, nicht die
  Blockliste (`share_read:` + `- x`-Zeilen), nicht leer, nicht `~`, nicht `._trash/`. **Harmloser
  Fehltreffer:** `share_read: null` (liest sich als keine Freigabe). Jeder echte Treffer: von Hand
  auf `[name]` umschreiben, **vor** dem Deploy.

## Anmerkungen 15.4 — B4 (2026-10-30, Opus)

- **Am Code reproduziert (In-Process-App, tmp-`DATA_ROOT`, tmp-`auth.sqlite3`):** `bob` ist
  Principal, `bob/.share.yml` = `write: [niklas]`, `read: [carol]`. Als `niklas`: `POST
  /api/v1/spaces/bob/members {mallory, write}` mit Re-Auth ⇒ **200** (Datei geändert), `DELETE
  …/members/carol` ⇒ **200**, `GET …/members` ⇒ `manageable: true` (und `orphans` befüllt).
- **Drei Stellen, nicht zwei:** der Plan nannte die beiden Schreib-Routen; `manageable` im GET ist
  dieselbe Frage (es schaltet den Verwalter-Hinweis `orphans` frei) — Advisor-Hinweis, mitgenommen.
  `_spaces_delete` behält `can_write`: ein Home-Space wird dort schon vorher abgewiesen, und in
  einem Team-Space ist `can_write` == `manages_space`.
- **Warum `manages_space` und keine neue Prüfung:** die Funktion trägt genau diese Regel schon für
  Ordner (P10-I) und Verschieben/Löschen (P9-K): eigener Space immer, Team-Space mit space-level
  `write:`, fremder Home-Space nie. Eine zweite Formulierung derselben Regel würde auseinanderlaufen.
  Fehlertext jetzt „Keine Verwaltungsrechte für diesen Space.“ (kein Test, kein JS prüfte den alten).
- **Wächter (4):** Gast add ⇒ 403 + Datei byteweise gleich · Gast remove ⇒ 403 + Datei gleich ·
  Gast GET ⇒ `manageable: false`, `orphans: []` · Team-Space `write:` ⇒ add/remove 200
  (Regressionsschutz, grün mit und ohne Fix). Eigentümer ⇒ 200 deckten die P7-Tests schon.
- **Gegenlauf:** `api.py` per `git stash` entfernt ⇒ genau die drei Gast-Wächter rot, 23 grün.
- **Datierte Abweichung von P7-L / N7 (gelockt, `phase7_spaces_admin_plan.md` §0.3/§0.4) —
  durch den Nikinger-Auftrag vom 2026-10-30** („`manages_space` statt `can_write` in beiden
  Mitglieder-Routen“): P7-L sagte „verwalten darf, wer im Ziel-Space `write:` hat“. Das gilt ab
  15.4 nur noch für **Team-Spaces** und den eigenen; in einem **fremden Home-Space** ist `write:`
  Gastrecht. Die Regel P7-L entstand vor dem Home-Space-Begriff (P10-I, Block 2). **Folge, die man
  merken muss:** ein Gast kann sich aus einem fremden Home-Space **nicht mehr selbst austragen**
  (vorher ja — als Nebenprodukt von N7; §0.4 Punkt 1 nannte die Selbstaussperrung eine
  hingenommene Kehrseite, kein Recht). Rückweg: der Eigentümer, oder `spacectl.py remove-member`.
  **Offene Frage an den Nikinger:** soll `DELETE …/members/<eigener Name>` für den Gast erlaubt
  bleiben (verengt nur den eigenen Zugriff)? Eine Zeile plus Wächter — nicht gebaut, weil der
  Auftrag „beide Routen“ lautete.
- **Fund (nicht im Review, am Code gelesen — C, nicht reproduziert): dieselbe Frage eine Ebene
  tiefer.** `PATCH /api/v1/items/{id}` mit `share_read`/`share_write`/`visibility` prüft für ein
  Item in einem fremden Home-Space nur `can_write_item_as_human()` und die **eigene** Re-Auth des
  Gasts — `folder` hat dort einen Eigentümer-Riegel, `share_*` nicht. Ein Schreib-Gast in Bobs
  Home-Space kann damit Bobs Items an `mallory` freigeben. MCP ist nicht betroffen (`share_*` über
  kein Werkzeug änderbar). **Kein Fix in 15.4** (außerhalb des Auftrags) — Kandidat für 15.5/15.6
  oder Backlog, Entscheidung beim Nikinger.
- **UI-Rest, nicht gebaut:** `spaces.js :: selectSpace()` zeigt die Knöpfe unabhängig von
  `manageable` — ein Gast klickt und bekommt jetzt die 403-Meldung. Backlog (UI-Schnitt), kein
  Rechte-Befund mehr.

## Anmerkungen 15.4b — B4′ + E6 (2026-10-30, Opus)

- **B4′ reproduziert (In-Process-App):** `niklas` mit `write:` in Bobs Home-Space, `PATCH` auf
  Bobs Item mit `share_read: [mallory]` / `share_write: [mallory]` / `visibility: human` und der
  **eigenen** Re-Auth ⇒ je **200**. (Erster Anlauf mit `visibility: shared` war 422 — kein gültiger
  Wert, `VISIBILITY_VALUES` = `private`/`human`; Test korrigiert, kein Befund.)
- **Fix:** ein Riegel in `_items_patch` vor dem Re-Auth-Gate — eines der drei Freigabefelder im Body
  und kein `manages_space(session.space, acl.space)` ⇒ 403. Gleiche Form wie der `folder`-Riegel
  darüber (Feld im Body, nicht „Wert geändert“): kein UI-Pfad schickt die Felder für fremde Items
  (P9-BP: der Freigeben-Knopf erscheint nur im eigenen Space), also trifft er keinen legitimen
  Aufruf. **Folge über B4′ hinaus:** auch ein Item-`share_write`-Halter kann die Freigaben eines
  fremden Items nicht mehr ändern — derselbe Grund (Rechteliste des Eigentümers).
- **E6 (Selbst-Austragen):** `DELETE …/members/<name>` ist erlaubt, wenn `name ==
  session.space` **und** `can_read` — das verengt nur den eigenen Zugriff. Ohne `can_read` wäre
  es ein (wirkungsloser, weil No-op) Weg in unsichtbare Spaces; der Wächter hält das fest.
- **Datenschutz-Einordnung (Nikinger-Frage, keine Rechtsberatung):** eine EU-Vorschrift, die
  genau diesen Knopf verlangt, ist mir nicht bekannt. Er passt zum Gedanken „Datenschutz durch
  Technikgestaltung“ — das ist eine Einordnung, nicht der Grund der Änderung (der Grund ist E6).
- **Anlegen ist nicht betroffen (am Code gelesen):** `_items_post` reicht nur
  `status`/`due`/`tags`/`links`/`format`/`folder`/`assignee` an den Kern; `share_*`/`visibility` im
  POST-Body fallen still weg. MCP `create_item` hat keine solchen Parameter.
- **Wächter (8 neu, `phase7_spaces_admin/tests/test_space_admin_api.py`):** Gast ändert
  `share_read`/`share_write`/`visibility` ⇒ 403, Datei byteweise gleich (3) · Gast **nimmt** Bobs
  Freigabe an `carol` zurück, ohne Anmeldedaten ⇒ 403 (der gefährlichere Fall: Verengen braucht
  keine Re-Auth — vorher 200, Advisor-Hinweis) · Gast schreibt den
  Body weiter (Regressionsschutz) · Team-Schreiber teilt weiter (Regressionsschutz) ·
  Selbst-Austragen 200, `carol` bleibt · Selbst-Austragen ohne Leserecht 403.
- **Gegenlauf, im Code neutralisiert:** Freigabe-Riegel aus ⇒ **4 rot** · Selbst-Austragen aus ⇒
  **1 rot** · `can_read`-Bedingung aus ⇒ **1 rot**.
