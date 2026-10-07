---
status: live
purpose: Teil der Abnahmematrix Phase 9 — die Blöcke doing, trace, settings und die drei Bildsichtungen (P9-59 – P9-120). Zeilen mit Stand und Beleg; die Bilanz und die Statusregel stehen im Hub ABNAHME_MATRIX.md
read-when: wenn eine Zeile aus diesem Bereich gesucht, belegt oder auf einen anderen Marker gesetzt wird
detail: L2
up: ./ABNAHME_MATRIX.md
down:
  - ../docs/concepts/phase9_hardening_block_doing_plan.md      # P9-59 – P9-68
  - ../docs/concepts/phase9_hardening_block_trace_plan.md      # P9-69 – P9-82
  - ../docs/concepts/phase9_hardening_block_settings_plan.md   # P9-83 – P9-120
updated: 2026-10-07 (angelegt — die Matrix ist in einen Hub und drei lebende Teile geteilt, jeder unter dem 40-KiB-Softcap; Abschnitte per `scripts/move_sections.py` verbatim aus dem Hub hierher)
---
# Abnahmematrix Phase 9 — Teil: die Blöcke doing, trace, settings und die drei Bildsichtungen (P9-59 – P9-120)

> Lebender Teil (📗), **kein** Archiv: die Zeilen hier zählen in die Bilanz im Hub
> `ABNAHME_MATRIX.md`, und ihr Marker darf sich ändern. Alles unter dieser Zeile ist beim Teilen
> **wortgleich** aus dem Hub verschoben worden.

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
