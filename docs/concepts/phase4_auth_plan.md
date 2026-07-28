---
status: plan (ausführungsreif)
purpose: Phase 4 — OAuth 2.1 + DCR. Entscheidungen P4-A–P4-R gelockt, Steps 0–7 sequenziert, Namen fixiert, Sicherheitsparameter mit Quelle belegt. Direkt an Claude Code übergebbar.
read-when: Ausführung von Phase 4; NICHT bei Session-Start anderer Phasen
detail: L2
up: ../../phase4_auth/CLAUDE.md
down:
  - ./PHASE3_CLOSEOUT_HANDOVER.md          # Herkunft der offenen Entscheidungen 1–6, Doku-Drift, geerbte [VERIFY]
  - ./phase3_edge_plan.md                   # P3-A–P3-N: Unit, Credential-Weg, Request-Log, Berührungsfläche
  - ./phase2_mcp_plan.md                    # P2-A–P2-N: Seam SpaceResolver/Principal, Tool-Contract
updated: 2026-07-28
---
# Phase 4 — OAuth 2.1 + Dynamic Client Registration
## Implementierungsplan für Claude Code

> **Author:** Browser-Planungssession, 2026-07-28 (Nikinger + Claude).
> **Audience:** Claude Code. Der Plan ist ausführungsreif — Entscheidungen sind gelockt,
> Schritte sequenziert, Namen fixiert. **Nichts hier muss neu hergeleitet werden.**
>
> **Drift-Konvention:** Alles, was gegen den echten Repo-Stand, die VM, eine externe Bibliothek
> oder eine fremde API geprüft werden muss, ist **`[VERIFY]`** markiert — bei Ausführung
> verifizieren, nie als gesichert übernehmen. Register in §9.
>
> **Zu den Ankern — bitte lesen, bevor du Zeilennummern erwartest.** Die Planungssession hatte
> **keinen** frischen Repo-Zugriff. Die Kopien im Projektwissen waren nachweislich veraltet
> (`P3_ABNAHME_2026-07-27.md` lag als *unausgefülltes Template* vor, `README.md` und
> Root-`CLAUDE.md` mit Stand 2026-07-24). `ROADMAP.md` und `docs/INDEX.md` stammen aus dem
> Drive-Snapshot **2026-07-28 05:11**. Deshalb stehen hier ausschließlich **Funktions-Anker**
> (`datei.py :: funktion()`) und **wörtliche Suchstrings**. Trage die realen Zeilennummern beim
> ersten Lesen in deine Step-Notizen ein, **nicht** in diesen Plan.
>
> **Doc-Layers gilt:** jede neue `.md` bekommt eine L1-Header-Card und eine Zeile in
> `docs/INDEX.md` — **im selben Commit** (Hard Rule 8).

---

## §0 Mission, Scope, gelockte Entscheidungen

### 0.1 Mission

**Der Pfad-Token verschwindet.** Am Ende von P4 lautet die Connector-URL
`https://<host>/mcp` — ohne Geheimnis darin. Beide Nutzer melden sich über einen echten
OAuth-2.1-Autorisierungsfluss an, den dieser Server selbst betreibt: Discovery, dynamische
Client-Registrierung, PKCE, Consent, kurzlebige Access-Token, rotierende Refresh-Token.

**Bauprinzip-Erinnerung:** Der Server ist dumm. P4 enthält **keine AI**, keine neuen Tools,
keine Fachlogik. Wer hier `tools.py` anfasst, ist in der falschen Phase.

**Der eigentliche Härtetest der Phase ist nicht der erste erfolgreiche Login, sondern der
erste erfolgreiche *Fehlschlag*:** ein wiederverwendeter Refresh-Token muss die ganze
Token-Familie töten, ein zweimal eingelöster Authorization-Code muss die daraus entstandenen
Token widerrufen, und ein falsches Passwort darf nicht verraten, ob das Konto existiert.
Diese drei Fälle sind Akzeptanzkriterien, keine Kür.

### 0.2 Ehrliche Bilanz: was P4 kostet

Das gehört an den Anfang, nicht in die Risiken:

**P4 entfernt ein Geheimnis aus der URL und stellt dafür drei unauthentifizierte
Endpunkte plus ein Login-Formular ins öffentliche Internet.** Vorher gab es genau eine
Angriffsfläche mit 256 Bit Entropie. Nachher gibt es `/oauth/register`, `/oauth/authorize`,
`/oauth/token`, zwei `.well-known`-Dokumente und ein Passwortfeld hinter einem Hostnamen, der
in Certificate-Transparency-Logs steht.

Das ist trotzdem der richtige Tausch — aber nur, **weil** die Härtung mitgebaut wird:
Redirect-Origin-Allowlist auf der Registrierung (§2.6), Argon2id + TOTP am Login (§2.5),
Fehlversuchsbremse (§2.7), keine Nutzer-Enumeration, keine Secrets im Log. Ohne diese Teile
wäre P4 eine Verschlechterung. Wer einen davon "erstmal weglässt", hat die Phase nicht
verkleinert, sondern kaputt gemacht.

### 0.3 Was P4 als gegeben übernimmt (nicht neu herleiten)

| Was | Wo es im Wortlaut steht |
|---|---|
| Sechs Tools, Tool-Contract, Fehlerabbildung | `docs/concepts/phase2_mcp_plan.md` §3 |
| `SpaceResolver` → `Principal`, `Permissions`-Seam, Guard | `phase2_mcp/mcpserver/auth.py`, `permissions.py`, `context.py` |
| Transport-Layout (`/health` + `Mount("/mcp")`) | `phase2_mcp/mcpserver/app.py`, `asgi.py` |
| Credential-Weg systemd → Prozess | `phase3_edge_plan.md` §2, `mcpserver/credentials.py :: load_space_map()` |
| Request-Log-Format, Feld-Whitelist, `TokenScrubbingFilter` | `phase3_edge_plan.md` §3, `mcpserver/request_log.py` |
| Unit, Platzhalter-Mechanik, `install_units.sh`, `local.env` | `phase3_edge_plan.md` §2.1, P3-J |
| Rahmenentscheidungen R1–R6, Hard Rules 1–8 | Root-`CLAUDE.md` |

**Scope laut `ROADMAP.md`, Phase 4 — DRIN:** Protected Resource Metadata, Authorization Server,
Dynamic Client Registration, PKCE, Token-Rotation.
**DRAUSSEN:** REST/UI (P5), MCP-Revision 2026-07-28, `fastmcp` 4, D6, neue Tools, feingranulare
Lese-Rechte, Off-site-Backup, Monitoring.

### 0.4 Die Entscheidungen des Nikingers vom 2026-07-28

Sie sind der Grund, warum dieser Plan so aussieht, und stehen deshalb vor der Tabelle:

1. **Eigener Authorization Server, handgeschrieben.** Kein Upstream-IdP, kein
   `OAuthProxy`. R6 (Lerneffekt) schlägt Bequemlichkeit.
2. **Sicherheit nach belegbaren, aktuellen Standards** — nicht nach Gefühl. Jede
   Sicherheitsentscheidung in diesem Plan trägt eine Quelle (§0.5). Wo eine Empfehlung
   *nicht* umgesetzt wird, steht der Grund dabei, nicht das Schweigen.
3. **Zweiter Faktor ist DRIN.** TOTP nach RFC 6238, weil der Login öffentlich erreichbar ist
   und ein einzelnes Passwort der einzige Schutz vor Schreibzugriff auf beide Spaces wäre.
4. **Befristeter Parallelbetrieb**, kein harter Schnitt — mit Verfallsdatum innerhalb der Phase.
5. **Die Login-Oberfläche ist bewusst eine Wegwerf-UI.** Sie wird in P5 ersetzt, nicht
   erweitert. Das steht als Kommentar im Code, damit niemand sie später "schön macht".

### 0.5 Normative Grundlage (verifiziert am 2026-07-28)

Diese Quellen sind der Maßstab. Wer in diesem Plan eine Sicherheitsentscheidung ändern will,
argumentiert gegen sie — nicht gegen mich.

| Kürzel | Quelle | Woraus hier etwas folgt |
|---|---|---|
| **BSI TR-02102-1**, Version 2026-01 (Stand 23.01.2026) | Kryptographische Verfahren: Empfehlungen und Schlüssellängen | Argon2id als empfohlenes passwortbasiertes Ableitungsverfahren |
| **OWASP Password Storage Cheat Sheet** | cheatsheetseries.owasp.org | Argon2id **erste Wahl**: `m=19456 KiB, t=2, p=1` (oder `m=47104, t=1, p=1`); scrypt nur, *wenn Argon2id nicht verfügbar ist* — in CPython ist es verfügbar, also fällt scrypt weg |
| **RFC 9700** (Jan 2025), OAuth 2.0 Security BCP | Refresh-Token öffentlicher Clients MÜSSEN sender-constrained sein **oder** rotieren · exaktes Redirect-URI-Matching · Authorization-Code genau einmal, bei Zweiteinlösung **alle daraus entstandenen Token widerrufen** · Sender-Constraining (mTLS/DPoP) SOLLTE — siehe Restrisiko R3 |
| **RFC 7636** | PKCE | `S256` Pflicht, `plain` wird abgelehnt |
| **RFC 9728** | Protected Resource Metadata | Aufbau und Fundort des PRM-Dokuments |
| **RFC 8414** | Authorization Server Metadata | Aufbau und Fundort des AS-Dokuments |
| **RFC 7591** | Dynamic Client Registration | `/oauth/register`, `application_type` |
| **RFC 8707** | Resource Indicators | `resource`-Parameter, Audience-Bindung des Access-Tokens |
| **RFC 9207** | `iss` im Authorization Response | Mix-up-Schutz, Metadaten-Flag |
| **RFC 6238 / 4226** | TOTP / HOTP | Zweiter Faktor, inklusive der Testvektoren als Unit-Tests |
| **MCP-Auth-Spec 2025-11-25** | modelcontextprotocol.io | Zielrevision. Server ist OAuth-2.1-Resource-Server, PRM Pflicht, `WWW-Authenticate` auf 401 |
| **Anthropic Connector-Doku**, `claude.com/docs/connectors/building/authentication` | Client-Verhalten | Callback-URL, DCR, PKCE-S256, Timeouts, Content-Types, Refresh-Verhalten (§0.6) |

**Zur MCP-Revision 2026-07-28:** Sie wird am Tag dieser Planung final. Claude unterstützt laut
Anthropic-Doku die Auth-Specs **2025-03-26, 2025-06-18 und 2025-11-25** — die neue ist dort
(noch) nicht genannt. Die sechs Auth-SEPs der neuen Revision sind zudem überwiegend
*Client*-Pflichten (`iss` prüfen, `application_type` senden, Credentials an den Issuer binden).
Serverseitig folgt daraus genau eine Sache, und die ist in diesem Plan drin: **`iss` im
Authorization Response** (P4-K). **P4 bleibt auf 2025-11-25.**

### 0.6 Harte Client-Vorgaben aus der Anthropic-Doku

Diese Zahlen und Formen sind keine Empfehlungen, sondern Abnahmebedingungen. `[VERIFY]` V14 —
die Seite ändert sich schneller als dieses Repo, **vor Step 4 einmal nachlesen**.

