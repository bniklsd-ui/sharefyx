---
status: live
purpose: Plan Block 17 „Film in die App" — der Launch-Film v4.0.0 läuft beim ersten Start im Vollbild und ist im Update-Log wieder aufrufbar. Auftrag, Befunde am Code, Entwurf, Schritte 17.1–17.5, Probe, Gegenläufe.
read-when: Arbeiten an der Einbindung des Films (vor Deploy D) — zuerst §1 (Auftrag) und §4 (Schritte)
detail: L2
up: ../../phase10_5_finishing/CLAUDE.md
down:
  - ./phase10_5_launch_film_plan.md   # 📗 Block 16 — wie der Film entstand
updated: 2026-11-01 (Plan, Claude Code — Auftrag des Nikingers, E1: r2 unverändert in git; nach Advisor: F9 Caddy, F10 Dateilisten, F1 am Quelltext geprüft, stummer Erststart ehrlich benannt; E2: Startbild, der Klick spielt ab) | 2026-11-01 (17.1–17.5 ✅ — Probe 10/10, vier Gegenläufe rot; §6 Ergebnis)
---
# Film in die App (Plan Block 17)

> **Auftrag (Nikinger, 2026-11-01, Startauftrag dieser Session):** „Film in the app. It plays full
> screen on the first start after the update and can be replayed from the update log. It needs a
> short plan first: Load the 25.7 MB video only when it plays, so the first page load stays light.
> Remember ‚already seen' per browser, with nothing stored on the server. Allow video in the browser
> security settings. Test it in a browser against a throwaway instance. Then Deploy D."

## 1. Entscheidungen

| # | Frage | Antwort (Nikinger 2026-11-01) |
|---|---|---|
| E1 | Welche Datei kommt in die Release? `deploy.sh` baut jede Release per `git clone` — die Datei muss also **in git** | **r2 unverändert committen** (25.663.438 B, SHA-256 `cab1f13a…`). Repo +25,7 MB dauerhaft; je Release ≈ +51 MB (Arbeitsbaum + `.git`), `KEEP=5`, 8,2 GB frei |
| E2 | Erststart: stummes Autoplay oder Startbild? (Browser sperren Ton ohne Klick; der Anmelde-Klick überlebt die Weiterleitung nicht) | **Startbild, der Klick spielt ab** — mit Ton und echtem Vollbild; das Video lädt erst nach dem Klick |

