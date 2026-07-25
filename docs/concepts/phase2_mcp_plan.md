---
status: plan (ausführungsreif)
purpose: Phase 2 — MCP-Server. Entscheidungen P2-A–P2-N gelockt, Steps 0–7 sequenziert, Namen fixiert. Direkt an Claude Code übergebbar.
read-when: Ausführung von Phase 2; NICHT bei Session-Start anderer Phasen
detail: L2
up: ../../phase2_mcp/CLAUDE.md
down:
  - ./phase1_storage_plan.md              # Contract §1/§2, Entscheidungen A–H
  - ./PHASE1_CLOSEOUT_HANDOVER.md         # Herkunft der Entscheidungen D1–D6
updated: 2026-07-25
---
# Phase 2 — MCP-Server
## Implementierungsplan für Claude Code

> **Author:** Browser-Planungssession, 2026-07-25 (Nikinger + Claude).
> **Audience:** Claude Code. Der Plan ist ausführungsreif — Entscheidungen sind gelockt,
> Schritte sequenziert, Namen fixiert. **Nichts hier muss neu hergeleitet werden.**
> **Drift-Konvention:** Alles, was gegen den echten Repo-Stand oder eine externe Bibliothek
> geprüft werden muss, ist **`[VERIFY]`** markiert — bei Ausführung verifizieren, nie als
> gesichert übernehmen. Der Planungschat hatte **keinen Zugriff auf den Repo-Stand nach dem
> P1-Abschluss** (nur auf einen Drive-Snapshot vom 2026-07-24 22:26 UTC). Deshalb gibt es hier
> **keine Zeilennummern**, sondern Funktions-Anker (`datei.py :: funktion()`). Trage die realen
> Zeilennummern beim ersten Lesen in deine Step-Notizen ein, nicht in diesen Plan.
> **Doc-Layers gilt:** jede neue `.md` bekommt eine L1-Header-Card und eine Zeile in
> `docs/INDEX.md` — **im selben Commit**.

---

## §0 Mission, Scope, gelockte Entscheidungen

### 0.1 Mission

**Claude kann lesen und schreiben — lokal, ohne Tunnel.** Phase 2 ist ein *dünner Adapter* über
dem in P1 bewiesenen Storage-Kern. Sie fügt drei Dinge hinzu, die P1 bewusst nicht hatte:
**Transport** (Streamable HTTP), **Identität** (Token → Space) und **Autorisierung**
(eigener Space schreibbar, fremde read-only).

**Bauprinzip-Erinnerung:** Der Server ist dumm. P2 enthält **keine AI**, keine Embeddings, keine
Zusammenfassungen. Die Tools reichen Store-Ergebnisse durch, formatieren sie token-sparsam und
entscheiden über Rechte. Mehr nicht. Wer hier ein LLM einbauen will → **stop**.

**Der eigentliche Härtetest der Phase ist nicht MCP, sondern Rule 4:** ein Codepfad, über den
ein fremder Space beschrieben werden kann, existiert nach dieser Phase nicht — auch nicht
versehentlich, auch nicht über `get()`.

### 0.2 Was P2 als gegeben übernimmt (nicht neu herleiten)

| Was | Wo es im Wortlaut steht |
|---|---|
| Frontmatter-Schema, Verzeichnislayout, Statusvokabular | `docs/concepts/phase1_storage_plan.md` §1 |
| `Item` · `ItemSummary` · `SpaceInfo` · `SearchResult` · `IndexStats` | `phase1_storage/storage/models.py` |
| `Store`-Signaturen | `phase1_storage/storage/store.py`, Plan §2 |
| Fehlertypen inkl. `ConflictError.current` | `phase1_storage/storage/errors.py` |
| Entscheidungen A–H (P1) | P1-Plan §0 |
| Rahmenentscheidungen R1–R6 | Root-`CLAUDE.md`, „Current state" |
| Herkunft von D1–D6 | `docs/concepts/PHASE1_CLOSEOUT_HANDOVER.md` |

**Scope laut `ROADMAP.md`, Phase 2 — DRIN:** Streamable HTTP, Token→Space-Auflösung, sechs Tools
(`list_spaces`, `search_items`, `get_item`, `create_item`, `update_item`, `append_to_item`),
`<untrusted_content>`-Wrapping fremder Bodies, Token-Budget-Disziplin im Listing.
**DRAUSSEN:** Löschen, MCP Resources, MCP Prompts, OAuth, öffentliche Erreichbarkeit.
**Ergänzung dieser Planungssession:** `/health` kommt vor (war P3) — fünf Zeilen, und der
Quick-Tunnel-Test am Phasenende braucht es ohnehin.

### 0.3 Entscheidung gegen die Präferenz des Nikingers: OAuth bleibt hinter P3

Der Nikinger hat OAuth-Vorziehen gewünscht, „außer ausdrückliche Empfehlung dagegen". **Hier ist
die ausdrückliche Empfehlung dagegen.** Drei Gründe, in absteigender Härte:

1. **OAuth ist in P2 nicht testbar.** Der Flow läuft über Anthropics Backend: Redirect auf
   `https://claude.ai/api/mcp/auth_callback`, danach ruft Anthropic `/token` von außen auf.
   Ein Server ohne öffentliche Erreichbarkeit kann den Flow nicht einmal durchlaufen — und
   öffentliche Erreichbarkeit **ist** Phase 3. OAuth in P2 hieße: P3 vorziehen und P2 dahinter
   verstecken.
2. **Die Metadaten hängen an der finalen URL.** Das `resource`-Feld der Protected Resource
   Metadata muss exakt der URL entsprechen, die der Nutzer in Claude eingibt — inklusive Pfad.
   Ein Cloudflare *Quick* Tunnel vergibt bei jedem Start eine neue Zufalls-Subdomain. Du würdest
   den Connector nach jedem Neustart neu registrieren. Das ist kein Lerneffekt, das ist Strafe.
3. **Drei Unbekannte gleichzeitig.** Neuer Server + neuer Tunnel + neuer Auth-Flow, und Claude
   meldet im Fehlerfall „Couldn't reach the MCP server" ohne Diagnose. Genau dagegen ist die
   Build-Reihenfolge der ROADMAP geschrieben.

**Gegenvorschlag, der den Wunsch trotzdem erfüllt** (in `ROADMAP.md` einzutragen, Step 0):

- **Reihenfolge ändern, nicht Phase 2 aufblähen:** OAuth wandert von „P5, ganz am Ende" auf
  **„direkt nach P3"**. Die Web-UI rutscht dahinter. Begründung: der Pfad-Token soll kurz leben,
  und die UI ist die Phase, die laut ROADMAP unter Druck wegfallen darf.
- **P2 baut den Seam, nicht die Implementierung.** Die Auth-Schicht dieser Phase ist bewusst
  austauschbar (P2-F): `SpaceResolver` liefert einen `Principal`, egal ob der aus einem
  Pfad-Token oder aus einem OAuth-Access-Token stammt. Der OAuth-Umbau berührt **keine** Zeile
  Tool-Code. Das ist die Investition, die das Vorziehen billig macht.

> Wenn der Nikinger das anders sieht, ist es eine Nachricht — aber dann wird P3 (Tunnel) vor
> dem Auth-Teil dieser Phase gebaut, nicht parallel dazu.

