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
updated: 2026-08-28 (Step Z Closeout -- Phase 7 formal abgeschlossen ✅ auf Nikinger-Entscheidung (22 von 24 Zeilen, 2 benannte Defekte an P8 vererbt), PHASE7_CLOSEOUT_HANDOVER.md + Uebersichtsgrafik neu, zweite Rotation dieses Heads (110KB->35KB), sechste und siebte P1-Contract-Oeffnung geschlossen) | 2026-08-28 (A6/P7-9 gefahren -- token_families 35->31, clients unveraendert 54 wie erwartet, Phase 7 vollstaendig abgenommen, nur noch Step-Z-Closeout-Dokumente offen) | 2026-08-28 (Abnahmezeilen 31-34 vom Nikinger live gegen die echte Instanz bestaetigt -- 32/33/34 ohne Vorbehalt, 31 mit demselben bereits bekannten P7-24-TOTP-Vorbehalt, kein neuer Fund) | 2026-08-25 (Step C3 gebaut -- Space-Verwaltung UI, spaces.js neu, echter Browser-Lauf gegen eine Wegwerf-Instanz Ende-zu-Ende bestanden, zwei Advisor-Funde vor dem Commit behoben, 904 Tests gruen) | 2026-08-25 (Step C4 Nachtrag -- Nikinger-Entscheidung: siebte Contract-Oeffnung statt archived_blockers-Riegel, storage/store.py :: move() erlaubt Space-Wechsel fuer archivierte Items, create(status=archived) faengt jetzt denselben Fall ab, 903 Tests gruen) | 2026-08-25 (Step C4 gebaut -- zweiphasiger Space-Entfernen-Algorithmus, Advisor-Fund: bereits archivierte Items brauchen einen eigenen Vorlauf-Riegel, P7-20/P7-21/Testanteil-P7-22 geschlossen) | 2026-08-25 (Gate A->C geprueft, alle vier Punkte live -- Block C gestartet, Step C1: Schreibseite von .share.yml in storage/acl.py, sechste Contract-Oeffnung gebaut) | 2026-08-25 (P7-4 erster echter Befund: FAIL, ID statt Titel genannt; P7-12-Abbau geprueft und bewusst NICHT gefahren -- Block C/P7-14 braucht testnutzer-p7 noch) | 2026-08-25 (P7-1/P7-2/P7-7 per echtem Browser-Klick bestanden, git-Reparatur nach Nikinger-Freigabe, nur noch P7-4/P7-9/P7-12 offen) | 2026-08-25 (P6.5-12/P7-5 per echtem Browser-Klick bestanden, testnutzer-p7-Substitution, 13/14 in Phase 6.5) | 2026-08-25 (echter deploy.sh-Lauf durch den Nikinger, Live-Release jetzt 53bad20 statt f96125e, A3s asset-strip live, P6.5-12 wieder testbar) | 2026-08-23 (A8: Phase 6.5 formal abgeschlossen als 🟡, 12/14, P6.5-8/13 via testnutzer-p7-Substitution, PHASE6_5_CLOSEOUT_HANDOVER.md + Uebersichtsgrafik neu, P1-Contract-Absatz aktualisiert) | 2026-08-23 (Step 0 gestartet, Doku-Audit gefahren, Skelett angelegt)
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

| 16 | Step Z (Abschluss, kein Code): `docs/concepts/PHASE7_CLOSEOUT_HANDOVER.md` (neu) + `phase7_spaces_admin_uebersicht.svg` (neu, 1080×1080, zweimal gerendert und per `Read` visuell geprüft), Rotation dieses Heads, sechste **und** siebte P1-Contract-Öffnung datiert geschlossen (`phase1_storage/CLAUDE.md`), `ROADMAP.md`/Root-`CLAUDE.md`/`docs/INDEX.md` auf **Phase 7 ✅** | Z | ✅ **vollständig** | 0 (reine Doku-/Grafik-Arbeit); `pytest` unverändert 904 |

*(Die Tabelle ist mit Step Z abgeschlossen — Phase 7 nimmt keine weiteren Zeilen auf.)*

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
„gebaut".** **[2026-08-28 Korrektur, Step Z]** Der Satz „Alle Zeilen ⬜ noch nicht angefangen"
stand hier seit dem Phasenstart und war seit dem 2026-08-25 falsch. **Endstand: 22 ✅ · 2 ❌ · 0
ungeprüft** — die Matrix ist vollständig durchgelaufen, die beiden ❌ (P7-4, P7-24) sind benannte,
an Phase 8 vererbte Defekte, siehe `docs/concepts/PHASE7_CLOSEOUT_HANDOVER.md` §4.

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

## Session stopped — 2026-08-28 (Step Z: Closeout — Handover, Übersichtsgrafik, Rotation, Phase 7 auf ✅)

**Auftrag:** Rückblick-Sitzung, ausdrücklich kein Bauauftrag. Vollständig gelesen statt
minimal-gelesen: dieser Phase-Head ganz, `SESSIONS_ARCHIVE.md` ganz, der Plan (§0–§10 inkl.
`[VERIFY]`-Register und geerbtem Ledger), `ROADMAP.md`s P7-Abschnitt, `docs/INDEX.md`. Ein
Abnahmeprotokoll existiert bewusst nicht (**P7-V** — der Zeilenstatus lebt im Abnahmestand oben).

