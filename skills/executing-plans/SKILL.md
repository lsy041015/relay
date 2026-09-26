---
name: executing-plans
description: Use when an approved implementation plan should be executed in the current session without delegated task workers
---

# Executing Plans

Execute an approved plan inline when the user chose that path, the change is
small, or delegation is unavailable. The main agent performs the implementation,
review, re-review, and final verification in this session. This skill has no
fresh-reviewer branch.

## Setup

Outside Git, use the approved working directory, brief, progress file, and
before/after file comparisons. Skip Git-only helpers; do not create a
repository or commits just for workflow bookkeeping.

1. Verify the approved plan, repository instructions, worktree, branch, and
   current user changes. Use `relay:using-git-worktrees` when
   isolation is required; never erase unrelated edits.
2. Resolve the plan workspace with
   `relay:subagent-driven-development`'s
   `scripts/sdd-workspace PLAN_FILE` and resume its ledger only when it names
   this plan. Record a fresh ledger identity otherwise.
3. Read the plan and spec once, scan shared interfaces and task consistency,
   and record every plan ruling before changing code.
4. Load `relay:test-driven-development` before Task 1 and
   apply `relay:verification-before-completion` before any
   completion claim.

## Task loop

For each task, read its brief and exact expected output. Work in the plan's
order and keep the change at the stated scope.

- For behavior changes, write and run the failing test first, make the
  smallest implementation pass, then refactor only when the green test
  protects behavior.
- For a command with an `Expected:` line, apply
  `relay:verification-before-completion`: inspect matching
  evidence or execute the complete command and compare its output to the
  expectation. If code is wrong, use
  `relay:systematic-debugging`; if the plan is wrong, record
  a main-agent `Ruling:` and continue with the smallest spec-consistent change.
- Keep focused tests near the task and run the task's final verification before
  marking it complete. Record the command, result, and relevant evidence in
  the ledger. Commit only when the plan or repository workflow requires it.

Do not stop between tasks to ask whether to continue. Stop for an irreversible
or security-sensitive operation, an external side effect requiring approval,
or a plan so broken that every path is a guess. Ask the user only when the
missing decision changes the requested outcome.

## Inline review

After each task, inspect the actual diff against the task brief and tests:
requirements, scope, callers, error paths, security, data loss,
accessibility, calibration, hardware safety, and preservation of user changes.
Use `relay:requesting-code-review` and its worksheet as a
checklist, but do the review yourself. If a finding needs code changes, write
the covering test, observe RED, fix it, observe GREEN, and run the relevant
suite. Do not create a reviewer or an implementation child from this mode.

## Final verification

Review the whole branch from its merge base and all staged, unstaged, and
untracked task changes. For entirely uncommitted work, inspect those changes
directly; no review-only commit is needed. Reconcile ledger Rulings and
deferred Minors, then apply
`relay:verification-before-completion` to reuse matching
verification evidence or run the affected complete commands after the last
change. Report commands and real output, including environment limits or
unresolved findings. Integrate through
`relay:finishing-a-development-branch` only after the user
has the required choices. Preserve plan artifacts until the handoff is
complete.
