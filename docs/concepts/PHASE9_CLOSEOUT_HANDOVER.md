---
status: snapshot
purpose: "Abschluss-Handover P9 → P10 — Status, Delta seit dem P8.6-Handover, offene Entscheidungen für die P10-Planung (ergänzt die Sammelstelle phase10_intake.md, ersetzt sie nicht), [VERIFY]-Bilanz, P1-Contract, und die Auswertung des Open-Tests MiniMax M3/M3.1 (Spacebunny) als offener, nicht blinder Datenpunkt. Phase 9 ist abgeschlossen und als v3.1.4 live."
read-when: vor dem Entwurf des P10-Plans einmal ganz lesen, zusammen mit phase10_intake.md — ersetzt das Nachlesen von Phase-Head und SESSIONS_ARCHIVE für alles außer der Detailhistorie
detail: L2
up: ../../ROADMAP.md
down:
  - ./phase10_intake.md                              # P10-Sammelstelle — das Register beginnt dort, nicht hier
  - ./phase9_hardening_plan.md                       # 📕 Plan, Locks P9-A–P9-U, §15 die ursprüngliche P10-Liste
  - ./phase9_hardening_block_feedback_plan.md        # letzter Block, Locks P9-BG–P9-BQ, §3 E2/E3 → P10
  - ../../phase9_hardening/ABNAHME_MATRIX.md         # kanonischer Closeout: Bilanz + Teile
  - ../../phase9_hardening/CLAUDE.md                 # Phase-Head, Modulstatus
  - ../../phase9_hardening/SESSIONS_ARCHIVE.md       # volle Phasenhistorie, verbatim, newest-first
  - ./phase9_hardening_uebersicht.svg                # Übersichtsgrafik
updated: 2026-10-08 (Abschluss-Handover P9 → P10, nach dem Deploy v3.1.4; mit Auswertung des Open-Tests MiniMax/Spacebunny auf Wunsch des Nikingers)
---
# Phase 9 — Closeout-Handover (P9 → P10)

> **Phase 9 ist abgeschlossen und ausgeliefert.** `v3.1.4` läuft seit dem **2026-10-08** aus Release
> `20261008T201607.460757Z`, SHA **`d04c0ec`**, `health_gate.sh` **9/9 OK**, Release-`pytest` **1265 passed**.
> Abnahme **121 ✅ · 12 ⚠️ · 1 ⬜** von 134 Zeilen, `[VERIFY]` **40 ✅ · 1 ⚠️ · 3 ⬜**. Kein offener Rest ist Code-Arbeit.

## 1 Status in fünf Sätzen

1. Geplant war eine **Härtungsphase in acht Steps** (Plan 2026-09-19, Lock P9-A); gebaut wurden die acht Steps **plus sieben Blöcke**, die
   unterwegs aus Befunden und Sichtprüfungen entstanden (doing, trace, Buttons-Extra, settings, drei Bildsichtungen, feedback).
2. Der Betrieb ist härter: **eigene Domain** `sharefyx.eurofyx.com` über einen VPS (Funnel bleibt Fallback, alte Adresse schreibt
   unbefristet), **Watchdog** live und am echten Ausfall belegt, **Vision-Dienst** auf der RTX 3060 (26,8 s statt 46–180 s Cold-Start).
3. Das Schema ist zweimal angekündigt geöffnet worden (`doing`/`assignee`, `updated_by` + Git-Autor) — **ohne Migration**, beim zweiten
   Mal ohne Index-Neuaufbau; Löschen existiert jetzt, **human-only**, nach `DATA_ROOT/._trash/`.
4. Fünf Deploys in der Phase (`v3.1.0` 10-02 · `v3.1.1` 10-03 · `v3.1.2` 10-05 · `v3.1.3` 10-07 · `v3.1.4` 10-08), jeder mit echter
   Gate-Ausgabe im Commit; Service-Touch durch einen Agenten **0**.
