# CCC Employment Role Router

Last hard-sync: 2026-09-04

## Required Parse

For every verified job capture:
- ROLE_CLASS
- SENIORITY
- MANDATORY_REQUIREMENTS
- PREFERRED_REQUIREMENTS
- TOOLS
- SECURITY_DOMAIN
- CLOUD_REQUIREMENTS
- GRC_REQUIREMENTS
- INCIDENT_RESPONSE_REQUIREMENTS
- DOCUMENTATION_REQUIREMENTS
- MANAGEMENT_REQUIREMENTS
- EXPERIENCE_REQUIREMENT
- EDUCATION_REQUIREMENT
- CERTIFICATIONS
- LOCATION
- REMOTE_STATUS
- COMPENSATION
- SOURCE
- POSTING_ID
- POSTING_DATE
- CLOSING_DATE

## Resume Selection

Use `RESUME_VARIANT_01` for SOC, cybersecurity operations, monitoring, network security, incident-response support, vulnerability analysis, associate security engineering, detection/monitoring support, and security-AI evaluation/training roles.

Use `RESUME_VARIANT_02` for security controls, GRC, risk, compliance, security assessment, cloud-security developmental-fit, and analyst-level security consulting roles.

## Fit Classes

### CLASS A — Direct Current Fit
Priority HIGH:
- SOC Analyst
- Cybersecurity Analyst
- Security Operations
- Network Security
- Security Monitoring
- Incident Response Support
- Vulnerability Analyst
- Associate Security Engineer
- AI Security Training / Evaluation

### CLASS B — Developmental / Stretch Fit
Apply only when mandatory experience does not hard-block, education/experience substitution is allowed, or Human Command directs application:
- Cybersecurity Analyst II
- Security Controls
- GRC
- Cloud Security
- Cybersecurity Consulting — Analyst Level

Missing experience is recorded, never fabricated.

### CLASS C — Senior / Management
Do not prioritize on compensation alone. Verify management experience, production cybersecurity tenure, direct reports, architecture ownership, and certification requirements. Unsupported hard requirements => `STRETCH_BLOCKED`.

## Requirement-to-Evidence Rule

`REQUIREMENT -> CAPABILITY -> EVIDENCE`

Preserve exact employer terminology only when evidence supports it. No keyword stuffing, no unsupported mirroring of the job description.

## External Action Gates

CCC may discover, verify, dedupe, score, select a resume variant, tailor drafts, prepare application answers, track, and reinject requirements.

Hold for Human Command when a new personal fact, legal attestation, salary commitment, background/clearance disclosure, CAPTCHA/MFA/ID verification, human assessment, interview, offer, negotiation, or contract acceptance is required.
