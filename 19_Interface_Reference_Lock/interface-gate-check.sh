#!/usr/bin/env bash
set -euo pipefail

STATE_DIR="${FA_STATE_DIR:-$HOME/.config/FreedomArchitect/state}"
VISUAL_STATE="${CCC_VISUAL_STATE:-$HOME/CCC_LIVING_OS/00_HOME/CCC_INFINITY_VISUAL_MASTER/state/current.json}"
RATIFICATION="$STATE_DIR/interface-human-ratification.json"
mkdir -p "$STATE_DIR"
chmod 700 "$STATE_DIR" 2>/dev/null || true
OUT="$STATE_DIR/INTERFACE_MATCH.state"

if [ ! -f "$VISUAL_STATE" ]; then
  printf '%s\n' HOLD > "$OUT"
  chmod 600 "$OUT" 2>/dev/null || true
  echo "INTERFACE_MATCH -> HOLD"
  echo "Missing machine state: $VISUAL_STATE"
  exit 0
fi

RESULT="$(python3 - "$VISUAL_STATE" "$RATIFICATION" <<'PY'
import json, pathlib, sys
p=pathlib.Path(sys.argv[1]); r=pathlib.Path(sys.argv[2])
try:
    d=json.loads(p.read_text(encoding='utf-8'))
except Exception:
    print('HOLD|INVALID_STATE_JSON'); raise SystemExit

master=d.get('canonical_visual_master') or {}
runtime=d.get('runtime') or {}
sha=str(master.get('sha256','')).lower()
technical = all(str(v).upper() == 'PASS' for v in [
    master.get('served_exact_bytes'),
    runtime.get('static_validation'),
    runtime.get('staging_exact_runtime'),
    runtime.get('production_exact_runtime'),
    runtime.get('pid_listener_match'),
    runtime.get('owner_identity'),
    runtime.get('exact_release_identity'),
    runtime.get('current_symlink'),
])

ratified=False
if technical and sha and r.is_file():
    try:
        receipt=json.loads(r.read_text(encoding='utf-8'))
        ratified=(str(receipt.get('sha256','')).lower()==sha and receipt.get('human_ratified') is True)
    except Exception:
        ratified=False

if technical and ratified:
    print('PASS|TECHNICAL_PASS_AND_HUMAN_RATIFICATION_SHA_MATCH')
elif technical:
    print('REVIEW|TECHNICAL_PASS_HUMAN_VISUAL_RATIFICATION_REQUIRED')
else:
    print('HOLD|TECHNICAL_INTERFACE_EVIDENCE_INCOMPLETE')
PY
)"

GATE="${RESULT%%|*}"
DETAIL="${RESULT#*|}"
printf '%s\n' "$GATE" > "$OUT"
chmod 600 "$OUT" 2>/dev/null || true
printf 'INTERFACE_MATCH -> %s\n' "$GATE"
printf 'DETAIL -> %s\n' "$DETAIL"
printf 'SOURCE -> %s\n' "$VISUAL_STATE"
