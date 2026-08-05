---
status: live
purpose: Phase-Head Web-UI, REST-API, Auth-Selbstverwaltung — Scope, harte Regeln, Modulstatus, aktueller Session-Handover
read-when: Arbeiten in phase5_ui/ oder an den in P5-B genannten Dateien in authserver/mcpserver — zuerst lesen, zusammen mit dem neuesten Session-stopped-Block
detail: L2
up: ../CLAUDE.md
down:
  - ../docs/concepts/phase5_ui_plan.md             # voller Plan, Entscheidungen P5-A–P5-AE, Steps 0–9
  - ../docs/concepts/PHASE4_CLOSEOUT_HANDOVER.md   # Herkunft der offenen Entscheidungen §4.1–§4.5, [VERIFY]-Bilanz V14–V26
updated: 2026-08-05
---

# CLAUDE.md — Phase 5: Web-UI, REST-API, Auth-Selbstverwaltung (`phase5_ui/`)

> **Menschen benutzen das System ohne SSH und ohne Editor.** Zwei getrennt beweisbare Dinge:
> ein Mensch kann sein Konto selbst verwalten (Einladung, Passwort/TOTP/Recovery, ohne Neustart),
> und ein Mensch kann Notizen/Aufgaben im Browser lesen und schreiben, über eine REST-API auf
> demselben Storage-Kern wie die sechs MCP-Tools.
> **Quelle der Wahrheit ist der Code, nicht dieses Dokument.**
> Vollständiges Design + alle 30 gelockten Entscheidungen (P5-A–P5-AE) + Steps 0–9:
> `../docs/concepts/phase5_ui_plan.md`.

## Mission (zuerst lesen)

