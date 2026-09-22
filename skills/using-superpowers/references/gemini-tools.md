# Gemini CLI Compatibility Note

This personal edition is Codex-operated. The table below is retained only as
source compatibility information; it is not an active Gemini routing guide and
does not authorize a non-implementation dispatch.

| Action | Typical Gemini CLI tool |
|---|---|
| Read a file | `read_file` |
| Create or edit a file | `write_file` / `replace` |
| Run a command | `run_shell_command` |
| Search or find files | `grep_search` / `glob` |
| Invoke a skill | `activate_skill` |
| Track work | `write_todos` |

If ported to Gemini, apply the role policy from
`superpowers-astra-luna:using-superpowers`: keep planning, diagnosis, review,
and re-review in the main session; delegate only an explicitly authorized
implementation worker, and never let that worker create another worker or an
independent evaluator. Do not copy model or parallel-dispatch settings from
this compatibility note.
