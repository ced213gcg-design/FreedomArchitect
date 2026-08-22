from agent_mesh import load_registry
def snapshot(path=None):
    data=load_registry(path) if path else load_registry()
    return [{"id":a["id"],"state":a["state"],"revocation_state":a["revocation_state"],"last_seen":a.get("last_seen")} for a in data.get("agents",[])]
