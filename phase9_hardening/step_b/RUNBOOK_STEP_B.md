---
status: live
purpose: Step B (P9) — tailscaled-watchdog installieren und live beweisen; trägt vier gemessene Befunde, die den Plan §4 korrigiert haben (darunter: der sudoers-Weg ist unbaubar und die polkit-Aktion dieser Box ist grob)
read-when: Installieren oder Testen des tailscaled-watchdog — vor dem ersten `systemctl`-Befehl an den Watchdog
detail: L2
up: ../../phase9_hardening/CLAUDE.md
down:
  - ../step_a/RUNBOOK_STEP_A.md              # derselbe Ablauf-Stil für den anderen Infra-Step
  - ../../phase3_edge/polkit/49-tailscaled-watchdog-restart.rules   # die Regel, um die es geht
  - ../../phase3_edge/scripts/tailscaled_watchdog.sh                 # das Skript, das die Unit startet
  - ../../docs/concepts/phase9_hardening_plan.md                    # §4, Abnahme P9-16–P9-20
updated: 2026-09-30 (Step B: M3-Anteil gebaut — polkit-Regel + vier Wächter + die V153-Probe; die Ausführung ist Nikinger-Arbeit, `systemctl` nie durch einen Agenten)
---

# Step B — `tailscaled-watchdog.service` installieren und beweisen

Der Nikinger führt jeden `sudo`- und `systemctl`-Befehl aus (Hard Rule 9). **Ein Schritt pro
Runde**, und nach jedem Schritt die Ausgabe lesen, bevor du weitergehst.

## §0 Vier Befunde, die vor B1 gemessen wurden (2026-09-30)

**Befund 1 — der Plan nennt zwei Wege, einer davon ist unbaubar.** Plan §4.2: „eng geschnittene
Polkit-Regel **oder** ein `sudoers`-Fragment". Die Unit setzt `NoNewPrivileges=true`, und sudo
lebt vom setuid-Bit:

```
$ setpriv --no-new-privs -- /usr/bin/sudo -n -l
sudo: The "no new privileges" flag is set, which prevents sudo from running as root.
```

Ein `NOPASSWD:`-Fragment wäre unter dieser Unit wirkungslos. Ihn zu retten hieße,
`NoNewPrivileges` abzuschwächen — also bleibt **polkit**. V153 ist damit entschieden, und
zwar gemessen, nicht nach Präferenz.

**Befund 2 — die Unit ist auf dieser VM noch gar nicht installiert.** `ls
/etc/systemd/system/tailscaled-watchdog.*` → *No such file or directory*; `systemctl list-timers`
zeigt 0 Timer. Der Deploy vom 2026-09-18 liegt **vor** dem Step-B-Code (2026-09-26), deshalb hat
`install_units.sh` die beiden Units nie kopiert.

**Befund 3 — `polkitd` ist vorhanden, aber die passende Aktion ist die grobe.**
`polkitd 124-2ubuntu1.24.04.4`. Der systemd ist **255.4-1ubuntu8.17**, und der lokal installierte
Manpage-Abschnitt *Security* sagt wörtlich: `StartUnit()`, `StopUnit()`, `KillUnit()`,
`RestartUnit()` und ähnliche erfordern **`org.freedesktop.systemd1.manage-units`** — *eine*
Aktion für alle Unit-Zustandsänderungen. Die feingranularen
`org.freedesktop.systemd1.manager.restart-unit` gibt es erst ab neuerem systemd.

**Folge, und sie ist der eigentliche Grund für B0:** polkit kann auf dieser Box nur nach Unit
filtern, wenn systemd der Aktion ein `unit`-Attribut mitgibt. Ob es das tut, ist
unprivilegiert **nicht** auslesbar — `pkcheck` kennt die Aktion nicht, weil systemd sie erst zur
Laufzeit bei polkitd registriert:

```
$ pkcheck --action-id org.freedesktop.systemd1.manager.restart-unit --process $$
Error checking for authorization …: Action … is not registered
```

