---
status: live
purpose: "Mini-Plan P9 Block settings + Restposten — Einstellungen als Fensterkette (Menü → Unterfenster → Space-Detail), Passwort-Reihenfolge, V118 auf eine Linie, D1 neu beschrieben, P9-11 Portscan-Anleitung, Phasenabschluss. Locks P9-AE–P9-AL, Abnahme P9-83–P9-95, [VERIFY] V185–V188"
read-when: Bau des settings-Blocks, P9-11-Portscan, oder P9-Closeout nach dem 2026-10-05
detail: L2
up: ../../phase9_hardening/CLAUDE.md
down:
  - ./phase9_hardening_plan.md               # 📕 übergeordneter P9-Plan; §12.4 Übersichtsgrafik, P9-11, P9-27, P9-36
  - ./phase9_hardening_block_trace_plan.md   # 📕 Formvorlage dieses Mini-Plans
updated: 2026-10-05 (**§10: sieben UI-Punkte aus der Bildsichtung, nicht gebaut** — Locks P9-AM–P9-AS, Abnahme P9-96–P9-102; zwei davon sind ausdrücklich „nicht anfassen"; zwei Folgen festgehalten: die zweite Vergleichsrichtung in P9-84 und der zu **eng** werdende Wächter) | 2026-10-05 (**gebaut, opencode/M3 — §9 gefüllt**; Release `v3.1.3` steht, nicht deployt; Probe 39/39, G1/G2/G3 rot, `pytest` 1223 → 1233 · **zwei Code-Befunde kamen aus dem Browser, nicht aus den Tests**, vier Punkte gegen den Plan abweichend begründet) | 2026-10-05 (geschrieben, Claude Code, nach dem Deploy `v3.1.2`; Wünsche und Entscheidungen des Nikingers vom selben Tag)
---

# Phase 9 — Block settings und die Restposten bis zum Closeout

> **Ein Block plus Aufräumen, kein Phasenplan.** Anlass: Nikinger am 2026-10-05, nach `v3.1.2`.
> Er hat dabei drei Fragen der Phase beantwortet (V118, D1, Vorsicht-Kontrast) und einen
> Umbau des Einstellungs-Menüs gewünscht. **Nicht gebaut ist noch nichts.** Der Plan ist gegen
> `main@0639195` gelesen.

## §0 Rahmen

### 0.1 Auftrag

1. **Einstellungen als Fensterkette.** Ein kleines Menü öffnet Unterfenster **daneben**, und das
   Menü bleibt sichtbar. Aus „Spaces verwalten" öffnet ein Klick auf einen Space ein drittes
   Fenster.
2. **Drei kleine Entscheidungen umsetzen:**
   - V118: eine Linie statt zwei
   - D1: neu beschreiben
   - Vorsicht-Kontrast: bleibt so
3. **Phase 9 schließen:**
   - P9-11-Portscan (Nikinger, Anleitung §5)
   - Übersichtsgrafik
   - Doku-Drift
   - ROADMAP
   - Phase auf ✅

### 0.2 Gemessener Ausgangszustand (Code, `main@0639195`, read-only)

| Stelle | Heute |
|---|---|
| `app.html:487` `#account-dialog` | Titel **„Passwort ändern"**, darunter Hinweis, dann zwei `.btn.account-nav` (Update-Log, Spaces) in **voller Breite** mit Chevron, dann das Passwortformular |
| Formularreihenfolge | aktuelles Passwort → **TOTP** → neues → wiederholen |
| `app.js:85` | „Spaces verwalten" **schließt** das Konto-Fenster und öffnet `#space-admin-dialog` |
| `updates.js` | „Update-Log ansehen" öffnet `#update-log-dialog` als eigenes Overlay |
| `#space-admin-dialog` | Liste (Zeilen ohne Abstand), Anlege-Zeile, `<hr>`, Detail (`#space-detail`) **im selben Fenster** |
| `.overlay` / `.overlay__panel` (`app.css:1814`) | jedes Fenster = eigenes Vollbild-Overlay, Panel `width: 90%; max-width: 440px` |
| `.account-nav` (`app.css:708`) | `width: 100%` — **auch** vom Alte-Adresse-Dialog benutzt (`#legacy-host-link`) |
| `graph.js :: drawEdges()` | Tag-Kante + explizite Kante desselben Paars = **zwei** Striche; `test_graph_reload.py:182` nagelt das fest |

### 0.3 Scope

**Drin:**
- `app.html` (die drei Einstellungs-Overlays)
- `app.css` (Fensterkette, Größen)
- `app.js`, `dialogs.js`, `spaces.js`, `updates.js` (Öffnen/Schließen)
- `graph.js` (V118)
- die Tests dazu
- eine Browser-Probe

**Draußen:**
- jede API-Änderung — die Routen bleiben byte-identisch
- der Alte-Adresse-Dialog
- `#space-remove-dialog`: bleibt ein **modales** Bestätigungsfenster obendrauf (zerstörende Aktion, eigener Fokus)

### 0.4 Tabu

Plan §0.3 unverändert. Dazu kommen `phase5_ui/webui/api.py`, `security.py` und `phase4_auth/`: der
Block ist reines Frontend.

## §1 Gelockte Entscheidungen

| Lock | Inhalt | Herkunft |
|---|---|---|
| **P9-AE** | Das Menü heißt **„Einstellungen"**. Es trägt **keinen** Hinweistext und genau drei Knöpfe in dieser Reihenfolge: **Passwort ändern · Spaces verwalten · Update-Log**. „Spaces verwalten" bleibt hinter `meta.space_admin` (P7-R). | Nikinger 2026-10-05 |
| **P9-AF** | Die Menüknöpfe tragen die **Optik der Ordnerzeilen im Navigationsbaum** (`.tree__folder`, z. B. „Offen“ unter dem eigenen Space): dieselbe Höhe, Polster, Schrift und Rundung, und **derselbe Auswahlzustand** (`aria-current="true"` mit Kante und Fill), wenn das zugehörige Unterfenster offen ist. Untereinander, alle so breit wie das Menü-Panel, das selbst nach Inhalt breit ist. Die Klasse `.account-nav` fällt im Menü weg und bleibt nur am Alte-Adresse-Dialog. **[2026-10-05] Korrigiert:** die erste Fassung nannte „Verschieben“ (`.btn`); der Nikinger hat per Bild die Baumzeile gezeigt (V185 ✅). Umsetzung: die Regeln von `.tree__folder` **wiederverwenden** (gemeinsame Klasse oder Selektorliste), nicht kopieren. Eine Kopie wäre die „dritte Variante“, die P9 am 2026-10-01 bei `.account-nav` schon einmal entfernt hat | Nikinger 2026-10-05, mit Bild |
| **P9-AG** | **Fensterkette statt Overlay-Wechsel:** ein Overlay `#settings-overlay` mit **einer Reihe** von Panels nebeneinander. Stufe 1 ist das Menü, Stufe 2 das gewählte Unterfenster, Stufe 3 das Space-Detail. Ein Klick auf einen anderen Menüknopf **ersetzt** Stufe 2 und schließt Stufe 3. Der Knopf des offenen Unterfensters trägt den Auswahlzustand der Konvention (`aria-current`, `--select-fill`), damit man sieht, wozu das Fenster daneben gehört. | Nikinger 2026-10-05; Auswahl-Markierung: Konvention v3 (`phase8_ui_graph/CLAUDE.md`) |
| **P9-AH** | **Schließen von rechts nach links:** ESC schließt das **rechteste** Panel. Jedes Unterfenster hat sein eigenes „Schließen", das nur dieses Panel und alles rechts davon schließt. Das Menü schließt die ganze Kette. Der Klick auf den Hintergrund verhält sich wie bei jedem anderen Overlay heute. | Folgerung aus P9-AG; ESC-Kette wie `app.js:258 ff.` |
| **P9-AI** | **Schmale Fenster (< Summe der Panelbreiten, Richtwert 1024 px):** es bleibt nur das **rechteste** Panel sichtbar, mit einem „Zurück"-Knopf links oben. Kein Quetschen, kein horizontales Scrollen. **[2026-10-05] Bestätigt:** schmal nur das rechteste Panel, auf voller Breite alle drei. | Claude Code; dieselbe Regel wie P8.6 Plan 2 (≤ 1024 px: Liste **oder** Editor, nie beides) |
| **P9-AJ** | **Passwort-Reihenfolge:** aktuelles Passwort → neues → wiederholen → **TOTP zuletzt**. So ist der Code beim Absenden noch frisch. Der Hinweis zu Connectoren und Sitzungen wandert **in** dieses Unterfenster. Die Request-Form bleibt byte-identisch. | Nikinger 2026-10-05 |
| **P9-AK** | **Spaces-Unterfenster:** Zeilen mit sichtbarem Abstand (`gap: var(--space)`), zwischen Liste und Anlege-Zeile eine Trennlinie, **dasselbe `<hr>`**, das heute vor dem Detail steht. Ein Klick auf einen Space öffnet Stufe 3 mit Mitgliedern, Hinzufügen, Re-Auth-Feldern und „Space entfernen". Update-Log-Unterfenster: **Inhalt identisch**, nur der Ort ändert sich. | Nikinger 2026-10-05 |
| **P9-AL** | **Größen:** Panels nach Inhalt statt `90 % / 440 px`. Richtwerte: Menü `fit-content`, Passwort und Spaces etwa 320–360 px, Update-Log behält seine Lesebreite. Knöpfe in Panels nie `width: 100 %`. Die Werte legt der Bau gegen Bilder fest, nicht vorher. | Nikinger 2026-10-05 („viel breiter als nötig") |

**Und drei Antworten des Nikingers auf offene Fragen der Phase:**

- **V118 / P9-36 → eine Linie.** *„Wenn A auf B verlinkt, ist B für A automatisch relevant."*
  Gebaut wird das so: die **explizite** Kante gewinnt und bleibt durchgezogen. Implizite Tag- und
  Ordner-Kanten für ein Paar mit expliziter Kante entfallen **bei der Übernahme**
  (`rebuildImplicitEdges`), nicht erst in `drawEdges()`. Grund: die Gradzählung soll stimmen,
  dasselbe Argument wie `dedupeEdges()` (`graph.js:252`). Der Test
  `test_a_tag_edge_and_an_explicit_edge_draw_two_lines` wird **umgedreht und umbenannt**, mit Datum.
- **Vorsicht-Kontrast (Backlog B17 Punkt 3) → bleibt.** *„Einheitlich mit dem Rest, aber doch etwas
  eigen."* Der Backlog-Punkt wird geschlossen, mit Datum.
- **D1 / P9-27 → neu beschrieben.** Die Matrix-Fassung war falsch. Richtig ist: ESC schließt im
  macOS-Vollbildfenster das Item, **und zusätzlich** beendet macOS den Vollbildmodus. Siehe §4.

## §2 Verworfene Alternativen

- **Drei getrennte Overlays nebeneinander positionieren.** Drei Hintergründe übereinander dunkeln
  dreifach ab. Außerdem bräuchte jedes Overlay die Geometrie der anderen. Ein Overlay mit einer
  Flex-Reihe hat eine einzige Stelle für Layout und ESC.
- **Unterfenster als Akkordeon im Menü.** Das widerspricht dem Wunsch „Menü und Unterfenster
  sichtbar, nebeneinander".
- **`.account-nav` global umbauen.** Das träfe den Alte-Adresse-Dialog mit. Den hat der Nikinger
  heute gesehen und abgenommen.
- **V118 in `drawEdges()` filtern.** Das Bild wäre richtig, die Grad- und Nachbarzählung
  (`recomputeDegrees`) falsch. Dieselbe Falle hat P8.6-N schon einmal benannt.

## §3 Bauschritte (ein Commit für den Block, ein Release `v3.1.3`)

1. **Markup.**
   - `#settings-overlay` mit `.settings-chain` und vier Panels: `#settings-menu`,
     `#settings-password`, `#settings-spaces`, `#settings-space-detail`; dazu das Update-Log-Panel.
   - Die bestehenden IDs der Formularfelder, Listen und Knöpfe **bleiben**. JS und Tests hängen an
     ihnen.
   - `#account-dialog`, `#space-admin-dialog` und `#update-log-dialog` als eigene Overlays fallen weg.
   - Das Update-Banner („Alle Updates ansehen") öffnet die Kette direkt mit dem Update-Log-Panel.
     **[VERIFY] V186:** ob das Banner heute denselben Dialog öffnet.
2. **JS.**
   - Ein kleines Modul `settings.js` mit `openSettings(stage2?)`, `openPanel(name)`,
     `closeFrom(name)` und `closeRightmost()`.
   - `dialogs.js :: openAccountDialog`, `spaces.js :: openSpaceAdminDialog/selectSpace` und
     `updates.js` öffnen Panels statt Overlays.
   - `anyOverlayOpen()` und die ESC-Kette in `app.js` kennen die Kette als **ein** Overlay mit
     `closeRightmost()`.
3. **CSS.**
   - `.settings-chain { display:flex; gap; align-items:flex-start }`
   - Panels mit `width: fit-content` bzw. den Richtwerten aus P9-AL
   - Menüknöpfe als Spalte mit `width: 100%` **des Menü-Panels**, das selbst `fit-content` ist —
     so werden alle so breit wie der breiteste
   - Space-Zeilen mit `gap`
   - der Schmal-Modus aus P9-AI
   - **Kein neuer Farbwert:** Glas, Schatten und Auswahl-Fill kommen aus bestehenden Tokens
4. **V118.** In `rebuildImplicitEdges()` die Paare der expliziten Kanten als Set vorhalten und
   implizite Kanten dieser Paare verwerfen. Den Test umdrehen: `segments_in_last_frame == 1`,
   `duplicate_segments == 0`.
5. **Tests.**
   - `test_static_routes.py`: die Assertions auf die alten Overlay-IDs, auf `.account-nav` im Menü
     und auf die Feldreihenfolge **umschreiben, nicht löschen**. Jede alte Assertion bekommt eine
     neue mit derselben Absicht.
   - Neuer `test_settings_chain.py`:
     - Reihenfolge der drei Knöpfe
     - kein Hinweistext im Menü
     - TOTP-Feld nach den Passwortfeldern
     - `.account-nav` nur noch am Alte-Adresse-Dialog
     - ESC-Kette verdrahtet
   - **[VERIFY] V187:** welche Skripte in `phase8_6_ui_polish/scripts/` und
     `phase8_ui_graph/scripts/` die alten IDs ansprechen (gefunden:
     `p86_block_b_self_check.py`, `p8_16_glass_fallback_probe.py`). Es sind historische Proben; sie
     werden **nicht** umgebaut, bekommen aber einen datierten Kopfvermerk.
6. **Browser-Probe** `phase9_hardening/scripts/p9_settings_chain_probe.py` gegen die Wegwerf-Instanz
   (Port 18775, PID-Datei):
   - S1: Menü — drei Knöpfe, Reihenfolge, berechnete Höhe, Polster und Rundung gleich einer `.tree__folder`-Zeile (±1 px), aktiver Knopf mit derselben Kante und demselben Fill wie „Offen“
   - S2: Passwort daneben, Menü bleibt sichtbar, Knopf trägt `aria-current`
   - S3: Wechsel auf Spaces ersetzt Stufe 2
   - S4: Klick auf Space öffnet Stufe 3, drei Panels gleichzeitig sichtbar bei 1440 px
   - S5: ESC dreimal schließt von rechts nach links, das vierte Mal ist nichts mehr offen
   - S6: Passwortwechsel **echt** gegen die Wegwerf-Instanz (TOTP aus dem Wegwerf-Seed) → Toast, Sitzung bleibt
   - S7: Space anlegen erscheint in der Liste, Detail zeigt Mitglieder
   - S8: 1024 px — nur das rechteste Panel sichtbar, „Zurück" funktioniert
   - S9: V118 — eine Linie (der bestehende Harness aus `test_graph_reload.py`)

   **Bilder bei 1440 und 1024 px, angesehen.** Gegenläufe:
   - G1 `aria-current`-Setzen raus → S2 rot
   - G2 `closeRightmost` schließt alles → S5 rot
   - G3 implizite Kante nicht verworfen → S9 rot
7. **Release:**
   - `.rail__version` `v3.1.3` (Patch)
   - `UPDATE_LOG` mit Tagesdatum, je eine `- `-Zeile für Einstellungen, Passwort-Reihenfolge und die eine Linie

## §4 D1 / P9-27 — was sich ändert

Gemeldet war 2026-09-23: *„ESC im Vollbild schließt zusätzlich das Item."* Die Matrix las daraus
„ESC soll nur das Vollbild verlassen". Laut Nikinger heute ist das Verhalten so: **ESC schließt das
Item (gewollt), und macOS beendet dabei das native Vollbildfenster (der grüne Knopf).**

- **Ursache:** das native Vollbild ist ein Fensterzustand des Betriebssystems, nicht der
  Web-Fullscreen-API. ESC beendet es, bevor oder während die Seite das `keydown` bekommt.
- **Was eine Seite tun könnte:** ESC per Keyboard Lock API reservieren. Die gibt es meines Wissens
  **nur in Chromium** und nur im Web-Vollbild. **[VERIFY] V188**, aus dem Gedächtnis, nicht
  nachgelesen.
- **Entschieden (Nikinger 2026-10-05): kein Code.** P9-27 wird zu einem `[VERIFY]`-Eintrag mit
  dieser Aufgabe: **belegen, dass das macOS-Verhalten ist, auf das die Seite keinen Einfluss hat**
  (V188). Danach geht die Phase weiter. D1 ist damit geschlossen, und P9-27 wird ⚠️ mit Verweis
  auf V188.

## §5 P9-11 — Portscan (Nikinger, MacBook, Firmen-VPN aus, Handy-Hotspot)

Der Hotspot macht das MacBook zu einem Rechner **außerhalb** des Heimnetzes. Werkzeug:
`brew install nmap`. Vier Ziele, jedes mit erwartetem Ergebnis:

| # | Ziel | Netz | Kommando | Erwartet | Warum |
|---|---|---|---|---|---|
| 1 | Öffentliche Ausgangs-IP der Heim-VM | Hotspot, Tailscale **aus** | `nmap -Pn -T4 176.2.220.64` | alles `filtered`, **kein** `open` | Die IP ist die Carrier-NAT-Adresse (CGNAT), heute von der VM gemessen. **Sie wechselt:** am Scan-Tag auf der VM neu holen mit `curl -s https://ifconfig.me` |
| 2 | VPS | Hotspot, Tailscale **aus** | `nmap -Pn -T4 217.160.128.146` | **nur** 80 und 443 `open`; 22 nicht `open` (SSH läuft übers Tailnet) | Der VPS ist die einzige öffentliche Fläche. Jeder dritte offene Port ist ein Befund |
| 3 | LAN-Adresse der VM | **Heim-WLAN**, Tailscale aus | `nmap -Pn -p 8765,8000-9000 192.168.68.175` | 8765 **nicht** `open` | Die App bindet `127.0.0.1`, der Relay nur die Tailnet-IP (P3-B) |
| 4 | Tailnet-Adresse der VM | Hotspot, Tailscale **an** | `nmap -Pn -p 8765 100.93.43.122` | `filtered` **oder** `open` — beides wird notiert | Die ACL erlaubt 8765 nur `tag:sharefyx-edge` (dem VPS). `filtered` vom MacBook wäre der fehlende **Gegenlauf zu V162 (Lesart B)** |

**Ergebnis zurück** als Ausgabe der vier Läufe. Eingetragen wird es in die Matrix: P9-11 ✅ oder
Befund. V162 B bekommt einen Vermerk.

## §6 Closeout (Claude Code, nach Block und Scan)

1. **Doku-Drift beheben, datiert:**
   - Root-Block und Matrix-Kopf nennen P9-15 noch „Arbeit der nächsten Session". Die Zeile selbst
     ist ⚠️ und am 2026-10-03 gemessen.
   - Die Root-Zahl „71 ✅ · 10 ⚠️ · 2 ⬜" weicht von der Matrix ab („71 · 9 · 3"). **Die Matrix
     gilt.**
   - `ROADMAP.md`-INDEX-Zahl (P9-6) nachziehen.
2. **Übersichtsgrafik** `docs/concepts/phase9_hardening_uebersicht.svg`, mit
   `~/.claude-code-tools/` gerendert und **angesehen**.
3. **ROADMAP-Zeile P9 → ✅.** Die P10-Liste übernimmt:
   - P9-13/V150 (zweites Konto)
   - die `/api/v1/overview`-Schleife (P9-15-Befund)
   - den Termin „alte Adresse wieder befristen", sobald der Arbeitslaptop die neue Domain erreicht
     (Vermutung: NRD-Sperre etwa 30 Tage, erneut testen um den 2026-11-02)
4. **Plan §9-Ergebnis** dieses Mini-Plans füllen, dann 🔄 → 📕.

## §7 Abnahme (P9-83 – P9-95)

`P9-83` Menütitel „Einstellungen", kein Hinweistext ·
`P9-84` drei Knöpfe in der Reihenfolge aus P9-AE, Standard-`.btn`-Höhe, nicht volle Breite ·
`P9-85` Unterfenster öffnet **neben** dem Menü, Menü bleibt sichtbar, aktiver Knopf markiert ·
`P9-86` Knopfwechsel ersetzt Stufe 2 ·
`P9-87` Space-Klick öffnet Stufe 3, drei Panels bei 1440 px sichtbar ·
`P9-88` ESC und „Schließen" schließen von rechts nach links ·
`P9-89` ≤ 1024 px nur das rechteste Panel plus „Zurück" ·
`P9-90` Passwort: alt → neu → wiederholen → TOTP, Wechsel live gegen Wegwerf grün ·
`P9-91` Space-Zeilen mit Abstand, Trennlinie vor der Anlege-Zeile, Update-Log-Inhalt unverändert ·
`P9-92` keine Knöpfe mit leerem Überraum (Bilder angesehen), Alte-Adresse-Dialog unverändert ·
`P9-93` V118: eine Linie, Gradzählung ohne implizite Doppelkante, Test umgedreht ·
`P9-94` P9-11 vier Läufe eingetragen ·
`P9-95` `pytest` ≥ 1223 + neue, `ui_budget` 5/5, Gegenläufe G1–G3 rot, Tabu-Diff leer

## §8 `[VERIFY]`

| Nr. | Frage |
|---|---|
| V185 | ✅ **beantwortet 2026-10-05:** gemeint ist die Baumzeile `.tree__folder` („Offen“), nicht „Verschieben“ — Bild des Nikingers. P9-AF ist danach korrigiert |
| V186 | Öffnet das Update-Banner heute `#update-log-dialog` (dann muss es die Kette öffnen)? |
| V187 | Welche historischen Proben sprechen die alten Overlay-IDs an? |
| V188 | **Belegen, dass das Beenden des macOS-Vollbilds per ESC Betriebssystem- bzw. Browser-Verhalten ist und die Seite es nicht verhindern kann.** Quelle nennen (Apple/WebKit-Doku oder Spezifikation der Keyboard Lock API mit Browser-Support). Kein Code, keine Heuristik — Nikinger 2026-10-05 |

## §9 Ergebnis

**Gebaut am 2026-10-05 (opencode/M3), Release `v3.1.3` steht, nicht deployt.** P9-83 – P9-93 ✅,
P9-95 ✅, **P9-94 ⬜** (Portscan — Nikinger-Schritt, §5). `pytest` **1223 → 1233**, `ui_budget` 5/5
(163,4 KB), Tabu-Diff §0.3 leer, Browser-Probe **39/39** gegen die TLS-Wegwerf-Instanz auf 18775,
Gegenläufe **G1 → 4 rot · G2 → 2 rot · G3 → rot**.

### Was gegen den Plan anders gebaut wurde — vier Punkte, jeder mit Grund

1. **V118 wird in `rebuildImplicitEdges()` gefiltert, nicht in `drawEdges()`** (Plan §3 Schritt 4
   sagte es bereits so — hier bestätigt). Der Grund ist im Docstring von `graph.js` und im
   `graph_reload_probe.mjs` festgehalten: die Gradzählung läuft über
   `explicitEdges.concat(implicitEdges)` und `drawNodes()` skaliert den Radius danach. Ein Filter
   erst beim Zeichnen hätte das Bild richtig und die Zählung falsch gelassen.
2. **Ein Öffner statt drei Listener** (nicht im Plan). Beim Bauen hingen **zwei** `click`-Listener
   auf `#account-manage-spaces`: `app.js` öffnete, `settings.js` schaltete um. Der Knopf hätte sich
   nie geschlossen. Jetzt hört nur `settings.js` zu, und die drei Eigentümer liefern ihren
   Zustands-Reset über `registerPanel(name, prepare)`. Wächter:
   `test_only_one_module_opens_a_panel`.
3. **„Zurück" ist in JEDER Stufe verdrahtet, auch in Stufe 3.** Im Plan steht der Knopf nur beim
   Schmal-Modus; die erste Fassung nahm `space-detail` aus der Verdrahtung aus, und die Browser-Probe
   S8 meldete ihn als **toten** Knopf — im Schmal-Modus ist das Detail das einzige Panel, also war
   der Knopf der einzige Weg zurück. Wächter: `test_every_stage_has_a_wired_back_button`.
4. **Der Schmal-Modus braucht Zwei `:has()`-Regeln, nicht eine** (nicht im Plan). Die erste Fassung
   blendete nur das Menü aus; bei offenem Detail blieben Spaces-Liste **und** Detail stehen — genau
   die zwei Panels, die P9-AI verbietet. „Welches Panel ist das rechteste" steht im Zustand
   (`hidden`), nicht im Markup, weil das Menü im DOM zuerst steht.

### V186 — die Antwort auf eine Frage, deren Antwort im Plan schon falsch stand

Das Update-Banner öffnet das Log **nicht**: es trägt nur „Verstanden" (`#update-banner-dismiss`).
Plan §3 Schritt 1 sprach von einem „Alle Updates ansehen" — eine Annahme über ein Bedienelement,
das es nicht gibt. Der einzige Weg ins Log ist der Menüpunkt.

### Zwei eigene Fehler, die die Wächter erst beim Bauen gefunden haben

- **Der Gegenlauf hat den eigenen Messaufbaum widerlegt** (G3). `graph_reload_probe.mjs` las den
  Frame **nach** dem Zurückschalten des Tag-Toggles — also einen, in dem die Zwillingskante nicht
  mehr existiert. Der Test wäre mit dem Filter **aus** grün gewesen. Behoben durch
  `frames` im Shim (`clearRect()` ist die echte Frame-Grenze) und durch das Sichern der Frames
  **vor** dem Toggle-Zurückschalten. Das ist dieselbe Fehlerklasse wie der 2026-10-02 eingecheckte
  Gegenlauf-Beleg: die Messung lief, aber an der falschen Stelle.
- **Der Schmal-Modus-Test prüfte eine Breite, die von der Antwort abhing.** `strokes.slice(-2)` →
  `slice(-1)`: die Schnittlänge war die *erwartete* Anzahl Linien. Jetzt wird der Frame gelesen,
  nicht geraten.

### Wächter, die umgeschrieben statt gelöscht wurden

`test_app_html_has_a_live_manage_spaces_entry` (Chevron-Assertion entfällt, `disabled`/`Phase 7`
bleiben wörtlich) · `test_account_nav_and_standard_button_wear_the_rail_selection_look` (jetzt nur
noch die `.btn`-Hälfte) · `test_account_nav_stays_layout_only_on_the_legacy_dialog` (neu, prüft
zusätzlich „genau ein Träger") · `test_1024_breakpoint_has_single_row_no_map` und zwei Nachbarn
(die 1024er Media-Query wird jetzt **alle** gelesen, nicht die erste — es gibt seit diesem Block
**zwei**).

### Offen

- **P9-94 / P9-11** — der Portscan (§5). Vier Läufe vom MacBook, Handy-Hotspot. **Von keinem
  Test ersetzbar** und deshalb ⬜, nicht ⚠️.
- **V188** — das Beenden des macOS-Vollbilds per ESC belegen. **Kein Code.** Der Keyboard-Lock-Weg
  steht in der Matrix als *aus dem Gedächtnis, nicht nachgelesen*; P9-27/D1 bleibt ⚠️, bis eine
  Quelle vorliegt.
- **Deploy `v3.1.3`** — Badge und `## 2026-10-05`-Block stehen. `deploy.sh` verlangt einen
  Datums-Block am Deploy-Tag; dieser Eintrag ist vom 2026-10-05, ein späterer Deploy braucht
  `SHAREFYX_ALLOW_STALE_UPDATELOG=1` oder einen neuen Block.

---

## §10 Nachtrag 2026-10-05 — UI-Rückmeldung nach der Bildsichtung, **nicht gebaut**

**Anlass.** Der Nikinger hat die sieben Probe-Bilder angesehen (der sechste war für das lokale
Vision-Modell nicht beantwortbar, siehe §9) und sieben Punkte notiert. **Hier steht keiner davon
umgesetzt** — der Block ist abgebaut und committet (`543f3a0`), dieser Nachtrag ist der Auftrag
für den nächsten Block. **Zwei der sieben Punkte sind ausdrücklich „gut, nicht anfassen"**; die
stehen hier, damit niemand sie später für verbesserlich hält.

| Lock | Inhalt | Herkunft |
|---|---|---|
| **P9-AM** | Der Titel **„Einstellungen" wird zentriert**, und der Abstand zwischen Titel und erstem Knopf wird **etwas größer** — **ein** Wert, an **zwei** Stellen im Stylesheet, nicht zweimal notiert (dieselbe Regel wie P9-AF: ein kopierter Wert ist der Beginn der dritten Variante) | Nikinger 2026-10-05 |
| **P9-AN** | **Unausgewählte** Menüpunkte bekommen die Fläche des Eingabefeldes (`.input`, im Panel „Name des neuen Space" genau so im Einsatz) — „leicht abgesetzt vom Fensterhintergrund, aber keine Plastik". **Nur die Fläche wechselt: Höhe, Polster, Schrift und Rundung bleiben exakt die der `.tree__folder`-Zeile** (P9-AF gilt unverändert). Gelesen als: die *Geometrie* wird weiterverwendet, die *Fläche* nicht | Nikinger 2026-10-05 („ich würde vorschlagen" — **Lesart, im Bau am Bild prüfen**) |
| **P9-AO** | **Ausgewählte** Menüpunkte behalten den heutigen Auswahlzustand unverändert: `aria-current="true"` + `--select-fill` + Kante. Kein neuer Wert, keine Änderung an der einen Regel | Nikinger 2026-10-05 |
| **P9-AP** | Der Text in den Menüknöpfen wird **zentriert** (heute `text-align: left` aus der Sammelregel) — die Beschriftung soll mittig in der Fläche stehen, nicht links | Nikinger 2026-10-05 |
| **P9-AQ** | Der „Zurück"-Knopf bekommt ein **echtes Icon** statt des Textpfeils, **horizontal zentriert**. Der Textpfeil `&larr;` hängt sichtbar nach unten (Glyphe, nicht Baseline) | Nikinger 2026-10-05 |
| **P9-AR** | Im Detail-Panel: **mehr Abstand** zwischen dem Space-Titel und der ersten Option — **derselbe** Wert wie in P9-AM. Der Titel stand bisher direkt über der ersten Zeile, ohne Trennung | Nikinger 2026-10-05 |
| **P9-AS** | **Alle Knöpfe in den Einstellungs-Fenstern werden rechts ausgerichtet** (`justify-content: flex-end` in den `.overlay__actions` **der Kette**), nicht in den anderen Overlays. Damit ist der Überlauf von „Space entfernen" mit den „(schreiben)"-Zeilen der Mitgliederliste weg, den er gemeldet hat | Nikinger 2026-10-05 |
| **P9-AT** | **Passwort-Panel und Update-Log-Panel bleiben unverändert.** Wörtlich seine Worte: *„great, as well as the update log"*. Der Lock existiert, damit ein späterer „aufräumen"-Impuls diese beiden Fenster nicht anfasst | Nikinger 2026-10-05 |

### Zwei Folgen, die man kennen muss, bevor man anfängt

1. **P9-84s Messung ändert ihren Gegenstand, nicht ihre Höhe.** Die Browser-Probe vergleicht
   heute die Menüpunkte mit einer echten `.tree__folder`-Zeile (Höhe, Polster, Schrift, Rundung).
   Nach P9-AN bleibt diese Messung **richtig** — die Geometrie ist unverändert. Neu ist eine
   **zweite** Vergleichsrichtung: unausgewählt gegen die Fläche des Eingabefeldes, ausgewählt gegen
   die aktive Baumzeile. Zwei Vergleiche, zwei Ziele; der erste darf nicht wegfallen, sonst
   bestünde der Block die Wiederverwendung nicht mehr.
2. **Der Wächter `test_settings_menu_items_reuse_the_tree_row_look` muss **enger** werden, sonst
   geht er an korrektem Code rot.** Er verbietet heute u. a. `background` in einer *eigenen* Regel
   für `.settings-menu__item` — genau das fordert P9-AN. Die Absicht des Wächters ist „keine
   **eigene Optik** für die Geometrie"; nach P9-AN ist eine eigene *Fläche* gewollt. **Neu zu
   untersagen** bleiben Höhe, Polster, Rundung, Schrift, Farbe des Textes, Kante, Schatten;
   **neu erlaubt** sind `background` (nur aus den vorhandenen Tokens, kein neuer Wert) und
   `text-align` (P9-AP). **Die Änderung gehört in denselben Commit wie der Bau** — ein Wächter,
   der eine Woche zu eng war, meldet in der Zwischenzeit berechtigt rot und wird dann
   weggeräumt, statt korrigiert.

### Das Icon aus P9-AQ gibt es noch nicht — und genau so soll es entstehen

Der Sprite (`app.html`, `<!-- ICONS:BEGIN -->`) kennt `i-chevron-right` (`<path d="m9 18 6-6-6-6" />`),
aber **kein** `i-chevron-left`. **Neu:** `i-chevron-left` als Spiegel davon,
`d="m15 18-6-6 6-6"`, gleiche `viewBox`. **Nicht** `i-log-out` wiederverwenden (Kreis mit Pfeil nach
oben links — das ist Abmelden, und die Verwechslung wäre billig) und **nicht** das Chevron
drehen (die Icons werden überall als `<use href>` eingebunden, eine `transform`-Regel müsste in
`icons.js` und würde jeden Träger treffen). Der Knopf wird ein Icon-Knopf mit `aria-label`
— die Beschriftung „Zurück" darf als Text weg, **die Zugänglichkeit nicht**: `.btn--icon` trägt
den Titel, und genau diese beiden (`title` + `aria-label`) sind zu setzen.

### Abnahme (P9-96 – P9-102), nicht gefahren

`P9-96` Menütitel zentriert, Abstand Titel→erster Knopf == der in P9-AR gemessene Wert (±1 px) ·
`P9-97` unausgewählter Menüpunkt: gleiche berechnete Fläche wie `#space-create-name-input`
(`background-image`/`background-color`/Kante), **Geometrie unverändert** gegen die Baumzeile ·
`P9-98` ausgewählter Menüpunkt trägt weiter `--select-fill`, byte-gleich zur heutigen Regel ·
`P9-99` `text-align` der Menüpunkte berechnet `center` · `P9-100` Back-Knopf enthält
`<use href="#i-chevron-left">` und **keinen** `←`-Text mehr, Icon zentriert, `aria-label` gesetzt ·
`P9-101` Abstand Space-Titel↔erste Option == Abstand Menü-Titel↔erster Knopf · `P9-102`
`.overlay__actions` **innerhalb der Kette** `justify-content: flex-end`, und die Bounding-Boxen von
„Space entfernen" und der letzten „(schreiben)"-Zeile **überlappen sich nicht** (≤ 0 px).

Gegenläufe für den Bau: `G4` P9-AP raus (Text wieder links) → P9-99 rot · `G5` P9-AS raus
(Buttons wieder links) → P9-102 rot · `G6` P9-AN **mit** einer eigenen Höhe → P9-97 rot.
