#!/usr/bin/env bash
#
# restore_auth_check.sh — entschlüsselt die JÜNGSTE Auth-Backup-Generation in ein
# Wegwerf-Verzeichnis, öffnet sie und zählt Zeilen je Tabelle (Plan §5 Step 8, P5-R).
#
# Gegenstück zu `phase3_edge/scripts/restore_check.sh`, das dasselbe für den `DATA_ROOT` tut.
# **Der Nachweis ist der Lauf, nicht das Skript** — das ist die Lehre aus P3 Abnahmezeile 13:
# das Restore-Skript existierte dort monatelang, und die Zeile fiel erst, als jemand es
# tatsächlich ausgeführt hat.
#
# Rein lesend gegenüber dem Backup-Verzeichnis: es wird nichts gelöscht, nichts überschrieben,
# nichts zurückgespielt. Ein Skript, das im Ernstfall Daten anfasst, prüft man ungern.
#
# Konfiguration ausschließlich über Umgebungsvariablen, kein Literal im Skript:
#   SHAREFYX_AUTH_BACKUP_DIR  Pflicht — Verzeichnis mit den *.cred-Generationen
#   SHAREFYX_CREDS_NAME       Optional, Default sharefyx-auth-backup
#
# Läuft als root (die Generationen sind 0600/root, und `systemd-creds decrypt` braucht den
# Host-Schlüssel).
#
# Ausgabe: genau eine JSON-Zeile auf stdout (Hard Rule 7), aller Fortschritt auf stderr.
# Exit ≠ 0 bei jeder Abweichung.

set -euo pipefail

BACKUP_DIR="${SHAREFYX_AUTH_BACKUP_DIR:?SHAREFYX_AUTH_BACKUP_DIR muss gesetzt sein}"
CREDS_NAME="${SHAREFYX_CREDS_NAME:-sharefyx-auth-backup}"

latest="$(find "$BACKUP_DIR" -maxdepth 1 -name 'auth-*.cred' | sort | tail -n1)"
if [[ -z "$latest" ]]; then
  echo "ABBRUCH: keine Generation in $BACKUP_DIR gefunden." >&2
  exit 1
fi

workdir="$(mktemp -d)"
trap 'rm -rf "$workdir"' EXIT

restored="$workdir/auth.sqlite3"
echo "entschlüssele $latest" >&2
systemd-creds decrypt --name="$CREDS_NAME" "$latest" "$restored" >&2

integrity="$(sqlite3 "$restored" "PRAGMA integrity_check;" 2>/dev/null || echo "fehlgeschlagen")"
if [[ "$integrity" != "ok" ]]; then
  echo "ABBRUCH: integrity_check meldet '$integrity'." >&2
  exit 1
fi

# Tabellen aus `sqlite_master` lesen statt einer fest verdrahteten Liste: das Schema wächst
# (Schema 2 kam in P5 Step 2 dazu), und eine Liste im Skript wäre genau die Art Kopie, die
# unbemerkt veraltet und dann eine neue Tabelle stillschweigend nicht prüft.
mapfile -t tables < <(
  sqlite3 "$restored" \
    "SELECT name FROM sqlite_master WHERE type='table' AND name NOT LIKE 'sqlite_%' ORDER BY name;"
)
if (( ${#tables[@]} == 0 )); then
  echo "ABBRUCH: wiederhergestellte Datenbank enthält keine einzige Tabelle." >&2
  exit 1
fi

counts=""
total=0
for table in "${tables[@]}"; do
  n="$(sqlite3 "$restored" "SELECT COUNT(*) FROM \"$table\";")"
  echo "  $table: $n" >&2
  total=$(( total + n ))
  [[ -n "$counts" ]] && counts="$counts,"
  counts="$counts\"$table\":$n"
done

# Eine Auth-Datenbank ohne einen einzigen Nutzer ist zwar formal gültig, als Backup aber wertlos
# — und genau der Fall, der beim Wiederherstellen am meisten wehtut.
users="$(sqlite3 "$restored" "SELECT COUNT(*) FROM users;" 2>/dev/null || echo 0)"
if (( users == 0 )); then
  echo "ABBRUCH: wiederhergestellte Datenbank enthält keine Nutzer (users=0)." >&2
  exit 1
fi

printf '{"ts":"%s","backup":"%s","ok":true,"tables":%s,"rows_total":%s,"counts":{%s}}\n' \
  "$(date -u +%Y-%m-%dT%H:%M:%S.%3NZ)" "$latest" "${#tables[@]}" "$total" "$counts"
