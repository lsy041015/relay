---
name: using-superpowers
description: Use when starting a Relay development workflow that needs planning, implementation handoff or review. Skip unrelated conversations and simple lookups.
---

<SUBAGENT-STOP>
If you were dispatched as an implementation worker, follow the task brief and
the implementer contract. Do not run this bootstrap or delegate more work.
</SUBAGENT-STOP>

# Using Superpowers

Read the relevant skill completely before taking the action it governs. Skill
instructions apply after the user's request and the host's actual tool rules;
those sources win when they conflict. Announce the skill you are using, then
follow its required workflow.

## Roles in Relay

The main session keeps the model and reasoning effort selected by the user.
This skill does not select, switch, or override either setting. The main agent
handles intake, brainstorming and planning, design decisions, code
review and re-review, diagnosis, integration, and final verification.

The only delegated role is an implementation worker. Use `gpt-6-luna` with
`reasoning_effort = "xhigh"` and `fork_turns = "none"`. Give it a bounded,
reviewable implementation result, the exact files it may touch, acceptance
criteria, tests, and report path. The worker implements, tests, self-reviews,
and investigates failures within that task. It never delegates an independent
planning, diagnosis, or review role and never creates another worker.

Use one worker by default and reuse it for related fixes with `followup_task`.
Do not create a fresh reviewer, planner, explorer, analyst, or escalation
worker. After two failed fix attempts with the same root cause, stop retrying and
have the main agent re-evaluate the cause, scope, or implementation directly.

Small edits, lookups, reviews, re-reviews, diagnosis, and short verification
can stay in the main session. Multiple Luna workers are allowed only when the
user explicitly requests parallel implementation and the files and state are
independent. Every such worker still uses the exact Luna/xhigh/no-history
settings and may not spawn children.

Do not claim independent review, diagnosis, or validation that was not run.
Keep TDD, systematic debugging, user-change protection, security checks,
hardware calibration and other safety requirements from the relevant skills.

## Codex reference

This personal edition is Codex-only. Use `references/codex-tools.md` for the
current Codex tool syntax. The other platform files are retained as source
compatibility notes and are not active routing or delegation instructions.
Internal skill links use the `superpowers-astra-luna:` namespace.
