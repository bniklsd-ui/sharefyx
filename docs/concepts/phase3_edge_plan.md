---
status: plan (ausführungsreif)
purpose: Phase 3 — Exposure & Betrieb. Entscheidungen P3-A–P3-N gelockt, Steps 0–7 sequenziert, Namen fixiert. Direkt an Claude Code übergebbar.
read-when: Ausführung von Phase 3; NICHT bei Session-Start anderer Phasen
detail: L2
up: ../../phase3_edge/CLAUDE.md
down:
  - ./PHASE2_CLOSEOUT_HANDOVER.md          # Herkunft der offenen Entscheidungen 1–8
  - ./phase2_mcp_plan.md                    # Entscheidungen P2-A–P2-N, Modul- und Tool-Contract
updated: 2026-07-26
---
# Phase 3 — Exposure & Betrieb
## Implementierungsplan für Claude Code

> **Author:** Browser-Planungssession, 2026-07-26 (Nikinger + Claude).
> **Audience:** Claude Code. Der Plan ist ausführungsreif — Entscheidungen sind gelockt,
> Schritte sequenziert, Namen fixiert. **Nichts hier muss neu hergeleitet werden.**
>
> **Drift-Konvention:** Alles, was gegen den echten Repo-Stand, die VM oder eine externe
> Bibliothek geprüft werden muss, ist **`[VERIFY]`** markiert — bei Ausführung verifizieren, nie
> als gesichert übernehmen. Register in §8.
>
> **Zu den Ankern:** Die Planungssession hatte Lesezugriff auf den Repo-Snapshot vom
> **2026-07-26 19:11 UTC** (Drive), aber ohne Zeilennummern. Deshalb stehen hier
> **Funktions-Anker** (`datei.py :: funktion()`) und, wo es exakter geht, **wörtliche
> Suchstrings**. Trage die realen Zeilennummern beim ersten Lesen in deine Step-Notizen ein,
> nicht in diesen Plan.
>
> **Doc-Layers gilt:** jede neue `.md` bekommt eine L1-Header-Card und eine Zeile in
> `docs/INDEX.md` — **im selben Commit** (Hard Rule 8).

---

## §0 Mission, Scope, gelockte Entscheidungen

### 0.1 Mission

**Der Connector steht in beiden Claude-Accounts und bleibt stehen.** P3 fügt dem in P2
bewiesenen Server nichts Fachliches hinzu. Sie gibt ihm drei Dinge, die er bisher nicht hatte:
eine **dauerhafte Adresse**, einen **Prozess, der von allein wieder hochkommt**, und ein
**Protokoll darüber, was er tut und wie lange er dafür braucht**.

**Bauprinzip-Erinnerung:** Der Server ist dumm. P3 enthält **keine AI**, keine neuen Tools,
keine Fachlogik. Wer hier `tools.py` anfasst, ist in der falschen Phase.

**Der eigentliche Härtetest der Phase ist nicht der Tunnel, sondern die Wiederherstellbarkeit:**
Nach einem VM-Reboot, nach einem `kill -9` und nach einem Backup-Restore muss dieselbe URL
dieselben Daten liefern — ohne dass ein Mensch etwas nachträgt.

### 0.2 Was P3 als gegeben übernimmt (nicht neu herleiten)

| Was | Wo es im Wortlaut steht |
|---|---|
| Sechs Tools, Tool-Contract, Fehlerabbildung | `docs/concepts/phase2_mcp_plan.md` §3 |
| `SpaceResolver` → `Principal`, `Permissions`-Seam | `phase2_mcp/mcpserver/auth.py`, `permissions.py` |
| Keyring-Format `{sha256(token): space}` | `phase2_mcp/mcpserver/credentials.py` |
| Transport-Layout (`/health` + `Mount("/mcp")` + `TokenPathASGI`) | `phase2_mcp/mcpserver/app.py`, `asgi.py` |
| Rahmenentscheidungen R1–R6, Hard Rules 1–8 | Root-`CLAUDE.md` |
| Offene Entscheidungen 1–8, Doku-Drift, geerbte `[VERIFY]` | `docs/concepts/PHASE2_CLOSEOUT_HANDOVER.md` |

**Scope laut `ROADMAP.md`, Phase 3 — DRIN:** Tunnel, systemd-Unit (`Restart=on-failure`,
`LoadCredential`), `/health`, strukturiertes Request-Log mit Tool-Name und Dauer, Backup des
Datenverzeichnisses, Runbook „Connector zeigt Disconnected".
**DRAUSSEN:** VPS-Migration, Monitoring/Alerting, OAuth, UI, neue Tools, D6.

### 0.3 Die drei Entscheidungen des Nikingers vom 2026-07-26

Sie sind der Grund, warum dieser Plan so aussieht, und stehen deshalb vor der Tabelle:

1. **Exposure über Tailscale Funnel** statt Cloudflare Named Tunnel. Kein Domainkauf, kein
   NS-Wechsel, stabiler Hostname, kostenlos.
2. **Space-Map über systemd `LoadCredential`** statt Keyring-im-Dienst.
3. **`fabian` und der zweite Connector sind Abnahmekriterium**, nicht Nacharbeit.

### 0.4 Korrektur zu Rahmenentscheidung R4 — nicht still, sondern datiert

R4 sagt heute: *„bei Cloudflare Tunnel terminiert Cloudflare TLS und sieht Klartext. Kein E2E."*

Mit Tailscale Funnel ist der erste Halbsatz **auf diesem Weg nicht mehr zutreffend**. Laut
Tailscales eigener Dokumentation terminiert **die Node selbst** TLS; die Funnel-Relays leiten
den verschlüsselten Strom weiter, ohne ihn zu entschlüsseln, und Tailscale erwirbt für
Funnel-Namen bewusst keine Zertifikate — nachprüfbar in den öffentlichen
Certificate-Transparency-Logs.

**Was daraus folgt und was nicht:**

- ✅ Der Relay-Betreiber sieht die Notizinhalte **nicht** im Klartext. Das ist gegenüber dem
  Cloudflare-Weg eine echte Verbesserung, keine Kosmetik.
- ❌ Es ist trotzdem **kein E2E**. Tailscale bleibt vertrauenswürdige Infrastruktur:
  Koordinationsserver, DNS für `ts.net`, Relays. Wer den Namen kontrolliert, könnte jederzeit
  ein gültiges Zertifikat erwerben. Die Aussage „kein E2E" bleibt also stehen — nur ihre
  Begründung wird präziser.

**Aufgabe in Step 0:** Root-`CLAUDE.md`, R4 bekommt eine **datierte Ergänzung** mit genau diesem
Inhalt. Der ursprüngliche Satz bleibt wörtlich stehen (er beschreibt korrekt, was bei Cloudflare
gilt) — ergänzt um „Ab P3 läuft der Weg über Tailscale Funnel; dort terminiert die Node selbst
TLS, siehe `docs/concepts/phase3_edge_plan.md` §0.4."

### 0.5 Gelockte Entscheidungen (P3-A – P3-N)

