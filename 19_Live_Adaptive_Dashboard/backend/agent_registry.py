from pathlib import Path
import yaml
def load(path): return yaml.safe_load(Path(path).read_text(encoding="utf-8"))
def public_view(path):
    data=load(path); return [{k:a.get(k) for k in ("id","type","owner","host","role","state","last_seen","version","revocation_state","health_endpoint")} for a in data.get("agents",[])]
