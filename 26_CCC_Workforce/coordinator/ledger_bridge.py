from pathlib import Path
import importlib.util, json
from jsonschema import validate

ROOT = Path(__file__).resolve().parents[2]
WORKFORCE = ROOT / "26_CCC_Workforce"

def _load_ledger():
    path = ROOT / "22_CCC_Ledger" / "ledger.py"
    spec = importlib.util.spec_from_file_location("ccc_ledger_for_workforce", path)
    mod = importlib.util.module_from_spec(spec); spec.loader.exec_module(mod); return mod

def validate_worker_event(event: dict):
    schema = json.loads((WORKFORCE / "schemas" / "worker-event.schema.json").read_text(encoding="utf-8"))
    validate(event, schema)
    return True

def to_ledger_event(event: dict):
    validate_worker_event(event)
    return {
        "event_id": event["event_id"],
        "timestamp": event["timestamp"],
        "source": event["source"],
        "owner": event["worker_id"],
        "organ": event["organ"],
        "run_id": event["run_id"],
        "event_type": "WORKER_EVENT",
        "previous_state": event["previous_state"],
        "new_state": event["current_state"],
        "change": {"task_id": event["task_id"], "fact": event["fact"], "risk": event["risk"], "action": event["action"], "next_owner": event["next_owner"], "next_action": event["next_action"], "confidence": event["confidence"], "cost": event["cost"], "approval_required": event["approval_required"]},
        "validation": "WORKER_EVENT_SCHEMA_VALID",
        "provenance": event["provenance"],
        "artifact_hashes": event["evidence_refs"],
        "synthetic": False,
        "financial_classification": "WORKFORCE_COST" if event["cost"] else "NON_FINANCIAL",
        "notes": "CCC Workforce event bridged into canonical Ledger without changing source authority."
    }

def append(path, event: dict):
    ledger = _load_ledger()
    return ledger.append_event(path, to_ledger_event(event))
