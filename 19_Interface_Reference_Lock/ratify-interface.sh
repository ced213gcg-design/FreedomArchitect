#!/usr/bin/env bash
set -euo pipefail

BASE="${FA_BASE:-$HOME/FreedomArchitect}"
STATE_DIR="${FA_STATE_DIR:-$HOME/.config/FreedomArchitect/state}"
VISUAL_STATE="${CCC_VISUAL_STATE:-$HOME/CCC_LIVING_OS/00_HOME/CCC_INFINITY_VISUAL_MASTER/state/current.json}"
RATIFICATION="$STATE_DIR/interface-human-ratification.json"

[ "${1:-}" = "RATIFY" ] || {
  echo "Usage: $0 RATIFY" >&2
  echo "Run only after Human Command visually confirms the live interface matches the approved reference." >&2
  exit 2
}

"$BASE/19_Interface_Reference_Lock/interface-gate-check.sh" >/dev/null
CURRENT="$(tr -d '[:space:]' < "$STATE_DIR/INTERFACE_MATCH.state" 2>/dev/null || true)"
[ "$CURRENT" = "REVIEW" ] || {
  echo "BLOCKED: technical interface gate must be REVIEW before visual ratification; current=$CURRENT" >&2
  exit 3
}

python3 - "$VISUAL_STATE" "$RATIFICATION" <<'PY'
import datetime as dt, json, pathlib, sys
src=pathlib.Path(sys.argv[1]); out=pathlib.Path(sys.argv[2])
d=json.loads(src.read_text(encoding='utf-8'))
master=d.get('canonical_visual_master') or {}
sha=str(master.get('sha256','')).lower()
if not sha:
    raise SystemExit('BLOCKED: canonical visual SHA missing')
receipt={
    'schema':'unc.interface.human-ratification.v1',
    'timestamp_utc':dt.datetime.now(dt.timezone.utc).isoformat(),
    'human_ratified':True,
    'sha256':sha,
    'machine_state_source':str(src),
    'note':'Human Command visually ratified the exact SHA-bound interface after technical REVIEW.'
}
out.write_text(json.dumps(receipt,indent=2)+'\n',encoding='utf-8')
PY
chmod 600 "$RATIFICATION" 2>/dev/null || true
"$BASE/19_Interface_Reference_Lock/interface-gate-check.sh"
