#!/usr/bin/env bash
#
# rotate_session_block.sh — Rotationsregel der Doc-Layers-Konvention ausführen.
#
# Ein Phase-Head trägt genau EINEN "## Session stopped"-Block: den neuesten. Dieses Skript
# verschiebt alle älteren verbatim nach SESSIONS_ARCHIVE.md (newest-first) und lässt den
# neuesten stehen.
#
# Prinzip: nichts wird abgetippt. Blöcke werden per `sed -n 'A,Bp'` ausgeschnitten, die
# Reassemblierung wird mit `cmp` gegen das Original geprüft, jeder Block wird nach dem
# Einfügen erneut byte-identisch gegengelesen — und erst danach wird geschrieben. Bei jeder
# Abweichung bricht das Skript ab, ohne eine Zieldatei angefasst zu haben.
#
# Aufruf:   scripts/rotate_session_block.sh <phase_verzeichnis> [repo_root]
# Beispiel: scripts/rotate_session_block.sh phase2_mcp
#
# Exit: 0 = rotiert · 1 = Abbruch, nichts geändert · 2 = nichts zu tun (bereits konform)

set -euo pipefail

PHASE_DIR="${1:-}"
REPO_ROOT="${2:-.}"

if [[ -z "$PHASE_DIR" ]]; then
  echo "Aufruf: $0 <phase_verzeichnis> [repo_root]   z.B. $0 phase1_storage" >&2
  exit 1
fi

HEAD="${REPO_ROOT}/${PHASE_DIR}/CLAUDE.md"
ARCHIVE="${REPO_ROOT}/${PHASE_DIR}/SESSIONS_ARCHIVE.md"
MARKER='^## Session stopped'

WORK="$(mktemp -d)"
trap 'rm -rf "$WORK"' EXIT

die() { echo "ABBRUCH: $*" >&2; exit 1; }

[[ -f "$HEAD" ]] || die "Phase-Head nicht gefunden: $HEAD"
cp "$HEAD" "$WORK/head.orig"

TOTAL_LINES="$(wc -l < "$HEAD")"

# ---------------------------------------------------------------- Blöcke finden
mapfile -t STARTS < <(grep -n "$MARKER" "$HEAD" | cut -d: -f1)
mapfile -t H2     < <(grep -n '^## '     "$HEAD" | cut -d: -f1)

block_end() {           # letzte Zeile des Blocks, der bei $1 beginnt
  local start="$1" h
  for h in "${H2[@]}"; do
    if (( h > start )); then echo $(( h - 1 )); return; fi
  done
  echo "$TOTAL_LINES"
}