| Vorgabe | Wert |
|---|---|
| Callback-URL der gehosteten Oberflächen | `https://claude.ai/api/mcp/auth_callback` |
| Registrierungsweg | DCR out of the box; CIMD nur, wenn die AS-Metadaten **beide** Flags `client_id_metadata_document_supported: true` **und** `"none"` in `token_endpoint_auth_methods_supported` tragen |
| PKCE | `code_challenge_method=S256` auf **jedem** Authorization-Request; Metadaten müssen `code_challenge_methods_supported: ["S256"]` führen |
| Auth-Auslöser | **Nur** ein Transport-Level-**401** mit `WWW-Authenticate`. Eine 200 mit `isError: true` erzeugt keinen Connect-Button, sondern Fließtext im Chat |
| PRM-Feld `resource` | muss **exakt** der URL entsprechen, die der Nutzer eingibt — inklusive Pfad |
| `authorization_servers` | Claude nimmt den **ersten** Eintrag und fällt nicht auf spätere zurück |
| Scope-Auswahl | `scope` im `WWW-Authenticate` gewinnt; sonst PRM-`scopes_supported`. `offline_access` wird **nur** angehängt, wenn die **AS**-Metadaten es in `scopes_supported` führen |
| Content-Types | `/oauth/token`: `application/x-www-form-urlencoded` · `/oauth/register`: `application/json` |
| Timeouts | 10 s für Discovery, Registrierung, Token · 30 s für Refresh |
| Refresh-Verhalten | reaktiv auf 401, proaktiv bis 5 min vor Ablauf; Fehlercode muss `invalid_grant` sein |
| Discovery-Cache | global, per URL, ~5 min Staleness — Metadatenänderungen wirken verzögert |
| Egress | Anthropic ruft aus `160.79.104.0/21` an |

### 0.7 Gelockte Entscheidungen (P4-A – P4-R)

| # | Thema | Festlegung |
|---|---|---|
| **A** | Authorization Server | **Eigener AS, im selben Prozess, als gewöhnliche Starlette-Routen.** Keine Delegation, kein `OAuthProxy`, **kein `auth=`-Parameter an `FastMCP`**. Begründung: der P2-Seam bleibt der einzige Ort, an dem Identität entsteht; ein Fehler im AS kann den MCP-Stack nicht von innen kompromittieren, weil der ihn nie sieht. |
| **B** | Verzeichnis & Paket | Verzeichnis **`phase4_auth/`** (ROADMAP), Paket **`authserver`** — **nicht** `auth`. Begründung: `mcpserver/auth.py` existiert seit P2; ein Top-Level-Paket `auth` daneben ist technisch zulässig und für Menschen und `grep` eine Falle. Abweichung von der ROADMAP wird dort **datiert korrigiert**, nicht still übergangen. |
| **C** | Abhängigkeitsrichtung | **`mcpserver` → `authserver`, niemals umgekehrt.** `authserver` kennt weder `storage` noch `mcpserver` noch FastMCP. Es kennt Starlette, SQLite und `argon2`. Damit ist der AS ohne den Rest des Projekts testbar. |
| **D** | Token-Format | **Opak.** `secrets.token_urlsafe(32)` (256 Bit), gespeichert wird ausschließlich `sha256`-Hex. Kein JWT, kein JWKS, kein Signing-Key. Begründung: bei **einem** Prozess, der AS und Resource Server zugleich ist, kauft JWT keine Eigenschaft, kostet aber Schlüsselverwaltung, eine Bibliothek und eine `alg`-Verwechslungsklasse. Opake Token sind sofort widerrufbar — JWTs sind es nicht. **`sha256` ist hier korrekt und nicht "zu schnell":** ein langsames KDF schützt vor *Raten*, und ein 256-Bit-Zufallswert ist nicht ratbar. Langsam wird nur das Passwort gehasht (P4-F). |
| **E** | Registrierung | **DCR (RFC 7591), kein CIMD.** Zwei Gründe, in dieser Reihenfolge: DCR ist **vollständig ohne Netz unit-testbar** (Hard Rule 7), CIMD verlangt einen ausgehenden HTTPS-Fetch mitten im `/authorize`-Handler. Und DCR ist bei Anthropic „out of the box". Dass die Draft-Spec DCR auf *MAY* zurückstuft und CIMD zum *SHOULD* macht, ist notiert — CIMD steht namentlich in §8 als Nachfolger. |
| **F** | Passwort-Hashing | **Argon2id über `argon2-cffi`**, Parameter als Modulkonstanten: `t=2`, `m=19456 KiB`, `p=1`, `hash_len=32`, `salt_len=16`. Quelle: OWASP + BSI TR-02102-1 (2026-01). **Bewusst *nicht* `hashlib.scrypt`**, obwohl das ohne neue Abhängigkeit ginge: OWASP nennt scrypt ausdrücklich für den Fall, *dass Argon2id nicht verfügbar ist*. In CPython ist es verfügbar. Eine Abhängigkeit ist der ehrlichere Preis als die zweitbeste Wahl. |
| **G** | Zweiter Faktor | **TOTP, RFC 6238**, 6 Stellen, 30 s Schritt, Toleranz **±1** Schritt, Secret 160 Bit Base32. Implementierung **stdlib** (`hmac`, `hashlib`, `struct`, `base64`) — die RFC-Testvektoren werden Unit-Tests. Default-Algorithmus **SHA-1**, weil Authenticator-Apps praktisch nur den beherrschen; `SHA256` ist konfigurierbar. **Ehrlich dazu:** HMAC-SHA-1 ist von den SHA-1-Kollisionsangriffen nicht betroffen, BSI TR-02102-1 würde SHA-256 vorziehen. Die Wahl ist Kompatibilität, kein Versehen, und steht so im Phase-Head. **Replay-Schutz:** der zuletzt akzeptierte Zähler wird je Space gespeichert; derselbe Code wird kein zweites Mal akzeptiert. |
| **H** | Wiederherstellung des 2. Faktors | **Keine Recovery-Codes.** Der Betreiber hat SSH; `provision_user.py` gibt einen neuen TOTP-Seed aus. Recovery-Codes wären ein zweiter, schwächerer Anmeldeweg für zwei Personen mit physischem Zugriff auf die Maschine — mehr Angriffsfläche als Nutzen. |
| **I** | Auth-Zustand | **Eigene SQLite unter `StateDirectory=sharefyx` → `/var/lib/sharefyx/auth.sqlite3`.** Enthält Clients, ausstehende Auth-Requests, Codes, Token-Familien, Access-/Refresh-Token, Fehlversuche, TOTP-Zähler — **alles Geheimnisartige nur als `sha256`-Hash**. **Hard Rule 2 gilt hier nicht:** diese Datenbank ist *autoritativ*, keine Ableitung aus Dateien. Das ist eine benannte Ausnahme, kein Regelbruch — sie berührt keine Nutzdaten. |
| **J** | Backup | Die Auth-SQLite kommt **nicht** ins `git bundle`. Konsequenz, dokumentiert statt entdeckt: nach einem Restore melden sich beide Nutzer einmal neu an. Begründung: Refresh-Token sind billig nachzuerzeugen und teuer zu verlieren; ein Backup davon wäre eine Kopie langlebiger Zugangsdaten auf einem zweiten Datenträger. |
| **K** | Fluss-Details | Authorization Code Flow mit PKCE **S256** (`plain` wird mit `invalid_request` abgelehnt). Öffentlicher Client, **kein** `client_secret`. Redirect-URI-Vergleich **exakt und byteweise** (RFC 9700), keine Wildcards, keine Präfixe, keine Port-Toleranz. **`iss` im Authorization Response** (RFC 9207) plus Metadaten-Flag `authorization_response_iss_parameter_supported: true`. `resource` (RFC 8707) wird angenommen, validiert und als Audience an den Access-Token gebunden. |
| **L** | Lebensdauern | Ausstehender Auth-Request **10 min** · Authorization-Code **60 s** · Access-Token **60 min** · Refresh-Token **30 Tage absolut**, bei jeder Nutzung rotiert. Alle vier als Env-Variablen mit diesen Defaults (§2.8), damit die Abnahme den Ablauf erzwingen kann, ohne zu warten. |
| **M** | Rotation & Familien | Jeder Code erzeugt eine **`family_id`**. Refresh rotiert innerhalb der Familie. **Zwei Tötungsregeln, beide aus RFC 9700:** (1) ein bereits eingelöster Authorization-Code, der erneut vorgelegt wird → **ganze Familie widerrufen**; (2) ein bereits rotierter Refresh-Token, der erneut vorgelegt wird → **ganze Familie widerrufen**. Antwort in beiden Fällen: `invalid_grant`, ohne Detail. |
| **N** | Migration | **`SPACE_AUTH_MODE ∈ {token, oauth, both}`, Default `oauth`.** `both` existiert ausschließlich während dieser Phase; **Step 7 setzt `oauth`, entfernt `TokenPathASGI` und widerruft beide Pfad-Token.** Abgesichert durch `test_default_auth_mode_is_oauth` **und** ein Akzeptanzkriterium, nicht durch einen Vorsatz. |
| **O** | Login-Oberfläche | **Zwei server-gerenderte HTML-Seiten** (Login+Consent in *einem* Formular, plus eine Fehlerseite), als Python-Strings in `templates.py`. Kein Framework, kein JS, kein CSS-Build, **keine Cookies und keine Session**. Der Auth-Request lebt als Zeile in der Datenbank, das Formular trägt nur eine zufällige, einmal gültige `request_id`. Modul-Docstring: *„Wegwerf-UI. Wird in P5 ersetzt, nicht erweitert."* |
| **P** | Härtung | `TrustedHostMiddleware` auf der **Wurzel**-App (sie trägt ab jetzt öffentliche Auth-Routen, bisher schützte `allowed_hosts` nur die FastMCP-App). Sicherheits-Header auf allen HTML- und Metadaten-Antworten (§2.6). Redirect-Origin-Allowlist auf `/oauth/register`. Fehlversuchsbremse am Login (§2.7). Einheitliche Fehlermeldung ohne Nutzer-Enumeration. |
| **Q** | Berührungsfläche | P4 darf in `phase2_mcp/` **genau anfassen**: `mcpserver/asgi.py`, `mcpserver/context.py`, `mcpserver/app.py`, `mcpserver/config.py`, `mcpserver/request_log.py`, `mcpserver/logging_setup.py`, `scripts/serve.py`. **Nicht** anfassen: `tools.py`, `permissions.py`, `server.py`, `auth.py` (das Protokoll bleibt, die neue Implementierung lebt in `authserver`), `credentials.py`, `storage/*`. Ein Änderungsbedarf dort ist ein Befund für den Nikinger, keine Aufgabe. |
| **R** | Bibliotheks-Pins | **`fastmcp==3.4.4` bleibt exakt** (P3-D unverändert). Neu: **`argon2-cffi>=25,<26`** `[VERIFY]` V15 — aktuelle Major bei Ausführung prüfen und **exakt** pinnen, nicht als Range committen. Sonst **keine** neuen Laufzeitabhängigkeiten: kein `authlib`, kein `pyjwt`, kein `jinja2`, kein `itsdangerous`. |

**Zu P4-Q, weil es beim Bauen juckt:** Der neue Auflösungspfad (`Authorization`-Header →
`Principal`) entsteht in `asgi.py`, **nicht** in `auth.py`. Das `SpaceResolver`-Protokoll aus P2
bleibt Wort für Wort stehen — genau dafür wurde es gebaut. Die neue Implementierung heißt
`authserver.resolver :: OAuthTokenResolver` und erfüllt es.

---

## §1 Architektur

### 1.1 Der Weg eines Requests nach P4

