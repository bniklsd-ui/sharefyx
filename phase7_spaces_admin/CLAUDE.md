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
updated: 2026-08-23 (A8: Phase 6.5 formal abgeschlossen als 🟡, 12/14, P6.5-8/13 via testnutzer-p7-Substitution, PHASE6_5_CLOSEOUT_HANDOVER.md + Uebersichtsgrafik neu, P1-Contract-Absatz aktualisiert) | 2026-08-23 (Step 0 gestartet, Doku-Audit gefahren, Skelett angelegt)
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

| 5 | A7b: `phase7_spaces_admin/scripts/testcred.py` (neu — `store`/`password`/`totp`/`purge`, hart auf `testnutzer-p7`/`nikinger-space`/`p7-testcred` verdrahtet, kein `--space`/`--key`/`--service`, `authserver/totp.py` nur importiert). **Nebenfund beim Bauen:** `pytest.ini`s `testpaths` hatte `phase7_spaces_admin/tests` nie aufgenommen (Step-0.6-Lücke) — der volle Lauf zeigte trotz neuer Tests weiterhin 836, erst `--collect-only` deckte es auf. Nachgetragen | A | ✅ **vollständig** | +7 `phase7_spaces_admin/tests/test_testcred.py`; 843 gesamt |

| 6 | A7 Anlegen (P7-J, schließt P6-W): `authctl.py invite testnutzer-p7 --purpose initial` (Nikinger, drei Plan-Text-Drifts korrigiert unterwegs — `--purpose enroll` existiert nicht, nur `initial`/`reset`; `SPACE` ist positional, kein `--space`; `SPACE_AUTH_DB`/`SPACE_PUBLIC_BASE_URL` fehlen ohne systemd-`STATE_DIRECTORY`, manuell gesetzt aus der laufenden Unit). Enrollment per `claude-in-chrome`: Passwort gesetzt, TOTP-Seed **einmalig** gesehen, sofort per stdin an `testcred.py store` gereicht (nie in Prosa/Datei), TOTP-Bestätigung mit `testcred.py totp` berechnet und akzeptiert. Recovery-Codes gezeigt, **bewusst nicht erfasst** (außerhalb von `testcred.py`s Schema, ein noch stärkeres Geheimnis als der laufende TOTP-Code, für keinen geplanten Ablauf gebraucht). `spacectl.py create-space testnutzer-p7` (Nikinger) — Space-Verzeichnis existiert | A | ✅ **Konto+Space live, Connector/Schreibprobe noch offen** | 0 (Live-Aktion, kein Code) |

| 7 | A7-Rest: `phase7_spaces_admin/scripts/p7_10_write_probe.py` (neu, echter Netz-OAuth-Fluss gegen den laufenden Server, `testcred.py`-gestützt, schreibt ein Item), `p7_11_visibility_probe.py` (neu, globale `search_items`-Probe), `p7_11_setup_fixture.py` (neu, Einmal-Setup über `storage.store.Store.update()` — Begründung siehe Modul-Docstring/Session-Block) | A | ✅ **P7-10/P7-11/P7-12b live bestanden** | 0 (Live-Probe-Skripte, gleiche Kategorie wie `oauth_smoke.py`/`migrate_visibility.py` — kein Unit-Test für einen echten Netzlauf) |

