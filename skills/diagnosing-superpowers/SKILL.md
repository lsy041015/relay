---
name: diagnosing-superpowers
description: Use when a Superpowers session has repeated work, ignored a plan, stumbled, produced poor results, or used unexpected time or tokens
---

# Diagnosing Superpowers

The main agent performs the diagnosis. This skill reports what happened with transcript
evidence; it does not create an analyst, audit, reviewer, or escalation agent,
and it does not prescribe a Superpowers change. Dimension prompts are worksheets
for the main agent's own passes.

## Workflow

Create a todo per applicable step and keep the original records read-only.

1. **Intake.** Get a statement naming the session(s), known turn range, user
   expectation, observed behavior, and metric or event that matters. An
   already-scoped request is sufficient; an unscoped whole-session "why"
   needs clarification before analysis.
2. **Locate.** Resolve each session to verified absolute paths with
   `references/session-discovery.md`. Confirm past sessions with first prompt
   and timestamp, list rejected candidates and reasons, and enumerate any
   historical worker transcripts. Create
   `~/.superpowers/diagnosing-superpowers/<session-id>/` and fill
   `templates/case.md` with provenance and record meanings.
3. **Triage.** Read the reported region yourself. Run the dimension prompts in
   `prompts/` as sequential main agent analysis passes: skill timeline, plan
   adherence, repeated work, stumbles, quality evidence, request conflicts,
   and cost/time. Use `references/context-safety.md` for every read. For a
   long or unpredictable transcript, process and aggregate it with
   context-mode; do not print whole records into context. Every finding must
   cite an absolute `path:line`.
4. **Report.** Fill `templates/report.md` in order, verify that each citation
   proves the claim, show the report, and give its path. Do not infer a cause
   from a summary, model name, or token count that is absent from the records.
5. **Issues.** When the report calls for a possible or likely issue, or the
   user asks, search according to `references/github-issues.md`. Show matches.
   If none match, draft `templates/issue.md`, show exact text, and create an
   issue only after the user's explicit approval.
6. **Export.** Build a bundle only when requested. Ask the redaction level
   (skeleton, evidence, or full), apply `templates/bundle-README.md`, and run
   `prompts/scrub.md` followed by `prompts/scrub-audit.md` until CLEAN. Reconcile
   the evidence, file list, counts, and privacy result before showing them.
   Archive only after approval; tell the user what it contains and that
   scrubbing is not a privacy certification.
7. **Similar sessions.** When asked, derive a confirmed signature, list
   candidates by mtime and size, locate marker lines, then run
   `prompts/similar-session.md` sequentially for each candidate and append the
   evidence to report §9.

## Evidence and safety rules

- Follow `references/context-safety.md` before reading every session file.
- Never modify, move, delete, or scrub the original session store.
- Preserve absolute paths, line numbers, timestamps, and the record-shape
  evidence that gives each field its meaning.
- Human prompts are only the records the case identifies as human-typed.
  Hook output, system reminders, and tool results are not user requests. In a
  historical worker transcript, `user` is the parent agent.
- Report Superpowers involvement in §7 and stop there. Do not diagnose the
  skill itself, propose a fix, or advise the user from transcript evidence.
- Do not archive or publish a bundle, issue, or comment before its required
  approval. Keep sensitive values out of reports when they are not needed to
  prove a finding.

## Quick lead order

| Complaint | Lead with |
|---|---|
| Took too long | cost-and-time, stumbles |
| Extra work | repeated-work, plan-adherence |
| Expensive | cost-and-time |
| Still running | skill-timeline and in-progress coverage |
| Ignored plan | plan-adherence and compaction events |
| Skill never fired | skill-timeline |

Internal skill links use the `superpowers-astra-luna:` namespace. The personal
edition is Codex-operated; no other host's delegation guide is an active
execution path.
