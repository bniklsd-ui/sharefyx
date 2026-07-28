---
status: snapshot
purpose: Abschluss-Handover P3→P4 — Status, Delta seit dem P2-Handover, [VERIFY]-Bilanz V1–V13, geerbte Abnahmezeilen, Doku-Drift aus der Autocompact-Session, offene Entscheidungen für die OAuth-Planung
read-when: Start des Phase-4-Chats, vor dem Entwurf des Claude-Code-Plans — danach nicht mehr
detail: L2
up: ../../phase3_edge/CLAUDE.md
down:
  - ./phase3_edge_plan.md              # Entscheidungen P3-A–P3-N, Steps 0–7
  - ./P3_ABNAHME_2026-07-27.md         # was live tatsächlich funktioniert hat, Befunde B5/B6
  - ./PHASE2_CLOSEOUT_HANDOVER.md      # Vorgänger, Herkunft der Entscheidungen 1–8
updated: 2026-07-28
---
# Phase 3 → Phase 4 — Abschluss-Handover

> **Für einen kalten Leser.** Dieses Dokument ersetzt keinen Plan und wiederholt keine
> Implementierung. **Quelle der Wahrheit ist der Code**, danach der Plan, danach das
> Abnahmeprotokoll — dieser Text zeigt nur darauf und sagt, was noch offen ist.
> Nach dem Entwurf des P4-Plans wird er nicht mehr gebraucht.

---

## 1 Status in fünf Zeilen

1. **P3 ist code-complete, nicht abgenommen.** Steps 0–7 gebaut, alle Tests grün, Live-Abnahme
   **10 von 13** Zeilen. Status in `ROADMAP.md`: 🟡, nicht ✅ — und das soll so bleiben, bis ein
   echter Reboot beobachtet wurde. ✅ heißt in diesem Projekt „live-verifiziert", nicht „gebaut".
2. **Der Connector steht in beiden Accounts.** Zwei Spaces existieren real (`niklas`, `fabian`),
   beide Token sind rotiert, Rule 4 ist erstmals unter echten Zwei-Nutzer-Bedingungen geprüft:
   fremder Body gewrappt, Schreibversuch `write_denied`.
3. **Exposure läuft über Tailscale Funnel, nicht über Cloudflare** (P3-A). Der Hostname ist
   stabil, TLS terminiert auf der eigenen Node. R4 hat dazu eine datierte Ergänzung bekommen.
4. **Der Dienst heilt sich selbst** (`Restart=on-failure`, Kill-Test bestanden) und **protokolliert
   sich selbst** (JSON-Zeilen in journald, Tool-Name + Space + Dauer, ohne Token und ohne Inhalt).
5. **Was P3 nicht bewiesen hat:** Reboot-Überleben, ein Timer-Lauf, ein grüner Restore-Check.
   Diese drei sind bewusst an P4 vererbt, nicht vergessen — siehe §4.

---

## 2 Delta seit dem P2-Handover

Nur was für P4 einen Unterschied macht:

| Was sich geändert hat | Konsequenz für P4 |
|---|---|
| Der Server läuft als **System-Dienst** (`sharefyx-mcp.service`), nicht mehr per Hand | Jede Codeänderung braucht ab jetzt `systemctl restart`. Ein vergessener Restart sieht aus wie „Token kaputt" (401) |
| Die Space-Map kommt über **`LoadCredentialEncrypted`** in den Prozess, Keyring ist nur noch Quelle und Fallback | P4 legt echte Geheimnisse an (Signing-Keys, Client-Secrets). Der Weg dafür existiert bereits — `credentials.py` hat die Verzweigung, `export_space_map.py` die Pipeline |
| Es gibt ein **strukturiertes Request-Log** mit Dauer je Tool-Aufruf | Erstmals messbar. **D6** (SQL-Filterung in `Store.search`) ist damit eine Zahlenfrage geworden, keine Gefühlsfrage |
| Der Pfad-Token steht jetzt **dauerhaft** in zwei Accounts, hinter einem stabilen, in CT-Logs auffindbaren Hostnamen | Das ist das stärkste Argument für P4. In P2 lebte der Token eine Stunde, jetzt bis zur Ablösung |
| `phase3_edge/` ist **kein Python-Paket** — Servercode blieb in `mcpserver` | P4 muss sich entscheiden: `phase4_auth/` mit Paket `auth` (so steht es in `ROADMAP.md`) oder dasselbe Muster wie P3. Siehe §6 |
| **Zwei Spaces existieren** statt einem | Cross-Space-Verhalten ist ab jetzt real testbar — auch für OAuth-Scopes |

