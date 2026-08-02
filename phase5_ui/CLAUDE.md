---
status: live
purpose: Phase-Head Web-UI, REST-API, Auth-Selbstverwaltung — Scope, harte Regeln, Modulstatus, aktueller Session-Handover
read-when: Arbeiten in phase5_ui/ oder an den in P5-B genannten Dateien in authserver/mcpserver — zuerst lesen, zusammen mit dem neuesten Session-stopped-Block
detail: L2
up: ../CLAUDE.md
down:
  - ../docs/concepts/phase5_ui_plan.md             # voller Plan, Entscheidungen P5-A–P5-AE, Steps 0–9
  - ../docs/concepts/PHASE4_CLOSEOUT_HANDOVER.md   # Herkunft der offenen Entscheidungen §4.1–§4.5, [VERIFY]-Bilanz V14–V26
updated: 2026-08-02
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

---

## Session stopped — 2026-08-02 (Step 1: Sicherheitsbefunde S2–S8 vollständig geschlossen)

**Für den nächsten, kalten Leser:** zweite Session der Phase. Der Nikinger gab grünes Licht für
Step 1 mit einer Einschränkung: falls der Plan Voraussetzungen nennt, die noch nicht erfüllt
sind, zuerst das klären. Genau das traf zu — Details unten unter „Plan-Drift, vor jedem Fix
geklärt". Alle sieben Befunde (S2–S8) sind geschlossen, `pytest -q` lief vor Beginn bei 333/333
und steht am Ende bei **353/353**.

