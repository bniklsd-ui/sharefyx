---
status: live
purpose: Zusatzplan zu P6 — „über alle lesbaren Items suchen"-Modus in der Web-UI (Deploy-Blocker vom 2026-08-18)
read-when: bevor der Deploy-Blocker gebaut wird, oder wenn geklärt werden muss, warum ein item-level geteiltes Item in der UI unauffindbar war
detail: L2
up: ./CLAUDE.md
down: ../docs/concepts/phase6_shares_plan.md §1.2 (Rechtemodell) · ./ITEM_MOVE_PLAN.md (Muster)
updated: 2026-08-19 (gebaut + Playwright-verifiziert gegen Wegwerf-Instanz, 10/10 gruen; Q1 vom Nikinger entschieden -- nur Titel/Tags; V57/V58 geschlossen; ein Advisor-Fund vor dem Commit behoben, editor.js clearDetail() setzt state.scope jetzt zurueck)
---

# GLOBAL_SEARCH_PLAN.md — „Alle Items" als eigener Suchbereich (P6, Zusatzplan)

> **Ein Satz:** Der Server kann global über alle lesbaren Items suchen **schon heute** — die
> Web-UI fragt nie danach. Dieser Plan macht den vorhandenen Modus in der Oberfläche erreichbar
> und stopft die drei Fallen, die eine naive Umsetzung sofort zu einem Fix-förmigen No-Op machen
> würden.
>
> **Muster:** Zusatzplan im Phase-Verzeichnis, wie `ITEM_MOVE_PLAN.md` — kein
> Konzept+Plan+Handover-Trio. Begründung für ein **eigenes** Dokument statt einer Erweiterung von
> `ITEM_MOVE_PLAN.md`: jenes steht bei ~39 KB dicht am 40-KB-Softcap (`docs/INDEX.md` vermerkt das
> ausdrücklich), und thematisch ist „Suchen/Finden" ein anderes Konzept als „Verschieben".

---

## §0 Herkunft und Befundlage

