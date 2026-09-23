---
name: requesting-code-review
description: Use when a completed change needs a requirements and quality review before the next task or integration
---

# Requesting Code Review

In the Relay workflow, requesting review means preparing an evidence-based
review pass for the main session. It does not create a reviewer agent.
The main agent reviews the actual diff, traces relevant call paths, and performs any
necessary re-review after the existing Luna implementation worker fixes it.

## When to review

- after a delegated implementation task and before marking it complete;
- after a major feature or risky bug fix;
- before integration, merge, publish, or other user-authorized handoff;
- after a worker fix, scoped to the finding and fix diff.

Small lookups or text-only edits may be checked inline. Never claim an
independent review when the main agent performed the review.

## Review steps

1. Record the correct base and head. Prefer the existing
   `subagent-driven-development/scripts/review-package` helper when the task
   has a committed range, so the commit list, stat, and full contextual diff
   are one readable artifact. Always also inspect staged and unstaged `git diff` plus
   `git ls-files --others --exclude-standard`, and read the task's untracked
   files directly, even when the task includes commits. If BASE equals HEAD,
   skip the commit-only helper; do not force a commit.
2. Read the task brief or requirements, the worker report, and the diff
   package. Do not trust the report without checking the changed code.
3. Check requirements file by file, then quality: behavior, error handling,
   security, data loss, accessibility, calibration and hardware safety,
   compatibility, tests, and scope. Read outside the diff only for a named
   concrete risk.
4. Apply `superpowers-astra-luna:verification-before-completion` to the
   reported evidence and current change. Inspect actual logs; reuse valid
   results and rerun only checks with missing, invalidated, or uncertain
   evidence.
5. Classify findings by effect:
   - Critical: unsafe, data-loss, security, or broken required behavior;
   - Important: a required behavior, regression, or fragile implementation;
   - Minor: a useful polish item that does not block the task.
6. Record the verdict and Minor items in the ledger. Send Critical or
   Important fixes to the same worker with `followup_task`, including file,
   location, cause, acceptance condition, and covering tests. The main agent performs
   the scoped re-review.

If two failed fix attempts have the same root cause, stop retrying and record
a main-agent `Ruling:`: change the plan, fix a small issue inline, or report the blocker.
Do not create a fresh reviewer, a fresh implementer, or a higher-tier child.

## Review report

Use [code-reviewer.md](code-reviewer.md) as the main-session worksheet. Start
with the compliance verdict, cite `file:line` evidence for every finding, list
strengths, show tests checked, and state `APPROVED` or `NEEDS_FIXES`. Include
requirements that could not be verified from the diff as explicit gaps.
