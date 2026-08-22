#!/usr/bin/env bash
set -Eeuo pipefail
SCENARIO_ID="DET-03"
TARGET_IP="${CCC_COWRIE_TARGET_IP:-10.69.69.30}"
PORT="${CCC_COWRIE_PORT:-2222}"
EVIDENCE_DIR="${CCC_TRIGGER_EVIDENCE_DIR:-$HOME/ccc-trigger-evidence}"
mkdir -p "$EVIDENCE_DIR"
echo "$SCENARIO_ID COWRIE INTERACTION"
[[ "$PORT" =~ ^(22|2222)$ ]] || { echo "REJECTED_COWRIE_PORT_NOT_BOUNDED" >&2; exit 2; }
TARGET_NAME="$(python3 "$(dirname "$0")/ccc_lab_guard.py" --ip "$TARGET_IP" --role honeypot_target --port "$PORT")"
command -v sshpass >/dev/null || { echo "HOLD_MISSING_SSHPASS" >&2; exit 5; }
TS="$(date -u +%Y-%m-%dT%H:%M:%SZ)"
RUN_ID="${SCENARIO_ID}-$(date -u +%Y%m%dT%H%M%SZ)"
OUT="$EVIDENCE_DIR/${RUN_ID}-cowrie.txt"
: > "$OUT"
for attempt in 1 2 3 4 5; do
  echo "interaction=$attempt" | tee -a "$OUT"
  sshpass -p 'CCC_DET03_FIXED_DUMMY_PASSWORD' ssh -p "$PORT" \
    -o PreferredAuthentications=password -o PubkeyAuthentication=no \
    -o StrictHostKeyChecking=no -o UserKnownHostsFile=/dev/null \
    -o ConnectTimeout=5 -o NumberOfPasswordPrompts=1 \
    ccc-det03-dummy@"$TARGET_IP" 'echo CCC_DET03_BENIGN_INTERACTION; exit' >>"$OUT" 2>&1 || true
done
python3 - "$EVIDENCE_DIR/${RUN_ID}-trigger.json" "$RUN_ID" "$TS" "$TARGET_NAME" "$TARGET_IP" "$PORT" "$OUT" <<'PY'
import json,sys
path,run,ts,name,ip,port,out=sys.argv[1:]
json.dump({'scenario_id':'DET-03','run_id':run,'trigger_time':ts,'source_host':'CCC-KALI-RED','target_host':name,'target_ip':ip,'target_port':int(port),'trigger_class':'BOUNDED_COWRIE_SSH','interaction_count':5,'local_trigger_evidence':out,'synthetic':False},open(path,'w'),indent=2)
PY
echo "TRIGGER_RECORDED $RUN_ID"
