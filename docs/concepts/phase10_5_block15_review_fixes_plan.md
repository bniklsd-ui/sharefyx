---
status: live
purpose: Plan P10.5 Block 15 — die Fixes aus dem Ultra-Review v4.0.0 (B1–B10), je Befund ein Wächter und ein Gegenlauf, vor Deploy D. Der Dienst darf nie an Daten scheitern, und eine Eingabe wird nie zum Pfad.
read-when: vor dem Bau eines Fix-Schritts 15.x, oder wenn ein Befund B1–B10 des Reviews zitiert wird
detail: L2
up: ../../phase10_5_finishing/CLAUDE.md
down:
  - phase10_5_ultra_review_v4.0.0.md                    # 📕 der Bericht, verbatim — die Befunde B1–B22
  - phase10_5_block14_7_plan.md                         # 📗 Muster dieses Plans (Schritte, Tor, Anmerkungen)
  - phase10_5_block15_review_fixes_plan_anhang.md      # 📦 die Anmerkungen 15.1–15.3b, verbatim
  - ../../phase1_storage/storage/store.py               # Kern: `_asset_matches()`, `rebuild_index()`, Rename-Wiederaufnahme
  - ../../phase5_ui/webui/api.py                        # REST: Typprüfung, Mitglieder-Routen
  - ../../phase2_mcp/mcpserver/tools.py                 # MCP: Space-Name, `offset`
