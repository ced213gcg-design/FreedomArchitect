import importlib.util, json
from pathlib import Path
M=Path(__file__).resolve().parents[1]/"backend"/"soc_adapter.py"; s=importlib.util.spec_from_file_location("soc_adapter",M); m=importlib.util.module_from_spec(s); s.loader.exec_module(m)
def test_missing_is_unknown(tmp_path): r=m.SocAdapter(tmp_path/"missing.json").get_state(); assert r["state"]=="UNKNOWN" and r["validation"]=="MISSING_SOURCE"
def test_missing_required_not_pass(tmp_path): p=tmp_path/"state.json"; p.write_text('{"status":"PASS"}'); r=m.SocAdapter(p).get_state(); assert r["state"]=="UNKNOWN"
def test_secret_fields_redacted(tmp_path):
    p=tmp_path/"state.json"; p.write_text(json.dumps({"timestamp":"2099-01-01T00:00:00Z","run_id":"r1","phase":"VERIFY","status":"VERIFY","host_health":{},"vm_health":{},"evidence":{"token":"abc"},"next_action":"x"})); r=m.SocAdapter(p).get_state(); assert r["data"]["evidence"]["token"]=="[REDACTED]"
