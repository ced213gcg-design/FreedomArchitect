import importlib.util, json, sys
from pathlib import Path

ROOT=Path(__file__).resolve().parents[2]
BACK=ROOT/"19_Live_Adaptive_Dashboard"/"backend"
sys.path.insert(0,str(BACK))

spec=importlib.util.spec_from_file_location("revenue_flywheel",BACK/"revenue_flywheel.py")
mod=importlib.util.module_from_spec(spec)
spec.loader.exec_module(mod)


def flywheel():
    return mod.get_revenue_flywheel(
        ROOT/"config"/"revenue-stream-registry.yaml",
        ROOT/"22_CCC_Ledger"/"economics"/"revenue-flywheel-policy.yaml",
    )


def test_registry_has_diversified_streams():
    out=flywheel()
    assert out["stream_count"] >= 8
    assert len({s["class"] for s in out["streams"]}) >= 6
    assert len(out["class_counts"]) >= 6
    assert out["diversification_gate"]["required_views"]


def test_realized_revenue_is_not_invented():
    out=flywheel()
    assert out["realized_revenue_total"] is None
    assert out["realized_revenue_total_validation"] == "NOT_CALCULATED_WITHOUT_LEDGER_AND_REVENUE_ASSURANCE_EVIDENCE"
    assert not any(s.get("realized_revenue") for s in out["streams"] if s.get("stage") != "RECONCILED")


def test_regenerative_loop_reinjects_next_alpha():
    out=flywheel()
    assert out["closed_loop"][0] == "KNOWLEDGE"
    assert "CUSTOMER_SUCCESS" in out["closed_loop"]
    assert "CUSTOMER_LEARNING" in out["closed_loop"]
    assert out["closed_loop"][-1] == "NEXT_ALPHA"
    assert out["recurring_customer_cycle"][-1] == "IMPROVE_OFFER"
    assert out["customer_success_gate"]["required_fields"]
    assert out["surplus_gate"]["automatic_money_movement"] is False
    assert out["surplus_gate"]["human_approval_required"] is True


def test_dashboard_endpoint_exposes_evidence_gate():
    app_spec=importlib.util.spec_from_file_location("ccc_app",BACK/"app.py")
    app=importlib.util.module_from_spec(app_spec)
    app_spec.loader.exec_module(app)
    status,_,body=app.route_request("GET","/api/economics/revenue-flywheel")
    payload=json.loads(body)
    assert status == 200
    assert payload["state"] == "VERIFY"
    assert payload["policy_version"] == 2
    assert payload["customer_success_gate"]["rule"]
    assert payload["diversification_gate"]["rule"]
    assert payload["validation"] == "DECLARED_REGISTRY_AND_POLICY_NOT_FINANCIAL_SETTLEMENT"