updated: 2026-10-31 (Schritt 15.6b — Fund B3′ gebaut: kaputte Datei fehlt in der Suche statt sie zu sprengen) | 2026-10-31 (Schritt 15.6 — B9/B10 geschlossen; Fund B3′ beim Nikinger; Anmerkungen 15.1–15.3b → Anhang) | 2026-10-30 (Schritt 15.5c — E3: Titel ≤ 256 Zeichen, Nikinger; Live-Durchsicht B6 0 Treffer) | 2026-10-30 (Schritt 15.5b — UI-Rest aus 15.4: Verwalten-Knöpfe nur bei `manageable`) | 2026-10-30 (Schritt 15.5 gebaut, Opus — B6/B7 geschlossen; E3 gemessen: Slug ≤ 100 Byte, kein Titel-Limit) | 2026-10-30 (Schritt 15.4b gebaut — B4′ + Selbst-Austragen; E1 überholt: Deploy D nach allen Fixes; E5-Durchsicht 0 Treffer) | 2026-10-30 (Schritt 15.4 gebaut, Opus — B4 geschlossen, drei Stellen statt zwei) | 2026-10-30 (Schritt 15.3b gebaut, Opus — E5: `share_*`-Skalar = eine Freigabe, `WARNING` mit Pfad) | 2026-10-30 (E5 entschieden — `share_*`-Skalar = eine Freigabe, Schritt 15.3b) | 2026-10-30 (Schritt 15.3 gebaut, Opus — B5/B8 geschlossen: Lesen nachsichtig, Schreiben streng, kein Fehler nach dem Write; Fund `links: [1]`) | 2026-10-30 (Schritt 15.2 gebaut, Opus — B2/B3/B20 geschlossen, E2 wie empfohlen; Fund: doppelte `links:` = derselbe Startblocker) | 2026-10-30 (E1 Hotfix ja, E4 Opus — Nikinger) | 2026-10-30 (Entwurf + Schritt 15.1 gebaut, Claude Code — B1 geschlossen, am Code bestätigt und per Gegenlauf bewiesen)
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
| B6 Space-Name ungeprüft | mittel, R | **ja** (2026-10-30): reproduziert, dazu `./team` und `team/.` — alle vier landen in `team/` mit rohem Namen im Frontmatter | **✅ 15.5** |
| B7 Titel-Länge → Dateiname | mittel, R | **ja**: reproduziert — 200 Umlaute `OSError 36`; Update auf 100 CJK: Datei am alten Namen mit `version: 2`, kein Commit | **✅ 15.5** |
| B9 Einladungs-Token im Log | mittel, R | **ja** (2026-10-31): reproduziert, GET **und** POST `/ui/invite/<token>` im Klartext; `_TOKEN_SEGMENT_RE` kannte nur `/mcp/` | **✅ 15.6** |
| B10 `search()` ohne Lock | mittel, R | **ja**: reproduziert, 3 Such-Threads gegen 300 Titel-Updates ⇒ **15** `FileNotFoundError` — nur mit `sys.setswitchinterval(1e-6)`, beim Standard **0** | **✅ 15.6** |
| B3′ kaputtes YAML in einer indizierten Datei (Fund 15.6) | — (nicht im Review), R | **ja**: Hand-Edit `title: [unclosed` ⇒ `search()` wirft `FrontmatterError` — die **ganze** Suche fällt, nicht nur die eine Zeile; `get()` der Datei ebenso | **✅ 15.6b** (Nikinger 2026-10-31: „fix it before deploy“) |
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
| **E3** | B7: Titel-Höchstlänge. Die Grenze ist ein **Schätzwert** (Dateiname ≤ 255 Byte, `itm_xxxxxxxx__` + `.md` = 17 Byte; Slug auf ≤ 100 Zeichen kürzen, Titel selbst ≤ 300 Zeichen) — bei 15.5 **gegen `os.statvfs().f_namemax`** und UTF-8-Bytes messen, nicht Zeichen zählen. | Claude Code, bei 15.5 gemessen | ✅ 2026-10-30 **gemessen:** `f_namemax` = 255 Byte (ext4); engster Name ist die tmp-Datei von `atomic_write` (Name + 14) ⇒ Slug ≤ 224 Byte; **gebaut: Slug ≤ 100 UTF-8-Byte** in `files.item_filename()` · **[2026-10-30, Nikinger] Titel ≤ 256 Zeichen** (15.5c) — eine Produktregel, kein Pfadschutz mehr; Kern + `maxlength` |
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
| **15.5 ✅** | B6, B7 | Space-Name-Validierung an **einer** Stelle im Kern, aufgerufen von MCP- und REST-Schreibpfaden; Slug kürzen, Titel-Höchstlänge, `OSError` sauber abbilden | `space="team/"` ⇒ abgelehnt; 200 Umlaute im Titel ⇒ weder 500 noch halber Write |
| **15.5b ✅** | UI-Rest 15.4 | `spaces.js`: Hinzufügen und „Entfernen“ nur bei `manageable`; der eigene Name behält „Entfernen“ (E6), danach zurück zur Liste | Browser-Probe an der Wegwerf-Instanz |
| **15.6 ✅** | B9, B10 | Einladungs-Pfad in die Redaktion (`request_log.py`, `logging_setup.py`); `search()` überspringt eine zwischenzeitlich verschwundene Datei | Log enthält den Token nicht; Such-Threads gegen Umbenennungen ⇒ kein `FileNotFoundError` |
| **15.6b ✅** | B3′ | `search()` überspringt eine unlesbare Datei (`OSError`/`ValueError`/`KeyError`/`TypeError`, wie `index._FILE_ERRORS`) mit `CRITICAL` und Pfad | Hand-Edit kaputtes YAML **und** Latin-1-Byte ⇒ Suche liefert die übrigen Items, Log nennt die Datei |
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
> **Verbatim verschoben** nach `phase10_5_block15_review_fixes_plan_anhang.md` (`scripts/move_sections.py`) — dort unter derselben Überschrift.

## Anmerkungen 15.2 — B2/B3/B20 (2026-10-30, Opus)
> **Verbatim verschoben** nach `phase10_5_block15_review_fixes_plan_anhang.md` (`scripts/move_sections.py`) — dort unter derselben Überschrift.

## Anmerkungen 15.3 — B5/B8 (2026-10-30, Opus)
> **Verbatim verschoben** nach `phase10_5_block15_review_fixes_plan_anhang.md` (`scripts/move_sections.py`) — dort unter derselben Überschrift.

## Anmerkungen 15.3b — E5 (2026-10-30, Opus)
> **Verbatim verschoben** nach `phase10_5_block15_review_fixes_plan_anhang.md` (`scripts/move_sections.py`) — dort unter derselben Überschrift.

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

