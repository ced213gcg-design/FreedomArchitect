from pathlib import Path
from datetime import datetime, timezone
import json, os
from evidence_bridge import validate_sanitized_payload, normalize_live_state

REQUIRED=("timestamp","run_id","phase","status","host_health","vm_health","evidence","next_action")
SENSITIVE=("password","secret","token","private_key","credential")

class SocAdapter:
    def __init__(self,path=None,stale_seconds=300):
        self.path=Path(path or os.getenv("CCC_SOC_STATE_PATH", r"C:\CCC\State\ccc-soc-live-state.json"))
        self.bridge_path=Path(os.getenv("CCC_BRIDGE_PAYLOAD_PATH", str(self.path.with_name("ccc-soc-bridge-payload.json"))))
        self.stale_seconds=stale_seconds
        self.last_valid_run_id=None
    def _redact(self,obj):
        if isinstance(obj,dict): return {k:("[REDACTED]" if any(s in k.lower() for s in SENSITIVE) else self._redact(v)) for k,v in obj.items()}
        if isinstance(obj,list): return [self._redact(v) for v in obj]
        return obj
    def _load(self):
        if self.path.exists():
            return json.loads(self.path.read_text(encoding="utf-8")), self.path, "STATE_FILE"
        if self.bridge_path.exists():
            payload=json.loads(self.bridge_path.read_text(encoding="utf-8"))
            errors=validate_sanitized_payload(payload)
            if errors: raise ValueError("INVALID_FILE_FALLBACK:"+";".join(errors))
            return normalize_live_state(payload,"FILE_FALLBACK"), self.bridge_path, "FILE_FALLBACK"
        return None, self.path, "MISSING"
    def get_state(self):
        base={"state":"UNKNOWN","connected":False,"stale":True,"source":str(self.path),"last_valid_run_id":self.last_valid_run_id}
        try:
            data,source,mode=self._load()
        except Exception as exc:
            return {**base,"connected":True,"validation":"INVALID_SANITIZED_FILE_FALLBACK","error":str(exc),"bridge_mode":"FILE_FALLBACK","next_action":"REPAIR_OR_RETRANSFER_SANITIZED_BRIDGE_PAYLOAD"}
        if data is None:
            return {**base,"validation":"MISSING_SOURCE","bridge_mode":os.getenv("CCC_BRIDGE_MODE","FILE_FALLBACK"),"next_action":"VERIFY_DELL_SOC_STATE_OR_SANITIZED_FILE_FALLBACK"}
        missing=[k for k in REQUIRED if k not in data]
        if missing: return {**base,"connected":True,"source":str(source),"validation":"MISSING_REQUIRED_FIELDS","missing":missing,"bridge_mode":mode,"next_action":"REPAIR_SOC_STATE_CONTRACT"}
        stale=True
        try:
            ts=datetime.fromisoformat(str(data["timestamp"]).replace("Z","+00:00")); stale=(datetime.now(timezone.utc)-ts.astimezone(timezone.utc)).total_seconds()>self.stale_seconds
        except Exception: pass
        self.last_valid_run_id=data.get("run_id") or self.last_valid_run_id
        state="VERIFY" if stale else str(data.get("status","VERIFY")).upper()
        if state=="PASS": state="VERIFY"
        clean=self._redact(data)
        validation=("VALID_FILE_FALLBACK_STALE" if stale else "VALID_FILE_FALLBACK") if mode=="FILE_FALLBACK" else ("VALID_CONTRACT_STALE" if stale else "VALID_CONTRACT")
        return {"state":state,"connected":True,"stale":stale,"validation":validation,"bridge_mode":mode,"last_valid_run_id":self.last_valid_run_id,"data":clean,"source":str(source)}
