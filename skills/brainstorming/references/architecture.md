# Architectural decisions

Use only for a real cross-component design question, not a small settled edit.
Identify the user, desired outcome, existing flow, constraints, interfaces and success criteria. If independent subsystems need separate execution boundaries, record their dependency order without expanding the scope.
Compare alternatives only where the choice matters. Explain the recommendation and tradeoffs; reuse current patterns where adequate.
Record components, data flow, inputs/outputs, failure handling, compatibility, rollout/recovery, and the tests or observations that establish acceptance. Cover security, data loss, privacy, accessibility and hardware calibration when relevant.
Keep boundaries understandable and independently verifiable. Avoid abstractions, dependencies or cleanup unrelated to the requested outcome.
Save the design at the user's location, otherwise `docs/superpowers/specs/YYYY-MM-DD-<topic>-design.md` when a durable artifact is useful. Do not create a commit solely to satisfy this workflow.
Review once for missing requirements, contradictions, placeholders, unverifiable claims and scope expansion. Correct supported gaps. Ask about unresolved consequential choices; do not ask again about already approved scope.
If the user requested approval before implementation, present the concrete design and wait. Otherwise continue authorized work, using `relay:writing-plans` when the implementation needs multiple verifiable steps.
