#!/usr/bin/env bash
#
# install_units.sh — ersetzt die vier Platzhalter (__REPO_ROOT__, __DATA_ROOT__, __VENV__,
# __ALLOWED_HOSTS__) in phase3_edge/systemd/*.{service,timer} aus phase3_edge/local.env und
# installiert die Ergebnisse nach /etc/systemd/system/. Bricht ab, wenn local.env fehlt oder ein
# Platzhalter unersetzt bleibt (Plan §4 Step 4).
#
# Legt KEINE Credential-Datei an — das ist ein manueller Schritt des Nikingers (Plan §2.1,
# README.md „Rotation im Dienstbetrieb").
#
# Aufruf: sudo phase3_edge/scripts/install_units.sh

set -euo pipefail

SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
PHASE_DIR="$(cd "$SCRIPT_DIR/.." && pwd)"
LOCAL_ENV="$PHASE_DIR/local.env"
SYSTEMD_SRC="$PHASE_DIR/systemd"
SYSTEMD_DEST="/etc/systemd/system"

if [[ ! -f "$LOCAL_ENV" ]]; then
  echo "ABBRUCH: $LOCAL_ENV fehlt. cp phase3_edge/local.env.example phase3_edge/local.env, dann ausfüllen." >&2
  exit 1
fi

# shellcheck disable=SC1090
source "$LOCAL_ENV"

for var in REPO_ROOT DATA_ROOT VENV ALLOWED_HOSTS; do
  if [[ -z "${!var:-}" ]]; then
    echo "ABBRUCH: $var ist in $LOCAL_ENV leer oder fehlt." >&2
    exit 1
  fi
done

shopt -s nullglob
units=("$SYSTEMD_SRC"/*.service "$SYSTEMD_SRC"/*.timer)
shopt -u nullglob

if [[ ${#units[@]} -eq 0 ]]; then
  echo "ABBRUCH: keine Unit-Dateien in $SYSTEMD_SRC gefunden." >&2
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
echo "Credential-Datei (/etc/sharefyx/spaces.cred) ist NICHT Teil dieses Skripts — siehe" \
     "README.md, Abschnitt 'Token ausgeben, rotieren, widerrufen'."
