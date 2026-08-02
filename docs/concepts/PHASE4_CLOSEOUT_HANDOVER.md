---
status: snapshot
purpose: Abschluss-Handover P4→P5 — Status, Delta seit dem P3-Handover, offene Entscheidungen für die Web-UI-Planung, [VERIFY]-Bilanz V14–V26
read-when: Start der P5-Planungssession, VOR dem Entwurf des Claude-Code-Plans — dann einmal ganz lesen
detail: L2
up: ../../phase4_auth/CLAUDE.md
down:
  - ./phase4_auth_plan.md                      # Entscheidungen P4-A–P4-R, Steps 0–7 — Herkunft, nicht Ergebnis
  - ./P4_ABNAHME_2026-07-29.md                 # was am 2026-07-29/30 tatsächlich funktioniert hat, 16/16
  - ./P4_SECURITY_REVIEW_2026-07-29.md         # S2–S8 offen + 15 verified negatives — vor jedem Fix lesen
  - ./PHASE3_CLOSEOUT_HANDOVER.md              # Vorgänger; V1–V13, Herkunft der P4-Entscheidungen
updated: 2026-08-01
---
# Phase 4 — Closeout-Handover (P4 → P5)

> **Für den kalten Leser.** Phase 4 ist abgeschlossen: **16/16 Abnahmezeilen live bestanden,
> 347 Tests grün, Schnitt vollzogen.** Der Pfad-Token existiert nicht mehr.
>
> **Dieses Dokument ist keine zweite Kopie des Plans.** Code ist Wahrheit; der Plan
> (`phase4_auth_plan.md`) ist Herkunft, das Abnahmeprotokoll ist Beleg, der Phase-Head
> (`phase4_auth/CLAUDE.md`) ist der operative Einstieg. Hier steht nur, was der P5-Chat wissen
> muss, **bevor** er plant — plus die Dinge, die sonst niemand aufschreibt.

---

## 1 Status in fünf Sätzen

1. **Der Pfad-Token ist weg.** Die Connector-URL lautet `https://<host>/mcp`, ohne Geheimnis.
   `TokenPathASGI` und `AuthModeASGI` sind aus dem Code entfernt, beide Token widerrufen,
   `SPACE_AUTH_MODE` lässt nur noch `oauth` zu.
2. **Ein eigener Authorization Server läuft im selben Prozess** — Discovery, DCR, PKCE `S256`,
   Argon2id + TOTP, opake Token mit Rotation und Familien-Widerruf nach RFC 9700.
3. **Der P2-Seam hat gehalten.** `git diff` auf `tools.py`, `permissions.py`, `server.py`,
   `storage/` blieb über die ganze Phase **leer** — die komplette Authentifizierung wurde
   ausgetauscht, ohne eine Zeile Tool-Code anzufassen. Das ist das stärkste Einzelergebnis der
   Phase, stärker als der Login selbst.
4. **Zwei echte Menschen sind live durchgelaufen.** Fabian hat von sich aus ein vollständiges
   Sechs-Tool-Protokoll plus zwei selbst gewählte Negativtests gefahren (Optimistic-Locking-
   `conflict`, Cross-Space-`write_denied`) — Rule 4 ist damit zum ersten Mal unter echtem OAuth
   **und** einem zweiten, unabhängigen Nutzer beobachtet.
5. **Offen bleiben bewusst:** sieben kleinere Sicherheitsbefunde (S2–S8), P3s Zeile 13
   (Restore-Nachweis, hält Phase 3 auf 🟡) und — für P5 das Wichtigste — **die Tatsache, dass es
   für Menschen keinen Weg gibt, ein Passwort zu setzen** (§4.1).

**Rotationsprüfung (Auftrag 4):** `phase4_auth/CLAUDE.md` trägt **genau einen** Session-Block
(`## Session stopped — 2026-07-30`, mit drei datierten Nachträgen). 36.569 B, unter dem
40-KB-Softcap. `SESSIONS_ARCHIVE.md` trägt neun archivierte Blöcke plus die am 2026-07-31
verbatim ausgelagerte Steps-0–6a-Narrative. **Nichts zu tun.**

