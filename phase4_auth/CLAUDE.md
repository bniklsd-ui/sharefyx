---
status: live
purpose: Phase-Head OAuth 2.1 + DCR — Scope, harte Regeln, Modulstatus, aktueller Session-Handover
read-when: Arbeiten in phase4_auth/ oder an den in P4-Q genannten Dateien in phase2_mcp/mcpserver — zuerst lesen, zusammen mit dem neuesten Session-stopped-Block
detail: L2
up: ../CLAUDE.md
down:
  - ../docs/concepts/phase4_auth_plan.md          # voller Plan, Entscheidungen P4-A–P4-R, Steps 0–7
  - ../docs/concepts/PHASE3_CLOSEOUT_HANDOVER.md  # Herkunft der offenen Entscheidungen, Doku-Drift, [VERIFY]-Bilanz
  - SESSIONS_ARCHIVE.md                            # ältere Session-Blöcke, newest-first
updated: 2026-07-28
---

# CLAUDE.md — Phase 4: OAuth 2.1 + DCR (`phase4_auth/`)

> **Der Pfad-Token verschwindet.** Ein eigener, handgeschriebener Authorization Server im selben
> Prozess ersetzt ihn — Discovery, Dynamic Client Registration, PKCE, Argon2id + TOTP, opake
> rotierende Token. Kein Upstream-IdP, kein `auth=`-Parameter an `FastMCP`.
> **Quelle der Wahrheit ist der Code, nicht dieses Dokument.**
> Vollständiges Design + alle 18 gelockten Entscheidungen (P4-A–P4-R) + Steps 0–7:
> `../docs/concepts/phase4_auth_plan.md`.

## Mission (zuerst lesen)

Der eigentliche Härtetest der Phase ist nicht der erste erfolgreiche Login, sondern der erste
erfolgreiche **Fehlschlag**: ein wiederverwendeter Refresh-Token muss die ganze Token-Familie
töten, ein zweimal eingelöster Authorization-Code muss die daraus entstandenen Token widerrufen,
und ein falsches Passwort darf nicht verraten, ob das Konto existiert. Diese drei Fälle sind
Akzeptanzkriterien, keine Kür (Plan §0.1).

## Bauprinzip (Projekt-Kernprinzip)

„Der Server ist dumm." **Phase 4 enthält KEINE AI, keine neuen Tools, keine Fachlogik.** Wer
hier `tools.py` anfasst, ist in der falschen Phase (P4-Q).

## Scope (Kurzform, Details: Plan §0.3/§0.7 P4-A–P4-R)

- **DRIN:** Protected Resource Metadata (RFC 9728), Authorization Server (RFC 8414), Dynamic
  Client Registration (RFC 7591), PKCE `S256` (RFC 7636), Token-Rotation + Familien-Widerruf
  (RFC 9700), `iss` im Authorization Response (RFC 9207), Argon2id-Passwörter, TOTP (RFC 6238)
  als zweiter Faktor, befristeter Parallelbetrieb `SPACE_AUTH_MODE=both`.
- **DRAUSSEN:** REST/UI (P5), MCP-Revision 2026-07-28, `fastmcp` 4, D6, neue Tools,
  feingranulare Lese-Rechte, Off-site-Backup, Monitoring, `/oauth/revoke`, `/oauth/introspect`,
  Recovery-Codes für den zweiten Faktor, CIMD (Seam vorhanden, siehe Plan §2.6 `[SEAM]`).

## Harte Regeln dieser Phase (nicht verhandelbar)

- **P4-A/P4-C — Eigener AS, strikte Abhängigkeitsrichtung.** `mcpserver → authserver`, niemals
  umgekehrt. `authserver` importiert nichts aus `mcpserver` oder `storage` — kennt nur
  Starlette, SQLite, `argon2-cffi`. Test: `test_authserver_does_not_import_mcpserver`.
- **P4-D — Token opak.** `secrets.token_urlsafe(32)`, gespeichert wird ausschließlich
  `sha256`-Hex. Kein JWT, kein JWKS, kein Signing-Key.
- **P4-F — Argon2id, nicht scrypt.** `t=2, m=19456 KiB, p=1` (OWASP + BSI TR-02102-1). `[VERIFY]`
  V17: Dauer eines echten Durchlaufs auf dieser VM messen, Zielkorridor 50–250 ms, Wert
  dokumentieren statt raten.
- **P4-I — Ausnahme von Hard Rule 2.** Die Auth-SQLite (`/var/lib/sharefyx/auth.sqlite3`) ist
  autoritativ, keine Ableitung aus Dateien — benannte Ausnahme, berührt keine Nutzdaten.
