---
status: live
purpose: Archiv älterer Session-stopped-Blöcke aus phase4_auth/CLAUDE.md, newest-first, verbatim
read-when: Audit vergangener Sessions dieser Phase; NICHT für normalen Session-Start
detail: L3
up: CLAUDE.md
updated: 2026-07-28
---
# Session-Archiv — Phase 4 OAuth 2.1 + DCR

Newest-first. Erste Rotation dieser Phase (2026-07-28, beim Abschluss von Step 3) — via
`scripts/rotate_session_block.sh phase4_auth`, nie von Hand.

## Session stopped — 2026-07-28 (Step 0 + Step 1 + Step 2)

**Ergebnis:** Step 0 (Haushalt, Drift, geerbte Abnahme), Step 1 (Gerüst, Konfiguration,
Kryptobausteine) und Step 2 (Passwörter, TOTP, Nutzerakten) abgeschlossen. `pytest -q` →
**225/225 grün** (168 P1+P2+P3 + 57 neue P4-Tests: 20 Step 1 + 37 Step 2).

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

**Step 2:** `passwords.py` (Argon2id über `argon2-cffi`, `verify_password` wirft nie —
`InvalidHashError` erbt von `ValueError`, nicht von `Argon2Error`, ein Test
(`test_verify_returns_false_on_garbage_hash`) deckte das sofort auf, `DUMMY_HASH` für den
Enumerationsschutz), `totp.py` (RFC 6238 über RFC 4226, stdlib, alle 15 Appendix-B-Vektoren
SHA1/SHA256/SHA512 grün, Replay-Schutz über injizierten `last_counter`), `users.py` (spiegelt
`credentials.py :: load_space_map()` bewusst — Credentials-Verzeichnis zuerst, Keyring-Fallback,
`warning` bei fehlender Datei, Ausnahme bei kaputtem Inhalt). `provision_user.py`/
`export_auth_users.py` nach `issue_token.py`/`export_space_map.py`-Muster, gegen Fake-Keyring
+ injizierten `get_password` getestet — **nicht** gegen den echten Keyring ausgeführt, gleiche
Grenze wie bei P2 Step 3s `--space nikinger`-Roundtrip (Sache des Nikingers, nicht Claude Codes).

**`[VERIFY]` V17, gemessen (nicht geraten):** Argon2id mit den Plan-Default-Parametern
(`t=2, m=19456, p=1`) maß auf dieser VM **~15 ms** je Durchlauf — deutlich unter dem
Zielkorridor 50–250 ms. Nach Plan-Vorgabe `t` erhöht: `t=8` misst **~53 ms** (`m`/`p`
unverändert), fünf Läufe, Werte im Session-Log oben unter „Step 2" nachvollziehbar. Konstante
in `passwords.py` dokumentiert den gemessenen statt einen geratenen Wert.

**Nächster Schritt (konkret):** Step 3 — Persistenz und Bremse (`authserver/{store,
ratelimit}.py`, `test_store.py`, `test_ratelimit.py`). Schema aus Plan §2.3, `AuthStore`
kapselt **jede** SQL-Anweisung (kein SQL außerhalb dieses Moduls, per Grep im Session-Block zu
belegen), `now_fn` injiziert. Der Kern der Phase — Code-Replay/Refresh-Replay-Tötungsregeln
(RFC 9700) sind hier, nicht später.

---

