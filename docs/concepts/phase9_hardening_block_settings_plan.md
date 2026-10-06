---
status: live
purpose: "Mini-Plan P9 Block settings + Restposten — Einstellungen als Fensterkette (Menü → Unterfenster → Space-Detail), Passwort-Reihenfolge, V118 auf eine Linie, D1 neu beschrieben, P9-11 Portscan-Anleitung, Phasenabschluss. Locks P9-AE–P9-AL, Abnahme P9-83–P9-95, [VERIFY] V185–V188"
read-when: Bau des settings-Blocks, P9-11-Portscan, oder P9-Closeout nach dem 2026-10-05
detail: L2
up: ../../phase9_hardening/CLAUDE.md
down:
  - ./phase9_hardening_plan.md               # 📕 übergeordneter P9-Plan; §12.4 Übersichtsgrafik, P9-11, P9-27, P9-36
  - ./phase9_hardening_block_trace_plan.md   # 📕 Formvorlage dieses Mini-Plans
updated: 2026-10-05 (**§10 gebaut** — die sieben Punkte aus der Bildsichtung, opencode/M3, Probe **56/56**, G4 → 2 rot · G5 → 2 rot · G6 → 3 rot; P9-96–P9-102 mit **5 ✅ · 2 ⚠️**. **Zwei Korrekturen an diesem Plan, beide gemessen:** P9-APs `text-align` war auf einem Flex-Knopf ein **No-op** (Textmitte 8,5 px daneben) → `justify-content`; und das **linke Polster** musste vom 32-px-Wert der Baumzeile auf `--space` (Nikinger-Entscheidung), sonst bleibt die Beschriftung 12 px neben der Mitte. G6 trifft **P9-84**, nicht P9-97) | 2026-10-05 (**§10: sieben UI-Punkte aus der Bildsichtung, nicht gebaut** — Locks P9-AM–P9-AS, Abnahme P9-96–P9-102; zwei davon sind ausdrücklich „nicht anfassen"; zwei Folgen festgehalten: die zweite Vergleichsrichtung in P9-84 und der zu **eng** werdende Wächter) | 2026-10-05 (**gebaut, opencode/M3 — §9 gefüllt**; Release `v3.1.3` steht, nicht deployt; Probe 39/39, G1/G2/G3 rot, `pytest` 1223 → 1233 · **zwei Code-Befunde kamen aus dem Browser, nicht aus den Tests**, vier Punkte gegen den Plan abweichend begründet) | 2026-10-05 (geschrieben, Claude Code, nach dem Deploy `v3.1.2`; Wünsche und Entscheidungen des Nikingers vom selben Tag)
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
  auf V188. **[2026-10-05: ausgeführt]** — V188 ✅, Belege in §9 und in der P9-27-Zeile der
  `ABNAHME_MATRIX.md`. Die Zeile oben („meines Wissens **nur in Chromium**") ist damit **gemessen,
  nicht geglaubt**: MDNs `browser-compat-data` sagt `safari: false`.

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
   - **[2026-10-05, aus dem settings-Nachtrag]** die **leere Space-Liste beim zu frühen Öffnen**
     von „Spaces verwalten" (`renderSpaceList()` rendert aus `state.spaces`, das erst nach
     `loadOverview()` steht; §10.3 Punkt 2). Kein Test entscheidet die Form der Reparatur, und die
     Wahrscheinlichkeit wächst linear mit den sichtbaren Spaces — sie gehört an denselben Ort wie
     der P9-15-Befund, mit dem sie dieselbe Ursache hat.
   - **[2026-10-05, aus dem settings-Nachtrag]** das **lokale Vision-Modell** (`qwen3-vl:8b` aus
     Step C) **gegen eine Alternative stellen** — größeres multimodal, anderes Backend oder
     „Bilder gar nicht maschinell auswerten". Grund sind **zwei gemessene Fehlaussagen an einem
     Tag**: einmal eine Frage nicht beantwortet und dann behauptet, ein *Menüpunkt* sei markiert
     (es ist die Rail-Zeile), und einmal — bei einer **reinen Layout-Frage** — **drei Panels mit
     erfundenen Inhalten** („Übersicht", „alpha", „VERKNÜPFUNGEN") gemeldet, von denen **keines** im
     Bild steht. Die vollständige Fehler-Signatur und die Regel daraus stehen in
     `docs/concepts/sichtpruefung_automation_conventions.md`; **das Prüf-Muster ist dort
     festgehalten: eine Frage, deren Antwort man schon kennt.** Bis dahin gilt unverändert: Layout
     und Zustand in der Probe messen, Sichtung beim Nikinger.
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
| V188 | ✅ **beantwortet 2026-10-05, vier Quellen, eine am Repo gemessen.** Es ist **Betriebssystem-Verhalten** (macOS, bei Web-Vollbild: User-Agent), und die Seite kann es **nicht verhindern, höchstens verschieben** — und die Verschiebung existiert auf dem MacBook nicht. Die vollständige Beweiskette mit wörtlichen Zitaten steht in der P9-27-Zeile der `ABNAHME_MATRIX.md`; Kurzfassung unten (§9, „V188"). **P9-27 → ⚠️, D1 geschlossen, kein Code** (dieser Plan, §4) |

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

### V188 — die Frage aus §4, mit Quellen beantwortet (2026-10-05)

§4 („meines Wissens **nur in Chromium** und nur im Web-Vollbild") stand **aus dem Gedächtnis**.
Nachgelesen und **an einer Stelle gemessen** — die Beweiskette steht vollständig in der
P9-27-Zeile der `ABNAHME_MATRIX.md`, hier die Kurzfassung und die zwei Punkte, die überraschen:

1. **Der Anwendungsfall ist nicht einmal die Web-API.** `app.js:259` ist der einzige
   `fullscreen`-Bezug der ganzen App; die Web-Fullscreen-API wird nirgends aufgerufen. Der gemeldete
   Fall — grüner Knopf, Ctrl+Cmd+F — ist natives macOS-Vollbild, und **dafür gibt es keine
   Web-API**: `fullscreenElement` bleibt `null`, kein `fullscreenchange`. Der Guard `app.js:259`
   ist für genau diesen Fall ein No-op. Das stand in der Matrix bisher als Vermutung.
2. **Der Ausgang ist nicht abschaltbar, und das ist gewollt.** WHATWG Fullscreen §8 verlangt einen
   **immer wirkenden** Ausgang (*„a means of exiting fullscreen that always works … to prevent a
   site from spoofing the end user"*); WICG Keyboard Lock §7 (**MUST**) gilt auch dann, wenn die
   Seite *alle* Tasten anfordert. Die einzige Wirkung von Keyboard Lock ist eine **Verschiebung**:
   ESC-Tastendruck → langer ESC-Tastendruck (> 2 s, WICG §3.2/§7, WHATWG §6, MDN
   `Element.requestFullscreen()`).

Und die Verschiebung selbst ist im gemeldeten Fall doppelt unbrauchbar: **(a)** WICG §4.2 — Keyboard
Lock gilt nur für **JS-initiiertes** Vollbild, *„During F11 fullscreen, no Keyboard Lock processing
of keyboard events will take place"*; **(b)** Browser-Support **gemessen** an MDNs
`browser-compat-data` (`api/Navigator.json`, `api/Keyboard.json`): `navigator.keyboard`,
`Keyboard.lock` und `Keyboard.unlock` sind Chrome/Chromium ab 68, **`firefox: false`**,
**`safari: false`**. Die Plan-Formulierung „nur in Chromium" ist damit nicht widerlegt, sondern
**gemessen** — und für den Anwendungsfall schärfer: **gar nicht vorhanden**.

**Folge:** P9-27 ⬜ → ⚠️ (gegenstandslos, nicht erfüllt), D1 geschlossen, **kein Code** — genau die
Entscheidung aus §4, die nur unter dieser Bedingung gelten durfte. P9-28 bleibt ✅: dessen ✅ gilt
der Web-API-Seite des Guards, und das ist eine andere Frage.

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
- **V188** — ✅ **beantwortet 2026-10-05** (Quellen und Kurzfassung in §9). Die Seite kann das
  Beenden des nativen macOS-Vollbilds per ESC **nicht verhindern**; P9-27 steht auf ⚠️, D1 ist
  geschlossen, es wurde **kein Code** gebaut.
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

### Abnahme (P9-96 – P9-102), gefahren 2026-10-05 (§10.1)

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

### §10.1 Ergebnis — **gebaut am 2026-10-05 (opencode/M3), gleiches Release `v3.1.3`**

P9-96 – P9-102 stehen mit **5 ✅ und 2 ⚠️** in der Abnahmematrix. `pytest` **1233 → 1238** (5 neue
Tests, keiner umgedreht), `ui_budget` 5/5 (**165,6 KB**), Tabu-Diff §0.3 leer, Browser-Probe
**56/56** gegen die TLS-Wegwerf-Instanz auf 18775. Gegenläufe: **G4 → 2 rot · G5 → 2 rot ·
G6 → 3 rot**.

**Die beiden ⚠️ sind benannte Abweichungen, keine offenen Punkte** — P9-97 (linker Polsterwert,
Nikinger-Entscheidung) und P9-99 (der andere Weg zur Mitte). Beide sind in der Matrix mit ihrem
gemessenen Wortlaut begründet.

### §10.2 Was gegen diesen Plan anders gebaut wurde — fünf Punkte

1. **P9-AP ist `justify-content: center`, nicht `text-align: center` — und die Vorgabe im Plan
   war ein No-op.** Der Menüknopf ist `display: flex` (Sammelregel mit `.tree__folder`), sein
   einziges Kind ein **anonymer Flex-Item**. `text-align` wirkt auf Blockcontainer; im Flex-Item
   zentriert es einen Text in sich selbst. Die erste Fassung des Baus hatte genau das, und die
   erste Browser-Probe maß die Textmitte **8,5 px neben** der Knopfmitte. Der Wächter verbietet
   `text-align` in einer eigenen Menüpunkt-Regel jetzt ausdrücklich — eine Deklaration, die
   nichts bewirkt, ist die zweite Wahrheit über denselben Zustand.
2. **Das linke Polster ist `var(--space)`, nicht das der Baumzeile (32 px) — Nikinger-Entscheidung
   vom 2026-10-05, und der Grund steht im Lock P9-AN selbst.** Als `.tree__folder` erbte der
   Menüpunkt die Einrückung der Baumzeile; dadurch lag sein Inhaltskasten 12 px rechts, und
   `justify-content: center` zentrierte **darin** — Textmitte 732 px bei einer Knopfmitte von
   720 px, und der breiteste Menüpunkt hatte 0 px Spiel. Exakt mittig ging nur mit symmetrischem
   Polster; das war eine Frage an den Nikinger, Antwort: **beidseitig 8 px**. **Was das kostet,
   steht am Stylesheet und in S1:** der Menüpunkt ist in *diesem* Wert nicht mehr die Baumzeile
   (Höhe, Polster oben/unten, Schrift und Rundung bleiben es), und die Browser-Messung vergleicht
   den linken Wert jetzt gegen `--space` und **nennt die 32 px der Baumzeile mit**.
   *Nicht* gebaut wurde die Alternative, die Einrückung an der Quelle (`.tree__folder`) auf die
   Rail einzuschränken: das hätte zusätzlich die Space-Zeilen im Panel verschoben, eine zweite,
   nicht beauftragte Änderung.
3. **`border-color` ist als erlaubte Eigenschaft dazugekommen**, obwohl der Plan in der Liste der
   „neu zu untersagenden" Werte auch „Kante" nennt. P9-97 vergleicht aber ausdrücklich
   „Hintergrund **und** Kante", und ohne die Haarlinie wäre die Fläche nicht die des Eingabefeldes,
   sondern eine neue. Die **Kurzform** `border` bleibt verboten — sie trägt Breite und Stil und
   könnte damit genau die Geometrie verändern, die P9-AF bindet. Der Wächter prüft außerdem, dass
   der Flächenwert **derselbe Token** ist, den die `.input`-Regel nennt, und nicht bloß *irgendein*
   Wert: der Name wird verglichen, nicht abgetippt.
4. **„Erste Option" aus P9-101 wird als „erster sichtbarer Block unter dem Titel" operiert.** Im
   Harness steht der Home-Space-Hinweis vor der leeren Mitgliederliste, der Abstand zur ersten
   *Mitgliederzeile* wäre also Titel + Hinweis und damit eine andere Größe. Gemessen wird 24 px ==
   24 px; die Regel wirkt in beiden Lesarten, weil 24 px größer ist als das `margin-top: 1em` der
   `<ul>` (16 px) und der Titelabstand damit der einzige bestimmende Wert bleibt.
5. **Gegenlauf G6 macht nicht P9-97 rot, sondern P9-84.** Der Plan kündigte an, eine eigene Höhe
   treffe die Flächen-Vergleichszeile; getroffen wird die **Geometrie**-Vergleichszeile S1, weil
   eine Höhe kein Farbwert ist. Gemessen: **3 Stationen rot** (`S1 Menüpunkt 1/2/3 optisch =
   Baumzeile`, `h=40` gegen `h=35.69`). Die Plan-Aussage ist damit als *falsch benannt* korrigiert,
   nicht als unerfüllt.

### §10.3 Zwei Befunde aus dem Lauf, die keine Abnahmezeile sind

1. **Der gemeldete Überlauf von „Space entfernen" mit den „(schreiben)"-Zeilen war im Harness
   nicht vorhanden** (121 px Luft, gemessen), und eine rechte Ausrichtung kann einen vertikalen
   Abstand nicht verursachen. P9-102 steht deshalb auf ✅ **mit dem ausdrücklichen Vorbehalt**, den
   Block nicht als Behebung zu behaupten: die Sichtprüfung an den echten Spaces des Ningkers ist
   der fehlende Beleg. Zwei Lesarten bleiben offen (horizontaler Überstand einer langen
   Mitgliedszeile — die `<li>` hat keine eigene Regel und kein `word-break`; oder der Fall tritt
   erst mit vielen Mitgliedern auf, weil das Panel dann scrollt).
2. **Die Space-Liste kann leer bleiben, wenn man sie zu früh öffnet** — `renderSpaceList()` rendert
   aus `state.spaces`, und das steht erst nach `loadOverview()` fest; neu gerendert wird nur beim
   nächsten Öffnen. Die Wahrscheinlichkeit wächst **linear mit den sichtbaren Spaces** (P9-15). Im
   Harness mit zwölf Spaces ist das der Normalfall: der erste Lauf dieser Session maß S1 gegen eine
   **leere** Rail und meldete die Station rot, ohne dass sich am Menü etwas geändert hätte.
   **Gemeldet, nicht gebaut** — die Reparatur ist eine Zustandsentscheidung, keine Zeilenänderung.
   Die Probe wartet jetzt auf die **Bedingung** (dieselbe Lehre wie S7), nicht auf eine Uhr.


---

## §11 Zweite Bildsichtung 2026-10-05 — vier Punkte, **nicht gebaut**

**Anlass.** Der Nikinger hat die vier Bilder aus `screenshots_latest/` angesehen und vier Punkte
notiert; zu 02 und 03/04 kam eine Rückfrage mit gemessenen Alternativen, beide beantwortet. **Hier
steht nichts umgesetzt** — das ist der Auftrag. **Er dreht zwei Locks des §10 um**, und das ist der
wichtigste Satz in diesem Abschnitt.

| Lock | Inhalt | Herkunft |
|---|---|---|
| **P9-AU** | **Abstand zwischen den drei Menüpunkten**: `var(--space)` (8 px), derselbe Wert wie `#space-admin-list` (P9-AK). **Gemessen heute: 0 px** — „die shouldn't be glued to each other" | Nikinger 2026-10-05, Punkt 01 |
| **P9-AV** | **Die Fläche der Menüpunkte ist die des Standardknopfes, nicht die des Eingabefeldes.** Unausgewählt exakt `.btn` (`--btn-std-fill` + `--btn-std-line` + der 1-px-Innenschatten), ausgewählt die **Akzentfläche** wie `.btn-primary` (`--accent-face-*` + `--accent-edge`). Damit **widerrufen**: P9-AN (Eingabefeld-Fläche) und die Auswahl-Regel aus P9-AO | Nikinger 2026-10-05, Punkt 01 + Rückfrage; **Entscheidung ausdrücklich: „Standard-Knopf + Akzentfläche für ausgewählt"** |
| **P9-AW** | **„Ändern" wird Vorsicht** (`.btn.action--caution`, Standardfläche + rote Beschriftung — wortgleich „Archivieren"), weil ein Passwortwechsel Rückweg-Kosten hat (alle Connectoren neu autorisieren, andere Sitzungen abgemeldet — der Panel-Text sagt es selbst). **„Abbrechen" → „Schließen"**, wie in allen anderen Fenstern. **P9-AT („Passwort-Panel bleibt unverändert") ist damit für diese zwei Knöpfe aufgehoben** und für den Rest (Felder, Reihenfolge, Hinweistext) ausdrücklich **nicht** | Nikinger 2026-10-05, Punkt 02 |
| **P9-AX** | **Die Beschriftung der Space-Zeilen bündig mit dem Panel-Titel.** Gemessen: der Titel steht auf der Inhaltskante, die Zeilenbeschriftung **33 px** daneben (32 px geerbtes Einzugs-Polster der Baumzeile + 1 px Rahmen) — die Zeile hat **kein** Icon, die Einrückung ist also leer. **Dazu** `#space-member-list`: `list-style: none; padding: 0` (Browser-Standard sind Aufzählungspunkte **und** 40 px Einzug) | Nikinger 2026-10-05, Punkt 03 („align … I suggest actually moving them to the left too") |
| **P9-AY** | **Das Namensfeld im Detail-Panel steht beidseitig bündig mit der Zeile darunter** (Auswahl-Knopf links, „Hinzufügen" rechts). Gemessen: **222 → 234 px, also +12 px** (Rundwert des Nikingers: „+10px"). **Nicht als Zahl notiert**, sondern als Folge der Spaltenbreiten (siehe unten) | Nikinger 2026-10-05, Punkte 03/04 („by adding a few pixels on the left") |
| **P9-AZ** | **Die Anlege-Zeile im Spaces-Panel wird eine Zeile**: „Name des neuen Space" **und** „Space anlegen" nebeneinander, das Feld links **und** rechts bündig mit der Linie darüber, Standard-Abstand zwischen den Knöpfen. **„Schließen" bleibt allein darunter, rechtsbündig. „Space anlegen" behält seine Größe** — nur das Feld ändert seine | Nikinger 2026-10-05, Rückfrage, wörtlich |

### Warum P9-AY keine Zahl bekommt (und P9-AZ doch)

`#settings-space-detail` trägt **drei** Elemente in einer `flex`-Zeile, die umbricht: das Namensfeld
allein, darunter Auswahl-Knopf und „Hinzufügen". „Beidseitig bündig mit der Zeile darunter" heißt in
einem Flex-Umbruch: **das Feld so breit wie der Inhalt der Folgezeile**. Als Zahl notiert wäre
`width: 234px` eine Kopie von zwei Knopfbreiten, die sich bei jeder Beschriftungsänderung still
verschiebt. Als Raster ist es eine **Folge**: `grid-template-columns: repeat(2, max-content)` lässt
die beiden Spalten von den Knöpfen messen, und das Feld überspannt beide
(`grid-column: 1 / -1`). Der plus 12 px ist damit **gemessen und gerechnet**, nicht getippt.

P9-AZ ist der Fall, in dem die Folge **nicht** greift: dort ist die Folgezeile *ein* Knopf (142 px),
und das Feld daran zu binden hieße, ein Eingabefeld auf 142 px zu verengen. Deshalb dort
`flex: 1` auf dem Feld — eine Zeile, volle Inhaltsbreite, Feld und Knopf an den beiden Kanten.

### §11.1 Ergebnis — **gebaut am 2026-10-06 (opencode/M3), Release `v3.1.3` unverändert**

P9-103 – P9-111 stehen mit **9 ✅** in der Abnahmematrix, zwei davon mit benannter Grenze im Text.
Browser-Probe **`p9_settings_polish_probe.py` 29/29** gegen die TLS-Wegwerf-Instanz auf 18775,
**sechs Gegenläufe G7–G12, 6 von 6 wirksam**. `pytest` **1238 → 1246** (8 neue Tests, 5
umgeschrieben, keiner gelöscht), `ui_budget` 5/5, Tabu-Diff §0.3 leer. **Kein Deploy** — das
`deploy.sh`-Gate verlangt einen Datumsblock am Deploy-Tag.

**Ein eigenes Probe-Skript statt eines Umbaus von `p9_settings_chain_probe.py`, aus V187:**
*ein umgebauter historischer Beleg beweist nichts mehr über den Block, für den er steht*. Der
§10-Lauf ist der Beleg für P9-AN — die Fläche, die P9-AV am Folgetag widerrufen hat. Ein
umbauter Lauf hätte beides beweisen wollen.

#### Was gegen diesen Plan anders gebaut wurde — drei Punkte

1. **P9-AV brauchte zwei Flächen, nicht eine.** Der Plan-Entwurf (und die Rückfrage) sagten
   „Standard-Knopf **oder** Standard + Rail-Akzent"; die Antwort war *„Standard-Knopf +
   Akzentfläche für ausgewählt"*. Damit ist die Menüpunkt-Kette eine **eigene** Auswahlregel, und
   die Menüpunkte stehen **nicht mehr** in der Sammelregel mit der Baumzeile. Das ist mehr als
   „die Fläche tauschen": ein Träger in beiden Regeln hätte zwei Flächen an einem Zustand, und
   die spätere gewinnt still. Der Wächter `test_the_selection_state_uses_aria_current_and_the_
   existing_fill` prüft heute beides — dass die Menüpunkte **nicht** mehr den Rail-Fill tragen
   **und** dass die Baumzeile ihn behält.
2. **`box-shadow` und `color` waren im Wächter verboten und sind es heute in je einer Form.**
   Der 1-px-Innenschatten gehört zur Fläche des Standardknopfes — ohne ihn sähe der Menüpunkt
   flacher aus als „Schließen" im Nachbarpanel, und genau dieser Vergleich war der Auftrag. Die
   Schriftfarbe der Auswahlregel kommt aus `.btn-primary`, **gelesen** und nicht abgetippt; ein
   **äußerer** Schatten und eine eigene Schriftfarbe in jeder anderen Regel bleiben verboten,
   und die neue Ausnahme wird **zwei** Mal negativ geprüft (`_schatten_verstoss`,
   `test_the_menu_item_watchdog_bites_on_built_in_violations`).
3. **Der erlaubte linke Polsterwert ist je Selektor verschieden.** Der Menüpunkt trägt
   `var(--space)` (Nikinger-Entscheidung vom 2026-10-05, damit die mittige Beschriftung echt
   mittig liegt), die **Space-Zeile** `0` (P9-AX: bündig mit dem Panel-Titel). Ein **einziger**
   erlaubter Wert könnte nicht beides sein — die Liste `ERLAUBTES_PADDING_LEFT_PRO_SELECTOR`
   ist die kleinste Form davon.

#### Der Gegenlauf, der eine Messlücke fand (G11)

**Ohne `flex: 1` auf dem Anlege-Feld nimmt das Feld seine Eigenbreite (194,89 px), der Knopf
schrumpft auf 127,11 px** — und die Paarbreite ist wieder exakt die Inhaltsbreite, also sind
**beide** Bündigkeits-Stationen weiterhin grün. Der Lock verlangt aber zusätzlich wörtlich
*„Space anlegen in seiner Größe gleich lassen und nur das Eingabefeld in seiner Größe ändern"*,
und **das war nicht gemessen**. Die Station misst jetzt die Eigenbreite an einer Kopie
desselben Knopfes **außerhalb** der Flex-Zeile (`inline-block`, also Inhaltsbreite) — dieselbe
Technik wie der eingefügte Vergleichspunkt bei den Flächen. Danach ist G11 rot. **Ein
Gegenlauf, der grün bleibt, ist ein Befund: entweder ist der Lock falsch oder die Messung — hier
die zweite.**

### Abnahme (P9-103 – P9-111), gefahren 2026-10-06 (§11.1)

`P9-103` Abstand der drei Menüpunkte == `rowGap` von `#space-admin-list` (8 px), an **beiden**
Übergängen · `P9-104` unausgewählter Menüpunkt: berechneter Hintergrund **== der `.btn`-Regel**
(Token-Namen verglichen, nicht abgetippt) und Schatten == deren 1-px-Innenschatten · `P9-105`
ausgewählter Menüpunkt: berechneter Verlauf **== der `.btn-primary`-Regel**, Kante == `--accent-edge`
· `P9-106` `#account-submit` trägt `action--caution`, Farbe == die Vorsichtsfarbe, Fläche == die des
Standardknopfes (keine gefüllte rote Fläche), und im Passwort-Panel steht **kein** „Abbrechen" mehr ·
`P9-107` Beschriftung der Space-Zeile == linke Kante des Panel-Titels (±1 px, mit `Range` gemessen) ·
`P9-108` Detail-Panel: linke Kante des Namensfeldes == linke Kante des Auswahlknopfes **und** seine
rechte Kante == rechte Kante der Aktionszeile (±1 px) · `P9-109` Spaces-Panel: Feld und „Space
anlegen" auf **einer** Zeile (±1 px `top`), Feld links == Inhaltskante, Knopf rechts == Inhaltskante ·
`P9-110` `#space-member-list` trägt `padding-left: 0` **und** `list-style: none` · `P9-111`
**P9-96/98/99/100/101/102 halten**: Titelabstand 24 px, Auswahlzustand an `aria-current`, mittige
Beschriftung (0 px), Chevron-„Zurück", gemeinsamer Titelabstand, Knöpfe rechts.

Gegenläufe: `G7` P9-AU raus → P9-103 rot · `G8` Fläche zurück auf `--sunken` → P9-104 rot ·
`G9` „Schließen" zurück auf „Abbrechen" → P9-106 rot · `G10` `grid-column: 1 / -1` raus → P9-108 rot ·
`G11` `flex: 1` raus → P9-109 rot · `G12` `padding-left: 0` raus → P9-107 rot.

### Was an den Wächtern des §10 gekippt ist — und warum das kein Rot im Repo heißt

Vier Wächter aus `test_settings_chain.py` beziehen sich auf Locks, die dieser Block umdreht. Sie
werden **im selben Commit** umgeschrieben, mit beiden Lesarten und Datum im Docstring — nicht
gelöscht und nicht erst in einer späteren Session weggeräumt:

| Wächter | Wirkung |
|---|---|
| `test_the_unselected_menu_item_takes_the_input_surface_verbatim` | **umgedreht**: prüft jetzt den Standard-Knopf (`--btn-std-fill`/`--btn-std-line`, Token **aus der `.btn`-Regel gelesen**) und dass die Auswahlfläche die Akzent-Familie ist. Der Name wird nicht angefasst, der Docstring nennt P9-AN als die widerrufene Lesart |
| `test_the_selection_state_uses_aria_current_and_the_existing_fill` | **umgedreht**: `aria-current="true"` bleibt (Zustand), die **Fläche** ist jetzt bewusst eine andere als die der Baumzeile — mit Begründung, sonst wäre der Wächter eine Lüge |
| `test_settings_menu_items_reuse_the_tree_row_look` | **gelockert**: Höhe/Polster/Rundung/Schrift bleiben verboten (P9-AF gilt), `background`/`border-color` sind jetzt erlaubt (bis auf den Wert), und der bislang verbotene **Innenschatten** ist erlaubt, ein **äußerer** bleibt verboten |
| `test_only_the_settings_chain_aligns_its_buttons_right` | **unverändert gültig** — P9-AZ nimmt der Anlegezeile die Zweizeiligkeit, nicht ihre Rechtsausrichtung |


---

## §12 Dritte Bildsichtung 2026-10-06 — vier neue Punkte, **nicht gebaut**

**Anlass.** Der Nikinger hat die acht Bilder aus `screenshots_latest/` angesehen und **vier Punkte
freigegeben** (02, 03, 05, 06) und **vier neue notiert**. Dieser Abschnitt ist die Messgrundlage
des nächsten Blocks: jede Zahl ist heute gemessen, damit er nicht neu messen muss.

**Freigegeben:** `02 looks fine now` · `03 great` · `05 looks fine now` · `06 yes`.

| Lock | Inhalt | Herkunft | **Gemessen am 2026-10-06** |
|---|---|---|---|
| **P9-BA** | Die **Menüpunkte umklammern ihr Kästchen enger**: der Kasten folgt dem **eigenen** Label, nicht dem längsten der drei. Der Text bleibt, wo er ist; nur die rechte Kante rückt nach links | *„move the button borders a little bit further to the left, leave the text where it is now. Cut the not used space from the right"* (Bild 08) | **Alle drei Kästchen sind heute 131 × 35,69 px** (im Bild: Flächenläufe y 414–434, 457–479, 501–523, je x 655..785). Die **Beschriftungen** sind 106 / 113 / **77 px** ⇒ das Update-Log-Kästchen hat **19 px Leerraum je Seite**. Die **Höhe ist bei allen dreien gleich** (35,69 px), und im Bild 01 ist **nichts ausgewählt** (0 Akzentpixel) |
| **P9-BB** | Zu P9-BA gehört die Klärung von Bild 01: *„the update-log button is still bigger, I think you need to decrease its height"*. **Die Höhe ist nicht größer** (35,69 px wie die anderen) — „bigger" heißt am Bild **19 px Leerraum**, und „decrease its height" passt **nicht** zur Korrektur aus P9-BA (die ändert die Breite, nicht die Höhe) | Bild 01 | **Braucht eine Antwort in einem Wort:** (a) dieselbe Korrektur wie 08 (Kästchen enger), oder (b) die Knöpfe werden auch **flacher** (weniger Polster oben/unten, heute 6 px)? Ein „b" ohne Zahlen wäre eine dritte, nicht messbare Form |
| **P9-BC** | **Die Space-Zeilen dürfen ihr Kästchen ebenfalls enger ziehen** — im Bild 08 haben sie **184–239 px Leerraum rechts** (Kästchen 330 px, Beschriftung 1 px links am Inhalt) | *„cut the not used space from the right on that picture"* | Der **Text steht bereits bündig links** (1 px, P9-AX ✅); offen ist **nur die Kästchenbreite**. **Nicht** gebaut: `justify-content` rechts würde die Beschriftung verschieben, und genau das soll er **nicht** |
| **P9-BD** | **Bild 04: der Hinweis, wo die Member-Zeile steht.** Die „Hinzufügen"-Optionen **sind im Bild** — sie stehen im Detail-Panel **oben**, nicht unten | *„where did the space hinzufügen options go?"* | **Am eingecheckten Bild nachgewiesen:** Standardfläche bei **y 207..231, x 958..1181** (Auswahl + „Hinzufügen"), Beschriftung „lesen" bei y 218..233, „Hinzufügen" bis x 1165; das **Name-Feld** darüber (y 157..197, Platzhalter y 171..182); „Schließen" bei y 264..285. Im Browser: alle drei **sichtbar, im Viewport**, Panel **294 px** mit `scrollHeight == clientHeight` (kein Scroll). **Der Mitglieder-Bereich ist leer** (Home-Space, Höhe 0) — die Bedienung klebt deshalb direkt unter dem Hinweistext |

### Ein Punkt, an dem das Bild etwas zeigte, das die Messung nicht prüfte (07)

`I honestly don't see that` — die neue Space-Zeile war in der Messung **sichtbar** (Top 808,
Panel 32..868, `sichtbarImPanel: true`), aber das Panel **scrollt** (`scrollHeight` 1417 gegen
`clientHeight` 834, `scrollTop` 459 im Messlauf mit 27 Zeilen). **Im Probelauf mit 17 Zeilen ist
der Anlegepunkt der letzte**, und ein neu angehängter Eintrag landet damit **unterhalb des
Sichtbereichs** — das Bild kann die Zeile also gar nicht zeigen, egal wie bündig sie steht.
**Für den nächsten Block:** vor dem Screenshot **die neue Zeile in den Sichtbereich rollen**
(`scrollIntoView`), und das Checkkriterium nennt das Panel, in dem die Aussage steht — Bild 07
zeigt nach dem Klick auf die erste Zeile das **Detail-Panel**, nicht die Liste.

### Abnahme (P9-112 – P9-115), nicht gefahren

`P9-112` Jeder Menüpunkt ist **so breit wie sein eigenes Label plus Polster** (keine Streckung auf
den längsten Nachbarn), die Beschriftung bleibt auf ihrer Kante · `P9-113` Jede Space-Zeile zieht
ihr Kästchen auf die Beschriftung plus Polster zusammen, **Text unverändert** · `P9-114` Bild 04:
die Member-Zeile steht dort, wo das Bild sie zeigt (y 157..246 im 1440er Bild), und das Check-
kriterium nennt die Position · `P9-115` Bild 07: die neu angelegte Zeile ist **im Bild sichtbar**
(aufgerollt) und bündig mit dem Titel.
