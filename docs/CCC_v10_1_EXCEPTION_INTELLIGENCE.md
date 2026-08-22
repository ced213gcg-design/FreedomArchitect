# CCC v10.1 Exception Intelligence

## Mission

CCC Exception Intelligence is the permanent sensory-priority organ for signals that deserve elevation above ordinary traffic: uncommon employment/contract/grant/customer opportunities, security/CVE/GitHub failures, market or hardware-price movements, research discoveries, regulatory/financial/infrastructure changes and capability gaps.

It is not an autonomous deal-maker, applicant, trader, incident commander or money mover. It verifies, cross-examines, scores, ages, records and routes evidence.

## Canonical flow

`SIGNAL -> VERIFY -> CROSS-EXAMINE -> SCORE -> LEDGER -> GAME THEORY -> MISSION CONTROL -> ORCHESTRA -> ACTION / HOLD`

A signal does not skip directly from discovery to execution.

## Required record

Each exception carries: `exception_id`, type, title, source, first_seen, last_verified, freshness_state, confidence, strategic_value, time_sensitivity, probability, economic_upside, capability_alignment, reinjection_value, fit_score, exception_score, risk, owner, next_action, approval_required, state and evidence_refs.

## Exception Score

Visible formula:

`0.35*StrategicValue + 0.20*TimeSensitivity + 0.15*Probability + 0.10*EconomicUpside + 0.10*CapabilityAlignment + 0.05*EvidenceConfidence + 0.05*ReinjectionValue`

- 90-100: CRITICAL OPPORTUNITY
- 80-89.999: HIGH PRIORITY
- 70-79.999: QUALIFIED
- 50-69.999: WATCH
- below 50: ARCHIVE / IGNORE

Every component remains inspectable. No opaque 91/100.

## Fit Score

Fit is intentionally separate from Exception Score. For employment, the default evidence categories are Education, Project Experience, Technical Match, Role Competencies, Domain Match, Location/Work Model and Evidence Strength. Each point must map to evidence. A component with no evidence receives zero effective points even if a claimed score is supplied.

## Freshness

Freshness is recalculated from `last_verified` against `config/exception-policy.yaml`. States are VERIFIED, AGING, STALE, CLOSED and SUPERSEDED. Security/GitHub/CVE signals use shorter windows than ordinary opportunities. A stale exception cannot remain in the high-priority queue regardless of its old score.

## Routing

- stale/closed/superseded -> HOLD
- critical/high SECURITY/CVE/GITHUB_FAILURE/INFRASTRUCTURE -> Mission Control security priority
- verified score >=80 -> Mission Control high-priority
- score >=70 -> Orchestra qualified queue
- score >=50 -> Exception Intelligence watch
- below 50 -> archive

Security/Trust/Ledger/SRE/SOC failures override commercial optimization.

## Reverse-learning loop

`EXTERNAL REQUIREMENT -> CAPABILITY GAP -> CCC LAB / PROJECT -> EVIDENCE -> REPORT -> GITHUB PORTFOLIO -> APPLICATION / RESPONSE -> RESULT -> LEDGER -> REINJECTION`

A lost opportunity may still be economically useful if it leaves reusable capability and evidence.

## Privacy

The public exception adapter uses an allowlist. It does not expose applicant/customer contact details, credentials, tokens, passwords or raw financial credentials. Evidence is referenced, not dumped into the public visualization.

## Financial boundary

An opportunity score is not revenue. A contract is not collected revenue. An invoice is not collected revenue. Restricted funding is not unrestricted cash. Internal savings are economic value, not cash receipts. Exception Intelligence may elevate a financial or commercial signal but cannot promote it into realized revenue; that remains Ledger + Revenue Assurance territory.

## Closure

Exception outcomes must ultimately preserve the lesson as WON, LOST, DECLINED, EXPIRED, SUPERSEDED or HOLD, then reinject useful capability/evidence rather than leaving immortal green opportunities cluttering the institution forever.
