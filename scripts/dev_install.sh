#!/usr/bin/env bash
# Editable install aller Phasenpakete. Läuft nach `python -m venv .venv && source .venv/bin/activate`.
set -euo pipefail

repo_root="$(cd "$(dirname "${BASH_SOURCE[0]}")/.." && pwd)"

# [2026-10-22, P10.5 Block 1, Schritt 1.4 — BT-6, Lock P10.5-Q] `constraints.txt` ist die
# EINZIGE Quelle aller transitiven Versionen: Dev-venv und Deploy gehen beide über dieses
# Skript (deploy.sh ruft das Skript des Releases auf), es gibt also auch nur diesen einen
# Installationsweg. Vorher war das transitive `mcp` ungepinnt — dev 1.28.1, live 1.30.0 —
# und `starlette` dev 1.3.1 gegen live 1.7.0: ein stiller Drift unter einem Dauerdienst,
# den P3-D verbietet.
#
# Fehlt die Datei, bricht das Skript ab. Kein stiller Fallback auf "installiere halt die
# neueste Version" — genau das war der Drift, den dieser Schritt abschafft.
if [ ! -f "$repo_root/constraints.txt" ]; then
    echo "ABBRUCH: $repo_root/constraints.txt fehlt — ohne diese Datei wären die Versionen ungepinnt." >&2
    exit 1
fi

python -m pip install --upgrade pip

for pkg_dir in "$repo_root"/phase*_*/; do
    if [ -f "$pkg_dir/pyproject.toml" ]; then
        echo "installing editable: $pkg_dir"
        python -m pip install -c "$repo_root/constraints.txt" -e "$pkg_dir[dev]"
    fi
done
