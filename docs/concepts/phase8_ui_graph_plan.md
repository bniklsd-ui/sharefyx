---
status: snapshot
purpose: ausführungsreifer P8-Plan — UI-Neuanstrich (v3), Verknüpfungs-Graph, drei P7-Erbposten; geschrieben für einen ausführenden Agenten (opencode/M3), der nicht mitgeplant hat
read-when: vor und während der Ausführung von Phase 8 — Abschnitt §0 zuerst, dann den jeweiligen Step
detail: L2 (📕-Snapshot, vom 40KB-Softcap ausgenommen)
up: ../../ROADMAP.md
down:
  - ./PHASE7_CLOSEOUT_HANDOVER.md            # Herkunft der Erbposten P7-24 / remove-space / P7-4
  - ../../phase8_ui_graph/CLAUDE.md          # Phase-Head (entsteht in Step 0.5)
updated: 2026-09-02 (P8-22+P8-24-Smokes gebaut, drei Phase-8-Funde als benannte Defekte in §9.4.6 -- graph.js ALPHA_DECAY / api.py _graph_get `writable` / graph.js Knotenklick-nach-Item -- mit je drei Optionen, §9.4.4 gegenstandslos (beide Substanz-Setups gebaut), Status 15-10-0; achte P1-Contract-Öffnung GESCHLOSSEN mit demselben Commit, Schliessungsbeleg in phase1_storage/CLAUDE.md §Geerbte Contracts; keine Python- oder JS-Datei in storage/mcpserver/webui/static angefasst, 958/958 pytest unveraendert, ui_budget 5/5 unveraendert) | 2026-09-02 (§9 Closeout gefüllt — Phase-8-Closeout in diesem Plan-Abschnitt per P8-N, Status 15 ✅ · 9 🟡 · 2 ⬜ vor Step-Z-Deploy; drei benannte Restdefekte + Glyph-Entscheidung dokumentiert, achte P1-Contract-Öffnung formal geschlossen; keine Python-/JS-Datei angefasst, keine Tests geändert, Sichtprüfung am echten Gerät + Sprung auf ✅ bleibt Nikinger-Aktion nach `deploy.sh main`) | 2026-08-28 (Nachtrag noch in der Planungssession: Step 0 als Fundament-Session Claude Code + Nikinger, C0 Anti-AI-Pattern-Research neu, P8-P gelockt, P8-25/26 + V93/V94) | 2026-08-28 (initial, Planungssession Claude Code Opus, N1–N12 vom Nikinger gelockt)
---
# Phase 8 — UI-Neuanstrich, Verknüpfungs-Graph, QoL (`phase8_ui_graph/`)

> **Planungsstand:** geschrieben am 2026-08-28 gegen `main`@`8f46745`, Live-Stand `e88a624`
> (v2.2). Alle zitierten Datei:Zeile-Anker wurden in der Planungssession gegen den echten Code
> geprüft — **der Ausführende prüft sie trotzdem erneut vor jedem Edit** (P7-Erfahrung:
> Zeilennummern driften um wenige Zeilen, Funktionsnamen nie).
>
> **Dokument-Konvention dieser Phase (P8-N):** EIN Dokument pro Phase. Dieses Dokument trägt am
> Ende (§9) den Closeout-Abschnitt — es gibt kein separates `PHASE8_CLOSEOUT_HANDOVER.md`.

---

## §0 Rahmen

### §0.0 Arbeitsweise (erstmals opencode/M3 als Ausführender)

- **Claude Code (Opus, high effort) hat geplant; opencode (Minimax M3 Thinking) führt aus.**
  Nikinger-Vorgabe aus dem P7-Handover §7, hier erstmals scharf. **Ausnahme: Step 0 ist die
  Fundament-Session** — sie läuft in Claude Code, gemeinsam und interaktiv mit dem Nikinger,
  und stellt erst die opencode-Fähigkeits-Parität her (§1). Ab Block A übernimmt opencode/M3.
- **Kein Advisor-Call während der Ausführung (P8-L, N12).** Die Qualitätsstufe, die in P7 elf
  Funde lieferte, wird ersetzt durch: (1) diese Planungstiefe, (2) die Pflicht-Testliste je
  Step, (3) die Selbstprüf-Checkliste am Step-Ende (§0.6), (4) Nikingers Sichtprüfung an den
  zwei Sichtprüfpunkten (§8).
- **opencode liest `CLAUDE.md`** — Voraussetzung dafür ist Step 0.4 (`AGENTS.md` entfernt,
  freigegeben 2026-08-28). Output-Styles/Plugins tragen nicht; alle Hard Rules stehen in
  `CLAUDE.md` selbst und gelten unverändert.
- **Tests:** vor jedem Commit `pytest -q` über das Repo, grün (Ausnahme: bekannter
  `test_authctl.py`-Flake — bei einem roten Lauf **zuerst prüfen, ob es der Flake ist**).
  Testprozesse erben **niemals** `SHAREFYX_*`/`SFX_*`-Env (hat historisch 52× den echten
  Dienst neu gestartet). Kein Test gegen den echten `DATA_ROOT` oder den laufenden Dienst;
  Wegwerf-Instanz (eigener Port, tmp-`DATA_ROOT`, eigenes venv) ist per Standing Permission
  erlaubt.
- **Commits:** Prefix `phase8:`, Doku-Update im selben Commit (Hard Rule 8), neue `.md` ⇒
  Indexzeile in `docs/INDEX.md` im selben Commit.

### §0.1 Nikinger-Entscheidungen N1–N12 (gelockt, 2026-08-28)

| # | Frage | Entscheidung |
|---|---|---|
| N1 | P7-24-Fix | **Option (d): kurzlebiges Reauth-Grant** (→ P8-A, Step A1) |
| N2 | remove-space-Reindex | **automatisch** (→ P8-B, Step A2) |
| N3 | P7-4 | Zweitprobe + nur Beschreibungstext schärfen; Eskalation wäre eine P8.1 (→ P8-C) |
| N4 | Graph-Kanten | **volles System aus allen drei Quellen**: `links:`-Feld + Body-Referenzen + implizite Kanten (Tags/Ordner) (→ P8-D) |
| N5 | Graph-Rendering | handgerollte Force-Simulation, kein Vendoring (→ P8-E) |
| N6 | Icon-Set | Empfehlung angenommen: **Lucide** (→ P8-F) |
| N7 | Schrift | IBM Plex Sans (+ Plex Mono). SF Pro war Nikingers Alternativvorschlag, ist aber **lizenzrechtlich ausgeschlossen** — Apples Font-Lizenz erlaubt keine Web-Self-Hosting-Nutzung (→ P8-G) |
| N8 | Liquid Glass | nur Akzente; **Auswahl bleibt immer eindeutig als ausgewählt sichtbar**, nie nur über Transparenz (→ P8-H) |
| N9 | Farblegende | **drei Kategorien**: eigener Space / geteilter Non-Home-Space / fremder Space (→ P8-I) |
| N10 | Übersicht | **tablos**; nur was gebraucht wird, keine Deko-Kacheln; der Graph ist das einzige grafische Element und hat funktionale Bedeutung (→ P8-J) |
| N11 | Version | Redesign + Graph = **v3.0** (→ P8-K) |
| N12 | Ausführung | opencode/M3, **kein Advisor während der Ausführung** (→ P8-L) |

### §0.2 Gelockte Entscheidungen P8-A – P8-Q

| # | Entscheidung | Kern |
|---|---|---|
| P8-A | P7-24-Fix als **Reauth-Grant** | 1× Passwort+TOTP an `POST /api/v1/reauth` → opakes, session-gebundenes Grant (TTL 90 s, in-memory, nie persistiert). Batch reicht das Grant statt Rohcredentials durch. Anti-Replay bleibt voll intakt: der TOTP-Code wird weiterhin genau einmal verbraucht. |
| P8-B | `_cmd_remove_space()` ruft am Ende `store.rebuild_index()` | Zweizeiler + Test; Warnhinweis-Variante verworfen (wird übersehen, reproduziert den 500er-Incident vom 2026-08-27). |
| P8-C | P7-4: Zweitprobe **vor** der Textänderung, dann `_TITLE_NOT_ID_HINT` schärfen | Rückgabeschema (Contract) bleibt unangetastet. Hält es wieder nicht → dokumentiertes Modellverhalten, Kandidat P8.1. |
| P8-D | Kanten aus drei Quellen | **explizit** = `links:`-Frontmatter-Einträge im `itm_`-Format + `itm_`-Referenzen im Body (serverseitig beim Indexieren extrahiert, → P8-M); **implizit** = gemeinsame Tags / gleicher Ordner, **rein clientseitig** aus den Knotendaten berechnet, per Toggle zuschaltbar. |
| P8-E | Graph handgerollt | Canvas 2D, eigene Force-Simulation (O(n²)-Repulsion reicht bei <300 Knoten), kein d3/cytoscape-Vendoring. Zwölftes JS-Modul `graph.js`. |
| P8-F | Icons: Lucide, **inline-Sprite in `app.html`** | Nur die ~30 gebrauchten SVGs, vendored unter `phase5_ui/vendor/lucide/` + `THIRD_PARTY_LICENSES.md`. Sprite als `<svg hidden>` mit `<symbol id="i-…">` direkt in `app.html` (Marker-Kommentare), Verwendung via `<use href="#i-…">` — same-document, keine CSP-Frage, kein Extra-Request. Externe Sprite-Datei verworfen (CSP-Einordnung externer `<use>`-Refs ist browserabhängig unklar). |
| P8-G | IBM Plex Sans (variabel) + IBM Plex Mono, Basis **16px** | OFL, Subsets über das bestehende Skript-Muster (`build_font_subset.sh` als Vorlage, gepinnter Release + SHA-256). SF Pro rechtlich tabu. Inter-Subset wird ersetzt, nicht ergänzt. |
| P8-H | Glass nur als Akzent | Dialoge/Overlays, Update-Banner, sticky Listen-Kopf, Toasts, Auswahl-Sheen. Pflicht: `@supports (backdrop-filter)`-Progressive-Enhancement + `prefers-reduced-transparency`-Fallback auf solide Flächen; Text auf Glas ≥ 4,5:1. Auswahl trägt **zusätzlich** einen soliden Akzent-Indikator (linke 3px-Kante + Outline). Chromium-only-Refraktionstricks (SVG-Displacement) sind tabu. |
| P8-I | Farbsemantik: 3 Space-Kategorien + bestehende Statusfarben | Tokens `--space-own` / `--space-shared` / `--space-foreign`; Startwerte §4.3, feinjustierbar **nur** in Nikingers Sichtprüfung. Sichtbare Mini-Legende in der Übersicht. Eine Farbe = eine Bedeutung; keine Deko-Farben, keine Gradients als Branding. |
| P8-J | Übersicht tablos | Kompakte Space-Zeilen mit klickbaren Zählern statt Kachel-Grid; Graph als Herzstück; „Zuletzt benutzt" bleibt; Öffnen der Übersicht schaltet die Listen-Spalte auf den globalen „Alle Items"-Scope. Graph wird **nicht** gepollt (Laden beim Öffnen + Refresh-Knopf); das 20-s-Zähler-Polling bleibt unverändert. |
| P8-K | `v3.0` im `.rail__version`-Badge | beim Deploy dieser Phase; Schema bleibt „bump je Deploy, nie zurück". |
| P8-L | Kein Advisor in der Ausführung | Ersatzmechanismen §0.0/§0.6. |
| P8-M | **Achte P1-Contract-Öffnung, benannt** | Neu: `storage/linkscan.py`; `index.py`: Tabelle `item_links` + `replace_item_links()` + Befüllung in `rebuild_index()`; `store.py`: Aufrufe an den Schreibpfaden + Lesemethode `links_all()`. **`models.py` und alle Dateiformate bleiben unangetastet; `test_characterization.py` (drei Golden Files) muss byte-identisch grün bleiben.** Datierte Notiz in `phase1_storage/CLAUDE.md` §„Geerbte Contracts" im Öffnungs-Commit. |
| P8-N | Ein Phasendokument | Closeout wird §9 dieses Dokuments; kein separates Handover-Dokument. |
| P8-O | `AGENTS.md` wird entfernt (Step 0.4) | Freigabe Nikinger 2026-08-28 (P7-Handover §7.2); `git rm` + INDEX-Zeile im selben Commit. |
| P8-P | Softcap-Ausnahme für zwei geschlossene Phase-Heads | `phase6_shares/CLAUDE.md` (~41 KB) und `phase5_ui/CLAUDE.md` (~41 KB): benannte Ausnahme in der jeweiligen INDEX-Zeile statt künstlicher Rotation (geschlossene Phase, genau ein Abschluss-Block, `rotate_session_block.sh` bräche mit `exit 2`). **Gelockt (Nikinger, 2026-08-28)** — Step 0.3 führt aus. |
| P8-Q | CSP bleibt byte-identisch | Alles ist self-hosted; `webui/security.py :: ui_security_headers()` wird in dieser Phase nicht angefasst. Abnahmekriterium: leerer Diff auf `security.py`. |