### 0.4 Gelockte Entscheidungen (P2-A – P2-N)

| # | Thema | Festlegung |
|---|---|---|
| **A** | Bibliothek | **`fastmcp` (PrefectHQ), `>=3.4,<3.5`**, exakt gepinnt in `phase2_mcp/pyproject.toml`. **Nicht** das offizielle `mcp`-SDK direkt (v1.x ist seit Juni 2026 im Maintenance-Modus, v2.0 ist Beta und benennt `FastMCP`→`MCPServer` um). `mcp` kommt nur transitiv mit. `[VERIFY]` aktuelle 3.4.x-Version bei Ausführung. |
| **B** | Protokollversion | Ziel ist die **finale Spec 2025-11-25**. **`stateless_http=True` ab Tag 1** — nicht als Skalierungsoption, sondern als Sicherheitsbedingung (siehe P2-D und §8, Risiko 1). Die Revision **2026-07-28** (Sessions weg, `Mcp-Method`/`Mcp-Name`-Header Pflicht) wird **nicht** in P2 adressiert; sie steht als Post-P3-Migrationspunkt in der ROADMAP. |
| **C** | Transport-Layout | Eine Starlette-App als Wurzel: `Route("/health")` + `Mount("/mcp", TokenPathASGI(mcp_app, …))`. Die FastMCP-App wird mit `path="/"` erzeugt; die Lifespan der FastMCP-App wird an die Wurzel-App **durchgereicht** (sonst initialisiert der Session-Manager nicht). |
| **D** | Auth v0 | Token im Pfad: `POST /mcp/<token>`. Auflösung **einmal pro HTTP-Request** in der ASGI-Schicht, Ergebnis in einem `ContextVar`. Jeder Tool-Aufruf prüft zusätzlich, dass der Principal zum Pfad des aktuellen Requests gehört (Guard, fail-closed). |
| **E** | Secrets | OS-Keyring, Service `nikinger-space`, Key `spaces`. Wert: JSON `{"<sha256-hex des Tokens>": "<space>"}`. **Im Keyring liegt kein umkehrbares Geheimnis.** Tokens entstehen ausschließlich über `scripts/issue_token.py`, werden **einmal** auf stdout gezeigt und nie wieder. |
| **F** | Autorisierung | Zwei getrennte Seams: `SpaceResolver` beantwortet *„wer bin ich"*, `Permissions` beantwortet *„wer darf was"*. P2-Policy (`OwnSpaceWritable`): eigener Space lesen+schreiben, alle anderen nur lesen. **Beliebig viele Spaces ab Tag 1** — keine Zwei-Nutzer-Annahme im Code, keine Space-Namen in Produktivcode oder Tests. |
| **G** | Schreib-Tools ohne Ziel-Space | `create_item`, `update_item`, `append_to_item` haben **keinen** `space`-Parameter. Der Ziel-Space ist immer der des Principals. Rule 4 ist damit architektonisch, nicht per `if`. |
| **H** | Fremde Inhalte | Jeder Body **und jeder Snippet** aus einem fremden Space wird in `<untrusted_content space="…">…</untrusted_content>` gewrappt. Vorkommen des Closing-Tags im Inhalt werden vorher entschärft (§3.5). Ohne Escaping ist der Wrap ausbrechbar und damit wertlos. |
| **I** | Ergebnisformate | `list_spaces` / `search_items`: **kompaktes JSON als Text-Content** (`separators=(",",":")`, `ensure_ascii=False`, Daten als ISO-Strings). `get_item`: **der Dateitext** (YAML-Frontmatter + Body) — bei fremden Items mit gewrapptem Body. Kein `structuredContent`/`outputSchema` in P2 `[VERIFY: Claude.ai-Unterstützung nicht dokumentiert]`. |
| **J** | Token-Budget | `search_items`: Default `limit=20`, Hard-Max `100`, `include_archived=False`. Alle drei als Modulkonstanten in `mcpserver/tools.py`, nicht als Literale verstreut. `Store.search()` bleibt unangetastet (`limit=50` im Kern). |
| **K** | Archivieren | Es gibt **kein** siebtes Tool und **kein** Delete. `update_item(status="archived")` wird intern auf `Store.archive()` geroutet — sonst entstünden zwei divergierende Archivzustände (Datei bleibt liegen vs. wandert nach `_archive/`). |
| **L** | P1-Contract-Erweiterung | Drei bewusste, einmalige Änderungen am `storage`-Paket (§4, Step 2): `Store.space_of()`, `Store.get(..., repair_drift=)`, Statusvalidierung. Vom Nikinger am 2026-07-25 freigegeben. **Danach ist der Contract wieder zu.** |
| **M** | OAuth | Nicht in P2 (§0.3). Der Seam wird gebaut, die ROADMAP-Reihenfolge geändert. |
| **N** | Fehlerabbildung | `AuthError` → **HTTP 401 ohne Detail** (nie ein Tool-Fehler, nie „unbekannter Token" vs. „kein Token" unterscheidbar). Storage-Fehler → `ToolError` mit maschinenlesbarem Präfix und handlungsfähigem Text (§3.6). `ConflictError` trägt `current_version` mit — der Client soll ohne Zusatz-Roundtrip mergen können (P1-Entscheidung C). |

---

## §1 Architektur

### 1.1 Der Weg eines Requests

```
Claude (Web/Desktop/Mobile)
   │  POST https://<host>/mcp/<token>       (in P2: http://127.0.0.1:8765/mcp/<token>)
   ▼
Starlette-Wurzel-App                         mcpserver/app.py
   ├── GET /health          → JSONResponse, kein Token, keine Space-Namen
   └── Mount("/mcp")        → TokenPathASGI  mcpserver/asgi.py
                                 │ 1. erstes Pfadsegment abschneiden = credential
                                 │ 2. resolver.resolve(credential) → Principal
                                 │ 3. Principal in ContextVar setzen
                                 │ 4. scope["path"] auf den Rest umschreiben
                                 ▼
                             FastMCP-App (stateless)   mcpserver/server.py
                                 └── Tools              mcpserver/tools.py
                                          │ current_principal()  +  Guard
                                          │ Permissions.can_read/can_write
                                          ▼
                                     storage.Store   (Phase 1, unverändert bis auf §4/Step 2)
```

**Warum der Token in der ASGI-Schicht aufgelöst wird und nicht im Tool:** die Auflösung
passiert genau einmal pro HTTP-Request, bevor irgendein MCP-Code läuft. Ein unbekannter Token
erzeugt eine 401, ohne dass der MCP-Stack ihn je sieht. Das ist auch die Stelle, an der später
ein OAuth-`Authorization`-Header statt eines Pfadsegments gelesen wird — eine Datei, ein Seam.

### 1.2 Modulübersicht `phase2_mcp/mcpserver/`

