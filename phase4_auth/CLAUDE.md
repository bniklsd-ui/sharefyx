---
status: live
purpose: Phase-Head OAuth 2.1 + DCR — Scope, harte Regeln, Modulstatus, aktueller Session-Handover
read-when: Arbeiten in phase4_auth/ oder an den in P4-Q genannten Dateien in phase2_mcp/mcpserver — zuerst lesen, zusammen mit dem neuesten Session-stopped-Block
detail: L2
up: ../CLAUDE.md
down:
  - ../docs/concepts/phase4_auth_plan.md          # voller Plan, Entscheidungen P4-A–P4-R, Steps 0–7
  - ../docs/concepts/PHASE3_CLOSEOUT_HANDOVER.md  # Herkunft der offenen Entscheidungen, Doku-Drift, [VERIFY]-Bilanz
  - SESSIONS_ARCHIVE.md                            # ältere Session-Blöcke, newest-first
updated: 2026-07-31
---

# CLAUDE.md — Phase 4: OAuth 2.1 + DCR (`phase4_auth/`)

> **Der Pfad-Token verschwindet.** Ein eigener, handgeschriebener Authorization Server im selben
> Prozess ersetzt ihn — Discovery, Dynamic Client Registration, PKCE, Argon2id + TOTP, opake
> rotierende Token. Kein Upstream-IdP, kein `auth=`-Parameter an `FastMCP`.
> **Quelle der Wahrheit ist der Code, nicht dieses Dokument.**
> Vollständiges Design + alle 18 gelockten Entscheidungen (P4-A–P4-R) + Steps 0–7:
> `../docs/concepts/phase4_auth_plan.md`.

## Mission (zuerst lesen)

Der eigentliche Härtetest der Phase ist nicht der erste erfolgreiche Login, sondern der erste
erfolgreiche **Fehlschlag**: ein wiederverwendeter Refresh-Token muss die ganze Token-Familie
töten, ein zweimal eingelöster Authorization-Code muss die daraus entstandenen Token widerrufen,
und ein falsches Passwort darf nicht verraten, ob das Konto existiert. Diese drei Fälle sind
Akzeptanzkriterien, keine Kür (Plan §0.1).

## Bauprinzip (Projekt-Kernprinzip)

„Der Server ist dumm." **Phase 4 enthält KEINE AI, keine neuen Tools, keine Fachlogik.** Wer
hier `tools.py` anfasst, ist in der falschen Phase (P4-Q).

## Scope (Kurzform, Details: Plan §0.3/§0.7 P4-A–P4-R)

- **DRIN:** Protected Resource Metadata (RFC 9728), Authorization Server (RFC 8414), Dynamic
  Client Registration (RFC 7591), PKCE `S256` (RFC 7636), Token-Rotation + Familien-Widerruf
  (RFC 9700), `iss` im Authorization Response (RFC 9207), Argon2id-Passwörter, TOTP (RFC 6238)
  als zweiter Faktor, befristeter Parallelbetrieb `SPACE_AUTH_MODE=both`.
- **DRAUSSEN:** REST/UI (P5), MCP-Revision 2026-07-28, `fastmcp` 4, D6, neue Tools,
  feingranulare Lese-Rechte, Off-site-Backup, Monitoring, `/oauth/revoke`, `/oauth/introspect`,
  Recovery-Codes für den zweiten Faktor, CIMD (Seam vorhanden, siehe Plan §2.6 `[SEAM]`).

**[2026-07-28 Nachtrag, `[VERIFY]` V14 vor Step 4]:** Web-Recherche gegen die aktuelle
Anthropic-Doku (`claude.com/docs/connectors/building/{authentication,lazy-authentication}`,
live geprüft) bestätigt 13 von 14 Plan-Annahmen aus §0.6 wortgleich oder sinngleich — **eine
Ausnahme:** native/Loopback-Clients (RFC 8252 §7.3) sind inzwischen ein **dokumentiertes,
aktuelles** Anthropic-Verhalten, nicht mehr nur eine Erweiterungs-Idee. Claude Code deklariert
laut aktueller Doku `http://127.0.0.1/callback` **und** `http://localhost/callback` in seinem
CIMD, Port ignoriert, und Anthropic verlangt von AS-Betreibern, beide zu akzeptieren.

**Nikinger-Entscheidung (2026-07-28):** trotzdem draußen lassen für Step 4 — weniger Variablen,
die parallel getestet werden müssten. Rejection von `application_type: native` bleibt wie
geplant (§2.6). Diese Notiz dokumentiert den **einfacheren Weg für später**, damit er bei
Bedarf nicht neu recherchiert werden muss:

1. **Redirect-Matching ist der leichte Teil**, nicht der ganze Umfang: `redirect_uri_allowed()`
   (das `[SEAM]` aus Plan §2.6) bräuchte eine zweite Vergleichsregel für Loopback-URIs mit
   ignoriertem Port — genau wie der Docstring dort bereits vorwegnimmt.
2. **Der eigentliche Umfang ist CIMD, nicht DCR.** Claude Code identifiziert sich laut Doku über
   eine CIMD-URL als `client_id`, nicht über `/oauth/register`. Das heißt: nicht nur die
   Redirect-Prüfung lockern, sondern eine zweite Client-Identifizierungsart (CIMD-Dokument per
   HTTP abrufen, statt DCR-Registrierungszeile aus `clients`-Tabelle lesen) zusätzlich zu DCR
   bauen. Das ist der eigentliche Aufwand, nicht die Redirect-URI-Regel.
3. **`client_id_metadata_document_supported` bleibt abwesend** in den AS-Metadaten (Plan §2.2),
   bis Punkt 2 gebaut ist — die Anwesenheit dieses Felds ist laut Doku das Signal, mit dem
   Claude auf CIMD statt DCR umschaltet.
4. Quelle/Zeitpunkt: Agent-Recherche dieser Session, 2026-07-28, gegen die oben genannten
   Live-Seiten — kein `[VERIFY]`-Rest, das war bereits die Verifikation.

## Harte Regeln dieser Phase (nicht verhandelbar)

- **P4-A/P4-C — Eigener AS, strikte Abhängigkeitsrichtung.** `mcpserver → authserver`, niemals
  umgekehrt. `authserver` importiert nichts aus `mcpserver` oder `storage` — kennt nur
  Starlette, SQLite, `argon2-cffi`. Test: `test_authserver_does_not_import_mcpserver`.
