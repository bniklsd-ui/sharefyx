---
status: live
purpose: Phase-Head Space-Verwaltung, Mehrfachauswahl, Konsolidierung — Scope, harte Regeln, Modulstatus, aktueller Session-Handover
read-when: Arbeiten in phase7_spaces_admin/ oder an den in §0.3/§3 des Plans genannten Dateien in storage/mcpserver/webui/scripts — zuerst lesen, zusammen mit dem neuesten Session-stopped-Block
detail: L2
up: ../CLAUDE.md
down:
  - ../docs/concepts/phase7_spaces_admin_plan.md   # voller Plan, Entscheidungen P7-A–P7-V, §0.1 gelockte N1–N10, Steps 0/A/C/B/Z
  - ../docs/concepts/PHASE6_CLOSEOUT_HANDOVER.md   # Herkunft: P6-Status, §4.1/§4.2, offene Entscheidungen §5.1–§5.7
  - ../phase6_shares/ITEM_MOVE_PLAN.md              # §9 Mehrfachauswahl (P6-AK–AN) — Block B baut das, unverändert
  - SESSIONS_ARCHIVE.md                             # ältere Session-Blöcke, newest-first
updated: 2026-08-23 (Step 0 gestartet, Doku-Audit gefahren, Skelett angelegt)
---
# CLAUDE.md — Phase 7: Space-Verwaltung, Mehrfachauswahl, Konsolidierung (`phase7_spaces_admin/`)

> Kein eigenes Python-Paket (wie `phase3_edge/`, `phase6_shares/`, `phase6_5_tools_images/`) —
> Servercode bleibt in `storage`/`mcpserver`/`webui`/`scripts`. **Quelle der Wahrheit ist der
> Code, nicht dieses Dokument.**

---

## Mission (zuerst lesen)

Drei Blöcke, ein Aufräumkapitel davor. **Reihenfolge: 0 → A → Gate → C → B** — Block C trägt den
Namen dieser Phase (Space-Admin-UI, seit P6 Step 7 Commit 6 in `app.html` als „kommt in Phase 7"
reserviert) und fällt unter Druck nie vor Block B. Details, alle zehn Nikinger-Fragen N1–N10,
gelockte Entscheidungen P7-A–P7-V, Berührungsfläche/Tabu, Schritt-Sequenz, Testliste,
Abnahmezeilen: `docs/concepts/phase7_spaces_admin_plan.md`.

## Scope (Kurzform, Details: Plan §0.2)

- **DRIN:** Item-ID sichtbar+auffindbar (Fabian-Meldung), Bild-Entfernen-Knopf (schließt
  P6.5-12), Feld-Whitelist an `_items_patch` (schließt O6), Doku-Audit Zeilen 8–16 (Handover
  §4.1, **Step 0 dieser Session**), Sichtbarkeits-Migration live (N4), dritter Principal
  `testnutzer-p7` + `testcred.py`, formaler Abschluss Phase 6.5, Space-Verwaltung in der
  Weboberfläche (volle `spacectl.py`-Parität, N5/N6/N7/N8/N9), Mehrfachauswahl
  (`ITEM_MOVE_PLAN.md` §9, N2).
- **DRAUSSEN:** FastMCP-4-Umstieg, `owner:`-Feld, Löschen von Items, Rechteverwaltung über
  MCP-Tools, automatische `_trash/`-Räumung, Funnel-Watchdog, Body-Volltextsuche in der Web-UI,
  Mehrfachauswahl für andere Aktionen als Verschieben.

## Harte Regeln dieser Phase (nicht verhandelbar)

- Alle Hard Rules aus Root-`CLAUDE.md` gelten unverändert.
- **P7-B — Berührungsfläche.** Auf: `storage/`, `webui/`, `mcpserver/tools.py`,
  `scripts/spacectl.py`, `scripts/diagnose.sh`, `docs/`. Tabu (`git diff` bleibt leer):
  `mcpserver/asgi.py`, `mcpserver/{server,permissions}.py`,
  `authserver/{crypto,totp,passwords,resolver,flows}.py`. `mcpserver/app.py` darf bei
  nachgezogener Signatur angefasst werden, jede solche Änderung wird im Session-Block benannt.