| Modul | Verantwortung | Kennt |
|---|---|---|
| `config.py` | `Settings` aus Umgebungsvariablen (DATA_ROOT, Host, Port, Log-Level) | nichts |
| `credentials.py` | Keyring-Zugriff, Token-Hashing, Token-Erzeugung | `keyring` |
| `auth.py` | `Principal`, `SpaceResolver`-Protokoll, `KeyringTokenResolver`, `AuthError` | `credentials` |
| `permissions.py` | `Permissions`-Protokoll, `OwnSpaceWritable` | nichts |
| `context.py` | `ContextVar` für den Principal, `current_principal()`, Guard | `auth` |
| `asgi.py` | `TokenPathASGI` — Pfadsegment → Principal → ContextVar → Delegation | `auth`, `context` |
| `tools.py` | die sechs Tools, Serialisierung, Wrapping, Fehlerabbildung | `storage`, `context`, `permissions` |
| `server.py` | `build_mcp(store, permissions)` → FastMCP-Instanz mit registrierten Tools | `fastmcp`, `tools` |
| `app.py` | `create_app(settings, resolver, store)` → Starlette-Wurzel-App | alle |
| `logging_setup.py` | stderr-Logging, **Token-Scrubbing**, Uvicorn-Access-Log aus | nichts |

**Abhängigkeitsrichtung ist strikt:** `tools.py` kennt weder HTTP noch Token. Es kennt einen
Principal und eine Policy. Das ist die Bedingung dafür, dass P4 (REST) und P5 (OAuth) denselben
Kern benutzen können, ohne ihn anzufassen.

---

## §2 Auth und Autorisierung (der Kern der Phase)

### 2.1 Datentypen

```python
# mcpserver/auth.py
@dataclass(frozen=True, kw_only=True)
class Principal:
    space: str          # der eigene Space — Ziel aller Schreiboperationen
    token_hash: str     # sha256-Hex; nur für Guard und gekürzte Logs, nie vollständig geloggt

class AuthError(Exception):
    """Kein oder unbekanntes Credential. Trägt bewusst keine Detailinformation."""

class SpaceResolver(Protocol):
    def resolve(self, credential: str) -> Principal: ...   # wirft AuthError

class KeyringTokenResolver:
    def __init__(self, *, load_map: Callable[[], dict[str, str]] = credentials.load_space_map) -> None: ...
    def resolve(self, credential: str) -> Principal: ...
    def reload(self) -> None: ...      # Map wird beim Start einmal geladen
```

**`load_map` ist injiziert** — genau wie `now_fn` in P1. Unit-Tests reichen ein Dict herein und
fassen **nie** einen echten Keyring an.

**Vergleich:** die Auflösung ist ein Dict-Lookup über `sha256(credential)`, kein
String-Vergleich über das Klartext-Token. Damit gibt es keinen Timing-Kanal über die Tokenlänge
und im Speicher liegt kein Klartext-Geheimnis herum.

### 2.2 Rechte

```python
# mcpserver/permissions.py
class Permissions(Protocol):
    def can_read(self, actor: str, target: str) -> bool: ...
    def can_write(self, actor: str, target: str) -> bool: ...
    def visible_spaces(self, actor: str, all_spaces: Sequence[str]) -> list[str]: ...

class OwnSpaceWritable:
    """P2-Policy: alles lesbar, nur der eigene Space schreibbar."""
    def can_read(self, actor: str, target: str) -> bool: return True
    def can_write(self, actor: str, target: str) -> bool: return actor == target
    def visible_spaces(self, actor, all_spaces): return [s for s in all_spaces if self.can_read(actor, s)]
```

**Erweiterungspfad (Nikinger-Auflage, 2026-07-25) — hier festhalten, damit es später nicht
unmöglich wird:**

- **Beliebig viele Spaces.** Nichts im Code kennt eine Anzahl. Die Keyring-Map ist ein Dict;
  `list_spaces` liest die Spaces aus `Store.list_spaces()`, nicht aus einer Konstante.
  **Space-Namen kommen in keinem Produktivcode und in keinem Test vor** — Tests benutzen
  Fixture-Namen wie `alpha`/`beta`.
- **Spätere Lese-Rechte zwischen Spaces.** `can_read` gibt heute immer `True` zurück, wird aber
  **jetzt schon von jedem Lesepfad aufgerufen** (`list_spaces`, `search_items`, `get_item`).
  Eine spätere `PolicyPermissions` (z. B. Regeln in `<space>/.space.yml`) ist ein Konstruktor-
  Austausch in `app.py`, kein Umbau.
- **Bekannte Grenze, ehrlich benannt:** `Store.search()` filtert nicht nach einer *Liste* von
  Spaces. Solange `can_read` konstant `True` ist, ist die Nachfilterung in `tools.py` ein No-op.
  Sobald echte Lese-Regeln kommen, muss die Filterung **in den Store** (oder in eine Suche je
  sichtbarem Space), sonst stimmen `total` und Paginierung nicht mehr. Das ist ein
  **`[SEAM]`-Kommentar im Code** und ein Eintrag in der ROADMAP, kein stiller Fallstrick.
- **Die ROADMAP sagt heute „Feingranulare Rechte: bewusst nicht auf der Roadmap".** Das bleibt
  richtig für P2 — aber der Satz wird um den Halbsatz ergänzt, dass der Seam existiert und
  warum. Widerspruchsfreiheit vor Bequemlichkeit.

### 2.3 Keyring-Format und Token-Ausgabe

```python
# mcpserver/credentials.py
KEYRING_SERVICE = "nikinger-space"
KEYRING_KEY_SPACES = "spaces"

def generate_token() -> str          # secrets.token_urlsafe(32)  → 256 Bit
def hash_token(token: str) -> str    # sha256-Hexdigest
def load_space_map() -> dict[str, str]
def save_space_map(mapping: dict[str, str]) -> None
def issue(space: str) -> str         # erzeugt, speichert nur den Hash, gibt das Token EINMAL zurück
def revoke(space: str) -> int        # entfernt alle Hashes dieses Space, gibt die Anzahl zurück
```

`phase2_mcp/scripts/issue_token.py`:
`--space <name>` → erzeugt, speichert, schreibt das Token **einmal auf stdout** und einen
Warnhinweis auf **stderr**. `--revoke <name>`, `--list` (zeigt Spaces und gekürzte Hashes, nie
Tokens).

**Doku-Auflage des Nikingers (D10) — im selben Commit wie Step 3, nicht später:**

1. `README.md` bekommt einen Abschnitt **„Token ausgeben, rotieren, widerrufen"**: die drei
   Kommandos, die Aussage *„das Token wird genau einmal angezeigt"*, und was zu tun ist, wenn es
   verloren geht (neu ausgeben, alten Hash entfernen, Connector-URL in Claude aktualisieren).
2. Root-`CLAUDE.md`, Hard Rule 1 bekommt eine **datierte Korrekturnotiz**: der Zugriff läuft über
   `phase2_mcp/mcpserver/credentials.py`, nicht über das nie gebaute `storage/credentials.py`.
   Die Regel selbst bleibt Wort für Wort stehen.
3. `phase2_mcp/CLAUDE.md` bekommt einen Absatz **„Warum nur Hashes im Keyring"**: der Server muss
   ein Token nur *wiedererkennen*, nie *vorzeigen*. Wer diese Eigenschaft aufgibt, um „das Token
   nochmal anzeigen" zu können, macht aus dem Keyring eine Passwortliste.
