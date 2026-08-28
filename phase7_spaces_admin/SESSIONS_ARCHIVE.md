---
status: live
purpose: Archivierte Session-stopped-Blöcke aus phase7_spaces_admin/CLAUDE.md, verbatim, newest-first
read-when: Auditieren der vollen Phase-7-Historie — der aktuelle Session-Block lebt im Phase-Head, nicht hier
detail: L3
up: ./CLAUDE.md
down:
updated: 2026-08-28 (zweite Rotation — der über fünfzehn Nachträge gewachsene 2026-08-24-Block verschoben, 984 Zeilen) | 2026-08-24 (erste Rotation — Step-0/A1–A8-Block verschoben, 379 Zeilen)
---
# SESSIONS_ARCHIVE.md — Phase 7: Space-Verwaltung, Mehrfachauswahl, Konsolidierung

Zwei Einträge, newest-first.

## Session stopped — 2026-08-24 (Manueller Purge gefahren, P6.5-12-Browserprobe: Deploy-Blocker gefunden, Versionsbump)

**Auftrag:** Fortsetzung derselben Sitzung, Datumswechsel während der Sitzung. Nikinger bot an,
den Purge (A6) manuell vorzuziehen und half beim P6.5-12-Browsernachweis mit eigenem Login.

**A6 — Purge manuell gefahren (Nikinger, `sudo systemctl start sharefyx-purge.service`).**
Baseline vorher (read-only): `clients: 54`, `token_families: 35`. Lauf `status=0/SUCCESS`, echte
Löschungen (`auth_requests: 8, auth_codes: 7, access_tokens: 15, invites: 1` — 31 Zeilen), aber
`clients`/`token_families` beide **unverändert bei 54/35**. Kein Fehlschlag — geprüft:
`TOKEN_FAMILY_RETENTION_S = 30*86400`, `CLIENT_RETENTION_S = 90*86400`
(`authserver/store.py:54,63`), ältester `clients`/`token_families`-Eintrag ist
`2026-07-29T15:02:27Z`. **Präzisierung gegenüber dem Plan-Text:** `token_families` wird ab
**2026-08-28** sichtbar sinken (deckt sich mit der Plan-Erwartung), `clients` aber erst ab
**2026-10-27** — fast zwei Monate später als angenommen. P7-9 bleibt ⬜, jetzt mit korrekter
Zeitangabe für beide Tabellen statt einer gemeinsamen.

**P6.5-12-Browserprobe: echter Fund, kein Bug.** Zweiter Login-Anlauf nötig — der erste
Nikinger-Login lief in einem Tab außerhalb meiner MCP-Tab-Gruppe, `sessionStorage`s
`sfx:csrf` wird ausschließlich von der `/ui/login`-POST-Antwort gesetzt
(`app.js:34-36`, `location.pathname !== "/ui/"`), ein reines Neuladen von `/ui/` liefert ihn
nicht nach — korrektes P5-H-Verhalten, kein Leck (erster Upload-Versuch schlug entsprechend mit
`403 csrf_failed` fehl). Nikinger loggte sich ein zweites Mal ein, diesmal im von mir
gesteuerten Tab (`testcred.py password`/`totp` in seinem eigenen Terminal, nie durch mich
gelesen). Upload gelang (`ast_2cf1ce2f`, `itm_ee1e0323`, PIL-PNG), Bild rendert sichtbar, `.md`
+ Asset-Datei korrekt im echten `DATA_ROOT`. **Aber:** `document.getElementById('asset-strip')`
→ `null` auf der Live-Seite. Ursache gefunden: **die Live-Instanz läuft weiterhin Release
`f96125e` (2026-08-21) — fünf Commits dahinter**, darunter A3 (`d974836`, baut genau dieses
`<div id="asset-strip">`). `docs/UPDATE_LOG.md`s oberster Eintrag ist auf `2026-08-23` datiert,
mit dem Datumswechsel auf `2026-08-24` würde `deploy.sh`s Gate (P6-X) jetzt ohnehin abbrechen.
**Kein Code-Fehler — der Knopf existiert im Repo, ist nur nie ausgeliefert worden.** P6.5-12
bleibt deshalb 🟡 ungeprüft, aus einem neuen, treffenderen Grund als zuvor.