### §0.3 Verbotsliste (Anti-AI-Look, verbindlich für jeden UI-Commit)

1. Keine Emoji und keine HTML-Entity-Zeichen als Icons — nur das Lucide-Sprite.
2. Kein Indigo/Violett-Gradient, überhaupt kein Gradient als Flächen-Branding.
3. Keine generischen 3er-Feature-Card-Grids; Struktur über Dichte/Whitespace, nicht über Rahmen-Boxen.
4. Farbe nur mit Bedeutung (§4.3-Legende + bestehende Statusfarben) — nie dekorativ.
5. Keine neuen Schriftfamilien außer den zwei gelockten (Plex Sans/Mono).
6. Kein Element, dessen Erkennbarkeit allein von Transparenz/Blur abhängt (P8-H).

### §0.4 Tabu-Liste (Diff muss über die gesamte Phase leer bleiben)

- `authserver/` vollständig (auch `totp.py` — A1 **benutzt** `verify_reauth()`, ändert nichts darunter).
- `mcpserver/` vollständig **außer** reinen Beschreibungstext-Strings in `tools.py` (A3, Präzedenz P7-T).
- `phase5_ui/webui/security.py` (P8-Q).
- `storage/` außerhalb der in P8-M benannten Öffnung (insbesondere: `models.py`, `frontmatter.py`, `files.py`, `patch.py`, `acl.py`, `history.py` unangetastet).
- Prüfkommando am Step-Ende: `git diff --stat main -- phase4_auth/ phase2_mcp/ phase5_ui/webui/security.py phase1_storage/storage/models.py phase1_storage/storage/frontmatter.py phase1_storage/storage/files.py phase1_storage/storage/patch.py phase1_storage/storage/acl.py phase1_storage/storage/history.py` → einzige erlaubte Zeile: `mcpserver/tools.py` (nur A3-Textänderung).

### §0.5 DRAUSSEN (bewusst, nicht vergessen)

FastMCP-4/V79 (bleibt eigene Mini-Phase per P5-C; Recherche 2026-08-28: Spec 2026-07-28 ist RC,
Clients handeln auf 2025-11-25 herunter, kein Deprecation-Termin — kein Handlungsdruck) ·
Body-Volltextsuche in der Web-UI (Q1) · Rechteverwaltung über MCP-Tools (P6-M) · neues
MCP-Tool für den Graph (der Graph ist Mensch-UI; Claude erreicht Links über `links:`/`get_item`)
· Löschen von Items (F2) · `_trash/`-Räumung · Funnel-Watchdog · O4/O5/O7 · Glyph-Entscheidungen
P6/P6.5 (offene Nikinger-Entscheidungen, kein P8-Auftrag) · Mobile/Realtime · Light-Mode
(Designsystem bleibt Dunkel-first, P5-X).

### §0.6 Selbstprüf-Checkliste am Ende **jedes** Steps (Advisor-Ersatz)

1. `pytest -q` grün (Flake-Regel §0.0 beachten).
2. Tabu-Diff-Kommando aus §0.4 leer (bzw. nur die A3-Ausnahme).
3. Jeder in diesem Step berührte Endpunkt: einmal den Fehlerpfad durchdacht — was passiert bei
   fehlender Session, fremdem Space, ungültiger Version, unbekanntem Feld? (Die P7-Advisor-Funde
   waren fast alle von dieser Sorte: ungeschützte Route, falscher Space im Reauth, nicht
   eingefrorenes Batch-Ziel.)
4. Neue/geänderte `.md` haben L1-Card und INDEX-Zeile; Modul-Status-Tabelle + `## Session
   stopped`-Block im Phase-Head aktualisiert (Hard Rule 8).
5. Bei UI-Steps: `python phase5_ui/scripts/ui_budget.py` — alle vier Budgets grün.

### §0.7 `[VERIFY]`-Register V81–V92

| # | Frage | Wann |
|---|---|---|
| V81 | `pytest -q`-Ausgangsstand real 904? | Step 0.1 |
| V82 | Alle in diesem Plan zitierten Datei:Zeile-Anker (Sammelmarker — vor jedem Edit prüfen) | laufend |
| V83 | IBM-Plex-Release: gibt es variable TTFs für Sans (wght-Achse) im GitHub-Release `IBM/plex`? Exakte Asset-URL + SHA-256 pinnen; sonst statische 400/500/600-Subsets | C1 |
| V84 | Subset-Größen Plex Sans/Mono; `ui_budget.py` Gesamtbudget (<250 KB gzip app.js+css+Fonts) nach Fonts+Sprite+`graph.js` | C1/D3 |
| V85 | `prefers-reduced-transparency`-Support in den real genutzten Browsern (Firefox! — der Funnel-Incident-Report kam aus Firefox); Fallback muss unabhängig davon über `@supports` funktionieren | C4 |
| V86 | Wie die P7-ID-Suche an der API heißt (Query-Parameter von `_items_get` für den ID-Lookup) — für die `#item/`-Navigation wiederverwenden, nichts erfinden | B4 |
| V87 | Felder von `IndexStats` (für A2s stdout-JSON) | A2 |
| V88 | Exakter CSS-Klassenname der ausgewählten Listenzeile (Mehrfachauswahl, P7 Block B) für den Auswahl-Sheen | C4 |
| V89 | Wie Handler an die `session_id` kommen (`sessions.py :: SessionManager`, Cookie `COOKIE_NAME`) — Grant-Bindung A1 | A1 |
| V90 | Ob `_measure_latency()` in `ui_budget.py` um `GET /api/v1/graph` ergänzt wird (informativ, kein Budget) — Entscheidung des Ausführenden | B3 |
| V91 | `tags`/`folder`/`space`/`type`/`status` stehen in den Summary-Daten, die `_graph_get` je Knoten braucht (`serializers.py`) | B3 |
| V92 | Existieren die §4.2-Lucide-Icon-Namen in der gepinnten Lucide-Version? (Namen driften zwischen Releases) | C2 |
| V93 | Welcher opencode-Weg liefert Browser-Steuerung über den Harness (Playwright-MCP? opencode-eigene Tools?) — Stand bei Ausführung prüfen, nicht aus dieser Planung übernehmen | Step 0.7 |
| V94 | Hat opencode/M3 brauchbare Web-Recherche für C0? Sonst läuft C0-Teil 1 als Claude-Code-Zuarbeit | Step 0.7 / C0 |

---

## §1 Step 0 — Fundament-Session (Claude Code + Nikinger) + Haushalt

> **Step 0 läuft in Claude Code, gemeinsam mit dem Nikinger** — er legt das Fundament, auf dem
> opencode/M3 ab Block A ausführt. Erst wenn 0.6–0.8 stehen, wechselt der Harness.

0.1 `pytest -q` → Ausgangsstand notieren (Erwartung 904, V81).
0.2 **Verifikations-Durchlauf** (der Step-0-Platzhalter dieses Projekts): (a) Stichprobe
    Doku↔Code — die drei Erbposten-Beschreibungen des P7-Handovers §4 gegen den echten Code;
    (b) alle `up:`/`down:`-Frontmatter-Links auflösbar (`grep`-Lauf über alle L1-Cards);
    (c) jede `.md` außerhalb `.git`/`.claude`/`.agents` hat eine INDEX-Zeile;
    (d) Softcap-Scan (`du -b` über alle lebenden Heads). „Nichts zu tun" ist ein zulässiges
    Ergebnis und wird gemeldet. Bekannt aus der Planung: die zwei Übergrößen aus P8-P.
0.3 P8-P ausführen (gelockt): benannte Ausnahme-Notiz in den INDEX-Zeilen der beiden Heads.
0.4 `git rm AGENTS.md` + zugehörige INDEX-Zeile raus, **ein** Commit (P8-O).
0.5 Skelett: `phase8_ui_graph/CLAUDE.md` (L1-Card, Modul-Status-Tabelle, leerer
    `## Session stopped`-Block) + `phase8_ui_graph/SESSIONS_ARCHIVE.md`; zwei INDEX-Zeilen +
    ROADMAP-Statuswechsel ⬜→🔄 im selben Commit.
0.6 **opencode installieren und konfigurieren (gemeinsam mit dem Nikinger):** Installation ist
    sein Handgriff, Claude Code assistiert. Prüfen, dass opencode `CLAUDE.md` lädt (nach 0.4
    gibt es kein `AGENTS.md` mehr, das sie verdeckt). Regeldatei-Verhalten mit einer
    Kontrollfrage an den opencode-Agenten verifizieren, nicht annehmen.
0.7 **Fähigkeits-Parität herstellen** — Ziel: opencode kann möglichst dasselbe wie Claude Code
    in diesem Projekt braucht. Mindestens: (a) **Browser-Steuerung über den Harness** (Pendant
    zu claude-in-chrome; Kandidat: Playwright-MCP als `mcp`-Block-Eintrag, V93) — ohne sie sind
    die (W)-Zeilen der Abnahmematrix und der Playwright-Lauf D nicht fahrbar; (b)
    **Web-Recherche-Fähigkeit** prüfen (V94) — braucht C0; fehlt sie, läuft C0-Teil 1 als
    Claude-Code-Zuarbeit und opencode bekommt nur den Katalog. opencode-Plugins sind JS/TS,
    Claude-Code-Plugins tragen nicht (P7-Handover §7.1) — Äquivalente suchen, nicht portieren.
0.8 **Smoke-Test des Executors:** opencode führt auf einem Wegwerf-Branch eine Kleinsttask aus
    (Testdatei anlegen, `pytest -q` eines Einzelmoduls, Browser-Probe gegen eine
    Wegwerf-Instanz-Seite) — beweist Regeln, Tools und Browser-Pfad; Branch wird verworfen.
    Ergebnis + exakte Konfiguration (Plugins/MCP-Einträge, Versionen) in den Phase-Head.

**DoD Step 0:** pytest-Stand notiert, Verifikationsbericht im Session-Block, AGENTS.md weg,
Skelett steht, opencode konfiguriert + Smoke-Test bestanden (P8-26), Konfig dokumentiert.

---

## §2 Block A — Erbposten (fällt unter Druck NIE)

### A1 — Reauth-Grant (schließt P7-24; P8-A)

**Server, `phase5_ui/webui/reauth.py`** (heute: `verify_reauth()` ab Zeile 20, session-los):

```python
REAUTH_GRANT_TTL_S = 90.0

@dataclass
class ReauthGrant:
    session_id: str
    expires_at: float

class ReauthGrantStore:
    def issue(self, session_id: str, now: float) -> str: ...   # secrets.token_urlsafe(32)
    def check(self, token: str, session_id: str, now: float) -> bool: ...  # purged lazily
```

