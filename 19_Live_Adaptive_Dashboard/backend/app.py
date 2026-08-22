from __future__ import annotations
from http.server import BaseHTTPRequestHandler,ThreadingHTTPServer
from pathlib import Path
from urllib.parse import urlparse
from datetime import datetime,timezone
import importlib.util,json,os,sys,uuid

HERE=Path(__file__).resolve().parent; ROOT=HERE.parents[1]
sys.path.insert(0,str(HERE)); sys.path.insert(0,str(ROOT))
from state_store import manifest,hosts,agents,ledger_path,repo_path,read_yaml
from soc_adapter import SocAdapter
from ledger_adapter import recent as ledger_recent
from agent_registry import public_view
from economics_gate import internal_evidence_decision,evaluate_mechanism
from revenue_flywheel import get_revenue_flywheel
from exception_adapter import get_exceptions,get_high_priority
from soc_mission_adapter import five_missions,mission_trace
from soc_scenario_adapter import scenario_summary,scenario_trace,bridge_status,sensor_inventory
from vm_state_adapter import vm_portals
from interaction_api import interaction_contract,normalize_interaction
from infinity_adapter import state as infinity_state,lifecycle as infinity_lifecycle,workers as constitutional_workers,handoffs as constitutional_handoffs
from crayola_adapter import current as crayola_current
from game_theory_adapter import analyze as game_theory_analyze,recent as game_theory_recent
from reinjection_adapter import current as reinjection_current

def _load(name,path):
    s=importlib.util.spec_from_file_location(name,path); m=importlib.util.module_from_spec(s); s.loader.exec_module(m); return m
pressure_mod=_load("pressure_loss",repo_path("21_CCC_Orchestra","pressure_loss.py")); ledger_mod=_load("ccc_ledger",repo_path("22_CCC_Ledger","ledger.py")); approvals_mod=_load("approvals",repo_path("23_CCC_Agent_Mesh","approvals.py")); agent_mesh_mod=_load("agent_mesh",repo_path("23_CCC_Agent_Mesh","agent_mesh.py"))
REGISTERED_ACTIONS={"PROCEED_REQUEST","RELEASE_REVIEW_REQUEST","SOC_RUNTIME_START_REQUEST"}

def _json(status,payload): return status,{"Content-Type":"application/json; charset=utf-8"},json.dumps(payload,default=str).encode()
def _organ_scores(organ):
    state=organ.get("state","INCUBATE"); base={"DORMANT":10,"SEED":20,"INCUBATE":35,"BUILD":50,"VERIFY":65,"READY":80,"THRIVE":90,"SCALE":95}.get(state,25)
    return {"Progress":base,"Evidence":max(10,base-10),"Compliance":70 if state not in ("HOLD","ISOLATE") else 35,"Resilience":50 if state in ("BUILD","VERIFY") else 60,"EconomicValue":50}
def _pressure():
    rows=[]
    for organ in manifest().get("organs",[]):
        p=pressure_mod.calculate(_organ_scores(organ)); rows.append({"organ":organ["id"],**p,"evidence_basis":"DECLARED_CONFIG_NOT_RUNTIME","constraint":"Weakest verified material dimension constrains promotion until evidence improves.","owner":"mission_control","state_change_evidence":"COLLECT_RUNTIME_EVIDENCE","next_action":"COLLECT_RUNTIME_EVIDENCE"})
    weakest=min(rows,key=lambda r:r["PressureLoss"]) if rows else None; return {"state":"VERIFY","principle":"WEAKEST_VERIFIED_MATERIAL_DIMENSION","organs":rows,"system_weakest":weakest,"hard_control_override":True}
def _sphere():
    nodes=[]
    for idx,o in enumerate(manifest().get("organs",[])):
        s=_organ_scores(o); nodes.append({"id":o["id"],"label":o["name"],"state":o["state"],"x":idx%5,"y":s["EconomicValue"],"w":100 if o.get("criticality")=="TIER_0" else 60,"s":s["Evidence"],"importance":100 if o.get("criticality")=="TIER_0" else 60,"activity":0,"confidence":s["Evidence"],"data_quality":"DECLARED_CONFIG"})
    return {"dimensions":{"X":"Capability","Y":"Productive Value","W":"Strategic Will / Authorization","S":"Verified Operating State"},"nodes":nodes,"edges":[],"exception_constellation":get_high_priority(),"symbolic_heartbeat_ms":963,"telemetry_independent":True}
def _revenue_flywheel(): return get_revenue_flywheel(repo_path("config","revenue-stream-registry.yaml"),repo_path("22_CCC_Ledger","economics","revenue-flywheel-policy.yaml"))

