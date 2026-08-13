---
status: live
purpose: L3-Archiv der Phase-6-Session-Bloecke -- Steps 0-6 (Haushalt, Werkzeug-Ergonomie, Betrieb, Update-Log/Banner, Storage-Fundament, Rechtepolitik, Verwaltung/Migration + Live-Cutover), verbatim aus phase6_shares/CLAUDE.md verschoben
read-when: Historie einer bereits abgeschlossenen Phase-6-Teilarbeit nachvollziehen -- nicht beim normalen Sessionstart lesen
detail: L3
up: ../phase6_shares/CLAUDE.md
updated: 2026-08-13
---

# SESSIONS_ARCHIVE.md — Phase 6 (`phase6_shares/`)

> Erste Rotation (2026-08-10, Nikinger-Auftrag): drei Nachträge (Steps 0/1/2 — Haushalt,
> Werkzeug-Ergonomie, Betrieb) waren seit Step 3 „settled, nicht mehr Arbeitskontext", der Kopf
> lag nahe am 40KB-Softcap. Rotationslogik wie `phase4_auth/CLAUDE.md`s Steps-0–6a-Verschiebung.
> **Zweite Rotation (2026-08-12,** `scripts/rotate_session_block.sh phase6_shares`**):** Kopf
> erreichte erneut den Softcap (39 KB), diesmal über `scripts/rotate_session_block.sh` statt von
> Hand — der neue Block (Steps 1–3, s. u.) wurde mechanisch verschoben, Byte-Identität geprüft,
> nur sein Titel danach korrigiert (siehe Hinweis im Block selbst). Newest zuoberst wie sonst
> überall in diesem Repo.
> **Dritte Rotation (2026-08-12, derselbe Tag, Step-5-Commit):** Step 4 (Storage-Fundament)
> wandert verbatim herein, wieder mechanisch über dasselbe Skript, Byte-Identität geprüft.
> **Vierte Rotation (2026-08-13, Planungssession `ITEM_MOVE_PLAN.md`):** derselbe Auslöser wie
> beim zweiten Mal — der Kopf riss mit dem neuen Block den Softcap (40,2 KB). Step 6 samt seinen
> vier Nachträgen (Tool-Beschreibungen, Live-Cutover der Steps 4–6, Wortmarken-Version, UI-Fund
> „nur lesen" trotz Schreibrecht) wandert verbatim herein, wieder über dasselbe Skript,
> Byte-Identität geprüft. Enthält am Ende eine datierte Korrekturnotiz zum UI-Fund: dessen
> zweiter Teil ist inzwischen deployed und live bestätigt — sie steht bewusst hier an der
> Aussage, die sie korrigiert, der aktuelle Stand steht im Kopf.
> **Fünfte Rotation (2026-08-13, Step-7a-Commit):** Planungssession `ITEM_MOVE_PLAN.md` (vierter
> Block) wandert herein. Das Rotationsskript hatte den neuen sechsten Block zunächst fälschlich
> archiviert (Konvention: der neueste Block steht am **Ende** der Head-Datei, nicht am Anfang —
> beim Einfügen vertauscht), von Hand auf die richtige Zuordnung korrigiert, keine Byte-Änderung
> an den Blöcken selbst. Details: `phase6_shares/CLAUDE.md`, Session-Block „sechster".

## Session stopped — 2026-08-13, sechster — (Step 7a gebaut: Textfarben-Token)

**Auftrag:** Nikinger — Step 7a bauen (`ITEM_MOVE_PLAN.md` §3, vom vorigen Block als „sofort und
unabhängig lieferbar" benannt): vier Token-Zeilen plus eine Regel in `app.css`, eigener kleiner
Deploy samt `UPDATE_LOG.md`-Eintrag.

**Ergebnis: gebaut, noch nicht deployt.** `phase5_ui/webui/static/app.css` — gegen den echten
Code verifiziert (`--text-muted`/`--text-faint` standen exakt an der im Plan genannten Stelle,
`.input::placeholder` exakt an Zeile 187 wie in §3.1 vermerkt):
```
--text-muted:       #C4CDD8;   /* war #9AA6B4 */
--text-faint:       #A7B2BF;   /* war #64707E */
--text-placeholder: #7E8A98;   /* neu, nur .input::placeholder */
```
Kontrastwerte waren bereits in `ITEM_MOVE_PLAN.md` §3.1 durchgerechnet (vorige Session) —
diese Session hat sie nicht neu gemessen, nur die vier Zeilen umgesetzt.

**Sichtprobe (Pflicht laut §3.3 DoD), diese Session neu gebaut, kein Repo-Artefakt:** Server
(braucht Projekt-`.venv`) und Browser-Treiber (braucht nur `playwright`) sprechen über echtes
HTTP miteinander, kein gemeinsamer Prozess nötig. `~/.claude-code-tools/svg-venv` hatte bereits
einen gecachten Chromium (`~/.cache/ms-playwright`, für die SVG-Renderpipeline) — das
`playwright`-Paket testweise trotzdem zusätzlich ins Projekt-`.venv` installiert, um Server und
Treiber im selben Skript zu starten. **Advisor-Fund vor dem Commit:** das bricht die im Repo
bereits etablierte Trennung — `svg-venv` existiert genau dafür, damit Browser-Automatisierung
nicht in das `.venv` einsickert, aus dem `pytest`/`deploy.sh` laufen. Behoben: `playwright`/
`greenlet`/`pyee` wieder aus dem Projekt-`.venv` deinstalliert; das Screenshot-Skript startet den
Server weiterhin mit dem Projekt-`.venv` (echter `uvicorn`, echte `authserver`/`webui`-Module),
treibt den Browser aber mit `svg-venv`s Python — zwei Prozesse, zwei Umgebungen, eine
HTTP-Verbindung dazwischen.

Skript (`/tmp/.../scratchpad/ui_screenshot.py`, nicht Teil des Repos): temporäres `DATA_ROOT` +
temporäre `AuthStore`, alle vier Routengruppen inkl. `static_routes()` gemountet, echter
`uvicorn` auf `localhost` (nicht `127.0.0.1` — Chrome behandelt nur `localhost` als potenziell
vertrauenswürdig genug für das `Secure`-Cookie ohne TLS), Einladung+TOTP-Enrollment per `httpx`
vorbereitet, echter Login-Roundtrip durch das Browser-Formular. Ein Stolperstein unterwegs:
`http.cookiejar` (unter `httpx`) verweigert das Zurücksenden eines `Secure`-Cookies über eine
reine `http://`-Verbindung strikter als ein echter Browser — Cookie deshalb zwischen den beiden
`httpx`-Schritten manuell weitergereicht statt der Jar vertraut.

Drei Screenshots gesehen (`Read`, nicht nur behauptet): Login-Seite (Platzhalter „TOTP- oder
Recovery-Code" jetzt klar lesbar), Liste mit Ordner-Chips/Kennzahlen-Kacheln/„Zuletzt benutzt"
(Space-Navigation, Zähler, Versionsstempel „v1 · 2026-08-13" alle im kalibrierten Grau lesbar),
Editor mit Meta-Panel („Kopfdaten YAML-Frontmatter", Formatierleiste, Versionsband „v1",
„Zeile anhängen..."-Platzhalter). Alle drei DoD-Sichten aus §3.3 abgedeckt.

**`docs/UPDATE_LOG.md`:** eine neue `- `-Zeile unter dem bereits heute datierten
`## 2026-08-13`-Abschnitt (kein neuer Heading nötig, das Datum stimmt bereits) — deploy.sh-Gate
(P6-X) bleibt damit ohne Override erfüllbar.

**Deploy bewusst nicht in dieser Session ausgeführt:** `deploy.sh` braucht Sudo für den
Service-Neustart — außerhalb dessen, was Claude Code selbst kann (dieselbe Grenze wie beim
Steps-4–6-Cutover, `SESSIONS_ARCHIVE.md`, dort ausdrücklich „vom Nikinger ausgeführt"). Dieser
Prozess läuft auf der echten Produktions-VM (`systemctl status sharefyx-mcp` zeigt den echten,
aktiven Dienst mit echtem Traffic während dieser Session) — ein Redeploy ist eine Aktion mit
Wirkung auf ein geteiltes System (Fabian benutzt denselben Dienst), also Nikinger-Sache, nicht
automatisch von Claude Code auszulösen.

**Rotation in dieser Session ausgeführt, mit Korrektur:** `scripts/rotate_session_block.sh
phase6_shares` archiviert den Block mit dem **höchsten Zeilenindex** im Head als „neuesten" —
Konvention ist also: der aktuellste Block steht am **Ende** der Datei, nicht am Anfang. Der
sechste Block wurde zunächst versehentlich **vor** dem fünften eingefügt; das Skript hat
daraufhin den fünften (älteren) behalten und den sechsten ins Archiv verschoben — mechanisch
korrekt nach seiner eigenen Regel, nur mit vertauschter Eingabe. Von Hand korrigiert: der fünfte
Block liegt jetzt an seiner richtigen Archivposition (vor „Step 6, dritter", newest-first), der
Head trägt nur noch diesen sechsten Block. Kein Byte-Identitätsverlust — beide Blöcke wurden
unverändert verschoben, nur die Zuordnung war falsch.

**Verifiziert:** `pytest -q` **724 passed** (unverändert — P5-T: JS/CSS bleiben
unit-ungetestet, keine neuen Tests erwartet). `git status --short` zeigt ausschließlich
`app.css`, `docs/UPDATE_LOG.md`, `phase6_shares/CLAUDE.md`, `phase6_shares/ITEM_MOVE_PLAN.md`,
`phase6_shares/SESSIONS_ARCHIVE.md`, `docs/INDEX.md`. `.venv` selbst ist nicht versioniert —
der Playwright-Fund war deshalb nur über den Advisor-Durchlauf sichtbar, nicht über `git status`.
Tabu-Diff nicht relevant (P5-B betrifft `storage/`/`mcpserver/{tools,permissions,server}.py`,
nicht `webui/static/`). Advisor vor diesem Commit konsultiert — beide Funde (Zeitform der
Verifiziert-Zeile, `.venv`-Leck) in dieser Fassung des Blocks bereits behoben.

**Nachtrag, noch vor dem ersten Deploy — Nikinger-Feedback:** Wortmarke „sharefyx" + Versionsbadge
sollten weiß statt grau sein, Badge auf `v2.1`; zusätzlich **alle Versionsnummern aus den
Dateien** (`item.version`, überall wo die UI sie zeigt) ebenfalls weiß statt grau. Das ist eine
bewusste Umkehrung eines Teils der §3.2-Entscheidung von vorhin (dort ausdrücklich *gegen*
„alles auf `--text`" — Platzhalter-Verwechslungsgefahr, leises Versionsband) — Nikinger hat hier
gezielt nur die Versionsnummern selbst gemeint, nicht die Platzhalter/Begleittexte, und das ist
sein Ruf, nicht meiner; keine Rücksprache nötig, nur sauber umgesetzt.

Vier Fundstellen identifiziert (`grep` nach `item.version`/`.rail__version` in `app.js`/`app.css`,
nicht geraten): `.rail__brand`+`.rail__version` (Wortmarke, Badge — Badge-`opacity:.6` dabei
entfernt, sonst bliebe „weiß" nur ein gedämpftes Weiß und der Zweck der Änderung wäre verfehlt),
`.editor__version` und `.version-band__number` (beide zeigen nur Versionstext, direkte
Farbänderung reicht), `.recent-row__meta`/`ro-meta` (zeigen Version **und** Datum/Typ im selben
Element — hier eine neue Klasse `.version-num` eingeführt statt die ganze Zeile weiß zu machen,
damit nur die Zahl selbst hervortritt, Datum/Typ bleiben gedämpft; `recent-row__meta` dafür in
`app.js` von einem Text-Span auf zwei verschachtelte Kindknoten umgebaut, `ro-meta`s Version-Span
bekam nur eine zweite Klasse). `app.html`: `v2` → `v2.1`.

**Eine Inferenz über den wörtlichen Auftrag hinaus, benannt statt still gemacht:** `ro-meta` ist
die Nur-lesen-Ansicht eines **fremden** Items (geteilter Space) — „alle Versionsnummern aus den
Dateien" wortwörtlich genommen schließt das ein, aber es ist die einzige der vier Fundstellen, zu
der kein Grep-Treffer zwang, sondern eine Lesart. Mitgenommen, weil die Alternative (dieselbe
Versionszahl in der eigenen Ansicht weiß, in der fremden grau) inkonsistent gewirkt hätte — bei
Widerspruch ist das eine Korrektur wert, kein stiller Fakt.

**Sichtprobe wiederholt**, diesmal mit der aus dem ersten Advisor-Fund gezogenen Konsequenz sauber
umgesetzt statt nur nachträglich repariert: Server-Setup (`server_setup.py`, Projekt-`.venv`,
Import von `authserver`/`webui`/`storage`) startet `uvicorn` und ruft danach `svg-venv`s Python
als **separaten Subprozess** nur für `screenshot_client.py` (reines Playwright, kein
Projekt-Import) — beide Umgebungen bleiben getrennt, kein erneutes Pip-Install im Projekt-`.venv`.
Drei neue Screenshots gesehen: Wortmarke „SHAREFYX v2.1" weiß, „v1 · 2026-08-13" in der
Übersicht mit weißer Zahl und gedämpftem Datum, Editor-Header „v1 gespeichert" und die
Versionsband-Zahl „v1" beide weiß.

**Verifiziert (zweiter Teil):** `pytest -q` erneut **724 passed**, unverändert. `.venv` erneut auf
ein sauberes `pip show playwright` geprüft (leer) — diesmal von vornherein nie installiert, kein
Nachräumen nötig. `git status --short` zeigt ausschließlich `app.css`/`app.html`/`app.js`.

**Nachtrag, noch vor dem ersten Deploy — Nikinger-Weisung zum Update-Banner:** nur die
v2.1-Zeilen dieser Deploy-Ära sollen im Banner erscheinen, nicht die v2-Rückschau (Umstellung
live + beide Hotfixes) erneut. `docs/UPDATE_LOG.md :: parse_update_log()` zeigt im Banner **immer
nur `entries[0]`** — ein Eintrag ist ein `##`-Block, nicht eine Zeile. Der bestehende
`## 2026-08-13`-Block (7 Zeilen: 2 neue v2.1 + 5 alte v2) in **zwei** gleichdatierte Blöcke
gesplittet — die eigene Docstring-Doku in `updates.py` sieht das ausdrücklich vor
("disambiguiert zwei `## <selbes Datum>`-Blöcke"). Oben (neu, `id=2026-08-13#1`): nur die zwei
v2.1-Zeilen. Darunter (`id=2026-08-13#2`): die fünf v2-Zeilen unverändert, bleiben im
Vollständigen Log ("Update-Log ansehen") sichtbar, verschwinden nur aus dem Auto-Popup.
Nachgeprüft, nicht nur behauptet: `parse_update_log()` gegen die echte Datei ausgeführt,
`entries[0]` hat exakt die zwei neuen Zeilen.

**Eine ehrlich benannte Unsicherheit, kein stiller Fund:** die ID-Vergabe ist rein positionell
(erstes gleichdatiertes Heading in Dateireihenfolge = `#1`), nicht inhaltsbasiert. Falls der
Nikinger das Banner für den `92b918b`-Deploy (die fünf v2-Zeilen, damals ebenfalls unter
`2026-08-13#1`) bereits gesehen/weggeklickt hat, trägt `users.seen_update_id` bereits genau diese
ID — und die neuen v2.1-Zeilen erben jetzt dieselbe ID, weil sie ebenfalls zum ersten
gleichdatierten Block wurden. In diesem Fall poppt das Banner **nicht** automatisch neu auf,
obwohl der Inhalt neu ist; „Update-Log ansehen" zeigt es trotzdem korrekt. Kein Zugriff auf die
echte `auth.sqlite3` genommen, um das zu prüfen (Auto-Mode-Classifier blockierte den Pfadversuch,
zu Recht — das wäre ein Griff in echte Nutzerdaten ohne zwingenden Grund). Für den Nikinger:
falls das Banner nach dem Deploy nicht von selbst erscheint, ist das der Grund, kein neuer Bug.

**Nikinger-Klarstellung zum Versionsschema, für spätere Bumps:** Versionsnummern spiegeln
Deploy-Zyklen, nicht Phasen — jeder Deploy erhöht die Zahl, Schema `x.y.z` wie in klassischer
Software-Versionierung, **nicht** neu bei 1 anfangend (diese Ära zählt als Fortsetzung von v2,
daher `v2.1`, nächster Deploy `v2.2` usw.).

**Nächster Schritt (konkret):** Nikinger führt `deploy.sh main` aus (Sudo-Neustart), bestätigt
danach live in allen drei Ansichten (Login, Liste, Editor) — das ist §3.3s letzter DoD-Punkt,
jetzt inklusive der weißen Wortmarke/Versionen — **und** dass das Banner nur die v2.1-Zeilen
zeigt (mit der oben benannten Unsicherheit im Hinterkopf). Danach ist **Step 7a vollständig
geschlossen** und der einzige noch offene UI-Rest aus `ITEM_MOVE_PLAN.md` erledigt. **Step 7**
(UI Dateisystem) ist als eigener Plan freigegeben (`/home/savefyx/.claude/plans/
serialized-seeking-aurora.md`, Nikinger-Entscheidung: Rename-Funktion bleibt draußen, Aufbau in
Unterschritten mit Checkpoints) — Ausführung beginnt in derselben Session, sobald dieser Nachtrag
committet ist. **Step 7b** setzt Step 7 voraus. Gate-A→B-Punkt 3 unverändert offen (realer
Purge-Lauf, frühestens 2026-08-28).

## Session stopped — 2026-08-13, fünfter — (Planungssession: `ITEM_MOVE_PLAN.md`, keine Code-Änderung)

**Auftrag:** Nikinger — die Planungsvormerkung des vorigen Blocks zu einem ausführungsreifen Plan
ausbauen, **inklusive** der UI-Bedienung zum Verschieben (geteilte Spaces über die UI anlegen
ausdrücklich **nicht**, P6-V bleibt), plus ein gemeldeter Lesbarkeitsdefekt („der graue Text ist
nicht gut lesbar"). Ablage als persistente Notiz im Phasenverzeichnis mit semantischer Verknüpfung
zum Hauptplan. Reine Doku-Session — kein Code angefasst, `git diff` außerhalb `.md` leer.

**Ergebnis: `phase6_shares/ITEM_MOVE_PLAN.md` (neu, 27 KB).** Entscheidungen **P6-AD–P6-AJ**
(Fortsetzung der Hauptplan-Nummerierung, die bei P6-AC endet), drei unabhängig lieferbare
Schnitte — **Step 7a** (Textfarben, jederzeit lieferbar) · **Step 7** (unverändert, Hauptplan) ·
**Step 7b** (Cross-Space-Move, setzt Step 7 voraus) —, Abnahmezeilen **25–30**, `[VERIFY]`
**V52–V55**, Nebenbefunde **O6/O7**. Verknüpfung im Hauptplan an zwei Stellen (`down:`-Eintrag der
Header-Card + datierter Hinweiskasten direkt über Step 7); der 📕-Snapshot bleibt inhaltlich
unverändert — dieselbe Behandlung wie die Korrekturnotiz in `P2_ADAPTER_ABNAHME_2026-07-26.md`.

**Vier Korrekturen an der Planungsvormerkung des vorigen Blocks** (dort steht „geprüft und
bestätigt fehlend auf allen drei Schichten" — gegen den Code nachgeprüft ist das so nicht haltbar;
der alte Text bleibt im Archiv verbatim stehen, dies ist die datierte Ersetzung):
1. **`Store.update(folder=…)` verschiebt real** und ist seit Step 4 gebaut (`store.py:475-480`,
   `_write_item_file():285-286`). Probelauf gegen ein Wegwerf-`DATA_ROOT`: die Datei landet unter
   `niklas/projekte/alpha/…md`; Tiefe > 2 und reservierte Namen werfen `ValidationError`. Auch
   `mcpserver/tools.py :: update_item(folder=)` und `webui/api.py :: _items_patch` können es,
   beide mit dem Eigentümer-only-Riegel vom 2026-08-12.
2. **`Store.update(space=…)` scheitert laut, nicht still** — `space` steht in
   `_SYSTEM_MANAGED_FIELDS` (`store.py:43`), `ValidationError: Feld 'space' ist vom Store
   verwaltet`. Der „still als Extra-Feld"-Effekt existiert, betrifft aber nur echte Tippfehler
   (`spce=…`), nicht `space` — festgehalten als **O6**, und der Grund, warum `move()` eine
   benannte Signatur statt `**changes` bekommt.
3. **Die UI kennt keine echten Ordner.** `app.js :: renderFolders()` rendert die vier Buckets,
   nicht Verzeichnisse; `GET /api/v1/overview` liefert gar kein `folders`-Feld (nur
   `/api/v1/spaces` tut das, und den benutzt der Baum nicht). Der fehlende Verschieben-Knopf ist
   ein Symptom, nicht die Ursache.
4. **Menschen können nicht einmal in einen Ordner anlegen** — `_items_post`s Feld-Whitelist
   (`api.py:343`) kennt `folder` nicht, `create_item(folder=)` über MCP schon. Die Agentenfläche
   kann seit Step 5 etwas, das die Menschenfläche nicht kann; im Zusatzplan als K4 mitgeschnitten.

**Der Fund, der Step 7b klein macht:** `_write_item_file()` berechnet den Zielpfad aus
`item.space` **und** `item.folder` — es hat nur nie ein `Item` mit geändertem `space` gesehen.
Simuliert (Wegwerf-`DATA_ROOT`, `replace(item, space="fabian")` + der bestehende Pfad): Datei
liegt danach unter `fabian/`, Frontmatter-`space:` ist mitgezogen, `get()`/`acl_of()`/`search()`
konsistent, **ein** Git-Commit (`move itm_… [fabian]`) mit von Git erkanntem Rename
(`{niklas/alt => fabian}/…`). Der Storage-Anteil von Step 7b ist damit eine öffentliche Methode um
bereits funktionierende Mechanik, kein neuer Schreibpfad. Zweiter Nebenbefund aus denselben
Läufen: **O7** — leer gewordene Quellordner bleiben liegen und erscheinen weiter in
`list_spaces().folders` (reiner Verzeichnis-Walk), was der Baum aus Step 7 als Geisterordner
zeigen würde; Behandlung als P6-AF im Zusatzplan.

**Nikinger-Entscheidung dieser Session (Grautext, per Frage gestellt statt geraten):** gemessen
sind es zwei Token, nicht eines — `--text-muted` (#9AA6B4, 19 Stellen) besteht WCAG AA bereits
(6.6–7.9:1), `--text-faint` (#64707E, 16 Stellen) fällt mit **3.2–3.9:1** durch. Gewählt:
**kalibriert anheben** (`--text-muted` → `#C4CDD8`, `--text-faint` → `#A7B2BF`) **plus ein neues
`--text-placeholder` (#7E8A98)** für `.input::placeholder`. Die wörtliche Fassung „alles auf
`--text`" hätte leere Eingabefelder wie gefüllte aussehen lassen und das absichtlich leise
Versionsband (Designsystem §4.4) so laut wie den Titel gemacht. Umsetzung ist Step 7a, **noch
nicht gebaut**.

**UI-Fund aus dem vorigen Block vollständig geschlossen:** der `activeSpaceWritable()`-Fix (Teil 2)
ist deployed und vom Nikinger per **manuellem UI-Test im Browser** validiert. Read-only
gegengeprüft statt die Meldung übernommen: `/opt/sharefyx/current` → Release
`20260813T120925.743482Z`, Arbeitsstand `92b918b` — derselbe Commit, der den Fix enthält, und
identisch mit dem lokalen `main`-HEAD; `docs/UPDATE_LOG.md` trägt dafür einen echten, heute
datierten Eintrag („hotfixed Rechte für shared space"), das `deploy.sh`-Gate (P6-X) ist also
regulär gelaufen, nicht per Override. **Beide Teile des UI-Funds sind live bestätigt.**

**Rotation in dieser Session ausgeführt:** der Head hatte mit diesem Block 40,2 KB erreicht und
damit den 40-KB-Softcap gerissen. Der vorige Block (2026-08-12, dritter, mit vier Nachträgen)
ist über `scripts/rotate_session_block.sh phase6_shares` **verbatim** nach `SESSIONS_ARCHIVE.md`
gewandert — nicht von Hand, nicht abgetippt. Die dort eingefügte Korrekturnotiz zum
deployten UI-Fix ist mitgewandert und steht damit an der Aussage, die sie korrigiert.

**Verifiziert:** kein Code geändert, `pytest -q` trotzdem zweimal als Regressionsprobe gefahren →
**724 passed**, unverändert. `git status --short` zeigt ausschließlich `.md`-Dateien. Die Belege
dieser Session sind drei Probeläufe gegen Wegwerf-`DATA_ROOT`s im Scratchpad (nie gegen den echten
`DATA_ROOT`, Hard Rule) und ein selbst geschriebener WCAG-Kontrastrechner; alle Ergebnisse stehen
im Zusatzplan §1.3/§3.1, keiner davon ist ein Repo-Artefakt geworden. **Der Advisor war in dieser
Session nicht verfügbar** (nicht in der Tool-Liste) — statt eines Advisor-Durchlaufs wurde jede
Behauptung des Plans einzeln gegen den Code oder einen Probelauf gestellt; das ist ein Ersatz,
kein Gleichwertiger, und beim nächsten substanziellen Commit nachzuholen.

**Nächster Schritt (konkret):** `ITEM_MOVE_PLAN.md` vom Nikinger freigeben lassen — damit sind
P6-AD–P6-AJ gelockt. Danach ist **Step 7a** (vier CSS-Token-Zeilen + eine Regel in `app.css`)
sofort und unabhängig lieferbar und derzeit der einzige noch nicht deployte UI-Rest; ein eigener
kleiner Deploy dafür ist die realistische Form. **Step 7** (UI Dateisystem, `app.js`-Split,
Freigabedialog, Ordnerbaum) bleibt der nächste große Schnitt, **Step 7b** setzt ihn voraus.
Gate-A→B-Punkt 3 unverändert offen (realer Purge-Lauf, frühestens 2026-08-28).

---

## Session stopped — 2026-08-12, dritter — (Step 6 — Verwaltung und Migration, Block B)

**Auftrag:** Nikinger-Sonderauftrag zu Sessionbeginn — vor jedem Deploy des Sichtbarkeits-
Cutovers mindestens Step 6 bauen (`spacectl.py`/`migrate_visibility.py`), damit die Umstellung
mit richtigem Werkzeug statt einer von Hand editierten `.share.yml` landet. Plan §4 Step 6 war
bereits ausführungsreif (Dateiliste, Unterbefehle, Report-Format, DoD) — per Root-Prompt-Regel
("wenn der Plan detailliert genug ist, das feststellen und atomar entlang seiner Schritte
vorgehen") direkt umgesetzt, kein eigener Planungsdurchlauf nötig. Vor dem ersten Code
`advisor()` konsultiert (Auftrag: unaufgefordert vor substanzieller Arbeit).

**Advisor-Runde vor dem Bau, vier Punkte übernommen:**
1. **Kein `version`-Sprung in `migrate_visibility.py`.** Ursprüngliche Annahme dieser Session
   ("ein Versionssprung wäre vertretbar") war falsch — ein fehlendes `visibility`-Feld hat schon
   vor der Migration den Default `private` (`models.py :: DEFAULT_VISIBILITY`, Frontmatter-
   Vertrag §2.1), nichts Beobachtbares ändert sich. Ein Versionssprung hätte jeder laufenden
   Claude-Instanz mit einer gerade gelesenen `version` einen `ConflictError` untergeschoben, der
   keiner ist — am Tag des Cutovers, an dem Abnahmezeile 8 getestet wird. Bestimmt die gesamte
   Architektur des Skripts: es ruft deshalb nie `Store.update()` auf (das würde pro Item
   committen), sondern schreibt über `storage.files.atomic_write` direkt.
2. **Kein Index-Rebuild nach `--apply` nötig — geprüft, nicht angenommen.** `storage/index.py ::
   row_from_file()` gibt einem fehlenden `visibility`-Feld bereits denselben Default (`"private"`,
   `fields.get("visibility", "private")`) — Datei und Index sagen vor und nach dem Lauf für jedes
   Item dasselbe. Kein `store.rebuild_index()`-Aufruf im Skript.
3. **`STATE_DIRECTORY`-Konvention aus dem Plan ist wörtlich unpassend, sinngemäß richtig.**
   Gegengeprüft: `phase4_auth/systemd/sharefyx-mcp.service` setzt `SPACE_DATA_ROOT` über eine
   eigene, direkt gesetzte `Environment=`-Zeile — unabhängig von `StateDirectory=sharefyx` (das
   trägt nur die Auth-DB). Gemeint war die **Haltung** von `authctl.py :: resolve_db_path()`
   ("aus der Umgebung auflösen, kein stiller Fallback ins Arbeitsverzeichnis"), nicht die
   wörtliche Variable. `mcpserver.config.load_settings()` wäre wiederverwendbar gewesen, aber
   Advisor riet zu einer eigenen vierzeiligen `_resolve_data_root()` je Skript statt einer neuen
   `phase6_shares → phase2_mcp`-Importabhängigkeit für ein einzelnes Feld — kein bestehender
   Code-Pfad außerhalb von `phase2_mcp`/`phase4_auth` importiert `mcpserver.config` bisher
   (gegengeprüft per `grep`), diese Abhängigkeit wäre neu und unbegründet gewesen. Umgesetzt:
   `--data-root`-Flag hat Vorrang, sonst `SPACE_DATA_ROOT` (Pflicht), in beiden Skripten identisch.
4. **Lock einmal für den gesamten `--apply`-Lauf, nicht je Datei.** Ein Flock auf
   `<data_root>/.write.lock` (dieselbe Datei wie `Store._file_write_lock()`, hier eigenständig
   reimplementiert statt als neue `Store`-Fläche exportiert — dieselbe Zurückhaltung wie P6
   Step 5) wird für die komplette Migration bzw. jeden `spacectl.py`-Schreibbefehl gehalten. Ein
   über mehrere Locks interleaved halbmigrierter Zustand mit einem parallel schreibenden Dienst
   wäre schwerer zu erklären als ein kurzzeitig blockierter Dienst.

**`phase6_shares/scripts/migrate_visibility.py` (neu):** `scan()` liest jedes `*.md` unter jedem
Space (inkl. `_archive/` — archivierte Items brauchen `visibility` genauso), meldet nur Items
ohne das Feld. `apply()` schreibt `visibility: private` je gemeldetem Item über
`frontmatter.parse`/`serialize` + `files.atomic_write`, dann **ein** `history.commit()` je Space
(`migrate visibility [<space>]`) — nicht je Item, wie Plan §2.3 verlangt (200 Commits wären
Lärm). `history.ensure_repo()` wird defensiv selbst aufgerufen (nicht von einem vorherigen
`Store()`-Aufruf vorausgesetzt) — sonst würde `history.commit()` gegen ein Verzeichnis ohne
`.git` nur `logger.critical` loggen (nie fatal) und der geforderte Commit bliebe stillschweigend
aus. `--dry-run` ist Default; Report als JSON-Zeilen (`{"id":…,"space":…,"path":…,"before":null,
"after":"private"}`) plus eine Summenzeile (`items_migrated`, `spaces_touched`) auf stdout.

**`phase6_shares/scripts/spacectl.py` (neu):** sieben Unterbefehle. `create-space` legt nur ein
Verzeichnis an — **kein eigener Commit** (Git kennt keine leeren Verzeichnisse, der erste
Item-Write erzeugt den ersten echten Commit), **aber jeder schreibende Unterbefehl inklusive
`create-space` initialisiert über `_DataRootLock.__enter__()` beiläufig ein Git-Repo**
(`history.ensure_repo()`, idempotent — derselbe Aufruf, den `Store.__init__` bei jedem
Dienststart ohnehin macht), falls noch keins existiert. Bewusst genannt statt nur im Code
sichtbar: `create-space` gegen ein brandneues `DATA_ROOT` initialisiert damit Git als
Seiteneffekt, ohne selbst zu committen. `list-spaces`/`show` lesen über `Store`/`AclReader` (Wiederverwendung
statt zweiter Lesepfad). `add-member`/`remove-member` schreiben `<space>/.share.yml` direkt
(eigener, lauter YAML-Loader — anders als `AclReader`, der bei einem kaputten Bestand fail-closed
still eine leere `Grant` zurückgibt, soll ein Operator, der gerade eine Freigabe bearbeitet, einen
kaputten Bestand sofort sehen, nicht stillschweigend überschreiben); `write:` impliziert `read:`
(Plan §1.2.2) — `add-member --write` trägt den Namen deshalb nur in `write:` ein, keine Dopplung
in `read:`. `remove-member` entfernt aus beiden Listen (vollständiger Widerruf, kein Flag nötig)
und löscht die Datei ganz, wenn danach nichts Nennenswertes übrig bleibt (`.share.yml`s eigene
"leer = nicht vorhanden"-Disziplin, analog Frontmatter §2.1). `remove-space --force` löscht den
Verzeichnisbaum (`shutil.rmtree` + ein Commit) — **nicht** ohne `--force` (Trockenlauf-Default,
druckt nur eine Vorschau), warnt immer, dass Git-Historie/Backups den Inhalt trotzdem behalten
(Hard Rule 4/F2), und scannt **vor** dem Löschen alle `.share.yml` im Bestand auf verbleibende
Referenzen auf den zu löschenden Space (Advisor-Fund: sonst produziert `remove-space` selbst
genau die verwaisten Namen, die `check`/Abnahmezeile 24 später melden). `check` (neu, nicht im
Plan-Text benannt, aber von der Step-6-DoD verlangt — "`diagnose.sh` meldet keine verwaisten
Namen" kann nur berichten, was ein YAML-Parser ausgewertet hat, kein zweiter Parser in Bash,
§2.2/V51) meldet `orphan_count`/`broken_count` als JSON.

**`phase3_edge/scripts/diagnose.sh`, Prüfung 12 (neu):** liest `DATA_ROOT`/`VENV` aus
`local.env` (dasselbe Sourcing-Muster wie Prüfung 5), ruft `spacectl.py check --json` über den
venv-Python auf, wertet `orphan_count + broken_count` aus (`python -c` auf dem JSON-Strom,
dasselbe Muster wie `abnahme_run.sh` — kein `jq`, kein zweiter JSON-Parser im Repo). INFO/
WARNUNG-Kategorie wie Prüfung 9/11, kein Abbruchkriterium — DATA_ROOT ist unter dem Dienst
gesetzt, nicht unter der Bash-Session, ein fehlendes `local.env` ist kein Fehlerzustand für
dieses Skript. **Manuell simuliert, nicht nur `bash -n`:** ein Wegwerf-`DATA_ROOT` mit zwei
Spaces und einer Freigabe angelegt, den geteilten Space per `shutil.rmtree` entfernt, Block 12
Zeile für Zeile gegen dieses Szenario gefahren — `orphan_count: 1`, korrekt den entfernten
Namen benannt. Scratch-Verzeichnis danach entfernt.

**Tests, beide Dateien neu (`importlib.util.spec_from_file_location`-Ladepfad wie
`test_authctl.py`, Skripte liegen in keinem Python-Paket):** `test_spacectl.py` (20 Tests:
DATA_ROOT-Auflösung, create/list/show, add/remove-member inkl. write-impliziert-read und
Verwaisungswarnung, remove-space Dry-Run vs. `--force`, `check` sauber/verwaist/kaputt) +
`test_migrate_visibility.py` (8 Tests: Dry-Run-Default schreibt nichts, Report-Inhalt, Version
bleibt unverändert, bereits gesetztes `visibility` bleibt unangetastet, ein Commit je Space bei
mehreren Items, zwei Commits bei zwei Spaces, DATA_ROOT-Auflösung). Beide Dateien injizieren
`env` in `main()` (nie `os.environ` direkt) und filtern `SHAREFYX_*`/`SFX_*` vor dem Aufruf
(P5-Lehre, memory `feedback_test_harness_never_inherits_env` — hier ohne reale Wirkung, da
keines der Skripte `systemctl` aufruft, aber dieselbe Disziplin durchgehalten, nicht erst bei
Bedarf nachgerüstet).

**Zweite Advisor-Runde, nach dem ersten Entwurf, vor dem Commit — ein Fund übernommen:**
`_cmd_remove_member` prüfte anders als `_cmd_add_member` nie, ob der Ziel-Space überhaupt
existiert — bei einem Tippfehler im Space-Namen liefert `_load_share_file()` `{}` (Datei fehlt
ja tatsächlich), `removed` bleibt leer, das Skript druckt „war in keiner Liste" und `EXIT_OK`.
Harmlos im Ergebnis, aber aus dem falschen Grund: die „kein Schreibzugriff"-Eigenschaft hing an
einer leeren Liste, nicht an einer Prüfung — ein Operator, der `remove-member niklsa fabian`
tippt, bekommt eine fröhliche Erfolgsmeldung und glaubt, die Freigabe sei weg, obwohl nie ein
echter Space namens `niklsa` existierte. Behoben: derselbe `ABBRUCH`-Guard wie in `add-member`,
plus `test_remove_member_on_unknown_space_aborts_instead_of_false_success`. **20 statt 19 Tests
in `test_spacectl.py`, 28 statt 27 insgesamt** — Zahlen unten schon korrigiert, nicht als
spätere Drift stehen gelassen (die elf dokumentierten Instanzen dieser Drift-Kategorie in
`phase2_mcp/CLAUDE.md` waren Warnung genug).

**Verifiziert:** `pytest -q` (gesamtes Repo) → **722 passed** (694 + 20 + 8, keine Regression),
Zahl der beiden neuen Dateien per `pytest --collect-only -q` nachgezählt, nicht aus dem
Schreibprozess geschätzt. `git status --short` nach den Testläufen zeigt außerhalb der neuen
Dateien nur `phase6_shares/CLAUDE.md`/`docs/INDEX.md` (Doc-Update) und `phase3_edge/scripts/
diagnose.sh` — kein `storage/`/`mcpserver/`/`authserver/`-Touch, wie für einen reinen
Tooling-Step erwartet.

**Status:** Step 6 ist **gebaut und unit-verifiziert**, nicht live geprüft — insbesondere ist
`migrate_visibility.py --apply` bisher ausschließlich gegen `tmp_path`-Wegwerfverzeichnisse
gelaufen, nie gegen den echten `DATA_ROOT` (Hard Rule: kein Test gegen den echten `DATA_ROOT`
durch Claude Code). DoD hat einen Live-Anteil, der laut Root-Prompt Sache des Nikingers ist
(echter dritter Nutzer, echter `diagnose.sh`-Lauf gegen den realen `DATA_ROOT`) — dieselbe
Aufteilung wie bei Steps 4/5 ("noch nicht live geprüft, kein eigener Abnahmematrix-Punkt"). Kein
MCP-Tool/`storage`-Kern-Code geändert — reine neue Operator-Skripte plus eine
`diagnose.sh`-Prüfung, wie geplant.

**Nächster Schritt (konkret):** Sonderauftrag ("mindestens Step 6") ist erfüllt — Rückmeldung an
den Nikinger vor Fortsetzung. **Empfehlung für den ersten echten Lauf, bevor der
Sichtbarkeits-Cutover live geht:** `migrate_visibility.py --data-root <echter DATA_ROOT>`
(Default `--dry-run`) einmal gegen den realen Bestand laufen lassen, den JSON-Report durchsehen
(Anzahl migrierter Items plausibel? welche Spaces betroffen?), **erst danach** `--apply` — genau
der Grund, warum dieses Skript existiert statt einer von Hand editierten `.share.yml`. Falls
weiter im Plan: Step 7 (UI Dateisystem, `webui/shares.py`, `app.js`-Split, Freigabedialog +
Re-Auth) ist der nächste Schritt, deutlich größerer Umfang (JS ohne Unit-Tests laut
P5-Konvention, `[VERIFY]` V43/V50) — kein Selbstläufer aus dieser Session heraus.
Gate-A→B-Punkt-3-Erinnerung bleibt unverändert gültig (frühestens 2026-08-28).

**Nachtrag 2026-08-13, vor Step 7:** der Nikinger brachte zwei Betriebs-Reports einer
arbeitenden Claude-Instanz mit — vermeintlich kein Weg, `status`/`links` ohne `patch_item`/
`append_to_item` zu ändern. Geprüft statt übernommen: `update_item` konnte das schon seit P6
Step 1 (alle Felder unabhängig optional, `body` weglassen rührt den Body nicht an) — die
Instanz griff nur zu den zwei Tools, deren Namen „gezielt" suggerieren, weil deren
Beschreibung das nicht ausschloss. Kein Code-/Schema-Fix nötig, nur die drei
Tool-Descriptions in `mcpserver/tools.py` präzisiert (Details + Testlauf:
`phase2_mcp/CLAUDE.md`s Korrekturnotiz vom selben Datum). Kein eigener Plan-Step, kein
Einfluss auf Step 7.

**Nachtrag 2026-08-13, dritter — Steps 4-6 live deployed, Cutover vollzogen, ein neuer
Shared Space, ein UI-Fund und eine Planungsvormerkung:**

**Auftrag:** Nikinger-Entscheidung, direkt aus dem laufenden Betrieb heraus: „power right
through the deployment". Vorausgegangen war ein Nebenbefund beim Testen der Runbook-Kommandos
für Step 6 (siehe vorheriger Nachtrag-Kontext) — `spacectl.py show` löste einen Index-Rebuild
(Schema 0→2) auf dem echten Index gegen den ECHTEN `DATA_ROOT` aus, weil `Store.__init__` den
laufenden Prozess ja nicht neu startet. Read-only anhand von `journalctl` (Fenster vor/nach dem
Rebuild-Zeitstempel `13:18:34`) geprüft statt angenommen: der laufende Dienst (altes Release,
kein Neustart) blieb durchgehend `200` auf `/mcp/` und `/api/v1/overview` — die neuen Spalten
tragen `NOT NULL DEFAULT`, altes `index.py` referenziert sie nie. Kein Schaden, aber der Fund
zeigt: der Index ist ein geteilter Zustand zwischen jedem lokalen Checkout und dem laufenden
Prozess, nicht nur zwischen Releases.

**Blockierender Befund vor dem eigentlichen Deploy:** die neue `SharePolicy` (Step 5) verlangt
für fremden Lesezugriff einen expliziten `.share.yml`-Grant (`permissions.py:58-66`) — anders
als das alte, noch live laufende Modell, das jeden fremden Space immer lesbar ließ. Weder
`niklas/.share.yml` noch `fabian/.share.yml` existierten. Ein Deploy ohne Gegenmaßnahme hätte
den beiden einzigen echten Nutzern dieses Systems gegenseitig die Notizen entzogen — dem
Nikinger vor dem Deploy vorgelegt (nicht stillschweigend gelöst), er hat sich für „ja, gegenseitig
lesbar halten" entschieden.

**Deploy-Reihenfolge, als ein Skript statt zwei loser Befehlsblöcke gebaut** (Advisor-Fund vor
dem Handover: getrennte Blöcke hätten in beliebiger Reihenfolge ausgeführt werden können —
`deploy.sh`s eigenes Health-Gate prüft `/health`/`/ui/login`/`/api/v1/me`/`/mcp/`, nicht „kann
niklas fabians Space noch lesen", ein Deploy vor den Grants wäre also grün durchgelaufen und
hätte den Zugriffsverlust verdeckt): `spacectl.py add-member niklas fabian --read` +
`add-member fabian niklas --read`, **hartes Grep-Gate** auf beide `.share.yml`-Dateien, erst
danach `deploy.sh main`. Vom Nikinger ausgeführt (Sudo für den Neustart, außerhalb dessen, was
Claude Code selbst kann). `docs/UPDATE_LOG.md` bekam einen echten, datierten Eintrag (Punkt „Doc
✓" der eigenen Deploy-Konvention, P6-X) statt eines `SHAREFYX_ALLOW_STALE_UPDATELOG`-Overrides,
weil dies — anders als die kosmetische Wortmarken-Änderung vorher am selben Tag — eine reale,
nutzersichtbare Verhaltensänderung ist.

**Ergebnis: `main`@`d068d1c` live, Release `20260813T113025.931306Z`, 722/722 Tests im Release
grün, Health-Gate 3/3 grün.** Live-Verifikation **eine Richtung bestätigt, eine offen**: über
den echten MCP-Connector (beide OAuth-Clients des Nikingers, `sharefyx` und
`Phase_4_sharefyx_Niklas`, identische Ergebnisse) `list_spaces` → alle drei Spaces sichtbar,
`IT-Sekus-Projekt` korrekt `writable:true` mit beiden Mitgliedern; `get_item`/`search_items`
gegen `fabian` lieferten echten Inhalt, korrekt in `<untrusted_content space="fabian">`
gewrappt — Rule 4 hält nach dem Cutover. **fabian→niklas ungetestet** — kein Zugriff auf
Fabians Token/Connector in dieser Session, bleibt offen bis Fabian selbst prüft oder es
weitergemeldet wird.

**Neuer Shared Space `IT-Sekus-Projekt`** (kanonischer Firmen-Projektname, Nikinger-Wahl):
beide Principals `--write` (impliziert read, `acl.py:76`), für Nutzung/Testing gedacht, bewusst
getrennt von den beiden echten Notiz-Spaces angelegt, damit Konflikt-/Mehrbenutzer-Tests dort
keine echten Daten berühren können.

**UI-Fund, behoben (Nachtrag, selber Tag):** die Weboberfläche zeigte `IT-Sekus-Projekt` im
Baum/in der Übersicht als „nur lesen", obwohl der Space laut MCP `writable:true` ist. **Root
Cause:** `webui/api.py:271` / `serializers.py:111` berechneten für die Space-Liste
ausschließlich `"own": space.name == session.space` — kein `writable`-Äquivalent zum
MCP-`list_spaces`-Feld. `app.js:598`/`676` kannte deshalb nur `space.own` und badgte jeden
nicht-eigenen Space hart als „nur lesen", ganz gleich ob ein `.share.yml`-Write-Grant existiert.
Die **Item-Ebene** war davon nie betroffen — `api.py:359` (`_items_get`) berechnet `readonly`
bereits korrekt über `can_write_item_as_human()`; der Fehler saß ausschließlich in der
Space-Übersicht/im Baum. **Fix:** `space_to_json()` (`serializers.py:107`) bekommt einen
neuen Pflicht-Parameter `writable: bool`; beide Aufrufer in `api.py` (`_spaces()`, `_overview()`)
berechnen ihn über `permissions.can_write(session.space, ...)` — derselbe Aufruf, den
`tools.py :: list_spaces()` für den MCP-Weg schon nutzt (`tools.py:294`), jetzt spiegelbildlich
auf der REST-Seite. `app.js:598`/`676` lesen jetzt `space.writable` statt `space.own` für das
Badge; die Baum-/Übersicht-**Gruppierung** (eigener vs. verbundener Space) bleibt bewusst bei
`own` — das ist eine andere Frage als Schreibrecht. +2 Tests (`test_serializers.py`,
`test_api.py`), +2 Assertions (`test_overview.py`); 722→724 gesamt. Deployed (Release
`20260813T115528.897376Z`, `sha 17303f0`) — der Nikinger meldete danach live: Badge korrekt weg,
aber **innerhalb** des Spaces weiterhin „nur lesen" und der Anlegen-Knopf weiterhin versteckt.

**Zweiter Teil desselben Bugs, im selben Nachtrag behoben:** derselbe Fehler saß eine Ebene
tiefer, unabhängig vom eben gefixten Badge. `app.js`s `ownSpaceActive()` (`state.activeSpace ===
state.ownSpace`) steuerte acht Stellen — den Anlegen-Dialog, den „nur lesen"-Text in der
Liste, den Leerzustand-Text, den Absende-Guard des Anlegen-Formulars — und fragte dabei
ausschließlich „ist das mein Home-Space", nie das tatsächliche Schreibrecht. Der Badge-Fix
allein änderte daran nichts, weil er nur die Space-Liste betraf, nicht diese acht Stellen.
**Fix:** neue Funktion `activeSpaceWritable()` (`app.js`, sucht `state.activeSpace` in
`state.spaces` — derselben Liste, die der Badge-Fix jetzt korrekt mit `writable` befüllt —
und liest dessen `.writable`), alle acht `ownSpaceActive()`-Aufrufstellen umgestellt, die jetzt
tote Funktion `ownSpaceActive()` selbst entfernt (nicht stehen gelassen). Kein Python geändert,
keine neuen Backend-Tests nötig (`space.writable` selbst ist bereits über die Backend-Tests
oben abgedeckt) — stattdessen `node --check` (Syntax) und eine Vier-Fall-Simulation
(eigener/schreibbar-fremder/nur-lesbar-fremder/unbekannter Space) der reinen Funktionslogik
gegen erwartete Werte, weil P5-T JS bewusst unit-ungetestet lässt und ein echter
Browser-Durchlauf einen laufenden Server + eine echte Sitzung bräuchte (außerhalb dieser
Session). **Nicht** interaktiv im Browser geprüft — der Nikinger sollte das nach dem nächsten
Deploy live bestätigen, dieselbe Lücke wie beim ersten Teil des Fixes.

> **[2026-08-13 Nachtrag zu diesem Absatz, fünfte Session] Lücke geschlossen.** Der Fix ist
> deployed und vom Nikinger per **manuellem UI-Test im Browser** validiert — genau der Durchlauf,
> den diese Session nicht selbst fahren konnte. Beleg read-only gegengeprüft statt die Meldung
> übernommen: `/opt/sharefyx/current` zeigt auf Release `20260813T120925.743482Z`, dessen
> Arbeitsstand `92b918b` trägt — derselbe Commit, der den `activeSpaceWritable()`-Fix enthält,
> und identisch mit dem lokalen `main`-HEAD. `docs/UPDATE_LOG.md` trägt dafür einen echten,
> heute datierten Eintrag („hotfixed Rechte für shared space"), das `deploy.sh`-Gate (P6-X) ist
> also regulär gelaufen, nicht per Override. **Beide Teile des UI-Funds sind damit geschlossen
> und live bestätigt.**

**Planungsvormerkung für die nächste Session (Opus, Browser-Planung) — Item-Verschieben:**
bereits vor dem Deploy geprüft und bestätigt fehlend auf allen drei Schichten
(`storage/store.py :: update()` kennt kein `space`-Feld — ein unbekannter Schlüssel landet
sogar stillschweigend als beliebiges Extra-Frontmatter-Feld statt eines Fehlers, `webui/api.py`s
`_items_patch` kennt nur `folder` nicht `space`, `mcpserver/tools.py :: update_item` hat keinen
`space`-Parameter). Der Nikinger-Wunsch: eine Planungssession soll klären, wie Item-Verschieben
**zwischen** Ordnern UND Spaces zusammen mit dem bereits gebauten geschichteten Ordnermodell
(`files.py :: MAX_FOLDER_DEPTH`/`validate_folder()`, Step 4) aussehen soll. Stichpunkte, die die
Planung mitnehmen sollte, nicht mehr:
- **Zwei Fälle, ein Werkzeug oder zwei?** Verschieben innerhalb des eigenen Space (nur
  `folder` ändert sich, bereits gebaut) vs. Verschieben über Space-Grenzen (physische
  Dateiverschiebung, echter Cross-Space-Write) — letzteres kollidiert mit Hard Rule 4/P6-U und
  bräuchte einen Write-Grant im ZIEL-Space, nicht nur im Quell-Space.
- **Git-Historie — geprüft, nicht mehr offen:** `history.ensure_repo(data_root)`/
  `commit(data_root, message)` (`storage/history.py:30,60`) nehmen beide den gesamten
  `DATA_ROOT`, nicht einen Space-Pfad — **ein** Repo für alle Spaces, kein Cross-Repo-Problem.
  Ein Cross-Space-Move ist damit `git mv <alt> <neu>` + **ein** Commit, dieselbe Atomarität wie
  jeder andere Write heute. Vereinfacht die Planung gegenüber der ursprünglichen Annahme.
- **Index/ACL:** ein verschobenes Item braucht eine neue `AclDecision` (neuer Space, neuer
  Ordner, ggf. andere `.share.yml`-Grants) — Version hochzählen oder nicht, dieselbe Abwägung
  wie bei der Sichtbarkeits-Migration.
- **Item-ID bleibt stabil** (Entscheidung F aus P1, `itm_<8hex>` unveränderlich) — ein Move darf
  daran nichts ändern, nur Verzeichnis + Frontmatter-`space`/`folder`.
- Ausgangspunkt für die Planung: dieser Abschnitt hier, nicht neu von vorne suchen.

Diese vier Punkte (Cutover-Ergebnis, UI-Fund, neuer Space, Planungsvormerkung) sind reine
Live-Betriebs-/Doku-Arbeit dieser Session — kein Code geändert außer `docs/UPDATE_LOG.md`
(bereits im vorigen Nachtrag committet). `pytest` unverändert bei 722/722 (Release-interner Lauf
von `deploy.sh` ist der Beleg, kein separater Lauf hier nötig).

**Nachtrag 2026-08-13, zweiter — UI-Kleinigkeit „on the fly":** der Nikinger meldete direkt im
Anschluss, die Wortmarke oben links zeige keine Versionsnummer, mit Vorschlag (dieselbe
Schriftart, kleiner, Phase 6 = v2). Umgesetzt in `phase5_ui/webui/static/{app.html,app.css}`
(`.rail__version`-Span neben `.rail__brand`, erbt `font-family`, 9px/60% Deckkraft) — Details,
Begründung der Breakpoint-Interaktion und Testabdeckung stehen in `phase5_ui/CLAUDE.md`s
Korrekturnotiz vom selben Datum, nicht doppelt hier. Visuell gegengeprüft: Playwright/Chromium
headless gegen die echte `app.css` (Datei-URI, `link href` temporär auf einen absoluten Pfad
umgeschrieben, damit `file://` die Stylesheet-Referenz auflöst — Serverstart wäre für eine reine
CSS-Sichtprobe unverhältnismäßig gewesen), Screenshot zeigt „SHAREFYX ᵛ²" wie gewünscht, danach
verworfen (kein Repo-Artefakt). Reine `webui/static/`-Änderung, kein Python-Code — `pytest`
722/722 unverändert als Regressionsprobe, kein neuer Test (JS/CSS bleiben laut P5-T
unit-ungetestet).

## Session stopped — 2026-08-12 (Step 5 — Rechtepolitik, Block B)

**Auftrag:** Step 5 aus `docs/concepts/phase6_shares_plan.md` §4 — `SharePolicy`/`Surface`
ersetzen `OwnSpaceWritable`, jeder item-level Lese-/Schreibpfad in `mcpserver/tools.py` und
`webui/api.py` wechselt von `space_of()`+space-level `can_read`/`can_write` auf `acl_of()`+
`can_read_item`/`can_write_item`. Vorbereitung: Advisor-Review des Plans vor dem Bau, gefolgt
von einer expliziten Nikinger-Entscheidung zu einem Fund außerhalb des Plan-Texts (siehe unten).

**Advisor-Fund vor dem Build, dem Nikinger vorgelegt statt still entschieden:** `folder` ist
seit Step 4 agenten-setzbar (`store.py`s Kommentar an `update()`s `folder`-Zweig sagte das
bereits ausdrücklich). Ein `share_write`-Halter, der ein fremdes Item in einen Ordner mit
breiterer `.share.yml` verschiebt, hätte dessen effektive Sichtbarkeit erweitert, ohne dass
Step 7s `widens()`/Re-Auth-Gate das je sähe — dieses Gate existiert nur für den
Menschen/UI-Pfad, die Agentenfläche hat grundsätzlich keinen Re-Auth-Mechanismus. **Nikinger-
Entscheidung (AskUserQuestion, 2026-08-12):** ein Nicht-Eigentümer darf `folder` nie ändern,
dauerhaft, nicht nur bis Step 7. Umgesetzt in beiden Adaptern (`tools.py::update_item`,
`webui/api.py::_items_patch`), je ein `ValidationError`/`403 forbidden` **vor** dem Schreiben,
je ein Test (`test_share_write_cannot_move_item_to_a_different_folder` in beiden Test-Dateien).

**`storage/acl.py` + `store.py` — kleine, dokumentierte Erweiterung über Step 5s Dateiliste
hinaus** (P6-C erlaubt `storage/`-Touches in dieser Phase generell): `Store.__init__` baute
bisher einen privaten `AclReader` ohne Zugriffspunkt — der Plan verlangt "ein Handle, kein
zweiter" für `SharePolicy` und `Store`. `Store.acl_reader` (neue Property) gibt genau diese
Instanz zurück. `AclReader.grants_for_space()` (neu, dünner Wrapper um `grants_for_dir()` auf
der Space-Wurzel) und `AclReader.decision_for()` (neu — die Vereinigungslogik, die
`Store.acl_of()` vorher inline berechnete) sind die Basis für `SharePolicy`s space-level
`can_read`/`can_write` UND für die item-weise Filterung in `search_items`/`GET /api/v1/items`
(eine `AclDecision` je `ItemSummary`-Zeile aus einem bereits geladenen `store.search()`-Ergebnis,
kein zweiter Index-Roundtrip pro Treffer). `Store.acl_of()` delegiert jetzt an `decision_for()`
statt die Logik zu duplizieren. Reine Refaktorierung, kein Verhalten geändert — die drei
Charakterisierungs-Goldens liefen vor UND direkt nach dieser einen Änderung isoliert grün,
bevor der Rest des Steps begann (P6-D, gezielt statt erst am Ende geprüft).

**`mcpserver/permissions.py`:** `Surface(str, Enum)` (`AGENT`/`HUMAN`), `Permissions`-Protokoll
um `can_read_item`/`can_write_item` erweitert, `SharePolicy(acl: AclReader)` ersetzt
`OwnSpaceWritable` vollständig (nicht danebengestellt). **Ein Punkt, den der Plan-Text nicht
auflöst und der beim Bau auffiel:** P5-B erlaubt dem UI-Paket genau ein Symbol aus `mcpserver`
— der Plan sagt nur "das Symbol ändert sich zu `SharePolicy`", sagt aber nicht, wie der
REST-Adapter dann `surface=Surface.HUMAN` an `can_read_item` übergeben soll, ohne `Surface`
als zweites Symbol zu importieren. Gelöst über `SharePolicy.can_read_item_as_human()` — eine
`SharePolicy`-eigene Bequemlichkeitsmethode, nicht Teil des `Permissions`-Protokolls, die
`Surface.HUMAN` innerhalb von `mcpserver/permissions.py` kapselt. `test_webui_imports_exactly_
one_mcpserver_symbol` (`phase5_ui/tests/test_api.py`) hält das jetzt gegen `{"mcpserver.
permissions.SharePolicy"}` fest, nicht mehr gegen `OwnSpaceWritable`.

**`mcpserver/app.py`:** `own_space_writable = OwnSpaceWritable()` → `permissions =
SharePolicy(store.acl_reader)`, an `build_mcp()` und `api_routes()` unverändert durchgereicht
(kein Signaturbruch, wie vom Plan vorhergesagt).

**`mcpserver/tools.py`, alle sieben Tools:** `get_item`/`update_item`/`append_to_item`/
`patch_item` lösen ihre Rechte jetzt über `store.acl_of(item_id)` statt `store.space_of(item_id)`
auf. `get_item` hält die „eigen"-Frage bewusst in zwei Variablen (Advisor-Fund, siehe Planungs-
Session): `writable` (steuert `repair_drift`) ist nicht dasselbe wie „gehört der Space" (steuert
den `<untrusted_content>`-Wrap, P6-O — ein geteiltes, aber schreibbares Item bleibt trotzdem
gewrappt). `search_items` filtert jetzt item-weise über `can_read_item` statt space-weise über
`visible_spaces` (Pflicht, nicht Komfort — sonst würde ein einzeln freigegebenes Item entweder
seinen ganzen Ordner mit sichtbar machen oder space-weise verschwinden, je nachdem wie
vorgefiltert würde) und bekommt einen `folder`-Parameter. `list_spaces` zeigt jetzt `members`/
`folders` je Space und zieht `visibility: human`-Items aus den `item_count`-Zählern ab (P6-P
gilt wörtlich auch für diese Zähler, nicht nur für `search_items/total`). `create_item` bekommt
`space=`/`folder=` (P6-U: Ziel-Space per Default die eigene, ein anderer nur mit `write:` in
deren `.share.yml`). `update_item` bekommt `folder=` (mit dem Fail-Closed-Riegel von oben);
`visibility`/`share_read`/`share_write` bleiben verboten (P6-M, unverändert). Die generische
`PermissionDenied`-Fehlermeldung (`map_storage_error`) wurde umformuliert — sie deckt jetzt drei
Ursachen ab (fremder Space, ungeteiltes Item, `visibility: human`), die alte Formulierung
("ist nicht dein Space") wäre für den dritten Fall (eigener Space, aber `visibility: human`)
schlicht falsch gewesen.

**`webui/api.py` + `webui/serializers.py`:** dieselbe Umstellung mit `Surface.HUMAN` (über
`can_read_item_as_human()`, siehe oben). `_items_get` filtert item-weise (inkl. `folder`-Query-
Parameter); `_items_get_one`/`_items_patch`/`_items_append`/`_items_archive` auf `acl_of()`+
`can_write_item` umgestellt. `serializers.py`: `item_to_json`/`summary_to_json` bekommen
`folder`/`visibility`/`share_read`/`share_write`/`shared`; `readonly` wird weiterhin vom
Aufrufer übergeben (keine Store-Aufrufe in `serializers.py`), jetzt aber ACL-basiert statt
reiner Space-Identität. `search_to_json()` ist auf eine dünne Hülle um bereits fertige
Item-Dicts geschrumpft (die ACL-Auflösung braucht `store.acl_reader`, das gehört in `api.py`,
nicht in die reine Übersetzungsschicht). `space_to_json` bekommt `members`/`folders`.
**Bewusst nicht Teil dieses Steps** (Step 5s Dateiliste nennt sie nicht, gehören zu Steps 7/8):
`kind: own|shared|foreign` auf Spaces, `/api/v1/meta`s neue Felder, `/api/v1/items/{id}/share`,
`GET /api/v1/overview`s `human`-Zähler (bräuchte einen `Store.search(visibility=)`-Filter, den
es nicht gibt, oder einen Rohscan — `_overview()` bleibt unangetastet).

**Testfolge, mandatiert vom Plan (§4 Step 5, zwölf Pflichttests) plus der eine Fail-Closed-
Ergänzung:** elf der zwölf sind neu in `phase2_mcp/tests/test_tools.py`/`test_permissions.py`
gebaut (die zwölfte, `test_acl_of_does_not_read_the_item_file`, existierte schon seit Step 4 in
`phase1_storage/tests/test_store.py`). Mehrere bestehende Tests mussten auf die neuen Semantiken
umgeschrieben werden, nicht nur die Fixtures — das ist die eigentliche Substanz dieser Session,
kein Nebeneffekt: `OwnSpaceWritable` machte jeden fremden Space universell lesbar
(`readonly=True`, aber `200`); ohne Freigabe ist ein fremdes Item jetzt unsichtbar/`403`
(`test_get_item_from_foreign_space_without_share_is_forbidden` ersetzt das alte "immer
lesbar"-Verhalten, `test_spaces_omits_foreign_space_without_a_share` ebenso auf der REST-Seite).
Betroffen waren auch die beiden Isolationstests in `phase2_mcp/tests/test_app.py`
(`test_principal_isolation_under_concurrency`, `test_all_seven_tools_are_callable_over_http`) —
Ersterer bekam eine STRENGERE Zusicherung (fremder Space fehlt jetzt ganz, statt nur
`writable=False`), Letzterer eine `.share.yml`, weil er den fremden Lese-Pfad ausdrücklich
demonstriert. Dieselbe Anpassung war für `phase2_mcp/scripts/mcp_smoke.py` und
`phase5_ui/scripts/ui_smoke.py` nötig (beide seeden seit P2/P5 einen fremden Space, ohne den
wären ihre eigenen „fremd lesen"-Prüfungen ab jetzt am neuen Fail-Closed-Default gescheitert,
nicht an einem Bug) — beide Skripte demonstrieren den Lese-Pfad in einen geteilten Space
absichtlich, deshalb hier bewusst `read: [<eigener Space>]` gesetzt statt den Test zu entschärfen.

**Verifiziert:** `pytest -q` (gesamtes Repo) → **691 passed** (671 + 9 `test_tools.py` + 7
`test_permissions.py` + 2 `test_api.py` + 2 `test_serializers.py`, keine Regression sonst).
Charakterisierungs-Goldens liefen isoliert vor+direkt nach dem `storage/acl.py`/`store.py`-Schritt
grün (oben) UND am Ende erneut. `git status --short` zeigt ausschließlich `storage/`,
`mcpserver/`, `phase2_mcp/{scripts,tests}`, `phase5_ui/{scripts,tests,webui}` — kein
`authserver/`-Touch, wie erwartet (P6-C erlaubt `storage`/`mcpserver`/`tools.py`/
`permissions.py`, nicht `authserver`). **Real ausgeführt, nicht nur `pytest`** (`SHAREFYX_*`/
`SFX_*` aus der Umgebung entfernt, wie nach dem 52-Neustart-Vorfall Pflicht): `phase2_mcp/
scripts/mcp_smoke.py --json` (13/13 `ok:true`), `phase5_ui/scripts/ui_smoke.py --json` (12/12
`ok:true`), `phase5_ui/scripts/ui_budget.py --json` (alle Budgets `ok:true`, echte
220-Item-Messung, `all_within_budget:true`).

**Status:** Step 5 ist damit **gebaut**, DoD aus Plan §4 Step 5 erfüllt (zwölf Pflichttests +
Fail-Closed-Ergänzung grün, reale Skript-Läufe grün). Kein eigener Abnahmematrix-Punkt für
diesen Step — die Live-Prüfung kommt mit den nutzerseitig sichtbaren Steps 6/7 (Verwaltung/
Migration, UI), Zeilen 8–18 der Abnahmematrix.

**Nachtrag, 2026-08-12, zweiter — Advisor-Fund nach dem ersten Step-5-Commit, sofort behoben
statt als offener Befund liegen gelassen:** `can_write_item` hatte keinen `surface`-Parameter
und keine `visibility`-Prüfung (Plan §1.2.4s Snippet gibt ihr keinen) — ein `visibility:
human`-Item war damit für die Agentenfläche zwar unlesbar (`can_read_item` sperrte korrekt),
aber weiterhin voll beschreibbar über den eigenen Space-Token: `append_to_item`/`update_item`
erreichten `store.append()`/`update()` ungehindert, und ein Versionskonflikt hätte sogar
Version/Zeitstempel des angeblich „vollständig nicht existenten" Items (P6-P) in der
Fehlermeldung preisgegeben. Anders als der Folder-Fund oben war das kein Plan-Zweifelsfall,
sondern ein Widerspruch zum Plan-Text selbst — kein Anlass für eine Nikinger-Rückfrage, sofort
korrigiert: `can_write_item`/`Permissions`-Protokoll bekommen denselben `surface`-Parameter wie
`can_read_item` (dieselbe Sperre: `Surface.AGENT` + `visibility=="human"` ⇒ `False`), plus
`can_write_item_as_human()` als Zwilling zu `can_read_item_as_human()` (P5-B, kein zweiter
`mcpserver`-Import im REST-Adapter). Alle sechs `tools.py`-Aufrufstellen und alle fünf
`webui/api.py`-Aufrufstellen nachgezogen. Drei neue Tests
(`test_can_write_item_human_only_blocks_agent_surface_even_for_owner`/
`test_can_write_item_as_human_is_equivalent_to_explicit_human_surface` in
`test_permissions.py`, `test_human_only_item_cannot_be_written_on_agent_surface` in
`test_tools.py` — bewusst inklusive eines Versionskonflikt-Versuchs, um das Leck explizit
auszuschließen, nicht nur den einfachen Schreibversuch). **694 Tests gesamt** (691 + 3).
Charakterisierungs-Goldens und alle drei Live-Skripte erneut grün, nach dem Fix.

**Vier weitere Advisor-Funde, nicht blockierend, bewusst nicht hier gefixt — als Eingabe für
spätere Steps festgehalten statt stillschweigend verloren:**
1. **Diese Änderung kippt reales Verhalten schon vor Step 6.** Nichts im echten Betrieb trägt
   heute eine `.share.yml`/`share_read` — sobald `deploy.sh` diesen Stand ausliefert, sieht
   Fabian Niklas' Space in `/api/v1/spaces`/`/api/v1/items` nicht mehr (Abnahmezeile 8s
   Zielzustand, nur **vor** `migrate_visibility.py`, nicht danach). Der Step-3-Banner hat das
   angekündigt, ist also keine Überraschung — aber der Nikinger sollte den Deploy-Zeitpunkt
   bewusst wählen, nicht nur das „ob".
2. **Ein reiner Ordner-Share lässt den Space unauffindbar.** `can_read`/`visible_spaces` lesen
   nur die Space-Wurzel-`.share.yml` (`grants_for_space`). Ein Space, der nur über
   `space/ordner/.share.yml` geteilt ist, liefert über `search_items`/`GET /api/v1/items`
   durchaus Treffer (item-weise gefiltert), taucht aber nie in `/api/v1/spaces` auf — Step 7s
   Navigationsbaum baut genau darauf auf. Eingabe für Step 7, nicht hier zu lösen.
3. **`get_item` auf ein ungeteiltes fremdes Item liefert `write_denied` statt eines
   Existenz-neutralen Fehlers** — anders als Plan §1.7.3/Abnahmezeile 22 für Assets
   ("404, nicht 403, kein Existenzleck"). IDs sind 8 Hex-Zeichen, Enumeration ist unpraktikabel,
   aber die Asymmetrie ist jetzt ein erreichbarer Pfad (vorher totes `can_read`-Immer-True), kein
   bloßer Seam mehr — eine bewusste Entscheidung wert, nicht automatisch nachziehen.
4. **`acl_of()` liest `share_*` aus dem Index, nicht aus der Datei** (bewusst, index-only ist der
   ganze Sinn) — ein Mensch, der eine Freigabe von Hand aus dem Frontmatter entfernt, sieht sie
   im Index für ein Request-Fenster noch als aktiv, weil `acl_of()` bewusst vor jedem
   drift-reparierenden `get()` läuft. Plan-gedeckt, aber das Fenster gehört benannt, damit Step 6s
   `spacectl.py`/UI als der vorgesehene Weg verstanden wird, nicht nur als der bequeme.

**Nächster Schritt (konkret):** Step 6 (Verwaltung und Migration) — `phase6_shares/scripts/
spacectl.py` (neu, `create-space`/`list-spaces`/`add-member`/`remove-member`/`show`/
`remove-space`), `phase6_shares/scripts/migrate_visibility.py` (neu, `--dry-run` Default,
schreibt `visibility: private` in Bestandsdateien ohne das Feld), `phase3_edge/scripts/
diagnose.sh`-Erweiterung. DoD: ein geteilter Space existiert real, ein dritter Nutzer ist
angelegt, `diagnose.sh` meldet keine verwaisten Namen. Gate-A→B-Punkt-3-Erinnerung bleibt
gültig (frühestens 2026-08-28), unabhängig vom Baufortschritt hier.

---

## Session stopped — 2026-08-12 (Step 4 — Storage-Fundament, Block B)

**Nachtrag, 2026-08-12, elfter — Step 4 (Storage-Fundament) begonnen, Charakterisierung zuerst
(P6-D).** Vor dem Umbau: Advisor-Review des Ausführungsplans holte einen echten operativen Fund
zutage, der weder im Plan noch beim ersten Lesen auffiel — `Store.__init__` ruft `rebuild_index()`
nie auf, und `phase2_mcp/scripts/serve.py` (der reale Diensteinstieg) auch nicht; einziger
Aufrufer heute ist der manuelle `space_cli.py`-Befehl (per `grep -rn "rebuild_index"` bestätigt).
Ein `INDEX_SCHEMA_VERSION`-Sprung, der `index.connect()` beim nächsten echten Deploy zum
Verwerfen+Leer-Neuanlegen zwingt (wie heute schon bei Korruption), würde den Produktivindex leer
zurücklassen, bis jemand von Hand reindiziert — jeder `get()` würde bis dahin `ItemNotFound`
werfen. Wird beim eigentlichen `index.py`-Umbau geschlossen: `connect()` liefert künftig
`(conn, rebuilt: bool)`, `Store.__init__` ruft bei `rebuilt=True` sofort selbst
`self.rebuild_index()` — dieselbe „Index ist billig, Dateien sind die Wahrheit"-Logik aus Hard
Rule 2, nur diesmal auch tatsächlich verdrahtet.

**Charakterisierung gebaut:** `phase6_shares/tests/test_characterization.py` (neu) + drei Golden
Files unter `phase6_shares/tests/golden/` (`roundtrip_create.md`, `drift_repaired.md`,
`archived.md`), byte-verglichen. Vier Fälle, wie im Plan gefordert — die beiden reinen
Verhaltensfälle (`ConflictError.current`, die vier Commit-Messages `create|update|append|archive`)
laufen als direkte Assertions statt eigener Golden-Dateien, gleiche Testkategorie wie
`phase1_storage/tests/test_store.py` es für dieselben Fälle schon tut, kein eigener Dateiinhalt
zu vergleichen. Goldens einmalig gegen den unveränderten HEAD-Code erzeugt (Scratchpad-Skript,
nicht im Repo — gleiche Kategorie wie P5 Steps 10/11 und der jsdom-Durchlauf aus Step 3),
`generate_id()` und `now_fn` deterministisch gemacht (`monkeypatch`), sonst wäre jeder Lauf ein
anderes Golden. **Ein echter Stolperstein dabei:** die erste Capture-Runde benutzte einen
gemeinsamen ID-Zähler über alle vier Fälle hinweg (`itm_00000001`…`itm_00000004`) — die echten
pytest-Fixtures sind aber function-scoped, jeder Test bekommt seinen eigenen frischen Zähler bei
1. Golden gegen den echten Testlauf verglichen schlug prompt fehl (`itm_00000001` erwartet,
`itm_00000004` bekommen); zweite Capture-Runde mit einem frischen Zähler je Fall behoben. Zwei
echte, jetzt eingefrorene Warzen dokumentiert, nicht korrigiert: CRLF im Body bleibt beim
Schreiben roh erhalten (`atomic_write`s Textmodus übersetzt nur `\n`, unter POSIX ein No-Op),
`store.get().body` normalisiert es beim Lesen trotzdem auf `\n` (`read_text()` vs. `read_bytes()`
in `index.row_from_file`) — dieselbe Diskrepanz, die der Advisor vorab benannt hatte.
`slugify("Ümlaut Café")` würde `é` unverändert (klein) im Dateinamen belassen (`isalnum()` ist
Unicode-bewusst) — im Golden-Fall bewusst mit ASCII-Titel umgangen, um den Dateinamen
vorhersagbar zu halten; kein Fund, nur eine Beobachtung am Rand.

**Verifiziert:** `pytest -q` → **625 passed** (621 + 4 neue, exakt die vier
`test_characterization.py`-Fälle). Kein `storage/`-Produktivcode in diesem Commit angefasst — nur
Tests, Goldens, dieser Head. Das ist der P6-D-Ausgangspunkt: jeder künftige Diff in diesem Step
muss diese vier Goldens byte-identisch lassen, außer dort, wo der Plan `visibility`/`share_read`/
`share_write` ausdrücklich als Subjekt einer Änderung benennt (keiner der drei aktuellen Goldens
berührt diese Felder).

**Nachtrag, 2026-08-12, zwölfter — Step 4 (Storage-Fundament) fertig gebaut, in derselben Sitzung
fortgesetzt.** Reihenfolge wie angekündigt: `files.py` zuerst (liefert `RESERVED_DIR_NAMES`/
`MAX_FOLDER_DEPTH`/`validate_folder()`/`folder_from_path()`, `acl.py` braucht die Konstante),
dann `acl.py` (neu), `models.py`, `index.py`, zuletzt `store.py` — jeder Schritt einzeln gegen
`pytest` verifiziert, die drei Goldens aus dem letzten Nachtrag liefen nach jedem Schritt mit.

**`files.py`:** `item_path(..., folder="")`, `validate_folder()`, `folder_from_path()`. Ein
echter Fund beim ersten Testlauf: `slugify("_archive")` strippt das führende `_` (kein
`isalnum()`-Zeichen) und würde `"archive"` liefern — ein Reserviert-Check NACH dem Slugifizieren
hätte nie gegriffen. Behoben: der Check läuft auf dem rohen, nur lowercased Segment, vor dem
Slugifizieren.

**`storage/acl.py`** (neu): `Grant`/`AclDecision`/`AclReader`, `yaml.safe_load` direkt (kein
zweiter Loader nötig, V51 — PyYAML ist bereits Dependency, `frontmatter.py` benutzt es schon).
`RESERVED_DIR_NAMES`/`MAX_FOLDER_DEPTH` bewusst in `files.py` statt hier (dokumentierte kleine
Abweichung vom Plan-Snippet §1.2.3 — Ordnerpfad-Validierung ist schon dessen Job). Fail-closed
überall: kaputtes/nicht-Mapping-`.share.yml` → `logger.critical` + leere `Grant`, nie eine
Exception im Lesepfad. Cache `dict[(path,mtime,size)->Grant]`, `invalidate()` für Tests/
`spacectl.py`.

**`models.py`:** `VISIBILITY_VALUES`/`DEFAULT_VISIBILITY`, `Item`/`ItemSummary` bekommen `folder`/
`visibility`/`share_read`/`share_write`, `SpaceInfo` bekommt `members`/`folders`.

**`index.py`:** vier neue Spalten, `INDEX_SCHEMA_VERSION = 2` über `PRAGMA user_version` (V46
geschlossen). **Der eine Fund, der über den Plan-Text hinausging** (Advisor-Review vor der
Umsetzung): `Store.__init__` rief `rebuild_index()` nie auf, `serve.py` (der reale
Diensteinstieg) auch nicht — nur `space_cli.py` von Hand. Ein reiner Schema-Sprung hätte den
Produktivindex nach dem nächsten Deploy leer zurückgelassen, jeder `get()` hätte `ItemNotFound`
geworfen, bis jemand manuell reindiziert. Behoben: `index.connect()` liefert jetzt
`(conn, rebuilt: bool)`, `Store.__init__` ruft bei `rebuilt=True` selbst `self.rebuild_index()`.
Erfüllt tatsächlich Entscheidung **G** aus `phase1_storage/CLAUDE.md` (`rebuild_index()`
öffentlich **und beim Start**) — die zweite Hälfte stand dort schon immer, war aber nie
verdrahtet.

**`store.py`:** `acl_of(item_id)` (index-only wie `space_of()`), `create()`/`update()` mit
`folder`/`visibility`/`share_read`/`share_write`, `search(spaces=, folder=)`, `list_spaces()`
verzeichnis- UND indexbasiert mit `members`/`folders`. `_item_to_text` schreibt `visibility` nur
bei Abweichung vom Default, `share_read`/`share_write` nur wenn nicht leer — sonst hätte jedes
bestehende Item beim nächsten Write ein stilles `visibility: private` bekommen, obwohl das
`migrate_visibility.py`s Job ist (Step 6). **Ein echter Bug, von den eigenen Tests gefangen:**
`acl_of()` unionte `share_write` zuerst nicht in `read` — ein Item mit `share_write: [x]` aber
leerem `share_read` hätte einen Schreiber ohne Leserecht gehabt. `test_acl_of_unions_item_shares_
with_share_yml` schlug beim ersten Lauf fehl, Fix: „write impliziert read" gilt jetzt auch für
die Item-eigenen Freigaben, nicht nur für `.share.yml`.

**Verifiziert, mehrstufig:** `pytest -q` → **671 passed** (625 + 46 neue: 36 in `phase1_storage/`
+ 10 `test_acl.py` — die 36 schließen die zwei `validate_folder()`-Traversal-Tests aus dem
zweiten Advisor-Durchlauf mit ein, siehe unten). Die drei Charakterisierungs-Goldens liefen VOR
und NACH dem gesamten Umbau
byte-identisch grün (P6-D erfüllt). `git diff --stat` auf `phase2_mcp/mcpserver`,
`phase5_ui/webui`, `phase4_auth/authserver` blieb **leer** — Step 4 bleibt vollständig innerhalb
`storage/` (P6-C eingehalten). **Real ausgeführt, nicht nur `pytest`** (das jeden `tmp_path`
immer frisch auf Schema-Version 2 startet und den Rebuild-Fix nie geprüft hätte):
`phase2_mcp/scripts/mcp_smoke.py --json` (alle 12 Schritte `ok:true`), `phase5_ui/scripts/
ui_budget.py --json` (alle Budgets `ok:true`, `all_within_budget:true`, echte 220-Item-Messung),
`phase5_ui/scripts/ui_smoke.py --json` (alle 11 Schritte `ok:true`). `ui_budget.py`s Log zeigt
den Rebuild-Fix live: gegen ein brandneues Temp-`DATA_ROOT` genau die erwartete Zeile
(`Index ... hat Schema-Version 0 (erwartet 2) — wird verworfen und leer neu angelegt`), danach
lief der komplette Lauf sauber durch.

Contract-Erweiterung in `phase1_storage/CLAUDE.md` unter „Geerbte Contracts" dokumentiert
(Fortsetzung der P6-Step-1-Öffnung, nicht eine vierte — siehe dort), Modul-Status-Tabelle dort um
Zeile 10 ergänzt.

**Zweiter Advisor-Durchlauf, vor dem Commit — zwei echte Funde, ein benannter offener Punkt:**

1. **Behoben:** `_row_to_item()`/`acl_of()` übernahmen `row["folder"]` direkt aus dem Index statt
   es aus dem Pfad neu abzuleiten. Der Index ist reine Ableitung (Hard Rule 2/„ein Index-Fehler
   fasst nie eine Datei an", `phase1_storage/CLAUDE.md`) — ein veralteter/falscher Spaltenwert
   hätte beim nächsten `update()` über `_write_item_file`s Zielpfad-Berechnung die Datei bewegt.
   Nicht über `pytest` mit frischem `tmp_path` erreichbar (Index und Datei entstehen dort immer
   zusammen), aber real: ein altes Binary gegen einen v2-Index schreibt `folder=''` in jede
   Zeile, die es anfasst (15-Spalten-`INSERT` ohne die vier neuen Spalten) — ab Step 5, sobald
   ein Adapter `folder` überhaupt setzt, ein echter Rollback-Pfad. Fix: beide Methoden rufen
   jetzt `files.folder_from_path()` auf dem tatsächlichen Pfad — bei `acl_of()` weiterhin reine
   Pfad-Arithmetik, kein Datei-Lesezugriff, der „liest die Item-Datei nicht"-Vertrag bleibt
   stehen. Alle 669 Tests weiterhin grün, Goldens weiterhin byte-identisch.
2. **Gepinnt, nicht verändert:** `validate_folder("../x")` lehnt nicht ab, sondern liefert
   `"item/x"` (`slugify("..")` fällt auf den `"item"`-Fallback zurück, kein `..`-Segment
   überlebt) — kein echter Traversal (der Pfad bleibt immer unter `data_root/space`), aber eine
   stille Umbenennung statt eines Fehlers. Tiefere Versuche (`"../../etc"`) fallen über den
   Tiefen-Check, nicht über einen dedizierten Traversal-Check. Zwei neue Tests in
   `test_files.py` pinnen genau dieses Verhalten, statt es unbeobachtet zu lassen — `folder`
   wird ab Step 5 Agenten-Eingabe.
3. **Offener Punkt, nicht diese Phase's Aufgabe:** `_item_to_text`s „nur bei Abweichung vom
   Default schreiben"-Regel (siehe oben) heißt, dass eine explizit gesetzte
   `visibility: private` beim nächsten `update()` wieder aus der Datei verschwindet (Default wird
   nie geschrieben, auch nicht wenn er vorher explizit dastand). Funktional harmlos — fehlend und
   `private` sind für `_item_from_text`/`row_from_file` dasselbe — aber Abnahmezeile 8 sagt
   „jedes Item trägt `visibility`" und wird vom Nikinger live gelesen; P6-L sagt, die Migration
   (Step 6) schreibt das Feld. Zwei mögliche Auflösungen, beide bewusst nicht hier entschieden:
   entweder der Nikinger akzeptiert „fehlend == private" als Erfüllung von Zeile 8, oder
   `visibility` wird „sticky" (geschrieben, sobald es einmal in der Quelldatei stand) — dann aber
   zusammen mit `migrate_visibility.py` in Step 6, nicht isoliert hier (würde sonst die drei
   Goldens aus diesem Step erneut anfassen). Kommentar sitzt zusätzlich direkt am betroffenen Test
   (`test_create_defaults_visibility_and_share_fields_and_omits_them_from_file`).

**Nachtrag, 2026-08-12, dreizehnter — Punkt 3 entschieden, Nikinger-Bestätigung.** „Fehlend ==
`private`" erfüllt Abnahmezeile 8 — **kein Sticky-Write**, keine Änderung an `_item_to_text`
nötig. Begründung, vom Nikinger nach Abwägung bestätigt: der Wert ist zur Laufzeit nie
mehrdeutig (`fields.get("visibility", DEFAULT_VISIBILITY)` ist derselbe Codepfad, ob das Feld
in der Datei steht oder nicht — ACL-Auflösung, `visibility: human`-Agentensperre (P6-P) und
API/UI-Anzeige unterscheiden „fehlt" nie von „explizit `private`"), und das Muster deckt sich mit
der bereits gelockten Konvention für `share_read`/`share_write` (§2.1: „leer = nicht vorhanden") —
`visibility` anders zu behandeln wäre die Inkonsistenz, nicht die Konsistenz. Einzige Konsequenz:
Abnahmezeile 8 wird künftig über `get_item`/die API gelesen (löst zu `private` auf), nicht über
ein rohes `grep visibility:` auf der `.md`-Datei — steht jetzt hier, damit es bei der Step-6-
Abnahme nicht überrascht. Punkt damit **geschlossen**, keine offene Aufgabe mehr für Step 6.

**Status:** Step 4 ist damit **gebaut**, DoD aus Plan §4 Step 4 erfüllt (Charakterisierung grün +
Contract dokumentiert). Kein eigener Abnahmematrix-Punkt für diesen Step — die Live-Prüfung
kommt erst mit den nutzerseitig sichtbaren Steps 5–7 (Rechtepolitik, Verwaltung/Migration, UI).

**Nächster Schritt (konkret):** Step 5 (Rechtepolitik) — `mcpserver/permissions.py`
(`SharePolicy`, `Surface`, `OwnSpaceWritable` entfernen), `mcpserver/tools.py` (alle Lese-/
Schreibpfade auf `acl_of()`/`can_read_item`/`can_write_item` umstellen, `search_items` filtert
`visibility: human` inkl. `total`), `mcpserver/app.py` (`AclReader` einmal bauen, mit `Store`
teilen), `webui/api.py`/`webui/serializers.py` (dasselbe mit `Surface.HUMAN`). Das ist der erste
Step, der `mcpserver`/`webui` tatsächlich anfasst — Gate-A→B-Punkt-3-Erinnerung bleibt gültig
(frühestens 2026-08-28, siehe oben), unabhängig vom Baufortschritt hier.

---

## Session stopped — 2026-08-09 bis 2026-08-12 (Steps 1–3 — Werkzeug-Ergonomie, Betrieb, Update-Log/Banner)

**Umbenannt bei der Rotation vom 2026-08-12** (dieser Block trug beim Verschieben noch den Titel
des allerersten Session-Blocks, „Step 0" — inhaltlich beginnt er aber mit der Steps-0–2-
Kurzfassung und geht dann vollständig in Steps 1–3 über; Titel korrigiert, damit er sich vom
darunterliegenden, tatsächlichen Step-0-Eintrag unterscheidet. Reiner Titel-Fix, kein Satz Prosa
darunter verändert.)

**Steps 0–2 (Haushalt/Verifikation, Werkzeug-Ergonomie, Betrieb) sind komprimiert und nach
`SESSIONS_ARCHIVE.md` verschoben** (2026-08-10, Nikinger-Auftrag) — dieselbe Rotationslogik wie
`phase4_auth/CLAUDE.md`s Steps-0–6a-Verschiebung: verbatim per `sed -n`, Byte-Identität vor dem
Löschen geprüft, nicht neu zusammengefasst. Die Modul-Status-Tabelle oben bleibt vollständig;
nur die Prosa darunter ist gewandert. **Kurzfassung des Archivierten:** Step 0 verifizierte den
P5-Übergabestand (576/576, V39–V41 geschlossen) und dokumentierte drei Regeländerungen (§0.7
a/b/c, u. a. Hard Rule 4 neu gefasst). Step 1 baute `patch_item` (`storage/patch.py`,
`mcpserver/receipts.py`, Quittungen statt Volltext an allen Schreib-Tools, V48 empirisch
geschlossen). Step 2 schloss O2 (`purge_expired()` räumt `token_families`/`clients` ab) und
ergänzte Client-Surface-Logging (`ua`-Feld, V42), `diagnose.sh` Prüfung 11, `ui_budget.py`s
Latenzmessung — Status blieb „gebaut, Live-Teile beim Nikinger" (V42, Gate-A→B-Punkt 3), beide
inzwischen in Steps 3s eigenen Nachträgen weitergeführt (siehe unten).


**Nachtrag, 2026-08-09, sechster — Step 3 (Update-Log und Banner) fertig, in derselben Sitzung
fortgesetzt.** Advisor-Review **vor** der Umsetzung eingeholt (Auftrag: „letzten machbaren Step
zu Ende bringen, Rest als Kommandos für den Nikinger"), vier Punkte daraus direkt übernommen,
nicht erst am Ende nachgezogen.

**Schema 3** (`authserver/store.py`): `users.seen_update_id TEXT`, additiv — anders als V1→V2
(nur neue Tabellen) muss diese Migration eine **bereits gefüllte** Tabelle erweitern; SQLite
kennt für `ALTER TABLE ADD COLUMN` kein `IF NOT EXISTS`, `_apply_schema_v3()` prüft deshalb
`PRAGMA table_info()` selbst. `SCHEMA_VERSION` → `"3"`. Zwei neue Methoden
(`get_seen_update_id`/`set_seen_update_id`), bewusst **nicht** als `UserRow`-Feld (Advisor-Fund:
`authctl.py`/`userdir.py`/`import_users_to_db.py` konsumieren `UserRow`, keines braucht diesen
Zustand). Drei bestehende Tests hätten sonst mit der falschen `schema_version`-Zahl weiter
gegrünt (`"2"` statt `"3"`) — beim ersten `pytest`-Lauf gefunden und korrigiert, nicht vom
Advisor: `test_schema_is_created_and_versioned`, die V1→V2-Migrationsprobe (endet nach Schema 3
zwangsläufig bei `"3"`, nicht `"2"`) und die dedizierte Versionsprobe selbst (umbenannt zu
`test_schema_version_is_three_after_initialise`). +3 Tests in `test_authserver_store.py`
(258→261): der v2→v3-Migrationstest (gleiches Muster wie der bestehende v1→v2-Test — Schema 2
von Hand gebaut, über `AuthStore` geöffnet, Spalte + Version geprüft) und zwei
`seen_update_id`-Roundtrip-Tests.

**`webui/updates.py`** (neu): `parse_update_log()`/`UpdateEntry`/`load_update_log()`. Strikt nach
Plan §2.4: `## <ISO-Datum>` beginnt einen Eintrag, `- ` eine Zeile, alles andere wird ignoriert.
ID = `"<Datum>#<n>"`, `n` zählt Wiederholungen desselben Datums in Dateireihenfolge (disambiguiert
zwei `## <selbes Datum>`-Blöcke). **Reihenfolge = Dateireihenfolge, nicht sortiert** — neue
Einträge werden oben eingefügt wie ein Changelog, `entries[0]` ist der neueste; das ist die
Prämisse, auf der sowohl `deploy.sh`s Gate („oberste Überschrift") als auch `api.py`s `latest_id`
aufbauen. `load_update_log()` fail-soft (fehlende/kaputte Datei ⇒ leere Liste ⇒ kein Banner, nie
ein 500) — kein Markdown-Rendering hier, das macht `app.js` mit dem vorhandenen Sanitizer (Hard
Rule 7 sinngemäß: der Server bleibt dumm, auch bei einem Log-Parser). +7 Tests
(`phase6_shares/tests/test_updates.py`, neue Datei — reine Funktionstests, kein Store, gleiche
Kategorie wie `test_patch.py`).

**`webui/api.py`**: `GET /api/v1/updates` (Einträge + `latest_id` + `seen_update_id` der
Sitzung), `POST /api/v1/updates/seen` (schreibt den **serverseitig berechneten** `latest_id`, nie
eine vom Client geschickte ID — Advisor-Vorgabe: unnötige Validierungsfläche und ein
Stale-Client-Rennen sonst umsonst). `api_routes()` bekommt dafür einen fünften Parameter,
`auth_store: AuthStore` — der gesehen-Zustand lebt in der Auth-SQLite, nicht im `storage`-Kern.
**Dokumentierte Ein-Zeilen-Abweichung** von Step 3s Plan-Dateiliste (nennt nur `webui/api.py`,
nicht `mcpserver/app.py`): `create_app()` muss den neuen Parameter durchreichen (`oauth.store`,
dieselbe Instanz wie `account_routes()`, kein zweiter DB-Handle) — acht weitere direkte
`api_routes(...)`-Aufrufer (`conftest.py` × 1, `test_api.py` × 3, `test_overview.py` × 1,
`ui_budget.py` × 2, `ui_smoke.py` × 1) mussten denselben fünften Parameter nachziehen. Per
`grep -rn "api_routes("` **vollständig** gefunden, nicht stichprobenartig — die ersten beiden
`pytest`-Läufe fingen nur die Testdateien ab; `ui_budget.py --json` real ausgeführt deckte den
gemockten Suite-Blindspot (Skripte laufen nie unter `pytest`) auf, `TypeError: api_routes()
missing 1 required positional argument`.

**`webui/static/js/updates.js`** (neu): `window.SharefyxUpdates.init({api, toast})`, injiziert
von `app.js`s `initShell()` an dessen eigenem Ende. **Muss vor `app.js` geladen werden**
(`app.html`, beide `defer`) — `updates.js` ruft `app.js`s globale `markdownToHtml()`/
`sanitizeHtml()` (Top-Level-Funktionen, kein IIFE, deshalb window-Properties trotz `"use
strict"`), umgekehrt bräuchte `app.js` sonst einen noch nicht existierenden
`window.SharefyxUpdates`. Advisor-Fund **vor** der Umsetzung, sonst hätte ein stiller No-Op das
Banner nie gezeigt, `pytest` bliebe grün (JS bleibt laut Plan unit-ungetestet, P5) — der
Nikinger hätte es im Browser gefunden, nicht die Suite.

**Node/jsdom-Simulation** (Scratchpad, nicht im Repo, gleiche Kategorie wie P5 Step 10/11):
erster Versuch mit `window.eval(appJs)` + `window.eval(updatesJs)` warf fälschlich
`ReferenceError: markdownToHtml is not defined` — **echter Befund über die Testmethode, kein
Bug im Code:** Strict-Mode-Direct-`eval()` isoliert Top-Level-Deklarationen von der aufrufenden
Umgebung (ECMAScript-Spezialfall genau für `eval()`), ein reales `<script defer>`-Tag tut das
nicht. Zweiter Versuch mit echten, ins DOM eingehängten `<script>`-Elementen (treue
Nachbildung von `<script src=... defer>`) lief sauber durch: Banner erscheint mit gerendertem
Markdown (`**Eintrag**` → `<strong>`), setzt `body.has-update-banner`, „Verstanden" versteckt
es und postet `/updates/seen`, „Update-Log ansehen" öffnet den Dialog mit denselben Einträgen,
ein bereits gesehener `latest_id` unterdrückt das Banner beim erneuten Laden vollständig.

**`deploy.sh`-Gate (P6-X):** läuft direkt nach `release_sha` (vor venv/pip/pytest — ein sicher
vermeidbarer Abbruch soll in Sekunden kommen, nicht nach dem teuersten Skriptteil), akzeptiert
UTC- **oder** lokales Datum (ein Deploy kurz nach Mitternacht Lokalzeit läge in UTC noch am
Vortag — ein falscher Abbruch bei einem legitimen Eintrag wäre der schlechtere Fehler als eine
zu großzügige Prüfung). `SHAREFYX_ALLOW_STALE_UPDATELOG=1` überspringt es. **Live-Fund beim
ersten Testlauf** (nicht Advisor): die `grep | sed`-Pipeline unter `pipefail` warf bei einer
fehlenden/leeren Datei einen rohen Bash-Fehler statt der eigenen ABBRUCH-Zeile — `grep` liefert
1 bei keinem Treffer, `pipefail` reicht das durch, `set -e` bricht die Zuweisung sofort ab,
bevor die eigene `if`-Prüfung überhaupt läuft. Mit `|| true` behoben. `test_deploy_scripts.py`s
`_env()`-Helfer setzt die Override-Variable jetzt als Default (die `source_repo`-Fixture trägt
kein `docs/UPDATE_LOG.md`, ohne Default wären alle ~18 bestehenden Deploy-Tests am neuen Gate
gescheitert, nicht nur die drei, die es gezielt prüfen) — dieselbe `_clean_environ()`-Disziplin,
die die Testliste (Plan §5) für jede neue Skript-Testdatei vorschreibt. +3 Tests: Gate blockiert
(kein Log), Gate lässt einen echten heute datierten Eintrag durch (Positivpfad, nicht nur der
Fehlerfall), Override umgeht ein fehlendes Log. Meta-Test
`test_harness_ignores_ambient_sharefyx_configuration` um die neue Env-Var ergänzt (hätte sonst
seinerseits falsch geschlagen).

**`docs/UPDATE_LOG.md`** (neu): erster Eintrag, datiert 2026-08-09, kündigt die künftige
Sichtbarkeitsumstellung an (P6-L, H1 — Pflichtinhalt laut Plan). **Ehrlich zum Gate:** dieser
Eintrag ist nur am 2026-08-09 selbst „frisch" — deployt der Nikinger an einem späteren Tag ohne
neuen Eintrag, blockiert `deploy.sh` by design (Override oder neuer Eintrag), das ist keine
Regression, sondern der Zweck des Gates.

**Schema-3-Rollback-Sicherheit geprüft** (`deploy.sh` rollt bei einem gerissenen Health-Gate auf
altes Binary zurück — „altes Binary gegen Schema-3-DB" ist ein realer Pfad). `upsert_user()`/
`_user_from_row()` benennen Spalten immer schon explizit, die neue Spalte ist für altes Binary
inert. **Eine echte, harmlose Nebenwirkung:** altes Binärs `initialise()` kennt
`_apply_schema_v3()` nicht und schreibt `schema_meta.schema_version` beim Start zurück auf
„2" (Spalte bleibt physisch stehen) — bis der nächste erfolgreiche Deploy wieder „3" schreibt.

**Kleine Design-Entscheidung:** Banner als `position: fixed` statt einer Grid-Zeile in `.shell`
(§4.1s Drei-Spalten-Layout bleibt unverändert); „Update-Log ansehen" sitzt im bestehenden
Konto-Dialog statt einen zweiten Einstellungs-Einstiegspunkt zu erfinden.

**Verifiziert:** `pytest -q` → **620 passed** (604 + 16 neue, deckt sich exakt: 3
`test_authserver_store.py` + 7 `test_updates.py` + 2 `test_api.py` + 3
`test_deploy_scripts.py` + 1 `test_static_routes.py` — der letzte aus dem zweiten Advisor-
Durchlauf, siehe unten). `mcp_smoke.py --json` weiterhin 13/13. `ui_budget.py --json` und
`ui_smoke.py --json` real ausgeführt, beide sauber (erst NACH dem Signatur-Fix — vorher der
`TypeError`-Fund oben). `node --check` auf `app.js`/`updates.js`. Tabu-Diff: `mcpserver/app.py`
ist eine dokumentierte Ein-Zeilen-Abweichung (siehe oben), sonst nur `phase4_auth/authserver/
store.py`, `phase5_ui/webui/{updates,api,config}.py`, `phase5_ui/webui/static/*`,
`phase5_ui/scripts/deploy.sh`, `phase5_ui/scripts/{ui_budget,ui_smoke}.py`, `docs/UPDATE_LOG.md`,
Testdateien — genau die in Step 3s Plan-Dateiliste plus die eine dokumentierte Abweichung.

**Zweiter Advisor-Durchlauf, vier Funde vor dem Commit behoben:** (1) Bannerhöhe war fest
(`44px`) statt am realen, mehrzeiligen Eintragstext gemessen — Fix + Begründung stehen jetzt als
Kommentar in `app.css`/`updates.js` (`syncBannerHeight()`). (2) „sechs weitere Aufrufer" war
falsch gezählt, tatsächlich acht (`grep`-Beleg oben) — korrigiert. (3) Die `updates.js`-vor-
`app.js`-Reihenfolge stand nur in Docstrings, kein Test bewies sie — zwei Ergänzungen in
`test_static_routes.py` (Content-Type-Tabelle + `test_updates_js_loads_before_app_js`). (4)
Schema-3-Rollback-Sicherheit tatsächlich geprüft, nicht nur behauptet — Ergebnis + der eine
harmlose Fund (`schema_version` fällt nach einem Rollback vorübergehend auf „2") stehen im
Absatz direkt darüber.

**Status ehrlich, nicht optimistisch:** Step 3 kann nicht ✅ schließen. **Gate-A→B-Punkt 4 ist
seit 2026-08-11 vollständig geschlossen** — Banner (nach dem Content-Fix vollständig lesbar) UND
Fabians Bestätigung (Update-Banner inklusive Sichtbarkeitsumstellungs-Ankündigung bei ihm
ebenfalls einwandfrei) sind beide bestätigt, technische Seite bei beiden Nutzern ohne Befund.
Einziger noch offener Gate-Punkt: **Punkt 3** (Purge-Zeilenrückgang, frühestens 2026-08-28).
Status bewusst **„gebaut, ein Live-Teil beim Nikinger"** — der eine verbleibende Teil ist rein
zeitgebunden, keine offene Aufgabe.

**Nächster Schritt (konkret):** Block A (Steps 0–3) ist damit vollständig **gebaut**, nichts
davon ist live. Vor Block B steht **GATE A→B** (Plan §4, vier Punkte) — konsolidierte
Reihenfolge für den Nikinger, über Step 2 und Step 3 hinweg, nicht nur Step 3 isoliert:

1. **Frisches Auth-Backup vor dem Deploy** — dieser Deploy migriert die laufende `auth.sqlite3`
   auf Schema 3 (additiv, aber ein frisches Backup unmittelbar davor kostet nichts und deckt
   genau den Fall ab, den `deploy.sh`s eigenes Pre-Deploy-Bundle NICHT abdeckt — das sichert nur
   `DATA_ROOT`, nicht `auth.sqlite3`): `sudo systemctl start sharefyx-authbackup.service`
   (bereits installierter Oneshot, `phase5_ui/systemd/sharefyx-authbackup.service`) — kein
   manueller `authbackup.sh`-Aufruf mit Env-Vars nötig.
2. **Deploy** — `phase5_ui/scripts/deploy.sh main` (oder der passende Ref). Bricht ohne einen
   heute datierten `docs/UPDATE_LOG.md`-Eintrag ab (P6-X) — der vorhandene Eintrag ist auf
   2026-08-09 datiert, trägt also nur am Tag des tatsächlichen Deploys; an einem späteren Tag
   entweder einen neuen Eintrag ergänzen oder `SHAREFYX_ALLOW_STALE_UPDATELOG=1` setzen (bewusst
   so, kein Bug).
3. ~~Gate-A→B-Punkt 1+2~~ — **✅ live bestanden, 2026-08-09** (Nachtrag unten).
4. ~~Gate-A→B-Punkt 4~~ — **✅ vollständig live bestanden, 2026-08-11.** Banner-Hälfte seit
   2026-08-10 (nach einem echten Fund, Nachtrag „achter" unten: Content-Bug in
   `docs/UPDATE_LOG.md`, nicht im Parser — behoben + Regressionstest). Fabian-Hälfte seit
   2026-08-11: bei ihm technisch einwandfrei, Banner inklusive Ankündigung der
   Sichtbarkeitsumstellung gesehen und bestätigt (Nachtrag unten).
5. ~~V42~~ — **geschlossen, 2026-08-12** (Nachtrag unten): `ua` wird von echten MCP-Clients
   zuverlässig gesetzt, unterscheidet aber **nicht** zwischen Claude-Oberflächen — alle senden
   `"Claude-User"`. Negativer, aber definitiver Befund, kein offener Punkt mehr.
6. **Gate-A→B-Punkt 3** — **versucht, 2026-08-09, korrekt noch nicht abgeschlossen** (Nachtrag
   unten): `clients`/`token_families` sind noch zu jung für die 30/90-Tage-Grenze. Frühestens
   ab 2026-08-28 erneut prüfen (`authctl.py purge-expired`, gegen den echten Zeilenrückgang).

Erst wenn alle vier Gate-Punkte stehen, beginnt Step 4 (Storage-Fundament, Block B) — nicht
vorher, das Gate ist im Plan hart. V42 war ohnehin kein Gate-Blocker; jetzt zusätzlich
geschlossen.

**[2026-08-12 Korrektur, Nikinger-Entscheidung]:** Der Nikinger hat explizit angewiesen, Step 4
jetzt zu beginnen und Punkt 3 als offenen, mitlaufenden Punkt zu tragen, statt bis 2026-08-28 zu
warten — eine bewusste, benannte Übersteuerung des Gates, keine stille Abweichung. Punkt 3 bleibt
unten als offen stehen (frühestens 2026-08-28), Step 2 bleibt „gebaut, ein Live-Teil beim
Nikinger" und Abnahmezeile 4 bleibt unverändert **nicht** ✅ — §6s Statusregel („✅ heißt
live-verifiziert, nicht gebaut") gilt unverändert fort. Diese Entscheidung überschreibt nur die
Reihenfolge (Step 4 vor Gate-Abschluss), nicht die Abnahmekriterien selbst.

**Nachtrag, 2026-08-09, siebter — Gate-A→B-Punkte 1–3 live geprüft** (Claude Code direkt auf der
VM, Connector zuvor vom Nikinger neu verbunden — die alte Verbindung hatte noch den 6-Tool-Stand
von vor P6). **Punkte 1+2 ✅:** an `itm_1b4fd59e` (Wegwerf-Testitem, danach archiviert) —
mehrdeutiger `old_text` schlägt fehl (`"edits[0] fand 2 Treffer (Zeilen 2, 4)"`), Datei
unverändert (`version` blieb 1); drei Ersetzungen über zwei Aufrufe, erster ohne `return_body`
liefert eine Quittung (`{"op":"patch",...,"replacements":2,"lines":[1,4],"bytes":{...}}`), zweiter
mit `return_body=true` den vollen Text. Vier eigene Git-Commits in `DATA_ROOT` bestätigt (`create`/
`patch`×2/`archive`). **Punkt 3 — Mechanismus bestätigt, Zahl noch nicht gesunken:**
`SPACE_AUTH_DB=/var/lib/sharefyx/auth.sqlite3 authctl.py purge-expired` lief sauber, 7 reale
abgelaufene Zeilen entfernt (1 `auth_codes` + 6 `access_tokens`) — aber `clients`/`token_families`
beide `0`, **ehrlicher Grund, kein Fehlschlag:** die älteste tote Familie ist vom 2026-07-29, elf
Tage alt, unter der 30-Tage-Grenze; kein Client ist 90 Tage alt (Dienst existiert erst seit
2026-07-24/29). Zeitgleich stiegen `clients`/`token_families` sogar leicht (39→40, 22→23) — der
Nikinger-Reconnect des Connectors registrierte einen neuen DCR-Client, reine Nebenwirkung der
Live-Prüfung selbst. `journalctl -u sharefyx-purge.service` bestätigt zusätzlich: der tägliche
Timer lief zuletzt Aug 9 00:04 (VOR dem heutigen Deploy) noch mit dem alten Purge-Code (Ausgabe
ohne `token_families`/`clients`-Schlüssel) — der heutige manuelle Lauf war der erste mit dem neuen
O2-Code, der nächste Timer-Lauf (Aug 10 00:02) läuft bereits dagegen. **Ob Schritt 1
(Auth-Backup vor dem Deploy) lief, ist aus dem Chat nicht ersichtlich** — der Nikinger postete
nur die `deploy.sh`-Ausgabe. Kein Vorfall, falls übersprungen (additive Migration, kein
Datenverlustrisiko), aber im Nachhinein nicht mehr sinnvoll nachholbar — beim nächsten Deploy
nicht vergessen.

**Nachtrag, 2026-08-10, achter — Gate-A→B-Punkt 4: Content-Bug im Banner gefunden+behoben,
Timer-Bestätigung nachgezogen.** Nikinger-Meldung: Banner sichtbar, Text abgeschnitten bei
„…und alles Neue ist nach". **Kein Parser-Bug** (tut exakt, was Plan §2.4 verlangt: nur `## `/
`- `-Zeilen zählen) — **ein Content-Bug:** der erste `docs/UPDATE_LOG.md`-Eintrag war weich
umgebrochener Fließtext über vier physische Zeilen, der Parser verschluckte die drei
Fortsetzungszeilen stillschweigend. Behoben: zwei echte `- `-Zeilen (je eine physische Zeile) +
ein `<!-- -->`-Formathinweis am Dateianfang. **Regressionstest ergänzt, nicht nur die Datei
gefixt:** `test_real_update_log_has_no_swallowed_continuation_lines` liest die REALE Datei, kein
Test hatte das bis dahin getan. +1 Test (`test_updates.py` 7→8, 621 gesamt). Parser-Gegenprobe:
beide Zeilen jetzt vollständig. **Purge-Timer bestätigt:** Lauf vom 2026-08-10 00:02 mit dem
neuen O2-Code (`token_families`/`clients` beide `0`, konsistent — noch nichts alt genug).
**Nachtrag, 2026-08-10, zweiter Teil:** Nikinger bestätigt Banner jetzt vollständig lesbar,
gerenderter Text stimmt mit dem korrigierten `docs/UPDATE_LOG.md` überein — Banner-Hälfte von
Gate-A→B-Punkt 4 damit ✅. **Nebenbefund während der Live-Prüfung, kein Vorfall:** zwei
transiente Connector-Aussetzer, beide Male griff der Retry, kein Datenverlust — Netzwerk-
Flakiness (Nikingers Einschätzung), kein Server-Fund; `journalctl` zeigte im fraglichen Fenster
keine Exceptions, keine Neustarts.

**Nachtrag, 2026-08-11 — Gate-A→B-Punkt 4 vollständig geschlossen.** Fabians Seite lief
störungsfrei — Connector/UI technisch einwandfrei, und er hat das Update-Banner samt Ankündigung
der Sichtbarkeitsumstellung gesehen und bestätigt (dem Nikinger gegenüber, nicht direkt Claude
Code). Damit ist die zweite, bis dahin einzig offene Hälfte von Punkt 4 geschlossen — **Gate-A→B
hat jetzt nur noch einen offenen Punkt: Punkt 3** (Purge-Zeilenrückgang, frühestens 2026-08-28,
siehe oben). Kein Code-/Testlauf diese Session — reine Statuspflege auf Nikinger-Bitte
(„downtime" vor Arbeitsbeginn morgen genutzt).

**Nachtrag, 2026-08-12 — V42 geschlossen, echtes journald-Fenster ausgewertet.** Fenster war
2026-08-10 00:00 bis heute (~2 Tage echter Betrieb, Deploy vom 08-09 hatte `journald` faktisch
geleert). `journalctl -u sharefyx-mcp --since "2026-08-10 00:00:00" | grep -o '"ua":"[^"]*"' |
sort | uniq -c`: 285 `/mcp`-Requests insgesamt, davon **278 mit `"ua":"Claude-User"`** — jeder
einzelne echte MCP-Tool-Aufruf in diesem Fenster (Rest: 4 eigene `python-httpx`-Testläufe, 2
`CensysInspect`, 1 `curl`, alles kein echter Claude-Client). **Befund: `ua` wird von echten
MCP-Clients zuverlässig gesetzt (nie leer/fehlend) — unterscheidet aber NICHT zwischen
Claude-Oberflächen.** Claude Code und claude.ai (Web/Desktop) senden auf der `/mcp`-Ebene
denselben generischen String, keine surface-spezifische Variante. Zusätzlich beobachtet auf
`/ui/*` (Browser, nicht MCP): 3393 Firefox-, 748 Chrome-, 13 Android-, 1 Safari-Aufruf — echte,
vielfältige menschliche Nutzung über die Testtage, bestätigt aber nur Browser-Diversität, nicht
MCP-Surface-Diversität. **V42 damit geschlossen** — negativer, aber definitiver Befund (P6 Step
2s Client-Surface-Logging liefert kein brauchbares Unterscheidungsmerkmal auf `ev="http"`; eine
Unterscheidung bräuchte eine andere Signalquelle, kein Scope dieser Phase). Kein Code-/Testlauf,
reine Log-Auswertung.

---

## Session stopped — 2026-08-09 (Step 0 — Haushalt, Verifikation, Regeländerungen)

**Auftrag:** Nikinger startete Phase 6 direkt in Claude Code (kein Browser-Planungsauftrag nötig —
`docs/concepts/phase6_shares_plan.md` lag bereits ausführungsreif und untracked im Repo, aus einer
Browser-Planungssession vom selben Tag gegen den Drive-Snapshot `2026_08_09_sharefyx-main`
geschrieben). Gearbeitet wurde Plan §4 Step 0, Punkte 1–6.

**Verifikationsdurchlauf (Plan-Punkt 1):**
- `pytest -q`: **576 passed** — deckt sich exakt mit der Plan-Behauptung. **V39 geschlossen.**
- `git status`: sauber bis auf das untracked `docs/concepts/phase6_shares_plan.md` (jetzt
  hinzugefügt). `HEAD` == `origin/main` (5524a42) — Push-Stand sauber.
- `find . -name "*.md" -size +40k`: keine neuen Treffer durch diesen Commit; bestehende Treffer
  sind bereits 📕/📦 (unverändert seit P5).
- `up:`/`down:`-Links: alle in diesem Commit neu gesetzten (`phase6_shares/CLAUDE.md` ↔
  `docs/concepts/phase6_shares_plan.md`, `docs/INDEX.md`-Zeilen) lösen auf.

**V40 — CVE-2026-48710 („BadHost"):** `pip show starlette` → **1.3.1**, ≥ 1.0.1. **Nicht
betroffen, geprüft-in-Ordnung.** Kein Pin-Update nötig, kein Befund S11.

**V41 — Anthropic-Connector-Doku (Nachfolger V33, seit P4 Step 0 mehrfach durchgereicht ohne
Bearbeitung — siehe `PHASE5_CLOSEOUT_HANDOVER.md` V33-Zeile):** **Diesmal tatsächlich gelesen**,
und zwar die richtige Fläche — dieses Projekt nutzt **Custom Connectors auf claude.ai/Desktop**
(R2), nicht die API-seitige `mcp_servers`/`mcp_toolset`-Fläche. `support.claude.com/en/articles/
11175166` (Custom-Connector-Guide) **nennt keine** Grenze für Tool-Anzahl, Beschreibungslänge oder
Schemaform — auch nichts zu Array-of-Objects-Parametern (relevant für `patch_item`s
`edits: list[TypedDict]`, Step 1). Zwei Drittquellen (sunpeak.ai, startdebugging.net, zur API-
Fläche, nicht zu Custom Connectors) behaupten ein 2KB-Deskriptionslimit bzw. Genauigkeitsverlust
ab 30–50 Tools — **unbestätigt für diese Fläche, nicht übernommen**, nur als Kontext notiert.
sechs → sieben Tools bleibt so oder so weit im unauffälligen Bereich. **V41 geschlossen**, echtes
Schemaform-Verhalten (`list[TypedDict]` durch `fastmcp` 3.4.x) bleibt V48, Step 1, empirisch zu
prüfen.

**Regeländerungen §0.7:**
- **(a) Hard Rule 4** in Root-`CLAUDE.md` neu gefasst, alter Wortlaut durchgestrichen stehen
  gelassen. **Zusatz gegenüber dem Plantext:** ein Satz, dass die neue Regel **erst mit Step 5**
  scharf wird (`.share.yml`/`share_write`/`SharePolicy` existieren vor Step 4/5 nicht im Code) —
  bis dahin gilt faktisch weiter die durchgestrichene Fassung. Reiner Zusatz, ändert die gelockte
  Formulierung nicht. Der `<untrusted_content>`-Satz der alten Regel bleibt **unverändert aktuell**
  (P6-O bestätigt ihn), nur der Cross-Space-Write-Satz wird ersetzt.
- **(b) `ROADMAP.md`:** neue P6-Zeile (🔄) plus datierte Korrekturen an „Feingranulare Rechte" und
  „Mehrmandantenfähigkeit" unter „Bewusst nicht auf der Roadmap".
- **(c) Handover §4.5:** der Plan-Widerspruch (P5 Step 9 „frische Einladung" vs. Plan §2.6 „reine
  Credential-Migration") wird hier festgehalten, nicht im 📕-Snapshot `phase5_ui_plan.md`:
  **gelebt wurde der Step-9-Weg** (frische Einladung). Damit geschlossen.

**V37 (Plan-Punkt 6) — „Exakte Abschnittsüberschriften in `docs/INDEX.md`":** laut
`PHASE5_CLOSEOUT_HANDOVER.md` (📕, nicht editierbar) „faktisch erledigt, nie explizit vermerkt".
**Hier formal abgehakt:** die Active-phase-Überschrift folgt in diesem Commit wieder demselben
Muster (`## Active phase (6 — …)`), wie es P5 in Step 0 anlegte.

**Minor Drift, inline korrigiert (kein Nikinger-Entscheid nötig):**
- `pytest.ini`s `testpaths` nennt Verzeichnisse explizit (kein Glob) — der Plan erwähnt das
  Nachziehen nirgends. `phase6_shares/tests` ergänzt, sonst würde Step 1 seine eigenen Tests nie
  einsammeln.
- Plan-Punkt 5 wollte `docs/INDEX.md` in diesem Commit auch um eine Zeile für `docs/UPDATE_LOG.md`
  ergänzen — diese Datei existiert erst ab Step 3. INDEX' eigene Regel („neue `.md` ⇒ Zeile im
  selben Commit") verbietet das Vorgreifen. Verschoben auf Step 3.
- `phase6_shares/tests/conftest.py` bewusst leer angelegt (P1-Step-0-Präzedenzfall: „Step 0 hat
  bewusst keine Tests, reines Skelett" — `phase1_storage/tests/conftest.py` ist bis heute leer).
- Plan-Punkt 5 nennt auch `scripts/` als Step-0-Deliverable. Git verfolgt keine leeren
  Verzeichnisse, und der erste reale Inhalt (`spacectl.py`/`migrate_visibility.py`) entsteht laut
  Plan erst in Step 6 — `scripts/` entsteht implizit mit der ersten Datei dort, nicht als leerer
  Platzhalter in diesem Commit.

**Phase-Head angelegt** (dieses Dokument), `docs/INDEX.md` um Plan + Phase-Head ergänzt, Root-
`CLAUDE.md`s „Current state" auf 🔄 Phase 6 gestellt.

**Verifiziert:** `pytest -q` nach allen Änderungen erneut grün (siehe Verifikations-Task, Ergebnis
oben) — Änderungen dieser Session sind ausschließlich Dokumentation + eine leere `conftest.py` +
eine `pytest.ini`-Zeile, kein Feature-Code.

**Nachtrag, 2026-08-09, zweiter — Advisor-Review vor Sessionende, vier Funde behoben** (Kurzform,
settled): `docs/INDEX.md`s `ROADMAP.md`-Zeile war stale, korrigiert; Vollständigkeitsprüfung
„jede `.md` hat eine INDEX-Zeile" nachgeholt, alle 32 verlinkt; Staleness-Grep über
`README.md`/`AGENTS.md`/`docs/PROMPTS.md`/`phase5_ui/CLAUDE.md` — keine weiteren Funde;
`ROADMAP.md`s „Mehrmandantenfähigkeit"-Absatz hatte sich selbst widersprochen, korrigiert.
`pytest -q` → 576/576, Size-Sweep sauber.

**Nachtrag, 2026-08-09, dritter — Step 1 (Werkzeug-Ergonomie) fertig** (Kurzform, settled):
`storage/patch.py` (neu: `TextEdit`/`PatchError`/`PatchResult`/`apply_edits()`), `Store.patch()`,
`mcpserver/receipts.py` (neu), siebtes Tool `patch_item`, `return_body` an allen vier
Schreib-Tools, `update_item` lehnt `visibility`/`share_read`/`share_write` ab. `mcp_smoke.py`
13/13. **V48 geschlossen:** `list[TypedDict]` rendert per `fastmcp` 3.4.4 zu einem brauchbaren
Schema, kein Fallback nötig — belegt über den echten `fastmcp.Client`. Drei Advisor-Funde vor
dem Commit: Kollateralschaden durch Quittungen-als-Default (sieben Tests auf JSON umgestellt),
`update_item`s Riegel war ohne die drei echten Parameter wirkungslos (ergänzt, `fastmcp` hätte
sonst vorher abgelehnt), Plan-Testdateinamen wären fixture-los gewesen (Fixtures folgen §5s
Tabelle, nicht dem Fließtext). Kleine Quittungs-Abweichungen von Plan §1.5.3 dokumentiert:
kein `folder` vor Step 4, Archivieren liefert `op="update"` nicht `op="archive"`. `pytest -q` →
**593 passed** (+17: 5 `test_patch.py` + 5 `test_store.py` + 7 `test_tools.py`). Tabu-Diff
gewahrt: nur `storage/`, `mcpserver/{tools,receipts}.py`, drei Testdateien.

**Nachtrag, 2026-08-09, vierter — zweiter Advisor-Durchlauf, zwei Funde vor Sessionende
behoben:** (1) Hard Rule 8 verlangte `phase1_storage/CLAUDE.md` und `phase2_mcp/CLAUDE.md` im
**selben** Commit wie `storage/patch.py`/`tools.py` — waren stattdessen einen Commit zu spät
nachgezogen. Beide jetzt aktuell: Modul-Status-Zeilen (P6 Step 1 als Zeile 9 je Paket),
Testzahlen 81/92 (`pytest --collect-only -q` nachgezählt), `phase2_mcp/CLAUDE.md`s P2-K-
Entscheidung („kein siebtes Tool") mit datierter Korrektur versehen, dritte Contract-Öffnung in
`phase1_storage/CLAUDE.md` dokumentiert. (2) `test_patch_creates_exactly_one_git_commit` prüfte
`len(log) == 2` (absolute Commitzahl im ganzen Test-Repo) statt das Delta — wäre auch bei einem
Bug in `create()`s Commit-Anzahl grün geblieben. Auf Vorher/Nachher-Differenz umgestellt. 593/593
weiterhin grün, eigener Commit (nicht `--amend`).

**Nachtrag, 2026-08-09, fünfter — Step 2 (Betrieb) fertig, in derselben Sitzung fortgesetzt.**
Plan §4 Step 2 (`docs/concepts/phase6_shares_plan.md:694-709`) ist der einzige Block-A-Step ohne
DoD/Testliste im Plandokument — vier Prosa-Punkte, keine Spezifikation. Zwei Advisor-Pässe vor
bzw. nach der Umsetzung eingeholt (Details unten je Punkt und im Verifiziert-Absatz); die
Ausführungsplanung selbst lag nur als Session-lokale Skizze vor und ist hier vollständig
nacherzählt, kein separates Dokument im Repo.

**1. O2** — `authserver/store.py :: purge_expired()` räumt jetzt auch `token_families` (tot =
nach dem bestehenden Ablauf-Sweep keine Kind-Zeile mehr in `access_tokens`/`refresh_tokens`/
`auth_codes` — deckt widerrufen, natürlich abgelaufen UND abgebrochene Autorisierung mit einem
Prädikat ab, letzteres nennt der Plan-Text nicht explizit, bewusste Erweiterung) und `clients`
(kein verbleibender `token_families`-Eintrag) ab, je mit eigener Altersgrenze:
`TOKEN_FAMILY_RETENTION_S` (30 Tage) und **länger** `CLIENT_RETENTION_S` (90 Tage) — eine
`clients`-Zeile ist die Registrierung, die ein Connector im Claude-Account weiter vorzeigt, und
P5-Q widerruft bei einem Passwortwechsel sofort alle Familien; zu kurze Client-Retention riskiert
„unknown client" beim nächsten Autorisierungsversuch statt eines einfachen Re-Auth. `NOT EXISTS`
statt `NOT IN` (immun gegen NULL-in-Subquery, auch wenn die FK-Spalten heute `NOT NULL` sind).
Reihenfolge zwingend wegen `PRAGMA foreign_keys=ON` (store.py:218): Familien zuerst, dann
Clients, in derselben Transaktion. Die 30-Tage-Grenze zählt ab `COALESCE(revoked_at,
created_at)`, nicht ab `created_at` allein — **zweiter Advisor-Durchlauf, echter Fund vor dem
Commit:** eine per Replay-Erkennung getötete Familie (der Härtetest aus der Phase-4-Mission,
`revoked_reason='refresh_replay'`) wäre unter der `created_at`-only-Fassung binnen 24h wieder
verschwunden, wenn sie schon Wochen alt war — ihr einziger forensischer Beleg gelöscht statt 30
Tage aufbewahrt. `ui_sessions`/`invites` daneben zählten schon immer richtig ab ihrem Ereignis;
`token_families` war beim ersten Entwurf die Ausnahme, jetzt korrigiert, mit eigenem
Regressionstest (`test_purge_expired_keeps_a_family_revoked_today_even_if_born_long_ago`).
+8 Tests in `test_authserver_store.py` (250→258).

**2. Client-Surface-Logging (`ua`, V42)** — landet ausschließlich auf `AccessLogASGI`s
`ev="http"`-Zeile (`_ALLOWED_FIELDS` + 120-Zeichen-Kürzung), nicht auf `ev="tool"`:
`ToolCallLogMiddleware` hat keinen ASGI-Scope-Zugriff, `context.py` steht nicht auf Step 2s
Berührungsliste. Geteilter Zeitstempel mit der `ev="tool"`-Zeile reicht für V42 (welche
Oberfläche stellte diese Anfrage). Verifiziert (nicht nur vom Advisor vermutet):
`TokenScrubbingFilter` (`logging_setup.py:65-77`) scrubbt Dict-**Werte** vor dem Formatter, ist
am `sharefyx.request`-Handler angeschlagen (`_configure_request_logger`) — `ua` bekommt beide
Verteidigungen (Kürzung + Muster-Scrub), nicht nur eine. +3 Tests (`test_request_log.py` 11→13,
`test_logging.py` 8→9).

**3. `diagnose.sh`** — Prüfung 11, INFO-Kategorie (kein `diagnose()`-Abbruch, gleiche Einordnung
wie die Backup-Frische-Prüfung direkt daneben): Alter von `sharefyx-purge.timer`s letztem Lauf
über `systemctl show ... --property=LastTriggerUSec`, WARNUNG mit Enable-Befehl falls nie
gelaufen, sonst WARNUNG ab > 48h. Der zweite Plan-Punkt (verwaiste Space-Namen in `.share.yml`)
bewusst nicht gebaut — die Datei existiert erst ab Step 4, der Plan selbst nennt das „ab Block
B". Kein Unit-Test (Skript hat wie der Rest von `diagnose.sh` keine automatisierten Tests) —
**aber real gegen den echten, auf dieser Maschine laufenden `sharefyx-purge.timer` geprüft**
(Advisor-Vorgabe, zweiter Durchlauf: `bash -n` beweist nur Syntax, nicht Ausgabeformat, genau der
Fehler hinter V13 „Ausgabeformat nie live geprüft"). Diese Session lief zufällig direkt auf der
Heim-VM (bestätigt über `hostname`/`DATA_ROOT`/`systemctl is-active sharefyx-mcp`, siehe
Projekt-Memory) — read-only `systemctl show sharefyx-purge.timer --property=LastTriggerUSec`
lieferte einen echten Zeitstempel (`LoadState=loaded`, `ActiveState=active`), das neue Skript-
Fragment korrekt gegengerechnet: Alter ≈ 18,6h, unter 48h, INFO-Zweig korrekt genommen — sowie
gegen einen nicht existierenden Unit-Namen (leere Ausgabe, `LoadState=not-found`), WARNUNG-Zweig
korrekt genommen. Kein Schreibzugriff, kein `restart`/`enable` — bleibt Nikinger-Sache.

**4. `ui_budget.py`** — neue, eigenständige `_measure_latency()` + `LatencyMetric`-Dataclass
(kein `budget_bytes`/`ok`, eigene JSON-Sektion `"latency"`) für `search_items`/`get_item` (MCP,
echter `mcpserver.app::create_app()`, gleicher Client/Transport-Stack wie `mcp_smoke.py`) und
`GET /api/v1/overview` (Session-Cookie direkt über `AuthStore.create_session()` gemintet, kein
Login-Umweg). Bewusst getrennt von den vier bestehenden Größen-`Metric`s: die hätten
`main()`s Exit-Code — ein live-verifiziertes Abnahme-Artefakt (P5 Zeile 15) — zeitabhängig
gemacht. Jede der drei Messungen macht einen verworfenen Aufwärmlauf vor dem gemessenen Aufruf
(Advisor-Fund, zweiter Durchlauf) — ohne den hätte ein einzelner kalter Aufruf Routen-Setup/
Session-Verhandlung mitgemessen, nicht die eigentliche Frage von P6-I/P6-S beantwortet. Echter
Lauf gegen ein temporäres `DATA_ROOT` (220 Items, dieselbe Saat wie `_measure()`, Hard Rule 2:
Index rekonstruiert sich immer aus den Dateien), **dreifach reproduziert:** `search_items`
95–96 ms/20 KB, `get_item` 5 ms/0,5 KB, `GET /api/v1/overview` **438–453 ms/1,5 KB** — konstant
über alle drei Läufe hinweg, also kein Kaltstart-Artefakt, sondern eine echte, reproduzierbare
Kostenstelle. `/api/v1/overview` aggregiert vermutlich über den vollen Index (P6-S, `Store.
search()` liest weiterhin jede Datei) — genau die Zahl, die die nächste Entscheidung laut Plan
haben sollte, kein Zufallsfund. Kein neuer Test (`ui_budget.py` hatte nie welche, gleiche
Kategorie wie `mcp_smoke.py`).

**Hard Rule 8, fünf Köpfe im selben Commit:** `phase4_auth/CLAUDE.md` (O2-Zeile geschlossen),
`phase2_mcp/CLAUDE.md` (Modul-Status Zeile 10 + „Gesamt"-Zeile neunte Drift-Instanz, 92→95),
`phase3_edge/CLAUDE.md` (Prüfung-11-Ergänzung), `phase5_ui/CLAUDE.md` (`ui_budget.py`-Ergänzung),
dieser Kopf. `docs/INDEX.md`s `phase2_mcp`-Zeile im selben Commit nachgezogen (Testzahl,
Step-2-Erwähnung).

**Verifiziert:** `pytest -q` → **604 passed** (593 + 11 neue, deckt sich exakt). Volle
Testsuite gelaufen, nicht nur die vier neuen Dateien. `ui_budget.py` real ausgeführt (Text UND
`--json`) — Zahlen oben sind aus diesem echten Lauf, keine Schätzung. `mcp_smoke.py --json`
weiterhin 13/13 (Step-1-Baseline unangetastet). `authctl.py purge-expired` nicht gesondert
gegen eine Temp-DB nachgestellt — bereits vollständig über die neuen `purge_expired()`-Tests
abgedeckt, ein zusätzlicher CLI-Probelauf hätte denselben Code-Pfad kein zweites Mal geprüft.

**Status ehrlich, nicht optimistisch:** Step 2 kann nicht ✅ schließen. V42 braucht zwei echte
Tage journald auf der Live-VM; Gate A→B Punkt 3 braucht einen echten Purge-Lauf mit sinkender
`clients`-Zeilenzahl. Beide sind Nikinger-Sache, nicht in dieser Session baubar — Status bewusst
**„gebaut, Live-Teile beim Nikinger"** (P5 Step 8s Präzedenzformulierung), V42 in der
Modul-Status-Tabelle namentlich offen.
