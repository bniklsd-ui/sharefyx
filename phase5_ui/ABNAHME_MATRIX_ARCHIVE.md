---
status: archive
purpose: L3-Archiv des Abschnitts „Abnahmestand (Plan §6)" aus `phase5_ui/CLAUDE.md` — die 20-Zeilen-Matrix mit Belegen, Kurzfassung, zwei späteren Nachträgen und der Cutover-Notiz, verbatim
read-when: nur beim Audit — welche der 20 Abnahmezeilen mit welchem Beleg live bestanden wurde, oder warum eine Zeile damals anders stand
detail: L3
up: ./CLAUDE.md
down:
updated: 2026-10-02 (erste Rotation, Gate/Z-Doku-Pflege P9-L — 99 Zeilen / 12.195 B wortgleich aus dem Head hierher verschoben; der Head behält nur noch Stand und Zeiger. Phase 5 ist seit 2026-08-09 abgeschlossen, die Matrix wurde seither nie nachgezogen)
---
# Abnahmestand Phase 5 (verbatim aus `CLAUDE.md`)

> **Rotiert am 2026-10-02, Gate/Z-Doku-Pflege (P9-L).** Alles unter der Überschrift ist **wortgleich**
> aus `phase5_ui/CLAUDE.md` §„Abnahmestand (Plan §6)" hierher verschoben — inklusive der
> Kurzfassung, der beiden späteren Nachträge (2026-08-13-Korrektur, 2026-10-02 trace-Block) und der
> Cutover-Notiz — die **vier** Nachträge der Zeile 20 stehen nicht hier, sondern im Session-Block unten. Der Phase-Head behält den Abschnittsnamen und den Stand
> (**20/20 ✅, Phase 5 ✅**). Das Abnahmeprotokoll als Kurzfassung bleibt, wo es war:
> `../docs/concepts/P5_ABNAHME_2026-08-09.md`.

## Abnahmestand (Plan §6) — Stand 2026-08-09

Die Ergebnisse entstanden über sieben Sessions verteilt, mehrere davon schon in
`SESSIONS_ARCHIVE.md`. Diese Tabelle ist der **eine** Ort, an dem der Gesamtstand steht; sie
wird bei jedem Live-Ergebnis nachgezogen. **Statusregel des Plans: ✅ heißt live-verifiziert,
nicht gebaut.** Alle 20 Zeilen stehen ✅ (2026-08-09) — die Matrix ist damit vollständig, und mit
den Step-9-Abschlussarbeiten (vierter Nachtrag unten) ist auch der formale Phasenschluss
(Root-`CLAUDE.md`/`ROADMAP.md` auf ✅) vollzogen. **Phase 5 ✅.**