- **P6-D gilt unverändert weiter.** Charakterisierungstests
  (`phase6_shares/tests/test_characterization.py`, drei Golden Files) laufen vor und nach jedem
  Umbau an `storage/` und müssen byte-identisch grün sein.
- **N7/§0.4 Punkt 1 — Selbstaussperrung ist möglich, bewusst kein Guard.** Jedes
  `write:`-Mitglied darf sich selbst aus der Mitgliederliste entfernen. Dokumentierter Rückweg:
  `spacectl.py add-member <space> <user> --write`.
- **N8/§0.4 Punkt 2 — Space-Entfernen verliert die Space-Zuordnung, nie die Items.** Items wandern
  vorher ins `_archive/` des Ausführenden; nur Müll (`_trash/`, verwaiste `_assets/`) stirbt mit
  dem `rmtree`.

## Modul-Status

| # | Modul | Step | Status | Tests |
|---|---|---|---|---|
| 1 | Haushalt, Verifikationsdurchlauf (0.1–0.5), Skelett (0.6), sechste Contract-Öffnung angekündigt (0.7) | 0 | ✅ **vollständig** — siehe Session-Block 2026-08-23 | 0 (Skelett, wie P1/P6/6.5 Step 0) |
| 2 | A1 (ID sichtbar+auffindbar: `api.py :: _items_get` ID-Zweig, `idChip()` in Editor + Nur-lesen, Such-Placeholder) + A2 (Tool-Beschreibungen: `_TITLE_NOT_ID_HINT` an vier Lese-Tools) | A | 🟡 **gebaut, JS nicht browserverifiziert** — Backend+Tools per `pytest` grün, Editor-Chip/Copy-Verhalten noch nicht in einem echten Browser gesehen | +5 (4 `phase5_ui/tests/test_api.py` + 1 `phase2_mcp/tests/test_tools.py`); 833 gesamt |

| 3 | A3 (Bild-Entfernen-Knopf, schließt P6.5-12): `markdownToHtml()` bekommt dritten Kontextschlüssel `assetIds` (V73 — sonst rendert ein entferntes Bild ein kaputtes `<img>`, nicht Alt-Text), `renderAssetStrip()`/`idChip`-Muster in `editor.js`, `DELETE .../assets/{id}` (bereits vorhanden). **Nebenfund beim Bauen, mitbehoben:** `_items_patch`/`_items_append`/`_items_archive` gaben `item_to_json()` bisher ohne `assets=` zurück — jede Antwort log `assets: []`, auch mit vorhandenen Bildern; `afterWrite()` lädt den Editor direkt aus genau dieser Antwort neu, ohne den Fix wäre die Asset-Leiste nach jedem Speichern leer gewesen | A | 🟡 **gebaut, JS nicht browserverifiziert** — Backend-Nebenfund per Test bewiesen, Entfernen-Knopf/Alt-Text-Verhalten noch nicht in einem echten Browser gesehen | +1 `phase5_ui/tests/test_api.py`; 834 gesamt |

| 4 | A4 (Feld-Whitelist an `_items_patch`, schließt O6): `_PATCH_FIELDS`-Konstante (korrigierte Liste aus V74 — `format` ergänzt), Prüfung direkt nach `body = await _json_body(request)`, vor jeder Rechteprüfung | A | ✅ **vollständig** | +2 `phase5_ui/tests/test_api.py`; 836 gesamt |

*(Weitere Zeilen entstehen mit dem Rest von Block A/C/B — siehe Plan §4 für die vollständige Schritt-Sequenz.)*

## Geerbte Contracts

