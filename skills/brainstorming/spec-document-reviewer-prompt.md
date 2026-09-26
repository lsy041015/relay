# Main Spec Review Worksheet

Use this worksheet in the main session after writing a design specification. It replaces
the old spec-reviewer dispatch.

```text
Spec: [SPEC_FILE_PATH]
```

Check for incomplete sections and placeholders, internal contradictions,
requirements that could be interpreted two ways, scope spanning unrelated
subsystems, unrequested features, and missing acceptance or safety conditions.
Compare the document with the conversation's settled decisions and preserve
the user's approval gates. Fix concrete issues inline before handing the spec
to `relay:writing-plans`.

```text
Status: Approved | Issues Found
Issues: <section, concrete problem, planning effect> | None
Recommendations: <advisory improvements> | None
```

This is a main-agent self-review. Do not create a reviewer, planner, analyst, or
other non-implementation worker.
