# Claude Code Plugins & MCP Servers

Reference list of plugins and MCP servers used with Claude Code in this vault. Reinstall with the commands below after a fresh setup.

> Antigravity skills live under `.agent/` — this file is Claude-only.

## Install commands

```bash
# Official marketplace (skill-creator, frontend-design, code-simplifier, context7)
/plugin marketplace add anthropics/claude-plugins-official
/plugin install skill-creator@claude-plugins-official
/plugin install frontend-design@claude-plugins-official
/plugin install code-simplifier@claude-plugins-official
claude plugin install context7@claude-plugins-official

# Buildomator (third-party marketplace)
/plugin marketplace add buildomator/marketplace
/plugin install bm@buildomator
/reload-plugins

# context-mode (third-party marketplace)
/plugin marketplace add mksglu/context-mode
/plugin install context-mode@context-mode

# claude-mem (third-party marketplace)
/plugin marketplace add thedotmack/claude-mem
/plugin install claude-mem

# oh-my-claudecode (third-party marketplace)
/plugin marketplace add https://github.com/Yeachan-Heo/oh-my-claudecode
/plugin install oh-my-claudecode
```

## Graphify (local CLI, not a plugin)

Builds a knowledge graph of a repo on disk (`graphify-out/graph.json`, `graph.html`, `GRAPH_REPORT.md`). No server or sign-in. `/bm:graphify build` shells out to this CLI (`graphify . --update`), so install it first. Requires Python 3.10+.

```bash
# Install the CLI (PyPI package name has two y's)
uv tool install graphifyy      # or: pipx install graphifyy

# uv installs to ~/.local/bin; make sure it is on PATH
export PATH="$HOME/.local/bin:$PATH"

# Optional: copy the skill into your assistant's global config dir
graphify install --platform claude

# Build/refresh the graph from code files (AST only, no LLM needed)
graphify update .

# Full extraction including docs/markdown (needs an LLM API key)
graphify extract .
```

`graphify claude install` is separate: it edits `CLAUDE.md` and adds a PreToolUse hook. Skip it unless you want that.

`/bm:graphify build` runs `graphify . --update`, but that form is not listed in the CLI help, so it may fail. If it does, use `graphify update .` directly. To use bm anyway, the project also needs `.planning/config.json` with `{"graphify": {"enabled": true}}`.

> Do not install the `Graphify-Labs/graphify-claude-plugin` marketplace plugin for this. It is a client for a hosted, authenticated service that indexes repos on their server, and it does not provide the local CLI.

## What each plugin does

| Plugin | Purpose |
| --- | --- |
| `skill-creator` | Create, edit, eval, and benchmark Claude skills. Use when scaffolding or tuning a skill. |
| `frontend-design` | Generates distinctive, production-grade frontend code (components, pages, apps) that avoids generic AI aesthetics. |
| `code-simplifier` | Simplifies and refines recently changed code for clarity and consistency while preserving behavior. |
| `bm` (Buildomator) | Plans, executes, and verifies coding work — phases, plans, milestones, audits, code review, UAT, ship. Each step runs in an isolated subcontext; project state lives in an MCP server and resumes after `/compact`. Commands use the `/bm:` prefix. Successor to GSD (`get-shit-done-cc`) and bundles its own SDK. |
| `context-mode` | Context-window protection. Provides `ctx_*` MCP tools that index large outputs (logs, fetches, batch commands) and let Claude search them instead of dumping into context. |
| `claude-mem` | Persistent cross-session memory database. Auto-captures observations and lets future sessions search prior work via `mem-search`. |
| `oh-my-claudecode` | Third-party plugin from `Yeachan-Heo/oh-my-claudecode`. Not reviewed yet; read its README before relying on it. |
| `context7` | Upstash-hosted docs lookup (bundles its MCP server) that fetches up-to-date library docs and code examples on demand. Use when answering API/library questions where freshness matters. |

## Notes

- `skill-creator`, `frontend-design`, `code-simplifier`, and `context7` live on the `claude-plugins-official` marketplace. It is usually preinstalled, so the `marketplace add` line is only needed if it's missing.
- `bm`, `context-mode`, `claude-mem`, and `oh-my-claudecode` need their marketplaces added first.
- Third-party marketplaces clone over SSH. On a fresh machine, run `ssh -T git@github.com` once and accept GitHub's host key, or `marketplace add` fails with "Host key verification failed".
- Migrating from GSD: remove any global SDK first (`npm uninstall -g get-shit-done-cc`), since a global `gsd-sdk`/`bm-sdk` binary overrides the one the plugin bundles. On first run, Buildomator backs up `~/.claude/get-shit-done/` to `get-shit-done-legacy/` and removes the old GSD skills, agents, and hooks. Update it via `/plugin` → Marketplace, not `/bm:update`.
- MCP install commands above default to user scope. Add `-s project` to write to a project's `.mcp.json` instead, or `-s local` for this-project-only.

