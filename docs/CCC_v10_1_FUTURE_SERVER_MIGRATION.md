# CCC v10.1 Future Server Migration

Current hosts: `ccc-hp-dev-01` and `ccc-dell-compute-01`.

Future roles move to `ccc-core-01`, `ccc-range-01`, and `ccc-pulse-01` without redesigning the application architecture.

`ccc-core-01`: Ledger, database, API, Mission Control, Living Intelligence, Exception Intelligence and CI runner.  
`ccc-range-01`: SOC, telemetry, honeypot, malware-analysis slot and simulation.  
`ccc-pulse-01`: portable telemetry/status, approval display and read-only emergency status.

Deployment law: `ROLE + CONFIG + TARGET = DEPLOYMENT`.

Migration sequence: provision target -> register identity/owner/roles -> apply config -> validate read-only health -> replay non-destructive tests -> verify Ledger lineage -> cut over one role at a time -> retain rollback to previous host until evidence supports retirement.

No hardware purchase or replacement automatically earns a new architecture, and no future host self-registers into the Agent Mesh.
