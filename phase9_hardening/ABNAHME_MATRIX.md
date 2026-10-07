---
status: live
purpose: Abnahmematrix der Phase 9 (P9-1 – P9-82) und [VERIFY]-Bilanz (V145 – V184) — jede Zeile mit Stand und Beleg, jeder Marker mit Antwort oder offenem Grund
read-when: beim Gate/Z-Checkout, bei jeder Frage „ist das schon abgenommen?", wenn eine Abnahmezeile oder ein [VERIFY] aus den Plänen nicht auffindbar ist, oder wenn jemand eine Zeile auf ✅ setzen will, für die es keinen Beleg gibt
detail: L2
up: ./CLAUDE.md
down:
  - ../docs/concepts/phase9_hardening_plan.md        # P9-1 – P9-58, §13-Register, §15 P10-Liste
  - ../docs/concepts/phase9_hardening_block_doing_plan.md   # P9-59 – P9-68, V173 – V178
  - ../docs/concepts/phase9_hardening_block_trace_plan.md   # P9-69 – P9-82, V179 – V184
  - ./step_a/RUNBOOK_STEP_A.md                       # Step-A-Ablauf A0b – A9, Abnahme P9-10 – P9-15
  - ./step_b/RUNBOOK_STEP_B.md                       # Step-B-Ablauf B0 – B3, Abnahme P9-16 – P9-20
  - SESSIONS_ARCHIVE.md                              # die Herleitung jeder Zeile im Wortlaut