5. **126 Commits** seit `06ab4f6`, `pytest` **995 → 1265**, `ui_budget` 5/5 (144,7 → **173,1 KB** von 250 KB).

## 2 Delta seit dem P8.6-Handover

| Block | Ergebnis | Zeiger |
|---|---|---|
| 0 Doku-Fundament | INDEX-Rotation, `doc_health.py`, später Rotations-/Verschiebe-Werkzeuge (`rotate_*`, `archive_index_entries.sh`, `move_sections.py`, `prepend_updated_chain.sh`) | Matrix P9-1–9 |
| A Domain | VPS + Caddy + `socat`-Relay (Plan-A4 war unbaubar, P3-B), A7/A8 harter Schnitt, `LEGACY_UNTIL=open` | `step_a/RUNBOOK_STEP_A.md` |
| B Watchdog | polkit-JS-Regel (sudoers unbaubar unter `NoNewPrivileges`), `RuntimeDirectoryPreserve=yes` (Rate-Limit war nie in Kraft) | `step_b/RUNBOOK_STEP_B.md` |
| C Vision | LXC CT 111, Treiber 580.173.02, `devN`-Passthrough; das Modell selbst ist für Sichtprüfung **gestrichen** (Fehlaussagen) | Matrix P9-21–26 |
| D Bugs | Drop-Ziel Space-Wurzel ✅; ESC/macOS-Vollbild ist OS-Verhalten (V188), kein Code | Matrix P9-27–32 |
| E Karte | kein zweiter `/graph`-Abruf, Positionen bleiben; V118 → **eine** Linie | Matrix P9-33–37, 93 |
| F/G/H | `doing`/`assignee` (9. Öffnung) · Löschen `._trash/` · `fastmcp==3.4.7` exakt | Plan §8–§10 |
| doing · trace · Extra | fünfter Eimer „In Arbeit“ · `updated_by` + Git-Autor (10. Öffnung) · Knöpfe auf Standardfläche | Block-Pläne |
| settings + 3 Sichtungen | Einstellungen als Fensterkette, viele gemessene CSS-Korrekturen | `…_block_settings_plan*.md` |
| feedback | Anlegen im aktiven Space (echter Bug), Team-Spaces verschieben/löschen, Enter, Löschdialog, Übersicht | `…_block_feedback_plan.md` |

## 3 Abnahmestand

**121 ✅ · 12 ⚠️ · 1 ⬜** — die ⚠️ sind **benannte Abweichungen, keine offenen Punkte**, außer zwei, die P10 ein Urteil schulden:

- **P9-124** (Konfliktkopie im Browser nie gefahren) und **P9-127** (Enter nur für vier von elf Overlays im Browser belegt) — Proben ergänzen
  oder als ausreichend erklären.
- Die übrigen zehn (P9-15, 22, 27, 31, 55, 56, 72, 74, 97, 99) tragen ihre Begründung in der Zeile; nichts davon ist Code-Arbeit.
- **⬜ P9-13 / V150** — zweites Claude-Konto auf die neue Adresse; ein Termin, kein Blocker (Plan §0.1a).
- **Beim Closeout nachgetragen:** P9-133/134 (standen in keiner Tabelle), P9-36 ⚠️ → ✅ (Entscheidung 10-05 nie nachgezogen),
  V162 A ✅ — die **erste Live-Löschung** liegt seit 10-07 in `._trash/niklas/` (read-only gezählt).

## 4 Für die P10-Planung — was `phase10_intake.md` noch nicht trägt

Die Sammelstelle ist der Einstieg (§2 Wünsche, §3 Erbe, §4 Lieferumfang). **Ergänzen, nicht neu herleiten:**

