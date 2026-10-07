---
status: live
purpose: Step A (P9) — gefuehrter Ablauf A1–A9 fuer die eigene Domain ueber einen VPS als TLS-Terminator; traegt die sechs gemessenen Befunde, die den Plan korrigiert haben, und den nummerierten Rueckfall auf den Funnel
read-when: der Nikinger einen der Schritte A1–A9 ausfuehren will, oder jemand fragt, warum A4 nicht so gebaut ist, wie der Plan §3.2 es sagt
detail: L2
up: ../CLAUDE.md
down:
  - ./RUNBOOK_STEP_A_ARCHIVE.md   # 📦 §0 Befund 1–10 und A1–A7 verbatim (2026-10-07)
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

## §0 Zehn Befunde, die den Step geändert haben
> **Verbatim verschoben** nach `RUNBOOK_STEP_A_ARCHIVE.md` (`scripts/move_sections.py`) — dort unter derselben Überschrift.

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

**Stand 2026-09-30 (Session-Verlauf, damit ein kalter Leser nicht bei null startet):**
A1 ✅ Domain `eurofyx.<tld>` bestellt, TLD-Entscheidung `.com` empfohlen · A2 ✅ VPS
`217.160.128.146`, Ubuntu 24.04.5, 1 vCPU/2 GB · A3 ✅ Policy (`tagOwners` + Grant
`tag:sharefyx-edge` → `100.93.43.122`, `tcp:8765`) und Beitritt mit
`--advertise-tags` erledigt · **A0b ✅ socat 1.8.0.0 + `sharefyx-tail-proxy.service` laeuft**
(zwei Listener: `127.0.0.1:8765` und `100.93.43.122:8765`; `diagnose.sh` danach unverändert
alle Prüfungen grün inklusive des öffentlichen Pfads — der Bestand ist unberührt) · **A6 ✅ Firewall auf dem VPS: 22 nur auf `tailscale0`, 80/443 offen, default deny —
Gegenprobe von der Heim-VM: Tailnet-SSH **offen**, öffentliches SSH **timeout**
(ufw *droppt* still, `deny` ≠ `reject`), 443 **refused** (Paket kommt am Host an,
lauscht noch nichts — der Zustand vor A4) · ~~**A5 wartet** auf die Domain-Registrierung~~
**[2026-10-01] A1 registriert, A5 ✅ (`sharefyx.eurofyx.com` → `217.160.128.146`)** · **als Nächstes
A4 (Caddy)**. Ab A7 hängt die Reihenfolge: **A7 und A8 in einer Sitzung** (Korrektur zu Befund 4).

**Stand 2026-10-01 (A4-Vorbereitungsrunde):** A4 ist als **A4a + A4b** neu gefasst (Befund 9:
kein Caddy auf dem VPS, gemessen an 80/443 = kein Listener) und die Abnahmezeile **P9-10 ist in
P9-10a/P9-10b geteilt** (Befund 8: gemessen `400 Invalid host header` für die neue Domain, die
ganze Kette über einen echten Caddy 2.6.2 vor dem Relay durchgespielt). Der zweite Platzhalter
der Vorlage hieß `<vps-tailnet>` und war als *VPS*-Adresse beschrieben, obwohl `reverse_proxy`
auf die **Heim-VM** zeigt — jetzt `<heimvm-tailnet>`, mit der gemessenen Ziel-IP im Kommentar.
**Offen ist genau ein Schritt: A4.**

## §2 Die Schritte

Jeder Schritt: **Ziel · was du tippst · was ich erwarte.** „Was ich erwarte" ist die
Messstelle — schick mir die Ausgabe, bevor du weitergehst. Steht dort „**Ausgabe lesen**",
ist die Ausgabe selbst das Ergebnis; „ok" genügt nicht (P8.6-Lektion, `umask 0177`).

### A1 — Domain beschaffen (du)
> **Verbatim verschoben** nach `RUNBOOK_STEP_A_ARCHIVE.md` (`scripts/move_sections.py`) — dort unter derselben Überschrift.

### A2 — VPS beschaffen (du)
> **Verbatim verschoben** nach `RUNBOOK_STEP_A_ARCHIVE.md` (`scripts/move_sections.py`) — dort unter derselben Überschrift.

### A3 — VPS ins Tailnet, als getaggter Node (du, ACL-Entwurf von mir)
> **Verbatim verschoben** nach `RUNBOOK_STEP_A_ARCHIVE.md` (`scripts/move_sections.py`) — dort unter derselben Überschrift.

### Feld für Feld im Formular „Add rule"
> **Verbatim verschoben** nach `RUNBOOK_STEP_A_ARCHIVE.md` (`scripts/move_sections.py`) — dort unter derselben Überschrift.

