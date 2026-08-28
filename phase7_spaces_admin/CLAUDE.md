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
updated: 2026-08-28 (A6/P7-9 gefahren -- token_families 35->31, clients unveraendert 54 wie erwartet, Phase 7 vollstaendig abgenommen, nur noch Step-Z-Closeout-Dokumente offen) | 2026-08-28 (Abnahmezeilen 31-34 vom Nikinger live gegen die echte Instanz bestaetigt -- 32/33/34 ohne Vorbehalt, 31 mit demselben bereits bekannten P7-24-TOTP-Vorbehalt, kein neuer Fund) | 2026-08-25 (Step C3 gebaut -- Space-Verwaltung UI, spaces.js neu, echter Browser-Lauf gegen eine Wegwerf-Instanz Ende-zu-Ende bestanden, zwei Advisor-Funde vor dem Commit behoben, 904 Tests gruen) | 2026-08-25 (Step C4 Nachtrag -- Nikinger-Entscheidung: siebte Contract-Oeffnung statt archived_blockers-Riegel, storage/store.py :: move() erlaubt Space-Wechsel fuer archivierte Items, create(status=archived) faengt jetzt denselben Fall ab, 903 Tests gruen) | 2026-08-25 (Step C4 gebaut -- zweiphasiger Space-Entfernen-Algorithmus, Advisor-Fund: bereits archivierte Items brauchen einen eigenen Vorlauf-Riegel, P7-20/P7-21/Testanteil-P7-22 geschlossen) | 2026-08-25 (Gate A->C geprueft, alle vier Punkte live -- Block C gestartet, Step C1: Schreibseite von .share.yml in storage/acl.py, sechste Contract-Oeffnung gebaut) | 2026-08-25 (P7-4 erster echter Befund: FAIL, ID statt Titel genannt; P7-12-Abbau geprueft und bewusst NICHT gefahren -- Block C/P7-14 braucht testnutzer-p7 noch) | 2026-08-25 (P7-1/P7-2/P7-7 per echtem Browser-Klick bestanden, git-Reparatur nach Nikinger-Freigabe, nur noch P7-4/P7-9/P7-12 offen) | 2026-08-25 (P6.5-12/P7-5 per echtem Browser-Klick bestanden, testnutzer-p7-Substitution, 13/14 in Phase 6.5) | 2026-08-25 (echter deploy.sh-Lauf durch den Nikinger, Live-Release jetzt 53bad20 statt f96125e, A3s asset-strip live, P6.5-12 wieder testbar) | 2026-08-23 (A8: Phase 6.5 formal abgeschlossen als 🟡, 12/14, P6.5-8/13 via testnutzer-p7-Substitution, PHASE6_5_CLOSEOUT_HANDOVER.md + Uebersichtsgrafik neu, P1-Contract-Absatz aktualisiert) | 2026-08-23 (Step 0 gestartet, Doku-Audit gefahren, Skelett angelegt)
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