**Deploy bewusst nicht selbst ausgeführt:** `deploy.sh` braucht `SHAREFYX_SYSTEMCTL="sudo
systemctl"` für den Restart-Schritt; `sudo -n true` bestätigte fehlende passwortlose Rechte
(`exit:1`). Genau die Art Aktion („live Dienst neu starten, beeinflusst laufende Sitzungen"),
die dieses Projekt konsequent dem Nikinger überlässt — kein Umgehungsversuch unternommen, dem
Nikinger die Optionen vorgelegt (selbst deployen / mir `sudo` geben / verschieben). **Nikinger-
Entscheidung: verschieben, Sitzung hier beenden, Test in der nächsten Sitzung.**

**Versionsbump, Nikinger-Auftrag:** `.rail__version` in `app.html` `v2.1` → `v2.2` (reiner
Hardcode wie die Wortmarke selbst, kein Test pinnt den String, kein Schema). Reitet mit dem
nächsten Deploy mit.

**Teardown:** Test-Asset `ast_2cf1ce2f` auf `itm_ee1e0323` per `p7_13_teardown.py` in `_trash/`
verschoben. Die Markdown-Referenz `![p65-browser-test.png](asset:ast_2cf1ce2f)` bleibt im Body
stehen (rendert nach dem nächsten Deploy als Alt-Text, V73-Konsequenz — bewusst nicht vorab per
Skript entfernt, da genau dieser Übergang Teil des nächsten P6.5-12-Nachweises ist).

**`pytest -q` weiterhin 843 passed.** Kein Quellcode dieser Sitzung geändert außer dem
Ein-Zeilen-Versionsbump; Tabu-Diff unverändert leer.

**Nächster Schritt, konkret:** vor der nächsten P6.5-12-Probe braucht es (1) einen neuen
`docs/UPDATE_LOG.md`-Eintrag datiert auf den Deploy-Tag (P6-X-Gate) und (2) einen echten
`deploy.sh`-Lauf durch den Nikinger (`sudo systemctl`-Rechte nötig). Danach: derselbe
Browser-Test wiederholen (Upload → Entfernen-Knopf → Alt-Text-Rendering →
`_trash/`-Dateiprüfung) — diesmal sollte `asset-strip` im DOM erscheinen. A6 bleibt bis
2026-08-28 (`token_families`) bzw. 2026-10-27 (`clients`) beobachtend offen, kein weiterer
Handgriff nötig.

**Nachtrag, 2026-08-25 — beide offenen Punkte erledigt, echter Deploy gefahren.** `docs/
UPDATE_LOG.md` bekam den neuen `## 2026-08-25`-Eintrag (Bild-Entfernen-Knopf angekündigt),
committet als `53bad20`. Danach fuhr der Nikinger `deploy.sh main` selbst (`sudo systemctl`-Recht
nötig, Claude Code hat das nicht). **Ergebnis, per Transkript:** Update-Log-Gate bestand ohne
Override, Health-Gate `/ui/login`→200/`/api/v1/me`→401/`/mcp/`→401 alle grün, Retention räumte
das älteste Release (`20260813...`) ab, JSON bestätigt `"result":"ok"`. **Read-only
gegengeprüft:** `readlink -f /opt/sharefyx/current` → `/opt/sharefyx/releases/
20260825T110849.160586Z`, `git -C /opt/sharefyx/current log --oneline -1` → `53bad20`, exakt der
Doku-Commit von oben — die Live-Instanz läuft damit fünf Commits weiter als vorher (`f96125e`)
und enthält jetzt A3s `<div id="asset-strip">`. **P6.5-12 ist damit wieder testbar, noch nicht
erneut geprobt** — nächster Schritt bleibt derselbe Browser-Test wie oben beschrieben, nur ohne
den Deploy-Blocker davor.

**Nachtrag, 2026-08-25 — P6.5-12/P7-5 per echtem Browser-Klick bestanden.** `testnutzer-p7` war
bereits über eine vom Nikinger geöffnete Tab eingeloggt (Cookie), meine eigene MCP-Tab teilt das
Cookie, aber `sessionStorage`s `sfx:csrf` ist tab-lokal und wird nur von der
`/ui/login`-Bootstrap-Antwort gesetzt (derselbe Mechanismus wie am 2026-08-23) — ein erster
Schreibversuch (Item anlegen) schlug entsprechend mit `CSRF-Token fehlt oder stimmt nicht` fehl.
Der Nikinger loggte sich erneut in der von mir gesteuerten Tab ein (eigenes Terminal, Zugangsdaten
nie durch mich gelesen); `sessionStorage.getItem('sfx:csrf')` bestätigte danach einen Token.

**Testablauf, per Transkript:** Item `itm_26f8d0b7` angelegt, `p65-retest.png` (4×4-PNG, per
PIL erzeugt) über `file_upload` + den echten Datei-Input hochgeladen, Asset-Chip
`ast_e60e8d8a` samt „×"-Knopf erschien im Asset-Strip (`ref_251`, ARIA-Label bereits „Bild
entfernen" — die vorher fehlende Fläche existiert jetzt wirklich im DOM). Vorschau bestätigte
das Bild vor dem Entfernen (`naturalWidth/Height:4`, korrekter `src`). „Bild entfernen" geklickt
→ Bestätigungsdialog „wird aus dem Dokument entfernt und in den Papierkorb des Items
verschoben" → bestätigt → Toast „Bild entfernt.". Vorschau danach: `p65-retest.png` als reiner
Text, kein `<img>`, kein Broken-Icon.

**Read-only gegengeprüft, nicht nur den Toast vertraut:** `.md`-Datei enthält weiterhin exakt
`![p65-retest.png](asset:ast_e60e8d8a)` — der Server schreibt die Referenz beim Entfernen nicht
um, nur die fehlende Asset-Datei macht sie zum Alt-Text (N5-Design, wie geplant). Datei liegt
real unter `_assets/itm_26f8d0b7/_trash/ast_e60e8d8a.png`. `git log` zeigt vier saubere,
getrennte Commits: `create` → `asset` → `update` (die `asset:`-Referenz im Body) →
`asset_trash` — kein Commit vermischt zwei Aktionen. Testitem danach archiviert
(`_archive/itm_26f8d0b7__...`), Trash-Asset bewusst nicht angerührt (ist der Beweis).

**Ergebnis: P6.5-12 ✅, P7-5 ✅ (via `testnutzer-p7`, gleicher Substitutionsgrund wie
P6.5-8/13 — dieselbe serverseitige Fläche, kein Bug-Risiko durch den Principal).**
`phase6_5_tools_images/CLAUDE.md` Abnahmestand jetzt **13 von 14** (nur noch P6.5-14 offen,
strukturell Nikinger-Sache). Modul-Status-Tabelle oben (P7-5) nachgezogen.

**Verifiziert:** keine Testsuite gelaufen (reine Live-Browser-/Doku-Session, kein Python-Diff).
Tabu-Diff nicht relevant.

**Offen für die nächste Session:** P7-9 (A6-Purge-Rückgang, `token_families` ab 2026-08-28,
`clients` ab 2026-10-27, rein beobachtend) — sonst nichts Neues aus dieser Sitzung.

**Nachtrag, 2026-08-25 — P7-1/P7-2/P7-7 per echtem Browser-Klick bestanden, git-Reparatur
zwischendurch.**

**Git-Zwischenfall (vor den Proben, beim Recherchieren von `p7_11_setup_fixture.py`):** `git
log` scheiterte mit `fatal: bad object HEAD` — der Commit `ef2e6be` (vorheriger Nachtrag dieser
Sitzung) war als acht 0-Byte-Objekte auf der Platte gelandet, alle mit demselben Zeitstempel
(13:28) — ein unterbrochener `git commit`-Schreibvorgang, isoliert auf genau dieses eine
Ereignis (`git reflog`/frühere Commits intakt, Arbeitskopie-Inhalt per `grep` gegengeprüft und
vollständig). **Reparatur nach expliziter Nikinger-Freigabe** (`git update-ref
refs/heads/main 6fb3eda...`, dann die acht verwaisten 0-Byte-Objekte gelöscht, `git read-tree
HEAD` gegen den stale Cache-Tree im Index, `touch` + `git add` + `git commit` neu) — Ergebnis
`6e60dbd`, `git fsck --full` danach sauber (nur harmlose dangling Objekte + eine veraltete
Reflog-Zeile, keine echte Beschädigung mehr). Kein Datenverlust: derselbe Inhalt, neuer,
gültiger Commit.

**P7-1 ✅, P7-2 ✅, P7-7 ✅** — Details in der Modul-Status-Tabelle oben. Zwei Nebenfunde beim
Bauen:
- **Freigeben-Dialog für `testnutzer-p7` ist strukturell leer**, nicht kaputt — `dialogs.js:262-
  266` (P6-V) listet nur `state.spaces`, und `testnutzer-p7` kennt (space-level) keinen anderen
  Space. Exakt der Fall, für den `p7_11_setup_fixture.py` existiert; hier zusätzlich bestätigt,
  dass ein leerer `Speichern`-Klick ein echtes, harmloses No-op-PATCH auslöst (Version bumpt, kein
  Fremdfeld erscheint) statt gar nichts zu tun.
- **`navigator.clipboard.readText()` per `javascript_tool` hängt den Tab auf** (45s-Timeout,
  „renderer möglicherweise eingefroren") — vermutlich ein Chrome-Berechtigungsprompt außerhalb
  des DOM, den Screenshots nicht zeigen. Nicht weiter verfolgt, seitdem gemieden: DOM-sichtbare
  Bestätigungen (Toast-Text, Quellcode-Verifikation der `.then()`-Kette) reichen als Beweis und
  sind ohnehin die robustere Prüfung.

**Aufräumen:** `p7_11`-Fixture-Freigabe (`share_read:[testnutzer-p7]` auf `itm_3d0ac2b3`) bewusst
**nicht** zurückgenommen — falls P7-2 später erneut vorgezeigt werden soll, ist die Fixture
sofort wieder nutzbar; Rücknahme ist Teil des ohnehin fälligen P7-12-Abbaus. Testitem `itm_
68f0251d` archiviert (`_archive/`), Test-Ordner `p7-7-test` bleibt (kein Lösch-Mechanismus für
leere Ordner in der UI, kein Schaden).

**Verifiziert:** kein Python-Code geändert (nur `.md`), Tabu-Diff nicht relevant. Kein `pytest`-
Lauf nötig — reine Live-Browser-/Git-Reparatursession.

**Damit bleiben aus dem P7-A-Rest nur noch: P7-4 (braucht Niklas selbst mit einem echten
Connector-Gespräch — nicht durch Claude Code allein herstellbar), P7-9 (kalendergebunden,
2026-08-28/2026-10-27) und P7-12 (Testnutzer-Abbau — laut eigenem Docstring „am Ende von Block
A"; mit P7-1/2/5/6/7/8/10/11/12b jetzt erledigt ist nur noch P7-9 offen, das `testnutzer-p7`
nicht braucht — der Abbau ist damit möglich, aber eine Nikinger-Entscheidung, kein automatischer
nächster Schritt).**

**Nachtrag, 2026-08-25 — P7-4 erster echter Befund (❌), P7-12 bewusst NICHT geschlossen.**

**P7-4:** Nikinger fragte im Webchat (Doku-Stand dort veraltet, unerheblich für diesen Befund)
„welche 3 Items sind die aktuellsten" — eine organische, ungestellte Probe genau des P7-4-
Kriteriums. Antwort kam als Tabelle mit jeder Zeile eingeleitet durch die rohe `itm_…`-ID, Titel
nur angehängt (`itm_3d0ac2b3 — P7-11 Sichtbarkeitsprobe...`). Das widerspricht dem Satz, der
wortgleich in vier Tool-Beschreibungen steht (`mcpserver/tools.py`: „Nenne einem Menschen
gegenüber immer den Titel eines Items, nicht seine itm_...-ID"). Kein Code-Fehler — die
Prosa-Anweisung reicht offenbar nicht gegen den Sog einer tabellarischen Antwort, wo `id` als
Feldname aus `search_items`s eigenem Rückgabeschema naheliegt. Modul-Status-Tabelle oben
(P7-4 ❌) nachgezogen. Bleibt ein UX-/Formulierungs-Befund, keine neue Aufgabe ohne
Nikinger-Entscheidung, ob/wie die Tool-Beschreibung geschärft werden soll.

**P7-12 — Nikinger-Auftrag „schließen, falls für spätere Blöcke nicht gebraucht" geprüft, Ergebnis:
gebraucht.** Gegen den Plan geprüft, nicht gegen den eigenen Docstring von `p7_11_setup_fixture.py`
(der nur „am Ende von Block A" sagt, ohne Block C zu kennen): `docs/concepts/
phase7_spaces_admin_plan.md` §Block C, **P7-14** — „Ein Mensch gibt seinen eigenen Space im
Browser für einen anderen zum Lesen frei; der andere sieht ihn danach", Wer: **Niklas +
`testnutzer-p7`**. Block C ist komplett ungebaut (P7-14–P7-22 alle ⬜) und braucht `testnutzer-p7`
ausdrücklich als Empfänger-Principal. **Ein Abbau jetzt („Block A ist fertig") würde P7-14 später
zwingen, den Principal neu anzulegen** — Mehrarbeit statt Ersparnis, und der Plan selbst enthält
diesen Widerspruch bereits (A7s „Abbauen, am Ende von Block A" wurde offenbar geschrieben, bevor
Block C den Principal als Testpartner brauchte). **Datierte Korrektur:** P7-12 bleibt bis nach
Block C offen, nicht „am Ende von Block A" — der Plan-Snapshot selbst bleibt unverändert (📕),
diese Zeile hier ist die maßgebliche Korrektur. Kein Handgriff ausgeführt, keine Löschung.

**Nachtrag, 2026-08-25 — Gate A→C geprüft: alle vier Punkte live, Block C gestartet (Nikinger-
Auftrag „next block should be unblocked").**

**Gate-Prüfung** (Plan `docs/concepts/phase7_spaces_admin_plan.md` §0/Block-C-Vorspann, vier
Punkte, alle vier live vor der ersten Zeile Block-C-Code):

| # | Kriterium | Beleg |
|---|---|---|
| 1 | Item per `itm_…`-ID im Browser gefunden | P7-1 ✅ (siehe oben) |
| 2 | Bild entfernbar, Alt-Text-Rendering, Datei in `_trash/` | P7-5 ✅ (siehe oben) |
| 3 | Migration gelaufen, 0 Dateien ohne `visibility:` | P7-8 ✅ (73/73) |
| 4 | `testnutzer-p7` echter Cross-Principal-Lesetest | P7-11 ✅ (Web-UI **und** MCP) |

Alle vier bereits vor dieser Sitzung geschlossen, hier nur formal gegen den Plan-Wortlaut
nachgeprüft — **Gate offen, Block C gestartet.**

**Step C1 gebaut — Schreibseite von `.share.yml` in `storage/acl.py` (sechste Contract-
Öffnung, P7-P).** Reine Extraktion aus `phase6_shares/scripts/spacectl.py`
(`_load_share_file`/`_dump_share_file`/`_spaces_referencing`, Schreibbodies von
`_cmd_create_space`/`_cmd_add_member`/`_cmd_remove_member`/`_cmd_remove_space`), kein neues
Verhalten. Anker vor dem Bau gegen den echten Code geprüft (nicht nur den Plan-Snapshot
übernommen) — Zeilennummern im Plan wichen leicht ab (Funktionen um wenige Zeilen gewachsen seit
`f5691e0`), Funktionsnamen stimmten exakt, wie vom Plan selbst vorgeschrieben.

Neu in `acl.py`: `read_share_file`/`write_share_file`/`add_member`/`remove_member`/
`create_space`/`remove_space_dir`/`spaces_referencing`/`AclWriteError`, plus `_WriteLock`
(dieselbe Bauart wie `spacectl.py`s bisherige `_DataRootLock`, jetzt die einzige verbleibende
Kopie). Jede Schreibfunktion nimmt den `.write.lock`-Flock selbst und gibt ihn vor der Rückkehr
frei — kein Aufruf einer `Store`-Methode darin (P7-M, Selbst-Deadlock-Vermeidung). `spacectl.py`
ruft jetzt `acl.*` auf; `_DataRootLock` ist komplett entfallen, `_load_share_file`/
`_find_share_files` bleiben (nur noch für `check`, rein lesend). Modulkopf-Docstring von
`spacectl.py` entsprechend nachgezogen (die Lock-Beschreibung war sonst stale gewesen).

**Verifiziert:** `phase6_shares/tests/test_spacectl.py` (20 Tests) **unverändert**, weiterhin
grün — der Regressionsbeweis der Extraktion. `phase6_shares/tests/test_characterization.py` (3
Golden Files) vor und nach byte-identisch grün (P7-C/P6-D). 19 neue Tests in
`phase7_spaces_admin/tests/test_acl_write.py`. Ein eigener Testfehlschlag korrigiert vor dem
Commit, kein Code-Fund: `test_remove_member_removes_from_both_lists` nahm fälschlich an, ein
`write=True`-Add trage den Namen auch in die Roh-Liste `read:` ein — `write:` impliziert `read:`
nur beim Lesen (`AclReader._parse`), nicht in der Datei selbst; Test korrigiert, schreibt den
Doppel-Eintrag jetzt direkt, um den echten Zwei-Listen-Entfernen-Pfad zu prüfen. `pytest -q`
volle Suite: **843 → 862** (Baseline vor dieser Sitzung read gegengezählt, nicht angenommen).
Tabu-Diff (`asgi.py`/`server.py`/`permissions.py`/`authserver/{crypto,totp,passwords,resolver,
flows}.py`) leer.

**Nachtrag, 2026-08-25 — Advisor-Runde nach dem C1-Commit, vier Funde, alle vier behoben in
einem Folgecommit.** Versäumnis vorweg: der Advisor-Call vor dem Commit (Standing-Feedback
dieses Projekts) wurde übersprungen, erst danach nachgeholt. `409fe18` wurde bewusst **nicht**
amended (Projektregel) — die vier Funde landen als eigener Commit mit eigenem Doku-Update.

1. **Dead Code + versteckte Divergenzquelle:** `write_share_file()` inlinete `yaml.safe_dump`+
   `atomic_write`+leer-löschen ein drittes Mal, `add_member`/`remove_member` je ein zweites Mal —
   und `write_share_file()` konnte von den beiden nie aufgerufen werden (P7-M-Deadlock, es nimmt
   den Lock selbst, sie halten ihn schon). Genau die Divergenzquelle, die P7-P verhindern sollte,
   nur ins Modul verlagert statt entfernt. **Behoben:** neues privates
   `_write_share_file_unlocked(path, data)` hält die Dump-Logik einmal; `add_member`/
   `remove_member` rufen es innerhalb ihres Locks auf, `write_share_file()` bleibt der
   öffentliche, lockende Wrapper darum. Der Deadlock ist jetzt durch Bauart unerreichbar, nicht
   nur per Kommentar vermieden.
2. **Commit-Betreffs waren nie gepinnt.** Der Plan verlangt die drei exakten Formate (`share
   <space> <key>+=<name>` / `unshare <space> <name>` / `remove-space <name>`) — genau das Stück,
   das die `DATA_ROOT`-Historie (Hard Rule 5, Undo-Pfad) leise brechen könnte, war ungeprüft.
   **Behoben:** die drei Commit-Tests in `test_acl_write.py` assertieren jetzt zusätzlich `git
   log -1 --format=%s` gegen den exakten Wortlaut.
3. **`phase1_storage/CLAUDE.md`s Modul-Tabelle fehlte Zeile 14** für die sechste Öffnung — der
   „Geerbte Contracts"-Absatz war da, die Tabellenzeile (Präzedenzfall: Zeile 13 bei der fünften
   Öffnung) fehlte. Nachgetragen, `Gesamt: 150` unverändert (Tests liegen außerhalb des Pakets,
   dieselbe Konvention wie Zeile 10).
4. **`acl.py`s Kopf-Docstring war nach dem Umbau falsch** — beschrieb das Modul weiterhin als
   rein lesend/fail-closed. Nachgezogen: zwei Sätze, die den bewussten Zwei-Pfade-Schnitt nennen
   (lesend fail-closed via `AclReader`, schreibend laut via `read_share_file`/`add_member`/…).

**Verifiziert:** 43/43 (`test_acl_write.py` + `test_spacectl.py` + Charakterisierung), volle
Suite **862/862** unverändert (Umbau, keine neuen Tests — drei bestehende umbenannt/erweitert).
Tabu-Diff weiterhin leer.

**Zweite Advisor-Runde, diesmal vor dem Commit (wie es sein soll), vier weitere Funde, alle
behoben:**

1. **`_dump_share_file` in `spacectl.py` war tot** — meine erste Edit-Runde ersetzte beide
   Aufrufer (`_cmd_add_member`/`_cmd_remove_member`), ließ die Funktionsdefinition selbst aber
   stehen (sie lag außerhalb des ersetzten `old_string`-Bereichs). Entfernt. Die Modul-Tabellen-
   zeile oben widersprach sich zusätzlich selbst („`_load_share_file` entfällt … bleibt") —
   richtiggestellt: entfallen sind `_DataRootLock`/`_dump_share_file`/`_spaces_referencing`,
   geblieben sind `_load_share_file`/`_find_share_files` (nur noch für `check`).
2. **`read_share_file()`s `AclWriteError`-Zweig (nicht-Mapping-YAML) war ungetestet** — die
   bestehende Malformed-YAML-Probe pinnt nur den `yaml.YAMLError`-Zweig. Zwei neue Tests: einer
   direkt gegen `read_share_file()`, einer gegen `add_member()` mit demselben kaputten Bestand
   (weder `add_member` noch `remove_member` fangen die Exception ab — bewusst, dieselbe „laut
   statt fail-closed"-Haltung wie beim direkten Lesen, kein Verhaltensunterschied zur alten
   `spacectl.py`-Fassung, die genauso unabgefangen `ValueError` warf).
3. **Plan-Testfall „leere Liste verschwindet" fehlte** — bisher nur „leere Datei wird entfernt"
   abgedeckt. Neuer Test: `read:`+`write:` beide besetzt, ein Name aus `read:` entfernt macht
   `read:` leer → der Schlüssel fehlt danach ganz (nicht `read: []`), die Datei bleibt (wegen
   `write:`) bestehen.
4. **`write_share_file()` hatte keine eigene Testabdeckung** — zwei neue Tests: Round-Trip durch
   `read_share_file()`, und leeres `data` entfernt eine bestehende Datei.

**Verifiziert (zweite Runde):** `test_acl_write.py` jetzt **24** Tests (`--collect-only`
gegengezählt, nicht addiert), zusammen mit `test_spacectl.py`+Charakterisierung **48/48** grün.
Volle Suite **862 → 867** (real gezählt). Tabu-Diff weiterhin leer.

**Nächster Schritt, konkret:** Step C2 (REST-Fläche, fünf neue Routen unter `/api/v1/spaces*`,
`webui/shares.py`-Erweiterung um `require_space_reauth()`) — Anker (`api.py:743-755`,
`api_routes()`-Signatur, `UserDirectory`-Principal-Check V76) vor dem Bau gegen den echten Code
prüfen, wie bei C1. Advisor-Call **vor** dem C2-Commit, nicht danach.

**Nachtrag, 2026-08-25 — Step C2 gebaut (Nikinger-Auftrag „Lets go on with C2"), zwei
Advisor-Runden vor dem Commit.**

**Vier von fünf Routen aus Plan §4.C2** (`POST /api/v1/spaces`, `GET/POST .../members`,
`DELETE .../members/{name}`) — `DELETE /api/v1/spaces/{space}` bleibt bewusst C4, siehe
Modul-Tabelle oben. Anker vor dem Bau geprüft: `api_routes()`-Signatur trägt bereits alles
Nötige (keine neue Parameter), Route-Tabelle liegt bei `api.py:779-802` (Plan nennt 743-755,
kosmetische Zeilendrift wie bei C1). **Ein Plan-Textfund:** §4.C2 beschreibt eine Extraktion
von `require_share_reauth()`s Credential-Hälfte in `_verify_reauth_credentials()` — diese
Extraktion existiert bereits, als `webui/reauth.py :: verify_reauth()`, gebaut vor dieser Phase
und von `account.py` UND `shares.py` bereits geteilt. `require_space_reauth()` ruft sie direkt
auf, keine Restrukturierung von `shares.py` nötig — der Plan-Text war insofern stale, spart
aber Arbeit, kostet keine.

**Erste Advisor-Runde (vor dem ersten Commitversuch), zwei Blocker + zwei Doku-Lücken:**

1. **Frisch angelegter Space war für niemanden sichtbar oder verwaltbar.**
   `acl.create_space()` legt bewusst nur ein leeres Verzeichnis an (dieselbe Zurückhaltung wie
   `spacectl.py create-space`, ein CLI-Operator ruft danach selbst `add-member` auf) — über die
   Weboberfläche gibt es diesen zweiten Handgriff aber nicht. **Fix:** `_spaces_post` seedet den
   Anlegenden direkt danach als `write`-Mitglied (`acl.add_member(..., write=True)`) — zwei
   Commits (`create-space` selbst committet nichts, der Seed-`add_member` einen), korrekt: die
   Mitgliedschaft ist eine echte Rechteänderung und gehört in die Historie. Ohne den Fix hätte
   P7-16 („neuer geteilter Space erscheint im Baum") strukturell nie bestehen können.
2. **`GET .../members` hatte gar keine Autorisierung.** Die Plan-Begründung dafür („spiegelt
   `GET /api/v1/spaces`, das zeigt Mitgliedschaft auch") war sachlich falsch — `_spaces` filtert
   über `_visible_space_infos()`/`permissions.visible_spaces()`, der neue Handler nahm `space`
   ungeprüft aus dem Pfad. Das öffnete ein Existenz-Orakel über beliebige Space-Namen,
   Mitglieder-Enumeration für nicht-lesbare Spaces, und (über `orphans`) einen Leak-Kanal quer
   über den ganzen `DATA_ROOT`. **Fix:** `permissions.can_read(session.space, space)`-Gate,
   `403` sonst; `manageable` bleibt der Render-Hinweis fürs Frontend.
3. `space_admin`-Feld in `_meta` war ungetestet — nachgetragen (`test_meta.py`).
4. Kill-Switch-Abdeckung nur 2 von 4 Routen — auf einen parametrisierten Test über alle vier
   ausgeweitet.

**Zweite Advisor-Runde (nach den ersten vier Fixes, vor dem tatsächlichen Commit), ein
weiterer Blocker:** `orphans` implementierte den falschen Namen — der Plan-Satz nennt
`acl.spaces_referencing()`, beschreibt aber „Namen ohne zugehörigen Space" — das ist
`spacectl.py check`s Semantik (Tippfehler in `read:`/`write:` gegen bekannte Space-Verzeichnisse
prüfen), nicht „wer verweist auf mich" (das ist tatsächlich `spaces_referencing()`s Job, und
C4s eigene Sache). **Fix:** `_space_members_get` vergleicht `grant.read | grant.write` jetzt
gegen die real existierenden Space-Verzeichnisse (`store.data_root.iterdir()`), dieselbe
Prüfung wie `_cmd_check`. Die `not is_home`-Ausnahme ist mit dem Fix ebenfalls gefallen — ein
Tippfehler im eigenen Home-Space ist genauso meldenswert. **Datierte Plan-Korrektur, wie bei
C1s P7-12-Zeitpunkt:** §4.C2s `orphans`-Beschreibung war intern widersprüchlich (Funktionsname
vs. beschriebenes Verhalten); der 📕-Snapshot bleibt unverändert, diese Zeile ist die
maßgebliche Korrektur.

**`atomic_write()`-Randfrage aus der ersten Runde geklärt, kein Fund:** `tempfile.mkstemp(dir=…)`
wirft `FileNotFoundError` auf einem fehlenden Space-Verzeichnis, legt keine Elternverzeichnisse
an — `acl.add_member()` auf einen nicht existierenden Space kann `create_space()`s
Namens-Riegel also nicht umgehen. Nichts zu tun, für C4 vermerkt.

**Verifiziert:** 21 neue Tests in `test_space_admin_api.py` (eigene Fixtures — `phase5_ui/tests/
conftest.py` ist kein Vorfahre von `phase7_spaces_admin/tests/`, dieselbe Isolation wie
`test_acl_write.py`), +1 `test_meta.py`, +1 `test_store.py` (`Store.data_root`-Property). Alle
gegen `--collect-only` gezählt, nicht addiert. Volle Suite **867 → 890**. Tabu-Diff leer.

**P7-22 bleibt ⬜, explizit benannt statt stillschweigend:** „`space_admin_enabled=False` lässt
alle fünf Routen `404` antworten" — vier von fünf sind jetzt getestet (parametrisierter
Kill-Switch-Test), die fünfte (`DELETE /api/v1/spaces/{space}`) existiert erst mit C4. „C2
fertig" heißt hier ausdrücklich nicht „P7-22 erfüllbar".

**Nächster Schritt, konkret:** Step C4 (Space entfernen, zweiphasig, P7-O/N8/N9) vor C3 (UI) —
C3s Entfernen-Dialog bräuchte sonst eine Route, die noch nicht existiert; C4 zuerst gibt C3 ein
vollständiges Backend in einem Rutsch. Anker vor dem Bau prüfen: `_STORE_FETCH_LIMIT`
(V78), `store.move()`/`store.archive()`-Reihenfolge, Lock-Disziplin (P7-M) für die
Vorlauf/Durchlauf-Schleife. Advisor-Call **vor** dem Commit.

**Nachtrag, 2026-08-25 — Step C4 gebaut (Nikinger-Auftrag „lets go on with C4"), ein
Advisor-Fund vor dem Commit behoben.**

Anker gegen den echten Code geprüft, nicht nur den Plan-Snapshot übernommen:
`_STORE_FETCH_LIMIT` (`api.py:145`, Plan nennt `144` — dieselbe Ein-Zeilen-Drift wie bei C1/C2),
`store.archive()`/`store.move()` (`store.py:586–663`, Reihenfolge durch `archive()`s
`folder=""`/`_archive/`-Ablage erzwungen — ein vorheriger `move()` würde die Datei sonst an die
Zielspace-Wurzel setzen, nicht ins Zielarchiv), `acl.remove_space_dir()` (`acl.py:291–301`,
kein eigener Vorlauf — das ist ausdrücklich C4s Job), `require_space_reauth()`
(`shares.py:96–121`, flacher `widening`-Flag statt `widens()`-Vergleich, exakt wie geplant).

`webui/api.py :: _spaces_delete` — fünfte Route `DELETE /api/v1/spaces/{space}`. Reihenfolge wie
im Plan: P7-K (bekannter Principal → 403) → P7-L (`can_write(home, space)` → 403) → Vorlauf
(`store.search()`-Paging über `_STORE_FETCH_LIMIT`, Blocker-Scan) → `require_space_reauth
(widening=True)` + `confirm == space` → Durchlauf (`move()`→`archive()` je Item, `ConflictError`
→ Abbruch mit beiden Listen) → harte `len(moved) == total`-Sperre → `acl.remove_space_dir()`.
Antwort trägt zusätzlich `orphan_refs` (`acl.spaces_referencing()`, vor dem `rmtree` berechnet,
da danach die eigene `.share.yml` des entfernten Space nicht mehr existiert).

**Advisor-Fund vor dem Commit (empirisch verifiziert, nicht nur behauptet):** ein Testfall mit
einem bereits archivierten Item im Zielspace fehlte. Direkt geprüft (`store.create()` +
`store.archive()` + `store.search()` gegen ein Wegwerf-`tmp_path`): `search()`s `total` zählt
archivierte Items mit, `store.move()` verbietet sie aber ausdrücklich
(`ValidationError("... ist archiviert — move verboten")`, `store.py:626–627`). Ohne einen
eigenen Riegel hätte das einen unbehandelten `ValidationError` mitten im Durchlauf ausgelöst —
ein `500` nach bereits verschobenen Items, ohne den von N9 verlangten Bericht mit beiden Listen.
**Behoben:** ein zweiter, eigener Vorlauf-Riegel (`archived_blockers`) lehnt die Entfernung
fail-closed ab, wenn der Space bereits archivierte Items enthält — genau wie beim
Schreib-Blocker wird dabei **nichts** bewegt. **Das ist eine bewusst offene Frage, keine stille
Lücke:** N8 sagt, Items sterben nie — aber der Store hat keine API, ein bereits archiviertes
Item in einen anderen Space zu verschieben. Eine Space mit Historie ist damit vorerst
unentfernbar. Ob das dauerhaft tragbar ist oder eine siebte, benannte Contract-Öffnung braucht
(`storage/store.py` bekäme eine Move-Variante für archivierte Items), ist eine Nikinger-
Entscheidung — dieser Commit trifft sie nicht, sondern hält die Grenze fail-closed.

**Zweiter, kleinerer Advisor-Fund:** `acl.spaces_referencing()` fehlte das `exclude=`, das
`spacectl.py remove-space` für dieselbe Prüfung setzt (die eigene `.share.yml` des entfernten
Space zählt dort nicht als Fremdreferenz auf sich selbst) — Parität-Drift gegen P7-Ks „volle
`spacectl.py`-Parität", behoben (`exclude=store.data_root / space / acl.ACL_FILENAME`).

**Ein weiterer, unabhängig entdeckter Fund beim Testen (kein Advisor-Fund, sondern ein eigener
Testflakiness-Fehler dieser Session):** der erste Entwurf des Konflikt-Abbruch-Tests nahm an,
`store.search()` liefere Items in Erstellungsreihenfolge — im vollen `pytest`-Lauf (echte
Wanduhr statt eines injizierten `now_fn`, `item_store`-Fixture hier bewusst ohne `now_fn` wegen
der Git-Commit-Reihenfolgeprüfungen) zeigte sich, dass die tatsächliche Suchreihenfolge davon
abweicht. Test korrigiert: er fragt `store.search()` selbst nach der Verarbeitungsreihenfolge,
statt eine Reihenfolge anzunehmen, die `_spaces_delete` nirgends verspricht.

**Kill-Switch-Testlücke aus dem C2-Commit geschlossen:** `test_space_admin_api.py`s
parametrisierter Kill-Switch-Test deckte bis jetzt nur vier von fünf Routen ab (die fünfte
existierte zum Zeitpunkt von C2 noch nicht). Um die neue `DELETE /api/v1/spaces/{space}`-Zeile
ergänzt — schließt den Testanteil von P7-22, der sonst als offener Rest hätte weitergetragen
werden müssen.

**Abnahmestand:** P7-20 ✅ *mit Vorbehalt* (der Schreib-Blocker ist unter der echten Union-ACL-
Semantik — `AclReader.grants_for_dir()` unioniert immer den Space-Root-Grant — mit echten
`.share.yml`-Daten unerreichbar, siehe Kommentar in `_spaces_delete`; der Test simuliert die
Divergenz direkt. Der archivierte-Item-Blocker aus demselben Kriterium ist dagegen real
erreichbar und eigenständig getestet). P7-21 ✅. P7-22 Testanteil geschlossen, Browser-Anteil
bleibt C3. Modul-Status-Tabelle (Zeile 11) und Abnahmestand-Tabelle oben nachgezogen.

**Verifiziert:** 8 neue Tests in `phase7_spaces_admin/tests/test_space_removal.py` (Vorlauf-
Blocker × 2 — Schreibrecht + bereits archiviert —, sauberer Durchlauf, Assets wandern mit, zwei
Commits je Item + ein `remove-space`-Commit, Verzeichnis weg, `ConflictError`-Abbruch mit beiden
Listen, Home-Space-Riegel, Re-Auth+Bestätigung), +1 in `test_space_admin_api.py` (Kill-Switch-
Zeile). Volle Suite **890 → 900**, real gezählt (`pytest -q`, nicht addiert). Tabu-Diff
(`asgi.py`/`server.py`/`permissions.py`/`authserver/{crypto,totp,passwords,resolver,flows}.py`)
leer. Kein neuer Contract-Absatz nötig — C4 fügt `storage/` nichts hinzu, es ruft nur bereits
bestehende Funktionen (`store.search/move/archive`, `acl.remove_space_dir/spaces_referencing`)
aus `webui/api.py` heraus auf.

**Nächster Schritt, konkret:** C3 (UI) — Entfernen-Dialog gegen die jetzt vollständige C2/C4-
REST-Fläche, Kill-Switch tatsächlich verdrahten (schließt P7-22s Browser-Anteil und macht
`space_admin_enabled` erstmals produktiv scharf), Home-Space-Ausnahme im Menü (P7-18s
Browser-Anteil). Danach Step C5 (Betrieb/Doku).

**Nachtrag, 2026-08-25 — Nikinger-Entscheidung zur oben offen gelassenen Frage: siebte
Contract-Öffnung statt dauerhaftem `archived_blockers`-Riegel.**

Auf Nachfrage empfohlen (Begründung: eine Space mit `_archive/`-Inhalt ist der Normalfall, nicht
der Ausnahmefall — jede Space mit echter Nutzungshistorie hätte sonst permanent unentfernbar
bleiben müssen, das widerspricht N8 direkter als eine kleine Erweiterung des Contracts es tut),
vom Nikinger bestätigt („do that then").

**Umgesetzt in `phase1_storage/storage/store.py`** (Anker vor dem Bau geprüft: `move()` bei
`store.py:617–663`, `_write_item_file()` bei `276–291`, `create()` bei `463–489`, alle drei
Guard-Vorkommen `"ist archiviert"` bei Zeilen 493/544/570/627 gegengezählt — nur `move()`s
Guard bei 627 wird relaxiert, die drei anderen (`update`/`append`/`patch`) bleiben unverändert):

- `move()`: der Guard `if current.status == "archived": raise ...` wird zu
  `if current.status == "archived" and folder not in (None, ""): raise ...` — ein reiner
  Space-Wechsel ist jetzt erlaubt, ein echter Ordner-Wechsel bleibt verboten (archivierte Items
  tragen nie eine Ordnerposition).
- `_write_item_file()` bekommt einen Sonderfall: `item.status == "archived"` routet den
  Zielpfad auf `<space>/_archive/<file>` statt über `files.item_path()` (das `_archive/` nicht
  kennt) — dieselbe Pfad-Sonderbehandlung, die vorher exklusiv `archive()`s eigener,
  separater Code hatte, jetzt am gemeinsamen Schreibpfad. Vor diesem Fix hätte ein `move()`
  auf ein archiviertes Item die Datei an die Ziel-Space-Wurzel gesetzt — physisch „entarchiviert“,
  während das Frontmatter weiter `status: archived` behauptet hätte.
- **Zweiter Advisor-Fund, vor demselben Commit:** `create(status="archived")` ist über
  `POST /api/v1/items` erreichbar (`_items_post`s Feld-Whitelist enthält `status`,
  `STATUS_VALUES` erlaubt `archived` für `note` **und** `task` seit der P2-Öffnung) und lief am
  ursprünglichen `move()`-Guard naturgemäß nie vorbei — der `_write_item_file()`-Fix hätte hier
  aber eine neue Divergenz erzeugt (Datei landet in `_archive/`, das zurückgegebene `Item`-Objekt
  im Speicher trägt trotzdem noch das angeforderte `folder`, bis der nächste `get()` es aus dem
  echten Pfad neu ableitet und verwirft). **Fix:** `create()` setzt `folder=""` selbst, sobald
  `status="archived"` — dieselbe Zurücksetzung, die `archive()` seit je her vornimmt, hier nur
  vorgezogen. Ein direkt als `archived` angelegtes Item verhält sich damit identisch zu einem,
  das später archiviert wurde.
- `_spaces_delete` (`webui/api.py`) verliert den `archived_blockers`-Riegel aus dem vorherigen
  Commit ersatzlos; der Durchlauf ruft `archive()` nur noch für Items auf, die `move()` nicht
  bereits als `status == "archived"` zurückgibt (kein doppelter Commit auf einem schon
  archivierten Item).

**Verifiziert:** `phase1_storage/tests/test_store.py`s `test_move_of_archived_item_is_rejected`
durch drei Tests ersetzt (Ordner-Wechsel weiterhin verboten, Space-Wechsel relokiert korrekt ins
Ziel-`_archive/`, genau ein `move`-Commit) + ein neuer Test für `create(status="archived")`.
`phase7_spaces_admin/tests/test_space_removal.py`s bisheriger 403-Test (`archived_blockers`)
durch einen 200-Test ersetzt, der zusätzlich gegenprüft, dass das bereits archivierte Item
KEINEN zweiten `archive`-Commit bekommt. Charakterisierung (P6-D/P7-C,
`phase6_shares/tests/test_characterization.py`) vor und nach byte-identisch grün. Volle Suite
**900 → 903**, real gezählt. Tabu-Diff weiterhin leer.

**Dated Plan-Korrektur** (wie bei C1s P7-12-Zeitpunkt und C2s `orphans`-Fund): Plan §4.C4s
Pseudocode ruft `store.archive()` unterschiedslos nach jedem `move()` auf — der tatsächliche
Code ruft es nur noch für Items auf, die nicht schon archiviert waren. Der 📕-Plan-Snapshot
bleibt unverändert, diese Zeile ist die maßgebliche Korrektur.

**Dokumentation der siebten Öffnung** (Ankündigung + Bau in derselben Sitzung, kein separater
Ankündigungs-Absatz vorher) steht vollständig in `phase1_storage/CLAUDE.md`s „Geerbte
Contracts" — Modul-Status-Zeile 15 dort, Gesamtzahl-Korrektur 150→154 (davon 151 korrigierte
Baseline aus einer übersehenen Zeile-10-Ergänzung in C2, +3 netto aus dieser Öffnung).

**Nächster Schritt, konkret:** unverändert C3 (UI) — die archivierte-Items-Frage ist jetzt
geschlossen, kein offener Posten mehr dafür.

**Nachtrag, 2026-08-25 — Step C3 gebaut (Nikinger-Auftrag „lets go on with C4" führte zu C4,
danach Rotationsversuch + Fortsetzung mit C3), ein Advisor-Fund mit zwei Teilen vor dem Commit
behoben, echter Browser-Lauf gegen eine Wegwerf-Instanz.**

**Rotationsversuch zuerst:** `scripts/rotate_session_block.sh phase7_spaces_admin` auf
Nikinger-Vorschlag gefahren — Ergebnis „Bereits konform: genau ein Session-Block im Head.
Nichts zu tun." (`exit 2`). Die ~58KB dieses Heads sind kein Rotationsrückstand (die Regel
rotiert beim Start eines NEUEN `## Session stopped`-Blocks, nicht nach Größe) — dieser Kopf
trägt seit Sitzungsbeginn genau einen Block, gewachsen über viele Nachträge derselben
fortlaufenden Sitzung. Kein Handgriff möglich, bis eine wirklich neue Session beginnt.

**C3 gebaut, drei gekoppelte Stellen in einem Commit (Plan §4.C3):** `app.html:283`s
Menüpunkt verliert `disabled`/„kommt in Phase 7" → „Spaces verwalten"; `config.py`s
`space_admin_enabled` Default `False`→`True`; `test_static_routes.py`s Stub-Test ersetzt.
**Zwei Plan-Positionen erwiesen sich als bereits erledigt, keine neue Arbeit:** `_meta`
trug `space_admin` bereits aus Step C2, `.rail__version` stand bereits auf `v2.2` aus der
A6-Session vom 2026-08-24 (P7-U) — beide Plan-Zeilen beim Nachlesen bestätigt, nicht blind
übernommen.

**Neues Modul `webui/static/js/spaces.js`** (P7-Q), Bauart wie `dialogs.js`: `initSpaces()`
im selben Muster wie die zehn bestehenden Module, `openSpaceAdminDialog()` (Liste aller
`writable`-Spaces aus `state.spaces`), `selectSpace()` (`GET .../members`, Home-Hinweis,
Mitgliederliste), Hinzufügen (immer Re-Auth wie serverseitig erzwungen, eingefroren-erste-
Fassung-Muster wie `pendingMoveBody`/`pendingShareBody`), Entfernen (kein Re-Auth),
`openRemoveSpaceDialog()` (Klartext-Konsequenz + getippte Bestätigung + Re-Auth, immer). Neue
Dialoge `#space-admin-dialog`/`#space-remove-dialog` als Geschwister von `#share-dialog`;
`app.js` bekommt `initSpaces()` im Bootstrap, beide Dialoge in `anyOverlayOpen()`/Escape,
einen Klick-Handler auf den Menüpunkt und **eine neue Zeile in `init()`**:
`document.getElementById("account-manage-spaces").hidden = !meta.space_admin` — ohne die
wäre der Kill-Switch (P7-R) nur serverseitig scharf gewesen, der Knopf bliebe sichtbar und
jeder Klick liefe in einen `404`.

**Advisor-Fund vor dem Commit, zwei Teile, beide in `spaces.js`:**
1. **Eingefrorener Hinzufügen-Request überlebt einen Space-Wechsel.** `selectSpace()` setzte
   `pendingMemberBody`/die Re-Auth-Felder nicht zurück — ein Re-Auth-Retry nach einem Wechsel
   von Space A zu Space B hätte den für A eingefrorenen Namen gegen B abgeschickt. Exakt der
   Fund, den `dialogs.js :: pendingMoveBody = null` beim Space-Wechsel im Verschieben-Dialog
   bereits kommentiert (`// Ziel geändert -- eine evtl. eingefrorene Fassung ist ungültig`) —
   hier übernommen, plus dieselbe Rücksetzung (inkl. Feldwerte) in `openSpaceAdminDialog()`,
   damit ein getipptes Passwort auch ein Schließen+Wiederöffnen des Dialogs nicht überlebt.
2. **`orphans` gelesen und verworfen.** C2s eigener Commit-Kommentar begründet `orphans`
   explizit als „der Render-Hinweis fürs Frontend" (Tippfehler-Fänger gegen bekannte
   Space-Verzeichnisse) — `selectSpace()` las das Feld nie. Jetzt als eigene Zeile in der
   Mitgliederliste gerendert („verwaist -- kein solcher Space mehr").

**Echter Browser-Lauf, Ende-zu-Ende, gegen eine Wegwerf-Instanz** (eigener Uvicorn-Prozess,
temporäres `DATA_ROOT`+`AuthStore`, `git=False`, Skript im Scratchpad, kein Repo-Teil):
Einladung→Enrollment→Login, Menüpunkt trägt kein `disabled` mehr (bestätigt per DOM-Lesung),
Dialog öffnet, `niklas`-Space zeigt den Home-Hinweis und **keinen** „Space entfernen"-Knopf,
Mitglied `fabian` (schreiben) hinzugefügt — erster Versuch ohne Credentials → `403
reauth_required`, Re-Auth-Formular erscheint, zweiter Versuch mit Passwort+TOTP → `200`,
Mitgliederliste aktualisiert. `fabian` ohne Re-Auth wieder entfernt (Toast bestätigt). Neuer
Space `team-c3-probe` angelegt (erscheint sofort im Baum, `niklas` automatisch als
Schreib-Mitglied gesät — C2s eigener Fund, hier bestätigt). `team-c3-probe` zeigt korrekt
einen „Space entfernen"-Knopf (kein Home-Space); Entfernen-Dialog zeigt den vorgeschriebenen
Konsequenztext, erster Versuch nur mit getipptem Namen → `403 reauth_required` +
„Re-Authentisierung fehlgeschlagen.", zweiter Versuch mit Credentials → `200`, Toast „Space
entfernt · 0 Item(s) archiviert", Space verschwindet aus dem Baum.

**Zwei Harness-Eigenheiten dieser Sitzung, für die nächste Session festgehalten (kein
Code-Fund):**
1. **CSRF bootstrapt sich ausschließlich über die `/ui/login`-POST-Antwort**, nicht über ein
   bloßes Neuladen von `/ui/` — dieselbe P5-H-Eigenheit, die schon für `testnutzer-p7` mehrfach
   dokumentiert wurde (`docs/INDEX.md`, P6.5-12-Fund). Direktes Navigieren zu `/ui/` nach einer
   Einladungs-/Enrollment-Sitzung lässt `sessionStorage['sfx:csrf']` leer — jeder erste
   Schreibversuch scheitert mit „CSRF-Token fehlt oder stimmt nicht", bis ein echter
   `/ui/login`-Roundtrip in DERSELBEN Tab durchlaufen wird.
2. **`get_page_text` kann eine Vor-Navigations-DOM liefern**, wenn es zu schnell nach einem
   Klick aufgerufen wird — dreimal fälschlich als „Login/Hinzufügen ist fehlgeschlagen"
   gelesen, obwohl der Server-Log denselben Request bereits mit `200` beantwortet hatte. Ein
   erneutes `get_page_text` (ggf. nach `wait`) zeigte danach den korrekten, bereits
   erfolgreichen Zustand. Für die zweite Wegwerf-Instanz (Kill-Switch-Probe,
   `space_admin_enabled=False`) führte dieselbe Klick-Unzuverlässigkeit dazu, dass der
   Login-POST dort nie beim Server ankam (kein einziges Mal in mehreren Versuchen) — die
   REST-Ebene wurde stattdessen per `curl` bestätigt (siehe P7-22-Zeile oben), der
   Menü-Ausblendung fehlt deshalb noch der Pixel-Beweis.

**Verifiziert:** +3 neue/geänderte Tests (`test_app_html_has_a_live_manage_spaces_entry` ersetzt
den Stub, `_JS_MODULES` um `"spaces"`, `test_ui_settings_space_admin_enabled_defaults_to_true`
in `test_api.py`). Volle Suite **903 → 904**, real gezählt. Tabu-Diff leer. `node --check` auf
`spaces.js`/`app.js` sauber (kein Ersatz für einen Test, nur eine Syntaxprobe — P5-T lässt JS
weiterhin unit-ungetestet).

**Abnahmestand:** P7-18 ✅ (Route + Knopf-fehlt, beide bestätigt). P7-22 ✅ (Route doppelt
bestätigt, Menü-Ausblendung jetzt pixel-verifiziert — siehe Nachtrag unten). Modul-Status-
Tabelle (Zeile 13) und Abnahmestand-Tabelle oben nachgezogen. `phase6_shares/CLAUDE.md`s
Zeile 16 (der ursprüngliche `space_admin_enabled`-Seam) bekam eine datierte Schließungsnotiz,
der Snapshot selbst bleibt unangetastet.

**Nächster Schritt, konkret:** Step C5 (Betrieb/Doku — `diagnose.sh` Prüfung 12 Textergänzung,
`docs/UPDATE_LOG.md`-Eintrag vor dem nächsten Deploy, P6-X-Gate beachten) und Block B
(Mehrfachauswahl, `phase6_shares/ITEM_MOVE_PLAN.md` §9). Vor dem nächsten Deploy zusätzlich:
`space_admin_enabled`s Default-Wechsel auf `True` bedeutet, dass Fabian den neuen Menüpunkt
ab dem nächsten Release sieht — im Update-Log-Eintrag erwähnen, nicht erst beim Deploy
entdecken lassen (Advisor-Hinweis).

**Nachtrag, 2026-08-25 — P7-22s Menü-Anteil geschlossen (Nikinger-Vorschlag „use my real
chrome browser"), root cause des Browser-Harness-Problems gefunden.**

**Root Cause, nicht nur Symptom:** das ursprüngliche Problem war nie „Login klappt in diesem
Browser nicht" — der allererste automatisierte Klick auf „Weiter" beim Einladungs-Formular
**gelang tatsächlich** (Server-Log: `POST /ui/invite/... 200 OK`). Ein `get_page_text`-Aufruf
direkt danach zeigte aber noch die alte, prä-Navigations-DOM (dieselbe Race-Bedingung, die
bereits im vorigen C3-Nachtrag notiert war) — das las ich fälschlich als Fehlschlag und klickte
ein zweites Mal. Der zweite Klick traf denselben, jetzt schon verbrauchten Einmal-Token
(`POST .../invite/... 404`) und riss die Enrollment mitten in der TOTP-Bestätigung ab, bevor
das Secret gesichert war — die Instanz landete in einem nicht mehr sauber fortsetzbaren
Zwischenzustand. **Kein Bug in `spaces.js`/`app.js`/der Login-Seite — ein Fehler in der
Auswertungsreihenfolge dieser Sitzung**, nicht im getesteten Code.

**Vorgehen mit dem Nikinger, dritte Wegwerf-Instanz (frisches `DATA_ROOT`, neuer
Einladungslink):** Claude Code füllte Formularfelder per Automation, der Nikinger klickte
selbst („Weiter", „Bestätigen", Login-Submit — dieselbe Arbeitsteilung wie bei
`testnutzer-p7`s Enrollment in P7 Step A7: TOTP-Sekret einmalig vom Nikinger vorgelesen, sofort
zur Code-Berechnung verwendet, nie in einer Datei oder einem Commit gelandet). **Danach lief
auch die automatisierte Login-Route** (`niklas`/Passwort/frischer TOTP-Code, Server-Log direkt
geprüft statt `get_page_text` zu vertrauen) — Login, Übersicht, `GET /api/v1/{me,meta,
overview,spaces,items}` alle `200`. Konto-Dialog geöffnet: zeigt ausschließlich „Update-Log
ansehen", **„Spaces verwalten" fehlt vollständig** — `meta.space_admin === false` blendet den
Menüpunkt tatsächlich aus, wie `app.js`s einzeilige Zuweisung es verspricht.

**Ergebnis: P7-22 ✅, beide Hälften.** Kein Code geändert (reine Verifikationssitzung),
Verifiziert-Absatz oben bleibt unverändert gültig (903/904-Zählung betrifft nur den C3-Commit,
nicht diesen Nachtrag). Tabu-Diff nicht relevant (keine Code-Änderung). Beide Wegwerf-Server
sauber beendet (`pkill`, Port frei bestätigt).

**Für die nächste Sitzung, falls dieselbe Klasse Fund nochmal auftritt:** nach einem Klick
IMMER zuerst den Server-Log (oder ein `wait` vor `get_page_text`) prüfen, bevor ein zweiter
Klick riskiert wird — ein zu früh gelesenes `get_page_text` ist nicht dasselbe wie ein
fehlgeschlagener Request.

**Nachtrag, 2026-08-26 — Step C5 (Betrieb/Doku) gebaut, Block C damit vollständig.**

Reiner Doku-/Skript-Text, kein Python-Verhalten geändert (Plan §C5 verlangt genau das: „ein
Satz im Prüfungstext, mehr nicht").

- `phase3_edge/scripts/diagnose.sh` Prüfung 12 (`spacectl.py check --json` gegen `.share.yml`-
  Referenzen): Kommentarblock um einen Satz ergänzt — dieselbe Prüfung deckt jetzt ausdrücklich
  auch die neue menschliche Space-Verwaltungsfläche (C2–C4) ab, ein per „Spaces verwalten"
  angelegter oder entfernter Space hinterlässt dieselben Spuren wie einer über `spacectl.py`.
  Die eigentliche Prüf-Logik/Ausgabetexte (Zeilen 226–244) bleiben unverändert — der Plan
  verlangt nur den einen erklärenden Satz, keine neue Fallunterscheidung.
- `docs/UPDATE_LOG.md`: neuer oberster Eintrag `## 2026-08-26`, zwei Zeilen (neuer Menüpunkt
  „Spaces verwalten"; Re-Auth-Hinweis bei Entfernen/größeren Mitgliederänderungen) — Format
  gegen den Datei-Kopf-Kommentar geprüft (kurze `- `-Zeilen, kein weiches Umbrechen). **Achtung
  für den tatsächlichen Deploy-Tag:** P6-X-Gate verlangt, dass der oberste Eintrag auf den
  Deploy-Tag datiert ist — falls `deploy.sh` nicht noch am 2026-08-26 läuft, muss das Datum
  vor dem Lauf auf den echten Tag nachgezogen werden, sonst bricht das Skript ab.
- Modul-Status-Tabelle (Zeile 14, neu) nachgezogen.

**Verifiziert:** `pytest -q` **904 → 904**, unverändert (keine neue Testdatei, keine geänderte
Assertion — Plan sieht für C5 keinen Test vor). Tabu-Diff leer (nur `diagnose.sh`-Kommentar +
`docs/UPDATE_LOG.md` + dieser Head berührt).

C5 trägt keine eigene Abnahmezeile (P7-1–P7-24 sind alle Zeilen 1–13 zugeordnet) — geprüft per
Grep, kein `P7-N`-Eintrag nennt `diagnose.sh`/`UPDATE_LOG`/„Betrieb". Kein offener Posten dieser
Art zurückgelassen.

**Damit ist Block C (C1–C5) vollständig.** Einzig verbleibender Scope-Punkt dieser Phase:
Block B (Mehrfachauswahl, `phase6_shares/ITEM_MOVE_PLAN.md` §9, Entscheidungen P6-AK–AN) —
kein neuer Endpunkt, kein neues MCP-Tool, Zweirunden-Re-Auth-Logik (P6-AM) wie im Plan-Auszug
oben. Danach Step Z (Abnahme/Deploy/Abschluss).

**Nächster Schritt, konkret:** Block B, `webui/static/js/state.js`/`list.js`/`tree.js`/
`dialogs.js`/`toasts.js`/`app.html` gemäß der Anker-Tabelle oben in `docs/concepts/
phase7_spaces_admin_plan.md` §"Block B".

**Nachtrag, 2026-08-26 — Block B gebaut (Mehrfachauswahl, §9), Phase-7-Scope damit vollständig
außer Step Z.**

**Umsetzung entlang der Plan-Anker (§9.3), sechs Dateien, reiner Frontend-Schnitt (P6-AL):**
`state.js` bekommt `selectedItemIds` (ein `Set`, geteilt wie der Rest von `state`). `list.js`:
`toggleSelected()`/`clearSelection()`/`renderSelectionToolbar()`, Strg+Klick UND Long-Press
(Pointer-Events, nur `pointerType !== "mouse"`, P5-W bleibt Desktop-first — kein eigener
Touch-Testlauf für diesen Zweig) auf jeder `movable`-Zeile, neue `moveSelectedItems(items,
target, credentials, onProgress)` als geteilte Zweirunden-Schleife. `tree.js`: `clearSelection()`
in `activateView()`/`navigateAll()` — dieselbe Exklusivitäts-Disziplin wie `folder`/`filter`
seit Step 7 Commit 1, zusätzlich beim Such-Debounce und beim Chip-„×“ in `list.js` (Suche zählt
laut §9.3 Punkt 1 ausdrücklich als Navigation). `dialogs.js`: `openMoveDialog(itemOrItems)`
normalisiert auf `moveTargetItems` (Array, IMMER — ein Einzel-Move wird zu `[item]`) — **derselbe
Dialog, keine zweite Definition** (P6-AK), Titel/Konsequenztext branchen auf `.length`.
`toasts.js`/`app.css`: `toast()` nimmt jetzt auch ein Array (mit `\n` verbunden), `.toast`
bekommt `white-space: pre-line` für die zweite Zeile der Sammelmeldung. `app.html`: neue
`#list-selection`-Werkzeugleiste unter `#list-chips`, `#move-dialog-title`/`#move-progress`.

**Zwei Advisor-Runden, insgesamt fünf Funde vor dem Commit behoben (keiner davon durch den
Browser-Lauf allein gefunden — beide Runden liefen VOR dem jeweils nächsten Schritt):**
1. **Batch-Ziel war nicht eingefroren** — `runBatchMove()` las `moveSpaceSelectEl.value`/
   `moveFolderSelectEl.value` bei JEDEM Klick neu, auch beim Re-Auth-Retry. Ein Dropdown-Wechsel
   zwischen Runde 1 und Runde 2 hätte die zurückgewiesenen Items an ein ANDERES Ziel geschickt
   als die bereits erfolgreichen — derselbe Fundtyp wie C3s `pendingMemberBody`. Behoben: neues
   `pendingBatchTarget`, eingefroren beim ersten Batch-Submit (dasselbe Muster wie
   `pendingMoveBody` beim Einzel-Move), PLUS `moveSpaceSelectEl.disabled`/`moveFolderSelectEl.
   disabled = true` für die Dauer eines laufenden Batches (zwei unabhängige Riegel für denselben
   Fund, nicht nur einer).
2. **Space-Wechsel-Handler räumte die Batch-Bilanz nicht auf** — nullte `moveBatchReauthItems`,
   ließ `moveBatchSucceeded`/`moveBatchFailed`/`pendingBatchTarget` stehen. In der Praxis durch
   Fix 1 unerreichbar (die Auswahlfelder sind währenddessen gesperrt), trotzdem als
   Defense-in-Depth nachgezogen — kein Verlass allein auf einen HTML-`disabled`, den die
   Accessibility-Probe dieser Sitzung nicht zweifelsfrei bestätigen konnte.
3. **Fehlender `.catch()`** auf der Erfolgs-Kette nach einem Batch (`loadItems().then(loadOverview)
   .then(...)`) — ein `401` mitten im Batch hätte eine unbehandelte Promise-Ablehnung hinterlassen
   (dieselbe Fundklasse wie P5 Step 10, `reportUnexpectedError()`). Behoben, `reportUnexpectedError`
   neu aus `api.js` importiert.
4. **Abgelaufene Sitzung mitten im Batch wäre als benannter Fehlschlag pro Item erschienen** —
   `api.js`s 401-Zweig zeigt die "Sitzung abgelaufen"-Karte bereits synchron; ohne Sonderfall
   hätte `moveSelectedItems()` trotzdem jedes verbleibende Item als `[unauthenticated]`
   gemeldet UND weiter erfolglose Requests abgeschickt. Behoben: `err.message ===
   "unauthenticated"` bricht die Schleife sofort ab, dieselbe Unterdrückung wie im Einzel-Move.
5. *(Kein Fund, gegengeprüft:)* die Konflikt-Fehlermeldung (`api.py :: _map_store_error()` —
   „Konflikt bei {id}: erwartete Version X, aktuell Y.“) liest sich sinnvoll eingebettet in der
   Batch-Sammelmeldung (`„Titel“ [Konflikt bei …]`) — keine Änderung nötig.

**Echter Browser-Lauf, Ende-zu-Ende, gegen eine Wegwerf-Instanz** (eigener Uvicorn-Prozess,
temporäres `DATA_ROOT`+`AuthStore`, `git=False`, Skript im Scratchpad, kein Repo-Teil — Nutzer
per `store.upsert_user()`+`confirm_totp()` direkt bestätigt angelegt, kein Einladungsumweg
nötig, Login selbst lief normal über die UI mit Passwort+echtem TOTP-Code):
- **Zeile 31** (N Items auf einmal): drei Notizen per Strg+Klick ausgewählt (Toolbar zeigte
  korrekt „3 ausgewählt“), Dialogtitel „3 Items verschieben“, Konsequenztext „Verschiebt 3 Items
  nach beta. …“ — alle drei korrekt gerendert.
- **Zeile 33** (ein fehlgeschlagenes Item blockiert die anderen nicht): eines der drei Items
  wurde VOR dem Klick über einen zweiten `Store`-Handle auf eine neue Version gebracht (echter
  Konflikt, nicht simuliert). Ergebnis: die anderen zwei landeten korrekt im Zielspace (Space-
  Zähler beta 1→3), das Konfliktitem blieb unverändert in alpha. **Die tatsächliche
  Sammelmeldung mit dem benannten Fehler wurde dabei NICHT gesehen** — der Dialog schloss sich
  vor dem Screenshot, der Toast war bereits abgelaufen. Nur die Nichtbewegung des Konfliktitems
  ist damit live bewiesen, nicht der Text der zweiten Toast-Zeile selbst.
- **Zeile 32** (ein gemeinsames Re-Auth-Formular für die ganze Auswahl): mit einer frischen
  `.share.yml`-Konstellation (alpha teilt NICHTS mit beta, beta teilt `write` mit alpha — echtes
  Widen, kein durch beidseitige Shares verdecktes No-Op, wie es der erste Durchlauf zeigte) zwei
  Items batch-verschoben: Runde 1 → „2 von 2 benötigen Passwort und Code“, EIN Formular. Ein
  wiederverwendeter TOTP-Code wurde vom Server korrekt als Replay abgelehnt (echtes
  Anti-Replay-Verhalten, kein Fund) — nach einem frischen Code liefen beide Items durch, Toast
  bestätigte, Dialog schloss, beta-Zähler stieg auf 5.
- **Zeile 34** (In-Space-Batch löst nie Re-Auth aus): zwei Items innerhalb von alpha in einen
  neuen Ordner verschoben — Dialog schloss sofort ohne jedes Re-Auth-Formular, beide Items auf
  v2, Ordner im Baum korrekt.
- **Konsole** ohne Fehler während des gesamten Laufs (Muster `error|Error|Uncaught|Unhandled`).

**Ehrlich benannt, nicht verschwiegen:** die zweizeilige Sammelmeldung mit namentlich genannten
Fehlern (§9.3 Punkt 4, Zeile 33s zweite Hälfte) ist NICHT im Browser gesehen — nur ihre
Voraussetzung (das Konfliktitem bleibt unbewegt, taucht nicht fälschlich als erfolgreich auf).
Der fünfte Advisor-Fund oben (Konflikt-Meldungstext) ist eine Code-Prüfung, kein Sichtbeweis.
Der von der Beraterin vorgeschlagene fünfte E2E-Fall (Dropdown-Wechsel zwischen Runde 1 und 2)
wurde NICHT nachgestellt — durch Fund 1 oben ist er strukturell unerreichbar geworden (die
Auswahlfelder sind während eines laufenden Batches gesperrt), nicht übersprungen.

**Abnahmezeilen 31–34 (`ITEM_MOVE_PLAN.md` §9.5, „Wer: Niklas“) bleiben formal offen** —
derselbe Umgang wie P6.5-12 vor dem echten Klick: ein Claude-Code-Browserlauf ist ein
Kandidatenbeleg, keine Abnahme durch den Nikinger selbst. **Gebaut, Claude-Code-Browserlauf
bestanden, Nikinger-Bestätigung steht aus.**

**Verifiziert:** `pytest -q` **904 → 904**, unverändert (P6-AL: reiner Frontend-Schnitt, keine
neue Backend-Testdatei laut Plan §9.4). `node --check` auf `list.js`/`dialogs.js` sauber. Tabu-
Diff: ausschließlich `phase5_ui/webui/static/{app.css,app.html,js/{state,list,dialogs,tree,
toasts}.js}` — `webui/api.py` bewusst NICHT angefasst (P6-AL, kein neuer Endpunkt), stärker als
§9 verlangt. Wegwerf-Server sauber beendet (`pkill`, `DATA_ROOT` gelöscht, Port frei bestätigt).

**Damit ist Block B fertig — Phase 7 ist inhaltlich vollständig (Block A, Gate, Block C, Block
B).** Einzig verbleibend: **Step Z** (Abnahme/Deploy/Abschluss, siehe Plan-Auszug oben) — frischer
`diagnose.sh`-Lauf, `docs/UPDATE_LOG.md`-Datum auf den echten Deploy-Tag geprüft, `pytest -q`/
`mcp_smoke.py`/`ui_smoke.py`/`ui_budget.py --json`, Tabu-Diff, dann `deploy.sh` durch den
Nikinger (braucht Sudo). Danach die Abnahmematrix real durchgehen (inkl. der jetzt offenen
Zeilen 31–34) und die Phase-7-Closeout-Dokumente schreiben.

**Nächster Schritt, konkret:** Step Z — mit dem Nikinger abstimmen, wann `deploy.sh` läuft und
ob das UPDATE_LOG-Datum vom 2026-08-26 noch zum tatsächlichen Deploy-Tag passt.

**Nachtrag, 2026-08-27 — Nikinger-Entscheidung: Deploy auf 2026-08-28.**

`docs/UPDATE_LOG.md`s oberster Block auf `## 2026-08-28` nachgezogen (P6-X-Gate: der Eintrag
muss den tatsächlichen Deploy-Tag tragen, sonst bricht `deploy.sh` ab). Dabei eine dritte Zeile
ergänzt, die bislang fehlte: Block B (Mehrfachauswahl) ist selbst eine sichtbare, menschen-
relevante Änderung (Strg+Klick/Long-Press-Auswahl + Sammel-Verschieben) und gehört damit in
denselben Deploy-Eintrag wie die Space-Verwaltung — beide Features landen im selben Release.
Parser-Probe (`parse_update_log()`) bestätigt alle drei Zeilen unverändert intakt unter
`entries[0]`. Kein Code-Diff sonst, reine Terminplanungs-Reaktion — `pytest`/Tabu-Diff nicht neu
gelaufen (nichts Python-Seitiges berührt).

**Weiterhin offen für den 2026-08-28-Lauf:** frischer `diagnose.sh`, `pytest -q`/`mcp_smoke.py`/
`ui_smoke.py`/`ui_budget.py --json`, Tabu-Diff, dann `deploy.sh` durch den Nikinger.

**Nachtrag, 2026-08-27 — Pre-Deploy-Checks gelaufen** (`pytest -q` 904/904, `mcp_smoke.py`
16/16, `ui_smoke.py` 12/12, `ui_budget.py --json` `all_within_budget: true`, Tabu-Diff über die
letzten 40 Commits leer — alle vier Skripte bauen ihre eigene temporäre Instanz, nie den echten
`DATA_ROOT`, deshalb von Claude Code selbst gefahren; `diagnose.sh` bewusst nicht — liest den
echten `DATA_ROOT`, bleibt Nikinger-Sache).

**Nachtrag, 2026-08-27 — Korrektur des Datumsplans, echter `deploy.sh`-Lauf gescheitert am
falschen Datum, sauber selbst aufgeräumt.** Der Nikinger fuhr `deploy.sh main` noch am selben
Tag (nicht am 28., wie oben angenommen — die „morgen"-Ankündigung eine Nachricht zuvor deckte
sich nicht mit dem tatsächlichen Zeitpunkt des Laufs). `deploy.sh`s eigenes Gate (P6-X) brach
korrekt ab: `docs/UPDATE_LOG.md` trug `## 2026-08-28`, das System-Datum (`date -u`/`date`, beide
gegengeprüft: 2026-08-27 UTC und CEST) erwartete `2026-08-27`. **Kein Fehlverhalten des Skripts
— das Gate hat exakt das getan, wofür es gebaut wurde.** Das unvollständige Release-Verzeichnis
(`/opt/sharefyx/releases/20260827T165500.903807Z`) hat `deploy.sh` bereits selbst entfernt (im
eigenen Log: „entferne unvollständiges Release"), `current` zeigte danach unverändert auf die
letzte gute Release (`20260825T110849.160586Z`) — read-only per `ls`/`readlink` bestätigt, keine
Leiche zurückgeblieben, kein Handgriff nötig. `docs/UPDATE_LOG.md`s oberster Block auf
`## 2026-08-27` korrigiert (Zeileninhalt unverändert, nur das Datum), Parser-Probe erneut grün.

**Nächster Schritt, konkret:** `deploy.sh main` erneut versuchen, mit demselben Env-Var-Satz wie
zuvor — das UPDATE_LOG-Gate sollte jetzt durchlaufen.

**Nachtrag, 2026-08-27 — echter `deploy.sh main`-Lauf durch den Nikinger, erfolgreich.**
**Live-Ergebnis:** `{"action":"deploy","result":"ok","release":"/opt/sharefyx/releases/
20260827T165737.663410Z","sha":"e88a6244d8eebb5d08d1d93c4a2725f84a2f5971","ref":"main",
"previous":"/opt/sharefyx/releases/20260825T110849.160586Z"}`. `pytest -q` im Release **904/904**
(zweiter, unabhängiger Lauf — im gebauten Release-Verzeichnis, nicht nur im Arbeitsbaum),
`/opt/sharefyx/current` zeigt jetzt auf `e88a624`, `sharefyx-mcp` neu gestartet, Health-Gate 3/3
grün (`/ui/login`→200, `/api/v1/me`→401, `/mcp/`→401 — alle drei die per `deploy.sh`-Kommentar
erwarteten Antworten: Stack vollständig gemountet UND Auth-Gate scharf, kein Fehlschlag),
Retention griff (`KEEP=5`, ältestes Release `20260813T115528` entfernt).

**Damit ist Phase 7 live deployt.** Block A/Gate/C/B stehen jetzt real auf der Maschine, nicht
nur im Repo. **Weiterhin offen, unverändert:** A6 (Purge-Gate, frühestens 2026-08-28) und die
volle Abnahmematrix real mit dem Nikinger durchgehen — insbesondere die neuen Zeilen 31–34
(bislang nur Claude-Code-Browserlauf gegen eine Wegwerf-Instanz, keine Nikinger-Abnahme auf der
echten Instanz) und alle Zeilen, die noch Fabians eigenen Login brauchen. **Root-`CLAUDE.md`,
`ROADMAP.md`, `docs/INDEX.md`** im selben Commit nachgezogen (Phase 7 jetzt „inhaltlich
vollständig, live deployt, Step Z läuft" statt „Block A weit fortgeschritten").

**Nächster Schritt, konkret:** mit dem Nikinger die volle Abnahmematrix (Plan §6/§9.5) real
durchgehen, danach `PHASE7_CLOSEOUT_HANDOVER.md` + Übersichtsgrafik + Rotationsprüfung.

**Nachtrag, 2026-08-27 — Abnahmematrix-Walkthrough gegen die echte Live-Instanz
(`e88a624`), Browser-Tool-Modus (Claude Code steuert, Nikinger klickt/tippt Zugangsdaten):**

Sieben Zeilen live geschlossen: **P7-14, P7-15 (beide Hälften), P7-16, P7-17, P7-19, P7-23 ✅.**
Eine neu gefunden, **P7-24 ❌** (echter Mechanismus-Fehler, kein reiner UI-Fund) — siehe
Abnahmestand-Tabelle oben für den vollen Befund und die Fix-Optionen, hier nur der Kern:
`list.js :: moveSelectedItems()` reicht dasselbe `credentials`-Objekt (ein TOTP-Code) an jedes
sequenzielle PATCH im Batch durch; der Server lehnt den wiederverwendeten Code korrekt als
Replay ab, wodurch ein re-auth-pflichtiger Batch mit N>1 Items strukturell mehr als zwei Runden
braucht statt der von P7-24 verlangten „ein Formular, nicht N". Bleibt offen bis der Nikinger
entscheidet, wie behoben wird. **P7-9 weiterhin blockiert** — `token_families`-Purge-Fenster
öffnet erst 2026-08-28, Systemdatum heute ist 2026-08-27, keine Umgehung versucht.

**Zwei operative Pannen dieser Sitzung, für zukünftige Läufe festgehalten:**
1. **Cookie-Kollision zwischen Tabs derselben Session.** `testnutzer-p7`s Login in einem zweiten
   Tab überschrieb das Session-Cookie für den ERSTEN Tab (gleicher Browser-Origin, gemeinsamer
   Cookie-Jar) — `niklas`s Tab zeigte danach `testnutzer-p7` als Home-Space, obwohl die
   rechte Seite noch die alte `niklas`-Übersicht cachte. Merke: ein zweiter Login in einem
   zweiten Tab **derselben** `claude-in-chrome`-Session ist kein isolierter Kontext, er
   invalidiert die erste Sitzung. Für zwei gleichzeitige Logins bräuchte es zwei getrennte
   Chrome-Profile/Inkognito-Fenster, nicht zwei Tabs — hier stattdessen sequenziell gearbeitet
   (Tab 2 nach Gebrauch geschlossen, Tab 1 neu eingeloggt).
2. **Koordinaten-Klicks nach einer Layout-Änderung sind unzuverlässig.** Mehrere `computer
   left_click`-Aufrufe auf feste Pixel-Koordinaten trafen nach einem Viewport-Wechsel
   (1214×545 → 1517×681 zwischen Screenshots) das falsche Feld — Text landete wiederholt im
   Passwortfeld statt im Space-Feld. Behoben durch Umstieg auf `find`+`form_input`/`ref`-Klicks
   (element-basiert statt pixel-basiert) für sicherheitsrelevante Formulare. Für künftige
   Läufe: bei jedem Login-/Formular-Schritt `find` statt gecachter Koordinaten verwenden,
   besonders nach einem Screenshot mit anderer Auflösung als der vorherige.

**Verifiziert:** keine Code-Änderung in diesem Nachtrag (reine Live-Abnahme + Doku). Kein
`pytest`-Lauf nötig. Abnahmestand-Tabelle und dieser Block sind der einzige Diff.

**Nachtrag, 2026-08-27 — P7-12 durchgeführt, `testnutzer-p7` vollständig zurückgebaut.** Exakt
nach dem Plan-Rezept (`docs/concepts/phase7_spaces_admin_plan.md:544-552`): `testcred.py purge`
(Claude Code, reiner Keyring-Vorgang, kein `DATA_ROOT`-Zugriff) zuerst, danach die drei
`DATA_ROOT`/Auth-DB-Schreibvorgänge durch den Nikinger selbst (`spacectl.py remove-space
testnutzer-p7 --force`, `authctl.py disable-user`/`revoke-sessions --space testnutzer-p7`) —
bewusst nicht von Claude Code ausgeführt, dieselbe Kategorie destruktiver Direktzugriff ohne
interaktives Re-Auth-Gate wie `deploy.sh`. `SPACE_AUTH_DB` war die nächste bekannte Lücke aus
A7 (systemd setzt `STATE_DIRECTORY`, eine interaktive Shell nicht) — diesmal mit dem echten
Pfad (`/var/lib/sharefyx/auth.sqlite3`, per `ls`-Zeitstempel als aktiv bestätigt) sofort gelöst,
keine neue Verzögerung. `spacectl.py check --json` bestätigt `orphan_count:0`/`broken_count:0` —
keine verwaisten `.share.yml`-Referenzen zurückgeblieben. Damit ist der dritte Test-Principal
dieser Phase vollständig entsorgt; jede künftige Phase, die einen dritten Nutzer braucht, legt
sich einen neuen an (Nikinger-Entscheidung dieser Sitzung, kein Wiederverwenden von
`testnutzer-p7`).

**Ehrliche Antwort auf die Nikinger-Frage „sind alle Tests fertig, ist Phase 7 damit vorbei?":
Nein, noch nicht — aber nur noch zwei Punkte, nicht drei (Korrektur unten).**
1. **P7-24 ❌** — der TOTP-Batch-Mechanismus-Fund oben. **Nikinger-Entscheidung, 2026-08-27:
   wird als echter Defekt anerkannt, Fix erst in der nächsten Phase.** Bleibt ❌ in der
   Abnahmestand-Tabelle stehen (kein stilles Weglassen, kein Umdeuten in ein akzeptiertes
   Restrisiko) — nur der Zeitpunkt der Behebung ist geklärt, nicht der Befund selbst.
2. **P7-9 ⬜** — `token_families`-Purge-Fenster öffnet erst 2026-08-28 (morgen), `clients` erst
   2026-10-27. **Nikinger-Entscheidung: bis morgen warten**, kein Umgehungsversuch.

**Korrektur, noch in dieser Sitzung: P6-Zeilen 36/37 fälschlich als offen geführt.** Der
Nikinger fragte direkt nach, ob `testnutzer-p7`s Test gleichwertig zu einem Fabian-Test ist —
Antwort: **mehr als gleichwertig, es ist der einzig mögliche Weg.** Der Plan selbst
(`docs/concepts/phase7_spaces_admin_plan.md:540`) begründet genau das: mit Fabian ist der Fall
„nur item-level Share, kein Space-Grant" **strukturell unerreichbar** — `niklas` steht bereits
in `fabian/.share.yml` unter `read:`, Fabian sieht als Empfänger also ohnehin alles über den
Space-Grant, ein item-level-only-Szenario lässt sich mit ihm gar nicht bauen. `testnutzer-p7`
hat **keinen** space-level Grant — deshalb wurde er für genau diesen Fall angelegt (P7-J). Die
Zeile P7-11 in der Abnahmestand-Tabelle oben (bereits ✅, Web-UI **und** MCP) trägt das als
Beleg schon direkt in ihrem eigenen Text: „Web-UI (**P6-Zeilen 36/37**, echter Login)". **P6-36/37
sind damit bereits geschlossen, nicht offen** — mein eigener Nachtrag oben (Punkt 3, „brauchen
Fabians eigenen Login") war falsch, hier korrigiert. `phase6_shares/CLAUDE.md` trägt an dieser
Stelle noch den alten Stand („36/37 brauchen Fabian") — das ist der zugehörige Doku-Fund für die
nächste Sitzung, nicht mehr Teil des Abnahme-Fortschritts dieser hier.

Alles andere in der Abnahmestand-Tabelle steht jetzt ✅. **Phase 7 ist damit sehr nah, aber
nicht formal abschließbar** — der Root-`CLAUDE.md`/`ROADMAP.md`/`docs/INDEX.md`-Sprung auf
„Phase 7 ✅" und `PHASE7_CLOSEOUT_HANDOVER.md`/Übersichtsgrafik/Rotationsprüfung bleiben
bewusst der nächsten Sitzung, sobald P7-9 (frühestens morgen) geprüft ist. P7-24 bleibt als
bekannter, akzeptierter Defekt in der nächsten Phase offen — das blockiert den Phase-7-Abschluss
selbst nicht mehr, muss aber im Closeout-Handover als offene Entscheidung an die nächste Phase
weitergereicht werden, nicht stillschweigend verschwinden.

**Nächster Schritt, konkret:** neue Sitzung ab 2026-08-28 — zuerst P7-9 (`clients`/
`token_families`-Rückgang nachprüfen), P7-24-Entscheidung einholen, dann erst der formale
Phase-7-Abschluss samt Closeout-Dokumenten.

**Nachtrag, 2026-08-27 (spät) — Live-Incident: `GET /api/v1/overview` → 500 auf jedem Gerät,
Ursache und Sofort-Fix.** Nikinger meldete den Fehler von einem neuen Gerät aus (DevTools-
Screenshot, `500` auf `/api/v1/overview`). `journalctl -u sharefyx-mcp` zeigte den echten
Traceback: `FileNotFoundError` in `storage/store.py :: _row_to_item()` für
`/home/savefyx/savefyx-data/testnutzer-p7/_archive/itm_26f8d0b7__p6-5-12-retest-2026-08-25.md`.

**Root Cause, kein Geräte-/Browser-Problem:** `spacectl.py :: _cmd_remove_space()`
(`phase6_shares/scripts/spacectl.py:170-195`) löscht mit `acl.remove_space_dir()` nur das
Verzeichnis auf der Platte — der SQLite-Index wird dabei **nie** angefasst. Der frühere P7-12-
Lauf dieser Sitzung (`spacectl.py remove-space testnutzer-p7 --force`, vom Nikinger ausgeführt)
hat damit einen index-only-Karteileichen-Zustand hinterlassen: Zeilen für `testnutzer-p7`s
Items standen weiter in der SQLite-Datenbank, obwohl die Dateien weg waren. Jede Anfrage, die
diese Zeilen berührt (`/api/v1/overview` iteriert `store.search()` über alle Buckets), krachte
mit dem `FileNotFoundError` — reproduzierbar für **jeden** eingeloggten Nutzer, nicht
gerätespezifisch (Screenshot zeigte Firefox/Windows, ein bislang ungenutztes Gerät — reiner
Zufall, dass es dort zuerst auffiel).

**Sofort-Fix, noch in dieser Sitzung, durch Hard Rule 2 vorab autorisiert** („SQLite darf
jederzeit gelöscht und aus den `.md`-Dateien vollständig rekonstruiert werden"): `space_cli.py
--data-root /home/savefyx/savefyx-data reindex --json` → `{"items_indexed": 78,
"duration_seconds": 0.044}`. `Store.rebuild_index()` nimmt denselben `.write.lock`-Flock wie der
laufende Dienst (P7-M) — sicher gegen die Live-Instanz gefahren, kein Neustart nötig. Danach
`journalctl --since "2 minutes ago"` grep nach `error|traceback` → leer, `curl .../api/v1/me` →
weiterhin `401` (Dienst gesund). **Vom Nikinger noch nicht gegengeprüft** (kein erneuter
Login-Versuch im selben Gespräch) — bitte auf dem betroffenen Gerät erneut `/ui/` laden und
bestätigen.

**Echter Fund, nicht nur ein einmaliger Vorfall — `spacectl.py remove-space` braucht einen
Nachlauf-Reindex oder zumindest einen Warnhinweis.** Jeder künftige `remove-space --force`-Lauf
reproduziert dieselbe Karteileiche für die entfernten Items, bis jemand von Hand reindiziert.
**Nikinger-Entscheidung noch offen:** `_cmd_remove_space()` um einen automatischen
`store.rebuild_index()`-Aufruf erweitern (ein Zweizeiler, gleiche Datei) oder nur die
Warnmeldung ergänzen („führe danach `reindex` aus")? Bleibt für die nächste Sitzung — nicht
mehr Teil des heutigen P7-12-Laufs, aber eine direkte Konsequenz davon, hier festgehalten statt
verloren zu gehen.

**Verifiziert:** keine Testsuite gelaufen (reine Betriebs-Wiederherstellung, kein Code-Diff in
diesem Nachtrag — der `spacectl.py`-Fix selbst ist noch nicht gebaut). Tabu-Diff nicht relevant.

**Nächster Schritt, konkret, VOR allem anderen in der nächsten Sitzung:** Nikinger bestätigt,
dass `/ui/` wieder lädt. Danach `spacectl.py remove-space`s fehlenden Reindex beheben (kleiner,
in-scope Fix, keine neue Planungsrunde nötig) — erst danach weiter mit P7-9/P7-24/Closeout.

**Nachtrag, 2026-08-28 — Abnahmezeilen 31–34 (`ITEM_MOVE_PLAN.md` §9.5) vom Nikinger selbst live
gegen die echte Instanz bestätigt.** Damit ist die in Zeile 874 oben und im Session-Block vom
2026-08-25 genannte Lücke „Gebaut, Claude-Code-Browserlauf bestanden, Nikinger-Bestätigung steht
aus" geschlossen — dies ist die Nikinger-Abnahme selbst, kein weiterer Kandidatenbeleg. Ergebnis,
Zeile für Zeile:

- **Zeile 31** (N Items in einem Vorgang, ein `move`-Commit je Item) — ✅ **mit demselben bereits
  bekannten Vorbehalt wie P7-24**: die Items landeten korrekt im Ziel, aber die Auswahl enthielt
  rechteerweiternde Items, und der Nikinger musste dafür N verschiedene TOTP-Codes eintippen
  statt einem. **Kein neuer Fund** — deckungsgleich mit dem bereits im Abnahmestand oben
  protokollierten P7-24-Mechanismus-Fehler (`list.js :: moveSelectedItems()` reicht denselben
  TOTP-Code an jedes sequenzielle PATCH durch, Server lehnt den Replay korrekt ab). Bereits als
  echter, in die nächste Phase verschobener Defekt anerkannt (Nikinger-Entscheidung 2026-08-27,
  siehe oben) — diese Probe bestätigt nur, dass Zeile 31 denselben Mechanismus trifft, öffnet
  keine neue Entscheidung.
- **Zeile 32** (genau ein rechteerweiterndes Item → ein Formular) — ✅ live bestanden.
- **Zeile 33** (ein fehlgeschlagenes Item blockiert die anderen nicht) — ✅ live bestanden.
- **Zeile 34** (reine In-Space-Auswahl löst nie Re-Auth aus) — ✅ live bestanden.

**Damit ist die Nikinger-Abnahme für Block B (Mehrfachauswahl) vollständig**, mit demselben
einen offenen Punkt, der bereits vor dieser Probe bekannt und entschieden war (P7-24, Fix in der
nächsten Phase). Kein neuer Code-Diff, keine neue Testsuite nötig — reine Abnahme-Dokumentation.
`docs/INDEX.md`, `ROADMAP.md`, Root-`CLAUDE.md` im selben Commit nachgezogen.

**Verbleibend für Step Z / Phase-7-Abschluss:** A6 (Purge-Gate, ab heute 2026-08-28 kalendarisch
möglich, `token_families`), danach `PHASE7_CLOSEOUT_HANDOVER.md` + Übersichtsgrafik +
Rotationsprüfung.

**Nachtrag, 2026-08-28 — A6 gefahren, P7-9 geschlossen.** Baseline (read-only, `sqlite3` gegen
`/var/lib/sharefyx/auth.sqlite3`): `clients: 54`, `token_families: 35`, unverändert seit
2026-08-24. Oldest-`token_families`-Zeile `2026-07-29T15:02:27Z` — 30-Tage-Fenster lief um
17:02 CEST heute ab. Nikinger fuhr `sudo systemctl start sharefyx-purge.service` selbst (Live-
Dienst-Restart bleibt Nikinger-Sache, keine passwortlose `sudo` für Claude Code bestätigt).
`journalctl -u sharefyx-purge.service`: `{'access_tokens': 7, 'token_families': 4, 'clients': 0,
...}` — read-only Gegenprobe bestätigt `token_families` 35→31, `clients` unverändert 54 (90-Tage-
Fenster öffnet erst 2026-10-27, kein Fund, erwartetes Verhalten). **A6/P7-9 damit erfüllt.**

**Damit ist Phase 7 vollständig abgenommen — kein offener Test, kein offenes Gate mehr.** Einzig
verbleibend: **Step Z Rest** — `PHASE7_CLOSEOUT_HANDOVER.md`, Übersichtsgrafik, Rotationsprüfung,
danach Root-`CLAUDE.md`/`ROADMAP.md`/`docs/INDEX.md` auf Phase 7 ✅ heben. **Nikinger-Entscheidung:
das ist die nächste Sitzung.**

## Session stopped — 2026-08-23 (Step 0 gestartet: Verifikationsdurchlauf + Doku-Audit)

**Auftrag:** Erste Claude-Code-Sitzung von Phase 7. Einstieg ist Step 0, erster Handgriff das
Doku-Audit aus Handover §4.1 (Plan §4 Step 0.2).

**0.1 — `pytest`-Ausgangsstand:** `828 passed`, deckungsgleich mit der Erwartung aus dem P6.5-
Handover-Nachtrag. **V71 geschlossen.**

**0.2 — Doku-Audit, mit SHA-Beweis je Zeile.** `LIVE = f96125e` (`/opt/sharefyx/current`).
Geprüft per `git merge-base --is-ancestor <sha> $LIVE` gegen die Commits, die den jeweiligen
Modul-Status-Zeilen 8–16 in `phase6_shares/CLAUDE.md` entsprechen:

| Zeile | Modul | Commit(s) | Ergebnis |
|---|---|---|---|
| 8 | Step 7a Textfarben + Wortmarke-Nachtrag | `562d279`, `15cf054` | IST live |
| 9 | Step 7 Commit 0 (app.js-Split) | `1959de8` | IST live |
| 10 | Step 7 Commit 1 (echter Ordnerbaum) | `fbcdb9f` | IST live |
| 11 | Step 7 Commit 2 (Sichtbarkeits-Chip) | `e48c039` | IST live |
| 12 | Step 7 Commit 3 (Ordner anlegen+Verschieben, K4) | `5db817e` | IST live |
| 13 | Step 7 Commit 4 (Drag & Drop) | `0c504a4` | IST live |
| 14 | Step 7 Commit 5a (Re-Auth-Gate Backend) | `928908c` | IST live |
| 15 | Step 7 Commit 5b (Freigabe-Dialog+Re-Auth-Formular) | `cd94061` | IST live |
| 16 | Step 7 Commit 6 (`space_admin_enabled`-Stub) | `0378c41` | IST live |

Zusätzlich geprüft, weil dieselbe Fehlbehauptung an zwei weiteren Stellen stand: **Vormerkungen
Punkt 2** (Space-zu-Space-Verschieben, Step 7b, drei Commits `9274346`/`3f476c7`/`abeaba6`) — alle
drei ebenfalls Vorfahren von `f96125e`.

**Befund: die Doku war stale, nicht der Code.** Alle neun geprüften Zeilen (8–16) trugen „gebaut,
noch nicht deployt" bzw. „Deploy beim Nikinger" — tatsächlich sind sie seit dem Phase-6.5-Deploy
(`f96125e`, 2026-08-21) live. **Wichtig, per Advisor-Hinweis eingehalten: „deployt" ≠
„abgenommen".** Diese Korrektur ändert ausschließlich den Deploy-Status der Zeilen, **nicht**
ihren Abnahmestatus — Zeile 8 z. B. bleibt ohne eigenen Abnahmematrix-Punkt, die Space-Move-
Zeilen 25–30 bleiben „offen", nur das „noch nicht deployt" darin ist jetzt falsch und wurde
entfernt. Korrigiert in `phase6_shares/CLAUDE.md` (Zeilen 8–16 + Vormerkungspunkt 2), in
Root-`CLAUDE.md`s Current-State-Absatz (trug denselben veralteten Satz zu `d348e2e`, obwohl
`phase6_shares/CLAUDE.md` die Korrektur vom 2026-08-23 schon hatte — Root hatte sie nie
bekommen) und in `docs/INDEX.md`s `phase6_shares/CLAUDE.md`-Zeile (trug „Step 7b vollständig
gebaut … noch nicht deployt").

**0.3 — Link-Auflösung.** Ein echter Fund: `docs/PROMPTS.md`s `up: CLAUDE.md` löste relativ zu
`docs/` auf `docs/CLAUDE.md` auf (existiert nicht) statt `../CLAUDE.md`. Behoben. Sonst leer.

**0.4 — Indexzeile je `.md`.** Leer, nach Ausschluss von `.pytest_cache/` (generiert, wie in
0.5s Find-Kommando bereits vorgesehen, hier nur im Plan-Kommando vergessen) und `docs/INDEX.md`
selbst (Selbstverweis erwartungsgemäß nicht vorhanden).

**0.5 — Softcap.** 12 Treffer (Plan-Erwartung aus der Planungssession: 11 — Delta ist
`phase7_spaces_admin_plan.md` selbst, nach der Zählung angelegt). Alle 12 sind 📕/📦-konform.
`phase6_shares/CLAUDE.md` (39.080 B) und `ITEM_MOVE_PLAN.md` (40.261 B) bleiben grenzwertig unter
dem Cap (40.960 B) — die Zeilen-8–16-Korrektur oben blieb bewusst minimal (Zellen-Edits + eine
datierte Korrekturzeile, keine neue Erzählung), um den Cap nicht zu reißen. Größe nach der
Korrektur nicht erneut über 40 KB.

**0.6 — Skelett angelegt.** `phase7_spaces_admin/CLAUDE.md` (diese Datei), `SESSIONS_ARCHIVE.md`
(leer), `tests/conftest.py` (leer). `ROADMAP.md`: fehlende P6.5-Tabellenzeile ergänzt (echte
Vorphasen-Lücke, beim Bearbeiten derselben Tabelle mitgefunden, datiert korrigiert) + neue
P7-Zeile + eigener Abschnitt. `docs/INDEX.md`: „Active phase" auf Phase 7 umgestellt, neue Zeilen
für Plan/Head/Archiv.

**0.7 — Sechste Contract-Öffnung angekündigt.** `phase1_storage/CLAUDE.md`, datierter Absatz mit
der Funktionsliste aus Plan §4 C1.

**DoD Step 0:** alle sechs Punkte gefahren, Ergebnis protokolliert (0.1/0.3/0.4 „nichts zu tun"
außer dem PROMPTS.md-Link-Fund; 0.2/0.5/0.6/0.7 mit Ergebnis); Audit-Tabelle mit SHA je Zeile
oben; Skelett steht; `pytest` unverändert bei 828.

**Nächster Schritt:** Block A (Fixes + Phase-6.5-Abschluss) — beginnt mit einem live
`migrate_visibility.py --apply` gegen den echten `DATA_ROOT` und dem Anlegen von
`testnutzer-p7`. Beides ist Nikinger-Sache zu autorisieren, nicht Claude Codes eigene
Entscheidung — Session hier bewusst gestoppt, um das einzuholen.

**Nachtrag, selber Tag — Nikinger-Freigabe „per Plan, mit Step A" erhalten, A1+A2 gebaut.**

**V73/V74 vorab geklärt, wie vom Advisor verlangt:**
- **V73 (A3-Vorbereitung):** `markdown.js` löst `asset:<id>` unabhängig davon auf, ob die
  Asset-Datei noch existiert — die Regex prüft nur die URL-**Form**, nicht die Existenz. Ein
  entferntes (nach `_trash/` verschobenes) Bild rendert deshalb heute ein **kaputtes `<img>`**,
  keinen Alt-Text. A3 braucht also tatsächlich den geplanten dritten Kontextschlüssel
  `assetIds` — noch nicht gebaut, folgt mit A3 selbst.
- **V74 (A4-Vorbereitung):** `grep 'method: "PATCH"' -B15` über `editor.js`/`list.js`/
  `dialogs.js` enumeriert. **Der Plan-Entwurf für `_PATCH_FIELDS` fehlte `format`** —
  `editor.js :: saveItem()` sendet `format: "markdown"` bei **jedem** Speichern
  (`editor.js:335`); ohne dieses Feld in der Whitelist hätte A4 jedes UI-Speichern mit `400`
  gebrochen. Korrigierte Feldliste notiert, wird mit A4 geschrieben.

**A1 — ID sichtbar + auffindbar (`api.py :: _items_get`, `editor.js`, `app.html`, `app.css`):**
ID-Zweig vor dem bestehenden Store-Aufruf (`ITEM_ID_RE.fullmatch`), space-/ordnerübergreifend
(P7-D/E), Rechteprüfung unverändert davor — eine ID ohne Leserecht liefert `total: 0`, nie
403/404 (kein Existenz-Orakel). `idChip(itemId)` (neu, `editor.js`) in beiden Detailansichten
(readonly `roMetaEl`, editierbar `#meta-item-id`), Klick kopiert über
`navigator.clipboard.writeText`, kein `execCommand`-Fallback. Such-Placeholder nennt jetzt
`itm_…`. **Tabu-Probe:** `git diff phase1_storage/storage/` leer (P7-D eingehalten).

**A2 — Tool-Beschreibungen nennen Titel, nicht ID (`mcpserver/tools.py`):** neue Konstante
`_TITLE_NOT_ID_HINT`, wörtlich identisch an `search_items`/`get_item`/`get_item_meta`/
`create_item` angehängt, gleiche Bauart wie `WRITE_TOOL_DIVISION`/`_LIST_SPACES_POINTER`.

**Tests:** +5 (`test_items_get_finds_an_item_by_its_id`,
`test_id_lookup_ignores_space_and_folder_filter`, `test_id_lookup_respects_read_permission`,
`test_id_lookup_with_unknown_id_returns_empty_list` in `phase5_ui/tests/test_api.py`;
`test_tool_descriptions_tell_the_agent_to_name_titles_not_ids` in
`phase2_mcp/tests/test_tools.py`). `pytest -q` **833 passed** (828 + 5).

**Ehrlich offen:** DoD verlangt eine echte Browserprobe für den Chip (sichtbar, kopierbar) und
einen echten Connector-Beweis für A2 (P7-4) — **beides diese Session nicht gefahren**, nur
Backend/Tool-Ebene per `pytest`. Abnahmezeilen P7-1/P7-4 bleiben deshalb ⬜, P7-2 🟡 (Backend
bewiesen, keine Browserprobe), P7-3 ✅ (reiner Test-Fall, kein Mensch nötig).

**Nächster Schritt:** A3 (Bild-Entfernen-Knopf, V73-Konsequenz eingeplant) und A4 (Feld-
Whitelist, korrigierte Liste aus V74 oben) folgen als eigene Commits, wie mit dem Advisor
abgestimmt.

**Nachtrag, selber Tag — A3 gebaut (V73-Konsequenz umgesetzt).** `markdown.js :: inlineMarkdown()`
prüft jetzt vor jedem `asset:<id>`-Auflösen, ob die ID in einem mitgegebenen `assetIds` steht —
fehlt sie, rendert der Alt-Text statt eines `<img>` (ohne `assetIds` bleibt das alte Verhalten,
`updates.js`s Aufrufe sind unberührt). `editor.js`: `renderAssetStrip(item)` (neu) zeigt jedes
Asset mit Dateiname + „×"; Klick fragt per `confirmDialog()` nach, Wortlaut „entfernen"/„Papier-
korb" (nie „löschen", der Server verschiebt nur nach `_trash/`), ruft `DELETE .../assets/{id}`
(bereits vorhanden, kein neuer Serverpfad), aktualisiert `item.assets` lokal und rendert Leiste +
Vorschau neu. `snapshotFromItem()` trägt jetzt `assets` mit, ein neu hochgeladenes Bild wird
sofort in `state.editingSnapshot.assets` gepusht (sonst zeigte die Leiste es erst nach dem
nächsten Neuladen).

**Echter Nebenfund beim Bauen, nicht Teil des Plans:** `_items_patch`/`_items_append`/
`_items_archive` (`webui/api.py`) reichten `item_to_json()` bisher **ohne** `assets=` durch —
jede Antwort trug `assets: []`, unabhängig vom tatsächlichen Bestand. `editor.js :: afterWrite()`
lädt den Editor direkt aus genau dieser Antwort neu (`loadEditorFromItem(item, …)`) — ohne den
Fix hätte jedes Speichern nach einem Bild-Einfügen die Asset-Leiste geleert und `assetIds` beim
nächsten Render-Zyklus leer gemacht, was ein soeben eingefügtes Bild fälschlich als Alt-Text
gezeigt hätte. Behoben: alle drei Endpunkte reichen jetzt `assets=store.list_assets(item.id)`
durch, wie `_items_get_one` es schon tat. Bewusst **nicht** mitbehoben: `_map_store_error()`s
Konfliktantwort (`detail.current`) trägt weiterhin keine `assets` — das ist eine reine
Modulfunktion ohne `store`-Zugriff, eine Signaturänderung hätte jeden Aufrufer in der Datei
berührt; der Konfliktdialog zeigt ohnehin keine Bildvorschau, also kein beobachtbarer Fehler,
nur vorsorglich notiert.

**Test:** +1 `phase5_ui/tests/test_api.py :: test_assets_survive_a_patch_response` (Bild
hochladen, PATCH + append, beide Antworten tragen das Asset). `pytest -q` **834 passed**
(833 + 1). Tabu-Probe (`storage/`) weiterhin leer — der Fix blieb vollständig in `webui/api.py`.

**Ehrlich offen, wie bei A1/A2:** keine Browserprobe für den Entfernen-Knopf/Alt-Text-Übergang
diese Session — P7-5 bleibt ⬜ „gebaut, ungeprüft" in der Abnahmematrix.

**Nachtrag, selber Tag — A4 gebaut (schließt O6).** `_PATCH_FIELDS`-Konstante in `webui/api.py`,
Prüfung `unknown = sorted(set(body) - _PATCH_FIELDS)` direkt nach `body = await
_json_body(request)`, vor jeder Rechteprüfung (unbekannte Felder werden abgewiesen, bevor
irgendetwas anderes über den Request nachdenkt). Liste ist die durch V74 korrigierte Fassung
(inkl. `format`, siehe Nachtrag oben) — `version`/`title`/`body`/`status`/`due`/`tags`/`links`/
`type`/`format`/`folder`/`space`/`visibility`/`share_read`/`share_write`/`password`/`totp`.
**Zwei Tests:** `test_items_patch_rejects_an_unknown_field` (`spce`-Tippfehler-Fall aus
`ITEM_MOVE_PLAN.md` §112, Datei bleibt byte-identisch unverändert) und
`test_items_patch_accepts_every_field_the_ui_sends` (pinnt `_PATCH_FIELDS` als Obermenge der
real von `editor.js`/`list.js`/`dialogs.js` gesendeten Schlüssel). **Ein Plan-Detail korrigiert
beim Testen, nicht angenommen:** der Plan-Text nennt „400 validation_failed" für den
Zurückweisungsfall — `webui/errors.py` bildet `validation_failed` durchgehend auf `422`
ab (Unprocessable Entity), nicht 400; der Test pinnt den tatsächlichen Code.

**Tests:** `pytest -q` **836 passed** (834 + 2). Tabu-Probe (`storage/`) weiterhin leer.

**Block A damit vollständig: A1, A2, A3, A4 gebaut, alle vier nur backend-/tool-seitig
verifiziert (`pytest`), keine der vier Browser-/Connector-Proben diese Session gefahren.**
Verbleibend in Block A: A5 (Sichtbarkeits-Migration, braucht den Nikinger für `--apply`), A6
(Purge-Gate, kalendarisch erst ab 2026-08-28), A7/A7b (dritter Principal `testnutzer-p7`, braucht
den Nikinger für die Einladung), A8 (formaler Abschluss Phase 6.5, setzt A3/A7 voraus). Session
hier bewusst gestoppt — die nächsten Schritte brauchen entweder den Nikinger direkt oder bauen
auf etwas auf, das er noch anstoßen muss.

**Nachtrag, selber Tag — zwei Vorarbeiten erledigt, die Claude Code selbst darf (Advisor-
Hinweis), damit der Nikinger-Handgriff kein blinder Griff wird:**

**A5 Schritt 2 (Claude-Code-Sache laut Plan): `migrate_visibility.py --dry-run` gegen den
echten `DATA_ROOT` gelaufen** (`--data-root /home/savefyx/savefyx-data`, Default ist bereits
`--dry-run`, kein `--apply`). Ergebnis: **`items_migrated: 73`, `dry_run: true`, `spaces_touched:
["IT-Sekus-Projekt", "fabian", "niklas"]`** — exakte Deckung mit der Plan-Erwartung (Handover §1
Punkt 4). Alle 73 Zeilen zeigen `"before": null, "after": "private"`. Kein Schreibzugriff (Skript
selbst berichtet `dry_run: true`, kein `git log`-Nachtrag im `DATA_ROOT` geprüft nötig, da das
Skript bei `--dry-run` laut eigenem Code keinen Store-Write auslöst). **A5 Schritt 3 (`--apply`)
bleibt Nikinger-Sache (P7-H) — nicht ausgeführt.**

**V75 geschlossen, gegen eine Wegwerf-Instanz, nicht den echten `DATA_ROOT`:** `spacectl.py
create-space testnutzer-p7` gegen ein Temp-Verzeichnis — Space-Name mit Bindestrich angenommen,
kein Sonderzeichen-Fehler (`_cmd_create_space` prüft nur `/`, führenden `.`, `RESERVED_DIR_NAMES`
— ein Bindestrich fällt in keine der drei Kategorien). `Store.create("testnutzer-p7", ...)`
direkt danach: Item angelegt, Datei liegt unter `testnutzer-p7/itm_…__v75-testprobe.md`,
`store.search(space="testnutzer-p7")` findet es wieder. **Der Bindestrich übersteht Anlegen,
Schreiben und Suchen — keine Sonderbehandlung nötig, `authctl.py invite --space
testnutzer-p7` kann unverändert kommen.**

**Zwei offene Fragen für den Nikinger, bevor A5/A7 weitergehen können (nicht von Claude Code
entscheidbar):**
1. **A5 Schritt 1** (`docs/UPDATE_LOG.md`-Eintrag, muss auf den `--apply`-Tag datiert sein,
   `deploy.sh` bricht sonst ab, P6-X) — läuft `--apply` heute (2026-08-23, Eintrag jetzt
   schreibbar) oder an einem späteren Tag (Eintrag dann)?
2. **A7 Schritt 1** — wann kann `authctl.py invite --space testnutzer-p7 --purpose enroll`
   laufen? Danach übernimmt Claude Code das Enrollment im Browser (`claude-in-chrome`) und den
   Rest von A7/A7b ohne weiteren Nikinger-Handgriff.

**Beide Fragen beantwortet (Nikinger, per AskUserQuestion, selber Tag): heute, auf beide.**
`docs/UPDATE_LOG.md` bekam den A5-Eintrag (2026-08-23, bewusst zurückhaltend formuliert — die
Migration macht laut Skript-Docstring nur explizit, was implizit längst galt, „sichtbar ändert
sich für dich nichts"), gegen `test_updates.py`/`test_deploy_scripts.py` grün geprüft (28/28).
**`authctl.py invite`/`spacectl.py create-space testnutzer-p7` bleiben laut Plan-Text
ausdrücklich „Nikinger, einmalig" — Claude Code führt sie nicht selbst aus**, auch nach der
Freigabe nicht (Live-Schreibzugriff auf `auth.sqlite3`, dieselbe Vorsicht wie bei jedem
`--apply`). **Warte auf: (a) den Nikinger führt `--apply` aus, (b) den Nikinger führt `authctl.py
invite` aus und gibt den Link weiter** — beides außerhalb dessen, was Claude Code aus dieser
Session heraus selbst anstößt.

**Nachtrag, selber Tag — nach A5 `--apply`/A7 Anlegen/A7b: P7-10/P7-11/P7-12b geschlossen, zwei
echte Funde unterwegs.**

**Fund 1 — claude.ai dedupliziert Custom Connectors organisationsweit nach Server-URL.** Ein
zweiter, eigener Connector `sharefyx-testnutzer-p7` (dieselbe MCP-URL wie der bestehende
`sharefyx`-Connector) ließ sich in claude.ai nicht anlegen: „In deiner Organisation existiert
bereits ein Connector mit dieser URL." Der OAuth-Login selbst funktionierte (Passwort+TOTP
akzeptiert, Redirect korrekt) — der Server ist gesund, die Blockade sitzt eine Ebene höher, in
claude.ai selbst. **Konsequenz:** P7-10/P7-12b laufen seither über
`phase7_spaces_admin/scripts/p7_10_write_probe.py` — einen echten Netz-OAuth-Client (DCR+PKCE,
`testcred.py`-gestützt), der denselben Authorization Server direkt anspricht, ohne einen
claude.ai-Connector zu brauchen. Ergebnis: `own_space_visible: true`, `itm_ee1e0323` geschrieben.
**Nebeneffekt, kein separater Nachweis nötig:** derselbe Lauf beweist P7-12b (Login allein über
`testcred.py`, kein Nikinger-Handgriff).

**Nebenfund, real reproduziert (nicht Teil des Plans):** das `computer`-Type-Tool des
Browser-Automations-Kanals ließ bei einem langen, schnell getippten String zuverlässig das
letzte Zeichen fallen (`…/mcp` → `…/mc`) — zweimal reproduziert, per Zoom-Screenshot UND
Accessibility-Tree bestätigt, nicht nur per Screenshot vermutet. Fund kam vom Nikinger selbst
(„du hast da einen Tippfehler"), nicht von Claude Code entdeckt. Kein sharefyx-Bug — Werkzeug-
Eigenheit, hier nur vermerkt, falls sie bei künftiger Browser-Automation wieder auftritt: ans
Feldende springen und das fehlende Zeichen einzeln nachtippen, dann per Zoom verifizieren.

**Fund 2 — die `Freigeben`-Dialogbox kann kein item-level Share an einen brandneuen Principal
setzen.** `dialogs.js :: openShareDialog()` listet ausdrücklich nur `state.spaces` (Spaces, die
der Actor schon über ein bestehendes `.share.yml` kennt) — dokumentierter, bewusster Scope-
Schnitt aus Step 7 Commit 5b (`phase6_shares/CLAUDE.md`, Modul-Zeile 15). `testnutzer-p7` hat
laut P7-11s eigenem Zweck **keinerlei** vorherige Beziehung zu `niklas` — genau der Fall, den
die Dialogbox nicht abdeckt. Kein Bug: `webui/api.py :: _items_patch` UND
`mcpserver/tools.py :: update_item()` erlauben `share_read`/`share_write` beide bereits
serverseitig für Menschen (P6-M sperrt nur MCP-Tools), die Lücke ist rein die Dialogbox-Fläche.
**Ein Versuch, das über einen rohen `fetch()`-`PATCH` aus der Browser-Konsole zu umgehen,
scheiterte korrekt** (`403 csrf_failed`) — der Double-Submit-CSRF-Token wird ausschließlich
einmalig auf der echten Login-Erfolgsseite ausgeliefert (P5-H), eine frisch navigierte
Tab-Session hat ihn nicht, und ihn zu bekommen hätte Niklas' echtes Passwort/TOTP gebraucht.
**Bestätigt: die Sicherheitsgrenze hält, kein Leck.** Stattdessen:
`phase7_spaces_admin/scripts/p7_11_setup_fixture.py` (neu) — ruft `storage.store.Store.update()`
direkt auf (Details/Einschränkung siehe Korrektur unten). Ergebnis: `itm_3d0ac2b3` trägt jetzt
`share_read: ["testnutzer-p7"]`, echter Git-Commit, `version` 1→2.

**P7-11-Ergebnis, zweifach belegt (Advisor-Hinweis: die MCP-Probe allein testet die falsche
Fläche — P6-Zeilen 36/37 sind ausdrücklich Web-UI-Kriterien, nicht der bereits vorher
funktionierende Agenten-Pfad):**
1. **MCP:** `p7_11_visibility_probe.py itm_3d0ac2b3` → `expected_item_visible: true`,
   `foreign_ids: ["itm_3d0ac2b3"]`, `foreign_ids_are_exactly_expected: true`.
2. **Web-UI, echter Login als `testnutzer-p7`** (`/ui/login`, dieselben drei Felder wie
   `/oauth/authorize`, `testcred.py`-gestützt): **P6-Zeile 36** — „Alle Items" zeigt genau zwei
   Einträge, `P7-10 Schreibprobe` (eigen) und `P7-11 Sichtbarkeitsprobe` (fremd, Chip „geteilt
   mit testnutzer-p7"), Klick öffnet es. **P6-Zeile 37** — Detailansicht zeigt „Nur lesen —
   fremder Space (niklas)", kein Editor (nur `share_read`, kein `share_write`). **Damit
   erstmals ein Empfänger ohne jede Space-Mitgliedschaft real durchgespielt** — mit `niklas`
   strukturell nie möglich (steht in `fabian/.share.yml` unter `read:`), das war der eigentliche
   Grund für den dritten Principal (P7-J).

**Nebenwirkung, bewusst in Kauf genommen:** der `/ui/login`-Lauf als `testnutzer-p7` hat Niklas'
eigene aktive UI-Sitzung im selben Browser beendet (ein Session-Cookie pro Domain) — Niklas
muss sich in der Web-UI neu anmelden, sein Passwort/TOTP war davon nie betroffen.

**Korrektur nach Advisor-Review, vor dem Commit:** der ursprüngliche Versuch, das CSRF-geschützte
`PATCH /api/v1/items/{id}` per rohem `fetch()` aus der Browserkonsole in einer frisch navigierten
(nicht über den echten Login-Fluss bootstrapten) Tab-Sitzung zu setzen, schlug korrekt mit `403
csrf_failed` fehl — das ist die Sicherheitsgrenze aus P5-H, die hält, kein Leck. Der
Double-Submit-CSRF-Token wird ausschließlich einmalig auf der echten Login-Erfolgsseite
ausgeliefert; ihn zu bekommen hätte Niklas' echtes Passwort/TOTP gebraucht. Deshalb stattdessen
`p7_11_setup_fixture.py` über `Store.update()` direkt — **ohne** das Re-Auth-Gate aus P6-N
(`require_share_reauth()`), das `_items_patch` einer Freigabe-Erweiterung davorschaltet
(Docstring korrigiert, Advisor-Fund).

**Teardown-Hinweis für P7-12, jetzt vermerkt statt erst beim Abbau entdeckt (Advisor-Fund):**
`spacectl.py check` prüft ausschließlich `.share.yml` (space-level), nie item-level
`share_read`/`share_write` in Frontmatter. Nach `spacectl.py remove-space testnutzer-p7` bliebe
`share_read: [testnutzer-p7]` auf `itm_3d0ac2b3` sonst eine verwaiste Freigabe, die kein
Werkzeug meldet — P7-12s Kriterium „keine verwaisten Freigaben" wäre dann ein falsches ✅. Vor
dem Abbau: diese Freigabe zurücknehmen oder das Fixture-Item archivieren.

**`pytest -q` 843 passed** (unverändert — die drei neuen Skripte sind Live-Probe-Skripte ohne
eigene Unit-Tests, gleiche Kategorie wie `oauth_smoke.py`/`migrate_visibility.py`). Tabu-Diff
(`mcpserver/asgi.py`, `authserver/{crypto,totp,passwords,resolver,flows}.py`) weiterhin leer.

**Vormerkung für den Fabian-Freigeben-Schnitt/§0.4:** die `Freigeben`-Dialogbox „nur bereits
bekannte Spaces" ist derselbe Scope-Schnitt, der P7-14/P7-16 (geteilte Spaces im Browser
anlegen/freigeben) betreffen könnte — dort wird der Zielraum aber immer VORHER angelegt/bekannt
sein (Block C), betrifft also vermutlich nicht dasselbe Muster. Nicht weiter verfolgt, außerhalb
dieses Fundes.

**Nächster Schritt:** P7-12 (Abbau — `testcred.py purge`, `spacectl.py remove-space
testnutzer-p7 --force`, `authctl.py disable-user`/`revoke-sessions`) erst am Ende von Block A,
nicht jetzt — `testnutzer-p7` wird für A8/weitere Abnahmezeilen noch gebraucht.

**Nachtrag, selber Tag — A8 (Phase 6.5 formal abschließen, P7-I) durchgeführt.**

**Advisor-Runde vor dem Bauen:** A8.1s Plan-Text („A3 schließt P6.5-12; A7 schließt P6.5-8 und
P6.5-13") war zum Zeitpunkt seines Entwurfs eine Absicht, keine gemessene Tatsache — vor dem
Schreiben des Handovers geprüft statt übernommen. **Diskriminierender Befund:** weder
`itm_3d0ac2b3` noch `itm_ee1e0323` trugen ein `_assets/`-Verzeichnis im echten `DATA_ROOT` — A3
baute den Knopf, testete ihn aber nicht am Bild; A7s Proben (`p7_10`/`p7_11`) berührten nie ein
Asset. A8.1s Satz war damit Plan-Drift, kein erledigter Punkt.

**P6.5-12/P7-5 — Browser-Nachweis dieser Sitzung bewusst nicht gefahren.** Ein Login als
`testnutzer-p7` im echten Chrome-Tab hätte Passwort/TOTP aus `testcred.py` in eine
`computer`-Type-Aktion getippt — anders als bei `p7_10`/`p7_11` (dort las das Skript die
Credentials intern, nie sichtbar für Claude Code) wäre das Geheimnis hier im sichtbaren
Werkzeugverlauf dieser Sitzung gelandet. Ein direkter `python -c`-Ausdruck, der `testcred.py
password`/`totp` roh ausgibt, wurde vom Auto-Mode-Classifier korrekt blockiert — als Bestätigung
behandelt, nicht umgangen. P6.5-12/P7-5 bleiben deshalb 🟡/⬜ (gebaut, ungeprüft), keine Regression.

**P6.5-13 — MCP-Fläche, per echtem OAuth-Client geschlossen.** `p7_13_asset_fixture.py itm_id`
(neu, Store-direkt) legte ein PIL-erzeugtes PNG auf `itm_3d0ac2b3` ab (`ast_e7f27214`, 77 Bytes)
— derselbe Store-Kürzungsweg wie `p7_11_setup_fixture.py`, kein neuer Serverpfad.
`p7_13_asset_share_gate_probe.py` (neu, gleiche OAuth-Bauart wie `p7_10_write_probe.py`) rief
`get_item_asset` als `testnutzer-p7` auf: mit reinem `share_read` (aus P7-11) →
`bytes_available:false`, nur Metadaten. `p7_13_share_write_fixture.py itm_id --version 2` (neu)
erweiterte auf `share_write` — derselbe Aufruf lieferte danach echte `image/png`-Bytes. **Exakt
das kommentierte P6.5-M-Verhalten (`tools.py :: get_item_asset()`), empirisch bestätigt, kein
neuer Sicherheitsbefund.**

**P6.5-8 — Web-UI-Fläche, per Cookie-Session-Skript statt Browser-Klick geschlossen.**
`p7_13_ui_asset_probe.py` (neu) postet gegen `/ui/login` (Cookie-Session, P5-D) und holt danach
`GET /api/v1/items/{id}/assets/{id}` — dieselbe Bauart wie die MCP-Probe, nur gegen die
Cookie-Fläche.

**Advisor-Fund, VOR dem Commit korrigiert (nicht danach entdeckt):** der erste Testlauf setzte
„ohne Session" (kein Cookie überhaupt, `401`, reine Authentifizierung — dieselbe Fläche wie P5
Zeile 19, nicht neu geprüft) mit „ohne Freigabe" (P6.5-8s tatsächliches Kriterium — angemeldet,
aber kein `share_read`/`share_write`) gleich und schloss daraus fälschlich auf einen
„Plan-Text-Drift" (Plan nennt `403`). **Drei saubere Zustände desselben Items nachgeholt, ein
Variable je Schritt geändert** (`p7_13_share_write_fixture.py --clear`/`--clear-read`, Item-
Version 3→4→5): `share_write` geleert, `share_read` behalten → UI `200` (HUMAN-Fläche braucht
nur Leserecht, P6-AW — bestätigt zugleich P6.5-13s Asymmetrie, MCP-Seite bleibt
`bytes_available:false` unter derselben Bedingung, sauber reproduziert); danach auch
`share_read` geleert → UI-`authenticated_status`: **`403`, deckungsgleich mit dem Plan-Text.**
**Der Plan-Text war richtig, der ursprüngliche „401 statt 403"-Befund war der eigentliche
Fehler.** Korrigiert in `phase6_5_tools_images/CLAUDE.md`s P6.5-8-Zeile (dortige, datierte
Korrekturnotiz, kein stilles Überschreiben).

**Teardown, gleich mitgezogen statt erst bei P7-12:** `p7_13_teardown.py` (neu,
`store.delete_asset()`) entfernt `ast_e7f27214` — landet wie jedes gelöschte Asset in
`_assets/itm_3d0ac2b3/_trash/` (N5, kein echtes Löschen, Entscheidung H bleibt unangetastet),
`list_assets()` zeigt danach `[]`. `share_read`/`share_write` sind bereits durch den dritten
Testzustand oben auf `[]` (Version 5). **Alle vier Teardown-Ledger-Punkte damit vorzeitig
geschlossen** — P7-12 selbst hat für `itm_3d0ac2b3` nichts mehr zu tun.

**Abnahmestand 6.5 neu gezählt (A8.2): 12 von 14**, nicht 14/14 — Glyph bleibt 🟡, aus der
Zahl abgeleitet, kein Grenzfall (P6.5-12 UND P6.5-14 offen, nicht nur P6.5-14 wie im
13/14-Beispiel des Plans). Details, Kriterienliste, `[VERIFY]`-Bilanz:
`docs/concepts/PHASE6_5_CLOSEOUT_HANDOVER.md` (neu). `phase6_5_tools_images/CLAUDE.md`s Matrix
+ `updated:`-Zeile korrigiert (kein neuer Session-Block dort — Rotationsregel, die Erzählung
lebt hier). `phase1_storage/CLAUDE.md`: Öffnungen 3/4/5 datiert geschlossen, Öffnung 6 (P7,
`acl.py`-Schreibseite) im selben Absatz als weiterhin offen benannt (A8.5, vermeidet die
Falschaussage, die P6-Handover §5.6 bereits umging). `docs/concepts/
phase6_5_tools_images_uebersicht.svg` (neu, 1080×1080) — zweimal gerendert und per `Read`
visuell geprüft, kein Textüberlauf. `ROADMAP.md`/Root-`CLAUDE.md`/`docs/INDEX.md` im selben
Umfang auf den neuen 6.5-Status gezogen — Root-`CLAUDE.md`s „Current state" hatte Phase 7 bisher
gar nicht erwähnt (eigener kleiner Fund, kein A8-Punkt, aber dieselbe Kategorie Doku-Drift wie
Step 0s Audit).

**Teardown-Ledger — alle vier Punkte bereits diese Sitzung geschlossen, nicht erst bei P7-12
(siehe „Advisor-Fund" oben: die dritte Nachprobe brauchte den geleerten Zustand ohnehin):**
`itm_3d0ac2b3` trägt jetzt `share_read: []`, `share_write: []` (Version 5) und `ast_e7f27214`
liegt in `_trash/` (`p7_13_teardown.py`, `list_assets()` → `[]`). Nichts bleibt für P7-12 an
diesem Item übrig.

**`pytest -q` weiterhin 843 passed** (fünf neue Skripte — vier aus der ersten A8-Runde plus
`p7_13_teardown.py` — alle Live-Probe-Kategorie ohne eigenen Unit-Test). Tabu-Diff unverändert
leer.

**Nächster Schritt:** A6 (Purge-Gate, `clients`/`token_families`-Rückgang, frühestens
2026-08-28) ist der letzte offene Block-A-Punkt außer P7-12 selbst. Bis dahin: Session hier
gestoppt — A6 ist kalendarisch blockiert, kein Claude-Code-Handgriff verkürzt das.

