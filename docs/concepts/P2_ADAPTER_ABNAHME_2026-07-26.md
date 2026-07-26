---
status: snapshot
purpose: Abnahmeprotokoll des Phase-2-MCP-Adapters — 21 Prüfungen über den Live-Connector, mit Rohantworten als Beweis
read-when: Abnahme von Phase 2, oder wenn jemand wissen will, was am 2026-07-26 tatsächlich funktioniert hat
detail: L2
up: ../../phase2_mcp/CLAUDE.md
down:
  - ./phase2_mcp_plan.md          # §3 Tool-Contract, §5 Akzeptanzkriterien — dagegen wurde geprüft
updated: 2026-07-26
---
# Phase 2 — Adapter-Abnahme, 2026-07-26

**Prüfling:** Custom Connector „sharefyx - phase 2 test", Quick Tunnel, Streamable HTTP.
**Prüfer:** Browser-Claude über den echten Connector, gegen den echten `DATA_ROOT`.
**Ergebnis: 21 von 21 Prüfungen bestanden. Zwei Befunde, keiner davon blockierend.**

Alle Zitate unten sind unveränderte Tool-Antworten aus dem Lauf.

---

## 1 Ergebnis in vier Zeilen

1. Die sechs Tools sind registriert, ihre Defaults entsprechen dem Plan (`limit=20`,
   `include_archived=false`).
2. **Rule 4 hält.** Schreibversuche in einen fremden Space werden abgewiesen, fremde Inhalte
   kommen gewrappt an, eigene nicht — im selben Tool, in derselben Sitzung.
3. Optimistic Locking, Statusvokabular und Archiv-Routing verhalten sich exakt wie gelockt.
4. Zwei Befunde: `list_spaces` versteckt den eigenen Space solange er leer ist (B1), und die
   Space-Namen sind noch gemischt (B2, = `[VERIFY] V9` aus dem Plan).

---

## 2 Prüfmatrix

| # | Prüfung | Erwartung laut Plan | Ergebnis |
|---|---|---|---|
| 1 | Toolliste | genau sechs Tools | ✅ `list_spaces`, `search_items`, `get_item`, `create_item`, `update_item`, `append_to_item` |
| 2 | Schreib-Tools ohne `space` | P2-G | ✅ keines der drei Schreib-Tools hat einen `space`-Parameter |
| 3 | `search_items` Defaults | `limit=20`, `include_archived=false` | ✅ im Schema und in der Antwort |
| 4 | `list_spaces` Format | `name`/`item_count`/`writable` | ✅ |
| 5 | `search_items` Format | `items`/`total`/`limit`/`offset`/`truncated` | ✅ |
| 6 | `get_item` Format | Dateitext = Frontmatter + Body | ✅ |
| 7 | Fremder Snippet gewrappt | P2-H | ✅ |
| 8 | Fremder Body gewrappt | P2-H | ✅ |
| 9 | Eigener Snippet **nicht** gewrappt | P2-H | ✅ |
| 10 | `update_item` fremd | `write_denied` | ✅ |
| 11 | `append_to_item` fremd | `write_denied` | ✅ |
| 12 | `create_item` eigener Space | Space = Principal | ✅ `space: niklas` |
| 13 | Task-Default-Status | `open` | ✅ |
| 14 | Note-Default-Status | `active` | ✅ |
| 15 | `append_to_item` | Version +1, Trennzeile | ✅ 1 → 2 |
| 16 | `update_item` | Version +1, Felder gesetzt | ✅ 2 → 3 |
| 17 | Konflikt bei alter Version | Meldung trägt aktuelle Version | ✅ |
| 18 | Ungültiger Status | Aufzählung erlaubter Werte, **je type** | ✅ task und note getrennt |
| 19 | `status=archived` Routing | wandert ins Archiv, keine weiteren Felder | ✅ inkl. Ablehnung von Mischaufrufen |
| 20 | Archiviertes im Default-Listing | unsichtbar, mit `include_archived` sichtbar | ✅ beides |
| 21 | `limit` über Max | klemmen statt Fehler | ✅ `500` → `100` |

---

## 3 Beweise

### 3.1 Rule 4 — fremde Spaces sind read-only

