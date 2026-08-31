---
status: live
purpose: Archiv älterer Session-Blöcke aus phase8_ui_graph/CLAUDE.md — newest-first, verbatim per Rotationsregel
read-when: nur wenn der aktuelle Session-Block im Phase-Head nicht reicht und Verlauf gebraucht wird
detail: L3
up: CLAUDE.md
updated: 2026-08-31 (erster Eintrag: 2026-08-28 Block-A-Startblock nach SESSIONS_ARCHIVE rotiert, da die zweite Session mit A1-Client + Smoke + N=14-Batch-Test den aktuellen Head-Block bildet)
---

# SESSIONS_ARCHIVE.md — Phase 8

Noch leer — der Phase-Head trägt bisher genau einen (aktuellen) Session-Block. Der erste Eintrag
hier entsteht bei der ersten Rotation (`scripts/rotate_session_block.sh phase8_ui_graph`).
## Session stopped — 2026-08-28 (Block A gestartet: A1-Backend gebaut, 912 Tests grün, JS-Client ausstehend)

**Auftrag:** A1 Reauth-Grant (P8-A, schließt P7-24) — der zweite Erbpost aus dem P7-Handover §4.
Plan detailliert genug (Option b), Anker vor jedem Edit gegen den echten Code verifiziert
(V82): `webui/reauth.py:20` (`verify_reauth()`-Signatur), `webui/shares.py:55/96` (zwei
`require_*_reauth()`), `webui/api.py:156/204/218/681/992+` (`_PATCH_FIELDS`/`api_routes()`/
`_require_session`/Whitelist-Check/Route-Liste), `mcpserver/app.py:211` (kein Diff nötig —
Grant-Store wird in `api_routes()` intern gebaut, neben `LoginThrottle`).

**Ergebnis A1-Backend (Commit 1 von vermutlich 2 für A1):**
- `webui/reauth.py` — `ReauthGrant`-`@dataclass` (session_id, expires_at) +
  `ReauthGrantStore`-Klasse (in-memory `dict[str, ReauthGrant]`, `issue()`/`check()` mit
  required `now: float` für deterministische Tests, lazy purge, nie persistiert, stirbt mit
  Prozess). Konstante `REAUTH_GRANT_TTL_S = 90.0`.
- `webui/shares.py` — beide `require_*_reauth()` akzeptieren `body["reauth_grant"]` ZUERST
  (vor `password`/`totp`), bei gültigem Grant sofortiger Return. Bindung an
  `session.session_hash` (nicht Klartext-Cookie — der existiert nur im Browser, P5-K; Hash
  ist die einzige serverseitig mögliche Session-Identität). **Wichtige Korrektur gegen den
  Plan-Text:** der Plan-Beispielcode schrieb `session.id`, das gibt es auf `SessionRow` nicht
  (`authserver/models.py:104-118` — `session_hash`/`space`/`csrf_hash`/Zeitstempel). Wenn der
  Plan `session_id` meinte, dann den Hash.
- `webui/api.py` — `_PATCH_FIELDS` um `"reauth_grant"` erweitert; `api_routes()` baut intern
  `ReauthGrantStore()` neben dem vorhandenen `LoginThrottle` (kein neuer Parameter, kein
  `mcpserver/app.py`-Diff); `require_share_reauth()`/`require_space_reauth()`-Aufrufe (drei
  Stellen) reichen `grant_store` durch; Filter im `_items_patch` (vorher: `"version",
  "password", "totp", "space"`) bekommt `"reauth_grant"` dazu (Hard Rule 1: ein langlebiges
  Token darf NIE als Frontmatter-Feld landen); neuer Handler `_reauth_post()` + Route
  `POST /api/v1/reauth`. **Throttle-Prüfung explizit vorgezogen** (`throttle.check()` vor
  `verify_reauth()`) — sonst hätte `verify_reauth()` die Sperre in ein `False` geschluckt und
  der Client hätte nicht zwischen „falsch" (403) und „Space gesperrt" (429) unterscheiden
  können. Spiegelung des Musters aus `routes_auth.py:59-67`. Fehlschlag-Pfad: 403 mit
  `reauth_required`, gedrosselt: 429 mit `rate_limited`, beides gemäß `errors.py`-Konvention.
