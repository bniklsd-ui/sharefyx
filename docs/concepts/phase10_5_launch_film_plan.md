---
status: live
purpose: Plan Block 16 „Launch-Film“ für Sharefyx v4.0.0 — Auftrag, Antworten des Nikingers (2026-10-31), Material, Technik (Frame = Funktion des Index), Storyboard mit der „4“, Schritte 16.0–16.5, Kriterien.
read-when: Arbeiten am Launch-Film — zuerst §1 (Antworten) und §5 (Schritte)
detail: L2
up: ../../phase10_5_finishing/CLAUDE.md
down:
  - ../UPDATE_LOG.md   # die Quelle der Feature-Liste (Blöcke 2026-10-23 bis 2026-10-26)
updated: 2026-10-31 (Plan, Claude Code — Notiz zum Plan Block 16 ausgebaut: Antworten Q1–Q7/QA–QC, Material neu, Storyboard, Schritte) | 2026-10-29 (notiert, Claude Code — Reihenfolge: erst das Ultra-Review, dann die Planung des Films)
---
# Launch-Film — Sharefyx v4.0.0 (Plan Block 16)

> **Auftrag (Nikinger, 2026-10-29, wörtlich):** „im Grunde genommen ein mit Code generierter
> ‚Product Launch' Film zu sharefyx 4.0.0, mit all den neuen Features. Dabei soll der Film an die
> existierenden Launches von Antrophic / OpenAi angelehnt sein, und künstlerisch die neuen
> Features, Bug fixes und verbesserungen zeigen, länge 40s - 1min."
> Nachtrag: „nur die Notiz für den Plan — dazu werden sicherlich Fragen aufkommen, die ich
> separat klären möchte. Externe Tools sind erlaubt."
>
> **Storyboard-Auftrag (Nikinger, 2026-10-31, wörtlich):** „do it in a ‚visually flowing move',
> and try to incorporate the v4.0.0 in the film e.g by zooming out and Ording all scenes at once so
> that they resemble the 4 or something creative.“

**Stand:** Plan, **nicht** begonnen — der Nikinger gibt ihn frei, dann 16.0. **Zeit:** der Film
soll an **diesem Wochenende** fertig werden, **vor** Deploy D (QA). **Risiko, benannt:** damit liegt
der Film auf dem Weg zu Deploy D — deshalb Probe zuerst, Standbild vor jedem Volllauf und eine
**Minimalfassung** (§5, 16.5), damit Politur den Deploy nie aufhält. Ob D notfalls ohne Film fährt,
entscheidet der Nikinger, nicht dieser Plan.

## §1 Antworten des Nikingers (2026-10-31)

| # | Frage | Antwort | Folge im Plan |
|---|---|---|---|
| Q1 | Echte UI oder nachgebaut? | **Echte UI** (Empfehlung) | Aufnahmen der Wegwerf-Instanz, stilisiert gerahmt (§3) |
| Q2 | Werkzeug | „wenn es andere Wege gibt, Video **reproduzierbar** zu erzeugen, offen dafür“ | Vergleich §3.1 — Entscheidung: Frame = Funktion des Index, kein Framework |
| Q3 | Sprache | **Deutsch** | alle Texttafeln deutsch, wie die UI |
| Q4 | Ton | Empfehlung angenommen | stummfähiger Schnitt + **im Code erzeugter** Ambient-Ton (§3.4) |
| Q5 | Format | ja, „solange die Qualität gut bleibt“ | Zahlen in §3.3 |
| Q6 | Publikum | „nicht speziell intern, aber **ohne Namen und Zugangsdaten**“ | Checkliste §4 |
| Q7 | KI-Szene | „was am besten passt“ | echter Lauf an der Wegwerf-Instanz, **aufgezeichnet und wiedergegeben** (§3.2) |
| QA | Film vor Deploy D? | „Film ist dieses Wochenende fertig, passt“ | Reihenfolge bleibt; Risiko oben |
| QB | Materialliste | „**ganz** neu“ | §2 |
| QC | Wer baut? | **Claude Code** (Opus) | Sichtung Standbilder beim Nikinger |

