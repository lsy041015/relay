# Hermes Agent Compatibility Note

This personal edition runs on Codex and Claude Code. These mappings are retained only for
readability when porting source documentation; they are not an active Hermes
delegation guide.

| Action | Typical Hermes tool |
|---|---|
| Read a file | `read_file` |
| Edit a file | `patch` |
| Run a command | `terminal` |
| Search files | `search_files` |
| Track work | `todo` |

If ported, apply `relay:using-superpowers`: the main session
owns plans, diagnosis, reviews, re-reviews, and integration. Delegate only an
explicitly authorized implementation unit. A worker may self-review and
debug its implementation but never delegates a non-implementation role or a
nested worker. Do not copy model or parallel-dispatch settings from this note.