---

## 2 Delta seit dem P3-Handover

Nur was sich geändert hat. Alles Unveränderte steht im P3-Handover und gilt weiter.

| Thema | P3-Stand | P4-Stand |
|---|---|---|
| Authentifizierung | Token im Pfad, `TokenPathASGI` | OAuth 2.1, `BearerAuthASGI` + `OAuthTokenResolver` |
| Identitätsquelle | Keyring `spaces` (nur Hashes) | Keyring `auth-users` — **enthält echte, umkehrbare TOTP-Seeds** |
| Zustand | zustandslos, alles aus Dateien | **zusätzlich** `/var/lib/sharefyx/auth.sqlite3`, autoritativ (P4-I) |
| Unit | `phase3_edge/systemd/` | MCP-Unit zog nach `phase4_auth/systemd/`; `StateDirectory`, zweites Credential |
| Abhängigkeiten | `fastmcp==3.4.4` | **+ `argon2-cffi==25.1.0`** exakt gepinnt. Sonst nichts Neues |
| Tests | ~168 | **347** |
| R5 (Auth v0) | gültig | **abgelöst** — im Root-`CLAUDE.md` datiert korrigiert |
| Hard Rule 1 | Token-Hashes im Keyring | ergänzt: ab P4 liegen dort **echte Geheimnisse**, gleicher Ort, höherer Einsatz |

**Neue Betriebswahrheiten, die P5 kennen muss:**

- **Nutzerakten werden genau einmal beim Start gelesen** (O1). Ein `provision_user.py`-Lauf wirkt
  erst nach `systemctl restart sharefyx-mcp`. Wer das vergisst, misst den alten Stand und sucht
  am falschen Ende.
- **`authctl.py` braucht `STATE_DIRECTORY=/var/lib/sharefyx`** außerhalb von systemd — bewusst
  kein stiller Fallback ins Arbeitsverzeichnis.
- **`ALLOWED_HOSTS` muss `127.0.0.1` enthalten**, sonst beantwortet die
  `TrustedHostMiddleware` jede lokale Anfrage mit `400`, inklusive `/health` und `diagnose.sh`.
- **DCR-Bremse: 20 Registrierungen pro Stunde, global.** Nach viel Testen ein `429`, kein Bug.
- **Claudes MCP-Client refresht `on-demand`, nicht per Timer** — belegt über 14 `access_tokens`-
  Zeilen derselben Familie. Für P5 relevant, falls dort Sitzungsverhalten modelliert wird.

---

## 3 Was P5 vom Code erbt — Verweise, keine Kopien

| Was | Wo |
|---|---|
| Alle 18 gelockten Entscheidungen P4-A–P4-R | `docs/concepts/phase4_auth_plan.md` §0.7 |
| Normative Grundlage (BSI TR-02102-1 2026-01, OWASP, RFC 9700/9728/8414/7591/7636/6238/9207) | ebd. §0.5 |
| Harte Client-Vorgaben von Anthropic (Callback-URL, Timeouts, Content-Types) | ebd. §0.6 — **`[VERIFY]` bei jeder Wiederverwendung**, die Seite ändert sich schneller als das Repo |
| Datenmodell der Auth-SQLite | `authserver/store.py` — Schema ist dort, nicht im Plan |
| Sicherheits-Header, CSP inkl. `csp_form_action` | `authserver/routes.py :: _security_headers()`, `config.py :: AuthSettings.csp_form_action` |
| Redirect-Prüfung — **die einzige Stelle** | `authserver/clients.py :: redirect_uri_allowed()`, abgesichert durch `test_redirect_uri_allowed_is_the_only_matching_path` |
| Runbooks (Inbetriebnahme, Zeile-9-Anleitung, `authctl`-Fallstricke) | `phase4_auth/CLAUDE.md` |
| Was live tatsächlich funktioniert hat | `docs/concepts/P4_ABNAHME_2026-07-29.md` |
| Was geprüft und für in Ordnung befunden wurde (15 verified negatives) | `docs/concepts/P4_SECURITY_REVIEW_2026-07-29.md` |

