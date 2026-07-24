---
status: live
purpose: Harness-neutraler Einstiegspunkt für Nicht-Claude-Code-Agenten — verweist auf CLAUDE.md und die Doc-Layers-Navigation
read-when: Session-Start in einem Harness, das AGENTS.md statt CLAUDE.md lädt (OpenCode, Aider, …)
detail: L2
up: CLAUDE.md
updated: 2026-07-24
---
# AGENTS.md

Dieses Repository nutzt `CLAUDE.md` als projektweite Instruktionsdatei. Der Inhalt ist
harness-neutral — nichts darin ist an Claude Code gebunden.

**Lies zuerst, in dieser Reihenfolge:**

1. [`CLAUDE.md`](./CLAUDE.md) — Bauprinzip, harte Regeln, Arbeitsweise, aktueller Stand.
2. [`docs/INDEX.md`](./docs/INDEX.md) — L0-Karte aller Dokumente. Navigation startet hier.
3. Den Head der aktiven Phase (steht unter „Current state" in `CLAUDE.md`) plus dessen
   neuesten `## Session stopped`-Block.

**Navigationsprinzip:** Jedes lebende Dokument trägt oben eine YAML-Header-Card von höchstens
15 Zeilen mit `purpose`, `read-when`, `up` und `down`. Lies erst die Card (Datei mit Zeilenlimit
15 öffnen) und entscheide daraus, ob sich der Body lohnt. Nie eine ganze Datei lesen, um
festzustellen, dass man sie nicht gebraucht hätte.

**Die wichtigste Regel, falls du nur eine mitnimmst:** Quelle der Wahrheit ist der getestete
Code, nicht das Dokument. Bei Widerspruch gewinnt das Artefakt — und das Dokument wird im selben
Zug mit datierter Korrekturnotiz gefixt, nicht später.
