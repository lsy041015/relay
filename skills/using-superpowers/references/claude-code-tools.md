# Claude Code Compatibility Note

This personal edition is operated through Codex. Claude Code is listed only
to explain why the source skill may contain `Agent`, `Skill`, or todo wording;
these notes are not an active model-routing or delegation path.

If the documentation is ported to Claude Code, preserve the role policy from
`superpowers-astra-luna:using-superpowers`: the main session owns planning,
diagnosis, review, re-review, and integration; only an explicitly authorized
implementation worker may be delegated; a worker may self-review and debug
its implementation but may not create independent planning, analysis, or
review roles. Do not infer Claude model names or nested-agent settings from
this compatibility note.
