from pathlib import Path
import importlib.util

ROOT=Path(__file__).resolve().parents[2]
P=ROOT/"26_CCC_Workforce"/"coordinator"/"ledger_bridge.py"
spec=importlib.util.spec_from_file_location("ledger_bridge",P); bridge=importlib.util.module_from_spec(spec); spec.loader.exec_module(bridge)

def test_worker_event_maps_to_canonical_ledger(tmp_path):
    event={"worker_id":"security","event_id":"e1","run_id":"r1","timestamp":"2026-08-22T08:00:00Z","source":"test","task_id":"t1","organ":"soc","previous_state":"INCUBATE","current_state":"VERIFY","fact":"test passed","risk":"low","action":"record","confidence":1.0,"evidence_refs":[],"cost":0,"approval_required":False,"next_owner":"command","next_action":"review","provenance":"unit-test"}
    record=bridge.append(tmp_path/"ledger.jsonl",event)
    assert record["event_type"]=="WORKER_EVENT"
    assert record["validation"]=="WORKER_EVENT_SCHEMA_VALID"
    assert record["owner"]=="security"
