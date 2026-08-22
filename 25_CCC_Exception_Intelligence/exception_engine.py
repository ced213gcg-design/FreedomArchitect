from __future__ import annotations
from copy import deepcopy
from .verifier import verify_exception
from .freshness import evaluate_freshness
from .fit_score import employment_fit,calculate_fit

WEIGHTS={"strategic_value":0.35,"time_sensitivity":0.20,"probability":0.15,"economic_upside":0.10,"capability_alignment":0.10,"confidence":0.05,"reinjection_value":0.05}

def exception_score(exception:dict)->dict:
    components={}; total=0.0
    for field,weight in WEIGHTS.items():
        value=float(exception.get(field,0))
        if value<0 or value>100: raise ValueError(f"{field} must be 0..100")
        components[field]={"value":value,"weight":weight,"weighted":round(value*weight,4)}; total+=value*weight
    score=round(total,2)
    classification="CRITICAL OPPORTUNITY" if score>=90 else "HIGH PRIORITY" if score>=80 else "QUALIFIED" if score>=70 else "WATCH" if score>=50 else "ARCHIVE / IGNORE"
    return {"score":score,"classification":classification,"formula":"strategic_value*0.35 + time_sensitivity*0.20 + probability*0.15 + economic_upside*0.10 + capability_alignment*0.10 + confidence*0.05 + reinjection_value*0.05","components":components}

def enrich_exception(exception:dict,freshness_policy=None,now=None,fit_components=None)->dict:
    out=deepcopy(exception); out.update(evaluate_freshness(out,freshness_policy,now=now))
    components=fit_components or out.get("fit_components") or {}
    out["fit_score"]=employment_fit(components) if out.get("type")=="EMPLOYMENT" else calculate_fit(components)
    out["exception_score"]=exception_score(out); out["verification"]=verify_exception(out)
    if not out["verification"]["ok"]: out["state"]="HOLD"
    return out
