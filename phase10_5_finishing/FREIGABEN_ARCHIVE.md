---
status: archive
purpose: L3-Archiv der Freigaben der Phase 10.5 — wer hat wann was freigegeben (Locks P10.5-A–W, Register-Tor, Eingriff in phase4_auth, Kontextgrenze, „alles Messbare an der Wegwerf-Instanz"). Verbatim aus dem Phase-Head verschoben, weil der Head über dem Softcap stand.
read-when: wenn eine Entscheidung der Phase 10.5 zurückgeführt werden soll — die Locks selbst stehen wortgleich im 📕-Plan (`docs/concepts/phase10_5_finishing_plan.md`), hier steht, **wer sie wann** gegeben hat
detail: L3
up: ../ROADMAP.md
down:
  - CLAUDE.md                                          # der Phase-Head, aus dem der Abschnitt verschoben wurde
  - ../docs/concepts/phase10_5_finishing_plan.md       # 📕 der Plan: Locks P10.5-A–W, Blöcke 0–12/Z, Abnahme
updated: 2026-10-24 (aus dem Phase-Head verschoben: der Head stand bei 41.343 B und damit über dem Softcap)
---
# Freigaben-Archiv — Phase 10.5

> **Warum dieses Archiv existiert (2026-10-24).** Der Phase-Head stand beim Bau von Block 10.5
> auf **41.343 B** — über dem Softcap (40.960 B), damit `doc_health` rot und das Deploy-Gate zu.
> Der Abschnitt „Freigaben" ist ein **Snapshot vom 21./22.10.2026**: die dort freigegebenen Locks
> stehen wortgleich im 📕-Plan, und die Tabelle wird sich nicht mehr ändern (eine neue Freigabe
> käme als neue Zeile **in den Head**, nicht in dieses Archiv). Er ist hierher gewandert,
> **verbatim** (`scripts/move_sections.py`).

## Freigaben

| Was | Wann | Wer |
|---|---|---|
| Plan `docs/concepts/phase10_5_finishing_plan.md` (Locks P10.5-A–W) | 2026-10-21 | Nikinger |
| Register-Tor **P10-8** — die Spalte „Ziel" wird verbindlich, abgehakt wird im Register | 2026-10-21 | Nikinger |
| **P10-C** — Eingriff in `phase4_auth/` (Lock **P10.5-O**): Loopback-Redirect mit Port, `application_type`, CSP `form-action` | 2026-10-21 | Nikinger |
| **P10.5-N** — P10-I in **beiden** Richtungen: kein Item wandert *in* einen fremden Home-Space hinein **und** nicht *aus* einem heraus | 2026-10-21 | Nikinger |
| Kontextgrenze **400.000** für `MiniMax-M3` und `MiniMax-M3.1-Flash` (P10.5-C, gesetzt von eurofyx-fleet, Neustart 22.10.) | 2026-10-22 | eurofyx-fleet |
| **Alles Messbare an der Wegwerf-Instanz** — Tests gegen die Live-Umgebung (echter `DATA_ROOT`, echte `auth.sqlite3`, Keyring, laufender Dienst, Funnel/Domain) nur, wenn der Server das nicht selbst entscheiden kann; die Entscheidung trifft der Nikinger (Wurzel-`CLAUDE.md` §Working style) | 2026-10-22 | Nikinger |

## Freigaben

| Was | Wann | Wer |
|---|---|---|
| Plan `docs/concepts/phase10_5_finishing_plan.md` (Locks P10.5-A–W) | 2026-10-21 | Nikinger |
| Register-Tor **P10-8** — die Spalte „Ziel" wird verbindlich, abgehakt wird im Register | 2026-10-21 | Nikinger |
| **P10-C** — Eingriff in `phase4_auth/` (Lock **P10.5-O**): Loopback-Redirect mit Port, `application_type`, CSP `form-action` | 2026-10-21 | Nikinger |
| **P10.5-N** — P10-I in **beiden** Richtungen: kein Item wandert *in* einen fremden Home-Space hinein **und** nicht *aus* einem heraus | 2026-10-21 | Nikinger |
| Kontextgrenze **400.000** für `MiniMax-M3` und `MiniMax-M3.1-Flash` (P10.5-C, gesetzt von eurofyx-fleet, Neustart 22.10.) | 2026-10-22 | eurofyx-fleet |
| **Alles Messbare an der Wegwerf-Instanz** — Tests gegen die Live-Umgebung (echter `DATA_ROOT`, echte `auth.sqlite3`, Keyring, laufender Dienst, Funnel/Domain) nur, wenn der Server das nicht selbst entscheiden kann; die Entscheidung trifft der Nikinger (Wurzel-`CLAUDE.md` §Working style) | 2026-10-22 | Nikinger |