- **P4-D — Token opak.** `secrets.token_urlsafe(32)`, gespeichert wird ausschließlich
  `sha256`-Hex. Kein JWT, kein JWKS, kein Signing-Key.
- **P4-F — Argon2id, nicht scrypt.** `m=19456 KiB, p=1` (OWASP + BSI TR-02102-1).
  **[2026-07-28 Korrektur, P4 Step 2]:** `t=2` war der Plan-Default, nicht der scharfe Wert —
  `[VERIFY]` V17 maß auf dieser VM ~15 ms damit (unter dem Zielkorridor 50–250 ms), Code läuft
  seit Step 2 mit **`t=8`** (~53–55 ms, gemessen). Konstante: `authserver/passwords.py ::
  ARGON2_TIME_COST`. V17 geschlossen, kein offener Punkt mehr.
- **P4-I — Ausnahme von Hard Rule 2.** Die Auth-SQLite (`/var/lib/sharefyx/auth.sqlite3`) ist
  autoritativ, keine Ableitung aus Dateien — benannte Ausnahme, berührt keine Nutzdaten.
- **P4-Q — Berührungsfläche.** P4 darf in `phase2_mcp/` genau anfassen: `mcpserver/asgi.py`,
  `mcpserver/context.py`, `mcpserver/app.py`, `mcpserver/config.py`, `mcpserver/request_log.py`,
  `mcpserver/logging_setup.py`, `scripts/serve.py`. **Nicht anfassen:** `tools.py`,
  `permissions.py`, `server.py`, `auth.py`, `credentials.py`, `storage/*`. Änderungsbedarf dort
  ist ein Befund für den Nikinger, keine Aufgabe.
- **P4-R — Bibliotheks-Pins.** `fastmcp==3.4.4` bleibt exakt (P3-D unverändert).
  `argon2-cffi==25.1.0` exakt gepinnt (in Step 0 gemessen, kein Range). Sonst keine neuen
  Laufzeitabhängigkeiten: kein `authlib`, kein `pyjwt`, kein `jinja2`, kein `itsdangerous`.

## Modul-Status

