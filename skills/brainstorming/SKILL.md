---
name: brainstorming
description: Use when a feature or behavior change needs unresolved design decisions. Skip read-only tasks and straightforward changes with settled requirements.
---

# Design before implementation

The main session owns design. Preserve the user's purpose, constraints and acceptance conditions. Read the relevant existing flow before choosing an approach; do not repeat questions already answered in the request.

Choose only the depth the task needs:

- **Bounded change:** requirements and implementation boundary are clear. State the approach briefly when useful, then implement within the existing authorization. No mandatory spec file, plan file or separate approval turn.
- **Feasibility spike:** identify the concrete question and cheapest adequate probe. Read-only checks can proceed. Keep throwaway experiments isolated and label their limits; retaining prototype code requires production verification.
- **Architectural change:** new subsystem, cross-component interface, migration or meaningful unresolved tradeoff. Read [architecture decisions](references/architecture.md), record the design and acceptance conditions, and use `superpowers-astra-luna:writing-plans` when a multi-step implementation plan helps execution.

Ask only for missing information or a consequential decision that cannot reasonably be inferred. Existing authorization persists. Honor an explicit request to stop for design or plan approval; otherwise do not turn routine document creation into a new permission gate. Host rules govern destructive or external actions. Record newly discovered scope or risk and reassess only the affected decision.

Stay within the request. Preserve security, privacy, data integrity, accessibility, compatibility and hardware calibration. Avoid unrelated refactoring and speculative features. Use a visual only when it clarifies a real decision, with the available host tools; do not start a separate visual-companion server by default.

Before implementation, confirm every acceptance condition has a verification path. For behavior changes use meaningful regression/TDD checks; use `superpowers-astra-luna:verification-before-completion` for reusable evidence. No separate planner or reviewer agents.
