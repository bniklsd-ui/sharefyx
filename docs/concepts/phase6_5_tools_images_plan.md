---
status: snapshot
purpose: Ausführungsreifer Plan der neuen QoS-Phase — MCP-Werkzeug-Ergonomie (5 offene Punkte) + Abschluss Block C (Bilder)
read-when: Kickoff dieser Phase, oder wenn geklärt werden muss, warum ein Tool so beschrieben ist bzw. wie ein Bild physisch liegt und wer es sehen darf
detail: L2
up: ../../ROADMAP.md
down: ../../phase6_shares/IMAGES_PLAN.md (Vorgänger-Zusatzplan, ab jetzt nachrangig) · ../../phase6_shares/CLAUDE.md · ./phase6_shares_plan.md
updated: 2026-08-20 (Opus-Planungssession, danach N1–N6 vom Nikinger live per AskUserQuestion beantwortet und in §0.0 gelockt — Phase 6.5, kein app.html-Fix nötig, kein Bulk-Append, Body-Suche als MCP-Opt-in, Bild-Trash statt Entfernen mit offener Vormerkung zur Langzeit-Aufräumung, MAX_MCP_ASSET_BYTES=1MiB; gelockt P6.5-A–P6.5-V, B1–B4 als Nikinger-Vorgabe eingearbeitet, V59/V61 empirisch geschlossen)
---

# Phase 6.5 — Werkzeug-Ergonomie und Bilder

> **Mission, zwei Blöcke:** (A) Eine arbeitende Claude-Instanz findet ihre Werkzeuge, versteht
> deren Aufgabenteilung aus der Beschreibung und zahlt keine Tausende Token für eine
> Versionsnummer. (B) Ein Bild liegt im Space, ist im Dokument sichtbar, technisch nur ein Link —
> und Claude sieht seine Bytes nur, wenn ein Mensch ausdrücklich danach fragt.
>
> **Unter Druck fällt Block B weg, nie Block A.** Block A ist reine Beschreibungs-/Tool-Arbeit
> ohne Datenformatänderung; Block B fasst zum ersten Mal Binärdaten an.
>
> **Quelle der Wahrheit ist der Code, nicht dieses Dokument.** Alle Zeilennummern sind Stand
> `main`@`2a4d8ca`, 2026-08-20 (`[VERIFY]` V70). Funktionsnamen sind die belastbaren Anker.

---

## §0 Offene Fragen an den Nikinger (N1–N6) — vor bzw. beim Kickoff zu klären

> Diese Planungssession hatte **kein** interaktives Frage-Werkzeug (`AskUserQuestion` war nicht
> verfügbar). Wie schon in `IMAGES_PLAN.md` §0 sind die Punkte **bewusst nicht** still aufgelöst
> worden. **Der gesamte Plan ist unter jeder Antwort baubar**; wo eine Antwort den Text ändert,
> steht es ausdrücklich dabei.