- **P4-Q — Berührungsfläche.** P4 darf in `phase2_mcp/` genau anfassen: `mcpserver/asgi.py`,
  `mcpserver/context.py`, `mcpserver/app.py`, `mcpserver/config.py`, `mcpserver/request_log.py`,
  `mcpserver/logging_setup.py`, `scripts/serve.py`. **Nicht anfassen:** `tools.py`,
  `permissions.py`, `server.py`, `auth.py`, `credentials.py`, `storage/*`. Änderungsbedarf dort
  ist ein Befund für den Nikinger, keine Aufgabe.
- **P4-R — Bibliotheks-Pins.** `fastmcp==3.4.4` bleibt exakt (P3-D unverändert).
  `argon2-cffi==25.1.0` exakt gepinnt (in Step 0 gemessen, kein Range). Sonst keine neuen
  Laufzeitabhängigkeiten: kein `authlib`, kein `pyjwt`, kein `jinja2`, kein `itsdangerous`.

## Modul-Status

| # | Modul | Step | Status | Tests |
|---|---|---|---|---|
| 1 | Haushalt, Drift, geerbte Abnahme, kritischer Keyring-Fund (nikinger-Token) | 0 | ✅ | 0 (kein Feature-Code) |
| 2 | Paketgerüst `phase4_auth/`, `authserver/{config,models,crypto,errors}.py` | 1 | ✅ | 20 (5 `test_crypto.py` + 12 `test_authserver_config.py` + 3 `test_errors.py`) |

**Zeile 1, Step 0:** kritischer Fund — ein nie widerrufener Keyring-Token für einen dritten,
seit P2-B2 umbenannten Space (`nikinger`), live und schreibfähig. Details, Zeitachse und
Behebung (Keyring-Widerruf + Export + `systemctl restart`, beide Male live bestätigt):
`docs/concepts/PHASE3_CLOSEOUT_HANDOVER.md` §5 Nachträge. Übrige Autocompact-Drift-Funde aus dem
Handover behoben (siehe dortiger Commit-Verlauf, nicht hier dupliziert). Geerbte P3-Abnahme:
Zeile 12 (Backup-Timer) durch echten Lauf bestätigt, V13 (`diagnose.sh` vs. echtes Tailscale)
geschlossen; Zeile 6 (Reboot) und Zeile 13 (Restore-Nachweis) bleiben bewusst offen.

**Zeile 2, Step 1:** `config.py` (`AuthSettings`/`load_auth_settings`, Env-Validierung inkl.
`SPACE_PUBLIC_BASE_URL`-Härtung), `crypto.py` (opake Token, `sha256`, PKCE gegen den
RFC-7636-Appendix-B-Vektor getestet, nicht gegen einen selbst berechneten Wert), `errors.py`
(RFC-6749-Fehlercode-Whitelist, `OAuthError`), `models.py` (Platzhalter — Persistenz-Modelle
folgen in Step 3, am dort festgelegten Schema orientiert, hier bewusst nicht vorweggenommen).
`argon2-cffi==25.1.0` exakt gepinnt (P4-R, in Step 0 gemessen). `dev_install.sh` nimmt
`phase4_auth/` ohne Änderung auf (V16 bestätigt). `.gitignore` um `*.sqlite3` erweitert (V21 —
vorher griff nur `.index.sqlite3` spezifisch, `auth.sqlite3` wäre committebar gewesen).

**Abweichung vom Plan, dokumentiert statt still übernommen:** der Plan sah `phase4_auth/tests/
__init__.py` vor. Das kollidiert real mit dem bereits bestehenden `phase3_edge/tests/__init__.py`
— beide würden pytest als dasselbe Top-Level-Modul `tests` gelten (kein gemeinsames Elternpaket,
kein `--import-mode=importlib` konfiguriert). Behoben durch Weglassen, wie in
`phase1_storage/tests`/`phase2_mcp/tests` bereits gehandhabt (kein `__init__.py`). Zweite Folge:
ein `test_config.py` hätte mit `phase2_mcp/tests/test_config.py` kollidiert (gleicher Basename,
keine Pakete) — Datei heißt deshalb `test_authserver_config.py`.

## Geerbte Contracts

Aus P2 (`phase2_mcp/CLAUDE.md`, `docs/concepts/phase2_mcp_plan.md` §2/§3): sechs Tools,
Tool-Contract, Fehlerabbildung, `SpaceResolver` → `Principal`, `Permissions`-Seam. Aus P3
(`phase3_edge/CLAUDE.md`, `docs/concepts/phase3_edge_plan.md` §2/§3): Credential-Weg systemd →
Prozess, Request-Log-Format, Unit-Platzhalter-Mechanik. **Der Contract ist ab jetzt wieder zu** —
P4 ändert `asgi.py`/`context.py` (P4-Q), fasst `tools.py`/`permissions.py`/`auth.py` nicht an.

