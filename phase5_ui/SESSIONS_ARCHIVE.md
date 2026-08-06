---
status: live
purpose: Archiv älterer Session-stopped-Blöcke aus phase5_ui/CLAUDE.md, newest-first, verbatim
read-when: Audit vergangener Sessions dieser Phase; NICHT für normalen Session-Start
detail: L3
up: CLAUDE.md
updated: 2026-08-06 (zehnter Block archiviert, Rotation nach dem Step-8-Live-Abschluss)
---

# Session-Archiv — Phase 5 Web-UI, REST-API, Auth-Selbstverwaltung

## Session stopped — 2026-08-05, vierter Nachtrag (Step 8: Deploy, Rollback, Staging, Auth-Backup, Messung)

**Ergebnis:** Step 8 ist gebaut. Bis hierher lief der Dienst direkt aus dem
Git-Arbeitsverzeichnis — ein Editor-Speichern wirkte sofort auf die laufende Instanz, ein
Rollback gab es nicht, und die `auth.sqlite3` (Passwort-Hashes, **umkehrbare** TOTP-Seeds,
Token-Familien) wurde von **keinem** Backup erfasst; gesichert war nur der `DATA_ROOT`. Ein
Plattenschaden hätte die Notizen gerettet und beide Konten gekostet.

Neu: `phase5_ui/scripts/{deploy.sh,rollback.sh,authbackup.sh,restore_auth_check.sh,ui_budget.py}`,
`phase5_ui/systemd/{sharefyx-authbackup.service,.timer,sharefyx-staging.service}`, vier weitere
Prüfungen in `phase3_edge/scripts/diagnose.sh`, drei optionale Platzhalter in
`install_units.sh`.

**Nikinger-Entscheidungen dieser Planung (2026-08-05):** Deploy-Quelle ist das **lokale Repo**,
nicht GitHub („von GitHub klonen nur Leute, die das Projekt selber hosten wollen") — `deploy.sh
origin/main` funktioniert nach einem `git fetch` trotzdem, der Klon bringt die Remote-Refs mit.
Staging wird **jetzt** gebaut, wie in P5-AB gelockt.

**Drei dokumentierte Abweichungen vom Plan-Wortlaut:**
1. **Health-Gate ohne „authentifizierte API-Probe".** Der Plan verlangt eine; eine echte
   Anmeldung bräuchte Passwort **und** TOTP-Seed auf der Platte, und **Hard Rule 1 verbietet das
   ausnahmslos**. Stattdessen vier Proben, die dasselbe beweisen, ohne ein Geheimnis anzulegen:
   `/health` → 200, `/ui/login` → 200 (webui gemountet), `/api/v1/me` ohne Cookie → **401**,
   `/mcp/` ohne Bearer → **401**. Ein Deploy, der versehentlich die Authentisierung ausbaut,
   fällt damit auf — genau darum ging es bei der Forderung.
2. **Drei Staging-Platzhalter statt zwei.** `__STAGING_BASE_URL__` kam dazu, weil
   `SPACE_PUBLIC_BASE_URL` unter `AUTH_MODE=oauth` Pflicht ist (`authserver/config.py`) — mit nur
   Port und `DATA_ROOT` wäre die Unit nicht startfähig gewesen.
3. **Die Staging-Platzhalter sind optional mit Default, nicht Pflicht.** Sonst bräche
   `install_units.sh` auf **jeder bestehenden Installation** ab, sobald die neue Unit dazukommt —
   die `local.env` der VM kennt die Schlüssel ja noch nicht. Defaults: Port `8766`,
   `<DATA_ROOT>-staging`, `<PUBLIC_BASE_URL>:<STAGING_PORT>`.

**Zwei eigene Funde:**
- **Ein zurückgerolltes Release wäre das nächste Rollback-Ziel gewesen.** Aufgefallen erst beim
  echten Probelauf, nicht beim Schreiben: nach einem gescheiterten Health-Gate bleibt das
  Release liegen (gewollt — man will hineinsehen können), ist aber das **jüngste** Verzeichnis.
  Der nächste erfolgreiche Deploy hätte es damit zum „vorherigen" Release gemacht; ein Rollback
  wäre auf genau dem Stand gelandet, der eben nachweislich den Gate gerissen hat. `deploy.sh`
  markiert es jetzt als `*.failed`, `rollback.sh` schließt solche Verzeichnisse aus. Beides mit
  einem Test festgehalten.
- **V13-Drift in `phase3_edge/`.** `phase3_edge/CLAUDE.md` dokumentiert V13 seit dem 2026-07-28
  als geschlossen — und führt es 114 Zeilen weiter unten in derselben Datei noch als offen; der
  `[VERIFY]`-Kommentar in `diagnose.sh` trug dieselbe veraltete Aussage („bei Abweichung in
  Step 7 korrigieren"). Beide Stellen mit datierter Notiz korrigiert. Kein `[VERIFY]` dieser Art
  ist mehr offen.

**Messung (P5-AD) — löst `[VERIFY]` V10 auf.** `ui_budget.py`, 220 synthetische Items,
in-process gegen ein temporäres `DATA_ROOT`:

| Messgröße | Gemessen | Ziel | |
|---|---|---|---|
| `GET /api/v1/items?limit=50` roh | **22.4 KB** | < 64 KB | ✅ |
| `GET /api/v1/items?limit=50` gzip | **1.2 KB** | < 12 KB | ✅ |
| `GET /api/v1/items/{id}` typisch | **0.6 KB** | < 8 KB | ✅ |
| `app.js` + `app.css` + Font | **54.8 KB** | < 250 KB | ✅ (js 14.6 / css 6.3 / Font 33.9) |
| Erstaufruf `/ui/` bis interaktiv | **58.2 KB** | < 400 KB | ✅ |

Alle fünf im Korridor, mit großem Abstand. **Was die letzte Zahl NICHT ist:** ein
Browser-Messwert. Sie summiert, was ein frischer Browser laden muss (`app.html` + statische
Dateien gzip + die drei Bootstrap-Antworten `/api/v1/{me,meta,overview}`, die `init()` in genau
dieser Reihenfolge holt) — ohne Verbindungsaufbau, TLS-Handshake und HTTP-Header. Eine
Nachbildung, ehrlich benannt, keine Labormessung.

**`[SEAM]` Blue/Green (P5-AC), dokumentiert statt gebaut:** `deploy.sh` liest den Zielport aus
**einer** Variablen (`SHAREFYX_PORT`) und benutzt sie an **einer** Stelle (der Health-Gate-URL).
Der spätere Weg wäre eine Template-Unit `sharefyx-mcp@.service` plus Zielwechsel über
`tailscale serve`/`funnel`. **Die Bedingung, unter der das überhaupt sinnvoll wird:** ab dann
müssen alle Schemaänderungen expand/contract-fähig sein, weil zwei Farben dieselbe
`auth.sqlite3`, denselben Index und dasselbe Git-Repo teilen. Solange das nicht gilt, wäre
Blue/Green kein Sicherheitsgewinn, sondern zwei Prozesse, die sich gegenseitig die Daten
umschreiben.

**Verifiziert:** `pytest -q` → **570/570 grün** (549 vorher, +21: 15 `test_deploy_scripts.py`
neu, +6 `test_units.py`). `pyflakes` und `bash -n` über alle neuen/geänderten Dateien sauber.
`deploy.sh`/`rollback.sh` **real gefahren** gegen ein Wegwerf-Layout mit gestubbtem
`systemctl`/`curl` und einem echten kleinen Git-Repo als Quelle — beide Fehlschlagpfade (rote
Tests, gerissener Health-Gate) inklusive Prüfung, wohin der Symlink danach zeigt.
`authbackup.sh`/`restore_auth_check.sh` real gegen eine echte kleine SQLite-Datei (Retention,
`0600`, Zeilenzählung). `install_units.sh` hermetisch gegen eine Wegwerf-Kopie mit umgebogenem
Ziel — alle acht Units ohne unaufgelösten Platzhalter. `git diff --stat` auf `storage/`,
`mcpserver/{tools,permissions,server}.py` bleibt **leer** (Akzeptanzkriterium 18).

Ein Test verdient eine eigene Erwähnung, weil er über die im Plan genannten hinausgeht:
`test_every_placeholder_in_every_unit_is_known_to_the_install_script` prüft **allgemein**, dass
kein `__FOO__` in irgendeiner Unit dem Installationsskript unbekannt ist. Ohne ihn hätte die
nächste Unit mit einem neuen Platzhalter erst beim `sudo install_units.sh` auf der echten
Maschine einen Abbruch erzeugt — und zwar für **alle** Units, nicht nur die neue.

**Advisor:** in dieser Session **nicht erreichbar** („temporarily overloaded", beim Review vor
dem Commit erneut versucht) — anders als in Step 7b, wo er mit F7 den schwersten Fund beisteuerte.
Ersatz: der dokumentierte Fallback (`pytest` + `pyflakes` + `bash -n` + echte Probeläufe aller
Skripte) plus ein gezielter Selbst-Review der riskantesten Stellen, der zwei Dinge ergab, beide
behoben: (1) beim **allerersten** Deploy gibt es kein vorheriges Release, `rollback.sh` bricht
dann korrekt ab — die Meldung sagt jetzt warum, und der Kommentar erklärt, weshalb das kein
Betriebsproblem ist (vor dem Cutover zeigt die Unit noch aufs Arbeitsverzeichnis; genau deshalb
steht der erste Deploy im Runbook **vor** dem Cutover). (2) `test_deploy_script_aborts_when_
tests_fail` scheitert in Wahrheit daran, dass im Wegwerf-Release gar kein `pytest` installiert
ist, nicht an einem absichtlich roten Test — der Docstring behauptete das Gegenteil und sagt es
jetzt geradeheraus. Die Aussage des Tests bleibt gültig: `deploy.sh` unterscheidet nicht zwischen
„Test rot" und „Testlauf nicht durchführbar", und beides muss denselben Abbruch auslösen.

**Nachtrag 2026-08-05, beim ersten echten Deploy des Nikingers — der schwerwiegendste Fund
dieses Steps, und er stammt aus meinem eigenen Testcode:**

Der Deploy brach ab („Tests im Release rot"), das Release wurde gelöscht, der Symlink blieb
unberührt — **das Sicherheitsnetz hat exakt so funktioniert, wie es soll.** Die Ursache dahinter
war aber keine echte Regression:

`test_deploy_scripts.py :: _env()` baute die Testumgebung aus `dict(os.environ)` und setzte nur
die Variablen, die es selbst braucht. Der Nikinger hatte für den Deploy
`SHAREFYX_SYSTEMCTL="sudo systemctl"` **exportiert** — diese Variable rutschte damit in jeden
Testlauf durch. Die Tests bauten also ein `deploy.sh`, das `sudo systemctl restart sharefyx-mcp`
**auf der echten Maschine** aufrief. Das PATH-Stubbing schützt davor nicht: `sudo` findet das
echte Binary über `secure_path`, nicht über den vorangestellten Stub-Pfad. Und weil unmittelbar
vorher ein `sudo -v` gelaufen war, brauchte es nicht einmal ein Terminal.

**Nachgeprüft, nicht vermutet:** `journalctl` zählte im Testfenster **52** Start-/Stop-Zeilen der
Produktiv-Unit. Die Testsuite hat den laufenden Dienst dutzendfach neu gestartet. Folgenlos
(ein Neustart ist harmlos, `/health` und `/ui/login` antworten wieder mit 200), aber es hätte nie
passieren dürfen: dieselbe Regel, die für `DATA_ROOT` und Netz gilt — **nie gegen die Realität** —
gilt für die Prozesssteuerung genauso.

Behoben in **beiden** betroffenen Testdateien über ein gemeinsames `_clean_environ()`, das jede
`SHAREFYX_*`/`SFX_*`-Variable des Aufrufers verwirft:
`phase5_ui/tests/test_deploy_scripts.py` (dort eskaliert) und
`phase3_edge/tests/test_backup_scripts.py` (dieselbe Bauart, dort hätte ein exportiertes
`SHAREFYX_BACKUP_KEEP` die Retention-Tests still verfälscht — vorsorglich mitgeschlossen).
Regressionstest `test_harness_ignores_ambient_sharefyx_configuration` hält fest, dass **nur**
vom Test selbst gesetzte Variablen übrig bleiben. Gegenprobe gefahren: mit exportiertem
`SHAREFYX_SYSTEMCTL`/`SHAREFYX_RELEASES_DIR`/`SHAREFYX_BACKUP_KEEP` waren vorher **3 Tests rot**,
danach alle grün.

**Die allgemeine Lehre, die über diesen Fall hinausgeht:** ein Test, dessen Verhalten von der
Shell des Aufrufers abhängt, ist kein Test. Wenn eine Testsuite ein Programm gegen eine Attrappe
laufen lässt, muss sie die Umgebung **konstruieren**, nicht erben.

**Nachtrag 2026-08-05/06 — Staging live, `[VERIFY]` V36 geschlossen:** der Nikinger hat den
DATA_ROOT geklont, `sharefyx-staging.service` aktiviert und die Instanz über
`sudo tailscale serve --bg --https=8766 8766` freigegeben. **Bewusst mit `sudo` statt
`tailscale set --operator=savefyx`** (Nikinger-Entscheidung): die Serve-Konfiguration überlebt
ohnehin im `tailscaled`-Zustand, ein dauerhaftes Operator-Recht würde dagegen genau dem Benutzer,
unter dem `deploy.sh` läuft, erlauben, den **Produktiv**-Funnel umzustellen oder abzuschalten.
Least privilege vor Bequemlichkeit.

**V36 read-only gegengeprüft:** Funnel steht auf 443 → `127.0.0.1:8765` (öffentlich, unverändert),
Serve auf 8766 → `127.0.0.1:8766` und ist als **`tailnet only`** ausgewiesen — kein gemeinsamer
Port, Staging nie über Funnel (P5-AB). Staging antwortet über den Tailnet-Weg mit 200 auf
`/health` und `/ui/login`, Produktiv unverändert 200.

**Die Falle, die dabei nicht zugeschnappt ist** (und die ich vorher in `local.env.example`
benannt habe): `STAGING_PORT` ist der **lokale** Port, `tailscale serve --https=<X>` bestimmt den,
den der Browser sieht. Der Default `<PUBLIC_BASE_URL>:<STAGING_PORT>` stimmt **nur**, wenn beide
gleich sind. Hier sind sie es (8766/8766), die eingesetzte `SPACE_PUBLIC_BASE_URL` deckt sich
exakt mit der realen Serve-URL. Bei `--https=8443` wäre sie falsch gewesen — und der erste
Einladungslink auf Staging wäre in demselben `403 Herkunft (Origin) stimmt nicht` gelandet, der
in P4 und P5 je eine Session gekostet hat. Deshalb war die Reihenfolge „erst serven, dann
ablesen, dann eintragen" keine Förmlichkeit.

**Nachtrag 2026-08-06 — der erste Staging-Einladungslink führte ins Leere, Ursache zweimal
meine, behoben:** der Nikinger meldete „die Accounts waren noch aktiv, die Einladungslinks haben
beide nicht funktioniert". Read-only nachgesehen statt geraten — und das Gegenteil belegt:
**Staging hatte 0 Nutzer, 0 UI-Sitzungen, 2 unverbrauchte Einladungen und insgesamt 4 Anfragen**;
Produktiv dagegen `niklas`/`fabian` aktiv. Das Journal zeigte den eigentlichen Vorgang wörtlich:
`{"path":"/ui/invite/kktcp…","status":404}` **auf der Produktivinstanz**. Die Einladung war für
die Staging-Datenbank erzeugt, der Link zeigte auf Produktiv. **Die Instanz-Trennung hat also
exakt funktioniert** — nur war das Werkzeug irreführend:

1. Mein Runbook-Befehl setzte nur `STATE_DIRECTORY`. `authctl.py invite` **verlangt** aber
   zusätzlich `SPACE_PUBLIC_BASE_URL` (`authctl.py:94`) — der Nikinger musste die fehlende
   Variable also selbst ergänzen, und der naheliegende Wert ist die Produktiv-URL.
2. `authctl.py invite` schrieb den Token in die Datenbank aus `STATE_DIRECTORY`/`SPACE_AUTH_DB`
   und baute den Link aus `SPACE_PUBLIC_BASE_URL` — **zwischen beiden gab es keinerlei
   Verbindung und keinen Abgleich.** Die Fehlermeldung auf der falschen Instanz lautet
   „Einladung ungültig oder abgelaufen", was sich wie „Konto existiert bereits" liest und in eine
   ganz andere Richtung führt.

Behoben (Nikinger-Anregung): `invite` nennt jetzt auf stderr die **beschriebene Datenbank mit
Kennzeichnung `[PRODUKTIV]`/`[STAGING]`**, die **gebaute Ziel-URL** und eine Prüfaufforderung.
Der Link selbst bleibt allein auf stdout (Hard Rule 7). Bewusst **keine** Heuristik, die aus der
URL auf die Instanz schließt: die Staging-URL enthält das Wort „staging" nicht (sie unterscheidet
sich nur im Port), eine solche Prüfung läge in der Hälfte der Fälle daneben. Das Werkzeug nennt
die Hälfte, die es sicher weiß — welche Datenbank es beschrieben hat — und überlässt den Abgleich
dem Menschen. **Der stärkere Weg wäre**, dass der Dienst seine `SPACE_PUBLIC_BASE_URL` beim Start
in `schema_meta` hinterlegt; dann könnte `authctl` autoritativ widersprechen. Als möglicher
Ausbau notiert, nicht gebaut — das berührt `authserver/store.py`s Startpfad und war für diesen
Nachtrag zu viel.

**Nachtrag 2026-08-06, zweiter Anlauf — „Proxy-Server verweigert die Verbindung" auf Staging:
kein Fehler, sondern die Sicherheitseigenschaft bei der Arbeit.** Der Nikinger bekam die Meldung
im Browser für `…ts.net:8766`. Serverseitig war alles gesund (Dienst `active`, `127.0.0.1:8766`
→ 200, **und der Tailnet-Name `https://…:8766/health` von der VM aus ebenfalls → 200**,
Serve-Konfiguration unverändert, `tailscaled` lauscht auf `100.118.131.68:8766`). Der Server
nahm die Verbindung also an — der Browser kam nie an.

`tailscale status` zeigt die Ursache in einer Zeile: **das Tailnet enthält genau ein Gerät**, die
VM selbst. Keine Peers. Der Windows-Host des Nikingers ist **nicht** Mitglied.

Der Grund, warum das nie auffiel:

| | Weg | Tailnet-Mitgliedschaft nötig? |
|---|---|---|
| Produktiv (443) | `tailscale funnel` → öffentliches Internet | **nein** |
| Staging (8766) | `tailscale serve` → nur Tailnet | **ja** |

