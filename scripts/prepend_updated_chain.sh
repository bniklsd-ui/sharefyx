#!/usr/bin/env bash
#
# prepend_updated_chain.sh — einen Faden an den ANFANG der `updated:`-Kette eines lebenden
# .md-Heads stellen, ohne die Datei von Hand anzufassen.
#
# Warum es dieses Skript gibt (2026-10-03, Phase 9, Gate/Z): der Faden-Voranstellen ist der letzte
# Handgriff im Rotations-Workflow, und er ist **fünfmal an einem Tag** mit demselben Fehler
# gescheitert — beim Kopieren der alten Zeile als Vorlage wanderte das `updated: `-Praefix mit in den
# neuen Faden, und ` | ` wurde zu ` · ` oder umgekehrt. Beide Formen sind für
# `scripts/rotate_index_updates.sh` unsichtbar: dessen Anker ist `' | '` + ISO-Datum, ein Faden, der
# mit `updated: ` beginnt oder hinter ` · ` steckt, bleibt beim Rotieren stehen (Gegenprobe (e)
# bricht dafür inzwischen ab, `tests/test_updated_chain.py` prüft es repo-weit).
#
# Die Diagnose war also nicht "aufpassen", sondern: **die Kette ist maschinell gepflegt, und die
# Hand ist das falsche Werkzeug** — dieselbe Aussage, die in `phase9_hardening/CLAUDE.md` im
# Session-Block steht.
#
# Aufruf:
#   scripts/prepend_updated_chain.sh <ziel.md> <faden-datei>
#
# Die Faden-Datei enthält **genau eine Zeile** und **ohne** `updated: `-Präfix. Das Skript verweigert
# jede andere Form, statt sie stillschweigend zu reparieren — ein Werkzeug, das den Fehler
# mitnimmt, ist die Fehlerklasse, die es verhindern soll.
#
# Gegenproben vor dem Schreiben:
#   (a) Form: der Faden beginnt mit `YYYY-MM-DD (`, enthält weder ` | updated: ` noch ` · ` vor
#       einem Datum (beides würde eigene Fäden im Faden erzeugen, die der Anker nicht sieht),
#   (b) Byte-Buchhaltung: neuer Körper == Faden + " | " + alter Körper,
#   (c) Werkzeugvertrag: in der neuen Zeile beginnt **jeder** Faden mit ` | ` (das ist genau die
#       Regel aus `tests/test_updated_chain.py`, hier am echten Ergebnis geprüft),
#   (d) Roundtrip: die alte Zeile zurück eingesetzt ergibt das Original byteweise,
#   (e) genau **eine** `updated: `-Zeile in der Frontmatter — die Feldform bleibt die des Skripts
#       `rotate_index_updates.sh`, das sucht mit `grep -n '^updated: '`.

set -euo pipefail

die() { echo "ABBRUCH: $*" >&2; exit 1; }