4. `phase2_mcp/CLAUDE.md` bekommt den Absatz **„Was der Pfad-Token nicht ist"**: kein
   OAuth-Ersatz, kein Schutz gegen Cloudflare (R4), gültig bis P3+1. Mit Verweis auf §0.3.

### 2.4 Der Guard (fail-closed)

`mcpserver/context.py`:

```python
def current_principal() -> Principal          # wirft AuthError, wenn keiner gesetzt ist
def set_principal(p: Principal) -> Token      # von TokenPathASGI benutzt
def assert_principal_matches_request() -> None
```

`assert_principal_matches_request()` liest den aktuellen HTTP-Request über FastMCPs
Dependency (`get_http_request()` `[VERIFY: Importpfad in 3.4.x — dokumentiert ist
fastmcp.server.dependencies.get_http_request; es gibt zusätzlich fastmcp.dependencies.CurrentRequest]`),
zieht das Token-Segment aus dessen Pfad und vergleicht `hash_token(...)` gegen
`principal.token_hash`. Ungleich → `AuthError`.

**Warum diese drei Zeilen wichtig sind:** In FastMCP gab es einen dokumentierten Fehlerfall, in
dem ein Tool im *stateful* HTTP-Modus den Request der **ersten** Anfrage einer Session sieht.
Genau das wäre hier ein stiller Cross-Space-Leak. `stateless_http=True` (P2-B) verhindert die
Ursache; der Guard macht aus einem Rest-Risiko einen lauten Fehler statt einer falschen Antwort.
Kostet einen SHA-256 pro Tool-Aufruf.

---

## §3 Tool-Contract

Alle sechs Tools werden mit `@mcp.tool` registriert, mit **Titel, knapper Beschreibung und
vollständigen Annotations**. Beschreibungen sind kurz — sie liegen in jedem Kontextfenster.

### 3.1 Signaturen und Annotations

| Tool | Parameter | `readOnly` | `destructive` | `idempotent` | `openWorld` |
|---|---|---|---|---|---|
| `list_spaces` | — | ✅ | ❌ | ✅ | ❌ |
| `search_items` | `query?`, `space?`, `type?`, `status?`, `tag?`, `due_before?`, `limit=20`, `offset=0`, `include_archived=False` | ✅ | ❌ | ✅ | ❌ |
| `get_item` | `item_id` | ✅ | ❌ | ✅ | ❌ |
| `create_item` | `type`, `title`, `body=""`, `tags=[]`, `links=[]`, `due?`, `status?` | ❌ | ❌ | ❌ | ❌ |
| `update_item` | `item_id`, `version`, `title?`, `body?`, `status?`, `tags?`, `links?`, `due?`, `type?` | ❌ | ✅ | ❌ | ❌ |
| `append_to_item` | `item_id`, `version`, `text` | ❌ | ❌ | ❌ | ❌ |

`create_item`/`update_item`/`append_to_item` haben **keinen `space`-Parameter** (P2-G).
`update_item` ist `destructive`, weil es Inhalt überschreibt und via `status="archived"`
verschiebt; `append_to_item` ist rein additiv und deshalb nicht.

### 3.2 Semantik im Einzelnen

**`list_spaces()`** → JSON-Liste über `Permissions.visible_spaces(...)`, je Eintrag
`{"name":…,"item_count":…,"writable":true|false}`. `writable` ist genau für den eigenen Space
`true`. Das erspart Claude einen Fehlversuch.

**`search_items(...)`** → ruft `Store.search()` mit durchgereichten Filtern.
`include_archived=False` (Default) setzt `status`-Filterung so, dass archivierte Items nicht
erscheinen; ist `status` explizit gesetzt, gewinnt der explizite Wert.
`limit` wird auf `[1, MAX_LIMIT]` geklemmt (nicht abgelehnt — eine Klemmung ist für ein Modell
brauchbarer als ein Fehler). Ergebnis:
`{"items":[…],"total":…,"limit":…,"offset":…,"truncated":true|false}`.
Je Item: `id, space, type, title, status, due, tags, links, updated, version, snippet`.
Snippets fremder Spaces werden gewrappt (§3.5).

**`get_item(item_id)`** → siehe §3.4. Liefert den **Dateitext**: Frontmatter + Body.

**`create_item(...)`** → `Store.create(space=principal.space, …)`.

**`update_item(...)`** → 1. `Store.space_of(item_id)`, 2. `can_write` prüfen → sonst
`PermissionDenied`, 3. bei `status == "archived"` → `Store.archive(item_id, version=version)`
und **alle anderen Felder ablehnen** (`ValidationError`, Text: erst inhaltlich updaten, dann
archivieren), 4. sonst `Store.update(item_id, version=version, **changes)`.

**`append_to_item(...)`** → analog, dann `Store.append(...)`.

### 3.3 Reihenfolge jeder Tool-Implementierung (immer gleich, keine Ausnahme)

```
1. principal = current_principal()
2. assert_principal_matches_request()
3. Zielraum bestimmen  (Schreibtools/get: Store.space_of(item_id); Suche: Filter)
4. Rechte prüfen       (permissions.can_read / can_write)
5. Store aufrufen
6. Ergebnis formatieren (+ Wrapping bei fremdem Space)
```

Schritt 4 kommt **vor** Schritt 5. Ein Rechtefehler darf den Store nicht erreichen.

### 3.4 `get_item` und die Drift-Reparatur (D3, gelöst)

```python
space = store.space_of(item_id)                       # nur Index, schreibt nichts
own   = permissions.can_write(principal.space, space)
item  = store.get(item_id, repair_drift=own)          # fremder Space ⇒ kein Dateischreibzugriff
```

Damit ist Rule 4 buchstäblich wahr: ein Lesezugriff auf einen fremden Space fasst dort keine
Datei an und erzeugt keinen Commit. Der Index wird trotzdem aktualisiert — der ist Ableitung
(P1-Entscheidung A) und sein Schreiben ist kein Cross-Space-Write.
**Konsequenz, die in `phase2_mcp/CLAUDE.md` gehört:** in fremden Spaces ist `version`
*informativ*, nicht autoritativ. Das ist folgenlos, weil es dort keine Writes gibt.

### 3.5 `<untrusted_content>` — Wrapping und Escaping

```python
UNTRUSTED_OPEN  = '<untrusted_content space="{space}">'
UNTRUSTED_CLOSE = "</untrusted_content>"

def wrap_untrusted(text: str, *, space: str) -> str:
    safe = text.replace("</untrusted_content", "</untrusted_ content")   # exakter Ersatzstring in Step 6 fixieren
    return f'{UNTRUSTED_OPEN.format(space=space)}\n{safe}\n{UNTRUSTED_CLOSE}'
```

**Ohne das Escaping ist der Wrap wertlos:** wer in seine eigene Notiz ein Closing-Tag schreibt,
schließt den Block vorzeitig und alles danach sieht für den Leser wie vertrauenswürdiger
Servertext aus. Das ist die Prompt-Injection, gegen die Rule 4 überhaupt geschrieben wurde.
Es gilt für **Bodies (`get_item`) und Snippets (`search_items`)** gleichermaßen.

### 3.6 Fehlerabbildung (P2-N)

