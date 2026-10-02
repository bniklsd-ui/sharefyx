---
status: live
purpose: "Mini-Plan P9 Block trace — Nachvollziehbarkeit: wer arbeitet dran (`assignee`, sichtbar in UI und MCP, vom Client gesetzt) und wer hat zuletzt geändert (`updated_by`, vom Server aus dem Principal gesetzt, plus Git-Autor). Zehnte P1-Contract-Öffnung, angekündigt. Locks P9-Y–P9-AD, Abnahme P9-69–P9-82, [VERIFY] V179–V184 (V179/V180/V181/V183 in der Planung beantwortet)."
read-when: Bau des trace-Blocks (opencode/M3) oder Herkunft von `updated_by` / P9-Z nachvollziehen
detail: L2
up: ../../phase9_hardening/CLAUDE.md
down:
  - ./phase9_hardening_block_doing_plan.md   # 📕 Vorgänger-Block; `doing` + Eimer „In Arbeit"
  - ./phase9_hardening_plan.md               # 📕 übergeordneter P9-Plan; P9-P (Hervorhebung → P10) wird hier datiert eingeengt
updated: 2026-10-02 (§9 gefüllt, opencode/M3, ein Commit — 🔄 → 📕, ab jetzt nicht mehr editiert) | updated: 2026-10-02 (geschrieben, Claude Code, Planungssession nach dem Deploy `v3.1.0`; beide Kernentscheidungen vom Nikinger getroffen)
---

# Phase 9 — Block trace (wer arbeitet dran, wer hat zuletzt geändert)

> **Ein Block, kein Phasenplan.** Anlass: Nikinger-Frage nach dem Deploy `v3.1.0`
> (2026-10-02), was `doing` in einem Space mit zwei Personen bedeutet. Antwort heute: der Status
> ist geteilt (eine Datei für alle), aber **niemand wird aufgezeichnet** — weder im Item noch
> in Git. Dieser Block macht beides sichtbar, für Menschen (UI) **und** für ein angeschlossenes
> LLM (MCP).

## §0 Rahmen

### 0.1 Auftrag in drei Sätzen

1. `assignee` (seit P9 Step F im Datenmodell, heute in keiner UI-Zeile sichtbar) wird in Liste
   und Editor angezeigt und editierbar; beim Wechsel auf „In Arbeit" füllt **der Client** es
   mit dem eigenen Space, wenn es leer ist.
2. Neues **server-verwaltetes** Feld `updated_by` (wie `updated`): bei jedem Write aus dem
   authentifizierten Principal gesetzt, nie vom Client setzbar; dazu wird der Git-Commit im
   DATA_ROOT mit dem Schreiber als Autor angelegt.
3. MCP liefert beide Felder in jedem Item-/Trefferobjekt und sagt dem LLM in den
   Tool-Beschreibungen, wann es `assignee` setzen soll.

### 0.2 Gemessener Ausgangszustand (2026-10-02, Claude Code, read-only)

| Fakt | Beleg |
|---|---|
| Git im DATA_ROOT kennt keinen Schreiber | `git log -3 --format='%an'` → dreimal `Space Server`; Message `update <id> [<space>]` = **Ziel**-Space |
| `Store` bekommt keinen Akteur | Signaturen `store.py:572/618/679/699/751/934` u. a., kein Parameter |
| Beide Kanäle kennen den Akteur | MCP `Principal.space` (`auth.py:17`), UI `session.space` (`api.py`) |
| Person = Home-Space | `users.py` ist nach Space geschlüsselt — ein Mensch, ein Home-Space |
| `assignee` im UI unsichtbar | kein Treffer in `static/js/*.js` außer Kommentar `state.js:17`; `currentFormValues()` (`editor.js:166`) kennt es nicht |
| `assignee` über MCP setzbar | `update_item(assignee=...)` `tools.py:667`, `create_item` analog; REST-PATCH-Whitelist `api.py:856` |
| Listen-Zeilen kommen aus Dateien, nicht aus Index-Spalten | `search()` → `_row_to_item()` liest die Datei → `_summary()` ⇒ **für `updated_by` keine Index-Spalte, kein Schema-Sprung, kein Neuaufbau beim Deploy** |
| Space-Namen sind kaum eingeschränkt | `acl.create_space()` verbietet nur `/`, führenden `.` und reservierte Namen (`acl.py:281`) ⇒ V179 |

