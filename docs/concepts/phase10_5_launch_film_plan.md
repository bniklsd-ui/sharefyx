---
status: live
purpose: Plan Block 16 „Launch-Film“ für Sharefyx v4.0.0 — Auftrag, Antworten des Nikingers (2026-10-31), Material, Technik (Frame = Funktion des Index), Storyboard mit der „4“, Schritte 16.0–16.5, Kriterien.
read-when: Arbeiten am Launch-Film — zuerst §1 (Antworten) und §5 (Schritte)
detail: L2
up: ../../phase10_5_finishing/CLAUDE.md
down:
  - ../UPDATE_LOG.md   # die Quelle der Feature-Liste (Blöcke 2026-10-23 bis 2026-10-26)
updated: 2026-11-01 (Schritt 16.7 ✅ — blaues Raster, Parallaxe, Vignette) | 2026-11-01 (Schritt 16.6 ✅ — Urknall-Auftakt, Zeitleiste relativ) | 2026-11-01 (§7 Sichtung 1 wörtlich + Runde 2: Urknall, Raster, 3D + Text, schneller) | 2026-11-01 (Schritt 16.5 🔄 — Volllauf fertig, Sichtung offen) | 2026-11-01 (Schritte 16.3/16.4 ✅ — Vorschau, Feinschliff, Ton) | 2026-11-01 (Schritt 16.2 ✅ — Bühne, Schlüsselbilder selbst geprüft) | 2026-11-01 (Schritt 16.1 ✅ — Aufnahmen, Funde: Ordner-Menü, clip.scale > 2) | 2026-11-01 (Schritt 16.0 ✅ — Probe: 2× über clip.scale, zwei Läufe byteweise gleich) | 2026-11-01 (Freigabe + Nachtrag N1–N3: Morph zur Schrift, 3 → 4, Sichtung = ganzer Film) | 2026-10-31 (Plan, Claude Code — Notiz zum Plan Block 16 ausgebaut: Antworten Q1–Q7/QA–QC, Material neu, Storyboard, Schritte) | 2026-10-29 (notiert, Claude Code — Reihenfolge: erst das Ultra-Review, dann die Planung des Films)
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

> **Freigabe + Nachtrag (Nikinger, 2026-11-01, wörtlich):** „Approved. of course, once the ‚4' is
> roughly formed, you need to add some morph / transition in order to ‚make' it into real text,
> you know — i´d also suggest ‚transforming' the old UI into the new one, but only if it fits the
> rest of the movie. I generally like the ‚creative' vision of Opus, so if you have something
> better in mind, im all for it. ill watch the whole video as review.“

**Stand:** **freigegeben 2026-11-01**, 16.0 läuft. **Zeit:** der Film
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
| QC | Wer baut? | **Claude Code** (Opus) | Standbilder prüft Claude Code selbst (16.2) |
| N1 | (2026-11-01) die grobe 4 → echte Schrift | Morph Pflicht | §3.5 „Finale“ |
| N2 | (2026-11-01) alte UI → neue UI | „nur wenn es passt“ | passt: der Film erzählt **3 → 4** (§3.5) |
| N3 | (2026-11-01) Sichtung | **der ganze Film** | eine Abnahme am Ende (16.5), keine Zwischen-Sichtung |

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

**Finale (N1) — von Kacheln zu Schrift.** Sobald die Kacheln die 4 grob bilden, zerfallen sie in
Punkte (dieselbe Punktsprache wie die Karte); die Punkte fliegen auf Stichproben **innerhalb** der
gesetzten Glyphe „4.0.0“ (Text in eine Offscreen-Leinwand gerendert, Punkte daraus gezogen,
fester Seed), verdichten sich, und die Glyphe blendet als **echte Schrift** voll auf. Alles aus
`frame` berechnet, kein Zufall zur Laufzeit.

