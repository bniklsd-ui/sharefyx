---
status: live
purpose: Phase-Head MCP-Server — Scope, harte Regeln, gelockte Entscheidungen, Modulstatus, aktueller Session-Handover
read-when: Arbeiten in phase2_mcp/ — zuerst lesen, zusammen mit dem neuesten Session-stopped-Block
detail: L2
up: ../CLAUDE.md
down:
  - ../docs/concepts/phase2_mcp_plan.md          # voller Plan, Entscheidungen P2-A–P2-N, Steps 0–7
  - ../docs/concepts/PHASE1_CLOSEOUT_HANDOVER.md # Herkunft der Entscheidungen D1–D6
  - SESSIONS_ARCHIVE.md                          # ältere Session-Blöcke, newest-first
updated: 2026-07-26 (live-verifiziert)
---
# CLAUDE.md — Phase 2: MCP-Server (`phase2_mcp/`)

> **Claude kann lesen und schreiben — lokal, ohne Tunnel.** Ein dünner Adapter über dem in P1
> bewiesenen Storage-Kern: Transport (Streamable HTTP), Identität (Token → Space), Autorisierung
> (eigener Space schreibbar, fremde read-only).
> **Quelle der Wahrheit ist der Code, nicht dieses Dokument.**
> Vollständiges Design + alle 14 gelockten Entscheidungen (P2-A–P2-N) + Steps 0–7:
> `../docs/concepts/phase2_mcp_plan.md`.

## Mission (zuerst lesen)

Der eigentliche Härtetest der Phase ist nicht MCP, sondern **Rule 4**: ein Codepfad, über den
ein fremder Space beschrieben werden kann, existiert nach dieser Phase nicht — auch nicht
versehentlich, auch nicht über `get()`. Zwei gleichzeitige Requests mit zwei verschiedenen
Tokens müssen zwei verschiedene Spaces sehen; wenn dieser Test fällt, ist es ein
Cross-Space-Leak, kein Testproblem.

## Bauprinzip (Projekt-Kernprinzip)

„Der Server ist dumm." **Phase 2 enthält KEINE AI.** Die Tools reichen Store-Ergebnisse durch,
formatieren sie token-sparsam und entscheiden über Rechte. Mehr nicht. Wer hier ein LLM
einbauen will → **stop**.

## Scope

- **DRIN:** `fastmcp` über Streamable HTTP `[VERIFY]`, Token→Space-Auflösung, sechs Tools
  (`list_spaces`, `search_items`, `get_item`, `create_item`, `update_item`, `append_to_item`),
  `<untrusted_content>`-Wrapping fremder Bodies + Snippets, Token-Budget-Disziplin im Listing,
  `/health`.
- **DRAUSSEN:** Löschen (`status: archived` reicht), MCP Resources, MCP Prompts, OAuth,
  öffentliche Erreichbarkeit/Tunnel (P3), SQL-Filterung in `Store.search()` (D6, zurückgestellt).

## Harte Regeln (nicht verhandelbar)

- Alle Hard Rules aus Root-`CLAUDE.md` gelten unverändert — insbesondere: kein Secret in einer
  Datei (Tokens nur als sha256-Hash im Keyring, Service `nikinger-space`), kein Last-Write-Wins,
  kein offener Port am Router, Logging → stderr, stdout nur maschinenlesbares JSON.
- **Rule 4 ist architektonisch, nicht per `if`.** `create_item`/`update_item`/`append_to_item`
  haben keinen `space`-Parameter; der Ziel-Space ist immer der des Principals (P2-G).
- **Auth fail-closed.** Kein/unbekanntes Token → HTTP 401 ohne Detail, nie ein Tool-Fehler, nie
  unterscheidbar von „falsches Token" (P2-N).
- **`stateless_http=True` ab Tag 1** — Sicherheitsbedingung, keine Skalierungsoption (P2-B, §8
  Risiko 1).
