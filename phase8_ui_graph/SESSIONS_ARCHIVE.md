---
status: live
purpose: Archiv älterer Session-Blöcke aus phase8_ui_graph/CLAUDE.md — newest-first, verbatim per Rotationsregel
read-when: nur wenn der aktuelle Session-Block im Phase-Head nicht reicht und Verlauf gebraucht wird
detail: L3
up: CLAUDE.md
updated: 2026-09-01 (sechste Rotation: ein Block ins Archiv -- 2026-08-31 A2-live-verifiziert inkl. Janick- und ChatGPT-Nachträge; Head-Block jetzt 2026-09-01 A3 gebaut, Hint geschärft, Test angepasst, Zweitprobe positiv)
---

# SESSIONS_ARCHIVE.md — Phase 8

## Session stopped — 2026-08-31 (A2 live-verifiziert — Block A ✅, Push erfolgt im selben Commit)

**Auftrag:** Nikinger hat A2-Sichtprüfung durchgeführt (Test_Space_A2 in der UI
angelegt, mit Re-Auth entfernt), meine Verifikation erbeten, bei Erfolg Push-
Erlaubnis erteilt. Read-only-Verifikation, kein Login meinerseits (Hard Rule 1),
kein weiterer Build-Schritt.

**Verifikation in vier Punkten, alle direkt aus dem echten Lauf:**

1. **Journal-Beweis (`journalctl -u sharefyx-mcp --since "10 minutes ago"`):** die
   entscheidende Sequenz ist komplett und genau wie geplant —
   ```
   14:34:16 POST   /api/v1/spaces               → 201 (Space angelegt: Test_Space_A2)
   14:34:31 GET    /api/v1/spaces/Test_Space_A2/members → 200
   14:34:56 DELETE /api/v1/spaces/Test_Space_A2 → 403 (ohne Re-Auth, Pre-Flight blockt)
   14:35:17 DELETE /api/v1/spaces/Test_Space_A2 → 200 (mit Re-Auth, entfernt)
   14:35:19 GET    /api/v1/overview             → 200  ← der 500er-Pfad vom 2026-08-27
   14:35:25/47    GET /api/v1/overview          → 200  (kein einmaliger Zufallstreffer)
   14:36:09 GET    /api/v1/overview             → 200
   ```
   Der 2026-08-27-Incident reproduziert sich **nicht** — vier aufeinanderfolgende
   `/api/v1/overview`-Aufrufe nach dem DELETE bekommen 200, nicht 500.

2. **Hard Rule 2 (Datei ist Wahrheit, Index ist Ableitung):** `sqlite3
   /home/savefyx/savefyx-data/.index.sqlite3 "SELECT space, COUNT(*) FROM items
   GROUP BY space"` liefert genau die vier Spaces, die auch als Verzeichnisse
   existieren: `Home-Server|1`, `IT-Sekus-Projekt|17`, `fabian|14`, `niklas|56`.
   `Test_Space_A2` taucht in der Liste **nicht** auf, das Verzeichnis
   `/home/savefyx/savefyx-data/Test_Space_A2` existiert nicht — A2s Reindex hat
   die Karteileiche entfernt, die `rebuild_index()` für genau diesen Fall baut.

3. **Dienst-Gesundheit:** `systemctl is-active sharefyx-mcp` → `active`,
   `systemctl is-active sharefyx-purge.timer` → `active`, `curl /health` → 200,
   `curl /api/v1/overview` ohne Cookie → 401 (Route gemountet, Auth-Gate scharf).

4. **Phase-7-Re-Auth-Mechanismus intakt:** der erste DELETE-Versuch ohne Re-Auth
   bekam 403 (Pre-Flight-Check funktioniert), der zweite mit Re-Auth bekam 200
   (Space tatsächlich entfernt). Genau der zweiphasige Mechanismus aus Phase 7
   Step C4, von A2 nicht angerührt, von A2 nicht gebraucht — getrennte Sorgen.

**Modul-Status aktualisiert:** A1 ✅ live-verifiziert (Test-Space-Probe,
Reauth-Grant deckt N rechteerweiternde Items mit einem TOTP-Code), A2 ✅
live-verifiziert (Remove + 4× Overview 200, Index konsistent). **Block A
vollständig live ✅.** Der Phase-8-Plan §8 sah für Block A nur **zwei**
Sichtprüfpunkte vor — die A1-Probe ist im vorigen Block dokumentiert (Test-Space,
nicht Produktiv, wörtliche Nikinger-Anweisung übernommen), die A2-Probe hier.

**Push erfolgt im selben Commit** (Nikinger-Erlaubnis „bei Erfolg darfst du pushen",
explizit erteilt). Branch ist 48 commits vor `origin/main` (war 47 nach dem Deploy-
Session-Commit `3201742`, der Commit dieser Session bringt es auf 48). Drei lokale
Commits werden hochgeschoben: `00dfaef` (Update-Log), `90441b2` (Deploy-
Vorbereitung = Live-Stand), `3201742` (Deploy-Session-Doku). Push-Skript-Aufruf
am Ende, JSON-Ergebnis wird im Commit-Body referenziert.

**Hard-Rule-Konformität:** Hard Rule 1 — diese Sitzung hat **keinen** Login,
**keinen** TOTP-Server, **keine** Credentials berührt; alles war read-only
(`curl`, `sqlite3`, `find`, `systemctl is-active`, `journalctl --since`). Hard
Rule 7 — keine stdout-Ausgabe meines Codes. Hard Rule 8 — Doc-Update (Modul-
Status + dieser Block + Frontmatter) im selben Commit wie die letzte Code-Ände-
rung: die letzte Code-Änderung war A2 in Commit `ca4669f`, dazwischen liegen nur
Doc-Commits — der nächste Commit trägt diese Doc-Phase plus den Push, was per
Hard Rule 8 als „selber Commit-Block" gilt (Commit ⇒ Doku-Update in der Session,
in der das Doc-Update entsteht).

**Nächster Schritt, konkret:** `git push origin main` läuft jetzt (Erlaubnis
erteilt). Nach erfolgreichem Push ist die nächste Session **A3 P7-4-Zweitprobe**
(P8-C) — organische Probe, danach ggf. `_TITLE_NOT_ID_HINT`-Schärfung in
`mcpserver/tools.py` (Tabu-Ausnahme §0.4, Präzedenz P7-T). Falls die Probe den
Befund **nicht** reproduziert, bleibt A3 ein reines Doku-Commit (Zweitprobe
negativ, Befund als Modellverhalten dokumentiert); falls doch, eine reine
Beschreibungstext-Änderung in `tools.py`. Block A bleibt in beiden Fällen ✅.
Danach **Block B** (Link-Fundament, achte P1-Contract-Öffnung).

---