```
Claude (Web/Desktop/Mobile) in zwei Accounts
   │  1. POST https://<host>/mcp            (ohne Token)
   │  ◄─ 401 + WWW-Authenticate: Bearer resource_metadata="…", scope="space"
   │  2. GET  /.well-known/oauth-protected-resource/mcp     → authorization_servers
   │  3. GET  /.well-known/oauth-authorization-server       → Endpunkte
   │  4. POST /oauth/register                               → client_id            (DCR)
   │  5. Browser → GET/POST /oauth/authorize                → code                 (PKCE, TOTP)
   │  6. POST /oauth/token                                  → access + refresh
   │  7. POST https://<host>/mcp  Authorization: Bearer …
   ▼
Tailscale-Funnel-Relay          — leitet weiter, entschlüsselt NICHT (P3 §0.4)
   ▼
tailscaled auf der VM           — TLS-Terminierung hier
   │  http://127.0.0.1:8765/…
   ▼
AccessLogASGI                              mcpserver/request_log.py   (P3, unverändert)
   ▼
TrustedHostMiddleware                      ← NEU in P4
   ▼
Starlette-Wurzel-App                       mcpserver/app.py
   ├── GET  /health                        → status, service, version, uptime_s   (unverändert)
   ├── GET  /.well-known/oauth-*           → authserver.routes                    ← NEU
   ├── POST /oauth/{register,authorize,token}
   │        GET  /oauth/authorize          → authserver.routes                    ← NEU
   └── Mount("/mcp") → AuthModeASGI                                               ← NEU
                          ├── BearerAuthASGI   (mode=oauth|both, Pfad leer)       ← NEU
                          │      └── authserver.resolver :: OAuthTokenResolver
                          └── TokenPathASGI    (mode=token|both, Pfad ≠ leer)     (P2, entfällt in Step 7)
                                 ▼
                          Principal in ContextVar     mcpserver/context.py
                                 ▼
                          FastMCP-App (stateless, ohne auth=)
                                 ├── ToolCallLogMiddleware        (P3, unverändert)
                                 └── Tools                        (P2, unverändert)
                                        ▼
                                   storage.Store                  (P1, unverändert)
```

**Alles unterhalb des `Principal` ist in dieser Phase read-only Betrachtungsgegenstand.**
Das ist die Zusage, die P2 mit dem Seam gegeben hat, und P4 ist der Termin, an dem sie fällig
wird. Wenn beim Bauen doch `tools.py` aufgeht, ist der Seam gebrochen — dann **stoppen und
melden**, nicht reparieren.

### 1.2 Was P4 anlegt

```
phase4_auth/
  CLAUDE.md                     # Phase-Head, L1-Card, Modultabelle, Runbooks
  SESSIONS_ARCHIVE.md           # leer angelegt, L1-Card, newest-first-Hinweis
  pyproject.toml                # Paket "authserver", Abhängigkeit argon2-cffi
  authserver/
    __init__.py
    config.py                   # AuthSettings aus Umgebung
    models.py                   # frozen dataclasses, keine Logik
    crypto.py                   # Token erzeugen/hashen, konstantzeitiger Vergleich, PKCE
    passwords.py                # Argon2id: hash_password(), verify_password(), needs_rehash()
    totp.py                     # RFC 6238, stdlib
    users.py                    # Nutzerakte aus systemd-Credential / Keyring
    store.py                    # SQLite: Schema, Migration, alle Abfragen
    ratelimit.py                # Fehlversuchsbremse, now_fn injiziert
    metadata.py                 # PRM- und AS-Metadatendokumente
    clients.py                  # DCR (RFC 7591), Redirect-Origin-Allowlist
    flows.py                    # authorize / consent / token / refresh — die Zustandslogik
    templates.py                # zwei HTML-Seiten, Sicherheits-Header      (Wegwerf-UI)
    errors.py                   # OAuth-Fehlerantworten, einheitlich
    routes.py                   # Starlette-Routen, dünn: parsen → flows → antworten
    resolver.py                 # OAuthTokenResolver — erfüllt mcpserver.auth.SpaceResolver
  scripts/
    provision_user.py           # Passwort setzen, TOTP-Seed erzeugen, otpauth://-URI EINMAL zeigen
    export_auth_users.py        # JSON auf stdout für systemd-creds (Gegenstück zu export_space_map.py)
    authctl.py                  # list-clients | list-tokens | revoke | unlock | purge-expired
    oauth_smoke.py              # End-to-End ohne Browser — der Beweis dieser Phase
  systemd/
    sharefyx-mcp.service        # ERSETZT die P3-Fassung: StateDirectory, zweites Credential
  tests/
    __init__.py
    test_crypto.py  test_passwords.py  test_totp.py  test_users.py
    test_store.py   test_ratelimit.py  test_metadata.py  test_clients.py
    test_flows.py   test_routes.py     test_templates.py  test_resolver.py

phase2_mcp/mcpserver/
    asgi.py                     # GEÄNDERT: BearerAuthASGI + AuthModeASGI
    context.py                  # GEÄNDERT: Guard vergleicht Bearer statt Pfadsegment
    app.py, config.py           # GEÄNDERT: Routen mounten, neue Settings
    request_log.py              # GEÄNDERT: ev="oauth"
    logging_setup.py            # GEÄNDERT: Scrubbing erweitert
phase2_mcp/tests/
    test_asgi_bearer.py         # NEU
```

**`phase4_auth/` ist — anders als `phase3_edge/` — wieder ein Python-Paket.** Es enthält
Servercode, der eigenständig testbar sein soll. `scripts/dev_install.sh` findet es über die
`pyproject.toml` automatisch; **nichts an `dev_install.sh` ändern** `[VERIFY]` V16.

### 1.3 Abhängigkeitsrichtung (strikt, wird getestet)

```
storage   ←   mcpserver   →   authserver
                                  │
                             argon2, sqlite3, starlette
```

`authserver` importiert **nichts** aus `mcpserver` oder `storage`. Das ist kein Stilwunsch:
es ist die Bedingung dafür, dass der AS in `phase4_auth/tests/` ohne `DATA_ROOT`, ohne Keyring
und ohne FastMCP läuft. Test dazu: `test_authserver_does_not_import_mcpserver` — durchsucht die
Modulquellen nach `mcpserver`/`storage`-Importen.

Die eine Ausnahme ist `resolver.py`: es **erfüllt** `mcpserver.auth.SpaceResolver`, ohne es zu
importieren (strukturelles `Protocol`, kein Vererbungszwang) und gibt ein Objekt mit den
Feldern `space` und `token_hash` zurück. Die Konstruktion des echten `Principal` passiert in
`mcpserver/asgi.py`. Damit bleibt die Richtung sauber.

---

## §2 Der Authorization Server

### 2.1 Endpunkte

| Methode | Pfad | Auth | Zweck |
|---|---|---|---|
| `GET` | `/.well-known/oauth-protected-resource` | — | PRM (RFC 9728) |
| `GET` | `/.well-known/oauth-protected-resource/mcp` | — | dasselbe Dokument, pfadsuffigierte Variante |
| `GET` | `/.well-known/oauth-authorization-server` | — | AS-Metadaten (RFC 8414) |
| `POST` | `/oauth/register` | — | DCR (RFC 7591), `application/json` |
| `GET` | `/oauth/authorize` | — | Login+Consent-Formular |
| `POST` | `/oauth/authorize` | Passwort + TOTP | Einwilligung, Code-Ausgabe, Redirect |
| `POST` | `/oauth/token` | PKCE | `authorization_code` und `refresh_token`, `x-www-form-urlencoded` |

**Beide PRM-Pfade werden bedient**, weil Claude bei fehlendem `resource_metadata`-Zeiger zuerst
die pfadsuffigierte Variante probiert. Wir liefern den Zeiger zwar immer mit — aber ein
Discovery-Weg, der nur unter Idealbedingungen funktioniert, ist ein Weg, der in der Abnahme
ausfällt.

**Kein `/oauth/revoke` und kein `/oauth/introspect`.** RFC 9700 empfiehlt Widerrufbarkeit —
die ist über `authctl.py revoke` gegeben, und zwar sofort wirksam, weil die Token opak sind
(P4-D). Ein Client-Endpunkt dafür wäre toter Code: Claude ruft ihn nicht.

### 2.2 Die zwei Metadatendokumente

`metadata.py` erzeugt beide aus `AuthSettings`, ohne Literale im Code:

```python
def protected_resource_metadata(settings: AuthSettings) -> dict[str, object]:
    """RFC 9728. 'resource' MUSS exakt der Connector-URL entsprechen."""
    # {
    #   "resource": "https://<host>/mcp",
    #   "authorization_servers": ["https://<host>"],
    #   "bearer_methods_supported": ["header"],
    #   "scopes_supported": ["space"]
    # }

def authorization_server_metadata(settings: AuthSettings) -> dict[str, object]:
    """RFC 8414 + RFC 9207-Flag."""
    # {
    #   "issuer": "https://<host>",
    #   "authorization_endpoint": "https://<host>/oauth/authorize",
    #   "token_endpoint":         "https://<host>/oauth/token",
    #   "registration_endpoint":  "https://<host>/oauth/register",
    #   "scopes_supported": ["space", "offline_access"],
    #   "response_types_supported": ["code"],
    #   "response_modes_supported": ["query"],
    #   "grant_types_supported": ["authorization_code", "refresh_token"],
    #   "token_endpoint_auth_methods_supported": ["none"],
    #   "code_challenge_methods_supported": ["S256"],
    #   "authorization_response_iss_parameter_supported": true
    # }
```

Drei Felder sind **nicht** Kosmetik, und die Tests halten sie fest:

- `offline_access` in den **AS**-`scopes_supported` — ohne diesen Eintrag fragt Claude keinen
  Refresh-Token an, und die Verbindung stirbt nach 60 Minuten.
- `code_challenge_methods_supported: ["S256"]` — die Spec verlangt, dass PKCE-Unterstützung
  erkennbar ist, bevor der Fluss beginnt.
- **`client_id_metadata_document_supported` fehlt bewusst.** Wäre es gesetzt, würde Claude auf
  CIMD umschalten (P4-E). Test: `test_as_metadata_has_no_cimd_flag`.

`issuer` hat **keinen** Pfad. Damit liegen die AS-Metadaten am kanonischen Ort
`/.well-known/oauth-authorization-server` und die Pfadableitung von RFC 8414 wird zum Nicht-Problem.

### 2.3 Datenmodell (`store.py`)

SQLite, WAL, `PRAGMA foreign_keys=ON`, alle Zeitstempel als ISO-8601-UTC-Strings (Konvention
aus P1). Schema-Version in `schema_meta`, damit ein späteres Feld kein Rätsel wird.

```sql
CREATE TABLE schema_meta      (key TEXT PRIMARY KEY, value TEXT NOT NULL);

CREATE TABLE clients (
  client_id        TEXT PRIMARY KEY,
  client_name      TEXT,
  application_type TEXT,
  redirect_uris    TEXT NOT NULL,          -- JSON-Array, exakte Strings
  created_at       TEXT NOT NULL,
  last_used_at     TEXT);

CREATE TABLE auth_requests (
  request_id_hash  TEXT PRIMARY KEY,       -- sha256 der ID aus dem Formular
  client_id        TEXT NOT NULL,
  redirect_uri     TEXT NOT NULL,
  state            TEXT,
  code_challenge   TEXT NOT NULL,
  scope            TEXT NOT NULL,
  resource         TEXT,
  created_at       TEXT NOT NULL,
  expires_at       TEXT NOT NULL,
  consumed_at      TEXT);

CREATE TABLE token_families (
  family_id        TEXT PRIMARY KEY,
  space            TEXT NOT NULL,
  client_id        TEXT NOT NULL,
  scope            TEXT NOT NULL,
  resource         TEXT NOT NULL,
  created_at       TEXT NOT NULL,
  revoked_at       TEXT,
  revoked_reason   TEXT);                  -- 'code_replay' | 'refresh_replay' | 'operator'

CREATE TABLE auth_codes (
  code_hash        TEXT PRIMARY KEY,
  family_id        TEXT NOT NULL REFERENCES token_families(family_id),
  client_id        TEXT NOT NULL,
  redirect_uri     TEXT NOT NULL,
  code_challenge   TEXT NOT NULL,
  created_at       TEXT NOT NULL,
  expires_at       TEXT NOT NULL,
  consumed_at      TEXT);

CREATE TABLE access_tokens (
  token_hash       TEXT PRIMARY KEY,
  family_id        TEXT NOT NULL REFERENCES token_families(family_id),
  space            TEXT NOT NULL,
  scope            TEXT NOT NULL,
  resource         TEXT NOT NULL,          -- Audience-Bindung, RFC 8707
  created_at       TEXT NOT NULL,
  expires_at       TEXT NOT NULL);

CREATE TABLE refresh_tokens (
  token_hash       TEXT PRIMARY KEY,
  family_id        TEXT NOT NULL REFERENCES token_families(family_id),
  created_at       TEXT NOT NULL,
  expires_at       TEXT NOT NULL,
  rotated_at       TEXT,
  successor_hash   TEXT);

CREATE TABLE login_attempts (
  space            TEXT PRIMARY KEY,
  failures         INTEGER NOT NULL DEFAULT 0,
  first_failure_at TEXT,
  locked_until     TEXT);

CREATE TABLE totp_replay (
  space            TEXT PRIMARY KEY,
  last_counter     INTEGER NOT NULL);

CREATE TABLE register_attempts (
  window_start     TEXT PRIMARY KEY,
  count            INTEGER NOT NULL);

CREATE INDEX ix_access_family  ON access_tokens(family_id);
CREATE INDEX ix_refresh_family ON refresh_tokens(family_id);
CREATE INDEX ix_access_exp     ON access_tokens(expires_at);
```

