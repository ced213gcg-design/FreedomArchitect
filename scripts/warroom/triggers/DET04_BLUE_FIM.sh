#!/usr/bin/env bash
set -Eeuo pipefail
SCENARIO_ID="DET-04"
EVIDENCE_DIR="${CCC_TRIGGER_EVIDENCE_DIR:-$HOME/ccc-trigger-evidence}"
WAZUH_CONFIG="${CCC_WAZUH_CONFIG:-/var/ossec/etc/ossec.conf}"
mkdir -p "$EVIDENCE_DIR"
echo "$SCENARIO_ID FILE INTEGRITY CHANGE"
python3 "$(dirname "$0")/ccc_local_guard.py" --name CCC-SOC-BLUE --role defensive_monitoring_sensor >/dev/null
[[ -r "$WAZUH_CONFIG" ]] || { echo "HOLD_MISSING_MONITORED_PATH: Wazuh syscheck configuration not readable at $WAZUH_CONFIG" >&2; exit 6; }
MONITORED_PATH="$(python3 - "$WAZUH_CONFIG" <<'PY'
import os,sys,xml.etree.ElementTree as ET
path=sys.argv[1]
try: root=ET.parse(path).getroot()
except Exception: raise SystemExit(2)
for node in root.iter('directories'):
    text=(node.text or '').strip()
    for raw in text.split(','):
        p=os.path.expandvars(os.path.expanduser(raw.strip()))
        if p and os.path.isdir(p) and os.access(p,os.W_OK):
            print(p); raise SystemExit(0)
raise SystemExit(3)
PY
)" || { echo "HOLD_MISSING_MONITORED_PATH: no actual Wazuh/syscheck monitored writable directory was confirmed." >&2; exit 7; }
TS="$(date -u +%Y-%m-%dT%H:%M:%SZ)"
RUN_ID="${SCENARIO_ID}-$(date -u +%Y%m%dT%H%M%SZ)"
TEST_FILE="$MONITORED_PATH/.ccc_det04_${RUN_ID}.txt"
OUT="$EVIDENCE_DIR/${RUN_ID}-fim-trigger.txt"
echo "monitored_path=$MONITORED_PATH" | tee "$OUT"
printf 'CCC DET-04 create %s\n' "$TS" > "$TEST_FILE"
sleep 1
printf 'CCC DET-04 modify %s\n' "$(date -u +%Y-%m-%dT%H:%M:%SZ)" >> "$TEST_FILE"
sleep 1
rm -f "$TEST_FILE"
echo "create_modify_delete=complete" | tee -a "$OUT"
python3 - "$EVIDENCE_DIR/${RUN_ID}-trigger.json" "$RUN_ID" "$TS" "$MONITORED_PATH" "$OUT" <<'PY'
import json,sys
path,run,ts,monitored,out=sys.argv[1:]
json.dump({'scenario_id':'DET-04','run_id':run,'trigger_time':ts,'source_host':'CCC-SOC-BLUE','target_host':'CCC-SOC-BLUE','trigger_class':'DISPOSABLE_FIM_FILE','monitored_path':monitored,'operation_sequence':['create','modify','delete'],'local_trigger_evidence':out,'synthetic':False},open(path,'w'),indent=2)
PY
echo "TRIGGER_RECORDED $RUN_ID"