updated: 2026-10-07 (**Portscan von außen eingetragen**: P9-11 und P9-94 ⬜ → ✅, Bilanz 104 ✅ · 12 ⚠️ · 1 ⬜ — vier Läufe vom MacBook plus ein Kontrolllauf, Rohausgabe `probes/p9_11_portscan_2026-10-07.txt`. Der `21/tcp open` auf Heim-IP und VPS ist ein **Pfad-Artefakt** (antwortet auch für `1.1.1.1` und `9.9.9.9`); die alte Gegenprobe „alles `filtered`, genau 8765“ datiert korrigiert; **Lauf 4 `open`** ist kein Gegenlauf zu V162 B (Listener ist `socat`), widerlegt aber die ACL-Prämisse des Mini-Plans — Befund für P10) | 2026-10-06 (**Nachsatz aus der dritten Sichtprüfung**: +1 Zeile **P9-120** (Lock P9-BF, Bild 08) mit **1 ✅** — das Kästchen der Space-Zeile ragt 8 px nach links, damit der Text innen wieder den Standardabstand hält (innen vorher **1 px links** gegen **9 px rechts**), die Beschriftung bleibt bündig mit dem Titel. Bilanz **102 ✅ · 12 ⚠️ · 3 ⬜** · **drei Wächter umgeschrieben, keiner gelöscht**: der Abstand-Wächter prüft `margin` **namensgenau** statt per Substring (`margin-bottom` stand auf keiner Verbotsliste), die Station P9-117 rechnet **beide** Polster, und die Verbotsliste trägt die drei `margin`-Langformen) | 2026-10-06 (**dritte Bildsichtung gebaut** — Abnahme **P9-116–P9-119** mit **4 ✅** statt der vier notierten, **nicht gebauten** Zeilen P9-112–P9-115: **P9-112 ist widerrufen** (der Nikinger hat den Auftrag auf „nur bei Spaces verwalten" eingeschränkt), die drei anderen sind abgelöst, weil ihre Nummern inzwischen etwas anderes prüfen; die Zuordnung steht als Tabelle im Abschnitt · **Bilanz 101 ✅ · 12 ⚠️ · 3 ⬜** · **sechs Befunde ohne Abnahmezeile**, darunter `box-sizing: border-box`, die Sammelregel und eine Station, die den eigenen Fehler nicht bemerkte · **datierte Korrektur:** die 1246 `pytest`-Tests des Vortages sind **1241** gemessen) | 2026-10-03 (**A7a + A7 + A8 gefahren** — Nikinger-Schritte, von M3 vorbereitet und gemessen; P9-10b ✅ · P9-12 ✅ · P9-13/V150 ⚠️ „1 von 2 Konten") · **A7a** = der risikoarme Vorlauf nur über `ALLOWED_HOSTS` (kein `resource`-Wechsel, Token bleiben gültig): neu lokal 200 · alter Funnel lokal 200 · **extern `https://sharefyx.eurofyx.com/health` 200 mit `ssl_verify_result=0`**, JSON `{"status":"ok",…}` — vorher an derselben Stelle 400 bei gültigem TLS · **A7** = der Schnitt: `PUBLIC_BASE_URL` auf die Domain, `LEGACY_ORIGIN`/`LEGACY_UNTIL=2026-10-17` dazu; `issuer` und alle drei Endpunkte zeigen auf die neue Domain, Start ohne Traceback · **A8**: Konto niklas liefert `list_spaces` über die neue Adresse, das zweite steht aus · **P9-15 bleibt ⬜** und gehört an den Deploy-Tag (`health_gate.sh` authentifiziert) · **Befund 4 bestätigt**: der A7-Restart entwertet alte Token (`resolver.py:48`), die Neuanmeldung war zwingend | 2026-10-03 (**Step D belegt** — zweite Fassung, opencode/M3, **kein Produktcode-Touch**, kein Deploy) · **P9-28/P9-29/P9-30 von ⚠️/⬜ auf ✅**: die Browser-Probe `p9_step_d_self_check.py` (Plan-§11 GA2-Station 1, die erste von dreien, die nie lief) fährt **16/16** gegen eine eigene TLS-Wegwerf-Instanz auf Port 18781 · **echte Maus-Input-Pipeline**, nicht `dispatchEvent` — Station 2 misst den vom Browser erzeugten Ereignisstrom (`dragstart=1, dragover=19, drop=1`, Item-ID im `dataTransfer`), weil sonst nur der Listener belegt wäre · **P9-30 als berechneter Stil** (`dashed`, `rgb(62,141,243)`) plus zwei Bilder, nicht als Klassennamen · **zwei Gegenläufe liegen rot im Repo** (G1 Space-Bindung raus → 5 Stationen rot, 6–9 grün; G2 `fullscreenElement`-Guard raus → Station 9 rot), mit `--report`/`--screenshots-dir` getrennt, damit kein Gegenlauf den Erfolgsbeleg überschreibt (derselbe Fehler wie beim trace-Block 2026-10-02) · **6 Wächter** in `test_step_d_drop_target.py`, Deckung in **beiden** Richtungen (jede ✅-Zeile braucht eine Station, jede Station eine existierende Zeile) · **Bilanz an diesem Tag 68 ✅ · 9 ⚠️ · 6 ⬜** (der heutige Stand steht weiter unten, er wandert) · **P9-27 bleibt ⬜** und das ist eine Eigenschaft: kein WebKit-Binary, natives Vollbild nicht automatisierbar · **drei eigene Fehler im selben Commit behoben**: der Ereigniszähler zählte sich selbst (`start=3, over=57` für einen Zug — Listener bei jedem `evaluate` neu registriert), `store.create()` **hängt** an statt zu leeren (der zweite `start` sah jedes Item doppelt), und die erste Fassung des neuen Tests war rot, weil er `dispatchEvent` im **Docstring** verbot — Wächter läuft jetzt über `tokenize`, nicht über Rohtext | 2026-10-03 (erste Fassung, Gate/Z-Doku-Hälfte Nummer zwei, opencode/M3, **kein Code-Touch**, kein Deploy) — **82 Abnahmezeilen (83 Tabellenzeilen, P9-10 geteilt): 65 ✅ · 10 ⚠️ · 8 ⬜** und **34 belegte [VERIFY]-Einträge**, nicht 40 (V167–V172 sind nie belegt) · **P9-56/57/58 heute gemessen**: Tabu-Diff hat **einen** unangekündigten Treffer (`phase7_spaces_admin/tests/test_space_removal.py`, 17 Z.) · `pytest` 1169, `ui_budget` 5/5 (155,2 KB), `doc_health` 0/0/0/0 · **P9-14 heute geschlossen** (Funnel-Host live 200), P9-10b heute gemessen (weiter 400, erwartet bis A7) · **V146/V148/V155 heute beantwortet**, V182/V184 am Code · **zwei Nummerkollisionen gefunden** (V162, V163 je zweimal vergeben)
---

# Abnahmematrix Phase 9 — P9-1 … P9-82 und `[VERIFY]`-Bilanz V145 … V184

Diese Datei ist der **eine** Ort, an dem steht, welche der 82 Abnahmezeilen der Phase 9 mit welchem
Beleg stehen. Sie ist **L2, nicht Archiv** — die Phase läuft, die Zeilen ändern sich noch. Herkunft
jeder Zeile: Plan §2.5/§3.4/§4.4/§5.6/§6.4/§7.5/§8.8/§9.6/§10/§14 plus die beiden Mini-Pläne;
Herleitung im Wortsinn in `SESSIONS_ARCHIVE.md`. **Nikinger-Entscheidung 2026-10-02:** die Matrix
kommt hierher und nicht in den Phase-Head — der Head liegt über dem Softcap, und ein 82-zeiliges
Archiv hineinzuschreiben hieße, das Falsche zu tun.

## Stand in einem Satz

**117 Tabellenzeilen für 117 Abnahmezeilen: 104 ✅ · 12 ⚠️ · 1 ⬜** (P9-10 in zwei prüfbare Hälften
geteilt; seit 2026-10-05 kommen der **settings-Block** P9-83–P9-95 mit 12 ✅ und **einem** ⬜
dazu — P9-94, der Portscan, ist ein Schritt des Nikingers und durch keinen Test ersetzbar —,
sein **Nachtrag** P9-96–P9-102 aus der Bildsichtung mit **5 ✅ und 2 ⚠️**, und die **dritte
Bildsichtung** P9-103–P9-111 mit **9 ✅**. Die beiden ⚠️ sind
**keine offenen Punkte**: P9-97 trägt die vom Nikinger entschiedene Abweichung im linken
Polsterwert, P9-99 den gemessenen Umweg (`justify-content` statt des im Plan genannten, wirkungslosen `text-align`). **A7+A8 sind am 2026-10-03 gefahren** (A7a als risikoarmer Vorlauf, dann A7, dann A8):
P9-10b und P9-12 sind **beide ✅**. *Datierte Korrektur 2026-10-07:* hier standen **3** offene
Zeilen (P9-11, P9-13/V150, P9-94). **P9-11 und P9-94 sind seit dem 2026-10-07 ✅** — der
`nmap`-Gegenlauf von außen ist gelaufen (Mini-Plan §5, vier Läufe plus ein Kontrolllauf, Grenze in der
P9-11-Zeile). Die **eine** offene Zeile ist P9-13/V150, das zweite Claude-Konto. **Kein ⬜ ist offene Code-Arbeit** — und
**er blockiert die Phase nicht**: P9-13 braucht ein
zweites Konto, und ein Schritt, den nur ein Mensch mit einem Konto tun kann, ist ein Termin, kein
Blocker (Plan §0.1a; die Regel steht auch in der Wurzel-`CLAUDE.md` §Working style). *Datierte
Korrektur 2026-10-05, zwei Sätze:* hier stand „**P9-15** ist der authentifizierte Latenzvergleich
und gehört an den **Deploy-Tag**" — **falsch, die Zeile ist seit dem 2026-10-03 ⚠️ und gemessen**
(die drei Läufe sind gefahren; der Vergleich gegen 372,9 ms war nicht möglich, V151), und der
Deploy schließt sie **nicht** (`health_gate.sh` liefert Läufe, kein brauchbares Kriterium).
Und der Halbsatz „seit dem 2026-10-04 ist **kein ⬜ ein Personenschritt**" war mit P9-94 falsch
— zwei der drei ⬜ sind genau das. Die drei Zeilen, die am 2026-10-03 durch die Step-D-Probe von ⬜/⚠️ auf ✅ gewandert
sind, waren vorher ausdrücklich als „strukturell erfüllt, nicht am Gerät belegt" geführt — der
Unterschied zwischen beidem ist der ganze Gegenstand dieser Matrix.

## Statusregel (was ein ✅ hier bedeutet)

| ✅ | erfüllt, **und der Beleg steht in der Spalte rechts** — Testname, Probe-Datei, Journalzeile, Bild oder eine heute ausgeführte Messung. „Würde beim nächsten Lauf stimmen" ist kein ✅ |
| ⚠️ | erfüllt **mit benannter Abweichung**: andere Form als im Plan, Testzahl über der Plan-Zahl, gegenstandslos am gewählten Anker, oder zum Bauzeitpunkt erfüllt und heute überholt |
| ⬜ | nicht erfüllt, mit Grund und Zuständigkeit. Ein ⬜ ohne Begründung ist ein Befund gegen dieses Dokument |
| ersetzt | **in P9: 0.** Wo eine Planzeile praktisch nicht mehr greift (P9-10 geteilt, P9-31 gegenstandslos), steht ⚠️ mit Begründung — eine Ersatzzeile, die man abnehmen kann, gibt es dort nicht. (P9-28 stand bis zum 2026-10-03 unter dieser Ausnahme und ist heute eine normale ✅: gegenstandslos war nur die **Form** der Nicht-Regression, nicht die Zeile) |

**Zeilen mit `pending: Deploy v3.1.1`** sind nicht ⬜, wenn ihr Kriterium gegen eine Wegwerf-Instanz
messbar war — sie sind ✅ mit dem Zusatz „live bewiesen erst mit v3.1.1". Die Liste steht am Ende.

---

## Step 0 — Doku-Fundament (P9-1 … P9-9)

| # | Kriterium | Stand | Beleg |
|---|---|---|---|
| **P9-1** | Phasenverzeichnis existiert, beide `.md` mit Card und INDEX-Zeile | ✅ | `CLAUDE.md` + `SESSIONS_ARCHIVE.md` mit L1-Card, INDEX-Abschnitt „Phase 9" mit beiden Zeilen; `doc_health` heute **0 Befunde** |
| **P9-2** | `rotate_index_updates.sh` läuft, alle vier Gegenproben grün | ✅ + datierte Nachtrags-Korrektur | Vier Gegenproben (a) Byte-Buchhaltung (b) `cmp` der Reassemblierung (c) jeder rotierte Eintrag byte-identisch im Archiv (d) `---` auf eigener Zeile, + `test_rotate_index_updates.py`. **Nachtrag 2026-10-02:** der erste *echte* Lauf rotierte 1 von 3 Fäden, weil einer ein `updated: `-Präfix trug, das der Split-Anker nicht sieht — „verlustfrei" war nur *im geschnittenen Teil* wahr. Behoben: **Gegenprobe (e)** (Abbruch bei einem zweiten Präfix) + 2 Tests; (e) entfernt → genau der Abbruch-Test rot |
| **P9-3** | `docs/INDEX.md` unter dem Größen-Kriterium **nach** Aufnahme aller P9-Zeilen | ✅ **geschlossen 2026-10-03 — mit neu baseliniertem Kriterium** | **Nikinger-Entscheidung 2026-10-03: die datierten Nachträge wandern in ein L3-Archiv, das Kriterium wird vom P8.6-Wert 38.912 B auf den 40-KiB-Softcap (40.960 B) neu baseliniert.** Der alte Wert stammte aus P8.6 Plan 2 §1.2 für eine Datei mit weniger Zeilen und war **per Kürzen unerreichbar** — gemessen am 2026-10-03, nicht vermutet: Stand **71.573 B**, davon **37.391 B datierte Nachträge in 43 von 93 Einträgen** (über die halbe Datei), und selbst ein Cap von 300 B je Eintragszeile ergäbe **39.971 B**. Gebaut: `docs/INDEX_ENTRIES_ARCHIVE.md` (verbatim, ein Abschnitt je Karte in Kartenreihenfolge) + `scripts/archive_index_entries.sh` mit **fünf Gegenproben**, darunter die **byteweise Reassemblierung des Originals** und (d) „kein datierter Nachtrag bleibt im INDEX", die Verschieben von Weglassen unterscheidet · **71.573 → 38.299 B** (Vergleich: Phasenstart `06ab4f6` **38.822 B**, damals ✅), die Karte damit zum ersten Mal seit `06ab4f6` unter dem Softcap · **Wächter** `test_index_archive.py` mit **vier** Skript-Gegenproben · **was diese Zeile jetzt nicht mehr behauptet:** die `updated:`-Kette der Karte sei die Restmasse — sie hat 1.155 B und war am 2026-10-03 rotiert, wer die Datei rotieren wollte hätte die falsche Stelle angefasst |
| **P9-4** | Die fünf Links in `…_h_r_3_escalation.md` lösen auf | ✅ | repariert (drei `./`, zwei `../../`); `updown_links` heute **0 Befunde** über alle `.md` |
| **P9-5** | Beide Mini-Pläne tragen eine L1-Card | ✅ | `phase8_6_ui_polish_block_g_r_plan.md` + `…_block_h_r_plan.md`, beide `status: snapshot` |
| **P9-6** | Die `ROADMAP.md`-INDEX-Zeile nennt die reale Größe und P9 | ⚠️ **beim Bau korrigiert, seither wieder stale** | damals 42.080 B, heute `ROADMAP.md` **48.498 B** — die Oversize-Benennung steht, die Zahl nicht. Straffung bleibt Step-Z-Arbeit |
| **P9-7** | Genau ein `screenshots_latest/`-Pfad, begründet gewählt | ✅ | `docs/screenshots_latest/` entfernt (alle sechs Symlinks dort waren tot), die Root-Instanz bleibt. **Nachtrag 2026-09-30:** die drei Tailscale-Arbeitsdateien des Nikinger blieben bewusst außen — eine enthielt die Knotenliste des Tailnets |
| **P9-8** | `doc_health.py` läuft, `test_doc_health.py` grün, alle vier Prüfungen 0 Befunde | ✅ **heute gemessen** | `index_lines 0 · header_cards 0 · updown_links 0 · oversize 0` (2026-10-03); der Wächter kennt die drei `oversize`-Fälle (benannt / unbenannt / stale benannt) |
| **P9-9** | `pytest` ≥ 995 (Step 0 addiert die neuen `doc_health`-Tests) | ✅ | **995 passed in 185,98 s** (2026-09-20, V147) → 1008 nach Step 0; **heute 1169 passed in 218,31 s**. Nebenbefund von damals, der P9-9 erst erfüllbar machte: `pytest.ini` listete `phase9_hardening/tests` nicht |

## Step A — Echte Domain über einen eigenen VPS (P9-10 … P9-15)

> **Datierte Plan-Korrektur 2026-10-01:** P9-10 war *eine* Zeile („200 **und** gültiges
> LE-Zertifikat") und ist damit **zwei** — die Zertifikats-Hälfte gehört Caddy (A4), die
> `200`-Hälfte `SPACE_ALLOWED_HOSTS` (A7). Der Wortlaut ist nicht abgeschwächt, sondern in zwei
> prüfbare Hälften zerlegt (dieselbe Form wie Befund 2: `/health` statt `/healthz`).

| # | Kriterium | Stand | Beleg |
|---|---|---|---|
| **P9-10a** | `/health` über die eigene Domain, **TLS-Hälfte** | ✅ | **heute nachgemessen**: `CN=sharefyx.eurofyx.com`, `issuer=Let's Encrypt YE1`, gültig 01.10.–30.12.2026; `curl -w '%{http_code} %{ssl_verify_result}'` → `400 0` — die Kette steht, der `400` ist Befund 8 |
| **P9-10b** | `/health` antwortet 200 | ✅ **geschlossen 2026-10-03 (A7a)** | **A7a ausgeführt, der risikoärmere Vorlauf:** nur `ALLOWED_HOSTS` bekam `sharefyx.eurofyx.com` dazu, **kein** `resource`-Wechsel, deshalb blieben die Token gültig. **Gemessen, dreifach:** neu lokal `200` · alter Funnel lokal `200` (Gegenprobe P9-14) · **extern `https://sharefyx.eurofyx.com/health` → `200` mit `ssl_verify_result=0`**, JSON `{"status":"ok",…}`, dazu 6× `GET /health status=200` im App-Journal. Die **Vorher**-Messung desselben Aufrufs war `400 Invalid host header` bei gültigem TLS — das ist der ganze öffentliche Weg als Beweis: Caddy terminiert, das Zertifikat gilt, die 400 kam aus dem Prozess |
| **P9-11** | `nmap` gegen die **Heim**-IP zeigt keinen offenen Port | ✅ **gemessen 2026-10-07, mit benannter Grenze** | Vier Läufe vom MacBook des Nikingers nach Mini-Plan §5, Rohausgabe verbatim in `probes/p9_11_portscan_2026-10-07.txt`. **Lauf 1** (Hotspot, Tailscale aus) gegen die Heim-IP `176.2.194.125` (am Scan-Tag auf der VM per `ifconfig.me` bestätigt; der Plan nannte noch `176.2.220.64`, die IP wechselt): **999 `filtered`, ein `21/tcp open`**. **Grenze, benannt:** Port 21 ist auf diesem Pfad **nicht beobachtbar**. Derselbe `21 open` erscheint mit fast gleicher Latenz (3,6 / 3,8 ms) beim VPS, und der **Kontrolllauf** (Hotspot, Tailscale aus) zeigt `21/tcp open … syn-ack` auch gegen `1.1.1.1` **und** `9.9.9.9` — etwas auf dem Mobilfunkpfad beantwortet 21 für jedes Ziel. Von der VM aus: **kein** Listener auf 21 (`ss -tln`), und eine TCP-Verbindung zu `217.160.128.146:21` läuft ins Timeout. Die VM hat **keine globale IPv6** (nur die Tailscale-ULA), der IPv4-Scan deckt die Heimseite also vollständig ab. **Lauf 3** (Heim-WLAN) `192.168.68.175`, 8765 + 8000–9000: alle 1001 Ports `closed` (RST), **8765 nicht `open`** — die App bindet `127.0.0.1`. **Lauf 4** (Hotspot, Tailscale an) `100.93.43.122:8765`: **`open`** — Befund siehe V162 *(Lesart B)*. *Datierte Korrektur 2026-10-07:* die Gegenprobe hier sagte „`192.168.68.175` alles `filtered` **und** `100.93.43.122` genau 8765“. **Beides ist nicht gemessen und gilt nicht:** das LAN antwortet `closed` (RST, keine Host-Firewall), Lauf 3b (alle Ports, nicht im Plan) zeigt **sechs** offene LAN-Ports auf `0.0.0.0` (7070, 7777, 47984/47989/47990/48010 — Sunshine und zwei nicht zugeordnete; Hygiene-Punkt für P10, **nicht angefasst**), und Lauf 4 prüfte nur `-p 8765`, „genau“ ist also unbelegt (`ss` zeigt auf der Tailnet-IP außerdem 443, 4096, 33210). **Es gilt das engere Kriterium aus Mini-Plan §5:** Heim-IP ohne offenen Port, LAN 8765 nicht `open`. |
| **P9-12** | `/.well-known/oauth-authorization-server` liefert den neuen `issuer` | ✅ **geschlossen 2026-10-03 (A7)** | **gemessen:** `{"issuer":"https://sharefyx.eurofyx.com","authorization_endpoint":"…/oauth/authorize","token_endpoint":"…/oauth/token","registration_endpoint":…}` — **alle vier** Felder aus der Basis-URL, wie V149 vorhergesagt hat. Gegenprobe derselben Route über A7a hinweg: dort stand noch der **alte** `issuer`, also hat A7a nachweislich nichts am `resource` bewegt. Der Schnitt war die Ursache, nicht ein Nebeneffekt |
| **P9-13** | `list_spaces` aus **beiden** Claude-Konten über die neue Adresse (V150) | ⬜ **zurückgestellt, wandert nach P10 — kein Blocker** (niklas ✅, zweites Konto nicht umgestellt) | **niklas: echter Connector-Aufruf über `https://sharefyx.eurofyx.com/mcp` ✅** — die Zeile ist damit **nicht** abgenommen, weil sie **beide** Konten verlangt; was fehlt, ist ein Konto, kein Code. **Nikinger-Entscheidung 2026-10-04: zurückgestellt, wandert nach P10, und ausdrücklich **kein** Phasen-Blocker** (Plan §0.1a; die Regel steht auch in der Wurzel-`CLAUDE.md` §Working style). **Die Begründung, die man merken muss:** ein Schritt, den nur ein Mensch mit einem Konto tun kann, ist kein Blocker, er ist ein Termin. Ein echter Blocker wäre ein **Code**-Fehler oder ein **Mess**-Befund. Die Gegenprobe der Gegenrichtung (Reihenfolge: erst das zweite, wenn das erste steht) bleibt mit der Zeile zusammen in P10. **Befund 4 hat sich bestätigt:** der A7-Restart hat die alten Token entwertet (`resolver.py:48` — „Token für eine andere Ressource ausgestellt"), der Neuanmeldung über die neue Adresse war zwingend, **kein** Neustart-Fehler. **Gegenprobe der Gegenrichtung steht noch aus:** das zweite Konto wird erst umgestellt, wenn das erste steht (sonst ist der Zustand halb umgestellt und die Fehlersuche unbrauchbar) |
| **P9-14** | Der Funnel-Hostname antwortet weiterhin; das Runbook beschreibt den Rückfall in nummerierten Schritten | ✅ **heute geschlossen** | **gemessen** `curl …tail4a8b49.ts.net/health` → `200`; **geschrieben** Runbook §2 A9, vier nummerierte Schritte inkl. der Korrektur zu Befund 4 (Rückweg = dieselbe A7/A8-Sequenz rückwärts, weil auch er die `resource` wechselt). **Befund 5 bleibt und ist keine offene Zeile:** nach A7 liest der Funnel, jeder Schreibvorgang der Web-UI über ihn wird 403 (CSRF-Origin, `security.py:84`) |
| **P9-15** | `/api/v1/overview`-Zeit gemessen und gegen 372,9 ms verglichen (V151) | ⚠️ **2026-10-03 gemessen — die Abweichung IST der Befund: der im Kriterium genannte Vergleich war nicht möglich** | **Gemessen, drei Läufe je Bein, aus dem Browser mit echter UI-Session, `status` 200 in allen sechs Läufen:** eigene Domain **3184 / 3176 / 3136 ms**, alte Funnel-Adresse **3074 / 3060 / ~~6051~~**. **Die Referenz 372,9 ms stammt aus `ui_budget.py` und ist nie über Funnel gemessen worden** — das Skript misst **in-process** über `httpx.ASGITransport` gegen ein `TemporaryDirectory` mit **220 synthetischen Items** (Moduldocstring: „Nie gegen den echten `DATA_ROOT`"). Plan §3.3 und diese Zeile haben die Provenienz falsch erinnert; die Zahl liegt **8,3×** unter dem Live-Wert. **Stattdessen beide Wege mit demselben Instrument verglichen — das ist die Frage hinter V151:** der VPS-Anteil ist **76–113 ms auf ~3,1 s = 2,4–3,6 %** ⇒ *nicht relevant*. **Aufschlüsselung des Live-Werts, in-process in der echten Form gemessen** (4 sichtbare Spaces, 220 Items, die 6 Durchgänge pro Space, die `_overview()` wirklich macht): **2.388–2.407 ms** in `/tmp` gegen **2.417–2.426 ms** auf der VM-Platte ⇒ **die Platte ist es nicht** (+1 %), der Rest ist der Client-Weg. **Der Ausreißer 6051 ms ist benannt, nicht wegge Mittelwert:** das Journal loggt jeden Request mit Zeitstempel, und im ganzen Fenster liegt der Start-zu-Start-Takt bei **3,01–3,16 s** — auf dem Server gibt es keinen 6-Sekunden-Takt. Ein **Dauerfeld hat der Log nicht**, die Aufteilung aus dem Browser (TTFB) wurde nicht erfasst, die Ursache bleibt **offen** (Verdacht: der Browser hat den Fetch verschoben). **Was V151s Antwort trägt, ist deshalb die Paarung, nicht der Ausreißer.** |

## Step B — `tailscaled-watchdog.service` (P9-16 … P9-20)

| # | Kriterium | Stand | Beleg |
|---|---|---|---|
| **P9-16** | Unit + Timer existieren, `systemctl list-timers` zeigt den Timer | ✅ | Timer `enabled` **und** `active`, `NEXT` gesetzt. Der eigentliche Beleg ist `healthy: Self.Online=true` + `Finished` im Journal — **ein laufender Timer beweist nicht, dass ein Dienst arbeitet** (der erste B2-Lauf lieferte `203/EXEC`) |
| **P9-17** | Tests grün (Plan sagt 5) | ✅ **12/12** | `test_tailscaled_watchdog.py`, 5 alt + 7 aus den Wächter-Runden. Die Plan-Zahl 5 war die Zeile, nicht die Summe — wie bei P9-39 und P9-52 |
| **P9-18** | Härtungs-Direktiven per statischem Wächter belegt | ✅ | `test_unit_file_has_the_three_hardening_directives` |
| **P9-19** | Absichtlich herbeigeführter Offline-Zustand ⇒ **genau ein** Restart, im Journal belegt | ✅ | ein Restart 9 s nach dem Stopp (18:05:40, Stufe 1→2→3, polkit-Pfad), danach **zehn Takte `rate-limited` ohne einen Restart** (256 s → 829 s, Fenster 900 s), `tailscaled` ~10 min unten. **Die Zeile hat ihren Zweck erfüllt:** `RuntimeDirectoryPreserve=no` löschte die State-Datei je Takt, das Limit war nie in Kraft — und der Test dafür war grün, weil sein Mock einen Zustandsspeicher simuliert, den es live nicht gibt |
| **P9-20** | V152 beantwortet — „gibt es nicht" ist zulässig | ✅ | „Gibt es nicht": kein Tailscale-eigenes Watchdog-Feature ohne kommerzielles Add-on |

## Step C — Vision-Dienst auf der RTX 3060 (P9-21 … P9-26)

| # | Kriterium | Stand | Beleg |
|---|---|---|---|
| **P9-21** | Der Dienst antwortet von der sharefyx-VM aus auf der internen Adresse | ✅ | Block (3) Runde 4b: 63 tok/s, `size_vram = size` |
| **P9-22** | Von außen nicht erreichbar — kein Funnel, kein Port (Hard Rule 6) | ⚠️ **deferred, architektonischer Beweis** | 192.168.68.140 ist RFC1918, die VM hat keine öffentliche IP (CGNAT), der Funnel mappt nur `127.0.0.1:8765`, kein Port-Forward am RUT X50, der einzige 11434-Listener sitzt in CT 111. **Nikinger-Entscheidung 2026-09-26:** extern nicht testbar |
| **P9-23** | Cold-Start gemessen und gegen 46–180 s gestellt | ✅ | **19,9 s** (Runde 4b) und **19,7 s** (Runde 5) |
| **P9-24** | Beide Skript-Fixes aus §5.3 im Code, Startzeile zeigt den echten Endpoint | ✅ | `serve()` loggt den aufgelösten Endpoint; `--endpoint` wirkt auch ohne `--check`; zentrale `resolve_endpoint(args)` mit Präzedenz `--endpoint` > `$LOCAL_VISION_ENDPOINT` > `DEFAULT_ENDPOINT`. 9 Tests + Gegenprobe: ohne den Fix **7/9 rot** |
| **P9-25** | V154 und V156 beantwortet | ✅ | **V154:** LXC — der Plan-§5.2-Umschaltpunkt greift nicht, LXC teilt den Host-Kernel und braucht kein IOMMU. **V156:** bei `qwen3-vl:8b` geblieben, damit der Gewinn zuzuordnen ist |
| **P9-26** | Echter Sichtprüfungslauf liefert dieselbe Aussage wie der CPU-Lauf vom 2026-09-10 | ✅ | beide Läufe gegen `c4_p8519_01_radiogruppe_im_dialog.png` mit **derselben Aussage**, 19,9 s statt 46 s Wand |

## Step D — Die zwei gemeldeten Bugs (P9-27 … P9-32)

| # | Kriterium | Stand | Beleg |
|---|---|---|---|
| **P9-27** | ESC im Vollbild verlässt den Vollbildmodus und schließt **nichts** — am echten Gerät belegt | ⚠️ **erfüllt in anderer Form, seit 2026-10-05 belegt (V188): es ist Betriebssystem-Verhalten, und die Seite kann es nicht verhindern** | **Nikinger-Entscheidung 2026-09-23 (zurückstellen) und 2026-10-05 (kein Code, D1 damit geschlossen)**. Die Zeile ist nicht erfüllt *worden*, sie ist **gegenstandslos geworden**: „am echten Gerät belegt" bleibt für das native macOS-Vollbild offen (P9-28 belegt nur die Web-API-Seite des Guards), aber die **Frage, die dahinter stand — kann die Seite etwas tun? — ist beantwortet: nein.** Vier Belege, jeder mit Ort: **(1) Der Anwendungsfall ist gar nicht die Web-API.** `grep -rn fullscreen phase5_ui/webui/static/js/app.js` liefert **eine** Zeile: `app.js:259`, `if (document.fullscreenElement) return;`. Die App ruft `requestFullscreen()` nirgends auf ⇒ der gemeldete Fall (grüner Knopf / Ctrl+Cmd+F) ist natives macOS-Vollbild, und dafür gibt es keine Web-API: `document.fullscreenElement` bleibt `null`, kein `fullscreenchange`. **Der Guard ist für genau diesen Fall ein No-op** — das stand hier bisher als Vermutung („mit hoher Sicherheit"), es ist jetzt gemessen. **(2) Der Ausgang ist absichtlich nicht in der Hand der Seite.** WHATWG *Fullscreen API* §4 UI: *„The user agent may end any fullscreen session without a close request or call to `exitFullscreen()` whenever the user agent deems it necessary."* §8 Security and Privacy: *„User agents should provide a means of exiting fullscreen that always works and advertise this to the user. This is to prevent a site from spoofing the end user by recreating the user agent or even operating system environment when fullscreen."* Der Ausgang ist die Anti-Spoofing-Garantie — **eine Seite, die ihn unterdrückt, ist per Spezifikation die Fälschung, nicht die Rettung.** **(3) Der einzige Hebel, den die Seite hätte, verschiebt nur — und er darf nie abschalten.** WICG *Keyboard Lock* §7 Security: *„the user agent MUST provide a way for the user to exit from keyboard lock **even if all of the keys are requested by the API**"* (+ langes ESC > 2 s). §3.2: *„If the key is held for 2 seconds, then exit from the keyboard handler and pass the key on to the user agent for normal processing (which will exit fullscreen (and pointer lock, if active))."* WHATWG Fullscreen §6: *„User agents should reserve an additional input for the purposes of exiting fullscreen"*, und wörtlich zum Muster: *„user agents that use the Esc key to exit fullscreen use keyboard lock to prevent immediate exit on key press, and instead require a long press to exit fullscreen."* MDN `Element.requestFullscreen()`: *„Browsers are expected to provide an alternative mechanism for exiting fullscreen mode when keyboard lock is enabled. Most browsers use the Esc key to exit normal fullscreen mode, and a long-press Esc key to exit keyboard lock."* **(4) Und dieser Hebel ist für den macOS-Fall doppelt unbrauchbar** — genau die Aussage, die im Plan §4 **aus dem Gedächtnis** stand: **(a)** Keyboard Lock gilt nur für **JS-initiiertes** Vollbild, WICG §4.2 wörtlich: *„the Keyboard Lock API is only valid when a JavaScript-initiated fullscreen is active. During F11 fullscreen, no Keyboard Lock processing of keyboard events will take place."* **(b) Browser-Support, heute gemessen** an MDNs `browser-compat-data` (`api/Navigator.json`, `api/Keyboard.json`, Branch `main`): `navigator.keyboard`, `Keyboard.lock`, `Keyboard.unlock` → Chrome ab 68, Edge/Opera/Chromium `mirror`, **`firefox: false`**, **`safari: false`** (damit auch `safari_ios`/`webview_ios` über `mirror`). **Auf dem Gerät, um das es geht, existiert die API nicht.** *Was das für P9-28 heißt:* dessen ✅ bleibt gültig — der Guard ist im Web-Vollbild genau richtig und am Browser beider Richtungen belegt; P9-27 und P9-28 sind zwei verschiedene Fragen. **Kein Fehlschlag als Erfolg verbucht** — und **kein Code gebaut** (Plan §4, Nikinger-Entscheidung 2026-10-05) |
| **P9-28** | ESC außerhalb des Vollbilds verhält sich unverändert wie vor P9 | ✅ **am 2026-10-03 im Browser belegt** (`p9_step_d_probe.json`, Stationen 8+9) | Beide Richtungen, und das gesetzte `fullscreenElement` ist im selben Lauf **gemessen**, nicht behauptet: ohne → ESC schließt das Item (`offen=True` → `zu=True`), mit → es schließt **nichts**. War bis heute „strukturell erfüllt, nicht am Gerät belegt". **Gegenprobe G2** (Guard raus) → genau Station 9 rot. *Grenze:* der Browser verlässt im Automationslauf bei ESC **nicht** den Vollbildmodus — synthetische Tastendrücke lösen seinen Exit nicht aus; geprüft ist die App-Seite des Guards |
| **P9-29** | Ein Item lässt sich aus einem Ordner auf die Space-Zeile zurückziehen | ✅ **am 2026-10-03 im Browser belegt** (`p9_step_d_probe.json`, 12 Stationen) | Drei Teile, weil ein Zug drei Fehler haben kann: **(a)** die Ereigniskette kam vom Browser — `dragstart=1`, `dragover=19`, `drop=1`, Item-ID im `dataTransfer` (ohne diese Station bewiesen die anderen nur den Listener); **(b)** der Serverzustand: `GET …/{id}` → `folder: ""`; **(c)** die Liste: 3 → 2 Zeilen, Toast „Verschoben nach (Space-Wurzel)". Ohne Restschaden belegt: die Gegenrichtung (Wurzel → Ordner, 1 PATCH) und der Leerlauf-Riegel `tree.js:139` (Drop kommt an, `drop=1`, aber **0** PATCH — an der Request-Zahl gemessen). **Gegenprobe G1** (Space-Bindung raus) → 5 Stationen rot, **6–9 grün** |
| **P9-30** | Der Drop-Zustand ist sichtbar | ✅ **am 2026-10-03 im Browser belegt** (`p9_step_d_probe.json`, Stationen 3+4) | Nicht „die Klasse ist gesetzt", sondern **wie sie aussieht**: berechneter Stil am Ziel im Zug — `dashed`, `rgb(62,141,243)` = `--accent`, auf der Space-Zeile, die sonst keine gestrichelte Kante hat. Bilder `p9_step_d_04_dragover_space_zeile.png` (im Zug) gegen `…_05_nach_dem_zug.png` (Toast, Zähler 3 → 2, ohne Kante). Station 4 prüft das **Wieder-Verschwinden** und bleibt in G1 grün, weil ihre Aussage eine *Abwesenheit* ist — kein Loch, sondern die Aussage |
| **P9-31** | Ein Zug auf einen Zähler-Chip löst **kein** Verschieben aus (V136) | ⚠️ **gegenstandslos am gewählten Anker** | Die Plan-Warnung zielt auf `.overview__space-open` (`list.js`); der Anker ist die `.tree__space`-Zeile (`tree.js`), und die hat **keine** verschachtelten interaktiven Kinder. Ein Guard, der nichts ausschließt, wäre ein irreführender Test — der dritte Test prüft deshalb den `space.own`-Riegel |
| **P9-32** | 3 neue Tests grün, `ui_budget` 5/5 | ✅ | die drei Wächter unter P9-27/28/29. `ui_budget` damals 145,0 KB, **heute nachgemessen 5/5 bei 155,2 KB** |

## Step E — Karte: Reload-Overload und V118 (P9-33 … P9-37)

| # | Kriterium | Stand | Beleg |
|---|---|---|---|
| **P9-33** | Zweiter Eintritt ohne Datenänderung erzeugt **keinen** zweiten `/graph`-Abruf | ✅ | Signatur aus dem `/overview`-Payload — **Plan-Korrektur:** der Graph-Knoten hat kein `updated`. Node-Harness und Browser-Probe (Port 18768): **0** Abrufe, auf `HEAD` **1** |
| **P9-34** | Die Karte springt beim Wiedereintritt nicht — im Screenshot-Paar belegt | ✅ | **1 von 10** verschiedenen Bildern in 1,5 s (auf `HEAD` 10 von 10, 467,6 px Sprung). Der Plan-Test hätte das **durchgelassen** — deshalb trägt die Zeile den Bildvergleich |
| **P9-35** | Datenänderung führt weiterhin zum Neuladen | ✅ | Refresh-Knopf erzwingt 1 · fremde Änderung wird aufgenommen (Knoten 14 → 15) 1 |
| **P9-36** | V118 beantwortet, **mit Nikinger-Entscheidung, falls es zwei Linien sind** | ⚠️ **beantwortet, die Entscheidung steht aus** | im Harness an einem echten Frame gemessen: `segments_in_last_frame: 2`, `duplicate_segments: 1`, gestrichelte Linie gezeichnet — `dedupeEdges()` und `buildTagEdges()` deduplizieren getrennt, erst `drawEdges()` führt zusammen. **Ob zwei Linien gewollt sind, ist deine Design-Frage**; ein Umstieg wäre samt Umkehr des Tests eine bewusste Änderung |
| **P9-37** | Tabu-Diff leer, `ui_budget` 5/5 | ✅ | Tabu-Bereichs-Diff `2f752f9^..HEAD` leer (Zusatzprobe `phase1_storage` ebenfalls leer, `space_cli.py` wurde nur **ausgeführt**, nicht angefasst); `ui_budget` 5/5, 149,0 KB |

## Step F — Schema-Fundament (P9-38 … P9-44)

| # | Kriterium | Stand | Beleg |
|---|---|---|---|
| **P9-38** | Die enge Probe zeigt genau drei Dateien | ✅ | `66117ff^..66117ff -- phase1_storage/storage` → `index.py`, `models.py`, `store.py`. **Plan-Korrektur:** §8.2 sagte neun Stellen, der Diff hat **18 Hunks** in genau diesen drei |
| **P9-39** | 9 Tests grün | ✅ **23** | Fünf der Plan-Tests waren Verhaltenstests, der Rest Wächter; `pytest` 1039 → 1062. Gegenprobe mit vier eingebauten Verstößen → **10 Tests rot** |
| **P9-40** | `_status_hint()` nennt `doing`, ohne dass `tools.py` es enthält | ✅ | Trennung Maschinen-/Navigations-Ebene, siehe auch P9-65 |
| **P9-41** | `note` akzeptiert `doing` nicht | ✅ | `STATUS_VALUES["note"]` bleibt `{active, archived}` |
| **P9-42** | Ein Altbestands-Item bekommt beim Write kein leeres `assignee` | ✅ | `_coerce_assignee()` behandelt fehlend ≠ leer |
| **P9-43** | Index-Neuaufbau über den echten `DATA_ROOT` gelaufen, Zeit notiert (V161) | ✅ | Deploy `v3.1.0`: Journal `wird verworfen` 11:40:30,240 → `Started server process` 11:40:31,287 = **≤ 1,05 s** für **197 Items** (V161 sagte 0,4–0,6 s für 153). Index danach `user_version 4`, 197 Zeilen |
| **P9-44** | V160 beantwortet und im Plan als Lock nachgetragen | ✅ | **Space-Name, ohne Validierung** (Lock **P9-U**) — eine Prüfung gegen die Space-Liste wäre eine zweite, nicht angekündigte Öffnung |

## Step G — Löschen (F2) nach `_trash/` (P9-45 … P9-52)

| # | Kriterium | Stand | Beleg |
|---|---|---|---|
| **P9-45** | Ein eigenes Item lässt sich nach zweifacher Rückfrage löschen | ✅ | Browser **14/14** gegen eine eigene TLS-Wegwerf-Instanz, zwei unabhängige Läufe; 6 Screenshots `docs/screenshots/p9_step_g_*`, Probe `probes/p9_step_g_probe.json` |
| **P9-46** | Ohne exakten Titel bleibt der Knopf gesperrt | ✅ | **serverseitig** geprüft (Muster `api.py:567`), nicht nur ein gesperrter Knopf |
| **P9-47** | Die Datei liegt unter `_trash/`, byte-identisch | ✅ | `DATA_ROOT/._trash/<space>/` — der Plan-Ort `<space>/_trash/` war **unbaubar** (Item nach `rebuild_index()` wieder da, `_trash` als Phantom-Space). Byte-Gleichheit gemessen |
| **P9-48** | Git-Commit im Datenverzeichnis vorhanden | ✅ | Commit-Existenz **und** Datei im Commit per `git log`/`git ls-files` geprüft, nicht per Spy auf `_commit()` |
| **P9-49** | Das Item erscheint in **keiner** Liste, Suche, Karte oder Übersicht | ✅ | inkl. **nach** `rebuild_index()` und **inkl. Karte** — der Plan-Test hätte den Defekt der Plan-Variante durchgelassen. Eingehende Kanten bleiben dangling, `_graph_get` filtert sie |
| **P9-50** | Kein MCP-Werkzeug kann löschen | ✅ | statisch: kein `@mcp.tool` mit Lösch-Namen, `tools.py` referenziert `trash()` nicht; plus Test gegen jeden Endpunkt, der `_trash/` listen könnte |
| **P9-51** | Ein fremdes Item lässt sich nicht löschen | ✅ | Rechte-Grenze gemessen, dazu Kartengeometrie und Nachbarn unberührt |
| **P9-52** | 7 Tests grün | ✅ **13 + 5** | die sieben der Plan-Liste plus sechs für die gemessenen Lücken (`test_step_g_trash.py`), fünf Endpunkt-Tests in `test_api.py`. Gegenprobe mit vier Verstößen → **11 rot**; `pytest` 1062 → 1078 |

## Step H — Abhängigkeits-Hygiene (P9-53 … P9-55)

| # | Kriterium | Stand | Beleg |
|---|---|---|---|
| **P9-53** | `fastmcp` 3.4.7 installiert | ✅ | durch die **Messung** erfüllt, nicht durch eine Änderung: der Live-Release lief bereits auf **3.4.7**, weil `deploy.sh:153` pro Release ein frisches venv baut und der Pin ein **Range** war — genau der stumme Drift, den P3-D verbietet |
| **P9-54** | V163 beantwortet | ✅ | Gegen den Code statt gegen das Aufrufbild: **nein** — CIMD abgeschaltet (`metadata.py:19`, P4-E/V14), `token_endpoint_auth_methods_supported: ["none"]` ⇒ gar keine Client-Assertions (`metadata.py:32`), und die benutzte Fläche enthält weder `OAuthProxy` noch `JWTVerifier`; Auth trägt der eigene `BearerAuthASGI`. Bump = Hygiene, kein Brand |
| **P9-55** | Der Pin bleibt `<3.5` | ⚠️ **in der Form abweichend** | gebaut ist `fastmcp==3.4.7` — innerhalb P9-R, aber ohne die Range-Form, weil die Range-Form der Mechanismus des gemessenen Drifts ist. **Nikinger-Entscheidung 2026-09-30**, im Plan §10 als Abweichung dokumentiert. Riegel: `test_the_installed_fastmcp_matches_the_pin`, läuft im **Release-venv** mit (`deploy.sh:169`) |

## Phasenweit (P9-56 … P9-58) — heute gemessen

| # | Kriterium | Stand | Beleg |
|---|---|---|---|
| **P9-56** | Bereichs-Tabu-Diff `<start>^..HEAD` über §0.3 leer — mit **genau einer** Ausnahme (Step F) | ⚠️ **ein Treffer, der nicht auf der Ausnahmenliste steht** | `git diff --stat 06ab4f6^..HEAD` über die sechs Pfade → **ein** Treffer: `phase7_spaces_admin/tests/test_space_removal.py`, 17 Zeilen (+15/−2). Grund: die Test-Attrappe für `Store.move()` hatte eine eigene Signatur, das neue `actor=` machte daraus einen HTTP 500 mitten im Space-Entfernen (trace-Plan §9: „ein Fund drei Phasen entfernt"). **Nicht umbenannt:** §0.3 sagt für `phase7_spaces_admin/` „Code; Doku-Zeilen erlaubt" — eine Testdatei ist beides nicht. **Die beiden angekündigten Öffnungen sind unberührt** und je gemessen: Step F genau drei Dateien, trace genau drei |
| **P9-57** | Service-Touch durch einen Agenten **0**: kein `pkill -f`, kein `systemctl`; Wegwerf-Instanz über PID-Datei oder Port gestoppt | ✅ | **messbare Hälfte heute:** kein Listener auf den P9-Wegwerf-Ports 18765–18780 (`ss -ltn`), die Produktionsinstanz läuft unverändert als PID 1994214 (nur gelesen). **Nicht prüfbar** ist die Behauptung „kein `systemctl` durch einen Agenten" — sie steht je Session-Block und ist kein maschinell prüfbarer Zustand |
| **P9-58** | `pytest` ≥ 995 + die neuen Tests, `ui_budget` 5/5, jeder Step-Commit mit Doc-Update im selben Commit | ✅ | **heute:** `pytest` **1169 passed** (218,31 s), `ui_budget` **5/5** (155,2 KB gzip von 250 KB), `doc_health` **0**. Doc-Update je Commit **über alle 72 Commits seit `06ab4f6` geprüft**: kein einziger ohne `.md`, und — die schärfere Form — **kein Commit mit Produktcode ohne `phase9_hardening/CLAUDE.md` im selben Commit** (die 11 Commits ohne Head sind reine Runbook-Commits). Hard Rule 8 ist damit nicht behauptet, sondern durchgezählt |

## Block doing — fünfter Eimer „In Arbeit" (P9-59 … P9-68)

| # | Kriterium | Stand | Beleg |
|---|---|---|---|
| **P9-59** | Eine `doing`-Aufgabe zählt in „In Arbeit" und in **keinem** anderen Eimer | ✅ | T3 `test_doing_task_counts_in_doing_and_nowhere_else` als **Mitgliedschafts-Beweis** (fünf Eimermengen, disjunkt und vollständig) — als Zahlengleichheit hätte es den Duplikat-Fall durchgelassen. Browser S3/S6 |
| **P9-60** | Zähler == Liste für „In Arbeit", mit nichtleerem Bestand | ✅ | T4 prüft `total == counts["doing"] == 1` **und** `items[0].title == "laufende Aufgabe"`; T8 (Altbestand) ist für diesen Eimer nicht mehr vakuös |
| **P9-61** | Jede `(type, status)`-Kombination aus `STATUS_VALUES` landet in genau einem Eimer | ✅ | T2, **generiert** aus `STATUS_VALUES` statt handgeschrieben; G1 → 7 rot, G3 → 2 rot |
| **P9-62** | Reihenfolge `open, doing, done, note, archived` | ✅ | T1 liest die Reihenfolge aus dem **Quelltext**; Browser S2 prüft die `data-bucket`-Folge im DOM |
| **P9-63** | Rail und Chips zeigen „In Arbeit", nirgends roh `doing` | ✅ | T6 vergleicht Label-**Menge** gegen Eimer-**Menge** (der `BUCKET_LABELS[b] \|\| b`-Rückfall ist sonst kein Fehler, er sieht nur aus wie ein Feature) |
| **P9-64** | Statuswechsel `open` → `doing` lässt die Rail-Zähler **ohne Reload** umspringen | ✅ | Browser S5/S6: Toast „Gespeichert · v2", danach `offen 1 → 0`, `in Arbeit 1 → 2`; Screenshot `p9_doing_04_*`; Browser-Gegenlauf **rot** |
| **P9-65** | Maschinenebene roh und vollständig; UI-Speichern verliert `assignee` nicht | ✅ | T5 schickt **exakt** `editor.js :: saveItem()`s Feldsatz (ohne `assignee`), danach über drei Lesepfade geprüft; Browser S8. **Der Browser-Gegenlauf ist der eigentliche Beleg für P9-W:** S5/S7/S8 bleiben auch ohne den Block grün — das Loch war rein navigativ |
| **P9-66** | Kein `storage/`-, MCP- oder Tabu-Touch, keine zehnte Contract-Öffnung | ✅ | Tabu-Diff leer, im Commit ausgegeben. Damit V174 beantwortet: §Geerbte Contracts musste **nicht** mitgezogen werden |
| **P9-67** | Jeder neue bzw. umgedrehte Wächter wird an einem eingebauten Verstoß rot | ✅ | G0 (Kontrolle) **0** · G1 **7** · G2 **2** · G3 **2** · G4 **1** · G5 **1**; Browser-Gegenlauf 7 von 11 rot |
| **P9-68** | `v3.1.0` live, `health_gate` grün, P9-43 gemessen | ✅ | Release `5414cb7`, Health-Gate **9/9**, P9-43 ≤ 1,05 s (siehe dort) |

## Block trace — Nachvollziehbarkeit (P9-69 … P9-82)

| # | Kriterium | Stand | Beleg |
|---|---|---|---|
| **P9-69** | Enge Probe = drei Dateien | ✅ | `git diff --stat 43fcac0^..43fcac0 -- phase1_storage/storage` → `history.py`, `models.py`, `store.py` — genau die drei in §0.4 angekündigten |
| **P9-70** | T1–T6 grün | ✅ | 5 `test_store.py` + 4 `test_history.py`; `pytest` 1128 → 1152 (**24** neue, im frischen venv gezählt) |
| **P9-71** | Wächter T7 grün und mit G1 rot | ✅ | `test_every_store_write_call_in_the_adapters_carries_an_actor`; G1 → 1 rot. Er scannt nur **Nicht-Test**-Module — die Attrappen-Klasse fängt er per Konstruktion nicht ab (P9-56) |
| **P9-72** | MCP liefert `updated_by` in `get_item`, `search_items` und Schreibantworten | ⚠️ **eine Datei mehr als §0.3 vorsah** | `mcpserver/receipts.py` — die Standardantwort eines Schreib-Tools ist die *Quittung*, nicht der Dateitext. Ohne diese eine Zeile hätte ein Agent nach einem fremden Write nicht die Antwort bekommen, in der er nachschaut |
| **P9-73** | `_ASSIGNEE_HINT` an beiden Tools wörtlich | ✅ | prüft zusätzlich die Nicht-Überschreiben-Hälfte |
| **P9-74** | Kein Kanal kann `updated_by` setzen | ⚠️ **eine Route verwirft statt abzulehnen** | Kern `ValidationError` · PATCH `422` · kein MCP-Parameter · **POST filtert lautlos auf eine Whitelist**. **Bewusst nicht vereinheitlicht:** eine `unknown`-Prüfung im POST würde jedes unbekannte Feld ablehnen und damit Round-Trips brechen, die den vollen Item-JSON zurückschicken. Beide Stellen im Code kommentiert |
| **P9-75** | Altbestand bleibt ohne Feld | ✅ | Test + Browser S7: die Lesezeile ist **weg**, nicht „unbekannt" |
| **P9-76** | Git-Autor = Schreiber, Committer unverändert | ✅ | Test + **live im Wegwerf-DATA_ROOT**: `git log --format=%an -3` → `beta, alpha, alpha` |
| **P9-77** | UI: „bei X" in der Liste | ✅ | Browser S2 (`task · doing · bei alpha`) + statischer Wächter |
| **P9-78** | UI: Editorfeld + „Zuletzt geändert von X" | ✅ | Browser S1/S3/S4 + Wächter für Feld **„Bei"** mit `<datalist>` und die Lesezeile |
| **P9-79** | P9-Z: Auto-Füllen nur bei leer, nie überschreiben | ✅ | Browser S1 (`'' → alpha`), S5 (`alpha → alpha`); Gegenlauf **S5 rot** (`alpha → beta`) — der eigentliche Beweis |
| **P9-80** | Browser S1–S7 grün, Gegenlauf rot | ✅ `pending: Deploy v3.1.1` | `probes/p9_trace_probe.json` **8/8** gegen eine Zwei-Principalen-TLS-Instanz mit echter Git-Historie; mit G4 **7/8** (S5 rot, `alpha → beta`) |
| **P9-81** | Gegenlauf G1–G5 jeder ≥ 1 rot | ✅ | G1 → **1** · G2 → **2** · G3 → **1** · G4 → **2** · G5 → **4** |
| **P9-82** | Frisches venv grün | ✅ `pending: Deploy v3.1.1` | `pytest` **1128/1128** im frischen Release-venv, mit dem `requests`-Defekt behoben (dessen Beleg ist der Lehrfall „eine unbenannte Handinstallation") |

## Block settings — Einstellungen als Fensterkette (P9-83 … P9-95)

| # | Kriterium | Stand | Beleg |
|---|---|---|---|
| **P9-83** | Menütitel „Einstellungen", kein Hinweistext | ✅ | `test_settings_chain.py::test_the_settings_menu_carries_exactly_three_buttons_in_the_locked_order` (prüft **Anzahl und Reihenfolge**, nicht das Vorhandensein der drei — ein vierter Knopf wäre sonst still durchgegangen) + Browser S1 |
| **P9-84** | Drei Knöpfe in der Reihenfolge aus P9-AE, Standardhöhe, nicht volle Breite | ✅ | Browser **S1, gemessen**: alle drei `h=35.69 px, padding 6px/32px, radius 6px` — **identisch** mit einer echten, inaktiven `.tree__folder`-Zeile in der Rail desselben Fensters (Toleranz ±1 px). Kein eigener Wert notiert, die Knöpfe tragen die Klasse selbst (P9-AF) |
| **P9-85** | Unterfenster öffnet **neben** dem Menü, Menü bleibt sichtbar, aktiver Knopf markiert | ✅ | Browser **S2**: `['settings-menu', 'settings-password']`, `x(Passwort) > x(Menü)`, `aria-current="true"` genau am aktiven, `"false"` an den anderen; `backgroundImage` = derselbe `linear-gradient` wie die aktive Baumzeile. Gegenlauf **G1 → 4 Stationen rot** |
| **P9-86** | Knopfwechsel ersetzt Stufe 2 | ✅ | Browser **S3**: Passwort → Update-Log, kein Passwort-Panel mehr, der neue Knopf markiert, 7 171 Zeichen Log-Inhalt |
| **P9-87** | Space-Klick öffnet Stufe 3, drei Panels bei 1440 px | ✅ | Browser **S4**: `['settings-menu', 'settings-spaces', 'settings-space-detail']` **in dieser x-Reihenfolge** (gemessen, nicht aus dem DOM abgeleitet — das Menü steht im Markup zuerst) |
| **P9-88** | ESC und „Schließen" schließen von rechts nach links | ✅ | Browser **S5**, drei ESC hintereinander: `3 Panels → 2 → 1 → 0`, danach `#settings-overlay[hidden]`. Gegenlauf **G2 → 2 Stationen rot** (ESC schloss alles) |
| **P9-89** | ≤ 1024 px nur das rechteste Panel plus „Zurück" | ✅ **nach einem echten Befund** | Browser **S8**. Die erste CSS-Fassung blendete nur das Menü aus und ließ bei offenem Detail **zwei** Panels stehen — genau das, was P9-AI verbietet. Zwei `:has()`-Regeln statt einer: Detail offen ⇒ Stufe 2 tritt zurück; irgendetwas rechts vom Menü offen ⇒ Menü tritt zurück |
| **P9-90** | Passwort: alt → neu → wiederholen → TOTP, Wechsel live gegen Wegwerf grün | ✅ | Browser **S6**: HTTP **200**, Panel geschlossen, Menü bleibt, Toast, `/api/v1/me` danach 200 (Sitzung besteht). Reihenfolge im Bild **angesehen** und im Wächter festgehalten |
| **P9-91** | Space-Zeilen mit Abstand, Trennlinie vor der Anlege-Zeile, Update-Log-Inhalt unverändert | ✅ | Browser **S4** (`row-gap` 8 px, `<hr>` über dem Eingabefeld) und **S7** am echten Paar (**8 px**). Update-Log: dieselbe Liste, 7 171 Zeichen, derselbe Parser `parse_update_log()` |
| **P9-92** | Keine Knöpfe mit leerem Überraum, Alte-Adresse-Dialog unverändert | ✅ **Bilder angesehen — 6 von 7, und die siebte mit einer Fehlaussage des Modells** | Angesehen: `01` (Menü, kein Hinweistext, keine Leerfläche), `02` (zwei Fenster nebeneinander, TOTP **zuletzt**, aktiver Knopf blau), `03` (Update-Log breiter, Text füllt die Breite), `04` (drei Panels in Stufenfolge, Trennlinie über dem Anlege-Feld, 8 px Zeilenabstand), `05` (bei 1024 **ein** Panel mit „Zurück"), `07` (drei Panels, Titel korrekt). **`06` (Passwort gewechselt) konnte das lokale Vision-Modell nicht beantworten** — erster Versuch in der Token-Grenze (`done_reason: length`), zweiter Versuch **falsch**: es meldete, der Menüpunkt „alpha" sei blau markiert. „alpha" ist **kein Menüpunkt**, sondern die Zeile in der Rail; nach dem Wechsel trägt **kein** Menüpunkt `aria-current` (gemessen: `sichtbare_panels == ['settings-menu']`). Der Zustand ist also belegt, die Sichtprüfung dieses einen Bildes nicht — und genau das ist der Grund, warum die Probe den Zustand misst und das Bild nur ergänzt. Das Menü misst **202 px** bei `min-width: 0` (kein Formularmaßband). `#legacy-host-dialog` byte-gleich, nur sein Kommentar trägt den neuen Hinweis. **[2026-10-05, nach der Bildsichtung des Nikingers: sieben UI-Punkte, nicht gebaut]** — Mini-Plan **§10**, Locks P9-AM–P9-AS, Abnahme P9-96–P9-102: Fläche der unausgewählten Menüpunkte, Titel zentrieren, Beschriftung zentrieren, „Zurück" mit echtem Icon, mehr Abstand über dem Space-Titel, **alle Knöpfe der Einstellungs-Fenster rechts ausrichten** (behebt den gemeldeten Überlauf mit den „(schreiben)"-Zeilen), Passwort- und Update-Log-Panel **unverändert lassen**. **P9-92 bleibt ✅** — sein Kriterium ist „kein Überraum, Alte-Adresse-Dialog unverändert", und kein Punkt der Rückmeldung trifft es: die Rückmeldung sind **neue** Kriterien mit neuen Nummern, keine Umkehr einer abgenommenen Zeile |
| **P9-93** | V118: eine Linie, Gradzählung ohne implizite Doppelkante, Test umgedreht | ✅ | `test_a_tag_edge_beside_an_explicit_edge_draw_one_line`: 1 Segment, 0 Duplikate, **keine** gestrichelte Linie, durchgezogene vorhanden. Gefiltert bei der **Übernahme** (`rebuildImplicitEdges()`), nicht in `drawEdges()` — sonst zählte `recomputeDegrees()` die Zwillingskante weiter und `drawNodes()` skaliert danach den Radius. Gegenlauf **G3 → rot** |
| **P9-94** | P9-11 vier Läufe eingetragen | ✅ **2026-10-07** | Alle vier Läufe plus der Kontrolllauf stehen mit Netz, Ergebnis und Grenze in der **P9-11**-Zeile, die Rohausgabe verbatim in `probes/p9_11_portscan_2026-10-07.txt`. **Lauf 2** (VPS `217.160.128.146`, Hotspot, Tailscale aus): **80 und 443 `open`, 22 nicht `open`** (`filtered`) — wie erwartet; der zusätzliche `21 open` ist dasselbe Pfad-Artefakt wie in Lauf 1. Die Netzzuordnung folgt der Anleitung der Session vom 2026-10-07 (A: Hotspot ohne Tailscale → B: Hotspot mit Tailscale → C: Heim-WLAN), und die Reihenfolge der eingefügten Ausgabe folgt ihr. Der Nikinger bestätigt, nach dieser Anleitung gescannt zu haben; ausdrücklich bezeichnet war nur der Kontrolllauf |
| **P9-95** | `pytest` ≥ 1223 + neue, `ui_budget` 5/5, Gegenläufe G1–G3 rot, Tabu-Diff leer | ✅ | `pytest` **1223 → 1233** (10 neue, 1 umgedreht, 3 umgeschrieben) · `ui_budget` **5/5** (163,4 KB; `js/settings.js` 3,0 KB gzip) · `node --check` grün · Tabu-Diff §0.3 **leer** (auch `api.py`/`security.py`/`phase4_auth/` unberührt, der Block ist reines Frontend) · G1 → 4 rot · G2 → 2 rot · G3 → rot |

## Block settings, Nachtrag — die sieben Punkte aus der Bildsichtung (P9-96 … P9-102)

**Anlass:** der Nikinger hat die Bilder vom 2026-10-05 angesehen und sieben Punkte notiert
(Plan §10, Locks P9-AM–P9-AS). **Zwei der sieben sind ausdrücklich „nicht anfassen"** (P9-AT:
Passwort- und Update-Log-Panel).

| # | Kriterium | Stand | Beleg |
|---|---|---|---|
| **P9-96** | Menütitel zentriert, Abstand Titel→erster Knopf == der in P9-AR gemessene Wert (±1 px) | ✅ | Browser **S11** (Titelmitte **0 px** von der Panelmitte, mit einem `Range` über den Textknoten gemessen) und **S13** (**24 px**). Der Abstand kommt aus **einem** Wert (`--settings-title-gap`, in `.settings-chain` definiert, zweimal benutzt) — Wächter `test_the_two_titles_share_one_gap_and_only_the_menu_title_is_centered` |
| **P9-97** | Unausgewählter Menüpunkt: gleiche berechnete Fläche wie `#space-create-name-input`, **Geometrie unverändert** gegen die Baumzeile | ⚠️ **benannte Abweichung, Nikinger-Entscheidung** | **Fläche ✅ gemessen (S10):** Menüpunkt `bg=rgb(12,16,21)` / `kante=rgba(255,255,255,0.16)` — **bytegleich** zum Eingabefeld, und **nicht** die Panelfläche (`rgba(27,32,39,0.55)`). **Geometrie: die Abweichung ist der linke Polsterwert.** Als `.tree__folder` erbte der Menüpunkt `padding-left: 32px` (Einrückung der Baumzeile) und lag damit **12 px neben** der Knopfmitte; exakt mittig (P9-AP) ging nur mit symmetrischem Polster. **Nikinger 2026-10-05: beidseitig `--space`.** **S1** vergleicht Höhe, Polster oben/unten, Rundung und Schrift **unverändert** mit der Baumzeile (`h=35.69`, `6px/8px/8px`, `r=6px`, 14 px) und nennt die 32 px der Baumzeile **im Ergebnis mit** |
| **P9-98** | Ausgewählter Menüpunkt trägt weiter `--select-fill`, byte-gleich zur heutigen Regel | ✅ | Browser **S2** (aktiver Menüpunkt = derselbe `linear-gradient` wie die aktive Baumzeile) · Wächter `test_the_selection_state_uses_aria_current_and_the_existing_fill` (Regel-Bodies **gleich**) und `test_the_unselected_menu_item_takes_the_input_surface_verbatim` (P9-AO) |
| **P9-99** | `text-align` der Menüpunkte berechnet `center` | ⚠️ **anderer Weg, gleiche Wirkung — gemessen** | **Das Kriterium des Plans war ein No-op, und das zeigte erst die Messung.** Der Knopf ist `display: flex` mit **anonymem Flex-Item** (Textknoten); `text-align: center` zentriert darin einen Text in sich selbst. Die erste Fassung des Baus hatte das und maß die Textmitte **8,5 px neben** der Mitte (S11 rot). Gebaut ist `justify-content: center` — die **Flex-Achse**: Textmitte **0 px**, Titelmitte **0 px**. Der Wächter verbietet `text-align` in einer eigenen Menüpunkt-Regel **ausdrücklich** |
| **P9-100** | Back-Knopf enthält `<use href="#i-chevron-left">` und **keinen** `←`-Text, Icon zentriert, `aria-label` gesetzt | ✅ | Browser **S12**, fünf Stationen: sichtbar · Icon **aufgelöst** (21,25 × 21,25 px — ein `<use>` auf ein fehlendes Symbol ergäbe 0 × 0) · `dx=0 dy=0` px · `innerText=''` · `aria-label='Zurück'` **und** `title='Zurück'`. Neues Symbol `i-chevron-left` (`d="m15 18-6-6 6-6"`), in `KNOWN` |
| **P9-101** | Abstand Space-Titel↔erste Option == Abstand Menü-Titel↔erster Knopf | ✅ | Browser **S13**: **24 px == 24 px** (±1 px). **Operierte Fassung, weil „erste Option" zweierlei bedeuten kann:** gemessen wird der Abstand zum **ersten sichtbaren Block unter dem Titel** — im Harness `space-detail-home-hint` (steht vor der leeren Mitgliederliste). Zur ersten *Mitgliederzeile* wäre es Titel + Hinweis, eine andere Größe. Die Regel wirkt in beiden Fällen, weil 24 px größer ist als das `margin-top: 1em` der `<ul>` (16 px) |
| **P9-102** | `.overlay__actions` **in der Kette** `justify-content: flex-end`, Boxen von „Space entfernen" und der letzten „(schreiben)"-Zeile überlappen sich nicht (≤ 0 px) | ✅ **mit benannter Messgrenze** | **S14:** Rahmenkante des Knopfes **auf** der Inhaltskante des Panels, Differenz **0,0 px** (beide Panels) · **Gegenrichtung gemessen:** der modale Entfernen-Dialog (P9-AK) richtet seine Knöpfe **nicht** aus (−155 px) · **S15:** Überlappung **−121,59 px**, also 121 px Luft. **Zwei Grenzen im Beleg:** „Space entfernen" ist im **Home-Space gesperrt** (P7-K) — gemessen wurde die `.overlay__actions`-Zeile, die ihn enthält; und ein Home-Space hat **keine Mitglieder**, die Gegenzeile war deshalb **synthetisch** in der echten Markupform aus `spaces.js :: memberRow()` (290 px breit bei 332 px Innenbreite) |

## Nachtrag 2026-10-06 — zweite Bildsichtung des Nikingers (P9-103 – P9-111)

**Anlass.** Der Nikinger hat die vier Bilder aus `screenshots_latest/` angesehen und vier Punkte
notiert (Abstand der Menüpunkte, Fläche der Menüpunkte, rote „Ändern"-Taste + „Schließen",
Bündigkeit von Namensfeld und Auswahl-Knopf); zu zwei davon hat er Rückfragen beantwortet.
**Mini-Plan §11**, Locks **P9-AU–P9-AZ**, Browser-Probe **29/29** gegen die TLS-Wegwerf-Instanz
(Port 18775), **sechs Gegenläufe** G7–G12, alle sechs wirksam.

| # | Kriterium | Stand | Beleg |
|---|---|---|---|
| **P9-103** | Abstand zwischen den drei Menüpunkten == der der Space-Zeilen, **an beiden Übergängen** | ✅ | **8,0 px / 8,0 px**, und `rowGap` von `#space-admin-list` ist **8px** — **verglichen, nicht abgetippt**. Vorher gemessen: **0,0 px** („glued to each other"). Der Abstand hängt an einem **Wrapper** (`.settings-menu__list`), nicht an `margin-bottom` am letzten Knopf |
| **P9-104** | unausgewählter Menüpunkt: berechnete Fläche und Kante == der **`.btn`**-Regel, dazu derselbe Innenschatten | ✅ | **berechnet** gegen einen eingefügten Vergleichspunkt derselben Klasse: `linear-gradient(rgb(12,28,49), rgb(5,11,19))` auf beiden, Kante gleich, `box-shadow` gleich. **Vorher** `rgb(12,16,21)` = `--sunken` (die Fläche des Eingabefeldes — „they are buttons and not fields to type something in") |
| **P9-105** | ausgewählter Menüpunkt: berechneter Verlauf == der **`.btn-primary`**-Regel, Kante == `--accent-edge`, **genau ein** `aria-current="true"` | ✅ | `linear-gradient(rgb(92,160,247), rgb(44,116,214))` == `.btn-primary`, Kante `rgb(18,60,116)` ==, **1** Träger. **Die Kette der Regeln ist umgedreht:** die Menüpunkte stehen **nicht mehr** in der Sammelregel mit der Baumzeile (`--select-fill`), die Baumzeile behält ihn |
| **P9-106** | `#account-submit` trägt die Vorsicht: Farbe == die Vorsichtsfarbe, Fläche == der Standardknopf, **keine** gefüllte rote Fläche; im Panel steht **kein** „Abbrechen" mehr | ✅ | Farbe `rgb(229,72,77)` == die Vorsichtsfarbe, Fläche == die von `.btn action--caution`. **Die Zählung der Trägerklasse ist von 2 auf 3 gewachsen** (`#logout-button`, `#archive-button`, `#account-submit`) — der Wächter wurde umgeschrieben, mit beiden Lesarten im Docstring. **„Abbrechen" → „Schließen"**, und die drei anderen Fenster tragen dasselbe Wort |
| **P9-107** | Beschriftung der Space-Zeilen == linke Kante des Panel-Titels (mit `Range` gemessen) | ✅ **mit einer benannten Grenze** | **1,0 px** Versatz — das ist der 1-px-Rahmen, nicht die Einrückung; vorher **33 px** (32 px geerbtes Einzugs-Polster + Rahmen). **Die Grenze:** die `<li>`-Mitgliederliste ist im Harness **nicht darstellbar** (der einzige eigene Space ist ein Home-Space und hat keine Mitglieder) — `#space-member-list` bekommt `list-style: none; padding: 0; margin: 0` **aus dem Browser-Standard abgeleitet** (Disc + 40 px Einzug) und **gegen die Deklaration** geprüft; die Wirkung an echten Spaces ist die Sichtprüfung |
| **P9-108** | Detail-Panel: linke Kante des Namensfeldes == linke Kante des Auswahlknopfes **und** rechte Kante == rechte Kante der Aktionszeile | ✅ | **0,0 px** auf **beiden** Kanten, bei 1440 **und** bei 1024. Vorher: Feld **222 px** gegen **234 px** der Folgezeile, also **12 px zu wenig** (Rundwert des Nikingers: „+10px"). Als **Rasterfolge** gebaut (`repeat(2, max-content)` + `grid-column: 1 / -1`), **nicht** als Breite — und der Wächter verbietet `width`/`flex`/`flex-basis` an dieser Regel ausdrücklich |
| **P9-109** | Spaces-Panel: Feld und „Space anlegen" auf **einer** Zeile, Feld links == Inhaltskante, Knopf rechts == Inhaltskante, **und der Knopf behält seine Größe** | ✅ | gleiche `top` (804,5 px), links **1,0 px** / rechts **1,0 px** (je Rahmen), Knopf **142 px** in der Zeile == **142 px** an einer Kopie außerhalb der Zeile. **Vorher: 80 px Versatz** und zwei Zeilen. **Die letzte Hälfte dieser Zeile ist ein Fund des Gegenlaufs** — siehe Befund 4 |
| **P9-110** | `#space-member-list` trägt `padding-left: 0` **und** `list-style: none` | ✅ **Deklaration, nicht Wirkung** | beide Eigenschaften sind deklariert und werden gegen die Deklaration geprüft. **Warum so und nicht gemessen:** die Liste ist im Wegwerf-Harness leer (Home-Space ohne Mitglieder); eine Wirkungsmessung wäre nur durch Erfinden eines Mitglieds möglich, und das wäre ein synthetischer Beleg für einen Zustand, den es live gibt |
| **P9-111** | **P9-96/98/99/100/101/102 halten** | ✅ | Titelabstand **24 px** (Menü **und** Detail), Beschriftung mittig (Textmitte **720** == Knopfmitte **720,0**), genau **1** `aria-current`, Chevron-„Zurück" unverändert, `.overlay__actions` weiter `flex-end`, Schmal-Modus zeigt genau **ein** Panel |

## Dritte Bildsichtung 2026-10-06 — **gebaut** (P9-116 – P9-119; P9-112 **widerrufen**)

**Freigegeben vom Nikinger am 2026-10-06** (wörtlich, je Bild aus `screenshots_latest/`):
**02** *„looks fine now"* · **03** *„great"* · **05** *„looks fine now"* · **06** *„yes"*.
**04 · 07 · 08** trugen je einen neuen Punkt; die Zeilen **P9-112 – P9-115** waren dafür am
2026-10-06 als „nicht gebaut" notiert und sind am selben Tag **abgelöst** worden — **P9-112 durch
seine eigene Widerrufung**, die drei anderen, weil ihre Nummern inzwischen etwas anderes bedeuten
als das, was sie am Vormtag prüften. **Die Zuordnung steht hier vollständig, damit keine Zeile
stillschweigend verschwindet** — und ihre Nummern stehen hier **ohne** `**`, weil der Zähl-Wächter
`test_acceptance_numbers.py` jede Zeile mit `| **P9-` als Abnahmezeile zählt: eine Zuordnungstabelle
im Fettdruck hätte die Bilanz um vier Zeilen verfälscht (gemessen: 120 statt 116):

| vorherige Zeile | ihr Inhalt | wohin |
|---|---|---|
| P9-112 | Menüpunkte so breit wie ihr eigenes Label (P9-BA) | **widerrufen** — der Nikinger am 2026-10-06 auf die Rückfrage: *„nur bei Spaces verwalten … aber nur dieses"*. Die Menüpunkte behalten ihre 131 px; **P9-116** prüft jetzt das, was er stattdessen beauftragt hat |
| P9-113 | Space-Zeilen auf ihre Beschriftung zusammenziehen (P9-BC) | **P9-117** (unverändert gebaut, neu gemessen) |
| P9-114 | Bild 04: die Member-Zeile steht dort, wo das Bild sie zeigt, und das Kriterium nennt die Position | **P9-119** (zusammen mit Bild 07: beide Punkte sind derselbe Fehler — ein Kriterium, das nicht sagt, wo man suchen soll) |
| P9-115 | Bild 07: die neu angelegte Zeile ist im Bild sichtbar (aufgerollt) und bündig | **P9-119** |

| # | Kriterium | Stand | Beleg |
|---|---|---|---|
| **P9-116** | Die **Menüpunkte sind flacher**: Polster 4 px oben/unten, **gemessene Höhe 31,69 px** statt 35,69 px — und ihre **Breite bleibt 131 px** (P9-BA widerrufen) | ✅ | Probe `p9_settings_kastchen_probe.py` **48/48**, Stationen **S1/P9-116** (3): Polster `4px` bei allen dreien (vorher `6px`), Höhen **[31.69, 31.69, 31.69]** px, Breiten **[131, 131, 131]** px. Die **mittige Beschriftung** bleibt: Textmitte **720** == Knopfmitte **720,0** (S2/P9-99). Antwort des Nikingers auf die Rückfrage: **(b) zusätzlich flacher** |
| **P9-117** | Jede **Space-Zeile umklammert ihr eigenes Label**: Kästchen = Beschriftung + Polster + Rahmen, **Text unverändert** | ✅ | **S5/P9-117** (3): 37 Zeilen, breitestes Kästchen **147 px** statt 330 px für alle; rechts **maximal 9 px** Leerraum bei 8 px Polster (vorher **192–245 px**); Beschriftung **1,0 px** bündig mit dem Titel (unverändert, P9-AX). `width: auto` an der Zeile + `align-items: flex-start` an der Liste, `max-width: 100%` als Bremse gegen lange Namen |
| **P9-118** | **Nur** das Spaces-Fenster wird schmaler — Menü, Passwort, Detail und Update-Log behalten ihre Breite; die Anlegezeile bleibt eine Zeile | ✅ | **S5/P9-118** (4): **338 px** statt **380 px** (gemessen am **geklonten Schatten ohne die neue Klasse**, Differenz 42 px); `min` == `max` == 338 px; Feld **138 px** von **288 px** Inhalt = **48 %** (Schwelle 45 %), Knopf **142 px** == Eigenbreite. **Bei 1024 px ist die feste Breite zurückgenommen**, das Panel flext (**422 px**, S6) |
| **P9-119** | **Bild 04** nennt die Position der Member-Zeile, **Bild 07** zeigt die neu angelegte Zeile aufgerollt und in der **Liste** | ✅ | **S5/P9-114**: Bedienzeile **16 px** unter dem Hinweistext, Mitgliederbereich **0 px**, Knopf **y 205,48..246,28** — das Kriterium nennt jetzt **y 205..246**. **S8/P9-119** (4): Ausgangszustand **gemessen** — Zeile bei y **1704** unterhalb des Folds (836 px); nach `scrollIntoView` **vollständig** im Panel (y **765**), Anlegezeile mit im Bild, Titel **nicht** (das Kriterium sagt das) |

### Was die Rückfrage vom 2026-10-06 geändert hat (P9-BB)

*„the update-log button is still bigger, I think you need to decrease its height"* — **gemessen ist
die Höhe bei allen drei Punkten gleich (35,69 px), und im Bild war nichts ausgewählt** (0
Akzentpixel). Die Rückfrage hatte zwei Korrekturen zur Wahl; der Nikinger antwortete **(b):
zusätzlich flacher** — und **präzisierte dabei P9-BA**: *„nur bei Spaces verwalten, dort die Buttons
der einzelnen Spaces nach Links, und das Fenster rechts verkleinern, aber nur dieses."*

**Daraus sind zwei Dinge geworden, und das zweite gab es vorher nicht:**

1. **P9-BB** — die Menüpunkte tragen ein eigenes vertikales Polster (4 px statt 6 px). Das ist die
   **erste bewusste Abweichung von P9-AF**, das die Höhe an `.tree__folder` band. Sie ist im
   Wächter **nicht pauschal erlaubt**, sondern an **einen** Wert gebunden (`padding-block:
   calc(var(--space) * 0.5)`, nur am Menüpunkt, an der Space-Zeile rot).
2. **P9-BE** — das „Fenster verkleinern, aber nur dieses" war in §12 noch gar nicht als Lock
   vorhanden; es ist als **neuer Lock P9-BE** entstanden, mit der Herleitung der Zahl in `app.css`
   (Feld + Abstand + Knopf = 288 px Inhalt) und **beiden** Richtungen im Wächter: die Klasse hängt
   genau einem Panel, und im Schmal-Modus ist die feste Breite zurückgenommen.

| **P9-120** | Die **Space-Zeile hält innen den Standardabstand auf beiden Seiten** und ihre Beschriftung bleibt bündig mit dem Panel-Titel; das Kästchen ragt 8 px in das Panelpolster | ✅ | **P9-BF** (Bild 08, 2026-10-06): innen **9 px links wie rechts** (vorher **1 gegen 9**), Kästchen **−8 px** gegen die Inhaltskante bei 24 px Panelpolster, Beschriftung **1,0 px** bündig mit dem Titel. Gebaut als `padding-left: var(--space)` **plus** `margin-left: calc(var(--space) * -1)` — beide Locks (P9-AX und P9-BF) halten nur zusammen; `pytest` **1246**, Probe **50/50**, **G19** als Gegenlauf · **Sichtprüfung: *‚perfekt, passt'*** — Bild 08, 2026-10-06 |

### Sieben Befunde aus diesem Block, die keine Abnahmezeile sind

1. **`min-width`/`max-width` sind bei `box-sizing: border-box` die Breite des *Rahmens*.** Die erste
   Fassung stand auf 288 px und lieferte damit **240 px Inhalt** und ein Anlegefeld von **88 px**.
   Die Browser-Probe hat es gemeldet (S5/P9-118), der Test nicht: er verglich „schmaler als die
   Basis" und war mit 288 gegen 340 grün — **auf der falschen Seite**. Jetzt steht 338 px (288 + 2×24
   + 2×1) und der Wächter vergleicht gegen das **`max-width`** der Basis.
2. **`width: 100%` stand in der Sammelregel, nicht in der eigenen Regel.** Die erste Fassung hat die
   eigene gelöscht und war der Meinung, damit sei das Strecken weg — der Gegenlauf G15 maß **28
   Kästchen auf 238 px**, also die volle Panelbreite. Dritte Fassung derselben Fehlerklasse in
   diesem Block (*die erste Regel ist nicht die, die ich meine*).
3. **Eine Station, die den eigenen Fehler nicht bemerkte.** „Schmaler als der Schatten" war mit
   288 px **grün**. Der Wächter prüft jetzt die **Ableitung** (Feldanteil ≥ 45 % des Inhalts), und
   **G18** ist der eigene Fehler als Mutation: 288 statt 338 ⇒ rot.
4. **G17 blieb grün, weil der Ausgangszustand Zufall war.** Die neue Zeile landete — bei 29 Spaces
   und unverändertem `scrollTop` — zufällig sichtbar. Die Probe stellt den Zustand jetzt **ausdrücklich
   her** (`scrollTop = 0`, Name mit `zz-`-Präfix ⇒ **letzte** Zeile ⇒ unterhalb des Folds), misst
   ihn als Station („der Ausgangszustand ist gemessen: die Zeile ist NICHT sichtbar") und danach das
   Aufrollen. Erst damit beißt G17.
5. **Eine feste Wartezeit hat die Kette an der falschen Stelle geschlossen.** Nach dem Klick auf die
   erste Zeile wartete der Lauf 0,8 s auf das Detail-Panel; `selectSpace()` holt erst die Items, und
   das Detail war beim ESC noch zu — der ESC schloss stattdessen die Liste. Die Lehre „auf die
   Bedingung warten, nicht auf die Uhr" stand schon im Skript und ist zum dritten Mal in diesem Block
   gebrochen worden.
6. **Die Bilanz des Vortages war um 5 zu hoch.** Der Block vom 2026-10-06 notiert `pytest` 1238 →
   **1246**; **gemessen** sammelt `HEAD` **1241** Tests ein (`pytest --collect-only`), dieser Block
   kommt auf **1245** (+4 neue, **0 gelöscht, 0 umgedreht**). Korrigiert wird die Zahl, nicht der
   Wächter — die Notiz ist eine Behauptung, `pytest --collect-only` ist die Messung.

7. **Das Gegenlauf-Rig hat vier der sechs Mutationen nie ausgeführt — und die erste „6/6“ war eine
   Behauptung ohne Beleg.** `returncode != 0` gilt auch für einen Lauf, der am **Login** scheitert (Exit 2),
   und das Rig **startete die mutierte Datei statt der Probe** (`str(datei)` statt `str(PROBE)` — für die vier
   CSS-Mutationen also `python app.css`, SyntaxError, Exit 1). Es zählte also **fünf** „wirksame“ Mutationen,
   von denen keine eine Station durchlaufen hatte. **Jetzt** gilt: bemerkt ist eine Mutation nur, wenn die
   **erwartete Station in der Probe-JSON rot** steht, und **fehlt** die JSON, gibt das Skript das stderr-Ende
   aus — die Fehlerursache war zweimal die, dass sie weggeworfen wurde. **Erst damit war der grüne
   Gegenlauf G17 überhaupt eine Aussage**: die neue Zeile war bei 29 Spaces **zufällig** sichtbar. Nach der
   Korrektur **6 von 6**, jede mit benannter roter Station (`g13` → S1/P9-116 · `g14`/`g15` → S5/P9-117 ·
   `g16`/`g18` → S5/P9-118 · `g17` → S8/P9-119), alle sechs JSONs im Repo. **Und:** ein abgebrochener Lauf hat
   den Hintergrundprozess mitgenommen und `app.css` **mutiert** im Baum hinterlassen — der Wächter hat das
   **sofort** gemeldet, die Wiederherstellung kam byteweise aus dem Snapshot des Rigs.

### Vier Befunde aus diesem Block, die keine Abnahmezeile sind

1. **Der Auftrag dreht zwei Locks des Vortags — und das ist der eigentliche Punkt.** P9-AN
   verlangte die **Eingabefeld**-Fläche für die unausgewählten Menüpunkte, P9-AO den
   **Rail-Auswahl-Fill**; der Nikinger hat am selben Tag beides umgedreht (P9-AV). Vier Wächter
   aus `test_settings_chain.py` und **zwei** aus `test_static_routes.py` waren damit an korrektem
   Code rot und wurden **im selben Commit** umgeschrieben — mit beiden Lesarten und Datum im
   Docstring, nicht gelöscht. Der Satz „P9-AN verlangt die Eingabefeld-Fläche" bleibt im Repo
   stehen, damit die Umkehr nachlesbar bleibt und niemand sie zurücksetzt.
2. **`#space-member-list` hatte überhaupt keine Regel.** Der Browser lieferte Aufzählungspunkte
   (`list-style: disc`) **und** 40 px Einzug — dieselbe Fehlerklasse wie P9-AX, nur **40 px**
   statt 33, und **an einem Element, das im Harness nicht darstellbar ist**. Gebaut wird es aus
   dem Standard abgeleitet, nicht aus einer Messung; das steht so in der Zeile.
3. **Der Menüpunkt ist damit optisch kein Baum-Eintrag mehr, obwohl er `.tree__folder` trägt.**
   P9-AF wollte die Wiederverwendung der Baumzeile; die Fläche kommt jetzt aus der
   Standardknopf-Familie. Die **Geometrie** (Höhe, Polster oben/unten, Schrift, Rundung) bleibt
   die der Baumzeile, und genau das ist getrennt geprüft und getrennt gemessen — aber eine
   Änderung, die aussieht wie „die Menüpunkte sind jetzt Knöpfe", wäre eine stille Abweichung von
   P9-AF und wird hier benannt.
4. **Der Gegenlauf G11 hat eine Lücke in der Messung gefunden, nicht im Build.** Ohne `flex: 1`
   auf dem Anlege-Feld nimmt das Feld seine Eigenbreite (194,89 px), der Knopf **schrumpft** auf
   127,11 px — und die Paarbreite ist wieder exakt die Inhaltsbreite, also sind **beide
   Bündigkeits-Stationen weiterhin grün**. Die Station prüfte nur die Kanten, der Lock aber
   verlangt zusätzlich „Space anlegen in seiner Größe gleich lassen" (wörtlich so). Die Station
   misst jetzt die **Eigenbreite** an einer Kopie desselben Knopfes außerhalb der Flex-Zeile;
   damit ist G11 rot. **Ein Gegenlauf, der grün bleibt, ist entweder ein Fehler im Lock oder ein
   Fehler in der Messung — hier der zweiten.**

### Drei Befunde aus diesem Block, die keine Abnahmezeile sind

1. **Der gemeldete Überlauf war hier nicht vorhanden — und wird nicht als behoben behauptet.**
   P9-AS sollte den Überlauf von „Space entfernen" mit den „(schreiben)"-Zeilen räumen; gemessen
   sind **121 px Luft**, und eine rechte Ausrichtung kann einen vertikalen Abstand nicht
   verursachen. Offen bleiben zwei Lesarten: **horizontaler** Überstand einer langen
   Mitgliedszeile (die `<li>` hat keine eigene Regel, `word-break` fehlt — passt hier mit 290 px
   bei 332 px) oder **nur bei vielen Mitgliedern**, weil das Panel dann scrollt. Kein Test hier
   entscheidet das; die Sichtprüfung an den echten Spaces des Nikingers ist der fehlende Beleg.
2. **Die Space-Liste kann leer bleiben, wenn man sie zu früh öffnet.** `renderSpaceList()`
   rendert aus `state.spaces`, das erst nach `loadOverview()` steht. Wer „Einstellungen → Spaces
   verwalten" vorher öffnet, bekommt eine leere Liste, und sie bleibt leer (neu gerendert wird
   nur beim nächsten Öffnen). Die Wahrscheinlichkeit **wächst linear mit den sichtbaren Spaces**
   (P9-15: sechs Durchgänge je Space) — im Harness mit zwölf Spaces der Normalfall: der erste
   Lauf maß S1 gegen eine **leere** Rail. **Gemeldet, nicht gebaut** — die Reparatur ist eine
   Zustandsentscheidung (zweiter Hook neben `registerPanel` oder ein Ereignis).
3. **Zwei Wächter sind an korrektem Code rot geworden und im selben Commit korrigiert** — beide
   kannten den neuen Knopf nicht: `class="btn settings-back"` mit fester Klassenreihenfolge (jetzt
   `btn btn--icon settings-back`) und ein `hidden`-Test auf dem **ganzen** Element (das
   `<svg aria-hidden="true">` enthält das Wort). Ein Wächter, der am Muster scheitert, sieht wie
   ein Befund aus.


**Zwei Zeilen, die nicht beim Umsatz liegen — sie sind benannt, weil sie jemand suchen wird:**

- **P9-92 wurde gegen den *Alte-Adresse*-Dialog eng gezogen**: `.account-nav` hat seit dem Umbau
  genau **einen** Träger, und ein Wächter prüft das mit — sonst wäre „nur noch eine Stelle" eine
  Behauptung, die beim nächsten Umbau stillschweigend falsch würde
  (`test_account_nav_stays_layout_only_on_the_legacy_dialog`).
- **P9-84 misst gegen die echte Baumzeile**, nicht gegen eine Zahl aus demselben Skript. Ein
  Wächter, der die Optik *behauptet* statt sie zu messen, wäre die neunte Wiederholung der Lehre
  aus den letzten Phasen; der Test prüft deshalb die **Ursache** (keine kopierten Werte), das
  Skript die **Wirkung** (gemessene Werte).

---

---

# `[VERIFY]`-Bilanz

## Was diese Zahl nicht ist

**34 belegte Einträge, nicht 40.** Die 40 ist die Größe des **Nummernbereichs** V145–V184, und die
Übergabe führte sie als „40 Einträge". Gegen die Quellen gezählt:

| Bereich | Zahlen | Belegt |
|---|---|---|
| V145–V166 (Plan §13 + Step C) | 22 | **22** — V166 steht nicht im Plan-Register, sondern nur im Session-Block vom 2026-09-25 (`devN` für LXC braucht PVE ≥ 8.1) |
| V167–V172 | 6 | **0** — in keiner Repo-Datei definiert, sie kommen nur als Bereichsangabe vor (`§12`/`§13`: „V145–V172") |
| V173–V178 (doing §10) | 6 | **6** |
| V179–V184 (trace §8) | 6 | **6** |

**V167–V172 sind reserviert und unbelegt.** Sie zu belegen wäre Erfindung, sie umzunummerieren hieße,
einen 📕-Snapshot zu editieren. Sie bleiben als Lücke stehen, damit niemand darauf aufbaut.

**Und zwei Nummern sind je zweimal vergeben:**

| Nummer | Lesart A (Plan §13) | Lesart B (Step-A-Runbook §5, „neu, hier") |
|---|---|---|
| **V162** | Wächst `_trash/` durch die Asset-Verschiebungen seit N5 messbar? (Step G) | Setzt ein Tailscale-TCP-Forwarder (`tailscale serve --tcp`) die Tailnet-ACLs durch? |
| **V163** | Betrifft der 3.4.7-Security-Fix dieses Projekt? (Step H) | Reicht `socat` mit `SystemCallFilter=@system-service` und `MemoryDenyWriteExecute=true`? |

Beide Lesarten stehen unten je mit ihrem eigenen Stand — eine stille Auswahl einer der beiden wäre
die Sorte Falschheit, die diese Matrix verhindern soll.

## Stand je Eintrag

| ID | Frage | Stand | Antwort / Beleg |
|---|---|---|---|
| V145 | `docs/INDEX.md` nach der Rotation unter dem Größen-Kriterium, mit allen P9-Zeilen? | ✅ **beantwortet 2026-10-03** | **Ja — nach der Nachtrags-Rotation, und mit einem Kriterium, das die Datei überhaupt erreichen kann.** `docs/INDEX.md` steht bei **38.299 B** gegen den neu baselinierten Softcap (40.960 B). Dieselbe Frage war am selben Tag zweimal gestellt und zweimal anders beantwortet: der Stand **beim Bau** (38.822 B auf `06ab4f6`, damals ✅) und der Stand **heute**, der in der Matrix als **61.108 B** stand und in Wirklichkeit **71.573 B** waren — 8.249 B daneben, zwei Tage lang, in genau der Zeile, deren Gegenstand eine Dateigröße ist. Aus einem „unerreichbar, aber warum" ist ein ✅ mit benanntem Weg geworden. Zahlen, Rechenweg und Fehlmessung stehen bei P9-3 |
| V146 | Ausnahmeliste in `doc_health.py` deckungsgleich mit der in `docs/INDEX.md` benannten? | ✅ | **heute beantwortet.** `CARD_EXEMPT` (7 Einträge) auf die vier INDEX-Kategorien abgebildet: Harness `.claude/RESUME.md` · Fixtures `phase6_shares/tests/golden/*.md` (3) · geparst `docs/UPDATE_LOG.md` · Vendor/Lizenz 2. **Kein ungenannter Fall:** `header_cards` = 0 Befunde |
| V147 | `pytest`-Baseline wirklich 995? | ✅ | 2026-09-20 gemessen: **995 passed in 185,98 s** |
| V148 | Funnel-Custom-Domain-Ausschluss gegen die **aktuelle** Tailscale-Doku bestätigt? | ✅ | **heute beantwortet.** (a) Die Doku-Seite zu eigenen Domains gibt es nur für **Tailscale PAM**, nicht für Funnel. (b) `tailscale/tailscale#11563`: ein CNAME trägt nicht, *„all tailscale sees (via SNI) is the CNAMEd name and does not know where to route the connection"*. **P9-E damit bestätigt**; der Weg (a) aus `PHASE8_6_CLOSEOUT_HANDOVER.md` §4.2 existiert weiterhin nicht |
| V149 | Welche Metadatenfelder leiten sich aus der Basis-URL ab? | ✅ | **alle abgeleitet, keines fest**; beim Einlösen kein `iss`-Check ⇒ der Basis-URL-Wechsel invalidiert keine Token-Familie |
| V150 | Hält der Anthropic-Connector unter der neuen Domain, in **beiden** Konten? | ⬜ **zurückgestellt, wandert nach P10** | **niklas ✅** (echter `list_spaces` über die neue Adresse, 2026-10-03) · zweites Konto steht aus — dieselbe Zeile wie P9-13, mit demselben Rest · **2026-10-04: ⬜, zurückgestellt und nach P10 gewandert** (Plan §0.1a), **kein Blocker** — die Marke wechselt von ⚠️ auf ⬜, weil ⚠️ in dieser Matrix *erfüllt mit benannter Abweichung* heißt und ein Konto keine Abweichung ist, sondern ein fehlender Schritt |
| V151 | Latenz über den VPS gegenüber 372,9 ms über Funnel? | ✅ | **beantwortet 2026-10-03: nein, nicht relevant — 2,4–3,6 %.** Der VPS-Anteil ist **76–113 ms auf ~3,1 s** (P9-15: beide Beine mit demselben Instrument aus dem Browser, drei Läufe je Bein, `status` 200). **Und die Prämisse der Frage ist korrigiert:** die 372,9 ms sind **nie über Funnel** gemessen worden, sondern in-process auf synthetischem Bestand (`ui_budget.py`, `httpx.ASGITransport`, `TemporaryDirectory`, 220 Items) — als Vergleichsmaßstab unbrauchbar und 8,3× zu niedrig. **Die eigentliche Kostenstelle ist der Endpunkt, nicht der Weg:** `_overview()` macht **einen `store.search()`-Durchgang pro Bucket und noch einen für die Liste, pro sichtbarem Space** — 5 Buckets seit `doing`, also 6 Durchgänge je Space, bei 4 sichtbaren Spaces **24 vollständige Durchgänge** über 197 Items, und jeder Durchgang liest jede indizierte Datei neu (`limit` ist egal, ~100 ms). Die Kosten wachsen **linear mit den Spaces**, nicht mit den Items. **Als Inhalt einer neuen Phase benannt, jetzt nicht verfolgt** (Nikinger 2026-10-03) |
| V152 | Tailscale-eigenes Watchdog-Feature ohne Add-on? | ✅ | „Gibt es nicht" |
| V153 | Polkit-Regel oder `sudoers`-Fragment? | ✅ | **polkit**; `sudoers` ist nachweislich ausgeschlossen (`NoNewPrivileges=true` → `setpriv` belegt `no_new_privs`). Die JS-Regel prüft zusätzlich `unit == "tailscaled.service"` und `subject.user == "savefyx"`; die Probe (Wegwerf-Unit, `tailscaled` unberührt) meldete `AUTORISIERT` bei `User=root` |
| V154 | IOMMU-Zustand des 3060-Hosts — LXC oder volle VM? | ✅ | **LXC** — Plan-§5.2-Umschaltpunkt greift nicht, LXC teilt den Host-Kernel |
| V155 | Zeilennummern `mcp_local_vision_server.py:223/274` gegen den aktuellen Stand | ✅ | **heute beantwortet: beide Anker sind gewandert** (C6 hat die Datei umgebaut, 361 Zeilen). `:223` ist heute die Nicht-JSON-Fehlerbehandlung, **nicht** die Startzeile; `:274` ist heute `def serve(endpoint, model)` — die reparierte Funktion, aber aus einem anderen Grund als geplant. Echte Anker heute: `resolve_endpoint()` `:97`, `DEFAULT_ENDPOINT` `:50`, `--endpoint` `:328`. **Drift klein, hier datiert korrigiert statt im 📕-Plan** |
| V156 | Bei `qwen3-vl:8b` bleiben oder VRAM-Luft nutzen? | ✅ | **bleiben**, damit der Geschwindigkeitsgewinn dem GPU-Wechsel und nicht dem Modell zuzuschreiben ist |
| V157 | Ist `document.fullscreenElement` beim ESC-`keydown` gesetzt? Chromium **und** WebKit | ⚠️ | **Chromium gemessen** (echter `requestFullscreen()` + `press("Escape")`): gesetzt, der einfache Guard genügt. **WebKit ungemessen** (kein Binary im Playwright-Cache). **Und für den gemeldeten Fall gegenstandslos:** die App ruft `requestFullscreen()` nirgends auf, der Guard adressiert natives macOS-Vollbild nicht (P9-27) |
| V158 | Reicht `closest()` zur Chip-Unterscheidung, oder braucht es eine eigene Klasse? | ✅ | **Am gewählten Anker nicht nötig** — `.tree__space` hat keine verschachtelten interaktiven Kinder. Ein Guard, der nichts ausschließt, wäre ein irreführender Test (P9-31) |
| V159 | Erscheint `doing` im `<select>` ohne Codeänderung? | ✅ | ja im Editor-Dropdown (`editor.js`), für den Anlegen-Dialog gegenstandslos (TYP-Vokabular, kein Status-Knopf) |
| V160 | Was ist `assignee`? | ✅ | **Space-Name, ohne Validierung** (Lock P9-U) |
| V161 | Dauer des Index-Neuaufbaus über den echten `DATA_ROOT` | ✅ | **≤ 1,05 s für 197 Items** beim Deploy `v3.1.0` (P9-43) |
| V162 *(Lesart A)* | Wächst `_trash/` durch die Asset-Verschiebungen seit N5 messbar? | ⬜ | unberührt — eine Löschung wurde live noch nicht beobachtet |
| V162 *(Lesart B)* | Setzt `tailscale serve --tcp` die Tailnet-ACLs durch? | ⚠️ | **teils beantwortet am 2026-10-04, mit Zitat — für den HTTP-Modus ausdrücklich, für `--tcp` schweigen die Docs.** Die Tailscale-Doku sagt wörtlich: *„access control rules apply to Serve just like any other service … those rules will also apply to the services you're sharing with Serve"* (Tailscale Serve, *Get started with Serve*, <https://tailscale.com/docs/features/tailscale-serve>, last validated 20.01.2026). Die **CLI-Referenz** zu `--tcp` / `--tls-terminated-tcp` (<https://tailscale.com/docs/reference/tailscale-cli/serve>, last validated 26.01.2026) nennt **kein** ACL-Verhalten — in **keine** Richtung. Grundsatz: *„By default, all connections between devices in your tailnet are denied unless explicitly permitted through your tailnet policy file"* (<https://tailscale.com/docs/features/access-control>). **Kein Gegenlauf möglich, und warum:** eine Widerlegung braucht eine *abgelehnte* Verbindung von einem zweiten Tailnet-Knoten — auf dieser VM gibt es keinen zweiten, mit dem ich Kommandos ausführen kann (`tailscale status` listet sie, aber Shell-Zugang ist Nikinger-Sache). **Konsequenz für die getroffene Entscheidung: keine.** `socat` ist deshalb **nicht** widerlegt, sondern im Gegenteil gedeckt: die elegante Alternative ist nur für den HTTP-Modus belegt, und eine offene Frage soll keine Firewall-Entscheidung tragen. Für den reinen L4-Relay von Caddy ist die ACL-Frage ohnehin zweitrangig — die Grant-Regel (`tag:sharefyx-edge` → `100.93.43.122:8765`) nennt Ziel-IP **und** Port, und `socat` ist ein gewöhnlicher Listener auf `tailscale0`, für den das ACL-Modell ohne Zusatzannahme gilt (Runbook §3 Befund 6). **Bleibt ⬜ für eine echte Messung**, Marker ⚠️ nach der Statusregel: das Kriterium ist in anderer Form beantwortet als gefragt. **Nachtrag 2026-10-07 (Portscan Lauf 4): kein Gegenlauf, sondern ein eigener Befund.** Vom MacBook (Hotspot, Tailscale an) ist `100.93.43.122:8765` **`open`**. Das prüft **nicht** `tailscale serve --tcp`, denn der Listener dort ist `socat` (`ss`: pid 362706, weiter an `127.0.0.1:8765`) — die Lesart B bleibt deshalb unberührt ⚠️. Es widerlegt aber die Prämisse aus Mini-Plan §5 „die ACL erlaubt 8765 nur `tag:sharefyx-edge`“: das ACL-Fragment `step_a/tailscale-acl.draft.json` ist **additiv**, die bestehenden Regeln des Tailnets gelten weiter und lassen das MacBook offenbar durch (die Live-ACL ist nicht gelesen — Schluss, nicht Messung). **Folge, für den Nikinger:** im Tailnet sind Auth und Host-Prüfung der App die einzige Sperre vor 8765; ein unauthentifiziertes `GET /health` auf der Tailnet-IP bekam am 2026-10-07 `400 Invalid host header`. Kandidat für P10, kein P9-Blocker |
| V163 *(Lesart A)* | Betrifft der 3.4.7-Security-Fix dieses Projekt? | ✅ | **nein**, drei Codepunkte (P9-54) |
| V163 *(Lesart B)* | Reicht `socat` mit Syscall-Filter und `MemoryDenyWriteExecute`? | ✅ | **beantwortet durch die Ausführung**: A0b lief, `socat` 1.8.0.0 läuft mit zwei Listenern, `diagnose.sh` danach alle Prüfungen grün |
| V164 | Läuft `deploy.sh` unter der neuen Domain-Konfiguration durch? | ✅ | **beantwortet 2026-10-03, `v3.1.1` ist live:** Release `/opt/sharefyx/releases/20261003T205843.757198Z`, SHA `3719487` = der Release-Commit, `health_gate.sh --expected-version=v3.1.1 --require-todays-update-log --expected-sha=3719487` **9/9 OK** (read-only gegengeprüft, nicht die Quittung übernommen: Symlink, Release-SHA, live-Badge und `## 2026-10-03`-Block alle einzeln nachgelesen). **Kein Index-Neuaufbau**, wie vorhergesagt: das Journal des Neustarts zeigt **keine** `wird verworfen`-Zeile — der trace-Block hat keinen Index-Sprung ausgelöst |
| V165 | Baut ein neuerer 580er `nvidia-uvm` gegen den pve-Kernel? | ✅ | 580.173.02 entpackt, `cuInit = 0` nach zweiter Reboot-Probe grün |
| V166 | Braucht `devN`-Passthrough für LXC PVE ≥ 8.1? | ✅ | `pve-manager/9.2.2` — Bedingung erfüllt |
| V167–V172 | *(nie definiert)* | — | **reserviert, unbelegt.** Siehe oben |
| V173 | Steht irgendwo ein Eimer-Name oder Status-Anzeigewort fest im Code? | ✅ | **gemessen:** ein Treffer (`state.js`, `filter: "open"`), ein Kommentar, Archiv-Skripte, die nicht erneut laufen. Die vier alten Smokes nehmen `.overview__space-count.first` und sind unkritisch |
| V174 | Muss `phase1_storage/CLAUDE.md` §Geerbte Contracts mitgezogen werden? | ✅ | **Nein**, solange P9-66 hält — und es hält (P9-66) |
| V175 | Port 18776 frei? | ✅ | im Repo frei; zur Laufzeit `ss -ltn` leer, weiterhin frei |
| V176 | Lassen sich die App-Fixtures in `phase9_hardening/tests/` benutzen? | ✅ | **nein**, gemessen: dort kein `conftest.py`. Deshalb stehen die Overview-Tests in `phase5_ui/tests/test_overview.py` |
| V177 | `pytest`-Baseline am Bau-Tag? | ✅ | 1122 passed in 200,9 s; Erwartung nach dem Block 1128 — eingetroffen |
| V178 | Ist `#field-status` im Vorschau-Modus bedienbar? | ✅ | `setEditorMode()` deaktiviert nur `[data-md]`; das Select sitzt im zugeklappten `<details id="meta-panel">`, die Probe klappt es auf — im Browser bestätigt |
| V179 | Echte Space-Namen als Git-Autor unproblematisch? | ✅ | `fabian`, `Home-Server`, `IT-Sekus-Projekt`, `Janick`, `niklas` — keiner berührt P9-AC; ein führendes `-` ist kritisch (`--author` bekommt den Wert als eigenes argv). **Gemeldeter Nebenbefund:** im DATA_ROOT liegt ein Eintrag namens wörtlich `*.sqlite3` |
| V180 | Schickt `saveItem()` den ganzen Formularstand? | ✅ | `editor.js:500–503` |
| V181 | `api.py:1001/1003` ein `if/else`? | ✅ | ein Request, ein Store-Aufruf, ein Commit |
| V182 | `updated_by` eines fremden Items innerhalb oder außerhalb von `<untrusted_content>`? | ✅ | **heute am Code: außerhalb.** `wrap_untrusted()` wirkt nur auf `item.snippet` (`tools.py:258`) und `item.body` (`:529`); `updated_by` steht neben `assignee` in der Metadaten-Liste. Rule 4 unberührt |
| V183 | Schreiben außerhalb `tools.py`/`api.py` noch irgendwo `updated_by`? | ✅ | nein — nur Operator- und Fixture-Skripte, alle bei `actor=""` (P9-AB); die T7-Allowlist ist deshalb heute **leer** |
| V184 | Ist `state.ownSpace` beim Öffnen des Editors immer gesetzt? | ✅ | **heute am Code: ja.** `app.js:283` setzt es in `init()` aus `/me`, **vor** `/meta` und vor `loadOverview()` — der Editor kann nicht ohne ihn offen sein. Der `!state.ownSpace`-Guard (`editor.js:781`) bleibt trotzdem die richtige Verteidigung |
| V185 | Welche Optik meinen die Menüknöpfe — „Verschieben" oder die Baumzeile? | ✅ | **beantwortet 2026-10-05 per Bild: die Baumzeile `.tree__folder`** („Offen"), nicht „Verschreiben". P9-AF wurde danach korrigiert, und die Umsetzung **verwendet die Klasse** statt die Optik zu kopieren — sonst wäre die dritte Variante entstanden, die P9 am 2026-10-01 bei `.account-nav` erst entfernt hat |
| V186 | Öffnet das Update-Banner heute `#update-log-dialog`? | ✅ | **nein.** Das Banner trägt **einen** Knopf, „Verstanden" (`#update-banner-dismiss`), und keinen zweiten Weg ins Log. Plan §3 Schritt 1 sprach von einem „Alle Updates ansehen" — das war eine Annahme über ein Bedienelement, das es nicht gibt. Der einzige Weg ist der Menüpunkt |
| V187 | Welche historischen Proben sprechen die alten Overlay-IDs an? | ✅ | **zwei Skripte, beide mit datiertem Kopfvermerk, keines umgebaut** (Plan §3 Schritt 5): `phase8_6_ui_polish/scripts/p86_block_b_self_check.py` (wartet auf `#account-dialog:not([hidden])`) und `phase8_ui_graph/scripts/p8_16_glass_fallback_probe.py` (drei Zugriffe). **Ein umgebauter historischer Beleg beweist nichts mehr über den Block, für den er steht** — dieselbe Begründung wie bei den gegen Proben. `p86_block_h_self_check.py`/`_h_r_*`/`p86_polish_smoke.py` erwähnen `.account-nav` nur im Kommentar bzw. als Klassenabfrage und laufen weiter |
| V188 | Ist das Beenden des macOS-Vollbilds per ESC Betriebssystem- oder Browser-Verhalten, und kann die Seite es verhindern? | ✅ **beantwortet 2026-10-05, vier Quellen, eine davon am Repo gemessen** | **Betriebssystem-Verhalten; die Seite kann es nicht verhindern, nur verschieben — und die Verschiebung existiert auf dem MacBook nicht.** Die vollständige Beweiskette mit wörtlichen Zitaten und Fundstellen steht in der **P9-27-Zeile** (sie ist derselbe Sachverhalt, und die Quelle gehört nicht an zwei Stellen). In Kurzform: `app.js:259` ist der einzige `fullscreen`-Bezug der App, die Web-API greift im nativen macOS-Vollbild nicht · WHATWG Fullscreen §4/§6/§8 halten fest, dass ein **immer wirkender** Ausgang Pflicht ist (Anti-Spoofing) und dass Keyboard Lock ihn nur von „Tastendruck" auf „langer Tastendruck" verschiebt · WICG Keyboard Lock §7 **darf** den Ausgang nicht abschalten, auch nicht bei *allen* angeforderten Tasten · §4.2 schließt F11/natives Vollbild aus, und MDN-`browser-compat-data` sagt `safari: false`. **Die Plan-Aussage „nur in Chromium" ist damit nicht geglaubt, sondern gemessen — und für den Anwendungsfall schärfer: gar nicht vorhanden.** **P9-27 ist damit ⚠️, D1 ist geschlossen** (Plan §4, Nikinger-Entscheidung 2026-10-05: *kein Code*) |

**Bilanz: 38 belegte Einträge — 35 ✅ · 1 ⚠️ · 2 ⬜.** *(Stand 2026-10-05, nach V188: die Matrix-Bilanz des
settings-Blocks war 34 ✅ · 1 ⚠️ · 3 ⬜ — V185/V186/V187 ⬜→✅, V188 neu und offen; V188 ist heute
beantwortet, die übrigen beiden ⬜ sind V150 (zweites Konto, wandert nach P10) und V162 *(Lesart
A)* (eine live noch nicht beobachtete Löschung). Die Zahl **40** von 2026-10-03 war der Nummernbereich; sie stimmt
jetzt zufällig wieder, weil vier belegte Nummern dazukamen und sechs weiterhin reserviert sind — eine
Koinzidenz, keine Bestätigung. Die Regel zählt Zeilen, nicht Bereiche.)* **Zählregel, ausdrücklich:** eine doppelt
vergebene Nummer (V162, V163) zählt **einmal**, und zwar mit ihrer **Lesart A**; die Tabelle hat
deshalb 36 Markerzeilen plus die reservierte Bereichszeile V167–V172 = 37. Wer nach der
Zeilen-Lesart zählt, kommt auf 31 ✅ · 3 ⚠️ · 2 ⬜. *Datierte Korrektur 2026-10-03:* hier stand
**28 ✅ · 3 ⚠️ · 3 ⬜** — die Summe 34 stimmte, die beiden anderen Zahlen lagen je eins daneben
(⚠️ und ⬜ gegeneinander vertauscht), was nach einer Symmetrie aussieht, die es nicht gibt.
Dazu 6 reservierte, unbelegte Nummern
(V167–V172) und die drei geerbten:

| ID | Frage | Stand |
|---|---|---|
| **V118** *(geerbt)* | Zwillingskanten — zwei Linien gewollt? | ✅ **beantwortet 2026-09-26 und entschieden 2026-10-05: eine Linie.** Erste Lesart (gemessen, eingefroren): zwei Linien, die zweite gestrichelt. Zweite Lesart (Nikinger): *„Wenn A auf B verlinkt, ist B für A automatisch relevant."* Gebaut als Verwerfen der impliziten Kante **bei der Übernahme** (`rebuildImplicitEdges()`), nicht in `drawEdges()` — sonst zählte die Gradzahl weiter, und die Knotengröße folgt ihr. Der Test ist mit Datum **umgedreht und umbenannt**, nicht gelöscht; beide Lesarten stehen in seinem Docstring |
| **V136** *(geerbt)* | Chip-Umstellung vs. `bindFolderDropTarget()` | ✅ **gegenstandslos am gewählten Anker** (P9-31/V158) |
| **V120** *(geerbt)* | Dynamischer Tab-Titel | ⬜ **bewusst offen**, außerhalb jedes Scopes (Plan §15) |

---

# Was diese Matrix nicht beweist

**Vier Dinge warten auf den Deploy `v3.1.1`** (Badge `app.html:20` + `##`-Block am Deploy-Tag, sonst
brennt das `deploy.sh`-Gate P6-X ab). Keines ist eine offene `P9-`-Zeile — sie stehen hier, damit
niemand sie mit einem eingecheckten Block verwechselt:

1. **trace-Block live.** P9-69–P9-82 sind gegen eine Zwei-Principalen-Wegwerf-Instanz mit echter
   Git-Historie belegt (8/8) — live sehen ist eine andere Aussage. Erwartbar: jedes bestehende Item
   zeigt **kein** „Zuletzt geändert von", bis es erstmals geschrieben wird (P9-AB); Eigenschaft,
   kein Fehler, gehört in den Changelog-Text. **Kein** Index-Neuaufbau, anders als nach Step F.
2. **B17 live gesehen.** Die Vorschrift-Fläche ist per Pixel-Probe 14/14 belegt, die Sichtprüfung am
   echten Gerät steht aus. Offen bleibt der **Kontrast 4,38:1** — besser als vorher (3,36:1) und
   weiterhin kein WCAG-AA (4,5:1 für normalgroßen Text; 14 px/500 ist kein „large text").
3. **Eine Live-Löschung.** Step G ist im Browser belegt (14/14), die Beobachtung am echten Space steht aus.
4. **Step H im Release-venv nach dem Pin** — gehört an den nächsten Deploy.

**Und zwei Lücken, die keine Messung schließen kann:**

- **Der Gate-Smoke aus Plan §11 (GA2) wurde nie gebaut — und die Lücke ist heute um eine Station
  kleiner.** `phase9_hardening/scripts/` hat die sechs Block-Proben (Reload, doing, trace, btn2,
  btn3, Step G) und seit dem 2026-10-03 eine siebte (`p9_step_d_self_check.py`, **16/16** mit zwei
  Gegenläufen im Repo); ein `p9_hardening_smoke.py` als **ein** Skript mit allen Stationen gibt es
  weiterhin nicht. Damit ist von den drei Zeilen, die 2026-10-03 als „ohne Probe" gemeldet waren,
  **eine** geschlossen: **P9-29 und P9-30 sind jetzt gefahren** (Plan-§11-Station 1 und 3, plus
  die ESC-Stationen zu P9-28). Offen bleibt **allein P9-27** — ESC im **nativen** macOS-Vollbild.
  Das ist keine Versäumnis, sondern eine Eigenschaft: kein WebKit-Binary im Playwright-Cache, und
  natives Vollbild ist per Spezifikation nicht automatisierbar (der Guard selbst ist für den
  gemeldeten Fall nachweislich ein No-op, `app.js` ruft `requestFullscreen()` nirgends auf).
- **GA1/GA4** sind durch die Block-Proben und den Deploy `v3.1.0` überholt; die Nikinger-Sichtprüfung
  (GA3) ist für die sechs `p9_trace_*`-Bilder am 2026-10-02 erfolgt, für B17 offen.

**Reihenfolge, Stand 2026-10-03 nach A7+A8:** (1) **zweites Claude-Konto umstellen** — schließt
P9-13 und V150 von ⚠️ auf ✅, es ist ein Konto und kein Code · (2) **Release-Commit + Deploy
`v3.1.1`** (Badge + `##`-Block **erst am Deploy-Tag**, sonst brennt das `deploy.sh`-Gate P6-X; der
trace-Block kommt mit, **kein** Index-Neuaufbau) — schließt V164 und P9-15, denn `health_gate.sh`
macht die authentifizierten `/api/v1/overview`-Läufe, die P9-15 gegen **372,9 ms** stellt · (3)
Rest Gate/Z: Übersichtsgrafik §12.4 (**gerendert und angesehen**), `docs/INDEX.md` rotieren,
ROADMAP-Zeile, Phase auf ✅. Herleitung im Phase-Head und in `SESSIONS_ARCHIVE.md`.

**[2026-10-05, zwei Korrekturen an diesem datierten Block — er bleibt als Momentaufnahme stehen,
die Sache stimmt an zwei Stellen nicht mehr:]**

1. **Schritt (2) ist erledigt, aber er hat nicht geschlossen, was er schließt.** `v3.1.1` ist am
   2026-10-03 live, **V164 ✅** — und **P9-15 bleibt ⚠️**: das dort genannte Kriterium stellt gegen
   **372,9 ms**, und dieser Wert ist nie über Funnel gemessen worden (V151: in-process auf
   synthetischem Bestand, 8,3× zu niedrig). `health_gate.sh` liefert also **Läufe ohne
   Kriterium**; der Deploy vom 2026-10-03 hat P9-15 nicht geschlossen, und der Satz hier
   behauptet es. Die Zeile selbst (oben) war schon am selben Tag korrekt auf ⚠️.
2. **„Offen bleibt allein P9-27" ist seit heute überholt.** P9-27 ist ⚠️ (V188 beantwortet, vier
   Quellen), und **D1 ist geschlossen** (Nikinger-Entscheidung 2026-10-05: *kein Code*). Was bleibt,
   ist **nicht automatisierbar** und damit **kein offener Punkt**: natives macOS-Vollbild hat keine
   Web-API, und der Guard `app.js:259` ist dafür nachweislich ein No-op — gemessen, nicht vermutet.