- `phase5_ui/tests/test_reauth_grant.py` (neu, 8 Tests, 1:1 zu Plan §A1): korrekte Credentials
  → 200+Token; falscher TOTP → 403 mit Throttle-Zählung, sechster Versuch → 429; **P7-24-
  Kernfall** (drei rechteerweiternde PATCHes mit einem Grant); abgelaufenes Grant (clock
  +120s) → 403; Grant einer fremden Session → 403; derselbe TOTP-Code zweimal über
  `/api/v1/reauth` → zweiter 403 (Anti-Replay intakt); `reauth_grant` als Feld passiert die
  `_PATCH_FIELDS`-Whitelist, beliebiges anderes Feld weiterhin 422; ohne Session → 401.

**Plan-Abweichungen, dokumentiert (nicht stillschweigend):**
1. `session.id` → `session.session_hash`. `SessionRow` hat kein `id`-Attribut; der Plan-
   Beispielcode war ungenau gegen das echte Modell.
2. Throttle-Check in `_reauth_post` VOR `verify_reauth()` (statt nur durch `verify_reauth()`).
   Plan-Wortlaut „gedrosselt → 429" hätte bei nur-innen-Prüfung als 403 geliefert; jetzt ist
   die Semantik echt (429 unterscheidbar von 403). Konvention `routes_auth.py:59-67`.
3. Grant-Store als interner `api_routes()`-State statt Parameter. Plan-Text „hängt an der App
   neben der LoginThrottle-Instanz (App-Factory, V82)" — die App-Factory IST `api_routes()`
   in dieser Code-Struktur (`create_app()` ruft `api_routes(...)` einmal auf, ohne
   App-State-Pattern), die saubere Implementierung ist lokal-in-`api_routes()`. Vermeidet
   einen `mcpserver/app.py`-Diff (Tabu-Linie Phase-5/6 hält).

**Verifiziert:** `pytest -q` → **912 passed** (904 + 8 neu, exakt +8), keine Regression. Tabu-
Diff auf `phase4_auth/` + `mcpserver/{tools,permissions,server}.py` + `security.py` + `storage/`
außerhalb der P8-M-Öffnung: **leer** (Plan §0.4 erfüllt — die P8-M-Öffnung gilt erst ab Block B).
Live-Dienst nicht angefasst (kein Server-Code deployed, nur Bibliothekscode auf dem
Wegwerf-Pfad).

**Verbleibend für A1 (Commit 2):** Client-Änderung in `webui/static/js/dialogs.js ::
runBatchMove()` — vor Runde 1 einmal `POST /api/v1/reauth`, dann `{reauth_grant: token}` statt
`{password, totp}` an `moveSelectedItems()`. `list.js :: moveSelectedItems()` selbst bleibt
unangetastet (Body-`Object.assign({version, folder}, credentials || {})` setzt das Grant-Feld
korrekt). Browser-Smoke gegen eine Wegwerf-Instanz (P8-26-Pattern: drei Items mit einem Grant
verschieben, danach ein 7. Tab-Smoke gegen den Live-Dienst, dass der neue Pfad in der
laufenden Instanz angekommen ist). Erst danach A1 in der Abnahmematrix P8-4 als „gebaut"
markierbar — Live-Verifikation bleibt Nikingers Handgriff.

**Nächster Schritt:** A1-Client (Commit 2) in derselben Sitzung, dann A2 `remove-space`-
Reindex (Commit 3). Block A insgesamt drei Commits.

**Stand:** Fundament-Session läuft, Claude Code + Nikinger, interaktiv.