- **Token nie im Log.** Uvicorn-Access-Log aus, Scrubbing-Filter auf jedem verbleibenden Logger.
- **Rotationsregel ab Tag 1.** Dieser Head trägt **genau einen** Session-Block. Beim Anlegen
  eines neuen wandert der bisherige **verbatim** nach `SESSIONS_ARCHIVE.md`, newest-first —
  Durchführung über `scripts/rotate_session_block.sh phase2_mcp`, nie von Hand.
- **Commit ⇒ Note-Update, im selben Commit** (Hard Rule 8): Modul-Tabelle unten + Session-Block.

## Die 14 Entscheidungen (P2-A – P2-N) — Kurzform (Details: Plan §0.4)

Bibliothek `fastmcp>=3.4,<3.5` (A) · Protokoll 2025-11-25, `stateless_http=True` (B) · Starlette-
Wurzel mit `Mount("/mcp")` (C) · Token im Pfad, Auflösung einmal pro Request (D) · Keyring
speichert nur Hashes (E) · `SpaceResolver`/`Permissions` getrennte Seams, beliebig viele Spaces
(F) · Schreib-Tools ohne `space`-Parameter (G) · `<untrusted_content>` mit Escaping (H) ·
kompaktes JSON / Dateitext als Ergebnisformate (I) · Token-Budget `limit=20`/`max=100` (J) ·
Archivieren nur über `update_item(status="archived")`, kein siebtes Tool (K) · drei einmalige
P1-Contract-Erweiterungen (L, Step 2) · OAuth bleibt hinter P3, Seam wird gebaut (M) ·
Fehlerabbildung mit handlungsfähigem Text (N).

## Modul-Status

| # | Modul | Step | Status | Tests |
|---|---|---|---|---|
| 1 | Haushalt, Verifikationsdurchlauf, Rotationsregel operationalisiert | 0 | ✅ | 0 (kein Feature-Code) |
| 2 | Paketgerüst `phase2_mcp/`, `mcpserver/config.py` | 1 | ✅ | 3 |
| 3 | P1-Contract-Erweiterungen (`space_of`, `repair_drift`, Statusvalidierung) | 2 | ✅ | 8 (in `phase1_storage/tests/`) |
| 4 | `credentials.py`, `scripts/issue_token.py` | 3 | ✅ (echter Keyring-Roundtrip vom Nikinger bestätigt) | 6 |
| 5 | `auth.py`, `permissions.py`, `context.py`, `asgi.py`, `logging_setup.py` | 4 | ✅ | 14 |
| 6 | `server.py`, `app.py`, `scripts/serve.py` | 5 | ✅ | 8 (`test_app.py`) |
| 7 | `tools.py` (die sechs Tools) | 6 | ✅ | 23 (`test_tools.py`) |
| 8 | `scripts/mcp_smoke.py`, Runbook, Größenmessung | 7 | ✅ **live-verifiziert** | 3 (`test_mcp_smoke.py`) |

**Zeile 7, Step 6 abgeschlossen:** `search_items`, `get_item`, `create_item`, `update_item`,
`append_to_item` lösen ihre seit Step 5 bestehenden `NotImplementedError`-Platzhalter ein
(§3.2/§3.4/§3.5/§3.6) — `list_spaces` war seit Step 5 bereits fertig. Zeile 6 (`test_app.py`)
wuchs um einen sechsten Test (`test_all_six_tools_are_callable_over_http`), der Step 6s eigenes
Done-when „alle sechs Tools über den ASGI-Testclient aufrufbar" gegen den echten Stack aus
Step 5 beweist — `test_tools.py` allein kann das nicht, weil dort der Guard gemockt ist (siehe
SESSIONS_ARCHIVE.md).

**Zeile 8, Step 7 abgeschlossen:** `mcp_smoke.py` (Gegenstück zu `space_cli.py` aus P1) plus
Runbook „Quick-Tunnel-Probe" oben und README-Abschnitt „MCP-Server smoke-testen". Grün gegen
ein temporäres `DATA_ROOT` verifiziert (Session-Block).

