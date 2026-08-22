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
 "20_CCC_Living_Organism/schemas/strategic-analysis.schema.json",
 "20_CCC_Living_Organism/schemas/worker-handoff.schema.json",
 "20_CCC_Living_Organism/schemas/reinjection-capsule.schema.json",
 "20_CCC_Living_Organism/schemas/crayola-cycle.schema.json",
 "20_CCC_Living_Organism/schemas/mechanism-gate-result.schema.json",
 "23_CCC_Agent_Mesh/registry.yaml",
 "22_CCC_Ledger/ledger.py",
 "22_CCC_Ledger/classify_financial_state.py",
 "22_CCC_Ledger/economics/technology-choice-matrix.yaml",
 "19_Live_Adaptive_Dashboard/backend/app.py",
 "19_Live_Adaptive_Dashboard/backend/infinity_adapter.py",
 "19_Live_Adaptive_Dashboard/backend/game_theory_adapter.py",
 "19_Live_Adaptive_Dashboard/backend/crayola_adapter.py",
 "19_Live_Adaptive_Dashboard/backend/reinjection_adapter.py",
 "19_Live_Adaptive_Dashboard/backend/economics_gate.py",
 "19_Live_Adaptive_Dashboard/backend/exception_adapter.py",
 "19_Live_Adaptive_Dashboard/backend/evidence_bridge.py",
 "19_Live_Adaptive_Dashboard/backend/soc_mission_adapter.py",
 "19_Live_Adaptive_Dashboard/backend/soc_scenario_adapter.py",
 "19_Live_Adaptive_Dashboard/backend/soc_latency.py",
 "19_Live_Adaptive_Dashboard/frontend/soc_physical_evidence.js",
 "19_Live_Adaptive_Dashboard/frontend/infinity_composition.js",
 "19_Live_Adaptive_Dashboard/frontend/ccc_infinity.css",
 "25_CCC_Exception_Intelligence/exception_engine.py",
 "25_CCC_Exception_Intelligence/verifier.py",
 "25_CCC_Exception_Intelligence/fit_score.py",
 "25_CCC_Exception_Intelligence/freshness.py",
 "25_CCC_Exception_Intelligence/routing.py",
 "26_CCC_Game_Theory/README.md",
 "26_CCC_Game_Theory/engine.py",
 "26_CCC_Game_Theory/policy.yaml",
 "26_CCC_Game_Theory/schemas/strategic-analysis.schema.json",
 "config/ccc-constitutional-workers.yaml",
 "24_CCC_Communications/gmail-contract.md",
 "config/exception-policy.yaml",
 "config/soc-five-test-registry.yaml",
 "config/soc-detection-scenarios.yaml",
 "config/soc-lab-targets.yaml",
 "docs/CCC_INFINITY_UPDATE_MASTER_v1.md",
 "docs/CCC_INFINITY_SUPERSESSION_MAP_v1.md",
 "docs/CCC_INFINITY_ACCEPTANCE_v1.md",
 "scripts/warroom/CCC_HP_SOC_WARROOM_ONE_DROP.sh",
 "scripts/warroom/CCC_DELL_SOC_WARROOM_ONE_DROP.ps1",
 "scripts/warroom/export_physical_artifacts.py",
]

