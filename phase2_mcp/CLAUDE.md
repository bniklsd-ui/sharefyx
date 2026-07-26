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
updated: 2026-07-26 (Step 7)
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
| 7 | `tools.py` (die sechs Tools) | 6 | ✅ | 22 (`test_tools.py`) |
| 8 | `scripts/mcp_smoke.py`, Runbook, Größenmessung | 7 | ✅ (code-complete — Live-Probe steht beim Nikinger aus) | 3 (`test_mcp_smoke.py`) |

**Zeile 7, Step 6 abgeschlossen:** `search_items`, `get_item`, `create_item`, `update_item`,
`append_to_item` lösen ihre seit Step 5 bestehenden `NotImplementedError`-Platzhalter ein
(§3.2/§3.4/§3.5/§3.6) — `list_spaces` war seit Step 5 bereits fertig. Zeile 6 (`test_app.py`)
wuchs um einen sechsten Test (`test_all_six_tools_are_callable_over_http`), der Step 6s eigenes
Done-when „alle sechs Tools über den ASGI-Testclient aufrufbar" gegen den echten Stack aus
Step 5 beweist — `test_tools.py` allein kann das nicht, weil dort der Guard gemockt ist (siehe
SESSIONS_ARCHIVE.md).

**Zeile 8, Step 7 abgeschlossen:** `mcp_smoke.py` (Gegenstück zu `space_cli.py` aus P1) plus
Runbook „Quick-Tunnel-Probe" oben und README-Abschnitt „MCP-Server smoke-testen". Grün gegen
ein temporäres `DATA_ROOT` verifiziert (Session-Block). Phase 2 ist damit **code-complete**;
„live-verifiziert" (§5.9) folgt erst, wenn der Nikinger die Quick-Tunnel-Probe gemeldet hat —
siehe `ROADMAP.md`, Status 🟡.

**Gesamt: 56 Tests** in `phase2_mcp/tests/` (3 `test_config.py` + 6 `test_credentials.py` + 4
`test_auth.py` + 3 `test_permissions.py` + 1 `test_logging.py` + 2 `test_context.py` + 4
`test_asgi.py` + 8 `test_app.py` + 22 `test_tools.py` + 3 `test_mcp_smoke.py`). Acht weitere
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

**Live-Stand (2026-07-26):** Schritte 1–4 vom Nikinger erfolgreich durchgeführt — Token
ausgegeben, Tunnel verbunden (`https://flyer-only-gaming-cpu.trycloudflare.com`, Frankfurt-Edge,
CONNECTIVITY PRE-CHECKS alle PASS), `serve.py` mit korrektem `--allowed-host` gestartet,
`curl .../health` → `{"status":"ok",...}`. Das beweist die Tunnel-Infrastruktur (R3) durch das
CGNAT-Mobilfunk-Uplink hindurch — **nicht** aber Akzeptanzkriterium §5.9: `/health` ist
unauthentifiziert und durchläuft weder `TokenPathASGI` noch ein einziges Tool. Schritte 5–6
(Connector in Claude anlegen, ein echter Read und ein echter Write aus einer Konversation)
stehen noch aus — erst danach wechselt `ROADMAP.md` von 🟡 auf ✅.

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

## Session stopped — 2026-07-26 (Step 7: Smoke-Test, Messung, Runbook)

**Ergebnis:** `phase2_mcp/scripts/mcp_smoke.py` — Gegenstück zu `space_cli.py` aus P1. Baut ein
**temporäres** `DATA_ROOT` (`tempfile.TemporaryDirectory`, nie das echte), zwei Fixture-Spaces
(`alpha`/`beta`), startet `create_app()` in-process über `httpx.ASGITransport` (kein echter
Port, kein Netz — dasselbe Muster wie `test_app.py`) und fährt alle acht Prüfpunkte aus dem
Plan durch: `list_spaces`, `create_item` ×3, `search_items`, `get_item` eigen/fremd, ein
`update_item`-Konflikt, `append_to_item`, `update_item(status=archived)`, ein `update_item` auf
einen fremden Space. `--json` für maschinenlesbare Ausgabe, sonst Textreport; Exit-Code `1` bei
jeder fehlgeschlagenen Prüfung. README bekam den Abschnitt „MCP-Server smoke-testen", der
Phase-Head diesen hier stehenden Runbook-Abschnitt „Quick-Tunnel-Probe" (oben, dauerhaft, nicht
nur im Session-Block — der Tunnel-Schritt selbst bleibt außerhalb des Repos).

**Kein echter Keyring, bewusst:** `mcp_smoke.py` importiert `keyring` nicht direkt — die beiden
Tokens entstehen über `credentials.generate_token()`/`hash_token()` (reine Funktionen) und
werden per injiziertem `load_map` in einen `KeyringTokenResolver` gereicht, exakt das Muster
aus den Unit-Tests. Ein Skript, das beliebig oft laufen soll, darf die reale Token→Space-Map
unter `nikinger-space` nicht anfassen. Empirisch geprüft (nicht nur behauptet): `load_space_map()`
gegen den echten Keyring zeigt nach mehreren `mcp_smoke.py`-Läufen weiterhin nur den einen
`nikinger`-Eintrag aus Step 3 — keine `alpha`/`beta`-Verschmutzung.

