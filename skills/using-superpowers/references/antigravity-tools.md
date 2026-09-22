# Antigravity Compatibility Note

The personal edition is Codex-only. Antigravity terms below explain source
compatibility and are not an operational delegation path.

| Action | Typical Antigravity mechanism |
|---|---|
| Dispatch an explicitly authorized implementation worker | `invoke_subagent` |
| Track work | task artifact written with `write_to_file` |

If ported, keep all planning, diagnosis, review, re-review, and integration in
the main session. A worker may implement, test, self-review, and debug its own
bounded task; it may not create a reviewer, analyst, planner, or nested worker.
Do not infer model routing from this note.
