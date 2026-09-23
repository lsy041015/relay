---
name: dispatching-parallel-agents
description: Use only when the user explicitly requests independent implementation work that can run concurrently without shared state
---

# Dispatching Parallel Agents

Parallel dispatch is an exception to the one-worker default. It is permitted
only when the user explicitly asks for parallel implementation and each unit
has disjoint files, interfaces, fixtures, and mutable state. The main agent first
confirms those boundaries; otherwise work sequentially or inline.

Do not use this skill for exploration, planning, diagnosis, test triage,
review, re-review, or a second opinion. Those remain in the main session.
A worker may not dispatch its own children.

## Dispatch contract

For every independent unit, provide a separate brief with its exact goal,
allowed files, settled interfaces, acceptance checks, tests, and report path.
Every call explicitly uses `gpt-6-luna`, `reasoning_effort = "xhigh"`, and
`fork_turns = "none"`. Make the calls concurrently only after confirming no
write or state dependency can overlap.

When all workers return, the main agent reads every actual diff and report, checks for
overlap and integration conflicts, and applies
`superpowers-astra-luna:verification-before-completion` to the combined
state. Reuse a matching result only when its command, scope, environment, exit
code, and actual log still apply; otherwise run the affected integration
verification. Worker reports are evidence, not approval. Send a concrete fix to the same
worker with `followup_task` when possible; do not create a reviewer or a fresh
fixer. If two failed fix attempts have the same root cause, the main agent stops retrying,
records a Ruling, and changes the plan or fixes inline.

## Boundary checklist

- Files and generated artifacts are disjoint.
- No worker changes a shared config, lockfile, schema, API, or test fixture.
- Each worker can test its result without another worker's uncommitted state.
- Integration order and any merge conflict resolution are known to the main agent.
- Hardware, calibration, permissions, and external side effects remain under
  the main agent's review and the user's existing authorization.

If any answer is uncertain, do not parallelize. Use one worker or execute in
the main session. Internal references use the
`superpowers-astra-luna:` namespace.
