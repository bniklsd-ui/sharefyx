---
status: snapshot
purpose: Ausführungsreifer Plan Phase 6 — Werkzeug-Ergonomie (patch_item), Dateisystem (Ordner, Sichtbarkeitsstufen, Freigaben, geteilte Spaces, >2 Nutzer), Update-Log/Banner, Bilder als verlinkte Assets
read-when: vor jedem Claude-Code-Step in phase6_shares/ — einmal §0.5 + den eigenen Step, nicht das ganze Dokument
detail: L2
up: ../../phase6_shares/CLAUDE.md
down:
  - ./PHASE5_CLOSEOUT_HANDOVER.md              # Herkunft: §4.1–§4.6, offene Entscheidungen, [VERIFY] V27–V38
  - ./phase5_ui_plan.md                        # P5-A–P5-AE, die diese Phase teilweise revidiert
  - ../../ROADMAP.md                           # P6-Zeile + die zwei korrigierten "Bewusst nicht"-Absätze
  - ../../phase6_shares/ITEM_MOVE_PLAN.md      # [2026-08-13] Zusatzplan zu Step 7: Item-Verschieben (Ordner+Space) + Textfarben — P6-AD–P6-AJ, Abnahmezeilen 25–30, V52–V55
updated: 2026-08-09
---
# Phase 6 — Freigaben, Ordner, Werkzeug-Ergonomie (`phase6_shares/`)

> **Für den ausführenden Sonnet.** Dieses Dokument ist ausführungsreif. Die Entscheidungen in
> §0.5 sind **gelockt** — nicht neu herleiten, nicht „verbessern". Widersprechende Evidenz ist
> ein expliziter Befund für den Nikinger, nie eine stille Abweichung.
>
> **Quelle der Wahrheit ist der Code, nicht dieser Plan.** Dieser Plan wurde am 2026-08-09 im
> Browser gegen den Drive-Snapshot `2026_08_09_sharefyx-main` geschrieben, **nicht** gegen ein
> frisches Arbeitsverzeichnis. Jeder Anker ist ein Funktionsname oder ein Suchstring, keine
> Zeilennummer. Alles, was seit dem Snapshot gedriftet sein kann, trägt `[VERIFY]` (§7).

---

## §0 Rahmen

### 0.1 Mission

**Drei Dinge, in dieser Reihenfolge beweisbar:**

1. Eine arbeitende Claude-Instanz kann eine Drei-Zeilen-Korrektur an einem großen Dokument
   machen, ohne es komplett neu zu schreiben — und ohne es als Antwort komplett zurückzubekommen.
2. Ein Mensch entscheidet pro Item, **wer** es sieht: nur er selbst, er und seine Claude-Instanz,
   oder ausgewählte andere. Und es gibt Orte, an denen mehrere gemeinsam schreiben.
3. Das System verträgt einen dritten Nutzer, ohne dass jemand eine Codezeile ändert.

Alles andere in dieser Phase ist Beiwerk.

### 0.2 Herkunft

| Quelle | Was daraus kommt |
|---|---|
| `PHASE5_CLOSEOUT_HANDOVER.md` §4.1 (F1a/F1b/F2) | Sichtbarkeitsstufen, geteilte Spaces, echte Ordner |
| `PHASE5_CLOSEOUT_HANDOVER.md` §4.2 | `patch_item` — wörtliches Live-Feedback einer arbeitenden Claude-Instanz, 2026-08-08 |
| `PHASE5_CLOSEOUT_HANDOVER.md` §4.3 | Client-Surface-Logging |
| `PHASE5_CLOSEOUT_HANDOVER.md` §4.4 | O2 — `clients`/`token_families` werden nie abgeräumt |
| `PHASE5_CLOSEOUT_HANDOVER.md` §4.5 | Plan-Widerspruch Step 9 vs. §2.6 — hier formal geschlossen (§0.7) |
| `ROADMAP.md`, „Bewusst nicht auf der Roadmap" | Genau die zwei Absätze, die diese Phase widerlegt — Korrektur in §0.7 |
| Nikinger-Antworten, Browser-Planungssession 2026-08-09 | A1–H3 des Fragenkatalogs, plus „Nikinger 1" (Drag & Drop) |

Diese Phase steht in **keiner** Roadmap-Zeile — sie ist ein QoS-Schnitt, entstanden aus echtem
Betrieb. Die Roadmap-Zeile wird in Step 0 nachgetragen, nicht andersherum.

### 0.3 Normative Grundlage

Fortschreibung von `phase5_ui_plan.md` §0.3, ergänzt um das, was P6 neu berührt:

| Quelle | Wofür in P6 |
|---|---|
| **BSI IT-Grundschutz APP.3.1** (Upload-Restriktionen) | Größen-, Typ- und Ablageregeln für Assets **vorab** festgelegt (§1.7), nicht nachträglich |
| **OWASP File Upload Cheat Sheet** | Typprüfung über Magic Bytes statt Endung, zufälliger Dateiname, Ausliefern mit `nosniff` |
| **BSI IT-Grundschutz CON.10** (Re-Authentisierung bei wichtigen Änderungen) | Das Re-Auth-Gate vor jeder rechte-**erweiternden** Änderung (§1.2.5) |
| **OWASP Access Control Cheat Sheet** — „deny by default", „fail securely" | Der Auflösungsalgorithmus in §1.2.3: unbekannter Space ⇒ kein Recht, kaputte `.share.yml` ⇒ kein Recht |
| RFCs aus P4/P5 | unverändert, P6 fasst die Auth-Fläche nicht an |

### 0.4 Externe Lage (Stand 2026-08-09, im Browser recherchiert)

