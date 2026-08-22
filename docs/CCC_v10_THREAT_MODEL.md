# CCC v10 Threat Model

## Protected assets
- source and release history
- Ledger evidence integrity
- agent identities and revocation state
- SOC live-state telemetry
- financial classifications and reconciled data
- human approval authority

## Primary threats
1. **Authority confusion:** a dashboard, Slack message, or agent capability is mistaken for approval.
2. **Evidence forgery:** stale or synthetic data is presented as verified operational truth.
3. **Credential exposure:** tokens, passwords, keys, or webhooks enter source, logs, or notifications.
4. **Agent impersonation / unregistered actor:** an unknown process attempts to submit events or actions.
5. **Privilege expansion:** a read-only component gains execution capability without policy change.
6. **Ledger tampering:** event history is rewritten, reordered, or detached from its hash chain.
7. **SOC boundary escape:** isolated lab activity is directed at unauthorized third-party systems.
8. **Supply-chain compromise:** dependencies or Actions introduce unreviewed code.
9. **Availability failure:** dashboard, Ledger, or SOC state disappears and UI falsely remains green.
10. **Commercial pressure overriding controls:** revenue urgency bypasses Trust/Ledger/SRE/SOC gates.

## P0 controls
- default deny Agent Mesh policy and no self-registration
- explicit allow/deny action lists and revocation state
- append-only hash-linked Ledger verification
- SOC adapter maps missing evidence to UNKNOWN
- action endpoint creates `pending_approval`, never direct consequential execution
- secrets prohibited from repository/Slack contracts
- branch + PR workflow; no direct main development
- JSON Schema validation and CI tests
- Imagination Station excluded from the mesh

## Residual risk
P0 does not yet provide hardware-backed identities, production secret management, remote attestation, a production database, or tested disaster recovery. Those capabilities remain VERIFY/HOLD until implemented and evidenced.
