#!/usr/bin/env bash
# Editable install aller Phasenpakete. Läuft nach `python -m venv .venv && source .venv/bin/activate`.
set -euo pipefail

repo_root="$(cd "$(dirname "${BASH_SOURCE[0]}")/.." && pwd)"

python -m pip install --upgrade pip

for pkg_dir in "$repo_root"/phase*_*/; do
    if [ -f "$pkg_dir/pyproject.toml" ]; then
        echo "installing editable: $pkg_dir"
        python -m pip install -e "$pkg_dir[dev]"
    fi
done
