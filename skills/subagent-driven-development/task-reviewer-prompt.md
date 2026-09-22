# Main Task Review Worksheet

Use this worksheet in the Astra session after an implementation worker
reports `DONE`. It replaces the old task-reviewer dispatch. Read the brief,
worker report, and one review package; inspect source outside the package only
for a named, concrete risk.

```text
Task: [TASK_NAME]
Brief: [BRIEF_FILE]
Global constraints: [GLOBAL_CONSTRAINTS]
Worker report: [REPORT_FILE]
Base: [BASE_SHA]
Head: [HEAD_SHA]
Diff package: [DIFF_FILE]
Always include staged and unstaged diffs plus the task's untracked files,
even when a committed range exists; never force a dummy commit.
```

## Review pass

1. Compare the diff with every requirement and acceptance condition. Check
   every listed file and identify missing, extra, or misunderstood behavior.
2. Trace changed interfaces and one focused call path for each concrete risk.
   Check error handling, security, data loss, accessibility, calibration,
   hardware safety, and preservation of unrelated user changes where relevant.
3. Treat the worker report as a claim. Confirm the test commands, exit codes,
   and output are present and actually cover the changed behavior. Do not
   repeat a full suite merely to reproduce a successful report; run a focused
   check only when a specific doubt remains.
4. Check that the implementation is understandable, follows local patterns,
   and does not add speculative abstraction, dependencies, or scope.

Do not invent an independent reviewer or ask another agent to inspect a part
of the diff. Astra owns this review and the subsequent re-review. If a finding
is real, send a precise fix to the same implementation worker with
`followup_task`. If two failed fix attempts have the same root cause, stop and
write an Astra Ruling before changing the plan or fixing inline.

## Output

```text
Spec compliance: ✅ clean | ❌ findings | ⚠️ cannot verify <requirement>
Strengths: <specific evidence>
Critical: <file:line, problem, effect, required fix> | None
Important: <file:line, problem, effect, required fix> | None
Minor: <file:line, deferred one-liner> | None
Tests checked: <commands and evidence>
Assessment: APPROVED | NEEDS_FIXES
```

Record Minor findings and unresolved verification gaps in the plan ledger.
Critical, Important, and confirmed spec gaps enter the scoped fix loop; they
are not silently waived.
