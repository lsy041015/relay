---
name: writing-skills
description: Use when creating, editing, or verifying a skill before it is enabled or deployed
---

# Writing Skills

Treat process documentation like behavior: define a pressure case, observe
the baseline, write the smallest rule that closes the observed failure, and
verify the rule against the same case. This is TDD applied to a skill. Use
`relay:test-driven-development` for the RED/GREEN discipline
and `anthropic-best-practices.md` for general authoring guidance.

The main session owns design, baseline analysis, review, and acceptance.
Do not create evaluation, review, or analyst agents. If a pressure scenario
must exercise a delegated implementation behavior, use only an already
authorized implementer worker with the exact task scope; an evaluator
worker is outside this edition. Do not claim a scenario was run when it was
only read or imagined.

## Start with the contract

Before editing, identify:

- the skill's trigger and non-trigger;
- the behavior a user should observe;
- the repository and runtime paths the skill may mention;
- user, host, security, privacy, data-loss, accessibility, calibration, and
  hardware constraints;
- existing references and examples that must stay compatible.

Read the existing skill and exact callers before changing it. Keep the
frontmatter valid: `name` uses letters, numbers, and hyphens, and `description`
starts with `Use when...` and describes triggers rather than the workflow.
Prefer one clear rule and one concrete example over repeated warnings.

## Skill TDD

### RED: baseline

Write realistic pressure scenarios that make the unwanted behavior tempting.
Combine time, sunk cost, authority, exhaustion, or social pressure. Give the
agent concrete options and a real action to choose. Run the scenario without
the candidate rule when a baseline is meaningful; record the exact choice,
rationalization, and evidence. If the control already behaves correctly, do
not invent a rule to solve a problem that was not observed.

### GREEN: smallest rule

Write only the guidance needed to prevent the observed violation. Make the
safe path operational: say what to inspect, which action to take, what output
to record, and when to stop. Place the key rule before long explanation. Use
conditional instructions for conditional behavior; avoid broad prohibitions
that leave the agent negotiating with the wording.

Run the same scenario with the skill and record compliance. Keep TDD, user
approval gates, and recovery rules explicit when the skill depends on them.

### REFACTOR: close evidence-backed loopholes

When a scenario still fails, record the new rationalization verbatim, update
the smallest section that closes it, and rerun the case. Do not pile up a
second copy of the workflow or universal line/word/token caps that discard
needed evidence. Remove contradictions rather than appending an override to
an obsolete flow.

## Content and structure

Use this compact structure when it fits:

```markdown
---
name: skill-name
description: Use when <specific trigger>
---

# Skill Name
What problem it solves and the invariant it protects.

## When to use
Trigger and non-trigger examples.

## Workflow
The smallest actionable sequence, including stop and recovery points.

## Verification
Evidence required before claiming completion.

## Common failures
Observed rationalizations and their direct counter-action.
```

Move heavy reference material, reusable scripts, or templates into supporting
files and link them directly from `SKILL.md`. Keep references one level deep.
Use tables for repeated fields, flowcharts only for non-obvious branches, and
examples that are complete enough to run or copy. Internal links in this
edition use the `relay:` namespace.

## Verification before deployment

1. Validate frontmatter, links, placeholder names, and examples.
2. Search the whole `skills/` tree for stale role instructions: separate
   reviewer/analyst/planner dispatch, fresh-worker escalation, unapproved
   nested delegation, wrong model/effort, old namespace, and hidden platform
   variants.
3. Run baseline and candidate pressure cases that matter. If execution is
   unavailable, report that limitation and distinguish static inspection from
   behavioral evidence.
4. Review the actual diff for scope, contradictions, and accidental edits.
5. Re-run the relevant checks after every correction and record commands,
   exit codes, and material output.

The final report names changed files, checks actually run, behavioral evidence,
and unresolved issues. It does not claim an independent evaluation that did
not occur. Publishing, installing, or changing global configuration remains a
separate user-authorized action.
