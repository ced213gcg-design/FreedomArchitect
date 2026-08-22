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
    hosts=yaml.safe_load((ROOT/"20_CCC_Living_Organism/host-registry.yaml").read_text()) or {}
    required_hosts={"ccc-hp-dev-01","ccc-dell-compute-01"}
    if not required_hosts.issubset(set((hosts.get('hosts') or {}).keys())): errors.append("missing-current-host")
    for hid,h in (hosts.get('hosts') or {}).items():
        if not h.get('roles'): errors.append(f"host-without-role:{hid}")
        if h.get('lifecycle') == 'CURRENT' and not h.get('authority'): errors.append(f"current-host-without-authority:{hid}")
    roles=yaml.safe_load((ROOT/"20_CCC_Living_Organism/role-registry.yaml").read_text()) or {}
    if roles.get('principles',{}).get('default') != 'deny': errors.append("role-default-not-deny")
    if roles.get('principles',{}).get('self_registration') is not False: errors.append("role-self-registration-not-disabled")
    agents=yaml.safe_load((ROOT/"23_CCC_Agent_Mesh/registry.yaml").read_text()); ids=[a['id'] for a in agents.get('agents',[])]
    required_agent_fields={"id","type","owner","host","role","public_key_or_identity_reference","allowed_inputs","allowed_outputs","allowed_actions","denied_actions","health_endpoint","state","last_seen","version","revocation_state"}
    for a in agents.get('agents',[]):
        missing=required_agent_fields-set(a)
        if missing: errors.append(f"agent-missing-fields:{a.get('id')}:{','.join(sorted(missing))}")
    if len(ids)!=len(set(ids)): errors.append("duplicate-agent-id")
    if agents.get('self_registration') is not False: errors.append("self-registration-not-disabled")
    print(json.dumps({"status":"PASS" if not errors else "FAIL","errors":errors},indent=2)); return 0 if not errors else 1
if __name__=="__main__": raise SystemExit(main())
