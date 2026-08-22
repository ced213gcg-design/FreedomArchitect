from datetime import datetime, timezone, timedelta

def now_iso(offset_ms=0):
    return (datetime.now(timezone.utc)+timedelta(milliseconds=offset_ms)).isoformat()

def valid_run(scenario_id='DET-01', run_id='run-1', state='PASS', evidence=True):
    return {
        'scenario_id':scenario_id,
        'run_id':run_id,
        'trigger_time':now_iso(0),
        'source_host':'CCC-KALI-RED',
        'target_host':'CCC-HONEY-TARGET',
        'trigger_class':'BOUNDED_TEST',
        'sensor':'Zeek',
        'source_event_time':now_iso(100),
        'detection_time':now_iso(200),
        'ledger_time':now_iso(300),
        'dashboard_time':now_iso(400),
        'latency_ms':400,
        'state':state,
        'evidence_refs':['sha256:abc'] if evidence else [],
        'control_gates_satisfied':['SOC-01','SOC-02','SOC-03'],
        'notes':'bounded test evidence',
        'synthetic':False,
    }

def valid_bridge(runs=None):
    return {
        'schema':'ccc.soc.evidence.bridge.v1',
        'timestamp':now_iso(),
        'source_host':'ccc-dell-compute-01',
        'run_id':'physical-run-1',
        'control_gates':[],
        'scenario_runs':runs or [],
        'vm_health':[],
        'sensor_health':[],
        'evidence_refs':[],
        'next_action':'REVIEW_EVIDENCE',
    }
