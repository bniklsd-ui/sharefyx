---
status: live
purpose: Menschliche Übersicht + Maschinen-Setup (venv, Keyring, Datenverzeichnis, Tests)
read-when: erstes Setup auf einer neuen Maschine, oder wenn jemand wissen will, was das Ding überhaupt ist
detail: L2
up: docs/INDEX.md
updated: 2026-07-25
---
# Space-Server

Ein geteilter Kontext-Speicher für zwei Personen und ihre Claude-Instanzen.

Notizen und Aufgaben liegen als **Markdown-Dateien mit YAML-Frontmatter** in einem
Git-Repository auf einer Heim-VM. Menschen bearbeiten sie im Editor oder (ab Phase 4) in einer
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
Tunnel (Cloudflare, ausgehend — CGNAT-tauglich)
   ▼
MCP-Server (Streamable HTTP, Token→Space)      [Phase 2]
   ▼
Storage-Kern: Dateien + Index + Locking        [Phase 1]
   ▲
REST-API + Web-UI für Menschen                 [Phase 4]
```

Der Storage-Kern ist die einzige Komponente, die Daten anfasst. MCP und REST sind zwei dünne
Adapter darüber — deshalb wird der Kern zuerst gebaut und offline bewiesen.

## Setup

> **Stand 2026-07-25:** Phase 1 (Storage-Kern) ist abgeschlossen und live-verifiziert — 68 Tests
> (70 bei Phasenabschluss, minus zwei bei Entfernung toten Codes in P2 Step 0), `space_cli.py`
> als Beweis. Die Befehle unten funktionieren real, nicht nur als Zielbild. Phase 2 (MCP-Server)
> ist im Aufbau; bis sie steht, gibt es keinen Netzpfad, nur den lokalen Storage-Kern + CLI.

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

```bash
python phase2_mcp/scripts/issue_token.py --space nikinger    # neues Token ausgeben
python phase2_mcp/scripts/issue_token.py --list              # Spaces + gekürzte Hashes
python phase2_mcp/scripts/issue_token.py --revoke nikinger   # alle Tokens dieses Space widerrufen
```

**Das Token wird genau einmal angezeigt** — direkt nach `--space` auf stdout, kein zweites Mal
abrufbar. Der Keyring speichert nur den sha256-Hash, nie das Token selbst. Wenn ein Token
verloren geht: neu ausgeben (`--space`), den alten Hash mit `--revoke` entfernen, danach die
Connector-URL in Claude aktualisieren (der alte Pfad-Token funktioniert ab dem Revoke nicht
mehr).

## Bewusst akzeptierte Kompromisse

Damit sie niemand später „entdeckt" und für einen Bug hält:

- **Keine Ende-zu-Ende-Verschlüsselung.** Der Server muss lesen können, damit Claude lesen kann.
  Bei Cloudflare Tunnel sieht zusätzlich Cloudflare den Klartext.
- **Auth v0 ist ein Token in der URL.** Ein Bearer-Passwort, das in Logs landet. Bewusst als
  Zwischenschritt gewählt; OAuth 2.1 ist Phase 5 und nicht optional.
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