Alles Übrige aus dem P2-Handover gilt unverändert: sechs Tools, Frontmatter-Contract,
`SpaceResolver → Principal`, `Permissions.can_read` als Seam, `stateless_http=True`.

---

## 3 `[VERIFY]`-Bilanz der Phase

Aufgelöst wie unaufgelöst, vollständig. V1–V12 stammen aus `phase3_edge_plan.md` §8, V13 ist in
der Phase entstanden.

| # | Was | Status |
|---|---|---|
| V1 | Repo-Stand, 133 Tests, `docs/test-results/` weg | ✅ aufgelöst, Step 0 |
| V2 | Installierte `fastmcp`-Version | ✅ **3.4.4** war bereits installiert, deckt sich mit dem P3-D-Pin |
| V3 | FastMCP-Middleware-API (Importpfad, Hook-Signatur) | ✅ aufgelöst im Code — der reale Pfad steht in `mcpserver/request_log.py`, nicht hier |
| V4 | `systemd-creds`, systemd ≥ 250, TPM2 | ✅ vorhanden; `has-tpm2` → *partial*, also **Host-Key statt TPM2**. Für P3-F ausreichend |
| V5 | Keyring-Backend der VM | ✅ aufgelöst, Wert in der Inventartabelle in `phase3_edge/SESSIONS_ARCHIVE.md` (Step 0) |
| V6 | venv-Pfad für `ExecStart` | ✅ `/home/savefyx/dev/savefxy/.venv/bin/python` |
| V7 | Tailscale: Version, Funnel-Voraussetzungen, `nodeAttrs` | ✅ live aufgelöst — der Dienst ist über `savefyx-vmware-virtual-platform.tail89fc2a.ts.net` öffentlich erreichbar |
| V8 | Welcher `Host`-Header bei uvicorn ankommt | ✅ faktisch aufgelöst (externes `/health` antwortet mit gesetztem `SPACE_ALLOWED_HOSTS`); der konkrete Wert steht in `phase3_edge/local.env`, gitignored |
| V9 | `ProtectHome=read-only` + `ReadWritePaths` erlaubt Git-Commits | ✅ **live geschlossen** — der `append_to_item`-Aufruf der Abnahme erzeugte zeitgleich den Commit `a400221c` im `DATA_ROOT`. Beleg: `P3_ABNAHME_2026-07-27.md`, B5 |
| V10 | Größenbudget von `search_items` gegen echten Bestand (geerbt aus P2 als V8) | ❌ **offen** — jetzt erstmals sinnvoll messbar, weil `fabian` Items hat |
| V11 | MCP-Revision 2026-07-28 | ❌ **offen, Watch-Item.** Die Revision wird **heute** final. Trigger bleibt das erste `fastmcp`-Release mit Support, nicht das Datum (P3-E) |
| V12 | Datenlimit des Mobilfunk-Uplinks | ❌ **offen** — nie geprüft. Mit einem Dauer-Tunnel plus Backup-Timer relevanter als vorher |
| V13 | Grep-Muster in `diagnose.sh`, Prüfung 4, gegen echtes `tailscale funnel status` | ❌ **offen** — der Phase-Head begründet das mit „Tailscale ist nicht installiert", was inzwischen falsch ist. Siehe §5, Fund 2 |

---

## 4 Was P4 aus P3 erbt (Step-0-Kandidaten, kein neuer Scope)

