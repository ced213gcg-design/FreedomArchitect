import json
from pathlib import Path
def recent(path,limit=25):
    p=Path(path)
    if not p.exists(): return []
    out=[]
    for line in p.read_text(encoding="utf-8").splitlines():
        if line.strip(): out.append(json.loads(line))
    return out[-limit:]