| # | Kriterium | Stand | Beleg |
|---|---|---|---|
| 1 | Einladungslink erzeugt, Konto von null auf aktiv | ✅ | Nikinger live, 2026-08-04 |
| 2 | Einladungslink ein zweites Mal → abgelehnt | ✅ | Nikinger live, 2026-08-05 |
| 3 | TOTP-Seed einmal gezeigt, Authenticator-Code akzeptiert | ✅ | Nikinger live, 2026-08-04 (nach dem `Referrer-Policy`/Origin-Fund) |
| 4 | Recovery-Code ersetzt den TOTP-Code, danach abgelehnt | ✅ | Nikinger live, 2026-08-05 |
| 5 | Passwort im Browser geändert **ohne** `systemctl restart`, neuer Login sofort gültig | ✅ | Nikinger live, 2026-08-05 nach Step 7b — **schließt Betriebsnotiz O1 auch live** |
| 6 | Nach dem Passwortwechsel: Connector fordert neue Autorisierung · andere UI-Sitzung beendet · aktuelle läuft weiter | ✅ | **Nikinger live, 2026-08-05** mit einem privaten Fenster als zweiter Sitzung (ein zweiter Tab teilt das Cookie und beweist nichts). Das private Fenster bekam die „Sitzung abgelaufen"-Karte. **Read-only in der DB gegengeprüft statt den Screenshot zu übernehmen:** 7 × `ui_sessions.revoked_reason='password_changed'`, 7 × `token_families.revoked_reason='password_changed'` (Connector muss neu autorisieren), und 6 × `rotated` — genau P5-Q, die eigene Sitzung wird **rotiert, nicht widerrufen** |
| 7 | Fehlversuchsbremse greift für UI-Login und OAuth-Consent gemeinsam | ✅ | Nikinger live, 2026-08-05 |
| 8 | `authctl.py list-users` zeigt keinen Hash und keinen Seed | ✅ | Nikinger live, 2026-08-05 |
| 9 | `auth.sqlite3` mit `strings`: kein Base32-Seed im Klartext | ✅ | Nikinger live, 2026-08-05 |
| 10 | Anlegen/Bearbeiten/Anhängen/Archivieren über die UI; `.md` im `DATA_ROOT` korrekt **und** Git-Commit existiert | ✅ | **Nikinger live, 2026-08-07** — vier UI-Aktionen auf `itm_b252a444`, `git log --oneline` im Datenverzeichnis zeigt vier eigene Commits (`create`/`update`/`append`/`archive`), Datei liegt danach korrekt unter `_archive/` |
| 11 | Konflikt in zwei Tabs → Versionsband `--warn` + Dialog, kein stiller Überschreiber | ✅ | Nikinger live, 2026-08-05 nach Step 7b |
| 12 | Fremder Space sichtbar/lesbar, **ohne** Schreib-Bedienelemente im DOM | ✅ | Nikinger live in DevTools, 2026-08-05 nach Step 7b (vorher nur `hidden` — siehe F7-Umfeld im Session-Block) |
| 13 | Unbekanntes Frontmatter-Feld überlebt eine UI-Bearbeitung unverändert | ✅ | **Nikinger live, 2026-08-07** — `custom_test: roundtrip-check` per Hand in `itm_749d6a12`s Frontmatter eingefügt, danach eine UI-Bearbeitung gespeichert; Feld überlebte unverändert. Nebenfund: `version` sprang 3→5 statt 3→4 — kein Bug, `store.py :: _reconcile_and_get_row()` erkannte die externe Änderung, schrieb einen eigenen `drift`-Commit (Version-Repair, Entscheidung D), erst danach kam der `update`-Commit der UI obendrauf; `git log` zeigt beide Commits einzeln |
| 14 | `format: markdown` erscheint nach dem ersten UI-Schreibvorgang und stört keinen Tool-Aufruf | ✅ | Feld war nach der ersten UI-Bearbeitung von `itm_749d6a12` bereits gesetzt; **Claude Code live über den echten MCP-Connector** (`get_item`, Space `niklas`) gegengeprüft — sauberer Read, keine Fehlermeldung, `format: markdown` unverändert im Ergebnis |
| 15 | `ui_budget.py` liefert alle vier Zahlen | ✅ | **Nikinger live, 2026-08-07** (`.venv/bin/python phase5_ui/scripts/ui_budget.py`, nachdem ein bloßes `python3` mit `ModuleNotFoundError: httpx` scheiterte — falscher Interpreter, kein Befund). Alle 5 Messgrößen im Zielkorridor, deckungsgleich mit dem Kandidatenbeleg vom 2026-08-05 |
| 16 | `deploy.sh` rollt bei kaputtem Health-Endpunkt automatisch zurück | ✅ | **Nikinger live, 2026-08-05 20:40**, nach dem Cutover auf `/opt/sharefyx/current`. `SHAREFYX_PORT=9999` zeigte das Gate auf einen toten Port (der Dienst selbst blieb gesund — simuliert wird ein kaputter Health-Endpunkt, nicht ein kaputter Dienst). Read-only gegengeprüft, nicht nur die Meldung übernommen: `current` zeigt wieder aufs erste Release, das gescheiterte liegt als `…Z.failed` daneben, `ExecMainStartTimestamp` passt zum Rollback-Neustart, alle vier Proben und der öffentliche Funnel-Weg wieder korrekt. **Der `.failed`-Fund vom selben Tag in Aktion:** ohne die Markierung wäre genau dieses Verzeichnis beim nächsten Rollback das Ziel gewesen |
| 17 | Beide Nutzer benutzen UI **und** Connector am selben Tag gegen dieselbe Instanz | ✅ | **Nikinger + Fabian, 2026-08-07.** Read-only in `auth.sqlite3` gegengeprüft statt die Meldung zu übernehmen: `ui_sessions` zeigt aktive Sitzungen für **beide** Spaces `niklas` und `fabian` an diesem Tag (05:14–12:32 UTC) — Fabians UI-Login stammt aus seiner Einladung/Reset (Step 9); `journalctl` bestätigt echten `/mcp`-Traffic am selben Tag. **Eine Präzisierung dieser Session:** Fabians aktuell aktive Connector-Autorisierung (`token_families`) wurde bereits 2026-08-06 08:23 ausgestellt — **vor** dem S10-Fix (Commit 10:33, deployt 2026-08-07 05:23/restart 07:25). Sie ist also die Fortsetzung der alten Sitzung, kein frischer Re-Auth unter dem gefixten Code, und beweist damit nur die Connector-**Nutzung** an sich (Zeile 17s Kriterium), nicht S10s Revoke-Verhalten unter Live-Bedingungen — dafür siehe Nebenfund unten |
| — | *(Staging war kein eigenes Akzeptanzkriterium — P5-AB nennt es im Scope, §6 prüft es nicht. Am 2026-08-06 abgeschaltet, Begründung im Session-Block.)* | | |
| 18 | `git diff` auf `storage/`, `mcpserver/{tools,permissions,server}.py`: leer | ✅ | bei jedem Step-Commit geprüft, zuletzt Step 7b |
| 19 | Cookie an `/mcp` ignoriert; Bearer an `/api` ignoriert | ✅ | Testseite ✅ (`test_isolation.py`, `test_overview.py`) **plus Nikinger live, 2026-08-07**: `curl` gegen `PUBLIC_BASE_URL` (aus `phase3_edge/local.env`) — `GET /api/v1/me` ohne Cookie/Bearer → `401`; `GET /mcp/` mit gefälschtem `__Host-sfx_session`-Cookie (kein Bearer) → `401` |
| 20 | Reboot: UI, Connector, Timer kommen ohne Handgriff zurück | ✅ | **Nikinger live, 2026-08-09** — unbewusst ausgelöster VM-Reboot (nicht `sudo reboot`), gleicher Prüffall wie P3 Zeile 6. Details im Session-Block |