Alles andere ist unten **entschieden** und begründet (Konvention „plan-first, minimal questions").

## 2. Befunde am Code (2026-11-01, `main@7bb27de`)

| # | Ort | Befund | Folge |
|---|---|---|---|
| F1 | `phase5_ui/webui/static_routes.py :: _static` | liefert per `found.read_bytes()` — **kein `Range`**, ganze Datei in den Speicher | Video über Starlette `FileResponse` — **am installierten Quelltext geprüft** (`starlette 1.9.0`, `responses.py:301–520`): `Range` → 206 mit `content-range`, 64-KiB-Blöcke, eigene Header nur per `setdefault` (unsere CSP/`Cache-Control` bleiben stehen). **Nur** für `.mp4`; die übrigen Dateien bleiben unverändert |
| F2 | dieselbe Datei, `_CONTENT_TYPES` | kein `.mp4` → `application/octet-stream`; mit `nosniff` spielt der Browser das nicht | `".mp4": "video/mp4"` (dieselbe Falle wie `logo.svg`, Block 7.2) |
| F3 | `_HASHED_NAME_RE` | ≥ 8 Hex vor der Endung ⇒ `immutable` | Dateiname `sharefyx-4.0.0.cab1f13a.mp4` — ein Jahr im Browser-Cache, beim Wiedersehen kein zweiter Download |
| F4 | `phase5_ui/webui/security.py :: ui_security_headers` | `default-src 'none'`, **kein `media-src`** ⇒ das Video wird blockiert | `media-src 'self'` — nur eigener Ursprung, kein `blob:`, kein `data:` |
| F5 | `phase5_ui/scripts/ui_budget.py :: static_payload_files` + Wächter `test_budget_coverage.py` | jede Datei unter `static/` muss in genau einer Liste stehen | das Video ist **weder** Erstaufruf **noch** Editor: eigene, benannte Ausnahme „auf Abruf" (`media/`), wie `app.html`/`OFL.txt`; der Wächter nennt sie |
| F6 | MP4 selbst | `ftyp` → `moov` (Byte 32) → `mdat` — **faststart** liegt schon vor | Wiedergabe beginnt nach den ersten Bytes, kein Umpacken nötig |
| F7 | Playwrights Chromium | Open-Source-Build **ohne H.264** | Probe mit `/usr/bin/google-chrome` (`executable_path`) — sonst prüft die Probe einen Browser, den kein Mensch benutzt |
| F9 | `phase9_hardening/step_a/Caddyfile.template` | kein `header`-, kein `encode`-Block — Caddy reicht die CSP der App unverändert durch | die Wegwerf-Instanz (ohne Caddy) misst dieselbe CSP wie live; **live** bestätigt erst der Nikinger nach Deploy D (Film spielt über die echte Adresse) |
| F10 | Dateilisten über `static/` | nur `test_budget_coverage.py:77` läuft rekursiv über `static/`; `.gitignore` fängt `.mp4` nicht | keine weitere Liste bricht an 25 MB Binärdaten |
| F8 | `localStorage`-Schema der UI | Präfix `sfx:` (`sfx:linkpicker:mode`), `try`/`catch` wegen privater Fenster (`dialogs.js:252`) | Schlüssel `sfx:film:gesehen`, gleiches Muster |

## 3. Entwurf

**Dateien.**

| Datei | Änderung |
|---|---|
| `phase5_ui/webui/static/media/sharefyx-4.0.0.cab1f13a.mp4` | neu (r2, byteweise) |
| `phase5_ui/webui/static/js/launchfilm.js` | neu, ES-Modul (≈ 3 KB) — `init()` aus `app.js` |
| `phase5_ui/webui/static/app.html` | Überlagerung `#launch-film` (ein `<video>` **ohne** `src`, `preload="none"`) + Knopf `#update-log-film` im Update-Log-Panel |
| `phase5_ui/webui/static/app.css` | `.launch-film`: `position: fixed; inset: 0`, schwarz, `object-fit: contain`, oberste Ebene |
| `phase5_ui/webui/security.py` | `media-src 'self'` |
| `phase5_ui/webui/static_routes.py` | `.mp4` → `video/mp4` über `FileResponse` (+ dieselben Sicherheits-Header) |
| `phase5_ui/scripts/ui_budget.py` | `media/` als benannte Ausnahme (Docstring; die Auswahl selbst bleibt) |

**Ablauf (`launchfilm.js`)** — nach E2 (Startbild statt Autoplay).

1. **Erststart:** `localStorage["sfx:film:gesehen"] !== "4.0.0"` ⇒ Schlüssel **sofort** setzen, dann
   die Überlagerung als **Startbild**: Titel, „▶ Film ansehen", „Überspringen". Sofort gesetzt,
   nicht am Ende: wer neu lädt, bekommt das Startbild nicht in Schleife.
2. **Laden nur beim Abspielen:** das `src` setzt erst der Klick auf „Film ansehen". Startbild,
   „Überspringen" und jeder spätere Aufruf ohne Klick fragen das Video **nie** an (Probe prüft das
   am Netzwerk-Log, nicht am Code).
3. **Der Klick ist die Nutzergeste:** in ihm laufen `requestFullscreen()` (echtes Vollbild; scheitert
   es, bleibt die Überlagerung — sie deckt das Fenster ohnehin) und `play()` **mit Ton**. Ohne Klick
   erlaubt kein Browser beides.
4. **Schließen:** „Überspringen"/„Schließen", `Escape`, Filmende. Danach Vollbild verlassen,
   `pause()`, `src` entfernen, `load()` — der Puffer wird freigegeben, nichts lädt nach.
5. **Wiedersehen:** Knopf „▶ Film zu v4.0.0" im Update-Log ⇒ derselbe Klick-Weg (Vollbild + Ton),
   unabhängig vom Schlüssel.
6. **Kein Speicher** (privates Fenster, `localStorage` wirft) ⇒ **kein** Startbild. Sonst stünde es
   bei jedem Laden da.

**Bewusst nicht:** kein Server-Zustand (Auftrag; `users.seen_update_id` bleibt allein beim Banner) ·
kein zweites Format (WebM) — eine Datei, ein Codec · kein `navigator.connection`-Sonderweg. Wer
**neu** dazukommt, sieht den Film auch beim ersten Start — „erster Start in diesem Browser".

## 4. Schritte

| # | Inhalt | Fertig, wenn |
|---|---|---|
| 17.1 | Server: `media-src`, `video/mp4`, `FileResponse`, Datei unter `static/media/`, Budget-Ausnahme | Unit-Tests grün: CSP trägt `media-src 'self'`; `GET` → 200 `video/mp4` `immutable`; `Range: bytes=0-99` → **206**, 100 B; Traversal bleibt 404; Budget-Wächter nennt `media/`; **Wächter: der Hash im Dateinamen = Präfix der echten SHA-256** (die Datei ist ein Jahr `immutable` — ein neuer Schnitt unter altem Namen bliebe sonst still im Cache) |
| 17.2 | UI: Überlagerung, `launchfilm.js`, Knopf im Update-Log | Wächter-Tests am Markup/Modul (Muster `test_pages_markup.py`) |
| 17.3 | Browser-Probe an der Wegwerf-Instanz (`film/wegwerf.py neu`, Port 8811, Chrome) — §5 | alle Zellen grün, JSON unter `phase10_5_finishing/probes/` |
| 17.4 | Gegenläufe — §5 | jede Zelle wird rot, wenn ihr Grund fehlt |
| 17.5 | Update-Log-Zeile zum Film, volle Suite, `doc_health`, `ui_budget`, Commit + Push | dann **Deploy D** (Plan §2.5): oberste Überschrift → Deploy-Tag; `deploy.sh` + `health_gate.sh` beim Nikinger |