**[2026-08-23, P7 Step 0] Sechste, benannte Öffnung des P1-Contracts angekündigt** (Plan §4 C1,
P7-P): `phase1_storage/storage/acl.py` bekommt eine Schreibseite — `read_share_file()`,
`write_share_file()`, `add_member()`, `remove_member()`, `create_space()`, `remove_space_dir()`,
`spaces_referencing()`, `AclWriteError`. Extraktion aus `spacectl.py` (Referenz:
`spacectl.py:90–107, 113–127, 133–148, 185–242`), keine Neuentwicklung, byte-identisches
Verhalten Bedingung für den Regressionsbeweis der 20 bestehenden `test_spacectl.py`-Tests. Wird
in Block C Step C1 umgesetzt, hier nur angekündigt — nach Phasenabschluss wieder geschlossen,
siehe `phase1_storage/CLAUDE.md`.

## Abnahmestand (Plan §6, P7-1–P7-24 plus P7-12b)

**Statusregel wie in P4/P5/P6/6.5: ✅ heißt live-verifiziert durch einen Menschen, nicht
„gebaut".** Alle Zeilen ⬜ **noch nicht angefangen** — Block A/C/B haben in dieser Session noch
keinen Code bekommen, nur Step 0 (Haushalt) lief.

| # | Kriterium | Wer | Status |
|---|---|---|---|
| P7-1 | Item-ID sichtbar + Klick kopiert | Niklas | ⬜ gebaut, ungeprüft |
| P7-2 | ID-Suche findet Item spaceübergreifend | Niklas | 🟡 Backend per Test bewiesen, keine Browserprobe |
| P7-3 | ID-Suche auf nicht lesbares Item → leere Liste | Claude Code, Test | ✅ `test_id_lookup_respects_read_permission` |
| P7-4 | Claude nennt Items beim Titel, nicht der ID | Niklas, echter Connector | ⬜ Text steht in vier Tool-Beschreibungen, kein Connector-Beweis |
| P7-5 | Bild im Editor entfernbar, landet in `_trash/` | Niklas | ⬜ gebaut, ungeprüft |
| P7-6 | `PATCH` mit Tippfehler-Feld abgewiesen (O6) | Claude Code, Test | ✅ `test_items_patch_rejects_an_unknown_field` |
| P7-7 | Speichern/Verschieben/Freigeben nach Whitelist unverändert | Niklas | 🟡 Whitelist per Test gegen die real gesendeten Felder gepinnt, keine Browserprobe |
| P7-8 | Migration: 0 `.md` ohne `visibility:` | Nikinger + Claude Code | ✅ `--apply` 2026-08-23, `items_migrated:73` (deckungsgleich Dry-Run), `grep -L '^visibility:'`→0, 3 Commits (niklas/fabian/IT-Sekus-Projekt) |
| P7-9 | `clients`/`token_families` sinken nach realem Purge (ab 2026-08-28) | Niklas | ⬜ |
| P7-10 | `testnutzer-p7` existiert, schreibt einmal | Nikinger + Claude Code | ⬜ |
| P7-11 | `testnutzer-p7` sieht nur sein item-level Item | Claude Code | ⬜ |
| P7-12 | `testnutzer-p7` entfernt, Keyring-Eintrag weg | Claude Code | ⬜ |
| P7-12b | Claude Code loggt sich ohne Nikinger als `testnutzer-p7` ein | Claude Code | ⬜ |
| P7-13 | Phase 6.5 formal abgeschlossen | Claude Code | ⬜ |
| P7-14 | Eigener Space im Browser freigegeben, Empfänger sieht ihn | Niklas + `testnutzer-p7` | ⬜ |
| P7-15 | Zurücknehmen kein Re-Auth, Erweitern eines | Niklas | ⬜ |
| P7-16 | Neuer geteilter Space im Browser angelegt | Niklas | ⬜ |
| P7-17 | Name-Kollision mit Principal abgewiesen | Claude Code, Test | ⬜ |
| P7-18 | Home-Space nicht entfernbar (Knopf fehlt, Route 403) | Claude Code, Test+Browser | ⬜ |
| P7-19 | Space mit N Items entfernt → alle N im `_archive/` | Niklas | ⬜ |
| P7-20 | Space mit nicht-schreibbarem Item nicht entfernbar, kein Teil-Move | Claude Code, Test | ⬜ |
| P7-21 | Entfernen ohne Namensbestätigung abgewiesen | Claude Code, Test | ⬜ |
| P7-22 | `space_admin_enabled=False` → Menüpunkt weg, Routen 404 | Claude Code, Test | ⬜ |
| P7-23 | N-Auswahl wandert in einem Vorgang, ein Commit je Item | Niklas | ⬜ |
| P7-24 | Ein rechteerweiterndes Item in Auswahl → ein Formular, nicht N | Niklas | ⬜ |

