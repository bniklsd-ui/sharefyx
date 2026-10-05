---
status: live
purpose: Phase-9-Head — Härtungsphase (Domain, Watchdog, Vision-Dienst, Doku-Rotation, zwei Bugs, Karten-Reload, neunte P1-Contract-Öffnung, `_trash/`-Löschen), Modulstatus, aktueller Session-Handover
read-when: Arbeiten in phase9_hardening/ — zuerst lesen, zusammen mit dem neuesten Session-stopped-Block
detail: L2
up: ../CLAUDE.md
down:
  - ../docs/concepts/phase9_hardening_plan.md    # voller Plan, Locks P9-A–P9-T, Steps 0–H
  - ../docs/concepts/phase9_hardening_block_doing_plan.md  # Mini-Plan doing-Block, Locks P9-V–P9-X
  - ../docs/concepts/PHASE8_6_CLOSEOUT_HANDOVER.md  # Herkunft der P9-Punkte
  - ABNAHME_MATRIX.md                            # P9-1 – P9-82 mit Stand und Beleg + [VERIFY]-Bilanz (2026-10-03)
  - SESSIONS_ARCHIVE.md                          # ältere Session-Blöcke, newest-first
  - UPDATES_ARCHIVE.md                          # ältere `updated:`-Fäden dieses Heads, verbatim (2026-10-03, 36 von 37)
  - MODULE_STATUS_ARCHIVE.md                   # ausführliche Statusspalten der §-Modulstatus-Tabelle, verbatim (2026-10-04)
