from pathlib import Path
import importlib.util
P=Path(__file__).resolve().parents[1]/"exception_router.py"; s=importlib.util.spec_from_file_location("exception_router",P); m=importlib.util.module_from_spec(s); s.loader.exec_module(m)
def test_router_preserves_human_authority_and_ledger():
    e={"exception_id":"ex-1","freshness_state":"VERIFIED","exception_score":{"score":88},"type":"EMPLOYMENT","risk":"LOW","approval_required":True}
    r=m.evaluate(e); assert r["target"]=="mission-control-agent" and r["ledger_required"] is True and r["human_authority_preserved"] is True