**Phase 2 ist ab 2026-07-26 live-verifiziert (§5.9):** der Nikinger hat die Quick-Tunnel-Probe
durchgeführt und zusätzlich eine vollständige Adapter-Abnahme über den echten Custom Connector
gefahren — 21 von 21 Prüfungen bestanden, gegen den echten `DATA_ROOT`, mit Rohantworten als
Beweis. Details, Prüfmatrix und Belege: `docs/concepts/P2_ADAPTER_ABNAHME_2026-07-26.md`.
`ROADMAP.md` steht jetzt auf ✅.

**Fund B1 aus der Abnahme, behoben (2026-07-26):** `list_spaces` zeigte den eigenen Space
nicht, solange er kein einziges Item hatte — `Store.list_spaces()` leitet Spaces ausschließlich
aus Indexzeilen ab (P1, keine separate Space-Registry), ein leerer Space hat keine. Eine
frische Claude-Sitzung sah damit ausschließlich Spaces, in die sie nicht schreiben darf, ohne
Möglichkeit, den eigenen Space-Namen vor dem ersten `create_item` zu erfahren. **Was geändert
wurde:** `mcpserver/tools.py :: list_spaces()` nimmt den eigenen Space jetzt immer in die
Antwort auf, notfalls mit `item_count: 0` — reine Tool-Schicht-Ergänzung, kein Store-Eingriff,
kein Contract-Bruch. Neuer Test `test_list_spaces_includes_empty_own_space`
(`test_tools.py`). Fund B2 (Space-Namen `nikinger`/`niklas` gemischt) bleibt bewusst offen —
Entscheidung des Nikingers auf dem echten `DATA_ROOT`, kein Code-Thema.

**Nebenbefund beim Nachtesten, nicht Teil der Abnahme:** `mcp_smoke.py`s eigener
`search_items`-Check war intermittierend flakig. Ursache: das Skript legt über 20 Items in
einer engen Schleife über die reale Systemuhr an (kein injizierter `now_fn` wie in den
Unit-Tests) — auf einer schnellen VM bekamen mehrere Items denselben `updated`-Zeitstempel,
und `Store.search()`s Sortierung entschied unter dieser Bindung über die Indexreihenfolge,
nicht die Anlegereihenfolge. Das drückte gelegentlich eines der drei `create_item`-Items aus
der Top-20-Seite. Kein Bug in `tools.py`/`store.py`. Behoben durch Aufteilen des Checks: die
Default-Listing-Prüfung misst nur noch Form + Größe (unabhängig von genau diesen drei IDs), eine
neue gezielte `search_items(query="Smoke-Item")`-Prüfung bestätigt die Fundbarkeit unabhängig
von Paginierung/Sortierreihenfolge. Acht Läufe in Folge grün, `pytest` viermal in Folge grün.

**Sicherheitsvorfall während der Abnahme, dokumentiert statt stillschweigend übergangen:** der
Nikinger teilte einen Screenshot des Connectors, der die volle URL inklusive Pfad-Token im
Klartext zeigte — und Claude Code wiederholte diesen Token dann selbst im Chat, um den Fund zu
erklären. Strukturell derselbe Vorfall wie in Step 3 (`SESSIONS_ARCHIVE.md`): ein Token außerhalb
des Keyrings, diesmal zusätzlich selbst verursacht statt nur weitergemeldet. **Sofort erkannt
und benannt, nicht stillschweigend weitergemacht.** Der Nikinger hat den Token für `niklas`
umgehend rotiert (`--revoke` + neu `--space`). Der Screenshot wurde **nicht** in dieses Repo
übernommen. Lehre, gleich wie in Step 3: ein Klartext-Token gehört nie in eine Antwort, auch
nicht beim Erklären eines Fundes — dieselbe Regel wie für Commits gilt auch für das eigene
Zitieren.