In-memory `dict[str, ReauthGrant]`, nie persistiert, nie geloggt, stirbt mit dem Prozess
(TTL 90 s macht das irrelevant). Bindung an die **Session** genügt: `verify_reauth()` prüft die
Credentials des angemeldeten Principals, nicht eines Ziel-Space — das Grant bedeutet „diese
Session hat sich vor < 90 s mit Passwort+TOTP ausgewiesen". Die Rechteprüfung je Item läuft
unverändert danach.

**[2026-08-31 Live urgency, Nikinger]** Erste echte N>2-Beobachtung aus dem Betrieb
(14-Item-Batch, alle rechteerweiternd): nicht nur der Mechanismus-Defekt aus dem Abnahme-Lauf
(Replay-Schleife ab Item 2), sondern die heute sichtbare Folge — bei N rasch aufeinander
folgenden, **verschiedenen** TOTP-Codes greift `LoginThrottle` (`authserver/ratelimit.py`)
und sperrt das Konto vorübergehend. Mit dem Grant-Fix entfällt der wiederholte TOTP pro Item
und damit jeder weitere Throttle-Eintrag; Beleg, dass P7-24 nicht-theoretisch ist und in der
P8-Priorität ganz oben steht.

**Neuer Endpunkt `POST /api/v1/reauth`** — Handler `_reauth_post()` in `webui/api.py`
(Registrierung neben den bestehenden Routen ~Zeile 1005, V82):
- Session-Pflicht (Plumbing wie `_items_patch`; `session_id` via `SessionManager`, V89).
- Body `{"password": str, "totp": str}` → `verify_reauth(userdir, throttle, store,
  space=<Session-Principal>, password=…, second_factor=…, now=…)` (reauth.py:20-29).
  Fehlversuche laufen damit automatisch in die bestehende `LoginThrottle`.
- 200 → `{"grant": "<token>", "expires_in": 90}`; falsche Credentials → 403, gedrosselt → 429
  (bestehende Fehlerkonvention von `errors.py` benutzen, nichts erfinden).
- Der Grant-Store hängt an der App neben der `LoginThrottle`-Instanz (App-Factory, V82).

**Akzeptanz des Grants:** `webui/shares.py :: require_share_reauth()` (Zeile 55) und
`require_space_reauth()` (Zeile 96): bevor der Passwort+TOTP-Pfad läuft — wenn der Request-Body
`reauth_grant` enthält und `grant_store.check(token, session_id, now)` wahr ist, gilt die
Re-Auth als erbracht. P7-N bleibt unangetastet (Space-Entfernen verlangt weiterhin zusätzlich
den getippten Namen). `_PATCH_FIELDS` (api.py:156) bekommt `"reauth_grant"` dazu — sonst 422
durch die A4-Whitelist.

**Client:** `dialogs.js` (Move-Dialog-Runde): wenn die Runde Credentials eingesammelt hat,
zuerst **ein** `POST /api/v1/reauth`; bei 200 wird `{reauth_grant: …}` als `credentials`-Objekt
an `list.js :: moveSelectedItems()` (Zeile 240-266) durchgereicht — dessen
`Object.assign({version, folder}, credentials)` (Zeile 246) braucht dafür **keine Änderung**.
Bei 403 zeigt der Dialog den Fehler und startet die Runde **nicht** (kein Item verbraucht).
Einzel-Item-Flows (Share-Dialog, einzelnes Verschieben) bleiben beim direkten
Passwort+TOTP-Pfad — kein Umbau ohne Not.

**Tests** (`phase5_ui/tests/test_reauth_grant.py`, neu):
1. Grant-Ausgabe mit korrekten Credentials → 200 + Token.
2. Falscher TOTP → 403, Throttle zählt.
3. Batch: 14 rechteerweiternde PATCHes mit demselben Grant → alle 200; Throttle-Counter
   unverändert vor und nach (Rate-Limit-Regression, N=14 entspricht dem Live-Fall).
4. Abgelaufenes Grant (Zeit vorgespult) → Re-Auth-Fehler wie bisher.
5. Grant einer fremden Session → abgelehnt.
6. Regression: derselbe **rohe** TOTP-Code zweimal → zweiter Request scheitert (Anti-Replay unverändert).
7. `reauth_grant` als Feld passiert die `_PATCH_FIELDS`-Whitelist; ein sonstiges unbekanntes Feld weiterhin 422.
8. Ohne Session → 401.

### A2 — `remove-space` reindiziert (P8-B)

`phase6_shares/scripts/spacectl.py :: _cmd_remove_space()` (Zeile 170-195): nach
`acl.remove_space_dir(...)` (Zeile 192) → `stats = store.rebuild_index()`
(`storage/store.py:809`, delegiert an `index.rebuild_index()`, index.py:187); Ergebnis ins
bestehende stdout-JSON (Feldnamen aus `IndexStats`, V87). **Test** in
`phase6_shares/tests/test_spacectl.py`: Space mit ≥1 Item anlegen, `remove-space --force`,
danach liefert eine Index-Query über alle Spaces keine Zeile des entfernten Space mehr und
wirft insbesondere kein `FileNotFoundError` (der Incident-Pfad von `_row_to_item()`).

### A3 — P7-4: Zweitprobe, dann Textschärfung (P8-C)

