---
status: snapshot
purpose: Plan Phase 10 (Bestandsaufnahme) gegen main@0a7aaf4 — gelockte Entscheidungen P10-A–P10-H, Steps 0–4/Z, Messanordnung M1–M7, Abnahme P10-1–P10-12, [VERIFY] V195–V206, unverbindliche Vorschau auf den Blockschnitt von P10.5. Das Register selbst steht nicht hier, sondern lebend in phase10_inventory/BAUSTELLENREGISTER.md.
read-when: vor jeder P10-Arbeit; vor dem Entwurf des P10.5-Plans (Step 4)
detail: L2
up: ../../ROADMAP.md
down:
  - ../../phase10_inventory/BAUSTELLENREGISTER.md   # das Register + Entscheidungsliste D-1–D-18 (📗, lebt)
  - ../../phase10_inventory/CLAUDE.md               # Phase-Head, Modulstatus, Session-Block
  - ./phase10_intake.md                             # Sammelstelle, Herkunft
  - ./PHASE9_CLOSEOUT_HANDOVER.md                   # Herkunft §4, [VERIFY]-Erbe
  - ./phase10_karte_c_stil_1.svg                    # Karte: Stile C1–C3 der gewählten Gehirnkarte (D-1b); erste Runde phase10_karte_entwurf_{a,b,c}.svg
updated: 2026-10-16 (angelegt — Planungssession Claude Code/Opus nach den vier Grundsatzantworten des Nikingers)
---
# Phase 10 — Bestandsaufnahme (Plan)

> **Auftrag in einem Satz:** P10 sammelt jede offene Baustelle, misst, was gemessen werden muss, holt die Entscheidungen des Nikingers
> ein und schreibt daraus den ausführungsreifen Plan für **P10.5** — **ohne eine Zeile Produktcode**. Das Bild des Nikingers (2026-10-08):
> P9 war das Fundament, P10 baut das Haus fertig und dämmt es; P11 darf erst danach über eine Garage nachdenken.

**Gegen:** `main@0a7aaf4` (2026-10-16), live `v3.1.4` (`d04c0ec`, Gate 9/9), `pytest` 1265, Matrix P9 121 ✅ · 12 ⚠️ · 1 ⬜,
`[VERIFY]` P9 40 ✅ · 1 ⚠️ · 3 ⬜. **Ausführung von P10:** Claude Code (Opus) mit dem Nikinger; P10 braucht keinen opencode-Ausführer.

## §0 Gelockte Entscheidungen