| # | Modul | Step | Status | Tests |
|---|---|---|---|---|
| 1 | Haushalt, Drift, geerbte Abnahme, kritischer Keyring-Fund (nikinger-Token) | 0 | ✅ | 0 (kein Feature-Code) |
| 2 | Paketgerüst `phase4_auth/`, `authserver/{config,models,crypto,errors}.py` | 1 | ✅ | 20 (5 `test_crypto.py` + 12 `test_authserver_config.py` + 3 `test_errors.py`) |
| 3 | `authserver/{passwords,totp,users}.py`, `scripts/{provision_user,export_auth_users}.py` | 2 | ✅ | 37 (6 `test_passwords.py` + 21 `test_totp.py` + 10 `test_users.py`) |
| 4 | `authserver/{store,ratelimit}.py` | 3 | ✅ | 19 (14 `test_authserver_store.py` + 5 `test_ratelimit.py`) |
| 5 | `authserver/{metadata,clients}.py`, erste Hälfte `routes.py` | 4 | ✅ | 16 (7 `test_metadata.py` + 8 `test_clients.py` + 1 neu in `test_authserver_config.py`) |
| 6 | `authserver/{flows,templates}.py`, `routes.py` vervollständigt (`/oauth/authorize`, `/oauth/token`) | 5 | ✅ | 36 (22 `test_flows.py` + 9 `test_routes.py` + 4 `test_templates.py` + 1 neu in `test_totp.py`) |
| 7a | `authserver/resolver.py`; `mcpserver/{asgi,context,app}.py` verdrahtet (Bearer-Auflösung, `AuthModeASGI`, `oauth=None`) | 6a | ✅ | 19 (6 `test_resolver.py` + 13 `test_asgi_bearer.py`) |
| 7b | `phase4_auth/scripts/oauth_smoke.py`; `mcpserver/{request_log,logging_setup}.py` erweitert (`OAuthLogASGI`, `_SECRET_PATTERNS`); `scripts/serve.py` verdrahtet (`SPACE_AUTH_MODE`-Gate) | 6b | ✅ | 6 neu in `test_oauth_smoke.py` (neue Datei, 11/11 `oauth_smoke.py` + fünf Regressionstests) + 3 neu in `test_request_log.py` + 6 neu in `test_logging.py` + 1 neu in `test_asgi_bearer.py` (Plan-Done-when-Klausel 3: sechs Tools unter Bearer vs. Pfad-Token) |
| 8 | `phase4_auth/scripts/authctl.py` (+ `store.py :: list_clients`/`list_families`, `config.py :: resolve_db_path`); `phase4_auth/systemd/sharefyx-mcp.service` (`StateDirectory`, zweites Credential, `SPACE_AUTH_MODE`/`SPACE_PUBLIC_BASE_URL`); `install_units.sh`/`local.env.example` erweitert; `oauth_smoke.py --base-url` (echtes Netz) | 7 | ✅ **Live-Abnahme abgeschlossen — 16/16 bestanden** (2026-07-30, Protokoll `docs/concepts/P4_ABNAHME_2026-07-29.md`). **[2026-07-30 Korrektur:** diese Zeile stand hier bis zu diesem Commit noch auf „12/16, 2026-07-29" — Zeile 9, 14/15 und der Schnitt liefen danach alle noch in derselben bzw. der Folgesession durch, ohne dass ein Zwischen-Commit diese Tabellenzeile nachzog. Dieselbe Drift-Kategorie, die Root-`CLAUDE.md` mehrfach dokumentiert (dort ist die Zeile explizit gegen genau dieses Vergessen abgesichert, diese Tabellenzeile hier bisher nicht).**]** | 21 neu: 9 `test_authctl.py` (neue Datei) + 5 neu in `test_authserver_store.py` + 3 neu in `test_units.py` (`phase3_edge/tests/`, davon 2 aus S1) + 4 neu in `test_oauth_smoke.py` |
| 8a | **Befund S1** (2026-07-29): `ALLOWED_HOSTS` ohne `127.0.0.1` machte Runbook-Schritt 4 unausführbar — `local.env.example` + `install_units.sh`-Warnung + Runbook korrigiert, kein Servercode geändert | 7 | ✅ | 2 neu in `test_units.py` (in Zeile 8 mitgezählt) |
| 8b | `phase4_auth/scripts/abnahme_run.sh` (2026-07-29) — automatisiert die acht maschinell prüfbaren Abnahmezeilen (1,2,3,10,11,12,13,16), spiegelt Aufbau/Redaktionsmuster von `phase3_edge/scripts/abnahme_run.sh` 1:1. Live gegen den echten Dienst probegelaufen (Zeilen 1/2/3/12 ok, 13/16 korrekt übersprungen, 10/11 korrekt übersprungen ohne echtes Passwort). Kein Ersatz für Zeilen 4–9/14/15 — eine curl-Nachbildung des Login-Formulars wäre eine zweite, ungetestete OAuth-Implementierung | 7 | ✅ | 0 (Runbook/Skript, gleiche Ausnahme wie `diagnose.sh`/`phase3_edge/scripts/abnahme_run.sh` — kein Unit-Test für ein Skript, das echten `systemd`/`journalctl`/Netzzugriff braucht) |
| 8c | **Live-Fund 2026-07-30:** `routes.py :: _security_headers()` — `form-action` trug nur `'self'`, Chromium prüft es aber auch gegen das Redirect-Ziel einer Formular-Antwort (hier: `302` nach `https://claude.ai/...`) und blockierte Fabians Verbindung lautlos nach jedem erfolgreichen Login. Fix: `config.py :: AuthSettings.csp_form_action` (neue Property, hält den Seam `test_redirect_uri_allowed_is_the_only_matching_path` intakt), `form-action 'self' https://claude.ai https://claude.com`. Deployt (`sudo systemctl restart`), Fabian erneut verbunden — **live bestätigt**: vollständiger Selbsttest aller sechs Tools (siehe Zeile 14/15 unten) | 7 | ✅ | 1 neu in `test_routes.py` |
| 8d | **Zeile 9 durchgeführt (2026-07-30):** `SPACE_OAUTH_ACCESS_TTL_S=60` via systemd-Drop-in, Connector neu verbunden, `create_item` → 90s Pause → `append_to_item`. DB-Gegenprobe (Claude Code, read-only): 14 `access_tokens`-Zeilen derselben `family_id`, Refresh **on-demand** exakt beim ersten Aufruf nach Ablauf, kein Hintergrund-Timer, kein neuer Login | 7 | ✅ | 0 (Live-Test, kein Code) |
| 8e | **Schnitt vollzogen (2026-07-30, Runbook-Schritt 8):** Nikinger führte `SPACE_AUTH_MODE=oauth`/`install_units.sh`/Restart/beide `--revoke`/`spaces.cred` neu/zweiter Restart live aus — **vor** jeder Code-Änderung (Plan-Reihenfolge). Claude Code verifizierte read-only (`systemctl cat` → `oauth`, `export_space_map.py` → 0 Einträge, alte Pfad-Token-URL → `401`, `/health` → `200`) und entfernte danach `TokenPathASGI`/`AuthModeASGI` aus `mcpserver/asgi.py`/`app.py` (`resolver`-Parameter aus `create_app()` entfällt mit), reduzierte `SPACE_AUTH_MODE` auf `_VALID_MODES=("oauth",)` (Plan-Wortlaut „zwei Werte" war ungenau, siehe `authserver/config.py`), entfernte `serve.py`s Step-6b-Gate (`oauth` jetzt Pflicht) — beide Nikinger-Entscheidungs-Reversierungen vorab per `AskUserQuestion` abgestimmt. **Zeile 16 damit live bestanden, 16/16, Phase 4 ✅.** | 7 | ✅ | 347 gesamt (vorher 353) — `test_asgi.py` gelöscht, `test_asgi_bearer.py` 14→10, `test_serve.py` neu (+2), restliche Dateien auf Bearer-Fixtures umgestellt |

**Steps 0–6a (Details für die Tabellenzeilen 1–7a oben) sind komprimiert und nach
`SESSIONS_ARCHIVE.md` verschoben** (2026-07-31, gleiche Rotationslogik wie
`scripts/rotate_session_block.sh`s Session-Blöcke — verbatim verschoben, nicht neu
zusammengefasst; Reassemblierung gegen den Originalstand geprüft). Diese Zeilen waren laut
eigener Notiz seit Step 6a „settled, testgepinnt, nicht mehr Arbeitskontext" — Grund für den
Nikinger-Auftrag, den Kopf unter den 40KB-Softcap zu bringen (siehe Session-Block unten, Fund
„44KB-Softcap"). Steps 7/7a–8e (die aktuell relevanten) bleiben unverändert oben in der Tabelle
und unten im Runbook/Session-Block.

## Geerbte Contracts

Aus P2 (`phase2_mcp/CLAUDE.md`, `docs/concepts/phase2_mcp_plan.md` §2/§3): sechs Tools,
Tool-Contract, Fehlerabbildung, `SpaceResolver` → `Principal`, `Permissions`-Seam. Aus P3
(`phase3_edge/CLAUDE.md`, `docs/concepts/phase3_edge_plan.md` §2/§3): Credential-Weg systemd →
Prozess, Request-Log-Format, Unit-Platzhalter-Mechanik. **Der Contract ist ab jetzt wieder zu** —
P4 ändert `asgi.py`/`app.py` (P4-Q). **[2026-07-28, Step 6a]:** `context.py` stand hier
ursprünglich mit auf der Änderungsliste (Plan §3.2 kündigt eine an) — real geändert wurde es
nicht, siehe Zeile 7a unten. P4 fasst `tools.py`/`permissions.py`/`auth.py` weiterhin nicht an.

## Runbook „Inbetriebnahme" (Step 7, live — führt der Nikinger aus, nicht Claude Code)

Claude Code liefert Code, Units und diese Befehlsfolge; alles, was den echten `DATA_ROOT`, den
echten Keyring, echte Nutzerakten/Token oder die Claude-Accounts berührt, führt der Nikinger
selbst aus (Plan §5 Step 7) — dieselbe Arbeitsteilung wie P3s „Inbetriebnahme"
(`phase3_edge/CLAUDE.md`). **Reihenfolge ist der halbe Runbook** (Plan-Wortlaut).

```
# 0) Vorbereitung — bereits erledigt (dieser Commit)
#    phase4_auth/systemd/sharefyx-mcp.service, install_units.sh + local.env.example erweitert,
#    authctl.py, oauth_smoke.py --base-url. local.env um AUTH_MODE=both, PUBLIC_BASE_URL
#    ergänzen (cp phase3_edge/local.env.example phase3_edge/local.env, falls noch nicht
#    geschehen — die sechs Werte eintragen).
#    [2026-07-29] ALLOWED_HOSTS MUSS 127.0.0.1 enthalten, sonst ist Schritt 4 unausführbar:
#    <node>.<tailnet>.ts.net,127.0.0.1 — siehe Befund S1 unten.

# 1) Nutzerakten provisionieren (TOTP-Seeds SOFORT in die Authenticator-Apps, QR aus der
#    otpauth://-URI — provision_user.py zeigt sie genau einmal)
python phase4_auth/scripts/provision_user.py --space niklas
python phase4_auth/scripts/provision_user.py --space fabian

# 2) Nutzerakten verschlüsselt bereitstellen — immer als Pipe, nie über eine Zwischendatei
#    (P3 §2.1, höherer Einsatz als bei spaces.cred: hier sind es echte TOTP-Seeds)
python phase4_auth/scripts/export_auth_users.py \
  | sudo systemd-creds encrypt --name=auth-users - /etc/sharefyx/auth-users.cred
sudo chmod 600 /etc/sharefyx/auth-users.cred

# 3) Units installieren, Dienst neu starten (AUTH_MODE=both aus local.env — Pfad-Token UND
#    Bearer laufen parallel, nichts fällt während der Abnahme aus)
sudo phase3_edge/scripts/install_units.sh
systemctl status sharefyx-mcp

# 4) oauth_smoke.py gegen den lokalen Port — BEVOR irgendjemand einen Connector anfasst
python phase4_auth/scripts/oauth_smoke.py --base-url http://127.0.0.1:8765 --space niklas
#    Fragt Passwort + TOTP-Seed interaktiv ab (getpass, nie als Argument). 11/11 erwartet.
#    Alle Prüfungen status=400 / "Invalid host header"? Dann fehlt 127.0.0.1 in der
#    SPACE_ALLOWED_HOSTS der INSTALLIERTEN Unit (systemctl cat sharefyx-mcp) — Befund S1:
#    local.env korrigieren, install_units.sh erneut, restart. Eine Änderung an local.env
#    allein wirkt nicht, die Unit unter /etc trägt den alten Wert bis zum Neu-Installieren.
#    [2026-07-29] Wurde provision_user.py zwischendurch erneut gelaufen (Passwort/TOTP neu)?
#    Dann vorher `sudo systemctl restart sharefyx-mcp` — die Nutzerakten werden EINMAL beim
#    Start gelesen (Befund O1). Gilt genauso für die Abnahmezeilen 6 und 7.

# 5) Discovery von außen — resource gegen die geplante Connector-URL halten
curl -s https://<node>.<tailnet>.ts.net/.well-known/oauth-protected-resource
curl -s https://<node>.<tailnet>.ts.net/.well-known/oauth-authorization-server

# 6) Connector in BEIDEN Accounts neu anlegen: https://<node>.<tailnet>.ts.net/mcp
#    Ohne Client-ID, ohne Secret. Connect -> Passwort + TOTP -> Consent.

# 7) Abnahmematrix fahren (unten) — Protokoll nach P2/P3-Konvention, mit Belegen statt
#    Behauptungen. docs/concepts/P4_ABNAHME_<Datum>.md erst NACH diesem Schritt schreiben
#    (ein Ergebnis-Protokoll für eine Matrix, die noch nicht gelaufen ist, wäre ein
#    fabriziertes Protokoll — Advisor-Vorgabe dieser Session).
#    [2026-07-29] phase4_auth/scripts/abnahme_run.sh deckt die acht maschinell prüfbaren
#    Zeilen ab (1,2,3,10,11,12,13,16 — Zeile 16 erst nach Schritt 8 sinnvoll) und schreibt
#    einen redigierten, einreichbaren CLI-Ausschnitt:
export SHAREFYX_HOST=savefyx-vmware-virtual-platform.tail89fc2a.ts.net
phase4_auth/scripts/abnahme_run.sh start      # vor den manuellen Zeilen 4–9
#    ... Zeilen 4–9 im echten Connector fahren (Notizen mitschreiben) ...
phase4_auth/scripts/abnahme_run.sh run  | tee ~/sharefyx-p4-abnahme-<Datum>.txt
#    Ausgabe liegt bewusst AUSSERHALB des Repos (~/, nicht docs/) — dieselbe Lehre wie der
#    Screenshot-Vorfall in P2 (phase2_mcp/CLAUDE.md): erst nach Sichtprüfung ohne jedes
#    Geheimnis in docs/concepts/P4_ABNAHME_<Datum>.md übernehmen.

# 8) Schnitt (NICHT auf einen Termin warten — Plan-Wortlaut: „ein both-Modus, der auf einen
#    Termin wartet, ist genau das Risiko, dessentwegen P4 vorgezogen wurde")
#    AUTH_MODE=oauth in local.env, install_units.sh erneut, restart.
python phase2_mcp/scripts/issue_token.py --revoke niklas
python phase2_mcp/scripts/issue_token.py --revoke fabian
python phase3_edge/scripts/export_space_map.py \
  | sudo systemd-creds encrypt --name=spaces - /etc/sharefyx/spaces.cred
sudo systemctl restart sharefyx-mcp
#    Danach TokenPathASGI/AuthModeASGI aus dem Code entfernen, SPACE_AUTH_MODE auf einen Wert
#    reduzieren — Codeentfernung IM SELBEN COMMIT wie die Abnahme (Plan-Wortlaut sagte "zwei
#    Werte", das war ohne frischen Repo-Zugriff geschrieben und ungenau: nur "oauth" hat nach
#    der vollen TokenPathASGI-Entfernung noch eine Implementierung, siehe authserver/config.py).
```

**Vollzogen, 2026-07-30 — dieser Schritt ist erledigt, kein offener Runbook-Punkt mehr.** Der
Nikinger führte die obige Befehlsfolge live aus; Claude Code verifizierte read-only
(`systemctl cat`, `export_space_map.py`, `curl` gegen die alte Pfad-Token-URL) und entfernte
danach `TokenPathASGI`/`AuthModeASGI` im selben Commit wie diese Doku-Aktualisierung. Details:
Modul-Status Zeile 8e oben, Session-Block unten.

**Fund, nicht behoben (Advisor, zweiter Durchlauf dieser Session):** `spaces.cred` und der
`export_space_map.py`-Schritt oben sind seit der Entfernung von `TokenPathASGI` **totes
Gewicht** — `serve.py` liest die Space-Map nicht mehr, aber die installierte Unit trägt
weiterhin `LoadCredentialEncrypted=spaces:/etc/sharefyx/spaces.cred` und verweigert den Start,
wenn diese Datei fehlt. Wer sie als „obsoletes P2-Überbleibsel" aufräumt, bricht den Dienst.
**Bewusst nicht angefasst** — die Unit-Datei zu ändern braucht `install_units.sh` + Restart
(Nikinger-Aktion, nicht Teil dieses Commits) und `phase3_edge/scripts/issue_token.py`/
`export_space_map.py`/`credentials.py` bleiben ohnehin außerhalb des P4-Q-Berührungsbereichs
(siehe Modul-Status Zeile 8e). Vorgemerkt für den nächsten Unit-Umbau, kein akuter Blocker.

**`authctl.py` braucht `STATE_DIRECTORY`, außerhalb von systemd nicht automatisch gesetzt**
(live gefunden, 2026-07-29): `config.py :: resolve_db_path()` verweigert bewusst einen stillen
Fallback ins Arbeitsverzeichnis — jeder `authctl.py`-Aufruf aus einer interaktiven Shell (nicht
nur `unlock`, auch `list-clients`/`list-tokens`/`revoke`/`purge-expired`) braucht:
```
STATE_DIRECTORY=/var/lib/sharefyx python phase4_auth/scripts/authctl.py <befehl> …
```
Kein `sudo` nötig — `/var/lib/sharefyx` gehört `savefyx`. Innerhalb des Dienstes exportiert
systemd `$STATE_DIRECTORY` selbst (`StateDirectory=sharefyx`), deshalb tauchte das in keinem
Test auf (`test_authctl.py` setzt `SPACE_AUTH_DB` direkt).

**Anleitung Zeile 9** (Access-Token-Ablauf, Claude refresht selbständig): über einen
systemd-Drop-in, nicht `local.env`/`install_units.sh` — Wegwerf-Testwert, eine Zeile zum
Entfernen statt ein Diff in einer getrackten Datei.

```
# 1) Kurze TTL (60s: reicht für eine Nachricht, kurz genug zum Abwarten)
sudo mkdir -p /etc/systemd/system/sharefyx-mcp.service.d
printf '[Service]\nEnvironment=SPACE_OAUTH_ACCESS_TTL_S=60\n' \
  | sudo tee /etc/systemd/system/sharefyx-mcp.service.d/override.conf
sudo systemctl daemon-reload && sudo systemctl restart sharefyx-mcp

# 2) Gegenprüfen, nicht behaupten
systemctl cat sharefyx-mcp | grep SPACE_OAUTH_ACCESS_TTL_S

# 3) WICHTIG: ein bereits verbundener Connector hält noch ein Token mit ALTER 1h-TTL — der
#    Neustart setzt dessen Ablauf nicht zurück. Connector einmal trennen und neu verbinden
#    (oder Reconnect, falls angeboten), damit ein Token unter der 60s-TTL entsteht.

# 4) ~90s warten, dann im SELBEN Chat einen weiteren Tool-Aufruf (z.B. list_spaces) —
#    kein neuer Connect, kein Consent-Screen. Soll einfach funktionieren.

# 5) Danach Override entfernen, sonst laufen echte Sessions dauerhaft mit 60s-Tokens
sudo rm /etc/systemd/system/sharefyx-mcp.service.d/override.conf
sudo systemctl daemon-reload
sudo systemctl restart sharefyx-mcp
```

**Beleg, nicht Gefühl:** danach gegenprüfen (Claude Code) — Journal zwischen Schritt 3/4 zeigt
ein zweites `"stage":"token"`, **ohne** neuen `authorize_get`/`authorize_post` davor (sonst
Login statt Refresh). `auth.sqlite3` read-only: dieselbe `family_id`, mehrere `access_tokens`
mit späteren `created_at`.

**`429 rate_limited` beim Neuverbinden?** DCR-Bremse ist global, 20/h (Plan §2.7) — nach dem
vielen Testen heute ggf. ausgereizt. Bis zur nächsten vollen Stunde warten, kein Bug.

**Stand 2026-07-30: 16 von 16 live bestanden — Schnitt vollzogen, Phase 4 ✅.** Protokoll mit
Belegen: `../docs/concepts/P4_ABNAHME_2026-07-29.md` (drei Nachträge 2026-07-30: Zeilen 14/15,
Zeile 9, Schnitt+Zeile 16).

**Abnahmematrix** (16 Zeilen, Protokoll nach P2/P3-Konvention — Belege statt Behauptungen).
**Stand 2026-07-30: alle 16 Zeilen live bestanden**, Belege je Zeile in
`../docs/concepts/P4_ABNAHME_2026-07-29.md`:

| # | Prüfung | Erwartung | Braucht Fabian |
|---|---|---|---|
| 1 | `/health` von außen | unverändert, unauthentifiziert | nein |
| 2 | `POST /mcp` ohne Token | **401** mit korrektem `WWW-Authenticate` | nein |
| 3 | Discovery von außen | beide `.well-known` liefern, `resource` exakt | nein |
| 4 | Connect `niklas` | DCR → Consent → Tool-Aufruf erfolgreich | nein |
| 5 | Falsches Passwort | generische Meldung, keine Enumeration | nein |
| 6 | Fünf Fehlversuche | Sperre greift, `authctl.py unlock --space niklas` hebt sie | nein |
| 7 | Falscher TOTP-Code | Fehlschlag; korrekter Code danach erfolgreich | nein |
| 8 | TOTP-Replay | derselbe Code ein zweites Mal → Fehlschlag | nein |
| 9 | Access-Token-Ablauf | TTL kurz setzen, Claude refresht selbständig | nein |
| 10 | Refresh-Replay | `oauth_smoke.py` → `invalid_grant`, Familie tot | nein |
| 11 | Code-Replay | `oauth_smoke.py` → `invalid_grant`, Familie tot | nein |
| 12 | Fremdregistrierung | `redirect_uri` auf fremder Domain → abgelehnt | nein |
| 13 | Secret-Grep im journald | **leer** | nein |
| 14 | Connect `fabian` | eigener Space, eigener Login | **ja** |
| 15 | Cross-Space unter OAuth | fremder Body gewrappt, Schreibversuch `write_denied` | **ja** |
| 16 | Pfad-Token tot | alte URL → 401 | nein |

**Terminrisiko (Nikinger-Entscheidung 2026-07-28, im Plan gelockt):** Zeilen 14/15 brauchten
Fabian — ein Terminrisiko, das die Phase nicht blockieren sollte. 14/16 wurde am 2026-07-30
erreicht (🟡 code-complete), beide Zwei-Personen-Zeilen folgten in derselben Session (✅). Schritt
8 (Schnitt) wartete wie gefordert **nicht** auf einen Termin.

**Done when** (Plan §5 Step 7) — **alle Klauseln erfüllt, Step 7 ✅:** 16/16 bestanden, Schnitt
vollzogen, Pfad-Token widerrufen, `TokenPathASGI` entfernt, Protokoll geschrieben,
`ROADMAP.md`/`docs/INDEX.md`/Phase-Head nachgezogen.

## Sicherheits-Review 2026-07-29 — offene Befunde S2–S8

Vollständiges Dokument mit Fehlfällen, Fix-Skizzen und der Liste der **geprüften und in Ordnung
befundenen** Punkte: `../docs/concepts/P4_SECURITY_REVIEW_2026-07-29.md`. Kurzfassung:

| # | Befund | Schwere | Datei |
|---|---|---|---|
| S1 | `ALLOWED_HOSTS` ohne `127.0.0.1` → `400 Invalid host header` lokal, Runbook-Schritt 4 unausführbar | Blocker | `local.env` / `install_units.sh` — ✅ **behoben** |
| S2 | `refresh_token`-Grant prüft `client_id` nicht (RFC 6749 §6) | niedrig | `flows.py`, `store.py :: rotate_refresh` |
| S3 | Kein Audience-Check: `AccessTokenRecord.resource` wird nie gegen `settings.resource` geprüft | niedrig (heute) | `resolver.py` |
| S4 | `scope` wird beim Zugriff nie durchgesetzt | niedrig | `resolver.py` |
| S5 | `f"{redirect_uri}?{query}"` zerlegt einen Redirect mit vorhandenem Query | niedrig | `routes.py :: _authorize_response` |
| S6 | `record["pwd"]`/`record["totp"]` → `KeyError` → 500 bricht den „wirft nie"-Vertrag daneben | niedrig-mittel | `flows.py :: submit_consent` |
| S7 | Unbegrenztes Zeilenwachstum aus unauth. Eingabe, `purge_expired()` nur manuell (kein Timer) | niedrig-mittel | `store.py` |
| S8 | `sudo install_units.sh` sourced eine nutzerschreibbare Datei als root | sehr niedrig | `install_units.sh` |
| O1 | Nutzerakten werden **einmal beim Start** gelesen — Provisionierung wirkt erst nach Restart | Betriebsnotiz | `scripts/serve.py` |

**Keiner von S2–S8 ist gefixt.** Bewusst: die Abnahmematrix läuft als Nächstes gegen genau diesen
Code; eine Verhaltensänderung an `flows.py`/`store.py` davor hieße, dass die Matrix etwas anderes
abnimmt als das Reviewte. Reihenfolge entscheidet der Nikinger.

---

## Session stopped — 2026-07-30 (Schnitt vollzogen, 16/16, Phase 4 ✅ — TokenPathASGI entfernt)

**Für den nächsten, kalten Leser:** vorige Session endete mit 15/16, einzig der Schnitt
(Runbook-Schritt 8) stand aus. Diese Session begann nach einem Context-Compaction-Verlust — der
einzige erhaltene Rest war eine Notiz: „16/16 confirmed — SPACE_AUTH_MODE=oauth is live, and the
old path-token URL now returns 401". Auftrag laut CLAUDE.md-Root-Prompt: erst den echten
Plan-Wortlaut lesen statt aus der eigenen Runbook-Paraphrase zu arbeiten, dann handeln.

**Erster Schritt, vor jeder Code-Änderung: die 16/16-Prämisse selbst verifizieren, nicht aus dem
Kontext-Rest übernehmen.** `git status` stand auf `d06ced0` (15/16, Schnitt offen) — die Notiz
allein wäre laut Repo-eigener Lehre („eine Doku-Aussage über den Repo-Zustand ist erst wahr,
wenn `git status` sie bestätigt", `phase2_mcp/CLAUDE.md`) kein Beleg gewesen. Read-only
gegengeprüft: `systemctl cat sharefyx-mcp` → `SPACE_AUTH_MODE=oauth`,
`SPACE_PUBLIC_BASE_URL=https://savefyx-vmware-virtual-platform.tail89fc2a.ts.net`;
`export_space_map.py` → `0 Einträge` (beide Pfad-Token tot); `curl` gegen die alte
Pfad-Token-URL (`/mcp/<beliebig>`) → `401`; `/health` → `200`, `uptime_s` plausibel seit dem
Restart. Der Nikinger hatte Runbook-Schritt 8 also tatsächlich bereits live ausgeführt, **vor**
jeder Code-Änderung — genau die vom Plan verlangte Reihenfolge. **Zeile 16 damit live bestanden,
16/16.**

**Scope-Klärung vor dem Umbau, per `AskUserQuestion`:** der Plan-Satz „TokenPathASGI und
AuthModeASGI aus dem Code entfernen" hat einen größeren Blast Radius als der Runbook-Kommentar
nahelegt — `README.md`s Dev-Workflow, `phase2_mcp/scripts/mcp_smoke.py` und `serve.py`s
Step-6b-`SPACE_AUTH_MODE`-Gate (eine gelockte Nikinger-Entscheidung vom 2026-07-28) hängen alle
am `oauth=None`-Pfad, der mit `TokenPathASGI` verschwindet. Zwei Fragen dem Nikinger vorgelegt,
nicht angenommen: (1) vollen Rückbau inklusive Dev-Pfad, oder Dev-Pfad als bewusste Ausnahme
erhalten? (2) `SPACE_AUTH_MODE` auf einen Wert (`oauth`) oder zwei (Plan-Wortlaut, aber nach der
vollen Entfernung funktional unbegründet) reduzieren? Antwort: **voller Rückbau**, **ein Wert**.

**Umsetzung, ein Commit:**
- `phase2_mcp/mcpserver/asgi.py` — `TokenPathASGI`, `AuthModeASGI`, `_credential_from_path`,
  `_send_401` gelöscht. Nur `BearerAuthASGI` bleibt.
- `phase2_mcp/mcpserver/app.py` — `create_app()`: `resolver`-Parameter entfernt (diente nur dem
  Bau von `TokenPathASGI`), `oauth: OAuthConfig` jetzt ohne Default, die `if oauth is None`-Weiche
  entfällt, `Mount("/mcp")` bekommt `BearerAuthASGI` direkt.
- `phase4_auth/authserver/config.py` — `_VALID_MODES=("oauth",)`, `base_url` unconditional
  Pflicht (die `mode in ("oauth","both")`-Verzweigung war mit nur einem gültigen Wert tot).
- `phase2_mcp/scripts/serve.py` — Step-6b-Gate (`"SPACE_AUTH_MODE" in os.environ`) entfernt,
  `load_auth_settings()` läuft jetzt immer ungefangen.
- `phase2_mcp/scripts/mcp_smoke.py`, `phase4_auth/scripts/oauth_smoke.py`,
  `phase4_auth/tests/test_oauth_smoke.py`, `phase2_mcp/tests/test_app.py`,
  `phase2_mcp/tests/test_asgi_bearer.py`, `phase2_mcp/tests/test_request_log.py` — Pfad-Token-
  Fixtures (`KeyringTokenResolver`/`_FakePathResolver`/feste Token-Strings im Pfad) durch echte,
  gegen eine temporäre `AuthStore` gemintete Bearer-Token ersetzt (`create_family()` +
  `issue_token_pair()`, dasselbe Muster wie `test_asgi_bearer.py` es für P4 Step 6a schon nutzte).
  **`mcp_smoke.py` steht nicht auf P4-Qs Berührungsliste** (die nennt `scripts/serve.py`, nicht
  `scripts/mcp_smoke.py`) — dem Nikinger vorab per `AskUserQuestion` vorgelegt (Option nannte
  die Datei explizit), gewählt: „Voller Rückbau". Genehmigt, nicht stillschweigend erweitert.
- `phase2_mcp/tests/test_serve.py` (neu) — bisher deckte kein Test `serve.py :: main()`s
  Verdrahtung ab (Settings → `AuthSettings` → `create_app()` → `uvicorn.run()`), beide
  Smoke-Skripte bauen `create_app()` direkt und rufen `main()` nie auf. Ohne diesen Test wäre der
  nächste `systemctl restart sharefyx-mcp` der erste echte Test dieser Verdrahtung gewesen
  (Advisor-Fund, zweiter Durchlauf dieser Session). `uvicorn.run`/`load_users` gepatcht, nie der
  echte Keyring oder ein echter Port.
- `phase2_mcp/tests/test_asgi.py` gelöscht (testete ausschließlich `TokenPathASGI`).
  `test_asgi_bearer.py` um `_FakePathResolver`, `test_auth_mode_token_preserves_p2_behaviour`,
  `test_auth_mode_both_serves_bearer_and_path`, `test_default_auth_mode_is_oauth` und
  `test_six_tools_behave_identically_under_bearer_and_path_token` gekürzt (14→10) — die
  Bearer-vs-Pfad-Token-Vergleichstests hatten mit dem Wegfall der zweiten Seite keinen
  Vergleichspartner mehr; **bewusst dokumentiert entfernt**, kein stilles Verschwinden (Advisor-
  Vorgabe dieser Session).
- `phase4_auth/tests/test_authserver_config.py` —
  `test_load_auth_settings_token_mode_does_not_require_base_url` durch
  `test_load_auth_settings_rejects_token_mode_after_the_cut` ersetzt.
- `README.md`, `phase3_edge/local.env.example`, `phase4_auth/CLAUDE.md` (dieses Dokument),
  `context.py`/`asgi.py`/`app.py`-Docstrings — auf den Schnitt nachgezogen.

**Verifiziert, nicht nur behauptet:** `pytest -q` → **347/347 grün** (vorher 353 — die Differenz
ist die Nettosumme aus `test_asgi.py` [-4], `test_asgi_bearer.py` [14→10, -4] und dem neuen
`test_serve.py` [+2, Advisor-Fund im zweiten Durchlauf: `serve.py :: main()`s Verdrahtung war
bis dahin ungetestet — beide Smoke-Skripte bauen `create_app()` direkt und rufen `main()` nie
auf], keine neue Lücke). `git diff --stat` auf `tools.py`/`permissions.py`/`server.py`/`storage/`
→ **leer** (Akzeptanzkriterium §6.9). Zusätzlich real gelaufen, nicht nur `pytest` grün
behauptet:
`mcp_smoke.py --json` → 12/12 Checks grün gegen den vollen `create_app()`-Stack mit echten
Bearer-Token; `oauth_smoke.py` (In-Process-Default) → **11/11 Prüfungen grün** (Discovery, DCR,
Consent, Code-Tausch, echter Tool-Aufruf mit Bearer, Refresh, Refresh-Replay tötet die Familie,
zweite Authorize-Runde, Code-Replay tötet die Familie) — der volle OAuth-Fluss funktioniert nach
der Entfernung des `resolver`-Parameters unverändert.

**Ergebnis: 16 von 16 Abnahmezeilen live bestanden. Phase 4 ✅ — alle acht Steps (0–7)
abgeschlossen.** `ROADMAP.md`, `docs/INDEX.md`, Root-`CLAUDE.md` im selben Commit nachgezogen
(P4 auf ✅, R5 abschließend korrigiert, Hard Rule 1 um den TOTP-Seed-Satz ergänzt).
`phase2_mcp/CLAUDE.md`s Test-Zähl-Zeile ebenfalls nachgezogen (100→94, `test_asgi.py`
verschwunden, `test_asgi_bearer.py` 14→10, `test_serve.py` neu mit 2).

**Zweiter Advisor-Durchlauf dieser Session** (nach dem ersten Commit-Entwurf, vor dem
tatsächlichen Commit) fand vier weitere Punkte: `serve.py :: main()` war ungetestet (behoben,
`test_serve.py` oben), `test_mcp_requires_token` prüfte `401` ohne den `WWW-Authenticate`-Header
zu prüfen (ergänzt — genau das ist Abnahmezeile 2), `spaces.cred` wurde totes Gewicht (dokumentiert
oben im Runbook, nicht angefasst), `mcp_smoke.py` liegt außerhalb von P4-Qs Berührungsliste
(bereits vorab mit dem Nikinger abgestimmt, hier nur nachträglich in den Papierpfad
aufgenommen). Alle vier in diesem Commit behoben oder dokumentiert, keiner still liegen gelassen.

**Nachtrag 2026-07-31 — Stale-Doc-Sweep (Nikinger-Auftrag, vor dem Push):** ein zweiter Check
lief gezielt nach veralteten Doku-Aussagen, nicht nur nach fehlenden Statusupdates. Drei echte
Funde, alle Kommentar-/Docstring-only: `phase3_edge/CLAUDE.md`s Disconnected-Runbook behauptete
noch, der `400`-Fehler träfe nur „unter `SPACE_AUTH_MODE=both|oauth`" — seit dem Schnitt ist die
`TrustedHostMiddleware` unconditional aktiv, der Mode-Qualifier war gegenstandslos, korrigiert
(aktiv gelesenes Runbook, nicht nur historische Notiz). Gleicher Fund in
`phase3_edge/tests/test_units.py`s Docstring, korrigiert ohne Testlogik/Fixture-Daten
anzufassen. `phase2_mcp/mcpserver/credentials.py :: load_space_map()`s Docstring behauptete, der
laufende Dienst löse Token noch darüber auf (`auth.py :: KeyringTokenResolver`) — seit dem
Schnitt läuft die Live-Auflösung ausschließlich über `OAuthTokenResolver`/Bearer,
`load_space_map()` bleibt nur Bestandswerkzeug. `pytest -q` weiterhin grün. Commit `47d5bc4`.

**Zweiter Nachtrag 2026-07-31 — Kopf unter den 40KB-Softcap komprimiert (Nikinger-Auftrag):**
die Steps-0–6a-Detailnarrative (Tabellenzeilen 1–7a, seit Step 6a als „settled, nicht mehr
Arbeitskontext" markiert) ist **verbatim** nach `SESSIONS_ARCHIVE.md` verschoben — gleiche
Disziplin wie `scripts/rotate_session_block.sh`: nichts abgetippt, drei-Teile-Schnitt
(`sed -n`) gegen den Originalstand auf Byte-Identität geprüft, bevor beide Dateien geschrieben
wurden. Die Modul-Status-**Tabelle** (alle 16 Zeilen) bleibt vollständig im Kopf; nur die Prosa
darunter ist gewandert. `phase4_auth/CLAUDE.md`: 46862 B → 35202 B (unter dem Softcap).
`phase4_auth/SESSIONS_ARCHIVE.md`: 59395 B → 72546 B (L3, kein Cap). `docs/INDEX.md`s
Größenangaben im selben Commit nachgezogen. `pytest -q` unverändert grün — reine Doku-Bewegung,
keine Code-Zeile berührt.

**Nächster Schritt (konkret):** kein offener Code- oder Live-Punkt mehr in P4, der Kopf ist
wieder unter dem Softcap. Es fehlt nur noch der **formale** Phasenabschluss (Handover-Dokument
P4→P5, analog `PHASE3_CLOSEOUT_HANDOVER.md`) — laut `docs/PROMPTS.md` ein eigener Prompt im
Browser-Webchat, Sache des Nikingers. Dabei mitnehmen: `spaces.cred`/`export_space_map.py` aus
der P4-Unit entfernen (siehe Runbook-Fund oben). Phase 3 bleibt bei 🟡 stehen (nur Zeile 13,
Restore-Nachweis, fehlt) — unverändert durch diese Session, nicht Teil ihres Auftrags.

**Dritter Nachtrag, 2026-08-02 (P5 Step 0 A — Rückbau vollzogen, mehrere Stellen oben jetzt
historisch):** der formale Phasenabschluss ist erledigt (`docs/concepts/
PHASE4_CLOSEOUT_HANDOVER.md`, P5-Planungssession), und der „Fund, nicht behoben" oben
(`spaces.cred`/`export_space_map.py` als totes Gewicht) ist geschlossen: beide Skripte
(`phase2_mcp/scripts/issue_token.py`, `phase3_edge/scripts/export_space_map.py`) sind gelöscht,
die `LoadCredentialEncrypted=spaces:…`-Zeile ist aus der Unit entfernt, `credentials.py` ist auf
`hash_token()` reduziert (`auth.py :: KeyringTokenResolver` mit entfernt). Konsequenz für diesen
Kopf: **die Runbook-Schritte 3/4 im „Schnitt"-Codeblock oben** (`issue_token.py --revoke`,
`export_space_map.py | systemd-creds encrypt`) beschreiben ausschließlich, was am 2026-07-30
tatsächlich lief — nicht mehr, was heute ausführbar wäre, beide Skripte existieren nicht mehr.
Ebenso ist die Aussage „`load_space_map()` bleibt nur Bestandswerkzeug" (Nachtrag oben) durch den
Rückbau überholt: die Funktion selbst ist entfernt, nicht nur ihr Docstring korrigiert. Beide
Stellen bleiben als historischer Nachweis stehen (Prinzip wie im Rest dieses Kopfs: Session-Blöcke
werden nicht rückwirkend umgeschrieben), diese Notiz macht die Drift nachvollziehbar. Details,
Testzahlen und die (noch offene) Nikinger-Aktion A.7: `phase5_ui/CLAUDE.md` Session-Block
2026-08-02.

