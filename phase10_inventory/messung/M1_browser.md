---
status: live
purpose: M1 — Wartezeiten im Browser des Nikingers über beide Eingänge (Domain, Funnel): Messwerte dreier Reihen und die daraus festgelegten Zielwerte D-3 (Register PF-1–PF-3, PF-5)
read-when: M1 auswerten oder D-3 festlegen
detail: L2
up: ../CLAUDE.md
down:
  - ../../docs/concepts/phase10_inventory_plan.md   # §4 M1: Anordnung
  - ../BAUSTELLENREGISTER.md                         # PF-1–PF-3, PF-5, D-3
updated: 2026-10-20 (M1 gemessen: drei Reihen, D-3 festgelegt)
---
# M1 — Browser-Messung

Anordnung (Plan §4): DevTools → Network, **kein HAR**, je Eingang **drei Läufe** von vier Szenarien.

| Szenario | Was | Zu notieren |
|---|---|---|
| S1 | Kaltstart, „Disable cache" an, bis die Übersicht steht | `DOMContentLoaded`, `Load`, `/api/v1/overview` Waiting + Total |
| S2 | warm, Home-Knopf | `/api/v1/overview` Waiting + Total |
| S3 | drei Space-Wechsel | je `/api/v1/items?…` Total |
| S4 | ein Item öffnen | Total der Item-Anfrage |

**Kontext je Messreihe:** Netz (Heim/Mobil/Arbeit) · Uhrzeit · Eingang (Domain `sharefyx.eurofyx.com` / Funnel `*.ts.net`).

**Abweichungen von Plan §4 M1 (P10-4 daher mit Vorbehalt):** S2 (Home-Knopf) nur im Arbeitsnetz gemessen, in beiden mobilen Reihen entfallen · Reihe 2: S1 ohne `overview`-Wert · die Domain ist aus dem Arbeitsnetz nicht erreichbar (Firmen-Proxy), Domain nur mobil · kein freier S4-Lauf im Arbeitsnetz · Zeitfenster der Reihe 3 nicht genannt · Safari/Firefox je nur eine Kombination Gerät × Netz. Die Aussage (Server-Boden 4,8–5,2 s, Stau hinter `overview`) trägt trotzdem, weil sie in allen drei Reihen gleich ausfällt.

## Messwerte (ms)

| Eingang | Netz | Uhrzeit | Szenario | Lauf 1 | Lauf 2 | Lauf 3 |
|---|---|---|---|---|---|---|
| Domain | | | S1 DCL / Load / overview Wait / Total | | | |
| Domain | | | S2 overview Wait / Total | | | |
| Domain | | | S3 items Total (×3 Wechsel) | | | |
| Domain | | | S4 Item Total | | | |
| Funnel | Arbeit (Firefox Dev) | 07:30–07:55 | S1 overview Total (Cache aus) | 4853 | 4828 | 4889 |
| Funnel | Arbeit (Firefox Dev) | 07:30–07:55 | S2 overview Total (Cache aus) | 4824 | 4869 | 12931 (Worst Case: Klick während laufender Aufrufe) |
| Funnel | Arbeit (Firefox Dev) | 07:30–07:55 | S3 items Total, je Block drei+ Wechsel (Cache aus) | 313 / 326 / 245 (frei); 4. Wechsel Home-Server 4830 (hinter Poll) | 8359 / 7009 / 8530 / 7347 / 6119 / 3867 / 1850 (während laufender Aufrufe) | 12174 / 8923 / 6893 / 4482 / 3496 (hinter 12-s-Stau) |
| Funnel | Arbeit (Firefox Dev) | 07:30–07:55 | S4 Item Total (Cache aus) | 8367 | 4813 | 9528 (alle drei hinter einem laufenden `overview`) |

Referenz serverseitig (M2): `/overview` Grundlinie ~2,4 s (`messung/M2_overview_bench.json`).

