#!/usr/bin/env bash
#
# rotate_index_updates.sh — Rotationsregel für die `updated:`-Kette von docs/INDEX.md.
#
# Vorbild ist rotate_session_block.sh: nichts wird abgetippt. Der Unterschied ist keine neue
# Mechanik, sondern eine andere Schnittstelle — rotate_session_block.sh schneidet an
# Zeilenanfängen (`^## Session stopped`), die `updated:`-Kette ist dagegen EINE physische Zeile
# mit ` | `-getrennten Einträgen. Getrennt wird nur an ` | `, dem ein ISO-Datum folgt
# (`\d{4}-\d{2}-\d{2}`) — ein ` | ` innerhalb eines Eintrags (z. B. in einer Markdown-Tabelle im
# Eintragstext) darf den Schnitt nicht verfälschen.
#
# Erhalten bleibt genau der jüngste Eintrag plus ein Zeiger auf das Archiv. Vier Gegenproben vor
# dem Schreiben: (a) Byte-Buchhaltung, (b) `cmp` der Reassemblierung, (c) jeder rotierte Eintrag
# byte-identisch im Archiv wiedergefunden, (d) der Frontmatter-Closer `---` steht danach auf
# einer eigenen Zeile. Bei jeder Abweichung bricht das Skript ab, ohne eine Zieldatei
# angefasst zu haben.
#
# Aufruf:   scripts/rotate_index_updates.sh [repo_root]
# Exit: 0 = rotiert · 1 = Abbruch, nichts geändert · 2 = nichts zu tun (bereits ein Eintrag)

set -euo pipefail

REPO_ROOT="${1:-.}"
INDEX="${REPO_ROOT}/docs/INDEX.md"
ARCHIVE="${REPO_ROOT}/docs/INDEX_UPDATES_ARCHIVE.md"

WORK="$(mktemp -d)"
trap 'rm -rf "$WORK"' EXIT

die() { echo "ABBRUCH: $*" >&2; exit 1; }

[[ -f "$INDEX" ]] || die "Index nicht gefunden: $INDEX"
[[ -f "$ARCHIVE" ]] || die "Archiv fehlt: $ARCHIVE — mit L1-Header-Card anlegen, dann erneut laufen."

cp "$INDEX" "$WORK/index.orig"
cp "$ARCHIVE" "$WORK/archive.orig"

