---
status: snapshot
purpose: "Abschluss-Handover P10.5 → P11: Status, Delta seit dem P10-Handover, das Leitziel von P11 (Writer-Optik bei Markdown-Kern — technisch nicht erfüllt), alle P11-Vormerkungen mit Fundstelle, Lage des Editor-Plans, offene Entscheidungen, [VERIFY]-Bilanz, Hinweise für den P11-Planer. Closeout Z 2026-11-07, formaler Schluss beim Nikinger; live ist v4.0.2."
read-when: zu Beginn der P11-Planung einmal ganz lesen — vor dem Editor-Plan (§5/§8) und dem Register; ersetzt das Nachlesen von Phase-Head und SESSIONS_ARCHIVE für alles außer der Detailhistorie
detail: L2
up: ../../ROADMAP.md
down:
  - ../../phase10_5_finishing/CLAUDE.md            # Head: Modulstatus 0–19/Z, Deploys A–F, „Offen beim Nikinger"
  - ./phase10_5_editor_4_1_plan.md                  # 📗 Editor-Plan: S3a–S11 = P11 Block 1, Entscheidungen §8
  - ../../phase10_inventory/BAUSTELLENREGISTER.md   # 📗 Register: die P11-Zeilen, AL-1
  - ./phase10_5_finishing_uebersicht.svg            # Übersichtsgrafik
updated: 2026-11-07 (angelegt — Closeout P10.5, Block Z; Nachtrag des Nikingers zum Editor eingearbeitet)
---
# Phase 10.5 — Closeout-Handover (P10.5 → P11)

> **Phase 10.5 ist fertig** (Closeout Z 2026-11-07; den formalen Schluss in `ROADMAP.md` und Wurzel-`CLAUDE.md`
> bestätigt der Nikinger). Abnahme **86 ✅ · 0 ⚠️ · 0 ⬜ von 86**, P10-J live belegt, live läuft **`v4.0.2`** (`d2ca573`).
> **Aber ein Soll ist technisch nicht erfüllt, und es war nie ein Abnahmemaß:** der Editor sieht nicht aus wie ein
> Textverarbeitungsdokument, sondern wie eine Markdown-Datei (Nikinger, 2026-11-07). Das ist das **Leitziel von P11** (§2).

## 1 Status in acht Sätzen

1. **Umfang:** 2026-10-22 bis 2026-11-07, **169 Commits** (`d5f6081..8247fc8`; die Plan-Commits `f6cbf3c`/`97d8f64` zählen zu P10).
   `pytest` **1268 → 1939**, `ui_budget` 5/5 → **6/6**, `doc_health` 0.
2. **Register (die Arbeitsliste, P10-B):** 49 P10.5-Zeilen, **48 ✅ · 1 ⬜** — offen nur **AL-1 Zeile 15** (Migration + Live-Check
   beim Nikinger). Fünf Zeilen standen veraltet auf ⬜ und sind im Closeout nachgezogen (PF-3, PA-7, KA-1, ED-1, UI-4; datiert).
3. **Abnahme:** geplant **61** Zeilen, am Ende **86** (+25 aus den Blöcken 13–19). Alle ✅, **0 ⚠️**. Gezählt ist nur, was
   gemessen wurde — die Writer-Optik war keine Zeile (§2).
4. **P10-J erfüllt:** ein Nicht-Claude-Client (opencode 1.18.33) führt live `list_spaces` aus, mit **zwei Modellanbietern**:
   MiniMax M3.1 Flash (gehostet, P10.5-27) und Ollama auf CT 111 (`qwen3-vl:8b`, Zusatzlauf `gpt-oss:20b`, P10.5-28).
   Danach ein Schreibtest: alle drei Modelle legten je ein Item an (vom Nikinger archiviert).
