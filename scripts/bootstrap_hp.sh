#!/usr/bin/env bash
set -euo pipefail
command -v python3 >/dev/null || { echo "python3 missing"; exit 1; }
python3 -m venv .venv
# shellcheck disable=SC1091
. .venv/bin/activate
pip install -r requirements.txt
python scripts/validate_ccc_repo.py
pytest -q