**[Korrektur 2026-07-26, Folgesession]:** Die Bilddatei lag bis zur Folgesession weiterhin
ungetrackt im Arbeitsverzeichnis (`docs/test-results/`) — nie versioniert, aber auch nicht
sofort entfernt. Nach Rücksprache mit dem Nikinger (Token bereits rotiert, Löschung freigegeben)
gelöscht. Lehre ergänzt: eine Doku-Aussage über den Repo-Zustand ist erst wahr, wenn `git
status` sie bestätigt, nicht wenn die Absicht dokumentiert wurde. Details: aktueller
Session-Block.

**Gesamt: 57 Tests** in `phase2_mcp/tests/` (3 `test_config.py` + 6 `test_credentials.py` + 4
`test_auth.py` + 3 `test_permissions.py` + 1 `test_logging.py` + 2 `test_context.py` + 4
`test_asgi.py` + 8 `test_app.py` + 23 `test_tools.py` + 3 `test_mcp_smoke.py`). Acht weitere
Tests aus Step 2 liegen in `phase1_storage/tests/` (siehe Modul-Status Zeile 3 und
`phase1_storage/CLAUDE.md`), werden dort mitgezählt, nicht hier.

## Geerbte Contracts

Aus P1 (`phase1_storage/CLAUDE.md`, `docs/concepts/phase1_storage_plan.md` §1/§2): Frontmatter-
Schema, `Item`/`SpaceInfo`/`ItemSummary`/`SearchResult`/`IndexStats`, `Store`-Signaturen
(`list_spaces`/`search`/`get`/`create`/`update`/`append`/`archive`/`rebuild_index`),
Fehlertypen inkl. `ConflictError.current`. **[2026-07-25, Step 2 abgeschlossen]** Drei
einmalige, vom Nikinger freigegebene Erweiterungen sind eingebracht (`space_of()`,
`get(..., repair_drift=)`, Statusvalidierung über `models.STATUS_VALUES`) — Details, Tests und
Begründung stehen in `phase1_storage/CLAUDE.md` unter „Geerbte Contracts" (dort, nicht doppelt
hier, da Code-nah). **Der Contract ist ab jetzt wieder zu.**

**D1, festgehalten statt stillschweigend übernommen:** `docs/concepts/PHASE1_CLOSEOUT_HANDOVER.md`
verlangte ausdrücklich Gegenprüfung von `ItemSummary` und `SpaceInfo.name`/`.item_count` (beides
Claude-Code-Eigenentscheidungen aus P1, im P1-Plan nicht spezifiziert), bevor P2 darauf aufbaut.
Der P2-Plan (`docs/concepts/phase2_mcp_plan.md` §0.2) übernimmt beide bereits als „gegeben" —
das zählt als Bestätigung durch die Browser-Planungssession mit dem Nikinger. Hier trotzdem
explizit vermerkt: **gilt als bestätigt, wenn der Nikinger nicht widerspricht** (siehe
Step-0-Session-Block unten).

**Warum nur Hashes im Keyring** (Plan §2.3, seit Step 3 in `mcpserver/credentials.py` real
umgesetzt): der Server muss ein Token nur *wiedererkennen*, nie *vorzeigen*. `issue()` gibt das
Token genau einmal zurück; ab dann existiert im Keyring nur noch
`{sha256(token): space}`. Wer diese Eigenschaft aufgibt, um „das Token nochmal anzeigen" zu
können, macht aus dem Keyring eine Passwortliste.

**Was der Pfad-Token nicht ist** (Plan §2.3): kein OAuth-Ersatz, kein Schutz gegen Cloudflare
(R4 — Cloudflare sieht bei P3 ohnehin Klartext), gültig bis P3+1. Siehe P2-Plan §0.3 für die
Begründung, warum OAuth trotzdem hinter P3 bleibt statt vorgezogen zu werden.