| 9 | C1 (Schreibseite von `.share.yml`, sechste Contract-Öffnung, P7-P): `storage/acl.py` bekommt `read_share_file`/`write_share_file`/`add_member`/`remove_member`/`create_space`/`remove_space_dir`/`spaces_referencing`/`AclWriteError` (Dump-Logik intern einmal in `_write_share_file_unlocked()`, Advisor-Fund nach dem ersten Commit). `spacectl.py`s vier schreibende Unterbefehle rufen jetzt `acl.*` auf; entfallen dort: `_DataRootLock`/`_dump_share_file`/`_spaces_referencing`. `_load_share_file`/`_find_share_files` bleiben — nur noch für `check`, rein lesend. Jede `acl`-Schreibfunktion nimmt den `.write.lock`-Flock selbst (P7-M) | C | ✅ **vollständig** | +24 `phase7_spaces_admin/tests/test_acl_write.py`; 867 gesamt |
| 10 | C2 (REST-Fläche für Space-Verwaltung): vier der fünf in Plan §4.C2 genannten Routen — `POST /api/v1/spaces`, `GET/POST .../{space}/members`, `DELETE .../{space}/members/{name}` (`DELETE /api/v1/spaces/{space}` bleibt C4, sein Vorlauf/Durchlauf-Algorithmus gehört dorthin, ein Stub-Handler wäre eine zweite unvollständige Fassung derselben Regel). `webui/shares.py :: require_space_reauth()` (neu, Re-Auth bei Mitglied-Hinzufügen, keins bei -Entfernen, P7-N) — ruft `verify_reauth()` direkt auf, keine neue Extraktion nötig: die im Plan beschriebene `_verify_reauth_credentials()`-Extraktion existiert bereits als `webui/reauth.py :: verify_reauth()` (gebaut vor dieser Phase, von `account.py` UND `shares.py` geteilt) — Plan-Text war insofern stale, keine neue Arbeit. `storage/store.py :: Store.data_root` (neue Read-Property, kein neues Verhalten, keine siebte Öffnung). `_meta` bekommt `space_admin` | C | ✅ **vollständig, zwei Advisor-Runden vor dem Commit** | +23 (21 `phase7_spaces_admin/tests/test_space_admin_api.py` neu + 1 `phase5_ui/tests/test_meta.py` + 1 `phase1_storage/tests/test_store.py`); 890 gesamt |
| 11 | C4 (Space entfernen, zweiphasig, P7-O/N8/N9): fünfte Route `DELETE /api/v1/spaces/{space}` in `webui/api.py :: _spaces_delete`. Vorlauf (kein Schreibvorgang) über `store.search()`-Paging mit `_STORE_FETCH_LIMIT`, Blocker-Scan via `permissions.can_write_item_as_human(home, store.acl_of(...))`; `require_space_reauth(widening=True)` + `confirm == space`; Durchlauf `store.move()` → `store.archive()` je Item; harte `len(moved) == total`-Sperre vor `acl.remove_space_dir()`. **Advisor-Fund (empirisch, vor dem ersten Commit):** `store.search()` zählt bereits archivierte Items mit (`total` schließt sie ein), `store.move()` verbot sie zu diesem Zeitpunkt aber noch explizit — ohne einen Riegel hätte das einen unbehandelten `ValidationError`/500 mitten im Durchlauf ausgelöst, ohne den von N9 verlangten Bericht. **Erster Fix in diesem Commit: ein Vorlauf-Riegel `archived_blockers`, fail-closed** — eine Space mit archivierten Items wäre damit vorerst unentfernbar gewesen. **Überholt durch Zeile 12 in derselben Sitzung** (Nikinger-Entscheidung, siehe unten) — der Riegel existiert im finalen Code nicht mehr. Zweiter, weiterhin gültiger Advisor-Fund: `acl.spaces_referencing()` fehlte das `exclude=`, das `spacectl.py remove-space` für dieselbe Prüfung setzt (Parität-Drift, behoben). `phase7_spaces_admin/tests/test_space_admin_api.py`s Kill-Switch-Parametrize um die fünfte Route ergänzt (schließt den Testanteil von P7-22) | C | ✅ **vollständig** | siehe Zeile 12 für die finale Testzahl |
| 12 | Nikinger-Entscheidung auf Nachfrage (dieselbe Sitzung): siebte, benannte Contract-Öffnung statt des `archived_blockers`-Riegels aus Zeile 11 — `storage/store.py :: move()` erlaubt jetzt einen reinen Space-Wechsel für archivierte Items (echter Ordner-Wechsel bleibt verboten), `_write_item_file()` legt sie dabei ins Ziel-`_archive/`. Zweiter Advisor-Fund vor diesem Commit: `create(status="archived")` (über MCP/REST erreichbar) lief am ursprünglichen Riegel vorbei und hätte sonst eine Divergenz erzeugt — `create()` setzt jetzt selbst `folder=""` bei `status="archived"`. `_spaces_delete` ruft `archive()` nur noch für Items auf, die `move()` nicht schon als archiviert zurückgibt (kein doppelter Commit). Volle Herleitung, inkl. der Anker-Prüfung gegen `phase1_storage/storage/store.py`, in `phase1_storage/CLAUDE.md`s „Geerbte Contracts" (siebte Öffnung) | C | ✅ **vollständig** | +4 `phase1_storage/tests/test_store.py` (3 ersetzen `test_move_of_archived_item_is_rejected`, 1 neu) + 1 `phase7_spaces_admin/tests/test_space_removal.py` (ersetzt den 403-Test aus Zeile 11 durch einen 200-Test); 903 gesamt |
| 13 | C3 (Oberfläche): Menüpunkt scharf geschaltet (`app.html` verliert `disabled`/„kommt in Phase 7"), `webui/config.py :: UiSettings.space_admin_enabled` Default `False`→`True` (P7-R, schließt den in `phase6_shares/CLAUDE.md` Zeile 16 gebauten Seam). Neues Modul `webui/static/js/spaces.js` (P7-Q): `openSpaceAdminDialog()`/Liste aller `writable`-Spaces, `selectSpace()` lädt `GET .../members`, Mitglieder-Hinzufügen (immer Re-Auth, eingefroren wie `dialogs.js`s `pendingMoveBody`)/-Entfernen (kein Re-Auth), `openRemoveSpaceDialog()` (Klartext-Konsequenz + getippte Bestätigung + Re-Auth). `app.html`: `#space-admin-dialog`/`#space-remove-dialog`, Geschwister von `#share-dialog`. `app.js`: `initSpaces()` in den Bootstrap, beide neuen Dialoge in `anyOverlayOpen()`/Escape, `account-manage-spaces`-Klick öffnet den Dialog, **`meta.space_admin` blendet den Menüpunkt aus** (P7-R — statisches HTML kennt den Kill-Switch sonst nicht, P5-T). **Zwei Advisor-Funde vor dem Commit:** (1) `selectSpace()` setzte `pendingMemberBody`/die Re-Auth-Felder beim Space-Wechsel nicht zurück — ein eingefrorener Hinzufügen-Versuch für Space A wäre nach einem Klick auf Space B gegen B abgeschickt worden, derselbe Fund, den `dialogs.js :: pendingMoveBody = null` beim Space-Wechsel bereits kommentiert; behoben, plus dieselbe Rücksetzung in `openSpaceAdminDialog()`. (2) `orphans` aus `GET .../members` wurde gelesen und verworfen, obwohl C2 es explizit als „Render-Hinweis fürs Frontend" gebaut hatte — jetzt in der Mitgliederliste als eigene Zeile gerendert. **Echter Browser-Lauf gegen eine Wegwerf-Instanz** (siehe Session-Block: Anlegen, Hinzufügen mit Re-Auth, Entfernen ohne Re-Auth, Entfernen-Dialog mit Konsequenztext+Bestätigung+Re-Auth, Home-Space-Ausnahme — alles Ende-zu-Ende bestanden) | C | ✅ **vollständig, zwei Advisor-Funde vor dem Commit behoben** | +2 (`test_app_html_has_a_live_manage_spaces_entry` ersetzt den Stub-Test, `_JS_MODULES` um `"spaces"` ergänzt) + 1 `test_api.py` (`UiSettings().space_admin_enabled is True`); JS bleibt laut P5-T unit-ungetestet, echter Browser-Lauf statt jsdom; 904 gesamt |
| 14 | C5 (Betrieb/Doku, kein Code): `phase3_edge/scripts/diagnose.sh` Prüfung 12 bekommt einen Satz im Prüfungstext (deckt jetzt ausdrücklich auch die menschliche Space-Verwaltungsfläche ab, nicht nur `spacectl.py`). `docs/UPDATE_LOG.md`-Eintrag (P6-X-Gate: oberster Eintrag muss den Deploy-Tag tragen) — **[2026-08-27] auf `## 2026-08-27` korrigiert** (ein zwischenzeitlicher `## 2026-08-28`-Stand ließ einen echten `deploy.sh`-Lauf am Gate scheitern, siehe Session-Block), Block-B-Zeile ergänzt | C | ✅ **vollständig** | 0 (Doku-/Skript-Text, kein Python-Verhalten geändert); 904 gesamt unverändert |
| 15 | Block B (Mehrfachauswahl, `phase6_shares/ITEM_MOVE_PLAN.md` §9, P6-AK–AN): `state.js` (`selectedItemIds`-Set), `list.js` (Strg+Klick/Long-Press-Toggle, Auswahl-Werkzeugleiste, `moveSelectedItems()`-Zweirunden-Schleife), `dialogs.js` (`openMoveDialog()` nimmt jetzt Item ODER Array, Batch-Zweig in `runBatchMove()` mit eingefrorenem `pendingBatchTarget`), `tree.js` (Auswahl leert sich bei Navigation), `toasts.js`/`app.css` (mehrzeilige Sammelmeldung), `app.html` (`#list-selection`, `#move-dialog-title`, `#move-progress`) | B | ✅ **vollständig, Advisor-Runde vor UND nach dem Browser-Lauf** | 0 (reiner Frontend-Schnitt, P6-AL — kein neuer Endpunkt, `webui/api.py` unangetastet, Tabu-Diff bestätigt nur `webui/static/`); 904 gesamt unverändert, JS bleibt laut P5-T unit-ungetestet |

*(Weitere Zeilen entstehen mit dem Rest von Block C/B — siehe Plan §4 für die vollständige Schritt-Sequenz.)*

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
| P7-1 | Item-ID sichtbar + Klick kopiert | Niklas | ✅ (via `testnutzer-p7`) — **[2026-08-25]** `itm_ee1e0323` sichtbar im Kopfdaten-Header, „ID kopieren" geklickt, „ID kopiert."-Toast bestätigt (`editor.js:202-204`: Toast läuft nur im `.then()` von `navigator.clipboard.writeText(itemId)` — kein Fake-Erfolg möglich) |
| P7-2 | ID-Suche findet Item spaceübergreifend | Niklas | ✅ (via `testnutzer-p7`) — **[2026-08-25]** `p7_11_setup_fixture.py` erneut gefahren (`share_read:[testnutzer-p7]` auf `itm_3d0ac2b3`, niklas-Space), Suche nach `itm_3d0ac2b3` in „Alle Items" fand das fremde Item, Chip „geteilt mit testnutzer-p7" |
| P7-3 | ID-Suche auf nicht lesbares Item → leere Liste | Claude Code, Test | ✅ `test_id_lookup_respects_read_permission` |
| P7-4 | Claude nennt Items beim Titel, nicht der ID | Niklas, echter Connector | ❌ **[2026-08-25]** erste echte Probe, organisch (kein gestellter Testfall) — Nikinger fragte im Webchat „welche 3 Items sind die aktuellsten", Claude antwortete mit einer Tabelle, deren Item-Spalte jede Zeile mit der rohen `itm_…`-ID einleitete (`itm_3d0ac2b3 — P7-11 Sichtbarkeitsprobe...`), Titel nur angehängt. Widerspricht dem Wortlaut aller vier Tool-Beschreibungen (`create_item`/`patch_item`/`search_items`/`get_item_meta`, `mcpserver/tools.py`) direkt. Kein Code-Fehler — die Prosa-Anweisung reicht offenbar nicht, sobald eine tabellarische Antwort naheliegt (`search_items` liefert `id` als Feldname, das Modell übernimmt es vermutlich als Zeilen-Anker). Bleibt ⬜/❌ bis weitere Datenpunkte vorliegen |
| P7-5 | Bild im Editor entfernbar, landet in `_trash/` | Niklas | ✅ (via `testnutzer-p7`) — **[2026-08-25]** echter Browser-Klick, `itm_26f8d0b7`/`ast_e60e8d8a`, siehe Session-Block |
| P7-6 | `PATCH` mit Tippfehler-Feld abgewiesen (O6) | Claude Code, Test | ✅ `test_items_patch_rejects_an_unknown_field` |
| P7-7 | Speichern/Verschieben/Freigeben nach Whitelist unverändert | Niklas | ✅ (via `testnutzer-p7`) — **[2026-08-25]** `itm_68f0251d`: Save (Body-Edit, v1→v2), Move (`p7-7-test`-Ordner angelegt + verschoben, Datei real dort, v2→v3), Share (leerer Dialog — `testnutzer-p7` kennt laut P6-V keine fremden Spaces, `Speichern` als No-op-PATCH echt abgeschickt, v3→v4). Frontmatter nach allen vier Commits (`create`/`update`×3) weiterhin exakt die erlaubten Felder, keine Fremdfelder |
| P7-8 | Migration: 0 `.md` ohne `visibility:` | Nikinger + Claude Code | ✅ `--apply` 2026-08-23, `items_migrated:73` (deckungsgleich Dry-Run), `grep -L '^visibility:'`→0, 3 Commits (niklas/fabian/IT-Sekus-Projekt) |
| P7-9 | `clients`/`token_families` sinken nach realem Purge | Niklas | ✅ **[2026-08-28]** `sudo systemctl start sharefyx-purge.service` durch den Nikinger, `journalctl`: `token_families: 4` entfernt (35→31, read-only via `sqlite3` bestätigt), `clients` unverändert `54` (90-Tage-Fenster öffnet erst 2026-10-27 — kein Fund, erwartetes Verhalten) |
| P7-10 | `testnutzer-p7` existiert, schreibt einmal | Nikinger + Claude Code | ✅ `p7_10_write_probe.py`, `itm_ee1e0323` |
| P7-11 | `testnutzer-p7` sieht nur sein item-level Item | Claude Code | ✅ Web-UI (P6-Zeilen 36/37, echter Login) **und** MCP (`p7_11_visibility_probe.py`) |
| P7-12 | `testnutzer-p7` entfernt, Keyring-Eintrag weg | Claude Code | ✅ **[2026-08-27]** genau nach Plan-Rezept (§ Zeile 544-552): `testcred.py purge` (Claude Code, Keyring lokal) → `spacectl.py remove-space testnutzer-p7 --force` + `authctl.py disable-user`/`revoke-sessions --space testnutzer-p7` (Nikinger, `SPACE_DATA_ROOT`/`SPACE_AUTH_DB` gegen die echte Instanz gesetzt) → `spacectl.py check --json` → `{"orphan_count":0,"orphans":[],"broken_count":0,"broken":[]}`, keine verwaisten `.share.yml`-Referenzen |
| P7-12b | Claude Code loggt sich ohne Nikinger als `testnutzer-p7` ein | Claude Code | ✅ derselbe Lauf wie P7-10 — Login/TOTP/Consent allein über `testcred.py` |
| P7-13 | Phase 6.5 formal abgeschlossen | Claude Code | ✅ Abschluss vollzogen (Phase 6.5 selbst steht 🟡, 12/14 — siehe `PHASE6_5_CLOSEOUT_HANDOVER.md`) |
| P7-14 | Eigener Space im Browser freigegeben, Empfänger sieht ihn | Niklas + `testnutzer-p7` | ✅ **[2026-08-27]** `niklas` teilte seinen Home-Space mit `testnutzer-p7` (lesen) über Konto → Spaces verwalten; zweiter Login als `testnutzer-p7` (`testcred.py`, ohne Nikinger) zeigte `niklas` sofort unter „Verbundene Spaces" (59 Items · nur lesen). Grant danach wieder entfernt (Aufräumen dieser Sitzung) |
| P7-15 | Zurücknehmen kein Re-Auth, Erweitern eines | Niklas | ✅ **[2026-08-27]**, beide Hälften live: Hinzufügen von `testnutzer-p7 (lesen)` verlangte „Diese Änderung erweitert Zugriffsrechte — Passwort und TOTP-Code nötig" (Nikinger gab beides ein); Entfernen desselben Mitglieds direkt danach lief ohne jede Re-Auth-Aufforderung durch (Toast „Mitglied entfernt · testnutzer-p7") |
| P7-16 | Neuer geteilter Space im Browser angelegt | Niklas | ✅ **[2026-08-27]** `p7-abnahme-space` über Konto → Spaces verwalten angelegt, Toast „Space angelegt", sofort in Sidebar/Space-Liste sichtbar (später im selben Lauf wieder entfernt, siehe P7-19) |
| P7-17 | Name-Kollision mit Principal abgewiesen | Claude Code, Test | ✅ **[2026-08-27]**, jetzt zusätzlich live: Anlegeversuch `fabian` (bestehender Principal-Name) im echten Browser → „'fabian' ist ein bestehender Principal-Name.", vom Nikinger live gesehen |
| P7-18 | Home-Space nicht entfernbar (Knopf fehlt, Route 403) | Claude Code, Test+Browser | ✅ Route: `test_home_space_cannot_be_removed` (403). Knopf fehlt: bestätigt gegen eine Wegwerf-Instanz (`spaceRemoveOpenEl.hidden = info.home` — Home-Space zeigte keinen „Space entfernen"-Knopf, ein anderer, nicht-Home-Space direkt danach zeigte ihn) |
| P7-19 | Space mit N Items entfernt → alle N im `_archive/` | Niklas | ✅ **[2026-08-27]** `p7-abnahme-space` mit 1 Item entfernt (Klartext-Konsequenz + getippte Bestätigung + Passwort/TOTP durch den Nikinger), niklas' Archiv 22→23, Item verifiziert unter `niklas > Archiv`, Status `archived` |
| P7-20 | Space mit nicht-schreibbarem Item nicht entfernbar, kein Teil-Move | Claude Code, Test | ✅ **mit Vorbehalt** — `test_removal_blocked_by_one_unwritable_item_moves_nothing` besteht nur über eine simulierte `can_write_item_as_human`-Divergenz: unter der echten Union-ACL-Semantik (`AclReader.grants_for_dir()` unioniert immer den Space-Root-Grant) macht ein P7-L-autorisierter Ausführender jedes Item automatisch schreibbar — ein realer Blocker ist mit echten `.share.yml`-Daten unerreichbar, der Pre-Flight-Check bleibt trotzdem die zweite, unabhängige Absicherung, die N9 verlangt. **Ein bereits archiviertes Item ist dagegen seit der siebten Contract-Öffnung (Zeile 12 der Modul-Tabelle) KEIN Blocker mehr** — `store.move()` verschiebt es korrekt ins Ziel-`_archive/`, `test_removal_moves_an_already_archived_item_to_the_home_archive` deckt genau das ab (ersetzt den vorherigen 403-Test aus dem ersten C4-Commit) |
| P7-21 | Entfernen ohne Namensbestätigung abgewiesen | Claude Code, Test | ✅ `test_removal_requires_reauth_and_typed_confirmation` (422 bei falschem `confirm`) |
| P7-22 | `space_admin_enabled=False` → Menüpunkt weg, Routen 404 | Claude Code, Test | ✅ Routenanteil: `test_all_five_routes_404_when_space_admin_disabled` **und** ein echter Server-Lauf (curl, `space_admin_enabled=False`) — `GET /api/v1/meta` → `"space_admin":false`, alle vier `/api/v1/spaces*`-Aufrufe → `404`. Menüpunkt-Anteil: Nikinger loggte sich selbst per Hand in die von Claude Code gesteuerte Tab ein (`niklas`/Passwort/TOTP, Zugangsdaten von Claude Code berechnet, nie gelesen — siehe Session-Block für den vollen Verlauf inkl. des ersten, gescheiterten Automatisierungs-Anlaufs), Konto-Dialog zeigt danach ausschließlich „Update-Log ansehen" — „Spaces verwalten" fehlt vollständig, `account-manage-spaces` bleibt via `meta.space_admin` ausgehängt |
| P7-23 | N-Auswahl wandert in einem Vorgang, ein Commit je Item | Niklas | ✅ **[2026-08-27]** Nikinger live gegen `e88a624`: zwei Items per Strg+Klick ausgewählt ("2 ausgewählt"), `Verschieben` → "2 Items verschieben", beide landeten in `IT-Sekus-Projekt` (Zähler 2→4) |
| P7-24 | Ein rechteerweiterndes Item in Auswahl → ein Formular, nicht N | Niklas | ❌ **[2026-08-27]** Formular selbst korrekt ("2 von 2 benötigen Passwort und Code" — EIN Dialog), aber der Nikinger musste ZWEI unterschiedliche TOTP-Codes eintippen, um beide Items durchzubekommen. Root Cause in `phase5_ui/webui/static/js/list.js:240` `moveSelectedItems()`: die Batch-Schleife ruft `PATCH /api/v1/items/{id}` sequenziell für jedes Item auf, reicht dabei aber dasselbe `credentials`-Objekt (ein Passwort+EIN TOTP-Code) unverändert an jeden Request durch. Der Server lehnt einen wiederverwendeten TOTP-Code als Replay ab (korrektes Sicherheitsverhalten) — das zweite (und jedes weitere) sequenzielle PATCH in derselben Batch-Runde scheitert deshalb strukturell, nicht zufällig. Für N>1 Items degeneriert das Zweirunden-Design (P6-AM) real Richtung "bis zu N Runden", nicht "höchstens 2" — genau das Gegenteil von P7-24s Anspruch. **Kein reiner UI-Fund wie P7-4, sondern ein Mechanismus-Fehler**: das gezeigte Formular ist korrekt, aber es kann pro Runde strukturell nur EIN Item wirklich durchbringen, wenn mehrere Items in derselben Runde re-auth brauchen. Fix-Optionen (nicht von Claude Code entschieden): (a) TOTP-Fenster serverseitig für Requests innerhalb desselben Batches tolerant machen (schwächt Anti-Replay, riskant), (b) Client wartet zwischen sequenziellen Requests auf einen neuen 30s-Fenster-Tick und fragt den Nutzer pro Fenster einmal (langsam, UX fragwürdig), (c) ehrlich dokumentieren: "ein Formular pro Runde" bedeutet bei TOTP-Widen-Batches in der Praxis oft mehrere Runden, P7-24s Kriterium selbst nachschärfen. Bleibt ⬜/❌ bis der Nikinger entscheidet |

**Geerbt und in dieser Phase nicht adressiert:** P6-Zeilen 7, 9, 14–17, 23, 25, 29, 30 sowie
P6.5-14 — bleiben im Handover offen, kein stilles Abhaken (Plan §6, Fußnote).

## Session stopped — 2026-08-24 (Manueller Purge gefahren, P6.5-12-Browserprobe: Deploy-Blocker gefunden, Versionsbump)

**Auftrag:** Fortsetzung derselben Sitzung, Datumswechsel während der Sitzung. Nikinger bot an,
den Purge (A6) manuell vorzuziehen und half beim P6.5-12-Browsernachweis mit eigenem Login.

**A6 — Purge manuell gefahren (Nikinger, `sudo systemctl start sharefyx-purge.service`).**
Baseline vorher (read-only): `clients: 54`, `token_families: 35`. Lauf `status=0/SUCCESS`, echte
Löschungen (`auth_requests: 8, auth_codes: 7, access_tokens: 15, invites: 1` — 31 Zeilen), aber
`clients`/`token_families` beide **unverändert bei 54/35**. Kein Fehlschlag — geprüft:
`TOKEN_FAMILY_RETENTION_S = 30*86400`, `CLIENT_RETENTION_S = 90*86400`
(`authserver/store.py:54,63`), ältester `clients`/`token_families`-Eintrag ist
`2026-07-29T15:02:27Z`. **Präzisierung gegenüber dem Plan-Text:** `token_families` wird ab
**2026-08-28** sichtbar sinken (deckt sich mit der Plan-Erwartung), `clients` aber erst ab
**2026-10-27** — fast zwei Monate später als angenommen. P7-9 bleibt ⬜, jetzt mit korrekter
Zeitangabe für beide Tabellen statt einer gemeinsamen.

**P6.5-12-Browserprobe: echter Fund, kein Bug.** Zweiter Login-Anlauf nötig — der erste
Nikinger-Login lief in einem Tab außerhalb meiner MCP-Tab-Gruppe, `sessionStorage`s
`sfx:csrf` wird ausschließlich von der `/ui/login`-POST-Antwort gesetzt
(`app.js:34-36`, `location.pathname !== "/ui/"`), ein reines Neuladen von `/ui/` liefert ihn
nicht nach — korrektes P5-H-Verhalten, kein Leck (erster Upload-Versuch schlug entsprechend mit
`403 csrf_failed` fehl). Nikinger loggte sich ein zweites Mal ein, diesmal im von mir
gesteuerten Tab (`testcred.py password`/`totp` in seinem eigenen Terminal, nie durch mich
gelesen). Upload gelang (`ast_2cf1ce2f`, `itm_ee1e0323`, PIL-PNG), Bild rendert sichtbar, `.md`
+ Asset-Datei korrekt im echten `DATA_ROOT`. **Aber:** `document.getElementById('asset-strip')`
→ `null` auf der Live-Seite. Ursache gefunden: **die Live-Instanz läuft weiterhin Release
`f96125e` (2026-08-21) — fünf Commits dahinter**, darunter A3 (`d974836`, baut genau dieses
`<div id="asset-strip">`). `docs/UPDATE_LOG.md`s oberster Eintrag ist auf `2026-08-23` datiert,
mit dem Datumswechsel auf `2026-08-24` würde `deploy.sh`s Gate (P6-X) jetzt ohnehin abbrechen.
**Kein Code-Fehler — der Knopf existiert im Repo, ist nur nie ausgeliefert worden.** P6.5-12
bleibt deshalb 🟡 ungeprüft, aus einem neuen, treffenderen Grund als zuvor.

**Deploy bewusst nicht selbst ausgeführt:** `deploy.sh` braucht `SHAREFYX_SYSTEMCTL="sudo
systemctl"` für den Restart-Schritt; `sudo -n true` bestätigte fehlende passwortlose Rechte
(`exit:1`). Genau die Art Aktion („live Dienst neu starten, beeinflusst laufende Sitzungen"),
die dieses Projekt konsequent dem Nikinger überlässt — kein Umgehungsversuch unternommen, dem
Nikinger die Optionen vorgelegt (selbst deployen / mir `sudo` geben / verschieben). **Nikinger-
Entscheidung: verschieben, Sitzung hier beenden, Test in der nächsten Sitzung.**

**Versionsbump, Nikinger-Auftrag:** `.rail__version` in `app.html` `v2.1` → `v2.2` (reiner
Hardcode wie die Wortmarke selbst, kein Test pinnt den String, kein Schema). Reitet mit dem
nächsten Deploy mit.

**Teardown:** Test-Asset `ast_2cf1ce2f` auf `itm_ee1e0323` per `p7_13_teardown.py` in `_trash/`
verschoben. Die Markdown-Referenz `![p65-browser-test.png](asset:ast_2cf1ce2f)` bleibt im Body
stehen (rendert nach dem nächsten Deploy als Alt-Text, V73-Konsequenz — bewusst nicht vorab per
Skript entfernt, da genau dieser Übergang Teil des nächsten P6.5-12-Nachweises ist).

**`pytest -q` weiterhin 843 passed.** Kein Quellcode dieser Sitzung geändert außer dem
Ein-Zeilen-Versionsbump; Tabu-Diff unverändert leer.

**Nächster Schritt, konkret:** vor der nächsten P6.5-12-Probe braucht es (1) einen neuen
`docs/UPDATE_LOG.md`-Eintrag datiert auf den Deploy-Tag (P6-X-Gate) und (2) einen echten
`deploy.sh`-Lauf durch den Nikinger (`sudo systemctl`-Rechte nötig). Danach: derselbe
Browser-Test wiederholen (Upload → Entfernen-Knopf → Alt-Text-Rendering →
`_trash/`-Dateiprüfung) — diesmal sollte `asset-strip` im DOM erscheinen. A6 bleibt bis
2026-08-28 (`token_families`) bzw. 2026-10-27 (`clients`) beobachtend offen, kein weiterer
Handgriff nötig.

**Nachtrag, 2026-08-25 — beide offenen Punkte erledigt, echter Deploy gefahren.** `docs/
UPDATE_LOG.md` bekam den neuen `## 2026-08-25`-Eintrag (Bild-Entfernen-Knopf angekündigt),
committet als `53bad20`. Danach fuhr der Nikinger `deploy.sh main` selbst (`sudo systemctl`-Recht
nötig, Claude Code hat das nicht). **Ergebnis, per Transkript:** Update-Log-Gate bestand ohne
Override, Health-Gate `/ui/login`→200/`/api/v1/me`→401/`/mcp/`→401 alle grün, Retention räumte
das älteste Release (`20260813...`) ab, JSON bestätigt `"result":"ok"`. **Read-only
gegengeprüft:** `readlink -f /opt/sharefyx/current` → `/opt/sharefyx/releases/
20260825T110849.160586Z`, `git -C /opt/sharefyx/current log --oneline -1` → `53bad20`, exakt der
Doku-Commit von oben — die Live-Instanz läuft damit fünf Commits weiter als vorher (`f96125e`)
und enthält jetzt A3s `<div id="asset-strip">`. **P6.5-12 ist damit wieder testbar, noch nicht
erneut geprobt** — nächster Schritt bleibt derselbe Browser-Test wie oben beschrieben, nur ohne
den Deploy-Blocker davor.

**Nachtrag, 2026-08-25 — P6.5-12/P7-5 per echtem Browser-Klick bestanden.** `testnutzer-p7` war
bereits über eine vom Nikinger geöffnete Tab eingeloggt (Cookie), meine eigene MCP-Tab teilt das
Cookie, aber `sessionStorage`s `sfx:csrf` ist tab-lokal und wird nur von der
`/ui/login`-Bootstrap-Antwort gesetzt (derselbe Mechanismus wie am 2026-08-23) — ein erster
Schreibversuch (Item anlegen) schlug entsprechend mit `CSRF-Token fehlt oder stimmt nicht` fehl.
Der Nikinger loggte sich erneut in der von mir gesteuerten Tab ein (eigenes Terminal, Zugangsdaten
nie durch mich gelesen); `sessionStorage.getItem('sfx:csrf')` bestätigte danach einen Token.

**Testablauf, per Transkript:** Item `itm_26f8d0b7` angelegt, `p65-retest.png` (4×4-PNG, per
PIL erzeugt) über `file_upload` + den echten Datei-Input hochgeladen, Asset-Chip
`ast_e60e8d8a` samt „×"-Knopf erschien im Asset-Strip (`ref_251`, ARIA-Label bereits „Bild
entfernen" — die vorher fehlende Fläche existiert jetzt wirklich im DOM). Vorschau bestätigte
das Bild vor dem Entfernen (`naturalWidth/Height:4`, korrekter `src`). „Bild entfernen" geklickt
→ Bestätigungsdialog „wird aus dem Dokument entfernt und in den Papierkorb des Items
verschoben" → bestätigt → Toast „Bild entfernt.". Vorschau danach: `p65-retest.png` als reiner
Text, kein `<img>`, kein Broken-Icon.

**Read-only gegengeprüft, nicht nur den Toast vertraut:** `.md`-Datei enthält weiterhin exakt
`![p65-retest.png](asset:ast_e60e8d8a)` — der Server schreibt die Referenz beim Entfernen nicht
um, nur die fehlende Asset-Datei macht sie zum Alt-Text (N5-Design, wie geplant). Datei liegt
real unter `_assets/itm_26f8d0b7/_trash/ast_e60e8d8a.png`. `git log` zeigt vier saubere,
getrennte Commits: `create` → `asset` → `update` (die `asset:`-Referenz im Body) →
`asset_trash` — kein Commit vermischt zwei Aktionen. Testitem danach archiviert
(`_archive/itm_26f8d0b7__...`), Trash-Asset bewusst nicht angerührt (ist der Beweis).

**Ergebnis: P6.5-12 ✅, P7-5 ✅ (via `testnutzer-p7`, gleicher Substitutionsgrund wie
P6.5-8/13 — dieselbe serverseitige Fläche, kein Bug-Risiko durch den Principal).**
`phase6_5_tools_images/CLAUDE.md` Abnahmestand jetzt **13 von 14** (nur noch P6.5-14 offen,
strukturell Nikinger-Sache). Modul-Status-Tabelle oben (P7-5) nachgezogen.

**Verifiziert:** keine Testsuite gelaufen (reine Live-Browser-/Doku-Session, kein Python-Diff).
Tabu-Diff nicht relevant.

**Offen für die nächste Session:** P7-9 (A6-Purge-Rückgang, `token_families` ab 2026-08-28,
`clients` ab 2026-10-27, rein beobachtend) — sonst nichts Neues aus dieser Sitzung.

**Nachtrag, 2026-08-25 — P7-1/P7-2/P7-7 per echtem Browser-Klick bestanden, git-Reparatur
zwischendurch.**

**Git-Zwischenfall (vor den Proben, beim Recherchieren von `p7_11_setup_fixture.py`):** `git
log` scheiterte mit `fatal: bad object HEAD` — der Commit `ef2e6be` (vorheriger Nachtrag dieser
Sitzung) war als acht 0-Byte-Objekte auf der Platte gelandet, alle mit demselben Zeitstempel
(13:28) — ein unterbrochener `git commit`-Schreibvorgang, isoliert auf genau dieses eine
Ereignis (`git reflog`/frühere Commits intakt, Arbeitskopie-Inhalt per `grep` gegengeprüft und
vollständig). **Reparatur nach expliziter Nikinger-Freigabe** (`git update-ref
refs/heads/main 6fb3eda...`, dann die acht verwaisten 0-Byte-Objekte gelöscht, `git read-tree
HEAD` gegen den stale Cache-Tree im Index, `touch` + `git add` + `git commit` neu) — Ergebnis
`6e60dbd`, `git fsck --full` danach sauber (nur harmlose dangling Objekte + eine veraltete
Reflog-Zeile, keine echte Beschädigung mehr). Kein Datenverlust: derselbe Inhalt, neuer,
gültiger Commit.

**P7-1 ✅, P7-2 ✅, P7-7 ✅** — Details in der Modul-Status-Tabelle oben. Zwei Nebenfunde beim
Bauen:
- **Freigeben-Dialog für `testnutzer-p7` ist strukturell leer**, nicht kaputt — `dialogs.js:262-
  266` (P6-V) listet nur `state.spaces`, und `testnutzer-p7` kennt (space-level) keinen anderen
  Space. Exakt der Fall, für den `p7_11_setup_fixture.py` existiert; hier zusätzlich bestätigt,
  dass ein leerer `Speichern`-Klick ein echtes, harmloses No-op-PATCH auslöst (Version bumpt, kein
  Fremdfeld erscheint) statt gar nichts zu tun.
- **`navigator.clipboard.readText()` per `javascript_tool` hängt den Tab auf** (45s-Timeout,
  „renderer möglicherweise eingefroren") — vermutlich ein Chrome-Berechtigungsprompt außerhalb
  des DOM, den Screenshots nicht zeigen. Nicht weiter verfolgt, seitdem gemieden: DOM-sichtbare
  Bestätigungen (Toast-Text, Quellcode-Verifikation der `.then()`-Kette) reichen als Beweis und
  sind ohnehin die robustere Prüfung.

**Aufräumen:** `p7_11`-Fixture-Freigabe (`share_read:[testnutzer-p7]` auf `itm_3d0ac2b3`) bewusst
**nicht** zurückgenommen — falls P7-2 später erneut vorgezeigt werden soll, ist die Fixture
sofort wieder nutzbar; Rücknahme ist Teil des ohnehin fälligen P7-12-Abbaus. Testitem `itm_
68f0251d` archiviert (`_archive/`), Test-Ordner `p7-7-test` bleibt (kein Lösch-Mechanismus für
leere Ordner in der UI, kein Schaden).

**Verifiziert:** kein Python-Code geändert (nur `.md`), Tabu-Diff nicht relevant. Kein `pytest`-
Lauf nötig — reine Live-Browser-/Git-Reparatursession.

**Damit bleiben aus dem P7-A-Rest nur noch: P7-4 (braucht Niklas selbst mit einem echten
Connector-Gespräch — nicht durch Claude Code allein herstellbar), P7-9 (kalendergebunden,
2026-08-28/2026-10-27) und P7-12 (Testnutzer-Abbau — laut eigenem Docstring „am Ende von Block
A"; mit P7-1/2/5/6/7/8/10/11/12b jetzt erledigt ist nur noch P7-9 offen, das `testnutzer-p7`
nicht braucht — der Abbau ist damit möglich, aber eine Nikinger-Entscheidung, kein automatischer
nächster Schritt).**

**Nachtrag, 2026-08-25 — P7-4 erster echter Befund (❌), P7-12 bewusst NICHT geschlossen.**

**P7-4:** Nikinger fragte im Webchat (Doku-Stand dort veraltet, unerheblich für diesen Befund)
„welche 3 Items sind die aktuellsten" — eine organische, ungestellte Probe genau des P7-4-
Kriteriums. Antwort kam als Tabelle mit jeder Zeile eingeleitet durch die rohe `itm_…`-ID, Titel
nur angehängt (`itm_3d0ac2b3 — P7-11 Sichtbarkeitsprobe...`). Das widerspricht dem Satz, der
wortgleich in vier Tool-Beschreibungen steht (`mcpserver/tools.py`: „Nenne einem Menschen
gegenüber immer den Titel eines Items, nicht seine itm_...-ID"). Kein Code-Fehler — die
Prosa-Anweisung reicht offenbar nicht gegen den Sog einer tabellarischen Antwort, wo `id` als
Feldname aus `search_items`s eigenem Rückgabeschema naheliegt. Modul-Status-Tabelle oben
(P7-4 ❌) nachgezogen. Bleibt ein UX-/Formulierungs-Befund, keine neue Aufgabe ohne
Nikinger-Entscheidung, ob/wie die Tool-Beschreibung geschärft werden soll.

**P7-12 — Nikinger-Auftrag „schließen, falls für spätere Blöcke nicht gebraucht" geprüft, Ergebnis:
gebraucht.** Gegen den Plan geprüft, nicht gegen den eigenen Docstring von `p7_11_setup_fixture.py`
(der nur „am Ende von Block A" sagt, ohne Block C zu kennen): `docs/concepts/
phase7_spaces_admin_plan.md` §Block C, **P7-14** — „Ein Mensch gibt seinen eigenen Space im
Browser für einen anderen zum Lesen frei; der andere sieht ihn danach", Wer: **Niklas +
`testnutzer-p7`**. Block C ist komplett ungebaut (P7-14–P7-22 alle ⬜) und braucht `testnutzer-p7`
ausdrücklich als Empfänger-Principal. **Ein Abbau jetzt („Block A ist fertig") würde P7-14 später
zwingen, den Principal neu anzulegen** — Mehrarbeit statt Ersparnis, und der Plan selbst enthält
diesen Widerspruch bereits (A7s „Abbauen, am Ende von Block A" wurde offenbar geschrieben, bevor
Block C den Principal als Testpartner brauchte). **Datierte Korrektur:** P7-12 bleibt bis nach
Block C offen, nicht „am Ende von Block A" — der Plan-Snapshot selbst bleibt unverändert (📕),
diese Zeile hier ist die maßgebliche Korrektur. Kein Handgriff ausgeführt, keine Löschung.

**Nachtrag, 2026-08-25 — Gate A→C geprüft: alle vier Punkte live, Block C gestartet (Nikinger-
Auftrag „next block should be unblocked").**

**Gate-Prüfung** (Plan `docs/concepts/phase7_spaces_admin_plan.md` §0/Block-C-Vorspann, vier
Punkte, alle vier live vor der ersten Zeile Block-C-Code):

| # | Kriterium | Beleg |
|---|---|---|
| 1 | Item per `itm_…`-ID im Browser gefunden | P7-1 ✅ (siehe oben) |
| 2 | Bild entfernbar, Alt-Text-Rendering, Datei in `_trash/` | P7-5 ✅ (siehe oben) |
| 3 | Migration gelaufen, 0 Dateien ohne `visibility:` | P7-8 ✅ (73/73) |
| 4 | `testnutzer-p7` echter Cross-Principal-Lesetest | P7-11 ✅ (Web-UI **und** MCP) |

Alle vier bereits vor dieser Sitzung geschlossen, hier nur formal gegen den Plan-Wortlaut
nachgeprüft — **Gate offen, Block C gestartet.**

**Step C1 gebaut — Schreibseite von `.share.yml` in `storage/acl.py` (sechste Contract-
Öffnung, P7-P).** Reine Extraktion aus `phase6_shares/scripts/spacectl.py`
(`_load_share_file`/`_dump_share_file`/`_spaces_referencing`, Schreibbodies von
`_cmd_create_space`/`_cmd_add_member`/`_cmd_remove_member`/`_cmd_remove_space`), kein neues
Verhalten. Anker vor dem Bau gegen den echten Code geprüft (nicht nur den Plan-Snapshot
übernommen) — Zeilennummern im Plan wichen leicht ab (Funktionen um wenige Zeilen gewachsen seit
`f5691e0`), Funktionsnamen stimmten exakt, wie vom Plan selbst vorgeschrieben.

Neu in `acl.py`: `read_share_file`/`write_share_file`/`add_member`/`remove_member`/
`create_space`/`remove_space_dir`/`spaces_referencing`/`AclWriteError`, plus `_WriteLock`
(dieselbe Bauart wie `spacectl.py`s bisherige `_DataRootLock`, jetzt die einzige verbleibende
Kopie). Jede Schreibfunktion nimmt den `.write.lock`-Flock selbst und gibt ihn vor der Rückkehr
frei — kein Aufruf einer `Store`-Methode darin (P7-M, Selbst-Deadlock-Vermeidung). `spacectl.py`
ruft jetzt `acl.*` auf; `_DataRootLock` ist komplett entfallen, `_load_share_file`/
`_find_share_files` bleiben (nur noch für `check`, rein lesend). Modulkopf-Docstring von
`spacectl.py` entsprechend nachgezogen (die Lock-Beschreibung war sonst stale gewesen).

**Verifiziert:** `phase6_shares/tests/test_spacectl.py` (20 Tests) **unverändert**, weiterhin
grün — der Regressionsbeweis der Extraktion. `phase6_shares/tests/test_characterization.py` (3
Golden Files) vor und nach byte-identisch grün (P7-C/P6-D). 19 neue Tests in
`phase7_spaces_admin/tests/test_acl_write.py`. Ein eigener Testfehlschlag korrigiert vor dem
Commit, kein Code-Fund: `test_remove_member_removes_from_both_lists` nahm fälschlich an, ein
`write=True`-Add trage den Namen auch in die Roh-Liste `read:` ein — `write:` impliziert `read:`
nur beim Lesen (`AclReader._parse`), nicht in der Datei selbst; Test korrigiert, schreibt den
Doppel-Eintrag jetzt direkt, um den echten Zwei-Listen-Entfernen-Pfad zu prüfen. `pytest -q`
volle Suite: **843 → 862** (Baseline vor dieser Sitzung read gegengezählt, nicht angenommen).
Tabu-Diff (`asgi.py`/`server.py`/`permissions.py`/`authserver/{crypto,totp,passwords,resolver,
flows}.py`) leer.

**Nachtrag, 2026-08-25 — Advisor-Runde nach dem C1-Commit, vier Funde, alle vier behoben in
einem Folgecommit.** Versäumnis vorweg: der Advisor-Call vor dem Commit (Standing-Feedback
dieses Projekts) wurde übersprungen, erst danach nachgeholt. `409fe18` wurde bewusst **nicht**
amended (Projektregel) — die vier Funde landen als eigener Commit mit eigenem Doku-Update.

1. **Dead Code + versteckte Divergenzquelle:** `write_share_file()` inlinete `yaml.safe_dump`+
   `atomic_write`+leer-löschen ein drittes Mal, `add_member`/`remove_member` je ein zweites Mal —
   und `write_share_file()` konnte von den beiden nie aufgerufen werden (P7-M-Deadlock, es nimmt
   den Lock selbst, sie halten ihn schon). Genau die Divergenzquelle, die P7-P verhindern sollte,
   nur ins Modul verlagert statt entfernt. **Behoben:** neues privates
   `_write_share_file_unlocked(path, data)` hält die Dump-Logik einmal; `add_member`/
   `remove_member` rufen es innerhalb ihres Locks auf, `write_share_file()` bleibt der
   öffentliche, lockende Wrapper darum. Der Deadlock ist jetzt durch Bauart unerreichbar, nicht
   nur per Kommentar vermieden.
2. **Commit-Betreffs waren nie gepinnt.** Der Plan verlangt die drei exakten Formate (`share
   <space> <key>+=<name>` / `unshare <space> <name>` / `remove-space <name>`) — genau das Stück,
   das die `DATA_ROOT`-Historie (Hard Rule 5, Undo-Pfad) leise brechen könnte, war ungeprüft.
   **Behoben:** die drei Commit-Tests in `test_acl_write.py` assertieren jetzt zusätzlich `git
   log -1 --format=%s` gegen den exakten Wortlaut.
3. **`phase1_storage/CLAUDE.md`s Modul-Tabelle fehlte Zeile 14** für die sechste Öffnung — der
   „Geerbte Contracts"-Absatz war da, die Tabellenzeile (Präzedenzfall: Zeile 13 bei der fünften
   Öffnung) fehlte. Nachgetragen, `Gesamt: 150` unverändert (Tests liegen außerhalb des Pakets,
   dieselbe Konvention wie Zeile 10).
4. **`acl.py`s Kopf-Docstring war nach dem Umbau falsch** — beschrieb das Modul weiterhin als
   rein lesend/fail-closed. Nachgezogen: zwei Sätze, die den bewussten Zwei-Pfade-Schnitt nennen
   (lesend fail-closed via `AclReader`, schreibend laut via `read_share_file`/`add_member`/…).

**Verifiziert:** 43/43 (`test_acl_write.py` + `test_spacectl.py` + Charakterisierung), volle
Suite **862/862** unverändert (Umbau, keine neuen Tests — drei bestehende umbenannt/erweitert).
Tabu-Diff weiterhin leer.

**Zweite Advisor-Runde, diesmal vor dem Commit (wie es sein soll), vier weitere Funde, alle
behoben:**

1. **`_dump_share_file` in `spacectl.py` war tot** — meine erste Edit-Runde ersetzte beide
   Aufrufer (`_cmd_add_member`/`_cmd_remove_member`), ließ die Funktionsdefinition selbst aber
   stehen (sie lag außerhalb des ersetzten `old_string`-Bereichs). Entfernt. Die Modul-Tabellen-
   zeile oben widersprach sich zusätzlich selbst („`_load_share_file` entfällt … bleibt") —
   richtiggestellt: entfallen sind `_DataRootLock`/`_dump_share_file`/`_spaces_referencing`,
   geblieben sind `_load_share_file`/`_find_share_files` (nur noch für `check`).
2. **`read_share_file()`s `AclWriteError`-Zweig (nicht-Mapping-YAML) war ungetestet** — die
   bestehende Malformed-YAML-Probe pinnt nur den `yaml.YAMLError`-Zweig. Zwei neue Tests: einer
   direkt gegen `read_share_file()`, einer gegen `add_member()` mit demselben kaputten Bestand
   (weder `add_member` noch `remove_member` fangen die Exception ab — bewusst, dieselbe „laut
   statt fail-closed"-Haltung wie beim direkten Lesen, kein Verhaltensunterschied zur alten
   `spacectl.py`-Fassung, die genauso unabgefangen `ValueError` warf).
3. **Plan-Testfall „leere Liste verschwindet" fehlte** — bisher nur „leere Datei wird entfernt"
   abgedeckt. Neuer Test: `read:`+`write:` beide besetzt, ein Name aus `read:` entfernt macht
   `read:` leer → der Schlüssel fehlt danach ganz (nicht `read: []`), die Datei bleibt (wegen
   `write:`) bestehen.
4. **`write_share_file()` hatte keine eigene Testabdeckung** — zwei neue Tests: Round-Trip durch
   `read_share_file()`, und leeres `data` entfernt eine bestehende Datei.

**Verifiziert (zweite Runde):** `test_acl_write.py` jetzt **24** Tests (`--collect-only`
gegengezählt, nicht addiert), zusammen mit `test_spacectl.py`+Charakterisierung **48/48** grün.
Volle Suite **862 → 867** (real gezählt). Tabu-Diff weiterhin leer.

**Nächster Schritt, konkret:** Step C2 (REST-Fläche, fünf neue Routen unter `/api/v1/spaces*`,
`webui/shares.py`-Erweiterung um `require_space_reauth()`) — Anker (`api.py:743-755`,
`api_routes()`-Signatur, `UserDirectory`-Principal-Check V76) vor dem Bau gegen den echten Code
prüfen, wie bei C1. Advisor-Call **vor** dem C2-Commit, nicht danach.

**Nachtrag, 2026-08-25 — Step C2 gebaut (Nikinger-Auftrag „Lets go on with C2"), zwei
Advisor-Runden vor dem Commit.**

**Vier von fünf Routen aus Plan §4.C2** (`POST /api/v1/spaces`, `GET/POST .../members`,
`DELETE .../members/{name}`) — `DELETE /api/v1/spaces/{space}` bleibt bewusst C4, siehe
Modul-Tabelle oben. Anker vor dem Bau geprüft: `api_routes()`-Signatur trägt bereits alles
Nötige (keine neue Parameter), Route-Tabelle liegt bei `api.py:779-802` (Plan nennt 743-755,
kosmetische Zeilendrift wie bei C1). **Ein Plan-Textfund:** §4.C2 beschreibt eine Extraktion
von `require_share_reauth()`s Credential-Hälfte in `_verify_reauth_credentials()` — diese
Extraktion existiert bereits, als `webui/reauth.py :: verify_reauth()`, gebaut vor dieser Phase
und von `account.py` UND `shares.py` bereits geteilt. `require_space_reauth()` ruft sie direkt
auf, keine Restrukturierung von `shares.py` nötig — der Plan-Text war insofern stale, spart
aber Arbeit, kostet keine.

**Erste Advisor-Runde (vor dem ersten Commitversuch), zwei Blocker + zwei Doku-Lücken:**

1. **Frisch angelegter Space war für niemanden sichtbar oder verwaltbar.**
   `acl.create_space()` legt bewusst nur ein leeres Verzeichnis an (dieselbe Zurückhaltung wie
   `spacectl.py create-space`, ein CLI-Operator ruft danach selbst `add-member` auf) — über die
   Weboberfläche gibt es diesen zweiten Handgriff aber nicht. **Fix:** `_spaces_post` seedet den
   Anlegenden direkt danach als `write`-Mitglied (`acl.add_member(..., write=True)`) — zwei
   Commits (`create-space` selbst committet nichts, der Seed-`add_member` einen), korrekt: die
   Mitgliedschaft ist eine echte Rechteänderung und gehört in die Historie. Ohne den Fix hätte
   P7-16 („neuer geteilter Space erscheint im Baum") strukturell nie bestehen können.
2. **`GET .../members` hatte gar keine Autorisierung.** Die Plan-Begründung dafür („spiegelt
   `GET /api/v1/spaces`, das zeigt Mitgliedschaft auch") war sachlich falsch — `_spaces` filtert
   über `_visible_space_infos()`/`permissions.visible_spaces()`, der neue Handler nahm `space`
   ungeprüft aus dem Pfad. Das öffnete ein Existenz-Orakel über beliebige Space-Namen,
   Mitglieder-Enumeration für nicht-lesbare Spaces, und (über `orphans`) einen Leak-Kanal quer
   über den ganzen `DATA_ROOT`. **Fix:** `permissions.can_read(session.space, space)`-Gate,
   `403` sonst; `manageable` bleibt der Render-Hinweis fürs Frontend.
3. `space_admin`-Feld in `_meta` war ungetestet — nachgetragen (`test_meta.py`).
4. Kill-Switch-Abdeckung nur 2 von 4 Routen — auf einen parametrisierten Test über alle vier
   ausgeweitet.

**Zweite Advisor-Runde (nach den ersten vier Fixes, vor dem tatsächlichen Commit), ein
weiterer Blocker:** `orphans` implementierte den falschen Namen — der Plan-Satz nennt
`acl.spaces_referencing()`, beschreibt aber „Namen ohne zugehörigen Space" — das ist
`spacectl.py check`s Semantik (Tippfehler in `read:`/`write:` gegen bekannte Space-Verzeichnisse
prüfen), nicht „wer verweist auf mich" (das ist tatsächlich `spaces_referencing()`s Job, und
C4s eigene Sache). **Fix:** `_space_members_get` vergleicht `grant.read | grant.write` jetzt
gegen die real existierenden Space-Verzeichnisse (`store.data_root.iterdir()`), dieselbe
Prüfung wie `_cmd_check`. Die `not is_home`-Ausnahme ist mit dem Fix ebenfalls gefallen — ein
Tippfehler im eigenen Home-Space ist genauso meldenswert. **Datierte Plan-Korrektur, wie bei
C1s P7-12-Zeitpunkt:** §4.C2s `orphans`-Beschreibung war intern widersprüchlich (Funktionsname
vs. beschriebenes Verhalten); der 📕-Snapshot bleibt unverändert, diese Zeile ist die
maßgebliche Korrektur.

**`atomic_write()`-Randfrage aus der ersten Runde geklärt, kein Fund:** `tempfile.mkstemp(dir=…)`
wirft `FileNotFoundError` auf einem fehlenden Space-Verzeichnis, legt keine Elternverzeichnisse
an — `acl.add_member()` auf einen nicht existierenden Space kann `create_space()`s
Namens-Riegel also nicht umgehen. Nichts zu tun, für C4 vermerkt.

**Verifiziert:** 21 neue Tests in `test_space_admin_api.py` (eigene Fixtures — `phase5_ui/tests/
conftest.py` ist kein Vorfahre von `phase7_spaces_admin/tests/`, dieselbe Isolation wie
`test_acl_write.py`), +1 `test_meta.py`, +1 `test_store.py` (`Store.data_root`-Property). Alle
gegen `--collect-only` gezählt, nicht addiert. Volle Suite **867 → 890**. Tabu-Diff leer.

**P7-22 bleibt ⬜, explizit benannt statt stillschweigend:** „`space_admin_enabled=False` lässt
alle fünf Routen `404` antworten" — vier von fünf sind jetzt getestet (parametrisierter
Kill-Switch-Test), die fünfte (`DELETE /api/v1/spaces/{space}`) existiert erst mit C4. „C2
fertig" heißt hier ausdrücklich nicht „P7-22 erfüllbar".

**Nächster Schritt, konkret:** Step C4 (Space entfernen, zweiphasig, P7-O/N8/N9) vor C3 (UI) —
C3s Entfernen-Dialog bräuchte sonst eine Route, die noch nicht existiert; C4 zuerst gibt C3 ein
vollständiges Backend in einem Rutsch. Anker vor dem Bau prüfen: `_STORE_FETCH_LIMIT`
(V78), `store.move()`/`store.archive()`-Reihenfolge, Lock-Disziplin (P7-M) für die
Vorlauf/Durchlauf-Schleife. Advisor-Call **vor** dem Commit.

**Nachtrag, 2026-08-25 — Step C4 gebaut (Nikinger-Auftrag „lets go on with C4"), ein
Advisor-Fund vor dem Commit behoben.**

Anker gegen den echten Code geprüft, nicht nur den Plan-Snapshot übernommen:
`_STORE_FETCH_LIMIT` (`api.py:145`, Plan nennt `144` — dieselbe Ein-Zeilen-Drift wie bei C1/C2),
`store.archive()`/`store.move()` (`store.py:586–663`, Reihenfolge durch `archive()`s
`folder=""`/`_archive/`-Ablage erzwungen — ein vorheriger `move()` würde die Datei sonst an die
Zielspace-Wurzel setzen, nicht ins Zielarchiv), `acl.remove_space_dir()` (`acl.py:291–301`,
kein eigener Vorlauf — das ist ausdrücklich C4s Job), `require_space_reauth()`
(`shares.py:96–121`, flacher `widening`-Flag statt `widens()`-Vergleich, exakt wie geplant).

`webui/api.py :: _spaces_delete` — fünfte Route `DELETE /api/v1/spaces/{space}`. Reihenfolge wie
im Plan: P7-K (bekannter Principal → 403) → P7-L (`can_write(home, space)` → 403) → Vorlauf
(`store.search()`-Paging über `_STORE_FETCH_LIMIT`, Blocker-Scan) → `require_space_reauth
(widening=True)` + `confirm == space` → Durchlauf (`move()`→`archive()` je Item, `ConflictError`
→ Abbruch mit beiden Listen) → harte `len(moved) == total`-Sperre → `acl.remove_space_dir()`.
Antwort trägt zusätzlich `orphan_refs` (`acl.spaces_referencing()`, vor dem `rmtree` berechnet,
da danach die eigene `.share.yml` des entfernten Space nicht mehr existiert).

**Advisor-Fund vor dem Commit (empirisch verifiziert, nicht nur behauptet):** ein Testfall mit
einem bereits archivierten Item im Zielspace fehlte. Direkt geprüft (`store.create()` +
`store.archive()` + `store.search()` gegen ein Wegwerf-`tmp_path`): `search()`s `total` zählt
archivierte Items mit, `store.move()` verbietet sie aber ausdrücklich
(`ValidationError("... ist archiviert — move verboten")`, `store.py:626–627`). Ohne einen
eigenen Riegel hätte das einen unbehandelten `ValidationError` mitten im Durchlauf ausgelöst —
ein `500` nach bereits verschobenen Items, ohne den von N9 verlangten Bericht mit beiden Listen.
**Behoben:** ein zweiter, eigener Vorlauf-Riegel (`archived_blockers`) lehnt die Entfernung
fail-closed ab, wenn der Space bereits archivierte Items enthält — genau wie beim
Schreib-Blocker wird dabei **nichts** bewegt. **Das ist eine bewusst offene Frage, keine stille
Lücke:** N8 sagt, Items sterben nie — aber der Store hat keine API, ein bereits archiviertes
Item in einen anderen Space zu verschieben. Eine Space mit Historie ist damit vorerst
unentfernbar. Ob das dauerhaft tragbar ist oder eine siebte, benannte Contract-Öffnung braucht
(`storage/store.py` bekäme eine Move-Variante für archivierte Items), ist eine Nikinger-
Entscheidung — dieser Commit trifft sie nicht, sondern hält die Grenze fail-closed.

**Zweiter, kleinerer Advisor-Fund:** `acl.spaces_referencing()` fehlte das `exclude=`, das
`spacectl.py remove-space` für dieselbe Prüfung setzt (die eigene `.share.yml` des entfernten
Space zählt dort nicht als Fremdreferenz auf sich selbst) — Parität-Drift gegen P7-Ks „volle
`spacectl.py`-Parität", behoben (`exclude=store.data_root / space / acl.ACL_FILENAME`).

**Ein weiterer, unabhängig entdeckter Fund beim Testen (kein Advisor-Fund, sondern ein eigener
Testflakiness-Fehler dieser Session):** der erste Entwurf des Konflikt-Abbruch-Tests nahm an,
`store.search()` liefere Items in Erstellungsreihenfolge — im vollen `pytest`-Lauf (echte
Wanduhr statt eines injizierten `now_fn`, `item_store`-Fixture hier bewusst ohne `now_fn` wegen
der Git-Commit-Reihenfolgeprüfungen) zeigte sich, dass die tatsächliche Suchreihenfolge davon
abweicht. Test korrigiert: er fragt `store.search()` selbst nach der Verarbeitungsreihenfolge,
statt eine Reihenfolge anzunehmen, die `_spaces_delete` nirgends verspricht.

**Kill-Switch-Testlücke aus dem C2-Commit geschlossen:** `test_space_admin_api.py`s
parametrisierter Kill-Switch-Test deckte bis jetzt nur vier von fünf Routen ab (die fünfte
existierte zum Zeitpunkt von C2 noch nicht). Um die neue `DELETE /api/v1/spaces/{space}`-Zeile
ergänzt — schließt den Testanteil von P7-22, der sonst als offener Rest hätte weitergetragen
werden müssen.

**Abnahmestand:** P7-20 ✅ *mit Vorbehalt* (der Schreib-Blocker ist unter der echten Union-ACL-
Semantik — `AclReader.grants_for_dir()` unioniert immer den Space-Root-Grant — mit echten
`.share.yml`-Daten unerreichbar, siehe Kommentar in `_spaces_delete`; der Test simuliert die
Divergenz direkt. Der archivierte-Item-Blocker aus demselben Kriterium ist dagegen real
erreichbar und eigenständig getestet). P7-21 ✅. P7-22 Testanteil geschlossen, Browser-Anteil
bleibt C3. Modul-Status-Tabelle (Zeile 11) und Abnahmestand-Tabelle oben nachgezogen.

**Verifiziert:** 8 neue Tests in `phase7_spaces_admin/tests/test_space_removal.py` (Vorlauf-
Blocker × 2 — Schreibrecht + bereits archiviert —, sauberer Durchlauf, Assets wandern mit, zwei
Commits je Item + ein `remove-space`-Commit, Verzeichnis weg, `ConflictError`-Abbruch mit beiden
Listen, Home-Space-Riegel, Re-Auth+Bestätigung), +1 in `test_space_admin_api.py` (Kill-Switch-
Zeile). Volle Suite **890 → 900**, real gezählt (`pytest -q`, nicht addiert). Tabu-Diff
(`asgi.py`/`server.py`/`permissions.py`/`authserver/{crypto,totp,passwords,resolver,flows}.py`)
leer. Kein neuer Contract-Absatz nötig — C4 fügt `storage/` nichts hinzu, es ruft nur bereits
bestehende Funktionen (`store.search/move/archive`, `acl.remove_space_dir/spaces_referencing`)
aus `webui/api.py` heraus auf.

**Nächster Schritt, konkret:** C3 (UI) — Entfernen-Dialog gegen die jetzt vollständige C2/C4-
REST-Fläche, Kill-Switch tatsächlich verdrahten (schließt P7-22s Browser-Anteil und macht
`space_admin_enabled` erstmals produktiv scharf), Home-Space-Ausnahme im Menü (P7-18s
Browser-Anteil). Danach Step C5 (Betrieb/Doku).

**Nachtrag, 2026-08-25 — Nikinger-Entscheidung zur oben offen gelassenen Frage: siebte
Contract-Öffnung statt dauerhaftem `archived_blockers`-Riegel.**

Auf Nachfrage empfohlen (Begründung: eine Space mit `_archive/`-Inhalt ist der Normalfall, nicht
der Ausnahmefall — jede Space mit echter Nutzungshistorie hätte sonst permanent unentfernbar
bleiben müssen, das widerspricht N8 direkter als eine kleine Erweiterung des Contracts es tut),
vom Nikinger bestätigt („do that then").

**Umgesetzt in `phase1_storage/storage/store.py`** (Anker vor dem Bau geprüft: `move()` bei
`store.py:617–663`, `_write_item_file()` bei `276–291`, `create()` bei `463–489`, alle drei
Guard-Vorkommen `"ist archiviert"` bei Zeilen 493/544/570/627 gegengezählt — nur `move()`s
Guard bei 627 wird relaxiert, die drei anderen (`update`/`append`/`patch`) bleiben unverändert):

- `move()`: der Guard `if current.status == "archived": raise ...` wird zu
  `if current.status == "archived" and folder not in (None, ""): raise ...` — ein reiner
  Space-Wechsel ist jetzt erlaubt, ein echter Ordner-Wechsel bleibt verboten (archivierte Items
  tragen nie eine Ordnerposition).
- `_write_item_file()` bekommt einen Sonderfall: `item.status == "archived"` routet den
  Zielpfad auf `<space>/_archive/<file>` statt über `files.item_path()` (das `_archive/` nicht
  kennt) — dieselbe Pfad-Sonderbehandlung, die vorher exklusiv `archive()`s eigener,
  separater Code hatte, jetzt am gemeinsamen Schreibpfad. Vor diesem Fix hätte ein `move()`
  auf ein archiviertes Item die Datei an die Ziel-Space-Wurzel gesetzt — physisch „entarchiviert“,
  während das Frontmatter weiter `status: archived` behauptet hätte.
- **Zweiter Advisor-Fund, vor demselben Commit:** `create(status="archived")` ist über
  `POST /api/v1/items` erreichbar (`_items_post`s Feld-Whitelist enthält `status`,
  `STATUS_VALUES` erlaubt `archived` für `note` **und** `task` seit der P2-Öffnung) und lief am
  ursprünglichen `move()`-Guard naturgemäß nie vorbei — der `_write_item_file()`-Fix hätte hier
  aber eine neue Divergenz erzeugt (Datei landet in `_archive/`, das zurückgegebene `Item`-Objekt
  im Speicher trägt trotzdem noch das angeforderte `folder`, bis der nächste `get()` es aus dem
  echten Pfad neu ableitet und verwirft). **Fix:** `create()` setzt `folder=""` selbst, sobald
  `status="archived"` — dieselbe Zurücksetzung, die `archive()` seit je her vornimmt, hier nur
  vorgezogen. Ein direkt als `archived` angelegtes Item verhält sich damit identisch zu einem,
  das später archiviert wurde.
- `_spaces_delete` (`webui/api.py`) verliert den `archived_blockers`-Riegel aus dem vorherigen
  Commit ersatzlos; der Durchlauf ruft `archive()` nur noch für Items auf, die `move()` nicht
  bereits als `status == "archived"` zurückgibt (kein doppelter Commit auf einem schon
  archivierten Item).

**Verifiziert:** `phase1_storage/tests/test_store.py`s `test_move_of_archived_item_is_rejected`
durch drei Tests ersetzt (Ordner-Wechsel weiterhin verboten, Space-Wechsel relokiert korrekt ins
Ziel-`_archive/`, genau ein `move`-Commit) + ein neuer Test für `create(status="archived")`.
`phase7_spaces_admin/tests/test_space_removal.py`s bisheriger 403-Test (`archived_blockers`)
durch einen 200-Test ersetzt, der zusätzlich gegenprüft, dass das bereits archivierte Item
KEINEN zweiten `archive`-Commit bekommt. Charakterisierung (P6-D/P7-C,
`phase6_shares/tests/test_characterization.py`) vor und nach byte-identisch grün. Volle Suite
**900 → 903**, real gezählt. Tabu-Diff weiterhin leer.

**Dated Plan-Korrektur** (wie bei C1s P7-12-Zeitpunkt und C2s `orphans`-Fund): Plan §4.C4s
Pseudocode ruft `store.archive()` unterschiedslos nach jedem `move()` auf — der tatsächliche
Code ruft es nur noch für Items auf, die nicht schon archiviert waren. Der 📕-Plan-Snapshot
bleibt unverändert, diese Zeile ist die maßgebliche Korrektur.

**Dokumentation der siebten Öffnung** (Ankündigung + Bau in derselben Sitzung, kein separater
Ankündigungs-Absatz vorher) steht vollständig in `phase1_storage/CLAUDE.md`s „Geerbte
Contracts" — Modul-Status-Zeile 15 dort, Gesamtzahl-Korrektur 150→154 (davon 151 korrigierte
Baseline aus einer übersehenen Zeile-10-Ergänzung in C2, +3 netto aus dieser Öffnung).

**Nächster Schritt, konkret:** unverändert C3 (UI) — die archivierte-Items-Frage ist jetzt
geschlossen, kein offener Posten mehr dafür.

**Nachtrag, 2026-08-25 — Step C3 gebaut (Nikinger-Auftrag „lets go on with C4" führte zu C4,
danach Rotationsversuch + Fortsetzung mit C3), ein Advisor-Fund mit zwei Teilen vor dem Commit
behoben, echter Browser-Lauf gegen eine Wegwerf-Instanz.**

**Rotationsversuch zuerst:** `scripts/rotate_session_block.sh phase7_spaces_admin` auf
Nikinger-Vorschlag gefahren — Ergebnis „Bereits konform: genau ein Session-Block im Head.
Nichts zu tun." (`exit 2`). Die ~58KB dieses Heads sind kein Rotationsrückstand (die Regel
rotiert beim Start eines NEUEN `## Session stopped`-Blocks, nicht nach Größe) — dieser Kopf
trägt seit Sitzungsbeginn genau einen Block, gewachsen über viele Nachträge derselben
fortlaufenden Sitzung. Kein Handgriff möglich, bis eine wirklich neue Session beginnt.

**C3 gebaut, drei gekoppelte Stellen in einem Commit (Plan §4.C3):** `app.html:283`s
Menüpunkt verliert `disabled`/„kommt in Phase 7" → „Spaces verwalten"; `config.py`s
`space_admin_enabled` Default `False`→`True`; `test_static_routes.py`s Stub-Test ersetzt.
**Zwei Plan-Positionen erwiesen sich als bereits erledigt, keine neue Arbeit:** `_meta`
trug `space_admin` bereits aus Step C2, `.rail__version` stand bereits auf `v2.2` aus der
A6-Session vom 2026-08-24 (P7-U) — beide Plan-Zeilen beim Nachlesen bestätigt, nicht blind
übernommen.

**Neues Modul `webui/static/js/spaces.js`** (P7-Q), Bauart wie `dialogs.js`: `initSpaces()`
im selben Muster wie die zehn bestehenden Module, `openSpaceAdminDialog()` (Liste aller
`writable`-Spaces aus `state.spaces`), `selectSpace()` (`GET .../members`, Home-Hinweis,
Mitgliederliste), Hinzufügen (immer Re-Auth wie serverseitig erzwungen, eingefroren-erste-
Fassung-Muster wie `pendingMoveBody`/`pendingShareBody`), Entfernen (kein Re-Auth),
`openRemoveSpaceDialog()` (Klartext-Konsequenz + getippte Bestätigung + Re-Auth, immer). Neue
Dialoge `#space-admin-dialog`/`#space-remove-dialog` als Geschwister von `#share-dialog`;
`app.js` bekommt `initSpaces()` im Bootstrap, beide Dialoge in `anyOverlayOpen()`/Escape,
einen Klick-Handler auf den Menüpunkt und **eine neue Zeile in `init()`**:
`document.getElementById("account-manage-spaces").hidden = !meta.space_admin` — ohne die
wäre der Kill-Switch (P7-R) nur serverseitig scharf gewesen, der Knopf bliebe sichtbar und
jeder Klick liefe in einen `404`.

**Advisor-Fund vor dem Commit, zwei Teile, beide in `spaces.js`:**
1. **Eingefrorener Hinzufügen-Request überlebt einen Space-Wechsel.** `selectSpace()` setzte
   `pendingMemberBody`/die Re-Auth-Felder nicht zurück — ein Re-Auth-Retry nach einem Wechsel
   von Space A zu Space B hätte den für A eingefrorenen Namen gegen B abgeschickt. Exakt der
   Fund, den `dialogs.js :: pendingMoveBody = null` beim Space-Wechsel im Verschieben-Dialog
   bereits kommentiert (`// Ziel geändert -- eine evtl. eingefrorene Fassung ist ungültig`) —
   hier übernommen, plus dieselbe Rücksetzung (inkl. Feldwerte) in `openSpaceAdminDialog()`,
   damit ein getipptes Passwort auch ein Schließen+Wiederöffnen des Dialogs nicht überlebt.
2. **`orphans` gelesen und verworfen.** C2s eigener Commit-Kommentar begründet `orphans`
   explizit als „der Render-Hinweis fürs Frontend" (Tippfehler-Fänger gegen bekannte
   Space-Verzeichnisse) — `selectSpace()` las das Feld nie. Jetzt als eigene Zeile in der
   Mitgliederliste gerendert („verwaist -- kein solcher Space mehr").

**Echter Browser-Lauf, Ende-zu-Ende, gegen eine Wegwerf-Instanz** (eigener Uvicorn-Prozess,
temporäres `DATA_ROOT`+`AuthStore`, `git=False`, Skript im Scratchpad, kein Repo-Teil):
Einladung→Enrollment→Login, Menüpunkt trägt kein `disabled` mehr (bestätigt per DOM-Lesung),
Dialog öffnet, `niklas`-Space zeigt den Home-Hinweis und **keinen** „Space entfernen"-Knopf,
Mitglied `fabian` (schreiben) hinzugefügt — erster Versuch ohne Credentials → `403
reauth_required`, Re-Auth-Formular erscheint, zweiter Versuch mit Passwort+TOTP → `200`,
Mitgliederliste aktualisiert. `fabian` ohne Re-Auth wieder entfernt (Toast bestätigt). Neuer
Space `team-c3-probe` angelegt (erscheint sofort im Baum, `niklas` automatisch als
Schreib-Mitglied gesät — C2s eigener Fund, hier bestätigt). `team-c3-probe` zeigt korrekt
einen „Space entfernen"-Knopf (kein Home-Space); Entfernen-Dialog zeigt den vorgeschriebenen
Konsequenztext, erster Versuch nur mit getipptem Namen → `403 reauth_required` +
„Re-Authentisierung fehlgeschlagen.", zweiter Versuch mit Credentials → `200`, Toast „Space
entfernt · 0 Item(s) archiviert", Space verschwindet aus dem Baum.

**Zwei Harness-Eigenheiten dieser Sitzung, für die nächste Session festgehalten (kein
Code-Fund):**
1. **CSRF bootstrapt sich ausschließlich über die `/ui/login`-POST-Antwort**, nicht über ein
   bloßes Neuladen von `/ui/` — dieselbe P5-H-Eigenheit, die schon für `testnutzer-p7` mehrfach
   dokumentiert wurde (`docs/INDEX.md`, P6.5-12-Fund). Direktes Navigieren zu `/ui/` nach einer
   Einladungs-/Enrollment-Sitzung lässt `sessionStorage['sfx:csrf']` leer — jeder erste
   Schreibversuch scheitert mit „CSRF-Token fehlt oder stimmt nicht", bis ein echter
   `/ui/login`-Roundtrip in DERSELBEN Tab durchlaufen wird.
2. **`get_page_text` kann eine Vor-Navigations-DOM liefern**, wenn es zu schnell nach einem
   Klick aufgerufen wird — dreimal fälschlich als „Login/Hinzufügen ist fehlgeschlagen"
   gelesen, obwohl der Server-Log denselben Request bereits mit `200` beantwortet hatte. Ein
   erneutes `get_page_text` (ggf. nach `wait`) zeigte danach den korrekten, bereits
   erfolgreichen Zustand. Für die zweite Wegwerf-Instanz (Kill-Switch-Probe,
   `space_admin_enabled=False`) führte dieselbe Klick-Unzuverlässigkeit dazu, dass der
   Login-POST dort nie beim Server ankam (kein einziges Mal in mehreren Versuchen) — die
   REST-Ebene wurde stattdessen per `curl` bestätigt (siehe P7-22-Zeile oben), der
   Menü-Ausblendung fehlt deshalb noch der Pixel-Beweis.

**Verifiziert:** +3 neue/geänderte Tests (`test_app_html_has_a_live_manage_spaces_entry` ersetzt
den Stub, `_JS_MODULES` um `"spaces"`, `test_ui_settings_space_admin_enabled_defaults_to_true`
in `test_api.py`). Volle Suite **903 → 904**, real gezählt. Tabu-Diff leer. `node --check` auf
`spaces.js`/`app.js` sauber (kein Ersatz für einen Test, nur eine Syntaxprobe — P5-T lässt JS
weiterhin unit-ungetestet).

**Abnahmestand:** P7-18 ✅ (Route + Knopf-fehlt, beide bestätigt). P7-22 ✅ (Route doppelt
bestätigt, Menü-Ausblendung jetzt pixel-verifiziert — siehe Nachtrag unten). Modul-Status-
Tabelle (Zeile 13) und Abnahmestand-Tabelle oben nachgezogen. `phase6_shares/CLAUDE.md`s
Zeile 16 (der ursprüngliche `space_admin_enabled`-Seam) bekam eine datierte Schließungsnotiz,
der Snapshot selbst bleibt unangetastet.

**Nächster Schritt, konkret:** Step C5 (Betrieb/Doku — `diagnose.sh` Prüfung 12 Textergänzung,
`docs/UPDATE_LOG.md`-Eintrag vor dem nächsten Deploy, P6-X-Gate beachten) und Block B
(Mehrfachauswahl, `phase6_shares/ITEM_MOVE_PLAN.md` §9). Vor dem nächsten Deploy zusätzlich:
`space_admin_enabled`s Default-Wechsel auf `True` bedeutet, dass Fabian den neuen Menüpunkt
ab dem nächsten Release sieht — im Update-Log-Eintrag erwähnen, nicht erst beim Deploy
entdecken lassen (Advisor-Hinweis).

**Nachtrag, 2026-08-25 — P7-22s Menü-Anteil geschlossen (Nikinger-Vorschlag „use my real
chrome browser"), root cause des Browser-Harness-Problems gefunden.**

**Root Cause, nicht nur Symptom:** das ursprüngliche Problem war nie „Login klappt in diesem
Browser nicht" — der allererste automatisierte Klick auf „Weiter" beim Einladungs-Formular
**gelang tatsächlich** (Server-Log: `POST /ui/invite/... 200 OK`). Ein `get_page_text`-Aufruf
direkt danach zeigte aber noch die alte, prä-Navigations-DOM (dieselbe Race-Bedingung, die
bereits im vorigen C3-Nachtrag notiert war) — das las ich fälschlich als Fehlschlag und klickte
ein zweites Mal. Der zweite Klick traf denselben, jetzt schon verbrauchten Einmal-Token
(`POST .../invite/... 404`) und riss die Enrollment mitten in der TOTP-Bestätigung ab, bevor
das Secret gesichert war — die Instanz landete in einem nicht mehr sauber fortsetzbaren
Zwischenzustand. **Kein Bug in `spaces.js`/`app.js`/der Login-Seite — ein Fehler in der
Auswertungsreihenfolge dieser Sitzung**, nicht im getesteten Code.

**Vorgehen mit dem Nikinger, dritte Wegwerf-Instanz (frisches `DATA_ROOT`, neuer
Einladungslink):** Claude Code füllte Formularfelder per Automation, der Nikinger klickte
selbst („Weiter", „Bestätigen", Login-Submit — dieselbe Arbeitsteilung wie bei
`testnutzer-p7`s Enrollment in P7 Step A7: TOTP-Sekret einmalig vom Nikinger vorgelesen, sofort
zur Code-Berechnung verwendet, nie in einer Datei oder einem Commit gelandet). **Danach lief
auch die automatisierte Login-Route** (`niklas`/Passwort/frischer TOTP-Code, Server-Log direkt
geprüft statt `get_page_text` zu vertrauen) — Login, Übersicht, `GET /api/v1/{me,meta,
overview,spaces,items}` alle `200`. Konto-Dialog geöffnet: zeigt ausschließlich „Update-Log
ansehen", **„Spaces verwalten" fehlt vollständig** — `meta.space_admin === false` blendet den
Menüpunkt tatsächlich aus, wie `app.js`s einzeilige Zuweisung es verspricht.

**Ergebnis: P7-22 ✅, beide Hälften.** Kein Code geändert (reine Verifikationssitzung),
Verifiziert-Absatz oben bleibt unverändert gültig (903/904-Zählung betrifft nur den C3-Commit,
nicht diesen Nachtrag). Tabu-Diff nicht relevant (keine Code-Änderung). Beide Wegwerf-Server
sauber beendet (`pkill`, Port frei bestätigt).

**Für die nächste Sitzung, falls dieselbe Klasse Fund nochmal auftritt:** nach einem Klick
IMMER zuerst den Server-Log (oder ein `wait` vor `get_page_text`) prüfen, bevor ein zweiter
Klick riskiert wird — ein zu früh gelesenes `get_page_text` ist nicht dasselbe wie ein
fehlgeschlagener Request.

**Nachtrag, 2026-08-26 — Step C5 (Betrieb/Doku) gebaut, Block C damit vollständig.**

Reiner Doku-/Skript-Text, kein Python-Verhalten geändert (Plan §C5 verlangt genau das: „ein
Satz im Prüfungstext, mehr nicht").

- `phase3_edge/scripts/diagnose.sh` Prüfung 12 (`spacectl.py check --json` gegen `.share.yml`-
  Referenzen): Kommentarblock um einen Satz ergänzt — dieselbe Prüfung deckt jetzt ausdrücklich
  auch die neue menschliche Space-Verwaltungsfläche (C2–C4) ab, ein per „Spaces verwalten"
  angelegter oder entfernter Space hinterlässt dieselben Spuren wie einer über `spacectl.py`.
  Die eigentliche Prüf-Logik/Ausgabetexte (Zeilen 226–244) bleiben unverändert — der Plan
  verlangt nur den einen erklärenden Satz, keine neue Fallunterscheidung.
- `docs/UPDATE_LOG.md`: neuer oberster Eintrag `## 2026-08-26`, zwei Zeilen (neuer Menüpunkt
  „Spaces verwalten"; Re-Auth-Hinweis bei Entfernen/größeren Mitgliederänderungen) — Format
  gegen den Datei-Kopf-Kommentar geprüft (kurze `- `-Zeilen, kein weiches Umbrechen). **Achtung
  für den tatsächlichen Deploy-Tag:** P6-X-Gate verlangt, dass der oberste Eintrag auf den
  Deploy-Tag datiert ist — falls `deploy.sh` nicht noch am 2026-08-26 läuft, muss das Datum
  vor dem Lauf auf den echten Tag nachgezogen werden, sonst bricht das Skript ab.
- Modul-Status-Tabelle (Zeile 14, neu) nachgezogen.

**Verifiziert:** `pytest -q` **904 → 904**, unverändert (keine neue Testdatei, keine geänderte
Assertion — Plan sieht für C5 keinen Test vor). Tabu-Diff leer (nur `diagnose.sh`-Kommentar +
`docs/UPDATE_LOG.md` + dieser Head berührt).

C5 trägt keine eigene Abnahmezeile (P7-1–P7-24 sind alle Zeilen 1–13 zugeordnet) — geprüft per
Grep, kein `P7-N`-Eintrag nennt `diagnose.sh`/`UPDATE_LOG`/„Betrieb". Kein offener Posten dieser
Art zurückgelassen.

**Damit ist Block C (C1–C5) vollständig.** Einzig verbleibender Scope-Punkt dieser Phase:
Block B (Mehrfachauswahl, `phase6_shares/ITEM_MOVE_PLAN.md` §9, Entscheidungen P6-AK–AN) —
kein neuer Endpunkt, kein neues MCP-Tool, Zweirunden-Re-Auth-Logik (P6-AM) wie im Plan-Auszug
oben. Danach Step Z (Abnahme/Deploy/Abschluss).

**Nächster Schritt, konkret:** Block B, `webui/static/js/state.js`/`list.js`/`tree.js`/
`dialogs.js`/`toasts.js`/`app.html` gemäß der Anker-Tabelle oben in `docs/concepts/
phase7_spaces_admin_plan.md` §"Block B".

**Nachtrag, 2026-08-26 — Block B gebaut (Mehrfachauswahl, §9), Phase-7-Scope damit vollständig
außer Step Z.**

**Umsetzung entlang der Plan-Anker (§9.3), sechs Dateien, reiner Frontend-Schnitt (P6-AL):**
`state.js` bekommt `selectedItemIds` (ein `Set`, geteilt wie der Rest von `state`). `list.js`:
`toggleSelected()`/`clearSelection()`/`renderSelectionToolbar()`, Strg+Klick UND Long-Press
(Pointer-Events, nur `pointerType !== "mouse"`, P5-W bleibt Desktop-first — kein eigener
Touch-Testlauf für diesen Zweig) auf jeder `movable`-Zeile, neue `moveSelectedItems(items,
target, credentials, onProgress)` als geteilte Zweirunden-Schleife. `tree.js`: `clearSelection()`
in `activateView()`/`navigateAll()` — dieselbe Exklusivitäts-Disziplin wie `folder`/`filter`
seit Step 7 Commit 1, zusätzlich beim Such-Debounce und beim Chip-„×“ in `list.js` (Suche zählt
laut §9.3 Punkt 1 ausdrücklich als Navigation). `dialogs.js`: `openMoveDialog(itemOrItems)`
normalisiert auf `moveTargetItems` (Array, IMMER — ein Einzel-Move wird zu `[item]`) — **derselbe
Dialog, keine zweite Definition** (P6-AK), Titel/Konsequenztext branchen auf `.length`.
`toasts.js`/`app.css`: `toast()` nimmt jetzt auch ein Array (mit `\n` verbunden), `.toast`
bekommt `white-space: pre-line` für die zweite Zeile der Sammelmeldung. `app.html`: neue
`#list-selection`-Werkzeugleiste unter `#list-chips`, `#move-dialog-title`/`#move-progress`.

**Zwei Advisor-Runden, insgesamt fünf Funde vor dem Commit behoben (keiner davon durch den
Browser-Lauf allein gefunden — beide Runden liefen VOR dem jeweils nächsten Schritt):**
1. **Batch-Ziel war nicht eingefroren** — `runBatchMove()` las `moveSpaceSelectEl.value`/
   `moveFolderSelectEl.value` bei JEDEM Klick neu, auch beim Re-Auth-Retry. Ein Dropdown-Wechsel
   zwischen Runde 1 und Runde 2 hätte die zurückgewiesenen Items an ein ANDERES Ziel geschickt
   als die bereits erfolgreichen — derselbe Fundtyp wie C3s `pendingMemberBody`. Behoben: neues
   `pendingBatchTarget`, eingefroren beim ersten Batch-Submit (dasselbe Muster wie
   `pendingMoveBody` beim Einzel-Move), PLUS `moveSpaceSelectEl.disabled`/`moveFolderSelectEl.
   disabled = true` für die Dauer eines laufenden Batches (zwei unabhängige Riegel für denselben
   Fund, nicht nur einer).
2. **Space-Wechsel-Handler räumte die Batch-Bilanz nicht auf** — nullte `moveBatchReauthItems`,
   ließ `moveBatchSucceeded`/`moveBatchFailed`/`pendingBatchTarget` stehen. In der Praxis durch
   Fix 1 unerreichbar (die Auswahlfelder sind währenddessen gesperrt), trotzdem als
   Defense-in-Depth nachgezogen — kein Verlass allein auf einen HTML-`disabled`, den die
   Accessibility-Probe dieser Sitzung nicht zweifelsfrei bestätigen konnte.
3. **Fehlender `.catch()`** auf der Erfolgs-Kette nach einem Batch (`loadItems().then(loadOverview)
   .then(...)`) — ein `401` mitten im Batch hätte eine unbehandelte Promise-Ablehnung hinterlassen
   (dieselbe Fundklasse wie P5 Step 10, `reportUnexpectedError()`). Behoben, `reportUnexpectedError`
   neu aus `api.js` importiert.
4. **Abgelaufene Sitzung mitten im Batch wäre als benannter Fehlschlag pro Item erschienen** —
   `api.js`s 401-Zweig zeigt die "Sitzung abgelaufen"-Karte bereits synchron; ohne Sonderfall
   hätte `moveSelectedItems()` trotzdem jedes verbleibende Item als `[unauthenticated]`
   gemeldet UND weiter erfolglose Requests abgeschickt. Behoben: `err.message ===
   "unauthenticated"` bricht die Schleife sofort ab, dieselbe Unterdrückung wie im Einzel-Move.
5. *(Kein Fund, gegengeprüft:)* die Konflikt-Fehlermeldung (`api.py :: _map_store_error()` —
   „Konflikt bei {id}: erwartete Version X, aktuell Y.“) liest sich sinnvoll eingebettet in der
   Batch-Sammelmeldung (`„Titel“ [Konflikt bei …]`) — keine Änderung nötig.

**Echter Browser-Lauf, Ende-zu-Ende, gegen eine Wegwerf-Instanz** (eigener Uvicorn-Prozess,
temporäres `DATA_ROOT`+`AuthStore`, `git=False`, Skript im Scratchpad, kein Repo-Teil — Nutzer
per `store.upsert_user()`+`confirm_totp()` direkt bestätigt angelegt, kein Einladungsumweg
nötig, Login selbst lief normal über die UI mit Passwort+echtem TOTP-Code):
- **Zeile 31** (N Items auf einmal): drei Notizen per Strg+Klick ausgewählt (Toolbar zeigte
  korrekt „3 ausgewählt“), Dialogtitel „3 Items verschieben“, Konsequenztext „Verschiebt 3 Items
  nach beta. …“ — alle drei korrekt gerendert.
- **Zeile 33** (ein fehlgeschlagenes Item blockiert die anderen nicht): eines der drei Items
  wurde VOR dem Klick über einen zweiten `Store`-Handle auf eine neue Version gebracht (echter
  Konflikt, nicht simuliert). Ergebnis: die anderen zwei landeten korrekt im Zielspace (Space-
  Zähler beta 1→3), das Konfliktitem blieb unverändert in alpha. **Die tatsächliche
  Sammelmeldung mit dem benannten Fehler wurde dabei NICHT gesehen** — der Dialog schloss sich
  vor dem Screenshot, der Toast war bereits abgelaufen. Nur die Nichtbewegung des Konfliktitems
  ist damit live bewiesen, nicht der Text der zweiten Toast-Zeile selbst.
- **Zeile 32** (ein gemeinsames Re-Auth-Formular für die ganze Auswahl): mit einer frischen
  `.share.yml`-Konstellation (alpha teilt NICHTS mit beta, beta teilt `write` mit alpha — echtes
  Widen, kein durch beidseitige Shares verdecktes No-Op, wie es der erste Durchlauf zeigte) zwei
  Items batch-verschoben: Runde 1 → „2 von 2 benötigen Passwort und Code“, EIN Formular. Ein
  wiederverwendeter TOTP-Code wurde vom Server korrekt als Replay abgelehnt (echtes
  Anti-Replay-Verhalten, kein Fund) — nach einem frischen Code liefen beide Items durch, Toast
  bestätigte, Dialog schloss, beta-Zähler stieg auf 5.
- **Zeile 34** (In-Space-Batch löst nie Re-Auth aus): zwei Items innerhalb von alpha in einen
  neuen Ordner verschoben — Dialog schloss sofort ohne jedes Re-Auth-Formular, beide Items auf
  v2, Ordner im Baum korrekt.
- **Konsole** ohne Fehler während des gesamten Laufs (Muster `error|Error|Uncaught|Unhandled`).

**Ehrlich benannt, nicht verschwiegen:** die zweizeilige Sammelmeldung mit namentlich genannten
Fehlern (§9.3 Punkt 4, Zeile 33s zweite Hälfte) ist NICHT im Browser gesehen — nur ihre
Voraussetzung (das Konfliktitem bleibt unbewegt, taucht nicht fälschlich als erfolgreich auf).
Der fünfte Advisor-Fund oben (Konflikt-Meldungstext) ist eine Code-Prüfung, kein Sichtbeweis.
Der von der Beraterin vorgeschlagene fünfte E2E-Fall (Dropdown-Wechsel zwischen Runde 1 und 2)
wurde NICHT nachgestellt — durch Fund 1 oben ist er strukturell unerreichbar geworden (die
Auswahlfelder sind während eines laufenden Batches gesperrt), nicht übersprungen.

**Abnahmezeilen 31–34 (`ITEM_MOVE_PLAN.md` §9.5, „Wer: Niklas“) bleiben formal offen** —
derselbe Umgang wie P6.5-12 vor dem echten Klick: ein Claude-Code-Browserlauf ist ein
Kandidatenbeleg, keine Abnahme durch den Nikinger selbst. **Gebaut, Claude-Code-Browserlauf
bestanden, Nikinger-Bestätigung steht aus.**

**Verifiziert:** `pytest -q` **904 → 904**, unverändert (P6-AL: reiner Frontend-Schnitt, keine
neue Backend-Testdatei laut Plan §9.4). `node --check` auf `list.js`/`dialogs.js` sauber. Tabu-
Diff: ausschließlich `phase5_ui/webui/static/{app.css,app.html,js/{state,list,dialogs,tree,
toasts}.js}` — `webui/api.py` bewusst NICHT angefasst (P6-AL, kein neuer Endpunkt), stärker als
§9 verlangt. Wegwerf-Server sauber beendet (`pkill`, `DATA_ROOT` gelöscht, Port frei bestätigt).

**Damit ist Block B fertig — Phase 7 ist inhaltlich vollständig (Block A, Gate, Block C, Block
B).** Einzig verbleibend: **Step Z** (Abnahme/Deploy/Abschluss, siehe Plan-Auszug oben) — frischer
`diagnose.sh`-Lauf, `docs/UPDATE_LOG.md`-Datum auf den echten Deploy-Tag geprüft, `pytest -q`/
`mcp_smoke.py`/`ui_smoke.py`/`ui_budget.py --json`, Tabu-Diff, dann `deploy.sh` durch den
Nikinger (braucht Sudo). Danach die Abnahmematrix real durchgehen (inkl. der jetzt offenen
Zeilen 31–34) und die Phase-7-Closeout-Dokumente schreiben.

**Nächster Schritt, konkret:** Step Z — mit dem Nikinger abstimmen, wann `deploy.sh` läuft und
ob das UPDATE_LOG-Datum vom 2026-08-26 noch zum tatsächlichen Deploy-Tag passt.

**Nachtrag, 2026-08-27 — Nikinger-Entscheidung: Deploy auf 2026-08-28.**

`docs/UPDATE_LOG.md`s oberster Block auf `## 2026-08-28` nachgezogen (P6-X-Gate: der Eintrag
muss den tatsächlichen Deploy-Tag tragen, sonst bricht `deploy.sh` ab). Dabei eine dritte Zeile
ergänzt, die bislang fehlte: Block B (Mehrfachauswahl) ist selbst eine sichtbare, menschen-
relevante Änderung (Strg+Klick/Long-Press-Auswahl + Sammel-Verschieben) und gehört damit in
denselben Deploy-Eintrag wie die Space-Verwaltung — beide Features landen im selben Release.
Parser-Probe (`parse_update_log()`) bestätigt alle drei Zeilen unverändert intakt unter
`entries[0]`. Kein Code-Diff sonst, reine Terminplanungs-Reaktion — `pytest`/Tabu-Diff nicht neu
gelaufen (nichts Python-Seitiges berührt).

**Weiterhin offen für den 2026-08-28-Lauf:** frischer `diagnose.sh`, `pytest -q`/`mcp_smoke.py`/
`ui_smoke.py`/`ui_budget.py --json`, Tabu-Diff, dann `deploy.sh` durch den Nikinger.

**Nachtrag, 2026-08-27 — Pre-Deploy-Checks gelaufen** (`pytest -q` 904/904, `mcp_smoke.py`
16/16, `ui_smoke.py` 12/12, `ui_budget.py --json` `all_within_budget: true`, Tabu-Diff über die
letzten 40 Commits leer — alle vier Skripte bauen ihre eigene temporäre Instanz, nie den echten
`DATA_ROOT`, deshalb von Claude Code selbst gefahren; `diagnose.sh` bewusst nicht — liest den
echten `DATA_ROOT`, bleibt Nikinger-Sache).

**Nachtrag, 2026-08-27 — Korrektur des Datumsplans, echter `deploy.sh`-Lauf gescheitert am
falschen Datum, sauber selbst aufgeräumt.** Der Nikinger fuhr `deploy.sh main` noch am selben
Tag (nicht am 28., wie oben angenommen — die „morgen"-Ankündigung eine Nachricht zuvor deckte
sich nicht mit dem tatsächlichen Zeitpunkt des Laufs). `deploy.sh`s eigenes Gate (P6-X) brach
korrekt ab: `docs/UPDATE_LOG.md` trug `## 2026-08-28`, das System-Datum (`date -u`/`date`, beide
gegengeprüft: 2026-08-27 UTC und CEST) erwartete `2026-08-27`. **Kein Fehlverhalten des Skripts
— das Gate hat exakt das getan, wofür es gebaut wurde.** Das unvollständige Release-Verzeichnis
(`/opt/sharefyx/releases/20260827T165500.903807Z`) hat `deploy.sh` bereits selbst entfernt (im
eigenen Log: „entferne unvollständiges Release"), `current` zeigte danach unverändert auf die
letzte gute Release (`20260825T110849.160586Z`) — read-only per `ls`/`readlink` bestätigt, keine
Leiche zurückgeblieben, kein Handgriff nötig. `docs/UPDATE_LOG.md`s oberster Block auf
`## 2026-08-27` korrigiert (Zeileninhalt unverändert, nur das Datum), Parser-Probe erneut grün.

**Nächster Schritt, konkret:** `deploy.sh main` erneut versuchen, mit demselben Env-Var-Satz wie
zuvor — das UPDATE_LOG-Gate sollte jetzt durchlaufen.

**Nachtrag, 2026-08-27 — echter `deploy.sh main`-Lauf durch den Nikinger, erfolgreich.**
**Live-Ergebnis:** `{"action":"deploy","result":"ok","release":"/opt/sharefyx/releases/
20260827T165737.663410Z","sha":"e88a6244d8eebb5d08d1d93c4a2725f84a2f5971","ref":"main",
"previous":"/opt/sharefyx/releases/20260825T110849.160586Z"}`. `pytest -q` im Release **904/904**
(zweiter, unabhängiger Lauf — im gebauten Release-Verzeichnis, nicht nur im Arbeitsbaum),
`/opt/sharefyx/current` zeigt jetzt auf `e88a624`, `sharefyx-mcp` neu gestartet, Health-Gate 3/3
grün (`/ui/login`→200, `/api/v1/me`→401, `/mcp/`→401 — alle drei die per `deploy.sh`-Kommentar
erwarteten Antworten: Stack vollständig gemountet UND Auth-Gate scharf, kein Fehlschlag),
Retention griff (`KEEP=5`, ältestes Release `20260813T115528` entfernt).

**Damit ist Phase 7 live deployt.** Block A/Gate/C/B stehen jetzt real auf der Maschine, nicht
nur im Repo. **Weiterhin offen, unverändert:** A6 (Purge-Gate, frühestens 2026-08-28) und die
volle Abnahmematrix real mit dem Nikinger durchgehen — insbesondere die neuen Zeilen 31–34
(bislang nur Claude-Code-Browserlauf gegen eine Wegwerf-Instanz, keine Nikinger-Abnahme auf der
echten Instanz) und alle Zeilen, die noch Fabians eigenen Login brauchen. **Root-`CLAUDE.md`,
`ROADMAP.md`, `docs/INDEX.md`** im selben Commit nachgezogen (Phase 7 jetzt „inhaltlich
vollständig, live deployt, Step Z läuft" statt „Block A weit fortgeschritten").

**Nächster Schritt, konkret:** mit dem Nikinger die volle Abnahmematrix (Plan §6/§9.5) real
durchgehen, danach `PHASE7_CLOSEOUT_HANDOVER.md` + Übersichtsgrafik + Rotationsprüfung.

**Nachtrag, 2026-08-27 — Abnahmematrix-Walkthrough gegen die echte Live-Instanz
(`e88a624`), Browser-Tool-Modus (Claude Code steuert, Nikinger klickt/tippt Zugangsdaten):**

Sieben Zeilen live geschlossen: **P7-14, P7-15 (beide Hälften), P7-16, P7-17, P7-19, P7-23 ✅.**
Eine neu gefunden, **P7-24 ❌** (echter Mechanismus-Fehler, kein reiner UI-Fund) — siehe
Abnahmestand-Tabelle oben für den vollen Befund und die Fix-Optionen, hier nur der Kern:
`list.js :: moveSelectedItems()` reicht dasselbe `credentials`-Objekt (ein TOTP-Code) an jedes
sequenzielle PATCH im Batch durch; der Server lehnt den wiederverwendeten Code korrekt als
Replay ab, wodurch ein re-auth-pflichtiger Batch mit N>1 Items strukturell mehr als zwei Runden
braucht statt der von P7-24 verlangten „ein Formular, nicht N". Bleibt offen bis der Nikinger
entscheidet, wie behoben wird. **P7-9 weiterhin blockiert** — `token_families`-Purge-Fenster
öffnet erst 2026-08-28, Systemdatum heute ist 2026-08-27, keine Umgehung versucht.

**Zwei operative Pannen dieser Sitzung, für zukünftige Läufe festgehalten:**
1. **Cookie-Kollision zwischen Tabs derselben Session.** `testnutzer-p7`s Login in einem zweiten
   Tab überschrieb das Session-Cookie für den ERSTEN Tab (gleicher Browser-Origin, gemeinsamer
   Cookie-Jar) — `niklas`s Tab zeigte danach `testnutzer-p7` als Home-Space, obwohl die
   rechte Seite noch die alte `niklas`-Übersicht cachte. Merke: ein zweiter Login in einem
   zweiten Tab **derselben** `claude-in-chrome`-Session ist kein isolierter Kontext, er
   invalidiert die erste Sitzung. Für zwei gleichzeitige Logins bräuchte es zwei getrennte
   Chrome-Profile/Inkognito-Fenster, nicht zwei Tabs — hier stattdessen sequenziell gearbeitet
   (Tab 2 nach Gebrauch geschlossen, Tab 1 neu eingeloggt).
2. **Koordinaten-Klicks nach einer Layout-Änderung sind unzuverlässig.** Mehrere `computer
   left_click`-Aufrufe auf feste Pixel-Koordinaten trafen nach einem Viewport-Wechsel
   (1214×545 → 1517×681 zwischen Screenshots) das falsche Feld — Text landete wiederholt im
   Passwortfeld statt im Space-Feld. Behoben durch Umstieg auf `find`+`form_input`/`ref`-Klicks
   (element-basiert statt pixel-basiert) für sicherheitsrelevante Formulare. Für künftige
   Läufe: bei jedem Login-/Formular-Schritt `find` statt gecachter Koordinaten verwenden,
   besonders nach einem Screenshot mit anderer Auflösung als der vorherige.

**Verifiziert:** keine Code-Änderung in diesem Nachtrag (reine Live-Abnahme + Doku). Kein
`pytest`-Lauf nötig. Abnahmestand-Tabelle und dieser Block sind der einzige Diff.

**Nachtrag, 2026-08-27 — P7-12 durchgeführt, `testnutzer-p7` vollständig zurückgebaut.** Exakt
nach dem Plan-Rezept (`docs/concepts/phase7_spaces_admin_plan.md:544-552`): `testcred.py purge`
(Claude Code, reiner Keyring-Vorgang, kein `DATA_ROOT`-Zugriff) zuerst, danach die drei
`DATA_ROOT`/Auth-DB-Schreibvorgänge durch den Nikinger selbst (`spacectl.py remove-space
testnutzer-p7 --force`, `authctl.py disable-user`/`revoke-sessions --space testnutzer-p7`) —
bewusst nicht von Claude Code ausgeführt, dieselbe Kategorie destruktiver Direktzugriff ohne
interaktives Re-Auth-Gate wie `deploy.sh`. `SPACE_AUTH_DB` war die nächste bekannte Lücke aus
A7 (systemd setzt `STATE_DIRECTORY`, eine interaktive Shell nicht) — diesmal mit dem echten
Pfad (`/var/lib/sharefyx/auth.sqlite3`, per `ls`-Zeitstempel als aktiv bestätigt) sofort gelöst,
keine neue Verzögerung. `spacectl.py check --json` bestätigt `orphan_count:0`/`broken_count:0` —
keine verwaisten `.share.yml`-Referenzen zurückgeblieben. Damit ist der dritte Test-Principal
dieser Phase vollständig entsorgt; jede künftige Phase, die einen dritten Nutzer braucht, legt
sich einen neuen an (Nikinger-Entscheidung dieser Sitzung, kein Wiederverwenden von
`testnutzer-p7`).

**Ehrliche Antwort auf die Nikinger-Frage „sind alle Tests fertig, ist Phase 7 damit vorbei?":
Nein, noch nicht — aber nur noch zwei Punkte, nicht drei (Korrektur unten).**
1. **P7-24 ❌** — der TOTP-Batch-Mechanismus-Fund oben. **Nikinger-Entscheidung, 2026-08-27:
   wird als echter Defekt anerkannt, Fix erst in der nächsten Phase.** Bleibt ❌ in der
   Abnahmestand-Tabelle stehen (kein stilles Weglassen, kein Umdeuten in ein akzeptiertes
   Restrisiko) — nur der Zeitpunkt der Behebung ist geklärt, nicht der Befund selbst.
2. **P7-9 ⬜** — `token_families`-Purge-Fenster öffnet erst 2026-08-28 (morgen), `clients` erst
   2026-10-27. **Nikinger-Entscheidung: bis morgen warten**, kein Umgehungsversuch.

**Korrektur, noch in dieser Sitzung: P6-Zeilen 36/37 fälschlich als offen geführt.** Der
Nikinger fragte direkt nach, ob `testnutzer-p7`s Test gleichwertig zu einem Fabian-Test ist —
Antwort: **mehr als gleichwertig, es ist der einzig mögliche Weg.** Der Plan selbst
(`docs/concepts/phase7_spaces_admin_plan.md:540`) begründet genau das: mit Fabian ist der Fall
„nur item-level Share, kein Space-Grant" **strukturell unerreichbar** — `niklas` steht bereits
in `fabian/.share.yml` unter `read:`, Fabian sieht als Empfänger also ohnehin alles über den
Space-Grant, ein item-level-only-Szenario lässt sich mit ihm gar nicht bauen. `testnutzer-p7`
hat **keinen** space-level Grant — deshalb wurde er für genau diesen Fall angelegt (P7-J). Die
Zeile P7-11 in der Abnahmestand-Tabelle oben (bereits ✅, Web-UI **und** MCP) trägt das als
Beleg schon direkt in ihrem eigenen Text: „Web-UI (**P6-Zeilen 36/37**, echter Login)". **P6-36/37
sind damit bereits geschlossen, nicht offen** — mein eigener Nachtrag oben (Punkt 3, „brauchen
Fabians eigenen Login") war falsch, hier korrigiert. `phase6_shares/CLAUDE.md` trägt an dieser
Stelle noch den alten Stand („36/37 brauchen Fabian") — das ist der zugehörige Doku-Fund für die
nächste Sitzung, nicht mehr Teil des Abnahme-Fortschritts dieser hier.

Alles andere in der Abnahmestand-Tabelle steht jetzt ✅. **Phase 7 ist damit sehr nah, aber
nicht formal abschließbar** — der Root-`CLAUDE.md`/`ROADMAP.md`/`docs/INDEX.md`-Sprung auf
„Phase 7 ✅" und `PHASE7_CLOSEOUT_HANDOVER.md`/Übersichtsgrafik/Rotationsprüfung bleiben
bewusst der nächsten Sitzung, sobald P7-9 (frühestens morgen) geprüft ist. P7-24 bleibt als
bekannter, akzeptierter Defekt in der nächsten Phase offen — das blockiert den Phase-7-Abschluss
selbst nicht mehr, muss aber im Closeout-Handover als offene Entscheidung an die nächste Phase
weitergereicht werden, nicht stillschweigend verschwinden.

**Nächster Schritt, konkret:** neue Sitzung ab 2026-08-28 — zuerst P7-9 (`clients`/
`token_families`-Rückgang nachprüfen), P7-24-Entscheidung einholen, dann erst der formale
Phase-7-Abschluss samt Closeout-Dokumenten.

**Nachtrag, 2026-08-27 (spät) — Live-Incident: `GET /api/v1/overview` → 500 auf jedem Gerät,
Ursache und Sofort-Fix.** Nikinger meldete den Fehler von einem neuen Gerät aus (DevTools-
Screenshot, `500` auf `/api/v1/overview`). `journalctl -u sharefyx-mcp` zeigte den echten
Traceback: `FileNotFoundError` in `storage/store.py :: _row_to_item()` für
`/home/savefyx/savefyx-data/testnutzer-p7/_archive/itm_26f8d0b7__p6-5-12-retest-2026-08-25.md`.

**Root Cause, kein Geräte-/Browser-Problem:** `spacectl.py :: _cmd_remove_space()`
(`phase6_shares/scripts/spacectl.py:170-195`) löscht mit `acl.remove_space_dir()` nur das
Verzeichnis auf der Platte — der SQLite-Index wird dabei **nie** angefasst. Der frühere P7-12-
Lauf dieser Sitzung (`spacectl.py remove-space testnutzer-p7 --force`, vom Nikinger ausgeführt)
hat damit einen index-only-Karteileichen-Zustand hinterlassen: Zeilen für `testnutzer-p7`s
Items standen weiter in der SQLite-Datenbank, obwohl die Dateien weg waren. Jede Anfrage, die
diese Zeilen berührt (`/api/v1/overview` iteriert `store.search()` über alle Buckets), krachte
mit dem `FileNotFoundError` — reproduzierbar für **jeden** eingeloggten Nutzer, nicht
gerätespezifisch (Screenshot zeigte Firefox/Windows, ein bislang ungenutztes Gerät — reiner
Zufall, dass es dort zuerst auffiel).

**Sofort-Fix, noch in dieser Sitzung, durch Hard Rule 2 vorab autorisiert** („SQLite darf
jederzeit gelöscht und aus den `.md`-Dateien vollständig rekonstruiert werden"): `space_cli.py
--data-root /home/savefyx/savefyx-data reindex --json` → `{"items_indexed": 78,
"duration_seconds": 0.044}`. `Store.rebuild_index()` nimmt denselben `.write.lock`-Flock wie der
laufende Dienst (P7-M) — sicher gegen die Live-Instanz gefahren, kein Neustart nötig. Danach
`journalctl --since "2 minutes ago"` grep nach `error|traceback` → leer, `curl .../api/v1/me` →
weiterhin `401` (Dienst gesund). **Vom Nikinger noch nicht gegengeprüft** (kein erneuter
Login-Versuch im selben Gespräch) — bitte auf dem betroffenen Gerät erneut `/ui/` laden und
bestätigen.

**Echter Fund, nicht nur ein einmaliger Vorfall — `spacectl.py remove-space` braucht einen
Nachlauf-Reindex oder zumindest einen Warnhinweis.** Jeder künftige `remove-space --force`-Lauf
reproduziert dieselbe Karteileiche für die entfernten Items, bis jemand von Hand reindiziert.
**Nikinger-Entscheidung noch offen:** `_cmd_remove_space()` um einen automatischen
`store.rebuild_index()`-Aufruf erweitern (ein Zweizeiler, gleiche Datei) oder nur die
Warnmeldung ergänzen („führe danach `reindex` aus")? Bleibt für die nächste Sitzung — nicht
mehr Teil des heutigen P7-12-Laufs, aber eine direkte Konsequenz davon, hier festgehalten statt
verloren zu gehen.

**Verifiziert:** keine Testsuite gelaufen (reine Betriebs-Wiederherstellung, kein Code-Diff in
diesem Nachtrag — der `spacectl.py`-Fix selbst ist noch nicht gebaut). Tabu-Diff nicht relevant.

**Nächster Schritt, konkret, VOR allem anderen in der nächsten Sitzung:** Nikinger bestätigt,
dass `/ui/` wieder lädt. Danach `spacectl.py remove-space`s fehlenden Reindex beheben (kleiner,
in-scope Fix, keine neue Planungsrunde nötig) — erst danach weiter mit P7-9/P7-24/Closeout.

**Nachtrag, 2026-08-28 — Abnahmezeilen 31–34 (`ITEM_MOVE_PLAN.md` §9.5) vom Nikinger selbst live
gegen die echte Instanz bestätigt.** Damit ist die in Zeile 874 oben und im Session-Block vom
2026-08-25 genannte Lücke „Gebaut, Claude-Code-Browserlauf bestanden, Nikinger-Bestätigung steht
aus" geschlossen — dies ist die Nikinger-Abnahme selbst, kein weiterer Kandidatenbeleg. Ergebnis,
Zeile für Zeile:

- **Zeile 31** (N Items in einem Vorgang, ein `move`-Commit je Item) — ✅ **mit demselben bereits
  bekannten Vorbehalt wie P7-24**: die Items landeten korrekt im Ziel, aber die Auswahl enthielt
  rechteerweiternde Items, und der Nikinger musste dafür N verschiedene TOTP-Codes eintippen
  statt einem. **Kein neuer Fund** — deckungsgleich mit dem bereits im Abnahmestand oben
  protokollierten P7-24-Mechanismus-Fehler (`list.js :: moveSelectedItems()` reicht denselben
  TOTP-Code an jedes sequenzielle PATCH durch, Server lehnt den Replay korrekt ab). Bereits als
  echter, in die nächste Phase verschobener Defekt anerkannt (Nikinger-Entscheidung 2026-08-27,
  siehe oben) — diese Probe bestätigt nur, dass Zeile 31 denselben Mechanismus trifft, öffnet
  keine neue Entscheidung.
- **Zeile 32** (genau ein rechteerweiterndes Item → ein Formular) — ✅ live bestanden.
- **Zeile 33** (ein fehlgeschlagenes Item blockiert die anderen nicht) — ✅ live bestanden.
- **Zeile 34** (reine In-Space-Auswahl löst nie Re-Auth aus) — ✅ live bestanden.

**Damit ist die Nikinger-Abnahme für Block B (Mehrfachauswahl) vollständig**, mit demselben
einen offenen Punkt, der bereits vor dieser Probe bekannt und entschieden war (P7-24, Fix in der
nächsten Phase). Kein neuer Code-Diff, keine neue Testsuite nötig — reine Abnahme-Dokumentation.
`docs/INDEX.md`, `ROADMAP.md`, Root-`CLAUDE.md` im selben Commit nachgezogen.

**Verbleibend für Step Z / Phase-7-Abschluss:** A6 (Purge-Gate, ab heute 2026-08-28 kalendarisch
möglich, `token_families`), danach `PHASE7_CLOSEOUT_HANDOVER.md` + Übersichtsgrafik +
Rotationsprüfung.

**Nachtrag, 2026-08-28 — A6 gefahren, P7-9 geschlossen.** Baseline (read-only, `sqlite3` gegen
`/var/lib/sharefyx/auth.sqlite3`): `clients: 54`, `token_families: 35`, unverändert seit
2026-08-24. Oldest-`token_families`-Zeile `2026-07-29T15:02:27Z` — 30-Tage-Fenster lief um
17:02 CEST heute ab. Nikinger fuhr `sudo systemctl start sharefyx-purge.service` selbst (Live-
Dienst-Restart bleibt Nikinger-Sache, keine passwortlose `sudo` für Claude Code bestätigt).
`journalctl -u sharefyx-purge.service`: `{'access_tokens': 7, 'token_families': 4, 'clients': 0,
...}` — read-only Gegenprobe bestätigt `token_families` 35→31, `clients` unverändert 54 (90-Tage-
Fenster öffnet erst 2026-10-27, kein Fund, erwartetes Verhalten). **A6/P7-9 damit erfüllt.**

**Damit ist Phase 7 vollständig abgenommen — kein offener Test, kein offenes Gate mehr.** Einzig
verbleibend: **Step Z Rest** — `PHASE7_CLOSEOUT_HANDOVER.md`, Übersichtsgrafik, Rotationsprüfung,
danach Root-`CLAUDE.md`/`ROADMAP.md`/`docs/INDEX.md` auf Phase 7 ✅ heben. **Nikinger-Entscheidung:
das ist die nächste Sitzung.**
