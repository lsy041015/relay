# Claude Code Tool Notes

Skills describe actions in prose. Follow the actual tool list and current
host rules when translating them to Claude Code calls; this document is
guidance, not an API contract.

## One delegated role

The main session keeps the user's selected model and reasoning effort and owns
planning, exploration, diagnosis, review, re-review, integration, and final
verification. A delegated call is for a bounded implementation worker only.
Do not dispatch a reviewer, analyst, planner, explorer, or nested helper.

The worker is the plugin agent `relay:implementer`, whose definition pins
`model: claude-sonnet-5` and `effort: high`. Dispatch it explicitly:

```text
Agent(
  subagent_type="relay:implementer",
  description="Implement task 2",
  prompt="<goal, exact scope, acceptance checks, tests, and report path>"
)
```

Do not pass a `model` override; the agent definition sets Sonnet 5 / high.
The worker starts with no conversation history, so the prompt must be the
complete brief. If the agent type is unavailable, never silently substitute
another agent: continue inline in the main session and report the limit.

## Fixes and lifecycle

Record the worker's agent id/name. When the main agent's review finds a
concrete defect, send the finding to the same worker with `SendMessage`;
include the file, location, failure, acceptance condition, and covering test.
A follow-up is a new implementation turn, not a new review seat. The worker
appends its result and test evidence to the report. The main agent reviews the
actual fix diff again.

If two failed fix attempts have the same root cause, stop retrying. The main
agent changes the diagnosis or plan, or fixes the small issue inline; do not
create a fresh worker merely to obtain different eyes. Explicitly requested
independent parallel implementation is the only exception to the one-worker
default: send multiple `Agent` calls in one message, each `relay:implementer`
with disjoint files and state.

## Waiting and evidence

Agents run in the background by default and notify on completion; do not
poll. Continue useful local work meanwhile. Do not treat an unverified worker
summary as proof: inspect the actual diff, affected call paths, and reported
test output.

## Environment and workspace

Before using worktree or branch operations, use read-only git inspection to
distinguish a linked worktree, an ordinary checkout, and detached HEAD. Apply
`relay:using-git-worktrees` for isolation and preserve unrelated user changes.
Do not delete a workspace or alter a shared branch without authorization.