- **`CVE-2026-48710` („BadHost")** — Starlette < 1.0.1, der `Host`-Header wird ungeprüft in
  `request.url` eingebaut; pfadbasierte Autorisierungs-Middleware ist damit umgehbar. MCP-Server
  werden in der Advisory ausdrücklich als besonders exponiert genannt (die MCP-Spec schreibt
  unauthentifizierte Discovery-Endpunkte vor). **Ersteinschätzung dieses Plans:** `create_app()`
  routet über `Mount`/`Route` (roher Scope-Pfad, nicht `request.url.path`) und setzt
  `TrustedHostMiddleware`, sobald `SPACE_ALLOWED_HOSTS` gesetzt ist — beides spricht gegen eine
  Betroffenheit. **Die installierte Version hat aber nie jemand geprüft** → Step 0, `[VERIFY]` V40.
- **`fastmcp`**: aktuelles Stable ist **3.4.6** (2026-08-05). Der Pin `>=3.4,<3.5` bleibt gültig.
  **FastMCP 4 liegt weiterhin nur als Beta vor.** Die MCP-Revision `2026-07-28` bleibt damit
  unverändert eine eigene Mini-Phase **nach** P6 (P5-C gilt fort) — P6 fasst weder Transport noch
  Auth an.
- Anthropic-Connector-Doku: seit 2026-07-28 nicht mehr gegengelesen (`[VERIFY]` V33 aus P5). P6
  ändert die Tool-Fläche (sechs → sieben Tools, neue Parameter, neues Rückgabeformat), damit ist
  V33 **fällig**, nicht optional → Step 0, fortgeführt als V41.

### 0.5 Gelockte Entscheidungen (P6-A – P6-AC)

| # | Thema | Lock | Herkunft |
|---|---|---|---|
| **P6-A** | Phasenschnitt | **Drei Blöcke, ein hartes Gate.** Block A = Werkzeuge, Betrieb, Update-Banner. Block B = Dateisystem. Block C = Bilder. Unter Druck fällt C weg, dann Bs geteilte Spaces — nie Block A. | A1 |
| **P6-B** | Verzeichnis/Paket | `phase6_shares/`, **kein neues Python-Paket** (wie `phase3_edge/`). Neuer Code lebt in `storage`, `mcpserver`, `webui`; `phase6_shares/` trägt `tests/`, `scripts/`, `CLAUDE.md`. Plan: `docs/concepts/phase6_shares_plan.md`. | A2 |
| **P6-C** | Berührungsfläche | **`storage/`, `mcpserver/tools.py`, `mcpserver/permissions.py` sind ausdrücklich AUF.** Das hebt P5-B auf und macht Akzeptanzkriterium 18 der Phase 5 gegenstandslos. Ersatz: P6-D. Weiterhin **tabu**: `mcpserver/asgi.py`, `authserver/{crypto,totp,passwords,resolver,flows}.py` — die Auth-Fläche wird in dieser Phase nicht angefasst (Ausnahme: eine additive Schema-Migration, P6-X). | A1, H2 |
| **P6-D** | Ersatz für den Seam-Beweis | **Charakterisierungstests vor dem Umbau.** Step 4 beginnt mit Golden-File-Tests gegen den heutigen `storage`-Kern (Frontmatter-Round-Trip inkl. unbekannter Felder, Drift-Repair, Konfliktverhalten, Archivpfade, Git-Commit-Messages). Diese Dateien müssen nach dem Umbau **byte-identisch** bleiben. Kein Step-Abschluss in Block B ohne grüne Charakterisierung. | H2 |
| **P6-E** | `patch_item` — Form | `patch_item(item_id, version, edits, return_body=False)`. `edits` ist eine **Liste** von `{old_text, new_text}`, sequenziell angewandt, **alles oder nichts**, ein Versionssprung, ein Git-Commit. Jeder `old_text` muss zum Zeitpunkt seiner Anwendung **genau einmal** im Body vorkommen. | B1 |
| **P6-F** | `patch_item` — Match | **Exakter Byte-Match.** Keine Whitespace-Normalisierung, keine Regex, kein Fuzzy. 0 Treffer ⇒ Fehler; >1 Treffer ⇒ Fehler mit Trefferzahl und den Zeilennummern der ersten beiden Fundstellen — **nie** ein Body-Ausschnitt. | B5 |
| **P6-G** | Konfliktverhalten von `patch_item` | **Wie alle anderen Schreibpfade: `version`-Mismatch ⇒ `ConflictError`, ohne Ausnahme.** Der naheliegende Trick („die Anker passen noch, also patche trotzdem") wäre ein inhaltsverankerter Merge und damit ein Loch in Hard Rule 3. Er wird **als benannter `[SEAM]`** in `store.patch()` dokumentiert und **nicht gebaut**. | B1 (out of the box, bewusst verworfen) |
| **P6-H** | Rückgabeformat der Schreib-Tools | **Alle vier Schreib-Tools** (`create_item`, `update_item`, `append_to_item`, `patch_item`) liefern per Default eine **kompakte Quittung** (§1.5.3). `return_body: bool = False` an jedem von ihnen holt den vollen Dateitext wie bisher. `get_item` bleibt unverändert. | B2, B3 |
| **P6-I** | Teilweises Lesen | **Draußen.** Kein `section=`/Zeilenbereich an `get_item` in P6. Stattdessen misst `ui_budget.py` künftig auch die Antwortgrößen der Tool-Fläche (Step 2) — die nächste Entscheidung bekommt Zahlen statt Bauchgefühl. | B4 |
| **P6-J** | Sichtbarkeitsstufen | Zwei Frontmatter-Werte, Freigaben additiv: `visibility: private` (Default — Eigentümer in der UI **und** dessen eigene Connectoren) und `visibility: human` (**nur** der Eigentümer in der UI, für keinen Agenten sichtbar, nicht freigebbar). „Geteilt" ist keine Stufe, sondern `share_read`/`share_write`. | C1 |
| **P6-K** | Item-Freigaben | Zwei Frontmatter-Listen: `share_read: [<space>, …]` und `share_write: [<space>, …]`. **Item-Schreibfreigaben sind drin** — sie kosten praktisch nichts, weil die Rechteauflösung ohnehin pfadweise gebaut wird (§1.2.3). | C1 |
| **P6-L** | Migration des Bestands | **Alles Bestehende wird `visibility: private`, ohne Freigaben.** Fabian verliert die Sicht auf Niklas' Space und umgekehrt; was geteilt bleiben soll, wandert bewusst in einen geteilten Space. Ein Migrationsreport listet jedes berührte Item. Fabian wird **vorher** informiert (Update-Banner, Block A ist deshalb vor Block B). | C2, H1 |
| **P6-M** | Wer darf Freigaben ändern | **Nur Menschen, nur in der UI, nur mit Re-Auth.** Kein MCP-Tool kann `share_read`/`share_write`/`visibility` setzen — die Felder stehen auf der Verbotsliste von `update_item`. Begründung: das Re-Auth-Gate ist gegen einen Agenten ohnehin kein Beweis (er könnte Inhalte in einen geteilten Space **kopieren**), aber es verhindert die einzige Klasse, die wirklich weh tut: eine injizierte Zeile in einem fremden Dokument, die 200 Items auf einmal freigibt. | C3 |
| **P6-N** | Re-Auth-Regel | **Jede Änderung, die die Menge der Lesenden oder Schreibenden vergrößert, verlangt Re-Auth. Jede Verkleinerung nicht.** Eine Funktion, eine Stelle: `webui/shares.py :: widens()`. Das Verschieben eines Items in einen geteilten Space fällt darunter. | C3 |
| **P6-O** | Wrapping | `<untrusted_content>` gilt unverändert für **alles außerhalb des Home-Space** — auch für geteilte Spaces, in die man selbst schreiben darf. Der Wrap ist eine Herkunftsmarkierung, keine Schreibsperre. | C4 |
| **P6-P** | `visibility: human` | Für die Agentenfläche **vollständig nicht existent**: nicht in `search_items`, nicht in `total`, nicht in `list_spaces`-Zählern. In der UI wird es normal gezählt und angezeigt. Umgesetzt über `Surface` (§1.2.4), nicht über einen Filter an jeder Aufrufstelle. | C5 |
| **P6-Q** | Ordner | **Echte Verzeichnisse.** `folder` wird **aus dem Pfad abgeleitet** und nie ins Frontmatter geschrieben (der Pfad ist bereits Wahrheit; zwei Quellen wären eine Driftquelle). Maximaltiefe **2**, Namen über `files.slugify()`, reserviert: `_archive`, `_assets`. | D1, D2 |
| **P6-R** | Archiv | Unverändert `<space>/_archive/`, **flach** — ein archiviertes Item verliert seinen Ordner. Die Archiv-Neugestaltung (F2 aus dem Handover) bleibt **draußen**. | D2, D3 |
| **P6-S** | D6 / SQL-Filterung | **Draußen, aber gemessen.** `Store.search()` liest weiterhin jede indizierte Datei. Step 2 erweitert `ui_budget.py` um Latenzmessungen für `/api/v1/overview` und `search_items`. | D4 |
| **P6-T** | Ort der Mitgliedschaft | **Datei, nicht Datenbank:** `.share.yml`, gültig in jedem Verzeichnis, in dem sie liegt (Space-Wurzel oder Unterordner). Erfüllt Hard Rule 2, landet automatisch im `git bundle`-Backup, ist im Editor lesbar — und ist **über kein Item-Tool erreichbar**, weil sie keine `.md` ist. | E1 |
| **P6-U** | Hard Rule 4 | **Wird neu gefasst** (Wortlaut in §0.7). Genau **ein** Tool ändert sich: `create_item` bekommt einen optionalen `space`-Parameter mit Default Home-Space. Die anderen Schreibpfade leiten ihr Ziel weiterhin aus der Item-ID ab. | E2 |
| **P6-V** | Verwaltung geteilter Spaces | **CLI in dieser Phase, UI gebaut aber abgeschaltet.** `phase6_shares/scripts/spacectl.py` ist der scharfe Weg. Die UI-Fläche entsteht mit, hängt aber hinter `UiSettings.space_admin_enabled` (Default **aus**) und zeigt einen sichtbar deaktivierten Menüpunkt „Geteilte Spaces verwalten — kommt in Phase 7". Freischaltung ist dann ein Ein-Zeilen-Schnitt in P7. | E3 |
| **P6-W** | Dritter Nutzer | Wird in der Abnahme **echt angelegt** (Space + Konto + Connector) und nach der Abnahme wieder **entfernt** — inklusive dokumentiertem Rückbauweg (`spacectl.py remove-space`). „Erweiterbar" ist kein Abnahmekriterium, ✅ heißt live-verifiziert. | E4 |
| **P6-X** | Update-Log | `docs/UPDATE_LOG.md`, strenges Format (§2.4), serverseitig geparst. Gesehen-Zustand pro Nutzer in `auth.sqlite3` (**Schema 3**, additiv). Kein `localStorage` (P5-V gilt fort). Banner nur in `/ui`, Volltext dauerhaft unter Einstellungen. **`deploy.sh` bricht ab, wenn der oberste Eintrag nicht das Datum des Deploy-Tages trägt** (Override: `SHAREFYX_ALLOW_STALE_UPDATELOG=1`). | G1–G4 |
| **P6-Y** | Assets — Ablage | `<DATA_ROOT>/<space>/_assets/<ast_id>.<ext>`, **im Git-Repo des Datenverzeichnisses** (ein Backup-/Restore-Weg, nicht zwei). Max **5 MiB** je Datei. Referenz im Markdown **relativ**: `![alt](_assets/ast_1a2b3c4d.png)` — bleibt in jedem Editor gültig. | F2, F3 |
| **P6-Z** | Assets — Typen | Erlaubt: **PNG, JPEG, WebP, GIF**. Erkennung über **Magic Bytes**, nie über die Endung. **HEIC/HEIF wird abgelehnt** — ausdrückliche Empfehlung gegen den Nikinger-Wunsch, Begründung §1.7.2. Kein EXIF-Strippen in P6 (dokumentiert, nicht vergessen: **O5**). | F4 (Abweichung) |
| **P6-AA** | Assets — Rechte | Claude darf Assets **referenzieren** (es ist Text), aber **nicht hochladen und nicht löschen**. Ausliefern respektiert dieselbe Rechteauflösung wie das enthaltende Verzeichnis. Kein Löschen von Assets in P6 (**O4**: verwaiste Assets bleiben liegen). | F4 |
| **P6-AB** | Drag & Drop | **Drin, mit Pflicht-Alternative.** Ziehen einer Zeile auf einen Ordner verschiebt; Ablegen einer Bilddatei im Editor lädt hoch und fügt den Link ein. Jede der beiden Gesten hat einen gleichwertigen Knopf-/Menüweg — eine Funktion, die nur per Maus-Geste erreichbar ist, gilt als nicht gebaut. Drag & Drop löst dieselben Re-Auth-Prüfungen aus wie der Knopfweg (P6-N). | Nikinger 1 |
| **P6-AC** | `app.js` | **Aufteilen** in ES-Module unter `webui/static/js/`, weiterhin **ohne Build-Step** (P5-T gilt fort): `app.html` lädt genau ein `<script type="module" src="/ui/static/js/app.js">`. Kein Bundler, kein npm, keine CDN-Quelle (CSP `script-src 'self'`). | H3 |

### 0.6 Was diese Phase NICHT tut

- **Kein Löschen von Items.** `status: archived` bleibt der einzige Weg (F2 unverändert draußen).
- **Kein FastMCP-4-Umstieg, keine MCP-Revision 2026-07-28, kein CIMD/DPoP.** Eigene Mini-Phase.
- **Keine Volltextsuche über Bodies, keine semantische Suche, kein Auto-Tagging.** Kernprinzip.
- **Kein Realtime/WebSocket, keine Mobilversion** (P5-W gilt fort).
- **Keine SQL-Filterung im Store** (P6-S).
- **Keine Rechteverwaltung über MCP-Tools** (P6-M).
- **Kein serverseitiges Rendern fremder Bodies** (P5-Y gilt unverändert fort — auch Bilder werden
  nicht serverseitig verarbeitet, nur validiert und ausgeliefert).

### 0.7 Regeländerungen, die diese Phase auslöst

Diese drei Textänderungen sind **Teil des Step-0-Commits**, nicht des Abschlusses — sonst
arbeitet Block B eine Woche lang gegen eine Regel, die er widerlegt.

**(a) Hard Rule 4, Root-`CLAUDE.md`, Neufassung mit datierter Korrekturnotiz.** Der alte Wortlaut
bleibt als durchgestrichene Zeile stehen (Projektkonvention), darunter:

> **[2026-08-09 Neufassung, P6-U]:** **Schreibrechte folgen der Mitgliedschaft, nicht dem Token.**
> Ziel-Space eines Writes ist per Default der Home-Space des Principals. Ein anderer Ziel-Space
> ist nur zulässig, wenn er in einer `.share.yml` unter `write:` steht oder das Item selbst
> `share_write` trägt — die Liste ist **Daten auf der Platte, kein `if` im Code**, und über kein
> Item-Tool änderbar. Jeder Body, der nicht aus dem Home-Space stammt, wird weiterhin in
> `<untrusted_content>` gewrappt. Der alte Satz („Cross-Space-Writes existieren architektonisch
> nicht") war vier Phasen lang richtig und ist mit geteilten Spaces nicht mehr haltbar; die
> Ersetzung ist eine bewusste Nikinger-Entscheidung vom 2026-08-09, keine stille Aufweichung.

**(b) `ROADMAP.md`** — neue P6-Zeile in der Phasentabelle, plus datierte Korrekturen an genau zwei
Absätzen unter „Bewusst nicht auf der Roadmap": *„Feingranulare Rechte"* und
*„Mehrmandantenfähigkeit — wenn ein dritter Nutzer dazukommt, ist das eine Planungssession"*.
Beide Sätze waren richtig; die Planungssession hat am 2026-08-09 stattgefunden.

**(c) Handover §4.5** — der offene Plan-Widerspruch (P5 Step 9 „frische Einladung" vs. §2.6
„reine Credential-Migration") wird als datierte Notiz in `docs/concepts/phase5_ui_plan.md`
**nicht** korrigiert (📕-Snapshots bleiben unangetastet), sondern in `phase6_shares/CLAUDE.md`
einmal festgehalten: **gelebt wurde der Step-9-Weg.** Damit ist er geschlossen.

---

## §1 Architektur

### 1.1 Berührungsfläche

| Paket | Was P6 dort tut |
|---|---|
| `storage` | **neu:** `acl.py`, `patch.py`. **geändert:** `models.py` (Felder), `store.py` (Contract-Erweiterung), `index.py` (Spalten + `user_version`), `files.py` (Ordnerpfade) |
| `mcpserver` | **geändert:** `tools.py` (siebtes Tool, Quittungen, `space`/`folder`), `permissions.py` (`SharePolicy`, `Surface`), `request_log.py` (`ua`-Feld), `app.py` (Verdrahtung) |
| `webui` | **neu:** `shares.py`, `updates.py`, `assets.py`, `static/js/*`. **geändert:** `api.py`, `serializers.py`, `config.py`, `static_routes.py`, `pages.py`, `static/{app.html,app.css}` |
| `authserver` | **nur** `store.py`: additive Schema-3-Migration (`users.seen_update_id`). Sonst nichts. |
| `phase6_shares/` | `tests/`, `scripts/{spacectl.py,migrate_visibility.py}`, `CLAUDE.md` |

Die Importregel aus P5-B (`webui` darf genau **ein** Symbol aus `mcpserver` importieren) bleibt
bestehen, das Symbol ändert sich: **`mcpserver.permissions.SharePolicy`** statt
`OwnSpaceWritable`. `test_webui_imports_exactly_one_mcpserver_symbol` wird entsprechend nachgezogen,
nicht gelockert.

### 1.2 Das Rechtemodell

#### 1.2.1 Die vier Quellen

| Quelle | Ort | Wer ändert sie |
|---|---|---|
| Eigentum | Verzeichnisname = Space-Name = `path.parts[0]` | niemand (implizit) |
| Space-/Ordner-Freigabe | `.share.yml` im jeweiligen Verzeichnis | Mensch: `spacectl.py` oder UI (abgeschaltet, P6-V) |
| Item-Freigabe | Frontmatter `share_read` / `share_write` | Mensch: UI mit Re-Auth (P6-M) |
| Agentensperre | Frontmatter `visibility: human` | Mensch: UI |

#### 1.2.2 `.share.yml`

```yaml
# <DATA_ROOT>/<space>/.share.yml  oder  <DATA_ROOT>/<space>/<folder>/.share.yml
read:  [fabian]
write: [fabian, dritter]
note:  "Projekt Alpha — geteilt seit 2026-08-12"   # optional, wird nie ausgewertet
```

- Unbekannte Schlüssel werden ignoriert, nicht als Fehler behandelt.
- **Ein Space-Name, der nicht als Verzeichnis existiert, wird ignoriert** und von `diagnose.sh`
  als Befund gemeldet (fail-closed, kein Recht durch Tippfehler).
- Eine nicht parsebare `.share.yml` erzeugt **kein** Recht und einen `logger.critical` — nie eine
  Ausnahme, die einen Lesepfad abbricht.
- `write:` impliziert `read:`. Ein Space in `write:` muss nicht zusätzlich in `read:` stehen.

#### 1.2.3 Auflösung (`storage/acl.py`)

```python
ACL_FILENAME = ".share.yml"
RESERVED_DIR_NAMES = frozenset({"_archive", "_assets"})
MAX_FOLDER_DEPTH = 2

@dataclass(frozen=True, kw_only=True)
class Grant:
    read: frozenset[str]
    write: frozenset[str]

@dataclass(frozen=True, kw_only=True)
class AclDecision:
    space: str                 # Eigentümer-Space = path.parts[0]
    folder: str                # "" oder "a" oder "a/b"
    visibility: str            # "private" | "human"
    read: frozenset[str]       # effektiv, ohne den Eigentümer selbst
    write: frozenset[str]      # effektiv, ohne den Eigentümer selbst

class AclReader:
    def __init__(self, data_root: Path) -> None: ...
    def grants_for_dir(self, directory: Path) -> Grant: ...   # Vereinigung aller Vorfahren
    def members_of_space(self, space: str) -> frozenset[str]: ...
    def invalidate(self) -> None: ...
```

**Regeln, wörtlich:**

1. Die effektiven Rechte eines Items sind die **Vereinigung** aller `.share.yml` vom Space-Wurzel-
   verzeichnis bis zum Ordner des Items, **plus** `share_read`/`share_write` des Items selbst.
   Vereinigung, nicht „nächster gewinnt" — monoton und in einem Satz erklärbar.
2. **`visibility: human` sticht alles.** Ein solches Item wird nie freigegeben, egal was in einer
   `.share.yml` darüber steht; die UI verweigert das Setzen von `share_*` daran.
3. Der Eigentümer-Space hat immer `read` und `write` auf seine eigenen Items — steht nicht in den
   Mengen, ergibt sich aus `acl.space == actor`.
4. Cache: `dict[(path, mtime, size) -> Grant]`, invalidiert sich über `stat()`. Kein TTL, kein
   Hintergrund-Thread. `invalidate()` existiert für Tests und für `spacectl.py`.

#### 1.2.4 `Surface` — warum `visibility: human` funktioniert

```python
# mcpserver/permissions.py
class Surface(str, Enum):
    AGENT = "agent"   # /mcp — Bearer
    HUMAN = "human"   # /ui, /api — Cookie-Session
```

Die Oberfläche wird **an genau einer Stelle je Adapter gesetzt** (`tools.py` immer `AGENT`,
`webui/api.py` immer `HUMAN`) und durchgereicht. Es gibt keinen Codepfad, in dem ein Bearer-Request
`HUMAN` sein kann — das ist dieselbe architektonische Trennung wie P5-D/F, eine Schicht tiefer.

```python
class Permissions(Protocol):
    def can_read(self, actor: str, target: str) -> bool: ...
    def can_write(self, actor: str, target: str) -> bool: ...
    def can_read_item(self, actor: str, acl: AclDecision, *, surface: Surface) -> bool: ...
    def can_write_item(self, actor: str, acl: AclDecision) -> bool: ...
    def visible_spaces(self, actor: str, all_spaces: Sequence[str]) -> list[str]: ...

class SharePolicy:
    """Ersetzt OwnSpaceWritable. Braucht den AclReader, sonst kennt sie keine Mitgliedschaft."""
    def __init__(self, acl: AclReader) -> None: ...
```

`OwnSpaceWritable` wird **entfernt**, nicht danebengestellt — zwei Policies, von denen eine tot
ist, sind eine Falle für `grep`.

#### 1.2.5 Rechte-Erweiterung und Re-Auth

```python
# webui/shares.py
@dataclass(frozen=True, kw_only=True)
class ShareState:
    visibility: str
    share_read: frozenset[str]
    share_write: frozenset[str]
    space: str
    folder: str

def widens(before: ShareState, after: ShareState, *, acl: AclReader) -> bool: ...
def require_share_reauth(request, session, *, before, after, acl) -> None: ...   # wirft ReauthRequired
```

`widens()` ist **wahr**, wenn die effektive Lese- oder Schreibmenge nach der Änderung eine echte
Obermenge der vorherigen ist — das schließt das Verschieben in einen Ordner oder Space mit
weitergehender `.share.yml` ein. Es ist **falsch** bei Rücknahme, bei `private → human` und bei
reinen Inhaltsänderungen.

> **Ehrliche Grenze, die in `shares.py` als Docstring steht:** Dieses Gate schützt gegen Versehen
> und gegen injektionsgetriebene Massenfreigabe. Es schützt **nicht** gegen einen Agenten, der
> entschlossen ist, Inhalte offenzulegen — der kann sie in einen geteilten Space **kopieren**, und
> das ist ein legitimer Schreibvorgang. Wer das ausschließen will, braucht ein anderes
> Vertrauensmodell, nicht ein weiteres Gate.

### 1.3 Ordner

- Pfad: `<DATA_ROOT>/<space>/<folder…>/<id>__<slug>.md`, maximal zwei Ordnerebenen.
- `folder` ist **abgeleitet**: `"/".join(path.relative_to(data_root).parts[1:-1])`.
- `files.item_path(data_root, space, item_id, slug, folder="")` — neuer Parameter, Default `""`
  hält jeden bestehenden Aufruf gültig.
- Verschieben: `Store.update(item_id, version=…, folder="projekte/alpha")` → `files.move_file()`,
  gleicher atomarer Pfad wie die Titeländerung heute.
- Archivieren bleibt flach (`<space>/_archive/`, P6-R). Ein Item, das aus dem Archiv geholt wird,
  gibt es nicht — Archivieren ist weiterhin einseitig.
- `index.rebuild_index()` läuft heute schon mit `rglob("*.md")`; verschachtelte Dateien werden also
  bereits gefunden. `[VERIFY]` V47: `.share.yml` und `_assets/` dürfen dabei **nicht** als Item
  einlaufen (Filter auf `*.md` greift, aber `_archive` ist heute schon drin — Verhalten prüfen,
  nicht annehmen).

### 1.4 Contract-Erweiterung `storage` (P1-Contract, dritte Öffnung)

> Der P1-Contract galt seit 2026-07-26 als „wieder zu". Er wird hier **einmalig und benannt**
> geöffnet. Nach Phasenabschluss ist er wieder zu.

**`models.py`:**

```python
VISIBILITY_VALUES: frozenset[str] = frozenset({"private", "human"})
DEFAULT_VISIBILITY = "private"

@dataclass(kw_only=True)
class Item:
    ...                              # unverändert
    folder: str = ""                 # NEU, abgeleitet, nie im Frontmatter
    visibility: str = "private"      # NEU, Frontmatter
    share_read: list[str] = field(default_factory=list)    # NEU, Frontmatter
    share_write: list[str] = field(default_factory=list)   # NEU, Frontmatter

@dataclass(kw_only=True)
class ItemSummary:
    ...                              # unverändert
    folder: str = ""
    visibility: str = "private"
    share_read: list[str] = field(default_factory=list)
    share_write: list[str] = field(default_factory=list)

@dataclass(kw_only=True)
class SpaceInfo:
    name: str
    item_count: int
    members: tuple[str, ...] = ()    # NEU: write-Mitglieder aus der Space-Wurzel-.share.yml
    folders: tuple[str, ...] = ()    # NEU: vorhandene Ordner, sortiert
```

`_KNOWN_FIELDS` in `store.py` wird um `visibility`, `share_read`, `share_write` erweitert —
**wichtig**, sonst landen sie in `Item.extra` und werden beim Round-Trip zwar erhalten, aber nie
ausgewertet.

**`store.py` — neue und geänderte Signaturen:**

```python
def acl_of(self, item_id: str) -> AclDecision: ...
    # index-only + .share.yml. Liest die Item-DATEI NICHT. Damit sicher aufrufbar, BEVOR
    # feststeht, ob der Zugriff erlaubt ist — dieselbe Eigenschaft wie space_of() (P2).

def create(self, space, *, type, title, body="", folder="", **fields) -> Item: ...
def update(self, item_id, *, version, **changes) -> Item: ...        # changes darf folder/visibility/share_* enthalten
def patch(self, item_id, *, version, edits: Sequence[TextEdit]) -> PatchResult: ...   # NEU
def search(self, query=None, *, space=None, spaces=None, folder=None, type=None,
           status=None, tag=None, due_before=None, limit=50, offset=0) -> SearchResult: ...
def list_spaces(self) -> list[SpaceInfo]: ...    # jetzt verzeichnis- UND indexbasiert
```

**`list_spaces()` ändert sein Verhalten:** heute leitet es Spaces ausschließlich aus Indexzeilen
ab — ein frisch angelegter geteilter Space ohne Item wäre unsichtbar (derselbe Fund wie B1 aus der
P2-Adapter-Abnahme, nur eine Ebene höher). Ab P6: **Vereinigung aus Verzeichnissen unter
`DATA_ROOT` (ohne führenden Punkt) und Indexzeilen.** Der Adapter-Fallback in `tools.py` und
`api.py :: _visible_space_infos()` für den eigenen leeren Space bleibt trotzdem stehen — er kostet
nichts und ist gegen einen anderen Fehlerfall gerichtet.

**`index.py`:** neue Spalten `folder`, `visibility`, `share_read_json`, `share_write_json`.
Schemaversionierung über `PRAGMA user_version` (`INDEX_SCHEMA_VERSION = 2`); bei Abweichung wird
der Index **verworfen und neu gebaut** — das ist nach Hard Rule 2 jederzeit erlaubt und billiger
als jede Migration. `[VERIFY]` V46: `connect()` kennt heute keinen Versionsbegriff.

### 1.5 Tool-Fläche (MCP)

#### 1.5.1 Sieben Tools

| Tool | Änderung |
|---|---|
| `list_spaces` | Payload je Space zusätzlich `members`, `folders`; `writable` unverändert aus `permissions.can_write` |
| `search_items` | neuer Parameter `folder: str \| None`; `visibility: human` fällt raus (Surface) |
| `get_item` | unverändert |
| `create_item` | neu: `space: str \| None = None` (Default Home), `folder: str \| None = None`; Quittung statt Dateitext |
| `update_item` | `visibility`/`share_read`/`share_write` sind **verboten** (`ValidationError` mit Verweis auf die UI); Quittung statt Dateitext |
| `append_to_item` | Quittung statt Dateitext |
| **`patch_item`** | **neu** |

#### 1.5.2 `patch_item`

```python
class TextEdit(TypedDict):
    old_text: str
    new_text: str

@mcp.tool(
    title="Item punktuell ändern",
    description=(
        "Ersetzt exakte Textstellen im Body eines Items, ohne den Rest neu zu schreiben. "
        "Jedes old_text muss genau einmal vorkommen; sonst schlägt der ganze Aufruf fehl "
        "und nichts wird geschrieben. Braucht die zuletzt gelesene version."
    ),
    annotations={"readOnlyHint": False, "destructiveHint": True,
                 "idempotentHint": False, "openWorldHint": False},
)
def patch_item(item_id: str, version: int, edits: list[TextEdit],
               return_body: bool = False) -> str: ...
```

Reihenfolge im Body **wörtlich wie bei den anderen Schreib-Tools** (Plan §3.3 aus P2):
`_authenticated_principal()` → `store.acl_of(item_id)` → `permissions.can_write_item()` →
`store.patch()` → formatieren. Ein Rechtefehler darf `store.patch()` nie erreichen.

`storage/patch.py`:

```python
class PatchError(ValidationError):
    def __init__(self, *, index: int, found: int, lines: list[int]) -> None: ...

@dataclass(frozen=True, kw_only=True)
class PatchResult:
    item: Item
    replacements: int
    lines: tuple[int, ...]        # 1-basierte Zeilennummern der angewandten Ersetzungen
    bytes_before: int
    bytes_after: int

def apply_edits(body: str, edits: Sequence[TextEdit]) -> tuple[str, tuple[int, ...]]: ...
```

`apply_edits` arbeitet rein funktional auf dem String, wirft `PatchError` bei `found != 1` und
schreibt nichts — `Store.patch()` ruft es **vor** dem Öffnen des Write-Locks auf Kopie auf und
schreibt erst danach. Damit ist „alles oder nichts" keine Transaktionslogik, sondern eine
Reihenfolge.

Fehlertext (`map_storage_error`, gleiche Familie wie die bestehenden):

```
patch_failed: edits[1] fand 0 Treffer — lies das Item neu mit get_item und prüfe den exakten Text
patch_failed: edits[0] fand 3 Treffer (Zeilen 12, 40, …) — mach old_text eindeutiger
```

> `[SEAM]` **Nicht gebaut, bewusst (P6-G):** ein `on_conflict="retry_if_unambiguous"`, das bei
> `version`-Mismatch trotzdem patcht, solange alle Anker noch eindeutig sind. Das wäre ein
> inhaltsverankerter Merge und damit ein Loch in Hard Rule 3 („kein Last-Write-Wins, nirgends").
> Wer das bauen will, braucht vorher eine Nikinger-Entscheidung zu Rule 3, nicht ein Argument
> über Bequemlichkeit.

#### 1.5.3 Die Quittung (`mcpserver/receipts.py`)

```python
def write_receipt(item: Item, *, op: str, replacements: int | None = None,
                  lines: Sequence[int] = (), bytes_before: int | None = None,
                  bytes_after: int | None = None) -> str: ...
```

Liefert `compact_json`:

```json
{"op":"patch","id":"itm_b252a444","space":"niklas","folder":"projekte","title":"Notizen Alpha",
 "version":8,"updated":"2026-08-12T09:41:00Z","replacements":2,"lines":[12,88],
 "bytes":{"before":41230,"after":41198}}
```

- `op` ∈ `create|update|append|patch`.
- `replacements`/`lines`/`bytes` nur bei `patch`; bei `append` zusätzlich `appended_bytes`.
- **Niemals Body-Inhalt**, auch nicht ausschnittsweise — sonst wandert unbemerkt fremder Text an
  einer Stelle heraus, die keine Wrap-Logik hat.
- `return_body=True` liefert stattdessen exakt das heutige `item_to_filetext(item)`, unverändert.

Die Tool-Beschreibung jedes Schreib-Tools nennt `return_body` in einem Halbsatz — sonst findet das
Modell den Weg zum vollen Body nicht.

### 1.6 REST-Fläche

| Route | Methode | Änderung |
|---|---|---|
| `/api/v1/spaces` | GET | `members`, `folders`, `kind: own\|shared\|foreign` |
| `/api/v1/overview` | GET | zählt für den eigenen Space auch `visibility: human` (P6-P); neuer Zähler `human` |
| `/api/v1/meta` | GET | zusätzlich `visibility_values`, `max_folder_depth`, `asset` (Typen/Limit), `space_admin_enabled` |
| `/api/v1/items` | GET | Filter `folder`; Antwortzeilen um `folder`, `visibility`, `share_read`, `share_write`, `shared: bool` |
| `/api/v1/items/{id}` | PATCH | darf `folder`, `visibility`, `share_read`, `share_write` — löst bei `widens()` `403 reauth_required` aus |
| `/api/v1/items/{id}/share` | POST | expliziter Freigabe-Endpunkt (die UI benutzt ihn, PATCH bleibt für Inhalt) |
| `/api/v1/updates` | GET | `{entries: [...], latest_id, seen_id}` |
| `/api/v1/updates/seen` | POST | setzt `seen_update_id`, CSRF-pflichtig |
| `/api/v1/assets` | POST | Upload (Block C) |
| `/ui/assets/{space}/{name}` | GET | Ausliefern mit Rechteprüfung (Block C) |
| `/api/v1/spaces/{name}/members` | POST/DELETE | **hinter `space_admin_enabled`, Default aus** (P6-V) |

Fehlercode-Familie wird um `reauth_required` und `patch_failed` erweitert (`webui/errors.py ::
ApiError`), Statuscodes `403` und `422`.

### 1.7 Assets (Block C)

#### 1.7.1 Kern

```python
# storage/assets.py
ASSET_ID_PREFIX = "ast_"
ASSETS_DIR_NAME = "_assets"
MAX_ASSET_BYTES = 5 * 1024 * 1024
ALLOWED_ASSETS: dict[bytes, tuple[str, str]] = {...}   # Magic Bytes -> (mime, ext)

def sniff(data: bytes) -> tuple[str, str] | None: ...
def store_asset(data_root: Path, space: str, data: bytes) -> AssetRef: ...
def asset_path(data_root: Path, space: str, name: str) -> Path | None: ...
```

`store_asset` schreibt über `files.atomic_write`-Zwilling `atomic_write_bytes()` und committet über
`history.commit(data_root, f"asset {ast_id} [{space}]")` — derselbe Weg wie jeder Item-Write, damit
Backup und Restore genau einen Pfad kennen.

#### 1.7.2 Warum HEIC/HEIF abgelehnt wird — ausdrückliche Empfehlung gegen den Wunsch

Drei Gründe, in dieser Reihenfolge:

1. **Chrome und Firefox zeigen HEIC nicht an.** Ein Bild, das nur in Safari sichtbar ist, ist in
   einem Zwei-bis-drei-Personen-Werkzeug schlimmer als kein Bild, weil der Fehler erst beim
   anderen auftritt.
2. **Serverseitige Konvertierung würde eine Bildbibliothek in den Prozess holen** (`pillow-heif`
   o. ä.). Bildparser sind eine der klassischsten RCE-Quellen; der Dienst hat heute **keine**
   Abhängigkeit, die Binärformate interpretiert. Das gegen Bequemlichkeit einzutauschen, ist ein
   schlechtes Geschäft für ein System, das öffentlich über einen Funnel erreichbar ist.
3. **Es ist praktisch selten nötig:** iOS/macOS wandeln beim Einfügen und beim Hochladen über ein
   `<input type="file">` in aller Regel selbst nach JPEG/PNG um.

Umsetzung: HEIC wird über Magic Bytes (`ftypheic`/`ftypheix`/`ftypmif1`) **erkannt** und mit einer
Meldung abgelehnt, die den Grund nennt und den Weg beschreibt („in der Fotos-App als JPEG
exportieren"). Eine stumme Ablehnung „unbekanntes Format" wäre hier falsch. `[SEAM]` für spätere
Transkodierung ist benannt, nicht gebaut. **Wenn der Nikinger das überstimmt, geht es in eine
eigene Runde mit eigener Abhängigkeitsprüfung — nicht als Zeile in Step 8.**

#### 1.7.3 Ausliefern

- Rechteprüfung wie bei einem Item im selben Verzeichnis (`AclReader.grants_for_dir`).
- `Content-Type` ausschließlich aus den Magic Bytes, nie aus dem Request, nie aus der Endung.
- `X-Content-Type-Options: nosniff`, CSP unverändert (`img-src 'self' data:` deckt es).
- `Cache-Control: private, max-age=300` — nicht `immutable`: eine zurückgenommene Freigabe soll
  nicht ein Jahr lang im Browser weiterleben. Fünf Minuten ist das bewusst gewählte Fenster.

### 1.8 Update-Log und Banner

- `docs/UPDATE_LOG.md`, Format §2.4, geparst von `webui/updates.py :: parse_update_log()`.
- Eintrags-ID = `"<YYYY-MM-DD>#<n>"` (n = Position des Tages, 1-basiert). Kein Release-Bezug, damit
  `deploy.sh` keine Repo-Datei verändern muss.
- Gesehen-Zustand: `auth.sqlite3`, Tabelle `users`, neue Spalte `seen_update_id TEXT`
  (**Schema 3**, rein additiv, `ALTER TABLE`). `[VERIFY]` V44: Migrationsmechanik von Schema 2
  übernehmen, nicht neu erfinden.
- Banner erscheint bei jedem Laden von `/ui`, solange `seen_update_id != latest_id`; „Verstanden"
  setzt ihn. Danach im Einstellungsdialog unter **„Update-Log"**.
- **Der erste Eintrag ist Pflichtinhalt von Step 3** und muss die Sichtbarkeitsumstellung
  ankündigen, bevor Block B sie durchführt (P6-L, H1).

---

## §2 Datenformate

### 2.1 Frontmatter (Erweiterung)

```yaml
---
id: itm_b252a444
space: niklas
type: note
title: Notizen Alpha
status: active
visibility: private          # NEU  private | human
share_read: [fabian]         # NEU  optional, leer = nicht vorhanden
share_write: []              # NEU  optional
tags: []
links: []
created: 2026-08-01T10:00:00Z
updated: 2026-08-12T09:41:00Z
version: 8
format: markdown
---
```

- Fehlende Felder ⇒ Defaults (`private`, leere Listen). Bestandsdateien bleiben damit lesbar,
  **bevor** die Migration läuft.
- Leere Listen werden **nicht** serialisiert (kein Rauschen in 200 Dateien).
- `folder` steht **nicht** im Frontmatter (P6-Q).

### 2.2 `.share.yml`

Siehe §1.2.2. Geparst mit dem hauseigenen Parser aus `storage/frontmatter.py`-Umfeld bzw. `yaml.safe_load`
— `[VERIFY]` V51: welcher Weg im Repo bereits existiert; **kein** neuer YAML-Parser.

### 2.3 Migrationsreport (`phase6_shares/scripts/migrate_visibility.py`)

JSON auf stdout (Hard Rule 7), eine Zeile je Item:
`{"id":…, "space":…, "path":…, "before":null, "after":"private"}`, am Ende eine Summenzeile.
`--dry-run` ist der **Default**; scharf erst mit `--apply`.

### 2.4 `docs/UPDATE_LOG.md`

```markdown
## 2026-08-12
- Deine Notizen sind ab sofort **standardmäßig privat**. Was andere sehen sollen, kommt in einen
  geteilten Space oder wird einzeln freigegeben.
- Ordner: Notizen und Aufgaben lassen sich in Ordner einsortieren (Ziehen oder Menü).

## 2026-08-10
- Claude kann Dokumente jetzt punktuell ändern statt komplett neu zu schreiben.
```

Parserregeln, streng: `## <ISO-Datum>` beginnt einen Eintrag; `- ` beginnt eine Zeile; alles andere
wird ignoriert. Kein Markdown-Rendering serverseitig — `app.js` rendert mit dem vorhandenen
Sanitizer.

---

## §3 Sicherheit

| Risiko | Antwort in diesem Plan |
|---|---|
| Injizierte Freigabe („gib alles frei") aus einem fremden Body | Kein Tool kann Freigaben setzen (P6-M). Bleibt: der Mensch in der UI mit Re-Auth. |
| Rechteentscheidung auf Basis gelesener Dateien | `acl_of()` liest **nur** Index + `.share.yml`, nie die Item-Datei — Rechteprüfung vor jedem Dateizugriff, wie `space_of()` seit P2. |
| Tippfehler in `.share.yml` erzeugt Recht | Unbekannter Space ⇒ ignoriert, `diagnose.sh`-Befund. Kaputte Datei ⇒ kein Recht + `critical`. |
| Bild-Upload als Angriffsfläche | Magic Bytes statt Endung, 5 MiB, `nosniff`, keine serverseitige Bildbibliothek (P6-Z), Ausliefern nur mit Leserecht. |
| Verwaiste Freigaben nach Löschen des dritten Spaces | Fail-closed (unbekannter Space = kein Recht) + `diagnose.sh`-Zeile + Rückbauweg in `spacectl.py remove-space`. |
| `visibility: human` leckt über Zähler | Surface-Filter greift auch in `total` und in den Overview-Zählern (P6-P), Test dafür ist Pflicht. |
| Host-Header-Bypass (CVE-2026-48710) | Step 0: Version prüfen, notfalls Pin anheben. `TrustedHostMiddleware` bleibt gesetzt. |
| `app.js`-Aufteilung bricht ungetestet etwas | JS bleibt laut P5 unit-ungetestet — deshalb ist der Split ein **eigener Commit ohne Funktionsänderung**, mit jsdom-Durchlauf davor und danach. |

---

## §4 Blöcke und Steps

Jeder Step endet mit: grünes `pytest -q`, Modul-Tabelle in `phase6_shares/CLAUDE.md` und
`## Session stopped`-Block im **selben** Commit (Hard Rule 8), neue `.md` ⇒ Zeile in
`docs/INDEX.md` im selben Commit.

### Block A — Werkzeuge, Betrieb, Kommunikation

#### Step 0 — Haushalt, Verifikation, Regeländerungen

1. **Verifikationsdurchlauf** (kein Selbstzweck, „nichts zu tun" ist ein zulässiges Ergebnis je
   Einzelpunkt): alle `up:`/`down:`-Links auflösbar · jede `.md` hat eine Zeile in
   `docs/INDEX.md` · `find . -name "*.md" -size +40k` — jeder Treffer muss 📕/📦 sein ·
   `pytest -q` (`[VERIFY]` V39: 576 behauptet) · `git status` sauber · Push-Stand gegen `origin/main`.
2. **`[VERIFY]` V40 — CVE-2026-48710:** `.venv/bin/pip show starlette`. Bei `< 1.0.1`: Pin in
   `phase4_auth/pyproject.toml` und `phase5_ui/pyproject.toml` auf `starlette>=1.0.1` anheben,
   Testsuite, **Befund S11 anlegen**. Bei `>= 1.0.1`: als geprüft-in-Ordnung notieren, nicht
   stillschweigend übergehen.
3. **`[VERIFY]` V41 (Nachfolger V33):** Anthropic-Connector-Doku gegenlesen — insbesondere, ob es
   Grenzen für Tool-Anzahl, Beschreibungslänge oder Schemaformen gibt, die ein siebtes Tool mit
   `list[TypedDict]`-Parameter betreffen. Ergebnis in den Session-Block, egal wie es ausfällt.
4. **Regeländerungen aus §0.7** (a) Rule 4, (b) ROADMAP-Zeile + zwei Korrekturabsätze,
   (c) §4.5-Widerspruch geschlossen.
5. **`phase6_shares/` anlegen:** `CLAUDE.md` (Phase-Head nach dem Muster von `phase5_ui/CLAUDE.md`:
   Mission, Bauprinzip, Scope, harte Regeln der Phase, Modul-Status-Tabelle, ein Session-Block),
   `tests/conftest.py`, `scripts/`. `docs/INDEX.md` um Plan + Phase-Head + `UPDATE_LOG.md` ergänzen.
6. **V37** formal abhaken (P5-Restposten, faktisch erledigt).

**DoD:** Testsuite grün und Zahl notiert; V40/V41 beantwortet; Rule 4 neu gefasst; Phase-Head steht.

#### Step 1 — Werkzeug-Ergonomie

**Dateien:** `storage/patch.py` (neu), `storage/store.py`, `mcpserver/receipts.py` (neu),
`mcpserver/tools.py`.

1. `storage/patch.py`: `TextEdit`, `PatchError`, `PatchResult`, `apply_edits()` (§1.5.2).
2. `Store.patch()` — Reihenfolge exakt: Lock nehmen → `_reconcile_and_get_row()` → Version prüfen
   (`ConflictError`) → `status == "archived"` ablehnen (wie `update`/`append`) → `apply_edits()` auf
   Kopie → `replace(current, body=…, version=+1, updated=now)` → `_write_item_file(op="patch")`.
3. `mcpserver/receipts.py :: write_receipt()` (§1.5.3).
4. `tools.py`: `patch_item` registrieren; `return_body` an alle vier Schreib-Tools; Quittung als
   Default; `update_item` lehnt `visibility`/`share_read`/`share_write` ab (die Felder existieren
   noch nicht — der Riegel entsteht **vor** dem Feld, damit Step 5 ihn nicht vergisst).
5. Tool-Beschreibungen nachziehen (jede nennt `return_body` in einem Halbsatz).

**Tests** (`phase6_shares/tests/test_patch.py`, `phase1_storage/tests/test_store_patch.py`,
`phase2_mcp/tests/test_tools_patch.py`):
- `test_apply_edits_replaces_each_anchor_once`
- `test_apply_edits_rejects_zero_matches_and_writes_nothing`
- `test_apply_edits_rejects_multiple_matches_and_names_the_lines`
- `test_edits_are_applied_in_order_and_may_depend_on_each_other`
- `test_patch_bumps_version_once_for_many_edits`
- `test_patch_creates_exactly_one_git_commit`
- `test_patch_on_version_mismatch_raises_conflict_and_leaves_file_untouched`
- `test_patch_on_archived_item_is_rejected`
- `test_patch_preserves_unknown_frontmatter_fields`
- `test_write_tools_return_receipt_by_default`
- `test_write_tools_return_full_filetext_when_return_body_true`
- `test_receipt_never_contains_body_text`
- `test_update_item_rejects_share_fields`

**DoD:** `mcp_smoke.py` um einen Patch-Durchgang erweitert und 13/13 grün.

#### Step 2 — Betrieb

**Dateien:** `mcpserver/request_log.py`, `phase5_ui/systemd/sharefyx-purge.*` (vorhanden),
`phase3_edge/scripts/diagnose.sh`, `phase5_ui/scripts/ui_budget.py`.

1. **O2:** den bestehenden Purge um `clients` (ohne aktive Familie, älter als N Tage) und
   `token_families` (widerrufen/abgelaufen, älter als N Tage) erweitern. **Keine neue Unit.**
   Grenzwert als Konstante mit Begründung, nicht als Literal.
2. **Client-Surface-Logging (A5):** Feld `ua` im bestehenden JSON-Log, gekürzt auf 120 Zeichen,
   **niemals** Token/Titel/Body. `[VERIFY]` V42: setzen die realen MCP-Clients den `User-Agent`
   verlässlich? Über zwei Tage journald **messen**, Ergebnis notieren; wenn nicht — Befund, kein
   Workaround.
3. `diagnose.sh`: zwei Prüfungen — Purge-Lauf jünger als 48 h, und (ab Block B) verwaiste
   Space-Namen in `.share.yml`.
4. `ui_budget.py`: Latenz + Antwortgröße für `/api/v1/overview`, `search_items`, `get_item`
   (P6-I/P6-S). Zahlen in den Session-Block.

#### Step 3 — Update-Log und Banner

**Dateien:** `docs/UPDATE_LOG.md` (neu), `webui/updates.py` (neu), `webui/api.py`,
`authserver/store.py` (Schema 3), `webui/static/js/updates.js`, `app.html`, `app.css`,
`phase5_ui/scripts/deploy.sh`.

1. `parse_update_log(text) -> list[UpdateEntry]`, `UpdateEntry(id, date, lines)`.
2. Schema 3: `users.seen_update_id TEXT` additiv (`[VERIFY]` V44).
3. `GET /api/v1/updates`, `POST /api/v1/updates/seen` (CSRF-pflichtig).
4. Banner in `/ui` + Einstellungsabschnitt „Update-Log".
5. `deploy.sh`-Gate (P6-X) inklusive Override-Variable und klarer Fehlermeldung.
6. **Erster Eintrag geschrieben** — er kündigt an, was Block B tun wird.

**Tests:** `test_updates.py` (Parser: leere Datei, kaputte Zeilen, Reihenfolge, ID-Vergabe),
`test_api.py` (+2: `seen` setzt, Banner-Zustand pro Nutzer getrennt), `test_deploy_scripts.py`
(+2: Gate greift, Override greift).

---

### 🚦 GATE A → B (Nikinger, live)

Erst wenn **alle vier** stehen, beginnt Block B:

1. `patch_item` über den **echten** Connector an einem echten Item, inklusive eines absichtlichen
   Fehlversuchs (mehrdeutiger `old_text`).
2. Eine Quittung ist im Tool-Ergebnis sichtbar, `return_body=True` liefert weiterhin den Volltext.
3. Purge ist real gelaufen (`journalctl`), `clients`-Zeilenzahl gesunken.
4. Update-Banner erscheint im Browser, verschwindet nach „Verstanden", ist unter Einstellungen
   wiederfindbar — **und Fabian hat den Eintrag über die anstehende Sichtbarkeitsumstellung
   gesehen.**

---

### Block B — Dateisystem

#### Step 4 — Storage-Fundament

**Reihenfolge ist hier nicht verhandelbar (P6-D):**

1. **Charakterisierungstests zuerst** (`phase6_shares/tests/test_characterization.py` +
   `tests/golden/`): Round-Trip einer Datei mit unbekannten Feldern, Umlauten und CRLF · Drift-
   Repair inkl. `drift`-Commit · `ConflictError.current` · Archivpfad · die vier Git-Commit-
   Messages (`create|update|append|archive <id> [<space>]`). Golden Files werden **byte-verglichen**.
2. `storage/acl.py` (§1.2.3).
3. `models.py`: neue Felder, `VISIBILITY_VALUES`, `DEFAULT_VISIBILITY`.
4. `files.py`: `item_path(..., folder="")`, `validate_folder(folder) -> str` (Slug je Segment,
   Tiefe ≤ 2, reservierte Namen).
5. `index.py`: vier neue Spalten, `INDEX_SCHEMA_VERSION`, `PRAGMA user_version`, Verwerfen-und-
   Neubauen bei Abweichung.
6. `store.py`: `_KNOWN_FIELDS` erweitert · `acl_of()` · `create(folder=)` · `update()` akzeptiert
   `folder`/`visibility`/`share_read`/`share_write` und verschiebt bei Ordnerwechsel ·
   `search(spaces=, folder=)` · `list_spaces()` verzeichnisbasiert.

**DoD:** Charakterisierung **byte-identisch grün**; Contract-Erweiterung in
`phase1_storage/CLAUDE.md` unter „Geerbte Contracts" dokumentiert (dritte, benannte Öffnung).

#### Step 5 — Rechtepolitik

**Dateien:** `mcpserver/permissions.py`, `mcpserver/tools.py`, `mcpserver/app.py`,
`webui/api.py`, `webui/serializers.py`.

1. `Surface`, erweitertes `Permissions`-Protokoll, `SharePolicy`; `OwnSpaceWritable` **entfernen**.
2. `app.py`: `AclReader` einmal bauen, in `SharePolicy` und `Store` teilen (ein Handle, kein zweiter).
3. `tools.py`: alle Lese- und Schreibpfade auf `acl_of()` + `can_read_item`/`can_write_item`
   umstellen, `Surface.AGENT` fix; `search_items` filtert `visibility: human` heraus **inklusive
   `total`**; `create_item(space=…, folder=…)`.
4. `webui/api.py`: dasselbe mit `Surface.HUMAN`; Serializer um `folder`/`visibility`/`share_*`/
   `shared` erweitert.
5. `test_webui_imports_exactly_one_mcpserver_symbol` auf `SharePolicy` nachziehen.

**Tests** (Auswahl, alle Pflicht):
- `test_foreign_space_is_invisible_without_share`
- `test_share_read_makes_exactly_one_item_visible_not_the_folder`
- `test_folder_share_is_inherited_by_children`
- `test_share_write_allows_update_and_append_but_not_in_other_folders`
- `test_human_only_item_is_invisible_to_agent_surface_including_total`
- `test_human_only_item_is_visible_and_counted_on_human_surface`
- `test_unknown_space_in_share_yml_grants_nothing`
- `test_broken_share_yml_grants_nothing_and_logs_critical`
- `test_create_item_into_shared_space_is_allowed_for_member`
- `test_create_item_into_foreign_space_is_denied`
- `test_foreign_body_is_still_wrapped_in_shared_space`
- `test_acl_of_does_not_read_the_item_file`

#### Step 6 — Verwaltung und Migration

**Dateien:** `phase6_shares/scripts/spacectl.py`, `phase6_shares/scripts/migrate_visibility.py`,
`phase3_edge/scripts/diagnose.sh`.

`spacectl.py` (`STATE_DIRECTORY`-Konvention wie `authctl.py`):
`create-space <name>` · `list-spaces` · `add-member <space> <user> --read|--write` ·
`remove-member` · `show <space>` · `remove-space <name> --force` (mit ausdrücklicher Warnung, dass
Git-Historie und Backups die Inhalte behalten).

`migrate_visibility.py`: `--dry-run` (Default) / `--apply`, Report nach §2.3, **rührt Bodies nicht
an** — schreibt ausschließlich `visibility: private` in Frontmatter ohne dieses Feld, über den
bestehenden atomaren Pfad, mit einem Git-Commit `migrate visibility [<space>]` je Space (nicht je
Item — 200 Commits wären Lärm).

**DoD:** Ein geteilter Space existiert real, ein dritter Nutzer ist angelegt, `diagnose.sh` meldet
keine verwaisten Namen.

#### Step 7 — UI Dateisystem

> **[2026-08-13 Ergänzung, kein Umschreiben dieses Snapshots]** Zu diesem Step gehört seit dem
> 2026-08-13 ein eigener, gegen den echten Code verifizierter Zusatzplan:
> **`../../phase6_shares/ITEM_MOVE_PLAN.md`** — Item-Verschieben zwischen Ordnern **und Spaces**
> (Cross-Space-Move fehlt auf allen Schichten), die UI-Bedienung dafür, sowie ein davon
> unabhängiger Lesbarkeitsfix der Textfarben-Token. Er trägt die Entscheidungen **P6-AD–P6-AJ**,
> die Abnahmezeilen **25–30**, `[VERIFY]` **V52–V55** und schneidet die Arbeit in **Step 7a**
> (Farben, jederzeit lieferbar), diesen Step 7 (unverändert) und **Step 7b** (Cross-Space-Move,
> setzt Step 7 voraus). Punkt 5 unten („Verschieben per Menü und Drag & Drop") bleibt Scope
> dieses Steps; er meint ausdrücklich nur den Ordnerwechsel **innerhalb** eines Space.
> Der Zusatzplan korrigiert außerdem vier Annahmen aus der Planungsvormerkung vom selben Tag
> (§1.2 dort) — u. a. dass `Store.update(folder=…)` längst gebaut ist.

**Dateien:** `webui/static/js/*` (Split, P6-AC), `app.html`, `app.css`, `webui/shares.py` (neu),
`webui/api.py`, `webui/config.py`.

1. **Zuerst der reine Split** (eigener Commit, keine Funktionsänderung): `app.js` → `js/{app,
   api,state,tree,list,editor,markdown,dialogs,toasts,updates}.js`. jsdom-Durchlauf vorher/nachher
   im Scratchpad, Ergebnis in den Session-Block. `[VERIFY]` V50: `<script type="module">` unter
   `script-src 'self'` ohne Build-Step.
2. Baum: Übersicht ▸ eigener Space ▸ Ordner ▸ **geteilte Spaces** ▸ verbundene Spaces.
3. Sichtbarkeits-Chip je Zeile (`privat` · `nur ich` · `geteilt mit …`).
4. Freigabedialog + `webui/shares.py :: widens()`/Re-Auth (`[VERIFY]` V43: exakte API von
   `webui/reauth.py`).
5. Ordner anlegen/umbenennen, Verschieben per Menü **und** per Drag & Drop (P6-AB).
6. `space_admin_enabled` (Default aus) + sichtbar deaktivierter Menüpunkt „kommt in Phase 7".

**Tests:** `test_shares.py` (`widens()`-Wahrheitstabelle, 8 Fälle), `test_api.py`
(+`reauth_required` bei Erweiterung, kein Gate bei Rücknahme), `test_pages_markup.py`
(+Chip, +deaktivierter Menüpunkt), `test_static_routes.py` (+Modul-Auslieferung).

---

### 🚦 GATE B (Live-Abnahme Teil 1)

Niklas zuerst allein, danach eine gemeinsame Sitzung mit Fabian, dritter Space live. Erst danach
Block C. Details: Abnahmematrix §6, Zeilen 8–18.

---

### Block C — Bilder

#### Step 8 — Assets-Kern
`storage/assets.py`, `webui/assets.py`, Routen, Limits, Rechteprüfung, `files.atomic_write_bytes()`.
Tests: Magic-Byte-Erkennung je Typ · HEIC wird mit **benannter** Meldung abgelehnt · >5 MiB
abgelehnt · Pfad-Traversal · fremdes Asset ohne Leserecht → 404 (nicht 403, kein Existenzleck) ·
Git-Commit entsteht.

#### Step 9 — Assets-UI
Knopf „Bild einfügen" (Picker) **und** Drop-Ziel im Editor (P6-AB); Vorschau löst `_assets/…`
relativ auf `/ui/assets/<space>/<name>` auf; Fortschritts- und Fehleranzeige; Markdown-Renderer
lässt `<img>` nur mit `src` aus der eigenen Herkunft zu (Sanitizer-Regel, kein `data:`-Bypass).

#### Step 10 — Abschluss
Abnahmeprotokoll `docs/concepts/P6_ABNAHME_<datum>.md` · `PHASE6_CLOSEOUT_HANDOVER.md` ·
`phase6_shares_uebersicht.svg` · ROADMAP/INDEX/Root-`CLAUDE.md` auf ✅ · Rotationsprüfung ·
Contract in `phase1_storage/CLAUDE.md` wieder schließen · offene Befunde (O4/O5) an P7 vererben ·
dritten Test-Nutzer entfernen (P6-W).

---

## §5 Testliste (Zusammenfassung)

| Datei | neu/erweitert | Schwerpunkt |
|---|---|---|
| `phase6_shares/tests/test_characterization.py` | neu | Golden Files, P6-D |
| `phase6_shares/tests/test_acl.py` | neu | Vererbung, fail-closed, Cache-Invalidierung |
| `phase6_shares/tests/test_patch.py` | neu | `apply_edits()` rein funktional |
| `phase6_shares/tests/test_spacectl.py` | neu | CLI, `_clean_environ()`-Muster (P5-Lehre!) |
| `phase6_shares/tests/test_migrate_visibility.py` | neu | Dry-Run ist Default, Report vollständig |
| `phase6_shares/tests/test_shares.py` | neu | `widens()`-Wahrheitstabelle |
| `phase6_shares/tests/test_updates.py` | neu | Parser |
| `phase6_shares/tests/test_assets.py` | neu | Magic Bytes, Limits, Traversal |
| `phase1_storage/tests/test_store.py` | erweitert | `patch`, `folder`, `acl_of`, `list_spaces` |
| `phase1_storage/tests/test_index.py` | erweitert | Schemaversion, neue Spalten |
| `phase2_mcp/tests/test_tools.py` | erweitert | siebtes Tool, Quittungen, Surface |
| `phase2_mcp/tests/test_permissions.py` | erweitert | `SharePolicy` |
| `phase5_ui/tests/test_api.py` | erweitert | `reauth_required`, Ordnerfilter, Serializer |
| `phase5_ui/tests/test_isolation.py` | erweitert | Surface-Trennung bleibt hart |

**Jede neue Testdatei, die Skripte gegen echte Systemkommandos testet, übernimmt `_clean_environ()`
— nicht `os.environ` erben.** (P5-Lehre: die Suite startete einmal den Produktivdienst 52-mal neu.)

---

## §6 Abnahmematrix

Statusregel unverändert: **✅ heißt live-verifiziert, nicht gebaut.**

| # | Kriterium | Wer |
|---|---|---|
| 1 | `patch_item` ändert drei Stellen in einem großen Dokument, ein Versionssprung, ein Git-Commit | Niklas |
| 2 | Mehrdeutiger `old_text` schlägt fehl, Datei unverändert (`git status` sauber) | Niklas |
| 3 | Quittung statt Volltext; `return_body=True` liefert den Volltext | Niklas |
| 4 | Purge räumt `clients`/`token_families` real ab (Zeilenzahl vorher/nachher) | Niklas |
| 5 | `ua`-Feld im Log unterscheidet zwei Claude-Oberflächen — **oder** der Befund steht, dass es das nicht tut | Niklas |
| 6 | Update-Banner erscheint, verschwindet nach „Verstanden", ist unter Einstellungen wiederfindbar | Niklas + Fabian |
| 7 | `deploy.sh` bricht ohne aktualisierten `UPDATE_LOG.md` ab | Niklas |
| 8 | Migration gelaufen: jedes Item trägt `visibility`, Report vollständig, Fabian sieht Niklas' Space **nicht** mehr | Niklas |
| 9 | Ein Ordner wird angelegt, ein Item hineingezogen, die Datei liegt real im Unterverzeichnis | Niklas |
| 10 | Ordner-Freigabe wirkt auf alle Items darin, ohne dass ein Item angefasst wurde | Niklas + Fabian |
| 11 | Ein einzelnes Item wird lesend freigegeben — Fabian sieht **nur** dieses | Fabian |
| 12 | `share_write` an einem Item: Fabian kann es ändern, ein Nachbaritem nicht | Fabian |
| 13 | Geteilter Space: beide legen Items an und ändern die des anderen | beide |
| 14 | Fremder Body ist auch im geteilten Space `<untrusted_content>`-gewrappt | Niklas (Connector) |
| 15 | `visibility: human`: in der UI sichtbar und gezählt, über den Connector **nirgends**, auch nicht in `total` | Niklas |
| 16 | Freigabe erweitern verlangt Re-Auth; Freigabe zurücknehmen nicht | Niklas |
| 17 | Kein MCP-Tool kann `share_*`/`visibility` setzen (Versuch → klarer Fehler) | Niklas (Connector) |
| 18 | Dritter Nutzer: Konto, Space, Connector, ein Schreibvorgang im geteilten Space | Niklas |
| 19 | Bild per Drag & Drop im Editor abgelegt → hochgeladen, Link eingefügt, Vorschau zeigt es | Niklas |
| 20 | Dasselbe Bild ist über den Connector nur ein Link, kein Binärinhalt | Niklas |
| 21 | HEIC wird mit begründeter Meldung abgelehnt | Niklas |
| 22 | Fremdes Asset ohne Leserecht → 404 | Fabian |
| 23 | Reboot: UI, Connector, Timer kommen ohne Handgriff zurück | passiv |
| 24 | Dritter Space nach der Abnahme entfernt, `diagnose.sh` meldet keine verwaisten Freigaben | Niklas |

---

## §7 `[VERIFY]`-Register

| # | Was | Wann |
|---|---|---|
| V39 | Reale `pytest`-Ausgangszahl (Plan behauptet 576, Stand Snapshot 2026-08-09) | Step 0 |
| V40 | Installierte Starlette-Version ≥ 1.0.1 (CVE-2026-48710) | Step 0 |
| V41 | Anthropic-Connector-Doku (Nachfolger V33): Grenzen für Tool-Anzahl/Schema/Beschreibung | Step 0 |
| V42 | Setzen reale MCP-Clients den `User-Agent` verlässlich? **Messen, nicht annehmen** | Step 2 |
| V43 | Exakte API von `webui/reauth.py` (Signatur, Marker-Lebensdauer) | Step 7 |
| V44 | Migrationsmechanik von `auth.sqlite3` Schema 2 → 3 (wie hat P5 es gemacht?) | Step 3 |
| V45 | Hook-Punkt in `deploy.sh` für das UPDATE_LOG-Gate | Step 3 |
| V46 | `index.connect()` kennt heute keinen Versionsbegriff — `PRAGMA user_version` einführen | Step 4 |
| V47 | Verhalten von `rebuild_index()` gegenüber `_archive/`, `_assets/`, `.share.yml` | Step 4 |
| V48 | Rendert `fastmcp` 3.4.x `list[TypedDict]` zu einem brauchbaren JSON-Schema? Fallback: `list[dict[str,str]]` + eigene Validierung | Step 1 |
| V49 | Uplink-Datenlimit (Nachfolger V12) **mit** Assets — endlich einmal bewerten | Step 8 |
| V50 | `<script type="module">` unter CSP `script-src 'self'` ohne Build-Step | Step 7 |
| V51 | Welcher YAML-Weg existiert im Repo für `.share.yml` — **kein zweiter Parser** | Step 4 |

Geerbt und weiterhin offen: **V12** (geht in V49 auf).

---

## §8 Risiken, ehrlich benannt

1. **Diese Phase löst die Garantie auf, die zwei Phasen lang der beste Beweis des Projekts war.**
   Der leere `git diff` auf `storage/`/`tools.py` ist ab Step 4 unmöglich. P6-D ist der Ersatz —
   **wenn die Charakterisierungstests gestrichen werden, hat diese Phase keinen Rückfallschutz.**
2. **Der Rechteumbau ist die erste Änderung des Projekts, bei der ein Fehler still Daten
   offenlegt** statt sichtbar abzubrechen. Deshalb fail-closed an jeder Stelle, deshalb die
   Pflichttests in Step 5, deshalb Abnahmezeilen 10–17 mit zwei Menschen.
3. **Die Migration (P6-L) fühlt sich für Fabian wie Datenverlust an**, wenn er den Update-Eintrag
   nicht gelesen hat. Block A vor Block B ist genau deshalb keine Geschmacksfrage.
4. **`app.js` splitten heißt, ungetesteten Code anzufassen.** Eigener Commit, jsdom davor/danach,
   sonst ist die Ursachensuche später nicht mehr eingrenzbar.
5. **Scope-Aufweichung ist in dieser Phase besonders billig** („ein Löschen wäre doch jetzt
   einfach…", „HEIC ist doch nur eine Zeile…"). Beides steht in §0.6/§1.7.2 mit Begründung
   draußen. Wer es aufmacht, macht dazu eine Nikinger-Entscheidung, keinen Commit.

---

## §9 Doku-Pflichten dieser Phase

| Datei | Was |
|---|---|
| `docs/INDEX.md` | Zeilen für diesen Plan, `phase6_shares/CLAUDE.md`, `docs/UPDATE_LOG.md`, später Abnahme + Handover + SVG |
| `ROADMAP.md` | P6-Zeile; datierte Korrektur an „Feingranulare Rechte" und „Mehrmandantenfähigkeit" |
| Root-`CLAUDE.md` | Hard Rule 4 neu gefasst (§0.7a); „Current state" auf 🔄 Phase 6 |
| `phase1_storage/CLAUDE.md` | dritte, benannte Contract-Öffnung — mit Datum wieder geschlossen in Step 10 |
| `phase2_mcp/CLAUDE.md` | siebtes Tool, `SharePolicy`, Quittungen |
| `phase5_ui/CLAUDE.md` | `app.js`-Split, neue Routen, Schema 3 |
| `phase4_auth/CLAUDE.md` | Befundtabelle: O2 geschlossen, ggf. S11 (Starlette), O4/O5 neu |
| `phase6_shares/CLAUDE.md` | Phase-Head, Modul-Tabelle, genau **ein** Session-Block (Rotation über `scripts/rotate_session_block.sh phase6_shares`) |
