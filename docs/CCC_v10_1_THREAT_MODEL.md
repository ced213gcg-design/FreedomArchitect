# CCC v10.1 Threat Model

## Protected assets

- GitHub source/history and branch integrity
- Ledger evidence chain and provenance
- Agent identities/registries and approval records
- SOC live state and authorized lab boundaries
- Opportunity/application/customer/financial privacy
- Exception Intelligence scoring/freshness integrity
- Revenue classification and reconciliation truth
- Human approval authority

## Trust boundaries

1. GitHub repository and CI.
2. HP/Crostini development host.
3. Dell/Hyper-V authorized SOC environment.
4. Agent Mesh registration and policy boundary.
5. Slack/Gmail external communication channels.
6. Public/dashboard visual payloads.
7. External opportunity/research sources.
8. Imagination Station, explicitly separate with no backchannel.

## Primary threats and controls

### Unbounded autonomy
**Threat:** agent executes consequential actions without approval.  
**Control:** default READ/OBSERVE/REPORT; registered action types; pending-approval only; Ledger event; human approval and rollback.

### Signal poisoning / fabricated opportunities
**Threat:** low-quality or malicious external data becomes priority truth.  
**Control:** source/evidence references, freshness, confidence, cross-examination, type-aware scoring, HOLD on insufficient evidence.

### Stale intelligence masquerading as current
**Threat:** old job/grant/CVE/market data remains green.  
**Control:** deterministic freshness state, `last_verified`, AGING/STALE transition tests, high-priority query excludes stale/closed/superseded signals.

### Score manipulation
**Threat:** unexplained 90+ score causes false urgency.  
**Control:** visible weighted formula, bounded numeric inputs, component evidence, unit tests, separate fit vs exception score.

### Financial-state contamination
**Threat:** opportunity/contract/invoice/grant/internal savings mislabeled as realized revenue.  
**Control:** explicit financial classifier; Ledger provenance; revenue flywheel reconciliation gate; no automatic money movement.

### Private-data leakage
**Threat:** personal application/customer/financial details leak through dashboard, Slack or Gmail.  
**Control:** public adapter allowlists, sanitized summaries, no credentials/secrets, no private payload in constellation.

### Unauthorized agent or self-registration
**Threat:** unknown service enters mesh.  
**Control:** explicit registry, default deny, revocation state, unknown-agent rejection tests, no self-registration.

### Covert command channel
**Threat:** Slack/Gmail/event routing becomes shell/C2 path.  
**Control:** structured message types only, no arbitrary command payloads, communication channels are sinks/channels not authority.

### SOC boundary escape
**Threat:** security logic targets unauthorized systems.  
**Control:** authoritative range `10.69.69.0/24`, no unauthorized scanning, no exploit deployment to third parties, SOC adapter read-only state ingestion.

### Ledger tampering
**Threat:** event history changed or deleted.  
**Control:** canonical event hashing, previous-event hash chain, verification tests, append-only semantics.

### GitHub/release compromise
**Threat:** direct-to-main changes or self-merge.  
**Control:** scoped v10.1 branch, CI/security workflows, reviewable draft PR, human merge authority.

## Hard stops

Release is HOLD on secrets exposure, unauthorized access, fabricated evidence, critical unresolved security defects, unbounded autonomy, material provenance failure, trust-boundary contamination, missing rollback for consequential change or unverifiable financial state.

## Residual risks

- Agent identity references remain configuration-bound until stronger attestation is deployed.
- P0 Ledger remains local JSONL rather than HA/DR database infrastructure.
- External source quality varies and must be continuously cross-examined.
- HP/Dell actual-host acceptance is still required after CI.
- Gmail/Slack delivery can fail and must never be treated as successful without delivery evidence.