### A0b — socat + Relay auf der Heim-VM (du; Unit liegt im Repo)
> **Verbatim verschoben** nach `RUNBOOK_STEP_A_ARCHIVE.md` (`scripts/move_sections.py`) — dort unter derselben Überschrift.

### A4 — Caddy auf dem VPS (Konfiguration von mir, sudo von dir) — **✅ 2026-10-01 erledigt**
> **Verbatim verschoben** nach `RUNBOOK_STEP_A_ARCHIVE.md` (`scripts/move_sections.py`) — dort unter derselben Überschrift.

### A5 — DNS auf den VPS (du)
> **Verbatim verschoben** nach `RUNBOOK_STEP_A_ARCHIVE.md` (`scripts/move_sections.py`) — dort unter derselben Überschrift.

### A6 — Firewall am VPS (du; Entwurf von mir)
> **Verbatim verschoben** nach `RUNBOOK_STEP_A_ARCHIVE.md` (`scripts/move_sections.py`) — dort unter derselben Überschrift.

### A7 — Die Heim-VM auf die neue Adresse stellen (du, sudo; Liste von mir)
> **Verbatim verschoben** nach `RUNBOOK_STEP_A_ARCHIVE.md` (`scripts/move_sections.py`) — dort unter derselben Überschrift.

### A8 — Connector in beiden Claude-Konten umstellen (du)

Ziel: beide Konten (niklas + fabian) zeigen auf `https://<domain>/mcp`. **Erst jetzt**, weil
A7 die Metadaten mit dem neuen `issuer` liefert (Befund 4, Plan §3.3).

- **Ausgabe lesen:** je Konto ein echter `list_spaces`-Aufruf, **kein `curl`**. Ein gültiges
  Zertifikat und ein 200 auf `/health` sagen nichts darüber, ob der Anthropic-Connector die
  Adresse akzeptiert — das ist `[VERIFY] V150` und nur ein echter Aufruf schließt sie.

**✅ TEILWEISE AUSGEFÜHRT 2026-10-03, 13:1x Uhr:** Konto **niklas** läuft über
`https://sharefyx.eurofyx.com/mcp` (echter Aufruf, Spaces kommen an) — das zweite Konto steht aus,
also sind **P9-13 und V150 ⚠️ „1 von 2"** und nicht ✅.

