#!/usr/bin/env bash
set -Eeuo pipefail

BRANCH="hotfix/ccc-soc-five-live-evidence-v1"
STAMP="$(date -u +%Y%m%dT%H%M%SZ)"
STEP="INIT"
BRIDGE_PID=""
DASH_PID=""

fail() {
  local rc=$?
  echo
  echo "============================================================" >&2
  echo "CCC HP WAR ROOM HARD FAIL" >&2
  echo "FAILED STEP: ${STEP}" >&2
  echo "EXIT CODE: ${rc}" >&2
  echo "NEXT REPAIR TARGET: inspect the command immediately above; no later hard gate was executed." >&2
  echo "============================================================" >&2
  exit "$rc"
}
trap fail ERR

step() {
  STEP="$1"
  echo
  echo "[$STEP] $2"
}

locate_repo() {
  if [[ -d "$HOME/FreedomArchitect/.git" ]]; then
    printf '%s\n' "$HOME/FreedomArchitect"
    return 0
  fi
  local found
  found="$(find "$HOME" -maxdepth 3 -type d -name .git -path '*/FreedomArchitect/.git' -print -quit 2>/dev/null || true)"
  [[ -n "$found" ]] || return 1
  dirname "$found"
}

step "PREFLIGHT-01" "Confirm Linux/Crostini-compatible host"
[[ "$(uname -s)" == "Linux" ]]
command -v git >/dev/null
command -v python3 >/dev/null
command -v node >/dev/null

step "PREFLIGHT-02" "Locate real FreedomArchitect Git repository"
REPO="$(locate_repo)"
cd "$REPO"
git rev-parse --is-inside-work-tree >/dev/null
[[ -d .git ]]

step "PRESERVE-03" "Preserve uncommitted work with timestamped stash when needed"
if [[ -n "$(git status --porcelain)" ]]; then
  STASH_LABEL="ccc-hp-warroom-preflight-$STAMP"
  git stash push -u -m "$STASH_LABEL" >/dev/null
  echo "Preserved local work in stash: $STASH_LABEL"
else
  echo "Working tree already clean."
fi

step "SYNC-04" "Fetch origin and switch to mission branch"
git fetch --prune origin
git switch "$BRANCH" 2>/dev/null || git switch -c "$BRANCH" --track "origin/$BRANCH"
git pull --ff-only origin "$BRANCH"
CURRENT_SHA="$(git rev-parse HEAD)"
echo "Branch: $(git branch --show-current)"
echo "SHA: $CURRENT_SHA"

step "PYTHON-05" "Create or reuse isolated Python environment"
python3 -m venv .venv
# shellcheck disable=SC1091
source .venv/bin/activate
python -m pip install --upgrade pip
python -m pip install -r requirements.txt

step "VALIDATE-06" "Run repository validator"
python scripts/validate_ccc_repo.py

step "TEST-07" "Run full Python test suite"
python -m pytest -q --import-mode=importlib

step "TEST-08" "Run Vanguard and SOC interaction Node tests"
node scripts/test_sphere.js
node scripts/test_exception_constellation.js
node scripts/test_soc_interaction_ui.js

step "SESSION-09" "Create local physical evidence workspace"
mkdir -p runtime/soc artifacts/soc-live-five/{screenshots,normalized,report}
chmod 700 runtime/soc artifacts/soc-live-five || true
TOKEN_FILE="$REPO/runtime/soc/.bridge-token"
python - <<'PY' > "$TOKEN_FILE"
import secrets
print(secrets.token_urlsafe(48))
PY
chmod 600 "$TOKEN_FILE"
export CCC_BRIDGE_TOKEN="$(cat "$TOKEN_FILE")"
export CCC_SOC_STATE_PATH="$REPO/runtime/soc/ccc-soc-live-state.json"
export CCC_BRIDGE_PAYLOAD_PATH="$REPO/runtime/soc/ccc-soc-bridge-payload.json"

step "BRIDGE-10" "Preflight receive-only Evidence Bridge or select honest file fallback"
BRIDGE_MODE="FILE_FALLBACK"
BRIDGE_ADDRESS=""
if [[ "${CCC_ENABLE_LAN_BRIDGE:-0}" == "1" ]]; then
  BIND_ADDR="${CCC_BRIDGE_BIND:-0.0.0.0}"
  export CCC_BRIDGE_BIND="$BIND_ADDR"
  python 19_Live_Adaptive_Dashboard/backend/evidence_bridge.py --host "$BIND_ADDR" --port "${CCC_BRIDGE_PORT:-8790}" > runtime/soc/evidence-bridge.log 2>&1 &
  BRIDGE_PID=$!
  sleep 1
  if kill -0 "$BRIDGE_PID" 2>/dev/null && python - <<'PY'
