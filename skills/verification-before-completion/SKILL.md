---
name: verification-before-completion
description: Use when about to claim work is complete, fixed, or passing, before committing or creating PRs - requires traceable verification evidence before success claims
---

# Verification Before Completion

## Overview

**Core principle:** Evidence before claims, always.

## The Evidence Rule

Do not claim that work is complete, fixed, or passing until the current result
has a verification record that another person can inspect. A result may be
reused when the main session confirms all of these conditions:

- the same code state is under test, including staged and unstaged changes and
  relevant untracked or newly created files;
- the command and verification scope are the same;
- relevant dependencies, configuration, runtime, hardware, and external state
  are unchanged or known to be equivalent; and
- the actual log and exit code are available, rather than only a success
  summary.

A Git SHA alone does not prove that an uncommitted change set or new file is
unchanged. Outside Git, record the needed file version or content evidence.
The main Astra session checks the worker's evidence against the actual change
set before reusing it.

Run the affected check again when evidence is missing or summary-only, the
code/dependency/environment/external state changed or is uncertain, the
requested scope is broader than the recorded scope, or the final integration
state has not been checked. Do not rerun a full suite for every progress
message when the evidence still satisfies this rule, and do not create an
unbounded retry loop. After a failure, diagnose its cause and run the covering
check after the fix; after two failed fix attempts with the same root cause,
stop and make an Astra ruling.

## The Gate Function

Before a completion or success claim:

1. **Identify** the command or existing evidence that proves the claim.
2. **Compare** its code, staged/unstaged/untracked state, environment, and
   scope with the current result.
3. **Run or reuse** the evidence under the rule above. If running, execute the
   complete command needed for the claim.
4. **Read** the output, exit code, and failure count or equivalent result.
5. **Report** the evidence and only then state the supported claim.

If the evidence does not support the claim, report the actual status and the
missing or failed check.

## Verification record

Keep the report short and inspectable. At minimum record:

```text
command: <exact command>
cwd: <working directory>
state: <commit plus staged/unstaged/untracked or file/content state>
environment: <relevant runtime, dependency, configuration, hardware, or external state>
exit: <numeric exit code>
log: <path or bounded result excerpt>
```

Store long logs in a file and report the failure cause, key result, and path in
the conversation. A worker's `PASS` sentence is not evidence until these
fields and the relevant state have been checked.

## Common failures

| Claim | Required evidence | Not sufficient |
|---|---|---|
| Tests pass | The required test command's output and exit code | A previous run without matching-state evidence or “should pass” |
| Linter is clean | The applicable linter output and exit code | A partial check or extrapolation |
| Build succeeds | The build command's output and exit code | A linter result |
| Bug is fixed | The original symptom and covering regression check | Code changed with no behavior check |
| Regression check works | Meaningful RED and GREEN observations | A test file that ran once |
| Worker completed | Actual diff and verification record | The worker's report alone |
| Requirements are met | A requirement-by-requirement inspection | Tests alone |

## TDD and requirement checks

For behavior changes, preserve a meaningful RED/GREEN record: the check fails
for the original behavior, the smallest implementation makes it pass, and the
covering check still passes for the final state. Use systematic debugging for
unexpected failures rather than guessing.

Re-read the approved requirements and inspect each acceptance condition before
reporting completion. Record gaps, environment limits, and unresolved
failures explicitly. Apply the same evidence rule to review, plan execution,
and integration decisions; do not silently convert a summary into proof.