Die Produktiv-UI lief immer über den **öffentlichen Funnel**, nie über das Tailnet. Staging ist
per P5-AB bewusst nicht öffentlich — also ist es aus einem Nicht-Tailnet-Browser korrekt
unerreichbar. Firefox' Wortlaut („Proxy-Server verweigert…") ist dabei irreführend; es ist eine
schlicht abgewiesene Verbindung, kein Proxy im Spiel (auf der VM sind weder Proxy-Umgebungs-
variablen noch ein GNOME-Systemproxy gesetzt, und es existiert dort gar kein Firefox-Profil —
der Browser läuft auf einem anderen Rechner).

**Weg zum Zugang:** Tailscale auf dem Windows-Host installieren, mit demselben Konto anmelden.
Bewusst **nicht** die Alternativen: ein SSH-Tunnel bräche die Basis-URL
(`https://…:8766` gegen `http://localhost:8766` → exakt der Origin-Fehler aus P4/P5), und
Staging über Funnel freizugeben verbietet P5-AB — eine Testinstanz gehört nicht ins öffentliche
Internet.

**Damit ist auch der „Zertifikatsfehler" bei Fabians Konto sehr wahrscheinlich erklärt** (Fabians
Gerät ist ebenso wenig im Tailnet) — **aber nicht bewiesen**: der Wortlaut lautete „Zertifikat",
nicht „Verbindung verweigert", und ein TLS-Fehler erreicht den Server nie, es steht also nichts
im Journal. Bleibt als offener, kleiner Punkt stehen, bis er wieder auftritt: exakter Wortlaut
und die URL aus der Adresszeile genügen zur Einordnung.

**Nachtrag 2026-08-06, dritter — Staging wird abgeschaltet. Revidiert P5-AB, Nikinger-Entscheidung.**

Der Weg dorthin gehört zum Befund, weil er zweimal an einer Begriffsverwechslung hing: der
Nikinger verstand „prod" als *die Umgebung, in der die Software produziert wird* (die Arbeitskopie
unter `/dev`) und „staging" als *die Instanz für den Alltag*. Tatsächlich ist es umgekehrt —
`sharefyx-mcp` hält die echten Notizen beider Personen, `sharefyx-staging` nur eine Kopie vom
Vormittag. Erst als der reale Zustand als Tabelle nebeneinanderstand (welche Daten, welche
Konten, wer kommt heran, welcher Code), war die Lage eindeutig. **Lehre: bei zwei Instanzen nie
über Namen verhandeln, sondern über Daten, Erreichbarkeit und Code.**

**Die Entscheidung und ihr Grund:** Staging ist überflüssig. Der Langzeittest der Software ist
die tägliche Nutzung von `sharefyx-mcp` selbst; eine zweite Instanz, die niemand aufruft, testet
nichts. Dazu kam die harte Randbedingung: die Hauptzugriffsrechner sind **Arbeitsrechner**, auf
denen weder Tailscale installiert noch die Netzwerkkonfiguration geändert werden darf. Ein
tailnet-only-Staging ist dort strukturell unerreichbar, und die VM nimmt hinter CGNAT auch keine
SSH-Verbindung für einen Tunnel an. Es blieb nur „öffentlich per Funnel" — und eine zweite
öffentliche Fläche für eine Instanz, die ihren Zweck ohnehin nicht erfüllt, ist ein schlechtes
Geschäft.

**Zwei eigene Funde, die diese Entscheidung mitgetragen haben:**
1. **Staging konnte seinen Zweck gar nicht erfüllen** — Konstruktionsfehler meinerseits: die
   Unit-Vorlage hat **einen** `__REPO_ROOT__`-Platzhalter, den beide Instanzen erben. Belegt über
   `systemctl show`: beide `ExecStart` zeigen auf `/opt/sharefyx/current`. Staging konnte damit
   andere *Daten* fahren, aber nie anderen *Code* — und „eine Änderung ausprobieren, bevor sie
   live geht" war der Zweck laut Plan. Ein echtes Staging bräuchte einen eigenen Symlink
   (`/opt/sharefyx/staging`) und ein Ziel-Argument in `deploy.sh`.
2. Dadurch war meine erste Risikoeinschätzung („Funnel auf Staging setzt ungetesteten Code aus")
   **für den heutigen Zustand zu streng** — es lief dieselbe Software. Für den Zustand, den
   Staging haben *sollte*, war sie richtig. Beides dem Nikinger vorgelegt statt eine Empfehlung
   stehenzulassen, deren Grundlage sich geändert hatte.

**Was bleibt und warum:** Unit, Skripte, Platzhalter und die vier Tests bleiben **im Repo**. Sie
sind gebaut, getestet und dokumentiert; abgeschaltet ist die *Inbetriebnahme*, nicht der Code.
Sobald ein Rechner existiert, der ins Tailnet darf, ist Staging ein `install_units.sh` +
`systemctl enable --now` + `tailscale serve` entfernt — **plus** der Release-Fix aus Fund 1, sonst
fährt es wieder dieselbe Software wie Produktiv. Das steht hier, damit niemand später eine
funktionierende Unit findet und annimmt, sie sei einsatzbereit.

**Manuell (Nikinger — alles, was Realität berührt):**
1. **Einmalig:** `sudo mkdir -p /opt/sharefyx/releases && sudo chown -R savefyx:savefyx /opt/sharefyx`
2. Erster Deploy aus dem Arbeitsverzeichnis:
   `SHAREFYX_RELEASES_DIR=/opt/sharefyx/releases SHAREFYX_CURRENT_LINK=/opt/sharefyx/current
   phase5_ui/scripts/deploy.sh main`
3. **Cutover:** `REPO_ROOT=/opt/sharefyx/current` und `VENV=/opt/sharefyx/current/.venv` in
   `phase3_edge/local.env`, dann `sudo phase3_edge/scripts/install_units.sh` + Restart.
   **Ab hier ist „Datei ändern + `systemctl restart`" wirkungslos** — es zählt nur noch, was
   deployt wurde. Escape-Hatch, falls nötig: den `current`-Symlink von Hand auf das
   Arbeitsverzeichnis zeigen lassen.
4. **Abnahmezeile 16:** Health-Endpunkt absichtlich unerreichbar machen (`SHAREFYX_PORT` auf
   einen toten Port), deployen, beobachten, dass automatisch zurückgerollt wird.
5. `sudo systemctl enable --now sharefyx-authbackup.timer`, danach `restore_auth_check.sh`
   **selbst ausführen** — der Nachweis ist der Lauf, nicht das Skript (Lehre aus P3 Zeile 13).
6. Staging hochziehen, `tailscale serve` prüfen — **V36:** nicht derselbe Port wie der Funnel.
   Achtung: Staging hat eine **eigene** `auth.sqlite3`, die Produktivkonten gelten dort nicht.
7. Unabhängig von Step 8 weiterhin offen: **Abnahmezeile 6** — zweiter Browser (privates
   Fenster/zweites Profil) angemeldet lassen, Passwort ändern, prüfen dass genau der abgemeldet
   wird und die aktuelle Sitzung weiterläuft.

**Nächster Schritt (konkret):** die sieben Punkte oben, dann Step 9 (gemeinsame Live-Abnahme
beider Nutzer + Handover, Plan §5 Step 9 / P5-AE).

## Session stopped — 2026-08-05, dritter Nachtrag (Step 7b: UI-Überarbeitung nach Live-Feedback)

**Ergebnis:** Der Nikinger hat Step 6/7 live benutzt und elf Punkte gemeldet; alle sind
umgesetzt, dazu sechs eigene Funde. Die Oberfläche hat jetzt einen Navigationsbaum statt zweier
flacher Rail-Blöcke, eine Übersichtsseite, plastische Bedienelemente, zwei farblich getrennte
Editor-Paneele, Rückmeldung nach jedem Schreibvorgang und gestaltete Auth-Seiten. Ausführungsplan
dieser Session: `/home/savefyx/.claude/plans/merry-tickling-elephant.md`.

**Zwei gelockte Entscheidungen revidiert — Nikinger-Entscheidung 2026-08-05, nicht still:**

| Gelockt | Bisher | Jetzt | Grund |
|---|---|---|---|
| **Plan §4.1** | „Keine Verläufe, keine Schlagschatten außer einem einzigen für Modale" | Verlauf + Innenhighlight + Kante + weicher Schatten auf Bedienelementen; eingelassene Eingabefelder | Die Zurücknahme führte live dazu, dass Knöpfe nicht als Knöpfe erkennbar waren. |
| **Plan §4.3** | Rail = zwei flache Blöcke (Spaces, Filter) | Rail = Baum (Übersicht · eigener Space ▸ Ordner · verbundene Spaces) + eigene Übersichtsseite | „Filter" sah aus wie eine zweite Top-Ebene neben „Spaces"; tatsächlich ist ein Filter immer an einen Space gebunden. Genau daher kam die Meldung „meine Notizen landen in *Notizen*, nicht in meinem Bereich". |

Unverändert bleiben: Farbtoken, Typografie (§4.2), Versionsband (§4.4), Fokusring und
120-ms-Bewegungsregel (§4.6), P5-U (kein WYSIWYG), P5-Y (kein serverseitiges Rendern), P5-W
(keine Mobilversion). `docs/concepts/phase5_ui_plan.md` bleibt als 📕-Snapshot **unverändert** —
dieselbe Handhabung wie beim §1.2-Widerspruch am 2026-08-03.

**Die elf Meldungen des Nikingers und was daraus wurde:**
1. *Keine Bestätigung beim Speichern* → Statuszeile `#toast` (§4.5 sah sie schon für „Dienst nicht
   erreichbar" vor) nach jedem Schreibvorgang, mit Versionsnummer: „Gespeichert · v11".
2. *Editor lässt sich nicht schließen* → `× Schließen` in der Kopfleiste, `Esc`, und die
   Übersicht-Schaltfläche; bei ungespeicherten Änderungen erst eine Rückfrage.
3. *Undurchsichtig, wo was hinkommt* → zwei beschriftete Paneele mit **verschiedenen Farben**:
   „Text (Markdown)" kühl (`--panel-body`), „Kopfdaten (YAML-Frontmatter)" warm (`--panel-meta`),
   zugeklappt vorbelegt (`<details>`, klappt also auch ohne JS) mit Zusammenfassungszeile und dem
   Hinweis, dass diese Felder in der Regel ein verbundenes Claude pflegt.
4. *„Ich kann in Fabis Space anlegen"* → **echter Fund, UI-seitig.** Der Server war immer korrekt
   (`_items_post()` liest nie ein `space` aus dem Body, P5-A), aber die UI zeigte „+" und „Erste
   Notiz anlegen" auch im fremden Space. Jetzt: Nur-lesen-Balken über der Liste, und die
   Bedienelemente werden **aus dem DOM ausgehängt** (siehe eigener Fund 7 unten).
5. *Eigene Notizen landen „in Notizen"* → strukturell durch den Baum gelöst; zusätzlich springt
   der aktive Ordner nach dem Anlegen dorthin, wo das neue Item tatsächlich liegt.
6. *UI-Umbau (Übersicht + Spaces als Überordner)* → umgesetzt, `GET /api/v1/overview` speist
   Kacheln, „Zuletzt benutzt" und die Zähler-Plaketten im Baum.
7. *Zu wenig Reaktion* → Toasts, Zähler im Baum nach jedem Schreibvorgang aktualisiert, aktiver
   Pfad sichtbar, „Speichern" deaktiviert wenn es nichts zu speichern gibt.
8. *Login-Seite unverändert* → alle sechs Seiten aus `pages.py` tragen jetzt die Karte
   `.auth`/`.auth-card`. **Ursache war nicht Faulheit, sondern eine Lücke:** die Seiten luden
   `app.css`, benutzten daraus aber keine einzige Klasse — ein Stylesheet-Link ohne Markup sieht
   im Diff nach Gestaltung aus und ist keine. `test_pages_markup.py` hält das jetzt fest.
9. *3D/Skeuomorphismus* → siehe Revision §4.1 oben.
10. *Verschiedene Farben für Text- und YAML-Feld* → siehe Punkt 3.
11. *Obsidian-artige Graph-Ansicht* → **Nikinger-Entscheidung: zurückgestellt.** Die Übersicht
    ist so gebaut, dass sie später als weitere Kachel eingehängt werden kann.

**Sechs eigene Funde (F1–F6), alle behoben:**
- **F1** `render_enrollment_page()` setzte den weißen QR-Hintergrund per `style="…"` — `security.py`
  sendet `style-src 'self'` **ohne** `unsafe-inline`, das blockiert auch Style-Attribute. Die
  Regel griff also nie: ein Fix, der wie einer aussah. Jetzt `class="qr-frame"`, mit Test.
- **F2** `window.alert`/`window.confirm` an fünf Stellen → eigener `#confirm-dialog` und Toasts.
- **F3** Nach dem Archivieren blieb das Item im Editor stehen, obwohl es aus der Liste
  verschwunden war → Editor schließt sich, Toast bestätigt.
- **F4** Der Leerzustand sagte immer „Keine Notizen in diesem Space", auch bei einer Suche ohne
  Treffer → drei unterschiedene Zustände (§4.5 verlangt das ausdrücklich).
- **F5** Filter-Chips wurden nur im Leerzustand gerendert und waren nicht entfernbar; `.chip__remove`
  war totes CSS → Such-Chip immer sichtbar und entfernbar.
- **F6** „Speichern" war immer aktiv → **das ist die Ursache des `v10`-Erlebnisses**, nicht nur die
  fehlende Bestätigung. Ohne echte Änderung ist der Knopf jetzt deaktiviert (und sieht auch so aus).
- **F7 — Advisor-Fund vor dem Commit, der schwerwiegendste der Session (Vorbestand aus Step 7).**
  Alle drei Schreibpfade adressierten das Item über `state.selectedId`, nahmen die Version aber aus
  `state.editingSnapshot`. `selectItem()` setzt `selectedId` **sofort**, `editingSnapshot` erst
  wenn die Antwort da ist — dazwischen liegt ein Fenster, in dem beide zu verschiedenen Items
  gehören. Ein `Strg+S` in diesem Moment schriebe den Inhalt von Item A unter der Kennung von Item
  B, und wenn beide Versionen zufällig gleich sind, **ohne Konflikt**: ein stiller Überschreiber,
  genau das, was Hard Rule 3 verbietet — nur clientseitig herbeigeführt, wo der Server nichts
  merken kann. Ein zweiter Pfad kam **erst durch Step 7b** hinzu: über „Zuletzt benutzt" lässt sich
  ein fremdes Item öffnen, ohne den Editor vorher zu verlassen; `showReadonlyItem()` hängte den
  Editor zwar aus, setzte aber weder `detailEditorEl.hidden = true` noch
  `state.editingSnapshot = null` — und `hidden` überlebt das Aushängen, der `Strg+S`-Wächter blieb
  also scharf. Behoben: alle drei Schreibaufrufe adressieren über `state.editingSnapshot.id`
  (Kennung und Version stammen damit beweisbar aus demselben Lesevorgang), plus die zwei fehlenden
  Zeilen in `showReadonlyItem()`. **Gegenprobe gefahren, nicht nur behauptet:** die jsdom-Prüfung
  „Strg+S bei offenem fremden Item schreibt nicht" wurde gegen eine Kopie mit zurückgenommenem Fix
  laufen gelassen — dort **ein** Schreibaufruf, mit Fix **null**.

**Zwei Funde, die über die Meldungen hinausgehen:**
- **Vierter Ordner „Erledigt".** Die drei Ordner des Mockups decken `STATUS_VALUES["task"]` nicht
  ab: eine auf `done` gesetzte Aufgabe fiel durch alle drei und war in der Oberfläche nirgends
  mehr auffindbar, bis jemand sie archivierte. `_BUCKETS` hat jetzt vier Einträge; ein Test hält
  fest, dass jeder Zähler exakt so viele Items meint, wie die Liste beim Klick zeigt.
- **Akzeptanzkriterium 12 war bisher nur halb erfüllt.** Der Step-7-Session-Block behauptet, für
  fremde Items würden „keine Editor-Elemente überhaupt gerendert" — tatsächlich standen Editor,
  „+"-Knopf und Anlegen-Dialog permanent in `app.html` und waren nur `hidden`, mit DevTools also
  auffindbar. Kriterium 12 sagt wörtlich „**ohne** Schreib-Bedienelemente **im DOM**". `app.js ::
  detachable()` hängt diese drei Teilbäume jetzt wirklich aus dem Dokument aus und später wieder
  ein; die jsdom-Simulation prüft beide Richtungen. **Korrektur an der Step-7-Zeile der
  Modultabelle, nicht am Step-7-Block selbst** (der ist rotiert und bleibt verbatim).

**Neuer Endpunkt `GET /api/v1/overview`** (wie `/api/v1/meta` in Step 7 in keiner Plan-Routentabelle):
je sichtbarem Space die vier Bucket-Zähler und die fünf zuletzt geänderten Items. Die Arbeit liegt
bewusst serverseitig — der Plan lässt JavaScript ungetestet, Python nicht. Kein LLM, keine Deutung,
nur Zählen und Sortieren; das Kernprinzip „der Server ist dumm" bleibt gewahrt. `GET /api/v1/meta`
gibt zusätzlich `buckets` heraus, damit `app.js` das Ordnervokabular nicht ein zweites Mal
definiert. `recent` trägt **kein** `snippet`: die Übersicht ist die erste Fläche, die mehrere
Spaces nebeneinander zeigt, ohne dass man bewusst „in einen fremden Space gewechselt" ist — dort
gehört fremder Fließtext nicht hin (Rule 4 dem Geiste nach). **Nebenwirkung, damit sie niemand
sucht:** `GET /api/v1/spaces` hat damit keinen Aufrufer mehr in `app.js` (`init()` geht
`/me` → `/meta` → `/overview`; `/overview` liefert die Space-Liste mit). Der Endpunkt bleibt —
er ist Teil des §3.1-Vertrags und weiterhin getestet, nur eben nicht mehr von der eigenen
Oberfläche benutzt.

**Verifiziert:** `pytest -q` (Repo-Wurzel) → **549/549 grün** (516 vorher, +33: 7 `test_overview.py`
+ 24 `test_pages_markup.py` (3 Aussagen × 8 Seiten) + 1 `test_meta.py` + 1 `test_static_routes.py`).
`pyflakes` sauber, `node --check app.js` sauber. `scripts/ui_smoke.py` → **12/12** (die
Seed-Suchregex musste auf das neue Klassen-Markup nachgezogen werden, gleiche Anpassung wie in
`test_invite_enroll.py` — beide Stellen mit datierter Notiz). `git diff --stat` auf `storage/`,
`mcpserver/tools.py`/`permissions.py`/`server.py` bleibt **leer** (Akzeptanzkriterium 18). Eine
Node/jsdom-Simulation im Scratchpad (nichts davon im Repo) fuhr **53 Prüfungen** über den vollen
Lebenszyklus — Baum, Übersicht, Anlegen mit Ordnersprung, Dirty-Gating (belegt: drei Klicks auf
„Speichern" ohne Änderung erzeugen **einen** `PATCH`, nicht drei), Vorschau, Anhängen, Konflikt,
Schließen mit und ohne Änderungen, fremder Space (fünf Prüfungen auf „nicht im DOM" plus die zwei
F7-Prüfungen), Suche mit Chip, Archivieren, Passwortdialog inklusive CSRF-Rotation,
Sitzungsablauf — alle grün. Ein Fehlschlag darin war ein Fehler der Simulation selbst
(`getElementById` auf einem korrekt ausgehängten Knoten), kein `app.js`-Fund.

**Advisor:** beim ersten Versuch (vor dem Bauen) nicht erreichbar („temporarily overloaded",
dasselbe Bild wie in der Step-6/7-Session), beim Review **vor dem Commit** dann erreichbar — und
er fand mit **F7** den schwerwiegendsten Fehler der Session, den weder `pytest` noch die
jsdom-Simulation in ihrer damaligen Fassung erreicht hatten (die Simulation prüfte
DOM-Anwesenheit, betrat aber nie den Zustand „eigenes Item mit lebendem `editingSnapshot` →
fremdes Item öffnen"). Zwei kleinere Advisor-Punkte ebenfalls übernommen: die Größenangabe für
Root-`CLAUDE.md` in `docs/INDEX.md` (26 → 32 KB — genau die Drift-Kategorie, die diese Datei
schon fünfmal getroffen hat) und der Hinweis, dass `/api/v1/spaces` keinen UI-Aufrufer mehr hat.

**Manuell (Nikinger, nicht Teil dieses Steps):**
- `sudo phase3_edge/scripts/install_units.sh && sudo systemctl restart sharefyx-mcp` — **Schritt
  null**, sonst liefert der Dienst weiter den alten Build.
- Sichtprüfung im echten Browser (Layout/Fokus/Tastatur verhalten sich in jsdom nicht identisch
  zu Chrome): Übersicht, Baum, plastische Bedienelemente, die zwei Panelfarben, Login-Seite.
- Fremder Space in DevTools: **kein** Schreib-Bedienelement im DOM (Akzeptanzkriterium 12).
- **Block-A-Abnahmezeilen 5 und 6** sind jetzt ohne DevTools-Behelf testbar: `⚙ Konto` →
  Passwort ändern ohne `systemctl restart`, neuer Login sofort gültig (Zeile 5); danach fordert
  der Connector neue Autorisierung, eine zweite UI-Sitzung ist beendet, die aktuelle läuft weiter
  (Zeile 6).

**Nächster Schritt (konkret):** Zeilen 5/6 live abnehmen (siehe oben), danach Step 8 (Betrieb:
Deploy, Rollback, Staging, Auth-Backup, Messung — Plan §5 Step 8).

---

## Session stopped — 2026-08-05, zweiter Nachtrag (Step 7: Editor, Vorschau, Konflikt, Frontmatter-Felder)

**Ergebnis:** Step 7 ist fertig — die Detail-Spalte ist jetzt ein echter Editor statt einer
Leseansicht. Anlegen (kleines Inline-Formular, Typ+Titel), Bearbeiten mit Markdown-Vorschau,
Anhängen (eigener API-Pfad, kein PATCH-Umweg), Archivieren, Frontmatter-Felder (Titel/Status/
Fällig/Tags/Links, Status-Vokabular aus dem neuen `GET /api/v1/meta` statt in der UI dupliziert),
Versionsband (§4.4, drei Zustände: Ruhe/ungespeichert/Konflikt), Konfliktdialog mit den zwei
Optionen aus §4.5 (kein Auto-Merge), Entwurfsschutz über `sessionStorage`, „Sitzung
abgelaufen"-Karte statt totem Redirect. Fremde Items bleiben strikt lesend (eigener Vorschau-
Zweig, keine Editor-Elemente werden für sie überhaupt gerendert — Akzeptanzkriterium 12).

**Harvest aus `docs/concepts/notiz_heft_example.html`** (vom Nikinger bereitgestellt, vorher
nicht zugänglich — siehe vorherige Rückfrage in dieser Session): `sanitizeHtml()`/
`markdownToHtml()`/`safeHref()` als Ausgangspunkt übernommen und erweitert (h1–h4 statt nur
h1–h3, Zitate und GFM-Tabellen neu — beides hatte die Quelle nicht), `.rich-editor`s
Formensprache für Zitat/Code/Tabelle/HR auf unsere Tokens umgesetzt. Bewusst NICHT übernommen:
`sanitizeStyle()`/Style-Attribute (unsere `style-src 'self'`-CSP ohne `unsafe-inline` verhindert
ohnehin, dass ein `style="..."` je greift), IMG/FIGURE/FONT/`data-asset-*` (kein Anhang-Feature,
P5-AA), Task-Checklisten (nicht in §3.5s Markdown-Teilmenge), `tel:`/`#note:`/`#asset:` (§3.5
nennt nur `http:`/`https:`/`mailto:`/`#item/<id>`). Die Symbolleiste selbst ist dort
`document.execCommand` gegen ein `contenteditable`-Feld (WYSIWYG) — P5-U verbietet das
ausdrücklich; übernommen wurde nur die Idee einer Leiste über dem Editor, die Buttons fügen hier
Markdown-Syntax in die `<textarea>` ein.

**Zwei Plan-Lücken/-Abweichungen, dokumentiert:**
1. `GET /api/v1/meta` (neu) taucht in keiner Routentabelle des Plans auf, wird aber von Step 7s
   eigenem Testnamen verlangt — session-gated, liefert `{"status_values": {...}}` direkt aus
   `storage.models.STATUS_VALUES`.
2. CSRF-Token-Übergabe/Sitzungsablauf-UX waren im Plan nicht spezifiziert — mit dem Nikinger vor
   dem Bauen geklärt (AskUserQuestion, siehe Plan-Datei dieser Session): „Sitzung
   abgelaufen"-Wiederanmeldung per Link zurück zu `/ui/login` (keine zweite Login-Implementierung,
   der Bootstrap-Redirect nach `/ui/` bringt den Entwurf über `sessionStorage` mit zurück);
   „Anlegen" als kleines Inline-Formular statt eines sofortigen Blanko-Items.

