# CCC v10.1 Architecture

## Purpose

v10.1 extends the v10 institutional control plane without replacing verified lineage. Layers 19-24 remain the operating foundation. Layer 25, **CCC Exception Intelligence**, becomes the sensory-priority organ that elevates unusual opportunities, threats, anomalies, constraints and capability gaps into an auditable decision path.

## Authority map

- **GitHub**: code authority.
- **Ledger**: factual/evidence authority.
- **Orchestra**: integration, placement and release authority.
- **Mission Control**: pressure and priority authority.
- **Codex**: implementation/repair agent on scoped branches.
- **Slack**: simulation/review/notification sink only.
- **Gmail**: external communication channel only.
- **Living Dashboard**: digital twin and human control surface.
- **Exception Intelligence**: sensory-priority detection, verification, scoring and routing organ.

External communications never become institutional truth. Final state returns to GitHub + Ledger + Orchestra.

## Control layers

### 19 Live Adaptive Dashboard
Human-understandable readout over approved state. v10.1 adds exception adapters, list/high-priority endpoints and the Exception Constellation. Consequential actions remain approval requests only.

### 20 CCC Living Organism
Canonical manifest, release gates, host/role/organ/communication registries and schemas. v10.1 adds exception/opportunity contracts and registers Layer 25.

### 21 CCC Orchestra
Placement/integration/release authority. v10.1 adds `exception_router.py` to move verified scored exceptions to Mission Control, HOLD or the correct domain organ without creating authority.

### 22 CCC Ledger
Append-only evidence chain. v10.1 adds explicit financial-state classification so opportunity, contract, invoice, collected cash, reconciled revenue, restricted funding and internal savings remain distinct.

### 23 CCC Agent Mesh
Explicitly registered/default-deny agents. v10.1 registers Gmail, Mission Control and Exception Intelligence agents. No self-registration or self-propagation.

### 24 CCC Communications
GitHub/Codex/Slack/Gmail communication contracts. Slack/Gmail remain non-authoritative and sanitized.

### 25 CCC Exception Intelligence
Permanent sensory-priority organ.

Flow:

`SIGNAL -> VERIFY -> CROSS-EXAMINE -> SCORE -> LEDGER -> GAME THEORY -> MISSION CONTROL -> ORCHESTRA -> ACTION / HOLD`

Every exception carries source, freshness, component scoring, owner, next action, approval state and evidence references. Stale signals cannot remain VERIFIED.

## Exception classes

`EMPLOYMENT`, `FEDERAL_OPPORTUNITY`, `CUSTOMER_LEAD`, `GRANT`, `SECURITY`, `CVE`, `GITHUB_FAILURE`, `HARDWARE_PRICE`, `MARKET`, `RESEARCH`, `REGULATORY`, `FINANCIAL`, `INFRASTRUCTURE`, `CAPABILITY_GAP`, `OTHER`.

## Scoring

Exception score is a visible weighted function:

- Strategic Value 35%
- Time Sensitivity 20%
- Probability 15%
- Economic Upside 10%
- Capability Alignment 10%
- Evidence Confidence 5%
- Reinjection Value 5%

Classification:

- 90-100 CRITICAL OPPORTUNITY
- 80-89 HIGH PRIORITY
- 70-79 QUALIFIED
- 50-69 WATCH
- 0-49 ARCHIVE / IGNORE

No opaque score is permitted.

## Fit score

Fit score is separate from Exception Score and exposes category components with evidence references. For employment, default categories are Education, Project Experience, Technical Match, Role Competencies, Domain Match, Location/Work Model and Evidence Strength. Missing evidence lowers the score rather than being guessed.

## Freshness

Freshness states: `VERIFIED`, `AGING`, `STALE`, `CLOSED`, `SUPERSEDED`. Policy is type-aware and explicit. Freshness is derived from `last_verified` and configured windows, not visual optimism.

## Reverse-learning loop

`EXTERNAL REQUIREMENT -> CAPABILITY GAP -> CCC LAB/PROJECT -> EVIDENCE -> REPORT -> GITHUB PORTFOLIO -> APPLICATION/RESPONSE -> RESULT -> LEDGER -> REINJECTION`

A lost opportunity can still produce retained capability.

## 4D Exception Constellation

High-value verified exceptions may appear as Alpha shooting-star events. Selection reveals FACT, EVIDENCE, SOURCE, LAST VERIFIED, FRESHNESS, STRATEGIC VALUE, RISK, GAME THEORY, CAPABILITY GAP, FIT SCORE, EXCEPTION SCORE, OWNER, NEXT ACTION and APPROVAL STATE. Public visual payloads exclude private application/customer/financial data.

## Host architecture

Current:

- `ccc-hp-dev-01`: ChromeOS/Crostini development, dashboard, Ledger, Orchestra and Exception Intelligence development.
- `ccc-dell-compute-01`: Windows/Hyper-V SOC runtime and authoritative SOC state producer.

Future:

- `ccc-core-01`: Ledger/database/API/Mission Control/Living Intelligence/Exception Intelligence/CI.
- `ccc-range-01`: SOC/telemetry/honeypot/malware-analysis/simulation.
- `ccc-pulse-01`: portable status/approval/read-only emergency display.

`ROLE + CONFIG + TARGET = DEPLOYMENT`. Hardware replacement does not force application redesign.

## Release law

`BUILD != READY`, `READY != THRIVE`, `THRIVE != SCALE`. A numeric score never overrides hard-stop failures. v10.1 cannot advance beyond VERIFY/HOLD without CI, exception freshness/scoring/fit evidence, rollback, actual-host evidence and human review.