**`version` in fremden Spaces** (Plan §3.4): `get(..., repair_drift=)` existiert seit Step 2 im
Store; genutzt wird es ab Step 6 (`tools.py :: get_item`, §3.4). Dort ist `version` in fremden
Spaces informativ, nicht autoritativ — es gibt dort per Architektur keine Writes.

## Runbook „Quick-Tunnel-Probe" (führt der Nikinger aus, nicht Claude Code)

Der Tunnel-Schritt wird **nicht committet** — kein Skript, keine Config, kein Hostname im Repo
(das ist P3). Diese Anleitung ist reine Dokumentation des Ablaufs (Plan §4 Step 7).

**[2026-07-26 Korrektur, vom Nikinger beim ersten Live-Lauf gefunden]** Die ursprüngliche
Reihenfolge (`serve.py --allowed-host` vor `cloudflared`) war zirkulär: die trycloudflare.com-
Subdomain wird von `cloudflared` **zufällig bei jedem Start neu vergeben**, existiert also erst
NACH Schritt „Tunnel starten" — sie kann nicht vorher in `--allowed-host` stehen. Reihenfolge
jetzt korrekt (Tunnel zuerst, Subdomain ablesen, danach `serve.py` mit der bekannten Subdomain
starten). Kein Bug im Code — `serve.py`/`app.py` hatten von Anfang an einen `--allowed-host`-
Parameter genau für diesen Zweck, nur die Runbook-Reihenfolge war falsch:

```
1. python phase2_mcp/scripts/issue_token.py --space niklas      # Token einmal notieren
2. cloudflared tunnel --url http://127.0.0.1:8765
       # Ausgabe abwarten: "Your quick Tunnel has been created!" mit der zugewiesenen
       # https://<subdomain>.trycloudflare.com — läuft in diesem Terminal weiter
3. SPACE_DATA_ROOT=/home/savefyx/savefyx-data python phase2_mcp/scripts/serve.py \
       --allowed-host '<subdomain>.trycloudflare.com'      # die aus Schritt 2 bekannte Subdomain
4. curl https://<subdomain>.trycloudflare.com/health        → {"status":"ok",…}
5. Claude → Settings → Connectors → Add custom connector:
       https://<subdomain>.trycloudflare.com/mcp/<token>
6. Neue Konversation, Connector aktivieren, ein Read und ein Write ausführen.
```

Bei jedem Neustart von `cloudflared` ändert sich die Subdomain — `serve.py` muss dann mit der
neuen Subdomain neu gestartet werden (Schritt 3 wiederholen).

**Live-Stand (2026-07-26):** Alle sechs Schritte vom Nikinger erfolgreich durchgeführt — Token
ausgegeben, Tunnel verbunden (`https://flyer-only-gaming-cpu.trycloudflare.com`, Frankfurt-Edge,
CONNECTIVITY PRE-CHECKS alle PASS), `serve.py` mit korrektem `--allowed-host` gestartet,
`curl .../health` → `{"status":"ok",...}`, Connector in Claude angelegt, **21 Tool-Aufrufe über
eine echte Konversation** statt nur ein Read und ein Write. Vollständiges Protokoll:
`docs/concepts/P2_ADAPTER_ABNAHME_2026-07-26.md`. `ROADMAP.md` steht auf ✅.

**Sicherheitsvorfall im selben Lauf:** ein Screenshot des Connectors zeigte die Verbindungs-URL
inklusive Pfad-Token im Klartext, und der Token wurde beim Erklären des Fundes zusätzlich im
Chat wiederholt — strukturell derselbe Vorfall wie in Step 3. Sofort erkannt, Token vom
Nikinger rotiert, Screenshot nie versioniert (Korrektur oben unter Modul-Status).

### Cloudflare-Voraussetzungen (vor Schritt 2)