def main():
    errors=[]
    for rel in REQUIRED:
        if not (ROOT/rel).exists(): errors.append(f"missing:{rel}")
    if errors:
        print(json.dumps({"status":"FAIL","errors":errors},indent=2)); return 1

    manifest=json.loads((ROOT/"20_CCC_Living_Organism/ccc.manifest.json").read_text())
    allowed=set(manifest["state_model"]["allowed"])
    if not str(manifest.get("version","")).startswith("10.1"): errors.append("manifest-version-not-v10.1")
    if manifest.get("release",{}).get("branch")!="upgrade/ccc-infinity-composition-v1": errors.append("wrong-infinity-release-branch")
    frozen=(manifest.get("release") or {}).get("frozen_physical_candidate") or {}
    if frozen.get("pr")!=4 or frozen.get("sha")!="7bf932c5aac08d31979761e28c5d9218e002f6ad" or frozen.get("must_remain_unmodified") is not True:
        errors.append("frozen-physical-candidate-contract-mismatch")

    triad=(manifest.get("governance") or {}).get("decision_triad") or []
    sextet=(manifest.get("governance") or {}).get("evidence_sextet") or []
    historical_cycle=(manifest.get("governance") or {}).get("completion_cycle") or []
    nonet=manifest.get("completion_nonet") or []
    creator=manifest.get("creator_alignment") or []
    if triad!=["FACT","RISK","ACTION"] or len(triad)!=3: errors.append("decision-triad-not-exact-3")
    if sextet!=["SOURCE","TIME","OWNER","CHANGE","VALIDATION","PROVENANCE"] or len(sextet)!=6: errors.append("evidence-sextet-not-exact-6")
    if len(creator)!=9: errors.append("creator-alignment-not-exact-9")
    if len(historical_cycle)!=10: errors.append("historical-completion-cycle-not-preserved")
    if len(nonet)!=9 or nonet[-1]!="OPERATIONALIZE / REINVEST": errors.append("completion-nonet-not-exact-9")
    if not any(x.get("field")=="governance.completion_cycle" for x in manifest.get("supersession_history",[])): errors.append("completion-supersession-not-recorded")

    infinity_lifecycle=manifest.get("lifecycle_infinity") or {}
    if infinity_lifecycle.get("sequence")!=["ALPHA","BETA","GAMMA","OMEGA","REINJECTION","NEXT_ALPHA"]: errors.append("infinity-lifecycle-invalid")
    gamma=infinity_lifecycle.get("gamma") or {}
    if gamma.get("is_pass") is not False: errors.append("gamma-must-not-be-pass")
    required_gamma={"PROMOTE_TO_OMEGA_CANDIDATE","RETURN_TO_BETA","HOLD","ISOLATE","DOCUMENTED_REJECTION"}
    if not required_gamma.issubset(set(gamma.get("outcomes") or [])): errors.append("gamma-outcomes-incomplete")

    cadence=manifest.get("symbolic_cadence") or {}
    if cadence.get("ui_cadence_ms")!=963: errors.append("symbolic-cadence-missing-963")
    if cadence.get("telemetry_independent") is not True: errors.append("symbolic-cadence-coupled-to-telemetry")
    if "Operational telemetry uses evidence-grounded timing." not in str(cadence.get("operator_notice","")): errors.append("symbolic-cadence-notice-missing")

    workers_contract=manifest.get("five_worker_constitution") or {}
    exact_workers=["COMMAND","INTELLIGENCE","SECURITY","REVENUE","COMMS"]
    if workers_contract.get("workers")!=exact_workers or workers_contract.get("exact_count")!=5: errors.append("five-worker-manifest-contract-invalid")
    if workers_contract.get("consensus_creates_truth") is not False: errors.append("worker-consensus-truth-invalid")

    game_contract=manifest.get("game_theory_contract") or {}
    if game_contract.get("authority")!="ADVISORY_ONLY": errors.append("game-theory-not-advisory-only")
    if game_contract.get("consequential_execution_allowed") is not False: errors.append("game-theory-execution-not-denied")
    if game_contract.get("direct_verified_ledger_write_allowed") is not False: errors.append("game-theory-ledger-truth-write-not-denied")

    crayola=manifest.get("crayola_contract") or {}
    if len(crayola.get("stages") or [])!=7: errors.append("crayola-stage-count-not-7")
    if set(crayola.get("terminal_output_types") or [])!={"EVIDENCE","CAPABILITY","MEMORY","SEED","DOCUMENTED_REJECTION"}: errors.append("crayola-terminal-types-invalid")

    organ_ids=[o.get("id") for o in manifest.get("organs",[])]
    if "exception_intelligence" not in organ_ids: errors.append("missing-exception-intelligence-organ")
    if len(organ_ids)!=len(set(organ_ids)): errors.append("duplicate-organ-id")
    game_org=next((o for o in manifest.get("organs",[]) if o.get("id")=="game_theory"),None)
    if not game_org or game_org.get("state") not in {"BUILD","VERIFY"}: errors.append("game-theory-runtime-state-overclaimed")
    for o in manifest.get("organs",[]):
        if o.get("state") not in allowed: errors.append(f"invalid-organ-state:{o.get('id')}:{o.get('state')}")

    schemas={}
    for p in (ROOT/"20_CCC_Living_Organism/schemas").glob("*.json"):
        try:
            schema=json.loads(p.read_text()); Draft202012Validator.check_schema(schema); schemas[p.name]=schema
        except Exception as exc: errors.append(f"invalid-schema:{p.name}:{exc}")
    gt_schema=ROOT/"26_CCC_Game_Theory/schemas/strategic-analysis.schema.json"
    try: Draft202012Validator.check_schema(json.loads(gt_schema.read_text()))
    except Exception as exc: errors.append(f"invalid-game-theory-schema:{exc}")

    yaml_paths=(list((ROOT/"20_CCC_Living_Organism").glob("*.yaml"))+list((ROOT/"23_CCC_Agent_Mesh").glob("*.yaml"))+list((ROOT/"26_CCC_Game_Theory").glob("*.yaml"))+list((ROOT/"config").glob("*.yaml")))
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

    worker_cfg=yaml.safe_load((ROOT/"config/ccc-constitutional-workers.yaml").read_text()) or {}
    worker_ids=[w.get("id") for w in worker_cfg.get("workers",[])]
    if worker_ids!=exact_workers or worker_cfg.get("exact_worker_count")!=5: errors.append("constitutional-worker-registry-invalid")
    if worker_cfg.get("truth_authority")!="LEDGER": errors.append("constitutional-worker-truth-authority-invalid")

    matrix=yaml.safe_load((ROOT/"22_CCC_Ledger/economics/technology-choice-matrix.yaml").read_text()) or {}
    if len(matrix.get("dimensions") or [])!=14: errors.append("mechanism-gate-dimensions-not-14")
    if set((matrix.get("choices") or {}).keys())!=set("ABCDEFGHI"): errors.append("mechanism-gate-choice-set-not-A-I")
    internal=(matrix.get("example_decisions") or {}).get("ccc_internal_evidence") or {}
    if internal.get("blockchain_required") is not False: errors.append("internal-evidence-must-not-default-blockchain")

    policy=yaml.safe_load((ROOT/"config/exception-policy.yaml").read_text()) or {}
    weights=(policy.get("scoring") or {}).get("weights") or {}
    if abs(sum(float(v) for v in weights.values())-1.0)>1e-9: errors.append("exception-weights-do-not-sum-1")
    public=set((policy.get("privacy") or {}).get("public_exception_fields") or [])
    forbidden=set((policy.get("privacy") or {}).get("forbidden_public_fields") or [])
    if public & forbidden: errors.append("exception-public-private-field-overlap")

    infinity_endpoints=set((manifest.get("dashboard") or {}).get("infinity_endpoints") or [])
    expected={"/api/infinity/state","/api/infinity/lifecycle","/api/infinity/reinjection","/api/crayola/current","/api/game-theory/analyze","/api/game-theory/recent","/api/workers/constitutional","/api/workers/handoffs","/api/economics/mechanism-gate"}
    if not expected.issubset(infinity_endpoints): errors.append("missing-infinity-api-contract")

    scenario_cfg=yaml.safe_load((ROOT/"config/soc-detection-scenarios.yaml").read_text()) or {}
    scenario_ids=[s.get("id") for s in scenario_cfg.get("scenarios",[])]
    if scenario_ids!=["DET-01","DET-02","DET-03","DET-04","DET-05"]: errors.append("invalid-physical-scenario-registry")
    target_cfg=yaml.safe_load((ROOT/"config/soc-lab-targets.yaml").read_text()) or {}
    if target_cfg.get("authoritative_range")!="10.69.69.0/24": errors.append("wrong-physical-lab-range")
    if target_cfg.get("policy",{}).get("require_exact_registered_target") is not True: errors.append("target-exact-match-not-required")

    print(json.dumps({"status":"PASS" if not errors else "FAIL","errors":errors},indent=2))
    return 0 if not errors else 1
if __name__=="__main__": raise SystemExit(main())