| Lock | Entscheidung | Herkunft |
|---|---|---|
| **P10-A** | **Zweiteilung bestätigt.** P10 = Bestandsaufnahme (Register, Messungen, Entscheidungen, Plan P10.5), **kein Produktcode**. P10.5 = Ausführung. **Tor:** P10.5 beginnt erst, wenn der Nikinger das Register freigegeben hat (P10-8). | Nikinger 2026-10-16 (Rückfrage), intake §1 |
| **P10-B** | **Das Register lebt, der Plan nicht.** `phase10_inventory/BAUSTELLENREGISTER.md` ist 📗 und trägt Register **und** Entscheidungsliste (§12 dort); dieser Plan ist ein 📕-Snapshot und verweist nur. Jede Baustelle steht genau einmal im Register, mit stabiler ID (Themenkürzel + Nummer, z. B. `PA-1`). | Konvention 📕 „never edit" |
| **P10-C** | **Anbieter-Unabhängigkeit ist Phasenziel**, auf Server-/Connector-Ebene: jeder standardkonforme MCP-Client kann sich verbinden. Es blockiert keinen Step, nur den **Abschluss von P10.5**; Abnahme: ein Nicht-Claude-Client führt `list_spaces` live über die echte Adresse aus. Modell-Routing bleibt Client-Seite (frühestens P11), nie im Server (Kernprinzip). **Bestätigt ist der Umfang, nicht der Eingriff:** der konkrete Eingriff in `phase4_auth/` (Sicherheitscode außerhalb der Phase) wird dem Nikinger mit dem P10.5-Plan vorgelegt; erst dessen Freigabe gilt als OK. In P10 wird nichts gebaut. | Nikinger 2026-10-16 |
| **P10-D** | **Karten-Umbau:** Stil (p8x §2.2), Layout über den Reload merken, Interaktion (Suche, Filter, Titel), „etwas gehirnartiger". **Form: C, die Gehirnkarte** (D-1, entschieden 2026-10-16 aus drei Entwürfen); den Stil innerhalb C wählt der Nikinger aus C1 Flächen, C2 Nervenbahnen, C3 Höhenlinien (D-1b). Einklappen (§2.5) ist **nicht** gewählt. Datenquelle bleibt `GET /api/v1/graph` mit seinen neun Feldern; ein zehntes wäre eine eigene Entscheidung. | Nikinger 2026-10-16 |
| **P10-E** | **Ausführer P10.5 = M3 Thinking über opencode**; M3.1 Preview (max) nur gezielt für CSS-/Darstellungsblöcke; ein Modell-Trailer je Commit. Der P10.5-Plan wird für einen Ausführer geschrieben, der nicht geplant hat: exakte Namen, Anker, Testlisten, Rückgabe-Auslöser (P8.5-O). | Nikinger 2026-10-16, Handover §4.9 |
| **P10-F** | **Messen vor Bauen.** Messanordnung und Zielwerte entstehen in P10 (Step 2/3), nicht nach dem Bau. Kein HAR-Export ins Repo — er trägt Cookie und CSRF-Token (Hard Rule 1); Messwerte stehen als Tabelle. | intake §2.1 |
| **P10-G** | **Nummerierung.** Locks `P10-A…`, Abnahme `P10-1…`, `[VERIFY]` ab **V195**; V167–V172 bleiben reserviert und unbelegt. Steps tragen Ziffern (0–4, Z), damit kein Lock-Buchstabe mit einem Step kollidiert. P10.5 setzt fort: `P10.5-A…`, `P10.5-1…`, nächstes freies V. | Memory „second-pass plan", P8.6-W |
| **P10-H** | **Tabu in P10:** Produktcode aller Phasen (`phase1_storage/` bis `phase9_hardening/`, ohne deren `.md`) und die Units bleiben unverändert. Erlaubt: Doku, Proben und Messskripte unter `phase10_inventory/` samt Tests dafür, Werkzeuge außerhalb des Repos (`~/.claude-code-tools/`). Prüfkommando: P10-11. | intake §1 |

### §0.1 Was P10 ausdrücklich nicht tut

Keinen Fix bauen, auch keinen offensichtlichen (BT-1 ist dringend, wird aber in P10.5 Block 1 gebaut, nicht hier) · keinen Dienst
anfassen (Hard Rule 9) · keine Messung gegen das echte `DATA_ROOT` oder die echte `auth.sqlite3` (Wegwerf-Instanz, Port 8799) · keine
neue Fähigkeit vordenken (P11) · nicht in Sharefyx-Items schreiben.

## §1 Ausgangslage und Step-0-Befund (gemessen 2026-10-16)

- **Doku:** `scripts/doc_health.py` → 0 Befunde in allen vier Prüfungen. Oversize-Check: jeder Treffer ist 📕/📦 **außer** drei Phase-Heads,
  die „benannt statt versteckt" geführt werden (`phase8_6_ui_polish/CLAUDE.md`, `phase8_ui_graph/CLAUDE.md`, `phase6_shares/CLAUDE.md`)
  → Register DO-1. `docs/INDEX.md` 38.404 B gegen die harte Grenze 40.960 B → DO-2.