**Kurz:** 20 von 20 live bestanden, 0 teilweise, 0 offen. Zeilen 10/13/14/15/17/19 sind am
2026-08-07 den Sprung von „Code fertig" auf „live" gegangen — **✅ heißt live-verifiziert, nicht
gebaut.** Zeile 17 war die letzte, die Fabian brauchte (Step 9); Zeile 20 (2026-08-09) war die
letzte insgesamt. **Abnahmematrix vollständig, Abnahmeprotokoll geschrieben**
(`docs/concepts/P5_ABNAHME_2026-08-09.md`), Migrations-Runbook-Schritt 4 bereits erledigt
vorgefunden (kein Kommando nötig, Session-Block). Alle Step-9-Abschlussarbeiten sind erledigt —
`phase5_ui_uebersicht.svg`, `PHASE5_CLOSEOUT_HANDOVER.md`, Rotationsprüfung (weiterhin genau ein
Session-Block, kein Rotieren nötig) und Root-`CLAUDE.md`/`ROADMAP.md` auf ✅, alle im selben
Commit (vierter Nachtrag unten). **Phase 5 formal abgeschlossen, 2026-08-09.**

**[2026-10-02, P9 Block trace] Nachvollziehbarkeit in der Oberfläche** (zehnte
P1-Contract-Öffnung, angekündigt; Locks P9-Z/AA/AB): `api.py` reicht `actor=session.space` an
**alle neun** Store-Schreibaufrufe durch (inkl. `_spaces_delete`, das beim Space-Entfernen fremde
Items in den Home-Space verschiebt — ein Mensch-Akt, also mit Akteur); `serializers.py` gibt
`updated_by` in `item_to_json()`/`summary_to_json()` mit; **`_PATCH_FIELDS` und die
POST-Whitelist bleiben ohne `updated_by`** (P9-AA) · `static/list.js :: itemMetaLine()` führt
„bei X" nach dem Status · `static/app.html` bekommt das Feld `#field-assignee` (Text +
`<datalist>` aus `state.spaces`) und die Lesezeile `#meta-updated-by` · `static/js/editor.js`
führt `assignee` in Schnappschuss/`currentFormValues()`/`isDirty()`/`renderMetaDigest()`/Laden/
Entwurf, **füllt es beim Wechsel auf `doing` nur wenn es leer ist** (P9-Z) und zeigt beide
Angaben in der Nur-lesen-Ansicht · `static/app.css` bekommt `.panel__readline` (`:empty` →
`display: none`).