5. **Live:** `v3.1.4` → **`v4.0.2`** über die Deploys A, B, D, E, F (C nie einzeln ausgeliefert, in D enthalten). Der Sprung auf
   `v4.0.0` war die Entscheidung des Nikingers (2026-10-26, „große Änderung").
6. **Sieben Blöcke kamen ungeplant dazu (13–19)** — Aufträge des Nikingers, ein neues Kartenlayout, die Fixes aus dem
   Ultra-Review, ein Launch-Film, die Live-Funde nach Deploy D und ein Editor-Hotfix. Sie sind mehr als ein Drittel der Phase.
7. **Das Ultra-Review vor `v4.0.0`** fand **22 Befunde, einer kritisch** (B1: Pfad-Traversal über `asset_id`, **live seit
   2026-08-20**). B1–B10 sind vor Deploy D behoben (Block 15), B11–B22 sind Backlog (§6).
8. **Der Editor:** Tabellen sind seit `v4.0.2` im eigenen Editor wieder Tabellen (Widget, P10.5-85). Alles Weitere zum
   Editor ist P11 Block 1 (`v4.1.0`, Minor-Sprung vom Nikinger schon entschieden).

## 2 Leitziel P11: Writer-Optik bei Markdown/HTML-Kern

**Das Soll (Nikinger, 2026-11-07):** der Editor sieht aus wie ein **Word- oder LibreOffice-Writer-Dokument**. Die gespeicherte
Datei bleibt **Markdown/HTML** (Hard Rule 2: Dateien sind die Wahrheit; der Byte-Vertrag V1–V6 aus P10.5-86 gilt weiter).
**Heute ist das technisch nicht erfüllt.** Der Nikinger beschreibt drei Bilder (sie liegen nicht im Repo):

| Bild | Beobachtung | Was der Editor-Plan dazu gemessen hat |
|---|---|---|
| 1 gpt-oss-Testnotiz | Tabelle richtig (Widget), der Text darüber in **Festbreitenschrift** | **F11**: Editor Plex Mono 13 px, Lesesicht Plex Sans 16 px → **S5a** |
| 2 Link | `[Vorgabe](#item/itm_e75266f2)` als Rohsyntax mit Klammern und Adresse (in der Cursorzeile) | das Hybrid-Prinzip von CM5 zeigt die Marker der **Cursorzeile** absichtlich — siehe unten |
| 3 „Executor-Bake-off" (lange echte Notiz) | `# ` sichtbar, durchgehend Festbreitenschrift, ungleiche Einrückungen, weiße Kästchen statt Aufgabenzeichen, breite Tabelle läuft rechts über den Bildrand (ob Bildausschnitt oder Widget-Breite: **nicht geprüft**) | **F11** (Schrift) · **F5** (Listenzeichen versteckt ⇒ „eingerückter Text") · **F4d**/S4 (Kästchen-Regel) · S5a (`overflow-x: auto` für breite Tabellen) · **F12** (Glyphen) |

Fundstellen: `docs/concepts/phase10_5_editor_4_1_plan.md` §2 (F4, F5, F11, F12), §5 (S4 „Editor-Anzeige = Wahrheit", S5a „ein
typografisches System", S5b Schriften); Anhang A6 (Klickgenauigkeit mit Plex Sans 16 px: 38/38) und A11 (Korrekturen „H4":
Kontrast, Mono-Teilmenge). *Hinweis zur Benennung:* der Nachtrag des Nikingers nennt den Befund „H4"; im Plan heißt die
Schrift-Messung **F11**, „H4" im Anhang betrifft Kontrast und Glyphen — beides gehört zum selben Leitziel.

**Was der P11-Plan neu entscheiden muss (der Editor-Plan reicht dafür nicht ganz):**
- **S4/S5a lösen Schrift, Listenzeichen, Kästchen, Überschriften-Größen und breite Tabellen** — aber nicht alles. Der Plan ist
  ein **CM5-Hybrid**: in der Cursorzeile stehen die Markdown-Marker sichtbar (`# `, `[…](…)`). Bild 2 ist genau dieser
  Zustand. Writer-Optik heißt: auch dort kein Rohtext, oder ein Link-/Überschriften-Widget. **Offen, nicht entschieden.**
- **S6 „Tabellen bearbeiten (im Rohtext)"** widerspricht dem Wunsch „nahtlos" (§6 Nr. 1) — neu entscheiden.
- **Die Abnahme:** die Blöcke 11 (Editor Stufe 1 + 2) und 13 (Größen, Knopfleiste, Farben) haben ihre Zeilen
  (P10.5-50–55, 62–64) und die Sichtung P10.5-51 **nach dem damaligen Maß** erfüllt. Das Soll „sieht aus wie ein
  Textverarbeitungsdokument" war **nie** ein Abnahmemaß und ist **nicht** erfüllt. *P10.5-63 („Knopfleiste nach Word") meint
  die Reihenfolge der Knöpfe, nicht die Optik des Dokuments.* **Ob dafür eine Abnahmezeile geöffnet wird, entscheidet der
  Nikinger** (§8 Nr. 1); sie ist in den 86 Zeilen **nicht** gezählt.
