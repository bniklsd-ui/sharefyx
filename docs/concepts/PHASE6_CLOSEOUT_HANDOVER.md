---
status: snapshot
purpose: Abschluss-Handover P6→P7 — Status (ehrlich: code-complete, NICHT vollständig live-verifiziert), Delta seit dem P5-Handover, offene Entscheidungen, [VERIFY]-Bilanz V39–V58
read-when: Start der nächsten Planungssession, VOR dem Entwurf des Claude-Code-Plans — dann einmal ganz lesen
detail: L2
up: ../../phase6_shares/CLAUDE.md
down:
  - ./phase6_shares_plan.md                     # Entscheidungen P6-A–P6-AC, Steps 0–10 — Herkunft, nicht Ergebnis
  - ../../phase6_shares/ITEM_MOVE_PLAN.md       # Step 7b + §9 Mehrfachauswahl (P6-AD–AN), Abnahmezeilen 25–34
  - ../../phase6_shares/GLOBAL_SEARCH_PLAN.md   # „Alle Items"-Modus (P6-AO–AT), Abnahmezeilen 35–39
  - ../../phase6_shares/IMAGES_PLAN.md          # Block C, nachrangig — abgelöst durch phase6_5_tools_images_plan.md
  - ./PHASE5_CLOSEOUT_HANDOVER.md               # Vorgänger; V27–V38, Herkunft der P6-Entscheidungen
updated: 2026-08-23
---
# Phase 6 — Closeout-Handover (P6 → nächste Phase)

> **Für den kalten Leser, ohne Beschönigung.** Phase 6 ist **code-complete und live deployt**,
> aber **nicht vollständig live-verifiziert**. Von 39 im Laufe der Phase definierten
> Abnahmezeilen (§6 des Plans 1–24, plus 25–34 aus `ITEM_MOVE_PLAN.md`, plus 35–39 aus
> `GLOBAL_SEARCH_PLAN.md`) sind **12 live bestanden**, zwei faktisch erfüllt aber nie als
> Abnahmelauf protokolliert, vier durch spätere Entscheidungen gegenstandslos/verschoben, der
> Rest offen. Vier Zeilen (31–34) wurden **nie gebaut**. Die Zeilen 40–47 (Block C, Bilder) sind
> nach **Phase 6.5** ausgewandert und zählen hier nicht mehr mit.
>
> **Es gibt kein `P6_ABNAHME_<datum>.md`.** Für eine nur teilweise verifizierte Phase wäre ein
> Abnahmeprotokoll eine Falschaussage. Die konsolidierte Statustabelle in **§3 dieses Dokuments
> ist der Ersatz** — nicht nach einem fehlenden Protokoll suchen.
>
> **Phase 6.5 ist NICHT Teil dieses Abschlusses.** Sie läuft als eigene, aktive Phase weiter
> (`phase6_5_tools_images/`, Stand 2026-08-23: 10 von 14 Abnahmezeilen). Dieser Handover
> schließt ausschließlich Phase 6.
>
> **Dieses Dokument ist keine zweite Kopie der Pläne.** Code ist Wahrheit; die vier Plandateien
> sind Herkunft, der Phase-Head (`phase6_shares/CLAUDE.md`) ist der operative Einstieg.

---

## 1 Status in fünf Sätzen

1. **Das Rechtemodell steht und läuft live.** `SharePolicy`/`Surface` haben `OwnSpaceWritable`
   ersetzt, ACL-Entscheidungen kommen aus `.share.yml`-Dateien auf der Platte (`storage/acl.py`),
   Freigaben sind item-, ordner- und space-weise möglich, kein MCP-Tool kann sie setzen (P6-M).
2. **Hard Rule 4 wurde in dieser Phase bewusst neu gefasst** — Schreibrechte folgen der
   Mitgliedschaft, nicht dem Token; Cross-Space-Writes existieren jetzt, aber nur über Daten auf
   der Platte, nie über einen `if`-Zweig im Code.
3. **Der Seam-Beweis der Phasen 4/5 (leerer `git diff` auf `storage/`) ist aufgelöst** und durch
   Charakterisierungstests mit byte-verglichenen Golden Files ersetzt (P6-D) — die haben über
   fünf Storage-Umbauten hinweg gehalten.