| # | Thema | Festlegung |
|---|---|---|
| **A** | Exposure | **Tailscale Funnel.** Stabiler Hostname `<node>.<tailnet>.ts.net`, TLS-Terminierung auf der Node, Persistenz über `--bg`. Voraussetzungen (Nikinger-Arbeit, nicht Claude Code): Tailscale ≥ 1.38.3, MagicDNS an, HTTPS-Zertifikate für den Tailnet an, `nodeAttrs`-Attribut **`funnel`** im Policy-File. Nur Ports **443 / 8443 / 10000** erlaubt. `[VERIFY]` V7. |
| **B** | Bindung | Der Server lauscht unverändert auf **`127.0.0.1:8765`**. Funnel proxyt dorthin. `SPACE_HOST` wird **nie** `0.0.0.0` — auch nicht „nur zum Testen". Hard Rule 6 gilt damit nicht nur am Router, sondern am Host. |
| **C** | `allowed_hosts` | Wird **Konfiguration statt CLI-Zufall**: neue Env-Variable `SPACE_ALLOWED_HOSTS` (kommagetrennt) in `config.py`. `serve.py --allowed-host` bleibt bestehen und **gewinnt**, wenn gesetzt. Grund: die systemd-Unit soll eine `Environment=`-Zeile pflegen, keine Argumentliste. |
| **D** | Bibliotheks-Pin | **`fastmcp==3.4.4` exakt** statt `>=3.4,<3.5`. Begründung: 3.4.3 hat den Host/Origin-Guard verschärft, 3.4.4 ihn wieder gelockert — Patchversionen ändern hier **Verhalten**, und unter einem Dauerdienst darf sich das nicht unbemerkt bewegen. Upgrades werden ein bewusster Commit mit Smoke-Test. `[VERIFY]` V2. |
| **E** | MCP-Revision 2026-07-28 | **Nicht in P3.** Belege: `fastmcp` 3.4.4 (08.07.2026) hat keinen Support; laut MCP-Blog brechen bestehende 2025-11-25-Server nicht, neue Clients handeln auf 2025-11-25 herunter. Watch-Item mit **Trigger statt Datum**: „erstes `fastmcp`-Release mit 2026-07-28-Support" → dann eigene Mini-Phase, weil es einen Bibliotheks-Major und `app.py` berührt. |
| **F** | Secrets | **`LoadCredentialEncrypted`.** `systemd-creds encrypt` erzeugt `/etc/sharefyx/spaces.cred`; systemd legt den Klartext nur im tmpfs unter `$CREDENTIALS_DIRECTORY/spaces` ab. `credentials.py :: load_space_map()` bekommt **genau eine** neue Verzweigung: Credentials-Verzeichnis zuerst, Keyring als Fallback. **Ehrlich dazu:** der Inhalt ist eine sha256-Hash-Map, kein umkehrbares Geheimnis. Die Verschlüsselung ist Regeltreue (Hard Rule 1) und Vorbereitung auf P4 (dort liegen echte Signing-Keys) — nicht Schutz dieser Datei. |
| **G** | Zwei Nutzer | **Ein Prozess, eine Unit, ein Port, ein Funnel.** `fabian` ist eine Zeile in der Space-Map, kein zweiter Serverprozess. Rule 4 ist architektonisch (P2-G), nicht prozessual. Zusatzargument: Funnel erlaubt nur drei Ports — zwei Prozesse würden diesen Vorrat ohne Gegenwert verbrauchen. Damit ist offene Entscheidung 3 aus dem P2-Handover geschlossen. |
| **H** | Request-Log | **JSON-Zeilen auf stderr, journald ist die Ablage.** Kein eigenes Logfile, keine Rotation im Code, kein Log-Verzeichnis im Repo. Zwei Ereignisarten (`ev="tool"`, `ev="http"`), Feld-Whitelist in §3. Beide laufen durch `TokenScrubbingFilter`. |
| **I** | `/health` | Bleibt unauthentifiziert und flach. **Genau ein neues Feld: `uptime_s`** (Integer). Begründung: der Disconnected-Runbook muss von außen unterscheiden können „Dienst läuft durch" vs. „Dienst ist gerade neu gestartet", ohne SSH. Weiterhin **keine** Space-Namen, Pfade, Item-Zahlen, Hostnamen. |
| **J** | systemd | Zwei System-Units (`sharefyx-mcp.service`, `sharefyx-backup.service` + `.timer`), `User=savefyx`. Im Repo stehen sie mit **Platzhaltern** (`__REPO_ROOT__`, `__DATA_ROOT__`, `__ALLOWED_HOSTS__`, `__VENV__`); `install_units.sh` ersetzt sie aus einer **gitignorierten** `phase3_edge/local.env`. Grund ist nicht Geheimhaltung (der Hostname steht ohnehin in CT-Logs), sondern Maschinenunabhängigkeit: der Kollege oder eine zweite VM sollen dasselbe Repo benutzen können. |
| **K** | Backup | **`git bundle` + Timer + verifizierter Restore im selben Lauf.** Ein Restore, den nie jemand ausgeführt hat, ist kein Backup. Ziel ist Konfiguration (`SHAREFYX_BACKUP_DIR`), kein Literal im Skript. Off-site ist **nicht** in P3. Bonus, der zu Hard Rule 2 passt: `.index.sqlite3` und `.write.lock` sind gitignored — das Bundle enthält damit ausschließlich die Wahrheit, nie die Ableitung. |
| **L** | Ops-Skripte | Bash, aber **über Python getestet**: `phase3_edge/tests/` legt Wegwerf-Git-Repos an und ruft die Skripte auf. Kein Netz, nie der echte `DATA_ROOT`. `pytest.ini` wird erweitert. |
| **M** | Token-Rotation | **Abschlussschritt der Phase**, nicht Nebenwirkung. Beide Token wurden während des Aufbaus über mehrere Kanäle gereicht; nach bestandener Abnahme werden sie neu ausgegeben. Die Reihenfolge **Token → Export → `systemctl restart` → Connector-URL** gehört in den Runbook: wer den Restart vergisst, bekommt 401 und sucht am falschen Ende. |
| **N** | Berührungsfläche | P3 darf in `phase2_mcp/` **genau anfassen**: `mcpserver/config.py`, `mcpserver/logging_setup.py`, `mcpserver/app.py`, `mcpserver/credentials.py`, `scripts/serve.py` — und **ein neues Modul** `mcpserver/request_log.py` anlegen. **Nicht** anfassen: `tools.py`, `permissions.py`, `auth.py`, `asgi.py`, `server.py`, `storage/*`. Ein Änderungsbedarf dort ist ein Befund für den Nikinger, keine Aufgabe. |

**Zu P3-N, weil es beim Bauen juckt:** Das Access-Log für 401er entsteht **nicht** in `asgi.py`,
sondern in einer eigenen ASGI-Hülle um die Wurzel-App (§3.3). Damit bleibt der einzige Codepfad,
der Token auflöst, in P3 unverändert — und ein Fehler im Logging kann die Auth nicht kaputt
machen.

---

## §1 Architektur

### 1.1 Der Weg eines Requests nach P3

```
Claude (Web/Desktop/Mobile) in zwei Accounts
   │  POST https://<node>.<tailnet>.ts.net/mcp/<token>
   ▼
Tailscale-Funnel-Relay          — leitet weiter, entschlüsselt NICHT (§0.4)
   ▼
tailscaled auf der VM           — TLS-Terminierung hier, Zertifikat liegt hier
   │  http://127.0.0.1:8765/mcp/<token>
   ▼
AccessLogASGI                    mcpserver/request_log.py   ← NEU in P3
   ▼
Starlette-Wurzel-App             mcpserver/app.py
   ├── GET /health   → status, service, version, uptime_s
   └── Mount("/mcp") → TokenPathASGI          (unverändert aus P2)
                           ▼
                       FastMCP-App (stateless)
                           ├── ToolCallLogMiddleware   ← NEU in P3
                           └── Tools                    (unverändert aus P2)
                                   ▼
                              storage.Store             (unverändert seit P1)
```

