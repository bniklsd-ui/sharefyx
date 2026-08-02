---
status: live
purpose: Regeln, Konventionen, Arbeitsweise und aktueller Stand des Space-Servers — wird jede Session automatisch geladen
read-when: immer, vor jeder Aktion in diesem Repository
detail: L2
up: docs/INDEX.md
down:
  - ROADMAP.md                          # Phasenplan + Status je Phase
  - docs/INDEX.md                       # L0-Karte aller .md
  - phase5_ui/CLAUDE.md                 # aktive Phase
updated: 2026-08-02
---
# CLAUDE.md — Project Instructions

> Read this file before doing anything in this repository.
> It is the single source of truth for project rules, conventions, and current state.

---

## What this project is

Ein **geteilter Kontext-Space-Server** für zwei Personen (Nikinger + Kollege) und deren
Claude-Instanzen. Notizen und Aufgaben liegen als Markdown-Dateien mit YAML-Frontmatter auf
einer Heim-VM; Claude greift über einen **Remote-MCP-Server** (Custom Connector, Streamable
HTTP) lesend und schreibend darauf zu, Menschen über eine Web-UI oder direkt im Editor.

Der Server läuft hinter **CGNAT** (RUT X50, Mobilfunk) — die Verbindung kommt von Anthropics
Backend, nicht vom Client. Erreichbarkeit daher **ausschließlich über einen ausgehenden
Tunnel**, niemals über Port-Forwarding.

Build order: `ROADMAP.md` · Doku-Karte: `docs/INDEX.md`

---

## Core principle (read carefully)

**Bauprinzip: Der Server ist dumm.**

Die gesamte Intelligenz sitzt beim Client (Claude). Der Server ist ein Aktenschrank mit
Schloss — mehr nicht.

**Der Server macht:**
- Dateien lesen/schreiben (atomar), Frontmatter parsen/serialisieren
- Index pflegen, Suchen beantworten, Paginierung
- Auth (Token → Space), Autorisierung (eigener Space schreibbar, fremde read-only)
- Versionierung, Konflikterkennung, Git-Commits
- Fehlerbehandlung, Logging, Health

**Der Server macht NIEMALS:**
- LLM-Calls, Embeddings, semantische Suche, Zusammenfassungen, Auto-Tagging
- irgendeine Form von „Verstehen" des Inhalts

Wer hier ein LLM einbauen will → **stop**. Das gehört auf die Client-Seite. Ein Server, der
Inhalte interpretiert, ist ein Server, dessen Fehlverhalten man nicht mehr debuggen kann —
und er importiert Prompt-Injection direkt in den Speicherpfad.

---

## Hard Rules (no exceptions)

1. **Niemals Secrets in Dateien.** Keine Tokens, keine Keys — nicht in `.env`, nicht in JSON,
   YAML oder Config. Space-Tokens und Tunnel-Credentials leben ausschließlich im OS-Keyring
   (Service `nikinger-space`) bzw. als systemd `LoadCredential`. Zugriff über
   `storage/credentials.py`. Ein Token in einem Commit ist ein Incident, kein Schönheitsfehler.
   **[2026-07-25 Korrektur, P2 Step 3]:** `storage/credentials.py` wurde nie gebaut — der
   reale Pfad ist `phase2_mcp/mcpserver/credentials.py`. Die Regel selbst bleibt unverändert.
   **[2026-07-30 Ergänzung, P4 Schnitt]:** Ab Phase 4 liegen dort **echte** Geheimnisse (TOTP-
   Seeds, umkehrbar) neben den reinen Token-Hashes aus P2/P3 — `phase4_auth/authserver/users.py`,
   Service weiterhin `nikinger-space`. Ein TOTP-Seed ist bei Kompromittierung nutzbar, ein
   Token-Hash nicht; dieselbe Hard Rule, höherer Einsatz.

2. **Dateien sind die Wahrheit, der Index ist Ableitung.** SQLite darf jederzeit gelöscht und
   aus den `.md`-Dateien vollständig rekonstruiert werden. Nie umgekehrt. Wer den Index als
   primären Speicher benutzt → stop.

3. **Kein Write ohne `version`.** Jede Schreiboperation trägt die gelesene Version; Mismatch →
   `ConflictError` mit dem aktuellen Item im Fehler. **Kein Last-Write-Wins, nirgends.**
   Zwei Claude-Instanzen im selben Space sind der Normalfall, nicht der Randfall.