4. **Alles ist deployt.** `main`@`f96125e` (2026-08-21, im Zuge des Phase-6.5-Deploys) trägt
   sämtlichen P6-Code inklusive der globalen Suche; `828 pytest` grün (Stand 2026-08-23, davon
   772 am Ende von P6 selbst).
5. **Was fehlt, fehlt am Menschen, nicht am Code** — mit drei Ausnahmen: §9 Mehrfachauswahl
   (nie gebaut), die Sichtbarkeits-Migration (nie gegen den echten `DATA_ROOT` gefahren) und
   der dritte Testnutzer (nie angelegt).

---

## 2 Delta seit dem P5-Handover

| Was | Wo im Code | Bemerkung |
|---|---|---|
| `patch_item` (siebtes MCP-Tool) + Quittungen statt Volltext an allen Schreib-Tools | `storage/patch.py`, `mcpserver/receipts.py`, `mcpserver/tools.py` | schließt §4.2 des P5-Handovers |
| O2 geschlossen: `purge_expired()` räumt `clients`/`token_families` | `authserver/store.py` | schließt §4.4 des P5-Handovers — **Live-Beleg fehlt** (Zeile 4) |
| Client-Surface-Logging (`ua`) | `mcpserver/asgi.py :: AccessLogASGI` | schließt §4.3, **mit negativem Befund** (V42) |
| Update-Log + Banner + `deploy.sh`-Gate | `webui/updates.py`, `docs/UPDATE_LOG.md`, Schema 3 | P6-X |
| ACL-Fundament | `storage/acl.py`, `models.py`/`files.py`/`index.py`/`store.py` | dritte Contract-Öffnung |
| Rechtepolitik | `mcpserver/permissions.py` (`SharePolicy`/`Surface`), `webui/api.py` | ersetzt `OwnSpaceWritable` |
| Verwaltung/Migration | `phase6_shares/scripts/{spacectl,migrate_visibility}.py`, `diagnose.sh` Prüfung 12 | schließt §4.1 (F1) |
| Echte Ordner, Sichtbarkeits-Chips, Verschieben, Drag & Drop, Freigabe-Dialog, Re-Auth-Gate | `webui/shares.py`, `webui/static/js/*` | `app.js` in zehn ES-Module gesplittet, weiterhin ohne Build-Step |
| `Store.move()` (Space+Ordner) | `storage/store.py` | vierte Contract-Öffnung |
| Globaler Suchmodus „Alle Items" | `webui/serializers.py`, `api.py`, `static/js/{state,tree,list}.js` | **kein neuer Endpunkt** — `GET /api/v1/items` ohne `space` war bereits global |

**Nicht geliefert gegenüber dem P5-Handover:** F2 (vollständiges Löschen) bleibt wie angekündigt
draußen — Items werden archiviert, nie gelöscht.

---

## 3 Abnahmestand — die Tabelle, die es sonst nirgends gibt

**Statusregel wie in P4/P5: ✅ heißt live-verifiziert durch einen Menschen, nicht „gebaut".**

### 3.1 Plan §6, Zeilen 1–24

