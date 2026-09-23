# Main Scoped Re-Review Worksheet

Use this worksheet in the main session after the existing implementation worker fixes
review findings. It replaces the old re-reviewer dispatch and keeps the pass
limited to the findings and the fix diff.

```text
Task: [TASK_NAME]
Brief: [BRIEF_FILE]
Findings under verification: [FINDINGS]
Worker report: [REPORT_FILE]
Fix base: [FIX_BASE_SHA]
Head: [HEAD_SHA]
Fix diff package: [DIFF_FILE]
Always inspect staged and unstaged diffs plus the fix's untracked files,
even when commits exist; never create a dummy commit just to package review.
```

For each listed finding, inspect the fix diff and report `ADDRESSED` only when
the specific defect is gone. Check the fix for new Critical or Important
breakage, and inspect the worker's appended test evidence. Do not re-review
untouched code, rerun a full suite without a concrete doubt, or create another
worker or reviewer. Out-of-scope observations are ledger entries; they do not
expand this pass.

```text
Finding 1: ADDRESSED | NOT_ADDRESSED — <file:line evidence>
Finding 2: ADDRESSED | NOT_ADDRESSED — <file:line evidence>
New Critical/Important breakage: <file:line, effect> | None
Out-of-scope observations: <one-line entries> | None
Tests checked: <covering commands and evidence>
Verdict: CLEAN | FINDINGS_REMAIN
```

If two failed fix attempts have the same root cause, stop the loop and record the
main agent's decision and its cost if wrong. Otherwise send the next concrete
fix to the same Luna worker with `followup_task`.
