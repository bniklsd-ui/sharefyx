---
status: live
purpose: Plan P10.5 Block 16 — der Launch-Film „Sharefyx 4.0" (≈ 40 s, Deutsch, mit Code gerendert) und seine Wiedergabe in der App (erster Start im Vollbild, Wiederaufruf im Update-Log). Storyboard, Werkzeugweg (Playwright-Frames + ffmpeg, Rückfall Remotion), Server- und UI-Teil, Schritte 16.0–16.6, Abnahme P10.5-89–92. Ersetzt die Notiz vom 2026-10-29; Locks P10.5-AH–AM.
read-when: vor dem Bau von Block 16, bei jeder Änderung an der Film-Wiedergabe in der App, oder wenn der Film neu gerendert wird
detail: L2
up: ../../phase10_5_finishing/CLAUDE.md
down:
  - phase10_5_block15_ultra_plan.md              # 📕 Block 15 — läuft vor diesem Block; §2 Arbeitsregeln, §6 [VERIFY] V225–V232
  - ../UPDATE_LOG.md                             # die Quelle der Feature-Liste (Blöcke 2026-10-23 bis 2026-10-26)
  - ../../phase5_ui/webui/static_routes.py       # Muster für die Medien-Route (Sitzungs-Gate, Pfadprüfung)
  - ../../phase5_ui/webui/static/js/updates.js   # Update-Log-Panel — dort sitzt der Wiederaufruf
  - ../../phase10_5_finishing/probes/p105_b14_karte_bilder.py   # Wegwerf-Saat 5 Spaces/152 Items, Login, Settle — Muster für die Aufnahmen
updated: 2026-10-30 (Plan — die Antworten des Nikingers B1–B8 vom 2026-10-30: ein Film ≈ 40 s mit Luft, Deutsch, alle Sharefyx-Nutzer, echte Oberfläche + stilisierte Ebene, In-App-Wiedergabe mit Mehraufwand akzeptiert, Musik optional, Budget eine Woche; Werkzeugwahl Playwright-Frames + ffmpeg mit Rückfall Remotion — Entscheidung der Planungssession auf Nachfrage) | 2026-10-29 (notiert, Claude Code — Reihenfolge: erst das Ultra-Review, dann die Planung des Films)
---
# P10.5 Block 16 — Launch-Film „Sharefyx 4.0"

> **Auftrag (Nikinger, 2026-10-29, wörtlich):** „im Grunde genommen ein mit Code generierter
> ‚Product Launch' Film zu sharefyx 4.0.0, mit all den neuen Features. Dabei soll der Film an die
> existierenden Launches von Antrophic / OpenAi angelehnt sein, und künstlerisch die neuen
> Features, Bug fixes und verbesserungen zeigen, länge 40s - 1min."
> Nachtrag: „nur die Notiz für den Plan — dazu werden sicherlich Fragen aufkommen, die ich
> separat klären möchte. Externe Tools sind erlaubt."
>
> **Antworten (2026-10-30):** B1 **ein** Film, Zieldauer **40 s** „mit Luft nach oben oder unten",
> umfangreicher als das 20–30-s-Intro der ROADMAP-Notiz vom 2026-10-26; die beiden Eigenschaften von
> dort bleiben: **beim ersten Start im Vollbild**, danach **im Update-Log** wieder aufrufbar; Block 16
> von P10.5, keine Phase P10.6 · B2 echte Oberfläche von der Wegwerf-Instanz in einer stilisierten
> Ebene · B3 Werkzeug: Empfehlung der Planungssession (§0 P10.5-AJ) · B4 Publikum alle
> Sharefyx-Nutzer, **Deutsch** · B5 Musik optional · B6 In-App-Wiedergabe, Mehraufwand akzeptiert ·
> B7 KI-Szene nachgestellt mit echter Werkzeugantwort · B8 Abnahme wie vorgeschlagen, Video darf
> auch durch Code erzeugt sein · Zeitbudget **eine Woche**.

## §0 Entscheidungen (Locks P10.5-AH–AM)

