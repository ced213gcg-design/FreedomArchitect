# LIL CED — FULL ALPHA CURRENT SPEC v0.8
**Status:** ADOPTED BY HUMAN COMMAND
**Date:** 2026-09-30
**Scope:** HP Chromebook / penguin Crostini only
**Source lineage:** Human-supplied `LIL_CED_FULL_ALPHA_DRAFT_v0.7.pdf`, adopted in full by explicit Human Command: “ADOPT ALL!!! INTEGRATE AND ADOPT ALL!!”
**ChatGPT dependency:** NONE by architecture. ChatGPT may assist development, but Lil Ced must run independently.
**Dell:** OUT OF SCOPE. No Dell paths, credentials, procedures, holds, lanes, or tests belong to the Lil Ced build.

## 1. Adopted alpha defaults
- Host target: HP Chromebook, penguin Crostini container, expected Linux user `ced213gcg`; Phase A re-observes before relying on it.
- Cabinet: `/home/ced213gcg/CCC_FILING_CABINET`; missing path = HOLD.
- Off-container backup: ChromeOS Files copy of `14_LIL_CED` to Drive or USB folder `LILCED_BACKUP`; container-only copy is not backup.
- Git: local Git permitted in alpha; push forbidden in alpha; remote may be named later; push remains consequential.
- Free RAM gate: refuse install below 400 MiB available; re-observe, never reuse a stale number.
- Free disk gate: refuse install below 2 GiB free; alpha core budget <= 1.5 GiB.
- Docker: must remain absent through alpha.
- Generation-1 trait: `/status` with no API key, cold start, exit 0, under 2 seconds.
- Sample: 5 cold starts. `h^2 = cold_passes / 5`. Fewer than 5 leaves reliability UNKNOWN.
- Revert rule: any cold-start failure reverts the candidate. A warm/session pass does not substitute.
- Scorer: Human Command reads the receipt. Lil Ced may not self-PASS.
- Spend cap: USD 0.25 per task, USD 2.00 per day, one in-flight model call.
- Model: Anthropic Claude; current Sonnet model ID pinned on install day. No OpenAI key.
- Secret file: `~/.config/lilced/secrets.env`, mode 0600, gitignored, never copied to cabinet, memory, logs, or receipts.
- MIT gate ON for pricing, token, settlement, custody, marketplace rules, or proposed blockchain/chain design. Blank worksheet fields HOLD.
- MIT gate OFF for status, hashing, launcher work, cabinet filing, and ordinary drafting. It must remain off and that behavior is tested.
- Approval syntax: `APPROVE <task_id>` or `DENY <task_id>`. Silence = deny.
- Workspace: `/home/ced213gcg/LilCed/workspace`; writes outside = HOLD.
- Read roots: workspace, cabinet, and non-secret files under `~/.config/lilced`; HOME is not a blanket read root.
- `/shell`: disabled in alpha. No hidden bash fallback.
- Lid close: checkpoint and stop; accepted. This HP is not represented as a 24/7 host.
- Closed alpha lanes: Letta, Open Interpreter, Goose, OpenHands, CrewAI, Microsoft Agent Framework, n8n, Hermes, OpenClaw, voice, HUD, local LLM.
- CLOSED is a valid alpha state, not a failure.

## 2. Canonical architecture
One small core owns flow. Other frameworks remain registered but closed until separately activated after alpha.

```text
HUMAN COMMAND
    |
    +-- Lil Ced Terminal (private operator client)
    |      |
    |      +-- local UNIX socket, mode 0600
    |
    +-- lilced-core
           |
           +-- load current Lil Ced spec
           +-- load SYSTEM_POLICY_CURRENT
           +-- verify MY_OG_CCC_BRAIN hash for material CCC work
           +-- LangGraph in-process state flow
           |      PRECHECK -> AUTHORITY -> EVIDENCE -> PLAN
           |      -> MIT_GATE_IF_TRIGGERED -> HUMAN_GATE
           |      -> EXECUTE -> VERIFY -> RECEIPT -> REINJECT / HOLD
           |
           +-- Markdown identity/doctrine/lessons
           +-- SQLite runtime/task state with TTL
           +-- one Anthropic model adapter
           +-- four alpha tools:
                  read | workspace-write | hash | status
```

