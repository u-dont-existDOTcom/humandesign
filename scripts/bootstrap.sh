#!/usr/bin/env bash
set -euo pipefail

repo_dir="$(cd "$(dirname "${BASH_SOURCE[0]}")/.." && pwd)"
venv_dir="${repo_dir}/.venv"

python3 -m venv "${venv_dir}"
"${venv_dir}/bin/python" -m pip install --upgrade pip
"${venv_dir}/bin/python" -m pip install -e "${repo_dir}[all,dev]"
"${venv_dir}/bin/python" -m pytest --collect-only -q

echo "Bootstrap complete. Run: ${venv_dir}/bin/hdmatch --help"

