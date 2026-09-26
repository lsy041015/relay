---
name: test-driven-development
description: Use when adding or changing program behavior, fixing a bug, or refactoring behavior that needs regression protection.
---

# Behavior-first verification

For a new behavior or bug fix, write a minimal regression test before implementation. Name the production behavior that would make it fail. Run it and confirm RED is the expected assertion failure, not a syntax, import or environment error. Then implement the smallest correct change, observe GREEN, and refactor only while checks remain green.

Tests exercise observable behavior and meaningful boundaries, not mocks or implementation wording. Reuse the project's test setup. Prefer real dependencies where practical; understand side effects before mocking. Keep test-only behavior out of production code. Read [writing good tests](writing-good-tests.md) when designing new or changed tests.

For a behavior-preserving refactor, establish passing coverage before the change and verify it afterwards; do not invent an artificial failure. For docs, formatting and non-behavioral config edits, use relevant diff, parser/schema, render or link checks instead of synthetic unit tests. A config change that affects runtime behavior still needs a behavioral check. Throwaway probes must not be described as production-ready without appropriate verification.

Preserve existing user code. If implementation already exists, add the missing regression and demonstrate it against the original behavior in an isolated copy or a safely reversible task-owned change. Never delete or reset user work to recreate test order. If RED cannot be demonstrated, report that evidence gap; do not claim test-first evidence.

During development run focused checks. Before completion run the project's required checks, including its normal full test command for production code changes, or reuse matching evidence under `relay:verification-before-completion`. A focused pass does not prove a green suite. Report every observed failure and its scope, including pre-existing failures; never imply checks passed when blocked.

Diagnose unexpected failures with `relay:systematic-debugging`. Preserve security, data-loss prevention, accessibility and hardware safety. Do not lower acceptance criteria to save tokens. Record command, state, environment, exit code and log before claiming success.
