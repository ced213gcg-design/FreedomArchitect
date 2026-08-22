from pathlib import Path
import importlib.util

P=Path(__file__).resolve().parents[1]/"coordinator"/"health.py"
spec=importlib.util.spec_from_file_location("health",P); health=importlib.util.module_from_spec(spec); spec.loader.exec_module(health)

def test_every_worker_has_offline_fallback():
    for worker in ["command","intelligence","security","revenue","communications"]:
        out=health.fallback_for(worker,False)
        assert out["fallback_active"] is True
        assert out["behavior"]

def test_security_outage_defaults_consequential_actions_hold():
    out=health.fallback_for("security",False)
    assert "HOLD" in out["behavior"]
