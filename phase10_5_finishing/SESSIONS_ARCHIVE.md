---
status: archive
purpose: L3-Archiv der älteren Session-Blöcke des Phase-10.5-Heads — verbatim, newest-first
read-when: beim Audit, wenn der Stand eines früheren Blocks dieser Phase gebraucht wird
detail: L3
up: ./CLAUDE.md
down:
updated: 2026-10-22 (angelegt — P10.5 Block 0, Schritt 0.2; noch kein Block rotiert, der erste steht im Head)
---
# Phase 10.5 — Session-Archiv

Hier stehen die älteren `## Session stopped`-Blöcke des Phase-10.5-Heads, **verbatim** und
newest-first — der neueste Block steht im Head (`../CLAUDE.md`), dieser Abschnitt trägt die Chronik.

**Warum es ein Archiv gibt:** die Doc-Layers-Konvention verlangt genau **einen** Session-Block pro
Phase-Head (Rotationsregel ab Tag 1, `scripts/rotate_session_block.sh`). Wer einen älteren Block
sucht, findet ihn hier — nicht im Head.

**Größe:** jeder Block ist auf **4 KiB** begrenzt (Lock P10.5-T, DO-3), geprüft von
`phase10_5_finishing/tests/test_head_rules.py`. Das ist die Lehre aus Phase 9: die alten Blöcke
trugen 10–17 KB, das P9-Archiv wuchs auf 396 KB — der teuerste Abschnitt einer Datei, den jede
Lesesitzung zuerst liest.
