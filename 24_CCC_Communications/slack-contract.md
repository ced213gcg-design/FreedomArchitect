# Slack Contract

Slack is a simulation/review/notification sink, not source of truth.

Suggested channels: `#ccc-orchestra`, `#ccc-build`, `#ccc-simulations`, `#ccc-security`, `#ccc-release`, `#ccc-exceptions`.

Allowed message types: BUILD, TEST, SIMULATION, SECURITY, RELEASE, EXCEPTION, APPROVAL_REQUEST, INCIDENT.

Minimum message fields: `[CCC][TYPE][STATE]`, Repo, Branch, Commit, Run, Organ, Summary, Pressure Loss, Next Action, Evidence Link.

Never send secrets, credentials, customer private data, malware binaries, raw financial credentials, raw protected evidence or arbitrary command payloads. Exception messages are sanitized summaries and must return to GitHub/Ledger/Orchestra for authoritative state.