def _append_interaction(event):
    ledger_event={
        "event_id":event["interaction_id"],
        "timestamp":event["timestamp"],
        "source":"living-dashboard",
        "owner":"human-operator",
        "organ":"living_intelligence",
        "run_id":event.get("run_id") or event["interaction_id"],
        "event_type":"INTERACTION_REQUEST",
        "previous_state":event.get("state_before") or "VERIFY",
        "new_state":event.get("state_after") or "HOLD",
        "change":event["action_type"],
        "validation":"SEMANTIC_INTERACTION_RECORDED_NOT_EXECUTED",
        "provenance":"POST /api/interaction-event",
        "artifact_hashes":[event["evidence_ref"]] if event.get("evidence_ref") else [],
        "synthetic":False,
        "financial_classification":"NON_FINANCIAL",
        "notes":f"Target={event['target_object']}; requested_effect={event.get('requested_effect')}; authority_required={event.get('authority_required')}. No underlying consequential action executed by this endpoint."
    }
    ledger_mod.append_event(ledger_path(),ledger_event)

def _frontend_payload(fp,path):
    payload=fp.read_bytes()
    if path in {"/","/index.html"}:
        marker=b'<script src="soc_physical_evidence.js"></script>'
        if marker not in payload:
            payload=payload.replace(b"</body>",marker+b"\n</body>")
    return payload

