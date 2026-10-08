---
status: live
purpose: "Mini-Plan P9 Block feedback — die Nutzer-Rückmeldung vom 2026-10-07 (Übersicht unlesbar, Anlegen im fremden Space landet zu Hause, Enter/ESC, Löschdialog, Ladezeiten, Schließen-Knopf, Mitglieder-Knöpfe) plus drei Scope-Entscheidungen (Verschieben/Löschen in Team-Spaces, Umbenennen, Editor-Umbau). Locks P9-BG–P9-BO (P9-BP vorgeschlagen), Abnahme P9-121–P9-134, [VERIFY] V189–V194"
read-when: Bau des feedback-Blocks, oder wenn der Nikinger eine der drei Scope-Entscheidungen §3 trifft
detail: L2
up: ../../phase9_hardening/CLAUDE.md
down:
  - ./phase9_hardening_plan.md                 # 📕 P9-Plan; Lock P9-A (kein UI-Umbau), P9-K (Löschen nur eigene), §15 P10-Liste
  - ./phase9_hardening_block_settings_plan.md  # Formvorlage; Einstellungs-Kette P9-AE–P9-AL, auf der B4/B5 aufsetzen
updated: 2026-10-08 (**B4 gebaut** — Abstand der Mitgliederzeilen, §8) | 2026-10-08 (**B3 gebaut** — Schließen im Einstellungsmenü, §8) | 2026-10-08 (**E1a gebaut** — Team-Spaces verschieben/löschen, V191/V192 beantwortet, §8; drei datierte Abweichungen) | 2026-10-08 (**B2 gebaut** — Zielangabe im Anlegen-Dialog, §8; datierte Korrektur: der Home-Fall von P9-BH ist unerreichbar) | 2026-10-07 (**Nikinger-Entscheidungen E1–E3 eingetragen**: E1 freigegeben — Lock P9-BP, fremde Items im Team-Space löschbar, Eigentum über den Git-Autor nachverfolgt (P9-BQ); E2 und E3 wandern als offene Punkte in den Closeout/P10; Closeout erst nach B1–B8 + E1a) | 2026-10-07 (angelegt — Rückmeldung des Nikingers vom selben Tag, gegen `main@497c5bd` am Code gelesen; **nichts gebaut**)
---

# Phase 9 — Block feedback: die Rückmeldung vom 2026-10-07

> **Ein Block, kein Phasenplan.** Anlass: die Liste des Nikingers vom 2026-10-07, nach `v3.1.3` und
> dem Portscan. **Nicht gebaut ist noch nichts.** Jede Ursache unten ist **am Code gelesen** (Datei
> und Zeile genannt). Was nur gelesen und nicht gemessen ist, steht als `[VERIFY]`. Gelesen gegen
> `main@497c5bd`.

## §0 Rahmen

### 0.1 Die Rückmeldung, wörtlich und nummeriert

| # | Wortlaut (Nikinger) | Art | Ziel |
|---|---|---|---|
| R1 | „it sekus space kann man in der Übersicht nicht lesen" → „verursacht durch zu viele Details in der Übersicht → Text-Anti-Overflow-Mechanismus einbauen" | Darstellungsfehler | **B7** |
| R2 | „beim Erstellen über UI in fremden Spaces wird Notiz trotzdem im Homespace erstellt, man landet zurück im eigenen Homespace" | **Bug** | **B1** + **B2** (zuerst) |
| R3 | „Enter + ESC bei allen Aktionen" | Bedienung | **B6** |
| R4 | „Name des zu löschenden Items direkt über dem Löschvorgang" | Bedienung | **B5** |
| R5 | „Endlich verschieben / archivieren / löschen / drag and drop in non-Home-Spaces, die nicht der Homespace eines anderen sind" | **Scope** (kehrt P9-K teilweise um) | **§3 E1**, Nikinger-Entscheidung |
| R6 | „Ladezeiten bei Intra-Klicks (z. B. Wechsel von Spaces) verbessern" | Leistung | **B8**, erst messen |
| R7 | „Bearbeiten-Ansicht vollständig durch bessere/veränderte uniformierte UI (ähnlich Word/Excel) ersetzen, keine explizite Bearbeitungsansicht mehr, vollständige Bildschirmfläche" | **Scope** (UI-Umbau) | **§3 E3**, Vorschlag P10 |
| R8 | „non-Home-Spaces + Ordner umbenennen" | **Scope** | **§3 E2**, Nikinger-Entscheidung |
| R9 | „Button von Entfernen von Personen im 3. Submenü bei Spaces verwalten ‚kleben' unten und oben aneinander" | Darstellungsfehler | **B4** |
| R10 | „Schließen-Button zum Main-Einstellungsmenü adden" | Bedienung | **B3** |

### 0.2 Was dieser Block **nicht** ist