**3 → 4 (N2) — der Film erzählt den Versionssprung.** Anfang: die Leiste zeigt die **alte**
Versionsangabe (`v3.1.6`, live seit 2026-10-23), die Ziffern rollen auf `v4.0.0`. In der Fahrt
kommen **drei** Kacheln im alten Aussehen an — Editor (Textfeld + „Rohtext“), Knopfleiste, Karte
(vor C2) — und ein Lichtstreif zieht darüber und hinterlässt die neue UI. Nur drei, damit der
Rhythmus nicht kippt. Die alte UI stammt aus einer zweiten Wegwerf-Instanz aus einem
`git worktree` auf **`e5c834e`** (Deploy B, `v3.1.6`) mit **denselben** Saatdaten; der Worktree liegt
außerhalb des Repos und wird danach entfernt.

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
| **16.0 ✅** Probe | `film-venv` (Playwright vorhanden, `imageio-ffmpeg`, numpy); Bühne mit zwei Platzhalter-Kacheln + einem echten UI-Standbild; 2 s rendern, **zweimal** | `libx264` vorhanden · beide Läufe **byteweise gleiche** Frame-Hashes · Sekunden je Frame gemessen · Platte: keine Frame-Dateien |
| **16.1 ✅** Aufnahmen | Saatdaten (§4), Wegwerf-Instanz, Playwright nimmt S1–S12 auf (2×, Bildfolgen für Tippen/Karte); KI-Lauf aufzeichnen + bereinigen | alle Kacheln als Bilder da · Checkliste §4 Punkte 1–4 ✓ |
| **16.2 ✅** Standbilder | drei Schlüsselbilder: Anfang (Leiste), mitten in der Fahrt, **die 4.0.0** (Kacheln und Schrift) | Claude Code prüft (Lesbarkeit der 4 bei 1080p) — vorher kein Volllauf (N3) |
| **16.3 ✅** Zeitleiste | volle `frame → Zustand`-Funktion, Easing, Texttafeln; Wächter: Determinismus (zwei Läufe, Hash) + Kacheln der 4 im Bild | pytest grün · Vorschau (niedrige Auflösung) ansehbar |
| **16.4 ✅** Ton | Ton-Skript, Marken aus der Zeitleiste | WAV deterministisch (Hash) |
| **16.5 ✅** Render (Sichtung 1 gefahren → Runde 2, §7) | Volllauf §3.3, MP4 nach `~/sharefyx-film/`, SHA-256 in den Commit; **Minimalfassung** als Rückfall: die 4-Fahrt mit 8 Kacheln, ohne KI-Szene und ohne Ton, 40 s | Kriterien §6 · Freigabe Nikinger |

## §6 Kriterien (planintern — Abnahmezeilen P10.5-80 ff. nur, wenn der Nikinger sie will)

| # | Kriterium |
|---|---|
| L1 | Determinismus: derselbe Frame-Bereich zweimal gerendert ⇒ identische Hashes |
| L2 | 1920 × 1080, 60 fps, H.264 CRF ≤ 18, `yuv420p`, aus 2×-Aufnahme; kein sichtbares Banding (Sichtung) |
| L3 | Länge 40–60 s |
| L4 | Checkliste §4 vollständig ✓ |
| L5 | jede gezeigte Funktion existiert in HEAD an der Wegwerf-Instanz |
| L6 | der ganze Film vom Nikinger abgenommen (N3) — Sichtung 1 (2026-11-01): „nicht schlecht“, drei Wünsche ⇒ Runde 2 (§7) |
| L7 | Quelle im Repo, pytest grün; MP4 außerhalb, SHA-256 notiert |

**Herkunft:** der Nikinger erinnert eine frühere Session zum Film. Im Repo, im Memory und im
Sharefyx-Space fand sich am 2026-10-29 **nichts** — falls es sie gibt, ist sie die bessere Quelle.

## Anmerkungen 16.0 — Probe (2026-11-01, Opus)

- **Gebaut:** `film/stage.js` (reine Funktionen: Easing, `phase()`, PRNG mulberry32, Kamera,
  Körnung), `film/probe.html` (2 s, zwei Platzhalter + ein echtes UI-Bild), `film/render.py`
  (HTTP nur auf 127.0.0.1, drei Wurzeln `/film` `/static` `/still`, sonst nichts; CDP-Aufnahme →
  `image2pipe` → ffmpeg). Werkzeug-venv `~/.claude-code-tools/film-venv` (Playwright 1.62.0 —
  dieselbe Version wie `e2e-venv`, nutzt dessen Chromium —, `imageio-ffmpeg` 7.0.2 mit `libx264`).
