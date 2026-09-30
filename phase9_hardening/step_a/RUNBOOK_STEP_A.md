---
status: live
purpose: Step A (P9) — gefuehrter Ablauf A1–A9 fuer die eigene Domain ueber einen VPS als TLS-Terminator; traegt die sechs gemessenen Befunde, die den Plan korrigiert haben, und den nummerierten Rueckfall auf den Funnel
read-when: der Nikinger einen der Schritte A1–A9 ausfuehren will, oder jemand fragt, warum A4 nicht so gebaut ist, wie der Plan §3.2 es sagt
detail: L2
up: ../CLAUDE.md
down:
  - ../../docs/concepts/phase9_hardening_plan.md   # §3 Step A, Locks P9-C/D/E, Abnahme P9-10..P9-15
  - ./Caddyfile.template                          # VPS-Konfiguration (A4)
  - ./tailscale-acl.draft.json                    # ACL-Entwurf (A3), Fragment zum Merge
  - ../../phase3_edge/systemd/sharefyx-tail-proxy.service  # der Relay, ohne den A4 nicht geht
---

[2026-09-29, beim Durchgehen von A3 gefunden: die ACL-Anweisung zeigte nur den `acls`-Block, nicht `tagOwners` — ohne den lehnt Tailscale `--advertise-tags` beim Beitritt ab. Reihenfolge „erst Policy, dann Beitritt" jetzt explizit, beides im Code-Block.] 
# Step A — Echte Domain über einen eigenen VPS

**Form: Coarbeit (P9-Q, Plan §0.5.1).** M3 leitet an, der Nikinger führt aus und liefert
jede echte Ausgabe zurück. **Ein Schritt pro Runde.** Diese Datei ist der vollständige
Ablauf, aber sie ist **keine Blockliste zum Abhaken**: bei DNS, Zertifikaten und
Reverse-Proxys hängt jeder Schritt an der Ausgabe des vorherigen. Die Runde startet mit A1.

**Hard Rule 6 gilt unverändert.** Die Heim-VM öffnet keinen Port am Router; sie baut nur
eine ausgehende Tailscale-Verbindung auf. Was hier gebaut wird, ist ein Terminator, den der
Nikinger selbst betreibt — der Unterschied zu Cloudflare Tunnel (P9-D, ausgeschlossen) ist
nicht „niemand sieht es", sondern „der, der es sieht, bist du".

---

## §0 Sechs Befunde, die vor A1 gemessen wurden

Diese sechs sind **kein Vorwand, nichts zu tun** — jeder davon ist entweder eine
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

### Befund 5 — Der Funnel bleibt danach **lesbar, aber nicht beschreibbar**

`phase5_ui/webui/security.py:84` — CSRF prüft `origin != settings.base_url`, **exakt**, ohne
Liste erlaubter Origins. Nach A7 gilt für die Web-UI `settings.base_url == https://<domain>`.
Ein Browser, der die alte Funnel-Adresse aufruft, schickt aber
`Origin: https://…ts.net` → **jeder POST/PATCH/PUT/DELETE wird 403.** GETs laufen
unverändert.

Das ist die Präzisierung, die Abnahmezeile P9-14 braucht („der Funnel-Hostname antwortet
weiterhin"). Richtig ist: **er antwortet, und er liest — Schreibvorgänge sind nach A7 weg.**
Ein echter Dual-Betrieb bräuchte eine zweite erlaubte Origin im Code, und `UiSettings`
(config.py:41) hat genau ein `base_url`-Feld; das wäre eine Codeänderung **außerhalb** von
Step A. **Empfehlung: nicht bauen.** Der Funnel ist der Rückfallweg für den Fall „der VPS
ist weg" — Lesen und ein intakter Connector reichen dafür, und der Schreibpfad läuft nach
A8 über die Domain. Wer es anders will, entscheidet das ausdrücklich; es ist eine
bewusste Mehrorigin-Mechanik, kein Konfigurationsdetail.

### Befund 6 — `socat` fehlt auf der VM, `tailscale` kann es (1.102.4)

`command -v socat` → nichts. Der Install ist ein Nikinger-Schritt (sudo, eine Zeile, §2 A0b).
`tailscale version` → **1.102.4**, `serve --help` zeigt `--tcp` und `--tls-terminated-tcp`.
Für den gewählten Weg wird die TCP-Fähigkeit **nicht** gebraucht — sie ist nur der Grund,
warum die Alternative nicht am fehlenden Werkzeug scheitern würde.

---

## §1 Was in dieser Runde passiert und was nicht

| | |
|---|---|
| **Gebaut (dieser Commit)** | das Relay-Unit, die Caddyfile-Vorlage, der ACL-Entwurf, dieses Runbook, ein Wächter-Test |
| **Nicht gebaut, mit Absicht** | kein `install_units.sh`-Eingriff, kein Code-Touch an `phase4_auth/`, kein Dual-Origin-Mechanismus, keine Änderung an `SPACE_HOST` |
| **Deine Schritte** | A1 Domain · A2 VPS · A3 Tailscale+ACL · A0b socat+Relay · A4 Caddy · A5 DNS · A7 Basis-URL · A8 Connector · die Abnahme P9-10–P9-15 |
| **Reihenfolge nicht frei** | A0b vor A4 · A5 vor der Zertifikatsprüfung · **A7 vor A8** · A8 vor P9-13 |

**Warum das Relay-Unit in `phase3_edge/` liegt und nicht in `phase9_hardening/`:** dort
liegen schon die Betriebs-Units (`sharefyx-backup.*`, `tailscaled-watchdog.*`), und es ist
P3-Eigentum, das Tailnet zu betreiben — dasselbe Muster wie der Watchdog aus Step B.

---

## §2 Die Schritte

Jeder Schritt: **Ziel · was du tippst · was ich erwarte.** „Was ich erwarte" ist die
Messstelle — schick mir die Ausgabe, bevor du weitergehst. Steht dort „**Ausgabe lesen**",
ist die Ausgabe selbst das Ergebnis; „ok" genügt nicht (P8.6-Lektion, `umask 0177`).

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

### A4 — Caddy auf dem VPS (Konfiguration von mir, sudo von dir)

Ziel: TLS-Terminierung für die eigene Domain, Weiterleitung über das Tailnet.

```bash
# auf dem VPS
# 1. Vorlage holen:  phase9_hardening/step_a/Caddyfile.template
# 2. Die drei Platzhalter ersetzen: <domain>, <vps-tailnet>, <kontakt>
sudo install -m 644 /etc/caddy/Caddyfile   # bzw. anlegen, Rechte root:root 0644
sudo systemctl reload caddy                # bzw. restart beim ersten Mal
```

- **Ausgabe lesen:** `journalctl -u caddy -n 30 --no-pager` — Caddy holt das Zertifikat per
  ACME. **Erwartet: eine Zeile ohne Fehler und der Hinweis auf die Zertifikatsausstellung.**
  Ein Zertifikatsfehler hier bedeutet fast immer: DNS auf A steht noch nicht (A5) oder Port
  80 ist nicht erreichbar. Deshalb ist die Reihenfolge A5 → A4 die sichere; wenn du A4 vor
  A5 machst, erwarte ich den Fehler und wir machen A5 sofort danach.

### A5 — DNS auf den VPS (du)

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

Ziel: 80/443 offen, alles andere zu, SSH nur über das Tailnet.

```bash
sudo ufw default deny incoming
sudo ufw default allow outgoing
sudo ufw allow 80/tcp comment "ACME + HTTP -> HTTPS"
sudo ufw allow 443/tcp comment "HTTPS"
sudo ufw enable
sudo ufw status verbose
```

- **Ausgabe lesen:** die Statusausgabe. Erwartet: 22 **nicht** offen, 80/443 offen.
- **Danach die Gegenprobe** (nicht im Terminal des VPS, sondern von deinem normalen Gerät):
  `ssh` auf die öffentliche IP muss ** scheitern**, über die Tailnet-IP muss es gehen.
  Schick beide Ausgaben — „ssh: connection refused" und „timeout" sind beide ein Fehlschlag,
  aber aus unterschiedlichen Gründen, und der Unterschied ist die Diagnose.

### A7 — Die Heim-VM auf die neue Adresse stellen (du, sudo; Liste von mir)

Ziel: `SPACE_PUBLIC_BASE_URL` und `ALLOWED_HOSTS` auf die neue Domain. **Befund 3 und 4.**

In `phase3_edge/local.env` (git-ignoriert, die einzige echte Konfigurationsquelle):

```
PUBLIC_BASE_URL=https://<domain>
ALLOWED_HOSTS=<domain>,savefyx-vmware-virtual-platform.tail4a8b49.ts.net,127.0.0.1
```

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

### A8 — Connector in beiden Claude-Konten umstellen (du)

Ziel: beide Konten (niklas + fabian) zeigen auf `https://<domain>/mcp`. **Erst jetzt**, weil
A7 die Metadaten mit dem neuen `issuer` liefert (Befund 4, Plan §3.3).

- **Ausgabe lesen:** je Konto ein echter `list_spaces`-Aufruf, **kein `curl`**. Ein gültiges
  Zertifikat und ein 200 auf `/health` sagen nichts darüber, ob der Anthropic-Connector die
  Adresse akzeptiert — das ist `[VERIFY] V150` und nur ein echter Aufruf schließt sie.

### A9 — Funnel als Rückfall dokumentieren (mache ich, sobald A1–A8 stehen)

Ziel: der nummerierte Rückfall. **Inhalt, verbindlich, in Kürze:**

Der Funnel **wird nicht abgeschaltet** (P9-C). Er bleibt betriebsbereit und antwortet weiter.
Seine Einschränkung ist **Befund 5**: nach A7 liest er, aber jeder Schreibvorgang der
Web-UI über ihn wird 403 (CSRF-Origin). Der Connector hängt an der Domain, nicht am Funnel —
deshalb ist der Ausfallfall „VPS weg" ein Lesefall, kein Ausfallfall.

Rückfall in nummerierten Schritten:
1. Prüfen, ob die Domain überhaupt antwortet: `curl -s https://<domain>/health` (von einem
   Gerät ohne VPN).
2. Antwortet sie nicht: VPS-Konsole prüfen (läuft der Caddy-Dienst, hat er eine IP, ist die
   DNS-Auflösung noch korrekt).
3. Antwortet die Domain, der Dienst dahinter aber nicht: auf der Heim-VM
   `phase3_edge/scripts/diagnose.sh` (alle sechs Prüfungen, Exit 0 = gesund).
4. Ist der VPS selbst weg: in `phase3_edge/local.env` `PUBLIC_BASE_URL` und `ALLOWED_HOSTS`
   auf den Funnel-Hostnamen zurückdrehen, `install_units.sh` + `restart sharefyx-mcp`, danach
   die Connector-Adresse in **beiden** Konten zurückstellen. Das ist dieselbe A7/A8-Sequenz
   rückwärts — es gibt keinen zweiten, kürzeren Weg, und genau deshalb steht er hier.

---

## §3 Abnahme (Plan §3.4, P9-10–P9-15)

| # | Abnahmezeile | Wie sie belegt wird | Status |
|---|---|---|---|
| P9-10 | `/health` antwortet 200 mit gültigem LE-Zertifikat | `curl` + Zertifikatsprüfung von extern (Pfad `/health`, s. Befund 2) | ⬜ |
| P9-11 | `nmap` gegen die **Heim**-IP zeigt keinen offenen Port | Gegenprobe mit Nikinger | ⬜ |
| P9-12 | `/.well-known/oauth-authorization-server` liefert den neuen `issuer` | A7-Messung | ⬜ |
| P9-13 | `list_spaces` aus **beiden** Konten über die neue Adresse | A8, echter Aufruf (V150) | ⬜ |
| P9-14 | Funnel antwortet weiter, Rückfall beschrieben | A9 — **mit der Befund-5-Einschränkung** | ⬜ |
| P9-15 | `/api/v1/overview` gemessen gegen 372,9 ms (V151) | drei Läufe, nicht einer | ⬜ |

**P9-11 ist der Test, den dieser Step am leichtesten besteht und am leichtesten verliert:**
`sharefyx-tail-proxy` öffnet 8765 auf `100.93.43.122`, also auf der **Tailnet**-Adresse. Das
ist kein offener Port am Router, und die LAN-Adresse `192.168.68.175` bleibt unberührt — P3-B
wird durch das Relay nicht gebrochen. Gegenprobe ist deshalb beides: `nmap` gegen
`192.168.68.175` (muss alles zu zeigen) **und** gegen `100.93.43.122` (muss genau 8765 zeigen,
was beweist, dass A4 überhaupt etwas findet).

---

## §4 Was dieser Schritt ausdrücklich nicht löst

- **Kein Weg zurück aus dem Tailnet-Risiko**, nur daraus heraus: der VPS hängt im Tailnet,
  die Heim-VM bleibt CGNAT-Bewohner. Hard Rule 6 unberührt.
- **Eine Kiste mehr zu patchen und laufende Kosten.** Der Preis für eine Adresse, die jeden
  Tailnet- und Account-Wechsel überlebt — die Entscheidung ist getroffen (P9-C), hier steht
  nur, was sie kostet.
- **Der Terminator sieht Klartext im Speicher.** Anders als Cloudflare (P9-D) ist es
  Deine eigene Kiste, aber es ist trotzdem ein Punkt, an dem Terminiert wird.
- **Keine Ausfallsicherung.** Fällt der VPS aus, gilt §2 A9 Schritt 4. Automatischer
  Failover ist nicht gebaut und nicht geplant.

---

## §5 Offene `[VERIFY]`s aus diesem Schritt

| Marker | Frage | Stand |
|---|---|---|
| **V149** (Plan) | Welche Metadatenfelder sind abgeleitet, welche fest? | **beantwortet** — alle abgeleitet, keines fest, s. Befund 4 |
| **V150** (Plan) | Hält der Anthropic-Connector nach dem Wechsel? | offen — A8, echter `list_spaces`, kein curl |
| **V151** (Plan) | Wie teuer ist der Weg über den VPS? | offen — P9-15, drei Läufe gegen 372,9 ms |
| **V148** (Plan) | Tailscale-Doku zu Funnel + eigener Domain | **bleibt `[VERIFY]`** — die Plan-Aussage (Funnel kann keine eigene Domain bedienen) ist plausibel und im Repo schon herangezogen, war in dieser Session aber **nicht** gegen die Live-Doku prüfbar (kein Netzzugriff). Ein VPS-Terminator umgeht diese Frage, statt sie zu beantworten — das ist der Grund, warum sie offen bleiben darf, ohne zu blockieren. |
| **V162** (neu, hier) | Setzt ein Tailscale-TCP-Forwarder (`tailscale serve --tcp`) die Tailnet-ACLs durch? | **offen und ungeprüft** — Grund, warum der Weg über `socat` gewählt wurde (§0 Befund 1). Wenn die Antwort „ja" lautet, ist `socat` ersetzbar und die Antwort gehört in den Plan. |
| **V163** (neu, hier) | Reicht `socat` mit `SystemCallFilter=@system-service` und `MemoryDenyWriteExecute=true`? | **offen** — der Wächter prüft nur, dass die Direktiven *gesetzt* sind; ob `socat` damit wirklich startet, zeigt sich erst beim ersten `systemctl start` in A0b. Falls es an der Syscall-Filterung scheitert, ist die Diagnose `systemd-analyze security` + die Meldung in `journalctl`; **nicht** einfach die Direktive fallen lassen, ohne es hier zu notieren. |

---

## §6 Nächste Runde

**A1 (Domain) und A2 (VPS) sind deine, nicht meine.** Sobald du eine Domain und eine
VPS-IP hast, geht es in dieser Reihenfolge weiter: A3 (Tailnet + ACL) → **A0b (socat +
Relay)** → A5 (DNS) → A4 (Caddy) → A6 (Firewall) → A7 (Basis-URL) → A8 (Connector) → A9
(Rückfall) → P9-10–P9-15.

**Modulstatus Step A bleibt 🟡**, nicht ✅: gebaut ist der Repo-Anteil, ausgeführt ist noch
nichts — dieselbe Einstufung wie Step B (🟡 = code-complete, install ausstehend).