import json, urllib.request
with urllib.request.urlopen('http://127.0.0.1:8790/health', timeout=2) as r:
    data=json.load(r)
    assert r.status==200 and data['status']=='PASS' and data['mode']=='RECEIVE_ONLY'
PY
  then
    LAN_IP="$(hostname -I 2>/dev/null | tr ' ' '\n' | grep -E '^[0-9]+\.[0-9]+\.[0-9]+\.[0-9]+$' | grep -v '^127\.' | head -n1 || true)"
    if [[ -n "$LAN_IP" ]]; then
      BRIDGE_MODE="HTTP_LAN"
      BRIDGE_ADDRESS="http://${LAN_IP}:${CCC_BRIDGE_PORT:-8790}/bridge/v1/evidence"
    else
      kill "$BRIDGE_PID" 2>/dev/null || true
      BRIDGE_PID=""
      BRIDGE_MODE="FILE_FALLBACK"
    fi
  else
    [[ -z "$BRIDGE_PID" ]] || kill "$BRIDGE_PID" 2>/dev/null || true
    BRIDGE_PID=""
  fi
fi
export CCC_BRIDGE_MODE="$BRIDGE_MODE"

step "MANIFEST-11" "Write local session manifest without secret material"
SESSION_MANIFEST="$REPO/artifacts/soc-live-five/session-manifest.json"
export CURRENT_SHA BRANCH BRIDGE_MODE BRIDGE_ADDRESS STAMP SESSION_MANIFEST
python - <<'PY'
import json, os, platform
from pathlib import Path
payload={
  'schema':'ccc.soc.physical.session.v1',
  'timestamp':os.environ['STAMP'],
  'host':'ccc-hp-dev-01',
  'platform':platform.platform(),
  'branch':os.environ['BRANCH'],
  'sha':os.environ['CURRENT_SHA'],
  'bridge_mode':os.environ['BRIDGE_MODE'],
  'bridge_address':os.environ.get('BRIDGE_ADDRESS') or None,
  'soc_state_path':str(Path('runtime/soc/ccc-soc-live-state.json')),
  'state':'VERIFY',
  'token_recorded':False,
  'next_action':'RUN_DELL_ONE_DROP_AND_TRANSFER_SANITIZED_EVIDENCE'
}
Path(os.environ['SESSION_MANIFEST']).write_text(json.dumps(payload,indent=2)+'\n',encoding='utf-8')
PY

step "DASHBOARD-12" "Start CCC Living Dashboard"
python 19_Live_Adaptive_Dashboard/backend/app.py > runtime/soc/dashboard.log 2>&1 &
DASH_PID=$!
sleep 1
kill -0 "$DASH_PID"
python - <<'PY'
import json, urllib.request
with urllib.request.urlopen('http://127.0.0.1:8787/api/health', timeout=3) as r:
    data=json.load(r)
    assert r.status==200 and data['status']=='PASS'
PY

step "REPORT-13" "Print exact operator handoff"
echo
echo "============================================================"
echo "CCC HP SOC WAR ROOM READY FOR PHYSICAL EVIDENCE"
echo "============================================================"
echo "Dashboard URL : http://127.0.0.1:8787"
echo "Branch        : $BRANCH"
echo "SHA           : $CURRENT_SHA"
echo "State         : VERIFY"
echo "Bridge mode   : $BRIDGE_MODE"
if [[ "$BRIDGE_MODE" == "HTTP_LAN" ]]; then
  echo "HP receiver   : $BRIDGE_ADDRESS"
  echo "Bridge token  : stored locally at runtime/soc/.bridge-token (mode 600); do not commit or paste into source files."
  echo "Dell next     : set CCC_HP_BRIDGE_ADDRESS to the receiver URL and CCC_HP_BRIDGE_TOKEN to the session token, then run scripts/warroom/CCC_DELL_SOC_WARROOM_ONE_DROP.ps1 as Administrator."
else
  echo "HP receiver   : not exposed; network bridge not explicitly enabled or did not pass preflight."
  echo "Dell next     : run scripts/warroom/CCC_DELL_SOC_WARROOM_ONE_DROP.ps1 as Administrator; it will emit a sanitized ccc-soc-bridge-payload.json for FILE_FALLBACK."
fi
echo "Session file  : artifacts/soc-live-five/session-manifest.json"
echo "Runtime data  : ignored by Git; do not commit raw physical evidence or secrets."
echo "============================================================"
echo
echo "Processes remain active in this terminal session: dashboard PID=$DASH_PID${BRIDGE_PID:+ bridge PID=$BRIDGE_PID}"
echo "Use Ctrl+C or explicit kill only after evidence review is complete."

wait "$DASH_PID"
