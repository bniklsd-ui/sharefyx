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
updated: 2026-10-04 (**zwei von dreizehn Statuszellen der eigenen Modulstatus-Tabelle waren unsichtbarer Text — der Fund kam aus der offenen Softcap-Frage, und die Behebung zog einen zweiten mit sich: der Zahlen-Wächter hat den Marker der *zweiten* `[VERIFY]`-Lesart weggeworfen** — opencode/M3, ein Commit, **kein Produktcode-Touch**, kein Deploy, kein Service-Touch; **7 neue Tests**, Gegenproben **G1–G7 rot**, Kontrolllauf grün; **Session-Block und `updated:`-Kette rotiert**, beide per Skript und verlustfrei) · **Befund:** Zeile 28 (Step B) und Zeile 38 (Gate/Z) tragen ein **rohes ` | ` im Text der Statusspalte** ⇒ GFM gibt ihnen **vier** Zellen statt drei und legt den Rest in eine **Phantom-Spalte** ⇒ **4.097 B waren in der gerenderten Ansicht unsichtbar** (2.990 + 1.107), darunter der komplette V153-Block des Step B. In einer Textausgabe sieht eine Tabelle mit *mehr* Zellen als ihr Kopf nicht kaputt aus, sie sieht nach einer Spalte aus · **behoben verlustfrei:** Step B ` | ` → ` · `, Gate/Z wanderte der Rohstrich **aus dem Codespan heraus** (der Text war ``` 4 Fäden mit ` | updated: `-Präfix ```, ein öffnender Backtick *vor* dem Rohstrich) · **`tests/test_table_shape.py` 6/6, repo-weit:** gemessen **3.284 Tabellenzeilen, 17 Abweichungen** — 2 hier, **15 in fremden Dateien** in `KNOWN_OFFENDERS` **mit Zeilennummer**; `\|` wird nicht gezählt (17 Stellen, Konvention), ```-Fences werden übersprungen · **zweiter Fund, die Repo-Lehre zum achten Mal:** `test_acceptance_numbers.py` blieb **grün**, als V162 *(Lesart B)* von ⬜ auf ⚠️ ging — die Regel *„eine doppelt vergebene Nummer zählt einmal, mit Lesart A"* **verwirft** den Marker der zweiten Lesart, und der stand damit in **keiner** Bilanz. Ein Wächter, der die *falsche* Rechnung richtig ausführt · `SECOND_READING_MARKERS = {"V162": "⚠️", "V163": "✅"}` nagelt jede zweite Lesart namentlich fest, eine dritte fällt als neuer Schlüssel auf; **die Abnahme-Seite ist nicht betroffen** (`_abnahme_rows` zählt jede Zeile) · **V162 *(Lesart B)* ⬜ → ⚠️ mit Zitat:** *„access control rules apply to Serve just like any other service"* (<https://tailscale.com/docs/features/tailscale-serve>, validiert 20.01.2026) — für `--tcp` nennt die CLI-Referenz **kein** ACL-Verhalten in **keine** Richtung; **kein Gegenlauf möglich** (eine Widerlegung braucht einen zweiten Tailnet-Knoten mit Shell). **Die socat-Wahl ist damit nicht widerlegt, sondern gedeckt** — *„eine offene Frage darf nicht die Grundlage einer Firewall-Entscheidung sein"* · **beide Rotationen gefahren, und das Ergebnis ist die Antwort auf die offene Frage:** der Head stand bei **66.223 B** (25.263 B über dem Softcap; Kette 11.702 · Modulstatus 29.579 · Backlog 5.975 · Block+Nachträge 17.778 B), nach Session-Block-Rotation (17.780 B verbatim ins `SESSIONS_ARCHIVE.md`) **59.354 B** und nach Kettenrotation (6 von 7 Fäden, `rotate_index_updates.sh` mit Zieldatei-Argument) **49.033 B** ⇒ **mit neuem Block und neuem Faden ≈ 55 KB, rund 14 KB über dem Softcap** (die exakte Zahl in der INDEX-Zeile; meine zwischenzeitliche Projektion „43 KB" war eine **Annahme über die eigene Blockgröße** — 4 KB angesetzt, 10,9 KB geschrieben, die Rotationsarithmetik selbst ging auf das Byte) — **die Blockschnittzahl ist damit gegenstandslos**, K=1 ist die Konvention, und selbst K=1 passt nicht, weil nicht die *Anzahl* der Blöcke das Problem ist, sondern die Breite einer Tabelle: **29.579 B in 13 Zeilen, davon 14.057 B in drei** (A 4.915 · Gate/Z 5.092 · B 4.050). Der letzte Hebel ist das Kürzen der Modulstatus-Tabelle in ein L3-Archiv (verbatim, Roundtrip, am 2026-10-02 an zwei Stellen bewährt) — **gemessen bereit, nicht getan, weil der Inhalt deine Entscheidung ist** · **vier eigene Fehler vor dem Commit behoben**, zwei davon mit der Lehre des Abends: ein Ausnahmelisten-Pfad, den es nicht gibt (der Prüfer meldete dadurch **rot statt grün**, richtig so) · `ROADMAP.md` zweimal als Dict-Schlüssel (der zweite still eine leere Ausnahme) · `hidden_bytes()` summierte die Trenner mit (Kennzahl 2 zu hoch) · die Reparatur-Gegenprobe suchte im **ganzen** Head und traf den Session-Block, der die kaputte Form wörtlich zitiert — **ein Wächter, der das Richtige an der falschen Stelle prüft, ist derselbe Fehler eine Ebene tiefer** · `pytest` **1209 → 1217**, Baseline **1209** vorab gemessen (der gestrige Block nennt 1203, die sechs Differenz sind `test_prepend_chain.py` — abgeglichen statt geglaubt), `ui_budget` 5/5, `doc_health` 0 | 2026-10-03 (**der letzte Handgriff im Rotations-Workflow ist abgeschafft: `scripts/prepend_updated_chain.sh` stellt einen Faden an den Kettenanfang, mit sechs Gegenproben und 6 Tests — nach fünfmal derselben Fehlerklasse an einem Tag, darunter einmal NACH der geschriebenen Diagnose**) · **Befund, der zum Werkzeug führte:** das Rotieren der Kette war maschinell, das **Voranstellen** nicht; beim Kopieren der alten Zeile als Vorlage wanderte das `updated:`-Präfix mit hinein (3×) oder ` | ` wurde zu ` · ` (2×) — für `rotate_index_updates.sh` beides unsichtbar · **das Skript verweigert beide Formen, statt sie zu reparieren**, und prüft den Werkzeugvertrag am echten Ergebnis (jeder Faden beginnt mit ` | `) vor dem Schreiben · **drei eigene Fehler vor dem Commit behoben:** die Closer-Prüfung las `FM_END+1` und brach **jeden** Happy-Path ab · ohne `|| true` beendet `pipefail`+`set -e` **stumm**, wenn das Feld fehlt (dieselbe Falle steht kommentiert in `rotate_index_updates.sh`) · meine Test-Fixtures: der `THREAD` war selbst ein Zwei-Faden-String und die ` · `-Gegenprobe ließ das Skript **durch** · **Gegenproben:** G1 nimmt den **echten** Faden aus diesem Commit (Durchlauf, danach kein Faden blind), G2/G3 brechen ab, G4 bricht **mit** Meldung ab, G5 (zwei Fäden, ` | `) läuft durch | ältere Einträge: phase9_hardening/UPDATES_ARCHIVE.md
---

# Phase 9 — Härtung

Voller Plan: `docs/concepts/phase9_hardening_plan.md`. Diese Datei trägt nur Modulstatus und
den aktuellen Session-Block; die Entscheidungen (P9-A–P9-T) und Step-Details stehen im Plan.

## Modulstatus

| Step | Inhalt | Status |
|---|---|---|
| 0 | Verifikations-Durchlauf, Doku-Fundament (Phasenverzeichnis, INDEX-Rotation, vier Defekte, `doc_health.py`, Baseline) | ✅ (Details im L3-Archiv) · Herleitung im L3-Archiv |
| A | Echte Domain über eigenen VPS | 🟡 **A7a + A7 ✅ 2026-10-03; A8 für Konto *niklas* ✅** — P9-10b ✅ · P9-12 ✅ · P9-14 ✅ · **P9-13/V150 ⬜ zurückgestellt, wandert nach P10, ist kein Blocker** (Nikinger 2026-10-04: ein Schritt, der nur ein Konto braucht, ist ein Termin, kein Blocker; Plan §0.1a) · **P9-15 ⬜ = Arbeit der nächsten Session** (drei Läufe `/api/v1/overview` mit echter UI-Session). Übergangsfenster schließt **2026-10-18** · Herleitung im L3-Archiv |
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

## Session stopped — 2026-10-04 (zweiundzwanzigster Block: **zwei von dreizehn Statuszellen der eigenen Modulstatus-Tabelle waren unsichtbarer Text** — der Fund kam aus der offenen Softcap-Frage, und die Behebung zog einen zweiten mit sich: der Zahlen-Wächter hat den Marker der *zweiten* `[VERIFY]`-Lesart weggeworfen; dazu V162 (Lesart B) von ⬜ auf ⚠️ mit Zitat. **Kein Produktcode-Touch, kein Deploy, kein Service-Touch.** Heute rotiert: der Block vom 2026-10-03 und die `updated:`-Kette, beide per Skript, beide verlustfrei)

**Die offene Frage war „wie viele Session-Blöcke bleiben im Head?" — und die Antwort hat einen
Fehler gefunden, den niemand gesucht hat.** Beim Zählen der Zeilen und Bytes (die Entschiedenheit
lag bei dir, die Zahlen nicht) fiel auf: die §-Modulstatus-Tabelle hat **13 Datenzeilen**, und
**zwei davon sind kaputtes Markdown.** In Zeile 28 (Step B) und Zeile 38 (Gate/Z) steht ein
**rohes ` | ` im Text der Statusspalte**. GFM trennt Zellen an `|`, also haben diese beiden Zeilen
**vier** Zellen statt drei, und der Renderer legt alles hinter dem Rohstrich in eine
**Phantom-Spalte**, die die Tabelle nicht hat.

**Gemessen, nicht geschätzt: 4.097 B dieses Heads waren in der gerenderten Ansicht unsichtbar** —
2.990 B in Step B, 1.107 B in Gate/Z. Darunter der **komplette V153-Block** des Step B (polkit
statt `sudoers`, `NoNewPrivileges`, die JS-Regel, die Probe) und der Schluss des Gate-Z-Eintrags.
Der Text war da, per Textsuche auffindbar, in jeder Zeilenzahl enthalten — und **unsichtbar**.
Eine Tabelle mit *mehr* Zellen als ihr Kopf sieht in einer Textausgabe nicht kaputt aus, sie sieht
nach einer weiteren Spalte aus. Das ist dieselbe Fehlerklasse wie der ` · `-Trenner in der
`updated:`-Kette (`test_updated_chain.py` vom 2026-10-03) und dieselbe Lehre: **eine maschinell
gepflegte Struktur braucht einen Wächter, nicht Aufmerksamkeit — und die dritte Ausprägung
dieser Klasse in dieser Phase.**

**Behoben verlustfrei, zwei Bytesops.** In Step B ` | ` → ` · ` (der Trenner war nie Inhalt; das
ist der Trenner, den dieselbe Datei 200 B weiter unten benutzt). In Gate/Z wanderte der Rohstrich
**aus dem Codespan heraus** — der Text war `` 4 Fäden mit ` | updated: `-Präfix ``, also ein
öffnender Backtick *vor* dem Rohstrich und der eigentliche Codespan danach; daraus ist
`` 4 Fäden mit `updated: `-Präfix `` geworden. **Null Zeichen verloren**, und ein Test
(`test_the_two_repaired_rows_kept_their_text`) verhindert, dass eine künftige Kürzung die
Behebung für eine Auslassung hält. Er prüft **nur** die Tabelle: die kaputte Form steht im
Session-Block und in der `updated:`-Kette weiterhin *wörtlich*, weil beide den Defekt beschreiben —
als Treffer gemeldet wäre das ein Fehlalarm.

**Der Wächter `tests/test_table_shape.py` (6 Tests, repo-weit).** Jede Tabellenzeile muss so viele
Zellen haben wie ihre Kopfzeile. **Gemessen über den ganzen Baum: 3.284 Tabellenzeilen, 17
Abweichungen** — 2 hier behoben, **15 in fremden Dateien** (abgeschlossene Phasen, `ROADMAP.md`,
zwei 📕-Snapshots, der P9-Plan, das Step-A-Runbook), alle in `KNOWN_OFFENDERS` **mit Zeilennummer**,
damit die Liste nicht wachsen kann, ohne dass es auffällt. Zwei Details, ohne die der Wächter
falsch-grün wäre: `\|` ist die **korrekte** Form und wird nicht gezählt (das Repo benutzt sie an 17
Stellen — `initial\|reset`, `Image \| str` — sie ist Konvention), und Zeilen in einem ```-Fence
sind Prosa über Masken (`awk '/^\| P8-/'` in einem 📕-Plan) und werden übersprungen. **Gegenproben
G1–G4 rot** (Rohstrich zurück in Step B · neue unbekannte Datei · reparierte Fundstelle bleibt in
der Liste · Zeilennummer falsch), Kontrolllauf 6/6 grün, danach byte-identisch wiederhergestellt.

