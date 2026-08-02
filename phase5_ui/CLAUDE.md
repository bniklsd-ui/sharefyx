---
status: live
purpose: Phase-Head Web-UI, REST-API, Auth-Selbstverwaltung — Scope, harte Regeln, Modulstatus, aktueller Session-Handover
read-when: Arbeiten in phase5_ui/ oder an den in P5-B genannten Dateien in authserver/mcpserver — zuerst lesen, zusammen mit dem neuesten Session-stopped-Block
detail: L2
up: ../CLAUDE.md
down:
  - ../docs/concepts/phase5_ui_plan.md             # voller Plan, Entscheidungen P5-A–P5-AE, Steps 0–9
  - ../docs/concepts/PHASE4_CLOSEOUT_HANDOVER.md   # Herkunft der offenen Entscheidungen §4.1–§4.5, [VERIFY]-Bilanz V14–V26
updated: 2026-08-02
---

# CLAUDE.md — Phase 5: Web-UI, REST-API, Auth-Selbstverwaltung (`phase5_ui/`)

> **Menschen benutzen das System ohne SSH und ohne Editor.** Zwei getrennt beweisbare Dinge:
> ein Mensch kann sein Konto selbst verwalten (Einladung, Passwort/TOTP/Recovery, ohne Neustart),
> und ein Mensch kann Notizen/Aufgaben im Browser lesen und schreiben, über eine REST-API auf
> demselben Storage-Kern wie die sechs MCP-Tools.
> **Quelle der Wahrheit ist der Code, nicht dieses Dokument.**
> Vollständiges Design + alle 30 gelockten Entscheidungen (P5-A–P5-AE) + Steps 0–9:
> `../docs/concepts/phase5_ui_plan.md`.

## Mission (zuerst lesen)