Eine Regel **ohne** Unit-Abgleich würde `savefxy` das Starten und Stoppen **jeder** Unit geben,
auch aus `sharefyx-mcp` heraus. Das ist in einer Härtungsphase eine Regression und wird nicht
gebaut. Die Repo-Regel verlangt deshalb zusätzlich `action.lookup("unit") == "tailscaled.service"`
— im ungünstigen Fall greift sie nicht und der Watchdog loggt seine vorhandene Fehlerzeile.
**Welcher der beiden Fälle gilt, entscheidet B0, und B0 fasst `tailscaled` nicht an.**

### Befund 5 — die Probe ist gelaufen: `AUTORISIERT`, und eine Verweigerung kostet 25 Sekunden

**B0 ist ausgeführt (2026-09-30, Belege vom Nikinger):**

```
$ systemctl restart sharefyx-watchdog-probe.service && echo AUTORISIERT || echo VERWEIGERT
AUTORISIERT

$ journalctl -u sharefyx-watchdog-probe.service -n 3 --no-pager
… systemd[1]: Starting sharefyx-watchdog-probe.service - WEGWERF-Probe …
… systemd[1]: sharefyx-watchdog-probe.service: Deactivated successfully.
… systemd[1]: Finished sharefyx-watchdog-probe.service - WEGWERF-Probe …
$ systemctl show -p User sharefyx-watchdog-probe.service
User=root
```

`User=root` und ein trotzdem erfolgreicher Restart aus der Hand von `savefyx` heißt: **polkit war
das Tor**, und `systemd 255.4` schickt das `unit`-Detail an die Aktion. **Die Repo-Regel greift
und ist eng.** Damit ist V153 vollständig entschieden und B1 kann laufen.

**Zwei Nebenbefunde, die in B3 zählen:**

1. **Eine Verweigerung kostet hier 25 Sekunden, nicht eine Sekunde.** Gegengetest mit einer Unit,
   die die Regel *nicht* nennt: `systemctl restart sharefyx-watchdog-probe.timer` →
   `Failed to restart …: Connection timed out`, `rc=1`, **gemessene Dauer 25 s**. Auf dieser VM
   läuft **kein polkit-Agent** (headless), eine nicht erteilte Autorisierung versucht also erst
   eine Rückfrage und läuft dann in den Agent-Timeout. Praktische Folge: **sollte die Regel
   irgendwann nicht mehr greifen, zeigt sich das im Journal als ~25-Sekunden-Hänger und nicht als
   ein schnelles „restart fehlgeschlag".** Für die Fehlersuche in B3 ist das die Kennzahl.
2. **Die Gegenprobe ist jetzt sauber — nach einem Nachlade-Rennen, das ich selbst produziert
habe.** Der erste Versuch nach dem Löschen der Probe-Regel lieferte `rc=0`; die Wiederholung
wenige Minuten später lieferte `rc=1` nach 25 s. Erklärung: polkitd hält die gelöschte Regel noch
kurz im Speicher. **Damit ist B0 vollständig bewiesen — mit** Regel autorisiert, **ohne** Regel
verweigert, gleiche Unit, gleicher User. Wer C0 wiederholt, sollte nach dem `rm` ein paar Sekunden
warten, sonst misst er das Rennen statt der Berechtigung.

 Der Test mit der `.timer`-Unit beweist nur, dass die
   Berechtigung nicht erteilt wurde; *warum* (Regel greift nicht vs. Unit existiert gar nicht —
   `systemctl is-enabled sharefyx-watchdog-probe.timer` sagt `not-found`) ist damit nicht
   getrennt. **Die saubere Gegenprobe braucht dein `sudo`** und steht als C0 in §2. Ohne sie bleibt
   der Schluss „polkit war das Tor" auf dem Journal-Beleg und der `User=root`-Messung — das trägt,
   aber C0 macht es eindeutig.