**Und der Fund, den die Behebung mit sich zog — die Repo-Lehre zum achten Mal, und diesmal mit
der Pointe, dass der Wächter die *falsche* Rechnung richtig ausführte.** Ich habe V162 *(Lesart B)*
von ⬜ auf ⚠️ gesetzt (unten begründet) und `test_acceptance_numbers.py` blieb **grün**. Grund: die
Zählregel für doppelt vergebene Nummern — *„eine Nummer zählt einmal, mit ihrer Lesart A"* — wirft
den Marker der **zweiten** Lesart **weg**, und der landet damit in **keiner** Bilanz: nicht in der
Überschrift der Matrix, nicht in `VERIFY_BALANCE`, nirgends. Ein ⚠️ oder ✅ konnte dort
**beliebig** stehen, ohne dass ein Wächter es bemerkte. Die Regel war am 2026-10-03 aus einem echten
Problem geboren (V162/V163 je zweimal vergeben, eine Übergabezahl 40 gegen 34 belegte) — und sie hat
dabei eine ganze Spalte Marker ungedeckt gelassen, ohne dass jemand die Regel ansah. **Gebaut:**
`SECOND_READING_MARKERS = {"V162": "⚠️", "V163": "✅"}` — die Arithmetik bleibt bei 34 (das ist die
aussagekräftige Übergabezahl, sie steht im Fließtext und in der Kopfzeile dieses Heads), aber
**jede zweite Lesart ist namentlich festgenagelt**, und eine **dritte** fällt als neuer Schlüssel
auf, weil der Test die Menge vergleicht. **Gegenproben G5–G7 rot**: G5 ist dieselbe Änderung, die
vor der Reparatur grün blieb; G6 eine erfundene dritte Lesart; G7 eine falsch festgenagelte
Konstante. **Das ist übrigens die Abnahme-Seite nicht betroffen** — `_abnahme_rows` zählt **jede**
Zeile, dort gibt es keine Verwerfungsregel. Der Fehler war auf eine Seite.