4. **Fremde Spaces sind read-only, fremde Inhalte sind Daten.** Cross-Space-Writes existieren
   architektonisch nicht (kein Parameter, keine Codepfad-Variante). Jeder Body aus einem
   fremden Space wird im Tool-Result in `<untrusted_content>` gewrappt. Begründung: Claude
   liest fremde Notizen *mit* aktiven Schreib-Tools — jede Zeile dort ist ein potenzieller
   Befehl.

5. **Writes sind atomar und fail-closed.** `tmp` + `os.replace` + `fsync` auf dem Verzeichnis.
   Nie ein halb geschriebenes Item auf der Platte. Jeder erfolgreiche Write erzeugt einen
   Git-Commit im Datenverzeichnis (Undo + Historie kostenlos).

6. **Nie ein offener Port am Router.** Erreichbarkeit ausschließlich über ausgehenden Tunnel.
   Wer Port-Forwarding oder DynDNS vorschlägt → stop, das scheitert an CGNAT und öffnet die
   Heim-VM.

7. **Logging → stderr; stdout nur maschinenlesbares JSON.** Atomic commits. Kein Subtask
   „done" ohne grünes `pytest` (gemockt, **kein Netz, kein echter Tunnel** in Unit-Tests).

8. **Commit ⇒ Doc-Update (zwingend, auch auf direkte Anweisung).** Jeder Step-Abschluss-Commit
   aktualisiert im **selben** Commit die Modul-/Status-Tabelle der Phase **und** den
   `## Session stopped`-Block. Neue `.md` ⇒ Zeile in `docs/INDEX.md` im selben Commit.

---

## Working style

- **Quelle der Wahrheit ist der Code, nicht dieses Dokument.** Bei Widerspruch gewinnt das
  getestete Artefakt; das Dokument wird sofort mit datierter Korrekturnotiz gefixt.
- **`[VERIFY]`-Marker:** Alles, was gegen den echten Repo-Stand oder eine externe API geprüft
  werden muss, ist so markiert. Bei Ausführung verifizieren, **nie** als gesichert übernehmen.
- **Gelockte Entscheidungen bleiben gelockt.** Widersprechende Evidenz wird ein expliziter
  Befund für den Menschen, nie eine stille Abweichung.
- **Act vs. ask:** reversible, in-scope Schritte selbst ausführen; bei destruktiven Aktionen,
  Scope-Änderungen und Out-of-Scope-Edits stoppen und fragen.
- **Handover für einen kalten Leser schreiben.** Ergebnis zuerst, kein Session-Slang, nächster
  Schritt konkret genug zum Sofortstart.

## Doku-Hygiene (Doc-Layers)

Vollspec: `docs/DOC_LAYERS_CONVENTION.md` (v1, 2026-07-06) — **byte-identische Kopie aus dem
Trading-Bot-Repo**, dort bewusst projekt-agnostisch geschrieben. Sie wird hier **nicht**
projektspezifisch angepasst: zwei Kopien derselben Regel, die sich unterschiedlich entwickeln,
sind schlimmer als eine, die an einer Stelle etwas allgemein formuliert ist. Wer sie ändern
will, ändert sie im Trading-Bot-Repo und kopiert erneut.

Kurzform: **L0** = `docs/INDEX.md` · **L1** = ≤15-Zeilen-Header-Card oben in jedem *lebenden*
Dokument · **L2** = schlanke Bodies, Softcap **≤40 KB** · **L3** = Archive und datierte
Snapshots. Rotationsregel ab Tag 1 scharf: ein Phase-Head trägt **genau einen** aktuellen
`## Session stopped`-Block; der vorherige wandert **verbatim** nach `SESSIONS_ARCHIVE.md`.
Durchführung über `scripts/rotate_session_block.sh <phase_verzeichnis>`, nie von Hand.

> Diese Regel gilt hier ab dem ersten Commit, nicht als späterer Rettungseinsatz. Im
> Trading-Bot-Repo wuchs `phase8_scheduler/CLAUDE.md` auf 211 KB, bevor sie eingeführt wurde.

---

## Current state

