---
status: snapshot
purpose: Abschluss-Handover P5→P6 — Status, Delta seit dem P4-Handover, offene Entscheidungen für die nächste Planung, [VERIFY]-Bilanz V27–V38
read-when: Start der P6-Planungssession, VOR dem Entwurf des Claude-Code-Plans — dann einmal ganz lesen
detail: L2
up: ../../phase5_ui/CLAUDE.md
down:
  - ./phase5_ui_plan.md                        # Entscheidungen P5-A–P5-AE, Steps 0–9 — Herkunft, nicht Ergebnis
  - ./P5_ABNAHME_2026-08-09.md                  # was am Ende tatsächlich live bewiesen wurde, 20/20
  - ./PHASE4_CLOSEOUT_HANDOVER.md                # Vorgänger; V14–V26, Herkunft der P5-Entscheidungen
updated: 2026-08-09
---
# Phase 5 — Closeout-Handover (P5 → P6)

> **Für den kalten Leser.** Phase 5 ist inhaltlich abgeschlossen: **20/20 Abnahmezeilen live
> bestanden, 576 Tests grün (gemockt), beide Blöcke durch das harte Gate.** Menschen benutzen
> das System jetzt ohne SSH.
>
> **Dieses Dokument ist keine zweite Kopie des Plans.** Code ist Wahrheit; der Plan
> (`phase5_ui_plan.md`) ist Herkunft, das Abnahmeprotokoll ist Beleg, der Phase-Head
> (`phase5_ui/CLAUDE.md`) ist der operative Einstieg. Hier steht nur, was der P6-Chat wissen
> muss, **bevor** er plant — plus die Dinge, die sonst niemand aufschreibt.

---

## 1 Status in fünf Sätzen

1. **Beide Blöcke stehen live bewiesen.** Block A (Sicherheit/Selbstverwaltung: Einladung,
   Passwort, TOTP, Recovery-Code, Fehlversuchsbremse, Session-Isolation) und Block B
   (REST-API/UI: Anlegen/Bearbeiten/Anhängen/Archivieren, Konfliktdialog, Fremd-Space
   read-only) — 20/20 Zeilen, 0 teilweise, 0 offen.
2. **Menschen setzen ihr Passwort jetzt selbst, ohne Neustart.** Das war der eigentliche
   Härtetest der Phase, nicht die Oberfläche — schließt Betriebsnotiz **O1** auch live
   (Abnahmezeile 5).
3. **Der P2/P4-Seam hat erneut gehalten.** `git diff` auf `storage/`,
   `mcpserver/{tools,permissions,server}.py` blieb über die gesamte Phase **leer**
   (Kriterium 18) — eine komplette Web-UI + REST-API entstand, ohne eine Zeile Tool-Code
   anzufassen. Zweiter Beweis dieser Art nach Phase 4, ein Level höher (diesmal eine ganze
   API-Fläche, nicht nur ein Auth-Austausch).
4. **Beide Menschen sind live durchgelaufen.** Niklas und Fabian benutzten UI **und** Connector
   am selben Tag gegen dieselbe Instanz (Zeile 17, Step 9) — das ist die eigentliche Aussage der
   Phase, nicht nur ein Kästchen in der Matrix.
