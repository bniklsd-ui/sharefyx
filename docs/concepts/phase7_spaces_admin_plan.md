---
status: snapshot
purpose: Ausführungsreifer P7-Plan — Space-Verwaltung in der Weboberfläche, Mehrfachauswahl, Konsolidierung; Entscheidungen P7-A–P7-V, Steps 0/A/C/B/Z, Abnahmezeilen P7-1–P7-24, [VERIFY] V71–V79
read-when: Arbeiten an Phase 7 — einmal ganz lesen, bevor die erste Zeile Code entsteht; danach je Step der zugehörige §4-Abschnitt
detail: L2
up: ../../ROADMAP.md
down:
  - ./PHASE6_CLOSEOUT_HANDOVER.md               # Herkunft: Status P6, §4.1/§4.2, offene Entscheidungen §5.1–§5.7
  - ../../phase6_shares/ITEM_MOVE_PLAN.md       # §9 Mehrfachauswahl (P6-AK–AN) — Block B baut das, unverändert
  - ../../phase6_shares/CLAUDE.md               # Modul-Tabelle Zeilen 8–16 (Doku-Audit, Step 0)
  - ./phase6_5_tools_images_plan.md             # Phase 6.5 — wird von P7 mit abgeschlossen (Block A, A8)
# Der Phase-Head `phase7_spaces_admin/CLAUDE.md` entsteht erst in Step 0.6 und wird dort in
# dieses `down:` nachgetragen — ein Link auf eine noch nicht existierende Datei würde die
# Linkprüfung aus Step 0.3 zu Recht rot färben.
updated: 2026-08-23 (Browser-Planungssession, Opus; alle zehn Nikinger-Fragen N1–N10 beantwortet und in §0.1 gelockt; Anker gegen main@f5691e0 und den Live-Stand /opt/sharefyx/current = f96125e verifiziert)
---
# Phase 7 — Space-Verwaltung, Mehrfachauswahl, Konsolidierung

> **Ausführungsreifer Plan für Claude Code (Sonnet 5).** Er ist so geschrieben, dass nichts
> davon neu hergeleitet werden muss: gelockte Entscheidungen, Schritt-Sequenz, exakte Funktions-
> und Typnamen, `Datei:Zeile`-Anker, Testliste, Abnahmekriterien.
>
> **Alle Zeilennummern sind Stand `main`@`f5691e0` (2026-08-23).** Die **Funktionsnamen** sind
> die belastbaren Anker, die Nummern die Bequemlichkeit. Weicht eine Nummer ab: Name suchen,
> Nummer ignorieren, keinen Fund daraus machen.
>
> **Quelle der Wahrheit ist der Code, nicht dieser Plan.** Bei Widerspruch gewinnt das getestete
> Artefakt; der Plan bleibt als 📕-Snapshot unverändert, die Korrektur wird datiert im Phase-Head
> vermerkt — dieselbe Disziplin wie in P4/P5/P6/6.5.

---

## §0 Bottom line

Phase 7 hat **drei Blöcke und ein Aufräumkapitel davor**:

| Block | Inhalt | Fällt unter Druck |
|---|---|---|
| **Step 0** | Haushalt, Verifikationsdurchlauf, Doku-Audit aus dem P6-Handover §4.1 | nie |
| **Block A** | Fixes aus Handover und Notizen + formaler Abschluss von Phase 6.5 | **nie** |
| **Block C** | Space-Verwaltung in der Weboberfläche (die reservierte Phase-7-Fläche) | als zweites |
| **Block B** | Mehrfachauswahl (`ITEM_MOVE_PLAN.md` §9, gelockt, nie gebaut) | **als erstes** |

**Reihenfolge: 0 → A → Gate → C → B.** Das ist bewusst nicht die Buchstabenfolge. Block C trägt
den Namen dieser Phase (Space-Admin-UI war seit P6 Step 7 Commit 6 für „Phase 7" reserviert und
steht so in `app.html`); Block B ist ein fertig geplanter Komfort-Schnitt, der ohne Schaden in
eine spätere Phase rutschen kann. Wer unter Token-Druck kürzen muss, kürzt B, nie C, niemals A.

**Was diese Phase beweisen soll, in einem Satz je Block:**

- **A:** Ein Mensch findet ein Item wieder, das eine Claude-Instanz ihm gegenüber `itm_807df219`
  genannt hat — und kann ein Bild wieder loswerden, das er eingefügt hat.
- **C:** Ein Mensch entscheidet im Browser, wer seinen Space lesen darf, legt einen geteilten
  Space an und wird einen wieder los, **ohne dass dabei ein Item verloren geht**.
- **B:** Zehn Items wandern in einem Vorgang in denselben Zielordner, mit **einem**
  Re-Auth-Formular statt zehn.

---

## §0.1 Was der Nikinger in dieser Planungssession entschieden hat (N1–N10, gelockt)

Diese zehn Antworten sind **Vorgabe, keine Ableitung**. Sie stehen über jeder gegenteiligen
Empfehlung weiter unten in diesem Dokument und über jeder Empfehlung der Vorphase.

| # | Frage | Antwort (gelockt 2026-08-23) |
|---|---|---|
| **N1** | Phase-7-Zuschnitt | **Fixes + Space-Admin-UI bauen.** P7 behält seinen reservierten Inhalt und baut ihn. `app.html`s „kommt in Phase 7" wird zur echten Bedienfläche, nicht zu „kommt in Phase 8". |
| **N2** | §9 Mehrfachauswahl | **In P7 bauen.** `ITEM_MOVE_PLAN.md` §9 unverändert ausführen (P6-AK–AN sind gelockt). |
| **N3** | Phase 6.5 | **P7 schließt sie mit ab.** P6.5-12 wird P7-Arbeit; 6.5 bekommt Handover + Übersichtsgrafik; danach ist genau eine Phase aktiv. |
| **N4** | Sichtbarkeits-Migration | **Lauf nachholen.** `migrate_visibility.py --apply` gegen den echten `DATA_ROOT`, 73 Commits werden bewusst in Kauf genommen. |
| **N5** | Umfang der Space-Verwaltung | **Volle `spacectl.py`-Parität in der Weboberfläche** — anlegen, Mitglieder verwalten, entfernen. |
| **N6** | Home-Spaces | **Von Anlegen und Entfernen ausgeschlossen, Mitgliederverwaltung ausdrücklich drin.** „Wer darf meinen Space lesen" ist der Alltagsnutzen, der die Fläche rechtfertigt. |
| **N7** | Wer darf verwalten | **Jedes `write:`-Mitglied.** Kein neues `owner:`-Feld, keine Migration. Die Selbstaussperrung wird bewusst in Kauf genommen (§0.4). |
| **N8** | Space entfernen | **Items zuerst in den Home-Space des Ausführenden verschieben und dort archivieren, danach `rmtree`.** Die Space-Zuordnung ist das Einzige, was unwiderruflich verlorengeht. |
| **N9** | Teilfehler beim Entfernen | **Vorher prüfen, bei jedem Hindernis gar nicht anfangen.** Kein halb entfernter Space. |
| **N10** | Abnahme-Blockade | **Dritter Testnutzer holt alles Mechanische, Fabian-Sitzung bleibt vollständig optional.** Der Nutzer heißt eindeutig **`testnutzer-p7`**. |

---

## §0.2 Scope

**DRIN:**

- Item-ID in der Weboberfläche sichtbar und **per ID auffindbar** (Fabian-Meldung 2026-08-23).
- Entfernen-Knopf für Bilder im Editor (schließt die Werkzeug-Lücke P6.5-12, Handover §4.2).
- Feld-Whitelist an `PATCH /api/v1/items/{id}` (Wurzel von Befund **O6**).
- Doku-Audit der Modul-Status-Zeilen 8–16 in `phase6_shares/CLAUDE.md` (Handover §4.1).
- Sichtbarkeits-Migration live (Handover §5.4, N4).
- Dritter Principal `testnutzer-p7` — angelegt, benutzt, wieder entfernt (schließt P6-W), samt
  `testcred.py` für einen Keyring-gestützten Zugang, den Claude Code ohne Nikinger benutzen kann.
- Formaler Abschluss von Phase 6.5 inkl. Schließen des P1-Contracts (Handover §5.6).
- **Space-Verwaltung in der Weboberfläche** — Mitglieder, Anlegen, Entfernen (N5/N6/N7/N8/N9).
- **Mehrfachauswahl** nach `ITEM_MOVE_PLAN.md` §9 (N2).

**DRAUSSEN — und zwar bewusst:**

- **FastMCP-4-Umstieg / MCP-Revision `2026-07-28`.** Seit **P5-C** gelockt als eigene Mini-Phase.
  Die Spec ist am 2026-07-28 erschienen (statuslos, `initialize`-Handshake und `Mcp-Session-Id`
  entfallen, Roots/Sampling/Logging deprecated) und `fastmcp 4` unterstützt sie; installiert sind
  `fastmcp 3.4.4` / `mcp 1.28.1`, und der echte Connector hat am 2026-08-23 nachweislich
  funktioniert. **Kein Migrationsschritt in P7**, kein Beobachtungsfeld in `AccessLogASGI`
  (`mcpserver/asgi.py` bleibt tabu, P6-C). Steht als `[VERIFY]` **V79** im Register, mehr nicht.
- **`owner:`-Feld in `.share.yml`** (N7 schließt es aus).
- **Löschen von Items.** F2 bleibt draußen, wie seit P5 — `status: archived`, nie `unlink`.
- **Rechteverwaltung über MCP-Tools.** P6-M gilt unverändert: kein Tool setzt `share_*` oder
  `visibility`. Die neue Verwaltungsfläche ist eine **Menschen**-Fläche.
- **Automatische `_trash/`-Räumung** (Vormerkung aus 6.5, unverändert offen).
- **Funnel-Watchdog / Selbstheilung.** Handover §5.5 nennt das ausdrücklich als offene
  Entscheidung, nicht als Auftrag. P7 fährt stattdessen vor jedem Deploy `diagnose.sh` frisch.
- **Body-Volltextsuche in der Web-UI** (Q1 aus `GLOBAL_SEARCH_PLAN.md` bleibt gelockt).
- **Mehrfachauswahl für andere Aktionen als Verschieben** (§9.6 des Zusatzplans).

---

## §0.3 Berührungsfläche und Tabu (P7-B)

**Auf:** `phase1_storage/storage/` · `phase5_ui/webui/` · `phase2_mcp/mcpserver/tools.py` ·
`phase6_shares/scripts/spacectl.py` · `phase3_edge/scripts/diagnose.sh` · `docs/`

**Tabu, `git diff` darauf bleibt leer:**
`phase2_mcp/mcpserver/asgi.py` · `phase2_mcp/mcpserver/{server,permissions}.py` ·
`phase4_auth/authserver/{crypto,totp,passwords,resolver,flows}.py`

`mcpserver/app.py` darf angefasst werden, **wenn** eine Signatur nachgezogen werden muss (wie in
P5 Step 8 und P6 Step 5); jede solche Änderung wird im Session-Block benannt, nicht stillschweigend
gemacht.

**P6-D gilt unverändert weiter:** Charakterisierungstests
(`phase6_shares/tests/test_characterization.py`, drei Golden Files) laufen **vor und nach** jedem
Umbau an `storage/` und müssen byte-identisch grün sein. Kein Step-Abschluss ohne das.

---

## §0.4 Zwei bewusst akzeptierte Konsequenzen, benannt statt versteckt

1. **Selbstaussperrung ist möglich (Folge aus N7).** Jedes `write:`-Mitglied darf die
   Mitgliederliste ändern — also auch das letzte `write:`-Mitglied sich selbst entfernen. Der
   Space ist danach über die Weboberfläche für niemanden mehr verwaltbar. **Dokumentierter
   Rückweg: `spacectl.py add-member <space> <user> --write` im Terminal.** Es wird **kein** Guard
   dagegen gebaut — der Nikinger hat die Regel in Kenntnis dieser Kehrseite gewählt, und jede
   Änderung steht als Commit in der Git-Historie des `DATA_ROOT`.