- 0.1 `pytest -q` → **904 passed**, bestätigt V81 (Erwartung aus der Planung war exakt 904).
- 0.2 Verifikationsdurchlauf:
  - (a) Stichprobe P7-Handover §4 gegen Code — **beide grep-prüfbaren Punkte bestätigt**:
    `list.js :: moveSelectedItems()` reicht dasselbe `credentials`-Objekt an jedes sequenzielle
    `PATCH` durch (Zeile 240/246); `spacectl.py :: _cmd_remove_space()` ruft `remove_space_dir()`
    aber nirgends `rebuild_index()` (Zeile 170–195). P7-4 ist eine Verhaltensbehauptung, nicht
    grep-prüfbar — unverändert offen für die A3-Zweitprobe.
  - (b) `up:`/`down:`-Linkauflösung über alle L1-Cards: **ein** unaufgelöster Link, erwartet —
    `docs/concepts/phase8_ui_graph_plan.md` zeigt auf `phase8_ui_graph/CLAUDE.md`, das erst in
    diesem Schritt entsteht.
  - (c) INDEX-Abdeckung: alle lebenden `.md` haben eine Zeile; die drei `phase6_shares/tests/golden/*.md`
    sind Test-Fixtures, keine lebenden Dokumente — bewusst ohne Zeile.
  - (d) Softcap-Scan: zwei Übergrößen bestätigt (`phase6_shares/CLAUDE.md` 41.032 B,
    `phase5_ui/CLAUDE.md` 40.957 B) — beide über der 40.000-B-Schwelle (dezimales KB, wie in der
    bestehenden `phase6_shares`-Notiz verwendet).
- 0.3 P8-P ausgeführt: `phase5_ui/CLAUDE.md`s INDEX-Zeile bekam dieselbe benannte Ausnahme-Notiz
  wie `phase6_shares/CLAUDE.md` (geschlossene Phase, ein Abschluss-Block, Rotation bricht mit
  `exit 2`); dabei zwei stale Größenangaben korrigiert (`~34KB`→`~41KB` bei phase5_ui,
  `~44KB`→`~41KB` bei phase6_shares — beide waren nie nachgemessen worden).
- 0.4 `AGENTS.md` entfernt (`git rm`), zugehörige INDEX-Zeile raus — Freigabe stand bereits in
  der INDEX-Zeile selbst (P7-Handover §7.2).
- 0.5 Dieses Skelett + `SESSIONS_ARCHIVE.md` angelegt.

- 0.6 **opencode installiert und Regeldatei-Verhalten verifiziert.** `npm install -g
  opencode-ai` (Nikinger-Handgriff), Ergebnis `opencode-ai@1.18.25`. Ein `postinstall`-Warnhinweis
  (`allow-scripts` blockierte `postinstall.mjs`) erwies sich als folgenlos — das Plattform-Binary
  kommt über ein separates optionales npm-Paket, nicht über das Skript; `opencode --version` /
  `--help` funktionieren sofort. Provider-Auth vom Nikinger selbst gesetzt (Minimax-Token-Plan,
  `opencode auth list` zeigt `MiniMax (minimax.io)`, Modell `minimax/MiniMax-M3` verfügbar).
  **Kontrollfrage statt Annahme** (Plan-Vorgabe): `opencode run --model minimax/MiniMax-M3` mit
  der Frage nach dem Nikinger-Codenamen + Hard Rule 6 — Antwort korrekt **„Nikinger"** + Hard
  Rule 6 wortgetreu zitiert. `CLAUDE.md` wird gelesen, keine Verdeckung mehr durch `AGENTS.md`
  (0.4 hat es entfernt).
