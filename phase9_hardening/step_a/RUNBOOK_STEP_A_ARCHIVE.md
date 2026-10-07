---
status: archive
purpose: L3-Archiv des Step-A-Runbooks — die zehn Befunde (§0) und die erledigten Schritte A1–A7, verbatim, unter denselben Überschriften
read-when: beim Audit, wenn „Runbook §0 Befund N" oder ein erledigter Schritt A1–A7 zitiert wird; das Runbook selbst trägt Überschrift und Zeiger
detail: L3
up: ./RUNBOOK_STEP_A.md
down:
updated: 2026-10-07 (angelegt — Nikinger-Auftrag „find a fix for the oversize docs"; §0 Befund 1–10 und A1–A7 per `scripts/move_sections.py` verbatim hierher, A8/A9 bleiben im Runbook, weil A8 für das zweite Konto offen ist)
---
# Runbook Step A — Befunde und erledigte Schritte (verbatim)

> Alles unter dieser Zeile ist **wortgleich** aus `RUNBOOK_STEP_A.md` verschoben, in Dokumentreihenfolge.

## §0 Zehn Befunde, die den Step geändert haben

[2026-10-01: 7 → 10. **Befund 8** (P9-10 ist bis A7 nicht erfüllbar, gemessen gegen den laufenden
Dienst), **Befund 9** (kein Caddy auf dem VPS, A4 hatte keinen Install-Schritt) und **Befund 10**
(`caddy validate` liest den Adapter aus dem Dateinamen) sind nachträglich dazugekommen; alle drei
haben den Ablauf geändert, nicht nur beschrieben. **A4 ist ausgeführt** (P9-10a grün, unten).]

Diese zehn sind **kein Vorwand, nichts zu tun** — jeder davon ist entweder eine
Plan-Korrektur (der Code sagt etwas anderes als der Plan) oder ein Klärungsbedarf, der
sonst mitten in A4 aufgetaucht wäre. Alle mit Fundstelle, damit sie nachprüfbar sind, nicht
behauptet.

### Befund 1 — A4 ist als geschrieben nicht baubar: auf der Tailnet-IP lauscht nichts

**Das ist der teuerste Befund, weil er die ganze Bauform betrifft.**

- `phase4_auth/systemd/sharefyx-mcp.service:13` — `Environment=SPACE_HOST=127.0.0.1`
- `ss -ltnp` (2026-09-29) — `LISTEN 127.0.0.1:8765 users:(("python",pid=1032))`, und
  **kein** weiterer Listener auf `100.93.43.122:8765`
- `tailscale serve status` — der Funnel proxyt auf `http://127.0.0.1:8765`; er funktioniert
  genau deshalb, weil `tailscaled` auf derselben Maschine in die Schleife connectet

Plan §3.2 A4 verlangt `reverse_proxy <heimvm-tailnet-name>:<port>`. Genau das kann nicht
funktionieren: auf der Tailnet-Adresse gibt es keinen Port, an den ein VPS sich connecten
könnte. **Die naheliegende Reparatur — `SPACE_HOST` auf `0.0.0.0` — ist verboten**, das ist
die gelockte P3-B-Entscheidung („`SPACE_HOST` wird nie `0.0.0.0`"; gilt am Host, nicht nur am
Router). Sie zu brechen, um einen Proxy zu retten, wäre genau die stille Abweichung, die
P8.6 zweimal gekostet hat.

**Die gewählte Lösung: ein Relay auf der Tailnet-IP, das nach Loopback weiterreicht.**
`phase3_edge/systemd/sharefyx-tail-proxy.service` (neu, in diesem Commit) macht
`100.93.43.122:8765 → 127.0.0.1:8765` mit `socat`. Die Anwendung bindet unverändert auf
Loopback, P3-B bleibt unangetastet, und der VPS erreicht genau diesen einen Port.

Zwei Alternativen, beide **verworfen**, mit Grund:

| Alternative | Warum nicht |
|---|---|
| `SPACE_HOST=0.0.0.0` (oder auf die Tailnet-IP) | Bricht P3-B und macht den Port zusätzlich im LAN erreichbar — in einer Härtungsphase eine Vergrößerung der Angriffsfläche, die niemand verlangt hat. |
| `tailscale serve --tcp=8765 tcp://127.0.0.1:8765` (Tailscale 1.102.4 kann das, `serve --help` gemessen) | Kein zusätzlicher Prozess, das wäre der elegantere Weg — **aber** ob Tailscale-TCP-Forwarder die Tailnet-ACLs durchsetzen, war in dieser Session **nicht verifizierbar** (kein Netzzugriff, s. §6 V162). Eine offene Frage darf nicht die Grundlage einer Firewall-Entscheidung sein. Der Relay ist ein gewöhnlicher Listener auf `tailscale0`, für den das ACL-Modell ohne Zusatzannahme gilt. |

**Für den VPS heißt das:** `reverse_proxy` zielt auf den **Tailnet-Namen oder die IP der
Heim-VM, Port 8765** — und der Weg dorthin existiert erst, wenn das Relay läuft (Schritt A0b,
siehe §2). Ohne Relay: `connection refused`, und der Fehler sieht aus wie ein Firewall-Problem,
ist aber ein fehlender Listener.

### Befund 2 — Die Health-Route heißt `/health`, nicht `/healthz`

Plan §3.4, Abnahmezeile P9-10 nennt `https://<domain>/healthz`. **Die Route existiert
nicht.** `phase2_mcp/mcpserver/app.py:216` registriert genau eine:
`routes.append(Route("/health", _health, methods=["GET"]))`. Jede Probe in diesem Runbook
läuft gegen `/health`. Plan-Korrektur, datiert 2026-09-29 — die Abnahmezeile P9-10 ist mit
ihrem Pfad-Wortlaut falsch, ihre **Aussage** (200 mit gültigem LE-Zertifikat) bleibt richtig.

### Befund 3 — `ALLOWED_HOSTS` muss die neue Domain bekommen, sonst antwortet alles 400

Caddy reicht den `Host`-Header des Clients unverändert durch. Die Wurzel-App trägt aber eine
`TrustedHostMiddleware` (`phase2_mcp/mcpserver/app.py:214`) mit genau den Hosts aus
`SPACE_ALLOWED_HOSTS`. Steht die neue Domain nicht dort, antwortet **jede** Anfrage über
den VPS mit `400 Invalid host header` — während `/health` lokal weiter 200 liefert.

Das ist keine Theorie, das ist der Live-Incident vom **2026-09-18**: nach der
Tailscale-Account-Migration war `curl -H "Host: <alter-Hostname>"` → `200`, `curl -H "Host:
<neuer-Hostname>"` → `400`, und die Diagnose „Dienst läuft, antwortet aber nicht" wäre
falsch gewesen (`phase3_edge/CLAUDE.md`, Session-Block 2026-09-18).

**Plan §3.2 A7 nennt nur `SPACE_PUBLIC_BASE_URL`. `ALLOWED_HOSTS` fehlt in der Zeile.** Der
Runbook-Schritt A7 unten umfasst beides.

### Befund 4 — V149 ist beantwortet: der `issuer` ist nichts als die Basis-URL, aber die

**Antwort auf V149** (Plan §3.3: welche Felder aus der Basis-URL abgeleitet werden, welche
feststehen): **alle vier, und keines steht fest.**

- `phase4_auth/authserver/config.py:45` — `AuthSettings.issuer` **ist** `base_url`, und
  `base_url` kommt aus `SPACE_PUBLIC_BASE_URL` (`_validate_base_url()` erzwingt `https://`
  und kein `/` am Ende)
- `phase4_auth/authserver/metadata.py:24-29` — `issuer`, `authorization_endpoint`,
  `token_endpoint`, `registration_endpoint` werden alle daraus gebildet
- `AuthSettings.resource` (Z. 49) = `{base_url}/mcp`, ebenfalls abgeleitet
- `allowed_redirect_origins` hat einen eigenen Default (Z. 37) — die Redirect-URIs der
  Claude-Clients liegen auf `claude.ai`/`claude.com` und **ändern sich mit A7 nicht**

**Was daraus folgt, und warum die §3.3-Falle trotzdem real ist:** A7 ist tatsächlich eine
Handvoll Env-Werte. Aber der `iss` ist Teil der **Client-Registrierung** (RFC 9207 — der
`iss` steht in der Authorization-Response, `flows.py:107/161/241`, `routes.py:154`). Die in
beiden Claude-Konten registrierten Clients kennen die alte Adresse. Ein Wechsel ohne
Nachzug der Metadaten sieht deshalb wie ein Auth-Bug aus und ist keiner. **A7 vor A8**, und
A8 erst, wenn `/.well-known/oauth-authorization-server` unter der neuen Domain den neuen
`issuer` liefert.

**Und die gute Nachricht, gemessen:** es gibt **nirgends** im `authserver` eine `iss`-Prüfung
gegen `settings.issuer` beim Einlösen von Tokens — `resolver.py` enthält überhaupt kein `iss`.
Der Wechsel der Basis-URL invalidiert also **keine** bestehende Token-Familie. Es ist kein
Massen-Re-Login zu befürchten; A8 betrifft nur die Connector-Adresse in den Konten.

> **[2026-10-01 Korrektur — der letzte Absatz ist falsch.]** Es gibt keine `iss`-Prüfung, aber
> eine **`resource`-Prüfung**: `phase2_mcp/mcpserver/app.py:196` baut den Resolver mit
> `expected_resource=oauth.settings.resource` (= `{base_url}/mcp`), und
> `phase4_auth/authserver/resolver.py:49` weist jedes Token ab, dessen `record.resource`
> davon abweicht (RFC-8707-Audience-Bindung, S3/S4 aus dem P4-Review). Die Familie speichert
> ihre `resource` (`store.py:387`), neue Tokens aus einem Refresh erben sie. **Folge: in dem
> Moment, in dem `sharefyx-mcp` mit der neuen Basis-URL startet (A7, nicht A8), lehnt `/mcp`
> jedes bestehende Token beider Konten ab** — beide Connectoren sind weg, bis sie neu
> verbunden sind. Ein Übergang „beide Adressen für den Connector" bräuchte eine Änderung in
> `phase4_auth/authserver/` (Tabu-Liste P9 §0.3). **Nikinger-Entscheidung 2026-10-01: harter
> Schnitt auf der Connector-Seite** — A7 und A8 in einer Sitzung, beide Konten verbinden sofort
> neu, kein Tabu-Eingriff.

### Befund 5 — Der Funnel bleibt danach **lesbar, aber nicht beschreibbar**

**[2026-10-05, Nikinger-Entscheidung] Das Fenster ist jetzt unbefristet möglich:**
`LEGACY_UNTIL=open`. Anlass: der Arbeitslaptop erreicht `sharefyx.eurofyx.com` hinter dem
Firmen-VPN (genua genuconnect) nicht. Firefox meldet `NS_ERROR_NET_RESET` mit 0 B; vom MacBook und
von der Heim-VM ist die Adresse einwandfrei erreichbar (DNS, TLS, `303` gemessen). *[Später am selben Tag gemessen: der Laptop hat keinen Direktweg, nur einen Firmen-Proxy, und **der Proxy** setzt die neue Domain zurück; kein SNI-Filter auf einem Direktweg.]* Die erste Vermutung war
ein Filter für neu registrierte Domains (registriert am 2026-10-01); Diagnosebefehle stehen im
Session-Block vom 2026-10-05 im Phase-Head. Die alte Adresse schreibt, **bis** die neue vom
Arbeitslaptop aus belegt funktioniert. Erst dann wird wieder ein Datum gesetzt, und das wird
angekündigt. Der Dialog nennt in diesem Zustand kein Datum.

`phase5_ui/webui/security.py:84` — CSRF prüft `origin != settings.base_url`, **exakt**, ohne
Liste erlaubter Origins. Nach A7 gilt für die Web-UI `settings.base_url == https://<domain>`.
Ein Browser, der die alte Funnel-Adresse aufruft, schickt aber
`Origin: https://…ts.net` → **jeder POST/PATCH/PUT/DELETE wird 403.** GETs laufen
unverändert.

Das ist die Präzisierung, die Abnahmezeile P9-14 braucht („der Funnel-Hostname antwortet
weiterhin"). Richtig ist: **er antwortet, und er liest — Schreibvorgänge sind nach A7 weg.**
Ein echter Dual-Betrieb bräuchte eine zweite erlaubte Origin im Code, und `UiSettings`
(config.py:41) hat genau ein `base_url`-Feld; das wäre eine Codeänderung **außerhalb** von
Step A. **Empfehlung: nicht bauen.** *[2026-10-01: vom Nikinger umentschieden, siehe unten.]* Der Funnel ist der Rückfallweg für den Fall „der VPS
ist weg" — Lesen und ein intakter Connector reichen dafür, und der Schreibpfad läuft nach
A8 über die Domain. Wer es anders will, entscheidet das ausdrücklich; es ist eine
bewusste Mehrorigin-Mechanik, kein Konfigurationsdetail.

> **[2026-10-01 Nikinger-Entscheidung — Übergangsfenster für die Web-UI.]** Es wird gebaut,
> und zwar eng: **genau eine** zusätzliche erlaubte Origin (der alte Funnel-Hostname,
> exakter String) mit einem **Enddatum in der Konfiguration** (Vorschlag zwei Wochen nach A7).
> Bis zum Enddatum kann die alte Adresse lesen und schreiben, danach nur noch lesen (der
> Zustand dieses Befunds). Auf der alten Adresse öffnet sich **bei jedem Laden** ein Dialog im
> Stil des Einstellungen-Dialogs mit dem Verweis auf die neue Adresse — schließbar, kommt beim
> nächsten Laden wieder. **Gilt nur für die Web-UI**; der Connector hat keinen Übergang
> (Korrektur zu Befund 4). Leer/ungesetzt = heutiges Verhalten.
### Befund 6 — `socat` fehlt auf der VM, `tailscale` kann es (1.102.4)

`command -v socat` → nichts. Der Install ist ein Nikinger-Schritt (sudo, eine Zeile, §2 A0b).
`tailscale version` → **1.102.4**, `serve --help` zeigt `--tcp` und `--tls-terminated-tcp`.
Für den gewählten Weg wird die TCP-Fähigkeit **nicht** gebraucht — sie ist nur der Grund,
warum die Alternative nicht am fehlenden Werkzeug scheitern würde.

---

### Befund 7 — die Tailnet-Policy heute (abgeschrieben am 2026-09-30)

Der Nikinger hat die aktive Policy gepostet. Sie ist die **unveränderte Standardvorlage**, und
zwei Stellen darin sind für diesen Step wichtiger als der Grant selbst.

**1. `tagOwners` ist als auskommentierter Block schon vorhanden** — dritter Block von oben,
direkt nach `groups`. Der *Add rule*-Knopf bleibt gesperrt, bis dort ein Tag *besitzt* wird.
Wörtlich so ersetzen (die `//` wegnehmen, den Tag umbenennen, sonst nichts):

```json
	"tagOwners": {
		"tag:sharefyx-edge": ["autogroup:admin"],
	},
```

**2. `nodeAttrs` mit dem `funnel`-Attribut für `autogroup:member` steht in dieser Datei.**
Das ist der Grant aus dem Incident vom 2026-09-18. **Nicht anfassen, nicht wegräumen, nicht
„aufräumen".** Wer die Vorlage zurücksetzt, verliert genau das, woran der öffentliche Funnel
hängt — und die Reparatur kostet eine erneute Freigabe in der Login-Console
(`phase3_edge/CLAUDE.md`, Session-Block 2026-09-18). Ebenso unangetastet: der `ssh`-Block
(Tailscale SSH im *check*-Modus) und der auskommentierte `postures`-Block.

**3. Befund, benannt statt mitgenommen: die Policy erlaubt heute alles.**

```json
"grants": [ {"src": ["*"], "dst": ["*"], "ip": ["*"]} ]
```

Unser Grant ist damit **zusätzlich, nicht einschränkend** — er verändert die aktuelle
Erlaubnis nicht, er dokumentiert nur, welche Erlaubnis der VPS *haben soll*. Für Step A ist das
richtig (die Tailnet-Konfiguration wird nicht nebenbei umgebaut), es heißt aber auch: **solange
die `*`-Regel steht, käme der VPS auch ohne unseren Grant auf alles.** Erst wenn die `*`-Regel
später durch spezifische Regeln ersetzt wird, trägt unser Grant die Erlaubnis. Den Ausbau der
`*`-Regel zu einer echten Liste machen wir **nicht** — das beträft alle sieben Knoten, den
Funnel und den Subnet-Router und ist eine eigene Entscheidung, kein Nebenposten von Step A.
Als Kandidat notiert, nicht gebaut.

**Nebenbei nützlich:** die Vorlage enthält einen auskommentierten `tests`-Block („Test access
rules every time they're saved"). Man kann unseren Test dort dauerhaft eintragen, dann prüft
Tailscale die Regel bei **jedem** Speichern der Policy — statt einmalig über
`Access controls` → `Tests`. Optional, wirkt erst, wenn jemand die Policy anfasst.

### Befund 8 — P9-10 ist bis A7 nicht erfüllbar, und der Grund steht nicht in der Zeile
**gemessen am 2026-10-01, gegen die laufende Instanz**

Abnahmezeile P9-10 verlangt: *`/health` antwortet 200 mit gültigem LE-Zertifikat*. Die
Zertifikats-Hälfte ist eine Caddy-Eigenschaft. Die **200** ist eine Eigenschaft der Anwendung —
und die antwortet für die neue Domain heute `400 Invalid host header`, weil `ALLOWED_HOSTS`
(noch nicht die Domain enthält. Befund 3 hat diese Kopplung richtig beschrieben, aber sie steht
als „A7 gehört dazu" im Plan und damit **hinter** der Abnahme, die A4 prüfen soll.

Belege, beide gegen den laufenden Dienst, nicht aus dem Code gelesen:

```bash
curl -s -o /dev/null -w '%{http_code}\n' http://127.0.0.1:8765/health                      # 200
curl -s -w '\n%{http_code}\n'    -H "Host: sharefyx.eurofyx.com" http://127.0.0.1:8765/health
# Invalid host header
# 400
curl -s -o /dev/null -w '%{http_code}\n' \
     -H "Host: savefyx-vmware-virtual-platform.tail4a8b49.ts.net" http://127.0.0.1:8765/health  # 200
```

Und die **ganze Kette** einmal mit einem echten Caddy davor, statt nur zu schließen: Caddy 2.6.2
(die Version, die das Ubuntu-24.04-Paket liefert) lokal auf einem Wegwerf-Port vor die
Relay-Adresse `100.93.43.122:8765` gestellt, also genau die Strecke, die der VPS in A4 nimmt:

| `Host:` | Antwort |
|---|---|
| `sharefyx.eurofyx.com` | `400` + `Invalid host header` |
| `100.93.43.122` | `400` + `Invalid host header` |
| `savefyx-vmware-virtual-platform.tail4a8b49.ts.net` | `200` + `{"status":"ok","service":"sharefyx-mcp",...}` |

Damit ist beides zugleich belegt: **das Relay funktioniert** (die dritte Zeile geht durch den
socat-Relay durch und kommt von der App), **und Caddy reicht den Host-Header unverändert
durch** — die Behauptung stand vorher nur als „Caddy-Default" im Kommentar.

**Was ich daraus gemacht habe:** P9-10 ist in §3 in **P9-10a** (Zertifikat, in A4) und **P9-10b**
(`200`, nach dem `ALLOWED_HOSTS`-Teil von A7) geteilt, und A4 nennt die `400` als das erwartete
Ergebnis. Das ist die ehrliche Form: „die Abnahme ist noch nicht reif" statt „A4 ist fertig und
etwas stimmt noch nicht".

**Offen, deine Entscheidung (nicht gebaut):** Man kann die `ALLOWED_HOSTS`-Hälfte von A7
**vorziehen** (dort als A7a ausformuliert) — dort passiert **kein** `resource`-Wechsel, also
bleiben beide Connectoren gültig und Fabian ist nicht nötig. Ich habe es nicht entschieden,
weil ein Neustart des Produktionsdiensts deine Sache ist.

### Befund 9 — auf dem VPS ist kein Caddy installiert, und A4 fing trotzdem mit „install" an
**gemessen am 2026-10-01, von der Heim-VM aus**

```
tailscale status  ->  100.121.142.113  ubuntu  tagged-devices  linux  (Online: true, Tags: ['tag:sharefyx-edge'])
curl http://100.121.142.113:80/   -> 000
curl http://100.121.142.113:443/  -> 000
```

`000` heißt: kein Listener. Das ist derselbe Zustand, den der A6-Test am 2026-09-30 als
„443 refused — Paket kommt am Host an, lauscht noch nichts" protokolliert hat, also **kein
Firewall-Problem**, sondern ein fehlendes Programm. Der Schritt A4 im Runbook fing trotzdem mit
`sudo install -m 644 /etc/caddy/Caddyfile` an — ein Befehl, der auf einer Maschine ohne Caddy
mit `No such file or directory` endet und den du dann Zwischenstand meldest. A4 hat jetzt
darum **A4a (installieren)** und **A4b (Konfiguration)**, und **A4a startet mit der Messung**,
ob überhaupt etwas da ist.

Zwei Nebensachen aus derselben Messung, weil sie die Wahl der Quelle bestimmen — beide mit den
Belegen in `Caddyfile.template`: das Paket ist **2.6.2** und legt `/var/log/caddy` im `postinst`
an (das Datei-Log der Vorlage ist damit beschreibbar, `caddy validate` sagt auf dieser Version
`Valid configuration`); und die Paket-Unit hat `ExecReload=… caddy reload … --force`, weshalb
**kein `admin off`** in der Vorlage steht — gemessen bricht `caddy reload` damit in
`dial tcp 127.0.0.1:2019: connection refused` ab.

### Befund 10 — `caddy validate` liest den Adapter aus dem **Dateinamen**
**gemessen am 2026-10-01, mit dem 2.6.2 des Ubuntu-Pakets, gegen die fertige Datei**

Beim Vorprüfen der A4b-Datei stolperte ich über einen Fehler, der aussieht wie eine kaputte
Konfiguration und keine ist:

```
$ caddy validate --config /tmp/opencode/A4b.Caddyfile
Error: decoding config: invalid character '#' looking for beginning of value
```

Die Datei ist **in Ordnung** — dieselbe Datei unter dem Namen `Caddyfile` sagt
`Valid configuration`. Caddy 2.6.2 erkennt die Syntax an einem **Präfix des Basisnamens**,
und zwar case-sensitiv:

| Name | Ergebnis |
|---|---|
| `Caddyfile`, `Caddyfile.fertig`, `Caddyfile.txt`, `Caddyfile.new` | `Valid configuration` |
| `caddyfile` (klein) | JSON-Adapter → `invalid character '#'` |
| `A4b.Caddyfile` | JSON-Adapter → `invalid character '#'` |

**Warum das in eine Härtungsphase gehört und nicht in eine Fußnote:** der Fehlertext sagt
„decoding config" und deutet auf Syntax oder kaputte Klammern. Wer ihn nicht kennt, fängt an,
die Datei zu reparieren — oder schlimmer, ersetzt sie durch eine „einfachere" ohne
Protokoll-Mitschnitt, nur weil die erste Variante sich weigerte. **A4b schreibt deshalb
verbindlich nach `/etc/caddy/Caddyfile`**, und für jeden anderen Dateinamen gilt
`--adapter caddyfile` als Anhängsel.


### A1 — Domain beschaffen (du)

**Beschlossen 2026-09-29: Produktname `sharefyx` + Firmenname `eurofyx`, als Subdomain des
Apex.** Die TLD ist **noch offen** — `eurofyx.de` war bei IONOS nicht verfügbar, angeboten
werden `eurofyx.com` und `eurofyx.{tech,app,cloud}`. **Empfehlung: `.com`**, und zwar aus
einem Grund, den man später nicht mehr hat: die Adresse steht dauerhaft in zwei
Claude-Konten, ein TLD-Wechsel später ist ein DNS-Wechsel **plus** A7/A8 in beiden Konten.
`.tech`/`.app`/`.cloud` altern nicht; `.app` trägt zusätzlich die HSTS-Preload-Pflicht
(unkritisch für uns, wir liefern ohnehin HTTPS, aber ein Detail, das man nicht tragen will).
**Technisch sind alle vier identisch** — Let's Encrypt stellt für jede aus, und die Basis-URL
wird nirgends geparst. `.de` ist damit nicht verloren: ist der Name später frei, ist er
registrierbar; für Firmennamen gibt es bei DENIC zusätzlich einen Nachweisweg über den
Handelsregisterauszug — *das ist ungeprüft, in dieser Umgebung gibt es keinen Netzzugriff*,
also als Möglichkeit genannt, nicht als Zusage.

**Beim Kauf prüfen: automatische Verlängerung einschalten.** Die Domain ist ab hier ein
Single-Point-of-Failure: Läuft sie aus, ist das Projekt weg, weil Connector-Adresse und
Zertifikat daran hängen.

`eurofyx.de` bleibt als Elternteil die richtige Form, weil das Apex für eine spätere
Firmen-Website frei bleibt, ohne dass an Sharefyx etwas angefasst wird.

**Warum nicht `space.eurofyx.de`** (M3 hatte das zuerst vorgeschlagen, aus Kürzegründen — die
Empfehlung ist zurückgenommen): an vier Stellen wird die Adresse als **exakter String**
verglichen (CSRF-Origin `security.py:84`, `TrustedHostMiddleware`, OAuth-`issuer`, Connector in
beiden Konten). Ein Alltagswort wie `space` ist das, was man falsch erinnert
(`spaces.`? `share.`?); `sharefyx` ist ein unverwechselbarer String. **Kürze ist hier nicht
das Kriterium, Wiedererkennbarkeit schon.**

**Gemessen, bevor das beschlossen wurde:** die Basis-URL wird nirgends strukturell zerlegt —
die einzigen `urlsplit`-Aufrufe im Projekt (`clients.py:33`, `routes.py:165`,
`oauth_smoke.py:114`) gelten den Redirect-URIs der *Clients* (`claude.ai/...`), nicht unserer
Adresse. Die einzige Prüfung an `SPACE_PUBLIC_BASE_URL` (`authserver/config.py:85`) verlangt
`https://` vorn, kein `/` hinten, kein `?`, kein `#` — ein dreigliedriger Name erfüllt alle
vier. Vorlage und ACL-Entwurf nehmen den Namen als Platzhalter, an den Dateien ändert sich
kein Byte.

Ziel: eine Domain, deren DNS-Zone du erreichst. Technisch relevant ist nur, dass du die
A-Records selbst setzen kannst (Schritt A5).

- **Stand 2026-09-29: bestellt und bezahlt, Registrierung noch nicht abgeschlossen** — A5 ist bis dahin blockiert, A3 und A0b nicht.
- **[2026-10-01] Registrierung abgeschlossen, `eurofyx.com` bei IONOS** — gemessen über `@1.1.1.1`/`@8.8.8.8`: NS `ns1084.ui-dns.org` u. a. (IONOS-Zone aktiv), Apex zeigt auf IONOS-Parking (`217.160.0.175` + AAAA), **kein** Wildcard, **kein** CAA (Let's Encrypt darf ausstellen), `sharefyx.eurofyx.com` noch ohne Datensatz. IONOS-Hinweise „nicht genutzt"/„SSL aktivieren" **ignorieren**: Apex bleibt frei, das Zertifikat holt Caddy (A4).
- Kauf `eurofyx.<tld>`. **Ausreichend ist jede normale Registrar-Oberfläche.** Praktisch ist
  derselbe Anbieter wie beim VPS: dann pflegst du den A-Record im selben Panel, in dem auch
  der VPS liegt. Ein Konto, eine Rechnung.
- **Ausgabe lesen:** welche Zone, welcher Registrar, ist `eurofyx.de` frei?

*Zur Form:* eine Subdomain genügt, eine Apex-Domain nicht — Letzteres ist hier entschieden
(siehe oben), weil das Apex für eine Firmen-Website frei bleiben soll.


### A2 — VPS beschaffen (du)

Ziel: eine Kiste mit **1 vCPU / 2 GB RAM**. Der Reverse-Proxy rechnet nichts — er
terminiert TLS und leitet weiter. Mehr kostet Geld ohne Gegenwert.

- **Ausgabe lesen:** Provider, Region, IPv4-Adresse, fertig?
- Danach: die öffentliche IPv4 notieren, sie braucht A5.


### A3 — VPS ins Tailnet, als getaggter Node (du, ACL-Entwurf von mir)

Ziel: der VPS ist im selben Tailnet und darf **genau einen** Port auf **genau einer**
Adresse erreichen.

Auf dem VPS:

```bash
curl -fsSL https://tailscale.com/install.sh | sh     # Nikinger, sudo
sudo tailscale up --advertise-tags=tag:sharefyx-edge
```

**Reihenfolge: erst die Policy, dann der Beitritt** — ohne `tagOwners` nimmt Tailscale das `--advertise-tags` nicht an, der Tag existiert dann nicht. Die Datei ist ein **Fragment**, kein Ersatz: die beiden `_`-Schlüssel (`_MERGE_HINWEIS`, `_WARUM`) sind Kommentar und gehören **nicht** ins Policy-File.

**Wo genau** (aus dem Screenshot vom 2026-09-30 belegt, nicht aus dem Gedächtnis): in der
linken Leiste **`Access controls` → `Policies`**. Das ist der Policy-Editor.

> **Die Verwechslungsfalle in dieser Console:** `Settings` → `Policy file management` klingt
> noch passender, ist aber die **Versionshistorie** (sehen, zurückrollen) — dort kannst du
> nichts sinnvoll editieren. Direktlink, falls du die Leiste nicht brauchst:
> `console.tailscale.com/admin/acls`

**Prüfwerkzeug, das direkt daneben liegt — benutze es.** `Access controls` → **`Tests`** ist
der ACL-Testharness der Tailnet-Policy: Quelle, erlaubtes Ziel, verweigertes Ziel eingeben,
die Console wertet gegen die *aktuelle* Policy aus. Trage dort ein:

```
source:        tag:sharefyx-edge
accept:        100.93.43.122:8765
deny:          (leer)
```

Erwartet: **accepted**. Das ist ein Nachweis, den `tailscale ping` dir *nicht* liefert (siehe
unten) — und er kostet keine Runde.

> **Belegt am Screenshot vom 2026-09-30, nicht aus dem Gedächtnis: diese Console baut
> `grants`, nicht `acls`.** Auf der Seite *Add rule* heißt der Knopf **„Save grant"**, die
> Live-Vorschau zeigt `{"ip": ["*:*"]}`, und das Formular hat *Source / Destination / Port and
> protocol*. Die klassische `acls`-Form geht auch, aber die GUI erzeugt sie nicht — sie
> auszutippen wäre Arbeit ohne Gegenwert. **Angekommen war zuerst die `acls`-Form; sie ist
> hiermit ersetzt, samt Test und ACL-Entwurf im Repo.**


### Feld für Feld im Formular „Add rule"

| Feld | Eingabe | Warum genau das |
|---|---|---|
| **Source** | `tag:sharefyx-edge` | **Hier stand am 2026-09-30 rot `tag not found` und der Knopf *Save grant* war deaktiviert** — der Tag existierte noch nicht. Das ist der erwartete erste Stolperstein, kein Fehler in der Eingabe. **Auflösung:** links `JSON editor`, dort `tagOwners` ergänzen (siehe unten), speichern, zurück zu *Add rule*. |
| **Destination** | `100.93.43.122` — oder aus der Liste das **Gerät** `savefyx-vmware-virtual-platform` | Beides gültig. Das Gerät ist lesbarer und überlebt eine IP-Änderung; der Entwurf im Repo nennt bewusst die IP, damit die Regel beim Merge nicht versehentlich auf ein anderes Gerät zeigt. |
| **Port and protocol** | **`tcp:8765` — unbedingt ändern!** | Steht dort unverändert *„All ports and protocols"*, steht in der Vorschau `{"ip": ["*:*"]}` und die Regel erlaubt **alles**. Das ist das eine Feld, bei dem ein Klick den Unterschied macht. |
| **Note** | `P9 Step A: TLS-Terminator darf nur den Sharefyx-Port der Heim-VM` | Optional, aber das Feld ist genau dafür da, und in einem Jahr weiß sonst niemand mehr, warum es die Regel gibt. |
| **Source posture / Via / App / Capability** | **leer lassen** | Nichts davon wird für diesen Weg gebraucht. |
| **JSON preview** | muss zeigen: `"ip": ["tcp:8765"]` | **Das ist die Abnahme — vor dem Speichern, nicht danach.** |
| → **Save grant** | | |

**Der `tagOwners`-Eintrag, wörtlich** (im `JSON editor`, **direkt nach der öffnenden Klammer**
einsetzen — dort braucht es kein Komma am Ende, das ist der fehlerfreie Ort):

```json
{
  "tagOwners": {
    "tag:sharefyx-edge": ["autogroup:admin"]
  },
  … deine bestehenden Schlüssel …
}
```

`autogroup:admin` = alle Admins dieses Tailnets. **Kein Komma nach der schließenden Klammer
von `tagOwners`** — nur zwischen den Schlüsseln. (Am Screenshot vom 2026-09-30 ist zu sehen,
dass die Console das *Note*-Feld selbst als `//`-Kommentar über das Objekt schreibt: in der
Policy-Datei sind Kommentare also erlaubt. Die `_`-Schlüssel aus `tailscale-acl.draft.json`
sind dagegen **echte JSON-Schlüssel** und gehören nicht in die Policy-Datei.)

Was `tagOwners` ist und wofür: der Tag muss einen *Besitzer* haben, sonst lehnt Tailscale
`--advertise-tags` beim Beitritt ab. `autogroup:admin` heißt „alle Admins dieses Tailnets".

- **Ausgabe lesen:** `tailscale status` vom VPS zeigt die Tailnet-IP des VPS.
- **`tailscale ping 100.93.43.122` ist ausdrücklich KEIN Nachweis** — weder für die Erreichbar-
  keit noch für die ACL-Regel. Der Befehl prüft den WireGuard-Pfad zwischen zwei `tailscaled`,
  nicht die Datenebene, auf der die ACL greift; er kann grün sein, während die Regel fehlt.
  **[Korrektur vom 2026-09-30: diese Erwartung stand hier vorher als „antwortet noch nicht"
  — das war geraten.]** Der echte Nachweis ist eine **TCP-Verbindung auf Port 8765** und der
  ist bis A0b nicht möglich. Bis dahin gilt: `status` zeigt die Node, mehr nicht.


### A0b — socat + Relay auf der Heim-VM (du; Unit liegt im Repo)

Ziel: Befund 1 auflösen. Das ist der Schritt, ohne den A4 nicht geht.

```bash
# auf der HEIM-VM (dieser Repo-Checkout), nicht auf dem VPS
sudo apt install socat
sudo install -m 0644 phase3_edge/systemd/sharefyx-tail-proxy.service /etc/systemd/system/
sudo systemctl daemon-reload
sudo systemctl enable --now sharefyx-tail-proxy.service
```

**Warum `install -m 0644` und nicht `install_units.sh`:** die Unit hat bewusst **keinen**
`__REPO_ROOT__`-Platzhalter im `ExecStart` (sie zeigt auf `/usr/bin/socat`). Genau damit ist
die Kopplung ausgeschlossen, die beim Watchdog zum Befund wurde — dort zeigte `ExecStart`
auf ein Release, das die Datei nicht enthält (Session-Block 2026-09-28). `install_units.sh`
wird hier **nicht** angefasst: das ist P3-Code, und dieser Commit bleibt additiv.

- **Ausgabe lesen:**
  ```bash
  ss -ltnp | grep 8765          # jetzt ZWEI Zeilen: 127.0.0.1:8765 und 100.93.43.122:8765
  systemctl is-active sharefyx-tail-proxy
  ```
  Fehlt die zweite Zeile, ist der Schritt nicht fertig. Bitte die **beiden** Zeilen schicken,
  nicht nur „active".
- **Der wahrscheinlichste Fehlschlag, falls die zweite Zeile fehlt:** `bind=` auf eine Adresse,
  die es beim Start noch nicht gab. Die Unit startet nach `tailscaled.service`, aber ein
  frisch gebootetes `tailscale0` kann einen Moment später kommen — `Restart=on-failure` mit
  5 s fängt das ab, es ist also kein dauerhafter Zustand. `systemctl status
  sharefyx-tail-proxy` zeigt dann `bind: Cannot assign requested address`. In dem Fall: fünf
  Sekunden warten, Status erneut. Bleibt es rot, ist es ein anderer Fehler — dann die
  Ausgabe schicken, nicht die Direktive entfernen.


### A4 — Caddy auf dem VPS (Konfiguration von mir, sudo von dir) — **✅ 2026-10-01 erledigt**

Ziel: TLS-Terminierung für die eigene Domain, Weiterleitung über das Tailnet. **Ab 2026-10-01
zwei Hälften** — vorher fehlte der Install-Schritt und der Schritt wäre mit einem
`No such file or directory` geendet (Befund 9).

> **✅ Ergebnis, alle drei Ausgaben wie erwartet:**
>
> | Ausgabe | Ergebnis |
> |---|---|
> | `caddy validate` | `Valid configuration` (die `WARN … not formatted`-Zeile ist die bekannte kosmetische, siehe Befund 9) |
> | `journalctl -u caddy` | `validations succeeded; finalizing order` → **`certificate obtained successfully`**, HTTP-01 in 6 s, Let's-Encrypt-`YE1` |
> | `https://sharefyx.eurofyx.com/health` | **`Invalid host header` + `400`** — Befund 8, das richtige Ergebnis |
> | `openssl s_client … -noout -subject -issuer -dates` | `subject=/CN=sharefyx.eurofyx.com`, `issuer=/C=US/O=Let's Encrypt/CN=YE1`, gültig 01.10.–30.12.2026 |
>
> **Der vierte Beleg, den es vorher nicht gab:** auf der **Heim-VM** steht zur selben Sekunde
> `19:30:49 GET /health status=400 ua=curl/8.7.1`, 0 ms. Der `400` kam also **aus der
> Anwendung**, nicht aus Caddy — das ist der Beweis, dass der Weg
> VPS → WireGuard → socat-Relay `100.93.43.122:8765` → App steht. Ein `502` oder
> `connection refused` wäre der Fehlerfall gewesen.
>
> **Zwei Nebenbefunde aus dem Journal, benannt statt wegesehen:**
>
> 1. `WARN tls: stapling OCSP … no OCSP server specified` — harmlos und erwartbar. Caddy will
>    OCSP stapeln und findet für diese Kette keinen Responder; der Zertifikatseintrag selbst
>    ist unberührt (der TLS-Handshake lief sauber, der Browser hat die Kette akzeptiert). Kein
>    Handlungsbedarf, aber wer das beim nächsten Mal sieht, soll es nicht für einen Fehler halten.
> 2. In denselben 30 Minuten stehen **19 Scan-Requests** (`ua=l9scan`, leakix.net) auf der alten
>    Funnel-Adresse — alle `400`, weil `TrustedHostMiddleware` fremde Hosts abweist. Vorbestehend,
>    durch die neue Domain weder besser noch schlechter: die Scanner kennen `sharefyx.eurofyx.com`
>    erst, seit der A-Record steht.
>
> **✅ 2026-10-01, später: der ACME-Platzhalter ist raus.** `read -rp` + `sed` hat die echte
> Adresse des Nikingers gesetzt (Zeile 21), `caddy validate` sagt wieder `Valid configuration`,
> `systemctl reload caddy` ohne Fehler — und der Erfolgsbeleg ist der, den es vorher nicht
> geben konnte: **`notBefore` ist unverändert** (`Oct  1 18:31:33 2026 GMT`). Genau das war
> vorhergesagt: die `email` gehört zum ACME-*Konto*, nicht zum Zertifikat, es wird nichts neu
> ausgestellt und erst die nächste Renewal-Runde legt ein Konto mit der richtigen Adresse an.
> **Die Adresse steht bewusst nicht in diesem Repo** — sie ist eine private, und der Ort für
> sie ist `/etc/caddy/Caddyfile` plus dein Postfach, nicht eine Doku, die jeder mit Lesezugriff
> auf das Repo sieht.
>
> **Ein Platzhalter war live geworden:** die ACME-Adresse stand als `deine@adresse.de` in
> `/etc/caddy/Caddyfile` — mein Beispielwert aus der Vorlage, von der `sed`-Zeile wörtlich
> übernommen. Funktionell folgenlos (Let's Encrypt prüft die Adresse nicht, es gehen nur keine
> Ablauf-Hinweise dorthin), in einer Härtungsphase aber eine falsche Angabe in einer
> Betriebsdatei. (Erledigt, siehe oben — der Text bleibt als Beleg, wie der Fehler aussah.)
>
> ```bash
> sudo sed -i 's/deine@adresse.de/DEINE@ADRESSE/' /etc/caddy/Caddyfile
> sudo systemctl reload caddy        # ExecReload der Paket-Unit; deshalb kein `admin off`
> ```

#### A4a — erst messen, dann installieren

> **✅ 2026-10-01: A4a erledigt.** `command -v caddy` → `kein Caddy` (Befund 9 bestätigt),
> `apt install -y caddy` → **`2.6.2`**, also genau die Version, gegen die die Vorlage validiert
> ist. Nebenbei: `libnss3-tools` kam als Abhängigkeit mit, der Paket-Neustart hat
> `systemd-logind` vertagt (beides folgenlos).

```bash
# auf dem VPS (SSH übers Tailnet: ssh -i <key> root@100.121.142.113)
command -v caddy && caddy version || echo "kein Caddy — Installation folgt"
```

**Erwartet: `kein Caddy` (Befund 9, gemessen am 2026-10-01: nichts lauscht auf 80/443).**
Kommt eine Version, ist A4a erledigt und wir gehen zu A4b — dann bitte die Version mitschicken,
weil die Vorlage gegen **2.6.2** validiert ist.

Installation, falls `kein Caddy`:

```bash
sudo apt update
sudo apt install -y caddy
caddy version          # nicht sudo: /usr/bin/caddy ist world-readable
```

**Erwartet: `2.6.2`** (das Ubuntu-24.04-Paket, `apt-cache policy caddy` am 2026-10-01). Der
`apt install` legt gleichzeitig die Unit an, den Nutzer `caddy` und `/var/log/caddy` (im
`postinst`, deshalb ist das Datei-Log der Vorlage beschreibbar) — **und ein Default-Caddyfile mit
einem `:80`-Block**, das A4b ersetzt.

#### A4b — Konfiguration und Neustart

```bash
# 1. Die drei Platzhalter ersetzen — auf dem VPS, nicht im Repo (die Datei bleibt Vorlage):
#      <domain>         -> sharefyx.eurofyx.com
#      <heimvm-tailnet> -> 100.93.43.122          (die HEIM-VM, nicht der VPS)
#      <kontakt>        -> deine E-Mail-Adresse
#    z. B. mit sed auf eine Kopie, dann nach /etc/caddy/Caddyfile:
sudo install -d -m 755 /etc/caddy
sudo install -m 644 /tmp/Caddyfile.sub /etc/caddy/Caddyfile
sudo caddy validate --config /etc/caddy/Caddyfile     # <- die Prüfung, die A4 gerettet hat
sudo systemctl restart caddy
```

**`<heimvm-tailnet>` ist die Falle in diesem Schritt** (2026-10-01 korrigiert: der Platzhalter
hieß vorher `<vps-tailnet>` und war als Node-Name *des VPS* beschrieben). Der VPS heißt
`ubuntu`, `100.121.142.113`. Trägt der VPS sich selbst als Ziel ein, sieht der Fehler aus wie
ein totes Relay — `connection refused` auf dem VPS statt „Ziel falsch".

**Warum `validate` vor `restart`:** ein Tippfehler wird sonst erst beim Neustart sichtbar —
und dann ist der Dienst weg, der vorher lief (die Paket-Unit startet Caddy als `User=caddy`).

- **Ausgabe lesen — drei getrennte Dinge, alle drei zählen:**

  1. `caddy version` → `2.6.2` (oder höher)
  2. `sudo journalctl -u caddy -n 40 --no-pager` → **die ACME-Zeile.** Erwartet etwas wie
     `certificate obtained successfully` / `serving initial configuration` **ohne** Fehler und
     ohne mehrfaches `retrying`. Ein Zertifikatsfehler heißt fast immer: Port 80 nicht
     erreichbar oder DNS zeigt noch nicht auf den VPS. Port 80/443 sind bei A6 offen, DNS steht
     seit A5 — wenn es trotzdem scheitert, ist die Zeile selbst das Ergebnis, nicht „ok".
  3. **Von einem Gerät ohne VPN:**
     ```bash
     curl -s -o /dev/null -w '%{http_code}\n' https://sharefyx.eurofyx.com/health
     openssl s_client -connect sharefyx.eurofyx.com:443 -servername sharefyx.eurofyx.com </dev/null 2>/dev/null \
       | openssl x509 -noout -subject -issuer -dates
     ```
     **Erwartet: `400` mit Rumpf `Invalid host header`, und ein LE-Zertifikat auf
     `subject=CN = sharefyx.eurofyx.com`.** Das ist **kein Fehlschlag**, sondern Befund 8: TLS
     steht, die Anwendung kennt die Domain noch nicht. Ein `000` oder ein
     `unable to get local issuer certificate` bedeutet dagegen: A4 ist nicht fertig — dann
     kommst du mit der Journalzeile zurück, nicht mit „geht nicht".


### A5 — DNS auf den VPS (du)

> **✅ 2026-10-01:** A-Record `sharefyx` → `217.160.128.146` bei IONOS gesetzt. Gegenprobe vom
> Mac ohne VPN: `dig +short sharefyx.eurofyx.com @1.1.1.1` → `217.160.128.146`. **Die Domain
> ist `sharefyx.eurofyx.com`.**

**Ziel-IP steht fest: `217.160.128.146`** (vom Nikinger am 2026-09-29 genannt, gegen die
tatsächliche Erreichbarkeit geprüft: öffentlich routbar, nicht privat, nicht im
Tailscale-Bereich `100.64.0.0/10`; Port 22 antwortet, der Server läuft).

Sobald die Zone existiert, **genau ein** Datensatz:

| Feld | Wert |
|---|---|
| Typ | `A` |
| Name/Host | `sharefyx` |
| Wert | `217.160.128.146` |
| TTL | Standard / 3600 |

**Kein `AAAA`.** IONOS schreibt dir eine IPv6 hin, die ist aber ein **separater** Datensatz
und bleibt leer. Zwei Adressen für einen Namen sind zwei Fehlerbilder, und die eine
Fehlersuche, die wir bei DNS nicht brauchen, ist die mit der zweiten. Kommt eine IPv6
später zurück, ist das ein eigener, bewusster Schritt.

**Kein CNAME auf `*.ts.net`** — das ist Lock P9-E und der Grund, warum der Plan diesen Weg
verworfen hat (Tailscale Funnel bedient nur Namen in der Tailnet-Domain; ein CNAME darauf
erzeugt einen TLS-Namens-Mismatch, weil Funnel per SNI an die Node durchreicht und diese ein
`*.ts.net`-Zertifikat präsentiert).

- **Ausgabe lesen:** von einem Gerät **ohne** VPN die IP auflösen lassen und die Ausgabe
  schicken. Auf der sharefyx-VM selbst löst MagicDNS auf — das ist als Prüfung wertlos. Der
  Auflösungsbefehl, mit dem wir in der nächsten Runde prüfen:
  `dig +short sharefyx.<deine-tld> @1.1.1.1`
  Erwartet: exakt `217.160.128.146`.
- **Was dieser A-Record öffentlich macht:** die IP steht ab dann in jedem öffentlichen
  Resolver. Das ist gewollt — es ist eine öffentliche Adresse. Kein Geheimnis (Hard Rule 1
  betrifft Tokens und Schlüssel, keine ohnehin auflösbaren IPs).


### A6 — Firewall am VPS (du; Entwurf von mir)

Ziel: 80/443 offen, alles andere zu, SSH **nur** über das Tailnet.

> **[Korrektur 2026-09-30, BEVOR der Schritt lief: meine erste Fassung dieses Schritts war
> fehlerhaft und hätte dich ausgesperrt.]** `ufw default deny incoming` gilt **auf allen
> Interfaces** — auch auf `tailscale0`. Die erste Fassung erlaubte 80/443, aber **kein SSH
> über das Tailnet**; wer zu dem Zeitpunkt über die Tailnet-IP verbunden ist, verliert die
> Verbindung, und wer über die öffentliche IP verbunden ist, verliert sie auch. Zurück kommt
> man nur über die IONOS-Webconsole. Die Regel für `tailscale0` fehlt in der ersten Fassung
> vollständig — sie ist unten ergänzt.

```bash
sudo ufw default deny incoming
sudo ufw default allow outgoing
sudo ufw allow in on tailscale0 to any port 22 proto tcp comment "SSH nur ueber Tailscale"
sudo ufw allow 80/tcp comment "ACME + HTTP -> HTTPS"
sudo ufw allow 443/tcp comment "HTTPS"
sudo ufw enable
sudo ufw status verbose
```

- **Ausgabe lesen:** die Statusausgabe. Erwartet: 80/443 offen, 22 **mit der
  `tailscale0`-Beschränkung** offen, sonst nichts.
- **Gegenprobe, in dieser Reihenfolge** (nicht im Terminal des VPS):
  1. **Erst** die Tailnet-Verbindung prüfen: `ssh root@100.121.142.113` von einem Gerät im
     Tailnet. **Muss gehen.** Scheitert sie, ist die `tailscale0`-Regel falsch oder
     fehlend — dann **nicht** `ufw disable` als Krücke, sondern die Regel prüfen.
  2. **Dann** die öffentliche IP: `ssh root@217.160.128.146` von einem Gerät **ohne** VPN
     muss **scheitern**. „connection refused" und „timeout" sind beide ein Fehlschlag, aber
     aus unterschiedlichen Gründen, und der Unterschied ist die Diagnose.
- **Reihenfolge innerhalb des Schritts:** `ufw enable` erst, **nachdem** alle vier Regeln
  stehen. `ufw enable` bei leerer Regeliste ist genau der Fehler, aus dem man nur mit
  Webconsole zurückkommt.


### A7 — Die Heim-VM auf die neue Adresse stellen (du, sudo; Liste von mir)

Ziel: `SPACE_PUBLIC_BASE_URL` und `ALLOWED_HOSTS` auf die neue Domain. **Befund 3 und 4.**

> **[2026-10-01] Der `restart` in diesem Schritt kappt beide Connectoren** (Korrektur zu
> Befund 4). Den Restart deshalb nur ansetzen, wenn **Fabian zeitgleich** A8 machen kann —
> A7 und A8 sind ab jetzt eine Sitzung, kein Abend dazwischen.

> **[2026-10-01, Vorschlag, wartet auf deine Anordnung — Befund 8] `ALLOWED_HOSTS` lässt sich
> als eigene Hälfte vorziehen** (`A7a`), weil dort **kein** `resource`-Wechsel passiert:
>
> ```bash
> # in phase3_edge/local.env: ALLOWED_HOSTS=sharefyx.eurofyx.com,savefyx-vmware-virtual-platform.tail4a8b49.ts.net,127.0.0.1
> sudo phase3_edge/scripts/install_units.sh
> sudo systemctl restart sharefyx-mcp
> curl -s -o /dev/null -w '%{http_code}\n' -H "Host: sharefyx.eurofyx.com" http://127.0.0.1:8765/health
> ```
>
> Erwartet: `200`. Danach ist P9-10b grün und der ganze öffentliche Weg (TLS, Zertifikat,
> Health) steht **vor** A7 — A7/A8 bleiben dann der einzige Schnitt mit Token-Folge.
> Gegenprobe, dass die alte Adresse dadurch nicht verloren geht: derselbe Befehl mit
> `-H "Host: savefyx-...ts.net"` → weiterhin `200`. **Nicht gebaut**: ein Neustart des
> Produktionsdiensts ist deine Sache, und ein `install_units.sh` ohne Not ist der Moment, in
> dem aus einem Kalibrier-Schritt ein Betriebsereignis wird.
>
> **✅ AUSGEFÜHRT 2026-10-03, 12:59 Uhr** — der Vorschlag ist damit entschieden und erledigt, in
> genau dieser Reihenfolge (A7a, dann A7, dann A8 am selben Tag). **Die Ausgabe, die kam:**
> `install_units.sh` erzeugt **zehn** Units (nicht fünf bis sechs — die Vorhersage in der Übergabe
> war zu niedrig, es waren nur die *Maße* falsch, nicht der Ablauf), alle vier Timer danach
> `enabled` **und** `active`, `tailscaled-watchdog` mit einem echten Takt `healthy: Self.Online=true`
> (der Takt ist der Beweis, nicht der laufende Timer — Lehre vom 2026-10-01). **Neu dabei:** die
> Unit trägt jetzt `SPACE_UI_LEGACY_ORIGIN=` / `_UNTIL=` **leer**, weil `local.env` noch keine
> `LEGACY_*`-Zeilen hatte; leer **beide** heißt laut `config.py:44` ausdrücklich *kein Fenster* und
> ist kein halbes Fenster, also kein Startfehler. **Gegenprobe, die A7a von A7 trennt:** der
> `issuer` stand nach A7a unverändert auf der alten Adresse — damit ist belegt, dass der Vorlauf
> den `resource` nicht angefasst hat.

**✅ AUSGEFÜHRT 2026-10-03, 13:05 Uhr** (A7, der Schnitt — `issuer` und alle drei Endpunkte zeigen
auf die neue Domain, App-Start ohne Traceback, beide Adressen extern 200 mit gültigem TLS).
**Der Ist-Zustand von `local.env` steht hier, weil die Datei git-ignoriert ist und ein
Neustart sie nicht zurücksetzt** — wer sie nicht im Repo findet, findet sie hier:

```
ALLOWED_HOSTS=sharefyx.eurofyx.com,savefyx-vmware-virtual-platform.tail4a8b49.ts.net,127.0.0.1
PUBLIC_BASE_URL=https://sharefyx.eurofyx.com
LEGACY_ORIGIN=https://savefyx-vmware-virtual-platform.tail4a8b49.ts.net
LEGACY_UNTIL=2026-10-17
```

Vor dem Lauf in `phase3_edge/local.env` (git-ignoriert, die einzige echte Konfigurationsquelle —
die beiden folgenden Blöcke sind die **Zielwerte**, und seit dem 2026-10-03 der **Ist-Zustand**):

```
PUBLIC_BASE_URL=https://<domain>
ALLOWED_HOSTS=<domain>,savefyx-vmware-virtual-platform.tail4a8b49.ts.net,127.0.0.1
LEGACY_ORIGIN=https://savefyx-vmware-virtual-platform.tail4a8b49.ts.net
LEGACY_UNTIL=<A7-Datum + 14 Tage, JJJJ-MM-TT>
```

**[2026-10-01] `LEGACY_*` = das UI-Übergangsfenster** (Befund 5, umentschieden): die alte Adresse
schreibt bis einschließlich `LEGACY_UNTIL` (Europe/Berlin), danach liest sie nur; Warndialog bei
jedem Laden. Wirkt **nur, wenn der Code vor A7 deployt ist** — ~~der Live-Release ist vom 2026-09-18~~
**[2026-10-03: Bedingung erfüllt]** der Live-Release ist `v3.1.0` vom 2026-10-02, das
Übergangsfenster ist also **live**, und A7 hat es scharf geschaltet. Gemessen: das Fenster öffnet
die Schreibpfade der alten Adresse **heute und am letzten Tag (2026-10-17, `clock() <= legacy_until`,
`config.py:76`) und schließt am 2026-10-18 von selbst** — `clock` ist pro Request, der Dienst muss
dafür **nicht** neu gestartet werden (genau dafür ist es ein `Callable`, kein Flag).
Ein Tippfehler in den zwei Zeilen ist ein Startfehler (fail-closed), kein stilles „aus".

Drei Punkte, die dabei nicht verloren gehen dürfen:

1. **`ALLOWED_HOSTS` braucht die neue Domain UND den alten Funnel-Hostnamen UND
   `127.0.0.1`.** Ohne `127.0.0.1` bricht jede lokale Prüfung mit 400 (Befund S1 aus P4). Ohne
   den Funnel-Host antwortet der Rückfallweg mit 400, obwohl P9-14 ihn noch verlangt.
2. `PUBLIC_BASE_URL` **ohne** `/` am Ende und mit `https://` — beides wird beim Start
   validiert, ein Verstoß ist ein Startfehler, kein stiller Fallback.
3. Nach `install_units.sh` ist ein **`systemctl restart sharefyx-mcp` zwingend** — das Skript
   restart't einen laufenden Dienst nicht (Live-Befund 2026-09-18, `phase3_edge/CLAUDE.md`).
   „installiert und gestartet" in der Skriptausgabe bedeutet nicht „mit neuer Konfiguration
   aktiv".

```bash
sudo phase3_edge/scripts/install_units.sh
sudo systemctl restart sharefyx-mcp
```

- **Ausgabe lesen:** beide Befehle, dann die Gegenprobe, die den Unterschied sichtbar macht:
  ```bash
  curl -s -o /dev/null -w '%{http_code}\n' -H "Host: <domain>"               http://127.0.0.1:8765/health
  curl -s -o /dev/null -w '%{http_code}\n' -H "Host: savefyx-vmware-virtual-platform.tail4a8b49.ts.net" http://127.0.0.1:8765/health
  ```
  Erwartet: `200` und `200`. Kommt `400`, ist `ALLOWED_HOSTS` nicht durch (Befund 3).
- **Und der eigentliche Wirkungsnachweis:**
  ```bash
  curl -s https://<domain>/.well-known/oauth-authorization-server | head -c 200
  ```
  Erwartet: `"issuer": "https://<domain>"` — das ist die Bedingung, unter der A8 passieren darf.
