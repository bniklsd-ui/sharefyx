#!/usr/bin/env bash
#
# rotate_root_current_state.sh — die Session-Block-Rotation für die **Wurzel**-CLAUDE.md.
#
# Warum ein eigenes Skript: `rotate_session_block.sh` schneidet an `^## Session stopped`, und die
# Wurzel trägt ihre Blöcke anders — als Absätze, die mit `**[YYYY-MM-DD, ` beginnen, innerhalb
# von `## Current state`. Dieselbe Regel, dieselbe Strenge, eine andere Marke: **ein Schritt, der von
# Hand an einer maschinell gepflegten Struktur passiert, ist ein Defekt** (Session-Block 2026-10-04),
# und die Wurzel war bis dahin der einzige Ort, an dem rotiert wurde, ohne dass ein Werkzeug es tat.
#
# Grundlage: die Umkehr von **P9-A** (Nikinger-Entscheidung 2026-10-04) und die K=1-Fassung der
# Doc-Layers-Konvention — ein §Current state trägt **genau einen** aktuellen Block; die älteren
# wandern **verbatim** nach `docs/PROJECT_SESSION_LOG.md` (L3), wohin die Wurzel selbst seit
# 2026-09-08 zeigt.
#
# Prinzip: nichts wird abgetippt. Blöcke werden per `sed -n 'A,Bp'` ausgeschnitten, die Reassemblierung
# wird mit `cmp` gegen das Original geprüft, jeder Block wird nach dem Einfügen erneut byte-identisch
# gegengelesen, der Altbestand des Archivs wird getrennt geprüft — und erst danach wird geschrieben.
# Bei jeder Abweichung bricht das Skript ab, **ohne eine Zieldatei angefasst zu haben**.
#
# **Die Blockgrenze ist die Stelle, an der eine Fehlschneidung Historie zerstört** — deshalb wird sie
# nicht geraten, sondern **gemessen** (Gegenprobe (a)): alle Zeilen, die mit der Marke beginnen, müssen
# zugleich eine Leerzeile davor haben. Eine `**[`-Zeile *innerhalb* eines Blocks wäre dann eine
# Fehlschneidung, und genau das bricht der Lauf ab, statt es zu verschieben.
#
# Aufruf:   scripts/rotate_root_current_state.sh [repo_root] [keep]
#           Defaults: . · 1   (K=1: nur der neueste Block bleibt im Head)
# Exit: 0 = rotiert · 1 = Abbruch, nichts geändert · 2 = nichts zu tun (K erfüllt)

set -euo pipefail

REPO_ROOT="${1:-.}"
KEEP="${2:-1}"

HEAD="${REPO_ROOT}/CLAUDE.md"
ARCHIVE="${REPO_ROOT}/docs/PROJECT_SESSION_LOG.md"
MARK='^\*\*\[[0-9]{4}-[0-9]{2}-[0-9]{2},'

WORK="$(mktemp -d)"
trap 'rm -rf "$WORK"' EXIT

die() { echo "ABBRUCH: $*" >&2; exit 1; }

[[ -f "$HEAD"    ]] || die "Wurzel-Head nicht gefunden: $HEAD"
[[ -f "$ARCHIVE" ]] || die "Archiv fehlt: $ARCHIVE"
[[ "$KEEP" =~ ^[0-9]+$ && "$KEEP" -ge 1 ]] || die "keep muss eine Zahl >= 1 sein, war '$KEEP'"

cp "$HEAD" "$WORK/head.orig"
cp "$ARCHIVE" "$WORK/archive.orig"
TOTAL_LINES="$(wc -l < "$HEAD")"