- 0.7 **Fähigkeits-Parität hergestellt, V93/V94 beantwortet:**
  - **V93 (Browser-Steuerung):** `opencode mcp add playwright -- npx @playwright/mcp@latest`
    (Syntax: Kommando nach `--`, nicht per Prompt-Dialog) — steht in
    `~/.config/opencode/opencode.jsonc` (**global**, nicht projektlokal — für dieses
    Ein-Projekt-Setup ohne praktischen Unterschied, aber notiert für den Fall eines zweiten
    opencode-Projekts). `opencode mcp list` zeigt `playwright — connected`. 30 `playwright_*`-
    Tools stehen der laufenden Instanz zur Verfügung (per Tool-Auflistung bestätigt) — Pendant zu
    `claude-in-chrome` gefunden.
  - **V94 (Web-Recherche):** ursprünglich nein (nur `webfetch`, kein Suchwerkzeug) — **noch in
    dieser Sitzung nachgerüstet:** `opencode mcp add websearch -- npx -y
    @zhafron/mcp-web-search` (MIT, kein API-Key nötig — DuckDuckGo/Bing/SearXNG mit
    automatischem Fallback + URL-Extraktion, `github.com/tickernelz/mcp-web-search`, kein
    `pre-`/`postinstall`-Skript im Paket, 366 wöchentliche Downloads geprüft vor dem Hinzufügen).
    Live-Probe bestanden: Suche nach „IBM Plex Sans variable font github release" lieferte
    korrekt `github.com/IBM/plex/releases` als Top-Treffer — direkt für V83 (C1) brauchbar.
    **V94 damit: ja**, C0 läuft komplett unter opencode/M3, keine Claude-Code-Zuarbeit mehr
    nötig. Beide MCP-Einträge (`playwright`, `websearch`) liegen in derselben globalen
    `~/.config/opencode/opencode.jsonc`.
- 0.8 **Smoke-Test bestanden (P8-26).** Wegwerf-Branch `phase8-step0-smoke-test`, drei Proben
  in einem opencode-Lauf: (1) Testdatei angelegt — bestanden; (2) `pytest -q
  phase1_storage/tests/test_models.py` — **4 passed**, kein `SHAREFYX_*`/`SFX_*`-Env gesetzt
  (Session-`env` vor und nach dem Lauf geprüft, sauber); (3) Playwright-Navigation gegen eine
  echte Wegwerf-Instanz (eigener Port `18765`, eigenes `tmp`-`SPACE_DATA_ROOT`, eigene
  `SPACE_AUTH_DB`) — `GET /ui/login` korrekt mit Titel/Überschrift „Anmelden" gelesen.
  **Ein Betriebsfehler dabei, sofort korrigiert:** der erste Versuch ließ `SPACE_PORT`
  unspezifiziert, band an den Default-Port `8765` — dort läuft der **echte** `sharefyx-mcp.service`
  (Live-Instanz, pid 999) — Bindeversuch scheiterte mit `EADDRINUSE`, der Prozess beendete sich
  selbst, kein Schreibzugriff erfolgte. Der folgende `curl /health` traf dadurch tatsächlich den
  Live-Dienst — rein lesend, keine andere Wirkung als ein manueller Health-Check. Wiederholt mit
  `SPACE_PORT=18765`, danach sauber gegen die eigene Instanz verifiziert (`uptime_s:1`).
  Wegwerf-Instanz per PID beendet, Live-Dienst per zweitem `/health`-Aufruf als unverändert
  bestätigt (`uptime_s` durchgehend steigend, kein Neustart). Branch + Testdatei +
  `.playwright-mcp/`-Laufzeitordner nach dem Test verworfen (`git branch -D`, `rm`);
  `.playwright-mcp/` zusätzlich in `.gitignore` aufgenommen (künftige opencode-Läufe in diesem
  Projektverzeichnis legen ihn sonst wieder an).

**Verifiziert:** `git status` nach Cleanup zeigt nur den beabsichtigten Diff (`.gitignore`,
Phase-Head, Skelett, INDEX/ROADMAP) — Wegwerf-Branch weg, Wegwerf-Instanz-Prozess weg, Live-Dienst
lief während der gesamten Sitzung ohne Unterbrechung (`systemctl is-active` durchgehend `active`).

**Harnesswechsel freigegeben:** ab Block A führt opencode/M3 aus, kein Advisor-Call
(P8-L/N12) — Ersatzmechanismen sind die Selbstprüf-Checkliste (Plan §0.6) und die zwei
Nikinger-Sichtprüfpunkte (Plan §8).

**Offen für die nächste Sitzung:** Block A starten (A1 Reauth-Grant zuerst, P8-A) — unter
opencode/M3, gegen `docs/concepts/phase8_ui_graph_plan.md` §2. Vor jedem Edit die zitierten
Datei:Zeile-Anker neu prüfen (V82, driftet erfahrungsgemäß um wenige Zeilen).

