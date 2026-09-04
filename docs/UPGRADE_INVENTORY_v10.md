# CCC v10 Upgrade Inventory

**Repository:** `ced213gcg-design/FreedomArchitect`  
**Upgrade branch:** `upgrade/ccc-living-dashboard-v10`  
**Baseline branch:** `main`  
**Baseline commit observed during inventory:** `6f8877517e20a58407bb26151b786f2230c6437e`  
**Method:** FACT / RISK / ACTION with SOURCE / TIME / OWNER / CHANGE / VALIDATION / PROVENANCE.

## Executive finding

The repository already contains a meaningful lineage of command, dashboard, automation, application, and controlled-auto components. v10 will **preserve and wrap** those components rather than replace them silently. The new layers 19-24 become the canonical CCC integration plane while legacy numbered directories remain available as compatibility and human-operating surfaces.

Build is not completion. Existing code is treated as evidence of prior capability, not proof of current READY state.

## Inventory

| Path | Purpose observed | Current state | Dependencies / inputs | v10 disposition | Evidence/source | Primary risk | Next action |
|---|---|---|---|---|---|---|---|
| `00_Admin_Control/assistant/` | Local assistant control files and heartbeat logging. | BUILD / legacy-local | `$HOME/FreedomArchitect`, shell, local files | **Preserve + integrate** | `heartbeat.sh`, `heartbeat.log`, inbox/review/question files | Heartbeat is file-based and not authoritative telemetry. | Expose only validated state through adapters; do not promote log existence to PASS. |
| `01_Cybersecurity/soc-analyst-lab/` | SOC-analysis portfolio/lab documentation. | BUILD / portfolio | Wireshark, Nmap, Linux CLI, documented scenarios | **Preserve + reference** | SOC Analyst Lab README | Portfolio narrative is not the Dell live SOC runtime. | Keep as portfolio lineage; v10 SOC adapter reads the approved Dell state surface instead. |
| `01_Cybersecurity/GitHub` | Git-linked cybersecurity component present as a repository commit/submodule-style entry. | VERIFY | External Git object / linked repository | **Preserve + isolate dependency** | repository tree | External linkage can drift independently. | Record dependency; do not rewrite automatically. |
| `05_Application_Engine/` | Tracks jobs, applications, follow-ups, recruiter outreach, scoring, and next actions. | BUILD / operational workflow | Markdown logs, pipeline files, scorecards, templates | **Preserve + future adapter** | Application Engine README | Manual Markdown state can become stale or conflict with canonical state. | Keep career data separate from CCC P0 control-plane truth; adapt later through Living Intelligence. |
| `06_Daily_Command_Dashboard/` | Daily human command/readout layer for priorities, KPI, mission, briefing, and end-of-day review. | BUILD / legacy-human-interface | Markdown status files, Bash launcher, `nano` | **Preserve + compatibility link** | README and `scripts/dashboard.sh` | Manual edits are not live telemetry and can disagree with runtime state. | Retain as daily human layer; point users to Living Dashboard for canonical v10 state. |
| `07_Unified_Launcher/` | Single local entry point routing into Freedom Architect modules. | BUILD / legacy-launcher | Bash and existing module paths | **Preserve + document link** | Unified Launcher README and launcher script | Hard-coded/local routing may not understand v10 role-driven services. | Add documented v10 Living Dashboard entry without breaking legacy paths. |
| `09_Mission_State_Dashboard/` | Tracks mission state, objective, active branch, public presence, portfolio readiness, recruiting metrics, next action. | BUILD / legacy-state-readout | Local state environment file and shell script | **Preserve + migrate fields via adapter/API** | README and `mission-state.sh` | Local `.env` snapshot can be mistaken for authoritative live state. | Map useful fields into v10 state model; missing evidence must remain UNKNOWN. |
| `10_Executive_Summary_Board/` | Leadership-level view of strategic mission, platform state, readiness, pipeline, risks, and next moves. | BUILD / legacy-executive-view | Existing dashboards and manually maintained state | **Preserve + supersede presentation** | Executive Summary Board README | High-level summary can conceal stale or unsupported inputs. | Living Intelligence executive view becomes evidence-backed successor; retain board for lineage. |
| `13_Autonomous_Loop/` | Local opportunity pipeline: job discovery → selection → package generation → logging → dashboard update. | BUILD / controlled-automation-lineage | Job finder, application generator, logging, mission state | **Preserve controlled principle** | Autonomous Loop README | Naming can imply broader autonomy than behavior; external submission is intentionally absent. | Keep bounded automation; do not expand into unapproved external actions. |
| `18_Controlled_Auto_Framework/` | Role-based controlled automation, thresholds, release rules, ownership, audit/approval separation. | VERIFY / governance precursor | `controlled_auto.json`, `roles.json`, scripts/docs | **Preserve + supersede governance through v10 registries/policies** | config files and repository tree | Existing role ownership is conceptual and does not yet provide cryptographic identity, registration, revocation, or live health. | Translate useful separation-of-duty concepts into v10 role/agent registries; no self-registration. |
| `freedom.sh` and root launch/control scripts where present | Root-level convenience/control entry points. | BUILD / legacy | Shell and existing numbered modules | **Preserve** | repository tree | Root scripts can bypass newer validation if modified carelessly. | Do not delete; document relationship after v10 services are proven. |