Alles unterhalb von `TokenPathASGI` ist in dieser Phase **read-only Betrachtungsgegenstand**.

### 1.2 Was P3 anlegt

```
phase3_edge/
  CLAUDE.md                     # Phase-Head, L1-Card, Modultabelle, Runbooks
  SESSIONS_ARCHIVE.md           # leer angelegt, L1-Card, newest-first-Hinweis
  local.env.example             # Vorlage; local.env selbst ist gitignored
  systemd/
    sharefyx-mcp.service
    sharefyx-backup.service
    sharefyx-backup.timer
  scripts/
    install_units.sh
    export_space_map.py
    backup_data_root.sh
    restore_check.sh
    diagnose.sh
  tests/
    __init__.py
    test_units.py
    test_backup_scripts.py

phase2_mcp/mcpserver/
    request_log.py              # NEU — das einzige neue Modul in mcpserver/
phase2_mcp/tests/
    test_request_log.py         # NEU
```

**Bewusste Abweichung vom Muster der Phasen 1 und 2, benannt statt versteckt:** `phase3_edge/`
ist **kein Python-Paket**. Es gibt kein `pyproject.toml`, keinen Paketnamen. Der Code, den P3
schreibt, ist Servercode und gehört deshalb nach `mcpserver`; `phase3_edge/` hält Units,
Ops-Skripte, deren Tests und die Doku. `scripts/dev_install.sh` verträgt das bereits — die
Schleife prüft `if [ -f "$pkg_dir/pyproject.toml" ]` und überspringt das Verzeichnis
lautlos. **Nichts an `dev_install.sh` ändern.**

---

## §2 Secrets und Deployment

### 2.1 Der Weg der Space-Map in den Dienst

```
issue_token.py --space niklas       → Keyring:  {sha256: "niklas", …}
        │                             (Quelle der Wahrheit bleibt der Keyring)
        ▼
export_space_map.py                 → JSON auf stdout, nichts auf Platte
        │
        │  python phase3_edge/scripts/export_space_map.py \
        │      | sudo systemd-creds encrypt --name=spaces - /etc/sharefyx/spaces.cred
        ▼
/etc/sharefyx/spaces.cred           (verschlüsselt, root:root 0600)
        │  LoadCredentialEncrypted=spaces:/etc/sharefyx/spaces.cred
        ▼
$CREDENTIALS_DIRECTORY/spaces       (tmpfs, nur für diesen Dienst sichtbar)
        ▼
credentials.py :: load_space_map()
```

**Warum die Pipe und keine Zwischendatei:** So entsteht der Klartext nie auf der Platte. Das ist
derselbe Reflex, der in P2 zweimal verletzt wurde (Screenshot, Chat-Zitat) — hier wird er in die
Kommandozeile eingebaut, statt in eine Ermahnung.

### 2.2 Änderung in `credentials.py` (die einzige)

Anker: `credentials.py :: load_space_map()`, direkt unter den Konstanten
`KEYRING_SERVICE = "nikinger-space"` / `KEYRING_KEY_SPACES = "spaces"`.

```python
CREDENTIAL_NAME = "spaces"

def credential_path() -> Path | None:
    """Pfad der von systemd bereitgestellten Space-Map, oder None außerhalb eines Dienstes.

    systemd setzt $CREDENTIALS_DIRECTORY nur für Units mit LoadCredential*; im
    interaktiven Betrieb (issue_token.py, Tests, mcp_smoke.py) ist die Variable nicht
    gesetzt und der Keyring bleibt der Weg.
    """

def load_space_map() -> dict[str, str]:
    """Credentials-Verzeichnis zuerst, Keyring als Fallback."""
```

**Härte-Anforderungen:**
- Fehlt die Datei trotz gesetztem `$CREDENTIALS_DIRECTORY`, wird **auf den Keyring
  zurückgefallen** und eine `warning` geloggt — nicht geworfen. Ein Dienst, der wegen eines
  Deployment-Fehlers gar nicht startet, ist schwerer zu diagnostizieren als einer, der 401
  liefert und es ins Log schreibt.
- Ist der Inhalt kein JSON-Objekt aus `str → str`, wird **geworfen**. Eine kaputte Map ist kein
  Fallback-Fall, sondern ein Fehler.
- `keyring` bleibt ausschließlich in diesem Modul importiert (P2-Regel, unverändert).

### 2.3 `phase3_edge/scripts/export_space_map.py`

`--help`, kein Argument nötig. Liest `credentials.load_space_map()` **aus dem Keyring**
(explizit, nicht über die neue Verzweigung — sonst exportiert das Skript im Dienstkontext sich
selbst), schreibt kompaktes JSON auf **stdout** und eine Zeile „N Einträge exportiert, keine
Tokens enthalten" auf **stderr** (Hard Rule 7). Kein Schreibzugriff, keine Datei, kein `--out`.

---

## §3 Das Request-Log

### 3.1 Format

Eine JSON-Zeile je Ereignis auf stderr, Logger `sharefyx.request`, `propagate=False`, eigener
Handler mit `JsonLineFormatter`. Die Menschen-Logs (uvicorn, fastmcp, Warnungen) bleiben
unverändert lesbar — nur dieser eine Logger ist maschinenlesbar.

```
{"ts":"2026-07-27T09:12:33.481Z","ev":"tool","tool":"search_items","space":"niklas","ms":37,"ok":true}
{"ts":"2026-07-27T09:12:41.902Z","ev":"tool","tool":"update_item","space":"niklas","ms":12,"ok":false,"err":"conflict"}
{"ts":"2026-07-27T09:13:02.118Z","ev":"http","method":"POST","path":"/mcp/<redacted>","status":401,"ms":1}
```

**Feld-Whitelist — was rein darf:**
`ts` · `ev` · `tool` · `space` · `ms` · `ok` · `err` · `method` · `path` · `status`

**Was niemals rein darf, mit Begründung:**

| Verboten | Warum |
|---|---|
| Das Token, auch teilweise | R5, zwei dokumentierte Vorfälle in P2 |
| Item-Titel, Bodies, Snippets | Das Log ist Betriebsdaten, nicht Inhalt — und fremde Inhalte sind laut Rule 4 Daten, keine Logzeilen |
| Fehler**meldungen** | `map_storage_error()` baut Texte wie `conflict: itm_… wurde geändert (…)` — die enthalten IDs und potenziell Titel. Ins Log geht **nur die Klasse** in `err` |
| Item-IDs | Für Betriebsdiagnose ohne Nutzen, für ein Leck ausreichend |

`err` ist auf die bekannten Klassen beschränkt: `conflict`, `item_not_found`, `write_denied`,
`invalid`, `internal`. Alles Unbekannte wird `internal`.

### 3.2 Tool-Ebene

`mcpserver/request_log.py`:

```python
LOGGER_NAME = "sharefyx.request"
ERROR_CLASSES: dict[type[Exception], str]      # Storage-/Tool-Fehler → Klassenname

class JsonLineFormatter(logging.Formatter): ...
def log_event(**fields: object) -> None: ...
def classify_error(exc: BaseException) -> str: ...

class ToolCallLogMiddleware(Middleware):
    """Misst Dauer und Ergebnis jedes Tool-Aufrufs. Kennt keine Argumente und keine
    Ergebnisse — nur Name, Space, Dauer, Erfolg, Fehlerklasse."""
    async def on_call_tool(self, context, call_next): ...
```

