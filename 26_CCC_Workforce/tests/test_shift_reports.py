from pathlib import Path
import json, yaml
from jsonschema import validate, ValidationError

ROOT = Path(__file__).resolve().parents[1]
SCHEMA = json.loads((ROOT / "schemas" / "shift-report.schema.json").read_text(encoding="utf-8"))

def test_exactly_two_formal_reports_policy():
    policy = yaml.safe_load((ROOT / "shift-policy.yaml").read_text(encoding="utf-8"))
    assert policy["formal_reports_per_shift"] == 2
    assert set(policy["formal_report_types"]) == {"MID_SHIFT_POSITION", "END_SHIFT_HANDOFF"}

def test_end_shift_requires_next_owner_and_action():
    report = {"shift_id":"s1","worker":"command","report_type":"END_SHIFT_HANDOFF","ended_at":"2026-08-22T04:00:00-05:00","starting_position":"x","completed_outcomes":[],"evidence":[],"unresolved_items":[],"final_state":"INCUBATE","where_work_stopped":"gate","next_owner":"security","exact_next_action":"verify runtime","expected_next_evidence":"test result","lessons_reinjection":[],"cost_summary":0}
    validate(report, SCHEMA)
    broken = dict(report); broken.pop("next_owner")
    try:
        validate(broken, SCHEMA)
        assert False, "missing next_owner must fail"
    except ValidationError:
        pass