**Aktive Phase:** Phase 5 — Web-UI, REST-API und Auth-Selbstverwaltung (`phase5_ui/`, Paket
`webui`) — **🔄 gestartet, 2026-08-02.** Browser-Planungssession abgeschlossen, ausführungsreifer
Plan liegt vor (`docs/concepts/phase5_ui_plan.md`, Entscheidungen P5-A–P5-AE, Steps 0–9, zwei
Blöcke: A = Sicherheit + Auth-Selbstverwaltung, B = REST-API + UI, harter Gate dazwischen).
Herkunft/offene Entscheidungen: `docs/concepts/PHASE4_CLOSEOUT_HANDOVER.md`. Phase-Head:
`phase5_ui/CLAUDE.md`. **Nächster Schritt:** Step 0 (Haushalt, Rückbau der P2-Token-Reste,
Doku-Drift) — läuft.

**Phase 4 — OAuth 2.1 + DCR** (`phase4_auth/`, Paket `authserver`) — **✅
abgeschlossen, 2026-07-30.** Mission erfüllt: der Pfad-Token ist verschwunden, ein eigener
Authorization Server ersetzt ihn (DCR, PKCE, Argon2id + TOTP), Schnitt vollzogen, 16/16
Abnahmezeilen live bestanden. Plan: `docs/concepts/phase4_auth_plan.md` (Entscheidungen
P4-A–P4-R gelockt, Steps 0–7, ausführungsreif — geschrieben ohne frischen Repo-Zugriff, siehe
Plan-Kopf). Herkunft/offene Entscheidungen: `docs/concepts/PHASE3_CLOSEOUT_HANDOVER.md`.
Phase-Head: `phase4_auth/CLAUDE.md`. **[2026-08-02 Nachtrag:]** der formale Phasenabschluss ist
erledigt — `docs/concepts/PHASE4_CLOSEOUT_HANDOVER.md` und die P5-Planungssession liegen vor,
Phase 5 ist gestartet (siehe oben).

**[2026-07-28 Korrektur:** diese Zeile stand hier zwischenzeitlich auf „P4 Step 0+1", obwohl
Step 2 und Step 3 im selben Tag folgten — Drift durch fehlendes Nachziehen dieser Datei bei
Step-Abschluss-Commits, jetzt behoben.**]**

**[2026-07-28 weitere Korrektur, im Step-5-Commit gefunden:** dieselbe Drift-Kategorie trat ein
zweites Mal ein — die vorige Korrektur brachte diese Zeile auf Step 3, aber die Step-4- und
Step-5-Abschluss-Commits zogen sie danach drei Steps lang nicht nach. Root-`CLAUDE.md` ist nicht
die Quelle der Wahrheit für den Phase-Fortschritt (das ist `phase4_auth/CLAUDE.md`), aber diese
Zeile hier muss trotzdem mitlaufen, sonst degradiert Hard Rule 8 zu einer Regel, die nur für den
Phase-Head gilt.**]**

