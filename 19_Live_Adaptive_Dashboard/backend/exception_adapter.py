from __future__ import annotations
from pathlib import Path
import importlib,json,os,yaml

ROOT=Path(__file__).resolve().parents[2]
engine=importlib.import_module("25_CCC_Exception_Intelligence.exception_engine")
freshness=importlib.import_module("25_CCC_Exception_Intelligence.freshness")
routing=importlib.import_module("25_CCC_Exception_Intelligence.routing")
DEFAULT_PATH=ROOT/"runtime"/"ccc-exceptions.jsonl"
DEFAULT_POLICY=ROOT/"config"/"exception-policy.yaml"

def _read_jsonl(path:Path):
    rows=[]; defects=[]
    if not path.exists(): return rows,["source_unavailable"]
    for n,line in enumerate(path.read_text(encoding="utf-8").splitlines(),1):
        if not line.strip(): continue
        try:
            value=json.loads(line)
            if not isinstance(value,dict): raise ValueError("record_not_object")
            rows.append(value)
        except Exception as exc: defects.append(f"line_{n}:{exc}")
    return rows,defects

def _policy(path:Path):
    if not path.exists(): return {"freshness":{"default":freshness.DEFAULT_POLICY,"types":{}},"privacy":{"public_exception_fields":[]}}
    return yaml.safe_load(path.read_text(encoding="utf-8")) or {}

def _safe(exception:dict,public_fields:list[str])->dict:
    out={k:exception.get(k) for k in public_fields if k in exception}; out["evidence_refs"]=list(exception.get("evidence_refs") or []); out["route"]=exception.get("route"); out["game_theory"]=exception.get("game_theory","PENDING_EVALUATION"); out["capability_gap"]=exception.get("capability_gap","NOT_DECLARED"); out["approval_state"]="REQUIRED" if exception.get("approval_required") else "NOT_REQUIRED"; return out

def get_exceptions(path=None,policy_path=None,now=None)->dict:
    path=Path(path or os.getenv("CCC_EXCEPTION_PATH",DEFAULT_PATH)); policy_path=Path(policy_path or os.getenv("CCC_EXCEPTION_POLICY",DEFAULT_POLICY)); p=_policy(policy_path); rows,defects=_read_jsonl(path)
    fields=(p.get("privacy") or {}).get("public_exception_fields") or ["exception_id","type","title","source","last_verified","freshness_state","confidence","strategic_value","exception_score","fit_score","risk","owner","next_action","approval_required","state"]
    enriched=[]
    for row in rows:
        item=engine.enrich_exception(row,p.get("freshness") or {},now=now); item["route"]=routing.route_exception(item); enriched.append(_safe(item,fields))
    material=[d for d in defects if d!="source_unavailable"]
    return {"state":"VERIFY" if not material else "HOLD","source_state":"UNAVAILABLE" if "source_unavailable" in defects else "AVAILABLE","count":len(enriched),"exceptions":enriched,"defects":defects,"validation":"EVIDENCE_BOUND_EXCEPTION_ADAPTER"}

def get_high_priority(path=None,policy_path=None,now=None)->dict:
    data=get_exceptions(path,policy_path,now)
    def score(item): return float((item.get("exception_score") or {}).get("score",0))
    current=[e for e in data["exceptions"] if e.get("freshness_state")=="VERIFIED" and score(e)>=80 and e.get("state")!="HOLD"]
    current.sort(key=score,reverse=True)
    return {"state":data["state"],"source_state":data["source_state"],"count":len(current),"exceptions":current,"validation":"VERIFIED_AND_SCORE_GTE_80_ONLY","defects":data["defects"]}