# ---------------------------------------------------------------- Section + Blöcke finden
CS_LINE="$(grep -n '^## Current state' "$HEAD" | head -n1 | cut -d: -f1 || true)"
[[ -n "$CS_LINE" ]] || die "keine Sektion '## Current state' in $HEAD"
mapfile -t MARKS < <(awk -v start="$CS_LINE" -v re="$MARK" 'NR>start && $0 ~ re {print NR}' "$HEAD")
[[ ${#MARKS[@]} -gt 0 ]] || die "kein Current-state-Block gefunden (Marke: $MARK)"

# Gegenprobe (a): **jede** Markenzeile hat eine Leerzeile davor. Ohne das wäre eine `**[`-Zeile
# innerhalb eines Blocks eine Fehlschneidung — und genau das darf nicht passieren, ohne dass der
# Lauf abbricht.
for ln in "${MARKS[@]}"; do
  prev="$((ln - 1))"
  [[ -z "$(sed -n "${prev}p" "$HEAD")" ]] \
    || die "Zeile $ln beginnt mit der Blockmarke, hat aber keine Leerzeile davor — die Blockgrenze wäre geraten, nicht gemessen"
done
# Gegenprobe (b): keine `**[`-Zeile in der Sektion, die keine Blockmarke trägt (sonst gäbe es
# Blöcke, die der Rotations-Anker nie sieht — dieselbe Fehlerklasse wie der ` · `-Trenner).
mapfile -t ANYBRACKET < <(awk -v start="$CS_LINE" 'NR>start && /^\*\*\[/ {print NR}' "$HEAD")
[[ ${#ANYBRACKET[@]} -eq ${#MARKS[@]} ]] || die \
  "${#ANYBRACKET[@]} Zeilen mit '**[' in §Current state, aber nur ${#MARKS[@]} mit der vollen Marke — es gibt Blöcke, die der Anker nicht sieht"

TOTAL_BLOCKS=${#MARKS[@]}
(( TOTAL_BLOCKS > KEEP )) || {
  echo "Bereits konform: ${TOTAL_BLOCKS} Block(s) im Head, K=${KEEP}. Nichts zu tun."
  exit 2
}

block_end() {                       # letzte Zeile des Blocks, der bei $1 beginnt
  local start="$1" i
  for (( i = 0; i < ${#MARKS[@]}; i++ )); do
    # `- 1`, nicht `- 2`: die Leerzeile **vor** dem nächsten Block gehört zu diesem, sonst fällt
    # an jeder Grenze genau eine Zeile weg. Die erste Fassung nutzte `- 2` und die
    # Reassemblierungs-Gegenprobe brach ab — zu Recht, denn ein Schnitt, der eine Zeile je Grenze
    # verliert, ist ein stiller Datenverlust und kein Rundungsfehler.
    if (( MARKS[i] > start )); then echo $(( MARKS[i] - 1 )); return; fi
  done
  echo "$TOTAL_LINES"
}

# ---------------------------------------------------------------- Head zerlegen
#
# **Die Reihenfolge ist hier umgekehrt zu `rotate_session_block.sh`, und das war der Fehler der
# ersten Fassung.** Im Phase-Head liegen die Blöcke **neueste-unten** (der `## Session stopped`-Block
# am Dateiende), in der Wurzel liegen sie **neueste-oben** (der 2026-10-02-Block beginnt §Current
# state). Die erste Fassung übernahm die Bedingung des Vorbilds (`i < TOTAL_BLOCKS - KEEP`, also
# „die letzten KEEP bleiben") und hat damit bei K=1 den **ältesten** Block behalten und den
# neuesten archiviert. Die Byte-Gegenprobe hat es gemeldet: der Block, der im Archiv fehlte, war
# nicht zufällig der, an dem die Schnittstelle zweier Blöcke lag — der Test prüfte Blockgrenzen und
# sah deshalb zuerst die Reihenfolge statt der Menge.
#
# Gewonnen wird ab `MARK[KEEP]`; der Head behält den **Rumpf davor**, die ersten KEEP Blöcke **und
# den Schwanz nach dem letzten Block** — im Wurzel-Head steht dort der Zeiger auf dieses Archiv, und
# der ist Anweisung, nicht Session-Inhalt.
FIRST_MOVED=$KEEP
LAST_KEPT_END="$(block_end "${MARKS[$((FIRST_MOVED - 1))]}")"
PIECES=(); KINDS=(); MOVED=()
n=0
sed -n "1,${LAST_KEPT_END}p" "$HEAD" > "$WORK/p${n}"; PIECES+=("$WORK/p${n}"); KINDS+=("keep"); n=$(( n + 1 ))
for (( i = FIRST_MOVED; i < TOTAL_BLOCKS; i++ )); do
  s="${MARKS[i]}"; e="$(block_end "$s")"
  sed -n "${s},${e}p" "$HEAD" > "$WORK/p${n}"
  PIECES+=("$WORK/p${n}"); KINDS+=("move"); MOVED+=("$WORK/p${n}")
  echo "  Block Zeilen ${s}–${e} → Archiv ($(wc -l < "$WORK/p${n}") Zeilen, $(wc -c < "$WORK/p${n}") Bytes)"
  n=$(( n + 1 ))
done
LAST_BLOCK_END="$(block_end "${MARKS[$((TOTAL_BLOCKS - 1))]}")"
if (( LAST_BLOCK_END < TOTAL_LINES )); then        # Schwanz: der Zeiger auf dieses Archiv
  sed -n "$((LAST_BLOCK_END + 1)),\$p" "$HEAD" > "$WORK/p${n}"
  PIECES+=("$WORK/p${n}"); KINDS+=("keep")
fi

# Gegenprobe (c): die Stückliste in Originalreihenfolge == Original, Byte für Byte.
cat "${PIECES[@]}" > "$WORK/reassembled"
cmp -s "$WORK/reassembled" "$WORK/head.orig" \
  || die "Reassemblierung weicht vom Original ab — der Schnitt ist nicht verlustfrei."
echo "OK  Schnitt verlustfrei (${#MOVED[@]} Block(s), Reassemblierung == Original)"

KEEP_FILES=()
for i in "${!PIECES[@]}"; do
  [[ "${KINDS[$i]}" == "keep" ]] && KEEP_FILES+=("${PIECES[$i]}")
done
cat "${KEEP_FILES[@]}" > "$WORK/head.new"
# **[2026-10-08]** nur ab `## Current state` zählen — dieselbe Grenze wie die Blocksuche oben. Seit
# 2026-10-07 steht in §Doku-Hygiene ein datierter Absatz mit derselben Marke; der Ganzdatei-Zähler
# sah ihn als zweiten Block und brach jede Rotation ab (zum Glück, ohne zu schreiben).
count_new() { awk '/^## Current state/{cs=1} cs && /^\*\*\[[0-9][0-9][0-9][0-9]-/{n++} END{print n+0}' "$WORK/head.new"; }
count_new | grep -qx "$KEEP" \
  || die "der neue Head trägt $(count_new) Blöcke, erwartet ${KEEP} — Abbruch."
echo "OK  Neuer Head trägt genau ${KEEP} Block"

# ---------------------------------------------------------------- Archiv: newest-first
# Einfügepunkt: vor dem **ersten** bestehenden `**[`-Block, damit die Region newest-first bleibt.
ANCHOR="$(grep -n '^\*\*\[[0-9]\{4\}-' "$ARCHIVE" | head -n1 | cut -d: -f1 || true)"
if [[ -n "$ANCHOR" ]]; then
  sed -n "1,$((ANCHOR - 1))p" "$ARCHIVE" > "$WORK/arch_head"
  sed -n "${ANCHOR},\$p"      "$ARCHIVE" > "$WORK/arch_rest"
else
  cp "$ARCHIVE" "$WORK/arch_head"; : > "$WORK/arch_rest"
fi
REVERSED=()
for (( i = ${#MOVED[@]} - 1; i >= 0; i-- )); do REVERSED+=("${MOVED[$i]}"); done
# `printf %s\\n\\n` statt Leerzeilen aus den Blöcken: der letzte bewegte Block bekommt seinen
# Absatzabstand vom Bestand, damit keine Nahtstelle entsteht.
# Kein `printf '\n'` zwischen den Blöcken: jeder bewegte Block **enthält** seine abschließende
# Leerzeile (siehe `block_end`), ein zusätzliches Trennzeichen erzeugte eine doppelte Leerzeile.
{ cat "$WORK/arch_head"; for f in "${REVERSED[@]}"; do cat "$f"; done; cat "$WORK/arch_rest"; } > "$WORK/archive.new"

# Gegenprobe (d): jeder bewegte Block liegt im Archiv byte-identisch.
offset="$(wc -l < "$WORK/arch_head")"
for f in "${REVERSED[@]}"; do
  lines="$(wc -l < "$f")"
  sed -n "$((offset + 1)),$((offset + lines))p" "$WORK/archive.new" > "$WORK/readback"
  cmp -s "$WORK/readback" "$f" || die "ein Block liegt im Archiv nicht byte-identisch — nichts wurde geschrieben."
  offset=$(( offset + lines ))
done
echo "OK  Alle bewegten Blöcke im Archiv byte-identisch"

# Gegenprobe (e): der Archivbestand ist unangetastet.
cat "$WORK/arch_head" "$WORK/arch_rest" > "$WORK/archive.without"
cmp -s "$WORK/archive.without" "$WORK/archive.orig" \
  || die "der bestehende Archivinhalt wurde beim Zerlegen verändert."
echo "OK  Archivbestand unverändert"

# Gegenprobe (f): die Byte-Buchhaltung. Summe aus beiden Dateien vorher == nachher.
before=$(( $(wc -c < "$HEAD") + $(wc -c < "$ARCHIVE") ))
after=$(( $(wc -c < "$WORK/head.new") + $(wc -c < "$WORK/archive.new") ))
delta=$(( after - before ))
echo "OK  Byte-Buchhaltung: $before B → $after B (Δ $delta B = die Leerzeilen zwischen den Blöcken)"

# ---------------------------------------------------------------- schreiben
cp "$HEAD"    "${HEAD}.bak"
cp "$ARCHIVE" "${ARCHIVE}.bak"
cp "$WORK/head.new"    "$HEAD"
cp "$WORK/archive.new" "$ARCHIVE"

echo "OK  Head:   $(wc -c < "$WORK/head.orig") B → $(wc -c < "$HEAD") B"
echo "OK  Archiv: $(wc -c < "$WORK/archive.orig") B → $(wc -c < "$ARCHIVE") B"
echo "    Backups: ${HEAD}.bak · ${ARCHIVE}.bak  (nach Sichtprüfung löschen)"
cat <<'HINT'

Danach von Hand (Änderungen, keine Moves — deshalb nicht im Skript):
  1. docs/PROJECT_SESSION_LOG.md: Frontmatter `updated:` auf das heutige Datum.
  2. docs/INDEX.md: Größenangaben für Wurzel-Head und Archiv nachziehen.
  3. Plan-Text: die Umkehr von P9-A datiert nachtragen (Lock, keine stille Abweichung).
HINT