**[2026-07-28 dritte Korrektur, im Step-6b-Commit gefunden:** dieselbe Drift-Kategorie trat ein
drittes Mal ein — der Step-6a-Abschluss-Commit zog diese Zeile nicht nach, obwohl er zwischen
Step 5 und Step 6b lag. Diese Zeile jetzt auf Step 6b gebracht, jeweils bei ihrem eigenen
Abschluss-Commit nachzuziehen, nicht erst wenn die Drift wieder auffällt.**]**
**[2026-07-29:** Step 7 nachgetragen — Code-Vorbereitung fertig, Live-Teile (Provisionierung,
`systemd-creds`, `systemctl restart`, Connector, Abnahmematrix) stehen aus, Sache des
Nikingers.**]**
**[2026-07-29, zweiter Nachtrag:** Der erste Live-Versuch von Runbook-Schritt 4
(`oauth_smoke.py --base-url`) scheiterte 4/4 mit `status=400` — Ursache **Befund S1**:
`SPACE_ALLOWED_HOSTS` ohne `127.0.0.1` lässt das Wurzel-`TrustedHostMiddleware` jede lokale
Anfrage mit `400 Invalid host header` beantworten, der Runbook-Schritt war damit strukturell
unausführbar. Behoben in `local.env.example`/`install_units.sh`/Runbook, **ohne** Servercode zu
ändern; gegen eine Wegwerf-Instanz mit `tmp`-`DATA_ROOT` als 11/11 belegt. Im selben Zug ein
vollständiges Sicherheits-Review von P3+P4: **keine Auth-Umgehung, kein Cross-Space-Leck, kein
Secret-Leak**; sieben kleinere offene Befunde S2–S8 plus Betriebsnotiz O1, bewusst **nicht**
gefixt, bis der Nikinger über die Reihenfolge gegenüber der Abnahmematrix entschieden hat.
Volles Dokument: `docs/concepts/P4_SECURITY_REVIEW_2026-07-29.md`.**]**
**[2026-07-29, dritter Nachtrag:** Live-Abnahme durchgeführt — **12 von 16 Zeilen bestanden**
(Refresh-/Code-Replay live mit echter Token-Familie, Fehlversuchsbremse mit exakter
Sperrzeit-Formel, Rule 4 unter echtem OAuth beobachtet). Bewusst offen: Zeile 9
(Token-Ablauf/Auto-Refresh, nächste Session mit vorbereiteter Anleitung), Zeilen 14/15 (Fabian,
verabredet), Zeile 16 (erst nach dem Schnitt). Zwei kleine Live-Funde behoben (B1: `authctl.py`
braucht `STATE_DIRECTORY` außerhalb von systemd; B2: `abnahme_run.sh` musste `/mcp/` mit
Trailing Slash prüfen, sonst falscher Negativbefund). Protokoll:
`docs/concepts/P4_ABNAHME_2026-07-29.md`.**]**
**[2026-07-30:** Zeilen 14/15 (Fabian) scheiterten zunächst — Login gelang serverseitig sechsmal
in Folge (echte Token-Familien, Passwort+TOTP korrekt), aber Chromium blockierte den `302`-
Redirect zurück zu `claude.ai` lautlos: `form-action 'self'` in der CSP wird gegen das
Redirect-Ziel geprüft, nicht nur gegen das unmittelbare Formular-`action`. Root Cause über einen
DevTools-Screenshot des Nikingers bestätigt, gefixt (`AuthSettings.csp_form_action`, `form-action
'self' https://claude.ai https://claude.com`), Seam-Test `test_redirect_uri_allowed_is_the_only_
matching_path` blieb dabei intakt. **Noch nicht auf `sharefyx-mcp` deployt** — braucht
`systemctl restart`, dann Fabian erneut testen.**]**
**[2026-07-30, zweiter Nachtrag:** Fix deployt, Fabian mit einem Klick erfolgreich verbunden —
er fuhr von sich aus ein vollständiges Sechs-Tool-Protokoll plus zwei Negativtests
(Optimistic-Locking-`conflict`, Cross-Space-`write_denied`), alles bestanden. **14 von 16
Abnahmezeilen live bestanden** — die im Runbook gelockte Terminrisiko-Schwelle ist erreicht:
„14/16 bestanden → 🟡 code-complete, P5 darf beginnen" (Nikinger-Entscheidung 2026-07-28).
Verbleibend: Zeile 9 (eigene Session), Zeile 16 (erst nach dem Schnitt). Details:
`docs/concepts/P4_ABNAHME_2026-07-29.md`, Nachtrag 2026-07-30.**]**
**[2026-07-30, dritter Nachtrag:** Zeile 9 (Access-Token-Ablauf) noch in derselben Session
durchgeführt — kurze TTL via systemd-Drop-in, Connector neu verbunden, ein Aufruf vor und einer
nach Ablauf ohne erneuten Login. DB-Gegenprobe: Refresh lief **on-demand** (erst beim ersten
Aufruf nach Ablauf, kein Hintergrund-Timer), belegt über 14 `access_tokens`-Zeilen derselben
Token-Familie. **15 von 16 Abnahmezeilen live bestanden — einzig verbleibend: der Schnitt
(Runbook-Schritt 8), danach Zeile 16 und der volle ✅-Status.**]**
**[2026-07-30, vierter Nachtrag — Schnitt vollzogen, 16/16, Phase 4 ✅:** der Nikinger hat
Runbook-Schritt 8 live ausgeführt (`SPACE_AUTH_MODE=oauth`, `install_units.sh`, Restart, beide
Pfad-Token widerrufen, `spaces.cred` neu geschrieben, zweiter Restart) — **vor** jeder
Code-Änderung, wie der Plan-Wortlaut verlangt. Claude Code hat das read-only gegenverifiziert,
nicht nur die Session-Zusammenfassung übernommen (Advisor-Vorgabe dieser Session, nach einem
Context-Compaction-Verlust der Details): `systemctl cat sharefyx-mcp` → `SPACE_AUTH_MODE=oauth`;
`export_space_map.py` → `0 Einträge`, beide Pfad-Token also tot; `curl` gegen die alte
Pfad-Token-URL → `401`; `/health` weiterhin `200` (Dienst gesund, `uptime_s` seit dem Restart
plausibel). **Zeile 16 damit live bestanden, 16/16.** Danach `TokenPathASGI`/`AuthModeASGI` aus
`phase2_mcp/mcpserver/asgi.py`/`app.py` entfernt (der `resolver`-Parameter aus `create_app()`
entfällt ersatzlos mit), `SPACE_AUTH_MODE` auf einen Wert reduziert (`_VALID_MODES=("oauth",)`
— der Plan-Wortlaut „zwei Werte" war ohne frischen Repo-Zugriff geschrieben und ungenau, siehe
`authserver/config.py`-Korrekturnotiz; mit dem Nikinger vorab abgestimmt statt still
abgewichen), `serve.py`s Step-6b-Gate entfernt (`oauth` jetzt immer Pflicht — reversiert eine
gelockte Entscheidung, ebenfalls mit dem Nikinger abgestimmt), `mcp_smoke.py`/`oauth_smoke.py`/
`test_oauth_smoke.py`/`test_app.py`/`test_asgi_bearer.py`/`test_request_log.py` auf echte
Bearer-Token gegen eine temporäre `AuthStore` umgestellt (Pfad-Token-Fakes gab es sonst nirgends
mehr zu bedienen), `test_asgi.py` (nur `TokenPathASGI`) gelöscht, `test_serve.py` (neu, deckt
`serve.py :: main()`s Verdrahtung bis `uvicorn.run()` ab — vorher ungetestet, siehe Advisor-Fund
im Session-Block). `pytest -q` → **347/347 grün** (vorher 353 — die Differenz ist die Nettosumme
aus gelöschten/gekürzten Pfad-Token-Tests minus den zwei neuen `test_serve.py`-Tests, keine
neue Lücke, siehe `phase2_mcp/CLAUDE.md`/`phase4_auth/CLAUDE.md` für die Aufschlüsselung je
Datei). `git diff` auf `tools.py`/`permissions.py`/`server.py`/`storage/` bleibt **leer**
(Akzeptanzkriterium §6.9). `mcp_smoke.py` (12/12) und `oauth_smoke.py` (11/11, In-Process-Modus)
zusätzlich real gegen den vollen Stack gelaufen, nicht nur `pytest` grün behauptet. **Phase 4 ist
damit ✅ — Steps 0–7 vollständig, Abnahmematrix 16/16, Schnitt vollzogen.** Protokoll-Nachtrag:
`docs/concepts/P4_ABNAHME_2026-07-29.md`.**]**
Step 0 (Haushalt, Drift, geerbte Abnahme), Step 1 (Gerüst, Konfiguration,
Kryptobausteine), Step 2 (Passwörter, TOTP, Nutzerakten), Step 3 (Persistenz +
Fehlversuchsbremse — Code-/Refresh-Replay-Tötung nach RFC 9700), Step 4 (Metadaten + dynamische
Registrierung), Step 5 (Autorisierungsfluss — `/oauth/authorize`, `/oauth/token`,
TOTP-Replay-Schutz, Enumerationsschutz), Step 6a (Resolver, Bearer-Auflösung,
`create_app()`-Verdrahtung), Step 6b (`oauth_smoke.py` 11/11, `OAuthLogASGI`,
`serve.py`-`SPACE_AUTH_MODE`-Gate — Step 6 damit vollständig) und Step 7 (`authctl.py`,
Unit-Umzug nach `phase4_auth/systemd/`, `oauth_smoke.py --base-url`, Live-Abnahme 16/16, Schnitt,
`TokenPathASGI`-Entfernung) sind durchgelaufen — **alle acht Steps ✅.** Kritischer Fund in
Step 0: ein nie widerrufener Keyring-Token
für einen dritten, seit P2-B2 umbenannten Space (`nikinger`) — live und schreibfähig, aber ohne
zugehöriges Verzeichnis unter `DATA_ROOT`.
Nikinger-Entscheidung: widerrufen (Keyring), Export + `sudo systemctl restart sharefyx-mcp`
nachgezogen (2026-07-28 14:12) — live gegen `diagnose.sh` und `export_space_map.py` bestätigt,
Token auch im laufenden Dienst tot. Details: `docs/concepts/PHASE3_CLOSEOUT_HANDOVER.md` §5
Nachtrag. Details zu Step 2–6b: Session-Blöcke in `phase4_auth/CLAUDE.md` bzw.
`phase4_auth/SESSIONS_ARCHIVE.md`.