| # | Posten | Herkunft | Art |
|---|---|---|---|
| 4.1 | **Tailnet-ACL**: das MacBook erreicht `100.93.43.122:8765` (Lauf 4 `open`); das Fragment ist additiv, die Live-ACL ist ungelesen | V162 B, P9-11 | Sicherheit, Entscheidung |
| 4.2 | **Sechs LAN-Ports auf `0.0.0.0`** (7070, 7777, 47984/89/90, 48010 — Sunshine u. a.) | Portscan Lauf 3b | Hygiene |
| 4.3 | **`/overview` = 6 Durchgänge × sichtbare Spaces** (~2,4 s Serverarbeit live); Ursache benannt, Messlatte 372,9 ms war falsch | P9-15, V151 | Performance (gehört zu intake §2.1) |
| 4.4 | Space-Liste bleibt leer, wenn „Spaces verwalten“ vor `loadOverview()` geöffnet wird | settings-Nachtrag | Bug |
| 4.5 | Transitives `mcp` ungepinnt (Dev 1.28.1, Live 1.30.0) | Step H | Lock-Entscheidung |
| 4.6 | Vision-Modell `qwen3-vl:8b` als Prüfwerkzeug gestrichen — Ersatz testen mit **einer** Frage bekannter Antwort, oder CT 111 stilllegen | Head §Backlog | Werkzeug |
| 4.7 | Übergangsfenster alte Adresse: `LEGACY_UNTIL=open` ist unbefristet — wieder befristen, sobald der Arbeitslaptop die neue Domain erreicht (Vermutung NRD-Sperre ~30 Tage, erneut testen um den **2026-11-02**) | settings-Plan §6 | Termin + Entscheidung |
| 4.8 | Kontrast der Vorsicht-Beschriftung **4,38:1** (unter AA) — „bleibt so“ (10-05), für P10 erneut bestätigen oder schließen | B17 | Design |
| 4.9 | **Ausführer für P10/P10.5** — der Open-Test ist beendet (§7), der Rest von P9 lief in Claude Code (Opus/Sonnet 5.5) | §7 | Entscheidung |
| 4.10 | `created_by` als P10-Option, falls die Git-Spur im UI sichtbar werden soll — wäre die **elfte** Öffnung | P9-BQ | Entscheidung |

**Zu bestätigen:** die Zweiteilung P10 (Register, kein Code) / P10.5 (Ausführung) aus intake §1 ist ein Vorschlag, kein Lock.

## 5 `[VERIFY]`-Bilanz V145–V194 + geerbte

**40 ✅ · 1 ⚠️ · 3 ⬜** (Nummern-Lesart, Zählregel in `ABNAHME_MATRIX_VERIFY.md`); V167–V172 sind **reserviert, unbelegt**.

- **Unaufgelöst, wandern nach P10:** **V150** (zweites Konto) · **V193** (Ordner umbenennen atomar?) · **V194** (was referenziert einen
  Space-Namen?) · **V120** (geerbt, Tab-Titel — jetzt intake §2.2).
- **Teilweise:** **V157** ⚠️ (WebKit ungemessen; für den gemeldeten Fall gegenstandslos) · **V162 Lesart B** ⚠️ (`tailscale serve --tcp`
  und ACLs: Docs schweigen; siehe 4.1).
- **Aufgelöst (Auswahl mit Folgen):** V148 Funnel kann keine eigene Domain · V149 alle Metadaten aus der Basis-URL · V151 VPS-Anteil
  2,4–3,6 % · V153 polkit statt sudoers · V160 `assignee` = Space-Name ohne Validierung · V161 ≤ 1,05 s Neuaufbau · V163 3.4.7-Fix inert ·
  V188 macOS-Vollbild ist OS-Verhalten · V189–V192 (feedback) · **V118** eine Linie · **V136** gegenstandslos am Anker.

## 6 P1-Contract