## Anmerkungen 15.5 — B6/B7 (2026-10-30, Opus)

- **B6 reproduziert (tmp-`DATA_ROOT`, MCP):** `create_item(space=…)` als `write:`-Mitglied von
  `team` mit `team/`, `team//`, `./team`, `team/.` ⇒ je **angelegt**, alle Dateien in `team/`,
  Quittung und Frontmatter mit dem **rohen** Namen; `update_item(space="team/")` ebenso (der
  Existenz-Check in `move()` sagt `(root / "team/").is_dir()` = wahr). `team/sub` war schon
  `write_denied` (keine `.share.yml`).
- **Fix B6:** `files.is_valid_space_name()` — **eine** Regel (str, nicht leer, kein `/`, kein NUL,
  kein führender Punkt, nicht reserviert, ≤ 255 Byte), aufgerufen in `Store.create()` und
  `Store.move()` auf das **Argument**, nicht auf `item.space` in `_write_item_file` — sonst würde
  ein schon liegendes Item mit `space: team/` unschreibbar. `rename_space()` und
  `acl.create_space()` hatten je eine eigene Kopie der alten Regel; beide rufen jetzt dieselbe
  Funktion (`AclWriteError` bleibt). Abgelehnt, nicht normalisiert. Die Adapter bekommen keinen
  eigenen Check: MCP ⇒ `invalid: …`, REST ⇒ 422 (beide über den vorhandenen
  `ValidationError`-Weg).
- **B7 reproduziert:** 200 Umlaute ⇒ `OSError 36` beim `mkstemp` (der Pfad im Fehler beginnt mit
  `.itm_…` — die tmp-Datei, nicht die Item-Datei). Update auf 100 CJK ⇒ die Datei am **alten**
  Namen mit neuem Titel und `version: 2`, Umbenennen gescheitert, kein Commit.
- **E3 gemessen:** `os.statvfs().f_namemax` = **255** (ext4, `/home/savefyx`). Item-Datei = Slug +
  17 Byte (`itm_xxxxxxxx__` + `.md`), tmp-Datei = Name + 14 Byte (`.` + Name + `.` + 8 + `.tmp`)
  ⇒ Slug ≤ **224** Byte. Gebaut: **100 Byte**, an einer Zeichengrenze, ohne `-` am Ende, in
  `files.item_filename()` — die eine Stelle, über die Write, Archiv und Papierkorb gehen. Bewusst
  **nicht** in `slugify()`: das baut auch Ordnersegmente, ein Kürzen dort würde bestehende Ordner
  still umbenennen. **Folge:** ein vorhandenes Item mit längerem Slug bekommt beim nächsten Write
  den kurzen Namen (harmlos, Lookup läuft über die ID).
- **Titel-Limit (15.5c, Nikinger: 256):** zuerst ohne gebaut (das Kürzen erfüllt das Done-when),
  dann auf Nikinger-Entscheidung `MAX_TITLE_CHARS = 256` **Zeichen** in `store.create()`/`update()`
  — beim Update nur ein **geänderter** Titel (die UI schickt ihn bei jedem Speichern; ein von Hand
  verlängerter Titel bliebe sonst unspeicherbar) — und `maxlength="256"` an beiden Titelfeldern.
  3 Wächter (Store 2, REST 1); Gegenlauf Limit aus **3 rot**, Bedingung „geändert“ aus **1 rot**.
- **Nebenbei (selbe Fehlerklasse):** ein Ordnersegment > 255 Byte ⇒ vorher `OSError 36` beim
  `mkdir`, jetzt `ValidationError` in `validate_folder()` (abgelehnt, nicht gekürzt — ein
  gekürzter Name wäre ein anderer Ordner; die Grenze ist die Dateisystemgrenze, kein bestehender
  Ordner kann darüber liegen).