[[ $# -eq 2 ]] || die "Aufruf: $0 <ziel.md> <faden-datei>"
TARGET="$1"
THREAD_FILE="$2"
[[ -f "$TARGET" ]]    || die "Zieldatei nicht gefunden: $TARGET"
[[ -f "$THREAD_FILE" ]] || die "Faden-Datei nicht gefunden: $THREAD_FILE"

WORK="$(mktemp -d)"; trap 'rm -rf "$WORK"' EXIT
cp "$TARGET" "$WORK/orig"

# ---------------------------------------------------------------- Faden lesen und prüfen
FADEN_RAW="$(cat "$THREAD_FILE")"
FADEN_LINES="$(grep -c '' "$THREAD_FILE" || true)"
[[ "$FADEN_LINES" -eq 1 ]] || die "die Faden-Datei muss genau eine Zeile haben, hat $FADEN_LINES"
FADEN="${FADEN_RAW%$'\r'}"
case "$FADEN" in
  "updated: "*)
    die "der Faden beginnt mit 'updated: ' — das Praefix gehoert an die ZEILE, nicht an den Faden (genau der Fehler, den dieses Skript verhindert; Absatz 'Warum es dieses Skript gibt')" ;;
esac
[[ "$FADEN" =~ ^[0-9]{4}-[0-9]{2}-[0-9]{2}\ +\( ]] \
  || die "der Faden muss mit 'JJJJ-MM-TT (' beginnen, damit der Split-Anker ihn als Faden erkennt: '${FADEN:0:40}'"
if printf '%s' "$FADEN" | grep -q ' | updated: [0-9]'; then
  die "der Faden enthaelt ' | updated: ' vor einem Datum — das waere ein eigener, unsichtbarer Faden"
fi
if printf '%s' "$FADEN" | grep -qE ' · [0-9]{4}-[0-9]{2}-[0-9]{2}'; then
  die "der Faden enthaelt ' · ' vor einem Datum — dieser Trenner ist fuer rotate_index_updates.sh blind, nimm ' | '"
fi
echo "OK  Form des Fadens (kein Praefix, kein blinder Trenner)"

# ---------------------------------------------------------------- Frontmatter und Kette finden
mapfile -t CLOSERS < <(grep -n '^---$' "$TARGET" | cut -d: -f1)
(( ${#CLOSERS[@]} >= 2 )) || die "Frontmatter nicht erkennbar (weniger als zwei '---'-Zeilen)"
FM_START="${CLOSERS[0]}"; FM_END="${CLOSERS[1]}"

# `|| true` ist Pflicht, nicht Kosmetik: ohne Treffer liefert `grep` 1, `pipefail` macht daraus
# einen Skriptabbruch, und `set -e` beendet das Skript **stumm** — der Aufrufer saehe exit 1
# ohne Zeile und muesste raten. (Dieselbe Falle steht in `rotate_index_updates.sh` und ist dort
# kommentiert; mein erster Entwurf hat sie trotzdem kopiert und war deshalb stumm.)
UPDATED_NO="$(sed -n "${FM_START},${FM_END}p" "$TARGET" | grep -n '^updated: ' | cut -d: -f1 || true)"
COUNT="$(sed -n "${FM_START},${FM_END}p" "$TARGET" | grep -c '^updated: ' || true)"
[[ -n "$UPDATED_NO" ]] || die "keine '^updated: '-Zeile in der Frontmatter — dann ist die Kette fuer jedes Werkzeug unsichtbar (der Defekt vom 2026-10-02 und sein Regression vom 2026-10-03)"
[[ "$COUNT" -eq 1 ]] || die "die Frontmatter traegt $COUNT 'updated: '-Zeilen, erwartet genau 1 (Zeile $((FM_START + UPDATED_NO - 1)))"
UPDATED_NO=$(( FM_START + UPDATED_NO - 1 ))

OLD_LINE="$(sed -n "${UPDATED_NO}p" "$TARGET")"
OLD_BODY="${OLD_LINE#updated: }"
echo "OK  Kette gefunden (Zeile $UPDATED_NO, ${#OLD_BODY} B, $(grep -c ' | ' <<<"$OLD_BODY" || true) Trenner)"

# ---------------------------------------------------------------- neue Zeile bauen
NEW_BODY="$FADEN | $OLD_BODY"
# (b) Byte-Buchhaltung
EXPECTED="$FADEN | $OLD_BODY"
[[ "$NEW_BODY" == "$EXPECTED" ]] || die "Byte-Buchhaltung schlägt fehl"
# (c) Werkzeugvertrag am echten Ergebnis: jeder Faden beginnt mit ' | '
python3 - "$NEW_BODY" <<'PYEOF' || exit 1
import re, sys
body = sys.argv[1]
for m in re.finditer(r"\d{4}-\d{2}-\d{2} \(", body):
    i = m.start()
    if i and not body[:i].endswith(" | "):
        print(f"ABBRUCH: ein Faden beginnt bei {i} ohne ' | '-Trenner — {body[max(0,i-30):i+30]!r}", file=sys.stderr)
        sys.exit(1)
PYEOF
echo "OK  jeder Faden der neuen Kette beginnt mit ' | '"

# ---------------------------------------------------------------- Datei bauen
TOTAL="$(wc -l < "$TARGET")"
{ sed -n "1,$((UPDATED_NO - 1))p" "$TARGET"
  printf 'updated: %s\n' "$NEW_BODY"
  sed -n "$((UPDATED_NO + 1)),\$p" "$TARGET"
} > "$WORK/new"

# (d) Roundtrip: alte Zeile zurück eingesetzt == Original
{ sed -n "1,$((UPDATED_NO - 1))p" "$WORK/new"
  printf '%s\n' "$OLD_LINE"
  sed -n "$((UPDATED_NO + 1)),\$p" "$WORK/new"
} > "$WORK/roundtrip"
cmp -s "$WORK/roundtrip" "$WORK/orig" \
  || die "Roundtrip fehlgeschlagen — nur die 'updated:'-Zeile darf sich aendern, sonst nichts"
echo "OK  Roundtrip: nur die 'updated:'-Zeile weicht vom Original ab"

# (e) genau eine Feldzeile
COUNT_NEW="$(sed -n "${FM_START},${FM_END}p" "$WORK/new" | grep -c '^updated: ' || true)"
[[ "$COUNT_NEW" -eq 1 ]] || die "in der neuen Datei stehen $COUNT_NEW 'updated: '-Zeilen, erwartet 1"
# Der Closer steht in der NEUEN Datei weiterhin in FM_END: die Zeile wurde 1:1 ersetzt, es
# verschiebt sich also nichts. (FM_END+1 waere die Zeile DANACH — mein erster Entwurf pruefte
# die und brach deshalb jeden Happy-Path ab.)
sed -n "${FM_END}p" "$WORK/new" | grep -qx -- '---' \
  || die "der Frontmatter-Closer steht nicht mehr auf eigener Zeile"
echo "OK  genau eine 'updated: '-Zeile, Frontmatter-Closer auf eigener Zeile"

# ---------------------------------------------------------------- schreiben
cp "$TARGET" "${TARGET}.bak"
cp "$WORK/new" "$TARGET"
echo "OK  $TARGET: $(wc -c < "$WORK/orig") B → $(wc -c < "$TARGET") B  (+$(( $(wc -c < "$TARGET") - $(wc -c < "$WORK/orig") )) B)"
echo "    Backup: ${TARGET}.bak  (nach Sichtprüfung löschen)"