### 0.3 Scope

**Drin:** `phase1_storage/storage/{models.py,store.py,history.py}` (zehnte Öffnung, §3),
`phase2_mcp/mcpserver/tools.py`, `phase5_ui/webui/{api.py,serializers.py}`,
`phase5_ui/webui/static/{js/list.js,js/editor.js,js/state.js,app.html,app.css}`, Tests, Doku.

**Draußen:** Verlaufsansicht (wer hat wann was geändert, aus `git log`) — Option C, vom Nikinger
nicht gewählt, P10-Kandidat. `created_by` (der Ersteller steht als Autor im ersten Git-Commit
des Items, ein zweites Feld wäre Doppelung). Hervorhebung von `doing`-Zeilen (P9-P bleibt P10).
`index.py` (kein Schema-Sprung, s. 0.2). Jede Rückwirkung auf Altbestand (P9-AB).

### 0.4 Tabu (Bereichs-Diff über den Block-Commit)

Leer bleiben müssen: `phase1_storage/storage/{index.py,frontmatter.py,acl.py,files.py,patch.py}`,
`phase4_auth/**`, `phase3_edge/**`, `phase2_mcp/mcpserver/{auth.py,context.py,security.py}`.
**Enge Probe:** `git diff --stat -- phase1_storage/storage` zeigt **genau drei Dateien**
(`models.py`, `store.py`, `history.py`). Jede vierte ist Abbruchgrund — anhalten, vorlegen.

### 0.5 Hard Rules, die der Block berührt

- **Kernprinzip „der Server ist dumm":** `updated_by` ist Auth-Buchhaltung (der Server *macht*
  Auth laut CLAUDE.md), kein Inhaltsverständnis. Die Regel „beim Wechsel auf `doing` `assignee`
  füllen" gibt einem Statuswert Bedeutung — **deshalb sitzt sie beim Client** (P9-Z), nicht im
  Server.
- **HR 3:** unverändert. Das Feld entsteht im selben Write, derselbe Versionssprung, kein
  zusätzlicher Write.
- **HR 4:** `updated_by`/`assignee` sind Space-Namen. Im MCP-Ergebnis eines fremden Items stehen
  sie im Frontmatter-Teil, nicht im `<untrusted_content>`-Body — sie sind vom Server gesetzt
  (`updated_by`) bzw. bereits heute dort (`assignee`). Kein neuer Injection-Pfad, aber V182.
- **HR 5:** Git-Autor ändert nichts an „ein Commit je Write".

## §1 Gelockte Entscheidungen