2. **Beim Entfernen eines Space geht die Space-Zuordnung verloren (Folge aus N8).** Die Items
   selbst überleben — im `_archive/` des Ausführenden. Was mit dem `rmtree` stirbt: der Inhalt von
   `<space>/_assets/<item_id>/_trash/` (bereits entfernte Bilder) und ein etwaiges
   `<space>/_assets/`-Verzeichnis zu Items, die es nicht mehr gibt. Beides ist per Definition
   Müll; die Git-Historie des `DATA_ROOT` behält es ohnehin.

---

## §1 Gelockte Entscheidungen (P7-A – P7-V)

| # | Entscheidung | Begründung |
|---|---|---|
| **P7-A** | **Drei Blöcke, Fall-Reihenfolge A > C > B, hartes Gate nach A.** | A schließt gemeldete Fehler und die Vorphase ab — auf einer Phase mit offenen Vorgängerfäden zu bauen ist die Lage, die P6 auf 🟡 gebracht hat. C trägt den Namen der Phase, B ist Komfort. |
| **P7-B** | **Berührungsfläche wie §0.3**, `mcpserver/asgi.py` und die fünf `authserver/`-Krypto-Module bleiben tabu. | Fortschreibung von P6-C. Eine Verwaltungsfläche für Freigaben ist kein Grund, an der Auth-Krypto zu rühren. |
| **P7-C** | **Charakterisierung (P6-D) vor und nach jedem `storage/`-Umbau.** | Der Seam-Beweis der Phasen 4/5 existiert nicht mehr; das ist sein Ersatz und hat über fünf Umbauten gehalten. |
| **P7-D** | **Die ID-Suche lebt an der API-Fläche (`webui/api.py :: _items_get`), NICHT in `store.search()`.** `store.py:421`s Haystack bleibt `title + tags` (+ `body` bei `in_body=True`). | Ein zusätzlicher Haystack-Term ändert das Verhalten **jedes** MCP-Aufrufers still mit. Der Bedarf ist ein Menschen-Bedarf: Claude adressiert Items längst direkt über `get_item`. Kein Contract-Ausschlag für ein UI-Problem. |
| **P7-E** | **Die ID-Suche ignoriert `space`- und `folder`-Filter und sucht immer global** über alles, was der Anfragende lesen darf. | Wer eine ID in der Hand hat, weiß gerade **nicht**, wo das Item liegt — das ist der ganze Fall. Ein ID-Treffer, der am aktiven Ordnerfilter scheitert, löst Fabians Problem nicht. |
| **P7-F** | **Zusätzlich zur Anzeige: die Tool-Beschreibungen weisen Claude an, Menschen gegenüber den Titel zu nennen.** Die ID bleibt die interne Adresse. | Anzeige behandelt das Symptom, die Beschreibung die Ursache. Beide sind billig, orthogonal und schließen sich nicht aus — dieselbe Kategorie wie Block A von Phase 6.5. |
| **P7-G** | **Die Feld-Whitelist kommt an `_items_patch`, nicht in `store.update()`.** `store.py:512–513` (`else: updated_extra[key] = value`) bleibt unverändert. | Genau dieser `else`-Zweig **ist** die Round-Trip-Treue aus P1 (unbekannte Frontmatter-Felder überleben; Abnahmezeile 13 der Phase 5 hängt daran). Der Tippfehler kommt über die HTTP-Fläche herein, dort gehört der Riegel hin. `mcpserver/tools.py :: update_item` ist durch seine typisierte Signatur bereits dicht. |
| **P7-H** | **Die Migration fährt der Nikinger, nicht Claude Code.** Claude Code bereitet das Kommando vor und prüft danach read-only nach. | Harte Projektregel seit P1: kein Test/Schreibvorgang gegen den echten `DATA_ROOT` durch Claude Code. Eine Migration mit 73 Commits ist der Extremfall davon, nicht die Ausnahme. |
| **P7-I** | **Phase 6.5 wird in Block A formal abgeschlossen** (Handover + Übersichtsgrafik + ROADMAP/Root-Status), **danach** wird der P1-Contract geschlossen — und im selben Atemzug die **sechste** Öffnung für P7 benannt. | Handover §5.6 hat das Schließen bewusst aufgeschoben, weil 6.5 noch in `storage/` arbeitete. P7 arbeitet dort erneut; ein Schließen ohne sofortige Neuöffnung wäre wieder eine Falschaussage. |
| **P7-J** | **Der dritte Principal heißt `testnutzer-p7`**, wird angelegt, für die Abnahme benutzt und am Ende von Block A wieder entfernt. | N10 („benenne ihn eindeutig"). Der Name kann mit keinem Menschen verwechselt werden und trägt seine Phase im Namen. Erfüllt zugleich P6-W (Abnahmezeilen 18/24, nie passiert). |
| **P7-K** | **Volle `spacectl.py`-Parität in der Weboberfläche, Home-Spaces von Anlegen und Entfernen ausgenommen, Mitgliederverwaltung für alle Spaces inklusive des eigenen Home-Space.** | N5/N6. Ein Home-Space entsteht über eine Einladung, nicht über einen Knopf; ihn zu entfernen hieße, einen Menschen zu löschen. Seine Leserechte zu ändern ist dagegen die häufigste Frage überhaupt. |
| **P7-L** | **Verwalten darf, wer im Ziel-Space `write:` hat** (`SharePolicy.can_write(session.space, space)`). Kein `owner:`-Feld, keine Migration. | N7. Folgt exakt der bestehenden Rechtelogik; die Kehrseite steht in §0.4 Punkt 1. |
| **P7-M** | **Kein Aufrufer hält den `.write.lock` und ruft darin eine `Store`-Methode auf.** Die neuen `.share.yml`-Schreibfunktionen nehmen den Lock **selbst**, für eine kurze kritische Sektion. Die Orchestrierung in `webui` nimmt ihn **nie**. | **Empirisch belegt in der Planungssession:** zwei `open()` auf dieselbe Datei im selben Prozess erzeugen zwei Open File Descriptions; das zweite `flock(LOCK_EX)` **blockiert** — Selbst-Deadlock. `spacectl.py:67` und `store.py:190` benutzen dieselbe Datei `<DATA_ROOT>/.write.lock`. In einem Einzelprozess-Async-Server friert das den ganzen Dienst ein, nicht nur den Request. |
| **P7-N** | **Ein Space entfernen verlangt immer Re-Auth UND eine getippte Bestätigung des Space-Namens** (`confirm: "<space>"` im Body). Mitglied hinzufügen verlangt Re-Auth (Erweiterung), Mitglied entfernen nicht (Rücknahme). | P6-N („Re-Auth bei Erweiterung, nicht bei Rücknahme") ist die bestehende Regel und wird für Mitglieder unverändert übernommen. Entfernen ist keine Rechteänderung, sondern die einzige destruktive Operation des Systems — sie bekommt das härtere Ritual, nicht das mildere. |
| **P7-O** | **Space entfernen ist zweiphasig: Vorlauf ohne Schreibvorgang, dann Durchlauf.** Scheitert der Vorlauf an auch nur einem Item, wird **nichts** bewegt. | N9. Git-Commits lassen sich nicht zurücknehmen — ein Rollback existiert nicht, also darf es keinen Zustand geben, aus dem man ihn bräuchte. |
| **P7-P** | **Die Schreibseite von `.share.yml` zieht in `storage/acl.py`** (sechste benannte Contract-Öffnung), `spacectl.py` wird darauf umgestellt. | `acl.py` besitzt die Lesehoheit über diese Dateien bereits. Zwei Implementierungen desselben YAML-Schreibformats (eine im Skript, eine im Server) driften garantiert auseinander. Die 20 bestehenden `test_spacectl.py`-Tests sind der Regressionsbeweis für die Extraktion. |
| **P7-Q** | **Neues ES-Modul `webui/static/js/spaces.js`**, kein Anbau an `dialogs.js`. | `dialogs.js` ist mit 623 Zeilen bereits die größte JS-Datei; P6-AC hat den Zehn-Modul-Schnitt genau dafür gemacht. `app.js` verdrahtet Module ohnehin nacheinander per `init(deps)`. |
| **P7-R** | **`UiSettings.space_admin_enabled` bleibt und kippt auf `True`**; es schaltet die **Server-Routen**, nicht die HTML-Datei. `GET /api/v1/meta` liefert `space_admin: bool`, die UI blendet den Menüpunkt danach ein oder aus. | `app.html` ist statisch, kein Templating (steht so im Feldkommentar `config.py:48`). Ein Kill-Switch für die einzige destruktive Fläche des Systems ist es wert, behalten zu werden — er muss nur serverseitig wirken, sonst ist er Dekoration. |
| **P7-S** | **Block B folgt `ITEM_MOVE_PLAN.md` §9 wortgetreu.** Dieser Plan ergänzt nur Anker, keine Entscheidungen. | P6-AK–AN sind gelockt und ausführungsreif. Sie hier zu paraphrasieren erzeugt zwei Fassungen derselben Regel — genau der Fehler, den `DOC_LAYERS_CONVENTION.md` verbietet. |
| **P7-T** | **Kein neues MCP-Tool in dieser Phase.** Die Tool-Fläche ändert sich ausschließlich in **Beschreibungstexten** (P7-F). | Verwaltung von Rechten ist Menschen-Fläche (P6-M); Mehrfachauswahl ist UI-Fläche (P6-AL). Beide Blöcke haben ausdrücklich kein Tool nötig. |
| **P7-U** | **Der Versionsbadge geht auf `v2.2`** (`app.html`, `.rail__version`), mit dem Deploy dieser Phase. | Etablierte Konvention: der Badge zählt Deploy-Zyklen, nicht Phasennummern (v2 → v2.1 in P6). |
| **P7-V** | **Kein `P7_ABNAHME_<datum>.md`, solange die Matrix nicht überwiegend live ist.** Der laufende Abnahmestand lebt im Phase-Head. | Dieselbe Ehrlichkeitsregel, die P6 auf 🟡 gebracht hat: ein Abnahmeprotokoll über eine halb verifizierte Phase ist eine Falschaussage. |
| **P7-W** | **Die Zugangsdaten von `testnutzer-p7` liegen im Keyring und sind für Claude Code über ein Skript abrufbar** (`phase7_spaces_admin/scripts/testcred.py`). Das Skript ist **hart auf diesen einen Principal verdrahtet** — kein `--space`, kein Schlüsselparameter, keine Möglichkeit, es auf `niklas`, `fabian`, `auth-dek` oder `auth-users` zu richten. Der Keyring-Eintrag stirbt mit dem Testnutzer. | Nikinger-Vorgabe 2026-08-23. **Hard Rule 1 wird dadurch nicht aufgeweicht, sondern eingehalten:** das Geheimnis lebt ausschließlich im Keyring (Service `nikinger-space`), nie in einer Datei, nie in einem Commit, nie in einer Logzeile — genau wie `authserver/users.py` es seit P4 macht. Neu ist nur, dass ein Skript es lesen darf, und das ist der etablierte Pfad (`load_users_from_keyring()`). **Die harte Verdrahtung ist der eigentliche Schutz:** ein Werkzeug mit `--space`-Parameter wäre kein Testhelfer, sondern ein Credential-Exfiltrationswerkzeug mit freundlichem Namen. |

---

## §2 Befundlage gegen den echten Code

Alles hier ist in der Planungssession **gegen das Repository geprüft**, nicht erinnert.

### 2.1 Der Fabian-Fund, zerlegt

> „hab nur gesehen dass er die einzelnen aufgaben oder notizen immer mit so bezeichnungen
> ausstattet und dann die immer anspricht, ich kann nur keine sehen im sharefyx und kann die
> garnicht zuordnen: itm_807df219 so ungefähr"

Zwei getrennte Ursachen, zwei getrennte Fixes:

| Hälfte | Befund | Fix |
|---|---|---|
| „ich kann keine sehen" | Die ID steht auf **jedem** JSON-Objekt (`webui/serializers.py :: item_to_json()` Feld `"id"`, `summary_to_json()` ebenso) und wird in `js/*.js` **ausschließlich zur internen Adressierung** benutzt — `grep` findet keine einzige Renderstelle. | A1: ID-Chip in beiden Detailansichten |
| „kann die garnicht zuordnen" | `store.py :: search()` baut den Haystack aus `f"{item.title} {' '.join(item.tags)}"` (`store.py:421`) — eine Suche nach `itm_807df219` findet **nichts**. | A1: ID-Lookup in `_items_get` (P7-D/P7-E) |

Dazu die Ursache eine Ebene höher: eine Claude-Instanz **nennt** einem Menschen gegenüber IDs.
Das ist P7-F.

### 2.2 Die vorhandenen Bausteine für Block C

| Baustein | Fundstelle | Was er schon kann |
|---|---|---|
| `.share.yml`-Lesen | `storage/acl.py` (ganze Datei, 138 Zeilen) | `Grant`, `AclDecision`, `AclReader.grants_for_space()`, `members_of_space()`, `decision_for()`, `stat()`-invalidierter Cache, fail-closed |
| `.share.yml`-Schreiben | `phase6_shares/scripts/spacectl.py:90–107` (`_load_share_file`/`_dump_share_file`), `:185–210` (add), `:213–242` (remove), `:133–148` (create), `:245–273` (remove-space inkl. `shutil.rmtree` in Zeile 270) | alles — aber ausschließlich als CLI, mit eigenem `_DataRootLock` (`:62–83`) |
| Re-Auth-Gate | `webui/shares.py :: require_share_reauth()` (Signatur `:55–65`), `widens()`, `webui/errors.py:47` (`"reauth_required": 403`) | Credential-Prüfung gegen `UserDirectory` + `LoginThrottle` + `AuthStore`, wirft `ApiError` |
| Route-Tabelle | `webui/api.py:743–755` | hier kommen die fünf neuen Routen hinein |
| `api_routes()`-Signatur | `webui/api.py:188–195` | trägt bereits `permissions`, `auth_store`, **`users: UserDirectory`** — Block C braucht **keinen neuen Parameter** |
| Meta-Endpunkt | `webui/api.py:255–261` | hier kommt `space_admin` hinein |
| Der Seam | `webui/config.py:52` (`space_admin_enabled: bool = False`), `app.html:283` (harter `disabled`-Knopf), `phase5_ui/tests/test_static_routes.py:135–145` (Test, der beides festhält — **inklusive Docstring, die „Phase 7" nennt**) | drei gekoppelte Stellen, die in **einem** Commit fallen müssen |

**Der Fund, der Block C klein macht:** `api_routes()` bekommt alles Nötige bereits herein. Es
fehlen fünf Routen, ein Modul, ein Dialog — kein neuer Parameter, keine neue Abhängigkeit, keine
Änderung an `mcpserver/app.py`.

### 2.3 Der Lock-Fund (Grundlage von P7-M)

`spacectl.py:62–83` und `store.py:186–197` sperren **dieselbe Datei**, `<DATA_ROOT>/.write.lock`,
über **verschiedene** File Descriptors. Empirisch in der Planungssession nachgemessen:

```
flock(fd_a, LOCK_EX)  →  ok
flock(fd_b, LOCK_EX)  →  BLOCKIERT (derselbe Prozess, zweites open())
```

`flock`-Sperren hängen an der Open File Description, nicht am Prozess. Ein Handler, der den Lock
hält und darin `store.move()` aufruft, hängt sich selbst auf — und mit sich den ganzen
Serverprozess, weil `webui` einprozessig-async läuft. **Das ist der wahrscheinlichste Weg, wie
Block C still kaputtgeht**, deshalb steht es als eigene Entscheidung im Register.

### 2.4 Der Live-Stand (Grundlage des Doku-Audits)

```
/opt/sharefyx/current -> /opt/sharefyx/releases/20260821T183341.270842Z
git -C /opt/sharefyx/current rev-parse HEAD  ->  f96125e
```

`d068d1c`, `92b918b`, `d348e2e` sind per `git merge-base --is-ancestor` **nachweislich Vorfahren**
davon. Der Verdacht des Handovers §4.1 („die Zeilen 8–16 sind stale") ist damit **plausibel, aber
noch nicht bewiesen** — bewiesen sind nur diese drei, in Prosa zitierten SHAs, nicht die neun
Commits hinter den Tabellenzeilen. Step 0 führt den Beweis (§4.0.2).

---

## §3 Berührungsfläche je Datei

| Datei | Block | Was passiert |
|---|---|---|
| `phase1_storage/storage/acl.py` | C1 | **+Schreibseite** (sechste benannte Contract-Öffnung) |
| `phase1_storage/storage/store.py` | — | **unverändert** (P7-D und P7-G halten beide davon fern) |
| `phase6_shares/scripts/spacectl.py` | C1 | auf `acl.py` umgestellt, `_DataRootLock` entfällt |
| `phase5_ui/webui/api.py` | A1, A4, C2, C3 | ID-Lookup, Feld-Whitelist, fünf Routen, `space_admin` in `_meta` |
| `phase5_ui/webui/shares.py` | C2 | Credential-Prüfung extrahiert, `require_space_reauth()` neu |
| `phase5_ui/webui/config.py` | C3 | `space_admin_enabled` auf `True`, Feldkommentar neu |
| `phase5_ui/webui/static/js/editor.js` | A1, A3 | ID-Chip, Asset-Leiste mit Entfernen-Knopf |
| `phase5_ui/webui/static/js/markdown.js` | A3 | Alt-Text-Fallback für unbekannte `asset:`-Referenzen (V73) |
| `phase5_ui/webui/static/js/spaces.js` | C3 | **neu** |
| `phase5_ui/webui/static/js/{app,list,state,dialogs}.js` | A1, B, C3 | Verdrahtung, Suchhinweis, Auswahl-Zustand |
| `phase5_ui/webui/static/{app.html,app.css}` | A1, A3, B, C3, P7-U | Dialoghülle, Chips, Auswahlleiste, Versionsbadge |
| `phase2_mcp/mcpserver/tools.py` | A2 | **nur Beschreibungstexte** (P7-T) |
| `phase7_spaces_admin/scripts/testcred.py` | A7b | **neu** — Testnutzer-Zugang aus dem Keyring, hart auf `testnutzer-p7` verdrahtet (P7-W) |
| `phase4_auth/authserver/totp.py` | A7b | **nur importiert, nie geändert** — bleibt auf der Tabu-Liste |
| `phase7_spaces_admin/` | 0, C | Phase-Head, `SESSIONS_ARCHIVE.md`, `tests/`, `scripts/` |
| `docs/` | alle | `INDEX.md`, `UPDATE_LOG.md`, Handover 6.5, Übersichtsgrafiken |

---

## §4 Schritt-Sequenz

Jeder Step endet mit einem Commit, der **im selben Commit** die Modul-Tabelle des Phase-Heads und
den `## Session stopped`-Block aktualisiert (Hard Rule 8). Kein Step gilt als fertig ohne grünes
`pytest`.

### Step 0 — Haushalt und Verifikationsdurchlauf

**Dies ist der vom Nikinger ausdrücklich verlangte Aufräumschritt. „Nichts zu tun" ist ein
zulässiges und zu meldendes Ergebnis** — aber jeder der sechs Punkte wird tatsächlich gefahren,
nicht überschlagen.

**0.1 — `pytest`-Ausgangsstand messen, nicht übernehmen.**
```
.venv/bin/python -m pytest -q 2>&1 | tail -3
```
Erwartung **828** (Stand 2026-08-23, Handover §1 Punkt 4) — `[VERIFY]` **V71**. Die reale Zahl
kommt in den Phase-Head, nicht die erwartete. Diese Suite hat in vier Phasen dreimal eine
Delta-Rechnung ohne Gegenzähler widerlegt; es wird gezählt, nicht gerechnet.

**0.2 — Doku-Audit (Handover §4.1), mit Beweis je Zeile.**

Betroffen: `phase6_shares/CLAUDE.md`, Modul-Status-**Zeilen 8–16** (Step 7a + Step 7 Commits 0–6)
und **Vormerkungen Punkt 2** — alle tragen `gebaut, noch nicht deployt` bzw. `Deploy beim
Nikinger`.

```bash
LIVE=$(git -C /opt/sharefyx/current rev-parse HEAD)   # 2026-08-23: f96125e
# Kandidaten-SHAs je Tabellenzeile finden — Commit-Betreffs sind die Brücke:
git log --oneline --format='%h %ad %s' --date=short \
  -- phase5_ui/webui/static/ phase5_ui/webui/api.py phase5_ui/webui/shares.py \
  | head -40
# je gefundenem SHA:
git merge-base --is-ancestor <sha> "$LIVE" && echo "<sha> IST live" || echo "<sha> ist NICHT live"
```

**Regel, nicht verhandelbar:** Eine Tabellenzeile bekommt nur dann „deployt", wenn für sie ein
konkreter SHA gefunden **und** als Vorfahre bewiesen wurde. Findet sich für eine Zeile kein
eindeutiger Commit, wird das als solches hingeschrieben („kein eindeutiger Commit zuordenbar"),
nicht geraten. Der Wert dieses Audits ist der Nachweis, nicht die Behauptung — genau deshalb hat
die Vorphase ihn nicht selbst gefahren.

**0.3 — `up:`/`down:`-Links auflösbar?** Über alle `.md` mit Frontmatter: jedes Ziel in `up:` und
`down:` relativ zur Datei auflösen, Existenz prüfen, Trefferliste ausgeben. Erwartung: leer.

**0.4 — Indexzeile je `.md`?** Jede `.md` unter `./` (ohne `.venv/`, `.git/`, `.agents/`,
`*/tests/golden/`) muss in `docs/INDEX.md` genau einmal vorkommen. Erwartung: leer.

**0.5 — Softcap-Prüfung.**
```
find . -name "*.md" -not -path "./.venv/*" -not -path "./.git/*" \
       -not -path "./.agents/*" -not -path "*/.pytest_cache/*" -size +40k
```
Jeder Treffer muss ein 📕 oder 📦 sein. **Stand der Planungssession: elf Treffer, alle regelkonform.**
Zwei lebende Dokumente sind grenzwertig und werden von P7 angefasst:
`phase6_shares/CLAUDE.md` (~38 KB) und `phase6_shares/ITEM_MOVE_PLAN.md` (~39 KB). **Wer eine der
beiden erweitert, prüft vorher die Größe** — reißt sie den Cap, wird vorher rotiert
(`scripts/rotate_session_block.sh`), nicht danach.

**0.6 — Phase-Skelett anlegen.**
- `phase7_spaces_admin/CLAUDE.md` — L1-Header-Card, Mission, Scope, harte Regeln dieser Phase,
  leere Modul-Tabelle, leere Abnahmematrix (P7-1–P7-24 aus §6), erster Session-Block.
- `phase7_spaces_admin/SESSIONS_ARCHIVE.md` — leer angelegt, mit Header-Card.
- `phase7_spaces_admin/tests/conftest.py` — leer, wie P6 Step 0 und 6.5 Step 0.
- `ROADMAP.md` — neue Phase-7-Zeile in der Tabelle **und** ein eigener Abschnitt (DRIN/DRAUSSEN/
  Status), Muster: der Phase-6.5-Abschnitt.
- `docs/INDEX.md` — Zeilen für diesen Plan, den Phase-Head, das Archiv; Abschnitt „Active phase"
  auf Phase 7 umstellen.

**0.7 — Sechste Contract-Öffnung ankündigen.** In `phase1_storage/CLAUDE.md` unter „Geerbte
Contracts": datierter Absatz, dass `storage/acl.py` eine Schreibseite bekommt (P7-P), mit
Funktionsliste aus §4.C1. **Ankündigung vor dem Code**, wie bei allen fünf Vorgängern.

**DoD Step 0:** alle sechs Punkte gefahren und ihr Ergebnis (auch „nichts zu tun") im
Session-Block protokolliert; Audit-Tabelle mit SHA je Zeile; Skelett steht; `pytest` unverändert.

---

### Block A — Fixes und Abschluss der Vorphase (fällt nie)

#### A1 — Item-ID sichtbar und auffindbar

**Backend** — `phase5_ui/webui/api.py :: _items_get` (`api.py:342–384`):

```python
from storage.files import ITEM_ID_RE   # ^itm_[0-9a-f]{8}$, files.py:40

raw_query = q.get("query")
query = raw_query.strip() if isinstance(raw_query, str) else None
id_lookup = bool(query and ITEM_ID_RE.fullmatch(query))
# P7-E: eine ID-Suche ignoriert Space- und Ordnerfilter — wer die ID hat, weiß nicht, wo es liegt.
global_scope = q.get("space") is None or id_lookup

result = store.search(
    None if id_lookup else query,
    space=None if id_lookup else q.get("space"),
    folder=None if id_lookup else q.get("folder"),
    type=q.get("type"), status=q.get("status"), tag=q.get("tag"),
    due_before=due_before, limit=_STORE_FETCH_LIMIT, offset=0,
)
```
Direkt **nach** dem bestehenden `can_read_item_as_human`-Filter (`api.py:369–372`):
```python
if id_lookup:
    items = [i for i in items if i.id == query]
```

Die Rechteprüfung bleibt damit unverändert davor — eine ID, auf die der Anfragende kein Leserecht
hat, liefert eine leere Ergebnisliste, **nicht** einen `403` und nicht einen `404`. Beides wäre ein
Existenz-Orakel über fremde Items.

**Frontend:**
- `editor.js :: showReadonlyItem()` (`editor.js:195–199`): nach dem Versionsbadge ein weiteres
  Element, `idChip(item.id)`.
- `editor.js`: neue Funktion `idChip(itemId)` — `<button type="button" class="id-chip"
  title="ID kopieren">itm_…</button>`; Klick ruft `navigator.clipboard.writeText(itemId)` und
  `toast("ID kopiert.")`. Kein `execCommand`-Fallback: fehlt die Clipboard-API, bleibt der Text
  markierbar, das genügt.
- Editor-Ansicht: derselbe Chip in die Kopfdaten-Fläche, neben `#meta-digest`
  (`app.html:102–105`) — neues `<span id="meta-item-id"></span>` in `.panel__head`, befüllt in
  `showEditableItem()`.
- `list.js`: der Platzhaltertext des Suchfelds (`#search-input`, verdrahtet `list.js:351`) nennt
  die ID: `"Titel, Tag oder itm_…"`.
- `app.css`: `.id-chip` — monospaced, `tnum`, gedämpft, gleiche Höhe wie `.version-num`.

**Tests** (`phase5_ui/tests/test_api.py`, +4):
| Name | Prüft |
|---|---|
| `test_items_get_finds_an_item_by_its_id` | `?query=itm_…` liefert genau dieses Item |
| `test_id_lookup_ignores_space_and_folder_filter` | Treffer auch bei gesetztem, nicht passendem `space=`/`folder=` (P7-E) |
| `test_id_lookup_respects_read_permission` | fremdes, nicht freigegebenes Item ⇒ **leere Liste**, kein 403/404 |
| `test_id_lookup_with_unknown_id_returns_empty_list` | `itm_deadbeef` ⇒ `total: 0`, kein Fehler |

**Tabu-Probe:** `git diff phase1_storage/storage/` bleibt in diesem Step leer (P7-D).

**DoD:** vier Tests grün, ID in beiden Ansichten sichtbar und kopierbar (Browserprobe, nicht
behauptet), Suche nach einer echten ID findet das Item.

#### A2 — Tool-Beschreibungen: Titel statt ID gegenüber Menschen (P7-F)

`phase2_mcp/mcpserver/tools.py` — ein Satz, wörtlich identisch, in die Beschreibungen von
`search_items`, `get_item`, `get_item_meta` und `create_item`:

> „Nenne einem Menschen gegenüber immer den **Titel** eines Items, nicht seine `itm_…`-ID — die
> ID ist eine interne Adresse und in der Weboberfläche nur als Kopierfeld sichtbar."

**Test** (`phase2_mcp/tests/test_tools.py`, +1): `test_tool_descriptions_tell_the_agent_to_name_titles_not_ids`
— prüft den Satz in allen vier Beschreibungen. **`[VERIFY]` V72:** wie die bestehenden Tests dieser
Datei an die Beschreibungstexte kommen (Phase 6.5 hat dafür bereits ein Muster etabliert, siehe
deren Plan §3 und `[VERIFY]` V63). **Dieses Muster übernehmen, keines erfinden.**

**DoD:** Test grün, `mcp_smoke.py` unverändert grün.

#### A3 — Entfernen-Knopf für Bilder (schließt P6.5-12)

**Kein neuer Serverpfad.** Vorhanden und ungenutzt:
- `storage/store.py :: delete_asset()` — verschiebt nach `_assets/<item_id>/_trash/`, löscht nie
  (Entscheidung N5 aus 6.5, Entscheidung H aus P1 bleibt unangetastet).
- `DELETE /api/v1/items/{item_id}/assets/{asset_id}` — `webui/api.py:703, 756–760`.

**Frontend** (`editor.js`, direkt neben dem Einfüge-Pfad `editor.js:511–534`):
- Neue Funktion `renderAssetStrip(item)` — rendert `item.assets` (steht bereits auf
  `item_to_json()`, Feld `"assets"`) als Leiste unter der Editor-Werkzeugleiste: je Asset der
  Dateiname und ein `×`-Knopf.
- `×` ruft `api("/items/" + id + "/assets/" + assetId, { method: "DELETE" })`, danach Item neu
  laden und `renderAssetStrip()` + Vorschau neu rendern.
- **Wortwahl:** „entfernen", nie „löschen" — der Server verschiebt, er löscht nicht. Der
  Bestätigungstext sagt das: „Das Bild wird aus dem Dokument entfernt und in den Papierkorb des
  Items verschoben."
- `app.html`: `<div class="asset-strip" id="asset-strip"></div>` unter `#editor-toolbar`.
- `app.css`: `.asset-strip`, `.asset-strip__item`, `.asset-strip__remove`.

**Der Teil, der leicht übersehen wird** — Abnahmezeile P6.5-12 verlangt: *„Referenz rendert danach
als Alt-Text."* Nach dem Entfernen steht `![Testbild](asset:ast_c28583e6)` weiter im Body.
`markdown.js:228` prüft die URL-Form gegen `^/api/v1/items/itm_[0-9a-f]{8}/assets/ast_[0-9a-f]{8}$`.
**`[VERIFY]` V73:** was `markdownToHtml()` mit einer `asset:`-Referenz macht, deren Asset es nicht
mehr gibt. Rendert sie ein kaputtes `<img>`, bekommt `markdownToHtml(body, { itemId, assetIds })`
einen dritten Kontextschlüssel und gibt für unbekannte IDs den **Alt-Text** statt eines `<img>`
aus. Rendert sie bereits Alt-Text: nichts tun, Befund notieren.

**Tests:** keine Unit-Tests (P5-T: JS bleibt ungetestet). Verifikation per echter Browserprobe:
Bild einfügen → sichtbar → entfernen → Alt-Text sichtbar → Datei liegt unter
`_assets/<item_id>/_trash/`. `pytest` unverändert als Regressionsprobe.

**DoD:** P6.5-12 live abhakbar; die Datei liegt nachweislich im `_trash/`, nicht gelöscht.

#### A4 — Feld-Whitelist an `_items_patch` (Befund O6)

`phase5_ui/webui/api.py :: _items_patch` (`api.py:435`), unmittelbar nach `body = await
_json_body(request)`:

```python
_PATCH_FIELDS = frozenset({
    "version", "title", "body", "status", "due", "tags", "links", "type",
    "folder", "space", "visibility", "share_read", "share_write",
    "password", "totp",          # Re-Auth, wird nie an store.update() gereicht
})
unknown = sorted(set(body) - _PATCH_FIELDS)
if unknown:
    raise ApiError("validation_failed", f"Unbekannte Felder: {unknown}")
```

**Warum hier und nicht in `store.update()`:** siehe P7-G. `store.py:512–513` **ist** die
Round-Trip-Treue — Abnahmezeile 13 der Phase 5 (ein von Hand eingefügtes `custom_test:`-Feld
überlebt eine UI-Bearbeitung) hängt an genau diesem `else`-Zweig. Ein Feld, das schon in der Datei
steht, wird davon nicht berührt; abgewiesen wird nur, was **neu über HTTP hereinkommt**.

**`[VERIFY]` V74, vor dem Schreiben der Liste:** welche Schlüssel die Oberfläche tatsächlich
sendet. `grep -n "method: \"PATCH\"" -B 15 phase5_ui/webui/static/js/*.js` — `editor.js:337`,
`list.js:163`, `dialogs.js` (Verschieben- und Freigabe-Dialog). **Die Whitelist muss eine Obermenge
davon sein**, sonst bricht das Speichern. Ein Test hält genau das fest.

**Tests** (`phase5_ui/tests/test_api.py`, +2):
- `test_items_patch_rejects_an_unknown_field` — `{"version":1,"spce":"fabian"}` ⇒ `400
  validation_failed`, Datei unverändert (genau der O6-Fall aus `ITEM_MOVE_PLAN.md` §112).
- `test_items_patch_accepts_every_field_the_ui_sends` — pinnt die Whitelist gegen die real
  gesendeten Schlüssel.

**Nicht mit erledigt:** `_items_post` hat seine Whitelist seit P6 Step 7 Commit 3. Die MCP-Seite ist
durch die typisierte `update_item`-Signatur (`tools.py:614–630`) bereits dicht. **O6 ist damit an
allen drei Flächen geschlossen** und darf im Handover als geschlossen geführt werden.

#### A5 — Sichtbarkeits-Migration live (N4, P7-H)

**Reihenfolge, nicht vertauschbar:**

1. `docs/UPDATE_LOG.md` bekommt **oben** einen auf den Migrationstag datierten Eintrag. Der erste
   Eintrag des Logs (2026-08-09) hat genau diese Umstellung angekündigt — sie jetzt ohne Notiz zu
   fahren, entwertet das Banner.
2. **Claude Code:** `--dry-run` (Default) gegen den echten `DATA_ROOT`, Report lesen. Erwartung
   **73 Dateien**, kein Versionssprung (das Skript hebt `version` bewusst nicht).
3. **Nikinger:** `migrate_visibility.py --apply`. **Nicht Claude Code** (P7-H).
4. **Claude Code, read-only:** `grep -L '^visibility:' <DATA_ROOT>/**/*.md | wc -l` ⇒ `0`;
   `git -C <DATA_ROOT> log --oneline | head` zeigt die Migrations-Commits.

**Was danach in der Doku steht — ehrlich, nicht geglättet:** Abnahmezeile 8 hat zwei Hälften. Die
erste ist damit erfüllt. Die zweite („Fabian sieht Niklas' Space nicht mehr") wurde beim Cutover
2026-08-13 **bewusst überstimmt** — es gibt gegenseitige `read:`-Grants, weil der Nikinger das so
wollte. Die Zeile wird entsprechend geteilt notiert, nicht als Ganzes abgehakt.

#### A6 — Gate-A→B-Punkt 3 aus Phase 6: Purge (datiert, ab 2026-08-28)

Die einzige rein kalendarische offene Zeile des Projekts (P6-Abnahmezeile 4). Ab **2026-08-28**
prüfbar:
```
sqlite3 <auth.sqlite3> "select count(*) from clients;  select count(*) from token_families;"
systemctl list-timers sharefyx-purge*        # lief der Timer?
# nach einem realen Purge-Lauf erneut zählen — die Zeilenzahl muss gesunken sein
```
Ist das Datum bei Ausführung noch nicht erreicht: Zeile bleibt offen, **wird als „Datum noch nicht
erreicht" protokolliert**, nicht als „nicht geprüft".

#### A7 — Dritter Principal `testnutzer-p7` (P7-J, schließt P6-W)

**Anlegen** (Nikinger, einmalig, wenige Minuten):
```
authctl.py invite --space testnutzer-p7 --purpose enroll
# Einladungslink im Browser öffnen, Passwort + TOTP setzen
spacectl.py create-space testnutzer-p7      # falls das Verzeichnis nicht schon existiert
```
**`[VERIFY]` V75:** dass Einladung, Enrollment und `create-space` einen **Bindestrich** im
Space-Namen akzeptieren. Geprüft ist bisher nur: `authctl.py` validiert Space-Namen gar nicht, und
`spacectl.py:135` lehnt nur `/`, führenden `.` und `RESERVED_DIR_NAMES` ab. `files.slugify()` und
`files.item_path()` sehen den Namen bei **jedem** Write — vor dem Anlegen einmal gegen eine
Wegwerf-Instanz probieren, nicht am echten `DATA_ROOT` herausfinden.

**Was er freischaltet** (das ist der Grund für den ganzen Schritt):

| P6-Zeile | Bisherige Blockade | Mit `testnutzer-p7` |
|---|---|---|
| 18 | dritter Nutzer nie angelegt | direkt erfüllbar |
| 24 | hing an 18 | direkt erfüllbar |
| 36/37 | mit `niklas` **strukturell unmöglich** — `niklas` steht in `fabian/.share.yml` unter `read:`, sieht dort also ohnehin alles | `testnutzer-p7` hat **keinen** space-level Grant ⇒ der Fall „nur item-level Share" ist endlich darstellbar |
| 10–13, 27, 28 | brauchten einen zweiten Menschen | mechanisch prüfbar (Fabian-Sitzung bleibt der schönere, aber optionale Weg — N10) |
| P6.5-8, P6.5-13 | dito | dito |

**Abbauen, am Ende von Block A:**
```
phase7_spaces_admin/scripts/testcred.py purge     # Keyring-Eintrag zuerst (A7b)
spacectl.py remove-space testnutzer-p7 --force
authctl.py disable-user --space testnutzer-p7
authctl.py revoke-sessions --space testnutzer-p7
spacectl.py check --json          # keine verwaisten .share.yml-Referenzen mehr
diagnose.sh                       # Prüfung 12 sauber
```
Das erfüllt P6-Abnahmezeile 24 („dritter Space entfernt, keine verwaisten Freigaben") **als echten
Lauf**, nicht als Konstruktion.

> **Reihenfolge-Hinweis:** A7 kommt **nach** A5. Ein frisch angelegter Space soll die
> Sichtbarkeitswelt sehen, die nach der Migration gilt, nicht die davor.

#### A7b — `testcred.py`: Testnutzer-Zugang für Claude Code (P7-W)

**Zweck, in einem Satz:** Claude Code soll sich als `testnutzer-p7` anmelden, Connector-Consent
geben und Re-Auth-Gates durchlaufen können, **ohne dass der Nikinger für jeden Abnahmeschritt
danebensitzt** — sonst löst der dritte Principal die Abnahmeblockade nur zur Hälfte.

**Neues Skript `phase7_spaces_admin/scripts/testcred.py`.** Vier Unterbefehle, keine Optionen:

| Befehl | Verhalten |
|---|---|
| `testcred.py store` | Liest ein JSON `{"space","password","totp_secret"}` von **stdin**, prüft `space == ALLOWED_SPACE`, legt es unter Keyring-Service `nikinger-space`, Schlüssel `p7-testcred` ab. **stdin, niemals `argv`** — Argumente stehen in der Prozessliste und in der Shell-History |
| `testcred.py password` | Passwort auf stdout, sonst nichts |
| `testcred.py totp` | Aktueller Code: `totp.totp_at(secret, int(time.time()) // 30)` auf stdout, sonst nichts |
| `testcred.py purge` | Keyring-Eintrag löschen. **Teil der A7-Abbau-Checkliste**, nicht optional |

**Die harte Verdrahtung (P7-W), das eigentliche Sicherheitsmerkmal:**

```python
ALLOWED_SPACE = "testnutzer-p7"      # Modulkonstante, kein Parameter
KEYRING_SERVICE = "nikinger-space"   # aus authserver.users übernommen, nicht neu erfunden
KEYRING_KEY = "p7-testcred"          # eigener Schlüssel, NIE auth-users oder auth-dek
```

Es gibt **kein** `--space`, **kein** `--key`, **kein** `--service`. Das Skript kann strukturell
nur diesen einen Eintrag lesen. Weicht der gespeicherte `space` von `ALLOWED_SPACE` ab, bricht es
ab. Ein Werkzeug mit freier Schlüsselwahl wäre ein Credential-Exfiltrationswerkzeug mit
freundlichem Namen — und läge außerdem in einem Git-Repository.

**Was das Skript NICHT tut, ausdrücklich:**
- keinen Wert nach stderr oder in ein Log schreiben (Hard Rule 7: stdout trägt das Ergebnis,
  stderr die Diagnose — der Seed erscheint in **keinem** von beiden, nur das abgeleitete Code-
  bzw. Passwortergebnis auf stdout);
- keinen Wert in eine Datei schreiben, auch nicht temporär (Hard Rule 1);
- `authserver/totp.py` **nicht ändern** — es wird ausschließlich **importiert**. Die Datei bleibt
  auf der Tabu-Liste (§0.3); eine zweite TOTP-Implementierung neben der getesteten wäre der
  klassische Weg, wie ein Krypto-Primitiv still auseinanderläuft.

**Ablauf beim Einrichten** (der einzige Schritt, der den Nikinger braucht, ist der erste):

1. **Nikinger:** `authctl.py invite --space testnutzer-p7 --purpose enroll` → Einladungslink.
2. **Claude Code:** Enrollment im Browser (`claude-in-chrome`) über diesen Link. Der TOTP-Seed
   wird **genau einmal** angezeigt — er wird in derselben Sitzung per Pipe an
   `testcred.py store` gereicht und **an keiner anderen Stelle festgehalten**: nicht im
   Transkript-Klartext, nicht im Scratchpad, nicht in einer Notiz.
3. **Ab hier ohne Nikinger:** Login, OAuth-Consent für einen eigenen Connector, Re-Auth-Gates —
   `testcred.py password` und `testcred.py totp` liefern, was die Formulare verlangen.

**Tests** (`phase7_spaces_admin/tests/test_testcred.py`, neu, ~7 — `keyring` wird gemockt, es
läuft **kein** echter Keyring-Zugriff in der Suite):
`store` lehnt einen fremden `space` ab · `store` liest ausschließlich stdin und akzeptiert keinen
Wert aus `argv` · `password`/`totp` geben genau einen Wert auf stdout und nichts sonst ·
`totp` stimmt gegen `totp.verify()` mit demselben Seed überein · `purge` entfernt den Eintrag ·
**Meta-Test: das Modul enthält keinen Pfad zu `auth-users`/`auth-dek`** und `ALLOWED_SPACE` ist
eine Konstante ohne Zuweisung aus `argv`/`os.environ` (dieselbe Kategorie wie
`test_security_review_register.py` aus P5 Step 1 — der Test hält eine Regel fest, nicht ein
Verhalten).

**`[VERIFY]` V80:** ob der Keyring in der Umgebung, in der Claude Code läuft, ohne
Desktop-Session beschreib- und lesbar ist (`keyring.get_password("nikinger-space", "auth-dek")`
lieferte in P5 einen Wert, also grundsätzlich ja — vor A7b einmal mit einem **Wegwerf-Schlüssel**
gegenprobieren, nicht mit dem echten).

#### A8 — Phase 6.5 formal abschließen (P7-I)

1. **Abnahmestand von 6.5 neu zählen.** A3 schließt P6.5-12; A7 schließt P6.5-8 und P6.5-13.
   Damit bleibt **P6.5-14** (Nikingers eigene Bewertung der Upload-Ankündigungsdisziplin) — das ist
   kein Selbstzertifizierungs-Kriterium und bleibt es auch.
2. **Glyph aus der gemessenen Zahl ableiten, nicht wählen:** 14/14 ⇒ ✅, sonst 🟡. Bei 13/14 mit
   ausschließlich P6.5-14 offen ist der Sprung auf ✅ eine **Nikinger-Entscheidung**, genau wie bei
   P6 — nicht vorwegnehmen.
3. **`docs/concepts/PHASE6_5_CLOSEOUT_HANDOVER.md`** (neu — **dieser Name ist verbindlich**, nicht
   `PHASE65_`; er folgt der Verzeichniskonvention `phase6_5_tools_images/`, weil eine Phase „6.5"
   sonst als „Phase 65" gelesen wird. Die Indexzeile trägt exakt diesen Namen) — Skelett von
   `PHASE6_CLOSEOUT_HANDOVER.md`: Status, Delta seit dem P6-Handover, Abnahmestand-Tabelle, offene
   Entscheidungen, `[VERIFY]`-Bilanz V59–V70 (V64 unverändert offen, V60 mit dem Deploy 2026-08-21
   geschlossen).
4. **`docs/concepts/phase6_5_tools_images_uebersicht.svg`** (neu) — jede abgeschlossene Phase hat
   eine. Stil der fünf Vorgänger, 1080×1080. **Rendern und tatsächlich ansehen** (`~/.claude-code-tools/`),
   nicht ungeprüft committen — in P5 und P6 fand genau diese Sichtprobe Textüberläufe.
5. **P1-Contract schließen — und im selben Absatz neu öffnen.** In `phase1_storage/CLAUDE.md`:
   Öffnungen 3 (P6 Step 4), 4 (`Store.move()`), 5 (Assets, 6.5) werden als geschlossen datiert;
   die in Step 0.7 angekündigte **sechste** (P7, `acl.py`-Schreibseite) bleibt offen und wird
   dabei ausdrücklich genannt. Ein Schließen ohne diesen Satz wäre dieselbe Falschaussage, die
   der P6-Handover §5.6 vermieden hat.
6. `ROADMAP.md` + Root-`CLAUDE.md` + `docs/INDEX.md` auf den neuen 6.5-Status, alles in **einem**
   Commit.

---

### GATE A → C (hart)

**Vier Punkte, alle live, bevor eine Zeile Block C entsteht:**

1. Ein Item wird in der Weboberfläche über seine `itm_…`-ID gefunden — von einem Menschen, im
   echten Browser (A1).
2. Ein Bild lässt sich im Editor entfernen; die Referenz rendert danach als Alt-Text; die Datei
   liegt im `_trash/` (A3, schließt P6.5-12).
3. Die Migration ist gelaufen: **0** `.md`-Dateien ohne `visibility:` (A5).
4. `testnutzer-p7` existiert und hat mindestens einen echten Cross-Principal-Lesetest über den
   Connector absolviert (A7).

**Warum ein hartes Gate:** Block C schreibt `.share.yml`-Dateien und entfernt Verzeichnisse aus
dem echten `DATA_ROOT`. Das auf einem Fundament zu tun, dessen Sichtbarkeitsmigration nie lief und
dessen Rechte-Randfall nie an einem echten dritten Principal geprüft wurde, ist genau die Sorte
Sand, auf der P6 auf 🟡 stehen geblieben ist. Ein Überspringen ist eine benannte
Nikinger-Entscheidung, kein Ermessen von Claude Code.

---

### Block C — Space-Verwaltung in der Weboberfläche

#### C1 — Schreibseite von `.share.yml` in `storage/acl.py` (sechste Contract-Öffnung, P7-P)

**Neu in `phase1_storage/storage/acl.py`** (Namen sind verbindlich):

```python
def read_share_file(data_root: Path, space: str) -> dict[str, list[str]]
def write_share_file(data_root: Path, space: str, data: dict) -> None
def add_member(data_root: Path, space: str, name: str, *, write: bool) -> bool
def remove_member(data_root: Path, space: str, name: str) -> list[str]
def create_space(data_root: Path, name: str) -> Path
def remove_space_dir(data_root: Path, name: str) -> None
def spaces_referencing(data_root: Path, name: str, *, exclude: Path | None = None) -> list[str]
class AclWriteError(ValueError): ...
```

**Verhalten, aus `spacectl.py` unverändert übernommen** (das ist eine Extraktion, keine
Neuentwicklung — die Referenz sind `spacectl.py:90–107, 113–127, 133–148, 185–242`):
- `write:` impliziert `read:` bereits beim **Lesen** (`acl.py:84`) — beim Schreiben wird ein Name
  deshalb **nicht** doppelt eingetragen.
- Leere Listen werden nicht mitgeschrieben; wird die Datei dadurch leer, wird sie entfernt
  (`spacectl.py:231–239`). Dieselbe „leer = nicht vorhanden"-Disziplin wie im Frontmatter.
- `read_share_file()` ist **laut**, nicht fail-closed: kaputtes YAML wirft. `AclReader._parse()`
  bleibt fail-closed — wer schreibt, muss einen kaputten Bestand sehen; wer Rechte auflöst,
  darf daraus nie mehr Rechte ableiten. **Die beiden Pfade bleiben getrennt.**
- `create_space()` lehnt `/`, führenden `.` und `files.RESERVED_DIR_NAMES` ab (`files.py:18`:
  `{"_archive", "_assets"}`), wirft sonst `AclWriteError`.
- Jede schreibende Funktion erzeugt **genau einen** `history.commit()` mit demselben
  Betreff-Format wie bisher: `share <space> <key>+=<name>` / `unshare <space> <name>` /
  `remove-space <name>`.

**P7-M, die Lock-Regel, hier konkret:** jede dieser Funktionen nimmt `flock` auf
`<data_root>/.write.lock` **selbst** und gibt ihn vor der Rückkehr wieder frei. Keine Funktion ruft
eine `Store`-Methode auf. Kein Aufrufer hält den Lock über mehrere dieser Aufrufe hinweg. Ein
Kommentar an der Lock-Hilfsfunktion nennt den Grund (zwei OFDs im selben Prozess blockieren
einander) — sonst baut ihn jemand in einem halben Jahr wieder ein.

**`spacectl.py` wird umgestellt:** `_load_share_file`, `_dump_share_file`, `_spaces_referencing`
und die Rümpfe von `_cmd_create_space`, `_cmd_add_member`, `_cmd_remove_member`,
`_cmd_remove_space` rufen die neuen `acl`-Funktionen. `_DataRootLock` (`spacectl.py:62–83`)
entfällt für diese Befehle. **Alle Ausgabetexte und Exit-Codes bleiben byte-identisch** — das ist
die Bedingung, unter der die 20 bestehenden Tests der Regressionsbeweis sein können.

**Tests:**
- `phase7_spaces_admin/tests/test_acl_write.py` (neu, ~12): hinzufügen · idempotent · `write`
  impliziert `read`, kein Doppel-Eintrag · entfernen aus beiden Listen · leere Liste verschwindet ·
  leere Datei wird entfernt · je Aufruf genau ein Commit · `create_space` lehnt `/`, `.` und
  `_archive` ab · `remove_space_dir` entfernt · `spaces_referencing` findet Verweise ·
  kaputtes YAML wirft (laut), während `AclReader` daneben leer bleibt (fail-closed).
- `phase6_shares/tests/test_spacectl.py` (20 Tests) läuft **unverändert** grün.
- **Charakterisierung (P7-C) vor und nach dem Umbau byte-identisch grün.**

#### C2 — REST-Fläche

**Fünf Routen**, in die Tabelle bei `api.py:743–755`:

```python
Route("/api/v1/spaces", _catch(_spaces_post), methods=["POST"]),
Route("/api/v1/spaces/{space}", _catch(_spaces_delete), methods=["DELETE"]),
Route("/api/v1/spaces/{space}/members", _catch(_space_members_get), methods=["GET"]),
Route("/api/v1/spaces/{space}/members", _catch(_space_members_post), methods=["POST"]),
Route("/api/v1/spaces/{space}/members/{name}", _catch(_space_members_delete), methods=["DELETE"]),
```

**Regeln, für jede der fünf gleich:**

| Regel | Umsetzung |
|---|---|
| Sitzung + CSRF | `await _require_session(request)` + `await _require_csrf_json(request, session)` bei allen schreibenden — wie jeder bestehende Schreibpfad |
| Kill-Switch (P7-R) | `if not settings.space_admin_enabled: raise ApiError("not_found", …)` als **erste** Zeile der schreibenden Handler |
| Autorisierung (P7-L) | `permissions.can_write(session.space, space)` — space-level, nicht item-level |
| Home-Space-Riegel (P7-K) | `_spaces_post` lehnt einen Namen ab, der einem bekannten Principal entspricht; `_spaces_delete` lehnt einen Space ab, der einem bekannten Principal entspricht. **`[VERIFY]` V76:** wie `users: UserDirectory` (bereits Parameter, `api.py:194`) nach der Existenz eines Principals gefragt wird — `userdir.py` lesen, Methode übernehmen, keine erfinden |
| Re-Auth (P7-N) | Mitglied hinzufügen ⇒ ja · Mitglied entfernen ⇒ nein · Space entfernen ⇒ **immer**, plus `confirm == space` im Body |

**`webui/shares.py` — eine Extraktion, kein zweiter Credential-Pfad:**
Die Credential-Hälfte von `require_share_reauth()` (`shares.py:55–65`) wandert in
`_verify_reauth_credentials(session, body, *, users, throttle, auth_store) -> None`. Sowohl
`require_share_reauth()` als auch das neue

```python
def require_space_reauth(session, body: dict, *, widening: bool,
                         users: UserDirectory, throttle: LoginThrottle,
                         auth_store: AuthStore) -> None
```

rufen sie. **Eine Implementierung der Passwort-/TOTP-Prüfung, zwei Tore** — genau wie
`api_routes()` und `account_routes()` sich heute schon `LoginThrottle` teilen (`api.py:196–200`).
`password`/`totp` werden **nie** weitergereicht, an keinen Store-Aufruf (der Advisor-Fund aus P6
Step 7 Commit 5a; ein Leck landete sonst im Frontmatter, Hard Rule 1).

**`GET /api/v1/spaces/{space}/members`** liefert:
```json
{"space": "IT-Sekus-Projekt", "read": ["fabian"], "write": ["niklas"],
 "home": false, "manageable": true, "orphans": []}
```
`orphans` aus `acl.spaces_referencing()` — Namen ohne zugehörigen Space, damit die Oberfläche
zeigt, was `diagnose.sh` Prüfung 12 sonst nur nachts meldet.

**Tests** (`phase7_spaces_admin/tests/test_space_admin_api.py`, neu, ~14):
Mitglied hinzufügen/entfernen als `write`-Mitglied · als Nicht-Mitglied ⇒ `403` · ohne CSRF ⇒
`403` · bei `space_admin_enabled=False` ⇒ `404` · Hinzufügen ohne Credentials ⇒ `403
reauth_required` · mit korrekten ⇒ `200` und `password`/`totp` landen nachweislich nicht in der
`.share.yml` · Entfernen **ohne** Re-Auth erfolgreich · Space anlegen · Name eines bekannten
Principals abgelehnt · reservierter Name abgelehnt · Home-Space entfernen ⇒ `403` · Entfernen ohne
`confirm` ⇒ `400` · Entfernen mit falschem `confirm` ⇒ `400`.

#### C3 — Oberfläche

**Die drei gekoppelten Stellen — in einem Commit, sonst wird die Suite rot:**

| Datei:Zeile | Vorher | Nachher |
|---|---|---|
| `app.html:283` | `<button … id="account-manage-spaces" disabled title="Kommt in Phase 7">Geteilte Spaces verwalten — kommt in Phase 7</button>` | `<button type="button" class="btn" id="account-manage-spaces">Spaces verwalten</button>` |
| `webui/config.py:48–52` | Feldkommentar „kommt erst in Phase 7 zum Tragen" | Kommentar beschreibt den **Kill-Switch**; `space_admin_enabled: bool = True` |
| `test_static_routes.py:135–145` | `test_app_html_has_a_disabled_manage_spaces_stub` (Docstring nennt Phase 7, Assertion prüft `disabled` und den String) | `test_app_html_has_a_live_manage_spaces_entry` — Knopf existiert, trägt **kein** `disabled`, und `"Phase 7"` kommt in `app.html` nicht mehr vor |

**`webui/api.py :: _meta`** (`api.py:255–261`) bekommt `"space_admin": settings.space_admin_enabled`.
+1 Test in `phase5_ui/tests/test_meta.py`.

**Neues Modul `webui/static/js/spaces.js`** (P7-Q) mit:
- `initSpaces(deps)` — Bootstrap-Muster wie alle zehn bestehenden Module.
- `openSpaceAdminDialog()` / `closeSpaceAdminDialog()` — Liste aller Spaces aus `state.spaces`
  mit `writable: true`; je Space Mitglieder (`GET …/members`), je Mitglied ein Entfernen-Knopf,
  darunter ein Hinzufügen-Formular (Name + `read`/`write`).
- `openCreateSpaceDialog()` / `openRemoveSpaceDialog(space)` — letzterer mit Namens-Tippfeld
  (P7-N) und dem Klartext, was passiert: *„N Items wandern in deinen Space `niklas` und werden dort
  archiviert. Der Space `X` selbst verschwindet. Die Zuordnung ist danach weg."*
- Re-Auth-Mini-Formular **nach dem etablierten Muster**: erste Fassung des Bodys beim ersten
  Absenden einfrieren (`pendingSpaceBody`), nur `password`/`totp` bei jedem Retry frisch lesen —
  wie `dialogs.js :: openShareDialog()` und `openMoveDialog()` es seit P6 Step 7 tun.
- Home-Spaces erscheinen in der Liste, aber **ohne** Entfernen-Knopf (P7-K).

**`app.js`**: `initSpaces(...)` in den Bootstrap; `#space-admin-dialog` in `anyOverlayOpen()` und
die Escape-Behandlung — dieselbe dokumentierte Abweichung wie bei jedem Dialog seit Step 7
Commit 3.

**`app.html`**: `#space-admin-dialog`-Hülle als Geschwister von `#share-dialog`; `pw-field`/
`pw-toggle`-Klassen benutzen, dann greift `initPasswordToggles()` ohne neuen JS-Code.
**Gleicher Commit: `.rail__version` auf `v2.2`** (P7-U).

**`[VERIFY]` V77:** `ui_budget.py` zählt die JS-Nutzlast über einen `js/*.js`-Glob (seit P6 Step 7
Commit 0) — ein elftes Modul zählt automatisch mit. Nach C3 einmal `ui_budget.py --json` gegen ein
temporäres `DATA_ROOT` fahren und prüfen, dass `all_within_budget` weiterhin `true` ist.

**Tests:** JS bleibt ungetestet (P5-T); Verifikation per Playwright/Browser gegen eine
Wegwerf-Instanz. `test_static_routes.py` und `test_meta.py` ziehen nach.

#### C4 — Space entfernen, zweiphasig (P7-O, N8/N9)

Der Algorithmus in `webui/api.py :: _spaces_delete`. **Die Orchestrierung hält zu keinem Zeitpunkt
den `.write.lock`** (P7-M) — jeder Aufruf sperrt für sich.

```
 0. home = session.space
    if space ist ein bekannter Principal  -> 403 (P7-K)
    if not permissions.can_write(home, space) -> 403 (P7-L)

 1. VORLAUF — kein Schreibvorgang, kein Commit:
    # VOLLSTÄNDIG aufzählen, nicht eine Seite. `_STORE_FETCH_LIMIT = 5000` (api.py:144) ist
    # eine echte Obergrenze, kein Seitenmaß: `_items_get` reicht sie an `store.search()` und
    # schneidet danach in Python. Ein einzelner Aufruf über einem großen Space prüfte sonst
    # eine Teilmenge, meldete "sauber", der Durchlauf verschöbe nur diese Teilmenge — und
    # Schritt 4 rmtree'te den Rest. Genau der Datenverlust, den N8/N9 verhindern sollen.
    items, offset = [], 0
    while True:
        page = store.search(space=space, limit=_STORE_FETCH_LIMIT, offset=offset)
        items += page.items
        offset += len(page.items)
        if len(items) >= page.total or not page.items: break
    total = len(items)

    blockers = [i.id für jedes i, für das
                permissions.can_write_item_as_human(home, store.acl_of(i.id)) falsch ist]
    if blockers: -> 403, Liste der IDs im Text, NICHTS wurde bewegt      (N9)

 2. require_space_reauth(..., widening=True)   # Entfernen: immer  (P7-N)
    if body.get("confirm") != space: -> 400

 3. DURCHLAUF, Item für Item:
    it = store.move(i.id, version=i.version, space=home, folder="")
    store.archive(it.id, version=it.version)
    -> zwei Git-Commits je Item, das ist der Preis von N8 und wird nicht wegoptimiert
    Bei ConflictError mitten im Lauf: ABBRUCH, Bericht, Space bleibt stehen.
    Die bereits verschobenen Items bleiben verschoben — ein Rollback existiert
    nicht, weil Git-Commits sich nicht zurücknehmen lassen. Der Bericht nennt
    beide Listen (verschoben / verblieben) namentlich.

 4. HARTE SPERRE VOR DEM rmtree:
    if archived != total: -> Abbruch, Verzeichnis bleibt stehen, Bericht.
    Das Verzeichnis fällt NUR, wenn jedes gezählte Item nachweislich umgezogen und
    archiviert ist. Diese Zeile ist der letzte Schutz gegen jeden Zählfehler
    weiter oben — sie wird nicht wegoptimiert, auch wenn sie redundant aussieht.
    acl.remove_space_dir(data_root, space)     # rmtree + ein Commit

 5. Antwort: {"removed": space, "archived": N, "orphan_refs": [...]}
```

**Warum `move()` dann `archive()` und nicht umgekehrt:** `store.archive()` (`store.py:578–599`)
setzt `folder=""` und legt die Datei unter `<space>/_archive/` ab — ein danach ausgeführter
`move()` würde sie an der Wurzel des Zielspace absetzen, nicht in dessen Archiv. `store.move()`
(`store.py:601`) zieht das Asset-Verzeichnis `_assets/<item_id>/` **innerhalb derselben
Lock-Sektion** mit, ein Move bleibt also ein Commit. Die Reihenfolge ist damit erzwungen, nicht
gewählt.

**Was mit dem `rmtree` stirbt** — hier stehen, weil es sonst niemand prüft: der Inhalt von
`<space>/_assets/<item_id>/_trash/` (bereits entfernte Bilder) und `_assets/`-Reste zu Items, die
es nicht mehr gibt. Beides ist Müll und in der Git-Historie des `DATA_ROOT` weiterhin vorhanden.
Leere Ordner im Space verschwinden mit demselben `rmtree`, `_cleanup_emptied_folders()` wird dafür
nicht gebraucht.

**Tests** (`phase7_spaces_admin/tests/test_space_removal.py`, neu, ~8):
Vorlauf blockiert bei einem nicht schreibbaren Item und bewegt **nichts** · Vorlauf sauber ⇒ alle
Items liegen danach unter `<home>/_archive/` · Assets wandern mit · zwei Commits je Item · genau
ein `remove-space`-Commit · Verzeichnis ist weg · `ConflictError` mitten im Lauf ⇒ Abbruch, Space
steht noch, Bericht nennt beide Listen · Home-Space ⇒ `403` vor jedem Schreibvorgang.

#### C5 — Betrieb und Doku

- `phase3_edge/scripts/diagnose.sh` Prüfung 12 (`spacectl.py check --json`) bleibt unverändert —
  sie prüft jetzt zusätzlich das Ergebnis einer Fläche, die Menschen bedienen. Ein Satz im
  Prüfungstext, mehr nicht.
- `docs/UPDATE_LOG.md`: Eintrag für die neue Fläche, datiert auf den Deploy-Tag.
- `phase7_spaces_admin/CLAUDE.md`: Modul-Tabelle, Abnahmestand.

---

### Block B — Mehrfachauswahl (fällt unter Druck zuerst)

**`phase6_shares/ITEM_MOVE_PLAN.md` §9 ist der Plan** (P7-S). Entscheidungen **P6-AK–P6-AN** sind
gelockt; dieser Abschnitt liefert nur die Anker gegen den heutigen Code.

| §9-Punkt | Wo im Code |
|---|---|
| 9.3 Punkt 1 — Auswahl in `state.selectedItemIds` (neues `Set`) | `webui/static/js/state.js` (112 Zeilen, einzelnes mutierbares Objekt) |
| 9.3 Punkt 1 — Modifier-Klasse `.list__row--selected` | `list.js :: renderList()`, Zeilenbau ab `list.js:241`; `<li>` ist bereits Flex (`app.css`, seit Step 7 Commit 3) |
| 9.3 Punkt 1 — Navigation leert die Auswahl | `tree.js :: navigate()` / `navigateFolder()`, dieselbe Exklusivitätsdisziplin wie `state.folder`/`state.filter` |
| 9.3 Punkt 2 — Auswahl-Werkzeugleiste | neu in `app.html` unter `#list-chips` (`app.html:52`) |
| 9.3 Punkt 2 — Dialog mit `moveTargetItems` statt `moveTargetItem` | `dialogs.js :: openMoveDialog()` |
| 9.3 Punkt 3 — `moveSelectedItems(items, {space, folder})` | neu in `list.js`, neben dem bestehenden `moveItemToFolder()` (`list.js:163`) — **derselbe** `PATCH`-Pfad, kein neuer Endpunkt (P6-AL) |
| 9.3 Punkt 4 — Sammel-Toast mit namentlichen Fehlern | `toasts.js` |

**Zweirunden-Logik (P6-AM), wörtlich:** Runde 1 schickt alle N Requests **ohne** Credentials. Kommt
mindestens ein `403 reauth_required`, zeigt die Oberfläche **ein** gemeinsames Re-Auth-Formular;
Runde 2 wiederholt **ausschließlich** die zurückgewiesenen. Items, die in Runde 1 durchgingen,
werden nicht erneut angefasst. Sequenziell, nicht parallel — `LoginThrottle` ist dieselbe Bremse
wie beim UI-Login.

**Tests:** keine neue Backend-Testdatei (§9.4). Playwright-Sichtprobe: 3+ Items · Batch ohne
Widen (kein Formular) · Batch mit genau einem Widen-Item (genau ein Formular) · ein absichtlich in
Konflikt gebrachtes Item mittendrin (Batch läuft weiter, taucht namentlich auf). `pytest`
unverändert.

---

### Step Z — Abnahme, Deploy, Abschluss

**Vor dem Deploy, in dieser Reihenfolge:**

1. `phase3_edge/scripts/diagnose.sh` **frisch** — nicht auf einen früheren Lauf vertrauen.
   Handover §5.5: der Funnel überlebte am 2026-08-19 einen Reboot nicht sauber; Prüfung 5 erkennt
   den Zustand jetzt, **heilt ihn aber nicht**. Bei Befund: `sudo systemctl restart tailscaled`.
2. `docs/UPDATE_LOG.md` — oberster Eintrag auf den **Deploy-Tag** datiert, sonst bricht
   `deploy.sh` ab (P6-X). Das ist kein Formalismus, das ist ein Gate im Skript.
3. `pytest -q` grün · `mcp_smoke.py` · `ui_smoke.py` · `ui_budget.py --json`
   (`all_within_budget: true`, V77).
4. Tabu-Diff: `git diff` auf die Liste aus §0.3 ist leer.
5. `deploy.sh` — **der Neustart braucht Sudo, also den Nikinger** (Präzedenz seit dem
   Steps-4–6-Cutover).

**Nach dem Deploy:** Abnahmematrix §6 durchgehen, jede Zeile mit Beleg. **✅ heißt
live-verifiziert, nicht gebaut** — die Regel, an der P6 ehrlich geblieben ist.

**Phasenabschluss:** `PHASE7_CLOSEOUT_HANDOVER.md`, `phase7_spaces_admin_uebersicht.svg`
(rendern und ansehen), Rotationsprüfung, ROADMAP/Root-`CLAUDE.md`/`INDEX.md` — alles in einem
Commit. **Und die Neubewertung von Phase 6:** nach A7 und Block B sind die Zeilen 18, 24, 31–34,
36, 37 erreichbar; ob P6 damit von 🟡 auf ✅ geht, ist und bleibt eine **Nikinger-Entscheidung**
(Handover §5.2), keine Rechnung.

---

## §5 Testliste (Soll)

| Datei | Δ | Inhalt |
|---|---|---|
| `phase5_ui/tests/test_api.py` | +6 | 4 × ID-Lookup (A1), 2 × Feld-Whitelist (A4) |
| `phase2_mcp/tests/test_tools.py` | +1 | Beschreibungssatz in vier Tools (A2) |
| `phase7_spaces_admin/tests/test_testcred.py` | +7 | Testnutzer-Zugang, inkl. Meta-Test gegen freie Schlüsselwahl (A7b) |
| `phase7_spaces_admin/tests/test_acl_write.py` | +12 | Schreibseite `.share.yml` (C1) |
| `phase7_spaces_admin/tests/test_space_admin_api.py` | +14 | fünf Routen, Rechte, Re-Auth, Kill-Switch (C2) |
| `phase7_spaces_admin/tests/test_space_removal.py` | +8 | Vorlauf/Durchlauf, Archivierung, Abbruch (C4) |
| `phase5_ui/tests/test_static_routes.py` | ±0 | ein Test umgeschrieben (C3) |
| `phase5_ui/tests/test_meta.py` | +1 | `space_admin` im Meta-Payload (C3) |
| `phase5_ui/tests/test_api.py` (C3) | +1 | `UiSettings().space_admin_enabled is True` — der **Default**, der ausgeliefert wird. Ohne diese Zeile kann Block C komplett hinter einem `False` versenden, und keine Testsuite merkt es; die `_env()`-Helfer-Erfahrung aus P6-X zeigt, dass genau solche Defaults hier schon einmal still überschrieben wurden |
| `phase6_shares/tests/test_spacectl.py` | ±0 | **muss unverändert grün bleiben** — Regressionsbeweis der Extraktion |
| `phase6_shares/tests/test_characterization.py` | ±0 | vor und nach C1 byte-identisch (P7-C) |

**Erwartetes Ziel: rund 878 Tests** (Ausgangsstand V71 + 50). Die Zahl ist eine Erwartung, keine
Vorgabe — **gezählt wird am Ende, nicht gerechnet.**

**Kein Unit-Test für JS/CSS/HTML** (P5-T gilt fort). Deren Nachweis ist die echte Browserprobe,
und die wird gesehen, nicht behauptet.

---

## §6 Abnahmematrix (P7-1 – P7-24, plus P7-12b)

**Statusregel wie in P4/P5/P6/6.5: ✅ heißt live-verifiziert durch einen Menschen, nicht „gebaut".**
Der laufende Stand lebt im Phase-Head, nicht in diesem Snapshot.

### Block A

| # | Kriterium | Wer |
|---|---|---|
| **P7-1** | Ein Item zeigt seine `itm_…`-ID in der Nur-lesen- **und** in der Editor-Ansicht; ein Klick kopiert sie | Niklas |
| **P7-2** | Eine Suche nach einer echten `itm_…`-ID findet genau dieses Item — auch wenn gerade ein anderer Space oder Ordner aktiv ist | Niklas |
| **P7-3** | Eine ID-Suche nach einem Item, das der Suchende nicht lesen darf, liefert eine **leere Liste** — keinen Fehler, kein Existenz-Orakel | Claude Code, Test + `testnutzer-p7` |
| **P7-4** | Eine frische Claude-Instanz nennt in einem Gespräch Items beim **Titel**, nicht bei der ID | Niklas, echter Connector |
| **P7-5** | Ein Bild lässt sich im Editor entfernen; die Referenz rendert danach als Alt-Text; die Datei liegt unter `_assets/<item_id>/_trash/` (**schließt P6.5-12**) | Niklas |
| **P7-6** | `PATCH /api/v1/items/{id}` mit `spce` (Tippfehler) wird abgewiesen, die Datei bleibt unverändert (**schließt O6**) | Claude Code, Test |
| **P7-7** | Speichern, Verschieben und Freigeben über die Oberfläche funktionieren nach der Whitelist unverändert | Niklas |
| **P7-8** | Migration gelaufen: **0** `.md`-Dateien ohne `visibility:` (**P6-Zeile 8, erste Hälfte**) | Nikinger führt aus, Claude Code prüft |
| **P7-9** | `clients`/`token_families` sinken nach einem realen Purge-Lauf (**P6-Zeile 4**, ab 2026-08-28) | Niklas |
| **P7-10** | `testnutzer-p7` existiert, hat Konto, Space und eigenen Connector und schreibt einmal (**P6-Zeile 18**) | Nikinger + Claude Code |
| **P7-11** | `testnutzer-p7` sieht ein **nur item-level** freigegebenes Item — und **nur** dieses (**P6-Zeilen 36/37**) | Claude Code |
| **P7-12** | `testnutzer-p7` wieder entfernt, **Keyring-Eintrag `p7-testcred` ist weg** (`testcred.py purge`), `spacectl.py check` und `diagnose.sh` melden keine verwaisten Freigaben (**P6-Zeile 24**) | Claude Code |
| **P7-12b** | Claude Code meldet sich **ohne Nikinger** als `testnutzer-p7` an — Login, TOTP und ein Re-Auth-Gate — allein über `testcred.py`; das Skript verweigert nachweislich jeden anderen Principal | Claude Code |
| **P7-13** | Phase 6.5 formal abgeschlossen: Handover, Übersichtsgrafik, Status, P1-Contract geschlossen und sechste Öffnung benannt | Claude Code |

### Block C

| # | Kriterium | Wer |
|---|---|---|
| **P7-14** | Ein Mensch gibt seinen **eigenen** Space im Browser für einen anderen zum Lesen frei; der andere sieht ihn danach, ohne dass jemand SSH benutzt hat | Niklas + `testnutzer-p7` |
| **P7-15** | Dieselbe Freigabe zurücknehmen verlangt **kein** Re-Auth; sie erweitern verlangt eines (P6-N/P7-N) | Niklas |
| **P7-16** | Ein neuer geteilter Space wird im Browser angelegt und erscheint im Baum | Niklas |
| **P7-17** | Ein Space-Name, der einem bestehenden Principal entspricht, wird beim Anlegen abgewiesen | Claude Code, Test |
| **P7-18** | Ein Home-Space lässt sich über die Oberfläche **nicht** entfernen — der Knopf fehlt und die Route antwortet `403` | Claude Code, Test + Browser |
| **P7-19** | Ein geteilter Space mit N Items wird entfernt: alle N Items liegen danach im `_archive/` des Ausführenden, die Bilder sind mitgewandert, das Verzeichnis ist weg | Niklas |
| **P7-20** | Ein Space mit einem für den Ausführenden **nicht schreibbaren** Item lässt sich nicht entfernen — und es wurde dabei **kein einziges** Item bewegt (P7-O/N9) | Claude Code, Test |
| **P7-21** | Space entfernen ohne getippte Namensbestätigung wird abgewiesen | Claude Code, Test |
| **P7-22** | `space_admin_enabled=False` lässt den Menüpunkt verschwinden und alle fünf Routen `404` antworten | Claude Code, Test |

### Block B

| # | Kriterium | Wer |
|---|---|---|
| **P7-23** | N ausgewählte Items wandern in einem Vorgang in dasselbe Ziel; ein `move`-Commit je Item (**P6-Zeilen 31/33**) | Niklas |
| **P7-24** | Eine Auswahl mit genau einem rechteerweiternden Item verlangt **ein** Formular, nicht N; eine reine In-Space-Auswahl verlangt keines (**P6-Zeilen 32/34**) | Niklas |

**Geerbt und in dieser Phase nicht adressiert:** P6-Zeilen 7, 9, 14–17, 23, 25, 29, 30 sowie
P6.5-14. Sie bleiben im Handover offen — **kein stilles Abhaken.**

---

## §7 `[VERIFY]`-Register

Fortsetzung ab **V71** (Phase 6.5 belegt V59–V70, siehe deren Plan §7 und Handover §6.2).

| # | Was | Wann prüfen |
|---|---|---|
| **V71** | Realer `pytest`-Ausgangsstand (Erwartung **828**) | Step 0.1, vor der ersten Änderung |
| **V72** | Wie die bestehenden `test_tools.py`-Tests an Tool-Beschreibungen kommen | vor A2 — Muster von Phase 6.5 übernehmen, keines erfinden |
| **V73** | Was `markdown.js :: markdownToHtml()` mit einer `asset:`-Referenz ohne existierendes Asset macht | vor A3 — entscheidet, ob ein Alt-Text-Fallback nötig ist |
| **V74** | Welche Schlüssel die Oberfläche im PATCH-Body tatsächlich sendet | **vor** A4 — die Whitelist muss eine Obermenge sein, sonst bricht das Speichern |
| **V75** | Ob Einladung, Enrollment und `create-space` einen Bindestrich im Space-Namen tragen | vor A7 — gegen eine **Wegwerf-Instanz**, nicht am echten `DATA_ROOT` |
| **V76** | Wie `UserDirectory` nach der Existenz eines Principals gefragt wird | vor C2 — `userdir.py` lesen, Methode übernehmen |
| **V77** | `ui_budget.py --json` nach dem elften JS-Modul weiterhin `all_within_budget: true` | nach C3 |
| **V78** | Ob `_STORE_FETCH_LIMIT` weiterhin `5000` ist (`api.py:144`, Stand dieser Planung) und `search()` weiterhin `total` unabhängig von `limit` liefert | vor C4. **Kein offener Entwurf mehr** — die Gegenmaßnahme steht bereits als Schleife + `archived == total`-Sperre in §4.C4; hier wird nur der angenommene Wert gegengelesen |
| **V79** | MCP-Revision `2026-07-28` / `fastmcp 4` — ob der Connector weiterhin auf `fastmcp 3.4.4` spricht | **nicht in P7.** Gehört laut **P5-C** in eine eigene Mini-Phase. Nur beobachten, nichts bauen |
| **V80** | Ob der Keyring aus der Umgebung von Claude Code heraus ohne Desktop-Session les- **und** schreibbar ist | vor A7b — mit einem **Wegwerf-Schlüssel** probieren, nie mit `auth-dek` oder `auth-users` |

---

## §8 Geerbte offene Posten (Ledger — damit nichts still verschwindet)

| Posten | Herkunft | Stand bei Planungsschluss |
|---|---|---|
| **V12/V49** — Uplink-Datenlimit, mit und ohne Assets | P3 bzw. P6 | **offen seit Phase 3**, nie bewertet |
| **V64** — ob claude.ai aus `destructiveHint: True` eine wiederholte Zustimmung macht | 6.5 | offen, Client-Verhalten, nicht zusagbar |
| **`filename`-Persistenzfrage** | 6.5 | offen |
| **`test_authctl.py`-Flake** | 6.5 | offen — bei einem roten Lauf **erst prüfen, ob es dieser ist**, bevor irgendetwas „repariert" wird |
| **O4** — verwaiste Assets bleiben liegen | P6 Plan §0.5 | teilweise durch den `_trash/`-Weg adressiert; **P7 räumt weiterhin nicht auf** |
| **O5** — kein EXIF-Strippen | P6 Plan §0.5 | offen, bewusst |
| **O6** — unbekannte Schlüssel landen still im Frontmatter | `ITEM_MOVE_PLAN.md` §112 | **wird in A4 geschlossen** |
| **O7** — leere Ordner überleben einen Move | `ITEM_MOVE_PLAN.md` §118 | Code existiert (`_cleanup_emptied_folders()`), nie live geprüft |
| **Kein UI-Rückweg aus einem geteilten Space** (Verschieben/Freigeben nur im eigenen Space sichtbar) | `list.js`, P6 | als „kein Bug, nicht blockierend" eingestuft — bleibt so |
| **`GET /api/v1/overview` kostet ~440–490 ms** und wird von jedem offenen Tab alle 20 s gepollt (`app.js:190`) | P6-S, in dieser Planungssession im Journal wiedergesehen | bekannte Kostenstelle, **kein Auftrag** — `Store.search()` liest je Aufruf jede indizierte Datei |
| **Funnel-Watchdog** | P3, Handover §5.5 | bewusst offene Entscheidung; P7 fährt `diagnose.sh` vor jedem Deploy |

---

## §9 Risiken

1. **Selbst-Deadlock über `.write.lock`** — der wahrscheinlichste Weg, Block C still kaputtzumachen.
   Gegenmaßnahme: P7-M, plus ein Kommentar an der Lock-Hilfsfunktion, der den Grund nennt.
2. **Ein halb entfernter Space.** Gegenmaßnahme: P7-O (Vorlauf), plus die ehrliche Ansage im
   Fehlerfall — es gibt keinen Rollback, Git-Commits sind endgültig.
3. **Die Migration erzeugt 73 Commits in der echten Historie.** Bewusst entschieden (N4), nicht
   rückgängig zu machen. Gegenmaßnahme: Dry-Run zuerst, Ausführung durch den Nikinger.
4. **Die Extraktion in C1 verändert `spacectl.py`s Verhalten unbemerkt.** Gegenmaßnahme: die 20
   bestehenden Tests müssen **unverändert** grün bleiben; Ausgabetexte und Exit-Codes byte-identisch.
5. **Drei gekoppelte Stellen für den Phase-7-Seam.** `app.html:283`, `config.py:48–52`,
   `test_static_routes.py:135–145` — wer zwei davon findet, bekommt eine rote Suite. Stehen
   deshalb als Tabelle in §4.C3, nicht in einem Fließtext.
6. **`testcred.py` ist ein Skript, das ein echtes Geheimnis herausgibt.** Gegenmaßnahme: harte
   Verdrahtung auf einen einzigen Principal und einen einzigen Keyring-Schlüssel (P7-W), ein
   Meta-Test, der genau das festhält, und `purge` als Pflichtzeile der Abbau-Checkliste. **Der
   Fehlermodus, auf den zu achten ist, ist nicht das Skript selbst, sondern seine Verallgemeinerung**
   — jemand ergänzt „nur schnell" ein `--space`, und aus einem Testhelfer wird ein
   Auslesewerkzeug für jedes Konto.
7. **Die Phase ist groß.** Vier Blöcke, zwei davon mit echtem Deploy-Risiko. Gegenmaßnahme: die
   Fall-Reihenfolge A > C > B ist im Kopf dieses Dokuments **und** im Phase-Head verankert. Ein
   Weglassen von B ist geplant und kein Scheitern.

---

## §10 Was dieser Plan nicht tut

- **Er baut keinen Eigentümerbegriff.** N7 hat sich dagegen entschieden; die Kehrseite steht in
  §0.4 Punkt 1 und wird nicht durch einen Guard geglättet, den niemand bestellt hat.
- **Er migriert nicht auf die MCP-Revision `2026-07-28`.** P5-C reserviert das als eigene
  Mini-Phase, und der Connector funktioniert nachweislich.
- **Er löscht keine Items.** F2 bleibt draußen. Auch beim Entfernen eines Space wird archiviert,
  nie gelöscht — nur das leergeräumte Verzeichnis fällt.
- **Er fasst `store.search()` nicht an.** Weder für die ID-Suche (P7-D) noch für die
  `_overview`-Kostenstelle (P6-S bleibt eine Messung, kein Auftrag).
- **Er baut keinen Funnel-Watchdog** und ersetzt `diagnose.sh` nicht durch Selbstheilung.
- **Er paraphrasiert `ITEM_MOVE_PLAN.md` §9 nicht.** Zwei Fassungen derselben Regel sind schlimmer
  als eine, die man aufschlagen muss.