5. **Formal geschlossen im selben Commit wie dieses Dokument.** Root-`CLAUDE.md`/`ROADMAP.md`
   stehen auf „Phase 5 ✅", `docs/INDEX.md` hat die `phase5_ui`-Zeilen nach „Completed phases"
   verschoben — Nikinger-Entscheidung dieser Session (AskUserQuestion: „im selben Commit"), weil
   die Abnahmematrix vollständig ist und die Statusregel des Plans ohnehin nur verlangt, dass ✅
   live-verifiziert bedeutet, nicht dass der Formalakt separat verzögert werden muss.

**Rotationsprüfung:** `phase5_ui/CLAUDE.md` trägt weiterhin **genau einen** Session-Block
(`## Session stopped — 2026-08-09`, jetzt mit vier Nachträgen — dieser Handover ist Teil des
vierten), unter dem 40-KB-Softcap. `SESSIONS_ARCHIVE.md` trägt dreizehn archivierte Blöcke.
**Nichts zu rotieren.**

**Repo-Zustand bei Abfassung dieses Dokuments:** Arbeitsbaum sauber vor diesem Commit, lokaler
`main` lag **4 Commits vor `origin/main`**. Nikinger-Entscheidung dieser Session: nach dem
Abschluss-Commit direkt pushen — der Push holt damit auch die vier vorher schon lokal fertigen
Commits nach, nicht nur diesen.

---

## 2 Delta seit dem P4-Handover

Nur was sich geändert hat. Alles Unveränderte steht im P4-Handover und gilt weiter.

| Thema | P4-Stand | P5-Stand |
|---|---|---|
| Passwortvergabe | keine — nur `provision_user.py` per SSH | Einladung + volle Selbstverwaltung im Browser (Passwort, TOTP, Recovery, Connector-Widerruf), kein SSH mehr nötig |
| Nutzerakten | Keyring `auth-users`, einmal beim Start gelesen (O1) | `auth.sqlite3` Schema 2 (`users`/`invites`/`recovery_codes`/`ui_sessions`), **live gelesen — O1 strukturell geschlossen** |
| TOTP-Seed at rest | im Keyring-Credential-Snapshot, umkehrbar | AES-256-GCM verschlüsselt in der DB, drittes Credential `auth-dek`, AAD = Space-Name (P5-J) |
| UI | keine — nur das P4-Wegwerf-Login-Formular für OAuth-Consent | echte Single-File-UI unter `/ui` (kein Build-Step), REST-API `/api/v1/*` |
| Auth-Wege | nur OAuth (Bearer) | **zwei architektonisch getrennte:** Cookie-Session (`/ui`, `/api`) und Bearer (`/mcp`) — keiner akzeptiert den anderen (P5-D/F, Kriterium 19) |
| Betrieb | Dienst lief aus dem Git-Arbeitsverzeichnis | Release-Verzeichnisse (`/opt/sharefyx/releases`), `deploy.sh`/`rollback.sh` mit Health-Gate + Auto-Rollback, verschlüsseltes Auth-Backup. **Cutover 2026-08-05** — „Datei ändern + `systemctl restart`" ist seither wirkungslos |
| Sicherheitsbefunde | S2–S8 offen (7 Stück) | S2–S8 **vollständig geschlossen**; zwei neue gefunden und geschlossen (**S9** Status-Gate fehlte, **S10** Reset widerrief keine Token-Familien/Sitzungen); **O2 weiterhin offen** |
| Tests | 347 | **576** |
| R5 (Auth) | OAuth 2.1 + DCR | unverändert — die UI ergänzt einen eigenen, getrennten Cookie-Session-Weg daneben, ersetzt nichts |

**Neue Betriebswahrheiten, die P6 kennen muss:**

- **Deploy-Quelle ist das lokale Repo, nicht GitHub** — `deploy.sh origin/main` funktioniert nach
  einem `git fetch` trotzdem, der Klon bringt die Remote-Refs mit (Nikinger-Entscheidung, Step 8).
- **Staging existiert im Code, ist aber abgeschaltet** — Unit, Skripte, vier Tests bleiben im
  Repo, die Inbetriebnahme wurde zurückgenommen (revidiert P5-AB). Grund: die Hauptzugriffsrechner
  sind Arbeitsrechner ohne Tailscale, ein tailnet-only-Staging ist dort strukturell unerreichbar,
  und eine zweite öffentliche Fläche für eine Instanz, die ihren Zweck nicht erfüllt, ist ein
  schlechtes Geschäft. Der Langzeittest ist die tägliche Nutzung von `sharefyx-mcp` selbst.
- **Ein Test, dessen Verhalten von der Shell des Aufrufers abhängt, ist kein Test** — die
  Testsuite erbte einmal `os.environ` und startete den Produktivdienst dabei 52-mal neu
  ([[feedback_test_harness_never_inherits_env]]). Behoben über `_clean_environ()`; jede neue
  Testdatei, die Skripte gegen echte Systemkommandos testet, muss dasselbe Muster übernehmen,
  nicht `os.environ` erben.
- **Das alte `auth-users`-Credential/Keyring ist vollständig entfernt** (bestätigt 2026-08-09,
  read-only geprüft) — die Laufzeit liest ausschließlich über `UserDirectory`/`auth.sqlite3`.
- **`GET /api/v1/spaces` hat keinen UI-Aufrufer mehr** (seit der Übersichtsseite in Step 7b,
  `init()` geht `/me` → `/meta` → `/overview`) — der Endpunkt bleibt Teil des Vertrags und
  getestet, nur eben nicht mehr von der eigenen Oberfläche benutzt.

---

## 3 Was P6 vom Code erbt — Verweise, keine Kopien

| Was | Wo |
|---|---|
| Alle 31 gelockten Entscheidungen P5-A–P5-AE | `docs/concepts/phase5_ui_plan.md` §0.5 |
| Datenmodell `auth.sqlite3` Schema 2 | `authserver/store.py` — Schema ist dort, nicht im Plan |
| REST-API-Vertrag `/api/v1/*` | `webui/api.py`, `webui/serializers.py` |
| Sicherheits-Header/CSP der UI (getrennt von der OAuth-Seite) | `webui/security.py :: ui_security_headers()` |
| Designsystem — Tokens, Typografie, Layout | `docs/concepts/phase5_ui_plan.md` §4, **aber §4.1/§4.3 vom Plan-Wortlaut abweichend** (siehe unten) |
| Betriebsrunbooks (Deploy/Rollback/Auth-Backup/Migration) | `phase5_ui/CLAUDE.md`, `phase5_ui/scripts/` |
| Was live tatsächlich funktioniert hat | `docs/concepts/P5_ABNAHME_2026-08-09.md` |
| Sicherheitsbefund-Historie S1–S10/O1–O2 | `phase4_auth/CLAUDE.md`s Befundtabelle (lebt dort, nicht in P5) |

**Designsystem-Revision, nicht im 📕-Plan nachgezogen (bewusst — Snapshot bleibt Snapshot):**
§4.1 („keine Verläufe/Schlagschatten außer bei Modalen") und §4.3 („Rail = zwei flache Blöcke")
wurden nach Live-Feedback in Step 7b revidiert — Bedienelemente brauchen sichtbare Tiefe, um als
Bedienelemente erkennbar zu sein, und die Rail ist jetzt ein Baum (Übersicht ▸ eigener Space ▸
Ordner ▸ verbundene Spaces) statt zweier Ebenen. Wer aus dem Plan-Dokument ein Folgeprojekt
ableitet, sollte `phase5_ui/CLAUDE.md`s Step-7b-Zeile lesen, nicht §4.1/§4.3 wörtlich nehmen.

---

## 4 Offene Entscheidungen für die P6-Planung

Diese gehören in die Q&A-Runde **vor** dem Plan, nicht in die Implementierung.

### 4.1 F1/F2 — Subspaces, Shared Spaces, vollständiges Löschen

Aus Live-Feedback (Step 8b), bewusst nicht in P5 umgesetzt. **Drei unabhängige
Teilentscheidungen, keine gemeinsame:**

1. **F1a — eigener Space standardmäßig nur für den Nutzer selbst + dessen Connectoren lesbar**
   (statt „von jedem lesbar wie heute"). Eine **Verschärfung** der Default-Leserechte, verletzt
   **keine** Hard Rule (Rule 4 verbietet Cross-Space-*Writes*, nicht das Verengen von Reads).
   Vertretbar als eigener, kleiner Schnitt. Fasst `mcpserver/permissions.py` an (P5-B tabu für
   P5, nicht für P6).
2. **F1b — ein „shared Space", in dem alle unabhängig volle Rechte haben.** Kollidiert
   **frontal** mit Hard Rule 4 („no exceptions"), fasst `tools.py`+`permissions.py` an und
   ändert das Vertrauensmodell, auf dem `<untrusted_content>` beruht. **Kein Ad-hoc-Umsetzung
   in P6 ohne eigene Grundsatzentscheidung.** Echte Unterordner (unabhängig von Rechten gedacht)
   gehören aus demselben Grund hierher, nicht zu einer Tag-basierten Notlösung — ein Tag hat
   keine eigene Identität, und sobald Ordner potenziell Rechtegrenzen tragen sollen, ist ihr
   natürlicher Ort ein echtes Verzeichnis in `storage/`.
3. **F2 — vollständiges Löschen.** Plan §0.5 nennt es explizit draußen, `storage.store.Store`
   hat keine Lösch-Methode. Als Antwort auf F2 wurde bei derselben Gelegenheit eine
   **Archiv-Neugestaltung** vorgeschlagen (Gruppierung nach Datum/Thema für einen „aufgeräumten"
   Eindruck ohne echtes Löschen) — ebenfalls auf eine spätere Phase verschoben, keine
   Ad-hoc-Umsetzung.

### 4.2 `patch_item` — Werkzeug-Ergonomie

Feedback aus dem echten Betrieb (2026-08-08, eine arbeitende Claude-Instanz über den echten
Connector): `update_item` ersetzt immer den kompletten Body — eine Drei-Zeilen-Korrektur an
einem großen Dokument zwingt zum Komplett-Rewrite, teuer und riskant. Konkreter Gegenvorschlag:
`patch_item(item_id, version, old_text, new_text)`, hart fehlschlagend wenn `old_text` nicht
genau einmal im Body vorkommt — dieselbe Philosophie wie die `version`-Pflicht in Hard Rule 3.
Berührt `mcpserver/tools.py` (P5-B tabu, Akzeptanzkriterium 18 verlangt dort einen leeren Diff)
— kein Ad-hoc-Fix, gehört in denselben Zuschnitt wie F1/F2.

### 4.3 Client-Surface-Logging

Welche Claude-Oberfläche (claude.ai/Desktop vs. Claude Code) einen `/mcp`-Request stellte — soll
ins Log, nicht in die UI. Nikinger-Entscheidung 2026-08-07: **kein Ausschluss** von Claude Code
als Nutzer des produktiven Connectors (dieselbe Autorisierung wie claude.ai-Web/Desktop-Zugriff,
der OAuth-Bearer unterscheidet nicht *welche* Oberfläche, nur *welcher Space*). Naheliegender Ort
bei Umsetzung: derselbe Request-Log-Pfad, der schon Bearer-Requests protokolliert
(`phase2_mcp/mcpserver`, `test_request_log.py`), vermutlich über den `User-Agent`-Header — bei
Umsetzung zu verifizieren, ob MCP-Clients den zuverlässig genug setzen, nicht anzunehmen.

### 4.4 O2 — `clients`/`token_families` werden nie abgeräumt

Geerbt aus Phase 4, weiterhin offen. Beobachtung aus dem echten Betrieb: 35 DCR-Registrierungen
in einer Woche, Fabians neun Token-Familien vom 30.07. stehen bis heute unwiderrufen in der DB.
Kein Sicherheitsrisiko (widerrufene/abgelaufene Zeilen sind wirkungslos), aber unbegrenztes
Zeilenwachstum. Kandidat für einen kleinen eigenen Schnitt, nicht zwingend P6-Kernscope, aber
vorzumerken.

### 4.5 Ein offener Plan-Widerspruch, nicht durch die Abnahme aufgelöst

`phase5_ui_plan.md` Step 9 Punkt 3 verlangt für Fabian eine „frische Einladung"; §2.6
(Migrationsrunbook) beschreibt an anderer Stelle desselben 📕-Dokuments stattdessen eine reine
Credential-Migration ohne neue Einladung. **Gelebt wurde der Step-9-Weg** (frische Einladung,
Fabians alter Account wurde dabei zurückgesetzt) — ohne Auswirkung auf die Abnahme selbst
(Zeile 17 verlangt nur „beide nutzen UI und Connector am selben Tag"), aber als
Plan-Inkonsistenz nicht aufgelöst. Für den nächsten Plan-Review vormerken, kein Blocker.

### 4.6 Doku-Register-Mislabel (kosmetisch, im Abschluss-Commit bereits korrigiert)

`phase5_ui/CLAUDE.md`s Modultabelle (Step 9) und der zugehörige Session-Block bezeichneten den
Abschluss der Inter-Variable-Font-Arbeit (Lizenz, Subsetting, Dateigröße, Cache-Header) als
„schließt V27". Laut dem `[VERIFY]`-Register in `phase5_ui_plan.md` §8 ist das tatsächlich
**V31** (Font) — V27 bezeichnet die `permissions.py`-Klassennamen, ein separates, ebenfalls
korrekt geschlossenes Item aus Step 5. Ein reiner Zahlendreher zwischen zwei bereits erledigten
Einträgen, keine inhaltliche Lücke — **im selben Commit wie dieses Dokument in
`phase5_ui/CLAUDE.md` korrigiert** (datierte Korrekturnotiz dort), kein P6-To-do mehr.

---

## 5 `[VERIFY]`-Bilanz

### 5.1 Aus Phase 5 (V27–V38)

| # | Was | Ergebnis |
|---|---|---|
| V27 | `permissions.py`-Klassen-/Methodennamen (`OwnSpaceWritable`, `can_read`, `can_write`) | **Aufgelöst** (Step 5) — als geteilte Instanz für MCP-Tools und REST-API verwendet |
| V28 | `cryptography`-Version, exakt gepinnt | **Aufgelöst** (Step 2) — `49.0.0`, gepinnt in `phase4_auth/pyproject.toml` |
| V29 | QR-Bibliothek | **Aufgelöst** (Step 4) — `segno==1.6.6`, exakt gepinnt |
| V30 | Herkunft/Größe der Passwort-Blocklist | **Aufgelöst** (Step 4) — `SecLists`s `10k-most-common.txt`, MIT, 10.000 Einträge/73 KB |
| V31 | Inter-Variable: Lizenz, Subsetting, Dateigröße, Cache-Header | **Aufgelöst** (Step 6) — 34,7 KB, im Code fälschlich als „V27" bezeichnet, siehe §4.6 |
| V32 | Reale `pytest`-Ausgangszahl nach dem Rückbau | **Aufgelöst** (Step 0) — 333 |
| V33 | Anthropic-Connector-Doku erneut gegenlesen (Nachfolger V14) | **Nicht bearbeitet.** Kein Session-Block erwähnt einen erneuten Lesedurchgang — plausibel, weil P5 keine neue OAuth-Client-Fläche baute (Block A ist Nutzerverwaltung, nicht Connector-Registrierung), aber **nicht explizit geprüft und geschlossen**. Echt offen für P6, falls dort die Connector-Seite nochmal berührt wird |
| V34 | `README.md` im aktuellen Stand lesen vor Korrektur | **Aufgelöst** (Step 0 C) |
| V35 | `dev_install.sh` nimmt `phase5_ui/` ohne Änderung auf | **Aufgelöst** (Step 3) |
| V36 | Tailscale Serve/Funnel — getrennter Port für Staging | **Aufgelöst** (Step 8) — dann Staging wieder abgeschaltet (§2), die Erkenntnis selbst bleibt gültig |
| V37 | Exakte Abschnittsüberschriften in `docs/INDEX.md` | **Faktisch erledigt, nie explizit als „geschlossen" vermerkt.** Step 0 C legte die Überschrift „Active phase (5 — Web-UI)" tatsächlich an; kein Session-Block nennt V37 namentlich. Kleine Doku-Hygiene-Lücke, kein Risiko |
| V38 | Reale Zeilennummern der Plan-Anker (Nachfolger V24) | **Laufend angewendet, kein Einzelabschluss vorgesehen.** Mehrmals real gegriffen — der §1.2-Zirkel (Step 4), der §1.5-Routentabellen-Widerspruch (Step 6), der §2.6/Step-9-Widerspruch (§4.5 oben) sind genau die Fälle, die dieser Marker mahnt zu prüfen statt blind zu übernehmen |

### 5.2 Geerbt aus Phase 4 — Stand jetzt

| # | Was | Stand |
|---|---|---|
| V10 | Größenbudget `search_items`/UI-Listen | **Aufgelöst** (Step 8, `ui_budget.py`) — alle fünf Messgrößen im Zielkorridor |
| V11 | MCP-Revision 2026-07-28 | überholt durch V25 (Phase 4) — eigene Mini-Phase, unverändert nicht begonnen |
| V12 | Datenlimit des Mobilfunk-Uplinks | **weiterhin offen** — nie bewertet, trotz P5s zusätzlichem Volumen (Assets-Seam, Zähler-Polling alle 20s). Kein beobachtetes Problem, aber auch keine Messung |
| V13 | `diagnose.sh`-Grep gegen echtes `tailscale funnel status` | **Aufgelöst seit Phase 4** (2026-07-28) — P5 Step 8 hat nur eine **Doku-Drift** korrigiert (`phase3_edge/CLAUDE.md` führte denselben Sachverhalt an zwei Stellen widersprüchlich), keine neue Prüfung nötig |

### 5.3 Neu aus Phase 4 (V25) — weiterhin unberührt

**FastMCP 4 / MCP-Revision 2026-07-28** bleibt eine eigene, unbegonnene Mini-Phase (P5-C) —
bewusst nicht mit P5 gebündelt. Für P6 nur relevant, falls die Connector-Seite selbst wieder
angefasst wird.

---

## 6 Was der P6-Chat als Erstes tun sollte

1. **Step 0 wie gehabt:** Verifikationsdurchlauf (`up:`/`down:` auflösbar, Indexzeile je `.md`,
   40-KB-Check, `pytest -q` gegen 576, Push-Stand gegenprüfen — §1 beschreibt den Stand zum
   Zeitpunkt dieses Handovers, das kann sich bis zum P6-Start bereits geändert haben).
2. **In der Q&A klären, bevor geplant wird:** §4.1 (F1/F2 — drei getrennte Teilentscheidungen,
   keine automatisch aus den anderen folgend), §4.2 (`patch_item` — echte `tools.py`-Änderung,
   kein Ad-hoc), §4.3 (Client-Surface-Logging — Umfang: nur Log oder auch UI-Anzeige?), §4.4
   (O2 — eigener kleiner Schnitt oder Teil eines größeren Aufräum-Scopes?).
3. **V33 nachholen**, falls P6 die Connector-/OAuth-Seite berührt (§5.1) — sonst als weiterhin
   offen mitführen, nicht stillschweigend als erledigt behandeln.

**Eine Warnung zum Schluss, weil sie in P4 und P5 mehrfach Zeit gekostet hat:** eine
Doku-Aussage über den Repo-Zustand ist erst wahr, wenn `git status` (oder die reale DB, oder
`journalctl`) sie bestätigt. Diese Phase hat das mehrfach am eigenen Leib erfahren — von der
52-fachen Testsuite-Neustart-Falle bis zum Origin/`Referrer-Policy`-Fund, der sich erst nach
sieben Nachträgen und zwei widerlegten Hypothesen auflöste. Beim P6-Start gilt dasselbe für
**dieses** Dokument: es ist ein 📕-Snapshot vom 2026-08-09. Was danach passiert ist, steht nicht
darin.
