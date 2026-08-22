import importlib.util, json, sys
from pathlib import Path
ROOT=Path(__file__).resolve().parents[2]; BACK=ROOT/"19_Live_Adaptive_Dashboard"/"backend"; sys.path.insert(0,str(BACK)); s=importlib.util.spec_from_file_location("ccc_app",BACK/"app.py"); app=importlib.util.module_from_spec(s); s.loader.exec_module(app)
def payload(result): return json.loads(result[2])
def test_health(): status,_,body=app.route_request("GET","/api/health"); assert status==200 and json.loads(body)["status"]=="PASS"
def test_manifest(): status,_,body=app.route_request("GET","/api/manifest"); assert status==200 and json.loads(body)["schema"]=="ccc.living_organism.manifest.v10"
