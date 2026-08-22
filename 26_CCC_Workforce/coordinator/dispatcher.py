from pathlib import Path
import yaml

ROOT = Path(__file__).resolve().parents[1]

def _routes():
    return yaml.safe_load((ROOT / "routing.yaml").read_text(encoding="utf-8"))["routes"]

def route(event_type: str):
    routes = _routes()
    if event_type not in routes:
        return {"status": "UNROUTED", "event_type": event_type, "next_owner": "command", "reason": "unknown_event_requires_command_triage"}
    rule = dict(routes[event_type])
    rule["status"] = "ROUTED"
    rule["event_type"] = event_type
    return rule