**Geerbt und in dieser Phase nicht adressiert:** P6-Zeilen 7, 9, 14–17, 23, 25, 29, 30 sowie
P6.5-14 — bleiben im Handover offen, kein stilles Abhaken (Plan §6, Fußnote).

## Session stopped — 2026-08-23 (Step 0 gestartet: Verifikationsdurchlauf + Doku-Audit)

**Auftrag:** Erste Claude-Code-Sitzung von Phase 7. Einstieg ist Step 0, erster Handgriff das
Doku-Audit aus Handover §4.1 (Plan §4 Step 0.2).

**0.1 — `pytest`-Ausgangsstand:** `828 passed`, deckungsgleich mit der Erwartung aus dem P6.5-
Handover-Nachtrag. **V71 geschlossen.**

**0.2 — Doku-Audit, mit SHA-Beweis je Zeile.** `LIVE = f96125e` (`/opt/sharefyx/current`).
Geprüft per `git merge-base --is-ancestor <sha> $LIVE` gegen die Commits, die den jeweiligen
Modul-Status-Zeilen 8–16 in `phase6_shares/CLAUDE.md` entsprechen:

| Zeile | Modul | Commit(s) | Ergebnis |
|---|---|---|---|
| 8 | Step 7a Textfarben + Wortmarke-Nachtrag | `562d279`, `15cf054` | IST live |
| 9 | Step 7 Commit 0 (app.js-Split) | `1959de8` | IST live |
| 10 | Step 7 Commit 1 (echter Ordnerbaum) | `fbcdb9f` | IST live |
| 11 | Step 7 Commit 2 (Sichtbarkeits-Chip) | `e48c039` | IST live |
| 12 | Step 7 Commit 3 (Ordner anlegen+Verschieben, K4) | `5db817e` | IST live |
| 13 | Step 7 Commit 4 (Drag & Drop) | `0c504a4` | IST live |
| 14 | Step 7 Commit 5a (Re-Auth-Gate Backend) | `928908c` | IST live |
| 15 | Step 7 Commit 5b (Freigabe-Dialog+Re-Auth-Formular) | `cd94061` | IST live |
| 16 | Step 7 Commit 6 (`space_admin_enabled`-Stub) | `0378c41` | IST live |

Zusätzlich geprüft, weil dieselbe Fehlbehauptung an zwei weiteren Stellen stand: **Vormerkungen
Punkt 2** (Space-zu-Space-Verschieben, Step 7b, drei Commits `9274346`/`3f476c7`/`abeaba6`) — alle
drei ebenfalls Vorfahren von `f96125e`.

