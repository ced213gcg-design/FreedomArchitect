from pathlib import Path
import json,re,sys,yaml
from jsonschema import Draft202012Validator
ROOT=Path(__file__).resolve().parents[1]
REQUIRED=["20_CCC_Living_Organism/ccc.manifest.json","20_CCC_Living_Organism/host-registry.yaml","20_CCC_Living_Organism/role-registry.yaml","23_CCC_Agent_Mesh/registry.yaml","22_CCC_Ledger/ledger.py","19_Live_Adaptive_Dashboard/backend/app.py"]
def main():
    errors=[]
    for rel in REQUIRED:
        if not (ROOT/rel).exists(): errors.append(f"missing:{rel}")
    if errors: print("\n".join(errors)); return 1
    manifest=json.loads((ROOT/REQUIRED[0]).read_text()); allowed=set(manifest["state_model"]["allowed"])
    for o in manifest["organs"]:
        if o["state"] not in allowed: errors.append(f"invalid-organ-state:{o['id']}:{o['state']}")
    for p in (ROOT/"20_CCC_Living_Organism/schemas").glob("*.json"):
        try: Draft202012Validator.check_schema(json.loads(p.read_text()))
        except Exception as exc: errors.append(f"invalid-schema:{p.name}:{exc}")
    for p in list((ROOT/"20_CCC_Living_Organism").glob("*.yaml"))+list((ROOT/"23_CCC_Agent_Mesh").glob("*.yaml"))+list((ROOT/"config").glob("*.yaml")):
        try: yaml.safe_load(p.read_text())
        except Exception as exc: errors.append(f"invalid-yaml:{p}:{exc}")
    agents=yaml.safe_load((ROOT/"23_CCC_Agent_Mesh/registry.yaml").read_text()); ids=[a['id'] for a in agents.get('agents',[])]
    if len(ids)!=len(set(ids)): errors.append("duplicate-agent-id")
    if agents.get('self_registration') is not False: errors.append("self-registration-not-disabled")
    print(json.dumps({"status":"PASS" if not errors else "FAIL","errors":errors},indent=2)); return 0 if not errors else 1
if __name__=="__main__": raise SystemExit(main())