**In dieser Datenbank steht kein einziges Geheimnis im Klartext.** Codes, Access-Token,
Refresh-Token und die Formular-`request_id` liegen ausschließlich als `sha256`-Hex vor. Wer die
Datei kopiert, kann sich damit nicht anmelden. Test: `test_no_plaintext_secret_in_database` —
treibt den ganzen Fluss mit Markerwerten und greppt die Rohdatei.

`AuthStore` bekommt `now_fn` injiziert (P1-Konvention), und **jede** Zustandsänderung, die
zwei Schritte hat (Code einlösen, Refresh rotieren), läuft in **einer** Transaktion mit
`BEGIN IMMEDIATE`. Ein Fluss, der zur Hälfte gilt, ist schlimmer als einer, der scheitert.

### 2.4 Der Fluss, Schritt für Schritt

**`GET /oauth/authorize`** — Reihenfolge der Prüfungen ist sicherheitsrelevant:

1. `client_id` unbekannt → **Fehlerseite rendern, nicht umleiten.**
2. `redirect_uri` nicht byteweise in `clients.redirect_uris` → **Fehlerseite rendern, nicht umleiten.**
   *Erst ab hier ist die Rücksprungadresse vertrauenswürdig.*
3. Ab jetzt gehen Fehler als Redirect mit `error`, `error_description`, `state` und `iss` zurück:
   `response_type != "code"` → `unsupported_response_type` ·
   `code_challenge` fehlt oder `code_challenge_method != "S256"` → `invalid_request` ·
   `scope` nicht Teilmenge von `{space, offline_access}` → `invalid_scope` ·
   `resource` gesetzt und ≠ `settings.resource` → `invalid_target`.
4. `AuthRequest` anlegen: `request_id = token_urlsafe(32)`, Hash speichern, TTL 10 min.
5. Formular rendern (§2.5).

**`POST /oauth/authorize`** — Felder `request_id`, `space`, `password`, `totp`, `action`:

1. `AuthRequest` per Hash laden; fehlt, abgelaufen oder `consumed_at` gesetzt → Fehlerseite.
   **Sofort als konsumiert markieren** — auch bei Fehlschlag. Ein Formular, ein Versuch.
2. `action == "deny"` → Redirect mit `error=access_denied`.
3. Sperre prüfen (`ratelimit.py`). Gesperrt → Fehlerseite mit Restzeit, **kein** Passwortcheck.
4. Nutzerakte laden. **Existiert der Space nicht, wird trotzdem ein Argon2id-Durchlauf gegen
   einen festen Dummy-Hash gefahren**, damit die Antwortzeit nicht verrät, ob das Konto
   existiert. Danach in jedem Fehlerfall dieselbe Meldung: *„Anmeldung fehlgeschlagen."*
5. Argon2id verifizieren **und** TOTP verifizieren. Beide Ergebnisse werden **erst am Ende**
   verknüpft — kein früher `return`, keine unterschiedlichen Meldungen.
6. TOTP-Replay: `counter <= totp_replay.last_counter` → Fehlschlag. Bei Erfolg hochsetzen.
7. Fehlschlag → `ratelimit.register_failure(space)`, Fehlerseite.
   Erfolg → `ratelimit.reset(space)`.
8. `token_families`-Zeile anlegen, Authorization-Code erzeugen (`token_urlsafe(32)`, TTL 60 s),
   Hash mit `client_id`, `redirect_uri`, `code_challenge`, `family_id` ablegen.
9. **302** auf `redirect_uri?code=…&state=…&iss=…`.

**`POST /oauth/token`, `grant_type=authorization_code`:**

1. Code-Hash laden. Unbekannt oder abgelaufen → `invalid_grant`.
2. **`consumed_at` gesetzt → Familie widerrufen (`code_replay`), alle Access- und
   Refresh-Token der Familie löschen, `invalid_grant`.** (RFC 9700)
3. `client_id` und `redirect_uri` müssen exakt übereinstimmen → sonst `invalid_grant`.
4. PKCE: `base64url(sha256(code_verifier))` ohne Padding, konstantzeitiger Vergleich gegen
   `code_challenge` → sonst `invalid_grant`.
5. Code als konsumiert markieren, Access-Token (60 min) und Refresh-Token (30 d) in derselben
   Transaktion anlegen.
6. Antwort `200`, `Cache-Control: no-store`, `Pragma: no-cache`:
   `{"access_token": …, "token_type": "Bearer", "expires_in": 3600, "refresh_token": …, "scope": "space offline_access"}`

**`POST /oauth/token`, `grant_type=refresh_token`:**

1. Hash laden. Unbekannt, abgelaufen oder Familie widerrufen → `invalid_grant`.
2. **`rotated_at` gesetzt → Familie widerrufen (`refresh_replay`), `invalid_grant`.** (RFC 9700)
3. Rotieren: alten Eintrag mit `rotated_at` und `successor_hash` versehen, neuen anlegen,
   neuen Access-Token ausgeben — alles in **einer** Transaktion.
4. Der neue Refresh-Token steht in derselben Antwort, die den alten entwertet — genau so
   verlangt es die Anthropic-Doku.

**Alle Fehlerantworten** kommen aus `errors.py` und tragen ausschließlich RFC-6749-Codes:
`invalid_request`, `invalid_client`, `invalid_grant`, `unauthorized_client`,
`unsupported_grant_type`, `invalid_scope`, `invalid_target`. **Niemals** ein eigener Code,
**niemals** eine Beschreibung, die zwischen „unbekannt", „abgelaufen" und „widerrufen"
unterscheidet.

### 2.5 Nutzerakten, Passwort, zweiter Faktor

**Format** (Quelle der Wahrheit: Keyring, Service `nikinger-space`, Key `auth-users`):

```json
{
  "niklas": {"pwd": "$argon2id$v=19$m=19456,t=2,p=1$…",
             "totp": "<BASE32-SEED>", "totp_alg": "SHA1",
             "created_at": "2026-07-…"}
}
```

Weg in den Dienst — **identisch zum P3-Muster**, deshalb ohne Neuerfindung:

```
provision_user.py --space niklas   → Keyring
        │  (Passwort über getpass, Seed erzeugt, otpauth://-URI EINMAL auf stdout)
        ▼
export_auth_users.py  |  sudo systemd-creds encrypt --name=auth-users - /etc/sharefyx/auth-users.cred
        ▼
LoadCredentialEncrypted=auth-users:/etc/sharefyx/auth-users.cred
        ▼
$CREDENTIALS_DIRECTORY/auth-users   →  users.py :: load_users()
```

**Der Unterschied zu P3, der benannt werden muss:** die Space-Map enthielt nur Hashes. Diese
Datei enthält **echte, umkehrbare Geheimnisse** — die TOTP-Seeds. Damit ist die Verschlüsselung
hier zum ersten Mal Schutz und nicht nur Regeltreue. Das gehört in den Phase-Head, und die
Warnung in `export_auth_users.py` sagt es beim Aufruf: *„Ausgabe enthält TOTP-Seeds im Klartext.
Nur in eine Pipe, nie in eine Datei."*

`provision_user.py` zeigt Passwort und Seed **genau einmal** und schreibt beide nie in eine
Datei — dieselbe Disziplin wie `issue_token.py` in P2, aus demselben Grund.

**`passwords.py`:**
```python
ARGON2_TIME_COST   = 2
ARGON2_MEMORY_KIB  = 19456      # 19 MiB — OWASP-Mindestkonfiguration
ARGON2_PARALLELISM = 1
ARGON2_HASH_LEN    = 32
ARGON2_SALT_LEN    = 16

def hash_password(password: str) -> str: ...
def verify_password(stored: str, password: str) -> bool: ...   # wirft nie, gibt False
def needs_rehash(stored: str) -> bool: ...
DUMMY_HASH: str                 # für den Enumerationsschutz aus §2.4, Schritt 4
```
`[VERIFY]` V17 — 19 MiB je Anmeldung auf der VM: RAM prüfen und die Dauer eines Durchlaufs
messen. Ziel 50–250 ms. Liegt sie deutlich darunter, `t` erhöhen und **den gemessenen Wert im
Session-Block dokumentieren**, nicht raten.

**`totp.py`** — stdlib, ~40 Zeilen:
```python
def generate_secret(nbytes: int = 20) -> str: ...              # Base32 ohne Padding
def totp_at(secret: str, counter: int, *, digits: int = 6, algo: str = "SHA1") -> str: ...
def verify(secret: str, code: str, *, now: float, window: int = 1,
           last_counter: int | None = None, ...) -> int | None: ...   # akzeptierter Zähler
def provisioning_uri(secret: str, *, space: str, issuer: str) -> str: ...
```
Tests gegen die **RFC-6238-Testvektoren** — das ist der Grund, dieses Modul selbst zu schreiben
statt eine Bibliothek zu ziehen: die Korrektheit ist gegen eine Norm beweisbar, nicht gegen
mein Vertrauen.

`[VERIFY]` V18 — **Systemzeit.** TOTP scheitert stumm bei Drift. `timedatectl show -p NTPSynchronized`
muss `yes` liefern; sonst ist das ein Befund vor Step 7, nicht danach.

### 2.6 Sicherheits-Header und Registrierungs-Allowlist

Alle HTML-Antworten und beide Metadatendokumente tragen:

| Header | Wert | Warum |
|---|---|---|
| `Content-Security-Policy` | `default-src 'none'; style-src 'unsafe-inline'; form-action 'self'; frame-ancestors 'none'; base-uri 'none'` | Es gibt kein JS, keine externen Ressourcen. Die Policy schreibt das fest, statt darauf zu vertrauen |
| `Referrer-Policy` | `no-referrer` | Verhindert, dass Query-Parameter der Auth-Seite abfließen |
| `X-Content-Type-Options` | `nosniff` | |
| `X-Frame-Options` | `DENY` | Clickjacking auf den Consent-Button |
| `Cache-Control` | `no-store` | Auf **allen** OAuth-Antworten, nicht nur auf `/token` |
| `Strict-Transport-Security` | `max-age=63072000; includeSubDomains` | Abschaltbar über `SPACE_OAUTH_HSTS=off`. **Hinweis im Phase-Head:** gilt für den ganzen Hostnamen, also auch für andere Dienste auf derselben Tailscale-Node |