**Kurz: nichts von Cloudflare nötig.** Schritt 2 benutzt Cloudflares **Quick Tunnel**
(`cloudflared tunnel --url ...`) — keine Registrierung, kein Account, keine Domain, kein
API-Token, kein `cloudflared login`. Nur der `cloudflared`-Client muss auf der VM installiert
sein. **Falle:** die meisten Cloudflare-Tutorials im Netz beschreiben stattdessen „Named
Tunnels" (`cloudflared tunnel create ...`), die einen Account **und** eine bei Cloudflare
verwaltete Domain brauchen — das ist ein anderer, schwererer Weg, nicht der hier benutzte.

`cloudflared` installieren, zwei Wege:

```bash
# Weg A — offizielles apt-Repo (sauber aktualisierbar)
sudo mkdir -p --mode=0755 /usr/share/keyrings
curl -fsSL https://pkg.cloudflare.com/cloudflare-main.gpg | sudo tee /usr/share/keyrings/cloudflare-main.gpg >/dev/null
echo "deb [signed-by=/usr/share/keyrings/cloudflare-main.gpg] https://pkg.cloudflare.com/cloudflared $(lsb_release -cs) main" | sudo tee /etc/apt/sources.list.d/cloudflared.list
sudo apt update && sudo apt install cloudflared

# Weg B — einzelnes Binary (schneller, kein Repo, reicht für einen einmaligen Test)
uname -m   # x86_64 -> amd64, aarch64 -> arm64
curl -Lo cloudflared https://github.com/cloudflare/cloudflared/releases/latest/download/cloudflared-linux-amd64
chmod +x cloudflared && sudo mv cloudflared /usr/local/bin/
```

`cloudflared --version` zur Kontrolle. `cloudflared tunnel --url ...` gibt sofort eine
zufällige `https://….trycloudflare.com`-URL aus, ohne Login-Prompt. Diese URL ist **ephemer**
— sie ändert sich bei jedem Neustart von `cloudflared`, für den einmaligen Probe-Lauf egal,
aber genau der Grund, warum R3 das als Übergang vor VPS+WireGuard (P3) behandelt, nicht als
Dauerlösung. Cloudflare sieht dabei weiterhin Klartext (R4, bereits akzeptiert). Weiches Limit
von ca. 200 gleichzeitigen Requests je Quick Tunnel — für einen manuellen Test irrelevant.

`[VERIFY]` bei Ausführung gegen die aktuelle Anthropic-Doku: Custom Connectors auf **Pro** ohne
Owner-Gate (Stand 2026-07-25 dokumentiert für Free/Pro/Max/Team/Enterprise; Free ist auf einen
Connector begrenzt). Diese Prüfung ist Sache des Nikingers beim Ausführen, nicht von Claude
Code — der Tunnel-/Connector-Schritt liegt außerhalb des P2-Scopes (§7).

**Ergebnis melden:** ein erfolgreicher Read und ein erfolgreicher Write über den echten
Connector heben Phase 2 von „code-complete" auf „live-verifiziert" (Akzeptanzkriterium §5.9) —
analog zu Phase 1s Live-Verify durch den Nikinger gegen den echten `DATA_ROOT`.

---

## Session stopped — 2026-07-26 (Live-Verifizierung: Adapter-Abnahme, B1-Fix, Screenshot-Fund)

**Ergebnis:** Phase 2 ist **live-verifiziert** (§5.9). Der Nikinger hat die Quick-Tunnel-Probe
durchgeführt und zusätzlich eine vollständige Adapter-Abnahme über den echten Custom Connector
gefahren — 21 von 21 Prüfungen gegen den echten `DATA_ROOT`, mit Rohantworten als Beweis.
Vollständiges Protokoll: `docs/concepts/P2_ADAPTER_ABNAHME_2026-07-26.md`. `ROADMAP.md` steht
auf ✅. Details siehe Modul-Status-Tabelle oben (Zeile 8).

