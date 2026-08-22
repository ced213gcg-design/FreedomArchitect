from pathlib import Path
import json,sys,yaml
from jsonschema import Draft202012Validator, validate
ROOT=Path(__file__).resolve().parents[1]
REQUIRED=["20_CCC_Living_Organism/ccc.manifest.json","20_CCC_Living_Organism/host-registry.yaml","20_CCC_Living_Organism/role-registry.yaml","23_CCC_Agent_Mesh/registry.yaml","22_CCC_Ledger/ledger.py","19_Live_Adaptive_Dashboard/backend/app.py","26_CCC_Workforce/workforce.yaml","26_CCC_Workforce/authority.yaml","26_CCC_Workforce/routing.yaml","26_CCC_Workforce/shift-policy.yaml","26_CCC_Workforce/model-routing.yaml"]
def main():
    errors=[]
    for rel in REQUIRED:
        if not (ROOT/rel).exists(): errors.append(f"missing:{rel}")
    if errors: print("\n".join(errors)); return 1
    manifest=json.loads((ROOT/REQUIRED[0]).read_text()); allowed=set(manifest["state_model"]["allowed"])
    for o in manifest["organs"]:
        if o["state"] not in allowed: errors.append(f"invalid-organ-state:{o['id']}:{o['state']}")
    schema_dirs=[ROOT/"20_CCC_Living_Organism/schemas",ROOT/"26_CCC_Workforce/schemas"]
    for directory in schema_dirs:
        for p in directory.glob("*.json"):
            try: Draft202012Validator.check_schema(json.loads(p.read_text()))
            except Exception as exc: errors.append(f"invalid-schema:{p.name}:{exc}")
    yaml_paths=list((ROOT/"20_CCC_Living_Organism").glob("*.yaml"))+list((ROOT/"23_CCC_Agent_Mesh").glob("*.yaml"))+list((ROOT/"config").glob("*.yaml"))+list((ROOT/"26_CCC_Workforce").glob("*.yaml"))
    for p in yaml_paths:
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
    agents=yaml.safe_load((ROOT/"23_CCC_Agent_Mesh/registry.yaml").read_text()) or {}; ids=[a['id'] for a in agents.get('agents',[])]
    required_agent_fields={"id","type","owner","host","role","public_key_or_identity_reference","allowed_inputs","allowed_outputs","allowed_actions","denied_actions","health_endpoint","state","last_seen","version","revocation_state"}
    for a in agents.get('agents',[]):
        missing=required_agent_fields-set(a)
        if missing: errors.append(f"agent-missing-fields:{a.get('id')}:{','.join(sorted(missing))}")
    if len(ids)!=len(set(ids)): errors.append("duplicate-agent-id")
    if agents.get('self_registration') is not False: errors.append("self-registration-not-disabled")
    workforce=yaml.safe_load((ROOT/"26_CCC_Workforce/workforce.yaml").read_text()) or {}; workers=workforce.get("workers",[])
    expected={"command","intelligence","security","revenue","communications"}
    if {w.get('id') for w in workers} != expected: errors.append("workforce-five-registration-mismatch")
    identities=[w.get('identity_ref') for w in workers]
    if len(identities)!=len(set(identities)): errors.append("workforce-shared-identity")
    try:
        ws=json.loads((ROOT/"26_CCC_Workforce/schemas/worker.schema.json").read_text())
        for w in workers: validate(w,ws)
    except Exception as exc: errors.append(f"workforce-worker-schema-fail:{exc}")
    shift=yaml.safe_load((ROOT/"26_CCC_Workforce/shift-policy.yaml").read_text()) or {}
    if shift.get("formal_reports_per_shift") != 2: errors.append("workforce-shift-report-count-not-two")
    authority=yaml.safe_load((ROOT/"26_CCC_Workforce/authority.yaml").read_text()) or {}
    if authority.get("default") != "deny": errors.append("workforce-authority-not-default-deny")
    model=yaml.safe_load((ROOT/"26_CCC_Workforce/model-routing.yaml").read_text()) or {}
    if model.get("unbounded_autonomous_loops") is not False: errors.append("workforce-unbounded-loop-enabled")
    print(json.dumps({"status":"PASS" if not errors else "FAIL","errors":errors},indent=2)); return 0 if not errors else 1
if __name__=="__main__": raise SystemExit(main())