Der Härtetest der Phase ist nicht die Oberfläche, sondern **Block A vor Block B**: ein System,
in dem ein Mensch sein Passwort selbst setzen kann, ist auch ohne schöne Oberfläche ein
Werkzeug. Eine schöne Oberfläche auf einem Konto, das nur per SSH existiert, ist es nicht. Unter
Druck fällt Block B (REST-API/UI) weg, nicht Block A (Sicherheit/Selbstverwaltung) — dieselbe
Roadmap-Regel („die späteste Phase fällt weg, nie eine frühere Regel") eine Ebene tiefer.

## Bauprinzip (Projekt-Kernprinzip)

„Der Server ist dumm." **Phase 5 enthält KEINE AI**, kein serverseitiges Rendern fremder Bodies
zu HTML (P5-Y), kein LLM, keine Zusammenfassung, kein Auto-Tagging.

## Scope (Kurzform, Details: Plan §0.5 P5-A–P5-AE)

- **DRIN:** Sicherheitsbefunde S2–S8 vollständig schließen (P5-S), Auth-Datenmodell in
  `auth.sqlite3` (Schema 2: `users`/`invites`/`recovery_codes`/`ui_sessions`), eigene
  Cookie-Session für die UI (kein OAuth, P5-D), REST-API `/api/v1/*` über denselben Storage-Kern,
  statische Single-File-UI unter `/ui` (kein Build-Step, P5-T), Deploy/Rollback/Staging/
  Auth-Backup (P5-AB/P5-R).
- **DRAUSSEN:** zweites Dateiformat/Anhänge (Seam ja, Implementierung nein, P5-Z/P5-AA),
  FastMCP-4-Umstieg/CIMD/DPoP (P5-C), Mobilversion (P5-W), Realtime/WebSocket, Löschen (bleibt
  `status: archived`), Rechte zwischen Spaces jenseits von Rule 4.

## Harte Regeln dieser Phase (nicht verhandelbar)

- Alle Hard Rules aus Root-`CLAUDE.md` gelten unverändert.
- **P5-B — Berührungsfläche.** P5 darf `authserver/` und `mcpserver/{app,asgi}.py` anfassen.
  **Tabu:** `storage/`, `mcpserver/tools.py`, `mcpserver/permissions.py`, `mcpserver/server.py`
  — `git diff` darauf ist am Phasenende leer (Akzeptanzkriterium 18). `webui` darf genau **ein**
  Symbol aus `mcpserver` importieren (`permissions.OwnSpaceWritable`), sonst nichts — ein Test
  hält das fest (`test_webui_imports_exactly_one_mcpserver_symbol`).
- **P5-D/P5-F — zwei getrennte Auth-Wege, architektonisch, nicht per `if`.** `/mcp` akzeptiert
  niemals Cookies (nur `Authorization: Bearer`). `/api`/`/ui` akzeptieren niemals Bearer-Token
  (nur Cookie-Session). Beide Richtungen sind Tests (Akzeptanzkriterium 19).
- **P5-G — UI-Session ≠ OAuth-Consent.** `/oauth/authorize` liest niemals Cookies und verlangt
  bei jeder Connector-Autorisierung Passwort **und** TOTP, auch bei bestehender UI-Sitzung.
- **P5-Y — fremde Bodies werden nie serverseitig zu HTML gerendert.** Die API liefert reinen
  Text; Rendering + Sanitizing passiert ausschließlich im Browser.
- **Rotationsregel ab Tag 1.** Dieser Head trägt **genau einen** Session-Block. Beim Anlegen
  eines neuen wandert der bisherige **verbatim** nach `SESSIONS_ARCHIVE.md` — Durchführung über
  `scripts/rotate_session_block.sh phase5_ui`, nie von Hand.
- **Commit ⇒ Note-Update, im selben Commit** (Hard Rule 8): Modul-Tabelle unten + Session-Block.

## Die gelockten Entscheidungen (P5-A – P5-AE) — Kurzform (Details: Plan §0.5)

Ein Phasenschnitt, zwei Blöcke, harter Gate dazwischen (A) · Berührungsfläche `authserver`/
`mcpserver/{app,asgi}` (B) · MCP-Revision 2026-07-28 bleibt eigene Mini-Phase (C) · eigene
Cookie-Session, kein OAuth für die UI (D) · `__Host-sfx_session`, Idle 12h/Absolut 7d (E) ·
`/mcp` nie Cookies, `/api`+`/ui` nie Bearer (F) · UI-Session kürzt Consent nicht ab (G) ·
Double-Submit-CSRF + Herkunftsprüfung (H) · Nutzerakten wandern in `auth.sqlite3` (I) ·
TOTP-Seeds AES-256-GCM verschlüsselt, drittes Credential `auth-dek` (J) · Einladungstoken/
Recovery-Codes/Session-IDs gehasht, nicht Argon2id (K) · `UserDirectory` liest live, kein
Neustart mehr nötig — schließt O1 (L) · Erstvergabe über Einmal-Einladung (M) · zehn
Recovery-Codes ersetzen den TOTP-Faktor (N) · Passwortpolitik 12–128 Zeichen + lokale Blocklist
(O) · Re-Auth bei sicherheitsrelevanten Änderungen (P) · Passwortwechsel widerruft alle
Token-Familien + fremde UI-Sessions (Q) · eigenes verschlüsseltes Auth-Backup (R) · S2–S8
vollständig schließen (S) · statische Single-File-UI, kein Build (T) · Markdown-Textarea +
Formatierhilfen, kein WYSIWYG (U) · Notizheft-Neubau mit Ernte (V) · 16:9-Desktop first, keine
Mobilversion (W) · Dunkel-first, Apple-Formensprache vor „Liquid Glass" (X) · fremde Bodies nie
serverseitig gerendert (Y) · Format-Seam ohne Implementierung (Z) · Anhänge draußen (AA) ·
Release-Verzeichnisse + Health-Gate + Staging, kein Blue/Green (AB) · Blue/Green als Seam (AC) ·
Messung statt Schätzung (`ui_budget.py`, AD) · gemeinsame Live-Abnahme, beide Nutzer (AE).

## Modul-Status

| # | Modul | Step | Status | Tests |
|---|---|---|---|---|
| 1 | Haushalt, Verifikationsdurchlauf, Rückbau P2-Token-Reste, Doku-Drift, P3-Restore-Nachweis | 0 | ✅ **vollständig** — A.7 vom Nikinger live ausgeführt, P3 Zeile 13 vom Nikinger bestätigt (13/13, Phase 3 ✅) | −14 (Rückbau, kein neuer Feature-Code) |
| 2 | Sicherheitsbefunde S2–S8 vollständig geschlossen (`authserver/{resolver,flows,store,ratelimit,routes}.py`, `phase3_edge/scripts/install_units.sh`, `phase5_ui/systemd/sharefyx-purge.{service,timer}`) | 1 | ✅ **vollständig** — 7/7 Befunde geschlossen, Meta-Test bestätigt keine offene Zeile mehr | +20 (2 `test_authserver_store.py` + 4 `test_resolver.py` + 2 `test_routes.py` + 3 `test_flows.py` + 2 `test_ratelimit.py` + 5 `test_units.py` + 2 `test_security_review_register.py`, neue Datei) |
| 3 | Auth-Datenmodell: Schema 2, `secretbox.py`, `userdir.py`, `flows.py`/`app.py`/`serve.py` auf `UserDirectory` umgestellt, `import_users_to_db.py` | 2 | ✅ **vollständig** — schließt O1 strukturell (kein Cache mehr) und die S7/S6-Restarbeit aus Step 1 (`ui_sessions`/`invites`-Purge, `UserDirectory.get()` ersetzt den Übergangs-Fix) | +61 (7 `test_secretbox.py` + 8 `test_authserver_config.py` + 23 `test_authserver_store.py` + 13 `test_userdir.py` + 3 `test_flows.py` + 7 `test_import_users_to_db.py`, drei neue Dateien) |
| 4 | Neues Paket `phase5_ui/` (`pyproject.toml`, `webui/{__init__,config,security,sessions,pages,routes_auth,errors}.py`, `phase5_ui/tests/`): Sessions, CSRF, Login/Logout | 3 | ✅ **vollständig** — `/ui/login`, `/ui/logout` gegen eine echte In-Process-`Starlette`-App durchgespielt; **V35 geschlossen** (`dev_install.sh`s `phase*_*/`-Glob nimmt `phase5_ui/` ohne Skriptänderung auf) | +22 (5 `test_sessions.py` + 7 `test_security.py` + 7 `test_routes_auth.py` + 3 `test_isolation.py`, vier neue Testdateien + `conftest.py`) |
| 5 | Selbstverwaltung: Einladung/Enrollment, Passwort, TOTP, Recovery, Connectoren (`webui/{account,reauth,passwords_policy}.py`, `webui/blocklist.txt`, `webui/{pages,routes_auth,errors}.py` erweitert; `authctl.py`-Erweiterung um `invite`/`list-users`/`disable-user`/`enable-user`/`list-sessions`/`revoke-sessions`; `authserver/store.py` um `revoke_families_for_space()`/`revoke_invites_for_space()`; `authserver/flows.py :: submit_consent()` um den Status-Gate) | 4 | ✅ **vollständig** — **V30 geschlossen** (Blocklist-Herkunft: `SecLists`-10k-Liste, siehe `passwords_policy.py`-Docstring); zwei Advisor-Funde vor dem Commit behoben (**S9** in `phase4_auth/CLAUDE.md`s Befund-Tabelle: `disable-user` blockierte den Login nicht; verworfener CSRF-Token nach Passwortwechsel — beide Details im Session-Block unten) | +31 (7 `test_account.py` + 7 `test_invite_enroll.py` + 3 `test_passwords_policy.py` + 1 `test_reauth.py`, vier neue Testdateien; +1 `test_routes_auth.py`; P4-seitig +1 `test_flows.py` + 8 `test_authctl.py` + 3 `test_authserver_store.py`) |
| 6 | `/ui/*` aus Step 5 vorgezogen verdrahtet: `mcpserver/app.py :: create_app()` mountet `ui_auth_routes()`+`account_routes()` (kein neuer Parameter, `UiSettings`/`SessionManager` aus dem vorhandenen `oauth`-Bündel gebaut) | 4→5 (Gate-Voraussetzung) | ✅ **vollständig** — Live-Fund des Nikingers (`/ui/invite/…` → `404`) UND ein Plan-Widerspruch (§1.2 verbietet `mcpserver→webui`, §1.5 verlangt es) gemeinsam geschlossen, Entscheidung + Details im Session-Block unten | +3 (`phase2_mcp/tests/test_app.py`: `test_create_app_mounts_ui_routes_without_import_cycle`, `test_ui_login_reachable_through_create_app`, `test_ui_invite_reachable_through_create_app`) |
| 7 | `/ui/enroll/confirm`: CSRF-Fehlschlag rendert jetzt einen Retry (`routes_auth.py :: _enrollment_retry()`, geteilt mit „falscher Code") statt `render_error_page()`s Sackgasse; **Root Cause gefunden und behoben:** `webui/security.py`s `Referrer-Policy` von `no-referrer` auf `strict-origin` — `no-referrer` liess die Fetch-Spec den `Origin`-Header eines reinen HTML-`<form>`-POSTs auf `null` setzen, auch bei einer echten Same-Origin-Anfrage | 4 (Gate-Live-Fund) | ✅ **vollständig, live bestätigt** — Prozess-Neustart-Zeitstempel gegen die erste erfolgreiche `200`-Antwort auf `/ui/enroll/confirm` read-only gegengeprüft (nicht nur behauptet); `errors.py :: CsrfError`s Docstring korrigiert (unabhängiger, vorbestehender Fund); Details `SESSIONS_ARCHIVE.md` (Fünfter–Neunter Nachtrag, 2026-08-03/04) | +2 (`test_enroll_confirm_csrf_failure_offers_a_retry_not_a_dead_end`, `test_csrf_foreign_origin_logs_the_received_value_but_not_to_the_client`, `test_ui_referrer_policy_does_not_null_the_origin_header_on_same_origin_posts` — drei Tests, siehe Archiv für die Aufschlüsselung je Nachtrag) |
| 8 | REST-API v1: `webui/{api,serializers}.py`, `mcpserver/app.py :: create_app()` mountet `api_routes(ui_settings, store, ui_sessions, own_space_writable)` (`OwnSpaceWritable()` jetzt einmal instanziiert, geteilt mit `build_mcp()`) | 5 | ✅ **vollständig** — `scripts/ui_smoke.py` (neu, Gegenstück zu `mcp_smoke.py`/`oauth_smoke.py`) läuft In-Process durch Einladung→Enrollment→Login→`/api/v1/{me,spaces,items,...}`, 12/12 Prüfungen grün; eigener Fund (nicht im Plan-Testliste): `storage.store.Store.archive()` hat anders als `update()`/`append()` keinen Schutz gegen ein bereits archiviertes Item — in `api.py` (nicht in `storage/`, dort tabu) mit einem zusätzlichen `store.get()`-Check NACH der Rechteprüfung geschlossen | +38 (23 `test_api.py` + 7 `test_serializers.py`, zwei neue Testdateien; `phase2_mcp/tests/test_app.py` +1 `test_api_items_reachable_through_create_app`; `phase5_ui/tests/test_isolation.py` `test_api_endpoint_ignores_bearer_token` geschärft — Platzhalter seit Step 3 gegen die echte, gemountete Route ersetzt, kein zusätzlicher Test) |

---

## Session stopped — 2026-08-05 (Block-A-Gate live gefahren — Origin-Bug gefunden und behoben, 7/9 Zeilen bestanden)

**Für den nächsten, kalten Leser — Kurzfassung, Details im 2026-08-03-Block in
`SESSIONS_ARCHIVE.md`:** diese Session begann mit einem vom Nikinger gemeldeten „TOTP-Seed
kaputt" beim Block-A-Gate. War kein TOTP-Bug — `journalctl` zeigte 100 % `403` auf jeden
`/ui/enroll/confirm`-Versuch, nie `422`, der Request erreichte die TOTP-Prüfung also nie.
Root Cause nach zwei widerlegten Zwischenhypothesen (eingebetteter Vorschau-Panel, dann
Browser-Extension — beide durch einen Test in sauberem Chrome-Inkognito ohne Extensions
widerlegt): `webui/security.py`s `Referrer-Policy: no-referrer` lässt die Fetch-Spec den
`Origin`-Header eines reinen HTML-`<form>`-POSTs (kein JavaScript) auf `null` setzen, auch bei
einer echten Same-Origin-Anfrage — `require_csrf()` lehnte das korrekt ab, der eigene Header
hatte sich selbst ausgesperrt. **Fix:** `Referrer-Policy` auf `strict-origin` (nullt nur bei
TLS-Downgrade, sendet nie den Pfad — bewusst nicht `same-origin`, das würde
`/ui/invite/<token>`s Einmal-Secret über `Referer` preisgeben). Live bestätigt, nicht nur
behauptet: Prozess-Neustart-Zeitstempel gegen die erste erfolgreiche `200`-Antwort auf
`/ui/enroll/confirm` read-only gegengeprüft. `authserver/routes.py`s identischer
`no-referrer`-Wert für die OAuth-Seiten bewusst nicht mitgeändert (anderer Flow, eigener,
unbehobener Befund).

**Block-A-Abnahmematrix (§6) durchgefahren:** Zeilen 1, 2, 3, 4, 7, 8, 9 live bestanden (Details
je Zeile im archivierten Block). Zeile 9 (`strings`-Grep gegen `auth.sqlite3`) vom
Auto-Mode-Classifier für Claude Code blockiert (Rohzugriff auf echte Secrets — dieselbe
Kategorie, die laut Root-`CLAUDE.md` dem Nikinger vorbehalten ist), vom Nikinger selbst
gegengeprüft: leer, kein Klartext-Seed. **Zeilen 5/6 (Passwortwechsel ohne Restart,
Session-/Connector-Widerruf danach) bewusst zurückgestellt, keine stille Ersatzlösung:** Step 4
baute dafür nur die JSON-API (`/api/v1/account/*`), keine HTML-Seite — die App-Shell ist
Step-5/6-Scope, der nach diesem Gate liegt. Ein DevTools-`fetch()`-Behelf wurde angeboten und
vom Nikinger ausdrücklich abgelehnt: „das ist ein Workaround, kein echter Test." Nikinger-
Entscheidung: 5/6 folgen mit einem echten Klick-Pfad, sobald der existiert.

**Verifiziert:** `pytest -q` (Repo-Wurzel) → **473/473 grün**. `git diff --stat` auf
`storage/`, `mcpserver/tools.py`/`permissions.py`/`server.py` bleibt leer (Akzeptanzkriterium
§6.18). Zwei kleine, unabhängige Kosmetik-Funde notiert, nicht behoben: `render_enrollment_page()`s
inline `style`-Attribut wird von der eigenen `style-src 'self'`-CSP blockiert (kosmetisch, QR
bleibt scanbar); `_PAGE`s `<link rel="stylesheet" href="/ui/static/app.css">` 404et auf jeder
UI-Seite (erwartet, `static_dir` ist Step-5/6-Scope).

**Block A (§6) damit vollständig bis auf die bewusst verschobenen Zeilen 5/6.** Der harte Gate
vor Block B gilt für die sieben live bestandenen Zeilen als erfüllt.

**Nachtrag, später am selben Tag — Step 5 (REST-API v1) abgeschlossen:** `webui/serializers.py`
(neu — `item_to_json`/`summary_to_json`/`search_to_json`/`space_to_json`, Plan §3.2) und
`webui/api.py` (neu — `/api/v1/{me,spaces,items,items/{id},items/{id}/append,
items/{id}/archive}`, Plan §3.1/§3.3) gebaut, `mcpserver/app.py :: create_app()` mountet
`api_routes(ui_settings, store, ui_sessions, own_space_writable)` — der `store`-Parameter war
bereits vorhanden (bediente bisher nur `build_mcp()`), kein neuer `create_app()`-Parameter nötig,
anders als in der vorigen Notiz erwartet. `OwnSpaceWritable()` läuft jetzt als eine geteilte
Instanz (`own_space_writable`) für MCP-Tools UND REST-API statt zweier getrennter.

**Reihenfolge `space_of()` → Rechteprüfung → Store-Aufruf** (Plan §3.3, „nicht verhandelbar")
wörtlich aus `mcpserver/tools.py` übernommen, nicht neu erfunden — dieselbe Begründung (Rule 4:
ein Rechtefehler darf den Store nie erreichen, `space_of()` ist index-only und deshalb sicher
auch für einen Space, auf den kein Zugriff besteht). Zwei Tests
(`test_space_of_is_called_before_permission_check`,
`test_patch_foreign_item_is_403_and_never_reaches_store`) laufen bewusst gegen einen
`unittest.mock.MagicMock(spec=Store)`, nicht den echten `Store` — mit `OwnSpaceWritable.can_read`
(heute immer `True`) hätte ein echter Store beide Tests vacuous bestehen lassen, ohne die
Aufrufreihenfolge tatsächlich zu belegen.

**Eigener Fund, nicht in der Plan-Testliste:** `storage.store.Store.archive()` hat anders als
`update()`/`append()` keinen Schutz gegen ein bereits archiviertes Item (`storage/` ist für diese
Phase tabu, P5-B — ein Fix dort wäre eine Scope-Änderung). `POST /api/v1/items/{id}/archive`
holt deshalb NACH der Rechteprüfung (sicher, eigener Space) einmal den aktuellen Stand per
`store.get()` und lehnt ein zweites Archivieren mit `422 validation_failed` ab, statt die Version
bei jedem Klick stillschweigend hochzuzählen. Zweiter kleiner Fund: `storage.store._coerce_due()`
wirft bei einem falsch formatierten `due`-String ein rohes `ValueError`
(`date.fromisoformat`), keine `ValidationError` — `api.py :: _map_store_error()` fängt beide
Typen gleich ab (422), damit ein API-Client nicht zwei verschiedene Fehlerformen für denselben
Fehlerfall sieht.

**`/api/v1/spaces`** wiederholt bewusst den B1-Fix aus P2 (`tools.py :: list_spaces()`): ein
eigener Space ohne ein einziges Item taucht in `Store.list_spaces()` sonst gar nicht auf — die
Sichtbarkeitsprüfung läuft dabei aus der (ggf. ergänzten) lokalen Liste, nicht aus einem zweiten,
frischen `store.list_spaces()`-Aufruf (Advisor-artiger Selbstfund beim Testen: ein frischer
Aufruf hätte den synthetisierten leeren eigenen Space nie als sichtbar erkannt).

**Suche (`GET /api/v1/items`):** Filterparameter (`query`/`space`/`type`/`status`/`tag`/
`due_before`) wandern unverändert an `Store.search()`; `limit`/`offset` NICHT direkt — `Store`
kennt keine Menge „sichtbarer Spaces", nur einen einzelnen `space`-Filter. Diese Datei holt bis
zu einer eigenen `_STORE_FETCH_LIMIT=5000`-Konstante (Kostenabwägung wie `tools.py`s
gleichnamiger Wert, hier erneut definiert statt importiert — ein Import aus `mcpserver.tools`
wäre ein zweites `mcpserver`-Symbol, P5-B erlaubt nur `OwnSpaceWritable`), filtert nach
sichtbaren Spaces und paginiert danach selbst — sonst würden `total`/`offset` verfälscht, sobald
ein unsichtbarer Space existierte.

**`scripts/ui_smoke.py`** (neu, Gegenstück zu `mcp_smoke.py`/`oauth_smoke.py`): temporäres
`DATA_ROOT` + temporäre `AuthStore`, In-Process (`httpx.ASGITransport`, kein Port, kein Netz,
kein `--base-url`-Modus — Step 5s Done-when verlangt nur den In-Process-Lauf). Fährt Einladung →
TOTP-Enrollment → Login → `/api/v1/me`/`/spaces` → Item anlegen/lesen/ändern/anhängen/
archivieren → Versionskonflikt → fremder Space (readonly) einmal vollständig durch. **12/12
Prüfungen grün**, lokal ausgeführt.

**Verifiziert:** `pytest -q` (Repo-Wurzel) → **504/504 grün** (473 vor diesem Nachtrag, +31: 23
`test_api.py` + 7 `test_serializers.py`, zwei neue Testdateien, + 1
`test_api_items_reachable_through_create_app` in `phase2_mcp/tests/test_app.py`;
`test_isolation.py`s Platzhalter wurde geschärft, kein zusätzlicher Test). `git diff --stat` auf
`storage/`, `mcpserver/tools.py`/`permissions.py`/`server.py` bleibt leer (Akzeptanzkriterium
§6.18) — nur `mcpserver/app.py` (P5-B erlaubt das) und Testdateien geändert. `pyflakes` über alle
neuen/geänderten Dateien lief sauber durch. **Advisor-Review vor diesem Commit war nicht
möglich** (Tool zweimal „temporarily overloaded" zurückgemeldet, nicht übersprungen) — Ersatz:
`pyflakes`, voller `pytest -q`, `ui_smoke.py` real ausgeführt, Tabu-Pfad-Diff geprüft, alles vor
dem Commit. Kein stiller Verzicht auf die sonst übliche Disziplin, festgehalten statt verschwiegen.

**Nächster Schritt (konkret):** Step 6 (UI-Gerüst: Shell, Tokens, Navigation, Liste, Suche —
Plan §4.1–§4.3/§4.6, `webui/static/{app.html,app.css,app.js}`). Die `apple-design`-Skill
(58,5K Installs, `emilkowalski/skills@apple-design`) ist seit dieser Session installiert — der
Plan-Vermerk in §4 „einen `apple-design`-Skill gibt es in dieser Umgebung nicht" ist damit
überholt, Step 6 kann sie direkt nutzen statt nur von `frontend-design` abzuleiten. Zeilen 5/6
folgen, sobald Step 6 einen echten Klick-Pfad für `/api/v1/account/password` bietet. Die drei
liegen gebliebenen Live-Aktionen aus Step 1/2 (S3/S4-Gegenprobe, Purge-Timer aktivieren,
Migrations-Runbook) bleiben unverändert offen, blockieren weiterhin keinen Code-Step.
