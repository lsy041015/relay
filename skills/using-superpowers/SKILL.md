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

The only delegated role is an implementation worker. Dispatch it with
the host implementer preset (Codex: `gpt-6-luna` / `xhigh` / `fork_turns = "none"`; Claude Code: `relay:implementer` agent = `claude-sonnet-5` / `high`) and no inherited history. Give it a bounded,
reviewable implementation result, the exact files it may touch, acceptance
criteria, tests, and report path. The worker implements, tests, self-reviews,
and investigates failures within that task. It never delegates an independent
planning, diagnosis, or review role and never creates another worker.

Use one worker by default and reuse it for related fixes with `followup_task` (Codex) / `SendMessage` (Claude Code).
Do not create a fresh reviewer, planner, explorer, analyst, or escalation
worker. After two failed fix attempts with the same root cause, stop retrying and
have the main agent re-evaluate the cause, scope, or implementation directly.

Small edits, lookups, reviews, re-reviews, diagnosis, and short verification
can stay in the main session. Multiple implementer workers are allowed only when the
user explicitly requests parallel implementation and the files and state are
independent. Every such worker still uses the same host implementer
preset and may not spawn children.

Do not claim independent review, diagnosis, or validation that was not run.
Keep TDD, systematic debugging, user-change protection, security checks,
hardware calibration and other safety requirements from the relevant skills.

## Host reference

This edition runs on Codex and Claude Code. Use `references/codex-tools.md` on
Codex and `references/claude-code-tools.md` on Claude Code for exact tool syntax. The other platform files are retained as source
compatibility notes and are not active routing or delegation instructions.
Internal skill links use the `relay:` namespace.