## Befunde S1 (Funnel, Arbeitsnetz, Firefox Developer Edition, 2026-10-20)

- `/api/v1/overview` **4853 / 4828 / 4889 ms** — auffallend stabil, also serverlastig, nicht netzbedingt (M2: ~2,4 s).
- `spaces` hängt gleich lang wie `overview` (4827 / 4896 ms), `items` (199–204 ms) und `graph` (288–388 ms) laufen erst danach; in Lauf 2 wartete sogar `favicon.ico` 4629 ms. Starke Indizien für einen blockierten Event-Loop (`api.py:685 _overview` ist `async def` mit synchronem `store.search()`, kein `to_thread`) — **noch nicht bewiesen**.
- Shell steht früh: DOMContentLoaded 157 ms, Load 831 ms (Lauf 1); statische Dateien 55–350 ms je Datei.
- Lauf 1 und 2 zeigen ein **zweites** `overview`/`spaces` direkt nach dem Laden (8317 ms bzw. noch offen), Lauf 3 nicht — Auslöser ungeklärt.
- Messart: Gesamtdauer aus der Balkenbeschriftung der Wasserfall-Spalte (Antwort nur 12 kB, Waiting ≈ Total); DCL/Load nur aus Lauf 1.
- S2 (Home-Knopf) **4824 / 4869 / 12931 ms**; Lauf 3 startete, während weitere `overview`-Aufrufe (Poll) offen waren — gestaute Aufrufe addieren sich (`spaces` im selben Fenster 61 / 658 / 1305 ms, wenn es nicht hinter `overview` wartet).
- 20-s-Poll im Dauerlauf (6 Paare in ~1,5 min): `overview` 4824 / 4829 / 4857 / 4834 / 4835 / 4808 ms. Der zweite `overview`/`spaces` im **Dauerlauf** ist demnach der Poll (`COUNTER_POLL_MS`); die Fokus-Vermutung (Claude Code) ist **nur dafür** widerlegt (Einwand des Nikingers: der Log lief weiter). Für das `overview`, das bei **jedem Item-Öffnen** mitläuft, bleibt sie offen (Reihe 3, §D-3).
- S3 (Space-Wechsel, `items?type=task&status=open&space=…`): **frei 245–326 ms**; sobald ein `overview` läuft, wartet der Wechsel bis zu dessen Ende — gemessen 1850–8530 ms, im schlechtesten Block **12174 ms** (hinter einem 12-s-Stau aus mehreren `overview`-Aufrufen).
- Klicks **innerhalb** eines Spaces (`items?type=…&status=…&space=Home-Server`, sechs Stück, ohne laufenden `overview`): **202–218 ms**.
- S4 (Item öffnen, `items/itm_…`, 3–37 kB): **8367 / 4813 / 9528 ms** — in allen drei Läufen lief gleichzeitig ein `overview` (8490 / 8241 / 9591 ms); ein freier S4-Lauf wurde **nicht** erfasst (Item-Anfrage bei freiem Server nicht gemessen).
- Testzeitraum Funnel/Arbeitsnetz: 2026-10-20, 07:30–07:55 Uhr (Angabe des Nikingers).
- S4 Nachlauf (`itm_b9fe1326`, 8,9 kB): **4754 ms**, wieder mit gleichzeitigem `overview` (4853 ms) — auch der als „ohne overview" gedachte Lauf war keiner. Vier von vier Item-Öffnungen trafen einen `overview`; die Code-Suche (`list.js`, `editor.js`, `tree.js`) fand **keinen** Aufruf von `loadOverview` auf dem Öffnen-Pfad (nur nach Schreibvorgängen) — Auslöser offen, Poll-Zufall bei vier von vier unwahrscheinlich (Poll belegt rund 24 % der Zeit).

## Reihe 2 — Funnel, MacBook mobil (Mobilfunk, ohne VPN), Safari, 2026-10-20 (ca. 11:10–11:24 Uhr)

