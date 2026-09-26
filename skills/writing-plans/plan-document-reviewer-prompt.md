# Main Plan Review Worksheet

Use this worksheet in the main session after writing a plan. It replaces the old
plan-reviewer dispatch.

```text
Plan: [PLAN_FILE_PATH]
Spec/design: [SPEC_FILE_PATH]
```

Read both documents and check:

- completeness: no TODO, placeholder, missing requirement, or unowned
  verification;
- alignment: every spec requirement is covered without scope creep;
- decomposition: task boundaries follow independently verifiable results and
  shared interfaces are explicit;
- buildability: files, symbols, decisions, tests, expected output, recovery,
  and safety conditions are actionable;
- role policy: no separate review, exploration, diagnosis, or model-escalation
  dispatch is required; delegated implementation uses the existing implementer
  worker contract when appropriate.

Output:

```text
Status: Approved | Issues Found
Issues: <task/section, concrete gap, implementation effect> | None
Recommendations: <advisory improvements> | None
```

Fix issues inline and repeat the worksheet. The user approves the final plan
before implementation.
