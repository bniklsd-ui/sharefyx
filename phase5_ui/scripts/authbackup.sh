#!/usr/bin/env bash
#
# authbackup.sh — verschlüsseltes Backup der `auth.sqlite3` (Plan §5 Step 8, P5-R).
#
# Warum überhaupt: der `DATA_ROOT` wird seit P3 als Git-Bundle gesichert, die **Auth-Datenbank
# nicht**. Dort liegen Passwort-Hashes, verschlüsselte TOTP-Seeds, Recovery-Codes, Token-Familien
# und UI-Sitzungen. Ohne dieses Backup kostet ein Plattenschaden beide Konten — die Notizen wären
# da, aber niemand käme mehr an sie heran.
#
# **Warum verschlüsselt und nicht einfach kopiert:** die Datei enthält echte Geheimnisse (die
# TOTP-Seeds sind umkehrbar, anders als die reinen Hashes aus P2/P3 — siehe Hard Rule 1,
# Ergänzung vom 2026-07-30). Eine Klartextkopie in einem Backup-Verzeichnis wäre ein zweiter,
# schlechter gesicherter Aufbewahrungsort für genau die Werte, die sonst im Keyring bzw. hinter
# `systemd-creds` liegen. `systemd-creds encrypt` bindet die Kopie an den Host-Schlüssel dieser
# Maschine: kein zusätzliches Schlüsselmaterial, das jemand verwalten (und verlieren) müsste.
#
# **Warum `sqlite3 .backup` und kein `cp`:** die Datenbank wird von einem laufenden Dienst
# benutzt. `cp` kann eine Datei mitten in einer Transaktion erwischen; `.backup` benutzt SQLites
# Online-Backup-API und liefert einen konsistenten Stand ohne den Dienst anzuhalten.
#
# Konfiguration ausschließlich über Umgebungsvariablen, kein Literal im Skript:
#   SHAREFYX_AUTH_DB          Pflicht — Pfad der auth.sqlite3
#   SHAREFYX_AUTH_BACKUP_DIR  Pflicht — Zielverzeichnis der verschlüsselten Generationen
#   SHAREFYX_AUTH_BACKUP_KEEP Optional, Default 7
#   SHAREFYX_CREDS_NAME       Optional, Default sharefyx-auth-backup
#
# Läuft als root: `systemd-creds encrypt --with-key=host` liest
# `/var/lib/systemd/credential.secret` (0600, root).
#
# Ausgabe: genau eine JSON-Zeile auf stdout (Hard Rule 7), aller Fortschritt auf stderr.

set -euo pipefail

AUTH_DB="${SHAREFYX_AUTH_DB:?SHAREFYX_AUTH_DB muss gesetzt sein}"
BACKUP_DIR="${SHAREFYX_AUTH_BACKUP_DIR:?SHAREFYX_AUTH_BACKUP_DIR muss gesetzt sein}"
KEEP="${SHAREFYX_AUTH_BACKUP_KEEP:-7}"
CREDS_NAME="${SHAREFYX_CREDS_NAME:-sharefyx-auth-backup}"

if [[ ! -f "$AUTH_DB" ]]; then
  echo "ABBRUCH: $AUTH_DB existiert nicht." >&2
  exit 1
fi

mkdir -p "$BACKUP_DIR"
chmod 0700 "$BACKUP_DIR"

# Der einzige Ort, an dem die Datenbank je im Klartext auf der Platte liegt. `mktemp -d` legt mit
# 0700 an, `trap … EXIT` räumt auch bei Abbruch, Fehler und Signal auf — und die Unit setzt
# zusätzlich `PrivateTmp=true`, das Verzeichnis ist also nicht einmal für andere Dienste sichtbar.
workdir="$(mktemp -d)"
trap 'rm -rf "$workdir"' EXIT

timestamp="$(date -u +%Y%m%dT%H%M%S.%6NZ)"
plain="$workdir/auth-${timestamp}.sqlite3"
target="$BACKUP_DIR/auth-${timestamp}.cred"

echo "konsistente Kopie über die SQLite-Backup-API" >&2
sqlite3 "$AUTH_DB" ".backup '$plain'" >&2

echo "verschlüssele nach $target" >&2
systemd-creds encrypt --name="$CREDS_NAME" "$plain" "$target" >&2
chmod 0600 "$target"

# Verifikation, gleiche Disziplin wie `backup_data_root.sh` („ein unverifiziertes Bundle ist
# schlimmer als keins, es täuscht Sicherheit vor"): sofort wieder entschlüsseln und die
# Datenbank öffnen. Das fängt einen kaputten oder gewechselten Host-Schlüssel am Tag des
# Backups auf — nicht erst am Tag, an dem man es braucht.
echo "verifiziere: entschlüsseln + PRAGMA integrity_check" >&2
verify="$workdir/verify.sqlite3"
if ! systemd-creds decrypt --name="$CREDS_NAME" "$target" "$verify" >&2; then
  rm -f "$target"
  echo "ABBRUCH: frisch geschriebenes Backup ist nicht entschlüsselbar, Datei gelöscht." >&2
  exit 1
fi
integrity="$(sqlite3 "$verify" "PRAGMA integrity_check;" 2>/dev/null || echo "fehlgeschlagen")"
if [[ "$integrity" != "ok" ]]; then
  rm -f "$target"
  echo "ABBRUCH: integrity_check meldet '$integrity', Datei gelöscht." >&2
  exit 1
fi

# Retention: ISO-ähnliche Zeitstempel sortieren lexikografisch korrekt, kein Parsing nötig.
mapfile -t generations < <(find "$BACKUP_DIR" -maxdepth 1 -name 'auth-*.cred' | sort)
count=${#generations[@]}
if (( count > KEEP )); then
  to_delete=$(( count - KEEP ))
  for ((i = 0; i < to_delete; i++)); do
    echo "entfernt (Retention, KEEP=$KEEP): ${generations[$i]}" >&2
    rm -f "${generations[$i]}"
  done
fi

bytes="$(stat -c%s "$target")"
printf '{"ts":"%s","backup":"%s","bytes":%s,"generations":%s,"verified":true}\n' \
  "$(date -u +%Y-%m-%dT%H:%M:%S.%3NZ)" "$target" "$bytes" "$(( count > KEEP ? KEEP : count ))"
