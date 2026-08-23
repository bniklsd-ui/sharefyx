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
| 1 | Haushalt, Verifikationsdurchlauf (0.1–0.5), Skelett (0.6), sechste Contract-Öffnung angekündigt (0.7) | 0 | 🔄 **läuft** — 0.1–0.6 diese Session, siehe Session-Block | 0 (Skelett, wie P1/P6/6.5 Step 0) |

*(Weitere Zeilen entstehen mit Block A/C/B — siehe Plan §4 für die vollständige Schritt-Sequenz.)*

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
| P7-1 | Item-ID sichtbar + Klick kopiert | Niklas | ⬜ |
| P7-2 | ID-Suche findet Item spaceübergreifend | Niklas | ⬜ |
| P7-3 | ID-Suche auf nicht lesbares Item → leere Liste | Claude Code, Test | ⬜ |
| P7-4 | Claude nennt Items beim Titel, nicht der ID | Niklas, echter Connector | ⬜ |
| P7-5 | Bild im Editor entfernbar, landet in `_trash/` | Niklas | ⬜ |
| P7-6 | `PATCH` mit Tippfehler-Feld abgewiesen (O6) | Claude Code, Test | ⬜ |
| P7-7 | Speichern/Verschieben/Freigeben nach Whitelist unverändert | Niklas | ⬜ |
| P7-8 | Migration: 0 `.md` ohne `visibility:` | Nikinger + Claude Code | ⬜ |
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
