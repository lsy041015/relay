<p align="center">
  <img src="assets/relay-banner.png" alt="Relay — a skill plugin where your main model designs and one fixed worker implements" width="100%">
</p>

<p align="center"><a href="README.md">한국어</a> · <b>English</b></p>

# Relay

> **A skill plugin that keeps design and review on the main model you chose and hands only bounded implementation work to one fixed worker per host.**

The same 15 skills run on Codex and Claude Code. A personal fork of [Jesse Vincent's Superpowers](https://github.com/obra/superpowers) 6.4.1.

> **Status: archived, no longer updated.** The last version (`6.4.1+claude.20260926`, `6.4.1+codex.20260926`) was a personal experiment.
> 16 regression tests passed on Linux and macOS; some fail on Windows (Git Bash). Usage savings were never proven.

> **Relay continues as [Orchestra](https://github.com/lsy041015/orchestra). New users should install Orchestra; this README records what Relay was.**

## Why

In long sessions the model you picked for design also does rote edits, upstream Superpowers' `subagent-driven-development` creates a
fresh subagent per task with a review after each (`UPSTREAM_README.md`), and Codex and Claude Code delegate differently. Relay keeps intake,
design, planning, review and final verification in the main session, on your model and effort, and gives one worker per host a brief
(goal, allowed files, acceptance checks, tests, report path) without the chat history.

## What it does

15 skills, helper scripts and one Claude Code worker agent. No MCP server, no account connections, no auto-run hooks.

- **Delegation**: one bounded task per worker; review fixes go back to the same worker. `task-brief` puts one `### Task N:` section of the plan in a file.
- **Two hosts, one tree**: `.claude-plugin/plugin.json` and `.codex-plugin/plugin.json` read the same `skills/`; skills call each other as `relay:<skill>`.
- **Extras**: git worktree isolation, a local Node.js visual companion for mockups (`skills/brainstorming/scripts/server.cjs`), post-hoc session diagnosis (`diagnosing-superpowers`).
- **Skills**: `using-superpowers`, `brainstorming`, `writing-plans` · `subagent-driven-development`, `executing-plans`, `using-git-worktrees`, `test-driven-development` · `systematic-debugging`, `requesting-code-review`, `receiving-code-review`, `verification-before-completion`, `diagnosing-superpowers` · `finishing-a-development-branch`, `dispatching-parallel-agents`, `writing-skills`.

## How it works

`using-superpowers` routes to `brainstorming` and `writing-plans` as needed. The worker implements, tests, checks its own diff and returns
`Status: DONE | BLOCKED | NEEDS_DECISION` with a report file; the main session reviews (`review-package`), sends fixes to the same worker,
verifies, and `finishing-a-development-branch` cleans up only worktrees Relay created. Small edits, reviews and diagnosis stay in the main
session; parallel workers only on explicit request. The plugin never changes the main session's model.

| Host | Worker preset | Call |
|---|---|---|
| Codex | `gpt-6-luna` · `reasoning_effort = "xhigh"` · `fork_turns = "none"` | `spawn_agent(...)`, fixes via `followup_task` |
| Claude Code | `relay:implementer` agent · `model: claude-sonnet-5` · `effort: high` | `Agent(subagent_type="relay:implementer", ...)`, fixes via `SendMessage` |

## What changed in Orchestra

| | Relay | Orchestra |
|---|---|---|
| Worker | One fixed preset per host (above) | A Claude subagent or a Codex CLI worker with the model and effort you pick |
| Assignment | One worker for a bounded task | `orchestra:orchestrator` (Claude Code) splits an approved plan into Easy / Medium / Hard / Hard (UI) tiers and routes each tier |
| Defaults | Pinned in `agents/implementer.md` and the skill docs | `~/.claude/orchestra.json`, `<project>/.orchestra.json` |
| Codex worker | Only as the Codex host's own `spawn_agent` | `codex-worker.mjs` runs `codex exec` directly, checks changed files before and after, fix rounds via `--resume <thread>` |
| Task list | No convention | `[Codex gpt-6-luna/high] Task 3: ...` |
| Skills | 15 | 16 (adds `orchestrator`) |
| Evidence | No CI, no recorded run | CI on Ubuntu, macOS and Windows; a recorded end-to-end demo (a web piano) |

## Install (historical)

Install Orchestra instead: `claude plugin marketplace add lsy041015/orchestra`, then `claude plugin install orchestra@orchestra`.
Do not enable Relay, Orchestra and upstream Superpowers together; same-named skills collide. What Relay used (Git and Bash;
Node.js for the visual companion; a separate `context-mode` tool for parts of long-session diagnosis):

```bash
claude plugin marketplace add lsy041015/relay && claude plugin install relay@relay   # Claude Code
codex plugin marketplace add lsy041015/relay && codex plugin add relay@relay         # Codex
python3 tests/test_task_brief.py            # tests, from the repo root
python3 tests/test_worktree_instructions.py
python3 tests/test_worktree_cleanup.py
python3 tests/test_sdd_safety.py
```

Start a new session afterwards. Updates: `claude plugin marketplace update relay` or `codex plugin marketplace upgrade relay`, then install
again. Local checkouts: `claude plugin marketplace add ./relay` and `claude plugin validate ./relay`; on Codex, a personal marketplace entry in
`~/.agents/plugins/marketplace.json`, a cache refresh with `update_plugin_cachebuster.py`, then `codex plugin add relay@personal`.
Coming from the older name, remove `superpowers-astra-luna@relay` (or `@personal`) first.

## Design notes

- `disallowedTools: Agent` in `agents/implementer.md` stops the Claude Code worker from spawning subagents: a removed tool, not a request.
- No silent model swaps: the frontmatter pins the model; if a preset is unavailable, the main session does the work or reports the limit.
- Cleanup removes a worktree only when its `relay-owned-worktree` marker matches the real path; a directory name proves nothing.
- `sdd-workspace` rejects symlinked paths and keeps an existing `.gitignore`; `task-done` records completion only if the test command succeeds.
- `task-brief` keeps the task text out of the main context and ignores headings inside code fences.
- The review prompt is a checklist for the main session, not an agent. Two failed fixes with the same root cause stop the loop.

## Limits

Savings were never measured (compare Codex's 7-day `usedPercent` or Claude Code plan usage with workload, settings, retries and
verification scope; tokens and time are not converted into quota). Linux and macOS passed 16 regression, 15 frontmatter and 8 Bash syntax
checks; Windows (Git Bash) partly fails on cp949 encoding (`PYTHONUTF8=1` helps partly), symlink permissions and CRLF, not skill logic.
Tests skip real model delegation and most recovery paths; no CI. The worktree fallback needs GNU `realpath -m`: Orchestra fixed that
check for macOS, Relay did not. No Codex workers from Claude Code and no model choice by difficulty (both came with Orchestra).

## Credits

MIT [LICENSE](LICENSE) from upstream [Superpowers](https://github.com/obra/superpowers) by Jesse Vincent (2025), kept unchanged, with
[UPSTREAM_README.md](UPSTREAM_README.md) and the inherited Prime Radiant [CODE_OF_CONDUCT.md](CODE_OF_CONDUCT.md). The icons in `assets/`
and `.codex-plugin/assets/` are the upstream Superpowers mark, not Relay branding. Names: `superpowers-astra-luna` → `relay` → `orchestra`;
send issues to [Orchestra](https://github.com/lsy041015/orchestra/issues). Not an official OpenAI, Anthropic or Superpowers release.

---

<p align="center"><sub>LSY.KOR · <a href="https://github.com/lsy041015">More projects</a></sub></p>