updated: 2026-10-05 (**Korrektur desselben Tages:** `d2cbec9` hatte den neuen Block *über* den alten gestellt, und `rotate_session_block.sh` behält den *letzten* — der neue lag dadurch im Archiv; jetzt verbatim zurückgetauscht, Byte-Summe gleich · **Laptop-Messung:** kein Direktweg, nur Firmen-Proxy, der Proxy setzt die neue Domain zurück — kein SNI-Filter) | 2026-10-05 (**Übergangsfenster unbefristet möglich: `LEGACY_UNTIL=open`** — der Arbeitslaptop erreicht die neue Domain hinter dem Firmen-VPN nicht (`NS_ERROR_NET_RESET`), vermutlich ein Filter gegen neu registrierte Domains; Dialog mit drei Zuständen, CSRF-Pfad byte-identisch (`date.max`), `pytest` 1217 → 1223, Probe 24/24 · **nicht deployt**, bis dahin gilt `2026-10-17`) | 2026-10-04 (**zwei von dreizehn Statuszellen der eigenen Modulstatus-Tabelle waren unsichtbarer Text — der Fund kam aus der offenen Softcap-Frage, und die Behebung zog einen zweiten mit sich: der Zahlen-Wächter hat den Marker der *zweiten* `[VERIFY]`-Lesart weggeworfen** — opencode/M3, ein Commit, **kein Produktcode-Touch**, kein Deploy, kein Service-Touch; **7 neue Tests**, Gegenproben **G1–G7 rot**, Kontrolllauf grün; **Session-Block und `updated:`-Kette rotiert**, beide per Skript und verlustfrei) · **Befund:** Zeile 28 (Step B) und Zeile 38 (Gate/Z) tragen ein **rohes ` | ` im Text der Statusspalte** ⇒ GFM gibt ihnen **vier** Zellen statt drei und legt den Rest in eine **Phantom-Spalte** ⇒ **4.097 B waren in der gerenderten Ansicht unsichtbar** (2.990 + 1.107), darunter der komplette V153-Block des Step B. In einer Textausgabe sieht eine Tabelle mit *mehr* Zellen als ihr Kopf nicht kaputt aus, sie sieht nach einer Spalte aus · **behoben verlustfrei:** Step B ` | ` → ` · `, Gate/Z wanderte der Rohstrich **aus dem Codespan heraus** (der Text war ``` 4 Fäden mit ` | updated: `-Präfix ```, ein öffnender Backtick *vor* dem Rohstrich) · **`tests/test_table_shape.py` 6/6, repo-weit:** gemessen **3.284 Tabellenzeilen, 17 Abweichungen** — 2 hier, **15 in fremden Dateien** in `KNOWN_OFFENDERS` **mit Zeilennummer**; `\|` wird nicht gezählt (17 Stellen, Konvention), ```-Fences werden übersprungen · **zweiter Fund, die Repo-Lehre zum achten Mal:** `test_acceptance_numbers.py` blieb **grün**, als V162 *(Lesart B)* von ⬜ auf ⚠️ ging — die Regel *„eine doppelt vergebene Nummer zählt einmal, mit Lesart A"* **verwirft** den Marker der zweiten Lesart, und der stand damit in **keiner** Bilanz. Ein Wächter, der die *falsche* Rechnung richtig ausführt · `SECOND_READING_MARKERS = {"V162": "⚠️", "V163": "✅"}` nagelt jede zweite Lesart namentlich fest, eine dritte fällt als neuer Schlüssel auf; **die Abnahme-Seite ist nicht betroffen** (`_abnahme_rows` zählt jede Zeile) · **V162 *(Lesart B)* ⬜ → ⚠️ mit Zitat:** *„access control rules apply to Serve just like any other service"* (<https://tailscale.com/docs/features/tailscale-serve>, validiert 20.01.2026) — für `--tcp` nennt die CLI-Referenz **kein** ACL-Verhalten in **keine** Richtung; **kein Gegenlauf möglich** (eine Widerlegung braucht einen zweiten Tailnet-Knoten mit Shell). **Die socat-Wahl ist damit nicht widerlegt, sondern gedeckt** — *„eine offene Frage darf nicht die Grundlage einer Firewall-Entscheidung sein"* · **beide Rotationen gefahren, und das Ergebnis ist die Antwort auf die offene Frage:** der Head stand bei **66.223 B** (25.263 B über dem Softcap; Kette 11.702 · Modulstatus 29.579 · Backlog 5.975 · Block+Nachträge 17.778 B), nach Session-Block-Rotation (17.780 B verbatim ins `SESSIONS_ARCHIVE.md`) **59.354 B** und nach Kettenrotation (6 von 7 Fäden, `rotate_index_updates.sh` mit Zieldatei-Argument) **49.033 B** ⇒ **mit neuem Block und neuem Faden ≈ 55 KB, rund 14 KB über dem Softcap** (die exakte Zahl in der INDEX-Zeile; meine zwischenzeitliche Projektion „43 KB" war eine **Annahme über die eigene Blockgröße** — 4 KB angesetzt, 10,9 KB geschrieben, die Rotationsarithmetik selbst ging auf das Byte) — **die Blockschnittzahl ist damit gegenstandslos**, K=1 ist die Konvention, und selbst K=1 passt nicht, weil nicht die *Anzahl* der Blöcke das Problem ist, sondern die Breite einer Tabelle: **29.579 B in 13 Zeilen, davon 14.057 B in drei** (A 4.915 · Gate/Z 5.092 · B 4.050). Der letzte Hebel ist das Kürzen der Modulstatus-Tabelle in ein L3-Archiv (verbatim, Roundtrip, am 2026-10-02 an zwei Stellen bewährt) — **gemessen bereit, nicht getan, weil der Inhalt deine Entscheidung ist** · **vier eigene Fehler vor dem Commit behoben**, zwei davon mit der Lehre des Abends: ein Ausnahmelisten-Pfad, den es nicht gibt (der Prüfer meldete dadurch **rot statt grün**, richtig so) · `ROADMAP.md` zweimal als Dict-Schlüssel (der zweite still eine leere Ausnahme) · `hidden_bytes()` summierte die Trenner mit (Kennzahl 2 zu hoch) · die Reparatur-Gegenprobe suchte im **ganzen** Head und traf den Session-Block, der die kaputte Form wörtlich zitiert — **ein Wächter, der das Richtige an der falschen Stelle prüft, ist derselbe Fehler eine Ebene tiefer** · `pytest` **1209 → 1217**, Baseline **1209** vorab gemessen (der gestrige Block nennt 1203, die sechs Differenz sind `test_prepend_chain.py` — abgeglichen statt geglaubt), `ui_budget` 5/5, `doc_health` 0 | 2026-10-03 (**der letzte Handgriff im Rotations-Workflow ist abgeschafft: `scripts/prepend_updated_chain.sh` stellt einen Faden an den Kettenanfang, mit sechs Gegenproben und 6 Tests — nach fünfmal derselben Fehlerklasse an einem Tag, darunter einmal NACH der geschriebenen Diagnose**) · **Befund, der zum Werkzeug führte:** das Rotieren der Kette war maschinell, das **Voranstellen** nicht; beim Kopieren der alten Zeile als Vorlage wanderte das `updated:`-Präfix mit hinein (3×) oder ` | ` wurde zu ` · ` (2×) — für `rotate_index_updates.sh` beides unsichtbar · **das Skript verweigert beide Formen, statt sie zu reparieren**, und prüft den Werkzeugvertrag am echten Ergebnis (jeder Faden beginnt mit ` | `) vor dem Schreiben · **drei eigene Fehler vor dem Commit behoben:** die Closer-Prüfung las `FM_END+1` und brach **jeden** Happy-Path ab · ohne `|| true` beendet `pipefail`+`set -e` **stumm**, wenn das Feld fehlt (dieselbe Falle steht kommentiert in `rotate_index_updates.sh`) · meine Test-Fixtures: der `THREAD` war selbst ein Zwei-Faden-String und die ` · `-Gegenprobe ließ das Skript **durch** · **Gegenproben:** G1 nimmt den **echten** Faden aus diesem Commit (Durchlauf, danach kein Faden blind), G2/G3 brechen ab, G4 bricht **mit** Meldung ab, G5 (zwei Fäden, ` | `) läuft durch | ältere Einträge: phase9_hardening/UPDATES_ARCHIVE.md
---

# Phase 9 — Härtung

Voller Plan: `docs/concepts/phase9_hardening_plan.md`. Diese Datei trägt nur Modulstatus und
den aktuellen Session-Block; die Entscheidungen (P9-A–P9-T) und Step-Details stehen im Plan.

## Modulstatus

| Step | Inhalt | Status |
|---|---|---|
| 0 | Verifikations-Durchlauf, Doku-Fundament (Phasenverzeichnis, INDEX-Rotation, vier Defekte, `doc_health.py`, Baseline) | ✅ (Details im L3-Archiv) · Herleitung im L3-Archiv |
| A | Echte Domain über eigenen VPS | 🟡 **A7a + A7 ✅ 2026-10-03; A8 für Konto *niklas* ✅** — P9-10b ✅ · P9-12 ✅ · P9-14 ✅ · **P9-13/V150 ⬜ zurückgestellt, wandert nach P10, ist kein Blocker** (Nikinger 2026-10-04: ein Schritt, der nur ein Konto braucht, ist ein Termin, kein Blocker; Plan §0.1a) · **P9-15 ⬜ = Arbeit der nächsten Session** (drei Läufe `/api/v1/overview` mit echter UI-Session). Übergangsfenster **unbefristet** gebaut (`LEGACY_UNTIL=open`, Nikinger 2026-10-05, Firmen-VPN erreicht die neue Domain nicht). Bis zum Deploy und `install_units.sh` gilt weiter `2026-10-17` · Herleitung im L3-Archiv |
| B | `tailscaled-watchdog.service` | ✅ **abgeschlossen 2026-10-01**, live; P9-16–P9-20 ✅, V152/V153 ✅. `socat` 1.8.0.0 + Unit laufen unter voller Härtung, `RuntimeDirectoryPreserve=yes` (Befund 7) und Systempfad (Befund `__REPO_ROOT__`) behoben · V153: `sudoers` unbaubar, polkit greift · Herleitung im L3-Archiv |
| C | Vision-Dienst auf der RTX 3060 | ✅ **abgeschlossen** (2026-09-26): GPU-Inferenz reboot-fest + C8 (`ollama` auf der VM `inactive`) · P9-21/-23/-26 ✅ · **P9-22 deferred** (Nikinger 2026-09-26, architektonisch belegt statt extern getestet) → Revisit Step Z oder P10 · Herleitung im L3-Archiv |
| D | Zwei gemeldete Bugs (ESC/Vollbild, Drop-Ziel Space-Wurzel) | 🟡 **D2 am Browser belegt 2026-10-03** (P9-28/-29/-30 ✅, Probe **16/16**); **D1 bewusst zurückgestellt** (Nikinger 2026-09-23) · **P9-27 ⬜** und bleibt es: natives macOS-Vollbild ist nicht automatisierbar, der `fullscreenElement`-Guard ist dafür ein No-op · Herleitung im L3-Archiv |
| E | Karte: Reload-Overload, V118 | ✅ **abgeschlossen** (2026-09-28): kein zweiter `/graph`-Abruf, bekannte Knoten behalten `x`/`y`, `force` nur am Refresh-Knopf · P9-33/-34/-35 ✅ · V118 beantwortet · die Design-Frage P9-36 („eine oder zwei Linien") liegt beim Nikinger · Herleitung im L3-Archiv |
| F | Schema-Fundament (neunte P1-Contract-Öffnung: `doing`/`assignee`) | 🟡 **code-complete 2026-09-30, live seit 2026-10-02** (`v3.1.0`) · P9-43 ✅ (≤ 1,05 s für 197 Items) · **der `doing`-Bereich ist seit 2026-10-02 geschlossen** (Lock P9-V) ⇒ **P9-P ist datiert eingeengt, nicht erledigt**: die prominente Darstellung bleibt P10 · P9-U (Space-Name, ohne Validierung) und P9-V stehen im Plan · Herleitung im L3-Archiv |
| G | Löschen (F2) nach `_trash/` | 🟡 **code-complete 2026-09-30, deployt 2026-10-02** (`v3.1.0`); **Live-Löschung noch nicht beobachtet** ⇒ V162 *(Lesart A)* ⬜ · der Lösch-Ort aus Plan §9.3 war unbaubar, Nikinger entschied `DATA_ROOT/._trash/<space>/` mit **null** P1-Änderungen · Herleitung im L3-Archiv |
| H | Abhängigkeits-Hygiene | 🟡 **code-complete 2026-09-30** · `fastmcp` **exakt** auf `3.4.7` gepinnt (P3-D/P4-R waren seit 2026-08 beschlossen und nie umgesetzt) · V163 ✅ (inert) · P9-55 ⚠️ in der Form (`==3.4.7` statt Range, Nikinger 2026-09-30) · **benannt, nicht gebaut:** das transitive `mcp` bleibt ungepinnt (P9-Backlog-Kandidat) · Herleitung im L3-Archiv |
| doing | Fünfter Eimer „In Arbeit" (Lock **P9-V**, Kandidat (a)) — Voraussetzung für den Deploy `v3.1.0` | ✅ **live seit 2026-10-02** (`v3.1.0`, Gate 9/9) · Locks P9-V/W/X · 6 Tests, Gegenlauf 7 rot, Browser 11/11 · Release-Commit `v3.1.1` **2026-10-03** · Herleitung im L3-Archiv |
| trace | Nachvollziehbarkeit: `assignee` sichtbar (UI + MCP, vom Client gefüllt, P9-Z) + `updated_by` + Git-Autor (P9-AA–AC); **zehnte P1-Contract-Öffnung** | 🟡 **code-complete 2026-10-02, seit 2026-10-03 live** (`v3.1.1`, Release `20261003T205843`, Gate 9/9) · Locks P9-Y–AD · **zehnte P1-Contract-Öffnung ohne Index-Schema-Sprung** ⇒ beim Deploy **kein** Neuaufbau (am Journal bestätigt) · 24 Tests, Browser 8/8 mit Zwei-Principalen-Instanz · Herleitung im L3-Archiv |
| E (Extra) | **Buttons ans Schema** (B17): die Knöpfe mit eigenen Flächen auf die Standard-Tokens `--btn-std-*` umstellen | ✅ **gebaut 2026-10-02 (B17), seit 2026-10-03 live** · die Backlog-Liste war an zwei Stellen falsch (15 statt 1 Knopf auf der alten Flächenfamilie) · `.btn.action--caution` trägt jetzt **exakt** die Standardfläche, nur die Beschriftung ist rot · Kontrast **4,38:1** bleibt unter WCAG-AA — **Design-Entscheidung, deine** · Herleitung im L3-Archiv |
| Gate/Z | Abnahme, Closeout | 🟡 **beide Doku-Hälften erledigt** (2026-10-02) · `ABNAHME_MATRIX.md` ist der **eine** Ort der Abnahme- und `[VERIFY]`-Bilanz, nicht diese Zeile · **[2026-10-04] beide Rotationen gefahren** (Block 17.780 B verbatim, Kette 6 von 7 Fäden) und diese Tabelle ins L3-Archiv gezogen ⇒ **der Head ist unter dem 40-KiB-Softcap** · **offen:** zweites Claude-Konto (P9-13/V150) · P9-15 ⬜ · Übersichtsgrafik §12.4 · Phase auf ✅ · Herleitung im L3-Archiv |

## Backlog (bewusst zurückgestellt, kein Phasen-Blocker)

- **B17 — ✅ GESCHLOSSEN am 2026-10-02** (war: „potentieller Extra-Schritt", in der Modulstatus-Tabelle
  als „E (Extra)" geführt). **Alle Knöpfe tragen jetzt eine Fläche aus einem Schema, und die zwei
  verbleibenden Ausnahmen sind je eine Klasse mit eigener Bedeutung.** Die Details, die Messungen und
  der Gegenlauf stehen in der Modulstatus-Zeile und im Session-Block 2026-10-02; hier bleiben die
  drei Punkte, die ein späterer Leser sonst falsch wüsste:
  1. **Die Liste dieses Eintrags war an zwei Stellen falsch** — sie nannte 15 Knöpfe und
     „`.btn.action--caution` (2 Knöpfe)". Richtig sind **1 Knopf** auf der alten Familie
     (`#archive-button`; der zweite Träger `#logout-button` ist ein `.rail__action` und hat keine
     Fläche) und **13** auf `--accent-face-*` (`.btn-primary`). Die 13 sind **kein Reststand**:
     Hauptaktion ist eine dokumentierte Ausnahme der Nikinger-Entscheidung vom 2026-10-01.
  2. **`.btn.action--caution` trägt exakt die Standardfläche**, nur die Beschriftung ist rot
     (`--caution`). Das ist wortgleich die Konvention-v3-Zeile „Standard-Knopfplastik, aber
     `color: var(--caution)`; **keine** gefüllte rote Fläche" — und die Konvention war zwischen
     dem 2026-10-01 und dem 2026-10-02 **nicht eingehalten** (die alte graue Fläche ist heller als
     die Standardfläche). Beide Stellen in `phase8_ui_graph/CLAUDE.md` sind datiert korrigiert.
  3. **Benannt, nicht entschieden:** der Kontrast der Vorsicht-Beschriftung liegt bei
     **4,38:1** (vorher 3,36:1 auf der grauen Plastik) — **unter** WCAG-AA 4,5:1 für normalgroßen
     Text (14 px/500 ist kein „large text"). Besser als vorher ist das keine Erfüllung. Die
     Kandidaten (hellere Vorschriftfarbe wie `--btn-std-line` als Text, oder die Kategorie doch an
     eine 1-px-Kante hängen) sind Design-Entscheidungen und gehören dem Nikinger.
  **Was ausdrücklich nicht gebaut wurde:** die eigene rot getönte Flächenfamilie `--caution-std-*`
  — sie *wäre* die gefüllte rote Fläche, die die Konvention ausschließt, und fiel deshalb.

- **P9-15 / V151 gemessen am 2026-10-03 — und der Befund ist größer als die Abnahmezeile:**
  **`/api/v1/overview` kostet live ~3,1 s**, davon **~2,4 s reine Serverarbeit.** Die
  Aufschlüsselung steht in `ABNAHME_MATRIX.md` (P9-15, V151) und ist in einem Satz hier: **`_overview()` wiederholt das ganze 6-Durchgänge-Muster pro sichtbarem Space** — ein `store.search()` pro Bucket plus einer für die Liste, und jeder Durchgang liest **jede** indizierte Datei neu (`limit` ist egal, ~100 ms). Bei 4 sichtbaren Spaces sind das **24 vollständige Durchgänge** über 197 Items; die Kosten wachsen **linear mit den Spaces**, nicht mit den Items. **Gemessen, nicht geraten:** in-process in der echten Form 2.388–2.407 ms in `/tmp` gegen 2.417–2.426 ms auf der VM-Platte (die Platte ist es also **nicht**), plus ein in-process Instrument (`ui_budget.py`, 1 Space / 220 Items), das den echten Endpunkt **3,3×** zu niedrig misst — 713 ms heute gegen 372,9 ms am 2026-09-13 auf **identischem** Instrument.
  **Nikinger-Entscheidung 2026-10-03: Inhalt einer neuen Phase, jetzt nicht weiter verfolgen.** Kein Code-Touch in P9, kein Backlog-Posten in dieser Phase. Zwei Dinge, die die neue Phase nicht neu messen muss: die **Ursache ist identifiziert** (die Per-Space-Schleife in `api.py`) und die **Messlatte ist falsch** (der 372,9-ms-Wert kommt aus einem anderen Instrument — Plan §3.3 erinnert seine Provenienz falsch). · **V151 selbst ist ✅**: der VPS-Weg kostet 76–113 ms auf ~3,1 s, also 2,4–3,6 % — *nicht relevant*. Der Weg war nie das Problem.
- **D1 — ESC im Vollbild schließt zusätzlich das Item.** Diagnose geklärt (macOS Safari,
  natives Vollbild über den grünen Knopf), Fix nicht — der gebaute
  `document.fullscreenElement`-Guard (Session 2026-09-23) sieht diesen Fall nicht, weil die
  Web-Fullscreen-API dort per Spezifikation nicht greift. **Nikinger-Entscheidung 2026-09-23:**
  zurückstellen, angehen, sobald genug Zeit da ist — kein aktiver Blocker für den Rest von P9.
  Ansatzpunkte für den nächsten Anlauf stehen im Session-Block 2026-09-23 unten (gegen echtes
  Safari messen, keine Heuristik raten).
- **Derselbe Vormittag, separater Vorfall, jetzt geschlossen: `mcp-proxy.anthropic.com`
  (Anthropics eigenes Connector-Relay für claude.ai) lieferte ~19 Minuten lang durchgehend
  Cloudflare-502 auf jeden `Sharefyx`-Connector-Call** (`list_spaces`, viermal probiert,
  09:35–09:41 CEST), danach ohne jede Aktion von unserer Seite wieder normal (09:41→später:
  `list_spaces` liefert sauber 4 Spaces). **Gemessen, nicht vermutet, dass es nicht an
  CGNAT/Mobilfunk (RUT X50) oder an der sharefyx-VM lag:** `journalctl -u sharefyx-mcp`
  zeigt für alle vier 502-Zeitpunkte **keinen einzigen eingehenden Request** — kein POST auf
  `/mcp`, nicht mal ein 4xx —, während `GET /health` über denselben eigenen Funnel-Endpoint
  in derselben Minute jedes Mal sofort 200 lieferte und ein `POST /mcp/` um 09:22 (vor dem
  Fenster) sauber 200 loggte. Die 502 kann also nicht vom eigenen Netz/Tunnel kommen, wenn der
  Request dort nie ankommt. Zwei Nikinger-Restarts (`sharefyx-mcp.service` + Funnel) während
  des Fensters haben nichts geändert — konsistent mit „Fehler liegt vor der eigenen
  Infrastruktur". `status.claude.com` zeigte zeitgleich keinen Incident, aber vier unabhängige
  `anthropics/claude-code`-GitHub-Issues (#48277, #48291, #94356, #69426) beschreiben exakt
  dasselbe Muster — wiederkehrende, nicht auf der Statusseite gelistete 502 an genau diesem
  Relay. **Eingestuft als: unbekannter, vorübergehender Ausfall bei Anthropic
  (`mcp-proxy.anthropic.com`), explizit nicht auf CGNAT/Mobilfunk-Setup oder die sharefyx-VM
  zurückzuführen** — Nikinger-Anordnung 2026-09-24, so dokumentieren und nicht weiter
  untersuchen.

## Session stopped — 2026-10-05 (dreiundzwanzigster Block: **die alte Adresse darf unbefristet schreiben — der Arbeitslaptop erreicht die neue nicht**; Produktcode-Touch im Übergangsfenster, **kein Deploy, kein Service-Touch**)

**Ergebnis.** Neu ist `SPACE_UI_LEGACY_UNTIL=open` (über `local.env`: `LEGACY_UNTIL=open`): die alte
Funnel-Adresse schreibt damit unbefristet. Der Warndialog dort kennt jetzt **drei** Zustände:

| Zustand | Titel | Knopf |
|---|---|---|
| unbefristet | „Es gibt eine neue Adresse" (*„… funktioniert bis auf Weiteres vollständig …"*) | „Hier weiterarbeiten" |
| befristet | „Diese Adresse wird abgeschaltet" | „Trotzdem hier bleiben" |
| abgelaufen | „Diese Adresse ist nur noch lesbar" | „Hier nur lesen" |

**Live ist noch nichts davon.** Solange der Nikinger nicht deployt, gilt weiter
`LEGACY_UNTIL=2026-10-17`. Das Fenster schließt dann am 2026-10-18.

**Anlass (Nikinger, 2026-10-05).** Der Arbeitslaptop erreicht `https://sharefyx.eurofyx.com/ui/`
nicht. Er läuft unter Windows mit Firefox 158, hinter dem Firmen-VPN genua genuconnect, das sich nicht
abschalten lässt. Die Fehlermeldung ist `NS_ERROR_NET_RESET` mit 0 B übertragen. Die alte Adresse
geht von dort, die neue geht vom MacBook.
**Von der Heim-VM gemessen:**
- A `217.160.128.146` über 1.1.1.1 und 8.8.8.8, **kein** AAAA
- TLSv1.3, Let's-Encrypt-Zertifikat `YE1`, `ssl_verify_result=0`
- `GET /ui/` → `303` über HTTP/2 und HTTP/1.1

**Vermutung, nicht belegt:** ein SNI-basierter Filter im Firmennetz gegen neu registrierte Domains.
`eurofyx.com` ist registriert seit 2026-10-01; `*.ts.net` ist dagegen kategorisiert. Der Caddy-Log auf
dem VPS wurde **nicht** gelesen, weil der VPS-Hostkey nicht in `known_hosts` steht und ich ihn nicht
ungefragt annehme.

**Diagnose für den Arbeitslaptop** (PowerShell, `curl.exe`, **nicht** `curl` — das ist dort
`Invoke-WebRequest`):

```powershell
Resolve-DnsName sharefyx.eurofyx.com                      # erwartet 217.160.128.146
Test-NetConnection 217.160.128.146 -Port 443              # TcpTestSucceeded?
curl.exe -v --resolve sharefyx.eurofyx.com:443:217.160.128.146 https://sharefyx.eurofyx.com/health
curl.exe -vk --resolve example.org:443:217.160.128.146 https://example.org/   # gleiche IP, anderer SNI
netsh winhttp show proxy
curl.exe -v https://www.google.com 2>&1 | findstr /i "issuer"   # Firmen-CA = TLS-Inspektion
```

Lesart:

| Befund | Bedeutung |
|---|---|
| Probe 3 mit Reset, Probe 4 mit TLS-Alert von Caddy | Filter auf den Hostnamen (SNI) |
| beide mit Reset | IP oder Hoster gesperrt |
| Resolve liefert eine andere IP | Firmen-DNS lenkt die Domain um |

Parallel kann der Nikinger auf dem VPS `journalctl -u caddy -f` laufen lassen, während der Laptop
probt. Erscheint **keine** Zeile, sitzt die Sperre davor. **Lösung:** IT-Ticket, Domain freigeben bzw.
kategorisieren lassen. **Nicht** umgehen.

**[2026-10-05, später — Laptop-Messung; die Vermutung oben ist korrigiert]** Der Laptop hat **keinen
direkten Internetzugang**, nur einen Firmen-Proxy (Nikinger). Gemessen hat er:
- DNS liefert `217.160.128.146`, also korrekt
- `Test-NetConnection :443` → Timeout
- beide `curl.exe --resolve`-Proben → Timeout nach 21 s, **mit und ohne** richtigen SNI

Das ist **kein SNI-Filter beim Direktweg**. Der Direktweg existiert gar nicht. Firefox läuft über den
Proxy, und **der Proxy** setzt die Verbindung zur neuen Domain zurück (`NS_ERROR_NET_RESET`). Die
alte `*.ts.net`-Adresse lässt er durch. Die Diagnose-Tabelle oben ist für diesen Laptop
gegenstandslos. **Lösung:** IT-Ticket, den Host auf der Proxy-Freigabeliste. Mit
`Invoke-WebRequest … -UseBasicParsing -ProxyUseDefaultCredentials` sieht man die Antwort des Proxys,
ohne seine Adresse zu nennen.

**Warum so gebaut.**
- **Wort `open` statt Datum 2099.** Ein Fantasiedatum hätte im Dialog gestanden, als
  Abschalttermin, den niemand beschlossen hat.
- **Fail-closed bleibt erhalten.** Nur das exakte Wort öffnet das Fenster. Leer oder halb gesetzt ist
  weiter ein Startfehler; `OPEN` wird abgelehnt, getestet.
- **Intern `date.max`.** Damit bleiben `legacy_writable()` und `origin_allowed()` **byte-identisch**:
  die CSRF-Prüfung ist nicht angefasst. `None` im Dataclass als „offen" zu deuten, hätte genau diesen
  Pfad fail-open gemacht.
- **`/api/v1/meta` meldet `until: null` bei `writable: true`.** Der Dialog liest das als
  „unbefristet", deshalb erscheint nie „31.12.9999".
- **Tabu-Liste §0.3 nicht berührt.** Geändert sind `mcpserver/config.py` (nicht `permissions.py` oder
  `server.py`), `webui/api.py`, `app.js` und `app.html`.

**Belege.**
- `pytest` **1217 → 1223**: 6 neue Fälle in `test_legacy_window.py` (open wird geparst · `OPEN` und
  halb gesetztes `open` abgelehnt · 2030 schreibbar, fremde Origin weiter 403 · `meta` ohne Datum ·
  Verdrahtung von Titel, Text und Knopf)
- `ui_budget` 5/5 (165,5 KB)
- `node --check` grün
- Wächter (c) aus `test_acceptance_numbers.py`: die gestrichene Masse beträgt unverändert **229 B**
- Wächter (c) aus `test_acceptance_numbers.py`: die gestrichene Masse beträgt unverändert **229 B**
- **Browser-Probe `p9a_legacy_probe.py` 24/24**, jetzt mit drei Läufen gegen die Wegwerf-Instanz
  auf Port 18775, gestoppt über die PID-Datei; Bild: `docs/screenshots/p9a_legacy_unbefristet.png`,
  angesehen

**Nächster Schritt (Nikinger, vor dem 2026-10-18):**
1. `phase5_ui/scripts/deploy.sh main`
2. in `phase3_edge/local.env` `LEGACY_UNTIL=open` setzen
3. `phase3_edge/scripts/install_units.sh` ausführen
4. Dienst neu starten und `health_gate.sh` laufen lassen
5. auf der alten Adresse den Dialog „Es gibt eine neue Adresse" sehen

**Notlösung ohne Release:** nur `LEGACY_UNTIL` auf ein späteres Datum setzen und Schritte 3–4
ausführen; der Dialog nennt dann dieses Datum. **Wann zurück auf ein Datum:** erst wenn der
Arbeitslaptop die neue Adresse belegt erreicht.