Safari, Caches deaktiviert, Spalte „Zeit" der Netzwerk-Tabelle. Beim Laden erscheint der Hinweisdialog „Es gibt eine neue Adresse" (UI) — keine Anfrage, nur Anzeige.

| Szenario | Gemessen |
|---|---|
| S1 Kaltstart (3 Läufe) | Shell (23 Anfragen, ohne `overview`) fertig nach **1,68 / 3,38 / 3,52 s**; `/ui/` selbst 322 ms / 2,16 s / 2,39 s (Arbeitsnetz Firefox: 204–375 ms). `overview` ist in den drei Screenshots **nicht im Bild** — Lücke. |
| S3 Space-Wechsel | zwei Blöcke mit vielen Klicks: Block 1 `items` **18,80 / 15,47 / 6,60 / 8,68 s** (`overview`/`spaces` daneben 13,85 s, `spaces` zuletzt 2,49 s); Block 2 `items` **16,47 / 15,51 / 28,43 / 26,35 / 25,63 / 22,41 / 14,47 / 19,66 s** (`overview`/`spaces` 16,46 s, 19,62 s, 9,33 s). Kein freier Wechsel dabei. |
| S4 Item öffnen | **11,80 s** (`overview` 11,88 s daneben) · **95,8 ms** (nach Neuladen, `items` fertig, kein `overview` mehr offen — erster freier S4-Wert) · **8,67 s** (`overview` 8,67 s daneben) |

- Der freie S4-Wert (95,8 ms) zeigt: ein Item selbst kostet kaum etwas; die Wartezeit kommt aus dem Stau hinter `overview`.
- Mobil ist `overview` mit 5,1–19,6 s deutlich länger als im Arbeitsnetz (4,8 s) — hier addieren sich Netz und gestaute Aufrufe (mehrere `overview`/`spaces` aus Poll und Klicks gleichzeitig); die Anteile sind aus diesen Screenshots nicht trennbar.
- **Empfangstest (Speedtest, MacBook mobil, Angabe des Nikingers):** Download 18,2 MB/s · Upload 3,36 MB/s · Ping **24 ms** im Leerlauf, **489 ms** unter Download-Last, **257 ms** unter Upload-Last · Jitter 8 ms. Das Netz ist schnell, aber unter Last träge (hohe Latenz bei Auslastung).
- S1 bleibt in Reihe 2 ohne `overview` stehen (Entscheidung Nikinger: Aussage steht bereits; der Vergleichswert kommt aus Reihe 3, Domain).

## Reihe 3 — Domain (`sharefyx.eurofyx.com`, VPS), MacBook mobil, Safari, 2026-10-20 (Zeitfenster nach 11:24 Uhr, nicht genannt)

Gleiche Einstellungen wie Reihe 2 (Caches deaktiviert). Vorgehen des Nikingers: warten, bis `overview` fertig ist, dann sofort ein Item öffnen — **kein realistisches Nutzerverhalten**, ein Messkniff.

| Szenario | Gemessen |
|---|---|
| S1 Kaltstart (3 Läufe) | `/ui/` **6,29 s / 254 ms / 6,29 s** (Seitenladezeit laut Statuszeile 6,74 s / 760 ms / 6,83 s); `overview` **4,96 / 4,89 / 5,16 s**, `spaces` 4,91 / 4,89 / 5,16 s; `items` 238 ms / **5,02 s** / 263 ms; `graph` 444 / 475 / 450 ms; statische Dateien je 101–314 ms |
| S3 Space-Wechsel (13 `items`-Anfragen in drei Blöcken) | frei: **273 / 335 ms**; sonst 1,59 / 1,83 / 1,91 / 2,18 / 2,70 / 3,10 / 4,41 / 4,61 / 6,57 / 8,93 / **14,22 s**; `overview` daneben 4,91–14,12 s |
| S4 Item öffnen (3 Läufe) | `itm_b9fe1326` **4,87 s** · `itm_73365679` **4,06 s** · `itm_f1c166bb` **4,89 s** — jedes Mal startete **gleichzeitig mit der Item-Anfrage ein neues `overview`/`spaces`-Paar** (4,95 / 12,91 / 4,96 s) |

