---
status: snapshot
purpose: Ausführungsreifer Plan für Phase 5 (Web-UI + REST-API + Auth-Selbstverwaltung) — gelockte Entscheidungen P5-A–P5-Z, Steps 0–9, Abnahmematrix, [VERIFY]-Register V27–V38
read-when: vor dem ersten Claude-Code-Commit der Phase 5, dann je Step der zugehörige §5-Abschnitt
detail: L3
up: ../../ROADMAP.md
down:
  - ./PHASE4_CLOSEOUT_HANDOVER.md             # Herkunft: offene Entscheidungen §4.1–§4.5, [VERIFY]-Bilanz V14–V26
  - ./phase4_auth_plan.md                     # P4-A–P4-R, normative Grundlage §0.5, Anthropic-Vorgaben §0.6
  - ./P4_SECURITY_REVIEW_2026-07-29.md        # S2–S8 im Wortlaut — vor Step 1 lesen
  - ../../phase4_auth/CLAUDE.md               # Runbooks, authctl-Fallstricke, O1
updated: 2026-08-02
---
# Phase 5 — Web-UI, REST-API und Auth-Selbstverwaltung (Plan)

> **Dieses Dokument ist bewusst groß** (deutlich über dem 40-KB-Softcap, Statusglyph 📕). Es ist
> ein datierter Snapshot, kein lebendes Dokument — die Softcap-Regel aus
> `docs/DOC_LAYERS_CONVENTION.md` gilt für L2-Bodies, nicht für 📕/📦. Der Oversize-Check
> (`find . -name "*.md" -size +40k`) muss diese Datei als 📕 finden, das ist korrekt.
>
> **Geschrieben gegen den Drive-Snapshot `2026_08_01_sharefyx-main`**, nicht gegen ein
> Live-Repo. Jede Aussage über den Repo-Zustand ist erst wahr, wenn `git status`/`pytest` sie
> bestätigt — Step 0 tut genau das. Symbolnamen in diesem Plan sind aus dem Snapshot gelesen,
> **Zeilennummern nicht**: die verdrahtet Claude Code beim Ausführen (V27).

---

## §0 Rahmen

### 0.1 Mission

**Menschen benutzen das System ohne SSH und ohne Editor.**

Das zerfällt in zwei Dinge, die getrennt beweisbar sind:

1. **Ein Mensch kann sein Konto selbst verwalten.** Erstvergabe über eine Einladung, Passwort
   ändern, TOTP einrichten, Wiederherstellung, Connector-Verbindungen sehen und kappen — alles
   im Browser, ohne Neustart des Dienstes.
2. **Ein Mensch kann Notizen und Aufgaben im Browser lesen und schreiben**, über eine REST-API,
   die denselben Storage-Kern benutzt wie die sechs MCP-Tools.

Punkt 1 ist ein Umbau am Auth-Kern, Punkt 2 ist neue Oberfläche. Sie stehen hintereinander,
nicht nebeneinander.

### 0.2 Was P5 als gegeben übernimmt (nicht neu herleiten)

| Was | Wo es im Wortlaut steht |
|---|---|
| Hard Rules 1–8, Bauprinzip „der Server ist dumm", R1–R6 | Root-`CLAUDE.md` |
| Frontmatter-Schema, `Item`/`ItemSummary`/`SpaceInfo`/`SearchResult`/`IndexStats` | `phase1_storage/storage/models.py` |
| `Store`-Signaturen, Konfliktverhalten, `_SYSTEM_MANAGED_FIELDS`, `extra`-Round-Trip | `phase1_storage/storage/store.py` |
| Sechs Tools, Rule-4-Architektur (Schreib-Tools ohne `space`-Parameter) | `phase2_mcp/mcpserver/tools.py` |
| `create_app()`-Verdrahtung, `OAuthConfig`, `BearerAuthASGI` | `phase2_mcp/mcpserver/{app,asgi}.py` |
| OAuth-Fluss, `AuthStore`-Schema, Argon2id/TOTP-Bausteine | `phase4_auth/authserver/*` |
| Alle 18 gelockten P4-Entscheidungen | `docs/concepts/phase4_auth_plan.md` §0.7 |
| Betriebswahrheiten O1, `STATE_DIRECTORY`, `ALLOWED_HOSTS`, DCR-Bremse | `docs/concepts/PHASE4_CLOSEOUT_HANDOVER.md` §2 |

**ROADMAP-Scope P5 (unverändert gültig):** DRIN = REST-API über demselben Storage-Kern, UI
gegen diese API. DRAUSSEN = Realtime/Collaboration, Anhänge, Mobile-App.

**Ergänzung dieser Planungssession:** die Auth-Selbstverwaltung (§0.1 Punkt 1) steht in der
ROADMAP nicht — sie kommt aus dem P4-Handover §4.1 und ist hier ausdrücklich in den Scope
aufgenommen worden (Nikinger-Entscheidung 2026-08-02, Antwort A1). Ohne sie ist die UI eine
Oberfläche auf einem Konto, das nur per SSH existiert.

### 0.3 Normative Grundlage

Fortschreibung von `phase4_auth_plan.md` §0.5, ergänzt um das, was P5 neu berührt:

| Quelle | Wofür in P5 |
|---|---|
| **BSI IT-Grundschutz CON.10** „Entwicklung von Webanwendungen" | Session-Management, CSRF (A15), Eingabevalidierung, Ausgabekodierung, Re-Authentisierung bei wichtigen Änderungen |
| **BSI IT-Grundschutz APP.3.1** „Webanwendungen und Webservices" | Sichere HTTP-Konfiguration (A21: Cookies mit `secure`/`SameSite`/`httponly`), Grenzwerte für Anmeldeversuche, Upload-Restriktionen (hier: Begründung, warum Uploads draußen bleiben) |
| **BSI TR-02102-1 (2026-01)** | AES-256-GCM für die Verschlüsselung der TOTP-Seeds at rest; Argon2id unverändert aus P4 |
| **OWASP Session Management Cheat Sheet** | Token-Entropie, `__Host-`-Präfix, Idle-/Absolut-Timeout, Invalidierung serverseitig |
| **OWASP Password Storage Cheat Sheet** | Argon2id-Parameter (unverändert, `ARGON2_TIME_COST = 8`, V17) |
| **draft-ietf-oauth-browser-based-apps-26** §7.1 | Begründung, warum die UI **kein** OAuth-Client wird |
| **RFC 6265bis** §4.1.3 | `__Host-`-Präfix-Semantik |
| **RFC 9700 / 9728 / 8414 / 7591 / 7636 / 6238 / 9207** | unverändert aus P4 |

`[VERIFY]` **V33:** Die Anthropic-Connector-Doku (`phase4_auth_plan.md` §0.6) ist vor Step 1
erneut gegenzulesen. Sie hat sich seit V14 (2026-07-28) mit hoher Wahrscheinlichkeit bewegt,
siehe §0.4.

### 0.4 Externe Lage, die sich seit dem P4-Handover geändert hat

**Die MCP-Spec-Revision `2026-07-28` ist seit dem 2026-07-28 final**, nicht mehr Release
Candidate. Für dieses Projekt relevant:

- Zustandsloser Kern: `initialize`/`initialized` und `Mcp-Session-Id` entfallen.
- `Mcp-Method`/`Mcp-Name` werden Pflicht-Header.
- MRTR ersetzt server-initiierte Requests über offene Streams.
- **DCR ist formal deprecated zugunsten CIMD**, mit einer Mindestfrist von zwölf Monaten.
- `iss` nach RFC 9207 ist Pflicht (hat der Server bereits), `application_type` bei DCR ebenfalls.
- Roots/Sampling/Logging und der HTTP+SSE-Transport sind deprecated.
- **FastMCP 4 liegt bislang nur als `4.0.0b1` (Beta) vor.**

**Konsequenz für P5 (gelockt als P5-C):** die Migration bleibt eine eigene Mini-Phase **nach**
P5. Begründung in zwei Sätzen: der laufende Server spricht `2025-11-25`, neue Clients handeln
herunter, und ein Beta-Framework unter einen gerade erst live bewiesenen Auth-Server zu
schieben, tauscht ein bekanntes Risiko gegen ein unbekanntes. Der Preis dafür ist, dass die
Zwölf-Monats-Frist der DCR-Deprecation ab jetzt läuft — das gehört in den Closeout-Handover,
nicht in diese Phase.

**Was P5 dafür schuldet:** kein Code in dieser Phase darf eine Annahme über MCP-Transport,
Session-Lifecycle oder DCR treffen. Die UI hängt am Storage-Kern und an `AuthStore`, nicht am
MCP-Adapter. Akzeptanzkriterium §6.18 prüft das.

### 0.5 Gelockte Entscheidungen

Alle Entscheidungen stammen aus der Browser-Planungssession vom 2026-08-02 (Frage-Antwort-Runde
im Chat, Antworten des Nikingers wörtlich übernommen). **Gelockte Entscheidungen bleiben
gelockt** — widersprechende Evidenz wird ein Befund für den Menschen, nie eine stille
Abweichung.