| # | Kurzform | Stand | Beleg / Grund |
|---|---|---|---|
| 1 | `patch_item` ändert drei Stellen, ein Versionssprung, ein Commit | ✅ | Gate A→B Punkt 1, echter Connector |
| 2 | Mehrdeutiger `old_text` schlägt fehl, Datei unverändert | ✅ | Gate A→B Punkt 1 |
| 3 | Quittung statt Volltext, `return_body=True` liefert ihn | ✅ | Gate A→B Punkt 2 |
| 4 | Purge räumt `clients`/`token_families` real ab | **offen** | Gate A→B Punkt 3 — reine Kalenderfrage, frühestens **2026-08-28**; per Nikinger-Entscheidung nicht blockierend |
| 5 | `ua` unterscheidet zwei Claude-Oberflächen **oder** der Befund steht | ✅ | V42, negativer aber definitiver Befund: `ua` unterscheidet **nicht** — die Zeile lässt genau das zu |
| 6 | Update-Banner erscheint / verschwindet / wiederfindbar | ✅ | Gate A→B Punkt 4, beide Hälften (Niklas 2026-08-10, Fabian 2026-08-11) |
| 7 | `deploy.sh` bricht ohne aktuellen `UPDATE_LOG.md` ab | 🟡 | im Deploy vom 2026-08-14 faktisch erlebt (Datum stand auf gestern, Eintrag musste nachgezogen werden), aber nie als eigener Prüflauf protokolliert; Unit-Tests decken beide Richtungen |
| 8 | Migration gelaufen, jedes Item trägt `visibility`, Fabian sieht Niklas' Space nicht mehr | **offen, zweiteilig** | **Erster Teil messbar unerfüllt:** `migrate_visibility.py --apply` lief nie gegen den echten `DATA_ROOT` — Nachprüfung 2026-08-23: **0 von 73** `.md`-Dateien tragen ein `visibility:`-Feld. Funktional harmlos (fehlend ⇒ `private` beim Lesen), formal offen. **Zweiter Teil bewusst überstimmt:** beim Cutover 2026-08-13 wurden gegenseitige `read:`-Grants gesetzt, damit sich Niklas und Fabian weiterhin lesen — die Zeile beschreibt einen Zielzustand, den der Nikinger nicht wollte |
| 9 | Ordner anlegen, Item hineinziehen, Datei real im Unterverzeichnis | 🟡 | faktisch erfüllt (echter `DATA_ROOT` trägt `niklas/nvidia-avo-harness/` und `niklas/otobo/` mit realem Item darin, 2026-08-23 nachgeprüft), aber nie als Abnahmelauf protokolliert — insbesondere nicht der Drag-&-Drop-Weg |
| 10 | Ordner-Freigabe wirkt auf alle Items darin | **offen** | braucht Fabian |
| 11 | Einzelnes Item lesend freigegeben — Fabian sieht **nur** dieses | **offen** | braucht Fabians Login (identische Blockade wie Zeilen 36/37) |
| 12 | `share_write` am Item: Fabian ändert es, Nachbaritem nicht | **offen** | braucht Fabian |
| 13 | Geteilter Space: beide legen an und ändern gegenseitig | **offen** | braucht Fabian; `IT-Sekus-Projekt` existiert real mit beiden als `write:` |
| 14 | Fremder Body auch im geteilten Space `<untrusted_content>`-gewrappt | 🟡 | live bestätigt für den **fremden** Space `fabian` (2026-08-13, echter Connector). Der geteilte Space `IT-Sekus-Projekt` selbst wurde nicht gegengeprüft — derselbe Codepfad, aber nicht dieselbe Zeile |
| 15 | `visibility: human` in der UI sichtbar, über den Connector nirgends | **offen** | gebaut + unit-getestet (P6-P), nie live geprüft — und mangels gelaufener Migration existiert kein Item mit `visibility: human` |
| 16 | Freigabe erweitern verlangt Re-Auth, zurücknehmen nicht | **offen** | gebaut (`webui/shares.py :: widens()`), Playwright-geprüft, nie live |
| 17 | Kein MCP-Tool kann `share_*`/`visibility` setzen | **offen** | gebaut + unit-getestet, nie live über den Connector versucht |
| 18 | Dritter Nutzer: Konto, Space, Connector, Schreibvorgang | **offen** | **nie angelegt** — der echte `DATA_ROOT` trägt genau `niklas`, `fabian`, `IT-Sekus-Projekt` |
| 19–22 | Bilder (Drag & Drop, nur Link über Connector, HEIC-Ablehnung, 404 ohne Recht) | **verschoben** | Block C ist nach **Phase 6.5** ausgewandert; die Nachfolgezeilen P6.5-5/6/9/11 sind dort teils bereits ✅ |
| 23 | Reboot: UI, Connector, Timer kommen ohne Handgriff zurück | ❌ **live widerlegt** | Reboot vom 2026-08-19: Dienst/`/health`/`funnel status` sahen gesund aus, von außen `NS_ERROR_CONNECTION_REFUSED`; `sudo systemctl restart tailscaled` behob es. `diagnose.sh` Prüfung 5 ist korrigiert, ein Watchdog ist **bewusst offene Entscheidung**. Eigentum: `phase3_edge/CLAUDE.md` |
| 24 | Dritter Space entfernt, `diagnose.sh` meldet keine verwaisten Freigaben | **gegenstandslos, solange 18 offen ist** | `spacectl.py check` + `diagnose.sh` Prüfung 12 sind gebaut und getestet |

