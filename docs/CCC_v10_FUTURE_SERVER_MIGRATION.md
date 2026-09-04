# CCC v10 Future Server Migration

## Current
- `ccc-hp-dev-01`: development, GitHub, Python, dashboard, Sigma/STIX/TAXII, local Ledger/Orchestra
- `ccc-dell-compute-01`: Hyper-V SOC range and live-state producer

## Future
- `ccc-core-01`: Ledger, database, API, Mission Control, Living Intelligence, CI runner
- `ccc-range-01`: SOC, telemetry, honeypot, malware-analysis slot, simulation
- `ccc-pulse-01`: portable/read-only status and approval display

## Migration invariant
`ROLE + CONFIG + TARGET = DEPLOYMENT`

Applications consume role and contract interfaces, not model-specific hardware assumptions. Migration changes host-registry/config deployment targets and validates evidence gates; it does not rewrite the application architecture merely because hardware changes.