| # | Thema | Lock | Herkunft |
|---|---|---|---|
| **P5-A** | Phasenschnitt | **Eine Phase**, Verzeichnis `phase5_ui/`, Paket `webui`. **Zwei Blöcke:** Block A = Steps 0–4 (Sicherheit + Auth-Selbstverwaltung), Block B = Steps 5–9 (REST-API + UI). **Harter Gate:** Block B beginnt erst, wenn Block A live-verifiziert ist (Abnahmezeilen 1–9). | A1 |
| **P5-B** | Reichweite in fremden Code | P5 **darf** `authserver/` und `mcpserver/{app,asgi}.py` anfassen. `storage/`, `mcpserver/tools.py`, `mcpserver/permissions.py`, `mcpserver/server.py` bleiben **tabu** — `git diff` darauf ist am Phasenende **leer** (§6.17). | A3 |
| **P5-C** | MCP-Revision 2026-07-28 / FastMCP 4 | Eigene Mini-Phase **nach** P5. P5 baut nichts, was den Umstieg verteuert. | A2, §0.4 |
| **P5-D** | Auth-Modell der UI | **Eigene serverseitige Cookie-Session. Kein OAuth für die UI.** Der Authorization Server bleibt exklusiv für MCP-Clients. Begründung: `draft-ietf-oauth-browser-based-apps-26` §7.1 — Frontend und API auf gemeinsamer Origin brauchen kein OAuth; eine OAuth-Schicht wäre hier Selbstzweck und würde die Audience-/Scope-Fläche verdoppeln. | B1 |
| **P5-E** | Session-Cookie | Name `__Host-sfx_session`. `Secure; HttpOnly; SameSite=Strict; Path=/`, kein `Domain`. Wert: 256-Bit `secrets.token_urlsafe(32)`, gespeichert als `sha256`-Hex. Idle-Timeout **12 h**, Absolut-Timeout **7 d**. ID-Rotation bei jedem erfolgreichen Login und bei jeder Re-Authentisierung. | B2 |
| **P5-F** | Trennung der beiden Auth-Wege | **`/mcp` akzeptiert niemals Cookies** (nur `Authorization: Bearer`). **`/api` und `/ui` akzeptieren niemals Bearer-Token** (nur Cookie-Session). Beide Richtungen sind Tests, nicht Konvention (§6.6). | B1/B2 |
| **P5-G** | UI-Session ≠ OAuth-Consent | Eine bestehende UI-Sitzung kürzt den OAuth-Consent **nicht** ab. `/oauth/authorize` liest keine Cookies und verlangt bei jeder Connector-Autorisierung Passwort **und** TOTP. Das hält P4-O intakt und macht `SameSite=Strict` überhaupt erst möglich. | B3 |
| **P5-H** | CSRF | Double-Submit-Token (Cookie-gebundenes `csrf_hash` in der Session, Wert im Formularfeld bzw. `X-CSRF-Token`-Header) **plus** Herkunftsprüfung (`Origin`, ersatzweise `Sec-Fetch-Site`) auf jeder Methode außer `GET`/`HEAD`. Fehlt eines von beiden → `403`, keine Zustandsänderung. BSI CON.10.A15. | B2 |
| **P5-I** | Nutzerakten-Speicher | Nutzerakten wandern aus Keyring/`systemd-creds` in die bestehende `auth.sqlite3`, Tabelle `users`. Ab dem Migrationsschritt ist **SQLite autoritativ**; Keyring/Credential sind nur noch Bootstrap-Quelle und werden nach der Verifikation widerrufen. Erweiterung der benannten P4-I-Ausnahme von Hard Rule 2. | C1 |
| **P5-J** | Geheimnisse at rest | **TOTP-Seeds werden verschlüsselt gespeichert** (AES-256-GCM, BSI TR-02102-1), Schlüssel als drittes systemd-Credential `auth-dek`. AAD = Space-Name, damit ein Seed nicht zwischen Zeilen getauscht werden kann. Neue Abhängigkeit `cryptography`, exakt gepinnt (V28). | C2 |
| **P5-K** | Was **nicht** verschlüsselt, sondern gehasht wird | Einladungstoken, Recovery-Codes und Session-IDs sind **hochentropische Zufallswerte** → `sha256` wie in `authserver/crypto.py :: hash_secret`, **nicht** Argon2id. Begründung steht bereits im Docstring von `crypto.py`: „ein 256-Bit-Zufallswert ist nicht ratbar, ein Passwort schon". Argon2id bleibt ausschließlich für Passwörter. *(Korrektur gegenüber der Q&A-Empfehlung, die für Recovery-Codes Argon2id vorschlug — ein Argon2-Hash ist nicht als Primärschlüssel nachschlagbar, und die Entropie macht ihn unnötig.)* | C5 + Korrektur |
| **P5-L** | Kein Neustart für Kontoänderungen | `load_users()` als Startzeit-Lesevorgang wird durch `authserver/userdir.py :: UserDirectory` ersetzt, das bei **jedem** Zugriff aus SQLite liest. Damit ist Befund **O1** geschlossen. | C1 |
| **P5-M** | Erstvergabe | **Einmal-Einladung**, kein Initialpasswort. `authctl.py invite <space>` gibt genau einmal einen Link aus (TTL **60 min**, single-use). Fluss: Passwort setzen → TOTP-Seed genau einmal anzeigen → mit einem Code verifizieren → Recovery-Codes genau einmal anzeigen → Konto aktiv. Selbstregistrierung existiert nicht. | C4 |
| **P5-N** | Recovery | **10 Recovery-Codes**, Format `xxxxx-xxxxx` (Base32, ≥ 50 Bit), einmalige Anzeige, Verbrauch markiert. Ein Recovery-Code ersetzt **den TOTP-Faktor**, nie das Passwort. Revidiert P4-H bewusst und datiert. | C5 |
| **P5-O** | Passwortpolitik | Minimum **12** Zeichen, Maximum **128**, keine Komplexitätsregeln, keine Rotationspflicht. Abgleich gegen eine **lokale** Blocklist (Datei im Repo) — der Server ruft nichts nach außen. | C6 |
| **P5-P** | Re-Authentisierung | Passwortwechsel, TOTP-Neueinrichtung, Recovery-Code-Neuausgabe, Beenden fremder Sessions und Widerruf einer Connector-Verbindung verlangen **Passwort + TOTP-Code** im selben Formular. BSI CON.10. | B3, C6 |
| **P5-Q** | Folgen eines Passwortwechsels | Alle Token-Familien des Space werden widerrufen (`revoke_family(..., "password_changed")`) **und** alle UI-Sessions außer der aktuellen beendet. Die UI sagt das **vor** dem Absenden an, nicht danach. | C7 |
| **P5-R** | Auth-Backup | `auth.sqlite3` bekommt ein **eigenes, verschlüsseltes Backup** (`sharefyx-authbackup.timer`), getrennt vom `DATA_ROOT`-`git bundle`. Geheimnisse landen nicht im Daten-Bundle. Sieben Generationen, `restore_auth_check.sh` als Nachweis. | C3 |
| **P5-S** | Sicherheitsbefunde | **S2–S8 werden vollständig geschlossen**, nicht nur S3/S4/S6. Das Register geht auf null. | F3 |
| **P5-T** | UI-Bauart | Eine statische Single-File-Anwendung (`app.html` + `app.css` + `app.js`), **kein Build-Step, kein npm, kein CDN**. Ausgeliefert vom selben Prozess unter `/ui`. CSP ohne `unsafe-inline` und ohne `unsafe-eval`. | D1 |
| **P5-U** | Editor | Markdown-Textarea mit Live-Vorschau. Formatierhilfen (Überschriften, Listen, Tabellen, Fett/Kursiv, Code, Link) fügen **Markdown-Syntax ein**, kein WYSIWYG, kein `contenteditable`. | D2 |
| **P5-V** | Notizheft-Beispiel | **Neubau mit Ernte.** Übernommen werden Layout-Ideen, `sanitizeHtml` und `markdownToHtml` (letzteres um Tabellen erweitert). Verworfen werden Vault-Krypto (`crypto.subtle`, PBKDF2, AES-GCM clientseitig), `localStorage`/IndexedDB als Speicher und `connect-src 'none'`. | D3 |
| **P5-W** | Zielgerät | **16:9-Desktop first**, ein einziges Layout, Referenzbreite ≥ 1280 px. Bis 1024 px darf es enger werden, darunter ist es nicht kaputt, aber auch nicht optimiert. **Eine Mobilversion ist ausdrücklich nicht Teil dieser Phase.** | D4 |
| **P5-X** | Designrichtung | Dunkel-first. Apples Formensprache vor „Liquid Glass" (Klarheit, Zurücknahme, Tiefe durch Hierarchie statt Effekt) über dem Aufbau und der Farbwelt der My-BMW-App. Vollständiges Token-System in §4. Nur **dunkel** in v1; die Tokens sind so gebaut, dass ein helles Thema später ein Token-Tausch ist. | D5 |
| **P5-Y** | Fremde Inhalte in der UI | Fremde Bodies werden **nie serverseitig zu HTML gerendert**. Die API liefert reinen Text; das Rendering passiert im Browser durch den eigenen Renderer plus Sanitizer. Fremde Spaces sind in der UI read-only, und zwar durch **Abwesenheit** der Schreib-Bedienelemente, nicht durch deaktivierte Buttons — dasselbe Prinzip wie Rule 4 im Toolschema. | D6 |
| **P5-Z** | Format-Seam | Ein `[SEAM]`-Frontmatter-Feld `format` (Default `markdown`). **Es wird kein zweites Format implementiert.** Der Seam braucht **keine Zeile in `storage/`**: unbekannte Frontmatter-Felder landen verlustfrei in `Item.extra` (P1-Entscheidung A) — belegt durch einen Round-Trip-Test. | E1 + Befund |
| **P5-AA** | Anhänge/Uploads | **Draußen.** Begründung im Plan festgehalten, nicht nur im Handover: BSI APP.3.1 verlangt vorab festgelegte Größen-, Typ- und Ablageregeln, und Rule 4 hat für einen fremden Nicht-Text-Body noch keine Antwort (`<untrusted_content>` wrappt Strings). Das ist eine eigene Phase. | E2 |
| **P5-AB** | Deployment | **Kein Blue/Green im Betrieb.** Gebaut werden: Release-Verzeichnisse mit `current`-Symlink, `deploy.sh` mit Pre-Deploy-Backup und Health-Gate, `rollback.sh`, und eine **Staging-Instanz** auf einem zweiten Port, nur über Tailscale **Serve** (tailnet-intern, nicht Funnel), mit geklontem `DATA_ROOT`. Downtime beim Umschalten ist ausdrücklich akzeptiert. | F1 |
| **P5-AC** | Blue/Green-Seam | Als benannter `[SEAM]` vorbereitet, nicht betrieben: `deploy.sh` kapselt den Ziel-Port an genau einer Stelle, und der Weg (Template-Unit + `tailscale serve`-Zielwechsel) ist im Phase-Head dokumentiert, damit er nicht neu recherchiert werden muss. **Alles bleibt auf einer VM.** | F2 |
| **P5-AD** | Messung statt Schätzung | `scripts/ui_budget.py` misst reale Antwortgrößen der API und der statischen Assets. Löst **V10** (Größenbudget) auf und liefert Zahlen für **V12** (Uplink-Datenlimit). Bis dahin wird konservativ geplant. | F6 |
| **P5-AE** | Abnahme | Eine gemeinsame Live-Abnahme am Ende: erst der Nikinger vollständig, dann Fabian im selben Durchgang („alles mit einem Mal"). | F7 |

### 0.6 Was P5 ausdrücklich **nicht** tut

- Keine Zeile in `storage/`, `mcpserver/tools.py`, `mcpserver/permissions.py`,
  `mcpserver/server.py` (P5-B).
- Kein zweites Dateiformat, keine Anhänge (P5-Z, P5-AA).
- Kein FastMCP-4-Umstieg, keine CIMD, kein DPoP (P5-C).
- Keine Mobilversion (P5-W).
- Kein Realtime, kein gleichzeitiges Bearbeiten, kein WebSocket. Optimistic Locking bleibt der
  einzige Konfliktmechanismus.
- Kein Löschen. `status: archived` bleibt die einzige Rücknahme.
- Keine Rechte zwischen Spaces jenseits von Rule 4. `Permissions.can_read` bleibt der Seam, den
  P5 benutzt, aber nicht ausbaut.
- Kein LLM, keine Zusammenfassung, kein Auto-Tagging — Bauprinzip.

---

## §1 Architektur

### 1.1 Ein Prozess, vier Adapter

```
                       Tailscale Funnel (TLS auf eigener Node)
                                    │
                         sharefyx-mcp.service (ein Prozess)
                                    │
        ┌───────────────┬───────────┴────────┬──────────────────┐
        │               │                    │                  │
  oauth_routes()    /health          Mount("/ui")        Mount("/mcp")
  (authserver)                    Mount("/api/v1")     BearerAuthASGI
        │                            (webui)                  │
        │                               │                     │
        └──────────► AuthStore ◄────────┘                     │
                    (auth.sqlite3)      │                     │
                                        └──► Store ◄──────────┘
                                          (DATA_ROOT, Dateien + Index + Git)
```

**Warum ein Prozess und nicht zwei:** zwei Prozesse würden gleichzeitig in dasselbe
Git-Repository, denselben SQLite-Index und dieselbe Auth-DB schreiben. `flock` schützt den
Dateischreibvorgang, aber `git commit` serialisiert sich nicht von selbst, und zwei Schreiber
auf einem `index.lock` sind ein Betriebsproblem, kein Architekturgewinn. Der Preis — Restart
trifft UI und MCP gleichzeitig — ist bei zwei Nutzern und akzeptierter Downtime (P5-AB) der
kleinere.

### 1.2 Paketgrenzen

| Paket | Verzeichnis | Darf importieren | Darf **nicht** importieren |
|---|---|---|---|
| `storage` | `phase1_storage/` | stdlib | alles andere im Projekt |
| `mcpserver` | `phase2_mcp/` | `storage`, `authserver` | `webui` |
| `authserver` | `phase4_auth/` | `storage`? **nein**, stdlib + `argon2` + `cryptography` | `mcpserver`, `webui` (P4-A/C bleibt gültig) |
| `webui` | `phase5_ui/` | `storage`, `authserver`, **genau ein Symbol aus `mcpserver`** | — |

**Die eine Ausnahme:** `webui` importiert `mcpserver.permissions.OwnSpaceWritable`.

Begründung: Rule 4 zweimal zu implementieren ist genau das Muster, das dieses Projekt an anderer
Stelle ausdrücklich ablehnt („zwei Kopien derselben Schutzregel sind schlimmer als eine",
`phase3_edge_plan.md` zur Token-Scrubbing-Regex). Ein Test hält die Kante schmal:
`test_webui_imports_exactly_one_mcpserver_symbol` grept das Paket und schlägt fehl, sobald ein
zweiter `mcpserver`-Import dazukommt.

`[VERIFY]` **V27:** exakte Klassen- und Methodennamen in `phase2_mcp/mcpserver/permissions.py`
(erwartet: `OwnSpaceWritable` mit `can_read`/`can_write`). Nicht geraten übernehmen — die Datei
lag in dieser Planungssession nicht vor.

### 1.3 Modulkarte `webui`

```
phase5_ui/
├─ pyproject.toml                 # Paket webui, wie phase4_auth/pyproject.toml
├─ CLAUDE.md                      # Phase-Head (L1-Card + Modultabelle + genau EIN Session-Block)
├─ SESSIONS_ARCHIVE.md            # ab dem zweiten Block, via scripts/rotate_session_block.sh
├─ webui/
│  ├─ __init__.py                 # __version__
│  ├─ config.py                   # UiSettings (Cookie-Name, TTLs, statisches Verzeichnis)
│  ├─ security.py                 # ui_security_headers(), CSRF, Herkunftsprüfung
│  ├─ sessions.py                 # SessionManager — Cookie ↔ AuthStore, kein SQL
│  ├─ reauth.py                   # require_reauth(): Passwort + TOTP in einem Schritt
│  ├─ pages.py                    # servergerendertes HTML: Login, Einladung, Fehler
│  ├─ routes_auth.py              # /ui/login, /ui/logout, /ui/invite/{token}
│  ├─ account.py                  # /api/v1/account/*
│  ├─ api.py                      # /api/v1/spaces, /items, /items/{id}, ...
│  ├─ serializers.py              # Item/ItemSummary → JSON, ISO-Daten, kein HTML
│  ├─ errors.py                   # ApiError → JSON-Fehlerkörper mit stabilen Codes
│  ├─ passwords_policy.py         # Längen-/Blocklist-Prüfung
│  ├─ blocklist.txt               # lokale Passwort-Blocklist (klein, im Repo)
│  └─ static/
│     ├─ app.html
│     ├─ app.css
│     ├─ app.js
│     └─ fonts/InterVariable-subset.woff2
├─ systemd/
│  ├─ sharefyx-authbackup.service
│  ├─ sharefyx-authbackup.timer
│  ├─ sharefyx-purge.service
│  ├─ sharefyx-purge.timer
│  └─ sharefyx-staging.service
├─ scripts/
│  ├─ deploy.sh
│  ├─ rollback.sh
│  ├─ restore_auth_check.sh
│  ├─ ui_budget.py
│  └─ ui_smoke.py                 # Gegenstück zu mcp_smoke.py/oauth_smoke.py
└─ tests/
   └─ test_*.py
```

### 1.4 Neue Module in `authserver` (P5-B erlaubt das)

| Modul | Zweck |
|---|---|
| `authserver/secretbox.py` | AES-256-GCM `seal()`/`open_()` mit AAD, Schlüssel aus Credential |
| `authserver/userdir.py` | `UserRecord`, `UserDirectory` — liest bei **jedem** Zugriff aus SQLite (P5-L) |
| `authserver/store.py` (erweitert) | Schema 1 → 2: `users`, `invites`, `recovery_codes`, `ui_sessions`; alle zugehörigen Methoden. **Kein SQL außerhalb dieser Datei** — die Regel aus P4 gilt weiter, auch für `webui` |

### 1.5 Route-Landkarte

Reihenfolge in `create_app()` ist bedeutsam (Starlette matcht von oben):

```python
routes  = list(oauth_routes(oauth.settings, oauth.store, oauth.users))   # unverändert
routes += webui_routes(ui_settings, auth_store, userdir, store, sessions) # NEU
routes.append(Route("/health", _health, methods=["GET"]))
routes.append(Mount("/mcp", app=bearer))
```

| Pfad | Methode | Auth | Antwort |
|---|---|---|---|
| `/ui/` | GET | keine (Shell), Daten erst über `/api` | `app.html` |
| `/ui/static/{path}` | GET | keine | statische Datei, `Cache-Control: public, max-age=31536000, immutable` bei gehashtem Dateinamen |
| `/ui/login` | GET/POST | keine → Session | HTML |
| `/ui/logout` | POST | Session + CSRF | 303 → `/ui/login` |
| `/ui/invite/{token}` | GET/POST | Einmaltoken | HTML |
| `/api/v1/me` | GET | Session | JSON |
| `/api/v1/spaces` | GET | Session | JSON |
| `/api/v1/items` | GET/POST | Session (+CSRF bei POST) | JSON |
| `/api/v1/items/{id}` | GET/PATCH | Session (+CSRF) | JSON, `409` bei Konflikt |
| `/api/v1/items/{id}/append` | POST | Session + CSRF | JSON |
| `/api/v1/items/{id}/archive` | POST | Session + CSRF | JSON |
| `/api/v1/account/password` | POST | Session + CSRF + Re-Auth | JSON |
| `/api/v1/account/totp/start` | POST | Session + CSRF + Re-Auth | JSON (Seed genau einmal) |
| `/api/v1/account/totp/confirm` | POST | Session + CSRF | JSON |
| `/api/v1/account/recovery-codes` | POST | Session + CSRF + Re-Auth | JSON (Codes genau einmal) |
| `/api/v1/account/sessions` | GET/DELETE | Session (+CSRF, Re-Auth bei DELETE) | JSON |
| `/api/v1/account/connectors` | GET | Session | JSON (Token-Familien) |
| `/api/v1/account/connectors/{family_id}` | DELETE | Session + CSRF + Re-Auth | JSON |

**Space-Auflösung:** kein Endpunkt nimmt den eigenen Space als Parameter entgegen. Er kommt aus
der Session. Schreib-Endpunkte haben **keinen** `space`-Parameter — dieselbe architektonische
Entscheidung wie bei den sechs Tools (Rule 4).

---

## §2 Block A — Sicherheit und Selbstverwaltung

### 2.1 Sicherheitsbefunde S2–S8 (P5-S)

Vollständiger Wortlaut in `docs/concepts/P4_SECURITY_REVIEW_2026-07-29.md` — **vor dem Fix
lesen**, dieser Plan ist die Umsetzung, nicht die Quelle.

| # | Fix, konkret |
|---|---|
| **S2** | `AuthStore.rotate_refresh()` bekommt einen zusätzlichen Parameter `client_id: str`. Innerhalb der bestehenden `BEGIN IMMEDIATE`-Transaktion wird `token_families.client_id` verglichen; Mismatch → `return None` (→ `invalid_grant`), **kein** Familien-Widerruf (ein falscher `client_id` ist kein Replay). `flows.issue_token()` reicht `client_id` durch. |
| **S3** | `OAuthTokenResolver.__init__(store, *, expected_resource: str)`. Nach `lookup_access_token` gilt: `record.resource != expected_resource` → `ResolveError`. `mcpserver/app.py :: create_app()` konstruiert mit `expected_resource=oauth.settings.resource`. |
| **S4** | Konstante `authserver/resolver.py :: REQUIRED_MCP_SCOPE = "space"`. `record.scope.split()` muss sie enthalten, sonst `ResolveError`. Ein Token mit nur `offline_access` verliert damit den Tool-Zugriff. |
| **S5** | `routes.py :: _authorize_response()` baut die Redirect-URL über `urllib.parse.urlsplit`/`urlencode`/`urlunsplit` und **mischt** vorhandene Query-Parameter, statt `f"{uri}?{query}"` zu bilden. |
| **S6** | Entfällt strukturell mit `UserDirectory.get()` → `UserRecord | None`. Ein unvollständiger Datensatz ist ein `None` mit `logger.warning`, kein `KeyError`. Der Enumerationsschutz greift wie bisher über `passwords.DUMMY_HASH`. |
| **S7** | `sharefyx-purge.service` + `.timer` (täglich, `Persistent=true`), ruft `authctl.py purge-expired` auf. `AuthStore.purge_expired()` wird um `ui_sessions` (absolut abgelaufen **oder** widerrufen älter als 7 d) und `invites` (abgelaufen oder konsumiert älter als 7 d) erweitert und gibt die Zählwerte je Tabelle zurück. |
| **S8** | `install_units.sh` sourced die Env-Datei nicht mehr blind: vorher `stat -c '%U %a'`, Abbruch wenn nicht `root` oder wenn gruppen-/weltschreibbar. Fehlermeldung nennt den erwarteten Zustand. |

### 2.2 Schema 2 der `auth.sqlite3`

`SCHEMA_VERSION` geht von `"1"` auf `"2"`. **Rein additiv** — vier neue Tabellen, keine
Änderung an bestehenden. `initialise()` führt `_SCHEMA` (unverändert) plus `_SCHEMA_V2` aus und
setzt `schema_meta.schema_version` per `INSERT OR REPLACE`. Ein Rückschritt auf Schema 1 ist
nicht vorgesehen und wird nicht gebaut.

```sql
CREATE TABLE IF NOT EXISTS users (
  space               TEXT PRIMARY KEY,
  password_hash       TEXT NOT NULL,
  password_changed_at TEXT,
  totp_secret_enc     BLOB,             -- AES-256-GCM, NULL bis zur Bestätigung
  totp_alg            TEXT NOT NULL DEFAULT 'SHA1',
  totp_confirmed_at   TEXT,
  status              TEXT NOT NULL DEFAULT 'active',   -- active | disabled
  created_at          TEXT NOT NULL);

CREATE TABLE IF NOT EXISTS invites (
  token_hash  TEXT PRIMARY KEY,
  space       TEXT NOT NULL,
  purpose     TEXT NOT NULL,            -- 'initial' | 'reset'
  created_at  TEXT NOT NULL,
  expires_at  TEXT NOT NULL,
  consumed_at TEXT);

CREATE TABLE IF NOT EXISTS recovery_codes (
  code_hash  TEXT PRIMARY KEY,
  space      TEXT NOT NULL,
  created_at TEXT NOT NULL,
  used_at    TEXT);

CREATE TABLE IF NOT EXISTS ui_sessions (
  session_hash        TEXT PRIMARY KEY,
  space               TEXT NOT NULL,
  csrf_hash           TEXT NOT NULL,
  created_at          TEXT NOT NULL,
  last_seen_at        TEXT NOT NULL,
  absolute_expires_at TEXT NOT NULL,
  revoked_at          TEXT,
  revoked_reason      TEXT);

CREATE INDEX IF NOT EXISTS ix_sessions_space  ON ui_sessions(space);
CREATE INDEX IF NOT EXISTS ix_recovery_space  ON recovery_codes(space);
CREATE INDEX IF NOT EXISTS ix_invites_space   ON invites(space);
```

**Warum kein `email`, kein `display_name`:** es gibt zwei Nutzer, der Space-Name ist die
Identität. Ein Feld, das nichts entscheidet, ist Ballast.

### 2.3 Neue `AuthStore`-Methoden

Alle in `authserver/store.py`, alle mit `now_fn`, mehrschrittige Änderungen in
`_transaction()`. Signaturen (verbindlich):

```python
# -- Nutzerakten ---------------------------------------------------------------
def get_user(self, space: str) -> UserRow | None
def list_users(self) -> list[UserRow]
def upsert_user(self, space: str, *, password_hash: str, totp_secret_enc: bytes | None,
                totp_alg: str, totp_confirmed_at: datetime | None, status: str) -> None
def set_password_hash(self, space: str, password_hash: str) -> None      # setzt password_changed_at
def set_totp(self, space: str, *, secret_enc: bytes, alg: str) -> None   # confirmed_at = NULL
def confirm_totp(self, space: str) -> None
def set_user_status(self, space: str, status: str) -> None

# -- Einladungen ---------------------------------------------------------------
def create_invite(self, *, space: str, purpose: str, ttl_s: int) -> str  # gibt Klartext-Token zurück
def peek_invite(self, token: str) -> InviteRow | None                    # rein lesend, für GET
def consume_invite(self, token: str) -> InviteRow | None                 # einmalig, für POST

# -- Recovery-Codes ------------------------------------------------------------
def replace_recovery_codes(self, space: str, codes: Iterable[str]) -> None  # löscht alte, legt neue
def consume_recovery_code(self, space: str, code: str) -> bool
def count_unused_recovery_codes(self, space: str) -> int

# -- UI-Sessions ---------------------------------------------------------------
def create_session(self, *, space: str, idle_ttl_s: int,
                   absolute_ttl_s: int) -> tuple[str, str]   # (session_id, csrf_token)
def touch_session(self, session_id: str, *, idle_ttl_s: int) -> SessionRow | None
def revoke_session(self, session_id: str, reason: str) -> None
def revoke_sessions_for_space(self, space: str, *, except_session_id: str | None,
                              reason: str) -> int
def list_sessions(self, space: str) -> list[SessionRow]
```

**`touch_session` ist der einzige Lesepfad der Session** und macht drei Dinge in einer
Transaktion: prüfen (nicht widerrufen, nicht absolut abgelaufen, `last_seen_at` nicht älter als
`idle_ttl_s`), `last_seen_at` aktualisieren, Zeile zurückgeben. Damit gibt es keinen Zustand,
in dem eine Route „gültig" liest und eine andere „abgelaufen".

Neue Dataclasses in `authserver/models.py`: `UserRow`, `InviteRow`, `SessionRow`.
`UserRow.totp_secret_enc` ist `bytes | None` — **verschlüsselt**; entschlüsselt wird
ausschließlich in `userdir.py`.

### 2.4 `secretbox.py`

```python
NONCE_LEN = 12

def seal(plaintext: bytes, *, key: bytes, aad: bytes) -> bytes:
    """nonce || ciphertext_mit_tag. AES-256-GCM (BSI TR-02102-1)."""

def open_(blob: bytes, *, key: bytes, aad: bytes) -> bytes:
    """Wirft SecretBoxError bei falschem Schlüssel, falscher AAD oder Manipulation."""
```

- Schlüssel: 32 Byte. Quelle in dieser Reihenfolge: `CREDENTIALS_DIRECTORY/auth-dek` (systemd
  `LoadCredentialEncrypted`), sonst Keyring `nikinger-space` / `auth-dek` (nur Entwicklung).
  Fehlt beides **und** ist die `users`-Tabelle nicht leer → Start scheitert laut. Kein stiller
  Klartextbetrieb.
- AAD = `space.encode("utf-8")`. Ein aus einer anderen Zeile kopierter Seed entschlüsselt nicht.
- Funktion in `authserver/config.py :: load_data_encryption_key(source: Mapping[str, str]) -> bytes | None`,
  gleiche Verzweigungslogik wie `users.load_users()`.

`[VERIFY]` **V28:** exakte `cryptography`-Version, die auf der VM installierbar ist (Wheel für
Ubuntu 22.04 und die dort laufende Python-Version). Exakt pinnen wie `argon2-cffi==25.1.0`.
Rohmessung: `python -c "from cryptography.hazmat.primitives.ciphers.aead import AESGCM"`.

### 2.5 `userdir.py`

```python
@dataclass(frozen=True, kw_only=True)
class UserRecord:
    space: str
    password_hash: str
    totp_secret: str | None      # Klartext-Base32, NUR im Speicher
    totp_alg: str
    totp_confirmed: bool
    status: str

class UserDirectory:
    def __init__(self, store: AuthStore, *, dek: bytes | None) -> None
    def get(self, space: str) -> UserRecord | None
    def spaces(self) -> list[str]
    def set_password(self, space: str, password: str) -> None
    def begin_totp_enrollment(self, space: str) -> str        # neuer Seed, unbestätigt
    def confirm_totp_enrollment(self, space: str, code: str, *, now: float) -> bool
    def issue_recovery_codes(self, space: str) -> list[str]   # Klartext genau einmal
    def consume_recovery_code(self, space: str, code: str) -> bool
```

**`get()` cacht nicht.** Das ist der ganze Punkt (P5-L, O1). Zwei Nutzer und ein SQLite-Lesevorgang
pro Login sind kein Performanceproblem; ein Cache wäre genau der Zustand, der O1 erzeugt hat.

**Anpassung im Bestand:** `flows.submit_consent(..., users=...)` nimmt statt
`Mapping[str, Mapping[str, str]]` ein `UserDirectory` entgegen und liest `record.password_hash` /
`record.totp_secret` / `record.totp_alg` statt `users[space]["pwd"]` usw. `app.py ::
OAuthConfig.users` ändert seinen Typ entsprechend. Das ist der S6-Fix (§2.1).

**Ein Recovery-Code funktioniert auch im OAuth-Consent-Formular** — sonst wäre ein Nutzer ohne
Authenticator zwar in der UI, aber nicht am Connector handlungsfähig. Das Feld heißt weiterhin
`totp`; ein Wert mit Bindestrich und Länge 11 wird als Recovery-Code geprüft. Ein Test hält das
fest.

### 2.6 Migration der Nutzerakten

`phase4_auth/scripts/import_users_to_db.py`:

1. `users.load_users_from_keyring()` lesen (**Keyring**, nicht Credential — die Quelle der
   Wahrheit für die Provisionierung, wie `export_auth_users.py`).
2. Für jeden Eintrag: `pwd` → `users.password_hash`, `totp` → `secretbox.seal(...)` →
   `totp_secret_enc`, `totp_alg` übernehmen, `totp_confirmed_at` = `created_at` (die bestehenden
   Seeds sind live bewiesen), `status = 'active'`.
3. Vorhandene Zeilen werden **nicht** überschrieben, außer mit `--force`.
4. Ausgabe: eine Zeile je Space mit `angelegt` / `übersprungen`, plus Gesamtzahl. Kein Seed, kein
   Hash auf stdout.
5. `--dry-run` ist Standard; Schreiben nur mit `--apply`.

**Reihenfolge im Betrieb (Nikinger-Aktion, Runbook im Phase-Head):**
Backup → `--dry-run` → `--apply` → `systemctl restart sharefyx-mcp` → beide Nutzer melden sich
am Connector **und** an der UI an → erst danach `LoadCredentialEncrypted=auth-users` aus der
Unit entfernen und den Keyring-Eintrag löschen. **Nicht vorher.** `spaces.cred` hat gezeigt, was
passiert, wenn eine Credential-Zeile und die Realität auseinanderlaufen.

### 2.7 Sessions, CSRF, Re-Auth

**`webui/sessions.py :: SessionManager`** — Cookie-Logik, kein SQL:

```python
COOKIE_NAME = "__Host-sfx_session"

class SessionManager:
    def __init__(self, store: AuthStore, *, settings: UiSettings) -> None
    def issue(self, response: Response, *, space: str) -> str    # gibt CSRF-Token zurück
    def load(self, request: Request) -> SessionRow | None        # ruft touch_session
    def rotate(self, request: Request, response: Response, *, space: str) -> str
    def clear(self, response: Response, session_id: str | None, reason: str) -> None
```

Cookie exakt: `__Host-sfx_session=<id>; Path=/; Secure; HttpOnly; SameSite=Strict`.
Kein `Domain`, kein `Max-Age` (Browser-Session-Cookie; die Lebensdauer ist serverseitig).

**CSRF (`webui/security.py`):**

```python
def require_csrf(request: Request, session: SessionRow) -> None:
    """Wirft CsrfError (→403) wenn eine der drei Prüfungen scheitert."""
```

1. Methode ist `GET`/`HEAD` → nichts zu tun.
2. **Herkunft:** `Origin` muss exakt `settings.base_url` sein. Fehlt `Origin`, gilt
   `Sec-Fetch-Site: same-origin` als Ersatz. Fehlt beides → `403`.
3. **Double-Submit:** `X-CSRF-Token` (JSON-Aufrufe) oder Formularfeld `csrf` (HTML-Formulare),
   verglichen mit `crypto.secrets_equal(hash_secret(wert), session.csrf_hash)`.

**Re-Auth (`webui/reauth.py`):**

```python
def verify_reauth(userdir: UserDirectory, throttle: LoginThrottle, store: AuthStore,
                  *, space: str, password: str, second_factor: str, now: float) -> bool
```

Benutzt dieselbe Fehlversuchsbremse wie der OAuth-Login (`ratelimit.LoginThrottle`, dieselbe
`login_attempts`-Tabelle, derselbe Space-Schlüssel). Eine Sperre gilt damit für **alle**
Anmeldewege gleichzeitig — genau richtig, sonst wäre die UI das Schlupfloch um die Bremse herum.

### 2.8 Einladungs- und Enrollment-Fluss

```
authctl.py invite niklas
  └─► https://<host>/ui/invite/<token>          (genau einmal auf stdout, TTL 60 min)

GET  /ui/invite/<token>   → peek_invite  → Formular „Passwort setzen"
POST /ui/invite/<token>   → consume_invite (einmalig!)
     ├─ Passwortpolitik prüfen (P5-O)
     ├─ set_password
     ├─ begin_totp_enrollment  → Seed + otpauth-URI + QR
     └─ Session ausstellen, Status „TOTP unbestätigt"
POST /api/v1/account/totp/confirm  → confirm_totp_enrollment
     └─ issue_recovery_codes → genau einmal angezeigt
```

**Solange TOTP unbestätigt ist**, ist der Account nur für die drei Enrollment-Endpunkte
freigeschaltet; jede andere API-Route antwortet `403 {"error": "totp_required"}`. Die UI zeigt
in diesem Zustand ausschließlich den Einrichtungsbildschirm.

**QR-Code:** `otpauth://`-URI aus `totp.provisioning_uri()`, gerendert als **inline-SVG**.
`[VERIFY]` **V29:** Bibliothek. Vorschlag `segno` (reines Python, keine Transitivabhängigkeiten,
MIT), exakt gepinnt. **Fallback ohne neue Abhängigkeit:** nur den Base32-Seed in Blöcken zu vier
Zeichen anzeigen — jede Authenticator-App kann ihn manuell aufnehmen. Der Seed wird **immer**
zusätzlich als Text angezeigt, auch wenn der QR-Code steht; ein QR-Code, den man nicht abtippen
kann, ist bei Kamerafehler eine Sackgasse.

### 2.9 Passwortpolitik

`webui/passwords_policy.py`:

```python
MIN_LEN = 12
MAX_LEN = 128

def check(password: str) -> list[str]:
    """Leere Liste = in Ordnung. Sonst Klartext-Gründe für die UI."""
```

- Länge, kein Zeichenklassenzwang.
- Abgleich gegen `blocklist.txt` (kleingeschrieben, `strip()`), plus die triviale Ableitung
  „Passwort enthält den Space-Namen".
- **Kein Netzaufruf.** Kein HIBP-Range-Query. Der Server telefoniert nicht nach Hause — das ist
  keine Bequemlichkeitsentscheidung, sondern dieselbe Regel, die LLM-Aufrufe verbietet.
- `[VERIFY]` **V30:** Herkunft und Größe der Blocklist. Vorschlag: die 10.000 häufigsten
  Passwörter aus einer öffentlich zugänglichen Liste, im Repo eingecheckt (~80 KB). Ein Kommentar
  am Dateikopf nennt Quelle und Stand.

---

## §3 Block B — REST-API und Oberfläche

### 3.1 API-Konventionen

- **Content-Type** `application/json; charset=utf-8`, immer. Kein Formular-Encoding auf `/api`.
- **Datumsformat** ISO-8601 UTC mit `Z` (`storage.store :: _format_dt`-Format für Zeitstempel,
  reines `YYYY-MM-DD` für `due`).
- **Fehlerkörper** einheitlich:
  ```json
  {"error": "<stabiler_code>", "message": "<für Menschen>", "detail": {}}
  ```
  Stabile Codes: `unauthenticated`, `csrf_failed`, `totp_required`, `forbidden`, `not_found`,
  `conflict`, `validation_failed`, `rate_limited`, `payload_too_large`, `internal`.
- **`409 conflict`** trägt zusätzlich das aktuelle Item:
  ```json
  {"error":"conflict","message":"...","detail":{"current": { ...Item... }}}
  ```
  Genau die Information, die `ConflictError.current` schon hat — kein zweiter Roundtrip nötig.
- **Kein HTML in Antworten.** Nirgends. Auch nicht in `message`.
- **Größenbegrenzung:** Request-Body maximal 1 MiB (`payload_too_large`), `limit` maximal 200.
- **Kein `Set-Cookie` auf `/api`** außer bei Session-Rotation nach Re-Auth.

### 3.2 Serialisierung

`webui/serializers.py`:

```python
def item_to_json(item: Item, *, readonly: bool) -> dict
def summary_to_json(s: ItemSummary) -> dict
def search_to_json(r: SearchResult, *, own_space: str) -> dict
def space_to_json(s: SpaceInfo, *, own_space: str) -> dict
```

- `item_to_json` gibt `body` als **reinen Text** aus, nie gerendert (P5-Y).
- `readonly` ist `True`, sobald `item.space != own_space`. Die UI benutzt genau dieses Feld, um
  Bedienelemente **nicht zu rendern**.
- `format` wird aus `item.extra.get("format", "markdown")` gelesen und als eigenes Feld
  ausgegeben. Beim Schreiben wandert es unverändert nach `extra` zurück. **Das ist der ganze
  Seam** (P5-Z) — keine Zeile in `storage/`.
- `extra` wird **vollständig** mitgeliefert (Schlüssel `extra`), damit ein Round-Trip durch die
  UI keine fremden Frontmatter-Felder verliert. Ein Test beweist das an einem Item mit einem
  unbekannten Feld.

### 3.3 Endpunkt-Semantik im Detail

**`GET /api/v1/items`** — Parameter identisch zu `Store.search()`:
`query`, `space`, `type`, `status`, `tag`, `due_before`, `limit` (Default 50, max 200), `offset`.
Ohne `space` wird über alle sichtbaren Spaces gesucht (`Permissions.can_read`).

**`POST /api/v1/items`** — Body: `type`, `title`, `body`, optional `status`, `due`, `tags`,
`links`, `format`. **Kein `space`.** Der Space kommt aus der Session.
→ `Store.create(session.space, type=..., title=..., body=..., **rest)`.

**`PATCH /api/v1/items/{id}`** — Body: `version` (Pflicht) plus die zu ändernden Felder.
Ablauf: `Store.space_of(id)` → `can_write` prüfen → `Store.update(id, version=..., **changes)`.
`ConflictError` → `409` mit `current`. `ValidationError` → `422 validation_failed`.
`ItemNotFound` → `404`.

**Reihenfolge ist nicht verhandelbar:** erst `space_of()`, dann Rechteprüfung, dann Store-Aufruf.
`space_of()` schreibt nichts und liest keine Datei — genau dafür wurde es in P2 gebaut. Ein
Rechtefehler darf den Store nicht erreichen.

**`POST /api/v1/items/{id}/append`** — `version`, `text`. → `Store.append(...)`.
**`POST /api/v1/items/{id}/archive`** — `version`. → `Store.archive(...)`.

**`GET /api/v1/account/connectors`** → `store.list_families(space=session.space)`, gefiltert auf
nicht widerrufene, mit `client_id`, `client_name` (aus `get_client`), `created_at`.
`DELETE .../{family_id}` → `revoke_family(family_id, "user_revoked")`, aber **nur** wenn die
Familie zum eigenen Space gehört; sonst `404` (nicht `403` — ein `403` wäre ein Orakel darüber,
dass die ID existiert).

### 3.4 Sicherheits-Header der UI

`webui/security.py :: ui_security_headers()` — **getrennt** von
`authserver/routes.py :: _security_headers()`. Die OAuth-Seiten brauchen `claude.ai` in
`form-action`, die UI nicht; eine gemeinsame Funktion würde eine der beiden Seiten schwächen.

```
Content-Security-Policy: default-src 'none'; script-src 'self'; style-src 'self';
    img-src 'self' data:; font-src 'self'; connect-src 'self'; form-action 'self';
    frame-ancestors 'none'; base-uri 'none'
Referrer-Policy: no-referrer
X-Content-Type-Options: nosniff
X-Frame-Options: DENY
Cross-Origin-Opener-Policy: same-origin
Cross-Origin-Resource-Policy: same-origin
Permissions-Policy: camera=(), microphone=(), geolocation=(), interest-cohort=()
Cache-Control: no-store          # außer für /ui/static mit gehashtem Namen
Strict-Transport-Security: max-age=63072000; includeSubDomains   # wenn settings.hsts
```

**`img-src 'self' data:`** ist die einzige Lockerung — der QR-Code wird als Inline-SVG
ausgegeben, und `data:` erlaubt das Icon-Set ohne zusätzliche Requests. `script-src 'self'` ohne
`unsafe-inline` heißt: **jedes** Stück JavaScript liegt in `app.js`. Kein `onclick`-Attribut,
kein `<script>`-Block. Das ist keine Stilfrage, das ist die Bedingung dafür, dass die CSP
überhaupt etwas wert ist.

### 3.5 Markdown im Browser

`app.js` enthält zwei aus dem `Notizheft_example.html` geerntete und erweiterte Funktionen
(P5-V):

- **`markdownToHtml(src)`** — Teilmenge, bewusst klein: ATX-Überschriften `#`–`####`, ungeordnete
  und geordnete Listen (eine Verschachtelungsebene), GFM-Tabellen (Pipe-Syntax, Ausrichtungszeile),
  Fett/Kursiv/Code-Spans, eingezäunte Codeblöcke, Zitate, horizontale Linien, Links.
  **Kein** rohes HTML aus der Quelle: `<` wird immer escaped, bevor irgendetwas anderes passiert.
- **`sanitizeHtml(html)`** — Allowlist über Tags und Attribute, danach ein zweiter Durchlauf über
  `href`: nur `http:`, `https:`, `mailto:` und interne `#item/<id>`-Anker. Alles andere wird
  entfernt, nicht neutralisiert.

**Reihenfolge:** `sanitizeHtml(markdownToHtml(escapeHtml(src)))`. Drei Schritte, und der
Sanitizer läuft zuletzt, nicht zuerst.

Für Bodies aus fremden Spaces gilt zusätzlich: die Vorschau bekommt eine sichtbare Umrandung mit
Herkunftsangabe. Das ist das menschliche Gegenstück zu `<untrusted_content>` — ein Mensch, der
eine fremde Notiz liest, soll sehen, dass es eine fremde ist.

---

## §4 Designsystem

Erarbeitet nach `frontend-design`, mit der Vorgabe aus D5: Apples Formensprache **vor** „Liquid
Glass" (Klarheit, Zurücknahme, Tiefe durch Hierarchie statt durch Material) über dem Aufbau und
der Farbwelt der My-BMW-App.

> **Zur Ehrlichkeit:** einen `apple-design`-Skill gibt es in dieser Umgebung nicht — verfügbar
> ist `frontend-design`. Was hier steht, ist daraus abgeleitet und an der Vorgabe kalibriert,
> nicht aus einem Apple-Regelwerk kopiert.

### 4.1 Farbtoken (dunkel, v1 einziges Thema)

```css
:root {
  --bg:            #0B0D10;   /* nahezu schwarz, leicht kühl — BMW-App-Grund */
  --surface:       #14181D;   /* Karten, Listenflächen */
  --surface-raised:#1B2027;   /* aktive Zeile, Eingabefelder */
  --line:          rgba(255,255,255,.08);   /* Haarlinie, KEIN Schatten */
  --line-strong:   rgba(255,255,255,.16);

  --text:          #E9EDF2;
  --text-muted:    #9AA6B4;
  --text-faint:    #64707E;

  --accent:        #3E8DF3;   /* das einzige Blau */
  --accent-quiet:  rgba(62,141,243,.14);
  --accent-line:   rgba(62,141,243,.40);

  --warn:          #E5A93C;   /* Konflikt, fremder Space */
  --danger:        #E5484D;   /* Widerruf, Archivieren */
  --ok:            #47B881;

  --radius:        10px;
  --radius-sm:     6px;
  --space:         8px;       /* alles ist ein Vielfaches davon */
}
```

**Genau ein Akzentblau.** Keine Verläufe, keine zweite Akzentfarbe, keine Schlagschatten außer
einem einzigen für Modale (`0 24px 64px rgba(0,0,0,.55)`). Tiefe entsteht durch Flächenhelligkeit
und Haarlinien — das ist die „Zurücknahme", die die Vorgabe meint.

### 4.2 Typografie

| Rolle | Schrift | Einsatz |
|---|---|---|
| UI + Fließtext | **Inter Variable**, selbst gehostet, latin-subgesetzt | alles außer Code |
| Zahlen/Metadaten | Inter mit `font-variant-numeric: tabular-nums` | Versionen, Daten, Zähler |
| Code + Editor | Systemstack `ui-monospace, SFMono-Regular, Menlo, Consolas, monospace` | 0 Byte Transfer |

**Genau eine Webfont-Datei.** `[VERIFY]` **V31:** Lizenz (SIL OFL), Dateigröße nach Subsetting
(Ziel < 120 KB), `font-display: swap`, Cache-Header. Falls das Subsetting nicht sauber
reproduzierbar ist: Systemstack, und die Entscheidung datiert im Phase-Head vermerken — eine
Schrift, deren Herkunft niemand mehr nachvollziehen kann, ist schlimmer als keine.

Skala (1.200er Verhältnis, auf 8-px-Raster gerundet):
`12 / 13 / 15 / 18 / 22 / 28`. Gewichte: 400 Fließtext, 500 UI-Labels, 600 Überschriften.
Zeilenhöhe 1.5 im Fließtext, 1.25 in Überschriften und Listenzeilen.

### 4.3 Layout (16:9, ≥ 1280 px)

```
┌───────────┬──────────────────┬──────────────────────────────────────────┐
│  RAIL     │  LISTE           │  ANSICHT / EDITOR                        │
│  240 px   │  380 px          │  Rest                                    │
│           │                  │                                          │
│ Spaces    │ ┌ Suchfeld ────┐ │ ┃ Titel                                  │
│  ▸ niklas │ │              │ │ ┃ ─────────────────────────────────────  │
│  ▸ fabian │ └──────────────┘ │ ┃ Status · Fällig · Tags · Links         │
│           │  Filterchips     │ ┃                                        │
│ Filter    │ ─────────────────│ ┃ [Bearbeiten | Vorschau]                │
│  Offen    │  Zeile           │ ┃                                        │
│  Notizen  │  Zeile ← aktiv   │ ┃ ....Text....                           │
│  Archiv   │  Zeile           │ ┃                                        │
│           │  ...             │ ┃                                        │
│ ────────  │                  │ ┗ Versionsband (siehe 4.4)               │
│ Konto     │                  │                                          │
└───────────┴──────────────────┴──────────────────────────────────────────┘
```

- Trennung durch Haarlinien (`--line`), keine Kästen um die Spalten.
- Listenzeile: zwei Zeilen hoch — Titel (15 px/500) über Metadaten (12 px/`--text-muted`,
  tabellarische Ziffern). Aktive Zeile bekommt `--surface-raised` plus eine 2-px-Akzentkante
  links.
- Zwischen 1024 und 1280 px klappt die Rail auf 64 px (nur Symbole) ein. Unter 1024 px verschwindet
  die Liste hinter einer Zurück-Navigation. **Mehr Mobilarbeit ist nicht Teil der Phase (P5-W).**

### 4.4 Signature-Element: das Versionsband

Ein 3 px breiter, vertikaler Streifen an der linken Kante der Editor-Spalte, unten mit der
Versionsnummer beschriftet (tabellarische Ziffern, 12 px, `--text-faint`).

- **Ruhezustand:** `--line`, Zahl gedämpft.
- **Ungespeicherte Änderungen:** Streifen wird `--accent`, Zahl bekommt ein `+`.
- **Der Server meldet eine neuere Version (409):** Streifen wird `--warn`, die Zahl zeigt
  `deine → aktuelle`, und der Konfliktdialog erscheint.

Warum genau das die Signatur ist: die These dieses Projekts ist Hard Rule 3 — kein
Last-Write-Wins, nirgends. Ein Versionszähler, den man permanent sieht, macht die
Kernentscheidung des Systems zum sichtbaren Bedienelement, statt sie in einer Fehlermeldung zu
verstecken. Das ist der einzige Ort, an dem die Oberfläche laut sein darf.

### 4.5 Zustände, die entworfen werden müssen (nicht improvisiert)

| Zustand | Gestaltung |
|---|---|
| Leerer Space | Ganzflächig, eine Zeile Text, ein Primärknopf „Erste Notiz anlegen". Keine Illustration. |
| Suche ohne Treffer | Trefferliste zeigt eine Zeile: die aktiven Filter als entfernbare Chips. |
| Fremder Space | Kopfzeile mit `--warn`-Haarlinie und Chip „Nur lesen". Schreib-Bedienelemente werden **nicht gerendert** (P5-Y). |
| Konflikt | Modal, zwei Optionen: „Aktuelle Fassung laden (deine Änderungen verwerfen)" und „Meine Fassung als neues Item anlegen". **Kein Auto-Merge, kein Überschreiben.** |
| Sitzung abgelaufen | Ganzflächige Karte statt Umleitung — ein Redirect mitten im Tippen wirft den Text weg. Wiederanmeldung im Dialog, danach wird der Entwurf wieder eingesetzt. |
| Dienst nicht erreichbar | Statuszeile am Fuß, kein Modal. Der Uplink wackelt gelegentlich, das ist bekannt (P3-Risiko). |
| TOTP unbestätigt | Ausschließlich der Einrichtungsbildschirm, keine Navigation daneben. |

**Entwurfsschutz:** der aktuelle Editorinhalt liegt in `sessionStorage` unter
`sfx:draft:<itemId>` und wird nach erfolgreichem Speichern gelöscht. Kein `localStorage`, keine
Persistenz über den Tab hinaus, keine Entwürfe fremder Items. Ein Kommentar im Code nennt die
Begründung.

### 4.6 Barrierefreiheit und Bewegung

- Sichtbarer Fokusring auf allem Bedienbaren: `outline: 2px solid var(--accent); outline-offset: 2px`.
- Kontrast: Fließtext ≥ 7:1, gedämpfter Text ≥ 4.5:1 gegen `--bg`.
- Tastatur: `/` fokussiert die Suche, `Ctrl/Cmd+S` speichert, `Esc` schließt Dialoge,
  `↑`/`↓` bewegen sich durch die Trefferliste. Alles ohne Maus erreichbar.
- Bewegung: ausschließlich 120-ms-Überblendungen bei Zustandswechseln, und die respektieren
  `prefers-reduced-motion: reduce`. Keine Ein-/Ausflug-Animationen. Sparsamkeit ist hier
  Designentscheidung, nicht Faulheit — und sie hilft V12.

---

## §5 Steps

Jeder Step endet mit grünem `pytest` (gemockt, **kein Netz, kein echter `DATA_ROOT`, kein echter
Tunnel**), aktualisierter Modultabelle im Phase-Head **und** aktualisiertem
`## Session stopped`-Block — im **selben** Commit (Hard Rule 8). Ab dem zweiten Block läuft
`scripts/rotate_session_block.sh phase5_ui`, nie von Hand.

**Gate zwischen Block A und B:** nach Step 4 wird nicht weitergebaut, bevor die Abnahmezeilen
1–9 (§6) live bestanden sind.

---

### Step 0 — Haushalt, Verifikationsdurchlauf, Rückbau, Inventar

Kein Feature-Code. Bei **B** ist „nichts zu tun" ein zulässiges und zu meldendes Ergebnis; bei
**A**, **C** und **D** nicht.

**A · Rückbau `spaces.cred` und der P2-Token-Reste** (P4-Handover §4.5). Zusammen, nicht einzeln:

1. `phase4_auth/systemd/sharefyx-mcp.service`: Zeile
   `LoadCredentialEncrypted=spaces:/etc/sharefyx/spaces.cred` entfernen.
2. `phase2_mcp/scripts/export_space_map.py` löschen.
3. `phase2_mcp/scripts/issue_token.py` löschen.
4. `phase2_mcp/mcpserver/credentials.py :: load_space_map()` und alles, was nur davon lebt,
   entfernen. **`hash_token` bleibt** — `asgi.py` verweist im Docstring darauf, dass es
   byte-identisch mit `authserver.crypto.hash_secret` ist.
5. `mcpserver/auth.py :: KeyringTokenResolver` prüfen: wenn nach 2–4 kein Aufrufer übrig ist,
   ebenfalls entfernen; `SpaceResolver` als Protokoll bleibt.
6. Tests, die nur die gelöschten Pfade abdecken, entfallen — die Testzahl **sinkt** in diesem
   Step. Das ist erwartet und wird im Session-Block mit Aufschlüsselung je Datei belegt, nicht
   nur als Zahl.
7. **Nikinger-Aktion:** `install_units.sh` + `systemctl restart sharefyx-mcp` + `/health` prüfen
   + einen Tool-Aufruf über den echten Connector. Erst danach `/etc/sharefyx/spaces.cred`
   löschen.

**B · Verifikationsdurchlauf** (Ergebnis melden, auch wenn es „nichts zu tun" lautet):

```bash
pytest -q                                              # Ausgangszahl notieren (V32)
grep -rEho '(^|\s)(up|down):\s*\S+|\]\(([^)]+)\)' --include='*.md' . | ...   # up:/down:/Links auflösen
find . -name "*.md" -size +40k                         # jeder Treffer muss 📕/📦 sein
grep -c '^## Session stopped' phase4_auth/CLAUDE.md    # muss 1 sein
comm -13 <(git ls-files '*.md' | sort) <(grep -o '](\./[^)]*\.md)' docs/INDEX.md | ... | sort)
```

Jede `.md` im Repo hat eine Zeile in `docs/INDEX.md`; jede `up:`/`down:`/Markdown-Linkangabe
löst auf eine existierende Datei auf.

**C · Doku-Drift schließen:**

1. `ROADMAP.md`, P5-Zeile: Status ⬜ → 🔄.
2. `ROADMAP.md`, P3-Zeile: falls der Restore-Nachweis (Zeile 13) inzwischen erbracht ist —
   der Nikinger hat ihn für **vor** Planbeginn zugesagt (Antwort F4) — Status 🟡 → ✅ mit
   datiertem Beleg. Falls nicht erbracht: **unverändert lassen und melden**, nicht wohlwollend
   hochstufen.
3. Root-`CLAUDE.md`, „Current state": aktive Phase auf **P5**, `down:` auf `phase5_ui/CLAUDE.md`
   umhängen, `updated:` setzen.
4. Root-`CLAUDE.md`, „Noch nicht entschieden": der Punkt „Web-UI: Neubau gegen die REST-API vs.
   Adaption des `Notizheft_example.html`" ist mit P5-V entschieden → durch eine datierte
   Korrekturnotiz ersetzen, nicht ersatzlos streichen.
5. `README.md`: das Architekturdiagramm nennt „Tunnel (Cloudflare, ausgehend)" und „REST-API +
   Web-UI für Menschen [Phase 4]" — beides falsch. → Tailscale Funnel, Phase 5. Ebenso die Zeile
   „Menschen bearbeiten sie im Editor oder (ab Phase 4) in einer Web-UI". `[VERIFY]` **V34**: der
   Snapshot vom 2026-08-01 zeigt eine `README.md` von 10.484 B gegenüber 6.445 B im
   Juli-Snapshot — sie wurde also bereits überarbeitet; erst lesen, dann korrigieren.
6. `docs/INDEX.md`: P4 wandert von „Active phase" nach „Completed phases" (🔄 → 📗), neuer
   Abschnitt „Active phase (5 — Web-UI)", und die Zeilen für dieses Plandokument sowie für
   `PHASE4_CLOSEOUT_HANDOVER.md` kommen dazu (§7).

**D · Umgebungsinventar** (in den Session-Block, roh, nicht paraphrasiert):

```bash
python3 -V; python3 -c "import sqlite3; print(sqlite3.sqlite_version)"
systemctl --version | head -1
tailscale version; tailscale serve status; tailscale funnel status
ss -ltnp | grep -E ':(8080|8081|9090)'      # freie Ports für Staging
df -h /var/lib /home/savefyx
python3 -c "from cryptography.hazmat.primitives.ciphers.aead import AESGCM; print('ok')"  # V28
vnstat -m 2>/dev/null || echo "kein vnstat"  # V12: Uplink-Verbrauch, falls messbar
```

**Done when:** `pytest -q` grün mit dokumentierter neuer Ausgangszahl; A live gegenverifiziert
(`/health` 200, ein echter Tool-Aufruf erfolgreich); B mit Ergebnis gemeldet; C committet; D im
Session-Block.

---

### Step 1 — Sicherheitsbefunde S2–S8

**Dateien:** `authserver/{resolver,flows,store,routes}.py`, `mcpserver/app.py` (nur die
`OAuthTokenResolver`-Konstruktion), `phase5_ui/systemd/sharefyx-purge.{service,timer}`,
`phase4_auth/scripts/authctl.py`, `phase3_edge/scripts/install_units.sh`.

Inhalte wie §2.1. **Vor dem ersten Fix:** `P4_SECURITY_REVIEW_2026-07-29.md` lesen — dieser Plan
ist die Umsetzung, das Review ist die Quelle.

**Tests:**
- `test_refresh_rejects_wrong_client_id` — S2
- `test_refresh_wrong_client_id_does_not_revoke_family` — S2, die wichtigere Hälfte
- `test_resolver_rejects_foreign_audience` — S3
- `test_resolver_accepts_own_audience` — S3
- `test_resolver_rejects_token_without_space_scope` — S4
- `test_resolver_accepts_token_with_space_scope` — S4
- `test_redirect_with_existing_query_keeps_both_params` — S5
- `test_redirect_error_with_existing_query_keeps_both_params` — S5
- `test_broken_user_record_yields_generic_login_failure` — S6, **kein 500**
- `test_unknown_space_and_broken_record_are_indistinguishable` — S6, Enumerationsschutz
- `test_purge_removes_expired_sessions_and_invites` — S7 (nach Step 2 zu ergänzen)
- `test_install_units_refuses_world_writable_env` — S8, Shell-Test über `bash -c`
- `test_security_review_register_is_empty` — ein Meta-Test, der die Liste der offenen Befunde
  im Phase-Head gegen die erwartete leere Menge prüft

**Done when:** `pytest` grün; `docs/concepts/P4_SECURITY_REVIEW_2026-07-29.md` bekommt einen
**datierten Nachtrag** (das Dokument selbst ist ein 📕-Snapshot — der Nachtrag steht im
Phase-Head, nicht im Snapshot), und der Phase-Head trägt die Tabelle S2–S8 mit Status
„geschlossen" plus Commit-Hash je Befund.

---

### Step 2 — Auth-Datenmodell: Schema 2, Verschlüsselung, `UserDirectory`

**Dateien:** `authserver/{store,models,secretbox,config,userdir}.py`, `authserver/flows.py`
(Typ-Anpassung), `mcpserver/app.py` (`OAuthConfig.users`-Typ),
`phase4_auth/scripts/import_users_to_db.py`, `phase4_auth/pyproject.toml` (Abhängigkeit).

Inhalte wie §2.2–§2.6.

**Reihenfolge innerhalb des Steps** (wichtig, sonst hängt der Dienst an einer halben Migration):
1. `secretbox.py` + `config.load_data_encryption_key()` + Tests — isoliert, ohne Store.
2. Schema 2 + neue `AuthStore`-Methoden + Tests.
3. `userdir.py` + Tests.
4. `flows.py`/`app.py` auf `UserDirectory` umstellen; **alle bestehenden 347 Tests müssen weiter
   grün sein** — das ist der Beleg, dass der Umbau verhaltensneutral ist.
5. `import_users_to_db.py` + Test gegen eine temporäre DB.

**Tests:**
- `test_seal_open_roundtrip`
- `test_open_fails_with_wrong_key`
- `test_open_fails_with_wrong_aad` — *der Test, der die Seed-Vertauschung ausschließt*
- `test_open_fails_on_tampered_ciphertext`
- `test_nonce_is_unique_across_seals`
- `test_missing_dek_with_nonempty_users_raises_at_startup`
- `test_schema_migrates_from_v1_to_v2_without_data_loss`
- `test_schema_version_is_two_after_initialise`
- `test_upsert_and_get_user_roundtrip`
- `test_set_password_updates_password_changed_at`
- `test_confirm_totp_sets_timestamp`
- `test_userdirectory_reads_fresh_after_external_update` — **belegt P5-L / schließt O1**
- `test_userdirectory_returns_none_for_broken_record`
- `test_userdirectory_never_returns_encrypted_seed`
- `test_flows_still_authenticate_with_userdirectory`
- `test_import_dry_run_writes_nothing`
- `test_import_skips_existing_rows_without_force`
- `test_import_prints_no_secret_material`

**Done when:** `pytest` grün, Gesamtzahl gestiegen; `import_users_to_db.py --dry-run` gegen eine
Wegwerf-DB gelaufen; **kein** Live-Lauf gegen die echte `auth.sqlite3` in diesem Step (das ist
Step 4, Runbook).

---

### Step 3 — Sessions, CSRF, Login-Seiten

**Dateien:** neues Paket `phase5_ui/` mit `pyproject.toml`, `webui/{__init__,config,security,
sessions,pages,routes_auth,errors}.py`, `phase5_ui/tests/`, `scripts/dev_install.sh` (Aufnahme
des neuen Pakets — `[VERIFY]` **V35**: das Skript nimmt Phasenpakete bisher automatisch auf,
siehe V16).

Inhalte wie §2.7, §3.4. `pages.py` rendert Login, Einladung, Enrollment und Fehler — **ohne
Template-Engine**, gleiche Bauart wie `authserver/templates.py`, aber mit dem Designsystem aus §4
und externem CSS (`/ui/static/app.css`), damit `style-src 'self'` gilt.

Der Modul-Docstring von `pages.py` beginnt mit:

```python
"""Servergerenderte HTML-Seiten für die Wege, auf denen es noch keine Sitzung gibt:
Login, Einladung, Enrollment, Fehler. Bewusst OHNE JavaScript — diese Seiten müssen auch
dann funktionieren, wenn app.js nicht lädt.

NICHT zu verwechseln mit authserver/templates.py: das ist die OAuth-Consent-Oberfläche und
bleibt getrennt (P5-G — eine UI-Sitzung kürzt den Consent nicht ab).
"""
```

**Tests:**
- `test_session_cookie_has_host_prefix_and_all_flags`
- `test_session_cookie_has_no_domain_attribute`
- `test_session_id_is_never_stored_in_plaintext`
- `test_idle_timeout_expires_session`
- `test_absolute_timeout_expires_session_despite_activity`
- `test_login_rotates_session_id`
- `test_logout_revokes_server_side`
- `test_expired_session_cookie_is_cleared_on_response`
- `test_csrf_missing_token_is_403`
- `test_csrf_wrong_token_is_403`
- `test_csrf_foreign_origin_is_403`
- `test_csrf_absent_origin_with_same_site_header_passes`
- `test_csrf_get_needs_no_token`
- `test_ui_pages_carry_security_headers`
- `test_ui_csp_has_no_unsafe_inline`
- `test_ui_csp_form_action_is_self_only` — *belegt, dass die UI-Header **nicht** die
  OAuth-Header sind*
- `test_login_uses_same_throttle_as_oauth_consent`
- `test_login_wrong_password_and_unknown_space_are_indistinguishable`
- `test_mcp_endpoint_ignores_session_cookie` — **P5-F, Richtung 1**
- `test_api_endpoint_ignores_bearer_token` — **P5-F, Richtung 2** (nach Step 5 zu schärfen)
- `test_oauth_authorize_never_reads_cookies` — **P5-G**

**Done when:** `pytest` grün; Login/Logout gegen eine In-Process-App durchgespielt.

---

### Step 4 — Selbstverwaltung: Einladung, Passwort, TOTP, Recovery, Connectoren

**Dateien:** `webui/{account,reauth,passwords_policy}.py`, `webui/blocklist.txt`,
`phase4_auth/scripts/authctl.py` (neue Unterbefehle), `webui/pages.py` (Enrollment-Seiten).

`authctl.py` bekommt:

| Unterbefehl | Wirkung |
|---|---|
| `invite <space> [--purpose initial\|reset] [--ttl 3600]` | erzeugt Einladung, gibt den Link **genau einmal** aus |
| `list-users` | Space, Status, `totp_confirmed`, `password_changed_at`, Anzahl offener Recovery-Codes. **Keine Hashes, keine Seeds.** |
| `disable-user <space>` / `enable-user <space>` | `users.status`; `disable` widerruft zugleich alle Sessions und Token-Familien |
| `list-sessions <space>` / `revoke-sessions <space>` | Betreiber-Notausgang |
| `purge-expired` | erweitert um `ui_sessions` und `invites` (S7) |

**Tests:**
- `test_invite_is_single_use`
- `test_invite_expires`
- `test_invite_link_is_printed_once_and_not_stored_plaintext`
- `test_invite_flow_sets_password_and_starts_totp`
- `test_account_is_locked_to_enrollment_until_totp_confirmed`
- `test_totp_confirm_requires_valid_code`
- `test_totp_secret_is_shown_exactly_once`
- `test_recovery_codes_are_shown_exactly_once`
- `test_recovery_code_replaces_totp_not_password`
- `test_used_recovery_code_cannot_be_reused`
- `test_recovery_code_works_in_oauth_consent_form`
- `test_password_change_requires_password_and_totp`
- `test_password_change_revokes_all_token_families` — **P5-Q**
- `test_password_change_revokes_other_sessions_but_not_current` — **P5-Q**
- `test_password_policy_rejects_short_and_blocklisted`
- `test_password_policy_rejects_space_name_substring`
- `test_password_policy_accepts_long_passphrase_without_symbols`
- `test_connector_list_shows_only_own_families`
- `test_connector_revoke_of_foreign_family_is_404_not_403`
- `test_reauth_failures_count_against_the_same_throttle`

**Done when:** `pytest` grün.
**Danach GATE:** Abnahmezeilen 1–9 live (§6). Block B beginnt erst danach.

---

### Step 5 — REST-API v1

**Dateien:** `webui/{api,serializers,errors}.py`, Verdrahtung in `mcpserver/app.py`
(`webui_routes(...)` in die Routenliste, vor `Mount("/mcp")`).

Inhalte wie §3.1–§3.3.

**Tests:**
- `test_items_search_maps_all_store_parameters`
- `test_items_search_limit_is_capped_at_200`
- `test_get_item_from_own_space_is_writable`
- `test_get_item_from_foreign_space_is_readonly_true`
- `test_create_item_has_no_space_parameter` — *Signaturtest, Rule 4 architektonisch*
- `test_create_item_uses_session_space`
- `test_patch_foreign_item_is_403_and_never_reaches_store` — Store gemockt, Aufrufzähler 0
- `test_space_of_is_called_before_permission_check`
- `test_version_mismatch_returns_409_with_current_item`
- `test_validation_error_returns_422`
- `test_unknown_item_returns_404`
- `test_archived_item_update_returns_422`
- `test_extra_frontmatter_fields_survive_roundtrip` — **belegt P5-Z**
- `test_format_field_defaults_to_markdown_and_roundtrips` — **belegt P5-Z**
- `test_no_html_appears_in_any_api_response`
- `test_oversized_body_returns_413`
- `test_api_requires_session_not_bearer` — P5-F
- `test_api_write_requires_csrf`
- `test_webui_imports_exactly_one_mcpserver_symbol` — §1.2

**Done when:** `pytest` grün; `scripts/ui_smoke.py` läuft In-Process durch alle Endpunkte
(Gegenstück zu `mcp_smoke.py`/`oauth_smoke.py`).

---

### Step 6 — UI-Gerüst: Shell, Tokens, Navigation, Liste und Suche

**Dateien:** `webui/static/{app.html,app.css,app.js}`, `webui/static/fonts/`,
Ausliefer-Route in `webui/routes_auth.py` bzw. eigenem `webui/static_routes.py`.

Inhalte wie §4.1–§4.3, §4.6.

**Reihenfolge:** erst `app.css` mit dem vollständigen Tokenblock und den drei Spalten, dann
`app.html` als Skelett, dann `app.js` mit Datenanbindung. Nicht andersherum — ein Layout, das
erst nach dem JavaScript entsteht, ist beim ersten Bild leer.

**Tests** (Python-seitig, das JS wird nicht unit-getestet — kein Node im Projekt, und ein
Test-Runner wäre eine neue Toolchain für sehr wenig):
- `test_static_files_are_served_with_correct_content_type`
- `test_static_hashed_assets_get_immutable_cache_header`
- `test_app_html_contains_no_inline_script`
- `test_app_html_contains_no_inline_style_attribute`
- `test_app_js_makes_no_external_requests` — Grep gegen `http://`/`https://`/`//cdn`
- `test_index_route_requires_session`

Die JS-Logik wird stattdessen über `ui_smoke.py` und die Live-Abnahme belegt. Das ist eine
bewusste Lücke, benannt statt verschwiegen.

---

### Step 7 — Editor, Vorschau, Konflikt, Frontmatter-Felder

**Dateien:** `webui/static/{app.js,app.css}` (Erweiterung).

Inhalte wie §3.5, §4.4, §4.5, P5-U.

Umfang:
- Textarea mit Monospace, Formatierleiste (fügt Markdown ein), Vorschau-Umschalter.
- Versionsband (§4.4) inklusive Konfliktzustand.
- Frontmatter-Editor: `title`, `status` (aus `models.STATUS_VALUES` je `type`), `due`, `tags`,
  `links`. `type` ist nach dem Anlegen **nicht** änderbar in der UI — der Store erlaubt es, aber
  ein Typwechsel ändert das gültige Statusvokabular, und das ist keine Interaktion, die man
  nebenbei klickt.
- Konfliktdialog mit den zwei Optionen aus §4.5.
- Entwurfsschutz über `sessionStorage`.
- Tastaturkürzel aus §4.6.

**Tests** (Python-seitig):
- `test_status_values_endpoint_matches_storage_models` — die UI darf das Vokabular nicht
  duplizieren; sie holt es aus `/api/v1/meta`
- `test_conflict_response_contains_full_current_item`
- `test_append_endpoint_is_used_for_append_not_patch`

**Done when:** `pytest` grün; ein vollständiger Durchlauf gegen eine lokale Wegwerf-Instanz mit
`tmp`-`DATA_ROOT`: anlegen → bearbeiten → Konflikt provozieren (zweiter Client) → auflösen →
archivieren.

---

### Step 8 — Betrieb: Deploy, Rollback, Staging, Auth-Backup, Messung

**Dateien:** `phase5_ui/scripts/{deploy.sh,rollback.sh,restore_auth_check.sh,ui_budget.py}`,
`phase5_ui/systemd/{sharefyx-authbackup.service,sharefyx-authbackup.timer,sharefyx-staging.service}`,
Ergänzung in `phase3_edge/scripts/diagnose.sh`.

**Deploy-Modell (P5-AB):**

```
/opt/sharefyx/releases/2026-08-14T18-22-05/     ← ausgecheckter Stand + venv
/opt/sharefyx/current -> releases/2026-08-14T18-22-05
```

`deploy.sh <git-ref>`:
1. `git bundle` des `DATA_ROOT` **und** verschlüsselte Kopie der `auth.sqlite3` ziehen
   (Pre-Deploy-Backup, unabhängig vom Timer).
2. Neues Release-Verzeichnis, `pip install`, `pytest -q` im Release. Schlägt es fehl → Abbruch,
   Symlink unberührt.
3. Symlink umlegen, `systemctl restart sharefyx-mcp`.
4. **Health-Gate:** bis zu 30 s auf `/health` `200` warten, dann eine authentifizierte
   API-Probe. Scheitert eines von beiden → automatisch `rollback.sh` und mit Exit-Code ≠ 0 enden.
5. Ältere Releases behalten: die letzten fünf.

`rollback.sh` legt den Symlink auf das vorherige Release und startet neu. Mehr nicht — je weniger
das Rollback tut, desto verlässlicher ist es.

**`[SEAM]` Blue/Green (P5-AC):** `deploy.sh` liest den Ziel-Port aus **einer** Variablen
(`SHAREFYX_PORT`, Default aus der Unit) und benutzt sie an genau einer Stelle. Der Phase-Head
dokumentiert den späteren Weg — Template-Unit `sharefyx-mcp@.service` plus Zielwechsel über
`tailscale serve`/`funnel` — **und die Bedingung, unter der er überhaupt sinnvoll wird:**
alle Schemaänderungen müssen ab dann expand/contract-fähig sein, weil zwei Farben dieselbe
`auth.sqlite3`, denselben Index und dasselbe Git-Repo benutzen. Wird in dieser Phase **nicht**
gebaut.

**Staging (P5-AB):** `sharefyx-staging.service` — zweite Instanz, eigener Port, eigener
`STATE_DIRECTORY`, `DATA_ROOT` als Klon (`git clone --no-hardlinks`), erreichbar **nur** über
`tailscale serve` (tailnet-intern), **niemals** über Funnel. `[VERIFY]` **V36:** Serve und Funnel
dürfen denselben Port nicht gleichzeitig belegen — Staging bekommt einen anderen.

**Auth-Backup (P5-R):** `sharefyx-authbackup.service` täglich:
`sqlite3 auth.sqlite3 ".backup /tmp/auth-<ts>.sqlite3"` → `systemd-creds encrypt` →
`/var/lib/sharefyx-backup/auth/`, sieben Generationen, `0600`, Eigentümer `root`.
`restore_auth_check.sh` entschlüsselt die jüngste Generation in ein Wegwerf-Verzeichnis, öffnet
sie und zählt Zeilen je Tabelle. **Der Nachweis ist der Lauf, nicht das Skript** — P3 Zeile 13
hat das gelehrt.

**Messung (P5-AD):** `ui_budget.py` misst gegen eine lokale Instanz mit synthetischem Bestand
(≥ 200 Items):

| Messgröße | Zielkorridor |
|---|---|
| `GET /api/v1/items?limit=50` roh / gzip | < 64 KB / < 12 KB |
| `GET /api/v1/items/{id}` typisch | < 8 KB |
| `app.js` + `app.css` + Font, gzip | < 250 KB gesamt |
| Erstaufruf `/ui/` bis interaktiv, Bytes gesamt | < 400 KB |

Ergebnis geht als Tabelle in den Phase-Head und **löst V10 auf**. Über- oder Unterschreitung
wird dokumentiert, nicht wegdiskutiert.

**`diagnose.sh`-Ergänzung:** UI erreichbar (`/ui/login` → 200), Session-Tabellenzahl,
letzter Auth-Backup-Zeitstempel, aktives Release-Verzeichnis. Zusammen mit V13 (Grep gegen echtes
`tailscale funnel status`) in einem Durchgang erledigen.

**Tests:**
- `test_deploy_script_aborts_when_tests_fail`
- `test_deploy_script_rolls_back_when_health_gate_fails`
- `test_rollback_restores_previous_symlink`
- `test_authbackup_keeps_seven_generations`
- `test_restore_auth_check_reports_row_counts`
- `test_ui_budget_reports_all_four_metrics`
- `test_staging_unit_uses_separate_state_directory`
- `test_staging_unit_is_not_funnel_exposed` — Grep gegen die Unit

---

### Step 9 — Live-Abnahme, zwei Personen, Handover

Kein neuer Feature-Code. Reihenfolge nach P5-AE („alles mit einem Mal"):

1. Migration der Nutzerakten live (§2.6-Runbook), inklusive Restart und Gegenprobe.
2. Nikinger fährt die vollständige Abnahmematrix (§6, Zeilen 1–20).
3. Fabian bekommt eine frische Einladung und fährt die Zwei-Personen-Zeilen (17–20) im selben
   Durchgang.
4. Erst danach: `LoadCredentialEncrypted=auth-users` aus der Unit, Keyring-Eintrag löschen,
   Restart, Gegenprobe.
5. `docs/concepts/P5_ABNAHME_<datum>.md` (📕, kein In-File-Card, Zeile in `docs/INDEX.md`).
6. `docs/concepts/phase5_ui_uebersicht.svg` — 1080×1080, Phasenübersicht wie in P3.
7. `docs/concepts/PHASE5_CLOSEOUT_HANDOVER.md` mit vollständigem `[VERIFY]`-Register.
8. Rotationsprüfung auf `phase5_ui/CLAUDE.md`.
9. `ROADMAP.md` + Root-`CLAUDE.md` auf ✅, **erst wenn die Matrix vollständig ist** — 🟡 heißt
   code-complete, ✅ heißt live-verifiziert.

---

## §6 Akzeptanzkriterien

**Block A (Gate nach Step 4):**

| # | Kriterium | Nachweis |
|---|---|---|
| 1 | Einladungslink erzeugt, Konto von null auf aktiv eingerichtet | Live, Browser |
| 2 | Einladungslink ein zweites Mal aufgerufen → abgelehnt | Live |
| 3 | TOTP-Seed einmal angezeigt, in einer echten Authenticator-App aufgenommen, Code akzeptiert | Live |
| 4 | Recovery-Codes einmal angezeigt; einer davon ersetzt beim Login den TOTP-Code; derselbe Code danach abgelehnt | Live |
| 5 | Passwort im Browser geändert, **ohne** `systemctl restart` — der neue Login funktioniert sofort | Live, **schließt O1** |
| 6 | Nach dem Passwortwechsel: Connector fordert neue Autorisierung, andere UI-Sitzung ist beendet, aktuelle läuft weiter | Live |
| 7 | Fehlversuchsbremse greift für UI-Login und OAuth-Consent gemeinsam | Live |
| 8 | `authctl.py list-users` zeigt keinen Hash und keinen Seed | Live |
| 9 | `auth.sqlite3` mit `strings` durchsucht: **kein Base32-TOTP-Seed im Klartext auffindbar** | Live, `strings`/`sqlite3` |

**Block B:**

| # | Kriterium | Nachweis |
|---|---|---|
| 10 | Anlegen, Bearbeiten, Anhängen, Archivieren über die UI; die `.md`-Datei im `DATA_ROOT` sieht danach korrekt aus und der Git-Commit existiert | Live, `git log` im Datenverzeichnis |
| 11 | Konflikt: zwei Tabs, beide bearbeiten dasselbe Item → der zweite bekommt das Versionsband in `--warn` und den Dialog, **kein stiller Überschreiber** | Live |
| 12 | Fremder Space: sichtbar, lesbar, **ohne** Schreib-Bedienelemente im DOM | Live, DevTools |
| 13 | Ein Item mit einem unbekannten Frontmatter-Feld überlebt eine Bearbeitung durch die UI unverändert | Live, `git diff` |
| 14 | `format: markdown` erscheint nach dem ersten UI-Schreibvorgang im Frontmatter und stört keinen Tool-Aufruf | Live |
| 15 | `ui_budget.py` liefert alle vier Zahlen, Ergebnis im Phase-Head | Live |
| 16 | `deploy.sh` mit absichtlich kaputtem Health-Endpunkt rollt automatisch zurück | Live |

**Übergreifend:**

| # | Kriterium | Nachweis |
|---|---|---|
| 17 | Beide Nutzer benutzen die UI und den Connector am selben Tag gegen dieselbe Instanz | Live, zwei Personen |
| 18 | `git diff` auf `storage/`, `mcpserver/tools.py`, `mcpserver/permissions.py`, `mcpserver/server.py` über die ganze Phase: **leer** | `git diff` |
| 19 | Cookie an `/mcp` wird ignoriert; Bearer an `/api` wird ignoriert | Test + Live-`curl` |
| 20 | Reboot der VM: UI, Connector, Timer kommen ohne Handgriff zurück | Live, passiv zulässig |

**Statusregel:** Phase 5 ist 🟡, solange auch nur eine Zeile offen ist. ✅ heißt live-verifiziert,
nicht gebaut.

---

## §7 Indexzeilen für `docs/INDEX.md`

Im selben Commit wie die jeweilige Datei (Hard Rule 8):

```
- [docs/concepts/phase5_ui_plan.md](./concepts/phase5_ui_plan.md) — 📕 ~55KB · Ausführungsreifer P5-Plan: Entscheidungen P5-A–P5-AE, Steps 0–9 (Block A Sicherheit/Selbstverwaltung, Block B REST-API/UI), Designsystem, Abnahmematrix 1–20, [VERIFY]-Register V27–V38
- [docs/concepts/PHASE4_CLOSEOUT_HANDOVER.md](./concepts/PHASE4_CLOSEOUT_HANDOVER.md) — 📕 ~18KB · Abschluss-Handover P4→P5: Status, Delta seit dem P3-Handover, offene Entscheidungen für die Web-UI-Planung, [VERIFY]-Bilanz V14–V26
```

Später in der Phase, jeweils im eigenen Commit:

```
- [phase5_ui/CLAUDE.md](../phase5_ui/CLAUDE.md) — 🔄 ~?KB · Phase-Head P5: Modulstatus, Runbooks (Migration, Deploy, Einladung), genau ein Session-Block
- [phase5_ui/SESSIONS_ARCHIVE.md](../phase5_ui/SESSIONS_ARCHIVE.md) — 📦 ~?KB · archivierte P5-Session-Blöcke, verbatim
- [docs/concepts/P5_ABNAHME_<datum>.md](./concepts/P5_ABNAHME_<datum>.md) — 📕 ~?KB · Live-Abnahme P5, 20 Zeilen, Rohbelege
- [docs/concepts/PHASE5_CLOSEOUT_HANDOVER.md](./concepts/PHASE5_CLOSEOUT_HANDOVER.md) — 📕 ~?KB · Abschluss-Handover P5→P6
```

`[VERIFY]` **V37:** die exakten Abschnittsüberschriften in `docs/INDEX.md` („Active phase (…)",
„Completed phases") gegen die reale Datei prüfen — sie werden je Phase umbenannt.

---

## §8 `[VERIFY]`-Register

| # | Was | Wann aufzulösen |
|---|---|---|
| **V27** | Exakte Klassen-/Methodennamen in `mcpserver/permissions.py` (`OwnSpaceWritable`, `can_read`, `can_write`) und die reale Signatur | Step 5, vor dem ersten Import |
| **V28** | `cryptography`-Version, die auf der VM installierbar ist; `AESGCM`-Import beweisen; exakt pinnen | Step 0 D, spätestens Step 2 |
| **V29** | QR-Bibliothek (`segno`?) inkl. Version — oder Fallback „nur Base32-Text" | Step 4 |
| **V30** | Herkunft, Stand und Größe der Passwort-Blocklist | Step 4 |
| **V31** | Inter-Variable: Lizenz, Subsetting, Dateigröße, Cache-Header. Sonst Systemstack | Step 6 |
| **V32** | Reale `pytest`-Ausgangszahl nach dem Rückbau in Step 0 A (sie **sinkt**) | Step 0 B |
| **V33** | Anthropic-Connector-Doku erneut gegenlesen (Nachfolger von V14): Callback-URLs, DCR-Deprecation, `application_type` | Step 1 |
| **V34** | `README.md` im aktuellen Stand lesen, bevor sie korrigiert wird (Größe hat sich seit Juli geändert) | Step 0 C |
| **V35** | `scripts/dev_install.sh` nimmt `phase5_ui/` auf, ohne geändert zu werden (Analogie V16) | Step 3 |
| **V36** | Tailscale: Serve und Funnel auf demselben Port schließen sich aus — freien Port für Staging bestimmen | Step 8 |
| **V37** | Exakte Abschnittsüberschriften in `docs/INDEX.md` | Step 0 C |
| **V38** | Reale Zeilennummern aller Plan-Anker (Nachfolger von V24) | je Step beim Verdrahten |
| — | **Geerbt:** V10 (Größenbudget → wird durch P5-AD/`ui_budget.py` aufgelöst), V12 (Uplink-Datenlimit → Messung in Step 0 D, Bewertung in Step 8), V13 (`diagnose.sh`-Grep → Step 8) | siehe Spalte |

---

## §9 Was nach P5 offen bleibt

Für den Closeout-Handover, damit es nicht neu hergeleitet werden muss:

- **Mini-Phase MCP-Revision `2026-07-28` + FastMCP 4.** Trigger ist gefallen (Spec final seit
  2026-07-28), aber FastMCP 4 ist noch Beta. Berührt Transport und Lifecycle, nicht Auth, nicht
  die UI. **Die Zwölf-Monats-Frist der DCR-Deprecation läuft ab dem 2026-07-28** — CIMD gehört
  in dieselbe Mini-Phase, nicht in eine eigene.
- **Echtes Blue/Green.** Der Seam steht (P5-AC). Voraussetzung ist eine expand/contract-Disziplin
  für alle Schemaänderungen.
- **Helles Thema.** Tokens sind dafür gebaut (P5-X), es ist ein Token-Tausch plus Kontrastprüfung.
- **Mobilversion.** Ausdrücklich aus P5 herausgehalten (P5-W).
- **Zweites Dateiformat / Anhänge.** Seam steht (P5-Z), Entscheidung nicht getroffen. Vorher zu
  beantworten: wie wrappt Rule 4 einen fremden Nicht-Text-Body?
- **D6** (SQL-Filterung in `Store.search`) — wird durch `ui_budget.py` zum ersten Mal mit Zahlen
  entscheidbar statt mit Gefühl.
- **`Permissions.can_read`** als echte Policy zwischen Spaces — Seam unverändert, Policy weiter
  bewusst `True`.
- **Off-site-Backup und Monitoring** — unverändert zurückgestellt.
- **DPoP** — sobald ein Client es spricht.

---

## §10 Eine Warnung zum Schluss

Diese Phase führt mehr Neues ein als P2, P3 und P4 zusammen: ein neues Paket, ein
Datenmodell-Umbau am Auth-Kern, eine zweite HTTP-Oberfläche, ein Deployment-Verfahren und ein
Designsystem. Der wahrscheinlichste Fehlermodus ist **nicht** ein Bug, sondern
**Scope-Aufweichung** — „das Frontmatter-Feld könnte man auch gleich…", „ein Upload wäre doch
nur…", „wenn wir schon dabei sind, dann auch mobil".

Dagegen hilft genau eine Sache, und sie steht schon in der ROADMAP: **unter Druck fällt die
späteste Phase weg, nie eine frühere Regel.** Innerhalb dieser Phase heißt das: unter Druck
fällt Block B weg, nicht Block A. Ein System, in dem ein Mensch sein Passwort selbst setzen
kann, ist auch ohne schöne Oberfläche ein Werkzeug. Eine schöne Oberfläche auf einem Konto, das
nur per SSH existiert, ist es nicht.