**Reihenfolge zwingend:** (1) Nikinger fährt die organische Zweitprobe („welche 3 Items sind
die aktuellsten") gegen die Live-Instanz **vor** jeder Textänderung — zweiter Datenpunkt.
(2) `mcpserver/tools.py :: _TITLE_NOT_ID_HINT` (Zeile 159-162) wird geschärft: Positiv- und
Negativbeispiel ergänzen (»Schreibe „Einkaufsliste Winter", nicht „itm_a1b2c3d4"; auch nicht
als Tabellen-Spalte«). Nur Beschreibungstext — P7-T-Präzedenz. (3) Test
`test_tool_descriptions_tell_the_agent_to_name_titles_not_ids` auf den neuen Wortlaut
anpassen. Ergebnis beider Proben wandert in die Abnahmezeile P8-5; hält es nach dem Deploy
wieder nicht → als Modellverhalten dokumentieren, Eskalation (Schema-Änderung) wäre P8.1.

---

## §3 Block B — Link-Fundament (achte P1-Contract-Öffnung, P8-M)

### B1 — `storage/linkscan.py` (neu)

```python
ITEM_REF_RE = re.compile(r"\bitm_[0-9a-f]{8}\b")   # exakt ITEM_ID_RE-Alphabet, files.py:40

def extract_item_refs(body: str) -> list[str]:
    """Eindeutige itm_-Referenzen in Auftrittsreihenfolge. Rein mechanisch, kein Verstehen."""
```

Ein Regex deckt beide expliziten Body-Formen ab — `#item/itm_…`-Hrefs **enthalten** das
`itm_`-Token. Kein Markdown-Parsen, keine Code-Block-Ausnahmen (eine ID in einem Code-Block
ist eine gemeinte Referenz; False-Positives sind bei 8 Hex-Zeichen hinter festem Präfix
praktisch ausgeschlossen). Pure Function, kein I/O.

### B2 — Index-Tabelle + Schreibpfade

`storage/index.py`: im Schema-Block (ab Zeile 29):

```sql
CREATE TABLE IF NOT EXISTS item_links (
  src_id TEXT NOT NULL, dst_id TEXT NOT NULL, kind TEXT NOT NULL,  -- 'frontmatter' | 'body'
  PRIMARY KEY (src_id, dst_id, kind)
);
CREATE INDEX IF NOT EXISTS idx_item_links_dst ON item_links(dst_id);
```

Neue Funktion `replace_item_links(conn, src_id: str, rows: list[tuple[str, str]]) -> None`
(DELETE WHERE src_id + Bulk-INSERT; `rows` = `[(dst_id, kind), …]`). `rebuild_index()`
(index.py:187) befüllt die Tabelle beim Voll-Rebuild mit (Hard Rule 2: Index bleibt vollständig
aus den `.md`-Dateien rekonstruierbar; ein Alt-Index ohne Tabelle heilt sich per
`CREATE IF NOT EXISTS` + Rebuild).

`storage/store.py`: an **jedem** Schreibpfad, der heute `upsert_item()` ruft
(create/update/patch/append/move/archive — Aufrufstellen per grep finden, V82):
`frontmatter_refs` = `links:`-Einträge, die `ITEM_REF_RE.fullmatch` bestehen (andere Strings im
freien `links:`-Feld bleiben erlaubt und werden schlicht keine Kante); `body_refs` =
`extract_item_refs(body)`; beides → `replace_item_links()`. Beim Entfernen eines Items aus dem
Index: `DELETE WHERE src_id` (dangling `dst_id`-Zeilen dürfen stehen bleiben — die API filtert).
Neue Lesemethode `Store.links_all(self) -> list[tuple[str, str, str]]` (src, dst, kind).

**Grenze der Öffnung:** genau diese drei Dateien (`linkscan.py` neu, `index.py`, `store.py`).
Kein Dateiformat, kein Modell, kein Frontmatter-Feld ändert sich —
`test_characterization.py` byte-identisch grün ist Abnahmekriterium (P8-14).

### B3 — `GET /api/v1/graph`

Handler `_graph_get()` in `webui/api.py`, Route neben `_overview` (~Zeile 1005):
- Knotenmenge = exakt die Items, die `_items_get` im globalen Scope liefern würde
  (dieselbe `can_read_item_as_human`-Filterung spiegeln, nichts Eigenes erfinden);
  `status=archived` draußen, `?archived=1` nimmt sie rein.
- Knoten-Payload minimal: `{id, title, space, own, shared, type, status, folder, tags}`
  (`own`/`shared` für die §4.3-Kategorie; Quelle `serializers.py`, V91).
- Kanten: `store.links_all()`, gefiltert auf `src != dst` und **beide** Endpunkte in der
  sichtbaren Knotenmenge (ACL-Leck-Riegel: ein unsichtbares Item existiert weder als Knoten
  noch als Kantenende), exakt dedupliziert.
- Antwort `{"nodes": […], "edges": [{"src","dst","kind"}, …]}`. Kein Polling (P8-J).
- **Tests** (`phase5_ui/tests/test_api.py`, neu `test_graph_*`): sichtbarer Fall mit
  frontmatter+body-Kante; fremdes `visibility:private`-Item erscheint weder als Knoten noch
  als Kantenende; dangling-Referenz erzeugt keine Kante; `archived`-Default; ohne Session 401.
- Storage-Tests: `phase1_storage/tests/test_linkscan.py` (Href-Form, nackte ID, Dedupe,
  Reihenfolge, kein Treffer) + Erweiterung der Index-/Store-Tests (upsert füllt, rebuild
  füllt, Entfernen räumt src-Zeilen).

### B4 — UI-Anschluss der Links (QoL)

- **`#item/`-Navigation:** Klick-Delegation (in `app.js` oder `editor.js`, wo die
  Body-Container-Events heute hängen, V82) auf `a[href^="#item/"]` → Item über den bestehenden
  P7-ID-Lookup öffnen (Parameter von `_items_get`, V86 — **wiederverwenden, nicht neu bauen**).
  `markdown.js :: safeHref()` (Zeile 223-228) whitelisted das Schema bereits; Rendering
  unverändert.
- **Link-Picker:** neuer kleiner Dialog `link-picker-dialog` in `app.html` (Muster der
  bestehenden `.overlay`-Dialoge), geöffnet über einen Icon-Knopf neben dem Links-Feld
  (`app.html:126-128`): Suchfeld → `GET /api/v1/items` global (Titel/Tags-Suche, existiert),
  Trefferklick hängt die `itm_`-ID ans `#field-links` an (Komma-Konvention des Feldes).
  `links` steht bereits in `_PATCH_FIELDS` (api.py:156) — kein API-Umbau.

**GATE B→C (hart):** voller `pytest` grün · `test_characterization.py` byte-identisch ·
Tabu-Diff leer · `_graph_get` gegen eine Wegwerf-Instanz mit ≥3 Spaces/ACL-Fall manuell
geprüft. Erst dann Designarbeit.

---

## §4 Block C — Design-Fundament v3 (De-AI-isierung)

### C0 — Anti-AI-Pattern-Research + UI-Audit

**Teil 1 — Research (Web, V94):** frische Recherche „woran erkennt man AI-generierte UIs und
wie behebt man es" — Designer-Blogs, offizielle Styleguides (Apple HIG, Material), Stand zum
Ausführungszeitpunkt. Startpunkt ist der Katalog unten (Planungsrecherche 2026-08-28); die
Recherche **ergänzt** ihn, sie beginnt nicht bei null.

**Starter-Katalog (Muster → Fix):**
1. Emoji/HTML-Entities als Icons → echtes Icon-System (C2)
2. Indigo/Violett-Gradients, Gradient-Branding → Farbsemantik-Tokens, Verbotsliste §0.3 (C3)
3. Inter als unreflektierter Default → bewusste Schriftentscheidung Plex (C1)
4. Austauschbare Card-Grids mit 1px-Grau-Rand → Struktur über Dichte/Whitespace (C5, D1)
5. Uniformes border-radius + Schatten auf allem → gezielte Erhebungsebenen (bestehende Plastik-Tokens aus Step 7b weiternutzen, nicht ersetzen)
6. Dekorative Farben ohne Bedeutung → eine Farbe = eine Bedeutung (C3)
7. Generische Marketing-Microcopy → nüchterne deutsche UI-Texte im Bestandston
8. Marketing-Seiten-Großzügigkeit (zentrierte Heros, riesige Abstände) in einer Daten-UI → dichte Arbeitsfläche (C5)

**Teil 2 — Audit:** systematischer Durchgang durch `app.html`, `app.css` und alle
JS-Render-Stellen gegen den (ergänzten) Katalog. Ergebnis: **Findings-Tabelle
Muster → Fundstelle (Datei:Zeile) → Fix → Ziel-Step (C1–C5/D1)** im Phase-Head. Ein Fund ohne
Heimat-Step wird eine **benannte Nikinger-Entscheidung**, kein stiller Scope-Zuwachs (P8-25).
C1–C5 arbeiten danach die Tabelle ab, nicht nur die Plan-Aufzählung.

### C1 — Typografie (P8-G)

- Neues Skript `phase5_ui/scripts/build_font_subset_plex.sh` nach dem Muster von
  `build_font_subset.sh` (dessen Kopf dokumentiert das Verfahren: gepinnter Release-Download +
  SHA-256, `pyftsubset`, Latin-Unicodes, Hash im Dateinamen → `immutable`-Cache über
  `_HASHED_NAME_RE`, static_routes.py:43). Quelle: GitHub-Release `IBM/plex` (V83).
  Sans: variable wght-Achse auf 380–620 beschneiden wie beim Inter-Vorbild; falls kein
  variables TTF im Release → statische Subsets 400/500/600. Mono: ein statisches
  400er-Subset.
- `app.css:13-19`: beide `@font-face`-Blöcke ersetzen; Inter-Dateien + Inter-`OFL.txt` raus,
  Plex-`OFL.txt` rein (Lizenztext ist Pflichtbestandteil).
- Tokens (`app.css:44-45`): `--font-ui: "IBM Plex Sans Var", ui-sans-serif, system-ui, …`;
  `--font-mono: "IBM Plex Mono", ui-monospace, …`. **IDs, Versions-Badge und Metazeilen rendern
  in `--font-mono`** (die `itm_`-ID-Chips aus P7-A1 sind der Hauptnutzer).
- Typo-Skala als Tokens statt Streu-px: `--fs-meta: 12.5px; --fs-ui: 14px; --fs-body: 16px;
  --fs-title: 18px; --fs-page: 22px`. `body` (app.css:79-86): `font-size: 16px;
  line-height: 1.55`. Lesebreite des gerenderten Bodys: `max-width: 72ch`.
- `ui_budget.py`-Lauf direkt nach dem Font-Swap (V84) — Fonts sind der größte Einzelposten.

### C2 — Icon-System (P8-F)

- Vendoring: `phase5_ui/vendor/lucide/` — nur die gebrauchten SVGs (gepinnte Lucide-Version im
  Ordner-README notieren) + `phase5_ui/THIRD_PARTY_LICENSES.md` (Lucide ISC, IBM Plex OFL).
- Generator `phase5_ui/scripts/build_icon_sprite.py`: liest `vendor/lucide/*.svg`, schreibt den
  Sprite-Block (`<svg hidden id="icon-sprite">…<symbol id="i-<name>" viewBox="0 0 24 24">`)
  zwischen die Marker `<!-- ICONS:BEGIN -->` / `<!-- ICONS:END -->` in `app.html`. Idempotent;
  wird von Hand aufgerufen (kein Build-Step zur Laufzeit, P5-T bleibt gewahrt).
- CSS: `.icon { width: 1.25em; height: 1.25em; stroke: currentColor; fill: none;
  stroke-width: 2; vertical-align: -0.25em; }` — Farbe folgt dem Text, keine Sonderfarben.
- **Ersetzungs-Map** (Entities → `<use href="#i-…">`), V92 für die Namen:
  | Stelle | heute | Icon |
  |---|---|---|
  | `app.html:23` Übersicht | `&#8962;` | `house` |
  | `app.html:33` Konto | `&#9881;` | `settings` |
  | `app.html:39` Abmelden | `&#9099;` | `log-out` |
  | `app.html:50` Anlegen | `&#43;` | `plus` |
  | `app.html:141/143/147` Editor-Leiste | `&#128279;`/`&#8221;`/`&#128444;` | `link` / `quote` / `image` |
  | `list.js:197` Chip-X | `×` | `x` |
  | `list.js:351` Verschieben | `→` | `folder-input` |
  | `list.js:368` Freigeben | `⇄` | `share-2` |
  | neu: Übersicht/Graph, Refresh, Suche, Ordner, Baum-Chevrons, Warn/Info in Dialogen | — | `waypoints`, `refresh-cw`, `search`, `folder`, `chevron-right/-down`, `triangle-alert`, `info` |
- JS-Helfer `js/icons.js` (dreizehntes Modul, winzig): `iconSvg(name)` → Markup-String für
  dynamische Einfügungen (list.js/tree.js/dialogs.js). Kein Inline-Script in `app.html` (CSP).
- `.rail__glyph` (Space-Anfangsbuchstabe, list.js:76/tree.js:204) **bleibt ein Buchstabe** —
  das ist Identität, kein Icon; er bekommt in C3 die Kategoriefarbe.
- Abnahme-Grep: `grep -nE '&#[0-9]+;' app.html` + Literal-Suche `→`/`⇄`/`×` in `js/` → 0 Icon-Treffer.

### C3 — Farbsemantik + Legende (P8-I)

- Neue Tokens in `:root` (app.css:21-70), Startwerte — Feinjustierung nur in Nikingers
  Sichtprüfung: `--space-own: #4A93F0` (Markenblau-Familie), `--space-shared: #2EB8A6` (Teal),
  `--space-foreign: #8B93A1` (neutrales Slate — „nicht deins" darf leise sein). Abstand zu
  `--warn: #E5A93C` / `--danger: #E5484D` ist gegeben; AA-Kontrast auf `--bg` prüfen.
- Kategorie-Ableitung im Client (`state.js`-Helfer `spaceCategory(space)`): `own` =
  Home-Space der Session, `shared` = `writable && !own`, `foreign` = Rest — die Felder liefert
  `GET /spaces` heute schon (P6-Badge-Fix).
- Anwendung überall identisch: `.rail__glyph`-Rand/Fond, Space-Punkt vor der Metazeile im
  globalen Listen-Scope (list.js:119-126 `itemMetaLine()`-Umfeld), Übersichts-Space-Zeilen
  (§5), Graph-Knoten (§5). **Statusfarben bleiben wie sie sind** (Akzent=interaktiv,
  Amber=warn, Rot=danger).
- Legende: kleines statisches Element im Übersichts-Kopf (`.legend`, drei Punkte + Label).

### C4 — Liquid-Glass-Akzente (P8-H)

- Tokens: `--glass-bg: rgba(27,32,39,.55); --glass-border: rgba(255,255,255,.14);
  --glass-blur: 14px;` und eine Utility-Klasse:

  ```css
  .glass { background: var(--surface-raised); border: 1px solid var(--glass-border);
           box-shadow: inset 0 1px 0 rgba(255,255,255,.08); }        /* Fallback = solide */
  @supports (backdrop-filter: blur(1px)) {
    .glass { background: var(--glass-bg);
             backdrop-filter: blur(var(--glass-blur)) saturate(1.5); } }
  @media (prefers-reduced-transparency: reduce) {
    .glass { backdrop-filter: none; background: var(--surface-raised); } }
  ```

- Träger: `.overlay`-Dialogkarten, `.update-banner`, `.list__head` (sticky über scrollender
  Liste — hier zahlt Glas funktional: man *sieht*, dass Inhalt darunter durchläuft), Toasts.
- **Auswahl-„Wassertropfen"** (Hochglanz-Sheet-Bild aus dem Auftrag): die ausgewählte
  Listenzeile (Klassenname V88) bekommt den Glass-Sheen (Top-Highlight + leichte Aufhellung)
  **plus** solide 3px-Akzentkante links + 1px-Akzent-Outline — die Auswahl bleibt bei
  deaktiviertem Blur/reduzierter Transparenz vollständig erkennbar (N8-Bedingung, P8-H).
- Kontrastpflicht: Text auf jeder Glass-Fläche ≥ 4,5:1 gegen den effektiven Grund.

### C5 — Dichte, Platz, Kleinigkeiten

- Listenzeilen: zweizeiliges Grid (Titel 16px / Metazeile 12,5px mono), vertikales Padding so,
  dass trotz größerer Schrift ≥ 1 Zeile mehr pro Bildschirm sichtbar ist als heute (bessere
  Platzausnutzung ist Auftrag, nicht Nebeneffekt).
- Editor: Body-Spalte zentriert auf `72ch`, Meta-Panel feste Breite — kein Vollbreiten-Flattern.
- Tastatur-QoL: `/` fokussiert die Listensuche (wenn kein Eingabefeld fokussiert ist).

**Sichtprüfpunkt 1 (Nikinger, Wegwerf-Instanz oder Screenshots):** Typo-Größen, die drei
Kategoriefarben, Glass-Intensität. Feinwerte dürfen hier justiert werden, Struktur nicht.

---

## §5 Block D — Übersicht + Graph

### D1 — Übersicht tablos (P8-J)

`list.js :: renderOverview()` (Zeile 31-86) + `loadOverview()` (Zeile 97-115) werden ersetzt,
`app.html:71-77` (`#detail-overview`) neu strukturiert — von oben nach unten:
1. Kopfzeile: Titel, `.legend` (C3), Refresh-Icon (lädt Overview **und** Graph neu).
2. **Kompakte Space-Zeilen statt Kachel-Grid:** je Space eine Zeile — Kategoriepunkt (C3),
   Name, dahinter die Zähler als klickbare Inline-Chips (`open · done · note`, Klick navigiert
   wie heute die Kacheln; Datenquelle unverändert `_overview()`, api.py:539-568). Keine
   Deko-Kacheln, keine leeren Buckets.
3. **Graph-Panel** (`#overview-graph`, `<canvas>`, ~55vh) — das einzige grafische Element.
4. „Zuletzt benutzt" bleibt (Bestandslogik).
Öffnen der Übersicht schaltet die Listen-Spalte auf den globalen Scope („Alle Items",
`tree.js:34-37`-Mechanik aufrufen, **nicht** duplizieren) — damit ist „alle Items als
Übersichtsliste" erfüllt, ohne die Liste in die Detailfläche zu kopieren. Achtung Regression
P6-Advisor-Fund: `editor.js :: clearDetail()` setzt `state.scope` zurück — Zusammenspiel
testen, nicht umgehen (V82).
Das 20-s-Polling (`app.js:211-222`, `COUNTER_POLL_MS`) bleibt für die Zähler; der Graph lädt
nur bei Öffnen/Refresh (P8-J).

### D2 — `js/graph.js` (Graph-Modul, handgerollt; P8-D/P8-E)

Umfang realistisch 300–400 Zeilen. Struktur:

- **Daten:** `loadGraph()` → `GET /api/v1/graph`; Knoten bekommen `cat` über
  `spaceCategory()` (C3) und `deg` (Gradzahl über explizite Kanten).
- **Implizite Kanten, clientseitig (P8-D):** `tagEdges(nodes)` — Kante zwischen Knoten mit
  ≥ 1 gemeinsamem Tag, **Tags, die auf > 15 Knoten vorkommen, werden übersprungen**
  (Clique-Riegel); `folderEdges(nodes)` — Kante zwischen Knoten mit gleichem `space`+`folder`,
  `folder != ""`. Zwei Checkbox-Toggles im Graph-Panel („Tags", „Ordner"), Default **aus** —
  der Default-Graph zeigt gemeinte, nicht zufällige Struktur.
- **Simulation:** flache Arrays, `tick()`: paarweise Repulsion (O(n²), Cutoff-Distanz),
  Federkraft je Kante (Ruhelänge ~60px), leichte Zentrums-Gravitation, Dämpfung ~0.85,
  Alpha-Decay, Stopp bei α < 0.005; Drag reheizt (α = 0.3). `requestAnimationFrame`-Loop
  endet mit der Simulation — kein Dauerbrenner.
- **Rendering:** Canvas 2D, `devicePixelRatio`-korrekt. Knotenradius `4 + 2·log2(1+deg)`,
  Kappe 12. Knotenfüllung = Kategoriefarbe. Kantenstile: explizit solide (frontmatter/body
  ununterschieden), Tag gestrichelt `[4,4]`, Ordner gepunktet `[1.5,3]`. Labels nur bei
  Zoom > 1.2 oder für Hover-Nachbarschaft.
- **Interaktion (Obsidian-Referenz-UX):** Hover → Nachbarn hervorheben, Rest auf 15 % Alpha
  dimmen; Klick → Item öffnen (derselbe ID-Lookup wie B4); Node-Drag; Wheel-Zoom 0.5–2.5 +
  Hintergrund-Pan; Doppelklick auf Hintergrund → Ansicht zurücksetzen.
- **`prefers-reduced-motion`:** Simulation synchron zu Ende rechnen (~300 Ticks), statisch
  rendern — kein animiertes Einschwingen.
- **Leerzustand:** kein Knoten mit Kante → Hinweistext („Verknüpfe Items über das Links-Feld
  oder eine itm_-Referenz im Text") statt leerer Fläche.

### D3 — Versionierung + Budget (P8-K)

`.rail__version` (app.html:20) → `v3.0`. `docs/UPDATE_LOG.md`: neuer oberster Eintrag **am
Deploy-Tag** (P6-X-Gate: `deploy.sh` verlangt das heutige Datum). `ui_budget.py`-Lauf: alle
vier Budgets grün (V84); `_measure_latency()`-Erweiterung um `/graph` nach Ermessen (V90).

**Sichtprüfpunkt 2 (Nikinger, Wegwerf-Instanz):** Übersicht + Graph mit realistischen Daten
(~30 Items, gemischte Kategorien). Playwright-Durchlauf gegen die Wegwerf-Instanz (Muster
`GLOBAL_SEARCH_PLAN.md`): Übersicht öffnen → globaler Scope aktiv → Graph rendert → Klick auf
Knoten öffnet Item → Legende sichtbar.

---

## §6 Step Z — Closeout

1. Abnahmematrix §7 vollständig durchgehen (live, durch den Nikinger; Wegwerf-Instanz-Zeilen
   dürfen von der Ausführung vorbelegt, müssen aber benannt werden).
2. Deploy: `deploy.sh main` durch den Nikinger (UPDATE_LOG-Gate beachten), Health-Gate 3/3,
   danach die Live-Zeilen der Matrix.
3. §9 dieses Dokuments füllen (Closeout statt eigenem Handover, P8-N); Übersichtsgrafik
   `docs/concepts/phase8_ui_graph_uebersicht.svg` (Render-Check per SVG-Tool);
   Root-`CLAUDE.md` „Current state", `ROADMAP.md`-Status, INDEX-Zeilen; Rotationsprüfung des
   Phase-Heads; Glyph-Entscheidung (✅ nur live-verifiziert) ist Nikingers.

---

## §7 Abnahmematrix P8-1 – P8-26

**Statusregel unverändert: ✅ heißt live-verifiziert durch einen Menschen, nicht „gebaut".**
(W) = Wegwerf-Instanz zulässig, (L) = nur live, (C) = Code/Test-Nachweis genügt.

| # | Kriterium |
|---|---|
| P8-1 (L) | Batch-Verschieben von ≥ 2 rechteerweiternden Items gelingt mit **genau einer** Passwort+TOTP-Eingabe (P7-24 geschlossen) |
| P8-2 (C) | Derselbe rohe TOTP-Code zweimal → zweiter Request abgelehnt (Anti-Replay-Regression) |
| P8-3 (C) | Abgelaufenes/fremdes Grant → Re-Auth-Fehler; Fehlversuche am Grant-Endpunkt drosseln |
| P8-4 (W) | `spacectl.py remove-space --force` hinterlässt keinen stalen Index; Overview-Pfad antwortet danach 200 |
| P8-5 (L) | P7-4-Zweitprobe vor der Textänderung gefahren + Ergebnis dokumentiert; nach Deploy dritte Probe dokumentiert |
| P8-6 (W) | `links:`-Eintrag und `itm_`-Body-Referenz erscheinen beide als Kante im Graph |
| P8-7 (C) | `rebuild_index()` rekonstruiert `item_links` vollständig nach Index-Löschung (Hard Rule 2) |
| P8-8 (L) | ACL: ein nicht lesbares Item erscheint weder als Knoten noch als Kantenende (echter Zweitnutzer-Fall) |
| P8-9 (W) | Klick auf `#item/…`-Link im gerenderten Body öffnet das Ziel-Item |
| P8-10 (W) | Link-Picker findet per Titelsuche und befüllt das Links-Feld |
| P8-11 (C) | `test_characterization.py` byte-identisch grün über die gesamte Phase |
| P8-12 (C) | Tabu-Diff (§0.4) leer bis auf die A3-Textänderung |
| P8-13 (C) | `grep -nE '&#[0-9]+;' app.html` und Literal-`→`/`⇄`/`×` in `js/` → 0 Icon-Treffer; `THIRD_PARTY_LICENSES.md` existiert |
| P8-14 (L) | Schriftbild: Plex 16px Basis, Nikinger bestätigt Lesbarkeit („größer und klarer") am echten Gerät |
| P8-15 (L) | Farblegende sichtbar; own/shared/foreign konsistent in Rail, Liste (globaler Scope), Übersicht und Graph |
| P8-16 (W) | Glass-Fallback: mit deaktiviertem `backdrop-filter` (oder reduzierter Transparenz) bleiben alle Flächen solide und die Auswahl eindeutig erkennbar |
| P8-17 (C) | `ui_budget.py`: alle vier Budgets grün nach Fonts+Sprite+`graph.js` |
| P8-18 (L) | Übersicht tablos: Space-Zeilen mit klickbaren Zählern, Graph eingebettet, „Zuletzt benutzt" vorhanden, keine Deko-Kacheln |
| P8-19 (L) | Öffnen der Übersicht aktiviert den globalen „Alle Items"-Scope in der Listen-Spalte |
| P8-20 (W) | Graph: Hover dimmt Nicht-Nachbarn, Klick öffnet das Item, Drag/Zoom/Pan funktionieren |
| P8-21 (W) | Tag-/Ordner-Toggles wirken; Default zeigt nur explizite Kanten; >15-Knoten-Tag erzeugt keine Clique |
| P8-22 (W) | 200-Knoten-Wegwerf-Datensatz: Simulation kommt < 3 s zur Ruhe, Interaktion ohne spürbares Haken; `prefers-reduced-motion` rendert statisch |
| P8-23 (L) | `v3.0`-Badge live, UPDATE_LOG-Eintrag vorhanden, Health-Gate 3/3 nach Deploy |
| P8-24 (W) | Playwright-Durchlauf gegen die Wegwerf-Instanz grün (Übersicht→Scope→Graph→Knotenklick→Item) |
| P8-25 (C) | C0-Findings-Tabelle existiert im Phase-Head; jeder Fund auf einen Step gemappt oder als benannte Nikinger-Entscheidung eskaliert |
| P8-26 (W) | Fundament: opencode steuert nachweislich einen Browser gegen eine Wegwerf-Instanz (Smoke-Test 0.8) — Voraussetzung aller (W)-Zeilen |

---

## §8 Reihenfolge und Fallregel

**0 (Fundament, Claude Code) → A → B → GATE → C (C0→C5) → D → Z.** Zwei Nikinger-Sichtprüfpunkte: nach C (Typo/Farben/Glass)
und in D (Übersicht/Graph). Unter Druck fällt zuerst D2-Feinschliff (Labels, Zoom-Komfort),
dann C4 (Glass), dann C5 — C0-Teil 2 (Audit) fällt nie, er ist billig und trägt die Verbotsliste — **nie Block A, nie die B-Integrität (ACL-Filter, Hard Rule 2,
Characterization)**. Ein UI-Schnitt ohne Glass ist auslieferbar; einer mit ACL-Leck nicht.

---

## §9 Closeout (Phase-8-Closeout — P8-N: kein separates Handover-Dokument)

> §9 ist nach P8-N **das** Closeout-Dokument dieser Phase. Es ersetzt ein separates
> `PHASE8_CLOSEOUT_HANDOVER.md`. Wer die äquivalente Form aus P7 gewohnt ist, findet sie hier.

### §9.1 Status in fünf Sätzen

1. **Phase 8 ist inhaltlich vollständig** — drei P7-Erbposten (Reauth-Grant,
   `remove-space`-Auto-Reindex, P7-4-Zweitprobe), achte P1-Contract-Öffnung
   (`linkscan.py`, `item_links`, `Store.links_all`, `GET /api/v1/graph`), Link-Picker,
   Design-Fundament v3 (Plex + Lucide + Farbsemantik + Glass + Dichte), tabellose
   Übersicht + handgerollter Canvas-Force-Graph, Versions-Bump v3.0 + UPDATE_LOG-Eintrag.
   **Bilanz 15 ✅ · 9 🟡 · 2 ⬜** von 26 Abnahmezeilen, Stand 2026-09-02 vor
   Step-Z-Deploy.
2. **Block A + B sind live seit `main@007b73d`** (Release `20260901T103944.634877Z`,
   Health-Gate 3/3 grün, `.rail__version` v2.2.3). Block C + D (21+ Commits seit dem
   letzten Live-Build) liegen lokal gestapelt — **das nächste `deploy.sh main` ist die
   Nikinger-Aktion**, das ist Hard-Rule-konform (niemals `sudo deploy.sh` aus dem
   `savefyx`-User).
3. **Der C0-Audit hat 35 Anti-AI-Pattern-Findings produziert, 0 davon eskaliert.** Die
   Verbotsliste §0.3 hat über die gesamte Phase gehalten — jeder Fund war auf einen
   Step gemappt oder bereits aligned. P8-25 ✅.
4. **Drei benannte Restdefekte wandern explizit in §9.4** (A3 Klammer/Aufzählung,
   Item-Link-Picker-Body-Lücke, Picker-A11y `aria-selected`) — kein Scope-Silentium,
   keine stillen Aufweichungen, benannte Punkte mit Optionen oder bewussten Vormerkungen.
5. **Die geänderte Arbeitsweise (Claude Code plant, opencode/M3 führt aus) hat operativ
   gehalten** — ~14 echte Selbstfunde über die gesamte Phase, davon 0 Blocker
   (P7-Bilanz zum Vergleich: 11 Funde mit 4 Blockern). Selbstprüf-Checkliste §0.6 und
   Playwright-Smoke-Pfad haben den Advisor-Call substituiert; die offene Frage ist die
   Glyph-Entscheidung ✅ vs. 🟡 (Nikinger, nach Live-Deploy + Sichtprüfung).

### §9.2 Delta seit dem P7-Handover

| Was | Wo | Bemerkung |
|---|---|---|
| Reauth-Grant (P7-24-Schließung) | `webui/reauth.py`, `webui/api.py :: _reauth_post`, `dialogs.js`, `list.js` | TTL 90 s, in-memory, session-gebunden; Anti-Replay scharf (TOTP genau einmal verbraucht); `90441b29`, live-verifiziert mit N=14-Batch |
| `remove-space`-Auto-Reindex | `phase6_shares/scripts/spacectl.py :: _cmd_remove_space()` | nach `remove_space_dir()` Zweizeiler `store.rebuild_index()`; `90441b29`, Live-Probe `Test_Space_A2` |
| `_TITLE_NOT_ID_HINT` geschärft | `mcpserver/tools.py` (nur Beschreibungstext, P7-T-Präzedenz) | `7254aa9`; Klammer/Aufzählung bleiben benannter Restdefekt (§9.4.1) |
| **Achte P1-Contract-Öffnung** | `storage/linkscan.py` (neu) · `index.py` (Tabelle `item_links` + Index, `replace_item_links`, `rebuild_index` populiert) · `store.py` (`_replace_links_for_item`, `Store.links_all`, 6 Schreibpfade, Drift-Repair) | `ed43ed6` + `f4c8844`; **mit §9.6 formal geschlossen** |
| `GET /api/v1/graph` | `webui/api.py :: _graph_get` | ACL-Filterung exakt wie `_items_get`; `58ff9a6`; P8-8 (Zweitnutzer-Pass-Through) bleibt 🟡 |
| `#item/`-Klick-Delegation | `app.js:107-115` | wiederverwendet P7-ID-Lookup-Parameter aus `_items_get` |
| Link-Picker-Dialog | `app.html`/`app.css`/`dialogs.js`/`editor.js` | füllt nur `links:`-Feld; kein Body-Pfad → Restdefekt (§9.4.2) |
| Lucide-Sprite + `js/icons.js` + `.icon`-CSS | `phase5_ui/vendor/lucide/`, Sprite-Block in `app.html`, `js/icons.js` (13. JS-Modul) | 18 Icons, ISC + MIT; V92 gepinnt (Lucide 1.38.0, SHA-256 d28944cf…) |
| Plex Sans/Mono | `phase5_ui/webui/static/fonts/`, Typo-Tokens in `app.css` | V83 gepinnt; Subsets via `build_font_subset_plex.sh` |
| Farbsemantik + Legende | `app.css` (`--space-own`/`--space-shared`/`--space-foreign`), `state.js :: spaceCategory()`, `.legend` | drei Kategorien + Mini-Legende in Übersicht |
| Liquid-Glass-Akzente | `app.css` (`--glass-{bg,border,blur,highlight}`-Tokens, `.glass`, `@supports`, `@media (prefers-reduced-transparency)`) | Auswahl trägt soliden Akzent-Indikator (N8) |
| `::selection` + 72ch-Editor + Padding-Token | `app.css` | F5/F21/F22 aus C0-Audit |
| Tabellose Übersicht + Counter-Chips | `list.js`, `app.html`/`app.css`/`app.js` | ersetzt das Kachel-Grid (F12/F13/F23); globaler Home-Scope beim Übersicht-Öffnen |
| Canvas-Force-Graph (handgerollt) | `js/graph.js` (~542 Zeilen, 6.2 KB gzipped) | 12. JS-Modul; Tag/Ordner-Toggles mit >15-Knoten-Cutoff; `prefers-reduced-motion` synchron 300 Ticks |
| Versions-Bump v2.2.3 → v3.0 | `app.html` `.rail__version` | Major bleibt v2, Patch = Phase-Step-Counter (P8-K) |
| UPDATE_LOG-Eintrag | `docs/UPDATE_LOG.md` | 2026-09-02, vier Bullet-Points (Übersicht tabellos, Verknüpfungs-Graph, globaler Home-Scope, Mini-Legende) |
| `AGENTS.md` entfernt | Repo-Wurzel | P8-O (Nikinger-Freigabe 2026-08-28) — opencode fällt damit auf `CLAUDE.md` zurück |
| opencode/M3-Setup | global installiert, Playwright-MCP verbunden, Nikinger-Auth gesetzt | V93, V94 erfüllt in Step 0.7 |
| Selection/Choice-Konvention v3 | Phase-Head (Doku) | vier-gliedrige Taxonomie (Choice/Toggle/Status/Navigation) + Chevron-Data-URL auf `select.input`; **erste Konvention, die *während* einer Phase entstand**, nicht im Plan stand |
| `phase8_ui_graph/scripts/{wegwerf_setup_*, *_smoke.py}` | neu | sieben Setup-/Smoke-Paare (`c3_/c4c5_/d1_/d2_/sichtpruefung2_/auswahl_chevron_`); Standing-Permission-Muster (Port-Range, File-Keyring, eigenes venv) pro Block reproduziert |
| 200-Knoten-Wegwerf-Fixture | `phase8_ui_graph/scripts/wegwerf_setup_200knoten.py`, `p8_22_smoke.py` | ⬜ P8-22 — Skript-Arbeit für eine nächste Session, nicht in dieser Phase gefahren |
| Kombinierter E2E-Smoke | `phase8_ui_graph/scripts/phase8_e2e_smoke.py` | 🟡 P8-24 — drei Teil-Smokes decken Teilpfade ab, der Ritt fehlt |

**Nicht angefasst** über die gesamte Phase: `mcpserver/asgi.py`,
`mcpserver/{server,permissions}.py`, `authserver/` (alle Krypto-Module),
`webui/security.py` (P8-Q), `storage/{models,frontmatter,files,patch,acl,history}.py`
(Tabu-Liste §0.4). **Tabu-Diff-Kommando** war bis auf die A3-Beschreibungstext-Ausnahme
in jedem Block-C leer — Disziplin gehalten.

### §9.3 Abnahmestand

**Verweis:** die kanonische Form ist die §7-Matrix im Phase-Head (26 Zeilen mit Status +
Beleg). Hier nur die Bilanz + drei Erläuterungen.

**15 ✅ · 10 🟡 · 0 ⬜** (Stand 2026-09-02, nach den 200-Knoten- und E2E-Smokes, vor
Step-Z-Deploy):

| Cluster | Zeilen |
|---|---|
| **15 ✅** | P8-1, P8-2, P8-3, P8-4 (Block A); P8-6, P8-7 (Block B Index); P8-9, P8-10 (Block B UI); P8-11, P8-12, P8-13 (Block B/C Constraints); P8-17 (Budget-Test); P8-25 (C0-Audit); P8-26 (Smoke-Fundament) |
| **10 🟡** | P8-5 (A3 Restdefekt Klammer/Aufzählung); P8-8 (B3 Zweitnutzer-Pass-Through); P8-14, P8-15, P8-16 (C1/C3/C4 Sichtprüfungen am echten Gerät); P8-18, P8-19 (D1 Sichtprüfung 2); P8-20, P8-21 (D2 Behavior-Assertions); P8-22 (Settle-Zeit 5.95 s statt < 3 s, graph.js ALPHA_DECAY — siehe §9.4.6 Befund A); P8-23 (D3 vorbereitet, post-deploy); P8-24 (Knotenklick → Item fehlt im Code — siehe §9.4.6 Befund C) |
| **0 ⬜** | keine mehr |

Drei Zeilen brauchen eine Erläuterung, damit sie nicht falsch gelesen werden:

- **P8-8 🟡 mit Code-Beleg, ohne Live-Pass-Through.** Die ACL-Filterung in `_graph_get`
  ist per Unit-Test gegen einen zweiten Space + gewollte `share_read`-Items verifiziert;
  **ein Smoke gegen die laufende Instanz mit zwei realen OAuth-Tokens** (Nikinger + Fabian
  oder `testnutzer-p7`) **steht aus** — das ist die einzige Lücke zwischen „Code korrekt"
  und „ACL wirklich gehalten". Empfehlung für die nächste Sitzung: ein Smoke mit zwei
  Tokens, zwei Spaces, einem gewollten `share_read`-Item und einem privaten Item, der die
  `nodes`/`edges`-Payload gegen die Erwartung prüft.
- **P8-20/P8-21 🟡 mit Screenshot, ohne explizite Browser-Assertion.** Hover-Dim,
  Klick-öffnet-Item, Drag/Zoom/Pan, Tag-Toggle, >15-Knoten-Cutoff: alle als Code-
  Invarianten da, im D2-Smoke 7/7 als Markup/Payload/Canvas-Pixel geprüft; **einzelne
  Behavior-Assertions (z. B. „Hover dimmt Nicht-Nachbarn auf 15 % Alpha") fehlen** — die
  Screenshots `d2_*` zeigen sie visuell, automatischer Beweis nicht.
- **P8-24 🟡 mit kombiniertem End-to-End-Smoke (Station 6 fehlt).** Der Ritt ist gebaut
  (`phase8_ui_graph/scripts/phase8_e2e_smoke.py`, 5/6 Stationen bestanden), aber die
  sechste Station schlägt fehl, weil der Klick-nach-Item-Pfad im Code fehlt. **Nicht mehr
  „drei Teil-Smokes ohne Ritt", sondern „Ritt da, letzte Station offen"** — siehe §9.4.6
  Befund C.

### §9.4 Restdefekte und offene Entscheidungen

#### §9.4.1 A3 Klammer-/Aufzählungs-Kontext (P8-5)

`mcpserver/tools.py :: _TITLE_NOT_ID_HINT` nennt heute zwei Negativ-Beispiele (Plain-Text
und Tabelle). Die Drittprobe vom 2026-09-01 hat gezeigt: in **Klammer-Kontexten** und
**Aufzählungen** nennt Claude weiterhin die rohe `itm_…`-ID. Drei Optionen, **keine** ist
gewählt:

- (a) Hint um eine dritte Zeile ergänzen („auch nicht in Klammern oder Aufzählungs-Zeilen")
  — hinweis-textuelle Lösung, gleicher Mechanismus wie schon, eine Zeile Code +
  Test-Anpassung.
- (b) Das Rückgabe-Schema von `search_items` ändern: `id` aus dem Default, `title` als
  Anker — berührt den P2-Contract, teurer.
- (c) Den Befund als Modellverhalten dokumentieren — eine dritte Probe nach einer
  Modellvariante wäre billig, eine Entscheidung nicht.

**Das ist eine Nikinger-Entscheidung, keine Claude-Ableitung.** Nikinger hat am
2026-09-01 A3 mit dem bestehenden Defekt auf 🟡 stehengelassen und den Punkt bewusst nach
§9 vererbt, wie P7-24/P7-4 damals — kein Scope-Silentium, ein benannter Punkt mit drei
Optionen.

#### §9.4.2 Item-Link-Picker füllt nur das Frontmatter-Feld (Vormerkung)

Der Link-Picker (`editor.js :: _appendLinkId`, B4) hängt die gewählte `itm_…`-ID an
`links:` an — das ist das **Graph-Kanten-Futter**. Wer heute einen **klickbaren Item-Link**
im Text will, muss die Ziel-ID kennen und `[Text](#item/itm_…)` selbst tippen. Der Picker
suggeriert optisch „ich verlinke", tut das aber nur für den Graphen.

**Nikinger-Auftrag 2026-09-02: nur vormerken.** Naheliegender Fix: `_appendLinkId` um eine
Variante erweitern, die `[<Titel>](#item/<id>)` an der Cursor-Position in
`#editor-textarea` einfügt — kein neuer Endpunkt, der Picker kennt Titel+ID bereits aus
seinem Suchergebnis. **Aktion für die nächste Phase (kein Phase-8-Auftrag mehr).**

#### §9.4.3 Picker-A11y `aria-selected` nie per JS gesetzt (Nebenfund 2026-09-02)

Der `.link-picker-results li`-Selektor hat ein `role="option"`-Markup mit
`aria-selected="true"` als Auswahl-Logik, **aber** `dialogs.js` setzt dieses Attribut nie
per JS. Konsequenz: Maus funktioniert (`:hover`/`:focus`), Tastatur nicht (kein
`ArrowUp`/`ArrowDown`, kein Enter-zur-Auswahl). Im Sweep „Standard überall" vom
2026-09-02 wurde die CSS-Regel auf den neuen Standard gehoben — die Regel ist aber
**toter Code**, bis jemand die JS-Auswahl-Logik nachzieht.

**Vormerkung für eine spätere A11y-Passage.** Bewusst nicht in dieser Phase behoben, weil
die Phase geschlossen wird und der Fix eine eigene Test-Strecke braucht (Tab-/Enter-
Tastaturtest, Screenreader-Probe).

#### §9.4.4 P8-22 + P8-24 — Status nach 200-Knoten-Smoke und kombiniertem E2E-Ritt

**Beide Substanz-Setups sind gebaut** (`phase8_ui_graph/scripts/wegwerf_setup_200knoten.py`
+ `p8_22_smoke.py` für P8-22, `phase8_e2e_smoke.py` für P8-24), beide gegen ihre jeweilige
Wegwerf-Instanz gefahren, beide ehrlich bilanziert (Kriterien werden gesammelt, nicht beim
ersten Fail abgebrochen). Beide werfen drei echte Funde ab, die in §9.4.6/§9.4.7 als benannte
Restdefekte vererbt sind — nicht stillschweigend nach P9 verschoben, sondern offen benannt:

- **P8-22: 4/5 Kriterien erfüllt, 1 ehrlicher Fail (Settle-Zeit).** Messung gegen den
  200-Knoten-Wegwerf (Port 18772, 120 own / 50 shared-write / 30 foreign-read, Ring-Links
  mit Schrittweite 7, Tag-Mix mit drei Sorten für den >15-Riegel):
  - Simulation kommt **5.95 s** zur Ruhe (Budget < 3 s). 351 Ticks in 5.82 s, Frame-p50
    16.7 ms (60 fps, nicht compute-bound). Ursache ist `ALPHA_DECAY 0.985` bis `ALPHA_MIN
    0.005` → 351 Ticks; der Kommentarkopf von `js/graph.js` behauptet „200 Knoten erreichen
    Ruhe in <3s auf einem normalen Browser" — das ist damit widerlegt.
  - Interaktion ohne Hakeln ✅: hover p95 0.4 ms / drag p95 0.3 ms / wheel p95 0.4 ms
    (60-fps-Budget 16.7 ms, weit darunter).
  - Tag-Toggle mit >15-Riegel ✅: `last-200` (200) und `gruppe-NN` (~17) bleiben aus,
    `spitze` (5) liefert 10 Paare.
  - `prefers-reduced-motion` rendert statisch ✅: 0 Animationsframes aus `graph.js`,
    Canvas statisch bebildert, Hash über 600 ms unverändert (170 fremde Frames =
    Playwright-Polling, mit Stack-Trace-Filter korrekt als „nicht die App" aussortiert).
- **P8-24: 5/6 Stationen bestanden, 1 ehrlicher Fail (Knotenklick → Item).** Kombinierter
  Ritt gegen den D2-Wegwerf (Port 18768, default; `--base`/`--root` für jede andere Instanz):
  - Stationen 1-5 ✅ (Login, Uebersicht tabellos, globaler Scope V82-idempotent, Graph
    gezeichnet, Hover dimmt Nicht-Nachbarn von 280 auf 103 voll deckende Knotenpixel).
  - Station 6 ❌: **Knotenklick öffnet das Item nicht.** Befund: `js/graph.js` importiert
    `selectItem` nicht, `onMouseDown`/`onMouseUp` setzen nur Drag/Pan, der
    „Klick → Editor.selectItem"-Pfad existiert im Code nicht. Plan §5 D2 und der
    Phase-Head-D2-Block behaupten ihn beide — die Doku ist überholt.

**Konsequenz für §9.4.6/§9.4.7 (neu, 2026-09-02):** drei Restdefekte wandern aus diesen
Smokes in die Vererbung.

#### §9.4.5 Geerbtes Ledger (P6/P6.5/P7), unverändert offen

| Posten | Herkunft | Stand |
|---|---|---|
| P6-Zeilen 7, 9, 14–17, 23, 25, 29, 30 | P6 | offen, in P8 nicht adressiert |
| P6.5-14 — Nikingers eigene Bewertung der Upload-Ankündigungsdisziplin | 6.5 | strukturell offen, kein Testlauf kann es schließen |
| Glyph-Entscheidung P6 (🟡) und P6.5 (🟡) | P6/6.5 | beide unverändert offen |
| O4 verwaiste Assets · O5 kein EXIF-Strippen · O7 leere Ordner überleben Move | P6 | offen; P8 hat keinen davon angefasst |
| `_trash/`-Räumung | 6.5 | bewusst nicht automatisiert; mittelfristig eigene Lösung nötig |
| V12/V49 Uplink-Datenlimit | P3/P6 | offen seit Phase 3, nie bewertet |
| V64 claude.ai-Verhalten bei `destructiveHint: True` | 6.5 | offen, Client-Verhalten |
| `filename`-Persistenzfrage · `test_authctl.py`-Flake | 6.5 | offen; bei einem roten Lauf **zuerst prüfen, ob es der Flake ist** |
| Funnel-Watchdog / Selbstheilung | P3 | bewusst offene Entscheidung, kein Auftrag |
| `GET /api/v1/overview` ~440–490 ms, alle 20 s gepollt | P6-S | bekannte Kostenstelle, kein Auftrag |
| Kein UI-Rückweg aus geteiltem Space | P6 | „kein Bug, nicht blockierend", bleibt so |
| V79 FastMCP-4 / `2026-07-28`-Revision | P5-C | eigene Mini-Phase, kein Phase-8-Auftrag |
| **Neu in P8:** A3 Klammer/Aufzählung · Item-Link-Picker-Body · Picker-A11y | P8 | siehe §9.4.1–§9.4.3 |
| **Neu in P8 (2026-09-02, aus den 200-Knoten-/E2E-Smokes):** Settle-Zeit (graph.js ALPHA_DECAY) · Foreign-Farbe unerreichbar (`_graph_get` setzt `shared` statt `writable`) · Knotenklick öffnet das Item nicht (graph.js hat keinen `selectItem`-Pfad) | P8 | siehe §9.4.6 (drei Nikinger-Entscheidungen, drei Optionen je Befund) |

**Was P8 ausdrücklich draußen ließ und was dadurch nicht Phase 9 verpflichtet:** FastMCP-4-
Umstieg, `_trash/`-Räumung, Funnel-Watchdog, Body-Volltextsuche in der Web-UI (Q1),
Rechteverwaltung über MCP-Tools, Löschen von Items (F2).

#### §9.4.6 Drei neue Restdefekte aus der Smoke-Sitzung (2026-09-02)

Aus den P8-22- und P8-24-Smokes sind drei echte Lücken aufgetaucht, die nicht in dieser
Session geschlossen wurden (Nikinger-Entscheidung A: „Lücken als benannte Defekte
vererben"). Die Befunde sind im Code verifiziert, mit Datum und Messwerten belegt, mit
drei Optionen zur Auflösung — wie §9.4.1 (A3 Klammer) ist auch dies eine Nikinger-
Entscheidung, keine Claude-Ableitung.

- **A — `graph.js` ALPHA_DECAY: 200 Knoten kommen nicht in < 3 s zur Ruhe (P8-22).**
  Gemessen: 5.95 s sichtbare Ruhe, 351 Ticks in 5.82 s, Frame-p50 16.7 ms. Die Dauer
  folgt allein aus der Abklingkurve `ALPHA_START 1 * ALPHA_DECAY^n < ALPHA_MIN 0.005`,
  nicht aus der Knotenzahl. Drei Optionen:
  - (a) `ALPHA_DECAY` von 0.985 auf z. B. 0.97 (ergibt ~171 Ticks, ~2.85 s) — eine
    Konstante, keine Semantik, aber berührt Plan §5 D2 (gelockt).
  - (b) `ALPHA_MIN` von 0.005 auf 0.02 (schnellere Abbruchbedingung — Bewegung unter
    `ALPHA_MIN` ist ohnehin unter einem Pixel und damit unsichtbar) — auch eine
    Konstante, weniger invasiv.
  - (c) Akzeptieren und Plan-Kommentar korrigieren: „< 5.85 s" statt „< 3 s" — ehrlich,
    aber zieht die Akzeptanzlinie nach unten.

- **B — `_graph_get` setzt `shared` statt `writable` (P8-15, Nebenfund der Smoke-Sitzung).**
  `webui/api.py` Zeile 677: `"shared": i.space != session.space` — und reicht das an
  `state.js :: spaceCategory({ own, writable })` weiter, wo `writable` der Parameter
  ist. Damit ist jeder fremde Knoten „shared" (türkis); die dritte C3-Farbe
  (`--space-foreign`, grau) ist im Graphen strukturell unerreichbar, obwohl die Legende
  sie anzeigt. Der 200-Knoten-Wegwerf hat `beta` als `--write` und `gamma` als `--read`
  und damit die zwei fremden Kategorien bewusst differenziert — der Graph zeigt beide
  einheitlich türkis. Drei Optionen:
  - (a) `api.py :: _graph_get` rechnet `writable` selbst aus (analog zu
    `webui/serializers.py :: overview_row_to_json`'s `shared`-Feld, das bereits
    `space`/`own`/`writable` differenziert).
  - (b) Neue ACL-Pipeline analog zu `permissions.SharePolicy.can_write_item_as_human`
    — der saubere Weg, aber teurer (P5-B-Disziplin halten: genau ein Import aus
    `mcpserver/` in `webui/`).
  - (c) Als bewussten Modellierungs-Befund dokumentieren und die Legende auf zwei
    Farben reduzieren (own / nicht-own) — semantisch: „dein Space" vs. „fremd", die
    Schreib-/Lese-Unterscheidung lebt auf der Item-Detailseite, nicht im Graphen.

- **C — Knotenklick öffnet das Item nicht (P8-20/P8-24).** `js/graph.js` importiert
  `selectItem` nicht, `onMouseDown`/`onMouseUp` setzen nur Drag/Pan zurück, der
  „Klick → Editor.selectItem"-Pfad existiert im Code nicht. Plan §5 D2 und der
  Phase-Head-D2-Block behaupten ihn beide — die Doku ist überholt, der Code fehlt.
  Drei Optionen:
  - (a) `onMouseUp` ergänzen: wenn `dragNode === null` und Klick-Distanz < 4 Pixel,
    `hitTest` auf `e`-Koordinaten + `selectItem(hit.id)`. ~5 Zeilen Produktionscode.
  - (b) Neuer `click`-Event-Handler auf dem Canvas (sauberer getrennt von `mousedown`/
    `mouseup`, aber zwei Event-Listener mehr im Hot Path).
  - (c) Doku an Code anpassen: „Klick öffnet das Item nicht (Plan §5 D2 abweichend
    vom Code)" — kein Code-Fix, ehrliche Verkleinerung des Funktionsumfangs.

**Das sind drei Nikinger-Entscheidungen, keine Claude-Ableitung.** Nikinger kann pro
Befund eine der drei Optionen wählen, die Befunde in eine P9-Planung verschieben, oder
den Code-Fix jeweils selbst anordnen (mit oder ohne opencode-Advisor).

#### §9.4.7 Phase-Status Glyphe ✅ vs. 🟡

„✅ heißt live-verifiziert, nicht gebaut" — die Projekt-Statusregel. Die aktuelle Bilanz
ist 15 ✅ · 10 🟡 · 0 ⬜. **Der Sprung auf ✅ ist eine Nikinger-Entscheidung nach
Live-Deploy + Sichtprüfung am echten Gerät** (P8-23, P8-14/15/16/18/19). Vor dem Sprung
steht mindestens Sichtprüfung 2 (Übersicht + Graph) und Sichtprüfung 3 (C4+C5 Glass +
Selection) auf dem Programm; beide Screenshots sind da, der formale Lauf am echten
Gerät gegen den dann deployten v3.0-Build fehlt.

**Optional:** wenn der Nikinger die drei 🟡-Restdefekte aus §9.4.1–§9.4.3 UND die drei
neuen aus §9.4.6 **vor** dem Sprung noch schließen will, kann die Bilanz vor dem
✅-Sprung adjustiert werden — diese Liste ist die Buchführung, nicht die Schwelle.
Achtung: die sechs optionalen Schließungen liegen in zwei verschiedenen Phasen — die drei
aus §9.4.6 sind Phase-8-Restdefekte, die drei aus §9.4.1–§9.4.3 sind teils Phase-7-
Restdefekte (A3, Item-Picker) und teils Phase-8-Nebenfunde (A11y).

### §9.5 `[VERIFY]`-Bilanz (V81–V92 + V93, V94)

| # | Frage | Status |
|---|---|---|
| V81 | `pytest -q` Ausgangsstand real 904? | ✅ geschlossen — real 904 in Step 0.1; Endstand **958** über alle Phase-8-Commits zusammen |
| V82 | Alle in diesem Plan zitierten `Datei:Zeile`-Anker vor jedem Edit prüfen | ✅ gehalten — Disziplin in jeder Block-Session |
| V83 | IBM-Plex-Release: variable TTFs für Sans (wght-Achse)? | ✅ geschlossen in C1 — Plex Sans Variable v0.2.0 gepinnt |
| V84 | `ui_budget.py` Gesamtbudget nach Fonts + Sprite + `graph.js` | ✅ geschlossen in D3 — 5/5 grün, Endstand **124.2/250 KB** |
| V85 | `prefers-reduced-transparency`-Support in real genutzten Browsern; Fallback unabhängig via `@supports` | ✅ strukturell geschlossen in C4 (Media-Query + `@supports`); **empirischer Browser-Lauf mit umgeschaltetem UA steht aus (P8-16 🟡)** |
| V86 | Wie die P7-ID-Suche an der API heißt (Query-Parameter von `_items_get`) | ✅ geschlossen in B4 — wiederverwendet, nicht erfunden |
| V87 | Felder von `IndexStats` (für A2s stdout-JSON) | ✅ geschlossen in A2 |
| V88 | Exakter CSS-Klassenname der ausgewählten Listenzeile | ✅ geschlossen in C4 (Vormerkungs-Sweep hat präzisiert: `.list__row[aria-current="true"]` + `.list__rows > li.list__row--selected`) |
| V89 | Wie Handler an die `session_id` kommen (`sessions.py :: SessionManager`, Cookie `COOKIE_NAME`) | ✅ geschlossen in A1 |
| V90 | `_measure_latency()` in `ui_budget.py` um `GET /api/v1/graph` ergänzen | **offen, niedrige Priorität** — Entscheidung des Ausführenden; in B3 nicht umgesetzt (informativ, kein Budget) |
| V91 | `tags`/`folder`/`space`/`type`/`status` in Summary-Daten für `_graph_get` | ✅ geschlossen in B3 |
| V92 | Existieren die §4.2-Lucide-Icon-Namen in der gepinnten Version? | ✅ geschlossen in C2 — Lucide 1.38.0, SHA-256 d28944cf… |
| V93 | Welcher opencode-Weg liefert Browser-Steuerung | ✅ geschlossen in Step 0.7 — Playwright-MCP |
| V94 | Hat opencode/M3 brauchbare Web-Recherche für C0? | ✅ geschlossen in Step 0.7 — websearch-MCP nachgerüstet |

**Zwei Marker offen, keiner ein Rest-Risiko dieser Phase:** V90 (informativ, niedrige
Priorität — Latenz-Messung am Graph-Endpunkt) und V79 (eigene Mini-Phase per P5-C,
weiterhin unberührt).

### §9.6 P1-Contract — achte Öffnung geschlossen

| Öffnung | Was | Stand |
|---|---|---|
| **achte** | `storage/linkscan.py` (neu, `ITEM_REF_RE`, `extract_item_refs(body)`) · `storage/index.py` (`INDEX_SCHEMA_VERSION = 3`, `item_links`-Tabelle + Index auf `dst_id`, `replace_item_links()`, `all_links()`, `row_from_file` ↳ `body_refs`, `rebuild_index` populiert, `delete_item` räumt src-Zeilen) · `storage/store.py` (`_replace_links_for_item()`, `Store.links_all()`, alle 6 Schreibpfade via `_write_item_file`, Drift-Repair) | **geschlossen mit diesem §9** (2026-09-02) |

Schließung folgt im selben Commit wie §9: datierte Notiz in
`phase1_storage/CLAUDE.md` §„Geerbte Contracts" mit dem Eintrag „Achte Öffnung
geschlossen mit Phase-8-Step-Z". Hard Rule 2 ist gehalten: `rebuild_index()` rekonstruiert
`item_links` vollständig aus den `.md`-Dateien (P8-7 ✅, 13 B2-Index-Tests). Die P6-D-
Disziplin `test_characterization.py` byte-identisch grün ist über die gesamte Phase
nachgehalten — bestätigt in jeder Block-Session (P8-11 ✅).

**Keine neunte Öffnung angekündigt.** Jede Phase-9-Arbeit an `storage/` braucht eine neue,
benannte Öffnung mit eigenem Absatz in `phase1_storage/CLAUDE.md`; kein stiller Anbau.

### §9.7 Geänderte Arbeitsweise ab Phase 8 (Rückschau)

Die in `PHASE7_CLOSEOUT_HANDOVER.md` §7 angekündigte Teilung **Claude Code plant, opencode
(M3) führt aus** hat in Phase 8 operativ gehalten:

- **Planungstiefe.** Der Plan wurde gegen `main@8f46745` geschrieben, alle zwölf
  Nikinger-Fragen N1–N12 in §0.1 vom Nikinger gelockt, Entscheidungen P8-A–P8-Q im Plan
  verbindlich. Anker `Datei:Zeile` haben sich in jeder Block-Session als hilfreich
  erwiesen — Funktionsnamen tragen, Zeilennummern driften (bestätigt in Block A und
  Block C).
- **Advisor-Ersatz.** Die Selbstprüf-Checkliste §0.6 (pytest, Tabu-Diff, Fehlerpfad,
  Doku-Update, ui_budget) wurde in jeder Block-Session eingehalten. Echter Fund-Reichtum
  pro Block (Selbstprüfung + Lesepfad-Auffälligkeiten): **Block A 5** (Anker-Drift,
  Auth-Anker, Body-Edge-Drift), **Block B 2** (`ITEM_REF_RE`-Bootstrap-Reihenfolge,
  `_PATCH_FIELDS`-Whitelist für `reauth_grant`), **Block C 4** (Border-Layout-Shift vor
  Vormerkung 3, Chevron-Skalierung in `.field .input`-Subkontext,
  `select.input:focus`-Asymmetrie, undefinierter `--accent-text`-Token), **Block D 3**
  (Counter-Chip-Klick-Regression, `aria-current`-Idempotenz bei Home-im-globalen-Scope,
  Empty-Hint-Wait-Funktion). **Bilanz: ~14 echte Funde, davon 0 Blocker** — substanziell
  weniger als die P7-Bilanz von 11 Funden mit 4 Blockern (ungeschützter
  `GET .../members`, eingefrorenes Re-Auth gegen den falschen Space, nicht eingefrorenes
  Batch-Ziel, `ValidationError` mitten im Space-Entfernen-Durchlauf). Die Selbstprüf-
  Disziplin trägt; der Advisor war ein Sicherheitsnetz für höhere Risiken (Auth, ACL,
  Migration), weniger für Layout/CSS.
- **Playwright als primäre Browser-Quelle.** Opencode mit Playwright-MCP hat sich als
  deutlich direkter erwiesen als der `claude-in-chrome`-Pfad in P5/P6. (W)-Zeilen der
  Abnahmematrix wurden in B4, C1+C2 (Sichtprüfung 1), C3, C4+C5 (Sichtprüfung 3), D1,
  D2, D3 (Sichtprüfung 2) gegen jeweils eigene Wegwerf-Instanzen gefahren. Standing-
  Permission-Muster hat sich bewährt: Port-Range pro Block, File-Keyring, eigenes venv
  (`~/.claude-code-tools/`).
- **Konventionen.** Die Selection/Choice-Konvention v3 (Phase-Head, vier-gliedrige
  Taxonomie) ist die erste Konvention, die **während** einer Phase entstand und nicht im
  Plan stand — Vormerkung 1 vom 2026-09-01 hat sie ausgelöst. Empfehlung für Phase 9:
  solche während der Phase entstehenden Konventionen am Ende in
  `docs/DOC_LAYERS_CONVENTION.md` überführen oder als Phase-9-Arbeitsanweisung
  weiterführen (im Phase-Head dokumentiert).

**Was die nächste Planung mitnimmt:** die offene V90-Entscheidung, die drei benannten
Restdefekte (§9.4.1–§9.4.3), die zwei noch zu fahrenden Substanz-Setups (§9.4.4), das
geerbte P6/P6.5/P7-Ledger (§9.4.5), die Glyph-Entscheidung ✅/🟡 nach Live-Deploy +
Sichtprüfung.

### §9.8 Was dieser Closeout nicht enthält

Keine Implementierungsdetails, die bereits im Code, in den Tests oder im Phase-Head
stehen. Wer die volle Herleitung eines einzelnen Bau-Schritts braucht — die Block-A/B/C/D-
Sitzungsblöcke, die Anker-Drift-Episoden, die C0-Research-Tabelle (35 Findings), die
Glass-Fallback-Diskussion, die Selection/Choice-Konvention-Entstehung, die Outline-
Nachschärfungen, die Vormerkungs-Sweep-Funde — findet sie in
`phase8_ui_graph/SESSIONS_ARCHIVE.md`, verbatim, newest-first (~190 KB, fünfundzwanzig
Einträge nach siebzehnter Rotation).

Auch nicht hier: ein separates `PHASE8_CLOSEOUT_HANDOVER.md`. Diese Phase folgt P8-N
(ein Dokument pro Phase); wer die Vorgelende-Struktur gewohnt ist, findet die äquivalente
Form hier in §9.
