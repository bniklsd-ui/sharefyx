---
status: snapshot
purpose: Sicherheits-Review des P4-Auth-Bündels + P3-Betriebsschicht, Stand 2026-07-29 (Step 7, vor der Live-Abnahme)
read-when: vor dem Fixen eines der Befunde S1–S8, oder wenn jemand wissen will, was schon geprüft und für in Ordnung befunden wurde
detail: L3
up: ../../phase4_auth/CLAUDE.md
down:
  - ./phase4_auth_plan.md
  - ../../phase4_auth/CLAUDE.md
updated: 2026-07-29
---

# Sicherheits-Review Phase 3 + 4 — 2026-07-29

**Auftrag des Nikingers:** „deeply review and inspect the current code, especially phase 3 and 4,
because it's about security, and I have the suspicion there's some underlying issue here."
Anlass war der fehlgeschlagene `oauth_smoke.py`-Lauf aus Runbook-Schritt 4 (4/4 Prüfungen
`status=400`).

**Ergebnis in einem Satz:** Der fehlgeschlagene Smoke-Test war **kein** Sicherheitsloch, sondern
ein Konfigurations-/Runbook-Defekt (S1, in diesem Commit behoben). Beim vollständigen Durchgang
durch `authserver/` und die P3-Betriebsschicht wurde **keine Umgehung der Authentifizierung, kein
Cross-Space-Leck und kein Secret-Leak** gefunden. Es bleiben sieben kleinere Befunde (S2–S8),
davon drei Spec-Abweichungen, ein Robustheitsfehler und zwei Ressourcen-Erschöpfungspfade.

**Keiner der Befunde S2–S8 wurde in diesem Commit gefixt.** Begründung: der Nikinger steht
mitten im Step-7-Runbook und fährt als Nächstes die 16-zeilige Abnahmematrix gegen genau diesen
Code. Eine Verhaltensänderung an `flows.py`/`store.py` jetzt hieße, dass die Matrix etwas anderes
abnimmt als das hier Reviewte. Was vor und was nach der Abnahme gefixt wird, entscheidet der
Nikinger.

---

## S1 — Runbook-Schritt 4 ist mit der ausgelieferten Unit-Vorlage unausführbar ✅ behoben

**Schweregrad:** Blocker für Step 7 · kein Sicherheitsloch · **in diesem Commit behoben**

`mcpserver/app.py :: create_app()` legt, sobald `oauth is not None` und `hosts is not None`, ein
`TrustedHostMiddleware` mit `SPACE_ALLOWED_HOSTS` über die **Wurzel**-App (Zeile ~124). Die
installierte Unit trug `SPACE_ALLOWED_HOSTS=savefyx-vmware-virtual-platform.tail89fc2a.ts.net`
— ohne `127.0.0.1`. Damit beantwortet der Dienst **jede** Anfrage mit `Host: 127.0.0.1:8765` mit
`400 Invalid host header`, bevor irgendein Handler läuft: `/health`, beide `.well-known`-
Dokumente, `/oauth/*`, `/mcp`.

Runbook-Schritt 4 lautet aber genau `oauth_smoke.py --base-url http://127.0.0.1:8765`. Der
Schritt konnte nie funktionieren. Betroffen sind außerdem `diagnose.sh` Prüfung 2 und jedes
lokale `curl` auf `/health` — d. h. auch das P3-Disconnected-Runbook wäre unter `AUTH_MODE=both`
falsch abgebogen („Dienst läuft, antwortet aber nicht lokal" statt „Host-Header nicht erlaubt").

Beleg (live, Produktionsdienst, read-only):

```
curl -s -o /dev/null -w '%{http_code}' http://127.0.0.1:8765/.well-known/oauth-authorization-server
→ 400
curl -s -H 'Host: savefyx-vmware-virtual-platform.tail89fc2a.ts.net' \
     http://127.0.0.1:8765/.well-known/oauth-authorization-server
→ 200 {"issuer":"https://savefyx-vmware-virtual-platform.tail89fc2a.ts.net", …}
curl -s http://127.0.0.1:8765/health
→ "Invalid host header" (HTTP 400)
```