| 8 | A8 (Phase 6.5 formal abschließen, P7-I): P6.5-8/13 per gebilligter `testnutzer-p7`-Substitution geschlossen — `p7_13_asset_fixture.py`/`p7_13_share_write_fixture.py` (neu, Store-direkte Fixtures) + `p7_13_asset_share_gate_probe.py`/`p7_13_ui_asset_probe.py` (neu, MCP- bzw. `/ui/login`-Cookie-Probe). `docs/concepts/PHASE6_5_CLOSEOUT_HANDOVER.md` (neu) + `phase6_5_tools_images_uebersicht.svg` (neu, zweimal gerendert/gegengeprüft). P1-Contract-Absatz (Öffnungen 3/4/5 datiert geschlossen, 6 als offen benannt) in `phase1_storage/CLAUDE.md`. `ROADMAP.md`/Root-`CLAUDE.md`/`docs/INDEX.md` auf den neuen 6.5-Status | A | ✅ **vollständig** — Abnahmestand 6.5: 12/14, P6.5-12/14 bleiben offen (siehe unten) | 0 (nur neue Live-Probe-Skripte, kein Unit-Test-Delta; `pytest` unverändert 843) |

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
| P7-10 | `testnutzer-p7` existiert, schreibt einmal | Nikinger + Claude Code | ✅ `p7_10_write_probe.py`, `itm_ee1e0323` |
| P7-11 | `testnutzer-p7` sieht nur sein item-level Item | Claude Code | ✅ Web-UI (P6-Zeilen 36/37, echter Login) **und** MCP (`p7_11_visibility_probe.py`) |
| P7-12 | `testnutzer-p7` entfernt, Keyring-Eintrag weg | Claude Code | ⬜ |
| P7-12b | Claude Code loggt sich ohne Nikinger als `testnutzer-p7` ein | Claude Code | ✅ derselbe Lauf wie P7-10 — Login/TOTP/Consent allein über `testcred.py` |
| P7-13 | Phase 6.5 formal abgeschlossen | Claude Code | ✅ 🟡 (12/14, `PHASE6_5_CLOSEOUT_HANDOVER.md`) |
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

**Nachtrag, selber Tag — nach A5 `--apply`/A7 Anlegen/A7b: P7-10/P7-11/P7-12b geschlossen, zwei
echte Funde unterwegs.**

**Fund 1 — claude.ai dedupliziert Custom Connectors organisationsweit nach Server-URL.** Ein
zweiter, eigener Connector `sharefyx-testnutzer-p7` (dieselbe MCP-URL wie der bestehende
`sharefyx`-Connector) ließ sich in claude.ai nicht anlegen: „In deiner Organisation existiert
bereits ein Connector mit dieser URL." Der OAuth-Login selbst funktionierte (Passwort+TOTP
akzeptiert, Redirect korrekt) — der Server ist gesund, die Blockade sitzt eine Ebene höher, in
claude.ai selbst. **Konsequenz:** P7-10/P7-12b laufen seither über
`phase7_spaces_admin/scripts/p7_10_write_probe.py` — einen echten Netz-OAuth-Client (DCR+PKCE,
`testcred.py`-gestützt), der denselben Authorization Server direkt anspricht, ohne einen
claude.ai-Connector zu brauchen. Ergebnis: `own_space_visible: true`, `itm_ee1e0323` geschrieben.
**Nebeneffekt, kein separater Nachweis nötig:** derselbe Lauf beweist P7-12b (Login allein über
`testcred.py`, kein Nikinger-Handgriff).

