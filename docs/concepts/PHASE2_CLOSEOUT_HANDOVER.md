---
status: snapshot
purpose: Abschluss-Handover P2→P3 — Status, Delta seit dem P1-Handover, offene Entscheidungen, [VERIFY]-Bilanz V1–V9
read-when: Start der P3-Planungssession, vor dem Entwurf des Claude-Code-Plans
detail: L2
up: ../../ROADMAP.md
down:
  - ./phase2_mcp_plan.md                      # Entscheidungen P2-A–P2-N, Steps 0–7
  - ./P2_ADAPTER_ABNAHME_2026-07-26.md        # Live-Abnahme, 21/21, Befunde B1/B2
  - ../../phase2_mcp/CLAUDE.md                # Phase-Head, Modulstatus, Runbook
updated: 2026-07-26
---
# Phase 2 → Phase 3 — Abschluss-Handover

> **Für den P3-Planungschat, vor dem Entwurf des Claude-Code-Plans.**
> Dies ist **kein zweiter Plan**. Was P2 gebaut hat, steht im Code; wie es entworfen wurde, in
> `phase2_mcp_plan.md`; was live bewiesen wurde, in `P2_ADAPTER_ABNAHME_2026-07-26.md`. Hier
> steht nur, was ein kalter Leser wissen muss, **bevor** er plant: Status, Delta, offene
> Entscheidungen, Verweise.

---

## 1 Status

Phase 2 ist **abgeschlossen und live-verifiziert** (2026-07-26). Steps 0–7 fertig, 10 Module im
Paket `mcpserver`, **133 Tests grün** (76 P1 + 57 P2), `mcp_smoke.py` 12/12 als Beweis-Skript.
Der Nikinger hat die Quick-Tunnel-Probe durchgeführt und darüber hinaus eine vollständige
Adapter-Abnahme über den echten Custom Connector gefahren: **21 von 21 Prüfungen** gegen den
echten `DATA_ROOT`, mit Rohantworten als Beleg. Beide dabei gefundenen Befunde sind geschlossen.
**Keine offenen Code- oder Daten-Findings.**

Was das praktisch heißt: Claude liest und schreibt über einen lokalen `fastmcp`-Server auf den
P1-Storage-Kern. Der Weg nach außen existiert bisher nur als **ephemere** Probe — dauerhaft
erreichbar zu werden, ist genau der Auftrag von P3.

---

## 2 Delta seit `PHASE1_CLOSEOUT_HANDOVER.md`

Was sich am Projekt geändert hat und **nicht** neu hergeleitet werden muss:

| Was | Wo nachlesen |
|---|---|
| **Phasen umnummeriert.** OAuth ist jetzt **P4**, Web-UI **P5**. Begründung: der Pfad-Token soll kurz leben, die UI darf unter Druck wegfallen, OAuth nicht. | `ROADMAP.md` (Korrektur 2026-07-25), `phase2_mcp_plan.md` §0.3 |
| **Der P1-Contract wurde dreimal erweitert und ist wieder zu.** `Store.space_of()`, `Store.get(..., repair_drift=)`, Statusvalidierung über `models.STATUS_VALUES`. Einmalig, freigegeben, getestet. | `phase1_storage/CLAUDE.md`, Abschnitt „Geerbte Contracts" |
| **D1–D6 sind erledigt.** Alle sechs offenen Punkte des P1-Handovers sind entschieden und umgesetzt — bis auf D6, das bewusst zurückgestellt wurde. | `phase2_mcp_plan.md` §0.4, `ROADMAP.md` „Zurückgestellt aus P2" |
| **Toter Code entfernt** (`files.rename_for_new_slug()`), P1-Testzahl dadurch von 70 auf 68 und mit den P2-Erweiterungstests auf 76. | `phase1_storage/CLAUDE.md` |
| **Rotationsskript existiert.** `scripts/rotate_session_block.sh <phase_verzeichnis>` — P3 benutzt es **ab dem ersten Session-Block**, nicht als späteren Rettungseinsatz. | Root-`CLAUDE.md`, „Doku-Hygiene" |
| **Hard Rule 1 hat eine Pfadkorrektur.** `storage/credentials.py` wurde nie gebaut; der reale Pfad ist `phase2_mcp/mcpserver/credentials.py`. Die Regel selbst ist unverändert. | Root-`CLAUDE.md`, Hard Rule 1 |
| **Space-Namen sind bereinigt.** Es existiert genau **ein** Space: `niklas` (3 Items). `nikinger/` gibt es nicht mehr. **`fabian` existiert noch nicht.** | `phase2_mcp/CLAUDE.md`, Befund B2 |
| **Zwei Token-Klartext-Vorfälle sind dokumentiert** (Step 3 und während der Abnahme). Token rotiert, Screenshot nie versioniert, Datei nachträglich entfernt. | `phase2_mcp/CLAUDE.md` + `SESSIONS_ARCHIVE.md` |

