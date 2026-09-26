---
name: receiving-code-review
description: Use when review feedback arrives and its correctness, scope, or implementation impact must be evaluated
---

# Receiving Code Review

Review feedback is input to the main agent's technical decision. Verify it against the
actual code, requirements, tests, and user decisions before changing anything.
Do not perform agreement or blind implementation.

## Response pattern

1. Read all feedback without reacting.
2. Restate each item as a concrete behavior or acceptance condition.
3. Check the cited code, call paths, tests, compatibility, and surrounding
   design. Name the evidence.
4. Classify it as required, optional, incorrect, or unclear.
5. Fix required items in severity order, one coherent change at a time, with
   a covering test. Keep user changes and the approved scope intact.
6. Re-run the relevant checks, inspect the fix diff, and report the result.

For a delegated task, send the concrete fix to the same implementer worker with
`followup_task` (Codex) / `SendMessage` (Claude Code): include the finding, file and location, why it matters, the
acceptance condition, and the covering test. The main agent performs the re-review.
Small corrections may stay inline. Do not create a new reviewer, fixer,
analyst, or model escalation. If two failed fix attempts have the same root cause,
record a main-agent `Ruling:` and re-evaluate the plan or implement the smallest
safe change directly.

## Unclear or conflicting feedback

Do not implement a partially understood batch. Resolve the ambiguity from
source, tests, the approved plan, and prior user decisions. Ask the user only
when a missing decision changes the requested outcome or cannot be inferred.
If feedback conflicts with a settled user decision, preserve that decision and
show the technical evidence; do not silently replace it.

## Technical checks

- A useful suggestion fixes behavior the product actually needs. Check usage
  before adding an unused feature or abstraction.
- Evaluate compatibility, error paths, security and data-loss risk, and any
  calibration or hardware constraints.
- Tests must exercise the reported behavior. A passing mock-only test is not
  evidence that the defect is fixed.
- State pushback plainly when feedback is wrong, with file and test evidence.
  If later evidence changes the ruling, correct it and continue without
  performative apology.

Internal references use the `relay:` namespace.