| Ursache | Antwort | Text (Muster) |
|---|---|---|
| kein/unbekanntes Token | **HTTP 401**, leerer Body | — (nie unterscheidbar machen) |
| `ItemNotFound` | `ToolError` | `item_not_found: <id> — prüfe die ID mit search_items` |
| `PermissionDenied` (P2-eigen) | `ToolError` | `write_denied: <space> ist nicht dein Space; du kannst dort nur lesen` |
| `ConflictError` | `ToolError` | `conflict: <id> wurde geändert (deine Version <n>, aktuell <m>, zuletzt <ts>) — lies neu mit get_item und wiederhole` |
| `ValidationError` | `ToolError` | `invalid: <konkreter Grund + erlaubte Werte>` |
| `SpaceNotFound` | `ToolError` | `space_not_found: <name>` |
| unerwartet | `ToolError`, generisch | `internal_error — siehe Serverlog`; Traceback nur nach stderr |

Jede Meldung nennt **den nächsten Schritt**, nicht nur den Zustand. Ein Modell, das
`conflict: …` liest, soll ohne Nachdenken wissen, dass es `get_item` aufrufen muss.

---

## §4 Steps (sequenziell, je ein Commit)

Jeder Step endet mit grünem `pytest` (gemockt, **kein Netz, kein echter `DATA_ROOT`**),
aktualisierter Modul-Tabelle im Phase-Head und aktualisiertem `## Session stopped`-Block —
**im selben Commit** (Hard Rule 8).

### Step 0 — Haushalt und Verifikationsdurchlauf

Kein Feature-Code. „Nichts zu tun" ist bei den Prüfpunkten ein zulässiges Ergebnis und wird
gemeldet; bei A1–A3 ist es keines.

**A · Rotationsregel operationalisieren** (aus dem P1-Closeout-Handover, dort A1–A3):
1. Überschrift des verbliebenen P1-Blocks auf `## Session stopped — 2026-07-25 (…)` bringen.
   `[VERIFY: kann im Abschluss-Chat bereits erledigt sein]`
2. `scripts/rotate_session_block.sh` einchecken, `chmod +x`, für `phase1_storage` laufen lassen.
   Erwartung: Head ~34 KB → ~11 KB, Archiv drei Blöcke newest-first.
   `[VERIFY: existiert der Skripttext schon? Wenn nicht, schreibst du ihn — Anforderungen:
   Blöcke per sed ausschneiden, Reassemblierung mit cmp gegen das Original prüfen, eingefügte
   Blöcke byte-identisch gegenlesen, erst dann schreiben.]`