**Vorbild „Fable 5.5“ (vom Nikinger genannt) — unverifiziert.** Eine offizielle Veröffentlichung
oder Benchmarks fanden sich am 2026-10-31 **nicht**; im Umlauf sind Community-Clips, deren Herkunft
die Quellen selbst als unbestätigt kennzeichnen (das Video selbst konnte ich nicht ansehen). Übernommen
wird nur das Allgemeine: **im Browser gerendert**, **durchgehende Kamera**, **getimte Übergänge**,
Punkt-/Partikelanimation mit weichem Easing. Quellen:
[aiidelist](https://aiidelist.com/blog/claude-fable-5-5),
[joaoqueiros](https://www.ai.joaoqueiros.com/blog/claude-fable-5-5-leak-animation-demos-evidence-check),
[cometapi](https://www.cometapi.com/claude-fable-5-5-rumor/).

## §2 Material — was v4.0.0 mitbringt (neu aus `docs/UPDATE_LOG.md`, alle P10.5-Blöcke)

Gezeigt wird nur, was **HEAD an der Wegwerf-Instanz wirklich zeigt** (kein erfundenes UI).
Spalte „Szene“ = Kachel im Storyboard (§3.5); „Tafel“ = nur Text, kein Bild.

| Bereich | Neu (Update-Log) | Szene |
|---|---|---|
| **Editor** | Live-Editor: Markdown formt sich beim Schreiben · To-dos als Kästchen · Farbe und Größe im Text · Knopfleiste in Words Reihenfolge, einheitliche blaue Knöpfe | S2, S3, S4 |
| **Karte** | ein kompakter Körper: Spaces eng um den eigenen, runde Umrisse · dieselben Notizen = dasselbe Bild · Beschriftungen überdecken sich nicht · ganze Karte auf einmal (Zoom 50 %) · Bahnen zwischen runden Zellen · Suche und Filter in der Karte · gemerkte Positionen · Aufgaben „In Arbeit“ hervorgehoben | S5, S6 |
| **Ordnung** | Ordner umbenennen (Items ziehen mit) · Team-Spaces umbenennen · Filter „Zugewiesen“ · geöffneter Space bleibt in den Einstellungen markiert | S7, S8 |
| **KI-Verbindung** | mehrere Notizen in **einem** Aufruf ergänzen, je mit eigener Version · neuestes MCP-Protokoll (2026-07-28), ältere Clients laufen weiter · lokale MCP-Clients melden sich direkt an · **MCP-Clients jenseits von Claude** (P10.5-26, Wegwerf-E2E — **nicht** „zwei Anbieter live“, P10.5-27/28 sind ⬜) | S9 |
| **Schneller** | Übersicht in einem Durchgang · Ladezustand ab 0,2 s · Space-Liste füllt sich auch bei später Übersicht | S10 |
| **Robuster und sicherer** | eine kaputt bearbeitete Notiz legt die Suche nicht mehr lahm · Titel höchstens 256 Zeichen · Mitglieder eines persönlichen Space verwaltet nur der Besitzer · keine Verschiebung in fremde persönliche Spaces · Fotos ohne GPS/EXIF, Ausrichtung bleibt · Befunde aus einem Code-Review behoben (**ohne** Einzelheiten, Q6) | S11, Tafel |
| **Gesicht** | eigenes Zeichen (Leiste, Tab) · Tab-Titel folgt der Ansicht · eigene Fehlerseite · Update-Hinweis in einer Zeile, Versionsangabe lesbar | S1, S12 |

## §3 Technik

### §3.1 Werkzeug (Q2) — reproduzierbar heißt: jedes Bild ist eine Funktion seiner Nummer

| Weg | Reproduzierbar? | Echte UI? | Urteil |
|---|---|---|---|
| **Bühne im Browser, `frame → Zustand`, Playwright-Screenshot je Frame, Pipe in ffmpeg** | ja — kein Takt, kein Netz | ja, als vorher aufgenommene Bilder | **gewählt**: dasselbe Prinzip, das die Frameworks intern nutzen, ohne neuen Stack |
| Remotion | ja (Frame-Seek) | ja (DOM) | React-Kette zusätzlich; Lizenzbedingungen `[VERIFY]` |
| Motion Canvas / Revideo | ja | nur Canvas — UI wieder als Bilder | gleichwertig, aber zweite Szenen-Sprache |
| Playwright `recordVideo` | nein (Echtzeit, Frames fallen) | ja | nur für Entwürfe |
| KI-Videogenerator | nein | **erfindet** UI | verworfen — Film über echte Features |

**Regel:** die Bühnenseite berechnet Kamera, Kachel-Lage, Deckkraft und Tipp-Fortschritt **nur aus
`frame`** — keine CSS-Transitions, kein `requestAnimationFrame`, keine Uhr, kein Netz. Die **echte
UI läuft nicht** in der Bühne (Polls, Realtime, Cursor-Blinken, Kartensimulation wären Zufall),
sondern wird **vorher** von der Wegwerf-Instanz aufgenommen: Standbilder und kurze Bildfolgen
(Playwright, `deviceScaleFactor: 2`, Zustand schrittweise — ein Zeichen tippen, ein Bild).

### §3.2 KI-Szene (Q7)

Ein **echter** MCP-Client ruft gegen die Wegwerf-Instanz `list_spaces` und `append_to_items` (drei
Notizen, ein Aufruf); die Antworten werden als JSON gespeichert und in der Bühne als Terminal-Kachel
**wiedergegeben** (Tipp-Fortschritt aus `frame`). Echte Daten, deterministische Darstellung, kein
Modellaufruf je Render. **Kein** Anbietername, **kein** Fremdlogo in der Kachel.

### §3.3 Qualität (Q5) — Zahlen

1920 × 1080, **60 fps**, H.264 (`libx264`), **CRF 16–18**, `yuv420p`, `+faststart`; Aufnahme mit
2× (3840 × 2160), Verkleinerung `lanczos` — UI-Schrift bleibt scharf; leichtes Rauschen/Dither auf
dunklen Flächen gegen Banding (8 Bit). Frames gehen per `image2pipe` **direkt** in ffmpeg — keine
3 000 PNGs auf der Platte der Live-VM. ffmpeg kommt aus `imageio-ffmpeg` (statische Binärdatei) in
einem eigenen Werkzeug-venv `~/.claude-code-tools/film-venv` — **`libx264` dort prüfen** (16.0).

### §3.4 Ton (Q4)

Stummfähiger Schnitt; dazu ein Ambient-Ton, **im Code erzeugt** (numpy, fester Seed, 48 kHz WAV:
Flächen + weiche Impulse auf den Szenenwechseln, Takt aus denselben Frame-Marken wie das Bild), per
ffmpeg dazugemischt. Keine Lizenzfrage. Ob er gut klingt, entscheidet der Nikinger.

### §3.5 Storyboard — eine Fahrt, die eine 4 schreibt

**Idee:** alle Szenen liegen als Kacheln auf **einer** großen Fläche, entlang der Striche einer
**„4“**. Die Kamera fährt **ohne Schnitt** von Kachel zu Kachel — sie schreibt die 4, ohne dass man
es merkt. Am Ende zoomt sie heraus, **alle Kacheln ordnen sich gleichzeitig** zur sauberen 4, und
die Punkte der Karte strömen aus S5 heraus und bilden **„.0.0“**. Klammer: der Film beginnt
**in** der Versionsangabe der Leiste (`v4.0.0`, echte UI) und endet bei der großen 4.0.0.

| s (≈) | Takt | Kachel / Inhalt |
|---|---|---|
| 0–4 | Schwarz, Zoom **aus** der Leisten-Versionsangabe, Zeichen baut sich auf | S1 |
| 4–13 | Abstrich der 4 (schräg): „Schreiben, wie es aussieht.“ | S2 Live-Editor tippt · S3 Kästchen · S4 Farbe/Größe + Leiste |
| 13–24 | Querstrich: „Alles verbunden.“ | S5 ganze Karte, Suche leuchtet Knoten an · S6 „In Arbeit“ · S7 Ordner umbenennen · S8 „Zugewiesen“ |
| 24–40 | senkrechter Strich abwärts: „Für Menschen und Maschinen.“ / „Schneller. Robuster.“ | S9 KI-Szene · S10 Übersicht + Ladezustand · S11 Suche trotz kaputter Notiz · S12 Fehlerseite/Tab-Titel |
| 40–48 | Zoom heraus, alle Kacheln ordnen sich zur 4; Kartenpunkte bilden „.0.0“ | alle |
| 48–54 | Endtafel „Sharefyx 4.0.0“ + Zeichen | — |

Die 4 braucht ≈ 16–18 Kacheln; 12 Szenen + Zwischenzustände (z. B. S2 vorher/nachher) füllen sie.
**Ob eine 4 aus 16:9-Kacheln bei 1080p lesbar ist, entscheidet ein Standbild (16.2) — vor jedem
Volllauf.** Texttafeln sind Vorschläge; der Wortlaut ist Sache der Sichtung.

## §4 Datenschutz-Checkliste (Q6) — vor jedem Volllauf abhaken

- Principals, Spaces, Notizen: **erfunden und neutral** (keine echten Personen; die Leiste zeigt
  den angemeldeten Namen — er ist erfunden).
- **Keine** Browserleiste, keine URL, kein Hostname, keine Domain im Bild.
- Transkript der KI-Szene **vor** der Wiedergabe bereinigt: keine MCP-URL, kein Token, kein
  Auth-Header (Prüfung per `grep` in 16.3, Ergebnis im Session-Block).
- Keine Fremdmarken (Namen, Logos) — auch nicht in der KI-Kachel.
- Review-Fixes nur allgemein („Befunde aus einem Code-Review behoben“), keine Einzelheiten.

## §5 Schritte — je Schritt ein Commit, Head im selben Commit (Hard Rule 8)

Quelle im Repo unter `phase10_5_finishing/film/` (Bühne, Aufnahme-, Saat-, Ton-, Render-Skript);
Aufnahmen und MP4 **außerhalb** (`~/sharefyx-film/`). Wegwerf-Instanz über
`phase10_inventory/probes/p10_wegwerf.py` (eigener Port, tmp-`DATA_ROOT`/`auth.sqlite3`,
File-Keyring, Umgebung ohne `SHAREFYX_*`/`SFX_*`, Stopp nur über die PID-Datei — Hard Rule 9).

| Schritt | Inhalt | Fertig, wenn |
|---|---|---|
| **16.0** Probe | `film-venv` (Playwright vorhanden, `imageio-ffmpeg`, numpy); Bühne mit zwei Platzhalter-Kacheln + einem echten UI-Standbild; 2 s rendern, **zweimal** | `libx264` vorhanden · beide Läufe **byteweise gleiche** Frame-Hashes · Sekunden je Frame gemessen · Platte: keine Frame-Dateien |
| **16.1** Aufnahmen | Saatdaten (§4), Wegwerf-Instanz, Playwright nimmt S1–S12 auf (2×, Bildfolgen für Tippen/Karte); KI-Lauf aufzeichnen + bereinigen | alle Kacheln als Bilder da · Checkliste §4 Punkte 1–4 ✓ |
| **16.2** Standbilder | drei Schlüsselbilder: Anfang (Leiste), mitten in der Fahrt, **die 4.0.0** | **Sichtung Nikinger** — vorher kein Volllauf |
| **16.3** Zeitleiste | volle `frame → Zustand`-Funktion, Easing, Texttafeln; Wächter: Determinismus (zwei Läufe, Hash) + Kacheln der 4 im Bild | pytest grün · Vorschau (niedrige Auflösung) ansehbar |
| **16.4** Ton | Ton-Skript, Marken aus der Zeitleiste | WAV deterministisch (Hash) · **Sichtung Nikinger** |
| **16.5** Render | Volllauf §3.3, MP4 nach `~/sharefyx-film/`, SHA-256 in den Commit; **Minimalfassung** als Rückfall: die 4-Fahrt mit 8 Kacheln, ohne KI-Szene und ohne Ton, 40 s | Kriterien §6 · Freigabe Nikinger |

## §6 Kriterien (planintern — Abnahmezeilen P10.5-80 ff. nur, wenn der Nikinger sie will)

| # | Kriterium |
|---|---|
| L1 | Determinismus: derselbe Frame-Bereich zweimal gerendert ⇒ identische Hashes |
| L2 | 1920 × 1080, 60 fps, H.264 CRF ≤ 18, `yuv420p`, aus 2×-Aufnahme; kein sichtbares Banding (Sichtung) |
| L3 | Länge 40–60 s |
| L4 | Checkliste §4 vollständig ✓ |
| L5 | jede gezeigte Funktion existiert in HEAD an der Wegwerf-Instanz |
| L6 | Standbilder (16.2) und Film (16.5) vom Nikinger abgenommen |
| L7 | Quelle im Repo, pytest grün; MP4 außerhalb, SHA-256 notiert |

**Herkunft:** der Nikinger erinnert eine frühere Session zum Film. Im Repo, im Memory und im
Sharefyx-Space fand sich am 2026-10-29 **nichts** — falls es sie gibt, ist sie die bessere Quelle.