def route_request(method,path,body=None):
    m=manifest(); static={
        "/":"index.html","/index.html":"index.html","/app.js":"app.js","/sphere.js":"sphere.js","/exception_constellation.js":"exception_constellation.js","/styles.css":"styles.css",
        "/ccc_multiverse.css":"ccc_multiverse.css","/interaction_telemetry.js":"interaction_telemetry.js","/context_lens.js":"context_lens.js","/command_deck.js":"command_deck.js","/ccc_horizon.js":"ccc_horizon.js","/object_cards.js":"object_cards.js","/executive_mode.js":"executive_mode.js","/soc_physical_evidence.js":"soc_physical_evidence.js",
        "/infinity_composition.js":"infinity_composition.js","/ccc_infinity.css":"ccc_infinity.css"
    }
    if method=="GET" and path in static:
        fp=repo_path("19_Live_Adaptive_Dashboard","frontend",static[path])
        if not fp.exists(): return _json(404,{"error":"frontend_missing"})
        ctype="text/html; charset=utf-8" if fp.suffix==".html" else "text/javascript; charset=utf-8" if fp.suffix==".js" else "text/css; charset=utf-8"; return 200,{"Content-Type":ctype},_frontend_payload(fp,path)
    if method=="GET" and path=="/api/health": return _json(200,{"status":"PASS","state":"BUILD","service":"ccc-living-dashboard","version":"10.1-P0","release":"CCC-INFINITY-COMPOSITION-v1","physical_patch":"TAPER-ONE-DROP-v1","frozen_physical_candidate_sha":"7bf932c5aac08d31979761e28c5d9218e002f6ad","timestamp":datetime.now(timezone.utc).isoformat()})
    if method=="GET" and path=="/api/manifest": return _json(200,m)
    if method=="GET" and path=="/api/hosts": return _json(200,hosts())
    if method=="GET" and path=="/api/organs": return _json(200,{"organs":m.get("organs",[])})
    if method=="GET" and path=="/api/mission": return _json(200,{"state":m.get("status"),"branch":"upgrade/ccc-infinity-composition-v1","frozen_physical_candidate":"hotfix/ccc-soc-five-live-evidence-v1@7bf932c5aac08d31979761e28c5d9218e002f6ad","next_action":"COMPOSE_INFINITY_WITHOUT_DISTURBING_PHYSICAL_ACCEPTANCE","validation":"DECLARED_INFINITY_BRANCH"})
    if method=="GET" and path=="/api/pressure-loss": return _json(200,_pressure())
    if method=="GET" and path=="/api/soc/state": return _json(200,SocAdapter().get_state())
    if method=="GET" and path in {"/api/soc/missions","/api/soc/control-gates"}: return _json(200,five_missions())
    if method=="GET" and path=="/api/soc/trace": return _json(200,mission_trace())
    if method=="GET" and path=="/api/soc/scenarios": return _json(200,scenario_summary())
    if method=="GET" and path=="/api/soc/scenario-trace": return _json(200,scenario_trace())
    if method=="GET" and path=="/api/soc/bridge": return _json(200,bridge_status())
    if method=="GET" and path=="/api/sensors": return _json(200,sensor_inventory())
    if method=="GET" and path=="/api/vms": return _json(200,vm_portals())
    if method=="GET" and path in {"/api/ledger/recent","/api/evidence/recent"}: return _json(200,{"events":ledger_recent(ledger_path())})
    if method=="GET" and path=="/api/agents": return _json(200,{"agents":public_view(repo_path("23_CCC_Agent_Mesh","registry.yaml"))})
    if method=="GET" and path=="/api/exceptions": return _json(200,get_exceptions())
    if method=="GET" and path=="/api/exceptions/high-priority": return _json(200,get_high_priority())
    if method=="GET" and path=="/api/sphere": return _json(200,_sphere())
    if method=="GET" and path=="/api/economics/technology-choice": return _json(200,internal_evidence_decision(repo_path("22_CCC_Ledger","economics","technology-choice-matrix.yaml")))
    if method=="GET" and path=="/api/economics/revenue-flywheel": return _json(200,_revenue_flywheel())
    if method=="GET" and path=="/api/infinity/state": return _json(200,infinity_state())
    if method=="GET" and path=="/api/infinity/lifecycle": return _json(200,infinity_lifecycle())
    if method=="GET" and path=="/api/infinity/reinjection": return _json(200,reinjection_current())
    if method=="GET" and path=="/api/crayola/current": return _json(200,crayola_current())
    if method=="GET" and path=="/api/game-theory/recent": return _json(200,game_theory_recent())
    if method=="GET" and path=="/api/workers/constitutional": return _json(200,constitutional_workers())
    if method=="GET" and path=="/api/workers/handoffs": return _json(200,constitional_handoffs())
    if method=="GET" and path=="/api/interaction/contract": return _json(200,interaction_contract())
    if method=="POST" and path=="/api/game-theory/analyze":
        payload=body if isinstance(body,dict) else json.loads(body or "{}"); result=game_theory_analyze(payload); return _json(200 if result.get("status")!="HOLD" else 422,result)
    if method=="POST" and path=="/api/economics/mechanism-gate":
        payload=body if isinstance(body,dict) else json.loads(body or "{}"); result=evaluate_mechanism(repo_path("22_CCC_Ledger","economics","technology-choice-matrix.yaml"),payload); return _json(200,result)
    if method=="POST" and path=="/api/interaction-event":
        payload=body if isinstance(body,dict) else json.loads(body or "{}"); event=normalize_interaction(payload)
        if not event.get("accepted"): return _json(400,event)
        if event.get("route")=="LEDGER_REQUIRED":
            _append_interaction(event); event["ledger_recorded"]=True; return _json(202,event)
        event["ledger_recorded"]=False; return _json(200,event)
    if method=="POST" and path=="/api/action-request":
        payload=body if isinstance(body,dict) else json.loads(body or "{}"); action=payload.get("action_type"); requester=payload.get("requester","dashboard-agent")
        if action not in REGISTERED_ACTIONS: return _json(400,{"status":"REJECTED","reason":"unregistered_action_type"})
        auth=agent_mesh_mod.authorize(requester,"submit_action_request")
        if not auth["allowed"]: return _json(403,{"status":"REJECTED","reason":"requester_not_authorized","detail":auth["reason"]})
        req=approvals_mod.create_request(action,requester,payload.get("payload",{})); event={"event_id":str(uuid.uuid4()),"timestamp":datetime.now(timezone.utc).isoformat(),"source":"living-dashboard","owner":requester,"organ":"mission_control","run_id":req["approval_id"],"event_type":"APPROVAL_REQUEST","previous_state":"VERIFY","new_state":"HOLD","change":action,"validation":"PENDING_HUMAN_APPROVAL","provenance":"POST /api/action-request","artifact_hashes":[],"synthetic":False,"financial_classification":"NON_FINANCIAL","notes":"Request recorded; no consequential action executed."}; ledger_mod.append_event(ledger_path(),event); return _json(202,{**req,"executed":False})
    return _json(404,{"error":"not_found"})
class Handler(BaseHTTPRequestHandler):
    def _send(self,method):
        path=urlparse(self.path).path; body=None
        if method=="POST":
            n=int(self.headers.get("Content-Length","0") or 0); raw=self.rfile.read(n) if n else b"{}"; body=raw.decode()
        status,headers,payload=route_request(method,path,body); self.send_response(status)
        for k,v in headers.items(): self.send_header(k,v)
        self.send_header("Content-Length",str(len(payload))); self.end_headers(); self.wfile.write(payload)
    def do_GET(self): self._send("GET")
    def do_POST(self): self._send("POST")
    def log_message(self,fmt,*args): return
def main():
    host=os.getenv("CCC_DASHBOARD_HOST","127.0.0.1"); port=int(os.getenv("CCC_DASHBOARD_PORT","8787")); print(f"CCC Living Dashboard Infinity Composition: http://{host}:{port}"); ThreadingHTTPServer((host,port),Handler).serve_forever()
if __name__=="__main__": main()