**Advisor war während der GESAMTEN Session (Block-A-Gate-Fortsetzung UND Step 6 UND Step 7)
nicht erreichbar** („temporarily overloaded", mehrfach erneut versucht). Ersatz — diesmal über
den bisherigen Fallback (pyflakes + `pytest`) hinaus zusätzlich verschärft: eine echte,
verhaltensgetriebene Node/jsdom-Simulation von `app.js` gegen die realen `app.html`/`app.css`-
Dateien (im Scratchpad, nichts davon im Repo — `jsdom` ist kein Projekt-Dependency, P5-T/„kein
Node im Projekt" bleibt unberührt). Diese Simulation fuhr den kompletten Lebenszyklus
(Init→Anlegen→Bearbeiten→Vorschau→Speichern→Anhängen→Konflikt→Auflösen→Archivieren), den
Nur-lesen-Pfad für fremde Items, die Tastaturkürzel und den Entwurfsschutz — und fand dabei zwei
echte Funde vor dem Commit:
1. Das Test-Mock selbst hatte einen `String.includes()`-Bug (`"/api/v1/meta".includes("/me")`
   ist `true`, weil `/meta` mit `/me` beginnt) — reiner Test-Harness-Fehler, kein `app.js`-Bug,
   aber ohne die Simulation nicht aufgefallen.
2. Beim Beheben davon zeigte sich ein echter `app.js`-Fund: `loadItems()`/`selectItem()`/
   `init()` hatten kein `.catch()` — ein `401` mitten in einer Suche hinterließ eine unbehandelte
   Promise-Ablehnung. Im Browser nur eine Konsolenwarnung (die „Sitzung abgelaufen"-Karte
   erscheint trotzdem, das passiert synchron in `api()` vor dem Verwerfen), in Node bricht das
   den Prozess ab — der Unterschied machte den Fund erst in der Simulation sichtbar. Behoben:
   neues `reportUnexpectedError()`, an allen drei „lose angestoßenen" Aufrufstellen als
   `.catch()` ergänzt (die vier nutzergetriebenen Aktionen Speichern/Anhängen/Archivieren/
   Anlegen hatten von Anfang an eigene Fehlerbehandlung).

**Verifiziert:** `pytest -q` (Repo-Wurzel) → **516/516 grün** (512 vor diesem Step, +4: 2
`test_meta.py`, neue Datei + 2 `test_api.py`). `pyflakes` über alle neuen/geänderten
Python-Dateien sauber. `git diff --stat` auf `storage/`, `mcpserver/tools.py`/`permissions.py`/
`server.py` bleibt leer (Akzeptanzkriterium §6.18). `node --check` auf `app.js` sauber. Die
jsdom-Simulation (siehe oben) deckte praktisch die komplette Interaktionsfläche ab, ist aber
ausdrücklich kein Ersatz für einen echten Browser — Layout/Fokus-Reihenfolge/Tastatur-Events
verhalten sich in jsdom nicht immer identisch zu Chrome.

**Import aus „Notepad Pro Local" — vom Nikinger angefragt, eingeschätzt, noch nicht begonnen:**
machbar als einmaliges Skript (kein eigener Phasen-Aufwand), aber mit echtem Verlust bei Bildern
(kein Anhang-Feature, P5-AA) und einer offenen Designfrage bei eingebetteten Aufgaben-Checklisten
(Notizheft kennt keine eigenständigen Aufgaben-Objekte). Details/Aufwandsschätzung: Plan-Datei
dieser Session (`/home/savefyx/.claude/plans/magical-stirring-meerkat.md`, Abschnitt „Import aus
Notepad Pro Local"). Wartet auf eine Nikinger-Entscheidung, ob die echten Notizen Bilder
enthalten, bevor der Umfang feststeht.

**Manuell (Nikinger, nicht Teil dieses Steps):** das eigentliche Step-7-„Done when" — anlegen →
bearbeiten (Vorschau sichtprüfen) → Konflikt mit einem zweiten Tab provozieren → auflösen →
archivieren, in einem echten Browser gegen eine Wegwerf- oder die Live-Instanz.

**Nächster Schritt (konkret):** Step 8 (Betrieb: Deploy, Rollback, Staging, Auth-Backup, Messung
— Plan §5 Step 8) ODER zuerst ein kleiner Nachtrag für die Block-A-Abnahmezeilen 5/6
(Passwortwechsel-Dialog gegen `/api/v1/account/password`, jetzt technisch möglich — die
Editor-Infrastruktur aus diesem Step liefert Dialog-/Overlay-/Formular-Muster, die sich direkt
wiederverwenden lassen). Reihenfolge ist eine Nikinger-Entscheidung, keine im Plan gelockte.


## Session stopped — 2026-08-05 (Step 6: UI-Gerüst — Shell, Tokens, Navigation, Liste, Suche)

**Ergebnis:** Step 6 ist fertig — `GET /ui/` liefert erstmals die echte App-Shell
(`webui/static/{app.html,app.css,app.js}`) statt der Step-3-Übergangsseite, verdrahtet gegen
`/api/v1/{me,spaces,items,items/{id}}` aus Step 5. Bewusst **kein** Editor, **kein**
Markdown-Rendering (§3.5), **kein** Versionsband (§4.4), **kein** Konfliktdialog — das ist
wörtlich Step 7s Aufgabenliste, nicht vorgezogen.

**Korrektur zu Plan §1.5s Routentabelle, vor dem Bau entschieden (nicht erst live gefunden):**
die Tabelle trägt für `/ui/` in der Auth-Spalte „keine" ein, aber derselbe Plan-Abschnitt (§5
Step 6) verlangt im selben Atemzug einen Test namens `test_index_route_requires_session` — ein
direkter Widerspruch innerhalb desselben 📕-Dokuments, dieselbe Kategorie wie der
`mcpserver→webui`-Zirkel aus P5 Step 4 (dort ebenfalls zugunsten des konkreteren Textes gegen
eine Ableitungstabelle aufgelöst, siehe `SESSIONS_ARCHIVE.md`). Aufgelöst zugunsten des
Testnamens: `GET /ui/` ohne gültige Sitzung → `303` nach `/ui/login` (`webui/static_routes.py ::
_index()`), mit Sitzung → `200` mit `app.html`. Dem Nikinger nicht vorab zur Entscheidung
vorgelegt (anders als der Zirkel-Fund in P5 Step 4) — die Kategorie ist dieselbe, aber die
Auflösung war hier eindeutig genug (ein Tabellen-Zellwert gegen einen explizit benannten Test im
selben Abschnitt), um sie als „kleine Drift" statt „entscheidungsbedürftig" einzustufen (Root-
`CLAUDE.md`: „kleine Drift selbst fixen und datiert vermerken; wenn nicht klein, stoppen und
fragen"). Wird hier vermerkt, nicht still verschwiegen.

**CSRF-Token-Übergabe an die Shell (im Plan nicht spezifiziert):** `SessionManager.rotate()`
gibt den CSRF-Token nur EIN einziges Mal als Klartext zurück (`ui_sessions` speichert nur den
Hash) — der Plan sagt nirgends, wie `app.js` daran kommt. Lösung: die seit Step 3 bestehende
Login-Erfolgsseite (`pages.py :: render_logged_in_page()`) behält ihr `<input type="hidden"
name="csrf" value="...">` unverändert und bekommt zusätzlich `<script src="/ui/static/app.js"
defer>`. `app.js`s Bootstrap-Teil (läuft auf JEDER `/ui/*`-Seite, erkennt sich selbst an
`document.getElementById('shell')`s Fehlen) liest das Feld aus, legt den Wert in
`sessionStorage['sfx:csrf']` ab (kein `localStorage` — konsistent mit dem in §4.5 bereits
gelockten Entwurfsschutz-Muster) und leitet per `location.replace('/ui/')` weiter. Ein `401
unauthenticated` von irgendeinem API-Aufruf schickt in Step 6 schlicht zu `/ui/login` zurück —
kein Entwurfsschutz nötig, es gibt in Step 6 noch nichts Eingetipptes zu verlieren; Step 7 baut
dafür die volle „Sitzung abgelaufen"-Karte aus §4.5, sobald der Editor existiert. Logout bleibt
ohne JavaScript funktionsfähig (das Formular aus Step 3 ist unverändert), `app.js` ergänzt nur
einen bequemeren Weg (`fetch('/ui/logout', ...)` mit dem CSRF-Header statt Formular-Submit).

**Font (V27 im VERIFY-Register, hier geschlossen statt auf Systemstack ausgewichen):**
`phase5_ui/scripts/build_font_subset.sh` (neu) lädt Inter Variable v4.1
(`github.com/rsms/inter`, OFL-1.1, SHA256-geprüft), pinnt die optische Größe auf Textgröße
(`opsz=14` — die einzige, die diese UI benutzt) und beschneidet die Gewichtsachse auf `380:620`
(deckt 400/500/600 aus Plan §4.2 mit Marge ab), subsetzt danach auf den
Google-Fonts-„latin"-Unicodebereich (deckt deutsche Umlaute/ß über Latin-1 Supplement ab) plus
`tnum/lnum/pnum/kern/liga/calt`. Ergebnis: **34,7 KB** (Ziel < 120 KB), variable Gewichtsachse
erhalten (`fvar: wght 380–620`), alle deutschen Sonderzeichen + `€` im `cmap` geprüft. Datei
trägt einen Kurzhash des Inhalts (`InterVariable-subset.2fa9d1dc.woff2`) — macht sie zu einem
echten „gehashten Asset" für `static_routes.py`s Cache-Header-Regel (unten), nicht nur einem
hypothetischen Fall. `LICENSE.txt` liegt unverändert als `webui/static/fonts/OFL.txt` daneben.
**Reproduzierbarkeit ist nicht Bit-Identität:** ein erneuter Lauf des Skripts kann eine andere
Hex-Prüfsumme erzeugen (der `head`-Tabellen-Zeitstempel in TTF/WOFF2 ist nicht deterministisch
über Compiler-Läufe hinweg) — das ist bei einem content-hashed Dateinamen erwartet und
unschädlich, verlangt aber bei jedem Font-Rebuild eine manuelle Ein-Zeilen-Anpassung der
`@font-face`-`src`-URL in `app.css`.

**Cache-Header-Regel (§3.4 „`no-store` außer für `/ui/static` mit gehashtem Namen"):**
`static_routes.py :: _HASHED_NAME_RE` erkennt einen Kurzhash unmittelbar vor der Dateiendung
(Punkt- oder Bindestrich-getrennt) — nur solche Dateien bekommen `public, max-age=31536000,
immutable`. `app.html`/`app.css`/`app.js` tragen bewusst KEINEN Hash (kein Build-Step, P5-T —
sie werden von Hand editiert; ein `immutable`-Cache auf einem unveränderten Dateinamen wäre nach
der nächsten Änderung ein tagelang stiller Bug) und bekommen `no-store`.

**Scope innerhalb der Shell:** Rail (Spaces + Filter „Offen"/„Notizen"/„Archiv" + Logout),
Liste (Suchfeld mit 200ms-Debounce, `↑`/`↓`-Navigation, `/`-Fokus-Shortcut), Detail
(schreibgeschützte Ansicht: Titel/Status/Fällig/Tags/Version, Rohtext in `<pre>`, sichtbare
„Nur lesen"-Kennzeichnung bei `item.readonly` — erfüllt den Geist von Akzeptanzkriterium 12
schon jetzt, auch wenn die Live-Abnahme erst mit einem echten Editor in Step 7 sinnvoll ist).
Rail-Kollaps ≤1280px und Liste-hinter-Zurück-Navigation <1024px (§4.3) sind gebaut, größtenteils
reines CSS, ein `data-view`-Attribut auf `#shell` für die eine JS-Umschaltung. `Esc`/`Ctrl+S`
bewusst NICHT gebunden (kein Dialog zu schließen, nichts zu speichern in Step 6) — im Code
kommentiert, warum sie fehlen, statt sie tot zu binden.

**Verifiziert:** `pytest -q` (Repo-Wurzel) → **512/512 grün** (504 vor diesem Step, +8: 7
`test_static_routes.py`, neue Datei, + 1 `test_ui_index_route_reachable_through_create_app` in
`phase2_mcp/tests/test_app.py`; `app.js` bleibt laut Plan unit-ungetestet, kein Node im
Projekt). `pyflakes` über alle neuen/geänderten Python-Dateien sauber. `git diff --stat` auf
`storage/`, `mcpserver/tools.py`/`permissions.py`/`server.py` bleibt leer (Akzeptanzkriterium
§6.18). Zusätzlich ein manueller In-Process-Durchlauf (wie `ui_smoke.py`, kein echter Browser):
anonymer `GET /ui/` → `303`/`/ui/login`, Login → Bootstrap-Seite mit `<script>`-Tag, `GET /ui/`
mit Sitzung → `200`/`app.html`, `GET /ui/static/app.css` → `200`/`text/css`/`no-store`,
`GET /ui/static/does-not-exist.css` → `404`. **Advisor-Review vor diesem Commit war nicht
möglich** (Tool zweimal „temporarily overloaded" zurückgemeldet, wie schon beim Step-5-Nachtrag
— derselbe dokumentierte Ersatz, nicht übersprungen): `pyflakes`, voller `pytest -q`, der
manuelle In-Process-Durchlauf oben, Tabu-Pfad-Diff, alles vor dem Commit.

**Manuell (Nikinger, nicht Teil dieses Steps):** ein echter Browser-Blick auf `/ui/` gegen eine
Wegwerf-Instanz — Layout/Typografie/die 1280px-/1024px-Breakpoints lassen sich nicht aus
`pytest` beurteilen.

**Nächster Schritt (konkret):** Step 7 (Editor, Vorschau, Konflikt, Frontmatter-Felder — Plan
§3.5, §4.4, §4.5, P5-U). Baut auf der in Step 6 gelegten `app.js`-Struktur auf (State/Render-
Funktionen, API-Client mit `sessionStorage`-CSRF, bereits vorbereiteter `X-CSRF-Token`-Pfad für
Nicht-GET-Aufrufe). Ersetzt außerdem den einfachen `401`→`/ui/login`-Redirect aus Step 6 durch
die volle „Sitzung abgelaufen"-Karte samt Entwurfsschutz (§4.5), sobald es etwas Eingetipptes
gibt, das dabei verloren gehen könnte. Zeilen 5/6 der Block-A-Abnahme folgen weiterhin, sobald
ein echter Klick-Pfad für `/api/v1/account/password` existiert.

---

## Session stopped — 2026-08-05 (Block-A-Gate live gefahren — Origin-Bug gefunden und behoben, 7/9 Zeilen bestanden)

**Für den nächsten, kalten Leser — Kurzfassung, Details im 2026-08-03-Block in
`SESSIONS_ARCHIVE.md`:** diese Session begann mit einem vom Nikinger gemeldeten „TOTP-Seed
kaputt" beim Block-A-Gate. War kein TOTP-Bug — `journalctl` zeigte 100 % `403` auf jeden
`/ui/enroll/confirm`-Versuch, nie `422`, der Request erreichte die TOTP-Prüfung also nie.
Root Cause nach zwei widerlegten Zwischenhypothesen (eingebetteter Vorschau-Panel, dann
Browser-Extension — beide durch einen Test in sauberem Chrome-Inkognito ohne Extensions
widerlegt): `webui/security.py`s `Referrer-Policy: no-referrer` lässt die Fetch-Spec den
`Origin`-Header eines reinen HTML-`<form>`-POSTs (kein JavaScript) auf `null` setzen, auch bei
einer echten Same-Origin-Anfrage — `require_csrf()` lehnte das korrekt ab, der eigene Header
hatte sich selbst ausgesperrt. **Fix:** `Referrer-Policy` auf `strict-origin` (nullt nur bei
TLS-Downgrade, sendet nie den Pfad — bewusst nicht `same-origin`, das würde
`/ui/invite/<token>`s Einmal-Secret über `Referer` preisgeben). Live bestätigt, nicht nur
behauptet: Prozess-Neustart-Zeitstempel gegen die erste erfolgreiche `200`-Antwort auf
`/ui/enroll/confirm` read-only gegengeprüft. `authserver/routes.py`s identischer
`no-referrer`-Wert für die OAuth-Seiten bewusst nicht mitgeändert (anderer Flow, eigener,
unbehobener Befund).

**Block-A-Abnahmematrix (§6) durchgefahren:** Zeilen 1, 2, 3, 4, 7, 8, 9 live bestanden (Details
je Zeile im archivierten Block). Zeile 9 (`strings`-Grep gegen `auth.sqlite3`) vom
Auto-Mode-Classifier für Claude Code blockiert (Rohzugriff auf echte Secrets — dieselbe
Kategorie, die laut Root-`CLAUDE.md` dem Nikinger vorbehalten ist), vom Nikinger selbst
gegengeprüft: leer, kein Klartext-Seed. **Zeilen 5/6 (Passwortwechsel ohne Restart,
Session-/Connector-Widerruf danach) bewusst zurückgestellt, keine stille Ersatzlösung:** Step 4
baute dafür nur die JSON-API (`/api/v1/account/*`), keine HTML-Seite — die App-Shell ist
Step-5/6-Scope, der nach diesem Gate liegt. Ein DevTools-`fetch()`-Behelf wurde angeboten und
vom Nikinger ausdrücklich abgelehnt: „das ist ein Workaround, kein echter Test." Nikinger-
Entscheidung: 5/6 folgen mit einem echten Klick-Pfad, sobald der existiert.

**Verifiziert:** `pytest -q` (Repo-Wurzel) → **473/473 grün**. `git diff --stat` auf
`storage/`, `mcpserver/tools.py`/`permissions.py`/`server.py` bleibt leer (Akzeptanzkriterium
§6.18). Zwei kleine, unabhängige Kosmetik-Funde notiert, nicht behoben: `render_enrollment_page()`s
inline `style`-Attribut wird von der eigenen `style-src 'self'`-CSP blockiert (kosmetisch, QR
bleibt scanbar); `_PAGE`s `<link rel="stylesheet" href="/ui/static/app.css">` 404et auf jeder
UI-Seite (erwartet, `static_dir` ist Step-5/6-Scope).

**Block A (§6) damit vollständig bis auf die bewusst verschobenen Zeilen 5/6.** Der harte Gate
vor Block B gilt für die sieben live bestandenen Zeilen als erfüllt.

**Nachtrag, später am selben Tag — Step 5 (REST-API v1) abgeschlossen:** `webui/serializers.py`
(neu — `item_to_json`/`summary_to_json`/`search_to_json`/`space_to_json`, Plan §3.2) und
`webui/api.py` (neu — `/api/v1/{me,spaces,items,items/{id},items/{id}/append,
items/{id}/archive}`, Plan §3.1/§3.3) gebaut, `mcpserver/app.py :: create_app()` mountet
`api_routes(ui_settings, store, ui_sessions, own_space_writable)` — der `store`-Parameter war
bereits vorhanden (bediente bisher nur `build_mcp()`), kein neuer `create_app()`-Parameter nötig,
anders als in der vorigen Notiz erwartet. `OwnSpaceWritable()` läuft jetzt als eine geteilte
Instanz (`own_space_writable`) für MCP-Tools UND REST-API statt zweier getrennter.

**Reihenfolge `space_of()` → Rechteprüfung → Store-Aufruf** (Plan §3.3, „nicht verhandelbar")
wörtlich aus `mcpserver/tools.py` übernommen, nicht neu erfunden — dieselbe Begründung (Rule 4:
ein Rechtefehler darf den Store nie erreichen, `space_of()` ist index-only und deshalb sicher
auch für einen Space, auf den kein Zugriff besteht). Zwei Tests
(`test_space_of_is_called_before_permission_check`,
`test_patch_foreign_item_is_403_and_never_reaches_store`) laufen bewusst gegen einen
`unittest.mock.MagicMock(spec=Store)`, nicht den echten `Store` — mit `OwnSpaceWritable.can_read`
(heute immer `True`) hätte ein echter Store beide Tests vacuous bestehen lassen, ohne die
Aufrufreihenfolge tatsächlich zu belegen.

**Eigener Fund, nicht in der Plan-Testliste:** `storage.store.Store.archive()` hat anders als
`update()`/`append()` keinen Schutz gegen ein bereits archiviertes Item (`storage/` ist für diese
Phase tabu, P5-B — ein Fix dort wäre eine Scope-Änderung). `POST /api/v1/items/{id}/archive`
holt deshalb NACH der Rechteprüfung (sicher, eigener Space) einmal den aktuellen Stand per
`store.get()` und lehnt ein zweites Archivieren mit `422 validation_failed` ab, statt die Version
bei jedem Klick stillschweigend hochzuzählen. Zweiter kleiner Fund: `storage.store._coerce_due()`
wirft bei einem falsch formatierten `due`-String ein rohes `ValueError`
(`date.fromisoformat`), keine `ValidationError` — `api.py :: _map_store_error()` fängt beide
Typen gleich ab (422), damit ein API-Client nicht zwei verschiedene Fehlerformen für denselben
Fehlerfall sieht.

**`/api/v1/spaces`** wiederholt bewusst den B1-Fix aus P2 (`tools.py :: list_spaces()`): ein
eigener Space ohne ein einziges Item taucht in `Store.list_spaces()` sonst gar nicht auf — die
Sichtbarkeitsprüfung läuft dabei aus der (ggf. ergänzten) lokalen Liste, nicht aus einem zweiten,
frischen `store.list_spaces()`-Aufruf (Advisor-artiger Selbstfund beim Testen: ein frischer
Aufruf hätte den synthetisierten leeren eigenen Space nie als sichtbar erkannt).

**Suche (`GET /api/v1/items`):** Filterparameter (`query`/`space`/`type`/`status`/`tag`/
`due_before`) wandern unverändert an `Store.search()`; `limit`/`offset` NICHT direkt — `Store`
kennt keine Menge „sichtbarer Spaces", nur einen einzelnen `space`-Filter. Diese Datei holt bis
zu einer eigenen `_STORE_FETCH_LIMIT=5000`-Konstante (Kostenabwägung wie `tools.py`s
gleichnamiger Wert, hier erneut definiert statt importiert — ein Import aus `mcpserver.tools`
wäre ein zweites `mcpserver`-Symbol, P5-B erlaubt nur `OwnSpaceWritable`), filtert nach
sichtbaren Spaces und paginiert danach selbst — sonst würden `total`/`offset` verfälscht, sobald
ein unsichtbarer Space existierte.

**`scripts/ui_smoke.py`** (neu, Gegenstück zu `mcp_smoke.py`/`oauth_smoke.py`): temporäres
`DATA_ROOT` + temporäre `AuthStore`, In-Process (`httpx.ASGITransport`, kein Port, kein Netz,
kein `--base-url`-Modus — Step 5s Done-when verlangt nur den In-Process-Lauf). Fährt Einladung →
TOTP-Enrollment → Login → `/api/v1/me`/`/spaces` → Item anlegen/lesen/ändern/anhängen/
archivieren → Versionskonflikt → fremder Space (readonly) einmal vollständig durch. **12/12
Prüfungen grün**, lokal ausgeführt.

**Verifiziert:** `pytest -q` (Repo-Wurzel) → **504/504 grün** (473 vor diesem Nachtrag, +31: 23
`test_api.py` + 7 `test_serializers.py`, zwei neue Testdateien, + 1
`test_api_items_reachable_through_create_app` in `phase2_mcp/tests/test_app.py`;
`test_isolation.py`s Platzhalter wurde geschärft, kein zusätzlicher Test). `git diff --stat` auf
`storage/`, `mcpserver/tools.py`/`permissions.py`/`server.py` bleibt leer (Akzeptanzkriterium
§6.18) — nur `mcpserver/app.py` (P5-B erlaubt das) und Testdateien geändert. `pyflakes` über alle
neuen/geänderten Dateien lief sauber durch. **Advisor-Review vor diesem Commit war nicht
möglich** (Tool zweimal „temporarily overloaded" zurückgemeldet, nicht übersprungen) — Ersatz:
`pyflakes`, voller `pytest -q`, `ui_smoke.py` real ausgeführt, Tabu-Pfad-Diff geprüft, alles vor
dem Commit. Kein stiller Verzicht auf die sonst übliche Disziplin, festgehalten statt verschwiegen.

**Nächster Schritt (konkret):** Step 6 (UI-Gerüst: Shell, Tokens, Navigation, Liste, Suche —
Plan §4.1–§4.3/§4.6, `webui/static/{app.html,app.css,app.js}`). Die `apple-design`-Skill
(58,5K Installs, `emilkowalski/skills@apple-design`) ist seit dieser Session installiert — der
Plan-Vermerk in §4 „einen `apple-design`-Skill gibt es in dieser Umgebung nicht" ist damit
überholt, Step 6 kann sie direkt nutzen statt nur von `frontend-design` abzuleiten. Zeilen 5/6
folgen, sobald Step 6 einen echten Klick-Pfad für `/api/v1/account/password` bietet. Die drei
liegen gebliebenen Live-Aktionen aus Step 1/2 (S3/S4-Gegenprobe, Purge-Timer aktivieren,
Migrations-Runbook) bleiben unverändert offen, blockieren weiterhin keinen Code-Step.

---

## Session stopped — 2026-08-03 (Step 4: Selbstverwaltung — Einladung, Passwort, TOTP, Recovery, Connectoren)

**Für den nächsten, kalten Leser:** diese Session begann nach einem Context-Compaction-Verlust
— der einzige erhaltene Rest war eine Notiz, dass eine vorige Session mitten in Step 4 stand:
Code + Tests für `account.py`/`reauth.py`/`passwords_policy.py`/`blocklist.txt` plus die
`authctl.py`-Erweiterung lagen bereits unstaged im Arbeitsverzeichnis, `git status` bestätigte
das (keine Behauptung aus dem Notiz-Rest übernommen, siehe Root-`CLAUDE.md`-Lehre „eine
Doku-Aussage über den Repo-Zustand ist erst wahr, wenn `git status` sie bestätigt"). Die Notiz
nannte drei ausstehende Schritte: `phase5_ui/tests` grün, danach das ganze Repo grün, dann eine
Advisor-Review vor der Dokumentation. Alle drei nachgeholt, plus was der Advisor dabei fand.

**Bauteile aus der vorigen (verlorenen) Session, gegengelesen statt neu gebaut:**
1. **`account.py`** — `/api/v1/account/*`, JSON durchgehend (§3.1). Jede Route lädt zuerst die
   Sitzung, state-ändernde Routen prüfen CSRF (`X-CSRF-Token`-Header), re-auth-pflichtige Routen
   (P5-P) zusätzlich Passwort+TOTP über `reauth.verify_reauth()`. Acht Routen: Passwort ändern,
   TOTP-Neueinrichtung (Start/Confirm), Recovery-Codes neu ausgeben, eigene Sessions
   auflisten/beenden, eigene Connector-Verbindungen auflisten/widerrufen.
2. **`reauth.py :: verify_reauth()`** — Passwort + TOTP in einem Schritt, **kein**
   Recovery-Code-Ersatz (anders als der normale Login, P5-P-Wortlaut „Passwort UND TOTP-Code").
   Dieselbe `LoginThrottle` wie UI-/OAuth-Login. Zähler-Reihenfolge korrekt: `set_totp_counter()`
   läuft erst nach `throttle.reset()`, also nach vollständigem Erfolg — dieselbe Lehre wie der
   Step-3-Advisor-Fund in `routes_auth.py`, hier beim Nachbau richtig übernommen.
3. **`passwords_policy.py`** — Länge (12–128) + Blocklist, kein Zeichenklassenzwang, kein
   Netzaufruf (Bauprinzip: der Server telefoniert nicht nach Hause). **V30 geschlossen:**
   `blocklist.txt` ist `danielmiessler/SecLists`s `10k-most-common.txt` (MIT-lizenziert, geht auf
   Mark Burnetts „10,000 Top Passwords" zurück), 10000 Einträge, 73 KB — deckt sich mit dem
   Plan-Vorschlag „~80 KB" fast exakt.
4. **`routes_auth.py`-Erweiterung** — `/ui/invite/{token}` (GET/POST), `/ui/enroll/confirm`.
   Passwortpolitik wird **vor** `consume_invite()` geprüft (die Einladung ist einmalig — ein zu
   schwaches erstes Passwort darf sie nicht verbrennen). `store.upsert_user()` statt
   `set_password()`/`begin_totp_enrollment()` allein, weil für einen brandneuen Space aus einer
   Einladung noch keine `users`-Zeile existiert (beide Methoden können nur `UPDATE`). TOTP-QR
   über `segno` (Inline-SVG, V29 geschlossen, `pyproject.toml` exakt gepinnt `segno==1.6.6`, P4-R
   pass'sches Pin-Muster übernommen) — geprüft, nicht nur behauptet: `pages.py ::
   render_enrollment_page()` rendert tatsächlich ein `<svg>`, die `img-src 'self' data:`-Lockerung
   in `security.py`s CSP-Kommentar war also zutreffend, nicht nur eine Ankündigung.
5. **`authctl.py`-Erweiterung** — sechs neue Unterbefehle: `invite` (Link genau einmal auf
   stdout, Klartext-Disziplin wie `provision_user.py`), `list-users` (keine Hashes/Seeds),
   `disable-user`/`enable-user`, `list-sessions`/`revoke-sessions`. `disable-user`/
   `revoke-sessions` dürfen anders als `revoke --family-id` sammeln (`--space`
   statt `--family-id`) — bewusste Ausnahme von der P4-Step-7-Regel „kein Sammelwiderruf",
   dokumentiert im Modul-Docstring: eine Sitzung/Familie ist kein Betreiber-Werkzeug wie ein
   DCR-Client, sondern der Notausgang, den Plan §5 Step 4 dafür vorsieht.

**Tests grün, wie in der Notiz gefordert:** `pytest phase5_ui/tests -q` → 39/39, `pytest -q`
(Repo-Wurzel) → 462/462 (436 zu Step-3-Ende, +26 aus der vorigen Session).

**Advisor-Review vor der Dokumentation (wie von der Notiz verlangt) — drei echte Funde, alle vor
dem Commit behoben, keiner still liegen gelassen:**

1. **`account.py :: _password()` verwarf den rotierten CSRF-Token — blockierend.**
   `sessions.rotate()` gibt den CSRF-Token nur EIN einziges Mal als Klartext zurück (`ui_sessions`
   speichert nur `csrf_hash`, exakt der Grund, aus dem `pages.py :: render_logged_in_page()` in
   Step 3 gebaut wurde) — der Rückgabewert landete bisher im Leeren. Jede folgende
   CSRF-geprüfte `/api/v1/account/*`-Anfrage nach einem Passwortwechsel hätte bis zum nächsten
   Login mit `403 csrf_failed` geantwortet. Fix: `response.render({"ok": True, "csrf_token":
   new_csrf})`, `content-length` nachgezogen. Neuer Test
   `test_password_change_returns_a_usable_csrf_token` (`test_account.py`) — macht bewusst einen
   ZWEITEN CSRF-geprüften Aufruf (`DELETE /api/v1/account/sessions`) mit dem neuen Token; der
   bestehende `test_password_change_revokes_other_sessions_but_not_current` hätte die Lücke
   nicht gefunden, weil sein Folgeaufruf ein `GET` ist (CSRF-frei).
2. **Kein Login-Pfad prüfte `record.status` — blockierend, neuer Sicherheitsbefund S9.**
   `authctl.py disable-user` widerrief bisher nur Sitzungen und Token-Familien, aber weder
   `webui/routes_auth.py :: _login_post` noch `authserver/flows.py :: submit_consent` lasen je
   `record.status` — ein deaktivierter Space konnte sich mit unverändertem Passwort/TOTP sofort
   wieder einloggen bzw. neu autorisieren, `disable-user` war ohne Live-Wirkung reines
   Papier-Kommando. Fix in **beiden** Pfaden: `account_active = record is not None and
   record.status == "active"`, zusätzliches Erfolgskriterium, nach dem unconditional
   Argon2id-Verify eingehängt (Enumerationsschutz bleibt intakt — kein eigener Fehlercode, exakt
   dieselbe generische Meldung wie ein falsches Passwort). Neue Tests:
   `test_disabled_account_cannot_log_in` (`test_routes_auth.py`),
   `test_disabled_account_cannot_consent` (P4 `test_flows.py`). Dokumentiert als **S9** in
   `phase4_auth/CLAUDE.md`s Befund-Tabelle (dated Nachtrag dort) — eine geschlossene Phase mit
   einem 📗 live gepflegten Kopf bekommt bei Code-Änderungen dieselbe Behandlung wie S2–S8, kein
   stiller Abstand von der eigenen Konvention.
3. **`disable-user` ließ eine offene Einladung am Leben — im selben Zug behoben, nicht nur
   notiert (Advisor: „billig genug für diesen Commit").** `_invite_post` legt über
   `store.upsert_user(..., status="active")` bei Einlösung eine neue, aktive Nutzerakte an — eine
   noch nicht eingelöste Einladung hätte `disable-user` damit unterlaufen können. Neue Methode
   `store.revoke_invites_for_space()` (markiert alle noch nicht eingelösten Einladungen als
   eingelöst, `consumed_at = jetzt`, kein eigenes „revoked"-Feld nötig — inklusive bereits
   abgelaufener Zeilen, kein `expires_at`-Filter, Docstring nennt das explizit), aufgerufen aus
   `_cmd_disable_user`. Neue Tests: `test_revoke_invites_for_space_only_touches_own_unconsumed_ones`
   (`test_authserver_store.py`), `test_disable_user_also_revokes_outstanding_invites`
   (`test_authctl.py`).

**Zwei weitere Advisor-Funde, bewusst NICHT gefixt, nur benannt (Advisor: „Warzen, keine
Blocker"):**
- `reauth.py :: verify_reauth()`/`flows.py :: submit_consent()`: `consume_recovery_code()` läuft
  bereits, sobald `password_ok` wahr ist — bei falschem TOTP UND korrektem Passwort UND einem
  vorgelegten Recovery-Code würde der Code verbrannt, obwohl der Login am Ende trotzdem scheitert
  (fehlt hier: TOTP war der vorgelegte Faktor, kein Recovery-Code-Pfad aktiv — betrifft also nur
  den Fall, dass jemand einen Recovery-Code an der TOTP-Stelle einreicht). Höchstens
  Selbst-Griefing, kein Fremdrisiko: das eigene Konto ist so oder so nicht eingeloggt. Nicht
  umgebaut, um den bestehenden, bereits getesteten Zweig nicht anzufassen.
- `authctl.py :: set_user_status()` ist ein stiller No-Op für einen nicht existierenden Space —
  `disable-user --space ghost` meldet „deaktiviert" ohne Wirkung. Operator-Werkzeug-Macke, kein
  Sicherheitsproblem (kein Space, kein Schaden), vorgemerkt für einen künftigen `authctl.py`-Umbau.

**Verifiziert, nicht nur behauptet, nach allen drei Fixes:** `pytest -q` (Repo-Wurzel) →
**467/467 grün** (462 vor den Fixes, +5: `test_password_change_returns_a_usable_csrf_token`,
`test_disabled_account_cannot_log_in`, `test_disabled_account_cannot_consent`,
`test_disable_user_also_revokes_outstanding_invites`,
`test_revoke_invites_for_space_only_touches_own_unconsumed_ones`). `git diff --stat` auf
`storage/`, `mcpserver/{tools,permissions,server}.py` bleibt leer (Akzeptanzkriterium §6.9,
gegengeprüft trotz P4-Dateien im Diff — `flows.py`/`store.py`/`authctl.py` liegen alle innerhalb
von P4-Qs erlaubter Berührungsfläche für `authserver`, keine davon auf der Tabu-Liste). Zweiter
Advisor-Durchlauf nach den Fixes bestätigte: Enumerationseigenschaft hält (Status-Gate sitzt nach
dem Argon2id-Verify in beiden Pfaden), `_revoke_family_locked()` löscht `access_tokens`/
`refresh_tokens`-Zeilen (kein bloßes `revoked_at`-Flag) — ein per `disable-user` widerrufenes
Bearer-Token stirbt sofort, nicht erst nach TTL-Ablauf.

**Doku-Abgleich gegen den Plan (Advisor-Auftrag, nicht blockierend):** die in Plan §5 Step 4
gelisteten Testnamen decken sich nicht alle wörtlich mit den tatsächlichen — drei Namen
(`test_recovery_code_replaces_totp_not_password`, `test_used_recovery_code_cannot_be_reused`,
`test_recovery_code_works_in_oauth_consent_form`) beschreiben Verhalten, das bereits in P5 Step 2
gebaut und getestet wurde (`test_authserver_store.py :: test_recovery_codes_replace_and_consume`,
`test_flows.py :: test_recovery_code_login_does_not_touch_totp_counter`/
`test_wrong_password_with_valid_recovery_code_does_not_burn_it`) — der Plan wurde ohne frischen
Repo-Zugriff geschrieben (wie alle P4/P5-Pläne) und zählt Verhalten aus einem früheren Step
erneut auf. Kein Deckungsloch, nur eine Namensabweichung.

**Nachtrag, später am selben Tag — `/ui/*` aus Step 5 vorgezogen verdrahtet, Live-Fund des
Nikingers während des Block-A-Gates:** `authctl.py invite niklas` lieferte einen
`/ui/invite/<token>`-Link, der Aufruf im Browser lieferte **`404`**. Ursache: `webui`s
Auth-Routen (`ui_auth_routes()`/`account_routes()`, Step 3/4, vollständig getestet) waren nie in
den echten Prozess gemountet — `mcpserver/app.py :: create_app()` kannte bis dahin ausschließlich
`oauth_routes()` und `Mount("/mcp")`. Grund: Plan §5 Step 5 listet genau diese Verdrahtung
("`webui_routes(...)` in die Routenliste") als **eigenen** Schritt, aber Step 5 selbst ist laut
Plan hinter dem Block-A-Gate verriegelt — und der Gate selbst verlangt Live-Zeilen 1–9 gegen
`/ui/login`/`/ui/invite/{token}` (§6). **Ein Zirkel im Plan-Text**, kein Interpretationsspielraum:
der Gate kann nicht bestehen, bevor der Schritt läuft, der hinter dem Gate liegt.

**Zweiter, unabhängiger Fund beim Nachlesen des Plans wegen desselben Themas:** Plan §1.2s
Paketgrenzen-Tabelle verbietet `mcpserver` ausdrücklich den Import von `webui`
("`mcpserver` … darf **nicht** importieren: `webui`") — aber §1.5s eigene Route-Landkarte zeigt
`create_app()` genau das tun (`routes += webui_routes(...)`). Beide Stellen stehen im selben
📕-Plandokument; §1.2 ist keine der 30 einzeln benannten, gelockten Entscheidungen (P5-A–P5-AE),
sondern eine Ableitungstabelle, die mit der im selben Dokument gezeichneten Architektur nicht
zusammenpasst.

**Beides dem Nikinger vorgelegt statt still aufgelöst** (Root-`CLAUDE.md`: „Widersprechende
Evidenz wird ein expliziter Befund für den Menschen, nie eine stille Abweichung"). Entscheidung:
**minimale Verdrahtung jetzt vorziehen** — nur `ui_auth_routes()`+`account_routes()` (beide
fertig, getestet), **nicht** `webui/api.py` (existiert noch nicht, echter Step-5-Scope) — damit
der Gate durchführbar wird, plus eine Korrektur der §1.2-Aussage hier im Phase-Head (📕-Plan
selbst bleibt unverändert, wie bei jeder Plan-Korrektur in diesem Projekt — siehe z. B.
`authserver/passwords.py :: ARGON2_TIME_COST`s Korrekturnotiz zum selben Muster).

**§1.2-Korrektur:** „`mcpserver` darf `webui` nicht importieren" gilt ab diesem Nachtrag **nicht
mehr uneingeschränkt** — `mcpserver/app.py :: create_app()` importiert `webui.routes_auth`/
`webui.account`, mit Begründung. Was UNVERÄNDERT gilt: `webui` importiert weiterhin höchstens ein
Symbol aus `mcpserver` (`permissions.OwnSpaceWritable`, P5-B, noch ungenutzt — kommt erst mit
`webui/api.py` in Step 5). Die Richtung des Verbots war die, die einen Zyklus verhindern sollte
(`mcpserver → webui → mcpserver`); ein reiner `mcpserver → webui`-Import ohne Rückweg ist
architektonisch unbedenklich. Geprüft, nicht nur behauptet: `mcpserver/permissions.py` (das
einzige `mcpserver`-Symbol, das `webui` je ziehen darf) importiert selbst nur `collections.abc`/
`typing` — kein Pfad zurück zu `mcpserver.app` oder `webui`, auch nicht sobald `webui/api.py` in
Step 5 dazukommt. Test `test_create_app_mounts_ui_routes_without_import_cycle`
(`phase2_mcp/tests/test_app.py`) hält diese Prämisse fest.

**Umsetzung, ein Commit:** `mcpserver/app.py :: create_app()` baut `UiSettings`/`SessionManager`
intern aus dem bereits vorhandenen `oauth`-Bündel (`oauth.settings.base_url`, `oauth.store`,
`oauth.users` — dieselbe `AuthStore`/`UserDirectory`-Instanz wie die OAuth-Seite, kein zweiter
DB-Handle), mountet `ui_auth_routes()`+`account_routes()` zwischen `oauth_routes()` und
`/health`/`Mount("/mcp")` — exakt die von §1.5 vorgezeichnete Reihenfolge. **Keine neuen
`create_app()`-Parameter.** Drei neue Tests in `phase2_mcp/tests/test_app.py`:
`test_create_app_mounts_ui_routes_without_import_cycle` (siehe oben),
`test_ui_login_reachable_through_create_app`, `test_ui_invite_reachable_through_create_app` —
beide Letzteren bauen bewusst die ECHTE `create_app()`-App (die `app`-Fixture, dieselbe wie die
MCP-Tests), nicht `phase5_ui/tests`s eigenständige `Starlette(routes=ui_auth_routes(…))`-Testapp
— genau der Unterschied, den der Live-Fund aufgedeckt hat: Step 3/4s Done-when-Nachweis lief nie
gegen den echten Prozess.

**Verifiziert:** `pytest -q` (Repo-Wurzel) → **470/470 grün** (467 vor diesem Nachtrag, +3).
`git diff --stat` auf `storage/`, `mcpserver/tools.py`/`permissions.py`/`server.py` bleibt leer
(Akzeptanzkriterium §6.18) — nur `mcpserver/app.py` und die beiden Testdateien geändert.
`phase2_mcp/CLAUDE.md`s Testzahl-Zeile im selben Commit nachgezogen (80→83).
`python -c "from mcpserver.app import create_app"` lief vor dem Testlauf zusätzlich isoliert
durch, um einen Importfehler von einem Testfehler zu unterscheiden.

**Schritt null vor dem Gate, nicht optional (Advisor-Hinweis):** dieser Nachtrag ändert nur den
Code. Der laufende `sharefyx-mcp`-Dienst führt noch den alten Build — „`/ui/login`/
`/ui/invite/{token}` sind live erreichbar" gilt erst nach
`sudo phase3_edge/scripts/install_units.sh && sudo systemctl restart sharefyx-mcp` (kein
Migrations-Runbook nötig, reiner Code-Deploy). Ohne diesen Restart liefert ein erneuter Versuch
mit dem Invite-Link wieder `404`, und der Fix sähe fälschlich kaputt aus.

**Zweiter Nachtrag, noch später am selben Tag — Sackgasse bei `/ui/enroll/confirm` beseitigt,
Ursache noch OFFEN, nicht behauptungsweise geschlossen:** der Nikinger kam beim Gate bis zum
TOTP-Enrollment und bekam dort `403 Herkunft (Origin) stimmt nicht` — `security.py ::
require_csrf()`s Origin-Prüfung schlug fehl. **Was diese Session behebt:** die Antwort auf einen
`CsrfError` in `routes_auth.py :: _enroll_confirm()` war bisher `pages.render_error_page()` —
eine echte Sackgasse ohne Formular, ohne Zurück, und die Einladung war schon verbraucht
(Einmal-Token), also auch keine neue Einladung als Ausweg. Jetzt: derselbe Codepfad, den „falscher
TOTP-Code" schon hatte (`_enrollment_retry()`, neu extrahiert, beide Fälle teilen sich die
Logik), rendert dieselbe Enrollment-Seite mit Fehlermeldung erneut — derselbe CSRF-Token bleibt
gültig (die Sitzung wird bei einem CSRF-Fehlschlag nicht widerrufen), kein neuer Login nötig.
Test `test_enroll_confirm_csrf_failure_offers_a_retry_not_a_dead_end`
(`phase5_ui/tests/test_invite_enroll.py`).

**Was diese Session NICHT behebt, Advisor-Korrektur vor dem Commit:** die erste Fassung dieses
Absatzes klang, als sei das Problem gelöst — ist es nicht. Wenn die Origin-Abweichung
**strukturell** ist (z. B. eine zweite, in der Praxis benutzte URL-Variante, die
`settings.base_url` nicht kennt), sendet der Browser beim erneuten Absenden desselben Formulars
dieselbe falsche Origin erneut — der Nutzer landet dann auf einer freundlicheren, aber ebenso
endlosen Schleife statt einer Sackgasse. **Root Cause noch nicht gefunden:**
`systemctl cat sharefyx-mcp` bestätigt `SPACE_PUBLIC_BASE_URL=https://savefyx-vmware-virtual-
platform.tail89fc2a.ts.net` — das ist eine Ableitung, kein Beleg für das, was der Browser
tatsächlich als `Origin`-Header sendet. Zwei Dinge sprechen gegen einen reinen Tippfehler in der
Config: `_invite_post` prüft gar kein CSRF (Einmal-Token ist dort das Gate) — der Fehler trat
also plausibel von Anfang an auf, nur unbemerkt, bis der erste CSRF-geprüfte Schritt kam; und
das `__Host-`-Cookie kam zurück (sonst „Sitzung abgelaufen" statt des Origin-Fehlers), also läuft
der Browser auf **irgendeiner** echten HTTPS-Origin, nicht auf `http://127.0.0.1` o. ä. — das
grenzt auf „HTTPS, aber ein anderer Host-String als der konfigurierte" ein, mehr nicht.

**Nikinger-Aktion vor dem nächsten Versuch:** DevTools → Network → den fehlschlagenden `POST
/ui/enroll/confirm` → Request Headers → `Origin` — Wert Zeichen für Zeichen gegen
`https://savefyx-vmware-virtual-platform.tail89fc2a.ts.net` halten. Gleiches Muster wie der
`form-action`-CSP-Fund in P4 (2026-07-30, `phase4_auth/CLAUDE.md`) — auch dort führte erst ein
DevTools-Beleg zur echten Ursache, keine Ableitung aus der Config. **Falls sich eine zweite,
legitime Origin herausstellt** (z. B. eine andere URL, unter der der Dienst ebenfalls erreichbar
ist): das ist eine Entscheidung für den Nikinger (`require_csrf()` auf eine Origin-Menge
auszuweiten wäre eine Sicherheitsentscheidung, keine, die hier auf eigene Initiative getroffen
wird), nicht stillschweigend im Code vorwegzunehmen.

**Verwandte, nicht angefasste Stelle:** `_logout` hat denselben `render_error_page()`-Sackgassen-
Musterfehler bei einem CSRF-Fehlschlag — bewusst nicht mitgefixt (nicht angefragt, kleinerer
Schaden: ein Logout-Fehlschlag lässt die Sitzung einfach bestehen, kein Datenverlust). Falls die
Origin-Ursache strukturell ist, träfe sie `_logout` genauso — dann ist das dieselbe Ursache,
kein neuer Fund, wenn er auftaucht.

**Verifiziert:** `pytest -q` (Repo-Wurzel) → **471/471 grün** (470 vor diesem Nachtrag, +1).
`errors.py :: CsrfError`s Docstring korrigiert (behauptete fälschlich „nie eine unterscheidbare
Detailmeldung nach außen" — `require_csrf()` warf schon immer drei unterscheidbare Klartexte,
unbedenklich, weil keine davon Kontoexistenz verrät, aber die Doku-Aussage war seit ihrem
ursprünglichen Commit falsch, unabhängig von diesem Nachtrag).

**Fünfter Nachtrag, 2026-08-04 — Auftrag „TOTP-Seed kaputt", tatsächlich derselbe Origin-Fund,
jetzt mit Beleg statt Verdacht:** der Nikinger meldete diese Session einen vermeintlich neuen
Fehler („weder Copy-Paste noch QR-Scan liefert einen gültigen Code, Google Authenticator
gegengetestet") — **kein neuer Fund**, sondern derselbe offene Origin-Fehlschlag von oben, nur
falsch zugeordnet (das Symptom trifft jeden Enrollment-Versuch gleich, unabhängig vom
TOTP-Eingabeweg, weil der Request nie bis zur TOTP-Prüfung kommt). Beleg statt Vermutung:
`journalctl -u sharefyx-mcp` zeigt **jeden** `POST /ui/enroll/confirm` seit 2026-08-03 mit
**Status 403**, keinen einzigen 422 („Code ungültig") oder 200 — bei einem echten TOTP-Problem
wäre mindestens ein 422 zu erwarten (falscher Code, aber CSRF bestanden). Das schließt die
Alternativhypothese „TOTP-Seed entschlüsselt nicht" aus (die hätte ebenfalls 422 erzeugt, nicht
403), ohne dass die Live-Datenbank angefasst werden musste.

Config-Parität read-only geprüft, alle drei Quellen stimmen exakt überein (kein Port-, kein
Hostname-Unterschied): `systemctl show sharefyx-mcp --property=Environment` →
`SPACE_PUBLIC_BASE_URL=https://savefyx-vmware-virtual-platform.tail89fc2a.ts.net`;
`phase3_edge/local.env` → `PUBLIC_BASE_URL` byte-identisch; `tailscale funnel status` → dieselbe
URL, Proxy-Ziel `127.0.0.1:8765`, Port 443 (kein 8443/10000). Root Cause also **nicht** eine
falsch konfigurierte Base-URL — die Abweichung muss im tatsächlich vom Browser gesendeten
`Origin`-Header liegen, und genau der Wert landete bisher **nirgends**, weder im Request-Log
(`mcpserver/request_log.py` protokolliert keine Header) noch sonst irgendwo im Prozess.

**Behoben — die Belegbarkeitslücke, nicht (noch) die Ursache selbst:** `webui/security.py ::
require_csrf()` loggt den abgelehnten Origin-Fehlschlag jetzt serverseitig
(`logger.warning("CSRF-Origin-Fehlschlag: erhalten %r, erwartet %r", origin, settings.base_url)`,
stdlib `logging` → stderr, Hard Rule 7). **Nur ins Log, nie in die Client-Antwort** —
`CsrfError.message` bleibt unverändert der generische Text, keine Erweiterung der
Enumerationsfläche. Test `test_csrf_foreign_origin_logs_the_received_value_but_not_to_the_client`
(`test_security.py`, `caplog`) hält beide Hälften fest: der Wert landet im Log, nicht in
`exc.message`. Das macht den nächsten fehlschlagenden Live-Versuch selbstbelegend — kein
DevTools-Screenshot mehr nötig, `journalctl -u sharefyx-mcp | grep -i "CSRF-Origin"` zeigt direkt
den String, der gegen `settings.base_url` verglichen wurde.

**Verifiziert:** `pytest -q` (Repo-Wurzel) → **472/472 grün** (471 vor diesem Nachtrag, +1).

**Sechster Nachtrag, 2026-08-04 — Root Cause gefunden: `Origin: null`, Server-Verhalten korrekt,
Mechanismus noch offen:** der neu geloggte Wert (Nikinger-Beleg, unmittelbar nach dem Restart):

```
CSRF-Origin-Fehlschlag: erhalten 'null', erwartet 'https://savefyx-vmware-virtual-platform.tail89fc2a.ts.net'
```

**`Origin: null` ist keine zweite legitime Origin** — es ist der Wert, den ein sandboxed Iframe
(kein `allow-same-origin`), ein `data:`/`file:`-Dokument oder ein manipuliertes Cross-Site-Formular
sendet. Ein CSRF-Schutz, der `null` akzeptiert, ist ein Lehrbuch-Bypass (der Wert ist genau das,
was ein Angreifer aus einem fremden Kontext erzeugen kann). **`require_csrf()` bleibt unverändert
— das Verhalten ist richtig, keine Erweiterung auf `null` oder eine Origin-Menge.** Die
DevTools-Konsole desselben Screenshots stützt das: zwei CSP-Meldungen zu `utils.js`/„sandbox eval
code" — beides referenziert keine Datei aus diesem Repo (gegengeprüft, `grep -r "utils.js"` →
leer) — legt nahe, dass die Seite nicht in einem gewöhnlichen Top-Level-Tab lief, sondern in einem
eingebetteten/sandboxed Vorschau-Panel (z. B. ein IDE-„Simple Browser" o. ä.) oder unter dem
Einfluss einer Browser-Extension, die Header/Skripte injiziert. **Zwei konkurrierende Mechanismen,
noch nicht unterschieden** (Advisor-Einwand, ernst genommen statt vorschnell benannt): ein
Cookie-Roundtrip war in der vorigen Session bereits belegt (`__Host-`-Cookie kam zurück) — ein
vollständig sandboxed Iframe ohne `allow-same-origin` bricht üblicherweise auch den
Cookie-Zugriff, was leicht in Spannung zu „Origin fehlt" steht. Die entscheidende, noch offene
Frage an den Nikinger: **war das ein normaler Chrome/Firefox-Tab (Adressleiste zeigt die volle
URL) oder ein Panel/eine Vorschau innerhalb eines anderen Programms (IDE, Tailscale-Helper,
o. ä.)?** Bis geklärt: **Testschritt ist, den Einladungslink in einem frischen, normalen
Top-Level-Tab zu öffnen** (idealerweise ohne Extensions) — das ist der Fix unabhängig vom
Mechanismus, kein Code ändert sich dafür.

**Zwei kleine, unabhängige Funde aus demselben Screenshot, notiert, nicht behoben (kein
Blocker):**
- `pages.py`s `render_enrollment_page()` (Zeile ~75) setzt `style="background:#fff;padding:8px;
  display:inline-block"` inline auf den QR-Wrapper — die eigene `style-src 'self'`-CSP blockiert
  das (`style-src-attr`), rein kosmetisch (der QR-Code selbst bleibt scanbar, nur der weiße
  Rahmen fehlt). Braucht eine Klasse in `app.css`, sobald `/ui/static` existiert (Step 5/6).
- `_PAGE`s `<link rel="stylesheet" href="/ui/static/app.css">` 404et auf jeder UI-Seite — bekannt
  und erwartet (`config.py :: UiSettings`-Docstring: „`static_dir` fehlt aus demselben Grund"),
  aber bisher nicht im Phase-Head vermerkt; jetzt hier, damit es beim Gate nicht als neuer Fund
  missverstanden wird.

**Siebter Nachtrag, 2026-08-04 — Nikinger-Rückfrage beantwortet, IDE-Panel UND In-App-Browser
ausgeschlossen:** Link kopiert und in einen normalen Browser eingefügt (nicht getippt in der VM,
kein eingebetteter Panel, keine Chat-/Mail-App als Zwischenschritt) — genau der „normale Tab",
den `require_csrf()` erwartet. Damit bleibt als führende Hypothese eine **Browser-Extension**, die
den `Origin`-Header auf `null` umschreibt (bekanntes Verhalten mancher Privacy-/Ad-Blocker-
Extensions bei POST-Anfragen) — dieselbe Deutung, die die beiden unerklärten
`utils.js`/„sandbox eval code"-CSP-Meldungen im Screenshot stützt (keine Datei aus diesem Repo,
also von außen injiziert). **Kein Server-Code geändert** — `require_csrf()`s Ablehnung bleibt
korrekt, unabhängig vom genauen Mechanismus.

**Achter Nachtrag, 2026-08-04 — beide bisherigen Hypothesen widerlegt, echte Ursache gefunden
und behoben:** der Nikinger testete den vorgeschlagenen sauberen Kontext — Chrome, privates
Fenster, Standardeinstellungen, keine Extensions gesetzt — **derselbe Fehlschlag.** Damit sind
sowohl „eingebetteter Vorschau-Panel" (siebter Nachtrag, bereits durch die Rückfrage davor
widerlegt) als auch „Browser-Extension" (siebter Nachtrag, hiermit widerlegt) vom Tisch —
`Origin: null` war zu keinem Zeitpunkt ein Client-Umgebungsproblem.

**Tatsächliche Ursache: der eigene `Referrer-Policy: no-referrer`-Header.** Die Fetch-Spec
(„append a request `Origin` header") bestimmt den `Origin`-Header einer Nicht-CORS-
Nicht-GET/HEAD-Anfrage — genau das, was `/ui/enroll/confirm`s reines HTML-`<form
method="post">` ohne JavaScript ist (Plan §2.8) — nach der Referrer-Policy des sendenden
Dokuments: `no-referrer` liefert dabei **immer** `Origin: null`, auch bei einer echten
Same-Origin-Anfrage an den eigenen Host. `require_csrf()` lehnte diesen Wert korrekt ab (das ist
der klassische CSRF-Bypass-String) — die eigene, zu strenge Referrer-Policy hat sich damit selbst
ausgesperrt. Deterministisch, kein Zufall: das erklärt in derselben Bewegung, warum der Fehler in
jedem bisherigen Versuch identisch auftrat (VM-Kontext, unbekannter Kontext, sauberes
Inkognito-Profil) und bestätigt die eigene Vorhersage aus dem vierten Nachtrag oben, dass
`_logout` (derselbe `require_csrf()`-Aufruf, dieselbe Referrer-Policy) genauso betroffen wäre.

**Fix:** `webui/security.py :: ui_security_headers()` — `Referrer-Policy` von `no-referrer` auf
**`strict-origin`** geändert. `strict-origin` nullt den `Origin`-Header nur bei einem
TLS-Downgrade (kann hier nicht vorkommen, `_validate_base_url()` erzwingt `https://`) und sendet
nie den Pfad — bewusst **nicht** `same-origin` gewählt (Advisor-Korrektur: `same-origin` würde
bei einer echten Same-Origin-Anfrage den vollen Pfad als `Referer` senden, und
`/ui/invite/<token>` trägt ein Einmal-Secret im Pfad, das sonst z. B. an `/ui/static/app.css`
durchsickern würde). `authserver/routes.py :: _security_headers()` trägt denselben
`no-referrer`-Wert für die OAuth-Seiten — **bewusst nicht mitgeändert** (andere Flows, 302 nach
`claude.ai`, andere Konsequenzen, P4s `csp_form_action`-Historie zeigt genau diese Fläche als
heikel) — als eigener, unbehobener Befund hier vermerkt, kein Blocker für Block A.

Test `test_ui_referrer_policy_does_not_null_the_origin_header_on_same_origin_posts`
(`test_security.py`) pinnt den neuen Header-Wert. **Nicht live verifizierbar von hier aus** —
`curl` interpretiert keine `Referrer-Policy`, nur ein echter Browser entscheidet, was er sendet;
der Test belegt ausschließlich, welchen String der Server jetzt schickt, nicht, dass der Browser
danach den echten `Origin` sendet. `pytest -q` (Repo-Wurzel) → **473/473 grün** (472 vor diesem
Nachtrag, +1).

**Neunter Nachtrag, 2026-08-04 — live bestätigt, Fix hält, Zeile 3 (§6) bestanden:** Restart um
18:34:38 (`systemctl show sharefyx-mcp -p ExecMainStartTimestamp`), danach EIN
Enrollment-Versuch um 18:36:40 — `journalctl` zeigt `{"method":"POST",
"path":"/ui/enroll/confirm","status":200,...}`, **keine** neue `CSRF-Origin-Fehlschlag`-Zeile
(die drei vorhandenen Zeilen im `grep`-Ausschnitt des Nikingers stammen alle von vor dem
Restart, 18:11/18:25/18:26). Kein Beleg aus zweiter Hand — Prozessstart-Zeitstempel UND
Log-Zeile read-only gegengeprüft, nicht nur die Nikinger-Zusammenfassung übernommen (dieselbe
Disziplin wie beim Phase-4-Schnitt). **Root Cause bestätigt: `Referrer-Policy: no-referrer` war
die alleinige Ursache, `strict-origin` behebt sie vollständig.** TOTP-Seed, Verschlüsselung,
Enrollment-Logik — alles war von Anfang an unbeteiligt.

**Zeile 3 (§6, Abnahmematrix Block A) damit live bestanden:** „TOTP-Seed einmal angezeigt, in
einer echten Authenticator-App aufgenommen, Code akzeptiert." Offen aus Block A bleiben Zeilen
1, 2, 4–9 (Einladungslink-Einmaligkeit, Recovery-Codes, Passwortwechsel ohne Restart,
Session-Widerruf, gemeinsame Fehlversuchsbremse, `authctl.py list-users`, `strings`-Grep gegen
`auth.sqlite3`) — der harte Gate vor Block B ist damit **nicht** vollständig, nur der bisherige
Blocker ist weg.

**Zehnter Nachtrag, 2026-08-05 — Zeilen 1, 2, 4, 7, 8, 9 live bestanden; Zeilen 5/6 auf nach dem
Step-5/6-App-Shell verschoben (Nikinger-Entscheidung):**
- **Zeile 1** (Einladungslink → aktives Konto): bereits durch den Enrollment-Durchlauf oben
  belegt.
- **Zeile 2** (Einladungslink zweimal): Nikinger meldet „ungültiger Einladungslink" beim
  zweiten Aufruf — bestanden.
- **Zeile 4** (Recovery-Code ersetzt TOTP): erste Anmeldung mit Recovery-Code erfolgreich,
  derselbe Code beim zweiten Versuch abgelehnt — bestanden.
- **Zeile 8** (`authctl.py list-users`): von Claude Code read-only ausgeführt — `niklas`/
  `fabian`, `status='active'`, `totp_confirmed=True`, kein Hash, kein Seed sichtbar — bestanden.
- **Zeile 9** (`strings` gegen `auth.sqlite3`): Grep-Versuch von Claude Code selbst vom
  Auto-Mode-Classifier blockiert (Zugriff auf die Rohdatei mit echten Secrets — genau die
  Kategorie „echte Nutzerakten", die laut Root-`CLAUDE.md` dem Nikinger vorbehalten ist, nicht
  umgangen). Nikinger führte denselben Befehl
  (`strings /var/lib/sharefyx/auth.sqlite3 | grep -E '^[A-Z2-7]{26,32}$'`) selbst aus — leere
  Ausgabe, kein Base32-Seed im Klartext — bestanden.
- **Zeilen 5/6** (Passwortwechsel ohne Restart / Session-/Connector-Widerruf danach): kein
  Klick-Pfad existiert dafür — Step 4 baute nur die JSON-API (`/api/v1/account/*`), keine
  HTML-Seite; die App-Shell (`app.js`, echte Formulare) ist Step 5/6-Scope, der **nach** diesem
  Gate liegt (dieselbe Plan-Reihenfolge-Spannung wie der `/ui/invite`-404-Fund oben). Ein
  DevTools-`fetch()`-Workaround wurde angeboten, vom Nikinger explizit abgelehnt: „das ist ein
  Workaround, kein echter Test." **Nikinger-Entscheidung: Zeilen 5/6 werden zurückgestellt, bis
  die echte App-Shell existiert, dann mit einem echten Klick-Pfad nachgeholt — kein Ersatztest
  jetzt.**
- **Zeile 7** (gemeinsame Fehlversuchsbremse UI-Login/OAuth-Consent): vom Nikinger live
  bestanden — eine Sperre über `/ui/login` griff auch für den OAuth-Consent-Login desselben
  Space, dieselbe `LoginThrottle`-Instanz wie erwartet (P4-Sicherheits-Review, keine zwei
  getrennten Bremsen). Danach zweimal von Claude Code aufgehoben
  (`authctl.py unlock --space niklas`, read-only-äquivalentes Aufräumen nach einem
  absichtlichen Fehlversuchstest, kein Zugriff auf Rohsecrets wie bei Zeile 9) — einmal
  zwischen den Testrunden, einmal danach, damit der Space nicht in gesperrtem Zustand
  zurückbleibt.

**Block A (§6) damit vollständig bis auf die bewusst verschobenen Zeilen 5/6: 1, 2, 3, 4, 7, 8,
9 live bestanden.** Der harte Gate vor Block B gilt für diese sieben Zeilen als erfüllt; 5/6
folgen nach der Step-5/6-App-Shell mit einem echten Klick-Pfad, kein weiterer Blocker davor.

**Nächster Schritt (konkret):** Step 5 (REST-API v1) — **teilweise, nicht vollständig vorgezogen**
(Advisor-Korrektur zum ersten Nachtrag: „bereits erledigt" überzog): Plan §1.5 zeigt
`webui_routes(ui_settings, auth_store, userdir, store, sessions)` mit einem `store`-Parameter
(dem `storage.Store`, für `/api/v1/items/*`) — dieser Nachtrag mountet nur `ui_auth_routes()`/
`account_routes()`, die diesen Parameter nicht brauchen. Step 5 baut `webui/api.py`/
`serializers.py` und braucht dafür einen weiteren, kleinen Edit an `create_app()` (den
`store`-Parameter zusätzlich durchreichen), keine komplette Neuverdrahtung, aber eben auch keine
Nullarbeit. Die drei liegen gebliebenen Live-Aktionen
aus Step 1/2 (S3/S4-Gegenprobe, Purge-Timer aktivieren, Migrations-Runbook) bleiben unverändert
offen, blockieren weiterhin keinen Code-Step.

## Session stopped — 2026-08-03 (Step 3: neues Paket `phase5_ui/` — Sessions, CSRF, Login/Logout)

**Für den nächsten, kalten Leser:** vierte Session der Phase, direkt im Anschluss an Step 2
(„weiter" nach der Advisor-Review + Commit von Step 2). Plan §5 Step 3 zeigt nur auf §2.7
(Sessions/CSRF/Re-Auth) und §3.4 (Sicherheits-Header) — **nicht** auf §2.8 (Einladungs-/
Enrollment-Fluss, braucht `webui/passwords_policy.py` aus Step 4) und **nicht** auf §2.9
(Passwortpolitik). Entsprechend baut dieser Step ausschließlich Login/Logout, nicht
`/ui/invite/{token}` — auch wenn §1.3s Modulkarte `routes_auth.py`/`pages.py` mit „Einladung,
Enrollment" beschreibt: das ist die **finale** Form über mehrere Steps hinweg, nicht Step 3s
Umfang. Mit dem Advisor vor dem ersten Code vorab geklärt (keine Ambiguität stillschweigend
aufgelöst).

**Neues Paket, editable installiert:** `phase5_ui/pyproject.toml` (Paket `webui`, Abhängigkeit
`authserver`), `webui/__init__.py`. `dev_install.sh`s `phase*_*/`-Glob nimmt das Verzeichnis ohne
Skriptänderung auf — **V35 damit geschlossen**, keine Codeänderung nötig, nur geprüft. Root-
`pytest.ini`s `testpaths` um `phase5_ui/tests` ergänzt (ohne diese Zeile hätte `pytest -q` vom
Repo-Wurzelverzeichnis die neuen 22 Tests nie gesammelt — mit `pytest phase5_ui/tests` allein
wäre das unbemerkt geblieben, Advisor-Hinweis).

**Bauteile, in Reihenfolge:**

1. **`config.py`** — `UiSettings` (Cookie-Name `__Host-sfx_session`, `idle_ttl_s`/
   `absolute_ttl_s` als Code-Konstanten 12h/7d nach P5-E, **nicht** über Umgebungsvariablen wie
   `AuthSettings.access_ttl_s` — P5-E nennt keinen Live-Testbedarf wie
   `SPACE_OAUTH_ACCESS_TTL_S` in P4, ein ungenutzter Konfigurationshaken wäre eine Fläche mehr,
   die falsch gesetzt werden kann). **Bewusst OHNE Env-Loader** (anders als
   `authserver.config.load_auth_settings()`, Advisor-Fund: eine erste Fassung hatte
   `load_ui_settings()`, aber nichts rief sie auf und kein Test deckte sie ab — totes Gewicht,
   Hard Rule 7 — entfernt statt ungetestet stehen gelassen). Ein eigenes `UiSettings`-Objekt,
   keine gemeinsame Settings-Klasse mit `authserver` (würde beide Seiten koppeln); die echte
   Umgebungsvariablen-Verdrahtung entscheidet sich erst in Step 5/6, wenn `/ui` real in
   `scripts/serve.py` gemountet wird. `static_dir` fehlt aus demselben „noch kein Bedarf"-Grund
   (§1.3s Modulkarte nennt es als Teil der finalen Form über mehrere Steps, nicht als
   Step-3-Bedarf — Step 3 liefert keine statischen Dateien aus).
2. **`errors.py`** — `CsrfError` (→403), kleinere Menge als `authserver/errors.py`: kein
   RFC-Fehlercode-Vokabular, das kommt erst mit `ApiError` in Step 5.
3. **`sessions.py :: SessionManager`** — `issue`/`load`/`rotate`/`clear` über die
   Step-2-`AuthStore`-Methoden (`create_session`/`touch_session`/`revoke_session`), kein
   eigenes SQL. Cookie exakt nach Plan: `Path=/`, `Secure`, `HttpOnly`, `SameSite=Strict`, kein
   `Domain`, kein `Max-Age`.
4. **`security.py`** — `ui_security_headers()` (eigene CSP, **getrennt** von
   `authserver/routes.py :: _security_headers()` — die OAuth-Seite braucht `claude.ai` in
   `form-action`, die UI nicht) und `require_csrf()`. **Dokumentierte Abweichung vom
   Plan-Schnipsel** (mit dem Advisor vorab abgestimmt, kein Alleingang): die Plan-Signatur zeigt
   nur `require_csrf(request, session)`, aber §2.7s Text selbst verlangt den Origin-Vergleich
   gegen `settings.base_url` — die Funktion trägt deshalb zusätzlich `settings: UiSettings` und
   `form_token: str | None` (der bereits aus dem Formular gelesene Wert, damit die Funktion den
   Request-Body nicht selbst konsumieren und nicht `async` werden muss — ein Aufrufer, der
   ohnehin `await request.form()` braucht, reicht das Feld einfach durch).
5. **`pages.py`** — `render_login_page()`/`render_error_page()` nach dem Muster von
   `authserver/templates.py` (kein Framework, kein `<script>`). **`render_logged_in_page()`
   zusätzlich zum Plan-Wortlaut, dokumentiert statt stillschweigend:** `SessionManager.rotate()`
   gibt den CSRF-Token nur EIN einziges Mal als Klartext zurück (`ui_sessions` speichert nur
   `csrf_hash`) — ein bloßer `302`-Redirect nach erfolgreichem Login hätte diesen Wert
   verworfen, und keine nachfolgende CSRF-geprüfte Anfrage (z. B. Logout) hätte je einen
   gültigen Wert vorlegen können. Die Seite trägt den Token als verstecktes Feld in einem
   Logout-Formular — Übergangslösung, **wird in Step 6 durch die echte App-Shell ersetzt**, kein
   dauerhafter Bestandteil des Designs.
6. **`routes_auth.py`** — `ui_auth_routes()`: `GET`/`POST /ui/login`, `POST /ui/logout`. Login
   dupliziert bewusst die enumerationssichere Prüfung aus `flows.py :: submit_consent()`
   (Argon2id unconditional, TOTP/Recovery nur wenn der Space existiert, dieselbe
   `LoginThrottle`/`login_attempts`-Tabelle) statt sie zu teilen — P5-G hält UI-Sitzung und
   OAuth-Consent architektonisch getrennt, eine gemeinsame Funktion wäre eine Kopplung, die der
   Plan hier nicht vorsieht. `/ui/invite/{token}` bewusst NICHT gebaut (siehe oben).

**Advisor-Fund, vor dem Commit behoben — derselbe Fehler wie in P5 Step 2, eine Zeile über der
Kopiervorlage übersehen:** die erste Fassung rief `store.set_totp_counter()` **innerhalb** des
TOTP-Zweigs auf, sobald `accepted_counter is not None` — also potenziell **vor** dem
Passwort-Gate weiter unten. Ein richtiger TOTP-Code mit falschem Passwort hätte damit das
aktuelle 30-Sekunden-Zeitfenster für den echten Nutzer verbrannt, exakt die Lehre, die der
Kommentar zwei Zeilen darüber in `flows.py` festhält (dort saß der Aufruf schon richtig, hinter
dem Gate) — beim Nachbau hier trotzdem in den falschen Zweig gerutscht. Fix: `accepted_counter`
vor der Verzweigung auf `None` initialisiert, `set_totp_counter()` erst nach
`throttle.reset(space)` (also nach dem vollständigen Erfolg) aufgerufen, genau wie in
`flows.py`. Neuer Test `test_correct_totp_with_wrong_password_does_not_burn_the_counter`
(`test_routes_auth.py`): falsches Passwort + gültiger TOTP-Code → 401, Zähler bleibt `None`.

**Tests, vier neue Testdateien plus `conftest.py` (`phase5_ui/tests/`, gemeinsame Fixtures — Muster
wie `test_flows.py`, `base_url` bewusst `https://…`: `__Host-`-Cookies verlangen `Secure`, httpx
sendet ein `Secure`-Cookie nicht über `http://` zurück, sonst sähen die Session-Tests grün aus,
ohne dass das Cookie je zurückreist):**
- `test_sessions.py` (5) — Cookie-Flags, kein `Domain`, Session-ID nie im Klartext in
  `ui_sessions` (direkte SQLite-Abfrage gegen die Testdatenbank, nicht nur Rückgabetyp-Prüfung),
  Idle-/Absolut-Timeout.
- `test_security.py` (7) — `require_csrf()` als reine Funktion (fehlender/falscher Token,
  fremde Herkunft, `Sec-Fetch-Site`-Ersatz bei fehlendem `Origin`, `GET` braucht keinen Token),
  CSP ohne `unsafe-inline`, `form-action` nur `'self'` (belegt: **nicht** die OAuth-Header).
- `test_routes_auth.py` (7) — Enumerationsschutz (falsches Passwort/unbekannter Space
  ununterscheidbar), Session-Rotation bei Login, Logout widerruft serverseitig, abgelaufenes
  Cookie wird beim Logout-Response gelöscht (`Max-Age=0`), Sicherheits-Header auf UI-Seiten,
  gemeinsame Fehlversuchsbremse mit dem OAuth-Consent-Login (fünf UI-Fehlversuche sperren auch
  einen anschließenden `flows.submit_consent()`-Aufruf für denselben Space), der
  TOTP-Zähler-Regressionstest oben.
- `test_isolation.py` (3, Akzeptanzkriterium §6.19/P5-F/P5-G) — `/mcp` ignoriert ein echtes,
  gültiges UI-Sitzungscookie (bleibt 401), `/oauth/authorize` liest niemals Cookies (identische
  Anfrage mit/ohne Sitzungscookie liefert dasselbe Login-Formular, kein abgekürzter Consent),
  `/api`-Bearer-Test als **dokumentierter Platzhalter** („nach Step 5 zu schärfen", Plan-Wortlaut
  wörtlich übernommen) — `/api/v1/*` existiert erst ab Step 5, ein Mount hier vorzugreifen wäre
  erfundener Scope; geprüft wird stattdessen, dass `SessionManager.load()` einen
  `Authorization`-Header schlicht ignoriert (kein Cookie → `None`, unabhängig vom Bearer-Wert).

**Verifiziert, nicht nur behauptet:** `pytest -q` (Repo-Wurzel, `pytest.ini` inklusive
`phase5_ui/tests`) → **436/436 grün** (414 zu Step-2-Ende, +22). `git diff` bleibt auf den
Tabu-Pfaden (`storage/`, `mcpserver/tools.py`/`permissions.py`/`server.py`) leer — `webui`
importiert in diesem Step nichts aus `mcpserver` (die P5-B-Ausnahme,
`permissions.OwnSpaceWritable`, kommt erst mit der REST-API in Step 5/6;
`test_webui_imports_exactly_one_mcpserver_symbol` deshalb bewusst noch nicht gebaut — ein Test
für „genau ein Import" wäre bei null Imports nicht aussagekräftig). `Done when` aus Plan §5
Step 3 („Login/Logout gegen eine In-Process-App durchgespielt") liegt buchstäblich vor:
`test_routes_auth.py` fährt echte `POST /ui/login` → `POST /ui/logout`-Rundläufe gegen eine aus
`ui_auth_routes()` gebaute `Starlette`-App, kein interner Kurzschluss über `SessionManager`
allein.

**Nächster Schritt (konkret):** Step 4 (Selbstverwaltung — Einladung, Passwort, TOTP, Recovery,
Connectoren: `webui/{account,reauth,passwords_policy}.py`, `webui/blocklist.txt`,
`authctl.py`-Erweiterungen). Danach der harte Gate vor Block B (Abnahmezeilen 1–9 live). Die
drei liegen gebliebenen Live-Aktionen aus Step 1/2 (S3/S4-Gegenprobe, Purge-Timer aktivieren,
Migrations-Runbook) bleiben unverändert offen, Sache des Nikingers, blockieren aber weiterhin
keinen Code-Step.

---

## Session stopped — 2026-08-02 (Step 2: Auth-Datenmodell Schema 2, `UserDirectory`, Migration)

**Für den nächsten, kalten Leser:** dritte Session der Phase, direkt im Anschluss an Step 1
(„go on" nach der Zusammenfassung der beiden noch offenen Live-Aktionen). Plan §5 Step 2s
eigene Reihenfolge (secretbox → Schema 2 + Store → `userdir.py` → `flows.py`/`app.py`-Umstieg →
Migrationsskript) wurde genau so durchlaufen. `pytest -q` stand zu Beginn bei 353/353, am Ende
bei **414/414** (+61, siehe Advisor-Nachtrag unten: zwei Tests kamen nach der ersten
412/412-Marke noch dazu, ein zweiter Advisor-Durchlauf fand einen echten Bug zwischen ihnen).

**Plan-Drift, vor dem Umbau geklärt (Advisor-Review vor Beginn):** keine — die Reihenfolge und
alle fünf Bauteile aus §2.2–§2.6 waren mit dem realen Repo-Stand deckungsgleich (Step 1 hatte
`UserDirectory`/Schema 2 bereits als „noch nicht gebaut" markiert, genau das ist jetzt
nachgeholt). Zwei Stellen, an denen bewusst über den Plan-Wortlaut hinausgegangen oder von ihm
abgewichen wurde, beide vorab mit dem Advisor abgestimmt:

- **Recovery-Code im OAuth-Consent-Formular** (§2.5, „ein Wert mit Bindestrich und Länge 11 wird
  als Recovery-Code geprüft") ist bereits in diesem Step verdrahtet, nicht erst in Step 4 — die
  Formerkennung lebt einzig in `userdir.py :: looks_like_recovery_code()`, `flows.py` leitet sie
  nicht selbst her. Wichtiger Fallstrick, den der Advisor benannte: ein Recovery-Login hat keinen
  TOTP-Zähler (`accepted_counter` bleibt `None`), `store.set_totp_counter()` darf deshalb NICHT
  mehr unbedingt nach jedem Erfolg laufen (vorher tat es das) — sonst würde ein Recovery-Login
  stillschweigend den TOTP-Replay-Zähler auf `None` zurücksetzen. Jetzt hinter
  `if accepted_counter is not None:` gattert, Regressionsgefahr in einem eigenen Testfall nicht
  extra geprüft (kein Recovery-Code existiert vor Step 4 für echte Nutzer, aber die Guard-Logik
  selbst ist über `test_totp_replay_is_rejected_without_burning_the_stored_counter` weiterhin
  abgedeckt, da dieser Test ausschließlich den TOTP-Zweig durchläuft).
- **`UserDirectory.__init__` prüft „DEK fehlt UND `users` nicht leer" selbst**, nicht
  `config.py` (der Plan nennt die Bedingung nur bei `secretbox.py`, ohne eine Datei festzulegen)
  — Begründung: das ist die Stelle, die tatsächlich entschlüsseln muss und bei jedem
  Prozessstart genau einmal läuft; `config.load_data_encryption_key()` bleibt eine reine
  Lesefunktion ohne Kenntnis vom `AuthStore`.

**Bauteile, in Reihenfolge:**

1. **`secretbox.py`** — AES-256-GCM (`cryptography.hazmat...aead.AESGCM`), `nonce || ciphertext`
   als ein `bytes`-Blob, `SecretBoxError` als einziger Fehlertyp (kein Unterschied nach Ursache
   nach außen, dieselbe Enumerationslogik wie `passwords.verify_password`).
2. **`config.py :: load_data_encryption_key()`** + `generate_/encode_/decode_data_encryption_key()`
   — dieselbe Verzweigung wie `users.load_users()` (`CREDENTIALS_DIRECTORY/auth-dek` zuerst,
   Keyring `nikinger-space`/`auth-dek` als Dev-Fallback), aber **kein** stiller
   Warn-und-Keyring-Fallback bei fehlender Datei: Abwesenheit ist hier entscheidungsrelevant für
   den Aufrufer (`UserDirectory.__init__`), nicht etwas, das diese Funktion selbst auflösen darf.
   `users.py`s Docstring-Behauptung „`keyring` wird nur hier importiert" korrigiert (gilt seit
   diesem Commit für zwei Module, unabhängig voneinander). **V28 geschlossen:** `cryptography`
   war bereits im `.venv` (49.0.0), jetzt exakt in `phase4_auth/pyproject.toml` gepinnt.
3. **Schema 2** (`store.py`) — vier neue Tabellen (`users`/`invites`/`recovery_codes`/
   `ui_sessions`), rein additiv, `SCHEMA_VERSION` `"1"`→`"2"` per `INSERT ... ON CONFLICT DO
   UPDATE` (vorher `INSERT OR IGNORE` — ein Prozess, der eine alte Schema-1-Datei öffnet,
   migriert jetzt automatisch beim ersten Start). Vollständige Methodenliste aus Plan §2.3
   (Nutzerakten/Einladungen/Recovery-Codes/UI-Sessions) 1:1 umgesetzt, neue Dataclasses
   `UserRow`/`InviteRow`/`SessionRow` in `models.py` (`SessionRow` trägt `session_hash`/
   `csrf_hash`, nie Klartext — dieselbe Hash-only-Disziplin wie Token/Codes, P5-K).
   **S7 dabei vollständig geschlossen:** `purge_expired()` deckt jetzt auch `ui_sessions`
   (absolut abgelaufen oder >7 Tage widerrufen) und `invites` (abgelaufen oder >7 Tage
   konsumiert) ab — die in Step 1 dokumentierte Lücke („Tabellen existieren erst in Step 2")
   ist damit geschlossen, `phase4_auth/CLAUDE.md`s S7-Zeile nachgezogen.
4. **`userdir.py`** — `UserDirectory.get()` liest live (kein Cache, **schließt O1 strukturell**:
   eine Provisionierung wirkt jetzt ohne Neustart), entschlüsselt `totp_secret_enc` mit AAD =
   Space-Name, fängt `SecretBoxError` ab (Log-Warnung, `totp_secret=None` statt Absturz) — **das
   ist S6s endgültige, strukturelle Schließung**, der `record.get(...)`-Übergangsfix aus Step 1
   ist jetzt entfernt (Zeile im Findings-Register bei `phase4_auth/CLAUDE.md` entsprechend
   nachgezogen: „geschlossen (P5 Step 1)" statt „strukturell erst in Step 2").
5. **`flows.py`/`routes.py`/`mcpserver/app.py`/`scripts/serve.py` auf `UserDirectory` umgestellt**
   — Advisor-Vorgabe befolgt: **verhaltensneutral**, nicht durch umgeschriebene Tests nur
   behauptet. In `test_flows.py`/`test_routes.py` änderte sich ausschließlich die
   `users`-Fixture-Konstruktion (jetzt `store.upsert_user(...)` + `UserDirectory(store, dek=...)`
   statt eines rohen Dicts) — alle Assertions blieben unverändert. **Zwei Ausnahmen, explizit
   dokumentiert statt still verschwunden:** `test_broken_user_record_yields_generic_login_failure`
   und `test_unknown_space_and_broken_record_are_indistinguishable` konnten ihren ursprünglichen
   Testfall (`{SPACE: {}}`, ein Dict ohne `"pwd"`/`"totp"`) nicht mehr herstellen — genau das IST
   S6s strukturelle Schließung (`store.get_user()` liefert nie ein unvollständiges Zwischending).
   Beide auf den jetzt einzig erreichbaren „kaputten Datensatz"-Fall umgestellt: ein TOTP-Seed,
   der mit einem ANDEREN DEK versiegelt wurde (z. B. nach einem DEK-Rotationsfehler) — beweist
   dieselbe Eigenschaft (generischer Fehlschlag, kein Absturz) unter der neuen Architektur.
   Neuer expliziter Test `test_flows_still_authenticate_with_userdirectory` (Plan-Namensvorgabe).
6. **`import_users_to_db.py`** — `--dry-run` Standard, `--apply` schreibt, `--force` überschreibt
   vorhandene Zeilen. Liest ausschließlich `load_users_from_keyring()` (nie das
   Credential-Snapshot). `totp_confirmed_at` übernimmt den ursprünglichen `created_at`-Wert (die
   Seeds sind live bewiesen, kein „unconfirmed"-Zustand für Bestandsnutzer). Bricht laut ab,
   wenn kein DEK geladen werden kann und der Keyring nicht leer ist.

**Kollateralberührungen außerhalb der Step-2-Dateiliste, dokumentiert (gleiche Kategorie wie
`oauth_smoke.py` in Step 1):** `phase2_mcp/scripts/serve.py` (Pflicht — `OAuthConfig.users`
ändert den Typ), `phase2_mcp/scripts/mcp_smoke.py` + `phase4_auth/scripts/oauth_smoke.py` +
`phase2_mcp/tests/{test_app,test_asgi_bearer,test_request_log,test_serve}.py` +
`phase4_auth/tests/test_oauth_smoke.py` (alle bauten `OAuthConfig(...users=...)` mit einem
rohen Dict). `phase4_auth/systemd/sharefyx-mcp.service` + `phase3_edge/tests/test_units.py`:
`LoadCredentialEncrypted=auth-users:...` entfernt (der Code liest diese Datei seit diesem
Commit nirgends mehr — dieselbe „totes Gewicht sofort abbauen"-Disziplin wie beim
`spaces.cred`-Fund in P4, nicht wie damals erst beim nächsten Unit-Umbau liegen gelassen),
`auth-dek:/etc/sharefyx/auth-dek.cred` dafür neu. `authserver/users.py :: load_users()` (die
Credential-Datei-Variante, nicht `load_users_from_keyring()`) ist jetzt echter toter Code —
bewusst NICHT gelöscht (außerhalb der Step-2-Dateiliste), Docstring korrigiert, vorgemerkt für
einen künftigen Rückbau, sobald `auth-users.cred`/der Keyring-Eintrag laut Migrations-Reihenfolge
unten formal abgelöst sind.

**Verifiziert, nicht nur behauptet:** `pytest -q` → **414/414 grün** (412 zu Sessionsende, +2 aus
den beiden Advisor-Nachträgen unten). Zusätzlich beide Smoke-Skripte real gelaufen (nicht nur
`pytest` grün behauptet, dreimal — einmal zu Sessionsende, je einmal nach jedem Advisor-Fund):
`mcp_smoke.py --json` → 12/12, `oauth_smoke.py --json` (In-Process-Default, echter
`UserDirectory`+DEK-Pfad) → **11/11** — der volle OAuth-Login-Fluss (Passwort + TOTP, jetzt über
verschlüsselte Seeds in `auth.sqlite3` statt einem Dict) funktioniert nach dem Umbau unverändert.
`git diff` bleibt auf den Tabu-Pfaden (`storage/`, `mcpserver/tools.py`/`permissions.py`/
`server.py`) leer.

**Zwei Advisor-Durchläufe vor dem Commit (dieselbe Session, wie in
`feedback_advisor_before_commit` festgehalten), drei echte Lücken gefunden, alle vor dem Commit
geschlossen, keine danach:**

1. Diese Datei dokumentierte Step 2 bereits als abgeschlossen, aber Root-`CLAUDE.md`s „Nächster
   Schritt" stand noch auf „Step 2" — dieselbe Drift-Kategorie, die diese Zeile in P4 schon
   dreimal betraf. Nachgezogen auf Step 3, mit datierter Korrekturnotiz statt stillem Fix.
2. Der neue `if accepted_counter is not None:`-Guard in `flows.py :: submit_consent()`
   (Recovery-Code-Zweig) war unbewiesen — der Session-Text behauptete, er sei durch
   `test_totp_replay_is_rejected_without_burning_the_stored_counter` gedeckt, aber dieser Test
   durchläuft laut eigener Beschreibung ausschließlich den TOTP-Zweig, nie den Recovery-Zweig.
   Neuer Test `test_recovery_code_login_does_not_touch_totp_counter` (`test_flows.py`) schließt
   das: Login mit einem Recovery-Code, danach `store.get_totp_counter(SPACE)` weiterhin `None`.
   Ohne diesen Test hätte eine Regression den TOTP-Replay-Zähler nach jedem Recovery-Login
   stillschweigend auf `None` zurückgesetzt — sicherheitsrelevant, nicht kosmetisch.
3. **Zweiter Durchlauf, echter Bug, nicht nur ein Test-Loch:** `users.consume_recovery_code()`
   mutiert (stempelt `used_at` in derselben Transaktion) und wurde VOR dem Passwort-Gate
   aufgerufen — ein Recovery-Code, korrekt eingegeben, aber mit einem Tippfehler im
   Passwortfeld, wurde dabei unwiderruflich verbrannt, ohne dass der Login gelang. Exakt das
   Spiegelbild der Lehre zwei Zeilen darunter im selben Modul („Zähler erst nach VOLLSTÄNDIGEM
   Erfolg hochsetzen"), nur auf der anderen Verzweigung übersehen. Fix: `totp_ok = password_ok
   and users.consume_recovery_code(...)` — Argon2id läuft weiterhin unconditional (Enumerations-
   schutz unberührt, ~55ms dominieren die paar µs SQLite-Lookup um Größenordnungen). Neuer Test
   `test_wrong_password_with_valid_recovery_code_does_not_burn_it`: falsches Passwort + gültiger
   Code → `ErrorPage`, derselbe Code funktioniert im nächsten Versuch mit korrektem Passwort noch.

Ein vom ersten Advisor-Durchlauf genannter Punkt (Schema-1→2-Migration gegen eine reale
Alt-Datenbank, nicht nur eine frisch angelegte) war bereits vorhanden
(`test_schema_migrates_from_v1_to_v2_without_data_loss`, baut eine echte Schema-1-DB von Hand,
öffnet sie über den normalen `AuthStore`-Konstruktor, prüft Datenerhalt UND Versions-Bump) —
falscher Alarm, im Advisor-Kontext fehlte lediglich der Diff-Ausschnitt, der das gezeigt hätte.

**Live-Runbook „Migration der Nutzerakten" (Nikinger-Aktion, Reihenfolge ist entscheidend —
Plan §2.6, Advisor-Vorgabe dieser Session):**

```
# 0) VORAUSSETZUNG, bevor irgendetwas installiert wird: der DEK muss existieren, BEVOR die
#    neue Unit-Zeile (LoadCredentialEncrypted=auth-dek:...) aktiv wird — sonst startet der
#    Dienst gar nicht mehr (dieselbe Falle wie spaces.cred in P4).
python -c "from authserver.config import generate_data_encryption_key, encode_data_encryption_key; \
  print(encode_data_encryption_key(generate_data_encryption_key()))" \
  | sudo systemd-creds encrypt --name=auth-dek - /etc/sharefyx/auth-dek.cred
sudo chmod 600 /etc/sharefyx/auth-dek.cred

# 1) Units installieren (bringt die neue auth-dek-Zeile UND entfernt die alte auth-users-Zeile)
sudo phase3_edge/scripts/install_units.sh
sudo systemctl restart sharefyx-mcp   # `users`-Tabelle ist noch leer -> UserDirectory(dek=...)
                                       # startet klaglos, aber noch niemand kann sich anmelden
systemctl status sharefyx-mcp

# 2) Migration, erst --dry-run, dann --apply (Backup vorher empfohlen, wie immer vor Schreiben
#    gegen die reale auth.sqlite3)
STATE_DIRECTORY=/var/lib/sharefyx python phase4_auth/scripts/import_users_to_db.py
STATE_DIRECTORY=/var/lib/sharefyx python phase4_auth/scripts/import_users_to_db.py --apply

# 3) Restart, damit UserDirectory die migrierten Zeilen sieht (O1 ist zwar geschlossen — kein
#    Cache mehr —, aber die Zeilen existieren ja erst nach diesem --apply-Lauf)
sudo systemctl restart sharefyx-mcp

# 4) Beide Nutzer melden sich am Connector an (UI kommt erst in Step 3/6) — ERST DANACH weiter.
#    Login niklas, Login fabian — beide mit unverändertem Passwort/TOTP.

# 5) Erst nachdem Schritt 4 für BEIDE bestätigt ist: alte Credential-Datei + Keyring-Eintrag
#    entfernen (nicht vorher — Lehre aus spaces.cred: eine Credential-Zeile und die Realität
#    dürfen nie auseinanderlaufen).
sudo rm -f /etc/sharefyx/auth-users.cred
python -c "import keyring; keyring.delete_password('nikinger-space', 'auth-users')"
```

**Nächster Schritt (konkret):** Drei Dinge stehen aus, alle Sache des Nikingers, keine davon
blockiert den nächsten Code-Step:

1. **Aus Step 1 weiterhin offen:** die S3/S4-Live-Gegenprobe gegen `token_families`
   (`resource`/`scope` der laufenden Verbindungen) vor dem nächsten Restart — siehe Absatz oben.
2. **Aus Step 1 weiterhin offen:** `sudo systemctl enable --now sharefyx-purge.timer`.
3. **Neu aus Step 2:** das Migrations-Runbook oben, in genau dieser Reihenfolge — kann mit (1)
   kombiniert werden, da beide denselben `install_units.sh`-Lauf und Restart teilen.

Code-seitig kann parallel weitergehen: Step 3 (Sessions, CSRF, Login-Seiten — neues Paket
`phase5_ui/` mit `webui/{config,security,sessions,pages,routes_auth,errors}.py`).

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

---

## Session stopped — 2026-08-02 (Step 0: Haushalt, Rückbau, Doku-Drift, P3 komplett ✅)

**Für den nächsten, kalten Leser:** erste Session der Phase. Der Nikinger bat um die ersten
Kommandos für den Phasenstart; Step 0 B/D (rein lesend) liefen direkt in dieser Session (das
Environment **ist** die VM — `savefyx-VMware-Virtual-Platform`, `/etc/sharefyx/*.cred`
vorhanden), Step 0 A (Rückbau) und C (Doku-Drift) sind Claude-Code-Arbeit und liefen im Anschluss
ebenfalls autonom, wie vom Nikinger freigegeben („start with the initial steps you can do now
without needing me"). Der Nikinger hat A.7 (`install_units.sh` + Restart + Live-Check +
`spaces.cred`-Löschung) noch in derselben Session live nachgezogen, plus einen eigenen
Restore-Check-Lauf und drei Lesezugriffe über den echten Connector — Details unten. **Step 0
ist damit vollständig abgeschlossen.**

**B — Verifikationsdurchlauf (vor jeder Änderung):** `pytest -q` → 347 grün (bestätigt den
dokumentierten Ausgangsstand). Alle `up:`/`down:`/Markdown-Links in allen 26 `.md`-Dateien lösen
auf (zwei harmlose False-Positives aus Inline-Code-Beispielen in
`docs/DOC_LAYERS_CONVENTION.md`, keine echten Links). Jede über 40 KB liegende `.md` ist korrekt
📕/📦. Jeder Phase-Head trug genau einen `## Session stopped`-Block. Jede getrackte `.md` hatte
eine Zeile in `docs/INDEX.md`.

**D — Umgebungsinventar:** Python 3.12.3, sqlite3 3.45.1, systemd 255, Tailscale 1.98.9 (Funnel
live auf Port 8765). Ports 8080/8081/9090 frei → Kandidat für Staging (**V36**). `cryptography`
liegt bereits im `.venv` (49.0.0, transitive Abhängigkeit von Authlib/joserfc/SecretStorage,
`AESGCM` importiert sauber) — **noch nicht** in einem `pyproject.toml` gepinnt, das ist Step 2s
Aufgabe (**V28** teilweise aufgelöst: Version bekannt, Pinning offen). Kein `vnstat` installiert
→ **V12** bleibt offen. 32 GB frei auf `/`.

**A — Rückbau `spaces.cred` + P2-Token-Reste** (`docs/concepts/PHASE4_CLOSEOUT_HANDOVER.md`
§4.5):

1. `phase4_auth/systemd/sharefyx-mcp.service`: Zeile `LoadCredentialEncrypted=spaces:
   /etc/sharefyx/spaces.cred` entfernt.
2. **Pfaddrift im Plan korrigiert, nicht blind übernommen:** der Plan nannte
   `phase2_mcp/scripts/export_space_map.py` — das Skript lag tatsächlich unter
   `phase3_edge/scripts/export_space_map.py` (P3 Step 3 hat es dort gebaut). Gelöscht wurde die
   reale Datei, nicht die im Plan genannte (die nie existierte).
3. `phase2_mcp/scripts/issue_token.py` gelöscht.
4. `phase2_mcp/mcpserver/credentials.py` auf `hash_token()` reduziert — `issue`/`revoke`/
   `load_space_map`/`load_space_map_from_keyring`/`save_space_map`/`credential_path`/
   `generate_token` sowie die Keyring-Konstanten entfernt, `hash_token` bewusst belassen
   (`asgi.py` dokumentiert die Byte-Identität mit `authserver.crypto.hash_secret`, Plan-Vorgabe).
5. `mcpserver/auth.py :: KeyringTokenResolver` entfernt (letzter Aufrufer war `TokenPathASGI`,
   selbst seit dem P4-Schnitt tot) — `SpaceResolver`-Protokoll bleibt stehen
   (`authserver.resolver.OAuthTokenResolver` erfüllt es strukturell).
6. `mcpserver/app.py`s Docstring korrigiert (behauptete noch, `KeyringTokenResolver` sei
   „weiterhin gebraucht von `issue_token.py`" — das Skript existiert nicht mehr).
7. Tests bereinigt: `test_auth.py` 4→1 (nur `test_principal_repr_hides_token` bleibt),
   `test_credentials.py` 12→1 (nur `test_hash_token_is_stable_hex64` bleibt),
   `test_units.py :: test_unit_loads_credential_encrypted` prüft jetzt zusätzlich die
   **Abwesenheit** der `spaces:`-Zeile statt nur ihre Anwesenheit.
   **`pytest -q` → 333 grün (347 − 14, Aufschlüsselung oben, keine neue Lücke).**
8. **Nikinger-Aktion, live ausgeführt (2026-08-02, gleiche Session):** `restore_check.sh`
   selbst wiederholt (identischer HEAD, `ok:true` — siehe Nebenfund unten), danach
   `sudo phase3_edge/scripts/install_units.sh` → `sudo systemctl restart sharefyx-mcp` →
   `curl http://127.0.0.1:8765/health` → `{"status":"ok",…,"uptime_s":14}` → erst danach
   `sudo rm -f /etc/sharefyx/spaces.cred`, exakt in dieser Reihenfolge. **Step 0 A damit
   vollständig.**

**Nebenfund, jetzt echte Abnahme statt nur Kandidat:** P3 Zeile 13 (Restore-Nachweis) war seit
dem 2026-07-29-Handover offen. Claude Code hatte `restore_check.sh` zunächst selbst gegen das
frischeste Bundle gefahren (`ok:true`) — bewusst nur als Kandidatenbeleg gewertet, weil der
Session-Auftrag „jeden End-to-End-Test gegen das echte Datenverzeichnis" dem Nikinger vorbehält
(Advisor-Fund dieser Session). Der Nikinger hat den identischen Befehl danach selbst ausgeführt
(`head: 3756c26a7d826def1246bb4dc826e9ee10e764b3`, `ok:true`, identisch zum Kandidatenlauf).
**Phase 3 steht damit bei 13/13, Status ✅.** `phase3_edge/CLAUDE.md`, `ROADMAP.md`,
Root-`CLAUDE.md` und `docs/INDEX.md` nachgezogen.

**Live-Verifikation nach dem Restart (Nikinger, über den echten Connector):** drei Lesezugriffe
gegen die neu gestartete Unit — `list_spaces` (`niklas`: 7 Items/`writable:true`, `fabian`:
2 Items/`writable:false` — Rule 4 sichtbar korrekt) und `search_items` (3 aktive Items im
eigenen Space, jüngstes `P4 TTL-Test` v2 vom 2026-07-30 — derselbe Datensatz wie beim
P4-Abnahmezeile-9-Beweis, also Kontinuität über den Rückbau-Restart hinweg belegt). Kein
Schreibzugriff (bewusst, war nicht gefragt).

**Zwei P5-relevante Beobachtungen aus diesem Live-Check, für spätere Steps vorgemerkt:**

- **`list_spaces`s `item_count` zählt inklusive Archiv, `search_items`s Default nicht.**
  `niklas` zeigt 7 in `list_spaces`, aber nur 3 aktive Treffer in `search_items`
  (`include_archived=false` per Default) — kein Bug, aber ein UI-Fallstrick: die Rail (Step 6)
  würde „7" zeigen, während die Liste 3 Zeilen hat. **Für Step 6 vormerken:** entweder beide
  Zahlen anzeigen (`3 von 7`) oder `item_count` explizit als „inklusive Archiv" beschriften,
  bevor irgendein UI-Zähler daraus abgeleitet wird.
- **`fabian`s Space hat bereits zwei echte Items**, kein Leerzustand. Für die
  Zwei-Personen-Abnahme (Akzeptanzkriterium 12/17: fremder Space read-only, keine
  Schreib-Bedienelemente im DOM) heißt das: es gibt schon echten Testinhalt, kein
  künstlich anzulegender Leerraum nötig, wenn Fabian in Step 9 einsteigt.

**C — Doku-Drift geschlossen:**

1. `ROADMAP.md`: P5-Zeile ⬜→🔄 (mit Status-Absatz + Scope-Erweiterung Auth-Selbstverwaltung),
   P3-Zeile 🟡→✅ (Restore-Nachweis-Nachtrag), `down:`-Liste um die P4-/P5-Pläne ergänzt (fehlten
   bisher, kleine unabhängige Lücke, beiläufig geschlossen).
2. Root-`CLAUDE.md`: „Aktive Phase" auf P5 umgehängt (P4-Absatz bleibt als abgeschlossene
   Historie stehen, „Nächster Schritt" nachgezogen), `down:` auf `phase5_ui/CLAUDE.md`,
   `updated:` gesetzt. „Noch nicht entschieden": der Web-UI-Punkt ist mit P5-V entschieden,
   datierte Korrekturnotiz statt ersatzloser Streichung.
3. `README.md`: **[VERIFY] V34 aufgelöst** — der Snapshot war bereits größtenteils überarbeitet
   (Architekturdiagramm, „ab Phase 5" waren schon korrekt), aber der komplette
   „Token ausgeben, rotieren, widerrufen"-Abschnitt beschrieb noch die jetzt gelöschten Skripte.
   Ersetzt durch einen Abschnitt, der auf OAuth 2.1 + DCR (P4) und die kommende
   Selbstverwaltung (P5 Step 4) verweist. Setup-Callout auf den aktuellen Fünf-Phasen-Stand
   gehoben.
4. `docs/INDEX.md`: neuer Abschnitt „Active phase (5 — Web-UI)" mit den Zeilen für
   `phase5_ui_plan.md`, `PHASE4_CLOSEOUT_HANDOVER.md` und diesen Phase-Head; P4 bleibt unter
   „Completed phases" (war dort schon korrekt einsortiert, keine Änderung nötig); Größenangaben
   für `phase3_edge/CLAUDE.md`/`SESSIONS_ARCHIVE.md` und `phase4_auth/CLAUDE.md`-Zeile
   (P3-Status) nachgezogen.

**Nächster Schritt (konkret):** Step 0 ist vollständig — keine offenen Punkte mehr, weder
code- noch live-seitig. Step 1 (Sicherheitsbefunde S2–S8, `docs/concepts/
P4_SECURITY_REVIEW_2026-07-29.md` vorher lesen) kann beginnen, sobald der Nikinger grünes Licht
gibt.

---

