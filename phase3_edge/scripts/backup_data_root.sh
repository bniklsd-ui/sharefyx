#!/usr/bin/env bash
#
# backup_data_root.sh — git bundle des DATA_ROOT + Verifikation + Retention (Plan §4 Step 5).
# Ein unverifiziertes Bundle ist schlimmer als keins (täuscht Sicherheit vor) — deshalb wird ein
# Bundle, das die eigene `git bundle verify` nicht besteht, sofort gelöscht, nicht behalten.
#
# Konfiguration ausschließlich über Umgebungsvariablen, kein Literal im Skript:
#   SHAREFYX_DATA_ROOT    Pflicht — das zu sichernde Git-Repo
#   SHAREFYX_BACKUP_DIR   Pflicht — Zielverzeichnis der Bundles
#   SHAREFYX_BACKUP_KEEP  Optional, Default 14 — wie viele Bundles bleiben
#
# Ausgabe: genau eine JSON-Zeile auf stdout (Hard Rule 7), aller Fortschritt auf stderr.

set -euo pipefail

DATA_ROOT="${SHAREFYX_DATA_ROOT:?SHAREFYX_DATA_ROOT muss gesetzt sein}"
BACKUP_DIR="${SHAREFYX_BACKUP_DIR:?SHAREFYX_BACKUP_DIR muss gesetzt sein}"
KEEP="${SHAREFYX_BACKUP_KEEP:-14}"

mkdir -p "$BACKUP_DIR"

# Mikrosekunden-Auflösung, keine Doppelpunkte im Dateinamen — bleibt lexikografisch sortierbar
# und vermeidet den Zeitstempel-Kollisionsfehler, der mcp_smoke.py in P2 flaky gemacht hat
# (SESSIONS_ARCHIVE.md, Step 7).
timestamp="$(date -u +%Y%m%dT%H%M%S.%6NZ)"
bundle="$BACKUP_DIR/sharefyx-data-${timestamp}.bundle"

echo "erstelle Bundle: $bundle" >&2
git -C "$DATA_ROOT" bundle create "$bundle" --all

echo "verifiziere Bundle" >&2
if ! git bundle verify "$bundle" >&2; then
  rm -f "$bundle"
  echo "ABBRUCH: Bundle-Verifikation fehlgeschlagen, Datei gelöscht: $bundle" >&2
  exit 1
fi

# Retention: älteste über KEEP hinaus löschen. ISO-ähnliche Zeitstempel sortieren
# lexikografisch korrekt, kein Parsing nötig.
mapfile -t bundles < <(find "$BACKUP_DIR" -maxdepth 1 -name 'sharefyx-data-*.bundle' | sort)
count=${#bundles[@]}
if (( count > KEEP )); then
  to_delete=$(( count - KEEP ))
  for ((i = 0; i < to_delete; i++)); do
    echo "entfernt (Retention, KEEP=$KEEP): ${bundles[$i]}" >&2
    rm -f "${bundles[$i]}"
  done
fi

bytes="$(stat -c%s "$bundle")"
printf '{"ts":"%s","bundle":"%s","bytes":%s}\n' \
  "$(date -u +%Y-%m-%dT%H:%M:%S.%3NZ)" "$bundle" "$bytes"