- **Neunte Öffnung (Step F, 2026-09-30):** `doing` in `STATUS_VALUES["task"]`, `assignee` mit Index-Spalte, Schema 3 → 4, keine Migration.
- **Zehnte Öffnung (trace, 2026-10-02):** `updated_by` (server-verwaltet, über keinen Kanal setzbar) + `actor` → Git-Autor; kein Schema-Sprung.
- Beide angekündigt, beide mit enger Probe genau drei Dateien. **Die elfte** stünde an für `created_by` (4.10) oder ein erweitertes
  Dateiformat im Editor (intake §2.3 Stufe 2) — beides ausdrücklich Nikinger-Entscheidung.
- Rechte: **Hard Rule 4 / P6-U gilt jetzt auch im Web-Pfad** (P9-BG); Team-Spaces erlauben Wegnehmen (P9-BP), fremde Home-Spaces nicht.
  MCP `update_item` folgt beim Ordnerwechsel in Team-Spaces **nicht** derselben Regel (`phase2_mcp/` war tabu) — intake §3.

## 7 Open-Test MiniMax M3 / M3.1 („Spacebunny“) — Fakten und offene Bewertung

> **Einordnung, zuerst:** N = 1, keine Vorregistrierung je Task, keine Wiederholung, und **diese Bewertung ist nicht blind** — die
> Modellidentitäten standen beim Lesen im Kontext (Item-Punkt 6 ist damit für diese Runde nicht erfüllbar). Ein Datenpunkt, kein Beweis.

**Fakten aus dem Repo (Commit-Grenzen nach Uhrzeit und Session-Blöcken, nicht nach Modell-Metadaten):**

| Marke | Commit | Zeit | Konfidenz |
|---|---|---|---|
| Start (Item angelegt 09-28 13:34) | `037d9ed` Step E | 09-28 16:16 | mittel — Block ohne Ausführer-Tag, Plan teilt E M3 zu |
| Wechsel M3 → M3.1 Preview (Notiz 09-30 17:24, Effort „max“) | Grenzfall `69ca248` Step H | 09-30 17:51 | niedrig — Notizzeit, keine Messung |
| Ende (Eskalation, MiniMax-Ausfall) | letzter M3: `ed13127` · Übernahme: `0c66277` (Claude Code) | 10-06 18:38 / 10-07 11:40 | hoch |

- Fenster `037d9ed^..ed13127`: **83 Commits**. Davon **16 mit Trailer Claude Opus 5.5** (10-01, 10-02, 10-05: Domain-Schnitt,
  Übergangsfenster, Mini-Pläne, Deploy-Fix, `v3.1.2`), **18 vor dem Wechsel** (M3: E, A-Vorbereitung und -Ausführung, F, G), **1 Grenzfall**,
  **48 nach dem Wechsel** M3.1 zugeordnet (B, A4, doing, trace, B17, Gate/Z-Doku, Matrix, Step-D-Probe, Rotationen, settings + drei Sichtungen).
- **Zuordnung ist Rekonstruktion:** nur 4 Commits tragen einen opencode-/MiniMax-Trailer; die übrigen sind über Session-Block-Köpfe
  (`opencode/M3`) und Plan-Zuteilung zugeordnet. Die Tage 10-03/10-04 haben teils keinen Ausführer-Tag (mittlere Konfidenz).

**Die zehn Item-Punkte, Datenstand:** (1) Grenzen ✅ jetzt oben · (2) Wechsel-Commit nur zeitlich · (3) Modell-ID je Commit **fehlt** ·
(4) Soll vor Ausführung ✅ (Pläne mit Locks und Abnahmezeilen je Block — die stärkste Grundlage) · (5) Fehlversuche nur als „eigene
Fehler“ in Blöcken, nicht systematisch · (6) blind ✗ · (7) Rubrik ✅ unten · (8) Kosten/Zeit **fehlen** · (9) Eingriffe nicht gezählt ·
(10) Harness-Konstanz nicht belegt — u. a. MCP-Timeout `local_vision` am 10-05 auf 600 s gesetzt.

