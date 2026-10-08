---
status: live
purpose: Abnahmematrix der Phase 9 (P9-1 – P9-82) und [VERIFY]-Bilanz (V145 – V184) — jede Zeile mit Stand und Beleg, jeder Marker mit Antwort oder offenem Grund
read-when: beim Gate/Z-Checkout, bei jeder Frage „ist das schon abgenommen?", wenn eine Abnahmezeile oder ein [VERIFY] aus den Plänen nicht auffindbar ist, oder wenn jemand eine Zeile auf ✅ setzen will, für die es keinen Beleg gibt
detail: L2
up: ./CLAUDE.md
down:
  - ABNAHME_MATRIX_STEPS.md     # Teil: Step 0–H, Phasenweit (P9-1 – P9-58)
  - ABNAHME_MATRIX_BLOECKE.md   # Teil: Blöcke und Bildsichtungen (P9-59 – P9-120)
  - ABNAHME_MATRIX_FEEDBACK.md  # Teil: Block feedback (P9-121 – P9-137), seit 2026-10-08
  - ABNAHME_MATRIX_VERIFY.md    # Teil: [VERIFY] je Eintrag (V145 – V188)
  - ../docs/concepts/phase9_hardening_plan.md        # P9-1 – P9-58, §13-Register, §15 P10-Liste
  - SESSIONS_ARCHIVE.md                              # die Herleitung jeder Zeile im Wortlaut