No adapter, model, worker, or framework can promote its own output to authoritative PASS.

## 3. MIT Blockchain + Game Theory / Mechanism Design gate
The MIT analytical layer is not decorative. It is an execution gate for economic/mechanism work.

Trigger categories:
- pricing;
- tokens or digital assets;
- settlement;
- custody;
- marketplace rules;
- incentive systems;
- ledger design;
- proposed blockchain/chain use;
- economic mechanism changes.

Required worksheet:
1. Players / principals / agents.
2. Objectives of each player.
3. Information available to each player; identify private/asymmetric/UNKNOWN information.
4. Available actions.
5. Payoffs: money, time, access, control, security, reputation, opportunity, risk.
6. Incentives created by the mechanism.
7. Incentive compatibility: does truthful/compliant behavior remain rational?
8. Strategic failure: deception, defection, collusion, free-riding, Sybil behavior, principal-agent conflict, metric gaming.
9. Enforcement and authority.
10. Settlement and finality.
11. Recovery/dispute path.
12. Evidence required for closure.
13. Blockchain necessity test, default = NO.
14. Human authority boundary.

Blockchain necessity test asks:
- Is there a real multi-party trust/coordination problem?
- Are there multiple writers or counterparties?
- Is shared state necessary?
- Is tamper-evident history insufficient without consensus?
- Is public verification actually needed?
- Is programmable settlement required?
- Do costs, privacy, throughput, finality, custody, governance, oracle, tax, legal, and regulatory burdens justify the chain?

If NO, use ordinary Git, signed append-only ledger, SQLite/database, or receipts.
Blockchain is not a prestige feature.
MIT/game-theory research informs reasoning; current law, regulators, contracts, tax/accounting authority, and actual evidence govern real-world compliance.

## 4. Generation-1 selection/reliability mechanism
`P = A + E + e`
`R = h^2 * S`

Generation 1 measures only the `/status` cold-start trait.
- `h^2 = cold_passes / 5`.
- `S` is not meaningful until all five cold-start observations exist.
- Less than five samples => `R = UNKNOWN`.
- Any cold-start failure => candidate reverts.
- Human Command is the scorer through receipts; Lil Ced cannot award itself PASS.

The mechanism worksheet runs only on MIT-trigger categories.
If a worksheet is opened, authorized, paid, settled, and reconciled are separate states and may never be collapsed.

## 5. Alpha build blocks
### Block A — Re-observe, no install
Run:
```bash
whoami
pwd
free -h
df -h ~
swapon --show
command -v docker || echo DOCKER_ABSENT
test -d /home/ced213gcg/CCC_FILING_CABINET && echo CABINET_PRESENT || echo CABINET_MISSING
```
HOLD if:
- user differs from expected and is not reconciled;
- available RAM < 400 MiB;
- free disk < 2 GiB;
- Docker is present;
- cabinet is missing.
Store raw output in `01_BASELINE_AND_INVENTORY`.

### Block B — Cabinet drawers and launchers, no venv
Create under `CCC_FILING_CABINET/14_LIL_CED/`:
```text
00_PLAN_AND_APPROVAL
01_BASELINE_AND_INVENTORY
02_ARCHITECTURE
03_MIT_GATE
04_SOURCE_AND_DEPENDENCIES
05_INSTALL_AND_CONFIG
06_MEMORY_AND_IDENTITY
07_MCP_AND_TOOLS
08_LANES_REGISTERED
09_SECURITY_AND_SECRETS
10_TESTS_AND_REGRESSIONS
11_RECEIPTS_AND_HASHES
12_RELEASES_AND_ROLLBACKS
13_INCIDENTS_AND_LESSONS
14_HUMAN_CORRECTIONS
15_ECONOMIC_MODELS
```
Create ChromeOS/Crostini launchers:
- CCC Filing Cabinet -> cabinet path
- Lil Ced Terminal -> reports `CORE_OFFLINE` until core exists; must not open bash.
Create off-container `LILCED_BACKUP` via ChromeOS Files.

