---
status: live
purpose: Menschliche Übersicht + Maschinen-Setup (venv, Keyring, Datenverzeichnis, Tests)
read-when: erstes Setup auf einer neuen Maschine, oder wenn jemand wissen will, was das Ding überhaupt ist
detail: L2
up: docs/INDEX.md
updated: 2026-07-28
---
# Space-Server

Ein geteilter Kontext-Speicher für zwei Personen und ihre Claude-Instanzen.

Notizen und Aufgaben liegen als **Markdown-Dateien mit YAML-Frontmatter** in einem
Git-Repository auf einer Heim-VM. Menschen bearbeiten sie im Editor oder (ab Phase 5) in einer
Web-UI. Claude greift über einen **Remote-MCP-Custom-Connector** darauf zu — jeder Nutzer hat
einen eigenen Space, beide dürfen den des anderen lesen.

**Was es nicht ist:** kein Wissensmanagement mit semantischer Suche, keine Cloud-Notizapp, kein
Gedächtnis für Claude. Es ist ein Aktenschrank, den man in jeder Konversation aktiv aufmachen
muss. Claude läuft nicht im Hintergrund und aktualisiert hier nichts von selbst.

## Warum Markdown + Frontmatter statt Datenbank

Drei Gründe, alle praktisch:

1. **Token-Effizienz.** Eine Suche liefert nur die Frontmatter-Felder plus einen kurzen Snippet
   zurück. Dreißig Treffer kosten dadurch wenige hundert Tokens statt Zehntausende. Das `links:`-
   Feld macht daraus einen rudimentären Graph, den Claude gezielt entlangläuft, statt breit zu suchen.
2. **Git ist die Versionierung.** Ein Commit je Schreibvorgang — Historie, Diffs und Undo ohne
   eine einzige Zeile eigenen Codes.
3. **Menschenlesbar.** Wenn der Server ausfällt, sind es immer noch Textdateien in einem
   Verzeichnis. Kein Export nötig, keine Geiselhaft.

SQLite wird trotzdem verwendet — aber ausschließlich als **abgeleiteter Index**, jederzeit
löschbar und aus den Dateien rekonstruierbar.

## Architektur in einem Absatz

```
Claude (Web/Desktop/Mobile)
   │  HTTPS, Verbindung kommt von Anthropics Backend
   ▼
Tailscale Funnel (ausgehend — CGNAT-tauglich, TLS terminiert auf der Node)
   ▼
MCP-Server (Streamable HTTP, Token→Space)      [Phase 2]
   ▼
Storage-Kern: Dateien + Index + Locking        [Phase 1]
   ▲
REST-API + Web-UI für Menschen                 [Phase 5]
```

**Korrektur (2026-07-28, P4 Step 0):** ersetzt Cloudflare Tunnel — P3 hat stattdessen Tailscale
Funnel gebaut (P3-A). Systemd-Unit, `/health`, Request-Log und Backup/Restore aus P3 sind hier
noch keine eigene Zeile, siehe `phase3_edge/CLAUDE.md`.

Der Storage-Kern ist die einzige Komponente, die Daten anfasst. MCP und REST sind zwei dünne
Adapter darüber — deshalb wird der Kern zuerst gebaut und offline bewiesen.

## Setup

> **Stand 2026-07-30:** Phase 1 (Storage-Kern) und Phase 2 (MCP-Server) sind abgeschlossen und
> live-verifiziert. Phase 3 (Exposure & Betrieb, Tailscale Funnel + systemd) ist code-complete,
> 🟡 — 12 von 13 Live-Abnahmezeilen bestanden, siehe `phase3_edge/CLAUDE.md`. Phase 4 (OAuth 2.1
> + DCR, Plan: `docs/concepts/phase4_auth_plan.md`) ist **live-verifiziert** — der Schnitt
> (Runbook-Schritt 8) ist vollzogen, der Connector läuft ausschließlich über OAuth 2.1 + DCR,
> der Pfad-Token existiert nicht mehr. Siehe Root-`CLAUDE.md` „Current state" für den
> verbindlichen aktiven Phasenstand.

```bash
python -m venv .venv && source .venv/bin/activate
./scripts/dev_install.sh          # editable installs aller Phasenpakete
pytest                            # gemockt, kein Netz
```

**Datenverzeichnis** (`DATA_ROOT`) ist ein **eigenes Git-Repository**, getrennt vom Code-Repo.
Es wird nie in dieses Repo eingecheckt.

