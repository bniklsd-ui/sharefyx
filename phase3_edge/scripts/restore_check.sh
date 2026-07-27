#!/usr/bin/env bash
#
# restore_check.sh — klont das jüngste Bundle aus SHAREFYX_BACKUP_DIR in ein Wegwerf-Verzeichnis
# und vergleicht HEAD sowie den Baum (HEAD^{tree}) mit dem echten SHAREFYX_DATA_ROOT (Plan §4
# Step 5). Ein Backup, dessen Restore nie geprüft wurde, ist kein Backup.
#
# Ausgabe: genau eine JSON-Zeile auf stdout bei Erfolg, aller Fortschritt auf stderr. Exit ≠ 0
# bei jeder Abweichung.

set -euo pipefail

DATA_ROOT="${SHAREFYX_DATA_ROOT:?SHAREFYX_DATA_ROOT muss gesetzt sein}"
BACKUP_DIR="${SHAREFYX_BACKUP_DIR:?SHAREFYX_BACKUP_DIR muss gesetzt sein}"

latest="$(find "$BACKUP_DIR" -maxdepth 1 -name 'sharefyx-data-*.bundle' | sort | tail -n1)"
if [[ -z "$latest" ]]; then
  echo "ABBRUCH: kein Bundle in $BACKUP_DIR gefunden." >&2
  exit 1
fi

workdir="$(mktemp -d)"
trap 'rm -rf "$workdir"' EXIT

echo "klone $latest nach $workdir/restore" >&2
git clone --quiet "$latest" "$workdir/restore" >&2

original_head="$(git -C "$DATA_ROOT" rev-parse HEAD)"
original_tree="$(git -C "$DATA_ROOT" rev-parse 'HEAD^{tree}')"
restored_head="$(git -C "$workdir/restore" rev-parse HEAD)"
restored_tree="$(git -C "$workdir/restore" rev-parse 'HEAD^{tree}')"

if [[ "$original_head" != "$restored_head" ]] || [[ "$original_tree" != "$restored_tree" ]]; then
  echo "ABBRUCH: Restore weicht ab — original HEAD=$original_head tree=$original_tree," \
       "restored HEAD=$restored_head tree=$restored_tree" >&2
  exit 1
fi

printf '{"ts":"%s","bundle":"%s","head":"%s","ok":true}\n' \
  "$(date -u +%Y-%m-%dT%H:%M:%S.%3NZ)" "$latest" "$restored_head"