updated: 2026-10-07 (**Portscan von außen eingetragen**: P9-11 und P9-94 ⬜ → ✅, Bilanz 104 ✅ · 12 ⚠️ · 1 ⬜ — vier Läufe vom MacBook plus ein Kontrolllauf, Rohausgabe `probes/p9_11_portscan_2026-10-07.txt`. Der `21/tcp open` auf Heim-IP und VPS ist ein **Pfad-Artefakt** (antwortet auch für `1.1.1.1` und `9.9.9.9`); die alte Gegenprobe „alles `filtered`, genau 8765“ datiert korrigiert; **Lauf 4 `open`** ist kein Gegenlauf zu V162 B (Listener ist `socat`), widerlegt aber die ACL-Prämisse des Mini-Plans — Befund für P10) | 2026-10-06 (**Nachsatz aus der dritten Sichtprüfung**: +1 Zeile **P9-120** (Lock P9-BF, Bild 08) mit **1 ✅** — das Kästchen der Space-Zeile ragt 8 px nach links, damit der Text innen wieder den Standardabstand hält (innen vorher **1 px links** gegen **9 px rechts**), die Beschriftung bleibt bündig mit dem Titel. Bilanz **102 ✅ · 12 ⚠️ · 3 ⬜** · **drei Wächter umgeschrieben, keiner gelöscht**: der Abstand-Wächter prüft `margin` **namensgenau** statt per Substring (`margin-bottom` stand auf keiner Verbotsliste), die Station P9-117 rechnet **beide** Polster, und die Verbotsliste trägt die drei `margin`-Langformen) | 2026-10-06 (**dritte Bildsichtung gebaut** — Abnahme **P9-116–P9-119** mit **4 ✅** statt der vier notierten, **nicht gebauten** Zeilen P9-112–P9-115: **P9-112 ist widerrufen** (der Nikinger hat den Auftrag auf „nur bei Spaces verwalten" eingeschränkt), die drei anderen sind abgelöst, weil ihre Nummern inzwischen etwas anderes prüfen; die Zuordnung steht als Tabelle im Abschnitt · **Bilanz 101 ✅ · 12 ⚠️ · 3 ⬜** · **sechs Befunde ohne Abnahmezeile**, darunter `box-sizing: border-box`, die Sammelregel und eine Station, die den eigenen Fehler nicht bemerkte · **datierte Korrektur:** die 1246 `pytest`-Tests des Vortages sind **1241** gemessen) | 2026-10-03 (**A7a + A7 + A8 gefahren** — Nikinger-Schritte, von M3 vorbereitet und gemessen; P9-10b ✅ · P9-12 ✅ · P9-13/V150 ⚠️ „1 von 2 Konten") · **A7a** = der risikoarme Vorlauf nur über `ALLOWED_HOSTS` (kein `resource`-Wechsel, Token bleiben gültig): neu lokal 200 · alter Funnel lokal 200 · **extern `https://sharefyx.eurofyx.com/health` 200 mit `ssl_verify_result=0`**, JSON `{"status":"ok",…}` — vorher an derselben Stelle 400 bei gültigem TLS · **A7** = der Schnitt: `PUBLIC_BASE_URL` auf die Domain, `LEGACY_ORIGIN`/`LEGACY_UNTIL=2026-10-17` dazu; `issuer` und alle drei Endpunkte zeigen auf die neue Domain, Start ohne Traceback · **A8**: Konto niklas liefert `list_spaces` über die neue Adresse, das zweite steht aus · **P9-15 bleibt ⬜** und gehört an den Deploy-Tag (`health_gate.sh` authentifiziert) · **Befund 4 bestätigt**: der A7-Restart entwertet alte Token (`resolver.py:48`), die Neuanmeldung war zwingend | 2026-10-03 (**Step D belegt** — zweite Fassung, opencode/M3, **kein Produktcode-Touch**, kein Deploy) · **P9-28/P9-29/P9-30 von ⚠️/⬜ auf ✅**: die Browser-Probe `p9_step_d_self_check.py` (Plan-§11 GA2-Station 1, die erste von dreien, die nie lief) fährt **16/16** gegen eine eigene TLS-Wegwerf-Instanz auf Port 18781 · **echte Maus-Input-Pipeline**, nicht `dispatchEvent` — Station 2 misst den vom Browser erzeugten Ereignisstrom (`dragstart=1, dragover=19, drop=1`, Item-ID im `dataTransfer`), weil sonst nur der Listener belegt wäre · **P9-30 als berechneter Stil** (`dashed`, `rgb(62,141,243)`) plus zwei Bilder, nicht als Klassennamen · **zwei Gegenläufe liegen rot im Repo** (G1 Space-Bindung raus → 5 Stationen rot, 6–9 grün; G2 `fullscreenElement`-Guard raus → Station 9 rot), mit `--report`/`--screenshots-dir` getrennt, damit kein Gegenlauf den Erfolgsbeleg überschreibt (derselbe Fehler wie beim trace-Block 2026-10-02) · **6 Wächter** in `test_step_d_drop_target.py`, Deckung in **beiden** Richtungen (jede ✅-Zeile braucht eine Station, jede Station eine existierende Zeile) · **Bilanz an diesem Tag 68 ✅ · 9 ⚠️ · 6 ⬜** (der heutige Stand steht weiter unten, er wandert) · **P9-27 bleibt ⬜** und das ist eine Eigenschaft: kein WebKit-Binary, natives Vollbild nicht automatisierbar · **drei eigene Fehler im selben Commit behoben**: der Ereigniszähler zählte sich selbst (`start=3, over=57` für einen Zug — Listener bei jedem `evaluate` neu registriert), `store.create()` **hängt** an statt zu leeren (der zweite `start` sah jedes Item doppelt), und die erste Fassung des neuen Tests war rot, weil er `dispatchEvent` im **Docstring** verbot — Wächter läuft jetzt über `tokenize`, nicht über Rohtext | 2026-10-03 (erste Fassung, Gate/Z-Doku-Hälfte Nummer zwei, opencode/M3, **kein Code-Touch**, kein Deploy) — **82 Abnahmezeilen (83 Tabellenzeilen, P9-10 geteilt): 65 ✅ · 10 ⚠️ · 8 ⬜** und **34 belegte [VERIFY]-Einträge**, nicht 40 (V167–V172 sind nie belegt) · **P9-56/57/58 heute gemessen**: Tabu-Diff hat **einen** unangekündigten Treffer (`phase7_spaces_admin/tests/test_space_removal.py`, 17 Z.) · `pytest` 1169, `ui_budget` 5/5 (155,2 KB), `doc_health` 0/0/0/0 · **P9-14 heute geschlossen** (Funnel-Host live 200), P9-10b heute gemessen (weiter 400, erwartet bis A7) · **V146/V148/V155 heute beantwortet**, V182/V184 am Code · **zwei Nummerkollisionen gefunden** (V162, V163 je zweimal vergeben)
---

# Abnahmematrix Phase 9 — P9-1 … P9-82 und `[VERIFY]`-Bilanz V145 … V184

Diese Datei ist der **eine** Ort, an dem steht, welche der 82 Abnahmezeilen der Phase 9 mit welchem
Beleg stehen. Sie ist **L2, nicht Archiv** — die Phase läuft, die Zeilen ändern sich noch. Herkunft
jeder Zeile: Plan §2.5/§3.4/§4.4/§5.6/§6.4/§7.5/§8.8/§9.6/§10/§14 plus die beiden Mini-Pläne;
Herleitung im Wortsinn in `SESSIONS_ARCHIVE.md`. **Nikinger-Entscheidung 2026-10-02:** die Matrix
kommt hierher und nicht in den Phase-Head — der Head liegt über dem Softcap, und ein 82-zeiliges
Archiv hineinzuschreiben hieße, das Falsche zu tun. *Datierte Korrektur 2026-10-07 (Nikinger-Auftrag
„find a fix for the oversize docs"):* „diese Datei" ist seitdem **dieser Hub plus drei lebende Teile**
— `ABNAHME_MATRIX_STEPS.md`, `ABNAHME_MATRIX_BLOECKE.md`, `ABNAHME_MATRIX_VERIFY.md`, jeder unter dem
40-KiB-Softcap (vorher 98.782 B in einer Datei). Die Abschnitte sind per `scripts/move_sections.py`
**wortgleich** gewandert, ihre Überschriften stehen unten mit Zeiger. **Teile, kein Archiv:** die
Zeilen zählen weiter in die Bilanz, ihr Marker darf sich ändern, und P9-3/P9-6/V145 tragen
Bytezahlen, die `test_acceptance_numbers.py` bei jedem Lauf nachmisst. Die Bilanz-Überschrift steht
nur hier.

## Stand in einem Satz

**130 Tabellenzeilen für 130 Abnahmezeilen: 116 ✅ · 13 ⚠️ · 1 ⬜** (P9-10 in zwei prüfbare Hälften
geteilt; seit 2026-10-05 kommen der **settings-Block** P9-83–P9-95 mit 12 ✅ und **einem** ⬜
dazu — P9-94, der Portscan, ist ein Schritt des Nikingers und durch keinen Test ersetzbar —,
sein **Nachtrag** P9-96–P9-102 aus der Bildsichtung mit **5 ✅ und 2 ⚠️**, und die **dritte
Bildsichtung** P9-103–P9-111 mit **9 ✅**. Die beiden ⚠️ sind
**keine offenen Punkte**: P9-97 trägt die vom Nikinger entschiedene Abweichung im linken
Polsterwert, P9-99 den gemessenen Umweg (`justify-content` statt des im Plan genannten, wirkungslosen `text-align`). **A7+A8 sind am 2026-10-03 gefahren** (A7a als risikoarmer Vorlauf, dann A7, dann A8):
P9-10b und P9-12 sind **beide ✅**. *Datierte Korrektur 2026-10-07:* hier standen **3** offene
Zeilen (P9-11, P9-13/V150, P9-94). **P9-11 und P9-94 sind seit dem 2026-10-07 ✅** — der
`nmap`-Gegenlauf von außen ist gelaufen (Mini-Plan §5, vier Läufe plus ein Kontrolllauf, Grenze in der
P9-11-Zeile). *Am selben Tag:* **P9-6** ⚠️ → ✅ (ROADMAP unter dem Cap, Oversize-Fix). Die **eine** offene Zeile ist P9-13/V150, das zweite Claude-Konto. **Kein ⬜ ist offene Code-Arbeit** — und
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
> **Verbatim verschoben** nach `ABNAHME_MATRIX_STEPS.md` (`scripts/move_sections.py`) — dort unter derselben Überschrift.

## Step A — Echte Domain über einen eigenen VPS (P9-10 … P9-15)
> **Verbatim verschoben** nach `ABNAHME_MATRIX_STEPS.md` (`scripts/move_sections.py`) — dort unter derselben Überschrift.

## Step B — `tailscaled-watchdog.service` (P9-16 … P9-20)
> **Verbatim verschoben** nach `ABNAHME_MATRIX_STEPS.md` (`scripts/move_sections.py`) — dort unter derselben Überschrift.

## Step C — Vision-Dienst auf der RTX 3060 (P9-21 … P9-26)
> **Verbatim verschoben** nach `ABNAHME_MATRIX_STEPS.md` (`scripts/move_sections.py`) — dort unter derselben Überschrift.

## Step D — Die zwei gemeldeten Bugs (P9-27 … P9-32)
> **Verbatim verschoben** nach `ABNAHME_MATRIX_STEPS.md` (`scripts/move_sections.py`) — dort unter derselben Überschrift.

## Step E — Karte: Reload-Overload und V118 (P9-33 … P9-37)
> **Verbatim verschoben** nach `ABNAHME_MATRIX_STEPS.md` (`scripts/move_sections.py`) — dort unter derselben Überschrift.

## Step F — Schema-Fundament (P9-38 … P9-44)
> **Verbatim verschoben** nach `ABNAHME_MATRIX_STEPS.md` (`scripts/move_sections.py`) — dort unter derselben Überschrift.

## Step G — Löschen (F2) nach `_trash/` (P9-45 … P9-52)
> **Verbatim verschoben** nach `ABNAHME_MATRIX_STEPS.md` (`scripts/move_sections.py`) — dort unter derselben Überschrift.

## Step H — Abhängigkeits-Hygiene (P9-53 … P9-55)
> **Verbatim verschoben** nach `ABNAHME_MATRIX_STEPS.md` (`scripts/move_sections.py`) — dort unter derselben Überschrift.

## Phasenweit (P9-56 … P9-58) — heute gemessen
> **Verbatim verschoben** nach `ABNAHME_MATRIX_STEPS.md` (`scripts/move_sections.py`) — dort unter derselben Überschrift.

## Block doing — fünfter Eimer „In Arbeit" (P9-59 … P9-68)
> **Verbatim verschoben** nach `ABNAHME_MATRIX_BLOECKE.md` (`scripts/move_sections.py`) — dort unter derselben Überschrift.

## Block trace — Nachvollziehbarkeit (P9-69 … P9-82)
> **Verbatim verschoben** nach `ABNAHME_MATRIX_BLOECKE.md` (`scripts/move_sections.py`) — dort unter derselben Überschrift.

## Block settings — Einstellungen als Fensterkette (P9-83 … P9-95)
> **Verbatim verschoben** nach `ABNAHME_MATRIX_BLOECKE.md` (`scripts/move_sections.py`) — dort unter derselben Überschrift.

## Block settings, Nachtrag — die sieben Punkte aus der Bildsichtung (P9-96 … P9-102)
> **Verbatim verschoben** nach `ABNAHME_MATRIX_BLOECKE.md` (`scripts/move_sections.py`) — dort unter derselben Überschrift.

## Nachtrag 2026-10-06 — zweite Bildsichtung des Nikingers (P9-103 – P9-111)
> **Verbatim verschoben** nach `ABNAHME_MATRIX_BLOECKE.md` (`scripts/move_sections.py`) — dort unter derselben Überschrift.

## Dritte Bildsichtung 2026-10-06 — **gebaut** (P9-116 – P9-119; P9-112 **widerrufen**)
> **Verbatim verschoben** nach `ABNAHME_MATRIX_BLOECKE.md` (`scripts/move_sections.py`) — dort unter derselben Überschrift.

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
> **Verbatim verschoben** nach `ABNAHME_MATRIX_VERIFY.md` (`scripts/move_sections.py`) — dort unter derselben Überschrift.

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

