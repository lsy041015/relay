# Main Code Review Worksheet

Use this worksheet for the main agent's task or whole-branch review. It replaces the
old code-reviewer dispatch template. Fill every field before reviewing.

```text
Description: [DESCRIPTION]
Requirements or plan: [PLAN_OR_REQUIREMENTS]
Base: [BASE_SHA]
Head: [HEAD_SHA]
Diff package: [DIFF_FILE]
Worker report, if any: [REPORT_FILE]
Always also review these actual workspace changes, even when commits exist:
staged diff: [STAGED_DIFF], unstaged diff: [UNSTAGED_DIFF], untracked files:
[UNTRACKED_FILES]
```

Read the requirements, report, and diff package once. The package is the
primary view of changed code; inspect an unchanged call site only to evaluate
a named concrete risk. Do not mutate the checkout, index, branch, or HEAD.

## Checks

Compare every requirement against the diff and mark missing, extra, or
misunderstood behavior. Check changed interfaces and relevant call paths for:

- correctness and edge cases;
- error handling, security, data loss, accessibility, and compatibility;
- required calibration, collision checks, or hardware safety;
- tests that assert behavior rather than mocks or empty execution;
- documentation and integration with local patterns;
- unnecessary abstractions, dependencies, or scope.

Treat a worker report as an unverified claim. Confirm its test commands,
exit codes, and relevant output. Run a focused test only for a concrete doubt
the report cannot answer. Do not create a subagent, another reviewer, or a
second opinion. The main agent owns this review and decides whether feedback is valid.

The specification expresses the required behavior but may not enumerate every
input. Grade silent behavior by the result a reasonable user should receive.
List any requirement you cannot verify from the diff as a verification gap.
Before the verdict, list any behavior you considered but set aside as outside
the plan or spec and why; the main agent must rule on each item rather than silently
drop it.

## Output

```text
### Spec Compliance
✅ Spec compliant | ❌ Issues found: <file:line findings>
⚠️ Cannot verify from diff: <requirement and focused check needed> | None

### Strengths
<specific file:line evidence>

### Declined to judge
<behavior set aside and reason> | None

### Issues
Critical: <file:line, problem, effect, fix> | None
Important: <file:line, problem, effect, fix> | None
Minor: <file:line, deferred one-liner> | None

### Tests checked
<commands, exit codes, and relevant output>

### Assessment
APPROVED | NEEDS_FIXES
Reasoning: <one or two technical sentences>
```

Critical and Important findings go to the existing implementation worker as a
focused `followup_task` when one exists; the main agent may fix a small issue inline.
After two failed fix attempts with the same root cause, record a main-agent Ruling
and change the plan or report the blocker. Minor findings and out-of-scope
observations go in the ledger for final triage.
