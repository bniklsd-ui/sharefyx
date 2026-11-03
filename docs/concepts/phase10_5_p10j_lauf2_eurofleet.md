---
status: live
purpose: Übergabe-Notiz an die eurofleet-Session — P10.5-28 „Live P10-J Lauf 2": opencode mit einem lokalen Modell (Ollama, CT 111) führt live `list_spaces` gegen Sharefyx aus. Was zu tun ist, was als Beleg zählt, was tabu ist.
read-when: die eurofleet-Session übernimmt P10.5-27/28 und die Anbindung aller opencode-Instanzen — diese Datei ganz lesen
detail: L2
up: ../../phase10_5_finishing/CLAUDE.md
down:
  - ./phase10_5_finishing_plan.md   # 📕 §6.7 Live-Abnahme P10-J (Topologie, Config, V214/V218)
updated: 2026-11-03 (Nikinger: auch Lauf 1 (P10.5-27) und die Anbindung **aller** opencode-Instanzen gehen an eurofleet; Wegwerf-Generalprobe grün, §6) | 2026-11-01 (angelegt, Claude Code — Nikinger: Lauf 2 geht an eurofleet, weil eurofleet die Container verwaltet)
---
# P10.5-28 — P10-J Lauf 2 an eurofleet (Übergabe)

> **Auftrag (Nikinger, 2026-11-01):** „i suggest leaving the 28 to eurofleet, since that manages the
> containers (write it a note, ill tell the session its there)". Lauf 1 (P10.5-27, MiniMax M3.1 Flash)
> macht der Nikinger selbst.

## 1. Warum das wichtig ist

Phase 10.5 endet erst, wenn ein **Nicht-Claude-Client** live `list_spaces` ausführt — mit **zwei**
Modellanbietern (Lock P10-J). Lauf 2 ist der zweite Anbieter: ein **lokales Modell** über Ollama auf
CT 111 (Lock P10.5-K). Der Server sieht in beiden Läufen denselben Client (opencode); der Unterschied
liegt allein beim Modell. Mit P10.5-27 zusammen ist das die Abschlussbedingung der Phase (P10.5-60).

## 2. Was zu tun ist

| # | Schritt | Hinweis |
|---|---|---|
| 1 | opencode auf einem Host, der **CT 111** (`http://192.168.68.140:11434`) **und** `https://sharefyx.eurofyx.com/mcp` erreicht | Container nach eurofleet-Konvention; nicht die Sharefyx-VM (5,8 GiB RAM, kein GPU) |
| 2 | Ollama-Provider in opencode: OpenAI-kompatible `baseURL` `http://192.168.68.140:11434/v1` | `[VERIFY V214]` — Erreichbarkeit vom opencode-Host zuerst prüfen |
| 3 | Modell mit **Tool-Aufrufen** wählen: zuerst `qwen2.5vl:7b` (liegt schon auf CT 111) prüfen; kann es keine Tools, ein kleines Textmodell mit Tool-Unterstützung **auf CT 111** ziehen | Modelle **nur** auf CT 111 ziehen (`/api/pull`, nacheinander, `/api/delete` zwischen Kandidaten) — nie auf der Sharefyx-VM (Vorfall 2026-10-18) |
| 4 | MCP-Server in `opencode.json`: `mcp.sharefyx = {type: "remote", url: "https://sharefyx.eurofyx.com/mcp", oauth: {}}`, dann `opencode mcp auth sharefyx` | `[VERIFY V218]`. **Der Login braucht einen Menschen** (Passwort + TOTP des eigenen Kontos) — Browser und der Callback-Lauscher von opencode (Port 19876) auf **derselben** Maschine, sonst `ssh -L 19876:127.0.0.1:19876 <host>` |
| 5 | Prompt: „Rufe list_spaces auf." | Ergebnis: die eigenen Spaces |

## 3. Was als Beleg zählt

- ein **Bildschirmfoto** (oder Textmitschnitt) des Tool-Ergebnisses in opencode, mit sichtbarem Modellnamen;
- die **Journalzeile** des Sharefyx-Dienstes mit `ev=tool`, `tool=list_spaces`, `ok=true` und der
  `client_id` von opencode — auslesen darf das der Nikinger (`journalctl -u sharefyx-mcp`), oder er gibt
  sie frei;
- Modell, Ollama-Version und opencode-Version.

Diese Belege kommen in die Zeile **P10.5-28** im Phase-Head (`phase10_5_finishing/CLAUDE.md`, Abnahmestand),
datiert. Wer den Head nicht schreiben soll, gibt sie dem Nikinger.

## 4. Tabu (Hard Rules, Wurzel-`CLAUDE.md`)