- **P10.5-55 (Rohtext-Schalter)** ist am 2026-10-25 abgenommen und am 2026-10-26 auf Wunsch des Nikingers für Nutzer
  entfernt worden (`setRawMode()` bleibt als interner Notausgang). Die Zeile belegt also einen Zustand, den es seit `v4.0.0`
  für Nutzer nicht mehr gibt.

**Die Lehre dahinter:** das Abnahmemaß hatte **keine Tabelle als Sichtkriterium** — und kein Kriterium „sieht aus wie ein
Dokument". Die Zeilen maßen Größen, Knopfleiste, Roundtrip und Budget. Der Tabellen-Fehler (seit `0cf72a1`, Block 11.3: der
eigene Editor hat keinen Darstellungsweg mehr, Plan F1) fiel deshalb erst live auf (2026-11-03). **Für P11:** das Leitziel als
messbare Zeilen fassen (z. B. Fließtext-Schrift = Plex Sans, keine Marker außerhalb der Cursorzeile, Aufgabe = Kästchen-Element,
Tabelle ≤ Containerbreite), je mit Probe-Zelle und Gegenlauf, **plus** eine Sichtung mit echten Notizen.

## 3 Delta seit dem P10-Handover

| Block | geplant | gebaut (Kurz) | Deploy | Zeiger |
|---|---|---|---|---|
| 0 Haushalt | ja | INDEX-Luft, Register-Luft, DO-3-Wächter; Plan-Hebel zu klein (2.478 B), erweitert | — | Plan Nachtrag 2026-10-22 |
| 1 Betrieb | ja | Caddy-Vorlage (V199), `SuccessExitStatus=143` (V200), `constraints.txt` | A | Modulstatus-Archiv |
| 2 Fehler/Parität | ja | BG-1, RE-1/2, P10-I in `SharePolicy`; Probe 28/28 Web × MCP | A | ebd. |
| 3 Hygiene | ja | EXIF-Strip in `Store.put_asset()` (P1-Öffnung 15), Waisen-Skript | A | ebd. |
| 4 Performance | ja | `/overview` ein Durchgang + `to_thread`: Bench **2405,6 → 107,3 ms** | A | ebd. |
| 5 MCP-Schicht | ja | FastMCP **4.1.3**, `proto` im Log, `append_to_items` | B | ebd. |
| 6 Anbieter | ja | Loopback-Redirect, `application_type`, CSP `form-action`, `/mcp` ohne Slash; DCR 400 → 201 | B | ebd. |
| 7 Darstellung | ja | 404-Seite, Logo, Tab-Titel, Kontrast, Assignee-Filter, `doing`-Ring | C → D | ebd. |
| 8 Karte C2 | ja | Lappen, Furchen, Zellen; Smoke 5/5 | C → D | ebd. |
| 9 Rechte/Namen | ja | `created_by`, `rename_folder`, `rename_space` (P1-Öffnungen 12–14) | D | ebd. |
| 10 Suche/Realtime | ja | Volltext, SSE (Latenz 141 ms, Shutdown 5,22 s) | D | ebd. |
| 11 Editor 1 + 2 | ja | CM5 vendort und nachgeladen, Live-Darstellung, Kästchen, Format-Vokabular (P1-Öffnung 11) | D | ebd. — **Writer-Optik: §2** |
| 12 Doku | ja | DO-1 (drei Heads unter Softcap), ROADMAP < 30 KB, Register-Bilanz per Skript | — | ebd. |
| 13 Aufträge | Nachtrag 10-25 | Editor-Größen, Knopfleiste nach Word, Knopffarben; Nachzug: `v4.0.0`, Rohtext-Schalter weg | D | Session-Archiv |
| 14 Kartenlayout | **neu** | „zufällig, aber geordnet": Saat, Regionen, Kamera, Beschriftungen, **ein Körper** (Option B), kompakt/glatt | D | Pläne 14, 14.6, 14.7 |
| 15 Review-Fixes | **neu** | B1–B10 (+B15, B20, B3′, B4′) | D | Plan Block 15 |
| 16 Launch-Film | **neu** (P10.6) | 48 s, zwei Sichtungsrunden | vor D | Plan Launch-Film |
| 17 Film in der App | **neu** | Startbild beim Erststart, Wiedersehen im Update-Log | D | Plan Block 17 |
| 18 Live-Funde | **neu** | Karte flüssig: Ruhe/Pan **309 → 2,3 ms**, Einschwingen **55 → 1,6 s**; Live-Zeilen-Probe 18/49 | E | Plan Block 18 |
| 19 Editor-Hotfix | **neu** | Darstellungs-Probe (28 Fixtures, 57 Zellen), Entwurfsschutz, Tabellen-Widget | F | Editor-Plan S0–S2R |
| Z Closeout | ja | dieser Handover, Grafik, Rotationen | — | Head |