- **Wächter (14 Funktionen, 40 Fälle):** `test_files.py` 6 Funktionen / 22 Fälle (Kappe an der Zeichengrenze, kurzer
  Slug unverändert, **echter** Write des schlimmsten tmp-Namens gegen `f_namemax`, Space-Namen
  14 abgelehnt / 4 angenommen, Ordnersegment) · `test_store.py` (create × 7 Namen inkl.
  `../draussen` und NUL, move × 3, 200 Umlaute mit Git, Update auf 100 CJK: neuer Name, Suche,
  genau **ein** Commit) · `test_tools.py` (create × 3, `update_item(space=)`) · `test_api.py`
  (POST `fabian/` ⇒ 422 ohne Datei; POST 200 Umlaute ⇒ 201, PATCH 100 CJK ⇒ 200, v2).
- **Gegenlauf, im Code neutralisiert:** Slug-Kappe aus ⇒ **6 rot** (3 Dateien-, 2 Store-, 1 REST-
  Wächter) · Space-Prüfung in `create`/`move` aus ⇒ **15 rot** (Store 10, MCP 4, REST 1) ·
  Ordner-Länge aus ⇒ **1 rot**. Jeweils nur die Wächter dieses Fixes.
- **Live-Frage vor Deploy D (Nikinger, read-only, wie die E5-Durchsicht):** B6 stand seit P6
  live offen. Der Fix heilt kein schon liegendes Item mit `space: team/` (es bleibt „fremd“ und
  wird von `rename_space` übersprungen). Prüfung: jede `.md` unter `DATA_ROOT`, deren
  `space:`-Zeile nicht dem obersten Verzeichnis entspricht —
  `cd <DATA_ROOT> && find . -path ./._trash -prune -o -name '*.md' -print0 | while IFS= read -r -d '' f; do d=${f#./}; d=${d%%/*}; s=$(sed -n 's/^space: *//p' "$f" | head -1); [ "$s" = "$d" ] || echo "$f: $s"; done`
  — 0 Zeilen ⇒ kein Übergang. **Gefahren 2026-10-30 (Claude Code, Nikinger-Auftrag, read-only):
  0 Treffer** bei 263 Items; längster Titel 89 Zeichen; 4 Slugs > 100 Byte. (Eine Nicht-Item-`.md` ohne `space:` erscheint mit leerem Wert; an einer Wegwerf-Kopie mit einem `space: team/`-Item erprobt: genau diese Zeile).

## Anmerkungen 15.5b — UI-Rest aus 15.4 (2026-10-30, Opus)

- **Auftrag:** Backlog aus 15.4, vom Nikinger an Claude Code übergeben („your call?“). Entschieden:
  **vor Deploy D bauen** — Deploy D liefert B4 aus; ohne diesen Schnitt sähe ein Schreib-Gast im
  fremden Home-Space Knöpfe, die mit „Keine Verwaltungsrechte“ scheitern.
- **Gebaut (`spaces.js`, `app.html`):** das Hinzufügen-Formular (`#space-member-add`) und jeder
  „Entfernen“-Knopf nur bei `manageable` aus `GET …/members` (seit 15.4 dieselbe Frage wie der
  Server); der **eigene** Name behält „Entfernen“ (E6). **Fund beim Bauen:** nach dem
  Selbst-Austragen lud der Dialog die Mitgliederliste neu — ohne Leserecht 403, das Panel blieb mit
  Fehlermeldung offen. Jetzt: Toast „Ausgetragen · <space>“, zurück zur Liste, `loadOverview()`.
- **Beleg:** `probes/p105_b15_5b_gast_knoepfe_probe.py` (Wegwerf 8799, PID-Datei) — Fix **4/4
  grün**; Gegenlauf mit dem alten `spaces.js`/`app.html` **3 rot** (`gast_formular`,
  `gast_knoepfe`, `austragen`), `team_verwalten` grün in beiden (Regressionszelle). **Erster
  Gegenlauf war zahnlos:** die Zelle maß den neuen Container, den das alte Markup nicht hat (fehlt
  = „versteckt“) — auf den Knopf umgezielt, der in beiden existiert, und beide Läufe neu gefahren.

## Anmerkungen 15.6 — B9/B10 (2026-10-31, Opus)

