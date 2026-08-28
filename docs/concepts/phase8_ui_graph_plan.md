---
status: snapshot
purpose: ausführungsreifer P8-Plan — UI-Neuanstrich (v3), Verknüpfungs-Graph, drei P7-Erbposten; geschrieben für einen ausführenden Agenten (opencode/M3), der nicht mitgeplant hat
read-when: vor und während der Ausführung von Phase 8 — Abschnitt §0 zuerst, dann den jeweiligen Step
detail: L2 (📕-Snapshot, vom 40KB-Softcap ausgenommen)
up: ../../ROADMAP.md
down:
  - ./PHASE7_CLOSEOUT_HANDOVER.md            # Herkunft der Erbposten P7-24 / remove-space / P7-4
  - ../../phase8_ui_graph/CLAUDE.md          # Phase-Head (entsteht in Step 0.5)
updated: 2026-08-28 (Nachtrag noch in der Planungssession: Step 0 als Fundament-Session Claude Code + Nikinger, C0 Anti-AI-Pattern-Research neu, P8-P gelockt, P8-25/26 + V93/V94) | 2026-08-28 (initial, Planungssession Claude Code Opus, N1–N12 vom Nikinger gelockt)
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
3. Batch: 3 rechteerweiternde PATCHes mit demselben Grant → alle 200 (der P7-24-Kernfall).
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

## §9 Closeout (wird in Step Z gefüllt — P8-N: kein separates Handover-Dokument)

*reserviert*
