---
status: live
purpose: Phase-Head Web-UI, REST-API, Auth-Selbstverwaltung — Scope, harte Regeln, Modulstatus, aktueller Session-Handover
read-when: Arbeiten in phase5_ui/ oder an den in P5-B genannten Dateien in authserver/mcpserver — zuerst lesen, zusammen mit dem neuesten Session-stopped-Block
detail: L2
up: ../CLAUDE.md
down:
  - ../docs/concepts/phase5_ui_plan.md             # voller Plan, Entscheidungen P5-A–P5-AE, Steps 0–9
  - ../docs/concepts/PHASE4_CLOSEOUT_HANDOVER.md   # Herkunft der offenen Entscheidungen §4.1–§4.5, [VERIFY]-Bilanz V14–V26
updated: 2026-08-03
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

---

## Session stopped — 2026-08-03 (Step 4: Selbstverwaltung — Einladung, Passwort, TOTP, Recovery, Connectoren)

**Für den nächsten, kalten Leser:** diese Session begann nach einem Context-Compaction-Verlust
— der einzige erhaltene Rest war eine Notiz, dass eine vorige Session mitten in Step 4 stand:
Code + Tests für `account.py`/`reauth.py`/`passwords_policy.py`/`blocklist.txt` plus die
`authctl.py`-Erweiterung lagen bereits unstaged im Arbeitsverzeichnis, `git status` bestätigte
das (keine Behauptung aus dem Notiz-Rest übernommen, siehe Root-`CLAUDE.md`-Lehre „eine
Doku-Aussage über den Repo-Zustand ist erst wahr, wenn `git status` sie bestätigt"). Die Notiz
nannte drei ausstehende Schritte: `phase5_ui/tests` grün, danach das ganze Repo grün, dann eine
Advisor-Review vor der Dokumentation. Alle drei nachgeholt, plus was der Advisor dabei fand.

**Bauteile aus der vorigen (verlorenen) Session, gegengelesen statt neu gebaut:**
1. **`account.py`** — `/api/v1/account/*`, JSON durchgehend (§3.1). Jede Route lädt zuerst die
   Sitzung, state-ändernde Routen prüfen CSRF (`X-CSRF-Token`-Header), re-auth-pflichtige Routen
   (P5-P) zusätzlich Passwort+TOTP über `reauth.verify_reauth()`. Acht Routen: Passwort ändern,
   TOTP-Neueinrichtung (Start/Confirm), Recovery-Codes neu ausgeben, eigene Sessions
   auflisten/beenden, eigene Connector-Verbindungen auflisten/widerrufen.
2. **`reauth.py :: verify_reauth()`** — Passwort + TOTP in einem Schritt, **kein**
   Recovery-Code-Ersatz (anders als der normale Login, P5-P-Wortlaut „Passwort UND TOTP-Code").
   Dieselbe `LoginThrottle` wie UI-/OAuth-Login. Zähler-Reihenfolge korrekt: `set_totp_counter()`
   läuft erst nach `throttle.reset()`, also nach vollständigem Erfolg — dieselbe Lehre wie der
   Step-3-Advisor-Fund in `routes_auth.py`, hier beim Nachbau richtig übernommen.
3. **`passwords_policy.py`** — Länge (12–128) + Blocklist, kein Zeichenklassenzwang, kein
   Netzaufruf (Bauprinzip: der Server telefoniert nicht nach Hause). **V30 geschlossen:**
   `blocklist.txt` ist `danielmiessler/SecLists`s `10k-most-common.txt` (MIT-lizenziert, geht auf
   Mark Burnetts „10,000 Top Passwords" zurück), 10000 Einträge, 73 KB — deckt sich mit dem
   Plan-Vorschlag „~80 KB" fast exakt.
4. **`routes_auth.py`-Erweiterung** — `/ui/invite/{token}` (GET/POST), `/ui/enroll/confirm`.
   Passwortpolitik wird **vor** `consume_invite()` geprüft (die Einladung ist einmalig — ein zu
   schwaches erstes Passwort darf sie nicht verbrennen). `store.upsert_user()` statt
   `set_password()`/`begin_totp_enrollment()` allein, weil für einen brandneuen Space aus einer
   Einladung noch keine `users`-Zeile existiert (beide Methoden können nur `UPDATE`). TOTP-QR
   über `segno` (Inline-SVG, V29 geschlossen, `pyproject.toml` exakt gepinnt `segno==1.6.6`, P4-R
   pass'sches Pin-Muster übernommen) — geprüft, nicht nur behauptet: `pages.py ::
   render_enrollment_page()` rendert tatsächlich ein `<svg>`, die `img-src 'self' data:`-Lockerung
   in `security.py`s CSP-Kommentar war also zutreffend, nicht nur eine Ankündigung.
5. **`authctl.py`-Erweiterung** — sechs neue Unterbefehle: `invite` (Link genau einmal auf
   stdout, Klartext-Disziplin wie `provision_user.py`), `list-users` (keine Hashes/Seeds),
   `disable-user`/`enable-user`, `list-sessions`/`revoke-sessions`. `disable-user`/
   `revoke-sessions` dürfen anders als `revoke --family-id` sammeln (`--space`
   statt `--family-id`) — bewusste Ausnahme von der P4-Step-7-Regel „kein Sammelwiderruf",
   dokumentiert im Modul-Docstring: eine Sitzung/Familie ist kein Betreiber-Werkzeug wie ein
   DCR-Client, sondern der Notausgang, den Plan §5 Step 4 dafür vorsieht.

**Tests grün, wie in der Notiz gefordert:** `pytest phase5_ui/tests -q` → 39/39, `pytest -q`
(Repo-Wurzel) → 462/462 (436 zu Step-3-Ende, +26 aus der vorigen Session).

**Advisor-Review vor der Dokumentation (wie von der Notiz verlangt) — drei echte Funde, alle vor
dem Commit behoben, keiner still liegen gelassen:**

1. **`account.py :: _password()` verwarf den rotierten CSRF-Token — blockierend.**
   `sessions.rotate()` gibt den CSRF-Token nur EIN einziges Mal als Klartext zurück (`ui_sessions`
   speichert nur `csrf_hash`, exakt der Grund, aus dem `pages.py :: render_logged_in_page()` in
   Step 3 gebaut wurde) — der Rückgabewert landete bisher im Leeren. Jede folgende
   CSRF-geprüfte `/api/v1/account/*`-Anfrage nach einem Passwortwechsel hätte bis zum nächsten
   Login mit `403 csrf_failed` geantwortet. Fix: `response.render({"ok": True, "csrf_token":
   new_csrf})`, `content-length` nachgezogen. Neuer Test
   `test_password_change_returns_a_usable_csrf_token` (`test_account.py`) — macht bewusst einen
   ZWEITEN CSRF-geprüften Aufruf (`DELETE /api/v1/account/sessions`) mit dem neuen Token; der
   bestehende `test_password_change_revokes_other_sessions_but_not_current` hätte die Lücke
   nicht gefunden, weil sein Folgeaufruf ein `GET` ist (CSRF-frei).
2. **Kein Login-Pfad prüfte `record.status` — blockierend, neuer Sicherheitsbefund S9.**
   `authctl.py disable-user` widerrief bisher nur Sitzungen und Token-Familien, aber weder
   `webui/routes_auth.py :: _login_post` noch `authserver/flows.py :: submit_consent` lasen je
   `record.status` — ein deaktivierter Space konnte sich mit unverändertem Passwort/TOTP sofort
   wieder einloggen bzw. neu autorisieren, `disable-user` war ohne Live-Wirkung reines
   Papier-Kommando. Fix in **beiden** Pfaden: `account_active = record is not None and
   record.status == "active"`, zusätzliches Erfolgskriterium, nach dem unconditional
   Argon2id-Verify eingehängt (Enumerationsschutz bleibt intakt — kein eigener Fehlercode, exakt
   dieselbe generische Meldung wie ein falsches Passwort). Neue Tests:
   `test_disabled_account_cannot_log_in` (`test_routes_auth.py`),
   `test_disabled_account_cannot_consent` (P4 `test_flows.py`). Dokumentiert als **S9** in
   `phase4_auth/CLAUDE.md`s Befund-Tabelle (dated Nachtrag dort) — eine geschlossene Phase mit
   einem 📗 live gepflegten Kopf bekommt bei Code-Änderungen dieselbe Behandlung wie S2–S8, kein
   stiller Abstand von der eigenen Konvention.
3. **`disable-user` ließ eine offene Einladung am Leben — im selben Zug behoben, nicht nur
   notiert (Advisor: „billig genug für diesen Commit").** `_invite_post` legt über
   `store.upsert_user(..., status="active")` bei Einlösung eine neue, aktive Nutzerakte an — eine
   noch nicht eingelöste Einladung hätte `disable-user` damit unterlaufen können. Neue Methode
   `store.revoke_invites_for_space()` (markiert alle noch nicht eingelösten Einladungen als
   eingelöst, `consumed_at = jetzt`, kein eigenes „revoked"-Feld nötig — inklusive bereits
   abgelaufener Zeilen, kein `expires_at`-Filter, Docstring nennt das explizit), aufgerufen aus
   `_cmd_disable_user`. Neue Tests: `test_revoke_invites_for_space_only_touches_own_unconsumed_ones`
   (`test_authserver_store.py`), `test_disable_user_also_revokes_outstanding_invites`
   (`test_authctl.py`).

**Zwei weitere Advisor-Funde, bewusst NICHT gefixt, nur benannt (Advisor: „Warzen, keine
Blocker"):**
- `reauth.py :: verify_reauth()`/`flows.py :: submit_consent()`: `consume_recovery_code()` läuft
  bereits, sobald `password_ok` wahr ist — bei falschem TOTP UND korrektem Passwort UND einem
  vorgelegten Recovery-Code würde der Code verbrannt, obwohl der Login am Ende trotzdem scheitert
  (fehlt hier: TOTP war der vorgelegte Faktor, kein Recovery-Code-Pfad aktiv — betrifft also nur
  den Fall, dass jemand einen Recovery-Code an der TOTP-Stelle einreicht). Höchstens
  Selbst-Griefing, kein Fremdrisiko: das eigene Konto ist so oder so nicht eingeloggt. Nicht
  umgebaut, um den bestehenden, bereits getesteten Zweig nicht anzufassen.
- `authctl.py :: set_user_status()` ist ein stiller No-Op für einen nicht existierenden Space —
  `disable-user --space ghost` meldet „deaktiviert" ohne Wirkung. Operator-Werkzeug-Macke, kein
  Sicherheitsproblem (kein Space, kein Schaden), vorgemerkt für einen künftigen `authctl.py`-Umbau.

**Verifiziert, nicht nur behauptet, nach allen drei Fixes:** `pytest -q` (Repo-Wurzel) →
**467/467 grün** (462 vor den Fixes, +5: `test_password_change_returns_a_usable_csrf_token`,
`test_disabled_account_cannot_log_in`, `test_disabled_account_cannot_consent`,
`test_disable_user_also_revokes_outstanding_invites`,
`test_revoke_invites_for_space_only_touches_own_unconsumed_ones`). `git diff --stat` auf
`storage/`, `mcpserver/{tools,permissions,server}.py` bleibt leer (Akzeptanzkriterium §6.9,
gegengeprüft trotz P4-Dateien im Diff — `flows.py`/`store.py`/`authctl.py` liegen alle innerhalb
von P4-Qs erlaubter Berührungsfläche für `authserver`, keine davon auf der Tabu-Liste). Zweiter
Advisor-Durchlauf nach den Fixes bestätigte: Enumerationseigenschaft hält (Status-Gate sitzt nach
dem Argon2id-Verify in beiden Pfaden), `_revoke_family_locked()` löscht `access_tokens`/
`refresh_tokens`-Zeilen (kein bloßes `revoked_at`-Flag) — ein per `disable-user` widerrufenes
Bearer-Token stirbt sofort, nicht erst nach TTL-Ablauf.

**Doku-Abgleich gegen den Plan (Advisor-Auftrag, nicht blockierend):** die in Plan §5 Step 4
gelisteten Testnamen decken sich nicht alle wörtlich mit den tatsächlichen — drei Namen
(`test_recovery_code_replaces_totp_not_password`, `test_used_recovery_code_cannot_be_reused`,
`test_recovery_code_works_in_oauth_consent_form`) beschreiben Verhalten, das bereits in P5 Step 2
gebaut und getestet wurde (`test_authserver_store.py :: test_recovery_codes_replace_and_consume`,
`test_flows.py :: test_recovery_code_login_does_not_touch_totp_counter`/
`test_wrong_password_with_valid_recovery_code_does_not_burn_it`) — der Plan wurde ohne frischen
Repo-Zugriff geschrieben (wie alle P4/P5-Pläne) und zählt Verhalten aus einem früheren Step
erneut auf. Kein Deckungsloch, nur eine Namensabweichung.

**Nachtrag, später am selben Tag — `/ui/*` aus Step 5 vorgezogen verdrahtet, Live-Fund des
Nikingers während des Block-A-Gates:** `authctl.py invite niklas` lieferte einen
`/ui/invite/<token>`-Link, der Aufruf im Browser lieferte **`404`**. Ursache: `webui`s
Auth-Routen (`ui_auth_routes()`/`account_routes()`, Step 3/4, vollständig getestet) waren nie in
den echten Prozess gemountet — `mcpserver/app.py :: create_app()` kannte bis dahin ausschließlich
`oauth_routes()` und `Mount("/mcp")`. Grund: Plan §5 Step 5 listet genau diese Verdrahtung
("`webui_routes(...)` in die Routenliste") als **eigenen** Schritt, aber Step 5 selbst ist laut
Plan hinter dem Block-A-Gate verriegelt — und der Gate selbst verlangt Live-Zeilen 1–9 gegen
`/ui/login`/`/ui/invite/{token}` (§6). **Ein Zirkel im Plan-Text**, kein Interpretationsspielraum:
der Gate kann nicht bestehen, bevor der Schritt läuft, der hinter dem Gate liegt.

**Zweiter, unabhängiger Fund beim Nachlesen des Plans wegen desselben Themas:** Plan §1.2s
Paketgrenzen-Tabelle verbietet `mcpserver` ausdrücklich den Import von `webui`
("`mcpserver` … darf **nicht** importieren: `webui`") — aber §1.5s eigene Route-Landkarte zeigt
`create_app()` genau das tun (`routes += webui_routes(...)`). Beide Stellen stehen im selben
📕-Plandokument; §1.2 ist keine der 30 einzeln benannten, gelockten Entscheidungen (P5-A–P5-AE),
sondern eine Ableitungstabelle, die mit der im selben Dokument gezeichneten Architektur nicht
zusammenpasst.

**Beides dem Nikinger vorgelegt statt still aufgelöst** (Root-`CLAUDE.md`: „Widersprechende
Evidenz wird ein expliziter Befund für den Menschen, nie eine stille Abweichung"). Entscheidung:
**minimale Verdrahtung jetzt vorziehen** — nur `ui_auth_routes()`+`account_routes()` (beide
fertig, getestet), **nicht** `webui/api.py` (existiert noch nicht, echter Step-5-Scope) — damit
der Gate durchführbar wird, plus eine Korrektur der §1.2-Aussage hier im Phase-Head (📕-Plan
selbst bleibt unverändert, wie bei jeder Plan-Korrektur in diesem Projekt — siehe z. B.
`authserver/passwords.py :: ARGON2_TIME_COST`s Korrekturnotiz zum selben Muster).

**§1.2-Korrektur:** „`mcpserver` darf `webui` nicht importieren" gilt ab diesem Nachtrag **nicht
mehr uneingeschränkt** — `mcpserver/app.py :: create_app()` importiert `webui.routes_auth`/
`webui.account`, mit Begründung. Was UNVERÄNDERT gilt: `webui` importiert weiterhin höchstens ein
Symbol aus `mcpserver` (`permissions.OwnSpaceWritable`, P5-B, noch ungenutzt — kommt erst mit
`webui/api.py` in Step 5). Die Richtung des Verbots war die, die einen Zyklus verhindern sollte
(`mcpserver → webui → mcpserver`); ein reiner `mcpserver → webui`-Import ohne Rückweg ist
architektonisch unbedenklich. Geprüft, nicht nur behauptet: `mcpserver/permissions.py` (das
einzige `mcpserver`-Symbol, das `webui` je ziehen darf) importiert selbst nur `collections.abc`/
`typing` — kein Pfad zurück zu `mcpserver.app` oder `webui`, auch nicht sobald `webui/api.py` in
Step 5 dazukommt. Test `test_create_app_mounts_ui_routes_without_import_cycle`
(`phase2_mcp/tests/test_app.py`) hält diese Prämisse fest.

**Umsetzung, ein Commit:** `mcpserver/app.py :: create_app()` baut `UiSettings`/`SessionManager`
intern aus dem bereits vorhandenen `oauth`-Bündel (`oauth.settings.base_url`, `oauth.store`,
`oauth.users` — dieselbe `AuthStore`/`UserDirectory`-Instanz wie die OAuth-Seite, kein zweiter
DB-Handle), mountet `ui_auth_routes()`+`account_routes()` zwischen `oauth_routes()` und
`/health`/`Mount("/mcp")` — exakt die von §1.5 vorgezeichnete Reihenfolge. **Keine neuen
`create_app()`-Parameter.** Drei neue Tests in `phase2_mcp/tests/test_app.py`:
`test_create_app_mounts_ui_routes_without_import_cycle` (siehe oben),
`test_ui_login_reachable_through_create_app`, `test_ui_invite_reachable_through_create_app` —
beide Letzteren bauen bewusst die ECHTE `create_app()`-App (die `app`-Fixture, dieselbe wie die
MCP-Tests), nicht `phase5_ui/tests`s eigenständige `Starlette(routes=ui_auth_routes(…))`-Testapp
— genau der Unterschied, den der Live-Fund aufgedeckt hat: Step 3/4s Done-when-Nachweis lief nie
gegen den echten Prozess.

**Verifiziert:** `pytest -q` (Repo-Wurzel) → **470/470 grün** (467 vor diesem Nachtrag, +3).
`git diff --stat` auf `storage/`, `mcpserver/tools.py`/`permissions.py`/`server.py` bleibt leer
(Akzeptanzkriterium §6.18) — nur `mcpserver/app.py` und die beiden Testdateien geändert.
`phase2_mcp/CLAUDE.md`s Testzahl-Zeile im selben Commit nachgezogen (80→83).
`python -c "from mcpserver.app import create_app"` lief vor dem Testlauf zusätzlich isoliert
durch, um einen Importfehler von einem Testfehler zu unterscheiden.

**Schritt null vor dem Gate, nicht optional (Advisor-Hinweis):** dieser Nachtrag ändert nur den
Code. Der laufende `sharefyx-mcp`-Dienst führt noch den alten Build — „`/ui/login`/
`/ui/invite/{token}` sind live erreichbar" gilt erst nach
`sudo phase3_edge/scripts/install_units.sh && sudo systemctl restart sharefyx-mcp` (kein
Migrations-Runbook nötig, reiner Code-Deploy). Ohne diesen Restart liefert ein erneuter Versuch
mit dem Invite-Link wieder `404`, und der Fix sähe fälschlich kaputt aus.

**Nächster Schritt (konkret):** nach dem Restart — der harte Gate vor Block B, Abnahmezeilen 1–9
(§6) live, Sache des Nikingers (Passwort/TOTP/Recovery/Session/Connector-Selbstverwaltung im
echten Browser gegen den echten Dienst). Danach erst Step 5 (REST-API v1) — **teilweise, nicht
vollständig vorgezogen** (Advisor-Korrektur: die erste Fassung dieses Absatzes behauptete „bereits
erledigt", das überzieht): Plan §1.5 zeigt `webui_routes(ui_settings, auth_store, userdir, store,
sessions)` mit einem `store`-Parameter (dem `storage.Store`, für `/api/v1/items/*`) — dieser
Nachtrag mountet nur `ui_auth_routes()`/`account_routes()`, die diesen Parameter nicht brauchen.
Step 5 baut `webui/api.py`/`serializers.py` und braucht dafür einen weiteren, kleinen Edit an
`create_app()` (den `store`-Parameter zusätzlich durchreichen), keine komplette Neuverdrahtung,
aber eben auch keine Nullarbeit. Die drei liegen gebliebenen Live-Aktionen
aus Step 1/2 (S3/S4-Gegenprobe, Purge-Timer aktivieren, Migrations-Runbook) bleiben unverändert
offen, blockieren weiterhin keinen Code-Step.