**Nebenfund, real reproduziert (nicht Teil des Plans):** das `computer`-Type-Tool des
Browser-Automations-Kanals ließ bei einem langen, schnell getippten String zuverlässig das
letzte Zeichen fallen (`…/mcp` → `…/mc`) — zweimal reproduziert, per Zoom-Screenshot UND
Accessibility-Tree bestätigt, nicht nur per Screenshot vermutet. Fund kam vom Nikinger selbst
(„du hast da einen Tippfehler"), nicht von Claude Code entdeckt. Kein sharefyx-Bug — Werkzeug-
Eigenheit, hier nur vermerkt, falls sie bei künftiger Browser-Automation wieder auftritt: ans
Feldende springen und das fehlende Zeichen einzeln nachtippen, dann per Zoom verifizieren.

**Fund 2 — die `Freigeben`-Dialogbox kann kein item-level Share an einen brandneuen Principal
setzen.** `dialogs.js :: openShareDialog()` listet ausdrücklich nur `state.spaces` (Spaces, die
der Actor schon über ein bestehendes `.share.yml` kennt) — dokumentierter, bewusster Scope-
Schnitt aus Step 7 Commit 5b (`phase6_shares/CLAUDE.md`, Modul-Zeile 15). `testnutzer-p7` hat
laut P7-11s eigenem Zweck **keinerlei** vorherige Beziehung zu `niklas` — genau der Fall, den
die Dialogbox nicht abdeckt. Kein Bug: `webui/api.py :: _items_patch` UND
`mcpserver/tools.py :: update_item()` erlauben `share_read`/`share_write` beide bereits
serverseitig für Menschen (P6-M sperrt nur MCP-Tools), die Lücke ist rein die Dialogbox-Fläche.
**Ein Versuch, das über einen rohen `fetch()`-`PATCH` aus der Browser-Konsole zu umgehen,
scheiterte korrekt** (`403 csrf_failed`) — der Double-Submit-CSRF-Token wird ausschließlich
einmalig auf der echten Login-Erfolgsseite ausgeliefert (P5-H), eine frisch navigierte
Tab-Session hat ihn nicht, und ihn zu bekommen hätte Niklas' echtes Passwort/TOTP gebraucht.
**Bestätigt: die Sicherheitsgrenze hält, kein Leck.** Stattdessen:
`phase7_spaces_admin/scripts/p7_11_setup_fixture.py` (neu) — ruft `storage.store.Store.update()`
direkt auf (Details/Einschränkung siehe Korrektur unten). Ergebnis: `itm_3d0ac2b3` trägt jetzt
`share_read: ["testnutzer-p7"]`, echter Git-Commit, `version` 1→2.

**P7-11-Ergebnis, zweifach belegt (Advisor-Hinweis: die MCP-Probe allein testet die falsche
Fläche — P6-Zeilen 36/37 sind ausdrücklich Web-UI-Kriterien, nicht der bereits vorher
funktionierende Agenten-Pfad):**
1. **MCP:** `p7_11_visibility_probe.py itm_3d0ac2b3` → `expected_item_visible: true`,
   `foreign_ids: ["itm_3d0ac2b3"]`, `foreign_ids_are_exactly_expected: true`.
2. **Web-UI, echter Login als `testnutzer-p7`** (`/ui/login`, dieselben drei Felder wie
   `/oauth/authorize`, `testcred.py`-gestützt): **P6-Zeile 36** — „Alle Items" zeigt genau zwei
   Einträge, `P7-10 Schreibprobe` (eigen) und `P7-11 Sichtbarkeitsprobe` (fremd, Chip „geteilt
   mit testnutzer-p7"), Klick öffnet es. **P6-Zeile 37** — Detailansicht zeigt „Nur lesen —
   fremder Space (niklas)", kein Editor (nur `share_read`, kein `share_write`). **Damit
   erstmals ein Empfänger ohne jede Space-Mitgliedschaft real durchgespielt** — mit `niklas`
   strukturell nie möglich (steht in `fabian/.share.yml` unter `read:`), das war der eigentliche
   Grund für den dritten Principal (P7-J).

**Nebenwirkung, bewusst in Kauf genommen:** der `/ui/login`-Lauf als `testnutzer-p7` hat Niklas'
eigene aktive UI-Sitzung im selben Browser beendet (ein Session-Cookie pro Domain) — Niklas
muss sich in der Web-UI neu anmelden, sein Passwort/TOTP war davon nie betroffen.

**Korrektur nach Advisor-Review, vor dem Commit:** der ursprüngliche Versuch, das CSRF-geschützte
`PATCH /api/v1/items/{id}` per rohem `fetch()` aus der Browserkonsole in einer frisch navigierten
(nicht über den echten Login-Fluss bootstrapten) Tab-Sitzung zu setzen, schlug korrekt mit `403
csrf_failed` fehl — das ist die Sicherheitsgrenze aus P5-H, die hält, kein Leck. Der
Double-Submit-CSRF-Token wird ausschließlich einmalig auf der echten Login-Erfolgsseite
ausgeliefert; ihn zu bekommen hätte Niklas' echtes Passwort/TOTP gebraucht. Deshalb stattdessen
`p7_11_setup_fixture.py` über `Store.update()` direkt — **ohne** das Re-Auth-Gate aus P6-N
(`require_share_reauth()`), das `_items_patch` einer Freigabe-Erweiterung davorschaltet
(Docstring korrigiert, Advisor-Fund).

**Teardown-Hinweis für P7-12, jetzt vermerkt statt erst beim Abbau entdeckt (Advisor-Fund):**
`spacectl.py check` prüft ausschließlich `.share.yml` (space-level), nie item-level
`share_read`/`share_write` in Frontmatter. Nach `spacectl.py remove-space testnutzer-p7` bliebe
`share_read: [testnutzer-p7]` auf `itm_3d0ac2b3` sonst eine verwaiste Freigabe, die kein
Werkzeug meldet — P7-12s Kriterium „keine verwaisten Freigaben" wäre dann ein falsches ✅. Vor
dem Abbau: diese Freigabe zurücknehmen oder das Fixture-Item archivieren.

**`pytest -q` 843 passed** (unverändert — die drei neuen Skripte sind Live-Probe-Skripte ohne
eigene Unit-Tests, gleiche Kategorie wie `oauth_smoke.py`/`migrate_visibility.py`). Tabu-Diff
(`mcpserver/asgi.py`, `authserver/{crypto,totp,passwords,resolver,flows}.py`) weiterhin leer.

**Vormerkung für den Fabian-Freigeben-Schnitt/§0.4:** die `Freigeben`-Dialogbox „nur bereits
bekannte Spaces" ist derselbe Scope-Schnitt, der P7-14/P7-16 (geteilte Spaces im Browser
anlegen/freigeben) betreffen könnte — dort wird der Zielraum aber immer VORHER angelegt/bekannt
sein (Block C), betrifft also vermutlich nicht dasselbe Muster. Nicht weiter verfolgt, außerhalb
dieses Fundes.

**Nächster Schritt:** P7-12 (Abbau — `testcred.py purge`, `spacectl.py remove-space
testnutzer-p7 --force`, `authctl.py disable-user`/`revoke-sessions`) erst am Ende von Block A,
nicht jetzt — `testnutzer-p7` wird für A8/weitere Abnahmezeilen noch gebraucht.

**Nachtrag, selber Tag — A8 (Phase 6.5 formal abschließen, P7-I) durchgeführt.**

**Advisor-Runde vor dem Bauen:** A8.1s Plan-Text („A3 schließt P6.5-12; A7 schließt P6.5-8 und
P6.5-13") war zum Zeitpunkt seines Entwurfs eine Absicht, keine gemessene Tatsache — vor dem
Schreiben des Handovers geprüft statt übernommen. **Diskriminierender Befund:** weder
`itm_3d0ac2b3` noch `itm_ee1e0323` trugen ein `_assets/`-Verzeichnis im echten `DATA_ROOT` — A3
baute den Knopf, testete ihn aber nicht am Bild; A7s Proben (`p7_10`/`p7_11`) berührten nie ein
Asset. A8.1s Satz war damit Plan-Drift, kein erledigter Punkt.

**P6.5-12/P7-5 — Browser-Nachweis dieser Sitzung bewusst nicht gefahren.** Ein Login als
`testnutzer-p7` im echten Chrome-Tab hätte Passwort/TOTP aus `testcred.py` in eine
`computer`-Type-Aktion getippt — anders als bei `p7_10`/`p7_11` (dort las das Skript die
Credentials intern, nie sichtbar für Claude Code) wäre das Geheimnis hier im sichtbaren
Werkzeugverlauf dieser Sitzung gelandet. Ein direkter `python -c`-Ausdruck, der `testcred.py
password`/`totp` roh ausgibt, wurde vom Auto-Mode-Classifier korrekt blockiert — als Bestätigung
behandelt, nicht umgangen. P6.5-12/P7-5 bleiben deshalb 🟡/⬜ (gebaut, ungeprüft), keine Regression.

**P6.5-13 — MCP-Fläche, per echtem OAuth-Client geschlossen.** `p7_13_asset_fixture.py itm_id`
(neu, Store-direkt) legte ein PIL-erzeugtes PNG auf `itm_3d0ac2b3` ab (`ast_e7f27214`, 77 Bytes)
— derselbe Store-Kürzungsweg wie `p7_11_setup_fixture.py`, kein neuer Serverpfad.
`p7_13_asset_share_gate_probe.py` (neu, gleiche OAuth-Bauart wie `p7_10_write_probe.py`) rief
`get_item_asset` als `testnutzer-p7` auf: mit reinem `share_read` (aus P7-11) →
`bytes_available:false`, nur Metadaten. `p7_13_share_write_fixture.py itm_id --version 2` (neu)
erweiterte auf `share_write` — derselbe Aufruf lieferte danach echte `image/png`-Bytes. **Exakt
das kommentierte P6.5-M-Verhalten (`tools.py :: get_item_asset()`), empirisch bestätigt, kein
neuer Sicherheitsbefund.**

**P6.5-8 — Web-UI-Fläche, per Cookie-Session-Skript statt Browser-Klick geschlossen.**
`p7_13_ui_asset_probe.py` (neu) postet gegen `/ui/login` (Cookie-Session, P5-D) und holt danach
`GET /api/v1/items/{id}/assets/{id}` — dieselbe Bauart wie die MCP-Probe, nur gegen die
Cookie-Fläche: authentifiziert + `share_write` → `200`/`image/png`/77 Bytes; ganz ohne Session
→ `401`. **Plan-Text-Drift, kein Bug:** `phase6_5_tools_images_plan.md` Zeile P6.5-8 nennt
„403" — der reale Endpunkt liefert bei fehlender Authentifizierung `401` (P5-typisch: kein
Unterschied zwischen „nicht angemeldet" und „falsche Anmeldedaten"), beides fail-closed.

**Abnahmestand 6.5 neu gezählt (A8.2): 12 von 14**, nicht 14/14 — Glyph bleibt 🟡, aus der
Zahl abgeleitet, kein Grenzfall (P6.5-12 UND P6.5-14 offen, nicht nur P6.5-14 wie im
13/14-Beispiel des Plans). Details, Kriterienliste, `[VERIFY]`-Bilanz:
`docs/concepts/PHASE6_5_CLOSEOUT_HANDOVER.md` (neu). `phase6_5_tools_images/CLAUDE.md`s Matrix
+ `updated:`-Zeile korrigiert (kein neuer Session-Block dort — Rotationsregel, die Erzählung
lebt hier). `phase1_storage/CLAUDE.md`: Öffnungen 3/4/5 datiert geschlossen, Öffnung 6 (P7,
`acl.py`-Schreibseite) im selben Absatz als weiterhin offen benannt (A8.5, vermeidet die
Falschaussage, die P6-Handover §5.6 bereits umging). `docs/concepts/
phase6_5_tools_images_uebersicht.svg` (neu, 1080×1080) — zweimal gerendert und per `Read`
visuell geprüft, kein Textüberlauf. `ROADMAP.md`/Root-`CLAUDE.md`/`docs/INDEX.md` im selben
Umfang auf den neuen 6.5-Status gezogen — Root-`CLAUDE.md`s „Current state" hatte Phase 7 bisher
gar nicht erwähnt (eigener kleiner Fund, kein A8-Punkt, aber dieselbe Kategorie Doku-Drift wie
Step 0s Audit).

**Teardown-Ledger erweitert (P7-12, jetzt vier statt zwei Punkte):**
1. `itm_3d0ac2b3` trägt `share_read: [testnutzer-p7]` (aus P7-11) — bereits vermerkt.
2. `itm_3d0ac2b3` trägt jetzt zusätzlich **`share_write: [testnutzer-p7]`** (aus P7-13) —
   `spacectl.py check` sieht das ebenso wenig wie `share_read`, gleiche Lücke, jetzt zwei Felder.
3. `itm_3d0ac2b3` trägt ein echtes **Asset** (`ast_e7f27214`, `niklas/_assets/itm_3d0ac2b3/`) —
   gehört `niklas`, nicht `testnutzer-p7`; `spacectl.py remove-space testnutzer-p7` räumt es
   nicht auf (fremdes Item), aber es bleibt als Testartefakt in niklas' Space stehen, wenn es
   niemand vorher entfernt.
4. **Empfehlung vor P7-12:** `share_read`/`share_write` auf `itm_3d0ac2b3` zurücknehmen (oder
   das Item archivieren) UND das Test-Asset per `store.delete_asset()` entfernen — alle drei in
   einem Zug, nicht einzeln vergessen.

**`pytest -q` weiterhin 843 passed** (vier neue Skripte, alle Live-Probe-Kategorie ohne eigenen
Unit-Test). Tabu-Diff unverändert leer.

**Nächster Schritt:** A6 (Purge-Gate, `clients`/`token_families`-Rückgang, frühestens
2026-08-28) ist der letzte offene Block-A-Punkt außer P7-12 selbst. Bis dahin: Session hier
gestoppt — A6 ist kalendarisch blockiert, kein Claude-Code-Handgriff verkürzt das.
