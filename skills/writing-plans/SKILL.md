---
name: writing-plans
description: "Use when a settled design needs multiple verifiable implementation steps. Skip ceremonial plans for obvious small changes."
---

# Writing Plans

Write the plan for the engineer who must implement it after context has been
compressed. The approved spec is the authority; the plan records how the
repository will satisfy it. The main agent writes and reviews the plan. There is no
plan-reviewer dispatch.

## Before writing

Read the approved design and relevant source. Confirm repository instructions,
current branch/worktree, existing tests, and user changes. Trace callers and
interfaces before choosing task boundaries. If the request is a one-file or
obvious edit, keep the work inline rather than producing a ceremonial plan.

## Plan structure

Save the plan at the repository's agreed path, normally
`docs/superpowers/plans/YYYY-MM-DD-<topic>-plan.md`. Include:

1. **Context and goal** — current behavior, desired behavior, constraints,
   and explicit non-goals.
2. **Global constraints** — settled model/tool, compatibility, safety,
   security, data-loss prevention, accessibility, calibration, and user-change
   requirements that bind every task.
3. **Interfaces and dependencies** — affected callers, data flow, test seams,
   and decisions already made.
4. **Tasks** — each task is one independently verifiable implementation result
   with exact files, symbols, behavior, tests, expected outputs, and commit
   boundary when commits are required. Group related files that must change
   together; split only at a real verification boundary.
   New plans use headings such as `### Task 1: 입력 검증`: the `Task` marker
   and positive integer are stable, while the title and body may be Korean.
   Put task subheadings below the task heading level. Older valid `Task N`
   headings remain readable; do not infer tasks from headings such as
   `### 1. 입력 검증`.
5. **Verification** — focused tests per task, integration checks, and final
   commands with expected evidence. Apply
   `superpowers-astra-luna:verification-before-completion` when deciding
   whether matching evidence can be reused or a command must run. Include TDD
   RED/GREEN steps for behavior changes. Review committed ranges with
   `review-package` and always include staged and unstaged diffs plus the
   task's untracked files. Entirely uncommitted work does not need a dummy
   commit for review.
6. **Review focus and recovery** — concrete risks, how to preserve unrelated
   changes, what to do on failure, and what decision would block progress.

Do not hide exact values, signatures, paths, or test cases in prose that a
worker cannot find. A task must say what it consumes from earlier tasks and
what later tasks may consume from it. Never add speculative architecture,
dependencies, or blanket line/word/token limits.

## Self-review before handoff

Read the completed plan once from top to bottom and check:

- every spec requirement maps to a task and verification;
- task boundaries do not conflict on shared files or interfaces;
- each task's files, symbols, tests, and expected output agree internally;
- the plan preserves TDD, systematic debugging, user changes, and safety;
- a worker can implement the task without inventing a design decision;
- scope and complexity are the smallest adequate shape.

Fix gaps inline. Honor a user-requested plan approval gate and ask about any
unresolved consequential decision. Otherwise the existing task authorization
permits execution; creating a plan does not add a new approval requirement. Use `superpowers-astra-luna:subagent-driven-development`
for bounded delegated work or `superpowers-astra-luna:executing-plans` for
inline execution.

## Execution handoff

The main session owns the plan, task selection, and code review. When a
task is clear and worth delegation, it creates one Luna worker with the exact
`gpt-6-luna` / `xhigh` / `fork_turns = "none"` settings and a focused task
brief. Related fixes return to that same worker. A second worker is permitted
only for explicitly requested independent parallel implementation. Reviewers,
planners, explorers, and diagnostic agents are not spawned.

Keep the plan and progress ledger as the recovery record. If implementation
reveals a plan defect, the main agent records a `Ruling:` with the chosen correction and
why it is safe before continuing. Do not silently rewrite requirements in a
worker prompt.
