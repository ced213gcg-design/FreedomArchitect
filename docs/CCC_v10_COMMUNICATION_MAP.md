# CCC v10 Communication Map

| Source | Target | Purpose | Authority | Data rule |
|---|---|---|---|---|
| GitHub | Codex | scoped implementation/repair | code context | branch/issue/PR scoped |
| GitHub Actions | Ledger | build/test/security evidence | evidence input | sanitized machine-readable summary |
| GitHub Actions | Slack | notification | non-authoritative | no secrets/raw protected evidence |
| Dell SOC state | Dashboard/SOC adapter | runtime telemetry | live input | read-only, contract-validated |
| Dashboard | Ledger | action request evidence | request only | pending approval, no direct action |
| Ledger | Orchestra | verified lineage/state | factual authority | append-only/hash-linked |
| Orchestra | Dashboard | pressure loss/release evaluation | integration/release evaluation | explicit evidence basis |
| Orchestra | Engineering/Codex | defect return | scoped repair | exact defect and path |
| Slack | Human | review/notification | non-authoritative | cannot execute shell or control nodes |

Imagination Station is outside this map and receives no CCC mesh backchannel.
