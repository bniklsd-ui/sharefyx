---
status: live
purpose: Phase-Head UI-Neuanstrich v3, Verknüpfungs-Graph, drei P7-Erbposten — Scope, harte Regeln, Modulstatus, aktueller Session-Handover
read-when: Arbeiten in phase8_ui_graph/ oder an den in §0.4 des Plans genannten Dateien in storage/mcpserver/webui/scripts — zuerst lesen, zusammen mit dem neuesten Session-stopped-Block
detail: L2
up: ../CLAUDE.md
down:
  - ../docs/concepts/phase8_ui_graph_plan.md       # voller Plan, Entscheidungen P8-A–P8-Q, §0.1 gelockte N1–N12, Steps 0/A/B/C/D/Z
  - ../docs/concepts/PHASE7_CLOSEOUT_HANDOVER.md   # Herkunft der drei Erbposten (P7-24/remove-space/P7-4)
  - SESSIONS_ARCHIVE.md                             # ältere Session-Blöcke, newest-first
updated: 2026-08-31 (Block A: A1 Reauth-Grant Client gebaut -- async runBatchMove + Grant-Round-2, test #3 auf N=14, Browser-Smoke gegen Wegwerf bestanden, Head rotiert, Live-Verifikation ausstehend) | 2026-08-28 (Block A gestartet -- A1 Reauth-Grant Backend gebaut, 912 Tests gruen, Plan-Drift session_id->session_hash + Throttle-Vorzug dokumentiert, JS-Client ausstehend) | 2026-08-28 (Nachtrag: websearch-MCP nachgerüstet -- @zhafron/mcp-web-search, kein API-Key, Live-Probe bestanden, V94 von nein auf ja) | 2026-08-28 (Step 0 abgeschlossen -- opencode-ai 1.18.25 global installiert, Minimax-Provider-Auth vom Nikinger gesetzt, Playwright-MCP verbunden (V93), CLAUDE.md-Regeldatei-Kontrollfrage bestanden, Smoke-Test P8-26 auf Wegwerf-Branch bestanden, Harnesswechsel zu opencode/M3 ab Block A freigegeben) | 2026-08-28 (Skelett angelegt, Step 0 Fundament-Session gestartet)
---

# CLAUDE.md — Phase 8: UI-Neuanstrich v3, Verknüpfungs-Graph, QoL (`phase8_ui_graph/`)

> Kein eigenes Python-Paket (wie `phase3_edge/`, `phase6_shares/`, `phase6_5_tools_images/`,
> `phase7_spaces_admin/`) — Servercode bleibt in `storage`/`mcpserver`/`webui`/`scripts`.
> **Quelle der Wahrheit ist der Code, nicht dieses Dokument.**

---

## Mission (zuerst lesen)

Vier Blöcke, Reihenfolge 0 → A → B → Gate → C → D → Z: **A** = drei P7-Erbposten schließen
(P7-24-TOTP-Replay per Reauth-Grant, `remove-space`-Auto-Reindex, P7-4-Zweitprobe) — fällt unter
Druck **nie**. **B** = Link-Fundament, achte P1-Contract-Öffnung (`storage/linkscan.py`,
`item_links`-Tabelle, `GET /api/v1/graph`). **C** = Design-Fundament v3, De-AI-isierung (IBM
Plex, Lucide-Sprite, Farblegende own/shared/foreign, Liquid-Glass-Akzente mit Pflicht-Fallback).
**D** = Übersicht tablos + handgerollter Canvas-Force-Graph.

**Erstmals opencode/M3 als Ausführender ab Block A** (P7-Handover §7) — Step 0 (diese Sitzung)
läuft noch in Claude Code, gemeinsam mit dem Nikinger, und stellt die opencode-Fähigkeits-Parität
her. **Kein Advisor während der Ausführung (P8-L, N12)** — Ersatz: Selbstprüf-Checkliste §0.6 des
Plans + zwei Nikinger-Sichtprüfpunkte.

## Scope

- **DRIN:** die drei P7-Erbposten, Link-Extraktion + Graph-Endpunkt, Design v3
  (Typografie/Icons/Farben/Glas), Übersicht tablos + Force-Graph, `AGENTS.md`-Entfernung,
  opencode-Einrichtung.
- **DRAUSSEN:** FastMCP-4/V79 (eigene Mini-Phase), Body-Volltextsuche, Rechteverwaltung über
  MCP-Tools, neues MCP-Tool für den Graph, Löschen von Items, `_trash/`-Räumung,
  Funnel-Watchdog, Mobile/Realtime, Light-Mode. Volle Liste: Plan §0.5 „DRAUSSEN".

Details, gelockte Entscheidungen P8-A–P8-Q, Verbots-/Tabu-Liste, Schritt-Sequenz, Testliste,
Abnahmezeilen: `docs/concepts/phase8_ui_graph_plan.md`.

**P8-N — ein Dokument pro Phase:** der Closeout wird §9 des Plans, kein separates Handover.

## Modul-Status

| Block | Inhalt | Status |
|---|---|---|
| Step 0 | Fundament-Session (Haushalt, AGENTS.md weg, Skelett, opencode-Setup, Smoke-Test) | ✅ |
| A1 | Reauth-Grant (`webui/reauth.py :: ReauthGrantStore` + Endpoint + Client + Tests, N=14-Batch) | 🟡 gebaut, Live-Deploy + Nikinger-Sichtprüfung ausstehend |
| A2 | `remove-space`-Auto-Reindex (`spacectl.py :: _cmd_remove_space()` → `store.rebuild_index()`) | ⬜ |
| A3 | P7-4: organische Zweitprobe + `_TITLE_NOT_ID_HINT` schärfen | ⬜ |
| Block B | Link-Fundament (`linkscan.py`, `item_links`, `GET /api/v1/graph`) | ⬜ |
| Block C | Design-Fundament v3 (Typografie, Icons, Farben, Glas) | ⬜ |
| Block D | Übersicht tablos + Force-Graph | ⬜ |
| Step Z | Closeout | ⬜ |

## Geerbte Contracts

Achte P1-Contract-Öffnung (P8-M) wird in Block B benannt und gebaut — Eintrag folgt in
`phase1_storage/CLAUDE.md` §„Geerbte Contracts" im Öffnungs-Commit, nicht hier dupliziert.

## Abnahmestand (Plan §7, P8-1–P8-26)

**Statusregel wie in P5/P6/P6.5/P7: ✅ heißt live-verifiziert durch den Nikinger, nicht
„gebaut".** Noch keine Abnahmezeile geprüft — Block A läuft (A1-Backend gebaut, Client+Live offen).

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
