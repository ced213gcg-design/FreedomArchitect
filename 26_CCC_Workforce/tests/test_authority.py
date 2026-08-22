from pathlib import Path
import yaml

ROOT = Path(__file__).resolve().parents[1]

def test_default_deny_and_human_final():
    a = yaml.safe_load((ROOT / "authority.yaml").read_text(encoding="utf-8"))
    assert a["default"] == "deny"
    assert a["human_authority_final"] is True
    assert "money_movement" in a["approval_required"]
    assert "protected_branch_merge_or_release" in a["approval_required"]

def test_workers_do_not_receive_forbidden_universal_power():
    a = yaml.safe_load((ROOT / "authority.yaml").read_text(encoding="utf-8"))
    assert "move_money" in a["workers"]["command"]["deny"]
    assert "move_money" in a["workers"]["revenue"]["deny"]
    assert "human_approval_bypass" in a["workers"]["security"]["deny"]
    assert "make_slack_truth_source" in a["workers"]["communications"]["deny"]