- **Fund:** `device_scale_factor=2` am Kontext reicht **nicht** — `Page.captureScreenshot` liefert
  trotzdem 1920 × 1080. **`clip.scale = 2`** rastert neu (3840 × 2160); im Augenvergleich so scharf
  wie `--force-device-scale-factor=2`, ein hochgerechnetes 1×-Bild ist sichtbar weich.
- **Gemessen (2×):** zwei Läufe ⇒ **gleiche Bild-Hashes und byteweise gleiche MP4**
  (`84c60a9a…`); **0,36 s je Bild** ⇒ Volllauf 54 s ≈ **19 min**; keine Frame-Dateien auf der Platte.
  Beleg `probes/p105_b16_0_probe.json`.
- **Wächter:** `tests/test_film_stage.py` (9: PRNG, `phase`, Kamera, Pfadschutz des
  Render-Servers); Gegenlauf (PRNG → `Math.random`, Pfadschutz entfernt) **4 rot**.

## Anmerkungen 16.1 — Aufnahmen (2026-11-01, Opus)

- **Werkzeug:** `film/wegwerf.py` (zwei Instanzen mit derselben erfundenen Saat — `neu` = HEAD,
  Port 8811; `alt` = `v3.1.6` aus `git worktree` auf `e5c834e`, Port 8812, alter Code über
  `PYTHONPATH` vor den *editable*-Findern; Badges gemessen `v4.0.0` / `v3.1.6`), `film/capture.py`
  (Fenster 1600 × 1000, `clip.scale = 2`), `film/ki_lauf.py` (S9).
- **Reihenfolge für einen sauberen Lauf** (die Szenen schreiben in die Saat — S7 benennt
  `projekte` um, S9 hängt an): je Instanz `stop` → Baum löschen → `setup` → `start`; dann
  `capture.py neu`, `capture.py alt`, zuletzt `ki_lauf.py`. Alles unter `~/sharefyx-film/` (40 MB).
- **Bestand:** neu S1–S8, S10–S12 (S2 = 107 Tippbilder), alt S1/S2/S5; S9 = echtes Transkript
  (`list_spaces`, `search_items`, `append_to_items` ⇒ 3 × `ok`, Version 3 → 4), geprüft: kein
  Token, keine URL, kein Host, kein `Bearer`.
- **Funde:** (1) „Umbenennen“ im Ordner-Menü öffnete nie den Dialog — eigener Commit `68eff7e`,
  Probe 4/4, Gegenlauf 3 rot. (2) Ein **Teil**ausschnitt mit `clip.scale` > 2 ignoriert den
  Ausschnitt (das ganze Fenster wird hineingequetscht, gemessen bei 4/5/6/8/10) ⇒ der Zoom aus
  der Marke wird auf der Bühne als **Vektor** gebaut (`logo.svg`, Plex, Lage aus
  `~/sharefyx-film/s1_*.json`); die Vollbild-Aufnahme bei 2× bleibt scharf (16.0). (3) v3.1.6
  öffnet den Editor in der Vorschau — Aufnahme schaltet über `#toggle-preview` um.
  (4) `scripts/move_sections.py` bricht mit `StopIteration` ab (nichts geschrieben) — nicht
  angefasst, Head stattdessen über `rotate_index_updates.sh` entlastet.
- **Für die Bühne gemessen:** der Versionsstreifen links im Editor zeigt „v1“ hochkant und
  beschnitten (sieht aus wie „\\“) — Produktgestaltung, kein Fehler; in der Kachel klein.

## Anmerkungen 16.2 — Bühne und Standbilder (2026-11-01, Opus)

- **Gebaut:** `film/film.js` (rein: Kacheln, Halte, Kamera, `zustand(n, geo)`; 3300 Bilder =
  55 s) und `film/film.html` (DOM + Punkte-Leinwand + gesetzte Glyphe). `render.py` wartet jetzt
  auf ein Promise aus `renderFrame` (Bildwechsel per `img.decode()`), `--nur-stills`.
