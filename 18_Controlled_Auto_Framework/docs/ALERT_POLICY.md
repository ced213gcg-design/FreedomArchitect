# Alert Policy

## Alert Types

### INFO
Normal operation, no action needed.

### REVIEW
Something is usable but should be reviewed.
Options:
- EDIT
- REVISE
- APPROVE
- HOLD

### ACTION
High-value target or urgent task requires timely execution.

### FAULT
System mismatch, weak output, or blocked release.

## Alert Payload Standard
Every alert should contain:
- summary
- reason
- confidence level
- affected role
- recommended next action
- options: EDIT / REVISE / APPROVE / HOLD