---

## 4 Offene Entscheidungen für die P5-Planung

Diese gehören in die Q&A-Runde **vor** dem Plan, nicht in die Implementierung.

### 4.1 Initiale Passwortvergabe — der eigentliche Blocker

**Das ist die wichtigste Zeile dieses Handovers.** Nikinger-Befund aus dem Live-Betrieb,
2026-08-01:

> Alles live getestet, jedoch ist definitiv eine initiale Passwort-Logik und extrem gute UI
> wichtig, um das Tool tatsächlich benutzbar zu halten.

Der aktuelle Stand ist ehrlich benannt: **es gibt keine Passwortvergabe für Menschen.** Es gibt
`provision_user.py` — ein SSH-Skript, das ein Passwort per `getpass` entgegennimmt und einen
TOTP-Seed genau einmal auf stdout schreibt. Danach: `export_auth_users.py` in eine Pipe,
`systemd-creds encrypt`, `systemctl restart`. **Vier Schritte, alle auf der VM, alle als
`savefyx`.** Für zwei Personen, von denen eine die VM administriert, hat das für P4 gereicht.
Als Dauerzustand ist es der Grund, warum das System kein Werkzeug ist, sondern ein Prototyp.

Konkret fehlt — jeder Punkt eine eigene Entscheidung, keine automatisch:

1. **Erstvergabe.** Einladungslink mit Einmal-Token? Initialpasswort mit erzwungenem Wechsel?
   Selbstregistrierung scheidet aus (zwei Nutzer, keine offene Anmeldung).
2. **Wechsel durch den Nutzer selbst**, ohne SSH und ohne Restart. Das kollidiert direkt mit
   O1 (`load_users()` liest einmal beim Start) — **P5 muss diesen Ladepfad anfassen, oder
   Passwortwechsel bleibt eine Neustart-Operation.** Das ist eine Architekturentscheidung, kein
   UI-Detail.
3. **TOTP-Einrichtung im Browser** statt QR-Code aus einer SSH-Sitzung. Braucht eine sichere
   Anzeige des Seeds genau einmal, plus einen Verifikationsschritt vor der Aktivierung.