- **Die 4:** 13 Kacheln im Raster 4 × 7 (Abstrich (1,1)(1,2)(0,3), Querstrich Zeile 4, Senkrechte
  Spalte 2). Fahrt mit Zoom-Knick zwischen den Halten, Kacheln leicht versetzt/gedreht (fester
  Seed); heraus zur **großen** 4 (88 % Bildhöhe), dort ordnen sie sich; im Morph gleitet die Kamera
  auf die Lage der Glyphe „4“ (aus der gesetzten Schrift gemessen), die Kacheln zerfallen in Punkte,
  die Punkte fliegen auf die Tinte von „4.0.0“ (Raster 14 px bei 1000 px Schrift), die Schrift
  blendet auf (N1).
- **3 → 4 (N2):** Anfang in der Vektor-Marke (Werte von `.rail__brand` gemessen), Ziffern rollen
  `v3.1.6` → `v4.0.0`, Kacheln erst unter 3× Zoom (die Aufnahme ist 2×); Lichtstreif alt → neu an
  s1 (Übersicht), s3 (Editor: Rohtext v3.1.6 → Live-Editor) und s5 (Karte).
- **Selbst geprüft (N3), zehn Schlüsselbilder:** die 4 aus Kacheln ist bei 1080p **lesbar**; der
  Zoom aus der Marke war in der ersten Fassung weich (Bitmap hinter dem Vektor) — behoben durch das
  Einblenden erst unter 3×. Wächter `tests/test_film_stage.py` +4 (rein, Halte, Ordnen, Streif);
  Gegenlauf „Ordnen nie fertig“ 1 rot.

## Anmerkungen 16.3/16.4 — Vorschau, Feinschliff, Ton (2026-11-01, Opus)

- **Vorschau** des ganzen Films bei 1× (3300 Bilder, 0,13 s/Bild) und als Kontaktbögen alle 1,5 s
  gesichtet. Nachgeschärft: erste Tafel erst ab dem Editor (Bild 330, nicht über der Übersicht) ·
  beim Ordnen leuchten die Kachelränder auf (die dunklen UI-Kacheln verschwammen mit dem Schwarz) ·
  der Abstrich liegt auf den Spalten 1,0 → 0,6 → 0,2 (vorher drei Stufen: Treppe statt Schräge).
- **Saubere Aufnahme vor dem Volllauf:** Saat neu, `capture.py neu` + `alt` in Szenenreihenfolge,
  `ki_lauf.py` — vorher zeigte S1 schon den umbenannten Ordner aus S7 und S9 hatte doppelt angehängt.
- **Ton (`film/ton.py`):** Fläche (D-Dur mit None), Glocke je Kamera-Ankunft, Anschwellen im Zoom
  heraus, Glitzern im Morph, Schlussakkord; Marken aus `film.js` über Node. Zwei Läufe ⇒ dieselbe
  WAV (`e55b591e…`); Pegel ≈ −16 dB RMS, Spitze −1 dBFS. **Gehört hat ihn noch niemand** — das Urteil
  ist Teil der Sichtung (N3). `render.py --ton` mischt ihn als AAC dazu (Bild kopiert).

## Anmerkungen 16.5 — Volllauf (2026-11-01, Opus)

- **Film:** `~/sharefyx-film/sharefyx-4.0.0.mp4` (außerhalb des Repos) — 55,0 s, 1920 × 1080,
  60 fps, H.264 High `yuv420p` (CRF 17, aus 2×-Aufnahme), AAC Stereo 48 kHz, **19.200.339 B**,
  SHA-256 `4ad60f966bfc1d9781f6323953d3761e31b8e68a0b5e0b2c7838a8dcb90b8085`; Bild-Hashkette
  `f76a421d…`; Ton `e55b591e…`. 0,54 s/Bild (≈ 30 min).
- **Kriterien:** L1 ✅ (16.0 byteweise; Ton zwei Läufe gleich) · L2 ✅ Zahlen (Banding-Urteil in der
  Sichtung) · L3 ✅ 55 s · L4 ✅ (erfundene Saat, keine Browserleiste/URL, Transkript geprüft, keine
  Fremdmarke, Review-Fixes nicht genannt) · L5 ✅ (jede Kachel ist eine Aufnahme von HEAD bzw.
  v3.1.6) · L6 ⬜ **Sichtung des ganzen Films beim Nikinger (N3)** · L7 ✅ (Quelle im Repo, pytest
  grün, MP4 außerhalb, SHA-256 hier).