**Registrierungs-Allowlist** (`clients.py`): `/oauth/register` akzeptiert nur `redirect_uris`,
deren Origin in `SPACE_OAUTH_ALLOWED_REDIRECT_ORIGINS` steht — Default
`https://claude.ai,https://claude.com`. Alles andere → `invalid_redirect_uri`.

Das ist die wirksamste einzelne Maßnahme dieser Phase. Ein offener DCR-Endpunkt im Internet
lässt jeden beliebige Clients anlegen; die Allowlist reduziert das auf „Anthropic oder gar
nicht". **Bewusster Preis:** Claude Code mit Loopback-Redirect wird damit abgelehnt. Das ist
Absicht (§8) und muss im Phase-Head stehen, damit der Fehlschlag später nicht wie ein Bug aussieht.

`application_type` wird gespeichert und, wenn `"native"`, mit `invalid_client_metadata`
abgelehnt — dieselbe Begründung.

**`[SEAM]` — Erweiterungspfad für native Clients (Nikinger-Auflage, 2026-07-28).** Die gesamte
Redirect-Prüfung lebt in **genau einer** Funktion, an genau einer Stelle:

```python
# authserver/clients.py
def redirect_uri_allowed(uri: str, settings: AuthSettings) -> bool:
    """Die EINZIGE Stelle, an der über Rücksprungadressen entschieden wird.

    P4-Policy: exakter Origin-Vergleich gegen settings.allowed_redirect_origins,
    ausschließlich https.

    [SEAM] Native Clients (Claude Code, CLI-Werkzeuge) brauchen Loopback-Redirects
    nach RFC 8252 §7.3: http://127.0.0.1:<wechselnder Port>/callback, Vergleich mit
    IGNORIERTEM Port. Das ist eine zweite Vergleichsregel, kein Sonderfall dieser hier —
    und es hängt an CIMD, nicht an DCR (§8). Wer das baut, ändert diese Funktion und
    ihre Tests, sonst nichts.
    """
```

Sie wird von `/oauth/register` **und** von `/oauth/authorize` aufgerufen — nirgends sonst wird
eine Redirect-URI bewertet. Test dazu: `test_redirect_uri_allowed_is_the_only_matching_path`
(Grep über `authserver/`: kein zweiter Vergleich von `redirect_uri` gegen eine Origin-Liste).

### 2.7 Fehlversuchsbremse (`ratelimit.py`)

```python
MAX_FAILURES      = 5
WINDOW_S          = 900        # 15 min
BASE_LOCKOUT_S    = 900        # 15 min, verdoppelt je weiterer Sperre
MAX_LOCKOUT_S     = 86400      # 24 h Deckel

class LoginThrottle:
    def __init__(self, store: AuthStore, *, now_fn: Callable[[], datetime]) -> None: ...
    def check(self, space: str) -> int | None: ...        # Restsperre in Sekunden oder None
    def register_failure(self, space: str) -> None: ...
    def reset(self, space: str) -> None: ...
```

Pro Space, nicht pro IP — der Login läuft im Browser des Menschen, dessen IP wechselt, während
der Angreifer seine wechseln kann. Der bewusst akzeptierte Preis ist ein Aussperr-DoS gegen
einen der beiden Nutzer; Gegenmittel ist `authctl.py unlock`, eine SSH-Sitzung entfernt.

`/oauth/register` bekommt eine eigene, gröbere Bremse: **20 Registrierungen pro Stunde
insgesamt** (`register_attempts`). Danach `429`. Die Allowlist ist die Tür, das hier ist der
Türstopper.

### 2.8 Konfiguration

Neue Umgebungsvariablen, alle mit dem bestehenden `SPACE_`-Präfix (Konvention aus P2/P3):

| Variable | Default | Bedeutung |
|---|---|---|
| `SPACE_AUTH_MODE` | `oauth` | `token` \| `both` \| `oauth` (P4-N) |
| `SPACE_PUBLIC_BASE_URL` | — (Pflicht bei `oauth`/`both`) | z. B. `https://<node>.<tailnet>.ts.net`, **ohne** Schrägstrich am Ende |
| `SPACE_AUTH_DB` | `$STATE_DIRECTORY/auth.sqlite3` | Fehlt beides → Startfehler, kein stiller Fallback in das Arbeitsverzeichnis |
| `SPACE_OAUTH_ALLOWED_REDIRECT_ORIGINS` | `https://claude.ai,https://claude.com` | §2.6 |
| `SPACE_OAUTH_ACCESS_TTL_S` | `3600` | |
| `SPACE_OAUTH_REFRESH_TTL_S` | `2592000` | |
| `SPACE_OAUTH_CODE_TTL_S` | `60` | |
| `SPACE_OAUTH_REQUEST_TTL_S` | `600` | |
| `SPACE_OAUTH_HSTS` | `on` | |

`resource` und `issuer` werden **abgeleitet**, nicht konfiguriert:
`resource = f"{base_url}/mcp"`, `issuer = base_url`. Zwei Variablen, die dasselbe zweimal sagen,
gehen irgendwann auseinander.

**Validierung beim Start**, hart: `SPACE_PUBLIC_BASE_URL` muss `https://` sein, ohne Query,
ohne Fragment, ohne Schrägstrich am Ende. Ein Tippfehler hier bricht die Discovery auf eine
Weise, die von außen wie „Server nicht erreichbar" aussieht.

---

## §3 Resource-Server-Seite

### 3.1 `mcpserver/asgi.py`

Anker: `class TokenPathASGI:` und dessen `__init__(self, app, *, resolver: SpaceResolver)`.

```python
class BearerAuthASGI:
    """Liest 'Authorization: Bearer <token>', löst auf, setzt den Principal.

    Fehlt der Header oder ist der Token unbekannt/abgelaufen: 401 mit
    WWW-Authenticate. Der Body ist beratend, das Signal ist Status + Header.
    """
    def __init__(self, app, *, resolver: SpaceResolver, challenge: str) -> None: ...
    async def __call__(self, scope, receive, send) -> None: ...


class AuthModeASGI:
    """Übergangsweiche für P4-N. Entfällt in Step 7 vollständig.

    mode='oauth' → immer Bearer.
    mode='token' → immer Pfadsegment (P2-Verhalten).
    mode='both'  → Pfadsegment vorhanden? dann TokenPathASGI, sonst BearerAuthASGI.
    """
    def __init__(self, *, mode: str, bearer, token_path) -> None: ...
```

Der Challenge-String wird **einmal** in `app.py` gebaut, nicht pro Request:

```
Bearer error="invalid_token", error_description="Authentication required",
       resource_metadata="<base>/.well-known/oauth-protected-resource/mcp", scope="space"
```

`[VERIFY]` V19 — die Header-Reihenfolge und die Anführungszeichen sind bei manchen Parsern
heikel. Beim ersten Live-Versuch mit `curl -si` gegenprüfen, dass Claude den Connect-Button
zeigt und nicht „Couldn't reach the MCP server".

**Nicht vergessen:** der 401 muss **auch** für `tools/list` und jede andere Methode kommen.
Wir bauen keine Lazy-Auth — alle sechs Tools sind geschützt, es gibt keine öffentliche
Teilmenge. Das ist einfacher und ehrlicher.

### 3.2 `mcpserver/context.py`

Anker: `def assert_principal_matches_request() -> None:`

Heute zieht der Guard das Token-Segment aus dem Pfad und vergleicht `hash_token(...)` gegen
`principal.token_hash`. Neu: er liest den `Authorization`-Header desselben Requests und
vergleicht dessen `sha256` — im Modus `both` fällt er auf das Pfadsegment zurück.

**Die Funktion bleibt, ihr Zweck bleibt, ihre Signatur bleibt.** Sie ist die Versicherung
gegen einen Request-Verwechsler im HTTP-Kontext und kostet einen SHA-256 pro Tool-Aufruf. Wer
sie beim Umbau „vereinfacht", entfernt genau die Zeile, die einen stillen Cross-Space-Leak in
einen lauten Fehler verwandelt.

### 3.3 `mcpserver/app.py`

Anker: `create_app(*, settings, resolver, store, allowed_hosts=None)`.

- `TrustedHostMiddleware` mit denselben `allowed_hosts` wie die FastMCP-App (P4-P).
- Die Routen aus `authserver.routes.oauth_routes(auth_settings, auth_store, users)` werden der
  Wurzel-App **vorangestellt** — `/.well-known/*` und `/oauth/*` liegen vor `Mount("/mcp")`.
- `Mount("/mcp", app=AuthModeASGI(...))` statt `Mount("/mcp", TokenPathASGI(...))`.
- Der Signaturzusatz ist **ein** optionaler Parameter: `oauth=None`. Ist er `None`, verhält sich
  `create_app` exakt wie in P3 — damit bleiben die bestehenden `test_app.py`-Tests unverändert
  gültig. Das ist kein Trick, sondern die Bedingung dafür, dass ein Testfehler in P4 auch aus
  P4 stammt.

---

## §4 Logging

`request_log.py` bekommt eine dritte Ereignisart. Feld-Whitelist wird erweitert um
`stage`, `client_id`, `grant`:

```
{"ts":"…","ev":"oauth","stage":"register","ok":true,"client_id":"cli_a1b2…","ms":8}
{"ts":"…","ev":"oauth","stage":"authorize_post","ok":false,"space":"niklas","err":"login_failed","ms":142}
{"ts":"…","ev":"oauth","stage":"token_refresh","ok":false,"err":"invalid_grant","ms":3}
```

`stage` ∈ `register`, `authorize_get`, `authorize_post`, `token_code`, `token_refresh`.
`err` ist auf die OAuth-Fehlercodes plus `login_failed`, `locked` und `replay` beschränkt.

**Was niemals in einer Logzeile stehen darf**, ergänzend zur P3-Tabelle:

| Verboten | Warum |
|---|---|
| Passwort, TOTP-Code | Offensichtlich — und genau deshalb der Ort, an dem es passiert |
| Authorization-Code, `code_verifier`, `code_challenge` | Der Code ist ein Einmal-Geheimnis; `code_verifier` bricht PKCE |
| Access- und Refresh-Token, auch gekürzt | Zwei dokumentierte Token-Klartext-Vorfälle in P2/P3 |
| Der `state`-Parameter | Kann clientseitige Kennungen tragen |
| Redirect-URI mit Query | Enthält im Fehlerfall den `error_description`-Text |

`logging_setup.py :: _TOKEN_SEGMENT_RE` wird zu einem **Satz** von Mustern erweitert
(`_SECRET_PATTERNS`), der zusätzlich `code=`, `access_token`, `refresh_token`, `password`,
`totp` und `Authorization: Bearer …` durch `<redacted>` ersetzt. Der bestehende
`TokenScrubbingFilter` bleibt die einzige Stelle, an der das passiert — **nicht** duplizieren.

**Der wichtigste Test des Logging-Steps:** `test_oauth_log_never_contains_secrets` treibt über
`oauth_smoke.py` den vollständigen Fluss mit erkennbaren Markerwerten
(`ZZZ-PASSWORD`, `ZZZ-CODE`, …) und prüft den kompletten Logpuffer auf jeden Marker. Er prüft
keine Implementierung, sondern eine Zusage — genauso wie sein Vorbild aus P3.

---

## §5 Steps

Jeder Step endet mit einem Commit, grünem `pytest` und der Doku-Pflicht aus §7 **im selben
Commit** (Hard Rule 8).

### Step 0 — Haushalt, Drift, geerbte Abnahme

Kein neuer Code. Vier Blöcke, „nichts zu tun" ist bei A und B ein zulässiges Ergebnis.