Der Space kommt aus `context.current_principal()` und wird defensiv geholt: wirft es `AuthError`
(darf im regulären Pfad nicht passieren), steht `space: null` in der Zeile statt eines Absturzes.
**Das Logging darf einen Tool-Aufruf nie zum Scheitern bringen** — `call_next` läuft in
`try/finally`, der Log-Schreibvorgang selbst in einem eigenen `try/except Exception`.

`[VERIFY]` **V3 — Importpfad und Signatur der FastMCP-Middleware.** Dokumentiert ist
`fastmcp.server.middleware.Middleware` mit Hooks der Form `on_call_tool(context, call_next)` und
`context.message.name`; FastMCP 3.4.3 hat dafür ausdrücklich ein Doku-Rezept ergänzt
(„audit/event-record recipe for tool-call middleware"). Registrierung über
`mcp.add_middleware(...)` in `app.py :: create_app()`, **nicht** in `server.py`.

**Fallback, falls die Middleware-API abweicht:** Die sechs registrierten Tool-Funktionen in
`server.py :: build_mcp()` bei der Registrierung umwickeln — gleiche Felder, gleiche Zeilen,
ohne `tools.py` anzufassen. Dann ist `server.py` ausnahmsweise mit betroffen; das ist **ein
Befund für den Session-Block**, keine stille Ausweitung von P3-N.

### 3.3 HTTP-Ebene

```python
class AccessLogASGI:
    """Umschließt die Wurzel-App. Misst Dauer, fängt den Status aus dem
    http.response.start-Event ab, loggt Methode, Pfad und Status. Kein Body, keine Header."""
    def __init__(self, app) -> None: ...
    async def __call__(self, scope, receive, send) -> None: ...
```

Eingebaut in `serve.py`, **nicht** in `create_app()` — damit die bestehenden `test_app.py`-Tests
unverändert gegen die nackte App laufen und das Access-Log separat testbar bleibt.

Der Pfad wird **vor** dem Loggen durch dieselbe Regex geschickt, die `TokenScrubbingFilter`
benutzt (`logging_setup.py :: _TOKEN_SEGMENT_RE`). Diese Regex wird dafür aus
`logging_setup.py` importiert, **nicht kopiert** — zwei Kopien derselben Schutzregel sind
schlimmer als eine.

### 3.4 Was das Log beantworten können muss

Die Felderliste ist nicht Geschmackssache, sie folgt aus vier Fragen, die im Betrieb wirklich
auftreten:

1. *Kommt überhaupt etwas an?* → `ev="http"`
2. *Ist es mein Account oder der des Kollegen?* → `space`
3. *Ist der Uplink langsam oder der Store?* → `ms` je Tool
4. *Klopft jemand Fremdes?* → `status: 401` mit `<redacted>`

Frage 3 ist zugleich die Messgrundlage für **D6**: `search_items` ist der Kandidat für die
SQL-Filterung. P3 baut das Messgerät, P4+ entscheidet mit Zahlen.

---

## §4 Steps (sequenziell, je ein Commit)

Jeder Step endet mit grünem `pytest` (gemockt, **kein Netz, kein echter `DATA_ROOT`, kein echter
Tunnel**), aktualisierter Modul-Tabelle im Phase-Head und aktualisiertem
`## Session stopped`-Block — **im selben Commit** (Hard Rule 8). Ab dem zweiten Block läuft
`scripts/rotate_session_block.sh phase3_edge`, nie von Hand.

### Step 0 — Haushalt, Verifikationsdurchlauf, Umgebungsinventar

Kein Feature-Code. Bei **B** ist „nichts zu tun" ein zulässiges und zu meldendes Ergebnis; bei
**A** und **C** nicht.

**A · Doku-Drift schließen** (Quelle: `PHASE2_CLOSEOUT_HANDOVER.md` §6, plus §0.4 dieses Plans):

1. Root-`CLAUDE.md`, **R5**: „OAuth 2.1 + DCR ist **Phase 5**" → **Phase 4** (ROADMAP-Korrektur
   vom 2026-07-25).
2. Root-`CLAUDE.md`, **R4**: datierte Ergänzung zu Tailscale Funnel (§0.4 dieses Plans).
3. Root-`CLAUDE.md`, „Current state": aktive Phase auf **P3**, `down:` auf
   `phase3_edge/CLAUDE.md` umhängen. `[VERIFY]`: der Drive-Snapshot vom 2026-07-24 nennt dort
   noch Phase 1 — der reale Stand kann bereits P2 sagen.
4. `ROADMAP.md` und `phase2_mcp/CLAUDE.md`, Abschnitt „Scope"/„DRIN": das
   **`[VERIFY]` hinter „`fastmcp` über Streamable HTTP" entfernen**. Wörtlicher Suchstring:
   `fastmcp` über Streamable HTTP `[VERIFY]`. Der Marker ist live widerlegt.
5. `ROADMAP.md`, Header-Card `down:`: `phase2_mcp_plan.md` und `phase3_edge_plan.md` ergänzen
   (heute steht dort nur `phase1_storage_plan.md`).
6. `ROADMAP.md`, P3-Zeile: Status ⬜ → 🔄; **Verzeichnisspalte prüfen** — die Tabelle nennt für
   P3 nur `phase3_edge/` ohne Paketnamen, das ist nach §1.2 **korrekt und bleibt so**.
7. `docs/INDEX.md`: P2 wandert von „Active phase" nach „Completed phases" (🔄 → 📗), neuer
   Abschnitt „Active phase (3 — Exposure & Betrieb)", und die fehlende Zeile für
   `PHASE2_CLOSEOUT_HANDOVER.md` kommt dazu:
   ```
   - [docs/concepts/PHASE2_CLOSEOUT_HANDOVER.md](./concepts/PHASE2_CLOSEOUT_HANDOVER.md) — 📕 ~11KB · Abschluss-Handover P2→P3: Status, Delta seit dem P1-Handover, offene Entscheidungen für die Exposure-Phase, [VERIFY]-Bilanz V1–V9
   ```

**B · Verifikationsdurchlauf:**

- Alle `up:`/`down:`-Ziele auflösbar? Jede `.md` mit Indexzeile?
- `find . -name "*.md" -not -path "./.agents/*" -not -path "*/.pytest_cache/*" -size +40k` —
  jeder Treffer muss 📕/📦 sein. Bekannt und erlaubt: `phase2_mcp_plan.md` (~46 KB),
  `phase2_mcp/SESSIONS_ARCHIVE.md` (~38 KB).
- **`git status` sauber, und `docs/test-results/` existiert tatsächlich nicht.** Dieser Punkt ist
  nicht rhetorisch: genau diese Aussage stand schon einmal als erledigt in der Doku, während die
  Datei noch im Arbeitsverzeichnis lag. Prüfen, nicht glauben.
- `pytest -q` → **133 grün** als Ausgangsbasis. Weicht die Zahl ab, ist das ein Befund vor dem
  ersten Commit, keine Kleinigkeit.

**C · Umgebungsinventar** (alles `[VERIFY]`, Ergebnisse tabellarisch in den Session-Block):

```
python --version                       # ≥3.10
which python && echo "$VIRTUAL_ENV"    # exakter venv-Pfad für ExecStart
pip show fastmcp | head -2             # installierte Version → P3-D
keyring --list-backends                # welches Backend V5 real bestätigt hat
systemctl --version | head -1          # ≥250 für systemd-creds
command -v systemd-creds && systemd-creds has-tpm2
tailscale version && tailscale status  # eingeloggt? welcher Node-/Tailnet-Name?
df -T /home/savefyx/savefyx-data       # ext4 (P1-Bedingung für flock)
command -v cloudflared                 # falls vorhanden → Rückbau in Step 6
```

