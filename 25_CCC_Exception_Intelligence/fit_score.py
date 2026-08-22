from __future__ import annotations

EMPLOYMENT_WEIGHTS={"Education":10,"Project Experience":20,"Technical Match":25,"Role Competencies":15,"Domain Match":10,"Location / Work Model":10,"Evidence Strength":10}

def _bounded(value):
    value=float(value)
    if value<0 or value>100: raise ValueError("score components must be between 0 and 100")
    return value

def calculate_fit(components:dict,weights:dict|None=None)->dict:
    if not isinstance(components,dict) or not components:
        return {"score":0.0,"components":[],"validation":"NO_COMPONENT_EVIDENCE","missing_evidence_components":[]}
    weights=weights or {name:1 for name in components}
    rows=[]; numerator=0.0; denominator=0.0
    for name,weight in weights.items():
        raw=components.get(name,{}) or {}; score=_bounded(raw.get("score",0)); evidence=list(raw.get("evidence_refs") or []); effective=score if evidence else 0.0; w=float(weight)
        numerator+=effective*w; denominator+=w
        rows.append({"name":name,"score":score,"effective_score":effective,"weight":w,"evidence_refs":evidence,"evidence_present":bool(evidence)})
    final=round(numerator/denominator,2) if denominator else 0.0
    return {"score":final,"components":rows,"validation":"EVIDENCE_BOUND","missing_evidence_components":[r["name"] for r in rows if not r["evidence_present"]]}

def employment_fit(components:dict)->dict: return calculate_fit(components,EMPLOYMENT_WEIGHTS)