**Fix (kein Code am Server geändert):** `127.0.0.1` gehört in `ALLOWED_HOSTS`.
`local.env.example` sagt das jetzt mit Begründung, `install_units.sh` warnt (nicht-fatal) wenn es
fehlt und `AUTH_MODE != token`, zwei neue Tests in `phase3_edge/tests/test_units.py` decken beide
Richtungen ab, und das P4-Runbook nennt die Voraussetzung bei Schritt 3.

**Das schwächt den DNS-Rebinding-Schutz nicht.** Der Schutz wirkt gegen einen Browser, den ein
Angreifer auf eine Seite lockt, deren Domain auf `127.0.0.1` zeigt — dieser Browser sendet
`Host: evil.example`, nie `Host: 127.0.0.1`. Ein Eintrag `127.0.0.1` ändert daran nichts.

**Verifiziert, nicht nur behauptet:** eine zweite, wegwerfbare Serverinstanz (Port 8799, eigenes
`tmp`-`DATA_ROOT`, eigene `auth.sqlite3`, eigene Test-Nutzerakte über `CREDENTIALS_DIRECTORY` —
**nie** der echte `DATA_ROOT`, **nie** der echte Keyring) mit `SPACE_ALLOWED_HOSTS=127.0.0.1`
lieferte `oauth_smoke.py --base-url http://127.0.0.1:8799` → **11/11 grün**, inklusive
`tool_call_with_bearer`. Damit ist auch die zweite, unabhängige Host-Prüfung belegt: `hosts` geht
nicht nur an das Wurzel-`TrustedHostMiddleware`, sondern auch an FastMCPs eigenen
Rebinding-Schutz in `mcp.http_app(allowed_hosts=…)`. Beide akzeptieren die `host:port`-Form mit
Eintrag `127.0.0.1`; ein Fix, der nur die Discovery repariert und dann am Tool-Aufruf stirbt, ist
damit ausgeschlossen.

---

## S2 — `refresh_token`-Grant prüft die `client_id` nicht

**Schweregrad:** niedrig (Spec-Abweichung) · **Datei:** `authserver/flows.py :: issue_token()`,
`authserver/store.py :: rotate_refresh()`

`rotate_refresh()` joint ausschließlich über `refresh_tokens.token_hash` und die Familie; der
`client_id` der Familie wird nie mit dem `client_id` des Requests verglichen. `issue_token()`
nimmt `client_id` entgegen, benutzt es aber nur im `authorization_code`-Zweig. RFC 6749 §6 und
RFC 9700 verlangen für öffentliche Clients eine Client-Identifikation auch beim Refresh.

**Konkreter Fehlfall:** ein zweiter, per DCR registrierter Client, der irgendwie an ein
Refresh-Token gerät, kann es einlösen, obwohl es nicht seiner Registrierung gehört. Praktisch
gering: das Refresh-Token ist selbst ein 256-Bit-Zufallswert, wer es hat, hat ohnehin gewonnen —
aber es ist eine Abweichung in einem Server, dessen erklärter Zweck Spec-Treue ist.

**Fix-Skizze:** `rotate_refresh()` zusätzlich `client_id` entgegennehmen und gegen
`token_families.client_id` prüfen; Mismatch → `None` (→ `invalid_grant`, ununterscheidbar).
`issue_token()` reicht `client_id` durch und verlangt es auch im Refresh-Zweig.

## S3 — Kein Audience-Check bei der Bearer-Auflösung

**Schweregrad:** niedrig (heute theoretisch) · **Datei:** `authserver/resolver.py ::
OAuthTokenResolver.resolve()`

`AccessTokenRecord.resource` wird durchgängig gespeichert (`token_families.resource`,
`access_tokens.resource`), aber an keiner Stelle mit `settings.resource` verglichen. `resource`
wird beim `/oauth/authorize` geprüft (`invalid_target`) und dann nie wieder benutzt.

**Warum es heute nicht beißt:** es gibt genau eine Ressource (`<base_url>/mcp`). **Warum es
trotzdem zählt:** die RFC-8707-Bindung ist genau die Eigenschaft, die verhindert, dass ein Token
für Ressource A bei Ressource B funktioniert. Sobald ein zweiter Ressourcenpfad dazukommt (P5
Web-UI ist ein realistischer Kandidat), ist die Lücke echt — und dann steht der fehlende Check
nicht mehr in einem frischen Review.

**Fix-Skizze:** ein `expected_resource` in den `OAuthTokenResolver` injizieren und
`record.resource != expected_resource` → `ResolveError`.