---

## Session stopped — 2026-07-28 (Step 0 + Step 1)

**Ergebnis:** Step 0 (Haushalt, Drift, geerbte Abnahme) und Step 1 (Gerüst, Konfiguration,
Kryptobausteine) abgeschlossen. `pytest -q` → **188/188 grün** (168 P1+P2+P3 + 20 neue P4-Tests).

**Kritischer Fund, geschlossen:** `export_space_map.py` zeigte zu Sessionbeginn drei aktive
Spaces (`fabian`, `niklas`, `nikinger`) statt der erwarteten zwei — ein Keyring-Token aus P2
Step 3, nie widerrufen trotz der B2-Umbenennung `nikinger/` → `niklas/`. Live und schreibfähig
(`Store.create()` legt Zielverzeichnisse automatisch an), aber dormant (`nikinger/` existierte
nicht mehr unter `DATA_ROOT`). Nikinger-Entscheidung: widerrufen. Ausgeführt in zwei Schritten,
beide live bestätigt: Keyring-Widerruf (`issue_token.py --revoke nikinger`), danach Export +
`sudo systemctl restart sharefyx-mcp` (2026-07-28 14:12:49) — `diagnose.sh` danach komplett
grün, `export_space_map.py` zeigt wieder exakt zwei Spaces. Vollständige Zeitachse:
`docs/concepts/PHASE3_CLOSEOUT_HANDOVER.md` §5 Nachträge. Nebeneffekt: die Handover-eigene
„Korrektur" von Fund 1 (die Behauptung, „alle drei Token rotiert" sei Drift und real seien es
zwei gewesen) war selbst falsch — zum Zeitpunkt der Prüfung existierten tatsächlich drei aktive
Spaces.

**Autocompact-Drift aus dem P3-Handover (§5) behoben:** README.md voll auf P3-Stand gezogen
(Cloudflare-Diagramm, Phasennummern OAuth/Web-UI, Tokenbeispiel), ROADMAP.md (Cloudflare →
Tailscale Funnel, `LoadCredential` → `LoadCredentialEncrypted`, P4-Paketname `auth` →
`authserver` per P4-B), Root-`CLAUDE.md` (R3-Ergänzung analog R4, Kollege-Prozess-Frage als in
P3-G entschieden markiert, „Aktive Phase" auf P4 gesetzt), `phase3_edge/CLAUDE.md`
(Tailscale-Installationsstatus, V13 geschlossen).

**Geerbte P3-Abnahme:** Zeile 12 (Backup-Timer) durch `systemctl list-timers` bestätigt (echter
Lauf 2026-07-28 00:00:50). Zeile 6 (Reboot) bleibt bewusst passiv offen. Zeile 13
(Restore-Nachweis) bewusst **nicht** nachgeholt — braucht ein frisches Bundle, kein Lauf
während ungeklärtem Credential-Zustand (war zum Prüfzeitpunkt ohnehin gegeben).

**Environment-Inventar (Step 0, `[VERIFY]` aufgelöst):** systemd 255 (≥235 für
`StateDirectory=`), NTP synchronisiert (`yes`), `argon2-cffi` aktuell `25.1.0` (P4-R-Pin),
`fastmcp` stabil weiterhin `3.4.5`/installiert `3.4.4` — **kein** stabiles 4.x, nur eine Alpha
`4.0.0a2` (`pip index versions --pre`). Der Plan-Befund „FastMCP 4 spricht die neue Revision,
P3-E-Trigger gefallen" ist damit nur zur Hälfte richtig — eine Alpha ist kein Release. Notiert,
keine Aktion (V25: nur beobachten).

**Step 1:** `authserver/{config,models,crypto,errors}.py` gebaut, `phase4_auth/pyproject.toml`
(Paket `authserver`, `argon2-cffi==25.1.0` exakt), `pytest.ini` um `phase4_auth/tests` erweitert,
`.gitignore` um `*.sqlite3` erweitert (V21). Abweichung vom Plan bei der Testdatei-Benennung
(siehe Modul-Status oben) — Ursache Namenskollisionen mit bestehenden `tests`-Verzeichnissen,
nicht antizipierbar ohne Repo-Zugriff (der Plan wurde ohne diesen geschrieben, siehe Plan-Kopf).

**Nächster Schritt (konkret):** Step 2 — Passwörter, TOTP, Nutzerakten
(`authserver/{passwords,totp,users}.py`, `phase4_auth/scripts/{provision_user,
export_auth_users}.py`). Argon2id-Parameter sind bereits gemessen (P4-R-Notiz oben) und werden
dort als Modulkonstanten eingesetzt, nicht neu hergeleitet.