**A · Verifikationsdurchlauf**
- Alle `up:`/`down:`-Ziele auflösbar? Jede `.md` mit Indexzeile?
- `find . -name "*.md" -not -path "./.agents/*" -not -path "*/.pytest_cache/*" -size +40k` —
  jeder Treffer muss 📕/📦 sein. Bekannt und erlaubt: `phase2_mcp_plan.md`, `phase3_edge_plan.md`,
  `phase2_mcp/SESSIONS_ARCHIVE.md`, `phase3_edge/SESSIONS_ARCHIVE.md`.
- `git status` sauber. `pytest -q` → **Ausgangszahl notieren** (~168 laut Handover, `[VERIFY]` V20).
  Weicht sie ab, ist das ein Befund **vor** dem ersten Commit.

**B · Autocompact-Drift** (Handover §5). **Zuerst** die eine Prüfung, die alles andere entscheidet:

```bash
python phase3_edge/scripts/export_space_map.py | python -c "import json,sys; m=json.load(sys.stdin); print(len(m), sorted(set(m.values())))"
# erwartet: 2 ['fabian', 'niklas']
```
Weicht die Zahl ab: **sofort stoppen und dem Nikinger melden.** Das ist ein Befund, kein
Aufräumjob — dann existiert ein Token, das niemand zuordnen kann.

Danach die fünf feststehenden Funde plus die vier Grep-Muster aus dem Handover.
**Regel:** 📕-Snapshots bekommen datierte Nachträge, keine Rückwirkung; lebende Dokumente
(`ROADMAP.md`, Root-`CLAUDE.md`, Phase-Heads, `docs/INDEX.md`) werden direkt korrigiert, mit
datierter Korrekturnotiz.

