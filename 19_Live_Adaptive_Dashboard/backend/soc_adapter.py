from pathlib import Path
from datetime import datetime, timezone
import json, os
REQUIRED=("timestamp","run_id","phase","status","host_health","vm_health","evidence","next_action")
SENSITIVE=("password","secret","token","private_key","credential")
class SocAdapter:
    def __init__(self,path=None,stale_seconds=300): self.path=Path(path or os.getenv("CCC_SOC_STATE_PATH", r"C:\CCC\State\ccc-soc-live-state.json")); self.stale_seconds=stale_seconds; self.last_valid_run_id=None
    def _redact(self,obj):
        if isinstance(obj,dict): return {k:("[REDACTED]" if any(s in k.lower() for s in SENSITIVE) else self._redact(v)) for k,v in obj.items()}
        if isinstance(obj,list): return [self._redact(v) for v in obj]
        return obj
    def get_state(self):
        base={"state":"UNKNOWN","connected":False,"stale":True,"source":str(self.path),"last_valid_run_id":self.last_valid_run_id}
        if not self.path.exists(): return {**base,"validation":"MISSING_SOURCE","next_action":"VERIFY_DELL_SOC_STATE_SOURCE"}
        try: data=json.loads(self.path.read_text(encoding="utf-8"))
        except Exception as exc: return {**base,"validation":"INVALID_JSON","error":str(exc),"next_action":"REPAIR_SOC_STATE_JSON"}
        missing=[k for k in REQUIRED if k not in data]
        if missing: return {**base,"connected":True,"validation":"MISSING_REQUIRED_FIELDS","missing":missing,"next_action":"REPAIR_SOC_STATE_CONTRACT"}
        stale=True
        try:
            ts=datetime.fromisoformat(str(data["timestamp"]).replace("Z","+00:00")); stale=(datetime.now(timezone.utc)-ts.astimezone(timezone.utc)).total_seconds()>self.stale_seconds
        except Exception: pass
        self.last_valid_run_id=data.get("run_id") or self.last_valid_run_id
        state="VERIFY" if stale else str(data.get("status","VERIFY")).upper()
        if state=="PASS": state="VERIFY"
        clean=self._redact(data)
        return {"state":state,"connected":True,"stale":stale,"validation":"VALID_CONTRACT_STALE" if stale else "VALID_CONTRACT","last_valid_run_id":self.last_valid_run_id,"data":clean,"source":str(self.path)}