**Fund B1, behoben:** `list_spaces` zeigte den eigenen Space nicht, solange er kein Item hatte.
`mcpserver/tools.py :: list_spaces()` nimmt den eigenen Space jetzt immer in die Antwort auf,
notfalls mit `item_count: 0` — reine Tool-Schicht-Ergänzung, kein Store-Eingriff. Neuer Test
`test_list_spaces_includes_empty_own_space`. Fund B2 (Space-Namen `nikinger`/`niklas` gemischt)
bleibt offen — Entscheidung des Nikingers auf dem echten `DATA_ROOT`, kein Code-Thema.

**`mcp_smoke.py`-Flakiness behoben:** das Skript legt Items in einer engen Schleife über die
reale Systemuhr an; auf einer schnellen VM konnten mehrere Items denselben `updated`-Zeitstempel
bekommen, wodurch die stabile Sortierung gelegentlich eines der drei `create_item`-Items aus der
Top-20-Seite drückte. Kein Bug in `tools.py`/`store.py`. Der `search_items`-Check ist jetzt
zweigeteilt: eine Default-Listing-Prüfung (Form + Größe, unabhängig von genau diesen IDs) und
eine gezielte `search_items(query="Smoke-Item")`-Prüfung für die Fundbarkeit. Aktueller Lauf:
12/12 Checks grün (`python phase2_mcp/scripts/mcp_smoke.py --json`).

**Sicherheitsvorfall, zweiteilig:** (1) Während der Abnahme zeigte ein Screenshot des Connectors
die Verbindungs-URL inklusive Pfad-Token im Klartext, und der Token wurde beim Erklären des
Fundes zusätzlich im Chat wiederholt — strukturell derselbe Vorfall wie in Step 3
(`SESSIONS_ARCHIVE.md`). Sofort erkannt, der Nikinger hat den Token für `niklas` umgehend
rotiert (`--revoke` + neu `--space`). (2) Bei der Übernahme in diese Session stellte sich heraus,
dass genau dieser Screenshot trotz gegenteiliger Doku-Aussage weiterhin ungetrackt im
Arbeitsverzeichnis lag (`docs/test-results/2026_07_26_p2-mcp-test/`) — die Behauptung „bewusst
nicht ins Repo übernommen" war zum Zeitpunkt dieser Session schlicht falsch. Vor jeder Aktion
beim Nikinger nachgefragt (Datei ist sein Artefakt, Löschen ist destruktiv); er bestätigte, dass
der abgebildete Token bereits durch den Rotationsschritt zerstört ist, und gab die Löschung
frei. Datei + leeres Verzeichnis entfernt, `docs/concepts/P2_ADAPTER_ABNAHME_2026-07-26.md` §7
um eine datierte Korrekturnotiz ergänzt (die Aussage selbst wird nicht rückwirkend umgeschrieben
— das Dokument ist ein 📕-Snapshot). Lehre: eine Doku-Aussage über den Repo-Zustand ist erst
wahr, wenn `git status` sie bestätigt, nicht wenn die Absicht dokumentiert wurde.

**Verifiziert:** `pytest -v` → **133/133 grün** (76 P1 + 57 P2, Aufschlüsselung je Testdatei
gegen die Modul-Status-Tabelle nachgezählt, exakt deckungsgleich). `mcp_smoke.py --json` → 12/12
Checks grün. `git status` nach der Bereinigung → `docs/test-results/` existiert nicht mehr.

**Nächster Schritt (konkret):** B2 ist die einzige offene Entscheidung dieser Phase und liegt
beim Nikinger (zwei Wege, siehe `docs/concepts/P2_ADAPTER_ABNAHME_2026-07-26.md` §4). Danach:
offizieller Phasenabschluss P2 (Browser-Webchat, analog Phase 1s Abschluss), Handover-Dokument
für P3 (Tunnel/systemd/Ops), neue Browser-Planungssession für Phase 3.