**Gemessene Abweichung von P9-AA, im Code dokumentiert statt geglättet:** die Klammer in P9-AA
lautet „ein mitgeschicktes Feld ist `ValidationError`, wie heute `updated`" — das gilt für
**PATCH** (unbekanntes Feld → `422 validation_failed`, `api.py:890`) und für den Kern
(`_SYSTEM_MANAGED_FIELDS`), **nicht** für **POST**: `_items_post` hat keine `unknown`-Prüfung,
sondern filtert lautlos auf eine Whitelist, ein `updated_by` im POST-Body wird also still
verworfen — dieselbe Eigenschaft, die heute `created`/`version`/`space` dort haben. Der Kern
bleibt unberührt (P9-74 hält: kein Kanal kann es setzen), aber die *Form* der Ablehnung ist je
Route eine andere. **Bewusst nicht vereinheitlicht:** eine `unknown`-Prüfung im POST würde jedes
unbekannte Feld ablehnen und damit Round-Trips über Schreib-Clients brechen, die den vollen
Item-JSON zurückschicken.

**Ein Test datiert zugeschnitten** (in `phase9_hardening/tests/test_step_f_schema.py`, nicht
hier): der Wächter gegen abgetipptes Step-F-Vokabular in `editor.js` musste P9-Z weichen — siehe
den dortigen Docstring. **Fünf neue Tests** in `phase5_ui/tests/`: einer in `test_api.py`
(`updated_by` aus der Sitzung **und** PATCH → 422 mit unangetasteter Datei, beide Hälften in
einem Test), vier in `test_static_routes.py` (P9-Z-Zweig am Text, „genau drei Zuweisungen an
`fieldAssigneeEl.value`", Markup-Feld-vs-Lesezeile, Listenzeile). **Browser 8/8** gegen eine
eigene **Zwei-Principalen**-TLS-Wegwerf-Instanz (Port 18777, `p9_trace_wegwerf.py`/
`p9_trace_self_check.py`), Gegenprobe: ohne die Leer-Prüfung im P9-Z-Zweig meldet S5 rot —
B zieht eine **A zugewiesene** Aufgabe auf „In Arbeit" und der Assignee springt von `alpha` auf
`beta`. Sechs Bilder `p9_trace_01..06_*`, `screenshots_latest/` darauf umgehängt.

**[2026-08-13 Korrektur, Nikinger-Feedback aus echtem Betrieb, außerhalb eines Plan-Steps]:**
die Wortmarke oben links (`.rail__brand`, `app.html`/`app.css`) trug keine Versionsnummer.
Ergänzt: `<span class="rail__version">v2</span>` neben „sharefyx" — Phase 6 entspricht laut
Nikinger v2 (kein eigenes Versionierungsschema im Code, reiner Hardcode wie die Wortmarke
selbst). Bewusst **keine** eigene Schriftart — `.rail__version` erbt `font-family` von
`.rail__brand` (nicht neu gesetzt), nur `font-size: 9px`/`opacity: .6`/`vertical-align: super`
zur optischen Unterordnung. Sichtgeprüft per Playwright-Screenshot gegen die echte `app.css`
(nicht nur behauptet) — bei ≤1280px Viewportbreite kollabiert `.rail__brand` ohnehin komplett
(bestehende Breakpoint-Regel §4.3, `app.css` Zeile ~1088), die Version ist dort also
plangemäß mit unsichtbar, kein neuer Sonderfall. Reine `webui/static/`-Änderung (P5-B tabu-Liste
betrifft nur `storage/`/`mcpserver/{tools,permissions,server}.py`, nicht statische Assets), JS
bleibt laut P5-T ohnehin unit-ungetestet — kein neuer Test, `pytest` (722/722) unverändert grün
zur Regressionsprobe. Phase 5 ist geschlossen; dieser Head bekommt keinen neuen
Session-Block dafür (kosmetischer Ein-Zeilen-Fix, kein Step) — Herleitung und Screenshot-Beleg
stehen stattdessen in `phase6_shares/CLAUDE.md`s aktuellem Session-Block (die aktive Phase, aus
der das Feedback kam).

**Cutover auf Release-Verzeichnisse vollzogen (2026-08-05 20:37, Nikinger):** der Dienst läuft
seither aus `/opt/sharefyx/current` statt aus dem Git-Arbeitsverzeichnis. „Datei ändern +
`systemctl restart`" ist damit wirkungslos — es zählt nur noch, was `deploy.sh` gebaut hat.
Rückweg, falls je nötig: `REPO_ROOT`/`VENV` in `phase3_edge/local.env` zurück auf