- **Für die Sichtung vorgemerkt:** das Terminal schreibt „Eintraege“ (die Mono-Schrift ist ein
  Teilsatz, gewählt wurde ASCII) — eine Zeile in `film.html :: terminalZeilen()`, falls gewünscht.
  Änderungswünsche gehen über die Zeitleiste in `film.js` (rein, Wächter) und einen neuen Volllauf.

## §7 Sichtung 1 und Runde 2 (Nikinger, 2026-11-01)

> **Wörtlich:** „Wow, honestly, not bad. Really not bad. Only three things i have to say:
> 1. the start is not that good, its seems buggy. I suggest using something similar as the big bang
> or an opening eye or something instead (see screenshot)
> 2. Black background seems unfinished - maybe add a slightly visible blue grid as background or
> something similar
> 3. Motion: most screenshots feel like a static diashow and some dont really get the viewer to
> realize the new effect. 3 Changes: use the not filled screen and add a short animated text.
> animate the screenshots / videos itselfs, a 3D effect with slight rotation is something i did as
> an editor, but just as an idea. Make the scenes slightly faster. the Renew effect you already
> have + the text would be a great match, in my opinion.“
> Screenshot: das Anfangsbild (angeschnittenes „x“, „v3.1.6“ frei im Schwarz) — abgelegt unter
> `~/sharefyx-film/sichtung1_anfang.png`.

**Befund zum Anfang (am Bild nachvollzogen):** die Kamera steht auf der Mitte der Versionsangabe;
vom Namen ist nur das angeschnittene „x“ zu sehen — wirkt wie ein Darstellungsfehler, nicht wie
ein Auftakt.

| Schritt | Inhalt | Fertig, wenn |
|---|---|---|
| **16.6 ✅** Auftakt | Ersetzt den Zoom aus der Marke: ein **Urknall** — ein Lichtpunkt auf Schwarz, der in die Punktwolke aufbricht (dieselbe Punktsprache wie das Finale: der Film beginnt mit Punkten, die auseinanderfliegen, und endet mit Punkten, die „4.0.0“ bilden); die Punkte ordnen sich zur Marke / zur ersten Kachel. Alternative „sich öffnendes Auge“ nur, falls der Urknall im Standbild nicht trägt. Die Ziffernrolle `v3.1.6` → `v4.0.0` bleibt, aber **ganz** im Bild (Name + Version, nicht angeschnitten) | drei Standbilder des Auftakts selbst geprüft; nichts angeschnitten |
| **16.7 ✅** Hintergrund | dezentes blaues Raster (Linien ≈ `rgba(62,141,243,.06–.08)`, Weltkoordinaten ⇒ es zieht mit der Kamera, Parallaxe), Vignette; die Körnung bleibt | Standbild Fahrt + große 4: Raster sichtbar, nicht laut |
| **16.8** Bewegung + Text | (a) die Kachel füllt das Bild nicht mehr: kleiner (≈ 60–65 % Breite), im Raum leicht **3D-gedreht** (`perspective` + `rotateY/rotateX`, driftet während des Halts, Push-in) — die Aufnahmen „leben“; (b) der freie Platz trägt je Szene einen **kurzen animierten Text** (Titel + eine Zeile, Wort für Wort / Zeile für Zeile eingeblendet), gekoppelt an den **Lichtstreif** (Text erscheint mit dem Streif); die Unterzeilen-Tafeln entfallen oder werden zu diesen Texten; (c) **schneller**: Halte ≈ −25 %, Film ≈ 42–48 s; (d) die Szenen, deren Effekt nicht ankommt, gezielt zeigen (Suche: Treffer heranzoomen; S5b ggf. streichen) | Vorschau ganz gesichtet; jede Szene hat ihren Text; Länge 40–60 s |
| **16.9** Volllauf 2 | Volllauf wie 16.5 (+ „Einträge“ statt „Eintraege“ prüfen: hat der Mono-Teilsatz `ä`?) | **Sichtung 2** beim Nikinger |