**V162 *(Lesart B)* von ⬜ auf ⚠️, mit Zitat und mit der Grenze des Zitats.** Die Tailscale-Doku sagt
wörtlich: *„access control rules apply to Serve just like any other service … those rules will also
apply to the services you're sharing with Serve"* (Tailscale Serve, *Get started with Serve*,
<https://tailscale.com/docs/features/tailscale-serve>, last validated 20.01.2026). Die
**CLI-Referenz** zu `--tcp` / `--tls-terminated-tcp`
(<https://tailscale.com/docs/reference/tailscale-cli/serve>, last validated 26.01.2026) nennt **kein**
ACL-Verhalten — in **keine** Richtung. Grundsatz: *„By default, all connections between devices in
your tailnet are denied unless explicitly permitted through your tailnet policy file"*
(<https://tailscale.com/docs/features/access-control>). **Warum kein Gegenlauf möglich ist:** eine
Widerlegung braucht eine *abgelehnte* Verbindung von einem zweiten Tailnet-Knoten, und auf dieser VM
kann ich auf keinem fremden Knoten Kommandos ausführen (`tailscale status` listet sieben, Shell-
Zugang ist deine Sache). **Konsequenz für die getroffene Entscheidung: keine** — `socat` ist damit
**nicht** widerlegt, sondern im Gegenteil gedeckt: die elegante Alternative ist nur für den
HTTP-Modus belegt, und *„eine offene Frage darf nicht die Grundlage einer Firewall-Entscheidung
sein"* (Runbook §3, Befund 6) war genau richtig. ⚠️ nach der Statusregel der Matrix, weil das
Kriterium in anderer Form beantwortet ist als gefragt; **bleibt ⬜ für eine echte Messung**.

**Eine eigene Rechenfehler-Vorschrift, die derselbe Block sich selbst auferlegt:** die Zeile oben
sagte zuerst „rund 2 KB über dem Softcap". Das war **meine** Prognose, und sie war falsch —
gerechnet hatte ich mit einem 4-KB-Block und geschrieben habe ich 10,9 KB. Die **Rotationsarithmetik
selbst ging auf das Byte** (17.780 B verschoben, 66.223 → 59.354 → 49.033 B), der Fehler steckt
ausschließlich in meiner Annahme über die eigene Ausführlichkeit. **Benannt, weil es dieselbe
Klasse ist wie die drei falschen Bilanzen vom 2026-10-03:** eine Zahl, die ich nicht gemessen habe,
aber wie eine behandelt habe.

**Was heute rotiert und was das kostet — beide Zahlen gemessen, keine geschätzt.** Der Head stand
bei **66.223 B**, also **25.263 B über dem 40-KiB-Softcap**, verteilt auf `updated:`-Kette
**11.702 B** · § Modulstatus **29.579 B** *(Stand vor dem heutigen Nachtrag, der eingerechnet sind es 30.564 B)* · § Backlog **5.975 B** · § Session-Block mit drei
Nachträgen **17.778 B**. Rotiert wird heute **beides**, was die Konvention vorschreibt und was
gestern offen blieb: der Block vom **2026-10-03** (Hauptblock + 3 Nachträge, 213 Zeilen) **verbatim**
nach `SESSIONS_ARCHIVE.md` per `scripts/rotate_session_block.sh`, und die **`updated:`-Kette** nach
`UPDATES_ARCHIVE.md` per `scripts/rotate_index_updates.sh` mit Zieldatei-Argument, danach der neue
Faden per `scripts/prepend_updated_chain.sh` — **beide Skripte, keine Hand**, alle Gegenproben des
Rotations-Werkzeugs grün. **Das Ergebnis ist die Antwort auf die offene Frage, und sie ist ernüchternd:**
nach beiden Rotationen **49.033 B**, mit dem neuen Block und dem neuen Faden **≈ 54 KB — damit
rund 13 KB über dem Softcap.** (Die exakte Zahl steht in der `docs/INDEX.md`-Zeile, weil eine
Zahl, die ihre eigene Länge mitnennt, sich beim Schreiben ändert; `doc_health` prüft sie mit einem
Band von ±2 KB.) Kette und Block sind damit *beide* erledigt, und der Rest ist **allein** die
§-Modulstatus-Tabelle: **30.564 B**, davon **30.520 B in 14 Zeilen** (Kopf + 13 Datenzeilen) und allein **15.041 B in drei Zeilen** (Gate/Z 6.075 · A 4.915 · B 4.051) — (die Zahlen der Tabelle **nach** dem eigenen Nachtrag von heute: 29.579 B ⇒ **30.564 B**, davon 30.520 B in 14 Zeilen = Kopf + 13 Datenzeilen, die drei größten **15.041 B** (Gate/Z 6.075 · A 4.915 · B 4.051) — eine Zahl, die ihre eigene Länge mitnimmt, altert beim Schreiben, also nachgemessen statt gerechnet)
(A 4.915 · Gate/Z 5.092 · B 4.050). **Die Blockschnittzahl ist damit gegenstandslos** — K=1 ist die Konvention, und selbst K=1
passt nicht, weil nicht die Anzahl der Blöcke das Problem ist, sondern die Breite einer Tabelle.
**Kürzen ist damit keine Formfrage mehr, sondern die einzige noch offene Hebel**, und er ist
deiner: der Inhalt dieser Zellen steht **wortgleich** in `SESSIONS_ARCHIVE.md` (280 KB), ist also
verlustfrei in ein L3-Archiv zu ziehen — der Weg ist am 2026-10-02 an zwei anderen Stellen
gegangen (`phase1_storage/CONTRACTS_ARCHIVE.md`, `phase5_ui/ABNAHME_MATRIX_ARCHIVE.md`, beide
verbatim mit Roundtrip-Gegenprobe). **Gemessen bereit, nicht getan**, weil der Inhalt des
Archivs deine Entscheidung ist.

**Und der Hebel, den man *nicht* ziehen darf, mit seiner Zahl, weil der Block von gestern ihn
genannt hat und jetzt im Archiv liegt:** die **gestrichenen** Statusabsätze dieser Tabelle sind
**229 B** — Faktor 58 gegen die rund 13 KB, die der Softcap übersteigen. Die verbreitete Geschichte
davon war „7.467 B, und Streichen brächte den Head sicher unter den Softcap"; sie ist seit dem
2026-10-03 widerlegt und der Wächter `test_the_lever_named_against_the_head_oversize_is_the_measured_one`
prüft das in **drei** Richtungen (ein zu kleiner Hebel kann die Überschreitung nicht beseitigen ·
die lebende Masse muss die tragende sein · **der neueste Session-Block nennt die gemessene Zahl,
sonst liest der nächste Start wieder nur die alte**). Clause (c) hat mich beim Schreiben dieses
Absatzes rot gemeldet, weil mein Block die Zahl nicht nannte — der Wächter hat seinen eigenen
Zweck erfüllt, an dem Text, der ihn ablösen wollte.

**Selbstprüfung, heute gemessen, nicht aus der Doku übernommen.** `pytest` **1209 → 1217**
(Baseline **1209** vor
Beginn (der 2026-10-03-Block nennt 1203; die sechs Differenz sind `test_prepend_chain.py`, mit
dessen Commit dazugekommen — abgeglichen statt geglaubt) · `ui_budget` **5/5** · `doc_health`
**0** · Tabu-Pfade unberührt · **kein `systemctl`, kein `pkill -f`**, keine Wegwerf-Instanz, kein
Netzzugriff, kein Deploy. **Vier eigene Fehler in diesem Block, alle vor dem Commit behoben und
zwei davon mit derselben Lehre wie der Fund:** (1) die Ausnahmeliste nannte einen Pfad, den es
nicht gibt (`docs/concepts/phase6_shares/…` statt `phase6_shares/…`) — der Prüfer meldete dadurch
den Veteranen als *unbekannten* Verstoß, also **rot statt grün**, was richtig war; (2) dieselbe
Liste hatte `ROADMAP.md` zweimal als Schlüssel, der zweite war stillschweigend eine leere
Ausnahme; (3) `hidden_bytes()` summierte die **Trenner** mit, die Kennzahl war damit um 2 zu hoch
— eine Zahl, die ihre eigene Form mitzählt; (4) die Reparatur-Gegenprobe suchte den reparierten
Text in der **ganzen Datei** und traf deshalb den Session-Block, der die kaputte Form wörtlich
zitiert — **ein Wächter, der das Richtige an der falschen Stelle prüft, ist derselbe Fehler wie der
verworfene Marker**, nur eine Ebene tiefer.

**Nächster Schritt, nach Zuständigkeit — und es ist fast nichts mehr, was an mir hängt.**
(1) **Du: die Modulstatus-Tabelle kürzen** (der einzige verbliebene Hebel, Zahlen oben, Weg
bewährt) oder sie als Endzustand benennen. (2) **Du: das zweite Claude-Konto umstellen** — drei
Handgriffe, kein Code; danach P9-13/V150 ✅. (3) **Du: P9-15** — drei Läufe `/api/v1/overview` mit
echter UI-Session, ein Cookie-Jar gehört nicht in eine Datei. (4) **Die Wurzel-Rotation**: heute entschieden (K=1) und gebaut — **P9-A ist der unberührte Scope-Lock**, der Fehlname „P9-A-Umkehr" ist in der Wurzel datiert korrigiert
Wurzel-`CLAUDE.md` (Umkehr + K=?; `K=1` ⇒ 17.515 B, liegt bereit). Danach, und **erst dann**:
Übersichtsgrafik §12.4 gerendert **und angesehen**, ROADMAP-Zeile, Phase auf ✅. **Fester Termin:
am 2026-10-18 schließt das Übergangsfenster von selbst** — die alte Adresse liest dann nur noch.
Absicht, kein Versehen.

**[2026-10-04, wie dieser Block überholt ist]** (1) und (4) sind **erledigt** — beide Strukturen
rotiert, beide Heads unter dem Softcap (Nachtrag unten). **(2) ist zurückgestellt und wandert nach
P10**: ein Schritt, der ein Konto braucht, ist kein Blocker (Plan §0.1a). **(3) P9-15 ist die Arbeit
der nächsten Session.** Die Liste bleibt unverändert stehen, weil ein Block ein Datumszeug ist.

### Nachtrag — die Wurzel-Rotation und das L3-Archiv: beide Heads jetzt unter dem Softcap

**Zwei Benennungen, die zwei Sessions lang offen waren, sind entschieden und gebaut (Nikinger,
2026-10-04), und die Antwort auf die erste war nicht die erwartete.** Die Phase hatte
`phase9_hardening/CLAUDE.md` bei **56.860 B = 15.900 B über** dem Softcap; Session-Block und
`updated:`-Kette waren heute Vormittag rotiert, und die Antwort auf „wie viele Blöcke bleiben im
Head?" lautet: **das war nie der Hebel.** Nach beiden Rotationen stand der Head bei 49.033 B — noch
**rund 14 KB drüber**, weil die **§-Modulstatus-Tabelle allein 30.564 B in 14 Zeilen** trug, davon
**15.041 B in drei Zeilen** (Gate/Z 6.075 · A 4.915 · B 4.050). **K=1 ist die Konvention, und selbst
K=1 passt nicht**, weil nicht die *Anzahl* der Blöcke das Problem ist, sondern die **Breite einer
Tabelle.** Beide Wege sind derselbe: verbatim nach L3, Roundtrip-Gegenprobe, im Head ein Kurzstand.
**Gebaut:** `phase9_hardening/MODULE_STATUS_ARCHIVE.md` — eine Sektion je Step, jeder Text
**byte-identisch**; im Head je Step ein **Kurzstand** mit Marker, Zustand, Offenem und Zeiger. Head
**56.860 → 31.357 B**, damit **zum ersten Mal unter dem 40-KiB-Softcap.**

**Und der zweite Weg, der derselbe ist: die Wurzel.** `CLAUDE.md` trug **24** Session-Blöcke in
§Current state (91.123 B von 114.771 B); **K=1** ⇒ **32.334 B**, die älteren 23 **verbatim** nach
`docs/PROJECT_SESSION_LOG.md` (L3, wohin die Wurzel seit 2026-09-08 selbst zeigt). **Byte-Buchhaltung
auf das Byte: 216.221 B in beiden Dateien vorher == 216.221 B nachher.** Dafür gab es bisher **kein
Werkzeug** — `rotate_session_block.sh` schneidet an `^## Session stopped`, und die Wurzel trägt ihre
Blöcke als `**[YYYY-MM-DD, `-Absätze. Also **`scripts/rotate_root_current_state.sh`** (sechs
Gegenproben) mit einer Eigenschaft, die kein Skript bisher hatte: **KEEP ist der _neueste_ Block,
weil die Wurzel newest-first ist — im Phase-Head ist die Reihenfolge umgekehrt.**

**Drei eigene Fehler in diesem Block, zwei davon von einem Wächter gefunden und einer von einer
Gegenprobe, die ich für eine Formkorrektur hielt.** (1) Die erste Fassung des Skripts übernahm die
Bedingung des Vorbilds (`i < TOTAL_BLOCKS - KEEP`, „die letzten KEEP bleiben") und hat damit bei K=1
den **ältesten** Block behalten und den neuesten archiviert. **Nicht** die Mengen-Gegenprobe hat es
gemeldet, sondern die **Byte-Gegenprobe** — und sie meldete den Block, an dem *zwei* Blockgrenzen
lagen, also die Reihenfolge und nicht die Zahl. (2) `block_end` gab `MARKS[i+1] - 2` und ließ damit
**an jeder Grenze eine Leerzeile fallen**; die Reassemblierungs-Gegenprobe brach ab, zu Recht — ein
Schnitt, der eine Zeile je Grenze verliert, ist stiller Datenverlust und kein Rundungsfehler. Erst
danach war der Archivteil byte-identisch. (3) Ich habe den Tippfehler „Doko-Strukturen" erst beim
Suchen bemerkt, und beim Suchen **zwei weitere Anker nicht gefunden**, weil ein Anker den Tippfehler
enthielt — **ein Anker, der den Fehler des Textes kopiert, findet den Fehler nicht.** Und eine
Diagnose, die ich selbst für erledigt hielt: der Ausdruck **„P9-A-Umkehr"** ist ein **Fehlname**,
siehe die datierte Korrektur in der Wurzel.

**Selbstprüfung:** `pytest` 1209 → **1218** · `ui_budget` **5/5** · `doc_health` **0** · Tabu-Pfade
unberührt · **kein `systemctl`, kein `pkill -f`**, keine Wegwerf-Instanz, kein Deploy. **`doc_health`
hat viermal rot gemeldet, viermal zu Recht** — nach jeder Größenänderung eine exakte INDEX-Angabe.

**Nächster Schritt — es ist nichts mehr, was an mir hängt, und genau das hat sich heute geändert.**
**Nikinger-Entscheidung 2026-10-04: Schritte, die am Fabi-Konto hängen, sind nie ein Phasen-Blocker.**
P9-13/V150 (das zweite Claude-Konto) standen zwei Sessions auf ⚠️ „1 von 2 Konten" und wurden damit
**faktisch zum Blocker durch eine Person**; sie sind heute auf ⬜ mit Wanderungsvermerk nach P10
gesetzt, und die Regel steht in der Wurzel-`CLAUDE.md` §Working style wie im Plan §0.1a. **Die
Marke wechselt dabei von ⚠️ auf ⬜, weil das zwei verschiedene Dinge sind:** ⚠️ heißt in dieser Matrix
*erfüllt mit benannter Abweichung*, und ein Konto ist keine Abweichung, sondern ein fehlender
Schritt. **Die Begründung, die man merken muss:** ein Schritt, den nur ein Mensch mit einem Konto tun
kann, ist **ein Termin**. Ein echter Blocker wäre ein **Code**-Fehler oder ein **Mess**-Befund.

**Und was bleibt, ist jetzt eine Aufgabe und kein Termin mehr: P9-15 ist die Arbeit der nächsten
Session.** Drei Läufe `/api/v1/overview` mit **echter UI-Session** (Passwort + TOTP) gegen die
Referenz 372,9 ms, die selbst falsch ist (in-process, `ui_budget.py`, nie über Funnel — gemessen am
2026-10-03, see dort). **Der offene Weg, damit daraus kein Cookie-Jar in einer Datei wird:** der
Browser wird von Playwright bedient und die **Anmeldung macht der Nikinger einmal im sichtbaren
Fenster** — das Passwort und der TOTP verlassen sein Fenster nie, es steht in keiner Datei und in
keinem Kommando, und der nächste Lauf kann die drei Läufe gegen dieselbe Session wiederholen. **Vor
dem Bau kurz in `docs/concepts/sichtpruefung_automation_conventions.md` nachsehen**, ob das dort
schon als Muster steht.

Danach, und **erst dann**: Übersichtsgrafik §12.4 gerendert **und angesehen**, ROADMAP-Zeile, Phase
auf ✅. Beide Benennungen von heute sind gebaut; beide Heads liegen unter dem Softcap.