## S4 — `scope` wird beim Zugriff nie durchgesetzt

**Schweregrad:** niedrig · **Datei:** `authserver/resolver.py`, `mcpserver/asgi.py ::
BearerAuthASGI`

`flows.SUPPORTED_SCOPES` gated den Autorisierungs-Request; der Wert landet in
`token_families.scope`/`access_tokens.scope` und wird in der Token-Antwort zurückgemeldet. Beim
tatsächlichen Zugriff auf `/mcp` prüft niemand ihn. Ein Token mit `scope="offline_access"`
(ohne `space`) bekommt vollen Tool-Zugriff.

**Fix-Skizze:** in `resolve()` `"space" in record.scope.split()` verlangen. Kostet drei Zeilen,
schließt die Lücke zwischen „wir dokumentieren Scopes" und „wir setzen Scopes durch".

## S5 — `redirect_uri` mit vorhandenem Query-String erzeugt eine kaputte URL

**Schweregrad:** niedrig (Korrektheit) · **Datei:** `authserver/routes.py ::
_authorize_response()`

`f"{result.redirect_uri}?{query}"` hängt bedingungslos ein `?` an. Ein registrierter Redirect
`https://claude.ai/cb?x=y` ergibt `https://claude.ai/cb?x=y?state=…&code=…` — der zweite `?`
wird Teil des Werts von `x`. `code`/`state` kommen zwar noch an, aber die Ziel-App sieht `x`
verfälscht. Kein Leck (das `?`-Anhängsel kann keinen Host wechseln), aber falsch.

**Fix-Skizze:** `urlsplit` + Query zusammenführen, oder minimal `"&" if urlsplit(uri).query else "?"`.

## S6 — Kaputte Nutzerakte → `KeyError` → HTTP 500 statt „Anmeldung fehlgeschlagen"

**Schweregrad:** niedrig-mittel (bricht eine Zusicherung, die der Code selbst aufstellt) ·
**Datei:** `authserver/flows.py :: submit_consent()`, Zeilen mit `record["pwd"]` / `record["totp"]`

`passwords.verify_password()` und `totp.verify()` tragen beide einen ausdrücklichen
„wirft nie"-Vertrag, ausdrücklich mit Enumerationsschutz begründet („ununterscheidbar von
außen", „500 statt Anmeldung fehlgeschlagen" steht wörtlich im `totp.py`-Docstring). Direkt
darüber greift `submit_consent()` mit `record["pwd"]` und `record["totp"]` per Index in ein
Dict, das aus einer JSON-Datei bzw. dem Keyring kommt. Fehlt ein Schlüssel — halb geschriebene
`auth-users.cred`, von Hand editierter Keyring-Eintrag, künftiges Feld-Rename — ist die Antwort
ein 500 statt der generischen Fehlermeldung. Ein 500 ausschließlich für existierende Spaces ist
genau das Enumerations-Orakel, das der umgebende Code verhindern soll.

**Fix-Skizze:** `record.get("pwd") or passwords.DUMMY_HASH`, `record.get("totp", "")` — `totp.verify`
gibt für ein ungültiges Base32 bereits `None` zurück, der Pfad ist also schon vorbereitet.

## S7 — Unbegrenztes Zeilenwachstum aus unauthentifizierter Eingabe, kein Purge-Timer

**Schweregrad:** niedrig-mittel (Disk-DoS auf einem öffentlich gefunnelten Endpunkt) ·
**Dateien:** `authserver/store.py :: upsert_login_attempt()`, `create_auth_request()`,
`purge_expired()`

Zwei Pfade, beide ohne Authentifizierung erreichbar:
1. `login_attempts` wird mit dem **vom Angreifer gewählten** `space`-String als PRIMARY KEY
   befüllt (`ratelimit.register_failure(space)` läuft auch für nicht existierende Spaces — das
   ist als Enumerationsschutz sogar so gewollt). Keine Existenzprüfung, keine Längenbegrenzung.
2. Jedes `GET /oauth/authorize` mit gültiger `client_id` legt eine `auth_requests`-Zeile an
   (TTL 600 s). Für `/oauth/register` gibt es eine Stundenbremse, für `/oauth/authorize` keine.