| Lock | Entscheidung | Herkunft |
|---|---|---|
| **P10.5-AH** | **Ein Film, Ziel 40 s, Korridor 30–50 s, Deutsch.** 1920 × 1080, 30 fps, H.264 (`yuv420p`, `+faststart`) als Pflichtformat, WebM optional. Publikum: alle Sharefyx-Nutzer (heute zwei) — kein zweiter Schnitt für außen. | Nikinger B1/B4 |
| **P10.5-AI** | **Inhalt = echte Oberfläche + stilisierte Ebene.** Aufnahmen stammen ausschließlich von einer Wegwerf-Instanz mit der Block-14-Saat (5 Spaces, 30/32/30/30/30 Items, feste Uhr); keine echten Notizen, kein `DATA_ROOT`. Die Bewegungsebene nutzt die Mittel des Produkts (IBM Plex, Lucide-Sprite, `logo.svg`, Farb-Tokens aus `app.css`). **Kein generatives Video für Oberflächen** — es würde UI erfinden; die KI-Szene zeigt eine **echte** `list_spaces`-Antwort in nachgestellter Darstellung, ohne nachgebaute Fremd-Oberfläche. | Nikinger B2/B7 |
| **P10.5-AJ** | **Werkzeugweg: Playwright-Frames + ffmpeg; Rückfall Remotion.** Die Szenen sind eine HTML/CSS-Seite mit einem deterministischen Takt (Web Animations API, `currentTime` je Frame); Playwright (Chromium aus `~/.claude-code-tools/e2e-venv`) schreibt je Frame ein PNG, `ffmpeg` kodiert. Keine neue Lizenz, kein Node-Toolchain, dieselbe Technik wie die Sichtprüfungs-Proben. **Rückfall Remotion** (Node, `~/.claude-code-tools/launch-film/`, außerhalb des Repos) greift nur bei den Auslösern in §7 — und dann mit Lizenzprüfung (V231). Quelle im Repo unter `phase10_5_finishing/film/`; Clips, Frames und Render **nicht** in Git (`.gitignore`), Ablage Drive + VM. | Planungssession auf Nachfrage B3 |
| **P10.5-AK** | **In-App-Wiedergabe.** Beim ersten Anmelden nach Deploy D ein Vollbild-Overlay (stumm, `playsinline`, Knopf „Überspringen/Schließen"); gesehen-Zustand serverseitig je Nutzer (`users.seen_film_id`, additive Spalte wie `seen_update_id`); Wiederaufruf über einen Knopf im Update-Log-Panel. Medien liegen **außerhalb** von `static/` in `UiSettings.media_dir` (Umgebung `SPACE_UI_MEDIA_DIR`), bedient von `GET /ui/media/{name}` (Sitzungs-Gate, `FileResponse` mit `Range`); CSP bekommt `media-src 'self'`. **Fail-soft:** fehlt Verzeichnis, Manifest oder Datei, gibt es kein Overlay und keinen Fehler. | Nikinger B6 |
| **P10.5-AL** | **Ton.** Der Pflicht-Film ist stumm (Browser blockieren Autoplay mit Ton; In-App ohnehin stumm). Musik ist Schritt 16.6, optional, nur mit lizenzfreier Quelle (CC0), als zweite Datei gemuxt — der stumme Film bleibt die Abnahmefassung. | Nikinger B5 |
| **P10.5-AM** | **Abnahme und Zeit.** Zwei Sichtungen des Nikingers (E1 Storyboard/Textkarten, E2 Film), vier messbare Zeilen P10.5-89–92. Budget **eine Woche** ab 16.0; Reihenfolge nach Block 15, vor Deploy D. **Reißt die Woche, gilt C1:** Deploy D zuerst, der Film kommt als `v4.0.1` — das entscheidet der Nikinger am Ende der Woche, nicht der Ausführer. | Nikinger B8/C1 |

## §1 Storyboard (Entwurf für die Sichtung E1 — 16.0)

Zeiten in Sekunden bei 30 fps (1200 Frames für 40 s). Jede Textkarte ist **ein** Satz, kurz, ohne
Ausrufezeichen — die Form der großen Launch-Filme: dunkler Grund, viel Luft, ein Gedanke je Bild.
Fonts: IBM Plex Sans (Karten), IBM Plex Mono (Werkzeugantwort). Grund: `--bg` der App (OLED-Schwarz),
Akzent `--accent`.

| # | Zeit | Bild | Textkarte (wörtlich) | Aufnahme |
|---|---|---|---|---|
| 1 | 0,0–4,0 | Das Zeichen zeichnet sich (Leuchtbahn, `logo.svg` als Strich-Animation), Wortmarke blendet ein, darunter die Version | „Sharefyx" · „Version 4.0" | keine |
| 2 | 4,0–9,0 | Langsame Kamerafahrt über die Übersicht (Ken-Burns, 4 % Zoom) | „Ein Aktenschrank. Für zwei Menschen und ihre KI." | Clip `uebersicht` |
| 3 | 9,0–16,0 | Editor: Tippen im Live-Editor, ein To-do-Kästchen wird geklickt, `[Wichtig]{.rot}` färbt sich beim Schreiben | „Schreiben, wie es im Kopf aussieht." | Clip `editor` |
| 4 | 16,0–23,0 | Gehirnkarte: Öffnen, die Karte sortiert sich, Suche „Projekt" hebt Treffer hervor, Filter, dann die ganze Karte | „Alles hängt zusammen." | Clip `karte` |
| 5 | 23,0–29,0 | Ordner umbenennen, Team-Space umbenennen, Filter „Zugewiesen" — drei kurze Schnitte | „Ordnung, die mitzieht." | Clips `ordner`, `space`, `zugewiesen` |
| 6 | 29,0–35,0 | Eine Monospace-Fläche: `list_spaces` tippt sich, die echte JSON-Antwort erscheint zeilenweise; Badge „MCP 2026-07-28" | „Eine Verbindung. Jeder Anbieter." | `list_spaces.json` (echte Antwort) |
| 7 | 35,0–40,0 | Drei Zeilen erscheinen nacheinander, dann Zeichen + Wortmarke | „Schneller. Sicherer. Fertig." · „Übersicht in einem Durchgang" · „Fotos ohne Standortdaten" · „22 Befunde geschlossen" · „sharefyx 4.0" | keine |

**Übergänge:** weiche Blenden (300 ms), eine Kamerafahrt je Szene, keine Wischer. **Was nicht im
Bild ist:** Space-Namen, Titel oder Texte aus echten Daten (nur die Saat), Adressen, Tokens, das
Journal. **Was E1 entscheidet:** Textkarten wörtlich, Szenenfolge, ob Szene 7 die „22 Befunde" nennt.

## §2 Technik — Aufnahme, Takt, Render, Prüfung

**Verzeichnis `phase10_5_finishing/film/`** (im Repo): `film.html`, `film.css`, `film.js`
(Takt + Szenensteuerung), `capture.py` (Aufnahmen), `render.py` (Frames → Video), `probe.py`
(Messung), `.gitignore` (`assets/`, `frames/`, `out/`). Die Mittel des Produkts werden **referenziert**,
nicht kopiert: `render.py` startet `python -m http.server` auf der Repo-Wurzel (eigener Port), die
Seite lädt `/phase5_ui/webui/static/app.css`, `/phase5_ui/webui/static/fonts/…`, `/phase5_ui/webui/static/logo.svg`.

**16.1 Aufnahme (`capture.py`).** Wegwerf-Instanz wie `p105_b14_karte_bilder.py` (`_setup`, `_seed`,
`_serve`, `_stop`, Login `alpha`, `settle`), Playwright-Context mit `record_video_dir="film/assets/"`,
`record_video_size={"width": 1920, "height": 1080}` (V225), `viewport` 1920 × 1080,
`reduced_motion="no-preference"`. Je Szene ein Skript mit festen Wartezeiten (keine Zufallsdauer):
Übersicht laden · Editor: Item öffnen, tippen (`page.keyboard.type(..., delay=40)`), Kästchen klicken ·
Karte: öffnen, `settle`, Suche tippen, Filter, „ganze Karte" · Ordner/Space umbenennen, Filter
„Zugewiesen". Ergebnis: ein `.webm` je Clip + `assets/MANIFEST.json` (Dateiname, Dauer, SHA-256).
`list_spaces.json`: echte Antwort über den In-Process-Tool-Aufruf wie `mcp_smoke.py`.

**16.2 Szene-Seite und Takt (`film.html/css/js`).** Jede Szene ist ein `<section data-scene data-start
data-end>`; Animationen laufen **ausschließlich** als CSS-Animationen/WAAPI (keine `setTimeout`-Choreo);
Clips sind `<video muted preload="auto">`. `film.js` exportiert `window.film.setTime(ms)`: pausiert alle
`document.getAnimations()` und setzt `currentTime = ms - startOffset`; setzt bei jedem sichtbaren
`<video>` `currentTime = (ms - clipStart)/1000` und wartet auf `seeked`; blendet Szenen über
`data-start/data-end`. Der Browser rendert damit für jedes `ms` denselben Zustand — unabhängig von
Echtzeit (V229).

**16.3 Render (`render.py`).** Playwright: Seite laden, `document.fonts.ready` abwarten, `page.set_viewport_size`
1920 × 1080; `for f in range(1200): page.evaluate("film.setTime(%d)" % round(f*1000/30));
page.screenshot(path="frames/f%05d.png")`; danach
`ffmpeg -framerate 30 -i frames/f%05d.png -c:v libx264 -pix_fmt yuv420p -crf 18 -movflags +faststart out/sharefyx-v4.mp4`
(V226), Poster = Frame 1199 als PNG. Dauer ≈ 1200 × 100 ms + Kodierung.

**Prüfung (`probe.py`, Wächter `tests/test_b16_film_probe.py` liest `probes/p105_b16_film.json`):**
`ffprobe`-Dauer im Korridor 30–50 s, 1920 × 1080, 30 fps, `yuv420p`; **Determinismus:** zwei
vollständige Renders, die Frames 0, 300, 600, 900, 1199 byteweise gleich (SHA-256); **Saat-Regel:**
kein String aus einer Blockliste echter Namen in den Textkarten (Liste in `probe.py`, nur Saat-Namen
erlaubt). Kein Bildurteil durch Code — das ist E2.

## §3 In-App-Wiedergabe (16.4)

**Server.**
- `webui/config.py`: `UiSettings.media_dir: Path | None = None`, geladen aus `SPACE_UI_MEDIA_DIR` auf
  demselben Weg wie `SPACE_UI_LEGACY_ORIGIN` (V232). Manifest `media_dir/film.json`:
  `{"id": "sharefyx-4.0", "file": "sharefyx-v4.mp4", "poster": "sharefyx-v4.png", "duration_s": 40}`.
- `webui/media_routes.py` (neu): `GET /ui/media/{name}` — Sitzung Pflicht (wie `static_routes._index`),
  `name` muss `^[A-Za-z0-9._-]+$` erfüllen und in `media_dir` liegen (Auflösung wie
  `_resolve_static_path`), Antwort `starlette.responses.FileResponse` (Range ✓, V222) mit
  `media_type` nach Endung (`.mp4` → `video/mp4`, `.webm` → `video/webm`, `.png` → `image/png`),
  `Cache-Control: private, max-age=86400`, Sicherheits-Header aus `ui_security_headers()`.
- `webui/api.py`: `GET /api/v1/film` → `{"film": <Manifest oder null>, "seen": <bool>}`
  (`auth_store.get_seen_film_id(space) == film["id"]`); `POST /api/v1/film/seen` (CSRF) → setzt die ID.
- `authserver/store.py`: additive Spalte `users.seen_film_id TEXT` über denselben Mechanismus wie
  `_SCHEMA_V3_COLUMNS` (Schema-Schritt 4; `PRAGMA table_info` vor `ALTER TABLE`), `get_seen_film_id()`,
  `set_seen_film_id()`. Eingriff in `phase4_auth/`: **Freigabe mit B6 (Nikinger 2026-10-30)**, P10-C-Muster.
- `webui/security.py:44`: `media-src 'self'` in die CSP.
- `mcpserver/app.py`: `media_routes(ui_settings, ui_sessions)` neben `static_routes()` mounten.

**UI.**
- `static/js/film.js` (neu, ES-Modul; `app.js` ruft `initFilm()` nach `initUpdates()`): beim Start
  `api("/film")`; ist `film` gesetzt und `seen` falsch → Overlay `#film-overlay` (Markup in
  `app.html`, `hidden`): Vollbild, `<video src="/ui/media/<file>" poster=… autoplay muted playsinline
  controls>`, Knöpfe „Überspringen" (sofort) und „Schließen" (nach Ende); beide → `POST /film/seen`,
  Overlay zu. `Escape` schließt ebenfalls (ohne `seen`? nein — Schließen ist Gesehen).
- Update-Log-Panel (`#settings-updates`, `updates.js`): Knopf „Launch-Film ansehen" (`#update-log-film`),
  nur sichtbar, wenn `film` gesetzt ist → öffnet dasselbe Overlay, ohne `seen` zu ändern.
- `app.css`: Overlay (OLED-Schwarz, Video ≤ 90 vw/vh, Knöpfe `.btn`), `prefers-reduced-motion`
  respektiert (kein Einblend-Effekt).
- **Budget:** die Medien liegen außerhalb von `static/`, `ui_budget` zählt nur `film.js` (≈ 3 KB) zum
  Erstaufruf (Korridor 250 KB, heute ≈ 209 KB).

**Tests.** `phase5_ui/tests/test_media_routes.py` (neu): ohne Sitzung 303; Traversal/ungültiger Name
404; fehlendes Verzeichnis 404; `Range: bytes=0-99` → 206 mit `Content-Range`; MIME je Endung ·
`test_api.py::test_film_is_null_without_a_manifest`, `::test_film_seen_roundtrip` (zwei Spaces getrennt)
· `test_security.py`: CSP enthält `media-src 'self'` · `phase4_auth/tests/test_authserver_store.py::test_schema_adds_seen_film_id_idempotently`
· `phase2_mcp/tests/test_app.py`: Medien-Route durch `create_app()` erreichbar · **Playwright-Probe**
`probes/p105_b16_film_probe.py` (Wegwerf mit Manifest + 2-s-Testvideo): erster Login → Overlay sichtbar,
`<video>` hat `src`; „Schließen" → POST, Reload → kein Overlay; Update-Log → Knopf → Overlay wieder;
Gegenlauf: Manifest entfernen → kein Overlay, keine Konsolenfehler.

**Deploy (Nikinger, vor D4):** `sudo install -d -o savefyx -g savefyx /var/lib/sharefyx-media`,
`sharefyx-v4.mp4` + `sharefyx-v4.png` + `film.json` hineinkopieren, in der Unit
`Environment=SPACE_UI_MEDIA_DIR=/var/lib/sharefyx-media` (Vorlage `phase4_auth/systemd/sharefyx-mcp.service`,
`install_units.sh`-Platzhalter wie `__LEGACY_ORIGIN__`; Leserechte reichen, die Unit härtet `/var/lib`
nur gegen Schreiben — V232 prüft die Unit-Härtung mit). Update-Log-Zeile (16.5).

## §4 Schritte (je Schritt ein Commit, Head im selben Commit)

| Schritt | Inhalt | Fertig, wenn | Tag |
|---|---|---|---|
| **16.0** | Storyboard §1 als Sichtungsvorlage: Textkarten wörtlich, Szenenfolge, Dauer; **V226** (`ffmpeg`/`libx264`), **V225** (Playwright) prüfen; `film/`-Gerüst mit `.gitignore` anlegen. **STOPP E1** — Sichtung der Textkarten durch den Nikinger. | Nikinger: „passt" (ggf. mit Änderungen) | 1 |
| **16.1** | `capture.py`: Wegwerf-Saat, sechs Clips + `list_spaces.json` + `MANIFEST.json` mit Hashes. | Clips vorhanden, Dauer je Clip ≥ Szenenlänge, Manifest stimmt | 1–2 |
| **16.2** | `film.html/css/js`: Szenen, Takt, Standbild je Szene (7 PNGs) als Zwischenstand. | `film.setTime()` liefert für jede Szene ein Standbild; 7 PNGs angesehen (Claude Code), keine Konsolenfehler | 2–3 |
| **16.3** | `render.py` + `probe.py`: zwei Renders, Zahlen nach `probes/p105_b16_film.json`, Wächter `tests/test_b16_film_probe.py`. **Rückfall-Entscheidung** nach §7 spätestens hier. | Dauer, Auflösung, fps, Determinismus grün | 3 |
| **16.4** | In-App (§3): Server, Auth-Spalte, UI, Tests, Playwright-Probe. | Tests grün, Probe grün, `ui_budget` grün, `doc_health` 0 | 4 |
| **16.5** | **STOPP E2** — Sichtung des Films (Drive-Link); bis zu zwei Korrekturrunden (Text, Timing, Schnitt); danach Update-Log-Zeile: „Neu: Ein kurzer Film zeigt, was Version 4.0 bringt — beim ersten Anmelden, später jederzeit im Update-Log." Abnahme P10.5-89–91. | Nikinger nimmt den Film ab | 5 |
| **16.6** | **Optional:** Musik (CC0-Quelle, Nachweis im Session-Block), `ffmpeg -i film.mp4 -i musik.* -c:v copy -c:a aac -shortest out/sharefyx-v4-musik.mp4`; die stumme Fassung bleibt die In-App-Datei. | zweite Datei auf Drive | 5–6 |
| **D** | Deploy D (Nikinger): Medien auf die VM, Unit-Umgebung, `deploy.sh main`, `health_gate.sh`, Live-Check Overlay. Abnahme P10.5-92. | `health_gate` 9/9, Overlay live einmal gesehen | — |

Reserve: zwei Tage. **Arbeitsregeln** wie Block 15 §2 (Wegwerf-Instanz, PID-Stopp, bereinigte
Umgebung, Session-Block ≤ 4 KiB, Rotation per Skript). Erlaubte Pfade: `phase10_5_finishing/{film,probes,tests}/**`,
`phase5_ui/webui/{config,api,security,media_routes}.py`, `phase5_ui/webui/static/{app.html,app.css,js/app.js,js/film.js,js/updates.js}`,
`phase5_ui/tests/**`, `phase4_auth/authserver/store.py` (nur die Spalte), `phase4_auth/tests/**`,
`phase4_auth/systemd/sharefyx-mcp.service` + `phase3_edge/scripts/install_units.sh` (Platzhalter),
`phase2_mcp/mcpserver/app.py` (Mount), `phase2_mcp/tests/test_app.py`, Doku.

## §5 Abnahme — P10.5-89–92

| # | Kriterium | Beleg |
|---|---|---|
| P10.5-89 | **Storyboard abgenommen (E1):** Textkarten und Szenenfolge vom Nikinger bestätigt, Deutsch, keine echten Daten | Session-Block 16.0 |
| P10.5-90 | **Render-Kriterien:** Dauer 30–50 s, 1920 × 1080, 30 fps, `yuv420p`/`+faststart`; zwei Renders mit identischen Stichproben-Frames; Saat-Regel grün; **Film abgenommen (E2)** | `probes/p105_b16_film.json`, Wächter, Session-Block 16.5 |
| P10.5-91 | **In-App:** erster Login zeigt das Overlay, Schließen setzt `seen`, kein zweites Mal; Wiederaufruf aus dem Update-Log; ohne Manifest kein Overlay und kein Fehler; Medien-Route verlangt Sitzung, liefert 206 bei `Range`; CSP nur `'self'` | Tests 16.4, Playwright-Probe |
| P10.5-92 | **Live nach Deploy D (Nikinger):** Overlay einmal gesehen, Wiederaufruf funktioniert, Journal ohne Fehler aus der Medien-Route | Live-Zeile, Nikinger |

## §6 `[VERIFY]`

Gemeinsame Nummerierung mit Block 15 (§6 dort): **V222** ✅ `FileResponse`/Range · **V225** Playwright-Version
und `record_video_size` · **V226** `ffmpeg`/`libx264` auf der VM · **V227** Node ≥ 18 (nur Rückfall) ·
**V228** Autoplay stumm + `playsinline` in Chromium und Safari · **V229** Determinismus des Takts ·
**V231** Remotion-5-Lizenz (nur Rückfall) · **V232** `SPACE_UI_MEDIA_DIR` über `load_ui_settings()` und
die Unit-Härtung gegen `/var/lib`.

## §7 Risiken und der Rückfall

- **Determinismus des Video-Seeks:** `<video>`-Frames können je nach Decoder um ein Bild abweichen. Erst
  Takt-Fixes (längere `seeked`-Wartezeit, Keyframe-Intervall 1 beim Neukodieren der Clips mit `ffmpeg -g 1`);
  **Rückfall-Auslöser (a):** nach Ende von Tag 3 sind die Stichproben-Frames zweier Renders nicht
  identisch, oder **(b):** der Render dauert über 15 Minuten. Dann Remotion in
  `~/.claude-code-tools/launch-film/` (`npx create-video`, `--browser-executable` auf das vorhandene
  Playwright-Chromium), dieselben Clips und Texte, Lizenz prüfen (V231), Entscheidung im Session-Block.
- **Zeit:** reißt die Woche, entscheidet der Nikinger nach P10.5-AM (Deploy D zuerst, Film als `v4.0.1`).
- **Bildurteil:** die Planungssession kann die Ästhetik nicht beurteilen, nur die Zahlen; darum zwei
  Sichtungen (E1, E2) statt einer — die Lehre aus 14.6 („gehirn-ähnlich" bei einem Seestern).
- **Dateigröße:** 40 s H.264 bei `crf 18` ≈ 15–30 MB; die Route streamt per `Range`, das Overlay
  lädt nicht vor dem Login. Wird die Datei > 40 MB, `crf 20`.
