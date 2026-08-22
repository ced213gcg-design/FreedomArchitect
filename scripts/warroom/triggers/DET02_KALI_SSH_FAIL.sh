#!/usr/bin/env bash
set -Eeuo pipefail
SCENARIO_ID="DET-02"
TARGET_IP="${CCC_BLUE_TARGET_IP:-}"
PORT="22"
EVIDENCE_DIR="${CCC_TRIGGER_EVIDENCE_DIR:-$HOME/ccc-trigger-evidence}"
mkdir -p "$EVIDENCE_DIR"
echo "$SCENARIO_ID FAILED SSH AUTH"
[[ -n "$TARGET_IP" ]] || { echo "HOLD_MISSING_REGISTERED_BLUE_RANGE_TARGET: set CCC_BLUE_TARGET_IP only after Blue has an explicitly registered 10.69.69.0/24 address." >&2; exit 4; }
TARGET_NAME="$(python3 "$(dirname "$0")/ccc_lab_guard.py" --ip "$TARGET_IP" --role defensive_monitoring_sensor --port "$PORT")"
command -v sshpass >/dev/null || { echo "HOLD_MISSING_SSHPASS" >&2; exit 5; }
TS="$(date -u +%Y-%m-%dT%H:%M:%SZ)"
RUN_ID="${SCENARIO_ID}-$(date -u +%Y%m%dT%H%M%SZ)"
OUT="$EVIDENCE_DIR/${RUN_ID}-ssh-fail.txt"
: > "$OUT"
for attempt in 1 2 3; do
  echo "attempt=$attempt" | tee -a "$OUT"
  sshpass -p 'CCC_DET02_FIXED_INVALID_PASSWORD' ssh -p "$PORT" \
    -o PreferredAuthentications=password -o PubkeyAuthentication=no \
    -o StrictHostKeyChecking=no -o UserKnownHostsFile=/dev/null \
    -o ConnectTimeout=5 -o NumberOfPasswordPrompts=1 \
    ccc-det02-invalid@"$TARGET_IP" true >>"$OUT" 2>&1 || true
done
python3 - "$EVIDENCE_DIR/${RUN_ID}-trigger.json" "$RUN_ID" "$TS" "$TARGET_NAME" "$TARGET_IP" "$OUT" <<'PY'
import json,sys
path,run,ts,name,ip,out=sys.argv[1:]
json.dump({'scenario_id':'DET-02','run_id':run,'trigger_time':ts,'source_host':'CCC-KALI-RED','target_host':name,'target_ip':ip,'trigger_class':'BOUNDED_FAILED_SSH','attempt_count':3,'dummy_user':'ccc-det02-invalid','local_trigger_evidence':out,'synthetic':False},open(path,'w'),indent=2)
PY
echo "TRIGGER_RECORDED $RUN_ID"
