#!/usr/bin/env bash
set -euo pipefail

repo_dir="$(cd "$(dirname "${BASH_SOURCE[0]}")/.." && pwd)"
venv_dir="${repo_dir}/.venv"

python3 -m venv "${venv_dir}"
"${venv_dir}/bin/python" -m pip install --upgrade pip
"${venv_dir}/bin/python" -m pip install -r "${repo_dir}/requirements-dev.lock"
"${venv_dir}/bin/python" -m pip install --no-build-isolation --no-deps -e "${repo_dir}"
"${venv_dir}/bin/python" -m pytest --collect-only -q

echo "Bootstrap complete. Run: ${venv_dir}/bin/hdmatch --help"
