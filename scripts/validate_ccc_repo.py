from pathlib import Path
import json,yaml
from jsonschema import Draft202012Validator

ROOT=Path(__file__).resolve().parents[1]
REQUIRED=[
 "20_CCC_Living_Organism/ccc.manifest.json",
 "20_CCC_Living_Organism/host-registry.yaml",
 "20_CCC_Living_Organism/role-registry.yaml",
 "20_CCC_Living_Organism/schemas/exception-event.schema.json",
 "20_CCC_Living_Organism/schemas/opportunity-event.schema.json",
 "20_CCC_Living_Organism/schemas/soc-evidence-bridge.schema.json",
 "20_CCC_Living_Organism/schemas/soc-detection-run.schema.json",
 "23_CCC_Agent_Mesh/registry.yaml",
 "22_CCC_Ledger/ledger.py",
 "22_CCC_Ledger/classify_financial_state.py",
 "19_Live_Adaptive_Dashboard/backend/app.py",
 "19_Live_Adaptive_Dashboard/backend/exception_adapter.py",
 "19_Live_Adaptive_Dashboard/backend/evidence_bridge.py",
 "19_Live_Adaptive_Dashboard/backend/soc_mission_adapter.py",
 "19_Live_Adaptive_Dashboard/backend/soc_scenario_adapter.py",
 "19_Live_Adaptive_Dashboard/backend/soc_latency.py",
 "19_Live_Adaptive_Dashboard/frontend/soc_physical_evidence.js",
 "25_CCC_Exception_Intelligence/exception_engine.py",
 "25_CCC_Exception_Intelligence/verifier.py",
 "25_CCC_Exception_Intelligence/fit_score.py",
 "25_CCC_Exception_Intelligence/freshness.py",
 "25_CCC_Exception_Intelligence/routing.py",
 "24_CCC_Communications/gmail-contract.md",
 "config/exception-policy.yaml",
 "config/soc-five-test-registry.yaml",
 "config/soc-detection-scenarios.yaml",
 "config/soc-lab-targets.yaml",
 "scripts/warroom/CCC_HP_SOC_WARROOM_ONE_DROP.sh",
 "scripts/warroom/CCC_DELL_SOC_WARROOM_ONE_DROP.ps1",
]
def main():
    errors=[]
    for rel in REQUIRED:
        if not (ROOT/rel).exists(): errors.append(f"missing:{rel}")
    if errors: print(json.dumps({"status":"FAIL","errors":errors},indent=2)); return 1
    manifest=json.loads((ROOT/"20_CCC_Living_Organism/ccc.manifest.json").read_text())
    allowed=set(manifest["state_model"]["allowed"])
    if not str(manifest.get("version","")).startswith("10.1"): errors.append("manifest-version-not-v10.1")
    if manifest.get("release",{}).get("branch")!="upgrade/ccc-living-dashboard-v10-1": errors.append("wrong-release-branch")
    organ_ids=[o.get("id") for o in manifest.get("organs",[])]
    if "exception_intelligence" not in organ_ids: errors.append("missing-exception-intelligence-organ")
    if len(organ_ids)!=len(set(organ_ids)): errors.append("duplicate-organ-id")
    for o in manifest.get("organs",[]):
        if o.get("state") not in allowed: errors.append(f"invalid-organ-state:{o.get('id')}:{o.get('state')}")
    schemas={}
    for p in (ROOT/"20_CCC_Living_Organism/schemas").glob("*.json"):
        try:
            schema=json.loads(p.read_text()); Draft202012Validator.check_schema(schema); schemas[p.name]=schema
        except Exception as exc: errors.append(f"invalid-schema:{p.name}:{exc}")
    yaml_paths=list((ROOT/"20_CCC_Living_Organism").glob("*.yaml"))+list((ROOT/"23_CCC_Agent_Mesh").glob("*.yaml"))+list((ROOT/"config").glob("*.yaml"))
    for p in yaml_paths:
        try: yaml.safe_load(p.read_text())
        except Exception as exc: errors.append(f"invalid-yaml:{p}:{exc}")
    hosts=yaml.safe_load((ROOT/"20_CCC_Living_Organism/host-registry.yaml").read_text()) or {}
    required_hosts={"ccc-hp-dev-01","ccc-dell-compute-01"}
    if not required_hosts.issubset(set((hosts.get("hosts") or {}).keys())): errors.append("missing-current-host")
    hp=(hosts.get("hosts") or {}).get("ccc-hp-dev-01",{})
    if "exception-intelligence-development" not in hp.get("roles",[]): errors.append("hp-missing-exception-role")
    for hid,h in (hosts.get("hosts") or {}).items():
        if not h.get("roles"): errors.append(f"host-without-role:{hid}")
        if h.get("lifecycle")=="CURRENT" and not h.get("authority"): errors.append(f"current-host-without-authority:{hid}")
    roles=yaml.safe_load((ROOT/"20_CCC_Living_Organism/role-registry.yaml").read_text()) or {}
    if roles.get("principles",{}).get("default")!="deny": errors.append("role-default-not-deny")
    if roles.get("principles",{}).get("self_registration") is not False: errors.append("role-self-registration-not-disabled")
    agents=yaml.safe_load((ROOT/"23_CCC_Agent_Mesh/registry.yaml").read_text()) or {}; ids=[a.get("id") for a in agents.get("agents",[])]
    required_agents={"github-agent","codex-agent","slack-sink","gmail-channel","hp-dev-agent","dell-soc-agent","ledger-agent","orchestra-agent","mission-control-agent","exception-intelligence-agent","dashboard-agent"}
    if not required_agents.issubset(set(ids)): errors.append("missing-required-agent")
    if len(ids)!=len(set(ids)): errors.append("duplicate-agent-id")
    if agents.get("self_registration") is not False: errors.append("self-registration-not-disabled")
    schema=schemas.get("agent-registration.schema.json")
    if schema:
        v=Draft202012Validator(schema)
        for a in agents.get("agents",[]):
            for e in v.iter_errors(a): errors.append(f"agent-schema:{a.get('id')}:{e.message}")
    policy=yaml.safe_load((ROOT/"config/exception-policy.yaml").read_text()) or {}
    weights=(policy.get("scoring") or {}).get("weights") or {}
    if abs(sum(float(v) for v in weights.values())-1.0)>1e-9: errors.append("exception-weights-do-not-sum-1")
    public=set((policy.get("privacy") or {}).get("public_exception_fields") or [])
    forbidden=set((policy.get("privacy") or {}).get("forbidden_public_fields") or [])
    if public & forbidden: errors.append("exception-public-private-field-overlap")
    expected={"/api/exceptions","/api/exceptions/high-priority"}
    if not expected.issubset(set((manifest.get("dashboard") or {}).get("p0_endpoints") or [])): errors.append("missing-exception-api-contract")
    scenario_cfg=yaml.safe_load((ROOT/"config/soc-detection-scenarios.yaml").read_text()) or {}
    scenario_ids=[s.get("id") for s in scenario_cfg.get("scenarios",[])]
    if scenario_ids!=["DET-01","DET-02","DET-03","DET-04","DET-05"]: errors.append("invalid-physical-scenario-registry")
    target_cfg=yaml.safe_load((ROOT/"config/soc-lab-targets.yaml").read_text()) or {}
    if target_cfg.get("authoritative_range")!="10.69.69.0/24": errors.append("wrong-physical-lab-range")
    if target_cfg.get("policy",{}).get("require_exact_registered_target") is not True: errors.append("target-exact-match-not-required")
    print(json.dumps({"status":"PASS" if not errors else "FAIL","errors":errors},indent=2))
    return 0 if not errors else 1
if __name__=="__main__": raise SystemExit(main())