Was es festmacht: **`purge_expired()` läuft nur manuell** über `authctl.py`. Es gibt keinen
Timer dafür (die einzige installierte Timer-Unit ist `sharefyx-backup.timer`). Abgelaufene
Zeilen verschwinden also nie von selbst.

**Fix-Skizze:** entweder eine `sharefyx-purge.timer` analog zur Backup-Unit, oder
`purge_expired()` opportunistisch aus `create_auth_request()` heraus (z. B. 1 von N Aufrufen).
Zusätzlich eine Längen-/Zeichenobergrenze auf `space` vor `register_failure()`.

## S8 — `sudo install_units.sh` sourced eine nutzerschreibbare Datei als root

**Schweregrad:** sehr niedrig auf dieser Ein-Nutzer-VM · **Datei:**
`phase3_edge/scripts/install_units.sh`, `source "$LOCAL_ENV"`

`phase3_edge/local.env` gehört `savefyx` und wird von `install_units.sh` unter `sudo` als root
**ausgeführt** (`source`, nicht geparst). Alles, was als `savefyx` läuft, kann dort Code
hinterlegen, der beim nächsten `sudo phase3_edge/scripts/install_units.sh` als root läuft. Auf
einer VM, auf der `savefyx` ohnehin `sudo` hat, ist das keine Rechteausweitung — nur ein Muster,
das man kennen sollte, bevor die Datei jemals von einem anderen Konto beschreibbar wird.

**Fix-Skizze (optional):** statt `source` ein `grep`-basiertes Parsen der sechs `KEY=VALUE`-
Zeilen. Kostet Lesbarkeit, gewinnt eine Eigenschaft, die hier heute niemand braucht.

---

## O1 — Betriebsnotiz, kein Befund: Nutzerakten werden einmal beim Start gelesen

`scripts/serve.py` ruft `load_users()` **einmal** auf und übergibt das Ergebnis als
`OAuthConfig.users`; `flows.submit_consent()` bekommt genau diese Momentaufnahme. Ein
`provision_user.py`-Lauf (Passwort- oder TOTP-Wechsel) wirkt deshalb erst nach
`systemctl restart sharefyx-mcp` — genau wie `KeyringTokenResolver.reload()` es für die
Pfad-Token seit P2 dokumentiert, also kein neues Verhalten.

Es steht nur nirgends im Runbook. Relevant für Abnahmezeilen 6 und 7 (Sperre/TOTP): wer dort
zwischendurch eine Nutzerakte neu provisioniert und ohne Restart weitertestet, misst den alten
Stand. Ergänzt im P4-Runbook.

---

## Ausdrücklich geprüft und **in Ordnung** (verified negatives)

Diese Liste steht hier, damit ein späterer Leser sie nicht erneut prüfen muss — und damit
sichtbar ist, worauf sich das „kein Loch gefunden" oben stützt.