- **Kein UI-Umbau** (Lock P9-A gilt weiter). Deshalb steht R7 unter §3 und nicht unter §4.
- **Kein Server-Verstehen.** Alles hier ist Darstellung, Bedienung oder Rechte. Der Server bleibt dumm.
- **Keine P1-Contract-Öffnung.** B1 nutzt das vorhandene `create(space, …)` des Stores. Das MCP-Werkzeug
  `create_item` ruft es seit P6 schon mit fremdem Ziel-Space auf (`phase2_mcp/mcpserver/tools.py:641`).

### 0.3 Tabu-Diff

`phase1_storage/`, `phase4_auth/`, `phase2_mcp/` bleiben unberührt, **außer** §3 E1 wird freigegeben.
Dann wird `phase5_ui/webui/api.py` angefasst, nicht die Permissions-Schicht. Erlaubt sind
`phase5_ui/webui/{api.py,static/app.html,static/app.css,static/js/*}`, die Tests dazu und
`phase9_hardening/`.

## §1 Befunde am Code (2026-10-07)

**B-1 — R2 ist ein echter Bug, und zwar ein architektonisch gewollter, der nie nachgezogen wurde.**
- Der Server liest kein `space` im Body von `_items_post`. Der Kommentar dazu (`phase5_ui/webui/api.py:867`)
  sagt: „der Ziel-Space ist immer die Sitzung, ein mitgeschicktes `space` wird stillschweigend
  ignoriert" (Lock P5-A).
- Das UI blendet den Anlegen-Knopf in schreibbaren Team-Spaces trotzdem **ein**:
  `activateView()` → `setCreateControlsPresent(activeSpaceWritable())`, `static/js/tree.js:316`.
- Es schickt keinen Space mit (`static/js/dialogs.js:1068`) und navigiert danach fest nach
  `navigate(state.ownSpace, …)` (`dialogs.js:1077`).
- Seit P6-U (Hard Rule 4, Fassung 2026-08-09) ist der Schreib-Ziel-Space aber **Daten**
  (`.share.yml` `write:`), nicht die Sitzung. MCP hat das umgesetzt, die Web-UI nicht.
- Dieselbe Lücke hat „Als neues Item anlegen" im Konfliktdialog (`dialogs.js:1046–1051`): eine
  Konfliktkopie aus einem Team-Space landet im Home-Space.

**B-2 — R1: der Space-Name hat in der Übersichtszeile die Breite 0 als Basis.**
- `.overview__space-name-label` hat `flex: 1; min-width: 0` (`static/app.css:1128`), also Basis 0.
- `.overview__space-counts` hat die Basis `auto`, also die volle Breite aller Chips. Eine Zeile mit
  vielen nicht leeren Eimern gibt den Platz zuerst den Chips, und der Name wird zu „i…" abgeschnitten.
- Das ist **das Gegenteil** eines Anti-Overflow-Mechanismus: der Overflow-Schutz sitzt am
  Namen, der eigentlich gelesen werden soll.
- *Gelesen, nicht gemessen* → V189.

**B-3 — R3: ESC ist schon global, Enter nicht.**
- `static/js/app.js:255–282` schließt mit ESC jedes der elf Overlays, von rechts nach links.
- Einen globalen Enter-Weg gibt es nicht. Enter wirkt nur dort, wo ein Feld es einzeln verdrahtet:
  im Link-Picker (`dialogs.js:762`) und an den Übersichts-Chips (`list.js:133`).

**B-4 — R4: der Titel steht im falschen der beiden Dialoge.**
- Der erste Schritt (`openTrashDialog()` → `confirmDialog`, `dialogs.js:357–360`) nennt den Titel im Fließtext.
- Der zweite Schritt, in dem man ihn **eintippen** muss (`#trash-dialog`, `static/app.html:574`), nennt
  ihn nicht. `trashConsequenceEl` (`dialogs.js:374`) sagt nur „Zur Sicherheit den Titel eintippen".

