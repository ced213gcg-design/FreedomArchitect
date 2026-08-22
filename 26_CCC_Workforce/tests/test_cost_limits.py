from pathlib import Path
import yaml

ROOT=Path(__file__).resolve().parents[1]

def test_model_router_prohibits_unbounded_loops_and_tracks_cost():
    d=yaml.safe_load((ROOT/"model-routing.yaml").read_text(encoding="utf-8"))
    assert d["unbounded_autonomous_loops"] is False
    required={"model_provider","input_cost","output_cost","tool_cost","run_id","worker","task","useful_outcome"}
    assert required.issubset(set(d["cost_accounting_required"]))
    assert d["rules"]["highest_cost_for_every_task"] is False