**Glyph-Entscheidung, dem Nikinger vorgelegt statt selbst getroffen.** Der Präzedenzfall des
Projekts ist eindeutig: jede bisher ✅ gesetzte Phase hatte **100 %** ihrer Abnahmezeilen (P3
13/13, P4 16/16, P5 20/20), jede 🟡 hatte das nicht (P6 12/39, P6.5 13/14). P7 steht bei **22/24
mit zwei live geprüften ❌** — kein Präzedenzfall deckt das ab. Drei Optionen vorgelegt (✅ mit
vererbten Defekten · 🟡 bis P7-24 gefixt ist · ✅ mit Fußnote im Glyph-Text). **Nikinger-
Entscheidung: ✅, Defekte vererbt weitergeben.** Tragende Unterscheidung gegenüber P6: dort waren
27 Zeilen **nie geprüft**, hier ist die Matrix **ganz gelaufen** und hat zwei Defekte
zurückgemeldet — geprüft-und-durchgefallen ist eine andere Kategorie als ungeprüft. Bedingung der
Entscheidung: die beiden ❌ verschwinden nicht, sie stehen als benannte Erbstücke im Handover.

**`docs/concepts/PHASE7_CLOSEOUT_HANDOVER.md` (neu).** Aufbau wie der 6.5er: Status in fünf
Sätzen, Delta seit dem P6.5-Handover (Tabelle, Verweise statt Wiederholung), Abnahmebilanz mit
den drei erläuterungsbedürftigen Zeilen (P7-20s Vorbehalt, P7-9s Kalenderfenster, das geerbte
Nicht-Adressierte), offene Entscheidungen für P8, `[VERIFY]`-Bilanz V71–V80, P1-Contract,
**neu gegenüber allen Vorgänger-Handovers: ein Abschnitt zur geänderten Arbeitsweise** (Opus
plant, opencode/M3 führt aus). Die drei Kopfpunkte für P8 in dieser Reihenfolge: **P7-24**
(TOTP-Replay im Batch), **`spacectl.py remove-space` reindiziert nicht** (der Live-Incident vom
2026-08-27 — Datenintegrität, rangiert bewusst vor dem UX-Befund), **P7-4**.

**`docs/concepts/phase7_spaces_admin_uebersicht.svg` (neu, 1080×1080).** Stilfortschreibung der
6.5er-Grafik (Kopfleiste mit Status-Badge, Mission-Box, farbcodierte Pfeile, DejaVu-Sans-Stack).
Inhaltliches Rückgrat: die Blockfolge 0 → A → Gate → C → B, der zweiphasige Space-Entfernen-
Mechanismus (roter Pfeil „ein Hindernis → es wird nichts bewegt", grüner Pfeil „jedes Item ins
`_archive/`, dann `rmtree`"), der `testnutzer-p7`-Lebenszyklus, und eine rot umrandete
„Was Phase 8 erbt"-Box. **Zweimal gerendert und per `Read` visuell gegengeprüft** — der erste Lauf
zeigte einen echten Fehler (Titel bei 25 px lief unter das Status-Badge, Untertitel ebenso),
behoben durch 21 px/12,5 px; der zweite Lauf ist überlaufsfrei.

**Zwei Doku-Funde dieser Sitzung, beide im selben Commit behoben:**
1. **Der Abnahmestand-Vorspann behauptete seit dem Phasenstart „Alle Zeilen ⬜ noch nicht
   angefangen"** — seit dem 2026-08-25 falsch, überlebt durch fünfzehn Nachträge, weil jeder
   Nachtrag die Tabelle pflegte und nie den Satz darüber. Ersetzt durch den gemessenen Endstand.
2. **Der Plan widerspricht sich beim `[VERIFY]`-Nummernkreis:** die Frontmatter nennt „V71–V79",
   das Register in §7 desselben Dokuments führt **V80** (Keyring-Zugriff für `testcred.py`)
   zusätzlich. Der 📕-Snapshot bleibt unverändert; die Korrektur steht im Handover §5.

**P1-Contract, beide Öffnungen dieser Phase geschlossen** (`phase1_storage/CLAUDE.md`, datiert):
die **sechste** (`acl.py`-Schreibseite) und die **siebte** (`store.move()` für archivierte Items).
Anders als beim 6.5er-Handover wird **keine** neue Öffnung weitergereicht — für P8 gilt: jede
Arbeit an `storage/` braucht eine neue, benannte Öffnung.

**Rotation.** Der Head trug bis zu diesem Block genau einen `## Session stopped`-Block (2026-08-24,
über fünfzehn Nachträge auf ~980 Zeilen gewachsen) — `rotate_session_block.sh` hätte davor
erwartungsgemäß mit `exit 2` „bereits konform" abgebrochen, wie am 2026-08-25 schon einmal
festgestellt. Erst das Anlegen **dieses** Blocks macht die Rotation überhaupt möglich; danach
gefahren, alle drei skripteigenen Byte-Prüfungen (verlustfreier Schnitt, Block im Archiv
byte-identisch, Archivbestand unverändert) grün.

**Verifiziert:** `pytest -q` **904 passed**, unverändert — diese Sitzung hat keine Zeile Python
angefasst (Diff ausschließlich `.md` und die neue `.svg`). Tabu-Diff nicht relevant.

**Phase 7 ist damit formal abgeschlossen: ✅ live-verifiziert.**

**Nächster Schritt, konkret:** Planung von Phase 8 im Browser-Chat. Einstiegsdokument ist
`docs/concepts/PHASE7_CLOSEOUT_HANDOVER.md`, nicht dieser Head. Die drei Punkte, die dort als
erstes eine Entscheidung brauchen, stehen in §4.1–§4.3; die geänderte Arbeitsweise (Ausführung in
opencode) in §7.
