from pathlib import Path
import importlib.util

def load_module(name):
    p = Path(__file__).resolve().parents[1] / "coordinator" / f"{name}.py"
    spec = importlib.util.spec_from_file_location(name, p); mod = importlib.util.module_from_spec(spec); spec.loader.exec_module(mod); return mod

def test_code_failure_routes_security_first():
    r = load_module("dispatcher").route("CODE_CI_FAILURE")
    assert r["primary"] == "security"
    assert "command" in r["secondary"]

def test_unknown_route_goes_to_command_triage_not_execution():
    r = load_module("dispatcher").route("ALIEN_EVENT")
    assert r["status"] == "UNROUTED"
    assert r["next_owner"] == "command"
