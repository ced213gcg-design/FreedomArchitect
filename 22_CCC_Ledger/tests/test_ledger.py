import importlib.util
from pathlib import Path
HERE=Path(__file__).resolve(); MOD=HERE.parents[1]/"ledger.py"
spec=importlib.util.spec_from_file_location("ccc_ledger", MOD); m=importlib.util.module_from_spec(spec); spec.loader.exec_module(m)

def event(i, synthetic=False):
    return {"event_id":f"e{i}","timestamp":"2026-08-22T00:00:00Z","source":"test","owner":"test","organ":"ledger","run_id":"r1","event_type":"TEST","previous_state":"BUILD","new_state":"VERIFY","change":f"change-{i}","validation":"PASS","provenance":"unit-test","artifact_hashes":[],"synthetic":synthetic,"financial_classification":"NON_FINANCIAL","notes":"test"}

def test_append_and_verify(tmp_path):
    p=tmp_path/"ledger.jsonl"; a=m.append_event(p,event(1)); b=m.append_event(p,event(2))
    assert b["previous_event_hash"]==a["event_hash"]
    assert m.verify_chain(p)["ok"] is True

def test_tamper_detected(tmp_path):
    p=tmp_path/"ledger.jsonl"; m.append_event(p,event(1)); text=p.read_text(); p.write_text(text.replace("change-1","tampered"))
    assert m.verify_chain(p)["ok"] is False

def test_synthetic_is_explicit(tmp_path):
    p=tmp_path/"ledger.jsonl"; r=m.append_event(p,event(1,True)); assert r["synthetic"] is True