4. **Wiederherstellung.** P4-H hat Recovery-Codes bewusst abgelehnt („der Betreiber hat SSH").
   Sobald es eine UI gibt, ist diese Begründung schwächer — **die Entscheidung gehört neu
   verhandelt, nicht stillschweigend fortgeschrieben.**
5. **Wo leben die Nutzerakten dann?** Keyring + `systemd-creds` ist ein Ein-Personen-Betriebsweg.
   Eine UI, die Passwörter schreibt, braucht einen schreibbaren Speicher — Kandidat ist die
   bestehende `auth.sqlite3`. Das wäre eine Erweiterung der P4-I-Ausnahme von Hard Rule 2 und
   muss **ausdrücklich** entschieden werden.

**Ehrliche Einordnung:** Punkt 2 und Punkt 5 sind zusammen kein UI-Thema, sondern ein Umbau am
Auth-Kern. Wer P5 als „Web-UI bauen" plant und die Passwortvergabe als Bildschirm darin
einsortiert, unterschätzt sie. Es ist plausibel, dass daraus eine **eigene Phase oder ein
eigener Step-Block vor der UI** wird. Das gehört in die Q&A, nicht in eine spätere Überraschung.

### 4.2 Weitere Dateiformate offenhalten

Nikinger-Vorgabe, 2026-08-01: **Markdown bleibt das Hauptformat**, aber weitere Formate sollen
offengehalten werden.

Das ist heute **nicht** der Fall, und zwar an mehreren Stellen gleichzeitig:

- `storage/` geht durchgängig von `.md` mit YAML-Frontmatter aus — Parser, Schreibpfad, Index.
- Der SQLite-Index kennt genau die Frontmatter-Felder aus P1.
- Die sechs Tools haben `body` als Textfeld; `create_item`/`append_to_item` kennen kein
  Binärformat und keinen MIME-Typ.
- P1-Handover und ROADMAP nennen Anhänge ausdrücklich als **draußen**.

**Was P5 dazu entscheiden muss** (nicht implementieren — entscheiden):

1. Geht es um **Textformate** neben Markdown (`.txt`, `.org`, `.csv`) oder um **Anhänge**
   (Bilder, PDF)? Das sind zwei völlig verschiedene Umbauten. Anhänge brechen „Dateien sind die
   Wahrheit" nicht, aber sie brechen das Frontmatter-Modell und die Token-Budget-Disziplin.
2. Reicht ein **`format`-Feld im Frontmatter** plus ein Seam im Store, oder braucht es einen
   zweiten Item-Typ? Ein Seam wäre billig und jetzt richtig platziert — genau das Muster von
   `Permissions.can_read`.
3. **Wie verhält sich Rule 4 zu einem fremden Nicht-Text-Body?** `<untrusted_content>` wrappt
   Text. Ein fremdes PDF ist kein wrapbarer String. Das ist kein Randfall, sondern eine offene
   Sicherheitsfrage — und sie muss beantwortet sein, **bevor** ein zweites Format existiert.

**Empfehlung für die Q&A:** in P5 einen benannten `[SEAM]` setzen (Frontmatter-Feld + eine
Verzweigungsstelle im Store), aber **kein zweites Format implementieren**. Formate sind billig
hinzuzufügen und teuer zurückzunehmen; das Datenmodell trägt die Konsequenz dauerhaft.

### 4.3 Web-UI: Neubau oder Adaption

Unverändert offen seit P1. `Notizheft_example.html` liegt im Projektwissen, seine clientseitige
Vault-Verschlüsselung ist mit R4 unvereinbar und müsste entfallen — was den Anpassungsaufwand
womöglich über den eines Neubaus hebt. **Vor P5 klären, nicht während.**

Neu hinzugekommen: die UI erbt jetzt einen konkreten Vorgänger. Die P4-Login-Seiten
(`authserver/templates.py`) sind **ausdrücklich als Wegwerf gebaut** — kein Framework, kein JS,
keine Cookies, Modul-Docstring sagt es wörtlich. Sie sind der erste Kunde der P5-UI, nicht ihr
Vorbild. Wer sie erweitert statt ersetzt, hat die Entscheidung P4-O missverstanden.

### 4.4 Sicherheitsbefunde S2–S8 — Reihenfolge entscheidet der Nikinger

Vollständig in `P4_SECURITY_REVIEW_2026-07-29.md`. Kurzfassung mit P5-Relevanz:

| # | Befund | Warum es P5 angeht |
|---|---|---|
| S2 | `refresh_token`-Grant prüft `client_id` nicht | Spec-Abweichung, praktisch gering |
| **S3** | **Kein Audience-Check** (`record.resource` nie gegen `settings.resource` geprüft) | **Wird mit P5 echt.** Heute gibt es genau eine Ressource. Eine REST-API ist die zweite — dann ist die Lücke real, und dann steht sie nicht mehr in einem frischen Review |
| **S4** | **`scope` wird beim Zugriff nie durchgesetzt** | Ein Token mit `offline_access` allein bekommt vollen Tool-Zugriff. Drei Zeilen Fix. Wenn P5 Scopes für die REST-API einführt, **muss** das vorher stehen |
| S5 | `redirect_uri` mit vorhandenem Query erzeugt kaputte URL | Korrektheit |
| S6 | Kaputte Nutzerakte → `KeyError` → 500 | **Berührt §4.1 direkt.** Sobald eine UI Nutzerakten schreibt, steigt die Wahrscheinlichkeit halb geschriebener Datensätze — und ein 500 nur für existierende Spaces ist genau das Enumerations-Orakel, das der Code sonst vermeidet |
| S7 | Unbegrenztes Zeilenwachstum, `purge_expired()` nur manuell | Disk-DoS auf öffentlichem Endpunkt. Ein `sharefyx-purge.timer` analog zur Backup-Unit wäre die saubere Antwort |
| S8 | `sudo install_units.sh` sourced nutzerschreibbare Datei als root | Sehr niedrig auf dieser VM |

**Empfehlung:** S3, S4 und S6 vor oder zu Beginn von P5 fixen — sie sind billig und werden
durch P5 teurer. S2, S5, S7, S8 können warten.

### 4.5 Vorgemerkt, klein, aber gefährlich beim Aufräumen

**`spaces.cred` ist totes Gewicht — und bricht trotzdem den Dienst, wenn es jemand löscht.**
`serve.py` liest die Space-Map seit dem Schnitt nicht mehr, aber die installierte Unit trägt
weiter `LoadCredentialEncrypted=spaces:/etc/sharefyx/spaces.cred` und verweigert ohne diese
Datei den Start. Wer sie als „obsoletes P2-Überbleibsel" wegräumt, legt den Server still.

Aufzuräumen sind zusammen: die Unit-Zeile, `export_space_map.py`, `issue_token.py`,
`credentials.py :: load_space_map()`. Braucht `install_units.sh` + Restart, also eine
Nikinger-Aktion. **Gehört in P5 Step 0**, nicht in eine spontane Aufräumaktion.

---

## 5 `[VERIFY]`-Bilanz

### 5.1 Aus Phase 4 (V14–V26)

| # | Was | Ergebnis |
|---|---|---|
| V14 | Anthropic-Auth-Doku gegenlesen | **Aufgelöst** (2026-07-28). 13 von 14 Plan-Annahmen bestätigt. **Eine Abweichung:** native/Loopback-Clients (RFC 8252 §7.3) sind inzwischen dokumentiertes, aktuelles Anthropic-Verhalten — Claude Code deklariert `http://127.0.0.1/callback` **und** `http://localhost/callback`, Port ignoriert. Nikinger-Entscheidung: trotzdem draußen. Der einfachere Weg für später steht im Phase-Head, damit er nicht neu recherchiert werden muss |
| V15 | `argon2-cffi`-Major exakt pinnen | **Aufgelöst** — `argon2-cffi==25.1.0` |
| V16 | `dev_install.sh` nimmt `phase4_auth/` auf, ohne geändert zu werden | **Aufgelöst** — `pyproject.toml` vorhanden, Tests laufen. *(Abgeleitet aus dem laufenden Betrieb; im Snapshot nicht als eigener Prüfsatz dokumentiert)* |
| V17 | Argon2id-Laufzeit auf der VM | **Aufgelöst mit Korrektur.** Der Plan-Default `t=2` maß ~15 ms — unter dem Zielkorridor 50–250 ms. Code läuft seit Step 2 mit **`t=8`** (~53–55 ms, gemessen). Konstante: `authserver/passwords.py :: ARGON2_TIME_COST` |
| V18 | NTP-Synchronität für TOTP | **Aufgelöst** — TOTP funktioniert live über mehrere Tage und zwei Nutzer. *(Praktisch bewiesen; ein expliziter `timedatectl`-Nachweis steht nicht im Snapshot)* |
| V19 | Exakte Form des `WWW-Authenticate`-Headers | **Aufgelöst** — Abnahmezeile 2 live bestanden, Connect-Button erschien |
| V20 | Ausgangs-Testzahl | **Aufgelöst** — Step 0 gemessen, heute 347 |
| V21 | `auth.sqlite3` gitignored | **Aufgelöst** — Security-Review, verified negative #14 |
| V22 | systemd ≥ 235 für `StateDirectory=` | **Aufgelöst** — Dienst läuft produktiv damit |
| V23 | Funnel reicht `/.well-known/*` durch | **Aufgelöst** — Abnahmezeile 3 live |
| V24 | Reale Zeilennummern der Plan-Anker | **Aufgelöst** — Step 6 verdrahtet |
| V25 | `fastmcp`-Versionslage, P3-E-Trigger | **Notiert, bewusst nicht gehandelt.** FastMCP 4 spricht die MCP-Revision 2026-07-28, der Trigger gilt als gefallen. Eigene Mini-Phase, **nicht** mit einem Auth- oder UI-Umbau bündeln |
| V26 | Geerbte P3-Marker | siehe §5.2 |

### 5.2 Geerbt aus Phase 3 — Stand jetzt

| # | Was | Stand |
|---|---|---|
| V10 | Größenbudget `search_items` | **offen** — nie gemessen, bei zwei Nutzern unkritisch. Wird mit P5 relevant, falls die UI Listen über dieselbe Suche zieht |
| V11 | MCP-Revision 2026-07-28 | **überholt durch V25** — Trigger gefallen, eigene Mini-Phase |
| V12 | Datenlimit des Mobilfunk-Uplinks | **offen** — nie bewertet. P5 erhöht das Volumen (Assets, Polling), also **vor** dem UI-Design einmal ansehen |
| V13 | `diagnose.sh`-Grep gegen echtes `tailscale funnel status` | **offen** |

### 5.3 Geerbte Abnahmezeile

**P3 Zeile 13 — Restore-Nachweis** ist die einzige noch fehlende Zeile und hält **Phase 3
weiterhin auf 🟡**. Zeilen 6 (Reboot) und 12 (Backup-Timer) haben sich im P4-Zeitraum passiv
erfüllt. Zeile 13 braucht ein frisches `git bundle` und einen `restore_check.sh`-Lauf —
**Achtung:** `restore_check.sh` **nicht umbauen**, bevor ein Lauf unter realen Bedingungen
stattgefunden hat; der P3-Befund B5 (Bundle älter als HEAD) war kein Defekt.

---

## 6 Was der P5-Chat als Erstes tun sollte

1. **Step 0 wie gehabt:** Verifikationsdurchlauf (`up:`/`down:` auflösbar, Indexzeile je `.md`,
   40-KB-Check, `pytest -q` gegen 347). „Nichts zu tun" ist ein zulässiges Ergebnis.
2. **`spaces.cred` und den P2-Token-Pfad zurückbauen** (§4.5) — mit Restart, als
   Nikinger-Aktion.
3. **P3 Zeile 13 einsammeln**, dann Phase 3 auf ✅ heben.
4. **S3/S4/S6 vor dem UI-Bau fixen** (§4.4) — billig jetzt, teuer später.
5. **In der Q&A klären, bevor geplant wird:** §4.1 (Passwortvergabe — inklusive der Frage, ob
   das eine eigene Phase ist), §4.2 (Formate: Seam ja, Implementierung nein), §4.3 (Neubau vs.
   Adaption), §4.4 (Fix-Reihenfolge).

**Eine Warnung zum Schluss, weil sie in P4 zweimal Geld gekostet hat:** eine Doku-Aussage über
den Repo-Zustand ist erst wahr, wenn `git status` sie bestätigt. Der Phase-Head selbst
dokumentiert zwei Fälle, in denen eine Tabellenzeile drei Steps hinterherhinkte, und einen, in
dem eine Context-Compaction die Details verlor und die Session mit einer unverifizierten
Prämisse begann. Beim P5-Start gilt dasselbe für **dieses** Dokument: es ist ein 📕-Snapshot vom
2026-08-01. Was danach passiert ist, steht nicht darin.