**Befund: die Doku war stale, nicht der Code.** Alle neun geprüften Zeilen (8–16) trugen „gebaut,
noch nicht deployt" bzw. „Deploy beim Nikinger" — tatsächlich sind sie seit dem Phase-6.5-Deploy
(`f96125e`, 2026-08-21) live. **Wichtig, per Advisor-Hinweis eingehalten: „deployt" ≠
„abgenommen".** Diese Korrektur ändert ausschließlich den Deploy-Status der Zeilen, **nicht**
ihren Abnahmestatus — Zeile 8 z. B. bleibt ohne eigenen Abnahmematrix-Punkt, die Space-Move-
Zeilen 25–30 bleiben „offen", nur das „noch nicht deployt" darin ist jetzt falsch und wurde
entfernt. Korrigiert in `phase6_shares/CLAUDE.md` (Zeilen 8–16 + Vormerkungspunkt 2), in
Root-`CLAUDE.md`s Current-State-Absatz (trug denselben veralteten Satz zu `d348e2e`, obwohl
`phase6_shares/CLAUDE.md` die Korrektur vom 2026-08-23 schon hatte — Root hatte sie nie
bekommen) und in `docs/INDEX.md`s `phase6_shares/CLAUDE.md`-Zeile (trug „Step 7b vollständig
gebaut … noch nicht deployt").

**0.3 — Link-Auflösung.** Ein echter Fund: `docs/PROMPTS.md`s `up: CLAUDE.md` löste relativ zu
`docs/` auf `docs/CLAUDE.md` auf (existiert nicht) statt `../CLAUDE.md`. Behoben. Sonst leer.

**0.4 — Indexzeile je `.md`.** Leer, nach Ausschluss von `.pytest_cache/` (generiert, wie in
0.5s Find-Kommando bereits vorgesehen, hier nur im Plan-Kommando vergessen) und `docs/INDEX.md`
selbst (Selbstverweis erwartungsgemäß nicht vorhanden).

**0.5 — Softcap.** 12 Treffer (Plan-Erwartung aus der Planungssession: 11 — Delta ist
`phase7_spaces_admin_plan.md` selbst, nach der Zählung angelegt). Alle 12 sind 📕/📦-konform.
`phase6_shares/CLAUDE.md` (39.080 B) und `ITEM_MOVE_PLAN.md` (40.261 B) bleiben grenzwertig unter
dem Cap (40.960 B) — die Zeilen-8–16-Korrektur oben blieb bewusst minimal (Zellen-Edits + eine
datierte Korrekturzeile, keine neue Erzählung), um den Cap nicht zu reißen. Größe nach der
Korrektur nicht erneut über 40 KB.

**0.6 — Skelett angelegt.** `phase7_spaces_admin/CLAUDE.md` (diese Datei), `SESSIONS_ARCHIVE.md`
(leer), `tests/conftest.py` (leer). `ROADMAP.md`: fehlende P6.5-Tabellenzeile ergänzt (echte
Vorphasen-Lücke, beim Bearbeiten derselben Tabelle mitgefunden, datiert korrigiert) + neue
P7-Zeile + eigener Abschnitt. `docs/INDEX.md`: „Active phase" auf Phase 7 umgestellt, neue Zeilen
für Plan/Head/Archiv.

**0.7 — Sechste Contract-Öffnung angekündigt.** `phase1_storage/CLAUDE.md`, datierter Absatz mit
der Funktionsliste aus Plan §4 C1.

**DoD Step 0:** alle sechs Punkte gefahren, Ergebnis protokolliert (0.1/0.3/0.4 „nichts zu tun"
außer dem PROMPTS.md-Link-Fund; 0.2/0.5/0.6/0.7 mit Ergebnis); Audit-Tabelle mit SHA je Zeile
oben; Skelett steht; `pytest` unverändert bei 828.

**Nächster Schritt:** Block A (Fixes + Phase-6.5-Abschluss) — beginnt mit einem live
`migrate_visibility.py --apply` gegen den echten `DATA_ROOT` und dem Anlegen von
`testnutzer-p7`. Beides ist Nikinger-Sache zu autorisieren, nicht Claude Codes eigene
Entscheidung — Session hier bewusst gestoppt, um das einzuholen.

**Nachtrag, selber Tag — Nikinger-Freigabe „per Plan, mit Step A" erhalten, A1+A2 gebaut.**

**V73/V74 vorab geklärt, wie vom Advisor verlangt:**
- **V73 (A3-Vorbereitung):** `markdown.js` löst `asset:<id>` unabhängig davon auf, ob die
  Asset-Datei noch existiert — die Regex prüft nur die URL-**Form**, nicht die Existenz. Ein
  entferntes (nach `_trash/` verschobenes) Bild rendert deshalb heute ein **kaputtes `<img>`**,
  keinen Alt-Text. A3 braucht also tatsächlich den geplanten dritten Kontextschlüssel
  `assetIds` — noch nicht gebaut, folgt mit A3 selbst.
- **V74 (A4-Vorbereitung):** `grep 'method: "PATCH"' -B15` über `editor.js`/`list.js`/
  `dialogs.js` enumeriert. **Der Plan-Entwurf für `_PATCH_FIELDS` fehlte `format`** —
  `editor.js :: saveItem()` sendet `format: "markdown"` bei **jedem** Speichern
  (`editor.js:335`); ohne dieses Feld in der Whitelist hätte A4 jedes UI-Speichern mit `400`
  gebrochen. Korrigierte Feldliste notiert, wird mit A4 geschrieben.

**A1 — ID sichtbar + auffindbar (`api.py :: _items_get`, `editor.js`, `app.html`, `app.css`):**
ID-Zweig vor dem bestehenden Store-Aufruf (`ITEM_ID_RE.fullmatch`), space-/ordnerübergreifend
(P7-D/E), Rechteprüfung unverändert davor — eine ID ohne Leserecht liefert `total: 0`, nie
403/404 (kein Existenz-Orakel). `idChip(itemId)` (neu, `editor.js`) in beiden Detailansichten
(readonly `roMetaEl`, editierbar `#meta-item-id`), Klick kopiert über
`navigator.clipboard.writeText`, kein `execCommand`-Fallback. Such-Placeholder nennt jetzt
`itm_…`. **Tabu-Probe:** `git diff phase1_storage/storage/` leer (P7-D eingehalten).

**A2 — Tool-Beschreibungen nennen Titel, nicht ID (`mcpserver/tools.py`):** neue Konstante
`_TITLE_NOT_ID_HINT`, wörtlich identisch an `search_items`/`get_item`/`get_item_meta`/
`create_item` angehängt, gleiche Bauart wie `WRITE_TOOL_DIVISION`/`_LIST_SPACES_POINTER`.

**Tests:** +5 (`test_items_get_finds_an_item_by_its_id`,
`test_id_lookup_ignores_space_and_folder_filter`, `test_id_lookup_respects_read_permission`,
`test_id_lookup_with_unknown_id_returns_empty_list` in `phase5_ui/tests/test_api.py`;
`test_tool_descriptions_tell_the_agent_to_name_titles_not_ids` in
`phase2_mcp/tests/test_tools.py`). `pytest -q` **833 passed** (828 + 5).

**Ehrlich offen:** DoD verlangt eine echte Browserprobe für den Chip (sichtbar, kopierbar) und
einen echten Connector-Beweis für A2 (P7-4) — **beides diese Session nicht gefahren**, nur
Backend/Tool-Ebene per `pytest`. Abnahmezeilen P7-1/P7-4 bleiben deshalb ⬜, P7-2 🟡 (Backend
bewiesen, keine Browserprobe), P7-3 ✅ (reiner Test-Fall, kein Mensch nötig).

**Nächster Schritt:** A3 (Bild-Entfernen-Knopf, V73-Konsequenz eingeplant) und A4 (Feld-
Whitelist, korrigierte Liste aus V74 oben) folgen als eigene Commits, wie mit dem Advisor
abgestimmt.

**Nachtrag, selber Tag — A3 gebaut (V73-Konsequenz umgesetzt).** `markdown.js :: inlineMarkdown()`
prüft jetzt vor jedem `asset:<id>`-Auflösen, ob die ID in einem mitgegebenen `assetIds` steht —
fehlt sie, rendert der Alt-Text statt eines `<img>` (ohne `assetIds` bleibt das alte Verhalten,
`updates.js`s Aufrufe sind unberührt). `editor.js`: `renderAssetStrip(item)` (neu) zeigt jedes
Asset mit Dateiname + „×"; Klick fragt per `confirmDialog()` nach, Wortlaut „entfernen"/„Papier-
korb" (nie „löschen", der Server verschiebt nur nach `_trash/`), ruft `DELETE .../assets/{id}`
(bereits vorhanden, kein neuer Serverpfad), aktualisiert `item.assets` lokal und rendert Leiste +
Vorschau neu. `snapshotFromItem()` trägt jetzt `assets` mit, ein neu hochgeladenes Bild wird
sofort in `state.editingSnapshot.assets` gepusht (sonst zeigte die Leiste es erst nach dem
nächsten Neuladen).