**Phase 3 — Exposure & Betrieb** (`phase3_edge/`, kein eigenes Python-Paket — Servercode bleibt
in `mcpserver`): 🟡 **code-complete, nicht vollständig live-bewiesen** — inzwischen 12 von 13
Abnahmezeilen live bestanden (Ursprungsstand 10/13: `docs/concepts/P3_ABNAHME_2026-07-27.md`).
Zeilen 6 (Reboot), 12 (Backup-Timer-Lauf) und 13 (Restore-Nachweis) sind laut
Nikinger-Entscheidung an P4 vererbt, nicht vergessen — Zeile 12 ist (P4 Step 0) durch einen
realen Timer-Lauf erfüllt. **[2026-07-29 Ergänzung:]** Zeile 6 ist jetzt ebenfalls ✅ — ein
unbeabsichtigter Reboot der VM (Neustart des Windows-Hosts des Nikingers) lieferte genau den
in der Nikinger-Entscheidung vom 2026-07-27 vorgesehenen Prüffall; Belege (Boot-Zeit,
Auto-Start ohne Handgriff, echter Tool-Traffic danach, unveränderte Funnel-URL, live `HTTP
200`) in `phase3_edge/CLAUDE.md`, Session-Block 2026-07-29. Einzig Zeile 13 (Restore-Nachweis,
braucht ein frisches Bundle) blockiert noch den Wechsel von 🟡 auf ✅. Formaler Abschluss-Handover an P4:
`docs/concepts/PHASE3_CLOSEOUT_HANDOVER.md`. Plan: `docs/concepts/phase3_edge_plan.md`
(Entscheidungen P3-A–P3-N gelockt, Steps 0–7). Phase-Head: `phase3_edge/CLAUDE.md`.