**Secrets** liegen ausschließlich im OS-Keyring (Service `nikinger-space`) bzw. als systemd
`LoadCredential`. Nicht in `.env`, nicht in einer Config, nicht in einer Shell-Variable. Wenn
irgendwo in diesem Projekt ein Token in einer Datei auftaucht, ist das ein Incident.

## Token ausgeben, rotieren, widerrufen

**[2026-07-30 Korrektur, Schnitt (Runbook-Schritt 8)]** Dieser Abschnitt beschreibt den
**Pfad-Token** aus P2 — seit dem Schnitt in Phase 4 verbindet sich niemand mehr darüber, beide
bestehenden Token sind live widerrufen und `TokenPathASGI` (der Code, der sie akzeptierte) ist
entfernt. `issue_token.py`/der Keyring bleiben trotzdem im Repo: reines Bestandswerkzeug, nicht
mehr Teil des Connect-Wegs. Die echte Anmeldung läuft ab jetzt über OAuth 2.1 + DCR (Passwort +
TOTP), siehe `phase4_auth/CLAUDE.md` — Runbook „Inbetriebnahme" (`provision_user.py`,
`authctl.py unlock`).

```bash
python phase2_mcp/scripts/issue_token.py --space niklas      # neues Token ausgeben
python phase2_mcp/scripts/issue_token.py --list              # Spaces + gekürzte Hashes
python phase2_mcp/scripts/issue_token.py --revoke niklas     # alle Tokens dieses Space widerrufen
```

**Das Token wird genau einmal angezeigt** — direkt nach `--space` auf stdout, kein zweites Mal
abrufbar. Der Keyring speichert nur den sha256-Hash, nie das Token selbst. Wenn ein Token
verloren geht: neu ausgeben (`--space`), den alten Hash mit `--revoke` entfernen, danach die
Connector-URL in Claude aktualisieren (der alte Pfad-Token funktioniert ab dem Revoke nicht
mehr).

### Rotation im Dienstbetrieb (ab P3)