if (( ${#STARTS[@]} == 0 )); then
  echo "HINWEIS: $HEAD trägt keinen '## Session stopped'-Block. Nichts zu rotieren." >&2
  exit 2
fi

if (( ${#STARTS[@]} == 1 )); then
  # Genau der Fall, der die Regel in P1 unterlaufen hat: ein Session-Block, aber danach
  # folgt eine weitere ##-Sektion, die faktisch ein zweiter Session-Block ist.
  last_start="${STARTS[0]}"
  trailing=0
  for h in "${H2[@]}"; do (( h > last_start )) && trailing=$(( trailing + 1 )); done
  if (( trailing > 0 )); then
    echo "WARNUNG: genau ein '## Session stopped'-Block, aber ${trailing} weitere ##-Sektion(en) danach." >&2
    echo "         Prüfen, ob eine davon faktisch ein Session-Block unter abweichender" >&2
    echo "         Überschrift ist. Falls ja: Überschrift auf das Schema bringen und erneut laufen." >&2
    exit 2
  fi
  echo "Bereits konform: genau ein Session-Block im Head. Nichts zu tun."
  exit 2
fi

[[ -f "$ARCHIVE" ]] || die "Archiv fehlt: $ARCHIVE — mit L1-Header-Card anlegen und in docs/INDEX.md eintragen, dann erneut laufen."
cp "$ARCHIVE" "$WORK/archive.orig"

KEEP_INDEX=$(( ${#STARTS[@]} - 1 ))   # der neueste Block bleibt stehen

# ---------------------------------------------------------------- Head zerlegen
# Ergebnis: eine geordnete Stückliste aus KEEP-Segmenten und MOVE-Blöcken.
PIECES=(); KINDS=(); MOVED=()
cursor=1; n=0

for i in "${!STARTS[@]}"; do
  (( i == KEEP_INDEX )) && continue
  s="${STARTS[$i]}"; e="$(block_end "$s")"
  if (( s > cursor )); then
    sed -n "${cursor},$((s - 1))p" "$HEAD" > "$WORK/p${n}"
    PIECES+=("$WORK/p${n}"); KINDS+=("keep"); n=$(( n + 1 ))
  fi
  sed -n "${s},${e}p" "$HEAD" > "$WORK/p${n}"
  PIECES+=("$WORK/p${n}"); KINDS+=("move"); MOVED+=("$WORK/p${n}")
  echo "  Block Zeilen ${s}–${e} → Archiv ($(wc -l < "$WORK/p${n}") Zeilen, $(wc -c < "$WORK/p${n}") Bytes)"
  n=$(( n + 1 )); cursor=$(( e + 1 ))
done

if (( cursor <= TOTAL_LINES )); then
  sed -n "${cursor},\$p" "$HEAD" > "$WORK/p${n}"
  PIECES+=("$WORK/p${n}"); KINDS+=("keep")
fi

# Prüfung 1: Stückliste in Originalreihenfolge == Original, Byte für Byte.
cat "${PIECES[@]}" > "$WORK/reassembled"
cmp -s "$WORK/reassembled" "$WORK/head.orig" \
  || die "Reassemblierung weicht vom Original ab — der Schnitt ist nicht verlustfrei."
echo "OK  Schnitt verlustfrei (${#MOVED[@]} Block(s), Reassemblierung == Original)"

# ---------------------------------------------------------------- neuer Head
KEEP_FILES=()
for i in "${!PIECES[@]}"; do
  [[ "${KINDS[$i]}" == "keep" ]] && KEEP_FILES+=("${PIECES[$i]}")
done
cat "${KEEP_FILES[@]}" > "$WORK/head.new"

grep -c "$MARKER" "$WORK/head.new" | grep -qx 1 \
  || die "Der neue Head trägt nicht genau einen Session-Block — Abbruch."
echo "OK  Neuer Head trägt genau einen Session-Block"

# ---------------------------------------------------------------- neues Archiv
# newest-first: die bewegten Blöcke kommen in umgekehrter Reihenfolge nach oben.
ANCHOR="$(grep -n "$MARKER" "$ARCHIVE" | head -n1 | cut -d: -f1 || true)"
if [[ -n "$ANCHOR" ]]; then
  sed -n "1,$((ANCHOR - 1))p" "$ARCHIVE" > "$WORK/arch_head"
  sed -n "${ANCHOR},\$p"      "$ARCHIVE" > "$WORK/arch_rest"
else
  cp "$ARCHIVE" "$WORK/arch_head"; : > "$WORK/arch_rest"
fi

REVERSED=()
for (( i = ${#MOVED[@]} - 1; i >= 0; i-- )); do REVERSED+=("${MOVED[$i]}"); done
cat "$WORK/arch_head" "${REVERSED[@]}" "$WORK/arch_rest" > "$WORK/archive.new"

# Prüfung 2: jeder bewegte Block liegt im Archiv byte-identisch.
offset="$(wc -l < "$WORK/arch_head")"
for f in "${REVERSED[@]}"; do
  lines="$(wc -l < "$f")"
  sed -n "$((offset + 1)),$((offset + lines))p" "$WORK/archive.new" > "$WORK/readback"
  cmp -s "$WORK/readback" "$f" \
    || die "Ein Block liegt im Archiv nicht byte-identisch — nichts wurde geschrieben."
  offset=$(( offset + lines ))
done
echo "OK  Alle bewegten Blöcke im Archiv byte-identisch"

# Prüfung 3: der Archivbestand ist unangetastet.
cat "$WORK/arch_head" "$WORK/arch_rest" > "$WORK/archive.without"
cmp -s "$WORK/archive.without" "$WORK/archive.orig" \
  || die "Das bestehende Archiv wurde beim Zerlegen verändert."
echo "OK  Archivbestand unverändert"

# ---------------------------------------------------------------- schreiben
cp "$WORK/head.orig"    "${HEAD}.bak"
cp "$WORK/archive.orig" "${ARCHIVE}.bak"
cp "$WORK/head.new"     "$HEAD"
cp "$WORK/archive.new"  "$ARCHIVE"

echo "OK  Head:   $(wc -c < "$WORK/head.orig") B → $(wc -c < "$HEAD") B"
echo "OK  Archiv: $(wc -c < "$WORK/archive.orig") B → $(wc -c < "$ARCHIVE") B"
echo "    Backups: ${HEAD}.bak · ${ARCHIVE}.bak  (nach Sichtprüfung löschen)"
cat <<'HINT'

Danach von Hand (Änderungen, keine Moves — deshalb nicht im Skript):
  1. SESSIONS_ARCHIVE.md: Frontmatter `updated:` auf das heutige Datum.
  2. docs/INDEX.md: Größenangaben für Head und Archiv nachziehen.
  3. Nahtstellen sichten: je eine Leerzeile vor jeder `##`-Überschrift, keine doppelte.
HINT