Zwei **zusätzliche** Funde aus dieser Planungssession:
- `README.md` ist auf Stand 2026-07-24 („Es existiert noch kein Code", Architekturdiagramm mit
  Cloudflare, „OAuth 2.1 ist Phase 5"). Vollständig auf P3-Stand ziehen.
- Root-`CLAUDE.md`, „Current state" nennt Phase 1 als aktive Phase. Auf P4 setzen, `down:` umhängen.

**C · Geerbte P3-Abnahme** (Handover §4). Stand laut Nikinger, 2026-07-28: **kein Reboot
gelaufen.** Also:
- Zeile 6 bleibt offen, **passiv** — kein erzwungener `sudo reboot`. Beim ersten echten Reboot
  `/health` von außen prüfen und P3 auf ✅ heben.
- Zeile 12 (`systemctl list-timers sharefyx-backup`) und Zeile 13 (`restore_check.sh` mit
  frischem Bundle) jetzt nachholen. **`restore_check.sh` nicht umbauen**, bevor ein Lauf unter
  diesen Bedingungen stattgefunden hat (B5 war kein Defekt).
- V13: `diagnose.sh`, Prüfung 4, einmal gegen das reale `tailscale funnel status` laufen lassen.

**D · Umgebungsinventar** (alles `[VERIFY]`, Ergebnisse tabellarisch in den Session-Block):

```bash
systemctl --version | head -1              # ≥ 235 für StateDirectory=
pip index versions fastmcp                 # ist der P3-E-Trigger gefallen? NUR notieren
pip index versions argon2-cffi             # exakter Pin für P4-R
free -m                                    # RAM-Budget für Argon2id (19 MiB/Anmeldung)
timedatectl show -p NTPSynchronized        # muss yes sein → TOTP
curl -s -o /dev/null -w '%{http_code}\n' https://<host>/.well-known/oauth-protected-resource
                                           # erwartet 404 — belegt, dass der Funnel .well-known durchreicht
```

**Befund, der schon feststeht und nur bestätigt werden muss:** FastMCP 4 spricht laut
Herstellerdoku die Revision 2026-07-28. Damit ist der Trigger aus P3-E vermutlich gefallen.
**Das ist eine Meldung an den Nikinger, keine Aufgabe in P4** — Bibliotheks-Major und
Auth-Umbau gleichzeitig machen jeden Fehlschlag unzuordenbar. Eintrag in `ROADMAP.md` unter
„Zurückgestellt", Formulierung: *Trigger gefallen am 2026-07-28, eigene Mini-Phase nach P4.*

**Done when:** alle Prüfpunkte beantwortet, `pytest` grün, ein Commit, Bericht an den Nikinger
mit Inventartabelle und Befundliste.

---

### Step 1 — Gerüst, Konfiguration, Kryptobausteine

**Dateien:** `phase4_auth/{CLAUDE.md,SESSIONS_ARCHIVE.md,pyproject.toml}`,
`authserver/{__init__,config,models,crypto,errors}.py`, `phase4_auth/tests/{__init__,test_crypto}.py`,
`pytest.ini`, `.gitignore`.

`pytest.ini` — wörtlich:
```
[pytest]
testpaths = phase1_storage/tests phase2_mcp/tests phase3_edge/tests
```
wird zu
```
[pytest]
testpaths = phase1_storage/tests phase2_mcp/tests phase3_edge/tests phase4_auth/tests
```

`.gitignore`: `*.sqlite3` ist über `phase1_storage` möglicherweise schon abgedeckt `[VERIFY]` V21 —
sicherstellen, dass `auth.sqlite3` in **keinem** Fall committet werden kann.

```python
# authserver/config.py
@dataclass(frozen=True, kw_only=True)
class AuthSettings:
    base_url: str
    db_path: Path
    mode: str = "oauth"
    allowed_redirect_origins: tuple[str, ...] = ("https://claude.ai", "https://claude.com")
    access_ttl_s: int = 3600
    refresh_ttl_s: int = 2592000
    code_ttl_s: int = 60
    request_ttl_s: int = 600
    hsts: bool = True

    @property
    def issuer(self) -> str: ...          # == base_url
    @property
    def resource(self) -> str: ...        # == f"{base_url}/mcp"

def load_auth_settings(env: Mapping[str, str] | None = None) -> AuthSettings: ...
```

```python
# authserver/crypto.py
def new_secret(nbytes: int = 32) -> str: ...            # secrets.token_urlsafe
def hash_secret(value: str) -> str: ...                 # sha256-Hex — für Token, NICHT für Passwörter
def secrets_equal(a: str, b: str) -> bool: ...          # hmac.compare_digest
def pkce_challenge(verifier: str) -> str: ...           # base64url(sha256(v)), ohne Padding
def verify_pkce(verifier: str, challenge: str) -> bool: ...
```

**Tests** (`test_crypto.py`): `test_new_secret_has_expected_entropy`,
`test_hash_secret_is_stable_and_hex`, `test_pkce_challenge_matches_rfc7636_appendix_b`,
`test_verify_pkce_rejects_mismatch`, `test_secrets_equal_is_constant_time_api`.

Der PKCE-Test läuft gegen das **Beispiel aus RFC 7636 Anhang B** — nicht gegen einen selbst
erzeugten Wert. Ein Selbsttest, der beide Seiten selbst berechnet, beweist nur Konsistenz.

**Done when:** `pytest` grün; `./scripts/dev_install.sh` nimmt `phase4_auth/` auf; Indexzeilen
für die zwei neuen `.md` im selben Commit.

---

### Step 2 — Passwörter, TOTP, Nutzerakten

**Dateien:** `authserver/{passwords,totp,users}.py`, `phase4_auth/scripts/{provision_user,export_auth_users}.py`,
Tests `test_passwords.py`, `test_totp.py`, `test_users.py`.

Inhalte wie §2.5. `users.py` spiegelt `credentials.py :: load_space_map()`:
Credentials-Verzeichnis zuerst, Keyring als Fallback, `warning` statt Ausnahme bei fehlender
Datei, **Ausnahme** bei kaputtem Inhalt. **Kein `keyring`-Import außerhalb dieses Moduls.**

**Tests:**
- `test_argon2_roundtrip`, `test_verify_rejects_wrong_password`,
  `test_verify_returns_false_on_garbage_hash` (wirft nicht),
  `test_parameters_match_owasp_minimum` — liest die Parameter aus dem erzeugten Hash-String zurück
- `test_totp_matches_rfc6238_test_vectors` — **der Test, um den es geht**
- `test_totp_accepts_previous_and_next_step`, `test_totp_rejects_replayed_counter`
- `test_provisioning_uri_is_wellformed`
- `test_load_users_prefers_credentials_dir`, `…_falls_back_to_keyring`, `…_raises_on_malformed`
- `test_export_contains_no_password_plaintext`
- `test_provision_prints_secret_once_and_never_writes_a_file`

**Done when:** `pytest` grün; `[VERIFY]` V17 (Argon2-Laufzeit) und V18 (NTP) beantwortet.

---

### Step 3 — Persistenz und Bremse

**Dateien:** `authserver/{store,ratelimit}.py`, `test_store.py`, `test_ratelimit.py`.

Schema aus §2.3. `AuthStore` kapselt **jede** SQL-Anweisung; kein SQL außerhalb dieses Moduls.
`now_fn` injiziert. Transaktionen wie in §2.3 beschrieben.

Methodennamen (fix):
```python
class AuthStore:
    def __init__(self, path: Path, *, now_fn: Callable[[], datetime]) -> None: ...
    def initialise(self) -> None: ...
    # Clients
    def create_client(self, ...) -> Client: ...
    def get_client(self, client_id: str) -> Client | None: ...
    # Auth-Requests
    def create_auth_request(self, ...) -> str: ...           # gibt die Klartext-request_id zurück
    def consume_auth_request(self, request_id: str) -> PendingAuthRequest | None: ...
    # Codes und Token
    def issue_code(self, ...) -> str: ...
    def consume_code(self, code: str) -> tuple[AuthorizationCode | None, bool]: ...  # (…, war_replay)
    def issue_token_pair(self, family_id: str, ...) -> tuple[str, str]: ...
    def rotate_refresh(self, refresh_token: str) -> tuple[str, str] | None: ...
    def revoke_family(self, family_id: str, reason: str) -> int: ...
    def lookup_access_token(self, token: str) -> AccessTokenRecord | None: ...
    def purge_expired(self) -> dict[str, int]: ...
```

**Tests** — der Kern der Phase, deshalb ausführlich:
- `test_schema_is_created_and_versioned`, `test_reopen_is_idempotent`
- `test_auth_request_is_single_use`, `test_auth_request_expires`
- `test_code_is_single_use`, `test_second_code_use_reports_replay`
- `test_refresh_rotation_returns_new_pair`
- `test_reused_refresh_reports_replay`
- `test_revoke_family_kills_access_and_refresh_tokens`
- `test_lookup_access_token_rejects_expired`
- `test_lookup_access_token_rejects_revoked_family`
- `test_no_plaintext_secret_in_database` — treibt den ganzen Fluss und greppt die Rohdatei
- `test_purge_expired_leaves_valid_rows`
- `test_lockout_after_five_failures`, `test_lockout_doubles`, `test_lockout_capped_at_24h`,
  `test_success_resets_counter`, `test_check_is_readonly`

**Done when:** `pytest` grün; kein SQL außerhalb `store.py` (Grep im Session-Block belegen).

---

### Step 4 — Metadaten und dynamische Registrierung

**Dateien:** `authserver/{metadata,clients}.py`, erste Hälfte von `routes.py`,
`test_metadata.py`, `test_clients.py`.

Inhalte wie §2.2 und §2.6. Vor diesem Step: `[VERIFY]` V14 — die Anthropic-Auth-Seite einmal
gegenlesen; sie ist die einzige Quelle, die sich ohne Vorwarnung ändert.

**Tests:**
- `test_prm_resource_equals_connector_url`
- `test_prm_lists_exactly_one_authorization_server`
- `test_as_metadata_advertises_s256_only`
- `test_as_metadata_lists_offline_access` — *ohne dieses Feld gibt es keinen Refresh-Token*
- `test_as_metadata_has_no_cimd_flag`
- `test_as_metadata_sets_iss_parameter_flag`
- `test_register_accepts_claude_redirect_uri`
- `test_register_rejects_foreign_origin`
- `test_register_rejects_native_application_type`
- `test_redirect_uri_allowed_is_the_only_matching_path` — belegt den `[SEAM]` aus §2.6
- `test_register_returns_no_client_secret`
- `test_register_is_rate_limited`
- `test_register_requires_json_content_type`
- `test_wellknown_paths_serve_identical_documents`

**Done when:** `pytest` grün; beide `.well-known`-Pfade liefern byte-identische Dokumente.

---

### Step 5 — Autorisierungsfluss

**Dateien:** `authserver/{flows,templates}.py`, `routes.py` vervollständigt, `test_flows.py`,
`test_routes.py`, `test_templates.py`.

Inhalte wie §2.4. `routes.py` bleibt **dünn**: parsen, `flows` aufrufen, antworten. Keine
Zustandslogik in den Handlern — sonst ist der Fluss nur über HTTP testbar.

`templates.py` beginnt mit:
```python
"""Wegwerf-UI. Wird in Phase 5 durch die echte Web-Oberfläche ERSETZT, nicht erweitert.

Kein Framework, kein JavaScript, kein CSS-Build, keine Cookies. Wer hier eine
Template-Engine einführt, hat die Phase verwechselt.
"""
```

**Tests:**
- `test_authorize_rejects_unknown_client_without_redirect`
- `test_authorize_rejects_unregistered_redirect_uri_without_redirect` — *die beiden wichtigsten
  Tests des Steps: ein Fehler darf hier niemals zu einer Umleitung führen*
- `test_authorize_rejects_plain_pkce`
- `test_authorize_redirect_error_carries_state_and_iss`
- `test_authorize_rejects_foreign_resource_parameter`
- `test_consent_requires_password_and_totp`
- `test_wrong_password_and_unknown_space_give_identical_response` — Enumerationsschutz
- `test_login_failure_increments_throttle`
- `test_locked_account_skips_password_check`
- `test_form_is_single_use`
- `test_code_exchange_happy_path`
- `test_code_exchange_rejects_wrong_verifier`
- `test_code_exchange_rejects_mismatched_redirect_uri`
- `test_code_replay_revokes_family`
- `test_refresh_rotates_and_returns_new_refresh`
- `test_refresh_replay_revokes_family`
- `test_all_token_errors_use_invalid_grant`
- `test_token_response_has_no_store`
- `test_html_responses_carry_security_headers`
- `test_no_cookie_is_ever_set` — belegt P4-O

**Done when:** `pytest` grün; jeder Fehlerpfad aus §2.4 hat genau einen Test.

---

### Step 6 — Anbindung an den Resource Server und der Beweis

**Dateien:** `authserver/resolver.py`, `mcpserver/{asgi,context,app,config,request_log,logging_setup}.py`,
`scripts/serve.py`, `phase2_mcp/tests/test_asgi_bearer.py`, `phase4_auth/scripts/oauth_smoke.py`,
`test_resolver.py`.

Inhalte wie §3 und §4.

`oauth_smoke.py` ist das Gegenstück zu `space_cli.py` (P1) und `mcp_smoke.py` (P2): es fährt
**ohne Browser** den vollständigen Fluss gegen einen lokal gestarteten Server —
Discovery → Registrierung → `GET /authorize` → Formular-POST mit Passwort und errechnetem
TOTP → Code → Token → `tools/call` mit Bearer → Refresh → **Reuse mit dem alten Refresh-Token**
(muss `invalid_grant` liefern und die Familie töten). Ausgabe: eine Zeile je Schritt mit
✅/❌, Exitcode ≠ 0 bei jedem Fehlschlag.

Er ist zugleich das Werkzeug, mit dem `test_oauth_log_never_contains_secrets` (§4) fährt, und
das erste, was in Step 7 bei einem Problem gestartet wird — er trennt „unser Server" von
„Claudes Client".

**Tests:**
- `test_missing_authorization_header_returns_401_with_challenge`
- `test_challenge_contains_resource_metadata_and_scope`
- `test_unknown_bearer_returns_401_without_detail`
- `test_expired_token_returns_401`
- `test_revoked_family_token_returns_401`
- `test_valid_bearer_sets_principal_space`
- `test_guard_rejects_principal_from_other_request`
- `test_auth_mode_token_preserves_p2_behaviour`
- `test_auth_mode_both_serves_bearer_and_path`
- `test_default_auth_mode_is_oauth` — **P4-N, das Verfallsdatum als Test**
- `test_oauth_log_never_contains_secrets`
- `test_oauth_events_carry_stage_and_duration`

**Done when:** `pytest` grün; `oauth_smoke.py` **11/11**; die sechs Tools verhalten sich unter
Bearer-Auth exakt wie unter Pfad-Token (Diff der Antworten im Session-Block).

---

### Step 7 — Betrieb, Live-Abnahme, Schnitt

**Dateien:** `phase4_auth/systemd/sharefyx-mcp.service`, `phase3_edge/scripts/install_units.sh`
(nur Platzhalterliste), `phase3_edge/local.env.example`, `phase4_auth/scripts/authctl.py`,
`phase4_auth/CLAUDE.md` (Runbooks), `docs/concepts/P4_ABNAHME_<YYYY-MM-DD>.md`.

**Unit-Ergänzungen** gegenüber der P3-Fassung — der Rest bleibt Wort für Wort:
```ini
StateDirectory=sharefyx
StateDirectoryMode=0700
LoadCredentialEncrypted=spaces:/etc/sharefyx/spaces.cred
LoadCredentialEncrypted=auth-users:/etc/sharefyx/auth-users.cred
Environment=SPACE_AUTH_MODE=__AUTH_MODE__
Environment=SPACE_PUBLIC_BASE_URL=__PUBLIC_BASE_URL__
```
Platzhalter-Mechanik unverändert nach P3-J. **`__AUTH_MODE__` steht während der Abnahme auf
`both` und am Ende dieses Steps auf `oauth`.**

**Inbetriebnahme, in dieser Reihenfolge** — die Reihenfolge ist der halbe Runbook:

1. `provision_user.py --space niklas`, dann `--space fabian`. TOTP-Seeds sofort in die
   Authenticator-Apps, QR aus der `otpauth://`-URI.
2. `export_auth_users.py | sudo systemd-creds encrypt --name=auth-users - /etc/sharefyx/auth-users.cred`
   — **immer als Pipe, nie über eine Zwischendatei** (P3 §2.1, gleicher Grund, höherer Einsatz:
   diesmal sind es echte Seeds).
3. `install_units.sh`, `systemctl daemon-reload`, `systemctl restart sharefyx-mcp`.
4. `oauth_smoke.py` gegen `127.0.0.1:8765` — **bevor** irgendjemand einen Connector anfasst.
5. Discovery von außen: beide `.well-known`-Dokumente per `curl` abrufen und `resource` gegen
   die geplante Connector-URL halten.
6. Connector in **beiden** Accounts neu anlegen mit `https://<host>/mcp`, ohne Client-ID,
   ohne Secret. Connect drücken, Passwort + TOTP eingeben, Consent bestätigen.
7. Abnahmematrix fahren (unten).
8. **Schnitt:** `SPACE_AUTH_MODE=oauth`, `install_units.sh`, `restart`,
   `issue_token.py --revoke niklas` und `--revoke fabian`, `export_space_map.py` erneut,
   `spaces.cred` neu schreiben, `restart`. Dann `TokenPathASGI` und `AuthModeASGI` aus dem Code
   entfernen und `SPACE_AUTH_MODE` auf zwei Werte reduzieren — **Codeentfernung im selben
   Commit wie die Abnahme**, sonst bleibt sie liegen.

**Abnahmematrix** (Protokoll nach P2/P3-Konvention, mit Belegen statt Behauptungen):

| # | Prüfung | Erwartung | Braucht Fabian |
|---|---|---|---|
| 1 | `/health` von außen | unverändert, unauthentifiziert | nein |
| 2 | `POST /mcp` ohne Token | **401** mit korrektem `WWW-Authenticate` | nein |
| 3 | Discovery von außen | beide `.well-known` liefern, `resource` exakt | nein |
| 4 | Connect `niklas` | DCR → Consent → Tool-Aufruf erfolgreich | nein |
| 5 | Falsches Passwort | generische Meldung, keine Enumeration | nein |
| 6 | Fünf Fehlversuche | Sperre greift, `authctl unlock` hebt sie | nein |
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

**Terminrisiko, ehrlich notiert (Nikinger-Entscheidung 2026-07-28):** Die Zeilen **14 und 15
brauchen den Kollegen** und sind damit ein Terminrisiko, das die Phase nicht blockieren soll.
Sie werden wie in P3 behandelt: Phase erreicht **🟡 code-complete**, sobald 14 von 16 Zeilen
bestanden sind; **✅** erst nach den beiden Zwei-Personen-Zeilen. **P5 darf bei 🟡 beginnen.**
Was **nicht** verschoben werden darf, ist Schritt 8 — der Schnitt. Ein `both`-Modus, der auf
einen Termin wartet, ist genau das Risiko, dessentwegen P4 vorgezogen wurde.

**Done when:** 14 von 16 bestanden, Schnitt vollzogen, Pfad-Token widerrufen, `TokenPathASGI`
entfernt, Protokoll geschrieben, `ROADMAP.md`/`docs/INDEX.md`/Phase-Head nachgezogen.

---

## §6 Akzeptanzkriterien der Phase

1. **Die Connector-URL enthält kein Geheimnis mehr.** `https://<host>/mcp`, in beiden Accounts.
2. Ein unauthentifizierter Aufruf erzeugt einen **401 mit `WWW-Authenticate`** — und Claude
   zeigt daraufhin einen Connect-Button, keinen Fließtext.
3. **Code-Replay und Refresh-Replay töten die Token-Familie**, beide belegt durch einen Lauf,
   nicht durch einen Test allein.
4. **Kein Klartext-Geheimnis** in der Datenbank, im journald, im Repo oder in einer Datei —
   per `grep` belegt, nicht behauptet.
5. **Zwei Faktoren am Login**, Passwort nach Argon2id mit belegten Parametern, TOTP gegen die
   RFC-Testvektoren geprüft.
6. **Nutzer-Enumeration ist nicht möglich:** falsches Passwort und unbekannter Space liefern
   dieselbe Antwort, und die Laufzeiten liegen in derselben Größenordnung.
7. **Die Registrierung ist nicht offen:** ein fremder Redirect-Origin wird abgelehnt.
8. `pytest` grün — die Ausgangszahl aus Step 0 plus die neuen, **ohne Netz, ohne Keyring, ohne
   echten `DATA_ROOT`, ohne echten Tunnel**.
9. **Die sechs Tools sind unverändert.** `git diff` auf `tools.py`, `permissions.py`,
   `server.py`, `storage/` ist **leer**. Das ist die Einlösung des P2-Seams.
10. **`SPACE_AUTH_MODE` ist `oauth`, `TokenPathASGI` ist gelöscht**, beide Pfad-Token widerrufen.
11. Doku-Pflichten aus §7 erfüllt — im jeweiligen Step-Commit, nicht nachgereicht.

---

## §7 Doku-Pflichten (Hard Rule 8)

| Datei | Was |
|---|---|
| `docs/INDEX.md` | Zeilen für `phase4_auth_plan.md`, `phase4_auth/CLAUDE.md`, `phase4_auth/SESSIONS_ARCHIVE.md`, später `P4_ABNAHME_*.md`; P3-Block auf 📗/📦; neuer Abschnitt „Active phase (4)" |
| Root-`CLAUDE.md` | „Current state" auf P4 · **R5 abschließend korrigieren** („Auth v0 … gültig bis P4" → *abgelöst am \<Datum\>, siehe P4*) · Hard Rule 1 um den Satz ergänzen, dass ab P4 **echte** Geheimnisse (TOTP-Seeds) im Keyring liegen, nicht nur Hashes · die entschiedene Zeile „eigener Prozess oder eigener Space" streichen (Handover §5, Fund 4) · `down:` umhängen |
| `ROADMAP.md` | P4 auf 🔄 bzw. 🟡/✅ · **P3-Scope-Zeile korrigieren** (Cloudflare → Tailscale Funnel, `LoadCredential` → `LoadCredentialEncrypted`) · Paketname `auth` → `authserver` mit datierter Begründung (P4-B) · unter „Zurückgestellt": P3-E-Trigger als gefallen vermerken, CIMD als DCR-Nachfolger aufnehmen |
| `README.md` | Vollständig auf Stand ziehen (Step 0) · Architekturdiagramm: Cloudflare → Tailscale Funnel, Auth-Zeile → OAuth 2.1 · neuer Abschnitt **„Anmeldung und Nutzerverwaltung"** (`provision_user.py`, TOTP einrichten, Passwort ändern, `authctl.py unlock`) · unter „Bewusst akzeptierte Kompromisse": Token-in-URL streichen, **Restrisiko R3 aus §9 aufnehmen** |
| `phase3_edge/CLAUDE.md` | „Tailscale ist nicht installiert" korrigieren (Handover §5, Fund 2) · Verweis auf die neue Unit-Fassung |
| `phase4_auth/CLAUDE.md` | Phase-Head: Scope, P4-A–P4-R in Kurzform, Modultabelle Steps 0–7, Rotationsregel mit Skriptverweis, Runbooks **„Connector lässt sich nicht verbinden"** und **„Zweiter Faktor verloren"**, Absatz **„Warum TOTP mit SHA-1 und nicht SHA-256"**, Absatz **„Warum Claude Code hier nicht funktioniert und das Absicht ist"**, Absatz **„Was diese SQLite von Hard Rule 2 unterscheidet"** |