**Plan-Drift, vor jedem Fix geklärt (nicht blind übernommen):** Plan §5 Step 1 nennt für S6 den
Fix „entfällt strukturell mit `UserDirectory.get()`" und für S7 eine Erweiterung von
`purge_expired()` um `ui_sessions`/`invites` — beides sind Schema-2/`UserDirectory`-Artefakte
aus **Step 2**, der noch nicht gebaut ist (`authserver/userdir.py` existiert nicht,
`SCHEMA_VERSION` steht weiterhin auf `"1"`, keine `ui_sessions`/`invites`-Tabelle). Statt auf
nicht existierenden Code zu bauen: S6 bekam die vom Sicherheits-Review selbst vorgeschlagene
Fix-Skizze direkt auf dem aktuellen `Mapping`-Zugriff (`record.get(...)` statt `record[...]`);
S7 bekam den Timer plus die Längenbegrenzung jetzt, die `ui_sessions`/`invites`-Abdeckung bleibt
wie vom Plan selbst vorgesehen (`test_purge_removes_expired_sessions_and_invites` trägt im Plan
den Zusatz „nach Step 2 zu ergänzen") ein Nachtrag für Step 2. Advisor-Review vor Beginn hat
diese beiden Stellen bestätigt und zusätzlich zwei Live-Risiken benannt (S3/S4 könnten laufende
Connector-Token invalidieren) — read-only DB-Gegenprobe war von der Auto-Mode-Klassifizierung
blockiert; Code-Analyse zeigt aber, dass `resource`/`scope` deterministisch aus `settings`
abgeleitet werden (`config.py :: AuthSettings.resource`, `flows.py`s `scope or "space"`-Default)
und deshalb für alle real ausgestellten Token übereinstimmen — siehe „Nächster Schritt" unten,
diese Annahme sollte vor einem echten Restart einmal gegengelesen werden.

**S2 — `refresh_token`-Grant prüft jetzt `client_id`:** `store.py :: rotate_refresh()` bekam
einen Pflicht-`client_id`-Parameter, geprüft gegen `token_families.client_id` **vor** der
`rotated_at`-Prüfung — ein Mismatch ist ein früher `return None` (`invalid_grant`), **kein**
Familienwiderruf (ein falscher `client_id` ist kein Replay, sonst wäre der neue Check selbst ein
Fernauslöser gegen fremde, legitime Familien — das ist laut Plan „die wichtigere Hälfte").
`flows.py :: issue_token()` verlangt `client_id` jetzt auch im Refresh-Zweig. Alle bestehenden
Aufrufer (`oauth_smoke.py` Schritte 8/9, mehrere Store-/Flow-Tests) angepasst.

**S3/S4 — Audience- und Scope-Check bei der Bearer-Auflösung:** `OAuthTokenResolver.__init__`
nimmt jetzt ein Pflicht-`expected_resource` entgegen, `resolve()` lehnt ab, wenn
`record.resource` nicht passt (S3) oder `"space"` nicht in `record.scope.split()` steht (S4).
`mcpserver/app.py :: create_app()` verdrahtet `expected_resource=oauth.settings.resource`.

**S5 — Redirect-Query-Merge statt Verstümmelung:** `routes.py :: _authorize_response()` baut
die Redirect-URL jetzt über `urlsplit`/`parse_qsl`/`urlencode`/`urlunsplit` und mischt
`code`/`state`/`error` in eine vorhandene Query hinein, statt bedingungslos ein zweites `?`
anzuhängen.

**S6 — kein `KeyError` mehr bei kaputten Nutzerakten:** `flows.py :: submit_consent()` liest
`record.get("pwd")`/`record.get("totp", "")` statt per Index — ein unvollständiger Datensatz
ergibt jetzt dieselbe generische Fehlermeldung wie ein unbekannter Space (Enumerationsschutz
bleibt intakt, `totp.verify()` fing ungültiges Base32 bereits vorher ab).

**S7 — Purge-Timer + Längenbegrenzung:** `phase5_ui/systemd/sharefyx-purge.{service,timer}`
(täglich, ruft `authctl.py purge-expired`) — `install_units.sh`s `SYSTEMD_SRCS` um
`phase5_ui/systemd` erweitert (sonst wäre der Timer totes Gewicht, Advisor-Fund). **Live noch
nicht aktiv:** anders als `sharefyx-backup.timer` (dessen Enable-Schritt im Inbetriebnahme-
Runbook bereits gelaufen ist) gibt es für `sharefyx-purge.timer` noch **keinen** ausgeführten
Enable-Schritt — `install_units.sh` kopiert die Unit-Dateien nach `/etc/systemd/system/`, das
allein startet keinen Timer. Nikinger-Aktion, sobald `install_units.sh` das nächste Mal läuft:
`sudo systemctl enable --now sharefyx-purge.timer` (analog zu Schritt 5 im bestehenden Runbook
für `sharefyx-backup.timer`). Bis dahin ist S7 code-seitig geschlossen, aber operativ noch
inaktiv — `purge_expired()` läuft weiterhin nur, wenn jemand `authctl.py purge-expired` von
Hand ruft. Zusätzlich `ratelimit.py :: MAX_SPACE_LEN = 128` — `space` kommt unauthentifiziert
aus dem Formular und war ohne Längenbegrenzung ein Disk-DoS-Vektor als PRIMARY KEY in
`login_attempts`.

**S8 — `install_units.sh` sourced nicht mehr blind:** ersetzt durch ein striktes
KEY=VALUE-Parsen (kein `eval`, keine Shell-Interpretation) statt `source`. **Bewusste Abweichung
vom Plan-Wortlaut:** die Plan-Tabelle nannte eine root-Ownership-Prüfung per `stat`
(„Abbruch wenn nicht root") — das widerspräche dem im Repo selbst dokumentierten Modell, in dem
`local.env` `savefyx` gehört und von `savefyx` angelegt wird (README.md, Runbooks). Stattdessen
die vom Sicherheits-Review selbst vorgeschlagene Fix-Skizze („grep-basiertes Parsen") gewählt,
die dieselbe Schwachstelle (beliebiger Bash-Code aus einer `savefyx`-schreibbaren Datei, als
root ausgeführt) ohne die Ownership-Kollision schließt. Manuell gegen eine Injection-Zeile
(`touch /tmp/PWNED`) verifiziert, bevor der Pytest-Test geschrieben wurde: Skript bricht mit
`ABBRUCH: ... kein KEY=VALUE` ab, keine Datei entsteht.

**Verifiziert, nicht nur behauptet:** `pytest -q` → **353/353 grün** (333 + 20: 2
`test_authserver_store.py` + 4 `test_resolver.py` + 2 `test_routes.py` + 3 `test_flows.py` + 2
`test_ratelimit.py` + 5 `test_units.py` + 2 `test_security_review_register.py`, neue Datei).
`test_security_review_register_is_empty` (neu) parst die S2–S8-Tabelle in
`phase4_auth/CLAUDE.md` direkt und schlägt fehl, sollte je eine Zeile wieder ohne ✅ dastehen.
`phase4_auth/CLAUDE.md`s S2–S8-Tabelle im selben Commit nachgezogen (Status-Spalte ergänzt,
veralteter „Keiner von S2–S8 ist gefixt"-Absatz durch eine datierte Korrekturnotiz ersetzt —
dieses Dokument ist 📗 live gepflegt, kein 📕-Snapshot, deshalb direkt korrigiert statt in einem
separaten Nachtrag dupliziert). `git diff` bleibt außerhalb der P5-B-Berührungsfläche
(`authserver/`, `mcpserver/app.py`, `phase3_edge/scripts/install_units.sh`,
`phase3_edge/tests/test_units.py`, neue `phase5_ui/systemd/`) leer auf `storage/`,
`mcpserver/tools.py`, `mcpserver/permissions.py`, `mcpserver/server.py` (Akzeptanzkriterium 18).

**Kleine Abweichung von P5-B, dokumentiert statt still erweitert:** `phase4_auth/scripts/
oauth_smoke.py` steht nicht auf Plan §5 Step 1s Dateiliste — geändert wurden zwei
`grant_type="refresh_token"`-Aufrufe (Schritte 8/9), die jetzt `client_id` mitschicken müssen
(S2-Signaturänderung an `flows.issue_token()`). Gleiche Kategorie wie `mcp_smoke.py` im
P4-Schnitt: eine erzwungene Anpassung an eine geänderte Signatur, kein neuer Scope-Griff.

**Nächster Schritt (konkret):** Zwei Dinge, bevor Step 2 beginnt — beide Sache des Nikingers,
keine Claude-Code-Aufgabe:

1. **Live-Voraussetzung vor dem nächsten `sudo systemctl restart sharefyx-mcp`:** S3/S4 fügen
   neue Ablehnungsbedingungen in den Bearer-Auflösungspfad ein, der gerade zwei echte
   Verbindungen (`niklas`, `fabian`) bedient. Code-Analyse zeigt, dass `resource`/`scope` für
   real ausgestellte Token deterministisch mit den jetzt geprüften Erwartungswerten
   übereinstimmen sollten (siehe „Plan-Drift" oben) — das ist aber eine Ableitung aus dem Code,
   **keine** Live-Verifikation (der read-only DB-Zugriff war für Claude Code in dieser Session
   durch die Auto-Mode-Klassifizierung blockiert). Vor dem nächsten Restart einmal gegenlesen:
   ```
   sqlite3 -readonly /var/lib/sharefyx/auth.sqlite3 \
     "SELECT space, scope, resource FROM token_families WHERE revoked_at IS NULL;"
   ```
   **Bestehensbedingung:** jede Zeile trägt `resource = https://savefyx-vmware-virtual-platform.tail89fc2a.ts.net/mcp`
   und `scope` enthält das Wort `space`. Trifft das nicht zu, loggt der Restart beide Nutzer aus
   (ein Client **darf** laut `SUPPORTED_SCOPES` legitim nur `offline_access` ohne `space`
   angefordert haben — das ist der konkrete Fehlfall, den S4 dann greifen lässt).
2. **`sudo systemctl enable --now sharefyx-purge.timer`** nach dem nächsten
   `install_units.sh`-Lauf (siehe S7 oben) — ohne diesen Schritt bleibt der Purge-Timer
   installiert, aber inaktiv.

Danach: Step 2 (Auth-Datenmodell Schema 2, `secretbox.py`, `userdir.py` — schließt auch die
S6/S7-Restarbeit von oben strukturell ab).
