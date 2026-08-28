#!/usr/bin/env bash
set -euo pipefail

STATE_DIR="${FA_STATE_DIR:-$HOME/.config/FreedomArchitect/state}"
VISUAL_STATE="${CCC_VISUAL_STATE:-$HOME/CCC_LIVING_OS/00_HOME/CCC_INFINITY_VISUAL_MASTER/state/current.json}"
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

RESULT="$(python3 - "$VISUAL_STATE" <<'PY'
import json, pathlib, sys
p=pathlib.Path(sys.argv[1])
try:
    d=json.loads(p.read_text(encoding='utf-8'))
except Exception as e:
    print('HOLD|INVALID_STATE_JSON')
    raise SystemExit

master=d.get('canonical_visual_master') or {}
runtime=d.get('runtime') or {}
truth=d.get('truth') or {}

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

ratification=str(truth.get('aesthetic_ratification','NO')).upper()
if technical and ratification in {'PASS','YES','RATIFIED','APPROVED'}:
    print('PASS|TECHNICAL_AND_HUMAN_VISUAL_RATIFIED')
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