### 3.2 `ITEM_MOVE_PLAN.md`, Zeilen 25–34

| # | Kurzform | Stand | Beleg / Grund |
|---|---|---|---|
| 25 | Grauer Text nach dem Deploy lesbar, Platzhalter erkennbar | **offen** | deployt am 2026-08-14; die Bewertung „lesbar" ist Nikingers eigene, nie protokolliert |
| 26 | Item über die UI nach `IT-Sekus-Projekt` verschoben, ein `move`-Commit | 🟡 **faktisch erfüllt** | genau das ist am **2026-08-23** passiert — der Nikinger hat den Move in seinem eigenen Browser mit TOTP ausgeführt, `5d06187 move itm_de2e4fd8 [IT-Sekus-Projekt]` steht in der echten `DATA_ROOT`-Historie. Protokolliert wurde er als **P6.5-10**, nie als P6-Zeile 26 abgehakt |
| 27 | Fabian sieht das verschobene Item und kann es ändern | **offen** | braucht Fabian (mechanisch gegen eine Wegwerf-Instanz bestätigt) |
| 28 | Item mit `share_write` ohne space-level Grant lässt sich von Fabian nicht wegverschieben | **offen** | braucht Fabian |
| 29 | Move zwischen zwei Spaces über den **Connector** | **offen** | der 26er-Move lief über die UI, nicht über MCP |
| 30 | Leergewordener Ordner verschwindet aus dem Baum | **offen** | mechanisch bestätigt (Wegwerf-Instanz), nicht live |
| 31–34 | Mehrfachauswahl (N Items auf einmal, ein Re-Auth-Formular, Teilfehler, kein Re-Auth in-space) | ❌ **nie gebaut** | Plan `ITEM_MOVE_PLAN.md` §9, Entscheidungen **P6-AK–P6-AN**, vom Nikinger gelockt und ausführungsreif. Größter offener Bauposten der Phase — siehe §5.1 |

### 3.3 `GLOBAL_SEARCH_PLAN.md`, Zeilen 35–39

| # | Kurzform | Stand | Beleg / Grund |
|---|---|---|---|
| 35 | „Alle Items" im Baum sichtbar und aktivierbar, Rückweg funktioniert | ✅ | 2026-08-23, echter `claude-in-chrome`-Connector |
| 36 | Empfänger mit **ausschließlich** item-level Share findet das Item | **offen** | mit `niklas` **strukturell nicht erzeugbar** — `niklas` steht in `fabian/.share.yml` unter `read:`, also ist dort ohnehin jedes Item über die Space-Mitgliedschaft sichtbar. Braucht Fabians eigenen Login oder ein drittes, isoliertes Setup |
| 37 | derselbe Empfänger sieht **nur** dieses eine Item | **offen** | identische Blockade wie 36 |
| 38 | Notizen und Aufgaben gemeinsam gelistet | ✅ | 2026-08-23, echter Connector |
| 39 | Kein Anlegen-Knopf im globalen Modus | ✅ | 2026-08-23 — beide `Anlegen`-Buttons nachweislich hinter `[hidden]`-Vorfahren |

### 3.4 `IMAGES_PLAN.md`, Zeilen 40–47

**Vollständig abgelöst.** `docs/concepts/phase6_5_tools_images_plan.md` ist seit 2026-08-20 die
maßgebliche Quelle; die Nachfolgezeilen heißen dort **P6.5-1–P6.5-14** mit eigener Zählung.
`IMAGES_PLAN.md` bleibt als Herkunftsnachweis der Bauart-Vorgabe stehen und wird nicht
weitergepflegt.

---

## 4 Zwei Aufgaben, die der Nikinger ausdrücklich für die nächste Phase benannt hat

Beides ist am 2026-08-23 gefunden und bewusst **nicht** in derselben Sitzung behoben worden.
Beides ist als konkreter Einstiegspunkt gedacht, nicht als Stimmungsbild.

### 4.1 Doku-Audit fällig — Modul-Status-Zeilen 8–16 in `phase6_shares/CLAUDE.md`

