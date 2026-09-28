# Claude Code Plugins & MCP Servers

Reference list of plugins and MCP servers used with Claude Code in this vault. Reinstall with the commands below after a fresh setup.

> Antigravity skills live under `.agent/` — this file is Claude-only.

## Install commands

```bash
# Official marketplace (skill-creator, superpowers, frontend-design)
/plugin install skill-creator@claude-plugins-official
/plugin install superpowers@claude-plugins-official
/plugin install frontend-design@claude-plugins-official

# Buildomator (successor to GSD / get-shit-done-cc)
/plugin marketplace add buildomator/marketplace
/plugin install bm@buildomator
/reload-plugins

# context-mode (third-party marketplace)
/plugin marketplace add mksglu/context-mode
/plugin install context-mode@context-mode

# claude-mem (third-party marketplace)
/plugin marketplace add thedotmack/claude-mem
/plugin install claude-mem
```

## MCP servers

```bash
# context7 — Upstash docs/code lookup MCP
claude mcp add context7 -- npx -y @upstash/context7-mcp@latest
```

## What each plugin does

| Plugin | Purpose |
| --- | --- |
| `skill-creator` | Create, edit, eval, and benchmark Claude skills. Use when scaffolding or tuning a skill. |
| `superpowers` | Discipline framework — meta-skills for TDD, debugging, brainstorming, plan writing, code review, parallel agents, worktrees. Adds the "always invoke skills first" rule. |
| `frontend-design` | Generates distinctive, production-grade frontend code (components, pages, apps) that avoids generic AI aesthetics. |
| `bm` (Buildomator) | Plans, executes, and verifies coding work — phases, plans, milestones, audits, code review, UAT, ship. Each step runs in an isolated subcontext; project state lives in an MCP server and resumes after `/compact`. Commands use the `/bm:` prefix. Successor to GSD (`get-shit-done-cc`) and bundles its own SDK. |
| `context-mode` | Context-window protection. Provides `ctx_*` MCP tools that index large outputs (logs, fetches, batch commands) and let Claude search them instead of dumping into context. |
| `claude-mem` | Persistent cross-session memory database. Auto-captures observations and lets future sessions search prior work via `mem-search`. |

## What each MCP server does

| Server | Purpose |
| --- | --- |
| `context7` | Upstash-hosted MCP that fetches up-to-date library docs and code examples on demand. Use when answering API/library questions where freshness matters. |

## Notes

- `skill-creator`, `superpowers`, and `frontend-design` all live on the `claude-plugins-official` marketplace (preinstalled — no `marketplace add` needed).
- `bm`, `context-mode`, and `claude-mem` need their marketplaces added first.
- Third-party marketplaces clone over SSH. On a fresh machine, run `ssh -T git@github.com` once and accept GitHub's host key, or `marketplace add` fails with "Host key verification failed".
- Migrating from GSD: remove any global SDK first (`npm uninstall -g get-shit-done-cc`), since a global `gsd-sdk`/`bm-sdk` binary overrides the one the plugin bundles. On first run, Buildomator backs up `~/.claude/get-shit-done/` to `get-shit-done-legacy/` and removes the old GSD skills, agents, and hooks. Update it via `/plugin` → Marketplace, not `/bm:update`.
- MCP install commands above default to user scope. Add `-s project` to write to a project's `.mcp.json` instead, or `-s local` for this-project-only.

