#!/usr/bin/env bash
#
# install_units.sh — ersetzt die sechs Platzhalter (__REPO_ROOT__, __DATA_ROOT__, __VENV__,
# __ALLOWED_HOSTS__, __AUTH_MODE__, __PUBLIC_BASE_URL__) in den Unit-Vorlagen aus
# phase3_edge/local.env und installiert die Ergebnisse nach /etc/systemd/system/. Bricht ab,
# wenn local.env fehlt oder ein Platzhalter unersetzt bleibt (Plan §4 Step 4, P4 §5 Step 7).
#
# **P4 Step 7:** `sharefyx-mcp.service` zog nach `phase4_auth/systemd/` um (die MCP-Unit ist ab
# P4 inhaltlich eine P4-Unit — StateDirectory, zweites Credential, zwei neue Environment-Zeilen).
# Die beiden Backup-Units (`sharefyx-backup.service`/`.timer`) bleiben in `phase3_edge/systemd/`
# — dieses Skript bleibt P3-Eigentum, liest jetzt aber aus **beiden** Verzeichnissen.
#
# Legt KEINE Credential-Datei an — das ist ein manueller Schritt des Nikingers (Plan §2.1,
# README.md „Rotation im Dienstbetrieb").
#
# Aufruf: sudo phase3_edge/scripts/install_units.sh

set -euo pipefail

SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
PHASE_DIR="$(cd "$SCRIPT_DIR/.." && pwd)"
REPO_DIR="$(cd "$PHASE_DIR/.." && pwd)"
LOCAL_ENV="$PHASE_DIR/local.env"
SYSTEMD_SRCS=("$PHASE_DIR/systemd" "$REPO_DIR/phase4_auth/systemd")
SYSTEMD_DEST="/etc/systemd/system"

if [[ ! -f "$LOCAL_ENV" ]]; then
  echo "ABBRUCH: $LOCAL_ENV fehlt. cp phase3_edge/local.env.example phase3_edge/local.env, dann ausfüllen." >&2
  exit 1
fi

# shellcheck disable=SC1090
source "$LOCAL_ENV"

for var in REPO_ROOT DATA_ROOT VENV ALLOWED_HOSTS AUTH_MODE PUBLIC_BASE_URL; do
  if [[ -z "${!var:-}" ]]; then
    echo "ABBRUCH: $var ist in $LOCAL_ENV leer oder fehlt." >&2
    exit 1
  fi
done

shopt -s nullglob
units=()
for src in "${SYSTEMD_SRCS[@]}"; do
  units+=("$src"/*.service "$src"/*.timer)
done
shopt -u nullglob

if [[ ${#units[@]} -eq 0 ]]; then
  echo "ABBRUCH: keine Unit-Dateien in ${SYSTEMD_SRCS[*]} gefunden." >&2
  exit 1
fi

mkdir -p "$SYSTEMD_DEST"

for unit in "${units[@]}"; do
  name="$(basename "$unit")"
  dest="$SYSTEMD_DEST/$name"
  sed \
    -e "s#__REPO_ROOT__#${REPO_ROOT}#g" \
    -e "s#__DATA_ROOT__#${DATA_ROOT}#g" \
    -e "s#__VENV__#${VENV}#g" \
    -e "s#__ALLOWED_HOSTS__#${ALLOWED_HOSTS}#g" \
    -e "s#__AUTH_MODE__#${AUTH_MODE}#g" \
    -e "s#__PUBLIC_BASE_URL__#${PUBLIC_BASE_URL}#g" \
    "$unit" > "$dest"

  if grep -qE '__[A-Z_]+__' "$dest"; then
    echo "ABBRUCH: $dest enthält noch einen unaufgelösten Platzhalter." >&2
    rm -f "$dest"
    exit 1
  fi
  echo "installiert: $dest"
done

systemctl daemon-reload
systemctl enable --now sharefyx-mcp.service

echo "sharefyx-mcp.service installiert und gestartet."
echo "Credential-Dateien (/etc/sharefyx/spaces.cred, /etc/sharefyx/auth-users.cred) sind NICHT" \
     "Teil dieses Skripts — siehe README.md, Abschnitt 'Token ausgeben, rotieren, widerrufen'" \
     "bzw. phase4_auth/CLAUDE.md fürs Auth-Credential."