- **Kein Secret in eine Datei.** Das OAuth-Token gehört opencode (dessen eigener Speicher), nie ins Repo,
  nie in eine Notiz, nie in einen Commit.
- **Den Dienst `sharefyx-mcp.service` nicht anfassen** — kein `systemctl`, kein `kill`. Er läuft live,
  zwei Menschen nutzen ihn.
- **Kein Schreib-Werkzeug** im Lauf: `list_spaces` reicht. Der Lauf arbeitet gegen echte Daten.
- **Kein LLM in den Server.** Das Modell ist Client-Sache — genau das beweist dieser Lauf.

## 5. Wenn es scheitert

Bekannte Fallen aus der Wegwerf-Probe (P10.5-26, `phase10_5_finishing/probes/p105_b6_opencode_e2e.py`):
ein `405` auf `GET /mcp` ist **normal** (keine Ursache); `opencode mcp debug` **vor** dem Lauf verfälscht
das Ergebnis. Ruft das Modell das Werkzeug nicht auf, liegt es fast immer am Modell (keine Tool-Aufrufe),
nicht am Server — dann das nächste Modell auf CT 111 probieren und das Ergebnis je Modell notieren.

## 6. Nachtrag 2026-11-03 — Lauf 1 geht ebenfalls an eurofleet, danach alle Instanzen

> **Auftrag (Nikinger, 2026-11-03):** „that is a job for eurofleet … we want to connect all opencode instances
> now that it's proven working." Damit liegen **beide** Läufe (P10.5-27 **und** P10.5-28) bei eurofleet.

**Was bewiesen ist** (Wegwerf-Generalprobe, `phase10_5_finishing/probes/p105_p10j_lauf1_wegwerf.py`, Beleg
`…_wegwerf.json`, Gegenlauf `…_gegenlauf_skip_auth.json`): der **installierte** opencode 1.18.33 + das **bezahlte**
`minimax/MiniMax-M3.1-Flash` durchläuft Registrierung → Consent → Token → das Modell ruft `sharefyx_list_spaces`
**selbst** auf; der Server loggt `ev=tool list_spaces ok=true`. Ohne den Consent-Schritt sieht das Modell kein
Werkzeug (Gegenlauf rot). Ein Lauf hing einmal im Timeout (nicht reproduziert, Ursache offen) — melden, falls er live
wieder auftritt.

**Lauf 1 (P10.5-27) — Rezept**, je Instanz in deren **eigener** Konfiguration:
1. `mcp.sharefyx = {type: "remote", url: "https://sharefyx.eurofyx.com/mcp", enabled: true}`; beim Agenten
   `agent.build.tools = {"sharefyx_*": true}` (in der Probe gesetzt, ob es ohne geht ist nicht gemessen). Kein
   `NODE_TLS_REJECT_UNAUTHORIZED` — live gibt es ein echtes Zertifikat.
2. `opencode mcp auth sharefyx` — **der Login braucht einen Menschen** (Passwort + TOTP des Kontos, Callback-Lauscher
   von opencode auf `127.0.0.1:19876`). Die Probe ersetzt den Menschen durch Chromium **nur** an der Wegwerf-Instanz mit
   Wegwerf-Konto; **live gibt es keine Automatisierung des Logins** (Passwort/TOTP-Seed sind Secrets, Hard Rule 1).
3. `opencode run "Rufe das Werkzeug list_spaces auf und nenne mir die Namen der Spaces." --model minimax/MiniMax-M3.1-Flash`.
4. Beleg wie §3 (Mitschnitt mit Modellname + Journalzeile `ev=tool`, `ok=true`, `client_id`).

**Alle opencode-Instanzen anbinden:** dasselbe Rezept pro Instanz; **jede** Instanz registriert sich selbst (DCR) und hält
**ihren eigenen** Token im eigenen Speicher (`<XDG_DATA_HOME>/opencode/mcp-auth.json`) — kein geteilter Token, nichts
ins Repo. Ob und welche Instanzen es außer der auf dieser VM gibt (Fleet-Dienst `opencode serve`, Port 4096, Tailnet),
weiß diese Notiz nicht — das ist eure Inventur. Zwei Dinge, die der Server nicht entscheidet, sondern die Konten:
welcher Principal (Space) jede Instanz sehen darf, und ob eine Instanz **schreiben** soll (der Lauf selbst: nur `list_spaces`).

**Phasenschluss:** P10.5-60 (P10-J zweimal live belegt) und das Closeout (Block Z) hängen an **diesen beiden Läufen**.
Meldet die Belege an den Nikinger; er trägt sie in P10.5-27/28/60 ein.