Der Härtetest der Phase ist nicht die Oberfläche, sondern **Block A vor Block B**: ein System,
in dem ein Mensch sein Passwort selbst setzen kann, ist auch ohne schöne Oberfläche ein
Werkzeug. Eine schöne Oberfläche auf einem Konto, das nur per SSH existiert, ist es nicht. Unter
Druck fällt Block B (REST-API/UI) weg, nicht Block A (Sicherheit/Selbstverwaltung) — dieselbe
Roadmap-Regel („die späteste Phase fällt weg, nie eine frühere Regel") eine Ebene tiefer.

## Bauprinzip (Projekt-Kernprinzip)

„Der Server ist dumm." **Phase 5 enthält KEINE AI**, kein serverseitiges Rendern fremder Bodies
zu HTML (P5-Y), kein LLM, keine Zusammenfassung, kein Auto-Tagging.

## Scope (Kurzform, Details: Plan §0.5 P5-A–P5-AE)

- **DRIN:** Sicherheitsbefunde S2–S8 vollständig schließen (P5-S), Auth-Datenmodell in
  `auth.sqlite3` (Schema 2: `users`/`invites`/`recovery_codes`/`ui_sessions`), eigene
  Cookie-Session für die UI (kein OAuth, P5-D), REST-API `/api/v1/*` über denselben Storage-Kern,
  statische Single-File-UI unter `/ui` (kein Build-Step, P5-T), Deploy/Rollback/Staging/
  Auth-Backup (P5-AB/P5-R).
- **DRAUSSEN:** zweites Dateiformat/Anhänge (Seam ja, Implementierung nein, P5-Z/P5-AA),
  FastMCP-4-Umstieg/CIMD/DPoP (P5-C), Mobilversion (P5-W), Realtime/WebSocket, Löschen (bleibt
  `status: archived`), Rechte zwischen Spaces jenseits von Rule 4.

## Harte Regeln dieser Phase (nicht verhandelbar)

- Alle Hard Rules aus Root-`CLAUDE.md` gelten unverändert.
- **P5-B — Berührungsfläche.** P5 darf `authserver/` und `mcpserver/{app,asgi}.py` anfassen.
  **Tabu:** `storage/`, `mcpserver/tools.py`, `mcpserver/permissions.py`, `mcpserver/server.py`
  — `git diff` darauf ist am Phasenende leer (Akzeptanzkriterium 18). `webui` darf genau **ein**
  Symbol aus `mcpserver` importieren (`permissions.OwnSpaceWritable`), sonst nichts — ein Test
  hält das fest (`test_webui_imports_exactly_one_mcpserver_symbol`).
- **P5-D/P5-F — zwei getrennte Auth-Wege, architektonisch, nicht per `if`.** `/mcp` akzeptiert
  niemals Cookies (nur `Authorization: Bearer`). `/api`/`/ui` akzeptieren niemals Bearer-Token
  (nur Cookie-Session). Beide Richtungen sind Tests (Akzeptanzkriterium 19).
- **P5-G — UI-Session ≠ OAuth-Consent.** `/oauth/authorize` liest niemals Cookies und verlangt
  bei jeder Connector-Autorisierung Passwort **und** TOTP, auch bei bestehender UI-Sitzung.
- **P5-Y — fremde Bodies werden nie serverseitig zu HTML gerendert.** Die API liefert reinen
  Text; Rendering + Sanitizing passiert ausschließlich im Browser.
- **Rotationsregel ab Tag 1.** Dieser Head trägt **genau einen** Session-Block. Beim Anlegen
  eines neuen wandert der bisherige **verbatim** nach `SESSIONS_ARCHIVE.md` — Durchführung über
  `scripts/rotate_session_block.sh phase5_ui`, nie von Hand.
- **Commit ⇒ Note-Update, im selben Commit** (Hard Rule 8): Modul-Tabelle unten + Session-Block.

## Die gelockten Entscheidungen (P5-A – P5-AE) — Kurzform (Details: Plan §0.5)

Ein Phasenschnitt, zwei Blöcke, harter Gate dazwischen (A) · Berührungsfläche `authserver`/
`mcpserver/{app,asgi}` (B) · MCP-Revision 2026-07-28 bleibt eigene Mini-Phase (C) · eigene
Cookie-Session, kein OAuth für die UI (D) · `__Host-sfx_session`, Idle 12h/Absolut 7d (E) ·
`/mcp` nie Cookies, `/api`+`/ui` nie Bearer (F) · UI-Session kürzt Consent nicht ab (G) ·
Double-Submit-CSRF + Herkunftsprüfung (H) · Nutzerakten wandern in `auth.sqlite3` (I) ·
TOTP-Seeds AES-256-GCM verschlüsselt, drittes Credential `auth-dek` (J) · Einladungstoken/
Recovery-Codes/Session-IDs gehasht, nicht Argon2id (K) · `UserDirectory` liest live, kein
Neustart mehr nötig — schließt O1 (L) · Erstvergabe über Einmal-Einladung (M) · zehn
Recovery-Codes ersetzen den TOTP-Faktor (N) · Passwortpolitik 12–128 Zeichen + lokale Blocklist
(O) · Re-Auth bei sicherheitsrelevanten Änderungen (P) · Passwortwechsel widerruft alle
Token-Familien + fremde UI-Sessions (Q) · eigenes verschlüsseltes Auth-Backup (R) · S2–S8
vollständig schließen (S) · statische Single-File-UI, kein Build (T) · Markdown-Textarea +
Formatierhilfen, kein WYSIWYG (U) · Notizheft-Neubau mit Ernte (V) · 16:9-Desktop first, keine
Mobilversion (W) · Dunkel-first, Apple-Formensprache vor „Liquid Glass" (X) · fremde Bodies nie
serverseitig gerendert (Y) · Format-Seam ohne Implementierung (Z) · Anhänge draußen (AA) ·
Release-Verzeichnisse + Health-Gate + Staging, kein Blue/Green (AB) · Blue/Green als Seam (AC) ·
Messung statt Schätzung (`ui_budget.py`, AD) · gemeinsame Live-Abnahme, beide Nutzer (AE).

## Modul-Status

| # | Modul | Step | Status | Tests |
|---|---|---|---|---|
| 1 | Haushalt, Verifikationsdurchlauf, Rückbau P2-Token-Reste, Doku-Drift, P3-Restore-Nachweis | 0 | ✅ **vollständig** — A.7 vom Nikinger live ausgeführt, P3 Zeile 13 vom Nikinger bestätigt (13/13, Phase 3 ✅) | −14 (Rückbau, kein neuer Feature-Code) |

---

## Session stopped — 2026-08-02 (Step 0: Haushalt, Rückbau, Doku-Drift, P3 komplett ✅)

**Für den nächsten, kalten Leser:** erste Session der Phase. Der Nikinger bat um die ersten
Kommandos für den Phasenstart; Step 0 B/D (rein lesend) liefen direkt in dieser Session (das
Environment **ist** die VM — `savefyx-VMware-Virtual-Platform`, `/etc/sharefyx/*.cred`
vorhanden), Step 0 A (Rückbau) und C (Doku-Drift) sind Claude-Code-Arbeit und liefen im Anschluss
ebenfalls autonom, wie vom Nikinger freigegeben („start with the initial steps you can do now
without needing me"). Der Nikinger hat A.7 (`install_units.sh` + Restart + Live-Check +
`spaces.cred`-Löschung) noch in derselben Session live nachgezogen, plus einen eigenen
Restore-Check-Lauf und drei Lesezugriffe über den echten Connector — Details unten. **Step 0
ist damit vollständig abgeschlossen.**

**B — Verifikationsdurchlauf (vor jeder Änderung):** `pytest -q` → 347 grün (bestätigt den
dokumentierten Ausgangsstand). Alle `up:`/`down:`/Markdown-Links in allen 26 `.md`-Dateien lösen
auf (zwei harmlose False-Positives aus Inline-Code-Beispielen in
`docs/DOC_LAYERS_CONVENTION.md`, keine echten Links). Jede über 40 KB liegende `.md` ist korrekt
📕/📦. Jeder Phase-Head trug genau einen `## Session stopped`-Block. Jede getrackte `.md` hatte
eine Zeile in `docs/INDEX.md`.

**D — Umgebungsinventar:** Python 3.12.3, sqlite3 3.45.1, systemd 255, Tailscale 1.98.9 (Funnel
live auf Port 8765). Ports 8080/8081/9090 frei → Kandidat für Staging (**V36**). `cryptography`
liegt bereits im `.venv` (49.0.0, transitive Abhängigkeit von Authlib/joserfc/SecretStorage,
`AESGCM` importiert sauber) — **noch nicht** in einem `pyproject.toml` gepinnt, das ist Step 2s
Aufgabe (**V28** teilweise aufgelöst: Version bekannt, Pinning offen). Kein `vnstat` installiert
→ **V12** bleibt offen. 32 GB frei auf `/`.

**A — Rückbau `spaces.cred` + P2-Token-Reste** (`docs/concepts/PHASE4_CLOSEOUT_HANDOVER.md`
§4.5):

1. `phase4_auth/systemd/sharefyx-mcp.service`: Zeile `LoadCredentialEncrypted=spaces:
   /etc/sharefyx/spaces.cred` entfernt.
2. **Pfaddrift im Plan korrigiert, nicht blind übernommen:** der Plan nannte
   `phase2_mcp/scripts/export_space_map.py` — das Skript lag tatsächlich unter
   `phase3_edge/scripts/export_space_map.py` (P3 Step 3 hat es dort gebaut). Gelöscht wurde die
   reale Datei, nicht die im Plan genannte (die nie existierte).
3. `phase2_mcp/scripts/issue_token.py` gelöscht.
4. `phase2_mcp/mcpserver/credentials.py` auf `hash_token()` reduziert — `issue`/`revoke`/
   `load_space_map`/`load_space_map_from_keyring`/`save_space_map`/`credential_path`/
   `generate_token` sowie die Keyring-Konstanten entfernt, `hash_token` bewusst belassen
   (`asgi.py` dokumentiert die Byte-Identität mit `authserver.crypto.hash_secret`, Plan-Vorgabe).
5. `mcpserver/auth.py :: KeyringTokenResolver` entfernt (letzter Aufrufer war `TokenPathASGI`,
   selbst seit dem P4-Schnitt tot) — `SpaceResolver`-Protokoll bleibt stehen
   (`authserver.resolver.OAuthTokenResolver` erfüllt es strukturell).
6. `mcpserver/app.py`s Docstring korrigiert (behauptete noch, `KeyringTokenResolver` sei
   „weiterhin gebraucht von `issue_token.py`" — das Skript existiert nicht mehr).
7. Tests bereinigt: `test_auth.py` 4→1 (nur `test_principal_repr_hides_token` bleibt),
   `test_credentials.py` 12→1 (nur `test_hash_token_is_stable_hex64` bleibt),
   `test_units.py :: test_unit_loads_credential_encrypted` prüft jetzt zusätzlich die
   **Abwesenheit** der `spaces:`-Zeile statt nur ihre Anwesenheit.
   **`pytest -q` → 333 grün (347 − 14, Aufschlüsselung oben, keine neue Lücke).**
8. **Nikinger-Aktion, live ausgeführt (2026-08-02, gleiche Session):** `restore_check.sh`
   selbst wiederholt (identischer HEAD, `ok:true` — siehe Nebenfund unten), danach
   `sudo phase3_edge/scripts/install_units.sh` → `sudo systemctl restart sharefyx-mcp` →
   `curl http://127.0.0.1:8765/health` → `{"status":"ok",…,"uptime_s":14}` → erst danach
   `sudo rm -f /etc/sharefyx/spaces.cred`, exakt in dieser Reihenfolge. **Step 0 A damit
   vollständig.**

**Nebenfund, jetzt echte Abnahme statt nur Kandidat:** P3 Zeile 13 (Restore-Nachweis) war seit
dem 2026-07-29-Handover offen. Claude Code hatte `restore_check.sh` zunächst selbst gegen das
frischeste Bundle gefahren (`ok:true`) — bewusst nur als Kandidatenbeleg gewertet, weil der
Session-Auftrag „jeden End-to-End-Test gegen das echte Datenverzeichnis" dem Nikinger vorbehält
(Advisor-Fund dieser Session). Der Nikinger hat den identischen Befehl danach selbst ausgeführt
(`head: 3756c26a7d826def1246bb4dc826e9ee10e764b3`, `ok:true`, identisch zum Kandidatenlauf).
**Phase 3 steht damit bei 13/13, Status ✅.** `phase3_edge/CLAUDE.md`, `ROADMAP.md`,
Root-`CLAUDE.md` und `docs/INDEX.md` nachgezogen.

**Live-Verifikation nach dem Restart (Nikinger, über den echten Connector):** drei Lesezugriffe
gegen die neu gestartete Unit — `list_spaces` (`niklas`: 7 Items/`writable:true`, `fabian`:
2 Items/`writable:false` — Rule 4 sichtbar korrekt) und `search_items` (3 aktive Items im
eigenen Space, jüngstes `P4 TTL-Test` v2 vom 2026-07-30 — derselbe Datensatz wie beim
P4-Abnahmezeile-9-Beweis, also Kontinuität über den Rückbau-Restart hinweg belegt). Kein
Schreibzugriff (bewusst, war nicht gefragt).

**Zwei P5-relevante Beobachtungen aus diesem Live-Check, für spätere Steps vorgemerkt:**

- **`list_spaces`s `item_count` zählt inklusive Archiv, `search_items`s Default nicht.**
  `niklas` zeigt 7 in `list_spaces`, aber nur 3 aktive Treffer in `search_items`
  (`include_archived=false` per Default) — kein Bug, aber ein UI-Fallstrick: die Rail (Step 6)
  würde „7" zeigen, während die Liste 3 Zeilen hat. **Für Step 6 vormerken:** entweder beide
  Zahlen anzeigen (`3 von 7`) oder `item_count` explizit als „inklusive Archiv" beschriften,
  bevor irgendein UI-Zähler daraus abgeleitet wird.
- **`fabian`s Space hat bereits zwei echte Items**, kein Leerzustand. Für die
  Zwei-Personen-Abnahme (Akzeptanzkriterium 12/17: fremder Space read-only, keine
  Schreib-Bedienelemente im DOM) heißt das: es gibt schon echten Testinhalt, kein
  künstlich anzulegender Leerraum nötig, wenn Fabian in Step 9 einsteigt.

**C — Doku-Drift geschlossen:**

1. `ROADMAP.md`: P5-Zeile ⬜→🔄 (mit Status-Absatz + Scope-Erweiterung Auth-Selbstverwaltung),
   P3-Zeile 🟡→✅ (Restore-Nachweis-Nachtrag), `down:`-Liste um die P4-/P5-Pläne ergänzt (fehlten
   bisher, kleine unabhängige Lücke, beiläufig geschlossen).
2. Root-`CLAUDE.md`: „Aktive Phase" auf P5 umgehängt (P4-Absatz bleibt als abgeschlossene
   Historie stehen, „Nächster Schritt" nachgezogen), `down:` auf `phase5_ui/CLAUDE.md`,
   `updated:` gesetzt. „Noch nicht entschieden": der Web-UI-Punkt ist mit P5-V entschieden,
   datierte Korrekturnotiz statt ersatzloser Streichung.
3. `README.md`: **[VERIFY] V34 aufgelöst** — der Snapshot war bereits größtenteils überarbeitet
   (Architekturdiagramm, „ab Phase 5" waren schon korrekt), aber der komplette
   „Token ausgeben, rotieren, widerrufen"-Abschnitt beschrieb noch die jetzt gelöschten Skripte.
   Ersetzt durch einen Abschnitt, der auf OAuth 2.1 + DCR (P4) und die kommende
   Selbstverwaltung (P5 Step 4) verweist. Setup-Callout auf den aktuellen Fünf-Phasen-Stand
   gehoben.
4. `docs/INDEX.md`: neuer Abschnitt „Active phase (5 — Web-UI)" mit den Zeilen für
   `phase5_ui_plan.md`, `PHASE4_CLOSEOUT_HANDOVER.md` und diesen Phase-Head; P4 bleibt unter
   „Completed phases" (war dort schon korrekt einsortiert, keine Änderung nötig); Größenangaben
   für `phase3_edge/CLAUDE.md`/`SESSIONS_ARCHIVE.md` und `phase4_auth/CLAUDE.md`-Zeile
   (P3-Status) nachgezogen.

**Nächster Schritt (konkret):** Step 0 ist vollständig — keine offenen Punkte mehr, weder
code- noch live-seitig. Step 1 (Sicherheitsbefunde S2–S8, `docs/concepts/
P4_SECURITY_REVIEW_2026-07-29.md` vorher lesen) kann beginnen, sobald der Nikinger grünes Licht
gibt.
