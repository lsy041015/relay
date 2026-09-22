# Codex Tool Notes

Skills describe actions in prose. Follow the actual tool list and current
host rules when translating them to Codex calls; this document is guidance,
not an API contract.

## One delegated role

The main Astra session owns planning, exploration, diagnosis, review,
re-review, integration, and final verification. A delegated call is for a
bounded implementation worker only. Do not dispatch a reviewer, analyst,
planner, explorer, or nested helper.

When the work is a clear implementation unit, make the dispatch explicit:

```text
spawn_agent(
  task_name="implementation_task_2",
  message="<goal, exact scope, acceptance checks, tests, and report path>",
  model="gpt-5.6-luna",
  reasoning_effort="xhigh",
  fork_turns="none"
)
```

`fork_turns = "none"` keeps the worker's context limited to the explicit
brief. It does not promise zero setup cost or remove system and tool rules.
The creation call's required settings are exactly `model =
"gpt-5.6-luna"`, `reasoning_effort = "xhigh"`, and `fork_turns = "none"`.
Never omit the model or effort when dispatching this role, and never silently
substitute another model if the requested preset is unavailable. Tell Astra
that the requested work cannot be delegated and continue inline when possible.

## Fixes and lifecycle

Record the worker id. When Astra's review finds a concrete defect, send the
finding to the same worker with `followup_task`; include the file, location,
failure, acceptance condition, and covering test. `followup_task` addresses the
existing worker; do not pass model, effort, or fork settings to that follow-up.
A follow-up is a new implementation turn, not a new review seat. The worker
appends its result and test evidence to the report. Astra reviews the actual
fix diff again.

If two failed fix attempts have the same root cause, stop retrying. Astra changes
the diagnosis or plan, or fixes the small issue inline;
do not promote the worker or create a fresh one merely to obtain different
eyes. Explicitly requested independent parallel implementation is the only
exception to the one-worker default, and each worker gets the same Luna/xhigh
settings with disjoint files and state.

## Waiting and evidence

Use the host's event wait for a running worker rather than short polling.
While Astra has useful local work, continue it; when idle, use one bounded wait
and reconcile the worker's report. Do not treat an unverified worker summary
as proof: inspect the actual diff, affected call paths, and reported test
output. Keep full logs in a file when they are large and summarize only the
relevant evidence.

## Environment and workspace

Before using worktree or branch operations, use read-only git inspection to
distinguish a linked worktree, an ordinary checkout, and detached HEAD. Apply
`superpowers-astra-luna:using-git-worktrees` for isolation and preserve
unrelated user changes. Do not delete a workspace or alter a shared branch
without the authorization required by the host and the user request.

When the Codex app owns an externally managed checkout, finish with the app's
native integration controls and report the exact state. Do not invent push,
merge, or publish operations.
