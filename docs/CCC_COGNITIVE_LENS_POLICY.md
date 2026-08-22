# CCC Cognitive Lens Policy

State: **SEED / DEFERRED_P1**

The Cognitive Lens is contextual AI assistance, never authority.

When promoted in a future branch it may explain, compare, research approved sources, generate bounded options, challenge risk, propose next action and summarize evidence.

Required display when active:

- AI STATE
- MODEL / PROVIDER
- COST
- SOURCES USED
- CONFIDENCE
- TOOLS USED
- LEDGER STATUS
- AUTHORITY = ADVISORY

No browser-to-provider credential path is allowed. Provider access must be backend mediated. Secrets, raw credentials, unnecessary private data and entire-repository payloads must not be sent by default.

Model output does not become Ledger truth without schema, provenance and evidence validation. If no evidence supports an answer, the interface must label it `UNVERIFIED MODEL ANALYSIS`.

Provider integration is deliberately not part of the SOC Live P0 hotfix.