---

## §8 Was P4 explizit NICHT tut

Client ID Metadata Documents · DPoP (RFC 9449) und mTLS (RFC 8705) · JWT-Access-Token, JWKS,
Introspection (RFC 7662), Revocation-Endpunkt (RFC 7009) · Claude Code mit Loopback-Redirect ·
Recovery-Codes · WebAuthn/Passkeys · mehr als zwei Scopes, Step-up-Autorisierung · Lazy-Auth mit
öffentlichen Tools · MCP-Revision 2026-07-28 · `fastmcp` 4 · D6 · REST/UI (P5) · feingranulare
Lese-Rechte · Monitoring, Alerting, Off-site-Backup · Änderungen an `tools.py`,
`permissions.py`, `server.py`, `storage/*`.

**Zwei davon sind keine Auslassungen, sondern anerkannte Lücken** — sie stehen deshalb auch in
§9 als Restrisiko: DPoP/mTLS (RFC 9700 empfiehlt Sender-Constraining) und WebAuthn (stärker als
TOTP). Beide scheitern am Client, nicht am Aufwand.

**Zu Claude Code, ausdrücklich und mit Begründung** (Nikinger-Entscheidung 2026-07-28: nicht in
P4, nicht in P5, eigene spätere Phase). Dass Claude Code den Adapter *heute* bedienen kann,
liegt daran, dass der Pfad-Token gar keine Client-Fähigkeit verlangt — die URL trägt das
Geheimnis, es gibt keinen Fluss zu beherrschen. Nach dem Schnitt in Step 7 entfällt das. Ein
späterer Support ist **kein Allowlist-Eintrag**, sondern vier Dinge:

1. `http`-Schema für Loopback in `redirect_uri_allowed()` zulassen (heute: nur `https`).
2. Eine **zweite** Vergleichsregel mit ignoriertem Port nach RFC 8252 §7.3 — P4-K („exakt und
   byteweise") gilt dann nicht mehr universell.
3. `application_type: "native"` annehmen statt ablehnen.
4. **Vermutlich CIMD statt DCR**, weil Claude Code sich über ein Client ID Metadata Document
   identifiziert. Das ist der teure Punkt: das CIMD-Flag in den AS-Metadaten schaltet **auch die
   gehosteten Oberflächen** von DCR auf CIMD um. Die Erweiterung wäre also **nicht additiv**,
   sondern ein Austausch des Weges, den P4 baut und abnimmt.

Dazu eine Eigenschaft, die Konfiguration nicht heilt: bei Loopback-Redirects kann jeder lokale
Prozess einen Port belegen und sich als der legitime Client ausgeben. Die MCP-Auth-Spec verlangt
deshalb, dass der Consent-Screen den Redirect-Host deutlich anzeigt, und empfiehlt eine
zusätzliche Warnung, wenn ausschließlich Loopback-Adressen registriert sind — also noch ein
Stück der Wegwerf-UI, die P5 ohnehin ersetzt.

**Deshalb ist die richtige spätere Form vermutlich nicht „Claude Code am selben AS", sondern ein
eigenes Werkzeug** (Plugin, lokaler Proxy, oder ein `authctl`-Befehl, der ein langlebiges
Gerätetoken ausstellt). Diese Frage gehört in eine Planungssession, nicht in einen Nachtrag zu
P4. Der Seam dafür steht in §2.6.

Wer während P4 anfängt, eines dieser Themen „schon mal vorzubereiten": **stop.** Der häufigste
Weg, eine Phase zu versenken, ist das Vorziehen der nächsten.

---

## §9 Risiken und `[VERIFY]`-Register

**Risiken**

1. **Der Fehlschlag ohne Fehlermeldung.** Stimmt `resource` im PRM nicht exakt mit der
   Connector-URL überein, oder fehlt der `WWW-Authenticate`-Header, meldet Claude nur
   „Couldn't reach the MCP server". Gegenmittel: Prüfung 3 der Abnahmematrix läuft **vor**
   Prüfung 4, und `oauth_smoke.py` trennt Server- von Client-Fehlern.
2. **Der Discovery-Cache.** Claude cacht die Metadaten global, per URL, rund fünf Minuten.
   Eine Metadatenkorrektur wirkt also verzögert — wer in dieser Zeit dreimal umbaut,
   diagnostiziert Gespenster. Gegenmittel: nach jeder Metadatenänderung fünf Minuten warten,
   und das steht im Runbook.
3. **Bearer-Token bleiben Bearer-Token (Restrisiko).** RFC 9700 empfiehlt Sender-Constraining
   über DPoP oder mTLS. Der Client unterstützt beides nicht. Ein abgeflossener Access-Token ist
   bis zu 60 Minuten nutzbar, ein Refresh-Token bis zur nächsten Rotation. Gegenmittel und
   ihre Grenze: kurze Lebensdauer, Rotation mit Reuse-Erkennung, sofortige Widerrufbarkeit über
   `authctl.py`. **Das gehört in `README.md` unter die akzeptierten Kompromisse** — es ist der
   direkte Nachfolger des Satzes über den Token in der URL.
4. **Der öffentliche Login.** Ein Passwortfeld hinter einem CT-auffindbaren Hostnamen. Gegenmittel:
   TOTP, Argon2id, Fehlversuchsbremse, keine Enumeration. Restrisiko: gezieltes Aussperren
   eines Nutzers.
5. **Die Zwei-Personen-Abnahme.** Zeilen 14/15 hängen am Kollegen. Bewusst kein Blocker
   (Step 7), aber ein dokumentiertes Terminrisiko — Rule 4 wurde unter OAuth dann eben noch
   nicht live geprüft, und das steht so im Protokoll statt es zu verschweigen.
6. **Vergessener Restart.** Unverändert aus P3, jetzt mit zwei Credentials statt einem. Ein
   neu ausgegebenes Passwort ohne `systemctl restart` erscheint als „Anmeldung fehlgeschlagen"
   und wird am falschen Ende gesucht. Eigener Schritt im Runbook.
7. **Uhrzeitdrift.** TOTP scheitert stumm. `timedatectl` gehört in `diagnose.sh`.
8. **Argon2 auf einer kleinen VM.** 19 MiB je Anmeldung sind harmlos; 19 MiB × parallele
   Rate-Limit-Umgehungsversuche sind es nicht. Die Bremse aus §2.7 greift **vor** dem
   Argon2-Aufruf — außer im Enumerationsschutz-Pfad, der genau einen Dummy-Durchlauf kostet.
9. **Schema-Migration.** `auth.sqlite3` ist autoritativ (P4-I) und **nicht** aus Dateien
   rekonstruierbar. Ein späteres Feld braucht eine echte Migration. Deshalb `schema_meta` ab
   Zeile eins — nachgerüstete Versionierung ist Archäologie.

**`[VERIFY]`-Register** (bei Ausführung auflösen und im Session-Block beantworten)

| # | Was | Wo im Plan |
|---|---|---|
| V14 | Anthropic-Auth-Doku gegenlesen: Callback-URL, DCR-Verhalten, Timeouts, Content-Types, `offline_access`-Regel | §0.6, Step 4 |
| V15 | Aktuelle `argon2-cffi`-Major → **exakt** pinnen | P4-R, Step 1 |
| V16 | `dev_install.sh` nimmt `phase4_auth/` auf, ohne geändert zu werden | §1.2, Step 1 |
| V17 | Argon2id-Laufzeit auf der VM (Ziel 50–250 ms), RAM-Budget | §2.5, Step 2 |
| V18 | `timedatectl show -p NTPSynchronized` == `yes` | §2.5, Step 2 |
| V19 | Exakte Form des `WWW-Authenticate`-Headers, die Claude akzeptiert | §3.1, Step 6/7 |
| V20 | Ausgangs-Testzahl (~168 laut Handover) | Step 0 A |
| V21 | `auth.sqlite3` ist gitignored | Step 1 |
| V22 | systemd ≥ 235 für `StateDirectory=`; Verzeichnis wird mit 0700 angelegt | Step 7 |
| V23 | Funnel reicht `/.well-known/*` durch (404 vor Step 4, 200 danach) | Step 0 D, Step 4 |
| V24 | Reale Zeilennummern aller Anker in `mcpserver/{asgi,context,app,config}.py` | §3, Step 6 |
| V25 | `fastmcp`-Versionslage: ist der P3-E-Trigger gefallen? **Nur notieren, nicht handeln** | Step 0 D |
| V26 | Geerbt aus P3: **V10** (Größenbudget `search_items`), **V11** (MCP-Revision), **V12** (Datenlimit Uplink), **V13** (`diagnose.sh`-Grep) | Step 0 C |

---

## §10 Was nach P4 offen bleibt (für den Closeout-Handover)

- **Reboot-Nachweis aus P3** — weiterhin passiv, weiterhin die Bedingung für ✅ bei P3.
- **Zwei-Personen-Zeilen 14/15**, falls in Step 7 nicht erreicht.
- **MCP-Revision 2026-07-28 + `fastmcp` 4** — Trigger gefallen, eigene Mini-Phase, vor oder
  nach P5 zu terminieren. Berührt Transport und Lifecycle, nicht Auth.
- **CIMD** als Nachfolger der DCR — die Draft-Spec zeigt in diese Richtung, der Aufwand ist
  klein, der Nutzen bei zwei Nutzern gering. Kein Termin.
- **DPoP** — sobald der Client es spricht. Bis dahin Restrisiko 3.
- **D6**, **Lese-Rechte zwischen Spaces**, **Off-site-Backup**, **Monitoring** — unverändert
  zurückgestellt.
- **P5 (Web-UI)** — die Login-Oberfläche aus P4 ist ihr erster Kunde, nicht ihr Vorbild.