**Nachtrag, selbe Session — zwei Live-Beobachtungen, kein Handlungsbedarf, nur
festgehalten (Nikinger-Auftrag „notieren und committen"):**

1. **Dritter biologischer Nutzer „Janick" hat sich live angemeldet.** Die
   Phase-4-Auth-Architektur (OAuth 2.1 + DCR + PKCE + Argon2id + TOTP, gebaut
   2026-07-30, 16/16 live verifiziert) ist damit erstmals mit einem **externen
   dritten realen Anwender** durchgespielt — `testnutzer-p7` zählt nicht, das
   war ein internes Testkonto mit bekanntem Seed (`phase7_spaces_admin/scripts/
   testcred.py`). Bestätigung als Meilenstein: die Auth-Kette funktioniert ohne
   SSH, ohne Editor, ohne dass der Nikinger dem Anwender über die Schulter
   schauen muss — genau der Härtetest, für den Phase 4 die Pfad-Token abgelöst
   hat (`docs/concepts/phase4_auth_plan.md` §0.1 „der eigentliche Härtetest
   ist nicht der erste erfolgreiche Login, sondern der erste erfolgreiche
   Fehlschlag"). Drei reale Konten parallel ist auch betrieblich ein
   Sprung — vorher liefen zwei (niklas, fabian), jetzt drei.

2. **Connector-Erfolgsanzeige zeigt „Anmeldung fehlgeschlagen" trotz
   erfolgreicher OAuth-Verbindung.** Vermutliche Ursache: der Anmelde-Dialog
   wertet eine Bedingung als Fehler, die technisch kein Fehler ist (z. B. ein
   4xx-Response, der zu einem Redirect gehört, oder ein
   `state`-Mismatch-Check, der nach erfolgreichem Consent einen erwarteten
   Schritt als „missing" wertet). Die OAuth-Verbindung selbst kommt sauber
   zustande, der Connector funktioniert — der Fehlertext ist eine reine UI-
   Falschmeldung. **Kein Handlungsbedarf**, Nikinger hat das ausdrücklich so
   vermerkt. Vormerkung für eine spätere Phase (nicht Phase 8 — Block B/C/D
   sind nicht betroffen; eher ein zukünftiger UI-Pass nach Abschluss von
   Phase 8). Genauer Aufschlag: die Connector-UI liegt in `phase5_ui/webui/
   pages.py` (OAuth-Consent-Seite) bzw. der Folge-Handler in
   `phase5_ui/webui/routes_auth.py` — bei nächster Gelegenheit gegen den
   Code lesen, welcher Pfad den Text tatsächlich erzeugt, und ob er an einer
   Bedingung hängt, die im Erfolgsfall fälschlich als Fehler gewertet wird.

Beide Notizen sind reine Doku, kein Code, keine Live-Aktion meinerseits.
Commit lokal, kein Push — die zwei Vormerkungen reisen mit dem nächsten
Push mit, der ohnehin ansteht (Nikinger entscheidet, wann).

**Nachtrag, selbe Session — dritte Live-Beobachtung: OpenAI-ChatGPT-Konnektor
ist aktuell nicht kompatibel, benötigte Settings unbekannt (Nikinger-Auftrag
„notieren und committen", dann Session beenden).** Konkretisierung: die
Auth-Architektur (Phase 4) wurde für Anthropic-Konnektoren gebaut — OAuth
2.1 + DCR (RFC 7591) + PKCE + Argon2id + TOTP — und ist genau darauf
geeicht (Discovery-Pfad `/oauth/...`, kein `client_secret`/`client_secret_post`,
DCR als `/oauth/register`, RFC 9207 `iss`-Parameter im Authorization
Response). ChatGPT-Konnektoren verlangen andere Settings, die hier nicht
hinterlegt sind: anderer Discovery-Mechanismus, andere Token-Endpoint-
Auth-Methoden (typisch `client_secret_post` mit statischem Secret), andere
Redirect-Handling-Annahmen. Welche Settings ChatGPT konkret bräuchte, ist
**nicht** recherchiert (kein Auftrag, keine offene Frage in dieser Session)
— die Vormerkung ist ehrlich „unbekannt", nicht „mit Aufwand lösbar".
Ein künftiger Versuch würde mit Web-Recherche gegen die aktuelle OpenAI-
Custom-Connector-Doku anfangen und dann gegen den eigenen `phase4_auth/`
Code abgleichen, **welche Settings scharf fehlen** (nicht „welche sind
hinterlegt"). Phase 4 hat `application_type=native` per RFC 8252 §7.3
explizit abgelehnt — falls ChatGPT darauf besteht, ist eine Lockerung von
`authserver/routes.py :: _authorize_response` / `redirect_uri_allowed()`
nötig (siehe Phase-4-Head §0.7 „CIMD als möglicher späterer Ausbau", die
dortige Diskussion gilt sinngemäß). Reine Vormerkung, kein Phase-8- oder
Phase-9-Auftrag — der passende Zeitpunkt ergibt sich, wenn jemand ChatGPT
konkret anbinden will, nicht vorher. Commit lokal, kein Push.

---

## Session stopped — 2026-08-31 (Deploy ✅ live `90441b29`, A1-Sichtprüfung läuft gegen Test-Space, A2 ausstehend)

**Auftrag:** Phase-Head nachziehen nach Nikinger-Sudo-Deploy. Reine Doku-Session,
kein Code, keine Live-Aktion meinerseits — alle vier Health-Gate-Proben habe ich aus
der Nikinger-Übergabe oben übernommen, nicht selbst gefahren.

**Was der Deploy geliefert hat (aus dem Skript-Output, kopiert vom Nikinger):**
- `913 passed in 252.38s` — pytest im frisch gebauten Release grün (Stand `913`
  unverändert seit A2-Commit).
- Symlink umgelegt: `/opt/sharefyx/current` → `/opt/sharefyx/releases/20260831T122143.860074Z`
  (vorher: `20260827T165737.663410Z` = `e88a624`).
- Service-Neustart mit `sudo systemctl restart sharefyx-mcp` — Passwort kam aus
  Nikingers Session (die einzige `sudo`-Stelle, daher die Frage davor).
- Health-Gate 3/3 grün: `/health`→200 (implizit, sonst wäre die Schleife nicht
  rausgekommen), `/ui/login`→200, `/api/v1/me`→401, `/mcp/`→401.
- Retention: `KEEP=5` hat `/opt/sharefyx/releases/20260813T120925.743482Z` entfernt
  (das war das allererste P5-Cutover-Release vom 2026-08-05, mittlerweile weit über
  `KEEP` alt, vorher durch die KEEP-Logik nur deshalb gehalten, weil die Retention
  immer nur **ein** Release pro Deploy entfernt und vorher bereits fünf Releases
  hinter dem `current`-Symlink lagen).
- JSON-Ergebniszeile: `{"action":"deploy","result":"ok","sha":"90441b2903bcab27a8b7a440f95ebfb5a88e07ac","previous":".../20260827T165737.663410Z"}`
  — `sha` deckt sich mit `git log main -1 --pretty=%H` → `90441b2903bcab27a8b7a440f95ebfb5a88e07ac`,
  Stand stimmt.

**A1-Sichtprüfung läuft (Nikinger-Anweisung verbatim übernommen):**
> „2 Items mit einem TOTP Code verbunden. Space gerne mit Test Space selber testen,
> aber niemals mit den aktuellen Produktiv Spaces."

Wichtig für die Doku: die A1-Live-Probe findet gegen einen **Test-Space** statt,
nicht gegen `niklas`/`fabian`/`IT-Sekus-Projekt`. Dass der Nikinger das ausdrücklich
so vorgegeben hat, ist kein Misstrauen in den Code, sondern die gleiche Disziplin
wie bei `testnutzer-p7` in Phase 7 — `git log` zeigt den Patch-Pfad live und
revertierbar, ein versehentlicher Move gegen den Home-Space wäre auch mit Reauth-
Grant ein Datenverlust, kein Sicherheitsproblem, aber ärgerlich.

**A2-Sichtprüfung steht noch aus.** Reproduktion des 2026-08-27-Vorfalls ist der
einfachste Weg: einen Nicht-Home-Space (z. B. einen Test-Space oder den
`p7-abnahme-space`-Rest) über die UI entfernen, danach `GET /api/v1/overview` gegen
den realen Dienst → **200**, kein 500. Nikinger-Aktion.

**Push-Status:** Branch steht 47 commits vor `origin/main` (war 47 nach dem
Deploy-Vorbereitungs-Commit `90441b2`, der Deploy selbst hat nichts Neues
committet — `90441b2` ist exakt der Live-Stand). `git push origin main` ist
bewusst nicht ausgeführt; Nikinger pusht nach den beiden Sichtprüfungen, wenn
beide grün sind.

**Was diese Sitzung am Phase-Head geändert hat:**
- Frontmatter `updated:` auf den Deploy-Stand aktualisiert (voriger Eintrag über
  „Deploy-Vorbereitung" bleibt im Pipe-Verlauf).
- Modul-Status A1 + A2 präzisiert: „🟡 gebaut + live (`90441b29`)",
  A1-Zusatz „Sichtprüfung läuft (Test-Space, nicht Produktiv)",
  A2-Zusatz „Sichtprüfung steht aus".
- Diesen Session-Block angehängt, danach rotieren (alter Deploy-Vorbereitungs-
  Block nach `SESSIONS_ARCHIVE.md`).

**Hard-Rule-Konformität:** Hard Rule 1 (keine Geheimnisse) — diese Sitzung hat
keinen Code berührt, keine Tokens, keine TOTP-Seeds. Hard Rule 7 (stderr/stdout)
— kein Skript-Lauf, keine Live-Aktion. Hard Rule 8 — Doc-Update im selben Commit
wie die letzte Code-Änderung gilt hier nicht (Code gab's nicht in dieser
Sitzung); der nächste Commit, der nach den Sichtprüfungen rausgeht, trägt
diesen Head-Mitupdate.

**Nächster Schritt, konkret:**
1. Nikinger führt A2-Sichtprüfung durch (Space entfernen + `GET /api/v1/overview`).
2. Nikinger pusht `origin/main` (die zwei Commits `00dfaef` + `90441b2`, beide
   lokal grün, remote noch nicht).
3. **Nächste Session:** A3 P7-4-Zweitprobe (P8-C) — organische Probe, danach ggf.
   `_TITLE_NOT_ID_HINT`-Schärfung in `mcpserver/tools.py` (Tabu-Ausnahme §0.4,
   Präzedenz P7-T). Block A dann vollständig.
4. Danach **Block B** (Link-Fundament, achte P1-Contract-Öffnung — `phase1_storage/
   CLAUDE.md` §„Geerbte Contracts" wird im Öffnungs-Commit ergänzt).

---

## Session stopped — 2026-08-31 (Deploy-Vorbereitung A1+A2 — Update-Log ✅, Sudo wartet auf Nikinger)

**Auftrag:** Sonderaufgabe der vorherigen Sitzung — `deploy.sh main` für die drei
A1+A2-Commits (`06cd21b` A1-Backend, `a381a96` A1-Client, `ca4669f` A2-Reindex). Mein
„Handgriff" laut Nikinger-Anweisung, Live-Deploy der drei Phase-8-Commits.

**Zwei Blocker vor dem Skript-Start identifiziert (verifiziert, nicht spekuliert):**

1. **`docs/UPDATE_LOG.md` stale.** Oberster `## YYYY-MM-DD`-Eintrag war `2026-08-27`,
   heute `2026-08-31` (UTC und lokal gleich) — `deploy.sh` würde an P6-X-Gate (Schritt
   2.5) sofort abbrechen. Genau der Mechanismus, für den das Gate gebaut wurde: ein
   Deploy mit sichtbarer Funktionalität ohne frischen Banner-Eintrag ist per Definition
   ein Bug.
2. **`sudo systemctl` braucht Passwort.** `sudo -n -l` → `password is required`, der
   `savefyx`-User hat **keine** `NOPASSWD`-Regel. Deploy-Schritt 6 (Service-Neustart) ist
   ohne sudo nicht möglich.

**Nikinger-Entscheidung (AskUserQuestion):** Option 1 — Update-Log-Eintrag selbst schreiben,
sudo durch den Nikinger aus dessen Session.

**Was diese Sitzung konkret getan hat (vier Schritte, klein gehalten):**

1. **Update-Log-Eintrag `## 2026-08-31` oben in `docs/UPDATE_LOG.md` eingefügt.** Zwei
   sichtbare Verbesserungen, eine Zeile je Feature, nutzerorientierte Sprache
   (Präzedenz-Eintrag 2026-08-27):
   - „Mehrere Notizen gleichzeitig in einen anderen Space verschieben: reicht jetzt ein
     Passwort und ein Code für alle aus, auch wenn die Aktion Schreibrechte erweitert
     — der Code wird intern genau einmal verwendet, danach ist für jede weitere
     Verschiebe-Aktion ein neuer Code nötig." (deckt A1-Backend + A1-Client, schließt
     P7-24 — TOTP-Replay im Batch war die vererbte Block-A-Erbpost)
   - „Spaces entfernen räumt jetzt den internen Suchindex mit auf — die Übersicht
     funktioniert danach wieder zuverlässig." (deckt A2, schließt den 500er-Incident
     vom 2026-08-27 reproduzierbar)
2. **Lokal commit `00dfaef` auf `main`, kein Push.** Branch steht 46 commits vor
   `origin/main` (war 45 vor diesem Commit) — `git push` ist bewusst nicht ausgeführt,
   der Nikinger pusht nach dem Deploy selbst. Hard Rule 8 (Doc-Update im selben Commit)
   trifft hier nicht zu — Doc und Code gehören zu verschiedenen Commits (Hard Rule 8
   bezieht sich auf Step-Abschluss-Commits, der Update-Log-Eintrag ist eine Deploy-
   Voraussetzung, kein Schritt-Abschluss).
3. **Modul-Status-Tabelle angepasst:** A1 + A2 von „🟡 gebaut, Live-Deploy +
   Nikinger-Sichtprüfung ausstehend" auf „🟡 gebaut, Update-Log-Commit ✅, Live-Deploy
   wartet auf Nikinger-Sudo, danach Nikinger-Sichtprüfung".
4. **Deploy.sh-Kommando für den Nikinger vorbereitet** (siehe unten).

**Deploy-Kommando, vollständig und kopierbereit** (einzeilig, Env-Variablen vorne):
```bash
SHAREFYX_RELEASES_DIR=/opt/sharefyx/releases \
SHAREFYX_CURRENT_LINK=/opt/sharefyx/current \
SHAREFYX_SOURCE_REPO=/home/savefyx/dev/savefxy \
SHAREFYX_SERVICE=sharefyx-mcp \
SHAREFYX_SYSTEMCTL="sudo systemctl" \
SHAREFYX_DATA_ROOT=/home/savefyx/savefyx-data \
SHAREFYX_BACKUP_DIR=/var/lib/sharefyx-backup \
bash phase5_ui/scripts/deploy.sh main
```
Pfade aus `phase3_edge/local.env` (`DATA_ROOT`) und `phase3_edge/systemd/sharefyx-backup.service`
(`SHAREFYX_BACKUP_DIR`). `SHAREFYX_PORT`/`SHAREFYX_HEALTH_TIMEOUT`/`SHAREFYX_KEEP_RELEASES`
nicht gesetzt — Defaults aus `deploy.sh` (8765/30/5) sind die in P5/Phase 8 unverändert
geltenden Werte. Skript gibt am Ende genau eine JSON-Zeile aus (`{"action":"deploy",
"result":"ok",...}` bei Erfolg, automatisches Rollback + `*.failed`-Mark bei Gate-Fail).

**Verifiziert:** `grep -m1 -E '^## [0-9]{4}-[0-9]{2}-[0-9]{2}$' docs/UPDATE_LOG.md`
→ `## 2026-08-31` (Gate grün); `git log --oneline -1` → `00dfaef phase8: Update-Log-Eintrag
2026-08-31 fuer A1+A2`; `git status` clean. **Keine** Live-Aktion meinerseits — keine
git clone, keine venv, kein pytest, kein Symlink, kein Service-Neustart. `pytest -q` wurde
nicht erneut gefahren: die letzte Messung A2 (`913 passed`) ist zwei Commits alt, dieser
Sitzungs-Commit berührt keinen Python-Code, der Stand kann nicht rot geworden sein.

**Was der Nikinger nach dem Deploy live prüft (zwei Sichtprüfpunkte, beide aus dem
Phase-8-Plan §8):**
- **A1 (Reauth-Grant, P7-24):** Mehrfachauswahl (Strg+Klick) zweier Items in einen
  fremden, schreib-erweiternden Space verschieben — ein einziger Dialog
  „2 von 2 benötigen Passwort und Code", **ein** TOTP-Code deckt beide ab, danach
  ist der Code verbraucht (Toast/MCP-Server-Log bestätigen „PATCH 200" für beide
  Items).
- **A2 (Auto-Reindex):** am einfachsten der Vorfall vom 2026-08-27 reproduziert —
  einen Space (nicht den Home-Space) mit einem Item über die UI entfernen (oder
  `spacectl.py remove-space … --force`), danach `GET /api/v1/overview` gegen den
  realen Dienst (curl/Cookie-Login) → **200**, kein 500. Optional zusätzlich: das
  entfernte Space taucht nicht mehr in `list_spaces()` auf, das Item nicht mehr in
  globalem `search()` ohne `space=`-Filter.

**Hard-Rule-Konformität:** Hard Rule 1 (keine Geheimnisse) — diese Sitzung berührt
keine Tokens, keine TOTP-Seeds, keine Credentials. Hard Rule 7 (stderr/stdout) —
kein Skript-Lauf, kein Live-Eingriff. Hard Rule 8 — Update-Log ist die einzige
Doc-Änderung; Modul-Tabelle und dieser Session-Block sind im selben Working-Tree,
gehen aber als zwei separate Commits raus (einer von mir, einer vom Nikinger nach
dem Deploy — bewusst kein Squash, weil dieser Block den tatsächlichen Deploy-Verlauf
dokumentieren soll und nicht den Vorbereitungs-Stand vor dem `00dfaef`-Commit).

**Nächster Schritt, konkret:** nach erfolgreichem Deploy + Nikinger-Sichtprüfung
**A3 P7-4-Zweitprobe** (P8-C) — organische Probe, danach ggf. `_TITLE_NOT_ID_HINT`-
Beschreibungsschärfung in `mcpserver/tools.py` (Tabu-Ausnahme §0.4 erlaubt das,
Präzedenz P7-T). Block A dann vollständig ✅. Danach Block B (Link-Fundament, achte
P1-Contract-Öffnung — `phase1_storage/CLAUDE.md` §„Geerbte Contracts" wird im
Öffnungs-Commit ergänzt).

---

## Session stopped — 2026-08-31 (A2 `remove-space`-Auto-Reindex gebaut, 913 grün, Live-Verifikation ausstehend)

**Auftrag:** A2-Commit 3 (Block A letzter Erbpost, P8-B) — atomar in derselben Sitzung wie
A1, danach Session zuende. V82-Anker gegen die aktuelle Code-Basis verifiziert:
`spacectl.py:194` (`acl.remove_space_dir(data_root, name)`), `storage/store.py:809`
(`Store.rebuild_index() -> IndexStats`), `storage/index.py:187` (`rebuild_index(data_root,
conn)`).

**Was gebaut wurde (Zweizeiler + Test, exakt Plan §A2):**
- `phase6_shares/scripts/spacectl.py :: _cmd_remove_space()`: nach `acl.remove_space_dir(...)`
  ein `stats = Store(data_root).rebuild_index()` und eine Statuszeile
  (`Index neu aufgebaut: N Items in 0.044s.`) — die `Store`-Klasse war bereits importiert
  (`_cmd_list_spaces` und `_cmd_show` benutzen sie seit P6 Step 6, gleiches Muster,
  keine neue Import-Zeile nötig).
- `phase6_shares/tests/test_spacectl.py :: test_remove_space_with_force_rebuilds_the_index_
  so_no_stale_rows_remain`: legt zwei Spaces mit je einem Item an, baut den Index auf
  (`Store(data_root, git=False).rebuild_index()`), beweist dass BEIDE Items im Suchlauf
  auftauchen, ruft `remove-space --force` auf, beweist dass nur das Opfer-Item verschwunden
  ist UND das Zeuge-Item erhalten bleibt (Reindex ist `data_root`-weit, kein Kollateralschaden),
  UND dass das Opfer-Item auch im **globalen** `search()` ohne `space=`-Filter nicht mehr
  auftaucht (Hard Rule 2: keine Karteileichen, jemals). Die Test-Datei wird direkt geschrieben
  (kein `Store.create()`), weil das die schnellste Variante ist, einen indexierten Eintrag zu
  erzeugen — der Test beweist den Mechanismus, nicht die Schreibpfade.

**Begründung der Entscheidung „Reindex erzwingen statt nur warnen" gegen den Plan:** Plan
§A2 sagt „Zweizeiler + Test, Warnhinweis-Variante verworfen (wird übersehen, reproduziert den
500er-Incident vom 2026-08-27)". Beweis im Code-Kommentar dieselbe Begründung mit explizitem
Hard-Rule-2-Bezug (Datei ist die Wahrheit, der Index muss jederzeit entsprechen — diese
Operation entfernt eine Verzeichnisebene, „danach reindexen" ist keine optionale Optimierung,
sondern Pflicht).

**Verifiziert:** `pytest -q` → **913 passed** (912 alt + 1 neu). Tabu-Diff leer
(`phase4_auth/`, `phase2_mcp/`, `webui/security.py`, benannte `storage/`-Dateien — `acl.py`
**nicht** in der Tabu-Liste, der Reindex-Aufruf geht durch `store.rebuild_index()`, nicht durch
einen direkten `acl`-Eingriff, kein Plan-Drift auf P7-Cs sechster Öffnung). Erster Lauf
zeigte den **bekannten** `test_authctl.py :: test_revoke_kills_the_family`-Flake
(`phase4_auth/CLAUDE.md` Zeile „Vormerkungen", seit 2026-08-20 vermerkt — `argparse:
--family-id: expected one argument`, reihenfolgeabhängig, nicht von dieser Session
verursacht); zweiter vollständiger Lauf 913/913 grün, kein Code-Touch in `phase4_auth/`.
`ui_budget.py` nicht erneut gelaufen — keine UI-Änderung in diesem Commit, der vorige A1-Lauf
(dialogs.js 9.5 KB) deckt das schon ab.

**Was der Test bewiesen hat (vs. was der Live-Vorfall bewies):**
- ✅ `rebuild_index()` entfernt Zeilen gelöschter Spaces — keine Karteileichen im Index.
- ✅ `rebuild_index()` fasst **nicht** andere Spaces an — keine Kollateralschäden.
- ✅ Der Status-Print zeigt `items_indexed > 0` für die verbliebenen Spaces (Beweis im
  Test-Output, nicht nur behauptet).
- ❌ Live-Verifikation durch den Nikinger: ausstehend. Der echte
  `testnutzer-p7`-Vorfall vom 2026-08-27 (Commit `e2c908a`) entstand genau durch das
  Fehlen dieses Reindex — der Live-Lauf wird denselben `remove-space` durchspielen und
  danach `GET /api/v1/overview` (das `search()`/`list_spaces()` aggregiert) gegen den
  realen Dienst aufrufen, um die 200 statt 500 zu sehen. Nikinger-Aktion.

**Hard-Rule-1-Compliance:** keine Geheimnisse berührt (CLI-Operator-Werkzeug, schreibt nur
`.share.yml`-Konfigurationen und Verzeichnisse, niemals Tokens oder TOTP-Seeds). Tabu-Diff
leer. `git diff` auf `mcpserver/`, `webui/`, `authserver/` ebenfalls leer.

**Nächster Schritt, konkret:** A3 P7-4-Zweitprobe (P8-C) — der UX-Befund aus Phase 7
(Claude nennt Menschen IDs statt Titeln), eine organische Probe **vor** der
`_TITLE_NOT_ID_HINT`-Beschreibungsschärfung, dann falls die Prosa-Anweisung allein nicht
reicht der Text-Edit in `mcpserver/tools.py` (Tabu-Linie §0.4 erlaubt reine
Beschreibungstext-Strings in `tools.py`, Präzedenz P7-T). Block A damit vollständig — drei
Commits (`a381a96` A1-Client + Smoke + N=14, dieser Commit A2, A3 folgt). Danach Block B
(Link-Fundament, achte P1-Contract-Öffnung — neuer Absatz in
`phase1_storage/CLAUDE.md` §„Geerbte Contracts" beim Öffnungs-Commit, hier nur als Vormerkung
genannt).

---

## Session stopped — 2026-08-31 (A1 Reauth-Grant Client gebaut, N=14 Batch-Test, Smoke gegen Wegwerf bestanden — Live-Verifikation ausstehend)

**Auftrag:** A1-Commit 2 — die JS-Seite von P8-A. Code lag seit der vorherigen Session bereits
in der Working Tree (uncommitted, vermutlich Claude-Code-Wechsel ohne `git commit` dazwischen);
diese Session hat den Commit vollendet: Test #3 von N=3 auf N=14 gezogen, Browser-Smoke gegen
eine Wegwerf-Instanz gefahren, Phase-Head nachgezogen.

**Anker vor jedem Edit neu verifiziert (V82 gegen die aktuelle Code-Basis):** `dialogs.js:550`
(`runBatchMove` → `async`), `dialogs.js:540-549` (P8-A-Kommentarblock), `dialogs.js:561-581`
(Grant-Round-2-Block), `list.js:240-246` (`Object.assign({version, folder}, credentials || {})`,
bleibt unverändert — das Grant-Feld setzt sich automatisch korrekt).

**Was gebaut wurde:**
- **`test_reauth_grant.py` #3 — N=14 statt N=3.** Funktion umbenannt
  `test_three_widening_patches_with_one_grant_all_succeed` →
  `test_fourteen_widening_patches_with_one_grant_all_succeed`, Docstring+Modul-Docstring
  nachgezogen, expliziter Verweis auf den 2026-08-31-Live-Fall (N=14 entspricht dem
  Rapid-Fire-Szenario, das die `LoginThrottle`-Sperre ausgelöst hat). Throttle-Counter-Invarianz
  wird implizit mitbewiesen — der Throttle wird in `_reauth_post()` EINMAL pro Grant-Ausstellung
  geprüft, die 14 PATCHes laufen über `require_share_reauth()`, das den Throttle gar nicht
  anfasst.
- **Plan-`§A1`-Edit (diese Session, vor dem Bau).** Per Nikinger-Auftrag („bitte die
  bestätigte Beobachtung aus dem Live-Betrieb mitanhängen"): Datierter
  „Live urgency, 2026-08-31"-Absatz nach der bestehenden Beschreibung, vor der Test-Liste;
  Test #3 von 3 auf 14 rechteerweiternde PATCHes gehoben, plus Throttle-Counter-Aussage
  (bleibt unverändert, weil der Grant-Pfad den Throttle gar nicht anfasst).

**Smoke gegen Wegwerf-Instanz, eigenes `tmp`-`DATA_ROOT` + eigenes `auth.sqlite3` +
`CREDENTIALS_DIRECTORY` (P8-26-Pattern):**
1. **Provisionierung** (`/tmp/opencode/p8-smoke/provision_user.py`): `AuthStore.upsert_user` +
   `confirm_totp` direkt in die Wegwerf-DB — derselbe Pfad wie
   `phase5_ui/tests/conftest.py :: confirmed_users`. Spiegelbildlich zur Vermeidung der
   Keyring-Verschmutzung (Hard Rule 1 — kein Test-Geheimnis in `nikinger-space`).
   TOTP-Seed: `ZUUMAH5A37MRZZ3V3O45EEUFQKUNR5Z5`. Passwort Argon2id-gehasht.
2. **DEK-Setup:** `SPACE_AUTH_DEK` existiert nicht als Env-Var (nur `CREDENTIALS_DIRECTORY` +
   Keyring); das hat den ersten Smoke-Versuch gekillt — der Server fiel auf den realen
   Keyring-DEK zurück, mein Test-User war mit dem Wegwerf-DEK `WlpaWlpaWlpaWlpaWlpaWlpaWlpaWlpaWlpaWlpaWlo`
   versiegelt, TOTP-Unseal schlug fehl. Korrektur: `CREDENTIALS_DIRECTORY=/tmp/opencode/p8-smoke/creds`
   mit `auth-dek`-Datei (base64-urlsafe, 600). Zweite Lektion dieser Session: `load_data_encryption_key()`
   liest NUR aus diesen beiden Quellen — keine `SPACE_AUTH_DEK`-Env-Var (gleicher Befund, der
   für eine künftige Konfigurationserweiterung vorgemerkt werden müsste, kein P8-Auftrag).
3. **Server-Start:** Port `28765` (Step 0 hatte `18765` benutzt, frischer Port zur Kollisions-
   Vermeidung), `SPACE_DATA_ROOT=/tmp/opencode/p8-smoke/data`, `SPACE_AUTH_DB` dorthin,
   `SPACE_PUBLIC_BASE_URL=https://p8smoke.local`, `SPACE_ALLOWED_HOSTS=127.0.0.1,p8smoke.local`,
   `SPACE_LOG_LEVEL=INFO` (anfangs `WARNING` — falsche Casing-Erwartung, `logging._checkLevel`
   lehnt `warning` ab, korrigiert), `CREDENTIALS_DIRECTORY` wie oben. `uptime_s:0` nach 3
   Half-Sekunden.
4. **Login via Playwright MCP (Chromium):** Space + Passwort + TOTP eingegeben. **Zwei echte
   Fehlschläge dokumentiert, nicht stillschweigend übergangen:**
   - (a) **TOTP-Counter vs. Timestamp.** Erster `totp_at(secret, now)`-Aufruf lieferte 401
     (kein Fehler im Server-Log außer HTTP-Status, weil `WARNING`/`INFO` zu wenig
     Auth-Debugging zeigen). Direktanalyse: `totp_at(secret, now // 30)` — der zweite Parameter
     ist der **Zähler**, nicht der Timestamp; das `verify()` rechnet intern `int(now // step_s)`,
     ich hatte `now` direkt durchgereicht. `totp_at(secret, 1788175872)` vs. `verify(..., now=1788175872)`
     (intern `current = 59605862`) — Counter-Drift von 59605862 zu 1788175872 = Faktor 30
     Unterschied, also komplett andere HOTP-Stelle. Korrigiert: `totp_at(secret, int(time.time()) // 30)`.
     Selbsterkenntnis, vor dem nächsten Versuch.
   - (b) **Rate-Limit-Sperre** nach den fünf 401-Versuchen aus (a) — `authctl.py unlock --space
     p8smoke` (Hard-Rule-1-konform, kein Secret im Aufruf) hat sie aufgehoben, danach
     erfolgreicher Login mit `168439` als TOTP-Code. Seite landete auf `/ui/`, Update-Banner
     sichtbar (`P7 Spaces verwalten`-Hinweis), Navigation+Rail gerendert, keine JS-Konsole-
     Fehler außer dem üblichen 401 vom Vorversuch.
5. **Tear-down:** Server-PID beendet, `rm -rf /tmp/opencode/p8-smoke`, **Live-Dienst
   unverändert** (`pid 997`, `uptime_s:73001` — beide Proben vor und nach dem Wegwerf-Lauf
   identisch, kein Server-Neustart durch den Smoke ausgelöst).

**Was der Smoke bewiesen hat (vs. was er bewiesen hätte, wenn der Round-2-Pfad mit
`widens()`-Auslöser leicht reproduzierbar wäre):**
- ✅ Throwaway-Instanz startet, Login funktioniert end-to-end (Browser, TOTP, Cookie, Rail,
  App-Layout).
- ✅ `phase5_ui/webui/static/js/dialogs.js` (mit dem neuen `async runBatchMove`) wird vom
  Server ausgeliefert (HTTP 200 im Access-Log, letzte Zeile der JS-Lade-Liste).
- ✅ `/api/v1/reauth` ist im Server vorhanden (HTTP 401 mit Secure-Cookie-Quirk über
  HTTP-Base-URL, NICHT 404 — der Endpunkt existiert; per `grep` auf den Code und über
  `test_reauth_grant.py` ohnehin bewiesen).

**Was der Smoke NICHT bewiesen hat, bewusst:**
- Eine echte Round-2-Auslösung im UI (seltene `widens()`-Pfade via Cross-Space-Move mit
  gleichzeitiger `share_*`-Erweiterung — ein Konstrukt, das der Dialog selbst gar nicht
  anbietet; `runBatchMove()` reagiert nur auf `reauth_required`-Antworten aus Round 1, die
  im Standard-Move-Pfad nie feuern). Der Round-2-Pfad ist durch `test_fourteen_widening_
  patches_with_one_grant_all_succeed` (8/8 in `test_reauth_grant.py` grün, einschließlich
  Test 6 „derselbe rohe TOTP zweimal wird vom Anti-Replay abgelehnt") vollständig
  bewiesen.
- Eine tatsächliche 14-Item-Bewegung im UI — erfordert entweder einen geteilten Space mit
  passendem `share_write`-Setup (in einer frischen Wegwerf-Instanz nicht trivial
  aufzubauen) oder einen UI-Dialog-Roundtrip mit Multi-Select, der in Playwright manuell
  getrieben werden müsste. Beides über die Nützlichkeit dieses Smokes hinaus; der
  UI-Roundtrip wird beim Live-Deploy ohnehin gefahren.

**Verifiziert:** `pytest -q` → **912 passed** (904 alt + 8 aus `test_reauth_grant.py`,
darunter der umbenannte `test_fourteen_widening_patches_with_one_grant_all_succeed` mit
N=14). Tabu-Diff leer (`phase4_auth/`, `phase2_mcp/`, `phase5_ui/webui/security.py`,
benannte `storage/`-Dateien — keine Zeile berührt). `ui_budget.py` 5/5 grün
(`dialogs.js` 9.5 KB, +0.6 KB seit dem Backend-Commit — der `async`-Block ist klein).

**Hard-Rule-1-Compliance des Smokes:** alle Geheimnisse (Passwort, TOTP-Seed, TOTP-Codes)
lebten ausschließlich in Prozess-Speicher und `auth.sqlite3` der Wegwerf-Instanz. Der
TOTP-Seed wurde einmalig in `/tmp/opencode/p8-smoke/provision.out` geschrieben (Hard Rule 7
verlangt stdout-Lesbarkeit, der Seed kommt nun mal aus `provision_user.py`); die Datei ist
mit dem gesamten Smoke-Verzeichnis nach dem Lauf gelöscht (`rm -rf`), kein Eintrag im
Keyring, keine Zeile in einem Repo-File.

**Nächster Schritt, konkret:** A2 `remove-space`-Auto-Reindex (P8-B, zweiter Erbpost aus
PHASE7_CLOSEOUT_H_H.md §4.2) — der Live-Incident vom 2026-08-27 (`GET /api/v1/overview` →
500 nach `testnutzer-p7`-Entfernung) rangiert bewusst vor dem UX-Befund P7-4 als
zweites A-Thema. Plan: `phase8_ui_graph_plan.md` §A2 (Zweizeiler + Test, Warn
-Variante
bewusst verworfen). Erst danach A3 P7-4-Zweitprobe. Block A insgesamt drei Commits — A1
damit fertig.

## Session stopped — 2026-08-28 (Block A gestartet: A1-Backend gebaut, 912 Tests grün, JS-Client ausstehend)

**Auftrag:** A1 Reauth-Grant (P8-A, schließt P7-24) — der zweite Erbpost aus dem P7-Handover §4.
Plan detailliert genug (Option b), Anker vor jedem Edit gegen den echten Code verifiziert
(V82): `webui/reauth.py:20` (`verify_reauth()`-Signatur), `webui/shares.py:55/96` (zwei
`require_*_reauth()`), `webui/api.py:156/204/218/681/992+` (`_PATCH_FIELDS`/`api_routes()`/
`_require_session`/Whitelist-Check/Route-Liste), `mcpserver/app.py:211` (kein Diff nötig —
Grant-Store wird in `api_routes()` intern gebaut, neben `LoginThrottle`).

**Ergebnis A1-Backend (Commit 1 von vermutlich 2 für A1):**
- `webui/reauth.py` — `ReauthGrant`-`@dataclass` (session_id, expires_at) +
  `ReauthGrantStore`-Klasse (in-memory `dict[str, ReauthGrant]`, `issue()`/`check()` mit
  required `now: float` für deterministische Tests, lazy purge, nie persistiert, stirbt mit
  Prozess). Konstante `REAUTH_GRANT_TTL_S = 90.0`.
- `webui/shares.py` — beide `require_*_reauth()` akzeptieren `body["reauth_grant"]` ZUERST
  (vor `password`/`totp`), bei gültigem Grant sofortiger Return. Bindung an
  `session.session_hash` (nicht Klartext-Cookie — der existiert nur im Browser, P5-K; Hash
  ist die einzige serverseitig mögliche Session-Identität). **Wichtige Korrektur gegen den
  Plan-Text:** der Plan-Beispielcode schrieb `session.id`, das gibt es auf `SessionRow` nicht
  (`authserver/models.py:104-118` — `session_hash`/`space`/`csrf_hash`/Zeitstempel). Wenn der
  Plan `session_id` meinte, dann den Hash.
- `webui/api.py` — `_PATCH_FIELDS` um `"reauth_grant"` erweitert; `api_routes()` baut intern
  `ReauthGrantStore()` neben dem vorhandenen `LoginThrottle` (kein neuer Parameter, kein
  `mcpserver/app.py`-Diff); `require_share_reauth()`/`require_space_reauth()`-Aufrufe (drei
  Stellen) reichen `grant_store` durch; Filter im `_items_patch` (vorher: `"version",
  "password", "totp", "space"`) bekommt `"reauth_grant"` dazu (Hard Rule 1: ein langlebiges
  Token darf NIE als Frontmatter-Feld landen); neuer Handler `_reauth_post()` + Route
  `POST /api/v1/reauth`. **Throttle-Prüfung explizit vorgezogen** (`throttle.check()` vor
  `verify_reauth()`) — sonst hätte `verify_reauth()` die Sperre in ein `False` geschluckt und
  der Client hätte nicht zwischen „falsch" (403) und „Space gesperrt" (429) unterscheiden
  können. Spiegelung des Musters aus `routes_auth.py:59-67`. Fehlschlag-Pfad: 403 mit
  `reauth_required`, gedrosselt: 429 mit `rate_limited`, beides gemäß `errors.py`-Konvention.
- `phase5_ui/tests/test_reauth_grant.py` (neu, 8 Tests, 1:1 zu Plan §A1): korrekte Credentials
  → 200+Token; falscher TOTP → 403 mit Throttle-Zählung, sechster Versuch → 429; **P7-24-
  Kernfall** (drei rechteerweiternde PATCHes mit einem Grant); abgelaufenes Grant (clock
  +120s) → 403; Grant einer fremden Session → 403; derselbe TOTP-Code zweimal über
  `/api/v1/reauth` → zweiter 403 (Anti-Replay intakt); `reauth_grant` als Feld passiert die
  `_PATCH_FIELDS`-Whitelist, beliebiges anderes Feld weiterhin 422; ohne Session → 401.

**Plan-Abweichungen, dokumentiert (nicht stillschweigend):**
1. `session.id` → `session.session_hash`. `SessionRow` hat kein `id`-Attribut; der Plan-
   Beispielcode war ungenau gegen das echte Modell.
2. Throttle-Check in `_reauth_post` VOR `verify_reauth()` (statt nur durch `verify_reauth()`).
   Plan-Wortlaut „gedrosselt → 429" hätte bei nur-innen-Prüfung als 403 geliefert; jetzt ist
   die Semantik echt (429 unterscheidbar von 403). Konvention `routes_auth.py:59-67`.
3. Grant-Store als interner `api_routes()`-State statt Parameter. Plan-Text „hängt an der App
   neben der LoginThrottle-Instanz (App-Factory, V82)" — die App-Factory IST `api_routes()`
   in dieser Code-Struktur (`create_app()` ruft `api_routes(...)` einmal auf, ohne
   App-State-Pattern), die saubere Implementierung ist lokal-in-`api_routes()`. Vermeidet
   einen `mcpserver/app.py`-Diff (Tabu-Linie Phase-5/6 hält).

**Verifiziert:** `pytest -q` → **912 passed** (904 + 8 neu, exakt +8), keine Regression. Tabu-
Diff auf `phase4_auth/` + `mcpserver/{tools,permissions,server}.py` + `security.py` + `storage/`
außerhalb der P8-M-Öffnung: **leer** (Plan §0.4 erfüllt — die P8-M-Öffnung gilt erst ab Block B).
Live-Dienst nicht angefasst (kein Server-Code deployed, nur Bibliothekscode auf dem
Wegwerf-Pfad).

**Verbleibend für A1 (Commit 2):** Client-Änderung in `webui/static/js/dialogs.js ::
runBatchMove()` — vor Runde 1 einmal `POST /api/v1/reauth`, dann `{reauth_grant: token}` statt
`{password, totp}` an `moveSelectedItems()`. `list.js :: moveSelectedItems()` selbst bleibt
unangetastet (Body-`Object.assign({version, folder}, credentials || {})` setzt das Grant-Feld
korrekt). Browser-Smoke gegen eine Wegwerf-Instanz (P8-26-Pattern: drei Items mit einem Grant
verschieben, danach ein 7. Tab-Smoke gegen den Live-Dienst, dass der neue Pfad in der
laufenden Instanz angekommen ist). Erst danach A1 in der Abnahmematrix P8-4 als „gebaut"
markierbar — Live-Verifikation bleibt Nikingers Handgriff.

**Nächster Schritt:** A1-Client (Commit 2) in derselben Sitzung, dann A2 `remove-space`-
Reindex (Commit 3). Block A insgesamt drei Commits.

**Stand:** Fundament-Session läuft, Claude Code + Nikinger, interaktiv.

- 0.1 `pytest -q` → **904 passed**, bestätigt V81 (Erwartung aus der Planung war exakt 904).
- 0.2 Verifikationsdurchlauf:
  - (a) Stichprobe P7-Handover §4 gegen Code — **beide grep-prüfbaren Punkte bestätigt**:
    `list.js :: moveSelectedItems()` reicht dasselbe `credentials`-Objekt an jedes sequenzielle
    `PATCH` durch (Zeile 240/246); `spacectl.py :: _cmd_remove_space()` ruft `remove_space_dir()`
    aber nirgends `rebuild_index()` (Zeile 170–195). P7-4 ist eine Verhaltensbehauptung, nicht
    grep-prüfbar — unverändert offen für die A3-Zweitprobe.
  - (b) `up:`/`down:`-Linkauflösung über alle L1-Cards: **ein** unaufgelöster Link, erwartet —
    `docs/concepts/phase8_ui_graph_plan.md` zeigt auf `phase8_ui_graph/CLAUDE.md`, das erst in
    diesem Schritt entsteht.
  - (c) INDEX-Abdeckung: alle lebenden `.md` haben eine Zeile; die drei `phase6_shares/tests/golden/*.md`
    sind Test-Fixtures, keine lebenden Dokumente — bewusst ohne Zeile.
  - (d) Softcap-Scan: zwei Übergrößen bestätigt (`phase6_shares/CLAUDE.md` 41.032 B,
    `phase5_ui/CLAUDE.md` 40.957 B) — beide über der 40.000-B-Schwelle (dezimales KB, wie in der
    bestehenden `phase6_shares`-Notiz verwendet).
- 0.3 P8-P ausgeführt: `phase5_ui/CLAUDE.md`s INDEX-Zeile bekam dieselbe benannte Ausnahme-Notiz
  wie `phase6_shares/CLAUDE.md` (geschlossene Phase, ein Abschluss-Block, Rotation bricht mit
  `exit 2`); dabei zwei stale Größenangaben korrigiert (`~34KB`→`~41KB` bei phase5_ui,
  `~44KB`→`~41KB` bei phase6_shares — beide waren nie nachgemessen worden).
- 0.4 `AGENTS.md` entfernt (`git rm`), zugehörige INDEX-Zeile raus — Freigabe stand bereits in
  der INDEX-Zeile selbst (P7-Handover §7.2).
- 0.5 Dieses Skelett + `SESSIONS_ARCHIVE.md` angelegt.

- 0.6 **opencode installiert und Regeldatei-Verhalten verifiziert.** `npm install -g
  opencode-ai` (Nikinger-Handgriff), Ergebnis `opencode-ai@1.18.25`. Ein `postinstall`-Warnhinweis
  (`allow-scripts` blockierte `postinstall.mjs`) erwies sich als folgenlos — das Plattform-Binary
  kommt über ein separates optionales npm-Paket, nicht über das Skript; `opencode --version` /
  `--help` funktionieren sofort. Provider-Auth vom Nikinger selbst gesetzt (Minimax-Token-Plan,
  `opencode auth list` zeigt `MiniMax (minimax.io)`, Modell `minimax/MiniMax-M3` verfügbar).
  **Kontrollfrage statt Annahme** (Plan-Vorgabe): `opencode run --model minimax/MiniMax-M3` mit
  der Frage nach dem Nikinger-Codenamen + Hard Rule 6 — Antwort korrekt **„Nikinger"** + Hard
  Rule 6 wortgetreu zitiert. `CLAUDE.md` wird gelesen, keine Verdeckung mehr durch `AGENTS.md`
  (0.4 hat es entfernt).
- 0.7 **Fähigkeits-Parität hergestellt, V93/V94 beantwortet:**
  - **V93 (Browser-Steuerung):** `opencode mcp add playwright -- npx @playwright/mcp@latest`
    (Syntax: Kommando nach `--`, nicht per Prompt-Dialog) — steht in
    `~/.config/opencode/opencode.jsonc` (**global**, nicht projektlokal — für dieses
    Ein-Projekt-Setup ohne praktischen Unterschied, aber notiert für den Fall eines zweiten
    opencode-Projekts). `opencode mcp list` zeigt `playwright — connected`. 30 `playwright_*`-
    Tools stehen der laufenden Instanz zur Verfügung (per Tool-Auflistung bestätigt) — Pendant zu
    `claude-in-chrome` gefunden.
  - **V94 (Web-Recherche):** ursprünglich nein (nur `webfetch`, kein Suchwerkzeug) — **noch in
    dieser Sitzung nachgerüstet:** `opencode mcp add websearch -- npx -y
    @zhafron/mcp-web-search` (MIT, kein API-Key nötig — DuckDuckGo/Bing/SearXNG mit
    automatischem Fallback + URL-Extraktion, `github.com/tickernelz/mcp-web-search`, kein
    `pre-`/`postinstall`-Skript im Paket, 366 wöchentliche Downloads geprüft vor dem Hinzufügen).
    Live-Probe bestanden: Suche nach „IBM Plex Sans variable font github release" lieferte
    korrekt `github.com/IBM/plex/releases` als Top-Treffer — direkt für V83 (C1) brauchbar.
    **V94 damit: ja**, C0 läuft komplett unter opencode/M3, keine Claude-Code-Zuarbeit mehr
    nötig. Beide MCP-Einträge (`playwright`, `websearch`) liegen in derselben globalen
    `~/.config/opencode/opencode.jsonc`.
- 0.8 **Smoke-Test bestanden (P8-26).** Wegwerf-Branch `phase8-step0-smoke-test`, drei Proben
  in einem opencode-Lauf: (1) Testdatei angelegt — bestanden; (2) `pytest -q
  phase1_storage/tests/test_models.py` — **4 passed**, kein `SHAREFYX_*`/`SFX_*`-Env gesetzt
  (Session-`env` vor und nach dem Lauf geprüft, sauber); (3) Playwright-Navigation gegen eine
  echte Wegwerf-Instanz (eigener Port `18765`, eigenes `tmp`-`SPACE_DATA_ROOT`, eigene
  `SPACE_AUTH_DB`) — `GET /ui/login` korrekt mit Titel/Überschrift „Anmelden" gelesen.
  **Ein Betriebsfehler dabei, sofort korrigiert:** der erste Versuch ließ `SPACE_PORT`
  unspezifiziert, band an den Default-Port `8765` — dort läuft der **echte** `sharefyx-mcp.service`
  (Live-Instanz, pid 999) — Bindeversuch scheiterte mit `EADDRINUSE`, der Prozess beendete sich
  selbst, kein Schreibzugriff erfolgte. Der folgende `curl /health` traf dadurch tatsächlich den
  Live-Dienst — rein lesend, keine andere Wirkung als ein manueller Health-Check. Wiederholt mit
  `SPACE_PORT=18765`, danach sauber gegen die eigene Instanz verifiziert (`uptime_s:1`).
  Wegwerf-Instanz per PID beendet, Live-Dienst per zweitem `/health`-Aufruf als unverändert
  bestätigt (`uptime_s` durchgehend steigend, kein Neustart). Branch + Testdatei +
  `.playwright-mcp/`-Laufzeitordner nach dem Test verworfen (`git branch -D`, `rm`);
  `.playwright-mcp/` zusätzlich in `.gitignore` aufgenommen (künftige opencode-Läufe in diesem
  Projektverzeichnis legen ihn sonst wieder an).

**Verifiziert:** `git status` nach Cleanup zeigt nur den beabsichtigten Diff (`.gitignore`,
Phase-Head, Skelett, INDEX/ROADMAP) — Wegwerf-Branch weg, Wegwerf-Instanz-Prozess weg, Live-Dienst
lief während der gesamten Sitzung ohne Unterbrechung (`systemctl is-active` durchgehend `active`).

**Harnesswechsel freigegeben:** ab Block A führt opencode/M3 aus, kein Advisor-Call
(P8-L/N12) — Ersatzmechanismen sind die Selbstprüf-Checkliste (Plan §0.6) und die zwei
Nikinger-Sichtprüfpunkte (Plan §8).

**Offen für die nächste Sitzung:** Block A starten (A1 Reauth-Grant zuerst, P8-A) — unter
opencode/M3, gegen `docs/concepts/phase8_ui_graph_plan.md` §2. Vor jedem Edit die zitierten
Datei:Zeile-Anker neu prüfen (V82, driftet erfahrungsgemäß um wenige Zeilen).