**[2026-10-04, Nikinger-Entscheidung: zurückgestellt, wandert nach P10, und ausdrücklich **kein**
Phasen-Blocker.]** Ein Schritt, der nur ein Konto braucht, ist kein Blocker, er ist ein Termin —
ein echter Blocker wäre ein **Code**-Fehler oder ein **Mess**-Befund. Die Marke wandert deshalb
von ⚠️ auf **⬜** (in der Matrix: P9-13 und V150, beide mit Wanderungsvermerk; Plan §0.1a, und
die Regel steht in der Wurzel-`CLAUDE.md` §Working style). **Was hier unverändert gilt:** die
Reihenfolge-Regel unterhalb — das zweite Konto **erst** umstellen, wenn das erste steht, und die
Reihenfolge-Regel wandert mit der Zeile nach P10, weil sie dieselbe Zeile meint. **P9-15** (drei
Läufe `/api/v1/overview` mit echter UI-Session) ist davon **unberührt** und die Arbeit der
nächsten Session. **Was der Schnitt real gekostet hat:** die
alten Token wurden entwertet (`resolver.py:48` — „Token für eine andere Ressource ausgestellt"), die
Neuanmeldung über die neue Adresse war **zwingend**, kein Neustart-Fehler. **Reihenfolge-Regel,
aus dieser Sitzung:** das zweite Konto **erst** umstellen, wenn das erste steht — ein halb
umgestellter Zustand macht die Fehlersuche unbrauchbar. **Für den Connector gibt es keinen
Übergang**: das `LEGACY_*`-Fenster gilt ausschließlich der Web-UI (CSRF-Origin, `config.py:81`),
die alte Adresse bleibt als **Browser**-Rückweg bis 2026-10-17 nutzbar, der alte **MCP**-Pfad
nicht. **Rückweg, falls A8 klemmt:** `PUBLIC_BASE_URL` in `local.env` zurück auf die alte Adresse,
`install_units.sh`, `systemctl restart sharefyx-mcp` — dann sind die alten Token wieder gültig
(„Rückweg = dieselbe A7/A8-Sequenz rückwärts", Befund 4).

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
   die Connector-Adresse in **beiden** Konten zurückstellen — **und neu verbinden**: auch der
   Rückweg wechselt die `resource`, jedes Token beider Konten wird beim Restart ungültig
   (Korrektur zu Befund 4, 2026-10-01). Das ist dieselbe A7/A8-Sequenz
   rückwärts — es gibt keinen zweiten, kürzeren Weg, und genau deshalb steht er hier.

---

## §3 Abnahme (Plan §3.4, P9-10–P9-15)

| # | Abnahmezeile | Wie sie belegt wird | Status |
|---|---|---|---|
| **P9-10a** | **`/health` über die eigene Domain mit gültigem LE-Zertifikat erreichbar — TLS-Hälfte** | A4b: `openssl s_client` (Subject, Issuer, Dates) + `curl -s -o /dev/null -w '%{http_code}' https://sharefyx.eurofyx.com/health`. **Erwartet `400` + `Invalid host header`** (Befund 8) — die `400` gehört zur Abnahme, sie ist der Beweis, dass die Kette bis zur App steht | **✅ 2026-10-01**: `certificate obtained successfully`, CN=`sharefyx.eurofyx.com`, issuer `Let's Encrypt YE1`, gültig 01.10.–30.12.2026; `400 Invalid host header` extern **und** als `status=400 ua=curl/8.7.1` im Journal der Heim-VM |
| **P9-10b** | **`/health` antwortet 200** (ursprünglicher Wortlaut von P9-10) | nach dem `ALLOWED_HOSTS`-Teil von A7 (oder A7a): `curl -s https://sharefyx.eurofyx.com/health` → `{"status":"ok",...}` | ⬜ |
| P9-11 | `nmap` gegen die **Heim**-IP zeigt keinen offenen Port | Gegenprobe mit Nikinger | ⬜ |
| P9-12 | `/.well-known/oauth-authorization-server` liefert den neuen `issuer` | A7-Messung | ⬜ |
| P9-13 | `list_spaces` aus **beiden** Konten über die neue Adresse | A8, echter Aufruf (V150) | ⬜ |
| P9-14 | Funnel antwortet weiter, Rückfall beschrieben | A9 — **mit der Befund-5-Einschränkung** | ⬜ |
| P9-15 | `/api/v1/overview` gemessen gegen 372,9 ms (V151) | drei Läufe, nicht einer | ⬜ |

**[2026-10-01, datierte Plan-Korrektur] P9-10 war als eine Zeile formuliert und ist damit zwei
Zeilen:** „200 **und** gültiges LE-Zertifikat" kann an keinem einzigen Punkt dieses Ablaufs
gleichzeitig erfüllt werden, weil die Zertifikats-Hälfte Caddy und die 200-Hälfte
`SPACE_ALLOWED_HOSTS` gehören, und `ALLOWED_HOSTS` ist A7. Die Aussage der Ursprungszeile
bleibt vollständig erhalten — sie ist nur in zwei prüfbare Hälften zerlegt, mit der Reihenfolge
P9-10a (A4) → P9-10b (A7). Das ist dieselbe Form wie Befund 2 (`/health` statt `/healthz`):
**der Plan-Wortlaut wird an der Code-Wahrheit ausgerichtet, nicht die Abnahme abgeschwächt.**

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
| **V151** (Vorabmessung, 2026-09-30) | Wie teuer ist der Weg über den VPS? | **erster Teilwert gemessen:** `tailscale ping` von der Heim-VM zum VPS antwortet in **28–37 ms über DERP Frankfurt**, nicht direkt („direct connection not established", erwartbar hinter CGNAT). Das ist das Tailnet-Bein, nicht der ganze Weg — die Referenz 372,9 ms gilt für einen kompletten `/api/v1/overview` über den Funnel. Ein DERP-Bein von ~30 ms ist dagegen vernachlässigbar, die eigentliche Latenz liegt zwischen Claude und dem VPS. **Der vollständige Vergleich (A7) steht noch aus.** | offen — P9-15, drei Läufe gegen 372,9 ms |
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

**[2026-10-01, Stand nach der A4-Vorbereitungsrunde]** Offen ist genau **ein** Schritt: **A4**,
mit A4a (messen, dann `apt install -y caddy`) und A4b (Caddyfile, `validate`, Restart) und den
drei Ausgaben, die ich oben nenne. **A4a ist reine Messung plus Paketinstallation, A4b ist
eine Datei und ein Neustart auf einer Maschine, die heute nichts Dienst-relevantes trägt.**
Danach ist die Reihenfolge, wie in §6 steht, mit zwei Änderungen aus den neuen Befunden:

1. **P9-10 ist zwei Abnahmezeilen** (§3, Befund 8). Die Zertifikats-Hälfte fällt in A4 an, die
   `200`-Hälfte wartet auf `ALLOWED_HOSTS` — A7 oder das vorgeschlagene A7a.
2. **A7 ist die einzige Stelle mit Token-Folge**, seit Befund 4 korrigiert ist. Alles davor
   (A4a, A4b, A7a) ist für beide Connectoren folgenlos; das ist der Grund, warum der Deploy von
   `v3.1.0` und das `LEGACY_*`-Fenster **vor** A7 gehört und nicht danach.
