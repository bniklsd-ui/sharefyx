---
status: live
purpose: Zusatzplan P6 — Item-Verschieben zwischen Ordnern UND Spaces (Storage/MCP/REST/UI) plus Lesbarkeitsfix der Textfarben-Token
read-when: vor P6 Step 7 / 7a / 7b, oder sobald Item-Verschieben, `Store.update(folder=)` oder `--text-muted`/`--text-faint` berührt werden
detail: L2
up: ./CLAUDE.md
down:
  - ../docs/concepts/phase6_shares_plan.md    # Hauptplan der Phase, P6-A–P6-AC, Steps 0–10 — dieser Plan hängt an Step 7
  - ../phase1_storage/CLAUDE.md               # "Geerbte Contracts" — dritte, benannte Öffnung, hier fortgesetzt
  - ../phase5_ui/CLAUDE.md                    # Designsystem-Herkunft der Farbtoken (§4.1/§4.3, Step 7b revidiert)
updated: 2026-08-17 — P6-AD–AJ gelockt (Nikinger-Freigabe, „planning session light"), V52–V55 gegen den echten Step-7-Code geschlossen, Guard-Routing-Fund in §4.2/§4.3 präzisiert, neues §9 Mehrfachauswahl (P6-AK–AN) + Abnahmezeilen 31–34. Ursprung 2026-08-13: erstellt (Nikinger-Auftrag: Item-Verschieben fehlt, UI dafür fehlt, Grautext schlecht lesbar)
---

# Zusatzplan P6 — Item verschieben, und die Textfarben

> **Für den ausführenden Sonnet.** Dieses Dokument ist ausführungsreif und **gegen den echten
> Code vom 2026-08-13 (`main`@`92b918b`) verifiziert**, nicht gegen einen Snapshot. Jede Aussage
> in §1 ist entweder gelesener Code oder ein protokollierter Probelauf — beides mit Fundstelle.
> **Quelle der Wahrheit bleibt trotzdem der Code**, nicht dieser Plan.
>
> Der Hauptplan der Phase (`../docs/concepts/phase6_shares_plan.md`) bleibt als 📕-Snapshot
> unverändert. Dieser Plan **ergänzt** ihn an Step 7 und erfindet nichts neu, was dort schon steht.

---

## §0 Bottom line

Verschieben **innerhalb** eines Space ist auf allen drei Schichten längst gebaut und getestet —
die Vormerkung vom 2026-08-13 hat das zu pessimistisch beschrieben. Was wirklich fehlt, sind zwei
Dinge: **Verschieben über Space-Grenzen** (existiert nirgends) und **jede Bedienung dafür in der
Oberfläche** (die UI kennt echte Ordner überhaupt nicht — ihre „Ordner" im Baum sind die vier
Buckets Notizen/Aufgaben/Erledigt/Archiv). Dazu ein unabhängiger Lesbarkeitsdefekt: ein
Farbtoken der UI liegt messbar unter WCAG AA.

Drei Schnitte, in dieser Reihenfolge unabhängig lieferbar:

| Schnitt | Was | Hängt ab von | Umfang |
|---|---|---|---|
| **Step 7a** | Textfarben-Token anheben | nichts — jederzeit lieferbar | 4 Zeilen CSS + Nachtrag (Wortmarke/Versionen weiß, `v2.1`) — ✅ **gebaut 2026-08-13, Deploy beim Nikinger** (`phase6_shares/CLAUDE.md` Session-Block) |
| **Step 7** | *(bestehend, Hauptplan)* echte Ordner in der UI, Verschieben per Menü/Drag & Drop | Steps 4–6 (live) | groß, unverändert |
| **Step 7b** | Verschieben über Space-Grenzen, alle Schichten + UI | Step 7 | mittel |

---

## §1 Befundlage gegen den echten Code

### 1.1 Was auf welcher Schicht existiert

| Schicht | Ordner-Move (innerhalb Space) | Space-Move (über Grenzen) | Fundstelle |
|---|---|---|---|
| `storage` | ✅ **gebaut** | ❌ fehlt | `store.py:475-480`, `_write_item_file():275-290` |
| MCP-Tools | ✅ **gebaut**, Eigentümer-only | ❌ fehlt (kein `space`-Parameter) | `tools.py:482`, `tools.py:514-520` |
| REST-API | ✅ **gebaut**, Eigentümer-only | ❌ fehlt | `api.py:393-398`, `api.py:400` |
| Web-UI | ❌ **fehlt vollständig** | ❌ fehlt | `app.js` — `folder` kommt nur als CSS-Klasse `tree__folder` vor |

### 1.2 Vier Korrekturen an der Vormerkung vom 2026-08-13

Die Planungsvormerkung im aktuellen Session-Block des Phase-Heads sagt „geprüft und bestätigt
fehlend auf allen drei Schichten". Gegen den Code nachgeprüft ist das in dieser Form **falsch** —
festgehalten als datierte Korrektur, nicht durch Umschreiben des alten Textes:

- **K1 — `Store.update(folder=…)` verschiebt real.** Der Probelauf gegen ein Wegwerf-`DATA_ROOT`
  legt ein Item an, ruft `update(folder="projekte/alpha")` und findet die Datei danach unter
  `niklas/projekte/alpha/…md`. `files.validate_folder()` hält Tiefe > 2 und reservierte Namen
  (`_archive`/`_assets`) mit `ValidationError` ab. Das ist genau das, was Hauptplan §1.3
  ankündigt — es ist in Step 4 gebaut worden, 20 Tests in `phase1_storage/tests/test_store.py`.
- **K2 — `Store.update(space=…)` scheitert laut, nicht still.** Die Vormerkung sagt, ein
  unbekannter Schlüssel lande „stillschweigend als beliebiges Extra-Frontmatter-Feld statt eines
  Fehlers". Für `space` stimmt das nicht: `space` steht in `_SYSTEM_MANAGED_FIELDS`
  (`store.py:43`), und `update()` wirft dafür `ValidationError: Feld 'space' ist vom Store
  verwaltet, nicht änderbar` (`store.py:471-472`). Still-als-Extra passiert nur bei einem echten
  **Tippfehler** (`spce="fabian"` → `extra={'spce': 'fabian'}`) — ein realer, aber anderer Befund,
  siehe O6 unten.
- **K3 — die UI kennt keine echten Ordner.** Nicht „die UI kann nicht verschieben", sondern eine
  Ebene davor: `app.js :: renderFolders()` (`app.js:565`) rendert die vier **Buckets** aus
  `state.meta.buckets`, nicht Verzeichnisse. `GET /api/v1/overview` liefert überhaupt kein
  `folders`-Feld (`api.py:272-280`) — nur `GET /api/v1/spaces` tut das (`serializers.py:114`),
  und diese Antwort benutzt der Baum nicht. Ein „Verschieben"-Knopf hätte heute kein Ziel.
- **K4 — Menschen können nicht einmal *in* einen Ordner anlegen.** `_items_post` filtert den
  Request-Body auf `{"status","due","tags","links","format"}` (`api.py:340-344`) — `folder` ist
  nicht dabei. Über MCP geht es (`create_item(folder=…)`, `tools.py:428`). Die Agentenfläche kann
  also seit Step 5 etwas, das die Menschenfläche nicht kann. Das gehört in Step 7 mitgeschlossen.

### 1.3 Der Fund, der Step 7b klein macht

`Store._write_item_file(item, old_path=…, op=…)` (`store.py:275-290`) berechnet den Zielpfad aus
`item.space` **und** `item.folder`, schreibt zuerst an den alten Pfad, verschiebt dann per
`files.move_file()` und indiziert die Zieldatei neu. Es hat nie ein `Item` mit geändertem `space`
gesehen — es verarbeitet eines aber vollständig korrekt.

Protokoll des Probelaufs (Wegwerf-`DATA_ROOT`, `_write_item_file` mit
`replace(item, space="fabian", folder="")` aufgerufen):

```
neuer Pfad:            fabian/itm_41afee60__umzug.md
Frontmatter space:     space: fabian          # mitgezogen, keine Divergenz Pfad↔Datei
get()                → space='fabian' folder='' version=2
acl_of()             → space='fabian' folder=''
search(space=fabian) → 1     search(space=niklas) → 0
git log -1           → move itm_41afee60 [fabian]
git show --stat -M   → {niklas/alt => fabian}/itm_41afee60__umzug.md   # Rename erkannt
Reste                → niklas/alt   (leeres Quellverzeichnis bleibt liegen)
```

**Konsequenz für den Zuschnitt:** Step 7b braucht in `storage/` keinen neuen Schreibpfad, keine
neue Atomarität und keine Git-Sonderbehandlung — nur eine öffentliche Methode, die ein `Item` mit
neuem `space` baut und den bestehenden Pfad aufruft. Der teure Teil liegt in der Rechteprüfung und
in der UI, nicht im Dateisystem.

### 1.4 Zwei offene Nebenbefunde (aus den Probeläufen, nicht aus dem Plan)

- **O6 — unbekannte `update()`-Schlüssel landen still im Frontmatter.** `spce="fabian"` erzeugt
  ein Extra-Feld statt eines Fehlers (`store.py:491-492`). Das ist bewusste Round-Trip-Treue aus
  P1 (unbekannte Felder überleben, Hard Rule „Round-Trip-Treue ist Pflicht") und **kein Bug** —
  aber es heißt, dass ein Tippfehler im Ziel-Parameter eines Moves lautlos ins Frontmatter
  wandert. Deshalb bekommt Step 7b eine **benannte Signatur** (`move(item_id, *, version, space=,
  folder=)`) statt `**changes` — dort ist ein Tippfehler ein `TypeError` beim Aufruf.
- **O7 — leere Ordner überleben einen Move.** Nach `folder="alt/tief"` → `folder="neu"` liegen
  `niklas/alt` und `niklas/alt/tief` weiter auf der Platte, und `Store.list_spaces()` meldet sie
  weiter als Ordner (`store.py:316-321` — reiner Verzeichnis-Walk). Git sieht davon nichts (Git
  kennt keine leeren Verzeichnisse), die UI aus Step 7 würde Geisterordner anzeigen. Behandlung:
  siehe P6-AF.

---

## §2 Neue Entscheidungen (P6-AD – P6-AJ)

Fortsetzung der Nummerierung aus Hauptplan §0.5 (dort endet sie bei P6-AC). Diese sieben sind
**Vorschläge dieses Plans** und werden mit der Nikinger-Freigabe dieses Dokuments gelockt.

**[2026-08-17 gelockt.]** Der „Nächster Schritt" der Planungssession vom 2026-08-13 (Fünfter
Session-Block, `SESSIONS_ARCHIVE.md`) stand seit Verfassung dieses Dokuments offen — die
Session, die Step 7a baute, war explizit auf `ITEM_MOVE_PLAN.md` §3 verengt, keine Session
dazwischen hat P6-AD–AJ freigegeben, und root-`CLAUDE.md`s „Noch nicht entschieden" trug den
Punkt bis heute unverändert seit 2026-08-13. Vor dem Bauen ausdrücklich geprüft statt
übernommen (dieselbe Kategorie wie die Doku-Status-Regel „✅ heißt live-verifiziert, nicht
gebaut" — hier umgekehrt: eine Entscheidung ist erst gelockt, wenn eine Freigabe dokumentiert
ist, nicht weil sie plausibel aussieht). **Nikinger-Freigabe dieser Session (2026-08-17,
„planning session light"):** „I confirm we can work on all points." — gilt als Freigabe dieses
gesamten Dokuments einschließlich §2. **P6-AD–P6-AJ sind ab hier gelockt.** Root-`CLAUDE.md`s
„Noch nicht entschieden"-Eintrag wird im selben Commit entfernt/ersetzt.

- **P6-AD — eigene Methode `Store.move()`, kein Feld an `update()`.** `space` bleibt in
  `_SYSTEM_MANAGED_FIELDS`. *Warum:* der Schutz dort ist tragend — er verhindert genau den
  Zustand, den Fund B2 der P2-Adapter-Abnahme real erzeugt hat (Verzeichnis sagt `niklas`,
  Frontmatter sagt `nikinger`, per Hand mit `sed` repariert). Ein Move ist kein Feld-Update,
  sondern eine Relokation mit eigener Rechtefrage; er verdient einen eigenen Namen im Log
  (`move`), im Tool und im Fehlertext.
- **P6-AE — Rechteregel: space-level Schreibrecht auf *beiden* Seiten.** Quelle **und** Ziel
  müssen `permissions.can_write(actor, space)` erfüllen — dieselbe Prüfung, die
  `create_item(space=…)` seit Step 5 benutzt (`tools.py:436`). *Warum diese und keine andere:*
  item-level `share_write` verleiht nie space-level Schreibrecht, also kann ein Delegat, der genau
  ein fremdes Item bearbeiten darf, es nicht in einen geteilten Space wegtragen — das wäre
  Exfiltration und Entzug in einem Zug, und die Re-Auth aus Step 7 sähe es nie (die greift nur
  beim Eigentümer, der seine eigene Freigabe erweitert). Symmetrisch formuliert und in einem Satz
  erklärbar, im Gegensatz zur Alternative „nur der Eigentümer-Space" — die hätte Items in einem
  geteilten Space unbewegbar gemacht, weil kein Principal `IT-Sekus-Projekt` heißt.
- **P6-AF — leere Quellordner werden nach dem Move aufgeräumt, aber nur eigene.** `move()`
  entfernt das Quellverzeichnis, wenn es danach leer ist, aufwärts bis maximal zur Space-Wurzel,
  und **nur**, wenn es keine `.share.yml` enthält. *Warum die Ausnahme:* eine `.share.yml` in
  einem leer gewordenen Ordner ist eine bewusste Freigabe eines Menschen, kein Rest — sie
  wegzuräumen würde eine Rechteeinstellung als Nebenwirkung eines Moves löschen.
- **P6-AG — der Move zählt die Version hoch.** Wie jeder andere Write. *Warum nicht wie bei
  `migrate_visibility.py`:* dort war nichts Beobachtbares anders (fehlendes `visibility` hatte
  schon vorher denselben Default). Hier ändern sich Pfad, Space und potenziell die gesamte
  `AclDecision` — eine Instanz, die das alte Item in der Hand hält, **muss** einen `ConflictError`
  bekommen.
- **P6-AH — `visibility`/`share_read`/`share_write` fahren unverändert mit.** Der Move
  transportiert das Item, er interpretiert es nicht. *Warum benannt statt selbstverständlich:* der
  Ziel-Space kann eine breitere `.share.yml` haben, die effektiven Rechte ändern sich also, ohne
  dass ein Item-Feld angefasst wird. Genau dafür ist das Re-Auth-Gate da (P6-AI), nicht ein
  stilles Zurücksetzen der Item-Felder.
- **P6-AI — ein Cross-Space-Move durch die UI läuft durch `widens()`/Re-Auth.** Wenn die
  effektive Lese-/Schreibmenge am Ziel eine echte Obermenge der Quelle ist, verlangt die UI
  Re-Auth — dieselbe Mechanik wie der Freigabedialog aus Step 7, kein zweites Gate. Über MCP gibt
  es kein Re-Auth (das kann ein Agent nicht), deshalb gilt dort P6-AJ.
- **P6-AJ — die Agentenfläche darf verschieben, aber nur innerhalb ihrer Mitgliedschaft.** Kein
  Sonderfall: `can_write` auf beiden Seiten ist bereits die vollständige Regel, ein Agent hat
  nirgends mehr Rechte als sein Principal. *Warum nicht ganz sperren:* das Werkzeug-Feedback, aus
  dem diese Phase entstanden ist, kam von einer arbeitenden Claude-Instanz; ein Ablagesystem, in
  dem der Agent Dinge anlegen, aber nie einsortieren kann, erzeugt genau die Sorte Handarbeit, die
  `patch_item` gerade abgeschafft hat.

**Bewusst NICHT in diesem Plan** (Nikinger-Vorgabe 2026-08-13): geteilte Spaces über die UI
anlegen. Das bleibt `spacectl.py` (P6-V: UI gebaut, aber abgeschaltet). Dieser Plan fügt dem
`space_admin_enabled`-Schalter nichts hinzu.

---

## §3 Step 7a — Lesbarkeit der Textfarben

**Auslöser:** Nikinger-Meldung 2026-08-13, „der graue Text ist nicht gut lesbar". Unabhängig von
allem anderen, jederzeit lieferbar.

### 3.1 Messung (nicht geschätzt)

WCAG-2.1-Kontrastverhältnisse der drei Textfarben gegen die fünf Flächenfarben der App:

| Token | Wert | gegen `--bg` | `--surface` | `--surface-raised` | `--panel-body` | `--panel-meta` | AA (4.5:1) |
|---|---|---|---|---|---|---|---|
| `--text` | `#E9EDF2` | 16.55 | 15.16 | 13.93 | 15.60 | 15.31 | ✅ |
| `--text-muted` | `#9AA6B4` | 7.86 | 7.20 | 6.62 | 7.41 | 7.27 | ✅ |
| `--text-faint` | `#64707E` | 3.86 | 3.53 | **3.24** | 3.63 | 3.57 | ❌ **fällt durch** |

Der gemeldete Defekt ist damit lokalisiert: **`--text-faint`** (16 Verwendungen) reißt AA auf
jeder Fläche der App. `--text-muted` (19 Verwendungen) besteht AA bereits.

### 3.2 Entschieden (Nikinger, 2026-08-13): kalibriert, Platzhalter ausgenommen

```css
--text:             #E9EDF2;   /* unverändert */
--text-muted:       #C4CDD8;   /* war #9AA6B4 —  7.9 → 12.1 : 1 */
--text-faint:       #A7B2BF;   /* war #64707E —  3.9 →  9.1 : 1 */
--text-placeholder: #7E8A98;   /* NEU, 5.0 : 1 — nur für .input::placeholder */
```

Und genau eine Regeländerung, `app.css:187`:

```css
.input::placeholder { color: var(--text-placeholder); }   /* war var(--text-faint) */
```

**Warum nicht einfach beide auf `--text` zeigen lassen** (die wörtliche Lesart des Vorschlags):
35 Regeln hängen an diesen zwei Token, darunter `.input::placeholder` (`app.css:187`) und
`.editor__version` (`app.css:682`). Ein Platzhalter in Fließtextweiß lässt ein **leeres**
Eingabefeld wie ein ausgefülltes aussehen — das ist kein Geschmacksfehler, das ist ein
Bedienfehler. Und das Versionsband ist nach Designsystem §4.4 absichtlich leise; es so laut wie
den Titel zu machen, kehrt eine bewusste Entscheidung um. Die kalibrierte Fassung erreicht beides:
alles Sichtbare deutlich über AA, die drei Ebenen der Tiefenstaffelung bleiben unterscheidbar.

**Warum die Token-Werte und nicht die 35 Regeln:** die Farbtoken sind laut `app.css`-Kopfkommentar
das eine, was auch die Step-7b-Revision von 2026-08-05 ausdrücklich **nicht** angefasst hat. Sie
sind der dafür vorgesehene Schalter. Wer stattdessen Regeln einzeln umhängt, hat danach zwei
Wahrheiten darüber, was „leiser Text" in dieser App bedeutet.

### 3.3 Umfang und Nachweis

- **Dateien:** `phase5_ui/webui/static/app.css` — vier Token-Zeilen plus eine Regel. Sonst nichts.
- **Kein Python, kein JS.** Auch `pages.py` nicht: die Auth-Seiten benutzen dieselben Token, kein
  Inline-`style` (P5-T, `app.css`-Kopfkommentar).
- **Tests:** keine neuen. JS/CSS bleiben nach P5-T unit-ungetestet; `pytest` läuft als reine
  Regressionsprobe (Erwartung: unverändert grün).
- **Sichtprobe Pflicht, nicht optional:** Screenshot gegen die echte `app.css` wie bei der
  Wortmarken-Änderung vom 2026-08-13 (`phase5_ui/CLAUDE.md`, Korrekturnotiz) — mindestens
  Editor mit Meta-Panel, Liste mit Chips, Login-Seite.
- **DoD:** Kontrastwerte nachgerechnet und im Session-Block protokolliert · Screenshot gesehen,
  nicht behauptet · `pytest` unverändert · Nikinger bestätigt live nach dem Deploy.

---

## §4 Step 7b — Item verschieben zwischen Spaces

**Voraussetzung: Step 7 ist gebaut** (echte Ordner im Baum, Verschieben innerhalb des Space per
Menü/Drag & Drop, `.share.yml`-Dialog mit `widens()`/Re-Auth). Ohne Step 7 gibt es weder eine
Ordneransicht noch die Re-Auth-Mechanik, an der P6-AI hängt.

### 4.1 `storage/store.py` — die eine neue Methode

```python
def move(self, item_id: str, *, version: int, space: str | None = None,
         folder: str | None = None) -> Item:
    """Verschiebt ein Item in einen anderen Space und/oder Ordner. Genau ein Git-Commit
    (`move <id> [<ziel-space>]`), genau ein Versionssprung, Frontmatter-`space` zieht mit.
    Autorisierung passiert NICHT hier (wie überall im Store) — siehe §4.2/§4.3.
    """
```

Ablauf, bewusst ohne neue Bausteine:

1. `_reconcile_and_get_row()` + `ConflictError` bei `version`-Mismatch + `ValidationError` bei
   `status == "archived"` — **wortgleich** zu `update()`/`append()`/`patch()`. Kein eigener
   Vorspann, kein abweichender Fehlertext.
2. `space` (falls gesetzt): Zielverzeichnis muss existieren und ein Space sein — sonst
   `ValidationError`. *Warum eine explizite Prüfung:* `_write_item_file()` würde das Verzeichnis
   sonst per `mkdir(parents=True)` beiläufig anlegen und aus einem Tippfehler einen neuen,
   rechtefreien Space machen.
3. `folder` (falls gesetzt): `files.validate_folder()` wie in `update()`. Bei Space-Wechsel ohne
   `folder`-Angabe: Ziel ist die Space-Wurzel (`""`), **nicht** der gleichnamige Ordner im
   Zielspace — ein Ordnername bedeutet in einem anderen Space etwas anderes und trägt eine andere
   `.share.yml`.
4. `replace(current, space=…, folder=…, version=+1, updated=now)` →
   `self._write_item_file(new_item, old_path=old_path, op="move")`. Das ist der in §1.3
   protokollierte, bereits funktionierende Pfad.
5. P6-AF: leer gewordene Quellverzeichnisse aufwärts entfernen, Abbruch bei `.share.yml` oder bei
   der Space-Wurzel.

**Bekanntes Fenster, geerbt und benannt:** zwischen `atomic_write` (alter Pfad, neues Frontmatter)
und `move_file` liegt ein Absturzfenster, in dem Datei und Verzeichnis divergieren. Das ist **kein
neuer Defekt** — `archive()` (`store.py:573-574`) hat dasselbe Fenster seit P1. Die Umkehrung
(erst am Ziel schreiben, dann die Quelle löschen) wäre schlechter: ein Absturz hinterließe dann
**zwei** Dateien mit derselben `id`, und `rebuild_index()` müsste zwischen zwei gleichberechtigten
Wahrheiten wählen. Divergenz ist reparierbar und sichtbar, ein doppeltes Item ist es nicht.

**Charakterisierung (P6-D):** `phase6_shares/tests/test_characterization.py` läuft vor und nach
diesem Umbau byte-identisch. `move()` ist additiv, `update()`/`archive()` werden nicht angefasst —
wenn ein Golden File kippt, ist etwas anderes passiert als geplant.

### 4.2 `mcpserver/tools.py` — `space` an `update_item`, kein achtes Tool

`update_item` bekommt `space: str | None = None`. Kein neues Tool. *Warum:* die Werkzeugliste ist
bereits auf sieben gewachsen, und der Aufrufer hat ohnehin schon `item_id` + `version` in der Hand
— ein `move_item`-Tool wäre dieselbe Signatur mit einem anderen Namen. `update_item` routet auf
`store.move()`, sobald `space` gesetzt ist; sonst bleibt alles wie heute.

Rechteprüfung, direkt nach dem bestehenden `can_write_item`-Block (`tools.py:504`):

```python
if space is not None and space != acl.space:
    if not permissions.can_write(principal.space, acl.space):      # Quelle
        raise map_storage_error(PermissionDenied(acl.space)) from None
    if not permissions.can_write(principal.space, space):          # Ziel
        raise map_storage_error(PermissionDenied(space)) from None
```

Und der bestehende Fail-Closed-Riegel gegen Nicht-Eigentümer-Ordnerwechsel (`tools.py:514-520`)
**bleibt unverändert** — er gilt weiter für den reinen Ordner-Move. Bei einem Space-Wechsel
ersetzt die Regel aus P6-AE ihn, weil sie strenger in der relevanten Richtung ist: sie verlangt
space-level Schreibrecht, das ein item-level `share_write`-Delegat per Konstruktion nie hat.

**[2026-08-17, Präzisierung dieser Session — Advisor-Fund vor dem Bauen.]** „Ersetzt ihn" war im
Text bisher nicht codeseitig verankert: der bestehende Riegel prüft `if folder is not None and
acl.space != principal.space`, ohne auf `space` zu achten. Für einen Space-Move MIT gleichzeitig
gesetztem Zielordner (der reale Fall in §4.4 Punkt 1 — der Dialog trägt beide Felder) wäre
`acl.space != principal.space` für praktisch jeden Cross-Space-Move wahr (kein Principal heißt
wie ein geteilter Space, P6-AE), der alte Riegel würde also fälschlich vor der neuen P6-AE-Prüfung
greifen und einen legitimen Move mit space-level Schreibrecht auf beiden Seiten ablehnen. Der
alte Riegel bekommt deshalb eine explizite Bedingung `space is None`:
```python
if folder is not None and space is None and acl.space != principal.space:
    raise map_storage_error(ValidationError(...)) from None
```
Bei `space is not None` übernimmt ausschließlich der P6-AE-Block oben die Prüfung (Quelle UND
Ziel). Neuer Pflichttest in §4.5: `test_update_item_with_space_and_folder_together_uses_space_
level_check_not_owner_guard` — ein Move mit `space=` UND `folder=` durch einen Actor mit
space-level Schreibrecht auf beiden Seiten, aber ohne Eigentümerschaft am Quell-Space, muss
gelingen (nicht am alten Riegel scheitern). Dasselbe Muster gilt analog in `webui/api.py`s
Pendant (§4.3) — dort ist der bestehende Eigentümer-Riegel derselbe Fund, derselbe Fix.

Tool-Description ergänzen (dieselbe Kategorie wie die drei Präzisierungen vom 2026-08-13):
`space=<name> verschiebt es in einen anderen Space — nur zwischen Spaces, in denen du schreiben
darfst.`

### 4.3 `webui/api.py` — `space` in `_items_patch`

Analog, mit `can_write_item_as_human()` als Vorprüfung und `permissions.can_write()` für beide
Seiten. Zusätzlich P6-AI: liegt am Ziel eine echte Rechteerweiterung vor, antwortet der Endpunkt
mit `reauth_required` statt zu verschieben — **exakt die Antwortform, die der Freigabedialog aus
Step 7 schon benutzt**, kein zweites Fehlerprotokoll. `webui/shares.py :: widens()` bekommt dafür
keinen neuen Code: eine `ShareState` trägt bereits `space` und `folder` (Hauptplan §1.2.5), ein
Move ist also nur ein weiterer Aufruf mit anderem `before`/`after`.

**Im selben Schnitt zu schließen (K4):** `_items_post` nimmt `folder` in seine Feld-Whitelist auf
(`api.py:343`). Ein Ablagesystem, in dem man ein Item verschieben, aber nicht direkt am Zielort
anlegen kann, ist eine halbe Funktion — und die Agentenfläche kann es seit Step 5.

### 4.4 UI — was der Mensch tatsächlich sieht

Aufbauend auf Step 7 (Ordnerbaum vorhanden, Verschieben innerhalb des Space vorhanden):

1. **Ein Dialog, zwei Felder.** „Verschieben nach …" mit Space-Auswahl (nur Spaces mit
   `writable: true` — die Liste trägt das Feld seit dem Badge-Fix vom 2026-08-13) und darunter
   Ordner-Auswahl **des gewählten Ziel-Space**. Wechsel des Space setzt die Ordnerauswahl auf
   „(Space-Wurzel)" zurück, siehe §4.1 Punkt 3. **[2026-08-17 V54 geklärt, kein Backend-Fund:]**
   die Ordnerliste jedes sichtbaren Space liegt bereits heute in `state.spaces` — `list.js ::
   loadOverview()` mischt `folders`/`members` aus `GET /api/v1/spaces` seit Step 7 Commit 1 in
   jeden Space-Eintrag (`state.js:28`), nicht nur den aktiven. `dialogs.js :: openMoveDialog()`
   liest `spaceByName(item.space).folders` schon heute für den bestehenden In-Space-Dialog
   (Zeile 195) — die Erweiterung um eine Space-Auswahl liest exakt denselben Weg für den
   GEWÄHLTEN Space, kein neuer Endpunkt, kein `GET /api/v1/overview`-Feld nötig (die alte Sorge
   aus §1.2 K3 galt `/overview`, nicht `/spaces`).
2. **Erreichbar von zwei Stellen**, dieselben zwei wie beim Archivieren heute: aus dem Editor-Kopf
   und aus dem Kontextmenü einer Listenzeile.
3. **Drag & Drop auf einen Space-Knoten im Baum** — mit derselben Pflicht-Alternative wie P6-AB
   sie für Bilder verlangt: die Menüvariante ist der Hauptweg, D&D ist die Abkürzung, nie der
   einzige Weg.
4. **Bestätigung mit Konsequenz im Klartext**, nicht „Sind Sie sicher?": *„Verschiebt das Item aus
   `niklas` nach `IT-Sekus-Projekt`. Alle Mitglieder dieses Space können es danach lesen und
   ändern."* Bei Rechteerweiterung folgt danach der Re-Auth-Dialog (P6-AI).
5. **Nach dem Move:** Toast, Liste neu laden, Auswahl folgt dem Item in den Ziel-Space — nicht die
   Auswahl leeren. Ein Verschieben, nach dem das Item verschwindet, fühlt sich wie ein Löschen an.
6. **Geisterordner (O7):** der Baum darf leere Ordner nicht dauerhaft anzeigen. P6-AF räumt sie
   serverseitig ab; die UI muss danach nur den Baum neu laden.

### 4.5 Tests

| Datei | Test | Prüft |
|---|---|---|
| `phase1_storage/tests/test_store.py` | `test_move_between_spaces_rewrites_frontmatter_space` | Pfad **und** Frontmatter, keine Divergenz (Fund B2) |
| ″ | `test_move_between_spaces_produces_exactly_one_commit` | ein `move`-Commit, kein Doppel |
| ″ | `test_move_bumps_version_and_conflicts_on_stale_version` | P6-AG |
| ″ | `test_move_to_nonexistent_space_raises_instead_of_creating_it` | §4.1 Punkt 2 |
| ″ | `test_move_removes_emptied_source_folder_but_keeps_one_with_share_yml` | P6-AF |
| ″ | `test_move_of_archived_item_is_rejected` | Gleichlauf mit `update()` |
| `phase6_shares/tests/test_acl.py` | `test_acl_decision_follows_the_item_into_the_target_space` | ACL folgt dem Pfad, nicht dem Item |
| `phase2_mcp/tests/test_tools.py` | `test_update_item_with_space_moves_between_shared_spaces` | Positivfall |
| ″ | `test_item_level_share_write_holder_cannot_move_item_to_another_space` | **P6-AE, der Kern** |
| ″ | `test_move_into_space_without_write_grant_is_denied` | Zielseite |
| ″ | `test_move_out_of_space_without_write_grant_is_denied` | Quellseite |
| `phase5_ui/tests/test_api.py` | `test_patch_with_space_requires_reauth_when_target_widens_access` | P6-AI |
| ″ | `test_patch_with_space_does_not_require_reauth_when_target_narrows` | Gegenrichtung |
| ″ | `test_create_item_accepts_folder` | K4 |
| `phase6_shares/tests/test_characterization.py` | *(unverändert)* | byte-identisch vor/nach (P6-D) |

**DoD Step 7b:** alle Tests grün · Charakterisierung byte-identisch · `git diff` auf
`authserver/` leer · ein realer Move über den echten Connector **und** einer über die UI vom
Nikinger bestätigt · `git log` im `DATA_ROOT` zeigt genau einen `move`-Commit mit erkanntem
Rename.

---

## §5 Neue Abnahmezeilen

Fortsetzung der Matrix in Hauptplan §6 (dort 1–24). **✅ heißt live-verifiziert, nicht gebaut.**

| # | Kriterium | Wer |
|---|---|---|
| 25 | Grauer Text ist nach dem Deploy lesbar; Platzhalter bleiben als leer erkennbar | Niklas |
| 26 | Ein Item wird über die UI von `niklas` nach `IT-Sekus-Projekt` verschoben; die Datei liegt real dort, `git log` zeigt **einen** `move`-Commit | Niklas |
| 27 | Fabian sieht das verschobene Item danach im geteilten Space und kann es ändern | Fabian |
| 28 | Ein Item mit `share_write` für Fabian, aber ohne space-level Grant, lässt sich von Fabian **nicht** wegverschieben (klare Fehlermeldung) | Fabian |
| 29 | Ein Item wird über den Connector zwischen zwei Spaces verschoben, in denen der Principal Mitglied ist | Niklas (Connector) |
| 30 | Nach dem Verschieben des letzten Items aus einem Ordner zeigt der Baum diesen Ordner nicht mehr | Niklas |

---

## §6 `[VERIFY]`-Register

Fortsetzung von Hauptplan §7 (dort V39–V51).

| # | Was | Wann | Status |
|---|---|---|---|
| V52 | Exakte Antwortform von `reauth_required` aus Step 7 — dieser Plan setzt Wiederverwendung voraus, Step 7 existiert noch nicht | Step 7b | **[2026-08-17 geschlossen]** Step 7 ist gebaut: `webui/shares.py :: require_share_reauth()` wirft `ApiError("reauth_required", <text>)`, `ShareState` trägt bereits `space`/`folder`. Plan-Annahme in §4.3 hält, keine Änderung nötig |
| V53 | Verhält sich `os.replace` über Space-Grenzen im echten `DATA_ROOT` weiterhin atomar? (Probelauf lief auf `/tmp`, ein Dateisystem; real ist es ext4 unter `/home` — **muss dasselbe Dateisystem sein**, sonst ist `move_file()` kein Rename mehr) | Step 7b | **[2026-08-17 geschlossen]** read-only gegen den echten `DATA_ROOT` geprüft: `stat -c %d` von `niklas`/`fabian`/`IT-Sekus-Projekt` liefert identisch `2050` (ext4, `/dev/sda2` auf `/`) — ein Dateisystem, `os.replace()` bleibt ein echtes Rename |
| V54 | Trägt `GET /api/v1/overview` nach Step 7 ein `folders`-Feld? Der Verschieben-Dialog braucht die Ordner des **Ziel**-Space, nicht nur des aktiven | Step 7b | **[2026-08-17 geschlossen, anders als erwartet]** Nein, und braucht es auch nicht — `GET /api/v1/spaces` trägt `folders` bereits für jeden sichtbaren Space, und `list.js :: loadOverview()` mischt das seit Step 7 Commit 1 in `state.spaces`. Kein Backend-Fund für §4.4 Punkt 1 |
| V55 | `search(folder=…)` ist heute **exakter** Gleichheitsvergleich (`store.py:391`), kein Präfix — reicht das für einen Baum mit zwei Ebenen, oder braucht Step 7 Präfix-Semantik? | Step 7 | geschlossen mit Step 7 (Baum ist zweistufig, exakter Vergleich je Ebene reicht — siehe Modul-Status Zeile 10, live per Playwright bestätigt) |

---

## §7 Risiken

1. **Ein Cross-Space-Move ist die erste Operation des Projekts, die Daten aus dem Besitz einer
   Person herausnimmt.** Alles andere fügt hinzu oder ändert an Ort und Stelle. Deshalb P6-AE auf
   beiden Seiten, deshalb Abnahmezeile 28 mit Fabian als Prüfer, deshalb der Klartext in der
   Bestätigung (§4.4 Punkt 4).
2. **Step 7b vor Step 7 zu bauen ist verlockend und falsch.** Die Storage-Schicht ist nach §1.3
   klein — man könnte sie an einem Nachmittag bauen. Ohne den Ordnerbaum aus Step 7 hätte sie aber
   keine Bedienung, und ohne `widens()`/Re-Auth kein Gate. Wer die Reihenfolge dreht, liefert eine
   Cross-Space-Schreiboperation ohne das Gate, das Hard Rule 4s Neufassung dafür vorsieht.
3. **Der CSS-Schnitt sieht harmloser aus als er ist.** 35 Regeln hängen an zwei Token. Ohne die
   Sichtprobe aus §3.3 fällt erst live auf, dass ein Platzhalter jetzt wie ein Wert aussieht.
4. **Scope-Aufweichung, konkret zu erwarten:** „wenn wir schon verschieben können, ist Löschen
   doch nur ein Move nach `/dev/null`". Nein — F2/Hauptplan §0.5 hält Löschen bewusst draußen, und
   `move()` prüft nach §4.1 Punkt 2 ausdrücklich auf ein existierendes Ziel.

---

## §8 Was dieser Plan nicht tut

- **Geteilte Spaces über die UI anlegen** — Nikinger-Vorgabe 2026-08-13, bleibt `spacectl.py`
  (P6-V).
- **Löschen** — F2, unverändert draußen.
- **Ordner tiefer als zwei Ebenen** — `MAX_FOLDER_DEPTH = 2` (P6-Q) bleibt.
- **Verschieben aus dem Archiv heraus** — Archivieren ist einseitig (P6-R). `move()` lehnt
  archivierte Items ab, gleichlaufend mit `update()`.
- **Massen-/Mehrfachauswahl beim Verschieben** — §§1–8 dieses Dokuments behandeln ausschließlich
  Step 7b (ein Item pro Vorgang). Der „eigene Befund mit eigener Entscheidung" ist eingetreten
  (Nikinger-Meldung 2026-08-14, siehe Phase-Head „Vormerkungen") — Entscheidungen und Umfang
  dafür stehen jetzt separat in **§9**, nicht rückwirkend hier eingemischt.

---

## §9 Mehrfachauswahl (Erweiterung, Nikinger-Auftrag 2026-08-17, „planning session light")

**Setzt Step 7b (§4) voraus** — jeder Batch-Vorgang ist am Ende nur eine Schleife über den dort
gebauten Einzel-Move-Pfad, kein eigener Schreibpfad. Kein eigener Charakterisierungs-Bedarf
(P6-D): `storage/`/`mcpserver/`/`webui/api.py` werden für dieses §9 **nicht angefasst**, reiner
Frontend-Schnitt.

### 9.1 Herkunft und Rahmen

Nikinger-Vorgabe vom 2026-08-14 (Phase-Head „Vormerkungen" Punkt 3), hier zum ersten Mal in
Entscheidungen gegossen: *„ein einmaliger Code für die Mehrfachauswahl-Aktion selbst ist
akzeptabel … Verschieben innerhalb eines Space muss dabei weiterhin codefrei bleiben."* Letzteres
ist bereits grep-bestätigt wahr (Punkt 3, Zeile 140f. oben): `moveItemToFolder()` patcht
ausschließlich `folder`, nie `share_read`/`share_write`, `widens()` greift bei einem reinen
Ordnerwechsel nie — eine In-Space-Mehrfachauswahl braucht also **keine neue Rechteprüfung**, nur
eine Schleife über einen bereits geprüften Aufruf.

### 9.2 Neue Entscheidungen (P6-AK – P6-AN)

Fortsetzung der Nummerierung aus §2 (dort endet sie bei P6-AJ).

- **P6-AK — ein gemeinsames Ziel für die ganze Auswahl, kein Ziel pro Item.** Der Dialog aus §4.4
  öffnet sich einmal für die gesamte Selektion. *Warum:* unabhängige Ziele pro Item wäre wieder
  N Einzeldialoge mit einem gemeinsamen Startknopf — löst das gemeldete Problem (40+
  Einzelaktionen an einem Tag) nicht. Ein Ziel für alle ist die kleinste Erweiterung, die den
  echten Schmerz behebt.
- **P6-AL — kein neuer Endpunkt, kein neues MCP-Tool.** Die Batch-Aktion ist eine clientseitige
  sequenzielle Schleife über das bestehende `PATCH /api/v1/items/{id}` aus Step 7b — pro Item ein
  eigener Request, keine Sammel-Payload. *Warum sequenziell, nicht parallel:* Re-Auth-Fehlversuche
  laufen über `LoginThrottle` (`authserver/ratelimit.py`, dieselbe Bremse wie UI-Login/Consent) —
  parallele Requests könnten das bei einem einzigen falschen Credential-Versuch unnötig
  strapazieren, sequenziell bleibt die Fehlerzuordnung außerdem eindeutig einem Item zugeordnet.
  *Warum kein neuer Endpunkt:* jeder einzelne Request durchläuft die volle, in §4 bereits gebaute
  und geprüfte P6-AE-Rechtsprüfung unverändert — kein neuer Codepfad, keine neue Angriffsfläche
  für Hard Rule 4. Das ist der „einmalige Code", den der Nikinger erlaubt hat: Auswahl sammeln,
  Fortschritt anzeigen, Teilfehler einsammeln — keine neue Schreib- oder Rechteprüfung.
  **Kein MCP-Tool:** Mehrfachauswahl ist laut Auslöser (Nikinger zieht mehrere Zeilen in der UI)
  ein Menschen-/UI-Feature; ein Agent kann seit P6-AJ bereits einzelne Items per `update_item
  (space=…)` verschieben, in einer eigenen Schleife, ohne dass dafür ein achtes Tool nötig wäre.
- **P6-AM — Re-Auth wird bei Bedarf einmal für die ganze Auswahl eingeholt, nicht angenommen.**
  Naiv „ein gemeinsames Ziel ⇒ ein gemeinsames `widens()`-Ergebnis" wäre **falsch** — `widens()`
  hängt auch an der `visibility`/`share_read`/`share_write` des einzelnen Items (§2, P6-AH), zwei
  Items mit demselben Ziel können unterschiedlich urteilen (eines bereits geteilt, eines noch
  `private`). Der Batch nimmt deshalb den bereits vorhandenen Server-Zustand ernst statt ihn
  vorherzusagen: **Runde 1** schickt alle N Requests ohne Credentials. Kommt mindestens ein
  `403 reauth_required` zurück, zeigt die UI **ein** gemeinsames Re-Auth-Mini-Formular (dieselbe
  Komponente wie der bestehende Freigabedialog, §4.3) — **Runde 2** wiederholt ausschließlich die
  zurückgewiesenen Requests mit `password`/`totp` angehängt. Items, die in Runde 1 schon
  durchgingen (kein Widen), werden nicht erneut angefasst. *Warum nicht konservativ IMMER
  Re-Auth verlangen:* das würde jede In-Space-Mehrfachauswahl (P6-AN) unnötig hinter ein
  Passwort-Formular stellen, obwohl der Server es nie verlangen würde — genau die Reibung, die
  dieser Schnitt beheben soll.
- **P6-AN — In-Space-Mehrfachauswahl bleibt ohne neues Rechte-Verhalten.** Direkte Folge aus 9.1:
  für einen reinen Ordnerwechsel liefert Runde 1 nie ein `reauth_required`, der Batch braucht also
  faktisch nie eine zweite Runde. Kein Sonderfall im Code — dieselbe Schleife wie P6-AL, nur dass
  Runde 2 in der Praxis leer bleibt.

### 9.3 UI (`phase5_ui/webui/static/js/`)

1. **Auswahl.** Strg+Klick oder Long-Press auf eine Listenzeile (Nikinger-Vorgabe) togglet die
   `<li>` in `state.selectedItemIds` (neues `Set`, `list.js`). Ausgewählte Zeilen bekommen eine
   Modifier-Klasse (`.list__row--selected`), analog zu `[aria-current]` bei der Navigation.
   **Navigation leert die Auswahl** (Ordnerwechsel, Bucket-Wechsel, Suche) — dieselbe
   Exklusivitäts-Disziplin wie `state.folder`/`state.filter` seit Step 7 Commit 1 (dort bereits
   ein Advisor-Fund zu ungeschütztem `state.filter`-Zugriff, siehe Modul-Status Zeile 10). Ohne
   diese Regel könnte eine Auswahl Items enthalten, die in der aktuellen Listenansicht gar nicht
   mehr sichtbar sind — die „8 von 10 verschoben"-Zusammenfassung (Punkt 4) würde dann auf Zeilen
   verweisen, die der Mensch nicht mehr sieht.
2. **Aktion.** Ein Auswahl-Werkzeugleiste erscheint nur, wenn `selectedItemIds` nicht leer ist:
   „N ausgewählt · Verschieben · Abwählen". „Verschieben" öffnet `openMoveDialog()` (§4.4) mit
   `moveTargetItems = [...ausgewählte Items]` statt eines einzelnen `moveTargetItem` — derselbe
   Dialog, keine zweite Dialog-Definition.
3. **Ausführung.** `moveSelectedItems(items, {space, folder})` (`list.js`, neu) — die in P6-AL/AM
   beschriebene Zweirunden-Schleife, meldet Fortschritt (`x von N`) im Dialog selbst.
4. **Ergebnis.** Sammel-Toast: „8 von 10 verschoben." Fehlgeschlagene Items namentlich in einer
   zweiten Zeile („2 fehlgeschlagen: „Einkaufsliste" [Konflikt], „Q3-Plan" [keine Schreibrechte
   am Ziel]") — kein stilles Verschlucken einzelner Fehler in einer Sammelmeldung ohne Namen.
5. **Nach dem Batch:** Auswahl geleert, Liste neu geladen (anders als bei §4.4 Punkt 5 — bei
   mehreren Items aus potenziell verschiedenen Ausgangsordnern ist „die Auswahl folgt in den
   Zielordner" kein eindeutiger Zustand mehr, eine geleerte Auswahl ist der ehrlichere Default).

### 9.4 Tests

**Keine neue Backend-Testdatei** — P6-AL macht dieses §9 zu einem reinen Frontend-Schnitt, der
bereits gebaute und getestete Step-7b-Endpunkt bleibt unverändert. Verifikation beim Bauen wie
bei jedem anderen JS-Schnitt dieser Phase (P5-T): Playwright-Sichtprobe gegen einen echten,
temporären Server — Mehrfachauswahl (3+ Items), Batch in einen Space ohne Widen (keine
Re-Auth-Aufforderung erwartet), Batch mit einem Widen-Item (genau ein Re-Auth-Formular), ein
absichtlich in Konflikt gebrachtes Item in der Mitte einer Auswahl (Batch läuft weiter, taucht
namentlich im Fehlerbericht auf). `pytest` läuft unverändert als Regressionsprobe (kein neuer
Test erwartet, keiner sollte kippen).

### 9.5 Neue Abnahmezeilen

Fortsetzung der Matrix aus §5 (dort 25–30).

| # | Kriterium | Wer |
|---|---|---|
| 31 | N ausgewählte Items werden auf einmal in denselben Zielspace/-ordner verschoben; alle N Dateien liegen danach real dort, ein `move`-Commit je Item | Niklas |
| 32 | Eine Auswahl mit genau einem rechteerweiternden Item verlangt **ein** Re-Auth-Formular pro Versuch, nicht eines je Item (ein Formular deckt Runde 2 für alle zurückgewiesenen Items gemeinsam ab — ein Tippfehler bei Passwort/TOTP zeigt es korrekt erneut) | Niklas |
| 33 | Ein einzelnes fehlgeschlagenes Item in der Auswahl (z. B. veraltete Version) blockiert die anderen nicht — Sammelmeldung nennt es namentlich | Niklas |
| 34 | Mehrfachauswahl innerhalb eines Space löst nie ein Re-Auth-Formular aus | Niklas |

### 9.6 Was §9 nicht tut

- **Unterschiedliche Ziele pro Item in einem Batch** — P6-AK, bewusst draußen.
- **Ein Bulk-Endpunkt oder ein achtes MCP-Tool** — P6-AL, bewusst draußen; dieselbe
  Zurückhaltung wie beim offenen „kein Bulk-Append"-Punkt der Werkzeug-Ergonomie-Vormerkung
  (Phase-Head, 2026-08-14) — ein Bulk-Schreibpfad ist ein eigener, größerer Schnitt mit eigener
  Rechteprüfung, kein Nebenprodukt dieses Plans.
- **Mehrfachauswahl für andere Aktionen** (Archivieren, Freigeben) — nur Verschieben war
  gemeldet, nur Verschieben ist hier geplant.
