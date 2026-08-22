from pathlib import Path
import importlib.util,json,os
BACKEND=Path(__file__).resolve().parents[1]/"backend"; spec=importlib.util.spec_from_file_location("ccc_app_v101",BACKEND/"app.py"); app=importlib.util.module_from_spec(spec); spec.loader.exec_module(app)
def test_exception_endpoints_return_honest_empty_when_source_missing(tmp_path,monkeypatch):
    monkeypatch.setenv("CCC_EXCEPTION_PATH",str(tmp_path/"missing.jsonl")); status,_,body=app.route_request("GET","/api/exceptions"); data=json.loads(body); assert status==200 and data["source_state"]=="UNAVAILABLE" and data["count"]==0
    status,_,body=app.route_request("GET","/api/exceptions/high-priority"); assert status==200 and json.loads(body)["count"]==0
