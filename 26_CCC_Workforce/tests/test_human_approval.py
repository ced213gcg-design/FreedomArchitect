from pathlib import Path
import yaml

ROOT=Path(__file__).resolve().parents[1]

def test_consequential_actions_are_approval_gated():
    a=yaml.safe_load((ROOT/"authority.yaml").read_text(encoding="utf-8"))
    needed={"money_movement","purchase","binding_contract","external_job_application_submission","customer_production_change","protected_branch_merge_or_release","critical_iam_or_network_policy_change","malware_execution","canonical_data_deletion","public_publication","legally_consequential_communication"}
    assert needed.issubset(set(a["approval_required"]))
