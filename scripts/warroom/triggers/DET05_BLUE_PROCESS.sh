#!/usr/bin/env bash
set -Eeuo pipefail
SCENARIO_ID="DET-05"
EVIDENCE_DIR="${CCC_TRIGGER_EVIDENCE_DIR:-$HOME/ccc-trigger-evidence}"
mkdir -p "$EVIDENCE_DIR"
echo "$SCENARIO_ID BENIGN PROCESS / COMMAND"
python3 "$(dirname "$0")/ccc_local_guard.py" --name CCC-SOC-BLUE --role defensive_monitoring_sensor >/dev/null
command -v auditctl >/dev/null || { echo "HOLD_MISSING_SENSOR: auditctl not present; no process event will be fabricated." >&2; exit 8; }
if command -v systemctl >/dev/null && ! systemctl is-active --quiet auditd 2>/dev/null; then
  echo "HOLD_MISSING_SENSOR: auditd is not active." >&2; exit 9
fi
if ! auditctl -l 2>/dev/null | grep -Eq '(^|[[:space:]])-S[[:space:]].*(execve|execveat)|execve|execveat'; then
  echo "HOLD_MISSING_SENSOR: no existing execve/execveat audit rule was confirmed." >&2
  exit 10
fi
TS="$(date -u +%Y-%m-%dT%H:%M:%SZ)"
RUN_ID="${SCENARIO_ID}-$(date -u +%Y%m%dT%H%M%SZ)"
OUT="$EVIDENCE_DIR/${RUN_ID}-process-trigger.txt"
echo "trigger_time=$TS" | tee "$OUT"
/bin/sh -c 'printf "%s\n" "CCC_DET05_BENIGN_PROCESS" >/dev/null'
echo "benign_process_exit=0" | tee -a "$OUT"
python3 - "$EVIDENCE_DIR/${RUN_ID}-trigger.json" "$RUN_ID" "$TS" "$OUT" <<'PY'
import json,sys
path,run,ts,out=sys.argv[1:]
json.dump({'scenario_id':'DET-05','run_id':run,'trigger_time':ts,'source_host':'CCC-SOC-BLUE','target_host':'CCC-SOC-BLUE','trigger_class':'BENIGN_PROCESS','process':'/bin/sh','marker':'CCC_DET05_BENIGN_PROCESS','sensor_preflight':'auditd_exec_rule_confirmed','local_trigger_evidence':out,'synthetic':False},open(path,'w'),indent=2)
PY
echo "TRIGGER_RECORDED $RUN_ID"