| # | Geprüft | Ergebnis |
|---|---|---|
| 1 | Läuft der Fail-Closed-Guard `assert_principal_matches_request()` auf dem echten Tool-Pfad, oder ist er nur definiert und getestet? | **Läuft.** `tools.py :: _authenticated_principal()` (Zeile 161) ruft ihn, und **alle sechs** Tools rufen `_authenticated_principal()` (Zeilen 199/253/303/340/378/427). Die Behauptung im `asgi.py`-Docstring („`context.py` brauchte keine Änderung") ist damit nicht vakuum-wahr, sondern belegt. |
| 2 | Redirect-Origin-Umgehung: `https://claude.ai@evil.example/cb` | Abgelehnt — `urlsplit().netloc` ist `claude.ai@evil.example`, nicht in der Allowlist. |
| 3 | Redirect-Origin-Umgehung: `https://claude.ai:443/cb` | Abgelehnt (strenger als nötig, aber sicher). |
| 4 | Redirect-Origin-Umgehung: Groß-/Kleinschreibung, `http://` statt `https://` | Beide abgelehnt. |
| 5 | Zweiter Vergleichspfad für Redirects irgendwo im Paket? | Nein — `redirect_uri_allowed()` ist die einzige Stelle, und `start_authorize()` prüft **zusätzlich** die Mitgliedschaft in der Registrierung. Eine später verschärfte Allowlist entwertet damit auch alte Registrierungen. |
| 6 | Login-CSRF auf `POST /oauth/authorize` | Kein praktischer Angriff: `request_id` ist ein `secrets.token_urlsafe(32)`, einmalig (`consume_auth_request()` markiert vor jeder Prüfung), und der Angreifer müsste zusätzlich Passwort **und** gültigen TOTP-Code des Opfers liefern. |
| 7 | PKCE: Downgrade auf `plain`, fehlende `code_challenge` | Beides abgelehnt (`code_challenge_method != "S256"` → `invalid_request`); Metadaten melden nur `S256`. |
| 8 | Fehlende Längenprüfung des `code_verifier` (RFC 7636: 43–128) | Formal eine Abweichung, praktisch wirkungslos — wer den Code abfängt, kennt den Verifier trotzdem nicht. Nicht als Befund gezählt. |
| 9 | Code-/Refresh-Replay (RFC 9700) | Korrekt: beides tötet die Familie in **einer** `BEGIN IMMEDIATE`-Transaktion, abgelaufen ≠ Replay. Live gegen die Wegwerf-Instanz bewiesen (`refresh_replay_kills_family`, `code_replay_kills_family`, jeweils `invalid_grant` + Folge-`401`). |
| 10 | TOTP-Replay | Zähler je Space persistiert, `verify()` überspringt `counter <= last_counter`, Hochsetzen erst nach **vollständigem** Erfolg (Passwort UND TOTP). |
| 11 | Enumeration über Antwortzeit bei nicht existierendem Space | Voller Argon2id-Verify gegen `DUMMY_HASH`; TOTP-Auslassung ist kein Orakel, weil Argon2id (t=8, ~55 ms) die HMAC-Prüfung um Größenordnungen dominiert. Ausnahme: S6. |
| 12 | Secrets im Log | `AccessLogASGI` loggt `path` **ohne** Query-String (`?code=…` kann gar nicht erst auftauchen), `OAuthLogASGI` liest weder Body noch Header, `log_event()` erzwingt eine Feld-Whitelist, `TokenScrubbingFilter` ist die dritte Schicht. Journal des laufenden Dienstes stichprobenartig gesichtet — nur `ev`-Zeilen mit Whitelist-Feldern. |
| 13 | DCR-Kontingent (20/h global) erschöpfbar durch Fremde | Ja — steht so im Plan §2.7 als bewusst akzeptierter grober Türstopper. Kein neuer Befund. |
| 14 | Kein Secret in einer Repo-Datei | `git ls-files` kennt `phase3_edge/local.env` nicht (gitignored), `*.sqlite3` gitignored, Unit-Vorlagen tragen nur Platzhalter (durch `test_unit_has_no_secret_shaped_value` abgesichert), `local.env` enthält nur Pfade + den öffentlichen Hostnamen. |
| 15 | `SPACE_HOST` weiterhin Loopback, kein offener Port | `ss -ltnp`: `127.0.0.1:8765` (Dienst) und Tailscale auf `:443` — kein `0.0.0.0`-Listener des Dienstes. |

---

## Was dieses Review **nicht** abgedeckt hat

- **Kein Live-Test gegen den echten `DATA_ROOT`, den echten Keyring oder die echten
  Nutzerakten.** Alle dynamischen Prüfungen liefen gegen eine Wegwerf-Instanz auf Port 8799 mit
  `tmp`-Verzeichnissen. Der Produktionsdienst wurde ausschließlich read-only angefasst (`curl
  /health`, `curl` auf Discovery, `systemctl status`, `journalctl`).
- **Keine Abnahmematrix.** Die 16 Zeilen aus dem P4-Runbook sind Sache des Nikingers und stehen
  weiterhin aus.
- **Kein `/code-review ultra`.** Der ist nutzergetriggert und abgerechnet; Claude Code kann ihn
  nicht selbst starten. Wenn der Nikinger eine zweite, unabhängige Meinung zu genau diesem Diff
  will, ist `/code-review ultra` der Weg — dieses Dokument ersetzt ihn nicht, es ist ein
  Einzel-Reviewer-Durchgang.
- **`storage/` (P1) und `tools.py` (P2)** wurden nur soweit gelesen, wie der Auth-Pfad sie
  berührt (Guard-Aufrufkette, Space-Bindung). Die Rule-4-Eigenschaft selbst ist durch P2s
  Testsuite und die P2-Adapter-Abnahme belegt, nicht durch dieses Review.
