from __future__ import annotations

def route_exception(exception:dict)->dict:
    freshness=exception.get("freshness_state"); score=float((exception.get("exception_score") or {}).get("score",0)); typ=exception.get("type","OTHER"); risk=str(exception.get("risk","")).upper(); approval=bool(exception.get("approval_required",False))
    if freshness in {"CLOSED","SUPERSEDED","STALE"}: return {"target":"exception-intelligence-agent","queue":"HOLD","reason":"not_current","approval_required":approval}
    if typ in {"SECURITY","CVE","GITHUB_FAILURE","INFRASTRUCTURE"} and risk in {"CRITICAL","HIGH"}: return {"target":"mission-control-agent","queue":"SECURITY_PRIORITY","reason":"risk_override","approval_required":True}
    if score>=80: return {"target":"mission-control-agent","queue":"HIGH_PRIORITY","reason":"exception_score","approval_required":approval}
    if score>=70: return {"target":"orchestra-agent","queue":"QUALIFIED","reason":"exception_score","approval_required":approval}
    if score>=50: return {"target":"exception-intelligence-agent","queue":"WATCH","reason":"exception_score","approval_required":False}
    return {"target":"exception-intelligence-agent","queue":"ARCHIVE","reason":"exception_score","approval_required":False}
