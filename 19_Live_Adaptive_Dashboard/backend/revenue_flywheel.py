from __future__ import annotations
from collections import Counter
from pathlib import Path
import yaml


def load_yaml(path: Path):
    return yaml.safe_load(Path(path).read_text(encoding="utf-8")) or {}


def get_revenue_flywheel(registry_path: Path, policy_path: Path):
    registry = load_yaml(registry_path)
    policy = load_yaml(policy_path)
    streams = registry.get("streams", []) or []
    stage_counts = Counter(s.get("stage", "UNKNOWN") for s in streams)
    class_counts = Counter(s.get("class", "UNKNOWN") for s in streams)

    realized_candidates = [
        s for s in streams
        if s.get("stage") == "RECONCILED" and s.get("realized_revenue") is True
    ]

    return {
        "state": "VERIFY",
        "policy_version": policy.get("version"),
        "principle": policy.get("principle"),
        "closed_loop": policy.get("closed_loop", []),
        "recurring_customer_cycle": policy.get("recurring_customer_cycle", []),
        "stream_count": len(streams),
        "stage_counts": dict(sorted(stage_counts.items())),
        "class_counts": dict(sorted(class_counts.items())),
        "streams": streams,
        "realized_revenue_status": (
            "EVIDENCE_PRESENT_REQUIRES_LEDGER_RECONCILIATION"
            if realized_candidates
            else "NO_RECONCILED_REALIZED_REVENUE_IN_REGISTRY"
        ),
        "realized_revenue_total": None,
        "realized_revenue_total_validation": "NOT_CALCULATED_WITHOUT_LEDGER_AND_REVENUE_ASSURANCE_EVIDENCE",
        "customer_success_gate": policy.get("customer_success_gate", {}),
        "surplus_gate": policy.get("surplus_gate", {}),
        "allocation_gate": policy.get("allocation_gate", {}),
        "diversification_gate": policy.get("diversification_gate", {}),
        "branch_result_gate": policy.get("branch_result_gate", {}),
        "portfolio_metrics": policy.get("portfolio_metrics", []),
        "control_boundaries": policy.get("control_boundaries", []),
        "validation": "DECLARED_REGISTRY_AND_POLICY_NOT_FINANCIAL_SETTLEMENT",
    }