**Done when:** alle Prüfpunkte beantwortet (auch mit „nichts zu tun"), `pytest` grün, ein Commit,
Bericht an den Nikinger mit der Inventartabelle.

---

### Step 1 — `phase3_edge/`-Gerüst und Konfiguration

**Dateien:** `phase3_edge/CLAUDE.md`, `phase3_edge/SESSIONS_ARCHIVE.md`,
`phase3_edge/local.env.example`, `phase3_edge/tests/__init__.py`, `.gitignore`-Ergänzung,
`pytest.ini`, `mcpserver/config.py`, `mcpserver/app.py`, `scripts/serve.py`.

**`pytest.ini`** — wörtlicher aktueller Inhalt:
```
[pytest]
testpaths = phase1_storage/tests phase2_mcp/tests
```
wird zu
```
[pytest]
testpaths = phase1_storage/tests phase2_mcp/tests phase3_edge/tests
```

**`.gitignore`**: `phase3_edge/local.env` ergänzen. `local.env.example` wird committet und
enthält ausschließlich Platzhalter — **keinen** echten Hostnamen, **kein** Token.

**`config.py`** — Anker: die Konstanten `DEFAULT_HOST` / `DEFAULT_PORT` / `DEFAULT_LOG_LEVEL`
und `load_settings()`:

```python
@dataclass(frozen=True, kw_only=True)
class Settings:
    data_root: Path
    host: str = DEFAULT_HOST
    port: int = DEFAULT_PORT
    log_level: str = DEFAULT_LOG_LEVEL
    allowed_hosts: tuple[str, ...] = ()     # NEU — SPACE_ALLOWED_HOSTS, kommagetrennt
```
Parsing: trennen an `,`, `strip()`, leere Einträge verwerfen. Leere oder fehlende Variable →
leeres Tupel. **Kein Default auf einen echten Hostnamen**, dieselbe Logik wie bei
`SPACE_DATA_ROOT`.

**`app.py`** — Anker: `create_app(*, settings, resolver, store, allowed_hosts=None)`. Neu:
```python
hosts = list(allowed_hosts) if allowed_hosts else (list(settings.allowed_hosts) or None)
mcp_app = mcp.http_app(path="/", stateless_http=True, allowed_hosts=hosts)
```
Der explizite Parameter gewinnt; danach die Settings; sonst FastMCPs eigener Default. Der
Docstring erhält einen Satz dazu.

**`serve.py`** — unverändert bis auf den durchgereichten Wert: `--allowed-host` bleibt
`action="append"`, `default=None`.

**`phase3_edge/CLAUDE.md`** (L1-Card, `up: ../CLAUDE.md`, `down:` auf den Plan und
`SESSIONS_ARCHIVE.md`): Scope, harte Regeln inklusive **P3-N (Berührungsfläche)** und
**P3-B (`127.0.0.1`)**, Modul-Status-Tabelle mit den Steps 0–7, Rotationsregel **mit
Skriptverweis**, und die zwei Runbook-Platzhalter (werden in Step 6/7 gefüllt).

**Tests** (`phase2_mcp/tests/test_config.py`, `test_app.py`):
- `test_allowed_hosts_defaults_to_empty`
- `test_allowed_hosts_parses_comma_list`
- `test_allowed_hosts_strips_whitespace_and_drops_empties`
- `test_create_app_prefers_explicit_allowed_hosts_over_settings`
- `test_create_app_uses_settings_allowed_hosts`

**Done when:** `pytest` grün; `./scripts/dev_install.sh` läuft unverändert durch (überspringt
`phase3_edge/` korrekt); Indexzeilen für die zwei neuen `.md` im selben Commit.

---

### Step 2 — Request-Log

**Dateien:** `mcpserver/request_log.py` (neu), `mcpserver/logging_setup.py`, `mcpserver/app.py`,
`scripts/serve.py`, `phase2_mcp/tests/test_request_log.py` (neu).

Inhalte wie §3. In `logging_setup.py :: configure_logging()` kommt genau ein Block dazu, der den
Logger `sharefyx.request` mit eigenem Handler, `JsonLineFormatter`, `TokenScrubbingFilter` und
`propagate = False` einrichtet. `_TOKEN_SEGMENT_RE` wird **exportiert**, nicht dupliziert.

**Tests:**
- `test_json_line_is_valid_json`
- `test_tool_event_has_tool_space_and_duration`
- `test_tool_event_error_carries_class_not_message` — der Text
  `conflict: itm_… wurde geändert` darf in keiner Logzeile stehen
- `test_tool_event_never_contains_item_title` — legt ein Item mit dem Titel
  `ZZZ-MARKER-TITLE` an, ruft alle sechs Tools, prüft den kompletten Logpuffer auf das Marker-Wort
- `test_http_event_redacts_token_segment`
- `test_http_event_logs_401_status`
- `test_logging_failure_does_not_break_tool_call` — Handler wirft, Tool liefert trotzdem
- `test_request_logger_does_not_propagate_to_root`

`test_tool_event_never_contains_item_title` ist der wichtigste Test dieses Steps. Er prüft nicht
eine Implementierung, sondern eine Zusage.

**Done when:** `pytest` grün; ein manueller Lauf von `mcp_smoke.py` zeigt auf stderr JSON-Zeilen
mit plausiblen Millisekunden; die Größentabelle aus P2 bleibt unverändert.

---

### Step 3 — Credentials über systemd

**Dateien:** `mcpserver/credentials.py`, `phase3_edge/scripts/export_space_map.py`,
`phase2_mcp/tests/test_credentials.py`, `README.md`.

Inhalte wie §2. **Keine Änderung** an `issue()`, `revoke()`, `hash_token()`, `generate_token()`.

**Tests** (alle mit `monkeypatch` auf `$CREDENTIALS_DIRECTORY` und einem Fake-Keyring; **nie**
der echte Keyring):
- `test_load_space_map_prefers_credentials_dir`
- `test_load_space_map_falls_back_when_credentials_dir_unset`
- `test_load_space_map_falls_back_when_credential_file_missing`
- `test_load_space_map_raises_on_malformed_credential`
- `test_export_writes_json_to_stdout_and_note_to_stderr`
- `test_export_contains_no_plaintext_token` — erzeugt ein Token über einen Fake-Keyring, prüft,
  dass es in der Ausgabe nicht vorkommt

**Doku im selben Commit:** `README.md`, Abschnitt „Token ausgeben, rotieren, widerrufen" bekommt
den vollständigen Vierschritt aus P3-M — inklusive des Satzes, dass ein vergessener
`systemctl restart` als 401 erscheint.

**Done when:** `pytest` grün; `[VERIFY]` V4 und V5 im Session-Block beantwortet.

---

### Step 4 — systemd-Units

**Dateien:** `phase3_edge/systemd/sharefyx-mcp.service`, `phase3_edge/scripts/install_units.sh`,
`phase3_edge/local.env.example`, `phase3_edge/tests/test_units.py`.

```ini
[Unit]
Description=Sharefyx MCP-Server (Phase 2 Adapter, Phase 3 Betrieb)
Documentation=file://__REPO_ROOT__/phase3_edge/CLAUDE.md
After=network-online.target tailscaled.service
Wants=network-online.target

[Service]
Type=exec
User=savefyx
Group=savefyx
WorkingDirectory=__REPO_ROOT__
Environment=SPACE_DATA_ROOT=__DATA_ROOT__
Environment=SPACE_HOST=127.0.0.1
Environment=SPACE_PORT=8765
Environment=SPACE_LOG_LEVEL=INFO
Environment=SPACE_ALLOWED_HOSTS=__ALLOWED_HOSTS__
LoadCredentialEncrypted=spaces:/etc/sharefyx/spaces.cred
ExecStart=__VENV__/bin/python __REPO_ROOT__/phase2_mcp/scripts/serve.py
Restart=on-failure
RestartSec=5
NoNewPrivileges=true
PrivateTmp=true
ProtectSystem=strict
ProtectHome=read-only
ReadWritePaths=__DATA_ROOT__
ProtectKernelTunables=true
ProtectControlGroups=true
RestrictAddressFamilies=AF_INET AF_INET6 AF_UNIX
MemoryDenyWriteExecute=true
SystemCallFilter=@system-service

[Install]
WantedBy=multi-user.target
```

`[VERIFY]` **V9 — `ProtectHome=read-only` gegen `ReadWritePaths`.** Der `DATA_ROOT` liegt unter
`/home`. `ReadWritePaths` soll den Unterpfad wieder schreibbar machen; wenn der erste Write
scheitert, ist der Fallback `ProtectHome=false` **mit einer datierten Notiz im Phase-Head**, warum
gelockert wurde. Nicht stillschweigend ändern.

Zweiter Fallstrick, vorab benannt: `ProtectSystem=strict` macht auch `/etc` read-only. Der
Dienst schreibt dort nichts — aber `git` im `DATA_ROOT` braucht eine benutzbare
Git-Identität (`user.name`/`user.email`). Die liegt in `~/.gitconfig` (unter `ProtectHome=read-only`
lesbar) oder im `DATA_ROOT` selbst. Beim ersten Write-Test prüfen, ob ein Commit real entsteht.

**`install_units.sh`:** liest `phase3_edge/local.env`, ersetzt die vier Platzhalter, schreibt
nach `/etc/systemd/system/`, `daemon-reload`, `enable --now`. Bricht ab, wenn `local.env` fehlt
oder ein Platzhalter unersetzt bleibt. **Legt keine Credential-Datei an** — das ist bewusst ein
manueller Schritt des Nikingers (§2.1).

**Tests** (`phase3_edge/tests/test_units.py`, reines Textparsen, kein systemd nötig):
- `test_unit_restarts_on_failure`
- `test_unit_loads_credential_encrypted`
- `test_unit_binds_loopback_only` — `SPACE_HOST=127.0.0.1`, nirgends `0.0.0.0`
- `test_unit_has_no_secret_shaped_value` — Regex `[A-Za-z0-9_-]{32,}` über alle
  `Environment=`-Werte; Platzhalter und Pfade fallen nicht darunter, ein versehentlich
  eingetragenes Token schon
- `test_unit_placeholders_are_unresolved_in_repo` — im Repo steht `__REPO_ROOT__`, nicht der
  echte Pfad
- `test_install_script_refuses_without_local_env`

`test_unit_has_no_secret_shaped_value` ist die billigste Versicherung gegen den Vorfall, der in
P2 zweimal passiert ist.

**Done when:** `pytest` grün; die Unit ist **noch nicht** auf der VM installiert — das ist Step 7.

---

### Step 5 — Backup und Restore-Nachweis

**Dateien:** `phase3_edge/scripts/backup_data_root.sh`, `phase3_edge/scripts/restore_check.sh`,
`phase3_edge/systemd/sharefyx-backup.service`, `sharefyx-backup.timer`,
`phase3_edge/tests/test_backup_scripts.py`.

`backup_data_root.sh`:
1. `set -euo pipefail`, Parameter über Umgebung (`SHAREFYX_DATA_ROOT`, `SHAREFYX_BACKUP_DIR`,
   `SHAREFYX_BACKUP_KEEP` mit Default `14`).
2. `git -C "$DATA_ROOT" bundle create "$BACKUP_DIR/sharefyx-data-<ISO-UTC>.bundle" --all`
3. `git bundle verify` auf das eben erzeugte Bundle — schlägt es fehl, wird die Datei gelöscht
   und mit Exit ≠ 0 abgebrochen. Ein unverifiziertes Bundle ist schlimmer als keins, weil es
   Sicherheit vortäuscht.
4. Retention: die ältesten über `KEEP` hinaus löschen, nach Namen sortiert (ISO-Zeitstempel
   sortiert lexikografisch korrekt).
5. Ausgabe: eine JSON-Zeile auf stdout (Hard Rule 7), Fortschritt auf stderr.

`restore_check.sh`: klont das jüngste Bundle in ein `mktemp -d`, vergleicht
`git rev-parse HEAD` sowie `git rev-parse HEAD^{tree}` mit dem Original und räumt auf. Exit ≠ 0
bei Abweichung.

**Der Timer ruft beides auf** (`sharefyx-backup.service` mit zwei `ExecStart=`-Zeilen bzw.
`ExecStartPost=`). Begründung: ein Restore-Test, der einen eigenen Timer hätte, wäre der erste,
den man beim Aufräumen deaktiviert.

`sharefyx-backup.timer`: `OnCalendar=daily`, `Persistent=true` (nachholen, wenn die VM aus war),
`RandomizedDelaySec=900`.

**Bewusst akzeptiert, damit es niemand als Bug meldet:** Das Bundle enthält nur committete
Historie. Läuft es exakt während eines Writes, fehlt der letzte Commit und ist im nächsten Lauf
enthalten. Kein Locking, kein `flock` gegen `.write.lock` — die Alternative wäre, dass ein Backup
einen Tool-Aufruf blockiert.

**Tests** (`phase3_edge/tests/test_backup_scripts.py`, alle gegen `tmp_path`, nie gegen den
echten `DATA_ROOT`):
- `test_backup_creates_verifiable_bundle`
- `test_backup_fails_and_cleans_up_on_corrupt_bundle`
- `test_backup_retention_keeps_newest_n`
- `test_backup_emits_single_json_line_on_stdout`
- `test_restore_check_matches_head_and_tree`
- `test_restore_check_detects_divergence` — manipuliertes Bundle → Exit ≠ 0
- `test_scripts_have_no_hardcoded_paths` — Regex auf `/home/savefyx` in beiden Skripten

**Done when:** `pytest` grün; beide Skripte laufen in einem Wegwerf-Repo durch.

---

### Step 6 — Runbooks, Diagnose, Cloudflare-Rückbau

**Dateien:** `phase3_edge/scripts/diagnose.sh`, `phase3_edge/CLAUDE.md`,
`phase2_mcp/CLAUDE.md`, `README.md`.

`diagnose.sh` prüft **in dieser Reihenfolge** und gibt genau eine Diagnose plus einen
Handlungssatz aus:

| # | Prüfung | Bei Fehlschlag heißt das |
|---|---|---|
| 1 | `systemctl is-active sharefyx-mcp` | Dienst tot → `journalctl -u sharefyx-mcp -n 50` |
| 2 | `curl -sf http://127.0.0.1:8765/health` | Dienst läuft, antwortet nicht → Port belegt oder Start hängt |
| 3 | `tailscale status` | Node offline → Uplink oder tailscaled |
| 4 | `tailscale funnel status` | Funnel aus → `tailscale funnel --bg 8765` |
| 5 | `curl -sf https://<host>/health` | Lokal ok, öffentlich nicht → **siehe Fallstrick unten** |
| 6 | `journalctl -u sharefyx-mcp --since -1h \| grep '"status":401' \| wc -l` | Nur Rauschen oder ein falsches Token |

**Runbook „Connector zeigt Disconnected"** im Phase-Head, als Entscheidungsbaum entlang dieser
sechs Zeilen. Er enthält den dokumentierten Tailscale-Fallstrick namentlich:

> **`funnel status` sagt „on", aber öffentlich hängt der TLS-Handshake.** Symptom: aus dem
> Tailnet antwortet `curl` sofort, von außen bleibt die Verbindung nach dem ClientHello stehen.
> Ursache in fast allen berichteten Fällen: das **`funnel`-Attribut fehlt im `nodeAttrs`-Block
> des Tailnet-Policy-Files**. Der lokale Status weiß davon nichts.

**Cloudflare-Rückbau:** Ist `cloudflared` installiert (Step 0 C), wird es **deaktiviert und
deinstalliert** — zwei parallele Wege nach außen sind ein Diagnoseproblem, kein Fallback. Der
Abschnitt „Runbook Quick-Tunnel-Probe" und „Cloudflare-Voraussetzungen" in
`phase2_mcp/CLAUDE.md` wird **ersetzt** durch einen dreizeiligen Verweis: Quick Tunnel war der
P2-Nachweis, der Betriebsweg ist ab P3 Tailscale Funnel, Details in `phase3_edge/CLAUDE.md`.
Cloudflare Named Tunnel bleibt als **dokumentierter Ausweichweg** in einem Absatz stehen
(Voraussetzung: eigene Domain in Cloudflares DNS) — für den Fall, dass Funnel ausfällt.

**Done when:** `diagnose.sh` läuft auf der VM durch (auch mit absichtlich gestopptem Dienst),
Runbook steht, `phase2_mcp/CLAUDE.md` enthält keine Anleitung mehr, die zu einem zweiten Weg
nach außen führt.

---

### Step 7 — Live-Abnahme (führt der Nikinger aus, nicht Claude Code)

Claude Code liefert die Befehlsfolge und wertet die Ergebnisse aus; alles, was den echten
`DATA_ROOT`, den echten Keyring, die echten Token oder die Claude-Accounts berührt, führt der
Nikinger selbst aus.

**Runbook „Inbetriebnahme", einmalig:**

```
# 0) Tailnet-Voraussetzungen (Admin-Konsole, einmalig)
#    MagicDNS an · HTTPS-Zertifikate an · nodeAttrs: "funnel" für diesen Node
tailscale status                       # Node-Name und Tailnet-Name notieren

# 1) Funnel dauerhaft einschalten
tailscale funnel --bg 8765
tailscale funnel status                # muss den Node-Namen und Port 443 zeigen

# 2) Konfiguration eintragen
cp phase3_edge/local.env.example phase3_edge/local.env
#    REPO_ROOT, DATA_ROOT, VENV, ALLOWED_HOSTS=<node>.<tailnet>.ts.net

# 3) Token für beide Spaces ausgeben (je einmal anzeigen, sicher notieren)
python phase2_mcp/scripts/issue_token.py --space niklas
python phase2_mcp/scripts/issue_token.py --space fabian

# 4) Space-Map verschlüsselt bereitstellen — ohne Klartext auf Platte
sudo mkdir -p /etc/sharefyx
python phase3_edge/scripts/export_space_map.py \
  | sudo systemd-creds encrypt --name=spaces - /etc/sharefyx/spaces.cred
sudo chmod 600 /etc/sharefyx/spaces.cred

# 5) Units installieren und starten
sudo phase3_edge/scripts/install_units.sh
systemctl status sharefyx-mcp

# 6) Erreichbarkeit
curl -s http://127.0.0.1:8765/health
curl -s https://<node>.<tailnet>.ts.net/health

# 7) Connector in beiden Accounts
#    https://<node>.<tailnet>.ts.net/mcp/<token>
```

**Abnahmematrix** — jede Zeile mit Beleg (Ausgabe oder Screenshot **ohne Token**):

| # | Prüfung | Erwartung |
|---|---|---|
| 1 | `/health` von außen | `{"status":"ok",…,"uptime_s":…}` |
| 2 | Connector `niklas` | Ein Read und ein Write erfolgreich |
| 3 | Connector `fabian` | Ein Read und ein Write erfolgreich, **eigener Space** |
| 4 | Cross-Space | `fabian` sieht `niklas` gewrappt und darf dort nicht schreiben |
| 5 | `list_spaces` bei leerem `fabian` | Eigener Space erscheint mit `item_count: 0` (B1-Fix) |
| 6 | **Reboot-Test** | VM neu starten, ohne Handgriff: Connector funktioniert, URL unverändert |
| 7 | **Kill-Test** | `sudo systemctl kill -s KILL sharefyx-mcp` → binnen 10 s wieder `ok` |
| 8 | Request-Log | `journalctl -u sharefyx-mcp` zeigt je Tool-Aufruf Name, Space, `ms` |
| 9 | **Token-Grep** | `journalctl -u sharefyx-mcp --since <Start> \| grep -F "<token>"` → **leer** |
| 10 | Titel-Grep | Ein Item mit markantem Titel anlegen, danach im Log suchen → **leer** |
| 11 | Fremdzugriff | `curl https://<host>/mcp/falsch` → 401, Logzeile mit `<redacted>` |
| 12 | Backup-Timer | `systemctl list-timers sharefyx-backup` zeigt einen Lauf |
| 13 | **Restore-Nachweis** | `restore_check.sh` grün, HEAD identisch |
| 14 | Größenbudget | `search_items` gegen den echten Bestand — geerbtes `[VERIFY]` V8 aus P2 |

**Abschluss, in dieser Reihenfolge:**
1. Beide Token rotieren (`--revoke` + neu), exportieren, `systemctl restart`, Connector-URLs in
   beiden Accounts aktualisieren (P3-M).
2. Abnahmeprotokoll `docs/concepts/P3_ABNAHME_<YYYY-MM-DD>.md` mit L1-Card, Prüfmatrix, Belegen
   und Indexzeile — Konvention aus P2.
3. `ROADMAP.md` P3 auf ✅, `docs/INDEX.md` und Phase-Head nachziehen.

**Done when:** 14 von 14 bestanden, Token rotiert, Protokoll geschrieben.

---

## §5 Akzeptanzkriterien der Phase

1. **Die Connector-URL überlebt einen VM-Reboot unverändert** und funktioniert danach ohne
   menschlichen Handgriff.
2. **Beide Accounts haben einen stehenden Connector**; jeder sieht beide Spaces und schreibt nur
   in seinen (Rule 4 unter echten Zwei-Nutzer-Bedingungen, erstmals).
3. `systemctl kill -s KILL` → Dienst binnen 10 s wieder gesund.
4. **Das Request-Log beantwortet die vier Fragen aus §3.4** und enthält über den gesamten
   Abnahmelauf weder Token noch Titel noch Body — per `grep` belegt, nicht behauptet.
5. Ein Fremdzugriff erscheint als 401-Zeile mit `<redacted>`.
6. **Backup und Restore sind beide gelaufen**, HEAD identisch.
7. `pytest` grün: 133 aus P1/P2 plus die neuen, ohne Netz, ohne Keyring, ohne echten `DATA_ROOT`,
   ohne echten Tunnel.
8. **Kein Secret und kein Maschinenzustand im Repo:** keine `.cred`-Datei, keine `local.env`,
   kein echter Hostname in einer committeten Unit (`test_unit_placeholders_are_unresolved_in_repo`).
9. Doku-Pflichten aus §6 erfüllt — im jeweiligen Step-Commit, nicht nachgereicht.

---

## §6 Doku-Pflichten (Hard Rule 8)

| Datei | Was |
|---|---|
| `docs/INDEX.md` | Zeilen für `docs/concepts/phase3_edge_plan.md`, `phase3_edge/CLAUDE.md`, `phase3_edge/SESSIONS_ARCHIVE.md`, `PHASE2_CLOSEOUT_HANDOVER.md`, später `P3_ABNAHME_*.md`; P2-Block auf 📗/📦; neuer Abschnitt „Active phase (3)" |
| Root-`CLAUDE.md` | R5-Korrektur (OAuth = P4), **R4-Ergänzung zu Funnel (§0.4)**, „Current state" auf P3, `down:` umhängen |
| `ROADMAP.md` | P3 auf 🔄 bzw. ✅; `down:`-Liste ergänzen; `[VERIFY]` hinter „fastmcp über Streamable HTTP" entfernen; unter „Zurückgestellt aus P2" den MCP-Revisions-Eintrag auf den **Trigger** statt das Datum umstellen (P3-E) |
| `README.md` | „Token ausgeben, rotieren, widerrufen" um Export/Restart erweitern; kurzer Abschnitt „Betrieb" (Unit, Timer, `diagnose.sh`); Architekturdiagramm: Cloudflare → Tailscale Funnel |
| `phase2_mcp/CLAUDE.md` | Quick-Tunnel-Runbook durch Verweis ersetzen; `[VERIFY]`-Marker im Scope entfernen; Notiz zu `SPACE_ALLOWED_HOSTS` und `request_log.py` |
| `phase3_edge/CLAUDE.md` | Phase-Head: Scope, P3-A–P3-N in Kurzform, Modultabelle Steps 0–7, Rotationsregel mit Skriptverweis, beide Runbooks, Absatz **„Warum der Hostname nicht geheim, aber trotzdem nicht im Repo ist"**, Absatz **„Was Funnel an R4 ändert und was nicht"** |

---

## §7 Was P3 explizit NICHT tut

Neue Tools · Löschen · OAuth (P4) · REST/UI (P5) · D6 · Migration auf die MCP-Revision
2026-07-28 · Monitoring, Alerting, Uptime-Checks von außen · VPS-Migration · Rate-Limiting ·
feingranulare Lese-Rechte · Änderungen an `tools.py`/`permissions.py`/`auth.py`/`asgi.py`/
`storage/*` · Off-site-Backup.

Wer während P3 anfängt, eines dieser Themen „schon mal vorzubereiten": **stop**. Der häufigste
Weg, eine Phase zu versenken, ist das Vorziehen der nächsten.

---

## §8 Bekannte Risiken und `[VERIFY]`-Register

**Risiken**

1. **Die Erreichbarkeit hängt jetzt an Tailscale.** Fallen die Funnel-Relays aus, zeigt Claude
   „Disconnected", und P3 hat per Scope kein Monitoring. Gegenmittel: der Runbook trennt
   „unser Dienst" von „deren Infrastruktur" in zwei Zeilen, und Cloudflare Named Tunnel bleibt
   als dokumentierter Ausweichweg beschrieben.
2. **Der stille Funnel-Fehlschlag** (lokal ok, öffentlich TLS-Hänger, fehlendes `nodeAttrs`)
   kostet ohne Vorwissen einen Abend. Deshalb steht er namentlich im Runbook, bevor er auftritt.
3. **Der Pfad-Token wird dauerhaft.** Mit einer stabilen Adresse steht er permanent in zwei
   Claude-Accounts, und der Hostname ist über Certificate-Transparency-Logs auffindbar. Die
   Entropie (256 Bit) trägt das; die Angriffsfläche wächst trotzdem von „eine Stunde" auf
   „bis P4". Das ist das stärkste Argument dafür, P4 direkt anzuschließen — und der Grund für
   die Rotation in P3-M.
4. **Mobilfunk-Uplink.** Funnel-Verkehr läuft über Tailscale-Relays; das kostet Latenz und
   Volumen. `[VERIFY]` V12: Datenlimit des RUT X50.
5. **Stiller Bibliotheks-Sprung.** `>=3.4,<3.5` hätte 3.4.3 unter den laufenden Dienst gezogen
   und dessen Host-Guard-Verhalten mitgebracht. Gegenmittel: P3-D.
6. **Rotation ohne Restart.** Neues Token, alte Credential im tmpfs → 401. Steht als eigener
   Schritt im Runbook, weil der Fehler wie „Connector kaputt" aussieht.
7. **journald-Volumen.** Ein stabiler Hostname zieht Scanner an; jede 401 ist eine Zeile.
   `journalctl --disk-usage` gehört in `diagnose.sh`; `SystemMaxUse=` bleibt Systemvoreinstellung.
8. **Sandbox-Direktiven vs. Git-Writes.** `ProtectHome`/`ProtectSystem` können den Commit im
   `DATA_ROOT` brechen. Der erste Write-Test nach dem Unit-Start ist deshalb Pflicht, nicht Kür.

**`[VERIFY]`-Register** (bei Ausführung auflösen und im Session-Block beantworten)

| # | Was | Wo im Plan |
|---|---|---|
| V1 | Repo-Stand: 133 Tests grün, `git status` sauber, `docs/test-results/` real weg, Indexzeilen vollständig | Step 0 B |
| V2 | Installierte `fastmcp`-Version; greift der Host/Origin-Guard in dieser Version, und braucht es `allowed_hosts` überhaupt noch? | P3-D, Step 1 |
| V3 | FastMCP-Middleware: Importpfad, Hook-Signatur `on_call_tool(context, call_next)`, `context.message.name` | §3.2, Step 2 |
| V4 | `systemd-creds` vorhanden, systemd ≥ 250, TPM2 oder Host-Key | §2.1, Step 3 |
| V5 | Welches Keyring-Backend die VM real benutzt (bestimmt den Fallback-Pfad) | Step 0 C, Step 3 |
| V6 | Exakter venv-Pfad und Python-Version für absolute `ExecStart`-Pfade | Step 0 C, Step 4 |
| V7 | Tailscale: Version, Funnel im genutzten Plan verfügbar, MagicDNS an, HTTPS-Certs an, `nodeAttrs: funnel` gesetzt, Node- und Tailnet-Name | Step 7 |
| V8 | Welcher `Host`-Header bei uvicorn ankommt, wenn Funnel proxyt — bestimmt den Wert von `SPACE_ALLOWED_HOSTS` | Step 1, Step 7 |
| V9 | `ProtectHome=read-only` + `ReadWritePaths` erlaubt Writes und Git-Commits im `DATA_ROOT` | Step 4 |
| V10 | Größenbudget gegen echte Daten, sobald `fabian` Items hat (geerbtes V8 aus P2) | Step 7, Zeile 14 |
| V11 | MCP-Revision 2026-07-28 ist am 28.07. final geworden — ändert sich Claudes Verhalten gegenüber einem 2025-11-25-Server? Beobachten, **nicht** migrieren | P3-E |
| V12 | Datenlimit des Mobilfunk-Uplinks | Risiko 4 |

---

## §9 Was nach P3 offen bleibt (für den Closeout-Handover)

- **P4 (OAuth)** — der Seam steht seit P2, das Argument dafür ist mit Risiko 3 stärker geworden.
- **D6** — jetzt mit Messdaten aus dem Request-Log entscheidbar statt nach Gefühl.
- **MCP 2026-07-28** — Trigger: erstes `fastmcp`-Release mit Support.
- **Lese-Rechte zwischen Spaces** — Seam existiert, Policy fehlt weiterhin bewusst.
- **Off-site-Backup und Monitoring** — beides bewusst außerhalb von P3, beides ohne Termin.