**Phase 2 — MCP-Server** (`phase2_mcp/`, Paket `mcpserver`): ✅ **abgeschlossen,
live-verifiziert seit 2026-07-26** — Quick-Tunnel-Probe + vollständige Adapter-Abnahme über den
echten Custom Connector durch den Nikinger, 21/21 Prüfungen, siehe
`docs/concepts/P2_ADAPTER_ABNAHME_2026-07-26.md`. Claude liest und schreibt über einen lokalen
`fastmcp`-Server auf den P1-Storage-Kern — Token→Space-Auflösung, sechs Tools,
`<untrusted_content>`-Wrapping fremder Bodies. Formaler Abschluss-Handover an P3:
`docs/concepts/PHASE2_CLOSEOUT_HANDOVER.md`. Plan: `docs/concepts/phase2_mcp_plan.md`
(Entscheidungen P2-A–P2-N, Steps 0–7). Phase-Head: `phase2_mcp/CLAUDE.md`.

**Phase 1 — Storage-Kern** (`phase1_storage/`, Paket `storage`): ✅ **abgeschlossen,
live-verifiziert.** Alle acht Module (Steps 0–7), 68 Tests grün (70 bei Phasenabschluss, minus
zwei bei Entfernung toten Codes in P2 Step 0 — siehe `phase1_storage/CLAUDE.md`) —
Frontmatter/Modelle, atomarer Datei-Store, SQLite-Index, Versionierung + Konfliktbehandlung,
Git-Commit je Write, Query-Layer, `space_cli.py` als Beweis. Der Nikinger hat den Lauf gegen den
echten `DATA_ROOT` (`/home/savefyx/savefyx-data`) selbst ausgeführt (2026-07-25, Hard Rule: kein
Test gegen den echten DATA_ROOT durch Claude Code). Details + Transkript:
`phase1_storage/CLAUDE.md`, Session-Block. Plan: `docs/concepts/phase1_storage_plan.md`
(Entscheidungen A–H gelockt, Steps 0–7). Die dort definierten Frontmatter-Felder und
`Store`-Signaturen sind ab jetzt Contract für P2 (drei einmalige, freigegebene Erweiterungen in
P2 Step 2 — siehe P2-Plan §0.4 Punkt L).