- **B9 gebaut (`logging_setup.py`):** `_TOKEN_SEGMENT_RE` = `(/mcp/|/ui/invite/)…` — **ein** Muster
  für beide Verbraucher (`AccessLogASGI` redigiert den Pfad direkt, `TokenScrubbingFilter` über
  `_SECRET_PATTERNS`). Gegengelesen, ob es weitere Lecks gibt: `routes_auth.py` und
  `peek_invite`/`consume_invite` loggen nichts (der Store speichert nur den Hash), es gibt keinen
  CSP-Report-Endpunkt, keine Zeile mit `request.url`; die übrigen Pfadparameter
  (`family_id`, `item_id`, `space`) sind keine Einlöse-Geheimnisse.
- **B10 gebaut (`Store.search()`):** `FileNotFoundError` je Zeile ⇒ die Zeile **unter dem Lock**
  neu holen und einmal neu lesen; keine Zeile (Papierkorb) oder Datei weiter weg (von Hand
  gelöscht) ⇒ überspringen. **Abweichung vom Wortlaut §3 („überspringen“), bewusst:** reines
  Überspringen ließe ein umbenanntes, also **existierendes** Item aus Seite und `total` fallen — ein
  Agent hielte es für gelöscht. Das Lock über alle Lesezugriffe zu halten, sperrte jeden Writer
  für die Dauer einer Suche; gefangen wird nur `FileNotFoundError`, kein `OSError`, kein
  `FrontmatterError`. Kein Adapter liest Item-Dateien selbst (gegengelesen: `phase2_mcp`,
  `phase5_ui`).
- **Wächter:** B9 — `test_request_log.py :: test_http_event_redacts_invite_token` (GET/POST, Token
  aus `create_invite()`, ganzer Logpuffer), `test_logging.py ::
  test_scrubbing_filter_redacts_invite_token_in_dict_message`. B10 — drei **deterministische**
  (`index.all_rows` gepatcht: nach dem Index-Read läuft Umbenennen / `trash` / Löschen von Hand)
  und **ein** Thread-Wächter wie im Review (3 Leser, 300 Updates reihum über 10 Items, 10
  Papierkorb-Züge, Umschaltintervall `1e-6`, ~5–7 s).
- **Gegenlauf:** B9 ohne Fix **3 rot** (GET, POST, Filter). B10 ohne Fix: die drei
  deterministischen **3/3 rot**; der Thread-Wächter in der ersten Fassung (ein Ziel-Item) nur **2
  von 3** rot — zahnlos genug, um umgebaut zu werden (Updates reihum, damit die Lage im
  `ORDER BY id` keine Rolle spielt), danach **5 von 5** rot.
- **Fund B3′ (Advisor-Probe, nicht gebaut):** eine indizierte Datei, von Hand zu ungültigem YAML
  editiert, lässt **jede** `search()` mit `FrontmatterError` scheitern — für alle Nutzer, bis die
  Datei repariert ist. 15.2 hat das für den **Neuaufbau** gelöst, nicht für den laufenden Betrieb.
  Entscheidung beim Nikinger: vor Deploy D (je Zeile überspringen + `CRITICAL` mit Pfad, wie
  `rebuild_index()`) oder Backlog.
- **15.6b gebaut (2026-10-31, Nikinger: vor dem Deploy):** `search()` liest jede Zeile über
  `read()` — unlesbar (dieselbe Fehlermenge wie `index._FILE_ERRORS`) ⇒ `CRITICAL` mit Pfad, Zeile
  fehlt in Seite und `total`; `FileNotFoundError` geht weiter an den B10-Weg. **Fund beim Bauen:**
  `type(exc).__name__` rief `None` auf — `type` ist in `search()` der Filter-Parameter; jetzt
  `exc.__class__`. `get()` der kaputten Datei wirft weiter (betrifft nur das eine Item).
  Wächter: `test_search_skips_a_hand_broken_file_and_says_where` (YAML, Latin-1); Gegenlauf
  (Fehlermenge leer) **2 rot**, die B10-Wächter bleiben grün.