**Echter Nebenfund beim Bauen, nicht Teil des Plans:** `_items_patch`/`_items_append`/
`_items_archive` (`webui/api.py`) reichten `item_to_json()` bisher **ohne** `assets=` durch —
jede Antwort trug `assets: []`, unabhängig vom tatsächlichen Bestand. `editor.js :: afterWrite()`
lädt den Editor direkt aus genau dieser Antwort neu (`loadEditorFromItem(item, …)`) — ohne den
Fix hätte jedes Speichern nach einem Bild-Einfügen die Asset-Leiste geleert und `assetIds` beim
nächsten Render-Zyklus leer gemacht, was ein soeben eingefügtes Bild fälschlich als Alt-Text
gezeigt hätte. Behoben: alle drei Endpunkte reichen jetzt `assets=store.list_assets(item.id)`
durch, wie `_items_get_one` es schon tat. Bewusst **nicht** mitbehoben: `_map_store_error()`s
Konfliktantwort (`detail.current`) trägt weiterhin keine `assets` — das ist eine reine
Modulfunktion ohne `store`-Zugriff, eine Signaturänderung hätte jeden Aufrufer in der Datei
berührt; der Konfliktdialog zeigt ohnehin keine Bildvorschau, also kein beobachtbarer Fehler,
nur vorsorglich notiert.

