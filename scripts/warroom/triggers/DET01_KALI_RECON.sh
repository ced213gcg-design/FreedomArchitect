#!/usr/bin/env bash
set -Eeuo pipefail
SCENARIO_ID="DET-01"
TARGET_IP="${CCC_DET01_TARGET_IP:-10.69.69.30}"
TARGET_ROLE="${CCC_DET01_TARGET_ROLE:-honeypot_target}"
PORTS="${CCC_DET01_PORTS:-22,80,443,2222}"
EVIDENCE_DIR="${CCC_TRIGGER_EVIDENCE_DIR:-$HOME/ccc-trigger-evidence}"
mkdir -p "$EVIDENCE_DIR"
echo "$SCENARIO_ID NETWORK RECON"
[[ "$TARGET_ROLE" == "honeypot_target" || "$TARGET_ROLE" == "defensive_monitoring_sensor" ]] || { echo "REJECTED_ROLE" >&2; exit 2; }
TARGET_NAME="$(python3 "$(dirname "$0")/ccc_lab_guard.py" --ip "$TARGET_IP" --role "$TARGET_ROLE")"
command -v nmap >/dev/null || { echo "HOLD_MISSING_NMAP" >&2; exit 3; }
TS="$(date -u +%Y-%m-%dT%H:%M:%SZ)"
RUN_ID="${SCENARIO_ID}-$(date -u +%Y%m%dT%H%M%SZ)"
OUT="$EVIDENCE_DIR/${RUN_ID}-nmap.txt"
# Bounded connect scan against one exact registered CCC lab target only.
nmap -Pn -sT -p "$PORTS" --max-retries 1 --host-timeout 30s "$TARGET_IP" | tee "$OUT"
python3 - "$EVIDENCE_DIR/${RUN_ID}-trigger.json" "$RUN_ID" "$TS" "$TARGET_NAME" "$TARGET_IP" "$OUT" <<'PY'
import json,sys
path,run,ts,name,ip,out=sys.argv[1:]
json.dump({'scenario_id':'DET-01','run_id':run,'trigger_time':ts,'source_host':'CCC-KALI-RED','target_host':name,'target_ip':ip,'trigger_class':'BOUNDED_NMAP','bounded_ports':'22,80,443,2222','local_trigger_evidence':out,'synthetic':False},open(path,'w'),indent=2)
PY
echo "TRIGGER_RECORDED $RUN_ID"