| # | Frage | Warum Nikinger, nicht Claude | Claudes Empfehlung (**nicht** gelockt) |
|---|---|---|---|
| **N1** | ~~Phasennummer: 7 oder 8?~~ **[2026-08-20 entschieden]** Nikinger-Entscheidung: diese Phase wird **6.5**, nicht 7 — sie gehört inhaltlich noch vor die Space-Admin-UI, die `phase5_ui/webui/static/app.html` Z. 281 als hart `disabled` Menüpunkt *„Geteilte Spaces verwalten — kommt in Phase 7"* ankündigt (committet, noch nicht deployt). Damit gibt es **keine Namenskollision mehr**: 6.5 sitzt zwischen 6 und 7, `app.html`s Text bleibt korrekt und wird **nicht** angefasst. | — (entschieden) | **Gelockt: Phase 6.5.** `app.html` Z. 281 bleibt unverändert (verweist weiterhin zu Recht auf die künftige Phase 7 = Space-Admin-UI). Kein Step-0-Textfix nötig. |
| **N2** | Verzeichnisname der Phase. | — (entschieden) | **Gelockt: `phase6_5_tools_images/`** (kein eigenes Python-Paket, wie `phase6_shares/` — trägt nur `tests/`, ggf. `scripts/`, `CLAUDE.md`). |
| **N3** | **Bulk-Append: wirklich bauen?** Befund dieser Planung, siehe §3 Step A3: *„mehrere Appends in einem Aufruf"* ist **heute schon möglich** — `append_to_item(text=…)` nimmt beliebig langen Text mit Zeilenumbrüchen; ein zweiter Parameter wäre `"\n".join(texts)` und damit reine Zeremonie. Die 40+ Aufrufe entstanden über einen **Tag verteilt**, weil die Ereignisse verteilt eintraten — kein Batch war überhaupt bildbar. Zusätzlich: `write_receipt()` liefert bei **jedem** Write die neue `version` mit, ein Re-Read zwischen Appends war nie nötig. | Es ist eine Wunsch-Bestätigung: Claude schlägt vor, einen gemeldeten Wunsch **nicht** zu bauen. Das gehört gemeldet, nicht still entschieden. | **Nicht bauen.** Stattdessen: ein Satz in `append_to_item`s Beschreibung („mehrere Einträge in einem Aufruf: Text mit Zeilenumbrüchen übergeben — ein Aufruf, ein Commit") plus der explizite Hinweis, dass die Quittung die nächste `version` bereits enthält. Kostet null Code, deckt den gemeldeten Schmerz. |
| **N4** | **Body-Volltextsuche für die MCP-Fläche — jetzt doch?** Befund dieser Planung: `Store.search()` lädt über `_row_to_item()` **jede** indizierte Datei ohnehin vollständig in den Speicher (genau D6s Kostenpunkt); der Body **liegt bereits da**, `matches()` schaut nur nicht hinein (`store.py` Z. 415: `haystack = f"{item.title} {' '.join(item.tags)}"`). Eine Body-Suche kostet an dieser Stelle **nichts zusätzlich**. Q1 (2026-08-19) hat Body-Suche für die **UI** bewusst ausgeschlossen — auf einer Kostenannahme, die hier nachweislich nicht trägt. | **Eine gelockte Nikinger-Entscheidung darf Claude nicht still umdrehen** (Working Style). Der Kostenbefund ist neue Evidenz, kein Freibrief. | **Opt-in, nicht Default:** `search_items(..., in_body: bool = False)`, eine Zeile in `matches()`. Default-Verhalten bleibt byte-identisch, Q1 bleibt für die UI unangetastet. Wenn der Nikinger es lieber ganz draußen hat: Step A4 entfällt ersatzlos, die ehrliche Beschreibung aus Step A1 bleibt (sie allein erklärt schon die „unzuverlässigen Treffer"). |
| **N5** | **B5 — darf ein Bild wieder ENTFERNT werden, und wie?** (Unverändert aus `IMAGES_PLAN.md` §0, als einzige der fünf noch offen.) `phase1_storage/CLAUDE.md` lockt Entscheidung **H**: *„Kein Delete im Kern-API. `status: archived` + `_archive/`. Hard Delete nur als separates, bestätigungspflichtiges Operator-Skript."* Ein `store.delete_asset()` wäre die **erste** Löschoperation im Kern-API. Wegen **B1 = ja** (Blobs sind in der Git-Historie) gibt ein Entfernen die Bytes ohnehin **nicht** frei — es ist eine Aufräum-/Anzeigefrage, keine Platzfrage. | Regelaufweichung an einer gelockten P1-Entscheidung. | **„Verschieben statt Entfernen":** `_assets/<item_id>/_trash/<asset_id>.<ext>`, dieselbe Bauart wie `_archive/`. Entscheidung H bleibt formal unangetastet, die Body-Referenz läuft ins Leere und rendert als Alt-Text, echtes Hard Delete bleibt Operator-Skript. Alternative: **„kein Entfernen in v1"** — dann entfallen `store.delete_asset()`, `DELETE /api/v1/items/{id}/assets/{id}`, der Entfernen-Knopf in `editor.js` und Abnahmezeile P6.5-12 **ersatzlos**; alles Übrige bleibt gleich. |
| **N6** | **Bild-Upload über MCP (B4 = ja): welche Größe/Kodierung?** Ein Bild muss durch ein Tool-Argument, also base64 im JSON — bei 5 MiB Rohgröße sind das ~6,8 MB Text in **einem** Tool-Call. Das ist keine Rechtsfrage, sondern eine Praktikabilitätsfrage. | Nutzungsfrage: was soll Claude tatsächlich hochladen (kleine generierte Diagramme? weitergereichte Screenshots?). | **Eigener, kleinerer Riegel für den MCP-Weg:** `MAX_MCP_ASSET_BYTES = 1 MiB` (Rohbytes nach base64-Dekodierung), Web-UI bleibt bei 5 MiB. Begründung im Plan (§3 Step B4). Wenn der Nikinger einen einheitlichen Riegel will: beide auf 5 MiB, eine Konstante weniger. |

### §0.0 Nikinger-Entscheidungen zu N1–N6 (2026-08-20, gelockt)

| # | Gelockte Antwort |
|---|---|
| **N1** | Phase **6.5** (nicht 7/8). Keine Kollision mit `app.html`s „kommt in Phase 7" — bleibt unangetastet. |
| **N2** | `phase6_5_tools_images/`. |
| **N3** | **Nicht bauen.** Nur Beschreibungssatz in `append_to_item` (wie empfohlen). |
| **N4** | **Ja, als Opt-in bauen** (`in_body: bool = False`, Step A4 bleibt drin). Q1 (UI) unangetastet. |
| **N5** | **Verschieben statt Entfernen** (`_assets/<item_id>/_trash/`, wie empfohlen). **Zusätzliche Nikinger-Anmerkung, als offene Vormerkung festzuhalten, kein Auftrag für diese Phase:** `_trash/` wird nie automatisch geräumt — anders als kB-große `.md`-Dateien können MB-große Bilder die Git-Historie/den `DATA_ROOT` über Zeit zu GB-Größen aufwachsen lassen. Braucht mittelfristig eine eigene operative Lösung (z. B. `diagnose.sh`-Meldung ab einer Schwelle, oder ein Operator-Purge-Skript analog zu Hard-Delete). Nicht Scope von Phase 6.5 — als Vormerkung in den neuen Phase-Head aufnehmen. |
| **N6** | **`MAX_MCP_ASSET_BYTES = 1 MiB`** (wie empfohlen). Nikinger-Begründung: Claude wird über MCP ohnehin nur selbst erzeugte SVGs oder kleine Screenshots hochladen, nicht großformatige Fotos. |

### §0.1 Vorgaben aus der Session vom 2026-08-20 (**nicht** mehr zu erfragen)

Vier der fünf `IMAGES_PLAN.md`-Fragen sind beantwortet. Sie sind ab hier **Vorgabe**, kein
Vorschlag:

| # | Antwort | Konsequenz im Plan |
|---|---|---|
| **B1** | **Ja, mit Größenriegel.** Bilder werden mitcommittet, Hard Rule 5 bleibt unverändert scharf. | `put_asset()` erzeugt genau einen Git-Commit. `_assets/` kommt **nicht** in die `.gitignore`. Abnahmezeile P6.5-9 bleibt drin. |
| **B2** | **5 MiB je Bild**, kein Space-Gesamtbudget in v1. | `MAX_ASSET_BYTES = 5 * 1024 * 1024`. Deckt sich mit dem älteren **P6-Y** (5 MiB), nicht mit `IMAGES_PLAN.md` §0s 2-MiB-Empfehlung. **Folge, die im Vorgängerplan falsch steht:** dessen §4 Punkt 5 („bei 2 MiB unkritisch") gilt bei 5 MiB weiterhin, aber knapper — siehe §4 Punkt 5 hier. |
| **B3** | **Differenziert, restriktiver als eine reine ACL-Prüfung.** Bildbytes für Claude: **eigener Space ja**, **fremdes Item nur bei Schreibrecht** (item-level `share_write` oder Shared Space mit `write:`), fremdes Item mit reinem Leserecht: **nur Metadaten**. **Zusätzlich, über den Vorgängerplan hinaus:** Claude lädt Bilder **generell nur auf direkte Anfrage**, nie automatisch — auch nicht bei **eigenen** Items. | Zwei getrennte Hälften, siehe **P6.5-N**: eine **erzwingbare** (Bytes verlassen den Server nur über ein eigenes, ausdrücklich aufgerufenes Tool; nie über `get_item`/`search_items`/eine Quittung) und eine **verhaltensseitige** (Tool-Beschreibung). Der Vorgängerplan formuliert das zu lose („`can_read_item` plus B3-Riegel") — die tatsächliche Bedingung steht in **P6.5-M** ausgeschrieben. |
| **B4** | **Ja, MCP-Upload erlaubt — mit Ankündigungspflicht.** Claude muss dem Nutzer **vor jedem** Upload ankündigen, dass es jetzt ein Bild ablegt. Kein stilles Hochladen, keine Dauererlaubnis. | **`P6-BB`/`P6-AA` sind damit teilweise überholt** — siehe §0.2. Neues Tool `put_item_asset` (§3 Step B4). Die Ankündigungspflicht ist eine **Beschreibungs-/Verhaltensanforderung**, kein Code-Gate; „kann nicht auf ‚immer erlauben' stehen" ist **Client-Verhalten von claude.ai**, das der Server nicht steuert → `[VERIFY]` **V64**, nicht als Zusage formulieren. |

### §0.2 Verhältnis zu `phase6_shares/IMAGES_PLAN.md` (Doku-Hygiene, nicht optional)

`IMAGES_PLAN.md` ist ein **📗-lebendes** Dokument und sagt in seinem heutigen Stand Dinge, die
durch B1–B4 überholt sind (u. a. „FÜNF offene Entscheidungen", „nur Web-UI in v1", „2 MiB",
„B3: Nein in v1"). Zwei lebende Kopien derselben Regel sind genau der Fehler, gegen den
`docs/DOC_LAYERS_CONVENTION.md` geschrieben ist.

**Regelung, in Step 0 auszuführen:**
1. **Dieses Dokument ist ab sofort die maßgebliche Herleitung** für Block C / Bilder; der
   *laufende* Stand (Antworten auf N1–N6, Step-Status, Befunde) lebt im Phase-Head, nicht hier —
   wie in jeder Phase zuvor. **Dieses Dokument wird nach dem Kickoff nicht mehr editiert** (📕).
2. `phase6_shares/IMAGES_PLAN.md` bekommt **oben, direkt unter der Header-Card**, eine datierte
   Zweizeilen-Notiz: *„[2026-08-20] Nachrangig. B1–B4 sind entschieden, Block C wird in
   `docs/concepts/phase6_5_tools_images_plan.md` ausgeführt — dort steht der maßgebliche Stand.
   Dieses Dokument bleibt als Herleitung stehen und wird nicht mehr fortgeschrieben."*
   Der Rest bleibt **unverändert** (Herkunftsnachweis, kein Umschreiben der Historie).
3. Die `docs/INDEX.md`-Zeile von `IMAGES_PLAN.md` wird im selben Commit um diesen Hinweis
   ergänzt; die neue Zeile für dieses Dokument kommt dazu (in dieser Planungssession bereits
   eingetragen).

**Aus `IMAGES_PLAN.md` übernommen und weiterhin gültig:** P6-AU, P6-AV, P6-AW, P6-AX, P6-AY,
P6-AZ, P6-BA. **Überholt:** P6-BB (MCP-Upload jetzt drin, B4), P6-AA („Claude … lädt nicht hoch"
— die Hälfte „löscht nicht" bleibt, siehe P6.5-Q).

---

## §1 Gelockte Entscheidungen dieser Phase (P6.5-A – P6.5-V)

Diese folgen entweder zwingend aus bestehenden Hard Rules / vorhandenen Nahtstellen, aus den
Vorgaben §0.1, oder sind reine Formatfestlegungen ohne Nikinger-Stake.

### Block A — Werkzeug-Ergonomie

| # | Entscheidung | Begründung / Beleg im Code |
|---|---|---|
| **P6.5-A** | **Block A fasst ausschließlich `mcpserver/tools.py`, `mcpserver/receipts.py` und (nur bei N4=ja) `storage/store.py :: search()` an.** Keine Änderung an `permissions.py`, `server.py`, `asgi.py`, `authserver/**`, keiner UI-Datei. | P6-C hat `tools.py` ausdrücklich geöffnet; die Phase erbt das. Je kleiner die Fläche, desto billiger der Regressionsbeweis (`mcp_smoke.py`). |
| **P6.5-B** | **Falsche Aussagen in Tool-Beschreibungen sind Bugs, keine Ergonomie-Wünsche — und Auffindbarkeit wird über Querverweise gelöst, nicht über Hoffnung.** `list_spaces`' Beschreibung (`tools.py` Z. 262–265) sagt heute *„`writable` ist nur für den eigenen Space true"* — **seit P6 Step 5/6 unwahr** (geteilte Spaces mit `write:`-Grant sind ebenfalls `writable:true`). Genau daraus entstand die an den Nikinger weitergegebene Falschaussage „Claude kann nur im eigenen Space schreiben". **Zweite Hälfte desselben Befunds:** die Instanz fand das Tool in ihrer Exploration gar nicht erst — eine Beschreibungskorrektur hilft nur einem Modell, das sie liest. Deshalb verweisen `create_item`/`update_item` ausdrücklich auf `list_spaces` (Step A1). | Dieselbe Kategorie wie die bereits behobene `patch_item`-Fehlermeldung (2026-08-14): eine Beschreibung, die das Modell aktiv in die Irre führt, ist ein Defekt. |
| **P6.5-C** | **Das Statusvokabular wird aus `storage.models.STATUS_VALUES` **generiert**, nicht abgetippt.** Kleine Hilfsfunktion `_status_hint()` in `tools.py`, die aus `valid_statuses("note")`/`valid_statuses("task")` einen Satz baut. | Eine abgetippte Liste driftet beim nächsten Statuswert still auseinander. Die Quelle ist bereits kanonisch (`models.py` Z. 89–99, seit P2 Step 2/D2). Ein Test prüft, dass jeder Wert aus `STATUS_VALUES` in der Beschreibung vorkommt — damit ist Drift ein roter Test, keine Entdeckung im Betrieb. |
| **P6.5-D** | **Die Aufgabenteilung der vier Schreib-Tools steht als **ein** identischer Satzblock in allen vieren** (`create_item`, `update_item`, `append_to_item`, `patch_item`), aus einer Konstante `WRITE_TOOL_DIVISION` zusammengesetzt. | Die Instanz musste sie über zwei Fehlversuche und einen Quellcode-Hinweis lernen. Ein Modell liest die Beschreibung des Tools, das es gerade erwägt — nicht die der anderen drei. Deshalb in jedem, nicht in einem. |
| **P6.5-E** | **Achtes Tool `get_item_meta(item_id)`** — Frontmatter + `version` + `body_bytes`, **kein** Body, **kein** Snippet, kompaktes JSON. | Der gemeldete Tausend-Token-Dump für eine einzige Zahl. Kein Store-Eingriff nötig: `store.get()` liefert das Item ohnehin, das Tool gibt nur weniger davon zurück. |
| **P6.5-F** | **`get_item_meta` wrappt nichts** und braucht es nicht: es gibt keinen Fließtext zurück. `title`/`tags` fremder Items erscheinen wie heute schon in `search_items`/`list_spaces` unverpackt. | Hard Rule 4 wrappt **Bodies/Snippets**. Dieselbe Einstufung wie der Sichtbarkeits-Chip (P6 Step 7 Commit 2) und `summary_to_dict()`s Metadatenfelder. **Kein neuer Präzedenzfall** — wer das ändern will, ändert es an allen drei Stellen gleichzeitig, nicht hier allein. |
| **P6.5-G** | **Kein Bulk-Append-Tool und kein `texts=`-Parameter** (vorbehaltlich **N3**). Stattdessen dokumentiert `append_to_item`, dass mehrzeiliger Text in **einem** Aufruf zulässig ist und die Quittung die nächste `version` bereits trägt. | `write_receipt()` (`receipts.py` Z. 55) liefert `version` bei jedem Write; ein Re-Read zwischen Appends war nie nötig. `"\n".join(texts)` serverseitig ist keine Ersparnis, sondern ein zweiter Codepfad für dasselbe. |
| **P6.5-H** | **Die Suchreichweite wird ehrlich benannt, bevor sie erweitert wird.** `search_items`' Beschreibung nennt ausdrücklich: Teilstring in **Titel und Tags**, Groß/Kleinschreibung egal, **nicht** im Body. | `store.py` Z. 415 ist die Wahrheit. Der Befund „Suchtreffer unzuverlässig" ist zu großen Teilen genau diese unbenannte Einschränkung — ein Modell, das sie kennt, sucht anders (Tag statt Bodyphrase) und rät nicht dreimal. Das gilt **unabhängig** von N4. |

### Block B — Bilder

| # | Entscheidung | Begründung / Beleg im Code |
|---|---|---|
| **P6.5-I** | **P6-AU/AV/AW/AX/AY/AZ/BA gelten unverändert fort** — Ablage `<DATA_ROOT>/<space>/_assets/<item_id>/<asset_id>.<ext>`, Asset-Verzeichnis zieht bei `Store.move()` mit, keine eigene Asset-ACL (erbt über die Route), Referenzschema `![Alt](asset:ast_<8hex>)`, kein Index-Eintrag, atomarer Write + Magic-Byte-Typprüfung ohne SVG, kein serverseitiges Bildverarbeiten. | Alle sieben sind in `IMAGES_PLAN.md` §1 gegen den Code begründet; diese Session hat keinen Widerspruch gefunden. `_assets` steht seit P6 Step 4 in `RESERVED_DIR_NAMES` (`files.py` Z. 17) und wird von `list_spaces()` bereits ausgefiltert. |
| **P6.5-J** | **`markdownToHtml()` bekommt einen Bildzweig, den es heute nicht gibt.** `inlineMarkdown()` (`markdown.js` Z. 25–31) kennt **kein** `!`-Präfix: `![Alt](asset:ast_x)` wird heute zu einem literalen `!` plus `<a href="asset:ast_x">Alt</a>`, dessen `href` `safeHref()` anschließend leert. Der neue `!`-Zweig muss **vor** dem Link-Replace `/\[([^\]]+)\]\(([^)\s]+)\)/` laufen, sonst frisst die Link-Regex ihn. | Fund dieser Session. `IMAGES_PLAN.md` §3 Step C3 spricht vom „`markdownToHtml()`-Bildzweig", als existierte er — er existiert nicht. Ohne diese Korrektur baut Sonnet gegen eine Fiktion. |
| **P6.5-K** | **Der Kopfkommentar von `markdown.js` (Z. 4–9) wird im selben Commit korrigiert.** Er nennt `IMG` und `#asset:` heute ausdrücklich als **bewusst nicht** übernommen („kein Anhang-Feature, P5-AA"). | Ein Kommentar, der die Regel dokumentiert, die man gerade aufhebt, ist ab dem Commit eine Falle für den nächsten Leser. Doku-Hygiene auf Codeebene. |
| **P6.5-L** | **Der Upload-Weg liest rohe Bytes und geht **nicht** durch `_json_body()`.** Eigener Leser mit eigenem Riegel `MAX_ASSET_BYTES = 5 MiB` (**B2**). | `webui/api.py` Z. 105/212: `_json_body()` erzwingt `MAX_BODY_BYTES = 1 MiB` und würde **jedes** reale Bild mit `413` abweisen. Ein zweiter Riegel ist hier kein Duplikat, sondern eine andere Größenordnung für einen anderen Inhaltstyp. |
| **P6.5-M** | **B3s Byte-Bedingung, ausgeschrieben** — Bildbytes gehen an die Agentenfläche genau dann, wenn: `acl.space == principal.space` **ODER** `permissions.can_write_item(principal.space, acl, surface=Surface.AGENT)`. Fremd + nur Leserecht ⇒ **Metadaten + Klartexthinweis, keine Bytes**. Fail-closed. | Die Bedingung ist **nicht** `can_read_item`. Ein fremdes Bild vor einem sehenden Modell ist ein Injektionskanal, den `<untrusted_content>` strukturell nicht erreicht (§4 Punkt 1). Schreibrecht ist der Nikinger-gewählte Vertrauensmarker: wer mir schreiben darf, kann mir ohnehin Text unterschieben. |
| **P6.5-N** | **B3s „nur auf direkte Anfrage" wird in zwei Hälften gebaut: erzwingbar + verhaltensseitig.** **Erzwingbar (pytest):** Bildbytes verlassen den Server über **genau ein** Tool (`get_item_asset`); `get_item`, `get_item_meta`, `search_items` und **jede** Quittung enthalten **nie** base64 oder Bilddaten — auch nicht für eigene Items. **Verhaltensseitig (Beschreibung, echte Connector-Probe):** die Tool-Beschreibung sagt ausdrücklich, dass dieses Tool **nur** aufgerufen wird, wenn der Mensch im Gespräch ausdrücklich den Bildinhalt verlangt, und nennt die Kosten. | Die Vorgabe ist strenger als ein Recht: sie ist eine Aufrufdisziplin. Ein Code-Gate kann „hat der Mensch gefragt?" nicht wissen. **Der Plan darf nicht so tun, als könne er es** — deshalb die Trennung, und deshalb eine eigene Abnahmezeile für die verhaltensseitige Hälfte. |
| **P6.5-O** | **B4s Ankündigungspflicht ist ebenfalls verhaltensseitig** und steht als **erster Satz** in der Beschreibung von `put_item_asset`: *„Kündige dem Nutzer VOR jedem Aufruf an, dass du jetzt ein Bild ablegst. Bei jedem Aufruf, nicht nur beim ersten."* Zusätzlich, **erzwingbar**: `annotations={"destructiveHint": True, "idempotentHint": False, "openWorldHint": False, "readOnlyHint": False}` — dieselbe Einstufung wie `patch_item`. | „Kann nicht auf ‚immer erlauben' stehen" ist **Client-Verhalten von claude.ai** (Werkzeug-Zustimmungs-UI), das der Server weder setzt noch prüft. `destructiveHint: True` ist der einzige Hebel, den das Protokoll dafür anbietet — ob claude.ai daraus tatsächlich eine wiederholte Rückfrage macht: `[VERIFY]` **V64**. |
| **P6.5-P** | **`put_item_asset` schreibt nur, wohin auch `create_item`/`patch_item` schreiben dürfen** — `permissions.can_write_item(principal.space, acl, surface=Surface.AGENT)`, dieselbe Zeile wie `append_to_item` (`tools.py` Z. 617). Kein eigener Rechteweg. | P6-AW eine Ebene höher: ein zweiter Rechteweg für Bilder wäre eine dritte Wahrheit neben `.share.yml` und `share_read`/`share_write`. |
| **P6.5-Q** | **Kein MCP-Tool entfernt ein Bild, und kein MCP-Tool setzt Rechte.** Die „löscht nicht"-Hälfte von P6-AA bleibt gelockt; P6-M (Freigaben nur durch Menschen) gilt unverändert — **kein** Asset-Tool bekommt einen `share_*`/`visibility`-Parameter. | Entfernen ist (bei N5 = ja) ein Menschenweg über die Web-UI; ein Agent, der Binärdaten aus fremden Items entfernen kann, ist eine Angriffsfläche ohne genannten Nutzen. |
| **P6.5-R** | **`asset_id` und `item_id` werden gegen `^ast_[0-9a-f]{8}$` bzw. `^itm_[0-9a-f]{8}$` validiert, bevor sie in einen `Path` fließen** — an **jeder** Eintrittsstelle (REST-Route, MCP-Tool, `files.asset_path()`). | Pfad-Traversal. Dieselbe Disziplin wie `_resolve_static_path()` (`static_routes.py`). Die Validierung sitzt zusätzlich in `files.py`, damit sie nicht an einem künftigen dritten Adapter vorbeigeht. |
| **P6.5-S** | **`move_asset_dir()` verlangt ein **nicht existierendes** Zielverzeichnis.** Existiert es, ist das ein Fehler, kein Merge. | **Empirisch geprüft in dieser Session** (V61 geschlossen): `os.replace()` auf ein Verzeichnis funktioniert auf `ext4` bei gleichem Dateisystem und wirft bei nicht-leerem Ziel `OSError(39, 'Directory not empty')`. Ein stiller Merge zweier Asset-Verzeichnisse wäre ein Datenmischfehler; ein Cross-Space-Move trifft im Normalfall nie ein existierendes Ziel (die `item_id` ist global eindeutig). |
| **P6.5-T** | **Fünfte, benannte Öffnung des P1-Contracts** (`storage/{files,store,models}.py`), **anzukündigen in `phase1_storage/CLAUDE.md` unter „Geerbte Contracts", BEVOR Code entsteht** — dieselbe Disziplin wie bei `patch()`, `acl_of()`, `move()`. Bei **N5 ≠ „gar nicht"** gehört zusätzlich eine datierte Notiz zu Entscheidung **H** dorthin. | Vorgabe aus `IMAGES_PLAN.md` §2, unverändert übernommen. Vier Vorgänger, gleiche Mechanik. |
| **P6.5-U** | **P6-D bleibt scharf:** die Charakterisierungstests (`phase6_shares/tests/test_characterization.py`, Golden Files) müssen **vor und nach** jedem `storage/`-Umbau **byte-identisch** grün sein. Ein Ausschlag ist ein Befund, kein anzupassender Golden File. | Ersatz für den Seam-Beweis, seit Block B von P6. Bilder fassen `store.py` an — genau der Fall, für den P6-D existiert. |
| **P6.5-V** | **Kein CSP-Eingriff.** `webui/security.py` Z. 43–47 liefert bereits `img-src 'self' data:`. Wer diesen Header anfasst, hat etwas falsch gemacht. `data:`-URIs bleiben trotzdem **im Body verboten** (siehe Step B3s `safeSrc()`) — die Lockerung dort gilt dem P4-QR-Code, nicht Nutzerinhalt. | Aus `IMAGES_PLAN.md` §2 übernommen, in dieser Session gegen `security.py` nachgeprüft. |

---

## §2 Berührungsfläche

**Erlaubt:**
- `phase2_mcp/mcpserver/tools.py`, `phase2_mcp/mcpserver/receipts.py` (Block A + B4).
- `phase1_storage/storage/{files,store,models}.py` — fünfte, benannte Contract-Öffnung (**P6.5-T**);
  `search()` nur bei **N4 = ja**.
- `phase5_ui/webui/{api,serializers}.py`, `phase5_ui/webui/static/**` (Block B).
- `phase3_edge/scripts/diagnose.sh` (neue Prüfung 13).
- `docs/UPDATE_LOG.md` (P6-X-Gate erzwingt einen Eintrag vor dem Deploy).

**Tabu, `git diff` muss leer bleiben:** `phase2_mcp/mcpserver/{permissions,server,asgi}.py`
(die Rechtepolitik bekommt für Bilder **nichts** Neues — P6-AW/P6.5-P), `phase4_auth/**`,
`phase1_storage/storage/index.py` (P6-AY), `phase5_ui/webui/security.py` (P6.5-V).

**Prüfbefehl (in jeden Step-Abschluss aufnehmen):**
```
git diff --stat -- phase2_mcp/mcpserver/permissions.py phase2_mcp/mcpserver/server.py \
  phase2_mcp/mcpserver/asgi.py phase4_auth phase1_storage/storage/index.py \
  phase5_ui/webui/security.py
```

---

## §3 Schritt-Sequenz

> Reihenfolge ist verbindlich. Block A ist vollständig unabhängig von Block B und darf allein
> deployt werden — das ist der Sinn des Blockschnitts.

### Step 0 — Haushalt und Ankündigungen (kein Feature-Code)

1. **N1–N6 sind bereits beantwortet** (§0.0, 2026-08-20, per `AskUserQuestion` in der
   auftraggebenden Claude-Code-Session). Beim Kickoff: Antworten in den neuen Phase-Head
   übernehmen (📕-Konvention — dieses Dokument bleibt Snapshot, §0.0 ist die Quelle).
2. Phase-Verzeichnis + Phase-Head anlegen (`phase6_5_tools_images/CLAUDE.md`, Konvention P1–P6:
   entsteht beim Kickoff, nicht in der Planung), Zeile in `docs/INDEX.md`.
3. `ROADMAP.md`: neue Phasenzeile in der Tabelle + eigener Abschnitt (DRIN/DRAUSSEN/Status),
   Muster wie Phase 6.
4. **§0.2 ausführen** — Nachrangig-Notiz in `phase6_shares/IMAGES_PLAN.md`, `docs/INDEX.md`-Zeile
   nachziehen.
5. **P6.5-T ausführen** — fünfte Contract-Öffnung in `phase1_storage/CLAUDE.md` ankündigen,
   **bevor** Step B1 Code schreibt.
6. `app.html` Z. 281 bleibt unangetastet — verweist weiterhin korrekt auf die künftige Phase 7
   (Space-Admin-UI), keine Kollision mit dieser Phase 6.5.
7. `pytest` als Ausgangsstand festhalten (**772 grün**, Stand `main`@`2a4d8ca` — `[VERIFY]` V70).
8. **Vor jedem Deploy dieser Phase:** `phase3_edge/scripts/diagnose.sh` frisch fahren (neue
   Prüfung 5, echter externer Pfad) — geerbte Auflage aus `phase3_edge/CLAUDE.md`,
   „[2026-08-19 MUSS-VOR-DEM-NÄCHSTEN-DEPLOY]".

**DoD:** Head + Index + Roadmap stehen, Notizen gesetzt, `pytest` unverändert grün, N1–N6
beantwortet und im Head protokolliert.

---

### Block A — Werkzeug-Ergonomie

#### Step A1 — Beschreibungen: Falschaussage, Statuswerte, Aufgabenteilung, Suchreichweite

**Datei: `phase2_mcp/mcpserver/tools.py`** (nur Beschreibungstexte + zwei Hilfsfunktionen, keine
Signaturänderung).

Neue Modul-Ebene-Helfer, direkt neben `compact_json()` (Z. 103):

```python
def _status_hint() -> str:
    """Statusvokabular aus storage.models.STATUS_VALUES generiert (P6.5-C) — nie abtippen."""
    parts = [
        f"{t}: {'|'.join(sorted(valid_statuses(t)))}"
        for t in sorted(STATUS_VALUES)
    ]
    return "Erlaubte status-Werte je type — " + " · ".join(parts) + "."

WRITE_TOOL_DIVISION = (
    "Aufgabenteilung der Schreib-Werkzeuge: create_item legt neu an · "
    "update_item ändert Frontmatter (status/tags/links/due/title) und optional den ganzen Body · "
    "append_to_item hängt Text ans Body-Ende · "
    "patch_item ersetzt exakte Textstellen IM BODY. "
    "patch_item und append_to_item erreichen Frontmatter grundsätzlich nicht."
)
```

Import ergänzen: `from storage.models import STATUS_VALUES, valid_statuses`.

Änderungen an den Beschreibungen:

| Tool | Anker | Änderung |
|---|---|---|
| `list_spaces` | Z. 260–265 | **P6.5-B, Falschaussage raus.** Neu: *„Listet alle sichtbaren Spaces mit Item-Anzahl, Mitgliedern und Ordnern. `writable:true` heißt: du darfst dort schreiben — das gilt für deinen eigenen Space UND für geteilte Spaces, in denen dir `write:` gewährt wurde. Ruf dies zuerst auf, wenn unklar ist, wo geschrieben werden darf; rate es nicht."* |
| `search_items` | Z. 313–318 | **P6.5-H.** Ergänzen: *„Gesucht wird als Teilstring in Titel und Tags (Groß/Kleinschreibung egal) — NICHT im Body. Wenn ein Begriff nichts findet, liegt er vermutlich nur im Fließtext: dann über tags/type/status/folder filtern statt den Suchbegriff zu variieren."* (Bei **N4 = ja** zusätzlich: *„…oder `in_body=True` setzen."*) |
| `get_item` | Z. 386 | Ergänzen: *„Liefert immer den vollen Body. Wenn du nur die aktuelle `version` oder Frontmatter brauchst, nimm `get_item_meta` — das ist um Größenordnungen billiger."* |
| `create_item` | Z. 414–421 | `+ " " + _status_hint() + " " + WRITE_TOOL_DIVISION` **plus Querverweis (zweite Hälfte von P6.5-B, Auffindbarkeit):** *„Unklar, in welche Spaces du schreiben darfst? Ruf zuerst `list_spaces` — `writable:true` ist die Antwort."* Begründung wie P6.5-D: ein Modell liest die Beschreibung des Tools, das es gerade erwägt, nicht die eines Tools, das es nicht gefunden hat. |
| `update_item` | Z. 463–470 | dito (inkl. Querverweis) |
| `append_to_item` | Z. 594–601 | dito, **plus P6.5-G**: *„Mehrere Einträge in einem Aufruf: übergib einen Text mit Zeilenumbrüchen — ein Aufruf, ein Commit, eine Versionserhöhung. Die Quittung enthält die neue `version`; du brauchst zwischen aufeinanderfolgenden Appends kein erneutes `get_item`."* |
| `patch_item` | Z. 629–638 | `+ " " + WRITE_TOOL_DIVISION` |

**Tests** (`phase2_mcp/tests/test_tools.py`, +5):
- `test_list_spaces_description_does_not_claim_own_space_only` — die Beschreibung enthält **nicht**
  mehr „nur für den eigenen Space" und erwähnt geteilte Spaces.
- `test_write_tool_descriptions_document_status_values` — für jeden Typ in `STATUS_VALUES` und
  jeden Wert darin: der Wert kommt in `create_item`s und `update_item`s Beschreibung vor
  (**P6.5-C**, fängt künftige Drift).
- `test_all_write_tools_carry_the_division_of_labour` — `WRITE_TOOL_DIVISION` ist Teilstring aller
  vier Beschreibungen.
- `test_search_description_states_title_and_tag_scope`.
- `test_write_tool_descriptions_point_to_list_spaces` — `create_item`/`update_item` nennen
  `list_spaces` (Auffindbarkeitshälfte von P6.5-B).
- `test_get_item_description_points_to_get_item_meta` (nach Step A2; bis dahin xfail/verschieben).

> Beschreibungstexte über `mcp._tool_manager` bzw. den von `register()` zurückgegebenen
> Funktionsdict auslesen — `[VERIFY]` **V63**: der etablierte Weg in dieser Suite ist
> `inspect.signature()` auf die zurückgegebenen Funktionen; ob die **Beschreibung** dort ebenso
> erreichbar ist oder über `await mcp.get_tools()` gelesen werden muss, gegen `fastmcp==3.4.4`
> prüfen (die Suite hat schon `fastmcp.Client`-Tests, siehe `phase2_mcp/tests/test_app.py`).

**DoD:** 6 neue Tests grün, `pytest` 772 → 778, Tabu-Diff leer, `mcp_smoke.py` unverändert grün.

#### Step A2 — Achtes Tool `get_item_meta` (P6.5-E/P6.5-F)

`tools.py`, direkt nach `get_item` (Z. 384–411) — gleiche Reihenfolge im Body wie dort
(`_authenticated_principal()` → `store.acl_of()` → `can_read_item(..., Surface.AGENT)` → Store →
Formatieren):

```python
@mcp.tool(
    title="Item-Metadaten lesen",
    description=(
        "Liest NUR Frontmatter und Version eines Items — ohne Body. Billig. "
        "Nimm dies statt get_item, wenn du die aktuelle version für einen Schreibaufruf "
        "brauchst oder nur Status/Tags/Ordner prüfen willst. body_bytes sagt dir, wie teuer "
        "ein get_item wäre."
    ),
    annotations={"readOnlyHint": True, "destructiveHint": False,
                 "idempotentHint": True, "openWorldHint": False},
)
def get_item_meta(item_id: str) -> str: ...
```

Rückgabe (`compact_json`), Felder exakt: `id`, `space`, `folder`, `type`, `title`, `status`,
`due` (ISO oder `null`), `tags`, `links`, `visibility`, `share_read`, `share_write`, `version`,
`created`, `updated` (beide über `_format_dt`), `body_bytes` (`len(item.body.encode("utf-8"))`),
`own` (`acl.space == principal.space`), `writable`
(`permissions.can_write_item(principal.space, acl, surface=Surface.AGENT)`).
**Nach Block B zusätzlich:** `assets` (siehe Step B4).

`store.get(item_id, repair_drift=False)` — ein reiner Metadaten-Lesevorgang soll **keinen**
Drift-Repair-Write auslösen; das ist bei `get_item` bewusst anders (dort steuert `writable` den
Repair). Als Kommentar in den Code, sonst wirkt es wie ein vergessener Parameter.

`register()`s Rückgabedict um `"get_item_meta"` erweitern (Z. 670 ff.).

**Tests** (`phase2_mcp/tests/test_tools.py`, +4): liefert Version ohne Body · enthält **keinen**
Body-Text (Negativ-Assertion auf einen im Body eindeutigen Marker) · fremdes, freigegebenes Item
ist lesbar und trägt `own:false` · fremdes Item ohne Grant → `PermissionDenied`.
`mcp_smoke.py` um einen `get_item_meta`-Schritt erweitern (13 → 14 Prüfungen).

**DoD:** 4 neue Tests grün (778 → 782), `mcp_smoke.py` 14/14, Tabu-Diff leer.

#### Step A3 — Bulk-Append: bewusst **nicht** gebaut (P6.5-G, vorbehaltlich N3)

Kein Code. Der Punkt ist in Step A1 durch die Beschreibung erledigt. **Im Phase-Head als
ausdrücklich abgelehnter Wunsch protokollieren**, mit der Begründung aus **N3** — ein gemeldeter
Wunsch, der wortlos verschwindet, taucht in drei Monaten erneut auf.

**Falls N3 = „doch bauen":** `append_to_item(item_id, version, text=None, texts=None, ...)`,
genau eine der beiden gesetzt (sonst `ValidationError`), `"\n".join(texts)` **vor** dem
`store.append()`-Aufruf, **ein** Commit, **ein** Versionssprung, Quittung um
`appended_parts: len(texts)` erweitert. +3 Tests (beide gesetzt → Fehler · keins gesetzt →
Fehler · drei Teile ergeben einen Commit).

#### Step A4 — Body-Suche als Opt-in (nur bei **N4 = ja**)

`phase1_storage/storage/store.py :: search()` (Z. 382 ff.):
- neuer Keyword-Parameter `in_body: bool = False`;
- in `matches()` (Z. 401 ff.), Query-Zweig Z. 414–417:
  ```python
  haystack = f"{item.title} {' '.join(item.tags)}"
  if in_body:
      haystack += " " + item.body
  if query.lower() not in haystack.lower():
      return False
  ```
  **Kein zusätzlicher Datei-Zugriff** — `item.body` ist bereits geladen (`_row_to_item()`).
- `mcpserver/tools.py :: search_items()` bekommt `in_body: bool = False` und reicht durch.
- **Die Web-UI bekommt nichts** (Q1 bleibt für die UI gelockt). `webui/api.py` unverändert.

**Tests:** `phase1_storage/tests/test_store.py` +3 (Default findet Bodytreffer **nicht** ·
`in_body=True` findet ihn · `in_body=True` ändert Sortierung/Total-Semantik nicht),
`phase2_mcp/tests/test_tools.py` +1 (Durchreichung). **P6.5-U:** Charakterisierung vorher/nachher
byte-identisch grün.

**DoD:** 4 neue Tests, Charakterisierung grün, `webui/`-Diff leer.

**Gate A → B:** Block A ist deploybar, sobald `pytest` grün, `mcp_smoke.py` grün, Tabu-Diff leer
und **eine echte Connector-Probe** durch den Nikinger gelaufen ist (Abnahmezeilen P6.5-1 – P6.5-4). Block B
darf davor gebaut, aber **nicht** davor deployt werden — ein Deploy, der Beschreibungsfehler und
den ersten Binärdatenpfad bündelt, macht jede Fehlersuche danach zweideutig.

---

### Block B — Bilder

#### Step B1 — Storage-Fundament (`storage/`, kein Adapter)

**Voraussetzung: P6.5-T ist angekündigt** (Step 0 Punkt 5). **P6-D:** Charakterisierung **vorher**
laufen lassen und den Golden-Stand festhalten.

`phase1_storage/storage/models.py` — neu:
```python
@dataclass(kw_only=True)
class AssetInfo:
    id: str          # ast_<8hex>
    mime: str        # image/png|image/jpeg|image/gif|image/webp
    bytes: int
    filename: str    # bereinigt, rein kosmetisch — NIE für die Pfadbildung
    created: datetime
```

`phase1_storage/storage/files.py`:
- `ASSET_ID_PREFIX = "ast_"`, `new_asset_id() -> str` (Zwilling zu `generate_id()`, Z. 33).
- `ASSET_ID_RE = re.compile(r"^ast_[0-9a-f]{8}$")`, `ITEM_ID_RE = re.compile(r"^itm_[0-9a-f]{8}$")`
  (**P6.5-R**) — `[VERIFY]` **V65**: das reale ID-Format gegen `generate_id()` prüfen (8 Hex ist die
  Erwartung aus P1-Entscheidung F; wenn `generate_id()` etwas anderes liefert, gewinnt der Code
  und beide Regexe ziehen nach).
- `ASSET_MIME_TYPES: tuple[tuple[bytes, str, str], ...]` — (Magic-Präfix, MIME, Endung) für
  PNG (`\x89PNG\r\n\x1a\n`), JPEG (`\xff\xd8\xff`), GIF (`GIF87a`/`GIF89a`),
  WebP (`RIFF` + Offset 8 `WEBP` — **Zweiteilprüfung**, nicht nur Präfix).
- `sniff_image_mime(data: bytes) -> tuple[str, str] | None` → (MIME, Endung) oder `None`.
  **SVG, HEIC, PDF sind nicht dabei und werden nicht ergänzt** (P6-AZ).
- `asset_dir(data_root, space, item_id) -> Path` → `<data_root>/<space>/_assets/<item_id>`;
  validiert `item_id` gegen `ITEM_ID_RE`, sonst `ValidationError`.
- `asset_path(data_root, space, item_id, asset_id, ext) -> Path`; validiert beide IDs.
- `move_asset_dir(src_dir: Path, dst_dir: Path) -> None` — **No-op, wenn `src_dir` nicht
  existiert** (Normalfall); sonst `dst_dir.parent.mkdir(parents=True, exist_ok=True)`,
  `os.replace(src_dir, dst_dir)`, `fsync` auf **beiden** Elternverzeichnissen. Existiert `dst_dir`
  bereits nicht-leer, propagiert `OSError(ENOTEMPTY)` unverändert (**P6.5-S**).

`phase1_storage/storage/store.py` (alle unter `self._lock`, Muster wie `append()` Z. 523 ff.):
- `put_asset(item_id, *, data: bytes, filename: str | None = None) -> AssetInfo`
  → `sniff_image_mime()` (`None` ⇒ `ValidationError`), `new_asset_id()`, `asset_dir().mkdir(...)`,
  atomarer Write (tmp + `os.replace` + `fsync` des Verzeichnisses — dieselbe Mechanik wie
  `atomic_write()` Z. 99, aber **binär**: entweder `atomic_write()` um einen Bytes-Zweig
  erweitern oder ein `atomic_write_bytes()` daneben; **Empfehlung: zweite Funktion**, damit die
  Textvariante ihre `encoding`-Semantik behält), dann `self._commit("asset", item_id, space)`
  (**B1**: genau **ein** Commit).
- `list_assets(item_id) -> list[AssetInfo]` — `iterdir()`, sortiert nach Name; `_trash/` wird
  übersprungen (nur bei N5 = „Verschieben"). Kein Index (**P6-AY**).
- `get_asset(item_id, asset_id) -> tuple[bytes, str]` — Bytes + MIME (MIME erneut aus den Magic
  Bytes, **nicht** aus der Endung).
- `delete_asset(item_id, asset_id) -> None` — **nur bei N5 ≠ „gar nicht"**; Empfehlung:
  `move_file()` nach `_assets/<item_id>/_trash/`, ein Git-Commit.
- `move()` (Z. 595 ff.) ruft zusätzlich `files.move_asset_dir(...)` — **innerhalb** derselben
  Lock-Sektion und **vor** dem Git-Commit, damit ein Move genau **einen** Commit erzeugt
  (P6-Abnahmezeile 26s Mechanik bleibt erhalten).
- `archive()` (Z. 572 ff.) lässt `_assets/<item_id>/` **stehen**.

**Tests** — `phase1_storage/tests/test_files.py` (+6): Magic-Byte-Erkennung je Format · WebP nur
mit korrektem Offset-8-`WEBP` · unbekannte Bytes → `None` · SVG abgelehnt · `asset_path()`
verweigert eine ungültige ID · `move_asset_dir()` ist No-op ohne Quellverzeichnis.
`phase1_storage/tests/test_store.py` (+8): `put_asset()` legt atomar an und erzeugt **genau einen**
Commit · `list_assets()` leer für ein Item ohne Bilder · `get_asset()` liefert Bytes+MIME ·
`delete_asset()` (N5-abhängig) · **`move()` zieht das Asset-Verzeichnis mit und erzeugt weiterhin
genau EINEN Commit** (**der wichtigste Test dieses Plans**) · `move()` ohne Assets unverändert
(Regression gegen die sechs Step-7b-Tests) · `archive()` lässt Assets liegen ·
`list_spaces()` zeigt `_assets` weiterhin nicht als Ordner (bestehender Test, muss grün bleiben).

**DoD:** +14 Tests, **Charakterisierung byte-identisch grün** (P6.5-U), Tabu-Diff leer.

#### Step B2 — REST-Fläche (`webui/`)

`phase5_ui/webui/api.py`:
- `MAX_ASSET_BYTES = 5 * 1024 * 1024` neben `MAX_BODY_BYTES` (Z. 105), mit Kommentar, **warum**
  es eine eigene Konstante ist (**P6.5-L**).
- neuer `async def _raw_body(request) -> bytes` — liest `await request.body()`, prüft gegen
  `MAX_ASSET_BYTES`, `413` (`payload_too_large`) bei Überschreitung. **Nicht** `_json_body()`.

| Route | Rechteprüfung | Anmerkung |
|---|---|---|
| `POST /api/v1/items/{item_id}/assets` | `store.acl_of()` + `can_write_item_as_human()` | Rohe Bytes im Request-Body (**kein** multipart, **kein** base64 — kein Parser-Zuwachs). `Content-Type` des Clients wird **ignoriert** (P6-AZ). CSRF wie jeder Schreibpfad (`_require_csrf_json`s Herkunftsprüfung — `[VERIFY]` **V66**: die Funktion prüft ggf. auch den JSON-Content-Type; falls ja, den Herkunftsteil herauslösen statt zu umgehen). `201` + `AssetInfo`-JSON. |
| `GET /api/v1/items/{item_id}/assets/{asset_id}` | `store.acl_of()` + `can_read_item_as_human()` (**P6-AW**) | Rohe Bytes, `Content-Type` aus den Magic Bytes, `Content-Disposition: inline`, `Cache-Control: no-store`. `X-Content-Type-Options: nosniff` kommt bereits aus `ui_security_headers()` — `[VERIFY]` **V67**: dass der Header auch auf `/api/v1/**` gesetzt wird und nicht nur auf die UI-Seiten. |
| `GET /api/v1/items/{item_id}/assets` | wie Lesen | Liste für den Editor. |
| `DELETE /api/v1/items/{item_id}/assets/{asset_id}` | wie Schreiben | Nur bei **N5 ≠ „gar nicht"**. |

Fehlerverhalten: fremdes/nicht existierendes Item liefert **denselben** Statuscode für „gibt es
nicht" und „darfst du nicht" (bestehende Praxis in `_items_get_one`, Z. 402–409 — **nicht** neu
erfinden, dortiges Verhalten kopieren).

`phase5_ui/webui/serializers.py :: item_to_json()` bekommt `"assets": [...]` (Metadaten, kein
Fließtext — dieselbe Einstufung wie der Sichtbarkeits-Chip). `summary_to_json()` bekommt
**nichts** (Listenzeilen bleiben schlank).

**Tests** (`phase5_ui/tests/test_api.py`, +6): Upload/Download-Roundtrip · zu groß → `413` ·
falscher Typ (z. B. SVG) → `422` · `DELETE` (N5-abhängig) · fremde Item-ID → kein
Existenzunterschied · Assets erscheinen in `item_to_json()`.
`phase6_5_tools_images/tests/test_assets_acl.py` (neu, +4 — Testheimat ist das NEUE Phasenverzeichnis, nicht `phase6_shares/`, siehe P6.5-A): fremdes Item mit `share_read` → Bild lesbar · ohne Grant → `403` · `share_read` allein
erlaubt kein `POST` · Asset folgt dem Item in den Zielspace und ist danach für die **Ziel**-Space-
Mitglieder lesbar (Zwilling zu `test_acl_decision_follows_the_item_into_the_target_space`).

**DoD:** +10 Tests, Tabu-Diff leer.

#### Step B3 — Web-UI: Anzeigen und Einfügen

`phase5_ui/webui/static/js/markdown.js` — **die Stelle, an der Bilder heute sterben:**
1. **`inlineMarkdown()` (Z. 25–31) bekommt einen Bildzweig VOR dem Link-Replace** (**P6.5-J**):
   ```js
   .replace(/!\[([^\]]*)\]\(([^)\s]+)\)/g, '<img src="$2" alt="$1">')
   ```
   direkt **vor** der bestehenden `\[…\]\(…\)`-Zeile. Ohne diese Reihenfolge frisst die
   Link-Regex das Bild.
2. `ALLOWED_TAGS` (Z. 186–189) um `"IMG"`; `ALLOWED_ATTRS` (Z. 190–194) um
   `IMG: new Set(["src", "alt"])`.
3. Neue `safeSrc(src)` neben `safeHref()` (Z. 197–202): akzeptiert **ausschließlich**
   `/^\/api\/v1\/items\/itm_[0-9a-f]{8}\/assets\/ast_[0-9a-f]{8}$/`. Alles andere ⇒ `<img>` durch
   seinen `alt`-Text ersetzen (**nicht** nur das Attribut entfernen — ein `<img>` ohne `src` ist
   ein toter Knoten). **Keine `data:`-URIs**, obwohl die CSP sie erlaubt (**P6.5-V**).
4. `markdownToHtml(src, options)` bekommt einen optionalen zweiten Parameter mit `{ itemId }`;
   im Bildzweig wird `asset:<asset_id>` zu `/api/v1/items/<itemId>/assets/<asset_id>` aufgelöst.
   **Fallende Kante:** `updates.js` ruft `markdownToHtml()` **ohne** Item-Kontext — dort darf ein
   `asset:` schlicht **nicht** auflösen und muss als Alt-Text erscheinen, **nicht** crashen.
   Alle Aufrufstellen mit `grep -rn "markdownToHtml" phase5_ui/webui/static/js/` prüfen.
5. **P6.5-K:** Kopfkommentar Z. 4–9 korrigieren (`IMG`/`#asset:` sind nicht mehr „bewusst nicht
   übernommen").
6. **P5-Y bleibt unangetastet:** kein serverseitiges HTML-Rendern.

`editor.js`: „Bild einfügen"-Knopf in der Formatierhilfen-Leiste — Dateiauswahl (`<input
type="file" accept="image/png,image/jpeg,image/gif,image/webp">`) → `POST` der rohen Bytes →
`![<Dateiname>](asset:<id>)` an der Cursorposition (dieselbe Mechanik wie der Link-Einfüger,
Z. 465–466). Fehlerfälle als Toast (`413`/`422`), nicht als stiller Nicht-Effekt.
**Einfügen per Zwischenablage/Drag & Drop ist v2** — der Knopf ist der Pflichtweg (dieselbe Regel
wie P6-AB).

`app.css`: `.md-body img { max-width: 100%; height: auto; }` — mehr nicht (**P6-BA**).

**Tests:** kein Unit-Test (P5-T). Stattdessen **Playwright gegen eine Wegwerf-Instanz** (Standing
Permission, eigener Port, `tmp`-`DATA_ROOT`, eigenes venv — **nie** die laufende Instanz):
Bild hochladen · im gerenderten Markdown sichtbar (**auf `naturalWidth > 0` prüfen**, nicht nur
auf Existenz des `<img>` — ein kaputter Pfad rendert trotzdem ein Element) · Screenshot ansehen ·
Konsolenfehler-Listener sauber · `![x](javascript:alert(1))` und
`![x](https://fremde.example/pixel.png)` werden entfernt und erzeugen **keinen** Netzabruf
(Netzwerk-Listener) · ein `asset:`-Link im Update-Banner crasht nicht.

**DoD:** Playwright-Lauf grün und **gesehen** (nicht behauptet), `pytest` unverändert,
Tabu-Diff leer.

#### Step B4 — MCP-Fläche (`mcpserver/tools.py`)

**V59 ist in dieser Planungssession empirisch geschlossen** (nicht nur aus der Spec abgeleitet) —
`fastmcp==3.4.4`, `fastmcp.utilities.types.Image(data=…, format="png")` wird von einem Tool mit
Rückgabetyp `Image | str` korrekt zu `ImageContent` bzw. `TextContent` konvertiert; geprüft über
einen `fastmcp.Client`-In-Process-Lauf. **Sonnet muss das nicht erneut herleiten**, nur den Import
setzen: `from fastmcp.utilities.types import Image`.

1. **Die `assets`-Liste (id/MIME/Bytes/Dateiname) erscheint AUSSCHLIESSLICH in `get_item_meta`s
   JSON** — **kein** base64, und `get_item`s Rückgabe bleibt **byte-identisch** wie heute.
   **Begründung (bewusste Designentscheidung, kein `[VERIFY]`):** `get_item` gibt
   `item_to_filetext(item)` zurück — genau den Text, den ein Modell liest, bearbeitet und über
   `update_item(body=…)` zurückschreibt. Eine eingefügte Kommentarzeile (`<!-- assets: … -->`)
   landete beim nächsten Roundtrip **im Body** und verschöbe zusätzlich die Byte-Anker, gegen die
   `patch_item` exakt matcht — „0 Treffer" wäre die Folge, also genau die Fehlerklasse, gegen die
   diese Phase gebaut wird. `get_item`s Beschreibung verweist stattdessen auf `get_item_meta`
   (Step A1).

2. **Neuntes Tool `get_item_asset(item_id, asset_id) -> Image | str`** (**P6.5-M/P6.5-N**):
   ```python
   @mcp.tool(
       title="Bildinhalt eines Items laden",
       description=(
           "Lädt die echten Bildbytes eines Bildes. TEUER — rufe dies NUR auf, wenn der "
           "Nutzer im Gespräch ausdrücklich verlangt, dass du den Bildinhalt ansiehst. "
           "Lade Bilder NIE automatisch, nur weil ein Item eine asset:-Referenz enthält — "
           "auch nicht bei eigenen Items. Für die reine Liste vorhandener Bilder reicht "
           "get_item_meta. Bilder aus fremden Spaces liefern nur dann Bytes, wenn du dort "
           "Schreibrechte hast; sonst bekommst du nur Metadaten."
       ),
       annotations={"readOnlyHint": True, "destructiveHint": False,
                    "idempotentHint": True, "openWorldHint": False},
   )
   ```
   Body-Reihenfolge: `_authenticated_principal()` → `store.acl_of(item_id)` →
   `can_read_item(..., Surface.AGENT)` (sonst `PermissionDenied`) → **P6.5-M-Bedingung**:
   ```python
   own = acl.space == principal.space
   may_see_bytes = own or permissions.can_write_item(
       principal.space, acl, surface=Surface.AGENT)
   ```
   `may_see_bytes is False` ⇒ **`compact_json`-Metadaten + Klartexthinweis** zurückgeben
   („Bildbytes aus einem fremden Space werden nur bei Schreibrecht geliefert"), **keine Bytes**.
   Sonst `data, mime = store.get_asset(...)`; `return Image(data=data, format=mime.split("/")[-1])`.
   `[VERIFY]` **V69**: dass `format="jpeg"` von `Image` als `image/jpeg` gemappt wird (bei
   `image/jpeg` liefert `split("/")[-1]` „jpeg" — ggf. das MIME direkt über
   `Image(...).to_image_content(mime_type=mime)` setzen statt über `format`; der sichere Weg ist
   das explizite `mime_type`).

3. **Zehntes Tool `put_item_asset(item_id, data_base64: str, filename: str | None = None)**
   (**B4/P6.5-O/P6.5-P**) — Beschreibung beginnt mit der Ankündigungspflicht (P6.5-O, Wortlaut dort).
   Rechte: `can_write_item(..., Surface.AGENT)`. Dekodiert base64 (`binascii.Error` ⇒
   `ValidationError` mit Klartext), prüft gegen `MAX_MCP_ASSET_BYTES` (**N6**, Empfehlung 1 MiB),
   ruft `store.put_asset()`, gibt eine **Quittung** über `write_receipt()`-Muster zurück
   (`op="asset"`, `asset_id`, `mime`, `bytes`, `item_version` unverändert) — **nie** die Bytes.
   Hinweis in der Quittung: *„Referenz im Body ergänzen mit `![Alt](asset:<id>)` — put_item_asset
   ändert den Body NICHT."*

4. `create_item`/`update_item`/`patch_item` bekommen **nichts** — Bilder laufen ausschließlich über
   `put_item_asset` (ein Schreibweg, ein Riegel).

5. `register()`s Rückgabedict um `get_item_asset`/`put_item_asset` erweitern; `mcp_smoke.py`
   um beide erweitern (14 → 16).

**Tests** (`phase2_mcp/tests/test_tools.py`, +7): `get_item_meta` listet Assets ohne Bytes ·
`get_item_asset` liefert `ImageContent` für ein eigenes Item · **fremdes Item mit `share_read`
(kein Write) → Metadaten, keine Bytes** (der B3-Kerntest) · fremdes Item **mit** `share_write` →
Bytes · fremdes Item ohne Grant → `PermissionDenied` · `put_item_asset` schreibt und liefert eine
Quittung ohne Bytes · `put_item_asset` in einen fremden Space ohne `write:` → `PermissionDenied`.
**Plus ein struktureller Test (P6.5-N, erzwingbare Hälfte):** für ein Item mit Bild enthält
**keine** Rückgabe von `get_item`, `get_item_meta`, `search_items` und **keine** Quittung eine
base64-Nutzlast (Assertion gegen den bekannten Bytes-Marker).

**DoD:** +8 Tests, `mcp_smoke.py` 16/16, Tabu-Diff leer (insbesondere `permissions.py`).

#### Step B5 — Betrieb und Deploy-Vorbereitung

- `phase3_edge/scripts/diagnose.sh`, **Prüfung 13**: Gesamtgröße aller `_assets/`-Verzeichnisse
  und Größe des `.git`-Verzeichnisses im `DATA_ROOT`, als **INFO** (kein Abbruchkriterium) —
  dieselbe Kategorie wie Prüfung 12. Begründung: **B2 = 5 MiB ohne Space-Budget** heißt
  *messen statt deckeln*; diese Zeile ist das Messgerät.
- `docs/UPDATE_LOG.md`: neuer Eintrag **oben**, heutiges Datum (P6-X-Gate in `deploy.sh` bricht
  sonst ab). Zwei Zeilen genügen: Bilder in Notizen; Claude-Werkzeuge klarer beschrieben.
- **Vor dem Deploy:** `diagnose.sh` frisch fahren (geerbte Auflage, Step 0 Punkt 8).
- `phase5_ui/scripts/ui_budget.py` einmal laufen lassen — die neuen `<img>`-Regeln und
  `editor.js`-Ergänzungen ändern die Nutzlast.

---

## §4 Sicherheitsbetrachtung (nicht optional)

1. **Hard Rule 4 und Bilder.** `<untrusted_content>` wrappt **Text**. Ein fremdes Bild vor einem
   sehenden Modell ist ein Injektionskanal, den dieser Wrapper strukturell **nicht** erreicht —
   die Bedrohung ist dieselbe, das Gegenmittel greift nicht. Deshalb **P6.5-M** (Bytes nur bei
   Schreibrecht) und **P6.5-N** (Bytes nie beiläufig). **Das darf nicht als „durch bestehende Regeln
   abgedeckt" durchrutschen.**
2. **Auslieferungsroute.** Genau **eine** ACL-Prüfung, auf demselben Pfad wie `_items_get_one`
   (P6-AW). Kein Weg, ein Asset ohne Item-ID zu adressieren — eine geratene `ast_`-ID nützt
   nichts, ohne die passende `itm_`-ID **und** Leserecht darauf.
3. **Typverwirrung.** Magic Bytes statt Client-Angabe, `nosniff` (V67), kein SVG (P6-AZ).
   `Content-Disposition: inline` **plus** korrektem MIME — kein Download-Umweg, über den ein
   Browser den Typ neu rät.
4. **Pfad-Traversal.** **P6.5-R**: beide IDs gegen strenge Regexe, validiert in `files.py` selbst,
   nicht nur am Adapter.
5. **Speicherverbrauch.** Rohe Bytes gehen komplett in den Speicher (wie `_json_body()` heute).
   Bei **B2 = 5 MiB** ist ein einzelner Upload unkritisch, aber es ist das **Fünffache** des
   bisherigen Maximums; eine weitere Erhöhung braucht Streaming, keinen größeren Riegel.
   Der MCP-Weg ist zusätzlich base64 (~+33 %) — Grund für den eigenen, kleineren
   `MAX_MCP_ASSET_BYTES` (**N6**).
6. **Kein neues Geheimnis.** Hard Rule 1 unberührt: keine Tokens, Keys, Credentials. `filename`
   wird bereinigt gespeichert und **nie** zur Pfadbildung benutzt.
7. **Git-Historie wächst monoton** (**B1 = ja**). Ein entferntes Bild gibt keine Bytes frei. Das
   ist bewusst akzeptiert; Prüfung 13 macht es sichtbar, bevor es weh tut.

---

## §5 Testliste (Pflicht, Zusammenfassung)

| Datei | Δ | Inhalt |
|---|---|---|
| `phase2_mcp/tests/test_tools.py` | +6 (A1) +4 (A2) +1 (A4, N4) +8 (B4) | Beschreibungen (P6.5-B/C/D/H), `get_item_meta`, `in_body`-Durchreichung, Asset-Tools inkl. **B3-Kerntest** und **P6.5-N-Strukturtest** |
| `phase1_storage/tests/test_files.py` | +6 | Magic Bytes je Format, WebP-Offset, SVG abgelehnt, ID-Validierung, `move_asset_dir()`-No-op |
| `phase1_storage/tests/test_store.py` | +8 (+3 bei N4) | `put/list/get/delete_asset`, **`move()` mit Assets = EIN Commit**, `move()` ohne Assets unverändert, `archive()`, `list_spaces()`-Regression, Body-Suche |
| `phase5_ui/tests/test_api.py` | +6 | Roundtrip, `413`, `422`, `DELETE`, kein Existenzunterschied, `item_to_json()` |
| `phase6_5_tools_images/tests/test_assets_acl.py` (neu) | +4 | `share_read` liest, ohne Grant `403`, `share_read` schreibt nicht, Asset folgt dem Item in den Zielspace |
| `phase6_shares/tests/test_characterization.py` | ±0 | **byte-identisch grün** vor und nach jedem `storage/`-Umbau (P6.5-U) |
| Playwright (Wegwerf-Instanz) | — | Upload sichtbar (`naturalWidth > 0`), Sanitizer entfernt `javascript:`/fremde URL **ohne Netzabruf**, `updates.js` crasht nicht, Konsole sauber |
| `mcp_smoke.py` | 13 → 16 | `get_item_meta`, `get_item_asset`, `put_item_asset` |

**Erwarteter Endstand `pytest`:** 772 → ~814 (± N3/N4/N5-Zweige).
**Harte Regel:** kein Step-Abschluss ohne grünes `pytest` (gemockt, kein Netz, kein echter
Tunnel) und leeren Tabu-Diff.

---

## §6 Abnahmekriterien (P6.5-1 – P6.5-14)

> **Eigene Zählung mit Präfix, bewusst:** P6s Abnahmezeilen 25–30 und 35–39 sind weiterhin
> offen und live; eine nackte „Zeile 13“ in einem künftigen Session-Block wäre zweideutig.

> ✅ heißt **live-verifiziert durch den Nikinger**, nicht „gebaut".

| # | Kriterium | Wie geprüft | Block |
|---|---|---|---|
| P6.5-1 | `list_spaces` beschreibt geteilte Spaces korrekt; eine frische Claude-Instanz sagt **nicht** mehr „ich kann nur im eigenen Space schreiben" | Nikinger, echter Connector, offene Frage an die Instanz | A |
| P6.5-2 | Eine Instanz nennt auf Nachfrage die erlaubten `status`-Werte **ohne** Fehlversuch | Nikinger, echter Connector | A |
| P6.5-3 | `get_item_meta` liefert Version + Frontmatter ohne Body; die Instanz nutzt es für einen Folge-Append | Nikinger, echter Connector | A |
| P6.5-4 | Eine Instanz erklärt die Aufgabenteilung `patch_item`/`update_item`/`append_to_item` **aus den Beschreibungen**, ohne Quellcode | Nikinger, echter Connector | A |
| P6.5-5 | Bild in der Web-UI hochgeladen, erscheint **sichtbar** im gerenderten Dokument | Nikinger, Browser | B |
| P6.5-6 | Die `.md`-Datei im `DATA_ROOT` enthält nur `![…](asset:ast_…)` — keine Binärdaten, kein base64 | Nikinger, `cat` im Datenverzeichnis | B |
| P6.5-7 | Die Bilddatei liegt unter `<space>/_assets/<item_id>/` und taucht in der UI **nicht** als Ordner auf | Nikinger, `ls` + Browser | B |
| P6.5-8 | Fabian öffnet ein ihm freigegebenes Item mit Bild und **sieht** es; ohne Freigabe liefert dieselbe Bild-URL `403` | Nikinger + Fabian, Browser + `curl` | B |
| P6.5-9 | Ein Upload erzeugt **genau einen** Git-Commit im `DATA_ROOT` (**B1**) | Nikinger, `git log --oneline` | B |
| P6.5-10 | Ein Cross-Space-Move nimmt das Bild mit; danach im Zielspace sichtbar, im Quellspace weg — **ein** Commit | Nikinger, Browser + `git log` | B |
| P6.5-11 | `![x](https://fremde.example/…)` und `![x](javascript:…)` im Body erzeugen **keinen** Netzabruf und kein `<img>` | Nikinger, DevTools-Netzwerktab | B |
| P6.5-12 | Ein Bild lässt sich wieder entfernen (Body-Referenz rendert danach als Alt-Text) — *entfällt bei N5 = „gar nicht"* | Nikinger, Browser | B |
| P6.5-13 | **B3 live:** Claude sieht ein Bild aus einem fremden, nur **lesbar** freigegebenen Item **nicht** (nur Metadaten); mit `share_write` sieht es das Bild | Nikinger + Fabian, echter Connector | B |
| P6.5-14 | **B3/B4 verhaltensseitig:** Claude lädt ein Bild **nicht** von sich aus, wenn ein Item eine `asset:`-Referenz trägt (erst auf ausdrückliche Bitte), und **kündigt jeden Upload vorher an** | Nikinger, echter Connector, zwei Gespräche | B |

> **Zeile P6.5-14 ist bewusst eine Verhaltens-, keine Codeprüfung** (P6.5-N/P6.5-O). Sie kann bei einer
> künftigen Modellversion anders ausfallen — dann ist das ein Befund für den Nikinger, kein
> stiller Fehlschlag.

**Geerbte, in dieser Phase NICHT gelöste Live-Proben** (nur mitgeführt, damit sie nicht
verschwinden): P6-Abnahmezeilen **25–30** (Step 7b, Item-Verschieben) und **35–39** (globale
Suche), **Gate A→B Punkt 3** aus P6 (Purge-Zeilenrückgang, frühestens 2026-08-28), sowie die
Auflage, `diagnose.sh` vor dem nächsten Deploy frisch zu fahren.

---

## §7 Ausdrücklich draußen

Thumbnails/Skalieren/EXIF-Strip (P6-BA) · SVG/HEIC (P6-AZ) · Video/Audio/PDF/beliebige Anhänge
(P5-AA bleibt zu — dies ist ein **Bild**-Schnitt) · Zwischenablage-/Drag-&-Drop-Einfügen von
Bildern (v2) · Deduplizierung gleicher Bilder über Items hinweg · Space-weiter Bild-Browser ·
Bildsuche jeder Art (Core Principle) · Body-Volltextsuche **in der Web-UI** (Q1 bleibt gelockt,
auch wenn N4 = ja) · Rechteverwaltung über MCP-Tools (P6-M) · Löschen von Items (F2) ·
Space-Admin-UI (P6-V; bleibt Phase 7, `app.html` unangetastet — N1) · semantische Suche/Embeddings
(Core Principle) · **§9 Mehrfachauswahl aus `phase6_shares/ITEM_MOVE_PLAN.md`** — ausführungsreif
geplant (P6-AK–AN), aber **P6-Scope**, nicht dieser hier; wenn der Nikinger sie mitnehmen will,
ist sie ein eigener Step ohne neuen Endpunkt und ohne neues MCP-Tool.

---

## §8 `[VERIFY]`-Register

| # | Zu prüfen | Status / warum unsicher |
|---|---|---|
| **V59** | `fastmcp>=3.4,<3.5` kann `ImageContent` aus einem Tool zurückgeben | ✅ **geschlossen, 2026-08-20, empirisch.** `fastmcp==3.4.4`; `fastmcp.utilities.types.Image(data=…, format="png")`; Tool mit Rückgabetyp `Image \| str` liefert je Zweig `ImageContent` bzw. `TextContent` (In-Process-`fastmcp.Client`-Lauf). |
| **V60** | claude.ai-Custom-Connectors **zeigen/verarbeiten** `ImageContent` | **offen** — Client-Verhalten, nicht Spec. Nur über eine echte Connector-Probe klärbar (Abnahmezeile P6.5-13). |
| **V61** | `os.replace` auf einem **Verzeichnis** ist auf `ext4` brauchbar | ✅ **geschlossen, 2026-08-20, empirisch.** `findmnt -T` bestätigt `ext4`; Verschieben eines Verzeichnisses gelingt, nicht-leeres Ziel ⇒ `OSError(39, 'Directory not empty')` ⇒ **P6.5-S**. |
| **V64** | Ob claude.ai aus `destructiveHint: True` eine **wiederholte** Zustimmung macht („nicht auf immer erlauben stellbar") | **offen, nicht zusagbar.** Client-seitig. Wenn nein, bleibt nur die Beschreibungspflicht (P6.5-O) — dann als Befund an den Nikinger melden, nicht stillschweigend hinnehmen. |
| **V65** | Reales ID-Format aus `files.generate_id()` (Annahme: 8 Hex, P1-Entscheidung F) | vor dem Schreiben der Regexe gegen den Code prüfen; Code gewinnt. |
| **V66** | `_require_csrf_json()` prüft ggf. auch den JSON-Content-Type und passt damit nicht auf einen Rohbytes-Upload | prüfen; falls ja, den **Herkunftsteil** herauslösen — **nicht** die Prüfung umgehen. |
| **V67** | `X-Content-Type-Options: nosniff` liegt auch auf `/api/v1/**`, nicht nur auf UI-Seiten | prüfen; falls nein, auf der Asset-Route explizit setzen. |
| ~~V68~~ | ~~`assets:`-Zeile in `get_item`s Dateitext~~ | **entfällt** — die Liste steht ausschließlich in `get_item_meta` (Step B4 Punkt 1, Roundtrip-/`patch_item`-Anker-Risiko), `get_item`s Rückgabe bleibt byte-identisch. |
| **V69** | `Image(format=…)`-MIME-Mapping für JPEG/WebP | sicherer Weg: `to_image_content(mime_type=mime)` explizit setzen. |
| **V70** | Alle Zeilennummern in diesem Dokument | Stand `main`@`2a4d8ca`, 2026-08-20. **Funktionsnamen sind die belastbaren Anker.** |
| — | MCP-Revision 2026-11-25 / FastMCP 4 | unverändert **Watch-Item** aus P2/P3 (Trigger = erstes `fastmcp`-Release mit Support), **kein** Scope dieser Phase. |

---

## §9 Kontext, der nicht zum Scope gehört (einzeilig mitgeführt)

- **>2 Nutzer:** am 2026-08-19 geprüft — Architektur trägt es, keine Stelle im Laufzeitcode ist
  auf zwei Principals hartkodiert (`phase6_shares/CLAUDE.md`). **Kein Plan nötig.**
- **§9 Mehrfachauswahl** (`ITEM_MOVE_PLAN.md`): geplant und gelockt (P6-AK–AN), nicht gebaut,
  P6-Scope. Nur Verweis, hier nicht neu geplant.
- **D6 / `Store.search()` liest jede Datei:** bekannter Kostenpunkt (P6-S), wächst mit der
  Item-, nicht der Nutzerzahl. Von N4 **nicht** verschlechtert (der Body ist bereits geladen).
- **Doku-Hygiene, Stand 2026-08-20:** kein Head über dem 40-KB-Softcap; alle neun Übergrößen sind
  📕/📦, wie die Regel es verlangt. **Aber:** `phase6_shares/CLAUDE.md` liegt bei **40 863 Bytes**
  — rund 100 Bytes unter dem Cap. Der nächste Session-Block dort braucht eine **Rotation**
  (`scripts/rotate_session_block.sh`), kein Anhängen.