**Ein echter Fund beim ersten Lauf, kein Advisor-Vorgriff:** `list_spaces` schlug beim ersten
Durchlauf fehl (`Spaces=['beta']` statt beider). Ursache: `Store.list_spaces()` leitet Spaces
ausschließlich aus vorhandenen Items ab (P1, keine separate Space-Registry) — `alpha` hatte zum
Zeitpunkt des ersten `list_spaces`-Aufrufs (Plan-Reihenfolge: Prüfpunkt 1, vor jedem
`create_item`) schlicht noch kein Item und war deshalb unsichtbar. Kein Bug in `tools.py`, ein
Fixture-Fehler im Smoke-Skript: `alpha` bekommt jetzt denselben Seed-Eintrag wie `beta`, bevor
die Prüfungen beginnen.

**Automatisiert statt nur manuell bewiesen** (wie `space_cli.py` in P1 per Subprozess-Tests):
`test_mcp_smoke.py` neu, 3 Tests, ruft `mcp_smoke.py` als echten Subprozess auf (kein Import —
gleiche Begründung wie bei `space_cli.py`: Namenskollisionsgefahr über künftige Phasen hinweg,
realistischste Prüfung). Prüft `--json`-Exit-Code 0 und dass alle Checks grün sind (Anzahl
bewusst **nicht** hartkodiert — der Exit-Code trägt das Pass/Fail-Signal, ein `len(checks) ==
N` würde bei jeder künftigen zusätzlichen Prüfung unnötig brechen), den Text-Report per Regex,
und statisch (Quelltext-Grep), dass das Skript `keyring` nicht direkt importiert.

**Advisor-Review vor dem Commit, ein Fund korrigiert (blockierend), zwei kleinere mitgenommen:**
Die erste Fassung der Größenmessung maß `search_items` gegen nur 5 vorhandene Treffer (1058 B)
— das beantwortet nicht die Frage, für die Step 7s eigenes Done-when eine Größentabelle
verlangt: hält das Token-Budget bei einem **echten Default-Listing** (§5 Kriterium 5, 20 Items
< 12 KB)? `mcp_smoke.py` seedet jetzt 17 zusätzliche Füll-Items mit realistischer Body-Länge
(vor den drei `create_item`-Aufrufen, damit diese als jüngste Items sicher im ersten
20er-Fenster bleiben) — `search_items` misst jetzt tatsächlich eine volle 20-Item-Seite.
Kleinere Fixes im selben Aufwasch: der Subprozess-Test hartkodierte die Checkanzahl (`== 11`,
siehe oben) und der YAML-Feld-Extraktor `_extract_field` bekam einen Kommentar zur stillen
Reihenfolge-Abhängigkeit (Frontmatter kommt immer vor dem Body, deshalb gewinnt bei
`re.search` nie eine zufällig gleichlautende Body-Zeile).

**Größenmessung (Bytes je Antwort, Live-Lauf gegen ein temporäres `DATA_ROOT`):**

| Operation | Bytes |
|---|---|
| `list_spaces` | 98 |
| `create_item` #1 | 172 |
| `create_item` #2 | 172 |
| `create_item` #3 | 172 |
| `search_items` (Default-Listing, 20 von 22 Treffern) | 6403 |
| `get_item` (eigen) | 172 |
| `get_item` (fremd, gewrappt) | 242 |
| `update_item` (Konflikt) | 140 |
| `append_to_item` | 183 |
| `update_item` (archivieren) | 187 |
| `update_item` (fremder Space, `write_denied`) | 65 |

`search_items` bei 6403 B liegt klar unter dem §5-Budget (20 Items < 12 KB) — jetzt eine echte
Antwort auf die Kriteriumsfrage, nicht nur ein Bestwert-Artefakt. Ergänzt, nicht ersetzt durch
`test_tools.py::test_search_result_size_budget` (Step 6, 20/30-Item-Grenzfälle als
Pass/Fail-Assertion in der Testsuite statt als gemeldete Zahl im Session-Block).

**Verifiziert (live):** `pytest -v` → **132/132 grün** (76 P1 + 56 P2). `mcp_smoke.py` manuell
ausgeführt (Text und `--json`, nach dem Advisor-Fix erneut), alle elf Prüfungen grün,
temporäres Verzeichnis nach Lauf sauber entfernt (`ls /tmp/mcp_smoke_*` findet nichts mehr).

**Phase 2 ist damit code-complete** (ROADMAP.md: 🟡). Fehlt für ✅ „live-verifiziert" (§5.9):
die Quick-Tunnel-Probe durch den Nikinger (Runbook oben) — ein echter Read und ein echter Write
über den Claude-Connector gegen den echten `DATA_ROOT`. Das ist die einzige verbleibende
Handlung dieser Phase, die Claude Code nicht selbst ausführen darf (Hard Rule: kein Test gegen
den echten `DATA_ROOT` durch Claude Code; Tunnel/Connector-Einrichtung ist ohnehin
Nikinger-Sache).

**Nächster Schritt (konkret):** Nikinger führt die Quick-Tunnel-Probe aus (Runbook oben) und
meldet das Ergebnis. Danach: offizieller Phasenabschluss P2 (laut `docs/PROMPTS.md` als eigener
Prompt im Browser-Webchat, analog zu Phase 1s Abschluss) — Status auf ✅, Handover-Dokument für
P3 (Tunnel/systemd/Ops), neue Browser-Planungssession für Phase 3.