**Der letzte Punkt ist für P3 kein Nebensatz.** P3 baut strukturiertes Request-Logging und
systemd-Units — also genau die zwei Mechanismen, die einen Pfad-Token dauerhaft auf Platte
schreiben würden. Zweimal in einer Phase ist ein Muster, kein Zufall.

---

## 3 Was P3 technisch vorfindet

Nur Einstiegspunkte. Details stehen im Code.

| Thema | Datei | Was P3 damit tut |
|---|---|---|
| Prozessstart, CLI-Flags | `phase2_mcp/scripts/serve.py` | wird von der systemd-Unit aufgerufen; `--allowed-host` existiert bereits |
| App-Komposition, Routen | `mcpserver/app.py` | `/health` ist schon da (in P2 vorgezogen) |
| Konfiguration über Env | `mcpserver/config.py` | `SPACE_DATA_ROOT` · `SPACE_HOST` · `SPACE_PORT` · `SPACE_LOG_LEVEL` |
| Logging, Token-Scrubbing | `mcpserver/logging_setup.py` | P3 erweitert auf Request-Log mit Tool-Name und Dauer |
| Secrets | `mcpserver/credentials.py`, `scripts/issue_token.py` | P3 entscheidet Keyring vs. systemd `LoadCredential` |
| Auth-Seam | `mcpserver/auth.py` (`SpaceResolver` → `Principal`) | **P4 tauscht hier**, nicht in `tools.py` |
| Rechte-Seam | `mcpserver/permissions.py` (`can_read` heute immer `True`) | von jedem Lesepfad bereits aufgerufen |
| Runbook Quick-Tunnel | `phase2_mcp/CLAUDE.md` | **Reihenfolge beachten: Tunnel zuerst, dann `serve.py`** |

Zur letzten Zeile: die ursprüngliche Runbook-Reihenfolge war zirkulär, weil die
trycloudflare-Subdomain erst beim Tunnelstart entsteht. Korrigiert, aber die zugrunde liegende
Eigenschaft bleibt — und sie ist der Kern der ersten P3-Entscheidung unten.

---

## 4 Offene Entscheidungen für die P3-Planung

Keine davon ist entschieden. Sie brauchen den Nikinger, nicht Claude Code.

1. **Tunnel-Variante — die eigentliche Entscheidung der Phase.** Quick Tunnel vergibt bei jedem
   Start eine neue Zufalls-Subdomain. Ein Connector, der „stehen bleibt" (P3-Mission), ist damit
   unvereinbar. Also: Named Tunnel (braucht Cloudflare-Account **und** verwaltete Domain) oder
   direkt VPS + WireGuard (R3 nennt es als P3-Option). Das ist eine Kosten- und
   Lernaufwand-Frage, keine technische.
2. **Wie kommt der Token in den Dienst?** Der Keyring braucht eine Session; ein systemd-Dienst
   hat keine. `LoadCredential` ist der in Hard Rule 1 vorgesehene Weg — betrifft
   `credentials.py` und ist damit ein Eingriff in P2-Code.
3. **Bekommt der Kollege einen eigenen Space oder einen eigenen Serverprozess?** Steht seit
   2026-07-24 offen in Root-`CLAUDE.md`. Muss **vor** der systemd-Unit entschieden sein, sonst
   wird die Unit zweimal geschrieben.
4. **Wer legt `fabian` an, und wann?** Der Space existiert nicht. Damit ist Cross-Space-Lesen
   real bis heute nur gegen einen Alt-Space getestet worden, nicht gegen einen zweiten Nutzer.
5. **MCP-Revision 2026-07-28 — in zwei Tagen final.** Sessions entfallen, `Mcp-Method`/`Mcp-Name`
   werden Pflicht. P2 hat bewusst gegen 2025-11-25 gebaut und ist bereits stateless. Die Frage
   ist nur noch: Migration **in** P3 oder danach. Mit Datum entscheiden, nicht mit Gefühl.
6. **Request-Log-Format.** Tool-Name und Dauer sind Scope. Der Request-Pfad enthält den Token —
   Scrubbing ist Pflicht, nicht Option (siehe §2, letzter Absatz).
7. **Backup des `DATA_ROOT`.** Das Datenverzeichnis ist ein Git-Repo auf Branch `master` **ohne
   Remote**. „Backup" steht im P3-Scope, das Ziel nicht.
8. **D6 jetzt oder später?** `Store.search()` liest jede indizierte Datei von der Platte. P3
   hängt den Server an einen Mobilfunk-Uplink — falls es je einen Moment für diese Optimierung
   gibt, dann diesen. Kostenfrage, kein Bug.

---

## 5 `[VERIFY]`-Bilanz der Phase

Alle neun Marker aus `phase2_mcp_plan.md` §8. **Acht aufgelöst, einer nur synthetisch.**