# ---------------------------------------------------------------- Frontmatter finden
mapfile -t CLOSERS < <(grep -n '^---$' "$INDEX" | cut -d: -f1)
(( ${#CLOSERS[@]} >= 2 )) || die "Frontmatter nicht erkennbar (weniger als zwei '---'-Zeilen)."
FM_START="${CLOSERS[0]}"
FM_END="${CLOSERS[1]}"

UPDATED_LINE_NO="$(sed -n "${FM_START},${FM_END}p" "$INDEX" | grep -n '^updated: ' | head -n1 | cut -d: -f1)"
[[ -n "$UPDATED_LINE_NO" ]] || die "Keine 'updated:'-Zeile in der Frontmatter gefunden."
UPDATED_LINE_NO=$(( FM_START + UPDATED_LINE_NO - 1 ))

UPDATED_LINE="$(sed -n "${UPDATED_LINE_NO}p" "$INDEX")"
PREFIX="updated: "
BODY="${UPDATED_LINE#"$PREFIX"}"

# ---------------------------------------------------------------- Kette splitten
# Split nur an ' | ' gefolgt von einem ISO-Datum — kein Split an einem ' | ' im Eintragstext.
mapfile -t ENTRIES < <(python3 - "$BODY" <<'PYEOF'
import re, sys
body = sys.argv[1]
parts = re.split(r' \| (?=\d{4}-\d{2}-\d{2})', body)
for p in parts:
    print(p)
PYEOF
)

if (( ${#ENTRIES[@]} <= 1 )); then
  echo "Bereits konform: die 'updated:'-Kette hat nur einen Eintrag. Nichts zu tun."
  exit 2
fi

KEEP="${ENTRIES[0]}"
ROTATED=("${ENTRIES[@]:1}")

# Gegenprobe (a): Byte-Buchhaltung — Summe der Teile + Trenner == Originalzeile.
SEP=" | "
RECOMPOSED="$KEEP"
for e in "${ROTATED[@]}"; do RECOMPOSED+="${SEP}${e}"; done
[[ "$RECOMPOSED" == "$BODY" ]] || die "Byte-Buchhaltung schlägt fehl — Split ist nicht verlustfrei."
echo "OK  Byte-Buchhaltung: ${#ROTATED[@]} rotierte(r) Eintrag/Einträge, Split verlustfrei"

# ---------------------------------------------------------------- neue Zeile bauen
NEW_LINE="${PREFIX}${KEEP} | ältere Einträge: docs/INDEX_UPDATES_ARCHIVE.md"

# ---------------------------------------------------------------- neuen Index bauen
TOTAL_LINES="$(wc -l < "$INDEX")"
sed -n "1,$((UPDATED_LINE_NO - 1))p" "$INDEX" > "$WORK/index.new"
printf '%s\n' "$NEW_LINE" >> "$WORK/index.new"
if (( UPDATED_LINE_NO < TOTAL_LINES )); then
  sed -n "$((UPDATED_LINE_NO + 1)),\$p" "$INDEX" >> "$WORK/index.new"
fi

# Gegenprobe (d): der Frontmatter-Closer '---' steht auf einer eigenen Zeile danach.
sed -n "$((FM_END + 1))p" "$WORK/index.new" | grep -qx -- '---' \
  || { CLOSER_LINE_NO_NEW="$(grep -n '^---$' "$WORK/index.new" | sed -n '2p' | cut -d: -f1)"; \
       [[ -n "$CLOSER_LINE_NO_NEW" ]] || die "Frontmatter-Closer nach dem Schreiben nicht mehr auf eigener Zeile."; }
echo "OK  Frontmatter-Closer bleibt auf eigener Zeile"

# ---------------------------------------------------------------- Archiv bauen (newest-first)
ANCHOR="$(grep -n '^---$' "$ARCHIVE" | sed -n '2p' | cut -d: -f1 || true)"
if [[ -n "$ANCHOR" ]]; then
  sed -n "1,${ANCHOR}p" "$ARCHIVE" > "$WORK/arch_head"
  TOTAL_ARCH="$(wc -l < "$ARCHIVE")"
  if (( ANCHOR < TOTAL_ARCH )); then
    sed -n "$((ANCHOR + 1)),\$p" "$ARCHIVE" > "$WORK/arch_rest"
  else
    : > "$WORK/arch_rest"
  fi
else
  cp "$ARCHIVE" "$WORK/arch_head"; : > "$WORK/arch_rest"
fi

{
  cat "$WORK/arch_head"
  for e in "${ROTATED[@]}"; do printf '%s\n' "- $e"; done
  cat "$WORK/arch_rest"
} > "$WORK/archive.new"

# Gegenprobe (c): jeder rotierte Eintrag byte-identisch im Archiv wiedergefunden.
for e in "${ROTATED[@]}"; do
  grep -qxF -- "- $e" "$WORK/archive.new" \
    || die "Ein rotierter Eintrag liegt im Archiv nicht byte-identisch: $e"
done
echo "OK  Alle rotierten Einträge im Archiv byte-identisch"

# Gegenprobe (b): die ursprüngliche 'updated:'-Zeile zurück in index.new eingesetzt muss
# byte-identisch das Original ergeben — prüft die ganze Datei, nicht nur die eine Zeile, die
# das Skript selbst gebaut hat (ein reiner grep-gegen-dieselbe-Variable-Vergleich wäre eine
# Tautologie und hätte den Doppel-Body-Bug aus der ersten Testrunde nicht gefangen).
{
  sed -n "1,$((UPDATED_LINE_NO - 1))p" "$WORK/index.new"
  printf '%s\n' "$UPDATED_LINE"
  NEW_TOTAL="$(wc -l < "$WORK/index.new")"
  if (( UPDATED_LINE_NO < NEW_TOTAL )); then
    sed -n "$((UPDATED_LINE_NO + 1)),\$p" "$WORK/index.new"
  fi
} > "$WORK/index.roundtrip"
cmp -s "$WORK/index.roundtrip" "$WORK/index.orig" \
  || die "Nur die 'updated:'-Zeile darf sich ändern — der Rest der Datei weicht vom Original ab."
echo "OK  Roundtrip: nur die 'updated:'-Zeile weicht vom Original ab, sonst nichts"

# ---------------------------------------------------------------- schreiben
cp "$WORK/index.orig"   "${INDEX}.bak"
cp "$WORK/archive.orig" "${ARCHIVE}.bak"
cp "$WORK/index.new"    "$INDEX"
cp "$WORK/archive.new"  "$ARCHIVE"

echo "OK  Index:  $(wc -c < "$WORK/index.orig") B → $(wc -c < "$INDEX") B"
echo "OK  Archiv: $(wc -c < "$WORK/archive.orig") B → $(wc -c < "$ARCHIVE") B"
echo "    Backups: ${INDEX}.bak · ${ARCHIVE}.bak  (nach Sichtprüfung löschen)"