## 5. Probe (17.3) und Gegenläufe (17.4)

| Zelle | Messung | Gegenlauf (Fix neutralisiert, Probe erneut) |
|---|---|---|
| P1 Erststart | Startbild sichtbar, Schlüssel = `4.0.0`, **keine** `*.mp4`-Anfrage; Klick ⇒ `currentTime > 0` nach 2 s, `muted === false` — Chrome mit `--autoplay-policy=document-user-activation-required` (die strenge Regel: nur so beweist der Klick etwas) | Schlüssel vorab gesetzt ⇒ kein Startbild |
| P2 nur auf Abruf | Startbild vor dem Klick und zweiter Aufruf: **keine** Anfrage an `*.mp4` im Netzwerk-Log (den Knopf „Überspringen" klickt die Probe nicht — er ruft nur `close()`) | `src` im Markup statt im Klick ⇒ Anfrage erscheint |
| P3 CSP | kein `securitypolicyviolation`, Video spielt | `media-src` entfernt ⇒ Verletzung, `currentTime` bleibt 0 |
| P4 Range | Browser-Anfrage bekommt 206 | `read_bytes()`-Weg ⇒ 200 ohne `Content-Range` |
| P5 Wiedersehen | Knopf im Update-Log startet den Film erneut | — |
| P6 Schließen | `Escape` ⇒ Überlagerung weg, `src` leer | — |
| P7 privates Fenster | `localStorage` wirft (Init-Skript) ⇒ kein Autoplay | — |
| P8 Bild | Bildschirmfoto mitten im Film (für den Nikinger, per `Read`) | — |

**Hinweis für ältere Proben:** eine Playwright-Probe, die künftig gegen eine frische Instanz läuft,
sieht zuerst den Film. Gegenmittel: `add_init_script` setzt `sfx:film:gesehen`.

## 6. Ergebnis (2026-11-01, Claude Code)

| Schritt | Stand | Beleg |
|---|---|---|
| 17.1 | ✅ | `test_static_routes.py` (206, `video/mp4`, `immutable`, CSP bleibt), `test_security.py` (`media-src 'self'`), `test_budget_coverage.py` (`_ausgenommen()`: `media/`) |
| 17.2 | ✅ | `js/launchfilm.js`, `app.html`, `app.css`; Wächter `phase10_5_finishing/tests/test_launch_film.py` (4: Hash = SHA-256-Präfix, kein `src`, `media/` nur der Film, kein Server-Zustand) |
| 17.3 | ✅ | `probes/p105_b17_film_probe.py` → `p105_b17_film.json`: **10/10** (Chrome, strenge Autoplay-Regel; Klick ⇒ Ton + Vollbild; Browser bekommt 206) |
| 17.4 | ✅ | vier Gegenläufe, jeder rot: G1 `--vorab-gesehen` ⇒ P1 · G2 `src` im Markup **ohne** `preload` ⇒ P2 (+P7) · G3 ohne `media-src` ⇒ P1/P3/P4/P5 · G4 ohne `FileResponse` ⇒ P4. JSON `p105_b17_film_gegenlauf_*.json` |
| 17.5 | ✅ | Update-Log-Zeile, Überschrift `## 2026-10-26` → `## 2026-11-01` (Deploy D); `ui_budget` 6/6 (Erstaufruf 232,3 KB gzip), `doc_health` 0 |

**Funde beim Bauen.** (1) P6 rot: im Vollbild tat ESC nichts, weil der Handler „im Vollbild
nichts tun" kannte — headless reicht ESC durch und verlässt das Vollbild nicht. ESC schließt
jetzt **immer** (`close()` verlässt das Vollbild selbst). (2) Gegenlauf G2 war zuerst zahnlos:
`src` im Markup **mit** `preload="none"` lädt in Chrome nichts — die Zusage hängt am **Paar**,
der Gegenlauf neutralisiert jetzt beide. (3) Zwei Anmeldungen im selben 30-s-Fenster scheitern am
TOTP-Replay-Schutz — die Probe wartet dann das nächste Fenster ab.
