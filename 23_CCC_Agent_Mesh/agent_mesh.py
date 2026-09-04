from pathlib import Path
import yaml
DEFAULT=Path(__file__).with_name("registry.yaml")
def load_registry(path=DEFAULT):
    data=yaml.safe_load(Path(path).read_text(encoding="utf-8")) or {}
    return data
def get_agent(agent_id, path=DEFAULT):
    for a in load_registry(path).get("agents",[]):
        if a.get("id")==agent_id: return a
    return None
def authorize(agent_id, action, path=DEFAULT):
    a=get_agent(agent_id,path)
    if not a: return {"allowed":False,"reason":"unknown_agent"}
    if a.get("revocation_state")!="ACTIVE": return {"allowed":False,"reason":"revoked_or_pending"}
    if action in a.get("denied_actions",[]): return {"allowed":False,"reason":"explicitly_denied"}
    return {"allowed": action in a.get("allowed_actions",[]), "reason":"allowed" if action in a.get("allowed_actions",[]) else "not_registered_for_agent"}
