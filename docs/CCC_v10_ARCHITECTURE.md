# CCC v10 Controlled Architecture

## Status

**Release:** v10 P0  
**Working state:** BUILD / VERIFY  
**Branch:** `upgrade/ccc-living-dashboard-v10`

Build is never completion. Evidence earns state.

## Executive architecture decision

CCC v10 is a **role-driven, evidence-gated, human-governed operating mesh**. GitHub is code authority; Ledger is factual/evidence authority; Orchestra is placement/integration/release evaluator; Living Dashboard is the human-readable digital twin; registered agents are bounded execution or telemetry actors. No component may infer authority merely because it can reach another component.

## Authority planes

### GitHub — code authority
- source and history
- branches and pull requests
- CI / Actions evidence
- releases and defect tracking
- never the sole source of runtime truth

### Ledger — evidence authority
- append-only event lineage
- state transitions
- hashes and run IDs
- source / time / owner / change / validation / provenance
- synthetic and operational data are explicitly distinguished

### Orchestra — integration / release authority
- reads approved GitHub, Ledger, and live-state inputs
- determines component placement and dependency health
- evaluates evidence gates and pressure loss
- returns defects to engineering
- cannot manufacture evidence or promote UNKNOWN to PASS

### Living Dashboard — human digital twin
- reads approved state
- exposes normalized APIs
- renders evidence-bound visual state
- may submit controlled action requests
- does not directly perform privileged/consequential actions

### Agent Mesh — bounded registered actors
- explicit registration only
- authenticated identity reference
- owner, host, role, allowed inputs/outputs/actions
- denied actions, health, state, version, revocation
- default deny for unknown agents/actions
- no self-registration, propagation, credential harvesting, covert C2, unauthorized scanning, or third-party exploitation

## Physical / host model

### Current

`ccc-hp-dev-01`
- ChromeOS / Crostini Linux
- Git, GitHub, Python, dashboard development, Sigma, STIX/TAXII, documentation
- local Ledger/Orchestra development
- local tests and non-destructive simulations

`ccc-dell-compute-01`
- Windows 11 Pro / PowerShell 5.1 / Hyper-V
- approved SOC range runtime
- source of `C:\CCC\State\ccc-soc-live-state.json`
- approved local VM orchestration and runtime validation only

### Future

`ccc-core-01`, `ccc-range-01`, and `ccc-pulse-01` are modeled now but remain **FUTURE**. Application architecture is role-driven so hardware replacement does not require a system rewrite.

`ROLE + CONFIG + TARGET = DEPLOYMENT`

## Layer map

### Preserved lineage
- `00_Admin_Control`
- `01_Cybersecurity`
- `05_Application_Engine`
- `06_Daily_Command_Dashboard`
- `07_Unified_Launcher`
- `09_Mission_State_Dashboard`
- `10_Executive_Summary_Board`
- `13_Autonomous_Loop`
- `18_Controlled_Auto_Framework`

### v10 controlled layer
- `19_Live_Adaptive_Dashboard` — API, adapters, state store, digital twin, sphere
- `20_CCC_Living_Organism` — manifest, schemas, host/role/communication contracts
- `21_CCC_Orchestra` — pressure loss, evidence gate, release gate, integration map
- `22_CCC_Ledger` — append-only evidence chain and economic/technology choice gate
- `23_CCC_Agent_Mesh` — registration, policy, health, approvals
- `24_CCC_Communications` — GitHub/Codex/Slack contracts and routing

## Canonical state model

Primary states:

`DORMANT → SEED → INCUBATE → BUILD → VERIFY → READY → THRIVE → SCALE`

Side states:

`HOLD / ISOLATE / RETIRE`

Rules:
1. Missing evidence is `UNKNOWN` at an adapter boundary, never PASS.
2. BUILD cannot self-promote to READY.
3. READY requires the P0 acceptance gate.
4. THRIVE requires repeated useful runtime output plus Ledger evidence.
5. Critical Trust/Ledger/SRE/SOC failure overrides commercial optimization.

## Event contract

All cross-organ state events use a schema-validated envelope containing identity, source, target, UTC timestamp, run ID, state, severity, payload, and evidence. Ledger events additionally preserve prior/new state, validation/provenance, artifact hashes, synthetic flag, and financial classification.

## Action model

`POST /api/action-request` is a **request path**, not a privileged execution path.

Phase-1 rules:
- only registered action types are accepted
- requests are recorded in Ledger
- return state is `pending_approval`
- no automatic money movement, contract submission, release approval, credential rotation, destructive operation, or critical network change

Dashboard modes:
- COACH / PLAN / SIMULATE / DIVE: informational/non-destructive
- PROCEED: creates approval request only
- PAUSE / HALT: unavailable for consequential controls until explicit registered-service approval policy exists

## Pressure Loss

Each active organ is evaluated from 0-100 on:
- Progress
- Evidence
- Compliance
- Resilience
- EconomicValue

`PressureLoss = minimum(dimension scores)`

The output must include the weakest dimension, supporting evidence, owner, blocking dependency, and next executable action. A due **state** may be recorded; fabricated dates are prohibited.

## Ledger technology principle

CCC does not assume blockchain. Internal evidence begins with the simplest architecture that satisfies integrity, audit, governance, performance, recovery, and economic requirements. v10 Phase-1 therefore favors a signed/hash-linked append-only event log or event-sourced store unless a genuine multi-party consensus requirement is proven.

## P0 release sequence

1. Inventory legacy repository.
2. Establish architecture, manifest, schemas, host/role/communication registries.
3. Implement append-only Ledger and chain verification.
4. Implement Dell SOC live-state adapter.
5. Implement Orchestra pressure-loss/evidence/release evaluation.
6. Implement Agent Mesh explicit registration and read-only health.
7. Implement Living Dashboard APIs.
8. Implement data-bound sphere visualization and Canvas fallback.
9. Add CI/security/validation and sanitized communications contracts.
10. Integrate legacy dashboards/launcher through adapters/documentation.
11. Run tests; fix/retest; generate release evidence.
12. Open a draft PR for human approval.

## P0 state

At architecture creation, v10 remains **BUILD / VERIFY**. No runtime, CI, SOC, Ledger, dashboard, or acceptance claim is implied by the existence of this document.
