import importlib.util,json,os,sys
from pathlib import Path
ROOT=Path(__file__).resolve().parents[2]; BACK=ROOT/"19_Live_Adaptive_Dashboard"/"backend"; sys.path.insert(0,str(BACK)); s=importlib.util.spec_from_file_location("ccc_app_action",BACK/"app.py"); app=importlib.util.module_from_spec(s); s.loader.exec_module(app)
def test_unknown_action_rejected(tmp_path,monkeypatch): monkeypatch.setenv("CCC_LEDGER_PATH",str(tmp_path/"l.jsonl")); status,_,b=app.route_request("POST","/api/action-request",{"action_type":"DO_ANYTHING"}); assert status==400
def test_proceed_is_pending_not_executed(tmp_path,monkeypatch): monkeypatch.setenv("CCC_LEDGER_PATH",str(tmp_path/"l.jsonl")); status,_,b=app.route_request("POST","/api/action-request",{"action_type":"PROCEED_REQUEST","requester":"dashboard-agent","payload":{}}); d=json.loads(b); assert status==202 and d["state"]=="pending_approval" and d["executed"] is False
def test_unregistered_requester_rejected(tmp_path,monkeypatch):
    monkeypatch.setenv("CCC_LEDGER_PATH",str(tmp_path/"l.jsonl"))
    status,_,b=app.route_request("POST","/api/action-request",{"action_type":"PROCEED_REQUEST","requester":"unknown-agent","payload":{}})
    assert status==403
