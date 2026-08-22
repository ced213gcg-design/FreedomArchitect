from __future__ import annotations

ALLOWED_TYPES={"EMPLOYMENT","FEDERAL_OPPORTUNITY","CUSTOMER_LEAD","GRANT","SECURITY","CVE","GITHUB_FAILURE","HARDWARE_PRICE","MARKET","RESEARCH","REGULATORY","FINANCIAL","INFRASTRUCTURE","CAPABILITY_GAP","OTHER"}
REQUIRED={"exception_id","type","title","source","first_seen","last_verified","confidence","strategic_value","time_sensitivity","probability","economic_upside","capability_alignment","reinjection_value","risk","owner","next_action","approval_required","state","evidence_refs","freshness_state","fit_score","exception_score"}
NUMERIC={"confidence","strategic_value","time_sensitivity","probability","economic_upside","capability_alignment","reinjection_value"}

def verify_exception(exception:dict)->dict:
    defects=[]; missing=sorted(REQUIRED-set(exception))
    if missing: defects.append("missing:"+",".join(missing))
    if exception.get("type") not in ALLOWED_TYPES: defects.append("unsupported_type")
    for key in NUMERIC:
        if key in exception:
            try: value=float(exception[key])
            except Exception: defects.append(f"non_numeric:{key}"); continue
            if not 0<=value<=100: defects.append(f"out_of_range:{key}")
    if not str(exception.get("source","")).strip(): defects.append("missing_source")
    evidence=exception.get("evidence_refs")
    if not isinstance(evidence,list): defects.append("evidence_refs_not_list")
    if exception.get("freshness_state")=="VERIFIED" and not evidence: defects.append("verified_without_evidence")
    return {"ok":not defects,"defects":defects,"state":"VERIFY" if not defects else "HOLD"}