Läuft der Server als systemd-Dienst (`sharefyx-mcp.service`, siehe „Betrieb" unten), liest er die
Space-Map **nicht** aus dem Keyring, sondern aus einer verschlüsselten Credential-Datei
(`LoadCredentialEncrypted`, `mcpserver/credentials.py :: load_space_map()`). Eine Token-Rotation
braucht deshalb vier Schritte in dieser Reihenfolge (P3-M):

```bash
python phase2_mcp/scripts/issue_token.py --revoke niklas
python phase2_mcp/scripts/issue_token.py --space niklas        # 1. Token neu ausgeben (Keyring)

python phase3_edge/scripts/export_space_map.py \                # 2. Export
  | sudo systemd-creds encrypt --name=spaces - /etc/sharefyx/spaces.cred

sudo systemctl restart sharefyx-mcp                              # 3. Neustart
#    ohne diesen Schritt bleibt die ALTE Space-Map im tmpfs — der Dienst liefert dann 401 auf
#    das neue Token, obwohl der Export erfolgreich war. Das sieht wie „Connector kaputt" aus,
#    ist aber ein vergessener Restart.

# 4. Connector-URL mit dem neuen Token in beiden Claude-Accounts aktualisieren
```

## MCP-Server smoke-testen

```bash
python phase2_mcp/scripts/mcp_smoke.py            # Text-Report
python phase2_mcp/scripts/mcp_smoke.py --json     # maschinenlesbar auf stdout
```

Baut ein **temporäres** `DATA_ROOT` (nie das echte), zwei Fixture-Spaces und zwei Tokens, die
nur in diesem Lauf existieren — der echte Keyring (Service `nikinger-space`) bleibt unangetastet.
Fährt die sechs Tools einmal komplett durch (beide Rule-4-Fälle: fremd lesen mit Wrap, fremd
schreiben mit `write_denied`) und misst die Antwortgröße je Aufruf. Exit-Code `0` nur, wenn alle
Prüfungen grün sind.

Lokal ohne Tunnel starten (Phase 3 baut die öffentliche Erreichbarkeit):

```bash
SPACE_DATA_ROOT=/pfad/zu/einem/testverzeichnis \
SPACE_PUBLIC_BASE_URL=https://localhost.example \
SPACE_AUTH_DB=/tmp/sharefyx-dev-auth.sqlite3 \
python phase2_mcp/scripts/serve.py
curl http://127.0.0.1:8765/health
```

**[2026-07-30 Korrektur, Schnitt (Runbook-Schritt 8)]** Ersetzt den vorigen Stand („ohne
`SPACE_AUTH_MODE` bleibt dieser Start der P3-Pfad", P4 Step 6b): `TokenPathASGI`/`AuthModeASGI`
sind entfernt, `create_app()` verlangt jetzt immer ein `OAuthConfig`-Bündel — auch ein lokaler
Testlauf ohne Tunnel braucht `SPACE_PUBLIC_BASE_URL` (ein beliebiger `https://`-Platzhalter, wird
nicht kontaktiert) und einen DB-Pfad (`SPACE_AUTH_DB` oder `STATE_DIRECTORY`). `/mcp` selbst ist
darüber nicht per `curl` testbar (braucht einen echten Bearer-Token) — dafür ist
`mcp_smoke.py` da, das seinen eigenen Token direkt gegen eine temporäre `AuthStore` ausstellt.
Details zum OAuth-Modus (nur noch `oauth`, seit dem Schnitt): `phase4_auth/CLAUDE.md`.

**Nebeneffekt, der vorher nicht existierte:** `serve.py` ruft `load_users()` jetzt **immer** auf
(vorher nur, wenn `SPACE_AUTH_MODE` gesetzt war). Außerhalb von systemd (kein
`CREDENTIALS_DIRECTORY`) fällt das auf den **echten** Keyring (Service `nikinger-space`) zurück
— ein lokaler `serve.py`-Lauf auf dieser Maschine liest damit echte Nutzerakten, auch wenn er nie
einen Login-Versuch bekommt. Kein Schreibzugriff, aber ein neuer Lesezugriff, den es vor dem
Schnitt nicht gab.

## Bewusst akzeptierte Kompromisse

Damit sie niemand später „entdeckt" und für einen Bug hält:

- **Keine Ende-zu-Ende-Verschlüsselung.** Der Server muss lesen können, damit Claude lesen kann.
  **[2026-07-28]** Seit P3 läuft der Weg über Tailscale Funnel, die Node terminiert TLS selbst —
  kein Relay-Betreiber sieht mehr Klartext, aber Tailscale bleibt vertrauenswürdige
  Infrastruktur (R4).
- **Bearer-Token bleiben Bearer-Token.** **[2026-07-30]** Löst den vorigen Satz über den Token
  in der URL ab (Phase 4, Schnitt vollzogen — der Pfad-Token existiert nicht mehr). RFC 9700
  empfiehlt Sender-Constraining über DPoP oder mTLS; der Client unterstützt beides nicht. Ein
  abgeflossener Access-Token ist bis zu 60 Minuten nutzbar, ein Refresh-Token bis zur nächsten
  Rotation. Gegenmittel und ihre Grenze: kurze Lebensdauer, Rotation mit Reuse-Erkennung,
  sofortige Widerrufbarkeit über `authctl.py` (Plan §9 Risiko 3).
- **Single Point of Failure.** Eine VM an einem Mobilfunk-Uplink. Fällt sie aus, zeigt Claude
  nur „Disconnected".
- **Kein Hintergrundgedächtnis.** Siehe oben — Claude muss in jeder Konversation angewiesen
  werden, den Space zu lesen.

Details und Begründungen: `CLAUDE.md` → „Current state" → Rahmenentscheidungen R1–R6.

## Eingefrorene Schreibweisen (Nikinger-Entscheidung, 2026-07-25)

Drei uneinheitliche Schreibweisen für denselben Ort sind **bewusst eingefroren, nicht
„repariert"**: Repo/Drive heißt `sharefyx`, VM-Pfade beginnen mit `/home/savefyx/…`, das
Code-Repo-Verzeichnis heißt `/home/savefyx/dev/savefxy` (Buchstabendreher gegenüber den beiden
anderen). Ebenso: `DATA_ROOT` steht auf Branch `master`, das Code-Repo auf `main` — kosmetisch,
kein Remote betroffen. Eine Umbenennung jetzt würde Pfade brechen, die Phase 3 wortwörtlich in
systemd-Units schreibt. Wer eine dieser Schreibweisen antastet, macht eine Scope-Entscheidung,
keine Aufräumarbeit.

## Navigation

Alle Dokumente sind in [`docs/INDEX.md`](./docs/INDEX.md) verzeichnet. Der Phasenplan steht in
[`ROADMAP.md`](./ROADMAP.md), die Arbeitsregeln in [`CLAUDE.md`](./CLAUDE.md).
