---
name: subagent-driven-development
description: Use when an approved implementation plan has a clear unit that can be delegated to an implementation worker
---

# Subagent-Driven Development

Use this workflow when a plan has a bounded implementation result that is
worth delegating. Astra remains the controller: it decides scope, reads the
plan, reviews every change, and integrates the result. Luna is an
implementation worker, not a second controller.

Use `superpowers-astra-luna:executing-plans` when the user chose inline work,
the change is tiny, or the host has no usable worker tool. Use
`superpowers-astra-luna:dispatching-parallel-agents` only for explicitly
requested independent parallel implementation.

## Invariants

- The main session stays on `gpt-6-astra` and keeps its selected effort.
- Every worker creation explicitly sets `model = "gpt-5.6-luna"`,
  `reasoning_effort = "xhigh"`, and `fork_turns = "none"`.
- Workers never spawn workers, reviewers, analysts, planners, or helpers. They
  may self-review their diff and investigate implementation failures as part
  of the assigned task.
- Astra performs task review and re-review from the actual diff and test
  evidence. Do not create a separate review agent or claim independent review.
- Reuse one worker for related tasks and fixes. After two failed fix attempts with
  the same root cause, Astra changes the diagnosis or takes the work inline;
  there is no model escalation or fresh-worker rescue path.
- TDD, systematic debugging, verification-before-completion, user-change
  preservation, and safety requirements remain in force.

## Setup and recovery

For Git repositories, use the steps below. For work outside Git, use the
approved staging directory, brief, progress file, and before/after file
comparison instead; the Git helpers do not apply. Do not initialize a
repository or create commits merely to satisfy workflow bookkeeping.

1. Confirm the approved plan and its Global Constraints. Use
   `superpowers-astra-luna:using-git-worktrees` to create or verify an
   isolated workspace; never assume a clean baseline.
2. Resolve this plan's workspace with `scripts/sdd-workspace PLAN_FILE` and
   use its `progress.md` ledger. A ledger for another plan, or the old flat
   ledger, belongs to another run. The first line must identify this plan.
3. Read the plan once. Scan task boundaries for shared files, interfaces,
   contradictory requirements, and tests that do not exercise the stated
   behavior. Record the table and any `Ruling:` decisions in the ledger.
4. Create the task checklist. Record the task's BASE commit before dispatch;
   use `scripts/task-brief PLAN_FILE N` so the worker receives a focused brief,
   never the whole plan history. New plans use `### Task N: title` with a
   positive integer and lower-level subheadings; the extractor preserves
   older valid `Task N` headings for compatibility.

The ledger is the recovery map after compaction. Do not redo a task with a
`Task N: complete` line. Preserve the workspace and unrelated user changes.
Do not run destructive cleanup, merge, push, publish, or hardware motion
outside the user's authorized scope.

## Task loop

### 1. Choose the execution path

Keep a one-file mechanical edit, lookup, or short verification in Astra. For a
clear multi-step implementation result, dispatch one Luna worker using
`implementer-prompt.md`. The brief must contain only the goal, acceptance
conditions, exact allowed files, interfaces and settled decisions, tests,
required source paths, and report path. The worker receives no inherited
history and no authority to widen scope.

Batch same-shape edits only when one worker can review them as one coherent
result. Do not dispatch parallel workers for overlapping files or shared
mutable state.

### 2. Worker contract

The worker reads the brief, follows TDD when the task changes behavior, edits
only the allowed scope, runs focused and required verification, self-reviews
its diff, and commits only when the plan asks for commits. It reports:

```text
Status: DONE | BLOCKED | NEEDS_DECISION
Changed files: <paths>
Tests: <commands, exit codes, relevant results>
Unresolved: <none or concrete issues>
Report: <absolute report path>
```

The detailed report keeps full test output and, when applicable, RED/GREEN
evidence. The short response is not a substitute for the report or the diff.

`BLOCKED` or `NEEDS_DECISION` means Astra supplies missing context or decides
the plan change. It does not trigger a different model. If two fix attempts
fail for the same root cause, Astra records the failure and replans or
implements directly.

### 3. Astra review

After a `DONE` result, Astra runs `scripts/review-package PLAN_FILE BASE HEAD`
when the task has a committed range and reads the actual package. Also inspect
all working-tree changes, even when commits exist: `git diff --cached`, `git diff`, and
`git ls-files --others --exclude-standard`, then read each untracked file that
belongs to the task. Review the staged, unstaged, and untracked changes as one
actual change set. When BASE equals HEAD, skip the commit-only helper; do not
create a dummy commit. Review requirements and quality together:

- every acceptance condition and listed file is present;
- no extra behavior, scope creep, or hidden worker-generated delegation;
- call paths, error handling, security, accessibility, calibration, and user
  changes remain safe;
- tests exercise behavior and the worker's reported commands and output are
  real and sufficient;
- the implementation is understandable and no simpler existing path was
  unnecessarily replaced.

Use the task review worksheet in `task-reviewer-prompt.md` as a checklist. It
is an Astra worksheet; do not dispatch it. Record the verdict and any Minor
finding in the ledger. A Critical or Important finding, a real spec gap, or a
requirement that cannot be verified enters the fix loop.

### 4. Fix loop

Send concrete findings to the same worker with `followup_task`, using
`re-review-prompt.md` to define the scope. The worker appends a fix report,
runs the covering tests, and returns the same status contract. Astra reads the
fix diff and re-reviews only the findings and touched code. New findings in the
fix diff join the list; unrelated observations go in the ledger.

After two failed fix attempts with the same root cause, stop the loop and write an
Astra `Ruling:`. Change the plan or implement the smallest safe correction
inline. Count post-review fix attempts; the initial implementation is not a
fix round. Never dispatch a fresh implementer or a higher-tier child as a retry.

When the task is clean, record:

```text
Task N: complete (range <base>..<head> or workspace changes, review clean,
tests: <command> → <result>)
```

Only then move to the next task. Preserve deferred Minor findings and all
Rulings for the final review.

## Final review and completion

After all tasks, Astra creates one whole-branch review package from the branch
merge base when there is a committed range and reviews it with
`requesting-code-review/code-reviewer.md` as a checklist. Always also inspect
staged and unstaged diffs plus untracked task files directly. If the work is
entirely uncommitted, skip the commit-only helper; do not force a dummy commit.
No final reviewer is created.
Astra applies `superpowers-astra-luna:verification-before-completion` to the
required final checks and the combined state. Check every ledger Ruling and
deferred Minor, and record any final fix. A remaining Critical or Important
issue is either corrected inline or sent as a concrete follow-up to the
existing Luna worker; Astra re-reviews the actual fix. There is no second
review agent or unlimited fix cycle.

Report verification evidence, failures, and environment limits.
Use `superpowers-astra-luna:finishing-a-development-branch` only after the
requested integration decision is ready. Never delete the plan workspace
until the ledger and required artifacts are preserved or the user authorized
the cleanup.

## Example handoff

```text
Task 2: add retry behavior
Brief: /workspace/.superpowers/sdd/retry/task-2-brief.md
Allowed files: src/retry.ts, test/retry.test.ts
Acceptance: bounded retries, abort preserved, focused test command
Worker: gpt-5.6-luna / xhigh / fork_turns=none
Report: /workspace/.superpowers/sdd/retry/task-2-report.md
```

Internal skill links use the `superpowers-astra-luna:` namespace.