**Leitplanken bleiben:** jedes Bild eine Funktion seiner Nummer (`film.js` rein, Wächter), echte
UI aus den Aufnahmen (keine erfundene), §4 Datenschutz, Ton aus `ton.py` (Marken folgen der neuen
Zeitleiste automatisch). Neue Aufnahmen nur, wenn eine Szene sie braucht (z. B. Suche näher).

## Anmerkungen 16.6 — Auftakt (2026-11-01, Opus)

- **Vorab: die Zeitleiste ist relativ.** `film.js :: FAHRT` trägt je Kachel Halt + Fahrt; Streif,
  Bildfolge, Wechsel und Terminal zählen ab dem Halt; `HALTE`, `KACHELN`, `ZOOM_AUS`, `MORPH`, `ENDE`,
  `FRAMES` werden abgeleitet (gleiche Namen und Formen — `ton.py` liest sie weiter). **Beleg:** mit den
  alten Dauern ist `zustand(n)` für **alle 3300 Bilder** gleich der alten Datei (0 Unterschiede).
- **Urknall** (`AUFTAKT` in `film.js`): Funke (Bild 10–46) → Blitz + Knall (46) → 485 Punkte fliegen
  auseinander (+ 1400 Staubpunkte, die nur verglimmen) → sammeln sich zur **ganzen** Marke (Zeichen,
  Name, Version; Zielpunkte aus der Tinte der gesetzten Marke, Raster 7 px) → die Marke blendet auf →
  Ziffernrolle 3.1.6 → 4.0.0 **groß in der Bildmitte** → die Marke landet in der Leiste von s1 (alte
  UI), der Streif macht die Kachel neu. **Eine** Punkt-Zeichenart für Auftakt und Finale
  (`film.html :: punkteZeichnen`).
- **Mitte = Tinte, nicht Kasten:** der Kasten der Leiste (239 px) ist breiter als seine Tinte
  (117 × 17 px) — gemessen in der Bühne (`filmGeo.markeBox`); gerendert: Tinte 830 px breit, Mitte
  (958,5 / 520). Standbilder 30–420 selbst geprüft, nichts angeschnitten.
- **Wächter** (`tests/test_film_stage.py`): die Tinte liegt in **jedem** Bild des Auftakts mit 20 px
  Rand im Bild und ist ≥ 800 px breit; gelandet sitzt sie im Maßstab der Kamera auf dem Kachelpunkt
  (0, 8). **Gegenlauf** (`MARKE_GROSS` = 34, der alte Zoom): genau dieser Wächter rot.
- **Ton:** Sog zum Funken + tiefer Schlag mit Rauschen auf dem Knall (`ton.py`, Marken aus
  `AUFTAKT`); zwei Läufe byteweise gleich; Pegel Knall-Spitze 0,89, Fahrt −18,8 dB RMS.

## Anmerkungen 16.7 — Hintergrund (2026-11-01, Opus)

- **Raster** auf einer eigenen Leinwand **hinter** der Welt, aus `cam` berechnet (`film.js :: raster`):
  Parallaxe 0,5 (es zieht halb so schnell wie die Kacheln); die Dichte bleibt bei jedem Zoom gleich —
  Abstand auf dem Bild in [80, 160) px, die feinen Linien blenden stetig ein. Linien im Knopf-Blau
  `#3E8DF3`, Deckkraft **0,14** — **gemessen am dekodierten MP4-Bild**: bei 0,075 kamen die Linien mit
  8–12/255 an (kaum da), bei 0,14 sichtbar, aber leise. Erscheint mit dem Knall (eine hellere Welle
  läuft von der Mitte aus), tritt im Morph auf 25 % zurück. **Vignette** (Ränder dunkler) als feste
  Ebene über den Kacheln, unter Text und Punkten. Körnung bleibt.
- **Wächter:** Dichte über **alle** Bilder · Parallaxe 0,5 · Erscheinen/Zurücktreten. **Gegenlauf:**
  ohne Stufen (`abstand = roh`) und mit Parallaxe 1 — genau die zwei Wächter rot.
- **Renderzeit:** die Messung schwankt mit der Last der VM (derselbe Bereich 0,15–0,48 s/Bild, auch
  ohne Raster) — kein messbarer Mehraufwand durch das Raster.