## Existing behavior that must remain true

1. Legacy directories are not silently deleted or rewritten.
2. `13_Autonomous_Loop` remains bounded and does not auto-submit external applications.
3. `18_Controlled_Auto_Framework` separation of approval, audit, logging, and execution is preserved conceptually while v10 adds explicit registration and trust controls.
4. Legacy dashboards remain human-operating/readout layers; v10 does not reinterpret stale/manual state as verified telemetry.
5. GitHub `main` is not a working branch for v10 implementation.

## v10 controlled additions

The following layers will be added according to the master batch:

- `19_Live_Adaptive_Dashboard/` — human-understandable, data-bound digital twin and API.
- `20_CCC_Living_Organism/` — manifest, registries, contracts, and schemas.
- `21_CCC_Orchestra/` — placement, integration, evidence, release, and pressure-loss evaluation.
- `22_CCC_Ledger/` — append-only evidence chain plus economic/technology decision gates.
- `23_CCC_Agent_Mesh/` — explicit agent registration, policy, health, revocation, and approval surfaces.
- `24_CCC_Communications/` — GitHub/Codex/Slack contracts and sanitized event routing.
- `config/`, `scripts/`, `.github/workflows/`, and `docs/` — deployment, validation, CI, threat model, migration, and release evidence.

## P0 dependency order derived from actual repository state

1. Establish v10 canonical manifest, schemas, host/role/communication registries.
2. Implement append-only Ledger because later state transitions require evidence lineage.
3. Implement Dell SOC adapter against `C:\CCC\State\ccc-soc-live-state.json`; missing input must produce `UNKNOWN`.
4. Implement Orchestra pressure-loss/evidence/release evaluation.
5. Implement Agent Mesh with explicit registration and default-deny action policy.
6. Implement Living Dashboard APIs on top of approved sources only.
7. Implement data-bound sphere visualization with Canvas fallback.
8. Add validation/bootstrap scripts and CI/security workflows.
9. Document communications, deployment, legacy integration, future role-based migration, and economics gate.
10. Run tests, repair failures, generate `UPGRADE_REPORT_v10.md`, and open a draft PR for human review.

## Known baseline risks

- Manual Markdown and `.env` state can be stale.
- Existing local scripts use workstation-specific paths.
- Existing controlled-auto roles are not authenticated identities.
- No v10 append-only evidence chain exists yet.
- No canonical JSON Schema contract currently gates all agent/state events.
- The Dell live SOC state surface is external to the repository and therefore cannot be marked PASS from GitHub alone.
- No evidence yet proves the v10 acceptance gate; current release state remains **BUILD / VERIFY**.

## Next executable action

Create the v10 canonical manifest, schemas, and host/role registries on this branch, then validate their internal references before implementing Ledger.
