# KEYCHAIN GATE AUTHORITY

## Purpose
Provide a secure, auditable access map without storing secret values or private doctrine in this public repository.

## Public Repository Rule
Repository files may contain credential names, purposes, storage locations, and verification state. They must never contain passwords, API keys, private tokens, recovery codes, private keys, seed phrases, session cookies, or private doctrine text.

## Storage Order
1. OS/native secure credential store when available.
2. Provider secret store such as GitHub Actions Secrets for automation-specific credentials.
3. Local user-only environment/config storage only when required, with least privilege and restrictive permissions.
4. Never commit raw secrets to Git.

## Logical Credential Manifest
- `OPENAI_API_KEY`
- `GITHUB_AUTH`
- `GOOGLE_DRIVE_AUTH`
- `GMAIL_AUTH`
- `CALENDAR_AUTH`
- future service credentials explicitly approved by Human Command

Presence reporting is limited to `PRESENT`, `MISSING`, `REVIEW`, or `UNKNOWN`.

## Gate Algorithm
1. Confirm intended service and scope.
2. Confirm storage backend.
3. Confirm credential presence without displaying the value.
4. Confirm least-privilege permissions.
5. Confirm no secret is tracked by Git.
6. Perform a harmless read-only authentication check where practical.
7. Record evidence timestamp locally.
8. Mark KEYCHAIN_LOCK `PASS` only when all required credentials pass.

## Gate States
- `PASS` — secure presence and access verified.
- `REVIEW` — present but scope/storage needs review.
- `HOLD` — missing, unsafe, exposed, or blocked.
- `UNKNOWN` — not checked.

## Exposure Response
If any secret is found in repository history or a displayed file, treat it as compromised, rotate/revoke it, remove active exposure, verify the replacement, and record the incident without recording the secret itself.

## Authority
Unc's World manages the process. Human Command controls credential issuance, rotation, provider authorization, and destructive/revocation actions unless explicitly delegated.