**Deploys:**

| # | Version | SHA | `health_gate` | live seit |
|---|---|---|---|---|
| A | `v3.1.5` | `7358f22` | 9/9 | 2026-10-23 |
| B | `v3.1.6` | `e5c834e` | 9/9 | 2026-10-23 |
| C | `v3.1.7` | — | — | nie einzeln, in D enthalten |
| D | `v4.0.0` | `2eb697f` | 9/9 | 2026-11-01 |
| E | `v4.0.1` | `0e317cf` | 9/9 | 2026-11-03 |
| F | `v4.0.2` | `d2ca573` | **8/9** am Folgetag | 2026-11-06 |

**Zu F:** der eine Fehler ist der Update-Log-Check mit `--require-todays-update-log` — der Lauf kam einen Tag nach dem Deploy,
der Log trägt richtig den Deploy-Tag. Alle anderen Prüfungen OK. **Ein sauberer Lauf ohne das Flag steht aus** (§8). Die
Bedingung von Block Z („alle Deploys mit echter `health_gate`-Ausgabe") ist damit für F nur mit diesem Vorbehalt erfüllt.

## 4 Verworfen, verschoben, nicht gebaut

- **PF-3 (Client-Cache):** nicht verlangt — P10.5-18 live: Waiting 187/163 ms ≤ 300 (Zahlen vom Nikinger angenommen).
  **PF-5** (Virtualisierung) bleibt verworfen, bis eine Messung es verlangt.
- **Editor 4.1 S3a–S11 → P11 Block 1** (E1 geteilt, 2026-11-05). **Editor-Farben / Stufe 3** (Farbraster + freie RGB) → P11
  (Block-18-Plan §4 E2).
- **A1 (`ausreisser`):** live nicht zu beobachten (Nikinger); die Zelle bleibt in der Wegwerf-Saat rot (Ordner-Zustand
  3,1 × `REGION_GAP`), kein Code.
- **C2-Furche:** das neue Layout (14.2) trennte die Spaces, die Furche hatte keinen Gegenstand mehr → Option B „ein Körper"
  (14.6, Nikinger 2026-10-28).
- **Rohtext-Schalter** für Nutzer entfernt (2026-10-26, Wunsch des Nikingers) — siehe §2 zu P10.5-55.
- **Ultra-Review B11–B22** (ohne B15/B20) → Backlog. **B18** (README „sechs Tools") ist im Closeout behoben, **B17** (zwei
  Versionsquellen: `/health` meldet `0.1.0`, die UI `v4.x`) ist Code → P11.
- **Deploy C** wurde nie einzeln ausgeliefert (der Badge `v4.0.0` stand schon auf dem Branch; C ging in D auf).

## 5 Pannen und Lehren (ehrlich)

- **Das Abnahmemaß hatte Lücken** — keine Tabelle, keine Writer-Optik als Sichtkriterium (§2). Gezählt wurde sauber, aber das
  Falsche fehlte.
- **Live-Funde nach Deploy D** (2026-11-01/03): Karte mit Tags und Ordnern träge (Kantenzeichnen: 309 ms je Bild), eine
  Schleuder (N1) im Tag-Zustand, Tabellen als Rohtext. Die Wegwerf-Saat hatte nicht die Form der echten Daten (Fabians
  Home-Space, Ordner mit 40–80 Items) — Grund für den Vorschlag Green/Blue (§6 Nr. 5).
- **Zwei Live-Fehler im Entwurfsschutz** (Entwurf weg nach Neuladen; „Wiederherstellen?" setzt eine KI-Änderung still zurück =
  clientseitiges Last-Write-Wins) fand erst die Analyse des Editor-Plans, nicht ein Test. Behoben in S1.
- **B1 kritisch, live seit 2026-08-20** — gefunden vom Ultra-Review, nicht von ~1800 Tests. Ein Review vor jedem Major-Release
  (Prompt 4) hat sich bezahlt gemacht.
- **Zahnlose Gegenläufe**, jeweils neu gebaut: der C2-Wächter in 14.2 (blieb bei „Furche aus" grün), 15.5 (der erste Gegenlauf),
  Block 17 G2, Block 18 `schleuder` (zahnlos unter der Mindestdistanz, Gurt bleibt, ungetestet). Der Caddy-Gegenlauf
  „ohne `flush_interval`" aus dem Plan existiert in Caddy 2.6.2 nicht.
- **Das Messgerät irrte einmal:** bei P10.5-26 lag der Fehler im Stub-Prototyp, nicht im Server (der verdächtige `405` war normal).
- **Plan-Rechnungen drifteten:** Block 0.5 (Hebel 2.478 B statt 3.000 B), die Zeilenzahl (61 → 86, an fünf Orten nachgezogen),
  das opencode-Rezept `agent.build.tools` (nicht nötig, gab Schreibwerkzeuge frei; korrigiert in Plan Block 18 §5.9).
- **Gate-Datumsfalle:** `--require-todays-update-log` am Folgetag scheitert (Deploy F). Lauf am Deploy-Tag oder ohne das Flag.
- **Ausführer (Rohdaten, Bewertung extern, P10.5-B):** 61 Commits tragen den Trailer MiniMax M3.1 Flash (Blöcke 0–11), 88 einen
  Claude-Trailer (Opus 5.5: 50, Sonnet 5.5: 38), **22 keinen** (13 aus Block 14 — laut Modulstatus opencode + Claude Code —, 9 vom
  2026-10-23: Deploy-Vorbereitung A/B und Block 7.1–7.3); Lock P10.5-B verlangte einen Trailer je Commit. Die Blöcke 13 und 15–19
  baute Claude Code.

## 6 P11-Vormerkungen (vollständig, je mit Fundstelle)

1. **Leitziel Writer-Optik** — §2 dieses Handovers; Editor-Plan §2/§5.
2. **Editor 4.1 = P11 Block 1** (S3a–S11, `v4.1.0`, ~11 Sitzungen; marked 18.1.3 als Renderer, CM5 bleibt, Budget „nachgeladen"
   zwei Zeilen) — Editor-Plan §5/§8, Head „Offen beim Nikinger" (Editor-Plan). **Erst planen, dann bauen.**
3. **Nahtloses Bearbeiten — eine Tabelle bleibt beim Bearbeiten eine Tabelle** (heute zeigt das Widget beim Klick den Quelltext;
   Plan S6 denkt „im Rohtext") — Head „P11-Vormerkungen des Nikingers (2026-11-06)" (1). Byte-Vertrag V1–V6 gilt weiter.
4. **„Feedback"-Knopf** in der Web-Oberfläche (wohin? Item in einem Feedback-Space oder ein Link; kein LLM, kein Secret im
   Client) — ebd. (2).
5. **Green/Blue-Instanz** (zweite, dauerhafte Instanz mit Datenkopie, eigener Port, zuerst deployt; Seam `SHAREFYX_PORT` seit P5) —
   Head „Handover-Posten (Nikinger 2026-11-03)". Prod ist kein Testfeld.
6. **Wiederkehrender Darstellungs-Check** (Render-Probe an der Wegwerf-Instanz als fester Schritt der Deploy-Vorbereitung +
   statischer Check in `health_gate.sh`) — Head „Neuer Posten für P11/Handover"; konkret im Editor-Plan §7 und S10.
7. **Editor-Farben / Stufe 3** (Farbraster + freie RGB; CSP: freie Farbe nur per CSSOM) — Block-18-Plan §4 E2; Editor-Plan §8 „Für
   später".
8. **`ev=tool` ohne `client_id`** (nur `ev=http` trägt den User-Agent) — Head „Befunde aus den Live-Läufen" (1);
   eurofleet-Notiz §7 Befund 2. Verwandt: unbekannte Argumente loggen als `err=internal` (Notiz §7 Befund 4).
9. **Sicherheits-Hinweis Schreib-Token:** `mcp.sharefyx` steht dauerhaft lesend **und schreibend** in
   `~/.config/opencode/opencode.json` dieser VM (Nikinger-Entscheidung); die Agenten von `opencode serve` können im Home-Space des
   Nikingers schreiben. Einzige Schranke gegen Prompt-Injection ist Hard Rule 4. Idee (keine Entscheidung): ein nur lesender
   Agenten-Principal. Der Nikinger **will** Lesezugriff projektübergreifend — Head „Befunde" (3)/(6); Notiz §7 Nachtrag.
10. **Trading-VM-Anbindung** (Eintrag und Login offen; Traktion-VM bewusst nicht) — Head „Befunde" (5); Notiz §7 Nachtrag.
11. **A1 `ausreisser`** — Modulstatus Block 18; Block-18-Plan §6 Nr. 4.
12. **Korpus-Lücke „Tabelle direkt unter einer Textzeile"** (live im Widget ok, aber keine der 28 Fixtures) — Head „Schreibtest der
    drei Modelle".
13. **Ultra-Review-Backlog:** B11 (`move()` ohne Rollback der Assets), B12 (Vollscan je Suche, Abschneiden über 5000 — ein
    Messauftrag), B13, B14 (MCP-Offset negativ), B16 (`archived` im Editor wählbar), **B17** (zwei Versionsquellen), B19 (tmp-Dateien
    im Git), B21 (Authorize-Zeilen ohne Limit), B22 (leerer Ordner-Rename loggt CRITICAL) — `phase10_5_ultra_review_v4.0.0.md`,
    Plan Block 15 Zeile 101.
14. **Register-Zeilen mit Ziel P11:** PA-4 (CIMD), ED-4 (Excel-artige Tabellen), UI-7 (Handy-Oberfläche), LG-11 (verbundene
    AI-Sessions) — `BAUSTELLENREGISTER.md`.
15. **Betrieb, klein:** Ollama braucht ein abgeleitetes Modell mit `num_ctx 16384` (Standard 4096 schneidet den Werkzeug-Prompt ab);
    `opencode run` liest stdin (`</dev/null`); Platte der VM regelmäßig räumen (`/tmp/opencode` Proben, pytest-Temp) — Notiz §7.

## 7 Editor-Plan: Lage und Entscheidungen

**Gebaut (P10.5 Block 19, `v4.0.2`):** S0 Probe + Korpus, S1 Entwurfsschutz, S2 Tabellen-Widget, S2R Release. Basislinie der Probe
heute: **26 von 57 Zellen rot** (Chromium und Firefox, 0 Abweichungen) — das ist der dokumentierte Rest für S3a–S11.
**Offen (P11 Block 1, `v4.1.0`):** S3a–S11. Die Abnahme-Vorschläge im Plan §6 tragen noch P10.5-Nummern (87–96) — P11 nummeriert neu.

| E | Frage | Stand |
|---|---|---|
| E1 | Platzierung | ✅ geteilt: `v4.0.2` in P10.5, Rest P11 Block 1 |
| E2 | Renderer | ✅ marked 18.1.3 vendoren |
| E3 | Budget „nachgeladen" | ✅ zwei Zeilen: Editor ≤ 100 KB, Renderer ≤ 20 KB |
| E4 | Inline-HTML | ✅ nur `<br>` |
| E5 | Fließtext Plex Sans 16 px | ✅ ja — **der Kern des Leitziels** |
| E6 | CRLF dokumentieren oder P1-Öffnung | ⬜ Empfehlung: dokumentieren (kein Code) |
| E7 | Fußnoten | ⬜ Empfehlung: eigene Minimal-Erweiterung ohne IDs |
| E8 | Rechtschreibprüfung / Tab außerhalb von Listen | ⬜ Empfehlung: (a) nicht in 4.1, (b) zwei Leerzeichen |
| E9 | MCP-Beschreibung um die Teilmenge ergänzen | ⬜ Empfehlung: ja (nur Text) |
| E10 | größte echte Notiz | beantwortet: 1836 Zeilen / 112.821 B |
| E11 | Konfliktdialog mit Zeilen-Diff | ⬜ Empfehlung: ja |
| E12 | Lesen/Bearbeiten-Schalter | ⬜ Empfehlung: nein — **im Licht des Leitziels neu prüfen** |

Quelle: Editor-Plan §8. Die `[VERIFY]` des Editor-Plans (V-E1–V-E14) stehen dort in §9 und wandern unverändert nach P11.

## 8 Offene Entscheidungen

| # | Frage | Wer | Anker |
|---|---|---|---|
| 1 | **Abnahmezeile für die Writer-Optik öffnen?** (nicht in den 86 gezählt) | Nikinger | §2 |
| 2 | **Formaler Schluss:** ROADMAP-Zeile P10.5 ✅ und Wurzel-„Current state" (vom Closeout vorbereitet) | Nikinger | Head, Session-Block |
| 3 | Hybrid (Marker in der Cursorzeile) gegen Writer-Optik; S6 „im Rohtext" gegen „nahtlos" | P11-Planer legt vor, Nikinger entscheidet | §2, §6 Nr. 3 |
| 4 | E6–E9, E11, E12 | Nikinger | §7 |
| 5 | Feedback-Knopf: Ziel der Rückmeldung | Nikinger | §6 Nr. 4 |
| 6 | Green/Blue bauen? | Nikinger | §6 Nr. 5 |
| 7 | nur lesender Agenten-Principal (Idee) · Trading-VM anbinden | Nikinger | §6 Nr. 9/10 |
| 8 | `health_gate` für F ohne `--require-todays-update-log` nachfahren | Nikinger | §3 |
| 9 | Ausführer für P11: der M3-Endpunkt ist bis **2026-11-15** zugesagt, Marktblick ~2026-11-10 (extern) | Nikinger + Planer | P10-Handover §5 Nr. 3 |
| 10 | Termine, keine Blocker: **BT-5** `LEGACY_UNTIL` (Arbeitslaptop-Test war um den 2026-11-02 fällig, kein Vermerk gefunden) · **AL-1 Zeile 15** · AL-2/AL-6 (Fabian, V150) · AL-4 (einmalige Bewertung P6.5-14) · V203 (Fleet) | Nikinger | Register |
| 11 | Regelkandidat „Sichtungen zuerst als Bilder an der Wegwerf-Instanz" als feste Regel? (steht als Arbeitsweise in der Wurzel seit 2026-10-22) | Nikinger | Head „Handover-Posten (Regelkandidat)" |

## 9 `[VERIFY]`-Bilanz

**V207–V219 (P10.5):** 9 ✅ · 1 ⚠️ · 1 ⬜ · 2 ohne Auflösungsvermerk — ✅ V207–V209, V211–V214, V218, V219 · ⚠️ V210 ·
⬜ V215 · ohne Vermerk (implizit erledigt) V216, V217.

| V | Stand | Ort |
|---|---|---|
| V207 | ✅ `fastmcp 4.1.3`, Changelog 4.1.1–4.1.3 ohne Bruch an den genutzten APIs | Modulstatus-Archiv Block 5 |
| V208 | ✅ claude.ai live: `proto="2026-07-28"` im Journal (löst V198 ab); den Wert für opencode nennt die eurofleet-Notiz nicht | P10.5-22 |
| V209 | ✅ opencode 1.19.4: Loopback `127.0.0.1:19876`, `application_type` fehlt | Block 6 |
| V210 | ⚠️ „CSP-Host-Quelle kann kein IPv6-Literal" steht als Tatsache in Code-Kommentaren (`clients.py:27`, `config.py:68`); eine Spec-Lektüre ist **nicht belegt** | Plan §4, Code |
| V211 | ✅ `visibility: hidden` hält den Cursor (0,0 px), gemessen | Block 11.4 |
| V212 | ✅ SSE über beide Eingänge, Caddy 2.6.2 puffert nicht | P10.5-49 |
| V213 | ✅ uvicorn 0.54.0, `timeout_graceful_shutdown=5`, Shutdown 5,22 s | Block 10.5 |
| V214 | ✅ CT 111 vom opencode-Host erreichbar, Werkzeugaufrufe mit `qwen3-vl:8b`/`gpt-oss:20b` (mit `num_ctx 16384`) | P10.5-28 |
| V215 | ⬜ Safari/SVG-Favicon nie gemessen (WebKit startet hier nicht, vgl. V-E1) | Plan Block 7.2 |
| V216 | kein Auflösungsvermerk gefunden — Block 0.5 baute das Archiv, `test_index_archive.py` blieb grün (implizit) | Plan §4 |
| V217 | kein Auflösungsvermerk gefunden — der D4-Aufruf lief bei A, B, D, E, F (implizit) | Plan §2.5 |
| V218 | ✅ `mcp.sharefyx = {type: "remote", url, oauth: {}}` trägt live; `agent.build.tools` nicht nötig | Notiz §7 Nachtrag |
| V219 | ✅ `Context.request_context.protocol_version` | Block 5 |

**Geerbt und geschlossen:** V197 (Block 6) · V199, V200 (Block 1) · V201-Rest (`ui_budget`, P10.5-50) · V193, V194 (Block 9) ·
V120 (Block 7) · V198 (durch V208). **Bleibt draußen:** V203 (eurofyx-fleet) · V150 (Termin).
**Ohne Nummer, aufgelöst:** zweiter Modellanbieter (P10.5-28) · CRLF normalisiert der Server, nicht CM5 (Editor-Plan F8).
**Ohne Nummer, offen:** die Writer-Optik (§2) · ob die breite Tabelle aus Bild 3 am Widget oder am Bildausschnitt überläuft.
**Nächste freie Nummer: V220** (repo-weit gegrept 2026-11-07; höchste vergebene V219). Die Editor-Plan-Marker V-E1–V-E14 sind
eine eigene Reihe.
**Weitere Reihen, offen und nicht nummeriert in V:** Addon Render V-A1–V-A7 (`phase10_5_block18_addon_render.md` §6:
GPU-Rasterung, dpr/Browser des Nikingers, Deckel der Zwischenspeicher-Schicht) · Addon Insel §7 (Live-Form der Spaces,
Firefox/Safari) · Launch-Film-Plan: Remotion-Lizenz (nicht gewählt, gegenstandslos). Gemeinsamer Nenner: **GPU, Firefox des
Nikingers und Safari wurden in P10.5 nie gemessen** (kopfloses Chromium/Firefox, Software-Rasterung).

## 10 Hinweise für den P11-Planer

- **Lesereihenfolge:** dieser Handover → Editor-Plan BLUF, §2, §5, §8 → Head „Offen beim Nikinger" → Register (P11-Zeilen).
- **Throwaway zuerst** (Wurzel, Working style 2026-10-22): alles Messbare an einer Wegwerf-Instanz; live nur, was der Server
  nicht selbst entscheiden kann — und das entscheidet der Nikinger. Wegwerf-Belege zählen als live, außer bei Identitätsfragen
  (Memory „throwaway evidence counts as live").
- **Ehrliche Gegenläufe:** nach einer Design-Änderung den Gegenlauf für die neue Szene neu bauen; jeder Anker genau einmal
  (Falle aus 18.2b). §5 zählt vier zahnlose Fälle.
- **Kein Ausführer-Kontext-Tod:** eine Session je Schritt, Kontext ≤ 200 K (Lehre aus 86 M Tokens, P10); Text gegenlesen.
- **Versionen:** `.rail__version` zählt Deploy-Zyklen, nicht Phasen. Ein Minor-/Major-Sprung ist Sache des Nikingers — **für
  `v4.1.0` ist er entschieden** (E1).
- **Abnahmemaß:** jede sichtbare Eigenschaft, die der Nikinger erwartet (Tabelle, Writer-Optik), wird eine Zeile mit Probe-Zelle,
  Gegenlauf **und** Sichtung mit echten Notizen — sonst wiederholt sich §2.
- **Größen:** `docs/INDEX.md` steht an der 3.000-B-Reserve (≤ 37.960 B, Wächter P10.5-2) — INDEX-Luft ist der erste Haushalt
  von P11. Session-Block ≤ 4 KiB (P10.5-T), Heads ≤ 40.960 B, ROADMAP < 30 KB.
- **Nummerierung:** Locks `P11-A…`, Abnahme `P11-1…`, `[VERIFY]` ab **V220**.
- **Sharefyx-Connector in Claude Code:** Live-Zeilen über den claude.ai-Connector gehen auf Auftrag des Nikingers; Schreibproben
  nur an einer eigenen Wegwerf-Notiz, nie an echten Items (P10.5-22).

## 11 Was dieser Handover nicht enthält

Die Abnahmezeilen mit Beleg (`phase10_5_finishing/ABNAHME_ARCHIVE.md`), die Vollstände der Blöcke (`MODULSTATUS_ARCHIVE.md`),
die Chronik (`SESSIONS_ARCHIVE.md`), die Locks im Wortlaut (`phase10_5_finishing_plan.md` §0) und den Editor-Plan selbst. Sie
werden dort gelesen, nicht hier kopiert.
