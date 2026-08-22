# CCC v10.1 Ledger Technology Decision Gate

## Rule

Use the simplest architecture that satisfies trust, audit, settlement, governance, privacy, performance, recovery and economic requirements. Blockchain symbolism is not a requirement.

## Fourteen independent questions

For every financial/evidence use case evaluate: authentication/identity; cryptographic integrity; automated execution; state/database model; replication/distribution; consensus need; settlement/finality; trusted-third-party or escrow alternative; governance; privacy/confidentiality; performance/cost; failure/recovery; legal/contract implications; incentive/mechanism-design consequences.

## Candidate technologies

A relational database; B signed/hash-linked append-only log; C event-sourced database; D replicated trusted-operator DB; E permissioned distributed ledger; F public blockchain; G smart contracts; H ordinary software automation without consensus; I trusted-third-party/escrow.

## P0 evidence decision

For CCC internal evidence there is still no proven multi-party consensus or settlement requirement. v10.1 therefore preserves the hash-linked append-only/event-sourced direction. Re-open the gate only when a factual requirement proves that trusted-operator storage cannot satisfy the trust/finality/governance model.

## v10.1 financial classifier

`classify_financial_state.py` prevents exception/opportunity records from contaminating financial truth:

- pipeline/opportunity != revenue
- contracted claim != collected cash
- invoice/receivable != collected cash
- collected but unreconciled != realized reconciled revenue
- reconciled restricted funds remain restricted
- internal savings/avoided cost remain economic value, not cash receipt
- deployable surplus is a later governed state, not a synonym for revenue

## Monetary taxonomy

Do not collapse central-bank money, commercial-bank deposits/liabilities, cash, securities/assets, certificates/claims, tokens representing claims, accounting entries, exchange balances, ledger representations or settlement assets into the word “money.”
