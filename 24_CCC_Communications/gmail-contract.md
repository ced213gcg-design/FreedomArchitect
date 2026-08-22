# Gmail Contract

Gmail is an **external communication channel**, never an institutional truth authority.

## Allowed

- receive opportunity messages
- send approved reports or drafts
- send approved notifications
- record delivery result

Any inbound opportunity is a signal only. Exception Intelligence must verify source, freshness and evidence before elevation.

## Delivery evidence

A send attempt does not equal delivery. Delivery may be recorded only from connector/API evidence.

Failure route:

`EMAIL_FAILED -> LEDGER EVENT -> EXCEPTION ROUTER -> DASHBOARD -> SLACK FALLBACK (if configured) -> HUMAN RESOLUTION`

Never claim delivered when blocked or unverified. Never send secrets, credentials, raw protected evidence, raw financial credentials or unapproved consequential instructions.