1. **Abnahmezeile 6 — Reboot.** Passiv: beim ersten echten Reboot `/health` von außen prüfen,
   Zeile nachtragen, `ROADMAP.md`/Phase-Head/Index von 🟡 auf ✅ heben. Kein erzwungener
   `sudo reboot` — das war eine bewusste Nikinger-Entscheidung, keine Nachlässigkeit.
2. **Abnahmezeile 12 — Backup-Timer.** `systemctl list-timers sharefyx-backup` muss einen Lauf
   zeigen. Sollte sich von selbst erledigt haben; falls nicht, ist der Timer nicht `enabled`.
3. **Abnahmezeile 13 — Restore-Nachweis.** Kein Defekt (B5): der Check vergleicht gegen den
   *lebenden* `DATA_ROOT`, das Bundle war schlicht älter. Ein sauberer Lauf braucht ein frisches
   Bundle und danach keine Schreibvorgänge. **Nicht** `restore_check.sh` umbauen, bevor das
   einmal unter diesen Bedingungen gelaufen ist.
4. **V13** — `diagnose.sh` einmal gegen das jetzt real vorhandene Tailscale laufen lassen.
5. **D6, V10, V11, V12** — unverändert zurückgestellt, jetzt mit Messgerät.

Nichts davon rechtfertigt eine eigene Phase. Zusammen sind das ein Vormittag in P4 Step 0.

---

## 5 Doku-Drift aus der Autocompact-Session — bitte gezielt suchen und fixen

**Was passiert ist:** In der letzten P3-Session war Autocompact aktiv. Der Kontext wurde
zwischendurch komprimiert, und dabei sind Formulierungen entstanden, die *plausibel klingen, aber
nicht stimmen*. Das ist keine Katastrophe und kein Grund, alles zu misstrauen — aber es ist ein
Muster, und Muster sucht man systematisch, nicht zufällig.

**Fünf Funde, die schon feststehen** (jeweils: was steht da, was stimmt wirklich):

| # | Datei | Was dort steht | Was stimmt |
|---|---|---|---|
| 1 | `phase3_edge/CLAUDE.md` (Abschluss-Punkt 1, Session-Block 2026-07-28), `P3_ABNAHME_2026-07-27.md` §6 + Nachtrag, Commit-Kommentar | „alle **drei** Token rotiert" | Es gibt **zwei** aktive Token: `niklas` und `fabian`. Die Drei entsteht durch Mitzählen des temporären `sharefyx_phase_3_fabian`-Tokens, der abgelöst wurde |
| 2 | `phase3_edge/CLAUDE.md`, Abschnitt „Umgebungsstand" | „**Tailscale ist auf dieser VM nicht installiert.**" | Stand aus Step 0 und inzwischen falsch — der Funnel läuft, die Abnahme lief öffentlich über `…tail89fc2a.ts.net`. Der daran hängende `[VERIFY]` (V13) bleibt trotzdem offen, aber mit anderer Begründung |
| 3 | `ROADMAP.md`, Phase 3, Abschnitt DRIN | „**Cloudflare Tunnel**", „`LoadCredential`" | Gebaut wurde **Tailscale Funnel** (P3-A) und **`LoadCredentialEncrypted`** (P3-F). Der Statusabsatz darunter wurde gepflegt, die Scope-Zeile nicht |
| 4 | Root-`CLAUDE.md`, „Noch nicht entschieden" | „Ob der Kollege einen eigenen Server-Prozess oder nur einen eigenen Space bekommt." | **Entschieden in P3-G** und live bewiesen: ein Prozess, ein Space je Person. Die Zeile gehört gestrichen bzw. mit Datum nach „entschieden" verschoben |
| 5 | Root-`CLAUDE.md`, R3 | „Start mit Cloudflare Tunnel, Migration auf VPS + WireGuard als P3-Option" | R4 hat eine datierte P3-Ergänzung bekommen, R3 nicht. Historisch korrekt als Beschlusslage, aber ohne Hinweis auf das, was tatsächlich gebaut wurde |