| Lock | Inhalt | Herkunft |
|---|---|---|
| **P9-Y** | Umfang = (A) `assignee` sichtbar + (B) `updated_by` + Git-Autor. Keine Verlaufsansicht. | Nikinger 2026-10-02 („Who + last editor") |
| **P9-Z** | `assignee` füllt **der Client**: die UI beim Wechsel auf `doing`, das LLM per Tool-Hinweis. Ein **gesetztes** `assignee` wird nie automatisch überschrieben. Ein Wechsel weg von `doing` leert es **nicht** (es bleibt als Spur; ein Mensch leert es von Hand). | Nikinger 2026-10-02 („Client fills it") + Planung |
| **P9-AA** | `updated_by` = Home-Space des Principals, in `_SYSTEM_MANAGED_FIELDS`, über **kein** MCP-Tool und **keine** REST-Route setzbar (ein mitgeschicktes Feld ist `ValidationError`, wie heute `updated`). Frontmatter-Feld, **keine** Index-Spalte. | Planung, §0.2 |
| **P9-AB** | Akteur leer (`actor=""`: Operator-Skripte, Tests, Drift-Abgleich) ⇒ `updated_by` bleibt **unverändert** — lieber der alte, wahre Wert als ein erfundener. Altbestand ohne Feld bleibt ohne Feld, **kein Backfill**, und es wird nie ein leeres `updated_by:` geschrieben (dasselbe Muster wie `assignee` F6, `store.py:206`). | Planung, Präzedenz P9-42 |
| **P9-AC** | Git: `history.commit(..., author=actor)` setzt `--author "<actor> <actor@sharefyx.invalid>"`; Committer bleibt `Space Server`. Ein Name mit `<`, `>` oder Zeilenumbruch ⇒ kein `--author`, `logger.warning`, Commit läuft trotzdem (nie fatal, `history.py`-Vertrag). | Planung, V179 |
| **P9-AD** | `actor` ist ein **optionales** Keyword (`actor: str = ""`) an allen Store-Schreibmethoden — 294 Test-Aufrufe von `create()` blieben sonst rot. Der Schutz gegen eine vergessene Aufrufstelle ist **ein Wächter-Test** über die Adapter (§4 T7), nicht der Typ. | Planung, gemessen |

**Datierte Einengung von P9-P** (`phase9_hardening_plan.md` §1): „Hervorhebung von `doing` → P10"
bleibt; die **Anzeige von `assignee` als Text** in der Metazeile ist keine Hervorhebung,
sondern Information, und gehört in diesen Block.

## §2 Verworfene Alternativen (Argument, kein Geschmack)

- **Server füllt `assignee` bei `doing`** — gäbe dem Server Statussemantik (Kernprinzip). Vom
  Nikinger abgewählt.
- **`actor` als Pflichtparameter** — fängt jede vergessene Stelle per `TypeError`, kostet aber
  ~400 Testanpassungen in fremden Phasen. Der Wächter T7 fängt dieselbe Klasse in den beiden
  Adapter-Paketen, in denen sie entstehen kann.
- **`actor` im Store-Konstruktor** — ein Store bedient beide Principals gleichzeitig (MCP und UI
  im selben Prozess); ein Akteur pro Instanz wäre falsch, sobald zwei Personen schreiben.
- **Index-Spalte `updated_by`** — nur nötig, um danach zu filtern; das will niemand. Kostete
  Schema v5 und einen weiteren Neuaufbau beim Deploy.
- **Akteur nur in der Commit-Message** — `--author` ist das Feld, das `git log --format=%an`,
  `git blame` und jedes Werkzeug lesen; die Message bleibt unverändert, damit bestehende Parser
  (Tests auf `"<op> <id> [<space>]"`) nicht brechen.

## §3 Zehnte P1-Contract-Öffnung (angekündigt, datiert 2026-10-02)

Wortlaut für `phase1_storage/CLAUDE.md` §Geerbte Contracts (M3 trägt die Zeile im Block-Commit
ein, Nummer = nächste freie): *„Zehnte, benannte Öffnung (P9 Block trace, P9-AA–P9-AD): `Item`/
`ItemSummary` bekommen `updated_by: str = ""`; `updated_by` steht in `_KNOWN_FIELDS` und
`_SYSTEM_MANAGED_FIELDS`; `create/update/append/patch/archive/move` nehmen `actor: str = ""` und
setzen `updated_by` nur bei nicht-leerem Akteur; alle Schreibmethoden inkl. `trash/put_asset/
delete_asset` reichen `actor` an `history.commit(author=)` durch. Kein Index-Schema-Sprung."*

## §4 Bauschritte (opencode/M3, **ein** Commit)

**T1 `models.py`:** `updated_by: str = ""` an `Item` und `ItemSummary` (nach `assignee`).

**T2 `store.py`:**
- `_KNOWN_FIELDS` += `"updated_by"`; `_SYSTEM_MANAGED_FIELDS` += `"updated_by"`.
- `_item_from_text`: `updated_by=str(fields.get("updated_by", "") or "")`.
- `_item_to_text`: `if item.updated_by: fields["updated_by"] = item.updated_by` (P9-AB, Muster
  `store.py:206`).
- `_summary`: `updated_by=item.updated_by` (sonst totes Feld — exakt der Fund F10 aus Step F).
- `create`/`update`/`append`/`patch`/`archive`/`move`: `actor: str = ""`; im `replace(...)`
  bzw. `Item(...)` `updated_by=actor or current.updated_by` (`create`: `actor`).
- `_write_item_file(..., actor="")` → `_commit(op, id, space, actor)`; ebenso die direkten
  `_commit`-Aufrufe in `archive` (`:748`), `put_asset` (`:863`), `delete_asset` (`:932`),
  `trash` (`:979`). Der Drift-Commit (`:311`) bekommt **keinen** Akteur.
- `trash` schreibt die Datei nicht neu ⇒ `updated_by` im Papierkorb bleibt der letzte Editor;
  der Löschende steht als Git-Autor. **So gewollt, nicht nachbessern.**

**T3 `history.py`:** `commit(data_root, message, author: str = "")`; Prüfung P9-AC;
`_run_git(..., "commit", "-m", message, *(["--author", f"{author} <{author}@sharefyx.invalid>"] if ok else []))`.

**T4 `tools.py` (MCP):**
- Jeder Store-Schreibaufruf (`:622, :748, :755, :759, :798, :836, :963` + alle weiteren, die
  der Wächter T7 findet) bekommt `actor=principal.space`.
- `item_to_filetext` (`:185`), `summary_to_dict` (`:212`) und das JSON-Item: `updated_by`
  ausgeben, wenn gesetzt (gleiches Muster wie `assignee`).
- Neue Konstante `_ASSIGNEE_HINT`, **wörtlich identisch** in `create_item` und `update_item`:
  *„Setzt du eine Aufgabe auf status doing und ist assignee leer, setze assignee auf deinen
  eigenen Space (list_spaces: own:true). Ein gesetztes assignee überschreibst du nur, wenn ein
  Mensch es ausdrücklich sagt. updated_by setzt der Server — du kannst es lesen, nicht
  schreiben."*
- `update_item`/`create_item` bekommen **keinen** `updated_by`-Parameter.

**T5 `api.py` + `serializers.py` (REST):**
- Jeder Store-Schreibaufruf (`:608, :610, :859, :1001, :1003, :1078, :1104, :1145, :1176,
  :1237`) bekommt `actor=session.space`. `:608` (Space-Entfernen verschiebt fremde Items in den
  Home-Space) ist ein Mensch-Akt ⇒ ebenfalls `session.space`.
- `item_to_json`/`summary_to_json`: `"updated_by": item.updated_by`.
- PATCH-Whitelist (`:856`) bekommt `updated_by` **nicht**.

**T6 UI:**
- `list.js :: itemMetaLine()`: bei `item.assignee` zusätzlich `"bei " + item.assignee` (nach
  Status, vor Fälligkeit). Kein `updated_by` in der Listenzeile (Rauschen).
- `app.html` Meta-Panel: Eingabefeld `#field-assignee` (Text, `list="assignee-options"`,
  Datalist aus `state.spaces`-Namen) und eine Lesezeile `#meta-updated-by`
  („zuletzt geändert von X · Datum", leer bei Altbestand). `ro-meta` (fremde Items,
  `editor.js:350`) bekommt beide Angaben als Text.
- `editor.js`: `assignee` in Snapshot (`:93`), `currentFormValues()`, `isDirty()`,
  `renderMetaDigest()` (`"bei X"`), Laden (`:373`) und Draft-Wiederherstellung (`:399`).
- **P9-Z im Editor — der einzige UI-Pfad, der `status` schreibt** (gemessen 2026-10-02: die
  übrigen PATCH-Bodies `list.js:261/345`, `dialogs.js:860/1011` tragen nur `folder`/`space`/
  Freigaben; ein künftiger Status-Pfad muss denselben Zweig bekommen): `fieldStatusEl` `change` → wenn neuer Wert `"doing"` **und**
  `fieldAssigneeEl.value.trim() === ""` → `fieldAssigneeEl.value = state.ownSpace`, dann
  `renderMetaDigest()`. Kein anderer Zweig fasst `assignee` an.
- Speichern: `assignee` geht wie `status` in den PATCH-Body. `saveItem()` (`editor.js:500`)
  schickt den **ganzen** Formularstand (V180) — ein unverändertes `assignee` steht also mit dem
  Schnappschuss-Wert im Body; das ist kein Überschreiben.

**T7 Tests (Liste, Mindestumfang):**

| # | Datei | Behauptung |
|---|---|---|
| 1 | `phase1_storage/tests/test_store.py` | `create(actor="a")` → Datei trägt `updated_by: a`, `get()` und `search()` liefern `a` |
| 2 | dto. | `update(actor="b")` auf Item von `a` → `b`; Version +1, **ein** Commit |
| 3 | dto. | `update(actor="")` → `updated_by` unverändert (P9-AB) |
| 4 | dto. | Altbestand ohne Feld + `update(actor="")` → Datei enthält **kein** `updated_by:` |
| 5 | dto. | `create(updated_by="x")` und `update(updated_by="x")` → `ValidationError` |
| 6 | `phase1_storage/tests/test_history.py` | Commit mit `author="niklas"` → `%an` = `niklas`, `%cn` = `Space Server`; `author="a<b"` → Default-Autor, Warnung, Commit da |
| 7 | `phase9_hardening/tests/test_trace_block.py` | **Wächter:** AST über **jedes Nicht-Test-Modul** unter `phase2_mcp/mcpserver/` und `phase5_ui/webui/` (nicht nur `tools.py`/`api.py` — ein künftiges Modul fiele sonst durch) — jeder Store-Aufruf `.<create|update|append|patch|archive|move|trash|put_asset|delete_asset>(` trägt ein `actor=`-Keyword. Ausnahmen nur über eine **benannte** Allowlist im Test (heute leer, s. V183) |
| 8 | dto. | MCP `update_item` als Principal B auf ein Item in einem geteilten Space → `updated_by: B`, `assignee` von A unverändert |
| 9 | dto. | MCP-Beschreibungen von `create_item` und `update_item` enthalten `_ASSIGNEE_HINT` wörtlich; `update_item` hat keinen Parameter `updated_by` |
| 10 | `phase5_ui/tests/test_api*.py` | REST-PATCH mit `updated_by` im Body → **422** `validation_failed` „Unbekannte Felder“ (gemessen: `_PATCH_FIELDS`-Prüfung `api.py:892`, Status `errors.py:50`) **und** die Datei bleibt unverändert; PATCH als `session.space` → Antwort trägt `updated_by` |
| 11 | `phase5_ui/tests/test_static_routes.py` | `editor.js` enthält den P9-Z-Zweig (`"doing"` + leer-Prüfung) und **keine** andere Zuweisung an `fieldAssigneeEl.value` außer Laden/Draft |

**Gegenlauf (Pflicht, Repo-Konvention):** je Verstoß einmal einbauen, Rotzahl notieren, zurück.
G1 `actor=` an **einer** `tools.py`-Stelle entfernen → T7 rot · G2 `updated_by` aus
`_SYSTEM_MANAGED_FIELDS` → T5/T10 rot · G3 `updated_by=actor or current.updated_by` → `=actor`
→ T3 rot · G4 P9-Z ohne Leer-Prüfung → T11 rot · G5 `--author` weglassen → T6 rot. **Ein
Verstoß, der nichts rot macht, heißt: Wächter wertlos, neu schneiden** (doing-Block §12.3).

**T8 Browser-Beleg** (Standing-Permission, Wegwerf-Instanz, eigener Port, tmp-DATA_ROOT,
`sichtpruefung_automation_conventions.md` Technik 4 „zwei unabhängige Principals"):
S1 A öffnet eine offene Aufgabe in einem geteilten Space, wählt „In Arbeit" → `#field-assignee`
zeigt `A` **vor** dem Speichern · S2 Speichern → Listenzeile „… doing · bei A" · S3 B lädt →
sieht die Aufgabe in „In Arbeit", Metazeile „bei A", Meta-Panel „zuletzt geändert von A" ·
S4 B ändert den Titel → „zuletzt geändert von B", `assignee` weiter `A` · S5 B setzt eine
Aufgabe mit `assignee: A` auf `doing` → bleibt `A` (P9-Z) · S6 `git -C <tmp-DATA_ROOT> log
--format=%an -3` → `B, A, …` · S7 Altbestand-Item ohne Feld → keine leere Zeile, keine
„von undefined". Gegenlauf mit G4 (≥ S1/S5 rot). Screenshots `p9_trace_*`,
`screenshots_latest/` umhängen. **Prüfskript darf bei fehlendem Element nicht abstürzen,
sondern rot melden** (doing-Block, Befund B4).

**T9 Doku (Hard Rule 8, selber Commit):** Phase-Head Modulstatus-Zeile `trace` + Session-Block
(Rotation per Skript, neuer Block **ans Dateiende**), `phase1_storage/CLAUDE.md` Contract-Zeile
(§3), `phase2_mcp/CLAUDE.md` + `phase5_ui/CLAUDE.md` Modulstatus je eine Zeile, dieser Plan §9
Ergebnis, `docs/INDEX.md`, Wurzel-Current-state, `doc_health` 0.

## §5 Selbstprüfung vor dem Commit

`pytest -q` grün (Baseline **1128**) · `ui_budget` 5/5 · enge Probe §0.4 = drei Dateien · Tabu
leer · `doc_health` 0 · **und ein frisches venv** (`python3 -m venv` + `scripts/dev_install.sh`
+ `pytest -q`, aus einem `git clone` — nicht `git archive`, sonst ist der Backup-Test rot),
weil der Deploy genau dort prüft (Lehre vom 2026-10-02). Kein `pkill -f`, kein `systemctl`.

## §6 Deploy (Nikinger, NICHT Teil des Blocks)

Kein Schema-Sprung ⇒ kein Index-Neuaufbau. Badge-Vorschlag **`v3.1.1`** (Patch: neue Anzeige,
keine neue Navigation); die Versionsnummer entscheidet der Nikinger. Release-Commit wie
`bdecfde` (Badge + `UPDATE_LOG`-Block mit Deploy-Datum), dann `deploy.sh main` +
`health_gate.sh --expected-version=<…> --require-todays-update-log --expected-sha=<…>`.
**Nach dem Deploy erwartbar:** alle bestehenden Items zeigen kein „zuletzt geändert von", bis
sie das erste Mal geschrieben werden (P9-AB) — Eigenschaft, kein Fehler; in den
Changelog-Text.

## §7 Abnahme (P9-69 – P9-82)

`P9-69` enge Probe = drei Dateien · `P9-70` T1–T6 grün · `P9-71` Wächter T7 grün und mit G1 rot
· `P9-72` MCP liefert `updated_by` in `get_item`, `search_items` und Schreibantworten · `P9-73`
`_ASSIGNEE_HINT` an beiden Tools wörtlich · `P9-74` kein Kanal kann `updated_by` setzen ·
`P9-75` Altbestand bleibt ohne Feld · `P9-76` Git-Autor = Schreiber, Committer unverändert ·
`P9-77` UI: „bei X" in der Liste · `P9-78` UI: Editorfeld + „zuletzt geändert von" · `P9-79`
P9-Z: Auto-Füllen nur bei leer, nie überschreiben · `P9-80` Browser S1–S7 grün, Gegenlauf rot ·
`P9-81` Gegenlauf G1–G5 jeder ≥ 1 rot · `P9-82` frisches venv grün.

## §8 `[VERIFY]`

- **V179 ✅ (2026-10-02, Planung)** Echte Space-Namen: `fabian`, `Home-Server`,
  `IT-Sekus-Projekt`, `Janick`, `niklas` — keiner berührt P9-AC. Die Prüfung bleibt, weil
  `create_space()` mehr erlaubt. Ein führendes `-` ist unkritisch: `--author` bekommt den Wert
  als eigenes argv-Element. **Nebenbefund, nicht Teil des Blocks:** im DATA_ROOT liegt ein
  Eintrag namens wörtlich `*.sqlite3` (vermutlich ein nicht expandierter Shell-Glob) — dem
  Nikinger gemeldet, nicht angefasst.
- **V180 ✅** `saveItem()` schickt den ganzen Formularstand (`editor.js:500–503`).
- **V181 ✅** `api.py:1001/1003` ist `if/else` — ein Request, ein Store-Aufruf, ein Commit.
- **V182** Taucht `updated_by` eines fremden Items im MCP-Ergebnis innerhalb oder außerhalb von
  `<untrusted_content>` auf? Erwartet außerhalb (Frontmatter-Teil); wenn innerhalb, ist es
  harmlos, aber zu notieren.
- **V183 ✅** `grep` über alle Nicht-Test-Quellen: außerhalb von `tools.py`/`api.py` schreiben
  nur Operator- und Fixture-Skripte (`phase1_storage/scripts/space_cli.py`, `*/scripts/wegwerf_*`,
  `p7_*_fixture.py`, `mcp_smoke.py`, `ui_smoke.py`, `ui_budget.py`) — alle bleiben bei
  `actor=""` (P9-AB). Kein weiteres `webui/`- oder `mcpserver/`-Modul schreibt; die
  T7-Allowlist ist deshalb heute leer.
- **V184** `state.ownSpace` ist beim Öffnen des Editors immer gesetzt (sonst füllt P9-Z
  `undefined`)?

## §9 Ergebnis

**Bilanz: 8 ✅ · 1 ⚠️ · 0 ⬜** (P9-69 – P9-82), `pytest` **1128 → 1152** (24 neue Tests — im frischen venv gezählt, nicht addiert),
`ui_budget` 5/5 (**155,1 KB**), enge Probe §0.4 = **genau drei Dateien** (`models.py`,
`store.py`, `history.py`), Tabu-Bereichs-Diff leer, `doc_health` 0, **kein `pkill -f`, kein
`systemctl`**, `sharefyx-mcp` nicht angefasst.

| # | Abnahmezeile | Stand | Beleg |
|---|---|---|---|
| P9-69 | enge Probe = drei Dateien | ✅ | `git diff --stat -- phase1_storage/storage` → `history.py`, `models.py`, `store.py` |
| P9-70 | T1–T6 grün | ✅ | 5 Tests `test_store.py` + 4 `test_history.py` |
| P9-71 | Wächter T7 grün und mit G1 rot | ✅ | `test_trace_block.py::test_every_store_write_call_in_the_adapters_carries_an_actor`; G1 → **1 rot** |
| P9-72 | MCP liefert `updated_by` in `get_item`, `search_items` und Schreibantworten | ✅ ⚠️ | `test_read_paths_and_the_receipt_carry_updated_by` — **eine Datei mehr als §0.3 vorsah:** `mcpserver/receipts.py` (Schreibantwort). Begründung unten |
| P9-73 | `_ASSIGNEE_HINT` an beiden Tools wörtlich | ✅ | `test_both_write_tools_carry_the_assignee_hint_verbatim` (prüft zusätzlich die *nicht*-überschreiben-Hälfte) |
| P9-74 | kein Kanal kann `updated_by` setzen | ✅ ⚠️ | Store `ValidationError` · PATCH `422` · kein MCP-Parameter · **POST verwirft lautlos** (Abweichung, unten) |
| P9-75 | Altbestand bleibt ohne Feld | ✅ | `test_legacy_item_without_the_field_never_gets_an_empty_one` + Browser S7 (Lesezeile **weg**, kein „unbekannt") |
| P9-76 | Git-Autor = Schreiber, Committer unverändert | ✅ | `test_commit_sets_the_author_and_leaves_the_committer_at_the_default` + **live im Wegwerf-`DATA_ROOT`**: `git log --format=%an -3` → `beta, alpha, alpha` |
| P9-77 | UI: „bei X" in der Liste | ✅ | Browser S2 (`task · doing · bei alpha`), statisch `test_the_list_meta_line_shows_the_assignee` |
| P9-78 | UI: Editorfeld + „zuletzt geändert von" | ✅ | Browser S1/S3/S4, `test_the_meta_panel_has_an_assignee_field_and_a_readonly_updated_by_line` |
| P9-79 | P9-Z: Auto-Füllen nur bei leer, nie überschreiben | ✅ | Browser S1 (`'' → alpha`) und S5 (`alpha → alpha`); Gegenlauf **S5 rot** (`alpha → beta`) |
| P9-80 | Browser S1–S7 grün, Gegenlauf rot | ✅ | `probes/p9_trace_probe.json` **8/8**; mit G4 **7/8** (S5 rot, `alpha → beta`) |
| P9-81 | Gegenlauf G1–G5 jeder ≥ 1 rot | ✅ | G1→**1** · G2→**2** · G3→**1** · G4→**2** · G5→**4** |
| P9-82 | frisches venv grün | ✅ | siehe unten |

### Drei Dinge, die der Plan nicht wusste

**1. Die Klammer in P9-AA war für eine Route ungenau (P9-74 ⚠️).** P9-AA sagt „ein
mitgeschicktes Feld ist `ValidationError`, wie heute `updated`". Gemessen: für **PATCH** stimmt
das (`422 validation_failed`, `api.py:890`) und für den Kern (`_SYSTEM_MANAGED_FIELDS`), für
**POST** nicht — `_items_post` hat keine `unknown`-Prüfung, sondern filtert **lautlos** auf eine
Whitelist. Ein `updated_by` im POST-Body wird also still verworfen, dieselbe Eigenschaft, die
heute `created`/`version`/`space` dort haben. **Nicht vereinheitlicht:** eine `unknown`-Prüfung im
POST würde jedes unbekannte Feld ablehnen und damit Round-Trips über Schreib-Clients brechen,
die den vollen Item-JSON zurückschicken. Beide Stellen im Code kommentiert.

**2. P9-72 verlangte eine Datei, die §0.3 nicht listet (P9-72 ⚠️).** „Schreibantworten" — die
**Standard**-Antwort jedes Schreib-Tools ist die *Quittung* (`receipts.py :: write_receipt()`),
nicht der Dateitext (`return_body=True`). Ohne diese eine Zeile hätte ein Agent nach einem
fremden Write genau die Antwort nicht bekommen, in der er nachschaut. `receipts.py` ist
bewusst nicht in §0.3 — und nicht in §0.4s Tabu-Liste; die Abweichung ist eine Zeile plus ein
Kommentar.

**3. Zwei Wächter aus dem Bestand kamen mit und wurden datiert behandelt.**
- `test_app.py::test_all_ten_tools_are_callable_over_http` prüft die Patch-Quittung als
  **exaktes Dict** und war der erste Ort, an dem die neue Zeile auffiel. Die Assertion nennt
  jetzt `updated_by: alpha` — und ist damit nebenbei der Beleg dafür, dass der Akteur aus dem
  **Token** kommt, nicht aus dem Aufruf.
- `test_step_f_schema.py::test_the_editor_status_dropdown_reads_the_vocabulary` verbot
  **jedes** Vorkommen von `assignee|doing` in `editor.js`. P9-Z verlangt genau das Gegenteil:
  „bei `doing` füllen" lässt sich nicht ohne den Namen des Statuswerts ausdrücken. Der Wächter
  ist **zugeschnitten, nicht entfernt**: keine abgetippte Vokabular-*Liste* in
  `populateStatusSelect()`, aber genau **eine** benannte Verzweigung mit Leer-Prüfung. Der
  Docstring trägt beide Richtungen mit Datum.

### Und ein Fund drei Phasen entfernt

`phase7_spaces_admin/tests/test_space_removal.py` hatte eine **Doppelgängerin** für
`Store.move()` mit eigener Signatur (`version, space=None, folder=None`). Das neue `actor=`
machte daraus einen `TypeError` — als **HTTP 500 mitten im Space-Entfernen**, also genau an der
Stelle, an der ein halb gelaufener Space-Entferner am teuersten ist. **Die Lektion ist die aus
P9-AD, an ihrem Gegenstück gemessen:** ein optionales Keyword hält *Aufrufstellen* heil, nicht
*Attrappen mit eigener Signatur*. Der Wächter T7 scannt nur Nicht-Test-Module und fängt diese
Klasse per Konstruktion **nicht** ab — sie wird in fremden Phasen erfunden.

### Was nicht gebaut wurde, mit Argument

Verlaufsansicht aus `git log` (P9-Y nicht gewählt, P10-Kandidat) · `created_by` (steht bereits
als Autor im ersten Git-Commit **des Items**) · Index-Spalte (niemand filtert danach, kostete
Schema v5 und einen weiteren Neuaufbau) · `actor` als Pflichtparameter (P9-AD, ~400
Testanpassungen in fremden Phasen) · ein `--author` mit Namensvalidierung über Space-Namen
(P9-AC: `<`, `>` und Zeilenumbruch ⇒ Warnung, Commit läuft trotzdem — `history.py`s Vertrag
„ein Write scheitert nie an Git" hat Vorrang).

### Deploy (Nikinger, nicht Teil des Blocks)

Badge `v3.1.0` → **`v3.1.1`** in `app.html:20`, neuer `## <Deploy-Tag>`-Block in
`docs/UPDATE_LOG.md` (P6-X-Gate), dann `deploy.sh main` und
`health_gate.sh --expected-version=v3.1.1 --require-todays-update-log --expected-sha=<sha>`.
**Nach dem Deploy erwartbar:** jedes bestehende Item zeigt **kein** „Zuletzt geändert von", bis
es das erste Mal geschrieben wird (P9-AB) — Eigenschaft, kein Fehler, gehört in den
Changelog-Text. **Kein Index-Neuaufbau** (kein Schema-Sprung) — anders als nach Step F.
