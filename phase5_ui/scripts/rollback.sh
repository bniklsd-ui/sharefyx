#!/usr/bin/env bash
#
# rollback.sh — legt den `current`-Symlink auf das vorherige Release und startet den Dienst neu
# (Plan §5 Step 8, P5-AB).
#
# **Dieses Skript tut absichtlich fast nichts.** Kein Health-Gate, kein Backup, keine Retention,
# kein Netzzugriff. Ein Rollback wird genau dann gebraucht, wenn ohnehin schon etwas kaputt ist —
# je weniger Schritte es hat, desto weniger kann daran scheitern. Alles, was hier zusätzlich
# stünde, wäre eine weitere Möglichkeit, im Notfall hängenzubleiben.
#
# Konfiguration ausschließlich über Umgebungsvariablen, kein Literal im Skript (dasselbe Muster
# wie phase3_edge/scripts/backup_data_root.sh):
#   SHAREFYX_RELEASES_DIR   Pflicht — Verzeichnis mit den Release-Verzeichnissen
#   SHAREFYX_CURRENT_LINK   Pflicht — der Symlink, den der Dienst benutzt
#   SHAREFYX_SERVICE        Optional, Default sharefyx-mcp
#
# Ausgabe: genau eine JSON-Zeile auf stdout (Hard Rule 7), aller Fortschritt auf stderr.

set -euo pipefail

RELEASES_DIR="${SHAREFYX_RELEASES_DIR:?SHAREFYX_RELEASES_DIR muss gesetzt sein}"
CURRENT_LINK="${SHAREFYX_CURRENT_LINK:?SHAREFYX_CURRENT_LINK muss gesetzt sein}"
SERVICE="${SHAREFYX_SERVICE:-sharefyx-mcp}"

if [[ ! -L "$CURRENT_LINK" ]]; then
  echo "ABBRUCH: $CURRENT_LINK ist kein Symlink — hier gibt es nichts zurückzurollen." >&2
  exit 1
fi

current_target="$(readlink -f "$CURRENT_LINK")"

# Release-Verzeichnisse tragen lexikografisch sortierbare UTC-Zeitstempel (siehe deploy.sh) —
# „das vorherige" ist damit schlicht der Eintrag davor, ohne Datumsparserei.
#
# `*.failed` wird ausgeschlossen: `deploy.sh` markiert so ein Release, das den Health-Gate
# gerissen hat und deshalb zurückgerollt wurde. Es bleibt zum Hineinsehen liegen, ist aber das
# jüngste Verzeichnis — ohne diesen Ausschluss wäre ausgerechnet der nachweislich kaputte Stand
# das nächste Rollback-Ziel.
mapfile -t releases < <(
  find "$RELEASES_DIR" -mindepth 1 -maxdepth 1 -type d -not -name '*.failed' | sort
)
if (( ${#releases[@]} < 2 )); then
  echo "ABBRUCH: weniger als zwei Releases in $RELEASES_DIR — kein Ziel für ein Rollback." >&2
  exit 1
fi

previous=""
for ((i = 0; i < ${#releases[@]}; i++)); do
  if [[ "$(readlink -f "${releases[$i]}")" == "$current_target" ]]; then
    if (( i == 0 )); then
      echo "ABBRUCH: $CURRENT_LINK zeigt bereits auf das älteste Release." >&2
      exit 1
    fi
    previous="${releases[$((i - 1))]}"
    break
  fi
done

if [[ -z "$previous" ]]; then
  # Kann passieren, wenn der Symlink auf etwas außerhalb von RELEASES_DIR zeigt (z.B. auf das
  # Arbeitsverzeichnis, siehe Escape-Hatch im Phase-Head). Dann ist das jüngste Release das
  # sinnvollste Ziel — aber nur, weil es hier keine „vorherige" Position gibt, die wir kennen.
  previous="${releases[-1]}"
  echo "HINWEIS: $CURRENT_LINK zeigte auf kein bekanntes Release ($current_target) —" \
       "es wird auf das jüngste gesetzt." >&2
fi

echo "Rollback: $current_target -> $previous" >&2

# Atomar: ein `ln -sfn` auf einen existierenden Symlink ist ein Zwei-Schritt-Vorgang (unlink,
# symlink) und hinterlässt bei einem Abbruch dazwischen gar keinen Link. `mv -T` ersetzt ihn in
# einem einzigen `rename()`.
tmp_link="${CURRENT_LINK}.rollback.$$"
ln -s "$previous" "$tmp_link"
mv -T "$tmp_link" "$CURRENT_LINK"

echo "starte $SERVICE neu" >&2
systemctl restart "$SERVICE" >&2

printf '{"ts":"%s","action":"rollback","from":"%s","to":"%s","service":"%s"}\n' \
  "$(date -u +%Y-%m-%dT%H:%M:%S.%3NZ)" "$current_target" "$previous" "$SERVICE"