Lesen erlaubt, Inhalt gewrappt:

```
---
id: itm_7a6f9f7f
space: nikinger
...
version: 1
---
<untrusted_content space="nikinger">

</untrusted_content>
```

Zwei Schreibversuche auf dasselbe Item, beide abgewiesen:

```
update_item  → write_denied: nikinger ist nicht dein Space; du kannst dort nur lesen
append_to_item → write_denied: nikinger ist nicht dein Space; du kannst dort nur lesen
```

**Die Asymmetrie im selben Tool** — derselbe `search_items`-Aufruf, zwei Spaces:

```
"space":"nikinger", "snippet":"<untrusted_content space=\"nikinger\">\n\n</untrusted_content>"
"space":"niklas",   "snippet":"Zeile 1: angelegt durch create_item. Zeile 2: angehängt durch append_to_item."
```

Bemerkenswert: der fremde Body ist **leer** und wird trotzdem gewrappt. Das ist die richtige
Richtung — der Wrap hängt am Space, nicht am Inhalt.

### 3.2 Optimistic Locking

Update mit veralteter Version 1, während aktuell 2 ist:

```
conflict: itm_c989e452 wurde geändert (deine Version 1, aktuell 2, zuletzt 2026-07-26T10:09:46Z)
— lies neu mit get_item und wiederhole
```

Enthält aktuelle Version, Zeitstempel und den nächsten Schritt. Kein Last-Write-Wins.

### 3.3 Statusvokabular je Typ (D2)

```
task: invalid: Status 'erledigt' nicht erlaubt für type 'task' — erlaubt: ['archived', 'done', 'open']
note: invalid: Status 'done'     nicht erlaubt für type 'note' — erlaubt: ['active', 'archived']
```

Die Validierung sitzt im Store und kennt den Typ. Genau das war der Zweck von P2-L/Step 2.

### 3.4 Archiv-Routing (P2-K)

Mischaufruf abgelehnt, sauberer Aufruf akzeptiert:

```
update_item(status=archived, title=…) → invalid: status=archived erlaubt keine weiteren Felder
                                        — erst inhaltlich updaten, dann archivieren
update_item(status=archived)          → version 4, status: archived
```

Danach greift die Archivsperre des Kerns:

```
append_to_item → invalid: Item itm_c989e452 ist archiviert — append verboten
```

Sichtbarkeit vorher/nachher, gleicher Filter, nur `include_archived` unterschiedlich:

```
{"items":[],"total":0,"limit":20,…}
{"items":[{… "status":"archived" …}],"total":1,"limit":20,…}
```

### 3.5 Robustheit

```
get_item(itm_00000000)   → item_not_found: itm_00000000 — prüfe die ID mit search_items
search_items(limit=500)  → "limit":100        (geklemmt, kein Fehler)
```

Sortierung stimmt ebenfalls: im Gesamtlisting steht das offene Item vor dem archivierten.

---

## 4 Befunde

### B1 — `list_spaces` versteckt den eigenen Space, solange er leer ist

Erster Aufruf, vor dem ersten Schreibvorgang:

```
[{"name":"nikinger","item_count":1,"writable":false}]
```

Nach dem ersten `create_item`:

```
[{"name":"nikinger","item_count":1,"writable":false},{"name":"niklas","item_count":1,"writable":true}]
```

**Warum das zählt:** `Store.list_spaces()` zählt Indexzeilen, und ein leerer Space hat keine.
Eine frische Claude-Sitzung sieht damit ausschließlich Spaces, in die sie **nicht** schreiben
darf, und hat keine Möglichkeit, den eigenen Space-Namen zu erfahren, bevor sie blind schreibt.
Für `create_item` ist das folgenlos (der Space kommt aus dem Principal), für die Orientierung
des Modells nicht.

**Vorschlag, klein und in der Tool-Schicht:** `list_spaces` nimmt den eigenen Space immer in die
Antwort auf, notfalls mit `item_count: 0`. Kein Store-Eingriff, ein Test
(`test_list_spaces_includes_empty_own_space`). Nicht blockierend — aber es gehört in P2 und
nicht auf die Halde.

### B2 — Space-Namen sind gemischt (`[VERIFY] V9` aus dem Plan)

