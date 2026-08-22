from __future__ import annotations
from datetime import datetime,timezone
from pathlib import Path
import yaml

DEFAULT_POLICY={"verified_max_hours":24,"aging_max_hours":72,"stale_archive_after_hours":168}

def _dt(value):
    if isinstance(value,datetime): dt=value
    else: dt=datetime.fromisoformat(str(value).replace("Z","+00:00"))
    if dt.tzinfo is None: dt=dt.replace(tzinfo=timezone.utc)
    return dt.astimezone(timezone.utc)

def load_policy(path=None):
    if not path: return {"default":dict(DEFAULT_POLICY),"types":{}}
    data=yaml.safe_load(Path(path).read_text(encoding="utf-8")) or {}
    return data.get("freshness",{"default":dict(DEFAULT_POLICY),"types":{}})

def evaluate_freshness(exception:dict,policy:dict|None=None,now=None)->dict:
    current=str(exception.get("freshness_state") or "").upper()
    if current in {"CLOSED","SUPERSEDED"}: return {"freshness_state":current,"age_hours":None,"archive_recommended":True,"reason":"terminal_state"}
    last=exception.get("last_verified")
    if not last: return {"freshness_state":"STALE","age_hours":None,"archive_recommended":True,"reason":"missing_last_verified"}
    now=_dt(now or datetime.now(timezone.utc)); age=max(0.0,(now-_dt(last)).total_seconds()/3600.0)
    policy=policy or {"default":dict(DEFAULT_POLICY),"types":{}}; p=dict(policy.get("default") or DEFAULT_POLICY); p.update((policy.get("types") or {}).get(exception.get("type"),{}) or {})
    verified=float(p.get("verified_max_hours",24)); aging=float(p.get("aging_max_hours",72)); archive=float(p.get("stale_archive_after_hours",168))
    state="VERIFIED" if age<=verified else "AGING" if age<=aging else "STALE"
    return {"freshness_state":state,"age_hours":round(age,2),"archive_recommended":age>archive,"reason":"age_policy","policy":{"verified_max_hours":verified,"aging_max_hours":aging,"stale_archive_after_hours":archive}}