- `/ui/` ist auf der Domain zweimal 6,29 s und einmal 254 ms: kalte Verbindung (mobil) gegen warme — **Vermutung, nicht belegt**.
- Das `overview` selbst kostet über die Domain **4,9–5,2 s** und im Funnel mobil 5,1 s (Reihe 2) und im Arbeitsnetz 4,8–4,9 s: **kein Eingangsunterschied bei `overview`**. Der Eingang unterscheidet sich nur bei `/ui/` und statischen Dateien.
- In allen drei S4-Läufen startet das zweite `overview` zusammen mit der Item-Anfrage, obwohl der Nikinger erst auf das Ende des vorigen `overview` wartet — kein Poll-Zufall. **Hypothese (nicht geprüft):** der `focus`-Handler in `app.js` (`window.addEventListener("focus", pollCounters)`) feuert, wenn der Nikinger vom Inspektor/Screenshot zurück in die Seite klickt, und löst jedes Mal ein `overview` aus. Das wäre ein Messartefakt **und** ein echter Nutzerpfad (jede Rückkehr in den Tab = ~4,8 s Blockade). Prüfung: Playwright-Probe auf der Wegwerf-Instanz, Item öffnen mit/ohne vorherigen Fokuswechsel.

## D-3 — Zielwerte (Nikinger 2026-10-20)

Festgelegt nach den drei Reihen oben; Abnahme in P10.5 mit dem Instrument `probes/p10_overview_bench.py` (M2) und einer Browser-Probe.

| Nr | Ziel | Abnahme |
|---|---|---|
| Z1 | `/api/v1/overview` serverseitig **≤ 300 ms** bei Live-Last — **unter Vorbehalt der Machbarkeit** (Nikinger: „wenn das realistische Zahlen sind") (heute ~2,4 s im Bench, 4,8–5,2 s im Browser) | Bench M2 (4 Spaces × 50 Items) |
| Z2 | **Kein Request wartet auf `/overview`**: Event-Loop bleibt frei; ein freier Space-Wechsel ≤ 1 s auch bei laufendem `overview` | Playwright-Probe: `overview` verzögern, Space wechseln, Item öffnen |
| Z3 | **Gerüst steht ≤ 1 s** (Layout und Platzhalter), Inhalt folgt; mobil kalte Verbindung ausgenommen | Browser-Probe, Shell-Zeit |
| Z4 | **Ladeanimation-Regel:** jede Anzeige, die länger als **200 ms** braucht, zeigt einen passenden Ladezustand (Gerüst/Platzhalter, Form offen); unter 200 ms geht sie **sofort** durch, ohne Animation | UI-Probe mit verzögertem Endpunkt (< 200 ms: kein Platzhalter, > 200 ms: Platzhalter) |

- **Grenze Hard Rule 3:** ein Platzhalter oder zwischengespeicherter Stand trägt nie eine `version` in einen Write; geschrieben wird nur auf frisch geladenen Items.
- **Realismus von Z1:** ungeprüft. Zählen über den Index statt sechs Durchläufe je Space (PF-1) soll es erreichen; fällt der Bench darüber, entscheidet der Nikinger neu (Z1 ist dann ein Messbefund, kein Fehler).
- **PF-3 (Cache) / PF-5 (Virtualisierung):** erst bauen, wenn Z1–Z3 gemessen offen bleiben.
- **Offene Prüfungen (P10.5 oder eigene Probe):** (a) Auslöser des `overview`, das bei jedem Item-Öffnen mitläuft (Hypothese: `focus`-Handler); (b) Event-Loop-Blockade `_overview` (`to_thread`) mit zwei parallelen Anfragen belegen; (c) freier S4-Wert im Arbeitsnetz.