**Nachtrag (2026-07-28, P4 Step 0): Fund 1 oben ist selbst falsch.** `export_space_map.py`
zeigte zu Beginn von P4 Step 0 real **drei** aktive Spaces: `fabian`, `niklas` **und
`nikinger`** — keine doppelt gezählte `fabian`-Hash, sondern ein dritter, echter Eintrag. Der
`nikinger`-Token stammte aus P2 Step 3 (erste eigene Space-Benennung, vor der B2-Umbenennung
`nikinger/` → `niklas/`) und war nie widerrufen worden, obwohl das Verzeichnis seit 2026-07-26
`niklas/` heißt — die B2-Prüfung („kein `nikinger` mehr") verglich nur den Dateibestand, nie den
Keyring. Der Token war live und schreibfähig (`Store.create()` legt Zielverzeichnisse mit
`mkdir(parents=True, exist_ok=True)` automatisch an), aber dormant: `nikinger/` existierte zum
Prüfzeitpunkt nicht unter `DATA_ROOT`. Der Nikinger hat den Fund bestätigt und den Token
widerrufen (`issue_token.py --revoke nikinger`, 2026-07-28) — `export_space_map.py` zeigt seither
wieder genau zwei Spaces. **Fund 1 dieser Tabelle wird nicht rückwirkend korrigiert** (📕-Snapshot-
Konvention) — dieser Nachtrag ist die richtige Zahl.

**Methode für die restliche Suche** — nicht alles lesen, sondern gezielt greppen:

```bash
# Zahlwörter und Mengenangaben, die beim Komprimieren gern kippen
grep -rn -E "\b(zwei|drei|vier|beide|alle drei)\b" --include="*.md" .

# Technologien, die in P3 ersetzt wurden
grep -rni -E "cloudflare|quick.?tunnel|LoadCredential\b" --include="*.md" .

# Behauptungen über den Maschinenzustand, die altern
grep -rn -E "nicht installiert|noch nicht|existiert nicht" --include="*.md" .

# Testzahlen gegen die Wahrheit prüfen
pytest -q | tail -3        # gegen die Modultabelle in phase3_edge/CLAUDE.md halten
```

**Die eine Prüfung, die alles Übrige entscheidet** — wie viele Token wirklich aktiv sind:

```bash
python phase3_edge/scripts/export_space_map.py | python -c "import json,sys; m=json.load(sys.stdin); print(len(m), sorted(set(m.values())))"
# erwartet: 2 ['fabian', 'niklas']
```

Weicht diese Zahl ab, ist das **kein Doku-Problem, sondern ein Befund**: dann existiert ein
Token, das niemand mehr zuordnen kann. Dann sofort stoppen und dem Nikinger melden, nicht
selbst aufräumen.

**Regeln für das Fixen:** `📕`-Snapshots (`P3_ABNAHME_2026-07-27.md`, die Pläne) werden **nicht**
rückwirkend korrigiert — sie bekommen bei Bedarf einen datierten Nachtrag, so wie es dort schon
gehandhabt wurde. Lebende Dokumente (`ROADMAP.md`, Root-`CLAUDE.md`, Phase-Heads, `docs/INDEX.md`)
werden direkt korrigiert, mit datierter Korrekturnotiz, wie es die Arbeitsweise vorschreibt.

---

## 6 Offene Entscheidungen für die P4-Planungssession

Diese gehören **in den Browser-Chat vor dem Plan**, nicht in Claude Code:

1. **Eigener Authorization Server oder delegiert?** Ein eigener AS ist der Lerneffekt, den R6
   meint — und gleichzeitig die Komponente, bei der eigene Fehler am teuersten sind.
2. **Was passiert mit dem Pfad-Token während der Migration?** Parallelbetrieb (beide Wege
   gleichzeitig gültig) ist bequem und verlängert genau das Risiko, dessentwegen P4 vorgezogen
   wurde. Ein harter Schnitt ist sauberer und kostet einen Abend Downtime für zwei Personen.
3. **Wo leben Client-Registrierungen, Codes und Refresh-Tokens?** Der Keyring ist dafür nicht
   gebaut, `DATA_ROOT` wäre eine Vermischung von Nutzdaten und Auth-Zustand. Wahrscheinlich eine
   eigene SQLite unter `StateDirectory=` — vor dem Plan entscheiden, nicht währenddessen.
4. **Verzeichnis- und Paketmuster:** `ROADMAP.md` sieht `phase4_auth/` · Paket `auth` vor. P3 hat
   bewusst kein Paket angelegt; P4 hat echten Servercode und sollte wieder eines bekommen —
   dann aber mit klarer Antwort darauf, ob `mcpserver` von `auth` abhängt oder umgekehrt.
5. **`[VERIFY]` vor dem Plan, nicht darin:** Anthropics aktuelle Anforderungen an OAuth-Connectors
   (Callback-URLs, unterstützte Spec-Version, DCR-Pflicht) ändern sich schneller als dieses
   Repo. Das gehört recherchiert, bevor Entscheidungen gelockt werden — die `ROADMAP.md` markiert
   es bereits so.
6. **Scope-Modell:** Braucht P4 überhaupt Scopes, wenn es zwei Nutzer und ein
   Space-je-Principal-Modell gibt? Die ehrliche Antwort ist womöglich „nein" — aber sie sollte
   begründet im Plan stehen, statt stillschweigend zu fehlen.

---

## 7 Wo alles steht

| Was | Pfad |
|---|---|
| Vollständiger P3-Plan, Entscheidungen P3-A–P3-N | `docs/concepts/phase3_edge_plan.md` |
| Was live tatsächlich funktioniert hat, Befunde B5/B6 | `docs/concepts/P3_ABNAHME_2026-07-27.md` |
| Befunde B3/B4, Umgebungsinventar aus Step 0, neun Session-Blöcke | `phase3_edge/SESSIONS_ARCHIVE.md` |
| Phase-Head: Runbooks, Modulstatus, Inbetriebnahme-Sequenz | `phase3_edge/CLAUDE.md` |
| Servercode aus P3 | `phase2_mcp/mcpserver/request_log.py`, `config.py`, `credentials.py`, `app.py` |
| Units, Ops-Skripte, deren Tests | `phase3_edge/systemd/`, `phase3_edge/scripts/`, `phase3_edge/tests/` |
| Übersichtsgrafik der Phase | `docs/concepts/phase3_edge_uebersicht.svg` |
| Vorgänger-Handover | `docs/concepts/PHASE2_CLOSEOUT_HANDOVER.md` |

**Indexzeile für `docs/INDEX.md`** (Abschnitt „Completed phases", im selben Commit):

```
- [docs/concepts/PHASE3_CLOSEOUT_HANDOVER.md](./concepts/PHASE3_CLOSEOUT_HANDOVER.md) — 📕 ~12KB · Abschluss-Handover P3→P4: Status, Delta seit dem P2-Handover, [VERIFY]-Bilanz V1–V13, geerbte Abnahmezeilen 6/12/13, Doku-Drift-Liste aus der Autocompact-Session, offene Entscheidungen für die OAuth-Planung
```

---

## 8 Rotationsprüfung

Geprüft gegen den Drive-Stand vom 2026-07-28 05:10: **`phase3_edge/CLAUDE.md` trägt genau einen
`## Session stopped`-Block** (2026-07-28), und `SESSIONS_ARCHIVE.md` enthält laut Indexzeile neun
archivierte Blöcke. Die Rotation ist also gelaufen, es ist **nichts zu verschieben**.

Was ein Browser-Chat nicht prüfen kann, ist die Byte-Identität der Reassemblierung. Falls
gewünscht, ist das im Repo eine Zeile:

```bash
grep -c '^## Session stopped' phase3_edge/CLAUDE.md      # muss 1 sein
grep -c '^## Session stopped' phase3_edge/SESSIONS_ARCHIVE.md
```