**Gelockte Rahmenentscheidungen (Nikinger, 2026-07-24, Browser-Planung):**

| # | Thema | Lock |
|---|---|---|
| R1 | Plan/Ausführung | Planung im Browser-Chat, Ausführung in Claude Code — wie im Trading-Bot-Projekt. |
| R2 | Plan-Tier | Beide Nutzer auf **Claude Pro**. Custom Connectors sind auf Pro verfügbar; jeder fügt seinen Connector selbst hinzu (kein Owner-Gate wie bei Team/Enterprise). `[VERIFY]` bei Ausführung gegen die aktuelle Doku. |
| R3 | Erreichbarkeit | **CGNAT** (RUT X50, Mobilfunk). Start mit **Cloudflare Tunnel** (schnellster Weg zum ersten Erlebnis), Migration auf **VPS + WireGuard** als P3-Option. Der MCP-Server ändert sich dabei nicht. **[2026-07-28 Ergänzung, P4 Step 0]:** Gebaut wurde stattdessen **Tailscale Funnel** (P3-A) — weder Cloudflare Tunnel noch VPS+WireGuard. Die Beschlusslage oben bleibt historisch korrekt stehen; Details zum tatsächlichen Weg: `docs/concepts/phase3_edge_plan.md` §0.4. |
| R4 | Vertraulichkeit | Bewusst akzeptiert: bei Cloudflare Tunnel terminiert Cloudflare TLS und sieht Klartext. **Kein E2E.** Der Server muss lesen können, damit Claude lesen kann — das schließt das Krypto-Modell des `Notizheft_example.html` aus. **[2026-07-27 Ergänzung, P3 Step 0]:** Ab P3 läuft der Weg über Tailscale Funnel; dort terminiert die Node selbst TLS, siehe `docs/concepts/phase3_edge_plan.md` §0.4. Der Relay-Betreiber sieht Notizinhalte damit nicht mehr im Klartext — „kein E2E" bleibt trotzdem richtig, denn Tailscale bleibt vertrauenswürdige Infrastruktur (Koordinationsserver, DNS, Relays). |
| R5 | Auth v0 | Token im Pfad (`/mcp/<token>`), Token = Identität = Space. Ehrlich benannter Kompromiss (Bearer-Passwort in einer URL, landet in Logs). **OAuth 2.1 + DCR ist Phase 4**, nicht optional-für-immer. **[2026-07-30 abgelöst, P4 Schnitt:]** Der Pfad-Token existiert nicht mehr — `TokenPathASGI` ist aus dem Code entfernt, beide Pfad-Token live widerrufen, `SPACE_AUTH_MODE` lässt nur noch `oauth` zu. Der Connector authentifiziert sich seither über OAuth 2.1 + DCR (Passwort + TOTP), siehe P4. |
| R6 | Zweck | **Lernprojekt**, später evtl. Arbeitswerkzeug. Bei Zielkonflikt gewinnt Lerneffekt über Bequemlichkeit — außer bei Safety/Secrets, dort gewinnt immer die sichere Variante. |

**Noch nicht entschieden (bewusst offen, für spätere Planungssessions):**
- *(aktuell keine offenen Punkte auf dieser Ebene — der einzige verbliebene, „Web-UI: Neubau vs.
  Adaption", ist mit P5-V entschieden, siehe Korrekturnotiz direkt darunter.)*

**[2026-08-02 Korrektur, P5-Planungssession]:** der bis dahin offene Punkt „Web-UI: Neubau gegen
die REST-API vs. Adaption des `Notizheft_example.html`" ist entschieden — **Neubau mit Ernte**
(Entscheidung P5-V, `docs/concepts/phase5_ui_plan.md` §0.5): Layout-Ideen sowie
`sanitizeHtml`/`markdownToHtml` werden übernommen, die clientseitige Vault-Verschlüsselung
(unvereinbar mit R4), `localStorage`/IndexedDB und `connect-src 'none'` werden verworfen.

**[2026-07-28 Korrektur, P4 Step 0]:** Der Punkt „Ob der Kollege einen eigenen Server-Prozess
oder nur einen eigenen Space bekommt" stand hier fälschlich noch als offen. Das ist seit P3-G
entschieden und live bewiesen: **ein Prozess, ein Space je Person.** Zwei Spaces existieren real
(`niklas`, `fabian`), beide über denselben `sharefyx-mcp.service`.
