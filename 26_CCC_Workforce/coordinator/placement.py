from pathlib import Path
import importlib.util

HERE = Path(__file__).resolve().parent

def _load(name):
    p = HERE / f"{name}.py"; spec = importlib.util.spec_from_file_location(f"workforce_{name}", p); mod = importlib.util.module_from_spec(spec); spec.loader.exec_module(mod); return mod

def place(event_type: str, online: dict, consequential: bool=False):
    if consequential and not online.get("security", False):
        return {"status": "HOLD", "reason": "SECURITY_OFFLINE_CONSEQUENTIAL_ACTION_DEFAULT_HOLD", "next_owner": "command"}
    route = _load("dispatcher").route(event_type)
    return {"status": "PLACED" if route.get("status") == "ROUTED" else "TRIAGE", "route": route, "authority": "ORCHESTRA_COMPATIBLE_REQUEST_ONLY"}