**Auslöser:** sophistizierter E2E-Lauf gegen eine Wegwerf-Instanz am 2026-08-18
(`phase6_shares/CLAUDE.md`, aktueller Session-Block, „Zwei echte Funde", Punkt 2). `beta` fand ein
Item, das `alpha` ihm ausschließlich item-level freigegeben hatte (`share_write: [beta]`, **kein**
space-level Grant in `alpha`s `.share.yml`), über die Web-UI nicht — 0 Treffer. Über den
MCP-Connector funktioniert dasselbe Szenario nachweislich.

**Nikinger-Entscheidung 2026-08-18:** echter Bug, **Blocker für den nächsten Deploy**.

### §0.1 Was diese Planungssession im Code nachgeprüft hat (2026-08-19, nicht übernommen, gelesen)

| Behauptung aus dem Session-Block | Prüfung | Ergebnis |
|---|---|---|
| `GET /api/v1/spaces` filtert über `permissions.visible_spaces()` (reines space-level `can_read`) | `webui/api.py :: _visible_space_infos()` (~Z. 247–261) → `_visible_spaces()` (Z. 222) → `SharePolicy.visible_spaces()` (`mcpserver/permissions.py` Z. 97) → `can_read()` (Z. 48) → `grants_for_space()` | **bestätigt.** Ein Space ohne space-level Grant taucht im Baum nie auf. Das ist **kein Bug** und wird von diesem Plan **nicht** geändert. |
| `list.js` setzt `params.set("space", state.activeSpace)` | `list.js :: loadItems()` Z. 320 | **bestätigt**, wörtlich. |
| Die Suche filtert serverseitig auf genau einen Space | `api.py :: _items_get()` Z. 334–344 reicht `space=q.get("space")` an `store.search()` durch | **bestätigt** — **aber nur, wenn der Parameter gesetzt ist.** |
| **NEU, der eigentliche Hebel** | `store.search()` (`storage/store.py` Z. 382–420): `if space is not None and item.space != space: return False` — bei `space=None` **kein** Space-Filter. `_items_get` filtert danach bereits **item-weise** über `permissions.can_read_item_as_human(session.space, _acl_for_summary(i))` (Z. 352–355) | **`GET /api/v1/items` ohne `space`-Parameter IST bereits die globale, item-weise ACL-gefilterte Suche.** Kein neuer Endpunkt nötig. |
| `GET /api/v1/items/{id}` öffnet ein solches Item | `_items_get_one()` Z. 400–409: `store.acl_of(item_id)` + `can_read_item_as_human` — **keine** Space-Sichtbarkeitsprüfung | **bestätigt.** Ein Treffer aus dem globalen Modus lässt sich anklicken und öffnen, ohne dass sein Space je im Baum stand. |

**Damit ist der Befund präzisiert:** es ist ein reiner Frontend-Fund plus **eine** kleine,
prinzipiengetriebene Serveränderung (§1.3, Snippet). Kein neuer Endpunkt, keine neue Route, kein
Eingriff in `permissions.py`, `acl.py` oder `storage/`.

### §0.2 Kostenbefund (relevant, weil er eine naheliegende Sorge ausräumt)

`Store.search()` liest **immer** alle Indexzeilen (`index.all_rows`) und für jede Zeile die
Item-Datei von der Platte (`_row_to_item()` → `path.read_text()`, `store.py` Z. 210–222). Der
`space`-Filter wirkt erst **danach**, in der `matches()`-Closure. Ein globaler Suchlauf kostet
deshalb **exakt so viel wie jede heutige Suche** — er wirft nur weniger weg. Der Wegfall des
`space`-Parameters ist kostenneutral. (Die Grundkosten selbst — P6-S, ~438 ms für
`GET /api/v1/overview` bei 220 Items — bleiben unverändert und sind **nicht** Scope dieses Plans.)

---

## §1 Gelockte Entscheidungen (P6-AO – P6-AT)

| # | Entscheidung | Begründung |
|---|---|---|
| **P6-AO** | **Kein neuer Endpunkt, keine neue Route.** Der globale Modus ist `GET /api/v1/items` **ohne** `space`-Query-Parameter. | Der Pfad existiert bereits und ist bereits item-weise ACL-gefiltert (§0.1). Ein zweiter Endpunkt wäre eine zweite Rechteprüfung, die divergieren kann — genau die Klasse Fehler, die `SharePolicy` in Step 5 zusammengeführt hat. |
| **P6-AP** | **Der Modus ist ein eigenes, explizites Zustandsfeld `state.scope` (`"space"` \| `"all"`), nicht `state.activeSpace === null`.** `state.activeSpace` bleibt im globalen Modus **unverändert stehen** (letzter Space, für den Rückweg). | `activeSpace === null` ist heute ein rein defensiv abgefangener, nie erreichter Zustand (`app.js` Z. 164 setzt ihn beim Boot, nur `activateView()` schreibt ihn danach). Ihn mit „global" zu belegen, hängt neue Bedeutung an ein Feld, das schon eine hat — dieses Repo wurde von genau dieser Klasse zweimal getroffen (`ownSpaceActive()`-Fund 2026-08-13, `state.filter=null`-Fund Step 7 Commit 1). |
| **P6-AQ** | **`scope: "all"` löscht `state.filter` UND `state.folder`** (beide auf `null`), genau wie `navigate()`/`navigateFolder()` sich gegenseitig ausschließen. `filterParams()` liefert im globalen Modus `{}`. | **Die Falle, die den Fix sonst wertlos macht:** `state.filter` steht per Default auf `"open"`, `filterParams()` würde daraus `type=task&status=open` machen. Eine globale Suche nach einer fremden **Notiz** hätte weiterhin 0 Treffer — ein Fix-förmiges No-Op, das wie ein Erfolg aussieht. |
| **P6-AR** | **Im globalen Modus sind alle Schreib-Bedienelemente aus dem DOM ausgehängt** (`setCreateControlsPresent(false)`), und `movable` je Zeile bleibt unverändert (`!item.readonly && item.space === state.ownSpace`). | Akzeptanzkriterium 12 aus P5 („kein Schreib-Bedienelement im DOM") wörtlich weitergeführt. Der globale Modus hat keinen Ziel-Space — „hier anlegen" ist dort sinnlos, nicht nur unerlaubt. |
| **P6-AS** | **Serverseitig wird `snippet` für Zeilen aus einem fremden Space im globalen Modus weggelassen** (`serializers.py :: summary_to_json(..., include_snippet: bool = True)`), analog zu `overview_row_to_json()`. Beim bewussten Betreten eines fremden Spaces (`space`-Parameter gesetzt) bleibt `snippet` erhalten, unverändert. | **Hard Rule 4, dem Geiste nach** — exakt die Begründung, die `serializers.py` Z. 80–86 für `overview_row_to_json()` bereits schriftlich trägt: der globale Modus ist die zweite Fläche, die Inhalte mehrerer Spaces nebeneinander zeigt, ohne dass man vorher bewusst in einen fremden Space gewechselt ist. Die Liste rendert `snippet` heute ohnehin nirgends (`list.js :: itemMetaLine()` nutzt nur `type`/`status`/`due`/`tags`) — die Änderung kostet keine Anzeige, schließt aber die API-Fläche. |
| **P6-AT** | **Der Space jeder Trefferzeile wird im globalen Modus angezeigt**, als zusätzliches Präfix in `itemMetaLine()`. Kein neues Feld nötig — `summary_to_json()` trägt `space` bereits (`serializers.py` Z. 59). | Ohne Space-Angabe ist eine Trefferliste über mehrere Spaces nicht interpretierbar. Space-Namen sind ACL-Metadaten, kein Fließtext — dieselbe Einstufung wie beim Sichtbarkeits-Chip (Step 7 Commit 2, zweiter Punkt), Hard Rule 4s `<untrusted_content>`-Wrapping betrifft sie nicht. |

### §1.1 Offene Frage an den Nikinger — **nicht von Claude zu entscheiden**

**Q1 — Was heißt „finden" für dich?**
`store.search()` matcht ausschließlich **Titel und Tags**
(`store.py` Z. 417: `haystack = f"{item.title} {' '.join(item.tags)}".lower()`), **niemals den
Body**. Ein globaler Modus findet ein item-level geteiltes Dokument also nur, wenn der Suchbegriff
im **Titel** oder in einem **Tag** steht.

Wenn dein mentales Modell des Blockers „ich tippe ein Wort, das *im Dokument* steht, und finde es"
ist, dann löst dieser Plan den Blocker **nicht vollständig** — dann braucht es zusätzlich eine
Body-Suche, und das ist ein eigener, größerer Schnitt (SQLite FTS5 oder ein Body-Scan;
`docs/concepts/phase2_mcp_plan.md` hat SQL-Filterung als **D6** ausdrücklich zurückgestellt).
Dieselbe Wurzel wie der Vormerkungs-Punkt „Suchtreffer gelegentlich unzuverlässig" aus dem
Werkzeug-Ergonomie-Feedback vom 2026-08-14.

**Bis Q1 beantwortet ist:** Steps 1–3 unten sind trotzdem vollständig ausführbar und richtig — sie
sind Voraussetzung für *jede* Antwort auf Q1. Eine etwaige Body-Suche käme additiv obendrauf, nicht
statt dessen.

**[2026-08-19, Nikinger-Entscheidung]:** Nur Titel/Tags — Steps G1–G3 wie geplant bauen, **keine**
Body-Suche in diesem Schnitt. Ausdrücklich als offene Lücke vermerkt, nicht stillschweigend
geschlossen: Textinhalt eines Dokuments bleibt über den globalen Modus unauffindbar, solange der
Suchbegriff nicht im Titel oder in einem Tag steht. Teilt die Wurzel mit dem Werkzeug-Ergonomie-
Punkt „Suchtreffer gelegentlich unzuverlässig" (2026-08-14) und mit D6
(`docs/concepts/phase2_mcp_plan.md`) — Kandidat für einen eigenen, größeren Schnitt später, kein
Scope hier.

---

## §2 Berührungsfläche

**Erlaubt (und nur das):**

- `phase5_ui/webui/serializers.py` — `summary_to_json()` bekommt einen Keyword-Parameter.
- `phase5_ui/webui/api.py` — `_items_get()` reicht ihn durch.
- `phase5_ui/webui/static/js/{state,list,tree}.js`, `static/app.html`, `static/app.css`.
- **[2026-08-19 Nachtrag, Advisor-Fund vor dem Commit]** `phase5_ui/webui/static/js/editor.js`
  — nicht ursprünglich geplant, aber eine direkte Konsequenz dieses Schnitts: `clearDetail()`
  ist ein zweiter, von `tree.js :: activateView()` unabhängiger Pfad, der `state.scope`
  ebenfalls zurücksetzen muss (Details: §3 Step G3-Nachtrag).

**Tabu, `git diff` am Ende leer:** `phase1_storage/storage/**`, `phase2_mcp/mcpserver/tools.py`,
`phase2_mcp/mcpserver/permissions.py`, `phase2_mcp/mcpserver/server.py`, `phase4_auth/**`.
(P5-B unverändert; P6-C erlaubt zwar `storage/` und `tools.py`, dieser Plan braucht beides nicht —
und ein Diff dort wäre ein Signal, dass etwas falsch verstanden wurde.)

---

## §3 Schritt-Sequenz

### Step G1 — Server: `snippet`-Riegel (P6-AS)

**Datei:** `phase5_ui/webui/serializers.py`

- `summary_to_json(s, *, own_space, readonly)` → `summary_to_json(s, *, own_space, readonly,
  include_snippet: bool = True)`. Bei `include_snippet=False` wird der Schlüssel `"snippet"`
  **nicht gesetzt** (nicht auf `None`) — dasselbe Ergebnis wie `overview_row_to_json()`s
  `row.pop("snippet")` (Z. 94), damit beide Flächen dieselbe Form liefern.
- Default `True` ⇒ alle bestehenden Aufrufer (`_items_get` im Space-Modus, `overview_row_to_json`)
  bleiben byte-identisch.

**Datei:** `phase5_ui/webui/api.py :: _items_get()` (~Z. 326–366)

- Direkt nach dem Lesen der Query-Parameter: `global_scope = q.get("space") is None`.
- In der `item_dicts`-Comprehension (Z. 358–364):
  `include_snippet=not (global_scope and i.space != session.space)`.

**Bewusst NICHT geändert:** die `store.search(...)`-Argumente. `space=q.get("space")` ist bei
fehlendem Parameter bereits `None` und damit bereits global — hier ist **nichts** zu tun. Wer hier
Code hinzufügt, hat den Befund missverstanden.

### Step G2 — Frontend: `state.scope` + globaler Ladeweg (P6-AP/AQ/AR)

**Datei:** `phase5_ui/webui/static/js/state.js`

- Neues Feld in `state`: `scope: "space"` (Default). Kommentar analog zu `folder`: exklusiv zu
  `filter`/`folder` — im Modus `"all"` sind beide `null`.
- `activeSpaceWritable()`: erste Zeile `if (state.scope === "all") return false;` **vor** der
  bestehenden `activeSpace === null`-Prüfung. Damit hängt `setCreateControlsPresent()` (Z. 88–91)
  ohne weitere Änderung alle Anlege-Bedienelemente aus (P6-AR), und `list.js` Z. 174/204/222/227
  ziehen automatisch nach.
- Neue exportierte Hilfsfunktion `isGlobalScope()` → `state.scope === "all"` (eine Stelle, an der
  der Vergleich steht — `list.js` und `tree.js` brauchen ihn beide).

**Datei:** `phase5_ui/webui/static/js/tree.js`

- Neue exportierte `navigateAll()`:
  ```
  state.scope = "all"; state.filter = null; state.folder = null;
  ```
  danach denselben Rumpf wie `activateView()` (`setCreateControlsPresent(activeSpaceWritable())`,
  `renderRail()`, `renderCrumb()`, `loadItems()`) — **`state.activeSpace` bleibt unangetastet**
  (P6-AP).
- `activateView()` (Z. 19–25) bekommt als erste Zeile `state.scope = "space";` — jeder Klick auf
  einen Space/Eimer/Ordner führt so garantiert aus dem globalen Modus zurück, ohne dass jede
  Aufrufstelle daran denken muss.
- `renderRail()` (Z. 199–213): **oberhalb** von „Mein Space" eine eigene Zeile
  `.tree__scope` — Beschriftung **„Alle Items"**, `aria-current="true"` genau dann, wenn
  `isGlobalScope()`. Klick geht wie jeder andere Baumknoten durch
  `closeEditor().then(proceed => proceed === false ? undefined : navigateAll())`
  (dieselbe Editor-Schutzlogik wie `renderFolders()` Z. 53–63 — sonst bleibt ein ungespeicherter
  Editor stehen, der bereits gemeldete Nikinger-Fund).
- Kein Zähler an dieser Zeile: `state.spaces` trägt keine Zahl für „alle lesbaren Items", und eine
  aus den sichtbaren Spaces aufaddierte Zahl wäre **falsch** (sie ließe genau die item-level
  geteilten Items weg, um die es hier geht). Lieber keine Zahl als eine unwahre.

**Datei:** `phase5_ui/webui/static/js/list.js`

- `filterParams()` (Z. 294–303): als **erste** Zeile `if (isGlobalScope()) return {};` — vor der
  `state.folder`-Prüfung. **Das ist P6-AQ, die kritischste Zeile dieses Plans.**
- `loadItems()` (Z. 316–324): `if (state.activeSpace && !isGlobalScope()) params.set("space", …)`.
- `renderCrumb()` (Z. 168–175): im globalen Modus `<strong>Alle Items</strong>` ohne
  `› <Ordner>`-Suffix; `listReadonlyEl.hidden` bleibt über `activeSpaceWritable()` gesteuert —
  **Prüfen und ggf. anpassen:** das Banner „nur lesen" wäre im globalen Modus sichtbar. Gewünscht
  ist stattdessen ein neutraler Hinweis oder gar keiner; Umsetzung: `listReadonlyEl.hidden =
  isGlobalScope() || activeSpaceWritable()`.
- `itemMetaLine()` (Z. 114–119): `if (isGlobalScope()) parts.unshift(item.space);` (P6-AT).
  **Geprüft (2026-08-19):** `itemMetaLine()` hat genau **einen** Aufrufer (`list.js` Z. 236, der
  Zeilen-Render). Die Übersichtsseite („Zuletzt benutzt“) baut ihre Zeilen selbst — kein
  redundantes Space-Präfix dort, kein Zusatzaufwand.
- `renderList()`s Leerzustand (Z. 200–210): eigener Zweig für den globalen Modus —
  `"Keine Treffer für „…"."` bei gesetzter Suche, sonst `"Keine lesbaren Items."`. Die bestehenden
  Zweige lesen `BUCKET_LABELS[state.filter]`, das ist im globalen Modus `null`.
- **Null-Sicherheit prüfen (Advisor-Fund-Kategorie „`state.filter=null`", Step 7 Commit 1):** eine
  Trefferzeile kann jetzt einen `item.space` tragen, den `state.spaces` **nicht** enthält —
  `spaceByName(item.space)` liefert dort `null`. Der heutige Render-Pfad dereferenziert das nicht
  (`renderList()` benutzt ausschließlich `activeSpaceWritable()`, `spaceByName` steht nur in
  `list.js` Z. 27 / `dialogs.js` Z. 169/207, alle drei außerhalb des Zeilen-Renderings) —
  **beim Bauen erneut gegenprüfen, nicht auf diese Zeile verlassen**, und einen echten Browserlauf
  mit Konsolenfehler-Listener fahren.

**Datei:** `phase5_ui/webui/static/app.css` — `.tree__scope` erbt von `.tree__space`;
optische Absetzung nach unten (Trennlinie), kein neues Farbtoken.

### Step G3 — Verifikation gegen eine Wegwerf-Instanz (kein Repo-Artefakt) [2026-08-19: gefahren]

**Nachtrag:** entgegen einer ersten, zu optimistischen Zwischennotiz dieser Session **wurde
dieser Schritt tatsächlich gefahren**, nach einem Advisor-Einwand vor dem Commit — der
Unit-Test in §4 deckt nur den Server ab, nie `filterParams()` selbst (P5-T, JS bleibt
unit-ungetestet, kein Ersatz möglich). Ergebnis: 10/10 Playwright-Prüfungen grün, inklusive
des Pflichtfalls unten UND einer zusätzlich gefundenen und noch vor dem Commit behobenen
Regression (`editor.js :: clearDetail()` setzte `state.scope` nicht zurück — Details:
`phase6_shares/CLAUDE.md`s aktuellem Session-Block). Schließt V57 und V58.

Der Lauf vom 2026-08-18 ist **wiederverwendbar** (`~/.claude-code-tools/e2e-venv`, Playwright +
httpx; Standing Permission, `docs/PROMPTS.md`, Abschnitt „Tests"). Aufbau exakt wie dort:
eigener Port, eigenes `tmp`-`DATA_ROOT`, selbst erzeugter DEK, `SPACE_PUBLIC_BASE_URL` passend zum
Browser-Origin (`http://127.0.0.1:<port>`), `totp_now()` mit Fensterwechsel.

**Der Pflichtfall ist wörtlich das Szenario aus Abnahmezeile 28:** `alpha` legt eine **Notiz**
(nicht `task`!) an und setzt `share_write: [beta]` — **kein** space-level Grant. `beta` loggt sich
in der Web-UI ein, klickt „Alle Items", findet die Notiz, öffnet sie, speichert sie.

> Der Notiz-statt-Aufgabe-Teil ist kein Detail: mit einer `task`/`open` hätte ein Bau, der P6-AQ
> vergisst, **trotzdem** grün ausgesehen.

---

## §4 Testliste (Pflicht, alle in `phase5_ui/tests/`)

Serverseitig (`pytest`):

1. `test_serializers.py :: test_summary_to_json_omits_snippet_key_when_disabled` — Schlüssel
   **fehlt**, ist nicht `None`.
2. `test_serializers.py :: test_summary_to_json_keeps_snippet_by_default` — Regression, bestehende
   Aufrufer unverändert.
3. `test_api.py :: test_items_without_space_param_returns_items_from_all_readable_spaces` — zwei
   Spaces, Item im fremden Space **nur** über item-level `share_read`, kein space-level Grant;
   Treffer erscheint.
4. `test_api.py :: test_items_without_space_param_still_hides_unreadable_items` — Fail-closed-
   Gegenprobe: ein Item ohne jeden Grant erscheint **nicht**.
5. `test_api.py :: test_global_items_omit_snippet_for_foreign_rows_but_keep_own` — eine eigene und
   eine fremde Zeile in derselben Antwort, genau eine trägt `snippet`.
6. `test_api.py :: test_items_with_space_param_keeps_snippet_for_foreign_space` — der bewusste
   Space-Wechsel bleibt unverändert (P6-AS' zweite Hälfte).
7. `test_api.py :: test_get_single_item_shared_item_level_only_is_readable` — belegt, dass ein
   Treffer aus dem globalen Modus auch **öffenbar** ist (heutiges Verhalten, hier gegen künftige
   Regression gepinnt).

Frontend: **keine Unit-Tests** (P5-T unverändert) — die Verifikation ist Step G3s echter
Browserlauf, mit Konsolenfehler-Listener und Assertions auf die tatsächlich gerenderten
Zeilentitel (nicht nur ein Screenshot), wie in Step 7 Commit 1 etabliert.

**Regressionsschwelle:** `pytest` gesamt 765 → **772**. Charakterisierung
(`phase6_shares/tests/test_characterization.py`) muss byte-identisch grün bleiben (P6-D) — sie
sollte von diesem Plan gar nicht berührt werden, ein Ausschlag dort ist ein Befund.

---

## §5 Abnahmekriterien (Zeilen 35–39, Fortsetzung von `ITEM_MOVE_PLAN.md`s 25–34)

> **Statusregel unverändert: ✅ heißt live-verifiziert durch den Nikinger, nicht gebaut.**

| # | Kriterium | Wie geprüft |
|---|---|---|
| 35 | „Alle Items" ist im Baum sichtbar und aktivierbar, ohne einen Space zu verlassen; ein Klick auf einen Space führt zurück | Nikinger, Browser |
| 36 | Ein Item, das ausschließlich item-level freigegeben ist (kein space-level Grant), erscheint für den Freigegebenen unter „Alle Items" und lässt sich öffnen | Nikinger + Fabian, echter Live-Space |
| 37 | Dasselbe Item ist bei `share_write` im geöffneten Editor speicherbar; bei nur `share_read` ist der geöffnete Editor schreibgeschützt (`readonly:true`, Nur-lesen-Ansicht statt Editor). **Gemeint ist die Detailansicht, nicht die Liste** — in der Liste sind unter „Alle Items“ ohnehin alle Anlege-Bedienelemente ausgehängt (P6-AR), das bewiese nichts | Nikinger, Browser + DevTools |
| 38 | „Alle Items" zeigt Notizen **und** Aufgaben gemeinsam (P6-AQ empirisch, nicht nur aus dem Code) | Nikinger, Browser |
| 39 | Unter „Alle Items" existiert kein Anlegen-Knopf und kein Anlege-Dialog **im DOM** (P6-AR, Fortführung von P5-Abnahmezeile 12) | Nikinger, DevTools |

---

## §6 Was dieser Plan ausdrücklich NICHT tut

- **Kein** Body-Volltextsuche (siehe Q1 — offene Nikinger-Frage, kein Claude-Entscheid).
- **Kein** Sichtbarmachen fremder Spaces im Baum ohne space-level Grant. Das ist korrektes,
  gewolltes Verhalten (`visible_spaces()`), nicht der Bug.
- **Kein** Verschieben-/Freigeben-Knopf für fremde Items — das ist Fund 1 vom 2026-08-18, vom
  Nikinger ausdrücklich als **kein Bug** eingestuft, reine Vormerkung.
- **Keine** der fünf offenen Werkzeug-Ergonomie-Vormerkungen (P6-C-Scope, andere Session). Berührt
  wird nur die gemeinsame **Wurzel** von „Suchtreffer unzuverlässig" — als Befund unter Q1
  benannt, nicht behoben.
- **Keine** Änderung an `mcpserver/tools.py :: search_items` — die Agentenfläche filtert bereits
  item-weise über alle Spaces (`tools.py` Z. 291–297) und hat den Fund nie gehabt.

---

## §7 Reihenfolge gegenüber dem übrigen P6-Restbestand

1. **Dieser Plan** (Deploy-Blocker) — muss **vor** dem nächsten `deploy.sh`-Lauf gebaut sein.
2. **Step 7b Deploy** (Item-Move) — bereits gebaut, wartet nur auf die Nikinger-Live-Probe
   (Abnahmezeilen 25–30). Kann **im selben** Deploy mitgehen; keine technische Abhängigkeit in
   beide Richtungen (Step 7b fasst `filterParams()`/`loadItems()` nicht an).
3. **§9 Mehrfachauswahl** (`ITEM_MOVE_PLAN.md` §9, P6-AK–AN) — setzt Step 7b voraus, nicht diesen
   Plan.
4. **Block C — Bilder** (`phase6_shares/IMAGES_PLAN.md`) — unabhängig, aber deutlich größer und
   mit offenen Nikinger-Entscheidungen; kommt nach diesem Plan.

---

## §8 `[VERIFY]`-Register

| # | Zu prüfen | Warum unsicher |
|---|---|---|
| **V56** | Alle Zeilennummern in diesem Dokument | Stand 2026-08-19, `main`@`2b155ce`. Die *Funktionsnamen* sind die belastbaren Anker, nicht die Zahlen. |
| **V57** | ~~`listReadonlyEl`-Verhalten im globalen Modus (§3, Step G2, `renderCrumb()`)~~ **[2026-08-19 geschlossen]** — Playwright-Lauf gegen die Wegwerf-Instanz zeigte keinen fälschlich sichtbaren „nur lesen"-Hinweis, keine Konsolenfehler. |
| **V58** | ~~Kein Render-Pfad dereferenziert `spaceByName(item.space)` für eine Zeile aus einem nicht gelisteten Space~~ **[2026-08-19 geschlossen]** — derselbe Lauf, null Konsolenfehler über den gesamten Durchgang (Login → Alle Items → Item aus unlistetem Space öffnen/speichern → Home). |
