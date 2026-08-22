#!/usr/bin/env bash
set -euo pipefail

deactivate 2>/dev/null || true
cd "$HOME"

STAMP="$(date +%Y%m%d-%H%M%S)"
REPO="$HOME/FreedomArchitect"
BRANCH="upgrade/ccc-v10-1-aesthetic-vanguard"
REMOTE="https://github.com/ced213gcg-design/FreedomArchitect.git"

echo "=========================================="
echo " CCC v10.1 VANGUARD / HP PREVIEW"
echo "=========================================="

if [ -d "$REPO" ] && [ ! -d "$REPO/.git" ]; then
  echo "[1/11] Preserving existing non-Git folder..."
  mv "$REPO" "${REPO}_PREVANGUARD_$STAMP"
fi

echo "[2/11] Ensuring HP/Crostini prerequisites..."
sudo apt-get update
sudo apt-get install -y git python3 python3-venv python3-pip nodejs npm

if [ -d "$REPO/.git" ]; then
  echo "[3/11] Reusing verified Git repository..."
  cd "$REPO"
  git fetch origin
  git switch "$BRANCH" 2>/dev/null || git switch -c "$BRANCH" --track "origin/$BRANCH"
  git pull --ff-only origin "$BRANCH"
else
  echo "[3/11] Cloning Vanguard branch from GitHub..."
  git clone --branch "$BRANCH" --single-branch "$REMOTE" "$REPO"
  cd "$REPO"
fi

echo "[4/11] Verifying repository identity..."
git status --short --branch
git branch --show-current
git rev-parse HEAD

echo "[5/11] Creating isolated Python environment..."
rm -rf .venv
python3 -m venv .venv
source .venv/bin/activate
python -m pip install --upgrade pip
python -m pip install -r requirements.txt

echo "[6/11] Validating CCC repository contracts..."
python scripts/validate_ccc_repo.py

echo "[7/11] Running Python regression suite..."
python -m pytest -q --import-mode=importlib

echo "[8/11] Testing Vanguard 4D Living Sphere..."
node scripts/test_sphere.js

echo "[9/11] Testing Vanguard Exception Constellation..."
node scripts/test_exception_constellation.js

echo "[10/11] Testing Vanguard UI/accessibility contract..."
node scripts/test_vanguard_ui.js

echo "[11/11] Starting CCC Living Intelligence Vanguard..."
echo
echo "=========================================="
echo " VANGUARD DASHBOARD"
echo " http://127.0.0.1:8787"
echo "=========================================="
echo
exec python 19_Live_Adaptive_Dashboard/backend/app.py