### Befund 6 — B2 hat es beim ersten Mal nicht getan: `status=203/EXEC` in jedem Takt

**Gemessen 2026-10-01, vom Nikinger ausgeführt und hier verifiziert:** `install_units.sh` lief
sauber durch, der Timer wurde `enabled`, `list-timers` zeigt ihn — und der Dienst scheiterte in
jedem Takt mit `Main process exited, code=exited, status=203/EXEC`.

Ursache, in zwei Schritten gemessen:

1. `systemctl cat tailscaled-watchdog.service | grep ExecStart` →
   `/opt/sharefyx/current/phase3_edge/scripts/tailscaled_watchdog.sh`. **Auf das Release, nicht
   auf den Checkout.**
2. `local.env:8` → `REPO_ROOT=/opt/sharefyx/current`, und `install_units.sh:53` verlangt diese
   Variable und überschreibt damit die berechnete `REPO_DIR` (gewollt: Prod-Units sollen aufs
   Release zeigen). Das Release ist `20260918T183907`; dort liegt das Skript **nicht**, es kam
   erst am 2026-09-26 ins Repo.

Der Scan über **alle** installierten Units derselben Art macht den Punkt präzise:

| Unit | ExecStart | |
|---|---|---|
| `sharefyx-backup` | `…/current/phase3_edge/scripts/backup_data_root.sh` | OK |
| `sharefyx-authbackup`, `-mcp`, `-purge`, `-staging` | `…/current/.venv/bin/python` | OK |
| `sharefyx-tail-proxy` | `/usr/bin/socat` | OK (Systempfad) |
| `tailscaled-watchdog` | `…/current/…/tailscaled_watchdog.sh` | **FEHLT** |

