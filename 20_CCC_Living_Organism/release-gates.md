# CCC v10 Release Gates

## READY gate

P0 may become READY only when repository inventory, manifest/schema/registry validation, Ledger chain tests, synthetic-vs-real separation, SOC UNKNOWN-on-missing behavior, Pressure Loss, Agent Mesh rejection of unknown agents, required API smoke tests, action-request pending approval behavior, local dashboard render, Canvas fallback, CI, secret scan, rollback documentation, upgrade report, and draft PR are evidenced.

## THRIVE gate

THRIVE is explicitly unavailable during P0. It requires repeated useful runtime output, known failure recovery, maintained trust boundaries, measurable useful output, no protected-data corruption, no critical pressure loss, Ledger/live-state agreement, and reinjection into the next Alpha.

## SCALE gate

SCALE requires THRIVE plus demonstrated capacity, SLO attainment, validated economics, scalable security/data lineage, and tested incident/rollback paths.

## Rule

No state is promoted from file existence, optimistic interpretation, or decorative dashboard status.