**Test:** +1 `phase5_ui/tests/test_api.py :: test_assets_survive_a_patch_response` (Bild
hochladen, PATCH + append, beide Antworten tragen das Asset). `pytest -q` **834 passed**
(833 + 1). Tabu-Probe (`storage/`) weiterhin leer — der Fix blieb vollständig in `webui/api.py`.

**Ehrlich offen, wie bei A1/A2:** keine Browserprobe für den Entfernen-Knopf/Alt-Text-Übergang
diese Session — P7-5 bleibt ⬜ „gebaut, ungeprüft" in der Abnahmematrix.

**Nachtrag, selber Tag — A4 gebaut (schließt O6).** `_PATCH_FIELDS`-Konstante in `webui/api.py`,
Prüfung `unknown = sorted(set(body) - _PATCH_FIELDS)` direkt nach `body = await
_json_body(request)`, vor jeder Rechteprüfung (unbekannte Felder werden abgewiesen, bevor
irgendetwas anderes über den Request nachdenkt). Liste ist die durch V74 korrigierte Fassung
(inkl. `format`, siehe Nachtrag oben) — `version`/`title`/`body`/`status`/`due`/`tags`/`links`/
`type`/`format`/`folder`/`space`/`visibility`/`share_read`/`share_write`/`password`/`totp`.
**Zwei Tests:** `test_items_patch_rejects_an_unknown_field` (`spce`-Tippfehler-Fall aus
`ITEM_MOVE_PLAN.md` §112, Datei bleibt byte-identisch unverändert) und
`test_items_patch_accepts_every_field_the_ui_sends` (pinnt `_PATCH_FIELDS` als Obermenge der
real von `editor.js`/`list.js`/`dialogs.js` gesendeten Schlüssel). **Ein Plan-Detail korrigiert
beim Testen, nicht angenommen:** der Plan-Text nennt „400 validation_failed" für den
Zurückweisungsfall — `webui/errors.py` bildet `validation_failed` durchgehend auf `422`
ab (Unprocessable Entity), nicht 400; der Test pinnt den tatsächlichen Code.

**Tests:** `pytest -q` **836 passed** (834 + 2). Tabu-Probe (`storage/`) weiterhin leer.

**Block A damit vollständig: A1, A2, A3, A4 gebaut, alle vier nur backend-/tool-seitig
verifiziert (`pytest`), keine der vier Browser-/Connector-Proben diese Session gefahren.**
Verbleibend in Block A: A5 (Sichtbarkeits-Migration, braucht den Nikinger für `--apply`), A6
(Purge-Gate, kalendarisch erst ab 2026-08-28), A7/A7b (dritter Principal `testnutzer-p7`, braucht
den Nikinger für die Einladung), A8 (formaler Abschluss Phase 6.5, setzt A3/A7 voraus). Session
hier bewusst gestoppt — die nächsten Schritte brauchen entweder den Nikinger direkt oder bauen
auf etwas auf, das er noch anstoßen muss.

