# CCC Context Lens Contract

Every meaningful selectable CCC object must answer:

- NAME
- PLAIN FUNCTION
- STATE
- FACT
- RISK
- NEXT ACTION
- OWNER
- SOURCE
- TIME
- VALIDATION
- APPROVAL REQUIREMENT

Raw evidence remains available through progressive disclosure.

## Progressive disclosure

First view prioritizes FACT / STATE / RISK / NEXT ACTION.

Expanded view includes owner, source, time and validation.

Raw evidence view preserves the underlying object payload for operator inspection. The UI must not mutate that evidence to make presentation cleaner.

## Request preview

A consequential-looking action opens a request preview. Confirmation creates a semantic request only. It does not execute the requested infrastructure/test effect.

## Unknown law

If evidence is missing, the Context Lens says UNKNOWN or identifies the missing evidence. It never manufactures green state from configuration presence.