### Block C — Skeleton, no model
Create:
```text
~/LilCed/app
~/LilCed/workspace
~/LilCed/tests
~/.config/lilced
~/.local/share/lilced
~/.local/state/lilced
```
- Create `~/.config/lilced/secrets.env` mode 0600.
- Use isolated venv; never replace system Python.
- Add `systemd --user` unit `lilced-core.service`.
- Socket: `~/.local/state/lilced/lilced.sock`, mode 0600.
- `/status` with empty secrets must exit 0 in under 2 seconds.
- If core is down, terminal prints `CORE_OFFLINE`; no hidden shell.

### Block D — Memory
Create:
- `~/LilCed/app/memory/identity.md`
- `~/LilCed/app/memory/brain.lock`
- `~/LilCed/app/memory/facts/`
- `~/LilCed/app/memory/lessons/`
- `~/.local/state/lilced/state.db`

Rules:
- `brain.lock` records OG CCC Brain hash for material CCC work; mismatch => HOLD.
- facts require date + evidence path.
- lessons are append-only.
- runtime state has TTL and never becomes doctrine by itself.
- Human Command can inspect and correct durable memory outside Lil Ced.

### Block E — MIT gate, no model
Create `03_MIT_GATE/worksheet.md`.
Tests:
1. Hash an ordinary draft. MIT gate stays OFF.
2. Worker can benefit from marking a pricing task complete without evidence. MIT gate triggers and HOLDs until worksheet/evidence close the incentive defect.

### Block F — One model, four tools, then CUT
- Pin model ID on install day in `04_SOURCE_AND_DEPENDENCIES`.
- Tools: read, workspace-write, hash, status.
- Deny alpha: send, push, publish, delete, sudo, unregistered MCP, and any unapproved privileged/system action.
- Run five cold starts of `/status` with API key unset.
- Calculate `h^2`; any failure => revert; fewer than five => reliability UNKNOWN.
- Receipt includes task_id, UTC timestamps, quoted objective, cold-start score, reliability state, final_state, next_action, lesson path.

## 6. Alpha stop line
Alpha is accepted only when all are true:
- Block A has fresh measurements.
- Lil Ced drawers exist.
- Main-screen launchers exist.
- Off-container `LILCED_BACKUP` exists.
- `/status` passes five cold starts with no API key.
- MIT OFF test passes for ordinary hash/draft work.
- MIT ON/HOLD test passes for incentive-sensitive pricing case.
- Unapproved action receives DENIED and a receipt.
- Memory and receipts survive restart.
- No live secret appears in Git, cabinet, memory, logs, or receipts.
- Closed lanes remain CLOSED and unloaded.
- No unrun test is promoted to PASS.

## 7. Post-alpha framework registry
These are adopted into Lil Ced's roadmap, but not installed or resident in alpha:
- Letta: later memory experiment; never outranks human-readable file memory.
- Open Interpreter: later workspace-scoped adapter; never full-access executor.
- Goose: later MCP discovery/recipe adapter; cannot self-install extensions.
- OpenHands: later coding lane; worktree/diff/test/checker receipt required.
- CrewAI: later role-based worker team; maker != checker.
- Microsoft Agent Framework: later enterprise adapter when a real workload exists.
- n8n: later workflow engine if host/off-host capacity supports it.
- Hermes: preferred later messaging gateway with allowlisted senders.
- OpenClaw: compatibility/import-export patterns; never sovereign brain.
- Voice/HUD: later interface lane after core inspectability.
- Local LLM: closed on this HP; off-host only unless hardware materially changes.

## 8. Receipts, evidence, and reinjection
Each material task receipt records:
- task_id;
- UTC start/end;
- quoted Human objective;
- authority;
- brain hash / policy commit for material CCC work;
- MIT gate status and worksheet path when triggered;
- tools used;
- proposed actions;
- approvals/denials;
- files changed + readback SHA-256;
- final state: PASS / FAIL / HOLD / UNKNOWN;
- next action;
- lesson path.

Corrections supersede; they never erase source history.
Verified faults become regression guards.
Lessons reinject through My OG CCC Brain / MIF-3 lineage as appropriate.

## 9. Authority
Human Command is final consequential authority.
FACT BEFORE CLAIM.
UNKNOWN != PASS.
EXECUTED != VERIFIED.
DOCUMENTED != DEPLOYED.
AUTHORIZED != EXECUTED.
PAID != SETTLED.
SETTLED != RECONCILED.

This v0.8 spec is ADOPTED. It supersedes the approval status of v0.7 while preserving v0.7 as source lineage.