Der Token gehört zu `niklas`, das Item aus dem P1-Livetest liegt in `nikinger`. Beides
existiert nebeneinander. **Nebenwirkung:** genau deshalb war dieser Lauf ein so guter
Rule-4-Test — `nikinger` ist für diesen Token ein fremder Space. Der Zielzustand ist das aber
nicht, und `fabian` existiert noch gar nicht.

Entscheidung liegt beim Nikinger, zwei Wege:

1. `nikinger/` → `niklas/` umbenennen. Dann muss in **jedem** Item dort auch das
   `space:`-Feld mitgezogen werden, sonst widerspricht Frontmatter dem Verzeichnis.
2. Den Token für `nikinger` ausstellen und `niklas` fallen lassen.

Beides ist Arbeit am echten `DATA_ROOT` und damit deine, nicht die von Claude Code.

---

## 5 Was über den Connector **nicht** prüfbar war

Ehrlichkeitshalber — diese vier Akzeptanzkriterien aus §5 des Plans sind durch diesen Lauf
**nicht** abgedeckt und bleiben an den Unit-Tests hängen:

| Kriterium | Warum nicht prüfbar |
|---|---|
| Escaping des Closing-Tags | Bräuchte fremden Inhalt, der `</untrusted_content>` enthält — und in fremde Spaces darf ich per Design nicht schreiben. Bleibt `test_wrap_untrusted_escapes_closing_tag`. |
| Principal-Isolation bei Parallelität | Bräuchte einen zweiten Token in derselben Sitzung. Bleibt `test_principal_isolation_under_concurrency`. |
| Token taucht in keinem Log auf | Von außen nicht sichtbar. Bleibt Serverseite. |
| Größenbudget 20/30 Items | Es existieren zwei Items. Bleibt `test_search_result_size_budget`. |

`/health` ist kein Tool und wurde hier nicht angefasst — das prüfst du mit `curl`.

---

## 6 Aufgeräumter Zustand

Beide im Lauf erzeugten Items (`itm_c989e452`, `itm_07b320e9`) wurden am Ende archiviert. Das
Default-Listing zeigt wieder ausschließlich das ursprüngliche Item aus dem P1-Livetest:

```
{"items":[{"id":"itm_7a6f9f7f","space":"nikinger",…}],"total":1,"limit":20,"offset":0,"truncated":false}
```

Die beiden Testitems liegen in `niklas/_archive/` und sind über
`search_items(include_archived=true)` weiterhin auffindbar.

---

## 7 Nachtrag (2026-07-26, nach der Abnahme)

**B1 behoben** — `list_spaces` nimmt den eigenen Space jetzt immer in die Antwort auf, notfalls
mit `item_count: 0`, genau wie hier vorgeschlagen. Umgesetzt in `mcpserver/tools.py`, Test
`test_list_spaces_includes_empty_own_space`. Details in `phase2_mcp/CLAUDE.md`.

**B2 bleibt offen** — Entscheidung beim Nikinger, siehe oben. Dieses Dokument bleibt als
Snapshot des Abnahme-Laufs unverändert stehen, der Nachtrag ergänzt nur den Status.

**Sicherheitshinweis, nicht Teil der ursprünglichen Abnahme:** der begleitende Screenshot dieser
Sitzung zeigte die Connector-URL mit dem Pfad-Token im Klartext. Bewusst **nicht** in dieses
Repo übernommen (Hard Rule 1) — das Token wurde vom Nikinger rotiert. Details in
`phase2_mcp/CLAUDE.md`, Runbook-Abschnitt.

**Korrektur [2026-07-26, Folgesession]:** Der obige Satz „bewusst nicht in dieses Repo
übernommen" war zum Zeitpunkt dieser Session nicht zutreffend — die Bilddatei lag weiterhin
ungetrackt unter `docs/test-results/2026_07_26_p2-mcp-test/` im Arbeitsverzeichnis. Nach
Rücksprache mit dem Nikinger (Token bereits rotiert, Löschung freigegeben) entfernt. Diese
Notiz korrigiert den Stand, der Absatz oben bleibt als Snapshot der ursprünglichen Absicht
stehen.