- **Drift gefunden:** (1) Fleet-Notiz §7 nennt `step_a/Caddyfile`, die Datei heißt `Caddyfile.template` (DO-5). (2) **Ledger-Lücke:** P6-Zeilen
  7/9/14–17/23/25/29/30, P6.5-14, O4/O5/O7, die Glyph-Entscheidungen und der Funnel-Watchdog standen bis P8.6 im geerbten Ledger und fehlen
  ab dem P9-Plan, ohne Schließvermerk → Register AL-1, AL-4, LG-7–LG-10, BT-10. (3) Der Editor-Wunsch (intake §2.3) widerspricht dem gelockten
  **P5-U** („kein WYSIWYG") → ED-1, D-4. (4) Der „verlorene" Planungsprompt ist `docs/PROMPTS.md` Prompt 2 (Korrektur `0a7aaf4`).
- **Am Code gemessen:** `mcp` im Dev-venv 1.28.1, `SUPPORTED_PROTOCOL_VERSIONS` endet bei `2025-11-25`. **MCP 2026-07-28** ist laut
  Versionierungsseite die **aktuelle** Version (Status „Current"; der P8-Plan §0.5 führte sie am 2026-08-28 noch als RC), führt DCR als
  *deprecated* und handelt die Version **je Anfrage** aus (`_meta`, `server/discover`), mit Rückwärtskompatibilität zu handshake-basierten
  Versionen bis `2025-11-25` (Register PA-1–PA-5). Der Graph-Knoten trägt `id, title, space, own, writable, type, status, folder, tags` —
  Suche und Filter der Karte brauchen kein neues Feld (KA-3).
- **Recherche-Quellen, primär gelesen am 2026-10-16:** MCP 2026-07-28 *Client Registration*
  (`modelcontextprotocol.io/specification/2026-07-28/basic/authorization/client-registration`) und *Versioning*
  (`modelcontextprotocol.io/specification/versioning`), opencode-Doku *MCP servers* (`opencode.ai/docs/mcp-servers/`), OpenAI Apps-SDK
  *Authentication* (`developers.openai.com/apps-sdk/build/auth`). Alles, was nur aus Sekundärquellen stammt (etwa der opencode-Callback
  aus PR #5940), steht als `[VERIFY]` in §6.

## §2 Quellen des Registers (Grundlage für P10-2)

| Quelle | Umfang | im Register als |
|---|---|---|
| intake §2.1–§2.3 (Wünsche 2026-10-08) | Performance, 404/Logo/Tab-Titel, Editor | PF-*, UI-1–UI-3, ED-* |
| intake §3 (Erbe P9) | 12 Zeilen | RE-*, LG-*, UI-4, UI-6, KA-1, KA-4, KA-5, LG-11 |
| intake §5–§7 (eurofyx-fleet) | ACL, Exit 143, Caddy, zwei Eingänge, Host-Header, Funnel-Regel, Backup | BT-1–BT-3, BT-7–BT-9, BT-12 |
| Handover §4.1–§4.10 | 10 Posten | BT-3, BT-4, PF-1, BG-1, BT-6, BT-11, BT-5, UI-5, P10-E, RE-7 |
| Matrix P9: 12 ⚠️ + 1 ⬜ | P9-13, 15, 22, 27, 31, 55, 56, 72, 74, 97, 99, 124, 127 | AL-5, AL-6, BG-2, BG-3 |
| `[VERIFY]` offen/teilweise | V150, V193, V194, V120, V157, V162 B | AL-6, RE-4, RE-3, UI-3, AL-7 |
| P9-Head §Backlog | Vision-Modell, `/overview`, `mcp-proxy`-Ausfall (geschlossen) | BT-11, PF-1 |
| geerbtes Ledger bis P8.6 (wiedergefunden) | P6-Zeilen, P6.5-14, O4/O5/O7, Glyphen, Funnel-Watchdog | AL-1–AL-4, LG-7–LG-10, BT-10 |
| Nikinger 2026-10-16 | Anbieter-Unabhängigkeit, Karten-Umbau | PA-*, KA-1–KA-3 |
| Step 0 (2026-10-16) | Oversize, INDEX-Rand, Drift, opencode-Marker | DO-1, DO-2, DO-5, BT-13 |

`TODO`/`FIXME`/`XXX`/`HACK` im Code außerhalb der Tests: **0 Treffer** (gemessen 2026-10-16) — keine weitere Quelle.

## §3 Steps

| Step | Inhalt | Wer | Fertig, wenn |
|---|---|---|---|
| **0** | Verifikations-Durchlauf (Doku ↔ Code, Links, INDEX-Zeilen, Oversize) | Claude Code | ✅ 2026-10-16, Befund in §1 |
| **1** | Register-Entwurf aus allen Quellen in §2, je Zeile ein Anker am Code | Claude Code | ✅ Entwurf 2026-10-16 (76 Zeilen); bleibt offen, bis die `[VERIFY]` aus Step 2 eingetragen sind |
| **2** | Messungen und Proben M1–M7 (§4) | M1 Nikinger, Rest Claude Code | jede Messung hat ihr Ergebnis im Register oder unter `phase10_inventory/messung/` |
| **3** | Entscheidungen D-1–D-18 einholen (Register §12) | Nikinger | jede D-Zeile trägt eine datierte Antwort oder „vertagt bis …" |
| **4** | Plan P10.5 schreiben (`docs/concepts/phase10_5_<name>_plan.md`) | Claude Code (Opus) | Locks, Blöcke, Abnahme je Block mit Probe **und** Gegenlauf, `[VERIFY]`, Rückgabe-Auslöser für M3 |
| **Z** | Closeout P10: Register-Freigabe (Tor), Bilanz, ROADMAP | Nikinger + Claude Code | P10-1–P10-12 erfüllt, §8 dieses Plans gefüllt |

**Reihenfolge:** Step 3 darf parallel zu Step 2 laufen; nur D-3 (Zielwerte) wartet auf M1/M2 und D-4 (Editor) auf M7. Step 4 beginnt erst,
wenn D-1b, D-3, D-4 und D-8 entschieden sind — sie bestimmen den Blockschnitt (D-1 ist seit 2026-10-16 entschieden: C).

## §4 Messungen und Proben (Step 2)

Alle Wegwerf-Läufe: eigener Port (**8799**), `tmp`-`DATA_ROOT`, `tmp`-`auth.sqlite3`, Umgebung **ohne** `SHAREFYX_*`/`SFX_*`
(Memory „test harness never inherits env"), Stopp nur über PID-Datei oder den eindeutigen Port (Hard Rule 9). Werkzeuge außerhalb des
Repos in `~/.claude-code-tools/` (Playwright: `e2e-venv`).

| M | Frage | Instrument | Ergebnis nach | Register |
|---|---|---|---|---|
| **M1** | Wie lange wartet ein Mensch wirklich — über **beide** Eingänge? | Browser des Nikingers (DevTools → Network), je Eingang drei Läufe von vier Szenarien: S1 Kaltstart mit „Disable cache" bis die Übersicht steht (`DOMContentLoaded`, `Load`, `/api/v1/overview` Waiting + Total) · S2 warm, Home-Knopf · S3 drei Space-Wechsel (`/api/v1/items?…`) · S4 ein Item öffnen. Dazu Netz (Heim/Mobil/Arbeit) und Uhrzeit — die Relay-Latenz schwankt (intake §7). **Kein HAR.** | `phase10_inventory/messung/M1_browser.md` (Tabellenvorlage legt Claude Code an) | PF-2 |
| **M2** | Was kostet `/overview` serverseitig bei Live-ähnlicher Last? | neues Instrument `phase10_inventory/probes/p10_overview_bench.py`: Wegwerf-`DATA_ROOT` mit **4 Spaces × 50 Items**, ein Principal sieht alle vier (das unterscheidet es von `ui_budget.py`, das mit einem Space 3,3× zu niedrig misst), in-process gegen `create_app()`; 1 Aufwärmlauf + 5 gemessene, JSON auf stdout (Hard Rule 7) | JSON + Zeile im Register; dasselbe Instrument wird die P10.5-Abnahme von PF-1 | PF-1, PF-2 |
| **M3** | Was schickt ein Nicht-Claude-Client, und woran scheitert er heute? | opencode isoliert installieren, gegen die Wegwerf-Instanz `opencode mcp auth` / `opencode mcp debug`; ein kleiner protokollierender Proxy davor hält den DCR-Request fest (`application_type`, `redirect_uris`, `token_endpoint_auth_method`). **Erwartet: rot** (`invalid_client_metadata` oder `invalid_redirect_uri`). Optional M3b: einen Client mit Loopback-Redirect direkt in die Wegwerf-`auth.sqlite3` schreiben und mit `oauth.clientId` bis `initialize` kommen — liefert die ausgehandelte Protokollversion | Register PA-1/PA-7, V195, V198 | PA-1, PA-5, PA-7 |
| **M4** | Reproduziert BG-1 in `v3.1.4`? | Playwright: `/api/v1/overview` per Route verzögern, „Spaces verwalten" sofort öffnen, Liste zählen | Register BG-1, V202 | BG-1 |
| **M5** | Halten P9-124 und P9-127 im Browser? | Playwright mit zwei Principalen (Muster aus `docs/concepts/sichtpruefung_automation_conventions.md`): Konfliktkopie landet im Space des Konflikt-Items; Enter in den sieben unbelegten Overlays. Jede Station mit Gegenlauf | `phase10_inventory/probes/` + Matrix-Nachtrag im Register | BG-2, BG-3 |
| **M6** | Wo liegt die Karte heute (Regressionsgrenze für KA-1), und was kostet die Gehirnkarte? | vorhandener `p8_22_smoke.py` gegen 200 Knoten: Settle-Ticks, Settle-Zeit, Zeichenzeit je Frame. Dazu ein Prototyp der Lappen-Berechnung (Raster × nächster Knoten, Erosion, Kontur) bei 200 Knoten: einmal nach dem Einschwingen gegen je Frame — davon hängt die Größe „M" von KA-1 ab | Register KA-1 | KA-1 |
| **M7** | Welche Editor-Bibliothek trägt Stufe 1 ohne Build-Schritt? | zwei bis drei Kandidaten in einer Scratchpad-Seite: Größe (minifiziert), Laden als einzelne vendorte Datei ohne Bundler (P5-T), Markdown-Roundtrip verlustfrei über 10 synthetische Fixtures (Listen, Tabellen, Code, Links, `itm_…`-Referenzen, Frontmatter unberührt), Tastatur | `phase10_inventory/messung/M7_editor.md` | ED-1, V201 |

## §5 Abnahme P10

**Statusregel wie P9:** ✅ = erfüllt mit Beleg am Ort · ⚠️ = erfüllt in anderer Form, Abweichung benannt · ⬜ = offen.

| # | Kriterium | Beleg |
|---|---|---|
| **P10-1** | Step-0-Bericht steht: `doc_health` 0, Oversize nur 📕/📦 oder benannt, Drift ins Register übernommen | §1 dieses Plans |
| **P10-2** | Jede Quelle aus §2 ist im Register abgedeckt; Gegenprobe per `grep` über die Quell-IDs (13 Matrixzeilen, 6 `[VERIFY]`, Handover 4.1–4.10, intake §2/§3/§5–§7, Ledger-Lücke) | Register + Closeout §8 |
| **P10-3** | Jede Registerzeile trägt Größe, Risiko, Entscheidungsbezug und Ziel | Register |
| **P10-4** | M1 gemessen (beide Eingänge, je 3 Läufe, 4 Szenarien) und Zielwerte entschieden (D-3) | `messung/M1_browser.md`, Register §12 |
| **P10-5** | M2 als Instrument im Repo; drei Aufrufe nacheinander liegen im Median innerhalb ±10 % | `probes/p10_overview_bench.py` + JSON |
| **P10-6** | M3: der echte Registrierungs-Request eines Nicht-Claude-Clients ist festgehalten, die Ablehnung reproduziert | Register PA-1, V195 |
| **P10-7** | M4–M7 gefahren; ein Ergebnis darf auch „reproduziert nicht" oder „Kandidat fällt" heißen | Register BG-*, KA-1, ED-1 |
| **P10-8** | **Tor:** der Nikinger hat das Register freigegeben (Datum im Register-Kopf) | Register |
| **P10-9** | D-1–D-18 tragen eine datierte Antwort oder „vertagt bis …" | Register §12 |
| **P10-10** | Plan P10.5 geschrieben: Locks, Blöcke, Abnahme je Block mit Probe und Gegenlauf, Rückgabe-Auslöser für M3, INDEX-Zeile | neuer Plan |
| **P10-11** | Kein Produktcode-Diff: `git diff --stat 0a7aaf4..HEAD -- phase1_storage phase2_mcp phase3_edge phase4_auth phase5_ui phase6_shares phase6_5_tools_images phase7_spaces_admin phase8_ui_graph phase8_5_picker_release phase8_6_ui_polish phase9_hardening scripts ':!*.md'` → leer | Closeout §8 |
| **P10-12** | Doku-Hygiene: neue `.md` mit Card und INDEX-Zeile, Softcap gehalten, ein Session-Block je Head, Hard Rule 8 je Commit | `doc_health`, Tests |

## §6 `[VERIFY]` V195–V206

| V | Frage | wird geklärt in |
|---|---|---|
| **V195** | Welchen DCR-Request schickt opencode wirklich (`application_type`, `redirect_uris`, Auth-Methode), und ist der Callback konfigurierbar? Bisher nur PR #5940 (Standard `http://127.0.0.1:19876/mcp/oauth/callback`) und eine Doku ohne Callback-Angabe | M3 |
| **V196** | Laut OpenAI-Doku (primär) unterstützt ChatGPT `none` mit PKCE und `private_key_jwt` und bevorzugt CIMD; Callback `https://chatgpt.com/connector_platform_oauth_redirect` oder `…/connector/oauth/{callback_id}`. Offen: was ChatGPT per DCR anfragt, wenn der AS nur `none` anbietet | nur wenn D-8 ChatGPT einschließt |
| **V197** | Blockiert Chromium den Loopback-Redirect nach dem Login, solange `form-action` ihn nicht nennt (Klasse des P4-Live-Funds 8c)? | P10.5, Gegenlauf im Browser |
| **V198** | Welche Protokollversion handelt live `mcp 1.30.0` aus, und greift beim Abnahme-Client die Rückwärtskompatibilität zu handshake-basierten Servern (`2025-11-25`), die die Spec 2026-07-28 beschreibt? | M3b |
| **V199** | Trägt die Live-Config auf der VPS genau die Fleet-Werte (`dial_timeout 10s`, `lb_try_duration 15s`, `lb_try_interval 1s`)? Der Nikinger liest `curl localhost:2019/config/` auf der VPS, bevor die Vorlage nachzieht | Step 2 (Nikinger) |
| **V200** | Endet `socat` bei SIGTERM reproduzierbar mit 143, und wirkt `SuccessExitStatus=143` ohne Relay-Neustart? (Fleet hat es gemessen, hier nicht nachgemessen) | P10.5, Wegwerf-Unit oder Nikinger |
| **V201** | Läuft eine Editor-Bibliothek ohne Build-Schritt, passt sie ins `ui_budget` (≤ 250 KB gesamt), und ist der Markdown-Roundtrip verlustfrei? | M7 |
| **V202** | Reproduziert BG-1 (leere Space-Liste) in `v3.1.4`? | M4 |
| **V203** | Prüft irgendein Wächter den **Funnel**-Pfad von außen? | Step 2 (Fleet-Repo lesen oder fragen) |
| **V204** | Sind die Glyph-Entscheidungen P6/P6.5 durch P8 (nur Lucide-Sprite) gegenstandslos? | Step 2, `git log -S` über die betroffenen Glyphen |
| **V205** | Welche der P6-Zeilen 7, 9, 14–17, 23, 25, 29, 30 lassen sich mit Belegen aus P7–P9 schließen? | Step 2, Abgleich mit P7/P9-Matrix |
| **V206** | Sind O7 („leere Ordner überleben einen Move") und P6-Zeile 30 („leergewordener Ordner verschwindet aus dem Baum") dieselbe Frage? | Step 2, Code `store.move()` |

**Geerbt, offen:** V150 (zweites Konto, Termin) · V193 (Ordner umbenennen atomar) · V194 (Verweise auf einen Space-Namen) · V120
(Tab-Titel). **Teilweise:** V157 (WebKit) · V162 B (ACL).

## §7 Vorschau auf P10.5 (unverbindlich — der Schnitt entsteht in Step 4)

Reihenfolge nach Risiko, das Dringende zuerst, das Größte zuletzt:

| Block | Inhalt (Register) | Größe | Notiz |
|---|---|---|---|
| 1 Betrieb | BT-1, BT-2, BT-6, BT-11, LG-5 | S | BT-1 ist der einzige dringende Posten |
| 2 Fehler + Parität | BG-1, RE-1, RE-2 | S | nach den Proben aus M4/M5 |
| 3 Performance | PF-1, PF-4, ggf. PF-3 | M | Abnahme mit dem M2-Instrument und gegen die Zielwerte aus D-3 |
| 4 Anbieter | PA-1, PA-2, ggf. PA-3, PA-6 | M | `phase4_auth/` — Sicherheitscode; Live-Abnahme PA-7 durch den Nikinger am Phasenende |
| 5 Darstellung | UI-1, UI-2, UI-3, UI-5, UI-6, KA-5 | M | M3.1 gezielt (P10-E) |
| 6 Karte | KA-1, KA-2, KA-3 | M–L | gegen die M6-Baseline |
| 7 Editor | ED-1, ED-2, ED-5 | L | eigener Mini-Plan, wenn D-4 „ja" sagt |
| 8 Doku + Altlasten | DO-1, DO-2, DO-3, LG-6, AL-* | S | zuletzt, damit die Doku den Endstand zeigt |

**Phasenabschluss P10.5** verlangt zusätzlich das Phasenziel aus P10-C (PA-7 live) — es blockiert keinen der Blöcke.

## §8 Closeout P10 (wird in Step Z gefüllt)

*leer bis Step Z*