3. Verweise setzen: Root-`CLAUDE.md` („Doku-Hygiene"), `phase1_storage/CLAUDE.md`
   („Harte Regeln"), `docs/PROMPTS.md` (Prompt 1 und Prompt 3 Punkt 4) nennen künftig den
   Skriptaufruf statt einer Handlungsanweisung. **`docs/DOC_LAYERS_CONVENTION.md` bleibt
   unangetastet** (byte-identische Kopie aus dem Trading-Bot-Repo). **Keine Indexzeile für die
   `.sh`** — `docs/INDEX.md` ist die Karte der `.md`.

**B · Verifikation:**
- Alle `up:`/`down:`-Ziele auflösbar? Jede `.md` mit Indexzeile? (u. a.
  `PHASE1_CLOSEOUT_HANDOVER.md` — `[VERIFY: Indexzeile fehlt im letzten mir bekannten Stand]`)
- `find . -name "*.md" -not -path "./.agents/*" -not -path "*/.pytest_cache/*" -size +40k` —
  jeder Treffer muss 📕/📦 sein.
- `files.rename_for_new_slug()` **entfernen** (samt Test in `test_files.py`); `store.py` benutzt
  `files.move_file()` direkt. Toter Code in der Contract-Fläche ist eine Falle für P4.
- Doku-Drift: der Step-2-Session-Block nennt `rename_for_new_slug()` — eine Zeile mit Datum
  korrigieren.

**C · Festlegungen eintragen (Nikinger-Entscheidungen vom 2026-07-25):**
- **Schreibweisen bleiben, wie sie sind.** `sharefyx` (Repo/Drive), `/home/savefyx/…` (VM),
  `/home/savefyx/dev/savefxy` (Code-Repo-Verzeichnis, Buchstabendreher). Das wird in
  `README.md` **als bewusst eingefroren dokumentiert**, damit es niemand später „repariert" —
  eine Umbenennung bricht Pfade, die P3 in systemd-Units schreibt. Ebenso: `DATA_ROOT` steht auf
  Branch `master`, das Code-Repo auf `main`.
- **`ROADMAP.md`:** Phase-5-Zeile → OAuth rückt **direkt hinter P3**, UI dahinter (§0.3).
  Neuer Abschnitt **„Zurückgestellt aus P2"** mit drei Einträgen:
  (a) **D6** — `Store.search()` liest jede indizierte Datei; Filterung in SQL verschieben ist
  eine Kostenfrage, kein Bug, und gehört ins `storage`-Paket, nicht in einen Adapter.
  (b) **MCP-Revision 2026-07-28** — Sessions entfallen, `Mcp-Method`/`Mcp-Name` werden Pflicht;
  Migration nach P3.
  (c) **Lese-Rechte zwischen Spaces** — Seam existiert (§2.2), Policy fehlt bewusst.
- Root-`CLAUDE.md`, „Current state": aktive Phase auf P2 setzen, `down:` auf
  `phase2_mcp/CLAUDE.md` umhängen.

**Done when:** alle Prüfpunkte beantwortet (auch mit „nichts zu tun"), `pytest` grün,
ein Commit, Bericht an den Nikinger mit den `[VERIFY]`-Ergebnissen.

---

### Step 1 — Paketgerüst `phase2_mcp/`

**Dateien:**
```
phase2_mcp/
  pyproject.toml           # name = "mcpserver", packages = ["mcpserver"]
  CLAUDE.md                # Phase-Head, L1-Card, Modultabelle, Rotationsregel + Skriptverweis
  SESSIONS_ARCHIVE.md      # leer angelegt, L1-Card, newest-first-Hinweis
  mcpserver/__init__.py    # __version__ = "0.1.0"
  mcpserver/config.py
  tests/__init__.py
```

`pyproject.toml` spiegelt `phase1_storage/pyproject.toml` exakt; abweichend nur:
`name = "mcpserver"`, `description`, `packages = ["mcpserver"]`, und
`dependencies = ["storage", "fastmcp>=3.4,<3.5", "keyring>=25"]`
`[project.optional-dependencies] dev = ["pytest", "pytest-asyncio", "httpx"]`
`[VERIFY: exakte 3.4.x-Version und ob pytest-asyncio nötig ist — FastMCP-Tests laufen async]`
`scripts/dev_install.sh` findet das Verzeichnis automatisch (`for pkg_dir in "$repo_root"/phase*_*/`).

`config.py`:
```python
@dataclass(frozen=True, kw_only=True)
class Settings:
    data_root: Path          # SPACE_DATA_ROOT   (Pflicht, kein Default auf den echten Pfad)
    host: str = "127.0.0.1"  # SPACE_HOST
    port: int = 8765         # SPACE_PORT
    log_level: str = "INFO"  # SPACE_LOG_LEVEL
def load_settings(env: Mapping[str, str] | None = None) -> Settings
```
**Kein Secret in `Settings`.** Der Default für `host` ist bewusst `127.0.0.1`: in P2 gibt es
keinen Grund, auf `0.0.0.0` zu lauschen.

**Tests:** `test_config.py` — `test_load_settings_requires_data_root`,
`test_load_settings_defaults`, `test_load_settings_port_invalid_raises`.

**Done when:** `./scripts/dev_install.sh` installiert beide Pakete editierbar,
`from mcpserver import __version__` importiert, `pytest` grün, Indexzeilen für die zwei neuen
`.md` in `docs/INDEX.md` im selben Commit.

---

### Step 2 — P1-Contract-Erweiterungen (freigegeben, einmalig)

Änderungen in `phase1_storage/storage/`. Danach ist der Contract wieder zu.

**2a — Statusvokabular + Validierung (D2).** In `models.py`:
```python
STATUS_VALUES: dict[str, frozenset[str]] = {
    "note": frozenset({"active", "archived"}),
    "task": frozenset({"open", "done", "archived"}),
}
def valid_statuses(item_type: str) -> frozenset[str]
```
In `store.py :: create()` und `store.py :: update()`: unbekannter `type` → `ValidationError`;
`status` außerhalb von `valid_statuses(type)` → `ValidationError` mit Aufzählung der erlaubten
Werte. **Begründung im Docstring:** die CLI hielt das mit `argparse choices` ab; jeder weitere
Adapter (MCP jetzt, REST in P4) wäre ein Eingang daran vorbei. Einmal im Kern statt dreimal
außen.

**2b — `Store.space_of()`.**
```python
def space_of(self, item_id: str) -> str:
    """Space eines Items, ausschließlich über den Index. Schreibt nichts, liest keine Datei.
    Wird von der Autorisierungsschicht (P2) gebraucht, BEVOR entschieden ist, ob ein
    Zugriff überhaupt erlaubt ist."""
```
Implementierung: `index.get_item_row()`, `None` → `ItemNotFound`.

**2c — `repair_drift` (D3).** `store.py :: _reconcile_and_get_row(item_id, *, repair_drift: bool = True)`
und `store.py :: get(item_id, *, repair_drift: bool = True)`.
Bei `repair_drift=False` **und** erkannter Inhaltsänderung: **kein** `_rewrite_version_in_file()`,
**kein** `_commit("drift", …)`. Stattdessen `index.upsert_item(self._conn, fresh)` mit der
Version, die in der Datei steht. Docstring-Ergänzung: *„In fremden Spaces ist `version`
informativ; dort gibt es per Architektur keine Writes."*
Die Default-Werte lassen jedes bestehende Verhalten unverändert — CLI und alle P1-Tests bleiben
gültig.

**Tests** (in `phase1_storage/tests/`):
- `test_store.py::test_space_of_returns_space`
- `test_store.py::test_space_of_unknown_raises_item_not_found`
- `test_store.py::test_get_repair_drift_false_leaves_file_untouched` (mtime + Bytes vergleichen)
- `test_store.py::test_get_repair_drift_false_creates_no_commit` (`git log`-Länge)
- `test_store.py::test_get_repair_drift_true_still_bumps` (Regression auf P1-Verhalten)
- `test_store.py::test_update_rejects_unknown_status`
- `test_store.py::test_create_rejects_unknown_status`
- `test_store.py::test_update_accepts_valid_status_per_type`

**Done when:** alle 70 P1-Tests plus die neuen grün. `phase1_storage/CLAUDE.md` bekommt eine
**datierte Notiz**, dass P2 diese drei Erweiterungen mit Freigabe eingebracht hat — sonst sieht
es später wie stiller Contract-Bruch aus.

---

### Step 3 — Credentials und Token-Ausgabe

**Dateien:** `mcpserver/credentials.py`, `phase2_mcp/scripts/issue_token.py`,
`phase2_mcp/tests/test_credentials.py`. Namen wie in §2.3.

**Härte-Anforderungen:**
- `keyring` wird **nur** in `credentials.py` importiert; alles darüber bekommt Funktionen
  injiziert. Unit-Tests fassen keinen Keyring an.
- `Principal.__repr__` und Log-Ausgaben zeigen höchstens `token_hash[:8]`.
- `issue_token.py` schreibt das Token auf **stdout**, alles andere auf **stderr** (Hard Rule 7).
- `--list` zeigt Spaces und gekürzte Hashes, nie Tokens.

**Doku im selben Commit:** die vier Punkte aus §2.3 (README-Abschnitt, Korrekturnotiz in
Hard Rule 1, zwei Absätze im Phase-Head).

**Tests:** `test_hash_token_is_stable_hex64`, `test_generate_token_length_and_uniqueness`,
`test_issue_stores_only_hash` (die Map enthält das Klartext-Token nirgends),
`test_revoke_removes_all_hashes_of_space`, `test_load_space_map_missing_key_returns_empty`,
`test_save_load_roundtrip_with_fake_backend`.

**Done when:** `pytest` grün; `[VERIFY: Keyring-Backend auf der VM]` — auf einem headless
Ubuntu ohne D-Bus scheitert das SecretService-Backend. Prüfe `keyring --list-backends` und
**melde das Ergebnis dem Nikinger**, statt eine Datei-Fallback-Lösung selbst zu wählen. Der
vorgesehene Produktionsweg ist ohnehin systemd `LoadCredential` in P3.

---

### Step 4 — Auth, Rechte, Request-Kontext

**Dateien:** `mcpserver/auth.py`, `mcpserver/permissions.py`, `mcpserver/context.py`,
`mcpserver/asgi.py`, `mcpserver/logging_setup.py` + Tests.

`asgi.py`:
```python
class TokenPathASGI:
    """Schneidet das erste Pfadsegment als Credential ab, löst es auf, setzt den Principal
    und delegiert an die MCP-App. Antwortet bei fehlendem/unbekanntem Credential mit 401
    ohne Body — die beiden Fälle dürfen von außen nicht unterscheidbar sein."""
    def __init__(self, app, *, resolver: SpaceResolver) -> None: ...
    async def __call__(self, scope, receive, send) -> None: ...
```
Verhalten: nur `scope["type"] == "http"` behandeln, sonst durchreichen. Pfad splitten,
leeres Segment → 401. `resolver.resolve()` → `AuthError` → 401. Erfolg: `set_principal()`,
`scope["path"]` auf `"/" + rest` setzen (und `raw_path` konsistent halten), `finally` den
ContextVar-Token zurücksetzen.

`logging_setup.py`:
```python
def configure_logging(level: str) -> None    # Handler auf stderr, kein Root-Handler auf stdout
class TokenScrubbingFilter(logging.Filter)   # ersetzt /mcp/<segment> durch /mcp/<redacted>
```
**Und: Uvicorn-Access-Log ausschalten** (`access_log=False`). Das Access-Log schreibt die
komplette URL — inklusive Token. Das ist der wahrscheinlichste Weg, wie dieses Projekt sein
Geheimnis verliert, und er kostet ein Keyword-Argument.

**Tests:** `test_auth.py` (`test_resolve_known_token`, `test_resolve_unknown_raises`,
`test_resolve_empty_raises`, `test_principal_repr_hides_token`),
`test_permissions.py` (`test_own_space_writable`, `test_foreign_space_read_only`,
`test_visible_spaces_filters_by_can_read`),
`test_asgi.py` (`test_missing_token_401`, `test_unknown_token_401`,
`test_path_is_rewritten_for_inner_app`, `test_principal_reset_after_request`),
`test_logging.py` (`test_scrubbing_filter_redacts_token_in_message`).

**Done when:** `pytest` grün, kein Netz, kein Keyring.

---

### Step 5 — Server und App

**Dateien:** `mcpserver/server.py`, `mcpserver/app.py`, `phase2_mcp/scripts/serve.py` + Tests.

```python
# server.py
def build_mcp(store: Store, permissions: Permissions, *, name: str = "sharefyx-spaces") -> FastMCP
# app.py
def create_app(*, settings: Settings, resolver: SpaceResolver, store: Store) -> Starlette
```
`create_app` baut:
```python
mcp = build_mcp(store, permissions)
mcp_app = mcp.http_app(path="/", stateless_http=True)      # [VERIFY] Signatur in 3.4.x
app = Starlette(
    routes=[Route("/health", health, methods=["GET"]),
            Mount("/mcp", app=TokenPathASGI(mcp_app, resolver=resolver))],
    lifespan=mcp_app.lifespan,                              # PFLICHT, sonst kein Session-Manager
)
```
`/health` → `{"status":"ok","service":"sharefyx-mcp","version":<mcpserver.__version__>}`.
**Keine Space-Namen, keine Pfade, keine Item-Zahlen** — der Endpunkt ist unauthentifiziert.

`serve.py`: liest `Settings`, baut `Store(settings.data_root)`, `KeyringTokenResolver()`,
startet uvicorn mit `access_log=False`. Optional `--allowed-host` (durchgereicht an
`http_app(allowed_hosts=…)`) — FastMCP prüft `Host`/`Origin` per Default gegen
DNS-Rebinding; hinter einem Tunnel ist der Host **nicht** localhost, und ohne diesen Schalter
scheitert die Quick-Tunnel-Probe in Step 7 mit einer irreführenden Meldung.

**Tests** (ASGI-Testclient, kein echter Port, kein Netz):
`test_app.py::test_health_ok`, `::test_health_leaks_no_space_names`,
`::test_mcp_requires_token`, `::test_tools_list_returns_six_tools`,
`::test_tools_list_annotations_present`,
`::test_principal_isolation_under_concurrency` — **der wichtigste Test der Phase:** zwei
gleichzeitige Tool-Aufrufe mit zwei verschiedenen Tokens müssen zwei verschiedene Spaces sehen.
Wenn dieser Test fällt, ist es kein Testproblem, sondern ein Cross-Space-Leak.

**Done when:** `pytest` grün; `tools/list` zeigt sechs Tools mit Annotations.

---

### Step 6 — Die sechs Tools

**Dateien:** `mcpserver/tools.py` + `phase2_mcp/tests/test_tools.py`.

Konstanten oben im Modul: `DEFAULT_LIMIT = 20`, `MAX_LIMIT = 100`,
`DEFAULT_INCLUDE_ARCHIVED = False`, `UNTRUSTED_OPEN`, `UNTRUSTED_CLOSE`.
Hilfsfunktionen: `wrap_untrusted()`, `summary_to_dict()`, `item_to_filetext()`,
`compact_json()`, `map_storage_error()`.

Reihenfolge in jedem Tool wie in §3.3, ohne Ausnahme. Fehlerabbildung wie §3.6.

**Tests:**
- `test_list_spaces_marks_own_space_writable`
- `test_list_spaces_filters_by_can_read`
- `test_search_defaults_exclude_archived`
- `test_search_explicit_status_wins_over_default`
- `test_search_limit_defaults_to_20`
- `test_search_limit_is_clamped_to_max`
- `test_search_snippet_of_foreign_space_is_wrapped`
- `test_get_item_own_space_returns_plain_filetext`
- `test_get_item_foreign_space_body_is_wrapped`
- `test_wrap_untrusted_escapes_closing_tag`
- `test_get_item_foreign_space_does_not_write_file` (Rule 4, über `repair_drift`)
- `test_create_item_uses_principal_space`
- `test_create_item_has_no_space_parameter` (Signatur-Inspektion — die Regel wird *geprüft*, nicht nur behauptet)
- `test_update_item_foreign_space_denied`
- `test_append_to_item_foreign_space_denied`
- `test_update_item_conflict_message_contains_current_version`
- `test_update_item_status_archived_routes_to_archive` (Datei liegt danach in `_archive/`)
- `test_update_item_status_archived_rejects_other_fields`
- `test_update_item_invalid_status_rejected`
- `test_search_result_size_budget` — 30 Items < 16 KB, 20 Items < 12 KB, misst die
  tatsächlich serialisierten Bytes und schlägt fehl, wenn die Grenze reißt

**Done when:** `pytest` grün; alle sechs Tools über den ASGI-Testclient aufrufbar; die drei
Rule-4-Tests (`foreign_denied` ×2, `foreign_does_not_write`) grün.

---

### Step 7 — Smoke-Test, Messung, Runbook

**Dateien:** `phase2_mcp/scripts/mcp_smoke.py`, README-Abschnitt, Runbook im Phase-Head.

`mcp_smoke.py` — das Gegenstück zu `space_cli.py` aus P1: baut ein temporäres `DATA_ROOT`
(**nie den echten**), legt zwei Fixture-Spaces an, startet die App in-process, verbindet einen
`fastmcp`-Client und fährt ab:
1. `list_spaces` — beide Spaces sichtbar, genau einer `writable`
2. `create_item` ×3 im eigenen Space
3. `search_items` — Treffer, Default-Limit, keine archivierten
4. `get_item` eigen → Klartext; `get_item` fremd → gewrappt
5. `update_item` mit falscher Version → lesbarer Konflikt
6. `append_to_item` → Version +1
7. `update_item(status="archived")` → Datei in `_archive/`
8. `update_item` auf ein fremdes Item → `write_denied`
9. Größenmessung: Bytes je Antwort, Ausgabe als Tabelle
Ausgabe wahlweise Text oder `--json` auf stdout, Logs auf stderr.

**Runbook „Quick-Tunnel-Probe" (führt der Nikinger aus, nicht Claude Code):**
```
1. python phase2_mcp/scripts/issue_token.py --space niklas      # Token einmal notieren
2. SPACE_DATA_ROOT=/home/savefyx/savefyx-data python phase2_mcp/scripts/serve.py \
       --allowed-host '<subdomain>.trycloudflare.com'
3. cloudflared tunnel --url http://127.0.0.1:8765
4. curl https://<subdomain>.trycloudflare.com/health        → {"status":"ok",…}
5. Claude → Settings → Connectors → Add custom connector:
       https://<subdomain>.trycloudflare.com/mcp/<token>
6. Neue Konversation, Connector aktivieren, ein Read und ein Write ausführen.
```
`[VERIFY]` bei Ausführung gegen die aktuelle Anthropic-Doku: Custom Connectors auf **Pro**
ohne Owner-Gate (Stand 2026-07-25 dokumentiert für Free/Pro/Max/Team/Enterprise; Free ist auf
einen Connector begrenzt). **Der Tunnel-Schritt wird nicht committet** — kein Skript, keine
Config, kein Hostname im Repo. Das ist P3.

**Done when:** `mcp_smoke.py` läuft vollständig grün gegen ein temporäres Verzeichnis; die
Größentabelle steht im Session-Block; der Nikinger hat die Quick-Tunnel-Probe durchgeführt und
das Ergebnis gemeldet.

---

## §5 Akzeptanzkriterien der Phase

1. `tools/list` liefert **genau sechs** Tools, jedes mit Titel, Beschreibung und vollständigen
   Annotations.
2. **Rule 4 ist bewiesen, nicht behauptet:** `create_item`/`update_item`/`append_to_item`
   besitzen keinen `space`-Parameter (Signatur-Test), Schreibversuche in fremde Spaces
   scheitern, und ein `get_item` auf einen fremden Space fasst dort keine Datei an.
3. Fremde Bodies und Snippets sind gewrappt, das Closing-Tag ist nicht ausbrechbar.
4. Zwei gleichzeitige Requests mit verschiedenen Tokens sehen verschiedene Spaces.
5. Ein Default-Listing über 20 Items bleibt unter 12 KB, über 30 Items unter 16 KB.
6. Das Token erscheint **nirgends** in stdout, stderr oder Logdateien.
7. `pytest` grün, ohne Netz, ohne Keyring, ohne echten `DATA_ROOT`.
8. Doku-Pflichten aus §6 erfüllt — im jeweiligen Step-Commit, nicht nachgereicht.
9. Quick-Tunnel-Probe durch den Nikinger erfolgreich (ein Read, ein Write über Claude).

---

## §6 Doku-Pflichten (Hard Rule 8)

| Datei | Was |
|---|---|
| `docs/INDEX.md` | Zeilen für `docs/concepts/phase2_mcp_plan.md`, `phase2_mcp/CLAUDE.md`, `phase2_mcp/SESSIONS_ARCHIVE.md`; P1-Block von 🔄 auf 📗/📦 umglyphen; fehlende Zeile für `PHASE1_CLOSEOUT_HANDOVER.md` `[VERIFY]` |
| Root-`CLAUDE.md` | aktive Phase = P2, `down:` umhängen, Korrekturnotiz zu Hard Rule 1 (Pfad von `credentials.py`), Halbsatz zum Rotationsskript |
| `ROADMAP.md` | P2 auf 🔄 bzw. 🟡/✅; OAuth vor die UI; Abschnitt „Zurückgestellt aus P2" (Step 0/C) |
| `README.md` | Abschnitt „Token ausgeben, rotieren, widerrufen"; Notiz zu den drei eingefrorenen Schreibweisen |
| `phase1_storage/CLAUDE.md` | datierte Notiz zu den drei freigegebenen Contract-Erweiterungen |
| `phase2_mcp/CLAUDE.md` | Modultabelle, Steps 0–7 mit Status, Rotationsregel **mit Skriptverweis**, Absätze „Warum nur Hashes im Keyring", „Was der Pfad-Token nicht ist", „`version` in fremden Spaces" |

---

## §7 Was P2 explizit NICHT tut

Löschen · MCP Resources · MCP Prompts · OAuth · Tunnel/systemd/öffentliche Erreichbarkeit ·
REST/UI · Volltextsuche über Bodies · Anhänge · semantische Suche · feingranulare Lese-Rechte
(nur der Seam) · SQL-Filterung in `Store.search()` (D6) · Migration auf die MCP-Revision
2026-07-28.

Wer während P2 anfängt, eines dieser Themen „schon mal vorzubereiten": **stop**. Der häufigste
Weg, eine Phase zu versenken, ist das Vorziehen der nächsten.

---

## §8 Bekannte Risiken und `[VERIFY]`-Register

**Risiken**

1. **Stale Request-Kontext.** In FastMCP kann ein Tool im *stateful* HTTP-Modus den Request der
   ersten Anfrage einer Session sehen. Hier wäre das ein Cross-Space-Leak. Gegenmittel:
   `stateless_http=True` (Ursache), Guard in §2.4 (Symptom), Test in Step 5 (Nachweis). Falls
   der Isolationstest fällt: **nicht weiterbauen**, sondern melden.
2. **Keyring auf headless Ubuntu.** SecretService braucht D-Bus. Wenn `keyring` scheitert, ist
   das ein Ops-Thema für P3 (systemd `LoadCredential`), keine Einladung, ein Token in eine Datei
   zu schreiben. Melden, nicht umgehen.
3. **Token im Pfad landet in jedem Log dazwischen.** Anthropic rät inzwischen ausdrücklich von
   Credentials in Connector-URLs ab, und die MCP-Auth-Spec verbietet Tokens im Query-String.
   Wir bleiben bewusst dabei (R5), mit drei Gegenmaßnahmen: 256-Bit-Entropie,
   Access-Log aus + Scrubbing-Filter, und OAuth direkt nach P3 statt am Ende. Wer den Token in
   ein Log schreibt, hat einen Incident, keinen Bug.
4. **Bibliotheks-Tempo.** `fastmcp` ist aktiv und schnell; die MCP-Revision 2026-07-28 wird am
   28.07.2026 final. Deshalb die exakte Pinnung (P2-A) und die bewusste Nicht-Migration in P2.
5. **Cloudflare sieht Klartext** (R4). Unverändert bewusst akzeptiert. Nur erwähnt, damit es
   niemand in P3 als Entdeckung meldet.

**`[VERIFY]`-Register** (bei Ausführung auflösen und im Session-Block beantworten)

| # | Was | Wo im Plan |
|---|---|---|
| V1 | Repo-Stand nach dem P1-Abschluss: Session-Block-Überschrift, `rotate_session_block.sh`, Indexzeile des Closeout-Handovers | Step 0 |
| V2 | `fastmcp`-Version 3.4.x; Signatur von `http_app(path=…, stateless_http=…, allowed_hosts=…)` | P2-A/B, Step 5 |
| V3 | Importpfad der Request-Dependency (`fastmcp.server.dependencies.get_http_request` vs. `fastmcp.dependencies.CurrentRequest`) | §2.4 |
| V4 | Verhält sich `Mount("/mcp", …)` + Pfad-Umschreibung wie geplant? Fallback: reines ASGI-Prefix-Matching ohne `Mount` | §1.1, Step 5 |
| V5 | Keyring-Backend auf der VM (`keyring --list-backends`) | Step 3 |
| V6 | Python-Version auf der VM ≥ 3.10 (P1 verlangt es bereits) | Step 1 |
| V7 | Custom Connectors auf Claude **Pro** ohne Owner-Gate | Step 7 |
| V8 | Größenbudget gegen echte Beispieldaten (20/30 Items) | Step 6 |
| V9 | Existieren im echten `DATA_ROOT` bereits Space-Verzeichnisse unter anderen Namen? Falls ja: Umbenennung ist **Nikinger-Arbeit** (Verzeichnis **und** `space:`-Feld in jedem Item), nie Claude Code | Step 0, Bericht |
