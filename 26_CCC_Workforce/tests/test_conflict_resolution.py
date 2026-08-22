from pathlib import Path
import importlib.util

P = Path(__file__).resolve().parents[1] / "coordinator" / "conflict.py"
spec=importlib.util.spec_from_file_location("conflict",P); conflict=importlib.util.module_from_spec(spec); spec.loader.exec_module(conflict)

def test_verified_ledger_beats_worker_analysis():
    out=conflict.resolve_claims([
        {"authority_level":"WORKER_ANALYSIS","fact":"A"},
        {"authority_level":"VERIFIED_LEDGER_LIVE_EVIDENCE","fact":"B"},
    ])
    assert out["winner"]["fact"] == "B"

def test_equal_authority_disagreement_is_visible_deadlock():
    out=conflict.resolve_claims([
        {"authority_level":"WORKER_ANALYSIS","fact":"A"},
        {"authority_level":"WORKER_ANALYSIS","fact":"B"},
    ])
    assert out["deadlock"] is True
    assert out["human_decision_required"] is True