| # | Marker | Ergebnis |
|---|---|---|
| V1 | Repo-Stand nach P1-Abschluss (Blocküberschrift, Rotationsskript, Indexzeile) | ✅ in Step 0 aufgelöst |
| V2 | `fastmcp`-Version, Signatur von `http_app(...)` | ✅ aufgelöst — `>=3.4,<3.5` läuft live |
| V3 | Importpfad der Request-Dependency | ✅ aufgelöst — `context.py`, Guard greift |
| V4 | `Mount("/mcp")` + Pfad-Umschreibung | ✅ aufgelöst — `asgi.py`, live bewiesen |
| V5 | Keyring-Backend auf der VM | ✅ aufgelöst — echter Roundtrip vom Nikinger bestätigt |
| V6 | Python ≥ 3.10 auf der VM | ✅ implizit aufgelöst |
| V7 | Custom Connectors auf **Pro** ohne Owner-Gate | ✅ aufgelöst — Connector selbst angelegt, funktioniert |
| V8 | Größenbudget gegen echte Daten | ⚠️ **nur synthetisch** — `mcp_smoke.py` misst gegen >20 selbst erzeugte Items; der echte `DATA_ROOT` hat 3 Items. Die Zahl stimmt, der Realitätstest steht noch aus |
| V9 | Space-Verzeichnisse im echten `DATA_ROOT` | ✅ aufgelöst — Befund B2, `nikinger/` → `niklas/` umbenannt |

**Neue, noch unaufgelöste Marker, die P3 erbt:**

- `[VERIFY]` **MCP-Revision 2026-07-28** gegen die dann finale Spec (siehe §4.5).
- `[VERIFY]` **Anthropic-Callback-URLs und unterstützte Auth-Spec-Version** — steht in
  `ROADMAP.md` bei P4, ändert sich schneller als das Dokument.
- `[VERIFY]` **V8 gegen einen realen Datenbestand**, sobald es einen gibt.

---

## 6 Doku-Drift, die in Step 0 der P3 gehört

Vier Kleinigkeiten, alle einzeilig, alle würden sonst später als Widerspruch auffallen:

1. Root-`CLAUDE.md`, **R5** sagt noch „OAuth 2.1 + DCR ist **Phase 5**". Seit der
   ROADMAP-Korrektur vom 2026-07-25 ist OAuth **P4**.
2. `ROADMAP.md` (P2-Abschnitt „DRIN") und `phase2_mcp/CLAUDE.md` (Abschnitt „Scope") tragen beide
   noch **`fastmcp` über Streamable HTTP `[VERIFY]`**. Der Marker ist live widerlegt — er gehört
   entfernt, nicht mitgeschleppt.
3. `ROADMAP.md`s `down:`-Liste nennt nur `phase1_storage_plan.md`, nicht den P2-Plan.
4. `docs/INDEX.md`: P2 wandert von „Active phase" nach „Completed phases" (🔄 → 📗), ein neuer
   Abschnitt für die aktive P3 kommt dazu, und dieses Dokument braucht seine Zeile:

```
- [docs/concepts/PHASE2_CLOSEOUT_HANDOVER.md](./concepts/PHASE2_CLOSEOUT_HANDOVER.md) — 📕 ~11KB · Abschluss-Handover P2→P3: Status, Delta seit dem P1-Handover, offene Entscheidungen für die Exposure-Phase, [VERIFY]-Bilanz V1–V9
```

---

## 7 Was P3 **nicht** anfassen sollte

- **`tools.py`, `permissions.py`, die Fachlogik in `auth.py`.** P3 ist Betrieb, nicht
  Fachlichkeit. Ein Änderungsbedarf dort ist ein Befund für den Nikinger, keine Aufgabe.
- **Der P1-Contract.** Er wurde in P2 Step 2 einmalig und freigegeben geöffnet und ist wieder zu.
- **Keine neuen Tools.** Sechs sind sechs. Wer ein siebtes braucht, braucht erst eine
  Planungssession.
- **OAuth.** Das ist P4, und der Seam dafür steht bereits.

---

## 8 Verweise

| Zweck | Pfad |
|---|---|
| Vollständiger P2-Plan, Entscheidungen P2-A–P2-N | `docs/concepts/phase2_mcp_plan.md` |
| Live-Abnahmeprotokoll, 21/21, Befunde B1/B2 | `docs/concepts/P2_ADAPTER_ABNAHME_2026-07-26.md` |
| Phase-Head P2: Modulstatus, Runbook, Session-Block | `phase2_mcp/CLAUDE.md` |
| Session-Historie P2, verbatim, newest-first | `phase2_mcp/SESSIONS_ARCHIVE.md` |
| Geerbter P1-Contract + die drei Erweiterungen | `phase1_storage/CLAUDE.md` |
| Phasenplan und Scope-Grenzen P3–P5 | `ROADMAP.md` |
| Herkunft der Rahmenentscheidungen R1–R6, Hard Rules | `CLAUDE.md` |
| Workflow-Prompts (Session-Start, Kickoff, Abschluss) | `docs/PROMPTS.md` |