Die Modul-Tabelle des Phase-Heads trägt in den Zeilen **8–16** (Step 7a und Step 7, Commits 0–6)
durchgehend `✅ gebaut, noch nicht deployt` bzw. `gebaut, Deploy beim Nikinger`. Dazu **Punkt 2
der Vormerkungen** („Step 7b … Noch nicht deployt").

**Der Verdacht ist begründet, aber ungeprüft.** Am 2026-08-23 stellte sich exakt dieselbe Aussage
für die globale Suche als stale heraus: `d348e2e` ist per `git merge-base --is-ancestor`
nachweislich Vorfahre von `main`@`f96125e`, dem laufenden Live-Deploy. Im Live-Browser derselben
Sitzung waren außerdem Verschieben-Dialog, Freigeben-Knopf, Sichtbarkeits-Chips und der echte
Ordnerbaum sichtbar — alles Artefakte genau dieser Commits.

**Auftrag für die nächste Phase:** je Commit `git merge-base --is-ancestor <sha> f96125e` fahren
(bzw. gegen den dann aktuellen Live-SHA) und die Tabellenzeilen im selben Commit korrigieren.
**Nicht raten, nicht pauschal auf „deployt" setzen** — der Wert dieses Audits ist der Nachweis,
nicht die Behauptung.

### 4.2 Werkzeug-Lücke: kein Entfernen-Knopf für Bilder in `editor.js`

`phase5_ui/webui/static/js/editor.js` hat **keine** Bedienfläche zum Entfernen eines Bildes —
`grep` auf `trash|entfern|delete.*asset` liefert null Treffer. Das steht im Widerspruch zur
gelockten Entscheidung **N5** („Verschieben statt Entfernen", nicht „gar nicht"), und der
Server-Endpunkt existiert bereits:

- `storage/store.py :: delete_asset()`
- `DELETE /api/v1/items/{item_id}/assets/{asset_id}` — `phase5_ui/webui/api.py:703, 756–760`

**Blockiert Abnahmezeile P6.5-12** (Phase 6.5, nicht Phase 6 — hier nur als angrenzender Kontext
genannt, zählt in §3 nicht mit). Nikinger-Entscheidung vom 2026-08-23: vorerst nur vermerken.

---

## 5 Offene Entscheidungen für die nächste Planung

### 5.1 §9 Mehrfachauswahl — geplant, gelockt, nie gebaut

Der größte offene Bauposten der Phase. `phase6_shares/ITEM_MOVE_PLAN.md` **§9**, Entscheidungen
**P6-AK–P6-AN**, Abnahmezeilen **31–34**. Ausführungsreif und per Nikinger-Freigabe gelockt: kein
neuer Endpunkt, kein neues MCP-Tool, und In-Space-Mehrfachauswahl braucht keine neue
Rechteprüfung (P6-AN). **Entscheidung nötig:** eigener kleiner Schnitt, Anhang an Phase 6.5 oder
Scope einer neuen Phase.

### 5.2 Der Phasenstatus selbst — ✅ oder 🟡?

`ROADMAP.md` und Root-`CLAUDE.md` stehen bewusst **nicht** auf ✅. Die eigene Statusregel des
Projekts („✅ heißt live-verifiziert") gibt das bei 12 bestandenen von 39 Zeilen nicht her; die
Roadmap-Legende hat für genau diesen Zustand das Glyph **🟡 code-complete, nicht live-bewiesen**.
Der Abschluss-Commit setzt P6 deshalb auf 🟡. **Der Sprung auf ✅ ist eine Nikinger-Entscheidung**
und hängt daran, ob die verbleibenden Zeilen noch geholt oder bewusst abgeschrieben werden.

### 5.3 Fabian-Blockade — vier Zeilen, eine Ursache

Die Zeilen 10–13, 27, 28 und 36/37 hängen alle an genau einem fehlenden Ding: **einer Sitzung mit
Fabians eigenem Login**. 36/37 zusätzlich daran, dass `niklas` einen space-level `read:`-Grant in
`fabian/.share.yml` besitzt und damit den Testfall „nur item-level Share" nicht darstellen kann.
**Entscheidung nötig:** gemeinsame Sitzung ansetzen, oder ein drittes isoliertes Principal
anlegen (dann fällt Zeile 18 mit ab).

### 5.4 Sichtbarkeits-Migration — nachholen oder abschreiben?

`migrate_visibility.py --apply` lief nie gegen den echten `DATA_ROOT` (0 von 73 Dateien tragen
`visibility:`). Funktional folgenlos, weil fehlende Werte beim Lesen zu `private` auflösen.
**Entscheidung nötig:** Lauf nachholen (macht Zeile 8s ersten Teil wahr, erzeugt 73 Commits in
der echten Historie) oder „fehlend ⇒ private" ausdrücklich als Zielzustand festschreiben und
Zeile 8 streichen.

### 5.5 Funnel-Watchdog — Zeile 23 ist live widerlegt

Der Reboot-Fund vom 2026-08-19 (`phase3_edge/CLAUDE.md`) ist bis heute nur diagnostisch
adressiert: `diagnose.sh` Prüfung 5 erkennt den Zustand jetzt, heilt ihn aber nicht.
**Selbstheilung/Watchdog ist bewusst offene Entscheidung, kein Auftrag.** Vor jedem Deploy
`diagnose.sh` frisch fahren, nicht auf „Reboot war schon mal ok" vertrauen.

### 5.6 P1-Contract bleibt bewusst offen — Abweichung von Plan §4 Step 10

Plan §4 Step 10 verlangt, die Contract-Öffnung in `phase1_storage/CLAUDE.md` zum Phasenende
wieder zu schließen. **Das wird hier bewusst nicht getan.** Die dritte (P6 Step 4) und vierte
(Step 7b, `Store.move()`) Öffnung gehören zwar P6 — die **fünfte gehört Phase 6.5** und ist
aktiv: 6.5 arbeitet weiterhin in `storage/{files,store,models}.py`. Ein Schließen jetzt wäre
eine Falschaussage. Der Plan wurde geschrieben, bevor Phase 6.5 existierte; das ist Plan-Drift,
kein Versäumnis. **Schließen, wenn 6.5 abschließt.**

### 5.7 Kleine Befunde, an die nächste Phase vererbt

| # | Befund | Fundstelle |
|---|---|---|
| **O4** | Verwaiste Assets bleiben liegen (kein Asset-Löschen in P6) | Plan §0.5 P6-AA — teilweise durch 6.5s `_trash/`-Weg adressiert, siehe §4.2 |
| **O5** | Kein EXIF-Strippen | Plan §0.5 P6-Z |
| **O6** | Unbekannte `update()`-Schlüssel landen still im Frontmatter (`spce="fabian"` erzeugt ein Feld statt eines Fehlers) | `ITEM_MOVE_PLAN.md` §112 — **weiterhin offen**, keine Feld-Whitelist |
| **O7** | Leere Ordner überleben einen Move (Geisterordner im Baum) | `ITEM_MOVE_PLAN.md` §118 — P6-AF räumt sie beim Move, Zeile 30 nie live geprüft |
| — | `PATCH /api/v1/items/{id}` hat **keine Feld-Whitelist** — dieselbe Wurzel wie O6, in Step 7 Commit 2 benannt | `webui/api.py :: _items_patch` |
| — | Verschieben-/Freigeben-Knopf nur für Items im eigenen Space sichtbar — kein UI-Rückweg aus einem geteilten Space | `list.js`, als „kein Bug, nicht blockierend" eingestuft |
| — | Body-Volltextsuche in der Web-UI bleibt draußen (Q1 gelockt) — in 6.5 nur als **MCP**-Opt-in `in_body=` geöffnet | `GLOBAL_SEARCH_PLAN.md` §1.1 |

---

## 6 `[VERIFY]`-Bilanz

### 6.1 Aus dem Hauptplan (§7, V39–V51)

| # | Stand |
|---|---|
| V39 | **geschlossen** — reale `pytest`-Ausgangszahl in Step 0 gemessen (nicht die behaupteten 576) |
| V40 | **geschlossen** — installierte Starlette in Step 0 geprüft |
| V41 | **geschlossen** — Connector-Doku gegengelesen; sechs → sieben Tools unauffällig |
| V42 | **geschlossen, negativ** (2026-08-12) — reale MCP-Clients setzen den `User-Agent` **nicht** unterscheidbar; `ua` trennt keine Claude-Oberflächen. Definitiver Befund, kein Nachholpunkt |
| V43 | **geschlossen mit Abweichung** — `webui/reauth.py` existiert nicht; gebaut wurde `webui/shares.py :: require_share_reauth()`, dessen Signatur die Plan-Skizze (§1.2.5) nicht abdeckte (echte Credential-Prüfung) |
| V44 | **geschlossen** — Schema 3 additiv per `ALTER TABLE`, wie P5 es gemacht hat |
| V45 | **geschlossen** — `deploy.sh`-Hook liegt direkt nach `release_sha`, vor venv/pip/pytest |
| V46 | **geschlossen** — `INDEX_SCHEMA_VERSION = 2` über `PRAGMA user_version`, Verwerfen-und-Neubauen bei Abweichung |
| V47 | **geschlossen** — `_archive/`, `_assets/`, `.share.yml` werden vom Rebuild korrekt nicht als Items gelesen (`RESERVED_DIR_NAMES`) |
| V48 | **geschlossen** — `fastmcp` 3.4.4 rendert `list[TypedDict]` zu brauchbarem JSON-Schema, kein Fallback nötig |
| V49 | **offen, vererbt** — Uplink-Datenlimit **mit** Assets. Gehörte zu Step 8/Block C, der nach Phase 6.5 gewandert ist; dort ebenfalls nicht bewertet |
| V50 | **geschlossen** — `<script type="module">` läuft unter CSP `script-src 'self'` ohne Header-Änderung |
| V51 | **geschlossen** — PyYAML ist bereits Dependency (`frontmatter.py` nutzt es), kein zweiter Parser |

### 6.2 Aus den Zusatzplänen

| # | Stand |
|---|---|
| V52 | **geschlossen** (2026-08-17) — `require_share_reauth()` wirft `ApiError("reauth_required", …)`, Plan-Annahme hält |
| V53 | **geschlossen** (2026-08-17) — `niklas`/`fabian`/`IT-Sekus-Projekt` liegen auf demselben Dateisystem (`stat -c %d` → `2050`), `os.replace()` bleibt ein echtes Rename |
| V54 | **geschlossen, anders als erwartet** — `/api/v1/overview` trägt kein `folders`-Feld und braucht keines; `/api/v1/spaces` liefert es bereits |
| V55 | **geschlossen** — `search(folder=…)` ist exakter Gleichheitsvergleich, für einen zweistufigen Baum ausreichend |
| V56 | **kein Prüfmarker im üblichen Sinn** — steht in `GLOBAL_SEARCH_PLAN.md` als Dauerwarnung: alle Zeilennummern dort sind Stand `main`@`2b155ce`, die **Funktionsnamen** sind die belastbaren Anker |
| V57 | **geschlossen** (2026-08-19) — kein fälschlich sichtbarer „nur lesen"-Hinweis im globalen Modus |
| V58 | **geschlossen** (2026-08-19) — kein Render-Pfad dereferenziert `spaceByName()` für eine Zeile aus einem nicht gelisteten Space |
| V59–V62 | **nach Phase 6.5 übernommen** (dort V59–V70). V59/V61 in deren Planungssession empirisch geschlossen, V60 mit dem Live-Deploy 2026-08-21, V64 unverändert offen. Kein Duplikat hier |

### 6.3 Geerbt

**V12** (Uplink-Datenlimit ohne Assets) geht laut Plan in V49 auf und ist damit **weiterhin
offen** — seit Phase 3 unbeantwortet.

---

## 7 Was die nächste Planungssession als Erstes tun sollte

1. **`phase6_shares/CLAUDE.md` lesen**, Modul-Tabelle plus neuesten Session-Block — dann sofort
   das Doku-Audit aus §4.1 fahren, bevor irgendetwas anderes geplant wird. Eine Planung auf
   stale Deploy-Aussagen ist eine Planung auf Sand.
2. **Entscheiden, ob §9 Mehrfachauswahl gebaut wird** (§5.1) — das ist der einzige gelockte,
   ausführungsreife Plan ohne Code.
3. **Entscheiden, ob eine Fabian-Sitzung angesetzt wird** (§5.3) — sie löst sieben Abnahmezeilen
   auf einen Schlag und ist der einzige Weg dorthin.
4. **Phase 6.5 zuerst abschließen lassen**, bevor der P1-Contract angefasst wird (§5.6).
5. **Nicht vergessen:** vor jedem Deploy `diagnose.sh` frisch fahren (§5.5), und `docs/
   UPDATE_LOG.md` braucht einen auf den Deploy-Tag datierten obersten Eintrag, sonst bricht
   `deploy.sh` ab (P6-X).
