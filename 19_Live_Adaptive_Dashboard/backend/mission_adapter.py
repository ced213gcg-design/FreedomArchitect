from pathlib import Path
def read_legacy_env(path):
    p=Path(path)
    if not p.exists(): return {"state":"UNKNOWN","source":str(p),"validation":"MISSING_LEGACY_SOURCE"}
    data={}
    for line in p.read_text(encoding="utf-8").splitlines():
        line=line.strip()
        if not line or line.startswith("#") or "=" not in line: continue
        k,v=line.split("=",1); data[k.strip()]=v.strip().strip('"').strip("'")
    return {"state":"VERIFY","source":str(p),"validation":"LEGACY_MANUAL_STATE_UNVERIFIED","data":data}