**B-5 — R9: die Mitgliederzeilen haben keinen Abstand, und das konnte bisher niemand sehen.**
- `.space-member-row` (`static/js/spaces.js:105`) hat keine CSS-Regel für einen Abstand.
- Die Wegwerf-Probe der Einstellungs-Kette hat **keine Mitglieder**. Das steht als benannte Grenze in
  P9-107 und P9-110 („die `<li>`-Mitgliederliste ist im Harness nicht darstellbar").
- Der Befund liegt also **genau in der Lücke, die die Matrix benannt hat**. Dieser Block schließt sie,
  statt sie wieder zu benennen.

**B-6 — R10:** das Menü-Panel `#settings-menu` (`app.html:385–403`) hat drei Menüpunkte, aber keine
`.overlay__actions`. Schließen geht nur mit ESC oder per Klick daneben.

**B-7 — R6: es gibt eine gemessene Spur, aber keine Messung des Space-Wechsels.**
- P9-15 hat `/api/v1/overview` aus dem Browser gemessen: **~3,1 s** über beide Adressen. Die
  `overview`-Schleife steht deshalb auf der P10-Liste.
- Ein Space-Wechsel (`activateView()`, `tree.js:299–319`) ruft nur `loadItems()`, also `/items?space=…`.
  Ob der Wechsel langsam ist, weil `/items` langsam ist, oder weil anderswo `loadOverview()`
  mitläuft, ist **nicht gemessen** → V190.

**B-8 — R5: Verschieben und Löschen sind in Team-Spaces an zwei Stellen gesperrt, beide absichtlich.**
- **Löschen:** P9-K, „nur eigene, schreibbare Items" (`api.py:1067–1070`, serverseitig).
- **Ordner-Verschieben:** `api.py:956`, `acl.space != session.space` → `forbidden`. In einem
  **Team-Space ist niemand der Eigentümer**, denn der Team-Space ist nicht der Home-Space eines
  Mitglieds. Deshalb kann dort **niemand** verschieben.
- **Im UI:** `movable = !item.readonly && item.space === state.ownSpace` (`list.js:426`). Davon hängen
  Strg+Klick, Long-Press, Drag und der Verschieben-Knopf ab.
- **Archivieren** ist serverseitig schon frei (`can_write_item_as_human`, `api.py:1161`). Ob das UI den
  Knopf dort zeigt, prüft V191.

## §2 Gelockte Entscheidungen (für B1–B8; P9-BP ist nur Vorschlag, §3 E1)

| Lock | Entscheidung | Warum |
|---|---|---|
| **P9-BG** | **Anlegen geht in den aktiven Space, wenn er schreibbar ist.** Der Client schickt `space`. `_items_post` prüft genau wie `tools.py:641`: `space` fehlt → Home-Space; `space != session.space` → `permissions.can_write(session.space, space)`, sonst `forbidden`. Danach landet man **im Ziel-Space** (`navigate(item.space, …)`), nicht im Home-Space | Eine Regel, zwei Wege (MCP und Web). Ersetzt **P5-A für den Web-Pfad**, datiert 2026-10-07. Hard Rule 4 in der Fassung vom 2026-08-09 verlangt das ausdrücklich |
| **P9-BH** | **Der Anlegen-Dialog nennt sein Ziel** („Anlegen in: *it sekus*"). In der globalen Sicht oder in einem nur lesbaren Space ist das Ziel der Home-Space, und das steht dann auch da | Der Bug war genau, dass das Ziel unsichtbar war. Ein Dialog ohne Zielangabe lässt den nächsten Bug wieder unsichtbar |
| **P9-BI** | **„Als neues Item anlegen" im Konfliktdialog** legt im Space des Konflikt-Items an (`state.editingSnapshot.space`), mit derselben Prüfung | Sonst hätte P9-BG einen zweiten, versteckten Eingang mit dem alten Verhalten |
| **P9-BJ** | **Übersicht: der Name hat Vorrang vor den Chips.** Name `flex: 0 1 auto` mit eigener Mindestbreite (Kandidat `min-width: min(16ch, 40%)`, mit V189 messen). Die Chip-Leiste bekommt `flex: 1 1 0; min-width: 0` und **bricht in eine zweite Zeile um**. Der volle Name steht immer im `title` | Der Anti-Overflow gehört an das, was weichen darf (die Chips), nicht an das, was gelesen werden soll. **Kein „+N"-Sammelchip**, solange zwei Zeilen reichen: das wäre ein neues Bedienelement, ohne dass gemessen ist, dass es gebraucht wird |
| **P9-BK** | **Enter löst die Primäraktion des obersten offenen Overlays aus.** Ein Handler in `app.js` neben dem ESC-Zweig. Er gilt nur in einzeiligen `<input>`, nie in `<textarea>`/`<select>`, nicht bei `event.isComposing`, und nicht, wenn der Primärknopf `disabled` ist. Primärknopf ist `.btn-primary` des Panels, in der Einstellungs-Kette der des **rechtesten** Panels. Inline-Felder mit Nachbarknopf (Mitglied hinzufügen, neuer Space) bekommen dasselbe Verhalten | Ein Handler statt elf: dieselbe Disziplin wie ESC (`app.js:255`). „Primär" ist schon im Markup markiert, und `disabled` ist schon das Gate des Löschdialogs. Enter kann das Titel-Gate also nicht umgehen |
| **P9-BL** | **Der Löschdialog zeigt den Titel als eigene Zeile direkt über dem Eingabefeld**, hervorgehoben und per `textContent` (der Titel ist Nutzerdaten, Hard Rule 4) | R4 wörtlich. Das Gate bleibt exakt (P9-K): **sichtbar machen ist nicht lockern** |
| **P9-BM** | **Mitgliederzeilen bekommen den Standardabstand am Wrapper** (`#space-member-list` als Flex-Spalte mit `gap: var(--space)`), nicht als `margin` am Knopf | Dasselbe Muster wie P9-AU (Menüpunkte). Der letzte Eintrag braucht keine Sonderbehandlung |
| **P9-BN** | **Das Einstellungsmenü bekommt „Schließen"** als `.btn` in `.overlay__actions`. Der Knopf schließt die **ganze** Kette, nicht nur das Menü | Ein Menü, das die Kette offen ließe, wäre ein Zustand, den ESC nie erzeugt |
| **P9-BO** | **Ladezeit: erst messen, dann bauen.** Kein Cache und kein Prefetch ohne V190. Ein Cache darf **nie** eine veraltete `version` zum Schreiben anbieten (Hard Rule 3). Er zeigt höchstens und lädt nach | Der einzige gemessene Wert (P9-15) betrifft `/overview`, nicht den Space-Wechsel. Raten wäre hier am teuersten |

## §3 Scope-Entscheidungen — **entschieden 2026-10-07**

| Frage | Entscheidung des Nikingers (wörtlich) | Folge |
|---|---|---|
| E1 | *„yes, that's thesable. But still track ownership if possible."* | **P9-BP gelockt** (Vorschlag unten, mit „alle Items"), dazu **P9-BQ**; Bauschritt **E1a** |
| E2 | *„fair, move it into the closeout as open items."* | **Nicht in P9 gebaut.** Ordner- und Space-Umbenennen stehen als offene Punkte im Closeout (P10-Liste), V193/V194 gehen mit |
| E3 | *„also fair, in my opinion."* | **P10**, Leitprojekt neben dem Karten-Umbau; in die P10-Liste des Closeouts |
| Closeout | *„closeout after these changes are wired."* | Closeout P9 **nach** B1–B8 und E1a |

**P9-BQ — Eigentum nachverfolgen, ohne neues Feld.**
- Seit Block trace (P9-AC, 2026-10-02) trägt jeder Git-Commit im Datenverzeichnis den Handelnden als
  Autor (`phase1_storage/storage/history.py:68`).
- Der Anlege-Commit nennt also, wer angelegt hat. Der Papierkorb-Commit nennt, wer gelöscht hat.
- `updated_by` (Frontmatter) nennt, wer zuletzt geändert hat.
- **Ein `created_by`-Feld wäre die elfte P1-Contract-Öffnung.** Es wird deshalb in P9 nicht gebaut.
  Es steht als P10-Option im Closeout, falls die Git-Spur im UI sichtbar werden soll.
- **Was E1a zeigt:** der Löschdialog im Team-Space nennt „zuletzt geändert von *X*" (`updated_by`),
  wenn das Feld da ist. Wer löscht, sieht dann, ob es das eigene Item ist.
- **Grenze, benannt:** Items vor dem 2026-10-02 tragen im Anlege-Commit die Default-Identität
  (`Space Server`). Ihr Anleger ist nur aus dem Kontext zu erschließen.

*Der Vorschlagstext von E1–E3 bleibt unten unverändert stehen, als Herleitung.*

**E1 — R5: Verschieben, Archivieren, Löschen, Drag & Drop in Team-Spaces.**
- **Vorschlag als Lock P9-BP:** in einem Space, der **nicht** der Home-Space eines Nutzers ist
  (`space ∉ userdir.list_spaces()`, V192), darf jedes Mitglied mit Schreibrecht verschieben,
  archivieren und löschen.
- **Löschen bleibt human-only, ohne Bulk und mit Titel-Gate.** Die Wiederherstellung bleibt Git (P9-J).
- **Home-Spaces anderer bleiben wie heute:** `share_write` erlaubt Ändern, aber nicht Wegnehmen.
- **Was sich dafür ändert:**
  - `api.py:1067` (P9-K) und `api.py:956` (Ordner-Lock) bekommen eine Ausnahme für Team-Spaces.
  - `list.js:426` `movable` bekommt dieselbe Bedingung, aus einem Feld `team: true` in `space_to_json`.
  - Das UI rät sie nicht selbst. Der Server sagt, was ein Team-Space ist.
- **Frage an den Nikinger:** darf ein Mitglied **fremde** Items im Team-Space löschen, oder nur die
  selbst angelegten (`updated_by`/Anleger aus Block trace)?
  - Der Vorschlag ist **alle**: es ist ein gemeinsamer Ordner, und `._trash/` macht jedes Löschen umkehrbar.
- **Warum nicht stillschweigend:** P9-K ist ein Lock mit Begründung (Prompt-Injection über fremde
  Bodies). E1 berührt die Begründung nicht, denn Löschen bleibt **human-only**. Es hebt aber eine
  Sperre auf, und das entscheidet der Nikinger.

**E2 — R8: Umbenennen von Team-Spaces und Ordnern.**
- **Ordner umbenennen** ist im Kern ein Verschieben aller Items eines Ordners. Jedes Item bekommt
  einen PATCH mit eigener `version`; kein Last-Write-Wins, ein Konflikt bricht für dieses Item ab und
  meldet es. Leere Ordner brauchen `ensure_folder` plus Entfernen.
  - Baubar in P9, **wenn E1 frei ist**, denn in Team-Spaces hängt es an derselben Sperre (`api.py:956`).
  - Offen: geht es atomar, oder nur Item für Item? → V193
- **Space umbenennen** berührt Verzeichnisname, `.share.yml` aller beteiligten Spaces,
  Mitgliederlisten, Git-Historie und Links, die den Space-Namen tragen. Das ist eine Datenmigration
  und keine Bedienfrage.
  - **Vorschlag: P10**, mit eigenem `[VERIFY]` V194 („was referenziert einen Space-Namen?").

**E3 — R7: Bearbeiten-Ansicht durch ein Word/Excel-artiges, durchgehend bearbeitbares UI ersetzen.**
- Das ist der Fall, den Lock P9-A ausschließt („kein UI-Umbau").
- **Vorschlag: P10, als Leitprojekt neben dem Karten-Umbau.** Kein Teil davon in P9, auch nicht
  „schon mal die volle Bildschirmbreite". Ein halber Umbau macht den Editor zur dritten Variante.
- Für P10 festzuhalten:
  - kein expliziter Bearbeiten-Modus
  - volle Bildschirmfläche
  - einheitliches Bedienschema
  - Speichern weiter mit `version` (Hard Rule 3). „Immer bearbeitbar" darf nicht „immer
    überschreibend" heißen.

## §4 Bauschritte (ein Commit je Schritt, ein Release `v3.1.4`)

| Schritt | Inhalt | Locks | Probe/Beleg |
|---|---|---|---|
| **B1** | Anlegen im aktiven schreibbaren Space. Server: `space` in `_items_post` lesen und prüfen. Client: `space` mitsenden, danach Navigation nach `item.space`. Konfliktdialog ebenso | P9-BG, P9-BI | Unit-Tests `api.py`: anlegen im Team-Space ✓, im fremden Home ohne `write:` → 403, ohne `space` → Home. Wegwerf-Browserprobe mit **zwei Principals** und Team-Space (Muster: `sichtpruefung_automation_conventions.md`, Zwei-Principal-Wegwerf) |
| **B2** | Zielangabe im Anlegen-Dialog | P9-BH | Probe: Text = aktiver Space bzw. Home in der globalen Sicht |
| **B3** | „Schließen" im Einstellungsmenü | P9-BN | Probe: Klick → Overlay `hidden`, alle Panels zu |
| **B4** | Abstand der Mitgliederzeilen. **Die Probe legt ein Mitglied an** und schließt damit die benannte Grenze von P9-107/P9-110 | P9-BM | gemessener Abstand == `--space` zwischen zwei Zeilen; Gegenlauf mit `gap: 0` → rot |
| **B5** | Titelzeile im Löschdialog | P9-BL | Probe: Zeile direkt über dem Feld, Text == Titel, ein HTML-Titel wird als Text gezeigt |
| **B6** | Enter-Handler | P9-BK | Probe je Overlay (Tabelle in §5): Enter im Feld löst die Primäraktion aus. Ein deaktivierter Knopf (Löschen ohne Titel) bleibt bei Enter folgenlos (**Gegenlauf**). Enter in `<textarea>` macht einen Zeilenumbruch |
| **B7** | Übersicht: Name vor Chips | P9-BJ | Probe bei 1440/1024/390 px mit einem Space mit **allen** Eimern gefüllt: Name voll lesbar (`scrollWidth <= clientWidth`) bis 16 Zeichen, Chips in ≤ 2 Zeilen. Gegenlauf: alte Regel → rot |
| **B8** | Ladezeit: erst V190 messen, dann **ein** gezielter Fix oder der Befund nach P10 | P9-BO | Messung vorher/nachher, drei Läufe, aus dem Browser (Muster P9-15) |

| **E1a** | Team-Spaces: verschieben, archivieren, löschen, Drag & Drop. Der Server liefert `team: true` je Space (V192). `api.py:1067` und `api.py:956` bekommen die Team-Ausnahme, `list.js:426` `movable` übernimmt sie. Der Löschdialog nennt `updated_by` | P9-BP, P9-BQ | Unit-Tests: Team-Space verschieben/löschen ✓ (auch ein fremdes Item); fremder Home-Space mit `share_write` löschen → 403 (**Gegenlauf, P9-K bleibt dort**); Git-Autor des Papierkorb-Commits == Handelnder. Zwei-Principal-Browserprobe mit Drag & Drop |

**Reihenfolge:** B1 zuerst, denn das ist der einzige Bug mit falsch abgelegten Daten. Danach die kleinen
(B3, B4, B5), dann B6/B7, B8 zuletzt. **E1a nach B1**, weil beide `api.py` anfassen und B1 der Bug ist. E2 wird nicht gebaut (§3).

**Sichtprüfung:** acht Bilder nach dem bekannten Muster, Abnahme beim Nikinger.

**Deploy `v3.1.4`:** Nikinger, mit `health_gate.sh --require-todays-update-log`. Dazu ein
`UPDATE_LOG`-Block mit den Punkten in Nutzersprache.

## §5 Enter-Abdeckung (Grundlage für B6)

| Overlay | Primäraktion | Besonderheit |
|---|---|---|
| `create-dialog` | Anlegen | — |
| `new-folder-dialog` | Anlegen | — |
| `link-picker-dialog` | eigener Enter-Weg (`dialogs.js:762`) | **ausgenommen**, sonst doppelt |
| `move-dialog` | Verschieben | Enter nur bei gewähltem Ziel |
| `share-dialog` | Freigeben | Re-Auth-Felder: Enter im TOTP-Feld = Absenden |
| `settings-overlay` | Primärknopf des rechtesten Panels | Passwort: Enter im TOTP-Feld |
| `space-remove-dialog` | Entfernen | Gate bleibt (`disabled`) |
| `conflict-dialog` | **keine** | Zwei gleichrangige Wege, Enter wäre Raten |
| `confirm-dialog` | Bestätigen | — |
| `trash-dialog` | Löschen | nur wenn Titel exakt passt (`disabled` sonst) |
| `legacy-host-dialog` | Schließen | — |

## §6 Abnahme (P9-121 – P9-137)

`P9-121` Anlegen im Team-Space legt **dort** an, und man landet dort ·
`P9-122` Anlegen ohne `space` → Home-Space (unverändert) ·
`P9-123` Anlegen im fremden Home ohne `write:` → 403, nichts geschrieben ·
`P9-124` Konfliktkopie landet im Space des Konflikt-Items ·
`P9-125` Anlegen-Dialog nennt sein Ziel ·
`P9-126` Übersicht: Name bis 16 Zeichen voll lesbar bei 1440/1024/390 px, Chips ≤ 2 Zeilen ·
`P9-127` Enter löst in jedem Overlay aus §5 die Primäraktion aus, die Ausnahmen bleiben folgenlos ·
`P9-128` Enter am deaktivierten Löschknopf ist folgenlos (Gegenlauf) ·
`P9-129` Löschdialog zeigt den Titel als Zeile direkt über dem Feld (Text, kein HTML) ·
`P9-130` Mitgliederzeilen mit Standardabstand, **gemessen mit angelegtem Mitglied** ·
`P9-131` Einstellungsmenü hat „Schließen", der Knopf schließt die ganze Kette ·
`P9-132` V190 gemessen; Fix mit Vorher/Nachher **oder** Befund mit Begründung auf der P10-Liste ·
`P9-133` `pytest` grün (≥ 1250 + neue), `ui_budget` 5/5, Tabu-Diff §0.3 leer, Gegenläufe rot ·
`P9-134` Sichtprüfung des Nikingers, acht Bilder ·
`P9-135` Team-Space: jedes Mitglied mit Schreibrecht verschiebt, archiviert und löscht, auch fremde Items, auch per Drag & Drop ·
`P9-136` Home-Space eines anderen: Löschen bleibt mit `share_write` verboten (403, Gegenlauf) ·
`P9-137` Der Papierkorb-Commit trägt den Löschenden als Git-Autor, der Löschdialog nennt `updated_by`

Die Zeilen kommen beim Bau in einen **neuen** Matrix-Teil (`ABNAHME_MATRIX_BLOECKE.md` hat 36,7 KB,
Regel seit dem Oversize-Fix: neuer Block → neuer Teil, `scripts/move_sections.py`).

## §7 `[VERIFY]`

| Nr. | Frage |
|---|---|
| V189 | Wie breit wird der Name in der Übersichtszeile heute für „it sekus" bei 1440/1024/390 px gemessen, und wie viele Chips hat die Zeile? (Wegwerf mit allen Eimern gefüllt; der echte Space nur beim Nikinger) |
| V190 | Was fordert ein Space-Wechsel an, und wie lange dauert jede Anfrage? Läuft `loadOverview()` mit? (Browser, drei Läufe, Muster P9-15) |
| V191 | Zeigt das UI den Archivieren-Knopf in Team-Spaces, obwohl der Server ihn erlaubt (`api.py:1161`)? |
| V192 | Ist `userdir.list_spaces()` (`phase4_auth/authserver/userdir.py:96`) vom Web-Prozess aus die verlässliche Quelle für „Home-Space eines Nutzers"? Oder braucht E1 ein eigenes Feld in der Space-Liste? |
| V193 | Geht Ordner-Umbenennen atomar (ein Commit), oder nur Item für Item mit je eigener `version`? |
| V194 | Was referenziert einen Space-Namen (Verzeichnis, `.share.yml`, Mitglieder, Index, Links, Auth)? — Grundlage für E2 „Space umbenennen" in P10 |

## §8 Ergebnis

### B1 — Anlegen im aktiven schreibbaren Space (gebaut 2026-10-07, nicht deployt)

- **Server:** `_items_post` (`phase5_ui/webui/api.py`) liest `space` und prüft mit `can_write(actor, target)` — dieselbe
  Prüfung wie `tools.py:641`. Ohne `space` bleibt der Home-Space; ohne `write:` → 403, nichts geschrieben.
- **Client:** der Anlegen-Dialog sendet `space: state.activeSpace` und navigiert nach `item.space`.
- **Datierte Korrektur 2026-10-07 (Code gewinnt):** B1 sagt, die Konfliktkopie nehme den Space aus dem
  Editier-Snapshot. Der Snapshot (`state.editingSnapshot`) trägt **kein** `space`; die Quelle ist
  `state.conflictCurrent.space`. Der Code nutzt sie.
- **Tests:** `test_create_item_has_no_space_parameter` (Lock P5-A) ist durch drei Tests ersetzt, `pytest` **1252**.
- **Browser:** Zwei-Principalen-Probe `phase9_hardening/scripts/p9_feedback_self_check.py` **4/4**; Gegenlauf gegen den alten
  Client **2/4 rot** (S1, S2). S1b (Item steht in der Liste) bleibt auch gegen den alten Code grün und
  trägt nichts. Rohdaten: `phase9_hardening/probes/p9_feedback_b1_probe*.json`.
- **Offene Lücke:** die Konfliktkopie (P9-BI) ist rein clientseitig und im Browser nicht gefahren ⇒ P9-124 ⚠️.

### B2 — Zielangabe im Anlegen-Dialog (gebaut 2026-10-08, nicht deployt)

- **Client:** `#create-target` (`app.html`, im `#create-dialog`) zeigt „Anlegen in: *Space*", im eigenen
  Home-Space mit dem Zusatz „(dein Home-Space)". Gefüllt in `openCreateDialog()` per `textContent` aus
  `state.activeSpace` — **dieselbe** Quelle, die der POST aus B1 als `space` sendet. Kein Server-Touch.
- **Datierte Korrektur 2026-10-08 (Code gewinnt):** P9-BH sagt, in der globalen Sicht oder in einem nur
  lesbaren Space stehe der Home-Space als Ziel da. Dieser Fall ist **unerreichbar**: dort ist der Dialog
  samt Knöpfen aus dem DOM ausgehängt (`setCreateControlsPresent(activeSpaceWritable())`), und
  `openCreateDialog()` bricht ohne Schreibrecht ab. Es gibt also keinen Dialog, der das Home-Ziel dort
  nennen könnte; die Zusage reduziert sich auf „der Dialog nennt das Ziel, wo er sich öffnen lässt".
  Für die **Übersicht** ist das nicht nur gelesen, sondern **gemessen**: dort bleibt `state.activeSpace`
  absichtlich stehen (`tree.js:66`), nach `team` → Übersicht ist er also `team` — Probe-Station S5 zählt
  trotzdem **0** sichtbare Anlegen-Knöpfe.
- **Belege:** Wächter `test_the_create_dialog_names_its_target_space` (gegen den alten Client rot), Probe
  **6/6 plus Messung S5** (S4/S4b neu, `probes/p9_feedback_b2_probe.json`), Gegenlauf **4/6 rot**, `pytest` **1253**, `ui_budget` 5/5, Tabu-Diff leer.

### E1a — Team-Spaces: verschieben, archivieren, löschen (gebaut 2026-10-08, nicht deployt)

- **Server (`api.py`):** `_is_team_space(space)` = keine Nutzerzeile (`auth_store.get_user(space) is None`) — dieselbe
  Nutzerverwaltung wie `_spaces_delete` (**V192 beantwortet**: die Nutzerverwaltung im Web-Prozess ist die Quelle, kein eigenes Feld
  auf der Platte). `_team_writer(actor, space)` verlangt zusätzlich **space-level** `can_write`. Die zwei
  Riegel (Ordner-PATCH und P9-K beim Löschen) bekommen diese Ausnahme. `team` steht in `/spaces` **und** `/overview`.
- **Client:** `spaceAllowsMove(space)` (`state.js`) = `own` oder (`team` und `writable`). Daran hängen `movable`
  (Strg+Klick, Long-Press, Verschieben, Löschen, Ziehen) und die Drop-Ziele im Baum. Der Löschdialog nennt
  „Zuletzt geändert von *X*" für Items außerhalb des eigenen Space (P9-BQ).
- **V191 beantwortet (am Code, in der Probe bestätigt):** Archivieren war in Team-Spaces schon frei — der
  Editor ist bei schreibbarem Item eingehängt, und `_items_archive` prüft nur `can_write_item_as_human`.
- **Befund aus der Browser-Probe, nicht aus dem Unit-Test:** das UI liest `state.spaces` aus `/overview`, nicht
  aus `/spaces`. Mit `team` nur in `/spaces` war der Unit-Test grün und die Probe rot (S8: 0 Löschknöpfe). Der
  Test prüft jetzt beide Antworten.
- **Datierte Abweichungen vom Plan (2026-10-08):**
  - **Space-Bindung beim Ziehen jetzt ausdrücklich** (`bindFolderDropTarget(button, spaceName, folderPath)`). Bis
    E1a war sie implizit: nur eigene Items waren ziehbar, nur der eigene Space war Ziel. Ohne die Prüfung
    landete ein Team-Item, auf einen Home-Ordner gezogen, als `folder`-PATCH **im Team-Space**. Jetzt: Toast,
    kein Schreibvorgang; ein Space-Wechsel bleibt dem Verschieben-Dialog.
  - **Freigeben bleibt beim eigenen Space.** E1 gibt Wegnehmen frei, nicht das Ändern fremder Sichtbarkeit.
  - **Ordner anlegen in Team-Spaces bleibt gesperrt** (`_spaces_create_folder`, `openNewFolderDialog` ist an
    `state.ownSpace` gebunden). Nicht im Plan genannt, also nicht gebaut — **offener Punkt für den
    Closeout/P10**. Ziehen und Verschieben in **vorhandene** Team-Ordner geht.
  - Zwei Step-D-Wächter in `test_static_routes.py` auf `spaceAllowsMove` und den Space-Namen umgeschrieben,
    **nicht gelöscht**; ihre Aussage (beide Drop-Aufrufe hinter **demselben** Riegel) bleibt.
- **Belege:** `pytest` **1260** (+7), Probe **11/11**, Gegenlauf gegen den Code vor E1a **4/4 rot**, Mutation
  ohne Home-Prüfung ⇒ P9-136-Test rot, `ui_budget` 5/5, Tabu-Diff §0.3 leer (nur `phase5_ui/webui/api.py`, wie
  §0.3 für E1 vorsieht).
- **Befund beim Abschluss (Advisor, gemessen, behoben):** ein `PATCH` mit `space` gleich dem **eigenen** Space des
  Items plus `folder` lief an beiden Prüfungen vorbei — P6-AE läuft nur bei echtem Wechsel, der Ordner-Riegel nur
  ohne `space`. Ein `share_write`-Halter konnte damit ein fremdes Home-Item umräumen (Test: **200**). Seit Step 7b
  (2026-08-17), nicht durch E1a. Fix: `space_change = target_space is not None and target_space != acl.space`, der
  Riegel greift bei `not space_change`. Stellt die fail-closed-Entscheidung vom 2026-08-12 wieder her.
- **`_is_team_space` liest die Nutzerzeile (`auth_store.get_user`), nicht `users.get()`:** Letzteres
  entschlüsselt den TOTP-Seed, und `/overview` läuft bei jedem Seitenaufruf (Hard Rule 1, Nachtrag 2026-07-30).
- **Step-D-Probe neu gefahren** (`bindFolderDropTarget` hat eine neue Signatur): **16/16** gegen den heutigen Code.
- **Offen für den Closeout, benannt:** MCP `update_item` behält den Ordner-Riegel ohne Team-Ausnahme
  (`phase2_mcp/` ist tabu) — Web und MCP folgen in Team-Spaces beim Ordnerwechsel **nicht** derselben Regel,
  anders als P9-BG beim Anlegen. Zusammen mit „Ordner anlegen in Team-Spaces" in die P10-Liste.
- **Nicht eingetragen:** V189–V194 stehen noch nicht in `ABNAHME_MATRIX_VERIFY.md` (B1/B2 haben sie dort auch
  nicht geführt). Nachtrag gehört in den Closeout.

### B3 — Schließen im Einstellungsmenü (gebaut 2026-10-08, nicht deployt)

- `#settings-menu-close` (`.btn`) in einer `.overlay__actions` unter den drei Menüpunkten; `settings.js :: init()`
  verdrahtet ihn auf `closeSettings` — die **ganze** Kette, wie P9-BN verlangt. Kein neuer CSS-Code: die Kette
  richtet `.overlay__actions` schon rechtsbündig aus (`.settings-chain .overlay__actions`).
- Belege: Wächter (ohne Fix rot), Probe S9 **12/12**, Gegenlauf alter Client S9 rot, `pytest` **1261**, `ui_budget` 5/5.
- **Für die Sichtprüfung:** der Knopf hat Standardhöhe und ist damit höher als die flachen Menüpunkte (P9-BB, 31,69 px).

### B4 — Abstand der Mitgliederzeilen (gebaut 2026-10-08, nicht deployt)

- `#space-member-list` ist eine Flex-Spalte mit `gap: var(--space)` (P9-BM); die bestehende Regel aus P9-AX
  trägt drei Zeilen mehr, es gibt weiterhin **genau eine** Regel für den Selektor.
- **Datierte Abweichung:** die Probe *legt kein Mitglied an*. Der Seed der Wegwerf-Instanz schreibt `team`
  mit `read`/`write: [alpha, beta]`, die Liste hat also vier Zeilen (beide Rollen je Principal) — das genügt, um
  die Grenze aus P9-107/P9-110 („Liste im Harness leer") zu schließen. Ein Anlegen bräuchte einen dritten Principal.
- Belege: Probe S10 **13/13**, Abstände [8, 8, 8] px; Gegenlauf `gap: 0` → S10 rot (Abstände [0, 0]); `pytest` **1261**.
- **Nachsatz 2026-10-08 (Sichtprüfung des Nikingers zu Bild B4):** „Entfernen" nahe am Text → rechtsbündig auf die Kante
  der Knöpfe darunter (`.space-member-row`: Flex, `space-between`, `gap`). Das hält auch das Fenster bei mittellangen
  Space-Namen stabil. Probe S10b 14/14, Gegenlauf rot.