**Offene Rubrik-Bewertung (1–5), M3 und M3.1 zusammen** — vor und nach dem Wechsel **nicht trennbar** (vorher nur zwei Tage, dieselben
Fehlerklassen in beiden Hälften):

| Dimension | Note | Beleg (Kurzform) |
|---|---|---|
| Korrektheit relativ zur Spec | 4 | jeder Block erfüllt seine Abnahme; Plan-Irrtümer per Messung gefunden (F 18 statt 9 Hunks, G Lösch-Ort, H-Prämisse, Plan-A4 unbaubar) |
| Testqualität | 3 | Gegenlauf-Kultur ist echt; zugleich wiederholt „Wächter prüft etwas anderes“ (die Blöcke zählen selbst bis zur neunten Wiederholung), ein Gegenlauf-Rig, das 4 von 6 Mutationen nie ausführte, ein Beleg, der der Gegenlauf selbst war |
| Plan-Treue | 5 | jede Abweichung datiert, Konflikte mit Locks zurückgegeben (B17-Konvention, P9-BA) statt still gebaut |
| Konventionstreue | 4 | Muster wiederverwendet (`space-remove`-Dialog, `registerPanel`, Tokens); drei CSS-Fehler „die erste Regel ist nicht die gemeinte“ |
| Fehlerbehandlung/Edge Cases | 4 | Phantom-Space, Rate-Limit-Speicher, Index-Sprung — gefunden; der PATCH-Bypass (E1a) und der Doppel-DELETE kamen erst in Claude-Sessions |
| Sicherheitspraxis | 4 | polkit eng statt sudoers, Hard Rule 9 durchgehend (Wegwerf nur per PID-Datei), Tailnet-HTML nicht eingecheckt; keine Sicherheitslücke eingeführt, aber auch keine der beiden gefundenen (E1a) selbst entdeckt |
| Commit-Hygiene | 2 | Ausführer kaum erkennbar, zweimal falsches Datum (41 bzw. 42 Fundstellen), sehr große Misch-Commits |
| Autonome Fehlerkorrektur | 4 | viele eigene Fehler vor dem Commit behoben und benannt; einige erst durch Advisor, Nikinger oder Wächter |

**Was die Tabelle nicht zeigt und P10 wissen sollte:** die **Ausführlichkeit** — Session-Blöcke von 10–17 KB, ein Archiv von 393 KB und vier
Softcap-Krisen in einer Phase. Das ist ein Kostenfaktor für jede spätere Lesesitzung. Und **M3.1 lief langsam** (Item, 10-07) — nicht gemessen.
**Für einen belastbaren Vergleich** bräuchte es den Bake-off aus dem verlinkten Item (Vorregistrierung, N ≥ 5, Wiederholung, blinder Judge).

## 8 Arbeitsweise — was getragen hat und bleibt

- **Messen vor Bauen**, und **auf die Bedingung warten, nicht auf die Uhr**; ein Gegenlauf zählt nur, wenn **die erwartete Station in der
  JSON rot** steht, nicht der Exit-Code.
- **Ein Wächter kennt nur Eigenschaften, die auf seiner Liste stehen** (`padding-block`, `border-box`, `margin-bottom` — dreimal).
- **Struktur, die eine Maschine pflegt, pflegt nur die Maschine:** Ketten per `prepend_updated_chain.sh`, Blöcke per `rotate_*`.
  `rotate_session_block.sh` behält den **unteren** Block.
- **Fabi-Schritte sind Termine, keine Blocker** (Wurzel §Working style).
- **Zustand wird gemessen, ein Bild belegt nur Wirkung;** Sichtprüfung bleibt beim Nikinger.

## 9 Was dieser Handover nicht enthält

Keine Implementierungsdetails, keine Locks im Wortlaut, keine Session-Chronik. Die stehen in Code, Tests, Plan und
`phase9_hardening/SESSIONS_ARCHIVE.md`. Die vollständige P10-Liste steht in `phase10_intake.md`.