**Nachtrag, selber Tag — zwei Vorarbeiten erledigt, die Claude Code selbst darf (Advisor-
Hinweis), damit der Nikinger-Handgriff kein blinder Griff wird:**

**A5 Schritt 2 (Claude-Code-Sache laut Plan): `migrate_visibility.py --dry-run` gegen den
echten `DATA_ROOT` gelaufen** (`--data-root /home/savefyx/savefyx-data`, Default ist bereits
`--dry-run`, kein `--apply`). Ergebnis: **`items_migrated: 73`, `dry_run: true`, `spaces_touched:
["IT-Sekus-Projekt", "fabian", "niklas"]`** — exakte Deckung mit der Plan-Erwartung (Handover §1
Punkt 4). Alle 73 Zeilen zeigen `"before": null, "after": "private"`. Kein Schreibzugriff (Skript
selbst berichtet `dry_run: true`, kein `git log`-Nachtrag im `DATA_ROOT` geprüft nötig, da das
Skript bei `--dry-run` laut eigenem Code keinen Store-Write auslöst). **A5 Schritt 3 (`--apply`)
bleibt Nikinger-Sache (P7-H) — nicht ausgeführt.**

**V75 geschlossen, gegen eine Wegwerf-Instanz, nicht den echten `DATA_ROOT`:** `spacectl.py
create-space testnutzer-p7` gegen ein Temp-Verzeichnis — Space-Name mit Bindestrich angenommen,
kein Sonderzeichen-Fehler (`_cmd_create_space` prüft nur `/`, führenden `.`, `RESERVED_DIR_NAMES`
— ein Bindestrich fällt in keine der drei Kategorien). `Store.create("testnutzer-p7", ...)`
direkt danach: Item angelegt, Datei liegt unter `testnutzer-p7/itm_…__v75-testprobe.md`,
`store.search(space="testnutzer-p7")` findet es wieder. **Der Bindestrich übersteht Anlegen,
Schreiben und Suchen — keine Sonderbehandlung nötig, `authctl.py invite --space
testnutzer-p7` kann unverändert kommen.**

**Zwei offene Fragen für den Nikinger, bevor A5/A7 weitergehen können (nicht von Claude Code
entscheidbar):**
1. **A5 Schritt 1** (`docs/UPDATE_LOG.md`-Eintrag, muss auf den `--apply`-Tag datiert sein,
   `deploy.sh` bricht sonst ab, P6-X) — läuft `--apply` heute (2026-08-23, Eintrag jetzt
   schreibbar) oder an einem späteren Tag (Eintrag dann)?
2. **A7 Schritt 1** — wann kann `authctl.py invite --space testnutzer-p7 --purpose enroll`
   laufen? Danach übernimmt Claude Code das Enrollment im Browser (`claude-in-chrome`) und den
   Rest von A7/A7b ohne weiteren Nikinger-Handgriff.

**Beide Fragen beantwortet (Nikinger, per AskUserQuestion, selber Tag): heute, auf beide.**
`docs/UPDATE_LOG.md` bekam den A5-Eintrag (2026-08-23, bewusst zurückhaltend formuliert — die
Migration macht laut Skript-Docstring nur explizit, was implizit längst galt, „sichtbar ändert
sich für dich nichts"), gegen `test_updates.py`/`test_deploy_scripts.py` grün geprüft (28/28).
**`authctl.py invite`/`spacectl.py create-space testnutzer-p7` bleiben laut Plan-Text
ausdrücklich „Nikinger, einmalig" — Claude Code führt sie nicht selbst aus**, auch nach der
Freigabe nicht (Live-Schreibzugriff auf `auth.sqlite3`, dieselbe Vorsicht wie bei jedem
`--apply`). **Warte auf: (a) den Nikinger führt `--apply` aus, (b) den Nikinger führt `authctl.py
invite` aus und gibt den Link weiter** — beides außerhalb dessen, was Claude Code aus dieser
Session heraus selbst anstößt.