**Es ist also kein Fehler der Pfadlogik, sondern eine Verzögerung:** alles, was beim letzten
Deploy schon im Repo war, ist im Release; die erste danach hinzugekommene operative Datei fehlt —
und trifft zuerst die neueste Unit. **Die Lehre stand im Repo bereits:** der Phase-3-Head
notiert den Befund seit 2026-09-28 wörtlich („der Watchdog startete dadurch ins Leere"), und der
tail-proxy wurde am 2026-09-29 genau deshalb **ohne** `__REPO_ROOT__` gebaut. Nur die
watchdog-Unit selbst ist nie nachgezogen worden — der Step-B-Code ist einen Tag älter als der
Befund. **Nikinger-Entscheidung 2026-10-01: Systempfad `/usr/local/libexec/sharefyx/`**, wie beim
tail-proxy. `Documentation=` entfällt mit derselben Begründung (es zeigte auf die Doku des
Releases). Ein elfter Wächter nagelt beides fest.

**Und dann gelöst, im dritten Takt** (B2a + B2 wiederholt, 2026-10-01, Journal-Beleg des
Nikingers verifiziert):

```
11:42:54  status=203/EXEC                                                        ← noch vor daemon-reload
11:43:59  tailscaled_watchdog.sh[1173002]: … healthy: Self.Online=true
11:43:59  Deactivated successfully. / Finished.
```

Die `healthy`-Zeile belegt mehr als den Pfad: die Unit läuft als `savefyx` unter
`NoNewPrivileges` + `ProtectSystem=strict` + `SystemCallFilter=@system-service` und findet
`tailscale`, `python3`, `date` und `timeout` im Sandbox-PATH. **Damit sind Stufe 1 und der
gesunde Normalfall live; Stufe 2 (netcheck) und Stufe 3 (Restart) warten auf B3.**

**Was das über den Watchdog sagt:** `203/EXEC` ist harmlos — das Skript lief nie, es wurde nichts
neugestartet. Aber es zeigt, dass ein durchlaufender Timer **nicht** beweist, dass ein Dienst
arbeitet. Seit B2a ist der Beweis die `healthy`-Zeile, nicht die Timer-Zeile.

## §1 Was in dieser Runde passiert und was nicht

| | |
|---|---|
| **Gebaut** | `phase3_edge/polkit/49-tailscaled-watchdog-restart.rules` (die Regel), `phase9_hardening/step_b/{99-tailscaled-watchdog-probe.rules, sharefyx-watchdog-probe.service}` (die Probe), vier neue Wächter in `phase9_hardening/tests/test_tailscaled_watchdog.py`, dieses Runbook |
| **Nicht gebaut, mit Absicht** | kein Eingriff in `install_units.sh`, keine Änderung am Watchdog-Skript, keine Regel ohne Unit-Abgleich, keine polkit-`pkla`-Defaults |
| **Deine Schritte** | B0 Probe · B1 Regel installieren · B2 Units + Timer · B3 P9-19 Offline-Probe · die Abnahme P9-16–P9-20 |

## §2 Die Schritte

### B0 — Probe: trägt die polkit-Aktion ein `unit`-Attribut? *(✅ gelaufen 2026-09-30 → AUTORISIERT)*

**Ziel:** entscheiden, ob die Repo-Regel überhaupt greifen kann — ohne dass `tailscaled`
irgendwann neugestartet wird.

```bash
# auf der HEIM-VM (dieser Repo-Checkout)
sudo install -m 0644 phase9_hardening/step_b/99-tailscaled-watchdog-probe.rules \
     /etc/polkit-1/rules.d/
sudo install -m 0644 phase9_hardening/step_b/sharefyx-watchdog-probe.service \
     /etc/systemd/system/
sudo systemctl daemon-reload
```

**Was ich erwarte:** keine Fehlermeldung. Installiert sind damit *nur* zwei Wegwerf-Dateien;
an `sharefyx-mcp`, `tailscaled` oder der Firewall ändert sich nichts.

**Danach der eigentliche Test — als `savefyx`, ohne `sudo`:**

```bash
systemctl restart sharefyx-watchdog-probe.service && echo AUTORISIERT || echo VERWEIGERT
```

**Was ich erwarte — zwei mögliche Antworten, beide sind ein Ergebnis:**

| Ausgabe | Bedeutung | Folge |
|---|---|---|
| `AUTORISIERT` | systemd 255 hängt das `unit`-Detail an die Aktion | die Repo-Regel ist eng und funktioniert → weiter mit B1 |
| `VERWEIGERT` (polkit-Fehler im Journal) | kein `unit`-Detail | die Repo-Regel bliebe stumm → **B1 entfällt**, zurück ans Zeichenbrett (siehe §4) |

**Aufraeumen, sobald die Antwort feststeht** (nicht später — die Probe-Unit ist ein Loch in
`/etc/systemd/system/`):

```bash
sudo rm -f /etc/systemd/system/sharefyx-watchdog-probe.service \
           /etc/polkit-1/rules.d/99-tailscaled-watchdog-probe.rules
sudo systemctl daemon-reload
```

### C0 — Gegenprobe: ohne Regel derselbe Befehl *(du, ein `sudo`; optional, aber eindeutig)*

Solange die Probe-Unit installiert ist, lässt sich der Beweis schließen: Regel weg, derselbe
Befehl, jetzt muss er verweigert werden.

```bash
sudo rm -f /etc/polkit-1/rules.d/99-tailscaled-watchdog-probe.rules
systemctl restart sharefyx-watchdog-probe.service; echo "rc=$?"
```

**Was ich erwarte:** `rc=1`, wiederum nach ~25 s (kein Agent, Befund 5). **Wichtig: nicht auf
`AUTORISIERT` hoffen** — falls er *doch* autorisiert wird, wäre polkit auf dieser Box nicht die
Grenze, die wir angenommen haben, und das wäre ein Befund für V153, kein Grund zur Eile.

### ### B1 — die echte Regel installieren *(du, nur bei `AUTORISIERT`)*

```bash
sudo install -m 0644 phase3_edge/polkit/49-tailscaled-watchdog-restart.rules \
     /etc/polkit-1/rules.d/
```

**Was ich erwarte:** keine Ausgabe. **Nur Polkit-Reload nötig, kein `daemon-reload`** — polkitd
liest `rules.d` bei jeder Anfrage neu. `install` überschreibt eine alte Fassung derselben Regel
folgenlos, deshalb ist der Befehl wiederholbar.

### B2a — Skript an den Systempfad installieren *(du, ein `sudo`; neu seit 2026-10-01)*

**Ziel:** das Skript dorthin legen, wo die Unit es sucht. `local.env` setzt
`REPO_ROOT=/opt/sharefyx/current`, deshalb zeigte der alte `ExecStart=__REPO_ROOT__/…` aufs
**Release** — und dort lag `tailscaled_watchdog.sh` nicht, weil es erst nach dem Deploy vom
2026-09-18 ins Repo kam. Das Ergebnis war `status=203/EXEC` in jedem Takt. Die Unit zeigt jetzt
auf einen Systempfad; dieses Kommando ist der Gegenstück und muss **vor** B2 laufen:

```bash
sudo install -D -m 0755 phase3_edge/scripts/tailscaled_watchdog.sh \
     /usr/local/libexec/sharefyx/tailscaled_watchdog.sh
```

**Was ich erwarte:** keine Ausgabe. **Nach jedem Skript-Update dasselbe Kommando erneut** — die
Unit startet die installierte Kopie, nicht die im Repo.

### B2 — Units installieren und den Timer aktivieren *(du)*

```bash
sudo phase3_edge/scripts/install_units.sh      # kopiert u. a. beide Watchdog-Units
sudo systemctl enable --now tailscaled-watchdog.timer
```

**B2a muss vorher gelaufen sein**, sonst startet die Unit ins Leere (203/EXEC) — genau das ist
am 2026-10-01 passiert.

**Zwei Fallen, beide bekannt:**

1. **`install_units.sh` aktiviert nur `sharefyx-mcp.service`.** Der Watchdog-Timer kommt
   installiert, aber **nicht** enabled — der zweite Befehl ist Pflicht, nicht Kosmetik. (Dasselbe
   gilt für `sharefyx-tail-proxy` aus Step A: `install_units.sh` startet es nicht mit.)
2. **Das Skript startet `sharefyx-mcp` neu** (`systemctl enable --now sharefyx-mcp.service`).
   Das ist erwartet und harmlos — der Dienst ist stateless und der Connector handelt einen
   Neuverbindungen, aber der MCP-Server ist währenddessen kurz nicht erreichbar. Wenn du das
   vermeiden willst, installier die beiden Watchdog-Units direkt (das Skript macht nichts
   weiter, als `__REPO_ROOT__` zu ersetzen):

   ```bash
   for u in service timer; do
     sed -e "s#__REPO_ROOT__#$(pwd)#" \
         phase3_edge/systemd/tailscaled-watchdog.$u > /tmp/tailscaled-watchdog.$u
     sudo install -m 0644 /tmp/tailscaled-watchdog.$u /etc/systemd/system/
   done
   sudo systemctl daemon-reload
   ```

**Prüfungen danach, alle drei ohne `sudo`:**

```bash
systemctl is-enabled tailscaled-watchdog.timer     # → enabled
systemctl list-timers tailscaled-watchdog.timer     # → eine Zeile mit NEXT
systemctl cat tailscaled-watchdog.service | grep ExecStart
```

**Was ich erwarte:** `enabled`, eine Timer-Zeile, und ein `ExecStart` **ohne** `__REPO_ROOT__` —
er muss jetzt `/usr/local/libexec/sharefyx/tailscaled_watchdog.sh` lauten. Ein `__REPO_ROOT__`
oder ein `/opt/sharefyx`-Pfad bedeutet: alte Unit im System, `install_units.sh` lief nicht
durch. Das ist **P9-16**.

**Dann der kostenlose Teil des Beweises, noch ohne jeden Ausfall:** der Timer feuert nach dem
Aktivieren praktisch sofort (`OnBootSec` liegt in der Vergangenheit). Innerhalb einer Minute:

```bash
journalctl -u tailscaled-watchdog.service -n 10 --no-pager
```

**Was ich erwarte:** eine Zeile `healthy: Self.Online=true`. Damit ist belegt, dass die Unit unter
ihrer Härtung durchläuft, Stufe 1 antwortet, und der Timer den Dienst wirklich aufruft — ohne
dass irgendetwas neugestartet wurde. (Aktueller Ausgangszustand, 2026-09-30, read-only gemessen:
`Self.Online = True`, `BackendState = Running`.)

### B3 — P9-19: ein absichtlich herbeigeführter Offline-Zustand *(du, Fenster mit LAN-Zugang)*

**Vorher lesen:** B3 ist der einzige Schritt, bei dem der Tailnet-Knoten kurz von außen
verschwindet. Der Claude-Connector ist währenddessen **nicht erreichbar** (er hängt am
Funnel-Host), deine lokale Sitzung ist es weiterhin. Nicht über das Tailnet starten.

**Ich empfehle Variante 1 zuerst**, weil sie sich von selbst heilt: mit `systemctl stop
tailscaled` fällt genau die Prüfung weg, auf die der Ablauf reagiert (`status --json` schlägt
fehl → *unclear* → `netcheck` schlägt fehl → Restart-Zweig), und der Watchdog startet den
Dienst von selbst wieder. Variante 2 (`tailscale down`) trifft den `Online=false`-Zweig, überlebt
aber einen Neustart und braucht deshalb ein manuelles `tailscale up` hinterher. Variante 3
(Control-Plane blockieren) ist dem Vorfall vom 2026-09-15 am nächsten und gleichzeitig die
Gefährlichste — sie ist **nicht** der erste Versuch.

```bash
# Variante 1 — selbstheilend, empfohlen für den ersten Durchgang
sudo systemctl stop tailscaled
sleep 90                       # der Timer feuert alle 60 s; 90 s lässt zwei Zykse zu
sudo systemctl is-active tailscaled      # → active, gerne von selbst gestartet
```

**Belege, die ich brauche (alle drei, ungekürzt):**

```bash
journalctl -u tailscaled-watchdog.service --since "-5 min" --no-pager   # Pfad: unclear → netcheck → restart
journalctl -u tailscaled.service --since "-5 min" --no-pager            # Systemds eigenes Started/Stopped
sudo systemctl status tailscaled-watchdog.service --no-pager            # Ergebniszeile
```

**Zusätzlich der Rate-Limit-Beweis (P9-19 fordert „genau einen Restart"):** die State-Datei
`/run/tailscaled-watchdog/last_restart` liegt jetzt in der Vergangenheit. Ein zweiter Ausfall
**innerhalb** von 15 min darf keinen Restart auslösen, sondern muss loggen:

```
… tailscaled-watchdog: rate-limited (NNNs since last, threshold 900s)
```

**Was ich erwarte:** genau **eine** `tailscaled restarted`-Zeile, und der Netcheck-Timeout von
30 s muss im Fenster sein — Stage 2 hat eigene 30 s, der Timer feuert also nicht zwingend im
ersten Zyklus. Rechne lieber mit zwei Zyklen (bis ~3 min nach dem Stopp).

**Falls die Regel nicht greift**, ist das kein Desaster: das Skript loggt `restart fehlgeschlag
(Polkit-Regel oder sudoers-Fragment fehlt? — V153)`, der Dienst bleibt unten, und du startest ihn
per `sudo systemctl start tailscaled`. Genau dafür steht die Zeile im Skript.

## §3 Abnahme (Plan §4.4, P9-16–P9-20)

| # | Kriterium | Stand |
|---|---|---|
| `P9-16` | `systemctl list-timers` zeigt den Timer | ✅ **2026-10-01** — Timer `enabled` **und** `active`, `NEXT` gesetzt. Der erste B2-Durchlauf lieferte noch `203/EXEC` (Befund 6); nach **B2a** steht der eigentliche Beleg: `tailscaled_watchdog.sh[…]: tailscaled-watchdog: healthy: Self.Online=true` + `Finished` |
| `P9-17` | 5 Tests grün | ✅ **10/10** grün (5 Alt + 5 neu aus den Wächter-Runden, zuletzt `test_execstart_carries_no_repo_path` nach dem 203/EXEC-Befund) |
| `P9-18` | Härtungs-Direktiven per statischem Wächter belegt | ✅ `test_unit_file_has_the_three_hardening_directives` |
| `P9-19` | Absichtlicher Offline-Zustand ⇒ genau ein Restart, im Journal belegt | ⬜ **B3** (du) |
| `P9-20` | V152 beantwortet | ✅ „gibt es nicht" (kein Tailscale-Feature ohne Add-on, `pragmaxim/tailscaled-watchdog` macht denselben Job) |
| `V153` | Polkit oder sudoers? | ✅ **beantwortet**: `sudoers` ist ausgeschlossen (Befund 1), polkit greift und trägt (Befund 5, `AUTORISIERT` mit Journal-Beleg bei `User=root`) |

## §4 Was dieser Schritt ausdrücklich nicht löst

- **Wenn B0 `VERWEIGERT` sagt**, ist die Repo-Regel wirkungslos und es bleiben zwei Wege, die
  beide eine Entscheidung des Nikingers sind, weil beide die Härtung berühren: (a) `manage-units`
  **ohne** Unit-Abgleich freigeben — das gibt `savefyx` das Management aller Units und ist
  abgelehnt; (b) den Watchdog als `User=root` fahren und gar nicht autorisieren — dann trägt das
  Skript aber PATH-aufgelöste Binaries (`tailscale`, `systemctl`, `date`, `timeout`) plus ein
  Inline-`python3` mit Root-Rechten, was die Sandbox aushebeln könnte. Eine dritte, sauberere
  Form wäre ein **fixer Root-Oneshot** (`ExecStart=/usr/bin/systemctl restart tailscaled.service`,
  keine Shell, keine PATH-Auflösung), den die unprivilegierte Einheit per Flag anstößt — das ist
  echte Umfangserweiterung und **nicht** in diesem Runde gebaut.
- **Ein Skript-Update braucht ein `sudo install -D -m 0755 …` an den Systempfad.** Das ist der Preis des release-unabhängigen Pfades und der Grund, warum B2a überhaupt existiert: die Unit startet die installierte Kopie, nicht die Datei im Repo.
- Der Watchdog erkennt **nur** einen Offline-Zustand des Knotens. Ein Ausfall, bei dem
  `tailscaled` läuft und die Control-Plane hängt, wird genau dann gesehen, wenn der Knoten
  dadurch auch als offline gilt — die Logik ist die des Plans (§4.2), nicht mehr.
- `Restart=on-failure` in `tailscaled` bleibt unberührt: er deckt den Vorfall vom 2026-09-15
  nachweislich nicht (der Dienst fiel nie), und der Watchdog ist genau deshalb gebaut.

## §5 Nächste Runde

**B0, C0, B1 und B2 sind gelaufen** (B2 einmal gescheitert, Befund 6). **Es fehlen B2a** (Skript an den Systempfad, ein `sudo install -D -m 0755`), **B2 wiederholen** und **B3 (P9-19)**. Erst die `healthy`-Zeile im Journal belegt, dass die Unit wirklich arbeitet — eine laufende Timer-Zeile beweist es nicht. Bleibt er aus, ist Step B **nicht** 🟡→✅: P9-19 ist eine
Abnahmezeile mit Beweischarakter, keine Formsache. Der nächste inhaltliche P9-Schritt ist
unabhängig davon **A4/A5** — beide hängen an der Domain und nicht am Watchdog.
