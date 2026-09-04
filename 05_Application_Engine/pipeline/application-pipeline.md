# CCC Employment Application Pipeline

## State Model
`DISCOVERED -> PRIMARY_VERIFIED -> ROLE_TWIN_READY -> RESUME_READY -> APPLICATION_READY -> EXTERNAL_GATE -> SUBMITTED -> ENGAGEMENT -> INTERVIEW -> OFFER -> EMPLOYED`

A state may advance only when its evidence exists. No inferred submissions, interviews, offers, or compensation.

## Application Ledger

| Job ID | Employer | Role | Source | Posting ID | Remote Status | Fit Class | Resume Variant | Derivative Version | JD Hash | Supported | Unsupported / Gaps | Evidence Refs | Application State | Submission Ref | Follow-Up | Notes |
|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|
| HHSC-20848 | Texas Health and Human Services Commission | Cybersecurity Analyst II | Primary employer source | 20848 | Onsite - Austin | B / Conditional Stretch | VARIANT_02 | Pending | Pending | Controls/risk/vulnerability/documentation fundamentals | 3+ years information-security analysis; production cloud/GRC experience not claimed | `verified-targets-2026-09-04.md` | STRETCH_REVIEW | None | None | Primary posting verified; no false experience substitution |
| CROWDSTRIKE-R26320 | CrowdStrike | Associate Security Engineer (Remote) | Primary employer source | R26320 | Remote - TX/USA | A / High Priority Review | VARIANT_01 | v1 created 2026-09-04 | Pending | SOC/log analysis, network/host analysis, scripting, documentation, authorized lab evidence | Exact employer stack experience must remain evidence-qualified | `remote-targets-2026-09-04.md` | RESUME_READY | None | None | Lab experience explicitly accepted by employer language; submission not recorded |

## Mandatory Version Fields
For every released derivative preserve:
- JOB_ID
- RESUME_VARIANT
- DERIVATIVE_VERSION
- JOB_DESCRIPTION_HASH
- CREATED_AT
- ATS_KEYWORDS_USED
- SUPPORTED_REQUIREMENTS
- UNSUPPORTED_REQUIREMENTS
- EVIDENCE_REFERENCES
- FINAL_FILE_HASH
- SUBMISSION_REFERENCE

## Truth Controls
- Job-board listing != primary-source fact.
- Recruiter claim != employer fact.
- Salary listing != offer.
- Applied != submitted unless a receipt/reference exists.
- Lab capability != production employment.
- Missing requirement != permission to fabricate.
